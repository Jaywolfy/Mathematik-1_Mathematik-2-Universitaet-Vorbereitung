# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 21: Vektorräume und Untervektorräume (Skript Disser WS 26/27, Abschn. 4.2 und 4.3, Def. 4.23 bis Bsp. 4.46)."""
from fractions import Fraction as F
from itertools import product

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(
    slug="vektorraeume",
    titel="Vektorräume und Untervektorräume",
    beschreibung="Vektorraumaxiome, Kⁿ, Polynome, Funktionenräume, Unterraumkriterium, Linearkombination, lineare Hülle",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 4.2 und 4.3",
    icon="🧱")

sp, vt, tx = mathlib.skalarprodukt, mathlib.tex_vektor, mathlib.tex


def rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def lin(coeffs, vs):
    """Linearkombination sum coeffs[j] * vs[j] (exakt)."""
    return [sum(F(c) * F(v[i]) for c, v in zip(coeffs, vs)) for i in range(len(vs[0]))]


def poly_tex(c):
    """[a0, a1, a2, ...] -> a0 + a1 X + a2 X^2 als LaTeX."""
    teile = []
    for j, a in enumerate(c):
        a = F(a)
        if a == 0:
            continue
        mon = "" if j == 0 else ("X" if j == 1 else f"X^{{{j}}}")
        betrag = tx(abs(a))
        if mon and abs(a) == 1:
            betrag = ""
        t = betrag + mon
        teile.append(("-" if a < 0 else "+", t))
    if not teile:
        return "0"
    erste = teile[0]
    s = ("-" if erste[0] == "-" else "") + erste[1]
    for vz, t in teile[1:]:
        s += f" {vz} {t}"
    return s


# ── Beispiele des Skripts nachrechnen ────────────────────────────────────
# Beispiel 4.26: (1 + X) + (2 - X + X^2) = 3 + X^2 und 2(1 + X) = 2 + 2X in R[X]
assert lin([1, 1], [[1, 1, 0], [2, -1, 1]]) == [3, 0, 1] and lin([2], [[1, 1]]) == [2, 2]
# Beispiel 4.24: (Z/2Z)^3 ist abgeschlossen unter Addition mod 2
assert [(a + b) % 2 for a, b in zip((1, 0, 1), (1, 1, 0))] == [0, 1, 1]
# Beispiel 4.29: F = {t -> a + bt}; (f + g)(t) = (a + c) + (b + d)t
_f, _g = (1, 2), (3, -1)
assert all((_f[0] + _f[1] * t) + (_g[0] + _g[1] * t) == (_f[0] + _g[0]) + (_f[1] + _g[1]) * t for t in range(-5, 6))
# Beispiel 4.39: E1 ∩ E2 = <(1, -1, 1)>
_pts = [x for x in product(range(-4, 5), repeat=3) if x[0] + x[1] == 0 and x[1] + x[2] == 0]
assert all(x[1] == -x[0] and x[2] == x[0] for x in _pts) and len(_pts) == 9
# Beobachtung 4.40: die Vereinigung der Koordinatenachsen ist nicht abgeschlossen
assert (1, 0) in {(x, y) for x in range(-1, 2) for y in range(-1, 2) if x * y == 0}
assert (1 + 0, 0 + 1) not in {(x, y) for x in range(-1, 2) for y in range(-1, 2) if x * y == 0}
# Beispiel 4.43: ⟨e1, e2, e1 + e2⟩ = ⟨e1, e2⟩ in R^3: (a + c) e1 + (b + c) e2
assert lin([2, 3, 1], [[1, 0, 0], [0, 1, 0], [1, 1, 0]]) == lin([3, 4], [[1, 0, 0], [0, 1, 0]])

k.lernziele([
    "Ich kann die Vektorraumaxiome (Def. 4.23) nennen und an Beispielen prüfen: $K^n$, $K[X]$, Funktionenräume (Bsp. 4.24 bis 4.29)",
    "Ich weiß, warum $\\mathbb{Z}^2$ und Bildcodierungen keine reellen Vektorräume sind (Bsp. 4.27) und kenne die Rechenregeln aus Satz 4.30",
    "Ich kann mit dem Unterraumkriterium (Satz 4.32) entscheiden, ob eine Teilmenge ein Untervektorraum ist, und kenne Gegenbeispiele (Bsp. 4.36, Beob. 4.40)",
    "Ich kann Linearkombinationen bilden und die lineare Hülle $\\langle M \\rangle$ bestimmen (Def. 4.37, 4.41, Satz 4.42, Bsp. 4.43 bis 4.46)",
])

k.warum(r"""
Dieselben Rechenregeln gelten für Pfeile, Polynome, Funktionen und Bitstrings. Wer die Axiome kennt, muss einen Satz nur einmal
beweisen und darf ihn überall verwenden. Funktionenräume sind die Grundlage von Signalverarbeitung und Fourieranalyse.
Bitstrings mit XOR bilden einen Vektorraum über $\mathbb{Z}/2\mathbb{Z}$: So rechnen Fehlerkorrekturcodes (Hamming-Codes, QR-Codes).
Unterräume sind die „abgeschlossenen“ Teile: Lösungsmengen homogener Gleichungssysteme sind immer welche.
""")

# ── Seite 1: Axiome ──────────────────────────────────────────────────────
k.erklaerung("Die Vektorraumaxiome", r"""
## Definition 4.23

:::analogie 🍳 Rezepte mischen
Zutaten lassen sich mischen (addieren) und skalieren (die Menge verdoppeln). Dafür gelten Regeln: Reihenfolge beim Mischen egal,
doppelt mischen ist doppelt skalieren. Ein [[Vektorraum]] ist alles, was diese Regeln erfüllt, nicht nur Pfeile.
:::

Ein [[Vektorraum]] über einem Körper $K$ ist eine Menge $V \neq \emptyset$ mit einer Verknüpfung $+\colon V^2 \to V$ und einer Abbildung $\cdot\colon K \times V \to V$ mit:

- (g) $(V, +)$ ist eine abelsche Gruppe, Nullvektor $0_V$.
- (d1) $\lambda(v + w) = \lambda v + \lambda w$, (d2) $(\lambda + \mu)v = \lambda v + \mu v$.
- (a) $\lambda(\mu v) = (\lambda\mu)v$, (e) $1_K v = v$.

:::rechnung Distributivgesetze im $\mathbb{R}^2$ mit $\lambda = 2$, $\mu = 3$, $v = (1, 2)^\top$, $w = (0, 4)^\top$
2 \cdot (1 + 0) = 2 \cdot 1 + 2 \cdot 0 || (d1) erste Komponente von $\lambda(v + w)$
2 \cdot (2 + 4) = 2 \cdot 2 + 2 \cdot 4 || (d1) zweite Komponente
(2 + 3) \cdot 2 = 2 \cdot 2 + 3 \cdot 2 || (d2) zweite Komponente von $(\lambda + \mu)v$
2 \cdot (3 \cdot 2) = (2 \cdot 3) \cdot 2 || (a) zweite Komponente
:::

Die Elemente von $V$ heißen **Vektoren**, die von $K$ **Skalare**. Die Skalarmultiplikation verknüpft zwei verschiedenartige Objekte (Skalar und Vektor).

:::alt Als Spielregeln
Du hast zwei Züge: „zwei Dinge zusammenlegen“ und „ein Ding mit einer Zahl vergrößern“. Die Axiome sind die Spielregeln, die verhindern, dass sich
beides widerspricht. Erfüllt ein Spiel (Pfeile, Polynome, Funktionen) die Regeln, gelten alle Sätze dieses Kapitels automatisch.
:::
""")

k.mehrfach("Was verlangt Definition 4.23 von einem Vektorraum $(V, +, \\cdot)$ über $K$?",
           ["$(V, +)$ ist eine abelsche Gruppe", "$(\\lambda + \\mu)v = \\lambda v + \\mu v$ für alle $\\lambda, \\mu \\in K$ und $v \\in V$", "$1_K v = v$ für alle $v \\in V$"],
           ["Zwei Vektoren $v, w$ lassen sich zu einem Vektor $v \\cdot w$ multiplizieren", "Auf $V$ gibt es ein Skalarprodukt, das Längen misst"],
           "Verlangt sind (g), (d1), (d2), (a), (e). Ein Produkt zweier Vektoren oder ein Skalarprodukt gehört **nicht** zur Definition. Das Skalarprodukt kommt erst in Abschnitt 4.6 dazu.",
           tipps=["Zähle die Axiome (g), (d1), (d2), (a), (e) auf.", "Die Skalarmultiplikation verknüpft Skalar und Vektor, nicht zwei Vektoren."],
           fehler={"Zwei Vektoren $v, w$ lassen sich zu einem Vektor $v \\cdot w$ multiplizieren": "Ein Vektorraum kennt nur $+$ (Vektor mit Vektor) und $\\cdot$ (Skalar mit Vektor). Ein Vektorprodukt ist nicht Teil der Definition.",
                   "Auf $V$ gibt es ein Skalarprodukt, das Längen misst": "Längen und Skalarprodukte werden erst in Abschnitt 4.6 als zusätzliche Struktur eingeführt."})

