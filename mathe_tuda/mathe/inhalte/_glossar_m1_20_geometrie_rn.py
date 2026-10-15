# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 20: Geometrie des ℝⁿ (Skript Disser, Abschn. 4.1)."""
from .glossar import eintrag

eintrag("Vektor", "Ein $n$-dimensionaler Vektor ist ein Element $\\mathbf{x} = (x_1, \\ldots, x_n)^\\top \\in \\mathbb{R}^n$, als Spalte geschrieben. "
        "Anschaulich: eine Verschiebung oder ein Punkt (Def. 4.1). Allgemeiner heißt jedes Element eines Vektorraums Vektor.",
        r"$(3, 1)^\top \in \mathbb{R}^2$ verschiebt $3$ nach rechts und $1$ nach oben.",
        "geometrie_rn", ["Vektoren", "Spaltenvektor"])
eintrag("Skalar", "Eine Zahl aus dem Körper $K$ (meist $\\mathbb{R}$), mit der man Vektoren multipliziert. "
        "Das Skalarprodukt zweier Vektoren ist dagegen selbst ein Skalar.",
        r"In $2 \cdot (1, 3)^\top = (2, 6)^\top$ ist $2$ der Skalar.",
        "geometrie_rn", ["Skalare"])
eintrag("Einheitsvektor", "Der $j$-te Einheitsvektor $\\mathbf{e}^{(j)}$ hat eine $1$ an Stelle $j$ und sonst $0$ (Def. 4.4). "
        "Jeder Vektor ist $\\mathbf{x} = x_1\\mathbf{e}^{(1)} + \\cdots + x_n\\mathbf{e}^{(n)}$. Allgemein heißt ein Vektor der Länge $1$ ebenfalls Einheitsvektor.",
        r"Im $\mathbb{R}^3$: $\mathbf{e}^{(2)} = (0, 1, 0)^\top$.",
        "geometrie_rn", ["Einheitsvektoren", "kanonischer Einheitsvektor"])
eintrag("Gerade im Raum", "Eine Menge $\\{\\mathbf{p} + t\\mathbf{u} \\mid t \\in \\mathbb{R}\\} \\subseteq \\mathbb{R}^n$ mit Stützvektor $\\mathbf{p}$ und Richtungsvektor $\\mathbf{u} \\neq \\mathbf{0}$ (Def. 4.5). "
        "Durch zwei verschiedene Punkte $\\mathbf{p}, \\mathbf{q}$ verläuft genau eine, nämlich $\\{\\mathbf{p} + t(\\mathbf{q} - \\mathbf{p})\\}$ (Satz 4.6).",
        r"$\{(1, 2)^\top + t(2, 1)^\top \mid t \in \mathbb{R}\}$ geht durch $(1, 2)^\top$ und $(3, 3)^\top$.",
        "geometrie_rn", ["Geradengleichung (Parameterform)", "Parameterform einer Geraden"])
eintrag("Ebene", "Eine Menge $\\{\\mathbf{p} + s\\mathbf{u} + t\\mathbf{v} \\mid s, t \\in \\mathbb{R}\\} \\subseteq \\mathbb{R}^n$, wobei $\\mathbf{u} \\neq \\mathbf{0}$ und $\\mathbf{v}$ kein Vielfaches von $\\mathbf{u}$ ist (Def. 4.5). "
        "Durch drei Punkte, die nicht auf einer Geraden liegen, verläuft genau eine (Satz 4.6).",
        r"$\{s\mathbf{e}^{(1)} + t\mathbf{e}^{(2)}\} \subseteq \mathbb{R}^3$ ist die $x_1$-$x_2$-Ebene.",
        "geometrie_rn", ["Ebenen", "Parameterform einer Ebene"])
eintrag("Stützvektor", "Der Vektor $\\mathbf{p}$ in $\\mathbf{p} + t\\mathbf{u}$ bzw. $\\mathbf{p} + U$: ein beliebiger fester Punkt der Geraden, Ebene oder des affinen Raums, von dem aus man „losgeht“.",
        r"Für $\{(0, 1, 1)^\top + r(1, 1, 1)^\top\}$ ist $(0, 1, 1)^\top$ ein Stützvektor.",
        "geometrie_rn", ["Aufpunkt", "Stützvektoren"])
eintrag("Richtungsvektor", "Ein Vektor $\\mathbf{u} \\neq \\mathbf{0}$, der die Richtung einer Geraden vorgibt, bzw. die zwei Vektoren $\\mathbf{u}, \\mathbf{v}$ einer Ebene (Def. 4.5). Man darf ihn skalieren.",
        r"$(2, 1)^\top$ und $(4, 2)^\top$ sind Richtungsvektoren derselben Geraden.",
        "geometrie_rn", ["Richtungsvektoren"])
