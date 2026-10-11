# -*- coding: utf-8 -*-
"""Fundament 4: Dezimalzahlen und Prozent – Stellenwerte, Umwandeln, periodisch, Runden, Prozent."""
import math
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

tex = mathlib.tex


def dz(x):
    """Endliche Dezimalzahl als LaTeX mit deutschem Komma: 0{,}375."""
    return mathlib.dezimal(F(x), 8)


def dz_text(x):
    """Wie dz, aber für Fließtext außerhalb von Formeln nicht gedacht: nur in $…$ verwenden."""
    return dz(x)


k = neues_kapitel(
    slug="dezimal_prozent",
    titel="Dezimalzahlen und Prozent",
    beschreibung="Stellenwerte, Bruch und Dezimalzahl umwandeln, periodische Zahlen, Runden und Prozentrechnung",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="💯")

k.lernziele([
    "Ich kenne die Stellenwerte nach dem Komma und kann Dezimalzahlen vergleichen",
    "Ich kann Brüche in Dezimalzahlen umwandeln und umgekehrt, auch periodische",
    "Ich kann auf eine vorgegebene Stelle richtig runden",
    "Ich kann Prozentwert, Grundwert und Prozentsatz berechnen",
    "Ich weiß, warum $+20\\,\\%$ und danach $-20\\,\\%$ nicht zum Startwert zurückführt",
])

k.warum(r"""
Computer speichern Kommazahlen als [[Gleitkommazahl|Gleitkommazahlen]]. Dabei passieren
Rundungsfehler: In Python ergibt `0.1 + 0.2` nicht genau `0.3`. Warum das so ist,
verstehst du nach diesem Kapitel. Prozent brauchst du ständig: Ein Algorithmus ist
$30\,\%$ schneller, eine Datei wird um $60\,\%$ kleiner, $5\,\%$ der Tests schlagen fehl.
Wer hier sauber rechnet, fällt auf keine falsche Statistik herein.
""")

# ── 1: Stellenwerte ────────────────────────────────────────────────────────
k.erklaerung("Stellenwerte nach dem Komma", r"""
    ## Zehntel, Hundertstel, Tausendstel

    :::analogie 💶 Geld
    $3{,}45$ Euro sind $3$ Euro, $4$ Zehn-Cent-Münzen und $5$ Ein-Cent-Münzen.
    Ein Zehn-Cent-Stück ist ein Zehntel Euro, ein Cent ein Hundertstel Euro.
    :::

    Eine [[Dezimalzahl]] hat Stellen nach dem Komma. Jede Stelle ist zehnmal
    kleiner als die davor. Das ist ihr [[Stellenwert]].

    | Stelle nach dem Komma | 1. | 2. | 3. |
    |---|---|---|---|
    | Wert | Zehntel $\frac{1}{10}$ | Hundertstel $\frac{1}{100}$ | Tausendstel $\frac{1}{1000}$ |

    :::rechnung Beispiel vorgerechnet
    3{,}45 = 3 + \frac{4}{10} + \frac{5}{100} || $4$ Zehntel und $5$ Hundertstel
    :::

    :::visual zahlenstrahl
    {"von": 0, "bis": 1, "schritt": 0.1, "punkte": [{"x": "0,45", "label": "0{,}45"}, {"x": "0,5", "label": "0{,}5", "farbe": "orange"}],
     "unterschrift": "Zwischen $0$ und $1$ liegen zehn Zehntel. $0{,}45$ liegt genau zwischen $0{,}4$ und $0{,}5$."}
    :::

    :::alt Mit dem Zollstock erklärt
    Ein Meter hat $10$ Dezimeter, ein Dezimeter hat $10$ Zentimeter, ein Zentimeter
    hat $10$ Millimeter. $1{,}234$ Meter sind also $1$ Meter, $2$ Dezimeter,
    $3$ Zentimeter und $4$ Millimeter. Jede Stelle weiter rechts ist die nächstkleinere
    Einheit auf dem Zollstock.
    :::
    ---
    ## Vergleichen und das Komma verschieben

    Um zwei Dezimalzahlen zu vergleichen, gehst du Stelle für Stelle von links vor.
    Fehlende Stellen füllst du mit Nullen auf. Das ändert den Wert nicht.

    :::rechnung Beispiel vorgerechnet
    0{,}5 = 0{,}50 || eine Null hinten anhängen ändert nichts
    0{,}50 > 0{,}45 || $50$ Hundertstel sind mehr als $45$ Hundertstel
    3{,}45 \cdot 10 = 34{,}5 || mal $10$: Komma eine Stelle nach rechts
    3{,}45 : 100 = 0{,}0345 || durch $100$: Komma zwei Stellen nach links
    :::

    :::achtung Mehr Ziffern heißt nicht größer
    $0{,}45 > 0{,}5$ ist falsch, obwohl $45$ größer als $5$ ist. Vergleiche Stelle für
    Stelle: Bei den Zehnteln steht $4$ gegen $5$. Damit ist $0{,}5$ größer.
    :::

    :::alt Mit Cent erklärt
    Rechne beide Zahlen in Cent um. $0{,}5$ Euro sind $50$ Cent, $0{,}45$ Euro sind
    $45$ Cent. Jetzt siehst du sofort: $50$ Cent sind mehr. Malnehmen mit $100$ heißt
    genau das: Euro in Cent umrechnen, also $3{,}45$ Euro sind $345$ Cent.
    :::
    """)

k.mc("Welche Zahl ist am größten?",
     ["$0{,}5$", "$0{,}45$", "$0{,}405$", "$0{,}099$"],
     "Vergleiche zuerst die Zehntel: $5$ ist mehr als $4$ und $0$. Also ist $0{,}5$ am größten.",
     tipps=["Vergleiche Stelle für Stelle von links.", "Schau zuerst nur auf die erste Stelle nach dem Komma.",
            "Fülle mit Nullen auf: $0{,}500$, $0{,}450$, $0{,}405$, $0{,}099$."],
     fehler={"$0{,}45$": "Mehr Ziffern heißen nicht größer. Bei den Zehnteln steht $4$, bei $0{,}5$ steht $5$.",
             "$0{,}405$": "$405$ ist zwar die größte Ziffernfolge, aber es sind Tausendstel: $0{,}405 < 0{,}500$.",
             "$0{,}099$": "Die $99$ sind nur Hundertstel und Tausendstel. Bei den Zehnteln steht eine $0$."})

