# -*- coding: utf-8 -*-
"""Fundament 10: Quadratische Gleichungen – Normalform, Nullprodukt, quadratische Ergänzung,
pq-Formel, Mitternachtsformel, Diskriminante, Satz von Vieta."""
from fractions import Fraction as F

from .. import mathlib, pruefer
from ..engine import neues_kapitel, ohne_gleiche

tex = mathlib.tex
tk = mathlib.tex_klammer
vz = mathlib.vorzeichen_tex


def _poly(a, b, c):
    return mathlib.Polynom({2: F(a), 1: F(b), 0: F(c)})


def _menge(werte):
    return "{" + "; ".join(mathlib.text(w) for w in werte) + "}"


def _ohne_gleiche_menge(loesung, fehler):
    """Wie engine.ohne_gleiche, aber für Lösungsmengen (ohne_gleiche kann nur Zahlen)."""
    soll = pruefer.bereich_parsen(loesung)
    erg, gesehen = [], []
    for w, m in fehler:
        try:
            v = pruefer.bereich_parsen(w)
        except (pruefer.TermFehler, ArithmeticError, ValueError):
            continue
        if pruefer.bereiche_gleich(v, soll) or any(pruefer.bereiche_gleich(v, g) for g in gesehen):
            continue
        gesehen.append(v)
        erg.append((w, m))
    return erg


def _ohne_gleiche_term(loesung, fehler, var="x"):
    """Wie engine.ohne_gleiche, aber für Terme (Äquivalenz statt Zahlvergleich)."""
    soll = pruefer.parse(loesung, [var]).ast
    erg, gesehen = [], []
    for w, m in fehler:
        a = pruefer.parse(w, [var]).ast
        if pruefer.aequivalent(a, soll, [var]).ok or any(pruefer.aequivalent(a, g, [var]).ok for g in gesehen):
            continue
        gesehen.append(a)
        erg.append((w, m))
    return erg


def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


def _xglied(c):
    """'+ 3x', '- x' (Koeffizient 1 wird weggelassen)."""
    return ("- " if c < 0 else "+ ") + ("" if abs(c) == 1 else str(abs(c))) + "x"


def _linearfaktor(r):
    """(x - r) als LaTeX bzw. Term-Text; r = 0 ergibt x."""
    return "x" if r == 0 else f"(x {vz(-r)})"


k = neues_kapitel(
    slug="quadratisch",
    titel="Quadratische Gleichungen",
    beschreibung="Normalform, Nullprodukt, quadratische Ergänzung, pq- und Mitternachtsformel, Diskriminante, Vieta",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="🏹")

k.lernziele([
    "Ich erkenne quadratische Gleichungen und bringe sie in die Normalform $x^2 + px + q = 0$",
    "Ich löse einfache Fälle ohne Formel: Wurzel ziehen, Ausklammern, Satz vom Nullprodukt",
    "Ich löse jede quadratische Gleichung mit der pq-Formel oder der Mitternachtsformel",
    "Ich sage mit der Diskriminante vorher, ob es zwei, eine oder keine Lösung gibt",
    "Ich zerlege $x^2 + px + q$ mit dem Satz von Vieta in Linearfaktoren",
])

k.warum(r"""
Quadratische Gleichungen tauchen in der Informatik ständig auf. Beim Raytracing (so
entstehen Bilder in Filmen und Spielen) prüft der Computer, ob ein Lichtstrahl eine
Kugel trifft. Das ist eine quadratische Gleichung, und die [[Diskriminante]] sagt
sofort: Treffer, Streifschuss oder daneben. In Mathe 1 berechnest du Eigenwerte einer
$2 \times 2$-Matrix als Lösungen einer quadratischen Gleichung. Und beim Abschätzen
von Laufzeiten fragst du: Ab welchem $n$ ist $n^2$ größer als $10n + 200$?
""")

# ── 1: Begriff und Normalform ─────────────────────────────────────────────
k.erklaerung("Was ist eine quadratische Gleichung?", r"""
    ## Wenn $x$ im Quadrat vorkommt

    :::analogie 🌱 Das quadratische Beet
    Ein quadratisches Beet hat $49$ Quadratmeter Fläche. Wie lang ist eine Seite?
    Nennst du die Seitenlänge $x$, dann gilt $x^2 = 49$.
    :::

    Eine [[quadratische Gleichung]] lässt sich in die Form $ax^2 + bx + c = 0$ mit
    $a \neq 0$ bringen. Die höchste Potenz von $x$ ist $2$.

    Eine **Lösung** ist eine Zahl, die beim Einsetzen eine wahre Aussage ergibt.

    :::rechnung Ist $3$ eine Lösung von $x^2 - 4x + 3 = 0$?
    3^2 - 4 \cdot 3 + 3 = 9 - 12 + 3 || $x = 3$ einsetzen
    = 0 || wahr: $3$ ist eine Lösung
    2^2 - 4 \cdot 2 + 3 = -1 || $x = 2$ einsetzen: $-1$ ist nicht $0$, also keine Lösung
    :::

    :::alt Als Zahlenrätsel erklärt
    Ich denke mir eine Zahl. Ich nehme sie mal sich selbst, ziehe das Vierfache der
    Zahl ab und addiere $3$. Heraus kommt $0$. Welche Zahl war es? Genau das fragt
    $x^2 - 4x + 3 = 0$. Probier die $1$: $1 - 4 + 3 = 0$. Auch die $1$ passt!
    Quadratische Gleichungen haben oft zwei Lösungen.
    :::
    ---
    ## Die Normalform

    Teilst du die ganze Gleichung durch $a$, steht vor $x^2$ eine $1$. Diese Form
    heißt [[Normalform]]:

    $$x^2 + px + q = 0$$

    Die Lösungen ändern sich dabei nicht, denn rechts bleibt $0 : a = 0$.

    :::rechnung $2x^2 - 8x + 6 = 0$ auf Normalform bringen
    \frac{2x^2 - 8x + 6}{2} = \frac{2x^2}{2} - \frac{8x}{2} + \frac{6}{2} || jeden Summanden durch $a = 2$ teilen
    = x^2 - 4x + 3 || kürzen
    :::

    Die Normalform ist $x^2 - 4x + 3 = 0$. Also ist $p = -4$ und $q = 3$: Das
    Vorzeichen gehört zur Zahl.

    :::achtung Nur einen Teil geteilt
    $x^2 - 8x + 6 = 0$ ist falsch. **Jeder** Summand muss durch $2$ geteilt werden,
    nicht nur der vor $x^2$.
    :::

    :::alt Mit einem Rezept erklärt
    Ein Kuchenrezept für $2$ Bleche halbierst du für $1$ Blech. Dann halbierst du
    **jede** Zutat, nicht nur das Mehl. Der Kuchen schmeckt gleich, er ist nur
    kleiner. Genauso hier: Jeder Summand wird durch $2$ geteilt, und die Lösungen
    bleiben dieselben.
    :::
    """)

