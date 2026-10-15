# -*- coding: utf-8 -*-
"""Fundament 14: Exponentialfunktion und Logarithmus – Wachstum, e, Logarithmusgesetze, log2, Gleichungen."""
import math
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

tex = mathlib.tex
vz = mathlib.vorzeichen_tex

k = neues_kapitel(
    slug="exp_log",
    titel="Exponentialfunktion und Logarithmus",
    beschreibung="Exponentielles Wachstum, die Zahl e, Logarithmen, log₂ und Bits, Exponentialgleichungen",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="🚀")

k.lernziele([
    "Ich kann Potenzen mit negativen Exponenten ausrechnen und erkenne exponentielles Wachstum",
    "Ich kann Logarithmen wie $\\log_2(32)$ im Kopf bestimmen, weil ich weiß, welche Frage sie beantworten",
    "Ich kann die Logarithmusgesetze anwenden und kenne den Fehler $\\log(a + b) \\neq \\log(a) + \\log(b)$",
    "Ich kann Exponentialgleichungen wie $3 \\cdot 2^x = 96$ oder $\\mathrm{e}^{2x} = 7$ lösen",
    "Ich kann mit $\\log_2$ ausrechnen, wie viele Bits man für $n$ Zustände braucht",
])

k.warum(r"""
Der [[Zweierlogarithmus]] ist die Lieblingsfunktion der Informatik. Mit $n$ Bits kannst du
$2^n$ verschiedene Muster speichern. Umgekehrt brauchst du für $1000$ Zustände
$\lceil \log_2(1000) \rceil = 10$ Bits. Die Binärsuche findet einen Eintrag unter einer
Million in höchstens $20$ Schritten, weil $2^{20} > 1\,000\,000$. Andersherum ist
[[exponentielles Wachstum]] der Albtraum: Ein Passwort aus $n$ Bits durchzuprobieren
kostet $2^n$ Versuche. Jedes zusätzliche Bit verdoppelt die Arbeit.
""")

# ── 1: Exponentielles Wachstum ─────────────────────────────────────────────
k.erklaerung("Exponentielles Wachstum", r"""
    ## Immer wieder verdoppeln

    :::analogie 🦠 Bakterien
    Ein Bakterium teilt sich jede Stunde in zwei. Nach $1$ Stunde sind es $2$, nach
    $2$ Stunden $4$, nach $3$ Stunden $8$. Jede Stunde wird **mal** $2$ genommen,
    nicht plus $2$.
    :::

    Wächst etwas in gleichen Schritten immer um denselben **Faktor**, heißt das
    [[exponentielles Wachstum]]. Die Anzahl nach $x$ Stunden ist $2^x$.

    :::rechnung $3$ Bakterien nach $4$ Stunden
    3 \cdot 2^4 || $4$-mal verdoppeln
    = 3 \cdot 16 || erst die Potenz
    = 48 || dann malnehmen
    :::

    :::visual funktionsgraph
    {"funktionen": [{"term": "2x", "label": "f(x)", "farbe": 2}, {"term": "2^x", "label": "g(x)", "farbe": 1}],
     "x": [-1, 6], "y": [-1, 40],
     "unterschrift": "Plus $2$ pro Schritt ($2x$) gegen mal $2$ pro Schritt ($2^x$): Die Verdopplung hängt alles ab."}
    :::

    :::alt Mit einem Blatt Papier erklärt
    Falte ein Blatt Papier. Jede Faltung verdoppelt die Dicke. Nach $10$ Faltungen
    liegen $2^{10} = 1024$ Lagen übereinander. Ein Stapel aus $10$ einzelnen
    Blättern wäre nur $10$ Lagen dick. Malnehmen schlägt Addieren.
    :::
    ---
    ## Die Exponentialfunktion

    Die Funktion $f(x) = a^x$ mit einer Basis $a > 0$, $a \neq 1$, heißt
    [[Exponentialfunktion]]. Die Variable steht im **Exponenten**.

    - $a^0 = 1$: Jeder Graph geht durch $(0 \mid 1)$.
    - $a^x > 0$ für alle $x$: Der Graph bleibt über der $x$-Achse.
    - $a > 1$: wächst. $0 < a < 1$: fällt.

    :::rechnung Negativer Exponent
    2^{-3} = \frac{1}{2^3} || Minus im Exponenten heißt: Kehrwert
    = \frac{1}{8} || ausrechnen
    :::

    :::visual funktionsgraph
    {"funktionen": [{"term": "a^x", "label": "f(x)"}],
     "parameter": [{"name": "a", "wert": 2, "von": 0.25, "bis": 4, "schritt": 0.25}],
     "x": [-4, 4], "y": [-1, 10],
     "unterschrift": "Für jedes $a$ geht der Graph durch $(0 \\mid 1)$. Für $a < 1$ fällt er."}
    :::

    :::achtung Zwei Verwechslungen
    $2^{-3}$ ist **nicht** negativ, sondern $\frac{1}{8}$. Und $2^x$ ist nicht $2x$:
    $2^5 = 32$, aber $2 \cdot 5 = 10$.
    :::

    :::alt Mit einer Leiter erklärt
    Geh auf der Leiter $\ldots, \frac{1}{4}, \frac{1}{2}, 1, 2, 4, 8, \ldots$ eine
    Sprosse nach rechts, nimmst du mal $2$. Eine Sprosse nach links: geteilt durch $2$.
    $2^{-3}$ heißt: von der $1$ aus drei Sprossen nach links, also $\frac{1}{8}$. Unter
    die $0$ kommst du so nie.
    :::
    ---
    ## Die Zahl e

    :::analogie 💶 Zinsen
    Eine Bank gibt $100\,\%$ Zinsen im Jahr. Zahlt sie zweimal im Jahr je $50\,\%$
    aus, wird aus $1$ € mehr als $2$ €, weil die Zinsen mitverzinst werden.
    :::

    Teilt man das Jahr in $n$ Teile, hat man am Ende $\left(1 + \frac{1}{n}\right)^n$ Euro.
    Für sehr großes $n$ nähert sich das der [[eulersche Zahl|eulersche Zahl]]
    $\mathrm{e} = 2{,}71828\ldots$ Die Funktion $f(x) = \mathrm{e}^x$ heißt kurz
    $\exp(x)$. Sie ist **die** Exponentialfunktion der Uni.

    :::rechnung Zwei und vier Zinstermine
    \left(1 + \frac{1}{2}\right)^2 = \left(\frac{3}{2}\right)^2 = \frac{9}{4} || $2{,}25$ €
    \left(1 + \frac{1}{4}\right)^4 = \left(\frac{5}{4}\right)^4 = \frac{625}{256} || etwa $2{,}44$ €
    :::

    :::alt Mit der Steigung erklärt
    Zeichne die Graphen von $2^x$ und $3^x$. An der Stelle $0$ ist $2^x$ etwas flacher
    als die Gerade $y = x + 1$, $3^x$ etwas steiler. Genau dazwischen liegt eine Basis,
    deren Graph bei $(0 \mid 1)$ die Steigung $1$ hat. Diese Basis ist $\mathrm{e}$.
    :::
    """)

