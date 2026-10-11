# -*- coding: utf-8 -*-
"""Fundament 8: Gleichungen – Äquivalenzumformungen, lineare Gleichungen, Bruchgleichungen, Formeln umstellen."""
from fractions import Fraction as F

from .. import mathlib, pruefer
from ..engine import neues_kapitel

tex = mathlib.tex

k = neues_kapitel(
    slug="gleichungen",
    titel="Gleichungen und Formeln umstellen",
    beschreibung="Äquivalenzumformungen, lineare Gleichungen, Bruchgleichungen mit Definitionsmenge und Formeln umstellen",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="⚖️")

k.lernziele([
    "Ich kann eine Lösung mit der Probe prüfen",
    "Ich löse lineare Gleichungen mit Äquivalenzumformungen, auch mit $x$ auf beiden Seiten",
    "Ich erkenne Gleichungen ohne Lösung und mit unendlich vielen Lösungen",
    "Ich bestimme bei Bruchgleichungen zuerst die Definitionsmenge und sortiere Scheinlösungen aus",
    "Ich kann eine Formel nach einer beliebigen Variable umstellen",
])

k.warum(r"""
Jedes Programm stellt Formeln um. Ein Spiel kennt Weg und Geschwindigkeit und braucht die
Zeit: $t = \frac{s}{v}$. Eine Grafikkarte rechnet Bildschirmpunkte in Koordinaten zurück.
Die Bedingung „Nenner nicht $0$“ ist im Code ein echter Absturz: `ZeroDivisionError`.
In Mathe 1 löst du ganze Systeme von Gleichungen mit dem Gauß-Algorithmus. Jeder einzelne
Schritt darin ist eine Äquivalenzumformung aus diesem Kapitel.
""")


def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


# ── 1: Gleichung, Lösung, Probe ────────────────────────────────────────────
k.erklaerung("Gleichungen und Äquivalenzumformungen", r"""
    ## Was ist eine Gleichung?

    :::analogie ⚖️ Waage
    Eine [[Gleichung]] ist eine Waage im Gleichgewicht: Links und rechts liegt
    gleich viel. Auf der linken Seite steckt ein unbekanntes Gewicht $x$.
    :::

    Eine Zahl ist eine **Lösung**, wenn beim Einsetzen links und rechts dasselbe
    herauskommt. Das Einsetzen heißt [[Probe]]. Alle Lösungen zusammen bilden die
    [[Lösungsmenge]] $\mathbb{L}$.

    :::rechnung Probe: Ist $x = 5$ eine Lösung von $3x + 5 = 20$?
    3 \cdot 5 + 5 = 15 + 5 || $5$ für $x$ einsetzen, Punkt vor Strich
    = 20 || links kommt $20$ heraus, rechts steht $20$: Lösung!
    :::

    :::alt Mit einem Zahlenrätsel erklärt
    „Ich denke mir eine Zahl. Ich nehme sie mal $3$ und addiere $5$. Heraus kommt
    $20$. Welche Zahl war es?“ Genau das ist die Gleichung $3x + 5 = 20$. Du kannst
    raten und prüfen: Bei $4$ kommt $17$ heraus, bei $5$ genau $20$.
    :::
    ---
    ## Auf beiden Seiten dasselbe tun

    Raten ist mühsam. Besser: Du formst die Gleichung um, bis $x$ allein steht.
    Erlaubt ist alles, was du **auf beiden Seiten gleich** machst: dieselbe Zahl
    addieren oder abziehen, mit derselben Zahl ungleich $0$ malnehmen oder teilen.
    Solche Schritte heißen [[Äquivalenzumformungen|Äquivalenzumformung]]. Sie ändern die
    Lösungsmenge nicht.

    :::visual rechnung
    {"links": "3x + 5", "rechts": "20",
     "schritte": [{"op": "-5", "text": "Auf beiden Seiten 5 wegnehmen."},
                  {"op": ":3", "text": "Beide Seiten durch 3 teilen."}],
     "unterschrift": "Was du links tust, tust du auch rechts. Die Waage bleibt im Gleichgewicht."}
    :::

    :::rechnung Beispiel vorgerechnet
    3x + 5 = 20 \quad | -5 || die $+5$ stört: auf beiden Seiten $5$ abziehen
    3x = 15 \quad | :3 || das $\cdot 3$ stört: beide Seiten durch $3$
    x = 5 || $x$ steht allein
    :::

    :::achtung Nur eine Seite verändert
    Aus $3x + 5 = 20$ wird nicht $3x = 20$. Wer links $5$ wegnimmt, muss auch rechts
    $5$ wegnehmen. Und malnehmen mit $0$ ist verboten: Aus jeder Gleichung würde $0 = 0$.
    :::

    :::alt Mit Rückwärtsgehen erklärt
    Morgens ziehst du erst Socken an, dann Schuhe. Abends geht es rückwärts: erst
    Schuhe aus, dann Socken. Mit $x$ ist zuerst „mal $3$“ passiert, dann „plus $5$“.
    Zum Lösen machst du es rückwärts: erst $-5$, dann $:3$.
    :::
    """)

k.wf("$x = 4$ ist eine Lösung von $3x - 2 = 10$.", True,
     "Probe: $3 \\cdot 4 - 2 = 12 - 2 = 10$. Links kommt dasselbe heraus wie rechts.",
     tipps=["Setze $4$ für $x$ ein und rechne die linke Seite aus."])

k.gleichung("3x + 5 = 20", loesung="{5}",
            erklaerung="Erst $-5$ auf beiden Seiten, dann $:3$. Probe: $3 \\cdot 5 + 5 = 20$.",
            tipps=["Was stört, damit $x$ allein steht? Zuerst die $+5$.",
                   "Nach $-5$ auf beiden Seiten: $3x = 15$.", "Jetzt beide Seiten durch $3$."],
            rechenweg=r"""
            :::rechnung
            3x + 5 = 20 \quad | -5 || $5$ auf beiden Seiten abziehen
            3x = 15 \quad | :3 || durch $3$ teilen
            x = 5 || Probe: $3 \cdot 5 + 5 = 20$
            :::
            """,
            typische_fehler=[("{25/3}", "Du hast $5$ addiert statt abgezogen. Die $+5$ verschwindet mit $-5$."),
                             ("{45}", "Du hast mit $3$ malgenommen. Das $\\cdot 3$ wird durch $:3$ rückgängig gemacht."),
                             ("{20/3}", "Die $5$ muss zuerst weg: Nimm auf **beiden** Seiten $5$ weg.")])

