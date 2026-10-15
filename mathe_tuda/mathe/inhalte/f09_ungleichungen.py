# -*- coding: utf-8 -*-
"""Fundament 9: Ungleichungen – umformen, Zeichen kippen, Intervalle, Doppelungleichungen, Fallunterscheidung."""
from fractions import Fraction as F

from .. import mathlib, pruefer
from ..engine import neues_kapitel

tex = mathlib.tex

k = neues_kapitel(
    slug="ungleichungen",
    titel="Ungleichungen",
    beschreibung="Ungleichungen umformen, das Zeichen bei negativen Faktoren umdrehen und Lösungen als Intervall angeben",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="📏")

k.lernziele([
    "Ich kann prüfen, ob eine Zahl eine Ungleichung erfüllt, und die Lösungsmenge als Intervall schreiben",
    "Ich forme lineare Ungleichungen um und drehe das Zeichen beim Malnehmen oder Teilen mit einer negativen Zahl",
    "Ich löse Doppelungleichungen und erkenne Ungleichungen ohne Lösung oder mit ganz $\\mathbb{R}$ als Lösung",
    "Ich mache eine Fallunterscheidung, wenn ich mit einem Term malnehme, dessen Vorzeichen ich nicht kenne",
])

k.warum(r"""
Ungleichungen stecken in jeder `if`-Abfrage: `if 0 <= i < len(liste)` prüft, ob ein Index
gültig ist. Das ist genau die Doppelungleichung $0 \le i < n$, also das Intervall $[0, n)$.
Laufzeitabschätzungen in der Informatik sind Ungleichungen: „Der Algorithmus braucht höchstens
$3n + 5$ Schritte.“ In Mathe 1 und 2 beweist du Grenzwerte mit Ungleichungen wie
$|a_n - a| < \varepsilon$. Wer dort das Zeichen falsch herum dreht, beweist das Falsche.
""")


def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


# ── 1: Ungleichung und Intervall ───────────────────────────────────────────
k.erklaerung("Ungleichungen und Intervalle", r"""
    ## Viele Lösungen auf einmal

    :::analogie 🎢 Achterbahn
    Am Eingang steht: „Mindestens $140$ cm groß“. Wer $140$, $152$ oder $185$ cm
    groß ist, darf fahren. Für die Körpergröße $x$ in cm gilt $x \ge 140$. Es gibt
    nicht eine Lösung, sondern unendlich viele.
    :::

    Eine [[Ungleichung]] vergleicht zwei Terme mit $<$ (kleiner), $\le$ (kleiner
    oder gleich), $>$ (größer) oder $\ge$ (größer oder gleich).

    :::visual zahlenstrahl
    {"von": 120, "bis": 160, "schritt": 5, "intervalle": [{"von": 140, "bis": "inf", "von_zu": true, "label": "x ≥ 140"}],
     "unterschrift": "Alle Zahlen ab $140$: Die $140$ selbst gehört dazu (voller Punkt)."}
    :::

    Ob eine Zahl passt, prüfst du wie bei Gleichungen durch Einsetzen.

    :::rechnung Probe: Erfüllt $x = 2$ die Ungleichung $2x + 1 < 7$?
    2 \cdot 2 + 1 = 5 || $2$ einsetzen
    5 < 7 || wahr: $x = 2$ ist eine Lösung
    :::

    :::alt Mit einem Programm erklärt
    Die Kasse der Achterbahn prüft `if groesse >= 140:`. Für jede Größe ist die
    Antwort ja oder nein. Die Lösungsmenge der Ungleichung ist die Menge aller Werte, bei denen
    das Programm „ja“ sagt.
    :::
    ---
    ## Intervalle: Bereiche aufschreiben

    Die Lösungsmenge ist meist ein [[Intervall]], ein lückenloser Bereich auf der
    Zahlengeraden. Eckige Klammer: Der Rand gehört dazu. Runde Klammer: Der Rand
    gehört nicht dazu. Bei $\infty$ steht immer eine runde Klammer.

    | Ungleichung | Intervall |
    |---|---|
    | $x < 3$ | $(-\infty, 3)$ |
    | $x \le 3$ | $(-\infty, 3]$ |
    | $x > -2$ | $(-2, \infty)$ |
    | $-2 < x \le 3$ | $(-2, 3]$ |

    :::visual zahlenstrahl
    {"von": -4, "bis": 5, "intervalle": [{"von": -2, "bis": 3, "von_zu": false, "bis_zu": true, "label": "(-2, 3]"}],
     "unterschrift": "Leerer Kreis bei $-2$ (nicht dabei), voller Punkt bei $3$ (dabei)."}
    :::

    In manchen Büchern steht $]-2, 3]$ statt $(-2, 3]$. Das bedeutet dasselbe.

    :::alt Mit einer Gästeliste erklärt
    Das Intervall ist eine Party, die Ränder sind zwei Gäste. Eckige Klammer: Der
    Gast am Rand steht auf der Liste und darf rein. Runde Klammer: Er steht nicht
    drauf, aber alle, die ihm beliebig nahe stehen, schon. $\infty$ ist gar kein
    Gast, nur „immer weiter“. Darum steht dort immer die runde Klammer.
    :::
    """)

