# -*- coding: utf-8 -*-
"""Vorkurs 6: Fakultät und Binomialkoeffizient – n!, (n über k), Pascalsches Dreieck, Symmetrie."""
import math
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

fak = math.factorial
B = mathlib.binom          # (n über k), 0 für k > n

# Alle Behauptungen dieses Kapitels rechnet Python nach.
assert fak(4) == 24 and fak(0) == 1 and fak(5) == 120
assert F(fak(7), fak(5)) == 42 and F(fak(8), fak(6)) == 56
assert B(5, 2) == 10 and B(4, 2) == 6 and B(10, 8) == B(10, 2) == 45 and B(4, 6) == 0
assert B(7, 3) == 35 and B(20, 18) == 190 and B(8, 3) == 56 and B(49, 6) == 13983816
assert sum(j for j in range(-3, 4)) * 5 == 0
for _n in range(0, 30):
    assert fak(_n + 1) == (_n + 1) * fak(_n)
    assert sum(B(_n, _k) for _k in range(_n + 1)) == 2 ** _n
    for _k in range(0, _n + 3):
        _def = F(fak(_n), fak(_n - _k) * fak(_k)) if _k <= _n else 0
        assert B(_n, _k) == _def == math.comb(_n, _k)
        if _k <= _n:
            assert B(_n, _k) == B(_n, _n - _k)
        if 1 <= _k <= _n:
            assert B(_n, _k - 1) + B(_n, _k) == B(_n + 1, _k)
            # Zwischenschritte der Musterlösung (Pascal-Regel)
            assert F(fak(_n) * _k, fak(_n - _k + 1) * fak(_k)) + F(fak(_n) * (_n - _k + 1), fak(_n - _k + 1) * fak(_k)) \
                == F(fak(_n + 1), fak(_n + 1 - _k) * fak(_k))
    for _a in range(-3, 4):
        for _b in range(-3, 4):
            assert (_a + _b) ** _n == sum(B(_n, _k) * _a ** (_n - _k) * _b ** _k for _k in range(_n + 1))

k = neues_kapitel(
    slug="binomial",
    titel="Fakultät und Binomialkoeffizient",
    beschreibung="n!, „n über k“, Auswahlen zählen, Symmetrie und das Pascalsche Dreieck",
    teil="vorkurs",
    quelle="MVK 2026, VL 2–3",
    icon="🔺")

k.lernziele([
    "Ich kann $n!$ ausrechnen und Brüche mit Fakultäten kürzen",
    "Ich kann $\\binom{n}{k}$ mit der Definition der TU ausrechnen, auch für $k = 0$ und $k > n$",
    "Ich kann $\\binom{n}{k}$ als Anzahl der Auswahlen von $k$ aus $n$ Dingen deuten",
    "Ich kenne die Symmetrie $\\binom{n}{k} = \\binom{n}{n-k}$ und die Regel des Pascalschen Dreiecks",
])

k.warum(r"""
Wie viele Passwörter, Schlüssel oder Bitfolgen gibt es? Solche Zählfragen
beantworten Fakultät und Binomialkoeffizient. Ein Byte mit genau drei Einsen gibt
es $\binom{8}{3} = 56$-mal. Wie viele Reihenfolgen probiert ein Sortieralgorithmus
im schlimmsten Fall durch? $n!$, und das wächst so schnell, dass schon $20!$ nicht
mehr in 32 Bit passt. In Python: `math.factorial(n)` und `math.comb(n, k)`.
""")

# ── 1: Fakultät ────────────────────────────────────────────────────────────
k.erklaerung("Fakultät", r"""
    ## Wie viele Reihenfolgen gibt es?

    :::analogie 📚 Bücherregal
    Drei Bücher sollen ins Regal. Für den ersten Platz hast du $3$ Bücher zur
    Wahl, dann noch $2$, dann $1$. Das sind $3 \cdot 2 \cdot 1 = 6$ Reihenfolgen.
    :::

    Für $n \in \mathbb{N}_0$ heißt $n!$ die [[Fakultät]] („n Fakultät“):

    $$n! := \prod_{k=1}^{n} k = 1 \cdot 2 \cdot \ldots \cdot n$$

    Für $n = 0$ ist das ein [[leeres Produkt]], also gilt $0! = 1$.

    :::rechnung Beispiel vorgerechnet
    4! = 1 \cdot 2 \cdot 3 \cdot 4 || alle Zahlen von $1$ bis $4$ malnehmen
    = 24 || ausrechnen
    0! = 1 || leeres Produkt
    :::

    :::alt Mit einer Warteschlange erklärt
    Vier Leute stellen sich an. Wer vorne steht: $4$ Möglichkeiten. Dahinter
    bleiben $3$, dann $2$, dann $1$. Jede Wahl lässt sich mit jeder späteren
    kombinieren, deshalb wird malgenommen: $4 \cdot 3 \cdot 2 \cdot 1 = 24$.
    Null Leute kann man auf genau eine Art anstellen: gar nicht. Daher $0! = 1$.
    :::
    ---
    ## Fakultäten kürzen

    Jede Fakultät enthält die kleinere: $n! = n \cdot (n - 1)!$. Damit kürzt du
    Brüche, ohne riesige Zahlen auszurechnen.

    :::rechnung Beispiel vorgerechnet
    \frac{7!}{5!} = \frac{7 \cdot 6 \cdot 5!}{5!} || $7! = 7 \cdot 6 \cdot 5!$
    = 7 \cdot 6 || $5!$ kürzen
    = 42 || ausrechnen
    :::

    Allgemein gilt zum Beispiel $\frac{(n+1)!}{n!} = n + 1$.

    :::achtung Fakultäten sind keine normalen Zahlen
    $\frac{6!}{3!}$ ist **nicht** $2!$. Richtig: $\frac{6!}{3!} = 6 \cdot 5 \cdot 4 = 120$.
    Und $(2n)!$ ist **nicht** $2 \cdot n!$: $(2 \cdot 3)! = 720$, aber $2 \cdot 3! = 12$.
    :::

    :::alt Mit Treppenstufen erklärt
    $7!$ ist eine Treppe aus den Stufen $1$ bis $7$, $5!$ die Treppe bis $5$.
    Teilst du die eine durch die andere, bleiben nur die Stufen übrig, die
    $5!$ nicht hat: $6$ und $7$.
    :::
    """)

