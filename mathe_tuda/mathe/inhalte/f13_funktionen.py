# -*- coding: utf-8 -*-
"""Fundament 13: Funktionen und Graphen – Funktionsbegriff, lineare Funktionen, Parabeln, Verschieben."""
from fractions import Fraction as F

from .. import mathlib, pruefer
from ..engine import neues_kapitel, ohne_gleiche

tex = mathlib.tex
tk = mathlib.tex_klammer
vz = mathlib.vorzeichen_tex      # F(-3) -> "- 3", F(2) -> "+ 2"

k = neues_kapitel(
    slug="funktionen",
    titel="Funktionen und Graphen",
    beschreibung="Was eine Funktion ist, Wertetabelle und Graph, Geraden, Parabeln, Verschieben und Strecken",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="📈")

k.lernziele([
    "Ich kann die Schreibweise $f\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto 2x + 1$ lesen und Funktionswerte ausrechnen",
    "Ich kann eine Wertetabelle anlegen und den Graphen einer Funktion zeichnen",
    "Ich kann Steigung und $y$-Achsenabschnitt einer Geraden bestimmen, auch aus zwei Punkten",
    "Ich kann aus $f(x) = a(x - d)^2 + e$ den Scheitelpunkt ablesen und sagen, wie die Parabel verschoben ist",
])

k.warum(r"""
Eine Funktion in Python, `def f(x): return 2*x + 1`, ist genau das, was dieses Kapitel
beschreibt: Eingabe hinein, **genau ein** Ergebnis heraus. In Mathe 1 heißen Funktionen
[[Abbildungen|Funktion]], und fast jeder Satz handelt von ihnen. Laufzeiten von Algorithmen
sind Funktionen der Eingabegröße $n$. In der Computergrafik verschiebst und streckst du
Figuren mit denselben Regeln, die du hier an Parabeln lernst.
""")

# ── 1: Was ist eine Funktion ───────────────────────────────────────────────
k.erklaerung("Was ist eine Funktion?", r"""
    ## Eine Regel, genau ein Ergebnis

    :::analogie 🥤 Getränkeautomat
    Du drückst eine Taste und bekommst genau ein Getränk. Drückst du dieselbe Taste
    noch einmal, kommt wieder dasselbe Getränk.
    :::

    Eine [[Funktion]] ordnet jeder erlaubten Zahl $x$ **genau eine** Zahl $f(x)$ zu.
    An der TU schreibt man das so:

    $$f\colon \mathbb{R} \to \mathbb{R},\quad x \mapsto 2x + 1$$

    Gelesen: „$f$ geht von $\mathbb{R}$ nach $\mathbb{R}$, $x$ wird auf $2x + 1$
    abgebildet.“ Kurz: $f(x) = 2x + 1$. Die Zahl $f(x)$ heißt [[Funktionswert]]
    an der Stelle $x$.

    :::rechnung Beispiel vorgerechnet: $f(3)$
    2 \cdot 3 + 1 || für $x$ die Zahl $3$ einsetzen
    = 6 + 1 || Punkt vor Strich
    = 7 || also ist $f(3) = 7$
    :::

    :::alt Mit Python erklärt
    `def f(x): return 2*x + 1` ist ein kleines Programm. Rufst du `f(3)` auf,
    rechnet es `2*3 + 1` und gibt `7` zurück. Jeder Aufruf mit `3` liefert wieder
    `7`. Mehr verlangt die Mathematik von einer Funktion nicht: zu jeder Eingabe
    genau eine Ausgabe.
    :::
    ---
    ## Wertetabelle und Graph

    Setzt du mehrere Zahlen ein, entsteht eine [[Wertetabelle]]. Jedes Paar wird ein
    Punkt $(x \mid f(x))$ im Koordinatensystem. Der [[Graph]] von $f$ besteht aus
    **allen** Punkten $(x \mid f(x))$ mit $x \in D$, nicht nur aus denen der Tabelle.
    Die Tabelle liefert nur einige davon.

    :::rechnung Wertetabelle für $f(x) = 2x + 1$
    2 \cdot (-1) + 1 = -1 || $f(-1) = -1$, Punkt $(-1 \mid -1)$
    2 \cdot 0 + 1 = 1 || $f(0) = 1$, Punkt $(0 \mid 1)$
    2 \cdot 1 + 1 = 3 || $f(1) = 3$, Punkt $(1 \mid 3)$
    :::

    :::visual funktionsgraph
    {"funktionen": [{"term": "2x + 1", "label": "f(x)"}], "wertetabelle": [-2, -1, 0, 1, 2],
     "punkte": [{"x": 1, "y": 3}], "x": [-4, 4], "y": [-4, 6],
     "unterschrift": "Der Punkt $(1 \\mid 3)$ liegt auf dem Graphen, weil $f(1) = 3$ ist."}
    :::

    !! Erst $x$ nach rechts, dann $f(x)$ nach oben.

    :::alt Wie eine Schatzkarte
    Ein Punkt $(1 \mid 3)$ ist eine Wegbeschreibung: Starte beim Ursprung, geh $1$
    Schritt nach rechts und $3$ Schritte nach oben. Der Graph ist die Spur aller
    Schätze, die die Funktion versteckt hat: für jedes $x$ genau einer.
    :::
    """)

