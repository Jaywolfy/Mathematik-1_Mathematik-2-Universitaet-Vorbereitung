# -*- coding: utf-8 -*-
"""Fundament 1: Zahlen und Zahlenmengen – ℕ, ℤ, ℚ, ℝ, Zahlenstrahl, Vorzeichen."""
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(
    slug="zahlen",
    titel="Zahlen und Zahlenmengen",
    beschreibung="Natürliche, ganze, rationale und reelle Zahlen, der Zahlenstrahl und das Vorzeichen",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="🔢")

k.lernziele([
    "Ich kann natürliche, ganze, rationale und reelle Zahlen unterscheiden",
    "Ich kann Zahlen auf dem Zahlenstrahl finden und der Größe nach ordnen",
    "Ich kann die Zeichen $<$, $>$, $\\le$ und $\\ge$ lesen und richtig benutzen",
    "Ich kann zu jeder Zahl die Gegenzahl angeben",
])

k.warum(r"""
Ein Computer muss für jede Zahl wissen, **welche Art** von Zahl es ist. Daraus
entstehen die Datentypen beim Programmieren: `int` steht für [[ganze Zahlen|ganze Zahl]]
aus $\mathbb{Z}$. In Python dürfen sie beliebig groß werden, in Java oder C nicht.
`float` speichert Kommazahlen im Zweiersystem und muss dabei runden, schon bei
$0{,}1$. Deshalb ergibt `0.1 + 0.2` nicht genau `0.3`. Wer das weiß, wundert sich
nicht über solche Fehler.
""")

# ── 1: Natürliche Zahlen und Zahlenstrahl ──────────────────────────────────
k.erklaerung("Zählen: die natürlichen Zahlen", r"""
    ## Die Zählzahlen

    :::analogie 🍎 Äpfel zählen
    Du zählst Äpfel in einer Kiste: eins, zwei, drei … Mit diesen Zahlen hat
    die Mathematik angefangen.
    :::

    Die Zahlen $1, 2, 3, 4, \ldots$ heißen [[natürliche Zahlen|natürliche Zahl]].
    Alle zusammen bilden eine [[Menge]]. Sie bekommt das Zeichen $\mathbb{N}$:

    $$\mathbb{N} = \{1, 2, 3, 4, \ldots\}$$

    Die drei Punkte bedeuten: „und so weiter, ohne Ende“. Eine größte
    natürliche Zahl gibt es nicht. Zu jeder Zahl kannst du 1 addieren.

    Nimmst du die Null dazu, schreibt man $\mathbb{N}_0 = \{0, 1, 2, 3, \ldots\}$.

    :::visual zahlenstrahl
    {"von": 0, "bis": 6, "punkte": [{"x": 1}, {"x": 2}, {"x": 3}, {"x": 4}, {"x": 5}],
     "unterschrift": "Jede natürliche Zahl hat ihren festen Platz rechts von der $0$."}
    :::

    :::info Vorsicht in Büchern
    Manche Bücher zählen die $0$ zu $\mathbb{N}$, andere nicht. Schau im
    Uni-Skript nach, welche Schreibweise gilt. Hier ist $0 \notin \mathbb{N}$:
    Das Zeichen $\in$ heißt „ist [[Element]] von“, $\notin$ heißt „ist nicht Element von“.
    :::

    :::alt Mit einer Treppe erklärt
    Stell dir eine Treppe vor. Die erste Stufe ist die $1$, die nächste die $2$
    und so weiter. Die Treppe hört nie auf. Jede Stufe ist eine natürliche Zahl.
    Der Boden vor der Treppe ist die $0$.
    :::
    ---
    ## Der Zahlenstrahl

    Ein **Zahlenstrahl** ist eine Linie, auf der jede Zahl ihren festen Platz hat.
    Er beginnt bei der $0$. Nach rechts werden die Zahlen größer.

    !! Weiter rechts auf dem Zahlenstrahl heißt: größer.

    Probier es aus: Tippe auf den Strahl und lies ab, wo du bist.

    :::visual zahlenstrahl
    {"von": 0, "bis": 10, "punkte": [{"x": 3, "label": "3"}, {"x": 7, "label": "7"}], "interaktiv": true,
     "unterschrift": "Die $7$ liegt rechts von der $3$. Also ist $3 < 7$."}
    :::

    :::alt Wie ein Lineal
    Ein Zahlenstrahl funktioniert wie ein Lineal. Am Anfang steht die $0$.
    Jeder Strich ist eine Zahl. Je weiter du nach rechts gehst, desto länger
    wird die Strecke von der $0$ aus. Die Zahl wird also größer.
    :::
    """)

