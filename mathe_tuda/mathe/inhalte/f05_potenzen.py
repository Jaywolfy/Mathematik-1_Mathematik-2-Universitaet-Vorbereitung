# -*- coding: utf-8 -*-
"""Fundament 5: Potenzen – Bedeutung, Potenzgesetze, negative Exponenten, Zweier- und Zehnerpotenzen."""
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

tex = mathlib.tex
tk = mathlib.tex_klammer


def pot(a, n):
    """Potenz als LaTeX; negative Basis in Klammern, Exponent immer in {}."""
    return f"{tk(a)}^{{{n}}}"


k = neues_kapitel(
    slug="potenzen",
    titel="Potenzen",
    beschreibung="Was $a^n$ bedeutet, Potenzgesetze, null und negative Exponenten, Zweier- und Zehnerpotenzen",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="🚀")

k.lernziele([
    "Ich weiß, was $a^n$ bedeutet, und kenne Basis und Exponent",
    "Ich unterscheide $(-2)^4$ und $-2^4$",
    "Ich kann die Potenzgesetze anwenden und kenne ihre Grenzen",
    "Ich kann mit $a^0$ und negativen Exponenten rechnen",
    "Ich kenne die Zweierpotenzen bis $2^{10}$ und schreibe Zahlen mit Zehnerpotenzen",
])

k.warum(r"""
Ein Computer denkt in [[Bits|Bit]]. Mit $n$ Bits gibt es $2^n$ verschiedene Muster: Ein Byte
aus $8$ Bits kann $2^8 = 256$ Werte annehmen. Speichergrößen wie $1024$ Byte sind
[[Zweierpotenzen|Zweierpotenz]]. Laufzeiten wie $n^2$ oder $2^n$ entscheiden, ob ein Programm
Sekunden oder Jahrtausende rechnet. Und `1e-9` in Python ist $10^{-9}$. Ohne Potenzen
kommst du in keiner Informatik-Vorlesung weit.
""")

# ── 1: Was ist eine Potenz ─────────────────────────────────────────────────
k.erklaerung("Was ist eine Potenz?", r"""
    ## Wiederholtes Malnehmen

    :::analogie 📄 Papier falten
    Faltest du ein Blatt einmal, liegen $2$ Lagen übereinander. Nach dem zweiten
    Falten $4$, dann $8$. Jedes Falten verdoppelt.
    :::

    Eine [[Potenz]] ist eine Kurzschrift für wiederholtes Malnehmen derselben Zahl:

    $$2^5 = \underbrace{2 \cdot 2 \cdot 2 \cdot 2 \cdot 2}_{5\text{ Faktoren}}$$

    Die untere Zahl ist die [[Basis|Basis einer Potenz]], sie wird malgenommen. Die obere Zahl ist
    der [[Exponent]], er zählt, wie oft.

    :::rechnung Beispiel vorgerechnet
    2^5 = 2 \cdot 2 \cdot 2 \cdot 2 \cdot 2 || $5$ Faktoren $2$
    = 32 || ausrechnen
    :::

    :::achtung Nicht malnehmen
    $2^5 = 2 \cdot 5 = 10$ ist falsch. Der Exponent zählt Faktoren, er ist kein Faktor.
    :::

    :::alt Mit einem Baum erklärt
    Ein Baum hat einen Stamm, der sich in $3$ Äste teilt. Jeder Ast teilt sich wieder in
    $3$, und jeder davon noch einmal in $3$. Ganz außen hast du $3 \cdot 3 \cdot 3 = 3^3 = 27$
    Zweige. Der Exponent $3$ ist die Zahl der Verzweigungsstufen.
    :::
    ---
    ## Minus und Klammern

    Gehört das Minus zur Basis, steht es in Klammern. Sonst kommt es erst am Ende dazu.

    :::rechnung Beispiel vorgerechnet
    (-2)^4 = (-2) \cdot (-2) \cdot (-2) \cdot (-2) || das Minus wird mitmultipliziert
    = 16 || vier Minus: gerade Anzahl, plus
    -2^4 = -(2 \cdot 2 \cdot 2 \cdot 2) || erst die Potenz, dann das Minus
    = -16 || Gegenzahl von $16$
    (-2)^3 = -8 || drei Minus: ungerade Anzahl, minus
    :::

    !! Negative Basis: Gerader Exponent gibt plus, ungerader Exponent gibt minus.

    :::alt Mit Python erklärt
    Python hält sich an dieselbe Regel: `-2**4` ergibt `-16`, `(-2)**4` ergibt `16`.
    Ohne Klammer bindet der Hochpfeil stärker als das Minus. Das Minus ist dann wie
    ein Schild „Gegenzahl bilden“, das erst am Schluss gelesen wird.
    :::
    """)

