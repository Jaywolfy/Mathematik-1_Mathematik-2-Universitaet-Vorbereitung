# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 27: Invertierbarkeit (Skript Disser, Abschn. 5.5)."""
from .glossar import eintrag

eintrag("invertierbare Matrix", "Eine Matrix $A \\in K^{n \\times n}$ heißt invertierbar, wenn es $B \\in K^{n \\times n}$ gibt mit $AB = BA = \\mathbb{I}_n$ (Def. 5.59). "
        "Diese Inverse $A^{-1} := B$ ist eindeutig (Beob. 5.60). Gleichwertig: $\\ker A = \\{0\\}$, $\\mathrm{rang}\\, A = n$, die Spalten bilden eine Basis (Satz 5.65).",
        r"$\begin{pmatrix}2 & 1\\ 1 & 1\end{pmatrix}^{-1} = \begin{pmatrix}1 & -1\\ -1 & 2\end{pmatrix}$; die Projektion $P$ ist nicht invertierbar.",
        "invertierbarkeit", ["invertierbar", "Inverse einer Matrix", "inverse Matrix", "Matrixinverse", "reguläre Matrix", "regulär"])
eintrag("allgemeine lineare Gruppe", "Die Menge $\\mathrm{GL}_n(K) = \\{A \\in K^{n \\times n} \\mid A \\text{ ist invertierbar}\\}$ mit der Matrixmultiplikation ist eine Gruppe "
        "mit neutralem Element $\\mathbb{I}_n$ (Beob. 5.69). Für $n \\ge 2$ ist sie nicht abelsch.",
        r"$\mathrm{GL}_2(\mathbb{R})$ enthält die Spiegelung $C$, aber nicht die Projektion $P$.",
        "invertierbarkeit", ["GL_n(K)", "GLn(K)", "GL"])
