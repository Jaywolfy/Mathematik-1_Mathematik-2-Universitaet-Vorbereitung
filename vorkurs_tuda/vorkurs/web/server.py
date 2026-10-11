# -*- coding: utf-8 -*-
"""Webserver der grafischen Oberfläche (nur Standardbibliothek).

Startet einen ThreadingHTTPServer auf 127.0.0.1, liefert die statischen Dateien
aus web/static und stellt die JSON-API aus ARCHITEKTUR.md (Abschnitt 9) bereit.

Aufruf:  python -m vorkurs.web.server [--port 8765] [--kein-browser]
"""

import argparse
import ast
import json
import random
import sys
import threading
import traceback
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

from .. import engine, fortschritt, markup, sandbox

STATIC = (Path(__file__).resolve().parent / "static").resolve()
MAX_BODY = 2 * 1024 * 1024          # 2 MB reichen für jeden Code
MAX_CODE = 100_000                  # Zeichen

MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".mjs": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".ico": "image/x-icon",
    ".woff2": "font/woff2",
    ".txt": "text/plain; charset=utf-8",
}

PRUEFUNGS_TEILE = ("tag1", "tag2", "tag3", "tag4")

# Nur für automatische Oberflächentests (`vorkurs_quiz.py --gui --e2e`): liefert Musterlösungen
# über /api/e2e/*. Ohne --e2e gibt es diese Adressen nicht (404 wie jede unbekannte Adresse).
E2E = False


class ApiFehler(Exception):
    """Fehler mit HTTP-Status und deutscher Meldung für den Client."""

    def __init__(self, status, text):
        super().__init__(text)
        self.status = status
        self.text = text


# ──────────────────────────────────────────────────────────────────────────
#  Zustand (Fortschritt im Speicher, Schreiben unter Lock)
# ──────────────────────────────────────────────────────────────────────────

class Zustand:
    def __init__(self):
        self.lock = threading.RLock()
        self.daten = fortschritt.laden()

    def speichern(self):
        if not fortschritt.speichern(self.daten):
            _log("Warnung: Fortschritt konnte nicht gespeichert werden.")


ZUSTAND = None


def _zustand():
    global ZUSTAND
    if ZUSTAND is None:
        ZUSTAND = Zustand()
    return ZUSTAND


def _log(text):
    try:
        print(text, file=sys.stderr, flush=True)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"), file=sys.stderr, flush=True)


# ──────────────────────────────────────────────────────────────────────────
#  Hilfen
# ──────────────────────────────────────────────────────────────────────────

def _flach(seiten):
    """markup.parse()-Seiten -> eine Blockliste."""
    bloecke = []
    for seite in seiten or []:
        bloecke.extend(seite)
    return bloecke


def _erklaerung_bloecke(text):
    if not text:
        return []
    try:
        return _flach(markup.parse(text))
    except Exception:  # Erklärung trotzdem als Text zeigen
        return []


def _frage(fid):
    f = engine.frage_nach_id(str(fid or ""))
    if f is None:
        raise ApiFehler(404, "Diese Frage gibt es nicht (mehr) – vermutlich wurden die Inhalte geändert. "
                             "Bitte lade die Seite neu (Taste F5).")
    return f


def _kapitel(slug):
    k = engine.kapitel_nach_slug(slug)
    if k is None:
        raise ApiFehler(404, f"Kapitel „{slug}“ nicht gefunden – vielleicht wurde es umbenannt. "
                             "Lade die Seite neu (F5) oder wähle ein Kapitel aus der Übersicht.")
    return k


def _text_bloecke(d):
    """Fragetext mit Markup (z. B. '## …', '• …') zusätzlich als Blöcke mitschicken."""
    text = d.get("aufgabe") or d.get("frage") or d.get("aussage") or ""
    if "\n" in text.strip():
        bloecke = _erklaerung_bloecke(text)
        if bloecke:
            d["text_bloecke"] = bloecke
    return d


def _frage_dict(f, daten, mit_kapitel=False):
    d = _text_bloecke(f.to_dict(mischen=True))
    if f.typ == "code":
        entwurf = daten["entwuerfe"].get(f.id)
        if entwurf:
            d["entwurf"] = entwurf
    if mit_kapitel and f.kapitel is not None:
        d["kapitel_titel"] = f.kapitel.titel
        d["kapitel_icon"] = f.kapitel.icon
    return d


