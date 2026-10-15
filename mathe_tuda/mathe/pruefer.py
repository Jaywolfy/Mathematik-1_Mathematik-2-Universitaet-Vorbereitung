# -*- coding: utf-8 -*-
"""Mathe-Prüflogik: sicherer Term-Parser, exakte Auswertung, Äquivalenz, Formchecks.

Kein eval: Eingaben werden in Tokens zerlegt und per rekursivem Abstieg in einen
AST aus Tupeln übersetzt (Whitelist). Der AST wird mit fractions.Fraction exakt
ausgewertet, wo das geht, sonst mit float.

AST-Knoten (Tupel):
    ("zahl", Fraction, text)          Zahl, text = wie eingegeben (z. B. "0,5")
    ("var", name)                     Variable (x, y, x_1, ...)
    ("konst", "pi" | "e")
    ("neg", a)  ("add", a, b)  ("sub", a, b)  ("mul", a, b, implizit)  ("div", a, b)
    ("pow", a, b)  ("fun", name, a)  ("fak", a)  ("abs", a)

Öffentliche Funktionen (Auswahl):
    parse(text, variablen=None) -> Term        Term.ast, Term.variablen, Term.klammern
    wert(ast, belegung) -> Fraction | float    (Undefiniert bei Definitionslücke)
    aequivalent(a, b, variablen) -> Vergleich
    form_pruefen(term, form) -> str | None     (Meldung, wenn die Form nicht passt)
    zu_latex(ast), zu_text(ast), ast_json(ast)
    zahl_parsen, liste_zerlegen, menge_parsen, bereich_parsen (Lösungsmengen)
    latex_zu_term(tex) (LaTeX-Teilmenge -> Term-Text), latex_pruefen(tex)
"""

import math
import random
import re
from dataclasses import dataclass, field
from fractions import Fraction

MAX_LAENGE = 400
MAX_TIEFE = 80
MAX_EXPONENT = 2000
MAX_FAKULTAET = 170
TOLERANZ = 1e-9

FUNKTIONEN = {
    "sqrt": "sqrt", "wurzel": "sqrt", "abs": "abs", "betrag": "abs",
    "sin": "sin", "cos": "cos", "tan": "tan", "ln": "ln", "lg": "log10",
    "log2": "log2", "log10": "log10", "ld": "log2", "lb": "log2", "exp": "exp",
}
KONSTANTEN = {"pi": "pi", "e": "e"}


class TermFehler(ValueError):
    """Eingabe kann nicht gelesen werden. pos = Zeichenposition (oder None)."""

    def __init__(self, meldung, pos=None):
        super().__init__(meldung)
        self.meldung = meldung
        self.pos = pos


class Undefiniert(ArithmeticError):
    """Ausdruck ist an dieser Stelle nicht definiert (z. B. Division durch 0)."""


class NichtExakt(ArithmeticError):
    """Exakte Auswertung nicht möglich (irrationaler Wert)."""


@dataclass
class Term:
    text: str
    ast: tuple
    variablen: set = field(default_factory=set)
    klammern: int = 0          # Anzahl Klammerpaare (ohne Funktionsklammern)
    implizit: bool = False      # enthält implizites Mal

    def latex(self):
        return zu_latex(self.ast)


# ──────────────────────────────────────────────────────────────────────────
#  Tokenizer
# ──────────────────────────────────────────────────────────────────────────

_ERSETZEN = [
    ("−", "-"), ("–", "-"), ("—", "-"), ("×", "*"), ("·", "*"), ("∙", "*"), ("⋅", "*"),
    ("÷", "/"), (":", "/"), ("²", "^2"), ("³", "^3"), ("⁴", "^4"), ("π", "pi"),
    ("√", " √ "), ("**", "^"), ("（", "("), ("）", ")"), ("½", "(1/2)"),
]

_TOKEN_RE = re.compile(r"""
    (?P<zahl>\d+(?:[.,]\d+)?|[.,]\d+) |
    (?P<name>[A-Za-zÄÖÜäöüß]+(?:_\{?\d+\}?|_[A-Za-z])?(?:\d+)?) |
    (?P<op>[-+*/^()\[\]|!√]) |
    (?P<raum>\s+) |
    (?P<fremd>.)
""", re.VERBOSE)


def _vorbereiten(text):
    s = str(text)
    for alt, neu in _ERSETZEN:
        s = s.replace(alt, neu)
    return s


def _namen_zerlegen(name, pos, variablen):
    """Zerlegt ein Wort in Funktion / Konstante / Variablen. Rückgabe: Liste (art, wert, pos)."""
    low = name.lower()
    if low in FUNKTIONEN:
        return [("fun", FUNKTIONEN[low], pos)]
    m = re.fullmatch(r"log_?\{?(2|10)\}?", low)
    if m:
        return [("fun", "log" + m.group(1), pos)]
    if low == "log":
        raise TermFehler("Bei „log“ fehlt die Basis. Schreibe ln (natürlich), log2 oder log10.", pos)
    if variablen and name in variablen:
        return [("var", name, pos)]
    m = re.fullmatch(r"([A-Za-z])_\{?(\d+|[A-Za-z])\}?", name)
    if m:
        return [("var", f"{m.group(1)}_{m.group(2)}", pos)]
    if low in KONSTANTEN and (not variablen or name not in variablen):
        return [("konst", KONSTANTEN[low], pos)]
    # gierig: bekannte Namen zuerst, dann einzelne Buchstaben
    teile, i = [], 0
    while i < len(name):
        rest = name[i:]
        gefunden = None
        for kandidat in sorted(set(FUNKTIONEN) | set(KONSTANTEN) | set(variablen or ()), key=len, reverse=True):
            if len(kandidat) > 1 and rest.lower().startswith(kandidat.lower()):
                gefunden = kandidat
                break
        if gefunden:
            teile.extend(_namen_zerlegen(rest[:len(gefunden)], pos + i, variablen))
            i += len(gefunden)
            continue
        c = name[i]
        if c.isdigit():
            j = i
            while j < len(name) and name[j].isdigit():
                j += 1
            teile.append(("zahl", (Fraction(int(name[i:j])), name[i:j]), pos + i))
            i = j
            continue
        if c.lower() == "e" and not (variablen and c in variablen):
            teile.append(("konst", "e", pos + i))
        elif c.isalpha() and c.isascii():
            teile.append(("var", c, pos + i))
        else:
            raise TermFehler(f"Das Zeichen „{c}“ kenne ich nicht.", pos + i)
        i += 1
    return teile


def tokens(text, variablen=None, komma_dezimal=True):
    s = _vorbereiten(text)
    if len(s) > MAX_LAENGE:
        raise TermFehler("Die Eingabe ist zu lang.")
    erg = []
    for m in _TOKEN_RE.finditer(s):
        art, wert, pos = m.lastgroup, m.group(), m.start()
        if art == "raum":
            continue
        if art == "zahl":
            if "," in wert and not komma_dezimal:
                raise TermFehler("Hier trennt das Komma Elemente. Schreibe Kommazahlen mit Punkt "
                                 "oder trenne die Elemente mit ;", pos)
            normal = wert.replace(",", ".")
            erg.append(("zahl", (Fraction(normal), wert), pos))
        elif art == "name":
            erg.extend(_namen_zerlegen(wert, pos, variablen))
        elif art == "op":
            erg.append(("op", wert, pos))
        else:
            if wert == ",":
                raise TermFehler("Ein einzelnes Komma verstehe ich hier nicht.", pos)
            if wert == "=":
                raise TermFehler("Hier ist nur ein Term gefragt, keine Gleichung. Lass „=“ weg.", pos)
            raise TermFehler(f"Das Zeichen „{wert}“ kenne ich hier nicht.", pos)
    return erg


# ──────────────────────────────────────────────────────────────────────────
#  Parser (rekursiver Abstieg)
# ──────────────────────────────────────────────────────────────────────────

