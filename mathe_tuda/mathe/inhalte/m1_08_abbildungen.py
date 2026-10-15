# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 8: Abbildungen (Skript Disser WS 26/27, Abschn. 1.7, Def. 1.66 bis Satz 1.82)."""
from itertools import product

from ..engine import neues_kapitel

k = neues_kapitel(
    slug="uni_abbildungen",
    titel="Abbildungen",
    beschreibung="Abbildung als eindeutige Relation, Bild und Urbild, injektiv, surjektiv, bijektiv, Verkettung, Umkehrabbildung, Einschränkung",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 1.7",
    icon="🎯")


# ── Hilfsfunktionen: Python rechnet alles an endlichen Abbildungen ────────
def ist_abb(X, R):
    return all(sum(1 for a, _ in R if a == x) == 1 for x in X)


def als_dict(R):
    return {a: b for a, b in R}


def bild(f, A):
    return {f[x] for x in A}


def urbild(f, X, B):
    return {x for x in X if f[x] in B}


def ist_inj(f):
    return len(set(f.values())) == len(f)


def ist_sur(f, Y):
    return set(f.values()) == set(Y)


def mtext(s):
    return "{" + "; ".join(str(x) for x in sorted(s)) + "}"


def mtex(s):
    return "\\emptyset" if not s else "\\{" + ", ".join(str(x) for x in sorted(s)) + "\\}"


def paare_tex(R):
    return "\\{" + ", ".join(f"({a}, {b})" for a, b in sorted(R, key=lambda p: (str(p[0]), str(p[1])))) + "\\}"


def rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


# Beispiel 1.67 nachrechnen
_X3, _Y3 = ["a", "b", "c"], [1, 2, 3]
_B67 = [{("a", 1), ("a", 2), ("b", 3), ("c", 3)}, {("a", 1), ("b", 3)}, {("a", 2), ("b", 2), ("c", 2)},
        {("a", 2), ("b", 3), ("c", 1)}]
assert [ist_abb(_X3, r) for r in _B67] == [False, False, True, True]
# Abbildung 1.6: eine Abbildung je Eigenschaft
_F_BIJ = {"a": 2, "b": 3, "c": 1}
_F_SUR = {"a": 1, "b": 2, "c": 2}
_F_INJ = {"a": 1, "b": 3}
_F_WED = {"a": 1, "b": 1, "c": 3}
assert (ist_inj(_F_BIJ), ist_sur(_F_BIJ, _Y3)) == (True, True)
assert (ist_inj(_F_SUR), ist_sur(_F_SUR, [1, 2])) == (False, True)
assert (ist_inj(_F_INJ), ist_sur(_F_INJ, _Y3)) == (True, False)
assert (ist_inj(_F_WED), ist_sur(_F_WED, _Y3)) == (False, False)
# Bild/Urbild (Bsp. in Def. 1.69): f: {0..5} -> {0..3}, x -> x mod 3
_X6, _Y4 = list(range(6)), [0, 1, 2, 3]
_FM = {x: x % 3 for x in _X6}
assert bild(_FM, _X6) == {0, 1, 2} and urbild(_FM, _X6, {1}) == {1, 4} and urbild(_FM, _X6, _Y4) == set(_X6)
assert urbild(_FM, _X6, {3}) == set()
# Beispiel 1.72
assert {2 * a for a in (0, 1, 2)} == {0, 2, 4}
assert {a + b for a in (0, 1) for b in (0, 2)} == {0, 1, 2, 3}
# Beispiel 1.67/1.68: kanonische Abbildung zur Parität
_M5 = [-1, 1, 2, 3, 4]
_NU = {x: frozenset(y for y in _M5 if y % 2 == x % 2) for x in _M5}
assert _NU[1] == frozenset({-1, 1, 3}) and _NU[4] == frozenset({2, 4})
# Beispiel 1.78 und 1.81 (endlicher Ausschnitt)
assert 2 not in {z * z for z in range(-50, 51)} and (-1) ** 2 == 1 ** 2
# Satz 1.82 (iii),(iv) an einem Beispiel
_f1, _g1 = {1: "a", 2: "b"}, {3: "c", 4: "d"}
_h1 = {**_f1, **_g1}
assert ist_inj(_h1) and ist_sur(_h1, ["a", "b", "c", "d"])
_p1 = {(x, y): (_f1[x], _g1[y]) for x in _f1 for y in _g1}
assert ist_inj(_p1) and ist_sur(_p1, list(product(["a", "b"], ["c", "d"])))

k.lernziele([
    "Ich kann entscheiden, ob eine Relation $f \\subseteq X \\times Y$ eine Abbildung ist, und schreibe Abbildungen als $f\\colon X \\to Y,\\ x \\mapsto f(x)$ (Def. 1.66, Bsp. 1.67, 1.68)",
    "Ich kann Bild $f(A)$ und Urbild $f^{-1}(B)$ bestimmen und die Schreibweise $\\{g(a) \\mid a \\in A\\}$ lesen (Def. 1.69, 1.71, Beob. 1.70)",
    "Ich kann injektiv, surjektiv und bijektiv nachweisen oder mit einem Gegenbeispiel widerlegen (Def. 1.73, Satz 1.74)",
    "Ich kann Abbildungen verketten, Umkehrabbildungen bestimmen und Einschränkungen nutzen (Def. 1.75 bis 1.80, Sätze 1.76, 1.79, 1.82)",
])

k.warum(r"""
Jede Funktion in deinem Code ist eine Abbildung: Der Typ des Parameters ist $X$, der Rückgabetyp
$Y$. Ob eine Funktion injektiv ist, entscheidet, ob ein Hash kollisionsfrei ist. Bijektiv heißt
verlustfrei umkehrbar: Verschlüsselung, Kompression ohne Verlust und Zeichenkodierung müssen
bijektiv auf ihrem Bild sein. Verkettung ist Funktionskomposition, und die Frage „Ist `decode(encode(x)) == x`?“
ist Satz 1.76. Im Vorkurs hast du Funktionen im Schulstil kennengelernt, hier werden sie streng als Relationen definiert.
""")

# ── Seite 1: Definition 1.66 ─────────────────────────────────────────────
k.erklaerung("Abbildung als Relation", r"""
## Definition 1.66

Im Vorkurs-Kapitel „Funktionen, Bild und Urbild“ hast du Funktionen $f\colon D \to W$ geschrieben.
Jetzt kommt die strenge Version: Eine Abbildung ist eine [[Relation]], die **eindeutig** ist.

**Definition 1.66.** Eine [[Abbildung]] ist eine Relation $f \subseteq X \times Y$, so dass es für jedes
$x \in X$ **genau ein** $f(x) \in Y$ gibt mit $(x, f(x)) \in f$. Man schreibt
$f\colon X \to Y,\ x \mapsto f(x)$ mit Definitionsmenge $X$ und Zielmenge $Y$. Die Vorschrift darf
unspezifiziert bleiben. Abbildungen zwischen Zahlenräumen heißen auch Funktionen.

:::visual relation_graph
{"links": ["a", "b", "c"], "rechts": [1, 2, 3], "pfeile": [["a", 2], ["b", 3], ["c", 1]],
 "namen": ["X", "Y"], "zeige": ["abbildung"],
 "unterschrift": "$f = \\{(a, 2), (b, 3), (c, 1)\\}$: Von jedem Element links geht genau ein Pfeil aus."}
:::

Eine Abbildung $\star\colon X \times X \to X$ heißt (binäre) [[Verknüpfung]] auf $X$. Man schreibt
$x \star y := \star(x, y)$, wie bei $3 + 4$.

:::alt Als Automat
Ein Automat bekommt aus $X$ eine Eingabe und muss **immer** genau eine Ausgabe aus $Y$ liefern. Nie keine
(Absturz), nie zwei (unentschlossen). Für die Ausgabe ist egal, wie die Maschine rechnet. Entscheidend ist
nur, wer welcher Ausgabe zugeordnet wird: eben die Menge der Paare $(x, f(x))$.
:::
""")

