# -*- coding: utf-8 -*-
"""Selbsttest: prüft ALLE Inhalte automatisch (python3 mathe_quiz.py --selbsttest).

Fehler lassen den Test scheitern (Exit-Code 1), Warnungen nicht. Geprüft wird u. a.:
Musterlösungen bestehen ihren Prüfer, typische Fehlwerte werden erkannt und sind nie
richtig, jeder Generator läuft mit 200 Seeds, :::rechnung wird nachgerechnet, alle
Formeln sind gültig, alle Visuals gültig, Mindestanforderungen je Kapitel.
"""

import json
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path

from . import engine, markup, pruefer
from .engine import Erklaerung, Generator, Zusammenfassung

_FARBE = {"rot": "91", "gruen": "92", "gelb": "93", "fett": "1", "grau": "90"}
GENERATOR_SEEDS = 200


class Bericht:
    def __init__(self, farben=True, leise=False):
        self.farben = farben and sys.stdout.isatty()
        self.fehler, self.warnungen = [], []
        self.leise = leise
        self.ungeprueft = 0
        self.geprueft_schritte = 0

    def f(self, name, text):
        return f"\033[{_FARBE[name]}m{text}\033[0m" if self.farben else text

    def fehler_melden(self, ort, text):
        self.fehler.append(f"{ort}: {text}")
        print("  " + self.f("rot", f"FEHLER  {ort}: {text}"))

    def warnung_melden(self, ort, text):
        self.warnungen.append(f"{ort}: {text}")
        if not self.leise:
            print("  " + self.f("gelb", f"WARNUNG {ort}: {text}"))


# ──────────────────────────────────────────────────────────────────────────
#  Äquivalenz-Batterie (prüft den Prüfer)
# ──────────────────────────────────────────────────────────────────────────

AEQUIVALENT = [("(x+1)^2", "x^2+2x+1"), ("2(x+3)", "2x+6"), ("x/2", "0,5x"), ("(a-b)(a+b)", "a^2-b^2"),
               ("1/2+1/3", "5/6"), ("x^2*x^3", "x^5"), ("sqrt(x^2)", "|x|"), ("(x^2-1)/(x-1)", "x+1"),
               ("2^(n+1)", "2*2^n"), ("ln(e^x)", "x"), ("3x-(2-x)", "4x-2"), ("-(-x)", "x"),
               ("1/(1/x)", "x"), ("(2x)^2", "4x^2"), ("a/b/c", "a/(b*c)"), ("2^3^2", "512")]
NICHT_AEQUIVALENT = [("(a+b)^2", "a^2+b^2"), ("1/2+1/3", "2/5"), ("2(x+3)", "2x+3"), ("-x^2", "x^2"),
                     ("sqrt(x^2)", "x"), ("x^2*x^3", "x^6"), ("(x+1)/(x+2)", "1/2"), ("2^(n+1)", "2^n+1"),
                     ("3x-(2-x)", "2x-2"), ("a/b/c", "a/(b/c)")]


def batterie(bericht):
    for a, b in AEQUIVALENT:
        if not pruefer.aequivalent(pruefer.parse(a).ast, pruefer.parse(b).ast).ok:
            bericht.fehler_melden("Prüfer", f"{a} ≡ {b} wird nicht erkannt")
    for a, b in NICHT_AEQUIVALENT:
        if pruefer.aequivalent(pruefer.parse(a).ast, pruefer.parse(b).ast).ok:
            bericht.fehler_melden("Prüfer", f"{a} ≢ {b} wird fälschlich als gleich erkannt")


def escape_pruefen(bericht):
    """Jede Inhaltsdatei muss ohne SyntaxWarning übersetzbar sein (z. B. "\\frac" ohne r-String)."""
    import warnings
    from pathlib import Path
    for datei in sorted((Path(__file__).resolve().parent / "inhalte").glob("*.py")):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                compile(datei.read_text(encoding="utf-8"), str(datei), "exec")
            except (SyntaxWarning, SyntaxError) as e:
                bericht.fehler_melden(datei.name, f"{e} – r-String vergessen oder Backslash nicht verdoppelt?")