k.zahl("Gegeben ist $f(x) = x^2 - 3x$. Berechne $f(-2)$.", 10,
       "Setze $-2$ mit Klammern ein: $(-2)^2 - 3 \\cdot (-2) = 4 + 6 = 10$.",
       tipps=["Ersetze jedes $x$ durch $(-2)$, mit Klammern.",
              "$(-2)^2 = 4$ und $-3 \\cdot (-2) = +6$.",
              "$4 + 6$"],
       rechenweg=r"""
       :::rechnung
       (-2)^2 - 3 \cdot (-2) || für $x$ die Zahl $-2$ in Klammern einsetzen
       = 4 + 6 || minus mal minus ergibt plus
       = 10 || addieren
       :::
       """,
       typische_fehler=[(2, "Du hast $-2^2 = -4$ gerechnet. Die Klammer fehlt: $(-2)^2 = 4$."),
                        (-2, "Vorzeichenfehler: $-3 \\cdot (-2) = +6$, nicht $-6$.")])

k.mc("Welche Zuordnung ist **keine** Funktion?",
     ["Jeder Zahl $x \\ge 0$ werden alle Zahlen $y$ mit $y^2 = x$ zugeordnet",
      "$x \\mapsto x^2$",
      "$x \\mapsto 5$",
      "$x \\mapsto -x$"],
     "Bei $y^2 = x$ bekommt zum Beispiel $x = 4$ zwei Werte: $y = 2$ und $y = -2$. Eine Funktion "
     "liefert aber zu jedem $x$ **genau einen** Wert.",
     tipps=["Prüfe bei jeder Zuordnung: Gibt es ein $x$, das zwei Ergebnisse bekommt?",
            "Probiere $x = 4$ bei $y^2 = x$."],
     fehler={"$x \\mapsto 5$": "Auch eine konstante Zuordnung ist eine Funktion: Jedes $x$ bekommt genau "
                              "einen Wert, nur eben immer denselben.",
             "$x \\mapsto x^2$": "$x \\mapsto x^2$ ist eine Funktion. Zwar haben $2$ und $-2$ denselben Wert $4$, "
                                "aber jedes $x$ bekommt nur **einen** Wert. Verboten ist nur ein $x$ mit zwei Werten."})

k.graph_punkt("Setze den Punkt des Graphen von $f(x) = 2x + 1$ an der Stelle $x = 1{,}5$.",
              {"funktionen": [{"term": "2x + 1", "label": "f(x)"}], "x": [-4, 4], "y": [-4, 6]},
              modus="setzen", ziel=(F(3, 2), 4),
              erklaerung="$f(1{,}5) = 2 \\cdot 1{,}5 + 1 = 4$. Der Punkt ist $(1{,}5 \\mid 4)$.",
              tipps=["Rechne zuerst $f(1{,}5)$ aus.", "$2 \\cdot 1{,}5 = 3$, dann noch $+1$.",
                     "Geh $1{,}5$ nach rechts und $4$ nach oben."],
              rechenweg=r"""
              :::rechnung
              2 \cdot 1{,}5 + 1 = 3 + 1 || $x = 1{,}5$ einsetzen
              = 4 || also Punkt $(1{,}5 \mid 4)$
              :::
              """,
              typische_fehler=[((F(3, 2), 3), "Du hast das $+1$ vergessen: $2 \\cdot 1{,}5 + 1 = 4$.")])

# ── 2: Definitionsmenge ────────────────────────────────────────────────────
k.erklaerung("Welche Zahlen sind erlaubt?", r"""
    ## Die Definitionsmenge

    :::analogie 🪙 Münzautomat
    Ein Parkautomat nimmt Münzen, aber keine Knöpfe. Für Knöpfe ist er nicht gebaut.
    :::

    Nicht jede Zahl darf in jede Funktion. Bei $f(x) = \frac{1}{x - 2}$ wäre für
    $x = 2$ der Nenner $0$, und durch $0$ teilt man nicht. Die [[Definitionsmenge]]
    $D$ enthält alle erlaubten Zahlen. In $f\colon D \to W$ steht $D$ links, rechts die
    [[Zielmenge]] $W$, in der die Ergebnisse liegen dürfen. Nicht jedes Element von $W$
    muss getroffen werden: $f\colon \mathbb{R} \to \mathbb{R},\ x \mapsto x^2$ erreicht $-1$ nie.
    In der Schule sucht man die größtmögliche Definitionsmenge, an der Uni gehört $D$
    zur Angabe der Funktion.

    :::rechnung Wann wird der Nenner null?
    x - 2 = 0 || verbotene Stelle suchen
    x = 2 || diese Zahl muss raus
    :::

    $$D = \mathbb{R} \setminus \{2\}$$

    Gelesen: „$\mathbb{R}$ ohne die $2$“. Bei $\sqrt{x}$ sind nur $x \ge 0$ erlaubt.

    :::achtung Verkehrt herum
    Die $2$ ist die **verbotene** Zahl. $D = \{2\}$ wäre genau falsch:
    Das hieße, **nur** die $2$ ist erlaubt.
    :::

    :::alt Mit einem Sieb erklärt
    Schütte alle reellen Zahlen in ein Sieb. Jede Zahl, mit der die Rechnung
    unmöglich wird, bleibt hängen: hier nur die $2$. Was durchfällt, ist die
    Definitionsmenge.
    :::
    """)

