# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 6: Ordnungen, Supremum und Infimum (Skript Disser WS 26/27, Abschn. 1.6,
Def. 1.42 bis Satz 1.58)."""
import json
import math
from itertools import combinations

from ..engine import neues_kapitel

k = neues_kapitel(
    slug="ordnungen",
    titel="Ordnungen, Supremum und Infimum",
    beschreibung="Ordnungsrelation, partiell und total geordnete Mengen, Maximum und Minimum, Schranken, sup und inf, Satz 1.58",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 1.6",
    icon="🪜")


# ── Hilfsfunktionen: Python rechnet Schranken, sup, inf, max, min ─────────
def teilmenge(a, b):
    return a <= b


def teilt(a, b):
    return b % a == 0


def ist_ordnung(m, leq):
    m = list(m)
    refl = all(leq(x, x) for x in m)
    anti = all(x == y for x in m for y in m if leq(x, y) and leq(y, x))
    trans = all(leq(x, z) for x in m for y in m for z in m if leq(x, y) and leq(y, z))
    return refl and anti and trans


def ist_total(m, leq):
    return all(leq(x, y) or leq(y, x) for x in m for y in m)


def obere(m, leq, n):
    return [x for x in m if all(leq(y, x) for y in n)]


def untere(m, leq, n):
    return [x for x in m if all(leq(x, y) for y in n)]


def minimum(leq, s):
    kand = [x for x in s if all(leq(x, y) for y in s)]
    return kand[0] if kand else None


def maximum(leq, s):
    kand = [x for x in s if all(leq(y, x) for y in s)]
    return kand[0] if kand else None


def sup(m, leq, n):
    return minimum(leq, obere(m, leq, n))


def inf(m, leq, n):
    return maximum(leq, untere(m, leq, n))


def potenzmenge(g):
    g = sorted(g)
    return [frozenset(c) for r in range(len(g) + 1) for c in combinations(g, r)]


def mtex(s):
    return "\\emptyset" if not s else "\\{" + ", ".join(str(x) for x in sorted(s)) + "\\}"


def mtext(s):
    return "{" + "; ".join(str(x) for x in sorted(s)) + "}"


def familie_tex(f):
    return "\\{" + ", ".join(mtex(a) for a in f) + "\\}"


def familie_text(f):
    return "{" + "; ".join(mtext(a) for a in f) + "}"


def _sortiert(f):
    return sorted(f, key=lambda a: (len(a), sorted(a)))


# Beispiele 1.51 und 1.57 nachrechnen
_P012 = potenzmenge({0, 1, 2})


def _hasse_bild(teil, titel, unterschrift):
    """Hasse-Diagramm von (P({0, 1, 2}), ⊆) mit hervorgehobener Teilmenge (Abbildung 1.3)."""
    el = [sorted(a) for a in sorted(_P012, key=lambda a: (len(a), sorted(a)))]
    return ":::visual hasse\n" + json.dumps({
        "elemente": el, "paare": [[a, b] for a in el for b in el if set(a) <= set(b)],
        "teilmenge": [sorted(a) for a in teil], "titel": titel, "unterschrift": unterschrift}, ensure_ascii=False) + "\n:::"


_BILD_A = _hasse_bild([{0}, {1}, {0, 1}], "$A$ in $(\\mathcal{P}(\\{0, 1, 2\\}), \\subseteq)$ (Abbildung 1.3)",
                      "Schwarz: $A$. Unter $\\{0, 1\\}$ liegen $\\{0\\}$ und $\\{1\\}$, die beiden sind nicht vergleichbar.")
_BILD_B = _hasse_bild([set(), {0}, {1}, {1, 2}], "$B$ in $(\\mathcal{P}(\\{0, 1, 2\\}), \\subseteq)$ (Abbildung 1.3)",
                      "Schwarz: $B$. Von $\\emptyset$ führt ein Weg nach oben zu jedem Element von $B$, aber kein Element von $B$ liegt über allen.")
assert ist_ordnung(_P012, teilmenge) and not ist_total(_P012, teilmenge)
_A = [frozenset({0}), frozenset({1}), frozenset({0, 1})]
_B = [frozenset(), frozenset({0}), frozenset({1}), frozenset({1, 2})]
assert maximum(teilmenge, _A) == frozenset({0, 1}) and minimum(teilmenge, _A) is None
assert minimum(teilmenge, _B) == frozenset() and maximum(teilmenge, _B) is None
_A_OBEN = _sortiert(obere(_P012, teilmenge, _A))
assert _A_OBEN == [frozenset({0, 1}), frozenset({0, 1, 2})]
assert sup(_P012, teilmenge, _A) == frozenset({0, 1}) and inf(_P012, teilmenge, _A) == frozenset()
assert inf(_P012, teilmenge, _B) == frozenset() and sup(_P012, teilmenge, _B) == frozenset({0, 1, 2})
_N2 = [frozenset({0}), frozenset({1})]
_N2_OBEN = _sortiert(obere(_P012, teilmenge, _N2))
# Teiler von 12
_T12 = [d for d in range(1, 13) if 12 % d == 0]
assert ist_ordnung(_T12, teilt) and not ist_total(_T12, teilt)
assert sup(_T12, teilt, [4, 6]) == 12 and inf(_T12, teilt, [4, 6]) == 2 and maximum(teilt, [4, 6]) is None

k.lernziele([
    "Ich kann prüfen, ob eine Relation eine Ordnungsrelation ist, und partiell von total geordnet unterscheiden (Def. 1.42, Bsp. 1.43, 1.44)",
    "Ich kann Maximum und Minimum bestimmen und beweisen, dass es höchstens eins gibt (Def. 1.46, Satz 1.47)",
    "Ich kann obere und untere Schranken, Supremum und Infimum bestimmen, auch in $(\\mathcal{P}(M), \\subseteq)$ (Def. 1.52, 1.53)",
    "Ich kann Satz 1.58 anwenden und beweisen: Das Maximum existiert genau dann, wenn $\\sup N$ existiert und in $N$ liegt",
])

k.warum(r"""
Sortieren, Versionsnummern, Abhängigkeiten im Build-System, Klassenhierarchien: Überall
steckt eine Ordnung. Bei Aufgaben mit Abhängigkeiten ist sie meist nur **partiell**, darum
gibt es mehrere gültige Reihenfolgen (topologisches Sortieren). Supremum und Infimum sind
die Grundlage für Grenzwerte in Kapitel 7 und für den „Join“ zweier Typen in
Programmiersprachen: der kleinste gemeinsame Obertyp ist ein Supremum.
""")

# ── Seite 1: Ordnungsrelation ─────────────────────────────────────────────
k.erklaerung("Ordnungsrelationen", r"""
## Reflexiv, antisymmetrisch, transitiv