k.mc("Welche dieser Zahlen ist **keine** natürliche Zahl?",
     ["$-4$", "$7$", "$1$", "$100$"],
     "Natürliche Zahlen sind die Zählzahlen $1, 2, 3, \\ldots$ ohne Minuszeichen. $-4$ gehört nicht dazu.",
     tipps=["Natürliche Zahlen sind die Zahlen, mit denen du Äpfel zählst.",
            "Kann man „minus 4 Äpfel“ zählen?"])

k.wf("Auf dem Zahlenstrahl liegt von zwei Zahlen die größere immer weiter rechts.", True,
     "Genau: Nach rechts werden die Zahlen größer.",
     tipps=["Denk an das Lineal: Wohin wächst es?"])

# ── 2: Negative Zahlen ─────────────────────────────────────────────────────
k.erklaerung("Unter null: die ganzen Zahlen", r"""
    ## Zahlen mit Minus

    :::analogie 🌡️ Das Thermometer
    Im Winter zeigt das Thermometer $-5$ Grad. Das sind fünf Grad **unter**
    null. Negative Zahlen liegen links von der $0$.
    :::

    Die [[ganzen Zahlen|ganze Zahl]] sind die natürlichen Zahlen, die $0$ und alle
    Zahlen mit Minus:

    $$\mathbb{Z} = \{\ldots, -3, -2, -1, 0, 1, 2, 3, \ldots\}$$

    Dafür verlängern wir den Zahlenstrahl nach links. So entsteht die [[Zahlengerade]].
    Das Minus vor der Zahl heißt [[Vorzeichen]]. Zu jeder Zahl gibt es eine
    [[Gegenzahl]]: gleich weit von der $0$ entfernt, aber auf der anderen Seite.
    Die Gegenzahl von $0$ ist $0$ selbst.

    :::visual zahlenstrahl
    {"von": -5, "bis": 5, "punkte": [{"x": -3, "label": "-3"}, {"x": 3, "label": "3"}],
     "pfeile": [{"von": 0, "bis": -3, "label": "3\\text{ nach links}"}, {"von": 0, "bis": 3, "label": "3\\text{ nach rechts}"}],
     "unterschrift": "$3$ und $-3$ sind Gegenzahlen: beide $3$ Schritte von der $0$ entfernt."}
    :::

    :::alt Mit einem Aufzug erklärt
    Denk an einen Aufzug. Das Erdgeschoss ist die $0$. Etage $3$ ist drei
    Stockwerke über dem Erdgeschoss. Etage $-3$ ist drei Stockwerke darunter
    im Keller. Beide sind gleich weit vom Erdgeschoss weg. Das Minus sagt nur:
    nach unten statt nach oben.
    :::
    ---
    ## Negative Zahlen vergleichen

    Auch hier gilt: Weiter rechts ist größer. Das heißt: $-5$ ist **kleiner**
    als $-2$, obwohl $5$ größer als $2$ ist.

    :::rechnung Beispiel vorgerechnet
    -5 < -2 || $-5$ liegt weiter links als $-2$
    -2 < 0 || jede negative Zahl ist kleiner als $0$
    0 < 3 || jede positive Zahl ist größer als $0$
    -5 < -2 < 0 < 3 || zusammen: von links nach rechts geordnet
    :::

    :::achtung Nur auf die Ziffer schauen
    „$-5$ ist größer als $-2$, weil $5$ größer als $2$ ist.“ Das stimmt nicht!
    Bei $-5$ Grad ist es **kälter** als bei $-2$ Grad. Kälter heißt: kleinere Zahl.
    :::

    :::alt Mit Schulden erklärt
    Stell dir vor, $-5$ bedeutet: Du hast $5$ Euro Schulden. $-2$ bedeutet:
    $2$ Euro Schulden. Wer $5$ Euro Schulden hat, hat **weniger** Geld.
    Deshalb ist $-5$ kleiner als $-2$.
    :::
    """)

