# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 26: Matrizen und Rechnen mit Matrizen (Skript Disser WS 26/27, Abschn. 5.3 und 5.4, Bsp. 5.27 bis Beob. 5.58)."""
import re
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche
from .glossar import finden

k = neues_kapitel(
    slug="matrizen_uni",
    titel="Matrizen und Rechnen mit Matrizen",
    beschreibung="Matrix als Tabelle der Basisbilder, Matrix-Vektor-Produkt, Darstellungsmatrix, Matrixprodukt als Verkettung, Rechenregeln, Nullteiler, Transponierte",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 5.3 und 5.4",
    icon="🧮")


# ── Hilfsfunktionen ─────────────────────────────────────────────────────────
def G(text):
    """<<Anzeige|Begriff>> wird zum Glossar-Link, falls der Begriff schon im Glossar steht (Kapitel 4 entsteht parallel)."""
    def ers(m):
        inhalt = m.group(1)
        anzeige, _, name = inhalt.rpartition("|")
        if finden(name.strip()):
            return f"[[{inhalt}]]"
        return anzeige or name
    return re.sub(r"<<(.+?)>>", ers, text)


def vt(v):
    return mathlib.tex_vektor(v)


def M(m):
    return mathlib.tex_matrix(m)


def R(zeilen, titel="", frei=False):
    p = "?? " if frei else ""
    kopf = ":::rechnung" + (f" {titel}" if titel else "")
    return kopf + "\n" + "\n".join(f"{p}{t} || {g}" for t, g in zeilen) + "\n:::"


def ints(m):
    """Fraction-Matrix/-Vektor mit ganzen Werten -> int."""
    if m and isinstance(m[0], (list, tuple)):
        return [[int(x) if F(x).denominator == 1 else F(x) for x in z] for z in m]
    return [int(x) if F(x).denominator == 1 else F(x) for x in m]


def ohne_gleiche_m(loesung, fehler):
    """Wie ohne_gleiche, aber für Matrizen (Listen von Zeilen): streicht Fehlwerte, die der Lösung oder einem früheren Fehlwert gleichen."""
    gesehen = [[[F(x) for x in z] for z in loesung]]
    erg = []
    for w, m in fehler:
        wm = [[F(x) for x in z] for z in w]
        if wm in gesehen:
            continue
        gesehen.append(wm)
        erg.append((w, m))
    return erg


mul, mv, tr = mathlib.mat_mul, mathlib.mat_vec, mathlib.transponiert

# ── Nachgerechnet beim Laden ───────────────────────────────────────────────
_A27 = [[1, 1, 0], [0, 0, 1]]
assert mv(_A27, [2, 3, 4]) == [5, 4] and mathlib.rang(_A27) == 2 and mathlib.kern(_A27) == [[-1, 1, 0]]
assert tr(_A27) == [[1, 0], [1, 0], [0, 1]]
_P = [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]
_C = [[1, 0], [0, -1]]
_R = [[0, 1], [1, 0]]
assert mul(_P, _C) == [[F(1, 2), F(-1, 2)], [F(1, 2), F(-1, 2)]] and mul(_C, _P) == [[F(1, 2), F(1, 2)], [F(-1, 2), F(-1, 2)]]
assert mul(_P, _P) == _P and mul(_C, _C) == [[1, 0], [0, 1]] and mul(_P, mathlib.mat_add(mathlib.einheitsmatrix(2), mathlib.skalar(-1, _P))) == [[0, 0], [0, 0]]
assert mathlib.mat_add(mathlib.einheitsmatrix(2), mathlib.skalar(-1, _P)) == [[F(1, 2), F(-1, 2)], [F(-1, 2), F(1, 2)]]
# Bsp. 5.36/5.41: T(f) = (a, a + b); f(0) = 2, f(1) = 5 -> a = 2, b = 3
_T = [[1, 0], [1, 1]]
assert mv(_T, [2, 3]) == [2, 5] and mathlib.inverse(_T) == [[1, 0], [-1, 1]]
# Bsp. 5.37: m_z mit z = a + bi
assert [[2, -3], [3, 2]] == [[2, -3], [3, 2]] and (2 + 3j) * (1 + 1j) == (2 - 3) + (3 + 2) * 1j and mv([[2, -3], [3, 2]], [1, 1]) == [-1, 5]
# Bsp. 5.55, 5.57
assert mv(tr([[1, 2]]), [3]) == [3, 6] and sum(x * y for x, y in zip([1, 2], [3, 4])) == 11 and mul([[1], [2]], [[3, 4]]) == [[3, 4], [6, 8]]
# Beob. 5.51: E11 E12 = E12, E12 E11 = O, E11 E22 = O
_E11, _E12, _E22 = [[1, 0], [0, 0]], [[0, 1], [0, 0]], [[0, 0], [0, 1]]
assert mul(_E11, _E12) == _E12 and mul(_E12, _E11) == [[0, 0], [0, 0]] and mul(_E11, _E22) == [[0, 0], [0, 0]]
# Beob. 5.58 an einem Beispiel
_A58, _B58 = [[1, 2], [3, 4]], [[0, 1], [1, 1]]
assert tr(mul(_A58, _B58)) == mul(tr(_B58), tr(_A58)) and mul(tr(_A58), tr(_B58)) != tr(mul(_A58, _B58))
# Matrixformate: (3 x 2)(2 x 4) = (3 x 4)
assert len(mul([[1, 2], [3, 4], [5, 6]], [[1, 2, 3, 4], [5, 6, 7, 8]])[0]) == 4
# Beispiel 5.27: Matrix aus Basisbildern von f(x, y, z) = (x + y, z)
assert [[mv(_A27, e)[i] for e in ([1, 0, 0], [0, 1, 0], [0, 0, 1])] for i in range(2)] == _A27

k.lernziele([
    "Ich kann das Matrix-Vektor-Produkt als Linearkombination der Spalten und als „Zeile mal Spalte“ berechnen (Def. 5.28, 5.29)",
    "Ich kann zu einer linearen Abbildung die Matrix aus den Basisbildern aufstellen und Kern und Rang daran ablesen (Satz 5.31, Beob. 5.33)",
    "Ich kann Darstellungsmatrizen bezüglich Basen bilden und damit Koordinaten umrechnen (Def. 5.38, Satz 5.40)",
    "Ich kann Matrizen addieren, multiplizieren und transponieren und weiß, warum das Produkt der Verkettung entspricht (Def. 5.42 bis 5.46, Satz 5.49, Def. 5.54)",
])

k.warum(r"""
Matrizen sind das Rechenformat der linearen Algebra: In der Computergrafik ist jede Drehung und Skalierung eine Matrix, jede Schicht eines
neuronalen Netzes ein Matrix-Vektor-Produkt, ein Suchmaschinen-Ranking eine Matrixpotenz. Das Produkt ist so definiert, dass es die
Hintereinanderausführung abbildet. Deshalb kommt es auf die Reihenfolge an, und der Rechenaufwand $\mathcal{O}(n^3)$ hat einen
anschaulichen Grund: $n^2$ Einträge, jeder eine Summe aus $n$ Produkten.
""")

# ── Seite 1: Matrix und Matrix-Vektor-Produkt ───────────────────────────────
k.erklaerung("Matrix und Matrix-Vektor-Produkt (Bsp. 5.27, Def. 5.28, 5.29)", G(r"""
## Die Spalten sind die Bilder

:::analogie 🧪 Mischkarte
Jede Spalte der Karte sagt, was aus einer Grundzutat entsteht. Mischt du $x$ Teile der ersten, $y$ der zweiten und $z$ der dritten Zutat, mischst du die Spalten im selben Verhältnis.
:::

Für $f(x, y, z)^\top = (x + y,\ z)^\top$ sind die Bilder der Standardbasisvektoren $(1, 0)^\top$, $(1, 0)^\top$, $(0, 1)^\top$ (Bsp. 5.27).
Nebeneinander geschrieben ergibt das eine [[Matrix]] $A \in K^{m \times n}$ (Def. 5.28): $A_{ij}$ steht in Zeile $i$, Spalte $j$.

**Definition 5.29.** $Ax := \sum_{j=1}^n x_j A_{\cdot j}$, das [[Matrix-Vektor-Produkt]]. Komponentenweise: $(Ax)_i = \sum_j A_{ij} x_j$.

""") + R([
    (r"A = " + M(_A27) + r" \in \mathbb{R}^{2 \times 3}", "$2$ Zeilen, $3$ Spalten: Format $m \\times n$ mit $m = 2$, $n = 3$"),
    (r"A \begin{pmatrix}2\\3\\4\end{pmatrix} = 2\begin{pmatrix}1\\0\end{pmatrix} + 3\begin{pmatrix}1\\0\end{pmatrix} + 4\begin{pmatrix}0\\1\end{pmatrix}", "Spaltenkombination mit den Koeffizienten $x_j$"),
    (r"= \begin{pmatrix}2 + 3 + 0\\0 + 0 + 4\end{pmatrix} = \begin{pmatrix}5\\4\end{pmatrix}", "dasselbe als Zeile mal Spalte: $1 \\cdot 2 + 1 \\cdot 3 + 0 \\cdot 4$ und $0 \\cdot 2 + 0 \\cdot 3 + 1 \\cdot 4$"),
], "Matrix-Vektor-Produkt, zwei Sichtweisen", frei=True) + G(r"""

:::achtung Format zuerst prüfen
$A \in K^{m \times n}$ lässt sich nur mit $x \in K^n$ multiplizieren, das Ergebnis liegt in $K^m$. Auch $m = 0$ oder $n = 0$ ist erlaubt (Bem. 5.30): dann ist $Ax$ der Nullvektor bzw. das leere Tupel.
:::

:::alt Als Tabelle mit Warenkorb
Die Zeilen sind Läden, die Spalten Produkte, die Einträge die Preise. Dein Einkaufszettel $x$ sagt, wie viel von jedem Produkt. $Ax$ ist die Rechnung je Laden.
:::
"""))

