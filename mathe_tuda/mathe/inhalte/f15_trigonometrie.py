# -*- coding: utf-8 -*-
"""Fundament 15: Trigonometrie und Bogenmaß – sin, cos, tan im Dreieck und am Einheitskreis."""
from fractions import Fraction as F

from .. import mathlib, pruefer
from ..engine import neues_kapitel, ohne_gleiche

tex = mathlib.tex

k = neues_kapitel(
    slug="trigonometrie",
    titel="Trigonometrie und Bogenmaß",
    beschreibung="Sinus, Kosinus und Tangens im Dreieck und am Einheitskreis, Bogenmaß, wichtige Werte, sin² + cos² = 1",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="📐")

k.lernziele([
    "Ich kann Sinus, Kosinus und Tangens im rechtwinkligen Dreieck als Seitenverhältnisse berechnen",
    "Ich kann Winkel zwischen Grad und Bogenmaß umrechnen, zum Beispiel $60^\\circ = \\frac{\\pi}{3}$",
    "Ich kann $\\cos(\\varphi)$ und $\\sin(\\varphi)$ als Koordinaten am Einheitskreis ablesen und kenne die wichtigen Werte",
    "Ich kann mit $\\sin^2(\\varphi) + \\cos^2(\\varphi) = 1$ aus dem Sinus den Kosinus berechnen",
])

k.warum(r"""
Jedes Spiel und jedes Grafikprogramm dreht Figuren. Ein Punkt $(x \mid y)$, um den
Winkel $\varphi$ gedreht, landet bei $(x\cos\varphi - y\sin\varphi \mid x\sin\varphi + y\cos\varphi)$:
Das ist die Drehmatrix aus Mathe 1. Töne und Funksignale sind Sinuskurven, die
Fourierreihen in Mathe 2 setzen jedes Signal daraus zusammen. Und `math.sin` in Python
rechnet im **Bogenmaß**, nicht in Grad. Wer das vergisst, bekommt Unsinn.
""")

# ── 1: Dreieck ─────────────────────────────────────────────────────────────
k.erklaerung("Sinus, Kosinus und Tangens im Dreieck", r"""
    ## Seitenverhältnisse

    :::analogie 🪜 Leiter an der Wand
    Lehnst du eine Leiter steiler an, reicht sie höher hinauf. Wie hoch sie im
    Verhältnis zu ihrer Länge reicht, hängt nur vom Winkel ab.
    :::

    Im rechtwinkligen Dreieck liegt die längste Seite, die [[Hypotenuse]], gegenüber
    dem rechten Winkel. Für einen spitzen Winkel $\alpha$ gibt es die
    **Gegenkathete** (gegenüber von $\alpha$) und die **Ankathete** (liegt an $\alpha$).
    Ihre Verhältnisse heißen [[Sinus]], [[Kosinus]] und [[Tangens]]:

    $$\sin(\alpha) = \frac{\text{Gegenkathete}}{\text{Hypotenuse}},\quad \cos(\alpha) = \frac{\text{Ankathete}}{\text{Hypotenuse}},\quad \tan(\alpha) = \frac{\text{Gegenkathete}}{\text{Ankathete}}$$

    :::rechnung Dreieck mit Gegenkathete $3$, Ankathete $4$, Hypotenuse $5$
    \frac{3}{5} = 0{,}6 || $\sin(\alpha)$
    \frac{4}{5} = 0{,}8 || $\cos(\alpha)$
    \frac{3}{4} = 0{,}75 || $\tan(\alpha)$
    :::

    :::alt Mit Schatten erklärt
    Zwei Stäbe, $1$ m und $2$ m lang, werfen zur selben Uhrzeit Schatten. Der lange
    Schatten ist doppelt so lang, das Verhältnis Stab zu Schatten ist gleich. Bei
    gleichem Winkel haben alle rechtwinkligen Dreiecke dieselben Seitenverhältnisse.
    Diese Verhältnisse bekommen Namen: Sinus, Kosinus, Tangens.
    :::
    """)

k.zahl("In einem rechtwinkligen Dreieck ist die Gegenkathete von $\\alpha$ genau $5$ lang, die Hypotenuse $13$. "
       "Berechne $\\sin(\\alpha)$.", F(5, 13),
       "$\\sin(\\alpha) = \\frac{\\text{Gegenkathete}}{\\text{Hypotenuse}} = \\frac{5}{13}$.",
       tipps=["Sinus: Gegenkathete durch Hypotenuse.", "Oben $5$, unten $13$.", "$\\frac{5}{13}$"],
       rechenweg=r"""
       :::rechnung
       \frac{5}{13} || Gegenkathete durch Hypotenuse
       :::
       """,
       typische_fehler=[(F(13, 5), "Kehrwert: Die Hypotenuse gehört in den Nenner. Ein Sinus ist nie größer als $1$."),
                        (F(12, 13), "Das ist der Kosinus: Ankathete $12$ durch Hypotenuse.")])

