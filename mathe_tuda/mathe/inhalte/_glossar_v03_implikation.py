# -*- coding: utf-8 -*-
"""Glossar-Einträge von Vorkurs 3: Implikation, Äquivalenz, Tautologie."""
from .glossar import eintrag

eintrag("Implikation", "Die Wenn-dann-Aussage $A \\Rightarrow B$. Sie ist nur falsch, wenn $A$ wahr und $B$ falsch ist.",
        r"$n \in \mathbb{N} \Rightarrow n \in \mathbb{Z}$ ist wahr.", "implikation", ["Wenn-dann-Aussage", "Folgerung"])
eintrag("Äquivalenz", "Die Genau-dann-wenn-Aussage $A \\Leftrightarrow B$. Sie ist wahr, wenn $A$ und $B$ denselben "
        "Wahrheitswert haben; gleichbedeutend mit $(A \\Rightarrow B) \\land (B \\Rightarrow A)$.",
        r"$x + 1 = 4 \Leftrightarrow x = 3$", "implikation", ["Genau-dann-wenn-Aussage", "äquivalent"])
eintrag("hinreichende Bedingung", "$A$ ist hinreichend für $B$, wenn $A \\Rightarrow B$ gilt: $A$ allein reicht schon für $B$.",
        "„$x = 3$“ ist hinreichend für „$x^2 = 9$“.", "implikation", ["hinreichend"])
eintrag("notwendige Bedingung", "$B$ ist notwendig für $A$, wenn $A \\Rightarrow B$ gilt: Ohne $B$ kann $A$ nicht gelten.",
        "„$n$ gerade“ ist notwendig für „$n$ durch $4$ teilbar“.", "implikation", ["notwendig"])
eintrag("Tautologie", "Eine Aussage, die immer wahr ist, egal welche Werte ihre Teilaussagen haben. Symbol ⊤.",
        r"$A \lor \neg A$", "implikation", ["Tautologien"])
eintrag("Widerspruch", "Eine Aussage, die immer falsch ist, egal welche Werte ihre Teilaussagen haben. Symbol ⊥.",
        r"$A \land \neg A$", "implikation", ["Kontradiktion"])
eintrag("Regeln von De Morgan", "Beim Hineinziehen einer Negation in eine Klammer kippt $\\land$ zu $\\lor$ und umgekehrt: "
        "$\\neg(A \\land B) \\Leftrightarrow \\neg A \\lor \\neg B$, $\\neg(A \\lor B) \\Leftrightarrow \\neg A \\land \\neg B$.",
        "Nicht (Regen und kalt) heißt: kein Regen oder nicht kalt.", "implikation", ["De Morgan", "De-Morgan-Regeln"])
