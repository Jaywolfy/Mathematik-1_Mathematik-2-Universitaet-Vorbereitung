# -*- coding: utf-8 -*-
"""Exakte Mathe-Helfer (nur Standardbibliothek, alles mit fractions.Fraction).

Inhalte, Generatoren, Visuals, Spielwiese und Selbsttest rechnen hiermit, damit
keine Lösung von Hand in eine Datei geschrieben werden muss.
"""

import math
import re
from fractions import Fraction

from . import pruefer

F = Fraction


# ──────────────────────────────────────────────────────────────────────────
#  Formatierung
# ──────────────────────────────────────────────────────────────────────────

def tex(x):
    """Zahl -> LaTeX (Brüche als \\frac, ganze Zahlen ohne Nenner)."""
    if isinstance(x, (int, Fraction)):
        return pruefer.fraction_latex(F(x))
    if isinstance(x, float):
        return dezimal(x)
    return str(x)


def tex_klammer(x):
    """Wie tex, negative Zahlen in Klammern (für 3 · (-2))."""
    s = tex(x)
    return f"\\left({s}\\right)" if s.startswith("-") else s


def text(x):
    if isinstance(x, (int, Fraction)):
        return pruefer.fraction_text(F(x))
    return dezimal(x)


def dezimal(x, stellen=6):
    """Kommazahl mit deutschem Komma, ohne überflüssige Nullen."""
    s = f"{float(x):.{stellen}f}".rstrip("0").rstrip(".")
    return s.replace(".", "{,}") if s != "-0" else "0"


def vorzeichen_tex(x):
    """'+ 3' / '- 3' für Rechnungen wie 2x + 3."""
    x = F(x)
    return f"- {tex(-x)}" if x < 0 else f"+ {tex(x)}"


def tex_vektor(v):
    return "\\begin{pmatrix}" + " \\\\ ".join(tex(x) for x in v) + "\\end{pmatrix}"


def tex_matrix(m, umgebung="pmatrix", trenner=None):
    """trenner = Spaltenindex für eine erweiterte Koeffizientenmatrix (A | b)."""
    if trenner is not None:
        spalten = "c" * trenner + "|" + "c" * (len(m[0]) - trenner)
        zeilen = " \\\\ ".join(" & ".join(tex(x) for x in z) for z in m)
        return f"\\left(\\begin{{array}}{{{spalten}}}{zeilen}\\end{{array}}\\right)"
    return f"\\begin{{{umgebung}}}" + " \\\\ ".join(" & ".join(tex(x) for x in z) for z in m) + f"\\end{{{umgebung}}}"


# ──────────────────────────────────────────────────────────────────────────
#  Zahlentheorie
# ──────────────────────────────────────────────────────────────────────────

def ggt(a, b):
    return math.gcd(int(a), int(b))


def kgv(a, b):
    return abs(int(a) * int(b)) // math.gcd(int(a), int(b)) if a and b else 0


def euklid_schritte(a, b):
    """Liste von (a, b, q, r) mit a = q·b + r, bis r = 0."""
    a, b = abs(int(a)), abs(int(b))
    schritte = []
    while b:
        q, r = divmod(a, b)
        schritte.append((a, b, q, r))
        a, b = b, r
    return schritte


def erweiterter_euklid(a, b):
    """(g, s, t) mit g = ggT(a, b) = s·a + t·b, dazu Tabelle [(a, b, q, s, t)]."""
    zeilen = []
    def rek(a, b):
        if b == 0:
            zeilen.append((a, b, None, 1, 0))
            return a, 1, 0
        q = a // b
        g, s1, t1 = rek(b, a % b)
        s, t = t1, s1 - q * t1
        zeilen.append((a, b, q, s, t))
        return g, s, t
    g, s, t = rek(int(a), int(b))
    zeilen.reverse()
    return g, s, t, zeilen