# ── 2: x auf beiden Seiten, Sonderfälle ────────────────────────────────────
k.erklaerung("x auf beiden Seiten und Sonderfälle", r"""
    ## Erst sortieren, dann teilen

    :::analogie 🧺 Wäsche sortieren
    Alle Socken in einen Korb, alle Hemden in den anderen. Bei Gleichungen sammelst
    du alle $x$-Terme auf einer Seite und alle Zahlen auf der anderen.
    :::

    Stehen Klammern da, löst du sie zuerst auf.

    :::rechnung Beispiel vorgerechnet
    5x - 3 = 2x + 9 \quad | -2x || $x$-Terme nach links
    3x - 3 = 9 \quad | +3 || Zahlen nach rechts
    3x = 12 \quad | :3 || durch die Zahl vor $x$ teilen
    x = 4 || Probe: links $17$, rechts $17$
    :::

    :::achtung Vorzeichen beim Herüberholen
    Aus $5x - 3 = 2x + 9$ wird **nicht** $7x = 12$. Die $2x$ verschwindet rechts nur
    mit $-2x$, und das gilt dann auch links.
    :::

    :::alt Mit einer Waage erklärt
    Auf der linken Schale liegen $5$ Kästchen, auf der rechten $2$ Kästchen und Gewichte.
    Nimm von beiden Schalen $2$ Kästchen weg: Die Waage bleibt im Gleichgewicht, aber
    rechts liegt kein Kästchen mehr. Genau das macht $| -2x$.
    :::
    ---
    ## Keine Lösung oder unendlich viele

    Manchmal verschwindet $x$ ganz. Dann entscheidet, was übrig bleibt:

    - Eine falsche Aussage wie $1 = 5$: Keine Zahl passt, $\mathbb{L} = \emptyset$ (leere Menge).
    - Eine wahre Aussage wie $2 = 2$: Jede Zahl passt, $\mathbb{L} = \mathbb{R}$.

    :::visual rechnung
    {"links": "2x + 1", "rechts": "2x + 5",
     "schritte": [{"op": "-2x", "text": "Auf beiden Seiten 2x wegnehmen: Übrig bleibt 1 = 5. Das stimmt nie."}],
     "unterschrift": "Keine Lösung: $\\mathbb{L} = \\emptyset$."}
    :::

    :::rechnung Unendlich viele Lösungen
    2(x + 1) = 2x + 2 || Klammer auflösen
    2x + 2 = 2x + 2 || beide Seiten sind gleich
    2 = 2 || nach $-2x$: wahr für jedes $x$, also $\mathbb{L} = \mathbb{R}$
    :::

    :::alt Mit Rätseln erklärt
    „Eine Zahl plus $1$ ist dieselbe Zahl plus $5$.“ Das klappt nie, egal welche
    Zahl. „Das Doppelte von Zahl plus $1$ ist das Doppelte der Zahl plus $2$.“ Das
    klappt immer. Beides sind echte Gleichungen, nur mit ungewöhnlicher Lösungsmenge.
    :::
    """)

k.gleichung("5x - 3 = 2x + 9", loesung="{4}",
            erklaerung="$-2x$, dann $+3$, dann $:3$: $x = 4$. Probe: $5 \\cdot 4 - 3 = 17 = 2 \\cdot 4 + 9$.",
            tipps=["Bring alle $x$-Terme auf eine Seite.", "Nach $-2x$: $3x - 3 = 9$.",
                   "Dann $+3$ und durch $3$ teilen."],
            rechenweg=r"""
            :::rechnung
            5x - 3 = 2x + 9 \quad | -2x || $x$-Terme nach links
            3x - 3 = 9 \quad | +3 || Zahlen nach rechts
            3x = 12 \quad | :3 || teilen
            x = 4 || Probe: $17 = 17$
            :::
            """,
            typische_fehler=[("{12/7}", "Du hast $2x$ addiert statt abgezogen. Die $+2x$ verschwindet rechts nur mit $-2x$."),
                             ("{2}", "Vorzeichenfehler bei der $-3$: Sie verschwindet mit $+3$, also $3x = 9 + 3 = 12$.")])

k.gleichung("2(x - 3) = x + 1", loesung="{7}",
            erklaerung="Klammer auflösen: $2x - 6 = x + 1$. Dann $-x$ und $+6$: $x = 7$.",
            tipps=["Löse zuerst die Klammer auf.", "$2(x - 3) = 2x - 6$.",
                   "$2x - 6 = x + 1$. Jetzt $-x$ und $+6$."],
            rechenweg=r"""
            :::rechnung
            2(x - 3) = x + 1 || Klammer auflösen
            2x - 6 = x + 1 \quad | -x || $x$ nach links
            x - 6 = 1 \quad | +6 || Zahlen nach rechts
            x = 7 || Probe: $2 \cdot 4 = 8 = 7 + 1$
            :::
            """,
            typische_fehler=[("{4}", "Beim Auflösen der Klammer wurde nur $x$ malgenommen: $2(x - 3) = 2x - 6$, nicht $2x - 3$."),
                             ("{-5}", "Vorzeichenfehler: Aus $x - 6 = 1$ wird mit $+6$ die Gleichung $x = 7$.")])

k.gleichung("2x + 1 = 2x + 5", loesung="keine",
            erklaerung="Nach $-2x$ bleibt $1 = 5$. Das ist falsch, egal was $x$ ist: keine Lösung.",
            tipps=["Bring die $x$-Terme auf eine Seite. Was passiert?", "Nach $-2x$ ist kein $x$ mehr da.",
                   "$1 = 5$ ist falsch. Was heißt das für die Lösungsmenge?"],
            rechenweg="Nach $-2x$ auf beiden Seiten bleibt $1 = 5$ übrig. Diese Aussage ist für kein $x$ wahr, "
                      "also $\\mathbb{L} = \\emptyset$.",
            typische_fehler=[("{0}", "$x = 0$ ist keine Lösung: Probe $1 = 5$ stimmt nicht. Wenn $x$ verschwindet "
                                     "und etwas Falsches übrig bleibt, gibt es gar keine Lösung."),
                             ("R", "Übrig bleibt $1 = 5$. Das ist falsch, also passt keine Zahl.")])

