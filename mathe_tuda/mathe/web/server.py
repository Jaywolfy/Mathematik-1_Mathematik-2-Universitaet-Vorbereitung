# -*- coding: utf-8 -*-
"""Webserver der grafischen Oberfläche (nur Standardbibliothek).

Startet einen ThreadingHTTPServer auf 127.0.0.1, liefert die statischen Dateien aus
web/static (inklusive KaTeX unter static/vendor/katex) und die JSON-API aus
ARCHITEKTUR.md (Abschnitt 9).

Aufruf:  python3 -m mathe.web.server [--port 8766] [--kein-browser]
"""

import argparse
import json
import random
import sys
import threading
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

from .. import engine, fortschritt, markup, pruefer

STATIC = (Path(__file__).resolve().parent / "static").resolve()
MAX_BODY = 1024 * 1024
STANDARD_PORT = 8766

MIME = {
    ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8", ".mjs": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png",
    ".ico": "image/x-icon", ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf",
    ".txt": "text/plain; charset=utf-8",
}

E2E = False


class ApiFehler(Exception):
    def __init__(self, status, text):
        super().__init__(text)
        self.status = status
        self.text = text


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

def _bloecke(text):
    if not text:
        return []
    try:
        return [b for s in markup.parse(text) for b in s]
    except Exception:  # noqa: BLE001
        return [{"typ": "absatz", "text": str(text)}]


def _frage(fid):
    f = engine.frage_nach_id(str(fid or ""))
    if f is None:
        raise ApiFehler(404, "Diese Aufgabe gibt es nicht (mehr) – vermutlich wurden die Inhalte geändert. "
                             "Bitte lade die Seite neu (Taste F5).")
    return f


def _konkret(f, seed):
    if isinstance(f, engine.Generator):
        if seed in (None, ""):
            raise ApiFehler(400, "Für diese Übungsaufgabe fehlt die Nummer (seed). Bitte neu laden.")
        try:
            return f.instanz(int(seed))
        except (TypeError, ValueError):
            raise ApiFehler(400, "Ungültige Aufgabennummer.")
    return f


def _kapitel(slug):
    k = engine.kapitel_nach_slug(slug)
    if k is None:
        raise ApiFehler(404, f"Kapitel „{slug}“ nicht gefunden. Lade die Seite neu (F5) oder wähle ein "
                             "Kapitel aus der Übersicht.")
    return k


def _frage_dict(q, daten, mit_kapitel=False):
    d = q.to_dict()
    d["frage_bloecke"] = _bloecke(d.get("frage"))
    entwurf = daten["entwuerfe"].get(f"{q.id}:{q.seed}" if q.seed else q.id)
    if entwurf:
        d["entwurf"] = entwurf
    if mit_kapitel and q.kapitel is not None:
        d["kapitel_titel"] = q.kapitel.titel
        d["kapitel_icon"] = q.kapitel.icon
    if getattr(q, "generator_titel", None):
        d["generator_titel"] = q.generator_titel
    return d


def _zweiter_versuch_moeglich(q, versuch, erg):
    if erg.ok or versuch >= 2:
        return False
    if q.typ in ("wf", "papier"):
        return False
    if q.typ == "mc" and len(getattr(q, "optionen", [])) <= 2:
        return False
    return True


def _int(wert, name, minimum=0, maximum=100_000):
    try:
        z = int(wert)
    except (TypeError, ValueError):
        raise ApiFehler(400, f"{name} muss eine Zahl sein.")
    if not minimum <= z <= maximum:
        raise ApiFehler(400, f"{name} liegt außerhalb des erlaubten Bereichs.")
    return z


# ──────────────────────────────────────────────────────────────────────────
#  API
# ──────────────────────────────────────────────────────────────────────────

def api_uebersicht(z, query, body):
    with z.lock:
        daten = z.daten
        teile = []
        for t in engine.TEILE:
            kap = engine.kapitel_von_teil(t["id"])
            if not kap:
                continue
            eintraege = []
            for k in kap:
                d = k.to_dict()
                d["fortschritt"] = fortschritt.kapitel_status(daten, k)
                eintraege.append(d)
            teile.append(dict(t, kapitel=eintraege))
        return {"teile": teile, "statistik": fortschritt.statistik(daten),
                "einstellungen": dict(daten.get("einstellungen") or {})}