# ── Seite 2: Beispiele Kⁿ, ℂ ─────────────────────────────────────────────
k.erklaerung("Beispiele: Kⁿ und ℂ", r"""
## Beispiele 4.24 und 4.25

Für jeden Körper $K$ ist $K^n$ mit komponentenweiser Rechnung ein Vektorraum über $K$ (Bsp. 4.24). Der Skalarkörper darf also wechseln:
$\mathbb{R}^n$, $\mathbb{Q}^n$ und $(\mathbb{Z}/2\mathbb{Z})^n$ (Bitstrings mit XOR, $1 + 1 = 0$).

Auch $\mathbb{C}$ ist ein Vektorraum, über $\mathbb{R}$ **und** über $\mathbb{C}$ (Bsp. 4.25). Die Vektoren sind dieselben komplexen Zahlen, aber
über $\mathbb{R}$ darfst du nur mit reellen Zahlen skalieren. $i$ ist in beiden Fällen ein Vektor, aber nur über $\mathbb{C}$ ein Skalar.

:::rechnung In $(\mathbb{Z}/2\mathbb{Z})^3$ (Rechnen mod $2$)
1 + 1 = 0 \text{ in } \mathbb{Z}/2\mathbb{Z} || erste Komponente von $(1, 0, 1)^\top + (1, 1, 0)^\top$
0 + 1 = 1 || zweite Komponente
1 + 0 = 1 || dritte Komponente: Summe $= (0, 1, 1)^\top$
:::

:::achtung Der Körper gehört zum Raum
„$\mathbb{C}$ ist ein Vektorraum“ ist unvollständig: Über $\mathbb{R}$ hat er (später) Dimension $2$, über $\mathbb{C}$ Dimension $1$.
:::

:::alt Als Zahlenschloss
Ein Zahlenschloss mit drei Bits ist ein Element von $(\mathbb{Z}/2\mathbb{Z})^3$: Zwei Schlösser überlagerst du Bit für Bit mit XOR. Skalieren gibt es nur mit $0$ (alles aus) und $1$ (unverändert).
:::
""")

k.mc("Welche dieser Mengen ist mit komponentenweiser Addition und der üblichen Skalarmultiplikation ein **reeller** Vektorraum?",
     ["$\\mathbb{R}^3$", "$\\mathbb{Z}^2$", "$(\\mathbb{Q} \\cap [0, 1])^N$ für $N \\ge 1$", "$\\mathbb{N}^2$"],
     "In $\\mathbb{Z}^2$ liegt $\\mathbf{e}^{(1)}$, aber $\\frac12\\mathbf{e}^{(1)} \\notin \\mathbb{Z}^2$ (Bsp. 4.27). Bei Bildcodierungen ist $\\mathbf{e}^{(1)}$ zulässig, aber $2\\mathbf{e}^{(1)}$ nicht. In $\\mathbb{N}^2$ fehlen additive Inverse. Nur $\\mathbb{R}^3$ ist abgeschlossen.",
     tipps=["Prüfe, ob das Ergebnis jeder Skalarmultiplikation mit $\\lambda \\in \\mathbb{R}$ wieder in der Menge liegt.", "Probiere $\\lambda = \\frac12$, $\\lambda = 2$ und $\\lambda = -1$."],
     fehler={"$\\mathbb{Z}^2$": "$\\mathbb{Z}^2$ ist zwar eine abelsche Gruppe, aber $\\frac12\\mathbf{e}^{(1)} \\notin \\mathbb{Z}^2$: nicht abgeschlossen unter reeller Skalarmultiplikation.",
             "$(\\mathbb{Q} \\cap [0, 1])^N$ für $N \\ge 1$": "$\\mathbf{e}^{(1)}$ ist erlaubt, $2\\mathbf{e}^{(1)}$ aber nicht (Eintrag $2 \\notin [0, 1]$). Außerdem $\\frac{\\sqrt 2}{2}\\mathbf{e}^{(1)}$ nicht rational.",
             "$\\mathbb{N}^2$": "Zu $(1, 0)^\\top$ gibt es kein additives Inverses in $\\mathbb{N}^2$, es ist nicht einmal eine Gruppe."})

k.vektor("Berechne in $(\\mathbb{Z}/2\\mathbb{Z})^3$ die Summe $(1, 0, 1)^\\top + (1, 1, 1)^\\top$. Gib die Einträge als $0$ oder $1$ an.",
         [0, 1, 0],
         "Komponentenweise mod $2$: $1 + 1 = 0$, $0 + 1 = 1$, $1 + 1 = 0$. Die Summe ist $(0, 1, 0)^\\top$.",
         tipps=["Rechne komponentenweise.", "In $\\mathbb{Z}/2\\mathbb{Z}$ gilt $1 + 1 = 0$.", "Erste Komponente: $1 + 1 = 0$."],
         rechenweg=rechnung([("1 + 1 = 2 \\equiv 0", "erste Komponente mod $2$"), ("0 + 1 = 1", "zweite Komponente"), ("1 + 1 = 2 \\equiv 0", "dritte Komponente mod $2$")]),
         typische_fehler=[([2, 1, 2], "Du hast nicht modulo $2$ gerechnet: In $\\mathbb{Z}/2\\mathbb{Z}$ ist $1 + 1 = 0$, die $2$ gibt es nicht."),
                          ([0, 1, 1], "Dritte Komponente: $1 + 1 = 0$ in $\\mathbb{Z}/2\\mathbb{Z}$.")])

# ── Seite 3: Polynome ────────────────────────────────────────────────────
k.erklaerung("Polynome als Vektoren", r"""
## Beispiele 4.26 und 4.27

$K[X]$ ist die Menge aller Polynome über $K$. Man addiert Koeffizienten gleicher Potenzen und multipliziert mit einem Skalar jeden Koeffizienten.
Fehlende Koeffizienten sind $0$. Der Nullvektor ist das Nullpolynom. Damit ist $K[X]$ ein Vektorraum über $K$ (Bsp. 4.26).

:::rechnung In $\mathbb{R}[X]$: $(1 + X) + (2 - X + X^2)$
1 + 2 = 3 || Koeffizient von $X^0$
1 + (-1) = 0 || Koeffizient von $X^1$: der Term verschwindet
0 + 1 = 1 || Koeffizient von $X^2$ (im ersten Polynom fehlt er): Ergebnis $3 + X^2$
2 \cdot 1 = 2 || $2(1 + X)$: Koeffizient von $X^0$ (dann $2 \cdot 1 = 2$ bei $X$): Ergebnis $2 + 2X$
:::

**Beispiel 4.27 (Gegenbeispiele):** $\mathbb{Z}^2$ ist mit $+$ eine abelsche Gruppe, aber kein reeller Vektorraum, denn $\mathbf{e}^{(1)} \in \mathbb{Z}^2$ und $\frac12\mathbf{e}^{(1)} \notin \mathbb{Z}^2$.
Auch Bildcodierungen $(\mathbb{Q} \cap [0, 1])^N$ sind keiner: $\mathbf{e}^{(1)}$ ist zulässig, $2\mathbf{e}^{(1)}$ nicht. Für die Rechnung betrachtet man sie im größeren Raum $\mathbb{R}^N$.

:::alt Als Koeffizientenvektor
Ein Polynom vom Grad $\le 2$ ist ein Vektor $(a_0, a_1, a_2)$, und Addition sowie Skalieren geschehen genau wie im $\mathbb{R}^3$. Nur gibt es beliebig hohe Grade, also beliebig lange Vektoren.
:::
""")

k.vektor("Berechne in $\\mathbb{R}[X]$ das Polynom $2(1 + X) + (2 - X + X^2)$. Gib die Koeffizienten $(a_0, a_1, a_2)^\\top$ von $a_0 + a_1X + a_2X^2$ an.",
         lin([2, 1], [[1, 1, 0], [2, -1, 1]]),
         "$2(1 + X) = 2 + 2X$; dazu $2 - X + X^2$: $X^0$: $4$, $X^1$: $2 - 1 = 1$, $X^2$: $1$. Ergebnis $4 + X + X^2$.",
         tipps=["Multipliziere zuerst jeden Koeffizienten von $1 + X$ mit $2$.", "Addiere dann Koeffizienten gleicher Potenzen, fehlende sind $0$.", "Koeffizient von $X^1$: $2 + (-1)$."],
         rechenweg=rechnung([("2 \\cdot 1 + 2 = 4", "Koeffizient von $X^0$"), ("2 \\cdot 1 + (-1) = 1", "Koeffizient von $X^1$"), ("2 \\cdot 0 + 1 = 1", "Koeffizient von $X^2$")]),
         typische_fehler=[([3, 0, 1], "Du hast $(1 + X) + (2 - X + X^2)$ ohne den Faktor $2$ gerechnet."),
                          ([4, 1, 0], "Der Koeffizient von $X^2$ fehlt: $0 + 1 = 1$.")])

