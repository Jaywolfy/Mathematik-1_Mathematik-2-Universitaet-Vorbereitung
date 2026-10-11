# -*- coding: utf-8 -*-
"""Python-Seite der Visualisierungen (:::visual TYP + JSON).

Für jeden Typ gibt es ein Schema (Pflicht- und optionale Felder) und eine
Ergänzungsfunktion, die exakte Daten berechnet (Fraction). Das Frontend zeichnet
nur und rechnet höchstens numerisch für Regler und Kurven.

    pruefen(art, daten) -> [Probleme]
    ergaenzen(art, daten) -> daten (mit zusätzlichen Feldern, siehe ARCHITEKTUR.md §4)
"""

import itertools
import math
import re
from fractions import Fraction

from . import mathlib, pruefer

F = Fraction

# Feldtypen: zahl (int/float/"1/2"), text, bool, liste, objekt, term, beliebig
SCHEMA = {
    "zahlenstrahl": ({"von": "zahl", "bis": "zahl"},
                     {"schritt": "zahl", "punkte": "liste", "intervalle": "liste", "pfeile": "liste",
                      "interaktiv": "bool", "beschriftung": "text", "unterschrift": "text", "titel": "text",
                      "mengen": "liste"}),
    "bruch": ({"zaehler": "zahl", "nenner": "zahl"},
              {"modell": "text", "erweitern": "zahl", "kuerzen": "bool", "plus": "liste", "mal": "liste",
               "interaktiv": "bool", "unterschrift": "text", "titel": "text"}),
    "rechnung": ({"links": "term", "rechts": "term", "schritte": "liste"},
                 {"variable": "text", "unterschrift": "text", "titel": "text"}),
    "funktionsgraph": ({"funktionen": "liste"},
                       {"parameter": "liste", "x": "liste", "y": "liste", "wertetabelle": "liste",
                        "nullstellen": "bool", "scheitel": "bool", "punkte": "liste", "unterschrift": "text",
                        "titel": "text", "gleiche_achsen": "bool"}),
    "parabel": ({}, {"a": "zahl", "b": "zahl", "c": "zahl", "form": "text", "regler": "bool",
                     "x": "liste", "y": "liste", "unterschrift": "text", "titel": "text"}),
    "einheitskreis": ({}, {"winkel": "zahl", "regler": "bool", "zeige": "liste", "bogenmass": "bool",
                           "unterschrift": "text", "titel": "text"}),
    "exp_log": ({}, {"basis": "zahl", "umkehr": "bool", "regler": "bool", "x": "liste", "y": "liste",
                     "unterschrift": "text", "titel": "text"}),
    "venn": ({"mengen": "liste"}, {"universum": "liste", "universum_name": "text", "markiert": "text",
                                   "interaktiv": "bool", "unterschrift": "text", "titel": "text"}),
    "relation_graph": ({"links": "liste", "rechts": "liste", "pfeile": "liste"},
                       {"namen": "liste", "zeige": "liste", "aufdecken": "bool", "unterschrift": "text",
                        "titel": "text"}),
    "wahrheitstabelle": ({"variablen": "liste", "ausdruecke": "liste"},
                         {"darstellung": "text", "unterschrift": "text", "titel": "text", "markiert": "liste",
                          "schrittweise": "bool"}),
    "induktion_domino": ({}, {"anzahl": "zahl", "anfang": "zahl", "aussage": "text", "text_anfang": "text",
                              "text_schritt": "text", "unterschrift": "text", "titel": "text"}),
    "beweisbaum": ({"wurzel": "objekt"}, {"unterschrift": "text", "titel": "text"}),
    "binaer": ({}, {"bits": "zahl", "wert": "zahl", "interaktiv": "bool", "hex": "bool",
                    "unterschrift": "text", "titel": "text"}),
    "modulo_uhr": ({"n": "zahl"}, {"start": "zahl", "plus": "zahl", "mal": "zahl", "potenz": "zahl",
                                   "interaktiv": "bool", "unterschrift": "text", "titel": "text"}),
    "euklid": ({"a": "zahl", "b": "zahl"}, {"erweitert": "bool", "unterschrift": "text", "titel": "text"}),
    "pascal": ({}, {"zeilen": "zahl", "markiert": "liste", "interaktiv": "bool", "unterschrift": "text",
                    "titel": "text"}),
    "kombi_baum": ({"stufen": "liste"}, {"wahrscheinlichkeiten": "liste", "pfad": "liste",
                                         "unterschrift": "text", "titel": "text"}),
    "urne": ({"kugeln": "objekt", "ziehungen": "zahl"},
             {"zuruecklegen": "bool", "reihenfolge": "bool", "unterschrift": "text", "titel": "text"}),
    "vektoren2d": ({"vektoren": "liste"}, {"zeige": "liste", "interaktiv": "bool", "x": "liste", "y": "liste",
                                           "faktor": "zahl", "unterschrift": "text", "titel": "text"}),
    "vektoren3d": ({"vektoren": "liste"}, {"drehbar": "bool", "unterschrift": "text", "titel": "text"}),
    "gerade_ebene": ({}, {"geraden": "liste", "ebenen": "liste", "punkte": "liste", "dim": "zahl",
                          "unterschrift": "text", "titel": "text"}),
    "matrix_mult": ({"a": "liste", "b": "liste"}, {"unterschrift": "text", "titel": "text"}),
    "gauss": ({"matrix": "liste"}, {"rechts": "liste", "reduziert": "bool", "unterschrift": "text", "titel": "text"}),
    "lgs_geometrie": ({"gleichungen": "liste"}, {"regler": "bool", "unterschrift": "text", "titel": "text"}),
    "transformation2d": ({"matrix": "liste"}, {"regler": "bool", "eigenvektoren": "bool",
                                               "unterschrift": "text", "titel": "text"}),
    "folge": ({}, {"term": "term", "start": "zahl", "rekursion": "term", "n_von": "zahl", "n_bis": "zahl",
                   "grenzwert": "term", "epsilon": "zahl", "interaktiv": "bool", "monotonie": "bool",
                   "schranken": "bool", "y": "liste", "unterschrift": "text", "titel": "text"}),
    "reihe": ({"term": "term"}, {"k_von": "zahl", "n_bis": "zahl", "grenzwert": "term",
                                 "unterschrift": "text", "titel": "text"}),
    "stetigkeit": ({"term": "term", "stelle": "zahl"}, {"epsilon": "zahl", "delta": "zahl", "x": "liste",
                                                        "y": "liste", "unterschrift": "text", "titel": "text"}),
    "tangente": ({"term": "term", "x0": "zahl"}, {"h": "zahl", "ableitung": "term", "sekante": "bool",
                                                  "x": "liste", "y": "liste", "unterschrift": "text", "titel": "text"}),
    "ableitung_graph": ({"term": "term"}, {"x": "liste", "y": "liste", "unterschrift": "text", "titel": "text"}),
    "kurvendiskussion": ({"term": "term"}, {"x": "liste", "y": "liste", "unterschrift": "text", "titel": "text"}),
    "riemann": ({"term": "term", "von": "zahl", "bis": "zahl"},
                {"n": "zahl", "n_max": "zahl", "art": "text", "stammfunktion": "term", "x": "liste", "y": "liste",
                 "unterschrift": "text", "titel": "text"}),
    "flaeche_integral": ({"term": "term", "von": "zahl", "bis": "zahl"},
                         {"term2": "term", "x": "liste", "y": "liste", "unterschrift": "text", "titel": "text"}),
    "landau": ({"funktionen": "liste"}, {"n_bis": "zahl", "log_achse": "bool", "unterschrift": "text", "titel": "text"}),
    "komplexe_ebene": ({"z": "liste"}, {"w": "liste", "op": "text", "interaktiv": "bool", "x": "liste",
                                        "y": "liste", "unterschrift": "text", "titel": "text"}),
    "graph": ({"knoten": "liste", "kanten": "liste"}, {"gerichtet": "bool", "gewichte": "liste",
                                                       "markiert": "liste", "unterschrift": "text", "titel": "text"}),
    "baum": ({"wurzel": "objekt"}, {"unterschrift": "text", "titel": "text"}),
}
VISUAL_TYPEN = tuple(SCHEMA)

