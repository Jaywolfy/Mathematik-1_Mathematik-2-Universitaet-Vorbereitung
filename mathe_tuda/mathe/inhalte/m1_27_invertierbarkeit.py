# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 27: Invertierbarkeit (Skript Disser WS 26/27, Abschn. 5.5, Def. 5.59 bis Beob. 5.69)."""
import re
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche
from .glossar import finden

k = neues_kapitel(
    slug="invertierbarkeit",
    titel="Invertierbarkeit",
    beschreibung="Inverse Matrix, Eindeutigkeit, Äquivalenzen (Satz 5.65), AB = I genügt, Inverse ausrechnen, (AB)^-1, GL_n(K)",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 5.5",
    icon="↩️")


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


mul, mv, tr, inv, I2 = mathlib.mat_mul, mathlib.mat_vec, mathlib.transponiert, mathlib.inverse, mathlib.einheitsmatrix(2)

# ── Nachgerechnet beim Laden ───────────────────────────────────────────────
_A1, _B1 = [[2, 1], [1, 1]], [[1, -1], [-1, 2]]
assert mul(_A1, _B1) == I2 and mul(_B1, _A1) == I2 and inv(_A1) == _B1
_C = [[1, 0], [0, -1]]
_P = [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]
assert mul(_C, _C) == I2 and inv(_P) is None and mathlib.rang(_P) == 1
assert inv([[1, 0], [1, 1]]) == [[1, 0], [-1, 1]]                       # Bsp. 5.64: [T]^-1
assert inv([[2, 1], [5, 3]]) == [[3, -1], [-5, 2]] and inv([[1, 2], [3, 4]]) == [[-2, 1], [F(3, 2), F(-1, 2)]]
assert mathlib.det([[2, 4], [1, 2]]) == 0 and inv([[2, 4], [1, 2]]) is None
# Bsp. 5.67: A = (1 0), B = (1, 0)^T: AB = I_1, BA != I_2
assert mul([[1, 0]], [[1], [0]]) == [[1]] and mul([[1], [0]], [[1, 0]]) == [[1, 0], [0, 0]]
# (AB)^-1 = B^-1 A^-1
_A68, _B68 = [[1, -1], [0, 1]], [[2, 1], [1, 1]]
assert inv(mul(_A68, _B68)) == mul(inv(_B68), inv(_A68)) and inv(mul(_A68, _B68)) == [[1, 0], [-1, 1]]
assert mul(inv(_A68), inv(_B68)) != inv(mul(_A68, _B68))
# Rechenweg-Aufgabe: Auswertung T(f) = (f(1), f(3)) mit Basis (1, t)
_TT = [[1, 1], [1, 3]]
assert inv(_TT) == [[F(3, 2), F(-1, 2)], [F(-1, 2), F(1, 2)]] and mv(inv(_TT), [4, 10]) == [1, 3]
# Satz 5.65: Spaltenrang
assert mathlib.rang([[1, 2], [2, 4]]) == 1 and mathlib.rang(_A1) == 2

k.lernziele([
    "Ich kann entscheiden, ob eine quadratische Matrix invertierbar ist, und kenne die gleichwertigen Bedingungen aus Satz 5.65",
    "Ich kann die Inverse einer $2 \\times 2$- oder $3 \\times 3$-Matrix bestimmen und mit einer Probe überprüfen (Def. 5.59, Beob. 5.60)",
    "Ich weiß, warum bei quadratischen Matrizen $AB = \\mathbb{I}_n$ schon $BA = \\mathbb{I}_n$ nach sich zieht (Kor. 5.66, Bsp. 5.67)",
    "Ich kann $(AB)^{-1} = B^{-1}A^{-1}$ anwenden und kenne die Gruppe $\\mathrm{GL}_n(K)$ (Satz 5.68, Beob. 5.69)",
])

k.warum(r"""
Eine invertierbare Matrix ist eine verlustfreie, umkehrbare Transformation: Verschlüsselungsverfahren wie der Hill-Chiffre,
Koordinatenwechsel in der Grafik-Pipeline und das Auflösen linearer Gleichungssysteme beruhen darauf. Umgekehrt ist
nicht invertierbar gleich Information geht verloren, wie bei einer Projektion. In der Numerik berechnet man die Inverse
fast nie explizit, aber man muss wissen, wann sie existiert: Satz 5.65 liefert dafür mehrere gleichwertige Tests.
""")

# ── Seite 1: Definition 5.59, Beobachtung 5.60 ──────────────────────────────
k.erklaerung("Inverse Matrix (Def. 5.59, Beob. 5.60)", G(r"""
## Rückgängig machen

:::analogie ↩️ Rückgängig-Knopf
Manche Aktionen lassen sich rückgängig machen (ein Foto drehen), andere nicht (ein Foto in Schwarzweiß umwandeln). Eine Matrix ist invertierbar, wenn ihre Abbildung einen Rückgängig-Knopf hat.
:::

**Definition 5.59.** $A \in K^{n \times n}$ heißt [[invertierbare Matrix|invertierbar]], wenn es $B \in K^{n \times n}$ gibt mit $AB = BA = \mathbb{I}_n$. Dieses $B$ ist die Inverse.

**Beobachtung 5.60.** Die Inverse ist **eindeutig**, geschrieben $A^{-1}$.

*Beweis.* Sind $B, C$ Inverse von $A$, so gilt $B = B\mathbb{I}_n = B(AC) = (BA)C = \mathbb{I}_n C = C$. $\square$

:::visual matrix_mult
{"a": [[2, 1], [1, 1]], "b": [[1, -1], [-1, 2]],
 "unterschrift": "$A A^{-1} = \\mathbb{I}_2$: Jede Zeile von $A$ mal Spalte von $A^{-1}$ gibt eine $1$ auf der Diagonale und $0$ daneben."}
:::

""") + R([
    (r"AB = \begin{pmatrix}2 & 1\\1 & 1\end{pmatrix}\begin{pmatrix}1 & -1\\-1 & 2\end{pmatrix} = \begin{pmatrix}2 - 1 & -2 + 2\\1 - 1 & -1 + 2\end{pmatrix} = \mathbb{I}_2", "Zeile mal Spalte"),
    (r"BA = \begin{pmatrix}1 & -1\\-1 & 2\end{pmatrix}\begin{pmatrix}2 & 1\\1 & 1\end{pmatrix} = \mathbb{I}_2", "auch in der anderen Reihenfolge: $B = A^{-1}$"),
], "Eine Inverse nachgerechnet", frei=True) + G(r"""

:::alt Als Wörterbuch
Zwei Wörterbücher, die beide Deutsch-Englisch rückgängig machen, müssten sich gegenseitig übersetzen: Dann sind sie dasselbe. Das ist die Eindeutigkeit. Das Beweisschema ist das aus Satz 3.9 für Gruppen.
:::
"""))

k.ordnen("Ordne den Beweis von Beobachtung 5.60: Zwei Inverse $B, C$ von $A$ sind gleich.",
         ["Seien $B$ und $C$ Inverse von $A$, also $AB = BA = \\mathbb{I}_n$ und $AC = CA = \\mathbb{I}_n$.",
          "Dann gilt $B = B\\mathbb{I}_n$, weil $\\mathbb{I}_n$ neutral ist (Kor. 5.50).",
          "Mit $\\mathbb{I}_n = AC$ folgt $B\\mathbb{I}_n = B(AC)$.",
          "Nach der Assoziativität (Kor. 5.50) ist $B(AC) = (BA)C$.",
          "Wegen $BA = \\mathbb{I}_n$ ist $(BA)C = \\mathbb{I}_n C = C$. Also $B = C$. $\\square$"],
         "Die Kette läuft $B = B\\mathbb{I}_n = B(AC) = (BA)C = \\mathbb{I}_n C = C$. Jede Gleichheit hat genau einen Grund.",
         ablenker=["Da $A$ invertierbar ist, darf man durch $A$ teilen: $B = C$.", "Weil $AB = BA$ gilt, ist die Matrixmultiplikation kommutativ."],
         tipps=["Der Beweis ist eine Gleichheitskette von $B$ nach $C$.", "Wo steht $\\mathbb{I}_n$, und welche Gleichung ersetzt es?", "Matrixmultiplikation ist nicht kommutativ, Division durch Matrizen gibt es nicht."])

