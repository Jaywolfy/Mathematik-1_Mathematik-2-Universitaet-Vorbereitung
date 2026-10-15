# -*- coding: utf-8 -*-
"""Glossar-Einträge von Vorkurs 4: Quantoren."""
from .glossar import eintrag

eintrag("Allaussage", "Eine Aussage der Form $\\forall x \\in M : E$ („für alle $x$ aus $M$ gilt $E$“). "
        "Sie wird durch ein einziges Gegenbeispiel widerlegt. Ihre Negation ist $\\exists x \\in M : \\neg E$.",
        r"$\forall x \in \mathbb{R} : x^2 \ge 0$", "quantoren", ["Allaussagen"])
eintrag("Existenzaussage", "Eine Aussage der Form $\\exists x \\in M : E$ („es gibt mindestens ein $x$ aus $M$ mit $E$“). "
        "Ein einziges Beispiel beweist sie. Ihre Negation ist $\\forall x \\in M : \\neg E$.",
        r"$\exists x \in \mathbb{N} : x^2 = 4$ (Beispiel $x = 2$)", "quantoren", ["Existenzaussagen"])
