# -*- coding: utf-8 -*-
"""Fortschritt: Laden/Speichern/Migration, XP, Level, Serie, Abzeichen, Leitner-Kästen.

Alle Funktionen verändern das daten-Dict im Speicher. Gespeichert wird erst mit
speichern(daten). Für Tests IMMER die Umgebungsvariable VORKURS_QUIZ_DATEN auf
einen eigenen Ordner setzen (dann wird auch die v1-Datei nur dort gesucht).
"""

import datetime
import json
import os
import shutil
import threading
import time
from pathlib import Path

PROGRAMMORDNER = Path(__file__).resolve().parent.parent
DATEINAME = "fortschritt.json"
V1_DATEINAME = "vorkurs_quiz_fortschritt.json"
V1_SICHERUNG = "vorkurs_quiz_fortschritt.v1.json"
UMGEBUNGSVARIABLE = "VORKURS_QUIZ_DATEN"

# slugs der 24 Kapitel aus v1 – in der alten Reihenfolge ("1" .. "24")
V1_KAPITEL_SLUGS = [
    "computer", "datentypen", "operatoren", "variablen", "strings", "typumwandlung",
    "ein_ausgabe", "fehler", "logik", "verzweigungen", "while_schleifen", "listen",
    "slicing", "tupel", "dictionaries", "for_schleifen", "module_import", "dateien",
    "funktionen", "rekursion", "java", "guter_code", "rsa", "hsv_rgb",
]

XP_ERSTER_VERSUCH = 10
XP_ZWEITER_VERSUCH = 5
XP_CODE = 30
XP_KAPITEL = 50
XP_WIEDERHOLUNG = 2          # bereits früher gelöste Frage erneut richtig

LEVEL_STUFEN = [0, 100, 250, 500, 900, 1400, 2000, 2800, 3800, 5000]
LEVEL_NAMEN = ["Neugierig", "Entdecken", "Ausprobieren", "Dranbleiben", "Verstehen",
               "Anwenden", "Knobeln", "Durchblicken", "Meistern", "Python-Profi"]

LEITNER_TAGE = [0, 1, 2, 4, 8]  # Kasten 1..5: nach so vielen Tagen wieder fällig

NOTEN = ((0.95, "1,0"), (0.9, "1,3"), (0.85, "1,7"), (0.8, "2,0"), (0.75, "2,3"),
         (0.7, "2,7"), (0.65, "3,0"), (0.6, "3,3"), (0.55, "3,7"), (0.5, "4,0"))

