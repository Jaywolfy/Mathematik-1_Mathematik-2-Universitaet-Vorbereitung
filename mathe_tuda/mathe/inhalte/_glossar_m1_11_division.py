# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 11: Multiplikation, Division und Division mit Rest (Skript Disser, Abschn. 2.5)."""
from .glossar import eintrag

eintrag("Multiplikation", "Das Produkt $a \\cdot b := |a \\times b|$ zählt die Paare eines Rasters mit $a$ Zeilen und $b$ Spalten (Def. 2.28). "
        "Es gilt $a \\cdot \\text{succ}(b) = a \\cdot b + a$ (Satz 2.29), und $|A \\times B| = |A| \\cdot |B|$ (Satz 2.31).",
        r"Das Schachbrett hat $8 \cdot 8 = 64$ Felder.",
        "division_rest", ["Multiplikationen"])
eintrag("Division", "Die Division $a / b$ ist die partielle Umkehrung der Multiplikation: Für $b \\neq 0$ und $b \\mid a$ ist $a / b$ das eindeutige $q$ "
        "mit $a = b \\cdot q$ (Def. 2.37). Geht die Rechnung nicht auf, nimmt man die Division mit Rest.",
        r"$12 / 3 = 4$, aber $13 / 3$ existiert in $\mathbb{N}$ nicht.",
        "division_rest", ["Quotient", "Quotienten"])
eintrag("Division mit Rest", "Zu $a, b \\in \\mathbb{N}$ mit $b \\neq 0$ gibt es eindeutig bestimmte $q, r \\in \\mathbb{N}$ mit $a = q \\cdot b + r$ und $r < b$ (Satz 2.41). "
        "Dabei ist $q = a \\operatorname{div} b$ der ganzzahlige Quotient und $r = a \\bmod b$ der Rest.",
        r"$47 = 5 \cdot 9 + 2$: $47 \operatorname{div} 9 = 5$, $47 \bmod 9 = 2$.",
        "division_rest", ["euklidische Division", "ganzzahlige Division"])
eintrag("Rest", "Der Rest $a \\bmod b$ bei Division von $a$ durch $b \\neq 0$ ist das $r < b$ aus $a = q \\cdot b + r$ (Def. 2.42). "
        "Es gilt $b \\mid a \\iff a \\bmod b = 0$ (Beob. 2.43). Reste kann man in Summen und Produkten sofort bilden (Satz 2.44).",
        r"$100 \bmod 7 = 2$, denn $100 = 14 \cdot 7 + 2$.",
        "division_rest", ["mod", "modulo", "Restbildung"])
eintrag("ganzzahliger Quotient", "Der Quotient $a \\operatorname{div} b$ aus der Division mit Rest (Def. 2.42): die größte Zahl $q$ mit $q \\cdot b \\le a$. "
        "In Programmiersprachen ist das `a // b`.",
        r"$100 \operatorname{div} 7 = 14$, denn $14 \cdot 7 = 98 \le 100 < 105 = 15 \cdot 7$.",
        "division_rest", ["div"])