class _Parser:
    def __init__(self, toks, text):
        self.t = toks
        self.i = 0
        self.text = text
        self.betrag_tiefe = 0
        self.tiefe = 0
        self.klammern = 0
        self.implizit = False

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def naechst(self):
        tok = self.peek()
        self.i += 1
        return tok

    def ist_op(self, *ops):
        tok = self.peek()
        return tok is not None and tok[0] == "op" and tok[1] in ops

    def pos(self):
        tok = self.peek()
        return tok[2] if tok else len(self.text)

    def _tiefer(self):
        self.tiefe += 1
        if self.tiefe > MAX_TIEFE:
            raise TermFehler("Der Ausdruck ist zu tief verschachtelt.")

    def ganz(self):
        if not self.t:
            raise TermFehler("Die Eingabe ist leer.", 0)
        a = self.summe()
        if self.peek() is not None:
            tok = self.peek()
            if tok[0] == "op" and tok[1] in ")]":
                raise TermFehler("Hier ist eine schließende Klammer zu viel.", tok[2])
            raise TermFehler(f"Mit „{tok[1] if tok[0] != 'zahl' else tok[1][1]}“ kann ich an dieser "
                             "Stelle nichts anfangen.", tok[2])
        return a

    def summe(self):
        self._tiefer()
        a = self.produkt()
        while self.ist_op("+", "-"):
            op = self.naechst()[1]
            b = self.produkt()
            a = ("add", a, b) if op == "+" else ("sub", a, b)
        self.tiefe -= 1
        return a

    def _beginnt_faktor(self):
        tok = self.peek()
        if tok is None:
            return False
        if tok[0] in ("zahl", "var", "konst", "fun"):
            return True
        if tok[0] == "op":
            if tok[1] in "([√":
                return True
            if tok[1] == "|" and self.betrag_tiefe == 0:
                return True
        return False

    def produkt(self):
        a = self.vorzeichen()
        while True:
            if self.ist_op("*", "/"):
                op = self.naechst()[1]
                if self.ist_op("*", "/", "^"):
                    raise TermFehler("Zwei Rechenzeichen hintereinander.", self.pos())
                b = self.vorzeichen()
                a = ("mul", a, b, False) if op == "*" else ("div", a, b)
            elif self._beginnt_faktor():
                tok = self.peek()
                vorher = self.t[self.i - 1]
                if tok[0] == "zahl" and vorher[0] == "zahl":
                    raise TermFehler("Zwei Zahlen ohne Rechenzeichen dazwischen. Meinst du ein Mal oder "
                                     "einen Bruch wie 2 1/2? Schreibe dann 2 + 1/2.", tok[2])
                if tok[0] == "zahl" and vorher[0] in ("var", "konst") or (tok[0] == "zahl" and vorher[1] == ")"):
                    # x2 oder (x+1)2 ist ungewöhnlich: als Mal lesen, aber erlaubt
                    pass
                b = self.potenz_mit_vorzeichen_verboten()
                self.implizit = True
                a = ("mul", a, b, True)
            else:
                return a

    def vorzeichen(self):
        if self.ist_op("-"):
            self.naechst()
            return ("neg", self.vorzeichen())
        if self.ist_op("+"):
            self.naechst()
            return self.vorzeichen()
        return self.potenz()

    def potenz_mit_vorzeichen_verboten(self):
        return self.potenz()

    def potenz(self):
        a = self.postfix()
        if self.ist_op("^"):
            pos = self.pos()
            self.naechst()
            if self.peek() is None:
                raise TermFehler("Nach ^ fehlt der Exponent.", pos)
            b = self.vorzeichen()   # rechtsassoziativ, 2^-1 erlaubt
            return ("pow", a, b)
        return a

    def postfix(self):
        a = self.atom()
        while self.ist_op("!"):
            self.naechst()
            a = ("fak", a)
        return a

    def atom(self):
        self._tiefer()
        tok = self.naechst()
        if tok is None:
            raise TermFehler("Der Ausdruck hört mitten drin auf. Fehlt noch eine Zahl?", len(self.text))
        art, wert, pos = tok
        if art == "zahl":
            erg = ("zahl", wert[0], wert[1])
        elif art == "var":
            erg = ("var", wert)
        elif art == "konst":
            erg = ("konst", wert)
        elif art == "fun":
            if self.ist_op("("):
                self.naechst()
                inner = self.summe()
                self._schliessen(")", pos)
            elif self._beginnt_faktor():
                inner = self.potenz()
            else:
                raise TermFehler(f"Nach {wert} fehlt das Argument, z. B. {wert}(x).", pos)
            erg = ("abs", inner) if wert == "abs" else ("fun", wert, inner)
        elif art == "op" and wert == "√":
            if self.peek() is None:
                raise TermFehler("Nach √ fehlt etwas.", pos)
            erg = ("fun", "sqrt", self.postfix())
        elif art == "op" and wert in "([":
            self.klammern += 1
            inner = self.summe()
            self._schliessen(")" if wert == "(" else "]", pos)
            erg = inner
        elif art == "op" and wert == "|":
            self.betrag_tiefe += 1
            inner = self.summe()
            self.betrag_tiefe -= 1
            if not self.ist_op("|"):
                raise TermFehler("Der Betragsstrich wird nicht geschlossen.", pos)
            self.naechst()
            erg = ("abs", inner)
        elif art == "op" and wert in ")]":
            raise TermFehler("Hier steht eine schließende Klammer, aber es fehlt etwas davor.", pos)
        else:
            raise TermFehler(f"An dieser Stelle erwarte ich eine Zahl oder Variable, nicht „{wert}“.", pos)
        self.tiefe -= 1
        return erg

    def _schliessen(self, zeichen, pos):
        if not self.ist_op(zeichen):
            if self.ist_op(")", "]"):
                raise TermFehler("Die Klammern passen nicht zusammen.", self.pos())
            raise TermFehler("Eine Klammer wird geöffnet, aber nicht geschlossen.", pos)
        self.naechst()


def parse(text, variablen=None, komma_dezimal=True):
    """Liest einen Term. variablen: erlaubte Variablennamen (für Mehrbuchstaben-Namen)."""
    text = str(text if text is not None else "").strip()
    toks = tokens(text, variablen, komma_dezimal)
    p = _Parser(toks, text)
    ast = p.ganz()
    return Term(text=text, ast=ast, variablen=variablen_von(ast), klammern=p.klammern,
                implizit=p.implizit)


def variablen_von(ast):
    if ast[0] == "var":
        return {ast[1]}
    erg = set()
    for kind in ast[1:]:
        if isinstance(kind, tuple):
            erg |= variablen_von(kind)
    return erg


def knoten_zahl(ast):
    return 1 + sum(knoten_zahl(k) for k in ast[1:] if isinstance(k, tuple))


# ──────────────────────────────────────────────────────────────────────────
#  Auswertung
# ──────────────────────────────────────────────────────────────────────────

def _ist_quadrat(n):
    if n < 0:
        return None
    r = math.isqrt(n)
    return r if r * r == n else None


def _wurzel_exakt(q, n=2):
    """n-te Wurzel einer Fraction, falls rational, sonst NichtExakt."""
    if q < 0:
        if n % 2 == 0:
            raise Undefiniert("Wurzel aus negativer Zahl")
        return -_wurzel_exakt(-q, n)
    def iroot(k):
        if k < 2:
            return k
        r = int(round(k ** (1.0 / n))) if k < 10 ** 300 else int(math.exp(math.log(k) / n))
        for c in (r - 1, r, r + 1):
            if c >= 0 and c ** n == k:
                return c
        return None
    a, b = iroot(q.numerator), iroot(q.denominator)
    if a is None or b is None:
        raise NichtExakt()
    return Fraction(a, b)


def _exakt(ast, bel):
    art = ast[0]
    if art == "zahl":
        return ast[1]
    if art == "var":
        if ast[1] not in bel:
            raise KeyError(ast[1])
        w = bel[ast[1]]
        if isinstance(w, float):
            raise NichtExakt()
        return Fraction(w)
    if art == "konst":
        raise NichtExakt()
    if art == "neg":
        return -_exakt(ast[1], bel)
    if art in ("add", "sub", "mul", "div"):
        a, b = _exakt(ast[1], bel), _exakt(ast[2], bel)
        if art == "add":
            return a + b
        if art == "sub":
            return a - b
        if art == "mul":
            return a * b
        if b == 0:
            raise Undefiniert("Division durch 0")
        return a / b
    if art == "pow":
        a, b = _exakt(ast[1], bel), _exakt(ast[2], bel)
        if b.denominator == 1:
            e = b.numerator
            if abs(e) > MAX_EXPONENT or (abs(a) > 1 and abs(e) * math.log2(max(abs(a.numerator), abs(a.denominator), 2)) > 20000):
                raise NichtExakt()
            if a == 0 and e < 0:
                raise Undefiniert("0 hoch negative Zahl")
            if a == 0 and e == 0:
                raise Undefiniert("0^0")
            return a ** e
        if a < 0:
            if b.denominator % 2 == 1:
                return _wurzel_exakt(a, b.denominator) ** b.numerator
            raise Undefiniert("gerade Wurzel aus negativer Zahl")
        if a == 0:
            if b > 0:
                return Fraction(0)
            raise Undefiniert("0 hoch negative Zahl")
        return _wurzel_exakt(a, b.denominator) ** b.numerator
    if art == "fak":
        a = _exakt(ast[1], bel)
        if a.denominator != 1 or a < 0:
            raise Undefiniert("Fakultät nur für natürliche Zahlen")
        if a > MAX_FAKULTAET:
            raise NichtExakt()
        return Fraction(math.factorial(int(a)))
    if art == "abs":
        return abs(_exakt(ast[1], bel))
    if art == "fun":
        name, a = ast[1], _exakt(ast[2], bel)
        if name == "sqrt":
            return _wurzel_exakt(a, 2)
        if name in ("sin", "tan") and a == 0:
            return Fraction(0)
        if name == "cos" and a == 0:
            return Fraction(1)
        if name == "exp" and a == 0:
            return Fraction(1)
        if name in ("ln", "log2", "log10"):
            if a <= 0:
                raise Undefiniert("Logarithmus nur für positive Zahlen")
            if a == 1:
                return Fraction(0)
            basis = {"log2": 2, "log10": 10}.get(name)
            if basis:
                for q in (a, 1 / a):
                    if q.denominator == 1:
                        n, k = q.numerator, 0
                        while n % basis == 0:
                            n //= basis
                            k += 1
                        if n == 1:
                            return Fraction(k if q is a else -k)
        raise NichtExakt()
    raise TermFehler(f"Unbekannter Knoten {art}")