k.gleichung("3(x + 2) = 3x + 6", loesung="R",
            erklaerung="Nach dem Auflösen steht links und rechts dasselbe: $3x + 6 = 3x + 6$. Jede Zahl ist Lösung.",
            tipps=["Löse die Klammer auf und vergleiche beide Seiten.",
                   "Links $3x + 6$, rechts $3x + 6$.", "Was bleibt nach $-3x$ übrig? Ist das wahr?"],
            rechenweg=r"""
            :::rechnung
            3(x + 2) = 3x + 6 || Klammer auflösen
            3x + 6 = 3x + 6 || beide Seiten gleich
            6 = 6 || wahr für jedes $x$: $\mathbb{L} = \mathbb{R}$
            :::
            """,
            typische_fehler=[("keine", "Wenn $x$ verschwindet und etwas **Wahres** übrig bleibt ($6 = 6$), passt jede Zahl."),
                             ("{0}", "$0$ ist eine Lösung, aber nicht die einzige. Probiere $x = 1$: $9 = 9$.")])

# ── 3: Brüche und Bruchgleichungen ─────────────────────────────────────────
k.erklaerung("Gleichungen mit Brüchen", r"""
    ## Nenner wegschaffen

    Stehen Brüche in der Gleichung, nimmst du **beide Seiten** mit dem
    [[Hauptnenner]] mal. Danach sind alle Brüche verschwunden.

    :::rechnung Beispiel vorgerechnet
    \frac{x}{2} + \frac{x}{3} = 5 \quad | \cdot 6 || Hauptnenner von $2$ und $3$ ist $6$
    3x + 2x = 30 || jeder Summand wird mal $6$ genommen: $6 \cdot \frac{x}{2} = 3x$
    5x = 30 \quad | :5 || zusammenfassen
    x = 6 || Probe: $3 + 2 = 5$
    :::

    :::achtung Nicht jeden Summanden malgenommen
    $\frac{x}{2} + \frac{x}{3} = 5 \to 3x + 2x = 5$ ist falsch. Die rechte Seite
    bekommt die $6$ auch ab: $30$.
    :::

    :::alt Mit Minuten erklärt
    $\frac{x}{2}$ und $\frac{x}{3}$ sind wie halbe und drittel Stunden. Rechnest du alles
    in Minuten, verschwinden die Brüche: Aus Stunden wird mal $60$. Genauso machst du
    mit „mal $6$“ aus Halben und Dritteln ganze Sechstel.
    :::
    ---
    ## Bruchgleichungen: erst die Definitionsmenge

    Steht $x$ **im Nenner**, heißt die Gleichung [[Bruchgleichung]]. Ein Nenner darf
    nie $0$ werden. Deshalb bestimmst du **vor** dem Rechnen die
    [[Definitionsmenge]] $D$: alle Zahlen, die man einsetzen darf.

    Bei $\frac{6}{x} + 1 = 4$ ist $x = 0$ verboten, also $D = \mathbb{R} \setminus \{0\}$.

    :::rechnung Beispiel vorgerechnet
    \frac{6}{x} + 1 = 4 \quad | -1 || Zahl nach rechts
    \frac{6}{x} = 3 \quad | \cdot x || mit dem Nenner malnehmen, erlaubt wegen $x \neq 0$
    6 = 3x \quad | :3 || durch $3$ teilen
    x = 2 || $2$ liegt in $D$, also $\mathbb{L} = \{2\}$
    :::

    :::alt Mit einem Verbotsschild erklärt
    Stell dir die Zahlengerade als Straße vor. An der Stelle $0$ steht ein Schild:
    „Durchfahrt verboten“, denn $\frac{6}{0}$ gibt es nicht. Bevor du losrechnest,
    schaust du nach solchen Schildern. Landet deine Lösung genau dort, zählt sie nicht.
    :::
    ---
    ## Scheinlösungen aussortieren

    Beim Malnehmen mit dem Nenner kann eine Zahl entstehen, die gar nicht in $D$
    liegt. So eine Zahl heißt [[Scheinlösung]].

    :::visual zahlenstrahl
    {"von": -2, "bis": 5, "punkte": [{"x": 2, "label": "verboten", "farbe": "orange"}],
     "unterschrift": "Bei $\\frac{x}{x - 2} = \\frac{2}{x - 2}$ ist $x = 2$ verboten: Der Nenner wäre $0$."}
    :::

    Bei $\frac{x}{x - 2} = \frac{2}{x - 2}$ ist $D = \mathbb{R} \setminus \{2\}$.
    Mal $(x - 2)$ ergibt $x = 2$. Aber $2 \notin D$. Also $\mathbb{L} = \emptyset$.

    :::achtung Definitionsmenge vergessen
    Wer $D$ nicht bestimmt, schreibt $\mathbb{L} = \{2\}$. Die Probe zeigt den Fehler:
    $\frac{2}{0}$ ist nicht definiert.
    :::

    :::alt Mit einer Fahrkarte erklärt
    Eine Lösung braucht eine gültige Fahrkarte, und die heißt $D$. Die $2$ hat die
    Rechnung zwar bis zum Schluss überstanden, aber ohne Fahrkarte. An der Kontrolle,
    der Probe, fliegt sie raus.
    :::
    """)

