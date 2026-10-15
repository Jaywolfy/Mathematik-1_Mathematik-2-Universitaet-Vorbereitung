# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 12: Potenz, Fakultät und Binomialkoeffizient
(Skript Disser WS 26/27, Abschn. 2.6 bis 2.8, Def. 2.46 bis Korollar 2.64)."""
from itertools import combinations, permutations, product
from math import comb, factorial

from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(
    slug="kombinatorik",
    titel="Potenz, Fakultät und Binomialkoeffizient",
    beschreibung="Abbildungen zählen (aᵇ), |P(M)| = 2^|M|, Permutationen und n!, k-elementige Teilmengen, Pascalsche Regel, binomischer Lehrsatz",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 2.6 bis 2.8",
    icon="🎲")


# ── Python rechnet alles nach ──────────────────────────────────────────────
def mtex(s):
    return "\\emptyset" if not s else "\\{" + ", ".join(str(x) for x in sorted(s)) + "\\}"


def abbildungen(B, A):
    """abb(B, A) als Liste von dicts (Def. 2.46)."""
    B, A = list(B), list(A)
    return [dict(zip(B, w)) for w in product(A, repeat=len(B))]


# Satz 2.47, 2.49: |abb(B, A)| = |A|^|B| = |A^|B||
assert len(abbildungen(range(4), range(10))) == 10 ** 4
assert all(len(abbildungen(range(b), "xyz"[:a])) == a ** b for a in range(4) for b in range(5))
assert len(abbildungen([], [1, 2, 3])) == 1 and len(abbildungen([], [])) == 1      # 0^0 = 1 (die leere Abbildung)
assert 0 ** 0 == 1 and len(abbildungen([1, 2], "xyz")) == 9 and len(abbildungen([1, 2, 3], [0, 1])) == 8
# Satz 2.47: Φ(f) = (f(g(0)), ..., f(g(|B|-1))) ist bijektiv
_f = {0: 3, 1: 1, 2: 4, 3: 1}
assert tuple(_f[i] for i in range(4)) == (3, 1, 4, 1)
# Satz 2.50, 2.51: Potenzgesetze
assert all(a ** (m + n) == a ** m * a ** n and (a ** m) ** n == a ** (m * n) and (a * b) ** n == a ** n * b ** n
           for a in range(5) for b in range(5) for m in range(5) for n in range(5))
assert 2 ** (3 + 2) == 2 ** 3 * 2 ** 2 == 32 and (2 ** 3) ** 2 == 64 == 2 ** 6 and (2 * 3) ** 2 == 36 == 2 ** 2 * 3 ** 2
# Satz 2.52: a^k mod n = (a mod n)^k mod n
assert all(a ** kk % n == (a % n) ** kk % n for a in range(30) for kk in range(8) for n in range(1, 12))
assert 3 ** 5 % 7 == 5 and [3 ** e % 7 for e in range(1, 6)] == [3, 2, 6, 4, 5]
# Satz 2.53: |P(M)| = 2^|M| mit Indikatorfunktion
_M = ["a", "b", "c"]
_teil = [set(c) for r in range(4) for c in combinations(_M, r)]
assert len(_teil) == 8 == 2 ** 3
_chi = {frozenset(A): tuple(1 if x in A else 0 for x in _M) for A in _teil}
assert len(set(_chi.values())) == 8
# Def. 2.54/2.55, Satz 2.56, 2.57
assert len(list(permutations(range(3)))) == 6 == factorial(3) and factorial(0) == 1 and factorial(4) == 4 * factorial(3) == 24
assert all(len(list(permutations(range(n)))) == factorial(n) for n in range(7))
assert all(factorial(n) == __import__("math").prod(range(1, n + 1)) for n in range(1, 12))
# Def. 2.58/2.59, Satz 2.60, 2.61
_tm = [set(c) for c in combinations(range(4), 2)]
assert len(_tm) == comb(4, 2) == 6 and comb(3, 5) == 0 and all(comb(n, 0) == 1 for n in range(10))
assert all(comb(n, kk) == factorial(n) // (factorial(kk) * factorial(n - kk)) for n in range(12) for kk in range(n + 1))
assert comb(5, 2) == 10 and factorial(5) // (factorial(2) * factorial(3)) == 10 == 120 // 12
# Satz 2.62: Pascal; Satz 2.63, Korollar 2.64
assert all(comb(n + 1, kk) == comb(n, kk) + comb(n, kk - 1) for n in range(12) for kk in range(1, n + 2))
assert comb(5, 2) == comb(4, 2) + comb(4, 1) == 6 + 4
assert all((a + b) ** n == sum(comb(n, kk) * a ** kk * b ** (n - kk) for kk in range(n + 1)) for a in range(5) for b in range(5) for n in range(8))
assert all(sum(comb(n, kk) for kk in range(n + 1)) == 2 ** n for n in range(14)) and 1 + 4 + 6 + 4 + 1 == 16
# Quiz: Menge mit 5 Elementen
assert (2 ** 5, comb(5, 2), comb(5, 0) + comb(5, 1) + comb(5, 2)) == (32, 10, 16)


_TEILMENGEN_ZEILEN = "\n".join(f"{mtex(A)} \\leftrightarrow {chi} || " + g
                               for A, chi, g in [(set(), (0, 0, 0), "keines der drei Elemente ist drin"),
                                                 ({"a"}, (1, 0, 0), "nur $a$ ist drin"),
                                                 ({"a", "c"}, (1, 0, 1), "$a$ und $c$ sind drin"),
                                                 ({"a", "b", "c"}, (1, 1, 1), "alle drei sind drin")])
assert all(_chi[frozenset(A)] == chi for A, chi in [(set(), (0, 0, 0)), ({"a"}, (1, 0, 0)), ({"a", "c"}, (1, 0, 1)), ({"a", "b", "c"}, (1, 1, 1))])
_PERM3 = ", ".join(f"({', '.join(map(str, p))})" for p in permutations(range(3)))
_TM24 = ", ".join(mtex(c) for c in combinations(range(4), 2))

k.lernziele([
    "Ich verstehe, dass $a^n$ die Anzahl der Abbildungen $n \\to a$ ist, und kenne $0^0 = 1$ sowie die Potenzgesetze und die Potenzregel für Reste (Def. 2.46 bis Satz 2.52)",
    "Ich begründe $|\\mathcal{P}(M)| = 2^{|M|}$ mit Indikatorfunktionen (Satz 2.53)",
    "Ich zähle Permutationen mit $n!$ und beweise $n! = \\prod_{i=1}^{n} i$ per Induktion (Def. 2.54, 2.55, Satz 2.56, 2.57)",
    "Ich berechne $\\binom{n}{k}$ als Anzahl der $k$-elementigen Teilmengen, mit der Fakultätsformel und mit der Pascalschen Regel und kenne den binomischen Lehrsatz (Def. 2.58, 2.59, Satz 2.60 bis 2.63, Kor. 2.64)",
])

k.warum(r"""
Wie viele Passwörter der Länge 8 gibt es? $62^8$. Wie viele Teilmengen hat ein Array mit $n$ Elementen? $2^n$, das ist der
Aufwand, wenn ein Algorithmus **alle** Teilmengen probiert. Wie viele Reihenfolgen gibt es? $n!$: Brute-Force-Sortieren
oder das Problem des Handlungsreisenden mit $n!$ Touren. Wie viele Wege gibt es, aus $n$ Elementen $k$ auszuwählen? $\binom{n}{k}$.
Wer Laufzeiten wie $2^n$ und $n!$ versteht und weiß, warum sie explodieren, kann einschätzen, wann ein Algorithmus nutzlos ist.
Der binomische Lehrsatz taucht später bei Wahrscheinlichkeit und in der Analysis wieder auf.
""")

# ── Seite 1: Abbildungen und Tupel ───────────────────────────────────────
k.erklaerung("Zeichenketten sind Abbildungen (Def. 2.46, Satz 2.47)", r"""
## Abbildungen von $B$ nach $A$