k.berechne("3,45*100",
           erklaerung="Mal $100$ heißt: Komma zwei Stellen nach rechts. $3{,}45 \\cdot 100 = 345$.",
           tipps=["Beim Malnehmen mit $10$, $100$, $1000$ wandert das Komma.", "Wie viele Nullen hat $100$?",
                  "Zwei Nullen: Komma zwei Stellen nach rechts."],
           rechenweg=r"""
           :::rechnung
           3{,}45 \cdot 10 = 34{,}5 || erste Null: eine Stelle nach rechts
           34{,}5 \cdot 10 = 345 || zweite Null: noch eine Stelle
           3{,}45 \cdot 100 = 345 || zusammen zwei Stellen
           :::
           """,
           typische_fehler=[(F(69, 2), "Du hast das Komma nur um eine Stelle verschoben. $100$ hat zwei Nullen, also zwei Stellen."),
                            (F(69, 20), "Nullen hinten anhängen ($3{,}4500$) ändert den Wert nicht. Das Komma muss wandern."),
                            (F(69, 2000), "Du hast das Komma nach links verschoben. Malnehmen mit $100$ macht die Zahl größer.")])

k.luecke("Welche Zahl gehört in die Lücke?",
         "0{,}07 = \\frac{\\luecke}{100}", [[7]],
         "Die $7$ steht an der zweiten Stelle nach dem Komma, also bei den Hundertsteln: $0{,}07 = \\frac{7}{100}$.",
         tipps=["An welcher Stelle nach dem Komma steht die $7$?", "Die zweite Stelle sind die Hundertstel.",
                "$7$ Hundertstel."],
         rechenweg=r"""
         :::rechnung
         0{,}07 = \frac{0}{10} + \frac{7}{100} || $0$ Zehntel, $7$ Hundertstel
         = \frac{7}{100} || zusammengefasst
         :::
         """,
         typische_fehler=[([70], "$\\frac{70}{100} = 0{,}70$. Bei $0{,}07$ steht an der Zehntelstelle eine $0$."),
                          ([F(7, 10)], "In den Zähler gehört eine ganze Zahl: Wie viele Hundertstel sind es?")])

# ── 2: Bruch <-> Dezimalzahl ───────────────────────────────────────────────
k.erklaerung("Bruch und Dezimalzahl umwandeln", r"""
    ## Von der Dezimalzahl zum Bruch

    Die Anzahl der Nachkommastellen sagt dir den [[Nenner]]: eine Stelle Zehntel,
    zwei Stellen Hundertstel, drei Stellen Tausendstel. Danach [[Kürzen|kürzt]] du.

    :::rechnung Beispiel vorgerechnet
    0{,}75 = \frac{75}{100} || zwei Nachkommastellen: Hundertstel
    = \frac{3}{4} || kürzen mit $25$
    0{,}125 = \frac{125}{1000} || drei Nachkommastellen: Tausendstel
    = \frac{1}{8} || kürzen mit $125$
    :::

    :::alt Mit Geld erklärt
    $0{,}75$ Euro sind $75$ Cent. Ein Euro hat $100$ Cent. Du hast also $75$ von
    $100$ Cent, das ist $\frac{75}{100}$ Euro. In Vierteln gedacht: Ein Viertel Euro
    sind $25$ Cent, und $75$ Cent sind drei davon, also $\frac{3}{4}$.
    :::
    ---
    ## Vom Bruch zur Dezimalzahl

    Ein Bruchstrich heißt „geteilt durch“. Oft geht es ohne schriftliches Teilen:
    [[Erweitern|Erweitere]] so, dass unten $10$, $100$ oder $1000$ steht.

    :::rechnung Beispiel vorgerechnet
    \frac{3}{8} = \frac{3 \cdot 125}{8 \cdot 125} || $8 \cdot 125 = 1000$
    = \frac{375}{1000} || drei Nullen unten: drei Nachkommastellen
    = 0{,}375 || als Dezimalzahl
    :::

    !! Das klappt genau dann, wenn der gekürzte Nenner nur die Primfaktoren $2$ und $5$ hat.

    Bei $\frac{1}{3}$ geht das nicht: Keine Zahl mal $3$ ergibt $10$, $100$ oder $1000$.

    :::alt Mit Teilen erklärt
    Stell dir vor, $3$ Pizzen werden an $8$ Leute verteilt. Jeder bekommt
    $3 : 8$ Pizzen. Rechne schriftlich: $30 : 8 = 3$ Rest $6$, dann $60 : 8 = 7$
    Rest $4$, dann $40 : 8 = 5$ Rest $0$. Fertig: $0{,}375$. Der Rest $0$ zeigt,
    dass die Division aufgeht.
    :::
    """)

k.zahl("Schreibe $0{,}35$ als vollständig gekürzten Bruch.", F(35, 100),
       "Zwei Nachkommastellen heißen Hundertstel: $\\frac{35}{100}$. Gekürzt mit $5$: $\\frac{7}{20}$.",
       gekuerzt=True, form="bruch",
       tipps=["Wie viele Nachkommastellen hat $0{,}35$?", "Zwei Stellen: Hundertstel. Also $\\frac{35}{100}$.",
              "Kürze $\\frac{35}{100}$ mit $5$."],
       rechenweg=r"""
       :::rechnung
       0{,}35 = \frac{35}{100} || zwei Nachkommastellen: Hundertstel
       = \frac{7}{20} || kürzen mit $5$
       :::
       """,
       typische_fehler=[(F(35, 1000), "Zwei Nachkommastellen sind Hundertstel, nicht Tausendstel."),
                        (F(35, 10), "$\\frac{35}{10} = 3{,}5$. Zwei Nachkommastellen bedeuten den Nenner $100$.")])