# ── Seite 2: Beispiel 1.67 ────────────────────────────────────────────────
k.erklaerung("Beispiel 1.67: Abbildung oder nicht?", r"""
## Pfeile zählen

Zwischen $\{a, b, c\}$ und $\{1, 2, 3\}$ betrachtet das Skript vier Relationen (Abbildung 1.5):

:::visual relation_graph
{"links": ["a", "b", "c"], "rechts": [1, 2, 3], "pfeile": [["a", 1], ["a", 2], ["b", 3], ["c", 3]],
 "namen": ["X", "Y"], "zeige": ["abbildung"],
 "unterschrift": "$a$ hat zwei Pfeile: keine Abbildung."}
:::

:::visual relation_graph
{"links": ["a", "b", "c"], "rechts": [1, 2, 3], "pfeile": [["a", 1], ["b", 3]],
 "namen": ["X", "Y"], "zeige": ["abbildung"],
 "unterschrift": "$c$ hat keinen Pfeil: keine Abbildung."}
:::

:::visual relation_graph
{"links": ["a", "b", "c"], "rechts": [1, 2, 3], "pfeile": [["a", 2], ["b", 2], ["c", 2]],
 "namen": ["X", "Y"], "zeige": ["abbildung"],
 "unterschrift": "Alle zeigen auf $2$: eine Abbildung (konstant)."}
:::

:::visual relation_graph
{"links": ["a", "b", "c"], "rechts": [1, 2, 3], "pfeile": [["a", 2], ["b", 3], ["c", 1]],
 "namen": ["X", "Y"], "zeige": ["abbildung"],
 "unterschrift": "Jedes Element links hat genau einen Pfeil: eine Abbildung."}
:::

:::achtung Rechts darf alles passieren
Gezählt wird nur an den Elementen **links**. Dass $2$ dreimal getroffen wird und $1$ und $3$ gar nicht,
stört bei einer Abbildung nicht (das betrifft erst injektiv und surjektiv).
:::

:::alt Als Zeugnis
Jede Schülerin (links) bekommt genau eine Note (rechts). Zwei Noten für eine Schülerin geht nicht, keine Note auch nicht.
Dass viele dieselbe Note bekommen oder manche Note nie vergeben wird, ist erlaubt.
:::
""")

k.zuordnen("Ordne jede Relation zwischen $\\{a, b, c\\}$ und $\\{1, 2, 3\\}$ ihrem Befund zu (Beispiel 1.67).",
           [("$\\{(a, 1), (a, 2), (b, 3), (c, 3)\\}$", "keine Abbildung: $a$ hat zwei Bilder"),
            ("$\\{(a, 1), (b, 3)\\}$", "keine Abbildung: $c$ hat kein Bild"),
            ("$\\{(a, 2), (b, 2), (c, 2)\\}$", "Abbildung (konstant)"),
            ("$\\{(a, 2), (b, 3), (c, 1)\\}$", "Abbildung (bijektiv)")],
           "Zähle die Paare je Element links: zwei, keines, je eines.",
           ablenker=["keine Abbildung: $2$ wird mehrfach getroffen"],
           tipps=["Zähle für jedes Element links, wie viele Paare mit ihm beginnen.",
                  "Mehrfach getroffene Elemente rechts sind kein Problem für die Abbildungseigenschaft."])

# ── Seite 3: Beispiel 1.68 ────────────────────────────────────────────────
k.erklaerung("Beispiel 1.68: wichtige Abbildungen", r"""
## Vier Standardbeispiele

Das Skript nennt vier Abbildungen, denen du ständig begegnest:

- Die **Identität** $\mathrm{id}_M\colon M \to M,\ x \mapsto x$ (kurz $\mathrm{id}$).
- **Addition und Multiplikation** $+, \cdot\colon Z \times Z \to Z$ für $Z \in \{\mathbb{N}, \mathbb{Z}, \mathbb{Q}, \mathbb{R}\}$: Verknüpfungen auf $Z$.
- **Polynome** $f\colon \mathbb{R} \to \mathbb{R},\ x \mapsto a_n x^n + \cdots + a_0$.
- Die **kanonische Abbildung** $\nu\colon M \to M/{\sim},\ x \mapsto [x]$ zu einer Äquivalenzrelation $\sim$.

:::rechnung Die kanonische Abbildung zur Parität auf $M = \{-1, 1, 2, 3, 4\}$
\nu(1) = [1] = \{-1, 1, 3\} || $1$ wird in seine Klasse geschickt
\nu(3) = [3] = \{-1, 1, 3\} || ein anderes Element, dieselbe Klasse
\nu(2) = \nu(4) = \{2, 4\} || die zweite Klasse
:::

Hier sehen wir: $\nu$ ist nicht injektiv ($\nu(1) = \nu(3)$) und immer surjektiv, denn jede Klasse $[a]$ ist das Bild von $a$.

:::alt Mit Etiketten
Die Identität klebt jedem Ding sein eigenes Etikett an. $\nu$ klebt jedem Ding das Etikett seiner Gruppe an:
Alle Ungeraden bekommen dasselbe Etikett. Damit ist $\nu$ eine Abbildung, aber nicht umkehrbar:
Vom Etikett „ungerade“ aus weißt du nicht mehr, welches der Dinge es war.
:::
""")

k.mehrfach("Welche der folgenden Zuordnungen sind Abbildungen?",
           ["$\\mathrm{id}_{\\mathbb{N}}\\colon \\mathbb{N} \\to \\mathbb{N},\\ x \\mapsto x$",
            "$+\\colon \\mathbb{Z} \\times \\mathbb{Z} \\to \\mathbb{Z},\\ (x, y) \\mapsto x + y$",
            "$f\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto 3x^2 - x + 5$"],
           ["$g\\colon \\mathbb{Z} \\to \\mathbb{Z},\\ x \\mapsto \\frac{x}{2}$",
            "$h\\colon \\mathbb{N} \\to \\mathbb{N},\\ x \\mapsto x - 1$",
            "$\\mathbb{Z} \\to \\mathbb{Z}$, $x \\mapsto$ „ein Teiler von $x$“"],
           "Bei $g$ liegt $\\frac12$ für $x = 1$ nicht in der Zielmenge $\\mathbb{Z}$, bei $h$ ist $0 - 1 = -1 \\notin \\mathbb{N}$. "
           "Bei „ein Teiler von $x$“ gibt es mehrere Kandidaten. Die Zielmenge gehört zur Abbildung: Der Wert muss **in $Y$ liegen**.",
           tipps=["Prüfe: Liegt für jedes $x$ der Definitionsmenge der Wert in der Zielmenge?", "Ist der Wert eindeutig?",
                  "Setze zum Testen $x = 0$ und $x = 1$ ein."],
           fehler={"$g\\colon \\mathbb{Z} \\to \\mathbb{Z},\\ x \\mapsto \\frac{x}{2}$": "$g(1) = \\frac12 \\notin \\mathbb{Z}$: Der Wert verlässt die Zielmenge.",
                   "$h\\colon \\mathbb{N} \\to \\mathbb{N},\\ x \\mapsto x - 1$": "Im Skript ist $0 \\in \\mathbb{N}$, und $h(0) = -1 \\notin \\mathbb{N}$.",
                   "$\\mathbb{Z} \\to \\mathbb{Z}$, $x \\mapsto$ „ein Teiler von $x$“": "$6$ hat die Teiler $1, 2, 3, 6$: nicht eindeutig."})

# ── Seite 4: Bild und Urbild ─────────────────────────────────────────────
k.erklaerung("Bild und Urbild", r"""
## Definition 1.69 und Beobachtung 1.70

Für $f\colon X \to Y$ gilt, wie im Vorkurs-Kapitel „Funktionen, Bild und Urbild“:

**Definition 1.69.**
(i) Das [[Bild]] von $A \subseteq X$ ist $f(A) := \{y \in Y \mid \exists x \in A : f(x) = y\}$.
(ii) Das [[Urbild]] von $B \subseteq Y$ ist $f^{-1}(B) := \{x \in X \mid f(x) \in B\}$.

**Beobachtung 1.70.** Es gilt $f^{-1}(Y) = X$, denn jedes $f(x)$ liegt in $Y$.
Dagegen gilt nur $f(X) \subseteq Y$, nicht immer Gleichheit.

:::rechnung $f\colon \{0, 1, 2, 3, 4, 5\} \to \{0, 1, 2, 3\},\ x \mapsto x \bmod 3$
0 \mapsto 0,\ 1 \mapsto 1,\ 2 \mapsto 2 || erste Hälfte
3 \mapsto 0,\ 4 \mapsto 1,\ 5 \mapsto 2 || zweite Hälfte: die Werte wiederholen sich
f(X) = \{0, 1, 2\} \neq \{0, 1, 2, 3\} || kein $x$ trifft die $3$: Bild kleiner als Zielmenge
f^{-1}(\{1\}) = \{1, 4\} || beide landen auf $1$
f^{-1}(\{3\}) = \emptyset || kein Urbild
:::

:::achtung $f^{-1}(B)$ braucht keine Umkehrabbildung
Das Urbild einer Menge gibt es für **jede** Abbildung. Eine Umkehrabbildung gibt es nur für bijektive Abbildungen (Satz 1.76).
:::

:::alt Mit einem Suchfilter
$f(A)$: „Welche Werte kommen heraus, wenn ich nur Eingaben aus $A$ erlaube?“ $f^{-1}(B)$:
„Welche Eingaben liefern einen Wert aus $B$?“ Das ist eine Datenbankabfrage rückwärts:
`SELECT x WHERE f(x) IN B`. Sie kann auch leer ausgehen.
:::
""")