k.vektor("Berechne $Ax$ für $A = \\begin{pmatrix}1 & 2\\\\ 3 & 4\\\\ 0 & 1\\end{pmatrix}$ und $x = \\begin{pmatrix}5\\\\ -1\\end{pmatrix}$.",
         ints(mv([[1, 2], [3, 4], [0, 1]], [5, -1])),
         "$Ax = 5 \\cdot (1, 3, 0)^\\top + (-1) \\cdot (2, 4, 1)^\\top = (5 - 2,\\ 15 - 4,\\ 0 - 1)^\\top = (3, 11, -1)^\\top$.",
         tipps=["Die erste Spalte wird mit $x_1 = 5$ multipliziert, die zweite mit $x_2 = -1$.", "Zeile für Zeile: erste Zeile $1 \\cdot 5 + 2 \\cdot (-1)$.", "Das Ergebnis hat drei Komponenten, weil $A$ drei Zeilen hat."],
         rechenweg=R([(r"Ax = 5\begin{pmatrix}1\\3\\0\end{pmatrix} + (-1)\begin{pmatrix}2\\4\\1\end{pmatrix}", "Def. 5.29"),
                      (r"= \begin{pmatrix}5 - 2\\15 - 4\\0 - 1\end{pmatrix} = \begin{pmatrix}3\\11\\-1\end{pmatrix}", "komponentenweise")], frei=True),
         typische_fehler=[(ints(mv([[1, 2], [3, 4], [0, 1]], [-1, 5])), "Du hast $x_1$ und $x_2$ vertauscht: Die erste Spalte gehört zu $x_1 = 5$."),
                          ([3, 11, 1], "Das Vorzeichen der letzten Komponente: $0 \\cdot 5 + 1 \\cdot (-1) = -1$.")])

k.zahl("Sei $A = \\begin{pmatrix}3 & 1 & 4\\\\ 1 & 5 & 9\\\\ 2 & 6 & 5\\end{pmatrix}$. Wie groß ist der Eintrag $A_{23}$?", 9,
       "$A_{ij}$ steht in Zeile $i$ und Spalte $j$. Also ist $A_{23}$ der Eintrag in Zeile $2$, Spalte $3$: die $9$.",
       tipps=["Eine Matrix ist eine Tabelle: Zeilen laufen waagerecht, Spalten senkrecht.", "Der erste Index ist die Zeile, der zweite die Spalte.", "Gehe zur zweiten Zeile und dort an die dritte Stelle."],
       rechenweg=R([(r"A_{2 \cdot} = (1, 5, 9)", "zweite Zeile"), (r"A_{23} = 9", "dritte Stelle dieser Zeile")], frei=True),
       typische_fehler=[(6, "Das ist $A_{32}$: Zeile und Spalte vertauscht."), (4, "Das ist $A_{13}$ (Zeile $1$, Spalte $3$). Der erste Index zählt die Zeile.")])

# ── Seite 2: Satz 5.31 ──────────────────────────────────────────────────────
k.erklaerung("Satz 5.31: Jede lineare Abbildung ist eine Matrix", G(r"""
## Matrix und Abbildung gehören zusammen

**Satz 5.31.** Jede Matrix $A \in K^{m \times n}$ definiert eine lineare Abbildung $f_A\colon K^n \to K^m,\ x \mapsto Ax$. Umgekehrt gibt es zu jeder linearen Abbildung
$f\colon K^n \to K^m$ **genau eine** Matrix $A$ mit $f = f_A$, nämlich
$$A = \big(f(e^{(1)}), \dots, f(e^{(n)})\big).$$

*Beweis.* Nach Satz 5.9 gibt es genau eine lineare Abbildung mit $e^{(j)} \mapsto A_{\cdot j}$, und nach Satz 5.8 gilt $f(x) = \sum x_j A_{\cdot j} = Ax$.

:::visual vektoren2d
{"vektoren": [{"x": 1, "y": 0, "label": "e_1"}, {"x": 0, "y": 1, "label": "e_2"}, {"x": 1, "y": 1, "label": "f(e_1)"}, {"x": -1, "y": 1, "label": "f(e_2)"}],
 "unterschrift": "$A = \\begin{pmatrix}1 & -1\\\\ 1 & 1\\end{pmatrix}$: Die Spalten sind die Bilder von $e_1$ und $e_2$ (Drehung um $45°$ mit Streckung $\\sqrt{2}$)."}
:::

""") + R([
    (r"\pi_G(e^{(1)}) = \pi_G(e^{(2)}) = \begin{pmatrix}1/2\\1/2\end{pmatrix}", "Projektion auf $G = \\langle (1, 1)^\\top \\rangle$ (Bsp. 5.35)"),
    (r"P = \begin{pmatrix}1/2 & 1/2\\1/2 & 1/2\end{pmatrix}", "Spalten nebeneinander"),
    (r"s_G(e^{(1)}) = e^{(2)},\ s_G(e^{(2)}) = e^{(1)} \Rightarrow R = \begin{pmatrix}0 & 1\\1 & 0\end{pmatrix}", "die Spiegelung vertauscht die Koordinaten"),
], "Zwei Matrizen aus Basisbildern", frei=True) + G(r"""

:::alt Als Gebrauchsanweisung
Eine lineare Abbildung ist vollständig beschrieben durch das, was sie mit den $n$ Grundrichtungen macht. Die Matrix ist diese Beschreibung in Tabellenform, nichts weiter.
:::
"""))

k.matrix("$f\\colon \\mathbb{R}^2 \\to \\mathbb{R}^2,\\ (x, y)^\\top \\mapsto (x + 2y,\\ 3x - y)^\\top$ ist linear. Bestimme die Matrix $A$ mit $f = f_A$.",
         [[1, 2], [3, -1]],
         "Spalten sind die Bilder der Standardbasisvektoren: $f(e^{(1)}) = f(1, 0) = (1, 3)^\\top$ und $f(e^{(2)}) = f(0, 1) = (2, -1)^\\top$.",
         tipps=["Setze $e^{(1)} = (1, 0)^\\top$ ein und schreibe das Ergebnis als **Spalte**.", "$f(1, 0) = (1 + 0,\\ 3 - 0) = (1, 3)$.", "Die zweite Spalte ist $f(0, 1) = (2, -1)$."],
         rechenweg=R([(r"f\begin{pmatrix}1\\0\end{pmatrix} = \begin{pmatrix}1\\3\end{pmatrix}", "erste Spalte"),
                      (r"f\begin{pmatrix}0\\1\end{pmatrix} = \begin{pmatrix}2\\-1\end{pmatrix}", "zweite Spalte"),
                      (r"A = \begin{pmatrix}1 & 2\\3 & -1\end{pmatrix}", "nebeneinander gestellt")], frei=True),
         typische_fehler=[([[1, 3], [2, -1]], "Du hast die Bilder als **Zeilen** statt als Spalten geschrieben. Das ist die Transponierte.")])

# ── Seite 3: Kern und Rang einer Matrix ─────────────────────────────────────
k.erklaerung("Kern und Rang einer Matrix (Def. 5.32, Beob. 5.33)", G(r"""
## Kern und Bild an den Spalten

**Definition 5.32.** $\ker A := \ker(f_A)$ und $\mathrm{rang}\, A := \mathrm{rang}(f_A)$.

**Beobachtung 5.33.** $\ker A = \{x \in K^n \mid Ax = 0\}$ und $f_A(K^n) = \langle A_{\cdot 1}, \dots, A_{\cdot n} \rangle$.
Also ist $\mathrm{rang}\, A = \dim \langle A_{\cdot 1}, \dots, A_{\cdot n} \rangle$: die Zahl linear unabhängiger Spalten.

""") + R([
    (r"A = " + M(_A27), "die Matrix aus Bsp. 5.27"),
    (r"A\begin{pmatrix}-1\\1\\0\end{pmatrix} = -\begin{pmatrix}1\\0\end{pmatrix} + \begin{pmatrix}1\\0\end{pmatrix} = 0", "die ersten beiden Spalten sind gleich: ein Kernvektor (Bsp. 5.34)"),
    (r"\mathrm{rang}\, A = \dim \left\langle \begin{pmatrix}1\\0\end{pmatrix}, \begin{pmatrix}0\\1\end{pmatrix} \right\rangle = 2", "erste und dritte Spalte bilden die Standardbasis des $\\mathbb{R}^2$"),
    (r"3 = 1 + 2", "Dimensionsformel: $n = \\dim\\ker A + \\mathrm{rang}\\, A$"),
], "Kern, Bild und Rang an Beispiel 5.34", frei=True) + G(r"""

:::alt Als Fotografie
Die Spalten sind die Bilder der Grundrichtungen. Zwei Spalten gleich: Zwei Richtungen landen am selben Ort, ihre Differenz ist unsichtbar (Kern). Das Bild ist alles, was sich aus den Spalten mischen lässt.
:::
"""))

