# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 17: Ringe, Körper und die rationalen Zahlen (Skript Disser WS 26/27, Abschn. 3.3 bis 3.5, Def. 3.46 bis 3.79)."""
from fractions import Fraction as F
from itertools import product
from math import gcd

from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(
    slug="ringe_koerper",
    titel="Ringe, Körper und die rationalen Zahlen",
    beschreibung="Ring, Vorzeichenregeln, Restklassenring, Nullteiler, ℚ aus Paaren, Körper, ℤ/pℤ, Körperhomomorphismen, angeordnete Körper",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 3.3 bis 3.5",
    icon="🏛️")


# ── Python prüft die Strukturen exakt ────────────────────────────────────
def mal_tafel(n):
    return [[(a * b) % n for b in range(n)] for a in range(n)]


def nullteiler(n):
    return {a for a in range(1, n) if any((a * b) % n == 0 for b in range(1, n))}


def einheiten(n):
    return {a for a in range(1, n) if any((a * b) % n == 1 for b in range(1, n))}


def ist_prim(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def inv_mod(a, n):
    return next(b for b in range(1, n) if (a * b) % n == 1)


def rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def mtext(s):
    return "{" + "; ".join(str(x) for x in sorted(s)) + "}"


# Beispiel 3.51 und 3.70
assert mal_tafel(4) == [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 0, 2], [0, 3, 2, 1]]
assert mal_tafel(5) == [[0, 0, 0, 0, 0], [0, 1, 2, 3, 4], [0, 2, 4, 1, 3], [0, 3, 1, 4, 2], [0, 4, 3, 2, 1]]
assert [inv_mod(a, 5) for a in (1, 2, 3, 4)] == [1, 3, 2, 4] and 2 not in einheiten(4) and nullteiler(4) == {2} and nullteiler(5) == set()
# Satz 3.54 und 3.69: Nullteiler genau bei zusammengesetztem n, Körper genau bei Primzahl n
for _n in range(2, 40):
    assert (nullteiler(_n) == set()) == ist_prim(_n)
    assert (len(einheiten(_n)) == _n - 1) == ist_prim(_n)
# Ringaxiome und Satz 3.48 in Z/6Z
_n = 6
for _a, _b, _c in product(range(_n), repeat=3):
    assert (_a * (_b + _c)) % _n == (_a * _b + _a * _c) % _n and ((_a * _b) * _c) % _n == (_a * (_b * _c)) % _n
    assert ((-_a) * _b) % _n == (-(_a * _b)) % _n and ((-_a) * (-_b)) % _n == (_a * _b) % _n
# Satz 3.67 / Fermat: a^(p-2) ist das Inverse in Z/pZ
assert all((a * pow(a, p - 2, p)) % p == 1 for p in (2, 3, 5, 7, 11, 13, 17) for a in range(1, p))
# φ4: k -> 4k ist kein Ringhomomorphismus (Einführung zu Def. 3.55)
assert 4 * (1 * 1) == 4 and (4 * 1) * (4 * 1) == 16 and 4 * 1 != 1
# Z -> Z/nZ erhält Addition, Multiplikation und die Eins (Bsp. 3.58)
assert all(((a * b) % 7) == (((a % 7) * (b % 7)) % 7) and ((a + b) % 7) == (((a % 7) + (b % 7)) % 7) for a in range(-20, 21) for b in range(-20, 21))


# Definition 3.60/3.61: Paare (a, b) mit b > 0 und ad = bc
def p_gleich(p, q):
    return p[0] * q[1] == p[1] * q[0]


def p_add(p, q):
    return (p[0] * q[1] + p[1] * q[0], p[1] * q[1])


def p_mul(p, q):
    return (p[0] * q[0], p[1] * q[1])


def p_div(p, q):
    a, b = p
    c, d = q
    return (a * d, b * c) if c > 0 else (-a * d, -b * c)


for _a, _b, _c, _d in product([-3, -1, 0, 2, 5], [1, 2, 3, 4], [-4, -2, 1, 3], [1, 2, 5]):
    _p, _q = (_a, _b), (_c, _d)
    assert F(*p_add(_p, _q)) == F(_a, _b) + F(_c, _d) and F(*p_mul(_p, _q)) == F(_a, _b) * F(_c, _d)
    assert p_div(_p, _q)[1] > 0 and F(*p_div(_p, _q)) == F(_a, _b) / F(_c, _d)
    assert (F(_a, _b) <= F(_c, _d)) == (_a * _d <= _b * _c)
assert p_gleich((2, 4), (1, 2)) and not p_gleich((2, 4), (1, 3))

k.lernziele([
    "Ich kann die Ringaxiome (g), (m), (d) nennen, Ringe von Nicht-Ringen unterscheiden und die Vorzeichenregeln aus ihnen beweisen (Def. 3.46, Satz 3.48)",
    "Ich kann in Restklassenringen $\\mathbb{Z}/n\\mathbb{Z}$ rechnen, Nullteiler finden und weiß, wann es keine gibt (Def. 3.49, 3.52, Satz 3.53, 3.54)",
    "Ich kann $\\mathbb{Q}$ als Paare $(a, b)$ mit $ad = bc$ beschreiben und damit rechnen (Def. 3.60, 3.61)",
    "Ich kann Körper definieren, $\\mathbb{Z}/p\\mathbb{Z}$ als Körper begründen und Inverse bestimmen (Def. 3.64, Satz 3.69)",
    "Ich kann Ring-, Körperhomomorphismen und angeordnete Körper einordnen (Def. 3.55, 3.71, 3.76, Satz 3.72, 3.73, 3.78)",
])

k.warum(r"""
Bits und Bytes rechnen in $\mathbb{Z}/2\mathbb{Z}$ und $\mathbb{Z}/256\mathbb{Z}$. Dass ein Byte-Wert nicht immer eine
Umkehrung bei der Multiplikation hat, liegt an Nullteilern. Prüfsummen, Hashing, Verschlüsselung (RSA arbeitet in $\mathbb{Z}/n\mathbb{Z}$)
und Fehlerkorrektur (Reed-Solomon in $\mathbb{F}_{256}$) leben von Körpern wie $\mathbb{Z}/p\mathbb{Z}$. Und die Lineare Algebra im
nächsten Kapitel läuft über **beliebigen** Körpern: Du brauchst dort nur die Körperaxiome, nicht die Zahlen $\mathbb{R}$.
""")

# ── Seite 1: Ringe ───────────────────────────────────────────────────────
k.erklaerung("Definition 3.46: Ring", r"""
## Zwei Verknüpfungen, die zusammenpassen

In $\mathbb{Z}$ gibt es Addition **und** Multiplikation. Ein [[Ring]] erfasst, wie beide zusammenwirken.

**Definition 3.46.** $(R, +, \cdot)$ mit $R \ne \emptyset$ und $+, \cdot\colon R^2 \to R$ ist ein Ring, falls

- (g) $(R, +)$ eine abelsche Gruppe ist (Nullelement $0$, Gegenelement $-a$),
- (m) $a(bc) = (ab)c$ (Assoziativität der Multiplikation),
- (d) $a(b + c) = ab + ac$ und $(a + b)c = ac + bc$ (Distributivität).

Gibt es $1$ mit $1a = a1 = a$, ist es ein Ring mit Eins. Gilt $ab = ba$, ist der Ring kommutativ.

**Beispiel 3.47.** $(\mathbb{Z}, +, \cdot)$ ist ein kommutativer Ring mit Eins. $(\mathbb{N}, +, \cdot)$ ist **kein** Ring: $(\mathbb{N}, +)$ ist keine Gruppe.

:::rechnung Distributivität in $\mathbb{Z}$ mit $a = 3$, $b = 4$, $c = 5$
3 \cdot (4 + 5) = 27 || (d): erst klammern
3 \cdot 4 + 3 \cdot 5 = 27 || (d): erst ausmultiplizieren, gleiches Ergebnis
(3 \cdot 4) \cdot 5 = 3 \cdot (4 \cdot 5) || (m): Klammern versetzen
:::

:::alt Als Buchhaltung
Die Addition ist das Kontobuch (Gruppe, Rückbuchung möglich), die Multiplikation ist „dasselbe $n$-mal buchen“. (d) sagt: $3$ Überweisungen
zu $4$ Euro und zu $5$ Euro sind dasselbe wie $3 \cdot 9$ Euro.
:::
""")

