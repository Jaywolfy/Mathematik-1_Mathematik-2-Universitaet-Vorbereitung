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
    "komplexe_ebene": ({}, {"z": "liste", "w": "liste", "op": "text", "interaktiv": "bool", "x": "liste",
                            "y": "liste", "punkte": "liste", "konjugiert": "bool", "betragskreis": "bool",
                            "pfeile": "bool", "unterschrift": "text", "titel": "text"}),
    "graph_gerichtet": ({"elemente": "liste", "paare": "liste"},
                        {"layout": "beliebig", "markiert": "liste", "unterschrift": "text", "titel": "text"}),
    "hasse": ({"elemente": "liste", "paare": "liste"},
              {"teilmenge": "liste", "sup": "bool", "inf": "bool", "schranken": "bool", "unterschrift": "text",
               "titel": "text"}),
    "aequivalenz_klassen": ({"klassen": "liste"},
                            {"elemente": "liste", "repraesentanten": "liste", "namen": "liste", "graph": "bool",
                             "unterschrift": "text", "titel": "text"}),
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
VISUAL_FERTIG |= {"graph_gerichtet", "hasse", "aequivalenz_klassen"}  # vis_ordnung.js


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


# ── Diskrete Visuals (Frontend: vis_diskret.js) ──────────────────────────

def _ganz(v, feld, von=None, bis=None):
    """JSON-Wert -> int mit Bereichsprüfung (verständliche Fehlermeldung)."""
    try:
        z = zahl(v)
    except (pruefer.TermFehler, ArithmeticError, ValueError):
        raise ValueError(f"'{feld}' muss eine ganze Zahl sein, nicht {v!r}")
    if isinstance(z, float) or z.denominator != 1:
        raise ValueError(f"'{feld}' muss eine ganze Zahl sein, nicht {v!r}")
    z = int(z)
    if (von is not None and z < von) or (bis is not None and z > bis):
        grenzen = f"mindestens {von}" if bis is None else (f"höchstens {bis}" if von is None else f"zwischen {von} und {bis}")
        raise ValueError(f"'{feld}' muss {grenzen} sein, nicht {z}")
    return z


_ZAHL_EL = re.compile(r"-?\d+(?:[.,]\d+)?$")


def _el_text(e):
    """Element einer Menge/Relation -> Anzeigetext (Vergleich über diesen Text)."""
    if isinstance(e, bool) or isinstance(e, (list, dict)) or e is None:
        raise ValueError(f"Element {e!r}: erlaubt sind Zahlen und kurze Texte")
    if isinstance(e, int):
        return str(e)
    if isinstance(e, float):
        return repr(e).replace(".", ",")
    s = str(e).strip()
    if not s:
        raise ValueError("leeres Element")
    return s


def _el_tex(s):
    if _ZAHL_EL.match(s):
        return s.replace(".", ",").replace(",", "{,}")
    if "\\" in s or re.fullmatch(r"[A-Za-z](?:_\{?\w+\}?)?(?:\^\{?\w+\}?)?", s):
        return s
    return "\\text{" + s.replace("{", "").replace("}", "") + "}"


def _menge_tex(elemente):
    return "\\{" + ", ".join(_el_tex(e) for e in elemente) + "\\}" if elemente else "\\emptyset"


def _aufzaehlen(teile):
    teile = list(teile)
    return teile[0] if len(teile) == 1 else ", ".join(teile[:-1]) + " und " + teile[-1]


# ---- Venn-Diagramm

def _mengen_ausdruck(text, namen):
    """Mengenausdruck wie 'A ∩ B', 'A \\ B', 'Komplement A', '(A ∪ B) ∩ C' -> AST."""
    s = str(text)
    s = re.sub(r"\\overline\{([^{}]*)\}", r"~(\1)", s)
    for alt, neu in (("\\cap", "∩"), ("\\cup", "∪"), ("\\setminus", "∖"), ("\\complement", "~"), ("\\", "∖"),
                     ("&", "∩"), ("|", "∪"), ("-", "∖"), ("¬", "~"), ("{", "("), ("}", ")")):
        s = s.replace(alt, neu)
    s = re.sub(r"(?i)\bkomplement(\s+von)?\b", "~", s)
    s = re.sub(r"(?i)\bohne\b", "∖", s)
    s = re.sub(r"\^\(?c\)?", "'", s)
    toks = re.findall(r"[^\W\d]\w*|[~∩∪∖()']|\S", s)
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def nimm():
        pos[0] += 1
        return toks[pos[0] - 1]

    def vereinigung():
        a = schnitt()
        while peek() in ("∪", "∖"):
            a = (nimm(), a, schnitt())
        return a

    def schnitt():
        a = einzel()
        while peek() == "∩":
            nimm()
            a = ("∩", a, einzel())
        return a

    def einzel():
        t = nimm()
        if t == "~":
            a = ("~", einzel())
        elif t == "(":
            a = vereinigung()
            if nimm() != ")":
                raise ValueError(f"markiert: Klammer fehlt in {text!r}")
        elif t in namen:
            a = ("menge", namen.index(t))
        else:
            raise ValueError(f"markiert: {t!r} ist keine der Mengen {namen} (in {text!r})")
        while peek() == "'":
            nimm()
            a = ("~", a)
        return a

    a = vereinigung()
    if pos[0] != len(toks):
        raise ValueError(f"markiert: unerwartet {toks[pos[0]]!r} in {text!r}")
    return a


def _mengen_wert(a, maske):
    if a[0] == "menge":
        return bool(maske >> a[1] & 1)
    if a[0] == "~":
        return not _mengen_wert(a[1], maske)
    x, y = _mengen_wert(a[1], maske), _mengen_wert(a[2], maske)
    return {"∩": x and y, "∪": x or y, "∖": x and not y}[a[0]]


