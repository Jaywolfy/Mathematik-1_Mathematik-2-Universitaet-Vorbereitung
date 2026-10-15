# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 20: Geometrie des ℝⁿ (Skript Disser WS 26/27, Abschn. 4.1, Def. 4.1 bis Beispiel 4.22)."""
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(
    slug="geometrie_rn",
    titel="Geometrie des ℝⁿ",
    beschreibung="Vektoren, Geraden und Ebenen, Schnittpunkte, Skalarprodukt, Länge, Orthogonalität, Hyperebene, Abstand (Satz 4.15), Kreuzprodukt, Fläche und Spatvolumen",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 4.1",
    icon="📐")

sp, kp, det = mathlib.skalarprodukt, mathlib.kreuzprodukt, mathlib.det
vt, tx = mathlib.tex_vektor, mathlib.tex


def rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def norm_quadrat(v):
    return sp(v, v)


# ── Beispiele des Skripts nachrechnen ────────────────────────────────────
# Beispiel 4.7: Gerade und Ebene schneiden sich in (2, 3, 3)
_P0, _W = [0, 1, 1], [1, 1, 1]
_PE, _U, _V = [0, 0, 1], [1, 1, 0], [1, 2, 2]
_loes = mathlib.lgs_loesen([[_U[i], _V[i], -_W[i]] for i in range(3)], [_P0[i] - _PE[i] for i in range(3)])
assert _loes["art"] == "eindeutig" and _loes["x"] == [1, 1, 2]          # s = 1, t = 1, r = 2
assert [_P0[i] + 2 * _W[i] for i in range(3)] == [2, 3, 3] == [_PE[i] + _U[i] + _V[i] for i in range(3)]
# Beispiel 4.13 und 4.22
_N = [2, -2, 1]
assert sp(_U, _N) == 0 and sp(_V, _N) == 0 and sp(_PE, _N) == 1
assert kp(_U, _V) == _N and norm_quadrat(_N) == 9
# Beispiel 4.16: Abstand vom Ursprung 1/3, nächster Punkt (2, -2, 1)/9
assert F(abs(0 - 1), 3) == F(1, 3)
assert [F(0) - F(0 - 1, 9) * c for c in _N] == [F(2, 9), F(-2, 9), F(1, 9)]
assert sp([F(2, 9), F(-2, 9), F(1, 9)], _N) == 1
# Beispiel 4.22: Spat mit w = (2, 0, 1): Volumen 5, Höhe 5/3
assert abs(sp(kp(_U, _V), [2, 0, 1])) == 5 and F(5, 3) * 3 == 5
# Beobachtung 4.10: dritte binomische Formel für Vektoren
_X, _Y = [1, 2, 3], [4, -1, 2]
assert norm_quadrat([a - b for a, b in zip(_X, _Y)]) == norm_quadrat(_X) - 2 * sp(_X, _Y) + norm_quadrat(_Y)
# Beobachtung 4.20 (Lagrange-Identität, im Beweis benutzt)
assert norm_quadrat(kp(_X, _Y)) == norm_quadrat(_X) * norm_quadrat(_Y) - sp(_X, _Y) ** 2

k.lernziele([
    "Ich kann Vektoren im $\\mathbb{R}^n$ addieren und mit Skalaren multiplizieren und jeden Vektor aus Einheitsvektoren aufbauen (Def. 4.1 bis 4.4, Beob. 4.3)",
    "Ich kann Geraden und Ebenen in Parameterform angeben, auch durch Punkte, und den Schnittpunkt einer Geraden mit einer Ebene berechnen (Def. 4.5, Satz 4.6, Bsp. 4.7)",
    "Ich kann Skalarprodukt, Länge, Abstand und Orthogonalität berechnen, Normalenvektor und Hyperebene bestimmen (Def. 4.9 bis 4.14)",
    "Ich kann den Abstand eines Punktes von einer Hyperebene berechnen und beweisen (Satz 4.15)",
    "Ich kann das Kreuzprodukt im $\\mathbb{R}^3$ berechnen und für Normalenvektor, Flächeninhalt und Spatvolumen nutzen (Def. 4.18, Satz 4.19, Beob. 4.20, 4.21)",
])

k.warum(r"""
Jedes 3D-Spiel und jeder Raytracer rechnet mit diesem Kapitel: Ein Sehstrahl ist eine Gerade, eine Wand eine Ebene,
und der Schnittpunkt entscheidet über die Farbe des Pixels (Bem. 4.8). Normalenvektoren steuern die Beleuchtung.
Eine Hyperebene trennt in einem Merkmalsraum „Klasse A“ von „Klasse B“: so arbeiten lineare Klassifikatoren und
die letzte Schicht vieler neuronaler Netze (Bem. 4.17). Abstand, Länge und Orthogonalität brauchst du später bei
Projektionen, Ausgleichsrechnung und Kompression.
""")

# ── Seite 1: Vektoren ────────────────────────────────────────────────────
k.erklaerung("Vektoren im ℝⁿ", r"""
## Definition 4.1 bis 4.4

:::analogie 🧭 Wegbeschreibung
„Geh 3 Schritte nach rechts und 2 nach oben“ ist ein Vektor mit zwei Einträgen. Zwei Anweisungen
nacheinander ausführen heißt addieren. Doppelt so weit gehen heißt mit $2$ multiplizieren.
:::

Ein [[Vektor]] im $\mathbb{R}^n$ ist eine Spalte $\mathbf{x} = (x_1, \ldots, x_n)^\top$ mit $n$ Einträgen,
den **Komponenten** (Def. 4.1). Addition und Multiplikation mit einem [[Skalar]] $\lambda \in \mathbb{R}$ laufen
**komponentenweise** (Def. 4.2). Der $j$-te [[Einheitsvektor]] $\mathbf{e}^{(j)}$ hat eine $1$ an Stelle $j$, sonst $0$ (Def. 4.4).
Damit ist $\mathbf{x} = x_1 \mathbf{e}^{(1)} + \cdots + x_n \mathbf{e}^{(n)}$ (Beob. 4.3: $\mathbb{R}^n$ ist mit $+$ eine [[abelsche|abelsch]] Gruppe).

:::visual vektoren2d
{"vektoren": [{"x": 3, "y": 1}, {"x": 1, "y": 2}], "zeige": ["summe", "vielfaches"], "faktor": 2,
 "unterschrift": "$\\mathbf{a} + \\mathbf{b}$ als Parallelogramm und $2\\mathbf{a}$ als doppelt so langer Pfeil."}
:::

:::rechnung Komponentenweise rechnen mit $\mathbf{x} = (1, 2, 3)^\top$, $\mathbf{y} = (0, 1, -1)^\top$
1 + 0 = 1 || erste Komponente von $\mathbf{x} + \mathbf{y}$
2 + 1 = 3 || zweite Komponente
3 + (-1) = 2 || dritte Komponente: $\mathbf{x} + \mathbf{y} = (1, 3, 2)^\top$
2 \cdot 3 = 6 || dritte Komponente von $2\mathbf{x}$: $2\mathbf{x} = (2, 4, 6)^\top$
:::

:::alt Als Tabellenzeile
Ein Vektor im $\mathbb{R}^3$ ist eine Zeile mit drei Zahlen, wie ein Datensatz (Alter, Größe, Gewicht). Zwei Datensätze addierst du
Spalte für Spalte, und „alle Werte verdoppeln“ ist $2\mathbf{x}$. Ein Python-Array `[1, 2, 3]` ist derselbe Gedanke.
:::
""")

k.vektor("Berechne $2\\mathbf{x} - \\mathbf{y}$ für $\\mathbf{x} = (1, 2, 3)^\\top$ und $\\mathbf{y} = (0, 1, -1)^\\top$.",
         [2 * 1 - 0, 2 * 2 - 1, 2 * 3 + 1],
         "Komponentenweise: $2 \\cdot 1 - 0 = 2$, $2 \\cdot 2 - 1 = 3$, $2 \\cdot 3 - (-1) = 7$.",
         tipps=["Rechne jede Komponente für sich.", "Multipliziere zuerst $\\mathbf{x}$ mit $2$, dann ziehe $\\mathbf{y}$ ab.",
                "Dritte Komponente: $6 - (-1)$."],
         rechenweg=rechnung([("2 \\cdot 1 - 0 = 2", "erste Komponente"), ("2 \\cdot 2 - 1 = 3", "zweite Komponente"),
                             ("2 \\cdot 3 - (-1) = 7", "dritte Komponente: Minus mal Minus")]),
         typische_fehler=[([2, 3, 5], "Dritte Komponente: $y_3 = -1$, also $6 - (-1) = 7$, nicht $6 - 1$."),
                          ([1, 1, 4], "Du hast $\\mathbf{x} - \\mathbf{y}$ gerechnet. Der Faktor $2$ gehört zu $\\mathbf{x}$.")])

# ── Seite 2: Geraden und Ebenen ──────────────────────────────────────────
k.erklaerung("Geraden und Ebenen", r"""
## Definition 4.5 und Satz 4.6

:::analogie 🧵 Faden und Tuch
Ein Faden ist eine [[Gerade|Gerade im Raum]]: Du hältst ihn an einem Punkt fest ([[Stützvektor]]) und ziehst in eine Richtung ([[Richtungsvektor]]).
Ein Tuch ist eine [[Ebene]]: ein Aufhängepunkt und zwei verschiedene Richtungen zum Spannen.
:::

Für $\mathbf{p}, \mathbf{u}, \mathbf{v} \in \mathbb{R}^n$ mit $\mathbf{u} \neq \mathbf{0}$ sind
$\{\mathbf{p} + t\mathbf{u} \mid t \in \mathbb{R}\}$ eine Gerade und $\{\mathbf{p} + s\mathbf{u} + t\mathbf{v} \mid s, t \in \mathbb{R}\}$ eine
Ebene, wenn zusätzlich $\mathbf{v} \neq \lambda\mathbf{u}$ für alle $\lambda$ gilt.
**Satz 4.6:** Durch $\mathbf{p} \neq \mathbf{q}$ verläuft genau eine Gerade, nämlich $\{\mathbf{p} + t(\mathbf{q} - \mathbf{p})\}$.
Durch drei Punkte, die nicht auf einer Geraden liegen, genau eine Ebene $\{\mathbf{p} + s(\mathbf{q} - \mathbf{p}) + t(\mathbf{r} - \mathbf{p})\}$.

:::rechnung Gerade durch $\mathbf{p} = (1, 2)^\top$ und $\mathbf{q} = (3, 3)^\top$
3 - 1 = 2 || erste Komponente des Richtungsvektors $\mathbf{q} - \mathbf{p}$
3 - 2 = 1 || zweite Komponente: Richtungsvektor $(2, 1)^\top$
1 + 2 \cdot 2 = 5 || Punkt für $t = 2$: erste Komponente
2 + 2 \cdot 1 = 4 || zweite Komponente: $(5, 4)^\top$ liegt auf der Geraden
:::

:::achtung Nicht eindeutig
Stützvektor und Richtungsvektoren darfst du ändern: $\mathbf{u}$ und $2\mathbf{u}$ beschreiben dieselbe Gerade. Zwei Beschreibungen
derselben Menge sehen oft verschieden aus. Bei der Ebene muss $\mathbf{v}$ **kein Vielfaches** von $\mathbf{u}$ sein, sonst entsteht nur eine Gerade.
:::

:::alt Als Wanderweg
Die Gerade ist ein langer gerader Weg: Du startest bei $\mathbf{p}$ und gehst $t$ Einheiten in Richtung $\mathbf{u}$,
rückwärts mit negativem $t$. Für die Ebene gibt es zwei Wege, und du darfst beliebig vor und zurück abbiegen.
:::
""")