k.zahl("Berechne $2^{-2}$.", F(1, 4),
       "$2^{-2} = \\frac{1}{2^2} = \\frac{1}{4}$.",
       tipps=["Minus im Exponenten heißt Kehrwert.", "$2^{-2} = \\frac{1}{2^2}$", "$2^2 = 4$"],
       rechenweg=r"""
       :::rechnung
       2^{-2} = \frac{1}{2^2} || Kehrwert
       = \frac{1}{4} || ausrechnen
       :::
       """,
       typische_fehler=[(-4, "Du hast $2 \\cdot (-2)$ gerechnet. Potenz heißt mehrfach malnehmen, nicht Basis mal Exponent. "
                             "Und der negative Exponent macht die Zahl nicht negativ, er bedeutet Kehrwert: $\\frac{1}{4}$."),
                        (F(-1, 4), "Das Minus gehört nicht vor das Ergebnis. $2^{-2} = \\frac{1}{4}$ ist positiv."),
                        (4, "Du hast das Minus im Exponenten weggelassen. $2^{-2}$ ist der Kehrwert von $2^2$.")])

k.zahl("In einer Petrischale sind $5$ Bakterien. Ihre Anzahl verdoppelt sich jede Stunde. Wie viele sind es nach $3$ Stunden?",
       5 * 2 ** 3,
       "$5 \\cdot 2^3 = 5 \\cdot 8 = 40$.",
       tipps=["Jede Stunde wird mal $2$ genommen.", "Nach $3$ Stunden: $5 \\cdot 2 \\cdot 2 \\cdot 2$.", "$5 \\cdot 8$"],
       rechenweg=r"""
       :::rechnung
       5 \cdot 2^3 || dreimal verdoppeln
       = 5 \cdot 8 || Potenz zuerst
       = 40 || malnehmen
       :::
       """,
       typische_fehler=[(11, "Du hast jede Stunde $2$ addiert. Verdoppeln heißt **mal** $2$."),
                        (1000, "Du hast $(5 \\cdot 2)^3$ gerechnet. Die Potenz gehört nur zur $2$: $5 \\cdot 2^3$."),
                        (30, "Du hast $5 \\cdot 2 \\cdot 3$ gerechnet. $2^3$ heißt $2 \\cdot 2 \\cdot 2$.")])

k.mc("Welche Funktion ist für große $x$ (zum Beispiel $x = 30$) am größten?",
     ["$2^x$", "$x^2$", "$100x$", "$1000$"],
     "$2^{30} = 1\\,073\\,741\\,824$, dagegen $30^2 = 900$ und $100 \\cdot 30 = 3000$. Exponentielles Wachstum "
     "überholt jede Potenz $x^2$ und jede Gerade irgendwann.",
     tipps=["Rechne alle vier für $x = 30$ aus, wenigstens grob.", "$2^{10} \\approx 1000$, also $2^{30} \\approx 1000^3$."],
     fehler={"$x^2$": "$30^2 = 900$. Bei $x^2$ steht das $x$ in der Basis, bei $2^x$ im Exponenten. Das zweite wächst viel schneller.",
             "$100x$": "Der große Faktor $100$ hilft nur am Anfang. $100 \\cdot 30 = 3000$, aber $2^{30}$ ist über eine Milliarde."})