**Definition 1.42.** Eine Relation $R$ auf $M$ heißt [[Ordnungsrelation]], falls sie
[[reflexiv]], [[antisymmetrisch]] und [[transitiv]] ist. Man schreibt dann oft
$\preccurlyeq\ := R$ und nennt $(M, \preccurlyeq)$ eine [[partiell geordnete Menge]].
Gilt zusätzlich $\forall x, y \in M : x \preccurlyeq y \lor y \preccurlyeq x$, heißt $\preccurlyeq$
eine [[Totalordnung]].

**Beispiel 1.43.** $\le$ auf $\mathbb{N}$, $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{R}$ ist jeweils eine Totalordnung.
**Beispiel 1.44.** $\subseteq$ ist auf jeder [[Potenzmenge]] $\mathcal{P}(M)$ eine Ordnungsrelation.

:::rechnung $\subseteq$ auf $\mathcal{P}(M)$ prüfen
A \subseteq A || reflexiv: jedes Element von $A$ liegt in $A$
A \subseteq B \land B \subseteq A \Rightarrow A = B || antisymmetrisch: Gleichheit von Mengen
A \subseteq B \land B \subseteq C \Rightarrow A \subseteq C || transitiv
\{1\} \not\subseteq \{2\},\ \{2\} \not\subseteq \{1\} || nicht total: unvergleichbar
:::

:::achtung „Partiell“ heißt nicht „nicht total“
Jede Totalordnung ist auch partiell geordnet. „Partiell“ erlaubt unvergleichbare Elemente,
verlangt sie aber nicht.
:::

:::alt Mit einem Stammbaum erklärt
„Ist Vorfahre von oder gleich“ ist eine Ordnung: Jeder ist sein eigener „Vorfahre oder
gleich“, zwei Personen können nicht gegenseitig Vorfahren voneinander sein, und der
Vorfahre eines Vorfahren ist ein Vorfahre. Aber Geschwister sind unvergleichbar: Keine ist
Vorfahrin der anderen. Darum ist die Ordnung nur partiell.
:::
---
## Teilmengen erben die Ordnung

**Beobachtung 1.45.** Ist $(M, \preccurlyeq)$ partiell (oder total) geordnet, dann auch
$(N, \preccurlyeq)$ für jede Teilmenge $N \subseteq M$. Die drei Bedingungen gelten für alle
Elemente von $M$, also erst recht für die von $N$.

Beispiel: Die Teilbarkeit $\mid$ ist auf $\mathbb{N}$ eine Ordnung (Übungsblatt in Kapitel
„Relationen“), also auch auf den Teilern von $12$, $T = \{1, 2, 3, 4, 6, 12\}$.

:::rechnung Vergleichbar oder nicht?
12 = 3 \cdot 4 || $4 \mid 12$: vergleichbar
6 = 3 \cdot 2 || $2 \mid 6$: vergleichbar
4 \nmid 6,\ 6 \nmid 4 || unvergleichbar: $(T, \mid)$ ist nicht total
1 \mid 2 \mid 4 \mid 12 || auf $\{1, 2, 4, 12\}$ ist $\mid$ total (eine Kette)
:::

:::alt Mit Versionsständen erklärt
Ein Git-Verlauf mit Verzweigungen: „Commit $a$ ist Vorgänger von $b$ oder gleich“ ordnet die
Commits. Zwei Commits auf verschiedenen Zweigen sind unvergleichbar. Schaust du nur einen
einzelnen Zweig an (eine Teilmenge), sind dort alle Commits vergleichbar: Die Teilmenge
erbt die Ordnung und ist sogar total geordnet.
:::
""")

k.wf("Jede total geordnete Menge ist auch eine partiell geordnete Menge.", True,
     "Eine Totalordnung ist nach Definition 1.42 eine Ordnungsrelation mit einer **zusätzlichen** Eigenschaft. "
     "Also ist $(M, \\preccurlyeq)$ dann insbesondere partiell geordnet.",
     tipps=["Lies Definition 1.42: „Gilt zusätzlich …“."])

_T12_KETTEN = {"$\\{1, 2, 4, 12\\}$": [1, 2, 4, 12], "$\\{1, 3, 6, 12\\}$": [1, 3, 6, 12], "$\\{2, 6\\}$": [2, 6]}
_T12_NICHT = {"$\\{2, 3\\}$": [2, 3], "$\\{4, 6, 12\\}$": [4, 6, 12], "$\\{1, 2, 3, 6\\}$": [1, 2, 3, 6]}
assert all(ist_total(v, teilt) for v in _T12_KETTEN.values())
assert not any(ist_total(v, teilt) for v in _T12_NICHT.values())

k.mehrfach("Welche Teilmengen von $T = \\{1, 2, 3, 4, 6, 12\\}$ sind mit der Teilbarkeit $\\mid$ **total** geordnet?",
           list(_T12_KETTEN), list(_T12_NICHT),
           "Total heißt: Je zwei Elemente sind vergleichbar. In $\\{2, 3\\}$ teilt weder $2$ die $3$ noch umgekehrt. "
           "In $\\{4, 6, 12\\}$ sind $4$ und $6$ unvergleichbar, in $\\{1, 2, 3, 6\\}$ die $2$ und die $3$.",
           tipps=["Prüfe für jedes Paar: Teilt die kleinere Zahl die größere?",
                  "Ein einziges unvergleichbares Paar macht die Teilmenge nicht total.",
                  "Achte auf $2$ und $3$ sowie $4$ und $6$."],
           fehler={"$\\{4, 6, 12\\}$": "$12$ ist zwar mit beiden vergleichbar, aber $4 \\nmid 6$ und $6 \\nmid 4$.",
                   "$\\{1, 2, 3, 6\\}$": "$2 \\nmid 3$ und $3 \\nmid 2$: unvergleichbar.",
                   "$\\{2, 3\\}$": "Weder $2 \\mid 3$ noch $3 \\mid 2$."})

# ── Seite 3: Maximum und Minimum ──────────────────────────────────────────
k.erklaerung("Maximum und Minimum", r"""
## Größtes und kleinstes Element

**Definition 1.46.** Sei $(M, \preccurlyeq)$ partiell geordnet. $x \in M$ heißt
[[Maximum]] von $(M, \preccurlyeq)$, falls $y \preccurlyeq x$ für **alle** $y \in M$, und
[[Minimum]], falls $x \preccurlyeq y$ für alle $y \in M$.

**Satz 1.47.** Jede partiell geordnete Menge hat höchstens ein Maximum und höchstens ein Minimum.

*Beweis.* Seien $x, y$ beide Maxima. Da $y$ Maximum ist und $x \in M$, gilt $x \preccurlyeq y$.
Da $x$ Maximum ist, gilt $y \preccurlyeq x$. Antisymmetrie liefert $x = y$. Für Minima genauso. $\square$

**Definition 1.48.** Existieren sie, heißen sie $\max M$ und $\min M$.

