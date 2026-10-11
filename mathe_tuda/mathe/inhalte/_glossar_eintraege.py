# -*- coding: utf-8 -*-
"""Einträge des Glossars, nach Kapiteln gruppiert (wird von glossar.py geladen)."""
from .glossar import eintrag  # noqa: F401

# ── Fundament 1: Zahlen ──────────────────────────────────────────────────
eintrag("Menge", "Eine Zusammenfassung von Objekten zu einem Ganzen. Die Objekte heißen Elemente. "
        "Man schreibt sie in geschweifte Klammern.", r"$\{1, 2, 3\}$ ist die Menge mit den Elementen $1$, $2$ und $3$.",
        "zahlen", ["Mengen"])
eintrag("Element", "Ein Objekt, das in einer Menge enthalten ist. $a \\in M$ heißt: $a$ ist Element von $M$.",
        r"$2 \in \{1, 2, 3\}$, aber $5 \notin \{1, 2, 3\}$.", "zahlen", ["Elemente"])
eintrag("natürliche Zahl", "Eine der Zählzahlen $1, 2, 3, \\ldots$ Die Menge aller natürlichen Zahlen heißt $\\mathbb{N}$. "
        "Mit der Null dazu schreibt man $\\mathbb{N}_0$.", r"$7 \in \mathbb{N}$, aber $-7 \notin \mathbb{N}$.",
        "zahlen", ["natürliche Zahlen", "N"])
eintrag("ganze Zahl", "Eine natürliche Zahl, die Null oder eine natürliche Zahl mit Minus davor. Die Menge heißt $\\mathbb{Z}$.",
        r"$-3$, $0$ und $12$ sind ganze Zahlen, $\frac{1}{2}$ nicht.", "zahlen", ["ganze Zahlen", "Z"])
eintrag("rationale Zahl", "Eine Zahl, die man als Bruch $\\frac{p}{q}$ mit einer ganzen Zahl $p$ und einer natürlichen Zahl $q$ "
        "schreiben kann. Die Menge heißt $\\mathbb{Q}$.", r"$\frac{3}{4}$, $-2 = \frac{-2}{1}$ und $0{,}25 = \frac{1}{4}$.",
        "zahlen", ["rationale Zahlen", "Q"])
eintrag("irrationale Zahl", "Eine reelle Zahl, die man **nicht** als Bruch schreiben kann. Ihre Nachkommastellen hören nie auf "
        "und wiederholen sich nie.", r"$\sqrt{2} = 1{,}41421\ldots$ und $\pi = 3{,}14159\ldots$", "zahlen",
        ["irrational", "irrationale Zahlen"])
eintrag("reelle Zahl", "Jeder Punkt auf der Zahlengeraden. Rationale und irrationale Zahlen zusammen. Die Menge heißt $\\mathbb{R}$.",
        r"$-2$, $\frac{1}{3}$, $\sqrt{2}$ und $\pi$ sind reelle Zahlen.", "zahlen", ["reelle Zahlen", "R"])
eintrag("Zahlenstrahl", "Eine Linie, die bei $0$ beginnt und auf der jede Zahl einen festen Platz hat. Nach rechts werden die Zahlen größer.",
        r"$3$ liegt links von $7$, also ist $3 < 7$.", "zahlen")
eintrag("Zahlengerade", "Der nach links verlängerte Zahlenstrahl. Links von der $0$ liegen die negativen Zahlen. Weiter rechts heißt größer.",
        r"$-2$ liegt links von $1$, also ist $-2 < 1$.", "zahlen")
eintrag("Teilmenge", r"$A$ ist Teilmenge von $B$ ($A \subset B$ oder $A \subseteq B$), wenn jedes Element von $A$ auch in $B$ liegt.",
        r"$\{1, 2\} \subset \{1, 2, 3\}$ und $\mathbb{N} \subset \mathbb{Z}$.", "zahlen", ["Teilmengen"])
eintrag("Vorzeichen", "Das Plus oder Minus vor einer Zahl. Es sagt, auf welcher Seite der Null die Zahl liegt. Die $0$ hat kein Vorzeichen.",
        r"$-5$ hat das Vorzeichen Minus, $5$ (also $+5$) das Vorzeichen Plus.", "zahlen")