k.zahl("Gib die Gegenzahl von $-5$ an.", 5,
       "Die Gegenzahl ist gleich weit von der $0$ entfernt, aber auf der anderen Seite: aus $-5$ wird $5$.",
       tipps=["Die Gegenzahl liegt auf der anderen Seite der $0$.",
              "$-5$ ist $5$ Schritte links von der $0$. Wo landest du mit $5$ Schritten nach rechts?",
              "Dreh das Vorzeichen um: aus Minus wird Plus."],
       rechenweg=r"""
       :::rechnung
       -5 || $5$ Schritte links von der $0$
       5 || Gegenzahl: $5$ Schritte rechts von der $0$
       :::
       """,
       typische_fehler=[(-5, "Das ist die Zahl selbst. Die Gegenzahl hat das **andere** Vorzeichen.")])

k.mc("Welche Aussage stimmt?",
     ["$-5 < -2$", "$-5 > -2$", "$-5 = -2$"],
     "$-5$ liegt auf der Zahlengeraden links von $-2$. Weiter links heißt kleiner, also $-5 < -2$.",
     tipps=["Zeichne beide Zahlen auf eine Zahlengerade.", "Welche Zahl liegt weiter links?"],
     fehler={"$-5 > -2$": "Du hast vermutlich nur $5$ und $2$ verglichen. Bei negativen Zahlen ist es umgekehrt: "
                          "$-5$ liegt weiter links, also ist $-5$ **kleiner**."})

k.zahl("Welche ganze Zahl liegt auf der Zahlengeraden genau in der Mitte zwischen $-6$ und $2$?", -2,
       "Von $-6$ bis $2$ sind es $8$ Schritte. Die Hälfte sind $4$ Schritte. Von $-6$ aus $4$ Schritte nach rechts: $-2$.",
       tipps=["Zähle zuerst, wie viele Schritte es von $-6$ bis $2$ sind.",
              "Es sind $8$ Schritte. Gehe die Hälfte davon.",
              "Starte bei $-6$ und gehe $4$ Schritte nach rechts."],
       rechenweg=r"""
       :::rechnung
       6 + 2 = 8 || $6$ Schritte bis zur $0$, dann $2$ weiter: Abstand $8$
       8 : 2 = 4 || die Hälfte des Abstands
       -6 + 4 = -2 || von $-6$ aus $4$ Schritte nach rechts
       :::
       """,
       typische_fehler=[(4, "$4$ ist der **halbe Abstand**, nicht die Mitte. Gehe von $-6$ aus $4$ Schritte nach rechts."),
                        (-4, "Du hast vermutlich $(-6 - 2) : 2$ gerechnet. Für die Mitte addiert man: $(-6 + 2) : 2$.")])

# ── 3: Brüche und Kommazahlen ──────────────────────────────────────────────
k.erklaerung("Teile vom Ganzen: die rationalen Zahlen", r"""
    ## Brüche gehören auch dazu

    :::analogie 🍕 Pizza teilen
    Eine Pizza wird in $4$ Stücke geteilt. Du isst $3$ davon. Du hast
    $\frac{3}{4}$ der Pizza gegessen. Das ist keine ganze Zahl, aber eine Zahl.
    :::

    Jede Zahl, die man als Bruch $\frac{p}{q}$ schreiben kann, heißt
    [[rationale Zahl]]. Oben steht eine ganze Zahl $p$, unten eine natürliche
    Zahl $q$. Alle zusammen bilden $\mathbb{Q}$.

    :::rechnung Beispiel vorgerechnet
    -3 = \frac{-3}{1} || jede ganze Zahl ist auch ein Bruch
    0{,}25 = \frac{25}{100} || zwei Nachkommastellen: Hundertstel
    = \frac{1}{4} || oben und unten durch $25$ geteilt (das heißt kürzen)
    :::

    !! Jede Kommazahl mit endlich vielen Stellen ist ein Bruch.

    :::alt Mit Geld erklärt
    $0{,}25$ Euro sind $25$ Cent, also $25$ von $100$ Cent: $\frac{25}{100}$.
    Viermal $25$ Cent ergeben einen ganzen Euro. Also ist $0{,}25 = \frac{1}{4}$.
    Kommazahlen und Brüche sind nur zwei Schreibweisen derselben Zahl.
    :::
    ---
    ## Brüche auf der Zahlengeraden

    Rationale Zahlen gibt es auch **zwischen** den ganzen Zahlen. $\frac{1}{2}$ liegt
    genau in der Mitte zwischen $0$ und $1$.

    :::visual zahlenstrahl
    {"von": -2, "bis": 2, "schritt": 0.5, "punkte": [{"x": "-3/2"}, {"x": "1/2"}, {"x": "3/4", "farbe": "orange"}],
     "unterschrift": "$-\\frac{3}{2} = -1{,}5$ liegt zwischen $-2$ und $-1$."}
    :::

    Zwischen zwei Brüchen findest du immer noch einen weiteren. Die
    rationalen Zahlen liegen also unendlich dicht. Trotzdem haben sie Lücken.
    Das zeigt der nächste Abschnitt.

    :::alt Mit einem Zollstock erklärt
    Auf einem Zollstock gibt es zwischen den Zentimetern noch Millimeter. Und
    du könntest jeden Millimeter noch weiter teilen. So ist es mit den
    Brüchen: Zwischen $0$ und $1$ liegen $\frac{1}{2}$, $\frac{1}{4}$,
    $\frac{1}{10}$ und unendlich viele mehr.
    :::
    """)