ABZEICHEN = [
    {"id": "erste_schritte", "titel": "Erste Schritte", "icon": "🐣",
     "beschreibung": "Die erste Frage richtig beantwortet."},
    {"id": "erstes_kapitel", "titel": "Kapitel geschafft", "icon": "📘",
     "beschreibung": "Das erste Kapitel abgeschlossen."},
    {"id": "erster_code", "titel": "Hallo, Code!", "icon": "💻",
     "beschreibung": "Die erste Programmieraufgabe gelöst."},
    {"id": "perfekt", "titel": "Volle Punktzahl", "icon": "🎯",
     "beschreibung": "Ein Kapitel mit allen Punkten abgeschlossen."},
    {"id": "tag1_komplett", "titel": "Tag 1 komplett", "icon": "1️⃣",
     "beschreibung": "Alle Kapitel von Tag 1 abgeschlossen."},
    {"id": "tag2_komplett", "titel": "Tag 2 komplett", "icon": "2️⃣",
     "beschreibung": "Alle Kapitel von Tag 2 abgeschlossen."},
    {"id": "tag3_komplett", "titel": "Tag 3 komplett", "icon": "3️⃣",
     "beschreibung": "Alle Kapitel von Tag 3 abgeschlossen."},
    {"id": "tag4_komplett", "titel": "Tag 4 komplett", "icon": "4️⃣",
     "beschreibung": "Alle Kapitel von Tag 4 abgeschlossen."},
    {"id": "bonus_komplett", "titel": "Extrameile", "icon": "⭐",
     "beschreibung": "Alle Bonus-Kapitel abgeschlossen."},
    {"id": "alles_komplett", "titel": "Vorkurs-Champion", "icon": "👑",
     "beschreibung": "Alle Kapitel abgeschlossen."},
    {"id": "serie_3", "titel": "Am Ball", "icon": "🔥",
     "beschreibung": "An 3 Tagen hintereinander geübt."},
    {"id": "serie_7", "titel": "7-Tage-Serie", "icon": "🌋",
     "beschreibung": "An 7 Tagen hintereinander geübt."},
    {"id": "pruefung_bestanden", "titel": "Bestanden!", "icon": "✅",
     "beschreibung": "Eine Probeprüfung mit 4,0 oder besser bestanden."},
    {"id": "pruefung_1x", "titel": "Einser-Kandidat", "icon": "🎓",
     "beschreibung": "Eine Probeprüfung mit einer 1,x abgeschlossen."},
    {"id": "fehlerkiste_leer", "titel": "Aufgeräumt", "icon": "🧹",
     "beschreibung": "Die Fehlerkiste komplett geleert."},
    {"id": "fragen_100", "titel": "Hundert!", "icon": "💯",
     "beschreibung": "100 verschiedene Fragen richtig beantwortet."},
    {"id": "code_10", "titel": "Tüftel-Anfang", "icon": "🧩",
     "beschreibung": "10 Programmieraufgaben gelöst."},
    {"id": "code_25", "titel": "Code-Handwerk", "icon": "🛠️",
     "beschreibung": "25 Programmieraufgaben gelöst."},
    {"id": "code_50", "titel": "Code-Rakete", "icon": "🚀",
     "beschreibung": "50 Programmieraufgaben gelöst."},
    {"id": "code_100", "titel": "Code-Legende", "icon": "🏆",
     "beschreibung": "100 Programmieraufgaben gelöst."},
    {"id": "level_5", "titel": "Halbzeit", "icon": "🌟",
     "beschreibung": "Level 5 erreicht."},
]
_ABZEICHEN_NACH_ID = {a["id"]: a for a in ABZEICHEN}

_LOCK = threading.RLock()


def _heute():
    return datetime.date.today()


def _heute_text():
    return _heute().isoformat()


# ──────────────────────────────────────────────────────────────────────────
#  Speicherort
# ──────────────────────────────────────────────────────────────────────────

def daten_ordner():
    """Ordner für den Fortschritt (VORKURS_QUIZ_DATEN überschreibt)."""
    eigener = os.environ.get(UMGEBUNGSVARIABLE)
    if eigener:
        return Path(eigener)
    return Path.home() / ".vorkurs_quiz"


def _beschreibbar(ordner):
    try:
        ordner.mkdir(parents=True, exist_ok=True)
        probe = ordner / f".schreibtest_{os.getpid()}_{threading.get_ident()}"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return True
    except OSError:
        return False


def fortschritt_datei():
    """Pfad der Fortschrittsdatei (Ausweichpfad im Programmordner, falls nötig)."""
    ordner = daten_ordner()
    if _beschreibbar(ordner):
        return ordner / DATEINAME
    return PROGRAMMORDNER / V1_DATEINAME


def v1_datei():
    """Wo die alte v1-Datei gesucht wird (bei VORKURS_QUIZ_DATEN: dort)."""
    eigener = os.environ.get(UMGEBUNGSVARIABLE)
    if eigener:
        return Path(eigener) / V1_DATEINAME
    return PROGRAMMORDNER / V1_DATEINAME


def ordner_beschreibbar():
    return _beschreibbar(daten_ordner())


# ──────────────────────────────────────────────────────────────────────────
#  Datenformat
# ──────────────────────────────────────────────────────────────────────────

