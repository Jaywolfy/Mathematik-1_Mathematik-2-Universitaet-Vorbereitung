# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 6: Ordnungen, Supremum und Infimum (Skript Disser, Abschn. 1.6)."""
from .glossar import eintrag

eintrag("Ordnungsrelation", "Eine Relation auf $M$, die reflexiv, antisymmetrisch und transitiv ist. Man schreibt "
        "sie oft $\\preccurlyeq$ (Skript Disser, Def. 1.42).",
        r"$\le$ auf $\mathbb{N}$, $\subseteq$ auf $\mathcal{P}(M)$, Teilbarkeit $\mid$ auf $\mathbb{N}$.",
        "ordnungen", ["Ordnungsrelationen", "partielle Ordnung", "Halbordnung"])
eintrag("partiell geordnete Menge", "Ein Paar $(M, \\preccurlyeq)$ aus einer Menge $M$ und einer Ordnungsrelation "
        "$\\preccurlyeq$ auf $M$. „Partiell“ heißt: Es dürfen unvergleichbare Elemente vorkommen, es muss aber nicht.",
        r"$(\mathcal{P}(\{1, 2\}), \subseteq)$: $\{1\}$ und $\{2\}$ sind unvergleichbar.",
        "ordnungen", ["partiell geordnete Mengen", "Poset"])
eintrag("Totalordnung", "Eine Ordnungsrelation $\\preccurlyeq$ auf $M$, bei der je zwei Elemente vergleichbar sind: "
        "$\\forall x, y \\in M : x \\preccurlyeq y \\lor y \\preccurlyeq x$. $(M, \\preccurlyeq)$ heißt dann total geordnet.",
        r"$\le$ auf $\mathbb{N}, \mathbb{Z}, \mathbb{Q}, \mathbb{R}$ (Bsp. 1.43).",
        "ordnungen", ["total geordnete Menge", "totale Ordnung", "total geordnet"])
eintrag("Maximum", "Ein $x \\in M$ mit $y \\preccurlyeq x$ für alle $y \\in M$; geschrieben $\\max M$. Es gibt höchstens "
        "eins (Satz 1.47), oft aber keins.",
        r"$\max\, (0, 1] = 1$; $(\mathbb{N}, \le)$ hat kein Maximum.",
        "ordnungen", ["Maxima", "größtes Element"])
eintrag("Minimum", "Ein $x \\in M$ mit $x \\preccurlyeq y$ für alle $y \\in M$; geschrieben $\\min M$. Es gibt höchstens "
        "eins (Satz 1.47).",
        r"$\min \mathbb{N} = 0$; $(0, 1]$ hat in $(\mathbb{R}, \le)$ kein Minimum.",
        "ordnungen", ["Minima", "kleinstes Element"])
eintrag("obere Schranke", "Ein $x \\in M$ mit $y \\preccurlyeq x$ für alle $y \\in N$ (für $N \\subseteq M$). "
        "$x$ muss nicht in $N$ liegen (Def. 1.52).",
        r"$5$ ist in $(\mathbb{R}, \le)$ eine obere Schranke von $(0, 1]$.",
        "ordnungen", ["obere Schranken"])
eintrag("untere Schranke", "Ein $x \\in M$ mit $x \\preccurlyeq y$ für alle $y \\in N$ (für $N \\subseteq M$) (Def. 1.52).",
        r"$-7$ ist in $(\mathbb{R}, \le)$ eine untere Schranke von $(0, 1]$.",
        "ordnungen", ["untere Schranken"])
eintrag("nach oben beschränkt", "$N \\subseteq M$ heißt nach oben (bzw. unten) beschränkt, wenn es eine obere (bzw. "
        "untere) Schranke in $M$ gibt, und beschränkt, wenn beides gilt (Def. 1.52 (iii)).",
        r"$\mathbb{N}$ ist in $(\mathbb{Z}, \le)$ nach unten, aber nicht nach oben beschränkt.",
        "ordnungen", ["nach unten beschränkt", "beschränkte Menge"])
eintrag("Supremum", "Die kleinste obere Schranke: $\\sup N := \\min\\{x \\in M \\mid x$ ist obere Schranke von $N\\}$, "
        "sofern dieses Minimum existiert (Def. 1.53). Es muss nicht in $N$ liegen.",
        r"In $(\mathbb{R}, \le)$: $\sup\, (0, 1) = 1$. In $(\mathcal{P}(M), \subseteq)$: Supremum = Vereinigung.",
        "ordnungen", ["Suprema", "kleinste obere Schranke"])
eintrag("Infimum", "Die größte untere Schranke: $\\inf N := \\max\\{x \\in M \\mid x$ ist untere Schranke von $N\\}$, "
        "sofern dieses Maximum existiert (Def. 1.53).",
        r"In $(\mathbb{R}, \le)$: $\inf\, (0, 1] = 0 \notin (0, 1]$ (Bsp. 1.54).",
        "ordnungen", ["Infima", "größte untere Schranke"])
