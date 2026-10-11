# -*- coding: utf-8 -*-
"""Fundament 12: Betrag – Abstand zur Null, Fallunterscheidung, Betragsgleichungen und
-ungleichungen, Dreiecksungleichung."""
from fractions import Fraction as F

from .. import mathlib, pruefer
from ..engine import neues_kapitel, ohne_gleiche

tex = mathlib.tex
tk = mathlib.tex_klammer
vz = mathlib.vorzeichen_tex


def _menge(werte):
    return "{" + "; ".join(mathlib.text(w) for w in werte) + "}"


def _ohne_gleiche_menge(loesung, fehler):
    """Wie engine.ohne_gleiche, aber für Lösungsmengen (ohne_gleiche kann nur Zahlen)."""
    soll = pruefer.bereich_parsen(loesung)
    erg, gesehen = [], []
    for w, m in fehler:
        v = pruefer.bereich_parsen(w)
        if pruefer.bereiche_gleich(v, soll) or any(pruefer.bereiche_gleich(v, g) for g in gesehen):
            continue
        gesehen.append(v)
        erg.append((w, m))
    return erg


def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


def _linear_tex(m, n):
    """m·x + n als LaTeX."""
    return mathlib.Polynom({1: F(m), 0: F(n)}).tex()


k = neues_kapitel(
    slug="betrag",
    titel="Betrag",
    beschreibung="Betrag als Abstand, Fallunterscheidung, Betragsgleichungen und -ungleichungen, Dreiecksungleichung",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="📏")

k.lernziele([
    "Ich verstehe den Betrag als Abstand zur Null und berechne Beträge",
    "Ich löse einen Betrag mit einer Fallunterscheidung auf",
    "Ich löse Betragsgleichungen wie $|x - 3| = 5$",
    "Ich löse Betragsungleichungen und schreibe die Lösungsmenge als Intervall",
    "Ich kenne die Dreiecksungleichung $|a + b| \\le |a| + |b|$",
])

k.warum(r"""
In Python heißt der Betrag `abs()`. Du brauchst ihn ständig: Kommazahlen im Computer
vergleicht man nie mit `==`, sondern prüft `abs(x - y) < 1e-9`, also ob ihr Abstand
winzig ist. Genau diese Idee „Abstand kleiner als $\varepsilon$“ ist im Vorkurs und in
Mathe 1 die Definition von Konvergenz: $|a_n - a| < \varepsilon$. Navigationssysteme
und Spiele messen Wege im Straßenraster mit Beträgen (Manhattan-Abstand), und die
[[Dreiecksungleichung]] steckt in fast jedem Beweis der Analysis.
""")

# ── 1: Betrag als Abstand ─────────────────────────────────────────────────
k.erklaerung("Betrag als Abstand", r"""
    ## Wie weit ist es bis zur Null?

    :::analogie 🛗 Der Aufzug
    Vom Erdgeschoss fährst du in den 3. Stock oder in das 3. Untergeschoss. In beiden
    Fällen fährst du $3$ Stockwerke weit. Die Richtung ist egal.
    :::

    Der [[Betrag]] $|x|$ ist der Abstand von $x$ zur $0$ auf der Zahlengeraden. Ein
    Abstand ist nie negativ. Also ist $|x| \ge 0$ für jede Zahl $x$.

    :::visual zahlenstrahl
    {"von": -5, "bis": 5, "punkte": [{"x": -3, "farbe": "orange"}, {"x": 3, "farbe": "orange"}, {"x": 0}],
     "pfeile": [{"von": 0, "bis": -3, "label": "3"}, {"von": 0, "bis": 3, "label": "3"}],
     "unterschrift": "$-3$ und $3$ sind beide $3$ Schritte von der $0$ entfernt: $|-3| = |3| = 3$."}
    :::

    :::rechnung Beispiele
    |-3| = 3 || $3$ Schritte bis zur $0$
    |3| = 3 || ebenfalls $3$ Schritte
    |0| = 0 || die $0$ ist von sich selbst $0$ entfernt
    |2 - 7| = |-5| = 5 || erst innen rechnen, dann den Betrag
    :::

    :::achtung Den Betrag in Teilen nehmen
    $|2 - 7| = |2| - |7| = -5$ ist falsch. Rechne **erst** innen aus, dann nimm den
    Betrag. Ein Betrag ist nie negativ.
    :::

    :::alt Mit dem Minus-Radiergummi erklärt
    Bei einer einzelnen Zahl macht der Betrag etwas Einfaches: Er radiert ein Minus vor
    der Zahl weg und lässt alles andere stehen. $|-7| = 7$, $|7| = 7$,
    $|-\frac{1}{2}| = \frac{1}{2}$. Steht innen eine Rechnung, rechnest du sie zuerst
    aus, damit nur noch eine Zahl dasteht.
    :::
    ---
    ## Abstand zweier Zahlen

    !! $|a - b|$ ist der Abstand von $a$ und $b$ auf der Zahlengeraden.

    Die Reihenfolge ist egal: $|a - b| = |b - a|$.

    :::visual zahlenstrahl
    {"von": -3, "bis": 6, "punkte": [{"x": -2}, {"x": 5}],
     "pfeile": [{"von": -2, "bis": 5, "label": "7"}],
     "unterschrift": "Von $-2$ bis $5$ sind es $7$ Schritte: $|5 - (-2)| = 7$."}
    :::

    :::rechnung Abstand von $5$ und $-2$
    |5 - (-2)| = |5 + 2| = 7 || große minus kleine Zahl
    |-2 - 5| = |-7| = 7 || andersherum: gleicher Abstand
    :::

    :::alt Mit dem Thermometer erklärt
    Morgens zeigt das Thermometer $-2$ Grad, mittags $5$ Grad. Um wie viel ist es
    wärmer geworden? Von $-2$ bis $0$ sind es $2$ Grad, von $0$ bis $5$ noch $5$,
    zusammen $7$ Grad. Den Temperaturunterschied gibst du immer positiv an, egal ob
    es wärmer oder kälter wurde. Genau das liefert $|5 - (-2)|$.
    :::
    """)