k.zahl("In einem rechtwinkligen Dreieck ist die Gegenkathete von $\\alpha$ genau $6$ lang und die Ankathete $8$. "
       "Berechne $\\tan(\\alpha)$.", F(6, 8),
       "$\\tan(\\alpha) = \\frac{6}{8} = \\frac{3}{4}$.",
       tipps=["Tangens: Gegenkathete durch Ankathete.", "$\\frac{6}{8}$", "Kürzen mit $2$."],
       rechenweg=r"""
       :::rechnung
       \frac{6}{8} = \frac{3}{4} || Gegenkathete durch Ankathete, gekürzt
       :::
       """,
       typische_fehler=[(F(4, 3), "Kehrwert: Die Gegenkathete gehört in den Zähler."),
                        (F(6, 10), "Das ist der Sinus. Die Hypotenuse wäre $10$, aber der Tangens braucht sie nicht.")])

# ── 2: Bogenmaß ────────────────────────────────────────────────────────────
k.erklaerung("Bogenmaß", r"""
    ## Winkel als Länge

    :::analogie 🧵 Faden um eine Dose
    Leg einen Faden entlang einer runden Dose mit Radius $1$. Wie viel Faden du für
    einen Winkel brauchst, misst den Winkel.
    :::

    Der [[Einheitskreis]] hat Radius $1$, also Umfang $2\pi$. Das [[Bogenmaß]] eines
    Winkels ist die Länge des Bogens, den er aus dem Einheitskreis schneidet. Ein
    voller Kreis, $360^\circ$, ist $2\pi$; ein halber, $180^\circ$, ist $\pi$.

    $$x = \frac{\alpha}{180^\circ} \cdot \pi$$

    :::rechnung Grad in Bogenmaß
    \frac{90}{180} \cdot \pi = \frac{\pi}{2} || $90^\circ$
    \frac{60}{180} \cdot \pi = \frac{\pi}{3} || $60^\circ$
    :::

    :::visual einheitskreis
    {"winkel": 60, "bogenmass": true, "zeige": [], "regler": true,
     "unterschrift": "Der Winkel im Bogenmaß ist die Länge des Kreisbogens von $(1 \\mid 0)$ bis zum Punkt."}
    :::

    :::achtung DEG oder RAD
    $\sin(30)$ heißt in der Uni-Mathematik: $30$ im Bogenmaß, fast fünf volle Umdrehungen ($30 : 2\pi \approx 4{,}8$).
    Taschenrechner auf RAD stellen. Python, Java und C rechnen immer im Bogenmaß.
    :::

    :::alt Mit Pizzastücken erklärt
    Eine Pizza mit Radius $1$ hat einen Rand der Länge $2\pi \approx 6{,}28$. Ein
    Viertel der Pizza hat den Rand $\frac{2\pi}{4} = \frac{\pi}{2}$. Statt „$90$ Grad“
    sagst du: Das Stück hat $\frac{\pi}{2}$ Rand.
    :::
    """)

k.zahl("Rechne $60^\\circ$ ins Bogenmaß um. Tippe zum Beispiel `pi/4`.", "pi/3",
       "$\\frac{60}{180} \\cdot \\pi = \\frac{\\pi}{3}$.",
       tipps=["Teile durch $180$ und nimm mal $\\pi$.", "$\\frac{60}{180} = \\frac{1}{3}$", "$\\frac{1}{3} \\cdot \\pi$"],
       rechenweg=r"""
       :::rechnung
       \frac{60}{180} \cdot \pi = \frac{1}{3} \cdot \pi || kürzen
       = \frac{\pi}{3} || fertig
       :::
       """,
       typische_fehler=[("pi/6", "Du hast durch $360$ geteilt. $360^\\circ$ sind $2\\pi$, also teilt man durch $180$ und nimmt mal $\\pi$."),
                        ("3pi", "Kehrwert: Es heißt $\\frac{60}{180}$, nicht $\\frac{180}{60}$.")])

k.zahl("Rechne $\\frac{3\\pi}{4}$ in Grad um.", 135,
       "$\\frac{3}{4} \\cdot 180^\\circ = 135^\\circ$.", einheit="°",
       tipps=["$\\pi$ entspricht $180^\\circ$.", "Ersetze $\\pi$ durch $180$.", "$\\frac{3 \\cdot 180}{4}$"],
       rechenweg=r"""
       :::rechnung
       \frac{3\pi}{4} \cdot \frac{180}{\pi} = \frac{3 \cdot 180}{4} || $\pi$ kürzt sich weg
       = 135 || also $135^\circ$
       :::
       """,
       typische_fehler=[(270, "Du hast $\\pi$ als $360^\\circ$ gerechnet. Ein halber Kreis, $\\pi$, sind $180^\\circ$."),
                        (240, "Kehrwert: $\\frac{4}{3} \\cdot 180 = 240$. Es heißt $\\frac{3}{4}$."),
                        ("3pi/4", "Das ist noch das Bogenmaß. Gesucht sind Grad: Ersetze $\\pi$ durch $180^\\circ$.")])