k.mc("Warum ist $(\\mathbb{N}, +, \\cdot)$ mit $\\mathbb{N} = \\{0, 1, 2, \\ldots\\}$ kein Ring?",
     ["Weil $(\\mathbb{N}, +)$ keine Gruppe ist: Zu $1$ gibt es kein Gegenelement in $\\mathbb{N}$",
      "Weil die Multiplikation auf $\\mathbb{N}$ nicht assoziativ ist",
      "Weil $(d)$ auf $\\mathbb{N}$ nicht gilt",
      "Weil $\\mathbb{N}$ kein Einselement hat"],
     "Assoziativität (m) und Distributivität (d) gelten in $\\mathbb{N}$, und $1$ ist das Einselement. Es scheitert an (g): $(\\mathbb{N}, +)$ ist keine abelsche Gruppe, da Inverse fehlen (Bsp. 3.47).",
     tipps=["Prüfe (g), (m), (d) der Reihe nach.", "Hat $1 \\in \\mathbb{N}$ ein $b$ mit $1 + b = 0$?"],
     fehler={"Weil die Multiplikation auf $\\mathbb{N}$ nicht assoziativ ist": "Sie ist assoziativ: $(2 \\cdot 3) \\cdot 4 = 2 \\cdot (3 \\cdot 4)$.",
             "Weil $(d)$ auf $\\mathbb{N}$ nicht gilt": "Das Distributivgesetz gilt in $\\mathbb{N}$.",
             "Weil $\\mathbb{N}$ kein Einselement hat": "$1$ ist das Einselement. Für einen Ring wird es ohnehin nur in „Ring mit Eins“ verlangt."})

# ── Seite 2: Satz 3.48 ───────────────────────────────────────────────────
k.erklaerung("Satz 3.48: Die Vorzeichenregeln folgen aus den Axiomen", r"""
## Minus mal Minus

**Satz 3.48.** In jedem Ring gilt $0 \cdot a = a \cdot 0 = 0$, $(-a)b = a(-b) = -(ab)$ und $(-a)(-b) = ab$.

*Beweis.* Mit (d): $a0 = a(0 + 0) = a0 + a0$. Außerdem $a0 = a0 + 0$. Kürzungsregel in $(R, +)$ (Satz 3.16 (ii)): $a0 = 0$.

Weiter $(-a)b + ab = ((-a) + a)b = 0b = 0$. Also ist $(-a)b$ das Inverse von $ab$: $(-a)b = -(ab)$.
Schließlich $(-a)(-b) = -((-a)b) = -(-(ab)) = ab$ (Satz 3.17).

:::rechnung Beweisidee in $\mathbb{Z}$ mit $a = 3$, $b = 5$
(-3) \cdot 5 + 3 \cdot 5 = (-3 + 3) \cdot 5 || (d): Ausklammern von $5$
(-3 + 3) \cdot 5 = 0 \cdot 5 || (g): $-3 + 3 = 0$
0 \cdot 5 = 0 || erster Teil des Satzes: $(-3) \cdot 5$ ist das Inverse von $15$, also $-15$
:::

:::achtung Das ist kein Axiom
„Minus mal Minus ist Plus“ steht in keiner Definition. Es ist eine **Folgerung** aus (g) und (d). Genau deshalb gilt es in jedem Ring, nicht nur in $\mathbb{Z}$.
:::

:::alt Als Schuldenbuch
$(-a)(-b)$ heißt: Eine Schuld ($-a$) wird $b$-mal rückgängig gemacht. Rückgängig machen einer Schuld ist ein Guthaben, und das Ergebnis ist $ab$. Die Axiome liefern dasselbe, ohne dieses Bild.
:::
""")

k.ordnen("Ordne den Beweis von Satz 3.48: $0 \\cdot a$-Teil und $(-a)b = -(ab)$ (in der Variante $a \\cdot 0 = 0$).",
         ["Es ist $a0 = a(0 + 0) = a0 + a0$ nach (d), denn $0 + 0 = 0$.",
          "Außerdem ist $a0 = a0 + 0$, da $0$ das neutrale Element von $(R, +)$ ist.",
          "Also $a0 + 0 = a0 + a0$, und die Kürzungsregel in $(R, +)$ (Satz 3.16 (ii)) liefert $a0 = 0$.",
          "Weiter ist $(-a)b + ab = ((-a) + a)b = 0b = 0$ (d und der erste Teil).",
          "Somit ist $(-a)b$ das additive Inverse zu $ab$, also $(-a)b = -(ab)$."],
         "Der erste Teil benutzt (d) und die Kürzungsregel der Gruppe $(R, +)$. Der zweite benutzt (d) und das erste Ergebnis: $0b = 0$.",
         ablenker=["Da $R$ ein Körper ist, gilt $a0 = 0$ sofort.", "Aus $a0 = a0 + a0$ folgt $a0 = 2 \\cdot a0$, also $a0 = 1$."],
         tipps=["Schreibe $0 = 0 + 0$ und multipliziere mit $a$.", "Dann hast du $a0 = a0 + a0$. Was sagt die Kürzungsregel für $(R, +)$?", "Im zweiten Teil brauchst du $0 \\cdot b = 0$."])

# ── Seite 3: Restklassenring ─────────────────────────────────────────────
k.erklaerung("Definition 3.49: Der Restklassenring ℤ/nℤ", r"""
## Mit Resten multiplizieren

**Definition 3.49.** $[a]_n \cdot [b]_n := [ab]_n$ auf $\mathbb{Z}/n\mathbb{Z}$. Mit der Addition aus Beispiel 3.15 ist das der [[Restklassenring]] modulo $n$.

**Satz 3.50.** Die Multiplikation ist [[wohldefiniert]], und $\mathbb{Z}/n\mathbb{Z}$ ist ein kommutativer Ring mit Nullelement $[0]_n$ und Einselement $[1]_n$.
*Wohldefiniert:* Aus $a - a' = kn$ und $b - b' = \ell n$ folgt $ab - a'b' = a(b - b') + b'(a - a') = (a\ell + b'k)n$.

**Beispiel 3.51.** Multiplikationstafeln (Vertreter $r$ für $[r]_n$):

| $\cdot$ | $0$ | $1$ | $2$ | $3$ |
|---|---|---|---|---|
| $0$ | $0$ | $0$ | $0$ | $0$ |
| $1$ | $0$ | $1$ | $2$ | $3$ |
| $2$ | $0$ | $2$ | $0$ | $2$ |
| $3$ | $0$ | $3$ | $2$ | $1$ |

| $\cdot$ | $0$ | $1$ | $2$ | $3$ | $4$ |
|---|---|---|---|---|---|
| $0$ | $0$ | $0$ | $0$ | $0$ | $0$ |
| $1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| $2$ | $0$ | $2$ | $4$ | $1$ | $3$ |
| $3$ | $0$ | $3$ | $1$ | $4$ | $2$ |
| $4$ | $0$ | $4$ | $3$ | $2$ | $1$ |

In $\mathbb{Z}/4\mathbb{Z}$ ist $[2] \cdot [2] = [0]$ obwohl $[2] \ne [0]$. In $\mathbb{Z}/5\mathbb{Z}$ tritt das nicht auf.

:::rechnung Drei Einträge nachgerechnet
(3 \cdot 3) \bmod 4 = 1 || $\mathbb{Z}/4\mathbb{Z}$: $9 = 2 \cdot 4 + 1$
(2 \cdot 2) \bmod 4 = 0 || $4 \equiv 0$: Produkt zweier Nicht-Nullen ist $0$
(2 \cdot 3) \bmod 5 = 1 || $\mathbb{Z}/5\mathbb{Z}$: $[2]$ und $[3]$ sind invers zueinander
:::

:::alt Als Uhr und als Sudoku
Multiplizieren heißt: $b$-mal um $a$ Stunden weiterspringen auf einer Uhr mit $n$ Plätzen. Bei $n = 5$ ist jede Zeile ohne die $0$ eine Umordnung von $1, 2, 3, 4$ wie bei einem Sudoku: Man kann umkehren. Bei $n = 4$ kommt in der Zeile der $2$ die $0$ doppelt vor: Man kann nicht kürzen.
:::
""")

k.luecke("Ergänze zwei Einträge der Multiplikationstafel von $\\mathbb{Z}/4\\mathbb{Z}$ (Bsp. 3.51): $[3]_4 \\cdot [3]_4 = [\\luecke]_4$ und $[2]_4 \\cdot [3]_4 = [\\luecke]_4$.",
         "[3]_4 \\cdot [3]_4 = [\\luecke]_4 \\quad\\text{und}\\quad [2]_4 \\cdot [3]_4 = [\\luecke]_4",
         [[1], [2]],
         "$3 \\cdot 3 = 9 = 2 \\cdot 4 + 1$, also $[1]_4$. $2 \\cdot 3 = 6 = 1 \\cdot 4 + 2$, also $[2]_4$.",
         tipps=["Multipliziere die Zahlen und reduziere modulo $4$.", "$3 \\cdot 3 = 9$, $2 \\cdot 3 = 6$.", "$9 \\bmod 4 = 1$ und $6 \\bmod 4 = 2$."],
         rechenweg=rechnung([("(3 \\cdot 3) \\bmod 4 = 1", "$9 = 2 \\cdot 4 + 1$"), ("(2 \\cdot 3) \\bmod 4 = 2", "$6 = 1 \\cdot 4 + 2$")]),
         typische_fehler=[([9, 6], "Du hast nicht modulo $4$ reduziert. Die Vertreter liegen in $\\{0, 1, 2, 3\\}$.")])