_A33 = [[1, 2, 1], [0, 1, 1]]
k.vektor("Bestimme einen Vektor $\\neq 0$, der $\\ker A$ aufspannt, für $A = \\begin{pmatrix}1 & 2 & 1\\\\ 0 & 1 & 1\\end{pmatrix}$ (jedes Vielfache $\\neq 0$ gilt).",
         ints(mathlib.kern(_A33)[0]),
         "$Ax = 0$ heißt $x + 2y + z = 0$ und $y + z = 0$. Aus der zweiten Gleichung $y = -z$, eingesetzt $x = -2y - z = 2z - z = z$. Mit $z = 1$: $(1, -1, 1)^\\top$. Probe: $1 - 2 + 1 = 0$ und $-1 + 1 = 0$.",
         vielfaches=True,
         tipps=["Löse $Ax = 0$ als Gleichungssystem: eine Variable bleibt frei.", "Setze $z = t$, dann folgt $y = -t$ aus der zweiten Zeile.", "Setze $y$ und $z$ in die erste Zeile ein: $x = t$."],
         rechenweg=R([(r"y + z = 0 \Rightarrow y = -z", "zweite Zeile"), (r"x + 2y + z = 0 \Rightarrow x = -2y - z = z", "erste Zeile, $y = -z$ eingesetzt"),
                      (r"\ker A = \left\langle \begin{pmatrix}1\\-1\\1\end{pmatrix} \right\rangle", "mit $z = 1$; Dimension $3 - 2 = 1$")], frei=True),
         typische_fehler=[([1, 1, -1], "Setze in die zweite Zeile ein: $1 + (-1) = 0$ stimmt, aber in die erste: $1 + 2 - 1 = 2 \\neq 0$.")])

k.zahl("Welchen Rang hat $A = \\begin{pmatrix}1 & 2 & 3\\\\ 2 & 4 & 6\\\\ 1 & 1 & 1\\end{pmatrix}$?", mathlib.rang([[1, 2, 3], [2, 4, 6], [1, 1, 1]]),
       "Die zweite Zeile ist das Doppelte der ersten, die dritte Zeile nicht. Nach dem Gauß-Verfahren bleiben zwei Pivots: Rang $2$. Der Rang einer Matrix ist auch die Zahl linear unabhängiger Spalten, hier ebenfalls $2$.",
       tipps=["Der Rang ist die Dimension des Spaltenraums.", "Eine Zeile ist ein Vielfaches einer anderen.", "Zwei unabhängige Zeilen sind übrig."],
       rechenweg=R([(r"Z_2 \leftarrow Z_2 - 2Z_1 = (0, 0, 0)", "die zweite Zeile verschwindet"),
                    (r"Z_3 \leftarrow Z_3 - Z_1 = (0, -1, -2)", "die dritte bleibt"),
                    (r"\mathrm{rang}\, A = 2", "zwei von null verschiedene Zeilen")], frei=True),
       typische_fehler=[(3, "Eine $3 \\times 3$-Matrix hat nur dann Rang $3$, wenn alle Zeilen unabhängig sind. Hier ist $Z_2 = 2Z_1$."),
                        (1, "Zwei Zeilen sind unabhängig: $Z_1$ und $Z_3$ sind keine Vielfachen voneinander.")])

# ── Seite 4: Darstellungsmatrix ─────────────────────────────────────────────
k.erklaerung("Darstellungsmatrix (Bsp. 5.36, 5.37, Def. 5.38)", G(r"""
## Matrizen in beliebigen Basen

Auch in Räumen aus Funktionen oder komplexen Zahlen helfen Matrizen: Man rechnet mit den Koordinaten bezüglich <<geordneten Basen|Basis>>.

**Definition 5.38.** Für $f\colon V \to W$ linear und geordnete Basen $\mathfrak{B} = (b^{(1)}, \dots, b^{(n)})$ von $V$, $\mathfrak{C}$ von $W$ ist
$$[f]_{\mathfrak{C} \leftarrow \mathfrak{B}} := \big([f(b^{(1)})]_{\mathfrak{C}}, \dots, [f(b^{(n)})]_{\mathfrak{C}}\big)$$
die [[Darstellungsmatrix]]: Spalte $j$ sind die <<Koordinaten|Koordinatenvektor>> des Bildes von $b^{(j)}$.

""") + R([
    (r"T\colon \mathcal{F} \to \mathbb{R}^2,\ f \mapsto \begin{pmatrix}f(0)\\f(1)\end{pmatrix},\ \mathfrak{B} = (1, t)", "Auswertung bei $0$ und $1$ (Bsp. 5.36)"),
    (r"T(1) = \begin{pmatrix}1\\1\end{pmatrix},\ T(t) = \begin{pmatrix}0\\1\end{pmatrix} \Rightarrow [T]_{\mathcal{E} \leftarrow \mathfrak{B}} = \begin{pmatrix}1 & 0\\1 & 1\end{pmatrix}", "Bilder der Basisfunktionen als Spalten (Bsp. 5.39)"),
    (r"m_z(1) = a + bi,\ m_z(i) = -b + ai \Rightarrow [m_z]_{\mathfrak{B} \leftarrow \mathfrak{B}} = \begin{pmatrix}a & -b\\b & a\end{pmatrix}", "Multiplikation mit $z = a + bi$, Basis $(1, i)$ (Bsp. 5.37)"),
    (r"c(1) = 1,\ c(i) = -i \Rightarrow [c]_{\mathfrak{B} \leftarrow \mathfrak{B}} = \begin{pmatrix}1 & 0\\0 & -1\end{pmatrix}", "Konjugation"),
], "Drei Darstellungsmatrizen aus dem Skript", frei=True) + G(r"""

:::alt Als Übersetzer
Ohne Koordinaten gibt es nur „Funktion“ oder „komplexe Zahl“. Die Basis ist das Wörterbuch: Sie übersetzt jedes Objekt in eine Zahlenliste. Die Darstellungsmatrix ist dann die Übersetzung der Abbildung in dieselbe Zahlensprache.
:::
"""))

k.matrix("Sei $z = 2 + 3i \\in \\mathbb{C}$. Bestimme die Darstellungsmatrix von $m_z\\colon \\mathbb{C} \\to \\mathbb{C},\\ w \\mapsto zw$ bezüglich der Basis $\\mathfrak{B} = (1, i)$ in beiden Räumen (Bsp. 5.37).",
         [[2, -3], [3, 2]],
         "$m_z(1) = 2 + 3i$ hat Koordinaten $(2, 3)^\\top$ und $m_z(i) = 2i + 3i^2 = -3 + 2i$ hat Koordinaten $(-3, 2)^\\top$. Beide als Spalten.",
         tipps=["Berechne $m_z(1)$ und $m_z(i)$ und lies Real- und Imaginärteil ab.", "Real- und Imaginärteil sind die Koordinaten bezüglich $(1, i)$.", "$m_z(i) = -3 + 2i$ ergibt die zweite **Spalte** $(-3, 2)$."],
         rechenweg=R([(r"m_z(1) = 2 + 3i \Rightarrow [m_z(1)]_{\mathfrak{B}} = (2, 3)^\top", "erste Spalte"),
                      (r"m_z(i) = (2 + 3i)i = -3 + 2i \Rightarrow [m_z(i)]_{\mathfrak{B}} = (-3, 2)^\top", "zweite Spalte, $i^2 = -1$")], frei=True),
         typische_fehler=[([[2, 3], [-3, 2]], "Das ist die Transponierte: Die Koordinatenvektoren der Bilder gehören in die **Spalten**.")])

k.mc("Was steht in der $j$-ten Spalte der Darstellungsmatrix $[f]_{\\mathfrak{C} \\leftarrow \\mathfrak{B}}$?",
     ["Der Koordinatenvektor $[f(b^{(j)})]_{\\mathfrak{C}}$ des Bildes des $j$-ten Basisvektors von $\\mathfrak{B}$",
      "Der Koordinatenvektor $[b^{(j)}]_{\\mathfrak{B}}$ des $j$-ten Basisvektors von $\\mathfrak{B}$",
      "Der Koordinatenvektor $[f(c^{(j)})]_{\\mathfrak{B}}$ des Bildes des $j$-ten Basisvektors von $\\mathfrak{C}$",
      "Der Vektor $f(b^{(j)})$ in Standardkoordinaten"],
     "Definition 5.38: Die Spalten sind die Koordinaten der Bilder der Basisvektoren der Ausgangsbasis $\\mathfrak{B}$, gemessen in der Zielbasis $\\mathfrak{C}$.",
     tipps=["Satz 5.31 sagt für Standardbasen: Spalten sind die Bilder der Basisvektoren.", "In welcher Basis wird das Bild gemessen: Ausgangs- oder Zielbasis?"],
     fehler={"Der Koordinatenvektor $[b^{(j)}]_{\\mathfrak{B}}$ des $j$-ten Basisvektors von $\\mathfrak{B}$": "Das ergäbe immer den $j$-ten Standardbasisvektor, also die Einheitsmatrix: Das $f$ käme gar nicht vor.",
             "Der Koordinatenvektor $[f(c^{(j)})]_{\\mathfrak{B}}$ des Bildes des $j$-ten Basisvektors von $\\mathfrak{C}$": "Die Basisvektoren der Zielbasis liegen im Zielraum, dort wirkt $f$ nicht. Eingesetzt werden die Basisvektoren der **Ausgangs**basis $\\mathfrak{B}$.",
             "Der Vektor $f(b^{(j)})$ in Standardkoordinaten": "Gemessen wird in der Basis $\\mathfrak{C}$, nicht in Standardkoordinaten. Das ist nur dann dasselbe, wenn $\\mathfrak{C}$ die Standardbasis ist."})