k.gleichung("x/2 + x/3 = 5", loesung="{6}",
            erklaerung="Mal $6$: $3x + 2x = 30$, also $5x = 30$ und $x = 6$.",
            tipps=["Schaffe die Nenner weg: Womit musst du malnehmen?",
                   "Der Hauptnenner ist $6$. Nimm **jeden** Summanden mal $6$, auch die rechte Seite.",
                   "$3x + 2x = 30$"],
            rechenweg=r"""
            :::rechnung
            \frac{x}{2} + \frac{x}{3} = 5 \quad | \cdot 6 || Hauptnenner $6$
            3x + 2x = 30 || jeder Summand mal $6$
            5x = 30 \quad | :5 || zusammenfassen
            x = 6 || Probe: $3 + 2 = 5$
            :::
            """,
            typische_fehler=[("{1}", "Die rechte Seite wurde nicht mit $6$ malgenommen. Jeder Summand auf **beiden** Seiten bekommt die $6$."),
                             ("{25/2}", "$\\frac{x}{2} + \\frac{x}{3}$ ist nicht $\\frac{2x}{5}$. Nenner werden nie addiert.")])

k.loesungsmenge("Gib die Definitionsmenge $D$ der Bruchgleichung $\\frac{3}{x - 4} = 1$ an. "
                "(Eingabe zum Beispiel `R \\ {1}`)",
                "R \\ {4}",
                "Der Nenner $x - 4$ wird $0$ für $x = 4$. Alle anderen Zahlen sind erlaubt: $D = \\mathbb{R} \\setminus \\{4\\}$.",
                tipps=["Welche Zahl macht den Nenner zu $0$?", "Löse $x - 4 = 0$.",
                       "$x = 4$ ist verboten. Alle anderen Zahlen sind erlaubt."],
                rechenweg=r"""
                :::rechnung
                x - 4 = 0 \quad | +4 || Wann ist der Nenner $0$?
                x = 4 || diese Zahl ist verboten
                :::
                Also $D = \mathbb{R} \setminus \{4\}$.
                """,
                typische_fehler=[("R \\ {-4}", "Setze $-4$ ein: $-4 - 4 = -8$, nicht $0$. Verboten ist $x = 4$."),
                                 ("R", "Für $x = 4$ steht $\\frac{3}{0}$ da. Diese Zahl muss aus $D$ heraus."),
                                 ("{4}", "Das ist gerade die **verbotene** Zahl. $D$ enthält alle anderen Zahlen.")])

k.loesungsmenge("Löse $\\frac{12}{x} - 1 = 3$. Gib die Lösungsmenge an.", "{3}",
                "$D = \\mathbb{R} \\setminus \\{0\\}$. Dann $\\frac{12}{x} = 4$, mal $x$: $12 = 4x$, also $x = 3 \\in D$.",
                tipps=["Bestimme zuerst $D$: Wann ist der Nenner $0$?",
                       "Bring die $1$ nach rechts: $\\frac{12}{x} = 4$.", "Mal $x$: $12 = 4x$."],
                rechenweg=r"""
                $D = \mathbb{R} \setminus \{0\}$.

                :::rechnung
                \frac{12}{x} - 1 = 3 \quad | +1 || Zahl nach rechts
                \frac{12}{x} = 4 \quad | \cdot x || erlaubt, da $x \neq 0$
                12 = 4x \quad | :4 || teilen
                x = 3 || $3 \in D$
                :::
                """,
                typische_fehler=[("{6}", "Vorzeichenfehler: Aus $-1$ wird beim Herüberholen $+1$, also $\\frac{12}{x} = 4$."),
                                 ("{1/3}", "Du hast $4 : 12$ gerechnet. Aus $12 = 4x$ folgt $x = 12 : 4$.")])

k.loesungsmenge("Löse $\\frac{x}{x - 2} = \\frac{2}{x - 2}$. Gib die Lösungsmenge an.", "keine",
                "$D = \\mathbb{R} \\setminus \\{2\\}$. Mal $(x - 2)$ ergibt $x = 2$, aber $2 \\notin D$. Also $\\mathbb{L} = \\emptyset$.",
                tipps=["Bestimme zuerst die Definitionsmenge.", "$x = 2$ ist verboten. Was liefert die Rechnung?",
                       "Die Rechnung liefert $x = 2$. Liegt das in $D$?"],
                rechenweg=r"""
                $D = \mathbb{R} \setminus \{2\}$, denn für $x = 2$ wird der Nenner $0$.

                Mal $(x - 2)$ auf beiden Seiten ergibt $x = 2$.

                $2 \notin D$: Das ist eine Scheinlösung. Also $\mathbb{L} = \emptyset$.
                """,
                typische_fehler=[("{2}", "Probe: $\\frac{2}{0}$ ist nicht definiert. $2$ liegt nicht in $D$, es ist eine Scheinlösung.")])

