# -*- coding: utf-8 -*-
"""Selbsttest: prüft ALLE Inhalte automatisch (python vorkurs_quiz.py --selbsttest).

Fehler lassen den Test scheitern (Exit-Code 1), Warnungen nicht.
"""

import sys
import time
from concurrent.futures import ThreadPoolExecutor

from . import engine, markup, sandbox
from .engine import (Ausdruck, Ausgabe, CodeAufgabe, Erklaerung, Luecke, MC, Puzzle,
                     Textfrage, WahrFalsch, Zusammenfassung)

_FARBE = {"rot": "91", "gruen": "92", "gelb": "93", "fett": "1", "grau": "90"}


class Bericht:
    def __init__(self, farben=True):
        self.farben = farben and sys.stdout.isatty()
        self.fehler = []
        self.warnungen = []

    def f(self, name, text):
        return f"\033[{_FARBE[name]}m{text}\033[0m" if self.farben else text

    def fehler_melden(self, ort, text):
        self.fehler.append(f"{ort}: {text}")
        print("  " + self.f("rot", f"FEHLER  {ort}: {text}"))

    def warnung_melden(self, ort, text):
        self.warnungen.append(f"{ort}: {text}")
        print("  " + self.f("gelb", f"WARNUNG {ort}: {text}"))


def _markup_pruefen(bericht, ort, text):
    """Markup-Probleme melden und :::code-Beispiele zum Ausführen sammeln."""
    for problem in markup.pruefen(text):
        bericht.fehler_melden(ort, problem)
    return markup.code_beispiele(markup.parse(text))


def _code_konfiguration_pruefen(f):
    """Prüft die Parameter einer Programmieraufgabe (Regeln, Alternativen, Anzahl, streng)."""
    probleme = []
    for regel in f.regeln:
        fehler = engine.regel_fehler(regel)
        if fehler:
            probleme.append(f"Ungültige Regel {regel!r}: {fehler}")
    if not isinstance(f.streng, bool):
        probleme.append(f"streng muss True oder False sein, nicht {f.streng!r}")
    if f.rekursiv is not None and not all(n.strip().isidentifier()
                                          for n in str(f.rekursiv).split("|")):
        probleme.append(f"rekursiv {f.rekursiv!r} ist kein gültiger Funktionsname")
    for i, t in enumerate(f.tests, 1):
        ort = f"Test {i}"
        if t.streng not in (None, True, False):
            probleme.append(f"{ort}: streng muss None, True oder False sein")
        for e in t.erwartet:
            if isinstance(e, tuple) and (not e or not all(a.strip() for a in e)):
                probleme.append(f"{ort}: leere Alternative in erwartet {e!r}")
            elif isinstance(e, str) and not e.strip():
                probleme.append(f"{ort}: leerer Text in erwartet")
        for text, n in t.anzahl.items():
            if not text.strip():
                probleme.append(f"{ort}: leerer Text in anzahl")
            if n < 0:
                probleme.append(f"{ort}: anzahl für {text!r} ist negativ")
        if t.aufruf and (t.erwartet or t.exakt is not None or t.anzahl or t.nicht or t.eingaben):
            probleme.append(f"{ort}: Funktionstest (F) mit erwartet/exakt/anzahl/nicht/eingaben – "
                            "diese Angaben werden ignoriert")
        if t.leerzeichen and t.exakt is None and not (t.streng or f.streng):
            probleme.append(f"{ort}: leerzeichen=True wirkt nur mit exakt oder streng")
    return probleme