k.mc("Welche Gleichung ist eine quadratische Gleichung?",
     ["$3x^2 - x = 4$", "$3x - 4 = 0$", "$x^3 + x^2 = 1$", "$2x + 5 = x - 1$"],
     "Bei $3x^2 - x = 4$ ist die höchste Potenz von $x$ genau $2$. Umgestellt: $3x^2 - x - 4 = 0$ mit $a = 3$.",
     tipps=["Suche die höchste Potenz von $x$.", "Quadratisch heißt: Die höchste Potenz ist genau $2$."],
     fehler={"$3x - 4 = 0$": "Hier kommt $x$ nur einfach vor, nicht im Quadrat. Das ist eine lineare Gleichung.",
             "$x^3 + x^2 = 1$": "Hier kommt $x^3$ vor. Die höchste Potenz ist $3$, nicht $2$. Das ist eine Gleichung dritten Grades."})

k.luecke("Bringe $3x^2 - 12x + 9 = 0$ auf Normalform. Was gehört in die Lücken?",
         "x^2 + \\luecke \\, x + \\luecke = 0", [[-4], [3]],
         "Alles durch $3$ teilen: $\\frac{-12}{3} = -4$ und $\\frac{9}{3} = 3$. Also $p = -4$ und $q = 3$.",
         tipps=["Vor $x^2$ soll eine $1$ stehen. Wodurch musst du teilen?",
                "Teile **jeden** Summanden durch $3$.",
                "$-12 : 3 = -4$ und $9 : 3 = 3$."],
         rechenweg=r"""
         :::rechnung
         \frac{3x^2 - 12x + 9}{3} = \frac{3x^2}{3} - \frac{12x}{3} + \frac{9}{3} || jeden Summanden durch $3$ teilen
         = x^2 - 4x + 3 || kürzen: $p = -4$, $q = 3$
         :::
         """,
         typische_fehler=[([-12, 9], "Du hast nur $x^2$ durch $3$ geteilt. **Jeder** Summand muss durch $3$ geteilt werden."),
                          ([4, 3], "Das Vorzeichen gehört zur Zahl: Aus $-12x$ wird $-4x$, also ist $p = -4$.")])

# ── 2: Einfache Fälle ─────────────────────────────────────────────────────
k.erklaerung("Einfache Fälle ohne Formel", r"""
    ## Nur $x^2$ und eine Zahl

    Fehlt der Teil mit $x$, stellst du nach $x^2$ um und ziehst die Wurzel. Aber
    Vorsicht: Auch $(-7)^2 = 49$. Es gibt **zwei** Lösungen.

    :::visual funktionsgraph
    {"funktionen": [{"term": "x^2", "label": "f(x)"}, {"term": "4", "label": "g(x)"}],
     "punkte": [{"x": -2, "y": 4}, {"x": 2, "y": 4}], "x": [-4, 4], "y": [-1, 8],
     "unterschrift": "Die Parabel $y = x^2$ erreicht die Höhe $4$ zweimal: bei $x = -2$ und bei $x = 2$."}
    :::

    :::rechnung $x^2 - 49 = 0$ lösen
    x^2 - 49 = 0 || Aufgabe
    x^2 = 49 || $+49$ auf beiden Seiten
    x_1 = 7 || positive Wurzel: $\sqrt{49} = 7$
    x_2 = -7 || negative Wurzel: $(-7)^2 = 49$ passt auch
    :::

    :::achtung Eine Lösung vergessen
    $x^2 = 49$ hat **zwei** Lösungen, $7$ und $-7$. Und $x^2 = -4$ hat **keine**:
    Kein Quadrat einer reellen Zahl ist negativ.
    :::

    :::alt Mit Spiegeln erklärt
    Quadrieren macht aus $7$ und aus $-7$ dasselbe: $49$. Die beiden Zahlen liegen
    spiegelbildlich zur $0$. Wer rückwärts von $49$ ausgeht, muss also beide
    Spiegelbilder finden. Nur bei $0$ fallen sie zusammen: $x^2 = 0$ hat genau eine
    Lösung, die $0$.
    :::
    ---
    ## Ein Produkt ist null

    !! Ein Produkt ist genau dann $0$, wenn mindestens ein Faktor $0$ ist.

    Das ist der [[Satz vom Nullprodukt]]. Fehlt die Zahl ohne $x$, hilft [[Ausklammern]]
    von $x$ und danach dieser Satz.

    :::rechnung $x^2 - 5x = 0$ lösen
    x^2 - 5x = 0 || Aufgabe: keine Zahl ohne $x$
    x(x - 5) = 0 || $x$ ausklammern
    x = 0 \text{ oder } x - 5 = 0 || ein Faktor muss $0$ sein
    x_1 = 0 || erster Faktor
    x_2 = 5 || zweiter Faktor: $x - 5 = 0$
    :::

    :::achtung Durch $x$ geteilt
    Wer $x^2 = 5x$ durch $x$ teilt, erhält nur $x = 5$. Die Lösung $0$ geht verloren,
    denn durch $0$ darf man nicht teilen. Klammere aus, statt zu teilen.
    :::

    :::alt Mit dem Taschenrechner erklärt
    Egal, welche Zahl du mit $0$ malnimmst: Es kommt $0$ heraus. Umgekehrt ergeben
    zwei Zahlen, die beide nicht $0$ sind, nie $0$, z. B. $3 \cdot (-2) = -6$.
    Kommt bei $x \cdot (x - 5)$ also $0$ heraus, muss schon $x$ oder $x - 5$ null
    gewesen sein.
    :::
    """)

k.gleichung("x^2 = 25",
            erklaerung="Wurzel ziehen, beide Vorzeichen: $x = 5$ oder $x = -5$, denn $(-5)^2 = 25$. Eingeben kannst du das als {5; -5} oder kurz als ±5.",
            tipps=["Welche Zahl ergibt mal sich selbst $25$?", "Es gibt eine positive und eine negative Zahl.",
                   "$5^2 = 25$ und $(-5)^2 = 25$."],
            rechenweg=r"""
            :::rechnung
            x^2 = 25 || Aufgabe
            x_1 = 5 || $\sqrt{25} = 5$
            x_2 = -5 || $(-5)^2 = 25$ passt auch
            :::
            """,
            typische_fehler=[("{5}", "Die negative Lösung fehlt: Auch $(-5)^2 = 25$."),
                             ("{12.5}", "Du hast durch $2$ geteilt. $x^2$ heißt $x \\cdot x$, nicht $2x$. Zieh die Wurzel.")])