def _num(ast, bel):
    art = ast[0]
    try:
        if art == "zahl":
            return float(ast[1])
        if art == "var":
            return float(bel[ast[1]])
        if art == "konst":
            return math.pi if ast[1] == "pi" else math.e
        if art == "neg":
            return -_num(ast[1], bel)
        if art in ("add", "sub", "mul", "div", "pow"):
            a, b = _num(ast[1], bel), _num(ast[2], bel)
            if art == "add":
                return a + b
            if art == "sub":
                return a - b
            if art == "mul":
                return a * b
            if art == "div":
                if b == 0:
                    raise Undefiniert("Division durch 0")
                return a / b
            if a == 0 and b <= 0:
                raise Undefiniert("0 hoch nicht-positive Zahl")
            if a < 0 and b != int(b):
                # ungerade Wurzeln negativer Zahlen (z. B. (-8)^(1/3))
                fb = Fraction(b).limit_denominator(1000)
                if fb.denominator % 2 == 1 and abs(float(fb) - b) < 1e-12:
                    return -((-a) ** b) if fb.numerator % 2 else (-a) ** b
                raise Undefiniert("Wurzel aus negativer Zahl")
            w = a ** b
            if isinstance(w, complex):
                raise Undefiniert("komplex")
            return w
        if art == "fak":
            a = _num(ast[1], bel)
            if a < 0 or a != int(a) or a > MAX_FAKULTAET:
                raise Undefiniert("Fakultät")
            return float(math.factorial(int(a)))
        if art == "abs":
            return abs(_num(ast[1], bel))
        if art == "fun":
            name, a = ast[1], _num(ast[2], bel)
            if name == "sqrt":
                if a < 0:
                    raise Undefiniert("Wurzel aus negativer Zahl")
                return math.sqrt(a)
            if name in ("ln", "log2", "log10"):
                if a <= 0:
                    raise Undefiniert("Logarithmus")
                return {"ln": math.log, "log2": math.log2, "log10": math.log10}[name](a)
            if name == "tan" and abs(math.cos(a)) < 1e-12:
                raise Undefiniert("tan")
            return {"sin": math.sin, "cos": math.cos, "tan": math.tan, "exp": math.exp}[name](a)
    except OverflowError:
        raise Undefiniert("zu groß")
    except (ValueError, ZeroDivisionError) as e:
        raise Undefiniert(str(e))
    raise TermFehler(f"Unbekannter Knoten {art}")


def wert(ast, belegung=None):
    """Exakt (Fraction), falls möglich, sonst float. Undefiniert bei Definitionslücke."""
    bel = belegung or {}
    try:
        return _exakt(ast, bel)
    except NichtExakt:
        pass
    except ZeroDivisionError:
        raise Undefiniert("Division durch 0")
    except KeyError as e:
        raise TermFehler(f"Die Variable {e.args[0]} hat keinen Wert.")
    try:
        w = _num(ast, bel)
    except KeyError as e:
        raise TermFehler(f"Die Variable {e.args[0]} hat keinen Wert.")
    if isinstance(w, float) and (math.isnan(w) or math.isinf(w)):
        raise Undefiniert("nicht endlich")
    return w


def gleich(a, b, tol=TOLERANZ):
    """Vergleicht zwei Werte (Fraction exakt, sonst relativ mit Toleranz)."""
    if isinstance(a, Fraction) and isinstance(b, Fraction):
        return a == b
    fa, fb = float(a), float(b)
    return abs(fa - fb) <= tol * max(1.0, abs(fa), abs(fb))


# ──────────────────────────────────────────────────────────────────────────
#  Äquivalenz
# ──────────────────────────────────────────────────────────────────────────

@dataclass
class Vergleich:
    ok: bool
    grund: str = ""
    stelle: dict = None
    ist: object = None
    soll: object = None
    gueltige_stellen: int = 0


def _stellen(variablen, rng, n):
    """Testbelegungen: kleine ganze Zahlen, Brüche, Kommazahlen (deterministisch)."""
    vs = sorted(variablen)
    for i in range(n):
        bel = {}
        for v in vs:
            r = rng.random()
            if i < 4:
                bel[v] = Fraction(rng.choice([-3, -2, -1, 2, 3, 4, 5]))
            elif r < 0.45:
                bel[v] = Fraction(rng.randint(-9, 9), rng.randint(2, 7))
            elif r < 0.75:
                bel[v] = Fraction(rng.randint(-12, 12))
            else:
                bel[v] = round(rng.uniform(-6, 6), 6) + 0.123456789e-3
        yield bel


def aequivalent(a, b, variablen=None, min_stellen=8, versuche=60, seed=12345):
    """Prüft, ob die ASTs a (Eingabe) und b (Lösung) dieselbe Funktion beschreiben."""
    vs = set(variablen or ()) | variablen_von(a) | variablen_von(b)
    rng = random.Random(seed)
    gueltig, nur_a, nur_b = 0, 0, 0
    for bel in _stellen(vs, rng, versuche):
        try:
            wb = wert(b, bel)
        except Undefiniert:
            wb = None
        try:
            wa = wert(a, bel)
        except Undefiniert:
            wa = None
        if wa is None and wb is None:
            continue
        if wa is None:
            nur_b += 1
            continue
        if wb is None:
            nur_a += 1
            continue
        if abs(float(wb)) > 1e12 or abs(float(wa)) > 1e12:
            continue
        if not gleich(wa, wb):
            return Vergleich(False, "ungleich", dict(bel), wa, wb, gueltig)
        gueltig += 1
        if gueltig >= max(min_stellen, 12) and not vs:
            break
        if gueltig >= 24:
            break
    if not vs and gueltig >= 1:
        return Vergleich(True, gueltige_stellen=gueltig)
    if gueltig >= min_stellen:
        if nur_b > gueltig:
            return Vergleich(False, "definitionsbereich", gueltige_stellen=gueltig)
        return Vergleich(True, gueltige_stellen=gueltig)
    if gueltig == 0 and nur_b and not nur_a:
        return Vergleich(False, "definitionsbereich", gueltige_stellen=0)
    return Vergleich(False, "zu_wenig_stellen", gueltige_stellen=gueltig)


# ──────────────────────────────────────────────────────────────────────────
#  Formchecks
# ──────────────────────────────────────────────────────────────────────────

def _ohne_neg(ast):
    while ast[0] == "neg":
        ast = ast[1]
    return ast


def _ist_summe(ast):
    return _ohne_neg(ast)[0] in ("add", "sub")


def _konstant(ast):
    return not variablen_von(ast)


def _ausmultipliziert(ast):
    art = ast[0]
    if art in ("mul",):
        if _ist_summe(ast[1]) or _ist_summe(ast[2]):
            return False
    if art == "div":
        if _ist_summe(ast[1]) and not _konstant(ast[1]):
            return False
        if not _konstant(ast[2]):
            return True   # Brüche mit Variablen im Nenner: nur Zähler prüfen
    if art == "pow" and _ist_summe(ast[1]) and not _konstant(ast[1]):
        return False
    if art == "neg" and _ist_summe(ast[1]):
        return False
    return all(_ausmultipliziert(k) for k in ast[1:] if isinstance(k, tuple))


def _faktorisiert(ast):
    a = _ohne_neg(ast)
    if a[0] in ("add", "sub"):
        return False
    if a[0] == "mul":
        return True
    if a[0] == "pow":
        return not _konstant(a[1])
    if a[0] == "div":
        return _faktorisiert(a[1]) or _konstant(a[1])
    return a[0] in ("var",)