k.berechne("3^4",
           erklaerung="$3^4 = 3 \\cdot 3 \\cdot 3 \\cdot 3 = 81$.",
           tipps=["Der Exponent sagt, wie oft die $3$ als Faktor dasteht.", "$3 \\cdot 3 \\cdot 3 \\cdot 3$",
                  "$9 \\cdot 9$"],
           rechenweg=r"""
           :::rechnung
           3^4 = 3 \cdot 3 \cdot 3 \cdot 3 || $4$ Faktoren $3$
           = 9 \cdot 9 || je zwei zusammenfassen
           = 81 || ausrechnen
           :::
           """,
           typische_fehler=[(12, "Du hast $3 \\cdot 4$ gerechnet. Der Exponent zählt die Faktoren: $3 \\cdot 3 \\cdot 3 \\cdot 3$."),
                            (64, "Das ist $4^3$. Basis und Exponent darf man nicht vertauschen."),
                            (27, "Du hast nur drei Faktoren genommen. Es sind vier.")])

k.berechne("-2^4",
           erklaerung="Ohne Klammer gehört das Minus nicht zur Basis: $-2^4 = -(2^4) = -16$.",
           tipps=["Steht das Minus in einer Klammer mit der $2$?", "Nein. Rechne zuerst $2^4$.",
                  "$2^4 = 16$, dann das Minus davor."],
           rechenweg=r"""
           :::rechnung
           -2^4 = -(2 \cdot 2 \cdot 2 \cdot 2) || erst die Potenz
           = -16 || dann die Gegenzahl
           :::
           """,
           typische_fehler=[(16, "Das wäre $(-2)^4$. Ohne Klammer wird nur die $2$ potenziert, das Minus kommt am Ende."),
                            (-8, "Du hast $-2 \\cdot 4$ gerechnet. Der Exponent zählt Faktoren.")])

k.berechne("(-3)^3",
           erklaerung="$(-3) \\cdot (-3) \\cdot (-3) = 9 \\cdot (-3) = -27$. Ungerader Exponent: minus.",
           tipps=["Die $-3$ steht in Klammern, also wird sie dreimal malgenommen.",
                  "Zähle die Minuszeichen: drei.", "$3^3 = 27$, Vorzeichen minus."],
           rechenweg=r"""
           :::rechnung
           (-3)^3 = (-3) \cdot (-3) \cdot (-3) || drei Faktoren $-3$
           = 9 \cdot (-3) || minus mal minus gibt plus
           = -27 || plus mal minus gibt minus
           :::
           """,
           typische_fehler=[(27, "Drei Minuszeichen: Zwei ergeben plus, das dritte macht wieder minus."),
                            (-9, "Du hast $-3 \\cdot 3$ gerechnet. Der Exponent zählt Faktoren.")])

# ── 2: Potenzgesetze ───────────────────────────────────────────────────────
k.erklaerung("Potenzgesetze", r"""
    ## Gleiche Basis: Exponenten addieren

    Schreib die Faktoren aus und zähle sie einfach:

    :::rechnung Beispiel vorgerechnet
    2^3 \cdot 2^4 = (2 \cdot 2 \cdot 2) \cdot (2 \cdot 2 \cdot 2 \cdot 2) || ausgeschrieben
    = 2^7 || $3 + 4 = 7$ Faktoren
    \frac{2^6}{2^2} = \frac{2 \cdot 2 \cdot 2 \cdot 2 \cdot 2 \cdot 2}{2 \cdot 2} || ausgeschrieben
    = 2^4 || zwei Faktoren kürzen sich weg: $6 - 2 = 4$
    :::

    Das sind die ersten beiden [[Potenzgesetze|Potenzgesetz]]:

    $$a^m \cdot a^n = a^{m + n} \qquad \frac{a^m}{a^n} = a^{m - n}$$

    :::achtung Exponenten malnehmen
    $2^3 \cdot 2^4 = 2^{12}$ ist falsch, ebenso $4^7$. Die Basis bleibt, die Exponenten
    werden **addiert**.
    :::

    :::alt Mit Ordnern erklärt
    Stell dir die Faktoren als Blätter in Ordnern vor. Ein Ordner hat $3$ Blätter
    mit einer $2$, ein anderer $4$. Legst du beide zusammen, hast du $7$ Blätter.
    Beim Teilen nimmst du Blätter wieder heraus: aus $6$ werden $6 - 2 = 4$.
    :::
    ---
    ## Potenz einer Potenz, gleicher Exponent

    :::rechnung Beispiel vorgerechnet
    (2^3)^2 = 2^3 \cdot 2^3 || $2^3$ zweimal als Faktor
    = 2^6 || $3 \cdot 2 = 6$ Faktoren
    2^5 \cdot 5^5 = (2 \cdot 5)^5 || gleicher Exponent: Basen zusammenfassen
    = 10^5 || $2 \cdot 5 = 10$
    :::

    $$\left(a^m\right)^n = a^{m \cdot n} \qquad a^n \cdot b^n = (a \cdot b)^n$$

    :::achtung Summen haben kein Gesetz
    $2^3 + 2^4 = 2^7$ ist falsch: $8 + 16 = 24$, aber $2^7 = 128$. Ebenso ist
    $(a + b)^2$ nicht $a^2 + b^2$. Die Gesetze gelten nur für Produkte und Quotienten.
    :::

    :::alt Mit Kisten erklärt
    $(2^3)^2$: Eine Kiste enthält $3$ Zweien als Faktoren. Du nimmst $2$ solche Kisten.
    Insgesamt sind es $3 \cdot 2 = 6$ Zweien. Bei $2^5 \cdot 5^5$ bildest du fünf Paare
    aus je einer $2$ und einer $5$. Jedes Paar ist $10$.
    :::
    """)