k.wf("$x = 3$ erfüllt die Ungleichung $2x + 1 < 7$.", False,
     "Probe: $2 \\cdot 3 + 1 = 7$. Aber $7 < 7$ ist falsch: $7$ ist nicht **kleiner** als $7$. "
     "Bei $\\le$ wäre $x = 3$ dabei.",
     tipps=["Setze $3$ ein. Ist das Ergebnis wirklich **kleiner** als $7$?"])

k.mehrfach("Welche Zahlen erfüllen $x \\ge -2$?",
           ["$-2$", "$0$", "$5$"], ["$-3$", "$-2{,}5$"],
           "Gesucht sind alle Zahlen ab $-2$, die $-2$ eingeschlossen. $-3$ und $-2{,}5$ liegen links von $-2$.",
           tipps=["$\\ge$ heißt „größer oder gleich“.", "Was liegt auf der Zahlengeraden rechts von $-2$ oder genau auf $-2$?"],
           fehler={"$-3$": "$-3$ liegt links von $-2$ und ist damit kleiner.",
                   "$-2{,}5$": "$-2{,}5$ liegt links von $-2$. Bei negativen Zahlen ist die mit dem größeren Betrag die kleinere."})

k.loesungsmenge("Schreibe die Lösungsmenge von $x \\le 4$ als Intervall. (Eingabe zum Beispiel `(-inf; 2)`)",
                "(-inf; 4]",
                "Alle Zahlen bis $4$, die $4$ eingeschlossen: $(-\\infty, 4]$.",
                tipps=["Wo beginnt der Bereich, wo endet er?", "Er reicht unendlich weit nach links bis $4$.",
                       "Gehört die $4$ dazu? Dann eckige Klammer."],
                rechenweg="$x \\le 4$: alle Zahlen links von $4$ und die $4$ selbst. Links unbegrenzt: $-\\infty$ mit runder "
                          "Klammer. Rechts die $4$ mit eckiger Klammer. Also $(-\\infty, 4]$.",
                typische_fehler=[("(-inf; 4)", "Bei $\\le$ gehört die $4$ dazu: eckige Klammer."),
                                 ("[4; inf)", "Das sind die Zahlen **ab** $4$. Gesucht sind die Zahlen **bis** $4$.")])

k.zuordnen("Ordne jeder Ungleichung ihr Intervall zu.",
           [("$x < 1$", "(−∞, 1)"), ("$x \\ge 1$", "[1, ∞)"), ("$0 \\le x < 1$", "[0, 1)"), ("$x > 0$", "(0, ∞)")],
           "Eckige Klammer, wenn der Rand dazugehört ($\\le$, $\\ge$). Runde Klammer bei $<$, $>$ und immer bei $\\infty$.",
           ablenker=["(−∞, 1]", "[1, ∞]"],
           tipps=["Achte darauf, ob der Rand dazugehört. Und bei ∞ steht nie eine eckige Klammer."])