def form_pruefen(term, form, referenz=None):
    """None, wenn die Form passt, sonst eine kurze Meldung (die Rechnung kann trotzdem stimmen)."""
    if not form:
        return None
    for f in str(form).split("|"):
        f = f.strip()
        if f == "ausmultipliziert" and not _ausmultipliziert(term.ast):
            return "Dein Term ist richtig, aber noch nicht ausmultipliziert. Löse alle Klammern auf."
        if f == "faktorisiert" and not _faktorisiert(term.ast):
            return ("Dein Term ist richtig, aber noch keine Produktform. Gesucht ist ein Produkt, "
                    "z. B. 3(x + 2) oder (x - 1)(x + 1).")
        if f == "ohne_klammern" and term.klammern:
            return "Dein Term ist richtig, soll aber ohne Klammern geschrieben werden."
        if f in ("gekuerzt", "vereinfacht"):
            meldung = _gekuerzt_meldung(term.ast)
            if meldung:
                return meldung
        if f == "ggt_ausgeklammert":
            meldung = _ggt_meldung(term.ast)
            if meldung:
                return meldung
        if f == "linearfaktoren":
            meldung = _linearfaktoren_meldung(term.ast)
            if meldung:
                return meldung
        if f in ("wurzel_vereinfacht", "vereinfacht"):
            meldung = _wurzel_meldung(term.ast)
            if meldung:
                return meldung
        if f in ("potenz", "vereinfacht"):
            meldung = _potenz_meldung(term.ast)
            if meldung:
                return meldung
        if f == "vereinfacht":
            meldung = _zahlen_meldung(term.ast)
            if not meldung and referenz is not None and _nur_zahlen(term.ast) and _einfache_zahl(referenz) \
                    and not _einfache_zahl(term.ast):
                meldung = "Richtig, aber rechne das noch zu einer Zahl aus."
            if meldung:
                return meldung
        if f == "vereinfacht" and referenz is not None and knoten_zahl(term.ast) > knoten_zahl(referenz) + 2:
            return "Dein Term ist richtig, lässt sich aber noch weiter vereinfachen."
    return None


def _linearfaktoren_meldung(ast):
    """Formcheck 'linearfaktoren': Produkt, dessen Faktoren über Q nicht weiter zerfallen."""
    from . import mathlib
    if not _faktorisiert(ast) and _ohne_neg(ast)[0] not in ("var",):
        return ("Dein Term ist richtig, aber noch keine Produktform. Gesucht ist ein Produkt aus "
                "Linearfaktoren wie (x - 1)(x + 2).")
    for f, _ in _faktoren(_ohne_neg(ast)):
        f = _ohne_neg(f)
        if f[0] == "pow":
            f = f[1]
        try:
            pol = mathlib.Polynom.aus_ast(f)
        except ValueError:
            continue
        if pol is not None and pol.grad() >= 2 and pol.rationale_nullstellen():
            return "Richtig, aber ein Faktor lässt sich noch weiter zerlegen. Suche seine Nullstellen."
    return None


def _ggt_meldung(ast):
    """Formcheck 'ggt_ausgeklammert': Zahl (und Potenz der Variablen) mal Klammer, in der kein
    gemeinsamer Faktor mehr steckt (ganzzahlige Koeffizienten mit ggT 1, kein gemeinsames x)."""
    from . import mathlib
    if _ist_summe(ast):
        return "Dein Term ist richtig, aber noch keine Produktform. Klammere den größten gemeinsamen Faktor aus."
    summen = [f for f, e in _faktoren(_ohne_neg(ast)) if _ist_summe(f)]
    if len(summen) != 1:
        return "Dein Term ist richtig, aber klammere den größten gemeinsamen Faktor aus: Zahl mal Klammer."
    try:
        pol = mathlib.Polynom.aus_ast(_ohne_neg(summen[0]))
    except ValueError:
        return None
    if pol is None:
        return None
    koeff = {e: c for e, c in pol.k.items() if c != 0}
    if any(Fraction(c).denominator != 1 for c in koeff.values()):
        return "Richtig, aber in der Klammer sollen ganze Zahlen stehen. Klammere eine ganze Zahl aus."
    g = 0
    for c in koeff.values():
        g = math.gcd(g, int(c))
    if g > 1:
        return f"Richtig, aber in der Klammer steckt noch der gemeinsame Faktor {g}. Klammere ihn mit aus."
    if koeff and min(koeff) > 0:
        return "Richtig, aber jeder Summand in der Klammer enthält noch die Variable. Klammere sie mit aus."
    return None


def _knoten(ast):
    yield ast
    for k in ast[1:]:
        if isinstance(k, tuple):
            yield from _knoten(k)


def _ist_wurzel(ast):
    a = _ohne_neg(ast)
    return (a[0] == "fun" and a[1] == "sqrt") or (
        a[0] == "pow" and a[2][0] == "zahl" and a[2][1].denominator != 1)


def _wurzel_meldung(ast):
    """Formcheck 'wurzel_vereinfacht': kein Quadratfaktor > 1 unter einer Quadratwurzel, keine
    ganz ausrechenbare Wurzel, keine Wurzel im Nenner."""
    for k in _knoten(ast):
        if k[0] == "fun" and k[1] == "sqrt" and k[2][0] == "zahl" and k[2][1].denominator == 1:
            n = k[2][1].numerator
            if n > 1:
                r = math.isqrt(n)
                if r * r == n:
                    return f"Richtig, aber $\\sqrt{{{n}}} = {r}$ lässt sich ganz ausrechnen."
                q = max(d for d in range(1, r + 1) if n % (d * d) == 0)
                if q > 1:
                    return (f"Richtig, aber unter der Wurzel steckt noch der Quadratfaktor ${q * q}$. "
                            f"Ziehe ihn heraus: $\\sqrt{{{n}}} = {q}\\sqrt{{{n // (q * q)}}}$.")
        if k[0] == "div" and any(_ist_wurzel(x) for x in _knoten(k[2])):
            return "Richtig, aber im Nenner steht noch eine Wurzel. Mach den Nenner rational."
    return None


def _faktoren(ast, exp=1):
    """Zerlegt Produkte und Quotienten in (faktor, +1|-1)."""
    a = ast
    if a[0] == "mul":
        return _faktoren(a[1], exp) + _faktoren(a[2], exp)
    if a[0] == "div":
        return _faktoren(a[1], exp) + _faktoren(a[2], -exp)
    return [(a, exp)]


def _potenz_meldung(ast):
    """Formcheck 'potenz': in jedem Produkt jede Basis höchstens einmal, keine Potenz einer Potenz."""
    for k in _knoten(ast):
        if k[0] == "pow" and _ohne_neg(k[1])[0] == "pow":
            return "Richtig, aber da steht noch eine Potenz einer Potenz. Multipliziere die Exponenten."
        if k[0] in ("mul", "div"):
            basen = []
            for f, _ in _faktoren(k):
                f = _ohne_neg(f)
                b = f[1] if f[0] == "pow" else f
                if b[0] in ("var", "konst"):
                    if b in basen:
                        return ("Richtig, aber die Basis " + (b[1] if b[0] == "var" else "e")
                                + " kommt noch mehrfach vor. Fasse die Potenzen zusammen.")
                    basen.append(b)
    return None


def _nur_zahlen(ast):
    return all(k[0] in ("zahl", "neg", "add", "sub", "mul", "div", "pow") for k in _knoten(ast))


def ausgerechnet_meldung(text):
    """Für Rechenfragen: Eingabe besteht nur aus Zahlen, ist aber noch kein einzelner Wert (z. B. 3,45*100)."""
    try:
        t = parse(text)
    except TermFehler:
        return None
    if _nur_zahlen(t.ast) and not _einfache_zahl(t.ast):
        return "Der Wert stimmt, aber rechne ihn noch ganz aus und gib eine einzelne Zahl an."
    return None


def _einfache_zahl(ast):
    a = _ohne_neg(ast)
    return a[0] == "zahl" or (a[0] == "div" and _ohne_neg(a[1])[0] == "zahl" and a[2][0] == "zahl")


def _zahlen_meldung(ast):
    """Teil von 'vereinfacht': mehrere reine Zahlfaktoren in einem Produkt zusammenrechnen."""
    for k in _knoten(ast):
        if k[0] == "div" and k[1][0] == "zahl" and k[2][0] == "zahl" and k is not ast:
            p_, q_ = k[1][1], k[2][1]
            if p_.denominator == q_.denominator == 1 and (q_ == 1 or math.gcd(p_.numerator, q_.numerator) > 1):
                return "Richtig, aber ein Zahlbruch lässt sich noch kürzen oder ausrechnen."
        if k[0] == "mul":
            zahlen = [f for f, e in _faktoren(k) if e == 1 and _ohne_neg(f)[0] == "zahl"]
            if len(zahlen) > 1:
                return "Richtig, aber die Zahlen im Produkt lassen sich noch zusammenrechnen."
        if k[0] in ("add", "sub", "mul", "pow") and _nur_zahlen(k) and k is not ast:
            return "Richtig, aber ein Teil besteht nur aus Zahlen. Rechne ihn aus."
    return None