k.luecke("Welcher Exponent gehört in die Lücke?",
         "2^{3} \\cdot 2^{4} = 2^{\\luecke}", [[7]],
         "Gleiche Basis: Exponenten addieren. $3 + 4 = 7$.",
         tipps=["Die Basis ist gleich.", "Zähle alle Faktoren $2$ zusammen.", "$3 + 4$"],
         rechenweg=r"""
         :::rechnung
         2^3 \cdot 2^4 = 2^{3 + 4} || gleiche Basis: Exponenten addieren
         = 2^7 || ausrechnen
         :::
         """,
         typische_fehler=[([12], "Bei gleicher Basis werden die Exponenten **addiert**, nicht malgenommen."),
                          ([1], "Das wäre beim Teilen. Hier wird malgenommen: addieren.")])

k.luecke("Welcher Exponent gehört in die Lücke?",
         "\\left(5^{2}\\right)^{3} = 5^{\\luecke}", [[6]],
         "Potenz einer Potenz: Exponenten malnehmen. $2 \\cdot 3 = 6$.",
         tipps=["$5^2$ steht dreimal als Faktor da.", "$5^2 \\cdot 5^2 \\cdot 5^2$", "$2 + 2 + 2 = 2 \\cdot 3$"],
         rechenweg=r"""
         :::rechnung
         (5^2)^3 = 5^2 \cdot 5^2 \cdot 5^2 || dreimal der Faktor $5^2$
         = 5^{2 \cdot 3} || $2 + 2 + 2 = 2 \cdot 3$
         = 5^6 || ausrechnen
         :::
         """,
         typische_fehler=[([5], "Hier werden die Exponenten nicht addiert. $5^2$ kommt dreimal vor: $2 \\cdot 3$."),
                          ([8], "Das wäre $2^3$ als Exponent. Bei $(a^m)^n$ ist der neue Exponent $m \\cdot n$.")])

k.luecke("Vereinfache mit den Potenzgesetzen.",
         "\\frac{x^{7} \\cdot x^{2}}{x^{4}} = x^{\\luecke}", [[5]],
         "Zähler: $x^{7 + 2} = x^9$. Geteilt durch $x^4$: $x^{9 - 4} = x^5$.",
         tipps=["Fasse zuerst den Zähler zusammen.", "Im Zähler steht $x^9$.", "$9 - 4$"],
         rechenweg=r"""
         :::rechnung
         \frac{x^7 \cdot x^2}{x^4} = \frac{x^9}{x^4} || Zähler: $7 + 2 = 9$
         = x^5 || teilen: $9 - 4 = 5$
         :::
         """,
         typische_fehler=[([F(7 * 2, 4)], "Du hast die Exponenten malgenommen und geteilt. Richtig: addieren und subtrahieren."),
                          ([13], "Beim Teilen wird der Exponent des Nenners **abgezogen**.")])

k.wf("$2^3 + 2^3 = 2^6$", False,
     "Für Summen gibt es kein Potenzgesetz. $2^3 + 2^3 = 8 + 8 = 16 = 2^4$, denn zweimal $2^3$ ist $2 \\cdot 2^3$.",
     tipps=["Rechne beide Seiten einzeln aus."])

