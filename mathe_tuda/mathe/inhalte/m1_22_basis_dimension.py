# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 22: Basen und Dimension (Skript Disser WS 26/27, Abschn. 4.4 und 4.5, Def. 4.47 bis Bsp. 4.76)."""
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(
    slug="basis_dimension",
    titel="Basen und Dimension",
    beschreibung="Lineare Unabhängigkeit, Basis, Koordinatenvektor, Austauschsatz, Basisergänzung, Dimension, Dimensionsformel für Untervektorräume",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 4.4 und 4.5",
    icon="🧭")

tx, vt = mathlib.tex, mathlib.tex_vektor
rang = mathlib.rang


def rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def lin(coeffs, vs):
    return [sum(F(c) * F(v[i]) for c, v in zip(coeffs, vs)) for i in range(len(vs[0]))]


def spalten(vs):
    """Vektoren als Spalten einer Matrix (für lgs_loesen)."""
    return [[v[i] for v in vs] for i in range(len(vs[0]))]


def unabhaengig(vs):
    return rang([list(v) for v in vs]) == len(vs)


def koordinaten(basis, x):
    """[x]_B (exakt) oder None, wenn x nicht in <B>."""
    erg = mathlib.lgs_loesen(spalten(basis), list(x))
    return None if erg["art"] == "keine" else erg["x"]


# ── Beispiele des Skripts nachrechnen ────────────────────────────────────
_E1, _E2 = [1, 0, 0], [0, 1, 0]
assert lin([1, 1, -1], [_E1, _E2, [1, 1, 0]]) == [0, 0, 0]                       # Bsp. 4.50
assert not unabhaengig([_E1, _E2, [1, 1, 0]]) and unabhaengig([_E1, _E2]) and unabhaengig([[1, 0, 0]])
assert not unabhaengig([[0, 0, 0]])                                                # Bsp. 4.49 (Nullvektor)
# Bsp. 4.51: a + bt = 0 für alle t: Auswerten bei t = 0 und t = 1
assert mathlib.lgs_loesen([[1, 0], [1, 1]], [0, 0])["x"] == [0, 0]
# Bsp. 4.59: E1 = {x1 + x2 = 0} hat die Basis ((1, -1, 0), (0, 0, 1))
assert unabhaengig([[1, -1, 0], [0, 0, 1]])
# Einleitung 4.7 / Bsp. 4.100: B = ((1,1),(1,0)), x = (2, 1) hat [x]_B = (1, 1)
assert koordinaten([[1, 1], [1, 0]], [2, 1]) == [1, 1]
# Bsp. 4.62: f(t) = a + bt hat [f]_B = (a, b) bezüglich (f0, f1); Vertauschen ergibt (b, a)
assert koordinaten([[1, 0], [0, 1]], [3, -2]) == [3, -2]
# Bsp. 4.76: dim E1 = dim E2 = 2, dim(E1 ∩ E2) = 1, dim(E1 + E2) = 3
_E1B, _E2B = [[1, -1, 0], [0, 0, 1]], [[1, 0, -1], [0, 1, -1]]
assert rang(_E1B + _E2B) == 3 and 2 + 2 - 1 == 3
assert rang([[1, -1, 1]]) == 1 and _E1B[0][0] + _E1B[0][1] == 0

k.lernziele([
    "Ich kann prüfen, ob Vektoren linear unabhängig sind, und eine Linearkombination angeben, die $0$ ergibt (Def. 4.47, Bsp. 4.49 bis 4.51, Satz 4.52)",
    "Ich kann entscheiden, ob eine Menge eine Basis ist, und weiß, warum jeder Vektor genau ein Koordinatentupel hat (Def. 4.54, Satz 4.55, Def. 4.61)",
    "Ich kann Koordinatenvektoren $[v]_{\\mathfrak{B}}$ in $K^n$, im Funktionenraum $F$ und in $\\mathbb{C}$ bestimmen (Bsp. 4.58 bis 4.63)",
    "Ich kenne Austauschsatz, Basisergänzung und Dimension und kann Dimensionen bestimmen (Satz 4.64, Kor. 4.65, 4.66, Def. 4.67, Satz 4.73, 4.74)",
    "Ich kann die Dimensionsformel für Untervektorräume anwenden und beweisen (Satz 4.75)",
])

k.warum(r"""
Eine Basis ist die kleinste vollständige Beschreibung: so viele Zahlen, wie der Raum Dimension hat, nicht mehr. Ein Bild mit $64 \times 64$ Pixeln lebt im $\mathbb{R}^{4096}$,
und eine Kompression sucht eine Basis, in der die meisten Koordinaten fast $0$ sind (Fourier, Wavelets, Haar). Beim maschinellen Lernen heißt „Merkmal überflüssig“: Der Vektor
ist linear abhängig von den anderen. Koordinaten sind die Zahlen, die dein Programm tatsächlich speichert.
""")

# ── Seite 1: lineare Unabhängigkeit ──────────────────────────────────────
k.erklaerung("Lineare Unabhängigkeit", r"""
## Definition 4.47, Beobachtung 4.48, Beispiele 4.49 bis 4.51

:::analogie 🎨 Farben mischen
Aus Rot und Blau kannst du Violett mischen, Violett ist also überflüssig. Rot und Blau lassen sich nicht auseinander mischen: Sie sind unabhängig.
:::

Eine Menge $M \subseteq V$ heißt [[linear unabhängig]], wenn für paarweise verschiedene $v^{(1)}, \ldots, v^{(m)} \in M$ gilt: Aus $\sum_{j} \lambda_j v^{(j)} = 0$ folgt $\lambda = 0$.
Anders gesagt: **Nur die triviale Kombination ergibt $0$.** Sonst heißt $M$ [[linear abhängig]].

:::rechnung Beispiel 4.50: $\{\mathbf{e}^{(1)}, \mathbf{e}^{(2)}, \mathbf{e}^{(1)} + \mathbf{e}^{(2)}\}$ ist abhängig
1 \cdot 1 + 1 \cdot 0 + (-1) \cdot 1 = 0 || erste Komponente von $1\mathbf{e}^{(1)} + 1\mathbf{e}^{(2)} + (-1)(\mathbf{e}^{(1)} + \mathbf{e}^{(2)})$
1 \cdot 0 + 1 \cdot 1 + (-1) \cdot 1 = 0 || zweite Komponente
1 \cdot 0 + 1 \cdot 0 + (-1) \cdot 0 = 0 || dritte Komponente: nichttriviale Kombination mit Ergebnis $\mathbf{0}$
:::

Beobachtung 4.48: Teilmengen unabhängiger Mengen sind unabhängig, Obermengen abhängiger Mengen sind abhängig. Bsp. 4.49: $\emptyset$ ist unabhängig; jede Menge mit $\mathbf{0}$ ist abhängig ($1 \cdot \mathbf{0} = \mathbf{0}$). Bsp. 4.51: $f^{(0)}(t) = 1$ und $f^{(1)}(t) = t$ sind unabhängig: Aus $a + bt = 0$ für alle $t$ folgt $a = 0$ ($t = 0$) und $b = 0$ ($t = 1$).

:::alt Als Redundanz
Eine abhängige Menge hat einen **überflüssigen** Vektor: Er steckt schon in den anderen. Bei Datenbanken: Eine Spalte, die sich aus den anderen berechnen lässt, enthält keine neue Information.
:::
""")

k.mehrfach("Welche Mengen sind linear unabhängig?",
           ["$\\{(1, 0, 0)^\\top, (0, 1, 0)^\\top\\}$", "$\\{(1, 2)^\\top\\}$", "$\\emptyset$"],
           ["$\\{(1, 2)^\\top, (2, 4)^\\top\\}$", "$\\{(1, 0)^\\top, (0, 1)^\\top, (1, 1)^\\top\\}$", "$\\{(0, 0)^\\top, (1, 1)^\\top\\}$"],
           "Unabhängig: kein Vektor ist Kombination der anderen. $(2, 4)^\\top = 2(1, 2)^\\top$, $(1, 1)^\\top = (1, 0)^\\top + (0, 1)^\\top$, und der Nullvektor macht jede Menge abhängig. $\\emptyset$ ist unabhängig (Bsp. 4.49).",
           tipps=["Suche einen Vektor, der Vielfaches oder Kombination der anderen ist.", "Mehr als $2$ Vektoren im $\\mathbb{R}^2$ gehen nicht (Austauschsatz).", "Der Nullvektor ist immer abhängig."],
           fehler={"$\\{(1, 2)^\\top, (2, 4)^\\top\\}$": "$(2, 4)^\\top = 2 \\cdot (1, 2)^\\top$: nichttriviale Kombination $2 \\cdot (1, 2) - (2, 4) = \\mathbf{0}$.",
                   "$\\{(1, 0)^\\top, (0, 1)^\\top, (1, 1)^\\top\\}$": "$(1, 1)^\\top = (1, 0)^\\top + (0, 1)^\\top$, also abhängig.",
                   "$\\{(0, 0)^\\top, (1, 1)^\\top\\}$": "$1 \\cdot \\mathbf{0} + 0 \\cdot (1, 1)^\\top = \\mathbf{0}$ ist nichttrivial (Bsp. 4.49)."})