k.mc("Sei $\\mathbf{u} = (1, 2, 0)^\\top$. Mit welchem $\\mathbf{v}$ ist $\\{\\mathbf{p} + s\\mathbf{u} + t\\mathbf{v} \\mid s, t \\in \\mathbb{R}\\}$ eine Ebene im Sinne von Def. 4.5?",
     ["$\\mathbf{v} = (0, 1, 1)^\\top$", "$\\mathbf{v} = (2, 4, 0)^\\top$", "$\\mathbf{v} = (-1, -2, 0)^\\top$", "$\\mathbf{v} = (0, 0, 0)^\\top$"],
     "Verlangt ist $\\mathbf{v} \\neq \\lambda\\mathbf{u}$ für alle $\\lambda$. $(2, 4, 0)^\\top = 2\\mathbf{u}$ und $(-1, -2, 0)^\\top = -\\mathbf{u}$ sind Vielfache, $\\mathbf{0} = 0 \\cdot \\mathbf{u}$ auch. Nur $(0, 1, 1)^\\top$ ist keins.",
     tipps=["Gesucht: kein $\\lambda$ mit $\\mathbf{v} = \\lambda\\mathbf{u}$.", "Ist $\\mathbf{v}$ ein Vielfaches von $\\mathbf{u}$, entsteht nur eine Gerade.",
            "Die dritte Komponente von $\\mathbf{u}$ ist $0$: Welcher Kandidat hat dort etwas anderes?"],
     fehler={"$\\mathbf{v} = (2, 4, 0)^\\top$": "$(2, 4, 0)^\\top = 2\\mathbf{u}$: ein Vielfaches, also nur eine Gerade.",
             "$\\mathbf{v} = (-1, -2, 0)^\\top$": "$(-1, -2, 0)^\\top = -\\mathbf{u}$: auch ein Vielfaches (negativer Faktor zählt).",
             "$\\mathbf{v} = (0, 0, 0)^\\top$": "Der Nullvektor ist $0 \\cdot \\mathbf{u}$, also ein Vielfaches von $\\mathbf{u}$."})

# ── Seite 3: Beweis Satz 4.6 ─────────────────────────────────────────────
k.erklaerung("Beweis von Satz 4.6 (Gerade)", r"""
## Warum nur eine Gerade durch zwei Punkte?

Wir zeigen: Enthält eine Gerade $g = \{\mathbf{a} + t\mathbf{v}\}$ die Punkte $\mathbf{p}$ und $\mathbf{q}$, so ist
$g = \{\mathbf{p} + t(\mathbf{q} - \mathbf{p})\}$. Die Punkte entsprechen Parametern $\alpha \neq \beta$: $\mathbf{p} = \mathbf{a} + \alpha\mathbf{v}$,
$\mathbf{q} = \mathbf{a} + \beta\mathbf{v}$. Subtrahieren liefert $\mathbf{q} - \mathbf{p} = (\beta - \alpha)\mathbf{v}$. Daraus folgt für jedes $t$

$$\mathbf{a} + t\mathbf{v} = \mathbf{p} + \tfrac{t - \alpha}{\beta - \alpha}(\mathbf{q} - \mathbf{p}).$$

Der Bruch durchläuft alle reellen Zahlen, also beschreiben beide Formeln dieselbe Menge.

:::rechnung Zahlenprobe mit $\mathbf{a} = (1, 0)^\top$, $\mathbf{v} = (2, 1)^\top$, $\alpha = 1$, $\beta = 3$, $t = 2$
1 + 2 \cdot 2 = 5 || erste Komponente von $\mathbf{a} + t\mathbf{v}$ (zweite: $0 + 2 \cdot 1 = 2$)
3 + \frac{2 - 1}{3 - 1} \cdot 4 = 5 || erste Komponente von $\mathbf{p} + \ldots$ mit $\mathbf{p} = (3, 1)^\top$, $\mathbf{q} - \mathbf{p} = (4, 2)^\top$
1 + \frac{2 - 1}{3 - 1} \cdot 2 = 2 || zweite Komponente: beide Formeln liefern $(5, 2)^\top$
:::

Bei drei Punkten läuft der Beweis ähnlich: Die Richtungsvektoren einer zweiten Ebene lassen sich durch $\mathbf{q} - \mathbf{p}$ und
$\mathbf{r} - \mathbf{p}$ ausdrücken (die Determinante $ad - bc$ ist $\neq 0$, sonst lägen die Punkte auf einer Geraden).
Zwei verschiedene Geraden haben deshalb höchstens einen gemeinsamen Punkt.

:::alt Als Lineal
Zwei Punkte auf dem Papier, dann legst du das Lineal an: Es gibt nur eine Möglichkeit. Jede andere Gerade durch beide Punkte
ist wieder dasselbe Lineal, nur mit anderem Startpunkt auf der Linie und anderer Schrittweite beschrieben.
:::
""")

k.ordnen("Ordne den Beweis von Satz 4.6 für die Gerade: Eine Gerade $g = \\{\\mathbf{a} + t\\mathbf{v}\\}$ enthalte $\\mathbf{p} \\neq \\mathbf{q}$.",
         ["Es gibt $\\alpha \\neq \\beta$ mit $\\mathbf{p} = \\mathbf{a} + \\alpha\\mathbf{v}$ und $\\mathbf{q} = \\mathbf{a} + \\beta\\mathbf{v}$.",
          "Subtraktion liefert $\\mathbf{q} - \\mathbf{p} = (\\beta - \\alpha)\\mathbf{v}$.",
          "Also gilt für jedes $t \\in \\mathbb{R}$: $\\mathbf{a} + t\\mathbf{v} = \\mathbf{p} + \\frac{t - \\alpha}{\\beta - \\alpha}(\\mathbf{q} - \\mathbf{p})$.",
          "Der Bruch $\\frac{t - \\alpha}{\\beta - \\alpha}$ durchläuft alle reellen Werte.",
          "Also ist $g = \\{\\mathbf{p} + t(\\mathbf{q} - \\mathbf{p}) \\mid t \\in \\mathbb{R}\\}$. $\\square$"],
         "Die beiden Punkte legen die Parameter $\\alpha \\neq \\beta$ fest. Dann lässt sich jede Gerade durch $\\mathbf{p}$ und $\\mathbf{q}$ umschreiben.",
         ablenker=["Wir wählen $\\alpha = \\beta$, damit sich die Rechnung vereinfacht.",
                   "Da $\\mathbf{q} - \\mathbf{p} = \\mathbf{0}$ ist, folgt die Behauptung."],
         tipps=["Beginne mit der Voraussetzung: Die Punkte liegen auf $g$.", "Zwei Gleichungen mit demselben $\\mathbf{a}$ lassen sich subtrahieren.",
                "Für $\\alpha = \\beta$ wäre $\\mathbf{p} = \\mathbf{q}$."])

k.wf("Zwei verschiedene Geraden im $\\mathbb{R}^3$ haben höchstens einen gemeinsamen Punkt.", True,
     "Zwei verschiedene gemeinsame Punkte würden nach Satz 4.6 beide Geraden festlegen, sie wären also gleich.",
     tipps=["Nutze: Durch zwei verschiedene Punkte verläuft genau eine Gerade."])

# ── Seite 4: Beispiel 4.7 ────────────────────────────────────────────────
k.erklaerung("Schnittpunkt von Gerade und Ebene", r"""
## Beispiel 4.7 und Bemerkung 4.8

Gerade $g = \{(0, 1, 1)^\top + r(1, 1, 1)^\top\}$, Ebene $E = \{(0, 0, 1)^\top + s(1, 1, 0)^\top + t(1, 2, 2)^\top\}$.
Im Schnittpunkt gilt **für alle drei Komponenten** Gleichheit. Das ergibt ein Gleichungssystem für $r, s, t$:

:::rechnung Schnittpunkt Schritt für Schritt
\text{(I) } s + t - r = 0 || erste Komponente: $0 + r = 0 + s + t$
\text{(II) } s + 2t - r = 1 || zweite Komponente
\text{(III) } 2t - r = 0 || dritte Komponente
\text{(II) } - \text{(I): } t = 1 || Subtraktion
\text{(III): } r = 2 \text{ und (I): } s = 1 || Einsetzen
0 + 2 \cdot 1 = 2 || Punkt auf der Geraden mit $r = 2$: erste Komponente (dann $3$ und $3$)
:::

Der einzige Schnittpunkt ist $\mathbf{x}^* = (2, 3, 3)^\top$. Beim Raytracing (Bem. 4.8) schneidet man so einen Sehstrahl mit einer ebenen
Fläche; danach prüft man, ob der Punkt auf dem vorwärts gerichteten Strahl und innerhalb der Fläche liegt.

:::alt Als Treffpunkt
Die Gerade ist eine Drohne auf Flugbahn, die Ebene ein Dach. Gesucht: Zeitpunkt $r$, an dem die Drohne das Dach berührt. Das Dach hat zwei
Koordinaten $s, t$ für den Ort auf dem Dach. Drei Gleichungen (x, y, z) für drei Unbekannte $r, s, t$.
:::
""")