k.wf("Für jede Basis $a > 0$ gilt $a^0 = 1$.", True,
     "Ja. Darum gehen alle Graphen $f(x) = a^x$ durch den Punkt $(0 \\mid 1)$.",
     tipps=["Denk an die Leiter: Wo steht man, bevor man den ersten Schritt macht?"])

# ── 2: Logarithmus ─────────────────────────────────────────────────────────
k.erklaerung("Der Logarithmus", r"""
    ## Die Frage nach dem Exponenten

    :::analogie 🔁 Wie oft verdoppeln?
    Aus $1$ Bakterium sollen $8$ werden. Wie viele Stunden musst du warten? Gesucht
    ist nicht das Ergebnis, sondern **wie oft** verdoppelt wird.
    :::

    Der [[Logarithmus]] beantwortet genau diese Frage:

    $$\log_a(y) = x \quad\Leftrightarrow\quad a^x = y$$

    Gelesen: „Logarithmus von $y$ zur Basis $a$“. Er ist die Zahl, mit der man $a$
    potenzieren muss, um $y$ zu erhalten. Erlaubt sind nur $y > 0$ und Basen $a > 0$, $a \neq 1$.

    :::rechnung Beispiele
    2^3 = 8 || darum ist $\log_2(8) = 3$
    \log_2(8) = 3 || der Exponent ist das Ergebnis
    10^3 = 1000 || darum ist $\log_{10}(1000) = 3$
    2^{-1} = \frac{1}{2} || darum ist $\log_2\left(\frac{1}{2}\right) = -1$
    :::

    :::visual exp_log
    {"basis": 2, "umkehr": true,
     "unterschrift": "$2^x$ und $\\log_2(x)$ sind Spiegelbilder an der Geraden $y = x$."}
    :::

    :::alt Mit Faktoren zählen erklärt
    Zerlege $8$ in Zweien: $8 = 2 \cdot 2 \cdot 2$. Das sind drei Zweien, also
    $\log_2(8) = 3$. Und $1000 = 10 \cdot 10 \cdot 10$: drei Zehnen, also
    $\log_{10}(1000) = 3$. Der Logarithmus zählt, wie viele Faktoren der Basis in
    der Zahl stecken.
    :::
    ---
    ## log₂: Bits und Halbieren

    Mit $n$ [[Bits|Bit]] gibt es $2^n$ verschiedene Muster. Für $N$ Zustände brauchst du also
    das kleinste $n$ mit $2^n \ge N$. Das ist $\log_2(N)$, aufgerundet.

    :::rechnung Wie viele Bits für $1000$ Zustände?
    2^9 = 512 || $9$ Bits reichen nicht
    2^{10} = 1024 || $10$ Bits reichen
    512 < 1000 \le 1024 || also $10$ Bits
    :::

    :::warum Binärsuche
    Eine sortierte Liste mit $1024$ Einträgen halbierst du bei jedem Vergleich. Nach
    $\log_2(1024) = 10$ Schritten bleibt ein Eintrag übrig.
    :::

    :::alt Mit Zahlenraten erklärt
    Jemand denkt sich eine Zahl von $1$ bis $8$. Du fragst: „Größer als $4$?“ und
    halbierst so jedes Mal. Nach drei Fragen weißt du die Zahl, denn $2^3 = 8$.
    Jede Ja/Nein-Antwort ist ein Bit.
    :::
    ---
    ## ln und lg

    Zwei Logarithmen haben eigene Namen:

    - $\ln(x) = \log_{\mathrm{e}}(x)$, der [[natürliche Logarithmus|natürlicher Logarithmus]],
    - $\operatorname{lg}(x) = \log_{10}(x)$, der Zehnerlogarithmus.

    :::rechnung Beispiele
    \ln(\mathrm{e}^3) = 3 || $\ln$ macht $\mathrm{e}^{\ldots}$ rückgängig
    \ln(1) = 0 || weil $\mathrm{e}^0 = 1$
    \log_{10}(0{,}01) = -2 || weil $10^{-2} = \frac{1}{100}$
    :::

    :::achtung Was „log“ bedeutet
    Steht im Uni-Skript nur $\log(x)$, ist meist $\ln(x)$ gemeint, in der
    Informatik oft $\log_2(x)$. Schau nach, was festgelegt ist. Und: $\log(0)$ und
    $\log(-1)$ gibt es nicht.
    :::

    :::alt Als Rückgängig-Taste erklärt
    $\mathrm{e}^x$ und $\ln(x)$ heben sich auf wie Strg+Z: $\ln(\mathrm{e}^5) = 5$
    und $\mathrm{e}^{\ln(5)} = 5$. Was die eine Funktion tut, macht die andere
    ungeschehen.
    :::
    """)

k.zahl("Berechne $\\log_2(32)$.", 5,
       "$2^5 = 32$, also $\\log_2(32) = 5$.",
       tipps=["Frage: $2$ hoch wie viel ergibt $32$?", "$2, 4, 8, 16, 32$: Zähle die Verdopplungen.", "$2^5 = 32$"],
       rechenweg=r"""
       :::rechnung
       2^5 = 32 || fünfmal die $2$
       \log_2(32) = 5 || der Exponent ist das Ergebnis
       :::
       """,
       typische_fehler=[(16, "Du hast $32 : 2$ gerechnet. Der Logarithmus fragt nach dem **Exponenten**: $2^? = 32$."),
                        (F(5, 2), "Fast: Der Exponent ist $5$. Er wird nicht noch durch $2$ geteilt.")])