k.mc("Warum ist $7$ auch eine rationale Zahl?",
     ["Weil man $7$ als Bruch $\\frac{7}{1}$ schreiben kann",
      "Weil $7$ eine Primzahl ist",
      "Weil $7$ ungerade ist",
      "$7$ ist keine rationale Zahl"],
     "Rational heißt: als Bruch schreibbar. $7 = \\frac{7}{1}$. Jede ganze Zahl ist also rational.",
     tipps=["Rational bedeutet: Man kann die Zahl als Bruch schreiben.",
            "Was steht unter dem Bruchstrich, wenn man durch $1$ teilt?"],
     fehler={"$7$ ist keine rationale Zahl": "Doch! Jede ganze Zahl ist auch rational: $7 = \\frac{7}{1}$."})

k.zahl("Schreibe $0{,}75$ als Bruch.", F(3, 4),
       "$0{,}75$ hat zwei Nachkommastellen, also Hundertstel: $\\frac{75}{100}$. Oben und unten durch $25$ geteilt: $\\frac{3}{4}$. Beides ist richtig.",
       form="bruch",
       tipps=["Zwei Nachkommastellen bedeuten Hundertstel.",
              "$0{,}75 = \\frac{75}{100}$. Durch welche Zahl kannst du oben und unten teilen?",
              "$\\frac{75}{100}$ ist schon richtig. Kleiner geht es mit: oben und unten durch $25$."],
       rechenweg=r"""
       :::rechnung
       0{,}75 = \frac{75}{100} || zwei Nachkommastellen: Hundertstel
       = \frac{75 : 25}{100 : 25} || oben und unten durch $25$ teilen
       = \frac{3}{4} || einfacher geschrieben (gekürzt)
       :::
       """,
       typische_fehler=[(F(75, 10), "$0{,}75$ hat **zwei** Nachkommastellen, das sind Hundertstel. Unter den Bruchstrich gehört $100$, nicht $10$."),
                        (F(3, 5), "Du hast oben und unten durch **verschiedene** Zahlen geteilt ($75 : 25$, aber $100 : 20$). Es muss dieselbe Zahl sein.")])

