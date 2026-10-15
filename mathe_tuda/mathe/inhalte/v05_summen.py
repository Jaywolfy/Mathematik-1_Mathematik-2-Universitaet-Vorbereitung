# -*- coding: utf-8 -*-
"""Vorkurs 5: Summen- und Produktzeichen – Σ, Π, leere Summe, Rechenregeln, Indexverschiebung."""
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

tk = mathlib.tex_klammer


def _S(f, a, b):
    """Summe f(a) + … + f(b), leer = 0 (exakt)."""
    return sum((F(f(k)) for k in range(a, b + 1)), F(0))


def _P(f, a, b):
    """Produkt f(a) · … · f(b), leer = 1 (exakt)."""
    p = F(1)
    for k in range(a, b + 1):
        p *= F(f(k))
    return p


# Alle Zahlen, die in den Erklärungen stehen, rechnet Python hier nach.
assert _S(lambda k: 2 * k, 1, 3) == 12
assert _S(lambda j: j, -1, 1) == 0
assert _S(lambda k: 2 * k - 1, 1, 5) == 1 + 3 + 5 + 7 + 9 == 25
assert _S(lambda k: k * k, 1, 4) == 30
assert _P(lambda k: k * k, 1, 3) == 36
assert _P(lambda j: 2 * j + 1, -2, 0) == 3
assert _S(lambda k: k, 5, 4) == 0 and _P(lambda k: k, 1, 0) == 1
assert _S(lambda k: 3 * k, 1, 4) == 3 * _S(lambda k: k, 1, 4) == 30
assert _P(lambda k: 2 * k, 1, 3) == 2 ** 3 * _P(lambda k: k, 1, 3) == 48
assert _S(lambda k: k, 1, 3) == _S(lambda k: k - 5, 6, 8) == 6
assert _P(lambda k: k * k, 3, 5) == _P(lambda k: (k + 5) ** 2, -2, 0) == 3600
assert _S(lambda k: 2 * k + 1, -3, 4) == _S(lambda k: 2 * k - 7, 1, 8) == 16
assert _S(lambda k: 2 * k + 9, 1, 8) != 16 and _S(lambda k: 2 * k + 5, 1, 8) != 16 and _S(lambda k: 2 * k - 3, 1, 8) != 16
assert _P(lambda k: F(k * k, 2), 1, 4) == 36
for _n in range(0, 40):
    assert _S(lambda k: k * k, 1, _n + 1) == _S(lambda k: k * k, 1, _n) + (_n + 1) ** 2
    assert _S(lambda k: (k + 1) ** 2 - k ** 2, 1, _n) == (_n + 1) ** 2 - 1
    assert _S(lambda k: 2 * k + 1, 1, _n) == _n * _n + 2 * _n
    assert _S(lambda k: k, 1, _n) == F(_n * (_n + 1), 2)
    assert _S(lambda k: (k - 2) ** 2, 3, 7) == _S(lambda k: k * k, 1, 5) == 55
    for _a in range(-3, 4):
        assert _P(lambda k: 3 * k + 1, _a, _a + _n % 5) == 3 ** (_n % 5 + 1) * _P(lambda k: k + F(1, 3), _a, _a + _n % 5)

k = neues_kapitel(
    slug="summen",
    titel="Summen- und Produktzeichen",
    beschreibung="Lange Summen und Produkte kurz schreiben: Σ, Π, leere Summe, Rechenregeln und Indexverschiebung",
    teil="vorkurs",
    quelle="MVK 2026, VL 2",
    icon="∑")

k.lernziele([
    "Ich kann Summen mit $\\sum$ und Produkte mit $\\prod$ lesen, ausschreiben und ausrechnen",
    "Ich kann eine Summe mit Pünktchen in die Schreibweise mit $\\sum$ übersetzen",
    "Ich weiß, warum die leere Summe $0$ und das leere Produkt $1$ ist",
    "Ich kann konstante Faktoren aus Summen und Produkten herausziehen",
    "Ich kann eine Indexverschiebung durchführen und den letzten Summanden abspalten",
])

k.warum(r"""
Das Summenzeichen ist eine `for`-Schleife auf Papier. `s = 0` und dann
`for k in range(1, n + 1): s += a(k)` berechnet genau $\sum_{k=1}^{n} a_k$.
Laufzeiten von Algorithmen werden als Summen ausgerechnet: Zwei verschachtelte
Schleifen über $n$ Elemente kosten $\sum_{i=1}^{n} \sum_{j=1}^{n} 1 = n^2$ Schritte.
Im Vorkurs der TU braucht ihr das Summenzeichen ab der dritten Vorlesung für
Induktionsbeweise, in Mathe 1 für Reihen und Matrizen.
""")

# ── 1: Summenzeichen ───────────────────────────────────────────────────────
k.erklaerung("Das Summenzeichen", r"""
    ## Eine Schleife auf Papier

    :::analogie 🧾 Kassenzettel
    Die Kasse geht Zeile für Zeile durch und addiert jeden Preis. Das
    [[Summenzeichen]] $\sum$ macht dasselbe mit Zahlen.
    :::

    So liest du $\displaystyle\sum_{k=1}^{3} 2k$:

    - Unten steht der [[Laufindex]] $k$ und wo er startet: bei $1$ (untere Grenze).
    - Oben steht, wo er aufhört: bei $3$ (obere Grenze).
    - Rechts steht der Summand $2k$. Setze jeden Wert von $k$ ein und addiere.

    $$\sum_{k=n}^{N} a_k := a_n + a_{n+1} + \ldots + a_{N-1} + a_N$$

    :::rechnung Beispiel vorgerechnet
    \sum_{k=1}^{3} 2k = 2 \cdot 1 + 2 \cdot 2 + 2 \cdot 3 || $k = 1, 2, 3$ nacheinander einsetzen
    2 \cdot 1 + 2 \cdot 2 + 2 \cdot 3 = 2 + 4 + 6 || jeden Summanden ausrechnen
    = 12 || addieren
    :::

    :::alt Als Programm erklärt
    Stell dir einen Zähler vor, der bei $1$ losläuft und bei $3$ stehen bleibt.
    Bei jedem Halt rechnet er $2 \cdot k$ aus und wirft das Ergebnis in einen Topf.
    Am Ende schaust du in den Topf: $2 + 4 + 6 = 12$. In Python:
    `sum(2 * k for k in range(1, 4))`. Achtung: `range` hört **vor** der $4$ auf.
    :::
    ---
    ## Der Laufindex ist nur ein Platzhalter

    Der Laufindex darf auch $i$ oder $j$ heißen, das Ergebnis bleibt gleich.
    Die Grenzen dürfen negativ sein. Gezählt wird immer in Einerschritten.

    :::rechnung Beispiel vorgerechnet
    \sum_{j=-1}^{1} j = (-1) + 0 + 1 || $j = -1, 0, 1$ einsetzen
    (-1) + 0 + 1 = 0 || addieren
    :::

    Von $n$ bis $N$ sind es $N - n + 1$ Summanden: von $3$ bis $7$ also
    $7 - 3 + 1 = 5$ Stück ($3, 4, 5, 6, 7$).

    :::achtung Ein Summand zu wenig
    Viele rechnen $N - n$ und vergessen das $+1$. Zähle im Zweifel mit den
    Fingern nach. Und in Python zählt `range(n, N)` nur bis $N - 1$.
    :::

    :::alt Mit Zaunpfählen erklärt
    Ein Zaun von Meter $3$ bis Meter $7$ hat Pfähle bei $3, 4, 5, 6, 7$:
    fünf Pfähle, aber nur vier Lücken dazwischen. Die Summanden sind die Pfähle.
    Deshalb kommt zu $7 - 3$ noch die $1$ dazu.
    :::
    """)