# ── 4: Formeln umstellen ───────────────────────────────────────────────────
k.erklaerung("Formeln umstellen", r"""
    ## Buchstaben wie Zahlen behandeln

    :::analogie 🚗 Autofahrt
    $s = v \cdot t$: Weg ist Geschwindigkeit mal Zeit. Du kennst Weg und Tempo und
    willst die Zeit wissen. Dann stellst du die Formel nach $t$ um.
    :::

    Eine Formel ist eine Gleichung mit mehreren Buchstaben. Beim Umstellen tust du so,
    als wären alle anderen Buchstaben Zahlen. Du machst genau die Schritte, die du
    auch mit Zahlen machen würdest.

    :::rechnung Erst mit Zahlen: $120$ km bei $60$ km/h
    120 = 60t \quad | :60 || durch die Zahl vor $t$ teilen
    2 = t || also $t = 2$ Stunden
    t = 2 || Probe: $60 \cdot 2 = 120$
    :::

    | Mit Buchstaben | Schritt |
    |---|---|
    | $s = v \cdot t$ | Ausgangsformel |
    | $\frac{s}{v} = t$ | beide Seiten $: v$ (erlaubt für $v \neq 0$) |
    | $t = \frac{s}{v}$ | Seiten tauschen |

    :::alt Mit Kästchen erklärt
    Decke $v$ mit einem Kästchen ab, in dem $60$ steht. Dann siehst du die Aufgabe
    $s = 60 \cdot t$, und die löst du mit $:60$. Nimm das Kästchen wieder weg: Aus
    $:60$ wird $:v$. Die Buchstaben ändern nichts am Rechenweg.
    :::
    ---
    ## Mehrere Schritte: rückwärts abbauen

    Die Umrechnung von Grad Celsius in Fahrenheit lautet $F = \frac{9}{5}C + 32$.
    Gesucht ist $C$. Mit $C$ passiert zuerst „mal $\frac{9}{5}$“, dann „plus $32$“.
    Zum Umstellen gehst du rückwärts.

    :::rechnung Erst mit Zahlen: $F = 212$
    212 = \frac{9}{5}C + 32 \quad | -32 || zuletzt kam $+32$, also zuerst $-32$
    180 = \frac{9}{5}C \quad | \cdot \frac{5}{9} || mit dem Kehrwert malnehmen
    100 = C || Wasser kocht bei $100$ Grad Celsius
    C = 100 || Seiten tauschen
    :::

    | Mit Buchstaben | Schritt |
    |---|---|
    | $F = \frac{9}{5}C + 32$ | Ausgangsformel |
    | $F - 32 = \frac{9}{5}C$ | $-32$ |
    | $\frac{5}{9}(F - 32) = C$ | $\cdot \frac{5}{9}$, Klammer nicht vergessen |

    :::achtung Die Klammer vergessen
    $C = \frac{5}{9}F - 32$ ist falsch. Das $\frac{5}{9}$ gilt für die ganze
    linke Seite $F - 32$, deshalb die Klammer.
    :::

    :::alt Mit einer Pfeilkette erklärt
    Schreib auf, was mit $C$ passiert: $C \to$ mal $\frac{9}{5}$ $\to$ plus $32$ $\to F$.
    Rückwärts kehrst du jeden Pfeil um und startest hinten: $F \to$ minus $32$
    $\to$ mal $\frac{5}{9}$ $\to C$. Also $C = \frac{5}{9}(F - 32)$.
    :::
    """)

k.term("Stelle $s = v \\cdot t$ nach $t$ um. Gib den Term für $t$ an.", "s/v",
       "Beide Seiten durch $v$ teilen: $t = \\frac{s}{v}$ (für $v \\neq 0$).", variablen="s, v",
       tipps=["Mit $t$ passiert nur „mal $v$“.", "Mach es rückgängig: beide Seiten durch $v$.",
              "$\\frac{s}{v} = t$"],
       rechenweg=r"""
       | Formel | Schritt |
       |---|---|
       | $s = v \cdot t$ | Ausgangsformel |
       | $\frac{s}{v} = t$ | beide Seiten $: v$ |
       """,
       typische_fehler=[("v/s", "Kehrwert erwischt: $s$ steht oben, also $t = \\frac{s}{v}$. Probe: $s = 120$, $v = 60$ ergibt $2$ Stunden."),
                        ("s*v", "Das $\\cdot v$ machst du mit $: v$ rückgängig, nicht mit noch einem $\\cdot v$.")])

k.term("Stelle $F = \\frac{9}{5}C + 32$ nach $C$ um. Gib den Term für $C$ an.", "5/9*(F - 32)",
       "Erst $-32$, dann mal $\\frac{5}{9}$: $C = \\frac{5}{9}(F - 32)$.", variablen="F",
       tipps=["Was passierte mit $C$ zuletzt? Das machst du zuerst rückgängig.",
              "Erst $-32$: $F - 32 = \\frac{9}{5}C$.", "Jetzt mit dem Kehrwert $\\frac{5}{9}$ malnehmen. Klammer!"],
       rechenweg=r"""
       | Formel | Schritt |
       |---|---|
       | $F = \frac{9}{5}C + 32$ | Ausgangsformel |
       | $F - 32 = \frac{9}{5}C$ | $-32$ |
       | $\frac{5}{9}(F - 32) = C$ | $\cdot \frac{5}{9}$ |
       """,
       typische_fehler=[("5/9*F - 32", "Klammer vergessen: Das $\\frac{5}{9}$ gilt für die ganze Seite $F - 32$."),
                        ("9/5*(F - 32)", "Du musst mit dem **Kehrwert** $\\frac{5}{9}$ malnehmen, nicht noch einmal mit $\\frac{9}{5}$."),
                        ("5/9*(F + 32)", "Die $+32$ verschwindet mit $-32$.")])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _vz(z):
    return f"+ {tex(z)}" if z >= 0 else f"- {tex(-z)}"


def _lin(a, b):
    """a x + b als LaTeX."""
    if a == 0:
        return tex(b)
    ax = "x" if a == 1 else "-x" if a == -1 else f"{a}x"
    return ax if b == 0 else f"{ax} {_vz(b)}"


def _menge(w):
    return "{" + mathlib.text(w) + "}"


def _fehler_mengen(loes, fehler):
    """Fehlwerte als Mengen; gleich der Lösung oder doppelt -> weg."""
    erg, gesehen = [], {loes}
    for w, m in fehler:
        if w is None or w in gesehen:
            continue
        gesehen.add(w)
        erg.append((_menge(w), m))
    return erg


