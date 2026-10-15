# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 18: Die reellen Zahlen (Skript Disser, Abschn. 3.6)."""
from .glossar import eintrag

eintrag("Vollständigkeitsaxiom", "Das Axiom R2 der reellen Zahlen: Jede nichtleere, nach oben beschränkte Teilmenge von $\\mathbb{R}$ besitzt ein Supremum in $\\mathbb{R}$ (Def. 3.80). "
        "Ein angeordneter Körper mit dieser Eigenschaft heißt vollständig. $\\mathbb{Q}$ ist nicht vollständig.",
        r"$\{t \in \mathbb{Q} \mid t \ge 0,\ t^2 < 2\}$ hat in $\mathbb{R}$ das Supremum $\sqrt{2}$, in $\mathbb{Q}$ keines.",
        "reelle_zahlen", ["Vollständigkeit", "vollständiger angeordneter Körper", "R2"])
eintrag("dicht", "$\\mathbb{Q}$ liegt dicht in $\\mathbb{R}$: Zwischen je zwei reellen Zahlen $x < y$ liegt eine rationale Zahl (Satz 3.86).",
        r"Zwischen $\sqrt{2}$ und $\sqrt{3}$ liegt zum Beispiel $\frac32$.",
        "reelle_zahlen", ["Q liegt dicht", "dicht in R"])
