# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 5: Relationen und ihre Eigenschaften (Skript Disser WS 26/27, Abschn. 1.6,
Def. 1.35 bis Bsp. 1.41)."""
from itertools import combinations, product

from ..engine import neues_kapitel

k = neues_kapitel(
    slug="relationen",
    titel="Relationen und ihre Eigenschaften",
    beschreibung="Relation als Teilmenge von N × M, gerichteter Graph, reflexiv, symmetrisch, antisymmetrisch, transitiv",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 1.6",
    icon="🔗")


# ── Hilfsfunktionen: Python rechnet alle Eigenschaften ─────────────────────
def _paar_tex(p):
    return f"({p[0]}, {p[1]})"


def _rel_tex(r):
    if not r:
        return "\\emptyset"
    return "\\{" + ", ".join(_paar_tex(p) for p in sorted(r)) + "\\}"


def _rel_text(r):
    return "{" + "; ".join(f"({a}; {b})" for a, b in sorted(r)) + "}"


def _mtex(s):
    """Endliche Menge (frozenset) als LaTeX."""
    if not s:
        return "\\emptyset"
    return "\\{" + ", ".join(str(x) for x in sorted(s)) + "\\}"


def gegenbeispiel(m, r, eig):
    """None, wenn r die Eigenschaft hat, sonst ein Gegenbeispiel (Tupel)."""
    if eig == "reflexiv":
        for x in m:
            if (x, x) not in r:
                return (x,)
    elif eig == "symmetrisch":
        for x, y in sorted(r):
            if (y, x) not in r:
                return (x, y)
    elif eig == "antisymmetrisch":
        for x, y in sorted(r):
            if x != y and (y, x) in r:
                return (x, y)
    elif eig == "transitiv":
        for x, y in sorted(r):
            for y2, z in sorted(r):
                if y == y2 and (x, z) not in r:
                    return (x, y, z)
    return None


EIGENSCHAFTEN = ("reflexiv", "symmetrisch", "antisymmetrisch", "transitiv")


def hat(m, r, eig):
    return gegenbeispiel(m, r, eig) is None


def _gegen_text(eig, g):
    if eig == "reflexiv":
        return f"$({g[0]}, {g[0]}) \\notin R$, die Schleife an ${g[0]}$ fehlt."
    if eig == "symmetrisch":
        return f"$({g[0]}, {g[1]}) \\in R$, aber $({g[1]}, {g[0]}) \\notin R$."
    if eig == "antisymmetrisch":
        return f"$({g[0]}, {g[1]}) \\in R$ und $({g[1]}, {g[0]}) \\in R$, aber ${g[0]} \\neq {g[1]}$."
    x, y, z = g
    zusatz = f" Auch $x = z$ ist erlaubt: Aus ${x}R{y}$ und ${y}R{x}$ müsste ${x}R{x}$ folgen." if x == z else ""
    return f"$({x}, {y}) \\in R$ und $({y}, {z}) \\in R$, aber $({x}, {z}) \\notin R$.{zusatz}"


def transitiver_abschluss(r):
    """Kleinste transitive Relation, die r enthält, und die Runden des Hinzufügens."""
    t = set(r)
    runden = []
    while True:
        neu = {(x, z) for (x, y) in t for (y2, z) in t if y == y2 and (x, z) not in t}
        if not neu:
            return t, runden
        runden.append(sorted(neu))
        t |= neu


# ── Beispiel 1.37: S auf P({1, 2, 3}) ─────────────────────────────────────
_P123 = [frozenset(c) for n in range(4) for c in combinations((1, 2, 3), n)]
_S = {(a, b) for a in _P123 for b in _P123 if a & b}
_S_ANZ = len(_S)
_S_DISJ = sum(1 for a in _P123 for b in _P123 if a and b and not a & b)
assert _S_ANZ == 49 - _S_DISJ
_S_TABELLE = "\n".join(
    f"| ${_mtex(a)}$ | " + (", ".join(f"${_mtex(b)}$" for b in _P123 if (a, b) in _S) or "keine") + " |"
    for a in _P123)
# Beispiel 1.41: Eigenschaften von S
assert [hat(_P123, _S, e) for e in EIGENSCHAFTEN] == [False, True, False, False]
_S_PARTNER_1 = [b for b in _P123 if (frozenset({1}), b) in _S]


def _mengen_text(liste):
    return "{" + "; ".join("{" + "; ".join(str(x) for x in sorted(b)) + "}" for b in liste) + "}"


k.lernziele([
    "Ich kann eine Relation als Teilmenge $R \\subseteq N \\times M$ lesen und $xRy$ richtig deuten (Def. 1.35, 1.36)",
    "Ich kann eine Relation auf einer endlichen Menge als gerichteten Graphen oder als Tabelle darstellen (Bsp. 1.37)",
    "Ich kann reflexiv, symmetrisch, antisymmetrisch und transitiv prüfen und jede verletzte Eigenschaft mit einem Gegenbeispiel widerlegen (Def. 1.38)",
    "Ich kann die Eigenschaften am Graphen ablesen und verstehe, warum eine leere Bedingung erfüllt ist (Bsp. 1.39 bis 1.41)",
])

k.warum(r"""
Relationale Datenbanken heißen so, weil jede Tabelle eine Relation ist: eine Menge von
Tupeln. „Folgt“ bei sozialen Netzwerken, „hängt ab von“ beim Build-System, „ist Unterklasse
von“ in Java: alles Relationen, alles gerichtete Graphen. Und die vier Eigenschaften
haben handfeste Folgen. Ein Vergleich zum Sortieren **muss** transitiv sein, sonst wirft
Javas `Collections.sort` die Ausnahme „Comparison method violates its general contract“.
""")

# ── Seite 1: Was ist eine Relation? ───────────────────────────────────────
k.erklaerung("Was ist eine Relation?", r"""
## Eine Relation ist eine Menge von Paaren

:::analogie 🗣️ Wer spricht welche Sprache?
Ada spricht Python und C, Ben spricht Java, Cem spricht keine dieser drei. Schreib jedes
zutreffende Paar (Person, Sprache) auf einen Zettel. Der Zettel **ist** die Relation.
:::

**Definition 1.35.** Eine (binäre) [[Relation]] zwischen den Mengen $N$ und $M$ ist eine
Teilmenge $R \subseteq N \times M$ des [[kartesischen Produkts|kartesisches Produkt]]. Für
$(x, y) \in R$ schreiben wir kurz $xRy$ („$x$ steht in Relation zu $y$“). Ist $N = M$, heißt
$R$ eine Relation **auf** der Menge $M$.

:::visual relation_graph
{"links": ["Ada", "Ben", "Cem"], "rechts": ["Python", "Java", "C"],
 "pfeile": [["Ada", "Python"], ["Ada", "C"], ["Ben", "Java"]],
 "namen": ["N", "M"], "zeige": ["abbildung"],
 "unterschrift": "$R = \\{(\\text{Ada}, \\text{Python}), (\\text{Ada}, \\text{C}), (\\text{Ben}, \\text{Java})\\}$. Ein Element darf beliebig viele Partner haben, auch keinen."}