k.mehrfach("Welche dieser Matrizen sind invertierbar?",
           ["$\\mathbb{I}_2$", "$C = \\begin{pmatrix}1 & 0\\\\ 0 & -1\\end{pmatrix}$ (Spiegelung)", "$\\begin{pmatrix}0 & 1\\\\ 1 & 0\\end{pmatrix}$", "$\\begin{pmatrix}2 & 0\\\\ 0 & 3\\end{pmatrix}$"],
           ["$P = \\frac12\\begin{pmatrix}1 & 1\\\\ 1 & 1\\end{pmatrix}$ (Projektion)", "die Nullmatrix $O \\in \\mathbb{R}^{2 \\times 2}$", "$\\begin{pmatrix}1 & 2\\\\ 2 & 4\\end{pmatrix}$"],
           "Invertierbar sind $\\mathbb{I}_2$ und $C$ (jeweils eigene Inverse), die Vertauschung (ebenfalls) und die Diagonalmatrix mit Inverse $\\mathrm{diag}(\\frac12, \\frac13)$. "
           "Bei $P$, $O$ und der letzten Matrix sind die Spalten linear abhängig: Es gibt einen Vektor $\\neq 0$ mit $Ax = 0$ (Beispiel 5.62, Satz 5.65).",
           tipps=["Eine Matrix ist nicht invertierbar, wenn ein Vektor $\\neq 0$ auf null abgebildet wird.", "Sind zwei Spalten Vielfache voneinander?", "Zweimal anwenden von $C$ oder der Vertauschung gibt die Identität."],
           fehler={"$P = \\frac12\\begin{pmatrix}1 & 1\\\\ 1 & 1\\end{pmatrix}$ (Projektion)": "$P(1, -1)^\\top = 0$: Der Kern ist nicht $\\{0\\}$, also nicht invertierbar (Bsp. 5.62).",
                   "die Nullmatrix $O \\in \\mathbb{R}^{2 \\times 2}$": "Die Nullmatrix bildet alles auf $0$ ab.",
                   "$\\begin{pmatrix}1 & 2\\\\ 2 & 4\\end{pmatrix}$": "Die zweite Spalte ist das Doppelte der ersten, also $A(2, -1)^\\top = 0$: Rang $1$."})

# ── Seite 2: Satz 5.61 ──────────────────────────────────────────────────────
k.erklaerung("Satz 5.61 und Beispiel 5.62", G(r"""
## Invertierbar heißt: die Abbildung ist umkehrbar

**Satz 5.61.** $A \in K^{n \times n}$ ist genau dann invertierbar, wenn $f_A\colon K^n \to K^n$ ein Automorphismus ist. Dann gilt $f_{A^{-1}} = (f_A)^{-1}$.

*Beweis.* „$\Rightarrow$“: $f_A \circ f_{A^{-1}} = f_{AA^{-1}} = f_{\mathbb{I}_n} = \mathrm{id}$ und ebenso andersherum, nach Satz 1.76 ist $f_A$ bijektiv.
„$\Leftarrow$“: $(f_A)^{-1}$ ist linear (Beob. 5.13), hat also eine Matrix $B$ (Satz 5.31). Aus $f_{AB} = \mathrm{id} = f_{\mathbb{I}_n}$ folgt $AB = BA = \mathbb{I}_n$ (Eindeutigkeit der Matrix). $\square$

""") + R([
    (r"C^2 = \mathbb{I}_2 \Rightarrow C^{-1} = C", "zweimal spiegeln gibt die Identität (Bsp. 5.62)"),
    (r"P\begin{pmatrix}1\\-1\end{pmatrix} = \begin{pmatrix}0\\0\end{pmatrix} = P\begin{pmatrix}0\\0\end{pmatrix}", "$f_P$ ist nicht injektiv, also nicht bijektiv: $P$ nicht invertierbar"),
], "Spiegelung und Projektion", frei=True) + G(r"""

:::alt Als Fahrstuhl
Ein Fahrstuhl, der Stockwerke eindeutig zuordnet (jedes Ziel genau ein Start), lässt sich rückwärts fahren. Ein Fahrstuhl, der zwei Startetagen auf dieselbe Zieletage schickt, nicht.
:::
"""))

k.mc("Welche Aussage über $A \\in K^{n \\times n}$ ist nach Satz 5.61 gleichwertig zur Invertierbarkeit?",
     ["$f_A\\colon K^n \\to K^n$ ist bijektiv (ein Automorphismus)", "$f_A$ ist linear", "$A$ ist symmetrisch", "$A$ hat keine Nullzeile"],
     "Satz 5.61: invertierbar genau dann, wenn $f_A$ ein Automorphismus ist, also bijektiv. Linear ist jedes $f_A$ (Satz 5.31). Symmetrie und fehlende Nullzeile sind weder notwendig noch hinreichend.",
     tipps=["Die Inverse einer Matrix entspricht der Umkehrabbildung.", "Gilt die Eigenschaft für jede Matrix, kann sie nichts über Invertierbarkeit aussagen."],
     fehler={"$f_A$ ist linear": "Das gilt für jede Matrix $A$ (Satz 5.31), auch für $P$, die nicht invertierbar ist.",
             "$A$ ist symmetrisch": "$P$ ist symmetrisch und nicht invertierbar; $\\begin{pmatrix}1 & 1\\\\ 0 & 1\\end{pmatrix}$ ist invertierbar und nicht symmetrisch.",
             "$A$ hat keine Nullzeile": "Notwendig, aber nicht hinreichend: $\\begin{pmatrix}1 & 1\\\\ 1 & 1\\end{pmatrix}$ hat keine Nullzeile und ist nicht invertierbar."})

# ── Seite 3: Korollar 5.63, Beispiel 5.64 ───────────────────────────────────
k.erklaerung("Korollar 5.63 und Beispiel 5.64", G(r"""
## Inverse und Umkehrabbildung in beliebigen Basen

**Korollar 5.63.** Ist $f\colon V \to W$ ein Isomorphismus und sind $\mathfrak{B}$, $\mathfrak{C}$ geordnete Basen von $V$ und $W$, so ist $[f]_{\mathfrak{C} \leftarrow \mathfrak{B}}$ invertierbar und
$$[f^{-1}]_{\mathfrak{B} \leftarrow \mathfrak{C}} = \big([f]_{\mathfrak{C} \leftarrow \mathfrak{B}}\big)^{-1}.$$
Ausgangs- und Zielbasis tauschen ihre Rollen. *Beweis.* $[f^{-1}][f] = [f^{-1} \circ f]_{\mathfrak{B} \leftarrow \mathfrak{B}} = \mathbb{I}_n$ nach Satz 5.49, ebenso $[f][f^{-1}] = \mathbb{I}_n$.

""") + R([
    (r"[T]_{\mathcal{E} \leftarrow \mathfrak{B}} = \begin{pmatrix}1 & 0\\1 & 1\end{pmatrix}", "Auswertung $T(f) = (f(0), f(1))^\\top$ auf $f(t) = a + bt$ (Bsp. 5.64)"),
    (r"T^{-1}\begin{pmatrix}u\\v\end{pmatrix}(t) = u + (v - u)t \Rightarrow [T^{-1}]_{\mathfrak{B} \leftarrow \mathcal{E}} = \begin{pmatrix}1 & 0\\-1 & 1\end{pmatrix}", "aus $a = u$, $a + b = v$ folgt $b = v - u$"),
    (r"\begin{pmatrix}1 & 0\\-1 & 1\end{pmatrix}\begin{pmatrix}2\\5\end{pmatrix} = \begin{pmatrix}2\\3\end{pmatrix}", "$a = 2$, $b = 3$: $f(t) = 2 + 3t$ mit $f(0) = 2$, $f(1) = 5$"),
], "Die Auswertung und ihre Umkehrung", frei=True) + G(r"""

:::alt Als Hin- und Rückfahrt
Hinfahrt von $\mathfrak{B}$ nach $\mathfrak{C}$: Matrix $[f]$. Die Rückfahrt von $\mathfrak{C}$ nach $\mathfrak{B}$ ist die Umkehrabbildung mit der inversen Matrix. Start und Ziel tauschen ihre Plätze, deshalb steht der Index umgekehrt da.
:::
"""))