# ── 4: Reelle Zahlen ───────────────────────────────────────────────────────
k.erklaerung("Lückenlos: die reellen Zahlen", r"""
    ## Zahlen, die kein Bruch sind

    Es gibt Zahlen, die man **nicht** als Bruch schreiben kann. Das bekannteste
    Beispiel ist $\sqrt{2}$, die Zahl, die mit sich selbst malgenommen $2$ ergibt.

    :::rechnung Beispiel vorgerechnet
    1{,}4^2 = 1{,}96 || etwas zu klein
    1{,}5^2 = 2{,}25 || etwas zu groß
    1{,}4 < \sqrt{2} < 1{,}5 || also liegt $\sqrt{2}$ dazwischen
    1{,}41^2 = 1{,}9881 || nächste Stelle: wieder etwas zu klein
    1{,}42^2 = 2{,}0164 || etwas zu groß
    1{,}41 < \sqrt{2} < 1{,}42 || so geht es endlos weiter
    :::

    Die Nachkommastellen von $\sqrt{2} = 1{,}41421356\ldots$ hören nie auf und
    wiederholen sich nie. Solche Zahlen heißen [[irrational|irrationale Zahl]].
    Auch $\pi = 3{,}14159\ldots$ gehört dazu. Dass $\sqrt{2}$ kein Bruch ist,
    wird in Mathe 1 bewiesen.

    :::alt Mit einem Quadrat erklärt
    Zeichne ein Quadrat mit $1$ cm Seitenlänge. Die Diagonale ist genau
    $\sqrt{2}$ cm lang. Die Strecke gibt es also wirklich. Trotzdem kannst du
    ihre Länge mit keinem Bruch genau angeben, egal wie fein du misst.
    :::
    ---
    ## Alle zusammen: die reellen Zahlen

    Rationale und irrationale Zahlen zusammen heißen [[reelle Zahlen|reelle Zahl]],
    kurz $\mathbb{R}$. Sie füllen die Zahlengerade ohne jede Lücke.

    :::visual zahlenstrahl
    {"von": -1, "bis": 4, "punkte": [{"x": "sqrt(2)", "label": "\\sqrt{2}"}, {"x": "pi", "label": "\\pi", "farbe": "orange"}, {"x": "-1/2"}],
     "unterschrift": "Jeder Punkt auf der Zahlengeraden ist eine reelle Zahl."}
    :::

    Die Zahlenmengen stecken ineinander wie Puppen:

    $$\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$$

    $A \subset B$ liest man „$A$ ist [[Teilmenge]] von $B$“: Jedes Element von $A$
    liegt auch in $B$. Manche Skripte schreiben dafür $\subseteq$.

    :::alt Welche Rechnung geht wo?
    Jede neue Zahlenmenge löst ein Problem der vorigen. In $\mathbb{N}$ geht
    $3 - 5$ nicht, es gibt kein Ergebnis. In $\mathbb{Z}$ schon: $-2$. In
    $\mathbb{Z}$ geht $1 : 2$ nicht. In $\mathbb{Q}$ schon: $\frac{1}{2}$. In
    $\mathbb{Q}$ gibt es keine Zahl, die mal sich selbst $2$ ergibt. In
    $\mathbb{R}$ schon: $\sqrt{2}$. Jede Menge enthält die vorige und noch mehr.
    :::
    """)

k.mc("Welche Zahl ist **nicht** rational?",
     ["$\\sqrt{2}$", "$\\frac{1}{3}$", "$-4$", "$0{,}5$"],
     "$\\sqrt{2}$ lässt sich nicht als Bruch schreiben. Die anderen schon: $-4 = \\frac{-4}{1}$, $0{,}5 = \\frac{1}{2}$.",
     tipps=["Rational heißt: als Bruch schreibbar.", "Bei drei der Zahlen findest du sofort einen Bruch."],
     fehler={"$\\frac{1}{3}$": "$\\frac{1}{3} = 0{,}333\\ldots$ hat zwar unendlich viele Nachkommastellen, ist aber ein Bruch "
                              "und damit rational. Irrational sind nur Zahlen, die man **nicht** als Bruch schreiben kann."})

k.mehrfach("Zu welchen Zahlenmengen gehört $-3$? Wähle alle passenden aus.",
           ["$\\mathbb{Z}$", "$\\mathbb{Q}$", "$\\mathbb{R}$"], ["$\\mathbb{N}$"],
           "$-3$ ist eine ganze Zahl. Weil die Mengen ineinanderstecken, ist sie auch rational und reell. Natürlich ist sie nicht: Da gibt es kein Minus.",
           tipps=["Denk an die Puppen: Was in einer kleinen Menge liegt, liegt auch in allen größeren.",
                  "In welcher kleinsten Menge liegt $-3$?"],
           fehler={"$\\mathbb{N}$": "Natürliche Zahlen sind die Zählzahlen $1, 2, 3, \\ldots$ ohne Minus."})

k.zuordnen("Ordne jeder Zahl die **kleinste** Zahlenmenge zu, in der sie liegt.",
           [("$5$", "ℕ (natürliche Zahlen)"), ("$-2$", "ℤ (ganze Zahlen)"),
            ("$\\frac{3}{4}$", "ℚ (rationale Zahlen)"), ("$\\sqrt{3}$", "ℝ (reelle Zahlen)")],
           "$5$ ist eine Zählzahl. $-2$ braucht das Minus. $\\frac{3}{4}$ braucht den Bruch. $\\sqrt{3}$ ist kein Bruch, also nur reell.",
           tipps=["Frag bei jeder Zahl: Ist sie eine Zählzahl? Braucht sie ein Minus? Braucht sie einen Bruch?"])

