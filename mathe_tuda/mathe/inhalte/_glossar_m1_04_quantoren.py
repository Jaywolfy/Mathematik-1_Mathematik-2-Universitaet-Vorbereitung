# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 4: All- und Existenzquantor (Disser 1.5)."""
from .glossar import eintrag

eintrag("Mengensystem", "Eine Menge, deren Elemente selbst Mengen sind, z. B. eine Menge $\\mathcal{M}$ von Teilmengen einer "
        "Grundmenge $G$. Über ein Mengensystem bildet man Vereinigung und Schnitt (Definition 1.34).",
        r"$\mathcal{M} = \{\{1, 2\}, \{2, 3\}\}$ hat $\bigcup = \{1, 2, 3\}$ und $\bigcap = \{2\}$.", "uni_quantoren",
        ["Mengensysteme", "Mengenfamilie"])
eintrag("leerer Schnitt", "Der Schnitt über das leere Mengensystem: $\\bigcap_{M \\in \\emptyset} M = G$. "
        "Er ist die ganze Grundmenge, weil die Bedingung „$x$ liegt in allen $M \\in \\emptyset$“ für jedes $x$ wahr ist. "
        "Die leere Vereinigung ist dagegen $\\emptyset$.",
        r"Ohne Grundmenge $G$ wäre der leere Schnitt „alles“, und das ist keine Menge.", "uni_quantoren",
        ["leerer Durchschnitt"])