def typ_batterie(bericht):
    """Jeder Fragetyp: Musterantwort richtig, typische Fehler erkannt, Sonderfälle (LGS ohne Lösung …)."""
    from fractions import Fraction as F
    T = dict(tipps=["a", "b"], rechenweg="r", erklaerung="e")
    fragen = [
        engine.Termfrage("t", "x^2 + 2x + 1", form="ausmultipliziert", variablen="x", typische_fehler=[("x^2+1", "m")], **T),
        engine.Loesungsmengefrage("l", "{2; 3}", typische_fehler=[("{2}", "m")], **T),
        engine.Loesungsmengefrage("l2", "(-2; 2) ∪ [3; inf)", **T),
        engine.Mengefrage("m", "{1; 2; (1; 2)}", **T),
        engine.Vektorfrage("v", [1, F(1, 2), -3], typische_fehler=[([-1, F(-1, 2), 3], "m")], **T),
        engine.Vektorfrage("v2", [1, 2], vielfaches=True, **T),
        engine.Matrixfrage("M", [[1, 2], [3, 4]], typische_fehler=[([[1, 3], [2, 4]], "m")], **T),
        engine.LGSFrage("g1", [[1, 1], [1, -1]], [3, 1], **T),
        engine.LGSFrage("g2", [[1, 1, 1], [2, 2, 2]], [3, 6], **T),
        engine.LGSFrage("g3", [[1, 1], [1, 1]], [1, 2], **T),
        engine.GraphPunkt("p", {"funktionen": [{"term": "x^2 - 2"}]}, modus="setzen", ziel=(0, -2), **T),
        engine.GraphPunkt("p2", {"funktionen": [{"term": "x^2 - 2"}]}, modus="ablesen", loesung=-1, **T),
        engine.Zahlfrage("z", F(3, 4), gekuerzt=True, form="bruch", typische_fehler=[(F(3, 5), "m")], **T),
        engine.Luecke("lk", "\\frac{2}{3} = \\frac{\\luecke}{12}", [[8]], typische_fehler=[([2], "m")], **T),
    ]
    erwartet_art = {"g1": "eindeutig", "g2": "unendlich", "g3": "keine"}
    for q in fragen:
        f, _ = konkrete_frage_pruefen(q)
        for x in f:
            if "Formel" not in x:
                bericht.fehler_melden(f"Typ-Batterie {q.typ} {q.frage!r}", x)
        if q.frage in erwartet_art and q.loesung["art"] != erwartet_art[q.frage]:
            bericht.fehler_melden("Typ-Batterie LGS", f"{q.frage}: {q.loesung['art']} statt {erwartet_art[q.frage]}")
    falsch = [(fragen[0], "(x+1)^2", "fast"), (fragen[0], "x^2+2y+1", "lesefehler"), (fragen[12], "0,75", "fast"),
              (fragen[12], "6/8", "fast"), (fragen[7], {"keine": True}, "nicht_ok"), (fragen[7], {"werte": ["3", "0"]}, "nicht_ok"),
              (fragen[8], {"werte": ["3", "0", "0"]}, "nicht_ok"), (fragen[8], {"werte": ["3-t-s", "t", "s"]}, "ok"),
              (fragen[9], {"keine": False, "werte": ["1", "0"]}, "nicht_ok"), (fragen[5], ["-2", "-4"], "ok")]
    for q, antwort, soll in falsch:
        e = q.pruefen(antwort)
        ist = "ok" if e.ok else "fast" if e.fast else "lesefehler" if e.lesefehler else "nicht_ok"
        if ist != soll:
            bericht.fehler_melden("Typ-Batterie", f"{q.typ}: Antwort {antwort!r} ergibt {ist}, erwartet {soll}")


# ──────────────────────────────────────────────────────────────────────────
#  :::rechnung nachrechnen
# ──────────────────────────────────────────────────────────────────────────

_NICHT_GEPRUEFT = re.compile(r"\\(text|operatorname|lim|sum|int|prod|vec|begin|binom|in|forall|exists|mid|equiv|pmod|bmod|cup|cap|subset|Rightarrow|Leftrightarrow|approx)\b")


def _rechnung_zeile(tex):
    s = re.sub(r"^\s*(\\Rightarrow|\\Leftrightarrow|\\iff|\\implies|⇒|⇔)\s*", "", tex)
    s = re.sub(r"\\q?quad\s*(\\mid|\||\\vert).*$", "", s)        # Umformungs-Notiz am Rand: | -5
    s = re.sub(r"\\q?quad\s*$", "", s)
    oder = None
    if re.search(r"\\text\{\s*oder\s*\}", s):
        oder = re.split(r"\\text\{\s*oder\s*\}", s)
    return s, oder


def _ast_von(teil):
    if not teil.strip():
        return None
    return pruefer.parse(pruefer.latex_zu_term(teil)).ast


def _rel_gilt(a, rel, b):
    wa, wb = float(pruefer.wert(a)), float(pruefer.wert(b))
    eps = 1e-9 * max(1, abs(wa), abs(wb))
    return {"=": abs(wa - wb) <= eps, "≠": abs(wa - wb) > eps, "<": wa < wb - eps, ">": wa > wb + eps,
            "≤": wa <= wb + eps, "≥": wa >= wb - eps}[rel]


def _einsetzen(ast, name, wert):
    if ast[0] == "var" and ast[1] == name:
        return wert
    return tuple(_einsetzen(k, name, wert) if isinstance(k, tuple) else k for k in ast)