# ── Seite 4: Funktionenräume ─────────────────────────────────────────────
k.erklaerung("Funktionenräume", r"""
## Beispiele 4.28 und 4.29

Für eine Menge $M$ und einen Körper $K$ ist $\mathrm{abb}(M, K)$, die Menge aller Abbildungen $M \to K$, ein Vektorraum, wenn man **punktweise** rechnet:
$(f + g)(x) := f(x) + g(x)$ und $(\lambda f)(x) := \lambda f(x)$. Der Nullvektor ist die Nullfunktion. Das ist ein [[Funktionenraum]].
Die Axiome folgen aus den Rechenregeln in $K$, weil zwei Abbildungen genau dann gleich sind, wenn sie an jeder Stelle übereinstimmen.

**Beispiel 4.29.** $F := \{f \in \mathrm{abb}(\mathbb{R}, \mathbb{R}) \mid \exists a, b \in \mathbb{R}\ \forall t\colon f(t) = a + bt\}$ ist ein Vektorraum:
$(f + g)(t) = (a + c) + (b + d)t$ und $(\lambda f)(t) = \lambda a + (\lambda b)t$ liegen wieder in $F$.

:::rechnung $f(t) = 1 + 2t$, $g(t) = 3 - t$: $(f + g)(t) = 4 + t$ und $(3g)(t) = 9 - 3t$
1 + 3 = 4 || konstante Terme addieren
2 + (-1) = 1 || Koeffizienten von $t$ addieren
5 + 1 = 6 || Probe bei $t = 2$: links $f(2) + g(2)$, die Summe der Werte
4 + 1 \cdot 2 = 6 || rechts $(f + g)(2)$: beide Wege stimmen überein
:::

:::alt Als Messreihe
Eine Funktion ist wie eine Messreihe mit unendlich vielen Messpunkten. Zwei Messreihen addierst du Punkt für Punkt, und „Skalieren“ ist Umrechnen der Einheit
(z. B. Meter in Zentimeter). $F$ ist die Teilmenge aller Messreihen, die auf einer Geraden liegen.
:::
""")

k.zahl("Seien $f(t) = 1 + 2t$ und $g(t) = 3 - t$ Funktionen in $F$. Berechne $(2f + 3g)(2)$.",
       2 * (1 + 2 * 2) + 3 * (3 - 2),
       "Punktweise: $(2f + 3g)(2) = 2f(2) + 3g(2) = 2 \\cdot 5 + 3 \\cdot 1 = 13$.",
       tipps=["Rechne punktweise: erst $f(2)$ und $g(2)$ ausrechnen.", "$f(2) = 5$, $g(2) = 1$.", "$2 \\cdot 5 + 3 \\cdot 1$."],
       rechenweg=rechnung([("1 + 2 \\cdot 2 = 5", "$f(2)$"), ("3 - 2 = 1", "$g(2)$"), ("2 \\cdot 5 + 3 \\cdot 1 = 13", "punktweise $(2f + 3g)(2)$")]),
       typische_fehler=[(6, "Du hast $f(2) + g(2)$ gerechnet, die Skalare $2$ und $3$ fehlen."),
                        (5, "Du hast $f(2) \\cdot g(2)$ gerechnet. Die Vektorraumoperation ist die **Summe** der Werte, nicht das Produkt.")])

# ── Seite 5: Satz 4.30 ───────────────────────────────────────────────────
k.erklaerung("Rechenregeln im Vektorraum", r"""
## Satz 4.30

In jedem Vektorraum gilt $0v = 0$, $\lambda 0 = 0$ und $(-1)v = -v$. Außerdem ist $\lambda v = 0$ genau dann, wenn $\lambda = 0$ oder $v = 0$.
(Im Skript ist der Beweis eine Übung.) Das Wichtige: Die Regeln folgen nur aus den Axiomen, gelten also in **jedem** Vektorraum.

:::rechnung $0v = 0$ aus den Axiomen, Schritt für Schritt
\text{In } K: 0 = 0 + 0 || Körperaxiom (neutrales Element)
0v = (0 + 0)v = 0v + 0v || (d2)
0 = 0v || auf beiden Seiten $-(0v)$ addieren (Gruppe)
:::

Für $(-1)v = -v$: $v + (-1)v = 1v + (-1)v = (1 + (-1))v = 0v = 0$. Also ist $(-1)v$ das additive Inverse von $v$.

:::alt Als Selbstverständlichkeit mit Beweis
Dass „null mal Pfeil gleich Nullpfeil“ gilt, ist im $\mathbb{R}^n$ klar. In einem fremden Vektorraum (Polynome, Funktionen) darf man es erst benutzen, wenn man es aus den
Axiomen gefolgert hat. Genau das leisten die zwei Zeilen oben.
:::
""")

k.ordnen("Ordne den Beweis von $0v = 0$ in jedem Vektorraum.",
         ["In $K$ gilt $0 = 0 + 0$.", "Also ist $0v = (0 + 0)v$, und nach (d2) gilt $(0 + 0)v = 0v + 0v$.",
          "Wir haben $0v = 0v + 0v$ gezeigt.", "Addiere auf beiden Seiten das additive Inverse $-(0v)$ von $0v$.",
          "Links entsteht $0$, rechts $0v$. Also ist $0v = 0$. $\\square$"],
         "Der Trick ist $0 = 0 + 0$ in $K$ und das Distributivgesetz (d2). Danach kürzt man in der Gruppe $(V, +)$.",
         ablenker=["Nach (d1) gilt $(0 + 0)v = 0v + 0v$.", "Da $v \\neq 0$ ist, darf man durch $v$ teilen."],
         tipps=["Beginne mit einer Zerlegung von $0 \\in K$.", "Welches Axiom löst $(0 + 0)v$ auf? (d1) betrifft Summen von Vektoren, (d2) Summen von Skalaren.", "Ein Vektor lässt sich nicht teilen: Man addiert das Inverse."])

# ── Seite 6: Untervektorräume ────────────────────────────────────────────
k.erklaerung("Untervektorräume und Satz 4.32", r"""
## Definition 4.31 und Satz 4.32

:::analogie 🏠 Haus im Haus
Ein Untervektorraum ist ein Vektorraum im Vektorraum: Du darfst innerhalb mischen und skalieren und das Haus nie verlassen.
:::

Ein [[Untervektorraum]] $U \subseteq V$ ist selbst ein Vektorraum mit den **eingeschränkten** Verknüpfungen. Alle Rechenregeln gelten schon in $V$, man muss also nur prüfen, dass die Ergebnisse in $U$ bleiben.

**Satz 4.32 (Unterraumkriterium).** $U \subseteq V$ ist genau dann ein Untervektorraum, wenn $U \neq \emptyset$ und $\lambda u + \mu w \in U$ für alle $u, w \in U$ und $\lambda, \mu \in K$.

:::rechnung Prüfung für $U = \{\mathbf{x} \in \mathbb{R}^3 \mid x_1 + x_2 = 0\}$ mit $u = (1, -1, 0)^\top$, $w = (2, -2, 5)^\top$, $\lambda = 2$, $\mu = -1$
1 + (-1) = 0 || $u \in U$
2 + (-2) = 0 || $w \in U$
2 \cdot 1 + (-1) \cdot 2 = 0 || erste Komponente von $\lambda u + \mu w$
2 \cdot (-1) + (-1) \cdot (-2) = 0 || zweite Komponente: $0 + 0 = 0$, also $\lambda u + \mu w \in U$
:::

Das Beispiel ist nur eine Probe. Der Beweis muss für **beliebige** $u, w, \lambda, \mu$ gelten.

:::alt Als Abgeschlossenheit
Wie eine Insel: Egal, wie du auf der Insel mit Addition und Skalieren hantierst, du landest nie im Wasser. Dazu gehört, dass die Insel nicht leer ist (mit $0$ als Land).
:::
""")

k.ordnen("Ordne den Beweis der Richtung „$\\Leftarrow$“ von Satz 4.32: Es gelte $U \\neq \\emptyset$ und $\\lambda u + \\mu w \\in U$ für alle $u, w \\in U$, $\\lambda, \\mu \\in K$.",
         ["Für $u, w \\in U$ gilt $u - w = 1u + (-1)w$ nach Satz 4.30 und (e), also $u - w \\in U$ (mit $\\lambda = 1$, $\\mu = -1$).",
          "Nach dem Untergruppenkriterium (Satz 3.24) ist $(U, +)$ eine Untergruppe von $(V, +)$, insbesondere abelsch.",
          "Für $\\lambda \\in K$ und $u \\in U$ gilt $\\lambda u = \\lambda u + 0_K u \\in U$, die Skalarmultiplikation lässt sich also auf $U$ einschränken.",
          "Die übrigen Axiome (d1), (d2), (a), (e) gelten schon in $V$, also auch für Elemente von $U$.",
          "Somit ist $(U, +, \\cdot)$ ein Untervektorraum. $\\square$"],
         "Aus $u - w \\in U$ bekommt man die Untergruppe, aus $\\mu = 0$ die Abgeschlossenheit unter Skalierung. Die übrigen Regeln erbt $U$ von $V$.",
         ablenker=["Wir müssen alle acht Vektorraumaxiome in $U$ einzeln nachrechnen, weil $U$ ein neues Objekt ist."],
         tipps=["Aus der Bedingung folgt die Untergruppeneigenschaft.", "Setze $\\mu = 0$ oder $w = u$, um nur zu skalieren.", "Die Rechenregeln erbt man von $V$."])

