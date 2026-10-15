# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 28: Basiswechsel und Ähnlichkeit, Bildcodierung (Skript Disser, Abschn. 5.6 und 5.7)."""
from .glossar import eintrag

eintrag("Basiswechselmatrix", "Zu geordneten Basen $\\mathfrak{B}, \\mathfrak{C}$ von $V$ die Matrix $S_{\\mathfrak{C} \\leftarrow \\mathfrak{B}} := [\\mathrm{id}_V]_{\\mathfrak{C} \\leftarrow \\mathfrak{B}}$ (Def. 5.71). "
        "Ihre Spalten sind die Koordinaten der alten Basisvektoren in der neuen Basis, und es gilt $[v]_{\\mathfrak{C}} = S_{\\mathfrak{C} \\leftarrow \\mathfrak{B}}[v]_{\\mathfrak{B}}$. "
        "Sie ist invertierbar mit $(S_{\\mathfrak{C} \\leftarrow \\mathfrak{B}})^{-1} = S_{\\mathfrak{B} \\leftarrow \\mathfrak{C}}$ (Kor. 5.73).",
        r"Für $\mathfrak{B} = ((1, 1)^\top, (1, 0)^\top)$ ist $S_{\mathcal{E} \leftarrow \mathfrak{B}} = \begin{pmatrix}1 & 1\\ 1 & 0\end{pmatrix}$.",
        "basiswechsel", ["Basiswechsel", "Transformationsmatrix", "Basiswechselmatrizen", "Koordinatenwechsel"])
eintrag("ähnliche Matrizen", "Zwei Matrizen $A, B \\in K^{n \\times n}$ heißen ähnlich, wenn es ein invertierbares $S$ gibt mit $B = S^{-1}AS$ (Def. 5.78). "
        "Das sind genau die Darstellungsmatrizen derselben linearen Abbildung $V \\to V$ bezüglich zwei Basen (Satz 5.79). Ähnlichkeit ist eine Äquivalenzrelation; "
        "ähnliche Matrizen haben denselben Rang und sind gleichzeitig invertierbar (Satz 5.81).",
        r"$P = \frac12\begin{pmatrix}1 & 1\\ 1 & 1\end{pmatrix}$ und $D = \begin{pmatrix}1 & 0\\ 0 & 0\end{pmatrix}$ sind ähnlich.",
        "basiswechsel", ["ähnlich", "Ähnlichkeit", "Ähnlichkeit von Matrizen", "ähnliche Matrix"])
eintrag("Haar-Transformation", "Koordinatenwechsel für zwei benachbarte Pixel $(a, b)^\\top$ zur Basis $((1, 1)^\\top, (1, -1)^\\top)$: neue Koordinaten sind der Mittelwert "
        "$m = \\frac{a + b}{2}$ und die halbe Differenz $d = \\frac{a - b}{2}$ (Abschn. 5.7). Sie ist umkehrbar ($a = m + d$, $b = m - d$) und Grundlage der Bildkompression.",
        r"$(0{,}40;\ 0{,}42)^\top \mapsto (0{,}41;\ -0{,}01)^\top$.",
        "basiswechsel", ["Haar-Wavelet", "Haar-Wavelet-Transformation", "Haar-Bildcodierung", "Bildcodierung", "Wavelet-Transformation"])
eintrag("Pixel", "Ein Bildpunkt eines digitalen Bildes. Im Skript hat ein Graustufen-Pixel einen Helligkeitswert in $[0, 1]$: $0$ ist schwarz, $1$ weiß. "
        "Ein Bild aus $w \\cdot h$ Pixeln ist ein Vektor in $\\mathbb{R}^{w \\cdot h}$.",
        r"Ein Bild aus vier Pixeln: $(0{,}40;\ 0{,}42;\ 0{,}80;\ 0{,}78)^\top$.",
        "basiswechsel", ["Bildpunkt", "Pixel (Bild)"])
eintrag("Schwellwert", "Ein Grenzwert $\\tau$, unterhalb dessen eine Größe als unwichtig gilt. Bei der Bildcodierung wird eine Differenz $d$ auf $0$ gesetzt, falls $|d| < \\tau$. "
        "Ein größerer Schwellwert spart mehr Speicher, verwirft aber auch größere Unterschiede.",
        r"Mit $\tau = 0{,}02$ wird $d = -0{,}01$ verworfen, $d = 0{,}05$ bleibt.",
        "basiswechsel", ["Schwelle", "Schwellenwert"])
