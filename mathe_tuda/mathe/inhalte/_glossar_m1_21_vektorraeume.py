# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 21: Vektorräume und Untervektorräume (Skript Disser, Abschn. 4.2 und 4.3)."""
from .glossar import eintrag

eintrag("Vektorraum", "Eine Menge $V \\neq \\emptyset$ mit Addition $+\\colon V^2 \\to V$ und Skalarmultiplikation $\\cdot\\colon K \\times V \\to V$ über einem Körper $K$, "
        "so dass $(V, +)$ eine abelsche Gruppe ist und (d1) $\\lambda(v + w) = \\lambda v + \\lambda w$, (d2) $(\\lambda + \\mu)v = \\lambda v + \\mu v$, (a) $\\lambda(\\mu v) = (\\lambda\\mu)v$, (e) $1v = v$ gelten (Def. 4.23).",
        r"$\mathbb{R}^n$, der Polynomraum $K[X]$, der Funktionenraum $\mathrm{abb}(M, K)$, $(\mathbb{Z}/2\mathbb{Z})^n$ (Bitstrings mit XOR).",
        "vektorraeume", ["Vektorräume", "linearer Raum", "K-Vektorraum"])
eintrag("Nullvektor", "Das neutrale Element $0_V$ der Addition in einem Vektorraum. Es gilt $0v = 0_V$ für jeden Vektor $v$ (Satz 4.30). Jeder Untervektorraum enthält ihn.",
        r"Im $\mathbb{R}^3$: $(0, 0, 0)^\top$. Im Funktionenraum: die Nullfunktion $t \mapsto 0$.",
        "vektorraeume", ["Nullelement des Vektorraums"])
eintrag("Untervektorraum", "Eine Teilmenge $U \\subseteq V$, die mit den eingeschränkten Verknüpfungen selbst ein Vektorraum ist (Def. 4.31). "
        "Nach Satz 4.32 genau dann, wenn $U \\neq \\emptyset$ und $\\lambda u + \\mu w \\in U$ für alle $u, w \\in U$, $\\lambda, \\mu \\in K$.",
        r"Ursprungsgeraden und -ebenen im $\mathbb{R}^n$; $\{\mathbf{x} \in \mathbb{R}^3 \mid x_1 + x_2 = 0\}$. Keiner: $\{\mathbf{x} \mid x_2 = 2x_1 + 1\}$ (ohne Nullvektor).",
        "vektorraeume", ["Unterraum", "Untervektorräume", "Teilraum", "Unterräume"])
eintrag("Unterraumkriterium", "Satz 4.32: $U \\subseteq V$ ist ein Untervektorraum genau dann, wenn $U \\neq \\emptyset$ und $\\lambda u + \\mu w \\in U$ für alle $u, w \\in U$, $\\lambda, \\mu \\in K$. "
        "In der Praxis: $0 \\in U$ prüfen, dann Abgeschlossenheit unter Summe und Vielfachen.",
        r"$U = \{\mathbf{x} \in \mathbb{R}^2 \mid x_1 = x_2\}$: $\mathbf{0} \in U$, und $\lambda(a, a)^\top + \mu(b, b)^\top = (\lambda a + \mu b)(1, 1)^\top \in U$.",
        "vektorraeume", ["Untervektorraumkriterium"])
eintrag("Funktionenraum", "Der Vektorraum $\\mathrm{abb}(M, K)$ aller Abbildungen $M \\to K$ mit punktweiser Addition $(f + g)(x) = f(x) + g(x)$ und Skalarmultiplikation $(\\lambda f)(x) = \\lambda f(x)$ (Bsp. 4.28). "
        "Nullvektor ist die Nullfunktion.",
        r"$F = \{t \mapsto a + bt\} \subseteq \mathrm{abb}(\mathbb{R}, \mathbb{R})$: $(2f + 3g)(t)$ rechnet man Wert für Wert.",
        "vektorraeume", ["Funktionenräume", "Abbildungsraum"])
eintrag("Linearkombination", "Zu Vektoren $v^{(1)}, \\ldots, v^{(m)}$ und Koeffizienten $\\lambda_1, \\ldots, \\lambda_m \\in K$ der Vektor $\\sum_{j=1}^m \\lambda_j v^{(j)}$ (Def. 4.41). Die leere Linearkombination ist $0$.",
        r"$2(1, 0)^\top - 3(0, 1)^\top = (2, -3)^\top$ ist eine Linearkombination von $\mathbf{e}^{(1)}, \mathbf{e}^{(2)}$.",
        "vektorraeume", ["Linearkombinationen"])
eintrag("lineare Hülle", "Für $M \\subseteq V$ der Schnitt $\\langle M \\rangle$ aller Untervektorräume von $V$, die $M$ enthalten (Def. 4.37): der kleinste solche Untervektorraum. "
        "Nach Satz 4.42 besteht sie genau aus den Linearkombinationen endlich vieler Vektoren aus $M$; $\\langle \\emptyset \\rangle = \\{0\\}$.",
        r"$\langle (1, -1, 0)^\top, (0, 0, 1)^\top \rangle = \{\mathbf{x} \in \mathbb{R}^3 \mid x_1 + x_2 = 0\}$.",
        "vektorraeume", ["Hülle", "Spann", "span", "aufgespannter Raum"])
eintrag("Erzeugendensystem", "Eine Menge $M \\subseteq V$ mit $\\langle M \\rangle = V$ (Def. 4.37): Jeder Vektor ist eine Linearkombination von Vektoren aus $M$.",
        r"$\{\mathbf{e}^{(1)}, \ldots, \mathbf{e}^{(n)}\}$ erzeugt $\mathbb{R}^n$; $\{X^j \mid j \in \mathbb{N}\}$ erzeugt $K[X]$.",
        "vektorraeume", ["Erzeugendensysteme", "erzeugt", "Erzeuger"])
