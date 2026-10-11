# -*- coding: utf-8 -*-
"""Fundament 7: Terme – zusammenfassen, ausmultiplizieren, ausklammern, binomische Formeln, kürzen."""
import math

from .. import mathlib, pruefer
from ..engine import neues_kapitel

k = neues_kapitel(
    slug="terme",
    titel="Terme und binomische Formeln",
    beschreibung="Gleichartiges zusammenfassen, Klammern auflösen, ausklammern, binomische Formeln und Bruchterme kürzen",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="🔤")

k.lernziele([
    "Ich kann gleichartige Terme zusammenfassen und Produkte wie $2x \\cdot 3x$ vereinfachen",
    "Ich kann Klammern ausmultiplizieren, auch Klammer mal Klammer",
    "Ich kenne die drei binomischen Formeln und weiß, warum $(a + b)^2 \\neq a^2 + b^2$ ist",
    "Ich kann ausklammern und Bruchterme kürzen, ohne aus Summen zu kürzen",
])

k.warum(r"""
Programme sind voller Terme: `2*x + 3*x` schreibt niemand gern, `5*x` ist kürzer
und schneller. Compiler vereinfachen Ausdrücke genau mit den Regeln dieses Kapitels.
Ausklammern spart Rechenzeit: $ax + ay$ braucht zwei Multiplikationen,
$a(x + y)$ nur eine. Das Horner-Schema für Polynome beruht genau darauf. In Mathe 1
formst du ständig Terme um: in Beweisen, beim Gauß-Algorithmus und bei Grenzwerten.
Ein falsches $(a + b)^2 = a^2 + b^2$ macht dort jede Rechnung kaputt.
""")


def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


def _p(text, var="x"):
    """Term -> Polynom (für exakte Koeffizienten)."""
    return mathlib.Polynom.aus_ast(pruefer.parse(text, [var]).ast, var)


def _tex(text, var="x"):
    return pruefer.parse(text, [var]).latex()


# ── 1: Zusammenfassen ──────────────────────────────────────────────────────
k.erklaerung("Variablen und Zusammenfassen", r"""
    ## Gleiches zu Gleichem

    :::analogie 🍎 Obstkorb
    In einem Korb liegen $3$ Äpfel, $2$ Birnen und noch $4$ Äpfel. Du sagst: $7$ Äpfel
    und $2$ Birnen. Äpfel und Birnen zählst du nie zusammen.
    :::

    Eine [[Variable]] wie $x$ ist ein Platzhalter für eine Zahl. Terme mit derselben
    Variable in derselben Potenz heißen [[gleichartige Terme|gleichartige Terme]]. Nur sie
    darfst du zusammenfassen: Du addierst die Zahlen davor.

    :::rechnung Beispiel vorgerechnet
    3x + 2y + 4x - y || Aufgabe
    = 3x + 4x + 2y - y || gleichartige Terme nebeneinander
    = 7x + y || $3 + 4 = 7$ und $2 - 1 = 1$
    :::

    :::achtung Ungleiches zusammenfassen
    $3x + 2y = 5xy$ ist falsch. Äpfel plus Birnen ergeben keine „Apfelbirnen“.
    Auch $x^2 + x$ bleibt stehen: $x^2$ und $x$ sind nicht gleichartig.
    :::

    :::alt Mit einer Probe erklärt
    Setz für $x$ und $y$ Zahlen ein, zum Beispiel $x = 10$ und $y = 1$.
    Dann ist $3x + 2y + 4x - y = 30 + 2 + 40 - 1 = 71$. Und $7x + y = 70 + 1 = 71$.
    Beide Terme liefern denselben Wert, also war das Zusammenfassen richtig.
    $5xy$ ergäbe $50$: falsch.
    :::
    ---
    ## Produkte vereinfachen

    Beim Malnehmen sortierst du: Zahlen zu Zahlen, Variablen zu Variablen. Das darfst
    du, weil die Reihenfolge beim Malnehmen egal ist. Gleiche Variablen werden zur
    Potenz: $x \cdot x = x^2$.

    :::rechnung Beispiel vorgerechnet
    2x \cdot 3x = 2 \cdot 3 \cdot x \cdot x || Zahlen nach vorn sortieren
    = 6x^2 || $2 \cdot 3 = 6$ und $x \cdot x = x^2$
    :::

    !! Plus: $x + x = 2x$. Mal: $x \cdot x = x^2$.

    :::alt Mit einer Fläche erklärt
    Ein Rechteck ist $2x$ breit und $3x$ hoch. Teile die Breite in $2$ Stücke der
    Länge $x$ und die Höhe in $3$ Stücke der Länge $x$. Dann besteht das Rechteck aus
    $2 \cdot 3 = 6$ kleinen Quadraten. Jedes hat die Fläche $x \cdot x = x^2$. Zusammen
    also $6x^2$.
    :::
    """)

k.vereinfache("3x + 2y + 4x - y", "7x + y", variablen="x, y", form="vereinfacht",
              frage="Fasse zusammen: $\\displaystyle {term}$.",
              erklaerung="Die $x$-Terme ergeben $3x + 4x = 7x$, die $y$-Terme $2y - y = y$.",
              tipps=["Welche Terme haben dieselbe Variable?",
                     "Sortiere: $3x + 4x$ und $2y - y$.",
                     "$3x + 4x = 7x$. Und $2y - y$ ist $1y$, also $y$."],
              rechenweg=r"""
              :::rechnung
              3x + 2y + 4x - y = 3x + 4x + 2y - y || gleichartige Terme sortieren
              = 7x + y || Zahlen davor addieren
              :::
              """,
              typische_fehler=[("7x + 3y", "Achte auf das Minus vor dem letzten $y$: $2y - y = y$, nicht $3y$."),
                               ("8xy", "$x$ und $y$ sind nicht gleichartig. Fasse nur $x$ mit $x$ und $y$ mit $y$ zusammen.")])

