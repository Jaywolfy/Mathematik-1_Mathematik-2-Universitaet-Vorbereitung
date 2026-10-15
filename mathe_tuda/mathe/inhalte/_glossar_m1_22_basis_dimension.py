# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 22: Basen und Dimension (Skript Disser, Abschn. 4.4 und 4.5)."""
from .glossar import eintrag

eintrag("linear unabhängig", "Eine Menge $M \\subseteq V$ ist linear unabhängig, wenn für paarweise verschiedene $v^{(1)}, \\ldots, v^{(m)} \\in M$ aus $\\sum_j \\lambda_j v^{(j)} = 0$ stets $\\lambda = 0$ folgt (Def. 4.47). "
        "Gleichwertig (Satz 4.52): Kein Vektor der Menge liegt in der linearen Hülle der übrigen.",
        r"$\{(1, 0)^\top, (0, 1)^\top\}$ ist unabhängig. $\emptyset$ ist unabhängig.",
        "basis_dimension", ["linear unabhängige Menge", "Unabhängigkeit", "unabhängig"])
eintrag("linear abhängig", "Das Gegenteil von linear unabhängig: Es gibt eine Linearkombination paarweise verschiedener Vektoren mit nicht allen Koeffizienten $0$, die $0$ ergibt. "
        "Dann ist ein Vektor überflüssig (Satz 4.52). Jede Menge mit dem Nullvektor ist abhängig.",
        r"$\{\mathbf{e}^{(1)}, \mathbf{e}^{(2)}, \mathbf{e}^{(1)} + \mathbf{e}^{(2)}\}$, denn $1\mathbf{e}^{(1)} + 1\mathbf{e}^{(2)} - 1(\mathbf{e}^{(1)} + \mathbf{e}^{(2)}) = \mathbf{0}$.",
        "basis_dimension", ["Abhängigkeit", "abhängig"])
eintrag("Basis (Vektorraum)", "Eine linear unabhängige Menge $B \\subseteq V$ mit $\\langle B \\rangle = V$ (Def. 4.54). Sie ist ein minimales Erzeugendensystem und eine maximale linear unabhängige Menge. "
        "Geordnet: Tupel $\\mathfrak{B} = (b^{(1)}, \\ldots, b^{(n)})$.",
        r"Standardbasis $\{\mathbf{e}^{(1)}, \ldots, \mathbf{e}^{(n)}\}$ von $K^n$; die Monome von $K[X]$; $\{1, i\}$ von $\mathbb{C}$ über $\mathbb{R}$.",
        "basis_dimension", ["Vektorraumbasis", "geordnete Basis", "Basen"])
eintrag("Standardbasis", "Die Basis $\\{\\mathbf{e}^{(1)}, \\ldots, \\mathbf{e}^{(n)}\\}$ von $K^n$ aus den Einheitsvektoren (Bsp. 4.58). Die geordnete Standardbasis ist $\\mathfrak{E} = (\\mathbf{e}^{(1)}, \\ldots, \\mathbf{e}^{(n)})$, und es gilt $[\\mathbf{x}]_{\\mathfrak{E}} = \\mathbf{x}$.",
        r"Standardbasis des $\mathbb{R}^2$: $(1, 0)^\top, (0, 1)^\top$.",
        "basis_dimension", ["kanonische Basis", "Standardbasen"])
eintrag("Koordinatenvektor", "Zu einer geordneten Basis $\\mathfrak{B} = (b^{(1)}, \\ldots, b^{(n)})$ und $v = \\sum_j x_j b^{(j)}$ der Vektor $[v]_{\\mathfrak{B}} = (x_1, \\ldots, x_n)^\\top \\in K^n$ (Def. 4.61). "
        "Er ist nach Satz 4.55 eindeutig bestimmt und hängt von der Basis und ihrer Reihenfolge ab.",
        r"$\mathfrak{B} = ((1, 1)^\top, (1, 0)^\top)$ und $\mathbf{x} = (2, 1)^\top$: $[\mathbf{x}]_{\mathfrak{B}} = (1, 1)^\top$.",
        "basis_dimension", ["Koordinaten", "Koordinatentupel", "Koordinatenvektoren"])
eintrag("Austauschsatz", "Satz 4.64: Ist $E$ ein endliches Erzeugendensystem von $V$, so ist jede linear unabhängige Menge $L$ endlich und $|L| \\le |E|$. "
        "Folgerung (Kor. 4.65): Alle Basen eines endlich erzeugten Vektorraums haben gleich viele Elemente.",
        r"Im $\mathbb{R}^3$ (Erzeugendensystem mit $3$ Elementen) gibt es keine vier linear unabhängigen Vektoren.",
        "basis_dimension", ["Steinitzscher Austauschsatz"])
eintrag("Basisergänzung", "Korollar 4.66: Zu einem endlichen Erzeugendensystem $E$ und einer linear unabhängigen Menge $L$ gibt es eine Basis $B$ mit $L \\subseteq B \\subseteq L \\cup E$. "
        "Man ergänzt $L$ also um Vektoren aus $E$ zu einer Basis (Basisauswahl für $L = \\emptyset$).",
        r"$L = \{(1, 1, 0)^\top\}$ lässt sich mit $\mathbf{e}^{(1)}, \mathbf{e}^{(3)}$ zur Basis des $\mathbb{R}^3$ ergänzen.",
        "basis_dimension", ["Basisauswahl", "Basisergänzungssatz"])
eintrag("Dimension", "Die Anzahl $\\dim_K V := |B|$ der Elemente einer Basis (Def. 4.67), nach Kor. 4.65 unabhängig von der Basis. "
        "Der Körper gehört dazu: $\\dim_{\\mathbb{R}} \\mathbb{C} = 2$, $\\dim_{\\mathbb{C}} \\mathbb{C} = 1$. Ohne endliche Basis heißt $V$ unendlichdimensional. "
        "Für affine Räume $p + U$ ist es $\\dim U$.",
        r"$\dim K^n = n$, Gerade durch $0$: $1$, Ebene durch $0$: $2$, $\dim K[X] = \infty$.",
        "basis_dimension", ["Vektorraumdimension", "dim", "endlichdimensional", "unendlichdimensional"])
eintrag("Dimensionsformel für Untervektorräume", "Satz 4.75: Für Untervektorräume $U, W$ eines endlichdimensionalen Raums gilt $\\dim(U + W) = \\dim U + \\dim W - \\dim(U \\cap W)$, "
        "wobei $U + W = \\{u + w \\mid u \\in U, w \\in W\\}$.",
        r"Zwei Ebenen im $\mathbb{R}^3$ mit Schnittgerade: $2 + 2 - 1 = 3$.",
        "basis_dimension", ["Dimensionsformel", "Dimensionssatz für Unterräume"])