k.wf("Für jede Abbildung $f\\colon X \\to Y$ gilt $f(X) = Y$.", False,
     "Beobachtung 1.70: Es gilt immer $f^{-1}(Y) = X$ und $f(X) \\subseteq Y$, aber nicht immer Gleichheit. "
     "Gleichheit $f(X) = Y$ ist genau die Surjektivität. Gegenbeispiel: die konstante Abbildung $\\{a, b, c\\} \\to \\{1, 2, 3\\}$, $x \\mapsto 2$.",
     tipps=["Denk an eine konstante Abbildung. Welche Werte werden getroffen?"])

k.menge("Sei $f\\colon \\{0, 1, 2, 3, 4, 5\\} \\to \\{0, 1, 2, 3\\},\\ x \\mapsto x \\bmod 3$. Bestimme $f(\\{1, 2, 4\\})$.",
        mtext(bild(_FM, {1, 2, 4})),
        "$f(1) = 1$, $f(2) = 2$, $f(4) = 1$. Doppelte zählen einmal: $f(\\{1, 2, 4\\}) = \\{1, 2\\}$.",
        tipps=["Setze jedes Element von $A = \\{1, 2, 4\\}$ ein.", "$4 \\bmod 3 = 1$.", "Doppelte Werte schreibst du nur einmal."],
        rechenweg=r"""
:::rechnung
1 \bmod 3 = 1 || Bild von $1$
2 \bmod 3 = 2 || Bild von $2$
4 \bmod 3 = 1 || Bild von $4$, schon dabei
:::
""",
        typische_fehler=[("{1; 2; 4}", "Das ist $A$ selbst. Das Bild besteht aus den **Funktionswerten**."),
                         ("{0; 1; 2}", "Das ist $f(X)$, das Bild von ganz $X$. Gefragt ist nur $f(A)$.")])

k.menge("Sei $f$ wie oben. Bestimme das Urbild $f^{-1}(\\{1, 3\\})$.",
        mtext(urbild(_FM, _X6, {1, 3})),
        "Gesucht sind alle $x \\in X$ mit $f(x) \\in \\{1, 3\\}$. Auf $1$ landen $1$ und $4$, auf $3$ landet kein $x$.",
        tipps=["Berechne $x \\bmod 3$ für jedes $x \\in \\{0, \\ldots, 5\\}$.", "Behalte die $x$ mit Wert $1$ oder $3$.", "Die $3$ wird gar nicht getroffen."],
        rechenweg=r"""
:::rechnung
1 \bmod 3 = 1 || $1 \in B$, also gehört $1$ dazu
4 \bmod 3 = 1 || $1 \in B$, also gehört $4$ dazu
3 \bmod 3 = 0 || $0 \notin B$: $3$ gehört nicht dazu (Achtung: die Zahl $3$ ist hier ein **Wert**)
:::
""",
        typische_fehler=[("{1; 3}", "Das ist $B$ selbst. Gesucht sind die **Stellen** $x$ mit $f(x) \\in B$."),
                         ("{1; 3; 4}", "$x = 3$ hat $f(3) = 0 \\notin B$. Verwechsle nicht den Wert $3$ in $B$ mit der Stelle $x = 3$."),
                         ("{}", "Das Urbild ist nicht leer: $f(1) = 1 \\in B$.")])

# ── Seite 5: Definition 1.71 ─────────────────────────────────────────────
k.erklaerung("Die Schreibweise {g(a) | a ∈ A}", r"""
## Definition 1.71

Für $g\colon X \to Y,\ x \mapsto g(x)$ und $A \subseteq X$ schreibt das Skript
$$\{g(a) \mid a \in A\} := g(A).$$
Die Abbildung $g$ wird nicht extra angegeben, wenn sie aus der Schreibweise und aus dem Zusammenhang klar ist.
Das ist die Mengenschreibweise „alle Werte von $g$ auf $A$“.

**Beispiel 1.72.** Mit den impliziten Abbildungen $g\colon \mathbb{N} \to \mathbb{N},\ z \mapsto 2z$ und
$h\colon \mathbb{N}^2 \to \mathbb{N},\ (a, b) \mapsto a + b$ gilt:

:::rechnung Beispiel 1.72 Schritt für Schritt
2 \cdot 0 = 0 || $a = 0$
2 \cdot 1 = 2 || $a = 1$
2 \cdot 2 = 4 || $a = 2$: also $\{2a \mid a \in \{0, 1, 2\}\} = \{0, 2, 4\}$
0 + 0 = 0 || $a = 0, b = 0$
0 + 2 = 2 || $a = 0, b = 2$; ebenso $1 + 0 = 1$ und $1 + 2 = 3$: also $\{a + b \mid a \in \{0, 1\}, b \in \{0, 2\}\} = \{0, 1, 2, 3\}$
:::

Bei mehreren Laufvariablen läuft man über **alle Kombinationen**. Mehrfach auftretende Werte zählen einmal.

:::alt Wie eine Schleife
`{2*a for a in [0, 1, 2]}` in Python ist genau diese Schreibweise, nur mit anderer Zeichensetzung.
Mit zwei Schleifen `{a + b for a in [0, 1] for b in [0, 2]}` bekommst du $\{0, 1, 2, 3\}$: vier Kombinationen, vier verschiedene Werte.
:::
""")

k.menge("Bestimme $\\{a \\cdot b \\mid a \\in \\{1, 2, 3\\},\\ b \\in \\{0, 2\\}\\}$. Eingabe zum Beispiel `{1; 2}`.",
        mtext({a * b for a in (1, 2, 3) for b in (0, 2)}),
        "Alle sechs Kombinationen: $1 \\cdot 0 = 0$, $1 \\cdot 2 = 2$, $2 \\cdot 0 = 0$, $2 \\cdot 2 = 4$, $3 \\cdot 0 = 0$, $3 \\cdot 2 = 6$. "
        "Menge ohne Doppelte: $\\{0, 2, 4, 6\\}$.",
        tipps=["Bilde alle Paare $(a, b)$ aus beiden Mengen.", "Es gibt $3 \\cdot 2 = 6$ Kombinationen.", "Die $0$ kommt dreimal vor, zählt aber einmal."],
        rechenweg=r"""
:::rechnung
1 \cdot 0 = 0 || erste Kombination
1 \cdot 2 = 2 || zweite
2 \cdot 2 = 4 || vierte
3 \cdot 2 = 6 || sechste; $0$ kommt mehrfach, zählt einmal
:::
""",
        typische_fehler=[("{0; 2; 6}", "Es fehlt $2 \\cdot 2 = 4$: Läuft man über alle Kombinationen, muss man alle sechs Paare prüfen."),
                         ("{0; 2; 4}", "Du hast $3 \\cdot 2 = 6$ vergessen. Prüfe alle sechs Kombinationen.")])

# ── Seite 6: Definition 1.73 ─────────────────────────────────────────────
k.erklaerung("Surjektiv, injektiv, bijektiv", r"""
## Definition 1.73

Soll man eine Abbildung umkehren, muss die neue Abbildung wieder jedem Element mindestens
und höchstens ein Element zuordnen. Daraus werden zwei Bedingungen. Für $f\colon X \to Y$:

(i) [[surjektiv]], falls $f(X) = Y$ (jedes $y$ wird getroffen),
(ii) [[injektiv]], falls $\forall x_1, x_2 \in X : (x_1 \neq x_2) \Rightarrow (f(x_1) \neq f(x_2))$ (kein $y$ wird doppelt getroffen),
(iii) [[bijektiv]], falls beides gilt. Dann ist $f$ eine **Bijektion** von $X$ nach $Y$.

:::visual relation_graph
{"links": ["a", "b", "c"], "rechts": [1, 2, 3], "pfeile": [["a", 2], ["b", 3], ["c", 1]],
 "namen": ["X", "Y"], "zeige": ["injektiv", "surjektiv", "bijektiv"],
 "unterschrift": "Bijektiv: Jedes $y$ hat genau einen Pfeil. Er lässt sich umdrehen."}
:::

:::visual relation_graph
{"links": ["a", "b", "c"], "rechts": [1, 2], "pfeile": [["a", 1], ["b", 2], ["c", 2]],
 "namen": ["X", "Y"], "zeige": ["injektiv", "surjektiv", "bijektiv"],
 "unterschrift": "Surjektiv, aber nicht injektiv: $b$ und $c$ landen beide auf $2$."}
:::

:::visual relation_graph
{"links": ["a", "b"], "rechts": [1, 2, 3], "pfeile": [["a", 1], ["b", 3]],
 "namen": ["X", "Y"], "zeige": ["injektiv", "surjektiv", "bijektiv"],
 "unterschrift": "Injektiv, aber nicht surjektiv: $2$ wird nicht getroffen."}
:::

:::visual relation_graph
{"links": ["a", "b", "c"], "rechts": [1, 2, 3], "pfeile": [["a", 1], ["b", 1], ["c", 3]],
 "namen": ["X", "Y"], "zeige": ["injektiv", "surjektiv", "bijektiv"],
 "unterschrift": "Weder noch: $a, b \\mapsto 1$ und $2$ wird nicht getroffen."}
:::

:::achtung Die Injektivität ist eine Wenn-dann-Aussage
$f(x_1) \neq f(x_2)$ **falls** $x_1 \neq x_2$ ist äquivalent zu: $f(x_1) = f(x_2) \Rightarrow x_1 = x_2$
(Kontraposition). Zum Beweisen nimmst du fast immer die zweite Form.
:::

:::alt Als Sitzplätze
$X$ sind Gäste, $Y$ Stühle, $f$ weist jedem Gast einen Stuhl zu. Injektiv: Keine zwei Gäste teilen sich einen Stuhl.
Surjektiv: Kein Stuhl bleibt leer. Bijektiv: Jeder Stuhl hat genau einen Gast, und du kannst von jedem Stuhl sagen, wer darauf sitzt.
:::
""")