k.matrix("Die Matrix $[T]_{\\mathcal{E} \\leftarrow \\mathfrak{B}} = \\begin{pmatrix}1 & 0\\\\ 1 & 1\\end{pmatrix}$ gehört zum Isomorphismus $T$ aus Beispiel 5.64. Bestimme $[T^{-1}]_{\\mathfrak{B} \\leftarrow \\mathcal{E}}$ (Korollar 5.63).",
         [[1, 0], [-1, 1]],
         "Nach Korollar 5.63 ist $[T^{-1}] = [T]^{-1}$. Probe: $\\begin{pmatrix}1 & 0\\\\ 1 & 1\\end{pmatrix}\\begin{pmatrix}1 & 0\\\\ -1 & 1\\end{pmatrix} = \\begin{pmatrix}1 & 0\\\\ 1 - 1 & 1\\end{pmatrix} = \\mathbb{I}_2$.",
         tipps=["Gesucht ist die inverse Matrix.", "Aus $a = u$ und $a + b = v$ folgt $b = v - u$.", "Die Spalten der Inversen sind die Lösungen von $Ax = e^{(1)}$ und $Ax = e^{(2)}$."],
         rechenweg=R([(r"\begin{pmatrix}1 & 0\\1 & 1\end{pmatrix}\begin{pmatrix}a\\b\end{pmatrix} = \begin{pmatrix}u\\v\end{pmatrix} \Rightarrow a = u,\ b = v - u", "System lösen"),
                      (r"\begin{pmatrix}a\\b\end{pmatrix} = \begin{pmatrix}1 & 0\\-1 & 1\end{pmatrix}\begin{pmatrix}u\\v\end{pmatrix}", "Koeffizientenmatrix der Lösung ist die Inverse")], frei=True),
         typische_fehler=[([[1, -1], [0, 1]], "Das ist die Transponierte der richtigen Matrix. Probe: $\\begin{pmatrix}1 & 0\\\\ 1 & 1\\end{pmatrix}\\begin{pmatrix}1 & -1\\\\ 0 & 1\\end{pmatrix} \\neq \\mathbb{I}_2$."),
                          ([[1, 0], [1, 1]], "Das ist die Matrix selbst. Eine Matrix ist hier nicht ihre eigene Inverse.")])

# ── Seite 4: Satz 5.65 ──────────────────────────────────────────────────────
k.erklaerung("Satz 5.65: Vier gleichwertige Bedingungen", G(r"""
## Satz 5.65

Für $A \in K^{n \times n}$ sind gleichwertig:

(i) $A$ ist invertierbar. (ii) $\ker A = \{0\}$. (iii) $\mathrm{rang}\, A = n$. (iv) $(A_{\cdot 1}, \dots, A_{\cdot n})$ ist eine geordnete <<Basis|Basis>> von $K^n$.

*Beweisidee.* (i) $\iff$ $f_A$ bijektiv (Satz 5.61). Bei gleichem Definitions- und Zielraum ist das schon gleichwertig zu injektiv (Satz 5.23), also zu (ii), und zu surjektiv, also zu (iii). Für (iv): $f_A(x) = \sum x_j A_{\cdot j}$, also ist jeder $y$ genau auf eine Weise Spaltenkombination, genau wenn die Spalten eine Basis sind (Satz 4.55).

""") + R([
    (r"A = \begin{pmatrix}1 & 2\\2 & 4\end{pmatrix}:\ A\begin{pmatrix}2\\-1\end{pmatrix} = \begin{pmatrix}0\\0\end{pmatrix}", "(ii) verletzt: Kern $\\neq \\{0\\}$"),
    (r"\mathrm{rang}\, A = 1 < 2 = n", "(iii) verletzt: Spalten linear abhängig, (iv) verletzt"),
    (r"B = \begin{pmatrix}2 & 1\\1 & 1\end{pmatrix}:\ \mathrm{rang}\, B = 2 = n", "Spalten $(2, 1)^\\top$ und $(1, 1)^\\top$ sind unabhängig: $B$ invertierbar"),
], "Ein Gegenbeispiel und ein Beispiel", frei=True) + G(r"""

:::alt Als Landkarte
Vier Wege auf derselben Insel: (i) umkehrbar, (ii) kein Vektor verschwindet, (iii) alle Richtungen werden erreicht, (iv) die Spalten sind ein brauchbares Koordinatensystem. Welchen du nimmst, hängt vom Problem ab. Aufgabenblätter fragen meist nach Rang oder Kern.
:::
"""))

k.mehrfach("Welche Aussagen sind für $A \\in K^{n \\times n}$ gleichwertig zur Invertierbarkeit (Satz 5.65)?",
           ["$\\ker A = \\{0\\}$", "$\\mathrm{rang}\\, A = n$", "Die Spalten von $A$ bilden eine Basis des $K^n$", "$f_A$ ist surjektiv"],
           ["$A$ hat keine Nullspalte", "$A_{ij} \\neq 0$ für alle $i, j$", "$A$ ist symmetrisch"],
           "Die ersten drei stehen in Satz 5.65, die Surjektivität folgt aus (iii) und Satz 5.23. Keine Nullspalte ist notwendig, aber nicht hinreichend, und Einträge $\\neq 0$ sagen nichts über lineare Unabhängigkeit.",
           tipps=["Suche Gegenbeispiele: eine Matrix ohne Nullspalte mit gleichen Spalten.", "$\\begin{pmatrix}1 & 1\\\\ 1 & 1\\end{pmatrix}$ hat nur Einträge $\\neq 0$."],
           fehler={"$A$ hat keine Nullspalte": "$\\begin{pmatrix}1 & 1\\\\ 1 & 1\\end{pmatrix}$ hat keine Nullspalte, aber Rang $1$.",
                   "$A_{ij} \\neq 0$ für alle $i, j$": "Alle Einträge $1$ ergeben Rang $1$; umgekehrt ist $\\begin{pmatrix}0 & 1\\\\ 1 & 0\\end{pmatrix}$ invertierbar.",
                   "$A$ ist symmetrisch": "$P$ ist symmetrisch und nicht invertierbar."})

k.luecke("Sei $A \\in K^{4 \\times 4}$ invertierbar. Dann gilt nach Satz 5.65 $\\dim\\ker A = \\luecke$ und $\\mathrm{rang}\\, A = \\luecke$.",
         "\\dim\\ker A = \\luecke,\\quad \\mathrm{rang}\\, A = \\luecke",
         [[0], [4]],
         "Invertierbar heißt $\\ker A = \\{0\\}$ (Dimension $0$) und $\\mathrm{rang}\\, A = n = 4$. Die Dimensionsformel passt: $4 = 0 + 4$.",
         tipps=["Satz 5.65 (ii) und (iii).", "Der Kern ist nur der Nullvektor.", "$n = 4$."],
         rechenweg=R([(r"4 = \dim\ker A + \mathrm{rang}\, A", "Dimensionsformel"), (r"4 = 0 + 4", "invertierbar: Kern trivial, voller Rang")]),
         typische_fehler=[([4, 0], "Vertauscht: Bei invertierbarem $A$ ist der Kern nur $\\{0\\}$ (Dimension $0$), der Rang ist $n$.")])