k.zahl("Berechne $\\displaystyle\\sum_{k=1}^{4} k$.", _S(lambda i: i, 1, 4),
       "$\\sum_{k=1}^{4} k = 1 + 2 + 3 + 4 = 10$.",
       tipps=["Setze $k = 1, 2, 3, 4$ nacheinander ein.", "Die Summanden sind einfach $1$, $2$, $3$ und $4$.",
              "$1 + 2 + 3 + 4$"],
       rechenweg=r"""
       :::rechnung
       \sum_{k=1}^{4} k = 1 + 2 + 3 + 4 || $k$ läuft von $1$ bis $4$
       1 + 2 + 3 + 4 = 10 || addieren
       :::
       """,
       typische_fehler=[(6, "Du hast bei $3$ aufgehört. Die obere Grenze $4$ gehört dazu."),
                        (4, "$4$ ist die Anzahl der Summanden. Gefragt ist ihre Summe.")])

k.zahl("Wie viele Summanden hat $\\displaystyle\\sum_{k=3}^{10} k^2$?", 10 - 3 + 1,
       "Von $3$ bis $10$: $10 - 3 + 1 = 8$ Summanden, nämlich $3^2, 4^2, \\ldots, 10^2$.",
       tipps=["Zähle, welche Werte $k$ annimmt.", "$k = 3, 4, 5, 6, 7, 8, 9, 10$", "Anzahl $= N - n + 1$"],
       rechenweg=r"""
       :::rechnung
       10 - 3 + 1 = 8 || obere Grenze minus untere Grenze plus $1$
       :::
       """,
       typische_fehler=[(7, "Du hast $10 - 3$ gerechnet. Beide Grenzen zählen mit, also kommt $1$ dazu."),
                        (10, "Die Summe startet erst bei $k = 3$, nicht bei $1$.")])

k.zahl("Berechne $\\displaystyle\\sum_{j=-2}^{2} j^2$.", _S(lambda j: j * j, -2, 2),
       "$(-2)^2 + (-1)^2 + 0^2 + 1^2 + 2^2 = 4 + 1 + 0 + 1 + 4 = 10$.",
       tipps=["$j$ läuft von $-2$ bis $2$, das sind fünf Werte.", "Quadrate von negativen Zahlen sind positiv.",
              "$4 + 1 + 0 + 1 + 4$"],
       rechenweg=r"""
       :::rechnung
       \sum_{j=-2}^{2} j^2 = (-2)^2 + (-1)^2 + 0^2 + 1^2 + 2^2 || $j = -2, -1, 0, 1, 2$ einsetzen
       (-2)^2 + (-1)^2 + 0^2 + 1^2 + 2^2 = 4 + 1 + 0 + 1 + 4 || quadrieren
       = 10 || addieren
       :::
       """,
       typische_fehler=[(0, "Du hast $j$ addiert statt $j^2$. Der Summand ist $j^2$."),
                        (2, "$-2^2$ ist nicht $(-2)^2$. Hier wird die ganze Zahl $j = -2$ quadriert: $(-2)^2 = 4$."),
                        (5, "Du hast nur $0^2 + 1^2 + 2^2$ gerechnet. Die negativen Werte von $j$ gehören auch dazu.")])

# ── 2: Pünktchen → Σ ───────────────────────────────────────────────────────
k.erklaerung("Von den Pünktchen zum Summenzeichen", r"""
    ## Das Muster finden

    Umgekehrt willst du oft eine lange Summe kurz schreiben. Dazu suchst du eine
    Formel, die aus der Nummer $k$ den $k$-ten Summanden macht.

    Bei $1 + 3 + 5 + 7 + 9$ stehen die ungeraden Zahlen. Die $k$-te ungerade Zahl
    ist $2k - 1$. Es gibt fünf Summanden, also läuft $k$ von $1$ bis $5$.

    :::rechnung Beispiel vorgerechnet
    1 + 3 + 5 + 7 + 9 = \sum_{k=1}^{5} (2k - 1) || Summand Nummer $k$ ist $2k - 1$
    2 \cdot 1 - 1 = 1 || Probe für $k = 1$: erster Summand
    2 \cdot 5 - 1 = 9 || Probe für $k = 5$: letzter Summand
    1 + 3 + 5 + 7 + 9 = 25 || Wert der Summe
    :::

    Wechselnde Vorzeichen bekommst du mit $(-1)^k$:
    $-1 + 2 - 3 + 4 = \sum_{k=1}^{4} (-1)^k \, k$.

    :::alt Mit einer Tabelle erklärt
    Schreib zwei Zeilen untereinander: oben die Nummer $k = 1, 2, 3, 4, 5$,
    unten den Summanden $1, 3, 5, 7, 9$. Unten steht immer „doppelt so viel wie
    oben, minus $1$“. Dieses „doppelt minus $1$“ ist der Summand $2k - 1$.
    :::
    """)