k.mehrfach("Welche der folgenden Abbildungen sind injektiv?",
           ["$\\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto 3x - 2$", "$\\mathbb{N} \\to \\mathbb{N},\\ x \\mapsto x + 1$",
            "$\\mathbb{R}_{\\ge 0} \\to \\mathbb{R},\\ x \\mapsto x^2$"],
           ["$\\mathbb{Z} \\to \\mathbb{Z},\\ x \\mapsto x^2$", "$\\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto |x|$",
            "$\\mathbb{N} \\to \\{0, 1\\},\\ x \\mapsto x \\bmod 2$"],
           "Bei $x \\mapsto x^2$ auf $\\mathbb{Z}$ und $x \\mapsto |x|$ gilt $f(1) = f(-1)$ mit $1 \\neq -1$, bei $x \\bmod 2$ gilt $f(0) = f(2)$. "
           "Auf $\\mathbb{R}_{\\ge 0}$ gibt es keine negativen Zahlen, die dasselbe Quadrat liefern; $3x - 2$ und $x + 1$ sind streng monoton.",
           tipps=["Suche zwei **verschiedene** Eingaben mit demselben Ergebnis.", "Probiere $x$ und $-x$ aus.", "Bei $x \\bmod 2$: Was machen $0$ und $2$?"],
           fehler={"$\\mathbb{Z} \\to \\mathbb{Z},\\ x \\mapsto x^2$": "$f(1) = f(-1) = 1$ mit $1 \\neq -1$.",
                   "$\\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto |x|$": "$|1| = |-1|$: Gegenbeispiel.",
                   "$\\mathbb{N} \\to \\{0, 1\\},\\ x \\mapsto x \\bmod 2$": "Unendlich viele Eingaben, nur zwei Werte: $f(0) = f(2) = 0$."})

k.luecke("Beweis der Injektivität von $f\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto 3x - 2$. Seien $x_1, x_2 \\in \\mathbb{R}$ mit $f(x_1) = f(x_2)$. Fülle die Lücken.",
         "3 x_1 - 2 = 3 x_2 - 2 \\;\\Rightarrow\\; 3 x_1 = \\luecke \\;\\Rightarrow\\; x_1 = \\luecke",
         [["3*x_2"], ["x_2"]],
         "Aus $f(x_1) = f(x_2)$ folgt $3x_1 - 2 = 3x_2 - 2$, also $3x_1 = 3x_2$ und $x_1 = x_2$. Damit ist $f$ injektiv.",
         tipps=["Addiere $2$ auf beiden Seiten.", "Teile dann beide Seiten durch $3$.", "Die erste Lücke ist $3 x_2$, die zweite $x_2$."],
         rechenweg=r"""
:::rechnung
3 x_1 - 2 = 3 x_2 - 2 || Voraussetzung $f(x_1) = f(x_2)$
3 x_1 = 3 x_2 || $+2$ auf beiden Seiten
x_1 = x_2 || durch $3$ teilen
:::
""",
         typische_fehler=[(["3*x_2 - 2", "x_2"], "Die $-2$ steht schon auf beiden Seiten und fällt durch Addieren weg. Nach $+2$ steht dort $3 x_2$.")])

# ── Seite 7: Satz 1.74 ───────────────────────────────────────────────────
k.erklaerung("Satz 1.74: Bijektiv heißt: genau ein Urbild", r"""
## Charakterisierung

**Satz 1.74.** $f\colon X \to Y$ ist genau dann bijektiv, wenn es zu jedem $y \in Y$ **genau ein** $x \in X$
mit $f(x) = y$ gibt.

*Beweis.* „$\Rightarrow$“: Die Surjektivität liefert **mindestens** ein solches $x$. Aus $f(x_1) = f(x_2) = y$
folgt mit Injektivität $x_1 = x_2$, also **höchstens** eins. „$\Leftarrow$“: Gibt es zu jedem $y$ ein $x$, ist $f(X) = Y$,
also $f$ surjektiv. Sind $x_1, x_2$ Urbilder desselben $y$, folgt aus der Eindeutigkeit $x_1 = x_2$: injektiv. $\square$

:::rechnung Satz 1.74 am Beispiel $x \mapsto x + 3$ auf $\mathbb{Z}$
\text{gegeben } y \text{: } y = x + 3 || zu gegebenem $y \in \mathbb{Z}$ suche $x$ mit diesem Wert
\text{also } x = y - 3 || nach $x$ aufgelöst: Lösung existiert (surjektiv)
\text{keine zweite Lösung} || $x + 3 = x' + 3$ gibt $x = x'$: höchstens eine (injektiv)
:::

:::alt Als Telefonbuch
Bijektiv heißt: Zu jeder Nummer gibt es genau einen Teilnehmer (rückwärts nachschlagen). Fehlt zu einer Nummer jeder Teilnehmer,
ist es nicht surjektiv. Teilen sich zwei Teilnehmer eine Nummer, ist es nicht injektiv.
:::
""")

k.ordnen("Ordne den Beweis von Satz 1.74, Richtung „$\\Leftarrow$“ (aus der eindeutigen Lösbarkeit folgt bijektiv).",
         ["Zu jedem $y \\in Y$ existiere genau ein $x \\in X$ mit $f(x) = y$.",
          "Da zu jedem $y$ ein $x$ existiert, ist $f(X) = Y$, also ist $f$ surjektiv.",
          "Seien $x_1, x_2 \\in X$ mit $f(x_1) = f(x_2) =: y$.",
          "Dann sind $x_1$ und $x_2$ Urbilder desselben $y$, und aus der Eindeutigkeit folgt $x_1 = x_2$.",
          "Also ist $f$ injektiv und damit bijektiv. $\\square$"],
         "Surjektiv folgt aus der Existenz, injektiv aus der Eindeutigkeit des Urbilds.",
         ablenker=["Da $f$ bijektiv ist, gibt es zu jedem $y$ ein $x$.",
                   "Da $x_1 \\neq x_2$, folgt $f(x_1) \\neq f(x_2)$."],
         tipps=["Existenz liefert die Surjektivität, Eindeutigkeit die Injektivität.", "Bijektivität darf noch nicht benutzt werden: Sie ist zu zeigen.",
                "Für die Injektivität nimmt man $f(x_1) = f(x_2)$ an."])

# ── Seite 8: Verkettung ──────────────────────────────────────────────────
k.erklaerung("Verkettung und Umkehrabbildung", r"""
## Definition 1.75, Satz 1.76, Definition 1.77

**Definition 1.75.** Für $f\colon X \to Y$ und $g\colon Y \to Z$ ist die [[Verkettung]]
$g \circ f\colon X \to Z,\ x \mapsto g(f(x))$. Erst $f$, dann $g$.

**Satz 1.76.** $f\colon X \to Y$ ist genau dann bijektiv, wenn es eine Abbildung $f^{-1}\colon Y \to X$ gibt mit
$f^{-1} \circ f = \mathrm{id}_X$ und $f \circ f^{-1} = \mathrm{id}_Y$. Dann ist $f^{-1}$ eindeutig bestimmt.
**Definition 1.77.** Diese $f^{-1}$ heißt [[Umkehrfunktion|Umkehrabbildung]] von $f$.

:::rechnung Verkettung und Umkehrung an $f\colon \mathbb{Z} \to \mathbb{Z},\ x \mapsto x + 3$
(g \circ f)(2) = g(5) = 10 || mit $g(x) = 2x$: erst $f(2) = 5$, dann $g(5) = 10$
(f \circ g)(2) = f(4) = 7 || andere Reihenfolge, anderes Ergebnis
x \mapsto x + 3 \mapsto (x + 3) - 3 = x || $f^{-1}(y) = y - 3$ macht $f$ rückgängig: $f^{-1} \circ f = \mathrm{id}$
:::

*Beweisidee „$\Rightarrow$“:* Zu bijektivem $f$ sei $f^{-1}(y)$ das **eindeutige** $x$ mit $f(x) = y$ (Satz 1.74).
*„$\Leftarrow$“:* Aus $f(x_1) = f(x_2)$ folgt $x_1 = f^{-1}(f(x_1)) = f^{-1}(f(x_2)) = x_2$ (injektiv); $y = f(f^{-1}(y))$ (surjektiv).

:::achtung $g \circ f$ liest man von rechts
Bei $(g \circ f)(x) = g(f(x))$ wird $f$ **zuerst** angewendet. Die Verkettung ist im Allgemeinen nicht kommutativ.
:::

:::alt Als Fließband
$f$ ist eine Station, $g$ die nächste. Das Werkstück läuft erst durch $f$, dann durch $g$. Die Umkehrung ist ein Band, das
rückwärts läuft: erst $g^{-1}$, dann $f^{-1}$. Beides zusammen bringt das Werkstück an den Anfang zurück.
:::
""")