def _zweiter_versuch_moeglich(f, versuch, ok):
    if ok or versuch >= 2:
        return False
    if f.typ == "wf":
        return False
    if f.typ == "mc" and len(getattr(f, "optionen", [])) <= 2:
        return False
    return True


def _statistik(daten):
    return fortschritt.statistik(daten)


def _code_text(body, feld="code"):
    code = body.get(feld, "")
    if not isinstance(code, str):
        raise ApiFehler(400, "Code muss Text sein.")
    if len(code) > MAX_CODE:
        raise ApiFehler(400, "Der Code ist zu lang.")
    return code


def _eingaben(body):
    e = body.get("eingaben") or []
    if isinstance(e, str):
        e = e.splitlines()
    if not isinstance(e, list):
        raise ApiFehler(400, "eingaben muss eine Liste sein.")
    return [str(x) for x in e][:200]


def _int(wert, name, minimum=0, maximum=10_000):
    try:
        z = int(wert)
    except (TypeError, ValueError):
        raise ApiFehler(400, f"{name} muss eine Zahl sein.")
    if not minimum <= z <= maximum:
        raise ApiFehler(400, f"{name} liegt außerhalb des erlaubten Bereichs.")
    return z


def _python_typ(text):
    try:
        return type(ast.literal_eval(str(text))).__name__
    except (ValueError, SyntaxError, TypeError, MemoryError, RecursionError):
        return "andere"


# ──────────────────────────────────────────────────────────────────────────
#  API-Endpunkte
# ──────────────────────────────────────────────────────────────────────────

def api_uebersicht(z, query, body):
    with z.lock:
        daten = z.daten
        teile = []
        for t in engine.TEILE:
            kap = [k for k in engine.KAPITEL if k.teil == t["id"]]
            if not kap:
                continue
            eintraege = []
            for k in kap:
                d = k.to_dict()
                d["fortschritt"] = fortschritt.kapitel_status(daten, k)
                eintraege.append(d)
            teile.append(dict(t, kapitel=eintraege))
        return {"teile": teile, "statistik": _statistik(daten),
                "einstellungen": dict(daten.get("einstellungen") or {})}


def api_kapitel(z, slug):
    k = _kapitel(slug)
    elemente = k.elemente_dicts(mischen=True)
    with z.lock:
        for e in elemente:
            if e.get("typ") == "frage":
                _text_bloecke(e["frage"])
            if e.get("typ") == "frage" and e["frage"].get("typ") == "code":
                entwurf = z.daten["entwuerfe"].get(e["frage"]["id"])
                if entwurf:
                    e["frage"]["entwurf"] = entwurf
        kd = k.to_dict()
        kd["fortschritt"] = fortschritt.kapitel_status(z.daten, k)
    alle = engine.KAPITEL
    i = alle.index(k)
    kd["vorheriges"] = alle[i - 1].slug if i > 0 else None
    kd["naechstes"] = alle[i + 1].slug if i + 1 < len(alle) else None
    kd["naechstes_titel"] = alle[i + 1].titel if i + 1 < len(alle) else None
    return {"kapitel": kd, "elemente": elemente}


def _antwort_bauen(f, erg, ok, zeige_loesung, info, daten):
    d = erg.to_dict(mit_loesung=zeige_loesung)
    if not zeige_loesung:
        d["erklaerung"] = ""          # Erklärung verrät die Lösung – erst nach dem 2. Versuch
    d["erklaerung_bloecke"] = _erklaerung_bloecke(d.get("erklaerung"))
    d["xp_neu"] = (info or {}).get("xp_neu", 0)
    d["neue_abzeichen"] = (info or {}).get("neue_abzeichen", [])
    d["statistik"] = _statistik(daten)
    return d


def api_antwort(z, query, body):
    f = _frage(body.get("id"))
    if f.typ == "code":
        return api_code_pruefen(z, query, {"id": f.id, "code": body.get("antwort", "")})
    versuch = 2 if str(body.get("versuch", 1)) == "2" else 1
    antwort = body.get("antwort")
    if f.typ == "wf" and isinstance(antwort, str):
        antwort = antwort.strip().lower() in ("true", "wahr", "w", "1", "ja")
    erg = f.pruefen(antwort)
    zweiter = _zweiter_versuch_moeglich(f, versuch, erg.ok)
    with z.lock:
        info = fortschritt.antwort_verbuchen(z.daten, f, erg.ok, versuch, endgueltig=not zweiter)
        z.speichern()
        d = _antwort_bauen(f, erg, erg.ok, erg.ok or not zweiter, info, z.daten)
    d["zweiter_versuch"] = zweiter
    d["versuch"] = versuch
    return d