:::rechnung Beispiele 1.49 und 1.50
\max\, (0, 1] = 1 || $I = \{x \in \mathbb{R} \mid 0 < x \le 1\}$: $1 \in I$, alle $x \in I$ sind $\le 1$
\min \mathbb{N} = 0 || $0 \le n$ für alle $n \in \mathbb{N}$
\frac{x}{2} < x \text{ für } x \in I || $I$ hat kein Minimum: zu jedem $x \in I$ liegt $\frac{x}{2}$ noch in $I$
n + 1 > n \text{ für } n \in \mathbb{N} || $\mathbb{N}$ hat kein Maximum
:::

:::alt Mit einem Siegertreppchen
Das Maximum ist wie ein Sieger, der gegen **jeden** im Feld gewonnen hat, auch gegen
sich selbst „unentschieden“. Zwei solche Sieger hätten gegeneinander gewonnen und verloren,
also sind sie dieselbe Person (Antisymmetrie). In $(0, 1]$ gibt es keinen Letzten: Wer auch
immer unten steht, die Hälfte seiner Zahl steht noch darunter.
:::
---
## Beispiel 1.51: In $(\mathcal{P}(\{0, 1, 2\}), \subseteq)$

$(\mathcal{P}(\{0, 1, 2\}), \subseteq)$ hat das Maximum $\{0, 1, 2\}$ und das Minimum $\emptyset$.
Nach Beobachtung 1.45 sind auch Teilmengen davon partiell geordnet. Das Hasse-Diagramm zeigt
die Ordnung: Eine Linie nach oben heißt „kleiner oder gleich“. Hervorgehoben (schwarz) sind
die beiden Teilmengen $A$ und $B$ aus Abbildung 1.3:

§A§

§B§

:::rechnung Beispiel 1.51 (Abbildung 1.3 im Skript)
A = \{\{0\}, \{1\}, \{0, 1\}\} || betrachte $(A, \subseteq)$
\{0\} \subseteq \{0, 1\},\ \{1\} \subseteq \{0, 1\} || $\max A = \{0, 1\}$
\{0\} \not\subseteq \{1\},\ \{1\} \not\subseteq \{0\} || kein Element liegt unter beiden: kein Minimum
B = \{\emptyset, \{0\}, \{1\}, \{1, 2\}\} || betrachte $(B, \subseteq)$
\emptyset \subseteq X \text{ für alle } X \in B || $\min B = \emptyset$
\{0\} \not\subseteq \{1, 2\} || kein Element liegt über allen: kein Maximum
:::

:::achtung Kein Maximum, obwohl nichts darüber liegt
In $B$ liegt über $\{0\}$ kein anderes Element von $B$, über $\{1, 2\}$ auch nicht. Trotzdem
ist keins von beiden ein Maximum, denn ein Maximum muss über **allen** liegen.
:::

:::alt Mit zwei Bergspitzen
Ein Gebirge mit zwei Gipfeln, die nicht vergleichbar sind (jeder auf seiner eigenen Seite).
Auf keinem Gipfel ist es weiter nach oben möglich, aber keiner überblickt den anderen. Ein
Maximum wäre ein Gipfel, von dem aus alles darunter liegt. Den gibt es hier nicht.
:::
""".replace("§A§", _BILD_A).replace("§B§", _BILD_B))

k.mc("Welche Aussage über $(\\{\\{0\\}, \\{1\\}, \\{0, 1\\}\\}, \\subseteq)$ stimmt (Beispiel 1.51)?",
     ["Maximum $\\{0, 1\\}$, kein Minimum", "Maximum $\\{0, 1\\}$, Minimum $\\emptyset$",
      "Minimum $\\{0\\}$ und Minimum $\\{1\\}$", "kein Maximum, kein Minimum"],
     "$\\{0\\} \\subseteq \\{0, 1\\}$ und $\\{1\\} \\subseteq \\{0, 1\\}$: Maximum $\\{0, 1\\}$. Ein Minimum müsste in der Menge liegen "
     "und unter $\\{0\\}$ und $\\{1\\}$ liegen. Das kann nur $\\emptyset$, und das ist kein Element.",
     tipps=["Maximum und Minimum müssen **Elemente der Menge** sein.", "Liegt $\\{0\\}$ unter $\\{1\\}$?"],
     fehler={"Maximum $\\{0, 1\\}$, Minimum $\\emptyset$": "$\\emptyset$ ist hier kein Element der Menge. Ein Minimum muss dazugehören. "
                                                          "($\\emptyset$ ist aber das Infimum, siehe später.)",
             "Minimum $\\{0\\}$ und Minimum $\\{1\\}$": "Nach Satz 1.47 gibt es höchstens ein Minimum. Und $\\{0\\} \\not\\subseteq \\{1\\}$."})

k.ordnen("Ordne den Beweis von Satz 1.47 für Minima.",
         ["Seien $x$ und $y$ Minima von $(M, \\preccurlyeq)$.",
          "Da $x$ ein Minimum ist und $y \\in M$, gilt $x \\preccurlyeq y$.",
          "Da $y$ ein Minimum ist und $x \\in M$, gilt $y \\preccurlyeq x$.",
          "Aus der Antisymmetrie von $\\preccurlyeq$ folgt $x = y$. $\\square$"],
         "Man nimmt zwei Minima an und zeigt, dass sie gleich sind. Der entscheidende Schritt ist die Antisymmetrie.",
         ablenker=["Aus der Transitivität von $\\preccurlyeq$ folgt $x = y$.",
                   "Da $\\preccurlyeq$ total ist, gilt $x \\preccurlyeq y$ oder $y \\preccurlyeq x$."],
         tipps=["Eindeutigkeit zeigt man so: zwei Kandidaten annehmen, Gleichheit folgern.",
                "Welche der drei Eigenschaften einer Ordnung liefert ein Gleichheitszeichen?",
                "Die Ordnung ist nur partiell, Totalität darfst du nicht benutzen."])

# ── Seite 5: Schranken ────────────────────────────────────────────────────
k.erklaerung("Obere und untere Schranken", r"""
## Schranken dürfen außerhalb liegen

**Definition 1.52.** Sei $(M, \preccurlyeq)$ partiell geordnet und $N \subseteq M$.

- (i) $x \in M$ heißt [[obere Schranke]] von $N$ in $(M, \preccurlyeq)$, falls $y \preccurlyeq x$ für alle $y \in N$.
- (ii) $x \in M$ heißt [[untere Schranke]] von $N$, falls $x \preccurlyeq y$ für alle $y \in N$.
- (iii) $N$ heißt [[nach oben beschränkt]] bzw. nach unten beschränkt, falls es eine obere bzw. untere
  Schranke gibt, und beschränkt, falls beides gilt.

Wichtig: Eine Schranke kommt aus der großen Menge $M$, nicht unbedingt aus $N$.