# ── 3: Null und negative Exponenten ────────────────────────────────────────
k.erklaerung("Null und negative Exponenten", r"""
    ## Die Reihe nach unten fortsetzen

    :::analogie 🪜 Treppe
    Jede Stufe nach unten teilt durch $2$. Auf der Treppe gibt es keinen Grund,
    bei $2^1$ stehen zu bleiben.
    :::

    :::rechnung Beispiel vorgerechnet
    2^3 = 8 || Start
    2^2 = 4 || eine Stufe tiefer: durch $2$
    2^1 = 2 || durch $2$
    2^0 = 1 || durch $2$
    2^{-1} = \frac{1}{2} || durch $2$
    2^{-2} = \frac{1}{4} || durch $2$
    :::

    !! $a^0 = 1$ und $a^{-n} = \frac{1}{a^n}$ für jede Basis $a \neq 0$.

    Ein negativer Exponent macht die Zahl also **nicht** negativ. Er bildet den
    [[Kehrwert]].

    :::alt Mit dem Gesetz erklärt
    Das Teilungsgesetz liefert dasselbe. $\frac{2^3}{2^3} = 1$, und nach dem Gesetz
    ist es $2^{3 - 3} = 2^0$. Also muss $2^0 = 1$ sein. Genauso ist
    $\frac{2^1}{2^3} = \frac{2}{8} = \frac{1}{4}$ und nach dem Gesetz $2^{1 - 3} = 2^{-2}$.
    :::
    ---
    ## Mit negativen Exponenten rechnen

    Alle Potenzgesetze gelten weiter. Am Ende schreibst du das Ergebnis meist als Bruch.

    :::rechnung Beispiel vorgerechnet
    10^{-3} = \frac{1}{10^3} || negativer Exponent: Kehrwert
    = \frac{1}{1000} || $10^3 = 1000$
    = 0{,}001 || drei Nachkommastellen
    2^{-3} \cdot 2^5 = 2^{-3 + 5} || gleiche Basis: addieren
    = 2^2 = 4 || ausrechnen
    :::

    :::achtung Negativer Exponent, negative Zahl?
    $2^{-3} = -8$ und $2^{-3} = -6$ sind falsch. Richtig ist $2^{-3} = \frac{1}{8}$:
    positiv und kleiner als $1$.
    :::

    :::alt Mit Einheiten erklärt
    Ein Millimeter ist $10^{-3}$ Meter, also ein Tausendstel Meter. Er ist winzig, aber
    nicht negativ. Ein Kilometer ist $10^3$ Meter. Plus-Exponent heißt: viele Meter
    zusammen. Minus-Exponent heißt: einen Meter in kleine Stücke teilen.
    :::
    """)

k.berechne("2^(-3)", gekuerzt=True,
           erklaerung="$2^{-3} = \\frac{1}{2^3} = \\frac{1}{8}$.",
           tipps=["Ein negativer Exponent bildet den Kehrwert.", "$2^{-3} = \\frac{1}{2^3}$.", "$2^3 = 8$."],
           rechenweg=r"""
           :::rechnung
           2^{-3} = \frac{1}{2^3} || Kehrwert von $2^3$
           = \frac{1}{8} || $2^3 = 8$
           :::
           """,
           typische_fehler=[(-8, "Ein negativer Exponent macht die Zahl nicht negativ, sondern bildet den Kehrwert."),
                            (-6, "Du hast $2 \\cdot (-3)$ gerechnet. Der Exponent zählt Faktoren, und negativ heißt: Kehrwert."),
                            (F(-1, 8), "Das Minus im Exponenten bleibt nicht als Vorzeichen stehen. $2^{-3}$ ist positiv.")])

k.zahl("Berechne $7^0$.", 1,
       "Jede Zahl außer $0$ hoch $0$ ergibt $1$: $7^0 = \\frac{7^1}{7^1} = 1$.",
       tipps=["Denk an die Treppe: $7^1 = 7$, eine Stufe tiefer heißt durch $7$.", "$7 : 7$", "Das Ergebnis ist nicht $0$."],
       rechenweg=r"""
       :::rechnung
       7^0 = \frac{7^1}{7^1} || Teilungsgesetz: $1 - 1 = 0$
       = 1 || eine Zahl durch sich selbst
       :::
       """,
       typische_fehler=[(0, "Null Faktoren heißt nicht null. Das leere Produkt ist $1$, siehe $\\frac{7}{7} = 7^0$."),
                        (7, "$7^1 = 7$. Bei $7^0$ wird noch einmal durch $7$ geteilt.")])