# Typen, die das Frontend schon zeichnen kann (wächst mit jeder Welle).
VISUAL_FERTIG = {"zahlenstrahl", "bruch", "rechnung", "funktionsgraph", "parabel"}
VISUAL_FERTIG |= {"einheitskreis", "exp_log", "tangente", "riemann", "vektoren2d", "matrix_mult", "gauss",
                  "komplexe_ebene"}  # vis_funktionen.js, vis_linalg.js
VISUAL_FERTIG |= {"venn", "wahrheitstabelle", "relation_graph", "pascal", "euklid", "modulo_uhr",
                  "induktion_domino", "folge"}  # vis_diskret.js


def _ist_zahl(v):
    if isinstance(v, bool):
        return False
    if isinstance(v, (int, float)):
        return True
    if isinstance(v, str):
        try:
            pruefer.zahl_parsen(v)
            return True
        except (pruefer.TermFehler, ArithmeticError):
            return v.strip() in ("inf", "-inf", "∞", "-∞")
    return False


def zahl(v):
    """JSON-Wert -> Fraction (oder float für inf/irrational)."""
    if isinstance(v, int):
        return F(v)
    if isinstance(v, float):
        return F(v).limit_denominator(10 ** 9) if math.isfinite(v) else v
    s = str(v).strip()
    if s in ("inf", "∞"):
        return math.inf
    if s in ("-inf", "-∞"):
        return -math.inf
    return pruefer.zahl_parsen(s)[1]


def zahl_tex(v):
    if isinstance(v, str) and v.strip() in ("inf", "∞", "-inf", "-∞"):
        return "-\\infty" if v.strip().startswith("-") else "\\infty"
    if isinstance(v, str):
        try:
            return pruefer.zu_latex(pruefer.parse(v).ast)
        except pruefer.TermFehler:
            return v
    if isinstance(v, float) and math.isinf(v):
        return "\\infty" if v > 0 else "-\\infty"
    return mathlib.tex(zahl(v))


def pruefen(art, daten):
    if art not in SCHEMA:
        return [f"Unbekannter Visual-Typ '{art}'. Erlaubt: {', '.join(VISUAL_TYPEN)}"]
    pflicht, optional = SCHEMA[art]
    probleme = []
    for feld, typ in pflicht.items():
        if feld not in daten:
            probleme.append(f"Pflichtfeld '{feld}' fehlt")
    for feld, wert in daten.items():
        typ = pflicht.get(feld) or optional.get(feld)
        if typ is None:
            if not feld.startswith("_"):
                probleme.append(f"unbekanntes Feld '{feld}'")
            continue
        if typ == "zahl" and not _ist_zahl(wert):
            probleme.append(f"Feld '{feld}' muss eine Zahl sein, nicht {wert!r}")
        elif typ == "text" and not isinstance(wert, str):
            probleme.append(f"Feld '{feld}' muss Text sein")
        elif typ == "bool" and not isinstance(wert, bool):
            probleme.append(f"Feld '{feld}' muss true/false sein")
        elif typ == "liste" and not isinstance(wert, list):
            probleme.append(f"Feld '{feld}' muss eine Liste sein")
        elif typ == "objekt" and not isinstance(wert, dict):
            probleme.append(f"Feld '{feld}' muss ein Objekt {{...}} sein")
        elif typ == "term":
            try:
                pruefer.parse(str(wert), ["n", "k", "x"])
            except pruefer.TermFehler as e:
                probleme.append(f"Feld '{feld}': Term {wert!r} unlesbar ({e.meldung})")
    if not probleme and art in _ZUSATZ_PRUEFUNG:   # inhaltliche Gegenprobe (z. B. Ableitung, Stammfunktion)
        probleme.extend(_ZUSATZ_PRUEFUNG[art](daten))
    if not probleme and art not in VISUAL_FERTIG:
        probleme.append(f"Visual-Typ '{art}' ist im Frontend noch nicht gebaut")
    return probleme


def ergaenzen(art, daten):
    fn = _ERGAENZER.get(art)
    if fn:
        fn(daten)
    return daten


# ──────────────────────────────────────────────────────────────────────────
#  Ergänzer
# ──────────────────────────────────────────────────────────────────────────

