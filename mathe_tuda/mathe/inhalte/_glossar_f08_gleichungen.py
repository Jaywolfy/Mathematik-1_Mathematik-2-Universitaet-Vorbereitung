# -*- coding: utf-8 -*-
"""Glossar-Einträge zu Fundament 8: Gleichungen und Formeln umstellen."""
from .glossar import eintrag

eintrag("Gleichung", "Zwei Terme, verbunden durch ein Gleichheitszeichen. Gesucht sind die Zahlen, für die beide Seiten "
        "denselben Wert haben.", r"$3x + 5 = 20$ ist eine Gleichung mit der Lösung $x = 5$.", "gleichungen", ["Gleichungen"])
eintrag("Lösungsmenge", r"Die Menge $\mathbb{L}$ aller Zahlen, die eine Gleichung oder Ungleichung erfüllen. "
        r"Sie kann leer sein ($\mathbb{L} = \emptyset$) oder alle Zahlen enthalten ($\mathbb{L} = \mathbb{R}$).",
        r"$3x + 5 = 20$ hat $\mathbb{L} = \{5\}$, $2x + 1 = 2x + 5$ hat $\mathbb{L} = \emptyset$.", "gleichungen", ["L"])
eintrag("Probe", "Eine gefundene Lösung in die Ausgangsgleichung einsetzen und prüfen, ob links und rechts dasselbe herauskommt.",
        r"$x = 5$ in $3x + 5 = 20$: $15 + 5 = 20$. Stimmt.", "gleichungen")
eintrag("Äquivalenzumformung", "Eine Umformung, die die Lösungsmenge nicht ändert: auf beiden Seiten dieselbe Zahl addieren "
        "oder abziehen, mit derselben Zahl ungleich $0$ malnehmen oder durch sie teilen.",
        r"$3x + 5 = 20 \;\; | -5$ ergibt $3x = 15$.", "gleichungen", ["Äquivalenzumformungen"])
eintrag("Bruchgleichung", "Eine Gleichung, bei der die Variable im Nenner steht. Man bestimmt zuerst die Definitionsmenge, "
        "weil kein Nenner $0$ werden darf.", r"$\frac{6}{x} + 1 = 4$ mit $D = \mathbb{R} \setminus \{0\}$ und $\mathbb{L} = \{2\}$.",
        "gleichungen", ["Bruchgleichungen"])
eintrag("Scheinlösung", "Eine Zahl, die beim Rechnen herauskommt, aber nicht in der Definitionsmenge liegt. "
        "Sie ist keine Lösung.", r"$\frac{x}{x - 2} = \frac{2}{x - 2}$ liefert $x = 2$, aber $2 \notin D$. Also $\mathbb{L} = \emptyset$.",
        "gleichungen", ["Scheinlösungen"])