k.zahl("Berechne $|-7| - |3|$.", 4,
       "$|-7| = 7$ und $|3| = 3$, also $7 - 3 = 4$.",
       tipps=["Berechne jeden Betrag einzeln.", "$|-7| = 7$", "$7 - 3$"],
       rechenweg=r"""
       :::rechnung
       |-7| - |3| = 7 - 3 || Beträge ausrechnen
       = 4 || subtrahieren
       :::
       """,
       typische_fehler=[(-10, "$|-7|$ ist $7$, nicht $-7$. Der Betrag ist ein Abstand und nie negativ."),
                        (10, "Das Minus **zwischen** den Beträgen bleibt stehen: $7 - 3$, nicht $7 + 3$.")])

k.zahl("Berechne $|2 - 9|$.", 7,
       "Erst innen rechnen: $2 - 9 = -7$. Dann den Betrag: $|-7| = 7$.",
       tipps=["Rechne erst aus, was im Betrag steht.", "$2 - 9 = -7$", "Der Abstand von $-7$ zur $0$ ist …"],
       rechenweg=r"""
       :::rechnung
       |2 - 9| = |-7| || erst innen rechnen
       = 7 || Abstand zur $0$
       :::
       """,
       typische_fehler=[(-7, "Ein Betrag ist nie negativ. $|-7| = 7$."),
                        (11, "Du hast $|2| + |9|$ gerechnet. Rechne zuerst innen: $2 - 9 = -7$.")])

k.zahl("Wie groß ist der Abstand der Zahlen $-4$ und $3$ auf der Zahlengeraden?", 7,
       "Abstand $= |3 - (-4)| = |3 + 4| = 7$. Von $-4$ bis $0$ sind es $4$, von $0$ bis $3$ noch $3$.",
       tipps=["Abstand von $a$ und $b$ ist $|a - b|$.", "$|3 - (-4)|$", "Minus minus wird plus: $|3 + 4|$."],
       rechenweg=r"""
       :::rechnung
       |3 - (-4)| = |3 + 4| || Abstand als Betrag der Differenz
       = 7 || ausrechnen
       :::
       """,
       typische_fehler=[(1, "Du hast $|3 + (-4)|$ gerechnet. Der Abstand ist der Betrag der **Differenz**: $|3 - (-4)|$."),
                        (-7, "Ein Abstand ist nie negativ.")])

# ── 2: Fallunterscheidung ─────────────────────────────────────────────────
k.erklaerung("Den Betrag auflösen", r"""
    ## Zwei Fälle

    Für Rechnungen mit Variablen braucht man eine Formel. Sie hat zwei Fälle, man
    nennt das [[Fallunterscheidung]]:

    $$|x| = \begin{cases} x, & \text{falls } x \ge 0 \\ -x, & \text{falls } x < 0 \end{cases}$$

    Im zweiten Fall ist $x$ negativ. Dann ist $-x$ **positiv**: Das Minus macht aus
    der negativen Zahl eine positive.

    :::rechnung Beide Fälle
    |5| = 5 || $5 \ge 0$: erster Fall, bleibt wie es ist
    |-4| = -(-4) = 4 || $-4 < 0$: zweiter Fall, Minus davor
    :::

    :::achtung $-x$ ist nicht automatisch negativ
    $-x$ heißt „Gegenzahl von $x$“. Für $x = -4$ ist $-x = 4$ positiv. Darum ist
    $|x| = -x$ für negative $x$ richtig.
    :::

    :::alt Als Programm erklärt
    So würdest du den Betrag programmieren: `if x >= 0: return x`, sonst
    `return -x`. Die zwei Zeilen sind genau die zwei Fälle. Für `x = -4` landet das
    Programm im zweiten Fall und gibt `-(-4)`, also `4` zurück.
    :::
    ---
    ## Betrag eines Terms

    Bei $|x - 3|$ fragst du: Wann ist das Innere $x - 3$ positiv oder $0$? Genau für
    $x \ge 3$. Dort bleibt alles, wie es ist. Für $x < 3$ kommt ein Minus vor die
    ganze Klammer:

    $$|x - 3| = \begin{cases} x - 3, & \text{falls } x \ge 3 \\ -(x - 3) = 3 - x, & \text{falls } x < 3 \end{cases}$$

    :::visual funktionsgraph
    {"funktionen": [{"term": "abs(x - 3)", "label": "f(x)"}, {"term": "x - 3", "label": "g(x)", "farbe": 2}],
     "x": [-2, 7], "y": [-4, 5],
     "unterschrift": "Wo $x - 3$ unter der Achse liegt, klappt der Betrag den Graphen nach oben."}
    :::

    :::rechnung Zwei Stellen einsetzen
    |5 - 3| = 5 - 3 = 2 || $x = 5 \ge 3$: erster Fall
    |1 - 3| = 3 - 1 = 2 || $x = 1 < 3$: zweiter Fall, $3 - x$
    :::

    :::alt Mit einem Spiegel erklärt
    Zeichne die Gerade $y = x - 3$. Links von $x = 3$ liegt sie unter der $x$-Achse.
    Leg einen Spiegel auf die $x$-Achse und klapp diesen Teil nach oben. Was du
    siehst, ist der Graph von $|x - 3|$: ein V mit der Spitze bei $3$. Der
    hochgeklappte Teil ist die Gerade $y = 3 - x$.
    :::
    """)

k.mc("Für $x < 2$ gilt: $|x - 2| = \\ldots$",
     ["$2 - x$", "$x - 2$", "$-x - 2$", "$x + 2$"],
     "Für $x < 2$ ist $x - 2$ negativ. Dann kommt ein Minus vor die ganze Klammer: $-(x - 2) = 2 - x$.",
     tipps=["Ist $x - 2$ für $x < 2$ positiv oder negativ?", "Negativ. Also gilt der Fall $|y| = -y$.",
            "$-(x - 2)$ ausrechnen."],
     fehler={"$x - 2$": "Für $x < 2$ ist $x - 2$ negativ. Ein Betrag ist aber nie negativ: Es kommt ein Minus davor.",
             "$-x - 2$": "Das Minus gilt für die **ganze** Klammer: $-(x - 2) = -x + 2$. Beide Vorzeichen drehen sich um."})