def api_code_pruefen(z, query, body):
    f = _frage(body.get("id"))
    if f.typ != "code":
        raise ApiFehler(400, "Das ist keine Programmieraufgabe.")
    code = _code_text(body)
    erg = f.pruefen(code)
    with z.lock:
        fortschritt.entwurf_speichern(z.daten, f.id, code)
        info = None
        if erg.ok:
            info = fortschritt.antwort_verbuchen(z.daten, f, True, 1, endgueltig=True)
        z.speichern()
        # Musterlösung gibt es nur über /api/loesung; Erklärung erst nach dem Lösen
        d = _antwort_bauen(f, erg, erg.ok, False, info, z.daten)
        if erg.ok:
            d["erklaerung"] = f.erklaerung
            d["erklaerung_bloecke"] = _erklaerung_bloecke(f.erklaerung)
    d["zweiter_versuch"] = False
    return d


def api_entwurf(z, query, body):
    f = _frage(body.get("id"))
    code = _code_text(body)
    with z.lock:
        fortschritt.entwurf_speichern(z.daten, f.id, code)
        z.speichern()
    return {}


def api_loesung(z, query, body):
    f = _frage(body.get("id"))
    with z.lock:
        fortschritt.loesung_angesehen(z.daten, f)
        z.speichern()
        stat = _statistik(z.daten)
    return {"loesung": f.loesung_anzeigen(), "erklaerung": f.erklaerung,
            "erklaerung_bloecke": _erklaerung_bloecke(f.erklaerung), "statistik": stat}


def api_ausfuehren(z, query, body):
    return sandbox.ausfuehren(_code_text(body), _eingaben(body))


def api_trace(z, query, body):
    return sandbox.trace(_code_text(body), _eingaben(body))


def api_abschluss(z, slug, body):
    k = _kapitel(slug)
    maximum = _int(body.get("max"), "max", 0, 100_000)
    punkte = _int(body.get("punkte"), "punkte", 0, maximum)
    with z.lock:
        info = fortschritt.kapitel_abschliessen(z.daten, k, punkte, maximum)
        z.speichern()
        return {"statistik": _statistik(z.daten), "neue_abzeichen": info.get("neue_abzeichen", []),
                "xp_neu": info.get("xp_neu", 0), "neuer_rekord": info.get("neuer_rekord", False)}


def api_training(z, query, body):
    modus = (query.get("modus") or ["pruefung"])[0]
    try:
        anzahl = int((query.get("anzahl") or ["0"])[0] or 0)
    except ValueError:
        anzahl = 0
    # 0 = Standardanzahl des Modus (früher wurde daraus 1: Fehlerkiste/Wiederholen zeigten nur 1 Frage)
    anzahl = min(100, anzahl) if anzahl > 0 else 0
    alle = engine.alle_fragen()
    with z.lock:
        daten = z.daten
        if modus == "pruefung":
            anzahl = anzahl or 30
            pool = [f for f in alle.values() if f.typ != "code"
                    and f.kapitel is not None and f.kapitel.teil in PRUEFUNGS_TEILE]
            if len(pool) < anzahl:
                pool = [f for f in alle.values() if f.typ != "code"]
            auswahl = random.sample(pool, min(anzahl, len(pool)))
        elif modus == "fehlerkiste":
            anzahl = anzahl or 20
            ids = [fid for fid in daten["fehlerkiste"] if fid in alle]
            auswahl = [alle[fid] for fid in ids[:anzahl]]
        elif modus == "wiederholen":
            anzahl = anzahl or 15
            ids = fortschritt.faellige_fragen(daten, anzahl, alle)
            auswahl = [alle[fid] for fid in ids]
        else:
            raise ApiFehler(400, "Unbekannter Trainingsmodus (pruefung, fehlerkiste oder wiederholen).")
        fragen = [_frage_dict(f, daten, mit_kapitel=True) for f in auswahl]
    return {"modus": modus, "fragen": fragen}