k.zahl("$A \\in \\mathbb{R}^{3 \\times 3}$ habe $\\mathrm{rang}\\, A = 2$. Welche Dimension hat $\\ker A$?", 1,
       "Dimensionsformel: $3 = \\dim\\ker A + 2$, also $\\dim\\ker A = 1$. Weil $\\ker A \\neq \\{0\\}$, ist $A$ nicht invertierbar (Satz 5.65).",
       tipps=["Dimensionsformel für $f_A$ mit $\\dim K^3 = 3$.", "$3 = \\dim\\ker A + \\mathrm{rang}\\, A$.", "Setze $\\mathrm{rang}\\, A = 2$ ein."],
       rechenweg=R([(r"3 = \dim\ker A + 2", "Satz 5.20"), (r"\dim\ker A = 1", "umgestellt")]),
       typische_fehler=[(2, "Das ist der Rang, nicht der Kern. Der Kern hat die fehlende Dimension."), (0, "Kern $\\{0\\}$ gilt nur bei Rang $3$.")])

# ── Seite 5: Korollar 5.66, Beispiel 5.67 ───────────────────────────────────
k.erklaerung("Korollar 5.66: Eine Probe genügt", G(r"""
## $AB = \mathbb{I}_n$ reicht

**Korollar 5.66.** Für $A, B \in K^{n \times n}$ folgt aus $AB = \mathbb{I}_n$ schon $BA = \mathbb{I}_n$ und $B = A^{-1}$.

*Beweis.* Aus $AB = \mathbb{I}_n$ folgt $A(By) = y$ für jedes $y$: $f_A$ ist surjektiv, nach Satz 5.23 auch injektiv, also $A$ invertierbar (Satz 5.61). Dann $B = \mathbb{I}_n B = (A^{-1}A)B = A^{-1}(AB) = A^{-1}$. $\square$

:::achtung Quadratisch ist wesentlich (Bsp. 5.67)
Für $A = \begin{pmatrix}1 & 0\end{pmatrix} \in \mathbb{R}^{1 \times 2}$ und $B = \begin{pmatrix}1\\0\end{pmatrix} \in \mathbb{R}^{2 \times 1}$ gilt $AB = \mathbb{I}_1$, aber $BA \neq \mathbb{I}_2$.
:::

""") + R([
    (r"AB = \begin{pmatrix}1 & 0\end{pmatrix}\begin{pmatrix}1\\0\end{pmatrix} = (1) = \mathbb{I}_1", "$(1 \\times 2)(2 \\times 1) = (1 \\times 1)$"),
    (r"BA = \begin{pmatrix}1\\0\end{pmatrix}\begin{pmatrix}1 & 0\end{pmatrix} = \begin{pmatrix}1 & 0\\0 & 0\end{pmatrix} \neq \mathbb{I}_2", "$(2 \\times 1)(1 \\times 2) = (2 \\times 2)$: die zweite Koordinate geht verloren"),
], "Warum quadratisch nötig ist", frei=True) + G(r"""

:::alt Als Einbahnstraße
$B$ bettet $\mathbb{R}$ in $\mathbb{R}^2$ ein, $A$ nimmt die erste Koordinate. Hin und zurück kommst du wieder an, zurück und hin nicht: Die zweite Koordinate ist weg. Bei quadratischen Matrizen kann so etwas nicht passieren.
:::
"""))

k.ordnen("Ordne den Beweis von Korollar 5.66: Aus $AB = \\mathbb{I}_n$ folgt $B = A^{-1}$ und $BA = \\mathbb{I}_n$.",
         ["Aus $AB = \\mathbb{I}_n$ folgt $A(By) = y$ für jedes $y \\in K^n$.",
          "Also hat jedes $y$ unter $f_A$ das Urbild $By$: $f_A$ ist surjektiv.",
          "Nach Satz 5.23 (gleiche Dimension) ist $f_A$ auch injektiv, nach Satz 5.61 ist $A$ invertierbar.",
          "Damit gilt $B = \\mathbb{I}_n B = (A^{-1}A)B = A^{-1}(AB) = A^{-1}\\mathbb{I}_n = A^{-1}$.",
          "Insbesondere ist $BA = A^{-1}A = \\mathbb{I}_n$. $\\square$"],
         "Erst Surjektivität, dann Injektivität über die Dimension, dann invertierbar, dann $B = A^{-1}$.",
         ablenker=["Weil Matrizen kommutieren, folgt $BA = AB = \\mathbb{I}_n$.", "Da $\\det A \\neq 0$ ist, existiert $A^{-1}$."],
         tipps=["Surjektivität lässt sich direkt ablesen: Welches Urbild hat $y$?", "Wo wird benutzt, dass $A$ quadratisch ist?", "Matrizen kommutieren nicht, Determinanten gibt es erst in Kapitel 6."])

k.wf("Für Matrizen $A \\in K^{m \\times n}$ und $B \\in K^{n \\times m}$ mit $m \\neq n$ folgt aus $AB = \\mathbb{I}_m$ immer $BA = \\mathbb{I}_n$.", False,
     "Beispiel 5.67: $A = (1\\ 0)$ und $B = (1, 0)^\\top$ haben $AB = \\mathbb{I}_1$, aber $BA = \\begin{pmatrix}1 & 0\\\\ 0 & 0\\end{pmatrix} \\neq \\mathbb{I}_2$. Der Beweis von Korollar 5.66 braucht gleiche Dimension von Definitions- und Zielraum.",
     tipps=["Teste $A = (1\\ 0)$ und $B = (1, 0)^\\top$."])

# ── Seite 6: Inverse ausrechnen ─────────────────────────────────────────────
k.erklaerung("Inverse ausrechnen: 2×2 und Gauß-Jordan", G(r"""
## Zwei Wege zur Inversen

**Spalten lösen.** Die Spalten von $A^{-1}$ sind die Lösungen $x$ von $Ax = e^{(j)}$, denn $A A^{-1}_{\cdot j} = \mathbb{I}_{\cdot j} = e^{(j)}$. Das macht das <<Gauß-Verfahren|Gauß-Verfahren>> gleichzeitig für alle $e^{(j)}$: $(A \mid \mathbb{I}_n) \to (\mathbb{I}_n \mid A^{-1})$.

**Formel $2 \times 2$.** Für $A = \begin{pmatrix}a & b\\ c & d\end{pmatrix}$ mit $ad - bc \neq 0$ gilt $A^{-1} = \frac{1}{ad - bc}\begin{pmatrix}d & -b\\ -c & a\end{pmatrix}$. Probe genügt (Kor. 5.66). Bei $ad - bc = 0$ sind die Spalten linear abhängig, $A$ ist nicht invertierbar.

:::visual gauss
{"matrix": [[2, 1, 1, 0], [5, 3, 0, 1]],
 "unterschrift": "$(A \\mid \\mathbb{I}_2)$ mit $A = \\begin{pmatrix}2 & 1\\\\ 5 & 3\\end{pmatrix}$ wird zu $(\\mathbb{I}_2 \\mid A^{-1})$. Rechts steht am Ende $\\begin{pmatrix}3 & -1\\\\ -5 & 2\\end{pmatrix}$."}
:::

""") + R([
    (r"ad - bc = 2 \cdot 3 - 1 \cdot 5 = 1", "$A = \\begin{pmatrix}2 & 1\\\\ 5 & 3\\end{pmatrix}$: Nenner $\\neq 0$"),
    (r"A^{-1} = \frac11\begin{pmatrix}3 & -1\\-5 & 2\end{pmatrix}", "$d$ und $a$ tauschen, $b$ und $c$ bekommen ein Minus"),
    (r"AA^{-1} = \begin{pmatrix}2 \cdot 3 - 5 & -2 + 2\\15 - 15 & -5 + 6\end{pmatrix} = \mathbb{I}_2", "Probe"),
], "Inverse einer $2 \\times 2$-Matrix", frei=True) + G(r"""

:::alt Als Zeigerwechsel
Bei $2 \times 2$ vertauscht du die Diagonale, wechselst das Vorzeichen der Nebendiagonale und teilst durch die Zahl $ad - bc$. Fehlt die Division, stimmt die Probe nur zufällig.
:::
"""))