def _mengen_tex(a, namen, aussen=True):
    if a[0] == "menge":
        return namen[a[1]]
    if a[0] == "~":
        return "\\overline{" + _mengen_tex(a[1], namen) + "}"
    op = {"∩": "\\cap", "∪": "\\cup", "∖": "\\setminus"}[a[0]]
    s = _mengen_tex(a[1], namen, False) + f" {op} " + _mengen_tex(a[2], namen, False)
    return s if aussen else f"({s})"


def _region_tex(maske, namen):
    innen = [namen[i] for i in range(len(namen)) if maske >> i & 1]
    aussen = [namen[i] for i in range(len(namen)) if not maske >> i & 1]
    if not innen:
        return "\\overline{" + " \\cup ".join(namen) + "}"
    links = " \\cap ".join(innen)
    if not aussen:
        return links
    if len(innen) > 1:
        links = f"({links})"
    rechts = aussen[0] if len(aussen) == 1 else "(" + " \\cup ".join(aussen) + ")"
    return f"{links} \\setminus {rechts}"


def _venn(d):
    mengen = d["mengen"]
    if not 2 <= len(mengen) <= 3:
        raise ValueError("venn: 2 oder 3 Mengen angeben")
    namen, inhalte = [], []
    for m in mengen:
        if not isinstance(m, dict) or "name" not in m:
            raise ValueError('Jede Menge als {"name": "A", "elemente": [...]}')
        fremd = set(m) - {"name", "elemente"}
        if fremd:
            raise ValueError(f"Menge {m.get('name')!r}: unbekannte Felder {sorted(fremd)}")
        name = str(m["name"]).strip()
        if not name or name in namen:
            raise ValueError(f"Mengenname {name!r} leer oder doppelt")
        if not isinstance(m.get("elemente", []), list):
            raise ValueError(f"Menge {name}: 'elemente' muss eine Liste sein")
        namen.append(name)
        inhalte.append([_el_text(e) for e in m.get("elemente", [])])
    alle = []
    if "universum" in d:
        alle = [_el_text(e) for e in d["universum"]]
        for name, els in zip(namen, inhalte):
            fehlt = [e for e in els if e not in alle]
            if fehlt:
                raise ValueError(f"Menge {name}: {fehlt} fehlen im universum")
    for els in inhalte:
        alle += [e for e in els if e not in alle]
    if len(alle) != len(set(alle)):
        raise ValueError("universum enthält ein Element doppelt")
    if len(alle) > 30:
        raise ValueError("venn: höchstens 30 Elemente")

    def maske_von(e):
        return sum(1 << i for i, els in enumerate(inhalte) if e in els)

    n = len(namen)
    d["_n"], d["_namen"] = n, namen
    d["_regionen"] = []
    for m in list(range(1, 2 ** n)) + [0]:
        els = [e for e in alle if maske_von(e) == m]
        d["_regionen"].append({"maske": m, "elemente": els, "tex": _region_tex(m, namen),
                               "elemente_tex": _menge_tex(els)})
    if "markiert" in d:
        a = _mengen_ausdruck(d["markiert"], namen)
        masken = [m for m in range(2 ** n) if _mengen_wert(a, m)]
        d["_markiert"] = masken
        d["_markiert_tex"] = _mengen_tex(a, namen)
        els = [e for e in alle if maske_von(e) in masken]
        d["_markiert_elemente"] = _menge_tex(els)
        d["_markiert_unvollstaendig"] = 0 in masken and "universum" not in d


# ---- Wahrheitstabelle

def _wahrheitstabelle(d):
    variablen = [str(v) for v in d["variablen"]]
    if not 1 <= len(variablen) <= 4:
        raise ValueError("wahrheitstabelle: 1 bis 4 Variablen")
    asts = [logik_parse(a) for a in d["ausdruecke"]]
    for a, text in zip(asts, d["ausdruecke"]):
        fremd = logik_variablen(a) - set(variablen)
        if fremd:
            raise ValueError(f"{text!r} benutzt unbekannte Variable(n) {sorted(fremd)}")
    if d.get("darstellung", "wf") not in ("wf", "01"):
        raise ValueError("darstellung: 'wf' (w/f, Standard) oder '01'")
    d["_kopf"] = [logik_tex(a) for a in asts]
    d["_zeilen"] = [{"werte": list(w), "ergebnisse": [logik_wert(a, dict(zip(variablen, w))) for a in asts]}
                    for w in itertools.product([True, False], repeat=len(variablen))]
    markiert = []
    for m in d.get("markiert", []):
        if isinstance(m, int) and not isinstance(m, bool) and 0 <= m < len(asts):
            markiert.append(m)
        elif isinstance(m, str) and m in d["ausdruecke"]:
            markiert.append(d["ausdruecke"].index(m))
        else:
            raise ValueError(f"markiert: {m!r} ist kein Eintrag aus 'ausdruecke' (Text oder Index ab 0)")
    d["_markiert"] = markiert
    spalten = [[z["ergebnisse"][j] for z in d["_zeilen"]] for j in range(len(asts))]
    d["_art"] = ["tautologie" if all(s) else "kontradiktion" if not any(s) else "erfuellbar" for s in spalten]
    d["_gleich"] = [[i, j] for i in range(len(spalten)) for j in range(i + 1, len(spalten)) if spalten[i] == spalten[j]]


# ---- Relationen / Abbildungen

_EIGENSCHAFTEN = ("abbildung", "injektiv", "surjektiv", "bijektiv")


