# -*- coding: utf-8 -*-
"""Glossar-Einträge zu Fundament 10: Quadratische Gleichungen."""
from .glossar import eintrag

eintrag("quadratische Gleichung", "Eine Gleichung, die sich in die Form $ax^2 + bx + c = 0$ mit $a \\neq 0$ bringen lässt. "
        "Die höchste Potenz von $x$ ist $2$. Sie hat zwei, eine oder keine reelle Lösung.",
        r"$2x^2 + 3x - 2 = 0$ hat die Lösungen $\frac{1}{2}$ und $-2$.", "quadratisch", ["quadratische Gleichungen"])
eintrag("Normalform", "Die Form $x^2 + px + q = 0$ einer quadratischen Gleichung: Vor $x^2$ steht eine $1$. "
        "Man erhält sie, indem man jeden Summanden durch $a$ teilt.",
        r"Aus $2x^2 - 8x + 6 = 0$ wird $x^2 - 4x + 3 = 0$, also $p = -4$, $q = 3$.", "quadratisch")
eintrag("Satz vom Nullprodukt", "Ein Produkt ist genau dann $0$, wenn mindestens einer der Faktoren $0$ ist.",
        r"$x(x - 5) = 0$ gilt genau für $x = 0$ oder $x = 5$.", "quadratisch", ["Nullprodukt"])
eintrag("quadratische Ergänzung", "Man addiert zu $x^2 + px$ die Zahl $\\left(\\frac{p}{2}\\right)^2$ und zieht sie wieder ab. "
        "So entsteht ein vollständiges Quadrat $\\left(x + \\frac{p}{2}\\right)^2$.",
        r"$x^2 + 6x + 5 = x^2 + 6x + 9 - 9 + 5 = (x + 3)^2 - 4$", "quadratisch")
eintrag("pq-Formel", "Lösungsformel für die Normalform $x^2 + px + q = 0$: "
        "$x_{1,2} = -\\frac{p}{2} \\pm \\sqrt{\\left(\\frac{p}{2}\\right)^2 - q}$.",
        r"$x^2 - 2x - 8 = 0$: $x = 1 \pm \sqrt{1 + 8} = 1 \pm 3$, also $4$ und $-2$.", "quadratisch", ["p-q-Formel"])
eintrag("Mitternachtsformel", "Lösungsformel für $ax^2 + bx + c = 0$: $x_{1,2} = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$. "
        "Man braucht vorher nicht durch $a$ zu teilen.",
        r"$2x^2 + 3x - 2 = 0$: $x = \frac{-3 \pm 5}{4}$, also $\frac{1}{2}$ und $-2$.", "quadratisch",
        ["abc-Formel", "Lösungsformel"])
eintrag("Diskriminante", "Der Ausdruck $D = b^2 - 4ac$ unter der Wurzel der Mitternachtsformel. "
        "$D > 0$: zwei Lösungen, $D = 0$: eine, $D < 0$: keine reelle Lösung.",
        r"$x^2 + 4x + 5 = 0$: $D = 16 - 20 = -4 < 0$, keine Lösung.", "quadratisch")
eintrag("Satz von Vieta", "Hat $x^2 + px + q = 0$ die Lösungen $x_1, x_2$, so gilt $x_1 + x_2 = -p$ und $x_1 \\cdot x_2 = q$, "
        "also $x^2 + px + q = (x - x_1)(x - x_2)$.",
        r"$x^2 - 5x + 6 = (x - 2)(x - 3)$, denn $2 + 3 = 5$ und $2 \cdot 3 = 6$.", "quadratisch", ["Vieta"])
eintrag("Nullstelle", "Eine Stelle $x_0$, an der ein Term oder eine Funktion den Wert $0$ hat: $f(x_0) = 0$. "
        "Am Graphen ist das ein Schnittpunkt mit der $x$-Achse.",
        r"$x^2 - 4$ hat die Nullstellen $2$ und $-2$.", "quadratisch", ["Nullstellen"])
