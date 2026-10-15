# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 14: Die ganzen Zahlen (Skript Disser, Abschn. 3.1)."""
from .glossar import eintrag

eintrag("wohldefiniert", "Eine Definition über Repräsentanten heißt wohldefiniert, wenn das Ergebnis nicht davon abhängt, "
        "welchen Repräsentanten einer Klasse man wählt (Def. 3.2, Bsp. 3.15, Satz 3.50).",
        r"$[a]_n + [b]_n := [a + b]_n$ ist wohldefiniert: Ersetzt du $a$ durch $a + n$, ändert sich die Klasse der Summe nicht.",
        "ganze_zahlen", ["Wohldefiniertheit", "unabhängig von der Wahl der Repräsentanten"])
eintrag("Vorzeichenregeln", "Die Regeln $(-a)b = a(-b) = -(ab)$ und $(-a)(-b) = ab$. Auf $\\mathbb{Z}$ folgen sie aus der "
        "Definition der Multiplikation (Def. 3.5), in einem Ring aus den Ringaxiomen (Satz 3.48).",
        r"$(-3) \cdot (-2) = 3 \cdot 2 = 6$.",
        "ganze_zahlen", ["Minus mal Minus"])