def _relation_graph(d):
    seiten = {}
    for seite in ("links", "rechts"):
        liste = [_el_text(e) for e in d[seite]]
        if not 1 <= len(liste) <= 10:
            raise ValueError(f"'{seite}': 1 bis 10 Elemente")
        if len(set(liste)) != len(liste):
            raise ValueError(f"'{seite}' enthält ein Element doppelt")
        seiten[seite] = liste
    links, rechts = seiten["links"], seiten["rechts"]
    pfeile = []
    for p in d["pfeile"]:
        if not (isinstance(p, list) and len(p) == 2):
            raise ValueError(f"Pfeil {p!r}: als [links, rechts] angeben")
        l, r = _el_text(p[0]), _el_text(p[1])
        if l not in links:
            raise ValueError(f"Pfeil {p!r}: {l!r} steht nicht in 'links'")
        if r not in rechts:
            raise ValueError(f"Pfeil {p!r}: {r!r} steht nicht in 'rechts'")
        if (l, r) in pfeile:
            raise ValueError(f"Pfeil {p!r} doppelt")
        pfeile.append((l, r))
    namen = d.get("namen", ["A", "B"])
    if len(namen) != 2 or not all(isinstance(x, str) for x in namen):
        raise ValueError('namen: zwei Texte, z. B. ["A", "B"]')
    zeige = d.get("zeige", list(_EIGENSCHAFTEN))
    if not zeige or any(z not in _EIGENSCHAFTEN for z in zeige):
        raise ValueError(f"zeige: Auswahl aus {list(_EIGENSCHAFTEN)}")
    t = {e: "$" + _el_tex(e) + "$" for e in links + rechts}
    aus = {l: [i for i, (a, _) in enumerate(pfeile) if a == l] for l in links}
    ein = {r: [i for i, (_, b) in enumerate(pfeile) if b == r] for r in rechts}
    verst = []
    for l in links:
        if not aus[l]:
            verst.append({"eigenschaft": "abbildung", "seite": "links", "element": links.index(l), "pfeile": [],
                          "text": f"{t[l]} hat keinen Pfeil."})
        elif len(aus[l]) > 1:
            ziele = _aufzaehlen(t[pfeile[i][1]] for i in aus[l])
            verst.append({"eigenschaft": "abbildung", "seite": "links", "element": links.index(l), "pfeile": aus[l],
                          "text": f"{t[l]} hat {len(aus[l])} Pfeile (zu {ziele})."})
    abb = not verst
    inj = sur = bij = None
    if abb:
        for r in rechts:
            if len(ein[r]) > 1:
                quellen = _aufzaehlen(t[pfeile[i][0]] for i in ein[r])
                verst.append({"eigenschaft": "injektiv", "seite": "rechts", "element": rechts.index(r),
                              "pfeile": ein[r], "text": f"{t[r]} wird mehrfach getroffen (von {quellen})."})
        for r in rechts:
            if not ein[r]:
                verst.append({"eigenschaft": "surjektiv", "seite": "rechts", "element": rechts.index(r),
                              "pfeile": [], "text": f"{t[r]} wird von keinem Pfeil getroffen."})
        inj = not any(v["eigenschaft"] == "injektiv" for v in verst)
        sur = not any(v["eigenschaft"] == "surjektiv" for v in verst)
        bij = inj and sur
    d["_links"] = [{"text": e, "tex": _el_tex(e)} for e in links]
    d["_rechts"] = [{"text": e, "tex": _el_tex(e)} for e in rechts]
    d["_pfeile"] = [[links.index(l), rechts.index(r)] for l, r in pfeile]
    d["_namen"] = namen
    d["_zeige"] = zeige
    d["_abbildung"], d["_injektiv"], d["_surjektiv"], d["_bijektiv"] = abb, inj, sur, bij
    d["_verstoesse"] = verst


# ---- Pascalsches Dreieck

def _pascal_tex(i, k):
    if 0 < k < i:
        a, b = math.comb(i - 1, k - 1), math.comb(i - 1, k)
        return (f"\\binom{{{i}}}{{{k}}} = \\binom{{{i - 1}}}{{{k - 1}}} + \\binom{{{i - 1}}}{{{k}}}"
                f" = {a} + {b} = {a + b}")
    return f"\\binom{{{i}}}{{{k}}} = 1"


def _pascal(d):
    n = _ganz(d.get("zeilen", 7), "zeilen", 1, 16)
    d["_zeilen"] = [[math.comb(i, k) for k in range(i + 1)] for i in range(n)]
    mark = []
    for m in d.get("markiert", []):
        if not (isinstance(m, list) and len(m) == 2):
            raise ValueError("markiert: Zellen als [n, k] (Zeile n und Stelle k, beide ab 0)")
        i, k = _ganz(m[0], "markiert n"), _ganz(m[1], "markiert k")
        if not 0 <= k <= i < n:
            raise ValueError(f"markiert: Zelle [{i}, {k}] liegt nicht im Dreieck (0 <= k <= n < {n})")
        mark.append({"n": i, "k": k, "wert": math.comb(i, k), "tex": _pascal_tex(i, k)})
    d["_markiert"] = mark


# ---- Euklidischer Algorithmus

def _lin_tex(s, x, t, y):
    return f"{s} \\cdot {x} {'+' if t >= 0 else '-'} {abs(t)} \\cdot {y}"


def _rueckwaerts(a, b, schritte):
    """Rückwärtseinsetzen: Zeilen {tex, text}; liefert (zeilen, s, t) mit ggT = s·a + t·b."""
    R = [a, b] + [s[3] for s in schritte]      # R[i] = q_i · R[i+1] + R[i+2]
    q = [s[2] for s in schritte]
    m = len(R) - 2                              # R[m] = ggT
    g = R[m]
    if m == 1:
        return [{"tex": f"{g} = 0 \\cdot {a} + 1 \\cdot {b}",
                 "text": f"${b}$ teilt ${a}$. Der ggT ist ${b}$ selbst."}], 0, 1
    zeilen = [{"tex": f"{g} = {R[m - 2]} - {q[m - 2]} \\cdot {R[m - 1]}",
               "text": f"Zeile {m - 1} nach dem ggT ${g}$ umstellen."}]
    s, t, j = 1, -q[m - 2], m - 2
    while j > 0:
        ein = f"\\hl{{({R[j - 1]} - {q[j - 1]} \\cdot {R[j]})}}"
        zeilen.append({"tex": f"{g} = {s} \\cdot {R[j]} {'+' if t >= 0 else '-'} {abs(t)} \\cdot {ein}",
                       "text": f"Zeile {j} umgestellt: ${R[j + 1]} = {R[j - 1]} - {q[j - 1]} \\cdot {R[j]}$. Einsetzen."})
        s, t = t, s - t * q[j - 1]
        zeilen.append({"tex": f"{g} = {_lin_tex(s, R[j - 1], t, R[j])}",
                       "text": f"Ausmultiplizieren und nach ${R[j - 1]}$ und ${R[j]}$ sortieren."})
        j -= 1
    if s * a + t * b != g:
        raise ValueError("Rückwärtseinsetzen ergibt keine Darstellung des ggT (interner Fehler)")
    zeilen.append({"tex": f"{_lin_tex(s, a, t, b)} = {s * a} {'+' if t * b >= 0 else '-'} {abs(t * b)} = {g}",
                   "text": "Probe: Es kommt wirklich der ggT heraus."})
    return zeilen, s, t