k.zahl("Berechne $5!$.", fak(5), "$5! = 1 \\cdot 2 \\cdot 3 \\cdot 4 \\cdot 5 = 120$.",
       tipps=["$n!$ heißt: alle Zahlen von $1$ bis $n$ malnehmen.", "$1 \\cdot 2 \\cdot 3 \\cdot 4 \\cdot 5$",
              "$4! = 24$, und $5! = 5 \\cdot 4!$."],
       rechenweg=r"""
       :::rechnung
       5! = 1 \cdot 2 \cdot 3 \cdot 4 \cdot 5 || Definition
       = 120 || ausrechnen
       :::
       """,
       typische_fehler=[(15, "Du hast addiert. Die Fakultät ist ein Produkt: $1 \\cdot 2 \\cdot 3 \\cdot 4 \\cdot 5$."),
                        (24, "Das ist $4!$. Die $5$ gehört auch noch dazu.")])

k.zahl("Berechne $0!$.", fak(0), "$0!$ ist ein leeres Produkt, also $1$.",
       tipps=["Schreib $0!$ als Produkt: $\\prod_{k=1}^{0} k$.", "Untere Grenze $1$, obere $0$: Es gibt keinen Faktor.",
              "Das leere Produkt ist $1$."],
       rechenweg=r"""
       :::rechnung
       0! = 1 || leeres Produkt
       :::
       """,
       typische_fehler=[(0, "Beim leeren Produkt wird gar nichts malgenommen, es bleibt der Startwert $1$. Außerdem passt nur $0! = 1$ zu $1! = 1 \\cdot 0!$.")])

k.zahl("Berechne $\\dfrac{8!}{6!}$, ohne $8!$ auszurechnen.", F(fak(8), fak(6)),
       "$\\frac{8!}{6!} = \\frac{8 \\cdot 7 \\cdot 6!}{6!} = 8 \\cdot 7 = 56$.",
       tipps=["Schreibe $8! = 8 \\cdot 7 \\cdot 6!$.", "Dann kürzt sich $6!$.", "$8 \\cdot 7$"],
       rechenweg=r"""
       :::rechnung
       \frac{8!}{6!} = \frac{8 \cdot 7 \cdot 6!}{6!} || $8! = 8 \cdot 7 \cdot 6!$
       = 8 \cdot 7 || $6!$ kürzen
       = 56 || ausrechnen
       :::
       """,
       typische_fehler=[(2, "Fakultäten kürzt man nicht wie Zahlen: $\\frac{8!}{6!}$ ist nicht $(8 - 6)!$."),
                        (336, "Die $6$ steckt in $6!$ und kürzt sich weg. Es bleiben nur $8 \\cdot 7$.")])

k.term("Vereinfache $\\dfrac{(n+1)!}{n!}$ für $n \\in \\mathbb{N}_0$ so, dass keine Fakultät mehr vorkommt.", "n+1",
       "$(n+1)! = (n+1) \\cdot n!$, also bleibt nach dem Kürzen $n + 1$.", variablen="n",
       tipps=["Schreibe $(n+1)!$ mit Hilfe von $n!$.", "$(n+1)! = (n+1) \\cdot n!$", "Jetzt $n!$ kürzen."],
       rechenweg=r"""
       Es gilt $(n+1)! = (n+1) \cdot n!$, also
       $$\frac{(n+1)!}{n!} = \frac{(n+1) \cdot n!}{n!} = n + 1.$$
       """,
       typische_fehler=[("n", "$(n+1)! = (n+1) \\cdot n!$: Nach dem Kürzen bleibt der Faktor $n + 1$, nicht $n$."),
                        ("1", "Die Fakultäten sind nicht gleich: $(n+1)!$ hat einen Faktor mehr als $n!$.")])

