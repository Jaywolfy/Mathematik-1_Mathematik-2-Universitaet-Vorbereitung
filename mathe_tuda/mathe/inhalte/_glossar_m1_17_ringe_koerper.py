# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 17: Ringe, Körper und die rationalen Zahlen (Skript Disser, Abschn. 3.3 bis 3.5)."""
from .glossar import eintrag

eintrag("Ring", "Ein Tupel $(R, +, \\cdot)$, in dem $(R, +)$ eine abelsche Gruppe ist, die Multiplikation assoziativ ist und die "
        "Distributivgesetze gelten (Def. 3.46). Mit Eins, wenn es $1$ mit $1a = a1 = a$ gibt; kommutativ, wenn $ab = ba$.",
        r"$(\mathbb{Z}, +, \cdot)$ und $(\mathbb{Z}/n\mathbb{Z}, +, \cdot)$ sind kommutative Ringe mit Eins.",
        "ringe_koerper", ["Ringe", "Ring mit Eins", "kommutativer Ring"])
eintrag("Restklassenring", "Die Menge $\\mathbb{Z}/n\\mathbb{Z}$ mit $[a]_n + [b]_n = [a + b]_n$ und $[a]_n \\cdot [b]_n = [ab]_n$ (Def. 3.49). "
        "Ein kommutativer Ring mit Nullelement $[0]_n$ und Einselement $[1]_n$ (Satz 3.50).",
        r"In $\mathbb{Z}/12\mathbb{Z}$ gilt $[5] \cdot [7] = [35] = [11]$.",
        "ringe_koerper", ["Restklassenringe", "Z/nZ"])
eintrag("Nullteiler", "Ein Element $a \\ne 0$ eines kommutativen Rings, zu dem es $b \\ne 0$ mit $ab = 0$ gibt (Def. 3.52). "
        "Dann ist $x \\mapsto ax$ nicht injektiv, und Kürzen ist unmöglich (Satz 3.53). Ein Ring ohne Nullteiler heißt nullteilerfrei.",
        r"In $\mathbb{Z}/4\mathbb{Z}$ ist $[2]$ ein Nullteiler: $[2] \cdot [2] = [0]$.",
        "ringe_koerper", ["nullteilerfrei", "Nullteilerfreiheit", "Nullteiler (Ring)"])
eintrag("Ringhomomorphismus", "Eine Abbildung $f\\colon R \\to S$ zwischen Ringen mit Eins mit $f(a + b) = f(a) \\oplus f(b)$, "
        "$f(a \\cdot b) = f(a) \\star f(b)$ und $f(1_R) = 1_S$ (Def. 3.55).",
        r"$\pi_n\colon \mathbb{Z} \to \mathbb{Z}/n\mathbb{Z},\ a \mapsto [a]_n$.",
        "ringe_koerper", ["Ringhomomorphismen", "Ringisomorphismus"])
eintrag("Körper", "Ein kommutativer Ring $(K, +, \\cdot)$ mit Eins, in dem $(K \\setminus \\{0\\}, \\cdot)$ eine Gruppe ist (Def. 3.64): "
        "Jedes $a \\ne 0$ hat ein multiplikatives Inverses. Körper haben keine Nullteiler und es gilt $0 \\ne 1$.",
        r"$\mathbb{Q}$, $\mathbb{R}$, $\mathbb{C}$ und $\mathbb{Z}/p\mathbb{Z}$ für Primzahlen $p$.",
        "ringe_koerper", ["Körper (algebraisch)", "Körperaxiome"])
eintrag("Körperhomomorphismus", "Ein Ringhomomorphismus zwischen zwei Körpern (Def. 3.71). Er ist immer injektiv (Satz 3.73), "
        "sein Bild ist wieder ein Körper (Satz 3.75).",
        r"Die Einbettung $\mathbb{R} \to \mathbb{C},\ x \mapsto (x, 0)$.",
        "ringe_koerper", ["Körperhomomorphismen", "Körperisomorphismus"])
eintrag("angeordneter Körper", "Ein Körper mit einer Totalordnung $\\le$, die mit Addition und Multiplikation verträglich ist: "
        "$a \\le b \\Rightarrow a + c \\le b + c$ und $a \\le b,\\ 0 \\le c \\Rightarrow ac \\le bc$ (Def. 3.76). Quadrate sind $\\ge 0$ (Satz 3.78).",
        r"$\mathbb{Q}$ und $\mathbb{R}$ sind angeordnet, $\mathbb{C}$ und $\mathbb{Z}/5\mathbb{Z}$ nicht.",
        "ringe_koerper", ["angeordnete Körper", "geordneter Körper"])