def _euklid(d):
    a, b = _ganz(d["a"], "a", 1, 10 ** 12), _ganz(d["b"], "b", 1, 10 ** 12)
    schritte = mathlib.euklid_schritte(a, b)
    d["_schritte"] = [list(s) for s in schritte]
    d["_ggt"] = math.gcd(a, b)
    if d.get("erweitert"):
        zeilen, s, t = _rueckwaerts(a, b, schritte)
        d["_rueckwaerts"] = zeilen
        d["_bezout"] = {"s": s, "t": t, "tex": f"{d['_ggt']} = {_lin_tex(s, a, t, b)}"}


# ---- Modulo-Uhr

def _modulo_uhr(d):
    n = _ganz(d["n"], "n", 2, 36)
    a = _ganz(d.get("start", 0), "start", -10 ** 6, 10 ** 6)
    ops = [k for k in ("plus", "mal", "potenz") if k in d]
    if len(ops) > 1:
        raise ValueError("modulo_uhr: nur eins von 'plus', 'mal', 'potenz'")
    art = ops[0] if ops else "rest"
    mod = f"\\pmod{{{n}}}"
    spruenge, potenzen = [], []
    if art == "plus":
        p = _ganz(d["plus"], "plus", -3 * n, 3 * n)
        roh = a + p
        spruenge = [[a % n, roh % n, p]]
        tex = f"{a} {'+' if p >= 0 else '-'} {abs(p)} = {roh} \\equiv {roh % n} {mod}"
    elif art == "mal":
        k = _ganz(d["mal"], "mal", 0, 24)
        if not 0 <= a < 10 ** 4:
            raise ValueError("modulo_uhr mit 'mal': start zwischen 0 und 9999")
        pos = 0
        for _ in range(k):
            spruenge.append([pos, (pos + a) % n, a])
            pos = (pos + a) % n
        roh = a * k
        tex = f"{a} \\cdot {k} = {roh} \\equiv {roh % n} {mod}"
    elif art == "potenz":
        k = _ganz(d["potenz"], "potenz", 1, 24)
        w = a % n
        potenzen = [{"exp": 1, "wert": w, "tex": f"{a}^{{1}} \\equiv {w} {mod}"}]
        for e in range(2, k + 1):
            neu = w * a % n
            spruenge.append([w, neu, e])
            potenzen.append({"exp": e, "wert": neu,
                             "tex": f"{a}^{{{e}}} \\equiv {w} \\cdot {a} = {w * a} \\equiv {neu} {mod}"})
            w = neu
        roh = None
        tex = f"{a}^{{{k}}} \\equiv {pow(a, k, n)} {mod}"
    else:
        roh = a
        tex = f"{a} \\equiv {a % n} {mod}"
    erg = pow(a, int(d["potenz"]), n) if art == "potenz" else roh % n
    d["_n"], d["_start"], d["_art"], d["_ergebnis"] = n, a, art, erg
    d["_wert"] = _ganz(d[art], art) if art != "rest" else 0
    d["_spruenge"], d["_potenzen"], d["_tex"] = spruenge, potenzen, tex
    if roh is not None:
        d["_rechnung"] = f"{roh} = {roh // n} \\cdot {n} + {roh % n}"


# ---- Induktion als Dominokette

def _induktion_domino(d):
    d["_anzahl"] = _ganz(d.get("anzahl", 8), "anzahl", 3, 12)
    d["_anfang"] = _ganz(d.get("anfang", 1), "anfang", -5, 100)


# ---- Folgen mit Grenzwert und ε-Schlauch

_FOLGE_NMAX = 10000


