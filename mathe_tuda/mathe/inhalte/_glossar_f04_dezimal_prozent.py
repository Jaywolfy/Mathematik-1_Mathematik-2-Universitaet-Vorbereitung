# -*- coding: utf-8 -*-
"""Glossar-Einträge zu Fundament 4: Dezimalzahlen und Prozent."""
from .glossar import eintrag

eintrag("Dezimalzahl", "Eine Zahl mit Komma. Die Stellen nach dem Komma sind Zehntel, Hundertstel, Tausendstel und so weiter.",
        r"$3{,}45 = 3 + \frac{4}{10} + \frac{5}{100}$", "dezimal_prozent",
        ["Dezimalzahlen", "Kommazahl", "Kommazahlen"])
eintrag("Stellenwert", "Der Wert, den eine Ziffer durch ihre Stelle bekommt. Jede Stelle weiter rechts ist zehnmal kleiner.",
        r"In $0{,}07$ steht die $7$ an der Hundertstelstelle: Sie ist $\frac{7}{100}$ wert.", "dezimal_prozent",
        ["Stellenwerte"])
eintrag("periodische Dezimalzahl", "Eine Dezimalzahl, deren Nachkommastellen sich ab einer Stelle immer wiederholen. "
        "Der wiederholte Teil heißt Periode und bekommt einen Strich.",
        r"$\frac{1}{3} = 0{,}\overline{3}$ und $\frac{3}{11} = 0{,}\overline{27}$", "dezimal_prozent",
        ["periodische Dezimalzahlen"])
eintrag("Runden", "Eine Zahl durch eine nahe Zahl mit weniger Stellen ersetzen. Nur die Ziffer direkt hinter der "
        "Rundungsstelle entscheidet: $0$ bis $4$ abrunden, $5$ bis $9$ aufrunden.",
        r"$2{,}346 \approx 2{,}3$ (auf Zehntel) und $2{,}346 \approx 2{,}35$ (auf Hundertstel)", "dezimal_prozent",
        ["gerundet"])
eintrag("Gleitkommazahl", "So speichert ein Computer Kommazahlen: im Zweiersystem mit fester Bitzahl (meist $64$ Bit). "
        "Viele Zahlen wie $0{,}1$ sind dort periodisch und werden deshalb gerundet.",
        r"In Python ergibt `0.1 + 0.2` den Wert `0.30000000000000004`.", "dezimal_prozent",
        ["Gleitkommazahlen", "float"])
eintrag("Prozent", "Hundertstel. $p\\,\\%$ bedeutet $\\frac{p}{100}$.",
        r"$15\,\% = \frac{15}{100} = 0{,}15$", "dezimal_prozent", ["%"])
eintrag("Grundwert", "Das Ganze, von dem bei der Prozentrechnung ausgegangen wird. Es entspricht $100\\,\\%$.",
        r"Bei „$15\,\%$ von $80$“ ist $80$ der Grundwert.", "dezimal_prozent")
eintrag("Prozentwert", "Der Teil des Grundwerts, der zum Prozentsatz gehört: $W = p \\cdot G$.",
        r"$15\,\%$ von $80$ ergibt den Prozentwert $12$.", "dezimal_prozent")
eintrag("Prozentsatz", "Wie viele Hundertstel des Grundwerts gemeint sind. Zum Rechnen als Dezimalzahl: $p = W : G$.",
        r"$12$ von $48$: $p = 12 : 48 = 0{,}25 = 25\,\%$", "dezimal_prozent")
