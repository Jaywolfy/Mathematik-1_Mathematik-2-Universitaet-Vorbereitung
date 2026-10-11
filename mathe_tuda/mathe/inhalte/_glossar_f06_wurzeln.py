# -*- coding: utf-8 -*-
"""Glossar-Einträge zu Fundament 6: Wurzeln."""
from .glossar import eintrag

eintrag("Quadratwurzel", "Für $a \\ge 0$ ist $\\sqrt{a}$ die nicht negative Zahl, die quadriert $a$ ergibt. "
        "Aus negativen Zahlen gibt es keine Quadratwurzel in $\\mathbb{R}$.",
        r"$\sqrt{49} = 7$, denn $7^2 = 49$ und $7 \ge 0$. Es ist $\sqrt{9} = 3$, nicht $\pm 3$.", "wurzeln",
        ["Quadratwurzeln"])
eintrag("Radikand", "Die Zahl oder der Term unter dem Wurzelzeichen.", r"Bei $\sqrt{12}$ ist $12$ der Radikand.", "wurzeln")
eintrag("Quadratzahl", "Das Quadrat einer ganzen Zahl, also $n^2$.", r"$1, 4, 9, 16, 25, 36, 49, 64, 81, 100$", "wurzeln",
        ["Quadratzahlen"])
eintrag("n-te Wurzel", "Für $a \\ge 0$ ist $\\sqrt[n]{a}$ die nicht negative Zahl, deren $n$-te Potenz $a$ ist. "
        "Bei ungeradem $n$ ist sie auch für negative $a$ erklärt.",
        r"$\sqrt[3]{8} = 2$, $\sqrt[4]{81} = 3$, $\sqrt[3]{-8} = -2$", "wurzeln", ["dritte Wurzel", "Kubikwurzel"])
eintrag("teilweise Wurzelziehen", "Die größte Quadratzahl als Faktor aus dem Radikanden herausziehen und ihre Wurzel "
        "vor die Wurzel schreiben.", r"$\sqrt{72} = \sqrt{36 \cdot 2} = 6\sqrt{2}$", "wurzeln", ["teilweise Wurzel ziehen"])
eintrag("rationaler Exponent", "Ein Bruch als Exponent. Für $a \\ge 0$ ist $a^{\\frac{1}{n}} = \\sqrt[n]{a}$ und "
        "$a^{\\frac{m}{n}} = (\\sqrt[n]{a})^m$.", r"$8^{\frac{2}{3}} = (\sqrt[3]{8})^2 = 4$", "wurzeln",
        ["rationale Exponenten"])
eintrag("Nenner rational machen", "Einen Bruch so erweitern, dass im Nenner keine Wurzel mehr steht.",
        r"$\frac{6}{\sqrt{3}} = \frac{6\sqrt{3}}{3} = 2\sqrt{3}$", "wurzeln")