:::

Eine Relation muss also nichts „ausrechnen“. Sie sagt nur, welche Paare dazugehören.

:::alt Als Tabelle in einer Datenbank
Stell dir eine Tabelle mit zwei Spalten vor, „Person“ und „Sprache“. Jede Zeile ist ein
[[geordnetes Paar]]. Die Menge aller Zeilen ist die Relation. Ob $(\text{Cem}, \text{Java})$
dazugehört, prüfst du, indem du die Zeile suchst: Sie fehlt, also gilt nicht
$\text{Cem}\,R\,\text{Java}$. Darum heißen solche Datenbanken *relational*.
:::
---
## Vergleichen ist auch eine Relation

**Definition 1.36.** Den Vergleich natürlicher Zahlen fasst das Skript als Relation auf:

$$\le\ = \{(n, m) \in \mathbb{N} \times \mathbb{N} \mid \exists k \in \mathbb{N} : m = n + k\}.$$

In Worten: $n \le m$ heißt, du kommst von $n$ durch Addieren einer natürlichen Zahl $k$ zu $m$.

:::rechnung Drei Paare prüfen
5 = 2 + 3 || mit $k = 3 \in \mathbb{N}$: also $(2, 5) \in\ \le$, kurz $2 \le 5$
4 = 4 + 0 || mit $k = 0 \in \mathbb{N}$: also $4 \le 4$
2 = 5 + (-3) || das einzige passende $k$ ist $-3 \notin \mathbb{N}$: also gilt **nicht** $5 \le 2$
:::

:::achtung $\mathbb{N}$ beginnt im Skript bei $0$
Im Skript ist $\mathbb{N} = \{0, 1, 2, \ldots\}$ (im Vorkurs war es ab $1$). Nur weil $k = 0$
erlaubt ist, gilt $n \le n$. Mit $\mathbb{N} = \{1, 2, \ldots\}$ hätte die Formel die
Relation $<$ beschrieben.
:::

:::alt Als Treppe
Stell dir die natürlichen Zahlen als Treppenstufen vor. $n \le m$ heißt: Von Stufe $n$
erreichst du Stufe $m$, indem du $k$ Stufen **nach oben** gehst, wobei $k = 0$ (stehen
bleiben) erlaubt ist. Nach unten gehen ist verboten, denn negative $k$ gibt es in
$\mathbb{N}$ nicht.
:::
""")

k.menge("Auf $A = \\{1, 2, 3\\}$ ist $R = \\{(x, y) \\in A \\times A \\mid x < y\\}$. Gib $R$ als Menge von Paaren an, "
        "zum Beispiel `{(1; 2); (2; 2)}`.",
        "{(1; 2); (1; 3); (2; 3)}",
        "Gehe alle $9$ Paare aus $A \\times A$ durch und behalte die mit $x < y$: $(1, 2)$, $(1, 3)$, $(2, 3)$.",
        tipps=["$A \\times A$ hat $3 \\cdot 3 = 9$ Paare. Prüfe jedes.",
               "Die erste Komponente muss echt kleiner als die zweite sein.",
               "Es bleiben drei Paare, alle mit $x$ links und größerem $y$ rechts."],
        rechenweg=r"""
:::rechnung
1 < 2 || $(1, 2) \in R$
1 < 3 || $(1, 3) \in R$
2 < 3 || $(2, 3) \in R$
:::

Alle anderen Paare fallen heraus, zum Beispiel $(2, 1)$ wegen $2 > 1$ und $(2, 2)$ wegen $2 = 2$.
""",
        typische_fehler=[("{(1; 2); (1; 3); (2; 3); (1; 1); (2; 2); (3; 3)}",
                          "Das wäre $x \\le y$. Bei $x < y$ fallen die Paare $(x, x)$ heraus."),
                         ("{(2; 1); (3; 1); (3; 2)}",
                          "Die Reihenfolge im Paar zählt: $(x, y)$ mit $x < y$, also steht die kleinere Zahl **vorn**."),
                         ("{(1; 2); (2; 3)}", "Es fehlt $(1, 3)$: Auch $1 < 3$ gilt, nicht nur Nachbarn zählen.")])

k.luecke("Zeige mit Definition 1.36, dass $7 \\le 10$ gilt: Welches $k \\in \\mathbb{N}$ passt?",
         "10 = 7 + \\luecke", [[3]],
         "Gesucht ist $k \\in \\mathbb{N}$ mit $10 = 7 + k$, also $k = 3$. Weil $3 \\in \\mathbb{N}$, gilt $7 \\le 10$.",
         tipps=["Definition 1.36: $n \\le m$, wenn $m = n + k$ für ein $k \\in \\mathbb{N}$.",
                "Hier ist $n = 7$ und $m = 10$.", "$10 - 7$"],
         rechenweg=r"""
:::rechnung
10 = 7 + 3 || $k = 3 \in \mathbb{N}$, also $7 \le 10$
:::
""",
         typische_fehler=[([-3], "Du hast $7 - 10$ gerechnet. Gesucht ist $k$ mit $10 = 7 + k$, und $k$ muss in $\\mathbb{N}$ liegen."),
                          ([17], "Du hast addiert. Es soll $7 + k = 10$ gelten.")])

# ── Seite 3/4: Gerichteter Graph und Beispiel 1.37 ────────────────────────
k.erklaerung("Relationen zeichnen: der gerichtete Graph", r"""
## Knoten und Pfeile

Eine Relation $R$ auf einer endlichen Menge $M$ zeichnet man als [[gerichteter Graph]]:
ein Knoten (Punkt) für jedes $a \in M$ und ein Pfeil von $a$ nach $b$ genau dann, wenn $aRb$
gilt. Ein Pfeil von $a$ zu sich selbst ($aRa$) heißt **Schleife**.

Wo kein Zeichenblatt ist, hilft eine Tabelle: Zeile $a$, Spalte $b$, Haken bei $aRb$.
Beispiel: $R = \{(1, 1), (1, 2), (2, 3), (3, 3)\}$ auf $M = \{1, 2, 3\}$.

| $aRb$? | $b = 1$ | $b = 2$ | $b = 3$ |
|---|---|---|---|
| $a = 1$ | ✓ | ✓ | |
| $a = 2$ | | | ✓ |
| $a = 3$ | | | ✓ |

:::rechnung Vom Paar zum Pfeil
(1, 1) \in R || Schleife an Knoten $1$
(1, 2) \in R || Pfeil $1 \to 2$
(2, 3) \in R || Pfeil $2 \to 3$
(3, 3) \in R || Schleife an Knoten $3$; an $2$ gibt es keine Schleife
:::