k.zahl("Berechne $\\log_2\\left(\\frac{1}{8}\\right)$.", -3,
       "$2^{-3} = \\frac{1}{8}$, also $\\log_2\\left(\\frac{1}{8}\\right) = -3$.",
       tipps=["Welche Zweierpotenz ist $8$?", "$\\frac{1}{8}$ ist der Kehrwert von $2^3$.", "Kehrwert heißt Minus im Exponenten."],
       rechenweg=r"""
       :::rechnung
       2^{-3} = \frac{1}{2^3} = \frac{1}{8} || Kehrwert von $2^3$
       \log_2\left(\frac{1}{8}\right) = -3 || der Exponent ist $-3$
       :::
       """,
       typische_fehler=[(3, "Vorzeichen: $2^3 = 8$, aber gesucht ist $\\frac{1}{8} = 2^{-3}$."),
                        (F(1, 3), "Der Logarithmus von $\\frac{1}{8}$ ist nicht $\\frac{1}{3}$. Gesucht: $2^? = \\frac{1}{8}$.")])

k.zahl("Ein Spiel soll $200$ verschiedene Gegenstände unterscheiden. Wie viele Bits braucht man mindestens?", 8,
       "$2^7 = 128 < 200$ reicht nicht, $2^8 = 256 \\ge 200$ reicht. Also $8$ Bits.",
       tipps=["Mit $n$ Bits gibt es $2^n$ Muster.", "Suche die kleinste Zweierpotenz, die mindestens $200$ ist.",
              "$2^7 = 128$, $2^8 = 256$."],
       rechenweg=r"""
       :::rechnung
       2^7 = 128 || zu wenig
       2^8 = 256 || genug
       128 < 200 \le 256 || also $8$ Bits
       :::
       """,
       typische_fehler=[(7, "$7$ Bits ergeben nur $2^7 = 128$ Muster. Das ist weniger als $200$: aufrunden!"),
                        (200, "Ein Bit pro Gegenstand ist viel zu viel. Bits verdoppeln die Möglichkeiten: $2^n \\ge 200$.")])

# ── 3: Logarithmusgesetze ──────────────────────────────────────────────────
k.erklaerung("Logarithmusgesetze", r"""
    ## Aus mal wird plus

    Weil sich beim Malnehmen von Potenzen die Exponenten addieren
    ($2^3 \cdot 2^2 = 2^5$), gelten die [[Logarithmusgesetze]], für $u, v > 0$:

    $$\log_a(u \cdot v) = \log_a(u) + \log_a(v)$$
    $$\log_a\left(\frac{u}{v}\right) = \log_a(u) - \log_a(v)$$
    $$\log_a(u^r) = r \cdot \log_a(u)$$

    :::rechnung Beispiele
    \log_2(8 \cdot 4) = \log_2(8) + \log_2(4) = 3 + 2 = 5 || Produkt wird Summe
    \log_2(2^{10}) = 10 \cdot \log_2(2) = 10 || Exponent nach vorn
    :::

    :::achtung Für Summen gibt es keine Regel
    $\log(u + v) \neq \log(u) + \log(v)$. Probe: $\log_2(4 + 4) = \log_2(8) = 3$,
    aber $\log_2(4) + \log_2(4) = 4$.
    :::

    :::alt Mit Rechenschiebern erklärt
    Früher hat man mit Rechenschiebern malgenommen. Darauf sind die Zahlen im
    Abstand ihrer Logarithmen eingetragen. Legt man zwei Strecken aneinander,
    addiert man Logarithmen, und abgelesen wird das Produkt. Malnehmen wurde so
    zu Strecken addieren.
    :::
    ---
    ## Basiswechsel

    Der Taschenrechner kennt meist nur $\ln$ und $\operatorname{lg}$. Jeder andere Logarithmus
    lässt sich damit ausrechnen:

    $$\log_a(y) = \frac{\ln(y)}{\ln(a)}$$

    :::rechnung Probe mit einem bekannten Wert
    \frac{\ln(32)}{\ln(2)} = 5 || stimmt mit $\log_2(32) = 5$ überein
    \frac{\ln(10)}{\ln(2)} = \log_2(10) || etwa $3{,}32$
    :::

    :::alt Mit Maßeinheiten erklärt
    Logarithmen zu verschiedenen Basen unterscheiden sich nur um einen festen Faktor,
    wie Zentimeter und Zoll. $\ln(a)$ ist der Umrechnungsfaktor: Teile durch ihn,
    und du hast den Logarithmus zur Basis $a$.
    :::
    """)