# ── 2: Binomialkoeffizient ─────────────────────────────────────────────────
k.erklaerung("Der Binomialkoeffizient", r"""
    ## n über k

    Für $n, k \in \mathbb{N}_0$ definiert die TU den [[Binomialkoeffizient]]en:

    $$\binom{n}{k} := \begin{cases} \dfrac{n!}{(n-k)! \cdot k!} & \text{falls } 0 \le k \le n, \\ 0 & \text{falls } k > n. \end{cases}$$

    Gelesen: „n über k“. Oben steht $n$, unten $k$, ohne Bruchstrich.

    :::rechnung Beispiel vorgerechnet
    \binom{5}{2} = \frac{5!}{(5-2)! \cdot 2!} || Definition, $k = 2 \le 5 = n$
    \frac{5!}{3! \cdot 2!} = \frac{5 \cdot 4 \cdot 3!}{3! \cdot 2!} || $5! = 5 \cdot 4 \cdot 3!$
    = \frac{5 \cdot 4}{2} || $3!$ kürzen, $2! = 2$
    = 10 || ausrechnen
    :::

    Schneller Trick: Oben $k$ Faktoren abwärts ab $n$, unten $k!$. Also
    $\binom{5}{2} = \frac{5 \cdot 4}{1 \cdot 2}$.

    :::achtung Kein Bruch
    $\binom{5}{2}$ ist nicht $\frac{5}{2}$. Und für $k > n$ ist der Wert $0$,
    nicht „undefiniert“: $\binom{4}{6} = 0$.
    :::

    :::alt Mit Kürzen erklärt
    $5!$ zählt alle Reihenfolgen von $5$ Dingen. Du willst aber nur wissen,
    **welche** $2$ vorne stehen. Die Reihenfolge der $3$ hinteren ($3!$) und der
    $2$ vorderen ($2!$) ist egal. Deshalb teilst du durch beides.
    :::
    """)

k.zahl("Berechne $\\displaystyle\\binom{5}{2}$.", B(5, 2), "$\\binom{5}{2} = \\frac{5!}{3! \\cdot 2!} = \\frac{5 \\cdot 4}{2} = 10$.",
       tipps=["Definition: $\\frac{n!}{(n-k)! \\cdot k!}$ mit $n = 5$, $k = 2$.", "$\\frac{5!}{3! \\cdot 2!}$",
              "$3!$ kürzen: $\\frac{5 \\cdot 4}{2}$."],
       rechenweg=r"""
       :::rechnung
       \binom{5}{2} = \frac{5!}{3! \cdot 2!} || Definition
       \frac{5!}{3! \cdot 2!} = \frac{5 \cdot 4}{2} || $3!$ kürzen
       = 10 || ausrechnen
       :::
       """,
       typische_fehler=[(F(5, 2), "$\\binom{5}{2}$ ist kein Bruch. Rechne $\\frac{5!}{3! \\cdot 2!}$."),
                        (20, "Du hast $5 \\cdot 4$ nicht mehr durch $2! = 2$ geteilt.")])

k.zahl("Berechne $\\displaystyle\\binom{4}{6}$.", B(4, 6), "Hier ist $k = 6 > 4 = n$. Nach Definition ist der Wert $0$.",
       tipps=["Vergleiche $k$ und $n$.", "$6 > 4$", "Für $k > n$ legt die Definition einen festen Wert fest."],
       rechenweg=r"""
       :::rechnung
       \binom{4}{6} = 0 || $k = 6 > 4 = n$
       :::
       """,
       typische_fehler=[(15, "Das ist $\\binom{6}{4}$. Oben steht hier die $4$, unten die $6$."),
                        (1, "Für $k > n$ ist der Binomialkoeffizient $0$: Man kann nicht $6$ aus $4$ Dingen auswählen.")])

# ── 3: Bedeutung ───────────────────────────────────────────────────────────
k.erklaerung("Was der Binomialkoeffizient zählt", r"""
    ## k aus n auswählen

    :::analogie 🍦 Eisdiele
    Es gibt $4$ Sorten, du nimmst $2$ verschiedene Kugeln in einen Becher. Wie
    viele verschiedene Becher gibt es? Die Reihenfolge im Becher ist egal.
    :::

    Bei den Sorten A, B, C, D sind das: AB, AC, AD, BC, BD, CD. Genau
    $\binom{4}{2}$ Stück. Allgemein gilt:

    !! $\binom{n}{k}$ ist die Anzahl der Möglichkeiten, $k$ Dinge aus $n$ verschiedenen auszuwählen, ohne Reihenfolge.

    :::rechnung Beispiel vorgerechnet
    \binom{4}{2} = \frac{4!}{2! \cdot 2!} || Definition
    \frac{4!}{2! \cdot 2!} = \frac{24}{4} = 6 || passt zu den sechs Bechern
    :::

    :::warum Bitfolgen zählen
    Wie viele 8-Bit-Wörter haben genau drei Einsen? Du wählst $3$ der $8$
    Stellen aus: $\binom{8}{3} = 56$.
    :::

    :::alt Mit Reihenfolgen erklärt
    Mit Reihenfolge gibt es $4 \cdot 3 = 12$ Möglichkeiten (erste Kugel, dann
    zweite). Dabei kommt jeder Becher doppelt vor: AB und BA. Also $12 : 2 = 6$.
    Dieses „durch $2!$ teilen“ steckt im Nenner von $\binom{4}{2}$.
    :::
    """)

k.mc("Aus $5$ Übungsaufgaben sollst du $2$ zum Vorrechnen auswählen. Wie viele Möglichkeiten gibt es?",
     ["$10$", "$20$", "$25$", "$7$"],
     "Die Reihenfolge ist egal: $\\binom{5}{2} = \\frac{5 \\cdot 4}{2} = 10$.",
     tipps=["Spielt die Reihenfolge der zwei Aufgaben eine Rolle?", "Nein. Also $\\binom{5}{2}$.",
            "$\\frac{5 \\cdot 4}{2}$"],
     fehler={"$20$": "$5 \\cdot 4 = 20$ zählt jede Auswahl doppelt (erst A dann B, erst B dann A).",
             "$25$": "$5 \\cdot 5$ würde erlauben, dieselbe Aufgabe zweimal zu nehmen.",
             "$7$": "Die Anzahlen werden nicht addiert. Zähle die Paare: $\\binom{5}{2}$."})