def _frage_pruefen(f):
    """Prüft eine Frage. Rückgabe: Liste von Fehlertexten (leer = ok)."""
    probleme = []
    try:
        if isinstance(f, MC):
            if len(f.optionen) < 2:
                probleme.append("MC hat weniger als 2 Optionen")
            if len(set(f.optionen)) != len(f.optionen):
                probleme.append("MC hat doppelte Optionen")
            if not f.pruefen(f.optionen[0]).ok or (len(f.optionen) > 1 and f.pruefen(f.optionen[1]).ok):
                probleme.append("MC-Prüfung liefert falsches Ergebnis")
        elif isinstance(f, WahrFalsch):
            if not isinstance(f.wahr, bool):
                probleme.append("wahr muss True oder False sein")
            if not f.pruefen(f.wahr).ok:
                probleme.append("Wahr/Falsch-Prüfung liefert falsches Ergebnis")
        elif isinstance(f, Textfrage):
            if not f.antworten:
                probleme.append("Textfrage ohne akzeptierte Antworten")
            elif not f.pruefen(f.antworten[0]).ok:
                probleme.append("Textfrage akzeptiert ihre eigene Antwort nicht")
        elif isinstance(f, Ausgabe):
            ausgabe, fehler = f.soll()
            if fehler == "Timeout":
                probleme.append("Ausgabe-Code läuft in ein Zeitlimit (Endlosschleife?)")
            else:
                antwort = fehler or ausgabe or "nichts"
                if not f.pruefen(antwort).ok:
                    probleme.append(f"Ausgabe-Frage akzeptiert die echte Ausgabe nicht: {antwort!r}")
        elif isinstance(f, Ausdruck):
            if not f.tests:
                probleme.append("Ausdruck ohne Tests")
            erg = f.pruefen(f.loesung)
            if not erg.ok:
                probleme.append(f"Musterlösung besteht nicht: {erg.meldung}")
        elif isinstance(f, Luecke):
            if f.anzahl_luecken() == 0:
                probleme.append("Lückencode enthält keine ___")
            if f.anzahl_luecken() != len(f.antworten):
                probleme.append(f"{f.anzahl_luecken()} Lücken, aber {len(f.antworten)} Antwortlisten")
            elif not f.pruefen([a[0] for a in f.antworten]).ok:
                probleme.append("Lückencode akzeptiert die eigenen Antworten nicht")
        elif isinstance(f, Puzzle):
            if len(f.zeilen) < 2:
                probleme.append("Puzzle hat weniger als 2 Zeilen")
            for a in f.ablenker:
                if a in f.zeilen:
                    probleme.append(f"Ablenker kommt in der Lösung vor: {a.strip()!r}")
            if not f.pruefen(f._loesungs_ids()).ok:
                probleme.append("Puzzle-Lösung wird nicht als richtig erkannt")
            if f.ablenker and f.pruefen(f._loesungs_ids()[:-1] + list(f._zeilen_ids())[-1:]).ok:
                probleme.append("Puzzle akzeptiert einen Ablenker")
        elif isinstance(f, CodeAufgabe):
            if not f.tests:
                probleme.append("Programmieraufgabe ohne Tests")
            probleme += _code_konfiguration_pruefen(f)
            erg = f.pruefen(f.loesung)
            if not erg.ok:
                gruende = [f"{d['name']}: {d['meldung']}" for d in erg.details if not d["ok"]]
                probleme.append("Musterlösung besteht nicht: " + ("; ".join(gruende) or erg.meldung))
        d = f.to_dict()
        if not d.get("id"):
            probleme.append("Frage ohne ID")
    except Exception as e:  # jede Ausnahme ist ein Fehler im Inhalt
        probleme.append(f"Ausnahme beim Prüfen: {type(e).__name__}: {e}")
    return probleme


def _beispiel_pruefen(block):
    erg = sandbox.ausfuehren(block["code"], block.get("eingaben", []))
    if erg["timeout"]:
        return ["Code-Beispiel läuft in ein Zeitlimit"]
    if block.get("trace"):
        t = sandbox.trace(block["code"], block.get("eingaben", []))
        if t.get("timeout"):
            return ["Trace-Beispiel läuft in ein Zeitlimit"]
    return []