k.zahl("Für welches $\\lambda \\in \\mathbb{R}$ ist $\\{(1, 2)^\\top, (3, \\lambda)^\\top\\}$ linear abhängig?", 6,
       "Zwei Vektoren sind genau dann abhängig, wenn einer ein Vielfaches des anderen ist: $(3, \\lambda)^\\top = 3 \\cdot (1, 2)^\\top = (3, 6)^\\top$, also $\\lambda = 6$.",
       tipps=["Abhängig heißt hier: parallel.", "Welcher Faktor macht aus der $1$ die $3$?", "Wende denselben Faktor auf die $2$ an."],
       rechenweg=rechnung([("3 \\cdot 1 = 3", "erste Komponente bestimmt den Faktor $3$"), ("3 \\cdot 2 = 6", "zweite Komponente: $\\lambda = 6$")]),
       typische_fehler=[(F(3, 2), "Das ist $3 : 2$. Du musst die $2$ mit dem Faktor $3$ multiplizieren."), (5, "Parallel heißt Vielfaches (Faktor), nicht um $2$ verschoben.")])

k.wf("Jede Menge $M \\subseteq V$, die den Nullvektor enthält, ist linear abhängig.", True,
     "Mit $m = 1$, $v^{(1)} = \\mathbf{0}$ und $\\lambda = (1)$ gilt $1 \\cdot \\mathbf{0} = \\mathbf{0}$ mit $\\lambda \\neq 0$ (Bsp. 4.49).",
     tipps=["Eine einzige nichttriviale Kombination, die $\\mathbf{0}$ ergibt, genügt."])

# ── Seite 2: Satz 4.52, Korollar 4.53 ────────────────────────────────────
k.erklaerung("Abhängig heißt: ein Vektor ist überflüssig", r"""
## Satz 4.52 und Korollar 4.53

**Satz 4.52.** $M$ ist genau dann linear abhängig, wenn es ein $v \in M$ mit $v \in \langle M \setminus \{v\} \rangle$ gibt.

*Beweis „$\Rightarrow$“:* Aus $\sum_j \lambda_j v^{(j)} = 0$ mit $\lambda_k \neq 0$ folgt durch Auflösen $v^{(k)} = \sum_{j \neq k} (-\lambda_j / \lambda_k)\, v^{(j)}$.
*„$\Leftarrow$“:* Ist $v \in \langle M \setminus \{v\} \rangle$, so ist $v$ nach Satz 4.42 eine Linearkombination anderer Vektoren. Subtrahiert man sie, bleibt eine Kombination mit Koeffizient $1 \neq 0$ bei $v$, die $0$ ergibt. $\square$

**Korollar 4.53 (Ergänzungskriterium).** Ist $L$ linear unabhängig und $w \notin L$, so ist $L \cup \{w\}$ genau dann linear unabhängig, wenn $w \notin \langle L \rangle$.

:::rechnung Beispiel: $L = \{(1, 0, 0)^\top, (0, 1, 0)^\top\}$, $w = (2, 3, 1)^\top$. Gilt $w \in \langle L \rangle$?
\text{(I) } a = 2 || erste Komponente: $a \cdot 1 + b \cdot 0 = 2$
\text{(II) } b = 3 || zweite Komponente: $a \cdot 0 + b \cdot 1 = 3$
2 \cdot 0 + 3 \cdot 0 = 0 || dritte Komponente der Kombination ist $0$, gefordert $1$: $w \notin \langle L \rangle$, also $L \cup \{w\}$ unabhängig
:::

:::alt Als Reichweite
$\langle L \rangle$ ist alles, was du mit $L$ erreichst. Liegt $w$ schon in Reichweite, bringt es nichts Neues und macht die Menge abhängig. Liegt $w$ außerhalb, wird die Reichweite größer, und die Menge bleibt unabhängig.
:::
""")

k.ordnen("Ordne den Beweis von Satz 4.52, Richtung „$\\Rightarrow$“: $M$ linear abhängig $\\Rightarrow$ es gibt $v \\in M$ mit $v \\in \\langle M \\setminus \\{v\\} \\rangle$.",
         ["Da $M$ linear abhängig ist, gibt es paarweise verschiedene $v^{(1)}, \\ldots, v^{(m)} \\in M$ und $\\lambda \\in K^m \\setminus \\{0\\}$ mit $\\sum_{j=1}^m \\lambda_j v^{(j)} = 0$.",
          "Sei $\\lambda_k \\neq 0$. Wir bringen alle Summanden mit $j \\neq k$ auf die rechte Seite: $\\lambda_k v^{(k)} = -\\sum_{j \\neq k} \\lambda_j v^{(j)}$.",
          "Multiplikation mit $\\lambda_k^{-1}$ ergibt $v^{(k)} = \\sum_{j \\neq k} \\left(-\\frac{\\lambda_j}{\\lambda_k}\\right) v^{(j)}$.",
          "Also ist $v^{(k)}$ eine Linearkombination von Vektoren aus $M \\setminus \\{v^{(k)}\\}$.",
          "Nach Satz 4.42 liegt $v^{(k)}$ damit in $\\langle M \\setminus \\{v^{(k)}\\} \\rangle$. $\\square$"],
         "Aus einer nichttrivialen Kombination, die $0$ ergibt, löst man einen Vektor mit Koeffizient $\\neq 0$ auf.",
         ablenker=["Da alle $\\lambda_j \\neq 0$ sind, darf man durch jedes $\\lambda_j$ teilen.", "Wir teilen durch $\\lambda_j$, auch wenn $\\lambda_j = 0$ ist."],
         tipps=["Beginne mit der Definition der linearen Abhängigkeit.", "Nur ein Koeffizient $\\lambda_k \\neq 0$ ist garantiert, nicht alle.", "Satz 4.42: Hüllen bestehen aus Linearkombinationen."])

# ── Seite 3: Basis ───────────────────────────────────────────────────────
k.erklaerung("Basis", r"""
## Definition 4.54 und Beobachtung 4.56, 4.57, Beispiele 4.58 bis 4.60

:::analogie 🧱 Kleinster Bausatz
Eine [[Basis|Basis (Vektorraum)]] ist ein Bausatz ohne überflüssiges Teil, mit dem sich **alles** bauen lässt: Weniger geht nicht mehr, mehr wäre Verschwendung.
:::

Eine **Basis** von $V$ ist eine linear unabhängige Menge $B \subseteq V$ mit $\langle B \rangle = V$. Eine endliche Basis, in feste Reihenfolge gebracht, heißt **geordnete Basis** $\mathfrak{B} = (b^{(1)}, \ldots, b^{(n)})$. $\emptyset$ ist Basis von $\{0\}$.

- Beob. 4.56: Eine Basis ist ein **minimales** Erzeugendensystem.
- Beob. 4.57: Eine Basis ist eine **maximale** linear unabhängige Menge.
- Bsp. 4.58: $\{\mathbf{e}^{(1)}, \ldots, \mathbf{e}^{(n)}\}$ ist die **Standardbasis** von $K^n$, geordnet $\mathfrak{E}$.
- Bsp. 4.59: $\left((1, -1, 0)^\top, (0, 0, 1)^\top\right)$ ist Basis von $E_1 = \{x_1 + x_2 = 0\}$.
- Bsp. 4.60: Die Monome $\{X^j \mid j \in \mathbb{N}\}$ bilden eine (unendliche) Basis von $K[X]$.

:::rechnung Beispiel 4.59: unabhängig, denn $a(1, -1, 0)^\top + b(0, 0, 1)^\top = \mathbf{0}$ erzwingt $a = b = 0$
\text{erste Komponente: } a = 0 || $a \cdot 1 + b \cdot 0 = 0$ 
\text{zweite Komponente: } -a = 0 || sie muss $0$ sein, also $a = 0$
\text{dritte Komponente: } b = 0 || $0 \cdot a + 1 \cdot b = 0$
:::

:::alt Als Koordinatensystem
Eine Basis legt Achsen fest: So viele Richtungen wie nötig, keine doppelt. Schief oder mit anderer Einheit ist erlaubt, nur muss jeder Punkt auf genau eine Weise erreichbar sein.
:::
""")

k.mc("Welche Menge ist eine Basis des $\\mathbb{R}^2$?",
     ["$\\{(1, 1)^\\top, (1, -1)^\\top\\}$", "$\\{(1, 2)^\\top, (2, 4)^\\top\\}$", "$\\{(1, 0)^\\top, (0, 1)^\\top, (1, 1)^\\top\\}$", "$\\{(1, 1)^\\top\\}$"],
     "Eine Basis ist unabhängig **und** erzeugend. $(1, 1)^\\top$ und $(1, -1)^\\top$ sind unabhängig und erzeugen $\\mathbb{R}^2$. Die anderen: parallel, zu viele (abhängig), zu wenige (erzeugt nur eine Gerade).",
     tipps=["Zwei Bedingungen: unabhängig und erzeugend.", "Im $\\mathbb{R}^2$ braucht man genau zwei Vektoren.", "Sind beide parallel?"],
     fehler={"$\\{(1, 2)^\\top, (2, 4)^\\top\\}$": "Die beiden Vektoren sind parallel ($(2, 4) = 2 \\cdot (1, 2)$): linear abhängig, keine Basis.",
             "$\\{(1, 0)^\\top, (0, 1)^\\top, (1, 1)^\\top\\}$": "Erzeugend, aber linear abhängig: $(1, 1) = (1, 0) + (0, 1)$. Ein Vektor ist überflüssig.",
             "$\\{(1, 1)^\\top\\}$": "Unabhängig, aber nicht erzeugend: $\\langle (1, 1)^\\top \\rangle$ ist nur eine Gerade."})