:::analogie 🔢 Das Zahlenschloss
Ein Schloss hat vier Stellen, jede zeigt eine Ziffer von $0$ bis $9$. Eine Einstellung ordnet **jeder Stelle genau eine Ziffer** zu. Das ist eine Abbildung von den Stellen in die Ziffern.
:::

**Definition 2.46.** $\text{abb}(B, A) := \{f \subseteq B \times A \mid f\colon B \to A\}$ ist die Menge aller Abbildungen von $B$ nach $A$.

**Satz 2.47.** Für jede Menge $A$ und jede endliche Menge $B$ gibt es eine Bijektion $\text{abb}(B, A) \to A^{|B|}$. Ist $A$ endlich, so gilt $|\text{abb}(B, A)| = |A^{|B|}|$.

:::rechnung Das Zahlenschloss als Abbildung und als Tupel
f\colon 0 \mapsto 3,\ 1 \mapsto 1,\ 2 \mapsto 4,\ 3 \mapsto 1 || eine Abbildung $\{0, 1, 2, 3\} \to \{0, \ldots, 9\}$
(3, 1, 4, 1) \in \{0, \ldots, 9\}^4 || dasselbe als Tupel: $\Phi(f) = (f(0), f(1), f(2), f(3))$
10 \cdot 10 \cdot 10 \cdot 10 = 10000 || je Stelle $10$ Möglichkeiten: so viele Einstellungen hat das Schloss
:::

:::alt Als Fragebogen
Ein Fragebogen hat vier Fragen mit je zehn Antwortmöglichkeiten. Ein ausgefüllter Bogen weist jeder Frage eine Antwort zu: Er ist eine Abbildung von den Fragen in die Antworten. Die Liste der Antworten in Reihenfolge der Fragen ist das Tupel.
:::
""")

k.zahl(r"Wie viele Abbildungen $f\colon \{0, 1, 2\} \to \{a, b\}$ gibt es?", 8,
       r"Jedes der $3$ Elemente der Definitionsmenge bekommt unabhängig einen von $2$ Werten: $2 \cdot 2 \cdot 2 = 2^3 = 8$ (Satz 2.49: $|A|^{|B|}$ mit $A = \{a, b\}$, $B = \{0, 1, 2\}$).",
       tipps=["Wie viele Möglichkeiten gibt es für $f(0)$?", r"Jedes der drei Elemente $0, 1, 2$ hat zwei Möglichkeiten.", r"$|A|^{|B|}$ mit $|A| = 2$ und $|B| = 3$"],
       rechenweg=r"""
:::rechnung
2 \cdot 2 \cdot 2 = 8 || $f(0), f(1), f(2)$ je zwei Möglichkeiten
2^3 = 8 || $|A|^{|B|}$
:::
""",
       typische_fehler=[(9, r"Du hast $3^2$ gerechnet: Basis und Exponent vertauscht. Die Basis ist die Größe der **Zielmenge** ($2$), der Exponent die der Definitionsmenge ($3$)."),
                        (6, r"Du hast $2 \cdot 3$ gerechnet. Die Wahlen sind unabhängig, die Anzahl multipliziert sich $3$-mal: $2 \cdot 2 \cdot 2$.")])

# ── Seite 2: Potenz ──────────────────────────────────────────────────────
k.erklaerung("Die Potenz (Def. 2.48, Satz 2.49, 2.50)", r"""
## $a^n$ zählt Abbildungen

**Definition 2.48.** $\text{pot}\colon \mathbb{N}^2 \to \mathbb{N},\ (a, n) \mapsto |\text{abb}(n, a)|$ und $a^n := \text{pot}(a, n)$ ([[Potenz]]).
Insbesondere $a^0 = 1$ für alle $a$, auch $0^0 = 1$: Es gibt genau eine Abbildung von $0 = \emptyset$ nach $a$, die leere Abbildung.

**Satz 2.49.** Für endliche $A, B$ gilt $|\text{abb}(B, A)| = |A|^{|B|} = |A^{|B|}|$.
**Satz 2.50 (Übung).** $a^n = \prod_{i=1}^{n} a$ für $n \ge 1$. Die Potenz ist wiederholtes Malnehmen, so wie das Produkt wiederholtes Addieren ist.

:::rechnung Anzahlen
|\text{abb}(\{1, 2\}, \{x, y, z\})| = 3^2 = 9 || zwei Stellen, je drei mögliche Werte
|\text{abb}(\{1, 2, 3\}, \{0, 1\})| = 2^3 = 8 || drei Stellen, je zwei Werte: die Bitstrings der Länge $3$
\text{Es gilt } 0^0 = 1 \text{ und } a^0 = 1 || genau eine Abbildung $\emptyset \to a$
:::

:::achtung Basis und Exponent
Bei $|\text{abb}(B, A)| = |A|^{|B|}$ steht die Größe der **Zielmenge** unten. Aus $\{0, 1, 2\}$ nach $\{a, b\}$ gibt es $2^3 = 8$, nicht $3^2 = 9$.
:::

:::alt Als Wahlbaum
Wähle für jede Stelle unabhängig einen Wert. Der erste Schritt hat $|A|$ Zweige, an jedem Zweig wieder $|A|$, und so weiter. Nach $|B|$ Stufen hat der Baum $|A| \cdot \ldots \cdot |A|$ Blätter.
:::
""")

k.mc(r"Was ist $0^0$ nach Definition 2.48?",
     [r"$1$, denn es gibt genau eine Abbildung $\emptyset \to 0$, nämlich die leere Abbildung",
      r"$0$, denn $0$ mal irgendetwas ist $0$",
      r"undefiniert, denn man darf nicht durch $0$ teilen",
      r"$\infty$"],
     r"$0^0 = |\text{abb}(\emptyset, \emptyset)| = 1$: Die leere Abbildung ist die einzige. Allgemein $a^0 = 1$, weil es genau eine Abbildung von der leeren Menge in jede Menge gibt.",
     tipps=[r"Zähle die Abbildungen von $\emptyset$ nach $\emptyset$.", "Die leere Menge hat keine Elemente, denen etwas zugeordnet werden müsste.", r"Es gibt genau eine: die leere Abbildung."],
     fehler={r"$0$, denn $0$ mal irgendetwas ist $0$": r"Die Potenz ist hier keine Multiplikation mit Null, sondern eine **Anzahl von Abbildungen**, und es gibt eine.",
             r"undefiniert, denn man darf nicht durch $0$ teilen": r"Hier wird nicht geteilt. Das Skript definiert $a^n$ für alle $a, n \in \mathbb{N}$, auch $0^0$.",
             r"$\infty$": r"Es gibt genau eine Abbildung, nicht unendlich viele."})

# ── Seite 3: Potenzgesetze ───────────────────────────────────────────────
k.erklaerung("Potenzgesetze und Reste (Satz 2.51, 2.52)", r"""
## Drei Gesetze aus Bijektionen

**Satz 2.51 ([[Potenzgesetze|Potenzgesetz]]).** Für alle $a, b, m, n \in \mathbb{N}$:
$$a^{m+n} = a^m \cdot a^n, \qquad (a^m)^n = a^{m \cdot n}, \qquad (a \cdot b)^n = a^n \cdot b^n.$$

Beweisidee: Ein $(m+n)$-Tupel zerfällt in ein $m$-Tupel und ein $n$-Tupel (erstes Gesetz). Eine Abbildung, die jedem $i \in n$ eine Abbildung $m \to a$ zuordnet, ist dasselbe wie eine Abbildung $m \times n \to a$ (zweites). Ein Tupel von Paaren ist ein Paar von Tupeln (drittes).

**Satz 2.52 (Potenzregel für Reste).** $a^k \bmod n = (a \bmod n)^k \bmod n$ für $n \neq 0$ (Übung).