def api_kapitel(z, slug):
    k = _kapitel(slug)
    elemente = k.elemente_dicts()
    with z.lock:
        for e in elemente:
            if e.get("typ") == "frage":
                q = e["frage"]
                q["frage_bloecke"] = _bloecke(q.get("frage"))
                entwurf = z.daten["entwuerfe"].get(q["id"])
                if entwurf:
                    q["entwurf"] = entwurf
        kd = k.to_dict()
        kd["fortschritt"] = fortschritt.kapitel_status(z.daten, k)
    kd["warum_bloecke"] = _bloecke(k.warum_text)
    alle = engine.KAPITEL
    i = alle.index(k)
    kd["vorheriges"] = alle[i - 1].slug if i > 0 else None
    kd["naechstes"] = alle[i + 1].slug if i + 1 < len(alle) else None
    kd["naechstes_titel"] = alle[i + 1].titel if i + 1 < len(alle) else None
    return {"kapitel": kd, "elemente": elemente}


def api_generator_neu(z, query, body):
    f = _frage((query.get("id") or [""])[0])
    if not isinstance(f, engine.Generator):
        raise ApiFehler(400, "Das ist keine Übungsmaschine.")
    with z.lock:
        return {"frage": _frage_dict(f.instanz(), z.daten, mit_kapitel=True)}


def _antwort_dict(q, erg, final, info, daten):
    d = erg.to_dict(mit_loesung=final)
    if not final:
        d["erklaerung"] = ""
    d["erklaerung_bloecke"] = _bloecke(d.get("erklaerung"))
    d["rechenweg_bloecke"] = _bloecke(d.get("rechenweg"))
    d["xp_neu"] = (info or {}).get("xp_neu", 0)
    d["neue_abzeichen"] = (info or {}).get("neue_abzeichen", [])
    d["statistik"] = fortschritt.statistik(daten)
    return d


def api_antwort(z, query, body):
    f = _frage(body.get("id"))
    q = _konkret(f, body.get("seed"))
    versuch = 2 if str(body.get("versuch", 1)) == "2" else 1
    antwort = body.get("antwort")
    if q.typ == "rechenweg":
        antwort = {"schritt": body.get("schritt", 0), "antwort": antwort}
    erg = q.pruefen(antwort)
    if erg.lesefehler:
        with z.lock:
            d = _antwort_dict(q, erg, False, None, z.daten)
        d.update(zweiter_versuch=True, versuch=versuch, final=False)
        return d
    zweiter = _zweiter_versuch_moeglich(q, versuch, erg)
    final = not zweiter
    with z.lock:
        info = None
        if q.typ == "papier":
            info = fortschritt.papier_verbuchen(z.daten, f, body.get("antwort") or [])
        elif q.typ == "rechenweg":
            schritt = _int(body.get("schritt", 0), "schritt", 0, 10)
            letzter = schritt == len(q.schritte) - 1
            if final and letzter:
                bisher = [bool(x) for x in (body.get("bisher") or [])]
                alles = all(bisher) and erg.ok
                info = fortschritt.antwort_verbuchen(z.daten, f, alles, 1 if alles and versuch == 1 else 2,
                                                     endgueltig=True)
                erg.teilpunkte = (sum(bisher) + erg.ok) / len(q.schritte)
        else:
            info = fortschritt.antwort_verbuchen(z.daten, f, erg.ok, versuch, endgueltig=final,
                                                 generator=isinstance(f, engine.Generator))
        z.speichern()
        d = _antwort_dict(q, erg, final, info, z.daten)
    d.update(zweiter_versuch=zweiter, versuch=versuch, final=final)
    return d