k.wf("Für alle reellen Zahlen $a$ und $b$ gilt $|a - b| = |a| - |b|$.", False,
     "Falsch. Gegenbeispiel $a = 1$, $b = 3$: $|1 - 3| = 2$, aber $|1| - |3| = -2$. "
     "Den Betrag darf man nicht auf die Teile einer Differenz verteilen. (Bei Produkten geht es: $|a \\cdot b| = |a| \\cdot |b|$.)",
     tipps=["Probiere $a = 1$ und $b = 3$."])

# ── 3: Betragsgleichungen ─────────────────────────────────────────────────
k.erklaerung("Betragsgleichungen", r"""
    ## Abstand gegeben, Zahl gesucht

    $|x - 3| = 5$ heißt: $x$ hat von $3$ den Abstand $5$. Von $3$ aus kannst du $5$
    Schritte nach rechts oder nach links gehen. Also gibt es zwei Lösungen.

    :::visual zahlenstrahl
    {"von": -3, "bis": 9, "punkte": [{"x": 3}, {"x": -2, "farbe": "orange"}, {"x": 8, "farbe": "orange"}],
     "pfeile": [{"von": 3, "bis": 8, "label": "5"}, {"von": 3, "bis": -2, "label": "5"}],
     "unterschrift": "Abstand $5$ von der $3$: bei $8$ und bei $-2$."}
    :::

    :::rechnung $|x - 3| = 5$ lösen
    |x - 3| = 5 || Aufgabe
    x - 3 = 5 \text{ oder } x - 3 = -5 || das Innere ist $5$ oder $-5$
    x_1 = 8 || $5 + 3$
    x_2 = -2 || $-5 + 3$
    :::

    :::alt Mit der Fallunterscheidung erklärt
    Ohne Bild geht es auch. Fall $x \ge 3$: Dann ist $|x - 3| = x - 3$, also
    $x - 3 = 5$ und $x = 8$. Das erfüllt $x \ge 3$. Fall $x < 3$: Dann ist
    $|x - 3| = 3 - x$, also $3 - x = 5$ und $x = -2$. Das erfüllt $x < 3$. Beide
    Fälle zusammen ergeben $\mathbb{L} = \{-2; 8\}$.
    :::
    ---
    ## Mit Faktor und Sonderfälle

    Steht vor $x$ eine Zahl, löst du nach dem Aufspalten zwei normale Gleichungen.

    :::rechnung $|2x - 4| = 6$ lösen
    |2x - 4| = 6 || Aufgabe
    2x - 4 = 6 \text{ oder } 2x - 4 = -6 || das Innere ist $6$ oder $-6$
    2x = 10 \text{ oder } 2x = -2 || $+4$
    x_1 = 5 || $10 : 2$
    x_2 = -1 || $-2 : 2$
    :::

    Zwei Sonderfälle: $|x + 1| = 0$ hat nur die Lösung $-1$. Und $|2x - 1| = -3$ hat
    **keine** Lösung, denn ein Betrag ist nie negativ.

    :::achtung Den zweiten Fall falsch aufgeschrieben
    Aus $|2x - 4| = 6$ folgt $2x - 4 = -6$, also $x = -1$. Falsch ist, einfach die
    erste Lösung $5$ mit Minus zu versehen: $-5$ ist keine Lösung, denn
    $|-10 - 4| = 14$. Mach immer die Probe.
    :::

    :::alt Graphisch erklärt
    Zeichne das V von $y = |2x - 4|$ mit der Spitze bei $x = 2$ und die waagerechte
    Gerade $y = 6$. Sie schneidet das V zweimal: bei $x = -1$ und bei $x = 5$. Die
    Gerade $y = 0$ berührt nur die Spitze, also eine Lösung. Die Gerade $y = -3$
    liegt unter dem V und trifft es nie: keine Lösung.
    :::
    """)

k.loesungsmenge("Löse $|x - 3| = 5$. Gib die Lösungsmenge an.", "{-2; 8}",
                "Abstand $5$ von der $3$: $3 + 5 = 8$ und $3 - 5 = -2$.",
                tipps=["$|x - 3|$ ist der Abstand von $x$ zur $3$.", "Das Innere ist $5$ oder $-5$.",
                       "$x - 3 = 5$ oder $x - 3 = -5$."],
                rechenweg=r"""
                :::rechnung
                |x - 3| = 5 || Aufgabe
                x - 3 = 5 \text{ oder } x - 3 = -5 || zwei Fälle
                x_1 = 8 || $+3$
                x_2 = -2 || $+3$
                :::
                """,
                typische_fehler=[("{8}", "Es fehlt der zweite Fall: Auch $x - 3 = -5$ hat Abstand $5$, also $x = -2$."),
                                 ("{-8; 2}", "Vorzeichen: $|x - 3|$ ist der Abstand zur $+3$, nicht zur $-3$.")])

k.loesungsmenge("Löse $|2x + 1| = 7$. Gib die Lösungsmenge an.", "{-4; 3}",
                "$2x + 1 = 7$ ergibt $x = 3$, $2x + 1 = -7$ ergibt $x = -4$.",
                tipps=["Spalte auf: Das Innere ist $7$ oder $-7$.", "$2x + 1 = 7$ oder $2x + 1 = -7$.",
                       "Im zweiten Fall: $2x = -8$."],
                rechenweg=r"""
                :::rechnung
                |2x + 1| = 7 || Aufgabe
                2x + 1 = 7 \text{ oder } 2x + 1 = -7 || zwei Fälle
                2x = 6 \text{ oder } 2x = -8 || $-1$
                x_1 = 3 || durch $2$
                x_2 = -4 || durch $2$
                :::
                """,
                typische_fehler=[("{-3; 3}", "Den zweiten Fall musst du ganz durchrechnen: $2x + 1 = -7$, also $2x = -8$ "
                                             "und $x = -4$. Probe mit $-3$: $|-6 + 1| = 5$."),
                                 ("{3}", "Es fehlt der Fall $2x + 1 = -7$.")])