# ── 4: Zweier- und Zehnerpotenzen ──────────────────────────────────────────
k.erklaerung("Zweier- und Zehnerpotenzen", r"""
    ## Zweierpotenzen und Bits

    Ein [[Bit]] ist $0$ oder $1$. Mit jedem weiteren Bit verdoppelt sich die Zahl
    der möglichen Muster. Mit $n$ Bits gibt es also $2^n$ Muster.

    | $n$ | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ | $7$ | $8$ | $9$ | $10$ |
    |---|---|---|---|---|---|---|---|---|---|---|---|
    | $2^n$ | $1$ | $2$ | $4$ | $8$ | $16$ | $32$ | $64$ | $128$ | $256$ | $512$ | $1024$ |

    :::rechnung Beispiel vorgerechnet
    2^8 = 256 || ein Byte: $8$ Bit, Werte $0$ bis $255$
    2^{10} = 1024 || ein Kibibyte hat $1024$ Byte
    2^{20} = 2^{10} \cdot 2^{10} || Potenzgesetz
    = 1048576 || ein Mebibyte, rund eine Million
    :::

    :::warum Lerne die Tabelle auswendig
    Du brauchst sie für Binärzahlen, Speichergrößen und Laufzeiten. $2^{10} \approx 1000$
    ist eine der nützlichsten Faustregeln der Informatik.
    :::

    :::alt Mit Ratespiel erklärt
    Jemand denkt sich eine Zahl von $1$ bis $1024$. Du fragst: „Ist sie größer als $512$?“
    Jede Antwort halbiert die Möglichkeiten. Nach $10$ Fragen bleibt genau eine übrig,
    denn $2^{10} = 1024$. Jede Ja-Nein-Antwort ist ein Bit.
    :::
    ---
    ## Zehnerpotenzen: sehr große und sehr kleine Zahlen

    $10^n$ ist eine $1$ mit $n$ Nullen. In der [[wissenschaftlichen Schreibweise|wissenschaftliche Schreibweise]]
    schreibst du eine Zahl als Zahl zwischen $1$ und $10$ mal [[Zehnerpotenz]].

    :::rechnung Beispiel vorgerechnet
    3200000 = 3{,}2 \cdot 10^6 || Komma $6$ Stellen nach links geschoben
    0{,}0004 = 4 \cdot 10^{-4} || Komma $4$ Stellen nach rechts geschoben
    :::

    | Vorsilbe | kilo | mega | giga | milli | mikro | nano |
    |---|---|---|---|---|---|---|
    | Faktor | $10^3$ | $10^6$ | $10^9$ | $10^{-3}$ | $10^{-6}$ | $10^{-9}$ |

    :::alt Mit dem Komma erklärt
    Der Exponent zählt, wie weit das Komma wandert. Plus: nach rechts, die Zahl wird
    groß. Minus: nach links, die Zahl wird klein. $4 \cdot 10^{-4}$: Starte bei
    $4{,}0$ und schiebe das Komma $4$ Stellen nach links, ergibt $0{,}0004$. In Python
    schreibst du dafür `4e-4`.
    :::
    """)

k.zahl("Wie viele verschiedene Werte kann man mit $8$ Bit darstellen?", 2 ** 8,
       "Jedes Bit verdoppelt die Zahl der Muster: $2^8 = 256$. Die Werte gehen von $0$ bis $255$.",
       tipps=["Mit $1$ Bit gibt es $2$ Muster, mit $2$ Bits $4$.", "Mit $n$ Bits gibt es $2^n$ Muster.", "$2^8$"],
       rechenweg=r"""
       :::rechnung
       2^8 = 2^4 \cdot 2^4 || aufteilen
       = 16 \cdot 16 || $2^4 = 16$
       = 256 || ausrechnen
       :::
       """,
       typische_fehler=[(16, "Du hast $2 \\cdot 8$ gerechnet. Jedes Bit **verdoppelt**: $2^8$."),
                        (255, "$255$ ist der größte Wert. Die $0$ zählt aber auch mit: $256$ Werte."),
                        (64, "Das ist $8^2$. Basis ist die $2$ (zwei Zustände pro Bit), Exponent die $8$.")])

k.luecke("Schreibe in wissenschaftlicher Schreibweise.",
         "0{,}0004 = 4 \\cdot 10^{\\luecke}", [[-4]],
         "Das Komma wandert $4$ Stellen nach rechts, um von $0{,}0004$ zu $4$ zu kommen. Die Zahl ist klein: Exponent $-4$.",
         tipps=["Wie oft musst du das Komma schieben, bis $4$ dasteht?", "$4$ Stellen. Ist die Zahl groß oder klein?",
                "Kleine Zahl: negativer Exponent."],
         rechenweg=r"""
         :::rechnung
         4 \cdot 10^{-4} = \frac{4}{10000} || negativer Exponent: Kehrwert
         = 0{,}0004 || vier Nachkommastellen
         :::
         """,
         typische_fehler=[([4], "$4 \\cdot 10^4 = 40000$. Die Zahl ist kleiner als $1$, also ist der Exponent negativ."),
                          ([-3], "Zähle die Stellen nach: Die $4$ steht an der vierten Nachkommastelle.")])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