def rechnung_pruefen(schritte):
    """Rückgabe: (fehler: [str], ungeprueft: int, geprueft: int)."""
    fehler, ungeprueft, geprueft = [], 0, 0
    zeilen = []                       # (index, [asts], [rels]) oder None
    for i, s in enumerate(schritte):
        if s.get("falsch"):
            zeilen.append(None)
            continue
        if s.get("widerspruch"):
            # "#"-Zeile: eine falsche Aussage ohne Variable, aus der L = ∅ folgt
            try:
                teile, rels = pruefer.latex_relationen(_rechnung_zeile(s["tex"])[0])
                asts = [_ast_von(p) for p in teile]
                if any(a is None or pruefer.variablen_von(a) for a in asts):
                    fehler.append(f"Schritt {i + 1}: Widerspruchszeile (#) muss eine Aussage ohne Variable sein")
                elif all(_rel_gilt(a, r, b) for (a, b), r in zip(zip(asts, asts[1:]), rels)):
                    fehler.append(f"Schritt {i + 1}: Widerspruchszeile (#) ist gar keine falsche Aussage")
                else:
                    geprueft += 1
            except (pruefer.NichtPruefbar, pruefer.TermFehler):
                ungeprueft += 1
            zeilen.append(None)
            continue
        tex, oder = _rechnung_zeile(s["tex"])
        if oder:
            try:
                teile = [pruefer.latex_relationen(o) for o in oder]
                asts = [[_ast_von(p) for p in teil[0]] for teil in teile]
                zeilen.append(("oder", asts, [t[1] for t in teile], i))
            except (pruefer.NichtPruefbar, pruefer.TermFehler):
                ungeprueft += 1
                zeilen.append(None)
            continue
        if _NICHT_GEPRUEFT.search(tex):
            ungeprueft += 1
            zeilen.append(None)
            continue
        try:
            teile, rels = pruefer.latex_relationen(tex)
            if "≠" in rels:
                raise pruefer.NichtPruefbar("≠")
            asts = [_ast_von(p) for p in teile]
            zeilen.append(("normal", asts, rels, i))
        except (pruefer.NichtPruefbar, pruefer.TermFehler):
            ungeprueft += 1
            zeilen.append(None)

    # Fortsetzungen "= …" mit dem letzten Ausdruck der Vorzeile verbinden
    vorher = None
    for z in zeilen:
        if z and z[0] == "normal" and z[1] and z[1][0] is None and vorher is not None:
            z[1][0] = vorher
        if z and z[0] == "normal" and z[1] and z[1][-1] is not None:
            vorher = z[1][-1]
        elif z is None:
            vorher = None

    # Lösungszeilen am Ende: var = Konstante (auch x_1 = …)
    loesungen, loesung_zeilen = {}, set()
    for z in reversed(zeilen):
        if not z or z[0] != "normal" or set(z[2]) != {"="} or None in z[1]:
            break
        a, b = z[1][0], z[1][-1]
        if a[0] == "var" and not any(pruefer.variablen_von(t) for t in z[1][1:]):
            name = re.sub(r"_\w+$", "", a[1])
            try:
                loesungen.setdefault(name, []).append(pruefer.wert(b))
                loesung_zeilen.add(z[3])
            except pruefer.Undefiniert:
                break
        else:
            break

    hat_widerspruch = any(x.get("widerspruch") for x in schritte)

    # Wie oft kommt jede Variable in den Zeilen vor? (für Definitionszeilen wie "D = b^2 - 4ac")
    vorkommen = {}
    for z in zeilen:
        if z and z[0] == "normal":
            for t in z[1]:
                if t is not None:
                    for v in pruefer.variablen_von(t):
                        vorkommen[v] = vorkommen.get(v, 0) + 1

    def ohne_loesung(a, b):
        """a = b hat keine Lösung, weil a - b konstant und ≠ 0 ist (an Stichproben geprüft)."""
        vs = sorted(pruefer.variablen_von(a) | pruefer.variablen_von(b))
        werte = []
        for k in range(1, 8):
            bel = {v: Fraction(k * (j + 2), 7) + Fraction(1, 13) for j, v in enumerate(vs)}
            try:
                werte.append(pruefer.wert(("sub", a, b), bel))
            except pruefer.Undefiniert:
                continue
        return len(werte) >= 4 and all(pruefer.gleich(w, werte[0]) for w in werte) and not pruefer.gleich(werte[0], 0)

    # Formel umgestellt: letzte Zeile "v = Term", Term ohne v, aber mit anderen Variablen
    umgestellt = None
    for z in reversed(zeilen):
        if z and z[0] == "normal" and z[2] == ["="] and None not in z[1]:
            a, b = z[1]
            if a[0] == "var" and pruefer.variablen_von(b) and a[1] not in pruefer.variablen_von(b):
                umgestellt = (a[1], b)
        break

    ungleichung_ende = None
    for z in reversed(zeilen):
        if z and z[0] == "normal" and len(z[2]) == 1 and z[2][0] in "<>≤≥" and None not in z[1]:
            a, b = z[1]
            if a[0] == "var" and not pruefer.variablen_von(b):
                ungleichung_ende = z
        break

    def gilt(a, rel, b, bel):
        wa, wb = pruefer.wert(a, bel), pruefer.wert(b, bel)
        if rel == "=":
            return pruefer.gleich(wa, wb)
        fa, fb = float(wa), float(wb)
        eps = 1e-9 * max(1, abs(fa), abs(fb))
        return {"<": fa < fb - eps, ">": fa > fb + eps, "≤": fa <= fb + eps, "≥": fa >= fb - eps}[rel]

    for z in zeilen:
        if not z:
            continue
        art, asts, rels, idx = z
        if art == "oder" or idx in loesung_zeilen:
            if idx in loesung_zeilen:
                geprueft += 1
                for (a, b), rel in list(zip(zip(asts, asts[1:]), rels))[1:]:
                    try:
                        if not gilt(a, rel, b, {}):
                            fehler.append(f"Schritt {idx + 1}: {pruefer.zu_text(a)} {rel} {pruefer.zu_text(b)} stimmt nicht")
                    except pruefer.Undefiniert:
                        fehler.append(f"Schritt {idx + 1}: Ausdruck ist nicht definiert")
            continue
        if None in asts:
            ungeprueft += 1
            continue
        vs = set().union(*[pruefer.variablen_von(a) for a in asts])
        for nr, ((a, b), rel) in enumerate(zip(zip(asts, asts[1:]), rels)):
            paar_vs = pruefer.variablen_von(a) | pruefer.variablen_von(b)
            if nr == 0 and rel == "=" and a[0] == "var" and vorkommen.get(a[1], 0) == 1 \
                    and a[1] not in pruefer.variablen_von(b) and (len(asts) > 2 or pruefer.variablen_von(b)):
                ungeprueft += 1      # Definitionszeile: neuer Name für den Term rechts davon
                continue
            try:
                if not paar_vs:
                    if not gilt(a, rel, b, {}):
                        fehler.append(f"Schritt {idx + 1}: {pruefer.zu_text(a)} {rel} {pruefer.zu_text(b)} stimmt nicht")
                    geprueft += 1
                elif rel == "=" and loesungen and set(v for v in paar_vs) <= set(loesungen) and len(paar_vs) == 1:
                    v = next(iter(paar_vs))
                    werte = loesungen[v]
                    erfuellt = []
                    for w in werte:
                        try:
                            erfuellt.append(gilt(a, "=", b, {v: w}))
                        except pruefer.Undefiniert:
                            pass   # z. B. Division durch (x - 1) bei der Lösung x = 1: diese Lösung hier nicht prüfbar
                    if not erfuellt:
                        if pruefer.aequivalent(a, b).ok:
                            geprueft += 1
                        else:
                            ungeprueft += 1
                        continue
                    if not any(erfuellt):
                        if pruefer.aequivalent(a, b).ok:
                            geprueft += 1
                            continue
                        fehler.append(f"Schritt {idx + 1}: Die Lösung {v} = {werte} erfüllt "
                                      f"{pruefer.zu_text(a)} = {pruefer.zu_text(b)} nicht")
                    elif not all(erfuellt):
                        ungeprueft += 1
                    else:
                        geprueft += 1
                elif rel == "=" and hat_widerspruch and ohne_loesung(a, b):
                    geprueft += 1
                elif rel == "=":
                    if not pruefer.aequivalent(a, b).ok and umgestellt and umgestellt[0] in paar_vs and \
                            pruefer.aequivalent(_einsetzen(a, *umgestellt), _einsetzen(b, *umgestellt)).ok:
                        geprueft += 1
                        continue
                    if not pruefer.aequivalent(a, b).ok:
                        fehler.append(f"Schritt {idx + 1}: {pruefer.zu_text(a)} und {pruefer.zu_text(b)} "
                                      "sind nicht gleich (Umformung falsch?)")
                    geprueft += 1
                elif ungleichung_ende is not None and len(paar_vs) == 1:
                    _, (ea, eb), (erel,), _ = ungleichung_ende
                    v = ea[1]
                    if paar_vs != {v}:
                        ungeprueft += 1
                        continue
                    for k in range(-40, 41):
                        x = Fraction(k, 4) + Fraction(1, 997)
                        try:
                            if gilt(a, rel, b, {v: x}) != gilt(ea, erel, eb, {v: x}):
                                fehler.append(f"Schritt {idx + 1}: Die Ungleichung hat eine andere Lösungsmenge "
                                              f"als das Ergebnis (z. B. bei {v} = {float(x):.3f})")
                                break
                        except pruefer.Undefiniert:
                            continue
                    geprueft += 1
                else:
                    ungeprueft += 1
            except pruefer.Undefiniert:
                fehler.append(f"Schritt {idx + 1}: Ausdruck ist nicht definiert (Division durch 0?)")
            except pruefer.TermFehler:
                ungeprueft += 1
    return fehler, ungeprueft, geprueft