# ── Seite 4: Nullteiler ──────────────────────────────────────────────────
k.erklaerung("Nullteiler: Wenn Kürzen scheitert", r"""
## Definition 3.52, Satz 3.53, Satz 3.54

**Definition 3.52.** In einem kommutativen Ring heißt $a \in R \setminus \{0\}$ [[Nullteiler]], falls es $b \in R \setminus \{0\}$ mit $ab = 0$ gibt.

**Satz 3.53.** $a \ne 0$ ist genau dann **kein** Nullteiler, wenn $M_a\colon R \to R,\ x \mapsto ax$ injektiv ist. (Daraus folgt die Kürzungsregel $ab = ac \Rightarrow b = c$.)

**Satz 3.54.** Ist $n > 1$ keine Primzahl, hat $\mathbb{Z}/n\mathbb{Z}$ Nullteiler.

*Beweis.* $n = rs$ mit $1 < r, s < n$. Dann $[r] \ne [0]$, $[s] \ne [0]$ und $[r][s] = [n] = [0]$.

:::rechnung In $\mathbb{Z}/15\mathbb{Z}$
3 \cdot 5 = 15 || $15 = 3 \cdot 5$, also $[3] \cdot [5] = [0]$ obwohl beide $\ne [0]$
(3 \cdot 4) \bmod 15 = 12 || $M_3$: $[4] \mapsto [12]$
(3 \cdot 9) \bmod 15 = 12 || $[9] \mapsto [12]$: $M_3$ ist nicht injektiv, wegen $4 \ne 9$
:::

:::alt Als Verschwinden
Ein Nullteiler ist ein Faktor, der etwas zum Verschwinden bringen kann, ohne selbst Null zu sein: Wie ein Filter, der zwei verschiedene Signale (4 und 9) gleich aussehen lässt. Dann kannst du das Signal nicht rekonstruieren.
:::
""")

k.mc("Welches Element von $\\mathbb{Z}/6\\mathbb{Z}$ ist **kein** Nullteiler?",
     ["$[5]_6$", "$[2]_6$", "$[3]_6$", "$[4]_6$"],
     "$[2] \\cdot [3] = [0]$ und $[4] \\cdot [3] = [12] = [0]$: Also sind $[2], [3], [4]$ Nullteiler. Für $[5]$ gilt $[5] \\cdot [b] = [0] \\iff 6 \\mid 5b \\iff 6 \\mid b$, also $[b] = [0]$.",
     tipps=["Suche zu jedem Element ein $[b] \\ne [0]$ mit Produkt $[0]$.", "$2 \\cdot 3 = 6$ und $4 \\cdot 3 = 12$.", "$5 \\equiv -1 \\pmod 6$, und $[-1] \\cdot [b] = [-b]$ ist nur für $[b] = [0]$ gleich $[0]$."],
     fehler={"$[2]_6$": "$[2] \\cdot [3] = [6] = [0]$ mit $[3] \\ne [0]$: $[2]$ ist Nullteiler.",
             "$[3]_6$": "$[3] \\cdot [2] = [0]$ mit $[2] \\ne [0]$: Nullteiler.",
             "$[4]_6$": "$[4] \\cdot [3] = [12] = [0]$ mit $[3] \\ne [0]$: Nullteiler."})

k.mehrfach("Welche der folgenden Ringe $\\mathbb{Z}/n\\mathbb{Z}$ haben **keine** Nullteiler?",
           ["$\\mathbb{Z}/2\\mathbb{Z}$", "$\\mathbb{Z}/7\\mathbb{Z}$", "$\\mathbb{Z}/13\\mathbb{Z}$"],
           ["$\\mathbb{Z}/9\\mathbb{Z}$", "$\\mathbb{Z}/10\\mathbb{Z}$", "$\\mathbb{Z}/12\\mathbb{Z}$"],
           "Nach Satz 3.54 hat $\\mathbb{Z}/n\\mathbb{Z}$ für zusammengesetztes $n$ Nullteiler: $9 = 3 \\cdot 3$, $10 = 2 \\cdot 5$, $12 = 3 \\cdot 4$. Für Primzahlen $p$ gibt es keine (Satz 3.69).",
           tipps=["Zerlege $n$: Ist $n$ eine Primzahl?", "$9 = 3 \\cdot 3$ liefert $[3] \\cdot [3] = [0]$."],
           fehler={"$\\mathbb{Z}/9\\mathbb{Z}$": "$[3] \\cdot [3] = [9] = [0]$: $[3]$ ist Nullteiler.",
                   "$\\mathbb{Z}/10\\mathbb{Z}$": "$[2] \\cdot [5] = [10] = [0]$.",
                   "$\\mathbb{Z}/12\\mathbb{Z}$": "$[3] \\cdot [4] = [12] = [0]$."})

# ── Seite 5: Ringhomomorphismen ──────────────────────────────────────────
k.erklaerung("Ringhomomorphismen", r"""
## Beide Verknüpfungen und die Eins erhalten

Ein Gruppenhomomorphismus für $+$ reicht nicht: $\phi_4\colon \mathbb{Z} \to \mathbb{Z},\ k \mapsto 4k$ erhält $+$, aber $\phi_4(1 \cdot 1) = 4$ und $\phi_4(1) \cdot \phi_4(1) = 16$.

**Definition 3.55.** $f\colon R \to S$ zwischen Ringen mit Eins ist ein ([[Ringhomomorphismus]]), falls für alle $a, b \in R$
$$f(a + b) = f(a) \oplus f(b),\quad f(a \cdot b) = f(a) \star f(b),\quad f(1_R) = 1_S.$$
Bijektiv: Ringisomorphismus. Ein Ringisomorphismus $R \to R$ heißt Automorphismus.

**Beispiel 3.56.** $\mathrm{id}_R$, $g \circ f$ und $f^{-1}$ (bei Isomorphismen) sind wieder Ringhomomorphismen, die Eins bleibt erhalten.
**Beobachtung 3.57.** Jeder Ringhomomorphismus ist ein Gruppenhomomorphismus für $+$: $f(0_R) = 0_S$, $f(-a) = -f(a)$.
**Beispiel 3.58.** $\pi_n\colon \mathbb{Z} \to \mathbb{Z}/n\mathbb{Z},\ a \mapsto [a]_n$ ist ein surjektiver Ringhomomorphismus. **Satz 3.59 (Übung):** $f(R)$ ist wieder ein Ring mit Eins $1_S$.

:::rechnung $\pi_7$ erhält $+$, $\cdot$ und $1$ (mit $a = 8$, $b = 12$)
8 + 12 = 20 || $\pi_7(20) = [20]_7 = [6]_7$
(8 \bmod 7) + (12 \bmod 7) = 1 + 5 || $[1]_7 + [5]_7 = [6]_7$: gleich
(8 \cdot 12) \bmod 7 = 96 \bmod 7 || $\pi_7(96) = [5]_7$
(1 \cdot 5) \bmod 7 = 5 || $\pi_7(8) \cdot \pi_7(12) = [1] \cdot [5] = [5]$: gleich
:::

:::alt Als Umrechnung
Ein Ringhomomorphismus rechnet Zahlen in ein anderes System um (hier: „nur der Rest zählt“), und beide Rechenarten (plus und mal) kommen gleich heraus, egal ob du erst rechnest oder erst umrechnest.
:::
""")

k.mc("Warum ist $\\phi_4\\colon \\mathbb{Z} \\to \\mathbb{Z},\\ k \\mapsto 4k$ kein Ringhomomorphismus, obwohl es ein Gruppenhomomorphismus für $+$ ist?",
     ["$\\phi_4(1) = 4 \\ne 1$ und $\\phi_4(1 \\cdot 1) = 4 \\ne 16 = \\phi_4(1) \\cdot \\phi_4(1)$",
      "Weil $\\phi_4$ nicht injektiv ist",
      "Weil $\\phi_4(0) \\ne 0$",
      "Weil $\\phi_4$ nicht surjektiv ist"],
     "Ringhomomorphismen müssen $f(a \\cdot b) = f(a) \\cdot f(b)$ und $f(1) = 1$ erfüllen. $\\phi_4$ erfüllt beides nicht. Injektivität und Surjektivität werden nicht verlangt.",
     tipps=["Prüfe die drei Bedingungen aus Definition 3.55 einzeln.", "Setze $a = b = 1$ in $f(ab) = f(a)f(b)$."],
     fehler={"Weil $\\phi_4$ nicht injektiv ist": "$\\phi_4$ ist injektiv ($\\ker(\\phi_4) = \\{0\\}$). Injektivität wird ohnehin nicht verlangt.",
             "Weil $\\phi_4(0) \\ne 0$": "$\\phi_4(0) = 0$. Das Problem ist die Multiplikation und die Eins.",
             "Weil $\\phi_4$ nicht surjektiv ist": "Surjektivität wird nicht verlangt (Bild: $4\\mathbb{Z}$)."})