def api_loesung(z, query, body):
    f = _frage(body.get("id"))
    q = _konkret(f, body.get("seed"))
    with z.lock:
        if q.typ != "papier":
            fortschritt.loesung_angesehen(z.daten, f)
            z.speichern()
        stat = fortschritt.statistik(z.daten)
    loesung = q.loesung_anzeigen()
    return {"loesung": loesung, "erklaerung": q.erklaerung, "rechenweg": q.rechenweg,
            "erklaerung_bloecke": _bloecke(q.erklaerung), "rechenweg_bloecke": _bloecke(q.rechenweg),
            "loesung_bloecke": _bloecke(loesung), "statistik": stat}


def api_papier_loesung(z, query, body):
    q = _konkret(_frage(body.get("id")), body.get("seed"))
    if q.typ != "papier":
        raise ApiFehler(400, "Das ist keine Papier-Aufgabe.")
    d = q.bewertung_dict()
    d["musterloesung_bloecke"] = _bloecke(d["musterloesung"])
    return d


def api_term_vorschau(z, query, body):
    """Zeigt, wie der Prüfer eine Eingabe versteht (Live-Vorschau des Eingabe-Pads)."""
    text = str(body.get("text") or "")[:400]
    typ = body.get("typ") or "term"
    variablen = body.get("variablen") or None
    if not text.strip():
        return {"latex": "", "fehler": None}
    try:
        if typ == "zahl":
            t, _ = pruefer.zahl_parsen(text)
            return {"latex": t.latex(), "fehler": None}
        if typ == "bereich":
            return {"latex": "\\mathbb{L} = " + pruefer.bereich_latex(pruefer.bereich_parsen(text)), "fehler": None}
        if typ == "menge":
            return {"latex": pruefer.menge_latex(pruefer.menge_parsen(text)), "fehler": None}
        t = pruefer.parse(text, variablen)
        d = {"latex": t.latex(), "fehler": None}
        if body.get("ast"):
            d["ast"] = pruefer.ast_json(t.ast)
            d["variablen"] = sorted(t.variablen)
        return d
    except pruefer.TermFehler as e:
        return {"latex": None, "fehler": e.meldung, "pos": e.pos}
    except pruefer.Undefiniert as e:
        return {"latex": None, "fehler": f"Nicht definiert: {e}"}


def api_abschluss(z, slug, body):
    k = _kapitel(slug)
    maximum = _int(body.get("max"), "max", 0, 100_000)
    punkte = _int(body.get("punkte"), "punkte", 0, maximum)
    with z.lock:
        info = fortschritt.kapitel_abschliessen(z.daten, k, punkte, maximum)
        z.speichern()
        return {"statistik": fortschritt.statistik(z.daten), "neue_abzeichen": info.get("neue_abzeichen", []),
                "xp_neu": info.get("xp_neu", 0), "neuer_rekord": info.get("neuer_rekord", False)}


def api_training(z, query, body):
    modus = (query.get("modus") or ["wiederholen"])[0]
    try:
        anzahl = min(100, max(0, int((query.get("anzahl") or ["0"])[0] or 0)))
    except ValueError:
        anzahl = 0
    alle = engine.alle_fragen()
    with z.lock:
        daten = z.daten
        if modus == "fehlerkiste":
            ids = [fid for fid in daten["fehlerkiste"] if fid in alle]
            auswahl = [alle[fid] for fid in ids[:anzahl or 20]]
        elif modus == "wiederholen":
            ids = fortschritt.faellige_fragen(daten, anzahl or 15, alle)
            auswahl = [alle[fid] for fid in ids]
        elif modus == "thema":
            k = _kapitel((query.get("kapitel") or [""])[0])
            gens = k.generatoren() or [f for f in k.fragen() if f.typ != "papier"]
            auswahl = [random.choice(gens) for _ in range(anzahl or 10)]
        elif modus == "klausur":
            modul = (query.get("modul") or ["mathe1"])[0]
            auswahl = _klausur_auswahl(modul, anzahl or 12)
        else:
            raise ApiFehler(400, "Unbekannter Trainingsmodus.")
        fragen = [_frage_dict(f.instanz() if isinstance(f, engine.Generator) else f, daten, mit_kapitel=True)
                  for f in auswahl]
    return {"modus": modus, "fragen": fragen}