# ── Seite 4: Satz 4.55 und Koordinaten ───────────────────────────────────
k.erklaerung("Eindeutige Darstellung und Koordinatenvektor", r"""
## Satz 4.55 und Definition 4.61

**Satz 4.55.** $\mathfrak{B} = (b^{(1)}, \ldots, b^{(n)})$ ist genau dann eine geordnete Basis von $V$, wenn zu jedem $v \in V$ **genau ein** Tupel $(x_1, \ldots, x_n) \in K^n$ mit $v = \sum_j x_j b^{(j)}$ existiert.

*Beweis „$\Rightarrow$“:* Die Existenz liefert $\langle B \rangle = V$. Gibt es zwei Darstellungen $\sum x_j b^{(j)} = \sum y_j b^{(j)}$, so folgt durch Subtraktion $\sum (x_j - y_j)b^{(j)} = 0$ und aus der linearen Unabhängigkeit $x_j = y_j$.
*„$\Leftarrow$“:* Eindeutigkeit der Darstellung von $0 = \sum 0 \cdot b^{(j)}$ liefert die Unabhängigkeit, die Existenz die Erzeugung. $\square$

Das Tupel heißt **Koordinatenvektor** $[v]_{\mathfrak{B}} := (x_1, \ldots, x_n)^\top \in K^n$ ([[Koordinatenvektor]]). Für die Standardbasis ist $[\mathbf{x}]_{\mathfrak{E}} = \mathbf{x}$.

:::achtung Basis und Reihenfolge gehören dazu
$[v]_{\mathfrak{B}}$ ist nur mit der Angabe der Basis eine Zahlenliste. Vertauschst du die Basisvektoren, vertauschen sich die Koordinaten. Der Vektor $v$ selbst bleibt gleich.
:::

:::rechnung Beispiel: $\mathfrak{B} = ((1, 1)^\top, (1, 0)^\top)$ und $\mathbf{x} = (2, 1)^\top$
\text{zweite Komponente: } x_1 = 1 || Die zweite Komponente der Kombination $x_1 b^{(1)} + x_2 b^{(2)}$ ist $x_1 \cdot 1 + x_2 \cdot 0$
\text{erste Komponente: } 1 + x_2 = 2 || also $x_2 = 1$
1 \cdot 1 + 1 \cdot 1 = 2 || Probe, also $[\mathbf{x}]_{\mathfrak{B}} = (1, 1)^\top$
:::

:::alt Als Postleitzahl
Die Basis ist das Adresssystem, die Koordinaten sind die Adresse. Ein Punkt hat in einem System genau eine Adresse. Wechselst du das System, bleibt der Punkt, aber die Adresse ändert sich.
:::
""")

k.ordnen("Ordne den Beweis von Satz 4.55, Richtung „$\\Rightarrow$“: Ist $\\mathfrak{B}$ eine geordnete Basis, so hat jedes $v$ genau eine Darstellung.",
         ["Wegen $\\langle B \\rangle = V$ hat jedes $v$ nach Satz 4.42 eine Darstellung $v = \\sum_j x_j b^{(j)}$ (nicht benötigte Vektoren mit Koeffizient $0$).",
          "Seien $v = \\sum_j x_j b^{(j)}$ und $v = \\sum_j y_j b^{(j)}$ zwei Darstellungen.",
          "Subtraktion liefert $\\sum_j (x_j - y_j) b^{(j)} = 0$.",
          "Wegen der linearen Unabhängigkeit der $b^{(j)}$ gilt $x_j - y_j = 0$ für alle $j$.",
          "Also ist $x_j = y_j$ für alle $j$: Die Darstellung ist eindeutig. $\\square$"],
         "Existenz kommt aus der Erzeugung, Eindeutigkeit aus der Unabhängigkeit.",
         ablenker=["Wegen $\\langle B \\rangle = V$ ist die Darstellung automatisch eindeutig, ein Vergleich zweier Darstellungen ist nicht nötig."],
         tipps=["Existenz und Eindeutigkeit werden getrennt gezeigt.", "Für Eindeutigkeit nimmt man zwei Darstellungen an und zeigt, dass sie gleich sind.", "Subtrahieren und die lineare Unabhängigkeit anwenden."])

k.vektor("Bestimme den Koordinatenvektor $[\\mathbf{x}]_{\\mathfrak{B}}$ von $\\mathbf{x} = (5, 2)^\\top$ bezüglich $\\mathfrak{B} = \\left((1, 1)^\\top, (1, 0)^\\top\\right)$.",
         koordinaten([[1, 1], [1, 0]], [5, 2]),
         "Gesucht $x_1, x_2$ mit $x_1(1, 1)^\\top + x_2(1, 0)^\\top = (5, 2)^\\top$. Zweite Komponente: $x_1 = 2$. Erste: $2 + x_2 = 5$, also $x_2 = 3$. Probe: $2 \\cdot 1 + 3 \\cdot 1 = 5$ und $2 \\cdot 1 + 3 \\cdot 0 = 2$.",
         tipps=["Schreibe $x_1 b^{(1)} + x_2 b^{(2)} = \\mathbf{x}$ komponentenweise auf.", "Die zweite Komponente enthält nur $x_1$.", "$x_1 = 2$, dann $2 + x_2 = 5$."],
         rechenweg=rechnung([("2 \\cdot 1 + 3 \\cdot 1 = 5", "erste Komponente der Probe"), ("2 \\cdot 1 + 3 \\cdot 0 = 2", "zweite Komponente der Probe")]),
         typische_fehler=[([3, 2], "Die Koordinaten stehen in der Reihenfolge der Basis: $x_1$ gehört zu $b^{(1)} = (1, 1)^\\top$."),
                          ([5, 2], "Das ist $\\mathbf{x}$ selbst, also $[\\mathbf{x}]_{\\mathfrak{E}}$ bezüglich der Standardbasis, nicht bezüglich $\\mathfrak{B}$.")])

# ── Seite 5: Koordinaten in Funktionen und ℂ ─────────────────────────────
k.erklaerung("Koordinaten in Funktionenraum und ℂ", r"""
## Beispiele 4.62 und 4.63

Ein Vektor muss keine Zahlenliste sein: Seine Koordinaten sind es immer.

**Beispiel 4.62.** Im Funktionenraum $F = \{t \mapsto a + bt\}$ ist $\mathfrak{B} = (f^{(0)}, f^{(1)})$ mit $f^{(0)}(t) = 1$, $f^{(1)}(t) = t$ eine geordnete Basis. Für $f(t) = a + bt$ ist $[f]_{\mathfrak{B}} = (a, b)^\top$.
Vertauscht man die Basisvektoren, vertauschen sich die Koordinaten: $[f]_{(f^{(1)}, f^{(0)})} = (b, a)^\top$.

**Beispiel 4.63.** Über $\mathbb{R}$ ist $\{1, i\}$ eine Basis von $\mathbb{C}$ mit $[a + bi]_{(1, i)} = (a, b)^\top$. Über $\mathbb{C}$ genügt $\{1\}$: $[z]_{(1)} = (z)$.

:::rechnung $f(t) = 3 - 2t$ bezüglich $\mathfrak{B} = (f^{(0)}, f^{(1)})$
3 \cdot 1 + (-2) \cdot 0 = 3 || Wert bei $t = 0$ liefert den Koeffizienten $a = 3$
3 \cdot 1 + (-2) \cdot 1 = 1 || Wert bei $t = 1$: $f(1) = a + b = 1$, also $b = -2$
3 + (-2) \cdot 2 = -1 || Probe bei $t = 2$: $f(2) = -1$, Koordinaten $[f]_{\mathfrak{B}} = (3, -2)^\top$
:::

:::alt Als Dateiformat
Ein Polynom wird als Array der Koeffizienten gespeichert: `[3, -2]` steht für $3 - 2t$. Die Basis (Monome) steht nicht in der Datei, sie ist das **Format**. Eine andere Basis bedeutet ein anderes Format für dieselbe Funktion.
:::
""")

