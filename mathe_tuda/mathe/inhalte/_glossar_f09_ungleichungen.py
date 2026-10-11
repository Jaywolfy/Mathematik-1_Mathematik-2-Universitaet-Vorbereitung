# -*- coding: utf-8 -*-
"""Glossar-Einträge zu Fundament 9: Ungleichungen."""
from .glossar import eintrag

eintrag("Ungleichung", r"Zwei Terme, verbunden durch $<$, $\le$, $>$ oder $\ge$. Die Lösungsmenge ist meist ein ganzer Bereich. "
        "Beim Malnehmen oder Teilen mit einer negativen Zahl dreht sich das Zeichen um.",
        r"$-3x \le 6 \iff x \ge -2$, also $\mathbb{L} = [-2, \infty)$.", "ungleichungen", ["Ungleichungen"])
eintrag("Intervall", r"Ein lückenloser Bereich der Zahlengeraden. Eckige Klammer: Rand gehört dazu. Runde Klammer: Rand gehört "
        r"nicht dazu. Bei $\infty$ steht immer eine runde Klammer. Statt $(a, b]$ schreibt man auch $]a, b]$.",
        r"$(-2, 3] = \{x \in \mathbb{R} : -2 < x \le 3\}$", "ungleichungen", ["Intervalle"])
eintrag("Doppelungleichung", "Zwei Ungleichungen in einer Zeile, die beide gelten müssen. Man formt alle drei Teile gleichzeitig um.",
        r"$-1 < 2x + 3 \le 7 \iff -2 < x \le 2$", "ungleichungen", ["Doppelungleichungen"])
eintrag("Fallunterscheidung", "Man rechnet mehrere Fälle getrennt, zum Beispiel $x > 0$ und $x < 0$, weil eine Umformung "
        "vom Fall abhängt. Am Ende vereinigt man die Ergebnisse aller Fälle.",
        r"$\frac{6}{x} > 2$: Für $x > 0$ folgt $0 < x < 3$, für $x < 0$ gibt es keine Lösung. Also $\mathbb{L} = (0, 3)$.",
        "ungleichungen", ["Fallunterscheidungen"])