# ── 2: Umformen ────────────────────────────────────────────────────────────
k.erklaerung("Ungleichungen umformen", r"""
    ## Fast wie bei Gleichungen

    Du darfst auf beiden Seiten dieselbe Zahl addieren oder abziehen. Du darfst mit
    einer **positiven** Zahl malnehmen oder durch sie teilen. Das Zeichen bleibt.

    :::rechnung Beispiel vorgerechnet
    2x - 3 < 5 \quad | +3 || $3$ auf beiden Seiten addieren
    2x < 8 \quad | :2 || durch die positive Zahl $2$ teilen
    x < 4 || $\mathbb{L} = (-\infty, 4)$
    :::

    :::visual zahlenstrahl
    {"von": -2, "bis": 7, "intervalle": [{"von": "-inf", "bis": 4, "bis_zu": false, "label": "x < 4"}],
     "unterschrift": "Alle Zahlen links von $4$, ohne die $4$."}
    :::

    :::alt Mit einer schiefen Waage erklärt
    Eine Waage hängt nach rechts, weil rechts mehr liegt. Legst du auf beide Seiten
    dasselbe Gewicht, hängt sie immer noch nach rechts. Nimmst du auf beiden Seiten
    die Hälfte weg, auch. Die Richtung der Schieflage bleibt, genau wie das Zeichen $<$.
    :::
    ---
    ## Negative Zahl: Das Zeichen kippt

    Es gilt $2 < 5$. Mal $(-1)$: Aus $2$ wird $-2$, aus $5$ wird $-5$. Aber $-2$
    liegt **rechts** von $-5$, also gilt $-2 > -5$.

    :::visual zahlenstrahl
    {"von": -6, "bis": 6, "punkte": [{"x": 2, "label": "2"}, {"x": 5, "label": "5"},
     {"x": -2, "label": "-2", "farbe": "orange"}, {"x": -5, "label": "-5", "farbe": "orange"}],
     "unterschrift": "Mal $(-1)$ spiegelt an der $0$: Die Reihenfolge dreht sich um."}
    :::

    !! Beim Malnehmen oder Teilen mit einer **negativen** Zahl dreht sich das Zeichen um.

    :::rechnung Beispiel vorgerechnet
    -3x + 1 \le 7 \quad | -1 || $1$ abziehen, Zeichen bleibt
    -3x \le 6 \quad | :(-3) || durch eine negative Zahl: $\le$ wird zu $\ge$
    x \ge -2 || $\mathbb{L} = [-2, \infty)$
    :::

    :::achtung Zeichen nicht umgedreht
    $-3x \le 6 \to x \le -2$ ist falsch. Probe mit $x = 0$: $-3 \cdot 0 = 0 \le 6$ stimmt,
    also muss $0$ zur Lösung gehören. Bei $x \le -2$ wäre die $0$ nicht dabei.
    :::

    :::alt Mit Schulden erklärt
    $2$ Euro sind weniger als $5$ Euro. Aber $2$ Euro **Schulden** sind besser als
    $5$ Euro Schulden: $-2 > -5$. Das Minus macht aus „weniger“ ein „mehr“. Darum
    dreht sich das Zeichen, sobald du mit einer negativen Zahl malnimmst.
    :::
    ---
    ## x auf beiden Seiten

    Löse zuerst die Klammern auf. Dann sammelst du wie bei Gleichungen alle $x$-Terme
    auf einer Seite.

    :::rechnung Beispiel vorgerechnet
    2(x - 1) \ge 5x + 4 || Klammer auflösen
    2x - 2 \ge 5x + 4 \quad | -5x || $x$-Terme nach links
    -3x - 2 \ge 4 \quad | +2 || Zahlen nach rechts
    -3x \ge 6 \quad | :(-3) || negativ: Zeichen kippt
    x \le -2 || $\mathbb{L} = (-\infty, -2]$
    :::

    :::alt Ohne Kippen gelöst
    Du kannst das Kippen auch umgehen: Bring $x$ auf die Seite, wo mehr $x$ stehen.
    Aus $2x - 2 \ge 5x + 4$ wird mit $-2x$ und $-4$ die Ungleichung $-6 \ge 3x$.
    Jetzt teilst du durch die **positive** $3$: $-2 \ge x$. Gelesen von rechts:
    $x \le -2$. Dasselbe Ergebnis, ohne Zeichenwechsel.
    :::
    """)

k.gleichung("2x - 3 < 5", loesung="(-inf; 4)",
            erklaerung="$+3$, dann $:2$. Beides ändert das Zeichen nicht: $x < 4$.",
            tipps=["Forme um wie bei einer Gleichung.", "Nach $+3$: $2x < 8$.",
                   "Teilen durch die positive $2$: Das Zeichen bleibt."],
            rechenweg=r"""
            :::rechnung
            2x - 3 < 5 \quad | +3 || Zahl nach rechts
            2x < 8 \quad | :2 || positive Zahl: Zeichen bleibt
            x < 4 || $\mathbb{L} = (-\infty, 4)$
            :::
            """,
            typische_fehler=[("(4; inf)", "Du hast das Zeichen gedreht. Beim Teilen durch die **positive** $2$ bleibt es."),
                             ("(-inf; 4]", "Bei $<$ gehört die $4$ nicht dazu: runde Klammer."),
                             ("(-inf; 1)", "Vorzeichenfehler: Die $-3$ verschwindet mit $+3$, also $2x < 8$.")])

k.gleichung("-3x + 1 <= 7", loesung="[-2; inf)",
            erklaerung="$-1$, dann $:(-3)$. Beim Teilen durch eine negative Zahl kippt $\\le$ zu $\\ge$: $x \\ge -2$.",
            tipps=["Bring zuerst die $1$ nach rechts.", "$-3x \\le 6$. Wodurch teilst du jetzt?",
                   "Durch $-3$, eine negative Zahl. Was passiert mit dem Zeichen?"],
            rechenweg=r"""
            :::rechnung
            -3x + 1 \le 7 \quad | -1 || Zahl nach rechts
            -3x \le 6 \quad | :(-3) || negative Zahl: Zeichen kippt
            x \ge -2 || $\mathbb{L} = [-2, \infty)$
            :::
            """,
            typische_fehler=[("(-inf; -2]", "Das Zeichen muss kippen: Du hast durch die negative Zahl $-3$ geteilt."),
                             ("(-2; inf)", "Bei $\\ge$ gehört die $-2$ dazu: eckige Klammer.")])

k.wf("Aus $-x > 4$ folgt $x > -4$.", False,
     "Mal $(-1)$ kippt das Zeichen: $x < -4$. Probe mit $x = 0$: $-0 > 4$ ist falsch, also darf $0$ "
     "keine Lösung sein. Bei $x > -4$ wäre sie es.",
     tipps=["Du nimmst mit $-1$ mal. Was passiert mit dem Zeichen?"])