# ── 3: Einheitskreis ───────────────────────────────────────────────────────
k.erklaerung("Der Einheitskreis", r"""
    ## sin und cos als Koordinaten

    Lauf auf dem Einheitskreis vom Punkt $(1 \mid 0)$ gegen den Uhrzeigersinn den Winkel
    $\varphi$ entlang. Du landest im Punkt

    $$P = (\cos(\varphi) \mid \sin(\varphi)).$$

    So sind Sinus und Kosinus für **jeden** Winkel erklärt, auch über $90^\circ$
    hinaus. Links von der $y$-Achse ist der Kosinus negativ, unter der $x$-Achse der Sinus.

    :::visual einheitskreis
    {"winkel": 120, "zeige": ["sin", "cos"], "regler": true, "bogenmass": true,
     "unterschrift": "Bei $120^\\circ$ liegt der Punkt links oben: $\\cos$ negativ, $\\sin$ positiv."}
    :::

    :::rechnung Ein halber Kreis: $\varphi = \pi$
    \cos(\pi) = -1 || der Punkt liegt bei $(-1 \mid 0)$
    \sin(\pi) = 0 || auf der $x$-Achse, Höhe $0$
    :::

    :::alt Mit einem Riesenrad erklärt
    Du sitzt in einem Riesenrad mit Radius $1$, die Achse ist der Ursprung. Der Sinus
    ist deine Höhe über der Achse, der Kosinus dein Abstand nach rechts. Ganz oben
    bist du bei $\sin = 1$, $\cos = 0$. Auf der linken Seite ist dein Kosinus negativ.
    :::
    ---
    ## Wichtige Werte

    | $\varphi$ | $0$ | $\frac{\pi}{6}$ | $\frac{\pi}{4}$ | $\frac{\pi}{3}$ | $\frac{\pi}{2}$ |
    |---|---|---|---|---|---|
    | Grad | $0^\circ$ | $30^\circ$ | $45^\circ$ | $60^\circ$ | $90^\circ$ |
    | $\sin(\varphi)$ | $0$ | $\frac{1}{2}$ | $\frac{\sqrt{2}}{2}$ | $\frac{\sqrt{3}}{2}$ | $1$ |
    | $\cos(\varphi)$ | $1$ | $\frac{\sqrt{3}}{2}$ | $\frac{\sqrt{2}}{2}$ | $\frac{1}{2}$ | $0$ |

    Der [[Tangens]] ist $\tan(\varphi) = \frac{\sin(\varphi)}{\cos(\varphi)}$. Bei
    $\frac{\pi}{2}$ ist er nicht definiert.

    :::rechnung Zwei Werte nachgerechnet
    \sin\left(\frac{\pi}{6}\right) = \frac{1}{2} || $30^\circ$
    \tan\left(\frac{\pi}{4}\right) = \frac{\sqrt{2}/2}{\sqrt{2}/2} = 1 || Sinus und Kosinus gleich
    :::

    :::alt Mit einem Zählmuster erklärt
    Schreib die Sinuswerte so: $\frac{\sqrt{0}}{2}, \frac{\sqrt{1}}{2}, \frac{\sqrt{2}}{2},
    \frac{\sqrt{3}}{2}, \frac{\sqrt{4}}{2}$. Unter der Wurzel zählst du $0, 1, 2, 3, 4$.
    Der Kosinus ist dieselbe Reihe rückwärts.
    :::
    ---
    ## Spiegeln am Einheitskreis

    Für Winkel außerhalb des ersten Viertels brauchst du keine neue Tabelle. Miss den
    **Bezugswinkel**, den Abstand des Punkts zur $x$-Achse: bei $150^\circ$ sind es
    $180^\circ - 150^\circ = 30^\circ$. Der Betrag des Werts ist der von $30^\circ$, das
    Vorzeichen liest du an der Lage ab.

    :::visual einheitskreis
    {"winkel": 150, "zeige": ["sin", "cos"], "regler": true, "bogenmass": true,
     "unterschrift": "Der Punkt zu $150^\\circ$ ist das Spiegelbild des Punkts zu $30^\\circ$ an der $y$-Achse."}
    :::

    :::rechnung $\varphi = \frac{5\pi}{6}$, also $150^\circ$, links oben
    \cos\left(\frac{5\pi}{6}\right) = -\cos\left(\frac{\pi}{6}\right) = -\frac{\sqrt{3}}{2} || links: $x$ negativ
    \sin\left(\frac{5\pi}{6}\right) = \sin\left(\frac{\pi}{6}\right) = \frac{1}{2} || oben: $y$ positiv
    :::

    :::alt Mit einem Spiegel erklärt
    Stell einen Spiegel auf die $y$-Achse. Der Punkt bei $30^\circ$, $\left(\frac{\sqrt{3}}{2} \mid \frac{1}{2}\right)$,
    erscheint im Spiegel bei $150^\circ$. Spiegeln ändert nur das Vorzeichen von $x$:
    $\left(-\frac{\sqrt{3}}{2} \mid \frac{1}{2}\right)$. Ein Spiegel an der $x$-Achse ändert das Vorzeichen von $y$.
    :::
    """)

_KREIS = {"funktionen": [{"term": "sqrt(1 - x^2)", "label": "y"}, {"term": "-sqrt(1 - x^2)", "label": "y"}],
          "x": [-1.5, 1.5], "y": [-1.5, 1.5], "gleiche_achsen": True}