k.vereinfache("2x * 3x", "6x^2", form="vereinfacht",
              erklaerung="Zahlen mal Zahlen: $2 \\cdot 3 = 6$. Variablen mal Variablen: $x \\cdot x = x^2$.",
              tipps=["Hier wird malgenommen, nicht addiert.",
                     "Sortiere: $2 \\cdot 3 \\cdot x \\cdot x$.",
                     "$x \\cdot x = x^2$."],
              rechenweg=r"""
              :::rechnung
              2x \cdot 3x = 2 \cdot 3 \cdot x \cdot x || Zahlen nach vorn
              = 6x^2 || ausrechnen
              :::
              """,
              typische_fehler=[("5x", "Du hast addiert: $2x + 3x = 5x$. Gefragt ist aber **mal**."),
                               ("6x", "Ein $x$ ist verloren gegangen: $x \\cdot x = x^2$, nicht $x$."),
                               ("5x^2", "Die Zahlen werden auch malgenommen: $2 \\cdot 3 = 6$.")])

k.mc("Welcher Term ist gleich $x + x + x$?",
     ["$3x$", "$x^3$", "$3 + x$"],
     "Dreimal $x$ addiert ist $3 \\cdot x = 3x$. $x^3 = x \\cdot x \\cdot x$ wäre dreimal **malgenommen**.",
     tipps=["Plus oder mal?", "Dreimal dieselbe Zahl addieren heißt: mal $3$."],
     fehler={"$x^3$": "$x^3$ heißt $x \\cdot x \\cdot x$. Hier wird aber addiert: $x + x + x = 3x$.",
             "$3 + x$": "Setz $x = 10$ ein: $x + x + x = 30$, aber $3 + x = 13$."})

# ── 2: Ausmultiplizieren ───────────────────────────────────────────────────
k.erklaerung("Klammern auflösen", r"""
    ## Ausmultiplizieren: jeder bekommt etwas

    :::analogie 🎁 Geschenktüten
    Du packst $3$ Tüten. In jede kommen $2$ Äpfel und $1$ Birne. Zusammen sind das
    $6$ Äpfel und $3$ Birnen. Die $3$ wirkt auf **alles** in der Tüte.
    :::

    [[Ausmultiplizieren]] heißt: Der Faktor vor der Klammer wird mit **jedem**
    Summanden in der Klammer malgenommen. Diese Regel heißt [[Distributivgesetz]]:
    $a(b + c) = ab + ac$.

    :::rechnung Beispiel vorgerechnet
    3(2x + 1) = 3 \cdot 2x + 3 \cdot 1 || $3$ mit jedem Summanden malnehmen
    = 6x + 3 || ausrechnen
    -2(x - 4) = -2 \cdot x + (-2) \cdot (-4) || auch das Minus gehört zum Faktor
    = -2x + 8 || minus mal minus gibt plus
    :::

    :::achtung Nur den ersten Summanden malnehmen
    $3(x + 2) = 3x + 2$ ist falsch. Die $2$ steckt auch in der Klammer und bekommt
    ihre $3$ ab: $3x + 6$. Und bei $-2(x - 4)$ ergibt $(-2) \cdot (-4)$ **plus** $8$.
    :::

    :::alt Mit einem Rechteck erklärt
    Ein Rechteck ist $3$ hoch und $2x + 1$ breit. Schneide es senkrecht in zwei
    Teile: eines $2x$ breit, eines $1$ breit. Die Flächen sind $3 \cdot 2x = 6x$ und
    $3 \cdot 1 = 3$. Zusammen $6x + 3$, also genau $3(2x + 1)$.
    :::
    ---
    ## Klammer mal Klammer

    Bei $(a + b)(c + d)$ multiplizierst du **jeden** Summanden der ersten Klammer mit
    **jedem** Summanden der zweiten. Das sind $2 \cdot 2 = 4$ Produkte.

    :::rechnung Beispiel vorgerechnet
    (x + 2)(x + 3) = x \cdot x + x \cdot 3 + 2 \cdot x + 2 \cdot 3 || jeder mit jedem: $4$ Produkte
    = x^2 + 3x + 2x + 6 || Produkte ausrechnen
    = x^2 + 5x + 6 || gleichartige Terme zusammenfassen
    :::

    :::achtung Nur Erstes mit Erstem
    $(x + 2)(x + 3) = x^2 + 6$ ist falsch. Es fehlen die gemischten Produkte
    $3x$ und $2x$. Probe mit $x = 1$: links $3 \cdot 4 = 12$, rechts $1 + 6 = 7$.
    :::

    :::alt Mit einem Gitter erklärt
    Zeichne eine Tabelle: oben stehen $x$ und $3$, links stehen $x$ und $2$. In jedes
    der $4$ Felder schreibst du das Produkt aus Zeile und Spalte: $x^2$, $3x$, $2x$,
    $6$. Die Summe aller Felder ist das Ergebnis. So vergisst du kein Produkt.
    :::
    """)