k.luecke("Wende das Produktgesetz an und rechne aus:",
         "\\log_3(9 \\cdot 27) = \\log_3(9) + \\log_3(27) = 2 + \\luecke = \\luecke",
         [[3], [5]],
         "$3^3 = 27$, also $\\log_3(27) = 3$. Summe: $2 + 3 = 5$. Probe: $9 \\cdot 27 = 243 = 3^5$.",
         tipps=["$3$ hoch wie viel ergibt $27$?", "$\\log_3(27) = 3$.", "$2 + 3$"],
         rechenweg=r"""
         :::rechnung
         3^2 = 9 || also $\log_3(9) = 2$
         3^3 = 27 || also $\log_3(27) = 3$
         9 \cdot 27 = 243 = 3^5 || Probe: Ergebnis $5$
         :::
         """,
         typische_fehler=[([3, 6], "$2 + 3 = 5$, nicht $6$. Beim Produktgesetz werden die Logarithmen **addiert**."),
                          ([9, 11], "$\\log_3(27)$ ist der Exponent, nicht $27 : 3$. $3^3 = 27$.")])

k.wf("Für alle $u, v > 0$ gilt $\\log_2(u + v) = \\log_2(u) + \\log_2(v)$.", False,
     "Falsch. Gegenbeispiel: $\\log_2(4 + 4) = 3$, aber $\\log_2(4) + \\log_2(4) = 4$. Das Gesetz gilt für das **Produkt** $u \\cdot v$.",
     tipps=["Setz $u = v = 4$ ein und rechne beide Seiten aus."])

k.zahl("Berechne $\\log_2(4^5)$.", 10,
       "$\\log_2(4^5) = 5 \\cdot \\log_2(4) = 5 \\cdot 2 = 10$.",
       tipps=["Potenzgesetz: Den Exponenten $5$ darfst du nach vorn ziehen.", "$5 \\cdot \\log_2(4)$", "$\\log_2(4) = 2$"],
       rechenweg=r"""
       :::rechnung
       \log_2(4^5) = 5 \cdot \log_2(4) || Exponent nach vorn
       = 5 \cdot 2 || $2^2 = 4$
       = 10 || Probe: $4^5 = 1024 = 2^{10}$
       :::
       """,
       typische_fehler=[(7, "Du hast $\\log_2(4) + 5$ gerechnet. Der Exponent wird **malgenommen**: $5 \\cdot \\log_2(4)$."),
                        (20, "$\\log_2(4)$ ist $2$, nicht $4$. Also $5 \\cdot 2$.")])

# ── 4: Exponentialgleichungen ──────────────────────────────────────────────
k.erklaerung("Exponentialgleichungen", r"""
    ## Glatte Fälle: gleiche Basis

    Steht die Unbekannte im Exponenten, heißt die Gleichung
    [[Exponentialgleichung]]. Erst die Potenz allein stellen, dann den Exponenten
    ablesen.

    :::rechnung Löse $3 \cdot 2^x = 96$
    3 \cdot 2^x = 96 || Potenz steht noch nicht allein
    2^x = 32 || durch $3$ teilen
    2^x = 2^5 || $32$ als Zweierpotenz schreiben
    x = 5 || Exponenten vergleichen
    :::

    :::achtung Nicht zu früh vereinfachen
    $3 \cdot 2^x$ ist **nicht** $6^x$. Potenz vor Mal: Erst teilst du durch $3$.
    :::

    :::alt Rückwärts gedacht
    Lies die Gleichung als Geschichte: Eine Zahl wurde $x$-mal verdoppelt und dann
    mit $3$ malgenommen. Heraus kam $96$. Mach es rückwärts: $96 : 3 = 32$. Und
    $32$ entsteht aus $1$ durch fünfmal Verdoppeln.
    :::
    ---
    ## Allgemein: logarithmieren

    Geht es nicht glatt auf, wendest du auf beiden Seiten den passenden Logarithmus an.
    $\ln$ hebt $\mathrm{e}^{\ldots}$ auf.

    :::rechnung Löse $\mathrm{e}^{2x} = 7$
    \mathrm{e}^{2x} = 7 || Potenz steht allein
    2x = \ln(7) || auf beiden Seiten $\ln$
    x = \frac{\ln(7)}{2} || durch $2$ teilen, etwa $0{,}97$
    :::

    Das exakte Ergebnis ist $\frac{\ln(7)}{2}$. Runde erst, wenn danach gefragt ist.

    :::alt Mit der Rückgängig-Taste erklärt
    $\mathrm{e}^{\ldots}$ hat etwas mit $2x$ gemacht. Um an $2x$ heranzukommen,
    drückst du auf beiden Seiten die Rückgängig-Taste $\ln$. Links bleibt $2x$, rechts
    steht $\ln(7)$. Der Rest ist eine ganz normale Gleichung.
    :::
    """)

k.zahl("Löse $5 \\cdot 3^x = 405$. Gib $x$ an.", 4,
       "$3^x = 81 = 3^4$, also $x = 4$.",
       tipps=["Stell zuerst die Potenz allein: Teile durch $5$.", "$3^x = 81$", "$3 \\cdot 3 \\cdot 3 \\cdot 3 = 81$"],
       rechenweg=r"""
       :::rechnung
       5 \cdot 3^x = 405 || Aufgabe
       3^x = 81 || durch $5$ teilen
       3^x = 3^4 || $81$ als Dreierpotenz
       x = 4 || Exponenten vergleichen
       :::
       """,
       typische_fehler=[(81, "$81$ ist der Wert von $3^x$. Gesucht ist der Exponent $x$."),
                        (27, "Du hast $405 : 15$ gerechnet, also $5 \\cdot 3$ zuerst. Potenz vor Mal: erst durch $5$ teilen.")])