k.mehrfach("Welche Teilmengen von $\\mathbb{R}^2$ sind Untervektorräume?",
           ["$\\{\\mathbf{0}\\}$", "$\\{\\mathbf{x} \\mid x_2 = 2x_1\\}$", "$\\{\\mathbf{x} \\mid x_1 + x_2 = 0\\}$"],
           ["$\\{\\mathbf{x} \\mid x_2 = 2x_1 + 1\\}$", "$\\{\\mathbf{x} \\mid x_1 x_2 = 0\\}$", "$\\{\\mathbf{x} \\mid x_1 \\ge 0\\}$"],
           "Eine Ursprungsgerade oder $\\{\\mathbf{0}\\}$ ist abgeschlossen. $x_2 = 2x_1 + 1$ enthält $\\mathbf{0}$ nicht. $x_1x_2 = 0$ ist die Vereinigung der Achsen: $\\mathbf{e}^{(1)} + \\mathbf{e}^{(2)}$ liegt nicht drin. $x_1 \\ge 0$ ist nicht unter Multiplikation mit $-1$ abgeschlossen.",
           tipps=["Liegt $\\mathbf{0}$ in der Menge? Wenn nein, ist sie kein Unterraum.", "Prüfe Summe und Vielfache an konkreten Vektoren.", "Zwei Geraden zusammen sind selten eine Gerade."],
           fehler={"$\\{\\mathbf{x} \\mid x_2 = 2x_1 + 1\\}$": "$\\mathbf{0}$ erfüllt $0 = 0 + 1$ nicht: Der Nullvektor fehlt (Bsp. 4.36).",
                   "$\\{\\mathbf{x} \\mid x_1 x_2 = 0\\}$": "$(1, 0)^\\top$ und $(0, 1)^\\top$ liegen drin, aber $(1, 1)^\\top$ nicht (Beob. 4.40).",
                   "$\\{\\mathbf{x} \\mid x_1 \\ge 0\\}$": "$(1, 0)^\\top$ liegt drin, $(-1) \\cdot (1, 0)^\\top = (-1, 0)^\\top$ nicht."})

# ── Seite 7: Beispiele für Unterräume ────────────────────────────────────
k.erklaerung("Beispiele und Gegenbeispiele", r"""
## Beispiele 4.33 bis 4.36 und Beobachtung 4.40

Immer Unterräume: $\{0\}$ und $V$ (Bsp. 4.33). $F$ (affine Funktionen) ist ein Unterraum von $\mathrm{abb}(\mathbb{R}, \mathbb{R})$ (Bsp. 4.34), und die Polynomfunktionen $P_K$ ebenfalls (Bsp. 4.35).
Geraden, Ebenen und Hyperebenen **durch den Ursprung** sind Unterräume von $\mathbb{R}^n$ (Bsp. 4.36), solche ohne Ursprung nicht: Ihnen fehlt der Nullvektor.

:::rechnung Gegenbeispiel: die Gerade $G = \{(1, 0)^\top + t(0, 1)^\top\}$ (ohne Ursprung)
\text{1 + 0 t = 0 ist unlösbar} || erste Komponente von $\mathbf{0}$: kein $t$ erfüllt das (links stets $1$)
(1 + 1, 0 + 0) = (2, 0) \text{ mit } 2 \ne 1 || Summe zweier Punkte von $G$ hat erste Komponente $2$: nicht in $G$
:::

**Beobachtung 4.40.** Die Vereinigung zweier Untervektorräume ist im Allgemeinen keiner: Die Koordinatenachsen sind Unterräume von $\mathbb{R}^2$,
aber $\{x_1 = 0 \text{ oder } x_2 = 0\}$ enthält $\mathbf{e}^{(1)}$ und $\mathbf{e}^{(2)}$, nicht deren Summe $(1, 1)^\top$.

:::alt Als Schleuse
Ein Unterraum muss den Ursprung enthalten, sonst könnte man durch Multiplikation mit $0$ aus ihm herausfallen. Zwei Unterräume zusammenwerfen verbindet sie nicht:
Die Summe eines Vektors aus dem einen und eines aus dem anderen liegt meist in keinem von beiden.
:::
""")

k.wf("Die Vereinigung zweier Untervektorräume von $V$ ist immer wieder ein Untervektorraum von $V$.", False,
     "Gegenbeispiel (Beob. 4.40): Die beiden Koordinatenachsen in $\\mathbb{R}^2$ sind Unterräume, ihre Vereinigung enthält $\\mathbf{e}^{(1)}$ und $\\mathbf{e}^{(2)}$, aber nicht $\\mathbf{e}^{(1)} + \\mathbf{e}^{(2)}$. Der **Schnitt** dagegen ist stets ein Unterraum (Satz 4.38).",
     tipps=["Denke an zwei Geraden durch den Ursprung."])

k.luecke("Zeige: $U = \\{\\mathbf{x} \\in \\mathbb{R}^3 \\mid x_1 + x_2 = 0\\}$ ist abgeschlossen. Für $\\mathbf{u}, \\mathbf{w} \\in U$ und $\\lambda, \\mu \\in \\mathbb{R}$ gilt für die ersten beiden Komponenten von $\\lambda\\mathbf{u} + \\mu\\mathbf{w}$:",
         "\\lambda(u_1 + u_2) + \\mu(w_1 + w_2) = \\lambda \\cdot \\luecke + \\mu \\cdot \\luecke = \\luecke",
         [[0], [0], [0]],
         "Wegen $\\mathbf{u}, \\mathbf{w} \\in U$ ist $u_1 + u_2 = 0$ und $w_1 + w_2 = 0$. Also $\\lambda \\cdot 0 + \\mu \\cdot 0 = 0$, und $\\lambda\\mathbf{u} + \\mu\\mathbf{w} \\in U$. Zusammen mit $\\mathbf{0} \\in U$ folgt nach Satz 4.32, dass $U$ ein Untervektorraum ist.",
         tipps=["Benutze $\\mathbf{u} \\in U$: Was ist $u_1 + u_2$?", "Dasselbe gilt für $\\mathbf{w}$.", "Alle drei Lücken sind $0$."],
         rechenweg=rechnung([("0 \\cdot \\lambda + 0 \\cdot \\mu = 0", "beide Klammern sind $0$")]),
         typische_fehler=[([1, 1, 1], "Die Klammern sind $0$, nicht $1$: $\\mathbf{u}, \\mathbf{w} \\in U$ bedeutet $u_1 + u_2 = 0$ und $w_1 + w_2 = 0$.")])

# ── Seite 8: Linearkombination, lineare Hülle ────────────────────────────
k.erklaerung("Linearkombination und lineare Hülle", r"""
## Definition 4.37 und 4.41, Satz 4.42

Eine [[Linearkombination]] von $v^{(1)}, \ldots, v^{(m)} \in V$ mit Koeffizienten $\lambda_1, \ldots, \lambda_m \in K$ ist $\sum_{j=1}^m \lambda_j v^{(j)}$.
Die [[lineare Hülle]] $\langle M \rangle$ einer Menge $M \subseteq V$ ist der **Schnitt aller Unterräume**, die $M$ enthalten (Def. 4.37), also der kleinste solche Unterraum.
Ist $\langle M \rangle = V$, heißt $M$ ein [[Erzeugendensystem]].

**Satz 4.42.** $\langle M \rangle$ besteht genau aus den Linearkombinationen endlich vieler Vektoren aus $M$. Insbesondere $\langle \emptyset \rangle = \{0\}$.

:::visual vektoren2d
{"vektoren": [{"x": 2, "y": 1}, {"x": 1, "y": 3}], "zeige": ["summe", "vielfaches"], "faktor": "3/2",
 "unterschrift": "Alle Linearkombinationen $\\lambda\\mathbf{a} + \\mu\\mathbf{b}$ füllen die ganze Ebene: $\\langle \\mathbf{a}, \\mathbf{b} \\rangle = \\mathbb{R}^2$."}
:::

:::rechnung Linearkombination $2\mathbf{a} - \mathbf{b}$ mit $\mathbf{a} = (2, 1)^\top$, $\mathbf{b} = (1, 3)^\top$
2 \cdot 2 - 1 = 3 || erste Komponente
2 \cdot 1 - 3 = -1 || zweite Komponente: $2\mathbf{a} - \mathbf{b} = (3, -1)^\top \in \langle \mathbf{a}, \mathbf{b} \rangle$
:::

:::alt Als Mischpult
Jeder Vektor in $M$ ist ein Regler. Eine Linearkombination ist eine Einstellung aller Regler, die Hülle sind alle erreichbaren Einstellungen. Weil Regler nach unten
und nach oben gehen (auch negative Koeffizienten), entsteht ein ganzer Raum, nie ein Strahl.
:::
""")

