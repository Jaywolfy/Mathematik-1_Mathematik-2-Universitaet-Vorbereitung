# -*- coding: utf-8 -*-
"""Glossar-Einträge von Vorkurs 11: Injektiv, surjektiv, bijektiv."""
from .glossar import eintrag

eintrag("injektiv", "$f\\colon D \\to W$ heißt injektiv, wenn aus $f(x_1) = f(x_2)$ stets $x_1 = x_2$ folgt. "
        "Kein Wert wird von zwei verschiedenen Stellen getroffen.",
        r"$x \mapsto 3x - 2$ auf $\mathbb{R}$ ist injektiv, $x \mapsto x^2$ auf $\mathbb{R}$ nicht: $f(-1) = f(1)$.",
        "injektiv", ["Injektivität"])
eintrag("surjektiv", "$f\\colon D \\to W$ heißt surjektiv, wenn $f(D) = W$ gilt: Zu jedem $y \\in W$ gibt es ein $x \\in D$ "
        "mit $f(x) = y$.",
        r"$x \mapsto x^2$ ist als $\mathbb{R} \to \mathbb{R}_{\ge 0}$ surjektiv, als $\mathbb{R} \to \mathbb{R}$ nicht.",
        "injektiv", ["Surjektivität"])
eintrag("bijektiv", "Injektiv und surjektiv zugleich: Jedes $y \\in W$ hat genau ein Urbild. "
        "Genau dann gibt es eine Umkehrfunktion.",
        r"$x \mapsto x^2$ als $\mathbb{R}_{\ge 0} \to \mathbb{R}_{\ge 0}$ ist bijektiv.",
        "injektiv", ["Bijektivität", "Bijektion"])
eintrag("Umkehrfunktion", "Zu bijektivem $f\\colon D \\to W$ die Funktion $f^{-1}\\colon W \\to D$, die jedem $y$ sein "
        "eindeutiges Urbild zuordnet. Es gilt $f^{-1}(f(x)) = x$ und $f(f^{-1}(y)) = y$. Nicht verwechseln mit "
        "dem Kehrwert $\\frac{1}{f}$ oder dem Urbild $f^{-1}(B)$ einer Menge.",
        r"$f(x) = 3x - 2$ hat $f^{-1}(y) = \frac{y + 2}{3}$.",
        "injektiv", ["Umkehrabbildung", "inverse Funktion", "Umkehrfunktionen"])