k.zahl("Schreibe $\\frac{3}{8}$ als Dezimalzahl.", F(3, 8),
       "Erweitere mit $125$: $\\frac{3}{8} = \\frac{375}{1000} = 0{,}375$.", form="dezimal",
       tipps=["Mit welcher Zahl wird $8$ zu $1000$?", "$8 \\cdot 125 = 1000$. Erweitere mit $125$.",
              "$\\frac{375}{1000}$: drei Nachkommastellen."],
       rechenweg=r"""
       :::rechnung
       \frac{3}{8} = \frac{3 \cdot 125}{8 \cdot 125} || erweitern mit $125$
       = \frac{375}{1000} || unten steht $1000$
       = 0{,}375 || drei Nachkommastellen
       :::
       """,
       typische_fehler=[(F(19, 5), "$3{,}8$ entsteht, wenn man Zähler und Nenner nebeneinanderschreibt. Der Bruchstrich heißt geteilt."),
                        (F(8, 3), "Das ist $8 : 3$. Rechne Zähler geteilt durch Nenner: $3 : 8$.")])

# ── 3: Periodische Dezimalzahlen ───────────────────────────────────────────
k.erklaerung("Periodische Dezimalzahlen", r"""
    ## Wenn die Division nie aufgeht

    Rechne $1 : 3$ schriftlich. Nach jedem Schritt bleibt der Rest $1$. Damit
    wiederholt sich alles, und die Ziffer $3$ kommt ohne Ende.

    :::rechnung Beispiel vorgerechnet
    10 = 3 \cdot 3 + 1 || Ziffer $3$, Rest $1$
    10 = 3 \cdot 3 + 1 || wieder Rest $1$: Es wiederholt sich
    \frac{1}{3} = 0{,}333\ldots = 0{,}\overline{3} || der Strich markiert die Periode
    \frac{3}{11} = 0{,}2727\ldots = 0{,}\overline{27} || hier wiederholen sich zwei Ziffern
    :::

    Eine solche Zahl heißt [[periodische Dezimalzahl]]. Jeder Bruch ist entweder
    eine endliche oder eine periodische Dezimalzahl.

    :::warum Warum `0.1 + 0.2` in Python nicht `0.3` ist
    Computer rechnen im Zweiersystem. Dort ist $\frac{1}{10}$ periodisch, so wie
    $\frac{1}{3}$ bei uns. Eine [[Gleitkommazahl]] hat nur $64$ Bit, also wird
    abgeschnitten. Darum liefert Python `0.30000000000000004`.
    :::

    :::alt Mit einer Uhr erklärt
    Beim Teilen durch $3$ gibt es nur die Reste $0$, $1$ und $2$. Taucht ein Rest
    zum zweiten Mal auf, beginnt alles von vorn, wie ein Zeiger, der wieder bei der
    gleichen Zahl ankommt. Darum muss sich jede nicht abbrechende Division irgendwann
    wiederholen.
    :::
    ---
    ## Die Periode zurück in einen Bruch

    Ein Trick: Schiebe die Periode so, dass sie sich beim Abziehen weghebt.

    :::rechnung Beispiel vorgerechnet
    x = 0{,}\overline{27} || Ziel: $x$ als Bruch
    100x = 27{,}\overline{27} || Periode hat $2$ Ziffern: mal $100$
    100x - x = 27 || abziehen: die Periode fällt weg
    99x = 27 || links zusammenfassen
    x = \frac{27}{99} || durch $99$ teilen
    x = \frac{3}{11} || kürzen mit $9$
    :::

    !! Merkregel: Periode durch so viele Neunen, wie sie Ziffern hat: $0{,}\overline{27} = \frac{27}{99}$.

    Steht vor der Periode noch eine Ziffer, wie bei $0{,}4\overline{3}$, schiebst du
    sie zuerst mit $\cdot\, 10$ vor das Komma.

    :::alt Mit Neunteln erklärt
    Merk dir eine einzige Zahl: $\frac{1}{9} = 0{,}111\ldots$ Dann ist
    $\frac{5}{9} = 0{,}555\ldots$, fünfmal so viel. Genauso ist
    $\frac{1}{99} = 0{,}0101\ldots$ und $\frac{27}{99} = 0{,}2727\ldots$ Die Neunen im
    Nenner erzeugen die Wiederholung.
    :::
    """)

k.mc("Welche Dezimalzahl ist $\\frac{2}{3}$?",
     ["$0{,}\\overline{6}$", "$0{,}6$", "$0{,}\\overline{3}$", "$0{,}\\overline{23}$"],
     "$2 : 3$: Jeder Schritt ist $20 : 3 = 6$ Rest $2$. Der Rest $2$ kehrt immer wieder, also $0{,}666\\ldots = 0{,}\\overline{6}$.",
     tipps=["Rechne $2 : 3$ schriftlich.", "$20 : 3 = 6$ Rest $2$. Welcher Rest kommt als Nächstes?",
            "Der Rest ist immer $2$: Die $6$ wiederholt sich."],
     fehler={"$0{,}6$": "$0{,}6 = \\frac{6}{10} = \\frac{3}{5}$. Bei $\\frac{2}{3}$ hört die $6$ nie auf.",
             "$0{,}\\overline{3}$": "Das ist $\\frac{1}{3}$. Für $\\frac{2}{3}$ brauchst du doppelt so viel.",
             "$0{,}\\overline{23}$": "Zähler und Nenner nebeneinander ergeben keine Dezimalzahl. Rechne $2 : 3$."})

k.zahl("Schreibe $0{,}\\overline{5}$ als vollständig gekürzten Bruch.", F(5, 9),
       "Eine Ziffer in der Periode: durch eine Neun teilen. $0{,}\\overline{5} = \\frac{5}{9}$.",
       gekuerzt=True, form="bruch",
       tipps=["Wie viele Ziffern hat die Periode?", "Eine Ziffer: mal $10$, dann $x$ abziehen.",
              "$10x - x = 5$, also $9x = 5$."],
       rechenweg=r"""
       :::rechnung
       x = 0{,}\overline{5} || Ziel: $x$ als Bruch
       10x = 5{,}\overline{5} || eine Ziffer Periode: mal $10$
       10x - x = 5 || abziehen: Periode fällt weg
       9x = 5 || zusammenfassen
       x = \frac{5}{9} || durch $9$ teilen
       :::
       """,
       typische_fehler=[(F(1, 2), "$\\frac{1}{2} = 0{,}5$ hört nach einer Stelle auf. Bei $0{,}\\overline{5}$ geht die $5$ ewig weiter."),
                        (F(5, 99), "Die Periode hat nur eine Ziffer. Also eine Neun im Nenner, nicht zwei.")])