eintrag("Standardskalarprodukt", "Für $\\mathbf{x}, \\mathbf{y} \\in \\mathbb{R}^n$ die Zahl $(\\mathbf{x} \\mid \\mathbf{y}) = \\sum_{j=1}^n x_j y_j$ (Def. 4.9). "
        "Symmetrisch und linear in beiden Argumenten. Das Ergebnis ist ein Skalar.",
        r"$(1, 2, 3)^\top$ und $(4, -1, 2)^\top$: $4 - 2 + 6 = 8$.",
        "geometrie_rn", ["Skalarprodukt im ℝⁿ", "inneres Produkt", "Punktprodukt"])
eintrag("euklidische Länge", "$\\lVert\\mathbf{x}\\rVert = \\sqrt{(\\mathbf{x} \\mid \\mathbf{x})} = \\sqrt{\\sum x_j^2}$ (Def. 4.9). Der Abstand von $\\mathbf{x}$ zu $\\mathbf{y}$ ist $\\lVert\\mathbf{x} - \\mathbf{y}\\rVert$. Für $n = 1$ der Betrag.",
        r"$\lVert(2, 3, 6)^\top\rVert = \sqrt{4 + 9 + 36} = 7$.",
        "geometrie_rn", ["euklidische Norm", "Länge eines Vektors", "Vektorlänge"])
eintrag("orthogonal", "Zwei Vektoren heißen orthogonal, $\\mathbf{x} \\perp \\mathbf{y}$, wenn $(\\mathbf{x} \\mid \\mathbf{y}) = 0$ (Def. 4.11). Anschaulich: senkrecht. Der Nullvektor ist zu jedem Vektor orthogonal.",
        r"$(1, 1)^\top \perp (1, -1)^\top$, denn $1 - 1 = 0$.",
        "geometrie_rn", ["senkrecht", "Orthogonalität", "orthogonale Vektoren"])
eintrag("Normalenvektor", "Ein Vektor $\\mathbf{n} \\neq \\mathbf{0}$, der zu den Richtungsvektoren einer Ebene orthogonal ist (Def. 4.11); bei einer Hyperebene $\\{\\mathbf{x} \\mid (\\mathbf{x} \\mid \\mathbf{a}) = b\\}$ ist $\\mathbf{a}$ ein Normalenvektor (Def. 4.14).",
        r"$\mathbf{n} = (2, -2, 1)^\top$ ist Normalenvektor der Ebene $2x_1 - 2x_2 + x_3 = 1$.",
        "geometrie_rn", ["Normalvektor", "Normalenvektoren"])
eintrag("Hyperebene", "Eine Menge $H = \\{\\mathbf{x} \\in \\mathbb{R}^n \\mid (\\mathbf{x} \\mid \\mathbf{a}) = b\\}$ mit $\\mathbf{a} \\neq \\mathbf{0}$ (Def. 4.14). "
        "Sie hat $n - 1$ Freiheitsgrade (Dimension $n - 1$, Satz 4.114). Im $\\mathbb{R}^3$ sind Ebenen und Hyperebenen dasselbe.",
        r"$\{\mathbf{x} \in \mathbb{R}^2 \mid x_1 + 2x_2 = 2\}$ ist eine Gerade, also eine Hyperebene im $\mathbb{R}^2$.",
        "geometrie_rn", ["Hyperebenen"])
eintrag("Kreuzprodukt", "Für $\\mathbf{x}, \\mathbf{y} \\in \\mathbb{R}^3$ der Vektor $\\mathbf{x} \\times \\mathbf{y} = (x_2y_3 - x_3y_2,\\ x_3y_1 - x_1y_3,\\ x_1y_2 - x_2y_1)^\\top$ (Def. 4.18). "
        "Er steht senkrecht auf $\\mathbf{x}$ und $\\mathbf{y}$, und $\\lVert\\mathbf{x} \\times \\mathbf{y}\\rVert$ ist die Fläche des Parallelogramms.",
        r"$\mathbf{e}^{(1)} \times \mathbf{e}^{(2)} = \mathbf{e}^{(3)}$, aber $\mathbf{e}^{(2)} \times \mathbf{e}^{(1)} = -\mathbf{e}^{(3)}$.",
        "geometrie_rn", ["Vektorprodukt", "Kreuzprodukte"])
eintrag("Spatvolumen", "Das Volumen des von $\\mathbf{u}, \\mathbf{v}, \\mathbf{w} \\in \\mathbb{R}^3$ aufgespannten Spats (Parallelepipeds): $|(\\mathbf{u} \\times \\mathbf{v} \\mid \\mathbf{w})|$ (Beob. 4.21). Grundfläche mal Höhe.",
        r"Kanten $(1,0,0)^\top, (1,2,0)^\top, (3,1,4)^\top$: Volumen $|2 \cdot 4| = 8$.",
        "geometrie_rn", ["Spat", "Parallelepiped", "Spatprodukt"])