:::rechnung Schranken von $N = \{\{0\}, \{1\}\}$ in $(\mathcal{P}(\{0, 1, 2\}), \subseteq)$
\{0\} \cup \{1\} = \{0, 1\} || eine obere Schranke muss $0$ und $1$ enthalten
\{0, 1\} \text{ und } \{0, 1, 2\} || genau diese beiden sind obere Schranken
\emptyset \subseteq \{0\},\ \emptyset \subseteq \{1\} || $\emptyset$ ist die einzige untere Schranke
:::

:::alt Mit Deckel und Boden
Leg die Elemente von $N$ in eine Kiste. Eine obere Schranke ist ein Deckel, der über
alle passt, ein Boden liegt unter allen. Deckel und Boden gehören nicht zum Inhalt der Kiste,
sie kommen aus dem Lager $M$. In $(\mathbb{R}, \le)$ sind für $(0, 1]$ zum Beispiel $1$, $5$
und $37$ Deckel, $0$ und $-7$ Böden.
:::
""")

k.menge("Bestimme alle oberen Schranken von $N = \\{\\{0\\}, \\{1\\}\\}$ in $(\\mathcal{P}(\\{0, 1, 2\\}), \\subseteq)$. "
        "Eingabe als Menge von Mengen, zum Beispiel `{{0}; {0; 2}}`.",
        familie_text(_N2_OBEN),
        "Eine obere Schranke $X$ muss $\\{0\\} \\subseteq X$ und $\\{1\\} \\subseteq X$ erfüllen, also $0, 1 \\in X$. "
        "In $\\mathcal{P}(\\{0, 1, 2\\})$ sind das $\\{0, 1\\}$ und $\\{0, 1, 2\\}$.",
        tipps=["Gesucht sind Mengen $X \\subseteq \\{0, 1, 2\\}$ mit $\\{0\\} \\subseteq X$ und $\\{1\\} \\subseteq X$.",
               "Also muss $X$ die $0$ und die $1$ enthalten.", "Die $2$ darf dabei sein oder nicht."],
        rechenweg=r"""
:::rechnung
\{0\} \subseteq X \land \{1\} \subseteq X \iff \{0, 1\} \subseteq X || Bedingung für eine obere Schranke
X = \{0, 1\} \text{ oder } X = \{0, 1, 2\} || alle Teilmengen von $\{0, 1, 2\}$, die $0$ und $1$ enthalten
:::
""",
        typische_fehler=[("{{0; 1}}", "Auch $\\{0, 1, 2\\}$ ist eine obere Schranke. Gefragt sind **alle**, nicht nur die kleinste."),
                         ("{{0}; {1}; {0; 1}; {0; 1; 2}}", "$\\{0\\}$ ist keine obere Schranke: $\\{1\\} \\not\\subseteq \\{0\\}$."),
                         ("{}", "Schranken müssen nicht in $N$ liegen. Sie kommen aus $\\mathcal{P}(\\{0, 1, 2\\})$.")])

# ── Seite 6: Supremum und Infimum ────────────────────────────────────────
k.erklaerung("Supremum und Infimum", r"""
## Die beste Schranke

**Definition 1.53.** Sei $(M, \preccurlyeq)$ partiell geordnet und $N \subseteq M$. Sofern es jeweils
existiert, heißt

$$\sup N := \min\{x \in M \mid x \text{ ist obere Schranke von } N\}$$

das [[Supremum]] und $\inf N := \max\{x \in M \mid x \text{ ist untere Schranke von } N\}$
das [[Infimum]] von $N$ in $(M, \preccurlyeq)$.

!! Das Supremum ist die kleinste obere Schranke. Das Infimum ist die größte untere Schranke.

:::rechnung Beispiele 1.54 und 1.55
I = (0, 1] \text{ in } (\mathbb{R}, \le) || kein Minimum, aber untere Schranken, etwa $-7$
\{x \in \mathbb{R} \mid x \le 0\} || Menge aller unteren Schranken von $I$
\inf I = 0 \notin I || ihr Maximum ist $0$
\inf \mathbb{N} = 0 = \min \mathbb{N} \text{ in } (\mathbb{Z}, \le) || $\mathbb{N}$ hat keine obere Schranke, also kein Supremum
:::

:::alt Mit einem Zaun erklärt
Alle oberen Schranken sind mögliche Zaunpfosten rechts von der Menge. Das Supremum ist der
Pfosten, der am dichtesten an der Menge steht. Bei $(0, 1]$ steht der dichteste linke Pfosten
genau bei $0$. Er berührt die Menge, gehört aber nicht dazu, denn $0 \notin (0, 1]$.
:::
---
## Beispiel 1.56: Wo kein Supremum existiert

In $(\mathbb{Q}, \le)$ betrachte $N = \{x \in \mathbb{Q} \mid x \ge 0 \text{ und } x^2 < 2\}$. Obere
Schranken gibt es, etwa $2$ oder $37$. Die Menge aller oberen Schranken ist
$\{q \in \mathbb{Q} \mid q \ge \sqrt{2}\}$. Sie hat **kein** Minimum, weil $\sqrt{2} \notin \mathbb{Q}$
(Satz 1.18) und man $\sqrt{2}$ mit rationalen Zahlen beliebig nahe kommt.

:::rechnung Rationale obere Schranken rücken immer näher
1{,}5^2 = 2{,}25 || $1{,}5$ ist obere Schranke ($2{,}25 > 2$)
1{,}42^2 = 2{,}0164 || $1{,}42$ auch, und kleiner
1{,}415^2 = 2{,}002225 || $1{,}415$ noch kleiner; so geht es endlos weiter
:::

:::achtung Das Supremum hängt von $M$ ab
In $(\mathbb{R}, \le)$ hat dieselbe Menge das Supremum $\sqrt{2}$. Schreibe daher immer dazu,
in welcher geordneten Menge du rechnest.
:::

:::alt Mit einem Lineal ohne Strich
Stell dir ein Lineal vor, auf dem nur die rationalen Zahlen markiert sind. Genau bei
$\sqrt{2}$ fehlt der Strich. Du suchst den kleinsten Strich rechts von $N$, aber jeder Strich
rechts von $\sqrt{2}$ hat noch einen weiteren Strich zwischen sich und $\sqrt{2}$.
:::
""")

k.zahl("In $(\\mathbb{R}, \\le)$ sei $N = \\{1 - \\frac{1}{n} \\mid n \\in \\mathbb{N} \\setminus \\{0\\}\\} = \\{0, \\frac{1}{2}, \\frac{2}{3}, \\frac{3}{4}, \\ldots\\}$. "
       "Bestimme $\\sup N$.", 1,
       "Jedes Element ist $< 1$, also ist $1$ obere Schranke. Jede Zahl $s < 1$ wird von einem Element überholt "
       "($1 - \\frac{1}{n} > s$ für große $n$). Also ist $1$ die kleinste obere Schranke. Ein Maximum hat $N$ nicht, denn $1 \\notin N$.",
       tipps=["Schreibe die ersten Elemente auf: $0, \\frac{1}{2}, \\frac{2}{3}, \\frac{3}{4}, \\ldots$",
              "Welcher Zahl kommen die Elemente immer näher, ohne sie zu erreichen?",
              "Das Supremum muss nicht in $N$ liegen."],
       rechenweg=r"""