k.loesungsmenge("Gib die Definitionsmenge von $f(x) = \\frac{3}{x + 4}$ an. "
                "Schreibweise zum Eintippen: `R \\ {5}` für „$\\mathbb{R}$ ohne $5$“.",
                "R \\ {-4}",
                "Der Nenner $x + 4$ wird für $x = -4$ null. Alle anderen Zahlen sind erlaubt: $D = \\mathbb{R} \\setminus \\{-4\\}$.",
                tipps=["Wann wird der Nenner $0$?", "Löse $x + 4 = 0$.",
                       "$x = -4$ ist verboten, alles andere erlaubt."],
                rechenweg=r"""
                :::rechnung
                x + 4 = 0 || Nenner null setzen
                x = -4 || verbotene Stelle
                :::

                $D = \mathbb{R} \setminus \{-4\}$
                """,
                typische_fehler=[("{-4}", "Das ist die **verbotene** Zahl. Gesucht sind alle erlaubten: $\\mathbb{R}$ ohne $-4$."),
                                 ("R \\ {4}", "Vorzeichen: $x + 4 = 0$ gilt für $x = -4$, nicht für $4$.")])

# ── 3: Lineare Funktionen ──────────────────────────────────────────────────
k.erklaerung("Geraden: lineare Funktionen", r"""
    ## Steigung und y-Achsenabschnitt

    :::analogie 🚕 Taxi
    Ein Taxi kostet $4$ € Grundgebühr und $2$ € pro Kilometer. Für $x$ Kilometer
    zahlst du $f(x) = 2x + 4$ Euro.
    :::

    Eine [[lineare Funktion]] hat die Form $f(x) = mx + b$. Ihr Graph ist eine Gerade.

    - $b$ ist der [[y-Achsenabschnitt]]: Die Gerade schneidet die $y$-Achse im Punkt $(0 \mid b)$.
    - $m$ ist die [[Steigung]]: Gehst du $1$ nach rechts, geht die Gerade $m$ nach oben.
      Ist $m$ negativ, geht sie nach unten.

    :::rechnung Taxi für $5$ km
    2 \cdot 5 + 4 || $x = 5$ einsetzen
    = 10 + 4 = 14 || also kosten $5$ km $14$ €
    :::

    :::visual funktionsgraph
    {"funktionen": [{"term": "m*x + b", "label": "f(x)"}],
     "parameter": [{"name": "m", "wert": 2, "von": -3, "bis": 3, "schritt": 0.5},
                   {"name": "b", "wert": 1, "von": -4, "bis": 4, "schritt": 0.5}],
     "x": [-5, 5], "y": [-5, 5],
     "unterschrift": "Schiebe $m$: Die Gerade kippt. Schiebe $b$: Sie rutscht nach oben oder unten."}
    :::

    :::alt Mit einer Treppe erklärt
    Stell dir die Gerade als Treppe vor. Jede Stufe ist $1$ breit und $m$ hoch.
    Bei $m = 2$ steigst du mit jedem Schritt nach rechts $2$ nach oben. Wo die
    Treppe die $y$-Achse trifft, steht sie auf der Höhe $b$.
    :::
    ---
    ## Die Gerade durch zwei Punkte

    Durch zwei Punkte geht genau eine Gerade. Ihre Steigung ist der Höhenunterschied
    geteilt durch den Unterschied nach rechts:

    $$m = \frac{y_2 - y_1}{x_2 - x_1}$$

    :::rechnung Gerade durch $(1 \mid 3)$ und $(4 \mid 9)$
    \frac{9 - 3}{4 - 1} = \frac{6}{3} = 2 || Steigung $m = 2$
    3 = 2 \cdot 1 + b || Punkt $(1 \mid 3)$ in $y = 2x + b$ einsetzen
    3 = 2 + b || ausrechnen
    b = 1 || auf beiden Seiten $2$ abziehen
    :::

    Also ist $f(x) = 2x + 1$.

    :::achtung Oben y, unten x
    Im Zähler stehen die $y$-Werte, im Nenner die $x$-Werte, beide in **derselben**
    Reihenfolge. $\frac{4 - 1}{9 - 3}$ wäre der Kehrwert der Steigung.
    :::

    :::alt Mit dem Steigungsdreieck erklärt
    Geh von $(1 \mid 3)$ zu $(4 \mid 9)$: $3$ Schritte nach rechts und $6$ nach
    oben. Auf jeden Schritt nach rechts kommen also $6 : 3 = 2$ nach oben. Das ist
    die Steigung.
    :::
    """)

k.zahl("Welche Steigung hat die Gerade durch $(2 \\mid 1)$ und $(4 \\mid 7)$?", 3,
       "$m = \\frac{7 - 1}{4 - 2} = \\frac{6}{2} = 3$.",
       tipps=["Steigung = Höhenunterschied geteilt durch Unterschied nach rechts.",
              "Oben $7 - 1$, unten $4 - 2$.", "$\\frac{6}{2}$"],
       rechenweg=r"""
       :::rechnung
       \frac{7 - 1}{4 - 2} = \frac{6}{2} || $y$-Werte oben, $x$-Werte unten
       = 3 || kürzen
       :::
       """,
       typische_fehler=[(F(1, 3), "Das ist der Kehrwert. Die $y$-Werte gehören in den Zähler."),
                        (-3, "Du hast oben und unten verschieden herum abgezogen. Nimm beide Male zuerst den zweiten Punkt.")])