:::rechnung Die Gesetze an Zahlen
2^{3+2} = 2^5 = 32 || linke Seite
2^3 \cdot 2^2 = 8 \cdot 4 = 32 || $a^{m+n} = a^m \cdot a^n$
(2^3)^2 = 8^2 = 64 = 2^{3 \cdot 2} || $(a^m)^n = a^{m \cdot n}$
(2 \cdot 3)^2 = 36 = 2^2 \cdot 3^2 || $(a \cdot b)^n = a^n \cdot b^n$: $4 \cdot 9$
:::

:::alt Mit Würfelstapeln
$2^5$ Würfelfolgen aus fünf Würfen lassen sich als erste drei und letzte zwei Würfe lesen: $2^3 \cdot 2^2$ Möglichkeiten. Die Zerlegung ändert die Anzahl nicht.
:::
""")

k.zahl(r"Berechne $3^5 \bmod 7$ mit Satz 2.52, ohne $3^5$ voll auszurechnen: Rechne Schritt für Schritt mit Resten.", 5,
       r"$3^1 = 3$, $3^2 = 9 \equiv 2$, $3^3 \equiv 2 \cdot 3 = 6$, $3^4 \equiv 6 \cdot 3 = 18 \equiv 4$, $3^5 \equiv 4 \cdot 3 = 12 \equiv 5 \pmod 7$. Kontrolle: $3^5 = 243 = 34 \cdot 7 + 5$.",
       tipps=[r"Nimm nach jeder Multiplikation mit $3$ sofort den Rest modulo $7$.", r"$3^2 = 9$ hat den Rest $2$.", r"Die Reste der Reihe nach: $3, 2, 6, 4, \ldots$"],
       rechenweg=r"""
:::rechnung
3 \cdot 3 = 9 = 1 \cdot 7 + 2 || $3^2$ hat Rest $2$
2 \cdot 3 = 6 = 0 \cdot 7 + 6 || $3^3$ hat Rest $6$
6 \cdot 3 = 18 = 2 \cdot 7 + 4 || $3^4$ hat Rest $4$
4 \cdot 3 = 12 = 1 \cdot 7 + 5 || $3^5$ hat Rest $5$
3^5 = 243 = 34 \cdot 7 + 5 || Kontrolle
:::
""",
       typische_fehler=[(15, r"Du hast $3 \cdot 5$ gerechnet. $3^5$ bedeutet fünfmal mit $3$ multiplizieren."),
                        (243, r"Das ist $3^5$ selbst. Es fehlt noch der Rest bei Division durch $7$."),
                        (3, r"Du hast $3^5 \bmod 7$ mit $3 \bmod 7$ verwechselt. Die Potenz muss mitgerechnet werden.")])

# ── Seite 4: Potenzmenge ─────────────────────────────────────────────────
k.erklaerung("Teilmengen zählen: |P(M)| = 2^|M| (Satz 2.53)", r"""
## Jedes Element ist drin oder nicht

Für jedes Element entscheidest du: **in** der Teilmenge oder **nicht**. Das sind zwei Möglichkeiten je Element.

**Satz 2.53.** Für endliche $M$ gilt $|\mathcal{P}(M)| = 2^{|M|}$.

*Beweis.* Jeder Teilmenge $A \subseteq M$ ordnest du ihre Indikatorfunktion $\chi_A\colon M \to 2 = \{0, 1\}$ mit $\chi_A(x) = 1$ für $x \in A$ und $0$ sonst zu.
Umgekehrt liefert jedes $\chi\colon M \to 2$ die Teilmenge $\{x \in M \mid \chi(x) = 1\}$. So ist $A \mapsto \chi_A$ eine Bijektion $\mathcal{P}(M) \to \text{abb}(M, 2)$, und mit Satz 2.49 folgt die Behauptung.

:::rechnung $M = \{a, b, c\}$ (Bits für $a, b, c$)
§ZEILEN§
2^3 = 8 || insgesamt $8$ Tupel aus $\{0, 1\}^3$, also $8$ Teilmengen
:::

:::alt Als Lichtschalter
Ein Raum hat $n$ Lichtschalter. Jede Stellung der Schalter ist eine Teilmenge der Lampen, die brennen. Mit $n$ Schaltern gibt es $2 \cdot \ldots \cdot 2 = 2^n$ Stellungen.
:::
""".replace("§ZEILEN§", _TEILMENGEN_ZEILEN))

k.zahl(r"Eine Menge $M$ hat $6$ Elemente. Wie viele Teilmengen hat $M$?", 64,
       r"Satz 2.53: $|\mathcal{P}(M)| = 2^{|M|} = 2^6 = 64$. Jedes Element ist in der Teilmenge oder nicht.",
       tipps=["Jedes Element hat zwei Möglichkeiten: drin oder nicht drin.", r"$2 \cdot 2 \cdot 2 \cdot 2 \cdot 2 \cdot 2$", r"$2^6$"],
       rechenweg=r"""
:::rechnung
2^6 = 2 \cdot 2 \cdot 2 \cdot 2 \cdot 2 \cdot 2 || sechs Entscheidungen mit je zwei Möglichkeiten
2^6 = 64 || ausgerechnet
:::
""",
       typische_fehler=[(12, r"Du hast $6 \cdot 2$ gerechnet. Die Entscheidungen sind unabhängig, die Anzahl multipliziert sich sechsmal."),
                        (36, r"Das ist $6^2$ (Basis und Exponent vertauscht). Die Basis ist $2$ (drin oder nicht drin), der Exponent $|M| = 6$.")])

k.wf(r"Die leere Menge $\emptyset$ hat genau eine Teilmenge.", True,
     r"Wahr: $|\mathcal{P}(\emptyset)| = 2^0 = 1$. Die einzige Teilmenge von $\emptyset$ ist $\emptyset$ selbst. Das passt zur einzigen leeren Abbildung $\emptyset \to \{0, 1\}$.",
     tipps=[r"Setze $|M| = 0$ in $2^{|M|}$ ein."])

# ── Seite 5: Permutationen ───────────────────────────────────────────────
k.erklaerung("Permutationen und Fakultät (Def. 2.54 bis Satz 2.56)", r"""
## Reihenfolgen zählen

Eine Sortierung von $n$ Elementen verwendet jedes Element genau einmal: Sie ist eine Bijektion von $n$ auf sich.

**Definition 2.54.** $\text{perm}(M) := \{\sigma \in \text{abb}(M, M) \mid \sigma \text{ bijektiv}\}$. Die Elemente heißen [[Permutationen|Permutation]].
**Definition 2.55.** $\text{fak}\colon \mathbb{N} \to \mathbb{N},\ n \mapsto |\text{perm}(n)|$ und $n! := \text{fak}(n)$ ([[Fakultät]]). Es gilt $0! = 1$, denn die leere Abbildung ist die einzige Bijektion von $0$ nach $0$.
**Satz 2.56 (Übung).** $|\text{perm}(M)| = |M|!$.

:::rechnung Die sechs Permutationen von $\{0, 1, 2\}$ (als Tupel $(\sigma(0), \sigma(1), \sigma(2))$)
§PERM§ || sechs Reihenfolgen
3! = 6 || also $|\text{perm}(3)| = 6$
:::

:::alt Als Sitzordnung
Drei Gäste (Nummern $0, 1, 2$) setzen sich auf drei Plätze. Jede Sitzordnung ist eine Permutation. Es gibt $6$ Möglichkeiten, bei $0$ Gästen genau eine (leerer Raum).
:::
""".replace("§PERM§", _PERM3))

k.zahl(r"Wie viele verschiedene Reihenfolgen gibt es, $4$ verschiedene Bücher in ein Regal zu stellen, also $|\text{perm}(4)|$?", 24,
       r"$|\text{perm}(4)| = 4! = 24$. Für den ersten Platz hast du $4$ Bücher zur Wahl, dann $3$, dann $2$, dann $1$: $4 \cdot 3 \cdot 2 \cdot 1 = 24$.",
       tipps=["Wie viele Bücher kommen für den ersten Platz in Frage?", r"Danach bleiben drei Bücher übrig.", r"$4 \cdot 3 \cdot 2 \cdot 1$"],
       rechenweg=r"""
