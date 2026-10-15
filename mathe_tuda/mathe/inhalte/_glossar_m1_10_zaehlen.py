# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 10: Endliche Mengen, Addition und Subtraktion (Skript Disser, Abschn. 2.3 und 2.4)."""
from .glossar import eintrag

eintrag("endliche Menge", "Eine Menge $M$ heißt endlich, wenn es eine Bijektion $f\\colon n \\to M$ für ein $n \\in \\mathbb{N}$ gibt (Def. 2.10). "
        "Dabei ist $n = \\{0, \\ldots, n-1\\}$.",
        r"$\{a, b, c\}$ ist endlich: $0 \mapsto a$, $1 \mapsto b$, $2 \mapsto c$ ist bijektiv. $\mathbb{N}$ ist nicht endlich.",
        "zaehlen", ["endlich", "endliche Mengen", "unendlich"])
eintrag("Kardinalität", "Die Zahl $|M| := n$ der Elemente einer endlichen Menge $M$, wobei $f\\colon n \\to M$ bijektiv ist (Def. 2.10). "
        "Sie ist eindeutig bestimmt, und es gilt $|n| = n$. Im Vorkurs heißt sie Mächtigkeit.",
        r"$|\{a, b, c\}| = 3$ und $|\emptyset| = 0$.",
        "zaehlen", ["Kardinalitäten", "Anzahl der Elemente"])
eintrag("Wohlordnungsprinzip", "Jede nichtleere Teilmenge $N \\subseteq \\mathbb{N}$ besitzt ein kleinstes Element (Satz 2.16). "
        "Das ist die Grundlage dafür, dass jede Suche nach dem kleinsten $n$ mit einer Eigenschaft terminiert.",
        r"Die Menge $\{n \in \mathbb{N} \mid n^2 > 50\}$ hat das Minimum $8$.",
        "zaehlen", ["Wohlordnung", "Wohlordnungssatz"])
eintrag("Nachfolgerregel", "Für die Addition $\\text{succ}(a) + b = \\text{succ}(a + b)$ (Satz 2.18), für die Multiplikation "
        "$a \\cdot \\text{succ}(b) = a \\cdot b + a$ (Satz 2.29). Sie führt Rechnen auf das Zählen weiter zurück.",
        r"$\text{succ}(3) + 2 = \text{succ}(5) = 6$.",
        "zaehlen", ["Nachfolgerregeln"])
eintrag("Subtraktion", "Die Differenz $b - a$ ist das eindeutige $k \\in \\mathbb{N}$ mit $b = a + k$, definiert nur für $a \\le b$ (Def. 2.24). "
        "Sie ist eine partielle Umkehrung der Addition.",
        r"$8 - 5 = 3$, aber $5 - 8$ existiert in $\mathbb{N}$ nicht.",
        "zaehlen", ["Differenz", "Subtraktion in ℕ"])
eintrag("Inklusions-Exklusions-Prinzip", "Für endliche Mengen gilt $|A \\cup B| = |A| + |B| - |A \\cap B|$ (Satz 2.27). "
        "Was in beiden Mengen liegt, wird von $|A| + |B|$ doppelt gezählt und einmal abgezogen.",
        r"$A = \{1, \ldots, 5\}$, $B = \{4, 5, 6, 7\}$: $|A \cup B| = 5 + 4 - 2 = 7$.",
        "zaehlen", ["Siebformel", "Inklusion-Exklusion"])
