# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 9: Natürliche Zahlen und vollständige Induktion (Skript Disser, Abschn. 2.1 und 2.2)."""
from .glossar import eintrag

eintrag("Peano-Axiome", "Fünf Bedingungen an ein Tupel $(N, n_0, \\text{succ})$, die beschreiben, was Zählen ist (Def. 2.1): "
        "P1 Existenz der Null, P2 jede Zahl hat einen Nachfolger, P3 die Null ist kein Nachfolger, P4 succ ist injektiv, "
        "P5 keine überflüssigen Elemente (Induktionsprinzip).",
        r"$(\mathbb{N}, 0, \text{succ})$ mit $\text{succ}(n) = n \cup \{n\}$ erfüllt P1 bis P5 (Satz 2.4).",
        "peano_induktion", ["Peano-Axiom", "Peano"])
eintrag("Nachfolger", "Die Zahl $\\text{succ}(n)$, die beim Zählen direkt nach $n$ kommt. Im Mengenmodell ist "
        "$\\text{succ}(n) = n \\cup \\{n\\}$ (Satz 2.4); später gilt $\\text{succ}(n) = n + 1$.",
        r"$\text{succ}(2) = 2 \cup \{2\} = \{0, 1, 2\} = 3$.",
        "peano_induktion", ["Nachfolgerabbildung", "succ"])
eintrag("starke Induktion", "Abwandlung der vollständigen Induktion (Beob. 2.9 (i)): Im Schritt darf man die Aussage für **alle** "
        "$m \\le n$ voraussetzen, nicht nur für $n$. Nötig, wenn der Fall $n + 1$ von beliebig kleinen Fällen abhängt.",
        r"Jedes $n \ge 2$ ist ein Produkt von Primzahlen: Ist $n = a \cdot b$ mit $a, b < n$, gilt die Aussage für $a$ und $b$ nach Annahme.",
        "peano_induktion", ["verallgemeinerte Induktion", "strenge Induktion"])
