# -*- coding: utf-8 -*-
"""Glossar-Einträge von Fundament 14: Exponentialfunktion und Logarithmus."""
from .glossar import eintrag

eintrag("exponentielles Wachstum", "Wachstum, bei dem eine Größe in gleichen Schritten immer mit demselben Faktor "
        "malgenommen wird, zum Beispiel verdoppelt.", r"$3$ Bakterien, die sich stündlich verdoppeln: nach $4$ Stunden $3 \cdot 2^4 = 48$.",
        "exp_log")
eintrag("Exponentialfunktion", "Eine Funktion $f(x) = a^x$ mit $a > 0$, $a \\neq 1$. Die Variable steht im Exponenten. "
        "Meist ist $\\exp(x) = \\mathrm{e}^x$ gemeint.", r"$f(x) = 2^x$ hat $f(0) = 1$, $f(3) = 8$, $f(-1) = \frac{1}{2}$.",
        "exp_log", ["Exponentialfunktionen", "exp"])
eintrag("eulersche Zahl", "Die Zahl $\\mathrm{e} = 2{,}71828\\ldots$, der Grenzwert von $\\left(1 + \\frac{1}{n}\\right)^n$. "
        "Sie ist irrational und Basis des natürlichen Logarithmus.", r"$\mathrm{e}^0 = 1$, $\ln(\mathrm{e}) = 1$.",
        "exp_log")
eintrag("Logarithmus", "$\\log_a(y)$ ist die Zahl $x$ mit $a^x = y$ (für $a > 0$, $a \\neq 1$, $y > 0$). "
        "Er beantwortet die Frage: $a$ hoch wie viel ergibt $y$?", r"$\log_2(8) = 3$, weil $2^3 = 8$.",
        "exp_log", ["Logarithmen", "log"])
eintrag("Zweierlogarithmus", "Der Logarithmus zur Basis $2$, $\\log_2$. Er zählt, wie oft man halbieren kann, "
        "und wie viele Bits man für $N$ Zustände braucht (aufgerundet).", r"$\log_2(1024) = 10$", "exp_log",
        ["log2", "binärer Logarithmus", "Logarithmus dualis"])
eintrag("natürlicher Logarithmus", "Der Logarithmus zur Basis $\\mathrm{e}$, geschrieben $\\ln$. Er macht $\\mathrm{e}^x$ rückgängig.",
        r"$\ln(\mathrm{e}^3) = 3$, $\ln(1) = 0$", "exp_log", ["ln"])
eintrag("Logarithmusgesetze", "Für $u, v > 0$: $\\log_a(uv) = \\log_a(u) + \\log_a(v)$, "
        "$\\log_a\\left(\\frac{u}{v}\\right) = \\log_a(u) - \\log_a(v)$, $\\log_a(u^r) = r \\log_a(u)$. Für Summen gibt es keine Regel.",
        r"$\log_2(8 \cdot 4) = 3 + 2 = 5$", "exp_log", ["Logarithmusgesetz"])
eintrag("Exponentialgleichung", "Eine Gleichung, in der die Unbekannte im Exponenten steht. Man stellt die Potenz allein "
        "und logarithmiert oder vergleicht Exponenten.", r"$3 \cdot 2^x = 96 \Rightarrow 2^x = 32 \Rightarrow x = 5$",
        "exp_log", ["Exponentialgleichungen"])