k.gleichung("x^2 - 7x = 0",
            erklaerung="$x$ ausklammern: $x(x - 7) = 0$. Nach dem Satz vom Nullprodukt ist $x = 0$ oder $x = 7$.",
            tipps=["Es gibt keine Zahl ohne $x$. Was kannst du ausklammern?",
                   "$x(x - 7) = 0$. Wann ist ein Produkt null?",
                   "Ein Faktor muss $0$ sein: $x = 0$ oder $x - 7 = 0$."],
            rechenweg=r"""
            :::rechnung
            x^2 - 7x = 0 || Aufgabe
            x(x - 7) = 0 || $x$ ausklammern
            x = 0 \text{ oder } x - 7 = 0 || Satz vom Nullprodukt
            x_1 = 0 || erster Faktor
            x_2 = 7 || zweiter Faktor
            :::
            """,
            typische_fehler=[("{7}", "Die Lösung $0$ fehlt. Hast du durch $x$ geteilt? Das darf man nicht, denn $x$ könnte $0$ sein."),
                             ("{0; -7}", "Vorzeichen: $x - 7 = 0$ ergibt $x = 7$, nicht $-7$.")])

k.wf("Die Gleichung $x^2 = -9$ hat die Lösungen $3$ und $-3$.", False,
     "Falsch. $3^2 = 9$ und $(-3)^2 = 9$, beide sind positiv. Kein Quadrat einer reellen Zahl ist negativ. "
     "Die Gleichung hat in $\\mathbb{R}$ keine Lösung.",
     tipps=["Rechne $(-3)^2$ aus. Kommt $-9$ heraus?"])

# ── 3: Die Formeln ────────────────────────────────────────────────────────
k.erklaerung("Quadratische Ergänzung und die Lösungsformeln", r"""
    ## Ein Quadrat ergänzen

    Bei $x^2 + 6x + 5 = 0$ hilft Ausklammern nicht. Die Idee: Mach aus $x^2 + 6x$
    ein vollständiges Quadrat. Die [[binomische Formel|binomische Formeln]] $(x + 3)^2 = x^2 + 6x + 9$
    zeigt: Es fehlt nur die $9$. Du addierst sie und ziehst sie sofort wieder ab.
    Das heißt [[quadratische Ergänzung]].

    :::rechnung $x^2 + 6x + 5 = 0$ lösen
    x^2 + 6x + 5 = 0 || Aufgabe
    x^2 + 6x + \hl{9 - 9} + 5 = 0 || $\left(\frac{6}{2}\right)^2 = 9$ addieren und wieder abziehen
    (x + 3)^2 - 4 = 0 || binomische Formel; $-9 + 5 = -4$
    (x + 3)^2 = 4 || $+4$ auf beiden Seiten
    x + 3 = 2 \text{ oder } x + 3 = -2 || Wurzel ziehen, beide Vorzeichen
    x_1 = -1 || $2 - 3 = -1$
    x_2 = -5 || $-2 - 3 = -5$
    :::

    :::alt Mit Fliesen erklärt
    Leg $x^2$ als Quadrat mit der Seite $x$. Die $6x$ teilst du in zwei Streifen
    $3 \cdot x$ und legst sie an zwei Seiten an. Fast ist ein großes Quadrat mit der
    Seite $x + 3$ entstanden. Nur die Ecke fehlt: ein kleines Quadrat $3 \cdot 3 = 9$.
    Legst du diese Ecke dazu, hast du genau $(x + 3)^2$. Deshalb heißt es Ergänzung.
    :::
    ---
    ## Die pq-Formel

    Rechnet man die quadratische Ergänzung allgemein für $x^2 + px + q = 0$, entsteht
    die [[pq-Formel]]:

    $$x_{1,2} = -\frac{p}{2} \pm \sqrt{\left(\frac{p}{2}\right)^2 - q}$$

    Sie gilt nur für die Normalform. Beispiel $x^2 - 2x - 8 = 0$, also $p = -2$, $q = -8$:

    :::rechnung pq-Formel Schritt für Schritt
    -\frac{-2}{2} = 1 || $-\frac{p}{2}$: das Vorzeichen von $p$ mitnehmen
    \left(\frac{-2}{2}\right)^2 - (-8) = 1 + 8 = 9 || unter der Wurzel
    \sqrt{9} = 3 || Wurzel ziehen
    1 + 3 = 4 || $x_1 = 4$ (mit Plus)
    1 - 3 = -2 || $x_2 = -2$ (mit Minus)
    (-2)^2 - 2 \cdot (-2) - 8 = 0 || Probe für $x_2$: stimmt
    :::

    :::visual parabel
    {"a": 1, "b": -2, "c": -8, "x": [-5, 7], "y": [-10, 6],
     "unterschrift": "Die Lösungen sind die Nullstellen der Parabel. Sie liegen symmetrisch um $x = 1$."}
    :::

    :::achtung Vorzeichen von $p$
    Bei $p = -2$ ist $-\frac{p}{2} = +1$, nicht $-1$. Schreib $p$ und $q$ immer mit
    Vorzeichen heraus. Und: Erst auf Normalform bringen!
    :::

    :::alt Mit der Symmetrieachse erklärt
    Die Parabel $y = x^2 - 2x - 8$ ist spiegelsymmetrisch. Ihre Achse liegt bei
    $x = -\frac{p}{2} = 1$. Die beiden [[Nullstellen|Nullstelle]] liegen gleich weit
    links und rechts davon. Wie weit, sagt die Wurzel: hier $3$. Die Formel heißt
    also: Geh zur Mitte $1$, dann $3$ nach rechts ($4$) und $3$ nach links ($-2$).
    :::
    ---
    ## Die Mitternachtsformel

    Willst du nicht erst durch $a$ teilen, nimm die [[Mitternachtsformel]] (auch
    abc-Formel) für $ax^2 + bx + c = 0$:

    $$x_{1,2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

    Beispiel $2x^2 + 3x - 2 = 0$, also $a = 2$, $b = 3$, $c = -2$:

    :::rechnung Mitternachtsformel Schritt für Schritt
    3^2 - 4 \cdot 2 \cdot (-2) = 9 + 16 = 25 || unter der Wurzel: $b^2 - 4ac$
    \sqrt{25} = 5 || Wurzel ziehen
    \frac{-3 + 5}{2 \cdot 2} = \frac{2}{4} = \frac{1}{2} || $x_1$ mit Plus
    \frac{-3 - 5}{2 \cdot 2} = \frac{-8}{4} = -2 || $x_2$ mit Minus
    :::

    :::achtung Zwei Stolperfallen
    Der **ganze** Zähler wird durch $2a = 4$ geteilt, nicht durch $2$. Und
    $-4ac$ mit negativem $c$ wird plus: $-4 \cdot 2 \cdot (-2) = +16$.
    :::

    :::alt Woher der Name kommt
    Man sagt: Diese Formel musst du auch können, wenn dich jemand um Mitternacht weckt.
    Inhaltlich ist sie die pq-Formel, nur ohne vorher durch $a$ zu teilen. Setzt du
    $p = \frac{b}{a}$ und $q = \frac{c}{a}$ in die pq-Formel ein und fasst zusammen,
    entsteht genau diese Formel. Du kannst also immer die Formel nehmen, die dir lieber ist.
    :::
    """)

