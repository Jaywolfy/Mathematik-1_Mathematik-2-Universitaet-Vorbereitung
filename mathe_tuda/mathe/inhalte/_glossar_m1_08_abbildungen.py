# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 8: Abbildungen (Skript Disser, Abschn. 1.7)."""
from .glossar import eintrag

eintrag("Verkettung", "Zu $f\\colon X \\to Y$ und $g\\colon Y \\to Z$ die Abbildung "
        "$g \\circ f\\colon X \\to Z,\\ x \\mapsto g(f(x))$ (Def. 1.75). Erst $f$, dann $g$: gelesen „$g$ nach $f$“.",
        r"$f(x) = x + 1$, $g(x) = 2x$: $(g \circ f)(3) = g(4) = 8$, aber $(f \circ g)(3) = f(6) = 7$.",
        "uni_abbildungen", ["Komposition", "Hintereinanderausführung", "Verkettungen"])
eintrag("Identität", "Die Abbildung $\\mathrm{id}_M\\colon M \\to M,\\ x \\mapsto x$, die jedes Element auf sich selbst "
        "abbildet (Bsp. 1.68). Sie ist bijektiv und ihre eigene Umkehrabbildung.",
        r"$f^{-1} \circ f = \mathrm{id}_X$ und $f \circ f^{-1} = \mathrm{id}_Y$ für bijektives $f$.",
        "uni_abbildungen", ["Identitätsabbildung", "identische Abbildung"])
eintrag("Einschränkung", "Zu $f\\colon X \\to Y$ und $A \\subseteq X$ die Abbildung "
        "$f|_A\\colon A \\to f(A),\\ x \\mapsto f(x)$ (Def. 1.80). Definitions- und Zielmenge werden verkleinert, "
        "die Vorschrift bleibt.",
        r"$x \mapsto x^2$ auf $\mathbb{R}$ ist nicht injektiv, die Einschränkung auf $\mathbb{R}_{\ge 0}$ ist bijektiv.",
        "uni_abbildungen", ["Restriktion", "Einschränkungen"])
eintrag("Verknüpfung", "Eine Abbildung $\\star\\colon X \\times X \\to X$ heißt (binäre) Verknüpfung auf $X$. "
        "Man schreibt $x \\star y := \\star(x, y)$ (Def. 1.66).",
        r"Die Addition $+\colon \mathbb{Z} \times \mathbb{Z} \to \mathbb{Z}$ ist eine Verknüpfung auf $\mathbb{Z}$.",
        "uni_abbildungen", ["binäre Verknüpfung", "Verknüpfungen"])
eintrag("kanonische Abbildung", "Zu einer Äquivalenzrelation $\\sim$ auf $M$ die Abbildung "
        "$\\nu\\colon M \\to M/{\\sim},\\ x \\mapsto [x]$, die jedes Element in seine Äquivalenzklasse schickt (Bsp. 1.68). "
        "Sie ist immer surjektiv.",
        r"Parität auf $\{1, 2, 3, 4\}$: $\nu(1) = \nu(3) = \{1, 3\}$.",
        "uni_abbildungen", ["kanonische Projektion"])
