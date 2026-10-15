# -*- coding: utf-8 -*-
"""Glossar-Einträge von Vorkurs 8: Kontraposition und Widerspruch."""
from .glossar import eintrag

eintrag("Kontraposition", "Die Aussage $\\neg B \\Rightarrow \\neg A$ zu einer Implikation $A \\Rightarrow B$. "
        "Beide sind gleichwertig. Beim Beweis durch Kontraposition zeigt man $\\neg B \\Rightarrow \\neg A$ "
        "statt $A \\Rightarrow B$.",
        "Kontraposition von „$n^2$ gerade $\\Rightarrow$ $n$ gerade“ ist „$n$ ungerade $\\Rightarrow$ $n^2$ ungerade“.",
        "kontraposition", ["Kontrapositionsaussage", "Beweis durch Kontraposition"])
eintrag("Widerspruchsbeweis", "Beweis von $A \\Rightarrow B$, bei dem man $A$ und $\\neg B$ annimmt und daraus "
        "einen Widerspruch ($\\bot$) herleitet. Dann war die Annahme falsch, also gilt $B$.",
        r"Annahme $\sqrt{2} = \frac{p}{q}$ vollständig gekürzt führt darauf, dass $p$ und $q$ gerade sind: Widerspruch.",
        "kontraposition", ["indirekter Beweis", "Beweis durch Widerspruch", "Widerspruchsbeweise"])
eintrag("Widerspruchsannahme", "Die Annahme am Anfang eines Widerspruchsbeweises: Die Voraussetzung gilt, "
        "die Behauptung aber nicht ($A \\land \\neg B$).",
        "Für „$2 \\mid n \\Rightarrow 2 \\mid n^3$“: Angenommen, $2 \\mid n$, aber $2 \\nmid n^3$.",
        "kontraposition", ["Annahme zum Widerspruch"])