k.vereinfache("3(2x + 1) - 2(x - 4)", "4x + 11", form="ausmultipliziert",
              frage="Multipliziere aus und fasse zusammen: $\\displaystyle {term}$.",
              erklaerung="$3(2x + 1) = 6x + 3$ und $-2(x - 4) = -2x + 8$. Zusammen $4x + 11$.",
              tipps=["Löse jede Klammer einzeln auf.",
                     "Die $-2$ gehört zum zweiten Faktor: $-2 \\cdot x$ und $-2 \\cdot (-4)$.",
                     "$6x + 3 - 2x + 8$. Jetzt zusammenfassen."],
              rechenweg=r"""
              :::rechnung
              3(2x + 1) - 2(x - 4) = 6x + 3 - 2x + 8 || beide Klammern ausmultiplizieren
              = 4x + 11 || zusammenfassen
              :::
              """,
              typische_fehler=[("4x - 5", "Vorzeichenfehler: $-2 \\cdot (-4) = +8$, nicht $-8$."),
                               ("4x + 1", "Du hast nur den ersten Summanden in der Klammer malgenommen. Jeder Summand bekommt den Faktor ab.")])

k.vereinfache("(x + 2)(x + 3)", "x^2 + 5x + 6", form="ausmultipliziert",
              frage="Multipliziere aus: $\\displaystyle {term}$.",
              erklaerung="Jeder mit jedem: $x^2 + 3x + 2x + 6 = x^2 + 5x + 6$.",
              tipps=["Wie viele Produkte entstehen bei zwei Summanden mal zwei Summanden?",
                     "Vier Produkte: $x \\cdot x$, $x \\cdot 3$, $2 \\cdot x$, $2 \\cdot 3$.",
                     "$x^2 + 3x + 2x + 6$. Jetzt zusammenfassen."],
              rechenweg=r"""
              :::rechnung
              (x + 2)(x + 3) = x^2 + 3x + 2x + 6 || jeder mit jedem
              = x^2 + 5x + 6 || zusammenfassen
              :::
              """,
              typische_fehler=[("x^2 + 6", "Die gemischten Produkte $x \\cdot 3$ und $2 \\cdot x$ fehlen. Jeder Summand wird mit jedem malgenommen."),
                               ("x^2 + 6x + 5", "Du hast $2 + 3$ und $2 \\cdot 3$ vertauscht: Vor dem $x$ steht die Summe $5$, hinten das Produkt $6$.")])

# ── 3: Binomische Formeln ──────────────────────────────────────────────────
k.erklaerung("Die binomischen Formeln", r"""
    ## Die erste binomische Formel

    $(a + b)^2$ heißt $(a + b)(a + b)$. Multiplizierst du aus, kommt immer dasselbe
    Muster heraus. Diese Abkürzungen heißen [[binomische Formeln]].

    !! $(a + b)^2 = a^2 + 2ab + b^2$

    :::rechnung Beispiel vorgerechnet
    (x + 3)^2 = (x + 3)(x + 3) || Quadrat heißt: mit sich selbst mal
    = x^2 + 3x + 3x + 9 || jeder mit jedem
    = x^2 + 6x + 9 || zusammenfassen: das ist $a^2 + 2ab + b^2$ mit $a = x$, $b = 3$
    :::

    :::achtung Der teuerste Fehler im ganzen Studium
    $(a + b)^2 = a^2 + b^2$ ist falsch. Probe mit Zahlen: $(1 + 2)^2 = 9$, aber
    $1^2 + 2^2 = 5$. Es fehlt der Mittelteil $2ab$.
    :::

    :::alt Mit einem Quadrat erklärt
    Zeichne ein Quadrat mit der Seite $a + b$. Teile jede Seite in ein Stück $a$
    und ein Stück $b$. Es entstehen vier Teile: ein Quadrat $a^2$, ein Quadrat $b^2$
    und **zwei** Rechtecke mit je $ab$. Wer nur $a^2 + b^2$ schreibt, vergisst die
    beiden Rechtecke.
    :::
    ---
    ## Zweite und dritte binomische Formel

    | Formel | Name |
    |---|---|
    | $(a - b)^2 = a^2 - 2ab + b^2$ | zweite binomische Formel |
    | $(a + b)(a - b) = a^2 - b^2$ | dritte binomische Formel |

    :::rechnung Beispiel vorgerechnet
    (2x - 5)^2 = (2x)^2 - 2 \cdot 2x \cdot 5 + 5^2 || zweite Formel mit $a = 2x$, $b = 5$
    = 4x^2 - 20x + 25 || $(2x)^2 = 4x^2$, das Quadrat gilt auch für die $2$
    (x + 4)(x - 4) = x^2 - 4^2 || dritte Formel: die Mittelteile heben sich auf
    = x^2 - 16 || $4^2 = 16$
    :::

    :::achtung Hinten wird nicht minus
    Bei $(a - b)^2$ ist nur der Mittelteil negativ. $b^2$ ist immer positiv: $(-5)^2 = 25$.
    :::

    :::alt Mit Kopfrechnen erklärt
    Rechne $49^2$ im Kopf: $49^2 = (50 - 1)^2 = 2500 - 100 + 1 = 2401$. Oder
    $21 \cdot 19 = (20 + 1)(20 - 1) = 400 - 1 = 399$. Die binomischen Formeln sind
    Rechentricks: Sie zerlegen eine schwere Aufgabe in leichte Stücke.
    :::
    """)