k.matrix("Bestimme die Inverse von $A = \\begin{pmatrix}2 & 1\\\\ 5 & 3\\end{pmatrix}$.", ints(inv([[2, 1], [5, 3]])),
         "$ad - bc = 6 - 5 = 1$, also $A^{-1} = \\begin{pmatrix}3 & -1\\\\ -5 & 2\\end{pmatrix}$. Probe: $AA^{-1} = \\begin{pmatrix}6 - 5 & -2 + 2\\\\ 15 - 15 & -5 + 6\\end{pmatrix} = \\mathbb{I}_2$.",
         tipps=["Formel: Diagonale tauschen, Nebendiagonale mit Minus, durch $ad - bc$ teilen.", "$ad - bc = 2 \\cdot 3 - 1 \\cdot 5 = 1$.", "Die Probe $AA^{-1} = \\mathbb{I}_2$ zeigt dir, ob es stimmt."],
         rechenweg=R([(r"ad - bc = 1", "Nenner"), (r"A^{-1} = \begin{pmatrix}3 & -1\\-5 & 2\end{pmatrix}", "Formel")], frei=True),
         typische_fehler=[([[3, 1], [5, 2]], "Die Vorzeichen der Nebendiagonale fehlen: $b$ und $c$ bekommen ein Minus."),
                          ([[3, -5], [-1, 2]], "Das ist die Transponierte der Inversen: Die Einträge $b$ und $c$ stehen vertauscht. Probe: $AA^{-1} \\neq \\mathbb{I}_2$."),
                          ([[2, 5], [1, 3]], "Das ist $A^\\top$. Probe: $AA^\\top \\neq \\mathbb{I}_2$.")])

k.matrix("Bestimme die Inverse von $A = \\begin{pmatrix}1 & 2\\\\ 3 & 4\\end{pmatrix}$ (mit Brüchen: Eingabe `1/2` o. ä.).", ints(inv([[1, 2], [3, 4]])),
         "$ad - bc = 4 - 6 = -2$. Also $A^{-1} = \\frac{1}{-2}\\begin{pmatrix}4 & -2\\\\ -3 & 1\\end{pmatrix} = \\begin{pmatrix}-2 & 1\\\\ \\frac32 & -\\frac12\\end{pmatrix}$.",
         tipps=["Rechne zuerst $ad - bc$.", "Das Matrix-Muster ist $\\begin{pmatrix}d & -b\\\\ -c & a\\end{pmatrix}$.", "Teile jeden Eintrag durch $-2$."],
         rechenweg=R([(r"ad - bc = 1 \cdot 4 - 2 \cdot 3 = -2", "Nenner"),
                      (r"A^{-1} = -\frac12\begin{pmatrix}4 & -2\\-3 & 1\end{pmatrix} = \begin{pmatrix}-2 & 1\\\frac32 & -\frac12\end{pmatrix}", "Formel")], frei=True),
         typische_fehler=[([[4, -2], [-3, 1]], "Die Division durch $ad - bc = -2$ fehlt."),
                          ([[2, -1], [F(-3, 2), F(1, 2)]], "Das Vorzeichen des Nenners: $ad - bc = -2$, nicht $+2$.")])

k.wf("$A = \\begin{pmatrix}2 & 4\\\\ 1 & 2\\end{pmatrix}$ ist invertierbar.", False,
     "Es gilt $ad - bc = 4 - 4 = 0$. Die erste Spalte ist die Hälfte der zweiten, also $A(2, -1)^\\top = 0$ und $\\ker A \\neq \\{0\\}$. Nach Satz 5.65 ist $A$ nicht invertierbar.",
     tipps=["Rechne $ad - bc$.", "Sind die Spalten Vielfache voneinander?"])

# ── Seite 7: Satz 5.68, Beobachtung 5.69 ────────────────────────────────────
k.erklaerung("Satz 5.68 und Beobachtung 5.69: GL_n(K)", G(r"""
## Rechenregeln für Inverse

**Satz 5.68.** Sind $A, B \in K^{n \times n}$ invertierbar, so auch $AB$, $A^{-1}$ und $A^\top$, und
$$(AB)^{-1} = B^{-1}A^{-1}, \qquad (A^{-1})^{-1} = A, \qquad (A^\top)^{-1} = (A^{-1})^\top.$$
(Beweis: Übung.) Die Reihenfolge kehrt sich um wie beim Ausziehen von Schuhen und Socken.

**Beobachtung 5.69.** $\mathrm{GL}_n(K) := \{A \in K^{n \times n} \mid A \text{ invertierbar}\}$ ist mit der Multiplikation eine Gruppe mit neutralem Element $\mathbb{I}_n$: die [[allgemeine lineare Gruppe]].

""") + R([
    (r"A = \begin{pmatrix}1 & -1\\0 & 1\end{pmatrix},\ B = \begin{pmatrix}2 & 1\\1 & 1\end{pmatrix},\ AB = \begin{pmatrix}1 & 0\\1 & 1\end{pmatrix}", "zwei invertierbare Matrizen und ihr Produkt"),
    (r"(AB)^{-1} = \begin{pmatrix}1 & 0\\-1 & 1\end{pmatrix}", "Formel oder Rechnen"),
    (r"B^{-1}A^{-1} = \begin{pmatrix}1 & -1\\-1 & 2\end{pmatrix}\begin{pmatrix}1 & 1\\0 & 1\end{pmatrix} = \begin{pmatrix}1 & 0\\-1 & 1\end{pmatrix}", "stimmt; $A^{-1}B^{-1}$ wäre falsch"),
], "$(AB)^{-1} = B^{-1}A^{-1}$ an einem Beispiel", frei=True) + G(r"""

:::alt Als Anziehen
Erst Socken, dann Schuhe: $AB$. Ausziehen läuft rückwärts: erst die Schuhe (also $B^{-1}$ als Erstes), dann die Socken. Die Summe zweier invertierbarer Matrizen ist dagegen nicht immer invertierbar: $\mathbb{I}_2 + (-\mathbb{I}_2) = O$.
:::
"""))

k.matrix("Sei $A^{-1} = \\begin{pmatrix}1 & 1\\\\ 0 & 1\\end{pmatrix}$ und $B^{-1} = \\begin{pmatrix}1 & -1\\\\ -1 & 2\\end{pmatrix}$. Bestimme $(AB)^{-1}$.",
         ints(mul([[1, -1], [-1, 2]], [[1, 1], [0, 1]])),
         "$(AB)^{-1} = B^{-1}A^{-1} = \\begin{pmatrix}1 & -1\\\\ -1 & 2\\end{pmatrix}\\begin{pmatrix}1 & 1\\\\ 0 & 1\\end{pmatrix} = \\begin{pmatrix}1 & 0\\\\ -1 & 1\\end{pmatrix}$.",
         tipps=["Satz 5.68: Die Reihenfolge kehrt sich um.", "Rechne $B^{-1}A^{-1}$, nicht $A^{-1}B^{-1}$.", "Zeile $1$ von $B^{-1}$ mal die Spalten von $A^{-1}$: $(1, 1 - 1)$."],
         rechenweg=R([(r"(AB)^{-1} = B^{-1}A^{-1}", "Satz 5.68"),
                      (r"= \begin{pmatrix}1 & -1\\-1 & 2\end{pmatrix}\begin{pmatrix}1 & 1\\0 & 1\end{pmatrix} = \begin{pmatrix}1 & 1 - 1\\-1 & -1 + 2\end{pmatrix} = \begin{pmatrix}1 & 0\\-1 & 1\end{pmatrix}", "Zeile mal Spalte")], frei=True),
         typische_fehler=[(ints(mul([[1, 1], [0, 1]], [[1, -1], [-1, 2]])), "Das ist $A^{-1}B^{-1}$. Beim Invertieren kehrt sich die Reihenfolge um: $(AB)^{-1} = B^{-1}A^{-1}$.")])