def lineare_gleichung(rng):
    while True:
        x0 = rng.randint(-9, 9)
        a = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6, 7])
        c = rng.choice([0, 0, -3, -2, -1, 1, 2, 3, 4])
        b = rng.choice([z for z in range(-12, 13) if z])
        if a - c not in (0, 1, -1) and (c == 0 or a + c != 0):
            break
    d = (a - c) * x0 + b
    m = a - c
    links, rechts = _lin(a, b), _lin(c, d)
    zeilen = []
    if c != 0:
        cx = "x" if c == 1 else "-x" if c == -1 else f"{c}x"
        notiz = f"-{cx}" if c > 0 else f"+{cx[1:]}"
        zeilen.append((f"{links} = {rechts} \\quad | {notiz}", "$x$-Terme nach links"))
    zeilen.append((f"{_lin(m, b)} = {tex(d)} \\quad | {'-' if b > 0 else '+'}{abs(b)}", "Zahlen nach rechts"))
    zeilen.append((f"{m}x = {tex(d - b)} \\quad | :{mathlib.tex_klammer(m)}", "durch die Zahl vor $x$ teilen"))
    zeilen.append((f"x = {x0}", f"Probe: links und rechts kommt ${a * x0 + b}$ heraus"))
    fehler = [(F(d + b, m), "Vorzeichenfehler beim Herüberholen der Zahl: Aus $+b$ wird auf der anderen Seite $-b$."),
              (F(d - b) * m, "Du hast malgenommen statt geteilt. Das $\\cdot$ vor $x$ wird mit $:$ rückgängig gemacht."),
              (F(d - b, -m), "Das Vorzeichen der Zahl vor $x$ gehört beim Teilen dazu.")]
    if c != 0 and a + c != 0:
        fehler.append((F(d - b, a + c), "Die $x$-Terme wurden addiert statt abgezogen. Was rechts verschwindet, wird links abgezogen."))
    return {
        "frage": f"Löse ${links} = {rechts}$. Gib die Lösungsmenge an.",
        "loesung": _menge(F(x0)),
        "tipps": ["Sammle alle $x$-Terme links und alle Zahlen rechts." if c else "Bring zuerst die Zahl auf die rechte Seite.",
                  f"Am Ende steht ${m}x = {tex(d - b)}$.", f"Teile durch ${m}$."],
        "rechenweg": _zeilen(*zeilen),
        "erklaerung": "Sortieren ($x$ links, Zahlen rechts), dann durch die Zahl vor $x$ teilen. Probe nicht vergessen.",
        "typische_fehler": _fehler_mengen(F(x0), fehler),
    }


def bruchgleichung(rng):
    while True:
        p = rng.randint(-6, 6)
        q = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5, 6])      # q = x0 - p
        b = rng.choice([-4, -3, -2, 2, 3, 4, 5])
        c = rng.choice([0, 0, -3, -2, -1, 1, 2, 3, 4])
        if p != 0 or c != 0:
            break
    a = b * q
    x0 = p + q
    nenner = "x" if p == 0 else f"x {_vz(-p)}"
    bruch = f"\\frac{{{a}}}{{{nenner}}}"
    links = bruch if c == 0 else f"{bruch} {_vz(c)}"
    rechts = b + c
    zeilen = []
    if c != 0:
        zeilen.append((f"{links} = {rechts} \\quad | {'-' if c > 0 else '+'}{abs(c)}", "Zahl nach rechts"))
    klam = "x" if p == 0 else f"({nenner})"
    zeilen.append((f"{bruch} = {b} \\quad | \\cdot {klam}", f"mit dem Nenner malnehmen, erlaubt wegen $x \\neq {p}$"))
    if p == 0:
        zeilen.append((f"{a} = {b}x \\quad | :{mathlib.tex_klammer(b)}", "durch die Zahl vor $x$ teilen"))
    else:
        zeilen.append((f"{a} = {b}({nenner})", "Klammer stehen lassen"))
        zeilen.append((f"{a} = {b}x {_vz(-b * p)} \\quad | {'-' if -b * p > 0 else '+'}{abs(b * p)}", "Klammer auflösen, Zahl nach links"))
        zeilen.append((f"{a + b * p} = {b}x \\quad | :{mathlib.tex_klammer(b)}", "durch die Zahl vor $x$ teilen"))
    zeilen.append((f"x = {x0}", f"${x0} \\neq {p}$, also liegt die Lösung in $D$"))
    fehler = [(F(a, b) - p if p != 0 else None, "Beim Auflösen von $b(x - p)$ ist ein Vorzeichen gekippt. Mach die Probe."),
              (F(a, b) if p != 0 else None, "Du hast nur durch $b$ geteilt und den Nenner-Teil vergessen: Es gilt $x - p = \\frac{a}{b}$, also noch $p$ dazu."),
              (F(b, a) + p if a != 0 else None, "Kehrwert erwischt: Aus $a = b \\cdot (\\ldots)$ folgt $(\\ldots) = \\frac{a}{b}$."),
              (F(a, rechts) + p if c != 0 and rechts != 0 else None, "Die Zahl auf der linken Seite muss zuerst nach rechts, bevor du mit dem Nenner malnimmst."),
              (F(p), f"${p}$ ist genau die Zahl, die den Nenner $0$ macht. Sie liegt nicht in $D$ und ist nie eine Lösung."),
              (F(-x0), "Fast: Der Betrag stimmt, aber das Vorzeichen nicht. Mach die Probe.")]
    return {
        "frage": f"Löse ${links} = {rechts}$. Gib die Lösungsmenge an.",
        "loesung": _menge(F(x0)),
        "tipps": [f"Definitionsmenge zuerst: Für welches $x$ wird ${nenner}$ zu $0$?",
                  (f"Bring die ${c}$ auf die rechte Seite, dann " if c else "") + ("n" if c else "N") + f"imm beide Seiten mal ${klam}$.",
                  f"Es entsteht ${a} = {b}" + (f"({nenner})$." if p else "x$.")],
        "rechenweg": f"$D = \\mathbb{{R}} \\setminus \\{{{p}\\}}$.\n\n" + _zeilen(*zeilen),
        "erklaerung": "Erst $D$ bestimmen, dann mit dem Nenner malnehmen, lösen und prüfen, ob die Lösung in $D$ liegt.",
        "typische_fehler": _fehler_mengen(F(x0), fehler),
    }