k.vereinfache("(x + 3)^2", "x^2 + 6x + 9", form="ausmultipliziert",
              frage="Multipliziere mit der binomischen Formel aus: $\\displaystyle {term}$.",
              erklaerung="Erste binomische Formel mit $a = x$ und $b = 3$: $x^2 + 2 \\cdot x \\cdot 3 + 9 = x^2 + 6x + 9$.",
              tipps=["Welche binomische Formel passt?",
                     "$(a + b)^2 = a^2 + 2ab + b^2$ mit $a = x$ und $b = 3$.",
                     "Der Mittelteil ist $2 \\cdot x \\cdot 3 = 6x$."],
              rechenweg=r"""
              :::rechnung
              (x + 3)^2 = x^2 + 2 \cdot x \cdot 3 + 3^2 || erste binomische Formel
              = x^2 + 6x + 9 || ausrechnen
              :::
              """,
              typische_fehler=[("x^2 + 9", "Das ist der Klassiker $(a + b)^2 = a^2 + b^2$. Es fehlt der Mittelteil $2ab = 6x$."),
                               ("x^2 + 3x + 9", "Der Mittelteil heißt $2ab$, also $2 \\cdot x \\cdot 3 = 6x$. Die $2$ fehlt.")])

k.wf("Für alle Zahlen $a$ und $b$ gilt $(a + b)^2 = a^2 + b^2$.", False,
     "Gegenbeispiel: $a = 1$, $b = 2$. Links $(1 + 2)^2 = 9$, rechts $1 + 4 = 5$. Richtig ist "
     "$(a + b)^2 = a^2 + 2ab + b^2$.",
     tipps=["Probiere es mit $a = 1$ und $b = 2$ aus."])

k.luecke("Ergänze die zweite binomische Formel:",
         "(2x - 5)^2 = 4x^2 - \\luecke \\, x + 25", [[20]],
         "Der Mittelteil ist $2ab = 2 \\cdot 2x \\cdot 5 = 20x$. Er bekommt das Minus.",
         tipps=["$(a - b)^2 = a^2 - 2ab + b^2$. Was ist hier $a$, was ist $b$?",
                "$a = 2x$ und $b = 5$.", "$2 \\cdot 2x \\cdot 5$"],
         rechenweg=r"""
         :::rechnung
         (2x - 5)^2 = (2x)^2 - 2 \cdot 2x \cdot 5 + 5^2 || zweite binomische Formel
         = 4x^2 - 20x + 25 || ausrechnen
         :::
         """,
         typische_fehler=[([10], "Die $2$ in $2ab$ fehlt: $2 \\cdot 2x \\cdot 5 = 20x$."),
                          ([5], "Der Mittelteil ist $2ab$, nicht nur $b$.")])

k.vereinfache("(x + 4)(x - 4)", "x^2 - 16", form="ausmultipliziert",
              frage="Multipliziere aus: $\\displaystyle {term}$.",
              erklaerung="Dritte binomische Formel: $(a + b)(a - b) = a^2 - b^2 = x^2 - 16$.",
              tipps=["Die Klammern unterscheiden sich nur im Vorzeichen.",
                     "Dritte binomische Formel: $a^2 - b^2$.", "$x^2 - 4^2$"],
              rechenweg=r"""
              :::rechnung
              (x + 4)(x - 4) = x^2 - 4x + 4x - 16 || jeder mit jedem
              = x^2 - 16 || die Mittelteile heben sich auf
              :::
              """,
              typische_fehler=[("x^2 + 16", "Das letzte Produkt ist $4 \\cdot (-4) = -16$."),
                               ("x^2 - 8x + 16", "Das wäre $(x - 4)^2$. Hier sind die Vorzeichen in den Klammern verschieden: dritte Formel.")])

k.zuordnen("Ordne jedem Term seine ausmultiplizierte Form zu.",
           [("$(a + b)^2$", "a² + 2ab + b²"), ("$(a - b)^2$", "a² − 2ab + b²"),
            ("$(a + b)(a - b)$", "a² − b²")],
           "Erste Formel: Plus in der Mitte. Zweite: Minus in der Mitte. Dritte: kein Mittelteil.",
           ablenker=["a² + b²"],
           tipps=["Nur die dritte Formel hat keinen Mittelteil. Und $a^2 + b^2$ passt zu keiner."])

# ── 4: Ausklammern ─────────────────────────────────────────────────────────
k.erklaerung("Ausklammern", r"""
    ## Rückwärts: den gemeinsamen Faktor herausziehen

    :::analogie 🧺 Wäschekorb
    In $6$ Hosen und $9$ Socken steckt eine $3$: Du kannst alles auf $3$ gleiche
    Körbe verteilen, in jedem liegen $2$ Hosen und $3$ Socken.
    :::

    [[Ausklammern]] ist Ausmultiplizieren rückwärts. Du suchst einen Faktor, der in
    **jedem** Summanden steckt, und schreibst ihn vor die Klammer.

    :::rechnung Beispiel vorgerechnet
    6x + 9 = 3 \cdot 2x + 3 \cdot 3 || in beiden Summanden steckt $3$
    = 3(2x + 3) || $3$ vor die Klammer
    x^2 - 4x = x \cdot x - x \cdot 4 || in beiden steckt $x$
    = x(x - 4) || $x$ vor die Klammer
    x^2 - 9 = x^2 - 3^2 || binomische Formel rückwärts erkennen
    = (x + 3)(x - 3) || dritte binomische Formel
    :::

    :::achtung Den Rest in der Klammer vergessen
    $x^2 + x = x(x)$ ist falsch. Aus $x$ wird beim Ausklammern $x \cdot 1$, die $1$
    bleibt stehen: $x(x + 1)$.
    :::

    :::alt Mit der Probe erklärt
    Ob du richtig ausgeklammert hast, siehst du sofort: Multipliziere wieder aus.
    $3(2x + 3) = 6x + 9$. Kommt der Ausgangsterm heraus, stimmt es. So wird jede
    Ausklammer-Aufgabe zu einer Ausmultiplizier-Aufgabe, die du schon kannst.
    :::
    """)