k.gleichung("x^2 + 2x - 15 = 0",
            erklaerung="pq-Formel mit $p = 2$, $q = -15$: $x = -1 \\pm \\sqrt{1 + 15} = -1 \\pm 4$, also $3$ und $-5$.",
            tipps=["Die Gleichung steht schon in Normalform. Lies $p$ und $q$ mit Vorzeichen ab.",
                   "$p = 2$, $q = -15$. Also $-\\frac{p}{2} = -1$.",
                   "Unter der Wurzel: $1 - (-15) = 16$. Dann $-1 \\pm 4$."],
            rechenweg=r"""
            :::rechnung
            -\frac{2}{2} = -1 || $-\frac{p}{2}$ mit $p = 2$
            \left(\frac{2}{2}\right)^2 - (-15) = 1 + 15 = 16 || unter der Wurzel, $q = -15$
            \sqrt{16} = 4 || Wurzel ziehen
            -1 + 4 = 3 || $x_1$
            -1 - 4 = -5 || $x_2$
            3^2 + 2 \cdot 3 - 15 = 0 || Probe für $x_1$
            :::
            """,
            typische_fehler=[("{5; -3}", "Die Vorzeichen sind vertauscht. Vorne steht $-\\frac{p}{2}$: Bei $p = 2$ ist das $-1$, nicht $+1$."),
                             ("{3}", "Es fehlt die zweite Lösung. Rechne $-1 - 4$ mit dem Minus der Formel.")])

k.gleichung("2x^2 - 5x + 2 = 0",
            erklaerung="Mitternachtsformel mit $a = 2$, $b = -5$, $c = 2$: unter der Wurzel $25 - 16 = 9$, "
                       "$x = \\frac{5 \\pm 3}{4}$, also $2$ und $\\frac{1}{2}$.",
            tipps=["Lies $a$, $b$ und $c$ mit Vorzeichen ab.",
                   "$b^2 - 4ac = (-5)^2 - 4 \\cdot 2 \\cdot 2 = 9$.",
                   "$x = \\frac{5 \\pm 3}{2 \\cdot 2}$. Teile durch $4$."],
            rechenweg=r"""
            :::rechnung
            (-5)^2 - 4 \cdot 2 \cdot 2 = 25 - 16 = 9 || unter der Wurzel: $b^2 - 4ac$
            \sqrt{9} = 3 || Wurzel ziehen
            \frac{5 + 3}{2 \cdot 2} = \frac{8}{4} = 2 || $x_1$: $-b = 5$, mit Plus
            \frac{5 - 3}{2 \cdot 2} = \frac{2}{4} = \frac{1}{2} || $x_2$: mit Minus
            :::
            """,
            typische_fehler=[("{1; 4}", "Du hast nur durch $2$ geteilt. Der Nenner ist $2a = 2 \\cdot 2 = 4$."),
                             ("{-2; -1/2}", "Vorzeichen: Vorne steht $-b$. Bei $b = -5$ ist $-b = +5$.")])

# ── 4: Diskriminante ──────────────────────────────────────────────────────
k.erklaerung("Wie viele Lösungen gibt es?", r"""
    ## Die Diskriminante

    Der Ausdruck unter der Wurzel heißt [[Diskriminante]]: $D = b^2 - 4ac$. Schon
    bevor du die Lösungen ausrechnest, sagt er dir, wie viele es gibt:

    | Diskriminante | Lösungen in $\mathbb{R}$ |
    |---|---|
    | $D > 0$ | zwei |
    | $D = 0$ | genau eine |
    | $D < 0$ | keine |

    :::visual funktionsgraph
    {"funktionen": [{"term": "x^2 - 2*x + c", "label": "f(x)"}],
     "parameter": [{"name": "c", "wert": -3, "von": -4, "bis": 4, "schritt": 0.5}],
     "nullstellen": true, "x": [-4, 6], "y": [-5, 8],
     "unterschrift": "Schiebe $c$: Bei $c = 1$ berührt die Parabel die Achse ($D = 0$), darüber schwebt sie ($D < 0$)."}
    :::

    :::rechnung Drei Gleichungen, drei Fälle
    (-2)^2 - 4 \cdot 1 \cdot (-3) = 16 || $x^2 - 2x - 3 = 0$: $D > 0$, zwei Lösungen
    (-2)^2 - 4 \cdot 1 \cdot 1 = 0 || $x^2 - 2x + 1 = 0$: $D = 0$, eine Lösung
    (-2)^2 - 4 \cdot 1 \cdot 2 = -4 || $x^2 - 2x + 2 = 0$: $D < 0$, keine Lösung
    :::

    :::alt Ohne Bild erklärt
    Die Lösungen sind „Mitte plus Wurzel“ und „Mitte minus Wurzel“, und unter der
    Wurzel steht $D$. Ist $D$ positiv, sind plus und minus zwei verschiedene Zahlen.
    Ist $D = 0$, ist $+0$ dasselbe wie $-0$: nur eine Lösung. Ist $D$ negativ, gibt
    es keine reelle Wurzel, also keine Lösung.
    :::
    """)