def primfaktoren(n):
    """{p: exponent}"""
    n = int(n)
    if n < 2:
        return {}
    erg, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            erg[p] = erg.get(p, 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        erg[n] = erg.get(n, 0) + 1
    return erg


def primfaktoren_tex(n):
    pf = primfaktoren(n)
    return " \\cdot ".join(f"{p}^{{{e}}}" if e > 1 else str(p) for p, e in pf.items())


def ist_prim(n):
    n = int(n)
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def inverse_mod(a, n):
    g, s, _, _ = erweiterter_euklid(a % n, n)
    if g != 1:
        return None
    return s % n


ZIFFERN = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def in_basis(n, basis):
    """(Ziffernfolge, Schritte [(n, basis, quotient, rest)])"""
    n, basis = int(n), int(basis)
    if n == 0:
        return "0", [(0, basis, 0, 0)]
    schritte = []
    while n:
        q, r = divmod(n, basis)
        schritte.append((n, basis, q, r))
        n = q
    return "".join(ZIFFERN[s[3]] for s in reversed(schritte)), schritte


def aus_basis(ziffern, basis):
    """(Wert, Summanden [(ziffer_wert, potenz)])"""
    ziffern = str(ziffern).strip().upper()
    summanden, wert = [], 0
    for i, z in enumerate(reversed(ziffern)):
        w = ZIFFERN.index(z)
        if w >= basis:
            raise ValueError(f"Ziffer {z} gibt es zur Basis {basis} nicht")
        summanden.append((w, i))
        wert += w * basis ** i
    return wert, list(reversed(summanden))


def binom(n, k):
    return math.comb(int(n), int(k)) if 0 <= k <= n else 0


def wurzel_vereinfachen(n):
    """√n = k·√m mit möglichst großem k. Rückgabe (k, m)."""
    n = int(n)
    k, m = 1, n
    p = 2
    while p * p <= m:
        while m % (p * p) == 0:
            m //= p * p
            k *= p
        p += 1
    return k, m


def wurzel_tex(n):
    k, m = wurzel_vereinfachen(n)
    if m == 1:
        return str(k)
    return (f"{k}\\sqrt{{{m}}}" if k > 1 else f"\\sqrt{{{m}}}")


# ──────────────────────────────────────────────────────────────────────────
#  Polynome (eine Variable, Koeffizienten als Fraction)
# ──────────────────────────────────────────────────────────────────────────

class Polynom:
    def __init__(self, koeff=None, var="x"):
        """koeff: dict {exponent: Fraction} oder Liste [a0, a1, ...]"""
        if isinstance(koeff, (list, tuple)):
            koeff = {i: F(c) for i, c in enumerate(koeff)}
        self.k = {e: F(c) for e, c in (koeff or {}).items() if c != 0}
        self.var = var

    @classmethod
    def aus_text(cls, text, var="x"):
        p = cls.aus_ast(pruefer.parse(text, [var]).ast, var)
        if p is None:
            raise ValueError("kein Polynom")
        return p

    @classmethod
    def aus_ast(cls, ast, var=None):
        """AST -> Polynom oder None (kein Polynom in EINER Variablen)."""
        vs = pruefer.variablen_von(ast)
        if len(vs) > 1:
            return None
        v = var or (next(iter(vs)) if vs else "x")
        try:
            return cls._rek(ast, v)
        except ValueError:
            return None

    @classmethod
    def _rek(cls, a, v):
        art = a[0]
        if art == "zahl":
            return cls({0: a[1]}, v)
        if art == "var":
            if a[1] != v:
                raise ValueError
            return cls({1: 1}, v)
        if art == "neg":
            return -cls._rek(a[1], v)
        if art == "add":
            return cls._rek(a[1], v) + cls._rek(a[2], v)
        if art == "sub":
            return cls._rek(a[1], v) - cls._rek(a[2], v)
        if art == "mul":
            return cls._rek(a[1], v) * cls._rek(a[2], v)
        if art == "div":
            n = cls._rek(a[2], v)
            if n.grad() != 0:
                raise ValueError
            return cls._rek(a[1], v) * cls({0: 1 / n.k.get(0, F(0))}, v) if n.k.get(0) else _fehler()
        if art == "pow":
            e = cls._rek(a[2], v)
            if e.grad() > 0:
                raise ValueError
            ex = e.k.get(0, F(0))
            if ex.denominator != 1 or ex < 0 or ex > 60:
                raise ValueError
            erg = cls({0: 1}, v)
            basis = cls._rek(a[1], v)
            for _ in range(int(ex)):
                erg = erg * basis
            return erg
        raise ValueError

    def grad(self):
        return max(self.k) if self.k else -1

    def lc(self):
        return self.k[self.grad()] if self.k else F(0)

    def __call__(self, x):
        return sum((c * F(x) ** e if not isinstance(x, float) else float(c) * x ** e)
                   for e, c in self.k.items()) if self.k else F(0)

    def __add__(self, o):
        o = o if isinstance(o, Polynom) else Polynom({0: o}, self.var)
        k = dict(self.k)
        for e, c in o.k.items():
            k[e] = k.get(e, 0) + c
        return Polynom(k, self.var)

    __radd__ = __add__

    def __neg__(self):
        return Polynom({e: -c for e, c in self.k.items()}, self.var)

    def __sub__(self, o):
        return self + (-(o if isinstance(o, Polynom) else Polynom({0: o}, self.var)))

    def __mul__(self, o):
        o = o if isinstance(o, Polynom) else Polynom({0: o}, self.var)
        k = {}
        for e1, c1 in self.k.items():
            for e2, c2 in o.k.items():
                k[e1 + e2] = k.get(e1 + e2, 0) + c1 * c2
        return Polynom(k, self.var)

    __rmul__ = __mul__

    def __eq__(self, o):
        return isinstance(o, Polynom) and self.k == o.k

    def divmod(self, d):
        """Polynomdivision: (Quotient, Rest, Schritte). Schritte für den Rechenweg."""
        if not d.k:
            raise ZeroDivisionError
        q, r, schritte = Polynom({}, self.var), Polynom(dict(self.k), self.var), []
        while r.k and r.grad() >= d.grad():
            e = r.grad() - d.grad()
            c = r.lc() / d.lc()
            t = Polynom({e: c}, self.var)
            abzug = t * d
            schritte.append({"term": t, "abzug": abzug, "rest_vorher": r})
            q = q + t
            r = r - abzug
        return q, r, schritte

    @staticmethod
    def ggt(a, b):
        while b.k:
            _, r, _ = a.divmod(b)
            a, b = b, r
        if not a.k:
            return a
        return Polynom({e: c / a.lc() for e, c in a.k.items()}, a.var)

    def _ganz(self):
        nenner = 1
        for c in self.k.values():
            nenner = nenner * c.denominator // math.gcd(nenner, c.denominator)
        return [int(c * nenner) for c in self.k.values()], nenner

    def inhalt_ggt(self, o):
        """ggT aller Koeffizienten beider Polynome (für 'gekürzt' bei (2x+2)/4)."""
        a, na = self._ganz()
        b, nb = o._ganz()
        if na != 1 or nb != 1:
            return 1
        g = 0
        for c in a + b:
            g = math.gcd(g, c)
        return g

    def ableitung(self):
        return Polynom({e - 1: c * e for e, c in self.k.items() if e > 0}, self.var)

    def rationale_nullstellen(self):
        """Alle rationalen Nullstellen (mit Vielfachheit nur einmal), sortiert."""
        if not self.k:
            return []
        ganz, _ = self._ganz()
        k = {e: c for e, c in zip(self.k.keys(), ganz)}
        erg = set()
        if 0 not in k:
            erg.add(F(0))
            m = min(k)
            k = {e - m: c for e, c in k.items()}
        a0, an = abs(k[0]), abs(k[max(k)])
        p = Polynom(k, self.var)
        for zp in _teiler(a0):
            for zq in _teiler(an):
                for s in (1, -1):
                    x = F(s * zp, zq)
                    if p(x) == 0:
                        erg.add(x)
        return sorted(erg)

    def tex(self):
        if not self.k:
            return "0"
        teile = []
        for e in sorted(self.k, reverse=True):
            c = self.k[e]
            v = self.var if e == 1 else (f"{self.var}^{{{e}}}" if e > 1 else "")
            if e and abs(c) == 1:
                koeff = ""
            else:
                koeff = tex(abs(c))
                if e and c.denominator != 1:
                    koeff = koeff
            teil = koeff + v if (koeff or v) else "1"
            if not teile:
                teile.append(("-" if c < 0 else "") + teil)
            else:
                teile.append(("- " if c < 0 else "+ ") + teil)
        return " ".join(teile)

    def text(self):
        return pruefer.zu_text(pruefer.parse(self.term()).ast)

    def term(self):
        """Term-Text für den Prüfer, z. B. '3*x^2 - 2*x + 1'."""
        if not self.k:
            return "0"
        teile = []
        for e in sorted(self.k, reverse=True):
            c = self.k[e]
            v = "" if e == 0 else (self.var if e == 1 else f"{self.var}^{e}")
            koeff = f"({text(abs(c))})" if c.denominator != 1 else str(abs(c.numerator))
            teil = (koeff + ("*" + v if v else "")) if (abs(c) != 1 or not v) else v
            teile.append((("-" if c < 0 else "") if not teile else (" - " if c < 0 else " + ")) + teil)
        return "".join(teile)

    def __repr__(self):
        return f"Polynom({self.term()})"


def _fehler():
    raise ValueError


def _teiler(n):
    n = abs(int(n))
    if n == 0:
        return [0]
    return [d for d in range(1, n + 1) if n % d == 0]


# ──────────────────────────────────────────────────────────────────────────
#  Gleichungen und Ungleichungen lösen (Polynome bis Grad 2, sonst rational)
# ──────────────────────────────────────────────────────────────────────────

def _nullstellen_exakt(p):
    """Liste von pruefer.Grenze (Wert + LaTeX), sortiert, ohne Doppelte.
       Grad 1/2 vollständig (auch irrational), höher: rationale + Rest bis Grad 2."""
    if p.grad() <= 0:
        return None if not p.k else []
    if p.grad() == 1:
        x = -p.k.get(0, F(0)) / p.k[1]
        return [pruefer.Grenze(x, tex(x))]
    if p.grad() == 2:
        a, b, c = p.k.get(2, F(0)), p.k.get(1, F(0)), p.k.get(0, F(0))
        d = b * b - 4 * a * c
        if d < 0:
            return []
        if d == 0:
            x = -b / (2 * a)
            return [pruefer.Grenze(x, tex(x))]
        try:
            w = pruefer._wurzel_exakt(d)
            xs = sorted({(-b - w) / (2 * a), (-b + w) / (2 * a)})
            return [pruefer.Grenze(x, tex(x)) for x in xs]
        except pruefer.NichtExakt:
            erg = []
            for s in (-1, 1):
                wert = (float(-b) + s * math.sqrt(float(d))) / float(2 * a)
                erg.append(pruefer.Grenze(wert, _quadrat_tex(a, b, d, s)))
            return sorted(erg, key=lambda g: g.f())
    rat = p.rationale_nullstellen()
    rest = p
    for x in rat:
        while True:
            q, r, _ = rest.divmod(Polynom({1: 1, 0: -x}, p.var))
            if r.k:
                break
            rest = q
    erg = [pruefer.Grenze(x, tex(x)) for x in rat]
    if rest.grad() <= 2 and rest.grad() >= 1:
        for g in _nullstellen_exakt(rest):
            if not any(pruefer.gleich_grenze(g, h) for h in erg):
                erg.append(g)
    elif rest.grad() > 2:
        raise ValueError("Polynom zu schwer für den exakten Löser")
    return sorted(erg, key=lambda g: g.f())


def _quadrat_tex(a, b, d, s):
    """LaTeX für (-b ± √d)/(2a), mit vereinfachter Wurzel, wenn d eine ganze Zahl ist."""
    if d.denominator != 1:
        return f"\\frac{{{tex(-b)} {'+' if s > 0 else '-'} \\sqrt{{{tex(d)}}}}}{{{tex(2 * a)}}}"
    k, m = wurzel_vereinfachen(d.numerator)
    nenner = 2 * a
    # (-b ± k√m) / nenner, gemeinsamen Faktor kürzen, wenn alles ganz ist
    if (-b).denominator == 1 and nenner.denominator == 1:
        g = math.gcd(math.gcd(int(-b), k), int(nenner))
        if nenner < 0:
            g = -g
        bb, kk, nn = F(-b) / g, F(k, g), F(nenner) / g
    else:
        bb, kk, nn = -b, F(k), nenner
    wurzel = (f"{tex(abs(kk))}\\sqrt{{{m}}}" if abs(kk) != 1 else f"\\sqrt{{{m}}}")
    zeichen = "+" if (s > 0) == (kk > 0) else "-"
    zaehler = (f"{tex(bb)} {zeichen} {wurzel}" if bb != 0 else (wurzel if zeichen == "+" else f"-{wurzel}"))
    return zaehler if nn == 1 else f"\\frac{{{zaehler}}}{{{tex(nn)}}}"


def loese(text, var="x"):
    """Löst eine Polynom-Gleichung oder -Ungleichung. Rückgabe: Liste pruefer.Intervall."""
    s = str(text).replace("≤", "<=").replace("≥", ">=")
    m = re.match(r"^(.*?)(<=|>=|<|>|=)(.*)$", s)
    if not m:
        raise ValueError("Keine (Un-)Gleichung")
    links, rel, rechts = m.group(1), m.group(2), m.group(3)
    p = Polynom.aus_ast(pruefer.parse(f"({links})-({rechts})", [var]).ast, var)
    if p is None:
        raise ValueError("Nur Polynom-Gleichungen kann ich exakt lösen")
    if not p.k:   # 0 = 0
        alle = rel in ("=", "<=", ">=")
        return [pruefer.Intervall(pruefer._MINF, False, pruefer._PINF, False)] if alle else []
    nst = _nullstellen_exakt(p)
    if rel == "=":
        return [pruefer.Intervall(g, True, g, True) for g in nst]
    # Vorzeichenanalyse zwischen den Nullstellen
    punkte = [pruefer._MINF] + nst + [pruefer._PINF]
    ok = {"<": lambda v: v < 0, ">": lambda v: v > 0, "<=": lambda v: v <= 0, ">=": lambda v: v >= 0}[rel]
    erg = []
    for lo, hi in zip(punkte, punkte[1:]):
        if math.isinf(lo.f()) and math.isinf(hi.f()):
            mitte = 0.0
        elif math.isinf(lo.f()):
            mitte = hi.f() - 1
        elif math.isinf(hi.f()):
            mitte = lo.f() + 1
        else:
            mitte = (lo.f() + hi.f()) / 2
        if ok(float(p(float(mitte)))):
            erg.append(pruefer.Intervall(lo, rel in ("<=", ">=") and not math.isinf(lo.f()),
                                         hi, rel in ("<=", ">=") and not math.isinf(hi.f())))
    if rel in ("<=", ">="):
        for g in nst:
            erg.append(pruefer.Intervall(g, True, g, True))
    return pruefer._normalisieren(erg)


# ──────────────────────────────────────────────────────────────────────────
#  Matrizen
# ──────────────────────────────────────────────────────────────────────────

def matrix(zeilen):
    return [[F(x) for x in z] for z in zeilen]


def transponiert(a):
    return [list(s) for s in zip(*a)]


def mat_mul(a, b):
    if len(a[0]) != len(b):
        raise ValueError("Spaltenzahl von A muss Zeilenzahl von B sein")
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def mat_vec(a, v):
    return [sum(F(x) * F(y) for x, y in zip(z, v)) for z in a]


def mat_add(a, b):
    return [[x + y for x, y in zip(za, zb)] for za, zb in zip(a, b)]


def skalar(c, a):
    return [[F(c) * x for x in z] for z in a]


def einheitsmatrix(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def _zeilen_name(i):
    return f"Z_{{{i + 1}}}"


def gauss(a, b=None, reduziert=True):
    """Gauß(-Jordan)-Verfahren mit Schritten.

    a: Matrix, b: rechte Seite (Vektor) oder None. Rückgabe dict:
      schritte: [{"matrix", "op" (LaTeX), "pivot": [z, s] | None, "zeilen": [geänderte Zeilen]}]
      ergebnis: Endmatrix, rang, pivots: [(z, s)]
    """
    m = [list(map(F, z)) + ([F(b[i])] if b is not None else []) for i, z in enumerate(a)]
    n_zeilen, n_spalten = len(m), len(a[0])
    schritte = [{"matrix": [z[:] for z in m], "op": "Start", "pivot": None, "zeilen": []}]
    pivots, z = [], 0
    for s in range(n_spalten):
        if z >= n_zeilen:
            break
        p = next((i for i in range(z, n_zeilen) if m[i][s] != 0), None)
        if p is None:
            continue
        if p != z:
            m[z], m[p] = m[p], m[z]
            schritte.append({"matrix": [r[:] for r in m], "op": f"{_zeilen_name(z)} \\leftrightarrow {_zeilen_name(p)}",
                             "pivot": [z, s], "zeilen": [z, p]})
        for i in range(z + 1, n_zeilen):
            if m[i][s] != 0:
                f = m[i][s] / m[z][s]
                m[i] = [x - f * y for x, y in zip(m[i], m[z])]
                schritte.append({"matrix": [r[:] for r in m],
                                 "op": f"{_zeilen_name(i)} \\leftarrow {_zeilen_name(i)} {_faktor_tex(-f)} {_zeilen_name(z)}",
                                 "pivot": [z, s], "zeilen": [i]})
        pivots.append((z, s))
        z += 1
    if reduziert:
        for z, s in reversed(pivots):
            if m[z][s] != 1:
                f = m[z][s]
                m[z] = [x / f for x in m[z]]
                schritte.append({"matrix": [r[:] for r in m],
                                 "op": f"{_zeilen_name(z)} \\leftarrow {_zeilen_name(z)} : {tex_klammer(f)}" if f.denominator == 1
                                 else f"{_zeilen_name(z)} \\leftarrow {tex_klammer(1 / f)} \\cdot {_zeilen_name(z)}",
                                 "pivot": [z, s], "zeilen": [z]})
            for i in range(z):
                if m[i][s] != 0:
                    f = m[i][s]
                    m[i] = [x - f * y for x, y in zip(m[i], m[z])]
                    schritte.append({"matrix": [r[:] for r in m],
                                     "op": f"{_zeilen_name(i)} \\leftarrow {_zeilen_name(i)} {_faktor_tex(-f)} {_zeilen_name(z)}",
                                     "pivot": [z, s], "zeilen": [i]})
    return {"schritte": schritte, "ergebnis": m, "rang": len(pivots), "pivots": pivots}


def _faktor_tex(f):
    f = F(f)
    if f == 1:
        return "+"
    if f == -1:
        return "-"
    return f"+ {tex(f)} \\cdot" if f > 0 else f"- {tex(-f)} \\cdot"


def rang(a):
    return gauss(a, reduziert=False)["rang"]


def det(a):
    a = matrix(a)
    n = len(a)
    if any(len(z) != n for z in a):
        raise ValueError("Determinante nur für quadratische Matrizen")
    m, d = [z[:] for z in a], F(1)
    for s in range(n):
        p = next((i for i in range(s, n) if m[i][s] != 0), None)
        if p is None:
            return F(0)
        if p != s:
            m[s], m[p] = m[p], m[s]
            d = -d
        d *= m[s][s]
        for i in range(s + 1, n):
            f = m[i][s] / m[s][s]
            m[i] = [x - f * y for x, y in zip(m[i], m[s])]
    return d


def inverse(a):
    """Inverse per Gauß-Jordan auf (A | E). None, wenn nicht invertierbar."""
    n = len(a)
    erw = [list(map(F, z)) + e for z, e in zip(a, einheitsmatrix(n))]
    g = gauss([z for z in erw], None, reduziert=True)
    if g["rang"] < n or any(s >= n for _, s in g["pivots"]):
        return None
    return [z[n:] for z in g["ergebnis"]]


def kern(a):
    """Basis des Kerns (Liste von Vektoren)."""
    g = gauss(a, reduziert=True)
    m, n = g["ergebnis"], len(a[0])
    pivot_spalten = [s for _, s in g["pivots"]]
    frei = [s for s in range(n) if s not in pivot_spalten]
    basis = []
    for f in frei:
        v = [F(0)] * n
        v[f] = F(1)
        for z, s in g["pivots"]:
            v[s] = -m[z][f]
        basis.append(v)
    return basis


def lgs_loesen(a, b):
    """{"art": "eindeutig"|"keine"|"unendlich", "x": partikuläre Lösung, "richtungen": [...], "gauss": ...}"""
    a, b = matrix(a), [F(x) for x in b]
    g = gauss(a, b, reduziert=True)
    m, n = g["ergebnis"], len(a[0])
    # Widerspruch: eine Zeile 0 = c mit c ≠ 0
    if any(all(x == 0 for x in z[:n]) and z[n] != 0 for z in m):
        return {"art": "keine", "x": None, "richtungen": [], "gauss": g}
    x = [F(0)] * n
    for z, s in g["pivots"]:
        x[s] = m[z][n]
    richtungen = kern(a)
    return {"art": "eindeutig" if not richtungen else "unendlich", "x": x, "richtungen": richtungen, "gauss": g}


def skalarprodukt(u, v):
    return sum(F(x) * F(y) for x, y in zip(u, v))


def kreuzprodukt(u, v):
    u, v = list(map(F, u)), list(map(F, v))
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]


def laenge_quadrat(v):
    return skalarprodukt(v, v)


def charakteristisches_polynom(a, var="λ"):
    """det(A - λE) als Polynom (über Leverrier-freie Entwicklung, exakt)."""
    n = len(a)
    a = matrix(a)
    # Matrix mit Polynom-Einträgen
    m = [[Polynom({0: a[i][j]} if i != j else {0: a[i][j], 1: -1}, "x") for j in range(n)] for i in range(n)]
    p = _det_poly(m)
    p.var = var
    return p


def _det_poly(m):
    n = len(m)
    if n == 1:
        return m[0][0]
    erg = Polynom({}, "x")
    for j in range(n):
        minor = [z[:j] + z[j + 1:] for z in m[1:]]
        t = m[0][j] * _det_poly(minor)
        erg = erg + t if j % 2 == 0 else erg - t
    return erg