# ── 4: Symmetrie, Pascal ───────────────────────────────────────────────────
k.erklaerung("Symmetrie und Pascalsches Dreieck", r"""
    ## Auswählen heißt auch weglassen

    Wählst du $2$ von $10$ Dingen aus, lässt du gleichzeitig $8$ weg. Deshalb gilt:

    $$\binom{n}{k} = \binom{n}{n-k}, \qquad \binom{n}{0} = \binom{n}{n} = 1, \qquad \binom{n}{1} = n$$

    :::rechnung Beispiel vorgerechnet
    \binom{10}{8} = \binom{10}{2} || Symmetrie: $10 - 8 = 2$
    \frac{10 \cdot 9}{1 \cdot 2} = 45 || zwei Faktoren statt acht
    :::

    :::alt Mit Mannschaften erklärt
    Aus $10$ Leuten werden $8$ fürs Spiel aufgestellt. Statt die $8$ auszuwählen,
    kannst du auch die $2$ auswählen, die auf der Bank sitzen. Jede Bank-Auswahl
    legt genau eine Mannschaft fest. Beide Anzahlen sind also gleich.
    :::
    ---
    ## Das Pascalsche Dreieck

    Schreibst du die Binomialkoeffizienten zeilenweise auf, entsteht das
    [[Pascalsche Dreieck|Pascalsches Dreieck]]. Jede Zahl ist die Summe der beiden darüber:

    $$\binom{n+1}{k} = \binom{n}{k-1} + \binom{n}{k} \qquad (1 \le k \le n)$$

    :::visual pascal
    {"zeilen": 7, "markiert": [ [5, 2] ], "interaktiv": true,
     "unterschrift": "Zeile $5$, Stelle $2$: $\\binom{5}{2} = \\binom{4}{1} + \\binom{4}{2} = 4 + 6$. Tippe auf andere Zahlen."}
    :::

    :::rechnung Beispiel vorgerechnet
    \binom{5}{2} = \binom{4}{1} + \binom{4}{2} || die beiden Zahlen darüber
    4 + 6 = 10 || Werte aus Zeile $4$
    :::

    :::alt Mit einem Lieblingsding erklärt
    Du wählst $2$ aus $5$ Dingen, eins davon ist dein Lieblingsding. Entweder ist
    es dabei: Dann wählst du nur noch $1$ aus den übrigen $4$. Oder es ist nicht
    dabei: Dann wählst du $2$ aus den übrigen $4$. Zusammen $4 + 6 = 10$.
    :::
    """)

k.zahl("Berechne $\\displaystyle\\binom{20}{18}$ geschickt.", B(20, 18),
       "Symmetrie: $\\binom{20}{18} = \\binom{20}{2} = \\frac{20 \\cdot 19}{2} = 190$.",
       tipps=["Nutze $\\binom{n}{k} = \\binom{n}{n-k}$.", "$\\binom{20}{18} = \\binom{20}{2}$", "$\\frac{20 \\cdot 19}{2}$"],
       rechenweg=r"""
       :::rechnung
       \binom{20}{18} = \binom{20}{2} || Symmetrie
       \frac{20 \cdot 19}{1 \cdot 2} = 190 || ausrechnen
       :::
       """,
       typische_fehler=[(380, "Du hast vergessen, durch $2! = 2$ zu teilen."),
                        (F(10, 9), "$\\binom{20}{18}$ ist kein Bruch $\\frac{20}{18}$.")])

k.luecke("Fasse mit der Regel des Pascalschen Dreiecks zusammen.",
         r"\binom{5}{2} + \binom{5}{3} = \binom{\luecke}{\luecke}", [[6], [3]],
         "Die beiden Zahlen $\\binom{5}{2}$ und $\\binom{5}{3}$ stehen nebeneinander in Zeile $5$. "
         "Ihre Summe steht darunter: $\\binom{6}{3} = 10 + 10 = 20$.",
         tipps=["Die Regel: $\\binom{n}{k-1} + \\binom{n}{k} = \\binom{n+1}{k}$.", "Hier ist $n = 5$ und $k = 3$.",
                "Unten steht $\\binom{6}{3}$."],
         rechenweg=r"""
         :::rechnung
         \binom{5}{2} + \binom{5}{3} = \binom{6}{3} || Pascal-Regel mit $n = 5$, $k = 3$
         10 + 10 = 20 || Probe: $\binom{6}{3} = 20$
         :::
         """,
         typische_fehler=[([10, 5], "Oben addierst du nicht. Die Summe zweier Nachbarn aus Zeile $5$ steht in Zeile $6$."),
                          ([6, 2], "Unten steht der größere der beiden unteren Werte: $k = 3$.")])

k.wf("Für alle $n, k \\in \\mathbb{N}_0$ mit $k \\le n$ gilt $\\binom{n}{k} = \\binom{n}{n-k}$.", True,
     "Wahr. In der Definition werden nur $(n-k)!$ und $k!$ im Nenner vertauscht: "
     "$\\frac{n!}{(n-k)! \\cdot k!} = \\frac{n!}{k! \\cdot (n-k)!}$.",
     tipps=["Setze $n - k$ statt $k$ in die Definition ein und vergleiche die Nenner."])