# ── Seite 6: ℚ ───────────────────────────────────────────────────────────
k.erklaerung("Definition 3.60: Die rationalen Zahlen ℚ", r"""
## Brüche ohne Division

$2x = 1$ hat keine Lösung in $\mathbb{Z}$. Wieder helfen Paare: $\frac{a}{b}$ wird als $(a, b) \in \mathbb{Z} \times (\mathbb{N}\setminus\{0\})$ geschrieben, Paare gleichen Quotienten werden zusammengefasst, **ohne zu dividieren**.

**Definition 3.60.** $(a, b) \sim (c, d) :\iff ad = bc$. $\mathbb{Q} := (\mathbb{Z} \times (\mathbb{N}\setminus\{0\}))/{\sim}$, $\frac{a}{b} := [(a, b)]$, $a = [(a, 1)]$.

**Definition 3.61.** $[(a, b)] + [(c, d)] = [(ad + bc,\ bd)]$, $[(a, b)] \cdot [(c, d)] = [(ac,\ bd)]$, für $c \ne 0$ die Division $[(ad,\ bc)]$ (bei $c < 0$: $[(-ad,\ -bc)]$), $\ [(a, b)] \le [(c, d)] \iff ad \le bc$.

**Beobachtung 3.62/3.63.** In $\mathbb{Q}$ haben $q + x = r$ und (für $q \ne 0$) $qx = r$ eindeutige Lösungen. $\mathbb{Q}$ ist ein kommutativer Ring ohne Nullteiler, alles wohldefiniert.

:::rechnung Mit Paaren: $\frac12 + \frac13$ und $\frac12 : \frac{-3}{4}$
1 \cdot 3 + 2 \cdot 1 = 5 || $ad + bc$ mit $(a, b) = (1, 2)$, $(c, d) = (1, 3)$
2 \cdot 3 = 6 || $bd$: Summe $[(5, 6)] = \frac56$
-1 \cdot 4 = -4 || Division durch $\frac{-3}{4}$ ($c = -3 < 0$): $-ad$
-2 \cdot (-3) = 6 || $-bc$: Ergebnis $[(-4, 6)] = -\frac23$
:::

:::achtung Nicht komponentenweise addieren
$[(a, b)] + [(c, d)]$ ist **nicht** $[(a + c,\ b + d)]$: $\frac12 + \frac13 \ne \frac25$.
:::

:::alt Als Pizza
$\frac12$ einer Pizza plus $\frac13$ einer Pizza: erst gleiche Stücke ($\frac36$ und $\frac26$) schneiden, das ist das Erweitern mit $bd$. Zählen: $5$ Stücke von $6$. Und $M_2\colon x \mapsto 2x$ ist auf $\mathbb{Z}$ injektiv, aber nicht surjektiv (die $1$ fehlt); in $\mathbb{Q}$ ist sie surjektiv. Das unterscheidet fehlende Quotienten von Nullteilern.
:::
""")

k.luecke("Berechne mit Paaren: $[(1, 2)] + [(2, 3)] = [(\\luecke,\\ \\luecke)]$ (Definition 3.61 (i)).",
         "[(1, 2)] + [(2, 3)] = [(\\luecke,\\ \\luecke)]",
         [[7], [6]],
         "$ad + bc = 1 \\cdot 3 + 2 \\cdot 2 = 7$ und $bd = 2 \\cdot 3 = 6$: $\\frac76 = \\frac12 + \\frac23$.",
         tipps=["Formel: $[(a, b)] + [(c, d)] = [(ad + bc,\\ bd)]$.", "Hier $a = 1$, $b = 2$, $c = 2$, $d = 3$.", "$1 \\cdot 3 + 2 \\cdot 2 = 7$ und $2 \\cdot 3 = 6$."],
         rechenweg=rechnung([("1 \\cdot 3 + 2 \\cdot 2 = 7", "$ad + bc$"), ("2 \\cdot 3 = 6", "$bd$"), ("1/2 + 2/3 = 7/6", "Probe mit Brüchen")]),
         typische_fehler=[([3, 5], "Du hast komponentenweise addiert: $(1 + 2,\\ 2 + 3)$. Richtig ist $(ad + bc,\\ bd)$.")])

# ── Seite 7: Körper ──────────────────────────────────────────────────────
k.erklaerung("Definition 3.64: Körper", r"""
## Dividieren darf man jetzt

**Definition 3.64.** Ein [[Körper]] ist ein kommutativer Ring $(K, +, \cdot)$ mit Eins, für den $(K \setminus \{0_K\}, \cdot)$ eine (abelsche) Gruppe ist.

Also: Jedes $a \ne 0$ hat ein multiplikatives Inverses $a^{-1}$. **Definition 3.65:** $\frac{a}{b} := a \cdot b^{-1}$ für $b \ne 0$, und ganzzahlige Potenzen $a^z$.

**Beobachtung 3.66.** Ein Körper hat keine Nullteiler und es gilt $0_K \ne 1_K$.

**Satz 3.67.** In einem Körper hat $a \cdot x = b$ mit $a \ne 0$ die eindeutige Lösung $x = a^{-1}b$.

*Beweis.* $a(a^{-1}b) = (aa^{-1})b = 1b = b$. Ist $y$ eine weitere Lösung, so $a(x - y) = b - b = 0$, und wegen Nullteilerfreiheit $x = y$.

**Beispiel 3.68.** $(\mathbb{Q}, +, \cdot)$ ist ein Körper: $\frac1q$ ist das Inverse von $q \ne 0$.

:::rechnung In $\mathbb{Q}$: $\frac34 x = \frac12$
\text{Satz 3.67: } x = a^{-1} b || mit $a = \frac34$, $b = \frac12$
(3/4)^{-1} = 4/3 || Inverses von $\frac34$
4/3 \cdot 1/2 = 2/3 || Lösung $x = \frac23$; Probe: $\frac34 \cdot \frac23 = \frac12$
:::

:::alt Als Werkzeugkasten
Ein Ring hat Werkzeuge für Plus, Minus, Mal. Ein Körper hat zusätzlich das Gegenstück zu Mal: Dividieren durch alles außer $0$.
In $\mathbb{Z}$ fehlt das, in $\mathbb{Q}$ ist es da.
:::
""")

k.zuordnen("Ordne jede Struktur ihrem Befund zu.",
           [("$(\\mathbb{Z}, +, \\cdot)$", "kommutativer Ring mit Eins, kein Körper"),
            ("$(\\mathbb{Q}, +, \\cdot)$", "Körper"),
            ("$(\\mathbb{Z}/4\\mathbb{Z}, +, \\cdot)$", "kommutativer Ring mit Nullteilern, kein Körper"),
            ("$(\\mathbb{Z}/5\\mathbb{Z}, +, \\cdot)$", "Körper mit fünf Elementen"),
            ("$(\\mathbb{N}, +, \\cdot)$", "kein Ring")],
           "In $\\mathbb{Z}$ fehlt das Inverse von $2$, in $\\mathbb{Z}/4\\mathbb{Z}$ ist $[2]$ Nullteiler, $\\mathbb{Z}/5\\mathbb{Z}$ und $\\mathbb{Q}$ haben alle Inversen, $(\\mathbb{N}, +)$ ist keine Gruppe.",
           ablenker=["Körper mit vier Elementen"],
           tipps=["Prüfe: abelsche Gruppe bezüglich $+$? Hat jedes $a \\ne 0$ ein Inverses bezüglich $\\cdot$?", "Eine Primzahl als $n$ gibt einen Körper."])