# ──────────────────────────────────────────────────────────────────────────
#  Fragen
# ──────────────────────────────────────────────────────────────────────────

def _texte_der_frage(q):
    texte = [q.frage, q.erklaerung, q.rechenweg] + list(q.tipps) + [m for _, m in q.typische_fehler]
    texte += list(getattr(q, "optionen", [])) + list(getattr(q, "richtig", [])) + list(getattr(q, "falsch", []))
    texte += list(getattr(q, "fehler", {}).values())
    texte += [x for p in getattr(q, "paare", []) for x in p]
    texte += list(getattr(q, "schritte", [])) if q.typ == "ordnen" else []
    if q.typ == "papier":
        texte += [q.musterloesung] + q.checkliste
    try:
        texte.append(q.loesung_anzeigen())
    except Exception as e:  # noqa: BLE001
        texte.append("")
        raise RuntimeError(f"loesung_anzeigen scheitert: {e}")
    return [t for t in texte if isinstance(t, str) and t]


def _markup_probleme(text):
    probleme = markup.pruefen(text)
    for f in markup.formeln(markup.parse(text)):
        for p in pruefer.latex_pruefen(f):
            probleme.append(f"Formel ${f[:40]}$: {p}")
    return list(dict.fromkeys(probleme))


_RECHENWEG_SCHRITT_TYPEN = {"zahl", "term", "loesungsmenge", "menge", "text", "vektor", "matrix", "mc", "luecke", "wf"}