# ── Seite 5: Satz 5.40 ──────────────────────────────────────────────────────
k.erklaerung("Satz 5.40: Die Matrix übersetzt Koordinaten", G(r"""
## Satz 5.40

**Satz 5.40.** Für $f\colon V \to W$ linear, geordnete Basen $\mathfrak{B}$ von $V$ und $\mathfrak{C}$ von $W$ und alle $v \in V$ gilt
$$[f(v)]_{\mathfrak{C}} = [f]_{\mathfrak{C} \leftarrow \mathfrak{B}} \cdot [v]_{\mathfrak{B}}.$$

Damit lässt sich $f(v) = y$ in Koordinaten lösen: $A[v]_{\mathfrak{B}} = [y]_{\mathfrak{C}}$ nach den Koordinaten von $v$ auflösen und daraus $v$ bilden.

""") + R([
    (r"A = [T]_{\mathcal{E} \leftarrow \mathfrak{B}} = \begin{pmatrix}1 & 0\\1 & 1\end{pmatrix},\ [y]_{\mathcal{E}} = \begin{pmatrix}2\\5\end{pmatrix}", "gesucht: $f(t) = a + bt$ mit $f(0) = 2$, $f(1) = 5$ (Bsp. 5.41)"),
    (r"\begin{pmatrix}1 & 0\\1 & 1\end{pmatrix}\begin{pmatrix}a\\b\end{pmatrix} = \begin{pmatrix}2\\5\end{pmatrix}", "$A[f]_{\\mathfrak{B}} = [y]_{\\mathcal{E}}$"),
    (r"a = 2,\ a + b = 5 \Rightarrow b = 3", "erste Zeile, dann zweite Zeile"),
    (r"f(t) = 2 + 3t", "aus den Koordinaten wieder die Funktion gebildet"),
], "Beispiel 5.41: Urbild über die Matrix", frei=True) + G(r"""

:::alt Als Zwei-Sprachen-Rechnung
Entweder rechnest du in der Sprache der Räume ($f(v)$), oder du übersetzt $v$ in Zahlen, multiplizierst mit der Matrix und übersetzt zurück. Satz 5.40 sagt: Beide Wege führen zum selben Ergebnis.
:::
"""))

k.ordnen("Ordne den Beweis von Satz 5.40.",
         ["Sei $A = [f]_{\\mathfrak{C} \\leftarrow \\mathfrak{B}}$ und $[v]_{\\mathfrak{B}} = (x_1, \\dots, x_n)^\\top$, also $v = \\sum_{j=1}^n x_j b^{(j)}$.",
          "Die $j$-te Spalte von $A$ ist $[f(b^{(j)})]_{\\mathfrak{C}}$, also $f(b^{(j)}) = \\sum_{i=1}^m A_{ij} c^{(i)}$.",
          "Mit Satz 5.8 folgt $f(v) = \\sum_j x_j f(b^{(j)}) = \\sum_j x_j \\sum_i A_{ij} c^{(i)}$.",
          "Wir vertauschen die Summen: $f(v) = \\sum_{i=1}^m \\big( \\sum_{j=1}^n A_{ij} x_j \\big) c^{(i)}$.",
          "Wegen der Eindeutigkeit der Basisdarstellung (Satz 4.55) ist die $i$-te Koordinate von $f(v)$ gleich $\\sum_j A_{ij} x_j$, das ist die $i$-te Komponente von $A[v]_{\\mathfrak{B}}$. $\\square$"],
         "Erst Koordinaten und Definition der Spalten, dann Linearität, dann Summen vertauschen, dann die Eindeutigkeit der Basisdarstellung.",
         ablenker=["Da $A$ invertierbar ist, genügt $[f(v)]_{\\mathfrak{C}} = A^{-1}[v]_{\\mathfrak{B}}$.", "Wir setzen $\\mathfrak{B} = \\mathfrak{C}$ voraus."],
         tipps=["Fange mit den Bezeichnungen an: Was sind $A$ und $x$?", "Die Linearität (Satz 5.8) wird gebraucht, um $f$ durch die Basisbilder auszudrücken.", "Invertierbarkeit und $\\mathfrak{B} = \\mathfrak{C}$ werden nirgends vorausgesetzt."])

k.vektor("Bestimme die Koordinaten $[f]_{\\mathfrak{B}} = (a, b)^\\top$ der Funktion $f(t) = a + bt$ mit $f(0) = 3$ und $f(1) = 7$, indem du $A[f]_{\\mathfrak{B}} = (3, 7)^\\top$ mit $A = \\begin{pmatrix}1 & 0\\\\ 1 & 1\\end{pmatrix}$ löst.",
         [3, 4],
         "Die erste Zeile gibt $a = 3$, die zweite $a + b = 7$, also $b = 4$. Die Funktion ist $f(t) = 3 + 4t$.",
         tipps=["Schreibe das System aus den beiden Zeilen von $A$ auf.", "Die erste Zeile lautet $1 \\cdot a + 0 \\cdot b = 3$.", "Setze $a = 3$ in $a + b = 7$ ein."],
         rechenweg=R([(r"a = 3", "erste Zeile"), (r"3 + b = 7 \Rightarrow b = 4", "zweite Zeile")], frei=True),
         typische_fehler=[([3, 7], "Das sind die Funktionswerte $f(0), f(1)$, nicht die Koordinaten. $b = f(1) - f(0)$.")])

# ── Seite 6: Addition und Skalar ────────────────────────────────────────────
k.erklaerung("Summe und Vielfache von Matrizen (Def. 5.42, Beob. 5.43)", G(r"""
## Spaltenweise addieren

**Definition 5.42.** Für $A, B \in K^{m \times n}$ und $\lambda \in K$ gilt $A + B := (A_{\cdot 1} + B_{\cdot 1}, \dots, A_{\cdot n} + B_{\cdot n})$ und $\lambda A := (\lambda A_{\cdot 1}, \dots)$, also $(A + B)_{ij} = A_{ij} + B_{ij}$ und $(\lambda A)_{ij} = \lambda A_{ij}$.

**Beobachtung 5.43.** $(K^{m \times n}, +, \cdot)$ ist ein Vektorraum der Dimension $mn$. Die Matrizen mit einer $1$ und sonst Nullen bilden eine Basis, der Nullvektor ist die [[Nullmatrix]] $O$.

""") + R([
    (r"\begin{pmatrix}1 & 2\\3 & 4\end{pmatrix} + \begin{pmatrix}0 & 1\\-1 & 2\end{pmatrix} = \begin{pmatrix}1 & 3\\2 & 6\end{pmatrix}", "Eintrag für Eintrag addieren"),
    (r"3 \begin{pmatrix}1 & 2\\3 & 4\end{pmatrix} = \begin{pmatrix}3 & 6\\9 & 12\end{pmatrix}", "jeden Eintrag mit $3$ multiplizieren"),
    (r"2 \cdot 3 = 6", "$\\dim K^{2 \\times 3} = 6$: sechs Basismatrizen $E_{ij}$ mit einer $1$ an Position $(i, j)$"),
], "Addieren und skalieren", frei=True) + G(r"""

:::alt Als Tabellenkalkulation
Zwei gleich große Tabellen addierst du zellenweise, eine Tabelle mit einer Zahl multiplizierst du zellenweise. Nur Tabellen gleichen Formats lassen sich addieren.
:::
"""))

k.zahl("Welche Dimension hat der Vektorraum $K^{3 \\times 4}$ der $(3 \\times 4)$-Matrizen (Beobachtung 5.43)?", 12,
       "Eine Matrix hat $3 \\cdot 4$ freie Einträge. Die zwölf Matrizen mit genau einer $1$ bilden eine Basis, also $\\dim = mn = 12$.",
       tipps=["Zähle die Einträge einer $3 \\times 4$-Matrix.", "Jeder Eintrag ist frei wählbar.", "$3 \\cdot 4$."],
       rechenweg=R([(r"\dim K^{3 \times 4} = 3 \cdot 4 = 12", "Beob. 5.43")]),
       typische_fehler=[(7, "Das wäre $m + n$. Jede Zeile hat $n$ Einträge, und es gibt $m$ Zeilen: $m \\cdot n$."), (4, "Das ist nur die Spaltenzahl.")])