k.vektor("Eine Gerade $g = \\{(1, 0, 0)^\\top + r(0, 1, 1)^\\top\\}$ schneidet die Ebene $E = \\{(0, 0, 2)^\\top + s(1, 0, 0)^\\top + t(0, 1, 0)^\\top\\}$. Bestimme den Schnittpunkt.",
         [1, 2, 2],
         "Komponenten: $1 = s$, $r = t$, $r = 2$. Also $r = 2$, und der Punkt ist $(1, 0, 0)^\\top + 2 \\cdot (0, 1, 1)^\\top = (1, 2, 2)^\\top$.",
         tipps=["Setze $\\mathbf{p}_g + r\\mathbf{u}_g = \\mathbf{p}_E + s\\mathbf{u}_E + t\\mathbf{v}_E$ komponentenweise an.", "Die dritte Komponente liefert $r$ direkt: $r = 2$.", "Setze $r = 2$ in die Gerade ein."],
         rechenweg=rechnung([("\\text{(I) } 1 = s", "erste Komponente: $1 + r \\cdot 0 = 0 + s \\cdot 1 + t \\cdot 0$"),
                             ("\\text{(II) } r = t", "zweite Komponente: $0 + r \\cdot 1 = 0 + s \\cdot 0 + t \\cdot 1$"),
                             ("\\text{(III) } r = 2", "dritte Komponente: $0 + r \\cdot 1 = 2$"),
                             ("0 + 2 \\cdot 1 = 2", "zweite Komponente des Punktes: $(1, 2, 2)^\\top$")]),
         typische_fehler=[([2, 1, 1], "Das sind die Parameter $(r, s, t)$, nicht der Punkt. Setze $r = 2$ in die Gerade ein."),
                          ([1, 0, 2], "Das ist der Punkt der Ebene für $s = 1$, $t = 0$. Auch $t = r = 2$ gehört zum Schnittpunkt.")])

# ── Seite 5: Länge und Skalarprodukt ─────────────────────────────────────
k.erklaerung("Länge und Skalarprodukt", r"""
## Definition 4.9 und Beobachtung 4.10

Aus dem Satz des Pythagoras folgt die Länge $\sqrt{x_1^2 + x_2^2 + x_3^2}$ im Raum. Für alle $n$ gilt:

$$(\mathbf{x} \mid \mathbf{y}) := \sum_{j=1}^n x_j y_j, \qquad \lVert \mathbf{x} \rVert := \sqrt{(\mathbf{x} \mid \mathbf{x})}.$$

Das ist das [[Standardskalarprodukt]]; die Zahl $\lVert\mathbf{x}\rVert$ heißt [[euklidische Länge]]. Der **Abstand** von $\mathbf{x}$ zu $\mathbf{y}$ ist $\lVert \mathbf{x} - \mathbf{y} \rVert$.
Das Ergebnis des Skalarprodukts ist eine **Zahl**, kein Vektor.

:::visual vektoren2d
{"vektoren": [{"x": 3, "y": 1}, {"x": -1, "y": 3}], "zeige": ["norm", "skalarprodukt"],
 "unterschrift": "$(\\mathbf{a} \\mid \\mathbf{b}) = 3 \\cdot (-1) + 1 \\cdot 3 = 0$: Die Vektoren stehen senkrecht."}
:::

:::rechnung $\mathbf{x} = (1, 2, 3)^\top$, $\mathbf{y} = (4, -1, 2)^\top$
1 \cdot 4 + 2 \cdot (-1) + 3 \cdot 2 = 8 || $(\mathbf{x} \mid \mathbf{y})$
\sqrt{1^2 + 2^2 + 3^2} = \sqrt{14} || $\lVert\mathbf{x}\rVert$
\sqrt{(-3)^2 + 3^2 + 1^2} = \sqrt{19} || Abstand: $\mathbf{x} - \mathbf{y} = (-3, 3, 1)^\top$
14 - 2 \cdot 8 + 21 = 19 || Probe der Formel $\lVert\mathbf{x} - \mathbf{y}\rVert^2 = \lVert\mathbf{x}\rVert^2 - 2(\mathbf{x} \mid \mathbf{y}) + \lVert\mathbf{y}\rVert^2$
:::

Weitere Regeln (Beob. 4.10): $\lVert\mathbf{x}\rVert \ge 0$, $\lVert\mathbf{x}\rVert = 0 \Leftrightarrow \mathbf{x} = \mathbf{0}$, $\lVert\mathbf{e}^{(i)}\rVert = 1$,
$(\mathbf{x} \mid \mathbf{y}) = (\mathbf{y} \mid \mathbf{x})$, $\lVert\lambda\mathbf{x}\rVert = |\lambda|\,\lVert\mathbf{x}\rVert$ und Linearität in beiden Argumenten. Für $n = 1$ ist die Länge der Betrag.

:::alt Als Gewichtung
$(\mathbf{x} \mid \mathbf{y})$ multipliziert gleiche Positionen und addiert: wie ein Warenkorb, bei dem $\mathbf{x}$ die Mengen und $\mathbf{y}$ die Preise
sind. Das Ergebnis ist der Gesamtpreis, eine einzelne Zahl. Die Länge ist die Wurzel aus „Menge mal Menge“.
:::
""")

k.zahl("Berechne $(\\mathbf{x} \\mid \\mathbf{y})$ für $\\mathbf{x} = (2, -1, 3)^\\top$ und $\\mathbf{y} = (1, 4, 2)^\\top$.",
       sp([2, -1, 3], [1, 4, 2]),
       "$2 \\cdot 1 + (-1) \\cdot 4 + 3 \\cdot 2 = 2 - 4 + 6 = 4$.",
       tipps=["Multipliziere gleiche Positionen.", "Addiere die drei Produkte zu **einer Zahl**.", "$2 - 4 + 6$."],
       rechenweg=rechnung([("2 \\cdot 1 + (-1) \\cdot 4 + 3 \\cdot 2 = 2 - 4 + 6", "Produkte der Komponenten"), ("2 - 4 + 6 = 4", "addieren")]),
       typische_fehler=[(6, "Du hast $-1 \\cdot 4$ als $+4$ gerechnet. Es ist $-4$."),
                        (14, "Das ist die Summe der Beträge der Produkte. Das Vorzeichen von $(-1) \\cdot 4 = -4$ zählt.")])

k.zahl("Berechne die Länge $\\lVert\\mathbf{x}\\rVert$ von $\\mathbf{x} = (2, 3, 6)^\\top$.", 7,
       "$\\lVert\\mathbf{x}\\rVert = \\sqrt{4 + 9 + 36} = \\sqrt{49} = 7$.",
       tipps=["Länge = Wurzel aus der Summe der Quadrate.", "$2^2 + 3^2 + 6^2 = 49$.", "$\\sqrt{49}$."],
       rechenweg=rechnung([("2^2 + 3^2 + 6^2 = 49", "Quadrate addieren"), ("\\sqrt{49} = 7", "Wurzel ziehen")]),
       typische_fehler=[(49, "Das ist $\\lVert\\mathbf{x}\\rVert^2$. Du musst noch die Wurzel ziehen."), (11, "Die Länge ist nicht die Summe der Einträge ($2 + 3 + 6$), sondern die Wurzel der Summe der Quadrate.")])

# ── Seite 6: Orthogonalität, Hyperebene ──────────────────────────────────
k.erklaerung("Orthogonalität, Normalenvektor, Hyperebene", r"""
## Definition 4.11 und 4.14, Beispiele 4.12 und 4.13

Zwei Vektoren sind [[orthogonal]] ($\mathbf{x} \perp \mathbf{y}$), wenn $(\mathbf{x} \mid \mathbf{y}) = 0$. Der Nullvektor ist zu jedem Vektor orthogonal.
Ein [[Normalenvektor]] $\mathbf{n} \neq \mathbf{0}$ einer Ebene im $\mathbb{R}^3$ ist orthogonal zu ihren Richtungsvektoren.
Eine [[Hyperebene]] ist $H = \{\mathbf{x} \in \mathbb{R}^n \mid (\mathbf{x} \mid \mathbf{a}) = b\}$ mit $\mathbf{a} \neq \mathbf{0}$; $\mathbf{a}$ ist ein Normalenvektor von $H$.

:::rechnung Ebene aus Bsp. 4.7: $\mathbf{u} = (1, 1, 0)^\top$, $\mathbf{v} = (1, 2, 2)^\top$, $\mathbf{p} = (0, 0, 1)^\top$, $\mathbf{n} = (2, -2, 1)^\top$
1 \cdot 2 + 1 \cdot (-2) + 0 \cdot 1 = 0 || $(\mathbf{u} \mid \mathbf{n}) = 0$
1 \cdot 2 + 2 \cdot (-2) + 2 \cdot 1 = 0 || $(\mathbf{v} \mid \mathbf{n}) = 0$
0 \cdot 2 + 0 \cdot (-2) + 1 \cdot 1 = 1 || $b = (\mathbf{p} \mid \mathbf{n})$: jeder Punkt der Ebene hat $(\mathbf{x} \mid \mathbf{n}) = 1$, also $2x_1 - 2x_2 + x_3 = 1$
:::

Im $\mathbb{R}^3$ sind Ebene und Hyperebene dasselbe. Im $\mathbb{R}^4$ hat eine Ebene zwei Parameter, eine Hyperebene dagegen $n - 1 = 3$ frei wählbare Koordinaten
(Dimension $n - 1$ zeigt Satz 4.114 in Kap. 24). **Bem. 4.17:** Eine Hyperebene teilt den Raum nach $(\mathbf{n} \mid \mathbf{x}) < b$ und $(\mathbf{n} \mid \mathbf{x}) > b$.
So entscheiden lineare Klassifikatoren.

:::alt Als Tür
Eine Tür ist (fast) eine Ebene. Der Türgriff zeigt senkrecht heraus: das ist der Normalenvektor. Auf welcher Seite der Tür du stehst, siehst du am Vorzeichen
von $(\mathbf{n} \mid \mathbf{x}) - b$. Auf der Tür selbst ist es $0$.
:::
""")

k.mehrfach("Welche der Vektoren sind orthogonal zu $\\mathbf{x} = (1, 1, 0)^\\top$?",
           ["$(1, -1, 5)^\\top$", "$(0, 0, 1)^\\top$", "$(0, 0, 0)^\\top$"],
           ["$(1, 1, 1)^\\top$", "$(2, 1, 0)^\\top$"],
           "Orthogonal heißt Skalarprodukt $0$: $1 - 1 + 0 = 0$, $0$, $0$. Dagegen $1 + 1 + 0 = 2$ und $2 + 1 = 3$.",
           tipps=["Berechne $(\\mathbf{x} \\mid \\mathbf{y})$ für jeden Kandidaten.", "Der Nullvektor ist zu allem orthogonal (Def. 4.11)."],
           fehler={"$(1, 1, 1)^\\top$": "$(\\mathbf{x} \\mid \\mathbf{y}) = 1 + 1 + 0 = 2 \\neq 0$. Dass er in dritter Richtung senkrecht ist, reicht nicht.",
                   "$(2, 1, 0)^\\top$": "$2 + 1 + 0 = 3 \\neq 0$."})