k.gleichung("2(x - 1) >= 5x + 4", loesung="(-inf; -2]",
            erklaerung="Klammer auflösen, $-5x$, $+2$, dann $:(-3)$ mit Zeichenwechsel: $x \\le -2$.",
            tipps=["Löse zuerst die Klammer auf.", "$2x - 2 \\ge 5x + 4$. Sammle die $x$-Terme.",
                   "$-3x \\ge 6$. Durch $-3$ teilen, Zeichen kippt."],
            rechenweg=r"""
            :::rechnung
            2(x - 1) \ge 5x + 4 || Aufgabe
            2x - 2 \ge 5x + 4 \quad | -5x || Klammer aufgelöst, $x$ nach links
            -3x - 2 \ge 4 \quad | +2 || Zahl nach rechts
            -3x \ge 6 \quad | :(-3) || Zeichen kippt
            x \le -2 || $\mathbb{L} = (-\infty, -2]$
            :::
            """,
            typische_fehler=[("[-2; inf)", "Beim Teilen durch $-3$ kippt das Zeichen: aus $\\ge$ wird $\\le$."),
                             ("(-inf; -2)", "Bei $\\le$ gehört die $-2$ dazu: eckige Klammer."),
                             ("(-inf; -1]", "Beim Auflösen der Klammer wurde nur $x$ malgenommen: $2(x - 1) = 2x - 2$.")])

# ── 3: Doppelungleichungen, Sonderfälle, Fallunterscheidung ────────────────
_D_LO, _D_HI = F(-1 - 3, 2), F(7 - 3, 2)
k.erklaerung("Doppelungleichungen und Sonderfälle", r"""
    ## Zwei Bedingungen auf einmal

    :::analogie 🌡️ Heizung
    Die Heizung hält die Zimmertemperatur $T$ zwischen $18$ und $22$ Grad:
    $18 \le T \le 22$. Eine Größe, zwei Grenzen gleichzeitig: Das ist eine
    [[Doppelungleichung]].
    :::

    Bei $-1 < 2x + 3 \le 7$ formst du **alle drei Teile** gleichzeitig um.

    :::rechnung Beispiel vorgerechnet
    -1 < 2x + 3 \le 7 \quad | -3 || überall $3$ abziehen
    -4 < 2x \le 4 \quad | :2 || überall durch $2$ teilen
    -2 < x \le 2 || $\mathbb{L} = (-2, 2]$
    :::

    :::visual zahlenstrahl
    {"von": -4, "bis": 4, "intervalle": [{"von": -2, "bis": 2, "von_zu": false, "bis_zu": true, "label": "(-2, 2]"}]}
    :::

    :::alt Mit zwei Ungleichungen erklärt
    $-1 < 2x + 3 \le 7$ sind zwei Ungleichungen, die beide gelten müssen:
    $-1 < 2x + 3$, also $x > -2$. Und $2x + 3 \le 7$, also $x \le 2$. Beides
    zusammen ist der Bereich zwischen $-2$ und $2$. Der Rechenweg oben macht beide
    Rechnungen in einem Durchgang.
    :::
    ---
    ## Wenn x verschwindet

    Wie bei Gleichungen kann $x$ ganz wegfallen. Dann entscheidet die übrige Aussage:
    wahr heißt $\mathbb{L} = \mathbb{R}$, falsch heißt $\mathbb{L} = \emptyset$.

    :::rechnung Immer wahr
    2x + 1 < 2x + 3 \quad | -2x || $x$ fällt weg
    1 < 3 || wahr für jedes $x$: $\mathbb{L} = \mathbb{R}$
    :::

    :::rechnung Nie wahr
    3x + 2 > 3x + 3 \quad | -3x || $x$ fällt weg
    # 2 > 3 || falsch für jedes $x$: $\mathbb{L} = \emptyset$
    :::

    :::alt Mit Wettlauf erklärt
    Zwei Läufer starten bei $1$ und bei $3$ und laufen gleich schnell ($2x$). Der
    erste holt den zweiten nie ein: $2x + 1 < 2x + 3$ gilt immer. Fragst du dagegen,
    wann der hintere vorne ist, lautet die Antwort: nie.
    :::
    ---
    ## Variable im Nenner: Fallunterscheidung

    Bei $\frac{6}{x} > 2$ möchtest du mit $x$ malnehmen. Aber kippt das Zeichen? Das
    hängt davon ab, ob $x$ positiv oder negativ ist. Also rechnest du beide Fälle
    getrennt. Das heißt [[Fallunterscheidung]]. $x = 0$ ist verboten.

    :::rechnung Fall 1: $x > 0$, Zeichen bleibt
    \frac{6}{x} > 2 \;\text{für}\; x > 0 \quad | \cdot x || Ausgangsungleichung im Fall $x > 0$
    6 > 2x \quad | :2 || mit dem positiven $x$ malgenommen: Zeichen bleibt
    x < 3 || zusammen mit $x > 0$: $(0, 3)$
    :::

    :::rechnung Fall 2: $x < 0$, Zeichen kippt
    \frac{6}{x} > 2 \;\text{für}\; x < 0 \quad | \cdot x || Ausgangsungleichung im Fall $x < 0$
    6 < 2x \quad | :2 || mit dem negativen $x$ malgenommen: Zeichen kippt
    x > 3 || aber $x < 0$ und $x > 3$ geht nicht: keine Lösung
    :::

    Also $\mathbb{L} = (0, 3)$.

    :::achtung Ohne Fallunterscheidung
    Wer einfach mit $x$ malnimmt, bekommt $x < 3$ und damit auch $x = -1$.
    Probe: $\frac{6}{-1} = -6 > 2$ ist falsch.
    :::

    :::alt Mit Vorzeichen erklärt
    Für negative $x$ ist $\frac{6}{x}$ negativ und damit nie größer als $2$. Also
    kommen nur positive $x$ in Frage. Dort kippt nichts: $6 > 2x$, also $x < 3$.
    Ergebnis: alle Zahlen zwischen $0$ und $3$.
    :::
    """)