k.mc("Welche Schreibweise ist gleich $1 + 3 + 5 + 7 + 9$?",
     [r"$\sum_{k=1}^{5} (2k - 1)$", r"$\sum_{k=1}^{5} (2k + 1)$", r"$\sum_{k=1}^{9} k$", r"$\sum_{k=0}^{5} (2k - 1)$"],
     "Für $k = 1, \\ldots, 5$ liefert $2k - 1$ genau $1, 3, 5, 7, 9$.",
     tipps=["Setze in jede Möglichkeit $k$ = untere Grenze ein: Kommt $1$ heraus?",
            "Prüfe auch die obere Grenze: Kommt $9$ heraus?", "$2 \\cdot 1 - 1 = 1$ und $2 \\cdot 5 - 1 = 9$."],
     fehler={r"$\sum_{k=1}^{5} (2k + 1)$": "Das ergibt $3 + 5 + 7 + 9 + 11$: alles um einen Platz verrutscht.",
             r"$\sum_{k=1}^{9} k$": "Das sind alle Zahlen $1 + 2 + \\ldots + 9$, auch die geraden.",
             r"$\sum_{k=0}^{5} (2k - 1)$": "Für $k = 0$ kommt der Summand $-1$ dazu: sechs Summanden statt fünf."})

k.luecke("Schreibe mit dem Summenzeichen. Welche obere Grenze gehört in die Lücke?",
         r"2 + 4 + 8 + 16 + 32 = \sum_{k=1}^{\luecke} 2^k", [[5]],
         "$2^1 = 2$, $2^2 = 4$, …, $2^5 = 32$. Der letzte Exponent ist $5$.",
         tipps=["Welche Zweierpotenz ist $32$?", "$32 = 2^5$", "Der Laufindex hört bei $5$ auf."],
         rechenweg=r"""
         :::rechnung
         2^1 = 2 || erster Summand für $k = 1$
         2^5 = 32 || letzter Summand für $k = 5$
         2 + 4 + 8 + 16 + 32 = 62 || Wert der Summe
         :::
         """,
         typische_fehler=[([32], "In die Lücke gehört der letzte Wert von $k$, nicht der letzte Summand: $32 = 2^5$."),
                          ([6], "Für $k = 6$ käme noch $2^6 = 64$ dazu. Der letzte Summand $32$ ist $2^5$.")])

# ── 3: Produktzeichen ──────────────────────────────────────────────────────
k.erklaerung("Das Produktzeichen", r"""
    ## Malnehmen statt addieren

    :::analogie 📈 Zinseszins
    Ein Guthaben wächst in jedem Jahr um einen Faktor. Nach drei Jahren hast du
    alle drei Faktoren miteinander malgenommen.
    :::

    Das [[Produktzeichen]] $\prod$ (großes Pi) liest du wie das Summenzeichen.
    Der Unterschied: Die Faktoren werden malgenommen.

    $$\prod_{k=n}^{N} a_k := a_n \cdot a_{n+1} \cdot \ldots \cdot a_{N-1} \cdot a_N$$

    :::rechnung Beispiel vorgerechnet
    \prod_{k=1}^{3} k^2 = 1^2 \cdot 2^2 \cdot 3^2 || $k = 1, 2, 3$ einsetzen
    1^2 \cdot 2^2 \cdot 3^2 = 1 \cdot 4 \cdot 9 || quadrieren
    = 36 || malnehmen
    \prod_{j=-2}^{0} (2j + 1) = (-3) \cdot (-1) \cdot 1 || $j = -2, -1, 0$ einsetzen
    (-3) \cdot (-1) \cdot 1 = 3 || minus mal minus gibt plus
    :::

    :::alt Als Programm erklärt
    Beim Produkt startet der Topf bei `p = 1`, nicht bei $0$. Dann kommt
    `for k in range(1, 4): p *= k**2`. Würdest du mit $0$ starten, wäre alles
    mal $0$ und am Ende $0$. Python hat dafür `math.prod`.
    :::
    """)

k.zahl("Berechne $\\displaystyle\\prod_{k=1}^{4} k$.", _P(lambda i: i, 1, 4),
       "$1 \\cdot 2 \\cdot 3 \\cdot 4 = 24$.",
       tipps=["$\\prod$ heißt malnehmen.", "Die Faktoren sind $1, 2, 3, 4$.", "$1 \\cdot 2 \\cdot 3 \\cdot 4$"],
       rechenweg=r"""
       :::rechnung
       \prod_{k=1}^{4} k = 1 \cdot 2 \cdot 3 \cdot 4 || $k = 1, 2, 3, 4$ einsetzen
       1 \cdot 2 \cdot 3 \cdot 4 = 24 || malnehmen
       :::
       """,
       typische_fehler=[(10, "Du hast addiert. Das Produktzeichen $\\prod$ heißt malnehmen."),
                        (6, "Du hast bei $3$ aufgehört. Die obere Grenze $4$ gehört dazu.")])

k.zahl("Berechne $\\displaystyle\\prod_{k=1}^{4} \\frac{k^2}{2}$. (Aufgabe aus der Vorkurs-Vorlesung)",
       _P(lambda i: F(i * i, 2), 1, 4),
       "$\\frac{1}{2} \\cdot \\frac{4}{2} \\cdot \\frac{9}{2} \\cdot \\frac{16}{2} = \\frac{576}{16} = 36$.",
       tipps=["Schreibe die vier Faktoren für $k = 1, 2, 3, 4$ hin.",
              "Im Nenner steht viermal die $2$, also $2^4 = 16$.", "Zähler: $1 \\cdot 4 \\cdot 9 \\cdot 16 = 576$."],
       rechenweg=r"""
       :::rechnung
       \prod_{k=1}^{4} \frac{k^2}{2} = \frac{1}{2} \cdot \frac{4}{2} \cdot \frac{9}{2} \cdot \frac{16}{2} || $k = 1, 2, 3, 4$ einsetzen
       \frac{1}{2} \cdot \frac{4}{2} \cdot \frac{9}{2} \cdot \frac{16}{2} = \frac{1 \cdot 4 \cdot 9 \cdot 16}{2^4} || Zähler mal Zähler, Nenner mal Nenner
       = \frac{576}{16} || ausrechnen
       = 36 || kürzen
       :::
       """,
       typische_fehler=[(F(576, 2), "Die $2$ im Nenner steht in **jedem** Faktor, also viermal: $2^4 = 16$."),
                        (15, "Das ist die Summe $\\frac{1 + 4 + 9 + 16}{2}$. $\\prod$ heißt malnehmen.")])