k.term("Gib die Funktionsgleichung der Geraden durch $(0 \\mid -2)$ und $(2 \\mid 4)$ an: $f(x) = \\ldots$",
       "3x - 2",
       "Der Punkt $(0 \\mid -2)$ liegt auf der $y$-Achse, also $b = -2$. Steigung $\\frac{4 - (-2)}{2 - 0} = 3$. "
       "Zusammen: $f(x) = 3x - 2$.",
       variablen="x",
       tipps=["Ein Punkt hat $x = 0$. Was verrät er?", "$b = -2$. Jetzt die Steigung: $\\frac{4 - (-2)}{2 - 0}$.",
              "$m = 3$ und $b = -2$."],
       rechenweg=r"""
       :::rechnung
       \frac{4 - (-2)}{2 - 0} = \frac{6}{2} = 3 || Steigung $m$
       :::

       Der Punkt $(0 \mid -2)$ liegt auf der $y$-Achse, also ist $b = -2$ und $f(x) = 3x - 2$.
       """,
       typische_fehler=[("3x + 2", "Der $y$-Achsenabschnitt ist $-2$: Der Punkt $(0 \\mid -2)$ liegt **unter** der $x$-Achse."),
                        ("1/3 x - 2", "Die Steigung ist der Kehrwert: $y$-Unterschied oben, $x$-Unterschied unten."),
                        ("x - 2", "Die Steigung ist nicht $\\frac{4 - 2}{2}$. Rechne $\\frac{4 - (-2)}{2 - 0}$.")])

k.wf("Der Graph von $f(x) = -2x + 5$ fällt von links nach rechts.", True,
     "Die Steigung $m = -2$ ist negativ: Mit jedem Schritt nach rechts geht es $2$ nach unten.",
     tipps=["Schau nur auf die Zahl vor dem $x$."])

# ── 4: Parabeln ────────────────────────────────────────────────────────────
k.erklaerung("Parabeln", r"""
    ## Die Normalparabel

    :::analogie ⛲ Wasserstrahl
    Ein Wasserstrahl aus einem Brunnen steigt, kehrt um und fällt wieder. Diese
    Bogenform heißt Parabel.
    :::

    Die einfachste [[Parabel]] ist der Graph von $f(x) = x^2$, die [[Normalparabel]].
    Sie ist symmetrisch zur $y$-Achse, weil $x$ und $-x$ denselben Wert haben. Ihr
    tiefster Punkt ist der [[Scheitelpunkt]] $S(0 \mid 0)$.

    :::rechnung Symmetrie an zwei Stellen
    (-2)^2 = 4 || $f(-2) = 4$
    2^2 = 4 || $f(2) = 4$: gleicher Wert, gespiegelt an der $y$-Achse
    :::

    :::visual funktionsgraph
    {"funktionen": [{"term": "x^2", "label": "f(x)"}], "wertetabelle": [-2, -1, 0, 1, 2],
     "scheitel": true, "x": [-4, 4], "y": [-1, 8],
     "unterschrift": "Die Wertetabelle ist links und rechts gleich: Spiegelbild an der $y$-Achse."}
    :::

    :::alt Mit Quadraten erklärt
    $x^2$ ist die Fläche eines Quadrats mit Seite $x$. Seite $1$: Fläche $1$.
    Seite $2$: Fläche $4$. Seite $3$: Fläche $9$. Die Fläche wächst immer schneller.
    Darum wird die Parabel nach außen immer steiler.
    :::
    """)

# ── 5: Verschieben und Strecken ────────────────────────────────────────────
k.erklaerung("Parabeln verschieben und strecken", r"""
    ## Nach oben und unten: $+\,e$

    :::analogie 🛗 Aufzug
    Die ganze Parabel steigt in einen Aufzug und fährt $e$ Stockwerke nach oben.
    Ihre Form bleibt gleich.
    :::

    Bei $f(x) = x^2 + e$ wird zu jedem Funktionswert $e$ addiert. Der Graph rutscht
    um $e$ nach oben, bei negativem $e$ nach unten.

    :::rechnung Scheitelpunkt von $f(x) = x^2 - 3$
    0^2 - 3 = -3 || an der Stelle $x = 0$: Scheitelpunkt $S(0 \mid -3)$
    :::

    :::visual funktionsgraph
    {"funktionen": [{"term": "x^2", "label": "x^2", "farbe": 2}, {"term": "x^2 + e", "label": "f(x)", "farbe": 1}],
     "parameter": [{"name": "e", "wert": -3, "von": -4, "bis": 4, "schritt": 0.5}],
     "x": [-4, 4], "y": [-5, 8]}
    :::

    :::alt Mit einer Tabelle erklärt
    Schreib die Wertetabelle von $x^2$ auf: $4, 1, 0, 1, 4$. Bei $x^2 - 3$ ziehst du
    von **jeder** Zahl $3$ ab: $1, -2, -3, -2, 1$. Jeder Punkt geht $3$ nach unten,
    also der ganze Graph.
    :::
    ---
    ## Nach links und rechts: $(x - d)$

    Bei $f(x) = (x - d)^2$ rutscht die Parabel um $d$ nach **rechts**. Der Scheitelpunkt
    liegt dort, wo die Klammer null wird.

    :::rechnung Scheitelpunkt von $f(x) = (x - 2)^2$
    x - 2 = 0 || die Klammer wird null
    x = 2 || also $S(2 \mid 0)$
    :::

    :::visual funktionsgraph
    {"funktionen": [{"term": "x^2", "label": "x^2", "farbe": 2}, {"term": "(x - d)^2", "label": "f(x)", "farbe": 1}],
     "parameter": [{"name": "d", "wert": 2, "von": -4, "bis": 4, "schritt": 0.5}],
     "x": [-5, 5], "y": [-1, 8]}
    :::

    :::achtung Minus heißt rechts
    $(x - 2)^2$ rückt nach **rechts**, $(x + 2)^2$ nach **links**. Wer nach dem
    Vorzeichen geht, landet auf der falschen Seite.
    :::

    :::alt Mit Verspätung erklärt
    $(x - 2)^2$ macht an der Stelle $x$, was $x^2$ an der Stelle $x - 2$ gemacht hat.
    Den Wert $0$ erreicht sie also erst bei $x = 2$, zwei Schritte später. Wer später
    dran ist, liegt weiter rechts.
    :::
    ---
    ## Strecken und spiegeln: der Faktor $a$

    Bei $f(x) = a(x - d)^2 + e$ ist $S(d \mid e)$ der Scheitelpunkt. Das ist die
    [[Scheitelpunktform]]. Der Faktor $a$ streckt:

    - $|a| > 1$: schmaler, $0 < |a| < 1$: breiter,
    - $a < 0$: nach unten offen (die Form wird umgeklappt).

    :::rechnung $f(x) = 2(x - 1)^2 - 8$ an der Stelle $x = 3$
    2 \cdot (3 - 1)^2 - 8 || Scheitelpunkt $S(1 \mid -8)$; $x = 3$ einsetzen
    = 2 \cdot 2^2 - 8 || erst die Klammer
    = 2 \cdot 4 - 8 || dann quadrieren
    = 0 || also ist $3$ eine Nullstelle: $f(3) = 0$
    :::

    :::visual funktionsgraph
    {"funktionen": [{"term": "a*(x - d)^2 + e", "label": "f(x)"}],
     "parameter": [{"name": "a", "wert": 2, "von": -3, "bis": 3, "schritt": 0.25},
                   {"name": "d", "wert": 1, "von": -4, "bis": 4, "schritt": 0.5},
                   {"name": "e", "wert": -8, "von": -8, "bis": 8, "schritt": 0.5}],
     "scheitel": true, "x": [-5, 6], "y": [-10, 10]}
    :::

    :::alt Mit einem Gummiband erklärt
    Die Parabel ist aus Gummi und am Scheitel festgenagelt. Ziehst du die Arme nach
    oben ($a = 2$), wird sie schmal. Lässt du nach ($a = \frac{1}{2}$), wird sie
    breit. Klappst du sie nach unten ($a = -1$), öffnet sie sich nach unten.
    :::
    """)