k.loesungsmenge("Löse $|x + 4| = -2$. Gib die Lösungsmenge an (leere Menge: {}).", "{}",
                "Ein Betrag ist nie negativ. Er kann nie $-2$ sein. Die Lösungsmenge ist leer.",
                tipps=["Kann ein Abstand negativ sein?", "$|x + 4| \\ge 0$ für jedes $x$.",
                       "Keine Zahl erfüllt die Gleichung."],
                rechenweg=r"""
                :::rechnung
                |x + 4| \ge 0 > -2 || Betrag ist nie negativ, aber rechts steht $-2$
                :::

                Also $\mathbb{L} = \{\}$.
                """,
                typische_fehler=[("{-6; -2}", "Probe mit $-6$: $|-6 + 4| = 2$, nicht $-2$. Ein Betrag ist nie negativ, "
                                              "die Gleichung hat keine Lösung.")])

# ── 4: Betragsungleichungen ───────────────────────────────────────────────
k.erklaerung("Betragsungleichungen", r"""
    ## Näher dran als $r$

    :::analogie 🐕 Der Hund an der Leine
    Ein Hund ist mit einer $3$ Meter langen Leine an einem Pfahl bei der $1$
    angebunden. Er kommt überall hin, wo der Abstand zum Pfahl höchstens $3$ ist.
    :::

    $|x - 1| < 3$ heißt: $x$ ist von der $1$ weniger als $3$ entfernt. Das sind alle
    Zahlen zwischen $1 - 3 = -2$ und $1 + 3 = 4$, ohne die Ränder.

    :::visual zahlenstrahl
    {"von": -4, "bis": 6, "punkte": [{"x": 1}],
     "intervalle": [{"von": -2, "bis": 4, "von_zu": false, "bis_zu": false, "label": "Abstand kleiner als 3"}],
     "unterschrift": "$|x - 1| < 3$: alle Zahlen im offenen Intervall $(-2, 4)$."}
    :::

    :::rechnung $|x - 1| < 3$ lösen
    |x - 1| < 3 || Abstand von $1$ kleiner als $3$
    -3 < x - 1 < 3 || das Innere liegt zwischen $-3$ und $3$
    -2 < x < 4 || überall $+1$
    :::

    Also $\mathbb{L} = (-2, 4)$, ein offenes [[Intervall]]. Mit $\le$ gehören die Ränder dazu: $[-2, 4]$.

    :::alt Mit Probezahlen erklärt
    Probier ein paar Zahlen aus. $x = 0$: $|0 - 1| = 1 < 3$, passt. $x = 4$:
    $|4 - 1| = 3$, das ist nicht kleiner als $3$, passt nicht. $x = 5$: $|5 - 1| = 4$,
    passt nicht. $x = -2$: $|-3| = 3$, passt nicht. $x = -1$: $|-2| = 2$, passt.
    Die passenden Zahlen liegen genau zwischen $-2$ und $4$.
    :::
    ---
    ## Weiter weg als $r$

    $|x - 1| \ge 3$ ist das Gegenteil: Abstand mindestens $3$. Dann liegt $x$ links
    von $-2$ oder rechts von $4$, die Ränder eingeschlossen. Die Lösungsmenge besteht
    aus zwei Teilen.

    :::visual zahlenstrahl
    {"von": -6, "bis": 8, "punkte": [{"x": 1}],
     "intervalle": [{"von": "-inf", "bis": -2, "von_zu": false, "bis_zu": true},
                    {"von": 4, "bis": "inf", "von_zu": true, "bis_zu": false}],
     "unterschrift": "$|x - 1| \\ge 3$: zwei Strahlen nach außen."}
    :::

    :::rechnung $|x - 1| \ge 3$ lösen
    |x - 1| \ge 3 || Abstand von $1$ mindestens $3$
    x - 1 \le -3 \text{ oder } x - 1 \ge 3 || das Innere ist ganz links oder ganz rechts
    x \le -2 \text{ oder } x \ge 4 || überall $+1$
    :::

    Also $\mathbb{L} = (-\infty, -2] \cup [4, \infty)$.

    :::achtung Innen und außen verwechselt
    „Kleiner als“ ergibt **ein** Intervall in der Mitte. „Größer als“ ergibt **zwei**
    Teile nach außen. $-3 \le x - 1 \le 3$ wäre hier genau falsch herum.
    :::

    :::alt Mit Funkreichweite erklärt
    Ein Sender steht bei der $1$ und reicht $3$ Kilometer weit. $|x - 1| < 3$ fragt:
    Wo hast du Empfang? Ein Stück in der Mitte. $|x - 1| \ge 3$ fragt: Wo hast du
    keinen Empfang (oder gerade noch am Rand)? Überall außerhalb, links und rechts.
    Das sind zwei getrennte Gebiete.
    :::
    """)

k.loesungsmenge("Löse $|x - 1| < 3$. Gib die Lösungsmenge als Intervall an.", "(-2; 4)",
                "Abstand von $1$ kleiner als $3$: zwischen $-2$ und $4$, ohne Ränder.",
                tipps=["$|x - 1|$ ist der Abstand zur $1$.", "$-3 < x - 1 < 3$.", "Überall $+1$: $-2 < x < 4$."],
                rechenweg=r"""
                :::rechnung
                |x - 1| < 3 || Aufgabe
                -3 < x - 1 < 3 || Innere zwischen $-3$ und $3$
                -2 < x < 4 || $+1$
                :::

                $\mathbb{L} = (-2, 4)$
                """,
                typische_fehler=[("[-2; 4]", "Die Ränder gehören nicht dazu: Bei $x = 4$ ist der Abstand genau $3$, "
                                             "und $3 < 3$ ist falsch. Nimm runde Klammern."),
                                 ("(-4; 2)", "Die Mitte ist $+1$, denn $|x - 1|$ misst den Abstand zur $1$, nicht zur $-1$."),
                                 ("(-inf; 4)", "Es gibt auch eine linke Grenze: Bei $x = -5$ ist der Abstand $6$, zu groß.")])