k.mc("Sei $H = \\{\\mathbf{x} \\in \\mathbb{R}^2 \\mid (\\mathbf{x} \\mid \\mathbf{a}) = 2\\}$ mit $\\mathbf{a} = (1, 2)^\\top$. Auf welcher Seite von $H$ liegt $\\mathbf{x} = (3, 1)^\\top$?",
     ["Auf der Seite $(\\mathbf{x} \\mid \\mathbf{a}) > 2$", "Auf der Seite $(\\mathbf{x} \\mid \\mathbf{a}) < 2$", "Auf $H$ selbst"],
     "$(\\mathbf{x} \\mid \\mathbf{a}) = 3 \\cdot 1 + 1 \\cdot 2 = 5 > 2$ (Bem. 4.17).",
     tipps=["Rechne $(\\mathbf{x} \\mid \\mathbf{a})$ aus und vergleiche mit $b = 2$.", "$3 \\cdot 1 + 1 \\cdot 2$."],
     fehler={"Auf der Seite $(\\mathbf{x} \\mid \\mathbf{a}) < 2$": "$3 + 2 = 5$ ist größer als $2$.",
             "Auf $H$ selbst": "Dazu müsste $(\\mathbf{x} \\mid \\mathbf{a}) = 2$ gelten, es ist aber $5$."})

# ── Seite 7: Satz 4.15 ───────────────────────────────────────────────────
k.erklaerung("Abstand eines Punktes von einer Hyperebene", r"""
## Satz 4.15 und Beispiel 4.16

**Satz 4.15.** Für $H = \{\mathbf{y} \mid (\mathbf{y} \mid \mathbf{a}) = b\}$ mit $\mathbf{a} \neq \mathbf{0}$ und $\mathbf{x} \in \mathbb{R}^n$ gilt

$$\min\{\lVert\mathbf{x} - \mathbf{p}\rVert \mid \mathbf{p} \in H\} = \frac{|(\mathbf{x} \mid \mathbf{a}) - b|}{\lVert\mathbf{a}\rVert}.$$

*Beweisidee:* Von $\mathbf{x}$ geht man in Richtung $\mathbf{a}$ bis zur Hyperebene: $\mathbf{p} := \mathbf{x} - \alpha\mathbf{a}$ mit $\alpha := ((\mathbf{x} \mid \mathbf{a}) - b)/\lVert\mathbf{a}\rVert^2$.
Dann ist $\mathbf{p} \in H$, und für jedes $\mathbf{y} \in H$ stehen $\mathbf{p} - \mathbf{y}$ und $\mathbf{x} - \mathbf{p}$ senkrecht (Pythagoras).

:::rechnung Beispiel 4.16: $H$ mit $\mathbf{n} = (2, -2, 1)^\top$, $b = 1$, Abstand vom Ursprung; danach von $\mathbf{x} = (3, 0, 0)^\top$
\sqrt{2^2 + (-2)^2 + 1^2} = 3 || $\lVert\mathbf{n}\rVert$
\frac{|0 - 1|}{3} = \frac{1}{3} || Abstand des Ursprungs
3 \cdot 2 + 0 \cdot (-2) + 0 \cdot 1 = 6 || $(\mathbf{x} \mid \mathbf{n})$
\frac{|6 - 1|}{3} = \frac{5}{3} || Abstand von $\mathbf{x} = (3, 0, 0)^\top$
:::

Der nächste Punkt für den Ursprung ist $\mathbf{p} = \frac19 (2, -2, 1)^\top$. Der kürzeste Weg zur Hyperebene steht immer **senkrecht** auf ihr.

:::alt Als Lot
Du stehst im Zimmer und willst zur Wand (Ebene). Der kürzeste Weg ist das Lot: Du gehst senkrecht zur Wand. Satz 4.15 sagt, wie lang dieser Weg ist:
Einsetzen in die Ebenengleichung, den Fehler $|(\mathbf{x} \mid \mathbf{a}) - b|$ nehmen und durch die Länge von $\mathbf{a}$ teilen.
:::
""")

k.ordnen("Ordne den Beweis von Satz 4.15 (Abstand eines Punktes von einer Hyperebene).",
         ["Setze $\\alpha := ((\\mathbf{x} \\mid \\mathbf{a}) - b) / \\lVert\\mathbf{a}\\rVert^2$ und $\\mathbf{p} := \\mathbf{x} - \\alpha\\mathbf{a}$.",
          "Es gilt $(\\mathbf{p} \\mid \\mathbf{a}) = (\\mathbf{x} \\mid \\mathbf{a}) - \\alpha\\lVert\\mathbf{a}\\rVert^2 = b$, also $\\mathbf{p} \\in H$.",
          "Für jedes $\\mathbf{y} \\in H$ gilt $(\\mathbf{p} - \\mathbf{y} \\mid \\mathbf{a}) = b - b = 0$.",
          "Damit sind $\\mathbf{p} - \\mathbf{y}$ und $\\mathbf{x} - \\mathbf{p} = \\alpha\\mathbf{a}$ orthogonal, und es folgt $\\lVert\\mathbf{x} - \\mathbf{y}\\rVert^2 = \\lVert\\mathbf{x} - \\mathbf{p}\\rVert^2 + \\lVert\\mathbf{p} - \\mathbf{y}\\rVert^2 \\ge \\lVert\\mathbf{x} - \\mathbf{p}\\rVert^2$.",
          "Das Minimum wird also bei $\\mathbf{p}$ angenommen, und $\\lVert\\mathbf{x} - \\mathbf{p}\\rVert = |\\alpha|\\,\\lVert\\mathbf{a}\\rVert = |(\\mathbf{x} \\mid \\mathbf{a}) - b| / \\lVert\\mathbf{a}\\rVert$. $\\square$"],
         "Der Punkt $\\mathbf{p}$ liegt auf $H$ und der Rest $\\mathbf{x} - \\mathbf{p}$ zeigt in Richtung $\\mathbf{a}$, also senkrecht zu $H$. Pythagoras liefert die Minimalität.",
         ablenker=["Wir wählen $\\mathbf{p}$ als beliebigen Punkt von $H$ und rechnen den Abstand direkt aus.",
                   "Da $\\lVert\\mathbf{p} - \\mathbf{y}\\rVert^2 \\le 0$ gilt, ist $\\mathbf{p}$ der nächste Punkt."],
         tipps=["Die Konstruktion von $\\mathbf{p}$ kommt zuerst, dann der Nachweis $\\mathbf{p} \\in H$.", "Für den Pythagoras brauchst du die Orthogonalität von $\\mathbf{p} - \\mathbf{y}$ und $\\mathbf{a}$.",
                "Ganz am Ende steht der Wert des Minimums."])

k.luecke("Satz 4.15 für $H = \\{\\mathbf{y} \\in \\mathbb{R}^3 \\mid (\\mathbf{y} \\mid \\mathbf{a}) = 1\\}$ mit $\\mathbf{a} = (2, -2, 1)^\\top$ und $\\mathbf{x} = (3, 0, 0)^\\top$. Fülle die Lücken.",
         "\\frac{|\\luecke - \\luecke|}{\\luecke}",
         [[6], [1], [3]],
         "$(\\mathbf{x} \\mid \\mathbf{a}) = 6$, $b = 1$ und $\\lVert\\mathbf{a}\\rVert = 3$. Der Abstand ist $\\frac53$.",
         tipps=["Die erste Lücke ist $(\\mathbf{x} \\mid \\mathbf{a})$.", "Die dritte Lücke ist $\\lVert\\mathbf{a}\\rVert = \\sqrt{4 + 4 + 1}$.", "$6$, $1$, $3$."],
         rechenweg=rechnung([("3 \\cdot 2 + 0 \\cdot (-2) + 0 \\cdot 1 = 6", "$(\\mathbf{x} \\mid \\mathbf{a})$"), ("\\sqrt{4 + 4 + 1} = 3", "$\\lVert\\mathbf{a}\\rVert$"),
                             ("\\frac{|6 - 1|}{3} = \\frac{5}{3}", "Abstand")]),
         typische_fehler=[([6, 1, 9], "$\\lVert\\mathbf{a}\\rVert = 3$, nicht $9$: $9$ ist $\\lVert\\mathbf{a}\\rVert^2$. Die Wurzel gehört dazu.")])

k.zahl("Berechne den Abstand von $\\mathbf{x} = (4, 1, 2)^\\top$ zur Ebene $H = \\{\\mathbf{y} \\in \\mathbb{R}^3 \\mid (\\mathbf{y} \\mid \\mathbf{a}) = 3\\}$ mit $\\mathbf{a} = (1, 2, 2)^\\top$.",
       F(7, 3),
       "$(\\mathbf{x} \\mid \\mathbf{a}) = 4 + 2 + 4 = 10$, $\\lVert\\mathbf{a}\\rVert = 3$. Abstand $= |10 - 3| / 3 = 7/3$.",
       gekuerzt=True,
       tipps=["Satz 4.15: $|(\\mathbf{x} \\mid \\mathbf{a}) - b| / \\lVert\\mathbf{a}\\rVert$.", "$(\\mathbf{x} \\mid \\mathbf{a}) = 10$.", "$\\lVert\\mathbf{a}\\rVert = 3$."],
       rechenweg=rechnung([("4 \\cdot 1 + 1 \\cdot 2 + 2 \\cdot 2 = 10", "$(\\mathbf{x} \\mid \\mathbf{a})$"), ("\\sqrt{1 + 4 + 4} = 3", "$\\lVert\\mathbf{a}\\rVert$"),
                           ("\\frac{|10 - 3|}{3} = \\frac{7}{3}", "Abstand")]),
       typische_fehler=[(7, "Du hast nicht durch $\\lVert\\mathbf{a}\\rVert = 3$ geteilt: Der Zähler ist nur der „Gleichungsfehler“, nicht der Abstand."),
                        (F(13, 3), "Du hast $b$ addiert. Es heißt $(\\mathbf{x} \\mid \\mathbf{a}) - b$."),
                        (F(7, 9), "Du hast durch $\\lVert\\mathbf{a}\\rVert^2 = 9$ geteilt. Im Nenner steht $\\lVert\\mathbf{a}\\rVert = 3$.")])