def _gekuerzt_meldung(ast):
    from . import mathlib
    a = _ohne_neg(ast)
    if a[0] == "div" and a[1][0] == "zahl" and a[2][0] == "zahl":
        p, q = a[1][1], a[2][1]
        if p.denominator == 1 and q.denominator == 1 and math.gcd(p.numerator, q.numerator) > 1:
            g = math.gcd(p.numerator, q.numerator)
            return (f"Richtig gerechnet, aber noch nicht vollständig gekürzt: Zähler und Nenner "
                    f"lassen sich beide durch {g} teilen.")
        return None
    if a[0] == "div":
        try:
            pz, pn = mathlib.Polynom.aus_ast(a[1]), mathlib.Polynom.aus_ast(a[2])
        except ValueError:
            return None
        if pz is None or pn is None:
            return None
        if pn.grad() < 1:
            if pz.grad() >= 1 and pz.inhalt_ggt(pn) > 1:
                return "Richtig gerechnet, aber Zähler und Nenner lassen sich noch durch dieselbe Zahl kürzen."
            return None
        g = mathlib.Polynom.ggt(pz, pn)
        if g.grad() >= 1:
            return "Richtig gerechnet, aber Zähler und Nenner haben noch einen gemeinsamen Faktor. Kürze ihn."
        if pz.inhalt_ggt(pn) > 1:
            return "Richtig gerechnet, aber noch nicht vollständig gekürzt."
    return None


def bruch_gekuerzt(text):
    """Prüft eine Zahleingabe wie '6/8' so, wie sie dasteht. None = ok, sonst Meldung."""
    try:
        t = parse(text)
    except TermFehler:
        return None
    return _gekuerzt_meldung(t.ast)


# ──────────────────────────────────────────────────────────────────────────
#  Ausgabe: LaTeX, Text, JSON
# ──────────────────────────────────────────────────────────────────────────

_PRIO = {"add": 1, "sub": 1, "mul": 2, "div": 2, "neg": 3, "pow": 4, "fak": 5,
         "zahl": 6, "var": 6, "konst": 6, "fun": 6, "abs": 6}


def _prio(ast):
    if ast[0] == "zahl" and (ast[1] < 0 or ast[1].denominator != 1 and not ("." in ast[2] or "," in ast[2])):
        return 2 if ast[1] >= 0 else 3
    return _PRIO[ast[0]]


def fraction_latex(q):
    q = Fraction(q)
    if q.denominator == 1:
        return str(q.numerator)
    s = "-" if q < 0 else ""
    return f"{s}\\frac{{{abs(q.numerator)}}}{{{q.denominator}}}"


def fraction_text(q):
    q = Fraction(q)
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


_UMGRUPPIEREN = __import__("threading").local()
_UMGRUPPIEREN.an = False


def aufgabe_latex(ast):
    """LaTeX für Aufgabentexte: (X·a)/b wird als X · a/b gesetzt (so liest man "2/3 * 3/4").
    Die Vorschau einer Eingabe nutzt dagegen zu_latex und zeigt die Struktur genau so, wie getippt."""
    _UMGRUPPIEREN.an = True
    try:
        return zu_latex(ast)
    finally:
        _UMGRUPPIEREN.an = False


_FUN_LATEX = {"sin": "\\sin", "cos": "\\cos", "tan": "\\tan", "ln": "\\ln", "log2": "\\log_2",
              "log10": "\\log_{10}", "exp": "\\exp"}


def zu_latex(ast):
    art = ast[0]

    def kl(kind, min_prio, rechts=False):
        s = zu_latex(kind)
        p = _prio(kind)
        if p < min_prio or (rechts and p == min_prio and art in ("sub", "div")):
            return f"\\left({s}\\right)"
        return s

    if art == "zahl":
        txt = ast[2]
        if txt and re.fullmatch(r"\d+([.,]\d+)?", txt):
            return txt.replace(",", "{,}").replace(".", "{,}") if ("," in txt or "." in txt) else txt
        return fraction_latex(ast[1])
    if art == "var":
        n = ast[1]
        m = re.fullmatch(r"([A-Za-z])_(\w+)", n)
        return f"{m.group(1)}_{{{m.group(2)}}}" if m else n
    if art == "konst":
        return "\\pi" if ast[1] == "pi" else "\\mathrm{e}"
    if art == "neg":
        inner = ast[1]
        s = zu_latex(inner)
        return f"-\\left({s}\\right)" if _prio(inner) <= 2 and inner[0] in ("add", "sub") else f"-{s}"
    if art == "add":
        rechts = ast[2]
        if rechts[0] == "neg":
            return f"{kl(ast[1], 1)} + \\left({zu_latex(rechts)}\\right)"
        return f"{kl(ast[1], 1)} + {kl(rechts, 1)}"
    if art == "sub":
        return f"{kl(ast[1], 1)} - {kl(ast[2], 2)}" if ast[2][0] != "neg" else \
            f"{kl(ast[1], 1)} - \\left({zu_latex(ast[2])}\\right)"
    if art == "mul":
        a, b = kl(ast[1], 2), kl(ast[2], 2, rechts=True)
        if ast[2][0] == "neg":
            b = f"\\left({zu_latex(ast[2])}\\right)"
        if ast[1][0] == "neg" and not ast[3]:
            a = f"\\left({zu_latex(ast[1])}\\right)"
        if ast[3] and not (ast[2][0] == "zahl"):
            return f"{a} {b}" if not (a[-1:].isdigit() and b[:1].isdigit()) else f"{a} \\cdot {b}"
        return f"{a} \\cdot {b}"
    if art == "div":
        z, n = ast[1], ast[2]
        # (X · a) / b  ->  X · a/b   (so wie man "2/3 * 3/4" meint und liest)
        if getattr(_UMGRUPPIEREN, "an", False) and z[0] == "mul" and z[2][0] == "zahl" and n[0] == "zahl" \
                and z[2][1].denominator == 1 and n[1].denominator == 1 and not z[3]:
            return zu_latex(("mul", z[1], ("div", z[2], n), False))
        return f"\\frac{{{zu_latex(z)}}}{{{zu_latex(n)}}}"
    if art == "pow":
        basis = ast[1]
        b = zu_latex(basis)
        if _prio(basis) <= 4 or basis[0] in ("fun",) or (basis[0] == "zahl" and _prio(basis) < 6):
            b = f"\\left({b}\\right)"
        return f"{b}^{{{zu_latex(ast[2])}}}"
    if art == "fak":
        inner = ast[1]
        s = zu_latex(inner)
        return f"\\left({s}\\right)!" if _prio(inner) < 6 else f"{s}!"
    if art == "abs":
        return f"\\left|{zu_latex(ast[1])}\\right|"
    if art == "fun":
        if ast[1] == "sqrt":
            return f"\\sqrt{{{zu_latex(ast[2])}}}"
        return f"{_FUN_LATEX[ast[1]]}\\left({zu_latex(ast[2])}\\right)"
    raise TermFehler(f"Unbekannter Knoten {art}")


def zu_text(ast):
    art = ast[0]

    def kl(kind, min_prio, rechts=False):
        s = zu_text(kind)
        p = _prio(kind)
        if p < min_prio or (rechts and p == min_prio and art in ("sub", "div")):
            return f"({s})"
        return s

    if art == "zahl":
        return ast[2] if ast[2] else fraction_text(ast[1])
    if art == "var":
        return ast[1]
    if art == "konst":
        return "π" if ast[1] == "pi" else "e"
    if art == "neg":
        return f"-({zu_text(ast[1])})" if ast[1][0] in ("add", "sub") else f"-{zu_text(ast[1])}"
    if art == "add":
        return f"{kl(ast[1], 1)} + {kl(ast[2], 1) if ast[2][0] != 'neg' else '(' + zu_text(ast[2]) + ')'}"
    if art == "sub":
        return f"{kl(ast[1], 1)} - {kl(ast[2], 2) if ast[2][0] != 'neg' else '(' + zu_text(ast[2]) + ')'}"
    if art == "mul":
        a, b = kl(ast[1], 2), kl(ast[2], 2, rechts=True)
        if ast[2][0] == "neg":
            b = f"({zu_text(ast[2])})"
        return f"{a}{b}" if ast[3] and ast[2][0] != "zahl" else f"{a} · {b}"
    if art == "div":
        return f"{kl(ast[1], 3)}/{kl(ast[2], 3)}"
    if art == "pow":
        b = zu_text(ast[1])
        if _prio(ast[1]) <= 4 or ast[1][0] == "fun":
            b = f"({b})"
        e = zu_text(ast[2])
        if e in ("2", "3"):
            return b + {"2": "²", "3": "³"}[e]
        return f"{b}^{e}" if _prio(ast[2]) >= 6 else f"{b}^({e})"
    if art == "fak":
        return f"({zu_text(ast[1])})!" if _prio(ast[1]) < 6 else f"{zu_text(ast[1])}!"
    if art == "abs":
        return f"|{zu_text(ast[1])}|"
    if art == "fun":
        if ast[1] == "sqrt":
            return f"√({zu_text(ast[2])})"
        return f"{ast[1]}({zu_text(ast[2])})"
    raise TermFehler(art)