k.graph_punkt("Setze den Scheitelpunkt von $f(x) = (x + 1)^2 - 2$.",
              {"funktionen": [{"term": "(x + 1)^2 - 2", "label": "f(x)"}], "x": [-5, 5], "y": [-4, 6]},
              modus="setzen", ziel=(-1, -2),
              erklaerung="$(x + 1) = (x - (-1))$, also $d = -1$. Dazu $e = -2$. Scheitelpunkt $S(-1 \\mid -2)$.",
              tipps=["Wo wird die Klammer null?", "$x + 1 = 0$ bei $x = -1$.",
                     "Der $y$-Wert ist die Zahl hinten: $-2$."],
              rechenweg=r"""
              :::rechnung
              x + 1 = 0 || die Klammer wird null
              x = -1 || $x$-Wert des Scheitelpunkts
              :::

              Dort ist $f(-1) = 0 - 2 = -2$. Also $S(-1 \mid -2)$.
              """,
              typische_fehler=[((1, -2), "Plus in der Klammer heißt **links**: $x + 1 = 0$ bei $x = -1$."),
                               ((-1, 2), "Der $y$-Wert ist $-2$: Das $-2$ hinten schiebt nach **unten**.")])

k.mc("Wie entsteht der Graph von $g(x) = (x - 3)^2 + 1$ aus der Normalparabel?",
     ["um $3$ nach rechts und um $1$ nach oben",
      "um $3$ nach links und um $1$ nach oben",
      "um $3$ nach rechts und um $1$ nach unten",
      "um $1$ nach rechts und um $3$ nach oben"],
     "Die Klammer $(x - 3)$ wird bei $x = 3$ null: $3$ nach rechts. Das $+1$ hebt um $1$. Scheitelpunkt $S(3 \\mid 1)$.",
     tipps=["Wo wird die Klammer null?", "$x - 3 = 0$ bei $x = 3$. Und das $+1$?"],
     fehler={"um $3$ nach links und um $1$ nach oben": "Minus in der Klammer heißt **rechts**: $x - 3 = 0$ bei $x = 3$.",
             "um $1$ nach rechts und um $3$ nach oben": "Du hast die beiden Zahlen vertauscht. Die Zahl in der "
                                                        "Klammer verschiebt nach links/rechts, die hinten nach oben/unten."})

k.term("Die Normalparabel wird um $2$ nach **links** und um $5$ nach **unten** verschoben. "
       "Gib den Funktionsterm an: $f(x) = \\ldots$",
       "(x + 2)^2 - 5",
       "Nach links um $2$: $(x + 2)^2$. Nach unten um $5$: $-5$. Zusammen $f(x) = (x + 2)^2 - 5$.",
       variablen="x",
       tipps=["Links/rechts steckt in der Klammer, oben/unten hinten.",
              "Nach links heißt: Die Klammer wird bei $x = -2$ null.", "$(x + 2)^2$ und dann $-5$."],
       rechenweg=r"""
       Die Klammer muss bei $x = -2$ null werden: $(x + 2)$. Nach unten um $5$: hinten $-5$.

       $$f(x) = (x + 2)^2 - 5$$
       """,
       typische_fehler=[("(x - 2)^2 - 5", "$(x - 2)^2$ rückt nach **rechts**. Nach links gehört $(x + 2)^2$."),
                        ("(x + 2)^2 + 5", "$+5$ hebt den Graphen an. Nach unten gehört $-5$."),
                        ("(x + 5)^2 - 2", "Du hast die Zahlen vertauscht: $2$ gehört in die Klammer, $5$ nach hinten.")])

