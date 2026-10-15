# -*- coding: utf-8 -*-
"""Glossar-Einträge zu Vorlesung 2 (Mengen und Quantoren). Vorhandene Begriffe (Menge, Teilmenge, Aussonderung,
Vereinigung, Potenzmenge, Quantor, Mengensystem …) werden nur verlinkt."""
from .glossar import eintrag

eintrag("Erzeugungsweise", "Eine erlaubte Art, aus bekannten Dingen eine neue [[Menge]] zu bilden. Disser verzichtet auf eine formale Definition "
        "von „Menge“ (Russell'sche Antinomie) und gibt stattdessen Erzeugungsweisen an: Aufzählung, Aussonderung, Vereinigung, "
        "Schnitt und Differenz, kartesisches Produkt und Potenzmenge.",
        r"$\{0, 1, 2\}$ (Aufzählung), $\{n \in \mathbb{N} \mid n \le 5\}$ (Aussonderung), $\{0, 1\}^3$ (kartesisches Produkt).",
        "vl02", ["Erzeugungsweisen", "Erzeugungsprinzip"])
eintrag("Aufzählung", "Die einfachste [[Erzeugungsweise]] für Mengen: Die Elemente stehen in geschweiften Klammern, durch Kommas getrennt, "
        "bei unendlichen Mengen mit Pünktchen, wenn das Muster klar ist. Reihenfolge und Wiederholungen spielen keine Rolle.",
        r"$\{0, 1, 2, 3, 4, 5\}$, $\{\ldots, -4, -2, 0, 2, 4, \ldots\}$, $\{0, 1, 1\} = \{1, 0\} = \{0, 1\}$.",
        "vl02", ["Aufzählen", "aufzählende Form"])
eintrag("Mengengleichheit", "Zwei Mengen $M$ und $N$ sind gleich, wenn sie dieselben Elemente haben, also wenn $M \\subseteq N$ und "
        "$N \\subseteq M$ gilt. Beweise zeigen deshalb immer beide Richtungen ([[doppelte Inklusion]]).",
        r"$\{0, 1, 1\} = \{1, 0\}$, denn jedes Element links liegt rechts und umgekehrt.", "vl02", ["Gleichheit von Mengen"])
eintrag("doppelte Inklusion", "Beweismuster für $M = N$: erst $M \\subseteq N$ zeigen (beliebiges $x \\in M$ nehmen, $x \\in N$ herleiten), dann "
        "$N \\subseteq M$. Ein „oder“ in der Voraussetzung wird durch eine [[Fallunterscheidung]] behandelt (Beweis von Satz 1.23).",
        r"Distributivgesetz: $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$ mit den Richtungen $\subseteq$ und $\supseteq$.",
        "vl02", ["Beweis der Mengengleichheit", "Inklusion"])
eintrag("Venn-Diagramm", "Bild von Mengen als überlappende Kreise. Jede Fläche entspricht einer Kombination von Elementen: "
        "Nur die Überlappung ist $M \\cap N$, beide Kreise zusammen sind $M \\cup N$, ein Kreis ohne die Überlappung ist $M \\setminus N$.",
        r"Bild zu Definition 1.21 im Skript Disser (Abbildung 1.1).", "vl02", ["Venn-Diagramme", "Mengendiagramm"])
eintrag("Bitstring", "Ein [[Tupel]] aus Nullen und Einsen. Alle Bitstrings der Länge $n$ bilden die Menge $\\{0, 1\\}^n$ mit $2^n$ Elementen. "
        "Jede Teilmenge einer $n$-elementigen Menge entspricht einem Bitstring (Element dabei: $1$, nicht dabei: $0$).",
        r"$\{0, 1\}^3$ enthält $(0, 0, 0)$, $(0, 0, 1)$, …, $(1, 1, 1)$: acht Bitstrings.", "vl02", ["Bitstrings", "Bitfolge"])
eintrag("Zeuge", "Ein einzelnes Element, das eine Existenzaussage $\\exists x \\in M : E(x)$ beweist: Man gibt ein $x \\in M$ an, für das $E(x)$ gilt. "
        "Das Gegenstück bei $\\forall$-Aussagen ist das [[Gegenbeispiel]].",
        r"$\exists n \in \mathbb{N} : n$ ist gerade. Zeuge: $n = 0$.", "vl02", ["Zeugen", "Existenzzeuge"])
eintrag("gebundene Variable", "Eine Variable, die von einem [[Quantoren|Quantor]] erfasst ist. In $\\forall x \\in M : E(x)$ ist $x$ gebunden: Es ist kein "
        "Platzhalter mehr, der noch belegt werden müsste, und die ganze Formel ist eine [[Aussage]]. Eine nicht gebundene Variable heißt frei.",
        r"In $\exists n \in \mathbb{N} : n$ ist gerade, ist $n$ gebunden. In „$n$ ist gerade“ ist $n$ frei (Aussageform).",
        "vl02", ["gebunden", "freie Variable", "gebundene Variablen"])