k.vektor("Bestimme $[f]_{\\mathfrak{B}'}$ für $f(t) = 3 - 2t$ bezüglich der **vertauschten** Basis $\\mathfrak{B}' = (f^{(1)}, f^{(0)})$ mit $f^{(0)}(t) = 1$ und $f^{(1)}(t) = t$.",
         [-2, 3],
         "$f = (-2) \\cdot f^{(1)} + 3 \\cdot f^{(0)}$. Die Koordinaten folgen der Reihenfolge der Basis: erst der Koeffizient von $f^{(1)}$, dann der von $f^{(0)}$.",
         tipps=["Lies die Koeffizienten von $f$ ab: konstanter Teil, Teil bei $t$.", "Die erste Koordinate gehört zum ersten Basisvektor $f^{(1)}(t) = t$.", "$(-2, 3)$."],
         rechenweg=rechnung([("(-2) \\cdot 2 + 3 \\cdot 1 = -1", "Probe bei $t = 2$: $f(2) = -1$")]),
         typische_fehler=[([3, -2], "Das sind die Koordinaten bezüglich $(f^{(0)}, f^{(1)})$. Bei vertauschter Basis vertauschen sich die Einträge.")])

k.mc("Wie lauten $\\dim_{\\mathbb{R}} \\mathbb{C}$ und $\\dim_{\\mathbb{C}} \\mathbb{C}$?",
     ["$2$ und $1$", "$1$ und $2$", "beide $1$", "beide $2$"],
     "Über $\\mathbb{R}$ ist $\\{1, i\\}$ eine Basis, über $\\mathbb{C}$ genügt $\\{1\\}$ (Bsp. 4.63, 4.71). Die Dimension hängt vom Skalarkörper ab.",
     tipps=["Welche Skalare sind erlaubt: nur reelle oder alle komplexen?", "Über $\\mathbb{C}$ ist $i = i \\cdot 1$."],
     fehler={"$1$ und $2$": "Verwechselt: Je mehr Skalare du hast, desto weniger Basisvektoren brauchst du. Über $\\mathbb{C}$ ist $i = i \\cdot 1$.",
             "beide $1$": "Über $\\mathbb{R}$ ist $i$ kein reelles Vielfaches von $1$, also braucht man zwei Basisvektoren.",
             "beide $2$": "Über $\\mathbb{C}$ ist $i = i \\cdot 1$ ein Vielfaches von $1$: $\\{1\\}$ reicht."})

# ── Seite 6: Austauschsatz ───────────────────────────────────────────────
k.erklaerung("Austauschsatz", r"""
## Satz 4.64 und Korollar 4.65

Alle Basen sollen gleich viele Elemente haben. Dafür vergleichen wir unabhängige Mengen mit Erzeugendensystemen.

**Satz 4.64 (Austauschsatz).** Ist $E$ ein endliches Erzeugendensystem von $V$, so ist jede linear unabhängige Menge $L \subseteq V$ endlich, und $|L| \le |E|$.

*Beweisidee:* Wäre $|L| > n := |E|$, so gäbe es unabhängiges $L_0 \subseteq L$ mit $n + 1$ Elementen. Wähle unter allen Erzeugendensystemen $F$ mit $n$ Elementen eines mit möglichst vielen Elementen aus $L_0$. Ein $v \in L_0 \setminus F$ lässt sich aus $F$ kombinieren; ein Basisvektor $w^{(k)} \in F \setminus L_0$ kann durch $v$ ersetzt werden. Das ergibt ein Erzeugendensystem mit noch mehr Elementen aus $L_0$: Widerspruch.

**Korollar 4.65.** Alle Basen eines endlich erzeugten Vektorraums sind endlich und haben **gleich viele** Elemente, denn $|B| \le |C|$ und $|C| \le |B|$.

:::rechnung Anwendung: Warum gibt es im $\mathbb{R}^3$ keine vier unabhängigen Vektoren?
\text{Erzeugendensystem mit 3 Elementen} || die Standardbasis $\{\mathbf{e}^{(1)}, \mathbf{e}^{(2)}, \mathbf{e}^{(3)}\}$
4 \le 3 \text{ ist falsch} || eine unabhängige Menge dürfte höchstens $3$ Elemente haben: vier Vektoren im $\mathbb{R}^3$ sind abhängig
:::

:::alt Als Parkplatz
$E$ sind die Parkplätze, $L$ die Autos, die unabhängig stehen müssen. Hat dein Erzeugendensystem $n$ Plätze, passen höchstens $n$ unabhängige Autos hinein, und man kann ein Auto gegen einen Platz „austauschen“.
:::
""")

k.ordnen("Ordne den Beweis des Austauschsatzes (Satz 4.64): $E$ endliches Erzeugendensystem mit $n = |E| \\ge 1$, $L$ linear unabhängig. Zu zeigen: $|L| \\le n$.",
         ["Angenommen, $|L| > n$. Dann gibt es eine linear unabhängige Menge $L_0 \\subseteq L$ mit $|L_0| = n + 1$.",
          "Unter allen Erzeugendensystemen $F$ mit $|F| = n$ wählen wir eines mit größtem $|F \\cap L_0|$ (möglich: $F = E$ ist zulässig).",
          "Wegen $|L_0| > |F|$ gibt es $v \\in L_0 \\setminus F$. Mit $F = \\{w^{(1)}, \\ldots, w^{(n)}\\}$ gilt $v = \\sum_j \\lambda_j w^{(j)}$.",
          "Da $(F \\cap L_0) \\cup \\{v\\}$ unabhängig ist, folgt mit Korollar 4.53, dass $v \\notin \\langle F \\cap L_0 \\rangle$. Also ist $\\lambda_k \\neq 0$ für ein $w^{(k)} \\in F \\setminus L_0$.",
          "Auflösen nach $w^{(k)}$ zeigt, dass $F' := (F \\setminus \\{w^{(k)}\\}) \\cup \\{v\\}$ ein Erzeugendensystem mit $|F'| = n$ und $|F' \\cap L_0| = |F \\cap L_0| + 1$ ist.",
          "Das widerspricht der Wahl von $F$. Also gilt $|L| \\le n$. $\\square$"],
         "Widerspruchsbeweis: Austauschen eines Vektors aus $F \\setminus L_0$ gegen $v \\in L_0$ vergrößert $|F \\cap L_0|$, obwohl dieses schon maximal war.",
         ablenker=["Wir wählen $F$ mit kleinstem $|F \\cap L_0|$, damit möglichst viele Vektoren ausgetauscht werden können.", "Da $v \\in F$ gilt, ist der Austausch überflüssig."],
         tipps=["Es ist ein Widerspruchsbeweis: Die Annahme steht am Anfang, der Widerspruch am Ende.", "Das Maximum von $|F \\cap L_0|$ wird gebraucht, um zu widersprechen.",
                "Korollar 4.53 sagt, wann ein Vektor außerhalb der Hülle liegt."])

# ── Seite 7: Basisergänzung und Dimension ────────────────────────────────
k.erklaerung("Basisergänzung und Dimension", r"""
## Korollar 4.66, Definition 4.67, Beispiele 4.68 bis 4.72

**Korollar 4.66 (Basisauswahl und -ergänzung).** Ist $E$ ein endliches Erzeugendensystem und $L$ linear unabhängig, so gibt es eine Basis $B$ mit $L \subseteq B \subseteq L \cup E$.
*Beweis:* Wähle $B$ unabhängig mit $L \subseteq B \subseteq L \cup E$ und größter Elementzahl. Wäre $\langle B \rangle \neq V$, läge ein $w \in E$ außerhalb, und $B \cup \{w\}$ wäre nach Kor. 4.53 unabhängig und größer. $\square$

Die Anzahl der Basiselemente ist wohldefiniert (Kor. 4.65): Die [[Dimension]] $\dim_K V := |B|$. Ohne endliche Basis heißt $V$ unendlichdimensional.

| Raum | Basis | Dimension |
|---|---|---|
| $K^n$ (Bsp. 4.68) | Standardbasis | $n$ |
| Gerade, Ebene durch $0$ in $\mathbb{R}^n$ (4.69) | $\{u\}$, $\{u, v\}$ | $1$, $2$ |
| $F$ (Bsp. 4.70) | $\{f^{(0)}, f^{(1)}\}$ | $2$ |
| $\mathbb{C}$ (Bsp. 4.71) | $\{1, i\}$ bzw. $\{1\}$ | $\dim_{\mathbb{R}} = 2$, $\dim_{\mathbb{C}} = 1$ |
| $K[X]$ (Bsp. 4.72) | Monome | $\infty$ |

:::rechnung Beispiel 4.72: $K[X]$ ist unendlichdimensional
\text{n + 1 > n} || es gibt $n + 1$ unabhängige Monome $X^0, \ldots, X^n$, aber ein Erzeugendensystem mit $n$ Vektoren erlaubt höchstens $n$ unabhängige
:::

:::alt Als Freiheitsgrade
Die Dimension zählt, wie viele Zahlen du festlegen musst, um einen Punkt zu beschreiben: Gerade $1$, Ebene $2$, Raum $3$. Ein Polynom beliebigen Grades braucht beliebig viele.
:::
""")

k.wf("Im $\\mathbb{R}^3$ gibt es vier Vektoren, die linear unabhängig sind.", False,
     "Der $\\mathbb{R}^3$ hat das Erzeugendensystem $\\{\\mathbf{e}^{(1)}, \\mathbf{e}^{(2)}, \\mathbf{e}^{(3)}\\}$ mit $3$ Elementen. Nach dem Austauschsatz hat jede linear unabhängige Menge höchstens $3$ Elemente.",
     tipps=["Denke an den Austauschsatz und die Standardbasis."])