_FV = {1: 2, 2: 3, 3: 1, 4: 4}
_GV = {1: 3, 2: 4, 3: 1, 4: 2}
k.zahl("Sei $f\\colon \\{1, 2, 3, 4\\} \\to \\{1, 2, 3, 4\\}$ mit $f(1) = 2$, $f(2) = 3$, $f(3) = 1$, $f(4) = 4$ und $g$ mit $g(1) = 3$, $g(2) = 4$, "
       "$g(3) = 1$, $g(4) = 2$. Berechne $(g \\circ f)(1)$.",
       _GV[_FV[1]],
       "Erst $f$: $f(1) = 2$. Dann $g$: $g(2) = 4$. Also $(g \\circ f)(1) = 4$.",
       tipps=["$(g \\circ f)(x) = g(f(x))$: Welche Abbildung wird zuerst angewendet?", "Berechne zuerst $f(1)$.", "$f(1) = 2$, jetzt $g(2)$."],
       rechenweg=r"""
:::rechnung
1 \mapsto 2 || erst $f$
2 \mapsto 4 || dann $g$
:::
""",
       typische_fehler=[(_FV[_GV[1]], "Das ist $(f \\circ g)(1) = f(g(1))$. Bei $g \\circ f$ wirkt $f$ **zuerst**."),
                        (_FV[1], "Das ist nur $f(1)$. Danach muss noch $g$ angewendet werden.")])

k.ordnen("Ordne den Beweis von Satz 1.76, Richtung „$\\Leftarrow$“: Existiert $f^{-1}$ mit $f^{-1} \\circ f = \\mathrm{id}_X$ und $f \\circ f^{-1} = \\mathrm{id}_Y$, so ist $f$ bijektiv.",
         ["Sei $f(x_1) = f(x_2)$.",
          "Dann gilt $x_1 = f^{-1}(f(x_1)) = f^{-1}(f(x_2)) = x_2$, also ist $f$ injektiv.",
          "Sei $y \\in Y$ beliebig.",
          "Dann gilt $y = f(f^{-1}(y))$, also liegt $y$ im Bild von $f$: $f$ ist surjektiv.",
          "Also ist $f$ bijektiv. $\\square$"],
         "Injektiv folgt aus $f^{-1} \\circ f = \\mathrm{id}$ (zuerst $f$, dann zurück), surjektiv aus $f \\circ f^{-1} = \\mathrm{id}$.",
         ablenker=["Dann gilt $f^{-1}(f(x)) = f(f^{-1}(x))$ für alle $x$."],
         tipps=["Welche Identität liefert die Injektivität, welche die Surjektivität?", "Für Injektivität: Wende $f^{-1}$ auf beide Seiten von $f(x_1) = f(x_2)$ an.",
                "Für Surjektivität: Welches $x$ erzeugt $y$?"])

# ── Seite 9: Beispiel 1.78 und Satz 1.79 ─────────────────────────────────
k.erklaerung("Warum x² sich nicht umkehren lässt", r"""
## Beispiel 1.78 und Satz 1.79

**Beispiel 1.78.** $f\colon \mathbb{Z} \to \mathbb{Z}_{\ge 0},\ x \mapsto x^2$ ist weder surjektiv noch injektiv, und es gibt keine
Umkehrfunktion $\mathbb{Z}_{\ge 0} \to \mathbb{Z}$.

:::rechnung Drei Gründe
f(\mathbb{Z}) = \{0, 1, 4, 9, 16, \ldots\} || $2$ liegt nicht im Bild: nicht surjektiv
(-1)^2 = 1^2 || zwei verschiedene Eingaben, ein Wert: nicht injektiv
f^{-1}(\{1\}) = \{-1, 1\} || zwei Urbilder: $f^{-1}(1)$ wäre nicht eindeutig; und $\sqrt{2} \notin \mathbb{Z}$
:::

**Satz 1.79.** Ist $f$ bijektiv, dann auch $f^{-1}$, und es gilt $(f^{-1})^{-1} = f$.

*Beweis (Idee).* Zu jedem $x \in X$ gibt es genau ein $y$ mit $f^{-1}(y) = x$, nämlich $y = f(x)$.
Nach Satz 1.74 ist $f^{-1}$ bijektiv, und die Umkehrung von $f^{-1}$ schickt $x$ wieder auf $f(x)$. $\square$

:::alt Als Wörterbuch
Ein Wörterbuch Deutsch nach Englisch lässt sich nur dann zu Englisch nach Deutsch umdrehen, wenn jedes englische Wort genau eine
Übersetzung hat und jedes vorkommt. Dreht man die Umkehrung nochmal um, hat man das Original.
:::
""")

k.mc("Warum hat $f\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto x^2$ keine Umkehrabbildung?",
     ["Sie ist nicht bijektiv: nicht injektiv ($f(1) = f(-1)$) und nicht surjektiv ($-1$ wird nicht getroffen)",
      "Weil $\\sqrt{x}$ nicht auf ganz $\\mathbb{R}$ definiert ist, obwohl $f$ bijektiv ist",
      "Weil das Urbild $f^{-1}(\\{4\\})$ nicht existiert",
      "Weil $f$ nicht stetig ist"],
     "Nach Satz 1.76 ist die Bijektivität genau die Bedingung. Hier scheitern Injektivität und Surjektivität. Das Urbild $f^{-1}(\\{4\\}) = \\{-2, 2\\}$ existiert immer.",
     tipps=["Satz 1.76: Umkehrabbildung $\\iff$ bijektiv.", "Prüfe $f(1)$ und $f(-1)$ sowie, ob $-1$ ein Urbild hat."],
     fehler={"Weil $\\sqrt{x}$ nicht auf ganz $\\mathbb{R}$ definiert ist, obwohl $f$ bijektiv ist": "$f$ ist **nicht** bijektiv. Dass $\\sqrt{x}$ negative Zahlen nicht kennt, ist ein Symptom, nicht der Grund.",
             "Weil das Urbild $f^{-1}(\\{4\\})$ nicht existiert": "Das Urbild einer Menge gibt es für jede Abbildung: $f^{-1}(\\{4\\}) = \\{-2, 2\\}$.",
             "Weil $f$ nicht stetig ist": "$f$ ist stetig. Stetigkeit spielt für die Umkehrbarkeit keine Rolle."})

# ── Seite 10: Einschränkung, Satz 1.82 ───────────────────────────────────
k.erklaerung("Einschränkung und Satz 1.82", r"""
## Definition 1.80, Beispiel 1.81, Satz 1.82

**Definition 1.80.** Die [[Einschränkung]] von $f\colon X \to Y$ auf $A \subseteq X$ ist
$f|_A\colon A \to f(A),\ x \mapsto f(x)$.

**Beispiel 1.81.** $f\colon \mathbb{R} \to \mathbb{R}_{\ge 0},\ x \mapsto x^2$ ist surjektiv, aber nicht injektiv.
Die Einschränkung $f|_{\mathbb{R}_{\ge 0}}$ ist bijektiv mit Umkehrfunktion $x \mapsto \sqrt{x}$.

**Satz 1.82.** Sind $f\colon X \to X'$ und $g\colon Y \to Y'$ bijektiv, so auch:
(i) $g \circ f\colon X \to Y'$, falls $X' = Y$; (ii) $f|_A\colon A \to f(A)$ für jedes $A \subseteq X$;
(iii) $h\colon X \cup Y \to X' \cup Y'$ mit $h(x) = f(x)$ für $x \in X$ und $h(x) = g(x)$ für $x \in Y$, falls $X \cap Y = \emptyset$ und $X' \cap Y' = \emptyset$;
(iv) $p\colon X \times Y \to X' \times Y',\ (x, y) \mapsto (f(x), g(y))$.

:::rechnung Satz 1.82 (iii) und (iv) an $f\colon \{1, 2\} \to \{a, b\}$, $g\colon \{3, 4\} \to \{c, d\}$
1 \mapsto a,\ 2 \mapsto b,\ 3 \mapsto c,\ 4 \mapsto d || $h$ ist auf $\{1, 2, 3, 4\}$ wohldefiniert, weil die Definitionsmengen disjunkt sind
2 \cdot 2 = 4 || $X \times Y$ hat $4$ Paare, $X' \times Y'$ auch
(1, 3) \mapsto (a, c),\ (1, 4) \mapsto (a, d),\ (2, 3) \mapsto (b, c),\ (2, 4) \mapsto (b, d) || $p$ trifft jedes der vier Paare genau einmal
:::

:::achtung Disjunktheit in (iii) ist nötig
Ohne $X \cap Y = \emptyset$ wäre $h$ nicht wohldefiniert: Für $x \in X \cap Y$ stünden $f(x)$ und $g(x)$ zur Wahl. Ohne
$X' \cap Y' = \emptyset$ könnten zwei Elemente denselben Wert bekommen: $h$ wäre nicht injektiv.
:::

:::alt Als Umbau
Eine Einschränkung verkleinert den Eingangsbereich und passt die Zielmenge an das tatsächlich getroffene Bild an. Damit wird jede
Abbildung surjektiv. Durch geschickte Wahl von $A$ (nur die Zahlen $\ge 0$) wird $x^2$ sogar injektiv und damit umkehrbar.
:::
""")