# ── Seite 7: Matrixprodukt ──────────────────────────────────────────────────
k.erklaerung("Matrixprodukt und Einheitsmatrix (Def. 5.45, 5.46, Bsp. 5.44, 5.47)", G(r"""
## Erst $B$, dann $A$

Die [[Einheitsmatrix]] $\mathbb{I}_n$ gehört zur Identität. **Definition 5.46.** Für $A \in K^{m \times n}$, $B \in K^{n \times r}$ ist
$$AB := (AB_{\cdot 1}, \dots, AB_{\cdot r}) \in K^{m \times r}, \qquad (AB)_{ij} = \sum_{k=1}^n A_{ik} B_{kj}.$$
Das [[Matrixprodukt]] wendet $A$ auf jede Spalte von $B$ an: Zeile mal Spalte. Spaltenzahl von $A$ = Zeilenzahl von $B$. Außerdem $A^0 := \mathbb{I}_n$, $A^{k+1} := AA^k$.

:::visual matrix_mult
{"a": [["1/2", "1/2"], ["1/2", "1/2"]], "b": [[1, 0], [0, -1]],
 "unterschrift": "$PC$ aus Bsp. 5.44: erst spiegeln ($C$), dann auf $G$ projizieren ($P$). Eintrag $c_{ij}$ = Zeile $i$ von $P$ mal Spalte $j$ von $C$."}
:::

""") + R([
    (r"PC = \frac12\begin{pmatrix}1 & 1\\1 & 1\end{pmatrix}\begin{pmatrix}1 & 0\\0 & -1\end{pmatrix} = \frac12\begin{pmatrix}1 & -1\\1 & -1\end{pmatrix}", "erst $C$, dann $P$ (Bsp. 5.47)"),
    (r"CP = \frac12\begin{pmatrix}1 & 1\\-1 & -1\end{pmatrix} \neq PC", "andere Reihenfolge, anderes Ergebnis"),
    (r"P^2 = P,\ C^2 = \mathbb{I}_2", "zweimal projizieren ändert nichts, zweimal spiegeln bringt zurück"),
], "Beispiel 5.47", frei=True) + G(r"""

:::alt Als Fließband
$AB$ ist ein Fließband mit zwei Stationen. Die Station, die zuerst arbeitet, steht im Produkt **rechts**, genauso wie in $g(f(x))$. Das Band ist nur zusammenbaubar, wenn der Ausgang der ersten Station zum Eingang der zweiten passt.
:::
"""))

k.matrix("Berechne $AB$ für $A = \\begin{pmatrix}1 & 2\\\\ 0 & 1\\end{pmatrix}$ und $B = \\begin{pmatrix}3 & 0\\\\ 1 & 2\\end{pmatrix}$.",
         ints(mul([[1, 2], [0, 1]], [[3, 0], [1, 2]])),
         "Eintrag für Eintrag: Zeile $i$ von $A$ mal Spalte $j$ von $B$. $(AB)_{11} = 1 \\cdot 3 + 2 \\cdot 1 = 5$, $(AB)_{12} = 1 \\cdot 0 + 2 \\cdot 2 = 4$, $(AB)_{21} = 0 \\cdot 3 + 1 \\cdot 1 = 1$, $(AB)_{22} = 0 \\cdot 0 + 1 \\cdot 2 = 2$.",
         tipps=["Wende $A$ auf jede Spalte von $B$ an.", "Der Eintrag $(AB)_{11}$ ist Zeile $1$ von $A$ mal Spalte $1$ von $B$: $1 \\cdot 3 + 2 \\cdot 1$.", "Das Ergebnis hat Zeile $1$: $(5, 4)$."],
         rechenweg=R([(r"AB_{\cdot 1} = \begin{pmatrix}1 & 2\\0 & 1\end{pmatrix}\begin{pmatrix}3\\1\end{pmatrix} = \begin{pmatrix}5\\1\end{pmatrix}", "erste Spalte von $AB$"),
                      (r"AB_{\cdot 2} = \begin{pmatrix}1 & 2\\0 & 1\end{pmatrix}\begin{pmatrix}0\\2\end{pmatrix} = \begin{pmatrix}4\\2\end{pmatrix}", "zweite Spalte von $AB$")], frei=True),
         typische_fehler=[(ints(mul([[3, 0], [1, 2]], [[1, 2], [0, 1]])), "Das ist $BA$. Beim Produkt $AB$ steht $A$ links: Zeilen von $A$ mal Spalten von $B$."),
                          ([[3, 0], [0, 2]], "Du hast Einträge an gleicher Stelle multipliziert. Das Matrixprodukt ist Zeile mal Spalte mit Summe.")])

# ── Seite 8: Beob. 5.48, Satz 5.49, Kor. 5.50 ───────────────────────────────
k.erklaerung("Produkt und Verkettung: Beob. 5.48, Satz 5.49, Kor. 5.50", G(r"""
## Das Produkt ist die Verkettung

**Beobachtung 5.48.** $f_{A+B} = f_A + f_B$, $f_{\lambda A} = \lambda f_A$ und $f_{AB} = f_A \circ f_B$.

**Satz 5.49.** Für lineare $f, h\colon V \to W$, $g\colon W \to X$ und Basen $\mathfrak{B}, \mathfrak{C}, \mathfrak{D}$ von $V, W, X$ gilt
$[f + h]_{\mathfrak{C} \leftarrow \mathfrak{B}} = [f] + [h]$, $[\lambda f] = \lambda [f]$ und
$$[g \circ f]_{\mathfrak{D} \leftarrow \mathfrak{B}} = [g]_{\mathfrak{D} \leftarrow \mathfrak{C}} \, [f]_{\mathfrak{C} \leftarrow \mathfrak{B}}.$$

**Korollar 5.50.** $(AB)C = A(BC)$, $A(B + C) = AB + AC$, $(A + B)C = AC + BC$, $\mathbb{I}_m A = A = A\mathbb{I}_n$, $(\lambda A)B = \lambda(AB) = A(\lambda B)$.

""") + R([
    (r"f\colon K^4 \to K^2:\ (2 \times 4),\quad g\colon K^2 \to K^3:\ (3 \times 2)", "zwei Abbildungen, Formate ihrer Matrizen"),
    (r"g \circ f\colon K^4 \to K^3:\ (3 \times 2)(2 \times 4) = (3 \times 4)", "die innere Zahl $2$ passt zusammen, die äußeren bleiben"),
], "Formate passen genau dann, wenn die Verkettung existiert", frei=True) + G(r"""

:::alt Als Kettenregel
Die Matrix von „erst $f$, dann $g$“ ist $[g][f]$. Das ist dieselbe Umkehr der Reihenfolge wie bei $g(f(x))$. Darum bleibt das Assoziativgesetz (Kor. 5.50) erhalten: Die Verkettung ist assoziativ, also auch das Produkt.
:::
"""))

k.zuordnen("Ordne jeder Operation auf linearen Abbildungen die Operation auf den Matrizen zu (Beob. 5.48, Satz 5.49).",
           [("$f + h$", "Summe $[f] + [h]$"), ("$\\lambda f$", "Vielfaches $\\lambda [f]$"), ("$g \\circ f$", "Produkt $[g][f]$"),
            ("$\\mathrm{id}_V$", "Einheitsmatrix $\\mathbb{I}_n$")],
           "Summen und Vielfache wirken spaltenweise. Die Verkettung wird zum Produkt, die Identität zur Einheitsmatrix.",
           ablenker=["Produkt $[f][g]$"],
           tipps=["Die Identität verändert nichts: Welche Matrix tut das?", "Die zuerst angewandte Abbildung steht im Produkt rechts."])

# ── Seite 9: Ring, Nullteiler ───────────────────────────────────────────────
k.erklaerung("Matrizen als Ring: Beob. 5.51, Bsp. 5.52, Bem. 5.53", G(r"""
## Kein Körper

**Beobachtung 5.51.** $(K^{n \times n}, +, \cdot)$ ist ein [[Ring]] mit Eins $\mathbb{I}_n$, für $n \ge 2$ **nicht kommutativ**, mit [[Nullteilern|Nullteiler]] und daher kein [[Körper]].

*Beweis.* Mit $E_{ij}$ (eine $1$ an Stelle $(i, j)$) gilt $E_{11}E_{12} = E_{12} \neq O = E_{12}E_{11}$ und $E_{11}E_{22} = O$.

**Beispiel 5.52.** Für die Projektion $P$ gilt $P(\mathbb{I}_2 - P) = O$ mit beiden Faktoren $\neq O$.

**Bemerkung 5.53.** $\mathrm{Hom}_K(V, W) \to K^{m \times n},\ f \mapsto [f]_{\mathfrak{C} \leftarrow \mathfrak{B}}$ ist ein Vektorraumisomorphismus.

""") + R([
    (r"E_{11}E_{12} = \begin{pmatrix}1 & 0\\0 & 0\end{pmatrix}\begin{pmatrix}0 & 1\\0 & 0\end{pmatrix} = \begin{pmatrix}0 & 1\\0 & 0\end{pmatrix}", "erst $E_{12}$, dann $E_{11}$"),
    (r"E_{12}E_{11} = \begin{pmatrix}0 & 1\\0 & 0\end{pmatrix}\begin{pmatrix}1 & 0\\0 & 0\end{pmatrix} = \begin{pmatrix}0 & 0\\0 & 0\end{pmatrix}", "andere Reihenfolge: das Nullprodukt"),
    (r"P(\mathbb{I}_2 - P) = \frac12\begin{pmatrix}1 & 1\\1 & 1\end{pmatrix}\cdot\frac12\begin{pmatrix}1 & -1\\-1 & 1\end{pmatrix} = O", "Bsp. 5.52: die Projektion löscht den senkrechten Anteil"),
], "Nicht kommutativ und mit Nullteilern", frei=True) + G(r"""

:::alt Als Werkzeugkasten
Bei Zahlen heißt $ab = 0$, dass einer null ist. Bei Matrizen kann ein Werkzeug (Projektion) genau das wegwerfen, was das andere (Differenz zur Projektion) übrig lässt. Beide tun etwas, zusammen nichts.
:::
"""))

