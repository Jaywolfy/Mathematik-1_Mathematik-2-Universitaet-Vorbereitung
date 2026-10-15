# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 19: Die komplexen Zahlen (Skript Disser, Abschn. 3.7 und 3.8)."""
from .glossar import eintrag

eintrag("komplexe Zahl", "Ein Element von $\\mathbb{C} := \\mathbb{R}^2$ (Def. 3.94), geschrieben $z = x + yi$ mit $x, y \\in \\mathbb{R}$ "
        "(kartesische Darstellung, Beob. 3.98). Addition komponentenweise, Multiplikation $(x_1, y_1)(x_2, y_2) = (x_1x_2 - y_1y_2,\\ x_1y_2 + y_1x_2)$.",
        r"$(2 + 3i)(1 - 5i) = 17 - 7i$.",
        "komplexe_zahlen_uni", ["komplexe Zahlen", "kartesische Darstellung", "C"])
eintrag("imaginäre Einheit", "Die komplexe Zahl $i := (0, 1)$ mit $i^2 = -1$ (Def. 3.97, Beob. 3.98). Die Gleichung $x^2 + 1 = 0$ hat die Lösungen $i$ und $-i$.",
        r"$i^2 = -1$, $i^3 = -i$, $i^4 = 1$.",
        "komplexe_zahlen_uni", ["imaginäre Zahl", "i"])
eintrag("Realteil", "Zu $z = x + yi$ der reelle Anteil $\\operatorname{Re}(z) := x$ (Def. 3.97).",
        r"$\operatorname{Re}(3 - 4i) = 3$.",
        "komplexe_zahlen_uni", ["Re"])
eintrag("Imaginärteil", "Zu $z = x + yi$ der reelle Koeffizient von $i$: $\\operatorname{Im}(z) := y$ (Def. 3.97). Er enthält das $i$ nicht.",
        r"$\operatorname{Im}(3 - 4i) = -4$, nicht $-4i$.",
        "komplexe_zahlen_uni", ["Im"])
eintrag("konjugiert komplexe Zahl", "Zu $z = x + yi$ die Zahl $\\bar z := x - yi$ (Def. 3.102): Spiegelung an der reellen Achse. "
        "Es gilt $z\\bar z = |z|^2$, und $z \\mapsto \\bar z$ ist ein Körperautomorphismus von $\\mathbb{C}$ (Satz 3.105).",
        r"$\overline{3 + 4i} = 3 - 4i$, $(3 + 4i)(3 - 4i) = 25 = |3 + 4i|^2$.",
        "komplexe_zahlen_uni", ["Konjugation", "konjugiert komplex"])
eintrag("komplexe Ebene", "Die Darstellung von $\\mathbb{C} = \\mathbb{R}^2$ als Ebene: $x + yi$ liegt bei $(x, y)$, Realteil auf der waagerechten, Imaginärteil auf der senkrechten Achse. "
        "Die Addition ist Vektoraddition, die Multiplikation eine Drehstreckung.",
        r"$3 + 4i$ liegt bei $(3, 4)$ im Abstand $5$ vom Ursprung.",
        "komplexe_zahlen_uni", ["Gaußsche Zahlenebene", "Zahlenebene", "gaußsche Ebene"])
eintrag("algebraisch abgeschlossen", "Ein Körper $K$, in dem jedes Polynom von positivem Grad eine Nullstelle hat (Def. 3.108). $\\mathbb{C}$ ist es, $\\mathbb{R}$ und $\\mathbb{Q}$ nicht.",
        r"$X^2 + 1$ hat in $\mathbb{R}$ keine Nullstelle, in $\mathbb{C}$ die Nullstellen $\pm i$.",
        "komplexe_zahlen_uni", ["algebraisch abgeschlossener Körper"])
eintrag("Fundamentalsatz der Algebra", "Jedes Polynom $p$ über $\\mathbb{C}$ vom Grad $n$ hat die Form $p(X) = a \\prod_{j=1}^{n}(X - z_j)$ mit $a, z_j \\in \\mathbb{C}$: "
        "es zerfällt in Linearfaktoren (Satz 3.109, ohne Beweis).",
        r"$X^4 - 1 = (X - 1)(X + 1)(X - i)(X + i)$.",
        "komplexe_zahlen_uni", ["Fundamentalsatz", "Zerfall in Linearfaktoren"])