# ── 5: Ungleichheitszeichen ────────────────────────────────────────────────
k.erklaerung("Kleiner, größer, gleich: die Vergleichszeichen", r"""
    ## Vier Zeichen zum Vergleichen

    | Zeichen | gelesen | Beispiel |
    |---|---|---|
    | $<$ | kleiner als | $3 < 5$ |
    | $>$ | größer als | $5 > 3$ |
    | $\le$ | kleiner oder gleich | $4 \le 4$ |
    | $\ge$ | größer oder gleich | $7 \ge 2$ |

    :::analogie 🐊 Das Krokodil
    Das Zeichen ist ein Krokodil-Maul. Es ist immer zur **größeren** Zahl hin
    geöffnet, denn das Krokodil will mehr fressen: $3 < 5$.
    :::

    :::rechnung Beispiel vorgerechnet
    -2 > -7 || $-2$ liegt rechts von $-7$
    4 \le 4 || „kleiner oder gleich“: gleich reicht schon
    \frac{1}{2} < \frac{3}{4} || $0{,}5$ liegt links von $0{,}75$
    :::

    :::alt Mit einem Pfeil erklärt
    Schau auf die Spitze des Zeichens. Die Spitze zeigt immer auf die
    **kleinere** Zahl. Bei $3 < 5$ zeigt die Spitze nach links zur $3$.
    Der Strich unten bei $\le$ heißt: „oder gleich“.
    :::
    """)

k.wf("$4 \\le 4$ ist eine wahre Aussage.", True,
     "„Kleiner oder gleich“ ist erfüllt, sobald einer der beiden Fälle gilt. $4 = 4$ reicht.",
     tipps=["Lies $\\le$ laut: „kleiner **oder** gleich“."])

k.zahl("Wie viele ganze Zahlen $x$ erfüllen $-2 < x \\le 3$?", 5,
       "Es sind $-1, 0, 1, 2, 3$. Die $-2$ gehört nicht dazu ($<$), die $3$ schon ($\\le$).",
       tipps=["Schreib alle ganzen Zahlen zwischen $-2$ und $3$ auf.",
              "Prüfe die Ränder: Gehört $-2$ dazu? Gehört $3$ dazu?",
              "$-2$ ist nicht dabei, $3$ ist dabei. Jetzt zählen."],
       rechenweg=r"""
       :::rechnung
       -2 < x || also ist $-2$ selbst **nicht** dabei
       x \le 3 || die $3$ ist dabei
       -1, 0, 1, 2, 3 || alle ganzen Zahlen dazwischen
       :::

       Das sind $5$ Zahlen.
       """,
       typische_fehler=[(6, "Du hast die $-2$ mitgezählt. Bei $<$ gehört der Rand **nicht** dazu."),
                        (4, "Bei $\\le$ gehört die $3$ dazu. Zähle sie mit.")])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _zufallszahl(rng):
    """(Wert, LaTeX-Anzeige, Kommazahl-Text oder None): ganze Zahl, Halbe/Viertel oder Kommazahl.
    Nur Halbe und Viertel, denn deren Kommazahlen (0,5 und 0,25) kennt man aus Abschnitt 3."""
    art = rng.choice(["ganz", "ganz", "bruch", "dezimal"])
    if art == "ganz":
        w = F(rng.randint(-9, 9))
        return w, mathlib.tex(w), None
    if art == "bruch":
        n = rng.choice([2, 4])
        w = F(rng.choice([z for z in range(-2 * n + 1, 2 * n) if z % n]), n)
        return w, mathlib.tex(w), mathlib.dezimal(w)
    w = F(rng.choice([z for z in range(-40, 41) if z % 10]), 10)
    return w, mathlib.dezimal(w), None