k.mehrfach("Welche Aussagen über $(\\mathbb{R}^{n \\times n}, +, \\cdot)$ für $n \\ge 2$ stimmen (Beobachtung 5.51)?",
           ["Die Multiplikation ist nicht kommutativ", "Es gibt Nullteiler: $AB = O$ mit $A, B \\neq O$", "$\\mathbb{I}_n$ ist neutral bezüglich der Multiplikation",
            "Die Multiplikation ist assoziativ"],
           ["Aus $AB = O$ folgt $A = O$ oder $B = O$", "Jede Matrix $A \\neq O$ hat eine Inverse"],
           "Die vier ersten Aussagen stehen in Beobachtung 5.51 bzw. Korollar 5.50. Mit $E_{11}E_{22} = O$ sieht man, dass ein Produkt null sein kann, ohne dass ein Faktor null ist, "
           "und dann hat $E_{11}$ keine Inverse.",
           tipps=["Denke an $E_{11}$ und $E_{22}$.", "Eine Matrix mit Nullspalte kann keine Inverse haben."],
           fehler={"Aus $AB = O$ folgt $A = O$ oder $B = O$": "Das gilt in Körpern, nicht für Matrizen: $E_{11}E_{22} = O$.",
                   "Jede Matrix $A \\neq O$ hat eine Inverse": "Die Projektion $P \\neq O$ bildet $(1, -1)^\\top$ auf $0$ ab und ist nicht invertierbar."})

# ── Seite 10: Transponierte ─────────────────────────────────────────────────
k.erklaerung("Die Transponierte (Def. 5.54, 5.56, Beob. 5.58)", G(r"""
## Zeilen werden Spalten

**Definition 5.54.** $A^\top \in K^{n \times m}$ mit $(A^\top)_{ji} := A_{ij}$: die [[Transponierte]].
Ein Vektor $v \in K^m$ gilt in Produkten als Matrix $K^{m \times 1}$, und $(u \mid v) = u^\top v$ (Def. 5.56).

**Beobachtung 5.58.** $(A^\top)^\top = A$, $(A + B)^\top = A^\top + B^\top$, $(\lambda A)^\top = \lambda A^\top$ und
$$(AB)^\top = B^\top A^\top.$$
Die Reihenfolge kehrt sich um. (Beweis: Übung.)

""") + R([
    (r"\begin{pmatrix}1 & 1 & 0\\0 & 0 & 1\end{pmatrix}^\top = \begin{pmatrix}1 & 0\\1 & 0\\0 & 1\end{pmatrix}", "Bsp. 5.55: erste Zeile wird erste Spalte"),
    (r"u^\top v = \begin{pmatrix}1 & 2\end{pmatrix}\begin{pmatrix}3\\4\end{pmatrix} = 1 \cdot 3 + 2 \cdot 4 = 11 = (u \mid v)", "Bsp. 5.57: Skalarprodukt als Matrixprodukt"),
    (r"uv^\top = \begin{pmatrix}1\\2\end{pmatrix}\begin{pmatrix}3 & 4\end{pmatrix} = \begin{pmatrix}3 & 4\\6 & 8\end{pmatrix}", "umgekehrte Reihenfolge: eine $2 \\times 2$-Matrix"),
], "Transponieren und Skalarprodukt", frei=True) + G(r"""

:::alt Als Schuhe und Socken
Erst Socken, dann Schuhe an: $AB$. Rückgängig machst du es in umgekehrter Reihenfolge: erst Schuhe aus, dann Socken aus. Genauso kehrt das Transponieren (und später das Invertieren) ein Produkt um.
:::
"""))

k.matrix("Seien $A = \\begin{pmatrix}1 & 2\\\\ 3 & 4\\end{pmatrix}$ und $B = \\begin{pmatrix}0 & 1\\\\ 1 & 1\\end{pmatrix}$. Berechne $(AB)^\\top$.",
         ints(tr(mul(_A58, _B58))),
         "$AB = \\begin{pmatrix}2 & 3\\\\ 4 & 7\\end{pmatrix}$, transponiert $\\begin{pmatrix}2 & 4\\\\ 3 & 7\\end{pmatrix}$. Oder $B^\\top A^\\top$: gleich, nicht $A^\\top B^\\top$.",
         tipps=["Berechne zuerst $AB$, dann vertausche Zeilen und Spalten.", "Probe: $B^\\top A^\\top$ muss dasselbe ergeben.", "$AB = \\begin{pmatrix}2 & 3\\\\ 4 & 7\\end{pmatrix}$."],
         rechenweg=R([(r"AB = " + M(mul(_A58, _B58)), "Zeile mal Spalte"), (r"(AB)^\top = " + M(tr(mul(_A58, _B58))), "Zeilen und Spalten vertauscht"),
                      (r"A^\top B^\top = " + M(mul(tr(_A58), tr(_B58))) + r" \neq (AB)^\top", "falsche Reihenfolge")], frei=True),
         typische_fehler=[(ints(mul(tr(_A58), tr(_B58))), "Das ist $A^\\top B^\\top$. Die Reihenfolge kehrt sich um: $(AB)^\\top = B^\\top A^\\top$."),
                          (ints(mul(_A58, _B58)), "Das ist $AB$ ohne Transponieren.")])

# ── Praxis ──────────────────────────────────────────────────────────────────
k.praxis()


def matrix_vektor(rng):
    m, n = rng.choice([(2, 2), (2, 3), (3, 2), (3, 3)])
    A = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
    x = [rng.randint(-3, 3) for _ in range(n)]
    if all(v == 0 for v in x):
        x[0] = 2
    erg = ints(mv(A, x))
    kandidaten = [(ints(mv(A, x[::-1])), "Du hast die Komponenten von $x$ in falscher Reihenfolge benutzt: $x_1$ gehört zur ersten Spalte."),
                  ([erg[0] * -1] + erg[1:], "Ein Vorzeichen in der ersten Komponente stimmt nicht: Rechne Zeile mal Spalte noch einmal."),
                  (erg[::-1], "Die Komponenten stehen in falscher Reihenfolge: Die erste Zeile von $A$ liefert die erste Komponente."),
                  ([-v for v in erg], "Alle Vorzeichen sind umgedreht: Rechne die Produkte noch einmal nach.")]
    if m == n:
        kandidaten.append((ints(mv(tr(A), x)), "Du hast mit der Transponierten gerechnet (Zeilen und Spalten vertauscht): Die Spalten von $A$ werden mit $x_j$ kombiniert."))
    fehler = ohne_gleiche(erg, kandidaten)
    spalten = " + ".join(f"({x[j]}) \\cdot {vt([A[i][j] for i in range(m)])}" for j in range(n))
    zeile1 = " + ".join(f"{A[0][j]} \\cdot ({x[j]})" for j in range(n))
    return {"frage": f"Berechne $Ax$ für $A = {M(A)}$ und $x = {vt(x)}$.",
            "loesung": erg,
            "tipps": ["Das Ergebnis liegt in $\\mathbb{R}^m$: Es hat so viele Komponenten wie $A$ Zeilen.", f"Spaltenweise: $Ax = x_1 A_{{\\cdot 1}} + \\dots + x_{n} A_{{\\cdot {n}}}$ mit $x = {vt(x)}$.",
                      f"Die erste Komponente ist Zeile $1$ mal $x$: ${zeile1} = {erg[0]}$."],
            "rechenweg": R([(f"Ax = {spalten}", "Def. 5.29: Linearkombination der Spalten"),
                            (f"= {vt(erg)}", "komponentenweise ausgerechnet")], frei=True),
            "erklaerung": "Das Matrix-Vektor-Produkt ist die Linearkombination der Spalten mit den Komponenten von $x$ als Koeffizienten (Def. 5.29).",
            "typische_fehler": fehler}


