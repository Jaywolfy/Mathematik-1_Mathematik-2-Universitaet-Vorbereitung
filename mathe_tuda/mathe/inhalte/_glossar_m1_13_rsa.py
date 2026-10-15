# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 13: Kryptographie RSA (Skript Disser, Abschn. 2.9)."""
from .glossar import eintrag

eintrag("Primzahl", "Eine Zahl $p \\in \\mathbb{N}$ mit $p > 1$, die keine Teiler außer $1$ und $p$ hat (Def. 2.65). "
        "Die Zahl $1$ ist keine Primzahl.",
        r"$2, 3, 5, 7, 11, 13$ sind Primzahlen, $15 = 3 \cdot 5$ und $1$ nicht.",
        "rsa", ["Primzahlen", "prim"])
eintrag("Primzahllemma", "Teilt eine Primzahl $p$ ein Produkt $a \\cdot b$, so teilt sie einen der Faktoren: $p \\mid ab \\Rightarrow p \\mid a$ oder $p \\mid b$ (Satz 2.66). "
        "Für zusammengesetzte Zahlen gilt das nicht.",
        r"$5 \mid 3 \cdot 10$ und $5 \mid 10$. Dagegen $6 \mid 3 \cdot 4$, aber $6 \nmid 3$ und $6 \nmid 4$.",
        "rsa", ["Euklids Lemma"])
eintrag("kleiner Satz von Fermat", "Ist $p$ eine Primzahl und $p \\nmid a$, so gilt $a^{p-1} \\bmod p = 1$ (Satz 2.67). "
        "Man kann also Exponenten modulo $p - 1$ reduzieren.",
        r"$3^6 \bmod 7 = 729 \bmod 7 = 1$ und $3^{100} \bmod 101 = 1$.",
        "rsa", ["Fermat", "Satz von Fermat", "kleiner Fermat"])
eintrag("RSA-Verfahren", "Public-Key-Verschlüsselung nach Rivest, Shamir und Adleman (Abschn. 2.9): Mit $n = pq$, $t = (p-1)(q-1)$ und $e \\cdot d \\bmod t = 1$ "
        "ist $(n, e)$ öffentlich, $d$ geheim. Verschlüsseln: $m \\mapsto m^e \\bmod n$, entschlüsseln: $c \\mapsto c^d \\bmod n$.",
        r"$n = 55$, $e = 3$, $d = 27$: $12 \mapsto 23 \mapsto 12$.",
        "rsa", ["RSA", "Rivest-Shamir-Adleman"])
eintrag("öffentlicher Schlüssel", "Bei RSA das Paar $(n, e)$, das jeder kennen darf und mit dem man Nachrichten verschlüsselt. "
        "Der Gegenpart ist der geheime Schlüssel $d$.",
        r"Alice veröffentlicht $(55, 3)$ und behält $d = 27$ für sich.",
        "rsa", ["Public Key", "geheimer Schlüssel", "privater Schlüssel"])
eintrag("euklidischer Algorithmus", "Verfahren zur Berechnung des $\\gcd$ zweier Zahlen durch fortgesetzte Division mit Rest. "
        "Rückwärts eingesetzt (erweitert) liefert er $s, u$ mit $a s + b u = \\gcd(a, b)$ und damit das Inverse zu $e$ modulo $t$.",
        r"$40 = 13 \cdot 3 + 1$, also $1 = 40 - 13 \cdot 3$: $-13 \equiv 27 \pmod{40}$ ist das Inverse von $3$.",
        "rsa", ["Euklid-Algorithmus", "erweiterter euklidischer Algorithmus"])