k.mehrfach("Welche Aussagen über $\\mathrm{GL}_n(K)$ stimmen (Beobachtung 5.69, Satz 5.68)?",
           ["Das Produkt zweier Elemente liegt wieder in $\\mathrm{GL}_n(K)$", "$\\mathbb{I}_n$ ist das neutrale Element", "Zu jedem $A$ liegt $A^{-1}$ wieder in $\\mathrm{GL}_n(K)$"],
           ["Die Summe zweier Elemente liegt wieder in $\\mathrm{GL}_n(K)$", "Für $n \\ge 2$ ist $\\mathrm{GL}_n(K)$ abelsch"],
           "Abgeschlossen unter Produkt und Inversen, neutrales Element $\\mathbb{I}_n$: Gruppe. Die Summe $\\mathbb{I}_2 + (-\\mathbb{I}_2) = O$ ist nicht invertierbar, und $AB \\neq BA$ gibt es schon in $\\mathrm{GL}_2$ (z. B. Spiegelung und Vertauschung).",
           tipps=["Prüfe die Gruppenaxiome: Abgeschlossenheit, neutrales Element, Inverse, Assoziativität.", "Kann eine Summe invertierbarer Matrizen null sein?"],
           fehler={"Die Summe zweier Elemente liegt wieder in $\\mathrm{GL}_n(K)$": "$\\mathbb{I}_2 + (-\\mathbb{I}_2) = O$ ist nicht invertierbar.",
                   "Für $n \\ge 2$ ist $\\mathrm{GL}_n(K)$ abelsch": "$C = \\mathrm{diag}(1, -1)$ und $\\begin{pmatrix}0 & 1\\\\ 1 & 0\\end{pmatrix}$ liegen in $\\mathrm{GL}_2$, kommutieren aber nicht."})

# ── Praxis ──────────────────────────────────────────────────────────────────
k.praxis()


def inverse_2x2(rng):
    while True:
        a, b, c, d = (rng.randint(-3, 4) for _ in range(4))
        det = a * d - b * c
        if det in (1, -1, 2, -2, 3):
            break
    A = [[a, b], [c, d]]
    Ai = ints(inv(A))
    kandidaten = [([[d, -b], [-c, a]], "Die Division durch $ad - bc$ fehlt."),
                  ([[d, b], [c, a]], "Die Vorzeichen der Nebendiagonale fehlen: $b$ und $c$ bekommen ein Minus."),
                  (tr(Ai), "Das ist die Transponierte der Inversen: Probe $AA^{-1} = \\mathbb{I}_2$ schlägt fehl."),
                  ([[F(x, 1) / det for x in (d, -b)], [F(x, 1) / det for x in (c, a)]], "Bei der unteren Zeile muss $-c$ stehen, nicht $c$.")]
    fehler = ohne_gleiche_m(Ai, kandidaten)
    return {"frage": f"Bestimme die Inverse von $A = {M(A)}$. Brüche gibst du als `1/2` ein.",
            "loesung": Ai,
            "tipps": ["Rechne zuerst $ad - bc$. Ist es $0$, gibt es keine Inverse.", "Die Inverse ist $\\frac{1}{ad - bc}\\begin{pmatrix}d & -b\\\\ -c & a\\end{pmatrix}$.",
                      f"Hier ist $ad - bc = {det}$. Teile jeden Eintrag von $\\begin{{pmatrix}}{d} & {-b}\\\\ {-c} & {a}\\end{{pmatrix}}$ durch ${det}$."],
            "rechenweg": R([(f"ad - bc = {a} \\cdot {d} - {mathlib.tex_klammer(b)} \\cdot {mathlib.tex_klammer(c)} = {det}", "Nenner $\\neq 0$: invertierbar (Satz 5.65)"),
                            (f"A^{{-1}} = \\frac{{1}}{{{det}}}{M([[d, -b], [-c, a]])} = {M(Ai)}", "Formel für $2 \\times 2$"),
                            (f"AA^{{-1}} = {M(mul(A, Ai))}", "Probe")], frei=True),
            "erklaerung": "Für $2 \\times 2$ gilt $A^{-1} = \\frac{1}{ad - bc}\\begin{pmatrix}d & -b\\\\ -c & a\\end{pmatrix}$, die Probe $AA^{-1} = \\mathbb{I}_2$ genügt nach Kor. 5.66.",
            "typische_fehler": fehler}


def inverse_3x3(rng):
    # A = L U mit ganzzahligen Einheits-Dreiecksmatrizen: det = 1, Inverse ganzzahlig
    while True:
        L = [[1, 0, 0], [rng.randint(-2, 2), 1, 0], [rng.randint(-2, 2), rng.randint(-2, 2), 1]]
        U = [[1, rng.randint(-2, 2), rng.randint(-2, 2)], [0, 1, rng.randint(-2, 2)], [0, 0, 1]]
        A = mul(L, U)
        if sum(1 for z in A for x in z if x == 0) <= 3 and A != mathlib.einheitsmatrix(3):
            break
    A = ints(A)
    Ai = ints(inv(A))
    g = mathlib.gauss([z + e for z, e in zip(A, mathlib.einheitsmatrix(3))], None, reduziert=True)
    zeilen = [(M(s["matrix"]), f"${s['op']}$" if s["op"] != "Start" else "Start: $(A \\mid \\mathbb{I}_3)$ nebeneinander geschrieben") for s in g["schritte"]][:8]
    kandidaten = [(tr(Ai), "Das ist die Transponierte der Inversen. Probe: $AA^{-1}$ ist dann nicht $\\mathbb{I}_3$."),
                  ([[-x for x in z] for z in Ai], "Alle Vorzeichen sind umgedreht: Das ist $-A^{-1}$."),
                  ([list(z) for z in Ai[::-1]], "Die Zeilen stehen in umgekehrter Reihenfolge.")]
    fehler = ohne_gleiche_m(Ai, kandidaten)
    return {"frage": f"Bestimme die Inverse von $A = {M(A)}$ (Gauß-Jordan auf $(A \\mid \\mathbb{{I}}_3)$ oder spaltenweise).",
            "loesung": Ai,
            "tipps": ["Schreibe $(A \\mid \\mathbb{I}_3)$ nebeneinander und bringe links die Einheitsmatrix hervor.",
                      "Eliminiere erst unter der Diagonale, dann darüber. Rechts wird dieselbe Umformung mitgemacht.",
                      f"Zur Kontrolle: Die Inverse hat die Spur {sum(Ai[i][i] for i in range(3))} (Summe der Diagonaleinträge)."],
            "rechenweg": R(zeilen + [(f"A^{{-1}} = {M(Ai)}", "rechts steht am Ende die Inverse"), (f"AA^{{-1}} = {M(mul(A, Ai))}", "Probe")], frei=True),
            "erklaerung": "Das Gauß-Jordan-Verfahren löst gleichzeitig $Ax = e^{(1)}$, $Ax = e^{(2)}$, $Ax = e^{(3)}$. Die Lösungen sind die Spalten von $A^{-1}$.",
            "typische_fehler": fehler}