k.zahl("Berechne die Diskriminante $D = b^2 - 4ac$ von $x^2 + 4x + 5 = 0$.", 4 ** 2 - 4 * 1 * 5,
       "$D = 4^2 - 4 \\cdot 1 \\cdot 5 = 16 - 20 = -4$. Weil $D < 0$ ist, hat die Gleichung keine reelle Lösung.",
       tipps=["Lies ab: $a = 1$, $b = 4$, $c = 5$.", "Setze ein: $4^2 - 4 \\cdot 1 \\cdot 5$.", "$16 - 20$"],
       rechenweg=r"""
       :::rechnung
       4^2 - 4 \cdot 1 \cdot 5 = 16 - 20 || einsetzen: $a = 1$, $b = 4$, $c = 5$
       = -4 || negativ: keine Lösung
       :::
       """,
       typische_fehler=[(36, "Du hast $+4ac$ gerechnet. In der Formel steht $b^2 \\hl{-} 4ac$."),
                        (-12, "$4^2 = 16$, nicht $8$. Quadrieren heißt mit sich selbst malnehmen.")])

k.zuordnen("Ordne jeder Gleichung die Anzahl ihrer reellen Lösungen zu.",
           [("$x^2 - 6x + 9 = 0$", "genau eine Lösung"),
            ("$x^2 + x + 1 = 0$", "keine Lösung"),
            ("$x^2 - x - 2 = 0$", "zwei Lösungen")],
           "Diskriminanten: $36 - 36 = 0$, $1 - 4 = -3$ und $1 + 8 = 9$.",
           tipps=["Berechne für jede Gleichung $D = b^2 - 4ac$ und schau nur auf das Vorzeichen."],
           rechenweg=r"""
           :::rechnung
           (-6)^2 - 4 \cdot 1 \cdot 9 = 0 || $D = 0$: genau eine Lösung
           1^2 - 4 \cdot 1 \cdot 1 = -3 || $D < 0$: keine Lösung
           (-1)^2 - 4 \cdot 1 \cdot (-2) = 9 || $D > 0$: zwei Lösungen
           :::
           """)

# ── 5: Vieta ──────────────────────────────────────────────────────────────
k.erklaerung("Der Satz von Vieta", r"""
    ## Lösungen und Faktoren

    Hat $x^2 + px + q = 0$ die Lösungen $x_1$ und $x_2$, dann gilt

    $$x^2 + px + q = (x - x_1)(x - x_2)$$

    Ausmultiplizieren zeigt: $x_1 + x_2 = -p$ und $x_1 \cdot x_2 = q$. Das ist der
    [[Satz von Vieta]]. Sind die Lösungen ganze Zahlen, kannst du sie damit oft im
    Kopf finden.

    :::rechnung $x^2 - 5x + 6$ zerlegen
    2 \cdot 3 = 6 || zwei Zahlen mit Produkt $q = 6$ suchen
    2 + 3 = 5 || ihre Summe muss $-p = 5$ sein
    (x - 2)(x - 3) = x^2 - 3x - 2x + 6 || Probe: ausmultiplizieren
    = x^2 - 5x + 6 || stimmt
    :::

    Die Lösungen von $x^2 - 5x + 6 = 0$ sind also $2$ und $3$.

    :::achtung Vorzeichen in der Klammer
    Die Lösung $2$ gehört zum Faktor $(x \hl{-} 2)$, nicht zu $(x + 2)$.
    Prüfe: Bei $x = 2$ muss die Klammer $0$ werden.
    :::

    :::alt Rückwärts gedacht
    Du kennst die Lösungen $2$ und $3$ und suchst eine Gleichung dazu.
    $(x - 2)(x - 3) = 0$ hat genau diese Lösungen, das sagt der Satz vom Nullprodukt.
    Multiplizierst du aus, erhältst du $x^2 - 5x + 6 = 0$. Die $-5$ ist minus die
    Summe der Lösungen, die $6$ ihr Produkt. Vieta liest diesen Weg rückwärts.
    :::
    """)

k.term("Zerlege $x^2 - x - 12$ in Linearfaktoren, also in die Form $(x - x_1)(x - x_2)$.",
       "(x - 4)(x + 3)",
       "Gesucht sind zwei Zahlen mit Produkt $-12$ und Summe $1$: $4$ und $-3$. Also $(x - 4)(x + 3)$.",
       variablen="x", form="linearfaktoren",
       tipps=["Suche zwei Zahlen mit Produkt $q = -12$ und Summe $-p = 1$.",
              "Ein Produkt von $-12$ heißt: eine Zahl ist positiv, eine negativ.",
              "$4 \\cdot (-3) = -12$ und $4 + (-3) = 1$."],
       rechenweg=r"""
       :::rechnung
       4 \cdot (-3) = -12 || Produkt gleich $q = -12$
       4 + (-3) = 1 || Summe gleich $-p = 1$
       (x - 4)(x + 3) = x^2 + 3x - 4x - 12 || Probe: ausmultiplizieren
       = x^2 - x - 12 || stimmt
       :::
       """,
       typische_fehler=[("(x + 4)(x - 3)", "Die Vorzeichen sind vertauscht. Zur Lösung $4$ gehört der Faktor $(x - 4)$. "
                                           "Probe: $(x + 4)(x - 3) = x^2 + x - 12$."),
                        ("(x - 6)(x + 2)", "Das Produkt stimmt ($-12$), aber die Summe $6 + (-2) = 4$ muss $1$ sein.")])