# ── 4: Runden ──────────────────────────────────────────────────────────────
k.erklaerung("Runden", r"""
    ## Auf eine Stelle runden

    :::analogie 🚌 Haltestellen
    Du stehst zwischen zwei Haltestellen und gehst zur näheren. Beim [[Runden]]
    sind die Haltestellen die Zahlen mit weniger Stellen.
    :::

    So gehst du vor:

    1. Markiere die Stelle, auf die gerundet wird.
    2. Schau nur auf die Ziffer **direkt dahinter**.
    3. Bei $0$ bis $4$ abrunden, bei $5$ bis $9$ aufrunden.

    :::visual zahlenstrahl
    {"von": 2.3, "bis": 2.4, "schritt": 0.01, "punkte": [{"x": "2,37", "label": "2{,}37", "farbe": "orange"}, {"x": "2,35", "label": "2{,}35"}],
     "unterschrift": "$2{,}37$ liegt näher an $2{,}4$ als an $2{,}3$. Die Mitte ist $2{,}35$."}
    :::

    :::rechnung Beispiel vorgerechnet
    2{,}37 \approx 2{,}4 || auf Zehntel: dahinter steht $7$, aufrunden
    2{,}346 \approx 2{,}3 || auf Zehntel: dahinter steht $4$, abrunden
    2{,}346 \approx 2{,}35 || auf Hundertstel: dahinter steht $6$, aufrunden
    :::

    :::achtung Nicht in mehreren Schritten runden
    $2{,}346 \to 2{,}35 \to 2{,}4$ ist falsch. Entscheidend ist nur die Ziffer direkt
    hinter der Rundungsstelle, hier die $4$. Richtig ist $2{,}3$.
    :::

    :::alt Mit dem Preisschild erklärt
    Ein Laden schreibt „ca. $2$ Euro“ an etwas, das $1{,}89$ Euro kostet. Für die
    ungefähre Angabe zählen nur die vollen Euro und die Ziffer danach: $1{,}8\ldots$
    liegt näher an $2$ als an $1$. Die $9$ ganz hinten spielt dafür keine Rolle mehr.
    :::
    """)

k.zahl("Runde $2{,}346$ auf eine Nachkommastelle.", F(23, 10),
       "Hinter der ersten Nachkommastelle steht $4$. Also abrunden: $2{,}3$.", form="dezimal",
       tipps=["Welche Ziffer steht direkt hinter der ersten Nachkommastelle?", "Es ist die $4$.",
              "$4$ heißt abrunden."],
       rechenweg=r"""
       :::rechnung
       2{,}346 \approx 2{,}3 || Ziffer hinter den Zehnteln ist $4$: abrunden
       :::
       """,
       typische_fehler=[(F(12, 5), "Du hast in zwei Schritten gerundet ($2{,}35 \\to 2{,}4$). Nur die Ziffer direkt hinter der Stelle zählt: $4$."),
                        (F(47, 20), "Das ist auf zwei Nachkommastellen gerundet. Gefragt ist eine.")])

k.wf("$3{,}96$ auf eine Nachkommastelle gerundet ergibt $4{,}0$.", True,
     "Hinter der $9$ steht $6$: aufrunden. Aus $3{,}9$ wird $4{,}0$. Die Null hinten zeigt, dass auf Zehntel genau gerundet wurde.",
     tipps=["Aufrunden von $3{,}9$ um ein Zehntel ergibt …?"])

# ── 5: Prozent ─────────────────────────────────────────────────────────────
k.erklaerung("Prozent", r"""
    ## Prozent heißt Hundertstel

    :::analogie 🏟️ Hundert Plätze
    Stell dir eine Halle mit genau $100$ Plätzen vor. $15\,\%$ heißt: $15$ von
    diesen $100$ Plätzen.
    :::

    [[Prozent]] ist nur eine andere Schreibweise: $1\,\% = \frac{1}{100} = 0{,}01$.
    Von wie viel du ausgehst, heißt [[Grundwert]] $G$. Der Anteil davon ist der
    [[Prozentwert]] $W$. Der [[Prozentsatz]] $p$ sagt, wie viel Prozent es sind.

    !! Prozentwert = Prozentsatz als Dezimalzahl mal Grundwert: $W = p \cdot G$.

    :::rechnung Beispiel vorgerechnet: 15 % von 80
    \frac{15}{100} \cdot 80 = 0{,}15 \cdot 80 || $15\,\%$ sind $15$ Hundertstel
    = 12 || ausrechnen
    :::

    :::alt Mit dem Dreisatz erklärt
    $100\,\%$ sind $80$. Dann ist $1\,\%$ hundertmal weniger: $80 : 100 = 0{,}8$.
    $15\,\%$ sind fünfzehnmal so viel wie $1\,\%$: $15 \cdot 0{,}8 = 12$. Du gehst
    also über das eine Prozent.
    :::
    ---
    ## Prozentsatz und Grundwert gesucht

    Aus $W = p \cdot G$ folgen die beiden anderen Formeln:

    | Gesucht | Formel |
    |---|---|
    | Prozentsatz | $p = W : G$ |
    | Grundwert | $G = W : p$ |

    :::rechnung Beispiel vorgerechnet
    12 : 48 = 0{,}25 || $12$ von $48$: Anteil ausrechnen
    0{,}25 = \frac{25}{100} || also $25\,\%$
    30 : 0{,}2 = 150 || $30$ sind $20\,\%$: Grundwert
    :::

    :::achtung Prozentsatz nicht in Dezimalzahl umgewandelt
    $W : 20 = 30 : 20 = 1{,}5$ ist falsch. Teile durch $0{,}2$, nicht durch $20$.
    :::

    :::alt Mit Probe erklärt
    Du weißt nicht, welche Formel? Dann prüf mit der Hauptformel nach.
    $20\,\%$ von $150$ sind $0{,}2 \cdot 150 = 30$. Passt. So kannst du jedes Ergebnis
    in der Prozentrechnung selbst kontrollieren.
    :::
    ---
    ## Prozentuale Änderung

    Steigt etwas um $20\,\%$, hast du $100\,\% + 20\,\% = 120\,\%$. Du nimmst mal $1{,}2$.
    Sinkt es um $20\,\%$, bleiben $80\,\%$: mal $0{,}8$.

    :::rechnung Beispiel vorgerechnet
    50 \cdot 1{,}2 = 60 || plus $20\,\%$
    60 \cdot 0{,}8 = 48 || danach minus $20\,\%$
    1{,}2 \cdot 0{,}8 = 0{,}96 || zusammen: nur $96\,\%$ vom Start
    :::

    :::achtung Plus und minus gleich viel Prozent heben sich nicht auf
    Die zweite Änderung rechnet mit dem neuen Grundwert $60$, nicht mit $50$.
    :::

    :::warum Laufzeiten
    Ein Algorithmus wird zweimal um $10\,\%$ schneller. Seine Laufzeit sinkt auf
    $0{,}9 \cdot 0{,}9 = 0{,}81$, also um $19\,\%$, nicht um $20\,\%$.
    :::

    :::alt Mit dem Laden erklärt
    Ein Shirt kostet $50$ Euro. Der Preis steigt um $10$ Euro auf $60$ Euro. Im
    Ausverkauf gibt es $20\,\%$ Rabatt auf $60$ Euro, das sind $12$ Euro. Du sparst
    mehr, als vorher aufgeschlagen wurde, und zahlst $48$ Euro.
    :::
    """)

