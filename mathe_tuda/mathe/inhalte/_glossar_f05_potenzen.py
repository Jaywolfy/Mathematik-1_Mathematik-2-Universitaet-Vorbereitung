# -*- coding: utf-8 -*-
"""Glossar-Einträge zu Fundament 5: Potenzen."""
from .glossar import eintrag

eintrag("Potenz", "Kurzschrift für wiederholtes Malnehmen: $a^n$ ist das Produkt aus $n$ Faktoren $a$.",
        r"$2^5 = 2 \cdot 2 \cdot 2 \cdot 2 \cdot 2 = 32$", "potenzen", ["Potenzen"])
eintrag("Basis einer Potenz", "Die Zahl unten in einer Potenz $a^n$, also $a$. Sie wird malgenommen.",
        r"Bei $3^4$ ist $3$ die Basis.", "potenzen")
eintrag("Exponent", "Die hochgestellte Zahl in einer Potenz $a^n$, also $n$. Er zählt, wie oft die Basis als Faktor dasteht. "
        "Negative Exponenten bilden den Kehrwert.", r"Bei $3^4$ ist $4$ der Exponent; $2^{-3} = \frac{1}{8}$.",
        "potenzen", ["Exponenten", "Hochzahl"])
eintrag("Potenzgesetz", "Rechenregel für Potenzen: $a^m a^n = a^{m+n}$, $\\frac{a^m}{a^n} = a^{m-n}$, $(a^m)^n = a^{mn}$, "
        "$a^n b^n = (ab)^n$. Für Summen gibt es kein solches Gesetz.",
        r"$2^3 \cdot 2^4 = 2^7$, aber $2^3 + 2^4 = 24 \neq 2^7$", "potenzen", ["Potenzgesetze"])
eintrag("Zweierpotenz", "Eine Potenz mit der Basis $2$. Mit $n$ Bits gibt es $2^n$ verschiedene Bitmuster.",
        r"$2^8 = 256$, $2^{10} = 1024$", "potenzen", ["Zweierpotenzen"])
eintrag("Zehnerpotenz", "Eine Potenz mit der Basis $10$. $10^n$ ist eine $1$ mit $n$ Nullen, $10^{-n}$ hat die $1$ an der $n$-ten Nachkommastelle.",
        r"$10^3 = 1000$, $10^{-3} = 0{,}001$", "potenzen", ["Zehnerpotenzen"])
eintrag("wissenschaftliche Schreibweise", "Eine Zahl als Produkt aus einer Zahl, die mindestens $1$ und kleiner als $10$ ist, und einer Zehnerpotenz.",
        r"$3200000 = 3{,}2 \cdot 10^6$ und $0{,}0004 = 4 \cdot 10^{-4}$ (in Python `4e-4`)", "potenzen")
eintrag("Bit", "Die kleinste Informationseinheit: $0$ oder $1$. Acht Bit sind ein Byte.",
        r"Mit $3$ Bit gibt es $2^3 = 8$ Muster: $000$, $001$, …, $111$.", "potenzen", ["Bits"])