def leere_daten():
    return {"version": 2, "kapitel": {}, "fragen": {}, "fehlerkiste": [], "pruefungen": [],
            "entwuerfe": {}, "xp": 0, "serie": {"tage": 0, "zuletzt": None}, "abzeichen": [],
            "einstellungen": {"theme": "auto"}, "meta": {}}


def _normalisieren(d):
    leer = leere_daten()
    if not isinstance(d, dict):
        return leer
    for schluessel, standard in leer.items():
        if not isinstance(d.get(schluessel), type(standard)):
            d[schluessel] = standard
    d["version"] = 2
    d["serie"].setdefault("tage", 0)
    d["serie"].setdefault("zuletzt", None)
    return d


def note_berechnen(punkte, max_punkte):
    quote = punkte / max_punkte if max_punkte else 0
    for grenze, note in NOTEN:
        if quote >= grenze:
            return note
    return "5,0"


def _note_als_zahl(note):
    try:
        return float(str(note).replace(",", "."))
    except ValueError:
        return 5.0


def migrieren_v1(alt):
    """Wandelt v1-Daten ({"kapitel": {"1": {...}}, "fehlerkiste", "pruefungen"}) in v2 um.
       Alte Fehlerkiste-IDs ("K02-012") lassen sich nicht zuordnen und werden verworfen."""
    neu = leere_daten()
    for nummer, eintrag in (alt.get("kapitel") or {}).items():
        try:
            index = int(nummer) - 1
            best, maximum = int(eintrag["best"]), int(eintrag["max"])
        except (ValueError, KeyError, TypeError):
            continue
        if 0 <= index < len(V1_KAPITEL_SLUGS):
            neu["kapitel"][V1_KAPITEL_SLUGS[index]] = {
                "best": best, "max": maximum, "abgeschlossen": True, "zuletzt": None}
            neu["xp"] += XP_KAPITEL + XP_ERSTER_VERSUCH * best
    for p in alt.get("pruefungen") or []:
        try:
            punkte, maximum = int(p["punkte"]), int(p["max"])
        except (ValueError, KeyError, TypeError):
            continue
        neu["pruefungen"].append({"datum": None, "punkte": punkte, "max": maximum,
                                  "note": note_berechnen(punkte, maximum)})
    neu["meta"]["migriert_von"] = 1
    neu["meta"]["migriert_am"] = _heute_text()
    _abzeichen_pruefen(neu)
    return neu


# ──────────────────────────────────────────────────────────────────────────
#  Laden & Speichern
# ──────────────────────────────────────────────────────────────────────────

def _freier_name(pfad):
    if not pfad.exists():
        return pfad
    n = 2
    while True:
        kandidat = pfad.with_name(f"{pfad.stem}-{n}{pfad.suffix}")
        if not kandidat.exists():
            return kandidat
        n += 1