k.berechne("15/100*80", frage="Wie viel sind $15\\,\\%$ von $80$?",
           erklaerung="$15\\,\\% = 0{,}15$. Also $0{,}15 \\cdot 80 = 12$.",
           tipps=["Schreibe $15\\,\\%$ als Dezimalzahl.", "$15\\,\\% = 0{,}15$.", "Rechne $0{,}15 \\cdot 80$."],
           rechenweg=r"""
           :::rechnung
           \frac{15}{100} \cdot 80 = 0{,}15 \cdot 80 || Prozent heißt Hundertstel
           = 12 || ausrechnen
           :::
           """,
           typische_fehler=[(1200, "Du hast $15 \\cdot 80$ gerechnet. $15\\,\\%$ sind aber nur $0{,}15$."),
                            (F(16, 3), "Du hast $80 : 15$ gerechnet. Prozentwert heißt: Prozentsatz **mal** Grundwert.")])

k.zahl("In einer Gruppe sind $48$ Personen, $12$ davon programmieren in Python. Wie viel Prozent sind das?",
       F(12, 48) * 100, "Anteil $12 : 48 = 0{,}25$, also $25\\,\\%$.", einheit="%",
       tipps=["Gesucht ist der Prozentsatz: $p = W : G$.", "Rechne $12 : 48$.",
              "$0{,}25$ sind $25$ Hundertstel."],
       rechenweg=r"""
       :::rechnung
       12 : 48 = 0{,}25 || Anteil $W : G$
       0{,}25 = \frac{25}{100} || $25$ Hundertstel, also $25\,\%$
       :::
       """,
       typische_fehler=[(F(1, 4), "Das ist der Anteil als Dezimalzahl. In Prozent: mal $100$, also $25\\,\\%$."),
                        (400, "Du hast $48 : 12$ gerechnet. Teile den Teil durch das Ganze: $12 : 48$.")])

k.zahl("$30$ Euro sind $20\\,\\%$ eines Preises. Wie hoch ist der ganze Preis?", F(30) / F(20, 100),
       "Gesucht ist der Grundwert: $G = W : p = 30 : 0{,}2 = 150$ Euro.", einheit="€",
       tipps=["Gesucht ist der Grundwert $G$.", "$G = W : p$ mit $p = 0{,}2$.", "$30 : 0{,}2$"],
       rechenweg=r"""
       :::rechnung
       30 : 0{,}2 = 150 || Grundwert $G = W : p$
       0{,}2 \cdot 150 = 30 || Probe
       :::
       """,
       typische_fehler=[(6, "Du hast $20\\,\\%$ von $30$ berechnet. Gesucht ist das Ganze, von dem $30$ ein Teil ist."),
                        (F(3, 2), "Du hast durch $20$ statt durch $0{,}2$ geteilt.")])

k.zahl("Ein Spiel kostet $50$ Euro. Der Preis steigt um $20\\,\\%$, danach sinkt er um $20\\,\\%$. Was kostet es jetzt?",
       F(50) * F(12, 10) * F(8, 10),
       "$50 \\cdot 1{,}2 = 60$, dann $60 \\cdot 0{,}8 = 48$ Euro. Die $20\\,\\%$ Rabatt beziehen sich auf $60$ Euro.",
       einheit="€",
       tipps=["Rechne die Schritte nacheinander.", "Erst $50 \\cdot 1{,}2$.", "Dann das Ergebnis mal $0{,}8$."],
       rechenweg=r"""
       :::rechnung
       50 \cdot 1{,}2 = 60 || plus $20\,\%$
       60 \cdot 0{,}8 = 48 || minus $20\,\%$ vom neuen Preis
       :::
       """,
       typische_fehler=[(50, "Plus $20\\,\\%$ und minus $20\\,\\%$ heben sich nicht auf: Der zweite Schritt rechnet mit $60$."),
                        (60, "Du hast nur den ersten Schritt gerechnet.")])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


def _zehnerexponent(n):
    """Kleinstes k mit n | 10^k (n hat nur Primfaktoren 2 und 5)."""
    for kk in range(0, 8):
        if (10 ** kk) % n == 0:
            return kk
    raise ValueError(n)