k.zahl("Berechne $f(3)$ für $f(x) = -2(x - 1)^2 + 3$.", -5,
       "$-2 \\cdot (3 - 1)^2 + 3 = -2 \\cdot 4 + 3 = -5$.",
       tipps=["Zuerst die Klammer, dann quadrieren, dann mal $-2$.",
              "$(3 - 1)^2 = 4$.", "$-2 \\cdot 4 + 3$"],
       rechenweg=r"""
       :::rechnung
       -2 \cdot (3 - 1)^2 + 3 || $x = 3$ einsetzen
       = -2 \cdot 2^2 + 3 || Klammer zuerst
       = -2 \cdot 4 + 3 || dann quadrieren
       = -5 || zum Schluss mal $-2$ und $+3$
       :::
       """,
       typische_fehler=[(19, "Du hast $-2 \\cdot 2$ zuerst gerechnet und dann quadriert. Potenz kommt vor Mal: erst $2^2 = 4$."),
                        (11, "Das Minus vor der $2$ ist verloren gegangen: $-2 \\cdot 4 = -8$.")])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


def _gerade_text(m, b):
    """Term-Text m*x + b für die Musterlösung und Fehlwerte."""
    m, b = F(m), F(b)
    if m.denominator == 1:
        vorne = "x" if m == 1 else "-x" if m == -1 else f"{m.numerator}x"
    else:
        vorne = ("-" if m < 0 else "") + f"({abs(m.numerator)}/{m.denominator})x"
    if b == 0:
        return vorne
    return vorne + (" + " if b > 0 else " - ") + mathlib.text(abs(b))


def _term_fehler(loesung, fehler):
    """Wie ohne_gleiche, aber für Terme in x: entfernt Fehlwerte, die äquivalent zur Lösung oder doppelt sind."""
    soll = pruefer.parse(loesung, ["x"]).ast
    erg, gesehen = [], []
    for w, m in fehler:
        a = pruefer.parse(w, ["x"]).ast
        if pruefer.aequivalent(a, soll, ["x"]).ok or any(pruefer.aequivalent(a, g, ["x"]).ok for g in gesehen):
            continue
        gesehen.append(a)
        erg.append((w, m))
    return erg


def gerade_durch_punkte(rng):
    m = F(rng.choice([-3, -2, -1, 1, 2, 3, F(1, 2), F(-1, 2), F(3, 2)]))
    b = F(rng.choice([z for z in range(-5, 6) if z != 0]))
    while True:
        x1 = rng.randint(-3, 3)
        dx = rng.choice([2, 4]) if m.denominator == 2 else rng.randint(1, 4)
        x2 = x1 + dx
        if x1 != 0 and x2 != 0:
            break
    y1, y2 = m * x1 + b, m * x2 + b
    loesung = _gerade_text(m, b)
    kette = f"\\frac{{{tex(y2)} - {tk(y1)}}}{{{x2} - {tk(x1)}}}"
    zwischen = f"\\frac{{{tex(y2 - y1)}}}{{{x2 - x1}}}"
    if (y2 - y1).denominator == 1 and x2 - x1 != 1 and zwischen != tex(m):
        kette += f" = {zwischen}"
    kette += f" = {tex(m)}"
    zeilen = [(kette, "Steigung: $y$-Unterschied durch $x$-Unterschied"),
              (f"{tex(y1)} = {tex(m)} \\cdot {tk(x1)} + b", f"Punkt $({x1} \\mid {tex(y1)})$ einsetzen"),
              (f"{tex(y1)} = {tex(m * x1)} + b", "ausrechnen"),
              (f"b = {tex(b)}", f"auf beiden Seiten ${tex(m * x1)}$ abziehen" if m * x1 > 0
               else f"auf beiden Seiten ${tex(-m * x1)}$ addieren")]
    fehler = [(_gerade_text(b, m) if b != m else None, "Du hast Steigung und $y$-Achsenabschnitt vertauscht: $m$ steht vor dem $x$."),
              (_gerade_text(-m, b), "Vorzeichen der Steigung: Rechne bei beiden Differenzen zuerst den zweiten Punkt."),
              (_gerade_text(1 / m, b) if abs(m) != 1 else None, "Die Steigung ist der Kehrwert: $y$-Unterschied in den Zähler."),
              (_gerade_text(m, -b), "Prüfe das Vorzeichen von $b$ mit der Probe: Setz einen Punkt ein.")]
    fehler = [(w, t) for w, t in fehler if w is not None]
    return {
        "frage": f"Gib die Funktionsgleichung der Geraden durch $P({x1} \\mid {tex(y1)})$ und "
                 f"$Q({x2} \\mid {tex(y2)})$ an: $f(x) = \\ldots$",
        "loesung": loesung, "variablen": "x",
        "tipps": ["Bestimme zuerst die Steigung $m = \\frac{y_2 - y_1}{x_2 - x_1}$.",
                  f"$m = \\frac{{{tex(y2)} - {tk(y1)}}}{{{x2} - {tk(x1)}}} = {tex(m)}$. Jetzt einen Punkt in $y = mx + b$ einsetzen.",
                  f"${tex(y1)} = {tex(m)} \\cdot {tk(x1)} + b$, also $b = {tex(b)}$."],
        "rechenweg": _zeilen(*zeilen) + f"\n\nAlso $f(x) = {mathlib.Polynom({1: m, 0: b}).tex()}$.",
        "erklaerung": "Erst die Steigung aus den beiden Punkten, dann $b$ durch Einsetzen eines Punktes.",
        "typische_fehler": _term_fehler(loesung, fehler),
    }


