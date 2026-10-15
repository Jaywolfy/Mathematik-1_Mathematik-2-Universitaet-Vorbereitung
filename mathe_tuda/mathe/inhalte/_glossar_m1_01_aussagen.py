# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 1: Aussagen und logische Verknüpfungen (Disser 1.1–1.2)."""
from .glossar import eintrag

eintrag("Kontravalenz", "Exklusives Oder (XOR), Zeichen $P \\oplus Q$: wahr, wenn **genau eine** der beiden "
        "Aussagen wahr ist (Skript Disser, Bemerkung 1.8). Anders als $P \\lor Q$ ist sie falsch, wenn beide gelten.",
        r"$\text{w} \oplus \text{w} = \text{f}$, $\text{w} \oplus \text{f} = \text{w}$; in Python für Wahrheitswerte `p != q`.",
        "uni_aussagen", ["XOR", "exklusives Oder"])
eintrag("ex falso quodlibet", "Lateinisch „aus Falschem folgt Beliebiges“: Ist $P$ falsch, so ist die Implikation "
        "$P \\Rightarrow Q$ wahr, egal welchen Wert $Q$ hat (Zeilen 3 und 4 der Wahrheitstabelle).",
        r"„Wenn $0 = 1$, dann ist Russell der Papst“ ist wahr.", "uni_aussagen", ["ex falso"])
eintrag("Kontrapositionsgesetz", "Satz 1.12 im Skript Disser: $(P \\Rightarrow Q) \\Leftrightarrow (\\neg Q \\Rightarrow \\neg P)$. "
        "Eine Implikation ist äquivalent zu ihrer Kontraposition (beide Teile negiert **und** Richtung getauscht). "
        "Nicht äquivalent sind die Umkehrung $Q \\Rightarrow P$ und $\\neg P \\Rightarrow \\neg Q$.",
        r"„Regnet es, ist die Straße nass“ $\Leftrightarrow$ „Ist die Straße trocken, regnet es nicht“.",
        "uni_aussagen", ["Kontrapositionsgesetze"])