def laden(pfad=None, v1_pfad=None):
    """Lädt den Fortschritt. Migriert beim ersten Start eine v1-Datei."""
    with _LOCK:
        pfad = Path(pfad) if pfad else fortschritt_datei()
        v1 = Path(v1_pfad) if v1_pfad else v1_datei()
        if pfad.exists():
            try:
                d = json.loads(pfad.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                try:
                    shutil.copy2(pfad, _freier_name(pfad.with_name(pfad.stem + ".defekt.json")))
                except OSError:
                    pass
                return leere_daten()
            if isinstance(d, dict) and d.get("version") != 2 and "kapitel" in d:
                # v1-Datei am selben Ort (Ausweichpfad im Programmordner)
                try:
                    shutil.copy2(pfad, _freier_name(pfad.with_name(V1_SICHERUNG)))
                except OSError:
                    pass
                d = migrieren_v1(d)
                speichern(d, pfad)
                return d
            return _normalisieren(d)
        if v1.exists() and v1.resolve() != pfad.resolve():
            try:
                alt = json.loads(v1.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                alt = None
            if isinstance(alt, dict):
                try:
                    shutil.copy2(v1, _freier_name(v1.with_name(V1_SICHERUNG)))
                except OSError:
                    return _normalisieren(migrieren_v1(alt))  # ohne Sicherung nichts löschen
                d = migrieren_v1(alt)
                if speichern(d, pfad):
                    try:
                        v1.unlink()
                    except OSError:
                        pass
                return d
        return leere_daten()


def speichern(daten, pfad=None):
    """Speichert atomar (erst .tmp, dann ersetzen). Rückgabe: True bei Erfolg."""
    with _LOCK:
        pfad = Path(pfad) if pfad else fortschritt_datei()
        tmp = pfad.with_name(pfad.name + ".tmp")
        try:
            pfad.parent.mkdir(parents=True, exist_ok=True)
            tmp.write_text(json.dumps(daten, ensure_ascii=False, indent=1), encoding="utf-8")
        except OSError:
            return False
        for versuch in range(10):
            try:
                os.replace(tmp, pfad)
                return True
            except PermissionError:      # Windows: Datei kurz von Virenscanner o. Ä. gesperrt
                time.sleep(0.05 * (versuch + 1))
            except OSError:
                break
        try:
            tmp.unlink()
        except OSError:
            pass
        return False


# ──────────────────────────────────────────────────────────────────────────
#  Verbuchen
# ──────────────────────────────────────────────────────────────────────────

def _frage_info(frage):
    """(id, typ) – frage darf ein Frage-Objekt oder eine ID sein."""
    if isinstance(frage, str):
        from . import engine
        f = engine.frage_nach_id(frage)
        return frage, (f.typ if f else None)
    return frage.id, frage.typ


def _fragen_eintrag(daten, fid):
    return daten["fragen"].setdefault(fid, {"richtig": 0, "falsch": 0, "zuletzt": None, "kasten": 1})


def _serie_aktualisieren(daten):
    heute = _heute()
    serie = daten["serie"]
    zuletzt = serie.get("zuletzt")
    if zuletzt == heute.isoformat():
        return
    gestern = (heute - datetime.timedelta(days=1)).isoformat()
    serie["tage"] = serie.get("tage", 0) + 1 if zuletzt == gestern else 1
    serie["zuletzt"] = heute.isoformat()


def antwort_verbuchen(daten, frage, ok, versuch=1, endgueltig=None):
    """Verbucht eine Antwort. Rückgabe: {"xp_neu", "neue_abzeichen"}.

    endgueltig: Ist das der letzte Versuch? Standard: versuch >= 2 oder Typ mc/wf.
    Ein falscher, nicht endgültiger Versuch zählt nur als 'falsch' – erst ein
    endgültig falscher kommt in die Fehlerkiste (Kasten 1).
    """
    with _LOCK:
        fid, typ = _frage_info(frage)
        if endgueltig is None:
            endgueltig = versuch >= 2 or typ in ("mc", "wf")
        eintrag = _fragen_eintrag(daten, fid)
        schon_geloest = eintrag["richtig"] > 0
        xp = 0
        if ok:
            eintrag["richtig"] += 1
            eintrag["kasten"] = min(5, int(eintrag.get("kasten", 1)) + 1)
            if typ == "code":
                if schon_geloest:
                    xp = XP_WIEDERHOLUNG
                elif eintrag.get("loesung_angesehen"):
                    xp = XP_ZWEITER_VERSUCH
                else:
                    xp = XP_CODE
            elif schon_geloest:
                xp = XP_WIEDERHOLUNG
            else:
                xp = XP_ERSTER_VERSUCH if versuch <= 1 else XP_ZWEITER_VERSUCH
            if fid in daten["fehlerkiste"]:
                daten["fehlerkiste"].remove(fid)
                if not daten["fehlerkiste"]:
                    daten["meta"]["fehlerkiste_geleert"] = True
        else:
            eintrag["falsch"] += 1
            if endgueltig:
                eintrag["kasten"] = 1
                if fid not in daten["fehlerkiste"]:
                    daten["fehlerkiste"].append(fid)
        eintrag["zuletzt"] = _heute_text()
        daten["xp"] += xp
        _serie_aktualisieren(daten)
        return {"xp_neu": xp, "neue_abzeichen": _abzeichen_pruefen(daten)}


def loesung_angesehen(daten, frage):
    """Musterlösung angesehen: Frage kommt in die Fehlerkiste (Kasten 1)."""
    with _LOCK:
        fid, _ = _frage_info(frage)
        eintrag = _fragen_eintrag(daten, fid)
        eintrag["loesung_angesehen"] = True
        eintrag["kasten"] = 1
        eintrag["zuletzt"] = _heute_text()
        if eintrag["richtig"] == 0 and fid not in daten["fehlerkiste"]:
            daten["fehlerkiste"].append(fid)


def kapitel_abschliessen(daten, kapitel, punkte, max_punkte):
    """Kapitel fertig gespielt. Rückgabe: {"xp_neu", "neue_abzeichen", "neuer_rekord"}."""
    with _LOCK:
        slug = kapitel if isinstance(kapitel, str) else kapitel.slug
        alt = daten["kapitel"].get(slug) or {}
        erstes_mal = not alt.get("abgeschlossen")
        neuer_rekord = bool(alt) and punkte > alt.get("best", -1)
        daten["kapitel"][slug] = {"best": max(int(punkte), int(alt.get("best", 0))),
                                  "max": int(max_punkte), "abgeschlossen": True,
                                  "zuletzt": _heute_text()}
        xp = XP_KAPITEL if erstes_mal else 0
        daten["xp"] += xp
        _serie_aktualisieren(daten)
        return {"xp_neu": xp, "neue_abzeichen": _abzeichen_pruefen(daten),
                "neuer_rekord": neuer_rekord}


def pruefung_verbuchen(daten, punkte, max_punkte):
    """Probeprüfung speichern. Rückgabe: {"note", "neue_abzeichen"}."""
    with _LOCK:
        note = note_berechnen(punkte, max_punkte)
        daten["pruefungen"].append({"datum": _heute_text(), "punkte": int(punkte),
                                    "max": int(max_punkte), "note": note})
        _serie_aktualisieren(daten)
        return {"note": note, "neue_abzeichen": _abzeichen_pruefen(daten)}


def entwurf_speichern(daten, frage_id, code):
    with _LOCK:
        if code and code.strip():
            daten["entwuerfe"][frage_id] = str(code)[:100_000]
        else:
            daten["entwuerfe"].pop(frage_id, None)


def einstellungen_setzen(daten, werte):
    with _LOCK:
        daten["einstellungen"].update(werte or {})


def zuruecksetzen(daten):
    """Setzt alles zurück (Einstellungen bleiben). Verändert daten direkt."""
    with _LOCK:
        einstellungen = daten.get("einstellungen") or {}
        daten.clear()
        daten.update(leere_daten())
        daten["einstellungen"].update(einstellungen)
        return daten


# ──────────────────────────────────────────────────────────────────────────
#  Wiederholen (Leitner)
# ──────────────────────────────────────────────────────────────────────────

def faellige_fragen(daten=None, n=10, fragen=None):
    """IDs von Fragen zum Wiederholen – bevorzugt niedrige Kästen und lange nicht gesehene.

    Auch als faellige_fragen(n) aufrufbar (lädt dann den gespeicherten Fortschritt).
    """
    if isinstance(daten, int):
        daten, n = None, daten
    if daten is None:
        daten = laden()
    if fragen is None:
        from . import engine
        fragen = engine.alle_fragen()
    heute = _heute()
    faellig, rest = [], []
    for fid, e in daten["fragen"].items():
        if fid not in fragen:
            continue
        kasten = min(5, max(1, int(e.get("kasten", 1))))
        try:
            zuletzt = datetime.date.fromisoformat(e.get("zuletzt") or "2000-01-01")
        except ValueError:
            zuletzt = datetime.date(2000, 1, 1)
        schluessel = (kasten, zuletzt.isoformat(), fid)
        if (heute - zuletzt).days >= LEITNER_TAGE[kasten - 1]:
            faellig.append(schluessel)
        else:
            rest.append(schluessel)
    faellig.sort()
    rest.sort()
    return [s[2] for s in (faellig + rest)[:n]]


def anzahl_faellig(daten, fragen=None):
    heute = _heute()
    if fragen is None:
        from . import engine
        fragen = engine.alle_fragen()
    anzahl = 0
    for fid, e in daten["fragen"].items():
        if fid not in fragen:
            continue
        kasten = min(5, max(1, int(e.get("kasten", 1))))
        try:
            zuletzt = datetime.date.fromisoformat(e.get("zuletzt") or "2000-01-01")
        except ValueError:
            zuletzt = datetime.date(2000, 1, 1)
        if (heute - zuletzt).days >= LEITNER_TAGE[kasten - 1]:
            anzahl += 1
    return anzahl


# ──────────────────────────────────────────────────────────────────────────
#  Level, Abzeichen, Statistik
# ──────────────────────────────────────────────────────────────────────────

def level(xp):
    """{"nummer", "name", "titel", "xp", "xp_start", "xp_naechstes", "fortschritt"}"""
    nummer = 1
    for i, grenze in enumerate(LEVEL_STUFEN):
        if xp >= grenze:
            nummer = i + 1
    start = LEVEL_STUFEN[nummer - 1]
    naechstes = LEVEL_STUFEN[nummer] if nummer < len(LEVEL_STUFEN) else None
    fortschritt = 1.0 if naechstes is None else (xp - start) / (naechstes - start)
    name = LEVEL_NAMEN[nummer - 1]
    return {"nummer": nummer, "name": name, "titel": f"Level {nummer} · {name}", "xp": xp,
            "xp_start": start, "xp_naechstes": naechstes, "fortschritt": round(fortschritt, 3)}


def _kennzahlen(daten):
    from . import engine
    fragen = engine.alle_fragen()
    geloest = {fid for fid, e in daten["fragen"].items() if e.get("richtig", 0) > 0 and fid in fragen}
    code_ids = {fid for fid, f in fragen.items() if f.typ == "code"}
    return fragen, geloest, code_ids


def _abzeichen_pruefen(daten):
    """Vergibt neu erreichte Abzeichen. Rückgabe: Liste der neuen Abzeichen-Dicts."""
    from . import engine
    fragen, geloest, code_ids = _kennzahlen(daten)
    kap = daten["kapitel"]
    fertig = {slug for slug, e in kap.items() if e.get("abgeschlossen")}
    erreicht = set()
    if geloest or any(e.get("best", 0) > 0 for e in kap.values()):
        erreicht.add("erste_schritte")
    if fertig:
        erreicht.add("erstes_kapitel")
    anzahl_code = len(geloest & code_ids)
    if anzahl_code >= 1:
        erreicht.add("erster_code")
    for grenze in (10, 25, 50, 100):
        if anzahl_code >= grenze:
            erreicht.add(f"code_{grenze}")
    if len(geloest) >= 100:
        erreicht.add("fragen_100")
    if any(e.get("max", 0) > 0 and e.get("best", 0) >= e.get("max", 0) for e in kap.values()):
        erreicht.add("perfekt")
    for teil in ("tag1", "tag2", "tag3", "tag4", "bonus"):
        slugs = {k.slug for k in engine.kapitel_von_teil(teil)}
        if slugs and slugs <= fertig:
            erreicht.add(f"{teil}_komplett")
    if engine.KAPITEL and {k.slug for k in engine.KAPITEL} <= fertig:
        erreicht.add("alles_komplett")
    tage = daten["serie"].get("tage", 0)
    if tage >= 3:
        erreicht.add("serie_3")
    if tage >= 7:
        erreicht.add("serie_7")
    for p in daten["pruefungen"]:
        note = _note_als_zahl(p.get("note"))
        if note <= 4.0:
            erreicht.add("pruefung_bestanden")
        if note < 2.0:
            erreicht.add("pruefung_1x")
    if daten["meta"].get("fehlerkiste_geleert"):
        erreicht.add("fehlerkiste_leer")
    if daten["xp"] >= LEVEL_STUFEN[4]:
        erreicht.add("level_5")
    neu = [a for a in ABZEICHEN if a["id"] in erreicht and a["id"] not in daten["abzeichen"]]
    daten["abzeichen"].extend(a["id"] for a in neu)
    return [dict(a) for a in neu]


def kapitel_status(daten, kapitel):
    """Fortschritt eines Kapitels für Übersichten."""
    e = daten["kapitel"].get(kapitel.slug) or {}
    ids = [f.id for f in kapitel.fragen()]
    richtig = sum(1 for fid in ids if daten["fragen"].get(fid, {}).get("richtig", 0) > 0)
    return {"best": e.get("best"), "max": e.get("max"), "abgeschlossen": bool(e.get("abgeschlossen")),
            "zuletzt": e.get("zuletzt"), "fragen_gesamt": len(ids), "fragen_richtig": richtig,
            "fortschritt": round(richtig / len(ids), 3) if ids else 0.0}


def statistik(daten):
    """Zahlen für das Dashboard."""
    from . import engine
    with _LOCK:
        fragen, geloest, code_ids = _kennzahlen(daten)
        teile = []
        for t in engine.TEILE:
            kapitel = engine.kapitel_von_teil(t["id"])
            if not kapitel:
                continue
            ids = [f.id for k in kapitel for f in k.fragen()]
            richtig = sum(1 for fid in ids if fid in geloest)
            fertig = sum(1 for k in kapitel if (daten["kapitel"].get(k.slug) or {}).get("abgeschlossen"))
            teile.append({"id": t["id"], "titel": t["titel"], "kapitel_gesamt": len(kapitel),
                          "kapitel_abgeschlossen": fertig, "fragen_gesamt": len(ids),
                          "fragen_richtig": richtig,
                          "fortschritt": round(richtig / len(ids), 3) if ids else 0.0})
        noten = [p for p in daten["pruefungen"] if p.get("note")]
        beste = min(noten, key=lambda p: _note_als_zahl(p["note"]))["note"] if noten else None
        return {
            "xp": daten["xp"],
            "level": level(daten["xp"]),
            "serie": dict(daten["serie"]),
            "abzeichen": list(daten["abzeichen"]),
            "abzeichen_alle": [dict(a, erreicht=a["id"] in daten["abzeichen"]) for a in ABZEICHEN],
            "teile": teile,
            "kapitel_gesamt": len(engine.KAPITEL),
            "kapitel_abgeschlossen": sum(1 for k in engine.KAPITEL
                                         if (daten["kapitel"].get(k.slug) or {}).get("abgeschlossen")),
            "fragen_gesamt": len(fragen),
            "fragen_richtig": len(geloest),
            "code_gesamt": len(code_ids),
            "code_geloest": len(geloest & code_ids),
            "fehlerkiste": len([fid for fid in daten["fehlerkiste"] if fid in fragen]),
            "faellig": anzahl_faellig(daten, fragen),
            "pruefungen": len(daten["pruefungen"]),
            "beste_note": beste,
        }


def abzeichen_nach_id(aid):
    return _ABZEICHEN_NACH_ID.get(aid)