:::rechnung
4 \cdot 3 \cdot 2 \cdot 1 = 24 || $4$ Möglichkeiten für Platz $1$, dann $3$, dann $2$, dann $1$
:::
""",
       typische_fehler=[(256, r"Das ist $4^4$: Du darfst ein Buch nicht mehrfach verwenden. Nach jeder Wahl bleibt ein Buch weniger."),
                        (16, r"Das ist $4 \cdot 4$ oder $4^2$. Nach der ersten Wahl hast du nur noch $3$ Bücher."),
                        (10, r"Das ist die Summe $1 + 2 + 3 + 4$. Die Wahlmöglichkeiten werden multipliziert.")])

# ── Seite 6: Satz 2.57 ───────────────────────────────────────────────────
k.erklaerung("n! als Produkt (Satz 2.57)", r"""
## Die Rekursion der Fakultät

**Satz 2.57.** Für alle $n \ge 1$ gilt $n! = \prod_{i=1}^{n} i$.

Der Beweis ist eine Induktion über $n$. Im Schritt liest du eine Permutation $\sigma \in \text{perm}(n+1)$ als Reihenfolge $(\sigma(0), \ldots, \sigma(n))$.
Du wählst zuerst $x := \sigma(0) \in n + 1$ ($n + 1$ Möglichkeiten). Die übrigen $n$ Elemente nummerierst du zu $0, \ldots, n - 1$ um und erhältst eine Permutation $\pi_\sigma \in \text{perm}(n)$.
Die Abbildung $\sigma \mapsto (\sigma(0), \pi_\sigma)$ ist eine Bijektion $\text{perm}(n+1) \to (n+1) \times \text{perm}(n)$.

:::rechnung Der Schritt an Zahlen
4! = 4 \cdot 3! || $(n + 1) \cdot n!$ mit $n = 3$
4 \cdot 6 = 24 || $3! = 6$ aus der Annahme
1 \cdot 2 \cdot 3 \cdot 4 = 24 || $\prod_{i=1}^{4} i$ stimmt überein
:::

:::alt Als Schlange
$n + 1$ Personen stellen sich an. Du wählst, wer vorne steht ($n + 1$ Möglichkeiten), danach ordnest du die übrigen $n$ in beliebiger Reihenfolge ($n!$ Möglichkeiten): $(n+1) \cdot n!$.
:::
""")

k.ordnen(r"Ordne den Induktionsbeweis von Satz 2.57: $n! = \prod_{i=1}^{n} i$ für $n \ge 1$.",
         [r"Induktionsanfang: $\text{perm}(1) = \{\text{id}_1\}$, also $1! = 1 = \prod_{i=1}^{1} i$.",
          r"Induktionsannahme: Für ein $n \ge 1$ gelte $n! = \prod_{i=1}^{n} i$.",
          r"Eine Permutation $\sigma \in \text{perm}(n+1)$ liest du als Reihenfolge $(\sigma(0), \ldots, \sigma(n))$ und wählst zuerst $x := \sigma(0)$.",
          r"Die übrigen $n$ Elemente nummerierst du um und erhältst $\pi_\sigma \in \text{perm}(n)$. So ist $\sigma \mapsto (\sigma(0), \pi_\sigma)$ eine Bijektion $\text{perm}(n+1) \to (n+1) \times \text{perm}(n)$.",
          r"Nach Satz 2.11, Satz 2.31 und der Annahme gilt $(n+1)! = (n+1) \cdot n! = (n+1) \cdot \prod_{i=1}^{n} i = \prod_{i=1}^{n+1} i$. $\square$"],
         r"Der Schritt zerlegt eine Reihenfolge von $n + 1$ Elementen in die Wahl des ersten und eine Reihenfolge der übrigen $n$. Die Produktregel (Satz 2.31) liefert den Faktor $n + 1$.",
         ablenker=[r"Aus $\sigma \in \text{perm}(n+1)$ folgt $\sigma(n) = n$, also bleibt nur $\text{perm}(n)$ übrig.",
                   r"Induktionsannahme: Für alle $n \ge 1$ gelte $n! = \prod_{i=1}^{n} i$."],
         tipps=["Der Beweis läuft über das Zerlegen einer Reihenfolge in das erste Element und den Rest.", "Wo kommt der Faktor $n + 1$ her?",
                "Die Annahme gilt für ein festes $n$, nicht für alle."])

# ── Seite 7: k-elementige Teilmengen ─────────────────────────────────────
k.erklaerung("Teilmengen fester Größe (Def. 2.58, 2.59, Satz 2.60)", r"""
## Auswählen ohne Reihenfolge

**Definition 2.58.** $\text{tm}_k(M) := \{A \subseteq M \mid A \text{ endlich}, |A| = k\}$ ist die Menge der $k$-elementigen Teilmengen.
**Definition 2.59.** $\binom{n}{k} := |\text{tm}_k(n)|$ („$n$ über $k$“, [[Binomialkoeffizient]]).
**Satz 2.60 (Übung).** $|\text{tm}_k(M)| = \binom{|M|}{k}$ für jede endliche Menge $M$.

Für $k > n$ ist $\text{tm}_k(n) = \emptyset$, also $\binom{n}{k} = 0$. Für $k = 0$ ist $\emptyset$ die einzige Teilmenge, also $\binom{n}{0} = 1$.

:::rechnung Die $2$-elementigen Teilmengen von $4 = \{0, 1, 2, 3\}$
\text{tm}_2(4) = §TM24§ || alle sechs Paare, die Reihenfolge zählt nicht
\binom{4}{2} = 6 || Anzahl der Paare
\binom{3}{5} = 0 \text{ und } \binom{3}{0} = 1 || keine $5$-elementige Teilmenge, genau eine $0$-elementige
:::

:::alt Als Team-Auswahl
Aus vier Personen wählst du ein Zweierteam. Das Team $\{0, 1\}$ ist dasselbe wie $\{1, 0\}$: Es zählt nur, wer dabei ist, nicht in welcher Reihenfolge du ihn genannt hast.
:::
""".replace("§TM24§", _TM24))

k.zahl(r"Wie viele $2$-elementige Teilmengen hat $\{a, b, c, d, e\}$, also $\binom{5}{2}$?", 10,
       r"$\{a,b\}, \{a,c\}, \{a,d\}, \{a,e\}, \{b,c\}, \{b,d\}, \{b,e\}, \{c,d\}, \{c,e\}, \{d,e\}$: zehn Stück.",
       tipps=["Zähle systematisch: erst alle Paare mit $a$, dann alle ohne $a$ mit $b$, …", r"Mit $a$ gibt es $4$ Paare, mit $b$ (ohne $a$) $3$, …", r"$4 + 3 + 2 + 1$"],
       rechenweg=r"""
:::rechnung
4 + 3 + 2 + 1 = 10 || Paare mit $a$, dann mit $b$ (ohne $a$), dann mit $c$ (ohne $a, b$), dann mit $d$
:::
""",
       typische_fehler=[(20, r"Das ist $5 \cdot 4$: Du zählst geordnete Paare, $(a, b)$ und $(b, a)$ zählen dann doppelt. Die Teilmenge $\{a, b\}$ gibt es nur einmal."),
                        (25, r"Das ist $5 \cdot 5$, also auch Paare mit gleichen Elementen und beide Reihenfolgen. Eine Teilmenge hat $2$ **verschiedene** Elemente."),
                        (7, r"Das ist $5 + 2$. Die Teilmengen werden multipliziert/gezählt, nicht addiert.")])

# ── Seite 8: Satz 2.61 ───────────────────────────────────────────────────
k.erklaerung("Die Formel für den Binomialkoeffizienten (Satz 2.61)", r"""
## Aus Permutationen gewonnen

**Satz 2.61.** Für $k \le n$ gilt $\binom{n}{k} = \dfrac{n!}{k!\,(n-k)!}$.