:::alt Als Straßenkarte
Die Knoten sind Orte, die Pfeile sind Einbahnstraßen. $aRb$ heißt: Es gibt eine
Einbahnstraße direkt von $a$ nach $b$. Eine Schleife ist ein Kreisverkehr, der zum
selben Ort zurückführt. Ob du von $1$ über $2$ nach $3$ fahren kannst, ist eine andere
Frage als ob es die direkte Straße $1 \to 3$ gibt. Genau darum geht es später bei „transitiv“.
:::
---
## Beispiel 1.37: gemeinsame Elemente

Sei $M = \mathcal{P}(\{1, 2, 3\})$ die [[Potenzmenge]] (alle $8$ Teilmengen) und

$$S := \{(A, B) \in M \times M \mid A \cap B \neq \emptyset\}.$$

$A S B$ heißt also: $A$ und $B$ haben mindestens ein gemeinsames Element. Die Tabelle
listet zu jedem $A$ alle Partner $B$ (das Skript zeichnet dazu Abbildung 1.2):

| $A$ | alle $B$ mit $A S B$ |
|---|---|
§TABELLE§

:::rechnung Einzelne Paare prüfen
\{1\} \cap \{1, 2\} = \{1\} \neq \emptyset || also $\{1\} S \{1, 2\}$
\{1\} \cap \{2, 3\} = \emptyset || also **nicht** $\{1\} S \{2, 3\}$
\emptyset \cap \emptyset = \emptyset || $\emptyset$ steht zu keiner Menge in Relation, nicht einmal zu sich
49 - §DISJ§ = §ANZ§ || von den $7 \cdot 7$ Paaren nichtleerer Mengen sind §DISJ§ disjunkt: $S$ hat §ANZ§ Paare
:::

:::alt Als Gruppenchat
Jede Teilmenge ist eine Gruppe von Leuten aus $\{1, 2, 3\}$. Zwei Gruppen stehen in
Relation, wenn mindestens eine Person in beiden ist. Die leere Gruppe hat niemanden,
also teilt sie mit keiner Gruppe eine Person, auch nicht mit sich selbst.
:::
""".replace("§TABELLE§", _S_TABELLE).replace("§DISJ§", str(_S_DISJ)).replace("§ANZ§", str(_S_ANZ)))

k.menge("Bestimme in Beispiel 1.37 alle $B \\in \\mathcal{P}(\\{1, 2, 3\\})$ mit $\\{1\\} S B$. "
        "Eingabe als Menge von Mengen, zum Beispiel `{{1}; {2; 3}}`.",
        _mengen_text(_S_PARTNER_1),
        "Gesucht sind alle Teilmengen, die die $1$ enthalten: $\\{1\\}$, $\\{1, 2\\}$, $\\{1, 3\\}$, $\\{1, 2, 3\\}$.",
        tipps=["$\\{1\\} \\cap B \\neq \\emptyset$ heißt: $B$ und $\\{1\\}$ haben ein gemeinsames Element.",
               "Das einzige Element von $\\{1\\}$ ist $1$. Also muss $1 \\in B$ gelten.",
               "Es gibt vier Teilmengen von $\\{1, 2, 3\\}$, die die $1$ enthalten."],
        rechenweg=r"""
:::rechnung
\{1\} \cap \{1\} = \{1\} || nicht leer
\{1\} \cap \{1, 2\} = \{1\} || nicht leer
\{1\} \cap \{1, 3\} = \{1\} || nicht leer
\{1\} \cap \{1, 2, 3\} = \{1\} || nicht leer
\{1\} \cap \{2, 3\} = \emptyset || fällt heraus, ebenso $\emptyset$, $\{2\}$, $\{3\}$
:::
""",
        typische_fehler=[("{{1; 2}; {1; 3}; {1; 2; 3}}",
                          "Es fehlt $\\{1\\}$ selbst: $\\{1\\} \\cap \\{1\\} = \\{1\\} \\neq \\emptyset$."),
                         ("{{}; {1}; {1; 2}; {1; 3}; {1; 2; 3}}",
                          "$\\emptyset$ gehört nicht dazu: $\\{1\\} \\cap \\emptyset = \\emptyset$."),
                         ("{1}", "Gesucht sind Mengen $B$, nicht Elemente. Schreibe jede Menge in geschweiften Klammern.")])

# ── Seite 5/6: Die vier Eigenschaften ─────────────────────────────────────
k.erklaerung("Die vier Eigenschaften (Definition 1.38)", r"""
## Reflexiv und symmetrisch

**Definition 1.38.** Eine Relation $R$ auf einer Menge $X$ heißt

- (i) [[reflexiv]], falls $\forall x \in X : xRx$,
- (ii) [[symmetrisch]], falls $\forall x, y \in X : (xRy \Rightarrow yRx)$.

Reflexiv: **Jedes** Element steht zu sich selbst in Relation. Symmetrisch: Gilt es in eine
Richtung, dann auch in die andere. Für „nicht“ genügt jeweils **ein** [[Gegenbeispiel]].

:::rechnung $R = \{(1, 1), (1, 2), (2, 1), (2, 2)\}$ auf $X = \{1, 2, 3\}$
(3, 3) \notin R || nicht reflexiv: Gegenbeispiel $x = 3$
(1, 2) \in R,\ (2, 1) \in R || das einzige Paar mit $x \neq y$ hat seinen Partner
(1, 1), (2, 2) \in R || $(x, x)$ ist sein eigener Partner: symmetrisch
:::

:::alt Mit Händeschütteln erklärt
„Hat die Hand geschüttelt von“ ist symmetrisch: Wenn Ada Ben die Hand gibt, gibt Ben auch
Ada die Hand. „Ist verliebt in“ ist nicht symmetrisch, leider. Reflexiv wäre eine Relation,
wenn sich jede Person selbst die Hand schüttelt. Fehlt eine einzige Person, ist es vorbei.
:::
---
## Antisymmetrisch und transitiv

Def. 1.38 weiter: $R$ heißt

- (iii) [[antisymmetrisch]], falls $\forall x, y \in X : ((xRy \land yRx) \Rightarrow x = y)$,
- (iv) [[transitiv]], falls $\forall x, y, z \in X : ((xRy \land yRz) \Rightarrow xRz)$.

Antisymmetrisch: Hin **und** zurück geht nur von einem Element zu sich selbst. Transitiv:
Wer in zwei Schritten von $x$ über $y$ nach $z$ kommt, kommt auch direkt hin.

:::rechnung $R = \{(1, 2), (2, 3), (1, 3), (3, 3)\}$ auf $\{1, 2, 3\}$
(1, 2), (2, 3) \in R \Rightarrow (1, 3) \in R || Kette $1, 2, 3$: Abkürzung da
(1, 3), (3, 3) \in R \Rightarrow (1, 3) \in R || Kette $1, 3, 3$: das Ziel ist $(1, 3)$, da
(2, 3), (3, 3) \in R \Rightarrow (2, 3) \in R || Kette $2, 3, 3$: da; alle Ketten geprüft, transitiv
(1, 2) \in R,\ (2, 1) \notin R || kein Paar $x \neq y$ in beide Richtungen: antisymmetrisch
:::