# (Ausgangsformel LaTeX, gesucht, Lösung (Term), Variablen, [(LaTeX-Zeile, Schritt)], [(Fehlterm, Meldung)])
_FORMELN = [
    (r"U = R \cdot I", "I", "U/R", "U, R", [(r"\frac{U}{R} = I", r"beide Seiten $: R$")],
     [("R/U", "Kehrwert erwischt: $U$ steht oben."), ("U*R", r"$\cdot R$ macht man mit $: R$ rückgängig.")]),
    (r"s = v \cdot t", "v", "s/t", "s, t", [(r"\frac{s}{t} = v", r"beide Seiten $: t$")],
     [("t/s", "Kehrwert erwischt: $s$ steht oben."), ("s*t", r"$\cdot t$ macht man mit $: t$ rückgängig.")]),
    (r"P = U \cdot I", "U", "P/I", "P, I", [(r"\frac{P}{I} = U", r"beide Seiten $: I$")],
     [("I/P", "Kehrwert erwischt: $P$ steht oben."), ("P*I", r"$\cdot I$ macht man mit $: I$ rückgängig.")]),
    (r"F = m \cdot a", "m", "F/a", "F, a", [(r"\frac{F}{a} = m", r"beide Seiten $: a$")],
     [("a/F", "Kehrwert erwischt: $F$ steht oben."), ("F - a", "Malnehmen macht man mit Teilen rückgängig, nicht mit Abziehen.")]),
    (r"A = \frac{1}{2} g \cdot h", "h", "2A/g", "A, g",
     [(r"2A = g \cdot h", r"beide Seiten $\cdot 2$"), (r"\frac{2A}{g} = h", r"beide Seiten $: g$")],
     [("A/(2g)", r"Das $\frac{1}{2}$ machst du mit $\cdot 2$ rückgängig. Die $2$ steht dann oben."),
      ("2g/A", "Kehrwert erwischt: $A$ steht oben.")]),
    (r"y = m x + b", "x", "(y - b)/m", "y, m, b",
     [(r"y - b = m x", r"$-b$"), (r"\frac{y - b}{m} = x", r"beide Seiten $: m$")],
     [("y/m - b", r"Reihenfolge: Erst $-b$, dann $: m$. Das $: m$ gilt für die ganze Seite $y - b$."),
      ("(y + b)/m", r"Die $+b$ verschwindet mit $-b$.")]),
    (r"v = \frac{s}{t}", "t", "s/v", "s, v",
     [(r"v \cdot t = s", r"beide Seiten $\cdot t$"), (r"t = \frac{s}{v}", r"beide Seiten $: v$")],
     [("v/s", "Kehrwert erwischt: $s$ steht oben."), ("s*v", r"Zuletzt musst du durch $v$ teilen, nicht malnehmen.")]),
    (r"u = 2a + 2b", "b", "(u - 2a)/2", "u, a",
     [(r"u - 2a = 2b", r"$-2a$"), (r"\frac{u - 2a}{2} = b", r"beide Seiten $: 2$")],
     [("u/2 - 2a", r"Das $: 2$ gilt für die ganze Seite $u - 2a$, also auch für $2a$."),
      ("(u + 2a)/2", r"Die $+2a$ verschwindet mit $-2a$.")]),
    (r"C = \frac{5}{9}(F - 32)", "F", "9/5*C + 32", "C",
     [(r"\frac{9}{5}C = F - 32", r"beide Seiten $\cdot \frac{9}{5}$ (Kehrwert)"), (r"\frac{9}{5}C + 32 = F", r"$+32$")],
     [("9/5*C - 32", r"Die $-32$ verschwindet mit $+32$."), ("5/9*C + 32", r"Mit dem **Kehrwert** $\frac{9}{5}$ malnehmen.")]),
    (r"V = l \cdot b \cdot h", "h", "V/(l*b)", "V, l, b", [(r"\frac{V}{l \cdot b} = h", r"beide Seiten $: (l \cdot b)$")],
     [("V/l*b", r"Du teilst durch das ganze Produkt $l \cdot b$: Beide stehen im Nenner."),
      ("l*b/V", "Kehrwert erwischt: $V$ steht oben.")]),
    (r"E = m \cdot c^2", "m", "E/c^2", "E, c", [(r"\frac{E}{c^2} = m", r"beide Seiten $: c^2$")],
     [("E/c", r"Geteilt wird durch $c^2$, nicht durch $c$."), ("E*c^2", r"$\cdot c^2$ macht man mit $: c^2$ rückgängig.")]),
    (r"K = 100 + 5n", "n", "(K - 100)/5", "K",
     [(r"K - 100 = 5n", r"$-100$"), (r"\frac{K - 100}{5} = n", r"beide Seiten $: 5$")],
     [("K/5 - 100", r"Erst $-100$, dann $: 5$ auf die ganze Seite."), ("(K + 100)/5", r"Die $+100$ verschwindet mit $-100$.")]),
]


def formel_umstellen(rng):
    formel, ziel, loes, var, schritte, fehler = rng.choice(_FORMELN)
    tabelle = "| Formel | Schritt |\n|---|---|\n" + f"| ${formel}$ | Ausgangsformel |\n" + \
        "\n".join(f"| ${z}$ | {s} |" for z, s in schritte)
    return {
        "frage": f"Stelle ${formel}$ nach ${ziel}$ um. Gib den Term für ${ziel}$ an.",
        "loesung": loes, "variablen": var,
        "tipps": [f"Was passiert mit ${ziel}$? Mach es in umgekehrter Reihenfolge rückgängig.",
                  f"Erster Schritt: {schritte[0][1]}.",
                  f"Am Ende steht ${schritte[-1][0]}$."],
        "rechenweg": tabelle,
        "erklaerung": "Behandle die anderen Buchstaben wie Zahlen und baue rückwärts ab, was mit der gesuchten Variable passiert.",
        "typische_fehler": fehler,
    }


k.praxis()

k.generator(lineare_gleichung, typ="loesungsmenge", titel="Lineare Gleichungen")
k.generator(bruchgleichung, typ="loesungsmenge", titel="Bruchgleichungen")
k.generator(formel_umstellen, typ="term", titel="Formeln umstellen")

k.loesungsmenge("Löse $\\frac{x}{x - 3} = \\frac{3}{x - 3} + 2$. Gib die Lösungsmenge an.", "keine",
                "$D = \\mathbb{R} \\setminus \\{3\\}$. Mal $(x - 3)$: $x = 3 + 2(x - 3)$, also $x = 3$. "
                "Aber $3 \\notin D$: Scheinlösung. $\\mathbb{L} = \\emptyset$.",
                tipps=["Bestimme zuerst $D$.", "Nimm **jeden** Summanden mal $(x - 3)$, auch die $2$.",
                       "$x = 3 + 2(x - 3)$. Löse und prüfe, ob das Ergebnis in $D$ liegt."],
                rechenweg=r"""
                $D = \mathbb{R} \setminus \{3\}$. Mal $(x - 3)$ auf beiden Seiten:

                :::rechnung
                x = 3 + 2(x - 3) || jeder Summand mal $(x - 3)$
                x = 2x - 3 \quad | -2x || Klammer auflösen, zusammenfassen
                -x = -3 \quad | \cdot (-1) || mal $-1$
                x = 3 || aber $3 \notin D$
                :::

                $x = 3$ ist eine Scheinlösung, also $\mathbb{L} = \emptyset$.
                """,
                typische_fehler=[("{3}", "Probe: Für $x = 3$ steht $\\frac{3}{0}$ da. $3$ liegt nicht in $D$, es ist eine Scheinlösung."),
                                 ("{1}", "Die $2$ wurde nicht mit $(x - 3)$ malgenommen. Jeder Summand bekommt den Faktor ab.")])

