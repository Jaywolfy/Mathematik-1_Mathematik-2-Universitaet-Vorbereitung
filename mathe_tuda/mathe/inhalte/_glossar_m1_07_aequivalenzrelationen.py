# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 7: Äquivalenzrelationen (Skript Disser, Abschn. 1.6)."""
from .glossar import eintrag

eintrag("Äquivalenzrelation", "Eine Relation auf $M$, die reflexiv, symmetrisch und transitiv ist; geschrieben $\\sim$ "
        "(Skript Disser, Def. 1.59). Sie legt fest, welche Elemente als „gleichwertig“ gelten.",
        r"„Haben dieselbe Parität“ auf $\mathbb{Z}$; $(z_1, n_1) \sim (z_2, n_2) :\iff z_1 n_2 = z_2 n_1$ für Brüche.",
        "aequivalenzrelationen", ["Äquivalenzrelationen"])
eintrag("Äquivalenzklasse", "Zu $a \\in M$ und einer Äquivalenzrelation $\\sim$ die Menge $[a] := \\{x \\in M \\mid x \\sim a\\}$ "
        "aller zu $a$ gleichwertigen Elemente (Def. 1.61). Die Klassen zerlegen $M$ in disjunkte, nichtleere Teile (Satz 1.63).",
        r"Parität auf $\{-1, 1, 2, 3, 4\}$: $[1] = \{-1, 1, 3\}$, $[2] = \{2, 4\}$.",
        "aequivalenzrelationen", ["Äquivalenzklassen"])
eintrag("Repräsentant", "Ein Element $a$ einer Äquivalenzklasse $K$; dann ist $K = [a]$. Jedes Element einer Klasse kann "
        "sie vertreten.",
        r"$[1] = [3] = [-1]$: $1$, $3$ und $-1$ sind Repräsentanten derselben Klasse.",
        "aequivalenzrelationen", ["Repräsentanten", "Vertreter"])
eintrag("Faktormenge", "Die Menge $M/{\\sim} := \\{U \\in \\mathcal{P}(M) \\mid \\exists a \\in M : U = [a]\\}$ aller "
        "Äquivalenzklassen (Def. 1.64). Ihre Elemente sind Mengen.",
        r"$\{-1, 1, 2, 3, 4\}/{\sim_2} = \{\{-1, 1, 3\}, \{2, 4\}\}$; $\mathbb{Q}$ als Faktormenge der Brüche (Bsp. 1.65).",
        "aequivalenzrelationen", ["Faktormengen", "Quotientenmenge"])