def matrixprodukt(rng):
    m, n, r = rng.choice([(2, 2, 2), (2, 2, 2), (2, 3, 2), (3, 2, 2), (2, 2, 3)])
    A = [[rng.randint(-2, 3) for _ in range(n)] for _ in range(m)]
    B = [[rng.randint(-2, 3) for _ in range(r)] for _ in range(n)]
    C = ints(mul(A, B))
    kandidaten = []
    if m == n == r:
        kandidaten.append((ints(mul(B, A)), "Das ist $BA$. Bei $AB$ stehen die Zeilen von $A$ links: Zeile von $A$ mal Spalte von $B$."))
        kandidaten.append(([[A[i][j] * B[i][j] for j in range(r)] for i in range(m)], "Du hast Einträge an gleicher Stelle multipliziert. Das Matrixprodukt ist Zeile mal Spalte mit Summe."))
    kandidaten.append(([[C[i][j] + (1 if (i, j) == (0, 0) else 0) for j in range(r)] for i in range(m)], "Der Eintrag oben links stimmt nicht: Rechne Zeile $1$ von $A$ mal Spalte $1$ von $B$ noch einmal."))
    fehler = ohne_gleiche_m(C, kandidaten)
    zeilen = [(f"(AB)_{{11}} = " + " + ".join(f"{A[0][t]} \\cdot ({B[t][0]})" for t in range(n)) + f" = {C[0][0]}", "Zeile $1$ von $A$ mal Spalte $1$ von $B$"),
              (f"AB = {M(C)}", f"alle {m * r} Einträge so berechnet, Format ${m} \\times {r}$")]
    return {"frage": f"Berechne $AB$ für $A = {M(A)}$ und $B = {M(B)}$.", "loesung": C,
            "tipps": [f"$A$ hat Format ${m} \\times {n}$ und $B$ Format ${n} \\times {r}$: Das Ergebnis hat Format ${m} \\times {r}$.",
                      "Der Eintrag $(AB)_{ij}$ ist Zeile $i$ von $A$ mal Spalte $j$ von $B$ (Summe der Produkte).",
                      f"$(AB)_{{11}} = {C[0][0]}$."],
            "rechenweg": R(zeilen, frei=True),
            "erklaerung": "Das Matrixprodukt wendet $A$ auf jede Spalte von $B$ an (Def. 5.46): $(AB)_{ij} = \\sum_k A_{ik} B_{kj}$.",
            "typische_fehler": fehler}


def darstellungsmatrix(rng):
    while True:
        c1 = [rng.randint(-2, 3), rng.randint(-2, 3)]
        c2 = [rng.randint(-2, 3), rng.randint(-2, 3)]
        if c1[0] * c2[1] - c1[1] * c2[0] != 0:
            break
    while True:
        D = [[rng.randint(-2, 3) for _ in range(2)] for _ in range(2)]    # gesuchte Darstellungsmatrix [f]_{C<-E}
        if sum(abs(x) for z in D for x in z) >= 2:
            break
    # f(e_j) = D_1j c1 + D_2j c2
    bilder = [[D[0][j] * c1[i] + D[1][j] * c2[i] for i in range(2)] for j in range(2)]
    fehler = ohne_gleiche_m(D, [(tr(D), "Du hast die Koordinaten als Zeilen statt als Spalten eingetragen: Spalte $j$ ist $[f(e^{(j)})]_{\\mathfrak{C}}$."),
                              ([[bilder[0][0], bilder[1][0]], [bilder[0][1], bilder[1][1]]], "Das sind die Standardkoordinaten der Bilder. Gefragt sind die Koordinaten bezüglich $\\mathfrak{C}$."),
                              ([D[1], D[0]], "Die Koordinaten bezüglich $c^{(1)}$ und $c^{(2)}$ stehen vertauscht: Die erste Zeile gehört zu $c^{(1)}$.")])
    return {"frage": (f"$f\\colon \\mathbb{{R}}^2 \\to \\mathbb{{R}}^2$ sei linear mit $f(e^{{(1)}}) = {vt(bilder[0])}$ und $f(e^{{(2)}}) = {vt(bilder[1])}$. "
                      f"Sei $\\mathfrak{{C}} = \\left({vt(c1)}, {vt(c2)}\\right)$ (eine Basis des $\\mathbb{{R}}^2$) und $\\mathcal{{E}}$ die Standardbasis. Bestimme $[f]_{{\\mathfrak{{C}} \\leftarrow \\mathcal{{E}}}}$."),
            "loesung": D,
            "tipps": ["Spalte $j$ ist der Koordinatenvektor $[f(e^{(j)})]_{\\mathfrak{C}}$ (Def. 5.38).",
                      "Schreibe $f(e^{(j)}) = \\alpha c^{(1)} + \\beta c^{(2)}$ und löse nach $\\alpha, \\beta$.",
                      f"Für die erste Spalte: ${vt(bilder[0])} = {D[0][0]} \\cdot {vt(c1)} + {D[1][0]} \\cdot {vt(c2)}$."],
            "rechenweg": R([(f"{vt(bilder[0])} = {D[0][0]} \\cdot {vt(c1)} + ({D[1][0]}) \\cdot {vt(c2)}", "erste Spalte: Koordinaten von $f(e^{(1)})$ bezüglich $\\mathfrak{C}$"),
                            (f"{vt(bilder[1])} = {D[0][1]} \\cdot {vt(c1)} + ({D[1][1]}) \\cdot {vt(c2)}", "zweite Spalte"),
                            (f"[f]_{{\\mathfrak{{C}} \\leftarrow \\mathcal{{E}}}} = {M(D)}", "als Spalten nebeneinander")], frei=True),
            "erklaerung": "Die Darstellungsmatrix sammelt die Koordinaten der Bilder der Ausgangsbasis (hier $\\mathcal{E}$), gemessen in der Zielbasis $\\mathfrak{C}$.",
            "typische_fehler": fehler}


def _matrix_mit_rang(rng, m, n, r):
    while True:
        basis = [[rng.randint(-2, 3) for _ in range(n)] for _ in range(r)]
        zeilen = []
        for i in range(m):
            if i < r:
                zeilen.append(basis[i][:])
            else:
                koef = [rng.randint(-1, 2) for _ in range(r)]
                zeilen.append([sum(c * basis[j][s] for j, c in enumerate(koef)) for s in range(n)])
        rng.shuffle(zeilen)
        if mathlib.rang(zeilen) == r:
            return zeilen


def rang_der_matrix(rng):
    m, n = rng.choice([(3, 3), (3, 4), (2, 3), (4, 3)])
    r = rng.randint(1, min(m, n))
    A = _matrix_mit_rang(rng, m, n, r)
    g = mathlib.gauss(A, reduziert=False)
    stufe = g["ergebnis"]
    fehler = ohne_gleiche(r, [(min(m, n), "Das ist die größtmögliche Zahl, nicht der tatsächliche Rang. Prüfe, ob sich eine Zeile aus den anderen kombinieren lässt."),
                              (m, "Das ist die Zeilenzahl. Der Rang zählt nur die unabhängigen Zeilen."),
                              (r + 1, "Der Rang ist kleiner: Mindestens eine Zeile ist eine Linearkombination der anderen.")])
    return {"frage": f"Bestimme den Rang von $A = {M(A)}$.",
            "loesung": r,
            "tipps": ["Der Rang ist die Dimension des Spaltenraums, also die Zahl linear unabhängiger Spalten (Beob. 5.33).",
                      "Bringe $A$ mit dem Gauß-Verfahren auf Zeilenstufenform und zähle die Zeilen, die nicht null sind.",
                      f"In der Stufenform bleiben {r} Zeile(n) ungleich null."],
            "rechenweg": R([(f"A \\to {M(stufe)}", "Zeilenstufenform nach dem Gauß-Verfahren (Zeilenumformungen ändern den Rang nicht)"),
                            (f"\\mathrm{{rang}}\\, A = {r}", "Anzahl der Zeilen ungleich null")], frei=True),
            "erklaerung": "Der Rang zählt die linear unabhängigen Spalten (oder Zeilen). Das Gauß-Verfahren liest ihn an den Pivots ab.",
            "typische_fehler": fehler}


k.generator(matrix_vektor, typ="vektor", titel="Matrix-Vektor-Produkt")
k.generator(matrixprodukt, typ="matrix", titel="Matrixprodukt berechnen")
k.generator(darstellungsmatrix, typ="matrix", titel="Darstellungsmatrix bezüglich einer Basis")
k.generator(rang_der_matrix, typ="zahl", titel="Rang einer Matrix bestimmen")

