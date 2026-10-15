# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 26: Matrizen und Rechnen mit Matrizen (Skript Disser, Abschn. 5.3 und 5.4)."""
from .glossar import eintrag

eintrag("Matrix", "Eine $(m \\times n)$-Matrix über $K$ ist ein Tupel $A = (a^{(1)}, \\dots, a^{(n)}) \\in K^{m \\times n}$ von $n$ Spaltenvektoren aus $K^m$ (Def. 5.28). "
        "Eintrag $A_{ij}$ in Zeile $i$ und Spalte $j$, Spalte $A_{\\cdot j}$, Zeile $A_{i \\cdot}$.",
        r"$A = \begin{pmatrix}1 & 1 & 0\\ 0 & 0 & 1\end{pmatrix} \in \mathbb{R}^{2 \times 3}$ hat die Spalten $(1, 0)^\top, (1, 0)^\top, (0, 1)^\top$.",
        "matrizen_uni", ["Matrizen", "Zeile (Matrix)", "Spalte (Matrix)"])
eintrag("Matrix-Vektor-Produkt", "Für $A \\in K^{m \\times n}$ und $x \\in K^n$ ist $Ax := \\sum_{j=1}^n x_j A_{\\cdot j}$, eine Linearkombination der Spalten (Def. 5.29). "
        "Komponentenweise gilt $(Ax)_i = \\sum_j A_{ij} x_j$: Zeile mal Spalte.",
        r"$\begin{pmatrix}1 & 1 & 0\\ 0 & 0 & 1\end{pmatrix}\begin{pmatrix}x\\y\\z\end{pmatrix} = \begin{pmatrix}x + y\\ z\end{pmatrix}$.",
        "matrizen_uni", ["Matrixprodukt mit Vektor", "Produkt Matrix mal Vektor"])
eintrag("Darstellungsmatrix", "Zu $f\\colon V \\to W$ linear und geordneten Basen $\\mathfrak{B}$ von $V$, $\\mathfrak{C}$ von $W$ die Matrix "
        "$[f]_{\\mathfrak{C} \\leftarrow \\mathfrak{B}}$, deren $j$-te Spalte der Koordinatenvektor $[f(b^{(j)})]_{\\mathfrak{C}}$ ist (Def. 5.38). "
        "Sie übersetzt Koordinaten: $[f(v)]_{\\mathfrak{C}} = [f]_{\\mathfrak{C} \\leftarrow \\mathfrak{B}} [v]_{\\mathfrak{B}}$ (Satz 5.40).",
        r"Für $m_z\colon w \mapsto zw$ auf $\mathbb{C}$ mit Basis $(1, i)$ und $z = a + bi$ ist die Darstellungsmatrix $\begin{pmatrix}a & -b\\ b & a\end{pmatrix}$.",
        "matrizen_uni", ["Darstellungsmatrizen", "Abbildungsmatrix"])
eintrag("Matrixprodukt", "Für $A \\in K^{m \\times n}$ und $B \\in K^{n \\times r}$ ist $AB := (AB_{\\cdot 1}, \\dots, AB_{\\cdot r}) \\in K^{m \\times r}$ (Def. 5.46), "
        "also $(AB)_{ij} = \\sum_k A_{ik} B_{kj}$. Es entspricht der Verkettung: $f_{AB} = f_A \\circ f_B$ (Beob. 5.48). Im Allgemeinen gilt $AB \\neq BA$.",
        r"$\begin{pmatrix}1 & 2\\ 0 & 1\end{pmatrix}\begin{pmatrix}3 & 0\\ 1 & 2\end{pmatrix} = \begin{pmatrix}5 & 4\\ 1 & 2\end{pmatrix}$.",
        "matrizen_uni", ["Matrixmultiplikation", "Matrizenprodukt", "Matrizenmultiplikation", "Zeile mal Spalte"])
eintrag("Einheitsmatrix", "Die Matrix $\\mathbb{I}_n \\in K^{n \\times n}$ der Identität auf $K^n$ (Def. 5.45): Einsen auf der Diagonale, sonst Nullen. "
        "Ihre Spalten sind die Standardbasisvektoren, und es gilt $\\mathbb{I}_m A = A = A \\mathbb{I}_n$.",
        r"$\mathbb{I}_2 = \begin{pmatrix}1 & 0\\ 0 & 1\end{pmatrix}$.",
        "matrizen_uni", ["Identitätsmatrix", "Einheitsmatrizen"])
eintrag("Nullmatrix", "Die Matrix $O \\in K^{m \\times n}$, deren Einträge alle $0$ sind: der Nullvektor des Vektorraums $K^{m \\times n}$ (Beob. 5.43).",
        r"$O = \begin{pmatrix}0 & 0\\ 0 & 0\end{pmatrix}$; $A + O = A$.",
        "matrizen_uni", ["Nullmatrizen"])
eintrag("Transponierte", "Zu $A \\in K^{m \\times n}$ die Matrix $A^\\top \\in K^{n \\times m}$ mit $(A^\\top)_{ji} = A_{ij}$: Zeilen werden zu Spalten (Def. 5.54). "
        "Es gilt $(AB)^\\top = B^\\top A^\\top$ (Beob. 5.58), und $(u \\mid v) = u^\\top v$ für Vektoren.",
        r"$\begin{pmatrix}1 & 1 & 0\\ 0 & 0 & 1\end{pmatrix}^\top = \begin{pmatrix}1 & 0\\ 1 & 0\\ 0 & 1\end{pmatrix}$.",
        "matrizen_uni", ["transponierte Matrix", "Transposition", "Transponieren"])
eintrag("Matrixpotenz", "Für $A \\in K^{n \\times n}$ ist $A^0 := \\mathbb{I}_n$ und $A^{k+1} := A A^k$ (Def. 5.46): die $k$-fache Anwendung derselben Abbildung.",
        r"Für die Spiegelung $C = \mathrm{diag}(1, -1)$ gilt $C^2 = \mathbb{I}_2$, für die Projektion $P$ gilt $P^2 = P$.",
        "matrizen_uni", ["Matrixpotenzen", "Potenz einer Matrix"])