k.vektor("Berechne die Linearkombination $2\\mathbf{a} - 3\\mathbf{b} + \\mathbf{c}$ mit $\\mathbf{a} = (1, 0, 1)^\\top$, $\\mathbf{b} = (0, 1, 2)^\\top$, $\\mathbf{c} = (1, 1, 1)^\\top$.",
         lin([2, -3, 1], [[1, 0, 1], [0, 1, 2], [1, 1, 1]]),
         "$2\\mathbf{a} = (2, 0, 2)$, $-3\\mathbf{b} = (0, -3, -6)$, $\\mathbf{c} = (1, 1, 1)$. Summe: $(3, -2, -3)^\\top$.",
         tipps=["Multipliziere jeden Vektor mit seinem Koeffizienten.", "Addiere dann komponentenweise.", "Dritte Komponente: $2 - 6 + 1$."],
         rechenweg=rechnung([("2 \\cdot 1 - 3 \\cdot 0 + 1 = 3", "erste Komponente"), ("2 \\cdot 0 - 3 \\cdot 1 + 1 = -2", "zweite Komponente"), ("2 \\cdot 1 - 3 \\cdot 2 + 1 = -3", "dritte Komponente")]),
         typische_fehler=[([3, -2, 9], "Dritte Komponente: $-3 \\cdot 2 = -6$, also $2 - 6 + 1 = -3$. Das Vorzeichen von $-3\\mathbf{b}$ gilt für alle Komponenten."),
                          ([3, 4, 5], "Das Minus bei $3\\mathbf{b}$ hast du übersehen: Es ist $-3\\mathbf{b}$, nicht $+3\\mathbf{b}$.")])

k.vektor("Stelle $\\mathbf{x} = (5, 3)^\\top$ als Linearkombination $\\lambda_1(1, 1)^\\top + \\lambda_2(1, -1)^\\top$ dar. Gib $(\\lambda_1, \\lambda_2)^\\top$ an.",
         [4, 1],
         "Komponenten: $\\lambda_1 + \\lambda_2 = 5$ und $\\lambda_1 - \\lambda_2 = 3$. Addieren: $2\\lambda_1 = 8$, also $\\lambda_1 = 4$, $\\lambda_2 = 1$.",
         tipps=["Schreibe die zwei Komponentengleichungen auf.", "Addiere die Gleichungen, dann fällt $\\lambda_2$ weg.", "$\\lambda_1 = 4$."],
         rechenweg=rechnung([("4 + 1 = 5", "erste Komponente der Probe"), ("4 - 1 = 3", "zweite Komponente der Probe")]),
         typische_fehler=[([1, 4], "Die Koeffizienten sind vertauscht: $\\lambda_1$ gehört zu $(1, 1)^\\top$.")])

# ── Seite 9: Erzeugendensysteme ──────────────────────────────────────────
k.erklaerung("Erzeugendensysteme in Beispielen", r"""
## Beispiele 4.39 und 4.43 bis 4.46

- $\mathbb{R}^n = \langle \mathbf{e}^{(1)}, \ldots, \mathbf{e}^{(n)} \rangle$, denn $\mathbf{x} = \sum x_j \mathbf{e}^{(j)}$ (Bsp. 4.43). Ein überflüssiger Erzeuger ändert nichts: $\langle \mathbf{e}^{(1)}, \mathbf{e}^{(2)}, \mathbf{e}^{(1)} + \mathbf{e}^{(2)} \rangle = \langle \mathbf{e}^{(1)}, \mathbf{e}^{(2)} \rangle$.
- $E_1 = \{x_1 + x_2 = 0\} = \langle (1, -1, 0)^\top, (0, 0, 1)^\top \rangle$, $E_2 = \{x_2 + x_3 = 0\}$, Schnitt $E_1 \cap E_2 = \langle (1, -1, 1)^\top \rangle$ (Bsp. 4.39, 4.44).
- $F = \langle f^{(0)}, f^{(1)} \rangle$ mit $f^{(0)}(t) = 1$, $f^{(1)}(t) = t$ (Bsp. 4.45).
- $K[X] = \langle \{X^j \mid j \in \mathbb{N}\} \rangle$: Monome erzeugen alle Polynome (Bsp. 4.46).

:::rechnung Der Schnitt $E_1 \cap E_2$: beide Gleichungen gelten
\text{x_2 = -x_1} || aus $x_1 + x_2 = 0$
\text{x_3 = -x_2 = x_1} || aus $x_2 + x_3 = 0$, also $\mathbf{x} = x_1(1, -1, 1)^\top$
1 + (-1) = 0 || Probe für $(1, -1, 1)^\top$ in $E_1$ (Gleichung $x_1 + x_2$)
(-1) + 1 = 0 || Probe in $E_2$ (Gleichung $x_2 + x_3$)
:::

:::alt Als Baukasten
Die Erzeuger sind die Bausteinsorten. $\langle M \rangle$ ist alles, was sich daraus bauen lässt. Ein Stein, den du aus den anderen bauen kannst (hier $\mathbf{e}^{(1)} + \mathbf{e}^{(2)}$), ist im Kasten überflüssig. Dieser Gedanke führt im nächsten Kapitel zur Basis.
:::
""")

k.mc("Welche Aussage über die Hülle in $\\mathbb{R}^3$ stimmt?",
     ["$\\langle \\mathbf{e}^{(1)}, \\mathbf{e}^{(2)}, \\mathbf{e}^{(1)} + \\mathbf{e}^{(2)} \\rangle = \\langle \\mathbf{e}^{(1)}, \\mathbf{e}^{(2)} \\rangle$, die Ebene $x_3 = 0$",
      "$\\langle \\mathbf{e}^{(1)}, \\mathbf{e}^{(2)}, \\mathbf{e}^{(1)} + \\mathbf{e}^{(2)} \\rangle = \\mathbb{R}^3$",
      "$\\langle \\mathbf{e}^{(1)}, \\mathbf{e}^{(2)}, \\mathbf{e}^{(1)} + \\mathbf{e}^{(2)} \\rangle$ ist ein dreidimensionaler Raum, weil drei Vektoren vorkommen",
      "$\\langle \\emptyset \\rangle = \\emptyset$"],
     "Es gilt $a\\mathbf{e}^{(1)} + b\\mathbf{e}^{(2)} + c(\\mathbf{e}^{(1)} + \\mathbf{e}^{(2)}) = (a + c)\\mathbf{e}^{(1)} + (b + c)\\mathbf{e}^{(2)}$: der dritte Vektor liefert nichts Neues, alle Vektoren haben $x_3 = 0$. Ferner $\\langle \\emptyset \\rangle = \\{0\\}$ (Satz 4.42).",
     tipps=["Welche dritte Komponente haben alle Linearkombinationen?", "Ist der dritte Erzeuger eine Kombination der ersten beiden?"],
     fehler={"$\\langle \\mathbf{e}^{(1)}, \\mathbf{e}^{(2)}, \\mathbf{e}^{(1)} + \\mathbf{e}^{(2)} \\rangle = \\mathbb{R}^3$": "Alle Erzeuger haben dritte Komponente $0$, also auch alle Linearkombinationen: Man erreicht $\\mathbf{e}^{(3)}$ nicht.",
             "$\\langle \\mathbf{e}^{(1)}, \\mathbf{e}^{(2)}, \\mathbf{e}^{(1)} + \\mathbf{e}^{(2)} \\rangle$ ist ein dreidimensionaler Raum, weil drei Vektoren vorkommen": "Es zählt nicht die Anzahl der Erzeuger, sondern wie viele davon überflüssig sind (Bsp. 4.43).",
             "$\\langle \\emptyset \\rangle = \\emptyset$": "Die leere Linearkombination hat den Wert $0$, also $\\langle \\emptyset \\rangle = \\{0\\}$ (Satz 4.42). Ein Unterraum ist nie leer."})


# ══ Praxis ═══════════════════════════════════════════════════════════════
def _rv(rng, lo=-3, hi=3, n=3):
    return [rng.randint(lo, hi) for _ in range(n)]


def _kl_zeilen(c, vs, erg, namen):
    z = []
    for i in range(len(vs[0])):
        teile = " + ".join(f"{tx(c[j])} \\cdot {tx(vs[j][i])}" for j in range(len(vs)))
        z.append((f"{teile} = {tx(erg[i])}", f"Komponente {i + 1}"))
    return z