def _klausur_auswahl(modul, anzahl):
    kap = engine.kapitel_von_teil(modul) + [k for k in engine.kapitel_von_teil("klausur") if modul in k.slug]
    pool = [f for k in kap for f in k.fragen() if f.typ not in ("wf",)]
    bevorzugt = [f for f in pool if f.phase == "praxis" or f.typ in ("papier", "mehrfach", "generator")]
    rest = [f for f in pool if f not in bevorzugt]
    random.shuffle(bevorzugt)
    random.shuffle(rest)
    return (bevorzugt + rest)[:anzahl]


def api_klausur_ergebnis(z, query, body):
    maximum = _int(body.get("max"), "max", 1, 10_000)
    punkte = float(body.get("punkte") or 0)
    if not 0 <= punkte <= maximum:
        raise ApiFehler(400, "punkte liegt außerhalb des erlaubten Bereichs.")
    with z.lock:
        info = fortschritt.klausur_verbuchen(z.daten, str(body.get("modul") or "")[:20], punkte, maximum,
                                             body.get("dauer"))
        z.speichern()
        return {"note": info["note"], "neue_abzeichen": info.get("neue_abzeichen", []),
                "statistik": fortschritt.statistik(z.daten)}


def api_diagnose(z, query, body):
    from ..inhalte import diagnose
    with z.lock:
        return {"fragen": [_frage_dict(q, z.daten, mit_kapitel=True) for q in diagnose.fragen_ziehen()],
                "letzte": z.daten.get("diagnose")}


def api_diagnose_ergebnis(z, query, body):
    from ..inhalte import diagnose
    ergebnisse = body.get("ergebnisse") or {}
    if not isinstance(ergebnisse, dict):
        raise ApiFehler(400, "ergebnisse muss ein Objekt sein.")
    auswertung = diagnose.auswerten({str(k): [int(v[0]), int(v[1])] for k, v in ergebnisse.items()})
    with z.lock:
        info = fortschritt.diagnose_verbuchen(z.daten, auswertung["kapitel"], auswertung["empfehlung"])
        z.speichern()
        auswertung.update(statistik=fortschritt.statistik(z.daten), neue_abzeichen=info["neue_abzeichen"],
                          xp_neu=info["xp_neu"])
    return auswertung


def api_formelsammlung(z, query, body):
    from ..inhalte import FORMELSAMMLUNG
    kapitel = [{"slug": k.slug, "titel": k.titel, "icon": k.icon, "teil": k.teil, "nummer": k.nummer,
                "seiten": markup.parse(k.zusammenfassung_text)} for k in engine.KAPITEL if k.zusammenfassung_text]
    return {"seiten": markup.parse(FORMELSAMMLUNG), "kapitel": kapitel,
            "teile": [{"id": t["id"], "titel": t["titel"]} for t in engine.TEILE]}


def api_glossar(z, query, body):
    from ..inhalte import glossar
    eintraege = []
    for g in sorted(glossar.GLOSSAR, key=lambda g: g["begriff"].lower()):
        k = engine.kapitel_nach_slug(g["kapitel"]) if g["kapitel"] else None
        eintraege.append(dict(g, kapitel_titel=k.titel if k else None))
    return {"eintraege": eintraege}


def api_spielwiese(z, werkzeug, body):
    from .. import spielwiese
    fn = spielwiese.WERKZEUGE.get(werkzeug)
    if fn is None:
        raise ApiFehler(404, "Dieses Werkzeug gibt es nicht.")
    try:
        erg = fn(body)
    except (pruefer.TermFehler, ValueError, ArithmeticError) as e:
        return {"fehler": getattr(e, "meldung", None) or str(e)}
    erg["rechenweg_bloecke"] = _bloecke(erg.get("rechenweg"))
    return erg


def api_entwurf(z, query, body):
    f = _frage(body.get("id"))
    schluessel = f"{f.id}:{body.get('seed')}" if body.get("seed") else f.id
    text = body.get("text")
    if text is not None and not isinstance(text, str):
        text = json.dumps(text, ensure_ascii=False)
    with z.lock:
        fortschritt.entwurf_speichern(z.daten, schluessel, text)
        z.speichern()
    return {}