# ── Seite 8: ℤ/pℤ ────────────────────────────────────────────────────────
k.erklaerung("Satz 3.69: ℤ/nℤ ist genau dann ein Körper, wenn n prim ist", r"""
## Mit Fermat zum Inversen

**Satz 3.69.** Für $n \in \mathbb{N}\setminus\{0\}$ ist $\mathbb{Z}/n\mathbb{Z}$ genau dann ein Körper, wenn $n$ eine Primzahl ist.

*Beweis.* $n = 1$: $[0]_1 = [1]_1$, kein Körper. $n > 1$ keine Primzahl: Nullteiler (Satz 3.54), also kein Körper.
$n = p$ prim: $\mathbb{Z}/p\mathbb{Z}$ ist kommutativer Ring mit Eins, $[0] \ne [1]$. Für $a \in \{1, \ldots, p-1\}$ gilt $p \nmid a$ und nach dem kleinen Satz von Fermat (Satz 2.67) $a^{p-1} \bmod p = 1$. Dann
$$[a]_p \cdot [a^{p-2}]_p = [a^{p-1}]_p = [1]_p,$$
also ist $[a^{p-2}]_p$ das Inverse zu $[a]_p$.

:::rechnung Inverses von $[3]$ in $\mathbb{Z}/7\mathbb{Z}$ (Bsp. 3.70 analog)
3^{5} = 243 || $a^{p-2}$ mit $p = 7$: $3^5$
243 - 34 \cdot 7 = 5 || $243 = 34 \cdot 7 + 5$: also $[3]^{-1} = [5]$
(3 \cdot 5) \bmod 7 = 1 || Probe: $15 = 2 \cdot 7 + 1$
:::

Beispiel 3.70: In $\mathbb{Z}/5\mathbb{Z}$ sind $[1]^{-1} = [1]$, $[2]^{-1} = [3]$, $[3]^{-1} = [2]$, $[4]^{-1} = [4]$. In $\mathbb{Z}/4\mathbb{Z}$ hat $[2]$ kein Inverses.

:::alt Als Zifferblatt
Auf einer Uhr mit Primzahl-Anzahl an Plätzen führt jeder Sprung der Weite $a$ (ohne $0$) irgendwann auf jeden Platz. Insbesondere auch auf $1$: Das ist das Inverse. Bei zusammengesetzten Zahlen bleibt man in Teilkreisen hängen.
:::
""")

k.ordnen("Ordne den Beweis von Satz 3.69, Richtung „$n$ prim $\\Rightarrow$ Körper“.",
         ["Sei $p$ eine Primzahl. Nach Satz 3.50 ist $\\mathbb{Z}/p\\mathbb{Z}$ ein kommutativer Ring mit Eins, und $[0]_p \\ne [1]_p$ wegen $p \\nmid 1$.",
          "Sei $[a]_p \\ne [0]_p$ mit $a \\in \\{1, \\ldots, p-1\\}$. Dann gilt $p \\nmid a$.",
          "Nach dem kleinen Satz von Fermat (Satz 2.67) ist $a^{p-1} \\bmod p = 1$.",
          "Damit $[a]_p \\cdot [a^{p-2}]_p = [a^{p-1}]_p = [1]_p$ nach Definition 3.49.",
          "Also hat jedes $[a]_p \\ne [0]_p$ ein multiplikatives Inverses, und $\\mathbb{Z}/p\\mathbb{Z}$ ist ein Körper."],
         "Der Ring ist schon bekannt, es bleiben nur die Inversen. Fermat liefert sie sogar explizit: $[a]^{-1} = [a^{p-2}]$.",
         ablenker=["Da $p$ ungerade ist, ist jedes Element durch $2$ teilbar.", "Wegen $a^{p-1} = 0$ folgt $[a] \\cdot [a^{p-2}] = [0]$."],
         tipps=["Was braucht man zusätzlich zu „kommutativer Ring mit Eins“, damit es ein Körper ist?", "Fermat benötigt $p \\nmid a$.", "Die Potenz $a^{p-2}$ ist das Inverse."])

k.zahl("Bestimme das multiplikative Inverse von $[3]_7$ in $\\mathbb{Z}/7\\mathbb{Z}$, als Vertreter $r \\in \\{1, \\ldots, 6\\}$.", 5,
       "$3 \\cdot 5 = 15 = 2 \\cdot 7 + 1$, also $[3]^{-1} = [5]$. Mit Fermat: $3^{5} = 243 \\equiv 5$.",
       tipps=["Suche $b$ mit $3b \\equiv 1 \\pmod 7$.", "Probiere $b = 1, \\ldots, 6$ oder rechne $3^{7-2} \\bmod 7$.", "$3 \\cdot 5 = 15 \\equiv 1$."],
       rechenweg=rechnung([("3 \\cdot 5 = 15", "$15 = 2 \\cdot 7 + 1$"), ("(3 \\cdot 5) \\bmod 7 = 1", "also $[3]_7^{-1} = [5]_7$")]),
       typische_fehler=[(4, "Das ist das **additive** Inverse $-3 \\equiv 4$. Gesucht ist das multiplikative: $3 \\cdot b \\equiv 1$."),
                        (3, "$3 \\cdot 3 = 9 \\equiv 2 \\ne 1$: $[3]$ ist nicht selbstinvers modulo $7$.")])

# ── Seite 9: Körperhomomorphismen ───────────────────────────────────────
k.erklaerung("Körperhomomorphismen", r"""
## Ohne Informationsverlust

**Definition 3.71.** Ein [[Körperhomomorphismus]] ist ein Ringhomomorphismus zwischen zwei Körpern. Bijektiv: Körperisomorphismus.

**Satz 3.73.** Jeder Körperhomomorphismus ist injektiv.

*Beweis.* Aus $f(c) = 0_L$ und $c \ne 0_K$ folgte $1_L = f(c c^{-1}) = f(c)f(c^{-1}) = 0_L$, ein Widerspruch. Also $\ker = \{0\}$, und $f$ ist injektiv (Satz 3.42 für $+$).

**Satz 3.72.** Jeder Körperhomomorphismus $f\colon \mathbb{Q} \to \mathbb{Q}$ ist die Identität.

*Beweis.* $f(1) = 1$, $f(n) = f(1 + \cdots + 1) = n$, $f(0) = 0$, $f(-n) = -n$. Für $q = \frac ab$: $b\,f(q) = f(b)f(q) = f(bq) = f(a) = a$. Satz 3.67 gibt $f(q) = \frac ab = q$.

:::rechnung Satz 3.72 für $q = \frac34$
1 + 1 + 1 = 3 || $f(3) = f(1) + f(1) + f(1) = 3$
4 \cdot x = 3 || $x := f(\frac34)$ erfüllt $4x = f(4)f(\frac34) = f(3) = 3$
x = 3/4 || Satz 3.67: eindeutige Lösung, also $f(\frac34) = \frac34$
:::

**Beobachtung 3.74, Satz 3.75 (Übung):** Der Körperhomomorphismus induziert Gruppenhomomorphismen $(K, +) \to (L, \oplus)$ und $(K \setminus \{0\}, \cdot) \to (L \setminus \{0\}, \star)$; das Bild $f(K)$ ist ein Körper.

:::alt Als Einbettung
Ein Körperhomomorphismus steckt einen Körper unverändert in einen größeren. Man kann $K$ mit seinem Bild $f(K) \subseteq L$ gleichsetzen: So steckt $\mathbb{Q}$ in $\mathbb{R}$ und $\mathbb{R}$ in $\mathbb{C}$.
:::
""")

k.ordnen("Ordne den Beweis von Satz 3.72: Jeder Körperhomomorphismus $f\\colon \\mathbb{Q} \\to \\mathbb{Q}$ ist die Identität.",
         ["Es gilt $f(1) = 1$ (Ringhomomorphismus) und $f(0) = 0$ (Satz 3.38 (i)).",
          "Für $n \\in \\mathbb{N}\\setminus\\{0\\}$ ist $f(n) = f(1 + \\cdots + 1) = f(1) + \\cdots + f(1) = n$.",
          "Aus $0 = f(n + (-n)) = f(n) + f(-n)$ folgt $f(-n) = -n$. Also $f(a) = a$ für alle $a \\in \\mathbb{Z}$.",
          "Für $q = \\frac ab$ gilt $b\\,f(q) = f(b)f(q) = f(bq) = f(a) = a$.",
          "Nach Satz 3.67 hat $bx = a$ genau eine Lösung, nämlich $\\frac ab$. Also $f(q) = q$."],
         "Erst $\\mathbb{Z}$ (Zählen mit $f(1) = 1$), dann $\\mathbb{Q}$ (Satz 3.67: eindeutige Lösung von $bx = a$).",
         ablenker=["Da $f$ surjektiv ist, ist $f$ die Identität.", "Für $q = \\frac ab$ ist $f(q) = \\frac{f(a)}{f(b)} = \\frac ab$ nach Definition der Division."],
         tipps=["Beginne mit den Zahlen $0$ und $1$, dann $n$, dann negativen Zahlen.", "Für Brüche brauchst du nur $b\\,f(q) = a$ und die Eindeutigkeit der Lösung.", "Satz 3.67 in einem Körper."])

k.wf("Es gibt einen Körperhomomorphismus $f\\colon \\mathbb{Z}/5\\mathbb{Z} \\to \\mathbb{Z}/7\\mathbb{Z}$.", False,
     "Satz 3.73: $f$ wäre injektiv, also hätte das Bild fünf Elemente. Aber $f(1 + 1 + 1 + 1 + 1) = 5 \\cdot 1 = [5]_7 \\ne [0]_7$, während $1 + 1 + 1 + 1 + 1 = [0]_5$ und $f([0]) = [0]$ ist. Widerspruch.",
     tipps=["Wende $f$ auf $1 + 1 + 1 + 1 + 1 = 0$ in $\\mathbb{Z}/5\\mathbb{Z}$ an."])