# ── Praxis ────────────────────────────────────────────────────────────────
def quadratische_gleichung_loesen(rng):
    a = rng.choice([1, 1, 1, 2, 3, -1, -2])
    art = rng.choices(["zwei", "eine", "keine"], [7, 2, 1])[0]
    if art == "zwei":
        r1, r2 = rng.sample(range(-7, 8), 2)
        p, q = -(r1 + r2), r1 * r2
    elif art == "eine":
        r1 = r2 = rng.choice([x for x in range(-6, 7) if x])
        p, q = -2 * r1, r1 * r1
    else:
        p = rng.choice([-6, -4, -2, 0, 2, 4, 6])
        q = (p // 2) ** 2 + rng.randint(1, 6)
    p, q = F(p), F(q)
    gl = _poly(a, a * p, a * q)
    norm = _poly(1, p, q)
    zeilen = []
    if a != 1:
        zeilen.append((f"\\frac{{{gl.tex()}}}{{{tex(a)}}} = {norm.tex()}",
                       f"durch $a = {tex(a)}$ teilen: Normalform"))
    rad = p * p / 4 - q
    ablesen = f"$p = {tex(p)}$ und $q = {tex(q)}$ ablesen"
    erste = f"-\\frac{{{tex(p)}}}{{2}}"
    if erste != tex(-p / 2):
        zeilen.append((f"{erste} = {tex(-p / 2)}", ablesen + "; $-\\frac{p}{2}$ berechnen"))
        grund = "unter der Wurzel"
    else:
        grund = ablesen + f"; $-\\frac{{p}}{{2}} = {tex(-p / 2)}$; unter der Wurzel"
    zeilen.append((f"\\left(\\frac{{{tex(p)}}}{{2}}\\right)^2 - {tk(q)} = {tex(p * p / 4)} - {tk(q)} = {tex(rad)}",
                   grund))
    fehler = []
    if rad < 0:
        loesung = "{}"
        zeilen.append((f"{tex(rad)} < 0", "negativ: Aus einer negativen Zahl gibt es keine reelle Wurzel"))
        falsch = pruefer.bereich_text(mathlib.loese(f"x^2 + ({mathlib.text(p)})*x + ({mathlib.text(p * p / 2 - q)}) = 0"))
        fehler.append((falsch, "Unter der Wurzel steht eine negative Zahl. Du hast ihr Minus einfach weggelassen. "
                               "Dann gibt es aber keine reelle Lösung: $\\mathbb{L} = \\emptyset$."))
        erkl = "Die Zahl unter der Wurzel ist negativ, also gibt es keine reelle Lösung."
    else:
        w = F(abs(r1 - r2), 2)
        x1, x2 = -p / 2 + w, -p / 2 - w
        zeilen.append((f"\\sqrt{{{tex(rad)}}} = {tex(w)}", "Wurzel ziehen"))
        if rad == 0:
            zeilen.append((f"x = {tex(x1)}", "Wurzel ist $0$: Plus und Minus geben dieselbe Zahl"))
            loesung = _menge([x1])
            fehler.append((_menge([-x1]), "Vorzeichen: Vorne steht $-\\frac{p}{2}$, also das **Gegenteil** von $\\frac{p}{2}$."))
        else:
            zeilen.append((f"{tex(-p / 2)} + {tex(w)} = {tex(x1)}", "$x_1$ mit Plus"))
            zeilen.append((f"{tex(-p / 2)} - {tex(w)} = {tex(x2)}", "$x_2$ mit Minus"))
            zeilen.append((f"x_1 = {tex(x1)}", "erste Lösung"))
            zeilen.append((f"x_2 = {tex(x2)}", "zweite Lösung"))
            loesung = _menge(sorted([x1, x2]))
            fehler.append((_menge([-x1, -x2]), "Die Vorzeichen sind vertauscht. Vorne steht $-\\frac{p}{2}$: "
                                               "das Vorzeichen von $p$ umdrehen."))
            fehler.append((_menge([x1]), "Es fehlt eine Lösung. Die Formel hat ein $\\pm$: einmal plus, einmal minus."))
        erkl = "Normalform, dann pq-Formel: $-\\frac{p}{2} \\pm \\sqrt{\\left(\\frac{p}{2}\\right)^2 - q}$."
    if a != 1:
        try:
            ohne = pruefer.bereich_text(mathlib.loese(f"x^2 + ({a * p})*x + ({a * q}) = 0"))
            fehler.append((ohne, f"Du hast vergessen, erst durch $a = {tex(a)}$ zu teilen. "
                                 "Die pq-Formel gilt nur für die Normalform."))
        except ValueError:
            pass
    return {
        "frage": f"Löse ${gl.tex()} = 0$. Gib die Lösungsmenge an.",
        "loesung": loesung,
        "tipps": ["Steht die Gleichung in Normalform? Sonst erst durch $a$ teilen." if a != 1
                  else "Die Gleichung steht schon in Normalform $x^2 + px + q = 0$.",
                  f"$p = {tex(p)}$ und $q = {tex(q)}$.",
                  f"Unter der Wurzel steht $\\left(\\frac{{p}}{{2}}\\right)^2 - q = {tex(rad)}$."],
        "rechenweg": f"Gleichung: ${gl.tex()} = 0$\n\n" + _zeilen(*zeilen),
        "erklaerung": erkl,
        "typische_fehler": _ohne_gleiche_menge(loesung, fehler),
    }


k.praxis()

k.generator(quadratische_gleichung_loesen, typ="loesungsmenge", titel="Quadratische Gleichungen lösen")


def anzahl_loesungen(rng):
    while True:
        a = rng.choice([1, 1, 2, 3, -1, -2])
        art = rng.choice(["null", "zufall", "zufall"])
        if art == "null":
            r = rng.choice([x for x in range(-4, 5) if x])
            b, c = -2 * a * r, a * r * r
        else:
            b, c = rng.randint(-8, 8), rng.choice([x for x in range(-9, 10) if x])
        d = b * b - 4 * a * c
        if abs(d) <= 120:
            break
    n = 2 if d > 0 else 1 if d == 0 else 0
    falsch_d = b * b + 4 * a * c
    n_falsch = 2 if falsch_d > 0 else 1 if falsch_d == 0 else 0
    gl = _poly(a, b, c)
    fehler = [(n_falsch, f"Achte auf das Minus in $b^2 - 4ac$: Du hast vermutlich $b^2 + 4ac = {falsch_d}$ gerechnet.")]
    if n == 1:
        fehler.append((2, "$D = 0$ heißt: Plus und Minus der Wurzel geben dieselbe Zahl. Es ist nur **eine** Lösung."))
    elif n == 2:
        fehler.append((1, f"$D = {d}$ ist positiv. Dann liefern Plus und Minus der Wurzel **zwei** verschiedene Lösungen."))
    else:
        fehler.append((2, f"$D = {d}$ ist negativ. Aus einer negativen Zahl gibt es keine reelle Wurzel, also **keine** Lösung."))
    return {
        "frage": f"Wie viele reelle Lösungen hat ${gl.tex()} = 0$? Gib die Anzahl an.",
        "loesung": n,
        "tipps": ["Berechne die Diskriminante $D = b^2 - 4ac$.",
                  f"$a = {tex(a)}$, $b = {tex(b)}$, $c = {tex(c)}$.",
                  "$D > 0$: zwei, $D = 0$: eine, $D < 0$: keine Lösung."],
        "rechenweg": _zeilen((f"{tk(b)}^2 - 4 \\cdot {tk(a)} \\cdot {tk(c)} = {b * b} - {tk(4 * a * c)} = {d}",
                              f"$D = b^2 - 4ac$ mit $a = {tex(a)}$, $b = {tex(b)}$, $c = {tex(c)}$"))
        + "\n\n" + ("$D > 0$: zwei Lösungen." if n == 2 else "$D = 0$: genau eine Lösung." if n == 1
                     else "$D < 0$: keine reelle Lösung."),
        "erklaerung": "Die Diskriminante $D = b^2 - 4ac$ entscheidet über die Anzahl der Lösungen.",
        "typische_fehler": ohne_gleiche(n, fehler),
    }


k.generator(anzahl_loesungen, typ="zahl", titel="Anzahl der Lösungen (Diskriminante)", glatt=True)


def vieta_zerlegen(rng):
    r1, r2 = rng.sample([x for x in range(-9, 10) if x], 2)
    p, q = -(r1 + r2), r1 * r2
    poly = _poly(1, p, q)
    loesung = f"{_linearfaktor(r1)}{_linearfaktor(r2)}"
    fehler = [(f"{_linearfaktor(-r1)}{_linearfaktor(-r2)}",
               "Die Vorzeichen in den Klammern sind vertauscht. Zur Lösung $x_1$ gehört der Faktor $(x - x_1)$."),
              (f"{_linearfaktor(r1)}{_linearfaktor(-r2)}",
               "Ein Vorzeichen stimmt nicht. Probe: Multipliziere aus und vergleiche mit der Aufgabe.")]
    mitte = f"x^2 {_xglied(-r2)} {_xglied(-r1)} {vz(q)}"
    return {
        "frage": f"Zerlege ${poly.tex()}$ in Linearfaktoren, also in die Form $(x - x_1)(x - x_2)$.",
        "loesung": loesung, "variablen": "x", "form": "linearfaktoren",
        "tipps": [f"Suche zwei Zahlen mit Produkt $q = {q}$ und Summe $-p = {-p}$.",
                  "Ist $q$ negativ, hat eine Zahl ein Minus. Ist $q$ positiv, haben beide dasselbe Vorzeichen.",
                  f"Eine der Zahlen ist ${r1}$."],
        "rechenweg": _zeilen((f"{tk(r1)} \\cdot {tk(r2)} = {q}", f"Produkt gleich $q = {q}$"),
                             (f"{tk(r1)} + {tk(r2)} = {-p}", f"Summe gleich $-p = {-p}$"),
                             (f"{_linearfaktor(r1)}{_linearfaktor(r2)} = {mitte}", "Probe: ausmultiplizieren"),
                             (f"= {poly.tex()}", "stimmt")),
        "erklaerung": "Satz von Vieta: Die Lösungen haben die Summe $-p$ und das Produkt $q$.",
        "typische_fehler": _ohne_gleiche_term(loesung, fehler),
    }


k.generator(vieta_zerlegen, typ="term", titel="Mit Vieta in Linearfaktoren zerlegen")

k.zahl("Für welche Zahl $c$ hat $x^2 + 6x + c = 0$ **genau eine** Lösung?", 9,
       "Genau eine Lösung heißt $D = 0$: $36 - 4c = 0$, also $c = 9$. Dann ist $x^2 + 6x + 9 = (x + 3)^2$.",
       tipps=["Genau eine Lösung: Was gilt dann für die Diskriminante?",
              "$D = 6^2 - 4 \\cdot 1 \\cdot c = 36 - 4c$ muss $0$ sein.",
              "$36 - 4c = 0$ nach $c$ auflösen."],
       rechenweg=r"""
       :::rechnung
       6^2 - 4 \cdot 1 \cdot c = 0 || genau eine Lösung: $D = 0$
       36 - 4c = 0 || ausrechnen
       4c = 36 || $+4c$
       c = 9 || durch $4$
       :::
       """,
       typische_fehler=[(3, "Das ist $\\frac{p}{2}$. Gesucht ist $c$ mit $\\left(\\frac{p}{2}\\right)^2 - c = 0$, also $c = 3^2$."),
                        (36, "Du hast $D = 36 - c$ gerechnet. In $b^2 - 4ac$ wird $c$ mit $4$ malgenommen.")])

k.zahl(r"""
    ## Ausblick Mathe 1: Eigenwerte

    In Mathe 1 berechnest du Eigenwerte einer Matrix als Lösungen einer quadratischen
    Gleichung. Für eine Matrix entsteht zum Beispiel
    $$\lambda^2 - 5\lambda + 4 = 0$$
    ($\lambda$ ist der griechische Buchstabe Lambda und steht hier einfach für $x$).
    Gib den **größeren** der beiden Eigenwerte an.
    """, 4,
       "Vieta: Produkt $4$ und Summe $5$ ergibt $1$ und $4$. Der größere Eigenwert ist $4$.",
       tipps=["Lies $p = -5$ und $q = 4$ ab, als stünde dort $x$.",
              "Vieta: zwei Zahlen mit Produkt $4$ und Summe $5$.",
              "$1 \\cdot 4 = 4$ und $1 + 4 = 5$."],
       rechenweg=r"""
       :::rechnung
       -\frac{-5}{2} = \frac{5}{2} || $-\frac{p}{2}$ mit $p = -5$
       \left(\frac{-5}{2}\right)^2 - 4 = \frac{25}{4} - \frac{16}{4} = \frac{9}{4} || unter der Wurzel
       \sqrt{\frac{9}{4}} = \frac{3}{2} || Wurzel ziehen
       \frac{5}{2} + \frac{3}{2} = 4 || größere Lösung
       \frac{5}{2} - \frac{3}{2} = 1 || kleinere Lösung
       :::
       """,
       typische_fehler=[(1, "Das ist der **kleinere** Eigenwert. Gefragt ist der größere."),
                        (-1, "Vorzeichen: Vorne steht $-\\frac{p}{2} = +\\frac{5}{2}$.")])

# Übungsblatt-Stil: erst umformen, dann pq-Formel, irrationale Lösungen
k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: erst umformen, dann lösen

    Bestimmen Sie alle $x \in \mathbb{R}$ mit
    $$(x - 1)^2 = 2x + 7.$$
    Geben Sie alle Zwischenergebnisse an.
    """,
    [{"typ": "term", "frage": "Bringe alles auf die linke Seite und multipliziere aus. "
                              "Gib die linke Seite von $\\ldots = 0$ an.",
      "loesung": "x^2 - 4x - 6", "variablen": "x", "form": "ausmultipliziert",
      "tipps": ["$(x - 1)^2 = x^2 - 2x + 1$ (binomische Formel).", "Dann $2x + 7$ auf beiden Seiten abziehen."],
      "rechenweg": "$(x - 1)^2 - 2x - 7 = x^2 - 2x + 1 - 2x - 7 = x^2 - 4x - 6$",
      "typische_fehler": [("x^2 - 4x + 8", "Beim Rüberbringen dreht sich das Vorzeichen: $1 - 7 = -6$, nicht $1 + 7$."),
                          ("x^2 - 2x - 6", "Auch $2x$ muss abgezogen werden: $-2x - 2x = -4x$.")]},
     {"typ": "zahl", "frage": "Mit $p = -4$ und $q = -6$: Berechne den Wert unter der Wurzel, "
                              "$\\left(\\frac{p}{2}\\right)^2 - q$.",
      "loesung": F(-4, 2) ** 2 - (-6),
      "tipps": ["$\\frac{p}{2} = -2$, also $\\left(\\frac{p}{2}\\right)^2 = 4$.", "$4 - (-6)$"],
      "rechenweg": "$\\left(\\frac{-4}{2}\\right)^2 - (-6) = 4 + 6 = 10$",
      "typische_fehler": [(-2, "Minus minus wird plus: $4 - (-6) = 4 + 6$.")]},
     {"typ": "loesungsmenge", "frage": "Gib die Lösungsmenge an. (Wurzeln schreibst du als sqrt(10).)",
      "loesung": "{2 - sqrt(10); 2 + sqrt(10)}",
      "tipps": ["$-\\frac{p}{2} = 2$.", "$x = 2 \\pm \\sqrt{10}$"],
      "rechenweg": "$x_{1,2} = 2 \\pm \\sqrt{10}$",
      "typische_fehler": [("{-2 - sqrt(10); -2 + sqrt(10)}", "Vorne steht $-\\frac{p}{2}$: Bei $p = -4$ ist das $+2$."),
                          ("{2 + sqrt(10)}", "Es fehlt die Lösung mit Minus.")]}],
    "Erst ausmultiplizieren und alles auf eine Seite bringen, dann die pq-Formel. "
    "Die Wurzel $\\sqrt{10}$ bleibt stehen: Das ist das exakte Ergebnis.",
    uebungsblatt=True,
    tipps=["Ziel: eine Gleichung der Form $x^2 + px + q = 0$.", "Danach die pq-Formel."],
    rechenweg=r"""
    :::rechnung
    (x - 1)^2 = 2x + 7 || Aufgabe
    x^2 - 2x + 1 = 2x + 7 || binomische Formel
    x^2 - 4x - 6 = 0 || $-2x - 7$ auf beiden Seiten
    -\frac{-4}{2} = 2 || $p = -4$, $q = -6$: $-\frac{p}{2}$
    \left(\frac{-4}{2}\right)^2 - (-6) = 4 + 6 = 10 || unter der Wurzel
    x_1 = 2 + \sqrt{10} || mit Plus
    x_2 = 2 - \sqrt{10} || mit Minus
    :::

    Also $\mathbb{L} = \{2 - \sqrt{10},\ 2 + \sqrt{10}\}$.
    """)

k.papier(r"""
    ## Beweisen wie in der Übung: die pq-Formel herleiten

    Zeigen Sie mit quadratischer Ergänzung: Ist $\left(\frac{p}{2}\right)^2 - q \ge 0$,
    so hat $x^2 + px + q = 0$ die Lösungen
    $$x_{1,2} = -\frac{p}{2} \pm \sqrt{\left(\frac{p}{2}\right)^2 - q}.$$
    Begründen Sie jeden Schritt.
    """,
    r"""
    **Schritt 1 (ergänzen):** Addiere und subtrahiere $\left(\frac{p}{2}\right)^2$:
    $$x^2 + px + \left(\frac{p}{2}\right)^2 - \left(\frac{p}{2}\right)^2 + q = 0$$

    **Schritt 2 (binomische Formel):** Die ersten drei Summanden sind
    $\left(x + \frac{p}{2}\right)^2$. Also
    $$\left(x + \frac{p}{2}\right)^2 = \left(\frac{p}{2}\right)^2 - q$$

    **Schritt 3 (Wurzel ziehen):** Die rechte Seite ist nach Voraussetzung $\ge 0$.
    Aus $y^2 = d$ mit $d \ge 0$ folgt $y = \sqrt{d}$ oder $y = -\sqrt{d}$. Also
    $$x + \frac{p}{2} = \pm \sqrt{\left(\frac{p}{2}\right)^2 - q}$$

    **Schritt 4:** $-\frac{p}{2}$ auf beiden Seiten ergibt die Formel. Jeder Schritt
    war eine Äquivalenzumformung, also sind das genau alle Lösungen.
    """,
    ["Ich habe $\\left(\\frac{p}{2}\\right)^2$ addiert und wieder abgezogen",
     "Ich habe $x^2 + px + \\left(\\frac{p}{2}\\right)^2$ als $\\left(x + \\frac{p}{2}\\right)^2$ erkannt",
     "Ich habe beim Wurzelziehen beide Vorzeichen berücksichtigt",
     "Ich habe die Voraussetzung $\\left(\\frac{p}{2}\\right)^2 - q \\ge 0$ beim Wurzelziehen benutzt"],
    "Die pq-Formel ist nichts anderes als die quadratische Ergänzung, einmal allgemein durchgerechnet.",
    tipps=["Orientiere dich an der Rechnung für $x^2 + 6x + 5 = 0$ und ersetze $6$ durch $p$ und $5$ durch $q$."])

k.zusammenfassung(r"""
    ## Quadratische Gleichungen

    | Fall | Weg | Beispiel |
    |---|---|---|
    | nur $x^2$ und Zahl | umstellen, Wurzel, **beide** Vorzeichen | $x^2 = 49$: $x = \pm 7$ |
    | keine Zahl ohne $x$ | $x$ ausklammern, Nullprodukt | $x(x - 5) = 0$: $x = 0$ oder $5$ |
    | Normalform | pq-Formel | $x_{1,2} = -\frac{p}{2} \pm \sqrt{\left(\frac{p}{2}\right)^2 - q}$ |
    | allgemein | Mitternachtsformel | $x_{1,2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$ |

    !! Diskriminante $D = b^2 - 4ac$: $D > 0$ zwei, $D = 0$ eine, $D < 0$ keine Lösung.

    - Normalform: alles durch $a$ teilen, **jeden** Summanden.
    - $p$ und $q$ immer mit Vorzeichen ablesen.
    - Vieta: $x_1 + x_2 = -p$, $x_1 \cdot x_2 = q$, also $x^2 + px + q = (x - x_1)(x - x_2)$.
    - Nie durch $x$ teilen: Die Lösung $0$ ginge verloren.
""")