def api_pruefung_ergebnis(z, query, body):
    maximum = _int(body.get("max"), "max", 1, 1000)
    punkte = _int(body.get("punkte"), "punkte", 0, maximum)
    with z.lock:
        info = fortschritt.pruefung_verbuchen(z.daten, punkte, maximum)
        z.speichern()
        return {"note": info["note"], "neue_abzeichen": info.get("neue_abzeichen", []),
                "statistik": _statistik(z.daten)}


def api_spickzettel(z, query, body):
    try:
        from ..inhalte.spickzettel import SPICKZETTEL
    except ImportError:
        SPICKZETTEL = ""
    kapitel = []
    for k in engine.KAPITEL:
        if k.zusammenfassung_text:
            kapitel.append({"slug": k.slug, "titel": k.titel, "icon": k.icon, "teil": k.teil,
                            "nummer": k.nummer, "seiten": markup.parse(k.zusammenfassung_text)})
    return {"seiten": markup.parse(SPICKZETTEL) if SPICKZETTEL else [], "kapitel": kapitel}


def api_visual_typen(z, query, body):
    werte = list(query.get("w") or [])
    if body and isinstance(body.get("werte"), list):
        werte = [str(w) for w in body["werte"]]
    typen = [_python_typ(w) for w in werte[:100]]
    return {"typen": typen, "typ": typen[0] if typen else None}


def api_zuruecksetzen(z, query, body):
    if body.get("bestaetigt") is not True:
        raise ApiFehler(400, "Zurücksetzen muss bestätigt werden.")
    with z.lock:
        fortschritt.zuruecksetzen(z.daten)
        z.speichern()
        return {"statistik": _statistik(z.daten)}


def api_einstellungen(z, query, body):
    erlaubt = {k: v for k, v in body.items()
               if isinstance(k, str) and len(k) < 40 and isinstance(v, (str, int, float, bool, type(None)))}
    with z.lock:
        fortschritt.einstellungen_setzen(z.daten, erlaubt)
        z.speichern()
    return {}


def _e2e_antwort(f):
    """Richtige Antwort im Format von /api/antwort bzw. /api/code/pruefen (nur Testmodus)."""
    if f.typ == "mc":
        return f.optionen[0]
    if f.typ == "wf":
        return f.wahr
    if f.typ == "text":
        return f.antworten[0]
    if f.typ == "ausgabe":
        ausgabe, fehler = f.soll()
        return fehler if fehler else (ausgabe if ausgabe else "nichts")
    if f.typ == "ausdruck":
        return f.loesung
    if f.typ == "luecke":
        return [a[0] for a in f.antworten]
    if f.typ == "puzzle":
        return f._loesungs_ids()
    return f.loesung_anzeigen()


def api_e2e_antwort(z, query, body):
    f = _frage((query.get("id") or [""])[0])
    return {"antwort": _e2e_antwort(f), "typ": f.typ}


def api_e2e_bericht(z, query, body):
    _log("E2E-BERICHT " + json.dumps(body, ensure_ascii=False))
    return {}


def api_status(z, query, body):
    from .. import VERSION
    return {"ok": True, "version": VERSION, "kapitel": len(engine.KAPITEL)}


GET_ROUTEN = {
    "/api/uebersicht": api_uebersicht,
    "/api/training": api_training,
    "/api/spickzettel": api_spickzettel,
    "/api/visual/typen": api_visual_typen,
    "/api/status": api_status,
}
POST_ROUTEN = {
    "/api/antwort": api_antwort,
    "/api/code/pruefen": api_code_pruefen,
    "/api/entwurf": api_entwurf,
    "/api/loesung": api_loesung,
    "/api/ausfuehren": api_ausfuehren,
    "/api/trace": api_trace,
    "/api/pruefung/ergebnis": api_pruefung_ergebnis,
    "/api/fortschritt/zuruecksetzen": api_zuruecksetzen,
    "/api/einstellungen": api_einstellungen,
    "/api/visual/typen": api_visual_typen,
}


