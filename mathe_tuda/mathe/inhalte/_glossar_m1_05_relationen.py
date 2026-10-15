# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 5: Relationen (Skript Disser, Abschn. 1.6)."""
from .glossar import eintrag

eintrag("Relation", "Eine (binäre) Relation zwischen den Mengen $N$ und $M$ ist eine Teilmenge "
        "$R \\subseteq N \\times M$. Statt $(x, y) \\in R$ schreibt man $xRy$. Ist $N = M$, heißt $R$ Relation "
        "auf $M$ (Skript Disser, Def. 1.35).",
        r"Auf $\{1, 2, 3\}$ ist $R = \{(1, 2), (1, 3), (2, 3)\}$ die Relation „kleiner als“: $1R2$, aber nicht $2R1$.",
        "relationen", ["Relationen", "binäre Relation"])
eintrag("gerichteter Graph", "Bild einer Relation $R$ auf einer endlichen Menge $M$: ein Knoten (Punkt) für jedes "
        "Element, ein Pfeil (gerichtete Kante) von $a$ nach $b$ genau dann, wenn $aRb$ gilt. Ein Pfeil von $a$ "
        "zu sich selbst heißt Schleife.",
        r"$R = \{(1, 1), (1, 2)\}$ auf $\{1, 2\}$: Schleife an $1$, Pfeil $1 \to 2$, an $2$ nichts.",
        "relationen", ["gerichtete Graphen", "Pfeildiagramm"])
eintrag("reflexiv", "Eine Relation $R$ auf $X$ heißt reflexiv, wenn $\\forall x \\in X : xRx$. Im Graphen: Jeder "
        "Knoten hat eine Schleife (Def. 1.38 (i)).",
        r"$\le$ auf $\mathbb{N}$ ist reflexiv, $<$ nicht.",
        "relationen", ["Reflexivität"])
eintrag("symmetrisch", "Eine Relation $R$ auf $X$ heißt symmetrisch, wenn $\\forall x, y \\in X : (xRy \\Rightarrow yRx)$. "
        "Im Graphen: Zu jedem Pfeil gibt es den Gegenpfeil (Def. 1.38 (ii)).",
        r"„haben ein gemeinsames Element“ ist symmetrisch, $\le$ auf $\mathbb{N}$ nicht: $2 \le 5$, aber nicht $5 \le 2$.",
        "relationen", ["Symmetrie einer Relation", "symmetrische Relation"])
eintrag("antisymmetrisch", "Eine Relation $R$ auf $X$ heißt antisymmetrisch, wenn "
        "$\\forall x, y \\in X : ((xRy \\land yRx) \\Rightarrow x = y)$. Im Graphen: Zwischen zwei verschiedenen "
        "Knoten gibt es nie Pfeile in beide Richtungen (Def. 1.38 (iii)). Nicht dasselbe wie „nicht symmetrisch“.",
        r"$\le$ und $<$ auf $\mathbb{N}$ sind antisymmetrisch, ebenso $\subseteq$ auf einer Potenzmenge.",
        "relationen", ["Antisymmetrie"])
eintrag("transitiv", "Eine Relation $R$ auf $X$ heißt transitiv, wenn "
        "$\\forall x, y, z \\in X : ((xRy \\land yRz) \\Rightarrow xRz)$. Im Graphen: Zu jedem Weg aus zwei "
        "Pfeilen gibt es auch die Abkürzung (Def. 1.38 (iv)).",
        r"$\le$ ist transitiv. „$A \cap B \neq \emptyset$“ nicht: $\{1\}$ trifft $\{1, 2\}$, $\{1, 2\}$ trifft $\{2\}$, aber $\{1\} \cap \{2\} = \emptyset$.",
        "relationen", ["Transitivität"])