:::rechnung
1 - \frac{1}{n} < 1 \text{ für alle } n || $1$ ist obere Schranke
1 - \frac{1}{100} = 0{,}99 || die Elemente kommen $1$ beliebig nahe
:::

Also ist keine Zahl $s < 1$ obere Schranke: $\sup N = 1 \notin N$.
""",
       typische_fehler=[(0, "$0 = \\min N$ ist das kleinste Element, also das Infimum. Gefragt ist das Supremum."),
                        (2, "$2$ ist zwar obere Schranke, aber nicht die kleinste: $1$ ist auch eine.")])

k.mc("Bestimme $\\inf I$ für $I = (0, 1]$ in $(\\mathbb{R}, \\le)$ (Beispiel 1.54).",
     ["$\\inf I = 0$, aber $I$ hat kein Minimum", "$\\inf I = \\min I = 0$",
      "$I$ hat kein Infimum, weil $0 \\notin I$", "$\\inf I = -7$"],
     "Die unteren Schranken sind genau alle $x \\le 0$. Ihr Maximum ist $0$. Weil $0 \\notin I$, ist $0$ kein Minimum.",
     tipps=["Welche Zahlen liegen unter allen Elementen von $(0, 1]$?", "Welche davon ist die größte?"],
     fehler={"$\\inf I = \\min I = 0$": "Ein Minimum muss in $I$ liegen. $0 \\notin (0, 1]$.",
             "$I$ hat kein Infimum, weil $0 \\notin I$": "Das Infimum darf außerhalb von $N$ liegen. Es kommt aus $M = \\mathbb{R}$.",
             "$\\inf I = -7$": "$-7$ ist eine untere Schranke, aber nicht die größte."})

# ── Seite 8: sup und inf in der Potenzmenge, Bsp. 1.57 ────────────────────
k.erklaerung("Supremum und Infimum in der Potenzmenge", r"""
## Beispiel 1.57: Vereinigung und Schnitt

In $(\mathcal{P}(M), \subseteq)$ ist für $N \neq \emptyset$ das Supremum die Vereinigung und
das Infimum der Schnitt aller Mengen in $N$. Die Vereinigung $V$ ist obere Schranke, und
jede obere Schranke enthält jede Menge aus $N$, also auch $V$.

:::rechnung Beispiel 1.57 in $\mathcal{P}(\{0, 1, 2\})$
\{0\} \cup \{1\} \cup \{0, 1\} = \{0, 1\} || $\sup A = \{0, 1\} = \max A$ für $A = \{\{0\}, \{1\}, \{0, 1\}\}$
\{0\} \cap \{1\} \cap \{0, 1\} = \emptyset || $\inf A = \emptyset \notin A$
\emptyset \cap \{0\} \cap \{1\} \cap \{1, 2\} = \emptyset || $\inf B = \emptyset = \min B$ für $B = \{\emptyset, \{0\}, \{1\}, \{1, 2\}\}$
\emptyset \cup \{0\} \cup \{1\} \cup \{1, 2\} = \{0, 1, 2\} || $\sup B = \{0, 1, 2\} \notin B$
:::

Auffällig: Ein Maximum ist immer auch das Supremum, ein Minimum immer das Infimum. Umgekehrt
gilt das nicht. Genau das sagt Satz 1.58.

:::alt Mit Playlists erklärt
Jede Menge ist eine Playlist aus den Songs $0, 1, 2$. Die kleinste Playlist, die alle
Playlists aus $N$ enthält, ist ihre Zusammenlegung (Vereinigung). Die größte Playlist, die in
allen enthalten ist, besteht aus den Songs, die überall vorkommen (Schnitt).
:::
""")

_C = [frozenset({0, 1}), frozenset({1, 2})]
k.menge("Bestimme $\\sup \\{\\{0, 1\\}, \\{1, 2\\}\\}$ in $(\\mathcal{P}(\\{0, 1, 2\\}), \\subseteq)$. Eingabe zum Beispiel `{0; 2}`.",
        mtext(sup(_P012, teilmenge, _C)),
        "Das Supremum in der Potenzmenge ist die Vereinigung: $\\{0, 1\\} \\cup \\{1, 2\\} = \\{0, 1, 2\\}$. Es liegt nicht in der Menge, "
        "darum gibt es kein Maximum.",
        tipps=["In $(\\mathcal{P}(M), \\subseteq)$ ist das Supremum die Vereinigung.",
               "Welche Elemente kommen in mindestens einer der beiden Mengen vor?",
               "Alle drei Zahlen."],
        rechenweg=r"""
:::rechnung
\{0, 1\} \cup \{1, 2\} = \{0, 1, 2\} || kleinste Menge, die beide enthält
:::
""",
        typische_fehler=[("{1}", "Das ist der Schnitt, also das Infimum. Gefragt ist das Supremum."),
                         ("{{0; 1}; {1; 2}}", "Das ist die Menge $N$ selbst. Das Supremum ist **ein** Element von $\\mathcal{P}(\\{0, 1, 2\\})$, also eine Menge von Zahlen.")])

# ── Seite 9: Satz 1.58 ────────────────────────────────────────────────────
k.erklaerung("Satz 1.58: Maximum gegen Supremum", r"""
## Wann ist das Supremum ein Maximum?

**Satz 1.58.** Sei $(M, \preccurlyeq)$ partiell geordnet und $N \subseteq M$.

- (i) $\max N$ existiert genau dann, wenn $\sup N$ existiert und $\sup N \in N$. Dann ist $\max N = \sup N$.
- (ii) $\min N$ existiert genau dann, wenn $\inf N$ existiert und $\inf N \in N$. Dann ist $\min N = \inf N$.

*Beweis von (i).* „$\Rightarrow$“: Sei $m := \max N$. Dann ist $m \in N$ und $m$ eine obere
Schranke. Für jede obere Schranke $x$ gilt $m \preccurlyeq x$, weil $m \in N$. Also ist $m$ die
kleinste obere Schranke: $\sup N = m \in N$. „$\Leftarrow$“: Liegt $\sup N$ in $N$, ist es
als obere Schranke ein Element von $N$ über allen anderen, also $\max N$. $\square$

:::rechnung Satz 1.58 an Beispielen
\sup A = \{0, 1\} \in A || also $\max A = \{0, 1\}$ (Bsp. 1.57)
\sup B = \{0, 1, 2\} \notin B || also hat $B$ kein Maximum
\inf\, (0, 1] = 0 \notin (0, 1] || also kein Minimum (Bsp. 1.54)
:::