k.graph_punkt("Setze auf dem Einheitskreis den Punkt zum Winkel $\\varphi = \\pi$.", _KREIS,
              modus="setzen", ziel=(-1, 0),
              erklaerung="$\\pi$ ist ein halber Kreis. Von $(1 \\mid 0)$ aus landest du gegenüber bei $(\\cos(\\pi) \\mid \\sin(\\pi)) = (-1 \\mid 0)$.",
              tipps=["Starte bei $(1 \\mid 0)$ und lauf gegen den Uhrzeigersinn.", "$\\pi$ entspricht $180^\\circ$, ein halber Kreis.",
                     "Der Punkt ist $(\\cos(\\pi) \\mid \\sin(\\pi))$."],
              rechenweg=r"""
              :::rechnung
              \cos(\pi) = -1 || $x$-Koordinate
              \sin(\pi) = 0 || $y$-Koordinate
              :::
              """,
              typische_fehler=[((0, 1), "Das ist $\\frac{\\pi}{2}$, ein Viertelkreis. $\\pi$ ist ein **halber** Kreis."),
                               ((1, 0), "Das ist der Startpunkt ($\\varphi = 0$). Lauf einen halben Kreis weiter.")])

k.wf("$\\cos\\left(\\frac{2\\pi}{3}\\right)$ ist negativ.", True,
     "$\\frac{2\\pi}{3} = 120^\\circ$. Der Punkt liegt links von der $y$-Achse, also ist der Kosinus negativ: $\\cos\\left(\\frac{2\\pi}{3}\\right) = -\\frac{1}{2}$.",
     tipps=["Rechne in Grad um und überlege, wo der Punkt auf dem Kreis liegt."])

k.mc("Welchen Wert hat $\\cos\\left(\\frac{\\pi}{3}\\right)$?",
     ["$\\frac{1}{2}$", "$\\frac{\\sqrt{3}}{2}$", "$\\frac{\\sqrt{2}}{2}$", "$1$"],
     "$\\frac{\\pi}{3} = 60^\\circ$, und $\\cos(60^\\circ) = \\frac{1}{2}$.",
     tipps=["$\\frac{\\pi}{3}$ sind $60^\\circ$.", "Der Kosinus ist die Sinusreihe rückwärts."],
     fehler={"$\\frac{\\sqrt{3}}{2}$": "Das ist $\\sin\\left(\\frac{\\pi}{3}\\right)$. Beim Kosinus läuft die Reihe rückwärts: $\\cos(60^\\circ) = \\frac{1}{2}$."})

# ── 4: Pythagoras ──────────────────────────────────────────────────────────
k.erklaerung("Der trigonometrische Pythagoras", r"""
    ## sin² + cos² = 1

    Der Punkt $(\cos(\varphi) \mid \sin(\varphi))$ liegt auf dem Kreis mit Radius $1$.
    Nach dem Satz des Pythagoras gilt deshalb für **jeden** Winkel:

    $$\sin^2(\varphi) + \cos^2(\varphi) = 1$$

    Dabei heißt $\sin^2(\varphi)$ dasselbe wie $(\sin(\varphi))^2$.

    :::rechnung Probe mit $\varphi = \frac{\pi}{6}$
    \left(\frac{1}{2}\right)^2 + \left(\frac{\sqrt{3}}{2}\right)^2 = \frac{1}{4} + \frac{3}{4} || einsetzen und quadrieren
    = 1 || stimmt
    :::

    :::achtung Wo das Quadrat hingehört
    $\sin^2(x)$ ist $(\sin(x))^2$, **nicht** $\sin(x^2)$. Und aus $\sin^2 + \cos^2 = 1$
    folgt **nicht** $\sin + \cos = 1$: Bei $\frac{\pi}{4}$ ist die Summe $\sqrt{2}$.
    :::

    :::alt Mit einem Dreieck im Kreis erklärt
    Zeichne vom Kreispunkt eine senkrechte Linie zur $x$-Achse. Es entsteht ein
    rechtwinkliges Dreieck: waagerecht $\cos(\varphi)$, senkrecht $\sin(\varphi)$,
    schräg der Radius $1$. Pythagoras: Kathete² plus Kathete² gleich Hypotenuse²,
    also $\cos^2 + \sin^2 = 1^2$.
    :::
    """)

k.zahl("Der Winkel $\\alpha$ ist spitz, und $\\sin(\\alpha) = 0{,}6$. Berechne $\\cos(\\alpha)$.", F(4, 5),
       "$\\cos^2(\\alpha) = 1 - 0{,}36 = 0{,}64$. Weil $\\alpha$ spitz ist, ist $\\cos(\\alpha) > 0$, also $0{,}8$.",
       tipps=["Nutze $\\sin^2 + \\cos^2 = 1$.", "$\\cos^2(\\alpha) = 1 - 0{,}6^2$", "$\\sqrt{0{,}64}$"],
       rechenweg=r"""
       :::rechnung
       1 - 0{,}6^2 = 1 - 0{,}36 = 0{,}64 || $\cos^2(\alpha)$
       \sqrt{0{,}64} = 0{,}8 || spitzer Winkel: positiv
       :::
       """,
       typische_fehler=[(F(2, 5), "Du hast $1 - 0{,}6$ gerechnet. Die Gleichung gilt für die **Quadrate**."),
                        (F(16, 25), "Das ist $\\cos^2(\\alpha)$. Jetzt noch die Wurzel ziehen."),
                        (F(-4, 5), "Der Winkel ist spitz, also liegt der Punkt rechts oben: $\\cos(\\alpha) > 0$.")])