k.zahl("Bestimme $\\dim \\langle (1, 2, 3)^\\top, (2, 4, 6)^\\top, (0, 1, 1)^\\top \\rangle$.", 2,
       "Der zweite Vektor ist $2 \\cdot (1, 2, 3)^\\top$, überflüssig. $\\{(1, 2, 3)^\\top, (0, 1, 1)^\\top\\}$ ist unabhängig (nicht parallel) und erzeugt dieselbe Hülle: Dimension $2$.",
       tipps=["Streiche überflüssige Vektoren.", "Welcher Vektor ist ein Vielfaches eines anderen?", "Bleiben zwei unabhängige übrig?"],
       rechenweg=rechnung([("2 \\cdot 1 = 2", "$(2, 4, 6)^\\top = 2 \\cdot (1, 2, 3)^\\top$, erste Komponente (zweite $2 \\cdot 2 = 4$, dritte $2 \\cdot 3 = 6$)")]),
       typische_fehler=[(3, "Du hast die Vektoren gezählt. Die Dimension zählt die **unabhängigen** Vektoren: $(2, 4, 6)^\\top = 2 \\cdot (1, 2, 3)^\\top$ ist überflüssig.")])

# ── Seite 8: Sätze 4.73 und 4.74 ─────────────────────────────────────────
k.erklaerung("Dimension und Unterräume", r"""
## Satz 4.73 und Satz 4.74

**Satz 4.73.** Sei $\dim V = n$ und $M \subseteq V$ mit $|M| = n$. Dann sind äquivalent: $M$ ist Basis; $M$ ist linear unabhängig; $\langle M \rangle = V$.
Bei der richtigen Anzahl genügt also **eine** der beiden Basiseigenschaften (im Skript Übung).

**Satz 4.74.** Jeder Untervektorraum $U$ eines endlichdimensionalen $V$ ist endlichdimensional, $\dim U \le \dim V$, und Gleichheit gilt genau dann, wenn $U = V$.

*Beweisidee:* Nach dem Austauschsatz haben unabhängige Teilmengen von $U$ höchstens $n$ Elemente. Eine unabhängige Menge $L \subseteq U$ größter Elementzahl ist eine Basis von $U$, sonst könnte man (Kor. 4.53) einen Vektor hinzufügen. Bei $\dim U = n$ ist $L$ nach Satz 4.73 auch Basis von $V$.

:::rechnung Anwendung: Ist $\{(1, 2)^\top, (3, 1)^\top\}$ eine Basis des $\mathbb{R}^2$?
1 \cdot 1 - 2 \cdot 3 = -5 || die Vektoren sind nicht parallel (Determinante $\ne 0$), also unabhängig
\text{dim } \mathbb{R}^2 = 2 || zwei unabhängige Vektoren im zweidimensionalen Raum bilden nach Satz 4.73 eine Basis
:::

:::alt Als Schubladen
Hast du $n$ Schubladen (Dimension) und genau $n$ Dinge, die sich nicht gegenseitig ersetzen, belegen sie alle Schubladen. Du musst nicht noch zusätzlich prüfen, ob alles abgedeckt ist.
:::
""")

k.mc("Sei $\\dim V = 4$ und $M = \\{v_1, v_2, v_3, v_4\\} \\subseteq V$ linear unabhängig. Was folgt?",
     ["$M$ ist eine Basis von $V$", "$M$ ist nur dann eine Basis, wenn zusätzlich $\\langle M \\rangle = V$ gezeigt wird", "$M$ ist linear abhängig, weil $|M| = \\dim V$", "$\\langle M \\rangle$ hat Dimension $3$"],
     "Satz 4.73: Bei $|M| = \\dim V$ genügt eine der beiden Eigenschaften. Aus linearer Unabhängigkeit folgt $\\dim \\langle M \\rangle = 4$, also $\\langle M \\rangle = V$ nach Satz 4.74.",
     tipps=["Satz 4.73.", "$\\dim \\langle M \\rangle = |M|$ bei unabhängigem $M$."],
     fehler={"$M$ ist nur dann eine Basis, wenn zusätzlich $\\langle M \\rangle = V$ gezeigt wird": "Bei genau $\\dim V$ Elementen folgt die Erzeugung automatisch (Satz 4.73), sie muss nicht gesondert gezeigt werden.",
             "$M$ ist linear abhängig, weil $|M| = \\dim V$": "Abhängigkeit droht erst bei mehr als $\\dim V$ Vektoren.",
             "$\\langle M \\rangle$ hat Dimension $3$": "$M$ ist unabhängig, also ist $M$ eine Basis von $\\langle M \\rangle$: Dimension $4$."})

# ── Seite 9: Dimensionsformel ────────────────────────────────────────────
k.erklaerung("Dimensionsformel für Untervektorräume", r"""
## Satz 4.75 und Beispiel 4.76

Für Untervektorräume $U, W$ von $V$ (endlichdimensional) ist die **Summe** $U + W := \{u + w \mid u \in U, w \in W\}$ ein Untervektorraum, und

$$\dim(U + W) = \dim U + \dim W - \dim(U \cap W).$$

*Beweis:* $U + W = \langle U \cup W \rangle$. Wähle eine Basis $B$ von $U \cap W$ und ergänze sie zu Basen $B_U$ von $U$ und $B_W$ von $W$ (Kor. 4.66). Dann erzeugt $B_U \cup B_W$ die Summe. Ist eine Kombination der Vektoren gleich $0$, so liegt der Teil aus $B_W \setminus B$ in $U \cap W$, hat also zwei Darstellungen in $B_W$, die nach Satz 4.55 beide aus Nullen bestehen. Damit ist $B_U \cup B_W$ unabhängig, und mit $B = B_U \cap B_W$ folgt $|B_U \cup B_W| = |B_U| + |B_W| - |B|$ (Satz 2.27). $\square$

:::rechnung Beispiel 4.76: $E_1 = \{x_1 + x_2 = 0\}$, $E_2 = \{x_2 + x_3 = 0\}$ in $\mathbb{R}^3$
2 + 2 - 1 = 3 || $\dim E_1 = \dim E_2 = 2$, $E_1 \cap E_2 = \langle (1, -1, 1)^\top \rangle$ hat Dimension $1$
\text{dim } \mathbb{R}^3 = 3 || nach Satz 4.74 folgt $E_1 + E_2 = \mathbb{R}^3$
:::

Ist $U \cap W = \{0\}$, addieren sich die Dimensionen.

:::alt Als Inklusion-Exklusion
Zähle die Richtungen von $U$ und von $W$ zusammen. Was in beiden steckt (der Schnitt), hast du doppelt gezählt, also einmal abziehen. Genau wie bei $|A \cup B| = |A| + |B| - |A \cap B|$ (Satz 2.27).
:::
""")

k.luecke("Dimensionsformel (Beispiel 4.76): Zwei Ebenen $E_1, E_2$ im $\\mathbb{R}^3$ schneiden sich in einer Geraden. Fülle die Lücken.",
         "\\dim(E_1 + E_2) = \\luecke + \\luecke - \\luecke = \\luecke",
         [[2], [2], [1], [3]],
         "$\\dim E_1 = \\dim E_2 = 2$ und $\\dim(E_1 \\cap E_2) = 1$ (Gerade): $2 + 2 - 1 = 3$, also $E_1 + E_2 = \\mathbb{R}^3$.",
         tipps=["Eine Ebene hat Dimension $2$, eine Gerade Dimension $1$.", "Der Schnitt wird abgezogen.", "$2, 2, 1, 3$."],
         rechenweg=rechnung([("2 + 2 - 1 = 3", "Dimensionsformel")]),
         typische_fehler=[([2, 2, 1, 5], "Du hast $\\dim(E_1 \\cap E_2)$ addiert statt abgezogen: $2 + 2 + 1$. Die Richtung im Schnitt ist doppelt gezählt.")])


# ══ Praxis ═══════════════════════════════════════════════════════════════
def _rv(rng, lo=-3, hi=3, n=3):
    return [rng.randint(lo, hi) for _ in range(n)]


def _satz(vs, namen="abc"):
    return ", ".join(f"\\mathbf{{{namen[i]}}} = {vt(vs[i])}" for i in range(len(vs)))