k.mc("Sei $f\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto x^2$. Auf welche Menge $A$ eingeschränkt ist $f|_A\\colon A \\to f(A)$ **bijektiv**?",
     ["$A = \\mathbb{R}_{\\ge 0}$", "$A = \\mathbb{R}$", "$A = \\{-1, 1\\}$", "$A = [-1, 1]$"],
     "$f|_A$ ist nach Definition 1.80 immer surjektiv auf $f(A)$. Injektiv ist $x^2$ nur auf einer Menge, die nicht $x$ und $-x$ zugleich enthält: z. B. $\\mathbb{R}_{\\ge 0}$.",
     tipps=["Die Zielmenge $f(A)$ ist automatisch das Bild: Es geht nur um Injektivität.", "Gibt es in $A$ zwei Zahlen $x \\neq -x$?"],
     fehler={"$A = \\mathbb{R}$": "$f(1) = f(-1)$: nicht injektiv.",
             "$A = \\{-1, 1\\}$": "$f(-1) = f(1) = 1$: nicht injektiv.",
             "$A = [-1, 1]$": "$-\\frac12$ und $\\frac12$ liegen beide in $[-1, 1]$ und haben dasselbe Quadrat."})

k.mehrfach("Welche Aussagen zu Satz 1.82 stimmen?",
           ["Die Verkettung zweier Bijektionen $g \\circ f$ ist bijektiv, falls $X' = Y$",
            "Für $f, g$ bijektiv ist $p\\colon (x, y) \\mapsto (f(x), g(y))$ bijektiv",
            "Die Einschränkung $f|_A\\colon A \\to f(A)$ einer Bijektion ist bijektiv"],
           ["In (iii) kann man auf die Bedingung $X \\cap Y = \\emptyset$ verzichten",
            "Die Verkettung zweier injektiver Abbildungen ist immer surjektiv"],
           "(i), (ii), (iv) stehen im Satz. In (iii) braucht man beide Disjunktheiten, damit $h$ wohldefiniert und injektiv ist. "
           "Injektive Abbildungen verketten sich zu injektiven, nicht zu surjektiven.",
           tipps=["Lies die Voraussetzungen von (i) bis (iv) noch einmal.", "Was passiert, wenn $X$ und $Y$ ein Element gemeinsam haben?"],
           fehler={"In (iii) kann man auf die Bedingung $X \\cap Y = \\emptyset$ verzichten": "Für $x \\in X \\cap Y$ wäre $h(x)$ nicht eindeutig definiert.",
                   "Die Verkettung zweier injektiver Abbildungen ist immer surjektiv": "Injektiv und surjektiv sind unabhängig: $\\{1\\} \\to \\{1, 2\\} \\to \\{1, 2, 3\\}$ mit $x \\mapsto x$ ist injektiv, aber nicht surjektiv."})


# ── Praxis ────────────────────────────────────────────────────────────────
_KEINE = "keine Abbildung"
_BIJ = "bijektiv"
_INJ = "injektiv, aber nicht surjektiv"
_SUR = "surjektiv, aber nicht injektiv"
_WED = "weder injektiv noch surjektiv"


def _klassifiziere(X, Y, R):
    """(Kategorie, Begründung als Text mit Beispielen)."""
    for x in X:
        bilder = sorted(b for a, b in R if a == x)
        if len(bilder) != 1:
            g = (f"${x}$ hat keinen Pfeil" if not bilder else f"${x}$ hat {len(bilder)} Pfeile (zu {', '.join('$' + str(b) + '$' for b in bilder)})")
            return _KEINE, f"{g}, also ist $R$ keine Abbildung. Injektiv und surjektiv sind dann gar nicht definiert."
    f = als_dict(R)
    doppelt = [y for y in sorted(set(f.values())) if sum(1 for v in f.values() if v == y) > 1]
    ungetroffen = [y for y in Y if y not in f.values()]
    inj, sur = not doppelt, not ungetroffen
    if doppelt:
        y = doppelt[0]
        quellen = ", ".join("$" + str(x) + "$" for x in X if f[x] == y)
        s_inj = f"nicht injektiv: ${y}$ wird von {quellen} getroffen"
    else:
        s_inj = "injektiv: kein $y$ wird doppelt getroffen"
    s_sur = (f"nicht surjektiv: ${ungetroffen[0]}$ wird nicht getroffen" if ungetroffen else "surjektiv: jedes $y$ wird getroffen")
    kat = _BIJ if inj and sur else _INJ if inj else _SUR if sur else _WED
    return kat, f"$R$ ist eine Abbildung, {s_inj}, {s_sur}."