def bruch_in_dezimal(rng):
    while True:
        n = rng.choice([2, 4, 5, 8, 10, 16, 20, 25, 40, 50])
        z = rng.randint(1, 2 * n)
        if math.gcd(z, n) == 1:
            break
    w = F(z, n)
    kk = _zehnerexponent(n)
    e = 10 ** kk // n
    zeilen = []
    if e > 1:
        zeilen.append((f"\\frac{{{z}}}{{{n}}} = \\frac{{{z} \\cdot {e}}}{{{n} \\cdot {e}}}",
                       f"erweitern mit ${e}$, denn ${n} \\cdot {e} = {10 ** kk}$"))
        zeilen.append((f"= \\frac{{{z * e}}}{{{10 ** kk}}}", "ausrechnen"))
    else:
        zeilen.append((f"\\frac{{{z}}}{{{n}}} = \\frac{{{z * e}}}{{{10 ** kk}}}", "der Nenner ist schon eine Zehnerzahl"))
    zeilen.append((f"= {dz(w)}", f"${kk}$ Null{'en' if kk > 1 else ''} im Nenner: ${kk}$ Nachkommastelle{'n' if kk > 1 else ''}"))
    nebeneinander = F(f"{z}.{n}")
    fehler = [(nebeneinander, "Zähler und Nenner nebeneinander ergeben nicht den Wert. Der Bruchstrich heißt geteilt."),
              (F(n, z), "Das ist der Kehrwert. Rechne Zähler geteilt durch Nenner.")]
    return {
        "frage": f"Schreibe $\\frac{{{z}}}{{{n}}}$ als Dezimalzahl.",
        "loesung": w, "form": "dezimal",
        "tipps": [f"Erweitere so, dass im Nenner $10$, $100$, $1000$ … steht.",
                  f"${n} \\cdot {e} = {10 ** kk}$.",
                  f"$\\frac{{{z * e}}}{{{10 ** kk}}}$ hat ${kk}$ Nachkommastelle{'n' if kk > 1 else ''}."],
        "rechenweg": _zeilen(*zeilen),
        "erklaerung": "Auf einen Zehnernenner erweitern, dann die Nachkommastellen abzählen.",
        "typische_fehler": ohne_gleiche(w, fehler),
    }


_STELLEN_TEXT = {0: "auf ganze Zahlen", 1: "auf eine Nachkommastelle", 2: "auf zwei Nachkommastellen"}
_STELLEN_NAME = {0: "Einer", 1: "Zehntel", 2: "Hundertstel"}


def _runde(x, s):
    q = x * 10 ** s
    return F(math.floor(q + F(1, 2)), 10 ** s)


def runden(rng):
    s = rng.choice([0, 1, 1, 2, 2])
    while True:
        ganz = rng.randint(0, 99)
        stellen = s + 2
        ziffern = [rng.randint(0, 9) for _ in range(stellen)]
        if rng.random() < 0.35:                   # Falle fürs Kettenrunden: …4 gefolgt von ≥ 5
            ziffern[s] = 4
            ziffern[s + 1] = rng.randint(5, 9)
        if ziffern[-1] == 0:
            ziffern[-1] = rng.randint(1, 9)
        x = ganz + sum(F(d, 10 ** (i + 1)) for i, d in enumerate(ziffern))
        w = _runde(x, s)
        if w != 0:
            break
    entscheid = ziffern[s]
    richtung = "aufrunden" if entscheid >= 5 else "abrunden"
    fehler = [(F(math.floor(x * 10 ** s), 10 ** s), "Du hast nur abgeschnitten. Prüfe die Ziffer dahinter: "
               + ("Sie ist $5$ oder größer, also aufrunden." if entscheid >= 5 else "abrunden.")),
              (_runde(_runde(x, s + 1), s), f"Du hast in zwei Schritten gerundet. Nur die Ziffer direkt hinter der Rundungsstelle zählt: ${entscheid}$."),
              (_runde(x, s + 1), "Du hast eine Stelle zu genau gerundet.")]
    return {
        "frage": f"Runde ${dz(x)}$ {_STELLEN_TEXT[s]}.",
        "loesung": w, "form": "dezimal",
        "tipps": [f"Die Rundungsstelle sind die {_STELLEN_NAME[s]}.",
                  f"Die Ziffer direkt dahinter ist ${entscheid}$.",
                  f"${entscheid}$ heißt {richtung}."],
        "rechenweg": _zeilen((f"{dz(x)} \\approx {dz(w)}", f"Ziffer hinter den {_STELLEN_NAME[s]}n ist ${entscheid}$: {richtung}")),
        "erklaerung": "Nur die Ziffer direkt hinter der Rundungsstelle entscheidet: $0$ bis $4$ ab, $5$ bis $9$ auf.",
        "typische_fehler": ohne_gleiche(w, fehler),
    }