# ── 5: Binomischer Lehrsatz ────────────────────────────────────────────────
k.erklaerung("Ausblick: der binomische Lehrsatz", r"""
    ## Woher der Name kommt

    Die Zahlen im Pascalschen Dreieck sind die Koeffizienten beim Ausmultiplizieren
    von $(a + b)^n$. Das ist der [[binomische Lehrsatz|binomischer Lehrsatz]]:

    $$(a + b)^n = \sum_{k=0}^{n} \binom{n}{k} a^{n-k} b^k$$

    Für $n = 2$ ist das die erste der [[binomischen Formeln|binomische Formeln]].

    :::rechnung Beispiel vorgerechnet
    (a + b)^3 = \binom{3}{0} a^3 + \binom{3}{1} a^2 b + \binom{3}{2} a b^2 + \binom{3}{3} b^3 || Lehrsatz mit $n = 3$
    (a + b)^3 = a^3 + 3a^2 b + 3a b^2 + b^3 || Zeile $3$: $1, 3, 3, 1$
    :::

    :::alt Mit Klammern erklärt
    $(a + b)^3 = (a+b)(a+b)(a+b)$. Beim Ausmultiplizieren nimmst du aus jeder
    Klammer $a$ oder $b$. Für $a b^2$ musst du in $2$ der $3$ Klammern $b$
    wählen. Dafür gibt es $\binom{3}{2} = 3$ Möglichkeiten.
    :::
    """)

k.zahl("Welcher Koeffizient steht vor $x^2$, wenn du $(x + 1)^5$ ausmultiplizierst?", B(5, 2),
       "Mit $a = x$, $b = 1$: Der Summand mit $x^2$ hat $n - k = 2$, also $k = 3$: $\\binom{5}{3} = 10$.",
       tipps=["Binomischer Lehrsatz mit $a = x$, $b = 1$, $n = 5$.", "$x^2 = x^{5-3}$, also $k = 3$.",
              "$\\binom{5}{3} = \\binom{5}{2}$"],
       rechenweg=r"""
       :::rechnung
       \binom{5}{3} = \binom{5}{2} || Symmetrie
       \frac{5 \cdot 4}{2} = 10 || ausrechnen
       :::
       """,
       typische_fehler=[(5, "$5$ ist der Koeffizient von $x^4$ (oder $x^1$). Für $x^2$ brauchst du $\\binom{5}{3}$."),
                        (2, "Der Exponent ist nicht der Koeffizient. Gesucht ist die Zahl vor $x^2$.")])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


def fakultaet_kuerzen(rng):
    art = rng.choice(["quotient", "quotient", "kehr", "doppel"])
    if art == "doppel":
        n = rng.randint(4, 9)
        m = rng.randint(1, n - 1)
        r = n - m
        w = F(fak(n), fak(m) * fak(r))
        frage = f"Berechne $\\dfrac{{{n}!}}{{{m}! \\cdot {r}!}}$."
        gross, klein = (m, r) if m >= r else (r, m)
        oben = " \\cdot ".join(str(i) for i in range(n, gross, -1))
        unten = " \\cdot ".join(str(i) for i in range(1, klein + 1))
        zeilen = [(f"\\frac{{{n}!}}{{{m}! \\cdot {r}!}} = \\frac{{{oben}}}{{{unten}}}", f"${gross}!$ kürzen"),
                  (f"= {w}", "ausrechnen")]
        fehler = [(F(fak(n), fak(m)), f"Du hast das ${r}!$ im Nenner vergessen."),
                  (fak(n - m - r) if n - m - r >= 0 else None, "Fakultäten kürzt man nicht wie Zahlen.")]
        tipps = [f"Kürze zuerst die größere Fakultät im Nenner, ${gross}!$.",
                 f"Oben bleibt ${oben}$.", f"Teile noch durch ${klein}! = {fak(klein)}$."]
    else:
        n = rng.randint(5, 12)
        d = rng.randint(1, 3)
        m = n - d
        oben = " \\cdot ".join(str(i) for i in range(n, m, -1))
        if art == "quotient":
            w = F(fak(n), fak(m))
            frage = f"Berechne $\\dfrac{{{n}!}}{{{m}!}}$, ohne die Fakultäten auszurechnen."
            zeilen = [(f"\\frac{{{n}!}}{{{m}!}} = \\frac{{{oben} \\cdot {m}!}}{{{m}!}}", f"${n}! = {oben} \\cdot {m}!$"),
                      (f"= {oben}", f"${m}!$ kürzen")]
            if d > 1:
                zeilen.append((f"= {w}", "ausrechnen"))
            fehler = [(fak(d), f"Fakultäten kürzt man nicht wie Zahlen: $\\frac{{{n}!}}{{{m}!}}$ ist nicht $({n} - {m})!$."),
                      (F(fak(n), fak(m - 1)), f"Der Faktor ${m}$ steckt in ${m}!$ und kürzt sich weg.")]
        else:
            w = F(fak(m), fak(n))
            frage = f"Berechne $\\dfrac{{{m}!}}{{{n}!}}$ als Bruch."
            zeilen = [(f"\\frac{{{m}!}}{{{n}!}} = \\frac{{{m}!}}{{{oben} \\cdot {m}!}}", f"${n}! = {oben} \\cdot {m}!$"),
                      (f"= \\frac{{1}}{{{oben}}}", f"${m}!$ kürzen"), (f"= {mathlib.tex(w)}", "ausrechnen")]
            fehler = [(1 / w, "Das ist der Kehrwert. Die größere Fakultät steht hier im Nenner."),
                      (F(1, fak(d)), "Fakultäten kürzt man nicht wie Zahlen.")]
        tipps = [f"Schreibe ${n}!$ als ${oben} \\cdot {m}!$.", f"Dann kürzt sich ${m}!$.", f"Es bleibt ${oben}$ übrig."]
    fehler = [(x, t) for x, t in fehler if x is not None]
    return {"frage": frage, "loesung": w, "gekuerzt": True, "tipps": tipps, "rechenweg": _zeilen(*zeilen),
            "erklaerung": "Die größere Fakultät als Produkt mit der kleineren schreiben, dann kürzen: $n! = n \\cdot (n-1)!$.",
            "typische_fehler": ohne_gleiche(w, fehler)}


