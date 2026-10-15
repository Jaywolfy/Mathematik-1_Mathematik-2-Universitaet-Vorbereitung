# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 3: Mengen (Disser 1.4)."""
from .glossar import eintrag

eintrag("Obermenge", "Gilt $N \\subseteq M$, heißt $M$ Obermenge von $N$, geschrieben $M \\supseteq N$.",
        r"$\mathbb{Z} \supseteq \mathbb{N}$, denn jede natürliche Zahl ist ganz.", "uni_mengen", ["Obermengen"])
eintrag("Russell'sche Antinomie", "Die Sammlung $S$ aller Mengen, die sich nicht selbst enthalten, kann keine Menge sein: "
        "Aus $S \\in S$ folgt $S \\notin S$ und umgekehrt. Deshalb erlaubt man nur bestimmte Bildungsweisen von Mengen.",
        r"Wie der Barbier, der genau die rasiert, die sich nicht selbst rasieren.", "uni_mengen",
        ["Russellsche Antinomie", "Russells Paradoxon"])
eintrag("Aussonderung", "Bildung einer Teilmenge einer Grundmenge $G$ durch eine Eigenschaft: $\\{x \\in G \\mid E(x)\\}$ "
        "enthält alle $x \\in G$, für die die Aussageform $E(x)$ gilt.",
        r"$\{n \in \mathbb{N} \mid n \le 5\} = \{0, 1, 2, 3, 4, 5\}$", "uni_mengen", ["Aussonderungsprinzip"])
eintrag("disjunkt", "Zwei Mengen $M$, $N$ heißen disjunkt, wenn sie kein gemeinsames Element haben, also $M \\cap N = \\emptyset$.",
        r"Die geraden und die ungeraden ganzen Zahlen sind disjunkt.", "uni_mengen", ["Disjunktheit"])
eintrag("Tupel", "Geordnete Aneinanderreihung endlich vieler Elemente $(a_1, \\ldots, a_n)$ mit $n \\in \\mathbb{N}$. "
        "Anders als bei Mengen zählen Reihenfolge und Wiederholungen. Für $n = 0$ gibt es das leere Tupel $()$.",
        r"$(1, 2) \neq (2, 1)$ und $(1, 1, 2)$ hat Länge $3$; dagegen $\{1, 1, 2\} = \{1, 2\}$.", "uni_mengen",
        ["n-Tupel", "leeres Tupel"])