def _folge(d):
    hat_t, hat_r = "term" in d, "rekursion" in d
    if hat_t == hat_r:
        raise ValueError("folge: entweder 'term' (in n) oder 'start' + 'rekursion' (in a und n) angeben")
    n_von = _ganz(d.get("n_von", 1), "n_von", 0, 1000)
    n_bis = _ganz(d.get("n_bis", n_von + 19), "n_bis", n_von + 1, n_von + 200)
    if hat_t:
        t = pruefer.parse(str(d["term"]), ["n"])
        if t.variablen - {"n"}:
            raise ValueError(f"term: nur die Variable n erlaubt, nicht {sorted(t.variablen - {'n'})}")
        d["_ast"] = pruefer.ast_json(t.ast)
        d["_tex"] = "a_n = " + t.latex()

        def glieder():
            for n in range(n_von, _FOLGE_NMAX + 1):
                yield n, pruefer.wert(t.ast, {"n": F(n)})
    else:
        if "start" not in d:
            raise ValueError("folge mit 'rekursion' braucht 'start' (das ist a_{n_von})")
        r = pruefer.parse(str(d["rekursion"]), ["a", "n"])
        if r.variablen - {"a", "n"}:
            raise ValueError(f"rekursion: nur a (Vorgänger) und n erlaubt, nicht {sorted(r.variablen - {'a', 'n'})}")
        start = zahl(d["start"])
        if isinstance(start, float) and not math.isfinite(start):
            raise ValueError("start muss endlich sein")
        d["_ast_rek"] = pruefer.ast_json(r.ast)
        d["_start"] = float(start)
        mit_an = _ersetzen_var(r.ast, "a", ("var", "a_n"))
        d["_tex"] = f"a_{{{n_von}}} = {zahl_tex(d['start'])},\\quad a_{{n+1}} = " + pruefer.zu_latex(mit_an)

        def glieder():
            w = start
            for n in range(n_von, _FOLGE_NMAX + 1):
                yield n, w
                if isinstance(w, F) and (w.numerator.bit_length() > 300 or w.denominator.bit_length() > 300):
                    w = float(w)
                w = pruefer.wert(r.ast, {"a": w, "n": F(n)})
    g = eps = None
    if "grenzwert" in d:
        gt = pruefer.parse(str(d["grenzwert"]), [])
        g = pruefer.wert(gt.ast)
        d["_grenzwert"], d["_grenzwert_tex"] = float(g), gt.latex()
    if "epsilon" in d:
        if g is None:
            raise ValueError("epsilon braucht einen grenzwert")
        eps = zahl(d["epsilon"])
        if not eps > 0:
            raise ValueError("epsilon muss > 0 sein")
        d["_epsilon"], d["_epsilon_tex"] = float(eps), zahl_tex(d["epsilon"])
    werte, letzt_schlecht, bis = [], None, n_von - 1
    try:
        for n, w in glieder():
            if n <= n_bis:
                werte.append(w)
            if eps is not None:
                if isinstance(w, F) and isinstance(g, F) and isinstance(eps, F):
                    schlecht = abs(w - g) >= eps
                else:
                    schlecht = not abs(float(w) - float(g)) < float(eps)
                if schlecht:
                    letzt_schlecht = n
            elif n >= n_bis:
                break
            bis = n
    except (pruefer.Undefiniert, OverflowError, ZeroDivisionError) as e:
        if bis < n_bis:
            raise ValueError(f"a_{bis + 1} ist nicht definiert ({e})")
    d["_werte"] = [[n_von + i, float(w)] for i, w in enumerate(werte)]
    if eps is not None:
        d["_n0_bis"] = bis
        d["_n0"] = None if letzt_schlecht == bis or bis < _FOLGE_NMAX else (
            n_von if letzt_schlecht is None else letzt_schlecht + 1)
    if d.get("monotonie"):
        diffs = [werte[i + 1] - werte[i] for i in range(len(werte) - 1)]
        if all(x > 0 for x in diffs):
            d["_monotonie"] = "streng monoton steigend"
        elif all(x >= 0 for x in diffs):
            d["_monotonie"] = "monoton steigend"
        elif all(x < 0 for x in diffs):
            d["_monotonie"] = "streng monoton fallend"
        elif all(x <= 0 for x in diffs):
            d["_monotonie"] = "monoton fallend"
        else:
            d["_monotonie"] = "nicht monoton"
    if d.get("schranken"):
        lo, hi = min(werte), max(werte)
        d["_schranken"] = {"min": float(lo), "max": float(hi), "min_tex": mathlib.tex(lo), "max_tex": mathlib.tex(hi)}


def _ersetzen_var(ast, name, neu):
    if ast[0] == "var" and ast[1] == name:
        return neu
    return tuple(_ersetzen_var(k, name, neu) if isinstance(k, tuple) else k for k in ast)


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
    "venn": _venn, "relation_graph": _relation_graph, "modulo_uhr": _modulo_uhr,
    "induktion_domino": _induktion_domino, "folge": _folge,
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


def _komplexe_ebene_z(d):
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


def _komplexe_ebene(d):
    if "z" not in d and "punkte" not in d:
        raise ValueError("komplexe_ebene braucht 'z' ([Re, Im]) oder 'punkte' (Liste von Zahlen)")
    if "z" not in d and ("w" in d or "op" in d):
        raise ValueError("'w' und 'op' gehören zu 'z'")
    if "z" in d:
        _komplexe_ebene_z(d)
    _komplexe_punkte(d)


def _komplexe_punkte(d):
    """Zusätzliche Zahlen als Pfeile/Punkte: punkte[{z: [Re, Im], label?, farbe?}] oder [Re, Im]."""
    if "punkte" not in d:
        if d.get("konjugiert") or d.get("betragskreis"):
            if "z" not in d:
                raise ValueError("'konjugiert'/'betragskreis' brauchen 'z' oder 'punkte'")
        return
    roh = d["punkte"]
    if not 1 <= len(roh) <= 8:
        raise ValueError("'punkte': 1 bis 8 Zahlen")
    erg = []
    for i, p in enumerate(roh, 1):
        if isinstance(p, list):
            p = {"z": p}
        if not isinstance(p, dict) or "z" not in p or set(p) - {"z", "label", "farbe"}:
            raise ValueError(f"Punkt {i}: als [Re, Im] oder {{\"z\": [Re, Im], \"label\": …, \"farbe\": 1-4}} angeben")
        re_, im_ = _komplex_zahl(f"punkte[{i}].z", p["z"])
        farbe = p.get("farbe", (i - 1) % 4 + 1)
        if farbe not in (1, 2, 3, 4) or isinstance(farbe, bool):
            raise ValueError(f"Punkt {i}: farbe muss 1 bis 4 sein")
        label = p.get("label")
        if label is None:
            label = ("z" if len(roh) == 1 else f"z_{{{i}}}") if "z" not in d else f"u_{{{i}}}"
        if not isinstance(label, str):
            raise ValueError(f"Punkt {i}: label ist Text (LaTeX)")
        info = _komplex_info(re_, im_)
        konj = _komplex_info(re_, -im_)
        info.update(label=label, farbe=farbe, konj_tex=konj["tex"])
        erg.append(info)
    d["_punkte"] = erg
    teile = [f"{p['label']} = {p['tex']}" for p in erg]
    d["_alt"] = "Gaußsche Zahlenebene mit " + "; ".join(t.replace("\\", "") for t in teile)