def kapitel_pruefen(kap, bericht, pool):
    """Prüft ein Kapitel (Struktur, Markup, alle Fragen)."""
    ort = f"Kapitel {kap.nummer} ({kap.slug})"
    if kap.teil not in engine.TEIL_IDS:
        bericht.fehler_melden(ort, f"unbekannter teil {kap.teil!r}")
    if not kap.lernziele:
        bericht.warnung_melden(ort, "keine lernziele")
    elif not 2 <= len(kap.lernziele) <= 5:
        bericht.warnung_melden(ort, f"{len(kap.lernziele)} Lernziele (empfohlen: 2–5)")
    if not kap.erklaerungen():
        bericht.warnung_melden(ort, "keine Erklärung")
    programmieren = [f for f in kap.fragen() if f.phase == "programmieren"]
    if len(programmieren) < 2:
        bericht.warnung_melden(ort, f"nur {len(programmieren)} Programmieraufgabe(n) (mind. 2)")
    if kap.zusammenfassung_text is None:
        bericht.warnung_melden(ort, "keine zusammenfassung")

    beispiele = []
    for e in kap.elemente:
        if isinstance(e, Erklaerung):
            beispiele += _markup_pruefen(bericht, f"{ort}, Erklärung '{e.titel}'", e.text)
        elif isinstance(e, Zusammenfassung):
            beispiele += _markup_pruefen(bericht, f"{ort}, Zusammenfassung", e.text)
        else:
            for feld in ("frage", "aussage", "aufgabe", "erklaerung"):
                text = getattr(e, feld, None)
                if isinstance(text, str):
                    beispiele += _markup_pruefen(bericht, f"{e.id} ({feld})", text)

    fragen = kap.fragen()
    ergebnisse = list(pool.map(_frage_pruefen, fragen))
    beispiel_ergebnisse = list(pool.map(_beispiel_pruefen, beispiele))
    for f, probleme in zip(fragen, ergebnisse):
        for p in probleme:
            bericht.fehler_melden(f"{f.id} [{f.typ}]", p)
    for b, probleme in zip(beispiele, beispiel_ergebnisse):
        for p in probleme:
            bericht.fehler_melden(f"{ort}, Beispiel", f"{p}: {b['code'][:40]!r}")
    return len(fragen)


def main(farben=True, kapitel=None):
    """Führt den Selbsttest aus. Rückgabe: Exit-Code (0 = keine Fehler)."""
    start = time.time()
    bericht = Bericht(farben)
    kapitel = list(engine.KAPITEL if kapitel is None else kapitel)
    print(bericht.f("fett", "SELBSTTEST – alle Inhalte werden geprüft …"))

    # IDs eindeutig?
    gesehen = {}
    for kap in engine.KAPITEL:
        for f in kap.fragen():
            if f.id in gesehen:
                bericht.fehler_melden(f.id, "ID kommt doppelt vor")
            gesehen[f.id] = f

    from .inhalte import SPICKZETTEL
    _markup_pruefen(bericht, "Spickzettel", SPICKZETTEL)

    gesamt = 0
    with ThreadPoolExecutor(max_workers=8) as pool:
        for kap in kapitel:
            print(bericht.f("fett", f"\nKapitel {kap.nummer}: {kap.titel}") +
                  bericht.f("grau", f"  [{kap.slug}, {kap.teil}]"))
            vorher = len(bericht.fehler)
            n = kapitel_pruefen(kap, bericht, pool)
            gesamt += n
            if len(bericht.fehler) == vorher:
                print("  " + bericht.f("gruen", f"✔ {n} Fragen/Aufgaben in Ordnung"))

    dauer = time.time() - start
    farbe = "rot" if bericht.fehler else "gruen"
    print()
    print(bericht.f("fett", bericht.f(farbe,
          f"{gesamt} Fragen/Aufgaben in {len(kapitel)} Kapiteln: "
          f"{len(bericht.fehler)} Fehler, {len(bericht.warnungen)} Warnungen ({dauer:.1f} s)")))
    return 1 if bericht.fehler else 0


if __name__ == "__main__":
    sys.exit(main())