eintrag("Gegenzahl", "Die Zahl mit gleichem Abstand zur Null, aber auf der anderen Seite. Die Gegenzahl von $0$ ist $0$.",
        r"Die Gegenzahl von $4$ ist $-4$, die von $-\frac{1}{2}$ ist $\frac{1}{2}$.", "zahlen")

# ── Fundament 2: Rechnen ─────────────────────────────────────────────────
eintrag("Term", "Ein sinnvoller Rechenausdruck aus Zahlen, Variablen, Rechenzeichen und Klammern, ohne Gleichheitszeichen.",
        r"$2 + 3 \cdot 4$ und $2x - 1$ sind Terme. $2x - 1 = 5$ ist kein Term, sondern eine Gleichung.", "rechnen", ["Terme"])
eintrag("Punkt vor Strich", "Mal und geteilt (Punktrechnung) werden vor plus und minus (Strichrechnung) ausgerechnet. "
        "Klammern kommen noch davor.", r"$2 + 3 \cdot 4 = 2 + 12 = 14$", "rechnen")

# ── Fundament 3: Brüche ──────────────────────────────────────────────────
eintrag("Bruch", "Eine Zahl der Form $\\frac{a}{b}$: $a$ Teile von einem Ganzen, das in $b$ gleiche Teile geteilt ist. "
        "Der Bruchstrich bedeutet „geteilt durch“.", r"$\frac{3}{4} = 3 : 4 = 0{,}75$", "brueche", ["Brüche"])
eintrag("Zähler", "Die Zahl über dem Bruchstrich. Sie zählt, wie viele Teile man nimmt.", r"Bei $\frac{3}{4}$ ist $3$ der Zähler.", "brueche")
eintrag("Nenner", "Die Zahl unter dem Bruchstrich. Sie nennt, in wie viele gleiche Teile das Ganze geteilt ist. Sie darf nie $0$ sein.",
        r"Bei $\frac{3}{4}$ ist $4$ der Nenner.", "brueche")
eintrag("Erweitern", "Zähler und Nenner mit derselben Zahl (nicht $0$) malnehmen. Der Wert des Bruchs bleibt gleich.",
        r"$\frac{2}{3} = \frac{2 \cdot 4}{3 \cdot 4} = \frac{8}{12}$", "brueche")
eintrag("Kürzen", "Zähler und Nenner durch denselben gemeinsamen Teiler (nicht $0$) teilen. Der Wert bleibt gleich. Vollständig gekürzt ist ein Bruch, "
        "wenn Zähler und Nenner keinen gemeinsamen Teiler außer $1$ haben.", r"$\frac{12}{18} = \frac{2}{3}$", "brueche")
eintrag("gleichnamig", "Brüche mit demselben Nenner heißen gleichnamig. Nur gleichnamige Brüche kann man direkt addieren.",
        r"$\frac{1}{5}$ und $\frac{3}{5}$ sind gleichnamig.", "brueche")
eintrag("Hauptnenner", "Der kleinste gemeinsame Nenner zweier Brüche, also das kgV der Nenner.",
        r"Für $\frac{1}{4}$ und $\frac{1}{6}$ ist der Hauptnenner $12$.", "brueche")
eintrag("Kehrwert", "Der Bruch mit vertauschtem Zähler und Nenner. Eine Zahl mal ihr Kehrwert ergibt $1$. Die $0$ hat keinen Kehrwert.",
        r"Der Kehrwert von $\frac{2}{3}$ ist $\frac{3}{2}$, der von $5$ ist $\frac{1}{5}$.", "brueche")
eintrag("ggT", "Größter gemeinsamer Teiler: die größte Zahl, die zwei Zahlen ohne Rest teilt. Damit kürzt man vollständig.",
        r"$\mathrm{ggT}(12, 18) = 6$", "brueche", ["größter gemeinsamer Teiler"])
eintrag("kgV", "Kleinstes gemeinsames Vielfaches: die kleinste positive Zahl, die durch beide Zahlen teilbar ist.",
        r"$\mathrm{kgV}(4, 6) = 12$", "brueche", ["kleinstes gemeinsames Vielfaches"])