def invertierbar_pruefen(rng):
    n = rng.choice([2, 3])
    invertierbar = rng.random() < 0.5
    r = n if invertierbar else n - 1
    while True:
        basis = [[rng.randint(-2, 3) for _ in range(n)] for _ in range(r)]
        zeilen = [b[:] for b in basis]
        while len(zeilen) < n:
            koef = [rng.randint(-1, 2) for _ in range(r)]
            zeilen.append([sum(c * basis[j][s] for j, c in enumerate(koef)) for s in range(n)])
        rng.shuffle(zeilen)
        if mathlib.rang(zeilen) == r:
            break
    A = zeilen
    ja = "ja: $\\mathrm{rang}\\, A = n$, die Spalten sind eine Basis"
    nein = "nein: $\\mathrm{rang}\\, A < n$, es gibt $x \\neq 0$ mit $Ax = 0$"
    ja2 = "ja, weil $A$ keine Nullzeile hat"
    loesung = ja if invertierbar else nein
    grund = (f"Der Rang ist ${r}$. " + ("Das ist gleich $n$: invertierbar (Satz 5.65 (iii))." if invertierbar
                                      else f"Das ist kleiner als $n = {n}$: Der Kern enthält einen Vektor $\\neq 0$, also nicht invertierbar."))
    g = mathlib.gauss(A, reduziert=False)
    optionen = [loesung] + [o for o in (ja, nein, ja2) if o != loesung]
    return {"typ": "mc", "frage": f"Ist $A = {M(A)}$ invertierbar?",
            "optionen": optionen, "fehler": {o: "Das stimmt nicht. " + grund for o in optionen[1:]},
            "tipps": ["Satz 5.65: $A$ ist genau dann invertierbar, wenn $\\mathrm{rang}\\, A = n$.", "Bringe $A$ mit dem Gauß-Verfahren auf Stufenform und zähle die Zeilen $\\neq 0$.",
                      "Ist eine Zeile ein Vielfaches oder eine Summe anderer Zeilen, sinkt der Rang."],
            "rechenweg": R([(f"A \\to {M(g['ergebnis'])}", "Zeilenstufenform"), (f"\\mathrm{{rang}}\\, A = {r}", f"Pivots zählen; $n = {n}$")], frei=True),
            "erklaerung": grund}


def inverse_produkt(rng):
    def zufall():
        while True:
            a, b, c, d = (rng.randint(-2, 3) for _ in range(4))
            if a * d - b * c in (1, -1):
                return [[a, b], [c, d]]
    A, B = zufall(), zufall()
    Ai, Bi = ints(inv(A)), ints(inv(B))
    erg = ints(mul(Bi, Ai))
    fehler = ohne_gleiche_m(erg, [(ints(mul(Ai, Bi)), "Das ist $A^{-1}B^{-1}$. Beim Invertieren kehrt sich die Reihenfolge um: $(AB)^{-1} = B^{-1}A^{-1}$."),
                                (ints(mul(A, B)), "Das ist $AB$ selbst, nicht seine Inverse."),
                                (ints(tr(mul(Bi, Ai))), "Das ist die Transponierte. Probe: Multipliziere mit $AB$."),
                                  ([[-x for x in z] for z in erg], "Alle Vorzeichen sind umgedreht: Das ist $-(AB)^{-1}$. Probe: Multipliziere mit $AB$."),
                                  ([list(z) for z in erg[::-1]], "Die Zeilen stehen in umgekehrter Reihenfolge. Probe: Multipliziere mit $AB$.")])
    return {"frage": f"Gegeben sind $A^{{-1}} = {M(Ai)}$ und $B^{{-1}} = {M(Bi)}$. Bestimme $(AB)^{{-1}}$.",
            "loesung": erg,
            "tipps": ["Satz 5.68: $(AB)^{-1} = B^{-1}A^{-1}$ (Reihenfolge umkehren).", "Du musst $A$ und $B$ nicht ausrechnen.",
                      f"Rechne $B^{{-1}} A^{{-1}}$: Zeile $1$ von $B^{{-1}}$ mal Spalte $1$ von $A^{{-1}}$."],
            "rechenweg": R([(f"(AB)^{{-1}} = B^{{-1}}A^{{-1}} = {M(Bi)}{M(Ai)}", "Satz 5.68"), (f"= {M(erg)}", "Zeile mal Spalte")], frei=True),
            "erklaerung": "Das Inverse eines Produkts ist das Produkt der Inversen in umgekehrter Reihenfolge (Satz 5.68).",
            "typische_fehler": fehler}


k.generator(inverse_2x2, typ="matrix", titel="Inverse einer 2×2-Matrix")
k.generator(inverse_3x3, typ="matrix", titel="Inverse einer 3×3-Matrix (Gauß-Jordan)")
k.generator(invertierbar_pruefen, typ="mc", titel="Ist die Matrix invertierbar?")
k.generator(inverse_produkt, typ="matrix", titel="Inverse eines Produkts")