:::achtung Antisymmetrisch heißt nicht „nicht symmetrisch“
Die Gleichheit $\{(1, 1), (2, 2)\}$ ist symmetrisch **und** antisymmetrisch. Die Relation
$\{(1, 2), (2, 1), (1, 3)\}$ ist keins von beiden. Prüfe jede Eigenschaft für sich.
:::

:::alt Mit einer Rangliste erklärt
„Ist mindestens so gut wie“ in einer Tabelle ohne Gleichstand: Wenn Team $x$ mindestens so
gut wie $y$ ist und $y$ mindestens so gut wie $x$, dann sind es dasselbe Team
(antisymmetrisch). Ist $x$ vor $y$ und $y$ vor $z$, dann ist $x$ vor $z$ (transitiv).
Ein „Schere, Stein, Papier“-Turnier ist dagegen nicht transitiv: Schere schlägt Papier,
Papier schlägt Stein, aber Schere schlägt nicht Stein.
:::
""")

_R_A = {(1, 1), (1, 2), (2, 1), (2, 2), (2, 3)}
assert [hat({1, 2, 3}, _R_A, e) for e in EIGENSCHAFTEN] == [False, False, False, False]
_R_B = {(1, 1), (2, 2), (3, 3), (1, 3)}
assert [hat({1, 2, 3}, _R_B, e) for e in EIGENSCHAFTEN] == [True, False, True, True]

k.mehrfach("Gegeben ist $R = \\{(1, 1), (2, 2), (3, 3), (1, 3)\\}$ auf $X = \\{1, 2, 3\\}$. Welche Eigenschaften hat $R$?",
           ["reflexiv", "antisymmetrisch", "transitiv"], ["symmetrisch"],
           "Alle drei Schleifen sind da (reflexiv). $(1, 3) \\in R$, aber $(3, 1) \\notin R$ (nicht symmetrisch). "
           "Kein Paar verschiedener Elemente in beide Richtungen (antisymmetrisch). Jede Kette, etwa $(1, 1), (1, 3)$ "
           "oder $(1, 3), (3, 3)$, endet in einem Paar, das schon in $R$ liegt (transitiv).",
           tipps=["Prüfe die vier Eigenschaften nacheinander.",
                  "Reflexiv: $(1, 1), (2, 2), (3, 3)$ da? Symmetrisch: Gibt es zu $(1, 3)$ auch $(3, 1)$?",
                  "Transitiv: Die einzigen Ketten benutzen Schleifen. Was ist dann die Abkürzung?"],
           fehler={"symmetrisch": "$(1, 3) \\in R$, aber $(3, 1) \\notin R$. Ein Paar ohne Gegenstück genügt als Gegenbeispiel."})

k.mc("Gegeben ist $R = \\{(1, 1), (1, 2), (2, 1), (2, 2), (2, 3)\\}$ auf $\\{1, 2, 3\\}$. Warum ist $R$ **nicht** transitiv?",
     ["Aus $(1, 2)$ und $(2, 3)$ müsste $(1, 3) \\in R$ folgen, das fehlt",
      "Aus $(1, 2)$ und $(2, 1)$ müsste $1 = 2$ folgen",
      "Es fehlt $(3, 3)$",
      "Zu $(2, 3)$ fehlt $(3, 2)$"],
     "Transitivität verlangt: $1R2$ und $2R3$ ergeben $1R3$. Das Paar $(1, 3)$ fehlt, das ist ein Gegenbeispiel.",
     tipps=["Transitiv: Für jede Kette $xRy$, $yRz$ muss $xRz$ gelten.",
            "Suche eine Kette, die mit $(2, 3)$ endet."],
     fehler={"Aus $(1, 2)$ und $(2, 1)$ müsste $1 = 2$ folgen":
             "Das ist die Bedingung für **antisymmetrisch**. Sie ist hier auch verletzt, beantwortet aber nicht die Frage nach der Transitivität.",
             "Es fehlt $(3, 3)$": "Das zeigt, dass $R$ nicht **reflexiv** ist. Für Transitivität brauchst du eine Kette ohne Abkürzung.",
             "Zu $(2, 3)$ fehlt $(3, 2)$": "Das zeigt, dass $R$ nicht **symmetrisch** ist. Gefragt ist nach transitiv."})

# ── Seite 7: Beispiel 1.39 ─────────────────────────────────────────────────
k.erklaerung("Beispiel 1.39: Die Relation ≤ auf ℕ", r"""
## Alle vier Eigenschaften mit Beweis

Jetzt prüfen wir $\le$ aus Definition 1.36. Jede Behauptung über **alle** Zahlen braucht
einen [[Beweis]], jedes „nicht“ ein Gegenbeispiel.

:::rechnung Beispiel 1.39 Schritt für Schritt
n = n + 0 \text{ mit } 0 \in \mathbb{N} || reflexiv: also $n \le n$ für jedes $n$
2 \le 5,\ 5 \not\le 2 || nicht symmetrisch: Gegenbeispiel
m = n + k,\ n = m + l \text{ mit } k, l \in \mathbb{N} || antisymmetrisch: Seien $n \le m$ und $m \le n$
n = n + k + l \text{ also } k + l = 0 || das zweite in das erste eingesetzt
k = l = 0 \text{ also } n = m || in $\mathbb{N}$ gibt es keine negativen Zahlen: beide sind $0$
m = n + k,\ p = m + l \text{ mit } k, l \in \mathbb{N} || transitiv: Seien $n \le m$ und $m \le p$
p = n + (k + l) \text{ mit } k + l \in \mathbb{N} || einsetzen; also $n \le p$
:::

Ergebnis: $\le$ ist reflexiv, antisymmetrisch und transitiv, aber nicht symmetrisch.