_ERGAENZER.update({
    "einheitskreis": _einheitskreis, "exp_log": _exp_log, "tangente": _tangente, "riemann": _riemann,
    "vektoren2d": _vektoren2d, "komplexe_ebene": _komplexe_ebene,
})


# ──────────────────────────────────────────────────────────────────────────
#  Relationen und Ordnungen: graph_gerichtet, hasse, aequivalenz_klassen
#  Frontend: vis_ordnung.js. Python liefert Knotentexte, Positionen (Einheiten, y nach unten),
#  Kanten als Indexpaare und alle Eigenschaften exakt.
# ──────────────────────────────────────────────────────────────────────────

def _teile_oben(s):
    """Zerlegt 'a, {b, c}, d' an Kommas auf oberster Ebene."""
    teile, tiefe, akt = [], 0, ""
    for c in s:
        if c in "({[":
            tiefe += 1
        elif c in ")}]":
            tiefe -= 1
        if c == "," and tiefe == 0:
            teile.append(akt)
            akt = ""
        else:
            akt += c
    teile.append(akt)
    return [t.strip() for t in teile]


def _knoten_text(e):
    """Element (Zahl, Text, Liste = Menge) -> normierter Anzeigetext; Mengen als '{1, 2}', leere Menge als '∅'."""
    if isinstance(e, list):
        return "{" + ", ".join(_knoten_text(x) for x in e) + "}" if e else "∅"
    s = _el_text(e).replace("\\emptyset", "∅").replace("\\varnothing", "∅")
    if s.startswith("{") and s.endswith("}"):
        inner = s[1:-1].strip()
        return "{" + ", ".join(_knoten_text(t) for t in _teile_oben(inner)) + "}" if inner else "∅"
    return s


def _knoten_tex(text):
    if text == "∅":
        return "\\emptyset"
    if text.startswith("{") and text.endswith("}"):
        return "\\{" + ", ".join(_knoten_tex(t) for t in _teile_oben(text[1:-1])) + "\\}"
    return _el_tex(text)


def _elemente_lesen(d, feld="elemente", maximal=16):
    liste = d[feld]
    if not 1 <= len(liste) <= maximal:
        raise ValueError(f"'{feld}': 1 bis {maximal} Elemente")
    texte = [_knoten_text(e) for e in liste]
    if len(set(texte)) != len(texte):
        doppelt = next(t for t in texte if texte.count(t) > 1)
        raise ValueError(f"'{feld}' enthält {doppelt!r} doppelt")
    return texte


def _paare_lesen(roh, texte, feld="paare"):
    idx = {t: i for i, t in enumerate(texte)}
    paare = []
    for p in roh:
        if not (isinstance(p, list) and len(p) == 2):
            raise ValueError(f"{feld}: {p!r} ist kein Paar [a, b]")
        a, b = _knoten_text(p[0]), _knoten_text(p[1])
        for x in (a, b):
            if x not in idx:
                raise ValueError(f"{feld}: {x!r} (in {p!r}) steht nicht in 'elemente'")
        if (idx[a], idx[b]) in paare:
            raise ValueError(f"{feld}: Paar {p!r} doppelt")
        paare.append((idx[a], idx[b]))
    return paare


def _kreis_layout(n):
    if n == 1:
        return [(0.0, 0.0)]
    if n == 2:
        return [(-1.0, 0.0), (1.0, 0.0)]
    r = max(1.0, 1 / (2 * math.sin(math.pi / n)))
    return [(r * math.cos(-math.pi / 2 + 2 * math.pi * i / n), r * math.sin(-math.pi / 2 + 2 * math.pi * i / n))
            for i in range(n)]