def potenz_auswerten(rng):
    while True:
        a = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6, 10])
        n = rng.randint(-3, 4)
        w = F(a) ** n
        if abs(w.numerator) <= 10000 and w.denominator <= 100 and n != 1 and (a, n) != (2, 2):
            break
    zeilen, fehler = [], []
    if n > 0:
        produkt = " \\cdot ".join([tk(a)] * n)
        zeilen.append((f"{pot(a, n)} = {produkt}", f"${n}$ Faktoren ${tk(a)}$"))
        zeilen.append((f"= {tex(w)}", "ausrechnen" + (", Vorzeichen: " + ("gerade Anzahl Minus" if n % 2 == 0 else "ungerade Anzahl Minus") if a < 0 else "")))
        tipps = [f"Der Exponent ${n}$ zählt die Faktoren.", f"${produkt}$", f"Rechne Schritt für Schritt."]
        fehler.append((a * n, f"Du hast ${tk(a)} \\cdot {n}$ gerechnet. Der Exponent zählt Faktoren."))
        if a < 0:
            fehler.append((-w, "Achte auf das Vorzeichen: Gerade Anzahl Minus gibt plus, ungerade gibt minus."))
        if n != abs(a):
            fehler.append((F(n) ** a if a > 0 else None, "Basis und Exponent vertauscht."))
    elif n == 0:
        zeilen.append((f"{pot(a, 0)} = 1", "jede Zahl außer $0$ hoch $0$ ist $1$"))
        tipps = ["Denk an die Treppe: Jede Stufe nach unten teilt durch die Basis.",
                 f"${pot(a, 1)} = {a}$, eine Stufe tiefer: durch ${tk(a)}$.", "Das Ergebnis ist immer dasselbe."]
        fehler += [(0, "Hoch $0$ ergibt $1$, nicht $0$."), (a, "Das ist hoch $1$. Hoch $0$ ergibt $1$.")]
    else:
        m = -n
        zeilen.append((f"{pot(a, n)} = \\frac{{1}}{{{pot(a, m)}}}", "negativer Exponent: Kehrwert"))
        zeilen.append((f"= {tex(w)}", f"${pot(a, m)} = {tex(F(a) ** m)}$"))
        tipps = ["Ein negativer Exponent bildet den Kehrwert.", f"${pot(a, n)} = \\frac{{1}}{{{pot(a, m)}}}$.",
                 f"${pot(a, m)} = {tex(F(a) ** m)}$."]
        fehler += [(-(F(a) ** m), "Ein negativer Exponent macht die Zahl nicht negativ. Er bildet den Kehrwert."),
                   (a * n, f"Du hast ${tk(a)} \\cdot ({n})$ gerechnet. Negativer Exponent heißt: Kehrwert der Potenz."),
                   (-w, "Das Minus im Exponenten ist kein Vorzeichen des Ergebnisses.")]
    fehler = [(f, t) for f, t in fehler if f is not None]
    return {
        "frage": f"Berechne ${pot(a, n)}$.",
        "loesung": w, "gekuerzt": True,
        "tipps": tipps, "rechenweg": _zeilen(*zeilen),
        "erklaerung": "Positiver Exponent: so viele Faktoren. $a^0 = 1$. Negativer Exponent: Kehrwert.",
        "typische_fehler": ohne_gleiche(w, fehler),
    }


def potenzgesetze_exponent(rng):
    basis = rng.choice(["2", "3", "5", "10", "a", "x"])
    art = rng.choice(["mal", "geteilt", "hoch", "gemischt"])
    m, n = rng.randint(2, 9), rng.randint(2, 6)
    if rng.random() < 0.3:
        n = -n
    p = lambda e: f"{basis}^{{{e}}}"  # noqa: E731
    if art == "hoch" and m == 2:
        m = 3                     # (a^2)^2: alle typischen Fehler fielen mit der Lösung zusammen
    if art == "mal":
        w, formel = m + n, f"{p(m)} \\cdot {p(n)} = {basis}^{{\\luecke}}"
        zeilen = [(f"{p(m)} \\cdot {p(n)} = {basis}^{{{m} + {tk(n)}}}", "gleiche Basis: Exponenten addieren")]
        fehler = [(m * n, "Beim Malnehmen werden die Exponenten **addiert**, nicht malgenommen."),
                  (m - n, "Das wäre beim Teilen. Beim Malnehmen wird addiert.")]
        tipp = "Gleiche Basis, malnehmen: Exponenten addieren."
    elif art == "geteilt":
        w, formel = m - n, f"\\frac{{{p(m)}}}{{{p(n)}}} = {basis}^{{\\luecke}}"
        zeilen = [(f"\\frac{{{p(m)}}}{{{p(n)}}} = {basis}^{{{m} - {tk(n)}}}", "gleiche Basis: Exponenten subtrahieren")]
        fehler = [(m + n, "Beim Teilen wird der Exponent des Nenners **abgezogen**."),
                  (F(m, n), "Die Exponenten werden nicht geteilt, sondern subtrahiert.")]
        tipp = "Gleiche Basis, teilen: Exponent oben minus Exponent unten."
    elif art == "hoch":
        w, formel = m * n, f"\\left({p(m)}\\right)^{{{n}}} = {basis}^{{\\luecke}}"
        zeilen = [(f"\\left({p(m)}\\right)^{{{n}}} = {basis}^{{{m} \\cdot {tk(n)}}}", "Potenz einer Potenz: Exponenten malnehmen")]
        fehler = [(m + n, "Bei einer Potenz einer Potenz werden die Exponenten **malgenommen**."),
                  (m ** n if abs(m ** n) < 10 ** 6 and n > 0 else None, "Der neue Exponent ist $m \\cdot n$, nicht $m^n$.")]
        tipp = "Potenz einer Potenz: Exponenten malnehmen."
    else:
        q = rng.randint(2, 6)
        w = m + n - q
        formel = f"\\frac{{{p(m)} \\cdot {p(n)}}}{{{p(q)}}} = {basis}^{{\\luecke}}"
        zeilen = [(f"\\frac{{{p(m)} \\cdot {p(n)}}}{{{p(q)}}} = \\frac{{{basis}^{{{m + n}}}}}{{{p(q)}}}", "Zähler: Exponenten addieren"),
                  (f"= {basis}^{{{m + n} - {q}}}", "teilen: Exponenten subtrahieren")]
        fehler = [(m + n + q, "Der Exponent im Nenner wird **abgezogen**."),
                  (m * n - q, "Im Zähler werden die Exponenten addiert, nicht malgenommen.")]
        tipp = "Erst den Zähler zusammenfassen, dann teilen."
    zeilen.append((f"= {basis}^{{{w}}}", "ausrechnen"))
    fehler = [([f], t) for f, t in fehler if f is not None and f != w]
    vorher = set()
    fehler = [x for x in fehler if not (x[0][0] in vorher or vorher.add(x[0][0]))]
    weg = _zeilen(*zeilen)
    return {
        "typ": "luecke",
        "frage": "Welcher Exponent gehört in die Lücke?",
        "formel": formel, "antworten": [[w]],
        "tipps": [tipp, "Schreib im Zweifel die Faktoren aus.", "Rechne nur mit den Exponenten, die Basis bleibt."],
        "rechenweg": weg,
        "erklaerung": "$a^m a^n = a^{m+n}$, $\\frac{a^m}{a^n} = a^{m-n}$, $(a^m)^n = a^{m \\cdot n}$.",
        "typische_fehler": fehler,
    }