def ast_json(ast):
    """AST für den JS-Auswerter (Zahlen als float)."""
    art = ast[0]
    if art == "zahl":
        return ["zahl", float(ast[1])]
    if art in ("var", "konst"):
        return [art, ast[1]]
    if art == "fun":
        return ["fun", ast[1], ast_json(ast[2])]
    if art == "mul":
        return ["mul", ast_json(ast[1]), ast_json(ast[2])]
    return [art] + [ast_json(k) for k in ast[1:]]


# ──────────────────────────────────────────────────────────────────────────
#  Zahl, Liste, Menge, Lösungsmenge
# ──────────────────────────────────────────────────────────────────────────

def zahl_parsen(text, komma_dezimal=True):
    """(Term, Wert) für eine Eingabe ohne Variablen."""
    t = parse(text, komma_dezimal=komma_dezimal)
    if t.variablen:
        v = ", ".join(sorted(t.variablen))
        raise TermFehler(f"Hier ist eine Zahl gefragt, aber in deiner Eingabe steht die Variable {v}.")
    return t, wert(t.ast)


def liste_zerlegen(text):
    """Zerlegt 'a; b; c' oder 'a, b, c' auf oberster Ebene.
       Rückgabe: (teile, komma_dezimal). ';' vorhanden -> ';' trennt, ',' ist Dezimalkomma."""
    s = str(text)
    trenner = ";" if ";" in s else ","
    teile, tiefe, aktuell = [], 0, ""
    for c in s:
        if c in "([{":
            tiefe += 1
        elif c in ")]}":
            tiefe -= 1
        if c == trenner and tiefe == 0:
            teile.append(aktuell)
            aktuell = ""
        else:
            aktuell += c
    teile.append(aktuell)
    erg = []
    for t in teile:
        erg.extend(_plusminus_aufspalten(t.strip()))
    return erg, trenner == ";"


def _plusminus_aufspalten(t):
    """'±5' -> ['5', '-5'];  '2 ± sqrt(10)' -> ['2 + sqrt(10)', '2 - sqrt(10)'];  'x = ±1' -> ['x = 1', 'x = -1']."""
    t = t.replace("+/-", "±").replace("+-", "±")
    i = t.find("±")
    if i < 0:
        return [t]
    vorne = t[:i].rstrip()
    if not vorne or vorne.endswith(("=", "{", "(")):
        plus, minus = t[:i] + t[i + 1:], t[:i] + "-" + t[i + 1:]
    else:
        plus, minus = t[:i] + "+" + t[i + 1:], t[:i] + "-" + t[i + 1:]
    return _plusminus_aufspalten(plus) + _plusminus_aufspalten(minus)


_LEER = {"", "{}", "∅", "ø", "leer", "leeremenge", "keine", "keinelösung", "keineloesung",
         "nichts", "{ }", "l={}", "l=∅"}


def _ist_leer(text):
    s = re.sub(r"\s+", "", str(text).lower())
    s = re.sub(r"^[lm]=", "", s)
    return s in _LEER or s in ("{}", "∅")


def _ohne_praefix(s):
    return re.sub(r"^\s*[A-ZLM](_\w+)?\s*=\s*(?=\{)", "", str(s).strip())


def _element_wert(text, komma_dezimal, e_symbol=False):
    text = text.strip()
    if not text:
        raise TermFehler("Ein Element ist leer (zwei Trennzeichen hintereinander?).")
    if text.startswith("{") and text.endswith("}"):
        return ("menge", menge_parsen(text, e_symbol=e_symbol))
    if text.startswith("(") and text.endswith(")") and ("," in text[1:-1] or ";" in text[1:-1]):
        teile, kd = liste_zerlegen(text[1:-1])
        return ("tupel", tuple(_element_wert(t, kd, e_symbol) for t in teile))
    if text == "E" or (text == "e" and e_symbol):
        return ("symbol", text)   # ein einzelnes E ist nie die Euler-Zahl; e nur, wenn der Aufrufer es als Symbol verlangt
    try:
        t = parse(text, komma_dezimal=komma_dezimal)
    except TermFehler:
        if re.fullmatch(r"[\wäöüÄÖÜß]+", text):
            return ("symbol", text)
        raise
    if t.variablen:
        if re.fullmatch(r"[A-Za-z]\w*", text):
            return ("symbol", text)
        return ("term", zu_text(t.ast))
    w = wert(t.ast)
    return ("zahl", w)


def _element_schluessel(e):
    art, w = e
    if art == "zahl":
        return ("zahl", w if isinstance(w, Fraction) else round(float(w), 9))
    if art == "tupel":
        return ("tupel", tuple(_element_schluessel(x) for x in w))
    if art == "menge":
        return ("menge", frozenset(_element_schluessel(x) for x in w))
    return (art, w)


def _symbole(elemente):
    """Alle Symbolnamen (rekursiv durch Mengen und Tupel)."""
    erg = set()
    for art, w in elemente:
        if art == "symbol":
            erg.add(w)
        elif art in ("menge", "tupel"):
            erg |= _symbole(w)
    return erg


def e_ist_symbol(elemente):
    """Kommt in dieser (mit e_symbol=True gelesenen) Menge ein Symbol e vor?"""
    return "e" in _symbole(elemente)


def menge_parsen(text, e_symbol=None):
    """Menge wie '{1; 2; 3}' oder '{a, b}' -> Liste von Elementen (art, wert).

    Elementname `e`: True = Buchstabe (Symbol), False = Euler-Zahl, None = automatisch: Buchstabe,
    wenn neben ihm ein anderes Symbol vorkommt ({a, b, e}), sonst Euler-Zahl ({e, 1})."""
    if e_symbol is None:
        erg = menge_parsen(text, True)
        if e_ist_symbol(erg) and _symbole(erg) - {"e"}:
            return erg
        return menge_parsen(text, False)
    s = _ohne_praefix(text)
    if _ist_leer(s):
        return []
    s = s.strip()
    # leere Menge als Element: {∅; {1}} wie {{}; {1}}
    s = re.sub(r"\\(?:emptyset|varnothing)|∅|ø", "{}", s)
    if s.startswith("{") and s.endswith("}"):
        s = s[1:-1]
    if not s.strip():
        return []
    teile, kd = liste_zerlegen(s)
    return [_element_wert(t, kd, e_symbol) for t in teile]


def menge_schluessel(elemente):
    return frozenset(_element_schluessel(e) for e in elemente)


def element_latex(e):
    art, w = e
    if art == "zahl":
        return fraction_latex(w) if isinstance(w, Fraction) else f"{float(w):.6g}"
    if art == "tupel":
        return "(" + ", ".join(element_latex(x) for x in w) + ")"
    if art == "menge":
        return "\\{" + ", ".join(element_latex(x) for x in w) + "\\}" if w else "\\emptyset"
    if art == "symbol":
        return w if len(w) == 1 else f"\\text{{{w}}}"
    return w


def menge_latex(elemente):
    if not elemente:
        return "\\emptyset"
    return "\\{" + "; ".join(element_latex(e) for e in elemente) + "\\}"


# Lösungsmengen als Liste von Intervallen ------------------------------------

INF = float("inf")


@dataclass(frozen=True)
class Grenze:
    wert: object          # Fraction | float | ±inf
    latex: str

    def f(self):
        return float(self.wert)


@dataclass
class Intervall:
    lo: Grenze
    lo_zu: bool           # geschlossen?
    hi: Grenze
    hi_zu: bool

    def punkt(self):
        return self.lo_zu and self.hi_zu and gleich_grenze(self.lo, self.hi)


def gleich_grenze(a, b):
    if math.isinf(a.f()) or math.isinf(b.f()):
        return a.f() == b.f()
    return gleich(a.wert, b.wert)


_MINF = Grenze(-INF, "-\\infty")
_PINF = Grenze(INF, "\\infty")


def _grenze(text, komma_dezimal):
    s = text.strip().replace(" ", "")
    if s in ("∞", "+∞", "inf", "+inf", "unendlich", "oo"):
        return _PINF
    if s in ("-∞", "−∞", "-inf", "-unendlich", "-oo"):
        return _MINF
    t, w = zahl_parsen(s, komma_dezimal)
    return Grenze(w, zu_latex(t.ast))