def binomialkoeffizient(rng):
    n = rng.randint(3, 12)
    art = rng.random()
    if art < 0.12:
        kk = n + rng.randint(1, 3)
    elif art < 0.2:
        kk = rng.choice([0, n])
    else:
        kk = rng.randint(1, n - 1)
    w = B(n, kk)
    frage = f"Berechne $\\displaystyle\\binom{{{n}}}{{{kk}}}$."
    if kk > n:
        return {"frage": frage, "loesung": w,
                "tipps": ["Vergleiche $k$ und $n$.", f"${kk} > {n}$", "Für $k > n$ ist der Binomialkoeffizient $0$."],
                "rechenweg": _zeilen((f"\\binom{{{n}}}{{{kk}}} = 0", f"$k = {kk} > {n} = n$")),
                "erklaerung": "Für $k > n$ setzt die Definition $\\binom{n}{k} = 0$: Man kann nicht mehr auswählen, als da ist.",
                "typische_fehler": ohne_gleiche(w, [(B(kk, n), f"Das ist $\\binom{{{kk}}}{{{n}}}$: oben und unten vertauscht."),
                                                    (1, "Für $k > n$ ist der Wert $0$, nicht $1$.")])}
    j = min(kk, n - kk)
    oben = " \\cdot ".join(str(i) for i in range(n, n - j, -1)) or "1"
    unten = " \\cdot ".join(str(i) for i in range(1, j + 1)) or "1"
    zeilen = [(f"\\binom{{{n}}}{{{kk}}} = \\frac{{{n}!}}{{{n - kk}! \\cdot {kk}!}}", "Definition")]
    if j != kk:
        zeilen.append((f"\\binom{{{n}}}{{{kk}}} = \\binom{{{n}}}{{{j}}}", f"Symmetrie: ${n} - {kk} = {j}$"))
    zeilen.append((f"\\frac{{{n}!}}{{{n - kk}! \\cdot {kk}!}} = \\frac{{{oben}}}{{{unten}}}", f"${max(kk, n - kk)}!$ kürzen"))
    zeilen.append((f"= {w}", "ausrechnen"))
    fehler = [(F(fak(n), fak(n - j)), f"Du hast nicht mehr durch ${j}! = {fak(j)}$ geteilt."),
              (F(n, kk) if kk else None, "Der Binomialkoeffizient ist kein Bruch $\\frac{n}{k}$."),
              (0 if kk in (0, n) else None, f"Für $k = {kk}$ gibt es genau eine Auswahl, der Wert ist $1$."),
              (F(fak(n), fak(kk)), f"Im Nenner fehlt ${n - kk}!$: Es wird durch $(n-k)! \\cdot k!$ geteilt.")]
    return {"frage": frage, "loesung": w,
            "tipps": ["Definition: $\\binom{n}{k} = \\frac{n!}{(n-k)! \\cdot k!}$.",
                      (f"Kürze ${max(kk, n - kk)}!$: Oben bleibt nur ${n}$." if j == 1 else f"Kürze ${max(kk, n - kk)}!$: Oben bleiben ${j}$ Faktoren ab ${n}$ abwärts.") if j else "Hier ist $k = 0$ oder $k = n$.",
                      f"$\\frac{{{oben}}}{{{unten}}}$"],
            "rechenweg": _zeilen(*zeilen),
            "erklaerung": "Oben die größere Fakultät kürzen, dann bleiben $\\min(k, n-k)$ Faktoren über dem Bruchstrich.",
            "typische_fehler": ohne_gleiche(w, [(x, t) for x, t in fehler if x is not None])}


def _faktoren_text(a, b):
    """(n+a)(n+a-1)…(n+b+1) als Term-Text und LaTeX."""
    teile = []
    for c in range(a, b, -1):
        teile.append("n" if c == 0 else f"n+{c}" if c > 0 else f"n-{-c}")
    txt = "".join(f"({t})" for t in teile)
    tex = " \\cdot ".join(f"({t.replace('+', ' + ').replace('-', ' - ')})" if t != "n" else "n" for t in teile)
    return txt, tex, teile