# ── Seite 10: Angeordnete Körper ─────────────────────────────────────────
k.erklaerung("Angeordnete Körper", r"""
## Ordnung, die mit Rechnen verträglich ist

**Definition 3.76.** Ein Körper $(K, +, \cdot)$ mit einer [[Totalordnung]] $\le$ heißt **angeordnet**, falls für alle $a, b, c$:
$$a \le b \Rightarrow a + c \le b + c, \qquad a \le b \text{ und } 0_K \le c \Rightarrow ac \le bc.$$

**Beispiel 3.77.** $(\mathbb{Q}, +, \cdot, \le)$ ist ein angeordneter Körper.

**Satz 3.78.** In einem angeordneten Körper gilt (i) $a > 0 \Rightarrow -a < 0$ und (ii) $a^2 \ge 0$ für alle $a$, insbesondere $1 > 0$.

*Beweis (ii).* Ist $0 \le a$: $0 = 0 \cdot a \le a \cdot a$. Ist $a \le 0$: $0 \le -a$, also $0 \le (-a)^2 = a^2$. Wegen $1 = 1^2 \ge 0$ und $1 \ne 0$ ist $1 > 0$.

**Definition 3.79.** Ein Körperhomomorphismus zwischen angeordneten Körpern ist ordnungserhaltend, falls $a \le b \Rightarrow f(a) \le f(b)$.

:::rechnung Satz 3.78 in $\mathbb{Q}$ mit $a = -\frac12$
-1/2 \cdot (-1/2) = 1/4 || $a^2 = (-a)^2 = \frac14 \ge 0$
1 = 1 \cdot 1 || $1 = 1^2 \ge 0$ und $1 \ne 0$, also $1 > 0$
:::

:::achtung Nicht jeder Körper lässt sich anordnen
In $\mathbb{Z}/5\mathbb{Z}$ gilt $[1] + [1] + [1] + [1] + [1] = [0]$, aber in einem angeordneten Körper wäre $1 > 0$ und damit $1 + \cdots + 1 > 0$. Auch $\mathbb{C}$ lässt sich nicht anordnen (nächstes Kapitel).
:::

:::alt Als Zahlengerade
Eine Anordnung erlaubt, Zahlen auf einer Geraden zu sortieren, und Verschieben (plus $c$) und Strecken mit positivem Faktor ändern die Reihenfolge nicht. Bei Quadraten ist das Ergebnis immer rechts von der $0$.
:::
""")

k.mc("Welche Aussage gilt in **jedem** angeordneten Körper $(K, +, \\cdot, \\le)$?",
     ["$a^2 \\ge 0$ für alle $a \\in K$", "$a^2 > 0$ für alle $a \\in K$", "Es gibt ein $a$ mit $a^2 = -1$", "$1 + 1 = 0$"],
     "Satz 3.78 (ii): $a^2 \\ge 0$. Für $a = 0$ ist $a^2 = 0$, nicht $> 0$. $a^2 = -1$ ist unmöglich (sonst $-1 \\ge 0$ und $1 > 0$ zugleich). $1 + 1 = 0$ widerspricht $1 > 0$ (Satz 3.78).",
     tipps=["Satz 3.78 nennt zwei Eigenschaften.", "Teste $a = 0$ in der zweiten Aussage."],
     fehler={"$a^2 > 0$ für alle $a \\in K$": "Für $a = 0$ ist $a^2 = 0$.",
             "Es gibt ein $a$ mit $a^2 = -1$": "Dann wäre $-1 = a^2 \\ge 0$, aber $1 > 0$ und somit $-1 < 0$ (Satz 3.78 (i)): Widerspruch.",
             "$1 + 1 = 0$": "In einem angeordneten Körper ist $1 > 0$, also $1 + 1 > 0$."})

k.praxis()


