# -*- coding: utf-8 -*-
"""Glossar-Einträge von Vorkurs 5: Summen- und Produktzeichen."""
from .glossar import eintrag

eintrag("Summenzeichen", "Das große Sigma $\\sum$ ist eine Kurzschrift für eine lange Summe. Unten steht, wo der "
        "Laufindex startet, oben, wo er aufhört; rechts steht, was für jeden Wert addiert wird.",
        r"$\sum_{k=1}^{3} 2k = 2 + 4 + 6 = 12$", "summen", ["Summe", "Summenschreibweise", "Sigma"])
eintrag("Produktzeichen", "Das große Pi $\\prod$ ist eine Kurzschrift für ein langes Produkt. Es funktioniert wie "
        "das Summenzeichen, nur wird malgenommen statt addiert.",
        r"$\prod_{k=1}^{3} k^2 = 1 \cdot 4 \cdot 9 = 36$", "summen", ["Produkt", "Produktschreibweise"])
eintrag("Laufindex", "Die Variable unter dem Summen- oder Produktzeichen (oft $k$, $i$ oder $j$). Sie durchläuft "
        "nacheinander alle ganzen Zahlen von der unteren bis zur oberen Grenze. Ihr Name ist egal.",
        r"In $\sum_{k=2}^{5} k$ ist $k$ der Laufindex, er nimmt die Werte $2, 3, 4, 5$ an.", "summen",
        ["Summenindex", "Summationsindex", "untere Grenze", "obere Grenze"])
eintrag("leere Summe", "Eine Summe, deren untere Grenze größer als die obere ist. Es wird nichts addiert, "
        "der Wert ist per Vereinbarung $0$.", r"$\sum_{k=5}^{4} k = 0$", "summen")
eintrag("leeres Produkt", "Ein Produkt, dessen untere Grenze größer als die obere ist. Es wird nichts malgenommen, "
        "der Wert ist per Vereinbarung $1$. Deshalb gilt $0! = 1$.", r"$\prod_{k=1}^{0} k = 1$", "summen")
eintrag("Indexverschiebung", "Den Laufindex umnummerieren, ohne den Wert zu ändern: Die Grenzen wandern um $j$, "
        "und im Term wird $k$ durch $k - j$ ersetzt.",
        r"$\sum_{k=1}^{3} k = \sum_{k=6}^{8} (k - 5)$", "summen", ["Indexshift"])
