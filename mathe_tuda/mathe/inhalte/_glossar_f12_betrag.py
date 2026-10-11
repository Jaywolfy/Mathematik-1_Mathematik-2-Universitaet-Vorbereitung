# -*- coding: utf-8 -*-
"""Glossar-Einträge zu Fundament 12: Betrag."""
from .glossar import eintrag

eintrag("Betrag", "Der Abstand einer Zahl zur $0$ auf der Zahlengeraden. Er ist nie negativ: "
        "$|x| = x$ für $x \\ge 0$ und $|x| = -x$ für $x < 0$. $|a - b|$ ist der Abstand von $a$ und $b$.",
        r"$|-3| = 3$, $|3| = 3$, $|2 - 7| = 5$", "betrag", ["Absolutbetrag", "Beträge", "Betragsfunktion"])
eintrag("Dreiecksungleichung", "Für alle reellen Zahlen $a, b$ gilt $|a + b| \\le |a| + |b|$: "
        "Ein Umweg ist nie kürzer als der direkte Weg.",
        r"$|3 + (-5)| = 2 \le 8 = |3| + |-5|$", "betrag")