k.wf("$\\sin^2(x)$ bedeutet $\\sin(x^2)$.", False,
     "Nein. $\\sin^2(x) = (\\sin(x))^2$: Erst den Sinus, dann quadrieren.",
     tipps=["Die $2$ steht am $\\sin$, nicht am $x$."])

# ── 5: Graphen ─────────────────────────────────────────────────────────────
k.erklaerung("Sinus und Kosinus als Funktionen", r"""
    ## Die Wellen

    Trägst du den Sinus über dem Winkel $x$ auf, entsteht eine Welle. Nach einer
    vollen Runde, $2\pi$, wiederholt sich alles. Sinus und Kosinus haben die
    [[Periode|periodische Funktion]] $2\pi$:

    $$\sin(x + 2\pi) = \sin(x), \qquad \cos(x + 2\pi) = \cos(x)$$

    Die Werte bleiben zwischen $-1$ und $1$. Die Kosinuswelle ist die Sinuswelle,
    um $\frac{\pi}{2}$ nach links verschoben.

    :::visual funktionsgraph
    {"funktionen": [{"term": "sin(x)", "label": "\\sin(x)"}, {"term": "cos(x)", "label": "\\cos(x)"}],
     "x": [-7, 7], "y": [-1.5, 1.5],
     "unterschrift": "Beide Wellen wiederholen sich alle $2\\pi \\approx 6{,}28$."}
    :::

    :::rechnung Eine Runde weiter
    \sin\left(\frac{\pi}{2} + 2\pi\right) = \sin\left(\frac{\pi}{2}\right) = 1 || $2\pi$ ändert nichts
    :::

    :::alt Mit dem Riesenrad über die Zeit erklärt
    Schreib jede Sekunde deine Höhe im Riesenrad auf und zeichne sie über der Zeit.
    Hoch, runter, hoch, runter: eine Welle. Nach einer vollen Umdrehung beginnt
    alles von vorn. Das ist die Periode.
    :::
    """)

k.zahl("Welche Periode hat die Sinusfunktion? Gib sie im Bogenmaß an, zum Beispiel `3pi`.", "2pi",
       "Nach einer vollen Runde, $2\\pi$ im Bogenmaß, wiederholt sich der Sinus.",
       tipps=["Eine volle Runde im Kreis.", "$360^\\circ$ im Bogenmaß.", "$2\\pi$"],
       rechenweg=r"""
       :::rechnung
       \frac{360}{180} \cdot \pi = 2\pi || eine volle Runde
       :::
       """,
       typische_fehler=[(360, "Richtig gedacht, aber in Grad. Gesucht ist das Bogenmaß: $2\\pi$."),
                        ("pi", "Nach $\\pi$ hat der Sinus das umgekehrte Vorzeichen: $\\sin\\left(\\frac{\\pi}{2} + \\pi\\right) = -1$. Erst nach $2\\pi$ wiederholt er sich.")])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


def _winkel(g):
    """Grad -> (TeX im Bogenmaß, Eingabetext)."""
    q = F(g, 180)
    if q == 0:
        return "0", "0"
    z, n = q.numerator, q.denominator
    zt = "\\pi" if z == 1 else f"{z}\\pi"
    tt = "pi" if z == 1 else f"{z}pi"
    if n == 1:
        return zt, tt
    return f"\\frac{{{zt}}}{{{n}}}", f"{tt}/{n}"


_SIN_Q1 = {0: "0", 30: "1/2", 45: "sqrt(2)/2", 60: "sqrt(3)/2", 90: "1"}
_TAN_Q1 = {0: "0", 30: "sqrt(3)/3", 45: "1", 60: "sqrt(3)"}


def _neg(t):
    return "0" if t == "0" else (t[1:] if t.startswith("-") else "-" + t)


def _sin_text(g):
    g %= 360
    if g <= 90:
        return _SIN_Q1[g]
    if g <= 180:
        return _SIN_Q1[180 - g]
    if g <= 270:
        return _neg(_SIN_Q1[g - 180])
    return _neg(_SIN_Q1[360 - g])


def _cos_text(g):
    return _sin_text(90 - g)


def _tan_text(g):
    g %= 180
    return _TAN_Q1[g] if g < 90 else _neg(_TAN_Q1[180 - g])


def _wert_tex(t):
    if t.startswith("-"):
        return "-" + pruefer.parse(t[1:]).latex()
    return pruefer.parse(t).latex()