k.praxis()

k.generator(gerade_durch_punkte, typ="term", titel="Gerade durch zwei Punkte")


def parabel_wert(rng):
    while True:
        a = rng.choice([-3, -2, -1, 2, 3, F(1, 2)])
        d = rng.choice([z for z in range(-4, 5) if z != 0])
        e = rng.randint(-6, 6)
        x0 = rng.randint(-3, 4)
        if x0 != d and x0 - d != -(x0 + d) and abs(x0 - d) <= 4 and (a * (x0 - d) ** 2).denominator == 1:
            break
    a, d, e = F(a), F(d), F(e)
    w = a * (x0 - d) ** 2 + e
    klammer = f"(x {vz(-d)})"
    term_tex = ("" if a == 1 else "-" if a == -1 else tex(a) if a.denominator == 1 else tex(a) + " \\cdot ") \
        + klammer + "^2" + ("" if e == 0 else f" {vz(e)}")
    einsetzen = f"{tex(a)} \\cdot ({x0} {vz(-d)})^2" + ("" if e == 0 else f" {vz(e)}")
    q = (x0 - d) ** 2
    zeilen = [(einsetzen, f"$x = {x0}$ einsetzen"),
              (f"= {tex(a)} \\cdot {tk(x0 - d)}^2" + ("" if e == 0 else f" {vz(e)}"), "zuerst die Klammer"),
              (f"= {tex(a)} \\cdot {q}" + ("" if e == 0 else f" {vz(e)}"), "dann quadrieren"),
              (f"= {tex(w)}", "malnehmen" + ("" if e == 0 else " und addieren"))]
    fehler = [(a * (x0 + d) ** 2 + e, "Du hast das Vorzeichen in der Klammer umgedreht: In der Klammer steht "
                                      f"$x {vz(-d)}$, also ${x0} {vz(-d)}$."),
              ((a * (x0 - d)) ** 2 + e, "Du hast zuerst mit $a$ malgenommen und dann quadriert. Potenz vor Mal!"),
              (-a * q + e if a < 0 else None, "Das Minus vor dem Faktor ist verloren gegangen."),
              (a * (x0 - d) + e, "Du hast das Quadrieren vergessen.")]
    fehler = [(f, m) for f, m in fehler if f is not None]
    return {
        "frage": f"Gegeben ist $f(x) = {term_tex}$. Berechne $f({x0})$.",
        "loesung": w,
        "tipps": ["Setz die Zahl für $x$ ein. Reihenfolge: Klammer, Potenz, Mal, Plus.",
                  f"Die Klammer ergibt ${x0} {vz(-d)} = {tex(x0 - d)}$.",
                  f"${tk(x0 - d)}^2 = {q}$, dann mal ${tex(a)}$" + ("" if e == 0 else f" und ${vz(e)}$") + "."],
        "rechenweg": _zeilen(*zeilen),
        "erklaerung": f"Der Scheitelpunkt ist $S({tex(d)} \\mid {tex(e)})$. Beim Einsetzen gilt: Klammer, Potenz, Mal, Plus.",
        "typische_fehler": ohne_gleiche(w, fehler),
    }


k.generator(parabel_wert, typ="zahl", titel="Parabel: Funktionswert", glatt=True)