def _zahlenstrahl(d):
    d["_von"], d["_bis"] = float(zahl(d["von"])), float(zahl(d["bis"]))
    for p in d.get("punkte", []):
        p["_x"] = float(zahl(p["x"]))
        p["_tex"] = zahl_tex(p["x"])
    for iv in d.get("intervalle", []):
        iv["_von"], iv["_bis"] = float(zahl(iv["von"])), float(zahl(iv["bis"]))
        iv["_tex"] = (("[" if iv.get("von_zu") else "(") + zahl_tex(iv["von"]) + ", " + zahl_tex(iv["bis"])
                      + ("]" if iv.get("bis_zu") else ")"))
    for p in d.get("pfeile", []):
        p["_von"], p["_bis"] = float(zahl(p["von"])), float(zahl(p["bis"]))
        if "label" not in p:
            diff = zahl(p["bis"]) - zahl(p["von"])
            p["label"] = ("+" if diff >= 0 else "") + mathlib.tex(diff)


def _bruch(d):
    z, n = zahl(d["zaehler"]), zahl(d["nenner"])
    if n == 0 or z.denominator != 1 or n.denominator != 1:
        raise ValueError("Zähler und Nenner müssen ganze Zahlen sein, Nenner nicht 0")
    g = math.gcd(int(z), int(n))
    d["_gekuerzt"] = [int(z) // g, int(n) // g]
    d["_wert_tex"] = mathlib.tex(z / n)
    if "plus" in d:
        a, b = d["plus"]
        fa, fb = F(*a), F(*b)
        hn = mathlib.kgv(a[1], b[1])
        d["_plus"] = {"hauptnenner": hn, "a": [a[0] * hn // a[1], hn], "b": [b[0] * hn // b[1], hn],
                      "summe": [a[0] * hn // a[1] + b[0] * hn // b[1], hn],
                      "gekuerzt": [(fa + fb).numerator, (fa + fb).denominator]}


_OP_RE = re.compile(r"^\s*([-+*/:·×])\s*(.+)$")


def _rechnung(d):
    """Waage: Gleichung links = rechts, Schritte wie {"op": "-5", "text": "..."}."""
    var = d.get("variable", "x")
    l = mathlib.Polynom.aus_text(d["links"], var)
    r = mathlib.Polynom.aus_text(d["rechts"], var)
    zust = [_waage_zustand(l, r, None, d.get("text"))]
    for s in d["schritte"]:
        m = _OP_RE.match(str(s["op"]))
        if not m:
            raise ValueError(f"Schritt {s['op']!r}: erwartet z. B. '-5', '+2x', ':3', '*2'")
        op, arg = m.group(1), mathlib.Polynom.aus_text(m.group(2), var)
        if op in "+":
            l, r = l + arg, r + arg
        elif op == "-":
            l, r = l - arg, r - arg
        else:
            if arg.grad() != 0 or not arg.k:
                raise ValueError("Mal/Geteilt nur mit Zahlen ungleich 0")
            c = arg.k[0]
            if op in ":/":
                c = 1 / c
            l, r = l * c, r * c
        op_tex = {"+": "+", "-": "-", "*": "\\cdot", "·": "\\cdot", "×": "\\cdot", "/": ":", ":": ":"}[op]
        zust.append(_waage_zustand(l, r, f"{op_tex}\\ {arg.tex()}", s.get("text", "")))
    d["_zustaende"] = zust


def _waage_zustand(l, r, op_tex, text):
    def bild(p):
        # Bild aus Kästchen (x) und Gewichten (1), nur für kleine nichtnegative ganze Zahlen
        if p.grad() > 1 or any(c < 0 or c.denominator != 1 for c in p.k.values()):
            return None
        x, e = int(p.k.get(1, 0)), int(p.k.get(0, 0))
        return {"x": x, "eins": e} if x <= 8 and e <= 24 else None
    return {"links": l.tex(), "rechts": r.tex(), "op": op_tex, "text": text or "",
            "bild_links": bild(l), "bild_rechts": bild(r)}


def _funktionsgraph(d):
    params = {p["name"]: zahl(p.get("wert", 1)) for p in d.get("parameter", [])}
    for p in d.get("parameter", []):
        p["_von"], p["_bis"] = float(zahl(p.get("von", -5))), float(zahl(p.get("bis", 5)))
        p["_wert"] = float(params[p["name"]])
        p.setdefault("schritt", 0.5)
    for f in d["funktionen"]:
        t = pruefer.parse(f["term"], ["x"] + list(params))
        fremd = t.variablen - {"x"} - set(params)
        if fremd:
            raise ValueError(f"Unbekannte Variable(n) {fremd} in {f['term']!r}")
        f["_ast"] = pruefer.ast_json(t.ast)
        f["_tex"] = t.latex()
        # exakte Werte für die Startbelegung
        poly = None
        try:
            ersetzt = _ersetzen(t.ast, params)
            poly = mathlib.Polynom.aus_ast(ersetzt, "x")
        except Exception:
            ersetzt = None
        if d.get("nullstellen") and poly is not None and poly.grad() >= 1:
            try:
                f["_nullstellen"] = [{"x": g.f(), "tex": g.latex} for g in mathlib._nullstellen_exakt(poly)]
            except ValueError:
                f["_nullstellen"] = []
        if d.get("scheitel") and poly is not None and poly.grad() == 2:
            a, b, c = poly.k.get(2, F(0)), poly.k.get(1, F(0)), poly.k.get(0, F(0))
            xs = -b / (2 * a)
            ys = poly(xs)
            f["_scheitel"] = {"x": float(xs), "y": float(ys), "tex": f"({mathlib.tex(xs)} \\mid {mathlib.tex(ys)})"}
        if d.get("wertetabelle") and ersetzt is not None:
            zeilen = []
            for x in d["wertetabelle"]:
                xv = zahl(x)
                try:
                    yv = pruefer.wert(ersetzt, {"x": xv})
                    zeilen.append({"x": zahl_tex(x), "y": mathlib.tex(yv)})
                except pruefer.Undefiniert:
                    zeilen.append({"x": zahl_tex(x), "y": "\\text{n. d.}"})
            f["_tabelle"] = zeilen
    for p in d.get("punkte", []):
        p["_x"], p["_y"] = float(zahl(p["x"])), float(zahl(p["y"]))
        p.setdefault("label", f"({zahl_tex(p['x'])} \\mid {zahl_tex(p['y'])})")


def _ersetzen(ast, werte):
    if ast[0] == "var" and ast[1] in werte:
        return ("zahl", F(werte[ast[1]]), "")
    return tuple(_ersetzen(k, werte) if isinstance(k, tuple) else k for k in ast)


def _parabel(d):
    for k in ("a", "b", "c"):
        d.setdefault(k, 1 if k == "a" else 0)
    a, b, c = zahl(d["a"]), zahl(d["b"]), zahl(d["c"])
    if a == 0:
        raise ValueError("a darf nicht 0 sein")
    xs, ys = -b / (2 * a), c - b * b / (4 * a)
    d["_scheitel"] = {"x": float(xs), "y": float(ys), "tex": f"({mathlib.tex(xs)} \\mid {mathlib.tex(ys)})"}
    p = mathlib.Polynom({2: a, 1: b, 0: c})
    d["_nullstellen"] = [{"x": g.f(), "tex": g.latex} for g in mathlib._nullstellen_exakt(p)]
    d["_tex"] = p.tex()


# ── Logik für Wahrheitstabellen ──────────────────────────────────────────

_LOGIK_ERSATZ = [("<->", "⇔"), ("<=>", "⇔"), ("->", "⇒"), ("=>", "⇒"), ("\\Leftrightarrow", "⇔"),
                 ("\\Rightarrow", "⇒"), ("\\neg", "¬"), ("\\lnot", "¬"), ("\\land", "∧"), ("\\wedge", "∧"),
                 ("\\lor", "∨"), ("\\vee", "∨"), ("\\oplus", "⊕"), ("&&", "∧"), ("||", "∨")]


def logik_parse(text):
    s = str(text)
    for alt, neu in _LOGIK_ERSATZ:
        s = s.replace(alt, neu)
    s = re.sub(r"\bnot\b", "¬", s)
    s = re.sub(r"\band\b", "∧", s)
    s = re.sub(r"\bor\b", "∨", s)
    s = re.sub(r"\bxor\b", "⊕", s)
    s = s.replace("!", "¬").replace("&", "∧").replace("|", "∨").replace("~", "¬")
    toks = re.findall(r"[A-Za-z_]\w*|[()¬∧∨⇒⇔⊕]|\S", s)
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def nimm():
        pos[0] += 1
        return toks[pos[0] - 1]

    def aequ():
        a = impl()
        while peek() == "⇔":
            nimm()
            a = ("⇔", a, impl())
        return a

    def impl():
        a = oder()
        if peek() == "⇒":
            nimm()
            return ("⇒", a, impl())   # rechtsassoziativ
        return a

    def oder():
        a = xor()
        while peek() == "∨":
            nimm()
            a = ("∨", a, xor())
        return a

    def xor():
        a = und()
        while peek() == "⊕":
            nimm()
            a = ("⊕", a, und())
        return a

    def und():
        a = nicht()
        while peek() == "∧":
            nimm()
            a = ("∧", a, nicht())
        return a

    def nicht():
        if peek() == "¬":
            nimm()
            return ("¬", nicht())
        t = nimm()
        if t == "(":
            a = aequ()
            if nimm() != ")":
                raise ValueError("Klammer fehlt")
            return a
        if t is None or not re.fullmatch(r"[A-Za-z_]\w*", t):
            raise ValueError(f"Unerwartet: {t!r}")
        if t in ("w", "W", "1", "true", "True"):
            return ("konst", True)
        if t in ("f", "F", "0", "false", "False"):
            return ("konst", False)
        return ("var", t)

    a = aequ()
    if pos[0] != len(toks):
        raise ValueError(f"Zu viel am Ende: {toks[pos[0]:]}")
    return a


def logik_wert(a, bel):
    op = a[0]
    if op == "var":
        return bel[a[1]]
    if op == "konst":
        return a[1]
    if op == "¬":
        return not logik_wert(a[1], bel)
    x, y = logik_wert(a[1], bel), logik_wert(a[2], bel)
    return {"∧": x and y, "∨": x or y, "⇒": (not x) or y, "⇔": x == y, "⊕": x != y}[op]


def logik_tex(a, aussen=True):
    op = a[0]
    if op == "var":
        return a[1]
    if op == "konst":
        return "w" if a[1] else "f"
    if op == "¬":
        return "\\neg " + logik_tex(a[1], False)
    s = logik_tex(a[1], False) + " " + _LOGIK_TEX[op] + " " + logik_tex(a[2], False)
    return s if aussen else f"({s})"


_LOGIK_TEX = {"∧": "\\land", "∨": "\\lor", "⇒": "\\Rightarrow", "⇔": "\\Leftrightarrow", "⊕": "\\oplus"}


def logik_variablen(a):
    if a[0] == "var":
        return {a[1]}
    return set().union(*[logik_variablen(k) for k in a[1:] if isinstance(k, tuple)]) if len(a) > 1 else set()


def _wahrheitstabelle(d):
    variablen = [str(v) for v in d["variablen"]]
    asts = [logik_parse(a) for a in d["ausdruecke"]]
    for a, text in zip(asts, d["ausdruecke"]):
        fremd = logik_variablen(a) - set(variablen)
        if fremd:
            raise ValueError(f"{text!r} benutzt unbekannte Variable(n) {sorted(fremd)}")
    d["_kopf"] = [logik_tex(a) for a in asts]
    d["_zeilen"] = [{"werte": list(w), "ergebnisse": [logik_wert(a, dict(zip(variablen, w))) for a in asts]}
                    for w in itertools.product([True, False], repeat=len(variablen))]


def _euklid(d):
    a, b = int(zahl(d["a"])), int(zahl(d["b"]))
    d["_schritte"] = [list(s) for s in mathlib.euklid_schritte(a, b)]
    d["_ggt"] = math.gcd(a, b)
    if d.get("erweitert"):
        g, s, t, _ = mathlib.erweiterter_euklid(a, b)
        d["_bezout"] = {"s": s, "t": t, "tex": f"{g} = {s} \\cdot {a} {'+' if t >= 0 else '-'} {abs(t)} \\cdot {b}"}


def _pascal(d):
    n = int(zahl(d.get("zeilen", 7)))
    d["_zeilen"] = [[math.comb(i, k) for k in range(i + 1)] for i in range(n)]


def _matrix_mult(d):
    a, b = mathlib.matrix(d["a"]), mathlib.matrix(d["b"])
    c = mathlib.mat_mul(a, b)
    d["_a"] = [[mathlib.tex(x) for x in z] for z in a]
    d["_b"] = [[mathlib.tex(x) for x in z] for z in b]
    d["_c"] = [[mathlib.tex(x) for x in z] for z in c]
    d["_rechnungen"] = [[" + ".join(f"{mathlib.tex_klammer(a[i][k])} \\cdot {mathlib.tex_klammer(b[k][j])}"
                                    for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
    # einzelne Produkte a_ik · b_kj (zum Hervorheben Schritt für Schritt)
    d["_summanden"] = [[[f"{mathlib.tex_klammer(a[i][k])} \\cdot {mathlib.tex_klammer(b[k][j])}" for k in range(len(b))]
                        for j in range(len(b[0]))] for i in range(len(a))]


def _gauss(d):
    g = mathlib.gauss(d["matrix"], d.get("rechts"), reduziert=d.get("reduziert", True))
    trenner = len(d["matrix"][0]) if d.get("rechts") is not None else None
    d["_schritte"] = [{"tex": mathlib.tex_matrix(s["matrix"], trenner=trenner), "op": s["op"],
                       "pivot": s["pivot"], "zeilen": s["zeilen"],
                       "matrix": [[mathlib.tex(x) for x in z] for z in s["matrix"]]} for s in g["schritte"]]
    d["_rang"] = g["rang"]
    d["_spalten"] = len(d["matrix"][0])   # Spalten von A (danach folgt ggf. die rechte Seite)
    if d.get("rechts") is not None:
        lsg = mathlib.lgs_loesen(d["matrix"], d["rechts"])
        namen = [f"x_{{{i + 1}}}" for i in range(len(d["matrix"][0]))]
        if lsg["art"] == "keine":
            d["_loesung_tex"] = "\\mathbb{L} = \\emptyset"
        elif lsg["art"] == "eindeutig":
            d["_loesung_tex"] = ",\\quad ".join(f"{n} = {mathlib.tex(x)}" for n, x in zip(namen, lsg["x"]))
        else:
            d["_loesung_tex"] = "\\text{unendlich viele Lösungen (" + str(len(lsg["richtungen"])) + " freie Variable" \
                + ("n" if len(lsg["richtungen"]) > 1 else "") + ")}"


_ERGAENZER = {
    "zahlenstrahl": _zahlenstrahl, "bruch": _bruch, "rechnung": _rechnung, "funktionsgraph": _funktionsgraph,
    "parabel": _parabel, "wahrheitstabelle": _wahrheitstabelle, "euklid": _euklid, "pascal": _pascal,
    "matrix_mult": _matrix_mult, "gauss": _gauss,
}


# ──────────────────────────────────────────────────────────────────────────
#  Funktionen/Analysis und Lineare Algebra/komplexe Zahlen
#  (einheitskreis, exp_log, tangente, riemann, vektoren2d, komplexe_ebene;
#   matrix_mult/gauss oben). Frontend: vis_funktionen.js, vis_linalg.js
# ──────────────────────────────────────────────────────────────────────────

def _wurzel_bruch_tex(q):
    """√q für eine Fraction q ≥ 0 als TeX, teilweise radiziert (√(3/4) -> \\frac{\\sqrt{3}}{2})."""
    q = F(q)
    k, m = mathlib.wurzel_vereinfachen(q.numerator * q.denominator)
    c = F(k, q.denominator)
    if m == 1:
        return mathlib.tex(c)
    w = f"\\sqrt{{{m}}}"
    z = w if c.numerator == 1 else f"{c.numerator}{w}"
    return z if c.denominator == 1 else f"\\frac{{{z}}}{{{c.denominator}}}"


def _pi_tex(q):
    """q·π als TeX (q Fraction)."""
    q = F(q)
    if q == 0:
        return "0"
    vz, q = ("-" if q < 0 else ""), abs(q)
    z = "\\pi" if q.numerator == 1 else f"{q.numerator}\\pi"
    return vz + (z if q.denominator == 1 else f"\\frac{{{z}}}{{{q.denominator}}}")


def _wert_tex(v):
    """(TeX, exakt) für einen Wert aus pruefer.wert.

    Fraction ist exakt. Ein float wird als ±c·√m (c rational) oder c·π erkannt, wenn er auf
    12 Stellen damit übereinstimmt (z. B. sqrt(3)/2 oder 1 - cos(pi)); sonst (Dezimalzahl, False).
    """
    if isinstance(v, (int, F)):
        return mathlib.tex(F(v)), True
    v = float(v)
    if not math.isfinite(v):
        return ("\\infty" if v > 0 else "-\\infty"), False
    q = F(v * v).limit_denominator(1000)
    if q.numerator < 10 ** 7 and abs(float(q) - v * v) <= 1e-12 * max(1.0, v * v):
        t = _wurzel_bruch_tex(q)
        return (("-" + t) if v < 0 and t != "0" else t), True
    q = F(v / math.pi).limit_denominator(60)
    if q != 0 and abs(float(q) * math.pi - v) <= 1e-12 * max(1.0, abs(v)):
        return _pi_tex(q), True
    return mathlib.dezimal(v, 4), False


def _gleich_tex(v):
    """'= …' oder '\\approx …'."""
    t, exakt = _wert_tex(v)
    return ("= " if exakt else "\\approx ") + t


def _zahl_tex_kurz(v):
    """Wie zahl_tex, rationale Werte aber gekürzt und mit Vorzeichen vor dem Bruch (-1/2 -> -\\frac{1}{2})."""
    w = zahl(v)
    return mathlib.tex(w) if isinstance(w, F) else zahl_tex(v)


def _klammer_tex(t):
    t = str(t)
    return f"\\left({t}\\right)" if t.startswith("-") or any(c in t[1:] for c in "+-") else t


def _term_x(feld, text):
    t = pruefer.parse(str(text), ["x"])
    fremd = t.variablen - {"x"}
    if fremd:
        raise ValueError(f"Feld '{feld}': nur die Variable x ist erlaubt, nicht {', '.join(sorted(fremd))}")
    return t


def _fwert(ast, x):
    """float-Wert oder None (undefiniert)."""
    try:
        w = float(pruefer.wert(ast, {"x": x}))
    except (pruefer.Undefiniert, ArithmeticError, OverflowError, ValueError):
        return None
    return w if math.isfinite(w) else None


def _ableitung_passt(f_ast, g_ast, lo, hi, n=31):
    """Stichprobe: stimmt g mit dem zentralen Differenzenquotienten von f überein?
    Rückgabe None (passt) oder Fehlertext."""
    gueltig = 0
    for i in range(n):
        x = lo + (hi - lo) * (i + 0.3711) / n
        hh = 1e-5 * max(1.0, abs(x))
        f1, f2, g = _fwert(f_ast, x + hh), _fwert(f_ast, x - hh), _fwert(g_ast, x)
        if f1 is None or f2 is None or g is None or abs(f1) > 1e8 or abs(f2) > 1e8:
            continue
        dq = (f1 - f2) / (2 * hh)
        if abs(dq - g) > 1e-4 * max(1.0, abs(dq), abs(g)):
            return f"bei x ≈ {x:.3f}: Differenzenquotient ≈ {dq:.5g}, angegeben {g:.5g}"
        gueltig += 1
    return None if gueltig >= 5 else "zu wenige Stellen, an denen beide Terme definiert sind"


def _pruefen_tangente(d):
    if "ableitung" not in d:
        return []
    try:
        f, g = _term_x("term", d["term"]), _term_x("ableitung", d["ableitung"])
        x0 = float(zahl(d["x0"]))
        lo, hi = (float(zahl(v)) for v in d["x"]) if isinstance(d.get("x"), list) and len(d["x"]) == 2 else (x0 - 4, x0 + 4)
    except (ValueError, ArithmeticError) as e:
        return [str(e)]
    fehler = _ableitung_passt(f.ast, g.ast, lo, hi)
    return [f"Feld 'ableitung' ist nicht die Ableitung von {d['term']!r} ({fehler})"] if fehler else []


def _pruefen_riemann(d):
    if "stammfunktion" not in d:
        return []
    try:
        f, s = _term_x("term", d["term"]), _term_x("stammfunktion", d["stammfunktion"])
        a, b = float(zahl(d["von"])), float(zahl(d["bis"]))
    except (ValueError, ArithmeticError) as e:
        return [str(e)]
    if not a < b:
        return ["'von' muss kleiner als 'bis' sein"]
    fehler = _ableitung_passt(s.ast, f.ast, a, b)
    return [f"Feld 'stammfunktion' passt nicht zu {d['term']!r}: F' ≠ f ({fehler})"] if fehler else []


_ZUSATZ_PRUEFUNG = {"tangente": _pruefen_tangente, "riemann": _pruefen_riemann}


# ── Einheitskreis ──

_SIN_Q1 = {0: "0", 15: "\\frac{\\sqrt{6}-\\sqrt{2}}{4}", 30: "\\frac{1}{2}", 45: "\\frac{\\sqrt{2}}{2}",
           60: "\\frac{\\sqrt{3}}{2}", 75: "\\frac{\\sqrt{6}+\\sqrt{2}}{4}", 90: "1"}
_TAN_Q1 = {0: "0", 15: "2-\\sqrt{3}", 30: "\\frac{\\sqrt{3}}{3}", 45: "1", 60: "\\sqrt{3}", 75: "2+\\sqrt{3}"}
_TAN_NEG = {15: "\\sqrt{3}-2", 75: "-2-\\sqrt{3}"}
_SIN_NEG = {15: "\\frac{\\sqrt{2}-\\sqrt{6}}{4}"}


def _sin_grad_tex(g):
    g %= 360
    ref, neg = (g, False) if g <= 90 else (180 - g, False) if g <= 180 else (g - 180, True) if g <= 270 else (360 - g, True)
    t = _SIN_Q1[ref]
    return _SIN_NEG.get(ref, "-" + t) if neg and t != "0" else t


def _tan_grad_tex(g):
    g %= 180
    if g == 90:
        return None
    if g < 90:
        return _TAN_Q1[g]
    ref = 180 - g
    return _TAN_NEG.get(ref, "-" + _TAN_Q1[ref])


def _einheitskreis(d):
    erlaubt = {"sin", "cos", "tan", "kurve"}
    zeige = d.setdefault("zeige", ["sin", "cos", "kurve"])
    falsch = [z for z in zeige if z not in erlaubt]
    if falsch:
        raise ValueError(f"zeige: unbekannt {falsch}, erlaubt {sorted(erlaubt)}")
    g = float(zahl(d.get("winkel", 30)))
    d["_winkel"] = g % 360 if not (g == 360) else 360.0
    tab = []
    for gr in range(0, 361, 15):
        tab.append({"grad": gr, "rad": _pi_tex(F(gr, 180)), "sin": _sin_grad_tex(gr),
                    "cos": _sin_grad_tex(gr + 90), "tan": _tan_grad_tex(gr)})
    d["_tabelle"] = tab


# ── Exponential- und Logarithmusfunktion ──

def _exp_log(d):
    roh = d.get("basis", 2)
    a = float(zahl(roh))
    if not a > 0 or abs(a - 1) < 1e-12:
        raise ValueError("Die Basis muss positiv und ungleich 1 sein")
    ist_e = isinstance(roh, str) and roh.strip() == "e"
    bt = _zahl_tex_kurz(roh)
    d["_basis"], d["_basis_tex"] = a, bt
    basis = bt if re.fullmatch(r"\d+", bt) else "\\left(" + bt + "\\right)"
    d["_exp_tex"] = "e^{x}" if ist_e else basis + "^{x}"
    d["_log_tex"] = "\\ln(x)" if ist_e else f"\\log_{{{bt}}}(x)"
    d["_punkte"] = {"exp": [{"x": 0, "y": 1, "tex": "(0 \\mid 1)"}, {"x": 1, "y": a, "tex": f"(1 \\mid {bt})"}],
                    "log": [{"x": 1, "y": 0, "tex": "(1 \\mid 0)"}, {"x": a, "y": 1, "tex": f"({bt} \\mid 1)"}]}


# ── Tangente und Sekante ──

def _tangente(d):
    t = _term_x("term", d["term"])
    d["_ast"], d["_tex"] = pruefer.ast_json(t.ast), t.latex()
    x0 = zahl(d["x0"])
    d["_x0"], d["_x0_tex"] = float(x0), _zahl_tex_kurz(d["x0"])
    try:
        y0 = pruefer.wert(t.ast, {"x": x0})
    except pruefer.Undefiniert:
        raise ValueError(f"f ist an der Stelle x0 = {d['x0']} nicht definiert")
    d["_y0"], (d["_y0_tex"], _) = float(y0), _wert_tex(y0)
    h = zahl(d.get("h", 1))
    if float(h) == 0:
        raise ValueError("h darf nicht 0 sein (die Sekante braucht zwei Punkte)")
    d["_h"] = float(h)
    try:
        y1 = pruefer.wert(t.ast, {"x": x0 + h})
        d["_m_sek_tex"] = _gleich_tex((y1 - y0) / h if isinstance(y1, F) and isinstance(y0, F) and isinstance(h, F)
                                      else (float(y1) - float(y0)) / float(h))
    except pruefer.Undefiniert:
        d["_m_sek_tex"] = None
    if "ableitung" in d:
        g = _term_x("ableitung", d["ableitung"])
        d["_abl_ast"], d["_abl_tex"] = pruefer.ast_json(g.ast), g.latex()
        try:
            m = pruefer.wert(g.ast, {"x": x0})
        except pruefer.Undefiniert:
            raise ValueError("Die Ableitung ist an x0 nicht definiert")
        d["_m"] = float(m)
        d["_m_tex"] = _gleich_tex(m)
        if all(isinstance(v, F) for v in (m, y0, x0)):
            d["_tangente_tex"] = "y = " + mathlib.Polynom({1: m, 0: y0 - m * x0}).tex()
        else:
            mt, x0t, y0t = _wert_tex(m)[0], d["_x0_tex"], d["_y0_tex"]
            d["_tangente_tex"] = f"y = {_klammer_tex(mt)} \\cdot (x - {_klammer_tex(x0t)}) + {_klammer_tex(y0t)}"


# ── Riemann-Summen ──

_RIEMANN_ARTEN = ("links", "rechts", "mitte", "ober", "unter")


def _riemann(d):
    t = _term_x("term", d["term"])
    a, b = zahl(d["von"]), zahl(d["bis"])
    if not float(a) < float(b):
        raise ValueError("'von' muss kleiner als 'bis' sein")
    n = zahl(d.get("n", 4))
    if n != int(n) or not 1 <= int(n) <= 500:
        raise ValueError("n muss eine ganze Zahl von 1 bis 500 sein")
    n = int(n)
    n_max = int(zahl(d.get("n_max", max(50, n))))
    art = d.setdefault("art", "links")
    if art not in _RIEMANN_ARTEN:
        raise ValueError(f"art muss eine von {', '.join(_RIEMANN_ARTEN)} sein")
    d.update({"_ast": pruefer.ast_json(t.ast), "_tex": t.latex(), "_von": float(a), "_bis": float(b),
              "_von_tex": _zahl_tex_kurz(d["von"]), "_bis_tex": _zahl_tex_kurz(d["bis"]), "_n": n, "_n_max": max(n, n_max)})
    for i in range(41):
        if _fwert(t.ast, float(a) + (float(b) - float(a)) * i / 40) is None:
            raise ValueError("f ist auf [von, bis] nicht überall definiert")
    dx = (b - a) / n
    summe = F(0) if isinstance(dx, F) else 0.0
    for i in range(n):
        l, r = a + i * dx, a + (i + 1) * dx
        if art in ("links", "rechts", "mitte"):
            y = pruefer.wert(t.ast, {"x": {"links": l, "rechts": r, "mitte": (l + r) / 2}[art]})
        else:
            # Ober-/Untersumme: Extremum der Stichprobe; liegt es am Rand, wird exakt gerechnet
            xs = [l + (r - l) * k / 40 for k in range(41)]
            ys = [_fwert(t.ast, x) for x in xs]
            j = (max if art == "ober" else min)(range(41), key=lambda k: ys[k])
            y = pruefer.wert(t.ast, {"x": xs[j]}) if j in (0, 40) else ys[j]
        summe = summe + y * dx if isinstance(y, F) and isinstance(summe, F) else float(summe) + float(y) * float(dx)
    st, exakt = _wert_tex(summe)
    d["_summe"] = {"n": n, "art": art, "wert": float(summe), "tex": st if exakt else None}
    if "stammfunktion" in d:
        s = _term_x("stammfunktion", d["stammfunktion"])
        fb, fa = pruefer.wert(s.ast, {"x": b}), pruefer.wert(s.ast, {"x": a})
        w = fb - fa if isinstance(fb, F) and isinstance(fa, F) else float(fb) - float(fa)
        wt, exakt = _wert_tex(w)
        d["_stamm_tex"] = s.latex()
        d["_integral"] = {"wert": float(w), "tex": wt, "exakt": exakt}


# ── Vektoren in der Ebene ──

def _vek_tex(x, y):
    return f"\\begin{{pmatrix}} {_wert_tex(x)[0]} \\\\ {_wert_tex(y)[0]} \\end{{pmatrix}}"


def _norm_tex(x, y):
    if isinstance(x, F) and isinstance(y, F):
        return "= " + _wurzel_bruch_tex(x * x + y * y)
    return _gleich_tex(math.hypot(float(x), float(y)))


def _vektoren2d(d):
    erlaubt = {"summe", "differenz", "kette", "vielfaches", "norm", "skalarprodukt"}
    zeige = d.setdefault("zeige", [])
    falsch = [z for z in zeige if z not in erlaubt]
    if falsch:
        raise ValueError(f"zeige: unbekannt {falsch}, erlaubt {sorted(erlaubt)}")
    vs = d["vektoren"]
    if not vs or len(vs) > 4:
        raise ValueError("1 bis 4 Vektoren angeben")
    werte = []
    for i, v in enumerate(vs):
        if not isinstance(v, dict) or "x" not in v or "y" not in v:
            raise ValueError("Jeder Vektor braucht {x, y}")
        x, y = zahl(v["x"]), zahl(v["y"])
        werte.append((x, y))
        v["_x"], v["_y"], v["_tex"] = float(x), float(y), _vek_tex(x, y)
        v["_norm_tex"] = _norm_tex(x, y)
        v.setdefault("label", "\\vec{" + "abcd"[i] + "}")
    if {"summe", "differenz", "kette", "skalarprodukt"} & set(zeige) and len(vs) < 2:
        raise ValueError("Summe, Differenz, Kette und Skalarprodukt brauchen zwei Vektoren")
    if len(vs) >= 2:
        (ax, ay), (bx, by) = werte[0], werte[1]
        d["_summe"] = {"tex": _vek_tex(ax + bx, ay + by), "norm_tex": _norm_tex(ax + bx, ay + by)}
        d["_differenz"] = {"tex": _vek_tex(ax - bx, ay - by), "norm_tex": _norm_tex(ax - bx, ay - by)}
        sp = ax * bx + ay * by
        d["_skalarprodukt"] = {"tex": _gleich_tex(sp), "orthogonal": abs(float(sp)) < 1e-12}
    lam = zahl(d.get("faktor", 2))
    d["_faktor"], d["_faktor_tex"] = float(lam), _zahl_tex_kurz(d.get("faktor", 2))
    ax, ay = werte[0]
    d["_vielfaches"] = {"tex": _vek_tex(lam * ax, lam * ay)}


# ── Komplexe Zahlen ──

def _komplex_tex(re, im):
    rt, re_ex = _wert_tex(re)
    it, im_ex = _wert_tex(abs(im) if isinstance(im, F) else abs(float(im)))
    r0, i0 = float(re) == 0, float(im) == 0
    if i0:
        return rt, re_ex
    ipart = "i" if it == "1" else (f"{_klammer_tex(it)}\\,i" if "\\frac" not in it else f"{it}\\,i")
    if r0:
        return ("-" if float(im) < 0 else "") + ipart, im_ex
    return f"{rt} {'-' if float(im) < 0 else '+'} {ipart}", re_ex and im_ex


def _komplex_info(re, im):
    tex, exakt = _komplex_tex(re, im)
    info = {"re": float(re), "im": float(im), "tex": tex, "exakt": exakt}
    if isinstance(re, F) and isinstance(im, F):
        bt, b_ex = _wurzel_bruch_tex(re * re + im * im), True
    else:
        bt, b_ex = _wert_tex(math.hypot(float(re), float(im)))
    info["betrag_tex"], info["betrag_exakt"] = bt, b_ex
    if float(re) == 0 and float(im) == 0:
        info.update(arg=None, arg_tex=None, arg_exakt=False, polar_tex="0")
        return info
    phi = math.atan2(float(im), float(re))
    q = F(phi / math.pi).limit_denominator(12)
    a_ex = abs(float(q) * math.pi - phi) <= 1e-9
    at = _pi_tex(q) if a_ex else mathlib.dezimal(phi, 4)
    info.update(arg=phi, arg_tex=at, arg_exakt=a_ex, arg_grad=math.degrees(phi))
    r = "" if bt == "1" else _klammer_tex(bt) + " \\cdot "
    if at == "0":
        info["polar_tex"] = f"{bt} \\cdot e^{{0}}"
    else:
        mal = "" if a_ex else " \\cdot "
        info["polar_tex"] = f"{r}e^{{{'-' if at.startswith('-') else ''}i{mal}{at.lstrip('-')}}}"
    info["polar_exakt"] = b_ex and a_ex
    return info


def _komplex_zahl(feld, paar):
    if not isinstance(paar, list) or len(paar) != 2:
        raise ValueError(f"'{feld}' muss [Realteil, Imaginärteil] sein, z. B. [3, 4]")
    return zahl(paar[0]), zahl(paar[1])


_KOMPLEX_OPS = ("keine", "konjugiert", "plus", "minus", "mal", "geteilt")


def _komplexe_ebene(d):
    zr, zi = _komplex_zahl("z", d["z"])
    d["_z"] = _komplex_info(zr, zi)
    op = d.setdefault("op", "mal" if "w" in d else "keine")
    if op not in _KOMPLEX_OPS:
        raise ValueError(f"op muss eine von {', '.join(_KOMPLEX_OPS)} sein")
    if op in ("plus", "minus", "mal", "geteilt") and "w" not in d:
        raise ValueError(f"op '{op}' braucht eine zweite Zahl w")
    if "w" in d:
        wr, wi = _komplex_zahl("w", d["w"])
        d["_w"] = _komplex_info(wr, wi)
    exakt = all(isinstance(v, F) for v in (zr, zi)) and ("w" not in d or all(isinstance(v, F) for v in (wr, wi)))
    num = (lambda v: v) if exakt else float
    if op == "konjugiert":
        er, ei = zr, -zi
    elif op == "plus":
        er, ei = num(zr) + num(wr), num(zi) + num(wi)
    elif op == "minus":
        er, ei = num(zr) - num(wr), num(zi) - num(wi)
    elif op == "mal":
        er, ei = num(zr) * num(wr) - num(zi) * num(wi), num(zr) * num(wi) + num(zi) * num(wr)
    elif op == "geteilt":
        nn = num(wr) * num(wr) + num(wi) * num(wi)
        if float(nn) == 0:
            raise ValueError("Division durch 0 (w = 0)")
        er, ei = (num(zr) * num(wr) + num(zi) * num(wi)) / nn, (num(zi) * num(wr) - num(zr) * num(wi)) / nn
    else:
        return
    d["_ergebnis"] = _komplex_info(er, ei)


_ERGAENZER.update({
    "einheitskreis": _einheitskreis, "exp_log": _exp_log, "tangente": _tangente, "riemann": _riemann,
    "vektoren2d": _vektoren2d, "komplexe_ebene": _komplexe_ebene,
})
