# -*- coding: utf-8 -*-
"""Glossar-Einträge zu Fundament 11: Polynome und Polynomdivision."""
from .glossar import eintrag

eintrag("Polynom", "Eine Summe von Vielfachen der Potenzen $x^0, x^1, x^2, \\ldots$: "
        "$a_n x^n + \\ldots + a_1 x + a_0$. Die Exponenten sind natürliche Zahlen oder $0$.",
        r"$2x^3 - x + 5$ ist ein Polynom, $\frac{1}{x}$ und $\sqrt{x}$ sind keine.", "polynome", ["Polynome"])
eintrag("Koeffizient", "Die Zahl, die vor einer Potenz von $x$ steht. Fehlt eine Potenz, ist ihr Koeffizient $0$.",
        r"Bei $2x^3 - x + 5$ sind die Koeffizienten $2$, $0$, $-1$ und $5$.", "polynome", ["Koeffizienten"])
eintrag("Grad", "Die höchste Potenz von $x$, die in einem Polynom mit einem Koeffizienten ungleich $0$ vorkommt.",
        r"$3x^4 - x^7 + 2$ hat den Grad $7$.", "polynome", ["Grad eines Polynoms"])
eintrag("Leitkoeffizient", "Der Koeffizient vor der höchsten Potenz eines Polynoms.",
        r"$3x^4 - x^7 + 2$ hat den Leitkoeffizienten $-1$.", "polynome")
eintrag("Absolutglied", "Der Summand eines Polynoms ohne $x$, also der Koeffizient $a_0$. Er ist der Wert $p(0)$.",
        r"Bei $x^3 - 2x^2 - 5x + 6$ ist das Absolutglied $6$.", "polynome")
eintrag("Polynomdivision", "Schriftliches Teilen eines Polynoms durch ein anderes: teilen, zurückmultiplizieren, "
        "abziehen, wiederholen. Ergebnis: Dividend = Quotient · Teiler + Rest.",
        r"$(x^2 + 5x + 6) : (x + 2) = x + 3$", "polynome")
eintrag("Linearfaktor", "Ein Faktor der Form $(x - x_0)$. Er gehört zur Nullstelle $x_0$.",
        r"$x^2 - 5x + 6 = (x - 2)(x - 3)$ hat die Linearfaktoren $(x - 2)$ und $(x - 3)$.", "polynome",
        ["Linearfaktoren", "Linearfaktorzerlegung"])
eintrag("Vielfachheit", "Wie oft der Linearfaktor $(x - x_0)$ in der Zerlegung eines Polynoms vorkommt. "
        "Bei einer doppelten Nullstelle berührt der Graph die $x$-Achse nur.",
        r"$(x - 1)^2 (x + 2)$: $1$ hat die Vielfachheit $2$, $-2$ die Vielfachheit $1$.", "polynome",
        ["doppelte Nullstelle"])
eintrag("Horner-Schema", "Rechenschema, um $p(x_0)$ schnell auszurechnen: Koeffizient herunterschreiben, mal $x_0$, "
        "nächsten Koeffizienten addieren. Die untere Zeile liefert auch $p(x) : (x - x_0)$.",
        r"$2x^3 - 3x^2 + 5$ bei $x_0 = 2$: $2,\ 1,\ 2,\ 9$, also $p(2) = 9$.", "polynome", ["Horner", "Hornerschema"])