def prozent_rechnen(rng):
    art = rng.choice(["W", "W", "p", "G"])
    while True:
        g = rng.choice([40, 60, 80, 120, 150, 200, 240, 250, 300, 400, 500, 800])
        p = rng.choice([5, 10, 12, 15, 20, 25, 30, 35, 40, 60, 75])
        w = F(g * p, 100)
        if w.denominator == 1 or (art == "W" and w.denominator <= 10):
            break
    pd = F(p, 100)
    if art == "W":
        frage = rng.choice([f"Wie viel sind ${p}\\,\\%$ von ${g}$?",
                            f"Ein Gerät kostet ${g}$ Euro. Es gibt ${p}\\,\\%$ Rabatt. Wie viel Euro sparst du?",
                            f"Eine Festplatte hat ${g}$ GB. ${p}\\,\\%$ davon sind belegt. Wie viele GB sind belegt?"])
        loes, einheit = w, None
        weg = _zeilen((f"{dz(pd)} \\cdot {g} = {dz(w)}", f"${p}\\,\\% = {dz(pd)}$, Prozentwert $W = p \\cdot G$"))
        tipps = [f"Schreibe ${p}\\,\\%$ als Dezimalzahl.", f"${p}\\,\\% = {dz(pd)}$.", f"Rechne ${dz(pd)} \\cdot {g}$."]
        fehler = [(g * p, f"Du hast ${p} \\cdot {g}$ gerechnet. ${p}\\,\\%$ sind aber ${dz(pd)}$."),
                  (F(g, p), "Du hast geteilt. Prozentwert heißt: Prozentsatz **mal** Grundwert."),
                  (g - w, "Das ist der Rest nach Abzug. Gefragt ist der Anteil selbst.")]
    elif art == "p":
        frage = rng.choice([f"Wie viel Prozent sind ${dz(w)}$ von ${g}$?",
                            f"Von ${g}$ Tests schlagen ${dz(w)}$ fehl. Wie viel Prozent sind das?"])
        loes, einheit = F(p), "%"
        weg = _zeilen((f"{dz(w)} : {g} = {dz(pd)}", "Anteil $W : G$"),
                      (f"{dz(pd)} = \\frac{{{p}}}{{100}}", f"also ${p}\\,\\%$"))
        tipps = ["Gesucht ist der Prozentsatz: $p = W : G$.", f"Rechne ${dz(w)} : {g}$.",
                 f"${dz(pd)}$ sind ${p}$ Hundertstel."]
        fehler = [(pd, f"Das ist der Anteil als Dezimalzahl. In Prozent: mal $100$."),
                  (F(g, w) * 100, f"Du hast ${g} : {dz(w)}$ gerechnet. Teile den Teil durch das Ganze.")]
    else:
        frage = rng.choice([f"${dz(w)}$ sind ${p}\\,\\%$ des Grundwerts. Wie groß ist der Grundwert?",
                            f"Ein Download hat ${dz(w)}$ MB geladen. Das sind ${p}\\,\\%$ der Datei. Wie groß ist die Datei in MB?"])
        loes, einheit = F(g), None
        weg = _zeilen((f"{dz(w)} : {dz(pd)} = {g}", f"Grundwert $G = W : p$ mit $p = {dz(pd)}$"),
                      (f"{dz(pd)} \\cdot {g} = {dz(w)}", "Probe"))
        tipps = ["Gesucht ist das Ganze, der Grundwert $G$.", f"$G = W : p$ mit $p = {dz(pd)}$.",
                 f"Rechne ${dz(w)} : {dz(pd)}$."]
        fehler = [(w * pd, f"Du hast ${p}\\,\\%$ von ${dz(w)}$ berechnet. ${dz(w)}$ ist schon der Teil."),
                  (F(w) / p, f"Du hast durch ${p}$ statt durch ${dz(pd)}$ geteilt.")]
    d = {
        "frage": frage, "loesung": loes,
        "tipps": tipps, "rechenweg": weg,
        "erklaerung": "Hauptformel $W = p \\cdot G$ mit $p$ als Dezimalzahl. Daraus $p = W : G$ und $G = W : p$.",
        "typische_fehler": ohne_gleiche(loes, fehler),
    }
    if einheit:
        d["einheit"] = einheit
    return d


def periode_in_bruch(rng):
    if rng.random() < 0.4:
        per = str(rng.randint(1, 8))
    else:
        while True:
            a = rng.randint(1, 98)
            per = f"{a:02d}"
            if per[0] != per[1]:
                break
    lang = len(per)
    neunen = 10 ** lang - 1
    zahl = int(per)
    w = F(zahl, neunen)
    faktor = 10 ** lang
    zeilen = [(f"x = 0{{,}}\\overline{{{per}}}", "Ziel: $x$ als Bruch"),
              (f"{faktor}x = {zahl}{{,}}\\overline{{{per}}}", f"Periode hat ${lang}$ Ziffer{'n' if lang > 1 else ''}: mal ${faktor}$"),
              (f"{faktor}x - x = {zahl}", "abziehen: die Periode fällt weg"),
              (f"{neunen}x = {zahl}", "zusammenfassen"),
              (f"x = \\frac{{{zahl}}}{{{neunen}}}", f"durch ${neunen}$ teilen")]
    if w.denominator != neunen:
        zeilen.append((f"x = {tex(w)}", f"kürzen mit ${neunen // w.denominator}$"))
    fehler = [(F(zahl, faktor), f"Das wäre $0{{,}}{per}$ ohne Periode. Die Ziffern wiederholen sich aber ewig."),
              (F(zahl, 10 ** (3 - lang) - 1 if lang == 1 else 9), "Zähle die Ziffern der Periode: so viele Neunen braucht der Nenner.")]
    return {
        "frage": f"Schreibe $0{{,}}\\overline{{{per}}}$ als vollständig gekürzten Bruch.",
        "loesung": w, "gekuerzt": True, "form": "bruch",
        "tipps": ["Wie viele Ziffern hat die Periode?",
                  f"Multipliziere $x = 0{{,}}\\overline{{{per}}}$ mit ${faktor}$ und ziehe $x$ ab.",
                  f"${neunen}x = {zahl}$. Teile und kürze."],
        "rechenweg": _zeilen(*zeilen),
        "erklaerung": "Periode durch so viele Neunen, wie sie Ziffern hat. Danach kürzen.",
        "typische_fehler": ohne_gleiche(w, fehler),
    }


k.praxis()

k.generator(bruch_in_dezimal, typ="zahl", titel="Bruch in Dezimalzahl", glatt=True)
k.generator(runden, typ="zahl", titel="Runden", glatt=True)
k.generator(prozent_rechnen, typ="zahl", titel="Prozentrechnung", glatt=True)
k.generator(periode_in_bruch, typ="zahl", titel="Periode in Bruch", glatt=True)