k.zahl("Löse $4 \\cdot \\mathrm{e}^{2x} = 12$. Gib das Ergebnis exakt an, zum Beispiel als `ln(5)/3`.",
       "ln(3)/2",
       "$\\mathrm{e}^{2x} = 3$, also $2x = \\ln(3)$ und $x = \\frac{\\ln(3)}{2} \\approx 0{,}549$.",
       tipps=["Erst die Potenz allein: durch $4$ teilen.", "$\\mathrm{e}^{2x} = 3$. Jetzt $\\ln$ auf beiden Seiten.",
              "$2x = \\ln(3)$"],
       rechenweg=r"""
       :::rechnung
       4 \cdot \mathrm{e}^{2x} = 12 || Aufgabe
       \mathrm{e}^{2x} = 3 || durch $4$ teilen
       2x = \ln(3) || $\ln$ auf beiden Seiten
       x = \frac{\ln(3)}{2} || durch $2$ teilen
       :::
       """,
       typische_fehler=[("ln(12)/2", "Du hast vergessen, zuerst durch $4$ zu teilen. Die Potenz muss allein stehen."),
                        ("ln(3/2)", "Du hast durch $2$ geteilt, bevor du logarithmiert hast. Erst $\\ln$, dann durch $2$."),
                        ("ln(3)", "Fast: $2x = \\ln(3)$. Jetzt noch durch $2$ teilen.")])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


_EXPONENTEN = {2: [-4, -3, -2, -1, 2, 3, 4, 5, 6, 7, 8, 10], 3: [-3, -2, -1, 2, 3, 4, 5],
               5: [-2, -1, 2, 3, 4], 10: [-3, -2, -1, 2, 3, 4, 6]}


def log_berechnen(rng):
    b = rng.choice([2, 2, 3, 5, 10])
    e = rng.choice(_EXPONENTEN[b])
    y = F(b) ** e
    if e > 0:
        ytex = str(y)
    elif b == 10:
        ytex = mathlib.dezimal(y)
    else:
        ytex = f"\\frac{{1}}{{{b ** -e}}}"
    zeilen = []
    if e > 0:
        zeilen.append((f"{b}^{{{e}}} = {y}", f"${e}$-mal die ${b}$ malnehmen"))
    else:
        zeilen.append((f"{b}^{{{e}}} = \\frac{{1}}{{{b}^{{{-e}}}}} = {ytex}", "Minus im Exponenten heißt Kehrwert"))
    zeilen.append((f"\\log_{{{b}}}\\left({ytex}\\right) = {e}", "der Exponent ist das Ergebnis"))
    fehler = [(-e, "Vorzeichen: " + ("Eine Zahl kleiner als $1$ hat einen **negativen** Logarithmus." if e < 0
                                     else "Eine Zahl größer als $1$ hat einen **positiven** Logarithmus.")),
              (y / b if e > 1 else None, f"Du hast ${ytex}$ durch ${b}$ geteilt. Gesucht ist der Exponent: ${b}^? = {ytex}$."),
              (b ** -e if e < 0 and b != 10 else None, f"Das ist der Nenner. Gesucht ist der Exponent: ${b}^? = {ytex}$."),
              (b ** -e if e < 0 and b == 10 else None, f"${ytex} = \\frac{{1}}{{{b ** -e}}}$: Du hast den Nenner angegeben. "
                                                       f"Gesucht ist der Exponent: ${b}^? = {ytex}$.")]
    fehler = [(w, m) for w, m in fehler if w is not None]
    return {
        "frage": f"Berechne $\\log_{{{b}}}\\left({ytex}\\right)$.",
        "loesung": e,
        "tipps": [f"Frage dich: ${b}$ hoch wie viel ergibt ${ytex}$?",
                  "Ist die Zahl kleiner als $1$, ist der Exponent negativ." if e < 0
                  else f"Zähle, wie oft du ${b}$ mit sich selbst malnehmen musst.",
                  f"${b}^{{{e}}} = {ytex}$"],
        "rechenweg": _zeilen(*zeilen),
        "erklaerung": "$\\log_a(y)$ ist der Exponent $x$ mit $a^x = y$.",
        "typische_fehler": ohne_gleiche(e, fehler),
    }


k.praxis()

k.generator(log_berechnen, typ="zahl", titel="Logarithmen im Kopf", glatt=True)