def wissenschaftlich(rng):
    mant = rng.choice([F(12, 10), F(25, 10), F(3), F(45, 10), F(6), F(72, 10), F(8), F(95, 10), F(375, 100), F(2)])
    e = rng.choice([x for x in range(-7, 9) if x not in (0, 1, -1)])
    zahl = mant * F(10) ** e
    mt = mathlib.dezimal(mant, 6)
    zt = mathlib.dezimal(zahl, 12)
    richtung = "links" if e > 0 else "rechts"
    fehler = [([-e], "Das Vorzeichen stimmt nicht. Große Zahlen haben positive, kleine Zahlen negative Exponenten."),
              ([e - 1 if e > 0 else e + 1], "Zähle die Stellen noch einmal genau, um die das Komma wandert.")]
    return {
        "typ": "luecke",
        "frage": "Schreibe in wissenschaftlicher Schreibweise.",
        "formel": f"{zt} = {mt} \\cdot 10^{{\\luecke}}", "antworten": [[e]],
        "tipps": [f"Um wie viele Stellen wandert das Komma von ${zt}$ bis ${mt}$?",
                  f"Es wandert ${abs(e)}$ Stellen nach {richtung}.",
                  "Große Zahl: positiver Exponent. Zahl kleiner als $1$: negativer Exponent."],
        "rechenweg": _zeilen((f"{mt} \\cdot 10^{{{e}}} = {zt}", f"Komma ${abs(e)}$ Stellen nach {'rechts' if e > 0 else 'links'} schieben")),
        "erklaerung": "Der Exponent zählt, wie weit das Komma wandert.",
        "typische_fehler": fehler,
    }


k.praxis()

k.generator(potenz_auswerten, typ="zahl", titel="Potenzen ausrechnen", glatt=True)
k.generator(potenzgesetze_exponent, typ="luecke", titel="Potenzgesetze")
k.generator(wissenschaftlich, typ="luecke", titel="Wissenschaftliche Schreibweise")

k.luecke("Vereinfache so weit wie möglich (Uni-Niveau, $x, y \\neq 0$).",
         "\\left(x^{3} y^{-2}\\right)^{2} \\cdot x^{-4} y^{5} = x^{\\luecke} y^{\\luecke}", [[2], [1]],
         "Erst die Klammer: $x^6 y^{-4}$. Dann je Basis die Exponenten addieren: $x^{6 - 4} y^{-4 + 5} = x^2 y$.",
         tipps=["Löse zuerst die Klammer auf: Jeder Exponent darin mal $2$.", "$x^6 y^{-4} \\cdot x^{-4} y^5$",
                "Für $x$: $6 + (-4)$. Für $y$: $-4 + 5$."],
         rechenweg=r"""
         :::rechnung
         (x^3 y^{-2})^2 \cdot x^{-4} y^5 = x^6 y^{-4} \cdot x^{-4} y^5 || Klammer: Exponenten mal $2$
         = x^{6 - 4} y^{-4 + 5} || gleiche Basen: Exponenten addieren
         = x^2 y || ausrechnen
         :::
         """,
         typische_fehler=[([2, -3], "In der Klammer wird **jeder** Exponent mit $2$ malgenommen: $y^{-2 \\cdot 2} = y^{-4}$."),
                          ([-1, 1], "$x^{3}$ hoch $2$ ist $x^6$, nicht $x^5$: Exponenten malnehmen.")])