# ── Seite 8: Kreuzprodukt ────────────────────────────────────────────────
k.erklaerung("Das Kreuzprodukt im ℝ³", r"""
## Definition 4.18 und Satz 4.19

Zu zwei Richtungsvektoren einer Ebene im $\mathbb{R}^3$ suchen wir einen Normalenvektor. Das [[Kreuzprodukt]] liefert ihn direkt, als **Vektor**:

$$\mathbf{x} \times \mathbf{y} := \begin{pmatrix} x_2 y_3 - x_3 y_2 \\ x_3 y_1 - x_1 y_3 \\ x_1 y_2 - x_2 y_1 \end{pmatrix}.$$

**Satz 4.19.** $(\mathbf{x} \times \mathbf{y}) \perp \mathbf{x}$, $(\mathbf{x} \times \mathbf{y}) \perp \mathbf{y}$ und $\mathbf{y} \times \mathbf{x} = -(\mathbf{x} \times \mathbf{y})$.
Das Produkt ist genau dann $\mathbf{0}$, wenn $\mathbf{x} = \mathbf{0}$ oder $\mathbf{y} = \lambda\mathbf{x}$.

:::rechnung $\mathbf{u} = (1, 1, 0)^\top$ und $\mathbf{v} = (1, 2, 2)^\top$ (Bsp. 4.22)
1 \cdot 2 - 0 \cdot 2 = 2 || erste Komponente: $u_2 v_3 - u_3 v_2$
0 \cdot 1 - 1 \cdot 2 = -2 || zweite: $u_3 v_1 - u_1 v_3$
1 \cdot 2 - 1 \cdot 1 = 1 || dritte: $u_1 v_2 - u_2 v_1$, also $\mathbf{u} \times \mathbf{v} = (2, -2, 1)^\top = \mathbf{n}$
:::

Merkregel: Die Indizes laufen zyklisch ($2,3$ dann $3,1$ dann $1,2$). Die Reihenfolge zählt: $\mathbf{e}^{(1)} \times \mathbf{e}^{(2)} = \mathbf{e}^{(3)}$, aber $\mathbf{e}^{(2)} \times \mathbf{e}^{(1)} = -\mathbf{e}^{(3)}$.

:::alt Als Schraube
Dreh den ersten Vektor zum zweiten, wie eine Schraube mit Rechtsgewinde: Sie bewegt sich in Richtung des Kreuzprodukts, senkrecht zur Drehebene.
Dreht man andersherum, läuft sie in die Gegenrichtung ($\mathbf{y} \times \mathbf{x} = -\mathbf{x} \times \mathbf{y}$).
:::
""")

k.vektor("Berechne $\\mathbf{x} \\times \\mathbf{y}$ für $\\mathbf{x} = (2, 0, 1)^\\top$ und $\\mathbf{y} = (1, 3, -1)^\\top$.",
         kp([2, 0, 1], [1, 3, -1]),
         "$(0 \\cdot (-1) - 1 \\cdot 3,\\ 1 \\cdot 1 - 2 \\cdot (-1),\\ 2 \\cdot 3 - 0 \\cdot 1) = (-3, 3, 6)$. Probe: $(\\mathbf{x} \\times \\mathbf{y} \\mid \\mathbf{x}) = -6 + 0 + 6 = 0$.",
         tipps=["Erste Komponente: $x_2 y_3 - x_3 y_2$.", "Zweite: $x_3 y_1 - x_1 y_3$, dritte: $x_1 y_2 - x_2 y_1$.", "Probe mit dem Skalarprodukt mit $\\mathbf{x}$."],
         rechenweg=rechnung([("0 \\cdot (-1) - 1 \\cdot 3 = -3", "erste Komponente"), ("1 \\cdot 1 - 2 \\cdot (-1) = 3", "zweite Komponente"),
                             ("2 \\cdot 3 - 0 \\cdot 1 = 6", "dritte Komponente"), ("2 \\cdot (-3) + 0 \\cdot 3 + 1 \\cdot 6 = 0", "Probe: orthogonal zu $\\mathbf{x}$")]),
         typische_fehler=[([3, -3, -6], "Das ist $\\mathbf{y} \\times \\mathbf{x}$ (Satz 4.19). Die Reihenfolge entscheidet über das Vorzeichen."),
                          ([-3, -3, 6], "In der zweiten Komponente steht $x_3 y_1 - x_1 y_3 = 1 + 2 = 3$ (nicht umgekehrt).")])

k.ordnen("Ordne den Beweis von Satz 4.19.",
         ["Ausmultiplizieren: $(\\mathbf{x} \\times \\mathbf{y} \\mid \\mathbf{x}) = (x_2y_3 - x_3y_2)x_1 + (x_3y_1 - x_1y_3)x_2 + (x_1y_2 - x_2y_1)x_3$. Alle Terme heben sich paarweise auf, also $= 0$.",
          "Vertauschen von $\\mathbf{x}$ und $\\mathbf{y}$ ändert in jeder Komponente das Vorzeichen: $\\mathbf{y} \\times \\mathbf{x} = -(\\mathbf{x} \\times \\mathbf{y})$.",
          "Daraus folgt $(\\mathbf{x} \\times \\mathbf{y} \\mid \\mathbf{y}) = -(\\mathbf{y} \\times \\mathbf{x} \\mid \\mathbf{y}) = 0$.",
          "Ist $\\mathbf{x} = \\mathbf{0}$ oder $\\mathbf{y} = \\lambda\\mathbf{x}$, verschwinden alle Komponenten von $\\mathbf{x} \\times \\mathbf{y}$.",
          "Ist umgekehrt $\\mathbf{x} \\times \\mathbf{y} = \\mathbf{0}$ und $x_i \\neq 0$, so gilt $x_i y_j = x_j y_i$ für alle $j$, also $\\mathbf{y} = (y_i / x_i)\\,\\mathbf{x}$. $\\square$"],
         "Die Orthogonalität zu $\\mathbf{x}$ folgt durch Ausmultiplizieren, die zu $\\mathbf{y}$ aus der Antisymmetrie. Der Zusatz zeigt man in beide Richtungen.",
         ablenker=["Wegen $\\mathbf{x} \\times \\mathbf{y} = \\mathbf{y} \\times \\mathbf{x}$ muss man die Orthogonalität zu $\\mathbf{y}$ nicht gesondert prüfen."],
         tipps=["Erst Orthogonalität zu $\\mathbf{x}$, dann Antisymmetrie, dann Orthogonalität zu $\\mathbf{y}$.", "Der Zusatz mit „genau dann“ besteht aus zwei Richtungen.",
                "Bei der Rückrichtung nutzt man eine Komponente $x_i \\neq 0$."])

# ── Seite 9: Fläche und Volumen ──────────────────────────────────────────
k.erklaerung("Fläche und Spatvolumen", r"""
## Beobachtung 4.20, 4.21 und Beispiel 4.22

**Beob. 4.20.** Für $\mathbf{u}, \mathbf{v} \in \mathbb{R}^3$ ist $\lVert\mathbf{u} \times \mathbf{v}\rVert$ der Flächeninhalt des von ihnen aufgespannten Parallelogramms.
Im $\mathbb{R}^2$ ist er $|u_1 v_2 - u_2 v_1|$.
**Beob. 4.21.** Das [[Spatvolumen]] eines von $\mathbf{u}, \mathbf{v}, \mathbf{w}$ aufgespannten Spats ist $|(\mathbf{u} \times \mathbf{v} \mid \mathbf{w})|$: Grundfläche mal Höhe,
wobei die Höhe nach Satz 4.15 der Abstand von $\mathbf{w}$ zur Grundebene ist.

:::visual vektoren2d
{"vektoren": [{"x": 3, "y": 1}, {"x": 1, "y": 2}], "zeige": ["summe"],
 "unterschrift": "Parallelogramm aus $\\mathbf{u}$ und $\\mathbf{v}$: Fläche $|3 \\cdot 2 - 1 \\cdot 1| = 5$."}
:::

:::rechnung Beispiel 4.22 mit $\mathbf{n} = \mathbf{u} \times \mathbf{v} = (2, -2, 1)^\top$ und $\mathbf{w} = (2, 0, 1)^\top$
\sqrt{4 + 4 + 1} = 3 || Fläche des Parallelogramms: $\lVert\mathbf{n}\rVert$
2 \cdot 2 - 2 \cdot 0 + 1 \cdot 1 = 5 || Volumen $|(\mathbf{n} \mid \mathbf{w})|$
\frac{5}{3} = \frac{5}{3} || Höhe nach Satz 4.15: $|(\mathbf{w} \mid \mathbf{n})| / \lVert\mathbf{n}\rVert$
3 \cdot \frac{5}{3} = 5 || Grundfläche mal Höhe: dasselbe Volumen
:::

*Beweisidee 4.20:* Zerlege $\mathbf{v}$ in einen Anteil entlang $\mathbf{u}$ und einen senkrechten Rest $\mathbf{w}'$ (die Höhe). Dann ist $\lVert\mathbf{u} \times \mathbf{v}\rVert = \lVert\mathbf{u}\rVert\,\lVert\mathbf{w}'\rVert$.

:::alt Als Ziegelstein
Ein Ziegelstein hat Boden (Grundfläche) und Höhe; Volumen ist Fläche mal Höhe. Das Kreuzprodukt liefert die Fläche und die Richtung der Höhe,
das Skalarprodukt mit der dritten Kante $\mathbf{w}$ misst, wie hoch $\mathbf{w}$ in diese Richtung hinaufreicht.
:::
""")

# ══ Praxis ═══════════════════════════════════════════════════════════════
def _rv(rng, lo=-3, hi=3, n=3):
    return [rng.randint(lo, hi) for _ in range(n)]