:::alt Mit Stufen auf einer Treppe
Reflexiv: Null Stufen gehen bringt dich auf deine Stufe. Antisymmetrisch: Wenn du von $n$
nach $m$ nur hochgehst und von $m$ nach $n$ auch nur hochgehst, bist du insgesamt
$k + l$ Stufen hoch und wieder am Start. Das geht nur mit $k = l = 0$. Transitiv: Erst $k$,
dann $l$ Stufen hoch sind zusammen $k + l$ Stufen hoch.
:::
""")

k.ordnen("Bringe den Beweis „$\\le$ auf $\\mathbb{N}$ ist transitiv“ (Beispiel 1.39) in die richtige Reihenfolge.",
         ["Seien $n, m, p \\in \\mathbb{N}$ mit $n \\le m$ und $m \\le p$.",
          "Nach Definition 1.36 gibt es $k, l \\in \\mathbb{N}$ mit $m = n + k$ und $p = m + l$.",
          "Einsetzen ergibt $p = (n + k) + l = n + (k + l)$.",
          "Wegen $k + l \\in \\mathbb{N}$ folgt $n \\le p$.",
          "Also ist $\\le$ transitiv. $\\square$"],
         "Ein Transitivitätsbeweis beginnt mit beliebigen $n, m, p$, für die die Voraussetzung gilt, übersetzt sie "
         "mit der Definition in Gleichungen und zeigt dann die Definition für $n \\le p$.",
         ablenker=["Nach Definition 1.36 gibt es ein $k \\in \\mathbb{N}$ mit $m = n + k$ und $p = m + k$.",
                   "Wähle $n = 1$, $m = 2$, $p = 3$. Dann gilt $1 \\le 3$."],
         tipps=["Ein Beweis über alle Zahlen beginnt mit „Seien …“.",
                "Für zwei verschiedene Ungleichungen brauchst du zwei verschiedene Zahlen $k$ und $l$.",
                "Ein einzelnes Zahlenbeispiel beweist keine Aussage über alle Zahlen."])

k.luecke("Antisymmetrie von $\\le$ (Beispiel 1.39): Aus $m = n + k$ und $n = m + l$ mit $k, l \\in \\mathbb{N}$ folgt "
         "$n = n + k + l$. Fülle die Lücken.",
         "k + l = \\luecke \\;\\Rightarrow\\; k = l = \\luecke \\;\\Rightarrow\\; m = n + \\luecke = n",
         [[0], [0], [0]],
         "Aus $n = n + k + l$ folgt $k + l = 0$. Zwei natürliche Zahlen mit Summe $0$ sind beide $0$. Also $m = n + 0 = n$.",
         tipps=["Ziehe auf beiden Seiten von $n = n + k + l$ die Zahl $n$ ab.",
                "Natürliche Zahlen sind nie negativ. Wann ist eine Summe zweier solcher Zahlen $0$?",
                "Alle drei Lücken haben denselben Wert."],
         rechenweg=r"""
:::rechnung
n = n + k + l \text{ also } k + l = 0 || $n$ auf beiden Seiten abziehen
k = l = 0 \text{ wegen } k, l \in \mathbb{N} || keine negativen Summanden
m = n + 0 \text{ also } m = n || einsetzen
:::
""")

# ── Seite 8: Am Graphen ablesen, Beispiel 1.41 ─────────────────────────────
k.erklaerung("Eigenschaften am Graphen ablesen", r"""
## Vier Blicke auf das Bild

Auf einer endlichen Menge liest du die Eigenschaften direkt am gerichteten Graphen ab:

| Eigenschaft | im Graphen |
|---|---|
| reflexiv | jeder Knoten hat eine Schleife |
| symmetrisch | zu jedem Pfeil gibt es den Gegenpfeil |
| antisymmetrisch | zwischen zwei verschiedenen Knoten nie Pfeile in beide Richtungen |
| transitiv | zu jedem Weg aus Pfeilen gibt es die Abkürzungskante |

**Beispiel 1.41.** Für $S$ aus Beispiel 1.37 (Abbildung 1.2 im Skript):

:::rechnung Beispiel 1.41
\emptyset \cap \emptyset = \emptyset || nicht reflexiv: $\emptyset$ hat keine Schleife
A \cap B \neq \emptyset \iff B \cap A \neq \emptyset || symmetrisch: Pfeile kommen in Gegenpaaren
\{1\} S \{1, 2\},\ \{1, 2\} S \{1\} || nicht antisymmetrisch, denn $\{1\} \neq \{1, 2\}$
\{1\} S \{1, 2\},\ \{1, 2\} S \{2\},\ \{1\} \cap \{2\} = \emptyset || nicht transitiv: die Abkürzung $\{1\} \to \{2\}$ fehlt
:::

:::alt Mit einem Netz aus Einbahnstraßen
Reflexiv: An jedem Ort gibt es einen Kreisverkehr. Symmetrisch: Jede Straße ist in
Wahrheit eine Straße mit Gegenverkehr. Antisymmetrisch: Zwischen zwei verschiedenen
Orten gibt es höchstens eine Richtung. Transitiv: Wer über einen Umweg von $x$ nach $z$
kommt, findet auch eine direkte Straße von $x$ nach $z$.
:::
""")

_R_G = {("a", "a"), ("b", "b"), ("c", "c"), ("a", "b"), ("b", "c"), ("a", "c")}
assert [hat({"a", "b", "c"}, _R_G, e) for e in EIGENSCHAFTEN] == [True, False, True, True]

k.zuordnen("Ordne jeder Eigenschaft zu, woran du sie im gerichteten Graphen erkennst.",
           [("reflexiv", "an jedem Knoten eine Schleife"),
            ("symmetrisch", "zu jedem Pfeil auch der Gegenpfeil"),
            ("antisymmetrisch", "zwischen verschiedenen Knoten nie Hin- und Rückpfeil"),
            ("transitiv", "zu jedem Weg aus zwei Pfeilen die Abkürzung")],
           "Das sind die vier Ableseregeln aus dem Skript direkt nach Beispiel 1.40.",
           ablenker=["jeder Knoten hat genau einen ausgehenden Pfeil"],
           tipps=["„Jeder Knoten hat genau einen ausgehenden Pfeil“ gehört zu Abbildungen (Abschnitt 1.7), nicht hierher."])

k.mc("Ein gerichteter Graph auf den Knoten $a, b, c$ hat Schleifen an allen drei Knoten und die Pfeile "
     "$a \\to b$, $b \\to c$, $a \\to c$. Welche Eigenschaft hat die Relation **nicht**?",
     ["symmetrisch", "reflexiv", "antisymmetrisch", "transitiv"],
     "Zum Pfeil $a \\to b$ fehlt der Gegenpfeil $b \\to a$, also nicht symmetrisch. Alle Schleifen sind da (reflexiv), "
     "nie Hin- und Rückpfeil (antisymmetrisch), und zum Weg $a \\to b \\to c$ gibt es die Abkürzung $a \\to c$ (transitiv).",
     tipps=["Gehe die vier Ableseregeln einzeln durch.", "Gibt es zu $a \\to b$ den Pfeil $b \\to a$?"],
     fehler={"transitiv": "Der einzige Weg aus zwei verschiedenen Pfeilen ist $a \\to b \\to c$, und die Abkürzung $a \\to c$ ist da. "
                          "Wege über Schleifen enden immer bei einem vorhandenen Pfeil.",
             "antisymmetrisch": "Zwischen zwei verschiedenen Knoten gibt es hier nie Pfeile in beide Richtungen. Das ist genau antisymmetrisch."})

# ── Seite 9: Beispiel 1.40 und die leere Bedingung ─────────────────────────
k.erklaerung("Beispiel 1.40: Wenn es nichts zu prüfen gibt", r"""
## Die Relation $<$ und die leere Bedingung

**Beispiel 1.40.** $< := \{(n, m) \in \mathbb{N} \times \mathbb{N} \mid n \le m \land n \neq m\}$ ist
nicht reflexiv (denn $0 < 0$ gilt nicht), nicht symmetrisch, aber transitiv.