k.rechenweg_aufgabe(r"""
## Quiz-Stil: Zurück vom Funktionswert zur Funktion

Sei $\mathcal{F}$ der Raum der Funktionen $f(t) = a + bt$ mit Basis $\mathfrak{B} = (1, t)$ (Beispiele 5.36 und 5.64) und $T\colon \mathcal{F} \to \mathbb{R}^2,\ f \mapsto (f(1), f(3))^\top$. Dann gilt
$[T]_{\mathcal{E} \leftarrow \mathfrak{B}} = \begin{pmatrix}1 & 1\\ 1 & 3\end{pmatrix}$.
""",
    [{"typ": "zahl", "frage": "Berechne $ad - bc$ für diese Matrix.", "loesung": 2,
      "tipps": ["Die Matrix ist $\\begin{pmatrix}a & b\\\\ c & d\\end{pmatrix}$.", "$a = 1$, $b = 1$, $c = 1$, $d = 3$."], "rechenweg": "$1 \\cdot 3 - 1 \\cdot 1 = 2$.",
      "typische_fehler": [(4, "Das ist $ad + bc = 3 + 1$. Es heißt $ad - bc$.")]},
     {"typ": "matrix", "frage": "Bestimme $[T^{-1}]_{\\mathfrak{B} \\leftarrow \\mathcal{E}} = ([T]_{\\mathcal{E} \\leftarrow \\mathfrak{B}})^{-1}$ (Korollar 5.63).",
      "loesung": inv(_TT),
      "tipps": ["Formel: $\\frac{1}{ad - bc}\\begin{pmatrix}d & -b\\\\ -c & a\\end{pmatrix}$.", "Teile die Matrix $\\begin{pmatrix}3 & -1\\\\ -1 & 1\\end{pmatrix}$ durch $2$."],
      "rechenweg": "$\\frac12\\begin{pmatrix}3 & -1\\\\ -1 & 1\\end{pmatrix} = \\begin{pmatrix}\\frac32 & -\\frac12\\\\ -\\frac12 & \\frac12\\end{pmatrix}$.",
      "typische_fehler": [([[3, -1], [-1, 1]], "Die Division durch $ad - bc = 2$ fehlt.")]},
     {"typ": "vektor", "frage": "Bestimme die Koordinaten $(a, b)^\\top = [f]_{\\mathfrak{B}}$ der Funktion $f$ mit $f(1) = 4$ und $f(3) = 10$.", "loesung": [1, 3],
      "tipps": ["Multipliziere die Inverse mit $(4, 10)^\\top$.", "Zweite Zeile: $-\\frac12 \\cdot 4 + \\frac12 \\cdot 10$."],
      "rechenweg": "$a = \\frac32 \\cdot 4 - \\frac12 \\cdot 10 = 1$, $b = -\\frac12 \\cdot 4 + \\frac12 \\cdot 10 = 3$, also $f(t) = 1 + 3t$.",
      "typische_fehler": [([4, 10], "Das sind die Funktionswerte, nicht die Koordinaten $a, b$.")]}],
    "$f(t) = 1 + 3t$. Probe: $f(1) = 4$, $f(3) = 10$. Die inverse Darstellungsmatrix macht aus Funktionswerten wieder Koeffizienten.",
    uebungsblatt=True,
    tipps=["$ad - bc$ steckt im Nenner der Inversen.", "Satz 5.40: Koordinaten $= $ Inverse mal Werte.", "Mach am Ende die Probe $f(1) = 4$, $f(3) = 10$."],
    rechenweg=r"""
:::rechnung
?? ad - bc = 1 \cdot 3 - 1 \cdot 1 = 2 || Nenner der Inversen
?? [T^{-1}] = \frac12\begin{pmatrix}3 & -1\\-1 & 1\end{pmatrix} || Formel für $2 \times 2$
?? [f]_{\mathfrak{B}} = [T^{-1}]\begin{pmatrix}4\\10\end{pmatrix} = \begin{pmatrix}1\\3\end{pmatrix} || Satz 5.40
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Satz 5.68 und Beobachtung 5.69 (im Skript „Übung“)

Seien $A, B \in K^{n \times n}$ invertierbar.

1. Zeigen Sie, dass $AB$ invertierbar ist mit $(AB)^{-1} = B^{-1}A^{-1}$.
2. Zeigen Sie, dass $A^{-1}$ invertierbar ist mit $(A^{-1})^{-1} = A$.
3. Zeigen Sie, dass $(\mathrm{GL}_n(K), \cdot)$ eine Gruppe ist.
""",
    r"""
**1.** Nach Kor. 5.50 gilt $(B^{-1}A^{-1})(AB) = B^{-1}(A^{-1}A)B = B^{-1}\mathbb{I}_nB = \mathbb{I}_n$ und $(AB)(B^{-1}A^{-1}) = A(BB^{-1})A^{-1} = A A^{-1} = \mathbb{I}_n$. Also ist $B^{-1}A^{-1}$ eine Inverse von $AB$; wegen der Eindeutigkeit (Beob. 5.60) die Inverse.

**2.** $A^{-1}A = AA^{-1} = \mathbb{I}_n$ sagt gerade, dass $A$ eine Inverse von $A^{-1}$ ist. Wegen der Eindeutigkeit ist $(A^{-1})^{-1} = A$.

**3.** Abgeschlossenheit: Teil 1. Assoziativität: Kor. 5.50. Neutrales Element: $\mathbb{I}_n \mathbb{I}_n = \mathbb{I}_n$, also $\mathbb{I}_n \in \mathrm{GL}_n(K)$, und $\mathbb{I}_n A = A = A\mathbb{I}_n$. Inverse: $A^{-1} \in \mathrm{GL}_n(K)$ nach Teil 2, und $A^{-1}A = \mathbb{I}_n$. $\square$
""",
    ["Bei 1 beide Gleichungen $(B^{-1}A^{-1})(AB) = \\mathbb{I}_n$ und $(AB)(B^{-1}A^{-1}) = \\mathbb{I}_n$ nachgerechnet",
     "Bei 1 oder 2 die Eindeutigkeit der Inversen (Beob. 5.60) genannt",
     "Bei 2 erkannt, dass $A$ selbst die Inverse von $A^{-1}$ ist",
     "Bei 3 alle vier Gruppenaxiome (Abgeschlossenheit, Assoziativität, neutrales Element, Inverse) genannt"],
    "Man zeigt Invertierbarkeit, indem man eine Matrix mit beiden Produkten $= \\mathbb{I}_n$ angibt, und beruft sich dann auf die Eindeutigkeit.",
    uebungsblatt=True,
    tipps=["Rate die Inverse von $AB$ und rechne beide Produkte nach.", "Klammern mit der Assoziativität umsetzen."])

k.papier(r"""
## Satz 5.65 beweisen: (i) $\iff$ (ii) $\iff$ (iii)

Sei $A \in K^{n \times n}$. Zeigen Sie unter Verwendung von Satz 5.61, 5.23 und der Dimensionsformel die Äquivalenz von (i) $A$ invertierbar, (ii) $\ker A = \{0\}$, (iii) $\mathrm{rang}\, A = n$.
""",
    r"""
Nach Satz 5.61 ist (i) gleichwertig zur Bijektivität von $f_A\colon K^n \to K^n$. Weil Definitions- und Zielraum dieselbe Dimension $n$ haben, ist $f_A$ nach Satz 5.23 genau dann bijektiv, wenn $f_A$ injektiv ist, und genau dann, wenn $f_A$ surjektiv ist.

(i) $\iff$ (ii): $f_A$ ist genau dann injektiv, wenn $\ker(f_A) = \{0\}$ (Beob. 5.17), also $\ker A = \{0\}$.

(i) $\iff$ (iii): $f_A$ ist genau dann surjektiv, wenn $f_A(K^n) = K^n$, nach Satz 4.74 genau dann, wenn $\dim f_A(K^n) = n$, also $\mathrm{rang}\, A = n$. $\square$
""",
    ["Satz 5.61 (invertierbar $\\iff$ $f_A$ bijektiv) als Ausgangspunkt genannt",
     "Satz 5.23 benutzt: bei gleicher Dimension genügt injektiv oder surjektiv",
     "(ii) über das Kernkriterium (Beob. 5.17) begründet",
     "(iii) über die Dimension des Bildes und Satz 4.74 begründet"],
    "Bijektiv, injektiv, surjektiv sind bei $f_A\\colon K^n \\to K^n$ gleichwertig. Injektiv liefert den Kern, surjektiv den Rang.",
    tipps=["Welche Eigenschaft von $f_A$ steckt hinter jedem der drei Punkte?"])

k.zusammenfassung(G(r"""
## Invertierbarkeit (Skript Abschn. 5.5)

- **Invertierbar** (Def. 5.59): $A \in K^{n \times n}$ mit $B$, $AB = BA = \mathbb{I}_n$. Die Inverse $A^{-1}$ ist **eindeutig** (Beob. 5.60: $B = B\mathbb{I}_n = B(AC) = (BA)C = C$).
- **Satz 5.61:** $A$ invertierbar $\iff$ $f_A$ Automorphismus, $f_{A^{-1}} = (f_A)^{-1}$. **Kor. 5.63:** $[f^{-1}]_{\mathfrak{B} \leftarrow \mathfrak{C}} = ([f]_{\mathfrak{C} \leftarrow \mathfrak{B}})^{-1}$.
- **Satz 5.65:** invertierbar $\iff$ $\ker A = \{0\}$ $\iff$ $\mathrm{rang}\, A = n$ $\iff$ Spalten bilden eine Basis von $K^n$.
- **Kor. 5.66:** Für quadratische Matrizen folgt aus $AB = \mathbb{I}_n$ schon $BA = \mathbb{I}_n$ (nicht für nicht quadratische: Bsp. 5.67).
- **Inverse berechnen:** $2 \times 2$: $\frac{1}{ad - bc}\begin{pmatrix}d & -b\\ -c & a\end{pmatrix}$ (nicht invertierbar bei $ad - bc = 0$). Allgemein: $(A \mid \mathbb{I}_n) \to (\mathbb{I}_n \mid A^{-1})$. Immer mit $AA^{-1} = \mathbb{I}_n$ prüfen.
- **Satz 5.68:** $(AB)^{-1} = B^{-1}A^{-1}$, $(A^{-1})^{-1} = A$, $(A^\top)^{-1} = (A^{-1})^\top$. **Beob. 5.69:** $\mathrm{GL}_n(K)$ ist eine Gruppe.

!! Zum Prüfen einer Inversen reicht ein Produkt: $AB = \mathbb{I}_n$ bei quadratischen Matrizen genügt.
"""))