# Übungsblatt-Stil: alles auf Basis 2
_zaehler = 5 + 2 * 3          # 2^5 · 4^3 = 2^5 · 2^6
_nenner = 3 * 2 - 1           # 8^2 · 2^(-1) = 2^6 · 2^(-1)
_wert = F(2) ** (_zaehler - _nenner)
assert _wert == F(2 ** 5 * 4 ** 3) / (F(8 ** 2) * F(1, 2))
k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: Potenzen zur gleichen Basis

    Berechnen Sie ohne Taschenrechner und geben Sie alle Zwischenschritte an:
    $$\frac{2^{5} \cdot 4^{3}}{8^{2} \cdot 2^{-1}}$$
    """,
    [{"typ": "luecke", "frage": "Schreibe $4^3$ als Zweierpotenz.", "formel": "4^{3} = 2^{\\luecke}", "antworten": [[6]],
      "tipps": ["$4 = 2^2$.", "$(2^2)^3$: Exponenten malnehmen."],
      "rechenweg": "$4^3 = (2^2)^3 = 2^6$",
      "typische_fehler": [([5], "$(2^2)^3$: Exponenten malnehmen, $2 \\cdot 3 = 6$.")]},
     {"typ": "luecke", "frage": "Fasse den Zähler zusammen.", "formel": "2^{5} \\cdot 2^{6} = 2^{\\luecke}",
      "antworten": [[_zaehler]],
      "tipps": ["Gleiche Basis, malnehmen.", "$5 + 6$"], "rechenweg": "$2^5 \\cdot 2^6 = 2^{11}$",
      "typische_fehler": [([30], "Beim Malnehmen werden Exponenten addiert.")]},
     {"typ": "luecke", "frage": "Fasse den Nenner zusammen ($8 = 2^3$).", "formel": "8^{2} \\cdot 2^{-1} = 2^{\\luecke}",
      "antworten": [[_nenner]],
      "tipps": ["$8^2 = (2^3)^2 = 2^6$.", "$6 + (-1)$"], "rechenweg": "$8^2 \\cdot 2^{-1} = 2^6 \\cdot 2^{-1} = 2^5$",
      "typische_fehler": [([7], "$2^{-1}$ hat den Exponenten $-1$: $6 + (-1) = 5$."),
                          ([-6], "Bei gleicher Basis werden die Exponenten addiert, nicht malgenommen.")]},
     {"typ": "zahl", "frage": "Berechne den ganzen Bruch.", "loesung": _wert,
      "tipps": ["$\\frac{2^{11}}{2^5}$", "$2^{11 - 5} = 2^6$"], "rechenweg": "$\\frac{2^{11}}{2^5} = 2^6 = 64$",
      "typische_fehler": [(2 ** 16, "Beim Teilen wird der Exponent des Nenners abgezogen: $11 - 5$."),
                          (6, "$2^6$ ist nicht $6$, sondern $64$.")]}],
    "Alles auf dieselbe Basis bringen, dann nur noch mit Exponenten rechnen.",
    uebungsblatt=True,
    tipps=["Schreibe $4$ und $8$ als Zweierpotenzen.", "Dann Zähler und Nenner getrennt zusammenfassen."],
    rechenweg=r"""
    :::rechnung
    \frac{2^5 \cdot 4^3}{8^2 \cdot 2^{-1}} = \frac{2^5 \cdot (2^2)^3}{(2^3)^2 \cdot 2^{-1}} || $4 = 2^2$, $8 = 2^3$
    = \frac{2^5 \cdot 2^6}{2^6 \cdot 2^{-1}} || Potenz einer Potenz
    = \frac{2^{11}}{2^5} || Exponenten addieren
    = 2^6 || Exponenten subtrahieren
    = 64 || ausrechnen
    :::
    """)

k.zusammenfassung(r"""
    ## Potenzen

    | Regel | Formel | Beispiel |
    |---|---|---|
    | Bedeutung | $a^n = a \cdot a \cdots a$ ($n$ Faktoren) | $2^5 = 32$ |
    | gleiche Basis mal | $a^m \cdot a^n = a^{m+n}$ | $2^3 \cdot 2^4 = 2^7$ |
    | gleiche Basis geteilt | $\frac{a^m}{a^n} = a^{m-n}$ | $\frac{2^6}{2^2} = 2^4$ |
    | Potenz einer Potenz | $(a^m)^n = a^{m \cdot n}$ | $(2^3)^2 = 2^6$ |
    | gleicher Exponent | $a^n b^n = (ab)^n$ | $2^5 \cdot 5^5 = 10^5$ |
    | null | $a^0 = 1$ ($a \neq 0$) | $7^0 = 1$ |
    | negativ | $a^{-n} = \frac{1}{a^n}$ | $2^{-3} = \frac{1}{8}$ |

    !! Für Summen gibt es kein Potenzgesetz: $2^3 + 2^4 \neq 2^7$.

    - $(-2)^4 = 16$, aber $-2^4 = -16$.
    - $2^8 = 256$, $2^{10} = 1024 \approx 10^3$.
    - Wissenschaftliche Schreibweise: $0{,}0004 = 4 \cdot 10^{-4}$, in Python `4e-4`.
""")
