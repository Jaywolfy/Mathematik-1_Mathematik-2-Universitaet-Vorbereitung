# -*- coding: utf-8 -*-
"""Glossar-Einträge von Fundament 13: Funktionen und Graphen."""
from .glossar import eintrag

eintrag("Funktion", "Eine Zuordnung, die jedem Element $x$ der Definitionsmenge $D$ **genau ein** Element $f(x)$ "
        "der Zielmenge $W$ zuordnet. Schreibweise: $f\\colon D \\to W,\\ x \\mapsto f(x)$. In Mathe 1 sagt man auch Abbildung.",
        r"$f\colon \mathbb{R} \to \mathbb{R},\ x \mapsto 2x + 1$ ordnet der $3$ den Wert $7$ zu.",
        "funktionen", ["Funktionen"])
eintrag("Zielmenge", "Die Menge $W$ in $f\\colon D \\to W$, in der die Funktionswerte liegen dürfen. "
        "Sie muss nicht ganz getroffen werden: Die Menge der tatsächlich angenommenen Werte (Wertemenge, Bild) kann kleiner sein.",
        r"$f\colon \mathbb{R} \to \mathbb{R},\ x \mapsto x^2$ hat die Zielmenge $\mathbb{R}$, nimmt aber nur Werte $\ge 0$ an.",
        "funktionen")
eintrag("Funktionswert", "Die Zahl $f(x)$, die eine Funktion einer Stelle $x$ zuordnet.",
        r"Für $f(x) = x^2$ ist der Funktionswert an der Stelle $3$ gleich $f(3) = 9$.", "funktionen",
        ["Funktionswerte"])
eintrag("Wertetabelle", "Eine Tabelle mit ausgewählten Stellen $x$ und den zugehörigen Funktionswerten $f(x)$.",
        r"Für $f(x) = 2x + 1$: $x = 0, 1, 2$ ergibt $f(x) = 1, 3, 5$.", "funktionen")
eintrag("Graph", "Die Menge aller Punkte $(x \\mid f(x))$ einer Funktion, gezeichnet im Koordinatensystem.",
        r"Der Graph von $f(x) = 2x + 1$ ist eine Gerade durch $(0 \mid 1)$ und $(1 \mid 3)$.", "funktionen",
        ["Graphen", "Funktionsgraph"])
eintrag("Definitionsmenge", "Die Menge $D$ aller Zahlen, die man in eine Funktion einsetzen darf. "
        "Verboten sind zum Beispiel Stellen, an denen ein Nenner $0$ wird. In der Schule sucht man die größtmögliche "
        "Definitionsmenge; an der Uni gehört $D$ zur Angabe der Funktion dazu.",
        r"$f(x) = \frac{1}{x - 2}$ hat $D = \mathbb{R} \setminus \{2\}$.", "funktionen",
        ["Definitionsbereich"])
eintrag("lineare Funktion", "Eine Funktion der Form $f(x) = mx + b$. Ihr Graph ist eine Gerade mit Steigung $m$ "
        "und $y$-Achsenabschnitt $b$.", r"$f(x) = 2x + 4$: Steigung $2$, schneidet die $y$-Achse bei $4$.",
        "funktionen", ["lineare Funktionen"])
eintrag("Steigung", "Bei einer Geraden: wie viel es nach oben geht, wenn man $1$ nach rechts geht. "
        "Aus zwei Punkten: $m = \\frac{y_2 - y_1}{x_2 - x_1}$.",
        r"Durch $(1 \mid 3)$ und $(4 \mid 9)$: $m = \frac{6}{3} = 2$.", "funktionen")
eintrag("y-Achsenabschnitt", "Der Wert $b$ in $f(x) = mx + b$. Dort schneidet die Gerade die $y$-Achse, im Punkt $(0 \\mid b)$.",
        r"$f(x) = 3x - 2$ schneidet die $y$-Achse bei $(0 \mid -2)$.", "funktionen")
eintrag("Parabel", "Der Graph einer quadratischen Funktion $f(x) = ax^2 + bx + c$ mit $a \\ne 0$. "
        "Bogenform mit einem höchsten oder tiefsten Punkt, dem Scheitelpunkt.",
        r"Der Graph von $f(x) = (x - 1)^2 - 4$ ist eine nach oben offene Parabel.", "funktionen", ["Parabeln"])
eintrag("Normalparabel", "Der Graph von $f(x) = x^2$. Symmetrisch zur $y$-Achse, Scheitelpunkt $S(0 \\mid 0)$.",
        r"Die Punkte $(-2 \mid 4)$, $(0 \mid 0)$ und $(2 \mid 4)$ liegen auf der Normalparabel.", "funktionen")
eintrag("Scheitelpunkt", "Der höchste oder tiefste Punkt einer Parabel. Bei $f(x) = a(x - d)^2 + e$ ist es $S(d \\mid e)$.",
        r"$f(x) = (x - 2)^2 + 1$ hat den Scheitelpunkt $S(2 \mid 1)$.", "funktionen", ["Scheitel"])
eintrag("Scheitelpunktform", "Die Schreibweise $f(x) = a(x - d)^2 + e$ einer quadratischen Funktion. "
        "Man liest den Scheitelpunkt $S(d \\mid e)$ direkt ab.",
        r"$f(x) = 2(x + 1)^2 - 3$ hat $d = -1$, $e = -3$, also $S(-1 \mid -3)$.", "funktionen")