def api_einstellungen(z, query, body):
    erlaubt = {k: v for k, v in body.items()
               if isinstance(k, str) and len(k) < 40 and isinstance(v, (str, int, float, bool, type(None)))}
    with z.lock:
        fortschritt.einstellungen_setzen(z.daten, erlaubt)
        z.speichern()
    return {}


def api_zuruecksetzen(z, query, body):
    if body.get("bestaetigt") is not True:
        raise ApiFehler(400, "Zurücksetzen muss bestätigt werden.")
    with z.lock:
        fortschritt.zuruecksetzen(z.daten)
        z.speichern()
        return {"statistik": fortschritt.statistik(z.daten)}


def api_demo_visuals(z, query, body):
    from .. import demo
    bloecke = [{"typ": "visual", **v} for v in demo.demo_daten()]
    bloecke.append({"typ": "rechnung", "titel": "Beispiel vorgerechnet", "schritte": [
        {"tex": "\\frac{1}{2} + \\frac{1}{3}", "grund": "Aufgabe", "falsch": False},
        {"tex": "= \\frac{\\hl{3}}{6} + \\frac{\\hl{2}}{6}", "grund": "auf den Hauptnenner $6$ erweitern", "falsch": False},
        {"tex": "= \\frac{5}{6}", "grund": "Zähler addieren, Nenner bleibt", "falsch": False},
        {"tex": "\\frac{1}{2} + \\frac{1}{3} = \\frac{2}{5}", "grund": "Zähler und Nenner einzeln addiert", "falsch": True}]})
    return {"bloecke": bloecke}


def api_status(z, query, body):
    from .. import VERSION
    return {"ok": True, "version": VERSION, "kapitel": len(engine.KAPITEL)}


def api_e2e_antwort(z, query, body):
    f = _frage((query.get("id") or [""])[0])
    q = _konkret(f, (query.get("seed") or [None])[0])
    schritt = int((query.get("schritt") or ["0"])[0])
    a = engine.musterantwort(q, schritt)
    if q.typ == "rechenweg":
        a = a["antwort"]
    return {"antwort": a, "typ": q.typ}


def api_e2e_formeln(z, query, body):
    from .. import selbsttest
    return {"formeln": sorted(set(selbsttest.alle_formeln()))}


def api_e2e_bericht(z, query, body):
    _log("E2E-BERICHT " + json.dumps(body, ensure_ascii=False))
    return {}


GET_ROUTEN = {
    "/api/uebersicht": api_uebersicht, "/api/training": api_training, "/api/diagnose": api_diagnose,
    "/api/formelsammlung": api_formelsammlung, "/api/glossar": api_glossar, "/api/status": api_status,
    "/api/generator/neu": api_generator_neu, "/api/demo/visuals": api_demo_visuals,
}
POST_ROUTEN = {
    "/api/antwort": api_antwort, "/api/loesung": api_loesung, "/api/papier/loesung": api_papier_loesung,
    "/api/term/vorschau": api_term_vorschau, "/api/klausur/ergebnis": api_klausur_ergebnis,
    "/api/diagnose/ergebnis": api_diagnose_ergebnis, "/api/entwurf": api_entwurf,
    "/api/einstellungen": api_einstellungen, "/api/fortschritt/zuruecksetzen": api_zuruecksetzen,
}