k.loesungsmenge("Löse die Doppelungleichung $-1 < 2x + 3 \\le 7$. Gib die Lösungsmenge als Intervall an.",
                f"({mathlib.text(_D_LO)}; {mathlib.text(_D_HI)}]",
                "Überall $-3$, dann überall $:2$: $-2 < x \\le 2$, also $(-2, 2]$.",
                tipps=["Forme alle drei Teile gleichzeitig um.", "Erst überall $-3$: $-4 < 2x \\le 4$.",
                       "Dann überall durch $2$. Die Zeichen bleiben."],
                rechenweg=r"""
                :::rechnung
                -1 < 2x + 3 \le 7 \quad | -3 || überall $3$ abziehen
                -4 < 2x \le 4 \quad | :2 || überall durch $2$
                -2 < x \le 2 || also $(-2, 2]$
                :::
                """,
                typische_fehler=[("[-2; 2]", "Links steht $<$: Die $-2$ gehört nicht dazu."),
                                 ("(-2; 2)", "Rechts steht $\\le$: Die $2$ gehört dazu."),
                                 ("(-4; 4]", "Du hast vergessen, durch $2$ zu teilen: Aus $-4 < 2x \\le 4$ folgt erst nach $:2$ das Ergebnis.")])

k.gleichung("3x + 2 > 3(x + 1)", loesung="keine",
            erklaerung="$3x + 2 > 3x + 3$. Nach $-3x$ bleibt $2 > 3$, das ist nie wahr: $\\mathbb{L} = \\emptyset$.",
            tipps=["Löse die Klammer auf.", "Sammle die $x$-Terme. Was bleibt übrig?",
                   "$2 > 3$: wahr oder falsch?"],
            rechenweg=r"""
            :::rechnung
            3x + 2 > 3(x + 1) || Klammer auflösen
            3x + 2 > 3x + 3 \quad | -3x || $x$ fällt weg
            # 2 > 3 || falsch für jedes $x$: $\mathbb{L} = \emptyset$
            :::
            """,
            typische_fehler=[("R", "Übrig bleibt $2 > 3$. Das ist falsch, also erfüllt keine Zahl die Ungleichung."),
                             ("(1/2; inf)", "Beim Auflösen der Klammer wurde nur die $1$ mit $3$ malgenommen, nicht das $x$. Richtig ist $3(x + 1) = 3x + 3$, dann fällt $x$ ganz weg.")])

k.loesungsmenge("Löse $\\frac{6}{x} > 2$. Gib die Lösungsmenge an.", "(0; 3)",
                "Fallunterscheidung: Für $x > 0$ folgt $x < 3$, also $(0, 3)$. Für $x < 0$ folgt $x > 3$, Widerspruch.",
                tipps=["Darfst du einfach mit $x$ malnehmen? Was, wenn $x$ negativ ist?",
                       "Rechne die Fälle $x > 0$ und $x < 0$ getrennt.",
                       "Fall $x > 0$: $6 > 2x$. Fall $x < 0$: $6 < 2x$."],
                rechenweg=r"""
                :::rechnung Fall 1: $x > 0$
                \frac{6}{x} > 2 \;\text{für}\; x > 0 \quad | \cdot x || mit positivem $x$ malnehmen
                6 > 2x \quad | :2 || Zeichen bleibt
                x < 3 || mit $x > 0$: $(0, 3)$
                :::

                :::rechnung Fall 2: $x < 0$
                \frac{6}{x} > 2 \;\text{für}\; x < 0 \quad | \cdot x || mit negativem $x$ malnehmen
                6 < 2x \quad | :2 || Zeichen gekippt beim Malnehmen mit $x$
                x > 3 || Widerspruch zu $x < 0$
                :::

                Also $\mathbb{L} = (0, 3)$.
                """,
                typische_fehler=[("(-inf; 3)", "Du hast ohne Fallunterscheidung mit $x$ malgenommen. Probe mit $x = -1$: $-6 > 2$ ist falsch."),
                                 ("[0; 3)", "$x = 0$ ist verboten: $\\frac{6}{0}$ gibt es nicht."),
                                 ("(3; inf)", "Probe mit $x = 4$: $\\frac{6}{4} = 1{,}5 > 2$ ist falsch.")])