k.term("Klammere den größten gemeinsamen Faktor aus: $6x + 9$.", "3(2x + 3)",
       "In $6x$ und in $9$ steckt die $3$: $6x + 9 = 3(2x + 3)$.", variablen="x", form="faktorisiert",
       tipps=["Welche Zahl teilt $6$ und $9$?", "Der ggT ist $3$. Teile jeden Summanden durch $3$.",
              "$6x : 3 = 2x$ und $9 : 3 = 3$."],
       rechenweg=r"""
       :::rechnung
       6x + 9 = 3 \cdot 2x + 3 \cdot 3 || $3$ steckt in beiden Summanden
       = 3(2x + 3) || ausklammern
       :::
       """,
       typische_fehler=[("3(2x + 9)", "Auch die $9$ muss durch $3$ geteilt werden: $9 : 3 = 3$."),
                        ("3(3x + 3)", "$6x : 3 = 2x$, nicht $3x$.")])

k.term("Faktorisiere mit einer binomischen Formel: $x^2 - 25$.", "(x + 5)(x - 5)",
       "$x^2 - 25 = x^2 - 5^2$. Das ist die rechte Seite der dritten binomischen Formel: $(x + 5)(x - 5)$.",
       variablen="x", form="faktorisiert",
       tipps=["Schreibe $25$ als Quadrat.", "$x^2 - 5^2$ hat die Form $a^2 - b^2$.",
              "$a^2 - b^2 = (a + b)(a - b)$"],
       rechenweg=r"""
       :::rechnung
       x^2 - 25 = x^2 - 5^2 || $25 = 5^2$
       = (x + 5)(x - 5) || dritte binomische Formel rückwärts
       :::
       """,
       typische_fehler=[("(x - 5)^2", "$(x - 5)^2 = x^2 - 10x + 25$. Das ist die zweite Formel, nicht die dritte."),
                        ("(x + 5)^2", "$(x + 5)^2$ hat einen Mittelteil $10x$. Bei $x^2 - 25$ gibt es keinen.")])

# ── 5: Bruchterme kürzen ───────────────────────────────────────────────────
k.erklaerung("Bruchterme kürzen", r"""
    ## Nur Faktoren kürzen, nie Summanden

    Ein [[Bruchterm]] ist ein Bruch mit Variablen, zum Beispiel $\frac{4x + 8}{4}$.
    Kürzen darfst du nur, wenn oben und unten ein **Produkt** steht. Deshalb wird
    zuerst ausgeklammert, dann gekürzt.

    :::rechnung Beispiel vorgerechnet
    \frac{4x + 8}{4} = \frac{4(x + 2)}{4} || Zähler ausklammern: jetzt ein Produkt
    = x + 2 || den Faktor $4$ kürzen
    \frac{x^2 - 9}{x + 3} = \frac{(x + 3)(x - 3)}{x + 3} || dritte binomische Formel im Zähler
    = x - 3 || den Faktor $(x + 3)$ kürzen, gilt für $x \neq -3$
    :::

    :::achtung Aus Summen kürzen
    $\frac{x + 3}{3} = x$ ist falsch. Die $3$ ist oben ein Summand, kein Faktor.
    Probe mit $x = 3$: links $\frac{6}{3} = 2$, rechts $3$.
    :::

    :::alt Mit Pizzastücken erklärt
    $\frac{4x + 8}{4}$ heißt: $4x + 8$ wird auf $4$ Leute verteilt. Jeder bekommt
    von **allem** ein Viertel: $x$ und $2$. Wer nur bei $4x$ kürzt, gibt einem Gast
    alle $8$ Stücke vom Rest und den anderen nichts.
    :::
    """)

k.vereinfache("(4x + 8)/4", "x + 2", form="vereinfacht",
              frage="Kürze: $\\displaystyle {term}$.",
              erklaerung="$4x + 8 = 4(x + 2)$. Dann kürzt sich die $4$: $x + 2$.",
              tipps=["Kürzen geht nur mit Faktoren. Steht oben ein Produkt?",
                     "Klammere im Zähler $4$ aus.", "$\\frac{4(x + 2)}{4}$"],
              rechenweg=r"""
              :::rechnung
              \frac{4x + 8}{4} = \frac{4(x + 2)}{4} || ausklammern
              = x + 2 || $4$ kürzen
              :::
              """,
              typische_fehler=[("x + 8", "Du hast nur die $4$ bei $4x$ gekürzt. Die $8$ muss auch durch $4$ geteilt werden."),
                               ("4x + 2", "Du hast nur die $8$ durch $4$ geteilt. Jeder Summand im Zähler wird geteilt.")])

k.mc("Welche Umformung ist richtig?",
     ["$\\frac{x^2 - 9}{x + 3} = x - 3$ für $x \\neq -3$",
      "$\\frac{x + 3}{3} = x$",
      "$\\frac{x^2 + 9}{x + 3} = x + 3$"],
     "Nur beim ersten Term steht oben ein Produkt mit dem Faktor $(x + 3)$: $x^2 - 9 = (x + 3)(x - 3)$. "
     "Bei den anderen wird aus einer Summe gekürzt.",
     tipps=["Kürzen darfst du nur Faktoren.", "Welcher Zähler lässt sich als Produkt mit $(x + 3)$ schreiben?"],
     fehler={"$\\frac{x + 3}{3} = x$": "Die $3$ ist im Zähler ein Summand. Probe mit $x = 3$: $\\frac{6}{3} = 2 \\neq 3$.",
             "$\\frac{x^2 + 9}{x + 3} = x + 3$": "$x^2 + 9$ lässt sich nicht in Faktoren zerlegen, nur $x^2 - 9$. Probe mit $x = 1$: $\\frac{10}{4} \\neq 4$."})