:::alt Mit einem Klassenbesten
Das Supremum ist die Messlatte, die gerade noch über allen liegt. Wenn jemand aus der
Klasse selbst genau an der Messlatte steht, ist er der Klassenbeste (Maximum). Liegt die
Messlatte knapp über allen, ohne dass jemand sie erreicht, gibt es eine Messlatte, aber
keinen Besten.
:::
""")

k.wf("Ist $(M, \\preccurlyeq)$ partiell geordnet, $N \\subseteq M$, und existiert $\\sup N$ mit $\\sup N \\in N$, dann hat $N$ ein Maximum.",
     True, "Das ist Satz 1.58 (i), Richtung „$\\Leftarrow$“: $\\sup N$ ist obere Schranke und liegt in $N$, also ist es $\\max N$.",
     tipps=["Schau dir Satz 1.58 (i) an."])


# ── Praxis ────────────────────────────────────────────────────────────────
def _rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def _cup(f):
    return " \\cup ".join(mtex(a) for a in f)


def _cap(f):
    return " \\cap ".join(mtex(a) for a in f)


def sup_inf_potenzmenge(rng):
    g = rng.choice([[0, 1, 2], [1, 2, 3], [0, 1, 2, 3]])
    pm = potenzmenge(g)
    while True:
        pool = pm if rng.random() < 0.25 else [a for a in pm if a and a != frozenset(g)]
        n = _sortiert(rng.sample(pool, rng.randint(2, 3)))
        s, i = sup(pm, teilmenge, n), inf(pm, teilmenge, n)
        if len({s, i}) == 2:
            break
    m_tex = f"(\\mathcal{{P}}({mtex(g)}), \\subseteq)"
    kopf = f"In ${m_tex}$ sei $N = {familie_tex(n)}$. "
    art = rng.choice(["sup", "inf", "obere", "max", "min"])
    zeilen_sup = [(f"{_cup(n)} = {mtex(s)}", "Supremum = Vereinigung")]
    zeilen_inf = [(f"{_cap(n)} = {mtex(i)}", "Infimum = Schnitt")]
    if art in ("sup", "inf"):
        loes = s if art == "sup" else i
        anders = i if art == "sup" else s
        fehler = [(mtext(anders), "Du hast " + ("den Schnitt (das Infimum)" if art == "sup" else "die Vereinigung (das Supremum)")
                   + " berechnet.")]
        if art == "sup" and frozenset(g) != s:
            fehler.append((mtext(g), "Die Grundmenge ist zwar eine obere Schranke, aber nicht unbedingt die kleinste."))
        if art == "inf" and i:
            fehler.append(("{}", "$\\emptyset$ ist eine untere Schranke, aber nicht unbedingt die größte."))
        fehler = [(t, m) for t, m in fehler if t != mtext(loes)]
        return {"typ": "menge",
                "frage": kopf + f"Bestimme $\\{art} N$. Eingabe zum Beispiel `{{0; 2}}`, die leere Menge als `{{}}`.",
                "loesung": mtext(loes),
                "tipps": ["In $(\\mathcal{P}(M), \\subseteq)$ gilt: " + ("Supremum = Vereinigung." if art == "sup" else "Infimum = Schnitt."),
                          "Welche Elemente kommen in " + ("mindestens einer" if art == "sup" else "jeder") + " Menge von $N$ vor?",
                          "Das Ergebnis muss nicht in $N$ liegen."],
                "rechenweg": _rechnung(zeilen_sup if art == "sup" else zeilen_inf),
                "erklaerung": ("Die Vereinigung ist obere Schranke und liegt in jeder oberen Schranke, also ist sie die kleinste."
                               if art == "sup" else
                               "Der Schnitt ist untere Schranke und enthält jede untere Schranke, also ist er die größte."),
                "typische_fehler": fehler}
    if art == "obere":
        ob = _sortiert(obere(pm, teilmenge, n))
        fehler = []
        if len(ob) > 1:
            fehler.append((familie_text([s]), "Das ist nur die kleinste obere Schranke (das Supremum). Gefragt sind **alle**."))
        if len(ob) == 1:
            fehler.append(("{}", "Es gibt immer mindestens eine obere Schranke, zum Beispiel die Grundmenge selbst."))
        if [a for a in n if a in ob] != ob:
            fehler.append((familie_text(n), "Das ist $N$ selbst. Obere Schranken müssen über **allen** Elementen von $N$ liegen."))
        zeilen = zeilen_sup + [(f"{mtex(s)} \\subseteq X \\subseteq {mtex(g)}", "obere Schranken: alle $X$, die die Vereinigung enthalten")]
        return {"typ": "menge",
                "frage": kopf + "Bestimme alle oberen Schranken von $N$. Eingabe als Menge von Mengen, zum Beispiel `{{1}; {1; 2}}`.",
                "loesung": familie_text(ob),
                "tipps": ["$X$ ist obere Schranke, wenn jede Menge aus $N$ Teilmenge von $X$ ist.",
                          f"Also muss $X$ die Vereinigung ${mtex(s)}$ enthalten.",
                          f"Zähle alle Teilmengen von ${mtex(g)}$ auf, die ${mtex(s)}$ enthalten."],
                "rechenweg": _rechnung(zeilen),
                "erklaerung": "Obere Schranken sind genau die Mengen, die die Vereinigung aller Mengen aus $N$ enthalten.",
                "typische_fehler": fehler}
    if art == "max":
        mx = maximum(teilmenge, n)
        richtig = f"$\\max N = {mtex(mx)}$" if mx is not None else "$N$ hat kein Maximum"
        opt = [richtig]
        fehler = {}
        if mx is None:
            o = f"$\\max N = {mtex(s)}$"
            opt.append(o)
            fehler[o] = f"${mtex(s)}$ ist das Supremum, liegt aber nicht in $N$. Ein Maximum muss Element von $N$ sein (Satz 1.58)."
            groesste = max(n, key=len)
            o2 = f"$\\max N = {mtex(groesste)}$"
            if o2 not in opt:
                opt.append(o2)
                fehler[o2] = f"${mtex(groesste)}$ hat die meisten Elemente, aber nicht jede Menge aus $N$ ist Teilmenge davon."
        else:
            opt.append("$N$ hat kein Maximum")
            fehler["$N$ hat kein Maximum"] = f"${mtex(mx)} \\in N$ enthält jede Menge aus $N$, ist also das Maximum."
        if f"$\\max N = {mtex(frozenset(g))}$" not in opt:
            opt.append(f"$\\max N = {mtex(frozenset(g))}$")
        zeilen = zeilen_sup + [(f"{mtex(s)} \\in N" if s in n else f"{mtex(s)} \\notin N",
                                "Satz 1.58: also " + ("ist das Supremum das Maximum" if s in n else "kein Maximum"))]
        return {"typ": "mc", "frage": kopf + "Was gilt für das Maximum von $N$?", "optionen": opt, "fehler": fehler,
                "tipps": ["Berechne zuerst $\\sup N$ (die Vereinigung).", "Satz 1.58: $\\max N$ existiert genau dann, wenn $\\sup N \\in N$."],
                "rechenweg": _rechnung(zeilen),
                "erklaerung": "Nach Satz 1.58 ist das Maximum genau das Supremum, falls es in $N$ liegt."}
    mn = minimum(teilmenge, n)
    richtig = f"$\\min N = {mtex(mn)}$" if mn is not None else "$N$ hat kein Minimum"
    opt = [richtig]
    fehler = {}
    if mn is None:
        o = f"$\\min N = {mtex(i)}$"
        opt.append(o)
        fehler[o] = f"${mtex(i)}$ ist das Infimum, liegt aber nicht in $N$. Ein Minimum muss Element von $N$ sein (Satz 1.58)."
    else:
        opt.append("$N$ hat kein Minimum")
        fehler["$N$ hat kein Minimum"] = f"${mtex(mn)} \\in N$ ist Teilmenge jeder Menge aus $N$, also das Minimum."
    if "$\\min N = \\emptyset$" not in opt:
        opt.append("$\\min N = \\emptyset$")
        fehler["$\\min N = \\emptyset$"] = "$\\emptyset$ liegt nicht in $N$. Ein Minimum muss Element von $N$ sein."
    zeilen = zeilen_inf + [(f"{mtex(i)} \\in N" if i in n else f"{mtex(i)} \\notin N",
                            "Satz 1.58: also " + ("ist das Infimum das Minimum" if i in n else "kein Minimum"))]
    return {"typ": "mc", "frage": kopf + "Was gilt für das Minimum von $N$?", "optionen": opt, "fehler": fehler,
            "tipps": ["Berechne zuerst $\\inf N$ (den Schnitt).", "Satz 1.58: $\\min N$ existiert genau dann, wenn $\\inf N \\in N$."],
            "rechenweg": _rechnung(zeilen),
            "erklaerung": "Nach Satz 1.58 ist das Minimum genau das Infimum, falls es in $N$ liegt."}


def teiler_ordnung(rng):
    n = rng.choice([12, 18, 20, 24, 30, 36, 60])
    t = [d for d in range(1, n + 1) if n % d == 0]
    while True:
        teil = sorted(rng.sample([d for d in t if d not in (1, n)], 2))
        s, i = sup(t, teilt, teil), inf(t, teilt, teil)
        if s not in teil and i not in teil:
            break
    t_tex = "\\{" + ", ".join(map(str, t)) + "\\}"
    art = rng.choice(["sup", "inf"])
    a, b = teil
    kopf = (f"Sei $T = {t_tex}$ die Menge der Teiler von ${n}$, geordnet durch die Teilbarkeit $\\mid$. "
            f"Sei $N = \\{{{a}, {b}\\}}$. ")
    ob, un = sorted(obere(t, teilt, teil)), sorted(untere(t, teilt, teil))
    if art == "sup":
        assert s == math.lcm(a, b)
        fehler = [(b, f"${b}$ ist bezüglich $\\le$ das größte Element, aber ${a} \\nmid {b}$. Hier zählt die Teilbarkeit."),
                  (a * b, f"${a} \\cdot {b}$ ist ein gemeinsames Vielfaches, aber nicht das kleinste" +
                   (f" (und kein Teiler von ${n}$)." if n % (a * b) else ".")),
                  (n, f"${n}$ ist obere Schranke, aber nicht unbedingt die kleinste.")]
        zeilen = [(f"{a} \\mid x \\text{{ und }} {b} \\mid x \\text{{ für }} x = {', '.join(map(str, ob))}", "das sind alle oberen Schranken in $T$"),
                  (f"\\sup N = {s}", f"die kleinste davon: ${s}$ teilt jede obere Schranke (kgV von ${a}$ und ${b}$)")]
        loes = s
        frage = kopf + "Bestimme $\\sup N$ in $(T, \\mid)$."
        tipps = ["Obere Schranken sind Elemente $x \\in T$ mit $a \\mid x$ und $b \\mid x$: gemeinsame Vielfache.",
                 f"Liste alle Teiler von ${n}$ auf, die durch ${a}$ und ${b}$ teilbar sind.",
                 "Die kleinste obere Schranke ist das kgV."]
        erkl = "In $(T, \\mid)$ ist das Supremum zweier Elemente ihr kleinstes gemeinsames Vielfaches."
    else:
        assert i == math.gcd(a, b)
        fehler = [(a, f"${a}$ ist bezüglich $\\le$ das kleinste Element, aber ${a} \\nmid {b}$."),
                  (1, "$1$ ist untere Schranke, aber nicht unbedingt die größte.")]
        zeilen = [(f"x \\mid {a} \\text{{ und }} x \\mid {b} \\text{{ für }} x = {', '.join(map(str, un))}", "das sind alle unteren Schranken in $T$"),
                  (f"\\inf N = {i}", f"die größte davon: jede untere Schranke teilt ${i}$ (ggT von ${a}$ und ${b}$)")]
        loes = i
        frage = kopf + "Bestimme $\\inf N$ in $(T, \\mid)$."
        tipps = ["Untere Schranken sind Elemente $x \\in T$ mit $x \\mid a$ und $x \\mid b$: gemeinsame Teiler.",
                 f"Liste die gemeinsamen Teiler von ${a}$ und ${b}$ auf.",
                 "Die größte untere Schranke ist der ggT."]
        erkl = "In $(T, \\mid)$ ist das Infimum zweier Elemente ihr größter gemeinsamer Teiler."
    fehler = [(w, m) for w, m in fehler if w != loes]
    seen, tf = set(), []
    for w, m in fehler:
        if w not in seen:
            seen.add(w)
            tf.append((w, m))
    return {"frage": frage, "loesung": loes, "tipps": tipps, "rechenweg": _rechnung(zeilen),
            "erklaerung": erkl, "typische_fehler": tf}


k.praxis()

k.generator(sup_inf_potenzmenge, typ="menge", titel="sup, inf, max, min in der Potenzmenge")
k.generator(teiler_ordnung, typ="zahl", titel="Supremum und Infimum bei Teilbarkeit")

k.rechenweg_aufgabe(r"""
## Übungsblatt-Stil: Teiler von 12