# ── 4: Leere Summe, leeres Produkt ─────────────────────────────────────────
k.erklaerung("Leere Summe und leeres Produkt", r"""
    ## Wenn der Start hinter dem Ende liegt

    Was ist $\sum_{k=5}^{4} k$? Der Laufindex soll bei $5$ starten und bei $4$
    aufhören. Es gibt keinen einzigen Summanden. Die TU vereinbart für $n > N$:

    $$\sum_{k=n}^{N} a_k := 0 \quad \text{(leere Summe)}, \qquad \prod_{k=n}^{N} a_k := 1 \quad \text{(leeres Produkt)}$$

    Warum gerade $0$ und $1$? Weil sie nichts verändern: $x + 0 = x$ und
    $x \cdot 1 = x$. Hängst du an eine [[leere Summe]] Summanden an, kommt genau
    deren Summe heraus. Beim [[leeren Produkt|leeres Produkt]] genauso.

    :::rechnung Beispiel vorgerechnet
    \sum_{k=1}^{3} k = \sum_{k=1}^{0} k + 1 + 2 + 3 || leere Summe plus drei Summanden
    0 + 1 + 2 + 3 = 6 || die leere Summe ist $0$
    \prod_{k=1}^{3} k = \prod_{k=1}^{0} k \cdot 1 \cdot 2 \cdot 3 || leeres Produkt mal drei Faktoren
    1 \cdot 1 \cdot 2 \cdot 3 = 6 || das leere Produkt ist $1$
    :::

    :::alt Mit einer Schleife erklärt
    `s = 0` und `for k in range(5, 5): s += k`: Die Schleife läuft kein
    einziges Mal. Übrig bleibt der Startwert $0$. Beim Produkt ist der
    Startwert `p = 1`, also bleibt $1$ übrig. Die Vereinbarung ist genau der
    Startwert der Schleife.
    :::
    """)

k.mc("Welchen Wert hat $\\displaystyle\\prod_{k=5}^{2} k$?", ["$1$", "$0$", "$120$", "$\\text{nicht definiert}$"],
     "Die untere Grenze $5$ ist größer als die obere $2$: leeres Produkt, also $1$.",
     tipps=["Vergleiche die untere und die obere Grenze.", "$5 > 2$: Es gibt keinen Faktor.",
            "Das leere Produkt ist per Vereinbarung …"],
     fehler={"$0$": "$0$ ist der Wert der leeren **Summe**. Beim Produkt ist es $1$, weil $x \\cdot 1 = x$.",
             "$120$": "Die Grenzen laufen nicht rückwärts. Von $5$ bis $2$ gibt es gar keinen Faktor.",
             "$\\text{nicht definiert}$": "Die TU vereinbart einen Wert: Das leere Produkt ist $1$."})

k.wf("$\\displaystyle\\sum_{k=4}^{3} k = 7$", False,
     "Falsch. Die untere Grenze $4$ ist größer als die obere $3$. Das ist eine leere Summe, ihr Wert ist $0$.",
     tipps=["Der Laufindex zählt nur aufwärts. Welche Werte nimmt er von $4$ bis $3$ an?"])

# ── 5: Rechenregeln ────────────────────────────────────────────────────────
k.erklaerung("Faktoren herausziehen", r"""
    ## Ausklammern im Großen

    Steht in jedem Summanden derselbe Faktor $\alpha$, darfst du ihn vor das
    Summenzeichen ziehen. Das ist das [[Distributivgesetz]], nur für viele Summanden.

    $$\sum_{k=n}^{N} \alpha \cdot a_k = \alpha \cdot \sum_{k=n}^{N} a_k \qquad \prod_{k=n}^{N} \alpha \cdot a_k = \alpha^{N-n+1} \cdot \prod_{k=n}^{N} a_k$$

    Beim Produkt steckt $\alpha$ in **jedem** der $N - n + 1$ Faktoren, deshalb
    kommt es als Potenz heraus. Summen darfst du außerdem auseinanderziehen:
    $\sum (a_k + b_k) = \sum a_k + \sum b_k$.

    :::rechnung Beispiel vorgerechnet
    \sum_{k=1}^{4} 3k = 3 \cdot \sum_{k=1}^{4} k || Faktor $3$ herausziehen
    3 \cdot (1 + 2 + 3 + 4) = 30 || Summe ausrechnen
    \prod_{k=1}^{3} 2k = 2^3 \cdot \prod_{k=1}^{3} k || drei Faktoren, also $2^3$
    2^3 \cdot (1 \cdot 2 \cdot 3) = 48 || ausrechnen
    :::

    :::achtung Nur einmal herausgezogen
    $\prod_{k=1}^{3} 2k$ ist nicht $2 \cdot 6 = 12$. Probe:
    $2 \cdot 4 \cdot 6 = 48$. Und Vorsicht: $\sum a_k b_k$ ist **nicht**
    $\sum a_k \cdot \sum b_k$.
    :::

    :::alt Mit Kisten erklärt
    Vier Kisten enthalten $3 \cdot 1$, $3 \cdot 2$, $3 \cdot 3$ und $3 \cdot 4$
    Flaschen. Du kannst jede Kiste zählen oder erst $1 + 2 + 3 + 4$ zählen und
    dann verdreifachen. Beim Produkt verdoppelst du dagegen jeden Faktor
    einzeln, das verdoppelt das Ergebnis dreimal hintereinander.
    :::
    """)

k.zahl("Berechne $\\displaystyle\\prod_{k=1}^{4} 3k$ mit der Regel zum Herausziehen.", _P(lambda i: 3 * i, 1, 4),
       "$\\prod_{k=1}^{4} 3k = 3^4 \\cdot (1 \\cdot 2 \\cdot 3 \\cdot 4) = 81 \\cdot 24 = 1944$.",
       tipps=["Der Faktor $3$ steckt in allen vier Faktoren.", "Also kommt $3^4 = 81$ heraus.",
              "$81 \\cdot 1 \\cdot 2 \\cdot 3 \\cdot 4$"],
       rechenweg=r"""
       :::rechnung
       \prod_{k=1}^{4} 3k = 3^4 \cdot \prod_{k=1}^{4} k || vier Faktoren, also $3^4$
       3^4 \cdot (1 \cdot 2 \cdot 3 \cdot 4) = 81 \cdot 24 || ausrechnen
       = 1944 || malnehmen
       :::
       """,
       typische_fehler=[(72, "Du hast die $3$ nur einmal herausgezogen. Sie steckt in jedem der vier Faktoren: $3^4$."),
                        (30, "Das ist die Summe $3 + 6 + 9 + 12$. Gefragt ist das Produkt.")])