# ── Praxis ─────────────────────────────────────────────────────────────────
_REL_TEX = {"<": "<", "<=": "\\le", ">": ">", ">=": "\\ge"}
_KIPP = {"<": ">", "<=": ">=", ">": "<", ">=": "<="}


def _vz(z):
    return f"+ {tex(z)}" if z >= 0 else f"- {tex(-z)}"


def _lin(a, b):
    if a == 0:
        return tex(b)
    ax = "x" if a == 1 else "-x" if a == -1 else f"{a}x"
    return ax if b == 0 else f"{ax} {_vz(b)}"


def _lin_text(a, b):
    """Eingabetext für mathlib.loese."""
    return f"{a}*x + ({b})"


def _halbgerade(rel, g):
    """Lösung von x rel g als Eingabetext."""
    gt = mathlib.text(g)
    return {"<": f"(-inf; {gt})", "<=": f"(-inf; {gt}]", ">": f"({gt}; inf)", ">=": f"[{gt}; inf)"}[rel]


def _gleich_bereich(a, b):
    return pruefer.bereiche_gleich(pruefer.bereich_parsen(a, "x"), pruefer.bereich_parsen(b, "x"))


def _fehler_bereiche(loes, fehler):
    erg, gesehen = [], [loes]
    for w, m in fehler:
        if any(_gleich_bereich(w, g) for g in gesehen):
            continue
        gesehen.append(w)
        erg.append((w, m))
    return erg


def lineare_ungleichung(rng):
    while True:
        g = rng.randint(-8, 8)
        a = rng.choice([-5, -4, -3, -2, -1, 2, 3, 4, 5])
        c = rng.choice([0, 0, 0, -2, -1, 1, 2, 3])
        b = rng.choice([z for z in range(-10, 11) if z])
        m = a - c
        if m != 0 and m != 1:
            break
    rel = rng.choice(["<", "<=", ">", ">="])
    d = m * g + b
    links, rechts = _lin(a, b), _lin(c, d)
    loes_rel = rel if m > 0 else _KIPP[rel]
    loes = _halbgerade(loes_rel, F(g))
    # Gegenprobe mit mathlib.loese
    berechnet = mathlib.loese(f"{_lin_text(a, b)} {rel} {_lin_text(c, d)}")
    assert pruefer.bereiche_gleich(berechnet, pruefer.bereich_parsen(loes, "x"))
    r = _REL_TEX[rel]
    zeilen = []
    if c != 0:
        cx = "x" if abs(c) == 1 else f"{abs(c)}x"
        zeilen.append((f"{links} {r} {rechts} \\quad | {'-' if c > 0 else '+'}{cx}", "$x$-Terme nach links, Zeichen bleibt"))
    zeilen.append((f"{_lin(m, b)} {r} {tex(d)} \\quad | {'-' if b > 0 else '+'}{abs(b)}", "Zahl nach rechts, Zeichen bleibt"))
    if m > 0:
        zeilen.append((f"{m}x {r} {tex(d - b)} \\quad | :{m}", "positive Zahl: Zeichen bleibt"))
    else:
        zeilen.append((f"{_lin(m, 0)} {r} {tex(d - b)} \\quad | :({m})", "negative Zahl: Zeichen kippt"))
    zeilen.append((f"x {_REL_TEX[loes_rel]} {g}", "Ergebnis"))
    offen = {"<": "<=", "<=": "<", ">": ">=", ">=": ">"}
    fehler = [(_halbgerade(offen[loes_rel], F(g)),
               "Die Grenze stimmt. Prüfe, ob sie dazugehört: Bei $<$ und $>$ runde, bei $\\le$ und $\\ge$ eckige Klammer.")]
    if m < 0:
        fehler.insert(0, (_halbgerade(rel, F(g)), "Du hast durch eine **negative** Zahl geteilt. Dabei kippt das Zeichen."))
    else:
        fehler.insert(0, (_halbgerade(_KIPP[rel], F(g)), "Das Zeichen kippt nur bei negativen Zahlen. Hier hast du durch eine positive geteilt."))
    fehler.append((_halbgerade(loes_rel, F(d + b, m)), f"Vorzeichenfehler beim Herüberholen der Zahl: Aus ${_vz(b)}$ links wird rechts ${_vz(-b)}$."))
    return {
        "frage": f"Löse ${links} {r} {rechts}$. Gib die Lösungsmenge als Intervall an.",
        "loesung": loes,
        "tipps": ["Forme um wie bei einer Gleichung: $x$-Terme links, Zahlen rechts.",
                  f"Am Ende steht ${_lin(m, 0)} {r} {tex(d - b)}$.",
                  f"Du teilst durch ${m}$. " + ("Das ist negativ: Das Zeichen kippt." if m < 0 else "Das ist positiv: Das Zeichen bleibt.")],
        "rechenweg": _zeilen(*zeilen),
        "erklaerung": "Umformen wie bei Gleichungen. Nur beim Malnehmen oder Teilen mit einer negativen Zahl kippt das Zeichen.",
        "typische_fehler": _fehler_bereiche(loes, fehler),
    }