Sei $T = \{1, 2, 3, 4, 6, 12\}$ mit der Teilbarkeit $\mid$ und $N = \{4, 6\}$.
Bestimmen Sie die oberen Schranken, $\sup N$, $\inf N$ und entscheiden Sie, ob $\max N$ existiert.
""",
    [{"typ": "menge", "frage": "Gib alle oberen Schranken von $N$ in $(T, \\mid)$ an.", "loesung": "{12}",
      "tipps": ["Gesucht: $x \\in T$ mit $4 \\mid x$ und $6 \\mid x$.", "Welche Teiler von $12$ sind durch $4$ und $6$ teilbar?"],
      "rechenweg": "Nur $12$ ist durch $4$ und durch $6$ teilbar.",
      "typische_fehler": [("{6; 12}", "$4 \\nmid 6$, also ist $6$ keine obere Schranke."),
                          ("{24}", "$24 \\notin T$. Schranken kommen aus $T$.")]},
     {"typ": "zahl", "frage": "Bestimme $\\sup N$.", "loesung": 12,
      "tipps": ["Es gibt nur eine obere Schranke.", "Das Minimum einer einelementigen Menge ist ihr Element."],
      "rechenweg": "$\\sup N = \\min \\{12\\} = 12$.",
      "typische_fehler": [(6, "$6$ ist bezüglich $\\le$ das größte Element von $N$, aber $4 \\nmid 6$.")]},
     {"typ": "zahl", "frage": "Bestimme $\\inf N$.", "loesung": 2,
      "tipps": ["Untere Schranken: $x \\mid 4$ und $x \\mid 6$.", "Das sind $1$ und $2$."],
      "rechenweg": "Untere Schranken sind $1$ und $2$; wegen $1 \\mid 2$ ist $\\inf N = 2$.",
      "typische_fehler": [(1, "$1$ ist untere Schranke, aber $1 \\mid 2$: $2$ ist größer bezüglich $\\mid$."),
                          (4, "$4 \\nmid 6$, also ist $4$ keine untere Schranke.")]},
     {"typ": "mc", "frage": "Existiert $\\max N$?",
      "optionen": ["Nein, denn $\\sup N = 12 \\notin N$", "Ja, $\\max N = 6$", "Ja, $\\max N = 12$"],
      "fehler": {"Ja, $\\max N = 6$": "$4 \\nmid 6$: $6$ liegt nicht über $4$.",
                 "Ja, $\\max N = 12$": "Ein Maximum muss in $N$ liegen. $12 \\notin N$."},
      "tipps": ["Satz 1.58 (i): Wann gibt es ein Maximum?", "Liegt $\\sup N$ in $N$?"], "erklaerung": "Nach Satz 1.58 gäbe es nur dann ein Maximum, wenn $\\sup N \\in N$."}],
    "In $(T, \\mid)$ ist $\\sup\\{4, 6\\} = 12$ (kgV) und $\\inf\\{4, 6\\} = 2$ (ggT). Wegen $12 \\notin N$ gibt es kein Maximum.",
    uebungsblatt=True,
    tipps=["Arbeite mit der Teilbarkeit, nicht mit $\\le$.", "Satz 1.58 verbindet Maximum und Supremum."],
    rechenweg=r"""