# ── 6: Indexverschiebung ───────────────────────────────────────────────────
k.erklaerung("Indexverschiebung", r"""
    ## Umnummerieren, ohne etwas zu ändern

    :::analogie 🏠 Hausnummern
    Eine Straße bekommt neue Hausnummern: Jede Nummer wird um $5$ größer. Die
    Häuser bleiben dieselben, nur die Schilder ändern sich.
    :::

    Bei der [[Indexverschiebung]] um $j$ wandern beide Grenzen um $j$. Damit
    dieselben Summanden herauskommen, ersetzt du im Term $k$ durch $k - j$:

    $$\sum_{k=n}^{N} a_k = \sum_{k=n+j}^{N+j} a_{k-j} \qquad \prod_{k=n}^{N} a_k = \prod_{k=n+j}^{N+j} a_{k-j}$$

    :::rechnung Beispiel vorgerechnet
    \sum_{k=1}^{3} k = \sum_{k=6}^{8} (k - 5) || Grenzen $+5$, im Term $k$ durch $k - 5$ ersetzen
    (6 - 5) + (7 - 5) + (8 - 5) = 1 + 2 + 3 || Probe: dieselben Summanden
    \prod_{k=3}^{5} k^2 = \prod_{k=-2}^{0} (k + 5)^2 || Grenzen $-5$, $k$ durch $k + 5$ ersetzen
    (-2 + 5)^2 \cdot (-1 + 5)^2 \cdot (0 + 5)^2 = 3^2 \cdot 4^2 \cdot 5^2 || Probe
    :::

    :::achtung Falsche Richtung
    Grenzen **plus** $j$ heißt im Term **minus** $j$. Prüfe immer den ersten
    Summanden: Setze die neue untere Grenze ein, es muss der alte erste Summand
    herauskommen.
    :::

    :::alt Mit einer Warteschlange erklärt
    Fünf Leute stehen an, mit Nummern $1$ bis $5$. Ein neues System vergibt die
    Nummern $11$ bis $15$. Wer jetzt die $11$ hat, hatte vorher die $1$: alte
    Nummer gleich neue Nummer minus $10$. Genau dieses „minus“ kommt in den Term.
    :::
    ---
    ## Den letzten Summanden abspalten

    Eine Summe bis $n + 1$ ist die Summe bis $n$ plus der letzte Summand. Diesen
    Trick brauchst du bei der vollständigen Induktion ständig.

    $$\sum_{k=1}^{n+1} a_k = \sum_{k=1}^{n} a_k + a_{n+1}$$

    :::rechnung Beispiel vorgerechnet
    \sum_{k=1}^{4} k^2 = \sum_{k=1}^{3} k^2 + 4^2 || letzten Summanden abspalten
    (1 + 4 + 9) + 16 = 30 || Probe
    \sum_{k=1}^{n+1} k^2 = \sum_{k=1}^{n} k^2 + (n + 1)^2 || allgemein: $k = n + 1$ einsetzen
    :::

    :::alt Mit einem Stapel erklärt
    Ein Stapel aus $n + 1$ Tellern ist ein Stapel aus $n$ Tellern plus der
    oberste Teller. Wenn du weißt, wie schwer die unteren $n$ sind, musst du nur
    noch den obersten dazurechnen.
    :::
    """)

_IV_OPT = [r"$\sum_{k=1}^{8} (2k - 7)$", r"$\sum_{k=1}^{8} (2k + 9)$", r"$\sum_{k=1}^{8} (2k + 5)$",
           r"$\sum_{k=1}^{8} (2k - 3)$"]
k.mc("Welcher Term stimmt mit $\\displaystyle\\sum_{k=-3}^{4} (2k + 1)$ überein? (Aufgabe aus der Vorkurs-Vorlesung)",
     _IV_OPT,
     "Verschiebung um $4$: Grenzen $-3 + 4 = 1$ und $4 + 4 = 8$, im Term $k$ durch $k - 4$ ersetzen: "
     "$2(k - 4) + 1 = 2k - 7$.",
     tipps=["Die neue untere Grenze ist $1$. Um wie viel wurde verschoben?",
            "Um $j = 4$. Ersetze im Term $k$ durch $k - 4$.", "$2(k - 4) + 1 = 2k - 8 + 1$"],
     fehler={_IV_OPT[1]: "Falsche Richtung: Grenzen plus $4$ heißt im Term $k - 4$, nicht $k + 4$.",
             _IV_OPT[2]: "Du hast $4$ zum ganzen Term addiert. Ersetzt wird nur $k$ durch $k - 4$.",
             _IV_OPT[3]: "Die Klammer fehlt: $2(k - 4) = 2k - 8$, nicht $2k - 4$."},
     rechenweg=r"""
     :::rechnung
     \sum_{k=-3}^{4} (2k + 1) = \sum_{k=1}^{8} (2(k - 4) + 1) || Indexverschiebung um $4$
     2(k - 4) + 1 = 2k - 7 || ausmultiplizieren
     2 \cdot 1 - 7 = -5 || Probe: neuer erster Summand
     2 \cdot (-3) + 1 = -5 || alter erster Summand, passt
     :::
     """)

k.luecke("Verschiebe den Index so, dass die Summe bei $k = 2$ beginnt. Fülle obere Grenze und Summanden aus.",
         r"\sum_{k=0}^{4} (k + 2) = \sum_{k=2}^{\luecke} \luecke", [[6], ["k"]],
         "Grenzen $+2$: $0 + 2 = 2$ und $4 + 2 = 6$. Im Term $k$ durch $k - 2$ ersetzen: $(k - 2) + 2 = k$.",
         tipps=["Um wie viel wird verschoben? Die untere Grenze geht von $0$ auf $2$.",
                "Auch die obere Grenze wandert um $2$. Im Term wird $k$ zu $k - 2$.",
                "$(k - 2) + 2 = k$"],
         rechenweg=r"""
         :::rechnung
         \sum_{k=0}^{4} (k + 2) = \sum_{k=2}^{6} ((k - 2) + 2) || Grenzen $+2$, $k$ durch $k - 2$
         (k - 2) + 2 = k || vereinfachen
         2 + 3 + 4 + 5 + 6 = 20 || Probe: beide Summen sind $20$
         :::
         """,
         typische_fehler=[([6, "k + 4"], "Falsche Richtung: Grenzen plus $2$ heißt im Term $k - 2$ einsetzen."),
                          ([4, "k"], "Die obere Grenze muss mitwandern: $4 + 2 = 6$.")])

k.luecke("Spalte den letzten Summanden ab.",
         r"\sum_{k=1}^{n+1} k^3 = \sum_{k=1}^{n} k^3 + \luecke", [["(n+1)^3"]],
         "Der letzte Summand entsteht, wenn du $k = n + 1$ einsetzt: $(n + 1)^3$.",
         tipps=["Welcher Summand fehlt rechts noch?", "Der für $k = n + 1$.", "Setze $k = n + 1$ in $k^3$ ein."],
         rechenweg=r"""
         :::rechnung
         \sum_{k=1}^{n+1} k^3 = \sum_{k=1}^{n} k^3 + (n + 1)^3 || $k = n + 1$ einsetzen
         :::
         """,
         typische_fehler=[(["n^3 + 1"], "Klammern! Eingesetzt wird $k = n + 1$, also $(n + 1)^3$, nicht $n^3 + 1$."),
                          (["n^3"], "$n^3$ steckt schon in der Summe bis $n$. Es fehlt der Summand für $k = n + 1$.")])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