def grad_bogen(rng):
    g = rng.choice([30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360])
    wt, wtext = _winkel(g)
    if rng.random() < 0.5:
        fehler = [(f"{g}pi/360", "Du hast durch $360$ geteilt. $180^\\circ$ entsprechen $\\pi$, also teilt man durch $180$."),
                  (f"180pi/{g}", f"Kehrwert: Es heißt $\\frac{{{g}}}{{180}} \\cdot \\pi$, nicht $\\frac{{180}}{{{g}}} \\cdot \\pi$."),
                  (f"{g}/180", "Das $\\pi$ fehlt: Nach dem Teilen durch $180$ wird mit $\\pi$ malgenommen.")]
        return {
            "frage": f"Rechne ${g}^\\circ$ ins Bogenmaß um. Tippe zum Beispiel `3pi/4`.",
            "loesung": wtext,
            "tipps": ["$180^\\circ$ entsprechen $\\pi$.", f"Rechne $\\frac{{{g}}}{{180}} \\cdot \\pi$.",
                      f"$\\frac{{{g}}}{{180}} = {tex(F(g, 180))}$"],
            "rechenweg": _zeilen((f"\\frac{{{g}}}{{180}} \\cdot \\pi = {wt}", "durch $180$ teilen, mal $\\pi$, kürzen")),
            "erklaerung": "Grad in Bogenmaß: $x = \\frac{\\alpha}{180^\\circ} \\cdot \\pi$.",
            "typische_fehler": ohne_gleiche(wtext, fehler),
        }
    fehler = [(2 * g, "Du hast $\\pi$ als $360^\\circ$ gerechnet. Ein halber Kreis, $\\pi$, sind $180^\\circ$."),
              (F(g, 2), "Du hast $\\pi$ als $90^\\circ$ gerechnet. $\\pi$ entspricht $180^\\circ$."),
              (F(g, 180) * F(314, 100),
               "Du hast nur $\\pi \\approx 3{,}14$ eingesetzt. Für Grad ersetzt man $\\pi$ durch $180^\\circ$.")]
    return {
        "frage": f"Rechne ${wt}$ in Grad um.",
        "loesung": g, "einheit": "°",
        "tipps": ["$\\pi$ entspricht $180^\\circ$.", "Ersetze $\\pi$ durch $180$.",
                  f"${wt} \\cdot \\frac{{180}}{{\\pi}}$"],
        "rechenweg": _zeilen((f"{wt} \\cdot \\frac{{180}}{{\\pi}} = {g}", "$\\pi$ kürzt sich, es bleiben Grad")),
        "erklaerung": "Bogenmaß in Grad: $\\alpha = \\frac{x}{\\pi} \\cdot 180^\\circ$.",
        "typische_fehler": ohne_gleiche(g, fehler),
    }


k.praxis()

k.generator(grad_bogen, typ="zahl", titel="Grad und Bogenmaß")


def exakter_wert(rng):
    while True:
        g = rng.choice([0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330])
        fn = rng.choice(["sin", "cos", "cos", "sin", "tan"])
        if not (fn == "tan" and g % 90 == 0) and not (g == 0 and fn != "cos"):
            break
    wt, _ = _winkel(g)
    wert = {"sin": _sin_text, "cos": _cos_text, "tan": _tan_text}[fn](g)
    arg = f"\\left({wt}\\right)"
    achsen = {0: ("(1 \\mid 0)", "auf der positiven $x$-Achse"), 90: ("(0 \\mid 1)", "auf der positiven $y$-Achse"),
              180: ("(-1 \\mid 0)", "auf der negativen $x$-Achse"), 270: ("(0 \\mid -1)", "auf der negativen $y$-Achse")}
    if g in achsen:
        punkt, wo = achsen[g]
        lage = f"Punkt ${punkt}$ {wo}"
        zeilen = [(f"\\{fn}{arg} = {_wert_tex(wert)}", f"${wt} = {g}^\\circ$: {lage}")]
        tipp2 = f"Der Punkt zu ${g}^\\circ$ ist ${punkt}$: Lies $x$ (Kosinus) und $y$ (Sinus) ab."
    else:
        quadrant = ("rechts oben" if g < 90 else "links oben" if g < 180 else "links unten" if g < 270 else "rechts unten")
        r = g if g < 90 else 180 - g if g < 180 else g - 180 if g < 270 else 360 - g
        rt, _ = _winkel(r)
        lage = f"Punkt {quadrant}"
        if r == g:
            zeilen = [(f"\\{fn}{arg} = {_wert_tex(wert)}", f"${wt} = {g}^\\circ$, Punkt rechts oben: Wert aus der Tabelle")]
            tipp2 = "Der Winkel liegt im ersten Viertel: Der Wert steht direkt in der Tabelle."
        else:
            neg = wert.startswith("-")
            zeilen = [(f"\\{fn}{arg} = {'-' if neg else ''}\\{fn}\\left({rt}\\right) = {_wert_tex(wert)}",
                       f"${wt} = {g}^\\circ$, Punkt {quadrant}; Bezugswinkel ${r}^\\circ$ zur $x$-Achse, "
                       f"Vorzeichen {'minus' if neg else 'plus'}")]
            tipp2 = (f"Der Punkt liegt {quadrant}. Sein Bezugswinkel zur $x$-Achse ist ${r}^\\circ$: "
                     f"Nimm den Wert von ${r}^\\circ$ und bestimme das Vorzeichen aus der Lage.")
    fehler = []
    if fn in ("sin", "cos"):
        anderer = _cos_text(g) if fn == "sin" else _sin_text(g)
        fehler.append((anderer, "Das ist der Wert von $\\" + ("cos" if fn == "sin" else "sin") + "$. "
                       "Der Sinus ist die Höhe ($y$), der Kosinus die $x$-Koordinate."))
    if wert != "0":
        fehler.append((_neg(wert), f"Das Vorzeichen stimmt nicht. Zu ${g}^\\circ$ gehört der {lage}."))
    if fn == "tan" and wert not in ("0",):
        fehler.append(("1/(" + wert + ")", "Kehrwert: $\\tan = \\frac{\\sin}{\\cos}$, nicht $\\frac{\\cos}{\\sin}$."))
    return {
        "frage": f"Gib den exakten Wert an: $\\{fn}{arg}$. Tippe zum Beispiel `sqrt(3)/2` oder `-1/2`.",
        "loesung": wert,
        "tipps": [f"Rechne in Grad um: ${wt} = {g}^\\circ$.", tipp2,
                  "Merkreihe für den Sinus: $\\frac{\\sqrt{0}}{2}, \\frac{\\sqrt{1}}{2}, \\frac{\\sqrt{2}}{2}, \\frac{\\sqrt{3}}{2}, \\frac{\\sqrt{4}}{2}$."
                  + (" Tangens: $\\frac{\\sin}{\\cos}$." if fn == "tan" else "")],
        "rechenweg": _zeilen(*zeilen),
        "erklaerung": "Am Einheitskreis: $\\cos$ ist die $x$-, $\\sin$ die $y$-Koordinate, $\\tan = \\frac{\\sin}{\\cos}$. "
                      "Außerhalb des ersten Viertels: Wert des Bezugswinkels nehmen, Vorzeichen aus der Lage.",
        "typische_fehler": ohne_gleiche(wert, fehler),
    }