def linearkombination_bilden(rng):
    """Def. 4.41: Linearkombination dreier Vektoren."""
    n = rng.choice([2, 3])
    vs = [_rv(rng, -3, 3, n) for _ in range(3)]
    c = [rng.randint(-3, 3) for _ in range(3)]
    while 0 in c[:2] or len(set(map(tuple, vs))) < 3:
        c = [rng.randint(-3, 3) for _ in range(3)]
        vs = [_rv(rng, -3, 3, n) for _ in range(3)]
    erg = lin(c, vs)
    fehler = [(lin([abs(x) for x in c], vs), "Die Vorzeichen der Koeffizienten wurden ignoriert."),
              (lin([c[0], c[1], 0], vs), "Der dritte Summand fehlt."),
              (lin(c[::-1], vs), "Die Koeffizienten sind den falschen Vektoren zugeordnet: $\\lambda_j$ gehört zu $\\mathbf{v}^{(j)}$."),
              (lin([c[0], c[1], -c[2]], vs), "Das Vorzeichen des dritten Koeffizienten wurde umgedreht."),
              (lin([-c[0], c[1], c[2]], vs), "Das Vorzeichen des ersten Koeffizienten wurde umgedreht."),
              (lin([c[0], -c[1], c[2]], vs), "Das Vorzeichen des zweiten Koeffizienten wurde umgedreht.")]
    namen = ["a", "b", "c"]
    kopf = ", ".join(f"\\mathbf{{{namen[j]}}} = {vt(vs[j])}" for j in range(3))
    return {"typ": "vektor",
            "frage": f"Berechne $({tx(c[0])})\\mathbf{{a}} + ({tx(c[1])})\\mathbf{{b}} + ({tx(c[2])})\\mathbf{{c}}$ mit ${kopf}$.",
            "loesung": erg,
            "tipps": ["Multipliziere jeden Vektor mit seinem Koeffizienten.", "Addiere komponentenweise.", f"Erste Komponente: ${tx(c[0])} \\cdot {tx(vs[0][0])} + {tx(c[1])} \\cdot {tx(vs[1][0])} + {tx(c[2])} \\cdot {tx(vs[2][0])}$."],
            "rechenweg": rechnung(_kl_zeilen(c, vs, erg, namen)),
            "erklaerung": "Eine Linearkombination ist die Summe der Vielfachen (Def. 4.41), gerechnet wird komponentenweise.",
            "typische_fehler": ohne_gleiche(erg, fehler)}