Ist $<$ antisymmetrisch? Die Bedingung lautet: **Falls** $n < m$ und $m < n$, **dann** $n = m$.
Es gibt aber gar keine Paare mit $n < m$ und $m < n$. Eine Allaussage über die
[[leere Menge]] ist immer wahr: Alle ihre Elemente (nämlich keine) erfüllen die Bedingung.

:::rechnung Warum $<$ antisymmetrisch ist
\{(n, m) \in \mathbb{N} \times \mathbb{N} \mid n < m \land m < n\} = \emptyset || es gibt kein einziges solches Paar
\forall (n, m) \in \emptyset : n = m || über die leere Menge: wahr
:::

:::achtung Leer heißt wahr
Wer bei antisymmetrisch „kein Beispiel, also falsch“ denkt, liegt falsch. Dasselbe gilt
für transitiv: Gibt es keine einzige Kette $xRy$, $yRz$, ist $R$ transitiv. Die leere
Relation $\emptyset$ ist symmetrisch, antisymmetrisch und transitiv.
:::

:::alt Mit einer Hausordnung erklärt
„Wer nach 22 Uhr Musik macht, zahlt 10 Euro.“ Wenn niemand nach 22 Uhr Musik macht, hat
niemand die Regel gebrochen. Die Regel ist eingehalten, ganz ohne Beispiel. Genauso ist
eine Wenn-dann-Bedingung erfüllt, wenn das „Wenn“ nie eintritt: Aus Falschem folgt alles.
:::
""")

k.wf("Die leere Relation $R = \\emptyset$ auf $X = \\{1, 2\\}$ ist transitiv.", True,
     "Transitiv verlangt für jede Kette $xRy$, $yRz$ auch $xRz$. In $\\emptyset$ gibt es keine Kette, die Bedingung ist leer "
     "und damit erfüllt. Reflexiv ist $\\emptyset$ dagegen nicht: $(1, 1) \\notin \\emptyset$.",
     tipps=["Gibt es überhaupt Paare, auf die die Bedingung angewendet werden muss?"])

k.wf("Jede antisymmetrische Relation ist nicht symmetrisch.", False,
     "Gegenbeispiel: Die Gleichheit $\\{(1, 1), (2, 2)\\}$ auf $\\{1, 2\\}$ ist symmetrisch (jedes Paar ist sein eigenes "
     "Gegenstück) und antisymmetrisch (Hin und Zurück nur bei $x = y$).",
     tipps=["Denk an eine Relation, die nur aus Schleifen besteht."])


# ── Praxis ────────────────────────────────────────────────────────────────
def _rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def _zufallsrelation(rng, m):
    art = rng.choice(["zufall", "reflexiv", "symmetrisch", "aequivalenz", "ordnung", "streng"])
    paare = list(product(m, m))
    if art in ("zufall", "reflexiv", "symmetrisch"):
        r = {p for p in paare if rng.random() < 0.3}
        if art == "reflexiv":
            r |= {(x, x) for x in m}
        if art == "symmetrisch":
            r |= {(y, x) for x, y in r}
    elif art == "aequivalenz":
        klasse = {x: rng.randint(0, len(m) - 2) for x in m}
        r = {(x, y) for x in m for y in m if klasse[x] == klasse[y]}
    else:
        reihe = list(m)
        rng.shuffle(reihe)
        r = {(reihe[i], reihe[j]) for i in range(len(reihe)) for j in range(i + 1, len(reihe)) if rng.random() < 0.5}
        r, _ = transitiver_abschluss(r)
        if art == "ordnung":
            r |= {(x, x) for x in m}
    if rng.random() < 0.35:
        p = rng.choice(paare)
        r ^= {p}
    return r


def relation_eigenschaften(rng):
    m = [1, 2, 3] if rng.random() < 0.55 else [1, 2, 3, 4]
    while True:
        r = _zufallsrelation(rng, m)
        if 2 <= len(r) <= 9:
            break
    m_tex = _mtex(m)
    richtig = [e for e in EIGENSCHAFTEN if hat(m, r, e)]
    falsch = [e for e in EIGENSCHAFTEN if not hat(m, r, e)]
    zeilen = []
    for e in EIGENSCHAFTEN:
        g = gegenbeispiel(m, r, e)
        if g is None:
            grund = {"reflexiv": "alle Schleifen $(x, x)$ liegen in $R$",
                     "symmetrisch": "zu jedem Paar $(x, y) \\in R$ liegt auch $(y, x)$ in $R$",
                     "antisymmetrisch": "kein Paar verschiedener Elemente in beide Richtungen",
                     "transitiv": "jede Kette $xRy$, $yRz$ hat ihre Abkürzung $xRz$"}[e]
            zeilen.append((f"\\text{{{e}: ja}}", grund))
        else:
            zeilen.append((f"\\text{{{e}: nein}}", _gegen_text(e, g)))
    fehler = {e: "Gegenbeispiel: " + _gegen_text(e, gegenbeispiel(m, r, e)) for e in falsch}
    return {
        "frage": f"Gegeben ist die Relation $R = {_rel_tex(r)}$ auf $M = {m_tex}$. "
                 "Welche Eigenschaften hat $R$? Kreuze alle zutreffenden an (es können auch keine sein).",
        "richtig": richtig, "falsch": falsch, "fehler": fehler,
        "tipps": ["Prüfe jede Eigenschaft einzeln. Für „nein“ genügt ein Gegenbeispiel.",
                  "Reflexiv: alle $(x, x)$ da? Symmetrisch: zu jedem $(x, y)$ auch $(y, x)$?",
                  "Antisymmetrisch: nie $(x, y)$ und $(y, x)$ mit $x \\neq y$. Transitiv: Suche Ketten $(x, y), (y, z)$ "
                  "und prüfe $(x, z)$, auch für $z = x$."],
        "rechenweg": _rechnung(zeilen),
        "erklaerung": "Eine Eigenschaft gilt nur, wenn die Bedingung für **alle** Elemente erfüllt ist. "
                      "Ein einziges Gegenbeispiel widerlegt sie.",
    }


def fehlende_paare(rng):
    m = [1, 2, 3, 4]
    ziel = rng.choice(["reflexiv", "symmetrisch", "transitiv"])
    while True:
        r = {p for p in product(m, m) if rng.random() < 0.25}
        if not 3 <= len(r) <= 6:
            continue
        if ziel == "reflexiv":
            fehlt = {(x, x) for x in m} - r
            ok = 1 <= len(fehlt) <= 3
        elif ziel == "symmetrisch":
            fehlt = {(y, x) for x, y in r} - r
            ok = 1 <= len(fehlt) <= 4
        else:
            hull, runden = transitiver_abschluss(r)
            fehlt = hull - r
            ok = 1 <= len(fehlt) <= 4
        if ok:
            break
    zeilen, fehler = [], []
    if ziel == "reflexiv":
        for x, _ in sorted(fehlt):
            zeilen.append((f"({x}, {x}) \\notin R", f"Schleife an ${x}$ fehlt"))
        alle = {(x, x) for x in m}
        if alle != fehlt:
            fehler.append((alle, "Paare, die schon in $R$ liegen, musst du nicht hinzufügen. Gesucht sind nur die fehlenden."))
    elif ziel == "symmetrisch":
        for x, y in sorted(fehlt):
            zeilen.append((f"({y}, {x}) \\in R,\\ ({x}, {y}) \\notin R", f"Gegenpaar zu $({y}, {x})$ fehlt"))
        umgedreht = {(y, x) for x, y in r}
        if umgedreht != fehlt:
            fehler.append((umgedreht, "Du hast alle umgedrehten Paare angegeben. Manche davon liegen schon in $R$."))
        fehler.append((r, "Das ist $R$ selbst. Gesucht sind die Paare, die noch **fehlen**."))
    else:
        hull, runden = transitiver_abschluss(r)
        bekannt = set(r)
        for i, runde in enumerate(runden):
            for x, z in runde:
                y = next(y for (a, y) in sorted(bekannt) if a == x and (y, z) in bekannt)
                neu = " (eben hinzugefügt)" if i > 0 else ""
                zeilen.append((f"({x}, {y}), ({y}, {z}) \\in R \\Rightarrow ({x}, {z})",
                               f"Abkürzung fehlt{neu}"))
            bekannt |= set(runde)
        if len(runden) > 1:
            fehler.append((set(runden[0]), "Nach dem Hinzufügen entstehen neue Ketten. Wiederhole die Suche, bis keine "
                                           "Abkürzung mehr fehlt."))
        ohne_diag = {(x, z) for x, z in fehlt if x != z}
        if ohne_diag != fehlt and ohne_diag:
            fehler.append((ohne_diag, "Auch Schleifen können fehlen: Aus $xRy$ und $yRx$ folgt mit Transitivität $xRx$."))
    fehler.append((r | fehlt, "Das ist die ganze neue Relation. Gesucht sind nur die Paare, die **hinzukommen**."))
    if len(fehlt) >= 2:
        fehler.append((set(sorted(fehlt)[:-1]), "Es fehlt noch mindestens ein Paar. Prüfe jedes Element bzw. jede Kette einzeln."))
    gesehen, tf = {frozenset(fehlt)}, []
    for menge, text in fehler:
        if frozenset(menge) not in gesehen:
            gesehen.add(frozenset(menge))
            tf.append((_rel_text(menge), text))
    return {
        "frage": f"Auf $M = {_mtex(m)}$ ist $R = {_rel_tex(r)}$ gegeben. Welche Paare musst du **mindestens** zu $R$ "
                 f"hinzufügen, damit die Relation {ziel} wird? Gib die Menge der fehlenden Paare an, zum Beispiel "
                 "`{(1; 2); (3; 3)}`.",
        "loesung": _rel_text(fehlt),
        "tipps": {"reflexiv": ["Reflexiv heißt: $(x, x) \\in R$ für jedes $x \\in M$.",
                               "Prüfe $(1, 1)$, $(2, 2)$, $(3, 3)$, $(4, 4)$.",
                               "Gib nur die Schleifen an, die noch fehlen."],
                  "symmetrisch": ["Symmetrisch heißt: Zu jedem $(x, y) \\in R$ muss $(y, x) \\in R$ liegen.",
                                  "Drehe jedes Paar um und schau, ob es schon da ist.",
                                  "Schleifen $(x, x)$ sind ihr eigenes Gegenpaar."],
                  "transitiv": ["Suche alle Ketten $(x, y), (y, z)$ in $R$ und prüfe, ob $(x, z)$ da ist.",
                                "Vergiss Ketten mit $z = x$ nicht: Aus $(1, 2), (2, 1)$ folgt $(1, 1)$.",
                                "Neu hinzugefügte Paare können neue Ketten bilden. Suche weiter, bis nichts mehr fehlt."]}[ziel],
        "rechenweg": _rechnung(zeilen),
        "erklaerung": {"reflexiv": "Für Reflexivität fehlen genau die Schleifen, die nicht in $R$ liegen.",
                       "symmetrisch": "Für Symmetrie fehlen genau die umgedrehten Paare, die nicht schon in $R$ liegen.",
                       "transitiv": "Für Transitivität fügst du so lange Abkürzungen hinzu, bis jede Kette ihre "
                                    "Abkürzung hat. Das Ergebnis ist die kleinste transitive Relation, die $R$ enthält."}[ziel],
        "typische_fehler": tf,
    }


k.praxis()

k.generator(relation_eigenschaften, typ="mehrfach", titel="Eigenschaften einer Relation bestimmen")
k.generator(fehlende_paare, typ="menge", titel="Fehlende Paare ergänzen")

k.rechenweg_aufgabe(r"""
## Quiz-Stil: eine Relation auf ℤ