# Übungsblatt-Stil: gemischt periodische Zahl
_x = F(13, 30)
k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: gemischt periodische Dezimalzahl

    Stellen Sie $x = 0{,}4\overline{3}$ als vollständig gekürzten Bruch dar.
    Geben Sie alle Zwischenschritte an.
    """,
    [{"typ": "zahl", "frage": "Mit welcher Zahl nimmst du $x$ zuerst mal, damit die $4$ vor dem Komma steht?",
      "loesung": 10,
      "tipps": ["Die $4$ steht eine Stelle hinter dem Komma.", "Eine Stelle nach rechts: mal $10$."],
      "rechenweg": "$10x = 4{,}\\overline{3}$: Jetzt beginnt die Periode direkt hinter dem Komma.",
      "typische_fehler": [(100, "Mit $100$ landet auch die erste $3$ vor dem Komma. Erst nur die Vorziffer verschieben.")]},
     {"typ": "zahl", "frage": "Es ist $100x = 43{,}\\overline{3}$ und $10x = 4{,}\\overline{3}$. "
                              "Ziehe ab: $90x = \\;?$",
      "loesung": 43 - 4,
      "tipps": ["Die Periode $0{,}\\overline{3}$ fällt beim Abziehen weg.", "$43 - 4$"],
      "rechenweg": "$100x - 10x = 43{,}\\overline{3} - 4{,}\\overline{3} = 39$",
      "typische_fehler": [(47, "Abziehen, nicht addieren: $43 - 4$.")]},
     {"typ": "zahl", "frage": "Gib $x$ als vollständig gekürzten Bruch an.", "loesung": _x, "gekuerzt": True, "form": "bruch",
      "tipps": ["$x = \\frac{39}{90}$.", "Kürze mit $3$."],
      "rechenweg": "$x = \\frac{39}{90} = \\frac{13}{30}$",
      "typische_fehler": [(F(43, 99), "Das wäre $0{,}\\overline{43}$. Hier wiederholt sich nur die $3$.")]},
     {"typ": "zahl", "frage": "Probe: Berechne $13 : 30$ und runde auf vier Nachkommastellen.",
      "loesung": _runde(_x, 4), "form": "dezimal",
      "tipps": ["$13 : 30 = 0{,}4333\\ldots$", "Hinter der vierten Stelle steht eine $3$: abrunden."],
      "rechenweg": "$13 : 30 = 0{,}43333\\ldots \\approx 0{,}4333$",
      "typische_fehler": [(F(4334, 10000), "Hinter der vierten Stelle steht $3$: abrunden, nicht aufrunden.")]}],
    "Vorziffer mit $\\cdot\\, 10$ vor das Komma schieben, dann wie bei einer reinen Periode abziehen.",
    uebungsblatt=True,
    tipps=["Erst die Vorziffer vor das Komma schieben.", "Dann zwei Gleichungen mit gleicher Periode abziehen."],
    rechenweg=r"""
    :::rechnung
    10x = 4{,}\overline{3} || Vorziffer vor das Komma
    100x = 43{,}\overline{3} || eine Periodenziffer weiter
    100x - 10x = 39 || abziehen: Periode fällt weg
    90x = 39 || zusammenfassen
    x = \frac{39}{90} || durch $90$ teilen
    x = \frac{13}{30} || kürzen mit $3$
    :::
    """)

k.papier(r"""
    ## Erklären wie in der Übung

    Begründe auf Papier: $0{,}\overline{9} = 1$.

    Gib zwei verschiedene Begründungen an.
    """,
    r"""
    **Begründung 1 (Drittel):** $\frac{1}{3} = 0{,}\overline{3}$. Mal $3$ genommen:
    $3 \cdot \frac{1}{3} = 1$ und $3 \cdot 0{,}\overline{3} = 0{,}\overline{9}$. Also ist
    $0{,}\overline{9} = 1$.

    **Begründung 2 (Trick mit $x$):** Setze $x = 0{,}\overline{9}$. Dann ist
    $10x = 9{,}\overline{9}$. Abziehen ergibt $9x = 9$, also $x = 1$.

    **Begründung 3 (kein Platz dazwischen):** Wären $0{,}\overline{9}$ und $1$ verschieden,
    müsste eine Zahl dazwischen liegen. Jede Zahl unter $1$ hat aber irgendwo eine
    Stelle kleiner als $9$, ist also kleiner als $0{,}\overline{9}$.
    """,
    ["Ich habe eine Begründung mit $\\frac{1}{3} = 0{,}\\overline{3}$ oder der Merkregel $\\frac{9}{9}$ angegeben",
     "Ich habe den Trick $10x - x$ sauber aufgeschrieben",
     "Ich habe verstanden, dass $0{,}\\overline{9}$ und $1$ zwei Schreibweisen derselben Zahl sind"],
    "Eine Zahl kann mehrere Dezimaldarstellungen haben. $0{,}\\overline{9}$ und $1$ sind dieselbe Zahl.",
    tipps=["Was ergibt $3 \\cdot 0{,}\\overline{3}$?"])

k.zusammenfassung(r"""
    ## Dezimalzahlen und Prozent

    | Was | Regel | Beispiel |
    |---|---|---|
    | Stellenwerte | Zehntel, Hundertstel, Tausendstel | $3{,}45 = 3 + \frac{4}{10} + \frac{5}{100}$ |
    | mal/durch $10^k$ | Komma $k$ Stellen verschieben | $3{,}45 \cdot 100 = 345$ |
    | Dezimal → Bruch | Nachkommastellen = Nullen im Nenner, dann kürzen | $0{,}75 = \frac{75}{100} = \frac{3}{4}$ |
    | Bruch → Dezimal | auf $10$, $100$, $1000$ erweitern oder teilen | $\frac{3}{8} = \frac{375}{1000} = 0{,}375$ |
    | Periode → Bruch | Periode durch gleich viele Neunen | $0{,}\overline{27} = \frac{27}{99} = \frac{3}{11}$ |
    | Runden | nur die Ziffer direkt dahinter: $0$–$4$ ab, $5$–$9$ auf | $2{,}346 \approx 2{,}3$ |
    | Prozentwert | $W = p \cdot G$ | $15\,\%$ von $80$: $0{,}15 \cdot 80 = 12$ |
    | Prozentsatz, Grundwert | $p = W : G$, $G = W : p$ | $12 : 48 = 25\,\%$ |
    | Änderung | $+p$: mal $(1 + p)$, $-p$: mal $(1 - p)$ | $+20\,\%$: mal $1{,}2$ |

    !! $+20\,\%$ und danach $-20\,\%$ ergibt $1{,}2 \cdot 0{,}8 = 0{,}96$, also $4\,\%$ weniger als vorher.

    - Mehr Ziffern heißt nicht größer: $0{,}5 > 0{,}45$.
    - Nie in mehreren Schritten runden.
    - $0{,}\overline{9} = 1$.
""")
