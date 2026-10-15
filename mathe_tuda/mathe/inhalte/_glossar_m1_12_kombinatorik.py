# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 12: Potenz, Fakultät und Binomialkoeffizient (Skript Disser, Abschn. 2.6 bis 2.8)."""
from .glossar import eintrag

eintrag("Abbildungsmenge", "Die Menge $\\text{abb}(B, A) := \\{f \\subseteq B \\times A \\mid f\\colon B \\to A\\}$ aller Abbildungen von $B$ nach $A$ (Def. 2.46). "
        "Für endliche Mengen hat sie $|A|^{|B|}$ Elemente (Satz 2.49).",
        r"$\text{abb}(\{0, 1\}, \{a, b\})$ hat $2^2 = 4$ Elemente.",
        "kombinatorik", ["abb", "Menge der Abbildungen"])
eintrag("Indikatorfunktion", "Zu $A \\subseteq M$ die Abbildung $\\chi_A\\colon M \\to \\{0, 1\\}$ mit $\\chi_A(x) = 1$ für $x \\in A$ und $0$ sonst "
        "(Beweis von Satz 2.53). Sie liefert eine Bijektion zwischen Teilmengen von $M$ und Abbildungen $M \\to \\{0, 1\\}$.",
        r"Für $M = \{a, b, c\}$ und $A = \{a, c\}$ ist $\chi_A = (1, 0, 1)$.",
        "kombinatorik", ["charakteristische Funktion", "χ"])
eintrag("Permutation", "Eine bijektive Abbildung $\\sigma\\colon M \\to M$ einer Menge auf sich selbst (Def. 2.54), also eine Umordnung der Elemente. "
        "Es gibt $|M|!$ Permutationen von $M$ (Satz 2.56).",
        r"$(2, 0, 1)$, gelesen als $\sigma(0) = 2$, $\sigma(1) = 0$, $\sigma(2) = 1$, ist eine Permutation von $\{0, 1, 2\}$.",
        "kombinatorik", ["Permutationen", "perm"])
eintrag("k-elementige Teilmenge", "Eine Teilmenge $A \\subseteq M$ mit genau $k$ Elementen. Ihre Menge heißt $\\text{tm}_k(M)$ (Def. 2.58), "
        "ihre Anzahl ist $\\binom{|M|}{k}$ (Satz 2.60).",
        r"$\{0, 2\}$ ist eine $2$-elementige Teilmenge von $\{0, 1, 2, 3\}$. Es gibt $\binom{4}{2} = 6$ davon.",
        "kombinatorik", ["k-elementige Teilmengen", "tm"])
eintrag("Pascalsche Regel", "$\\binom{n+1}{k} = \\binom{n}{k} + \\binom{n}{k-1}$ für $k \\ge 1$ (Satz 2.62). "
        "Sie erklärt, warum jede Zahl im Pascalschen Dreieck die Summe der beiden darüber ist.",
        r"$\binom{5}{2} = \binom{4}{2} + \binom{4}{1} = 6 + 4 = 10$.",
        "kombinatorik", ["Pascal'sche Regel", "Pascalsche Rekursion"])