def konkrete_frage_pruefen(q, ist_generator=False, glatt=False):
    """Prüft eine konkrete Frage. Rückgabe: (fehler, warnungen)."""
    fehler, warn = [], []
    for t in _texte_der_frage(q):
        for p in _markup_probleme(t):
            fehler.append(p)
        for b in markup.alle_bloecke(markup.parse(t)):
            if b["typ"] == "rechnung":
                f, _, _ = rechnung_pruefen(b["schritte"])
                fehler += [f":::rechnung: {x}" for x in f]
    if q.typ == "rechenweg":
        for i, st in enumerate(q.schritte):
            if st.typ not in _RECHENWEG_SCHRITT_TYPEN:
                fehler.append(f"Rechenweg-Schritt {i + 1}: Typ {st.typ!r} kann die Oberfläche als Teilschritt "
                              f"nicht anzeigen (erlaubt: {', '.join(sorted(_RECHENWEG_SCHRITT_TYPEN))})")
    if q.typ == "mc":
        if len(q.optionen) < 2:
            fehler.append("MC hat weniger als 2 Optionen")
        if len(set(q.optionen)) != len(q.optionen):
            fehler.append("MC hat doppelte Optionen")
        for o in q.fehler:
            if o not in q.optionen[1:]:
                fehler.append(f"fehler-Eintrag passt zu keiner falschen Option: {o!r}")
    if q.typ == "mehrfach" and set(q.richtig) & set(q.falsch):
        fehler.append("Option ist zugleich richtig und falsch")
    # Musterlösung
    if q.typ == "rechenweg":
        for i, s in enumerate(q.schritte):
            e = q.pruefen(engine.musterantwort(q, i))
            if not e.ok:
                fehler.append(f"Rechenweg-Schritt {i + 1}: Musterlösung besteht nicht ({e.meldung} {e.hinweis or ''})")
            f2, w2 = konkrete_frage_pruefen(s)
            fehler += [f"Schritt {i + 1}: {x}" for x in f2]
        if not 2 <= len(q.schritte) <= 5:
            warn.append(f"Rechenweg mit {len(q.schritte)} Schritten (empfohlen 2–5)")
    else:
        e = q.pruefen(engine.musterantwort(q))
        if not e.ok:
            fehler.append(f"Musterlösung besteht nicht: {e.meldung} {e.hinweis or ''}".strip())
    # Typische Fehler: nie richtig, immer erkannt
    for wert, meldung in q.typische_fehler:
        try:
            antwort = engine.fehler_als_antwort(q, wert)
            e = q.pruefen(antwort)
        except Exception as ex:  # noqa: BLE001
            fehler.append(f"Fehlwert {wert!r} lässt sich nicht prüfen: {type(ex).__name__}: {ex}")
            continue
        if e.ok or e.fast:
            fehler.append(f"Fehlwert {wert!r} wird als richtig gewertet (gleich der Lösung?)")
        elif e.lesefehler:
            fehler.append(f"Fehlwert {wert!r} ist nicht lesbar: {e.meldung}")
        elif not e.fehler_erkannt:
            fehler.append(f"Fehlwert {wert!r} wird nicht als typischer Fehler erkannt")
    # Tipps, Rechenweg, Erklärung
    mindest_tipps = 1 if q.typ in ("wf", "zuordnen", "papier") else 2
    if len(q.tipps) < mindest_tipps:
        fehler.append(f"nur {len(q.tipps)} Tipp(s), mindestens {mindest_tipps} (vage → konkret → fast Lösung)")
    elif len(q.tipps) < 3 and q.typ in engine.RECHEN_TYPEN:
        warn.append("weniger als 3 gestufte Tipps")
    if q.typ in engine.RECHEN_TYPEN | {"rechenweg"} and not q.rechenweg:
        fehler.append("Rechenaufgabe ohne Rechenweg")
    if not (q.erklaerung or q.rechenweg):
        fehler.append("weder Erklärung noch Rechenweg")
    if glatt and q.typ == "zahl":
        w = q.soll
        if not isinstance(w, Fraction) or w.denominator > 100 or abs(w.numerator) > 10 ** 6:
            fehler.append(f"Lösung ist nicht glatt: {w}")
    return fehler, warn