def fakultaet_term(rng):
    b = rng.choice([-2, -1, 0, 1, 2, 3])
    a = b + rng.choice([1, 2, 2, 3])
    fa = "n!" if a == 0 else f"(n + {a})!" if a > 0 else f"(n - {-a})!"
    fb = "n!" if b == 0 else f"(n + {b})!" if b > 0 else f"(n - {-b})!"
    txt, tex, teile = _faktoren_text(a, b)
    ergebnis_tex = tex
    if len(teile) == 1:
        ergebnis_tex = teile[0].replace("+", " + ").replace("-", " - ")
        tex = ergebnis_tex if teile[0] == "n" else f"({ergebnis_tex})"
    nur_erster = teile[0]
    fehler = [(nur_erster, f"${fa}$ hat {a - b} Faktoren mehr als ${fb}$. Alle bleiben stehen.")] if len(teile) > 1 else []
    extra = "n" if b == 0 else f"n+{b}" if b > 0 else f"n-{-b}"
    extra_tex = extra.replace("+", " + ").replace("-", " - ")
    fehler.append((f"{txt}({extra})", f"Ein Faktor zu viel: ${extra_tex}$ steckt in ${fb}$ und kürzt sich weg."))
    return {"frage": f"Vereinfache $\\dfrac{{{fa}}}{{{fb}}}$ für $n \\ge 1$ so, dass keine Fakultät mehr vorkommt.",
            "loesung": txt, "variablen": "n",
            "tipps": [f"Schreibe ${fa}$ als Produkt mit ${fb}$.", f"${fa} = {tex} \\cdot {fb}$", f"Kürze ${fb}$."],
            "rechenweg": f"Es gilt ${fa} = {tex} \\cdot {fb}$. Nach dem Kürzen bleibt ${ergebnis_tex}$.",
            "erklaerung": "Die größere Fakultät enthält die kleinere: $(n+1)! = (n+1) \\cdot n!$.",
            "typische_fehler": ohne_gleiche(txt, fehler)}


k.praxis()

k.generator(fakultaet_kuerzen, typ="zahl", titel="Fakultäten kürzen")
k.generator(binomialkoeffizient, typ="zahl", titel="Binomialkoeffizienten berechnen")
k.generator(fakultaet_term, typ="term", titel="Fakultäten mit n kürzen")

k.zuordnen("Ordne jedem Term sein Ergebnis zu. (Aufgabe aus der Vorkurs-Vorlesung)",
           [("$5!$", "120"), ("$\\binom{7}{3}$", "35"), ("$\\sum_{j=-3}^{3} 5j$", "0"),
            ("$\\prod_{k=1}^{4} \\frac{k^2}{2}$", "36")],
           "$5! = 120$, $\\binom{7}{3} = \\frac{7 \\cdot 6 \\cdot 5}{6} = 35$, in $\\sum 5j$ heben sich "
           "$\\pm 5, \\pm 10, \\pm 15$ weg, und $\\prod \\frac{k^2}{2} = \\frac{576}{16} = 36$.",
           ablenker=["12", "16"],
           tipps=["Rechne jeden Term einzeln aus. Bei der Summe: Welche Summanden heben sich weg?"])