def _graph_layout(texte, layout):
    n = len(texte)
    if layout is None or layout == "kreis":
        return _kreis_layout(n)
    if layout == "zeilen":
        spalten = max(1, math.ceil(math.sqrt(n)))
        return [(float(i % spalten), float(i // spalten)) for i in range(n)]
    if isinstance(layout, dict):
        pos = {}
        for k, v in layout.items():
            t = _knoten_text(k)
            if t not in texte:
                raise ValueError(f"layout: {k!r} steht nicht in 'elemente'")
            if isinstance(v, dict):
                v = [v.get("x"), v.get("y")]
            if not (isinstance(v, list) and len(v) == 2 and all(_ist_zahl(c) for c in v)):
                raise ValueError(f"layout: Position von {k!r} als [x, y] angeben")
            pos[t] = (float(zahl(v[0])), -float(zahl(v[1])))      # y nach oben angegeben, intern nach unten
        fehlt = [t for t in texte if t not in pos]
        if fehlt:
            raise ValueError(f"layout: Position fehlt für {', '.join(fehlt)}")
        return [pos[t] for t in texte]
    raise ValueError('layout: "kreis", "zeilen" oder {Element: [x, y], …}')


def _knoten_dicts(texte, pos, **extra):
    return [{"text": t, "tex": _knoten_tex(t), "x": round(x, 4), "y": round(y, 4), **extra}
            for t, (x, y) in zip(texte, pos)]


def _graph_gerichtet(d):
    texte = _elemente_lesen(d)
    paare = _paare_lesen(d["paare"], texte)
    pos = _graph_layout(texte, d.get("layout"))
    idx = {t: i for i, t in enumerate(texte)}
    mk_knoten, mk_kanten = [], []
    for m in d.get("markiert", []):
        if isinstance(m, list) and len(m) == 2 and _knoten_text(m[0]) in idx and _knoten_text(m[1]) in idx \
                and (idx[_knoten_text(m[0])], idx[_knoten_text(m[1])]) in paare:
            mk_kanten.append([idx[_knoten_text(m[0])], idx[_knoten_text(m[1])]])
        elif _knoten_text(m) in idx:
            mk_knoten.append(idx[_knoten_text(m)])
        else:
            raise ValueError(f"markiert: {m!r} ist weder ein Element noch ein Pfeil der Relation")
    d["_knoten"] = _knoten_dicts(texte, pos)
    d["_kanten"] = [list(p) for p in paare]
    d["_markiert_knoten"], d["_markiert_kanten"] = mk_knoten, mk_kanten
    schleifen = [texte[a] for a, b in paare if a == b]
    teile = [f"{texte[a]} nach {texte[b]}" if a != b else f"Schleife an {texte[a]}" for a, b in paare]
    d["_alt"] = (f"Gerichteter Graph mit {len(texte)} Knoten ({', '.join(texte)}) und {len(paare)} Pfeilen"
                 + (": " + "; ".join(teile) if teile else ", ohne Pfeile")
                 + (f". Schleifen an: {', '.join(schleifen)}" if schleifen else ""))


# ---- Hasse-Diagramm

def _hasse_analyse(texte, paare):
    """Ordnung (reflexiv-transitiver Abschluss), Überdeckungen (transitive Reduktion), Höhen."""
    n = len(texte)
    le = [[i == j for j in range(n)] for i in range(n)]
    for a, b in paare:
        le[a][b] = True
    for k in range(n):
        for i in range(n):
            if le[i][k]:
                for j in range(n):
                    if le[k][j]:
                        le[i][j] = True
    for i in range(n):
        for j in range(i + 1, n):
            if le[i][j] and le[j][i]:
                raise ValueError(f"Keine Halbordnung: {texte[i]} und {texte[j]} stehen in beide Richtungen "
                                 "in Relation (Antisymmetrie verletzt)")
    ueber = [(i, j) for i in range(n) for j in range(n)
             if i != j and le[i][j] and not any(k != i and k != j and le[i][k] and le[k][j] for k in range(n))]
    hoehe = [0] * n
    for _ in range(n):
        for i, j in ueber:
            hoehe[j] = max(hoehe[j], hoehe[i] + 1)
    return le, ueber, hoehe


def _hasse_ebenen(n, ueber, hoehe):
    """Reihenfolge je Schicht (Schwerpunktverfahren gegen Kreuzungen)."""
    top = max(hoehe)
    ebenen = [[i for i in range(n) if hoehe[i] == h] for h in range(top + 1)]
    unten = {j: [i for i, jj in ueber if jj == j] for j in range(n)}
    oben = {i: [j for ii, j in ueber if ii == i] for i in range(n)}

    def platz():
        return {i: p for e in ebenen for p, i in enumerate(e)}

    for _ in range(6):
        for h in range(1, top + 1):
            p = platz()
            ebenen[h].sort(key=lambda i: (sum(p[u] for u in unten[i]) / len(unten[i])) if unten[i] else p[i])
        for h in range(top - 1, -1, -1):
            p = platz()
            ebenen[h].sort(key=lambda i: (sum(p[u] for u in oben[i]) / len(oben[i])) if oben[i] else p[i])
    return ebenen


def _hasse(d):
    texte = _elemente_lesen(d, maximal=20)
    n = len(texte)
    paare = _paare_lesen(d["paare"], texte)
    le, ueber, hoehe = _hasse_analyse(texte, paare)
    ebenen = _hasse_ebenen(n, ueber, hoehe)
    top = len(ebenen) - 1
    pos = [None] * n
    for h, e in enumerate(ebenen):
        for p, i in enumerate(e):
            pos[i] = (p - (len(e) - 1) / 2, float(h))      # y nach unten: Schicht 0 (klein) ganz unten
    for i in range(n):
        pos[i] = (pos[i][0], float(top) - pos[i][1])
    idx = {t: i for i, t in enumerate(texte)}
    T = None
    if "teilmenge" in d:
        T = []
        for e in d["teilmenge"]:
            t = _knoten_text(e)
            if t not in idx:
                raise ValueError(f"teilmenge: {e!r} steht nicht in 'elemente'")
            if idx[t] not in T:
                T.append(idx[t])
    if (d.get("sup") or d.get("inf") or d.get("schranken")) and T is None:
        raise ValueError("'sup', 'inf' und 'schranken' brauchen 'teilmenge'")
    d["_knoten"] = _knoten_dicts(texte, pos)
    for i, k in enumerate(d["_knoten"]):
        k["ebene"] = hoehe[i]
    d["_kanten"] = [list(p) for p in ueber]          # [klein, groß]
    d["_ebenen"] = [list(e) for e in ebenen]
    d["_ordnung"] = [[i, j] for i in range(n) for j in range(n) if i != j and le[i][j]]
    d["_teilmenge"] = T
    info = []
    if T is not None:
        tt = "\\{" + ", ".join(_knoten_tex(texte[i]) for i in T) + "\\}" if T else "\\emptyset"
        obere = [u for u in range(n) if all(le[t][u] for t in T)]
        untere = [u for u in range(n) if all(le[u][t] for t in T)]
        sup = next((u for u in obere if all(le[u][v] for v in obere)), None)
        inf = next((u for u in untere if all(le[v][u] for v in untere)), None)
        d["_obere"], d["_untere"], d["_sup"], d["_inf"] = obere, untere, sup, inf

        def aufz(ids):
            return "$\\{" + ", ".join(_knoten_tex(texte[i]) for i in ids) + "\\}$" if ids else "keine"
        info.append(f"Teilmenge $T = {tt}$ (schwarz)")
        if d.get("schranken"):
            info.append(f"obere Schranken von $T$: {aufz(obere)}")
            info.append(f"untere Schranken von $T$: {aufz(untere)}")
        if d.get("sup"):
            if sup is not None:
                info.append(f"$\\sup T = {_knoten_tex(texte[sup])}$ (kleinste obere Schranke)")
            else:
                info.append("$T$ hat kein Supremum: " + ("es gibt keine obere Schranke." if not obere
                            else f"die oberen Schranken {aufz(obere)} haben kein kleinstes Element."))
        if d.get("inf"):
            if inf is not None:
                info.append(f"$\\inf T = {_knoten_tex(texte[inf])}$ (größte untere Schranke)")
            else:
                info.append("$T$ hat kein Infimum: " + ("es gibt keine untere Schranke." if not untere
                            else f"die unteren Schranken {aufz(untere)} haben kein größtes Element."))
    d["_info"] = info
    d["_alt"] = (f"Hasse-Diagramm mit {n} Elementen in {len(ebenen)} Schichten, kleinere Elemente unten. Linien: "
                 + (", ".join(f"{texte[i]} unter {texte[j]}" for i, j in ueber) or "keine")
                 + (f". Hervorgehoben: {', '.join(texte[i] for i in T)}" if T else "")
                 + (f". Supremum: {texte[d['_sup']]}" if d.get("sup") and d.get("_sup") is not None else "")
                 + (f". Infimum: {texte[d['_inf']]}" if d.get("inf") and d.get("_inf") is not None else ""))


# ---- Äquivalenzklassen

def _aequivalenz_klassen(d):
    roh = d["klassen"]
    if not 1 <= len(roh) <= 8 or not all(isinstance(k, list) and k for k in roh):
        raise ValueError("'klassen': 1 bis 8 nichtleere Listen")
    klassen = [[_knoten_text(e) for e in k] for k in roh]
    alle = [t for k in klassen for t in k]
    if len(alle) > 24:
        raise ValueError("höchstens 24 Elemente insgesamt")
    for t in alle:
        if alle.count(t) > 1:
            raise ValueError(f"{t!r} steht mehrfach in 'klassen' (Klassen sind disjunkt, Elemente nur einmal)")
    if "elemente" in d:
        el = [_knoten_text(e) for e in d["elemente"]]
        if set(el) != set(alle):
            fehlt = [t for t in el if t not in alle]
            extra = [t for t in alle if t not in el]
            raise ValueError("'klassen' passt nicht zu 'elemente'"
                             + (f": in keiner Klasse: {', '.join(fehlt)}" if fehlt else "")
                             + (f"; nicht in elemente: {', '.join(extra)}" if extra else ""))
    graph = bool(d.get("graph"))
    if graph and any(len(k) > 4 for k in klassen):
        raise ValueError("'graph': höchstens 4 Elemente je Klasse (sonst zu viele Pfeile)")
    reps = []
    wunsch = [_knoten_text(e) for e in d.get("repraesentanten", [])]
    for t in wunsch:
        if t not in alle:
            raise ValueError(f"repraesentanten: {t!r} steht in keiner Klasse")
    for k in klassen:
        w = [t for t in wunsch if t in k]
        if len(w) > 1:
            raise ValueError(f"repraesentanten: zwei Vertreter in einer Klasse ({', '.join(w)})")
        reps.append(w[0] if w else k[0])
    namen = d.get("namen")
    if namen is not None and (len(namen) != len(klassen) or not all(isinstance(x, str) for x in namen)):
        raise ValueError("'namen': ein Text je Klasse")
    # Layout: Klassen als Zellen eines Gitters, Elemente je Klasse auf einem kleinen Kreis
    form = []
    w = 1.45 if graph else 1.0        # mit Pfeilen mehr Platz
    for k in klassen:
        n = len(k)
        if n == 1:
            p = [(0.0, 0.0)]
        elif n == 2:
            p = [(-0.8 * w, 0.0), (0.8 * w, 0.0)]
        else:
            r = w * max(0.95, 0.55 / math.sin(math.pi / n))
            p = [(r * math.cos(-math.pi / 2 + 2 * math.pi * i / n), r * math.sin(-math.pi / 2 + 2 * math.pi * i / n))
                 for i in range(n)]
        rad = max(math.hypot(x, y) for x, y in p) + (1.25 if graph else 0.85)
        form.append((p, rad))
    anz = len(klassen)
    spalten = 1 if anz == 1 else (anz if anz <= 3 else (2 if anz == 4 else (3 if anz <= 6 else 4)))
    zelle = 2 * max(r for _, r in form) + 0.5
    knoten, kl_out, kanten = [], [], []
    for ki, (k, (p, rad)) in enumerate(zip(klassen, form)):
        cx, cy = (ki % spalten) * zelle, (ki // spalten) * zelle
        basis = len(knoten)
        for t, (x, y) in zip(k, p):
            knoten.append({"text": t, "tex": _knoten_tex(t), "x": round(cx + x, 4), "y": round(cy + y, 4),
                           "klasse": ki, "vertreter": t == reps[ki]})
        name_tex = namen[ki] if namen else "[" + _knoten_tex(reps[ki]) + "]"
        name_txt = namen[ki] if namen else "[" + reps[ki] + "]"
        kl_out.append({"name": name_txt, "name_tex": name_tex, "x": round(cx, 4), "y": round(cy, 4),
                       "r": round(rad, 4), "knoten": list(range(basis, basis + len(k))),
                       "tex": name_tex + " = \\{" + ", ".join(_knoten_tex(t) for t in k) + "\\}"})
        if graph:
            kanten += [[a, b] for a in range(basis, basis + len(k)) for b in range(basis, basis + len(k))]
    d["_knoten"], d["_klassen"], d["_kanten"] = knoten, kl_out, kanten
    d["_alt"] = (f"{len(klassen)} Äquivalenzklassen mit insgesamt {len(alle)} Elementen: "
                 + "; ".join(f"Klasse {k['name']} mit {', '.join(t)}" for k, t in zip(kl_out, klassen))
                 + (". Die Relation ist als Graph mit Pfeilen zwischen allen Elementen einer Klasse gezeigt." if graph else ""))


_ERGAENZER.update({"graph_gerichtet": _graph_gerichtet, "hasse": _hasse, "aequivalenz_klassen": _aequivalenz_klassen})