def frage_pruefen(q):
    """Rückgabe: (fehler, warnungen) für eine Frage aus einem Kapitel (Generator: 200 Seeds)."""
    try:
        if isinstance(q, Generator):
            fehler, warn = [], []
            gesehen = set()
            for seed in range(1, GENERATOR_SEEDS + 1):
                try:
                    k = q.instanz(seed)
                    k.to_dict()
                    f, w = konkrete_frage_pruefen(k, True, q.glatt)
                    if q.probe is not None and not q.probe(q.daten(seed)):
                        f.append("Generator-Probe schlägt fehl")
                    if not k.typische_fehler and k.typ in engine.RECHEN_TYPEN:
                        w.append("Generator-Instanz ohne typische Fehler")
                    gesehen.add(k.frage + "|" + str(k.loesung_anzeigen()))
                except ZeroDivisionError:
                    f, w = ["Division durch 0"], []
                except Exception as e:  # noqa: BLE001
                    f, w = [f"Ausnahme: {type(e).__name__}: {e}"], []
                for x in f:
                    if len(fehler) < 6:
                        fehler.append(f"seed {seed}: {x}")
                for x in w:
                    if x not in warn:
                        warn.append(x)
            if len(gesehen) < 10:
                warn.append(f"nur {len(gesehen)} verschiedene Aufgaben in {GENERATOR_SEEDS} Seeds")
            return fehler, warn
        fehler, warn = konkrete_frage_pruefen(q)
        # Bequeme Varianten gegenprüfen
        if getattr(q, "autor_loesung", None) is not None:
            autor = pruefer.bereich_parsen(str(q.autor_loesung), q.variable)
            if not pruefer.bereiche_gleich(autor, q.soll):
                fehler.append(f"Angegebene Lösung {q.autor_loesung!r} ≠ berechnet {pruefer.bereich_latex(q.soll)}")
        if q.typ == "term" and getattr(q, "aufgabe_term", None):
            a = pruefer.parse(q.aufgabe_term, q.variablen).ast
            if not pruefer.aequivalent(a, q.soll_term.ast, q.variablen).ok:
                fehler.append("vereinfache(): Lösung ist nicht äquivalent zum Ausgangsterm")
            if q.form and pruefer.form_pruefen(q.soll_term, q.form, q.soll_term.ast):
                fehler.append(f"vereinfache(): Lösung erfüllt die verlangte Form {q.form!r} selbst nicht")
        return fehler, warn
    except Exception as e:  # noqa: BLE001
        return [f"Ausnahme beim Prüfen: {type(e).__name__}: {e}"], []


# ──────────────────────────────────────────────────────────────────────────
#  Kapitel
# ──────────────────────────────────────────────────────────────────────────

def _glossar_pruefen(bericht, ort, text):
    from .inhalte import glossar
    for begriff in markup.glossar_verweise(text):
        if not glossar.finden(begriff):
            bericht.fehler_melden(ort, f"Glossar-Begriff [[{begriff}]] fehlt im Glossar (inhalte/_glossar_<kapitel>.py)")


def _alle_texte_eines_kapitels(kap):
    texte = [kap.warum_text or ""] + list(kap.lernziele)
    for e in kap.elemente:
        if isinstance(e, (Erklaerung, Zusammenfassung)):
            texte.append(e.text)
        elif isinstance(e, Generator):
            k = e.instanz(1)
            texte += _texte_der_frage(k)
        else:
            texte += _texte_der_frage(e)
    return texte