*Beweisidee.* Ordne alle $n$ Elemente an (das sind $n!$ Permutationen). Für jede Auswahl $A \in \text{tm}_k(n)$ sei $P_A$ die Menge der Permutationen, die die ersten $k$ Plätze auf $A$ abbilden.
In $P_A$ darfst du die $k$ Elemente von $A$ beliebig anordnen ($k!$ Möglichkeiten) und die übrigen $n - k$ beliebig ($(n-k)!$): $|P_A| = k!\,(n-k)!$.
Jede Permutation liegt in genau einem $P_A$. Also ist $n! = \binom{n}{k} \cdot k!\,(n-k)!$.

:::rechnung $\binom{5}{2}$ mit der Formel
\frac{5!}{2! \cdot 3!} = \frac{120}{2 \cdot 6} || $5! = 120$, $2! = 2$, $3! = 6$
\frac{120}{12} = 10 || ausgerechnet: das passt zu den zehn Paaren von eben
10 \cdot 2! \cdot 3! = 120 = 5! || Probe: $\binom{5}{2} \cdot 2! \cdot 3! = 5!$
:::

:::alt Als Ausschuss
Du schreibst alle $n!$ Reihenfolgen der Personen auf. Danach vergisst du die Reihenfolge innerhalb des Ausschusses ($k!$ Anordnungen sind dasselbe) und innerhalb der übrigen ($(n-k)!$): Dann teilst du durch $k!\,(n-k)!$.
:::
""")

k.luecke(r"Berechne $\binom{6}{2}$ mit Satz 2.61. Fülle die Lücken.",
         r"\binom{6}{2} = \frac{6!}{2! \cdot \luecke!} = \luecke",
         [[4], [15]],
         r"$n - k = 6 - 2 = 4$ und $\frac{6!}{2! \cdot 4!} = \frac{720}{2 \cdot 24} = \frac{720}{48} = 15$.",
         tipps=[r"Der zweite Fakultätsterm im Nenner ist $(n - k)!$.", r"$6 - 2 = 4$", r"$\frac{720}{48}$"],
         rechenweg=r"""
:::rechnung
\frac{6!}{2! \cdot 4!} = \frac{720}{2 \cdot 24} || $6! = 720$
\frac{720}{48} = 15 || ausgerechnet
:::
""",
         typische_fehler=[([2, 180], r"Im Nenner steht $k! \cdot (n - k)!$, also $2! \cdot 4!$ und nicht $2! \cdot 2!$. Mit $\frac{720}{2 \cdot 2} = 180$ hast du durch $2! \cdot 2!$ geteilt.")])

# ── Seite 9: Pascal ──────────────────────────────────────────────────────
k.erklaerung("Pascalsche Regel (Satz 2.62)", r"""
## Jede Zahl ist die Summe der beiden darüber

**Satz 2.62 ([[Pascalsche Regel]]).** Für $k \ge 1$ gilt $\binom{n+1}{k} = \binom{n}{k} + \binom{n}{k-1}$.

*Beweis.* Zerlege $\text{tm}_k(n+1)$ in $A_0 := \{A \mid n \notin A\}$ und $A_1 := \{A \mid n \in A\}$. Die Abbildung $A \mapsto A$ ist eine Bijektion $A_0 \to \text{tm}_k(n)$.
Die Abbildung $A \mapsto A \setminus \{n\}$ ist eine Bijektion $A_1 \to \text{tm}_{k-1}(n)$ (Umkehrung $B \mapsto B \cup \{n\}$). Die Mengen $A_0$ und $A_1$ sind disjunkt, also addieren sich die Anzahlen (Satz 2.21).

:::visual pascal
{"zeilen": 7, "markiert": [[5, 2]],
 "unterschrift": "Tippe auf $\\binom{5}{2} = 10$: Die Zahl ist $\\binom{4}{2} + \\binom{4}{1} = 6 + 4$. Das ist das Pascalsche Dreieck."}
:::

:::rechnung Wie die Regel zählt
6 + 4 = 10 || $\binom{4}{2} + \binom{4}{1}$: Paare ohne das neue Element $+$ Paare mit ihm
\binom{5}{2} = 10 || $\text{tm}_2(5)$ hat zehn Paare
:::

:::alt Als Wahl des letzten Elements
Wähle $k$ aus $n + 1$ Personen. Entweder die letzte Person ist **nicht** dabei: Dann wählst du alle $k$ aus den ersten $n$. Oder sie **ist** dabei: Dann fehlen noch $k - 1$ aus den ersten $n$.
:::
""")

k.ordnen(r"Ordne den Beweis der Pascalschen Regel (Satz 2.62): $\binom{n+1}{k} = \binom{n}{k} + \binom{n}{k-1}$ für $k \ge 1$.",
         [r"Zerlege $\text{tm}_k(n+1)$ in $A_0 := \{A \mid n \notin A\}$ und $A_1 := \{A \mid n \in A\}$.",
          r"Die Abbildung $A \mapsto A$ ist eine Bijektion von $A_0$ nach $\text{tm}_k(n)$.",
          r"Die Abbildung $A \mapsto A \setminus \{n\}$ ist eine Bijektion von $A_1$ nach $\text{tm}_{k-1}(n)$, ihre Umkehrung ist $B \mapsto B \cup \{n\}$.",
          r"Da $A_0$ und $A_1$ disjunkt sind, gilt nach Satz 2.21 und Satz 2.11: $|\text{tm}_k(n+1)| = |A_0| + |A_1|$.",
          r"Also ist $\binom{n+1}{k} = \binom{n}{k} + \binom{n}{k-1}$. $\square$"],
         r"Man teilt die Auswahlen danach, ob das Element $n$ dabei ist. Beide Teile lassen sich mit Bijektionen auf kleinere Auswahlen zurückführen.",
         ablenker=[r"Die Abbildung $A \mapsto A \cup \{n\}$ ist eine Bijektion von $A_0$ nach $\text{tm}_{k-1}(n)$.",
                   r"Die Mengen $A_0$ und $A_1$ haben gemeinsame Elemente, also muss man $|A_0 \cap A_1|$ abziehen."],
         tipps=["Teile nach der Frage: Ist das Element $n$ in der Teilmenge oder nicht?", "Wohin führt die Abbildung, die $n$ aus $A$ entfernt?",
                "Disjunkte Vereinigung heißt: einfach addieren."])

# ── Seite 10: Binomischer Lehrsatz ───────────────────────────────────────
k.erklaerung("Binomischer Lehrsatz (Satz 2.63, Korollar 2.64)", r"""
## $(a + b)^n$ ausmultiplizieren

**Satz 2.63 ([[binomischer Lehrsatz]]).** Für alle $a, b, n \in \mathbb{N}$ gilt
$$(a + b)^n = \sum_{k=0}^{n} \binom{n}{k} a^k b^{n-k}.$$

Der Beweis (Übung) ist eine Induktion mit der Pascalschen Regel. Anschaulich: Beim Ausmultiplizieren von $n$ Klammern wählst du aus jeder $a$ oder $b$. Der Term $a^k b^{n-k}$ entsteht, wenn du in genau $k$ Klammern $a$ wählst, und dafür gibt es $\binom{n}{k}$ Möglichkeiten.

**Korollar 2.64.** $\sum_{k=0}^{n} \binom{n}{k} = 2^n$ (setze $a = b = 1$).

:::rechnung Beispiele
(a + b)^3 = b^3 + 3ab^2 + 3a^2 b + a^3 || Koeffizienten $1, 3, 3, 1$: die Zeile $n = 3$ im Pascalschen Dreieck
(1 + 1)^4 = 2^4 = 16 = 1 + 4 + 6 + 4 + 1 || Korollar 2.64 für $n = 4$
:::

