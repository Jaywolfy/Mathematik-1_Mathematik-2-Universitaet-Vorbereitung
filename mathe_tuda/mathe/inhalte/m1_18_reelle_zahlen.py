# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 18: Die reellen Zahlen (Skript Disser WS 26/27, Abschn. 3.6, Def. 3.80 bis Satz 3.93)."""
from fractions import Fraction as F

from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(
    slug="reelle_zahlen",
    titel="Die reellen Zahlen",
    beschreibung="Lücken in ℚ, Vollständigkeitsaxiom, Intervalle, ℚ liegt dicht, n-te Wurzel, rationale Potenz, Betrag und Dreiecksungleichung",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 3.6",
    icon="📏")


# ── Python rechnet exakt ─────────────────────────────────────────────────
def iroot(x, n):
    """Exakte n-te Wurzel einer natürlichen Zahl, sonst None."""
    r = round(x ** (1 / n))
    for c in (r - 1, r, r + 1):
        if c >= 0 and c ** n == x:
            return c
    return None


def brtex(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"\\frac{{{x.numerator}}}{{{x.denominator}}}"


def rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def verbessern(u):
    """Zu jeder rationalen oberen Schranke u > 0 von S = {t ∈ ℚ | t ≥ 0, t² < 2} eine kleinere (Bsp. 1.56)."""
    return (u + 2 / u) / 2


# Bemerkung zu (3.1): keine kleinste rationale obere Schranke
_u = F(3, 2)
for _ in range(6):
    _v = verbessern(_u)
    assert _u * _u > 2 and _v * _v > 2 and 0 < _v < _u and _v * _v != 2
    _u = _v
assert verbessern(F(3, 2)) == F(17, 12)
assert F(7, 5) ** 2 < 2 < F(3, 2) ** 2 and F(141, 100) ** 2 < 2 < F(142, 100) ** 2
# Satz 3.86 an einem Beispiel
assert F(1, 3) < (F(1, 3) + F(1, 2)) / 2 < F(1, 2) and (F(1, 3) + F(1, 2)) / 2 == F(5, 12)
# Beispiel 3.91 und Satz 3.90 (Unabhängigkeit von der Bruchdarstellung)
assert iroot(16 ** 3, 4) == 8 and F(1, iroot(16, 2)) == F(1, 4)
assert iroot(9 ** 2, 4) == iroot(9, 2) == 3
# Satz 3.93 (Dreiecksungleichung, Produktregel) an Stichproben
_zahlen = [F(a, b) for a in range(-6, 7) for b in (1, 2, 3)]
assert all(abs(x + y) <= abs(x) + abs(y) and abs(x * y) == abs(x) * abs(y) and abs(x) == abs(-x) for x in _zahlen for y in _zahlen)
assert all(-abs(x) <= x <= abs(x) for x in _zahlen)

k.lernziele([
    "Ich kann begründen, warum $\\mathbb{Q}$ Lücken hat, und das Vollständigkeitsaxiom (R2) formulieren (Def. 3.80, Beob. 3.81)",
    "Ich kann Intervalle in den vier Formen schreiben und offene, abgeschlossene und halboffene unterscheiden (Def. 3.85)",
    "Ich kenne die Sätze 3.86 und 3.87 (ℚ dicht in ℝ, Existenz der $n$-ten Wurzel) und kann Wurzeln und rationale Potenzen berechnen (Def. 3.88, 3.89, Satz 3.90, Bsp. 3.91)",
    "Ich kann den Betrag und die Dreiecksungleichung benutzen und beweisen (Def. 3.92, Satz 3.93)",
])

k.warum(r"""
Computer rechnen mit rationalen Zahlen (Gleitkomma ist eine endliche Näherung davon). Trotzdem arbeitet die Analysis
mit $\mathbb{R}$: Grenzwerte, Nullstellen und $\sqrt{2}$ existieren nur dort. Das Vollständigkeitsaxiom ist der Grund, warum eine
stetige Funktion mit Vorzeichenwechsel eine Nullstelle hat, warum Algorithmen wie Bisektion und Newton-Verfahren
funktionieren und warum monotone, beschränkte Folgen konvergieren (Kap. „Folgen“). Der Betrag misst Abstand, die Dreiecksungleichung
ist die Grundlage jeder Fehlerabschätzung.
""")

# ── Seite 1: Lücken in ℚ ─────────────────────────────────────────────────
k.erklaerung("Lücken in ℚ", r"""
## Die Fallkurve

Eine Kugel fällt: $h(t) = 2 - t^2$. Die rationalen Zeitpunkte, zu denen sie noch über dem Boden ist, sind
$$S := \{t \in \mathbb{Q} \mid t \ge 0 \text{ und } t^2 < 2\}.$$
$S \ne \emptyset$ (es enthält $0$) und $S$ hat obere Schranken, aber **kein [[Supremum]] in $\mathbb{Q}$** (Bsp. 1.56). Der Aufprall liegt in einer Lücke.

:::rechnung Keine kleinste rationale obere Schranke
(3/2)^2 = 9/4 || $\frac32$ ist obere Schranke von $S$, denn $\frac94 > 2$
(3/2 + 2/(3/2))/2 = 17/12 || $u \mapsto \frac12(u + \frac2u)$ liefert eine kleinere rationale Schranke
(17/12)^2 = 289/144 || $\frac{289}{144} > 2$: wieder eine obere Schranke, wieder kleiner als $\frac32$
:::

Das geht endlos weiter: Zu jeder rationalen oberen Schranke gibt es eine kleinere. Eine **kleinste** gibt es nicht.

:::alt Als Zollstock
Du misst die Diagonale eines Einheitsquadrats mit einem Zollstock, der nur Bruchteile kennt. Egal, wie fein die Striche sind, die Diagonale landet zwischen zwei Strichen und trifft keinen. Es fehlt eine Zahl.
:::
""")

k.mc("Warum hat $S = \\{t \\in \\mathbb{Q} \\mid t \\ge 0,\\ t^2 < 2\\}$ in $\\mathbb{Q}$ kein Supremum?",
     ["Zu jeder rationalen oberen Schranke gibt es eine kleinere rationale obere Schranke, eine kleinste existiert nicht",
      "Weil $S$ nach oben unbeschränkt ist",
      "Weil $S$ leer ist",
      "Weil $\\sqrt{2}$ rational ist"],
     "$S$ ist nichtleer ($0 \\in S$) und nach oben beschränkt (durch $\\frac32$). Das Supremum müsste $\\sqrt{2}$ sein, und das ist nicht rational. Die Verbesserung $u \\mapsto \\frac12(u + \\frac2u)$ zeigt, dass es keine kleinste rationale Schranke gibt.",
     tipps=["Hat $S$ eine obere Schranke? Ist es leer?", "Wie groß wäre die kleinste obere Schranke, wenn man alle reellen Zahlen zulassen dürfte?"],
     fehler={"Weil $S$ nach oben unbeschränkt ist": "$\\frac32$ ist eine obere Schranke von $S$: Für $t \\in S$ gilt $t^2 < 2 < \\frac94$.",
             "Weil $S$ leer ist": "$0 \\in S$, denn $0^2 = 0 < 2$.",
             "Weil $\\sqrt{2}$ rational ist": "$\\sqrt{2}$ ist **nicht** rational (Kap. „Beweisformen“). Genau das erzeugt die Lücke."})

# ── Seite 2: Definition 3.80 ─────────────────────────────────────────────
k.erklaerung("Definition 3.80: Die Axiome der reellen Zahlen", r"""
## Axiome statt Konstruktion

Wie bei den natürlichen Zahlen (Peano) legt das Skript Axiome fest.

**Definition 3.80.** $(\mathbb{R}, +, \cdot, \le)$ erfüllt die Axiome der reellen Zahlen, falls

- **R1.** $(\mathbb{R}, +, \cdot, \le)$ ist ein [[angeordneter Körper]],
- **R2.** (Vollständigkeitsaxiom) Jede nichtleere, nach oben beschränkte Teilmenge von $\mathbb{R}$ hat ein Supremum in $\mathbb{R}$.

**Beobachtung 3.81.** Jede nichtleere, nach unten beschränkte Menge $A$ hat ein [[Infimum]]: $\inf A = -\sup(-A)$ mit $-A := \{-a \mid a \in A\}$.

**Satz 3.82 (ohne Beweis).** Es gibt einen vollständigen angeordneten Körper, und je zwei sind durch genau einen ordnungserhaltenden Körperisomorphismus isomorph. **Definition 3.83:** Wähle einen; seine Elemente heißen reelle Zahlen, und $\mathbb{Q}$ wird über $\iota$ mit einem Teil von $\mathbb{R}$ identifiziert.

:::rechnung Suprema in $\mathbb{R}$
\sup \{t \in \mathbb{R} \mid t \ge 0,\ t^2 < 2\} = \sqrt{2} || in $\mathbb{R}$ existiert das Supremum der Menge $S$ (R2), in $\mathbb{Q}$ nicht
\inf \{1/n \mid n \in \mathbb{N} \setminus \{0\}\} = 0 || $-A$ hat das Supremum $0$, also $\inf A = -0 = 0$ (Beob. 3.81)
:::

**Bemerkung 3.84.** Eine Konstruktion identifiziert $q \in \mathbb{Q}$ mit $\{q' \in \mathbb{Q} \mid q' < q\}$ und $\sqrt{2}$ mit $\{q \in \mathbb{Q} \mid q < 0 \text{ oder } q^2 < 2\}$.

:::alt Als lückenloses Lineal
$\mathbb{R}$ ist ein Lineal ohne Lücken: Von oben nach unten schiebst du eine Schranke herunter, bis sie nicht mehr weiter kann. Dort ist der Punkt. In $\mathbb{Q}$ kommst du bei $\sqrt{2}$ an eine Stelle, an der kein Strich steht.
:::
""")

k.wf("$\\mathbb{Q}$ ist ein angeordneter Körper, erfüllt aber das Vollständigkeitsaxiom nicht.", True,
     "R1 gilt für $\\mathbb{Q}$ (Bsp. 3.77). R2 scheitert: Die Menge $S = \\{t \\in \\mathbb{Q} \\mid t \\ge 0, t^2 < 2\\}$ ist nichtleer, nach oben beschränkt und hat kein rationales Supremum.",
     tipps=["Welche der beiden Axiome R1, R2 gilt für $\\mathbb{Q}$?"])

k.zahl("Sei $A = \\{1 + \\frac1n \\mid n \\in \\mathbb{N}\\setminus\\{0\\}\\} = \\{2, \\frac32, \\frac43, \\ldots\\}$. Bestimme $\\inf A$.", 1,
       "Alle Elemente sind $> 1$, und $1 + \\frac1n$ kommt beliebig nah an $1$ heran: $\\inf A = 1$. Es gibt kein Minimum: $1 \\notin A$. Das größte Element ist $2$, ein Maximum.",
       tipps=["Welche Zahl ist untere Schranke von $A$?", "Wie klein wird $\\frac1n$ für große $n$?", "$1$ ist die größte untere Schranke, wird aber nie angenommen."],
       rechenweg=rechnung([("1 + 1/1 = 2", "$n = 1$: das größte Element"), ("1 + 1/100 = 101/100", "$n = 100$: schon nah an $1$"), ("1 + 1/n > 1", "für jedes $n$: $1$ ist untere Schranke, aber nicht angenommen")]),
       typische_fehler=[(2, "$2$ ist das **Maximum** von $A$ (größtes Element), nicht das Infimum."),
                        (0, "$0$ ist eine untere Schranke, aber nicht die größte. Alle Elemente sind $> 1$.")])

# ── Seite 3: Intervalle ──────────────────────────────────────────────────
k.erklaerung("Definition 3.85: Intervalle", r"""
## Offen, abgeschlossen, halboffen

Für $a \le b$ in $\mathbb{R}$ ist
$$(a, b) := \{x \in \mathbb{R} \mid a < x < b\},\quad [a, b] := \{x \mid a \le x \le b\},\quad (a, b] := \{x \mid a < x \le b\},\quad [a, b) := \{x \mid a \le x < b\}.$$
$(a, b)$ heißt offen, $[a, b]$ abgeschlossen, $(a, b]$ und $[a, b)$ halboffen. Dazu die unbeschränkten [[Intervall|Intervalle]] $(a, \infty)$, $[a, \infty)$, $(-\infty, a)$, $(-\infty, a]$ und $(-\infty, \infty) = \mathbb{R}$.

$-\infty$ und $\infty$ sind **keine** reellen Zahlen, nur Teil der Schreibweise. Neben $(a, b]$ findest du manchmal $]a, b]$.

:::visual zahlenstrahl
{"von": -1, "bis": 6, "schritt": 1,
 "intervalle": [{"von": 0, "bis": 2, "von_zu": true, "bis_zu": false, "label": "[0, 2)"}, {"von": 3, "bis": 5, "von_zu": false, "bis_zu": true, "label": "(3, 5]"}],
 "unterschrift": "Ausgefüllt heißt: Der Randpunkt gehört dazu. Ein Kreis heißt: nicht dabei."}
:::

:::achtung Runde Klammer bei ±∞
$\infty$ gehört nie dazu: Es heißt $[a, \infty)$, nie $[a, \infty]$.
:::

:::alt Als Einlass
Eckige Klammer: Die Person an der Tür darf hinein. Runde Klammer: Sie steht noch draußen. Bei $\infty$ gibt es keine Tür, also nur eine runde Klammer.
:::
""")

k.zuordnen("Ordne jede Menge der richtigen Intervallschreibweise zu.",
           [("$\\{x \\in \\mathbb{R} \\mid -1 < x \\le 3\\}$", "(-1, 3]"),
            ("$\\{x \\in \\mathbb{R} \\mid -1 \\le x < 3\\}$", "[-1, 3)"),
            ("$\\{x \\in \\mathbb{R} \\mid x \\ge 3\\}$", "[3, ∞)"),
            ("$\\{x \\in \\mathbb{R} \\mid x < 3\\}$", "(-∞, 3)"),
            ("$\\{x \\in \\mathbb{R} \\mid |x| \\le 3\\}$", "[-3, 3]")],
           "„$<$“ gibt eine runde Klammer, „$\\le$“ eine eckige. $\\infty$ steht immer in runder Klammer. $|x| \\le 3$ bedeutet $-3 \\le x \\le 3$.",
           ablenker=["[3, ∞]"],
           tipps=["Strikte Ungleichung heißt: Randpunkt gehört nicht dazu.", "Bei $\\pm\\infty$ gibt es keinen Randpunkt."])


def _ivtex(a, b, lo, ro):
    return ("(" if lo else "[") + str(a) + ", " + str(b) + (")" if ro else "]")


def intervall_notation(rng):
    a = rng.randint(-6, 3)
    b = a + rng.randint(2, 6)
    form = rng.choice(["beschr", "beschr", "unten", "oben"])
    LE, GE = "\\le", "\\ge"
    if form == "beschr":
        lo, ro = rng.random() < 0.5, rng.random() < 0.5
        zl = "<" if lo else LE
        zr = "<" if ro else LE
        bed = f"{a} {zl} x {zr} {b}"
        richtig = _ivtex(a, b, lo, ro)
        optionen = [richtig] + [_ivtex(a, b, l, r) for l in (True, False) for r in (True, False) if (l, r) != (lo, ro)]
        fehler = {}
        for o in optionen[1:]:
            if o[0] != richtig[0] and o[-1] != richtig[-1]:
                wo = "beiden Enden"
            elif o[0] != richtig[0]:
                wo = "dem linken Ende"
            else:
                wo = "dem rechten Ende"
            fehler[o] = f"Die Klammer an {wo} passt nicht: „<“ gehört zu einer runden, „≤“ zu einer eckigen Klammer."
        gl = f"Strikt: ${a}$ gehört nicht dazu, runde Klammer" if lo else f"${a}$ gehört dazu, eckige Klammer"
        gr = f"Strikt: ${b}$ gehört nicht dazu, runde Klammer" if ro else f"${b}$ gehört dazu, eckige Klammer"
        zeilen = [("\\text{linkes Ende}", gl), ("\\text{rechtes Ende}", gr)]
    else:
        zu = rng.random() < 0.5
        if form == "unten":
            bed = f"x {GE if zu else '>'} {a}"
            richtig = ("[" if zu else "(") + f"{a}, ∞)"
            optionen = [richtig, ("(" if zu else "[") + f"{a}, ∞)", f"(-∞, {a}" + (")" if zu else "]"), f"[{a}, ∞]"]
        else:
            bed = f"x {LE if zu else '<'} {b}"
            richtig = "(-∞, " + str(b) + ("]" if zu else ")")
            optionen = [richtig, "(-∞, " + str(b) + (")" if zu else "]"), ("[" if zu else "(") + f"{b}, ∞)", f"[-∞, {b}" + ("]" if zu else ")")]
        fehler = {o: "Prüfe: Gehört der Randpunkt dazu (eckig) oder nicht (rund)? Und liegt die Menge links oder rechts vom Randpunkt? Bei $\\pm\\infty$ steht immer eine runde Klammer." for o in optionen[1:]}
        zeilen = [("\\text{Randpunkt dabei? Richtung?}", "$\\ge$ und $\\le$: eckige Klammer. $>$ und $<$: runde Klammer.")]
    return {"typ": "mc",
            "frage": f"Welche Intervallschreibweise beschreibt $\\{{x \\in \\mathbb{{R}} \\mid {bed}\\}}$?",
            "optionen": optionen, "fehler": fehler,
            "tipps": ["Gehören die Randpunkte dazu? „$\\le$“ ja (eckig), „$<$“ nein (rund).", "Bei $\\infty$ steht immer eine runde Klammer.", "Zeichne die Menge auf dem Zahlenstrahl: ausgefüllt oder offen am Rand?"],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Nach Definition 3.85: „$<$“ schließt den Randpunkt aus (rund), „$\\le$“ ein (eckig); $\\pm\\infty$ gehört nie dazu."}


# ── Seite 4: Satz 3.86 und 3.87 ──────────────────────────────────────────
k.erklaerung("Satz 3.86 und Satz 3.87", r"""
## ℚ liegt dicht, und Wurzeln existieren

**Satz 3.86 (ohne Beweis).** Für alle $x, y \in \mathbb{R}$ mit $x < y$ gibt es $q \in \mathbb{Q}$ mit $x < q < y$. Man sagt: $\mathbb{Q}$ liegt [[dicht]] in $\mathbb{R}$.

**Satz 3.87 (ohne Beweis).** Für $a \in [0, \infty)$ und $n \in \mathbb{N}\setminus\{0\}$ hat $x^n = a$ **genau eine** Lösung $x \in [0, \infty)$.

Satz 3.87 folgt aus der Vollständigkeit: Die Lösung von $x^2 = 2$ ist $\sup S$.

:::rechnung Satz 3.86 an $x = \frac13$, $y = \frac12$
(1/3 + 1/2)/2 = 5/12 || der Mittelwert ist rational und liegt dazwischen
1/3 < 5/12 || $4 < 5$: $\frac13 = \frac4{12} < \frac5{12}$
5/12 < 1/2 || $5 < 6$: also $\frac13 < \frac5{12} < \frac12$
:::

:::achtung Dicht heißt nicht gleich
Zwischen je zwei reellen Zahlen liegt eine rationale, aber $\mathbb{Q} \ne \mathbb{R}$: $\sqrt{2} \notin \mathbb{Q}$. Auch zwischen je zwei rationalen Zahlen liegt eine irrationale.
:::

:::alt Als Pixel
Stell dir vor, du zoomst beliebig weit in die Zahlengerade. In jedem noch so kleinen Ausschnitt findest du einen Bruch. Trotzdem fehlen auf der Geraden Punkte wie $\sqrt{2}$, die erst die Vollständigkeit liefert.
:::
""")

k.mc("Welche Aussage folgt aus Satz 3.86?",
     ["Zwischen $\\sqrt{2}$ und $\\sqrt{3}$ liegt eine rationale Zahl", "$\\mathbb{Q} = \\mathbb{R}$", "Zwischen $0$ und $1$ liegt keine irrationale Zahl", "$\\sqrt{2}$ ist rational, weil es beliebig gut angenähert wird"],
     "Satz 3.86 gilt für alle reellen $x < y$, also auch für $\\sqrt{2} < \\sqrt{3}$: Es gibt ein $q \\in \\mathbb{Q}$ dazwischen, zum Beispiel $\\frac{3}{2}$. Dichte macht $\\mathbb{Q}$ aber nicht gleich $\\mathbb{R}$.",
     tipps=["Satz 3.86 braucht nur $x < y$ in $\\mathbb{R}$.", "Dicht heißt „beliebig nah“, nicht „gleich“."],
     fehler={"$\\mathbb{Q} = \\mathbb{R}$": "Dicht bedeutet nicht gleich: $\\sqrt{2} \\in \\mathbb{R} \\setminus \\mathbb{Q}$.",
             "Zwischen $0$ und $1$ liegt keine irrationale Zahl": "$\\frac{\\sqrt{2}}{2}$ liegt zwischen $0$ und $1$ und ist irrational.",
             "$\\sqrt{2}$ ist rational, weil es beliebig gut angenähert wird": "Gute Näherung heißt nicht, dass die Zahl rational ist. $\\sqrt{2}$ ist irrational."})

# ── Seite 5: Wurzeln und rationale Potenzen ──────────────────────────────
k.erklaerung("Definition 3.88 und 3.89: n-te Wurzel, rationale Potenz", r"""
## Mit Brüchen potenzieren

**Definition 3.88.** Für $a \in [0, \infty)$ und $n \in \mathbb{N}\setminus\{0\}$ ist $\sqrt[n]{a} := x$, wobei $x \in [0, \infty)$ die eindeutige Lösung von $x^n = a$ ist (Satz 3.87).

**Definition 3.89.** Für $a \in (0, \infty)$ und $q = \frac mn \in \mathbb{Q}$ ($m \in \mathbb{Z}$, $n \in \mathbb{N}\setminus\{0\}$) ist $a^q := \sqrt[n]{a^m}$.

**Satz 3.90.** Das hängt nicht von der Darstellung $q = \frac mn$ ab, und es gelten $a^{p+q} = a^p a^q$, $(a^p)^q = a^{pq}$, $(ab)^q = a^q b^q$.

:::rechnung Beispiel 3.91
16^3 = 4096 || $m = 3$: erst $a^m$
8^4 = 4096 || $\sqrt[4]{4096} = 8$, denn $8^4 = 4096$: also $16^{3/4} = 8$
16^{-1} = 1/16 || $m = -1$, $n = 2$: $16^{-1/2} = \sqrt{16^{-1}}$
(1/4)^2 = 1/16 || $\sqrt{\frac1{16}} = \frac14$: also $16^{-1/2} = \frac14$
:::

:::achtung Nur die nichtnegative Lösung
$\sqrt{4} = 2$, **nicht** $\pm 2$. Die Gleichung $x^2 = 4$ hat zwei Lösungen, aber $\sqrt{4}$ ist die eine nichtnegative.
:::

:::alt Als Zwei-Schritt-Rezept
$a^{m/n}$: Erst die Zähler-Potenz $a^m$, dann die $n$-te Wurzel. Oder erst die Wurzel, dann die Potenz: dasselbe Ergebnis. Bei negativem $m$ steht der Kehrwert.
:::
""")


def rationale_potenz(rng):
    n = rng.choice([2, 3, 4])
    kand = [2, 3, 4, 5, F(2, 3), F(3, 2), F(1, 2), F(3, 4)]
    b = F(rng.choice([x for x in kand if x ** n < 700]))
    m = rng.choice([x for x in (-3, -2, -1, 1, 2, 3, 4, 5) if x % n != 0])
    a = b ** n
    w = b ** m
    falsch = [(b ** (-m), "Das Vorzeichen des Exponenten wurde ignoriert: Ein negativer Exponent bedeutet den Kehrwert."),
              (b * m, "Du hast die Wurzel mit $m$ multipliziert. Richtig ist: Wurzel ziehen, dann mit $m$ potenzieren."),
              (a ** m, "Du hast nur mit dem Zähler $m$ potenziert. Danach muss noch die $n$-te Wurzel gezogen werden."),
              (b ** (m * n) if abs(m * n) <= 8 else a, "Du hast mit $m$ und $n$ multipliziert. $a^{m/n}$ bedeutet $m$ **durch** $n$.")]
    zeilen = [(f"({brtex(b)})^{{{n}}} = {brtex(a)}", f"Basis $a = {brtex(a)}$ ist $({brtex(b)})^{n}$: also $\\sqrt[{n}]{{a}} = {brtex(b)}$"),
              ((f"({brtex(b)})^{{{m}}} = {brtex(w)}" if m > 0 else f"({brtex(1 / b)})^{{{-m}}} = {brtex(w)}"),
               f"$a^{{{m}/{n}}} = ({brtex(b)})^{{{m}}} = {brtex(w)}$" + ("" if m > 0 else " (negativer Exponent: Kehrwert)"))]
    return {"frage": f"Berechne $\\left({brtex(a)}\\right)^{{{m}/{n}}}$ (Definition 3.89). Gib das Ergebnis als gekürzten Bruch oder als ganze Zahl an.",
            "loesung": w, "gekuerzt": True,
            "tipps": [f"Schreibe ${brtex(a)}$ als Potenz: ${brtex(a)} = x^{{{n}}}$.", f"Dann ist $\\sqrt[{n}]{{{brtex(a)}}} = x$ mit $x = {brtex(b)}$.", f"Jetzt $x^{{{m}}}$ berechnen, bei negativem Exponenten mit Kehrwert."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": f"$a^{{m/n}} = \\sqrt[n]{{a^m}} = (\\sqrt[n]{{a}})^m$ (Def. 3.89, Satz 3.90). Hier ist $\\sqrt[{n}]{{a}} = {brtex(b)}$.",
            "typische_fehler": ohne_gleiche(w, falsch)}


k.zahl("Berechne $\\sqrt[3]{27} + \\sqrt[4]{16}$ (Definition 3.88).", 3 + 2,
       "$3^3 = 27$ und $2^4 = 16$, beide Wurzeln sind nichtnegativ: $3 + 2 = 5$.",
       tipps=["Welche nichtnegative Zahl hoch $3$ ergibt $27$?", "Welche hoch $4$ ergibt $16$?", "$3 + 2$."],
       rechenweg=rechnung([("3^3 = 27", "also $\\sqrt[3]{27} = 3$"), ("2^4 = 16", "also $\\sqrt[4]{16} = 2$"), ("3 + 2 = 5", "Summe")]),
       typische_fehler=[(3 + 4, "$\\sqrt[4]{16} = 2$, nicht $4$: Gesucht ist die Zahl, deren **vierte** Potenz $16$ ist."),
                        (9 + 4, "Wurzel ziehen heißt nicht durch $n$ teilen: $\\sqrt[3]{27} = 3$, nicht $9$.")])

k.zahl("Berechne $8^{2/3}$ (Definition 3.89).", 4,
       "$8^{2/3} = \\sqrt[3]{8^2} = \\sqrt[3]{64} = 4$. Oder $(\\sqrt[3]{8})^2 = 2^2 = 4$.",
       tipps=["$\\frac23$ heißt: $m = 2$, $n = 3$.", "$\\sqrt[3]{8} = 2$.", "Jetzt mit $2$ potenzieren."],
       rechenweg=rechnung([("2^3 = 8", "$\\sqrt[3]{8} = 2$"), ("2^2 = 4", "$m = 2$: also $8^{2/3} = 4$")]),
       typische_fehler=[(F(16, 3), "$8^{2/3}$ ist nicht $\\frac{8^2}{3}$. Der Nenner $3$ bedeutet die dritte Wurzel."),
                        (2, "Das ist nur $\\sqrt[3]{8} = 2$. Danach muss noch mit $m = 2$ potenziert werden.")])

# ── Seite 6: Betrag ──────────────────────────────────────────────────────
k.erklaerung("Definition 3.92 und Satz 3.93: Der Betrag", r"""
## Abstand zur Null

**Definition 3.92.** $|x| := x$ für $x \ge 0$ und $|x| := -x$ für $x < 0$ (Betragsfunktion).

**Satz 3.93.** Für alle $x, y \in \mathbb{R}$ gilt
$$|x| \ge 0,\quad |x| = |-x| = \sqrt{x^2},\quad -|x| \le x \le |x|,\quad |xy| = |x||y|,\quad |x| = 0 \Leftrightarrow x = 0,\quad |x + y| \le |x| + |y|.$$
Die letzte Ungleichung heißt [[Dreiecksungleichung]].

*Beweis der Produktregel.* $|xy|$ und $|x||y|$ sind nichtnegativ, und $|xy|^2 = (xy)^2 = x^2y^2 = |x|^2|y|^2 = (|x||y|)^2$. Nach der Eindeutigkeit der nichtnegativen Quadratwurzel (Satz 3.87) sind sie gleich.

:::rechnung Mit $x = -3$, $y = 4$
|(-3) \cdot 4| = 12 || $|xy| = |{-12}| = 12$
|-3| \cdot |4| = 12 || $|x||y| = 3 \cdot 4$: gleich
\sqrt{(-3)^2} = 3 || $\sqrt{x^2} = |x|$, nicht $x$ (das wäre $-3$)
:::

:::achtung Wurzel aus Quadrat ist der Betrag
$\sqrt{x^2} = |x|$, **nicht** $x$. Für $x = -3$ ist $\sqrt{9} = 3$.
:::

:::alt Als Entfernung
$|x - y|$ ist der Abstand zweier Zahlen auf der Geraden, egal in welche Richtung. Der Betrag vergisst das Vorzeichen und behält die Größe.
:::
""")

k.luecke("Beweis der Produktregel an $x = -3$, $y = 4$: $|xy|^2 = (xy)^2 = (-12)^2 = \\luecke = 9 \\cdot \\luecke = |x|^2 \\cdot |y|^2$.",
         "(xy)^2 = (-12)^2 = \\luecke = 9 \\cdot \\luecke",
         [[144], [16]],
         "$(-12)^2 = 144$ und $|x|^2 = 9$, $|y|^2 = 16$: $9 \\cdot 16 = 144$. Beide Seiten sind nichtnegativ und haben dasselbe Quadrat, also sind sie gleich.",
         tipps=["Quadriere $-12$.", "$|y|^2 = 4^2$.", "Die Lücken sind $144$ und $16$."],
         rechenweg=rechnung([("(-12)^2 = 144", "Quadrat des Produkts"), ("9 \\cdot 16 = 144", "Produkt der Quadrate: gleich")]),
         typische_fehler=[([-144, 16], "Ein Quadrat ist nie negativ: $(-12)^2 = +144$.")])

k.wf("Für alle $x \\in \\mathbb{R}$ gilt $\\sqrt{x^2} = x$.", False,
     "Es gilt $\\sqrt{x^2} = |x|$ (Satz 3.93). Für $x = -3$: $\\sqrt{9} = 3 \\ne -3$.",
     tipps=["Setze $x = -3$ ein."])

# ── Seite 7: Dreiecksungleichung ─────────────────────────────────────────
k.erklaerung("Die Dreiecksungleichung", r"""
## |x + y| ≤ |x| + |y|

Anschaulich: Der Weg von $0$ nach $x + y$ ist nie länger als erst $|x|$ und dann $|y|$ zu laufen. Gleichheit gilt, wenn beide in dieselbe Richtung gehen.

*Beweis.* Aus $-|x| \le x \le |x|$ und $-|y| \le y \le |y|$ folgt durch Addition
$$x + y \le |x| + |y| \quad\text{und}\quad -(x + y) \le |x| + |y|.$$
Da $|x + y|$ je nach Vorzeichen gleich $x + y$ oder $-(x + y)$ ist, folgt $|x + y| \le |x| + |y|$. $\square$

:::rechnung Dreiecksungleichung an Zahlen
|3 + (-5)| = 2 || $|x + y|$ mit $x = 3$, $y = -5$
|3| + |-5| = 8 || $|x| + |y|$: $2 \le 8$ (strikt, da verschiedene Vorzeichen)
|3 + 5| = 8 || gleiche Vorzeichen: $|x + y| = 8$
|3| + |5| = 8 || $8 = 8$: Gleichheit
:::

:::alt Als Umweg
Erst nach rechts, dann nach links: Du läufst viel, kommst aber nur wenig voran ($2$ von $8$). In dieselbe Richtung gibt es keinen Umweg, und beide Längen sind gleich.
:::
""")

k.ordnen("Ordne den Beweis der Dreiecksungleichung $|x + y| \\le |x| + |y|$ (Satz 3.93).",
         ["Nach Satz 3.93 gilt $-|x| \\le x \\le |x|$ und $-|y| \\le y \\le |y|$.",
          "Addition der beiden rechten Ungleichungen ergibt $x + y \\le |x| + |y|$.",
          "Addition der beiden linken Ungleichungen ergibt $-|x| - |y| \\le x + y$, also $-(x + y) \\le |x| + |y|$.",
          "Nach Definition ist $|x + y|$ gleich $x + y$ oder gleich $-(x + y)$.",
          "In beiden Fällen ist $|x + y| \\le |x| + |y|$. $\\square$"],
         "Beide möglichen Werte von $|x + y|$ ($x + y$ und $-(x + y)$) liegen unter $|x| + |y|$, also auch $|x + y|$.",
         ablenker=["Quadrieren gibt $|x + y|^2 = |x|^2 + |y|^2$, also Gleichheit.", "Da $|x| \\ge x$, folgt $|x| + |y| = |x + y|$."],
         tipps=["Starte mit den Schranken $-|x| \\le x \\le |x|$ für beide Zahlen.", "Addiere die Ungleichungen getrennt: rechte mit rechten, linke mit linken.", "Der Betrag ist eine Fallunterscheidung: $x + y$ oder $-(x + y)$."])

k.mc("Für welche Zahlen gilt in $|x + y| \\le |x| + |y|$ Gleichheit?",
     ["$x = 2$, $y = 5$", "$x = 2$, $y = -5$", "$x = -2$, $y = 5$", "Nie: es gilt immer strikt „$<$“"],
     "Gleichheit gilt genau dann, wenn $x$ und $y$ dasselbe Vorzeichen haben (oder eine der Zahlen $0$ ist). $2 + 5 = 7 = |2| + |5|$. Bei $2$ und $-5$ gilt $3 < 7$.",
     tipps=["Rechne links und rechts aus.", "Wann heben sich die Beträge teilweise weg?"],
     fehler={"$x = 2$, $y = -5$": "$|2 + (-5)| = 3 < 7 = |2| + |-5|$: strikt.",
             "$x = -2$, $y = 5$": "$|-2 + 5| = 3 < 7$: strikt.",
             "Nie: es gilt immer strikt „$<$“": "Bei gleichen Vorzeichen gilt Gleichheit, zum Beispiel $|2 + 5| = |2| + |5|$."})

k.praxis()


def sup_intervall(rng):
    a = rng.randint(-5, 3)
    b = a + rng.randint(2, 7)
    lo, ro = rng.random() < 0.5, rng.random() < 0.5
    iv = _ivtex(a, b, lo, ro)
    korrekt = f"$\\sup A = {b}$ und $A$ hat ein Maximum ($\\max A = {b}$)" if not ro else f"$\\sup A = {b}$, aber $A$ hat kein Maximum"
    pool = [f"$\\sup A = {b}$ und $A$ hat ein Maximum ($\\max A = {b}$)", f"$\\sup A = {b}$, aber $A$ hat kein Maximum",
            f"$\\sup A = {a}$", f"$A$ hat kein Supremum in $\\mathbb{{R}}$, weil $A$ nicht abgeschlossen ist"]
    optionen = [korrekt] + [o for o in pool if o != korrekt]
    fehler = {pool[0]: f"Das Maximum müsste in $A$ liegen. Bei $A = {iv}$ gehört ${b}$ nicht dazu: kein Maximum, aber ${b}$ ist die kleinste obere Schranke.",
              pool[1]: f"${b}$ liegt in $A = {iv}$ und ist deshalb ein Maximum.",
              pool[2]: f"${a}$ ist das untere Ende. Das Supremum ist die **kleinste obere** Schranke ${b}$.",
              pool[3]: "Nach R2 hat jede nichtleere, nach oben beschränkte Menge ein Supremum, ob offen oder nicht."}
    fehler = {o: fehler[o] for o in optionen[1:]}
    return {"typ": "mc",
            "frage": f"Sei $A = {iv} \\subseteq \\mathbb{{R}}$. Welche Aussage über Supremum und Maximum stimmt?",
            "optionen": optionen, "fehler": fehler,
            "tipps": ["Das Supremum ist die kleinste obere Schranke. Wo liegt sie?", "Ein Maximum muss selbst Element der Menge sein. Gehört der rechte Randpunkt dazu?", "Nach R2 existiert das Supremum immer, wenn $A \\ne \\emptyset$ nach oben beschränkt ist."],
            "rechenweg": rechnung([("\\text{Rechter Rand}", f"${b}$ gehört {'nicht ' if ro else ''}zu $A$: {'kein Maximum' if ro else 'Maximum'}")]),
            "erklaerung": "Das Supremum existiert nach R2. Es ist ein Maximum, wenn es zur Menge gehört, sonst nicht (offene Intervallenden)."}


def betrag_dreieck(rng):
    while True:
        x, y = F(rng.randint(-9, 9), rng.choice([1, 1, 2])), F(rng.randint(-9, 9), rng.choice([1, 1, 2]))
        if x != 0 and y != 0 and (x > 0) != (y > 0):
            break
    w = abs(x) + abs(y) - abs(x + y)
    falsch = [(abs(x + y) - abs(x) - abs(y), "Das Vorzeichen ist vertauscht: Nach der Dreiecksungleichung ist $|x| + |y| - |x + y| \\ge 0$."),
              (abs(x) + abs(y), "Das ist nur $|x| + |y|$. Davon muss noch $|x + y|$ abgezogen werden."),
              (abs(x) - abs(y) - abs(x + y), "Beide Beträge werden addiert: $|x| + |y|$, nicht $|x| - |y|$.")]
    zeilen = [(f"|{brtex(x)}| + |{brtex(y)}| = {brtex(abs(x) + abs(y))}", "Summe der Beträge"), (f"|{brtex(x)} + ({brtex(y)})| = {brtex(abs(x + y))}", "Betrag der Summe"),
              (f"{brtex(abs(x) + abs(y))} - {brtex(abs(x + y))} = {brtex(w)}", "Differenz (nie negativ)")]
    return {"frage": f"Berechne $|x| + |y| - |x + y|$ für $x = {brtex(x)}$ und $y = {brtex(y)}$ (Dreiecksungleichung). Gib das Ergebnis als gekürzten Bruch oder ganze Zahl an.",
            "loesung": w, "gekuerzt": True,
            "tipps": ["Berechne zuerst $|x|$, $|y|$ und $x + y$.", "Beachte: Beträge sind nie negativ.", f"$|x + y| = {brtex(abs(x + y))}$."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Das Ergebnis ist immer $\\ge 0$ (Dreiecksungleichung). Es ist $0$ genau dann, wenn $x$ und $y$ dasselbe Vorzeichen haben.",
            "typische_fehler": ohne_gleiche(w, falsch)}


k.generator(intervall_notation, typ="mc", titel="Intervallschreibweise")
k.generator(sup_intervall, typ="mc", titel="Supremum und Maximum von Intervallen")
k.generator(rationale_potenz, typ="zahl", titel="Rationale Potenzen", glatt=False)
k.generator(betrag_dreieck, typ="zahl", titel="Betrag und Dreiecksungleichung")

k.rechenweg_aufgabe(r"""
## Quiz-Stil: Reelle Zahlen und Betrag

Sei $A = \{x \in \mathbb{R} \mid -2 \le x < 3\}$.
""",
    [{"typ": "mc", "frage": "Wie schreibt man $A$ als Intervall?", "optionen": ["$[-2, 3)$", "$(-2, 3)$", "$[-2, 3]$", "$(-2, 3]$"],
      "fehler": {"$(-2, 3)$": "Wegen $-2 \\le x$ gehört $-2$ zu $A$: eckige Klammer links.", "$[-2, 3]$": "Wegen $x < 3$ gehört $3$ nicht zu $A$: runde Klammer rechts.",
                 "$(-2, 3]$": "Beide Klammern sind vertauscht."},
      "tipps": ["„$\\le$“ eckig, „$<$“ rund.", "Links steht $\\le$."], "erklaerung": "$-2 \\le x$: eckig, $x < 3$: rund."},
     {"typ": "zahl", "frage": "Bestimmen Sie $\\sup A$.", "loesung": 3,
      "tipps": ["Die kleinste obere Schranke.", "Gehört $3$ zu $A$?"], "erklaerung": "$\\sup A = 3 \\notin A$, also kein Maximum.",
      "typische_fehler": [(-2, "$-2$ ist das Infimum (und Minimum) von $A$.")], "rechenweg": ":::rechnung\n3 - 0 = 3 || $3$ ist die kleinste obere Schranke\n:::"},
     {"typ": "wf", "frage": "$A$ hat ein Maximum.", "wahr": False, "tipps": ["Ein Maximum muss in $A$ liegen."],
      "erklaerung": "Für jedes $x \\in A$ ist $\\frac{x + 3}{2} \\in A$ und größer als $x$ (Mittelwert): Es gibt kein größtes Element."}],
    "$A = [-2, 3)$ hat $\\min A = \\inf A = -2$, aber nur $\\sup A = 3$ ohne Maximum.",
    uebungsblatt=True,
    tipps=["Nach R2 hat $A$ ein Supremum.", "Das Maximum wäre ein größtes Element von $A$."],
    rechenweg=r"""
:::rechnung
-2 \le x || linkes Ende gehört dazu
x < 3 || rechtes Ende gehört nicht dazu
(x + 3)/2 = x + (3 - x)/2 || Mittelwert von $x$ und $3$ liegt strikt zwischen beiden
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Betragsregeln

Zeigen Sie für alle $x, y \in \mathbb{R}$ mit Satz 3.93:

1. $\big||x| - |y|\big| \le |x - y|$ (umgekehrte Dreiecksungleichung).
2. $|x| = \sqrt{x^2}$.
""",
    r"""
**1.** Es gilt $|x| = |(x - y) + y| \le |x - y| + |y|$ (Dreiecksungleichung), also $|x| - |y| \le |x - y|$. Vertauscht man $x$ und $y$, so ist $|y| - |x| \le |y - x| = |x - y|$ (Satz 3.93, $|z| = |-z|$).
Zusammen liegen $|x| - |y|$ und $-(|x| - |y|) = |y| - |x|$ beide unter $|x - y|$, also $\big||x| - |y|\big| \le |x - y|$.
**2.** $|x| \ge 0$ und $|x|^2 = x^2$ (für $x \ge 0$: $x^2 = x^2$, für $x < 0$: $(-x)^2 = x^2$). Nach der Eindeutigkeit der nichtnegativen Lösung von $t^2 = x^2$ (Satz 3.87) ist $|x| = \sqrt{x^2}$. $\square$
""",
    ["Bei (1) $x = (x - y) + y$ geschrieben und die Dreiecksungleichung angewendet",
     "Beide Richtungen ($|x| - |y|$ und $|y| - |x|$) abgeschätzt",
     "Bei (2) gezeigt, dass $|x|$ nichtnegativ ist und $|x|^2 = x^2$ erfüllt",
     "Bei (2) die Eindeutigkeit aus Satz 3.87 genannt"],
    "Die umgekehrte Dreiecksungleichung folgt aus der normalen, wenn man $x = (x - y) + y$ schreibt. Der Betrag ist die nichtnegative Wurzel des Quadrats.",
    uebungsblatt=True,
    tipps=["Schreibe $x$ als Summe zweier Terme, auf die du die Dreiecksungleichung anwenden kannst.", "Für (2) brauchst du zwei Eigenschaften: nichtnegativ und gleiches Quadrat."])

k.papier(r"""
## Übungsblatt-Stil: Eine Lücke in ℚ

Sei $S = \{t \in \mathbb{Q} \mid t \ge 0,\ t^2 < 2\}$. Zeigen Sie: Zu jeder rationalen oberen Schranke $u > 0$ von $S$ mit $u^2 > 2$ gibt es eine kleinere rationale obere Schranke $v$ mit $v^2 > 2$.
(Hinweis: $v := \frac12(u + \frac2u)$.)
""",
    r"""
$v = \frac12(u + \frac2u) \in \mathbb{Q}$ und $v > 0$. Aus $u^2 > 2$ folgt $\frac2u < u$, also $v < \frac12(u + u) = u$.
Außerdem $v^2 - 2 = \frac14(u + \frac2u)^2 - 2 = \frac14(u - \frac2u)^2 > 0$, denn $u \ne \frac2u$ (sonst $u^2 = 2$, aber $u^2 > 2$). Also $v^2 > 2$.
Ist $t \in S$, so ist $t^2 < 2 < v^2$ und $t, v \ge 0$, daher $t < v$: $v$ ist obere Schranke von $S$. Damit gibt es keine kleinste rationale obere Schranke. $\square$
""",
    ["$v$ als rational und positiv erkannt",
     "$v < u$ aus $\\frac2u < u$ gefolgert",
     "$v^2 > 2$ durch Ausrechnen von $v^2 - 2$ gezeigt",
     "Gezeigt, dass $v$ obere Schranke von $S$ ist (aus $t^2 < 2 < v^2$)"],
    "So sieht man, dass $\\mathbb{Q}$ nicht vollständig ist: Die Menge $S$ hat obere Schranken, aber keine kleinste.",
    uebungsblatt=True,
    tipps=["Wieso ist $\\frac2u < u$?", "Berechne $v^2 - 2$ und wende die binomische Formel auf $(u - \\frac2u)^2$ an."])

k.zusammenfassung(r"""
## Die reellen Zahlen (Skript Abschn. 3.6, Def. 3.80 bis Satz 3.93)

- **Lücke in ℚ:** $S = \{t \in \mathbb{Q} \mid t \ge 0,\ t^2 < 2\}$ hat obere Schranken, aber kein rationales Supremum.
- **Axiome** (Def. 3.80): R1 angeordneter Körper, R2 Vollständigkeit: Jede nichtleere, nach oben beschränkte Menge hat ein Supremum. Beob. 3.81: nach unten beschränkt $\Rightarrow$ Infimum, $\inf A = -\sup(-A)$. Satz 3.82: Je zwei vollständige angeordnete Körper sind eindeutig isomorph.
- **Intervalle** (Def. 3.85): $(a, b)$ offen, $[a, b]$ abgeschlossen, $(a, b]$, $[a, b)$ halboffen, $(a, \infty)$ usw. $\pm\infty$ sind keine Zahlen.
- **Satz 3.86:** ℚ liegt dicht in ℝ. **Satz 3.87:** $x^n = a$ hat genau eine Lösung in $[0, \infty)$.
- **Wurzel** (Def. 3.88) $\sqrt[n]{a}$ = diese Lösung; **rationale Potenz** (Def. 3.89) $a^{m/n} = \sqrt[n]{a^m}$, Potenzgesetze (Satz 3.90), $16^{3/4} = 8$, $16^{-1/2} = \frac14$.
- **Betrag** (Def. 3.92, Satz 3.93): $|x| = \sqrt{x^2}$, $|xy| = |x||y|$, $-|x| \le x \le |x|$, **Dreiecksungleichung** $|x + y| \le |x| + |y|$.

!! $\sqrt{x^2} = |x|$, und $\sqrt{4} = 2$ (nicht $\pm 2$).
""")
