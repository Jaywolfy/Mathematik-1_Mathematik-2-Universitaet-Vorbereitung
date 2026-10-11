# -*- coding: utf-8 -*-
"""Werkzeuge der Spielwiese: rechnen mit vollständigem Rechenweg (Markup).

Jede Funktion bekommt das JSON der Anfrage und liefert {"ergebnis": LaTeX, "rechenweg": Markup}.
"""

import math
from fractions import Fraction

from . import mathlib, pruefer

F = Fraction
tex = mathlib.tex


def _bruch(text):
    t, w = pruefer.zahl_parsen(str(text))
    if not isinstance(w, Fraction):
        raise ValueError(f"{text} ist keine rationale Zahl")
    return w


def bruch(body):
    a, b, op = _bruch(body.get("a", "")), _bruch(body.get("b", "")), body.get("op", "+")
    z = []
    if op in "+-":
        hn = mathlib.kgv(a.denominator, b.denominator)
        ea, eb = hn // a.denominator, hn // b.denominator
        erg = a + b if op == "+" else a - b
        z.append(f"\\frac{{{a.numerator}}}{{{a.denominator}}} {op} \\frac{{{b.numerator}}}{{{b.denominator}}} "
                 f"|| Aufgabe")
        z.append(f"= \\frac{{{a.numerator * ea}}}{{{hn}}} {op} \\frac{{{b.numerator * eb}}}{{{hn}}} "
                 f"|| auf den Hauptnenner {hn} erweitern (mit {ea} bzw. {eb})")
        zaehler = a.numerator * ea + (b.numerator * eb if op == "+" else -b.numerator * eb)
        z.append(f"= \\frac{{{zaehler}}}{{{hn}}} || Zähler {'addieren' if op == '+' else 'subtrahieren'}, Nenner bleibt")
    elif op in ("*", "·"):
        erg = a * b
        z.append(f"\\frac{{{a.numerator}}}{{{a.denominator}}} \\cdot \\frac{{{b.numerator}}}{{{b.denominator}}} || Aufgabe")
        z.append(f"= \\frac{{{a.numerator} \\cdot {mathlib.tex_klammer(b.numerator)}}}{{{a.denominator} \\cdot {b.denominator}}} "
                 "|| Zähler mal Zähler, Nenner mal Nenner")
        z.append(f"= \\frac{{{a.numerator * b.numerator}}}{{{a.denominator * b.denominator}}} || ausrechnen")
    elif op in ("/", ":"):
        if b == 0:
            raise ValueError("Durch 0 kann man nicht teilen.")
        erg = a / b
        z.append(f"\\frac{{{a.numerator}}}{{{a.denominator}}} : \\frac{{{b.numerator}}}{{{b.denominator}}} || Aufgabe")
        z.append(f"= \\frac{{{a.numerator}}}{{{a.denominator}}} \\cdot \\frac{{{b.denominator}}}{{{b.numerator}}} "
                 "|| mit dem Kehrwert malnehmen")
        z.append(f"= \\frac{{{a.numerator * b.denominator}}}{{{a.denominator * b.numerator}}} || ausrechnen")
    else:
        raise ValueError("Unbekannte Rechenart")
    z.append(f"= {tex(erg)} || vollständig gekürzt")
    return {"ergebnis": tex(erg), "rechenweg": ":::rechnung\n" + "\n".join(z) + "\n:::"}


def primfaktoren(body):
    n = int(_bruch(body.get("n", "")))
    if not 2 <= n <= 10 ** 12:
        raise ValueError("Bitte eine ganze Zahl zwischen 2 und 10^12.")
    z, rest, p = [], n, 2
    while rest > 1 and p * p <= rest:
        while rest % p == 0:
            z.append(f"{rest} = {p} \\cdot {rest // p} || durch {p} teilbar")
            rest //= p
        p += 1 if p == 2 else 2
    if rest > 1:
        z.append(f"{rest} = {rest} || {rest} ist eine Primzahl")
    return {"ergebnis": f"{n} = {mathlib.primfaktoren_tex(n)}",
            "rechenweg": ":::rechnung\n" + "\n".join(z) + "\n:::"}


def basis(body):
    von, nach = int(body.get("von", 10)), int(body.get("nach", 2))
    if not (2 <= von <= 36 and 2 <= nach <= 36):
        raise ValueError("Basen zwischen 2 und 36.")
    wert, summanden = mathlib.aus_basis(str(body.get("zahl", "")).strip(), von)
    zeilen = []
    if von != 10:
        terme = " + ".join(f"{w} \\cdot {von}^{{{p}}}" for w, p in summanden)
        zeilen.append(f"{wert} = {terme} || Stellenwerte zur Basis {von} aufaddieren")
    ziffern, schritte = mathlib.in_basis(wert, nach)
    for n, b, q, r in schritte:
        zeilen.append(f"{n} = {q} \\cdot {b} + {r} || Rest {r} ist die Ziffer {mathlib.ZIFFERN[r]}")
    rw = ":::rechnung\n" + "\n".join(zeilen) + "\n:::\n\nDie Reste von unten nach oben gelesen ergeben die Ziffern."
    return {"ergebnis": f"{wert}_{{10}} = \\mathtt{{{ziffern}}}_{{{nach}}}", "rechenweg": rw}


