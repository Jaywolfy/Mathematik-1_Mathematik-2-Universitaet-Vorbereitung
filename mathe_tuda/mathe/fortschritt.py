# -*- coding: utf-8 -*-
"""Fortschritt: Laden/Speichern, XP, Level, Serie, Abzeichen, Leitner-Kästen, Meisterschaft.

Alle Funktionen verändern das daten-Dict im Speicher. Gespeichert wird erst mit
speichern(daten). Für Tests IMMER die Umgebungsvariable MATHE_QUIZ_DATEN auf
einen eigenen Ordner setzen, sonst landet der Test im echten Fortschritt.
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
AUSWEICH_DATEINAME = "mathe_quiz_fortschritt.json"
UMGEBUNGSVARIABLE = "MATHE_QUIZ_DATEN"
VERSION = 1

XP_ERSTER_VERSUCH = 10
XP_ZWEITER_VERSUCH = 5
XP_WIEDERHOLUNG = 2
XP_GENERATOR = 3            # jede weitere richtig gelöste Generator-Instanz
XP_PAPIER_PUNKT = 5
XP_KAPITEL = 50
XP_DIAGNOSE = 30

LEVEL_STUFEN = [0, 100, 250, 500, 900, 1400, 2000, 2800, 3800, 5000]
LEVEL_NAMEN = ["Zahlenneugier", "Bruchsicher", "Termgewandt", "Gleichungsklar", "Funktionsblick",
               "Beweislust", "Matrixkraft", "Grenzwertgespür", "Integralgefühl", "Mathe-Profi"]

LEITNER_TAGE = [0, 1, 2, 4, 8]

NOTEN = ((0.95, "1,0"), (0.9, "1,3"), (0.85, "1,7"), (0.8, "2,0"), (0.75, "2,3"),
         (0.7, "2,7"), (0.65, "3,0"), (0.6, "3,3"), (0.55, "3,7"), (0.5, "4,0"))

MEISTER_STUFEN = ((0.85, "gemeistert"), (0.6, "sicher"), (0.01, "angefangen"), (0.0, "neu"))

ABZEICHEN = [
    {"id": "erste_schritte", "titel": "Erste Schritte", "icon": "🐣", "beschreibung": "Die erste Aufgabe richtig gelöst."},
    {"id": "diagnose", "titel": "Standort bestimmt", "icon": "🧭", "beschreibung": "Den Diagnosetest gemacht."},
    {"id": "erstes_kapitel", "titel": "Kapitel geschafft", "icon": "📘", "beschreibung": "Das erste Kapitel abgeschlossen."},
    {"id": "perfekt", "titel": "Volle Punktzahl", "icon": "🎯", "beschreibung": "Ein Kapitel mit allen Punkten abgeschlossen."},
    {"id": "fundament_komplett", "titel": "Festes Fundament", "icon": "🧱", "beschreibung": "Alle Fundament-Kapitel abgeschlossen."},
    {"id": "vorkurs_komplett", "titel": "Vorkurs geschafft", "icon": "🎒", "beschreibung": "Alle Vorkurs-Kapitel abgeschlossen."},
    {"id": "vorlesung_komplett", "titel": "Alle Vorlesungen nachgelernt", "icon": "🎓", "beschreibung": "Alle Vorlesungs-Lektionen abgeschlossen."},
    {"id": "mathe1_komplett", "titel": "Mathe 1 geschafft", "icon": "1️⃣", "beschreibung": "Alle Kapitel von Mathe 1 abgeschlossen."},
    {"id": "mathe2_komplett", "titel": "Mathe 2 geschafft", "icon": "2️⃣", "beschreibung": "Alle Kapitel von Mathe 2 abgeschlossen."},
    {"id": "alles_komplett", "titel": "Alles durch", "icon": "👑", "beschreibung": "Alle Kapitel abgeschlossen."},
    {"id": "meister_1", "titel": "Erste Meisterschaft", "icon": "🥇", "beschreibung": "Ein Kapitel gemeistert."},
    {"id": "meister_10", "titel": "Zehnfach gemeistert", "icon": "🏅", "beschreibung": "Zehn Kapitel gemeistert."},
    {"id": "generator_25", "titel": "Übungsmaschine", "icon": "⚙️", "beschreibung": "25 Generator-Aufgaben gelöst."},
    {"id": "generator_100", "titel": "Rechenmarathon", "icon": "🏃", "beschreibung": "100 Generator-Aufgaben gelöst."},
    {"id": "erster_beweis", "titel": "Auf Papier", "icon": "✍️", "beschreibung": "Die erste Papier-Aufgabe selbst bewertet."},
    {"id": "serie_3", "titel": "Am Ball", "icon": "🔥", "beschreibung": "An 3 Tagen hintereinander geübt."},
    {"id": "serie_7", "titel": "7-Tage-Serie", "icon": "🌋", "beschreibung": "An 7 Tagen hintereinander geübt."},
    {"id": "serie_30", "titel": "Monatsserie", "icon": "🗓️", "beschreibung": "An 30 Tagen hintereinander geübt."},
    {"id": "klausur_bestanden", "titel": "Bestanden!", "icon": "✅", "beschreibung": "Eine Probeklausur mit 4,0 oder besser."},
    {"id": "klausur_1x", "titel": "Einser-Kandidatur", "icon": "🎓", "beschreibung": "Eine Probeklausur mit einer 1,x."},
    {"id": "fehlerkiste_leer", "titel": "Aufgeräumt", "icon": "🧹", "beschreibung": "Die Fehlerkiste komplett geleert."},
    {"id": "fragen_100", "titel": "Hundert!", "icon": "💯", "beschreibung": "100 verschiedene Aufgaben richtig gelöst."},
    {"id": "fragen_500", "titel": "Fünfhundert!", "icon": "🚀", "beschreibung": "500 verschiedene Aufgaben richtig gelöst."},
    {"id": "level_5", "titel": "Halbzeit", "icon": "🌟", "beschreibung": "Level 5 erreicht."},
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
    eigener = os.environ.get(UMGEBUNGSVARIABLE)
    if eigener:
        return Path(eigener)
    return Path.home() / ".mathe_quiz"


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
    ordner = daten_ordner()
    if _beschreibbar(ordner):
        return ordner / DATEINAME
    return PROGRAMMORDNER / AUSWEICH_DATEINAME


def ordner_beschreibbar():
    return _beschreibbar(daten_ordner())


# ──────────────────────────────────────────────────────────────────────────
#  Datenformat
# ──────────────────────────────────────────────────────────────────────────

def leere_daten():
    return {"version": VERSION, "kapitel": {}, "fragen": {}, "fehlerkiste": [], "klausuren": [],
            "entwuerfe": {}, "xp": 0, "serie": {"tage": 0, "zuletzt": None}, "abzeichen": [],
            "diagnose": None, "papier": {}, "generatoren": {},
            "einstellungen": {"theme": "auto", "schrift": "m", "animationen": True, "pause_hinweis": True,
                              "pause_minuten": 25, "begruessung_gesehen": False},
            "meta": {}}


def _normalisieren(d):
    leer = leere_daten()
    if not isinstance(d, dict):
        return leer
    for schluessel, standard in leer.items():
        if schluessel == "diagnose":
            if not isinstance(d.get("diagnose"), (dict, type(None))):
                d["diagnose"] = None
            continue
        if not isinstance(d.get(schluessel), type(standard)):
            d[schluessel] = standard
    for k, v in leer["einstellungen"].items():
        d["einstellungen"].setdefault(k, v)
    d["version"] = VERSION
    d["serie"].setdefault("tage", 0)
    d["serie"].setdefault("zuletzt", None)
    return d


def note_berechnen(punkte, max_punkte):
    quote = punkte / max_punkte if max_punkte else 0
    for grenze, note in NOTEN:
        if quote >= grenze - 1e-9:
            return note
    return "5,0"


def _note_als_zahl(note):
    try:
        return float(str(note).replace(",", "."))
    except ValueError:
        return 5.0


def _freier_name(pfad):
    if not pfad.exists():
        return pfad
    n = 2
    while True:
        kandidat = pfad.with_name(f"{pfad.stem}-{n}{pfad.suffix}")
        if not kandidat.exists():
            return kandidat
        n += 1


def laden(pfad=None):
    with _LOCK:
        pfad = Path(pfad) if pfad else fortschritt_datei()
        if not pfad.exists():
            return leere_daten()
        try:
            d = json.loads(pfad.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            try:
                shutil.copy2(pfad, _freier_name(pfad.with_name(pfad.stem + ".defekt.json")))
            except OSError:
                pass
            return leere_daten()
        return _normalisieren(d)


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
            except PermissionError:
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


def antwort_verbuchen(daten, frage, ok, versuch=1, endgueltig=None, generator=False, teilpunkte=None):
    """Verbucht eine Antwort. Rückgabe: {"xp_neu", "neue_abzeichen"}.

    Ein falscher, nicht endgültiger Versuch zählt nur als 'falsch'. Erst ein endgültig
    falscher kommt in die Fehlerkiste (Kasten 1)."""
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
            if generator:
                g = daten["generatoren"]
                g[fid] = g.get(fid, 0) + 1
            if schon_geloest:
                xp = XP_GENERATOR if generator else XP_WIEDERHOLUNG
            elif eintrag.get("loesung_angesehen"):
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


def papier_verbuchen(daten, frage, haken):
    """Selbstbewertung einer Papier-Aufgabe (Liste von bool). XP: 5 je neu abgehaktem Punkt."""
    with _LOCK:
        fid, _ = _frage_info(frage)
        n, m = sum(bool(h) for h in haken), len(haken)
        alt_best = daten["papier"].get(fid, {}).get("punkte", 0)
        daten["papier"][fid] = {"punkte": max(n, alt_best), "max": m, "datum": _heute_text()}
        info = antwort_verbuchen(daten, fid, n == m, 1, endgueltig=True)
        daten["xp"] -= info["xp_neu"]
        xp = max(0, n - alt_best) * XP_PAPIER_PUNKT
        daten["xp"] += xp
        info["xp_neu"] = xp
        info["neue_abzeichen"] += _abzeichen_pruefen(daten)
        return info


def loesung_angesehen(daten, frage):
    with _LOCK:
        fid, _ = _frage_info(frage)
        eintrag = _fragen_eintrag(daten, fid)
        eintrag["loesung_angesehen"] = True
        eintrag["kasten"] = 1
        eintrag["zuletzt"] = _heute_text()
        if eintrag["richtig"] == 0 and fid not in daten["fehlerkiste"]:
            daten["fehlerkiste"].append(fid)


def kapitel_abschliessen(daten, kapitel, punkte, max_punkte):
    with _LOCK:
        slug = kapitel if isinstance(kapitel, str) else kapitel.slug
        alt = daten["kapitel"].get(slug) or {}
        erstes_mal = not alt.get("abgeschlossen")
        neuer_rekord = bool(alt) and punkte > alt.get("best", -1)
        daten["kapitel"][slug] = {"best": max(int(punkte), int(alt.get("best", 0))), "max": int(max_punkte),
                                  "abgeschlossen": True, "zuletzt": _heute_text()}
        xp = XP_KAPITEL if erstes_mal else 0
        daten["xp"] += xp
        _serie_aktualisieren(daten)
        return {"xp_neu": xp, "neue_abzeichen": _abzeichen_pruefen(daten), "neuer_rekord": neuer_rekord}


def klausur_verbuchen(daten, modul, punkte, max_punkte, dauer=None):
    with _LOCK:
        note = note_berechnen(punkte, max_punkte)
        daten["klausuren"].append({"modul": modul, "datum": _heute_text(), "punkte": punkte,
                                   "max": max_punkte, "note": note, "dauer": dauer})
        _serie_aktualisieren(daten)
        return {"note": note, "neue_abzeichen": _abzeichen_pruefen(daten)}


def diagnose_verbuchen(daten, ergebnis, empfehlung):
    with _LOCK:
        erstes = daten.get("diagnose") is None
        daten["diagnose"] = {"datum": _heute_text(), "ergebnis": ergebnis, "empfehlung": empfehlung}
        xp = XP_DIAGNOSE if erstes else 0
        daten["xp"] += xp
        _serie_aktualisieren(daten)
        return {"xp_neu": xp, "neue_abzeichen": _abzeichen_pruefen(daten)}


def entwurf_speichern(daten, frage_id, text):
    with _LOCK:
        if text and str(text).strip():
            daten["entwuerfe"][frage_id] = str(text)[:50_000]
        else:
            daten["entwuerfe"].pop(frage_id, None)


def einstellungen_setzen(daten, werte):
    with _LOCK:
        daten["einstellungen"].update(werte or {})


def zuruecksetzen(daten):
    with _LOCK:
        einstellungen = daten.get("einstellungen") or {}
        daten.clear()
        daten.update(leere_daten())
        daten["einstellungen"].update(einstellungen)
        return daten


# ──────────────────────────────────────────────────────────────────────────
#  Wiederholen (Leitner)
# ──────────────────────────────────────────────────────────────────────────

def _faellig(e, heute):
    kasten = min(5, max(1, int(e.get("kasten", 1))))
    try:
        zuletzt = datetime.date.fromisoformat(e.get("zuletzt") or "2000-01-01")
    except ValueError:
        zuletzt = datetime.date(2000, 1, 1)
    return (heute - zuletzt).days >= LEITNER_TAGE[kasten - 1], (kasten, zuletzt.isoformat())


def faellige_fragen(daten, n=10, fragen=None):
    if fragen is None:
        from . import engine
        fragen = engine.alle_fragen()
    heute = _heute()
    faellig, rest = [], []
    for fid, e in daten["fragen"].items():
        if fid not in fragen:
            continue
        ist, schluessel = _faellig(e, heute)
        (faellig if ist else rest).append(schluessel + (fid,))
    faellig.sort()
    rest.sort()
    return [s[2] for s in (faellig + rest)[:n]]


def anzahl_faellig(daten, fragen=None):
    if fragen is None:
        from . import engine
        fragen = engine.alle_fragen()
    heute = _heute()
    return sum(1 for fid, e in daten["fragen"].items() if fid in fragen and _faellig(e, heute)[0])


# ──────────────────────────────────────────────────────────────────────────
#  Level, Meisterschaft, Abzeichen, Statistik
# ──────────────────────────────────────────────────────────────────────────

def level(xp):
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


def meisterschaft(daten, kapitel):
    """Abdeckung × (0,6 · Trefferquote + 0,4 · mittlere Leitner-Stufe). Rückgabe (wert, stufe)."""
    ids = [f.id for f in kapitel.fragen()]
    if not ids:
        return 0.0, "neu"
    eintraege = [daten["fragen"].get(fid) for fid in ids]
    beantwortet = [e for e in eintraege if e and (e.get("richtig", 0) + e.get("falsch", 0)) > 0]
    if not beantwortet:
        return 0.0, "neu"
    abdeckung = len(beantwortet) / len(ids)
    r = sum(e.get("richtig", 0) for e in beantwortet)
    f = sum(e.get("falsch", 0) for e in beantwortet)
    quote = r / (r + f) if r + f else 0
    stufe = sum((min(5, int(e.get("kasten", 1))) - 1) / 4 for e in beantwortet) / len(beantwortet)
    wert = round(abdeckung * (0.6 * quote + 0.4 * stufe), 3)
    for grenze, name in MEISTER_STUFEN:
        if wert >= grenze:
            return wert, name
    return wert, "neu"


def _kennzahlen(daten):
    from . import engine
    fragen = engine.alle_fragen()
    geloest = {fid for fid, e in daten["fragen"].items() if e.get("richtig", 0) > 0 and fid in fragen}
    return fragen, geloest


def _abzeichen_pruefen(daten):
    from . import engine
    fragen, geloest = _kennzahlen(daten)
    kap = daten["kapitel"]
    fertig = {slug for slug, e in kap.items() if e.get("abgeschlossen")}
    erreicht = set()
    if geloest:
        erreicht.add("erste_schritte")
    if daten.get("diagnose"):
        erreicht.add("diagnose")
    if fertig:
        erreicht.add("erstes_kapitel")
    if len(geloest) >= 100:
        erreicht.add("fragen_100")
    if len(geloest) >= 500:
        erreicht.add("fragen_500")
    if any(e.get("max", 0) > 0 and e.get("best", 0) >= e.get("max", 0) for e in kap.values()):
        erreicht.add("perfekt")
    for teil in ("fundament", "vorlesung", "vorkurs", "mathe1", "mathe2"):
        slugs = {k.slug for k in engine.kapitel_von_teil(teil)}
        if slugs and slugs <= fertig:
            erreicht.add(f"{teil}_komplett")
    if engine.KAPITEL and {k.slug for k in engine.KAPITEL} <= fertig:
        erreicht.add("alles_komplett")
    gemeistert = sum(1 for k in engine.KAPITEL if meisterschaft(daten, k)[1] == "gemeistert")
    if gemeistert >= 1:
        erreicht.add("meister_1")
    if gemeistert >= 10:
        erreicht.add("meister_10")
    gen = sum(daten["generatoren"].values())
    if gen >= 25:
        erreicht.add("generator_25")
    if gen >= 100:
        erreicht.add("generator_100")
    if daten["papier"]:
        erreicht.add("erster_beweis")
    tage = daten["serie"].get("tage", 0)
    for grenze in (3, 7, 30):
        if tage >= grenze:
            erreicht.add(f"serie_{grenze}")
    for p in daten["klausuren"]:
        note = _note_als_zahl(p.get("note"))
        if note <= 4.0:
            erreicht.add("klausur_bestanden")
        if note < 2.0:
            erreicht.add("klausur_1x")
    if daten["meta"].get("fehlerkiste_geleert"):
        erreicht.add("fehlerkiste_leer")
    if daten["xp"] >= LEVEL_STUFEN[4]:
        erreicht.add("level_5")
    neu = [a for a in ABZEICHEN if a["id"] in erreicht and a["id"] not in daten["abzeichen"]]
    daten["abzeichen"].extend(a["id"] for a in neu)
    return [dict(a) for a in neu]


def kapitel_status(daten, kapitel):
    e = daten["kapitel"].get(kapitel.slug) or {}
    ids = [f.id for f in kapitel.fragen()]
    richtig = sum(1 for fid in ids if daten["fragen"].get(fid, {}).get("richtig", 0) > 0)
    wert, stufe = meisterschaft(daten, kapitel)
    return {"best": e.get("best"), "max": e.get("max"), "abgeschlossen": bool(e.get("abgeschlossen")),
            "zuletzt": e.get("zuletzt"), "fragen_gesamt": len(ids), "fragen_richtig": richtig,
            "fortschritt": round(richtig / len(ids), 3) if ids else 0.0,
            "meisterschaft": wert, "meister_stufe": stufe}


def statistik(daten):
    from . import engine
    with _LOCK:
        fragen, geloest = _kennzahlen(daten)
        teile = []
        for t in engine.TEILE:
            kapitel = engine.kapitel_von_teil(t["id"])
            if not kapitel:
                continue
            ids = [f.id for k in kapitel for f in k.fragen()]
            richtig = sum(1 for fid in ids if fid in geloest)
            fertig = sum(1 for k in kapitel if (daten["kapitel"].get(k.slug) or {}).get("abgeschlossen"))
            meister = [meisterschaft(daten, k)[0] for k in kapitel]
            teile.append({"id": t["id"], "titel": t["titel"], "kapitel_gesamt": len(kapitel),
                          "kapitel_abgeschlossen": fertig, "fragen_gesamt": len(ids), "fragen_richtig": richtig,
                          "fortschritt": round(richtig / len(ids), 3) if ids else 0.0,
                          "meisterschaft": round(sum(meister) / len(meister), 3) if meister else 0.0})
        noten = [p for p in daten["klausuren"] if p.get("note")]
        beste = min(noten, key=lambda p: _note_als_zahl(p["note"]))["note"] if noten else None
        return {
            "xp": daten["xp"], "level": level(daten["xp"]), "serie": dict(daten["serie"]),
            "abzeichen": list(daten["abzeichen"]),
            "abzeichen_alle": [dict(a, erreicht=a["id"] in daten["abzeichen"]) for a in ABZEICHEN],
            "teile": teile, "kapitel_gesamt": len(engine.KAPITEL),
            "kapitel_abgeschlossen": sum(1 for k in engine.KAPITEL
                                         if (daten["kapitel"].get(k.slug) or {}).get("abgeschlossen")),
            "fragen_gesamt": len(fragen), "fragen_richtig": len(geloest),
            "generator_geloest": sum(daten["generatoren"].values()),
            "fehlerkiste": len([fid for fid in daten["fehlerkiste"] if fid in fragen]),
            "faellig": anzahl_faellig(daten, fragen), "klausuren": len(daten["klausuren"]),
            "beste_note": beste, "diagnose": daten.get("diagnose"),
        }


def abzeichen_nach_id(aid):
    return _ABZEICHEN_NACH_ID.get(aid)