k.loesungsmenge("Löse $|x + 2| \\ge 1$. Gib die Lösungsmenge an.", "(-inf; -3] ∪ [-1; inf)",
                "$|x + 2| = |x - (-2)|$ ist der Abstand zur $-2$. Mindestens $1$ entfernt: $x \\le -3$ oder $x \\ge -1$.",
                tipps=["$|x + 2|$ ist der Abstand zur $-2$.", "„Mindestens“ heißt: zwei Teile nach außen.",
                       "$x + 2 \\le -1$ oder $x + 2 \\ge 1$."],
                rechenweg=r"""
                :::rechnung
                |x + 2| \ge 1 || Abstand zur $-2$ mindestens $1$
                x + 2 \le -1 \text{ oder } x + 2 \ge 1 || ganz links oder ganz rechts
                x \le -3 \text{ oder } x \ge -1 || $-2$
                :::

                $\mathbb{L} = (-\infty, -3] \cup [-1, \infty)$
                """,
                typische_fehler=[("[-3; -1]", "Das ist die Lösung von $|x + 2| \\le 1$. „Größer gleich“ ergibt zwei Teile nach außen."),
                                 ("(-inf; -3) ∪ (-1; inf)", "Bei $\\ge$ gehören die Ränder dazu: eckige Klammern."),
                                 ("(-inf; 1] ∪ [3; inf)", "$|x + 2|$ ist der Abstand zur $-2$, nicht zur $+2$.")])

# ── 5: Dreiecksungleichung ────────────────────────────────────────────────
k.erklaerung("Die Dreiecksungleichung", r"""
    ## Ein Umweg ist nie kürzer

    !! Für alle reellen Zahlen $a, b$ gilt $|a + b| \le |a| + |b|$.

    Das ist die [[Dreiecksungleichung]]. Gleichheit gilt genau dann, wenn $a$ und $b$
    nicht verschiedene Vorzeichen haben. Für Produkte gilt dagegen immer
    $|a \cdot b| = |a| \cdot |b|$.

    :::rechnung Drei Beispiele
    |3 + 4| = 7 \le 7 = |3| + |4| || gleiche Vorzeichen: Gleichheit
    |3 + (-5)| = 2 \le 8 = |3| + |-5| || verschiedene Vorzeichen: echt kleiner
    |3 \cdot (-5)| = 15 = |3| \cdot |-5| || beim Produkt immer gleich
    :::

    :::alt Mit einem Spaziergang erklärt
    Du gehst $3$ Schritte nach rechts und dann $5$ nach links. Am Ende stehst du
    $|3 + (-5)| = 2$ Schritte vom Start entfernt. Gelaufen bist du aber $3 + 5 = 8$
    Schritte. Der Abstand zum Start ist nie größer als der gelaufene Weg. Gleich groß
    ist er nur, wenn du nie umdrehst.
    :::
    """)

k.mc("Wann gilt $|a + b| = |a| + |b|$?",
     ["wenn $a \\cdot b \\ge 0$ ist, also keine verschiedenen Vorzeichen", "immer", "nie", "nur wenn $a = b$"],
     "Bei gleichen Vorzeichen (oder wenn eine Zahl $0$ ist) addieren sich die Abstände einfach. "
     "Bei verschiedenen Vorzeichen heben sie sich teilweise auf: $|3 + (-5)| = 2 < 8$.",
     tipps=["Probiere $a = 3$, $b = 4$ und dann $a = 3$, $b = -5$.",
            "Bei $3$ und $-5$ heben sich die Zahlen teilweise auf."],
     fehler={"immer": "Gegenbeispiel: $|3 + (-5)| = 2$, aber $|3| + |-5| = 8$.",
             "nur wenn $a = b$": "Auch $a = 3$, $b = 4$ liefert Gleichheit: $|7| = 3 + 4$."})


# ── Praxis ────────────────────────────────────────────────────────────────
def betrag_berechnen(rng):
    art = rng.choice(["differenz", "differenz", "zwei_betraege", "abstand"])
    while True:
        a, b = rng.randint(-12, 12), rng.randint(-12, 12)
        if a != b and a != 0 and b != 0:
            break
    if art == "differenz":
        w = abs(a - b)
        frage = f"Berechne $|{a} - {tk(b)}|$."
        weg = _zeilen((f"|{a} - {tk(b)}| = |{a - b}|", "erst innen rechnen"), (f"= {w}", "Abstand zur $0$"))
        fehler = [(a - b, "Ein Betrag ist nie negativ."),
                  (abs(a) - abs(b), "Der Betrag lässt sich nicht auf die Teile einer Differenz verteilen. Erst innen rechnen."),
                  (abs(a) + abs(b), "Rechne zuerst innen aus. $|a - b|$ ist nicht $|a| + |b|$.")]
        erkl = "Erst das Innere ausrechnen, dann den Betrag nehmen."
        tipps = ["Rechne zuerst aus, was im Betrag steht.", f"${a} - {tk(b)} = {a - b}$",
                 "Der Betrag ist der Abstand zur $0$."]
    elif art == "zwei_betraege":
        w = abs(a) - abs(b)
        frage = f"Berechne $|{a}| - |{b}|$."
        weg = _zeilen((f"|{a}| - |{b}| = {abs(a)} - {abs(b)}", "jeden Betrag einzeln"), (f"= {w}", "subtrahieren"))
        fehler = [(abs(a - b), "Das ist $|a - b|$. Hier wird jeder Betrag einzeln genommen."),
                  (a - b, "Die Beträge fehlen: $|" + str(a) + "| = " + str(abs(a)) + "$."),
                  (abs(a) + abs(b), "Das Minus zwischen den Beträgen bleibt stehen.")]
        erkl = "Jeden Betrag einzeln ausrechnen. Das Ergebnis darf hier negativ sein: Das Minus steht außerhalb der Beträge."
        tipps = ["Berechne jeden Betrag einzeln.", f"$|{a}| = {abs(a)}$ und $|{b}| = {abs(b)}$.",
                 f"${abs(a)} - {abs(b)}$"]
    else:
        w = abs(a - b)
        frage = f"Wie groß ist der Abstand der Zahlen ${a}$ und ${b}$ auf der Zahlengeraden?"
        weg = _zeilen((f"|{a} - {tk(b)}| = |{a - b}|", "Abstand als Betrag der Differenz"), (f"= {w}", "ausrechnen"))
        fehler = [(abs(a + b), "Der Abstand ist der Betrag der **Differenz**, nicht der Summe."),
                  (-w, "Ein Abstand ist nie negativ.")]
        erkl = "Der Abstand von $a$ und $b$ ist $|a - b|$."
        tipps = ["Abstand von $a$ und $b$ ist $|a - b|$.", f"$|{a} - {tk(b)}|$", f"${a} - {tk(b)} = {a - b}$"]
    return {"frage": frage, "loesung": w, "tipps": tipps, "rechenweg": weg, "erklaerung": erkl,
            "typische_fehler": ohne_gleiche(w, fehler)}


