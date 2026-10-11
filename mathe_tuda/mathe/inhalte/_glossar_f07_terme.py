# -*- coding: utf-8 -*-
"""Glossar-Einträge zu Fundament 7: Terme und binomische Formeln."""
from .glossar import eintrag

eintrag("Variable", "Ein Buchstabe wie $x$, der als Platzhalter für eine Zahl steht. Setzt man eine Zahl ein, "
        "bekommt der Term einen Wert.", r"In $2x + 1$ ist $x$ die Variable. Für $x = 3$ ergibt sich $7$.",
        "terme", ["Variablen", "Platzhalter"])
eintrag("gleichartige Terme", "Terme mit denselben Variablen in denselben Potenzen. Nur sie darf man zusammenfassen, "
        "indem man die Zahlen davor addiert.", r"$3x$ und $4x$ sind gleichartig: $3x + 4x = 7x$. $x^2$ und $x$ sind es nicht.",
        "terme", ["gleichartig", "gleichartiger Term"])
eintrag("Ausmultiplizieren", "Eine Klammer auflösen: Der Faktor vor der Klammer wird mit jedem Summanden in der Klammer "
        "malgenommen.", r"$3(2x + 1) = 6x + 3$", "terme")
eintrag("Distributivgesetz", "Die Regel $a(b + c) = ab + ac$. Sie erlaubt Ausmultiplizieren und, rückwärts gelesen, Ausklammern.",
        r"$-2(x - 4) = -2x + 8$", "terme", ["Verteilungsgesetz"])
eintrag("binomische Formeln", r"Drei Abkürzungen fürs Ausmultiplizieren: $(a + b)^2 = a^2 + 2ab + b^2$, "
        r"$(a - b)^2 = a^2 - 2ab + b^2$ und $(a + b)(a - b) = a^2 - b^2$.",
        r"$(x + 3)^2 = x^2 + 6x + 9$, aber **nicht** $x^2 + 9$.", "terme",
        ["binomische Formel", "erste binomische Formel", "zweite binomische Formel", "dritte binomische Formel"])
eintrag("Ausklammern", "Einen Faktor, der in jedem Summanden steckt, vor eine Klammer ziehen. Das Gegenteil von "
        "Ausmultiplizieren. Eine Summe wird so zum Produkt (faktorisieren).", r"$6x + 9 = 3(2x + 3)$", "terme",
        ["Faktorisieren"])
eintrag("Bruchterm", "Ein Bruch, in dessen Nenner (oft auch im Zähler) eine Variable steht. Kürzen darf man nur gemeinsame "
        "Faktoren, nie Summanden.", r"$\frac{x^2 - 9}{x + 3} = x - 3$ für $x \neq -3$", "terme", ["Bruchterme"])
