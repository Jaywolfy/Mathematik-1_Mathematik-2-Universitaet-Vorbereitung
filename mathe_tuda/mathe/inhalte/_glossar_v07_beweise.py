# -*- coding: utf-8 -*-
"""Glossar-Einträge von Vorkurs 7: Direkter Beweis."""
from .glossar import eintrag

eintrag("Voraussetzung", "Was in einem Satz als gegeben angenommen wird, der Teil vor dem $\\Rightarrow$. "
        "Im Beweis darfst du sie benutzen und musst zeigen, wo sie eingeht.",
        r"In „$2 \mid n \Rightarrow 2 \mid n^3$“ ist $2 \mid n$ die Voraussetzung.", "beweise",
        ["Voraussetzungen", "Annahme"])
eintrag("Behauptung", "Was in einem Satz gezeigt werden soll, der Teil nach dem $\\Rightarrow$. "
        "Im Beweis darfst du sie nicht benutzen, du musst bei ihr ankommen.",
        r"In „$2 \mid n \Rightarrow 2 \mid n^3$“ ist $2 \mid n^3$ die Behauptung.", "beweise",
        ["Behauptungen", "zu zeigen"])
eintrag("direkter Beweis", "Beweis von $A \\Rightarrow B$ durch eine Kette von Folgerungen "
        "$A \\Rightarrow Z_1 \\Rightarrow Z_2 \\Rightarrow \\ldots \\Rightarrow B$, jede begründet.",
        r"$n = 2k \Rightarrow n^3 = 8k^3 = 2 \cdot (4k^3) \Rightarrow 2 \mid n^3$", "beweise",
        ["direkte Beweise", "Implikationskette"])
eintrag("Teiler", "Für $n, k \\in \\mathbb{N}$ heißt $k$ Teiler von $n$ (geschrieben $k \\mid n$, „k teilt n“), "
        "wenn es ein $m \\in \\mathbb{N}$ mit $n = k \\cdot m$ gibt. Man sagt auch: $n$ ist durch $k$ teilbar.",
        r"$7 \mid 42$, denn $42 = 7 \cdot 6$. Aber $4 \nmid 10$.", "beweise",
        ["teilt", "teilbar", "Teilbarkeit"])
eintrag("gerade Zahl", "Eine ganze Zahl $n$ heißt gerade, wenn es ein $k \\in \\mathbb{Z}$ mit $n = 2k$ gibt, "
        "und ungerade, wenn es ein $k \\in \\mathbb{Z}$ mit $n = 2k + 1$ gibt. Jede ganze Zahl ist genau eins von beidem.",
        r"$0 = 2 \cdot 0$ ist gerade, $-7 = 2 \cdot (-4) + 1$ ist ungerade.", "beweise",
        ["gerade", "ungerade", "ungerade Zahl", "gerade Zahlen", "ungerade Zahlen"])
