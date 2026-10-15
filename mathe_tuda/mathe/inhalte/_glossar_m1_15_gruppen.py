# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 15: Gruppen (Skript Disser, Abschn. 3.2)."""
from .glossar import eintrag

eintrag("Gruppe", "Ein Tupel $(G, \\ast)$ aus $G \\ne \\emptyset$ und einer Verknüpfung $\\ast\\colon G^2 \\to G$ mit "
        "Assoziativität, neutralem Element und inversen Elementen (Def. 3.8).",
        r"$(\mathbb{Z}, +)$, $(\{-1, 1\}, \cdot)$, $(\mathbb{Z}/n\mathbb{Z}, +)$, die Bitgruppe $B_n$.",
        "gruppen", ["Gruppen"])
eintrag("abelsch", "Eine Gruppe heißt abelsch (kommutativ), falls zusätzlich $a \\ast b = b \\ast a$ für alle $a, b$ gilt (Def. 3.8).",
        r"$(\mathbb{Z}, +)$ ist abelsch, die Permutationen von $\{a, b, c\}$ mit $\circ$ nicht.",
        "gruppen", ["abelsche Gruppe", "kommutative Gruppe"])
eintrag("neutrales Element", "Das Element $e$ einer Gruppe mit $e \\ast a = a$ (und nach Satz 3.9 auch $a \\ast e = a$) für alle $a$. "
        "Es ist eindeutig. In additiv geschriebenen Gruppen heißt es $0$.",
        r"In $(\mathbb{Z}, +)$ ist es $0$, in $(\{-1, 1\}, \cdot)$ ist es $1$.",
        "gruppen", ["Einselement der Gruppe", "neutrale Elemente"])
eintrag("inverses Element", "Zu $a \\in G$ das Element $b$ mit $b \\ast a = e$ (nach Satz 3.9 auch $a \\ast b = e$), geschrieben $a^{-1}$, additiv $-a$. "
        "Es ist eindeutig.",
        r"In $\mathbb{Z}/7\mathbb{Z}$ ist $[3]^{-1} = [4]$, denn $3 + 4 = 7 \equiv 0$.",
        "gruppen", ["Inverses", "inverse Elemente"])
eintrag("Assoziativität", "Eigenschaft einer Verknüpfung: $a \\ast (b \\ast c) = (a \\ast b) \\ast c$. Die Klammern dürfen versetzt werden.",
        r"Addition und Verkettung von Abbildungen sind assoziativ, die Subtraktion nicht: $(5 - 3) - 1 \ne 5 - (3 - 1)$.",
        "gruppen", ["Assoziativgesetz", "assoziativ"])
eintrag("Kürzungsregel", "In einer Gruppe folgt aus $a \\ast b = a \\ast c$ stets $b = c$, und aus $b \\ast a = c \\ast a$ stets $b = c$ (Satz 3.16 (ii)).",
        r"Aus $5 + b = 5 + c$ in $\mathbb{Z}$ folgt $b = c$.",
        "gruppen", ["Kürzungsregeln", "Kürzungsgesetz"])
eintrag("Verknüpfungstafel", "Tabelle einer Verknüpfung auf einer endlichen Menge: In Zeile $a$ und Spalte $b$ steht $a \\ast b$. "
        "In der Tafel einer Gruppe kommt in jeder Zeile und Spalte jedes Element genau einmal vor.",
        r"Tafel von $(\{-1, 1\}, \cdot)$: $1 \cdot 1 = 1$, $1 \cdot (-1) = -1$, $(-1) \cdot (-1) = 1$.",
        "gruppen", ["Gruppentafel", "Verknüpfungstabelle", "Cayley-Tafel"])
eintrag("Restklasse", "Zu $a \\in \\mathbb{Z}$ und $n \\in \\mathbb{N}\\setminus\\{0\\}$ die Menge $[a]_n := \\{b \\in \\mathbb{Z} \\mid b \\bmod n = a \\bmod n\\}$ "
        "aller Zahlen mit demselben Rest wie $a$ (Bsp. 3.15).",
        r"$[3]_5 = \{\ldots, -7, -2, 3, 8, 13, \ldots\}$.",
        "gruppen", ["Restklassen", "Klasse modulo n"])
eintrag("Bitgruppe", "Die abelsche Gruppe $B_n := (\\{0, 1\\}^n, \\oplus)$ mit stellenweiser Addition modulo $2$ (XOR). "
        "Neutral ist $(0, \\ldots, 0)$, jedes Element ist sein eigenes Inverses (Bsp. 3.14).",
        r"In $B_3$: $(1, 0, 1) \oplus (1, 1, 0) = (0, 1, 1)$.",
        "gruppen", ["XOR-Gruppe", "Bitgruppen"])
