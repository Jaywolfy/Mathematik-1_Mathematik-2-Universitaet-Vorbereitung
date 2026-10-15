# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 2: Logisches Schließen und Beweisformen (Disser 1.3)."""
from .glossar import eintrag

eintrag("Theorem", "Ein besonders wichtiger [[Satz]]. Ein Hilfssatz heißt Lemma, eine unmittelbare Folgerung Korollar.",
        r"Der Fundamentalsatz der Algebra wird oft „Theorem“ genannt.", "beweisformen", ["Theoreme"])
eintrag("definierendes Gleichheitszeichen", "Das Zeichen $:=$ (gelesen „ist definiert als“) gibt einem neuen Symbol "
        "eine Bedeutung. Das gewöhnliche $=$ vergleicht dagegen zwei schon bekannte Ausdrücke.",
        r"$c := a + b$ führt $c$ ein; danach ist $c = a + b$ eine wahre Aussage.", "beweisformen",
        ["Definitionszeichen", "ist definiert als"])
eintrag("Schlussregel", "Eine Regel, nach der aus wahren Aussagen eine weitere wahre Aussage folgt, zum Beispiel "
        "Modus ponens, Modus tollens oder Elimination. Jede Schlussregel entspricht einer Tautologie.",
        r"Aus $P \land Q$ folgt $P$ („Und zerlegen“).", "beweisformen", ["Schlussregeln", "logischer Schluss"])
eintrag("Modus ponens", "Schlussregel: Gelten $P$ und $P \\Rightarrow Q$, dann gilt auch $Q$ (eine Implikation vorwärts nutzen).",
        r"„Wer den Schlüssel hat, war im Raum. Anna hat ihn. Also war Anna im Raum.“", "beweisformen")
eintrag("Modus tollens", "Schlussregel: Gelten $P \\Rightarrow Q$ und $\\neg Q$, dann gilt auch $\\neg P$ "
        "(eine Implikation über das Kontrapositionsgesetz rückwärts nutzen).",
        r"„Regnet es, ist die Straße nass. Sie ist trocken. Also regnet es nicht.“", "beweisformen")
eintrag("Elimination (Schlussregel)", "Schlussregel: Gelten $P \\lor Q$ und $\\neg P$, dann gilt $Q$ (einen Fall ausschließen).",
        r"„Es war Anna oder Ben. Anna war es nicht. Also Ben.“", "beweisformen", ["Elimination"])
