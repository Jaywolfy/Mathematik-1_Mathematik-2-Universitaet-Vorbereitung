# -*- coding: utf-8 -*-
"""Glossar-Einträge von Vorkurs 10: Funktionen, Bild und Urbild."""
from .glossar import eintrag

eintrag("Abbildung", "Anderes Wort für [[Funktion]]: eine Vorschrift $f\\colon D \\to W$, die jedem $x \\in D$ "
        "genau ein $f(x) \\in W$ zuordnet. In der Uni-Mathematik sind beide Wörter gleichbedeutend.",
        r"$g\colon \{\text{Dreieck}, \text{Quadrat}\} \to \mathbb{N},\ x \mapsto$ Anzahl der Ecken ist eine Abbildung.",
        "abbildungen", ["Abbildungen"])
eintrag("maximaler Definitionsbereich", "Die größte Menge reeller Zahlen, für die eine Vorschrift einen Wert liefert: "
        "kein Nenner $0$, nichts Negatives unter einer Quadratwurzel.",
        r"$x \mapsto \frac{1}{x}$ hat den maximalen Definitionsbereich $\mathbb{R} \setminus \{0\}$.",
        "abbildungen", ["maximale Definitionsbereich", "maximalen Definitionsbereich"])
eintrag("Bild", "Für $f\\colon D \\to W$ und $A \\subseteq D$ ist $f(A) = \\{f(x) : x \\in A\\}$ die Menge der Funktionswerte "
        "aller $x \\in A$. $f(D)$ heißt Bild (Bildmenge) von $f$. Das Bild von $x$ ist der einzelne Wert $f(x)$.",
        r"$f\colon \mathbb{R} \to \mathbb{R},\ x \mapsto x^2$ hat das Bild $f(\mathbb{R}) = \mathbb{R}_{\ge 0}$.",
        "abbildungen", ["Bildmenge"])
eintrag("Urbild", "Für $f\\colon D \\to W$ und $B \\subseteq W$ ist $f^{-1}(B) = \\{x \\in D : f(x) \\in B\\}$ das Urbild von $B$. "
        "Es existiert für jede Funktion, auch ohne Umkehrfunktion. Ein $x$ mit $f(x) = y$ heißt Urbild von $y$.",
        r"Für $x \mapsto x^2$ auf $\mathbb{R}$ ist $f^{-1}(\{4\}) = \{-2, 2\}$ und $f^{-1}(\{-1\}) = \emptyset$.",
        "abbildungen", ["Urbilder", "Urbildmenge"])