:::alt Als Summe aller Teilmengen
Die Zahl $\binom{n}{k}$ zählt die Teilmengen der Größe $k$. Alle Teilmengen zusammen sind $\sum_k \binom{n}{k}$, und nach Satz 2.53 sind das $2^n$.
:::
""")

k.zahl(r"Welchen Koeffizienten hat $a^2 b^3$ in $(a + b)^5$ nach dem binomischen Lehrsatz?", 10,
       r"Der Koeffizient von $a^k b^{n-k}$ ist $\binom{n}{k}$. Hier $n = 5$, $k = 2$: $\binom{5}{2} = 10$.",
       tipps=[r"Lies $n$ und $k$ ab: $a^2 b^3$ mit $2 + 3 = 5$.", r"Gesucht ist $\binom{5}{2}$.", r"$\binom{5}{2} = \frac{5!}{2! \cdot 3!}$"],
       rechenweg=r"""
:::rechnung
\frac{5!}{2! \cdot 3!} = \frac{120}{12} = 10 || $\binom{5}{2}$
:::
""",
       typische_fehler=[(1, r"Das wäre der Koeffizient von $a^5$ oder $b^5$. Bei gemischten Potenzen $a^2 b^3$ steht ein Binomialkoeffizient davor."),
                        (6, r"Das ist $2 \cdot 3$. Der Koeffizient ist $\binom{5}{2}$, nicht das Produkt der Exponenten."),
                        (32, r"Das ist die Summe aller Koeffizienten $2^5$ (Korollar 2.64), nicht der einzelne.")])

k.mc(r"Was ergibt $\sum_{k=0}^{5} \binom{5}{k}$?",
     [r"$32 = 2^5$ (Korollar 2.64)", r"$25 = 5^2$", r"$120 = 5!$", r"$10 = \binom{5}{2}$"],
     r"Korollar 2.64: Setze $a = b = 1$ im binomischen Lehrsatz, $(1 + 1)^5 = 32$. Als Teilmengen gezählt: alle Teilmengen von $5$ Elementen, $|\mathcal{P}(5)| = 2^5$. Zeile $5$ des Dreiecks: $1 + 5 + 10 + 10 + 5 + 1 = 32$.",
     tipps=[r"Setze $a = b = 1$ in $(a + b)^n$.", r"Die Summe zählt alle Teilmengen aller Größen.", r"Zeile $5$ des Pascalschen Dreiecks ist $1, 5, 10, 10, 5, 1$."],
     fehler={r"$25 = 5^2$": r"Basis und Exponent vertauscht: $(1 + 1)^5 = 2^5$, nicht $5^2$.",
             r"$120 = 5!$": r"Die Fakultät zählt Reihenfolgen, die Summe der Binomialkoeffizienten zählt Teilmengen.",
             r"$10 = \binom{5}{2}$": r"Das ist nur **ein** Summand der Zeile $5$, nicht die ganze Summe."})


# ── Praxis ────────────────────────────────────────────────────────────────
def rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def abbildungen_zaehlen(rng):
    while True:
        a, n = rng.choice([2, 3, 4, 5, 6, 10]), rng.choice([2, 3, 4, 5])
        if a ** n != n ** a and a != n:
            break
    loesung = a ** n
    szenario = rng.choice(["pin", "abb", "code", "bits"] if a != 2 else ["abb", "bits", "potenz"])
    if szenario == "pin":
        frage = f"Ein Zahlenschloss hat ${n}$ Stellen, jede zeigt eine Ziffer aus $\\{{0, \\ldots, {a - 1}\\}}$. Wie viele Einstellungen gibt es?"
    elif szenario == "abb":
        frage = f"Wie viele Abbildungen $f\\colon B \\to A$ gibt es, wenn $|B| = {n}$ und $|A| = {a}$ ist?"
    elif szenario == "code":
        frage = f"Ein Code besteht aus ${n}$ Zeichen eines Alphabets mit ${a}$ Zeichen (Wiederholungen erlaubt). Wie viele Codes gibt es?"
    elif szenario == "bits":
        a = 2
        n = rng.choice([3, 5, 6, 7, 8])
        loesung = 2 ** n
        frage = f"Wie viele Bitstrings der Länge ${n}$ gibt es?"
    else:
        a = 2
        n = rng.choice([3, 5, 6, 7])
        loesung = 2 ** n
        frage = f"Eine Menge $M$ hat ${n}$ Elemente. Wie viele Teilmengen hat $M$?"
    fehler = [(n ** a if szenario in ("pin", "abb", "code") else a * n, "Basis und Exponent vertauscht: Die Basis ist die Anzahl der **Werte** je Stelle, der Exponent die Anzahl der Stellen."),
              (a * n, "Du hast multipliziert statt zu potenzieren. Die Wahl je Stelle ist unabhängig: $a \\cdot a \\cdot \\ldots \\cdot a$ ($n$ Faktoren)."),
              (a ** n - 1, "Es gibt keinen Grund, eine Möglichkeit abzuziehen: Auch die „Nullstellung“ zählt (Satz 2.49).")]
    return {
        "frage": frage, "loesung": loesung,
        "tipps": ["Wie viele Möglichkeiten gibt es für eine einzelne Stelle (bzw. ein einzelnes Element)?", "Die Wahlen sind unabhängig: Die Anzahl multipliziert sich.",
                  f"Rechne ${a} \\cdot \\ldots \\cdot {a}$ mit ${n}$ Faktoren, also ${a}^{{{n}}}$."],
        "rechenweg": rechnung([(f"{a}^{{{n}}} = {loesung}", f"Satz 2.49: $|A|^{{|B|}}$ mit $|A| = {a}$, $|B| = {n}$")]),
        "erklaerung": "Satz 2.49: Die Anzahl der Abbildungen $B \\to A$ ist $|A|^{|B|}$. Zeichenketten, Bitstrings und Teilmengen sind Spezialfälle (Satz 2.47, 2.53).",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


def reihenfolgen_zaehlen(rng):
    n = rng.randint(4, 8)
    loesung = factorial(n)
    was = rng.choice([f"Auf einem Podest sollen ${n}$ verschiedene Personen", f"In einem Regal sollen ${n}$ verschiedene Bücher",
                      f"In einer Playlist sollen ${n}$ verschiedene Lieder", f"Eine Staffel besteht aus ${n}$ verschiedenen Läuferinnen, die"])
    ende = rng.choice(["in beliebiger Reihenfolge nebeneinander stehen", "in beliebiger Reihenfolge stehen", "in beliebiger Reihenfolge laufen"])
    ende = {"Auf": "in beliebiger Reihenfolge nebeneinander stehen", "In ": "in beliebiger Reihenfolge angeordnet werden", "Ein": "in beliebiger Reihenfolge laufen"}[was[:3]]
    prod_text = " \\cdot ".join(str(i) for i in range(n, 0, -1))
    fehler = [(n ** n, "Jedes Element wird genau einmal verwendet, es gibt keine Wiederholungen. Nach jeder Wahl bleibt eines weniger: Das ist $n!$, nicht $n^n$."),
              (n * (n - 1), "Das sind nur die ersten beiden Faktoren. Auch für die weiteren Plätze musst du multiplizieren."),
              (factorial(n - 1), "Das ist $(n-1)!$. Der erste Platz hat $n$ Möglichkeiten, die dazugehören.")]
    return {
        "frage": f"{was} {ende}. Wie viele Reihenfolgen gibt es, also $|\\text{{perm}}({n})|$?",
        "loesung": loesung,
        "tipps": ["Wie viele Personen kommen für den ersten Platz in Frage? Und danach?", f"Für den ersten Platz ${n}$, für den zweiten ${n - 1}$, …", f"${n}! = {prod_text}$"],
        "rechenweg": rechnung([(f"{n}! = {prod_text} = {loesung}", f"Satz 2.57: $n! = \\prod_{{i=1}}^{{n}} i$")]),
        "erklaerung": "Eine Reihenfolge ist eine Bijektion $n \\to n$. Es gibt $n!$ davon (Definition 2.55, Satz 2.57).",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


def teams_auswaehlen(rng):
    n = rng.randint(5, 9)
    kk = rng.randint(2, 4)
    loesung = comb(n, kk)
    geordnet = factorial(n) // factorial(n - kk)
    fehler = [(geordnet, f"Du hast die Reihenfolge mitgezählt ($\\frac{{n!}}{{(n-k)!}} = {geordnet}$). Im Team zählt nur, **wer** dabei ist: Teile noch durch $k! = {factorial(kk)}$."),
              (n ** kk, "Das wäre eine Auswahl **mit** Wiederholung und Reihenfolge. Hier sind es $k$ verschiedene Personen ohne Reihenfolge."),
              (n * kk, "Du hast multipliziert statt $\\binom{n}{k}$ auszurechnen.")]
    return {
        "frage": f"Aus ${n}$ Personen soll ein Team aus ${kk}$ Personen ausgewählt werden (die Reihenfolge spielt keine Rolle). Wie viele Teams gibt es, also $\\binom{{{n}}}{{{kk}}}$?",
        "loesung": loesung,
        "tipps": [f"Gesucht ist die Anzahl der ${kk}$-elementigen Teilmengen von ${n}$ Elementen.", f"Satz 2.61: $\\binom{{n}}{{k}} = \\frac{{n!}}{{k! \\, (n-k)!}}$ mit $n = {n}$, $k = {kk}$.",
                  f"Rechne $\\frac{{{n}!}}{{{kk}! \\cdot {n - kk}!}}$."],
        "rechenweg": rechnung([(f"\\frac{{{n}!}}{{{kk}! \\cdot {n - kk}!}} = \\frac{{{factorial(n)}}}{{{factorial(kk) * factorial(n - kk)}}} = {loesung}",
                                f"Satz 2.61, Zähler $n!$ und Nenner $k!(n-k)!$ ausgerechnet")]),
        "erklaerung": "Ein Team ist eine Teilmenge: Es gibt $\\binom{n}{k}$ davon (Definition 2.59, Satz 2.61).",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


def pascal_regel(rng):
    n = rng.randint(5, 9)
    kk = rng.randint(2, n - 2)
    a1, a2 = comb(n - 1, kk), comb(n - 1, kk - 1)
    loesung = [[a1], [a2], [a1 + a2]]
    assert a1 + a2 == comb(n, kk)
    fehler = [([a2, a1, a1 + a2], f"Die Reihenfolge ist vertauscht: Der erste Summand ist $\\binom{{{n - 1}}}{{{kk}}} = {a1}$, der zweite $\\binom{{{n - 1}}}{{{kk - 1}}} = {a2}$."),
              ([a1, a2, a1 * a2], "Die Pascalsche Regel **addiert** die beiden Zahlen darüber."),
              ([a1, a1, 2 * a1], f"Der zweite Summand ist $\\binom{{{n - 1}}}{{{kk - 1}}}$ (eine Stelle weiter links im Dreieck), nicht dasselbe wie der erste.")]
    return {
        "frage": f"Berechne $\\binom{{{n}}}{{{kk}}}$ mit der Pascalschen Regel. Du darfst $\\binom{{{n - 1}}}{{{kk}}}$ und $\\binom{{{n - 1}}}{{{kk - 1}}}$ aus dem Dreieck oder mit Satz 2.61 bestimmen.",
        "formel": f"\\binom{{{n}}}{{{kk}}} = \\binom{{{n - 1}}}{{{kk}}} + \\binom{{{n - 1}}}{{{kk - 1}}} = \\luecke + \\luecke = \\luecke",
        "antworten": loesung,
        "tipps": [f"Satz 2.62: $\\binom{{n+1}}{{k}} = \\binom{{n}}{{k}} + \\binom{{n}}{{k-1}}$ mit $n + 1 = {n}$.", f"Bestimme $\\binom{{{n - 1}}}{{{kk}}}$ und $\\binom{{{n - 1}}}{{{kk - 1}}}$ einzeln.",
                  f"$\\binom{{{n - 1}}}{{{kk}}} = {a1}$ und $\\binom{{{n - 1}}}{{{kk - 1}}} = {a2}$."],
        "rechenweg": rechnung([(f"{a1} + {a2} = {a1 + a2}", f"Summe der beiden Zahlen über $\\binom{{{n}}}{{{kk}}}$ im Pascalschen Dreieck")]),
        "erklaerung": "Jede Zahl im Pascalschen Dreieck ist die Summe der beiden Zahlen darüber (Satz 2.62).",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


def potenz_rest(rng):
    while True:
        n = rng.randint(5, 13)
        a = rng.randint(2, 12)
        kk = rng.randint(4, 8)
        ra = a % n
        loesung = pow(a, kk, n)
        if ra not in (0, 1, n - 1) and loesung not in (0, 1, ra) and a != n:
            break
    zeilen, r = [], ra
    for e in range(2, kk + 1):
        neu = (r * ra) % n
        zeilen.append((f"{r} \\cdot {ra} = {r * ra} = {r * ra // n} \\cdot {n} + {neu}", f"Rest von $({a} \\bmod {n})^{{{e}}}$: Satz 2.52, nach jedem Schritt Rest nehmen"))
        r = neu
    assert r == loesung
    fehler = [((ra * kk) % n, f"Du hast $({a} \\bmod {n}) \\cdot {kk}$ gerechnet. Der Exponent ${kk}$ heißt: ${kk}$-mal mit ${ra}$ multiplizieren."),
              (a ** kk, f"Das ist ${a}^{{{kk}}}$ selbst. Es fehlt der Rest bei Division durch ${n}$."),
              (ra, f"Das ist nur ${a} \\bmod {n}$. Die Potenz muss mitgerechnet werden.")]
    return {
        "frage": f"Bestimme ${a}^{{{kk}}} \\bmod {n}$ mit Satz 2.52, ohne ${a}^{{{kk}}}$ voll auszurechnen.",
        "loesung": loesung,
        "tipps": [f"Ersetze ${a}$ durch ${a} \\bmod {n} = {ra}$.", f"Multipliziere der Reihe nach mit ${ra}$ und nimm nach jedem Schritt den Rest modulo ${n}$.",
                  f"Die Reste lauten der Reihe nach: ${', '.join(str(pow(a, e, n)) for e in range(1, kk + 1))}$."],
        "rechenweg": rechnung(zeilen),
        "erklaerung": "Satz 2.52 und Satz 2.44: Du darfst nach jeder Multiplikation den Rest nehmen, die Zahlen bleiben klein.",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


k.praxis()

k.generator(abbildungen_zaehlen, typ="zahl", titel="Abbildungen, Codes und Teilmengen zählen")
k.generator(reihenfolgen_zaehlen, typ="zahl", titel="Reihenfolgen zählen (Fakultät)")
k.generator(teams_auswaehlen, typ="zahl", titel="Teams auswählen (Binomialkoeffizient)")
k.generator(pascal_regel, typ="luecke", titel="Pascalsche Regel anwenden")
k.generator(potenz_rest, typ="zahl", titel="Potenzen modulo n")

k.rechenweg_aufgabe(r"""
## Quiz-Stil: Teilmengen einer Menge