# ──────────────────────────────────────────────────────────────────────────
#  HTTP-Handler
# ──────────────────────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    server_version = "VorkursQuiz/2"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # keine Zeile pro Anfrage im Terminal
        pass

    # --- Antworten ---
    def _senden(self, status, inhalt, typ, cache="no-store"):
        try:
            self.send_response(status)
            self.send_header("Content-Type", typ)
            self.send_header("Content-Length", str(len(inhalt)))
            self.send_header("Cache-Control", cache)
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(inhalt)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass

    def _json(self, status, daten):
        inhalt = json.dumps(daten, ensure_ascii=False, default=str).encode("utf-8")
        self._senden(status, inhalt, "application/json; charset=utf-8")

    def _fehler(self, status, text):
        self._json(status, {"fehler": text})

    # --- Sicherheit: nur von dieser Seite aus (kein fremdes Web darf Code ausführen) ---
    def _host_ok(self):
        host = (self.headers.get("Host") or "").lower()
        name = host.rsplit(":", 1)[0] if not host.startswith("[") else host.split("]")[0] + "]"
        return name in ("127.0.0.1", "localhost", "[::1]")

    def _origin_ok(self):
        origin = self.headers.get("Origin")
        if not origin or origin == "null":
            return origin is None
        try:
            teile = urlsplit(origin)
        except ValueError:
            return False
        return (teile.hostname in ("127.0.0.1", "localhost", "::1")
                and teile.port == self.server.server_address[1])

    def _body(self):
        try:
            laenge = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            raise ApiFehler(400, "Ungültige Anfrage.")
        if laenge > MAX_BODY:
            raise ApiFehler(413, "Anfrage zu groß.")
        roh = self.rfile.read(laenge) if laenge else b""
        if not roh:
            return {}
        try:
            daten = json.loads(roh.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            raise ApiFehler(400, "Ungültiges JSON.")
        if not isinstance(daten, dict):
            raise ApiFehler(400, "Erwartet wird ein JSON-Objekt.")
        return daten

    def _api(self, methode, pfad, query):
        z = _zustand()
        body = {}
        if methode == "POST":
            typ = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            if typ != "application/json":
                raise ApiFehler(415, "Bitte JSON senden (Content-Type: application/json).")
            body = self._body()
        if pfad.startswith("/api/e2e/") and E2E:
            if methode == "GET" and pfad == "/api/e2e/antwort":
                return api_e2e_antwort(z, query, body)
            if methode == "POST" and pfad == "/api/e2e/bericht":
                return api_e2e_bericht(z, query, body)
        if methode == "GET":
            if pfad in GET_ROUTEN:
                return GET_ROUTEN[pfad](z, query, body)
            if pfad.startswith("/api/kapitel/"):
                slug = pfad[len("/api/kapitel/"):]
                if "/" not in slug and slug:
                    return api_kapitel(z, slug)
        else:
            if pfad in POST_ROUTEN:
                return POST_ROUTEN[pfad](z, query, body)
            if pfad.startswith("/api/kapitel/") and pfad.endswith("/abschluss"):
                slug = pfad[len("/api/kapitel/"):-len("/abschluss")]
                return api_abschluss(z, slug, body)
            if pfad == "/api/beenden":
                threading.Thread(target=self.server.shutdown, daemon=True).start()
                return {}
        raise ApiFehler(404, "Unbekannte Adresse.")

    def _anfrage(self, methode):
        try:
            teile = urlsplit(self.path)
            pfad = unquote(teile.path)
            query = parse_qs(teile.query)
            if not self._host_ok():
                return self._fehler(403, "Zugriff nur über 127.0.0.1 erlaubt.")
            if pfad.startswith("/api/"):
                if methode == "POST" and not self._origin_ok():
                    return self._fehler(403, "Anfrage von fremder Seite abgelehnt.")
                antwort = self._api(methode, pfad.rstrip("/") or "/", query)
                return self._json(200, antwort)
            if methode != "GET" and methode != "HEAD":
                return self._fehler(405, "Methode nicht erlaubt.")
            return self._statisch(pfad)
        except ApiFehler as e:
            return self._fehler(e.status, e.text)
        except Exception as e:  # noqa: BLE001 – alles abfangen, Server soll weiterlaufen
            _log(f"[Fehler] {methode} {self.path}\n" + traceback.format_exc())
            return self._fehler(500, f"Interner Fehler: {type(e).__name__}: {e}")

    def _statisch(self, pfad):
        if pfad in ("/", "/index.html"):
            datei = STATIC / "index.html"
        elif pfad.startswith("/static/"):
            datei = (STATIC / pfad[len("/static/"):]).resolve()
        elif pfad == "/favicon.ico":
            datei = STATIC / "favicon.svg"
        else:
            return self._fehler(404, "Nicht gefunden.")
        try:
            datei.relative_to(STATIC)          # Pfad-Traversal verhindern
        except ValueError:
            return self._fehler(403, "Zugriff verweigert.")
        if not datei.is_file():
            return self._fehler(404, "Nicht gefunden.")
        typ = MIME.get(datei.suffix.lower(), "application/octet-stream")
        self._senden(200, datei.read_bytes(), typ, cache="no-cache")

    def do_GET(self):
        self._anfrage("GET")

    def do_HEAD(self):
        self._anfrage("HEAD")

    def do_POST(self):
        self._anfrage("POST")

    def do_OPTIONS(self):
        # Keine CORS-Freigaben: Fremde Seiten bekommen keinen Zugriff.
        self._fehler(405, "Nicht erlaubt.")


class Server(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False   # Windows: sonst könnten zwei Server denselben Port belegen
    # Standard wäre 5: Der Browser lädt beim Start ~15 Module gleichzeitig, mit zwei Tabs
    # lehnte Windows dann Verbindungen ab ("Failed to fetch" / "Keine Verbindung").
    request_queue_size = 128

    def handle_error(self, request, client_address):
        # Abgebrochene Verbindungen (Browser-Tab zu, Neuladen) sind normal – kein Traceback.
        fehler = sys.exc_info()[1]
        if isinstance(fehler, (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, TimeoutError)):
            return
        _log(f"[Fehler] Verbindung {client_address}\n" + traceback.format_exc())


# ──────────────────────────────────────────────────────────────────────────
#  Start
# ──────────────────────────────────────────────────────────────────────────

def server_erstellen(port=8765, versuche=30):
    """Erstellt den Server auf dem ersten freien Port ab `port`."""
    letzter = None
    for p in range(port, port + versuche):
        try:
            return Server(("127.0.0.1", p), Handler)
        except OSError as e:
            letzter = e
    raise OSError(f"Kein freier Port zwischen {port} und {port + versuche - 1} gefunden ({letzter}).")


def _ausgeben(text):
    try:
        print(text, flush=True)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"), flush=True)


def main(port=8765, browser=True, e2e=False):
    """Startet die grafische Oberfläche. Blockiert bis Strg+C oder 'Beenden'.
       e2e=True: Testmodus (Musterlösungen über /api/e2e/antwort) – nur für automatische Tests."""
    global E2E
    E2E = bool(e2e)
    _zustand()  # Fortschritt laden (inkl. Migration) – Fehler früh sehen
    server = server_erstellen(port)
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    _ausgeben("")
    _ausgeben("  🐍  Python-Vorkurs · Lernquiz (grafische Oberfläche)")
    _ausgeben(f"  Lernquiz läuft auf {url} – zum Beenden Strg+C")
    if server.server_address[1] != port:
        _ausgeben(f"  (Port {port} war belegt, deshalb {server.server_address[1]}.)")
    if E2E:
        _ausgeben("  ACHTUNG: Testmodus (--e2e) – der Server verrät Musterlösungen. Nur für Tests!")
    if browser:
        _ausgeben("  Der Browser öffnet sich gleich. Falls nicht: Adresse oben kopieren.")
    _ausgeben("")
    threading.Thread(target=_vorberechnen, daemon=True).start()
    if browser:
        threading.Timer(0.5, _browser_oeffnen, args=(url,)).start()
    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        with _zustand().lock:
            _zustand().speichern()
        _ausgeben("  Lernquiz beendet. Dein Fortschritt ist gespeichert. Bis bald! 👋")
    return 0


def _vorberechnen():
    try:
        engine.vorberechnen()
    except Exception:  # noqa: BLE001 – nur Beschleunigung
        pass


def _browser_oeffnen(url):
    try:
        webbrowser.open(url)
    except Exception:  # noqa: BLE001
        _ausgeben(f"  Browser konnte nicht geöffnet werden – bitte {url} selbst öffnen.")


def _cli(argv=None):
    p = argparse.ArgumentParser(description="Vorkurs-Lernquiz – grafische Oberfläche")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--kein-browser", action="store_true")
    p.add_argument("--e2e", action="store_true", help=argparse.SUPPRESS)
    a = p.parse_args(argv)
    for strom in (sys.stdout, sys.stderr):
        try:
            strom.reconfigure(encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass
    return main(port=a.port, browser=not a.kein_browser, e2e=a.e2e)


if __name__ == "__main__":
    sys.exit(_cli())