def zahlen_ordnen(rng):
    zahlen = {}
    while len(zahlen) < 5:
        w, anzeige, komma = _zufallszahl(rng)
        zahlen.setdefault(w, (anzeige, komma))
    geordnet = sorted(zahlen)
    kette = " < ".join(zahlen[w][0] for w in geordnet)
    brueche = [w for w in geordnet if zahlen[w][1]]
    weg = ""
    if brueche:
        weg = "Brüche als Kommazahl: " + ", ".join(f"${zahlen[w][0]} = {zahlen[w][1]}$" for w in brueche) + ".\n\n"
    tipps = ["Stell dir die Zahlen auf der Zahlengeraden vor."]
    tipps.append("Bei negativen Zahlen gilt: Je weiter weg von der $0$, desto kleiner." if geordnet[0] < 0
                 else "Alle Zahlen sind mindestens $0$: Die kleinste liegt am nächsten an der $0$.")
    tipps.append("Hilfe für Brüche: $\\frac{1}{2} = 0{,}5$ und $\\frac{1}{4} = 0{,}25$." if brueche
                 else "Vergleiche zuerst die Stellen vor dem Komma.")
    return {
        "typ": "ordnen",
        "frage": "Bringe die Zahlen in die richtige Reihenfolge: von der **kleinsten** zur **größten**.",
        "schritte": [f"${zahlen[w][0]}$" for w in geordnet],
        "tipps": tipps,
        "erklaerung": f"Von links nach rechts auf der Zahlengeraden: ${kette}$.",
        "rechenweg": weg + f"Geordnet: ${kette}$",
    }


k.praxis()

k.generator(zahlen_ordnen, typ="ordnen", titel="Zahlen ordnen")


def ganze_zwischen(rng):
    a = rng.randint(-8, 3)
    b = rng.randint(a + 3, a + 10)
    links = rng.choice(["<", "\\le"])
    rechts = rng.choice(["<", "\\le"])
    lo = a + 1 if links == "<" else a
    hi = b - 1 if rechts == "<" else b
    liste = list(range(lo, hi + 1))
    n = len(liste)
    fehler = [(b - a + 1, "Du hast beide Ränder mitgezählt. Prüfe bei jedem Rand: Steht dort $<$ (nicht dabei) oder $\\le$ (dabei)?"),
              (b - a - 1, "Du hast beide Ränder weggelassen. Bei $\\le$ gehört der Rand dazu."),
              (b - a, "Fast: Einer der beiden Ränder ist falsch gezählt. Prüfe $<$ und $\\le$ einzeln.")]
    return {
        "frage": f"Wie viele ganze Zahlen $x$ erfüllen ${a} {links} x {rechts} {b}$?",
        "loesung": n,
        "tipps": ["Schreib die ganzen Zahlen zwischen den Grenzen auf.",
                  f"Gehört ${a}$ dazu? Gehört ${b}$ dazu? Schau auf $<$ oder $\\le$.",
                  f"Die kleinste passende Zahl ist ${lo}$, die größte ${hi}$."],
        "rechenweg": f"Kleinste passende ganze Zahl: ${lo}$. Größte: ${hi}$.\n\n"
                     f"Alle: ${', '.join(str(z) for z in liste)}$. Das sind ${n}$ Zahlen.",
        "erklaerung": "Bei $<$ gehört der Rand nicht dazu, bei $\\le$ schon.",
        "typische_fehler": ohne_gleiche(n, fehler),
    }


k.generator(ganze_zwischen, typ="zahl", titel="Ganze Zahlen zählen", glatt=True)


def _abstand_zeile(a, b):
    """Abstand von a bis b (a < b) durch Schritte zählen, ohne „Minus minus“ (kommt erst in Kapitel 2)."""
    if a < 0 < b:
        return (f"{-a} + {b} = {b - a} || ${-a}$ {'Schritt' if a == -1 else 'Schritte'} bis zur $0$, "
                f"dann ${b}$ weiter: Abstand ${b - a}$")
    if b <= 0:
        return f"{-a} - {-b} = {b - a} || Abstand zur $0$: ${-a}$ und ${-b}$, Unterschied ${b - a}$"
    return f"{b} - {a} = {b - a} || Abstand: ${b - a}$ Schritte"