def _lin_tex(c, d, var="k"):
    """c·k + d als LaTeX."""
    s = var if c == 1 else f"-{var}" if c == -1 else f"{c}{var}"
    if d > 0:
        s += f" + {d}"
    elif d < 0:
        s += f" - {-d}"
    return s


def _lin_text(c, d, var="k"):
    return _lin_tex(c, d, var).replace(" ", "")


def summe_auswerten(rng):
    art = rng.choice(["linear", "quadrat", "wechsel", "linear", "leer"])
    a = rng.randint(-2, 3)
    b = a + rng.randint(2, 4)
    if art == "linear":
        c = rng.choice([2, 3, 4, 5, -2, -3])
        d = rng.choice([-3, -2, -1, 1, 2, 3])
        f = lambda i: c * i + d          # noqa: E731
        st = f"({_lin_tex(c, d)})"
    elif art == "quadrat":
        d = rng.choice([0, 1, -1, 2])
        f = lambda i: i * i + d          # noqa: E731
        st = "k^2" if d == 0 else f"(k^2 {'+' if d > 0 else '-'} {abs(d)})"
    elif art == "wechsel":
        f = lambda i: (-1) ** i * i      # noqa: E731
        st = "(-1)^k \\cdot k"
    else:
        c = rng.choice([2, 3, 5])
        f = lambda i: c * i              # noqa: E731
        st = f"{c}k"
        a, b = b, a                      # leere Summe
    w = _S(f, a, b)
    frage = f"Berechne $\\displaystyle\\sum_{{k={a}}}^{{{b}}} {st}$."
    if a > b:
        return {
            "frage": frage, "loesung": w,
            "tipps": ["Vergleiche zuerst untere und obere Grenze.", f"Die untere Grenze ${a}$ ist größer als die obere ${b}$.",
                      "Eine leere Summe hat den Wert $0$."],
            "rechenweg": _zeilen((f"\\sum_{{k={a}}}^{{{b}}} {st} = 0", f"${a} > {b}$: leere Summe")),
            "erklaerung": "Liegt die untere Grenze über der oberen, gibt es keinen Summanden. Die leere Summe ist $0$.",
            "typische_fehler": ohne_gleiche(w, [(_S(f, b, a), "Der Laufindex zählt nicht rückwärts. Hier gibt es keinen Summanden: leere Summe."),
                                                (1, "$1$ ist der Wert des leeren **Produkts**. Die leere Summe ist $0$.")]),
        }
    werte = [F(f(i)) for i in range(a, b + 1)]
    einzeln = " + ".join(tk(x) for x in werte)
    fehler = [(_S(f, a, b - 1), "Du hast den letzten Summanden vergessen. Die obere Grenze gehört dazu (anders als bei `range`)."),
              (_S(f, a + 1, b), "Du hast den ersten Summanden vergessen. Die untere Grenze gehört dazu.")]
    if art == "linear":
        fehler.append((sum(c * i for i in range(a, b + 1)) + d, "Das $" + str(d) + "$ gehört zu **jedem** Summanden, nicht nur einmal dazu."))
    if art == "quadrat":
        fehler.append((_S(lambda i: i + d, a, b), "Du hast $k$ statt $k^2$ addiert."))
    if art == "wechsel":
        fehler.append((_S(lambda i: i, a, b), "Das Vorzeichen $(-1)^k$ fehlt: Für ungerade $k$ ist es $-1$."))
    return {
        "frage": frage, "loesung": w,
        "tipps": [f"Der Laufindex nimmt die Werte ${', '.join(str(i) for i in range(a, b + 1))}$ an.",
                  "Setze jeden Wert ein und schreibe die Summanden nebeneinander.",
                  f"Die Summanden sind ${einzeln}$."],
        "rechenweg": _zeilen((f"\\sum_{{k={a}}}^{{{b}}} {st} = {einzeln}", f"$k = {a}, \\ldots, {b}$ einsetzen"),
                             (f"{einzeln} = {mathlib.tex(w)}", "addieren")),
        "erklaerung": "Laufindex von der unteren bis zur oberen Grenze einsetzen, dann addieren.",
        "typische_fehler": ohne_gleiche(w, fehler),
    }


def produkt_auswerten(rng):
    art = rng.choice(["linear", "faktor", "leer", "linear"])
    if art == "linear":
        a = rng.randint(-3, 1)
        b = a + rng.randint(2, 3)
        d = rng.choice([1, 2, 3, 4, 5])
        if any(i + d == 0 for i in range(a, b + 1)):
            d += b - a + 1 + (-a)
        f = lambda i: i + d              # noqa: E731
        st = f"(k + {d})"
        w = _P(f, a, b)
        werte = [F(f(i)) for i in range(a, b + 1)]
        einzeln = " \\cdot ".join(tk(x) for x in werte)
        fehler = [(_S(f, a, b), "Du hast addiert. Das Produktzeichen $\\prod$ heißt malnehmen."),
                  (_P(f, a, b - 1), "Du hast den letzten Faktor vergessen. Die obere Grenze gehört dazu.")]
        zeilen = [(f"\\prod_{{k={a}}}^{{{b}}} {st} = {einzeln}", f"$k = {a}, \\ldots, {b}$ einsetzen"),
                  (f"{einzeln} = {mathlib.tex(w)}", "malnehmen")]
        tipps = ["$\\prod$ heißt malnehmen.", f"Setze $k = {a}, \\ldots, {b}$ ein.", f"Die Faktoren sind ${einzeln}$."]
    elif art == "faktor":
        c = rng.choice([2, 3, 5, 10])
        m = rng.randint(2, 4)
        a, b = 1, m
        st = f"{c}k"
        w = _P(lambda i: c * i, 1, m)
        fak = " \\cdot ".join(str(i) for i in range(1, m + 1))
        fehler = [(c * _P(lambda i: i, 1, m), f"Die ${c}$ steckt in **jedem** der ${m}$ Faktoren, also kommt ${c}^{m}$ heraus."),
                  (_S(lambda i: c * i, 1, m), "Du hast addiert. $\\prod$ heißt malnehmen.")]
        zeilen = [(f"\\prod_{{k=1}}^{{{m}}} {c}k = {c}^{m} \\cdot \\prod_{{k=1}}^{{{m}}} k", f"${m}$ Faktoren, jeder enthält ${c}$"),
                  (f"{c}^{m} \\cdot ({fak}) = {mathlib.tex(w)}", "ausrechnen")]
        tipps = [f"Ziehe die ${c}$ aus jedem Faktor heraus.", f"Es gibt ${m}$ Faktoren, also ${c}^{m}$.",
                 f"${c}^{m} \\cdot ({fak})$"]
    else:
        a = rng.randint(3, 6)
        b = a - rng.randint(1, 3)
        st = rng.choice(["k", "(k + 1)", "k^2", "2k"])
        w = F(1)
        fehler = [(0, "$0$ ist die leere **Summe**. Das leere Produkt ist $1$."),
                  (_P(lambda i: i, b, a), "Der Laufindex zählt nicht rückwärts. Es gibt keinen Faktor.")]
        zeilen = [(f"\\prod_{{k={a}}}^{{{b}}} {st} = 1", f"${a} > {b}$: leeres Produkt")]
        tipps = ["Vergleiche zuerst untere und obere Grenze.", f"${a} > {b}$", "Das leere Produkt hat den Wert $1$."]
    return {
        "frage": f"Berechne $\\displaystyle\\prod_{{k={a}}}^{{{b}}} {st}$.",
        "loesung": w, "tipps": tipps, "rechenweg": _zeilen(*zeilen),
        "erklaerung": "Faktoren für alle Werte des Laufindex malnehmen. Leeres Produkt: $1$.",
        "typische_fehler": ohne_gleiche(w, fehler),
    }


