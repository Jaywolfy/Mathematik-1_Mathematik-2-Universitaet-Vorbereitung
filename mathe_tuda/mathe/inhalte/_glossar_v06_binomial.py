# -*- coding: utf-8 -*-
"""Glossar-Einträge von Vorkurs 6: Fakultät und Binomialkoeffizient."""
from .glossar import eintrag

eintrag("Fakultät", "Für $n \\in \\mathbb{N}_0$ ist $n! := \\prod_{k=1}^{n} k = 1 \\cdot 2 \\cdot \\ldots \\cdot n$ "
        "(gelesen „n Fakultät“). $n!$ zählt, auf wie viele Arten man $n$ Dinge in eine Reihenfolge bringen kann. "
        "Es gilt $0! = 1$ (leeres Produkt) und $n! = n \\cdot (n-1)!$.",
        r"$4! = 1 \cdot 2 \cdot 3 \cdot 4 = 24$", "binomial", ["n!", "Fakultäten"])
eintrag("Binomialkoeffizient", "Für $n, k \\in \\mathbb{N}_0$ ist $\\binom{n}{k} := \\frac{n!}{(n-k)! \\cdot k!}$ "
        "falls $k \\le n$ und $0$ falls $k > n$ (gelesen „n über k“). Er zählt, wie viele Möglichkeiten es gibt, "
        "$k$ Dinge aus $n$ auszuwählen, wenn die Reihenfolge egal ist.",
        r"$\binom{4}{2} = \frac{4!}{2! \cdot 2!} = 6$", "binomial", ["n über k", "Binomialkoeffizienten"])
eintrag("Pascalsches Dreieck", "Dreieck aus Binomialkoeffizienten: Zeile $n$ enthält $\\binom{n}{0}, \\ldots, "
        "\\binom{n}{n}$. Jede Zahl ist die Summe der beiden Zahlen schräg darüber: "
        "$\\binom{n+1}{k} = \\binom{n}{k-1} + \\binom{n}{k}$.",
        "Zeile 4: $1, 4, 6, 4, 1$", "binomial", ["Pascal-Dreieck"])
eintrag("binomischer Lehrsatz", "Formel zum Ausmultiplizieren von $(a + b)^n$: "
        "$(a+b)^n = \\sum_{k=0}^{n} \\binom{n}{k} a^{n-k} b^k$. Die binomischen Formeln sind der Fall $n = 2$.",
        r"$(a+b)^3 = a^3 + 3a^2 b + 3ab^2 + b^3$", "binomial", ["Binomialsatz"])