Auf $\mathbb{Z}$ ist die Relation $T := \{(x, y) \in \mathbb{Z} \times \mathbb{Z} \mid x \cdot y > 0\}$ gegeben
(„$x$ und $y$ haben dasselbe Vorzeichen und sind nicht $0$“).
""",
    [{"typ": "mc", "frage": "Ist $T$ reflexiv?",
      "optionen": ["Nein, denn $0 \\cdot 0 = 0$, also $(0, 0) \\notin T$", "Ja, denn $x \\cdot x = x^2 > 0$",
                   "Nein, denn $(-1) \\cdot 1 < 0$"],
      "fehler": {"Ja, denn $x \\cdot x = x^2 > 0$": "$x^2 > 0$ gilt für alle $x \\neq 0$, aber nicht für $x = 0$. Ein Gegenbeispiel genügt.",
                 "Nein, denn $(-1) \\cdot 1 < 0$": "Reflexiv betrifft nur Paare $(x, x)$. Das Paar $(-1, 1)$ ist dafür kein Gegenbeispiel."},
      "tipps": ["Reflexiv: $(x, x) \\in T$ für **jedes** $x \\in \\mathbb{Z}$.", "Teste $x = 0$."],
      "erklaerung": "$0 \\cdot 0 = 0$ ist nicht $> 0$."},
     {"typ": "wf", "frage": "$T$ ist symmetrisch.", "wahr": True,
      "tipps": ["Ist $x \\cdot y$ dasselbe wie $y \\cdot x$?"],
      "erklaerung": "$x \\cdot y > 0 \\Rightarrow y \\cdot x > 0$, weil die Multiplikation kommutativ ist."},
     {"typ": "mc", "frage": "Ist $T$ transitiv?",
      "optionen": ["Ja: Aus $xy > 0$ und $yz > 0$ folgt $x y^2 z > 0$, also $xz > 0$ wegen $y^2 > 0$",
                   "Nein: $(1, 2), (2, -1)$ ist ein Gegenbeispiel",
                   "Nein, weil $T$ nicht reflexiv ist"],
      "fehler": {"Nein: $(1, 2), (2, -1)$ ist ein Gegenbeispiel": "$(2, -1) \\notin T$, denn $2 \\cdot (-1) = -2 < 0$. Das ist keine Kette in $T$.",
                 "Nein, weil $T$ nicht reflexiv ist": "Die vier Eigenschaften sind unabhängig. Eine Relation kann transitiv sein, ohne reflexiv zu sein."},
      "tipps": ["Multipliziere die beiden Ungleichungen $xy > 0$ und $yz > 0$.", "In einer Kette in $T$ ist $y \\neq 0$, also $y^2 > 0$."],
      "erklaerung": "$(xy)(yz) = xz \\cdot y^2 > 0$ und $y^2 > 0$, also $xz > 0$."},
     {"typ": "wf", "frage": "$T$ ist antisymmetrisch.", "wahr": False,
      "tipps": ["Suche zwei verschiedene Zahlen $x, y$ mit $xTy$ und $yTx$."],
      "erklaerung": "$1 \\cdot 2 > 0$ und $2 \\cdot 1 > 0$, aber $1 \\neq 2$."}],
    "Ergebnis: $T$ ist symmetrisch und transitiv, aber weder reflexiv (wegen $0$) noch antisymmetrisch.",
    uebungsblatt=True,
    tipps=["Prüfe jede Eigenschaft einzeln. Achte auf die Zahl $0$.",
           "Für transitiv: Multipliziere die beiden Bedingungen."],
    rechenweg=r"""