k.praxis()

k.generator(betrag_berechnen, typ="zahl", titel="Beträge berechnen", glatt=True)


def betragsgleichung(rng):
    m = rng.choice([1, 1, 1, 2, 3])
    n = rng.choice([x for x in range(-9, 10) if x])
    c = rng.choices([rng.randint(1, 9), 0, -rng.randint(1, 5)], [8, 1, 1])[0]
    innen = _linear_tex(m, n)
    frage = f"Löse $|{innen}| = {c}$. Gib die Lösungsmenge an (leere Menge: {{}})."
    if c < 0:
        loesung = "{}"
        falsch = sorted({F(-c - n, m), F(c - n, m)})
        fehler = [(_menge(falsch), f"Ein Betrag ist nie negativ. $|{innen}| = {c}$ hat keine Lösung.")]
        weg = (f"Ein Betrag ist immer $\\ge 0$, rechts steht aber ${c}$. Keine Zahl erfüllt die Gleichung.\n\n"
               "Also $\\mathbb{L} = \\{\\}$.")
        tipps = ["Kann ein Betrag negativ sein?", f"$|{innen}| \\ge 0$, aber rechts steht ${c}$.",
                 "Die Lösungsmenge ist leer."]
    elif c == 0:
        x0 = F(-n, m)
        loesung = _menge([x0])
        zeilen = [(f"|{innen}| = 0", "Aufgabe"), (f"{innen} = 0", "nur die $0$ hat Betrag $0$")]
        if m != 1:
            zeilen.append((f"{m}x = {-n}", f"${vz(-n)}$ auf beiden Seiten"))
        zeilen.append((f"x = {tex(x0)}", "nach $x$ auflösen"))
        weg = _zeilen(*zeilen)
        fehler = [(_menge([-x0]), "Vorzeichen: Rechne $" + innen + " = 0$ sauber nach $x$ um.")]
        tipps = ["Welche Zahl hat den Betrag $0$?", f"Nur die $0$. Also ${innen} = 0$.", "Nach $x$ auflösen."]
    else:
        x1, x2 = F(c - n, m), F(-c - n, m)
        loesung = _menge(sorted([x1, x2]))
        zeilen = [(f"|{innen}| = {c}", "Aufgabe"),
                  (f"{innen} = {c} \\text{{ oder }} {innen} = {-c}", "das Innere ist $" + str(c) + "$ oder $" + str(-c) + "$")]
        if m != 1:
            zeilen.append((f"{m}x = {c - n} \\text{{ oder }} {m}x = {-c - n}", f"${vz(-n)}$ auf beiden Seiten"))
        zeilen.append((f"x_1 = {tex(x1)}", "erster Fall" + (f": ${c - n} : {m}$" if m != 1 else f": ${c} {vz(-n)}$")))
        zeilen.append((f"x_2 = {tex(x2)}", "zweiter Fall" + (f": ${-c - n} : {m}$" if m != 1 else f": ${-c} {vz(-n)}$")))
        weg = _zeilen(*zeilen)
        fehler = [(_menge([x1]), "Es fehlt der zweite Fall: Auch das Innere $= " + str(-c) + "$ hat den Betrag $" + str(c) + "$."),
                  (_menge(sorted({x1, -x1})), "Den zweiten Fall musst du ganz durchrechnen: $" + innen + " = " + str(-c)
                   + "$. Einfach die erste Lösung mit Minus versehen geht nicht. Mach die Probe."),
                  (_menge(sorted({F(c + n, m), F(-c + n, m)})), "Beim Umstellen ist das Vorzeichen von $" + str(n)
                   + "$ gekippt. Bring die Zahl mit der Gegenrechnung auf die andere Seite.")]
        tipps = ["Spalte auf: Das Innere ist $" + str(c) + "$ oder $" + str(-c) + "$.",
                 f"${innen} = {c}$ oder ${innen} = {-c}$.", "Löse beide Gleichungen nach $x$ auf."]
    return {"frage": frage, "loesung": loesung, "tipps": tipps, "rechenweg": weg,
            "erklaerung": "$|T| = c$ mit $c > 0$ heißt $T = c$ oder $T = -c$. Für $c = 0$ nur $T = 0$, für $c < 0$ keine Lösung.",
            "typische_fehler": _ohne_gleiche_menge(loesung, fehler)}


k.generator(betragsgleichung, typ="loesungsmenge", titel="Betragsgleichungen")


def _iv(lo, lo_zu, hi, hi_zu):
    def g(v):
        return "-inf" if v == "-inf" else "inf" if v == "inf" else str(v)
    return ("[" if lo_zu else "(") + g(lo) + "; " + g(hi) + ("]" if hi_zu else ")")