# Übungsblatt-Stil: Bruchgleichung mit zwei Nennern
_L = F(2, 3)
k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: Bruchgleichung

    Bestimmen Sie die Definitionsmenge und die Lösungsmenge der Gleichung
    $$\frac{2}{x - 1} + \frac{1}{x + 1} = \frac{3}{x^2 - 1}.$$
    Geben Sie alle Zwischenschritte an.
    """,
    [{"typ": "loesungsmenge", "frage": "Bestimme die Definitionsmenge $D$ (Eingabe zum Beispiel `R \\ {2; 5}`).",
      "loesung": "R \\ {-1; 1}",
      "tipps": ["Welche Zahlen machen einen der Nenner zu $0$?", "$x - 1 = 0$, $x + 1 = 0$ und $x^2 - 1 = 0$."],
      "rechenweg": "$x - 1 = 0$ für $x = 1$, $x + 1 = 0$ für $x = -1$, und $x^2 - 1 = (x + 1)(x - 1)$ liefert nichts Neues. "
                   "Also $D = \\mathbb{R} \\setminus \\{-1, 1\\}$.",
      "typische_fehler": [("R \\ {1}", "Auch $x + 1$ ist ein Nenner. Für $x = -1$ wird er $0$.")]},
     {"typ": "term", "frage": "Nimm beide Seiten mit dem Hauptnenner $x^2 - 1 = (x + 1)(x - 1)$ mal. "
                              "Welcher Term steht danach auf der **linken** Seite (zusammengefasst)?",
      "loesung": "3x + 1", "variablen": "x",
      "tipps": ["$\\frac{2}{x - 1} \\cdot (x + 1)(x - 1) = 2(x + 1)$.", "$2(x + 1) + (x - 1)$ zusammenfassen."],
      "rechenweg": "$2(x + 1) + 1 \\cdot (x - 1) = 2x + 2 + x - 1 = 3x + 1$",
      "typische_fehler": [("3x + 3", "Der zweite Summand ist $1 \\cdot (x - 1) = x - 1$, nicht $x + 1$."),
                          ("3", "Links bleiben die Faktoren stehen, die sich **nicht** wegkürzen: $2(x + 1) + (x - 1)$.")]},
     {"typ": "loesungsmenge", "frage": "Löse $3x + 1 = 3$ und prüfe gegen $D$. Gib die Lösungsmenge an.",
      "loesung": "{" + mathlib.text(_L) + "}",
      "tipps": ["$-1$, dann $:3$.", "$x = \\frac{2}{3}$. Liegt das in $D$?"],
      "rechenweg": "$3x = 2$, also $x = \\frac{2}{3}$. Es ist $\\frac{2}{3} \\neq \\pm 1$, also $\\mathbb{L} = \\{\\frac{2}{3}\\}$.",
      "typische_fehler": [("{4/3}", "Vorzeichenfehler: Aus $+1$ wird beim Herüberholen $-1$."),
                          ("keine", "$\\frac{2}{3}$ ist erlaubt: Nur $1$ und $-1$ fehlen in $D$.")]}],
    "Erst $D$ bestimmen, dann mit dem Hauptnenner malnehmen, die lineare Gleichung lösen und gegen $D$ prüfen.",
    uebungsblatt=True,
    tipps=["Faktorisiere $x^2 - 1$ mit der dritten binomischen Formel.",
           "Der Hauptnenner ist $(x + 1)(x - 1)$."],
    rechenweg=r"""
    $D = \mathbb{R} \setminus \{-1, 1\}$, denn $x^2 - 1 = (x + 1)(x - 1)$.

    :::rechnung
    \frac{2}{x - 1} + \frac{1}{x + 1} = \frac{3}{x^2 - 1} \quad | \cdot (x + 1)(x - 1) || mit dem Hauptnenner malnehmen
    2(x + 1) + (x - 1) = 3 || Nenner kürzen sich weg
    3x + 1 = 3 \quad | -1 || zusammenfassen
    3x = 2 \quad | :3 || teilen
    x = \frac{2}{3} || $\frac{2}{3} \in D$
    :::

    Also $\mathbb{L} = \{\frac{2}{3}\}$.
    """)

k.zusammenfassung(r"""
    ## Gleichungen lösen

    | Was | Regel |
    |---|---|
    | Äquivalenzumformung | auf **beiden** Seiten dasselbe: $+$, $-$, $\cdot$ und $:$ (nicht mit $0$) |
    | Lineare Gleichung | $x$-Terme links, Zahlen rechts, durch die Zahl vor $x$ teilen |
    | $x$ verschwindet | falsche Aussage: $\mathbb{L} = \emptyset$, wahre Aussage: $\mathbb{L} = \mathbb{R}$ |
    | Brüche | mit dem Hauptnenner malnehmen, jeden Summanden |
    | Bruchgleichung | **zuerst** $D$ bestimmen, am Ende Lösungen gegen $D$ prüfen |
    | Formel umstellen | andere Buchstaben wie Zahlen behandeln, rückwärts abbauen |

    !! Probe: Lösung in die Ausgangsgleichung einsetzen. Links und rechts muss dasselbe herauskommen.

    - Beispiel: $\frac{x}{x - 2} = \frac{2}{x - 2}$ liefert $x = 2 \notin D$, also $\mathbb{L} = \emptyset$.
    - $F = \frac{9}{5}C + 32 \iff C = \frac{5}{9}(F - 32)$
""")