def indexverschiebung(rng):
    a = rng.randint(-3, 3)
    b = a + rng.randint(3, 6)
    neu = rng.choice([x for x in range(-2, 4) if x != a])
    j = neu - a
    art = rng.choice(["linear", "quadrat"])
    if art == "linear":
        c = rng.choice([2, 3, -2, 4])
        d = rng.choice([-5, -1, 1, 3, 4])
        st = _lin_tex(c, d)
        neu_term = _lin_text(c, d - c * j)
        falsch_term = _lin_text(c, d + c * j)
        f_alt = lambda i: c * i + d                  # noqa: E731
        f_neu = lambda i: c * i + d - c * j          # noqa: E731
        zwischen = f"{c} \\cdot (k {'-' if j > 0 else '+'} {abs(j)}) {'+' if d > 0 else '-'} {abs(d)}"
        zeile2 = (f"{zwischen} = {_lin_tex(c, d - c * j)}", "ausmultiplizieren")
        st_anzeige = f"({st})"
    else:
        st = "k^2"
        neu_term = f"(k{'-' if j > 0 else '+'}{abs(j)})^2"
        falsch_term = f"(k{'+' if j > 0 else '-'}{abs(j)})^2"
        f_alt = lambda i: i * i                      # noqa: E731
        f_neu = lambda i: (i - j) ** 2               # noqa: E731
        zeile2 = (f"(k {'-' if j > 0 else '+'} {abs(j)})^2 = k^2 {'-' if j > 0 else '+'} {2 * abs(j)}k + {j * j}",
                  "zur Kontrolle ausmultipliziert")
        st_anzeige = st
    assert _S(f_alt, a, b) == _S(f_neu, a + j, b + j)
    loesung = [[b + j], [neu_term]]
    rich = f"um ${j}$ nach oben" if j > 0 else f"um ${-j}$ nach unten"
    return {
        "frage": f"Verschiebe den Index so, dass die Summe bei $k = {neu}$ beginnt. Fülle obere Grenze und Summanden aus.",
        "formel": f"\\sum_{{k={a}}}^{{{b}}} {st_anzeige} = \\sum_{{k={neu}}}^{{\\luecke}} \\left(\\luecke\\right)",
        "antworten": loesung,
        "tipps": [f"Die untere Grenze wandert von ${a}$ auf ${neu}$, also {rich}.",
                  f"Die obere Grenze wandert genauso: ${b} {'+' if j > 0 else '-'} {abs(j)} = {b + j}$.",
                  f"Im Term ersetzt du $k$ durch $k {'-' if j > 0 else '+'} {abs(j)}$."],
        "rechenweg": _zeilen((f"\\sum_{{k={a}}}^{{{b}}} {st_anzeige} = \\sum_{{k={neu}}}^{{{b + j}}} "
                              f"\\left({st.replace('k', '(k ' + ('-' if j > 0 else '+') + ' ' + str(abs(j)) + ')')}\\right)",
                              f"Grenzen ${'+' if j > 0 else '-'}{abs(j)}$, im Term $k$ durch $k {'-' if j > 0 else '+'} {abs(j)}$ ersetzen"),
                             zeile2,
                             (" + ".join(tk(F(f_alt(i))) for i in range(a, b + 1)) + " = " + mathlib.tex(_S(f_alt, a, b)),
                              "Probe: alte Summanden"),
                             (" + ".join(tk(F(f_neu(i))) for i in range(a + j, b + j + 1)) + " = " + mathlib.tex(_S(f_neu, a + j, b + j)),
                              "neue Summanden: dieselben Zahlen, derselbe Wert")),
        "erklaerung": "Grenzen um $j$ verschieben, im Term $k$ durch $k - j$ ersetzen. Probe: Der erste Summand bleibt gleich.",
        "typische_fehler": ohne_gleiche(loesung, [
            ([[b + j], [falsch_term]], "Falsche Richtung: Wandern die Grenzen um $j$ nach oben, kommt im Term $k - j$ hinein."),
            ([[b], [neu_term]], "Die obere Grenze muss genauso mitwandern wie die untere.")]),
    }


k.praxis()

k.generator(summe_auswerten, typ="zahl", titel="Summen ausrechnen")
k.generator(produkt_auswerten, typ="zahl", titel="Produkte ausrechnen")
k.generator(indexverschiebung, typ="luecke", titel="Indexverschiebung")