def _normalisieren(intervalle):
    iv = [i for i in intervalle if i.lo.f() < i.hi.f() or i.punkt()]
    iv.sort(key=lambda i: (i.lo.f(), not i.lo_zu))
    erg = []
    for i in iv:
        if erg:
            last = erg[-1]
            beruehrt = last.hi.f() > i.lo.f() or (gleich_grenze(last.hi, i.lo) and (last.hi_zu or i.lo_zu))
            if beruehrt:
                if i.hi.f() > last.hi.f() or (gleich_grenze(i.hi, last.hi) and i.hi_zu):
                    last.hi, last.hi_zu = i.hi, i.hi_zu if not gleich_grenze(i.hi, last.hi) else (i.hi_zu or last.hi_zu)
                continue
        erg.append(Intervall(i.lo, i.lo_zu, i.hi, i.hi_zu))
    return erg


_REL = {"<": ("lt"), "<=": "le", "≤": "le", ">": "gt", ">=": "ge", "≥": "ge", "=<": "le", "=>": "ge"}


def _ungleichung(teil, variable, kd):
    """'x < 2', '2 <= x', '-1 < x <= 4', 'x = 3' -> Liste von Intervallen oder None."""
    s = teil.replace(" ", "")
    stuecke = re.split(r"(<=|>=|=<|=>|≤|≥|<|>|=)", s)
    if len(stuecke) < 3:
        return None
    werte, rels = stuecke[0::2], stuecke[1::2]
    vname = variable
    def ist_var(w):
        return re.fullmatch(r"[A-Za-z](_?\{?\w+\}?)?", w) is not None and not re.fullmatch(r"\d+", w)
    if len(werte) == 2:
        if ist_var(werte[0]):
            r, g = rels[0], _grenze(werte[1], kd)
        elif ist_var(werte[1]):
            r = {"<": ">", ">": "<", "<=": ">=", ">=": "<=", "≤": "≥", "≥": "≤", "=<": "=>", "=>": "=<", "=": "="}[rels[0]]
            g = _grenze(werte[0], kd)
        else:
            return None
        if r == "=":
            return [Intervall(g, True, g, True)]
        art = _REL[r]
        if art == "lt":
            return [Intervall(_MINF, False, g, False)]
        if art == "le":
            return [Intervall(_MINF, False, g, True)]
        if art == "gt":
            return [Intervall(g, False, _PINF, False)]
        return [Intervall(g, True, _PINF, False)]
    if len(werte) == 3 and ist_var(werte[1]):
        a, b = _grenze(werte[0], kd), _grenze(werte[2], kd)
        r1, r2 = _REL.get(rels[0]), _REL.get(rels[1])
        if r1 in ("lt", "le") and r2 in ("lt", "le"):
            return [Intervall(a, r1 == "le", b, r2 == "le")]
        if r1 in ("gt", "ge") and r2 in ("gt", "ge"):
            return [Intervall(b, r2 == "ge", a, r1 == "ge")]
    return None


def bereich_parsen(text, variable="x"):
    """Lösungsmenge -> normalisierte Liste von Intervallen (Punkte = [a, a]).

    Erlaubt: '{2; -3}', 'x = 2 oder x = -3', '2, -3', '[0, 3)', ']-∞, 2]', 'x < 2',
    '-1 < x <= 4', 'x < 0 oder x > 2', Vereinigung mit ∪, 'ℝ', 'keine', '{}', 'ℝ \\ {2}'.
    """
    s = str(text).strip()
    s = s.replace("−", "-").replace("–", "-").replace("≦", "≤").replace("≧", "≥")
    s = re.sub(r"^\s*L\s*=\s*", "", s)
    # "x = ±5" bzw. "x = 2 ± sqrt(3)" -> "5; -5"
    m = re.fullmatch(r"\s*[a-zA-Z](?:_\w+)?\s*=\s*([^;{}]*(?:±|\+/-|\+-)[^;{}]*)", s)
    if m:
        s = "; ".join(_plusminus_aufspalten(m.group(1).strip()))
    if _ist_leer(s):
        return []
    roh = re.sub(r"\s+", "", s.lower())
    if roh in ("r", "ℝ", "allereellenzahlen", "alle", "allex", "unendlichviele"):
        return [Intervall(_MINF, False, _PINF, False)]
    m = re.fullmatch(r"(?:ℝ|r)(?:\\|∖|ohne)(.*)", roh)
    if m:
        ausnahmen = sorted(_punkte(m.group(1)), key=lambda g: g.f())
        erg, lo, lo_zu = [], _MINF, False
        for p in ausnahmen:
            erg.append(Intervall(lo, lo_zu, p, False))
            lo, lo_zu = p, False
        erg.append(Intervall(lo, False, _PINF, False))
        return _normalisieren(erg)
    teile = re.split(r"\s*(?:∪|\boder\b|\bu\b|\|\||\bvereinigt\b)\s*", s)
    erg = []
    for teil in teile:
        teil = teil.strip()
        if not teil:
            continue
        if teil[0] in "[](" and teil[-1] in "[]()" and not teil.startswith("{"):
            innen = teil[1:-1]
            stuecke, kd = liste_zerlegen(innen)
            if len(stuecke) != 2:
                raise TermFehler(f"Ein Intervall braucht genau zwei Grenzen: {teil}. "
                                 "Bei Kommazahlen trenne mit ;, z. B. [0,5; 3].")
            a, b = _grenze(stuecke[0], kd), _grenze(stuecke[1], kd)
            lo_zu = teil[0] == "[" and not math.isinf(a.f())
            hi_zu = teil[-1] == "]" and not math.isinf(b.f())
            if a.f() > b.f():
                raise TermFehler(f"Im Intervall {teil} ist die linke Grenze größer als die rechte.")
            erg.append(Intervall(a, lo_zu, b, hi_zu))
            continue
        if teil.startswith("{") or ";" in teil or ("," in teil and not re.search(r"[<>≤≥=]", teil)):
            for p in _punkte(teil):
                erg.append(Intervall(p, True, p, True))
            continue
        if re.search(r"[<>≤≥=]", teil):
            kd = True
            # mehrere Gleichungen mit Komma: "x1 = 2, x2 = 3"
            if "," in teil and teil.count("=") > 1:
                for st in liste_zerlegen(teil)[0]:
                    iv = _ungleichung(st, variable, True)
                    if iv is None:
                        raise TermFehler(f"„{st}“ verstehe ich nicht.")
                    erg.extend(iv)
                continue
            iv = _ungleichung(teil, variable, kd)
            if iv is None:
                raise TermFehler(f"„{teil}“ verstehe ich nicht. Schreibe z. B. x < 2 oder [0; 3).")
            erg.extend(iv)
            continue
        for p in _punkte(teil):
            erg.append(Intervall(p, True, p, True))
    return _normalisieren(erg)


def _punkte(text):
    s = text.strip()
    if s.startswith("{") and s.endswith("}"):
        s = s[1:-1]
    if not s.strip():
        return []
    teile, kd = liste_zerlegen(s)
    erg = []
    for t in teile:
        t = re.sub(r"^\s*[A-Za-z](_?\{?\d+\}?)?\s*=\s*", "", t)
        erg.append(_grenze(t, kd))
    return erg


def bereiche_gleich(a, b):
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if not (gleich_grenze(x.lo, y.lo) and gleich_grenze(x.hi, y.hi)
                and x.lo_zu == y.lo_zu and x.hi_zu == y.hi_zu):
            return False
    return True


def bereich_latex(ivs):
    return re.sub(r"\\frac\{-(\w+)\}", r"-\\frac{\1}", _bereich_latex(ivs))


def _bereich_latex(ivs):
    if not ivs:
        return "\\emptyset"
    if len(ivs) == 1 and math.isinf(ivs[0].lo.f()) and math.isinf(ivs[0].hi.f()):
        return "\\mathbb{R}"
    if all(i.punkt() for i in ivs):
        el = [i.lo.latex for i in ivs]
        trenner = ";\\ " if any("{,}" in e for e in el) else ", "
        return "\\{" + trenner.join(el) + "\\}"
    teile = []
    for i in ivs:
        if i.punkt():
            teile.append("\\{" + i.lo.latex + "\\}")
        else:
            trenner = ";\\ " if "{,}" in i.lo.latex + i.hi.latex else ", "
            teile.append(("[" if i.lo_zu else "(") + i.lo.latex + trenner + i.hi.latex + ("]" if i.hi_zu else ")"))
    return " \\cup ".join(teile)


# ──────────────────────────────────────────────────────────────────────────
#  LaTeX-Teilmenge -> Term-Text (für das Nachrechnen von :::rechnung)
# ──────────────────────────────────────────────────────────────────────────