def _matrix(text):
    zeilen = [z for z in str(text).strip().splitlines() if z.strip()]
    m = [[_bruch(x) for x in pruefer.liste_zerlegen(z.replace(" ", ";") if ";" not in z and "," not in z
                                                     else z)[0] if x.strip()] for z in zeilen]
    if not m or any(len(z) != len(m[0]) for z in m):
        raise ValueError("Alle Zeilen brauchen gleich viele Einträge.")
    return m


def matrix(body):
    a, op = _matrix(body.get("a", "")), body.get("op", "det")
    if op == "det":
        d = mathlib.det(a)
        g = mathlib.gauss(a, reduziert=False)
        rw = "Zeilenstufenform per Gauß (Zeilentausch dreht das Vorzeichen):\n\n" + _gauss_markup(g, None)
        rw += f"\n\nDie Determinante ist das Produkt der Diagonale (mit Vorzeichen): $\\det A = {tex(d)}$."
        return {"ergebnis": f"\\det A = {tex(d)}", "rechenweg": rw}
    if op == "transponiert":
        t = mathlib.transponiert(a)
        return {"ergebnis": f"A^T = {mathlib.tex_matrix(t)}", "rechenweg": "Zeilen werden zu Spalten."}
    if op == "inverse":
        n = len(a)
        if any(len(z) != n for z in a):
            raise ValueError("Nur quadratische Matrizen haben eine Inverse.")
        erw = [z + e for z, e in zip(a, mathlib.einheitsmatrix(n))]
        g = mathlib.gauss(erw, reduziert=True)
        inv = mathlib.inverse(a)
        rw = "Gauß-Jordan auf $(A \\mid E)$:\n\n" + _gauss_markup(g, n)
        if inv is None:
            return {"ergebnis": "\\text{nicht invertierbar}", "rechenweg": rw + "\n\nLinks entsteht keine Einheitsmatrix: $A$ ist nicht invertierbar."}
        return {"ergebnis": f"A^{{-1}} = {mathlib.tex_matrix(inv)}", "rechenweg": rw}
    if op == "mult":
        b = _matrix(body.get("b", ""))
        c = mathlib.mat_mul(a, b)
        rw = "\n".join(f"- Zeile {i + 1} mal Spalte {j + 1}: $" + " + ".join(
            f"{mathlib.tex_klammer(a[i][k])} \\cdot {mathlib.tex_klammer(b[k][j])}" for k in range(len(b)))
            + f" = {tex(c[i][j])}$" for i in range(len(a)) for j in range(len(b[0])))
        return {"ergebnis": f"A \\cdot B = {mathlib.tex_matrix(c)}", "rechenweg": rw}
    raise ValueError("Unbekannte Operation")


def _gauss_markup(g, trenner):
    zeilen = []
    for s in g["schritte"]:
        grund = "Start" if s["op"] == "Start" else f"${s['op']}$"
        zeilen.append(f"{mathlib.tex_matrix(s['matrix'], trenner=trenner)} || {grund}")
    return ":::rechnung\n" + "\n".join(zeilen) + "\n:::"


def lgs(body):
    erw = _matrix(body.get("a", ""))
    a, b = [z[:-1] for z in erw], [z[-1] for z in erw]
    l = mathlib.lgs_loesen(a, b)
    rw = _gauss_markup(l["gauss"], len(a[0]))
    if l["art"] == "keine":
        return {"ergebnis": "\\mathbb{L} = \\emptyset", "rechenweg": rw + "\n\nEine Zeile lautet $0 = c$ mit $c \\neq 0$: keine Lösung."}
    if l["art"] == "eindeutig":
        return {"ergebnis": f"\\vec x = {mathlib.tex_vektor(l['x'])}", "rechenweg": rw}
    terme = mathlib.tex_vektor(l["x"]) + "".join(f" + {p} {mathlib.tex_vektor(r)}" for p, r in zip("tsru", l["richtungen"]))
    return {"ergebnis": f"\\vec x = {terme}", "rechenweg": rw + "\n\nFreie Variablen werden zu Parametern."}


WERKZEUGE = {"bruch": bruch, "primfaktoren": primfaktoren, "basis": basis, "matrix": matrix, "lgs": lgs}
