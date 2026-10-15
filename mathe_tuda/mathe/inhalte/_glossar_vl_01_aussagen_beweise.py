# -*- coding: utf-8 -*-
"""Glossar-Einträge zu Vorlesung 1 (Aussagen und Beweise). Vorhandene Begriffe (Aussage, Implikation, De Morgan,
Beweisformen, gerade Zahl …) werden nur verlinkt."""
from .glossar import eintrag

eintrag("Belegung", "Eine Belegung setzt für jede Variable einer [[Aussageform]] einen konkreten Wert ein. Erst dadurch "
        "wird aus der Aussageform eine [[Aussage]] (Skript Disser, Definition 1.3).",
        r"$B_1(x)$: „Die Zahl $x$ ist gerade.“ Mit der Belegung $x = 4$ entsteht die wahre Aussage $B_1(4)$, mit $x = 5$ die falsche $B_1(5)$.",
        "vl01", ["belegen", "Belegungen"])
eintrag("logische Verknüpfung", "Eine logische Verknüpfung macht aus einer oder zwei Aussagen eine neue Aussage, deren "
        "Wahrheitswert nur von den Wahrheitswerten der Teile abhängt: $\\neg$, $\\land$, $\\lor$, $\\oplus$, $\\Rightarrow$, $\\Leftrightarrow$. "
        "Eine [[Wahrheitstabelle|Wahrheitstafel]] legt sie fest. Zwei Aussagen lassen sich auf $2^4 = 16$ Arten verknüpfen (Bemerkung 1.9).",
        r"$P \land Q$ ist nur wahr, wenn $P$ und $Q$ wahr sind.", "vl01", ["Junktor", "logische Verknüpfungen"])
eintrag("Beweisform", "Ein wiederkehrendes Grundmuster, nach dem ein Beweis aufgebaut ist. In Vorlesung 1: [[direkter Beweis]] "
        "($P$ annehmen, $Q$ herleiten), [[Äquivalenzumformung]], Beweis durch [[Kontraposition]] ($\\neg Q$ annehmen, $\\neg P$ herleiten), "
        "[[Widerspruchsbeweis]] ($P$ und $\\neg Q$ annehmen, $C \\land \\neg C$ herleiten) und [[Fallunterscheidung]].",
        r"Satz 1.17 lässt sich durch Kontraposition und durch Widerspruch beweisen.", "vl01", ["Beweisformen", "Beweismuster"])