def schnitt_gerade_ebene(rng):
    """Gerade p0 + r w schneidet Ebene p + s u + t v (Bsp. 4.7)."""
    while True:
        p, u, v, w = _rv(rng, -2, 2), _rv(rng, -2, 2), _rv(rng, -2, 2), _rv(rng, -2, 2)
        r0, s0, t0 = rng.randint(-2, 2), rng.randint(-2, 2), rng.randint(-2, 2)
        if det([u, v, w]) != 0 and len({r0, s0, t0}) >= 2 and r0 != 0:
            break
    x = [p[i] + s0 * u[i] + t0 * v[i] for i in range(3)]
    p0 = [x[i] - r0 * w[i] for i in range(3)]
    loes = mathlib.lgs_loesen([[u[i], v[i], -w[i]] for i in range(3)], [p0[i] - p[i] for i in range(3)])
    assert loes["art"] == "eindeutig" and loes["x"] == [s0, t0, r0]
    zeilen = [(f"\\text{{({'I' * (i + 1) if i < 3 else ''}) }} {u[i]}s + ({v[i]})t - ({w[i]})r = {p0[i] - p[i]}",
               f"Komponente {i + 1}: ${p0[i]} + r \\cdot {tx(w[i])} = {p[i]} + s \\cdot {tx(u[i])} + t \\cdot {tx(v[i])}$") for i in range(3)]
    zeilen.append((f"\\text{{Lösung }} s = {s0},\\ t = {t0},\\ r = {r0}", "Gauß-Verfahren oder Elimination"))
    zeilen += [(f"{p0[i]} + {tx(r0)} \\cdot {tx(w[i])} = {x[i]}", f"Komponente {i + 1} des Schnittpunkts") for i in range(3)]
    fehler = [([s0, t0, r0], "Das sind die Parameter $(s, t, r)$, nicht der Punkt. Setze $r$ in die Gerade ein."),
              ([p0[i] + s0 * w[i] for i in range(3)], "Du hast den Parameter $s$ der Ebene in die Gerade eingesetzt. Dort steht $r$.")]
    return {"typ": "vektor",
            "frage": f"Bestimme den Schnittpunkt der Geraden $g = \\{{{vt(p0)} + r{vt(w)}\\}}$ mit der Ebene $E = \\{{{vt(p)} + s{vt(u)} + t{vt(v)}\\}}$.",
            "loesung": x,
            "tipps": ["Setze beide Darstellungen gleich und vergleiche die drei Komponenten: ein Gleichungssystem für $r, s, t$.",
                      "Löse es durch Elimination (Bsp. 4.7) und achte auf die Vorzeichen bei $r$.",
                      f"Es kommt $r = {r0}$ heraus. Setze das in die Geradengleichung ein."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Im Schnittpunkt liegt der Punkt in beiden Mengen: Gleichheit in jeder Komponente ergibt drei Gleichungen für die drei Parameter.",
            "typische_fehler": ohne_gleiche(x, fehler)}


def kreuzprodukt_normale(rng):
    """Normalenvektor einer Ebene als u × v (Def. 4.18, Satz 4.19)."""
    while True:
        u, v = _rv(rng), _rv(rng)
        n = kp(u, v)
        if any(c != 0 for c in n):
            break
    falsch_mitte = [n[0], -n[1], n[2]]
    fehler = [([-c for c in n], "Das ist $\\mathbf{v} \\times \\mathbf{u}$. Die Reihenfolge bestimmt das Vorzeichen (Satz 4.19)."),
              (falsch_mitte, "Die mittlere Komponente ist $u_3 v_1 - u_1 v_3$, nicht $u_1 v_3 - u_3 v_1$.")]
    zeilen = [(f"{u[1]} \\cdot {tx(v[2])} - {tx(u[2])} \\cdot {tx(v[1])} = {tx(n[0])}", "erste Komponente $u_2 v_3 - u_3 v_2$"),
              (f"{u[2]} \\cdot {tx(v[0])} - {tx(u[0])} \\cdot {tx(v[2])} = {tx(n[1])}", "zweite Komponente $u_3 v_1 - u_1 v_3$"),
              (f"{u[0]} \\cdot {tx(v[1])} - {tx(u[1])} \\cdot {tx(v[0])} = {tx(n[2])}", "dritte Komponente $u_1 v_2 - u_2 v_1$"),
              (f"{tx(u[0])} \\cdot {tx(n[0])} + {tx(u[1])} \\cdot {tx(n[1])} + {tx(u[2])} \\cdot {tx(n[2])} = 0", "Probe: orthogonal zu $\\mathbf{u}$")]
    return {"frage": f"Bestimme einen Normalenvektor der Ebene mit den Richtungsvektoren $\\mathbf{{u}} = {vt(u)}$ und $\\mathbf{{v}} = {vt(v)}$ als Kreuzprodukt $\\mathbf{{u}} \\times \\mathbf{{v}}$.",
            "loesung": n,
            "tipps": ["Benutze die Formel aus Def. 4.18, Komponente für Komponente.", "Die Indizes laufen zyklisch: $(2, 3)$, $(3, 1)$, $(1, 2)$.",
                      "Mache die Probe: $(\\mathbf{u} \\times \\mathbf{v} \\mid \\mathbf{u})$ muss $0$ sein."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Das Kreuzprodukt steht senkrecht auf beiden Faktoren (Satz 4.19), ist also ein Normalenvektor der Ebene.",
            "typische_fehler": ohne_gleiche(n, fehler)}


_PYTH = [[1, 2, 2], [2, -2, 1], [2, 3, 6], [1, 4, 8], [4, 4, 7], [2, 6, 9], [3, 4, 0], [0, 5, 12], [1, 1, 1, 1], [2, 2, 2, 2], [1, 2, 2, 4], [3, 4], [5, 12], [6, 8]]


def abstand_hyperebene(rng):
    """Satz 4.15 mit ganzzahliger Länge von a."""
    a = list(rng.choice(_PYTH))
    rng.shuffle(a)
    a = [c * rng.choice([-1, 1]) for c in a]
    n = len(a)
    lq = norm_quadrat(a)
    l = int(round(float(lq) ** 0.5))
    assert l * l == lq
    while True:
        b = rng.randint(-5, 5)
        x = [rng.randint(-4, 4) for _ in range(n)]
        z = sp(x, a) - b
        if z != 0:
            break
    loes = F(abs(z), l)
    fehler = [(F(abs(z)), "Du hast nicht durch $\\lVert\\mathbf{a}\\rVert$ geteilt. Der Zähler allein ist nur der „Gleichungsfehler“."),
              (F(abs(z), lq), "Du hast durch $\\lVert\\mathbf{a}\\rVert^2$ geteilt. Im Nenner steht die Länge $\\lVert\\mathbf{a}\\rVert$."),
              (F(abs(sp(x, a) + b), l), "Du hast $b$ addiert. Es heißt $(\\mathbf{x} \\mid \\mathbf{a}) - b$.")]
    if z < 0:
        fehler.append((F(z, l), "Der Abstand ist nie negativ: Betrag nehmen."))
    ax = "(" + ", ".join(str(c) for c in a) + ")^\\top"
    xs = "(" + ", ".join(str(c) for c in x) + ")^\\top"
    zeilen = [(" + ".join(f"{tx(x[i])} \\cdot {tx(a[i])}" for i in range(n)) + f" = {tx(sp(x, a))}", "$(\\mathbf{x} \\mid \\mathbf{a})$"),
              ("\\sqrt{" + " + ".join(f"({a[i]})^2" for i in range(n)) + f"}} = {l}", "$\\lVert\\mathbf{a}\\rVert$"),
              (f"\\frac{{|{tx(sp(x, a))} - ({b})|}}{{{l}}} = {tx(loes)}", "Satz 4.15")]
    return {"frage": f"Berechne den Abstand von $\\mathbf{{x}} = {xs}$ zur Hyperebene $H = \\{{\\mathbf{{y}} \\in \\mathbb{{R}}^{{{n}}} \\mid (\\mathbf{{y}} \\mid \\mathbf{{a}}) = {b}\\}}$ mit $\\mathbf{{a}} = {ax}$.",
            "loesung": loes, "gekuerzt": True,
            "tipps": ["Satz 4.15: $|(\\mathbf{x} \\mid \\mathbf{a}) - b| / \\lVert\\mathbf{a}\\rVert$.", f"$\\lVert\\mathbf{{a}}\\rVert = {l}$.", f"$(\\mathbf{{x}} \\mid \\mathbf{{a}}) = {sp(x, a)}$."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Einsetzen in die Hyperebenengleichung liefert $(\\mathbf{x} \\mid \\mathbf{a}) - b$. Geteilt durch $\\lVert\\mathbf{a}\\rVert$ ist das der kürzeste Abstand (Satz 4.15).",
            "typische_fehler": ohne_gleiche(loes, fehler)}


def spatvolumen(rng):
    """Beobachtung 4.21: |(u × v | w)|."""
    while True:
        u, v, w = _rv(rng, -2, 2), _rv(rng, -2, 2), _rv(rng, -2, 2)
        n = kp(u, v)
        s = sp(n, w)
        if s != 0 and any(c != 0 for c in n):
            break
    loes = abs(s)
    fehler = []
    if s < 0:
        fehler.append((s, "Das Volumen ist nie negativ: Setze den Betrag $|(\\mathbf{u} \\times \\mathbf{v} \\mid \\mathbf{w})|$."))
    fehler.append((F(loes, 6), "Durch $6$ teilt man beim Tetraeder (Pyramide mit Dreiecksboden). Der Spat hat das volle Volumen $|(\\mathbf{u} \\times \\mathbf{v} \\mid \\mathbf{w})|$."))
    fehler.append((abs(sum(n)), "Du hast nur die Komponenten von $\\mathbf{u} \\times \\mathbf{v}$ addiert. Es fehlt das Skalarprodukt mit $\\mathbf{w}$."))
    zeilen = [(f"\\text{{u × v = }} {tx(n[0])},\\ {tx(n[1])},\\ {tx(n[2])}", "Kreuzprodukt der ersten beiden Kanten"),
              (f"{tx(n[0])} \\cdot {tx(w[0])} + {tx(n[1])} \\cdot {tx(w[1])} + {tx(n[2])} \\cdot {tx(w[2])} = {tx(s)}", "Skalarprodukt mit $\\mathbf{w}$"),
              (f"|{tx(s)}| = {tx(loes)}", "Betrag")]
    return {"frage": f"Berechne das Volumen des Spats mit den Kanten $\\mathbf{{u}} = {vt(u)}$, $\\mathbf{{v}} = {vt(v)}$, $\\mathbf{{w}} = {vt(w)}$.",
            "loesung": loes,
            "tipps": ["Beob. 4.21: Volumen $= |(\\mathbf{u} \\times \\mathbf{v} \\mid \\mathbf{w})|$.", f"Zuerst $\\mathbf{{u}} \\times \\mathbf{{v}} = {vt(n)}$.", "Dann das Skalarprodukt mit $\\mathbf{w}$ und der Betrag."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Grundfläche $\\lVert\\mathbf{u} \\times \\mathbf{v}\\rVert$ mal Höhe $|(\\mathbf{w} \\mid \\mathbf{e})|$ ergibt $|(\\mathbf{u} \\times \\mathbf{v} \\mid \\mathbf{w})|$.",
            "typische_fehler": ohne_gleiche(loes, fehler)}


def orthogonal_parameter(rng):
    """Skalarprodukt Null setzen (Def. 4.11)."""
    while True:
        a, b, c = rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-3, 3)
        d, e = rng.randint(-3, 3), rng.randint(-3, 3)
        if c != 0 and (a * d + b * e) != 0:
            break
    t = F(-(a * d + b * e), c)
    fehler = [(F(a * d + b * e, c), "Das Vorzeichen fehlt: $c\\,t = -(ad + be)$."),
              (F(-(a * d + b * e)), "Du hast nicht durch $c$ geteilt: $c \\cdot t = -(ad + be)$.")]
    return {"frage": f"Bestimme $t \\in \\mathbb{{R}}$ so, dass $\\mathbf{{x}} = ({a}, {b}, {c})^\\top$ und $\\mathbf{{y}} = ({d}, {e}, t)^\\top$ orthogonal sind.",
            "loesung": t, "gekuerzt": True,
            "tipps": ["Orthogonal heißt $(\\mathbf{x} \\mid \\mathbf{y}) = 0$.", f"$(\\mathbf{{x}} \\mid \\mathbf{{y}}) = {a} \\cdot {tx(d)} + {b} \\cdot {tx(e)} + {c} \\cdot t$.", "Löse die lineare Gleichung nach $t$."],
            "rechenweg": rechnung([(f"{a} \\cdot {tx(d)} + {b} \\cdot {tx(e)} + {c} t = 0", "Skalarprodukt Null setzen"),
                                   (f"{c} t = {-(a * d + b * e)}", "Zahlen nach rechts"), (f"t = {tx(t)}", f"durch ${c}$ teilen")]),
            "erklaerung": "Das Skalarprodukt ist linear in $t$; die Gleichung $(\\mathbf{x} \\mid \\mathbf{y}) = 0$ hat genau eine Lösung, wenn $c \\neq 0$.",
            "typische_fehler": ohne_gleiche(t, fehler)}


k.praxis()

k.zahl("Berechne den Flächeninhalt des von $\\mathbf{u} = (4, 1)^\\top$ und $\\mathbf{v} = (2, 3)^\\top$ aufgespannten Parallelogramms.",
       abs(4 * 3 - 1 * 2),
       "Im $\\mathbb{R}^2$ ist die Fläche $|u_1 v_2 - u_2 v_1| = |4 \\cdot 3 - 1 \\cdot 2| = 10$.",
       tipps=["Beob. 4.20: $|u_1 v_2 - u_2 v_1|$.", "$4 \\cdot 3 = 12$ und $1 \\cdot 2 = 2$.", "Differenz bilden, Betrag nehmen."],
       rechenweg=rechnung([("4 \\cdot 3 - 1 \\cdot 2 = 10", "Formel für die Fläche")]),
       typische_fehler=[(14, "Du hast $u_1 v_2 + u_2 v_1$ gerechnet. Die Fläche ist die **Differenz** der Kreuzprodukte."),
                        (F(5), "Du hast $\\frac12$ der Fläche gerechnet (Dreieck). Gefragt ist das Parallelogramm.")])

k.zahl("Berechne das Volumen des Spats mit den Kanten $\\mathbf{u} = (1, 0, 0)^\\top$, $\\mathbf{v} = (1, 2, 0)^\\top$, $\\mathbf{w} = (3, 1, 4)^\\top$.",
       abs(sp(kp([1, 0, 0], [1, 2, 0]), [3, 1, 4])),
       "$\\mathbf{u} \\times \\mathbf{v} = (0, 0, 2)^\\top$, also $|(\\mathbf{u} \\times \\mathbf{v} \\mid \\mathbf{w})| = |0 + 0 + 8| = 8$ (Grundfläche $2$, Höhe $4$).",
       tipps=["Beob. 4.21: $|(\\mathbf{u} \\times \\mathbf{v} \\mid \\mathbf{w})|$.", "Zuerst $\\mathbf{u} \\times \\mathbf{v}$.", "$\\mathbf{u} \\times \\mathbf{v} = (0, 0, 2)^\\top$."],
       rechenweg=rechnung([("0 \\cdot 0 - 0 \\cdot 2 = 0", "erste Komponente von $\\mathbf{u} \\times \\mathbf{v}$"), ("0 \\cdot 1 - 1 \\cdot 0 = 0", "zweite Komponente"),
                           ("1 \\cdot 2 - 0 \\cdot 1 = 2", "dritte Komponente: $(0, 0, 2)^\\top$"), ("0 \\cdot 3 + 0 \\cdot 1 + 2 \\cdot 4 = 8", "Skalarprodukt mit $\\mathbf{w}$")]),
       typische_fehler=[(2, "Das ist nur die Grundfläche $\\lVert\\mathbf{u} \\times \\mathbf{v}\\rVert$. Mit der Höhe $4$ ergibt sich das Volumen."),
                        (F(8, 3), "Spat ist kein Tetraeder: Es gibt keinen Faktor $\\frac13$.")])

k.generator(schnitt_gerade_ebene, typ="vektor", titel="Schnittpunkt von Gerade und Ebene")
k.generator(kreuzprodukt_normale, typ="vektor", titel="Normalenvektor mit dem Kreuzprodukt")
k.generator(abstand_hyperebene, typ="zahl", titel="Abstand Punkt–Hyperebene (Satz 4.15)")
k.generator(spatvolumen, typ="zahl", titel="Spatvolumen")
k.generator(orthogonal_parameter, typ="zahl", titel="Orthogonalität: Parameter bestimmen")

_PU, _PV, _PP, _PZ = [1, 0, 2], [1, 1, 0], [0, 1, 1], [3, 1, 2]
_PN = kp(_PU, _PV)
_PB = sp(_PP, _PN)
_PL = int(round(float(norm_quadrat(_PN)) ** 0.5))
assert _PN == [-2, 2, 1] and _PB == 3 and _PL == 3
assert F(abs(sp(_PZ, _PN) - _PB), _PL) == F(5, 3)

k.rechenweg_aufgabe(r"""
## Übungsblatt-Stil: Ebene, Normalenvektor, Abstand

Gegeben ist die Ebene $E = \{(0, 1, 1)^\top + s(1, 0, 2)^\top + t(1, 1, 0)^\top \mid s, t \in \mathbb{R}\}$ im $\mathbb{R}^3$.
Bestimmen Sie einen Normalenvektor, eine Gleichung der Form $(\mathbf{x} \mid \mathbf{n}) = b$ und den Abstand von $\mathbf{z} = (3, 1, 2)^\top$ zu $E$.
""",
    [{"typ": "vektor", "frage": "Schritt 1: Berechne $\\mathbf{n} = \\mathbf{u} \\times \\mathbf{v}$ mit $\\mathbf{u} = (1, 0, 2)^\\top$, $\\mathbf{v} = (1, 1, 0)^\\top$.",
      "loesung": _PN,
      "tipps": ["Def. 4.18, Komponente für Komponente.", "Erste Komponente: $0 \\cdot 0 - 2 \\cdot 1$."],
      "rechenweg": rechnung([("0 \\cdot 0 - 2 \\cdot 1 = -2", "erste Komponente"), ("2 \\cdot 1 - 1 \\cdot 0 = 2", "zweite Komponente"), ("1 \\cdot 1 - 0 \\cdot 1 = 1", "dritte Komponente")]),
      "typische_fehler": [([-c for c in _PN], "Das ist $\\mathbf{v} \\times \\mathbf{u}$: Reihenfolge beachten.")]},
     {"typ": "zahl", "frage": "Schritt 2: Bestimme $b = (\\mathbf{p} \\mid \\mathbf{n})$ mit $\\mathbf{p} = (0, 1, 1)^\\top$.", "loesung": _PB,
      "tipps": ["Jeder Punkt der Ebene erfüllt $(\\mathbf{x} \\mid \\mathbf{n}) = (\\mathbf{p} \\mid \\mathbf{n})$.", "$0 \\cdot (-2) + 1 \\cdot 2 + 1 \\cdot 1$."],
      "rechenweg": rechnung([("0 \\cdot (-2) + 1 \\cdot 2 + 1 \\cdot 1 = 3", "Skalarprodukt mit $\\mathbf{n}$")])},
     {"typ": "zahl", "frage": "Schritt 3: Berechne den Abstand von $\\mathbf{z} = (3, 1, 2)^\\top$ zu $E$ mit Satz 4.15.", "loesung": F(5, 3), "gekuerzt": True,
      "tipps": ["$|(\\mathbf{z} \\mid \\mathbf{n}) - b| / \\lVert\\mathbf{n}\\rVert$.", "$\\lVert\\mathbf{n}\\rVert = 3$."],
      "rechenweg": rechnung([("3 \\cdot (-2) + 1 \\cdot 2 + 2 \\cdot 1 = -2", "$(\\mathbf{z} \\mid \\mathbf{n})$"), ("\\sqrt{4 + 4 + 1} = 3", "$\\lVert\\mathbf{n}\\rVert$"),
                             ("\\frac{|-2 - 3|}{3} = \\frac{5}{3}", "Satz 4.15")]),
      "typische_fehler": [(5, "Du hast nicht durch $\\lVert\\mathbf{n}\\rVert = 3$ geteilt."), (F(1, 3), "Du hast $(\\mathbf{z} \\mid \\mathbf{n}) + b$ gerechnet. Es heißt $(\\mathbf{z} \\mid \\mathbf{n}) - b = -2 - 3 = -5$.")]}],
    "Der Normalenvektor steht senkrecht auf beiden Richtungsvektoren, $b$ ergibt sich aus dem Stützvektor, der Abstand aus Satz 4.15.",
    uebungsblatt=True,
    tipps=["Normalenvektor: Kreuzprodukt der Richtungsvektoren.", "Ebenengleichung: $b = (\\mathbf{p} \\mid \\mathbf{n})$."],
    rechenweg=r"""
:::rechnung
0 \cdot 0 - 2 \cdot 1 = -2 || erste Komponente von $\mathbf{u} \times \mathbf{v}$
0 \cdot (-2) + 1 \cdot 2 + 1 \cdot 1 = 3 || $b$
\frac{|-2 - 3|}{3} = \frac{5}{3} || Abstand nach Satz 4.15
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Beobachtung 4.10 und Orthogonalität

1. Zeigen Sie für $\mathbf{x}, \mathbf{y} \in \mathbb{R}^n$: $\lVert\mathbf{x} - \mathbf{y}\rVert^2 = \lVert\mathbf{x}\rVert^2 - 2(\mathbf{x} \mid \mathbf{y}) + \lVert\mathbf{y}\rVert^2$.
2. Folgern Sie: Sind $\mathbf{x} \perp \mathbf{y}$, so gilt $\lVert\mathbf{x} + \mathbf{y}\rVert^2 = \lVert\mathbf{x}\rVert^2 + \lVert\mathbf{y}\rVert^2$ (Pythagoras).
3. Sei $H = \{\mathbf{x} \in \mathbb{R}^n \mid (\mathbf{x} \mid \mathbf{a}) = b\}$ und $\mathbf{x}, \mathbf{y} \in H$. Zeigen Sie $(\mathbf{x} - \mathbf{y} \mid \mathbf{a}) = 0$.
""",
    r"""
**1.** $\lVert\mathbf{x} - \mathbf{y}\rVert^2 = (\mathbf{x} - \mathbf{y} \mid \mathbf{x} - \mathbf{y}) = (\mathbf{x} \mid \mathbf{x} - \mathbf{y}) - (\mathbf{y} \mid \mathbf{x} - \mathbf{y})
= (\mathbf{x} \mid \mathbf{x}) - (\mathbf{x} \mid \mathbf{y}) - (\mathbf{y} \mid \mathbf{x}) + (\mathbf{y} \mid \mathbf{y}) = \lVert\mathbf{x}\rVert^2 - 2(\mathbf{x} \mid \mathbf{y}) + \lVert\mathbf{y}\rVert^2$ (Linearität, Symmetrie).

**2.** Wie in 1 mit $+$: $\lVert\mathbf{x} + \mathbf{y}\rVert^2 = \lVert\mathbf{x}\rVert^2 + 2(\mathbf{x} \mid \mathbf{y}) + \lVert\mathbf{y}\rVert^2$. Wegen $(\mathbf{x} \mid \mathbf{y}) = 0$ fällt der mittlere Term weg.

**3.** $(\mathbf{x} - \mathbf{y} \mid \mathbf{a}) = (\mathbf{x} \mid \mathbf{a}) - (\mathbf{y} \mid \mathbf{a}) = b - b = 0$. Der Normalenvektor steht also senkrecht auf jedem Verbindungsvektor zweier Punkte von $H$. $\square$
""",
    ["In 1 die Linearität in beiden Argumenten benutzt",
     "In 1 die Symmetrie $(\\mathbf{x} \\mid \\mathbf{y}) = (\\mathbf{y} \\mid \\mathbf{x})$ zum Zusammenfassen benutzt",
     "In 2 den Term $2(\\mathbf{x} \\mid \\mathbf{y})$ wegen Orthogonalität gestrichen",
     "In 3 beide Punkte in die Hyperebenengleichung eingesetzt"],
    "Skalarprodukt ist bilinear und symmetrisch: Beide Regeln braucht man, um wie bei den binomischen Formeln auszumultiplizieren.",
    uebungsblatt=True,
    tipps=["Multipliziere $(\\mathbf{x} - \\mathbf{y} \\mid \\mathbf{x} - \\mathbf{y})$ wie eine binomische Formel aus."])

k.papier(r"""
## Beweisaufgabe: Beobachtung 4.20 (Parallelogrammfläche)

Seien $\mathbf{u}, \mathbf{v} \in \mathbb{R}^3$, $\mathbf{u} \neq \mathbf{0}$. Schreibe $\mathbf{u} = a\mathbf{e}$ mit $a = \lVert\mathbf{u}\rVert$, $\lVert\mathbf{e}\rVert = 1$ und
$\mathbf{v} = b\mathbf{e} + \mathbf{w}$ mit $b = (\mathbf{v} \mid \mathbf{e})$, $\mathbf{w} = \mathbf{v} - b\mathbf{e}$. Zeige $\lVert\mathbf{u} \times \mathbf{v}\rVert = a\,\lVert\mathbf{w}\rVert$
und erkläre, warum das „Grundseite mal Höhe“ ist. (Benutze $\lVert\mathbf{e} \times \mathbf{w}\rVert^2 = \lVert\mathbf{e}\rVert^2\lVert\mathbf{w}\rVert^2 - (\mathbf{e} \mid \mathbf{w})^2$.)
""",
    r"""
Es gilt $(\mathbf{w} \mid \mathbf{e}) = (\mathbf{v} \mid \mathbf{e}) - b(\mathbf{e} \mid \mathbf{e}) = b - b = 0$. Das Kreuzprodukt ist bilinear und $\mathbf{e} \times \mathbf{e} = \mathbf{0}$, also
$\mathbf{u} \times \mathbf{v} = a\mathbf{e} \times (b\mathbf{e} + \mathbf{w}) = a\,(\mathbf{e} \times \mathbf{w})$. Mit der angegebenen Identität
$\lVert\mathbf{e} \times \mathbf{w}\rVert^2 = 1 \cdot \lVert\mathbf{w}\rVert^2 - 0 = \lVert\mathbf{w}\rVert^2$. Somit $\lVert\mathbf{u} \times \mathbf{v}\rVert = a\,\lVert\mathbf{w}\rVert$.
Hier ist $a = \lVert\mathbf{u}\rVert$ die Länge der Grundseite und $\lVert\mathbf{w}\rVert$ die Höhe: $\mathbf{w}$ ist der zu $\mathbf{u}$ senkrechte Anteil von $\mathbf{v}$. $\square$
""",
    ["$(\\mathbf{w} \\mid \\mathbf{e}) = 0$ nachgerechnet",
     "$\\mathbf{u} \\times \\mathbf{v} = a(\\mathbf{e} \\times \\mathbf{w})$ mit Bilinearität und $\\mathbf{e} \\times \\mathbf{e} = \\mathbf{0}$ begründet",
     "Die Identität für $\\lVert\\mathbf{e} \\times \\mathbf{w}\\rVert^2$ eingesetzt und die Wurzel gezogen",
     "Die geometrische Deutung als Grundseite mal Höhe angegeben"],
    "Zerlegung von $\\mathbf{v}$ in einen Anteil entlang $\\mathbf{u}$ und einen senkrechten Rest ist die Grundidee. Sie kehrt in Kapitel 24 als Orthogonalprojektion wieder.",
    tipps=["Zeige zuerst $\\mathbf{w} \\perp \\mathbf{e}$.", "Das Kreuzprodukt ist linear in jedem Argument (aus der Definition)."])

k.mc("Ein linearer Klassifikator trennt Datenpunkte $\\mathbf{x} \\in \\mathbb{R}^{100}$ durch $(\\mathbf{n} \\mid \\mathbf{x}) = b$. Wie nennt man diese Menge, und welche Dimension hat sie?",
     ["Hyperebene der Dimension $99$", "Ebene der Dimension $2$", "Gerade der Dimension $1$", "Hyperebene der Dimension $100$"],
     "Nach Def. 4.14 ist $H = \\{\\mathbf{x} \\mid (\\mathbf{x} \\mid \\mathbf{n}) = b\\}$ eine Hyperebene; ihre Dimension ist $n - 1 = 99$ (Satz 4.114 in Kap. 24, Anschauung: $99$ frei wählbare Koordinaten).",
     uebungsblatt=True,
     tipps=["Eine Gleichung nimmt dem Raum einen Freiheitsgrad.", "$n - 1$."],
     fehler={"Ebene der Dimension $2$": "Eine Ebene im Sinne von Def. 4.5 hat nur zwei Parameter, eine Hyperebene im $\\mathbb{R}^{100}$ dagegen $99$.",
             "Hyperebene der Dimension $100$": "Die Gleichung $(\\mathbf{x} \\mid \\mathbf{n}) = b$ legt eine Koordinate fest: $100 - 1 = 99$ bleiben frei."})

k.zusammenfassung(r"""
## Geometrie des ℝⁿ (Skript Abschn. 4.1, Def. 4.1 bis Beispiel 4.22)

- **Vektor** $\mathbf{x} = (x_1, \ldots, x_n)^\top$; $+$ und $\lambda\cdot$ komponentenweise (Def. 4.1, 4.2); $\mathbb{R}^n$ ist abelsche Gruppe (Beob. 4.3); $\mathbf{x} = \sum x_j \mathbf{e}^{(j)}$ (Def. 4.4).
- **Gerade** $\{\mathbf{p} + t\mathbf{u}\}$ mit $\mathbf{u} \neq \mathbf{0}$, **Ebene** $\{\mathbf{p} + s\mathbf{u} + t\mathbf{v}\}$ mit $\mathbf{v} \neq \lambda\mathbf{u}$ (Def. 4.5). Durch zwei Punkte genau eine Gerade, durch drei Punkte (nicht auf einer Geraden) genau eine Ebene (Satz 4.6).
- **Schnitt Gerade/Ebene:** Komponenten gleichsetzen, Gleichungssystem für die Parameter lösen (Bsp. 4.7).
- $(\mathbf{x} \mid \mathbf{y}) = \sum x_j y_j$, $\lVert\mathbf{x}\rVert = \sqrt{(\mathbf{x} \mid \mathbf{x})}$, Abstand $\lVert\mathbf{x} - \mathbf{y}\rVert$ (Def. 4.9); $\lVert\mathbf{x} - \mathbf{y}\rVert^2 = \lVert\mathbf{x}\rVert^2 - 2(\mathbf{x} \mid \mathbf{y}) + \lVert\mathbf{y}\rVert^2$ (Beob. 4.10).
- **Orthogonal:** $(\mathbf{x} \mid \mathbf{y}) = 0$ (Def. 4.11). **Hyperebene** $\{\mathbf{x} \mid (\mathbf{x} \mid \mathbf{a}) = b\}$, Normalenvektor $\mathbf{a}$ (Def. 4.14).
- **Abstand** (Satz 4.15): $\min\{\lVert\mathbf{x} - \mathbf{p}\rVert \mid \mathbf{p} \in H\} = |(\mathbf{x} \mid \mathbf{a}) - b| / \lVert\mathbf{a}\rVert$.
- **Kreuzprodukt** $\mathbf{x} \times \mathbf{y}$ (Def. 4.18): senkrecht auf beiden, $\mathbf{y} \times \mathbf{x} = -\mathbf{x} \times \mathbf{y}$, $= \mathbf{0}$ genau bei Parallelität (Satz 4.19).
- **Fläche** $\lVert\mathbf{u} \times \mathbf{v}\rVert$ bzw. $|u_1 v_2 - u_2 v_1|$ (Beob. 4.20); **Spatvolumen** $|(\mathbf{u} \times \mathbf{v} \mid \mathbf{w})|$ (Beob. 4.21).

!! Skalarprodukt: Zahl. Kreuzprodukt: Vektor (nur im $\mathbb{R}^3$). Abstand immer mit $\lVert\mathbf{a}\rVert$ im Nenner.
""")