_t1 = _S(lambda i: (i - 2) ** 2, 3, 7)
k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: Indexverschiebung

    Zeigen Sie durch eine Indexverschiebung, dass
    $$\sum_{k=3}^{7} (k - 2)^2 = \sum_{k=1}^{5} k^2$$
    gilt, und berechnen Sie den Wert.
    """,
    [{"typ": "zahl", "frage": "Um wie viel muss der Index verschoben werden, damit die Summe bei $k = 1$ beginnt? "
      "(Gib die Zahl $j$ an, die zu den Grenzen addiert wird.)", "loesung": -2,
      "tipps": ["Die untere Grenze soll von $3$ auf $1$.", "$3 + j = 1$"],
      "rechenweg": "$3 + (-2) = 1$, also $j = -2$.",
      "typische_fehler": [(2, "Die Grenze wird kleiner: von $3$ auf $1$. Also $j = -2$.")]},
     {"typ": "term", "frage": "Was steht nach der Verschiebung im Summanden? ($k$ wird durch $k - j = k + 2$ ersetzt.)",
      "loesung": "k^2", "variablen": "k",
      "tipps": ["Ersetze in $(k - 2)^2$ das $k$ durch $k + 2$.", "$((k + 2) - 2)^2$"],
      "rechenweg": "$((k + 2) - 2)^2 = k^2$",
      "typische_fehler": [("(k-4)^2", "Falsche Richtung: Bei $j = -2$ wird $k$ durch $k + 2$ ersetzt.")]},
     {"typ": "zahl", "frage": "Berechne den Wert der Summe.", "loesung": _t1,
      "tipps": ["$1 + 4 + 9 + 16 + 25$", "Addiere die fünf Quadratzahlen."],
      "rechenweg": "$1 + 4 + 9 + 16 + 25 = 55$",
      "typische_fehler": [(30, "Das ist nur bis $4^2$. Die Summe geht bis $5^2 = 25$.")]}],
    "Indexverschiebung: Grenzen um $j$ ändern und im Term $k$ durch $k - j$ ersetzen.",
    uebungsblatt=True,
    tipps=["Zuerst die Verschiebung bestimmen, dann den Term umschreiben.",
           "Bei $j = -2$ wird $k$ durch $k + 2$ ersetzt."],
    rechenweg=r"""
    :::rechnung
    \sum_{k=3}^{7} (k - 2)^2 = \sum_{k=1}^{5} ((k + 2) - 2)^2 || Indexverschiebung um $j = -2$
    ((k + 2) - 2)^2 = k^2 || vereinfachen
    1 + 4 + 9 + 16 + 25 = 55 || Wert
    :::
    """)

k.papier(r"""
    ## Übungsblatt-Stil: Teleskopsumme

    Sei $n \in \mathbb{N}$.

    a) Zeigen Sie mit einer Indexverschiebung: $\displaystyle\sum_{k=1}^{n} \big((k + 1)^2 - k^2\big) = (n + 1)^2 - 1$.

    b) Folgern Sie daraus mit den Rechenregeln für Summen: $\displaystyle\sum_{k=1}^{n} k = \frac{n(n + 1)}{2}$.
    """,
    r"""
    **a)** Summe auseinanderziehen, im ersten Teil den Index um $1$ verschieben:

    $$\sum_{k=1}^{n} \big((k+1)^2 - k^2\big) = \sum_{k=1}^{n} (k+1)^2 - \sum_{k=1}^{n} k^2 = \sum_{k=2}^{n+1} k^2 - \sum_{k=1}^{n} k^2$$

    Beide Summen enthalten $2^2, \ldots, n^2$. Diese heben sich weg. Übrig bleibt
    der letzte Summand der ersten und der erste Summand der zweiten Summe:

    $$= (n+1)^2 - 1^2 = (n + 1)^2 - 1.$$

    **b)** Ausmultiplizieren: $(k+1)^2 - k^2 = 2k + 1$. Mit a) und den Rechenregeln:

    $$(n+1)^2 - 1 = \sum_{k=1}^{n} (2k + 1) = 2 \sum_{k=1}^{n} k + \sum_{k=1}^{n} 1 = 2 \sum_{k=1}^{n} k + n.$$

    :::rechnung Nach der Summe auflösen
    (n + 1)^2 - 1 - n = n^2 + n || ausmultiplizieren
    \frac{n^2 + n}{2} = \frac{n(n + 1)}{2} || durch $2$ teilen, $n$ ausklammern
    :::

    Also $\sum_{k=1}^{n} k = \frac{n(n+1)}{2}$. $\square$
    """,
    ["Ich habe die Summe in zwei Summen zerlegt",
     "Ich habe den Index in $\\sum (k+1)^2$ richtig verschoben (Grenzen $2$ bis $n + 1$)",
     "Ich habe begründet, welche Summanden sich wegheben",
     "Ich habe $(k+1)^2 - k^2 = 2k + 1$ benutzt und $\\sum_{k=1}^{n} 1 = n$ beachtet",
     "Ich bin bei $\\frac{n(n+1)}{2}$ angekommen"],
    "Summen, bei denen sich fast alles weghebt, heißen Teleskopsummen: Wie ein Fernrohr schieben sie sich zusammen.",
    uebungsblatt=True,
    tipps=["Ziehe die Summe in $\\sum (k+1)^2 - \\sum k^2$ auseinander und verschiebe im ersten Teil den Index."])

k.zusammenfassung(r"""
    ## Summen- und Produktzeichen

    | Was | Schreibweise | Beispiel |
    |---|---|---|
    | Summe | $\sum_{k=n}^{N} a_k = a_n + \ldots + a_N$ | $\sum_{k=1}^{3} 2k = 12$ |
    | Produkt | $\prod_{k=n}^{N} a_k = a_n \cdot \ldots \cdot a_N$ | $\prod_{k=1}^{3} k^2 = 36$ |
    | leere Summe ($n > N$) | $\sum_{k=n}^{N} a_k = 0$ | $\sum_{k=5}^{4} k = 0$ |
    | leeres Produkt ($n > N$) | $\prod_{k=n}^{N} a_k = 1$ | $\prod_{k=1}^{0} k = 1$ |
    | Faktor heraus | $\sum \alpha a_k = \alpha \sum a_k$, $\prod_{k=n}^{N} \alpha a_k = \alpha^{N-n+1} \prod a_k$ | $\prod_{k=1}^{3} 2k = 2^3 \cdot 6$ |
    | Indexverschiebung | $\sum_{k=n}^{N} a_k = \sum_{k=n+j}^{N+j} a_{k-j}$ | $\sum_{k=1}^{3} k = \sum_{k=6}^{8} (k-5)$ |
    | Abspalten | $\sum_{k=1}^{n+1} a_k = \sum_{k=1}^{n} a_k + a_{n+1}$ | |

    !! Anzahl der Summanden von $n$ bis $N$: $N - n + 1$.

    - Grenzen plus $j$ heißt im Term $k - j$. Probe mit dem ersten Summanden.
    - Der Laufindex darf beliebig heißen: $\sum_{k} a_k = \sum_{i} a_i$.
""")