def betragsungleichung(rng):
    mitte = rng.choice([x for x in range(-6, 7)])
    r = rng.randint(1, 6)
    rel = rng.choice(["<", "<=", ">", ">="])
    rel_tex = {"<": "<", "<=": "\\le", ">": ">", ">=": "\\ge"}[rel]
    zu = rel in ("<=", ">=")
    innen = "x" if mitte == 0 else f"x {vz(-mitte)}"
    lo, hi = mitte - r, mitte + r
    if rel in ("<", "<="):
        loesung = _iv(lo, zu, hi, zu)
        verkehrt = _iv("-inf", False, lo, not zu) + " ∪ " + _iv(hi, not zu, "inf", False)
        zeilen = [(f"|{innen}| {rel_tex} {r}", f"Abstand von ${mitte}$ " + ("höchstens" if zu else "kleiner als") + f" ${r}$"),
                  (f"{-r} {rel_tex} {innen} {rel_tex} {r}", f"das Innere liegt zwischen ${-r}$ und ${r}$")]
        if mitte != 0:
            zeilen.append((f"{lo} {rel_tex} x {rel_tex} {hi}", f"überall ${vz(mitte)}$"))
        ergebnis_tex = ("[" if zu else "(") + f"{lo}, {hi}" + ("]" if zu else ")")
        falsch_mitte = _iv(-mitte - r, zu, -mitte + r, zu)
        rand = _iv(lo, not zu, hi, not zu)
        erkl = "Abstand kleiner als $r$: ein Intervall um die Mitte."
    else:
        loesung = _iv("-inf", False, lo, zu) + " ∪ " + _iv(hi, zu, "inf", False)
        verkehrt = _iv(lo, not zu, hi, not zu)
        zeilen = [(f"|{innen}| {rel_tex} {r}", f"Abstand von ${mitte}$ " + ("mindestens" if zu else "größer als") + f" ${r}$")]
        klein = "<" if rel == ">" else "\\le"
        zeilen.append((f"{innen} {klein} {-r} \\text{{ oder }} {innen} {rel_tex} {r}", "ganz links oder ganz rechts"))
        if mitte != 0:
            zeilen.append((f"x {klein} {lo} \\text{{ oder }} x {rel_tex} {hi}", f"überall ${vz(mitte)}$"))
        ergebnis_tex = f"(-\\infty, {lo}" + ("]" if zu else ")") + " \\cup " + ("[" if zu else "(") + f"{hi}, \\infty)"
        falsch_mitte = _iv("-inf", False, -mitte - r, zu) + " ∪ " + _iv(-mitte + r, zu, "inf", False)
        rand = _iv("-inf", False, lo, not zu) + " ∪ " + _iv(hi, not zu, "inf", False)
        erkl = "Abstand größer als $r$: zwei Teile nach außen."
    fehler = [(verkehrt, "Innen und außen verwechselt. „Kleiner“ ergibt ein Intervall in der Mitte, "
                         "„größer“ zwei Teile nach außen."),
              (rand, "Die Grenzen stimmen, aber nicht, ob sie dazugehören. Bei $<$ und $>$ gehören die Ränder nicht dazu, "
                     "bei $\\le$ und $\\ge$ schon.")]
    if mitte != 0:
        fehler.append((falsch_mitte, f"Die Mitte ist ${mitte}$: $|{innen}|$ misst den Abstand zur ${mitte}$, nicht zur ${-mitte}$."))
    return {
        "frage": f"Löse $|{innen}| {rel_tex} {r}$. Gib die Lösungsmenge an.",
        "loesung": loesung,
        "tipps": [f"$|{innen}|$ ist der Abstand von $x$ zur ${mitte}$.",
                  "Kleiner: ein Intervall in der Mitte. Größer: zwei Teile nach außen.",
                  f"Die Grenzen sind ${mitte} - {r} = {lo}$ und ${mitte} + {r} = {hi}$."],
        "rechenweg": _zeilen(*zeilen) + f"\n\n$\\mathbb{{L}} = {ergebnis_tex}$",
        "erklaerung": erkl,
        "typische_fehler": _ohne_gleiche_menge(loesung, fehler),
    }


k.generator(betragsungleichung, typ="loesungsmenge", titel="Betragsungleichungen")

k.zahl(r"""
    ## Informatik: Abstand im Straßenraster

    In einer Stadt mit rechtwinkligen Straßen (wie Manhattan) kann man nicht schräg
    laufen. Der Weg zwischen den Kreuzungen $(x_1, y_1)$ und $(x_2, y_2)$ ist
    $$|x_1 - x_2| + |y_1 - y_2|.$$
    Diesen **Manhattan-Abstand** nutzen Wegfinder in Spielen und Algorithmen auf Rastern.
    Berechne ihn für $(1, 5)$ und $(4, 1)$.
    """, abs(1 - 4) + abs(5 - 1),
       "$|1 - 4| + |5 - 1| = 3 + 4 = 7$: drei Blöcke waagerecht, vier senkrecht.",
       tipps=["Rechne die beiden Beträge einzeln.", "$|1 - 4| = 3$", "$|5 - 1| = 4$"],
       rechenweg=r"""
       :::rechnung
       |1 - 4| + |5 - 1| = |-3| + |4| || einsetzen, innen rechnen
       = 3 + 4 || Beträge
       = 7 || addieren
       :::
       """,
       typische_fehler=[(1, "Ohne Beträge heben sich die Wege auf: $-3 + 4 = 1$. Jeder Block zählt aber positiv."),
                        (5, "Das ist der Luftlinien-Abstand $\\sqrt{3^2 + 4^2}$. Im Straßenraster läuft man nicht schräg.")])

