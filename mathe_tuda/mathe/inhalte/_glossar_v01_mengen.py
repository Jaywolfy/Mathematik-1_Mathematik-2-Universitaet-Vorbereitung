# -*- coding: utf-8 -*-
"""Glossar-Einträge von Vorkurs 1: Mengen."""
from .glossar import eintrag

eintrag("Grundmenge", "Die Menge, aus der die Elemente ausgewählt werden, z. B. $\\mathbb{N}$ oder $\\mathbb{R}$. "
        "Auch das Komplement wird bezüglich der Grundmenge gebildet.",
        r"In $\{x \in \mathbb{Z} : x^2 < 5\}$ ist $\mathbb{Z}$ die Grundmenge.", "mengen")
eintrag("leere Menge", "Die Menge ohne jedes Element, Zeichen $\\emptyset$. Sie ist Teilmenge jeder Menge.",
        r"$\{x \in \mathbb{N} : x < 1\} = \emptyset$, aber $\{0\} \neq \emptyset$.", "mengen")
eintrag("Vereinigung", "$A \\cup B$ enthält alle Elemente, die in $A$ oder in $B$ (oder in beiden) liegen.",
        r"$\{1, 2\} \cup \{2, 3\} = \{1, 2, 3\}$", "mengen", ["Vereinigungsmenge"])
eintrag("Durchschnitt", "$A \\cap B$ enthält genau die Elemente, die in $A$ und in $B$ liegen.",
        r"$\{1, 2\} \cap \{2, 3\} = \{2\}$", "mengen", ["Schnittmenge"])
eintrag("Differenzmenge", "$A \\setminus B$ („$A$ ohne $B$“) enthält die Elemente von $A$, die nicht in $B$ liegen.",
        r"$\{1, 2, 3\} \setminus \{2\} = \{1, 3\}$", "mengen")
eintrag("Komplement", "Das Komplement $A^C$ (auch $\\overline{A}$) enthält alle Elemente der Grundmenge $G$, "
        "die nicht in $A$ liegen.", r"In $G = \{1, 2, 3, 4\}$ ist $\{1, 2\}^C = \{3, 4\}$.", "mengen",
        ["Komplementmenge"])
eintrag("Kommutativgesetz", "Die Reihenfolge darf vertauscht werden, ohne dass sich das Ergebnis ändert.",
        r"$A \cup B = B \cup A$, $A \cap B = B \cap A$, $a + b = b + a$; aber $A \setminus B \neq B \setminus A$.",
        "mengen", ["Kommutativgesetze", "kommutativ"])
eintrag("Mächtigkeit", "Die Anzahl der Elemente einer endlichen Menge $A$, geschrieben $|A|$.",
        r"$|\{1, 2, 5, 9\}| = 4$, $|\emptyset| = 0$", "mengen")
eintrag("Potenzmenge", "Die Menge $\\mathcal{P}(A)$ aller Teilmengen von $A$. Hat $A$ genau $n$ Elemente, "
        "hat $\\mathcal{P}(A)$ genau $2^n$ Elemente.",
        r"$\mathcal{P}(\{a, b\}) = \{\emptyset, \{a\}, \{b\}, \{a, b\}\}$", "mengen")
eintrag("geordnetes Paar", "Zwei Objekte in fester Reihenfolge, geschrieben $(a, b)$. Anders als bei Mengen gilt "
        "$(a, b) \\neq (b, a)$, wenn $a \\neq b$.", r"$(1, 2) \neq (2, 1)$, aber $\{1, 2\} = \{2, 1\}$.", "mengen",
        ["geordnete Paare"])
eintrag("kartesisches Produkt", "$A \\times B$ ist die Menge aller geordneten Paare $(a, b)$ mit $a \\in A$ und $b \\in B$. "
        "Es gilt $|A \\times B| = |A| \\cdot |B|$.",
        r"$\{1, 2\} \times \{x\} = \{(1, x), (2, x)\}$; $\mathbb{R} \times \mathbb{R} = \mathbb{R}^2$", "mengen")