k.generator(exakter_wert, typ="zahl", titel="Exakte Werte am Einheitskreis")

_TRIPEL = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]


def dreieck_verhaeltnis(rng):
    a, b, c = rng.choice(_TRIPEL)
    s = rng.choice([1, 1, 2, 3])
    if rng.random() < 0.5:
        a, b = b, a
    g, an, h = a * s, b * s, c * s          # Gegenkathete, Ankathete, Hypotenuse
    fn = rng.choice(["sin", "cos", "tan"])
    fehlt = rng.choice(["h", "g", "an"]) if fn != "tan" else rng.choice(["h", "nichts"])
    gegeben = {"g": f"Gegenkathete ${g}$", "an": f"Ankathete ${an}$", "h": f"Hypotenuse ${h}$"}
    if fn == "sin":
        brauche = ["g", "h"]
    elif fn == "cos":
        brauche = ["an", "h"]
    else:
        brauche = ["g", "an"]
    if fehlt in brauche:
        andere = [x for x in ("g", "an", "h") if x != fehlt]
    else:
        andere = brauche
    loesung = {"sin": F(g, h), "cos": F(an, h), "tan": F(g, an)}[fn]
    zeilen = []
    if fehlt == "h" and "h" in brauche:
        zeilen.append((f"\\sqrt{{{g}^2 + {an}^2}} = \\sqrt{{{h * h}}} = {h}", "Hypotenuse mit Pythagoras"))
    elif fehlt == "g" and "g" in brauche:
        zeilen.append((f"\\sqrt{{{h}^2 - {an}^2}} = \\sqrt{{{g * g}}} = {g}", "Gegenkathete mit Pythagoras"))
    elif fehlt == "an" and "an" in brauche:
        zeilen.append((f"\\sqrt{{{h}^2 - {g}^2}} = \\sqrt{{{an * an}}} = {an}", "Ankathete mit Pythagoras"))
    z, n = {"sin": (g, h), "cos": (an, h), "tan": (g, an)}[fn]
    name = {"sin": "Gegenkathete durch Hypotenuse", "cos": "Ankathete durch Hypotenuse", "tan": "Gegenkathete durch Ankathete"}[fn]
    zeilen.append((f"\\frac{{{z}}}{{{n}}}" + ("" if F(z, n).denominator == n else f" = {tex(F(z, n))}"), name))
    fehler = [(F(n, z), "Kehrwert: " + ("Die Hypotenuse gehört in den Nenner." if fn != "tan" else "Die Gegenkathete gehört in den Zähler.")),
              ({"sin": F(an, h), "cos": F(g, h), "tan": F(an, g)}[fn],
               "Gegenkathete und Ankathete vertauscht. Die Gegenkathete liegt dem Winkel $\\alpha$ **gegenüber**.")]
    if fn != "tan":
        fehler.append((F(g, an) if fn == "sin" else F(an, g), "Du hast die Katheten geteilt. Sinus und Kosinus brauchen die Hypotenuse."))
    return {
        "frage": f"In einem rechtwinkligen Dreieck kennst du am Winkel $\\alpha$: {gegeben[andere[0]]} und {gegeben[andere[1]]}. "
                 f"Berechne $\\{fn}(\\alpha)$ als gekürzten Bruch.",
        "loesung": loesung, "gekuerzt": True,
        "tipps": [{"sin": "Sinus: Gegenkathete durch Hypotenuse.", "cos": "Kosinus: Ankathete durch Hypotenuse.",
                   "tan": "Tangens: Gegenkathete durch Ankathete."}[fn],
                  "Fehlt dir eine Seite, hilft Pythagoras: $a^2 + b^2 = c^2$." if fehlt in brauche else "Beide nötigen Seiten sind gegeben.",
                  f"$\\frac{{{z}}}{{{n}}}$, dann kürzen."],
        "rechenweg": _zeilen(*zeilen),
        "erklaerung": "Gegenkathete liegt gegenüber von $\\alpha$, Ankathete liegt an $\\alpha$, die Hypotenuse gegenüber dem rechten Winkel.",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


k.generator(dreieck_verhaeltnis, typ="zahl", titel="Seitenverhältnisse im Dreieck", glatt=True)

k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: Aus dem Sinus den Rest bestimmen

    Es sei $\alpha \in \left(0, \frac{\pi}{2}\right)$ mit $\sin(\alpha) = \frac{5}{13}$.
    Bestimmen Sie $\cos(\alpha)$ und $\tan(\alpha)$ exakt. Begründen Sie das Vorzeichen.
    """,
    [{"typ": "zahl", "frage": "Berechne $\\cos^2(\\alpha)$ als Bruch.", "loesung": 1 - F(5, 13) ** 2,
      "tipps": ["$\\cos^2(\\alpha) = 1 - \\sin^2(\\alpha)$", "$1 - \\frac{25}{169}$"],
      "rechenweg": "$\\cos^2(\\alpha) = 1 - \\frac{25}{169} = \\frac{144}{169}$",
      "typische_fehler": [(F(8, 13), "Du hast $1 - \\frac{5}{13}$ gerechnet. Es gilt für die **Quadrate**: $1 - \\left(\\frac{5}{13}\\right)^2$.")]},
     {"typ": "zahl", "frage": "Berechne $\\cos(\\alpha)$.", "loesung": F(12, 13),
      "tipps": ["Wurzel aus $\\frac{144}{169}$.", "$\\alpha$ liegt zwischen $0$ und $\\frac{\\pi}{2}$: Welches Vorzeichen hat der Kosinus?"],
      "rechenweg": "$\\cos(\\alpha) = \\sqrt{\\frac{144}{169}} = \\frac{12}{13}$, positiv, weil $\\alpha$ im ersten Viertel des Kreises liegt.",
      "typische_fehler": [(F(-12, 13), "Für $\\alpha \\in \\left(0, \\frac{\\pi}{2}\\right)$ liegt der Punkt rechts oben: $\\cos(\\alpha) > 0$."),
                          (F(144, 169), "Das ist $\\cos^2(\\alpha)$. Jetzt noch die Wurzel.")]},
     {"typ": "zahl", "frage": "Berechne $\\tan(\\alpha)$.", "loesung": F(5, 12),
      "tipps": ["$\\tan = \\frac{\\sin}{\\cos}$", "$\\frac{5/13}{12/13}$"],
      "rechenweg": "$\\tan(\\alpha) = \\frac{5/13}{12/13} = \\frac{5}{12}$",
      "typische_fehler": [(F(12, 5), "Kehrwert: $\\tan = \\frac{\\sin}{\\cos}$.")]}],
    "Mit $\\sin^2 + \\cos^2 = 1$ bekommt man $\\cos^2$, das Vorzeichen folgt aus der Lage des Winkels, dann $\\tan = \\frac{\\sin}{\\cos}$.",
    uebungsblatt=True,
    tipps=["Trigonometrischer Pythagoras.", "Achte auf das Vorzeichen beim Wurzelziehen."],
    rechenweg=r"""
    :::rechnung
    1 - \left(\frac{5}{13}\right)^2 = 1 - \frac{25}{169} = \frac{144}{169} || $\cos^2(\alpha)$
    \sqrt{\frac{144}{169}} = \frac{12}{13} || positiv, da $0 < \alpha < \frac{\pi}{2}$
    \frac{5}{13} : \frac{12}{13} = \frac{5}{12} || $\tan(\alpha) = \frac{\sin(\alpha)}{\cos(\alpha)}$
    :::
    """)

k.zusammenfassung(r"""
    ## Trigonometrie

    | | Dreieck | Einheitskreis |
    |---|---|---|
    | $\sin(\alpha)$ | $\frac{\text{Gegenkathete}}{\text{Hypotenuse}}$ | $y$-Koordinate |
    | $\cos(\alpha)$ | $\frac{\text{Ankathete}}{\text{Hypotenuse}}$ | $x$-Koordinate |
    | $\tan(\alpha)$ | $\frac{\text{Gegenkathete}}{\text{Ankathete}}$ | $\frac{\sin}{\cos}$ |

    - Bogenmaß: $x = \frac{\alpha}{180^\circ} \cdot \pi$; $360^\circ = 2\pi$, $180^\circ = \pi$, $90^\circ = \frac{\pi}{2}$.
    - Wichtige Werte: $\sin$ von $0, \frac{\pi}{6}, \frac{\pi}{4}, \frac{\pi}{3}, \frac{\pi}{2}$ ist $\frac{\sqrt{0}}{2}, \frac{\sqrt{1}}{2}, \frac{\sqrt{2}}{2}, \frac{\sqrt{3}}{2}, \frac{\sqrt{4}}{2}$; $\cos$ rückwärts.
    - Periode $2\pi$; Werte zwischen $-1$ und $1$.

    !! $\sin^2(\varphi) + \cos^2(\varphi) = 1$, mit $\sin^2(\varphi) = (\sin(\varphi))^2$.

    - Computer rechnen im Bogenmaß: Taschenrechner auf RAD.
""")