# Übungsblatt: Ungleichung mit zwei Beträgen, Fallunterscheidung
k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: Fallunterscheidung mit zwei Beträgen

    Bestimmen Sie die Menge aller $x \in \mathbb{R}$ mit
    $$|x - 2| \le |x + 4|.$$
    Unterscheiden Sie dazu die Fälle $x \ge 2$, $\ -4 \le x < 2$ und $x < -4$.
    """,
    [{"typ": "loesungsmenge", "frage": "Fall $x \\ge 2$: Beide Beträge fallen weg, $x - 2 \\le x + 4$. "
                                       "Welche $x \\ge 2$ erfüllen das?",
      "loesung": "[2; inf)",
      "tipps": ["$x$ auf beiden Seiten abziehen: $-2 \\le 4$.", "Das ist immer wahr. Also alle $x$ dieses Falls."],
      "rechenweg": "$x - 2 \\le x + 4 \\iff -2 \\le 4$: immer wahr. Lösung im Fall: $[2, \\infty)$.",
      "typische_fehler": [("{}", "$-2 \\le 4$ ist **wahr**. Also erfüllen alle $x \\ge 2$ die Ungleichung.")]},
     {"typ": "loesungsmenge", "frage": "Fall $-4 \\le x < 2$: Jetzt ist $|x - 2| = 2 - x$ und $|x + 4| = x + 4$. "
                                       "Welche $x$ aus diesem Bereich erfüllen $2 - x \\le x + 4$?",
      "loesung": "[-1; 2)",
      "tipps": ["$2 - x \\le x + 4$ nach $x$ auflösen.", "$-2 \\le 2x$, also $x \\ge -1$. Dann mit $-4 \\le x < 2$ schneiden."],
      "rechenweg": "$2 - x \\le x + 4 \\iff -2 \\le 2x \\iff x \\ge -1$. Mit $-4 \\le x < 2$: $[-1, 2)$.",
      "typische_fehler": [("[-1; inf)", "Das Ergebnis gilt nur im Fallbereich $-4 \\le x < 2$. Schneide damit."),
                          ("[-1; 2]", "Die $2$ gehört nicht zu diesem Fall (sie ist im Fall $x \\ge 2$).")]},
     {"typ": "loesungsmenge", "frage": "Fall $x < -4$: $|x - 2| = 2 - x$ und $|x + 4| = -x - 4$. "
                                       "Welche $x < -4$ erfüllen $2 - x \\le -x - 4$? (leere Menge: {})",
      "loesung": "{}",
      "tipps": ["$x$ auf beiden Seiten addieren.", "Es bleibt $2 \\le -4$. Ist das wahr?"],
      "rechenweg": "$2 - x \\le -x - 4 \\iff 2 \\le -4$: falsch. Keine Lösung in diesem Fall.",
      "typische_fehler": [("(-inf; -4)", "$2 \\le -4$ ist **falsch**. Also erfüllt kein $x$ dieses Falls die Ungleichung.")]},
     {"typ": "loesungsmenge", "frage": "Gib die gesamte Lösungsmenge an.", "loesung": "[-1; inf)",
      "tipps": ["Vereinige die drei Teillösungen.", "$[-1, 2) \\cup [2, \\infty)$"],
      "rechenweg": "$\\mathbb{L} = \\{\\} \\cup [-1, 2) \\cup [2, \\infty) = [-1, \\infty)$",
      "typische_fehler": [("[2; inf)", "Auch der mittlere Fall liefert Lösungen: $[-1, 2)$.")]}],
    "Bei mehreren Beträgen teilt man die Zahlengerade an den Stellen, an denen ein Inneres $0$ wird. "
    "In jedem Bereich fallen die Beträge weg. Zum Schluss werden die Teillösungen vereinigt. "
    "Anschaulich: Die Zahlen, die näher an $2$ als an $-4$ liegen oder gleich weit weg, beginnen bei der Mitte $-1$.",
    uebungsblatt=True,
    tipps=["Die Inneren werden bei $x = 2$ und $x = -4$ null. Dort wechseln die Fälle.",
           "In jedem Fall die Beträge durch $T$ oder $-T$ ersetzen und normal lösen."],
    rechenweg=r"""
    :::rechnung Fall $x \ge 2$
    x - 2 \le x + 4 || beide Inneren $\ge 0$
    -2 \le 4 || $-x$: immer wahr, also $[2, \infty)$
    :::

    :::rechnung Fall $-4 \le x < 2$
    2 - x \le x + 4 || $|x - 2| = 2 - x$
    -2 \le 2x || $+x$ und $-4$ auf beiden Seiten
    x \ge -1 || durch $2$
    :::

    Mit $-4 \le x < 2$ ergibt das $[-1, 2)$.

    Fall $x < -4$: $2 - x \le -x - 4$ wird zu $2 \le -4$, das ist falsch. Keine Lösung.

    $$\mathbb{L} = [-1, 2) \cup [2, \infty) = [-1, \infty)$$
    """)

k.papier(r"""
    ## Beweisen wie in der Übung: umgekehrte Dreiecksungleichung

    Zeigen Sie mit der Dreiecksungleichung: Für alle $a, b \in \mathbb{R}$ gilt
    $$\big|\, |a| - |b| \,\big| \le |a - b|.$$
    """,
    r"""
    **Benutzt:** Dreiecksungleichung $|u + v| \le |u| + |v|$, und $|y| \le c$ gilt genau
    dann, wenn $-c \le y \le c$.

    **Schritt 1:** Schreibe $a = (a - b) + b$. Mit der Dreiecksungleichung:
    $$|a| = |(a - b) + b| \le |a - b| + |b|, \quad \text{also} \quad |a| - |b| \le |a - b|.$$

    **Schritt 2:** Genauso mit vertauschten Rollen, $b = (b - a) + a$:
    $$|b| \le |b - a| + |a|, \quad \text{also} \quad |b| - |a| \le |b - a| = |a - b|.$$
    Mal $(-1)$: $|a| - |b| \ge -|a - b|$.

    **Schritt 3:** Zusammen gilt $-|a - b| \le |a| - |b| \le |a - b|$. Das heißt genau
    $\big|\, |a| - |b| \,\big| \le |a - b|$. $\square$
    """,
    ["Ich habe $a$ als $(a - b) + b$ geschrieben und die Dreiecksungleichung angewendet",
     "Ich habe die Rollen von $a$ und $b$ vertauscht und $|b - a| = |a - b|$ benutzt",
     "Ich habe beide Abschätzungen zu $-|a - b| \\le |a| - |b| \\le |a - b|$ zusammengesetzt",
     "Ich habe begründet, warum daraus die Aussage mit dem äußeren Betrag folgt"],
    "Der Trick „geschickt Null addieren“ ($a = a - b + b$) kommt in Analysis-Beweisen ständig vor.",
    tipps=["Schreibe $a = (a - b) + b$ und wende die Dreiecksungleichung an."])

k.zusammenfassung(r"""
    ## Betrag

    $$|x| = \begin{cases} x, & x \ge 0 \\ -x, & x < 0 \end{cases}$$

    | Aufgabe | Bedeutung | Lösung |
    |---|---|---|
    | $|x - 3| = 5$ | Abstand zu $3$ ist $5$ | $\{-2; 8\}$ |
    | $|x - 1| < 3$ | näher als $3$ an $1$ | $(-2, 4)$ |
    | $|x - 1| \ge 3$ | mindestens $3$ von $1$ weg | $(-\infty, -2] \cup [4, \infty)$ |
    | $|T| = c < 0$ | Betrag negativ | keine Lösung |

    !! $|a - b|$ ist der Abstand von $a$ und $b$. Ein Betrag ist nie negativ.

    - Erst innen rechnen, dann den Betrag: $|2 - 7| = |-5| = 5$.
    - $|a \cdot b| = |a| \cdot |b|$, aber $|a - b| \neq |a| - |b|$ im Allgemeinen.
    - Dreiecksungleichung: $|a + b| \le |a| + |b|$.
    - Bei mehreren Beträgen: Fälle an den Stellen, wo ein Inneres $0$ wird.
""")