:::rechnung
12 = 3 \cdot 4 = 2 \cdot 6 || $12$ ist obere Schranke, die einzige in $T$
4 = 2 \cdot 2,\ 6 = 3 \cdot 2 || $2$ ist untere Schranke, ebenso $1$
\sup N = 12 \notin N || also kein Maximum (Satz 1.58)
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Satz 1.58 (ii) beweisen

Das Skript beweist nur Teil (i) und schreibt „die zweite ist analog“. Beweisen Sie Teil (ii):

Sei $(M, \preccurlyeq)$ partiell geordnet und $N \subseteq M$. Dann existiert $\min N$ genau dann, wenn
$\inf N$ existiert und $\inf N \in N$ gilt. In diesem Fall ist $\min N = \inf N$.
""",
    r"""
**„$\Rightarrow$“:** Sei $m := \min N$. Dann gilt $m \in N$ und $m \preccurlyeq y$ für alle $y \in N$, also ist
$m$ eine untere Schranke von $N$. Sei $x \in M$ eine beliebige untere Schranke von $N$. Da $m \in N$, gilt
$x \preccurlyeq m$. Also ist $m$ größer oder gleich jeder unteren Schranke und selbst eine: $m$ ist das
Maximum der Menge der unteren Schranken. Damit existiert $\inf N = m$, und $\inf N = m \in N$.

**„$\Leftarrow$“:** Existiere $\inf N$ mit $\inf N \in N$. Als untere Schranke erfüllt $\inf N \preccurlyeq y$
für alle $y \in N$. Zusammen mit $\inf N \in N$ ist $\inf N$ nach Definition 1.46 das Minimum von $N$, also
$\min N = \inf N$. $\square$
""",
    ["Beide Richtungen getrennt bewiesen",
     "In „$\\Rightarrow$“ gezeigt, dass $m$ untere Schranke ist",
     "In „$\\Rightarrow$“ eine **beliebige** untere Schranke $x$ genommen und $x \\preccurlyeq m$ begründet (mit $m \\in N$)",
     "In „$\\Leftarrow$“ Definition 1.46 des Minimums benutzt",
     "Die Richtung der Relation $\\preccurlyeq$ überall richtig herum geschrieben"],
    "Spiegle den Beweis von (i): Maximum wird Minimum, obere wird untere Schranke, $y \\preccurlyeq x$ wird $x \\preccurlyeq y$.",
    uebungsblatt=True,
    tipps=["Schreibe den Beweis von (i) ab und drehe jedes $\\preccurlyeq$ und jedes Wort „obere/größte“ um."])

k.zusammenfassung(r"""
## Ordnungen (Skript Abschn. 1.6, Def. 1.42 bis Satz 1.58)

- **Ordnungsrelation** $\preccurlyeq$: reflexiv, antisymmetrisch, transitiv; $(M, \preccurlyeq)$ partiell geordnet.
- **Totalordnung**: zusätzlich $\forall x, y : x \preccurlyeq y \lor y \preccurlyeq x$. Beispiel $\le$ auf $\mathbb{R}$; $\subseteq$ ist nur partiell.
- Teilmengen erben die Ordnung (Beob. 1.45).

| Begriff | Definition | liegt in $N$? |
|---|---|---|
| $\max N$ | $y \preccurlyeq x$ für alle $y \in N$, $x \in N$ | ja |
| obere Schranke | $y \preccurlyeq x$ für alle $y \in N$, $x \in M$ | nicht nötig |
| $\sup N$ | kleinste obere Schranke | nicht nötig |
| $\inf N$ | größte untere Schranke | nicht nötig |

- Satz 1.47: höchstens ein Maximum/Minimum (Beweis mit Antisymmetrie).
- Satz 1.58: $\max N$ existiert $\iff$ $\sup N$ existiert und $\sup N \in N$; dann $\max N = \sup N$. Analog min/inf.
- In $(\mathcal{P}(M), \subseteq)$: $\sup$ = Vereinigung, $\inf$ = Schnitt. In (Teiler, $\mid$): $\sup$ = kgV, $\inf$ = ggT.
- $\inf\, (0, 1] = 0$ ohne Minimum; $\{x \in \mathbb{Q} \mid x \ge 0, x^2 < 2\}$ hat in $\mathbb{Q}$ kein Supremum.

!! Das Supremum ist die kleinste obere Schranke. Das Infimum ist die größte untere Schranke.
""")