def kapitel_pruefen(kap, bericht, pool):
    ort = f"Kapitel {kap.nummer} ({kap.slug})"
    klausur = kap.teil == "klausur"
    fragen = kap.fragen()
    if not kap.quelle:
        bericht.fehler_melden(ort, "quelle fehlt (z. B. \"MVK 2026, VL 3\" oder \"Mathe I (PO 2023), Skript Kap. 2.1\")")

    # Markup, Formeln, Rechnungen
    seiten_gesamt = 0
    for e in kap.elemente:
        if not isinstance(e, (Erklaerung, Zusammenfassung)):
            continue
        eo = f"{ort}, {'Erklärung ' + repr(e.titel) if isinstance(e, Erklaerung) else 'Merkzettel'}"
        for p in _markup_probleme(e.text):
            bericht.fehler_melden(eo, p)
        seiten = e.seiten()
        for nr, seite in enumerate(seiten, 1):
            so = f"{eo}, Seite {nr}"
            for b in markup.alle_bloecke([seite]):
                if b["typ"] == "rechnung":
                    f, u, g = rechnung_pruefen(b["schritte"])
                    bericht.ungeprueft += u
                    bericht.geprueft_schritte += g
                    for x in f:
                        bericht.fehler_melden(so + ", :::rechnung", x)
            if isinstance(e, Erklaerung):
                seiten_gesamt += 1
                typen = {b["typ"] for b in seite}
                inner = {b["typ"] for b in markup.alle_bloecke([seite])}
                if not ({"rechnung", "visual"} & inner):
                    bericht.fehler_melden(so, "Seite ohne vorgerechnetes Beispiel (:::rechnung) und ohne :::visual")
                if "alt" not in typen:
                    bericht.fehler_melden(so, "Seite ohne :::alt (zweite Erklärung für „Ich verstehe das nicht“)")
                n = markup.woerter(seite)
                if n > 170:
                    bericht.fehler_melden(so, f"{n} Wörter (höchstens etwa 120)")
                elif n > 120:
                    bericht.warnung_melden(so, f"{n} Wörter (empfohlen höchstens 120)")
    if kap.warum_text:
        for p in _markup_probleme(kap.warum_text):
            bericht.fehler_melden(ort + ", Warum", p)
    for z in kap.lernziele:
        for p in _markup_probleme(z):
            bericht.fehler_melden(ort + ", Lernziel", p)
    for t in _alle_texte_eines_kapitels(kap):
        _glossar_pruefen(bericht, ort, t)

    # Mindestanforderungen
    if not klausur:
        if not 3 <= len(kap.lernziele) <= 5:
            bericht.fehler_melden(ort, f"{len(kap.lernziele)} Lernziele (verlangt 3–5)")
        if not kap.warum_text:
            bericht.fehler_melden(ort, "keine Warum-Box (k.warum(...))")
        if not 4 <= seiten_gesamt <= 10:
            bericht.fehler_melden(ort, f"{seiten_gesamt} Erklärseiten (verlangt 4–10)")
        boxen = [b for e in kap.erklaerungen() for b in markup.alle_bloecke(e.seiten())
                 if b["typ"] == "box" and b["art"] == "achtung"]
        if not boxen:
            bericht.fehler_melden(ort, "keine :::achtung-Box mit typischen Fehlern")
        ueben = [f for f in fragen if f.phase == "ueben"]
        praxis = [f for f in fragen if f.phase == "praxis"]
        if not 6 <= len(ueben) <= 14:
            bericht.fehler_melden(ort, f"{len(ueben)} Verständnis-/Rechenfragen (verlangt 6–14)")
        mit_fe = sum(1 for f in ueben if f.hat_fehlererkennung())
        if mit_fe < 3:
            bericht.fehler_melden(ort, f"nur {mit_fe} Fragen mit Fehlererkennung (verlangt mind. 3)")
        if kap.rechenthema and not kap.generatoren():
            bericht.fehler_melden(ort, "Rechenthema ohne Generator")
        if len(praxis) < 2:
            bericht.fehler_melden(ort, f"nur {len(praxis)} Praxisaufgaben (verlangt mind. 2, nach k.praxis())")
        if not any(f.uebungsblatt for f in praxis):
            bericht.fehler_melden(ort, "keine Praxisaufgabe im Übungsblatt-Stil (uebungsblatt=True)")
        if kap.zusammenfassung_text is None:
            bericht.fehler_melden(ort, "kein Merkzettel (k.zusammenfassung)")
        # Reihenfolge: lernziele -> erklaerung zuerst
        if kap.elemente and not isinstance(kap.elemente[0], Erklaerung):
            bericht.fehler_melden(ort, "das erste Element muss eine Erklärung sein")

    ergebnisse = list(pool.map(frage_pruefen, fragen))
    for q, (f, w) in zip(fragen, ergebnisse):
        for x in f:
            bericht.fehler_melden(f"{q.id} [{q.typ}]", x)
        for x in w:
            bericht.warnung_melden(f"{q.id} [{q.typ}]", x)
    return len(fragen)


