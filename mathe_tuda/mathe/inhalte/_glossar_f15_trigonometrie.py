# -*- coding: utf-8 -*-
"""Glossar-Einträge von Fundament 15: Trigonometrie und Bogenmaß."""
from .glossar import eintrag

eintrag("Hypotenuse", "Die längste Seite eines rechtwinkligen Dreiecks. Sie liegt dem rechten Winkel gegenüber. "
        "Die beiden anderen Seiten heißen Katheten.", r"Im Dreieck mit den Seiten $3$, $4$, $5$ ist $5$ die Hypotenuse.",
        "trigonometrie", ["Kathete", "Katheten", "Gegenkathete", "Ankathete"])
eintrag("Sinus", "Im rechtwinkligen Dreieck: Gegenkathete durch Hypotenuse. Am Einheitskreis: die $y$-Koordinate "
        "des Punkts zum Winkel $\\varphi$.", r"$\sin\left(\frac{\pi}{6}\right) = \frac{1}{2}$", "trigonometrie", ["sin"])
eintrag("Kosinus", "Im rechtwinkligen Dreieck: Ankathete durch Hypotenuse. Am Einheitskreis: die $x$-Koordinate "
        "des Punkts zum Winkel $\\varphi$.", r"$\cos(0) = 1$, $\cos(\pi) = -1$", "trigonometrie", ["cos", "Cosinus"])
eintrag("Tangens", "$\\tan(\\varphi) = \\frac{\\sin(\\varphi)}{\\cos(\\varphi)}$; im Dreieck Gegenkathete durch Ankathete. "
        "Nicht definiert, wo $\\cos(\\varphi) = 0$ ist.", r"$\tan\left(\frac{\pi}{4}\right) = 1$", "trigonometrie", ["tan"])
eintrag("Einheitskreis", "Der Kreis mit Radius $1$ um den Ursprung. Der Punkt zum Winkel $\\varphi$ ist "
        "$(\\cos(\\varphi) \\mid \\sin(\\varphi))$.", r"Zum Winkel $\frac{\pi}{2}$ gehört der Punkt $(0 \mid 1)$.",
        "trigonometrie")
eintrag("Bogenmaß", "Ein Winkel, gemessen als Länge des zugehörigen Bogens auf dem Einheitskreis. "
        "$360^\\circ$ entsprechen $2\\pi$, also $x = \\frac{\\alpha}{180^\\circ} \\cdot \\pi$.",
        r"$90^\circ = \frac{\pi}{2}$, $60^\circ = \frac{\pi}{3}$", "trigonometrie", ["Radiant", "rad"])
eintrag("periodische Funktion", "Eine Funktion, die sich nach einer festen Länge $p > 0$ wiederholt: $f(x + p) = f(x)$ für alle $x$. "
        "Das kleinste solche $p$ heißt Periode der Funktion.", r"$\sin$ und $\cos$ haben die Periode $2\pi$.",
        "trigonometrie", ["periodische Funktionen"])