def exp_gleichung(rng):
    b = rng.choice([2, 2, 3, 5])
    xmax = {2: 7, 3: 4, 5: 3}[b]
    if rng.random() < 0.5:
        x = rng.randint(2, xmax)
        c = rng.choice([c for c in range(2, 8) if c != b])
        d = c * b ** x
        zeilen = [(f"{c} \\cdot {b}^x = {d}", "Aufgabe"),
                  (f"{b}^x = {b ** x}", f"durch ${c}$ teilen"),
                  (f"{b}^x = {b}^{{{x}}}", f"${b ** x}$ als Potenz von ${b}$"),
                  (f"x = {x}", "Exponenten vergleichen")]
        fehler = [(b ** x, f"${b ** x}$ ist der Wert von ${b}^x$. Gesucht ist der Exponent $x$."),
                  (F(d, c * b), f"Du hast ${b ** x}$ noch einmal durch ${b}$ geteilt. Gesucht ist, wie oft man ${b}$ "
                                f"malnehmen muss, um ${b ** x}$ zu erhalten.")]
        frage = f"Löse ${c} \\cdot {b}^x = {d}$."
        tipps = [f"Stell die Potenz allein: Teile durch ${c}$.", f"${b}^x = {b ** x}$",
                 f"${b ** x}$ ist ${b}$ hoch ${x}$."]
    else:
        s = rng.choice([z for z in (-2, -1, 1, 2, 3) if max(2, 1 + z) <= xmax])
        x = rng.randint(max(2, 1 + s), xmax) - s          # Exponent x + s liegt zwischen 2 und xmax, x >= 1
        d = b ** (x + s)
        zeilen = [(f"{b}^{{x {vz(F(s))}}} = {d}", "Aufgabe"),
                  (f"{b}^{{x {vz(F(s))}}} = {b}^{{{x + s}}}", f"${d}$ als Potenz von ${b}$"),
                  (f"x {vz(F(s))} = {x + s}", "Exponenten vergleichen"),
                  (f"x = {x}", f"${vz(F(-s))}$ auf beiden Seiten")]
        fehler = [(x + s, f"Das ist der ganze Exponent $x {vz(F(s))}$. Jetzt noch nach $x$ auflösen."),
                  (x + 2 * s, "Beim Auflösen hast du in die falsche Richtung gerechnet. Probe: Setz dein $x$ ein.")]
        frage = f"Löse ${b}^{{x {vz(F(s))}}} = {d}$."
        tipps = [f"Schreib ${d}$ als Potenz von ${b}$.", f"${d} = {b}^{{{x + s}}}$. Vergleiche die Exponenten.",
                 f"$x {vz(F(s))} = {x + s}$"]
    return {
        "frage": frage, "loesung": x, "tipps": tipps,
        "rechenweg": _zeilen(*zeilen),
        "erklaerung": "Potenz allein stellen, beide Seiten als Potenz derselben Basis schreiben, Exponenten vergleichen.",
        "typische_fehler": ohne_gleiche(x, fehler),
    }


k.generator(exp_gleichung, typ="zahl", titel="Exponentialgleichungen", glatt=True)

_DINGE = ["Farben", "Spielfiguren", "Zeichen", "Sensorzustände", "Räume in einem Gebäude", "Lagerplätze", "Tonhöhen"]


def bits_zaehlen(rng):
    n_bits = rng.randint(3, 12)
    if rng.random() < 0.25:
        anzahl = 2 ** n_bits
    else:
        anzahl = rng.randint(2 ** (n_bits - 1) + 1, 2 ** n_bits - 1)
    ding = rng.choice(_DINGE)
    zeilen = [(f"2^{{{n_bits - 1}}} = {2 ** (n_bits - 1)}", f"${n_bits - 1}$ Bits reichen nicht"),
              (f"2^{{{n_bits}}} = {2 ** n_bits}", f"${n_bits}$ Bits reichen"),
              (f"{2 ** (n_bits - 1)} < {anzahl} \\le {2 ** n_bits}", f"also ${n_bits}$ Bits")]
    fehler = [(n_bits - 1, f"${n_bits - 1}$ Bits ergeben nur $2^{{{n_bits - 1}}} = {2 ** (n_bits - 1)}$ Muster. Das ist zu wenig."),
              (n_bits + 1, f"Schon $2^{{{n_bits}}} = {2 ** n_bits}$ Muster reichen für ${anzahl}$."
                           + (" Genau gleich viele reicht auch." if anzahl == 2 ** n_bits else "")),
              (anzahl, "Ein Bit pro Möglichkeit ist viel zu viel. $n$ Bits ergeben $2^n$ Muster.")]
    return {
        "frage": f"Ein Programm soll ${anzahl}$ verschiedene {ding} als Bitmuster speichern. "
                 "Wie viele Bits braucht es mindestens?",
        "loesung": n_bits,
        "tipps": ["Mit $n$ Bits gibt es $2^n$ verschiedene Muster.",
                  f"Suche die kleinste Zweierpotenz, die mindestens ${anzahl}$ ist.",
                  f"$2^{{{n_bits - 1}}} = {2 ** (n_bits - 1)}$ und $2^{{{n_bits}}} = {2 ** n_bits}$."],
        "rechenweg": _zeilen(*zeilen),
        "erklaerung": "Man braucht das kleinste $n$ mit $2^n \\ge N$, also $\\log_2(N)$ aufgerundet.",
        "typische_fehler": ohne_gleiche(n_bits, fehler),
    }


k.generator(bits_zaehlen, typ="zahl", titel="Bits zählen mit log₂", glatt=True)