def scheitel_lesen(rng):
    d = rng.choice([z for z in range(-5, 6) if z != 0])
    e = rng.choice([z for z in range(-6, 7) if z != 0 and abs(z) != abs(d)])
    a = rng.choice([1, 1, -1, 2, 3, -2])
    welche = rng.choice(["x", "y"])
    vorne = "" if a == 1 else "-" if a == -1 else str(a)
    term_tex = f"{vorne}(x {vz(F(-d))})^2 {vz(F(e))}"
    loesung = d if welche == "x" else e
    fehler = [(-d, "Vorzeichen: Der Scheitelpunkt liegt dort, wo die Klammer null wird.") if welche == "x"
              else (-e, f"Vorzeichen: Die Zahl hinten ist ${e}$. Sie ist direkt die $y$-Koordinate, ohne Vorzeichenwechsel."),
              (e if welche == "x" else d, "Du hast $x$- und $y$-Koordinate vertauscht."),
              (a, "Der Faktor vor der Klammer streckt nur, er verschiebt nicht.")]
    return {
        "frage": f"Lies aus $f(x) = {term_tex}$ die **{welche}-Koordinate** des Scheitelpunkts ab.",
        "loesung": loesung,
        "tipps": ["Scheitelpunktform: $f(x) = a(x - d)^2 + e$ hat den Scheitel $S(d \\mid e)$.",
                  f"Die Klammer $(x {vz(F(-d))})$ wird bei $x = {d}$ null.",
                  f"$S({d} \\mid {e})$"],
        "rechenweg": _zeilen((f"x {vz(F(-d))} = 0", "die Klammer wird null"), (f"x = {d}", "$x$-Wert des Scheitels"))
                     + f"\n\nDort bleibt nur die Zahl hinten: $y = {e}$. Also $S({d} \\mid {e})$.",
        "erklaerung": "In $a(x - d)^2 + e$ ist $S(d \\mid e)$. Achte auf das Minus in der Klammer.",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


k.generator(scheitel_lesen, typ="zahl", titel="Scheitelpunkt ablesen", glatt=True)

# Übungsblatt-Stil: Parabel untersuchen
k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: Eine Parabel untersuchen

    Gegeben ist die Funktion
    $$f\colon \mathbb{R} \to \mathbb{R},\quad x \mapsto 2(x - 1)^2 - 8.$$
    Bestimmen Sie den Scheitelpunkt, den Schnittpunkt mit der $y$-Achse und alle [[Nullstellen|Nullstelle]].
    Geben Sie alle Zwischenschritte an.
    """,
    [{"typ": "zahl", "frage": "Welche $x$-Koordinate hat der Scheitelpunkt?", "loesung": 1,
      "tipps": ["Wo wird die Klammer null?", "$x - 1 = 0$"],
      "rechenweg": "Die Klammer $(x - 1)$ wird bei $x = 1$ null.",
      "typische_fehler": [(-1, "Minus in der Klammer heißt rechts: $x - 1 = 0$ bei $x = 1$.")]},
     {"typ": "zahl", "frage": "Welche $y$-Koordinate hat der Scheitelpunkt?", "loesung": -8,
      "tipps": ["Setz $x = 1$ ein.", "$2 \\cdot 0^2 - 8$"],
      "rechenweg": "$f(1) = 2 \\cdot 0^2 - 8 = -8$, also $S(1 \\mid -8)$.",
      "typische_fehler": [(8, "Das $-8$ schiebt nach **unten**.")]},
     {"typ": "zahl", "frage": "Wo schneidet der Graph die $y$-Achse? Gib $f(0)$ an.", "loesung": -6,
      "tipps": ["Auf der $y$-Achse ist $x = 0$.", "$2 \\cdot (0 - 1)^2 - 8 = 2 \\cdot 1 - 8$"],
      "rechenweg": "$f(0) = 2 \\cdot (-1)^2 - 8 = 2 - 8 = -6$",
      "typische_fehler": [(-8, "Das ist der Scheitel. Setz $x = 0$ ein: $(0 - 1)^2 = 1$."),
                          (-10, "$(-1)^2 = +1$, nicht $-1$.")]},
     {"typ": "zahl", "frage": "Berechne die **kleinere** Nullstelle.", "loesung": -1,
      "tipps": ["Setze $f(x) = 0$ und isoliere die Klammer: $(x - 1)^2 = 4$.",
                "$x - 1 = 2$ oder $x - 1 = -2$."],
      "rechenweg": "$2(x - 1)^2 = 8$, also $(x - 1)^2 = 4$, also $x - 1 = \\pm 2$. Kleinere: $x = -1$.",
      "typische_fehler": [(3, "Das ist die größere Nullstelle. Beim Wurzelziehen gibt es auch $x - 1 = -2$.")]},
     {"typ": "zahl", "frage": "Berechne die **größere** Nullstelle.", "loesung": 3,
      "tipps": ["$x - 1 = 2$", "$x = 2 + 1$"],
      "rechenweg": "$x - 1 = 2$, also $x = 3$.",
      "typische_fehler": [(1, "Du hast $x - 1 = 0$ gelöst. Gesucht ist $x - 1 = 2$.")]}],
    "Scheitelpunktform: $S(d \\mid e)$ ablesen. Nullstellen: $f(x) = 0$ setzen, Klammer isolieren, "
    "Wurzel ziehen und beide Vorzeichen beachten.",
    uebungsblatt=True,
    tipps=["Die Funktion steht schon in Scheitelpunktform.", "Für die Nullstellen: $f(x) = 0$ setzen."],
    rechenweg=r"""
    Scheitelpunkt aus $a(x - d)^2 + e$: $S(1 \mid -8)$.

    :::rechnung Schnittpunkt mit der $y$-Achse
    2 \cdot (0 - 1)^2 - 8 = 2 \cdot 1 - 8 || $x = 0$ einsetzen
    = -6 || Schnittpunkt $(0 \mid -6)$
    :::

    :::rechnung Nullstellen
    2(x - 1)^2 - 8 = 0 || Funktionswert null setzen
    2(x - 1)^2 = 8 || $+8$
    (x - 1)^2 = 4 || $:2$
    x - 1 = 2 \text{ oder } x - 1 = -2 || Wurzel ziehen: beide Vorzeichen
    x_1 = -1 || kleinere Nullstelle
    x_2 = 3 || größere Nullstelle
    :::
    """)

k.zusammenfassung(r"""
    ## Funktionen und Graphen

    - Eine Funktion $f\colon D \to W,\ x \mapsto f(x)$ ordnet jedem $x \in D$ **genau einen** Wert $f(x)$ zu.
    - $D$ ist die Definitionsmenge: alle erlaubten $x$. Bei $\frac{1}{x - 2}$ ist $D = \mathbb{R} \setminus \{2\}$.
    - Graph: alle Punkte $(x \mid f(x))$. Erst nach rechts, dann nach oben.

    | Funktion | Form | Bedeutung |
    |---|---|---|
    | linear | $f(x) = mx + b$ | Steigung $m$, schneidet die $y$-Achse bei $b$ |
    | Steigung | $m = \frac{y_2 - y_1}{x_2 - x_1}$ | $y$ oben, $x$ unten |
    | Normalparabel | $f(x) = x^2$ | Scheitel $S(0 \mid 0)$ |
    | Scheitelpunktform | $f(x) = a(x - d)^2 + e$ | Scheitel $S(d \mid e)$ |

    !! $(x - 2)^2$ rückt nach **rechts**, $(x + 2)^2$ nach **links**.

    - $|a| > 1$ schmaler, $0 < |a| < 1$ breiter, $a < 0$ nach unten offen.
""")