def abbildung_eigenschaften(rng):
    art = rng.choice(["bij", "inj", "sur", "weder", "keine"])
    if art == "bij":
        n = rng.choice([3, 4])
        X, Y = list("abcd"[:n]), list(range(1, n + 1))
        werte = Y[:]
        rng.shuffle(werte)
        f = dict(zip(X, werte))
    elif art == "inj":
        nx = rng.choice([2, 3])
        X, Y = list("abcd"[:nx]), list(range(1, nx + rng.randint(1, 2) + 1))
        f = dict(zip(X, rng.sample(Y, nx)))
    elif art == "sur":
        ny = rng.choice([2, 3])
        X, Y = list("abcde"[:ny + rng.randint(1, 2)]), list(range(1, ny + 1))
        werte = Y[:] + [rng.choice(Y) for _ in range(len(X) - ny)]
        rng.shuffle(werte)
        f = dict(zip(X, werte))
    else:
        nx, ny = rng.choice([3, 4]), rng.choice([3, 4])
        X, Y = list("abcd"[:nx]), list(range(1, ny + 1))
        while True:
            f = {x: rng.choice(Y) for x in X}
            if not ist_inj(f) and not ist_sur(f, Y):
                break
    R = set(f.items())
    if art == "keine":
        x = rng.choice(X)
        if rng.random() < 0.5 and len(R) > 1:
            R.discard((x, f[x]))
        else:
            R.add((x, rng.choice([y for y in Y if y != f[x]])))
    kat, grund = _klassifiziere(X, Y, R)
    optionen = [kat] + [o for o in (_KEINE, _BIJ, _INJ, _SUR, _WED) if o != kat]
    fehler = {o: f"Das stimmt nicht. {grund}" for o in optionen[1:]}
    zeilen = [(f"\\text{{Pfeile von }} {x} \\text{{: }} {len([b for a, b in R if a == x])}", f"für jedes $x \\in X$ gezählt") for x in X][:1]
    zeilen = [("\\text{Befund}", grund)]
    return {"typ": "mc",
            "frage": f"Gegeben sind $X = {mtex(X)}$, $Y = {mtex(Y)}$ und die Relation $R = {paare_tex(R)} \\subseteq X \\times Y$. Was trifft zu?",
            "optionen": optionen, "fehler": fehler,
            "tipps": ["Zähle für jedes Element von $X$ die Pfeile. Ist es immer genau einer?",
                      "Wenn ja: Wird ein Element von $Y$ mehr als einmal getroffen (injektiv verletzt) oder gar nicht (surjektiv verletzt)?",
                      "Ein einziges Gegenbeispiel pro Eigenschaft genügt."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Erst prüfen, ob es eine Abbildung ist (genau ein Pfeil je $x$), dann injektiv und surjektiv."}


def bild_urbild_abb(rng):
    nx, ny = rng.choice([5, 6]), rng.choice([4, 5])
    X, Y = list(range(1, nx + 1)), list(range(1, ny + 1))
    f = {x: rng.choice(Y) for x in X}
    tab = ", ".join(f"f({x}) = {f[x]}" for x in X)
    kopf = f"Sei $f\\colon {mtex(X)} \\to {mtex(Y)}$ gegeben durch ${tab}$. "
    if rng.random() < 0.5:
        A = sorted(rng.sample(X, rng.randint(2, 4)))
        loes = bild(f, A)
        zeilen = [(f"{x} \\mapsto {f[x]}", f"Bild von ${x}$") for x in A]
        fehler = [(mtext(A), "Das ist $A$ selbst. Das Bild besteht aus den **Funktionswerten**."),
                  (mtext(bild(f, X)), "Das ist $f(X)$. Gefragt ist nur $f(A)$."),
                  (mtext(urbild(f, X, set(A))), "Das ist das Urbild $f^{-1}(A)$. Gesucht ist das Bild: Setze die Elemente von $A$ in $f$ ein.")]
        frage = kopf + f"Bestimme das Bild $f({mtex(A)})$. Eingabe zum Beispiel `{{1; 2}}`."
        tipps = ["Setze jedes Element von $A$ in die Tabelle ein.", f"Zum Beispiel $f({A[0]}) = {f[A[0]]}$.", "Doppelte Werte schreibst du einmal."]
        erkl = "$f(A) = \\{f(x) \\mid x \\in A\\}$ sammelt die Funktionswerte der Elemente von $A$."
    else:
        B = set(rng.sample(Y, rng.randint(1, 2)))
        loes = urbild(f, X, B)
        zeilen = [(f"{x} \\mapsto {f[x]}", f"${f[x]} \\in B$, also gehört ${x}$ dazu" if f[x] in B else f"${f[x]} \\notin B$") for x in X]
        fehler = [(mtext(B), "Das ist $B$ selbst. Gesucht sind die **Stellen** $x$, deren Wert in $B$ liegt."),
                  (mtext(bild(f, X)), "Das ist das Bild $f(X)$. Gesucht sind die Eingaben, nicht die Ausgaben."),
                  (mtext(bild(f, loes)) if loes else "{" + "}", "Das sind die Werte. Gesucht sind die Stellen $x$.")]
        if len(loes) > 1:
            fehler.append((mtext(sorted(loes)[:-1]), "Es fehlt noch ein $x$. Prüfe jedes Element von $X$."))
        if loes:
            fehler.append(("{}", "Das Urbild ist nicht leer."))
        frage = kopf + f"Bestimme das Urbild $f^{{-1}}({mtex(B)})$. Eingabe zum Beispiel `{{1; 2}}`, die leere Menge als `{{}}`."
        tipps = ["Gehe alle $x \\in X$ durch.", "Behalte genau die $x$, deren Wert in $B$ liegt.", "Ist kein Wert in $B$, ist das Urbild leer."]
        erkl = "$f^{-1}(B) = \\{x \\in X \\mid f(x) \\in B\\}$ sammelt alle Stellen mit Wert in $B$."
    gesehen, tf = {mtext(loes)}, []
    for w, t in fehler:
        if w not in gesehen:
            gesehen.add(w)
            tf.append((w, t))
    return {"frage": frage, "loesung": mtext(loes), "tipps": tipps, "rechenweg": rechnung(zeilen), "erklaerung": erkl,
            "typische_fehler": tf}


def verkettung_wert(rng):
    n = 5
    X = list(range(1, n + 1))
    while True:
        f = {x: rng.choice(X) for x in X}
        g = {x: rng.choice(X) for x in X}
        x0 = rng.choice(X)
        gf, fg = g[f[x0]], f[g[x0]]
        if len({gf, fg, f[x0], g[x0]}) >= 3:
            break
    tf = ", ".join(f"f({x}) = {f[x]}" for x in X)
    tg = ", ".join(f"g({x}) = {g[x]}" for x in X)
    fehler = [(fg, f"Das ist $(f \\circ g)({x0})$. Bei $g \\circ f$ wirkt $f$ **zuerst**."),
              (f[x0], f"Das ist nur $f({x0})$. Danach muss noch $g$ angewendet werden."),
              (g[x0], f"Das ist nur $g({x0})$. Zuerst muss $f$ angewendet werden.")]
    fehler = [(w, t) for w, t in fehler if w != gf]
    seen, tfl = set(), []
    for w, t in fehler:
        if w not in seen:
            seen.add(w)
            tfl.append((w, t))
    return {"frage": f"Sei $f, g\\colon {mtex(X)} \\to {mtex(X)}$ mit ${tf}$ und ${tg}$. Berechne $(g \\circ f)({x0})$.",
            "loesung": gf,
            "tipps": ["$(g \\circ f)(x) = g(f(x))$: erst $f$, dann $g$.", f"Berechne zuerst $f({x0}) = {f[x0]}$.", f"Wende nun $g$ auf ${f[x0]}$ an."],
            "rechenweg": rechnung([(f"{x0} \\mapsto {f[x0]}", "erst $f$"), (f"{f[x0]} \\mapsto {gf}", "dann $g$")]),
            "erklaerung": "In $g \\circ f$ wirkt $f$ zuerst, danach $g$.", "typische_fehler": tfl}


def umkehr_wert(rng):
    n = rng.choice([4, 5])
    X = list(range(1, n + 1))
    while True:
        w = X[:]
        rng.shuffle(w)
        f = dict(zip(X, w))
        inv = {v: k_ for k_, v in f.items()}
        y0 = rng.choice(X)
        if inv[y0] != f[y0] and inv[y0] != y0:
            break
    tf = ", ".join(f"f({x}) = {f[x]}" for x in X)
    fehler = [(f[y0], f"Das ist $f({y0})$, nicht $f^{{-1}}({y0})$. Gesucht ist das $x$ mit $f(x) = {y0}$."),
              (y0, "Die Umkehrabbildung ist nicht die Identität.")]
    fehler = [(w, t) for w, t in fehler if w != inv[y0]]
    return {"frage": f"Die Abbildung $f\\colon {mtex(X)} \\to {mtex(X)}$ ist bijektiv mit ${tf}$. Bestimme $f^{{-1}}({y0})$.",
            "loesung": inv[y0],
            "tipps": [f"Gesucht ist das eindeutige $x$ mit $f(x) = {y0}$.", "Suche in der Tabelle die Stelle, an der der Wert vorkommt.",
                      f"Es ist $f({inv[y0]}) = {y0}$."],
            "rechenweg": rechnung([(f"{inv[y0]} \\mapsto {y0}", f"$f({inv[y0]}) = {y0}$, also $f^{{-1}}({y0}) = {inv[y0]}$")]),
            "erklaerung": "Die Umkehrabbildung schickt $y$ auf das eindeutige $x$ mit $f(x) = y$ (Satz 1.74 und 1.76).",
            "typische_fehler": fehler}


k.praxis()

k.generator(abbildung_eigenschaften, typ="mc", titel="Abbildung, injektiv, surjektiv oder bijektiv?")
k.generator(bild_urbild_abb, typ="menge", titel="Bild und Urbild endlicher Abbildungen")
k.generator(verkettung_wert, typ="zahl", titel="Verkettung auswerten")
k.generator(umkehr_wert, typ="zahl", titel="Umkehrabbildung bestimmen")

k.rechenweg_aufgabe(r"""
## Quiz-Stil: Zwei Abbildungen auf ℤ

Sei $f\colon \mathbb{Z} \to \mathbb{Z},\ x \mapsto 2x + 1$ und $g\colon \mathbb{Z} \to \mathbb{Z},\ x \mapsto x^2$.
""",
    [{"typ": "wf", "frage": "$f$ ist injektiv.", "wahr": True,
      "tipps": ["Aus $2x_1 + 1 = 2x_2 + 1$ folgt?"], "erklaerung": "$2x_1 + 1 = 2x_2 + 1 \\Rightarrow x_1 = x_2$."},
     {"typ": "mc", "frage": "Ist $f$ surjektiv?",
      "optionen": ["Nein: $f(x)$ ist immer ungerade, also wird $0$ nicht getroffen", "Ja: $x = \\frac{y - 1}{2}$ löst $f(x) = y$", "Nein: $f$ ist nicht injektiv"],
      "fehler": {"Ja: $x = \\frac{y - 1}{2}$ löst $f(x) = y$": "Für gerades $y$ ist $\\frac{y-1}{2}$ nicht ganzzahlig, also kein Element von $\\mathbb{Z}$.",
                 "Nein: $f$ ist nicht injektiv": "$f$ ist injektiv. Aber das ist ohnehin eine andere Eigenschaft als Surjektivität."},
      "tipps": ["Welche Parität haben alle Werte $2x + 1$?", "Suche ein $y \\in \\mathbb{Z}$, das nicht getroffen wird."],
      "erklaerung": "Der Wert $0$ ist gerade und wird nicht getroffen."},
     {"typ": "zahl", "frage": "Berechne $(g \\circ f)(2)$.", "loesung": 25,
      "tipps": ["Erst $f$, dann $g$.", "$f(2) = 5$."], "rechenweg": "$f(2) = 5$, $g(5) = 25$.",
      "typische_fehler": [(9, "Das ist $(f \\circ g)(2) = f(4) = 9$. Bei $g \\circ f$ wirkt $f$ zuerst.")]},
     {"typ": "zahl", "frage": "Berechne $(f \\circ g)(2)$.", "loesung": 9,
      "tipps": ["Erst $g$, dann $f$.", "$g(2) = 4$."], "rechenweg": "$g(2) = 4$, $f(4) = 9$.",
      "typische_fehler": [(25, "Das ist $(g \\circ f)(2)$. Bei $f \\circ g$ wirkt $g$ zuerst.")]}],
    "$f$ ist injektiv, aber nicht surjektiv, also nicht bijektiv. Die Verkettung ist nicht kommutativ: $(g \\circ f)(2) = 25 \\neq 9 = (f \\circ g)(2)$.",
    uebungsblatt=True,
    tipps=["Für Injektivität nimmst du $f(x_1) = f(x_2)$ an.", "Für Surjektivität suche ein nicht getroffenes $y$."],
    rechenweg=r"""
:::rechnung
\text{Annahme: } 2 x_1 + 1 = 2 x_2 + 1 || Voraussetzung $f(x_1) = f(x_2)$
\text{also } x_1 = x_2 || $-1$ und $:2$: also injektiv
2 \cdot 2 + 1 = 5 || $f(2) = 5$
5^2 = 25 || $g(5)$, also $(g \circ f)(2) = 25$
4 = 2^2 || $g(2) = 4$; $2 \cdot 4 + 1 = 9$ ergibt $(f \circ g)(2)$
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Satz 1.82 (i) und (iv) (im Skript „Übung“)

Seien $f\colon X \to X'$ und $g\colon Y \to Y'$ bijektiv.

1. Falls $X' = Y$: Zeigen Sie, dass $g \circ f\colon X \to Y'$ bijektiv ist.
2. Zeigen Sie, dass $p\colon X \times Y \to X' \times Y',\ (x, y) \mapsto (f(x), g(y))$ bijektiv ist.
""",
    r"""
**1. Injektiv:** Seien $x_1, x_2 \in X$ mit $(g \circ f)(x_1) = (g \circ f)(x_2)$, also $g(f(x_1)) = g(f(x_2))$.
Da $g$ injektiv ist, folgt $f(x_1) = f(x_2)$. Da $f$ injektiv ist, folgt $x_1 = x_2$.
**Surjektiv:** Sei $z \in Y'$. Da $g$ surjektiv ist, gibt es $y \in Y = X'$ mit $g(y) = z$. Da $f$ surjektiv ist, gibt es $x \in X$ mit
$f(x) = y$. Dann $(g \circ f)(x) = g(y) = z$. Also ist $g \circ f$ bijektiv.

**2. Injektiv:** Aus $p(x_1, y_1) = p(x_2, y_2)$ folgt $(f(x_1), g(y_1)) = (f(x_2), g(y_2))$, also komponentenweise
$f(x_1) = f(x_2)$ und $g(y_1) = g(y_2)$. Injektivität von $f$ und $g$ liefert $x_1 = x_2$ und $y_1 = y_2$, also $(x_1, y_1) = (x_2, y_2)$.
**Surjektiv:** Sei $(u, v) \in X' \times Y'$. Es gibt $x \in X$ mit $f(x) = u$ und $y \in Y$ mit $g(y) = v$. Dann $p(x, y) = (u, v)$. $\square$
""",
    ["In (i) Injektivität mit zwei Schritten bewiesen (zuerst $g$, dann $f$ anwenden)",
     "In (i) Surjektivität rückwärts konstruiert ($z$, dann $y$, dann $x$)",
     "In (iv) die Gleichheit von Paaren komponentenweise ausgewertet",
     "In (iv) für Surjektivität ein Urbild $(x, y)$ aus zwei einzelnen Urbildern gebaut"],
    "Injektiv zeigt man mit „$f(x_1) = f(x_2) \\Rightarrow x_1 = x_2$“, surjektiv, indem man zu beliebigem Zielelement ein Urbild angibt.",
    uebungsblatt=True,
    tipps=["Bei (i) arbeitest du dich Schritt für Schritt von außen nach innen: erst $g$, dann $f$ rückgängig machen."])

k.papier(r"""
## Übungsblatt-Stil: Injektivität widerlegen und beweisen

Entscheiden Sie für jede Abbildung, ob sie injektiv und ob sie surjektiv ist. Beweisen Sie oder geben Sie ein Gegenbeispiel an.

1. $f_1\colon \mathbb{Z} \to \mathbb{Z},\ x \mapsto x^2 + 1$
2. $f_2\colon \mathbb{R} \to \mathbb{R},\ x \mapsto 2x - 5$
3. $f_3\colon \mathbb{N} \to \mathbb{N},\ x \mapsto x + 2$
""",
    r"""
**1.** Nicht injektiv: $f_1(1) = 2 = f_1(-1)$ mit $1 \neq -1$. Nicht surjektiv: $f_1(x) = x^2 + 1 \ge 1$, also wird $0$ nicht getroffen.

**2.** Injektiv: $2x_1 - 5 = 2x_2 - 5 \Rightarrow x_1 = x_2$. Surjektiv: Zu $y \in \mathbb{R}$ ist $x = \frac{y + 5}{2}$ ein Urbild, denn $2 \cdot \frac{y + 5}{2} - 5 = y$. Also bijektiv, $f_2^{-1}(y) = \frac{y + 5}{2}$.

**3.** Injektiv: $x_1 + 2 = x_2 + 2 \Rightarrow x_1 = x_2$. Nicht surjektiv: Die Werte sind alle $\ge 2$, also werden $0$ und $1$ nicht getroffen.
""",
    ["Für $f_1$ das Gegenbeispiel $1, -1$ und ein nicht getroffenes $y$ angegeben",
     "Für $f_2$ Injektivität UND Surjektivität (mit konstruiertem Urbild) gezeigt",
     "Für $f_3$ ein nicht getroffenes Element von $\\mathbb{N}$ gefunden (im Skript ist $0 \\in \\mathbb{N}$)"],
    "Gegenbeispiele sind konkrete Zahlen. Beweise gelten für beliebige $x_1, x_2$ bzw. beliebiges $y$.",
    uebungsblatt=True,
    tipps=["Probiere bei Quadraten die Zahl und ihr Negatives aus.", "Löse $f(x) = y$ nach $x$ auf und prüfe, ob $x$ in der Definitionsmenge liegt."])

k.zusammenfassung(r"""
## Abbildungen (Skript Abschn. 1.7, Def. 1.66 bis Satz 1.82)

- **Abbildung** (Def. 1.66): Relation $f \subseteq X \times Y$ mit genau einem $f(x)$ für jedes $x \in X$; $f\colon X \to Y,\ x \mapsto f(x)$. Verknüpfung: $\star\colon X \times X \to X$.
- **Beispiele 1.68:** $\mathrm{id}_M$, $+$ und $\cdot$, Polynome, kanonische Abbildung $\nu\colon M \to M/{\sim},\ x \mapsto [x]$.
- **Bild** $f(A) = \{y \in Y \mid \exists x \in A : f(x) = y\}$, **Urbild** $f^{-1}(B) = \{x \in X \mid f(x) \in B\}$ (Def. 1.69). $f^{-1}(Y) = X$, aber nur $f(X) \subseteq Y$ (Beob. 1.70).
- $\{g(a) \mid a \in A\} := g(A)$ (Def. 1.71).

| Eigenschaft (Def. 1.73) | Bedeutung | Nachweis |
|---|---|---|
| surjektiv | $f(X) = Y$ | zu jedem $y$ ein Urbild angeben |
| injektiv | $x_1 \neq x_2 \Rightarrow f(x_1) \neq f(x_2)$ | $f(x_1) = f(x_2) \Rightarrow x_1 = x_2$ zeigen |
| bijektiv | beides | genau ein Urbild je $y$ (Satz 1.74) |

- **Verkettung** $g \circ f\colon x \mapsto g(f(x))$ (Def. 1.75): erst $f$, dann $g$.
- **Satz 1.76:** $f$ bijektiv $\iff$ es gibt $f^{-1}$ mit $f^{-1} \circ f = \mathrm{id}_X$, $f \circ f^{-1} = \mathrm{id}_Y$ (eindeutig). Satz 1.79: $(f^{-1})^{-1} = f$.
- **Einschränkung** $f|_A\colon A \to f(A)$ (Def. 1.80). $x \mapsto x^2$ ist auf $\mathbb{R}_{\ge 0}$ bijektiv (Bsp. 1.81).
- **Satz 1.82:** Verkettung, Einschränkung, Vereinigung (bei disjunkten Mengen) und Produkt von Bijektionen sind Bijektionen.

!! Gegenbeispiele sind konkrete Zahlen, Beweise gelten für beliebige Elemente.
""")
