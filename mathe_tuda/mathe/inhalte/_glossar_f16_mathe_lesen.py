# -*- coding: utf-8 -*-
"""Glossar-Einträge von Fundament 16: Mathematik lesen."""
from .glossar import eintrag

eintrag("Quantor", "Ein Zeichen, das sagt, für wie viele Elemente eine Aussage gelten soll: "
        "$\\forall$ (für alle, Allquantor) oder $\\exists$ (es gibt mindestens ein, Existenzquantor).",
        r"$\forall x \in \mathbb{R} : x^2 \ge 0$ ist wahr; $\exists x \in \mathbb{Z} : x^2 = 4$ ist wahr.",
        "mathe_lesen", ["Quantoren", "Allquantor", "Existenzquantor"])
eintrag("Gegenbeispiel", "Ein einzelnes Beispiel, das eine Für-alle-Aussage widerlegt.",
        r"$x = 0$ ist ein Gegenbeispiel zu $\forall x \in \mathbb{R} : x^2 > 0$.", "mathe_lesen", ["Gegenbeispiele"])
eintrag("Index", "Eine tief gestellte Nummer oder Variable, die zusammengehörige Größen unterscheidet. "
        "Nicht zu verwechseln mit dem Exponenten.", r"$x_1, x_2, x_3$ sind drei Zahlen; bei $a_n = 2n + 1$ ist $a_3 = 7$.",
        "mathe_lesen", ["Indizes"])
eintrag("Definition", "Legt fest, was ein Begriff bedeutet. Oft mit $:=$ (ist definiert als) oder $:\\Leftrightarrow$ geschrieben.",
        r"$n \in \mathbb{Z}$ heißt gerade $:\Leftrightarrow \exists k \in \mathbb{Z} : n = 2k$.", "mathe_lesen",
        ["Definitionen"])
eintrag("Satz", "Eine bewiesene mathematische Aussage der Form Voraussetzung $\\Rightarrow$ Behauptung. "
        "Kleinere Sätze heißen Lemma, direkte Folgerungen Korollar.",
        "Sind $m, n$ gerade, so ist $m + n$ gerade.", "mathe_lesen", ["Sätze", "Lemma", "Korollar"])
eintrag("Beweis", "Eine lückenlose Begründung, warum ein Satz gilt. Sie beginnt bei der Voraussetzung und endet mit "
        "der Behauptung, markiert durch $\\square$ oder „q.e.d.“.", r"$m + n = 2k + 2l = 2(k + l)$, also gerade. $\square$",
        "mathe_lesen", ["Beweise"])
