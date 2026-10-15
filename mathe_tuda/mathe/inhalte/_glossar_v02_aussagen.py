# -*- coding: utf-8 -*-
"""Glossar-Einträge von Vorkurs 2: Aussagen und Wahrheitstafeln."""
from .glossar import eintrag

eintrag("Aussage", "Ein Ausdruck, dem man eindeutig einen Wahrheitswert (wahr oder falsch) zuordnen kann. "
        "Befehle, Fragen und Terme sind keine Aussagen.",
        "„$7$ ist eine Primzahl“ (wahr), „$3 > 5$“ (falsch).", "aussagen", ["Aussagen"])
eintrag("Wahrheitswert", "Wahr (w, $1$) oder falsch (f, $0$). Jede Aussage hat genau einen davon.",
        "„$2 + 5 = 7$“ hat den Wahrheitswert w.", "aussagen", ["Wahrheitswerte"])
eintrag("Aussageform", "Ein Ausdruck mit Variablen, der nach dem Einsetzen von Werten aus einer Grundmenge "
        "eine Aussage wird.", r"$2x = 6$ mit $x \in \mathbb{R}$: für $x = 3$ wahr, für $x = 1$ falsch.",
        "aussagen", ["Aussageformen"])
eintrag("Negation", "Die Verneinung $\\neg A$ einer Aussage $A$. Sie hat immer den umgekehrten Wahrheitswert.",
        r"$\neg(x > 3)$ ist $x \le 3$.", "aussagen", ["Verneinung", "negieren"])
eintrag("Konjunktion", "Die Verknüpfung „und“, $A \\land B$. Sie ist nur wahr, wenn $A$ und $B$ beide wahr sind.",
        "„$4$ ist gerade und $4 > 3$“ ist wahr.", "aussagen")
eintrag("Disjunktion", "Die Verknüpfung „oder“, $A \\lor B$. Sie ist wahr, wenn mindestens eine der Aussagen wahr ist "
        "(auch wenn beide wahr sind).", "„$2$ ist gerade oder $2$ ist prim“ ist wahr.", "aussagen")
eintrag("Wahrheitstafel", "Eine Tabelle, die für jede Kombination der Wahrheitswerte der Grundaussagen den Wert "
        "einer Formel angibt. Bei $n$ Grundaussagen hat sie $2^n$ Zeilen.",
        r"Für $A \land B$: w, f, f, f in den Zeilen (w,w), (w,f), (f,w), (f,f).", "aussagen",
        ["Wahrheitstafeln", "Wahrheitstabelle"])