k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: Zählen mit Binomialkoeffizienten

    a) Wie viele 8-Bit-Wörter enthalten genau drei Einsen?

    b) Beim Lotto „6 aus 49“ werden $6$ von $49$ Zahlen gezogen. Wie viele verschiedene Tipps gibt es?

    c) Wie viele 8-Bit-Wörter gibt es insgesamt? Begründen Sie mit $\sum_{k=0}^{8} \binom{8}{k}$.
    """,
    [{"typ": "zahl", "frage": "a) Anzahl der 8-Bit-Wörter mit genau drei Einsen:", "loesung": B(8, 3),
      "tipps": ["Du wählst die $3$ Stellen aus, an denen eine $1$ steht.", "$\\binom{8}{3} = \\frac{8 \\cdot 7 \\cdot 6}{6}$"],
      "rechenweg": "$\\binom{8}{3} = \\frac{8 \\cdot 7 \\cdot 6}{1 \\cdot 2 \\cdot 3} = 56$",
      "typische_fehler": [(336, "Das zählt die Reihenfolge der Einsen mit. Die Einsen sind aber gleich: durch $3! = 6$ teilen.")]},
     {"typ": "zahl", "frage": "b) Anzahl der Lotto-Tipps:", "loesung": B(49, 6),
      "tipps": ["$\\binom{49}{6}$", "$\\frac{49 \\cdot 48 \\cdot 47 \\cdot 46 \\cdot 45 \\cdot 44}{720}$"],
      "rechenweg": "$\\binom{49}{6} = \\frac{49 \\cdot 48 \\cdot 47 \\cdot 46 \\cdot 45 \\cdot 44}{6!} = 13\\,983\\,816$",
      "typische_fehler": [(F(fak(49), fak(43)), "Hier fehlt das Teilen durch $6! = 720$: Die Reihenfolge der Ziehung ist egal.")]},
     {"typ": "zahl", "frage": "c) Anzahl aller 8-Bit-Wörter:", "loesung": sum(B(8, i) for i in range(9)),
      "tipps": ["Jedes Wort hat $0$, $1$, …, oder $8$ Einsen.", "$1 + 8 + 28 + 56 + 70 + 56 + 28 + 8 + 1$"],
      "rechenweg": "$\\sum_{k=0}^{8} \\binom{8}{k} = 1 + 8 + 28 + 56 + 70 + 56 + 28 + 8 + 1 = 256 = 2^8$",
      "typische_fehler": [(255, "Das Wort mit $0$ Einsen ($k = 0$, also $00000000$) zählt auch mit.")]}],
    "Jedes Wort hat eine bestimmte Anzahl $k$ von Einsen. Summiert über alle $k$ ergibt sich $2^8$, "
    "passend dazu, dass jede der $8$ Stellen $2$ Möglichkeiten hat.",
    uebungsblatt=True,
    tipps=["Auswählen ohne Reihenfolge: Binomialkoeffizient.", "In c) jedes $k$ von $0$ bis $8$ einzeln zählen."],
    rechenweg=r"""
    :::rechnung
    \binom{8}{3} = \frac{8 \cdot 7 \cdot 6}{1 \cdot 2 \cdot 3} || drei der acht Stellen wählen
    \frac{8 \cdot 7 \cdot 6}{1 \cdot 2 \cdot 3} = 56 || a)
    1 + 8 + 28 + 56 + 70 + 56 + 28 + 8 + 1 = 256 || c): Zeile $8$ des Pascalschen Dreiecks
    2^8 = 256 || Probe: zwei Möglichkeiten je Stelle
    :::
    """)

k.papier(r"""
    ## Übungsblatt-Stil: Rechenregeln beweisen

    Seien $n, k \in \mathbb{N}_0$.

    a) Zeigen Sie für $k \le n$: $\displaystyle\binom{n}{k} = \binom{n}{n-k}$.

    b) Zeigen Sie für $1 \le k \le n$: $\displaystyle\binom{n}{k-1} + \binom{n}{k} = \binom{n+1}{k}$.
    """,
    r"""
    **a)** Sei $0 \le k \le n$. Dann ist auch $0 \le n - k \le n$, also gilt für
    beide Seiten der erste Fall der Definition. Mit $n - (n - k) = k$ folgt

    $$\binom{n}{n-k} = \frac{n!}{(n - (n-k))! \cdot (n-k)!} = \frac{n!}{k! \cdot (n-k)!} = \binom{n}{k}.$$

    **b)** Sei $1 \le k \le n$. Dann sind $k - 1$ und $k$ zwischen $0$ und $n$.
    Wir bringen beide Brüche auf den Hauptnenner $(n-k+1)! \cdot k!$. Dazu nutzen
    wir $k! = k \cdot (k-1)!$ und $(n-k+1)! = (n-k+1) \cdot (n-k)!$:

    $$\binom{n}{k-1} + \binom{n}{k} = \frac{n!}{(n-k+1)! \, (k-1)!} + \frac{n!}{(n-k)! \, k!}
      = \frac{n! \cdot k}{(n-k+1)! \, k!} + \frac{n! \cdot (n-k+1)}{(n-k+1)! \, k!}$$

    $$= \frac{n! \cdot (k + n - k + 1)}{(n-k+1)! \, k!} = \frac{n! \cdot (n+1)}{(n+1-k)! \, k!}
      = \frac{(n+1)!}{(n+1-k)! \, k!} = \binom{n+1}{k}.$$

    Im letzten Schritt: $(n+1) \cdot n! = (n+1)!$, und wegen $k \le n + 1$ ist das
    genau die Definition von $\binom{n+1}{k}$. $\square$
    """,
    ["a) Ich habe begründet, dass für $n - k$ derselbe Fall der Definition gilt",
     "a) Ich habe $n - (n - k) = k$ benutzt",
     "b) Ich habe den Hauptnenner $(n-k+1)! \\cdot k!$ gebildet und das Erweitern begründet",
     "b) Ich habe $k + (n - k + 1) = n + 1$ und $(n+1) \\cdot n! = (n+1)!$ benutzt",
     "Ich habe die Voraussetzung $1 \\le k \\le n$ an der richtigen Stelle verwendet"],
    "Beide Regeln folgen direkt aus der Definition. In b) ist der Hauptnenner der Schlüssel.",
    uebungsblatt=True,
    tipps=["In b): Erweitere den ersten Bruch mit $k$, den zweiten mit $n - k + 1$."])

k.zusammenfassung(r"""
    ## Fakultät und Binomialkoeffizient

    | Was | Formel | Beispiel |
    |---|---|---|
    | Fakultät ($n \in \mathbb{N}_0$) | $n! = \prod_{k=1}^{n} k$, $0! = 1$ | $4! = 24$ |
    | Rekursion | $n! = n \cdot (n-1)!$ | $\frac{7!}{5!} = 7 \cdot 6 = 42$ |
    | Binomialkoeffizient | $\binom{n}{k} = \frac{n!}{(n-k)! \cdot k!}$ für $k \le n$, sonst $0$ | $\binom{5}{2} = 10$ |
    | Sonderfälle | $\binom{n}{0} = \binom{n}{n} = 1$, $\binom{n}{1} = n$ | $\binom{4}{6} = 0$ |
    | Symmetrie | $\binom{n}{k} = \binom{n}{n-k}$ | $\binom{20}{18} = \binom{20}{2} = 190$ |
    | Pascal | $\binom{n+1}{k} = \binom{n}{k-1} + \binom{n}{k}$ | $\binom{5}{2} = 4 + 6$ |
    | Lehrsatz | $(a+b)^n = \sum_{k=0}^{n} \binom{n}{k} a^{n-k} b^k$ | $(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3$ |

    !! $\binom{n}{k}$ zählt die Auswahlen von $k$ aus $n$ Dingen ohne Reihenfolge.

    - Schnell rechnen: $\binom{n}{k} = \frac{n \cdot (n-1) \cdots (n-k+1)}{k!}$.
    - $\frac{6!}{3!} \neq 2!$ und $(2n)! \neq 2 \cdot n!$.
""")