k.rechenweg_aufgabe(r"""
## Quiz-Stil: Projektion und Spiegelung (Bsp. 5.44 bis 5.47)

Seien $P = \frac12\begin{pmatrix}1 & 1\\ 1 & 1\end{pmatrix}$ (Projektion auf $G = \langle (1, 1)^\top \rangle$) und $C = \begin{pmatrix}1 & 0\\ 0 & -1\end{pmatrix}$ (Spiegelung an der ersten Achse).
""",
    [{"typ": "matrix", "frage": "Berechne $PC$ (erst spiegeln, dann projizieren).", "loesung": mul(_P, _C),
      "tipps": ["Zeile mal Spalte, mit dem Faktor $\\frac12$ am Ende.", "Zeile $1$ von $P$ mal Spalte $2$ von $C$ ist $\\frac12 (1 \\cdot 0 + 1 \\cdot (-1))$."],
      "rechenweg": "$PC = \\frac12\\begin{pmatrix}1 & -1\\\\ 1 & -1\\end{pmatrix}$.",
      "typische_fehler": [(mul(_C, _P), "Das ist $CP$ (erst projizieren, dann spiegeln).")]},
     {"typ": "matrix", "frage": "Berechne $CP$.", "loesung": mul(_C, _P),
      "tipps": ["Jetzt steht $C$ links.", "Zeile $2$ von $C$ ist $(0, -1)$."],
      "rechenweg": "$CP = \\frac12\\begin{pmatrix}1 & 1\\\\ -1 & -1\\end{pmatrix}$.",
      "typische_fehler": [(mul(_P, _C), "Das ist $PC$.")]},
     {"typ": "wf", "frage": "Es gilt $PC = CP$.", "wahr": False,
      "tipps": ["Vergleiche die beiden Ergebnisse."], "erklaerung": "Das Matrixprodukt ist im Allgemeinen nicht kommutativ."},
     {"typ": "matrix", "frage": "Berechne $C^2$.", "loesung": mul(_C, _C),
      "tipps": ["Zweimal spiegeln.", "Das Ergebnis ist die Einheitsmatrix."],
      "rechenweg": "$C^2 = \\begin{pmatrix}1 & 0\\\\ 0 & 1\\end{pmatrix} = \\mathbb{I}_2$.",
      "typische_fehler": [(_C, "Das wäre $C$ selbst. Zweimal $-1$ ergibt $+1$ in der zweiten Diagonale.")]}],
    "$PC \\neq CP$, und $C^2 = \\mathbb{I}_2$: Zweimaliges Spiegeln bringt jeden Vektor zurück, $C$ ist sein eigenes Inverses.",
    uebungsblatt=True,
    tipps=["Das Produkt $XY$ bedeutet: erst $Y$, dann $X$.", "Zeile mal Spalte.", "$C^2 = CC$."],
    rechenweg=r"""
:::rechnung
?? PC = \frac12\begin{pmatrix}1 & -1\\1 & -1\end{pmatrix},\ CP = \frac12\begin{pmatrix}1 & 1\\-1 & -1\end{pmatrix} || verschieden
?? C^2 = \begin{pmatrix}1 & 0\\0 & 1\end{pmatrix} || zweimal spiegeln
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Satz 5.49

Seien $f\colon V \to W$ und $g\colon W \to X$ linear, $\mathfrak{B}, \mathfrak{C}, \mathfrak{D}$ geordnete Basen von $V, W, X$. Zeigen Sie
$$[g \circ f]_{\mathfrak{D} \leftarrow \mathfrak{B}} = [g]_{\mathfrak{D} \leftarrow \mathfrak{C}} \, [f]_{\mathfrak{C} \leftarrow \mathfrak{B}}.$$
Sie dürfen Satz 5.40 und die Beobachtung $f_{AB} = f_A \circ f_B$ verwenden.
""",
    r"""
Sei $F := [f]_{\mathfrak{C} \leftarrow \mathfrak{B}}$ und $G := [g]_{\mathfrak{D} \leftarrow \mathfrak{C}}$. Für alle $v \in V$ gilt nach Satz 5.40 zweimal angewandt
$$[g(f(v))]_{\mathfrak{D}} = G [f(v)]_{\mathfrak{C}} = G \big( F [v]_{\mathfrak{B}} \big) = (GF) [v]_{\mathfrak{B}},$$
die letzte Gleichheit wegen $f_{GF} = f_G \circ f_F$ (Beob. 5.48).
Setzt man für $v$ nacheinander die Basisvektoren $b^{(j)}$ ein, so ist $[b^{(j)}]_{\mathfrak{B}} = e^{(j)}$ der $j$-te Standardbasisvektor, und $(GF) e^{(j)}$ ist die $j$-te Spalte von $GF$.
Die $j$-te Spalte von $[g \circ f]_{\mathfrak{D} \leftarrow \mathfrak{B}}$ ist dagegen $[g(f(b^{(j)}))]_{\mathfrak{D}}$. Beide Spalten stimmen überein, also ist $GF = [g \circ f]_{\mathfrak{D} \leftarrow \mathfrak{B}}$. $\square$
""",
    ["Satz 5.40 wird auf $f$ und dann auf $g$ angewandt",
     "Das Klammern von $G(F[v])$ zu $(GF)[v]$ wird mit Beob. 5.48 begründet",
     "Für $v = b^{(j)}$ wird $[v]_{\\mathfrak{B}} = e^{(j)}$ benutzt",
     "Die Gleichheit der Spalten liefert die Gleichheit der Matrizen"],
    "Satz 5.40 zweimal, Assoziativität über Beob. 5.48, dann die Basisvektoren einsetzen, damit Spalten herauskommen.",
    uebungsblatt=True,
    tipps=["Beginne mit $[g(f(v))]_{\\mathfrak{D}}$ und wende Satz 5.40 an.", "Welche Koordinatenvektoren hat der $j$-te Basisvektor von $\\mathfrak{B}$ bezüglich $\\mathfrak{B}$?"])

k.papier(r"""
## Übungsblatt-Stil: Rechenregeln (Kor. 5.50 und Beob. 5.58, im Skript „Übung“)

1. Zeigen Sie für $A \in K^{m \times n}$ und $B, C \in K^{n \times r}$: $A(B + C) = AB + AC$.
2. Zeigen Sie für $A \in K^{m \times n}$ und $B \in K^{n \times r}$: $(AB)^\top = B^\top A^\top$.
""",
    r"""
**1.** Die $j$-te Spalte von $A(B + C)$ ist $A(B + C)_{\cdot j} = A(B_{\cdot j} + C_{\cdot j})$. Das Matrix-Vektor-Produkt ist linear in $x$ (Satz 5.31), also $= AB_{\cdot j} + AC_{\cdot j}$, die $j$-te Spalte von $AB + AC$.

**2.** Für $i \in \{1, \dots, m\}$, $j \in \{1, \dots, r\}$ gilt
$$((AB)^\top)_{ji} = (AB)_{ij} = \sum_{k=1}^n A_{ik} B_{kj}, \qquad (B^\top A^\top)_{ji} = \sum_{k=1}^n (B^\top)_{jk} (A^\top)_{ki} = \sum_{k=1}^n B_{kj} A_{ik}.$$
Beide Summen stimmen überein. $\square$
""",
    ["Bei 1 spaltenweise argumentiert und die Linearität von $x \\mapsto Ax$ benutzt",
     "Bei 2 den Eintrag $(AB)_{ij}$ als Summe $\\sum_k A_{ik} B_{kj}$ hingeschrieben",
     "Bei 2 die Einträge der Transponierten richtig vertauscht ($(A^\\top)_{ki} = A_{ik}$)",
     "Bei 2 die Gleichheit der Summen festgestellt"],
    "Spaltenweise argumentieren bzw. die Einträge vergleichen: Beide Beweise sind reine Indexrechnung.",
    tipps=["Für 1: Zeige, dass jede Spalte beider Seiten übereinstimmt.", "Für 2: Schreibe den Eintrag an Position $(j, i)$ beider Seiten als Summe."])

k.zusammenfassung(G(r"""
## Matrizen (Skript Abschn. 5.3 und 5.4)

- **Matrix** $A \in K^{m \times n}$ (Def. 5.28): $n$ Spalten aus $K^m$, Eintrag $A_{ij}$ (Zeile $i$, Spalte $j$). **$Ax := \sum_j x_j A_{\cdot j}$** (Def. 5.29), $(Ax)_i = \sum_j A_{ij} x_j$.
- **Satz 5.31:** $f_A\colon x \mapsto Ax$ ist linear, und jede lineare $f\colon K^n \to K^m$ ist $f_A$ für genau ein $A = (f(e^{(1)}), \dots, f(e^{(n)}))$.
- $\ker A = \{x \mid Ax = 0\}$, Bild $= \langle A_{\cdot 1}, \dots, A_{\cdot n} \rangle$, $\mathrm{rang}\, A$ = Zahl linear unabhängiger Spalten (Def. 5.32, Beob. 5.33).
- **Darstellungsmatrix** $[f]_{\mathfrak{C} \leftarrow \mathfrak{B}}$ (Def. 5.38): Spalte $j$ ist $[f(b^{(j)})]_{\mathfrak{C}}$. **Satz 5.40:** $[f(v)]_{\mathfrak{C}} = [f]_{\mathfrak{C} \leftarrow \mathfrak{B}} [v]_{\mathfrak{B}}$.
- $A + B$, $\lambda A$ eintragsweise; $K^{m \times n}$ hat Dimension $mn$ (Def. 5.42, Beob. 5.43).
- **Matrixprodukt** $AB = (AB_{\cdot 1}, \dots, AB_{\cdot r})$, $(AB)_{ij} = \sum_k A_{ik} B_{kj}$, Format $(m \times n)(n \times r)$ (Def. 5.46). $\mathbb{I}_n$ neutral (Def. 5.45). $f_{AB} = f_A \circ f_B$ (Beob. 5.48), $[g \circ f] = [g][f]$ (Satz 5.49).
- **Rechenregeln** (Kor. 5.50): assoziativ, distributiv. $K^{n \times n}$ ist ein Ring mit Eins, für $n \ge 2$ nicht kommutativ und mit Nullteilern (Beob. 5.51, Bsp. 5.52).
- **Transponierte** $(A^\top)_{ji} = A_{ij}$, $(AB)^\top = B^\top A^\top$, $(u \mid v) = u^\top v$ (Def. 5.54, 5.56, Beob. 5.58).

!! Das zuerst angewandte steht im Produkt rechts: $[g \circ f] = [g][f]$.
"""))