# ── Praxis ─────────────────────────────────────────────────────────────────
def _vz(z):
    """+ 3 / - 3 zum Anhängen an einen Term."""
    return f"+ {z}" if z >= 0 else f"- {-z}"


def _lin(a, b):
    """a x + b als Text (für Parser und Anzeige)."""
    ax = "x" if a == 1 else "-x" if a == -1 else f"{a}x"
    return ax if b == 0 else f"{ax} {_vz(b)}"


def _ptext(p):
    """Polynom mit ganzen Koeffizienten -> Eingabetext wie '4x^2 - 20x + 25'."""
    teile = []
    for e in sorted(p.k, reverse=True):
        c = int(p.k[e])
        x = "" if e == 0 else "x" if e == 1 else f"x^{e}"
        betrag = abs(c)
        stueck = (str(betrag) if betrag != 1 or e == 0 else "") + x
        if not teile:
            teile.append(("-" if c < 0 else "") + stueck)
        else:
            teile.append(("- " if c < 0 else "+ ") + stueck)
    return " ".join(teile) if teile else "0"


def _anhaengen(tex):
    """'-2x + 8' -> '- 2x + 8', '6x' -> '+ 6x' (zum Anhängen an einen Term)."""
    return "- " + tex[1:] if tex.startswith("-") else "+ " + tex


def _ohne_aequivalente(loesung, fehler):
    """Fehlterme, die zufällig zur Lösung äquivalent oder doppelt sind, entfernen."""
    soll = pruefer.parse(loesung, ["x"]).ast
    erg, gesehen = [], []
    for w, m in fehler:
        ast = pruefer.parse(w, ["x"]).ast
        if pruefer.aequivalent(ast, soll, ["x"]).ok or any(pruefer.aequivalent(ast, g, ["x"]).ok for g in gesehen):
            continue
        gesehen.append(ast)
        erg.append((w, m))
    return erg


def ausmultiplizieren_zusammenfassen(rng):
    while True:
        a, d = rng.choice([2, 3, 4, 5]), rng.choice([-5, -4, -3, -2, 2, 3, 4])
        b, e = rng.randint(1, 4), rng.randint(1, 4)
        c = rng.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
        f = rng.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
        if a * b + d * e != 0 and a * c + d * f != 0:
            break
    aufgabe = f"{a}({_lin(b, c)}) {'+' if d > 0 else '-'} {abs(d)}({_lin(e, f)})"
    p1, p2 = _p(f"{a}*({_lin(b, c)})"), _p(f"{d}*({_lin(e, f)})")
    loes = p1 + p2
    zw = f"{p1.tex()} {_anhaengen(p2.tex())}"
    fehler = [(_ptext(p1 + _p(f"{d * e}x - {d * f}")),
               f"Vorzeichenfehler beim zweiten Produkt: ${tex_kl(d)} \\cdot {tex_kl(f)} = {d * f}$."),
              (_ptext(_p(f"{a * b}x + {c} + {d * e}x + {f}")),
               "Du hast nur den ersten Summanden in den Klammern malgenommen. Jeder Summand bekommt den Faktor ab.")]
    if d > 0 and f > 0:
        fehler = fehler[1:]          # ohne Minus gibt es keinen Vorzeichenfehler
    return {
        "frage": f"Multipliziere aus und fasse zusammen: ${_tex(aufgabe)}$.",
        "loesung": _ptext(loes), "variablen": "x", "form": "ausmultipliziert",
        "tipps": ["Löse jede Klammer einzeln auf.",
                  f"Der zweite Faktor ist ${d}$: Das Vorzeichen gehört dazu.",
                  f"Nach dem Auflösen: ${zw}$. Jetzt zusammenfassen."],
        "rechenweg": _zeilen((f"{_tex(aufgabe)} = {zw}", "beide Klammern ausmultiplizieren"),
                             (f"= {loes.tex()}", "gleichartige Terme zusammenfassen")),
        "erklaerung": "Jeder Summand in der Klammer wird mit dem Faktor davor malgenommen, das Vorzeichen des Faktors inklusive.",
        "typische_fehler": _ohne_aequivalente(_ptext(loes), fehler),
    }


def tex_kl(z):
    return mathlib.tex_klammer(z)