def polynom_kombination(rng):
    """Bsp. 4.26: Rechnen in K[X] über Koeffizienten."""
    while True:
        p = [rng.randint(-3, 3) for _ in range(rng.choice([2, 3]))]
        q = [rng.randint(-3, 3) for _ in range(3)]
        lam, mu = rng.choice([-2, -1, 2, 3]), rng.choice([-2, -1, 2, 3])
        if p[-1] != 0 and q[-1] != 0:
            break
    pp = p + [0] * (3 - len(p))
    erg = lin([lam, mu], [pp, q])
    zeilen = [(f"{tx(lam)} \\cdot {tx(pp[j])} + {tx(mu)} \\cdot {tx(q[j])} = {tx(erg[j])}", f"Koeffizient von $X^{j}$") for j in range(3)]
    fehler = [(lin([1, 1], [pp, q]), "Die Skalare $\\lambda$ und $\\mu$ fehlen: Gerechnet wurde $p + q$."),
              (lin([lam, mu], [pp, q[::-1]]), "Die Koeffizienten von $q$ stehen verkehrt herum: $a_0$ gehört zu $X^0$."),
              (lin([lam, -mu], [pp, q]), "Das Vorzeichen von $\\mu$ wurde umgedreht.")]
    return {"typ": "vektor",
            "frage": f"Sei $p = {poly_tex(p)}$ und $q = {poly_tex(q)}$ in $\\mathbb{{R}}[X]$. Berechne $({tx(lam)})p + ({tx(mu)})q$ und gib die Koeffizienten $(a_0, a_1, a_2)^\\top$ an.",
            "loesung": erg,
            "tipps": ["Multipliziere jeden Koeffizienten mit dem Skalar.", "Addiere Koeffizienten gleicher Potenzen. Fehlende Koeffizienten sind $0$.", f"Koeffizient von $X^0$: ${tx(lam)} \\cdot {tx(pp[0])} + {tx(mu)} \\cdot {tx(q[0])}$."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "In $K[X]$ addiert man Koeffizienten gleicher Potenzen und skaliert jeden Koeffizienten (Bsp. 4.26).",
            "typische_fehler": ohne_gleiche(erg, fehler)}


def funktionenraum_wert(rng):
    """Bsp. 4.28 und 4.29: punktweise Operationen in F."""
    while True:
        a, b, c, d = _rv(rng, -3, 3, 4)
        lam, mu = rng.choice([-2, -1, 2, 3]), rng.choice([-2, -1, 2, 3])
        t0 = rng.randint(-3, 3)
        if b != 0 and d != 0 and t0 != 0 and a + b * t0 != 0 and c + d * t0 != 0:
            break
    f0, g0 = a + b * t0, c + d * t0
    erg = lam * f0 + mu * g0
    zeilen = [(f"{tx(a)} + {tx(b)} \\cdot {tx(t0)} = {tx(f0)}", f"$f({t0})$"), (f"{tx(c)} + {tx(d)} \\cdot {tx(t0)} = {tx(g0)}", f"$g({t0})$"),
              (f"{tx(lam)} \\cdot {tx(f0)} + {tx(mu)} \\cdot {tx(g0)} = {tx(erg)}", "punktweise: $(\\lambda f + \\mu g)(t_0) = \\lambda f(t_0) + \\mu g(t_0)$")]
    fehler = [(f0 + g0, "Die Skalare $\\lambda$ und $\\mu$ fehlen."), (lam * f0 * mu * g0, "Du hast multipliziert. In $F$ addiert man die Funktionen, also die Werte."),
              (lam * f0 - mu * g0, "Zwischen den beiden Summanden steht ein Plus: $\\lambda f(t_0) + \\mu g(t_0)$."), (lam * f0 + g0, "Der Skalar $\\mu$ fehlt bei $g$.")]
    return {"frage": f"Seien $f(t) = {poly_tex([a, b]).replace('X', 't')}$ und $g(t) = {poly_tex([c, d]).replace('X', 't')}$ in $F$. Berechne $({tx(lam)}f + {tx(mu)}g)({t0})$.",
            "loesung": erg,
            "tipps": ["Rechne punktweise: Setze erst $t_0$ in $f$ und $g$ ein.", f"$f({t0}) = {f0}$ und $g({t0}) = {g0}$.", "Dann $\\lambda f(t_0) + \\mu g(t_0)$."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Addition und Skalarmultiplikation in $F$ sind punktweise definiert (Bsp. 4.28, 4.29).",
            "typische_fehler": ohne_gleiche(erg, fehler)}


_UR_OPT = ["Ja, ein Untervektorraum", "Nein, der Nullvektor liegt nicht in der Menge",
           "Nein, nicht abgeschlossen unter der Addition (der Nullvektor liegt aber drin)",
           "Nein, nicht abgeschlossen unter der Skalarmultiplikation (Addition geht)"]


def _gl_links(a, n):
    s = ""
    for i in range(n):
        if a[i] == 0:
            continue
        c = "" if abs(a[i]) == 1 else str(abs(a[i]))
        s += (" - " if a[i] < 0 else (" + " if s else "")) + f"{c}x_{i + 1}" if s else (("-" if a[i] < 0 else "") + f"{c}x_{i + 1}")
    return s


def _bsp_menge(art, n, a, b):
    ax = _gl_links(a, n)
    if art == "homogen":
        return f"\\{{\\mathbf{{x}} \\in \\mathbb{{R}}^{{{n}}} \\mid {ax} = 0\\}}", lambda x: sum(a[i] * x[i] for i in range(n)) == 0
    if art == "inhomogen":
        return f"\\{{\\mathbf{{x}} \\in \\mathbb{{R}}^{{{n}}} \\mid {ax} = {b}\\}}", lambda x: sum(a[i] * x[i] for i in range(n)) == b
    if art == "achsen":
        return f"\\{{\\mathbf{{x}} \\in \\mathbb{{R}}^{{{n}}} \\mid x_1 x_2 = 0\\}}", lambda x: x[0] * x[1] == 0
    if art == "halbraum":
        return f"\\{{\\mathbf{{x}} \\in \\mathbb{{R}}^{{{n}}} \\mid x_1 \\ge 0\\}}", lambda x: x[0] >= 0
    return f"\\mathbb{{Z}}^{{{n}}}", lambda x: all(F(v).denominator == 1 for v in x)


def _klasse(n, ist_in, probe_k=4):
    """Brute-Force-Klassifikation über ein kleines Gitter (nur zur Kontrolle der Konstruktion)."""
    pts = [x for x in product(range(-probe_k, probe_k + 1), repeat=n) if ist_in(x)]
    pts = pts[::max(1, len(pts) // 60)]
    if not ist_in([0] * n):
        return 1
    add_ok = all(ist_in([p + q for p, q in zip(x, y)]) for x in pts for y in pts)
    skal_ok = all(ist_in([F(1, 2) * p for p in x]) and ist_in([-p for p in x]) for x in pts)
    if add_ok and skal_ok:
        return 0
    return 2 if not add_ok else 3


def unterraum_entscheiden(rng):
    art = rng.choice(["homogen", "inhomogen", "achsen", "halbraum", "ganzzahlig", "homogen"])
    n = rng.choice([2, 3])
    while True:
        a = [rng.randint(-3, 3) for _ in range(n)]
        if any(a):
            break
    b = rng.choice([-2, -1, 1, 2, 3])
    tex_m, ist_in = _bsp_menge(art, n, a, b)
    soll = {"homogen": 0, "inhomogen": 1, "achsen": 2, "halbraum": 3, "ganzzahlig": 3}[art]
    assert _klasse(n, ist_in) == soll, (art, n, a, b)
    grund = {0: "Er enthält $\\mathbf{0}$, und mit $\\mathbf{x}, \\mathbf{y}$ liegt jede Linearkombination wieder in der Menge: Die Gleichung ist homogen und linear.",
             1: f"$\\mathbf{{0}}$ erfüllt die Gleichung nicht ($0 = {b}$ wäre nötig). Ohne Nullvektor kein Untervektorraum (Bsp. 4.36).",
             2: "Die Menge ist die Vereinigung zweier Unterräume, die Summe $\\mathbf{e}^{(1)} + \\mathbf{e}^{(2)}$ liegt nicht in ihr (Beob. 4.40).",
             3: ("$(1, 0, \\ldots)$ liegt in der Menge, $(-1) \\cdot (1, 0, \\ldots)$ nicht: die Skalarmultiplikation führt hinaus."
                 if art == "halbraum" else "$\\mathbf{e}^{(1)} \\in \\mathbb{Z}^n$, aber $\\frac12\\mathbf{e}^{(1)} \\notin \\mathbb{Z}^n$ (Bsp. 4.27).")}[soll]
    optionen = [_UR_OPT[soll]] + [o for i, o in enumerate(_UR_OPT) if i != soll]
    return {"typ": "mc",
            "frage": f"Ist $U = {tex_m}$ ein Untervektorraum von $\\mathbb{{R}}^{{{n}}}$?",
            "optionen": optionen, "fehler": {o: f"Das stimmt nicht. {grund}" for o in optionen[1:]},
            "tipps": ["Liegt $\\mathbf{0}$ in $U$? Wenn nein, ist es kein Untervektorraum.", "Prüfe das Unterraumkriterium (Satz 4.32) an einem Beispiel: Summe und Vielfaches.",
                      "Ein einziges Gegenbeispiel genügt, ein Beweis verlangt beliebige Elemente."],
            "rechenweg": rechnung([("\\text{Befund}", grund)]),
            "erklaerung": "Zuerst $\\mathbf{0}$ testen, dann Summe und Vielfache (Satz 4.32)."}


def in_lineare_huelle(rng):
    """Ist x in <u, v>? Mit Koeffizienten bzw. Widerspruch (Def. 4.37, Satz 4.42)."""
    while True:
        u, v = _rv(rng, -2, 2), _rv(rng, -2, 2)
        if u[0] * v[1] - u[1] * v[0] != 0:
            break
    lam, mu = rng.randint(-3, 3), rng.randint(-3, 3)
    ja = rng.random() < 0.5
    x = lin([lam, mu], [u, v])
    if not ja:
        x[2] += rng.choice([-2, -1, 1, 2])
    erg_ja = mathlib.rang([[u[i], v[i], x[i]] for i in range(3)]) == mathlib.rang([[u[i], v[i]] for i in range(3)])
    assert erg_ja == ja
    zeilen = [(f"\\text{{Komponenten 1, 2: }} \\lambda = {lam},\\ \\mu = {mu}", "aus den ersten beiden Gleichungen")]
    kontrolle = lam * u[2] + mu * v[2]
    zeilen.append((f"{tx(lam)} \\cdot {tx(u[2])} + {tx(mu)} \\cdot {tx(v[2])} = {tx(kontrolle)}", f"dritte Komponente der Kombination; gefordert ist ${tx(x[2])}$"))
    opt = ["Ja, $\\mathbf{x}$ liegt in $\\langle \\mathbf{u}, \\mathbf{v} \\rangle$", "Nein, $\\mathbf{x}$ liegt nicht in $\\langle \\mathbf{u}, \\mathbf{v} \\rangle$"]
    optionen = opt if ja else opt[::-1]
    msg = (f"Mit $\\lambda = {lam}$, $\\mu = {mu}$ passen alle drei Komponenten." if ja else
           f"Die ersten beiden Komponenten erzwingen $\\lambda = {lam}$, $\\mu = {mu}$. Dann ist die dritte Komponente ${kontrolle}$, gefordert ist aber ${x[2]}$.")
    return {"typ": "mc",
            "frage": f"Liegt $\\mathbf{{x}} = {vt(x)}$ in der linearen Hülle $\\langle \\mathbf{{u}}, \\mathbf{{v}} \\rangle$ mit $\\mathbf{{u}} = {vt(u)}$, $\\mathbf{{v}} = {vt(v)}$?",
            "optionen": optionen, "fehler": {optionen[1]: "Das stimmt nicht. " + msg},
            "tipps": ["$\\mathbf{x} \\in \\langle \\mathbf{u}, \\mathbf{v} \\rangle$ heißt: Es gibt $\\lambda, \\mu$ mit $\\lambda\\mathbf{u} + \\mu\\mathbf{v} = \\mathbf{x}$.",
                      "Löse die ersten beiden Komponenten nach $\\lambda, \\mu$ auf.", "Prüfe mit den gefundenen Zahlen die dritte Komponente."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Nach Satz 4.42 besteht die lineare Hülle aus den Linearkombinationen. Ein Gleichungssystem entscheidet."}


k.praxis()

k.generator(linearkombination_bilden, typ="vektor", titel="Linearkombination ausrechnen")
k.generator(polynom_kombination, typ="vektor", titel="Rechnen in K[X]")
k.generator(funktionenraum_wert, typ="zahl", titel="Rechnen im Funktionenraum F")
k.generator(unterraum_entscheiden, typ="mc", titel="Untervektorraum oder nicht?")
k.generator(in_lineare_huelle, typ="mc", titel="Liegt x in der linearen Hülle?")

k.wf("Die Bildcodierungen $(\\mathbb{Q} \\cap [0, 1])^N$ aus der Einleitung des Kapitels (Graustufenbilder mit $N$ Pixeln) bilden einen reellen Vektorraum.", False,
     "Bsp. 4.27: $\\mathbf{e}^{(1)}$ ist eine zulässige Codierung, aber $2\\mathbf{e}^{(1)}$ nicht (Wert $2 > 1$). Für die Vektorrechnung betrachtet man die Bilder im größeren Raum $\\mathbb{R}^N$.",
     tipps=["Skaliere ein Bild mit $\\lambda = 2$: Bleiben alle Werte in $[0, 1]$?"])

_E1N, _E2N = [1, 1, 1], [1, 0, -1]
_SCHN = mathlib.kern([_E1N, _E2N])
assert len(_SCHN) == 1 and _SCHN[0] == [F(1), F(-2), F(1)]

k.rechenweg_aufgabe(r"""
## Übungsblatt-Stil: Schnitt zweier Ebenen

Seien $E_1 = \{\mathbf{x} \in \mathbb{R}^3 \mid x_1 + x_2 + x_3 = 0\}$ und $E_2 = \{\mathbf{x} \in \mathbb{R}^3 \mid x_1 - x_3 = 0\}$.
Zeigen Sie, dass $E_1$ ein Untervektorraum ist, bestimmen Sie $E_1 \cap E_2$ als lineare Hülle und entscheiden Sie über $E_1 \cup E_2$.
""",
    [{"typ": "wf", "frage": "$E_1$ ist ein Untervektorraum von $\\mathbb{R}^3$.", "wahr": True,
      "tipps": ["$\\mathbf{0}$ erfüllt die Gleichung.", "Die Gleichung ist linear und homogen: Summen und Vielfache bleiben drin."],
      "erklaerung": "$\\mathbf{0} \\in E_1$, und aus $u_1 + u_2 + u_3 = 0$, $w_1 + w_2 + w_3 = 0$ folgt $(\\lambda u_1 + \\mu w_1) + (\\lambda u_2 + \\mu w_2) + (\\lambda u_3 + \\mu w_3) = 0$ (Satz 4.32)."},
     {"typ": "vektor", "frage": "Bestimme einen Erzeuger von $E_1 \\cap E_2$: einen Vektor $\\mathbf{s}$ mit $E_1 \\cap E_2 = \\langle \\mathbf{s} \\rangle$ (Normierung: $s_1 = 1$).",
      "loesung": [1, -2, 1], "vielfaches": True,
      "tipps": ["Beide Gleichungen müssen gelten.", "Aus $x_1 - x_3 = 0$ folgt $x_3 = x_1$. Setze das in die erste Gleichung ein."],
      "rechenweg": rechnung([("\\text{Aus } x_1 - x_3 = 0: x_3 = x_1", "zweite Gleichung"), ("\\text{Einsetzen: } x_1 + x_2 + x_1 = 0, \\text{ also } x_2 = -2x_1", "erste Gleichung"),
                             ("1 + (-2) + 1 = 0", "Probe $\\mathbf{s} = (1, -2, 1)^\\top$ in $E_1$")]),
      "typische_fehler": [([1, 2, 1], "Vorzeichen von $x_2$: $2x_1 + x_2 = 0$ ergibt $x_2 = -2x_1$.")]},
     {"typ": "wf", "frage": "$E_1 \\cup E_2$ ist ein Untervektorraum von $\\mathbb{R}^3$.", "wahr": False,
      "tipps": ["Wähle $\\mathbf{u} \\in E_1 \\setminus E_2$ und $\\mathbf{w} \\in E_2 \\setminus E_1$.", "Ist die Summe in $E_1$ oder $E_2$?"],
      "erklaerung": "$\\mathbf{u} = (1, -1, 0)^\\top \\in E_1 \\setminus E_2$ und $\\mathbf{w} = (1, 0, 1)^\\top \\in E_2 \\setminus E_1$. Die Summe $(2, -1, 1)^\\top$ hat Koordinatensumme $2 \\neq 0$ und $x_1 - x_3 = 1 \\neq 0$, liegt also in keiner der beiden Ebenen (Beob. 4.40)."}],
    "Der Schnitt zweier Unterräume ist wieder ein Unterraum (Satz 4.38), die Vereinigung im Allgemeinen nicht (Beob. 4.40).",
    uebungsblatt=True,
    tipps=["Unterraumkriterium: $\\mathbf{0}$ und Abgeschlossenheit.", "Der Schnitt erfüllt beide Gleichungen gleichzeitig."],
    rechenweg=r"""
:::rechnung
1 + (-2) + 1 = 0 || $(1, -2, 1)^\top$ erfüllt $x_1 + x_2 + x_3 = 0$
1 - 1 = 0 || und $x_1 - x_3 = 0$
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Rechenregeln und Schnitt (Sätze 4.30 und 4.38, im Skript „Übung“)

Sei $V$ ein Vektorraum über $K$.

1. Zeigen Sie $\lambda 0 = 0$ für alle $\lambda \in K$ und $(-1)v = -v$ für alle $v \in V$.
2. Zeigen Sie: Aus $\lambda v = 0$ folgt $\lambda = 0$ oder $v = 0$.
3. Seien $U_1, U_2$ Untervektorräume von $V$. Zeigen Sie, dass $U_1 \cap U_2$ ein Untervektorraum ist.
""",
    r"""
**1.** $\lambda 0 = \lambda(0 + 0) = \lambda 0 + \lambda 0$ nach (d1). Addiere $-(\lambda 0)$ auf beiden Seiten: $0 = \lambda 0$.
$v + (-1)v = 1v + (-1)v = (1 + (-1))v = 0v = 0$ nach (e), (d2) und $0v = 0$. Also ist $(-1)v$ das additive Inverse $-v$.

**2.** Sei $\lambda v = 0$ und $\lambda \neq 0$. Dann ist $v = 1v = (\lambda^{-1}\lambda)v = \lambda^{-1}(\lambda v) = \lambda^{-1}0 = 0$ (Axiome (e), (a) und Teil 1).

**3.** $0 \in U_1 \cap U_2$, also ist der Schnitt nicht leer. Seien $u, w \in U_1 \cap U_2$ und $\lambda, \mu \in K$. Da $u, w \in U_1$, liegt $\lambda u + \mu w$ in $U_1$ (Satz 4.32), ebenso in $U_2$. Also liegt es im Schnitt, und Satz 4.32 liefert die Behauptung. $\square$
""",
    ["In 1: $\\lambda 0 = \\lambda 0 + \\lambda 0$ mit (d1) hergeleitet und das Inverse addiert",
     "In 1: $(-1)v + v = 0$ aus (e), (d2) und $0v = 0$ gefolgert",
     "In 2: den Fall $\\lambda \\neq 0$ mit $\\lambda^{-1}$ behandelt (Axiom (a))",
     "In 3: Nichtleerheit ($0 \\in U_1 \\cap U_2$) und Abgeschlossenheit beide gezeigt"],
    "Beweise im Vektorraum verwenden nur die Axiome. Bei Schnitten genügt das Unterraumkriterium für beide Mengen getrennt.",
    uebungsblatt=True,
    tipps=["Starte mit $0 = 0 + 0$ im Körper bzw. $0 = 0 + 0$ im Vektorraum.", "Bei 2 hilft eine Fallunterscheidung: $\\lambda = 0$ oder $\\lambda \\neq 0$."])

k.papier(r"""
## Beweisaufgabe: Satz 4.42 und Polynome

1. Beweisen Sie Satz 4.42: $\langle M \rangle$ ist die Menge $L$ aller Linearkombinationen endlich vieler Vektoren aus $M$. (Zeigen Sie $L$ ist Unterraum, $M \subseteq L$, und $L \subseteq \langle M \rangle$.)
2. Sei $P_{\le 2} = \{p \in \mathbb{R}[X] \mid \text{Grad}(p) \le 2\} \cup \{0\}$. Zeigen Sie mit Satz 4.32, dass $P_{\le 2}$ ein Untervektorraum von $\mathbb{R}[X]$ ist. Warum bilden die Polynome vom Grad **genau** $2$ keinen?
""",
    r"""
**1.** $L$ enthält $0$ (leere Linearkombination) und $M \subseteq L$ ($v = 1v$). Für $x = \sum a_j v^{(j)}$, $y = \sum b_j w^{(j)}$ gilt $\lambda x + \mu y = \sum (\lambda a_j)v^{(j)} + \sum(\mu b_j)w^{(j)} \in L$.
Nach Satz 4.32 ist $L$ ein Unterraum mit $M \subseteq L$, kommt also im Schnitt aus Def. 4.37 vor: $\langle M \rangle \subseteq L$. Umgekehrt enthält jeder Unterraum $U \supseteq M$ alle Linearkombinationen von $M$, also $L \subseteq \langle M \rangle$. Für $M = \emptyset$ bleibt nur $0$.

**2.** Das Nullpolynom liegt in $P_{\le 2}$. Für $p, q \in P_{\le 2}$ hat $\lambda p + \mu q$ keine Potenzen über $X^2$, liegt also in $P_{\le 2}$. Die Polynome vom Grad genau $2$ enthalten das Nullpolynom nicht, und $X^2 + (-X^2) + 1$ hat Grad $0$: Die Summe $X^2 + (-X^2) = 0$ verlässt die Menge.
""",
    ["In 1: $L$ als Unterraum nachgewiesen (Nullvektor und Abgeschlossenheit)",
     "In 1: beide Inklusionen $L \\subseteq \\langle M \\rangle$ und $\\langle M \\rangle \\subseteq L$ begründet",
     "In 2: Nullpolynom und Abgeschlossenheit unter Summe und Vielfachem geprüft",
     "In 2: Gegenbeispiel für „Grad genau $2$“ angegeben (Summe $X^2 + (-X^2)$ bzw. fehlendes Nullpolynom)"],
    "Hüllen beweist man über „kleinster Unterraum“: Ein Unterraum, der $M$ enthält, enthält auch $\\langle M \\rangle$.",
    tipps=["Für $\\langle M \\rangle \\subseteq L$ benutze Def. 4.37: Der Schnitt ist höchstens so groß wie $L$.", "Das Polynom $X^2$ hat Grad $2$, $-X^2$ auch."])

k.zusammenfassung(r"""
## Vektorräume und Untervektorräume (Skript Abschn. 4.2 und 4.3, Def. 4.23 bis Bsp. 4.46)

- **Vektorraum** über $K$ (Def. 4.23): $(V, +)$ abelsche Gruppe, (d1) $\lambda(v + w) = \lambda v + \lambda w$, (d2) $(\lambda + \mu)v = \lambda v + \mu v$, (a) $\lambda(\mu v) = (\lambda\mu)v$, (e) $1v = v$.
- **Beispiele:** $K^n$ (Bsp. 4.24), $\mathbb{C}$ über $\mathbb{R}$ und über $\mathbb{C}$ (4.25), $K[X]$ (4.26), $\mathrm{abb}(M, K)$ punktweise (4.28), $F = \{a + bt\}$ (4.29). Keine Vektorräume: $\mathbb{Z}^2$, Bildcodierungen $(\mathbb{Q} \cap [0, 1])^N$ (4.27).
- **Satz 4.30:** $0v = 0$, $\lambda 0 = 0$, $(-1)v = -v$; $\lambda v = 0 \iff \lambda = 0 \lor v = 0$.
- **Untervektorraum** (Def. 4.31) und **Unterraumkriterium** (Satz 4.32): $U \neq \emptyset$ und $\lambda u + \mu w \in U$.
- Ursprungsgeraden und -ebenen sind Unterräume, ohne Ursprung nicht (Bsp. 4.36). Schnitte von Unterräumen sind Unterräume (Satz 4.38), Vereinigungen im Allgemeinen nicht (Beob. 4.40).
- **Linearkombination** $\sum \lambda_j v^{(j)}$ (Def. 4.41). **Lineare Hülle** $\langle M \rangle$ = Schnitt aller Unterräume $\supseteq M$ (Def. 4.37) = Menge aller Linearkombinationen (Satz 4.42), $\langle \emptyset \rangle = \{0\}$.
- Erzeugendensysteme: $\mathbb{R}^n = \langle \mathbf{e}^{(1)}, \ldots, \mathbf{e}^{(n)} \rangle$, $F = \langle f^{(0)}, f^{(1)} \rangle$, $K[X] = \langle \{X^j\} \rangle$ (Bsp. 4.43 bis 4.46).

!! Bei jedem Unterraum zuerst $\mathbf{0}$ testen. Schnitt: Unterraum. Vereinigung: meist nicht.
""")