def _json_sicher(x):
    """JavaScript versteht kein Infinity/NaN in JSON: ±inf -> "inf"/"-inf", NaN -> None."""
    if isinstance(x, float):
        if x != x:
            return None
        if x in (float("inf"), float("-inf")):
            return "inf" if x > 0 else "-inf"
        return x
    if isinstance(x, dict):
        return {k: _json_sicher(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json_sicher(v) for v in x]
    return x


class Handler(BaseHTTPRequestHandler):
    server_version = "MatheQuiz/1"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass

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
        text = json.dumps(_json_sicher(daten), ensure_ascii=False, default=str, allow_nan=False)
        self._senden(status, text.encode("utf-8"), "application/json; charset=utf-8")

    def _fehler(self, status, text):
        self._json(status, {"fehler": text})

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
        return teile.hostname in ("127.0.0.1", "localhost", "::1") and teile.port == self.server.server_address[1]

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
            if pfad == "/api/e2e/antwort":
                return api_e2e_antwort(z, query, body)
            if pfad == "/api/e2e/formeln":
                return api_e2e_formeln(z, query, body)
            if pfad == "/api/e2e/bericht":
                return api_e2e_bericht(z, query, body)
        if methode == "GET":
            if pfad in GET_ROUTEN:
                return GET_ROUTEN[pfad](z, query, body)
            if pfad.startswith("/api/kapitel/"):
                slug = pfad[len("/api/kapitel/"):]
                if slug and "/" not in slug:
                    return api_kapitel(z, slug)
        else:
            if pfad in POST_ROUTEN:
                return POST_ROUTEN[pfad](z, query, body)
            if pfad.startswith("/api/kapitel/") and pfad.endswith("/abschluss"):
                return api_abschluss(z, pfad[len("/api/kapitel/"):-len("/abschluss")], body)
            if pfad.startswith("/api/spielwiese/"):
                return api_spielwiese(z, pfad[len("/api/spielwiese/"):], body)
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
                return self._json(200, self._api(methode, pfad.rstrip("/") or "/", query))
            if methode not in ("GET", "HEAD"):
                return self._fehler(405, "Methode nicht erlaubt.")
            return self._statisch(pfad)
        except ApiFehler as e:
            return self._fehler(e.status, e.text)
        except Exception as e:  # noqa: BLE001
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
            datei.relative_to(STATIC)
        except ValueError:
            return self._fehler(403, "Zugriff verweigert.")
        if not datei.is_file():
            return self._fehler(404, "Nicht gefunden.")
        typ = MIME.get(datei.suffix.lower(), "application/octet-stream")
        cache = "max-age=86400" if "/vendor/" in str(datei) else "no-cache"
        self._senden(200, datei.read_bytes(), typ, cache=cache)

    def do_GET(self):
        self._anfrage("GET")

    def do_HEAD(self):
        self._anfrage("HEAD")

    def do_POST(self):
        self._anfrage("POST")

    def do_OPTIONS(self):
        self._fehler(405, "Nicht erlaubt.")


class Server(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False
    request_queue_size = 128

    def handle_error(self, request, client_address):
        fehler = sys.exc_info()[1]
        if isinstance(fehler, (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, TimeoutError)):
            return
        _log(f"[Fehler] Verbindung {client_address}\n" + traceback.format_exc())


def server_erstellen(port=STANDARD_PORT, versuche=30):
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


def main(port=STANDARD_PORT, browser=True, e2e=False):
    global E2E
    E2E = bool(e2e)
    _zustand()
    server = server_erstellen(port)
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    _ausgeben("")
    _ausgeben("  ∑  Mathe für Informatik · Lernsystem (grafische Oberfläche)")
    _ausgeben(f"  Läuft auf {url} – zum Beenden Strg+C")
    if server.server_address[1] != port:
        _ausgeben(f"  (Port {port} war belegt, deshalb {server.server_address[1]}.)")
    if E2E:
        _ausgeben("  ACHTUNG: Testmodus (--e2e) – der Server verrät Musterlösungen. Nur für Tests!")
    if browser:
        _ausgeben("  Der Browser öffnet sich gleich. Falls nicht: Adresse oben kopieren.")
    _ausgeben("")
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
        _ausgeben("  Lernsystem beendet. Dein Fortschritt ist gespeichert. Bis bald! 👋")
    return 0


def _browser_oeffnen(url):
    try:
        webbrowser.open(url)
    except Exception:  # noqa: BLE001
        _ausgeben(f"  Browser konnte nicht geöffnet werden – bitte {url} selbst öffnen.")


def _cli(argv=None):
    p = argparse.ArgumentParser(description="Mathe-Lernsystem – grafische Oberfläche")
    p.add_argument("--port", type=int, default=STANDARD_PORT)
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
