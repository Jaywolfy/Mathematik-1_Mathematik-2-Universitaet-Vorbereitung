# -*- coding: utf-8 -*-
"""Glossar-Einträge von Vorkurs 9: Vollständige Induktion."""
from .glossar import eintrag

eintrag("vollständige Induktion", "Beweisprinzip für Aussagen $A(n)$ über alle natürlichen Zahlen $n \\ge n_0$: "
        "Zeige $A(n_0)$ (Induktionsanfang) und dass aus $A(n)$ stets $A(n+1)$ folgt (Induktionsschritt). "
        "Dann gilt $A(n)$ für alle $n \\ge n_0$, wie bei einer Reihe fallender Dominosteine.",
        r"$\sum_{k=1}^{n} k = \frac{n(n+1)}{2}$ für alle $n \in \mathbb{N}$", "induktion",
        ["Induktion", "Induktionsbeweis", "Prinzip der vollständigen Induktion"])
eintrag("Induktionsanfang", "Erster Teil eines Induktionsbeweises (IA): Man prüft die Aussage für den kleinsten "
        "Wert, meist $n = 1$, durch direktes Nachrechnen. Die Induktionsvoraussetzung darf hier nicht benutzt werden.",
        r"IA für $\sum_{k=1}^{n} k = \frac{n(n+1)}{2}$: $\sum_{k=1}^{1} k = 1 = \frac{1 \cdot 2}{2}$ ✓", "induktion",
        ["IA", "Induktionsbeginn"])
eintrag("Induktionsvoraussetzung", "Die Annahme (IV), dass die Aussage $A(n)$ für ein beliebiges, aber festes $n$ "
        "gilt. Nicht „für alle $n$“, denn das wäre schon die Behauptung.",
        r"IV: Für ein beliebiges, aber festes $n \in \mathbb{N}$ gelte $\sum_{k=1}^{n} k = \frac{n(n+1)}{2}$.",
        "induktion", ["IV", "Induktionsannahme", "Induktionshypothese"])
eintrag("Induktionsschritt", "Teil eines Induktionsbeweises (IS, $n \\to n + 1$): Man zeigt mit Hilfe der IV, dass "
        "die Aussage auch für $n + 1$ gilt. Die Stelle, an der die IV eingeht, wird gekennzeichnet.",
        r"$\sum_{k=1}^{n+1} k = \sum_{k=1}^{n} k + (n+1) \overset{(IV)}{=} \frac{n(n+1)}{2} + (n + 1)$", "induktion",
        ["IS", "Induktionsschritte"])
eintrag("Induktionsschluss", "Letzter Satz eines Induktionsbeweises (ISch): Nach dem Prinzip der vollständigen "
        "Induktion gilt die Aussage für alle $n \\ge n_0$.",
        "Nach dem Prinzip der vollständigen Induktion gilt die Formel für alle $n \\in \\mathbb{N}$.", "induktion",
        ["ISch"])
eintrag("geometrische Summe", "Summe von Potenzen derselben Zahl $q$: $\\sum_{k=0}^{n-1} q^k = \\frac{q^n - 1}{q - 1}$ "
        "für $q \\neq 1$. Für $q = 2$: $1 + 2 + 4 + \\ldots + 2^{n-1} = 2^n - 1$.",
        r"$1 + 2 + 4 + 8 = 15 = 2^4 - 1$", "induktion", ["geometrische Summenformel"])