def katex_pruefen(bericht):
    """Alle Formeln mit echtem KaTeX rendern, falls Node verfügbar ist."""
    node = shutil.which("node")
    skript = Path(__file__).resolve().parent.parent / "tools" / "katex_check.js"
    if not node or not skript.exists():
        bericht.warnung_melden("KaTeX", "Node nicht gefunden – Formeln nur mit dem Python-Validator geprüft "
                                        "(vollständig: E2E-Modus ?e2e=formeln im Browser)")
        return
    formeln = sorted(set(alle_formeln()))
    erg = subprocess.run([node, str(skript)], input=json.dumps(formeln), capture_output=True, text=True,
                         timeout=120, encoding="utf-8")
    for zeile in erg.stdout.splitlines():
        if zeile.startswith("FEHLER"):
            bericht.fehler_melden("KaTeX", zeile[7:])


def alle_formeln():
    """Alle LaTeX-Formeln aller Inhalte (auch für GET /api/e2e/formeln)."""
    erg = []
    for kap in engine.KAPITEL:
        for t in _alle_texte_eines_kapitels(kap):
            erg += markup.formeln(markup.parse(t))
        for e in kap.elemente:
            if hasattr(e, "formel"):
                erg.append(e.formel.replace("\\luecke", "\\boxed{\\phantom{00}}"))
    from .inhalte import FORMELSAMMLUNG, glossar
    erg += markup.formeln(markup.parse(FORMELSAMMLUNG))
    for g in glossar.GLOSSAR:
        erg += markup.formeln_im_text(g["erklaerung"]) + markup.formeln_im_text(g["beispiel"])
    return erg


def main(farben=True, kapitel=None, leise=False):
    start = time.time()
    bericht = Bericht(farben, leise)
    alle = list(engine.KAPITEL)
    if kapitel:
        wahl = [k for k in alle if k.slug in kapitel]
        if not wahl:
            print(f"Kein Kapitel mit slug {kapitel}")
            return 2
        alle = wahl
    print(bericht.f("fett", "SELBSTTEST – alle Inhalte werden geprüft …"))

    batterie(bericht)
    typ_batterie(bericht)
    escape_pruefen(bericht)
    ids = {}
    for kap in engine.KAPITEL:
        for f in kap.fragen():
            if re.search(r"-\d+$", f.id):
                bericht.fehler_melden(f.id, "Frage doppelt (gleicher Text im selben Kapitel)")
            ids[f.id] = f

    from .inhalte import FORMELSAMMLUNG, glossar, LADEFEHLER
    for name, text in LADEFEHLER + glossar.LADEFEHLER:
        bericht.fehler_melden(f"Modul {name}", f"lässt sich nicht laden: {text}")
    for p in _markup_probleme(FORMELSAMMLUNG):
        bericht.fehler_melden("Formelsammlung", p)
    namen = set()
    for g in glossar.GLOSSAR:
        o = f"Glossar „{g['begriff']}“"
        for feld in ("erklaerung", "beispiel"):
            for p in _markup_probleme(g[feld]):
                bericht.fehler_melden(o, p)
        for n in [g["begriff"]] + g["synonyme"]:
            if n.lower() in namen:
                bericht.fehler_melden(o, f"Begriff/Synonym {n!r} doppelt")
            namen.add(n.lower())
        if g["kapitel"] and not engine.kapitel_nach_slug(g["kapitel"]):
            bericht.warnung_melden(o, f"Kapitel {g['kapitel']!r} gibt es (noch) nicht")

    from . import demo
    for v in demo.demo_daten():
        if v["fehler"]:
            bericht.fehler_melden(f"Demo-Visual {v['art']}", v["fehler"])

    gesamt = 0
    with ThreadPoolExecutor(max_workers=8) as pool:
        for kap in alle:
            print(bericht.f("fett", f"\nKapitel {kap.nummer}: {kap.titel}") + bericht.f("grau", f"  [{kap.slug}, {kap.teil}]"))
            vorher = len(bericht.fehler)
            n = kapitel_pruefen(kap, bericht, pool)
            gesamt += n
            if len(bericht.fehler) == vorher:
                print("  " + bericht.f("gruen", f"✔ {n} Aufgaben in Ordnung"))
    katex_pruefen(bericht)

    dauer = time.time() - start
    farbe = "rot" if bericht.fehler else "gruen"
    print()
    print(bericht.f("grau", f"Nachgerechnete Rechnungsschritte: {bericht.geprueft_schritte}, "
                           f"nicht automatisch prüfbar: {bericht.ungeprueft}"))
    print(bericht.f("fett", bericht.f(farbe, f"{gesamt} Aufgaben in {len(alle)} Kapiteln: {len(bericht.fehler)} Fehler, "
                                             f"{len(bericht.warnungen)} Warnungen ({dauer:.1f} s)")))
    return 1 if bericht.fehler else 0


if __name__ == "__main__":
    sys.exit(main())