:::rechnung
0 \cdot 0 = 0 || nicht $> 0$: $(0, 0) \notin T$, nicht reflexiv
x \cdot y = y \cdot x || symmetrisch
(x y)(y z) = x z \cdot y^2 || für transitiv: beide Seiten $> 0$ und $y^2 > 0$, also $xz > 0$
1 \cdot 2 = 2 \cdot 1 = 2 || $1T2$ und $2T1$ mit $1 \neq 2$: nicht antisymmetrisch
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Teilbarkeit als Relation

Auf $\mathbb{N}$ sei $n \mid m :\iff \exists k \in \mathbb{N} : m = k \cdot n$ („$n$ teilt $m$“).

1. Zeigen Sie, dass $\mid$ reflexiv und transitiv ist.
2. Zeigen Sie, dass $\mid$ antisymmetrisch, aber nicht symmetrisch ist. (Vorsicht bei $n = 0$.)
3. Auf $\mathbb{Z}$ definiert man $n \mid m :\iff \exists k \in \mathbb{Z} : m = k \cdot n$. Ist diese Relation
   antisymmetrisch?
""",
    r"""
**1. Reflexiv:** Für $n \in \mathbb{N}$ ist $n = 1 \cdot n$ mit $1 \in \mathbb{N}$, also $n \mid n$.
**Transitiv:** Seien $n \mid m$ und $m \mid p$. Dann gibt es $k, l \in \mathbb{N}$ mit $m = k n$ und
$p = l m$. Einsetzen: $p = l (k n) = (l k) \cdot n$ mit $l k \in \mathbb{N}$, also $n \mid p$.

**2. Nicht symmetrisch:** $1 \mid 2$ (denn $2 = 2 \cdot 1$), aber nicht $2 \mid 1$, denn $1 = k \cdot 2$
hat keine Lösung $k \in \mathbb{N}$.
**Antisymmetrisch:** Seien $n \mid m$ und $m \mid n$, also $m = k n$ und $n = l m$ mit $k, l \in \mathbb{N}$.
*Fall $n = 0$:* Dann $m = k \cdot 0 = 0 = n$.
*Fall $n \neq 0$:* Aus $n = l k n$ folgt durch Kürzen $l k = 1$. In $\mathbb{N}$ geht das nur mit
$l = k = 1$, also $m = n$. In beiden Fällen ist $m = n$. $\square$

**3.** Nein: $1 \mid -1$ (denn $-1 = (-1) \cdot 1$) und $-1 \mid 1$ (denn $1 = (-1) \cdot (-1)$), aber $1 \neq -1$.
Auf $\mathbb{Z}$ ist die Teilbarkeit also nicht antisymmetrisch.
""",
    ["Reflexiv mit $k = 1$ begründet",
     "Transitiv: zwei verschiedene Faktoren $k, l$ benutzt und $p = (lk) \\cdot n$ hergeleitet",
     "Nicht symmetrisch mit einem konkreten Gegenbeispiel gezeigt",
     "Antisymmetrie mit Fallunterscheidung $n = 0$ und $n \\neq 0$ bewiesen (Kürzen nur für $n \\neq 0$)",
     "Für $\\mathbb{Z}$ das Gegenbeispiel $1$ und $-1$ gefunden"],
    "Beweise über alle Zahlen beginnen mit „Seien …“. Jede Widerlegung braucht ein konkretes Gegenbeispiel. "
    "Kürzen durch $n$ ist nur für $n \\neq 0$ erlaubt, darum die Fallunterscheidung.",
    uebungsblatt=True,
    tipps=["Für antisymmetrisch: Setze $m = kn$ in $n = lm$ ein und unterscheide $n = 0$ und $n \\neq 0$."])

k.zusammenfassung(r"""
## Relationen (Skript Abschn. 1.6, Def. 1.35 bis Bsp. 1.41)

- **Relation** zwischen $N$ und $M$: Teilmenge $R \subseteq N \times M$; $xRy :\iff (x, y) \in R$. Für $N = M$: Relation auf $M$.
- $\le\ = \{(n, m) \in \mathbb{N}^2 \mid \exists k \in \mathbb{N} : m = n + k\}$ (Def. 1.36), $\mathbb{N} = \{0, 1, 2, \ldots\}$.
- **Gerichteter Graph:** Knoten je Element, Pfeil $a \to b$ bei $aRb$, Schleife bei $aRa$.

| Eigenschaft (Def. 1.38) | Formel | im Graphen |
|---|---|---|
| reflexiv | $\forall x : xRx$ | überall Schleifen |
| symmetrisch | $\forall x, y : xRy \Rightarrow yRx$ | Pfeile in Gegenpaaren |
| antisymmetrisch | $\forall x, y : (xRy \land yRx) \Rightarrow x = y$ | nie Hin und Zurück zwischen verschiedenen Knoten |
| transitiv | $\forall x, y, z : (xRy \land yRz) \Rightarrow xRz$ | jede Abkürzung vorhanden |

- $\le$ auf $\mathbb{N}$: reflexiv, antisymmetrisch, transitiv, nicht symmetrisch (Bsp. 1.39).
- $<$ auf $\mathbb{N}$: nicht reflexiv, nicht symmetrisch, antisymmetrisch (leere Bedingung!), transitiv (Bsp. 1.40).
- $A S B :\iff A \cap B \neq \emptyset$ auf $\mathcal{P}(\{1, 2, 3\})$: nur symmetrisch (Bsp. 1.37, 1.41).

!! Für „gilt“ brauchst du einen Beweis für alle Elemente, für „gilt nicht“ ein einziges Gegenbeispiel.
""")