Sei $M$ eine Menge mit $5$ Elementen.
""",
    [{"typ": "zahl", "frage": r"Wie viele Teilmengen hat $M$ insgesamt?", "loesung": 32,
      "tipps": [r"Satz 2.53: $|\mathcal{P}(M)| = 2^{|M|}$.", r"$2^5$"],
      "rechenweg": r"$2^5 = 32$.", "erklaerung": r"Jedes der $5$ Elemente ist drin oder nicht.",
      "typische_fehler": [(25, r"Das ist $5^2$. Die Basis ist $2$, der Exponent $|M| = 5$.")]},
     {"typ": "zahl", "frage": r"Wie viele davon haben genau $2$ Elemente?", "loesung": 10,
      "tipps": [r"Gesucht ist $\binom{5}{2}$.", r"$\frac{5!}{2! \cdot 3!}$"],
      "rechenweg": r"$\binom{5}{2} = \frac{120}{2 \cdot 6} = 10$.", "erklaerung": "Zweielementige Teilmengen sind genau $\\binom{5}{2}$.",
      "typische_fehler": [(20, r"Du hast die Reihenfolge mitgezählt ($5 \cdot 4$). Teile durch $2! = 2$.")]},
     {"typ": "zahl", "frage": r"Wie viele davon haben **höchstens** $2$ Elemente?", "loesung": 16,
      "tipps": [r"Höchstens $2$ heißt $0$, $1$ oder $2$ Elemente.", r"$\binom{5}{0} + \binom{5}{1} + \binom{5}{2}$"],
      "rechenweg": r"$1 + 5 + 10 = 16$.", "erklaerung": r"Die disjunkten Fälle (Satz 2.21) werden addiert: $\binom{5}{0} = 1$, $\binom{5}{1} = 5$, $\binom{5}{2} = 10$.",
      "typische_fehler": [(15, r"Die leere Menge zählt auch: $\binom{5}{0} = 1$ gehört dazu."),
                          (10, r"Das sind nur die Teilmengen mit **genau** $2$ Elementen.")]}],
    r"$|\mathcal{P}(M)| = 32$, davon $\binom{5}{2} = 10$ mit genau zwei und $1 + 5 + 10 = 16$ mit höchstens zwei Elementen.",
    uebungsblatt=True,
    tipps=["Für „höchstens“ addierst du die Fälle $0$, $1$ und $2$.", "Die Fälle sind disjunkt, also addierst du nach Satz 2.21."],
    rechenweg=r"""