def binomisch_ausmultiplizieren(rng):
    a = rng.choice([1, 1, 2, 3])
    b = rng.randint(1, 9)
    art = rng.choice(["plus", "minus", "dritte"])
    ax = "x" if a == 1 else f"{a}x"
    axq = "x" if a == 1 else f"({a}x)"            # (2x)^2 in der Formel
    if art == "plus":
        aufgabe = f"({ax} + {b})^2"
        formel = f"{axq}^2 + 2 \\cdot {ax} \\cdot {b} + {b}^2"
        name = "erste binomische Formel"
    elif art == "minus":
        aufgabe = f"({ax} - {b})^2"
        formel = f"{axq}^2 - 2 \\cdot {ax} \\cdot {b} + {b}^2"
        name = "zweite binomische Formel"
    else:
        aufgabe = f"({ax} + {b})({ax} - {b})"
        formel = f"{axq}^2 - {b}^2"
        name = "dritte binomische Formel"
    loes = _p(aufgabe)
    a2, mitte, b2 = a * a, 2 * a * b, b * b
    vz = "+" if art == "plus" else "-"
    if art in ("plus", "minus"):
        fehler = [(f"{a2}x^2 + {b2}", "Der Mittelteil $2ab$ fehlt. $(a \\pm b)^2$ ist **nicht** $a^2 \\pm b^2$."),
                  (f"{a2}x^2 {vz} {a * b}x + {b2}", "Der Mittelteil heißt $2ab$: Die $2$ fehlt.")]
        if art == "minus":
            fehler.append((f"{a2}x^2 - {mitte}x - {b2}", "Das letzte Glied ist $b^2$, und ein Quadrat ist nie negativ."))
        if a > 1:
            fehler.append((f"{a}x^2 {vz} {mitte}x + {b2}", f"Das Quadrat gilt für den ganzen Faktor: $({a}x)^2 = {a2}x^2$."))
    else:
        fehler = [(f"{a2}x^2 + {b2}", f"Das letzte Produkt ist ${b} \\cdot (-{b}) = -{b2}$."),
                  (f"{a2}x^2 - {mitte}x + {b2}", "Das wäre $(a - b)^2$. Bei verschiedenen Vorzeichen in den Klammern gilt die dritte Formel.")]
        if a > 1:
            fehler.append((f"{a}x^2 - {b2}", f"Das Quadrat gilt für den ganzen Faktor: $({a}x)^2 = {a2}x^2$."))
    return {
        "frage": f"Multipliziere mit einer binomischen Formel aus: ${_tex(aufgabe)}$.",
        "loesung": _ptext(loes), "variablen": "x", "form": "ausmultipliziert",
        "tipps": ["Welche der drei binomischen Formeln passt?",
                  f"Das ist die {name} mit $a = {ax}$ und $b = {b}$.",
                  f"Setze ein: ${formel}$."],
        "rechenweg": _zeilen((f"{_tex(aufgabe)} = {formel}", name),
                             (f"= {loes.tex()}", "ausrechnen")),
        "erklaerung": "Binomische Formeln: $(a + b)^2 = a^2 + 2ab + b^2$, $(a - b)^2 = a^2 - 2ab + b^2$, "
                      "$(a + b)(a - b) = a^2 - b^2$.",
        "typische_fehler": _ohne_aequivalente(_ptext(loes), fehler),
    }


k.praxis()

k.generator(ausmultiplizieren_zusammenfassen, typ="term", titel="Ausmultiplizieren und zusammenfassen")
k.generator(binomisch_ausmultiplizieren, typ="term", titel="Binomische Formeln anwenden")


def ausklammern(rng):
    while True:
        g = rng.choice([2, 3, 4, 5, 6, 7, 8])
        p, q = rng.randint(1, 7), rng.choice([-9, -7, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 7, 9])
        if math.gcd(p, abs(q)) == 1:
            break
    px = "" if p == 1 else str(p)
    if rng.random() < 0.35:     # g p x^2 + g q x = g x (p x + q)
        aufgabe = f"{g * p}x^2 {_vz(g * q)}x"
        faktor_tex = f"{g}x"
        loes = f"{g}x({_lin(p, q)})"
        zerlegt = f"{g}x \\cdot {px}x {'+' if q > 0 else '-'} {g}x \\cdot {abs(q)}"
        fehler = [(f"{g}({_lin(p, q)})", f"In beiden Summanden steckt auch ein $x$. Klammere ${g}x$ aus."),
                  (f"{g}x({px}x)", "Der zweite Summand fehlt in der Klammer.")]
        tipp2 = f"Gemeinsam sind die Zahl ${g}$ und ein $x$."
    else:
        aufgabe = f"{g * p}x {_vz(g * q)}"
        faktor_tex = str(g)
        loes = f"{g}({_lin(p, q)})"
        zerlegt = f"{g} \\cdot {px}x {'+' if q > 0 else '-'} {g} \\cdot {abs(q)}"
        fehler = [(f"{g}({_lin(p, g * q)})", f"Auch ${g * q}$ muss durch ${g}$ geteilt werden."),
                  (f"{g}({_lin(g * p, q)})", f"Auch ${g * p}x$ muss durch ${g}$ geteilt werden.")]
        tipp2 = f"Der größte gemeinsame Teiler von ${g * p}$ und ${abs(g * q)}$ ist ${g}$."
    return {
        "frage": f"Klammere den größten gemeinsamen Faktor aus: ${_tex(aufgabe)}$.",
        "loesung": loes, "variablen": "x", "form": "faktorisiert",
        "tipps": ["Was steckt in jedem Summanden?", tipp2, f"Teile jeden Summanden durch ${faktor_tex}$."],
        "rechenweg": _zeilen((f"{_tex(aufgabe)} = {zerlegt}", f"${faktor_tex}$ steckt in jedem Summanden"),
                             (f"= {_tex(loes)}", "ausklammern")),
        "erklaerung": "Ausklammern ist Ausmultiplizieren rückwärts. Probe: wieder ausmultiplizieren.",
        "typische_fehler": _ohne_aequivalente(loes, fehler),
    }


k.generator(ausklammern, typ="term", titel="Ausklammern")

k.vereinfache("(a + b)^2 - (a - b)^2", "4ab", variablen="a, b", form="vereinfacht",
              frage="Vereinfache so weit wie möglich: $\\displaystyle {term}$.",
              erklaerung="Erste und zweite binomische Formel, dann die Minusklammer: $a^2 + 2ab + b^2 - a^2 + 2ab - b^2 = 4ab$.",
              tipps=["Wende auf beide Quadrate eine binomische Formel an.",
                     "Vor dem zweiten Quadrat steht ein Minus: Setze sein Ergebnis in Klammern.",
                     "$(a^2 + 2ab + b^2) - (a^2 - 2ab + b^2)$"],
              rechenweg=r"""
              :::rechnung
              (a + b)^2 - (a - b)^2 = (a^2 + 2ab + b^2) - (a^2 - 2ab + b^2) || erste und zweite binomische Formel
              = a^2 + 2ab + b^2 - a^2 + 2ab - b^2 || Minusklammer: jedes Vorzeichen umdrehen
              = 4ab || $a^2$ und $b^2$ heben sich weg
              :::
              """,
              typische_fehler=[("0", "Du hast vermutlich $(a + b)^2 = a^2 + b^2$ gerechnet. Der Mittelteil $2ab$ ist wichtig."),
                               ("2b^2", "Die Minusklammer dreht **jedes** Vorzeichen um, auch das von $-2ab$."),
                               ("2a^2 + 2b^2", "Vor dem zweiten Quadrat steht ein Minus. Es gilt für die ganze Klammer.")])