k.zahl("Wie viele Vergleiche braucht die Binärsuche höchstens, um in einer sortierten Liste mit "
       "$2^{20} = 1\\,048\\,576$ Einträgen einen Eintrag zu finden? Nimm an: Jeder Vergleich halbiert die Liste, "
       "und am Ende bleibt genau ein Eintrag übrig.",
       20,
       "Nach $k$ Halbierungen sind noch $\\frac{2^{20}}{2^k}$ Einträge übrig. Bei $k = 20$ ist es einer. Also $\\log_2(2^{20}) = 20$.",
       tipps=["Jeder Vergleich halbiert die Anzahl.", "Wie oft kann man $2^{20}$ halbieren, bis $1$ übrig ist?",
              "$\\log_2(2^{20})$"],
       rechenweg=r"""
       :::rechnung
       \frac{2^{20}}{2^{20}} = 1 || nach $20$ Halbierungen bleibt ein Eintrag
       \log_2(2^{20}) = 20 || das ist der Logarithmus
       :::
       """,
       typische_fehler=[(524288, "Das ist die Hälfte der Liste, also die Anzahl nach **einem** Vergleich. Gesucht ist die Zahl der Halbierungen."),
                        (10, "$\\sqrt{2^{20}} = 2^{10}$ hilft hier nicht. Halbieren zählt Faktoren $2$: Es sind $20$.")])

# Übungsblatt-Stil
k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: Exponentialgleichung

    Bestimmen Sie alle $x \in \mathbb{R}$ mit
    $$5 \cdot 2^{x + 1} = 160.$$
    Geben Sie alle Umformungsschritte an.
    """,
    [{"typ": "zahl", "frage": "Stell die Potenz allein. Welchen Wert hat $2^{x + 1}$?", "loesung": 32,
      "tipps": ["Teile beide Seiten durch $5$.", "$160 : 5$"],
      "rechenweg": "$5 \\cdot 2^{x + 1} = 160 \\;\\Rightarrow\\; 2^{x + 1} = 32$",
      "typische_fehler": [(F(16), "Du hast durch $10$ geteilt. $5 \\cdot 2^{x + 1}$ ist nicht $10^{x + 1}$ und auch nicht $10 \\cdot 2^x$.")]},
     {"typ": "zahl", "frage": "Schreibe $32$ als Zweierpotenz. Welchen Wert hat also $x + 1$?", "loesung": 5,
      "tipps": ["$2^? = 32$", "$2, 4, 8, 16, 32$"],
      "rechenweg": "$2^{x + 1} = 2^5$, also $x + 1 = 5$.",
      "typische_fehler": [(16, "Gesucht ist der Exponent, nicht $32 : 2$.")]},
     {"typ": "zahl", "frage": "Welchen Wert hat $x$?", "loesung": 4,
      "tipps": ["$x + 1 = 5$", "Zieh $1$ ab."],
      "rechenweg": "$x + 1 = 5$, also $x = 4$. Probe: $5 \\cdot 2^5 = 160$.",
      "typische_fehler": [(6, "Du hast $1$ addiert statt abgezogen. Probe: $5 \\cdot 2^7 = 640 \\neq 160$.")]}],
    "Potenz allein stellen, als Potenz derselben Basis schreiben, Exponenten vergleichen, nach $x$ auflösen. Zum Schluss die Probe.",
    uebungsblatt=True,
    tipps=["Erst durch $5$ teilen.", "Dann die rechte Seite als Zweierpotenz schreiben."],
    rechenweg=r"""
    :::rechnung
    5 \cdot 2^{x + 1} = 160 || Aufgabe
    2^{x + 1} = 32 || durch $5$ teilen
    2^{x + 1} = 2^5 || $32 = 2^5$
    x + 1 = 5 || Exponenten vergleichen
    x = 4 || $1$ abziehen
    :::

    Probe: $5 \cdot 2^{4 + 1} = 5 \cdot 32 = 160$. Also $\mathbb{L} = \{4\}$.
    """)

k.zusammenfassung(r"""
    ## Exponentialfunktion und Logarithmus

    | Regel | Beispiel |
    |---|---|
    | $a^0 = 1$, $a^{-n} = \frac{1}{a^n}$ | $2^{-3} = \frac{1}{8}$ |
    | $\log_a(y) = x \Leftrightarrow a^x = y$ (für $a > 0$, $a \neq 1$, $y > 0$) | $\log_2(8) = 3$ |
    | $\log_a(u \cdot v) = \log_a(u) + \log_a(v)$ | $\log_2(32) = \log_2(8) + \log_2(4)$ |
    | $\log_a\left(\frac{u}{v}\right) = \log_a(u) - \log_a(v)$ | $\log_2\left(\frac{8}{2}\right) = 3 - 1$ |
    | $\log_a(u^r) = r \cdot \log_a(u)$ | $\log_2(4^5) = 5 \cdot 2 = 10$ |
    | $\log_a(y) = \frac{\ln(y)}{\ln(a)}$ | $\log_2(10) = \frac{\ln(10)}{\ln(2)}$ |

    - $\mathrm{e} = 2{,}71828\ldots$, $\ln = \log_{\mathrm{e}}$, $\operatorname{lg} = \log_{10}$; $\ln(\mathrm{e}^x) = x$.
    - Logarithmen gibt es nur von Zahlen $> 0$.

    !! $\log(u + v) \neq \log(u) + \log(v)$, und $3 \cdot 2^x \neq 6^x$.

    - Für $N$ Zustände braucht man $\log_2(N)$ Bits, aufgerundet. Binärsuche: $\log_2(n)$ Schritte.
    - Gleichung $c \cdot a^x = d$: Potenz allein stellen, dann logarithmieren oder Exponenten vergleichen.
""")