def doppelungleichung(rng):
    while True:
        p = rng.randint(-6, 4)
        q = p + rng.randint(1, 6)
        a = rng.choice([2, 3, 4, 5, -1, -2, -3])
        b = rng.choice([z for z in range(-8, 9) if z])
        if a != 1:
            break
    pz, qz = rng.random() < 0.5, rng.random() < 0.5            # gehören p bzw. q dazu?
    rel = {True: "\\le", False: "<"}
    if a > 0:
        lo, hi, r_lo, r_hi = a * p + b, a * q + b, rel[pz], rel[qz]
    else:                                                       # Reihenfolge dreht sich
        lo, hi, r_lo, r_hi = a * q + b, a * p + b, rel[qz], rel[pz]
    mitte = _lin(a, b)
    zeilen = [(f"{lo} {r_lo} {mitte} {r_hi} {hi} \\quad | {'-' if b > 0 else '+'}{abs(b)}", "überall die Zahl wegbringen"),
              (f"{lo - b} {r_lo} {_lin(a, 0)} {r_hi} {hi - b} \\quad | :{mathlib.tex_klammer(a)}",
               "überall teilen" + ("" if a > 0 else ": negativ, beide Zeichen kippen"))]
    kipp = {"\\le": "\\ge", "<": ">"}
    if a < 0:
        zeilen.append((f"{q} {kipp[r_lo]} x {kipp[r_hi]} {p}", "beide Zeichen gekippt"))
        zeilen.append((f"{p} {rel[pz]} x {rel[qz]} {q}", "von rechts nach links gelesen"))
    else:
        zeilen.append((f"{p} {rel[pz]} x {rel[qz]} {q}", "Ergebnis"))
    loes = f"{'[' if pz else '('}{p}; {q}{']' if qz else ')'}"
    fehler = [(f"{'(' if pz else '['}{p}; {q}{')' if qz else ']'}",
               "Die Grenzen stimmen. Prüfe, welche Ränder dazugehören: $\\le$ eckige, $<$ runde Klammer.")]
    lo_f, hi_f = F(lo, a), F(hi, a)
    u, o = min(lo_f, hi_f), max(lo_f, hi_f)
    if u != o:
        fehler.append((f"{'[' if pz else '('}{mathlib.text(u)}; {mathlib.text(o)}{']' if qz else ')'}",
                       f"Die ${b}$ in der Mitte muss zuerst auf **allen** Seiten weg, bevor du teilst."))
    return {
        "frage": f"Löse ${lo} {r_lo} {mitte} {r_hi} {hi}$. Gib die Lösungsmenge als Intervall an.",
        "loesung": loes,
        "tipps": ["Forme alle drei Teile gleichzeitig um.",
                  f"Zuerst überall ${'-' if b > 0 else '+'}{abs(b)}$: ${lo - b} {r_lo} {_lin(a, 0)} {r_hi} {hi - b}$.",
                  f"Dann überall durch ${a}$." + (" Negativ: Beide Zeichen kippen." if a < 0 else "")],
        "rechenweg": _zeilen(*zeilen) + f"\n\nAlso $\\mathbb{{L}} = {pruefer.bereich_latex(pruefer.bereich_parsen(loes, 'x'))}$.",
        "erklaerung": "Bei einer Doppelungleichung formst du alle drei Teile gleich um. Teilen durch eine negative Zahl kippt beide Zeichen.",
        "typische_fehler": _fehler_bereiche(loes, fehler),
    }


k.praxis()

k.generator(lineare_ungleichung, typ="loesungsmenge", titel="Lineare Ungleichungen")
k.generator(doppelungleichung, typ="loesungsmenge", titel="Doppelungleichungen")

_N_MAX = (20 + 7 - 1) // 3          # größtes n mit 3n - 7 < 20 ist 8
k.menge("Bestimme alle natürlichen Zahlen $n \\ge 1$ mit $3n - 7 < 20$. Gib sie als Menge an.",
        "{" + "; ".join(str(n) for n in range(1, 30) if 3 * n - 7 < 20) + "}",
        "$3n < 27$, also $n < 9$. Die natürlichen Zahlen ab $1$ darunter sind $1$ bis $8$.",
        tipps=["Löse erst die Ungleichung für $n$.", "$3n < 27$, also $n < 9$.",
               "Welche natürlichen Zahlen ab $1$ sind kleiner als $9$?"],
        rechenweg=r"""
        :::rechnung
        3n - 7 < 20 \quad | +7 || Zahl nach rechts
        3n < 27 \quad | :3 || positive Zahl: Zeichen bleibt
        n < 9 || $9$ selbst gehört nicht dazu
        :::

        Also $n \in \{1, 2, \ldots, 8\}$.
        """,
        typische_fehler=[("{1; 2; 3; 4; 5; 6; 7; 8; 9}", "Bei $n < 9$ ist die $9$ nicht dabei: $3 \\cdot 9 - 7 = 20$ ist nicht kleiner als $20$.")])