def restklasse_mal(rng):
    n = rng.choice([6, 7, 8, 9, 10, 11, 12, 15])
    a, b = rng.randint(2, n - 1), rng.randint(2, n - 1)
    while a * b < n:
        a, b = rng.randint(2, n - 1), rng.randint(2, n - 1)
    w = (a * b) % n
    falsch = [(a * b, f"Du hast nicht modulo ${n}$ reduziert. Der Vertreter liegt in $\\{{0, \\ldots, {n - 1}\\}}$."),
              ((a + b) % n, "Das ist die Summe $[a] + [b]$. Gefragt ist das Produkt.")]
    zeilen = [(f"{a} \\cdot {b} = {a * b}", f"$[{a}]_{{{n}}} \\cdot [{b}]_{{{n}}} = [{a * b}]_{{{n}}}$"),
              (f"({a} \\cdot {b}) \\bmod {n} = {w}", f"${a * b} = {a * b // n} \\cdot {n} + {w}$")]
    extra = " (Beachte: Das Produkt kann $[0]$ sein, obwohl beide Faktoren $\\ne [0]$ sind.)" if w == 0 else ""
    return {"frage": f"Berechne $[{a}]_{{{n}}} \\cdot [{b}]_{{{n}}}$ in $\\mathbb{{Z}}/{n}\\mathbb{{Z}}$ und gib den Vertreter $r \\in \\{{0, \\ldots, {n - 1}\\}}$ an.{extra}",
            "loesung": w,
            "tipps": ["Multipliziere $a$ und $b$ in $\\mathbb{Z}$.", f"Teile durch ${n}$ mit Rest.", f"${a * b} = {a * b // n} \\cdot {n} + {w}$."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Nach Definition 3.49 gilt $[a]_n \\cdot [b]_n = [ab]_n$. Danach reduzierst du modulo $n$.",
            "typische_fehler": ohne_gleiche(w, falsch)}


def nullteiler_finden(rng):
    n = rng.choice([6, 8, 9, 10, 12, 14, 15, 16, 18, 20])
    N = nullteiler(n)
    teiler = {d for d in range(2, n) if n % d == 0}
    falsch = [(mtext(teiler), "Das sind nur die echten Teiler von $n$. Auch Vielfache davon (mit $a \\cdot b \\equiv 0$) sind Nullteiler."),
              (mtext(N | {0}), "$0$ ist nach Definition 3.52 kein Nullteiler ($a \\in R \\setminus \\{0\\}$)."),
              (mtext(set(range(1, n))), "Nicht jedes Element ist Nullteiler: Prüfe zum Beispiel $[1]$.")]
    a0 = min(N)
    b0 = next(b for b in range(1, n) if (a0 * b) % n == 0)
    zeilen = [(f"{a0} \\cdot {b0} = {a0 * b0}", f"$[{a0}] \\cdot [{b0}] = [{a0 * b0}] = [0]$ mit $[{a0}], [{b0}] \\ne [0]$: $[{a0}]$ ist Nullteiler")]
    return {"frage": f"Bestimme alle Nullteiler von $\\mathbb{{Z}}/{n}\\mathbb{{Z}}$ als Menge der Vertreter $r \\in \\{{1, \\ldots, {n - 1}\\}}$, zum Beispiel `{{2; 3}}`.",
            "loesung": mtext(N),
            "tipps": ["$a$ ist Nullteiler, wenn es $b \\ne 0$ mit $ab \\equiv 0 \\pmod n$ gibt.", f"Faktorisiere ${n}$: Elemente mit gemeinsamem Teiler mit ${n}$ sind Kandidaten.",
                      "Genau die $a$ mit $\\operatorname{ggT}(a, n) > 1$ sind Nullteiler."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "In $\\mathbb{Z}/n\\mathbb{Z}$ ist $[a] \\ne [0]$ genau dann Nullteiler, wenn $\\operatorname{ggT}(a, n) > 1$ (sonst hat es ein Inverses).",
            "typische_fehler": ohne_gleiche(mtext(N), falsch)}


assert all(nullteiler(n) == {a for a in range(1, n) if gcd(a, n) > 1} for n in range(2, 40))


def inverse_modp(rng):
    p = rng.choice([7, 11, 13])
    a = rng.randint(2, p - 2)
    while inv_mod(a, p) == a or inv_mod(a, p) == (-a) % p:
        a = rng.randint(2, p - 2)
    w = inv_mod(a, p)
    falsch = [((-a) % p, "Das ist das **additive** Inverse $-a \\bmod p$. Gesucht ist das multiplikative: $a \\cdot b \\equiv 1$."),
              (a, f"${a} \\cdot {a} = {a * a} \\equiv {(a * a) % p} \\ne 1$: $[a]$ ist nicht selbstinvers."),
              (pow(a, p - 1, p), "$a^{p-1} \\equiv 1$ ist der Fermat-Wert. Das Inverse ist $a^{p-2}$.")]
    return {"frage": f"Bestimme das multiplikative Inverse von $[{a}]_{{{p}}}$ im Körper $\\mathbb{{Z}}/{p}\\mathbb{{Z}}$ als Vertreter $r \\in \\{{1, \\ldots, {p - 1}\\}}$.",
            "loesung": w,
            "tipps": [f"Gesucht ist $b$ mit ${a} \\cdot b \\equiv 1 \\pmod{{{p}}}$.", f"Probiere $b = 1, 2, \\ldots$ oder rechne ${a}^{{{p - 2}}} \\bmod {p}$ (Fermat).", f"${a} \\cdot {w} = {a * w} = {a * w // p} \\cdot {p} + 1$."],
            "rechenweg": rechnung([(f"{a} \\cdot {w} = {a * w}", f"$[{a}] \\cdot [{w}] = [{a * w}]$"), (f"({a} \\cdot {w}) \\bmod {p} = 1", f"also $[{a}]_{{{p}}}^{{-1}} = [{w}]_{{{p}}}$")]),
            "erklaerung": f"In $\\mathbb{{Z}}/{p}\\mathbb{{Z}}$ ist $[a]^{{-1}} = [a^{{{p - 2}}}]$ (Satz 3.69, Fermat). Man kann auch kleine Werte durchprobieren.",
            "typische_fehler": ohne_gleiche(w, falsch)}


def rationale_paare(rng):
    op = rng.choice(["+", "*", ":"])
    while True:
        p = (rng.randint(-5, 5), rng.randint(2, 6))
        q = (rng.randint(-5, 5), rng.randint(2, 6))
        if p[0] != 0 and q[0] != 0 and gcd(abs(p[0]), p[1]) == 1 and gcd(abs(q[0]), q[1]) == 1 and p[1] != q[1]:
            break
    if op == "+":
        r = p_add(p, q)
        formel = f"({p[0]} \\cdot {q[1]} + {p[1]} \\cdot {q[0]},\\ {p[1]} \\cdot {q[1]})"
        regel = "Definition 3.61 (i): $(ad + bc,\\ bd)$"
        falsch = [(F(p[0] + q[0], p[1] + q[1]), "Das ist komponentenweise addiert. Richtig ist $(ad + bc,\\ bd)$.")]
    elif op == "*":
        r = p_mul(p, q)
        formel = f"({p[0]} \\cdot {q[0]},\\ {p[1]} \\cdot {q[1]})"
        regel = "Definition 3.61 (iii): $(ac,\\ bd)$"
        falsch = [(F(p[0] * q[1] + p[1] * q[0], p[1] * q[1]), "Das ist die Summe. Gefragt ist das Produkt.")]
    else:
        r = p_div(p, q)
        formel = f"({p[0]} \\cdot {q[1]},\\ {p[1]} \\cdot {q[0]})" if q[0] > 0 else f"(-{p[0]} \\cdot {q[1]},\\ -{p[1]} \\cdot ({q[0]}))"
        regel = "Definition 3.61 (iv): $(ad,\\ bc)$ für $c > 0$, sonst $(-ad,\\ -bc)$"
        falsch = [(F(p[0] * q[0], p[1] * q[1]), "Das ist das Produkt. Beim Dividieren muss das zweite Paar umgedreht werden."),
                  (F(p[0] * q[1], p[1] * q[0]) * -1, "Das Vorzeichen ist falsch. Bei $c < 0$ rutscht das Minus in die erste Zahl: $(-ad,\\ -bc)$.")]
    w = F(*r)
    if not ohne_gleiche(w, falsch):
        return rationale_paare(rng)
    symb = {"+": "+", "*": "\\cdot", ":": ":"}[op]
    zeilen = [(f"{formel} = ({r[0]}, {r[1]})", regel), (f"{r[0]}/{r[1]} = {w}", "gekürzt")]
    return {"frage": f"Berechne mit den Regeln aus Definition 3.61: $[({p[0]}, {p[1]})] {symb} [({q[0]}, {q[1]})]$. Gib den Wert als gekürzten Bruch an.",
            "loesung": w, "gekuerzt": True,
            "tipps": [f"Welche Regel passt? ({regel})", f"Das Ergebnispaar ist $({r[0]}, {r[1]})$.", "Kürze den Bruch am Ende. Paare, die denselben Bruch beschreiben, sind gleich."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": f"Die Rechenregeln auf Paaren (Def. 3.61) liefern dieselben Werte wie die Bruchrechnung: ${p[0]}/{p[1]} {symb} {q[0]}/{q[1]} = {w}$.",
            "typische_fehler": ohne_gleiche(w, falsch)}


k.generator(restklasse_mal, typ="zahl", titel="Multiplizieren in Z/nZ")
k.generator(nullteiler_finden, typ="menge", titel="Nullteiler in Z/nZ finden")
k.generator(inverse_modp, typ="zahl", titel="Inverse in Z/pZ")
k.generator(rationale_paare, typ="zahl", titel="Rechnen mit Paaren: ℚ")

k.rechenweg_aufgabe(r"""
## Quiz-Stil: Der Ring $\mathbb{Z}/8\mathbb{Z}$

Betrachten Sie den Restklassenring $\mathbb{Z}/8\mathbb{Z}$ (Vertreter ohne Index).
""",
    [{"typ": "zahl", "frage": "Berechnen Sie $[3] \\cdot [5]$ als Vertreter $r \\in \\{0, \\ldots, 7\\}$.", "loesung": 7,
      "tipps": ["$3 \\cdot 5 = 15$.", "$15 = 1 \\cdot 8 + 7$."], "rechenweg": ":::rechnung\n(3 \\cdot 5) \\bmod 8 = 7 || $15 = 8 + 7$\n:::",
      "erklaerung": "$[3] \\cdot [5] = [15] = [7]$."},
     {"typ": "mc", "frage": "Ist $[4]$ ein Nullteiler?", "optionen": ["Ja: $[4] \\cdot [2] = [0]$ mit $[2] \\ne [0]$", "Nein: $[4] \\ne [0]$", "Nein: $4 \\nmid 8$"],
      "fehler": {"Nein: $[4] \\ne [0]$": "Nullteiler sind gerade Elemente $\\ne 0$ mit einem Partner $\\ne 0$ und Produkt $0$.",
                 "Nein: $4 \\nmid 8$": "$4 \\mid 8$, und genau deshalb $[4] \\cdot [2] = [8] = [0]$."},
      "tipps": ["Suche $b \\ne [0]$ mit $4b \\equiv 0 \\pmod 8$.", "$b = 2$: $4 \\cdot 2 = 8$."], "erklaerung": "$4 \\cdot 2 = 8 \\equiv 0$."},
     {"typ": "menge", "frage": "Bestimmen Sie alle Elemente von $\\{1, \\ldots, 7\\}$, die in $\\mathbb{Z}/8\\mathbb{Z}$ ein multiplikatives Inverses haben (Vertreter).", "loesung": "{1; 3; 5; 7}",
      "tipps": ["Ungerade $a$ haben $\\operatorname{ggT}(a, 8) = 1$.", "Prüfe $3 \\cdot 3 = 9 \\equiv 1$."], "rechenweg": ":::rechnung\n(3 \\cdot 3) \\bmod 8 = 1 || $[3]^{-1} = [3]$\n(5 \\cdot 5) \\bmod 8 = 1 || $[5]^{-1} = [5]$\n:::",
      "erklaerung": "Genau die zu $8$ teilerfremden $a$ sind invertierbar: $1, 3, 5, 7$. Die geraden Zahlen sind Nullteiler.",
      "typische_fehler": [("{1; 2; 3; 4; 5; 6; 7}", "Gerade Zahlen haben kein Inverses: $2b$ ist immer gerade, also $\\ne 1 \\bmod 8$.")]}],
    "Im Ring $\\mathbb{Z}/8\\mathbb{Z}$ sind genau die ungeraden Elemente invertierbar. Er ist kein Körper, denn $8$ ist keine Primzahl.",
    uebungsblatt=True,
    tipps=["Reduzieren Sie jedes Produkt modulo $8$.", "Ein Element ist invertierbar, wenn es zu $8$ teilerfremd ist."],
    rechenweg=r"""
:::rechnung
3 \cdot 5 = 15 || Produkt
4 \cdot 2 = 8 || $[4][2] = [0]$
3 \cdot 3 = 9 || $9 = 8 + 1$
:::
""")

k.wf("In einem Körper gilt: Aus $ab = ac$ und $a \\ne 0$ folgt $b = c$.", True,
     "Ein Körper hat keine Nullteiler (Beobachtung 3.66), also ist $M_a$ injektiv (Satz 3.53): Kürzen ist erlaubt. Alternativ: Multipliziere mit $a^{-1}$.",
     tipps=["Multipliziere beide Seiten mit $a^{-1}$."])

k.wf("Der Ring $(\\mathbb{Z}/6\\mathbb{Z}, +, \\cdot)$ erfüllt die Kürzungsregel „$ab = ac$ und $a \\ne 0$ $\\Rightarrow b = c$“.", False,
     "$[2] \\cdot [1] = [2]$ und $[2] \\cdot [4] = [8] = [2]$, aber $[1] \\ne [4]$. Das passt zu Satz 3.53: $[2]$ ist Nullteiler, also ist $M_{[2]}$ nicht injektiv.",
     tipps=["Suche $a \\ne 0$ und zwei verschiedene $b, c$ mit demselben Produkt $ab$."])

k.papier(r"""
## Übungsblatt-Stil: Satz 3.53

Sei $(R, +, \cdot)$ ein kommutativer Ring und $a \in R \setminus \{0\}$. Zeigen Sie: $a$ ist genau dann kein Nullteiler, wenn $M_a\colon R \to R,\ x \mapsto ax$ injektiv ist.
""",
    r"""
„$\Rightarrow$“: Sei $a$ kein Nullteiler und $M_a(b) = M_a(c)$, also $ab = ac$. Dann $a(b - c) = ab - ac = 0$ (Distributivität und Satz 3.48). Da $a \ne 0$ kein Nullteiler ist, folgt $b - c = 0$, also $b = c$. Somit ist $M_a$ injektiv.
„$\Leftarrow$“: Sei $M_a$ injektiv und $b \in R$ mit $ab = 0$. Wegen Satz 3.48 ist $M_a(0) = a0 = 0 = ab = M_a(b)$. Aus der Injektivität folgt $b = 0$. Es gibt also kein $b \ne 0$ mit $ab = 0$: $a$ ist kein Nullteiler. $\square$
""",
    ["Richtung „$\\Rightarrow$“: aus $ab = ac$ wurde $a(b - c) = 0$ gebildet",
     "Danach die Nullteilerfreiheit von $a$ auf $b - c$ angewendet",
     "Richtung „$\\Leftarrow$“: $a0 = 0$ (Satz 3.48) als zweites Urbild von $0$ benutzt",
     "Aus der Injektivität $b = 0$ geschlossen"],
    "Nullteiler und Injektivität von $x \\mapsto ax$ sind dieselbe Eigenschaft, zweimal beschrieben. Das erklärt, warum Kürzen nur ohne Nullteiler funktioniert.",
    uebungsblatt=True,
    tipps=["Für „$\\Rightarrow$“ bringst du $ab = ac$ in die Form $a \\cdot (\\ldots) = 0$.", "Für „$\\Leftarrow$“ brauchst du zwei Elemente mit demselben Bild unter $M_a$: Welche?"])

k.papier(r"""
## Übungsblatt-Stil: Satz 3.59 (Bild eines Ringhomomorphismus)

Sei $f\colon R \to S$ ein Ringhomomorphismus zwischen Ringen mit Eins. Zeigen Sie: $f(R)$ ist mit den eingeschränkten Verknüpfungen ein Ring mit Einselement $1_S$.
""",
    r"""
Nach Beobachtung 3.57 ist $f$ ein Gruppenhomomorphismus für $+$. Nach Satz 3.38 (iii) ist $(f(R), \oplus)$ eine Untergruppe von $(S, \oplus)$, und nach Satz 3.38 (iv) abelsch.
Abgeschlossenheit unter $\star$: $f(a) \star f(b) = f(a \cdot b) \in f(R)$. Assoziativität (m) und Distributivität (d) übertragen sich von $S$ auf die Teilmenge $f(R)$.
Einselement: $1_S = f(1_R) \in f(R)$ und $1_S \star x = x \star 1_S = x$ für alle $x \in f(R)$. $\square$
""",
    ["Additive Gruppe über Satz 3.38 (iii) und (iv) begründet",
     "Abgeschlossenheit unter der Multiplikation über die Homomorphieeigenschaft gezeigt",
     "Assoziativität und Distributivität als vererbt erkannt",
     "$1_S = f(1_R) \\in f(R)$ als Einselement benannt"],
    "Das Bild eines Homomorphismus hat dieselbe Art von Struktur wie der Definitionsbereich. Das nutzt du später wieder, etwa bei Körpern (Satz 3.75).",
    uebungsblatt=True,
    tipps=["Prüfe die Ringaxiome (g), (m), (d) und die Eins einzeln.", "Elemente von $f(R)$ haben die Form $f(a)$."])

k.papier(r"""
## Übungsblatt-Stil: Satz 3.75 (Bild eines Körperhomomorphismus)

Sei $f\colon K \to L$ ein Körperhomomorphismus. Zeigen Sie: $f(K)$ ist mit den eingeschränkten Verknüpfungen ein Körper. (Hinweis: Satz 3.59 und Beobachtung 3.74.)
""",
    r"""
Nach Satz 3.59 ist $f(K)$ ein Ring mit Einselement $1_L$, kommutativ, da $K$ es ist (Satz 3.38 (iv) analog für $\cdot$). Sei $y = f(a) \in f(K)$ mit $y \ne 0_L$. Dann ist $a \ne 0_K$ (denn $f(0_K) = 0_L$), also existiert $a^{-1}$.
Es gilt $y \star f(a^{-1}) = f(a \cdot a^{-1}) = f(1_K) = 1_L$ und $f(a^{-1}) \in f(K)$. Also hat jedes $y \ne 0_L$ in $f(K)$ ein Inverses, und $f(K)$ ist ein Körper. $\square$
""",
    ["Ring mit Eins und Kommutativität des Bildes begründet",
     "Für $y = f(a) \\ne 0_L$ gefolgert, dass $a \\ne 0_K$",
     "Das Inverse $f(a^{-1})$ angegeben und die Rechnung $f(a)f(a^{-1}) = 1_L$ gezeigt"],
    "Das Bild eines Körperhomomorphismus ist ein Körper, der in $L$ liegt: So steckt $\\mathbb{Q}$ in $\\mathbb{R}$.",
    tipps=["Welches Element ist das Inverse von $f(a)$?"])

k.zusammenfassung(r"""
## Ringe, Körper und ℚ (Skript Abschn. 3.3 bis 3.5, Def. 3.46 bis 3.79)

- **Ring** (Def. 3.46): $(R, +, \cdot)$ mit (g) $(R, +)$ abelsche Gruppe, (m) $\cdot$ assoziativ, (d) Distributivität. Mit Eins, kommutativ. $(\mathbb{Z}, +, \cdot)$ ja, $\mathbb{N}$ nein. **Satz 3.48:** $0a = 0$, $(-a)b = -(ab)$, $(-a)(-b) = ab$.
- **Restklassenring** (Def. 3.49, Satz 3.50): $[a]_n \cdot [b]_n = [ab]_n$, kommutativer Ring mit $[0]_n, [1]_n$. Tafeln für $n = 4, 5$ (Bsp. 3.51).
- **Nullteiler** (Def. 3.52): $a \ne 0$ mit $ab = 0$ für ein $b \ne 0$. **Satz 3.53:** $a$ kein Nullteiler $\iff x \mapsto ax$ injektiv. **Satz 3.54:** $n > 1$ nicht prim $\Rightarrow$ Nullteiler in $\mathbb{Z}/n\mathbb{Z}$.
- **Ringhomomorphismus** (Def. 3.55): $f(a + b)$, $f(ab)$, $f(1_R) = 1_S$. $\pi_n\colon \mathbb{Z} \to \mathbb{Z}/n\mathbb{Z}$ (Bsp. 3.58). Bild ist Ring (Satz 3.59).
- **$\mathbb{Q}$** (Def. 3.60, 3.61): Paare $(a, b)$, $(a, b) \sim (c, d) \iff ad = bc$; $[(a, b)] + [(c, d)] = [(ad + bc,\ bd)]$, $\cdot = [(ac,\ bd)]$.
- **Körper** (Def. 3.64): kommutativer Ring mit Eins, $(K \setminus \{0\}, \cdot)$ Gruppe. Keine Nullteiler, $0 \ne 1$ (Beob. 3.66). $ax = b$ hat $x = a^{-1}b$ (Satz 3.67).
- **Satz 3.69:** $\mathbb{Z}/n\mathbb{Z}$ Körper $\iff$ $n$ prim ($[a]^{-1} = [a^{p-2}]$ nach Fermat).
- **Körperhomomorphismus** (Def. 3.71): immer injektiv (Satz 3.73); $\mathbb{Q} \to \mathbb{Q}$ ist die Identität (Satz 3.72).
- **Angeordneter Körper** (Def. 3.76): Totalordnung, $a \le b \Rightarrow a + c \le b + c$, $0 \le c \Rightarrow ac \le bc$. Satz 3.78: $a^2 \ge 0$, $1 > 0$.

!! Kürzen ($ab = ac \Rightarrow b = c$) geht nur ohne Nullteiler, und Dividieren geht nur im Körper.
""")