def _klammer_inhalt(s, i):
    """s[i] == '{' -> (inhalt, index nach '}')"""
    tiefe, j = 0, i
    while j < len(s):
        if s[j] == "{":
            tiefe += 1
        elif s[j] == "}":
            tiefe -= 1
            if tiefe == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise TermFehler("Geschweifte Klammer nicht geschlossen")


class NichtPruefbar(ValueError):
    pass


def latex_zu_term(tex):
    """Übersetzt eine LaTeX-Teilmenge in Term-Syntax. NichtPruefbar, wenn unbekannt."""
    s = str(tex)
    s = re.sub(r"\\hl\{", "{", s)
    s = re.sub(r"\\(?:color|textcolor)\{[^}]*\}", "", s)
    s = re.sub(r"\\(left|right|big|Big|bigg|Bigg)(?=[()\[\]|.]|\\\{|\\\})", "", s)
    s = s.replace("\\left.", "").replace("\\right.", "")
    s = re.sub(r"\\(,|;|!|quad|qquad| )", " ", s)
    s = s.replace("{,}", ".").replace("\\cdot", "*").replace("\\times", "*").replace("\\div", "/")
    s = s.replace("\\pi", "pi").replace("\\mathrm{e}", "e").replace("\\operatorname{e}", "e")
    s = re.sub(r"\\(?:mathrm|operatorname)\{(sin|cos|tan|ln|exp)\}", r"\\\1", s)
    s = re.sub(r"\\log_\{?(2|10)\}?", r"log\1 ", s)
    s = re.sub(r"\\(sin|cos|tan|ln|exp)\b", r"\1 ", s)
    s = s.replace("\\lvert", "|").replace("\\rvert", "|").replace("\\vert", "|")
    # \frac, \dfrac, \tfrac, \sqrt
    while True:
        m = re.search(r"\\[dt]?frac\s*", s)
        if not m:
            break
        i = m.end()
        if i >= len(s) or s[i] != "{":
            raise NichtPruefbar("frac ohne Klammern")
        z, j = _klammer_inhalt(s, i)
        if j >= len(s) or s[j] != "{":
            raise NichtPruefbar("frac ohne Nenner")
        n, k = _klammer_inhalt(s, j)
        s = s[:m.start()] + f"(({z})/({n}))" + s[k:]
    while True:
        m = re.search(r"\\sqrt\s*(\[[^\]]*\])?\s*", s)
        if not m:
            break
        i = m.end()
        if i >= len(s) or s[i] != "{":
            raise NichtPruefbar("sqrt ohne Klammern")
        z, j = _klammer_inhalt(s, i)
        if m.group(1):
            s = s[:m.start()] + f"(({z})^(1/({m.group(1)[1:-1]})))" + s[j:]
        else:
            s = s[:m.start()] + f"sqrt({z})" + s[j:]
    s = re.sub(r"_\{(\w+)\}", r"_\1", s)
    s = s.replace("{", "(").replace("}", ")")
    if "\\" in s:
        raise NichtPruefbar(f"unbekannter Befehl in {tex!r}")
    return s


_RELATIONEN_LATEX = [("\\leq", "≤"), ("\\le", "≤"), ("\\geq", "≥"), ("\\ge", "≥"), ("\\neq", "≠"),
                     ("\\ne", "≠"), ("\\lt", "<"), ("\\gt", ">")]


def latex_relationen(tex):
    """Zerlegt 'A = B < C' in (['A', 'B', 'C'], ['=', '<'])."""
    s = tex
    for alt, neu in _RELATIONEN_LATEX:
        s = re.sub(re.escape(alt) + r"(?![a-zA-Z])", neu, s)
    s = s.replace("&", "")
    stuecke = re.split(r"(=|≤|≥|≠|<|>)", s)
    return [x.strip() for x in stuecke[0::2]], stuecke[1::2]


# ──────────────────────────────────────────────────────────────────────────
#  LaTeX-Validator (offline, ohne KaTeX)
# ──────────────────────────────────────────────────────────────────────────

LATEX_BEFEHLE = set("""
frac dfrac tfrac sqrt cdot times div pm mp le leq ge geq neq ne lt gt approx equiv sim cong
pi alpha beta gamma delta Delta epsilon varepsilon zeta eta theta vartheta Theta iota kappa lambda Lambda
mu nu xi Xi rho sigma Sigma tau phi varphi Phi chi psi Psi omega Omega Gamma Pi
sin cos tan cot arcsin arccos arctan sinh cosh tanh ln log exp lim limsup liminf max min sup inf det dim ker deg gcd
sum prod int iint oint infty partial nabla mathbb mathcal mathrm mathbf mathit mathsf operatorname text textbf textit
left right big Big bigg Bigg bigl bigr Bigl Bigr quad qquad
in notin ni subset subseteq supset supseteq subsetneq cup cap setminus emptyset varnothing forall exists nexists neg lnot land lor wedge vee
Rightarrow Leftarrow Leftrightarrow rightarrow leftarrow leftrightarrow to mapsto implies iff impliedby longrightarrow Longrightarrow longmapsto
overline underline hat bar vec tilde dot ddot widehat widetilde overrightarrow overbrace underbrace binom tbinom dbinom choose
begin end hline cline displaystyle textstyle scriptstyle ldots cdots vdots ddots dots mid nmid parallel perp angle triangle circ bullet
lfloor rfloor lceil rceil langle rangle lvert rvert lVert rVert vert Vert backslash setminus
color textcolor colorbox htmlClass hl luecke boxed cancel bcancel xcancel phantom hphantom vphantom
underset overset stackrel substack prime ast star dagger aleph ell hbar Re Im mod bmod pmod
equiv not uparrow downarrow updownarrow Uparrow Downarrow mathfrak checkmark square blacksquare Box
tag notag nonumber limits nolimits
 mathbin colon lg top oplus Longleftrightarrow preccurlyeq succcurlyeq prec succ bigcup bigcap coloneqq ominus otimes bigoplus nRightarrow nLeftrightarrow bot nexists""".split())
LATEX_UMGEBUNGEN = {"pmatrix", "bmatrix", "vmatrix", "matrix", "array", "cases", "aligned", "align*",
                    "gathered", "smallmatrix", "Bmatrix", "Vmatrix", "rcases", "split"}


def latex_pruefen(tex):
    """Liefert Probleme in einer LaTeX-Formel (leere Liste = in Ordnung)."""
    probleme = []
    s = str(tex)
    if "\n\n" in s:
        probleme.append("Leerzeile in Formel")
    tiefe = 0
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            m = re.match(r"\\([A-Za-z]+|.)", s[i:])
            befehl = m.group(1) if m else ""
            if befehl.isalpha() and befehl not in LATEX_BEFEHLE:
                probleme.append(f"unbekannter LaTeX-Befehl \\{befehl}")
            i += len(m.group(0)) if m else 1
            continue
        if c == "{":
            tiefe += 1
        elif c == "}":
            tiefe -= 1
            if tiefe < 0:
                probleme.append("zu viele }")
                tiefe = 0
        i += 1
    if tiefe:
        probleme.append("{ und } passen nicht zusammen")
    links = len(re.findall(r"\\left(?![a-zA-Z])", s))
    rechts = len(re.findall(r"\\right(?![a-zA-Z])", s))
    if links != rechts:
        probleme.append("\\left und \\right passen nicht zusammen")
    for art, name in re.findall(r"\\(begin|end)\{([^}]*)\}", s):
        if name not in LATEX_UMGEBUNGEN:
            probleme.append(f"unbekannte Umgebung {name}")
    if s.count("\\begin") != s.count("\\end"):
        probleme.append("\\begin und \\end passen nicht zusammen")
    for ctrl in "\f\b\a\v\t\r":
        if ctrl in s:
            probleme.append("Steuerzeichen in Formel (r-String vergessen?)")
    return probleme


def grenze_text(g):
    """Grenze -> Eingabetext (für Musterantworten)."""
    if math.isinf(g.f()):
        return "inf" if g.f() > 0 else "-inf"
    if isinstance(g.wert, Fraction):
        return fraction_text(g.wert)
    try:
        return latex_zu_term(g.latex)
    except (NichtPruefbar, TermFehler):
        return repr(g.f())


def bereich_text(ivs):
    """Intervalle -> Eingabetext, den bereich_parsen wieder versteht."""
    if not ivs:
        return "{}"
    if all(i.punkt() for i in ivs):
        return "{" + "; ".join(grenze_text(i.lo) for i in ivs) + "}"
    teile = []
    for i in ivs:
        if i.punkt():
            teile.append("{" + grenze_text(i.lo) + "}")
        else:
            teile.append(("[" if i.lo_zu else "(") + grenze_text(i.lo) + "; " + grenze_text(i.hi)
                         + ("]" if i.hi_zu else ")"))
    return " ∪ ".join(teile)