# Übungsblatt-Stil: Bruchterm vollständig kürzen
k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: Bruchterm kürzen

    Vereinfachen Sie so weit wie möglich und geben Sie an, für welche $x$ die Umformung gilt:
    $$\frac{x^2 - 6x + 9}{x^2 - 9}$$
    """,
    [{"typ": "term", "frage": "Schreibe den Zähler $x^2 - 6x + 9$ als Produkt.", "loesung": "(x - 3)^2",
      "variablen": "x", "form": "faktorisiert",
      "tipps": ["Erkennst du eine binomische Formel?", "$9 = 3^2$ und $6x = 2 \\cdot x \\cdot 3$: zweite Formel."],
      "rechenweg": "$x^2 - 6x + 9 = x^2 - 2 \\cdot x \\cdot 3 + 3^2 = (x - 3)^2$",
      "typische_fehler": [("(x + 3)^2", "Der Mittelteil ist negativ: zweite binomische Formel, also $(x - 3)^2$."),
                          ("(x + 3)(x - 3)", "Das ist $x^2 - 9$. Der Zähler hat aber einen Mittelteil $-6x$.")]},
     {"typ": "term", "frage": "Schreibe den Nenner $x^2 - 9$ als Produkt.", "loesung": "(x + 3)(x - 3)",
      "variablen": "x", "form": "faktorisiert",
      "tipps": ["$9 = 3^2$.", "Dritte binomische Formel: $a^2 - b^2 = (a + b)(a - b)$."],
      "rechenweg": "$x^2 - 9 = x^2 - 3^2 = (x + 3)(x - 3)$",
      "typische_fehler": [("(x - 3)^2", "$(x - 3)^2$ hätte einen Mittelteil $-6x$. Hier hilft die dritte Formel.")]},
     {"typ": "term", "frage": "Kürze den gemeinsamen Faktor. Wie lautet der vereinfachte Bruchterm?",
      "loesung": "(x - 3)/(x + 3)", "variablen": "x", "form": "gekuerzt",
      "tipps": ["Oben steht $(x - 3)(x - 3)$, unten $(x + 3)(x - 3)$.", "Kürze einmal $(x - 3)$."],
      "rechenweg": "$\\frac{(x - 3)^2}{(x + 3)(x - 3)} = \\frac{x - 3}{x + 3}$ für $x \\neq 3$ und $x \\neq -3$",
      "typische_fehler": [("(x - 3)/(x - 3)", "Gekürzt wird der gemeinsame Faktor $(x - 3)$, einmal oben und einmal unten."),
                          ("-1", "Aus Summen darf man nicht kürzen: $\\frac{x - 3}{x + 3}$ ist nicht $-1$.")]}],
    "Erst Zähler und Nenner in Faktoren zerlegen (binomische Formeln), dann gemeinsame Faktoren kürzen. "
    "Die Umformung gilt nur, wo der ursprüngliche Nenner nicht $0$ ist: $x \\neq 3$ und $x \\neq -3$.",
    uebungsblatt=True,
    tipps=["Kürzen geht nur mit Faktoren: Zerlege Zähler und Nenner.",
           "Beide lassen sich mit binomischen Formeln zerlegen."],
    rechenweg=r"""
    :::rechnung
    \frac{x^2 - 6x + 9}{x^2 - 9} = \frac{(x - 3)^2}{(x + 3)(x - 3)} || zweite und dritte binomische Formel
    = \frac{(x - 3)(x - 3)}{(x + 3)(x - 3)} || Quadrat ausschreiben
    = \frac{x - 3}{x + 3} || den Faktor $(x - 3)$ kürzen, gilt für $x \neq 3$ und $x \neq -3$
    :::
    """)

k.zusammenfassung(r"""
    ## Terme umformen

    | Was | Regel | Beispiel |
    |---|---|---|
    | Zusammenfassen | nur gleichartige Terme | $3x + 2y + 4x = 7x + 2y$ |
    | Produkte | Zahlen zu Zahlen, Variablen zu Variablen | $2x \cdot 3x = 6x^2$ |
    | Ausmultiplizieren | Faktor mal jeden Summanden | $-2(x - 4) = -2x + 8$ |
    | Klammer mal Klammer | jeder mit jedem | $(x + 2)(x + 3) = x^2 + 5x + 6$ |
    | Ausklammern | gemeinsamen Faktor vor die Klammer | $6x + 9 = 3(2x + 3)$ |
    | Kürzen | nur Faktoren, nie Summanden | $\frac{4x + 8}{4} = x + 2$ |

    !! $(a + b)^2 = a^2 + 2ab + b^2$, $(a - b)^2 = a^2 - 2ab + b^2$, $(a + b)(a - b) = a^2 - b^2$

    - $(a + b)^2 \neq a^2 + b^2$: Probe mit $a = 1$, $b = 2$ ergibt $9 \neq 5$.
    - Jede Umformung kannst du mit einer Probe prüfen: Zahl einsetzen, beide Seiten vergleichen.
""")