:::rechnung
2^5 = 32 || alle Teilmengen
\frac{5!}{2! \cdot 3!} = 10 || genau zwei Elemente
1 + 5 + 10 = 16 || $\binom{5}{0} + \binom{5}{1} + \binom{5}{2}$
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Fakultät, Potenz und Lehrsatz

1. Beweisen Sie Satz 2.56: $|\text{perm}(M)| = |M|!$ für jede endliche Menge $M$. Geben Sie dazu eine Bijektion $\text{perm}(M) \to \text{perm}(|M|)$ an.
2. Beweisen Sie Satz 2.63 (binomischer Lehrsatz) per Induktion über $n$ mit der Pascalschen Regel. Benutzen Sie $a, b \in \mathbb{N}$ beliebig.
""",
    r"""
**1.** Sei $g\colon |M| \to M$ eine Bijektion. Definiere $\Phi\colon \text{perm}(M) \to \text{perm}(|M|)$, $\sigma \mapsto g^{-1} \circ \sigma \circ g$ und $\Psi\colon \text{perm}(|M|) \to \text{perm}(M)$, $\tau \mapsto g \circ \tau \circ g^{-1}$.
Beide sind wohldefiniert, denn Verkettungen von Bijektionen sind bijektiv (Satz 1.82). Es gilt $\Psi(\Phi(\sigma)) = g g^{-1} \sigma g g^{-1} = \sigma$ und $\Phi(\Psi(\tau)) = \tau$. Nach Satz 1.76 ist $\Phi$ bijektiv.
Mit Satz 2.11: $|\text{perm}(M)| = |\text{perm}(|M|)| = |M|!$. $\square$

**2. Anfang** ($n = 0$): $(a + b)^0 = 1 = \binom{0}{0} a^0 b^0$.
**Annahme:** Für ein $n$ gelte $(a+b)^n = \sum_{k=0}^{n} \binom{n}{k} a^k b^{n-k}$.
**Schritt:** $(a+b)^{n+1} = (a+b)(a+b)^n = \sum_{k=0}^{n} \binom{n}{k} a^{k+1} b^{n-k} + \sum_{k=0}^{n} \binom{n}{k} a^k b^{n+1-k}$ (Distributivität, Potenzgesetze).
Im ersten Summanden nennst du $j := k + 1$ um: $\sum_{j=1}^{n+1} \binom{n}{j-1} a^j b^{n+1-j}$. Dann sind beide Summen über $a^j b^{n+1-j}$ geschrieben, und für $1 \le j \le n$ steht dort $\binom{n}{j-1} + \binom{n}{j} = \binom{n+1}{j}$ (Pascal). Die Randterme $j = 0$ und $j = n+1$ haben den Koeffizienten $1 = \binom{n+1}{0} = \binom{n+1}{n+1}$.
Also $(a+b)^{n+1} = \sum_{j=0}^{n+1} \binom{n+1}{j} a^j b^{n+1-j}$. $\square$
""",
    ["In 1.: beide Abbildungen $\\Phi$ und $\\Psi$ angegeben und gezeigt, dass sie zueinander invers sind",
     "In 1.: Satz 2.11 zum Schluss benutzt, um $|\\text{perm}(M)| = |M|!$ zu erhalten",
     "In 2.: Anfang bei $n = 0$ korrekt",
     "In 2.: Im Schritt $(a+b)^{n+1} = (a+b) \\cdot (a+b)^n$ und die Annahme eingesetzt, dann ausmultipliziert",
     "In 2.: Indexverschiebung $j = k + 1$ und die Pascalsche Regel für $1 \\le j \\le n$ benutzt, Randterme gesondert behandelt"],
    "Bei 1. wird eine Bijektion „umbenannt“, bei 2. ist die Pascalsche Regel der Schlüssel zum Zusammenfassen der beiden Summen.",
    uebungsblatt=True,
    tipps=["Bei 1.: Die Umkehrabbildung von $\\Phi$ benutzt $g$ und $g^{-1}$ in der anderen Reihenfolge.", "Bei 2.: Multipliziere $(a + b)$ in die Summe und trenne $a \\cdot$ und $b \\cdot$.",
           "Bei 2.: Nach der Indexverschiebung stehen zwei Summen mit gleichem Term $a^j b^{n+1-j}$."])

k.zusammenfassung(r"""
## Potenz, Fakultät, Binomialkoeffizient (Skript Abschn. 2.6 bis 2.8)

- **Abbildungen zählen** (Def. 2.46, 2.48; Satz 2.47, 2.49): $\text{abb}(B, A)$ hat $|A|^{|B|}$ Elemente. $a^n := |\text{abb}(n, a)|$, $a^0 = 1$, $0^0 = 1$. Satz 2.50: $a^n = \prod_{i=1}^{n} a$.
- **Potenzgesetze** (2.51): $a^{m+n} = a^m a^n$, $(a^m)^n = a^{mn}$, $(ab)^n = a^n b^n$. **Reste** (2.52): $a^k \bmod n = (a \bmod n)^k \bmod n$.
- **Potenzmenge** (2.53): $|\mathcal{P}(M)| = 2^{|M|}$ (Indikatorfunktion $\chi_A\colon M \to \{0, 1\}$).
- **Permutationen** (2.54): $\text{perm}(M)$ = Bijektionen $M \to M$. $n! := |\text{perm}(n)|$, $0! = 1$ (2.55). $|\text{perm}(M)| = |M|!$ (2.56). $n! = \prod_{i=1}^{n} i$ (2.57).
- **Binomialkoeffizient** (2.58, 2.59): $\binom{n}{k} := |\text{tm}_k(n)|$; $\binom{n}{k} = 0$ für $k > n$, $\binom{n}{0} = 1$. $|\text{tm}_k(M)| = \binom{|M|}{k}$ (2.60).
- **Formel** (2.61): $\binom{n}{k} = \frac{n!}{k!(n-k)!}$ für $k \le n$. **Pascal** (2.62): $\binom{n+1}{k} = \binom{n}{k} + \binom{n}{k-1}$.
- **Binomischer Lehrsatz** (2.63): $(a+b)^n = \sum_{k=0}^{n} \binom{n}{k} a^k b^{n-k}$. **Korollar 2.64:** $\sum_{k=0}^{n} \binom{n}{k} = 2^n$.

!! Basis = Größe der **Zielmenge**, Exponent = Größe der **Definitionsmenge**: $|\text{abb}(B, A)| = |A|^{|B|}$.
""")