# Übungsblatt-Stil: Bruchungleichung mit Fallunterscheidung
k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: Ungleichung mit Fallunterscheidung

    Bestimmen Sie die Menge aller $x \in \mathbb{R} \setminus \{-1\}$ mit
    $$\frac{2x - 1}{x + 1} \le 1.$$
    Unterscheiden Sie die Fälle $x + 1 > 0$ und $x + 1 < 0$.
    """,
    [{"typ": "loesungsmenge",
      "frage": "Fall 1: $x > -1$. Nimm mit $x + 1$ mal (positiv, Zeichen bleibt) und löse. "
               "Welche $x$ mit $x > -1$ erfüllen die Ungleichung?",
      "loesung": "(-1; 2]",
      "tipps": ["$2x - 1 \\le x + 1$.", "Das ergibt $x \\le 2$. Schneide mit $x > -1$."],
      "rechenweg": "$2x - 1 \\le x + 1 \\Leftrightarrow x \\le 2$. Zusammen mit $x > -1$: $(-1, 2]$.",
      "typische_fehler": [("(-inf; 2]", "Im Fall 1 gilt zusätzlich $x > -1$. Schneide die Bereiche."),
                          ("[-1; 2]", "$x = -1$ ist verboten: Der Nenner wäre $0$.")]},
     {"typ": "loesungsmenge",
      "frage": "Fall 2: $x < -1$. Jetzt ist $x + 1$ negativ. Welche $x$ mit $x < -1$ erfüllen die Ungleichung?",
      "loesung": "keine",
      "tipps": ["Beim Malnehmen mit $x + 1 < 0$ kippt das Zeichen: $2x - 1 \\ge x + 1$.",
                "Das ergibt $x \\ge 2$. Passt das zu $x < -1$?"],
      "rechenweg": "$2x - 1 \\ge x + 1 \\Leftrightarrow x \\ge 2$. Das widerspricht $x < -1$: keine Lösung.",
      "typische_fehler": [("[2; inf)", "Im Fall 2 gilt $x < -1$. Die Zahlen ab $2$ gehören nicht dazu."),
                          ("(-inf; -1)", "Probe mit $x = -2$: $\\frac{-5}{-1} = 5 \\le 1$ ist falsch.")]},
     {"typ": "loesungsmenge", "frage": "Gib die gesamte Lösungsmenge an.", "loesung": "(-1; 2]",
      "tipps": ["Vereinige die Ergebnisse beider Fälle.", "Fall 2 liefert nichts."],
      "rechenweg": "$\\mathbb{L} = (-1, 2] \\cup \\emptyset = (-1, 2]$",
      "typische_fehler": [("(-inf; 2]", "Ohne Fallunterscheidung kommt zu viel heraus. Probe mit $x = -2$: $5 \\le 1$ ist falsch.")]}],
    "Mit einem Term malnehmen, dessen Vorzeichen man nicht kennt, erfordert eine Fallunterscheidung. "
    "Jeder Fall liefert einen Teil der Lösung; am Ende werden sie vereinigt.",
    uebungsblatt=True,
    tipps=["Wann ist $x + 1$ positiv, wann negativ?", "Im negativen Fall kippt das Zeichen."],
    rechenweg=r"""
    **Fall 1:** $x > -1$, also $x + 1 > 0$. Mal $(x + 1)$, Zeichen bleibt:

    :::rechnung
    2x - 1 \le x + 1 \quad | -x + 1 || $x$ nach links, Zahl nach rechts
    x \le 2 || zusammen mit $x > -1$: $(-1, 2]$
    :::

    **Fall 2:** $x < -1$, also $x + 1 < 0$. Mal $(x + 1)$, Zeichen kippt:

    :::rechnung
    2x - 1 \ge x + 1 \quad | -x + 1 || $x$ nach links, Zahl nach rechts
    x \ge 2 || Widerspruch zu $x < -1$: keine Lösung
    :::

    Also $\mathbb{L} = (-1, 2]$.
    """)

k.zusammenfassung(r"""
    ## Ungleichungen

    | Umformung | Zeichen |
    |---|---|
    | auf beiden Seiten $+$ oder $-$ | bleibt |
    | mal oder geteilt durch eine positive Zahl | bleibt |
    | mal oder geteilt durch eine negative Zahl | **kippt**: $<$ wird $>$, $\le$ wird $\ge$ |
    | mal einen Term mit unbekanntem Vorzeichen | Fallunterscheidung |

    !! Negative Zahl beim Malnehmen oder Teilen: Zeichen umdrehen.

    | Ungleichung | Intervall |
    |---|---|
    | $x < a$ | $(-\infty, a)$ |
    | $x \ge a$ | $[a, \infty)$ |
    | $a < x \le b$ | $(a, b]$ |

    - Eckige Klammer: Rand gehört dazu. Runde Klammer: Rand gehört nicht dazu. Bei $\infty$ immer rund.
    - $x$ fällt weg: wahre Aussage $\mathbb{L} = \mathbb{R}$, falsche Aussage $\mathbb{L} = \emptyset$.
""")