def mitte(rng):
    while True:
        a = rng.randint(-12, 6)
        b = a + 2 * rng.randint(2, 8)
        if a != 0 and a + b != 0:
            break
    m = (a + b) // 2
    fehler = [((b - a) // 2, "Das ist der **halbe Abstand**. Die Mitte erreichst du, wenn du von der linken Zahl so viele Schritte nach rechts gehst."),
              ((a - b) // 2, f"Für die Mitte addiert man die Zahlen: $({a} + {mathlib.tex_klammer(b)}) : 2$, nicht subtrahieren."),
              (a + b, "Du hast vergessen, durch $2$ zu teilen.")]
    return {
        "frage": f"Welche Zahl liegt genau in der Mitte zwischen ${a}$ und ${b}$?",
        "loesung": m,
        "tipps": ["Bestimme zuerst den Abstand der beiden Zahlen.",
                  f"Der Abstand ist ${b - a}$. Gehe die Hälfte davon.",
                  f"Starte bei ${a}$ und gehe ${(b - a) // 2}$ Schritte nach rechts."],
        "rechenweg": f":::rechnung\n{_abstand_zeile(a, b)}\n"
                     f"{b - a} : 2 = {(b - a) // 2} || halber Abstand\n"
                     f"{a} + {(b - a) // 2} = {m} || von ${a}$ nach rechts gehen\n:::",
        "erklaerung": "Die Mitte von $a$ und $b$ ist $\\frac{a + b}{2}$.",
        "typische_fehler": ohne_gleiche(m, fehler),
    }


k.generator(mitte, typ="zahl", titel="Die Mitte finden", glatt=True)

k.menge(r"""
    ## Übungsblatt-Stil: Mengen aufzählen

    In Uni-Skripten werden Mengen oft durch eine **Eigenschaft** beschrieben:

    $$M = \{x \in \mathbb{Z} \mid -3 \le x < 2\}$$

    Gelesen: „$M$ ist die Menge aller ganzen Zahlen $x$, für die gilt:
    $-3 \le x < 2$.“ Gib $M$ in aufzählender Form an, z. B. $\{1; 2; 3\}$.
    Trenne die Elemente beim Eintippen mit **;**, weil das Komma auch das Dezimalkomma sein kann.
    """,
    "{-3; -2; -1; 0; 1}",
    "Die ganzen Zahlen von $-3$ (dabei, wegen $\\le$) bis unter $2$ (nicht dabei, wegen $<$): $-3, -2, -1, 0, 1$.",
    uebungsblatt=True,
    tipps=["Der senkrechte Strich $\\mid$ heißt „für die gilt“.",
           "Prüfe beide Ränder: Ist $-3$ dabei? Ist $2$ dabei?",
           "$-3$ ist dabei, $2$ nicht. Schreib alle ganzen Zahlen dazwischen auf."],
    rechenweg=r"""
    :::rechnung
    -3 \le x || $-3$ gehört dazu
    x < 2 || $2$ gehört **nicht** dazu, $1$ schon
    M = \{-3; -2; -1; 0; 1\} || alle ganzen Zahlen dazwischen
    :::
    """,
    typische_fehler=[("{-3; -2; -1; 0; 1; 2}", "Die $2$ gehört nicht dazu: Es heißt $x < 2$, nicht $x \\le 2$."),
                     ("{-2; -1; 0; 1}", "Die $-3$ gehört dazu: Es heißt $-3 \\le x$, also ist $x = -3$ erlaubt.")])

k.zusammenfassung(r"""
    ## Zahlen und Zahlenmengen

    | Menge | Name | Beispiele |
    |---|---|---|
    | $\mathbb{N} = \{1, 2, 3, \ldots\}$ | natürliche Zahlen | $1$, $7$, $100$ |
    | $\mathbb{N}_0 = \{0, 1, 2, \ldots\}$ | mit Null | $0$, $5$ |
    | $\mathbb{Z} = \{\ldots, -1, 0, 1, \ldots\}$ | ganze Zahlen | $-3$, $0$, $8$ |
    | $\mathbb{Q}$ | rationale Zahlen (Brüche) | $\frac{3}{4}$, $-2$, $0{,}25$ |
    | $\mathbb{R}$ | reelle Zahlen | $\sqrt{2}$, $\pi$, alle oben |

    $$\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$$

    !! Auf der Zahlengeraden gilt: weiter rechts = größer. Darum ist $-5 < -2$.

    - Gegenzahl: gleicher Abstand zur $0$, anderes Vorzeichen: $5 \leftrightarrow -5$. Die Gegenzahl von $0$ ist $0$.
    - $<$ kleiner, $>$ größer, $\le$ kleiner oder gleich, $\ge$ größer oder gleich.
    - Bei $<$ gehört der Rand nicht dazu, bei $\le$ schon.
""")