def basis_oder_nicht(rng):
    """Satz 4.73: n Vektoren im R^n sind genau dann eine Basis, wenn sie linear unabhängig sind."""
    n = rng.choice([2, 3])
    ja = rng.random() < 0.5
    while True:
        vs = [_rv(rng, -3, 3, n) for _ in range(n)]
        if not ja:
            a, b = rng.randint(-2, 2), rng.randint(-2, 2)
            if n == 2:
                vs[1] = [a * c for c in vs[0]] if a != 0 else vs[1]
                if a == 0:
                    continue
            else:
                vs[2] = [int(x) for x in lin([a, b], vs[:2])]
                if a == 0 and b == 0:
                    continue
        if unabhaengig(vs) == ja and all(any(c != 0 for c in v) for v in vs):
            break
    if n == 2:
        d = vs[0][0] * vs[1][1] - vs[0][1] * vs[1][0]
        zeilen = [(f"{tx(vs[0][0])} \\cdot {tx(vs[1][1])} - {tx(vs[0][1])} \\cdot {tx(vs[1][0])} = {tx(d)}",
                   "$u_1 v_2 - u_2 v_1$: genau dann $\\ne 0$, wenn die Vektoren nicht parallel sind")]
        grund = (f"Die Größe $u_1v_2 - u_2v_1 = {d}$ ist {'ungleich' if ja else 'gleich'} $0$: die Vektoren sind {'nicht ' if ja else ''}parallel.")
    elif ja:
        zeilen = [("\\text{Gauß: Rang 3}", "Die Zeilenumformungen liefern drei Pivots, also nur die triviale Kombination")]
        grund = "Das Gauß-Verfahren liefert Rang $3$: Nur die triviale Linearkombination ergibt $\\mathbf{0}$."
    else:
        a_, b_ = next((x, y) for x in range(-2, 3) for y in range(-2, 3) if lin([x, y], vs[:2]) == [F(c) for c in vs[2]])
        zeilen = [(f"{tx(a_)} \\cdot {tx(vs[0][i])} + {tx(b_)} \\cdot {tx(vs[1][i])} = {tx(vs[2][i])}", f"Komponente {i + 1}: $\\mathbf{{c}} = {tx(a_)}\\mathbf{{a}} + {tx(b_)}\\mathbf{{b}}$") for i in range(3)]
        grund = f"$\\mathbf{{c}} = {tx(a_)}\\mathbf{{a}} + {tx(b_)}\\mathbf{{b}}$: Ein Vektor ist überflüssig, die Menge ist linear abhängig."
    opt = [f"Ja, eine Basis des $\\mathbb{{R}}^{n}$", f"Nein, keine Basis des $\\mathbb{{R}}^{n}$ (linear abhängig)"]
    optionen = opt if ja else opt[::-1]
    namen = "uv" if n == 2 else "abc"
    kopf = ", ".join(f"\\mathbf{{{namen[i]}}} = {vt(vs[i])}" for i in range(n))
    return {"typ": "mc",
            "frage": f"Bilden ${kopf}$ eine Basis des $\\mathbb{{R}}^{n}$?",
            "optionen": optionen, "fehler": {optionen[1]: "Das stimmt nicht. " + grund},
            "tipps": [f"Nach Satz 4.73 genügt bei $n = {n}$ Vektoren im $\\mathbb{{R}}^{n}$ die lineare Unabhängigkeit.",
                      "Ist ein Vektor ein Vielfaches oder eine Kombination der anderen?", "Suche eine nichttriviale Kombination, die $\\mathbf{0}$ ergibt."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Bei genau $\\dim V$ Vektoren ist „Basis“ dasselbe wie „linear unabhängig“ (Satz 4.73)."}


def abhaengigkeit_koeffizienten(rng):
    """Def. 4.47: nichttriviale Linearkombination, die 0 ergibt."""
    while True:
        u, v = _rv(rng, -3, 3, 3), _rv(rng, -3, 3, 3)
        a, b = rng.choice([-3, -2, -1, 1, 2, 3]), rng.choice([-3, -2, -1, 1, 2, 3])
        if unabhaengig([u, v]):
            break
    w = [int(x) for x in lin([a, b], [u, v])]
    loes = [a, b, -1]
    fehler = [([a, b, 1], "Das dritte Vorzeichen: $a\\mathbf{u} + b\\mathbf{v} + 1\\mathbf{w}$ ergibt nicht $\\mathbf{0}$. Es muss $-1$ sein, weil $\\mathbf{w}$ auf die andere Seite wandert."),
              ([b, a, -1], "Koeffizienten vertauscht: $\\lambda_1$ gehört zu $\\mathbf{u}$."),
              ([-a, -b, -1], "Alle Vorzeichen stimmen nicht: Aus $\\mathbf{w} = a\\mathbf{u} + b\\mathbf{v}$ folgt $a\\mathbf{u} + b\\mathbf{v} - \\mathbf{w} = \\mathbf{0}$.")]
    zeilen = [(f"{tx(a)} \\cdot {tx(u[i])} + {tx(b)} \\cdot {tx(v[i])} + (-1) \\cdot {tx(w[i])} = 0", f"Komponente {i + 1}") for i in range(3)]
    return {"typ": "vektor", "vielfaches": True,
            "frage": f"Die Vektoren $\\mathbf{{u}} = {vt(u)}$, $\\mathbf{{v}} = {vt(v)}$, $\\mathbf{{w}} = {vt(w)}$ sind linear abhängig. Gib eine nichttriviale Linearkombination $\\lambda_1\\mathbf{{u}} + \\lambda_2\\mathbf{{v}} + \\lambda_3\\mathbf{{w}} = \\mathbf{{0}}$ an, als Vektor $(\\lambda_1, \\lambda_2, \\lambda_3)^\\top$.",
            "loesung": loes,
            "tipps": ["Suche $\\mathbf{w}$ als Kombination von $\\mathbf{u}$ und $\\mathbf{v}$: $\\mathbf{w} = a\\mathbf{u} + b\\mathbf{v}$.", "Löse die ersten beiden Komponenten nach $a, b$ auf.", f"$\\mathbf{{w}} = {a}\\mathbf{{u}} + ({b})\\mathbf{{v}}$, also $\\lambda_3 = -1$."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Aus $\\mathbf{w} = a\\mathbf{u} + b\\mathbf{v}$ folgt $a\\mathbf{u} + b\\mathbf{v} - \\mathbf{w} = \\mathbf{0}$ (Satz 4.52).",
            "typische_fehler": ohne_gleiche(loes, fehler)}


def koordinaten_bestimmen(rng):
    """Def. 4.61: Koordinatenvektor bezüglich einer geordneten Basis."""
    n = rng.choice([2, 3])
    while True:
        B = [_rv(rng, -2, 3, n) for _ in range(n)]
        if unabhaengig(B):
            break
    x_koord = [rng.randint(-3, 3) for _ in range(n)]
    if all(c == 0 for c in x_koord):
        x_koord[0] = 1
    x = [int(c) for c in lin(x_koord, B)]
    erg = koordinaten(B, x)
    assert erg == [F(c) for c in x_koord]
    zeilen = [(" + ".join(f"{tx(x_koord[j])} \\cdot {tx(B[j][i])}" for j in range(n)) + f" = {tx(x[i])}", f"Probe, Komponente {i + 1}") for i in range(n)]
    fehler = [(x, "Das ist $\\mathbf{x}$ selbst, also $[\\mathbf{x}]_{\\mathfrak{E}}$ bezüglich der Standardbasis."),
              (x_koord[::-1], "Die Koordinaten stehen in der Reihenfolge der Basis: $x_j$ gehört zu $b^{(j)}$.")]
    kopf = ", ".join(vt(b) for b in B)
    return {"typ": "vektor",
            "frage": f"Bestimme $[\\mathbf{{x}}]_{{\\mathfrak{{B}}}}$ für $\\mathbf{{x}} = {vt(x)}$ und die geordnete Basis $\\mathfrak{{B}} = \\left({kopf}\\right)$.",
            "loesung": x_koord,
            "tipps": ["Gesucht sind $x_1, \\ldots, x_n$ mit $x_1 b^{(1)} + \\cdots + x_n b^{(n)} = \\mathbf{x}$.", "Schreibe das komponentenweise als Gleichungssystem und löse es.", f"Die Probe ergibt $\\mathbf{{x}} = {vt(x)}$."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Nach Satz 4.55 gibt es genau ein Koordinatentupel; man findet es durch Lösen des Gleichungssystems $\\sum x_j b^{(j)} = \\mathbf{x}$.",
            "typische_fehler": ohne_gleiche(x_koord, fehler)}


def dimension_huelle(rng):
    """Dimension einer linearen Hülle: unabhängige Vektoren zählen (Def. 4.67, Kor. 4.66)."""
    while True:
        r = rng.choice([1, 2, 2, 3])
        basis = [_rv(rng, -2, 2, 4) for _ in range(r)]
        if unabhaengig(basis):
            break
    vs = [list(b) for b in basis]
    rel = []
    for _ in range(rng.choice([1, 2])):
        c = [rng.randint(-2, 2) for _ in range(r)]
        if all(x == 0 for x in c):
            c[0] = 1
        vs.append([int(x) for x in lin(c, basis)])
        rel.append((c, len(vs) - 1))
    perm = list(range(len(vs)))
    rng.shuffle(perm)
    vs2 = [vs[p] for p in perm]
    d = rang(vs2)
    assert d == r
    namen = "abcdef"
    zeilen = [(f"\\text{{Anzahl unabhängiger Vektoren: }} {r}", "unabhängige Vektoren zählen")]
    for c, idx in rel:
        i = perm.index(idx)
        zeilen.append((f"\\text{{Vektor {namen[i]} ist Kombination der übrigen}}", "überflüssig, wird nicht gezählt"))
    fehler = [(len(vs2), "Du hast alle Vektoren gezählt. Die Dimension zählt nur die unabhängigen, überflüssige Vektoren (Kombinationen der anderen) fallen weg."),
              (min(len(vs2), 4), "Die Dimension ist nicht die Dimension des umgebenden Raums $\\mathbb{R}^4$, sondern die der Hülle."),
              (max(1, d - 1), "Zu klein: Prüfe, welche Vektoren wirklich überflüssig sind."), (d + 1, "Zu groß: Ein weiterer Vektor ist eine Kombination der übrigen.")]
    return {"frage": "Bestimme $\\dim \\langle " + ", ".join(f"\\mathbf{{{namen[i]}}}" for i in range(len(vs2))) + " \\rangle$ im $\\mathbb{R}^4$ mit " +
            "$" + ", ".join(f"\\mathbf{{{namen[i]}}} = {vt(vs2[i])}" for i in range(len(vs2))) + "$.",
            "loesung": d,
            "tipps": ["Die Dimension ist die Anzahl der Vektoren einer Basis der Hülle.", "Streiche Vektoren, die sich aus den anderen kombinieren lassen.", "Prüfe, ob einer ein Vielfaches oder eine Summe von Vielfachen der anderen ist."],
            "rechenweg": rechnung(zeilen[:1] + zeilen[1:]),
            "erklaerung": "Eine Basis der Hülle entsteht, indem man überflüssige Vektoren streicht (Kor. 4.66). Die Dimension ist deren Anzahl.",
            "typische_fehler": ohne_gleiche(d, fehler)}


def dimensionsformel_rechnen(rng):
    """Satz 4.75."""
    n = rng.choice([4, 5, 6])
    while True:
        a, b = rng.randint(2, n - 1), rng.randint(2, n - 1)
        s = rng.randint(max(a, b), min(n, a + b))
        e = a + b - s
        if e >= 0 and e <= min(a, b):
            break
    gesucht = rng.choice(["summe", "schnitt"])
    if gesucht == "summe":
        frage = f"Seien $U, W$ Untervektorräume des $\\mathbb{{R}}^{{{n}}}$ mit $\\dim U = {a}$, $\\dim W = {b}$ und $\\dim(U \\cap W) = {e}$. Bestimme $\\dim(U + W)$."
        loes, rw = s, [(f"{a} + {b} - {e} = {s}", "Dimensionsformel (Satz 4.75)")]
        fehler = [(a + b, "Du hast den Schnitt nicht abgezogen: Seine Richtungen sind doppelt gezählt."), (a + b + e, "Der Schnitt wird abgezogen, nicht addiert."),
                  (max(a, b), "Das ist nur die größere der beiden Dimensionen. Die Summe enthält beide Räume und ist mindestens so groß."), (n, "Die Summe ist nicht automatisch der ganze Raum, rechne mit der Formel.")]
    else:
        frage = f"Seien $U, W$ Untervektorräume des $\\mathbb{{R}}^{{{n}}}$ mit $\\dim U = {a}$, $\\dim W = {b}$ und $\\dim(U + W) = {s}$. Bestimme $\\dim(U \\cap W)$."
        loes, rw = e, [(f"{a} + {b} - {s} = {e}", "Dimensionsformel nach $\\dim(U \\cap W)$ umgestellt")]
        fehler = [(s - a - b if s - a - b != e else e + 1, "Vorzeichen: $\\dim(U \\cap W) = \\dim U + \\dim W - \\dim(U + W)$."), (a + b + s, "Die Formel wurde falsch umgestellt."),
                  (s - max(a, b), "Das ist nicht $\\dim U + \\dim W - \\dim(U + W)$."), (abs(a - b), "Nur die Differenz der Dimensionen ist nicht der Schnitt: Benutze Satz 4.75.")]
    return {"frage": frage, "loesung": loes,
            "tipps": ["$\\dim(U + W) = \\dim U + \\dim W - \\dim(U \\cap W)$.", "Setze die bekannten Zahlen ein.", "Stelle bei Bedarf die Gleichung um."],
            "rechenweg": rechnung(rw),
            "erklaerung": "Der Schnitt zählt in $\\dim U + \\dim W$ doppelt, die Formel zieht ihn einmal ab (Satz 4.75).",
            "typische_fehler": ohne_gleiche(loes, [f_ for f_ in fehler if f_[0] >= 0])}


k.praxis()

k.generator(basis_oder_nicht, typ="mc", titel="Basis des ℝⁿ oder nicht?")
k.generator(abhaengigkeit_koeffizienten, typ="vektor", titel="Abhängigkeit: Koeffizienten bestimmen")
k.generator(koordinaten_bestimmen, typ="vektor", titel="Koordinatenvektor bestimmen")
k.generator(dimension_huelle, typ="zahl", titel="Dimension einer linearen Hülle")
k.generator(dimensionsformel_rechnen, typ="zahl", titel="Dimensionsformel (Satz 4.75)")

k.zahl("Ein Graustufenbild mit $16 \\times 16$ Pixeln wird als Vektor im $\\mathbb{R}^N$ gespeichert (ein Eintrag je Pixel). Welche Dimension hat $\\mathbb{R}^N$, und wie viele Elemente hat jede Basis?", 256,
       "Jedes Pixel ist eine Koordinate: $N = 16 \\cdot 16 = 256$. Nach Korollar 4.65 hat jede Basis genau $256$ Elemente, etwa die Standardbasis (ein Pixel hell, alle anderen schwarz).",
       tipps=["Zähle die Pixel.", "Alle Basen haben gleich viele Elemente (Kor. 4.65).", "$16 \\cdot 16$."],
       rechenweg=rechnung([("16 \\cdot 16 = 256", "Anzahl der Pixel = Dimension")]),
       typische_fehler=[(32, "Das ist $16 + 16$. Das Bild hat $16$ Zeilen mit je $16$ Pixeln, also $16 \\cdot 16$ Einträge.")])

_PU1, _PU2, _PW1, _PW2 = [1, 0, 1], [0, 1, 1], [1, 1, 0], [0, 0, 1]
assert unabhaengig([_PU1, _PU2]) and unabhaengig([_PW1, _PW2]) and rang([_PU1, _PU2, _PW1, _PW2]) == 3
assert lin([1, 1], [_PU1, _PU2]) == lin([1, 2], [_PW1, _PW2]) == [1, 1, 2]

k.rechenweg_aufgabe(r"""
## Übungsblatt-Stil: Dimension von Summe und Schnitt

Seien $U = \langle (1, 0, 1)^\top, (0, 1, 1)^\top \rangle$ und $W = \langle (1, 1, 0)^\top, (0, 0, 1)^\top \rangle$ Untervektorräume des $\mathbb{R}^3$.
Bestimmen Sie $\dim U$, $\dim(U + W)$ und mit der Dimensionsformel $\dim(U \cap W)$. Geben Sie einen Erzeuger des Schnitts an.
""",
    [{"typ": "wf", "frage": "Die beiden Erzeuger von $U$ sind linear unabhängig, also gilt $\\dim U = 2$.", "wahr": True,
      "tipps": ["Sind $(1, 0, 1)^\\top$ und $(0, 1, 1)^\\top$ parallel?"],
      "erklaerung": "Kein Vektor ist Vielfaches des anderen (verschiedene Nullstellen), also unabhängig und eine Basis von $U$."},
     {"typ": "zahl", "frage": "Bestimme $\\dim(U + W)$.", "loesung": 3,
      "tipps": ["$U + W$ wird von allen vier Vektoren erzeugt.", "Enthält $\\{(1, 0, 1)^\\top, (0, 1, 1)^\\top, (1, 1, 0)^\\top, (0, 0, 1)^\\top\\}$ drei unabhängige Vektoren?"],
      "rechenweg": rechnung([("1 \\cdot 0 + 0 \\cdot 0 + 1 \\cdot 1 = 1", "z. B. liefert $(0, 0, 1)^\\top$ den dritten Einheitsvektor; mit $(1, 0, 1)^\\top$ und $(0, 1, 1)^\\top$ erhält man alle drei: $U + W = \\mathbb{R}^3$")]),
      "typische_fehler": [(4, "Vier Vektoren im $\\mathbb{R}^3$ können nicht unabhängig sein (Austauschsatz).")]},
     {"typ": "zahl", "frage": "Bestimme $\\dim(U \\cap W)$ mit der Dimensionsformel.", "loesung": 1,
      "tipps": ["$\\dim(U + W) = \\dim U + \\dim W - \\dim(U \\cap W)$.", "$\\dim W = 2$."],
      "rechenweg": rechnung([("2 + 2 - 3 = 1", "Satz 4.75 nach $\\dim(U \\cap W)$ umgestellt")]),
      "typische_fehler": [(0, "$2 + 2 - 3 = 1$, nicht $0$: Zwei Ebenen im $\\mathbb{R}^3$ schneiden sich in mindestens einer Geraden.")]},
     {"typ": "vektor", "frage": "Gib einen Erzeuger des Schnitts $U \\cap W$ an (Vielfache zählen).", "loesung": [1, 1, 2], "vielfaches": True,
      "tipps": ["Ein Vektor $a(1, 0, 1)^\\top + b(0, 1, 1)^\\top = (a, b, a + b)^\\top$ liegt in $U$.", "In $W$ liegen die Vektoren $(c, c, d)^\\top$.", "Setze gleich: $a = b = c$ und $d = a + b$."],
      "rechenweg": rechnung([("1 \\cdot 1 + 1 \\cdot 1 = 2", "dritte Komponente $a + b = d$ für $a = b = 1$, also $(1, 1, 2)^\\top$")]),
      "typische_fehler": [([1, 1, 1], "Dritte Komponente: $a + b = 2$, nicht $1$.")]}],
    "Die Dimensionsformel zählt den Schnitt einmal ab. Zwei verschiedene Ebenen des $\\mathbb{R}^3$ durch $\\mathbf{0}$ schneiden sich immer in einer Geraden.",
    uebungsblatt=True,
    tipps=["Vier Vektoren im $\\mathbb{R}^3$: höchstens drei sind unabhängig.", "Dimensionsformel nach dem Schnitt umstellen."],
    rechenweg=r"""
:::rechnung
2 + 2 - 3 = 1 || $\dim(U \cap W)$ nach Satz 4.75
1 + 1 = 2 || dritte Komponente von $(1, 1, 2)^\top$ in $U$
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Satz 4.73 und Beobachtung 4.48 (im Skript „Übung“ bzw. unbewiesen)

Sei $V$ ein Vektorraum mit $\dim V = n$.

1. Zeigen Sie: Ist $A \subseteq B \subseteq V$ und $B$ linear unabhängig, so ist $A$ linear unabhängig.
2. Zeigen Sie Satz 4.73: Ist $M \subseteq V$ mit $|M| = n$ linear unabhängig, so ist $M$ eine Basis.
3. Zeigen Sie: Ist $\langle M \rangle = V$ und $|M| = n$, so ist $M$ linear unabhängig.
""",
    r"""
**1.** Seien $v^{(1)}, \ldots, v^{(m)} \in A$ paarweise verschieden und $\sum \lambda_j v^{(j)} = 0$. Die Vektoren liegen auch in $B$, also folgt $\lambda = 0$ aus der Unabhängigkeit von $B$.

**2.** $M$ ist unabhängig. Wäre $\langle M \rangle \neq V$, gäbe es $w \in V \setminus \langle M \rangle$, und $M \cup \{w\}$ wäre nach Korollar 4.53 unabhängig mit $n + 1$ Elementen. Nach dem Austauschsatz hat aber jede unabhängige Menge höchstens $n$ Elemente. Widerspruch. Also $\langle M \rangle = V$.

**3.** Wäre $M$ abhängig, gäbe es nach Satz 4.52 ein $v \in M$ mit $v \in \langle M \setminus \{v\} \rangle$. Dann erzeugt $M \setminus \{v\}$ mit $n - 1$ Elementen schon $V$. Nach Korollar 4.66 (Basisauswahl) gibt es eine Basis aus höchstens $n - 1$ Elementen, im Widerspruch zu $\dim V = n$ (Korollar 4.65). $\square$
""",
    ["In 1: Teilmenge $\\Rightarrow$ dieselbe nichttriviale Kombination wäre in $B$ möglich",
     "In 2: Ergänzungskriterium (Kor. 4.53) mit dem Austauschsatz kombiniert",
     "In 3: Satz 4.52 (ein überflüssiger Vektor) und Eindeutigkeit der Basislänge (Kor. 4.65) benutzt"],
    "Bei genau $n$ Vektoren gilt: unabhängig $\\Leftrightarrow$ erzeugend $\\Leftrightarrow$ Basis. Beide Beweise sind Widerspruchsbeweise mit dem Austauschsatz.",
    uebungsblatt=True,
    tipps=["Für 2: Angenommen $\\langle M \\rangle \\neq V$. Welcher Vektor fehlt?", "Für 3: Aus einem abhängigen Erzeugendensystem lässt sich ein Vektor streichen."])

k.papier(r"""
## Beweisaufgabe: Dimensionsformel (Satz 4.75)

Seien $U, W$ Untervektorräume eines endlichdimensionalen Vektorraums $V$. Sei $B$ eine Basis von $U \cap W$, ergänzt zu Basen $B_U$ von $U$ und $B_W$ von $W$.
Zeigen Sie, dass $B_U \cup B_W$ eine Basis von $U + W$ ist, und folgern Sie $\dim(U + W) = \dim U + \dim W - \dim(U \cap W)$.
""",
    r"""
**Erzeugung:** Jedes $u + w$ mit $u \in U$, $w \in W$ ist eine Linearkombination aus $B_U \cup B_W$. Also $\langle B_U \cup B_W \rangle = U + W$.

**Unabhängigkeit:** Sei eine Linearkombination der Vektoren aus $B_U \cup B_W$ gleich $0$. Fasse die Beiträge aus $B_U$ zu $u \in U$ und die aus $B_W \setminus B_U$ zu $w \in W$ zusammen: $u + w = 0$. Dann ist $w = -u \in U \cap W$, hat also eine Darstellung durch $B \subseteq B_W$. In der Basis $B_W$ hat $w$ so zwei Darstellungen (eine mit $B$, eine mit $B_W \setminus B$), nach Satz 4.55 sind alle Koeffizienten $0$. Es folgt $w = 0$, $u = 0$, und die Unabhängigkeit von $B_U$ liefert auch die übrigen Koeffizienten $0$.

**Zählen:** $B_U \cap B_W = B$, also $\dim(U + W) = |B_U \cup B_W| = |B_U| + |B_W| - |B| = \dim U + \dim W - \dim(U \cap W)$ (Satz 2.27). $\square$
""",
    ["Erzeugung von $U + W$ durch $B_U \\cup B_W$ begründet",
     "Die Kombination in einen Teil aus $U$ und einen aus $W$ zerlegt und $w \\in U \\cap W$ erkannt",
     "Eindeutigkeit der Darstellung (Satz 4.55) in $B_W$ benutzt",
     "$B_U \\cap B_W = B$ gezeigt und das Zählargument (Satz 2.27) angewendet"],
    "Der Schnitt liefert gemeinsame Basisvektoren. Alles, was nur in einer Seite liegt, kommt zusätzlich dazu, und die gemeinsamen Vektoren zählen einmal.",
    tipps=["Starte mit einer Linearkombination, die $0$ ergibt, und teile sie auf.", "Der Teil $w$ liegt in $W$ und in $U$."])

k.zusammenfassung(r"""
## Basen und Dimension (Skript Abschn. 4.4 und 4.5, Def. 4.47 bis Bsp. 4.76)

- **Linear unabhängig** (Def. 4.47): nur die triviale Kombination ergibt $0$. $\emptyset$ ist unabhängig; Mengen mit $\mathbf{0}$ sind abhängig (Bsp. 4.49). Teilmengen unabhängiger Mengen sind unabhängig (Beob. 4.48).
- **Satz 4.52:** $M$ abhängig $\iff$ ein $v \in M$ liegt in $\langle M \setminus \{v\} \rangle$. **Kor. 4.53:** $L \cup \{w\}$ unabhängig $\iff$ $w \notin \langle L \rangle$.
- **Basis** (Def. 4.54): unabhängig und erzeugend; minimal erzeugend, maximal unabhängig (Beob. 4.56, 4.57). Standardbasis von $K^n$, Monome von $K[X]$ (Bsp. 4.58, 4.60).
- **Satz 4.55:** $\mathfrak{B}$ geordnete Basis $\iff$ jeder Vektor hat genau eine Darstellung. **Koordinatenvektor** $[v]_{\mathfrak{B}}$ (Def. 4.61), Bsp. 4.62, 4.63 ($\mathbb{C}$ über $\mathbb{R}$ und $\mathbb{C}$).
- **Austauschsatz** (Satz 4.64): $|L| \le |E|$. **Kor. 4.65:** alle Basen gleich groß. **Kor. 4.66:** Basisauswahl und Basisergänzung, $L \subseteq B \subseteq L \cup E$.
- **Dimension** $\dim_K V := |B|$ (Def. 4.67): $\dim K^n = n$, Gerade $1$, Ebene $2$, $\dim F = 2$, $\dim_{\mathbb{R}} \mathbb{C} = 2$, $\dim_{\mathbb{C}} \mathbb{C} = 1$, $K[X]$ unendlichdimensional.
- **Satz 4.73:** Bei $|M| = \dim V$ ist unabhängig $\iff$ erzeugend $\iff$ Basis. **Satz 4.74:** $\dim U \le \dim V$, Gleichheit genau bei $U = V$.
- **Dimensionsformel** (Satz 4.75): $\dim(U + W) = \dim U + \dim W - \dim(U \cap W)$.

!! Die Dimension zählt unabhängige Vektoren, nicht alle. Koordinaten hängen von der Basis und ihrer Reihenfolge ab.
""")
