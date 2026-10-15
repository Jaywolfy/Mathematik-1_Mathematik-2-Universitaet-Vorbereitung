# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 11: Multiplikation, Division und Division mit Rest
(Skript Disser WS 26/27, Abschn. 2.5, Def. 2.28 bis Bsp. 2.45)."""
from itertools import product
from math import prod

from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(
    slug="division_rest",
    titel="Multiplikation, Division und Division mit Rest",
    beschreibung="Produkt als |a × b|, Produktzeichen, Teilbarkeit, Division als partielle Umkehrung, Division mit Rest (Satz 2.41), div und mod, Rechnen mit Resten (Satz 2.44)",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 2.5",
    icon="➗")


# ── Python rechnet alles nach ──────────────────────────────────────────────
def mtex(s):
    return "\\emptyset" if not s else "\\{" + ", ".join(str(x) for x in sorted(s)) + "\\}"


# Def. 2.28: a · b := |a × b|
assert all(len(set(product(range(a), range(b)))) == a * b for a in range(12) for b in range(12))
assert len(set(product(range(1, 9), "ABCDEFGH"))) == 64
# Satz 2.29, 2.30 (mit Gegenbeispiel a = 0), 2.32
assert all(a * (b + 1) == a * b + a for a in range(15) for b in range(15))
assert all((a * b != a * c) or b == c for a in range(1, 15) for b in range(15) for c in range(15))
assert 0 * 2 == 0 * 7 and 2 != 7
assert all(n * (m + r) == n * m + n * r for n in range(8) for m in range(8) for r in range(8))
# Produktzeichen (Def. 2.33), Satz 2.34, 2.35
assert prod(range(1, 5)) == 24 and sum(7 for _ in range(4)) == 28 == 7 * 4
# Teilbarkeit (Def. 2.36): b | a :⇔ ∃q: a = b·q
def teilt(b, a):
    return any(a == b * q for q in range(a + 1))
assert teilt(0, 0) and teilt(5, 0) and not teilt(0, 5) and teilt(1, 7) and teilt(7, 7) and not teilt(3, 10)
assert teilt(3, 12) and 12 // 3 == 4 and not teilt(3, 13)
# Satz 2.39, Beispiel 2.40: Kartenblatt
_RAENGE = [2, 3, 4, 5, 6, 7, 8, 9, 10, "B", "D", "K", "A"]
_FARBEN = ["♣", "♠", "♡", "♢"]
_KARTEN = list(product(_RAENGE, _FARBEN))
assert len(_KARTEN) == 52
_klassen_rang = {r: [c for c in _KARTEN if c[0] == r] for r in _RAENGE}
assert len(_klassen_rang) == 13 and all(len(v) == 4 for v in _klassen_rang.values()) and 52 // 4 == 13 and 4 * 13 == 52
# Satz 2.41: Division mit Rest, Beispiel 47 = 5·9 + 2
assert divmod(47, 9) == (5, 2) and [kk for kk in range(48) if kk * 9 <= 47] == list(range(6))
for _a in range(0, 80):
    for _b in range(1, 20):
        _paare = [(q, r) for q in range(_a + 1) for r in range(_b) if q * _b + r == _a]
        assert _paare == [(_a // _b, _a % _b)]           # existiert genau ein Paar
# Satz 2.44: Rechnen mit Resten, Beispiel 2.45
for _a in range(0, 40):
    for _b in range(0, 40):
        for _n in range(1, 14):
            assert (_a + _b) % _n == ((_a % _n) + (_b % _n)) % _n
            assert (_a * _b) % _n == ((_a % _n) * (_b % _n)) % _n
assert ((9 + 6) * 23 + 705) % 7 == 0 and (9 + 6) * 23 + 705 == 1050 == 7 * 150
assert [9 % 7, 6 % 7, (2 + 6) % 7, 23 % 7, 705 % 7] == [2, 6, 1, 2, 5]
# Übungsaufgabe: Rest von (17 + 9)·31 + 502 bei Division durch 8
assert [17 % 8, 9 % 8, (17 + 9) % 8, 31 % 8, (2 * 7) % 8, 502 % 8, ((17 + 9) * 31 + 502) % 8] == [1, 1, 2, 7, 6, 6, 4]

k.lernziele([
    "Ich kann das Produkt $a \\cdot b$ als $|a \\times b|$ erklären und kenne Nachfolgerregel, Kürzungsregel und $|A \\times B| = |A| \\cdot |B|$ (Def. 2.28, Satz 2.29 bis 2.32)",
    "Ich lese das Produktzeichen $\\prod$ und erkläre, wann $b \\mid a$ gilt und wie die Division als partielle Umkehrung definiert ist (Def. 2.33, 2.36, 2.37, Beob. 2.38)",
    "Ich wende Satz 2.39 an, wenn gleich große Äquivalenzklassen gezählt werden (Bsp. 2.40)",
    "Ich bestimme $a \\operatorname{div} b$ und $a \\bmod b$ und rechne mit Resten, um große Zahlen zu vermeiden (Satz 2.41 bis 2.44, Bsp. 2.45)",
])

k.warum(r"""
`a // b` und `a % b` sind in jeder Programmiersprache Division mit Rest. Der Rest steckt hinter Ringpuffern
(`index % laenge`), Hashtabellen (`hash(x) % m`), Uhrzeiten, Prüfziffern und der gesamten Kryptographie (Kapitel
„RSA“). Satz 2.44 erlaubt, Zwischenergebnisse sofort durch ihren Rest zu ersetzen. Genau deshalb kann ein Rechner
$m^e \bmod n$ mit riesigen Zahlen berechnen, ohne zu überlaufen. Und Satz 2.39 ist der Grund, warum ein Hash
mit $m$ Behältern bei gleichmäßiger Verteilung in jedem Behälter gleich viele Einträge hat.
""")

# ── Seite 1: Multiplikation ──────────────────────────────────────────────
k.erklaerung("Multiplikation als Zählen eines Rasters (Def. 2.28)", r"""
## Zeilen mal Spalten

:::analogie ♟️ Das Schachbrett
Ein Schachbrett hat die Zeilen $1$ bis $8$ und die Spalten $A$ bis $H$. Jedes Feld ist ein Paar (Zeile, Spalte). Die Anzahl der Felder ist die Anzahl der Paare.
:::

**Definition 2.28.** $\cdot\colon \mathbb{N}^2 \to \mathbb{N},\ (a, b) \mapsto |a \times b|$. Die Zahl $ab := a \cdot b$ heißt Produkt von $a$ und $b$.
Insbesondere gilt $a \cdot 1 = a$. Du zählst also die Paare $(x, y)$ mit $x \in a$ und $y \in b$, also $a$ Zeilen mit je $b$ Einträgen.

:::rechnung Das Schachbrett
|\{1, \ldots, 8\} \times \{A, \ldots, H\}| = 64 || jedes Feld ist ein Paar (Zeile, Spalte)
8 \cdot 8 = 64 || acht Zeilen mit je acht Feldern
3 \cdot 4 = 12 || $3 \times 4$-Raster: $3$ Zeilen, je $4$ Einträge
:::

:::alt Mit Kacheln
Du fliest einen Boden mit $a$ Reihen zu je $b$ Kacheln. Die Gesamtzahl der Kacheln ist $a \cdot b$. Dreh den Boden um $90°$: dann sind es $b$ Reihen zu je $a$
Kacheln, also $b \cdot a$. Die Anzahl der Paare hängt nicht von der Zählweise ab.
:::
""")

k.zahl(r"Ein Brett hat die Zeilen $1, \ldots, 8$ und die Spalten $A, \ldots, H$. Wie viele Felder hat es, also $|\{1, \ldots, 8\} \times \{A, \ldots, H\}|$?", 64,
       r"Jedes Feld ist ein Paar (Zeile, Spalte): $8 \cdot 8 = 64$ Paare.",
       tipps=["Zähle erst die Zeilen, dann die Spalten.", "Jede Zeile hat so viele Felder wie es Spalten gibt.", r"$8 \cdot 8$"],
       rechenweg=r"""
:::rechnung
8 \cdot 8 = 64 || $|A \times B| = |A| \cdot |B|$
:::
""",
       typische_fehler=[(16, r"Du hast $8 + 8$ gerechnet. Für jede der $8$ Zeilen gibt es $8$ Spalten: Das ist ein Produkt."),
                        (8, r"Das ist die Anzahl der Zeilen allein. Jede Zeile hat $8$ Felder.")])

# ── Seite 2: Satz 2.29 bis 2.31 ──────────────────────────────────────────
k.erklaerung("Nachfolgerregel, Kürzungsregel, Produkte von Mengen (Satz 2.29 bis 2.31)", r"""
## Rechengesetze der Multiplikation

**Satz 2.29 (Nachfolgerregel).** $a \cdot (b + 1) = a \cdot \text{succ}(b) = a \cdot b + a$.
*Beweis:* $a \times \text{succ}(b) = (a \times b) \cup (a \times \{b\})$ ist eine disjunkte Vereinigung, und $|a \times \{b\}| = a$ (Satz 2.21).

**Satz 2.30 (Kürzungsregel).** Für $a \neq 0$ gilt $a \cdot b = a \cdot c \Rightarrow b = c$ (Übung).
**Satz 2.31.** Für endliche Mengen gilt $|A \times B| = |A| \cdot |B|$, denn Bijektionen $|A| \to A$, $|B| \to B$ liefern $|A| \times |B| \to A \times B$ (Satz 1.82).

:::rechnung Satz 2.29 und die Grenze von Satz 2.30
5 \cdot 4 + 5 = 25 || Satz 2.29: $5 \cdot \text{succ}(4) = 5 \cdot 4 + 5$
5 \cdot 5 = 25 || dasselbe, denn $\text{succ}(4) = 5$
0 \cdot 2 = 0 \cdot 7 || beide gleich $0$, aber $2 \neq 7$: Bei $a = 0$ darf man nicht kürzen
:::

:::alt Als Treppe aus Reihen
Hast du $b$ Reihen mit je $a$ Stühlen und stellst eine Reihe dazu, kommen genau $a$ Stühle dazu. Das ist $a \cdot b + a$.
:::
""")

k.ordnen(r"Ordne den Beweis der Nachfolgerregel (Satz 2.29): $a \cdot \text{succ}(b) = a \cdot b + a$.",
         [r"Die Mengen $a \times b$ und $a \times \{b\}$ sind disjunkt.",
          r"Wegen $\text{succ}(b) = b \cup \{b\}$ gilt $a \cdot \text{succ}(b) = |a \times \text{succ}(b)| = |(a \times b) \cup (a \times \{b\})|$.",
          r"Nach Satz 2.21 ist das $|a \times b| + |a \times \{b\}|$.",
          r"Wegen $|a \times \{b\}| = |a| = a$ ist das $a \cdot b + a$. $\square$"],
         r"Man zerlegt das Raster in das alte Raster $a \times b$ und die neue Zeile $a \times \{b\}$ und addiert.",
         ablenker=[r"Die Mengen $a \times b$ und $a \times \{b\}$ haben dieselben Elemente.",
                   r"Daraus folgt $a \cdot \text{succ}(b) = a \cdot b \cdot a$."],
         tipps=["Zerlege $a \\times \\text{succ}(b)$ in zwei Teile, die sich nicht überlappen.", "Welcher Satz zählt eine disjunkte Vereinigung?",
                r"Die neue Zeile $a \times \{b\}$ hat genau $a$ Elemente."])

k.wf(r"Für alle $a, b, c \in \mathbb{N}$ gilt: Aus $a \cdot b = a \cdot c$ folgt $b = c$.", False,
     r"Falsch. Satz 2.30 verlangt $a \neq 0$. Gegenbeispiel: $a = 0$, $b = 2$, $c = 7$: Es ist $0 \cdot 2 = 0 \cdot 7$, aber $2 \neq 7$.",
     tipps=["Welche Voraussetzung steht in Satz 2.30?", "Teste $a = 0$."])

# ── Seite 3: Satz 2.32, Produktzeichen ───────────────────────────────────
k.erklaerung("Distributivität und das Produktzeichen (Satz 2.32, Def. 2.33)", r"""
## Die Rechenregeln

**Satz 2.32.** Für alle $n, m, r \in \mathbb{N}$ gilt (Übung): $nm = mn$ (kommutativ), $(nm)r = n(mr)$ (assoziativ), $n(m + r) = nm + nr$ ([[distributiv|Distributivgesetz]]).
Es gilt „Punkt vor Strich“: $n + mr := n + (m \cdot r)$.

**Definition 2.33.** Für $a\colon \{n_0, \ldots, n\} \to Z$ mit einer Multiplikation auf $Z$ ist
$$\prod_{i=n_0}^{n} a(i) := a(n_0) \cdot a(n_0 + 1) \cdot \ldots \cdot a(n).$$
Die Sätze 2.34 und 2.35 (Summe gleicher Summanden und $\sum 2i = n(n+1)$) hast du im Kapitel „Natürliche Zahlen und vollständige Induktion“ per Induktion bewiesen.

:::rechnung Distributivität und Produkt
3 \cdot (4 + 5) = 3 \cdot 9 = 27 || links erst die Klammer
3 \cdot 4 + 3 \cdot 5 = 12 + 15 = 27 || rechts ausmultipliziert: gleich
\prod_{i=1}^{4} i = 1 \cdot 2 \cdot 3 \cdot 4 = 24 || Produktzeichen: ein Faktor je $i$
:::

:::alt Mit zwei Rechtecken
Ein $3 \times 9$-Rechteck lässt sich in ein $3 \times 4$- und ein $3 \times 5$-Rechteck zerschneiden. Die Fläche bleibt gleich. Das ist das Distributivgesetz.
:::
""")

k.zahl(r"Berechne $\prod_{i=2}^{5} i$ nach Definition 2.33.", 120,
       r"Vier Faktoren für $i = 2, 3, 4, 5$: $2 \cdot 3 \cdot 4 \cdot 5 = 120$.",
       tipps=["Die untere Grenze ist $n_0 = 2$, nicht $1$.", r"Multipliziere $2, 3, 4, 5$.", r"$2 \cdot 3 = 6$, $6 \cdot 4 = 24$, $24 \cdot 5 = 120$"],
       rechenweg=r"""
:::rechnung
2 \cdot 3 \cdot 4 \cdot 5 = 6 \cdot 4 \cdot 5 || ersten beiden Faktoren
6 \cdot 4 \cdot 5 = 120 || weiter
:::
""",
       typische_fehler=[(60, r"Du hast die $5$ vergessen. Die obere Grenze gehört dazu."),
                        (14, r"Du hast addiert ($2 + 3 + 4 + 5$). Das Produktzeichen $\prod$ multipliziert.")])

# ── Seite 4: Division ────────────────────────────────────────────────────
k.erklaerung("Teilbarkeit und Division (Def. 2.36, 2.37, Beob. 2.38)", r"""
## Nur wenn es aufgeht

Die Abbildung $q \mapsto b \cdot q$ trifft nicht jede Zahl: $3$ liegt nicht im Bild von $q \mapsto 2q$. Die Division ist darum nur eine partielle Umkehrung.

**Definition 2.36.** $b \mid a :\iff \exists q \in \mathbb{N} : a = b \cdot q$ („$a$ ist durch $b$ teilbar“, [[b teilt a|Teiler]]).
**Definition 2.37.** Für $b \neq 0$ mit $b \mid a$ ist $\frac{a}{b} := q$ mit dem eindeutigen $q$ aus $a = b \cdot q$ (Satz 2.30).
**Beobachtung 2.38.** $b \cdot q = a \iff \frac{a}{b} = q$ (für $b \neq 0$ und $b \mid a$). Insbesondere $a/1 = a$.

:::rechnung Beispiele
12 = 3 \cdot 4 || also $3 \mid 12$ und $\frac{12}{3} = 4$
13 = 3 \cdot q \text{ hat kein } q \in \mathbb{N} || $3 \nmid 13$: die Division $13/3$ existiert nicht
0 = 5 \cdot 0 || $5 \mid 0$ gilt, aber $0 \mid 5$ gilt nicht, denn $5 = 0 \cdot q$ ist unmöglich
:::

:::achtung Durch $0$ teilen
$0 \mid 0$ gilt nach Definition 2.36, denn $0 = 0 \cdot q$. Die Division $a/b$ ist aber nur für $b \neq 0$ erklärt, denn $q$ wäre nicht eindeutig.
:::

:::alt Als gleiche Päckchen
$b \mid a$ heißt: Du kannst $a$ Murmeln ohne Rest in Päckchen zu je $b$ Stück verteilen. Der Quotient $a / b$ ist die Anzahl der Päckchen.
:::
""")

k.mehrfach("Welche dieser Aussagen gelten nach Definition 2.36?",
           [r"$5 \mid 0$", r"$0 \mid 0$", r"$1 \mid 7$", r"$7 \mid 7$"],
           [r"$0 \mid 5$", r"$3 \mid 10$"],
           r"$b \mid a$ heißt $a = b \cdot q$. $0 = 5 \cdot 0$, $0 = 0 \cdot 5$, $7 = 1 \cdot 7$, $7 = 7 \cdot 1$. Dagegen hat $5 = 0 \cdot q$ keine Lösung und $10 = 3 \cdot q$ auch nicht.",
           tipps=[r"Suche zu jeder Aussage ein $q \in \mathbb{N}$ mit $a = b \cdot q$.", r"Bei $0 \mid 5$: Was ergibt $0 \cdot q$?", r"$3 \cdot 3 = 9$, $3 \cdot 4 = 12$."],
           fehler={r"$0 \mid 5$": r"$0 \cdot q = 0 \neq 5$ für jedes $q$: $0$ teilt nur die $0$.",
                   r"$3 \mid 10$": r"$10 = 3 \cdot 3 + 1$, es bleibt Rest $1$: $3 \nmid 10$."})

# ── Seite 5: Satz 2.39 ───────────────────────────────────────────────────
k.erklaerung("Gleich große Klassen zählen (Satz 2.39, Beispiel 2.40)", r"""
## Division zählt Klassen

**Satz 2.39.** Sei $M$ endlich, $\sim$ eine Äquivalenzrelation auf $M$, und alle [[Äquivalenzklassen|Äquivalenzklasse]] haben dieselbe Größe $b \neq 0$.
Dann gilt $b \mid |M|$ und $|M/{\sim}| = \frac{|M|}{b}$.

*Beweis:* Die Klassen zerlegen $M$ in $|M/{\sim}|$ disjunkte Mengen mit je $b$ Elementen. Nach Satz 2.21 ist $|M| = b + \cdots + b = b \cdot |M/{\sim}|$.

**Beispiel 2.40.** Ein Kartenblatt hat $52$ Karten (Rang mal Farbe). Gleicher Rang ist eine Äquivalenzrelation, jede Klasse hat $4$ Karten.

:::rechnung Karten nach Rang
52 = 13 \cdot 4 || Ränge $2, \ldots, 10, B, D, K, A$ sind $13$ Stück, mal $4$ Farben
\frac{52}{4} = 13 || Satz 2.39: $|M/{\sim}| = 13$ Klassen
\frac{52}{13} = 4 || nach Farbe: $13$ Karten pro Klasse, also $4$ Klassen
:::

:::alt Mit Sitzgruppen
$52$ Personen in Vierergruppen: $52 : 4 = 13$ Gruppen. Das geht nur auf, wenn alle Gruppen gleich groß sind.
:::
""")

k.zahl(r"Ein Kartenblatt hat $52$ Karten. Zwei Karten sind äquivalent, wenn sie dieselbe **Farbe** haben (♣, ♠, ♡, ♢). Wie viele Äquivalenzklassen gibt es?", 4,
       r"Jede Klasse hat $13$ Karten (ein Rang je Karte), also $|M/{\sim}| = \frac{52}{13} = 4$ (Satz 2.39).",
       tipps=["Wie viele Karten hat jede Klasse?", r"Satz 2.39: $|M/{\sim}| = |M| : b$.", r"$52 : 13$"],
       rechenweg=r"""
:::rechnung
\frac{52}{13} = 4 || $|M| = 52$ und Klassengröße $b = 13$
:::
""",
       typische_fehler=[(13, "Das ist die Anzahl der Klassen bei gleichem **Rang**. Bei gleicher Farbe hat jede Klasse $13$ Karten."),
                        (52, "Das ist $|M|$. Gesucht ist die Anzahl der Klassen.")])

# ── Seite 6: Satz 2.41 ───────────────────────────────────────────────────
k.erklaerung("Division mit Rest (Satz 2.41)", r"""
## Was übrig bleibt

Teilt $b$ die Zahl $a$ nicht, kannst du trotzdem zerlegen:

**Satz 2.41.** Für alle $a, b \in \mathbb{N}$ mit $b \neq 0$ gibt es **eindeutig bestimmte** $q, r \in \mathbb{N}$ mit
$$a = q \cdot b + r \quad \text{und} \quad r < b.$$

Idee: $q$ ist das größte $k$ mit $k \cdot b \le a$. Dann bleibt $r = a - q \cdot b$, und $r < b$, sonst passte noch ein $b$ hinein.

:::rechnung $a = 47$, $b = 9$
Q = \{k \mid 9k \le 47\} = \{0, 1, 2, 3, 4, 5\} || $5 \cdot 9 = 45 \le 47$, aber $6 \cdot 9 = 54 > 47$
\text{also } q = 5 || das Maximum von $Q$
47 - 5 \cdot 9 = 2 || $r = a - q \cdot b$
47 = 5 \cdot 9 + 2 || mit $2 < 9$ ✓
:::

:::alt Mit Bussen
$47$ Personen, jeder Bus fasst $9$. Du füllst $5$ Busse ganz, im sechsten sitzen $2$. Ein sechster **voller** Bus ginge nicht, darum ist der Rest kleiner als $9$.
:::
""")

k.luecke(r"Zerlege $47 = \luecke \cdot 9 + \luecke$ mit Rest kleiner als $9$ (Satz 2.41).",
         r"47 = \luecke \cdot 9 + \luecke",
         [[5], [2]],
         r"$5 \cdot 9 = 45 \le 47 < 54 = 6 \cdot 9$, also $q = 5$ und $r = 47 - 45 = 2$.",
         tipps=[r"Welches ist das größte $q$ mit $q \cdot 9 \le 47$?", r"$5 \cdot 9 = 45$", r"$r = 47 - 45$"],
         rechenweg=r"""
:::rechnung
5 \cdot 9 + 2 = 47 || Probe
:::
""",
         typische_fehler=[([4, 11], r"Rechnerisch stimmt $4 \cdot 9 + 11 = 47$, aber der Rest $11$ ist nicht kleiner als $9$. Es passt noch ein $9$ hinein."),
                          ([6, -7], r"$6 \cdot 9 = 54 > 47$: Der Rest darf nicht negativ sein, also ist $q = 6$ zu groß."),
                          ([2, 5], r"Du hast Quotient und Rest vertauscht: $2 \cdot 9 + 5 = 23 \neq 47$.")])

# ── Seite 7: Beweis ──────────────────────────────────────────────────────
k.erklaerung("Beweis von Satz 2.41: Existenz", r"""
## Das größte $k$ finden

Der Beweis nutzt Satz 2.5, Satz 2.15 und die Subtraktion.

1. $Q := \{k \in \mathbb{N} \mid k \cdot b \le a\}$ ist nichtleer, denn $0 \cdot b = 0 \le a$.
2. $Q$ ist endlich: Wegen $b \neq 0$ ist $b = 1 + c$ (Satz 2.5), also $k \le k \cdot b \le a$ für $k \in Q$.
3. Daher hat $Q$ ein Maximum $q$ (Satz 2.15).
4. $r := a - q \cdot b$ erfüllt $a = q \cdot b + r$.
5. Wäre $r \ge b$, so $r = b + s$ und $a = (q+1) \cdot b + s$: Dann läge $q + 1$ in $Q$. Das widerspricht der Maximalität.

:::rechnung Der Widerspruchsschritt an $a = 47$, $b = 9$, $q = 4$
4 \cdot 9 = 36 \le 47 || $4 \in Q$, aber nicht das Maximum
47 - 36 = 11 \ge 9 || der Rest $11$ ist zu groß: ein weiteres $9$ passt noch hinein
5 \cdot 9 = 45 \le 47 || also liegt $q + 1 = 5$ in $Q$: $q = 4$ war nicht maximal
:::

:::alt Mit Schritten auf einer Treppe
Du gehst mit Schritten der Länge $b$ von $0$ aus so weit wie möglich, ohne $a$ zu überschreiten. Die letzte Stelle ist $q \cdot b$. Bis $a$ fehlt noch ein Stück, das kürzer als ein Schritt ist: der Rest.
:::
""")

k.ordnen(r"Ordne den Existenzbeweis von Satz 2.41 (Division mit Rest).",
         [r"Setze $Q := \{k \in \mathbb{N} \mid k \cdot b \le a\}$. Es gilt $0 \in Q$, also $Q \neq \emptyset$.",
          r"Wegen $b \neq 0$ ist $b = 1 + c$ (Satz 2.5), und für $k \in Q$ gilt $k \le k \cdot b \le a$. Also ist $Q$ endlich.",
          r"Nach Satz 2.15 besitzt $Q$ ein Maximum $q := \max Q$.",
          r"Wegen $q \cdot b \le a$ existiert $r := a - q \cdot b$, und es gilt $a = q \cdot b + r$.",
          r"Wäre $r \ge b$, so wäre $r = b + s$ und $a = (q + 1) \cdot b + s$, also $q + 1 \in Q$ im Widerspruch zur Maximalität von $q$. Daher ist $r < b$. $\square$"],
         r"Aus der Nichtleere und Endlichkeit von $Q$ folgt ein Maximum. Das Maximum liefert Quotient und Rest, und die Maximalität zwingt $r < b$.",
         ablenker=[r"Setze $Q := \{k \in \mathbb{N} \mid k \cdot b \ge a\}$. Diese Menge hat ein Maximum.",
                   r"Setze $q := a \operatorname{div} b$ und $r := a \bmod b$."],
         tipps=["Wähle eine Menge, die eine endliche Obergrenze hat.", "Der Beweis darf nicht mit „div“ und „mod“ beginnen: Die sind erst durch den Satz definiert.",
                "Am Ende steht ein Widerspruch zur Maximalität."])

k.mc(r"Warum verlangt Satz 2.41 die Bedingung $r < b$?",
     [r"Ohne sie wären $q$ und $r$ nicht eindeutig: $47 = 4 \cdot 9 + 11 = 5 \cdot 9 + 2$",
      r"Weil sonst $b$ durch $0$ geteilt würde",
      r"Weil $r$ sonst nicht in $\mathbb{N}$ läge",
      r"Weil sonst $q = 0$ wäre"],
     r"Ohne $r < b$ gäbe es mehrere Zerlegungen: Mit jedem kleineren $q$ wächst $r$ um $b$. Die Bedingung wählt genau eine aus.",
     tipps=[r"Zerlege $47 = q \cdot 9 + r$ mit verschiedenen $q$.", r"Probiere $q = 4$ und $q = 5$.", "Was passiert mit dem Rest, wenn du den Quotienten um eins verkleinerst?"],
     fehler={r"Weil sonst $b$ durch $0$ geteilt würde": r"Dafür ist die Bedingung $b \neq 0$ zuständig, nicht $r < b$.",
             r"Weil $r$ sonst nicht in $\mathbb{N}$ läge": r"$11 \in \mathbb{N}$: Die Zerlegung $47 = 4 \cdot 9 + 11$ liegt in $\mathbb{N}$, ist aber nicht die gesuchte.",
             r"Weil sonst $q = 0$ wäre": r"Für $a = 47$ und $b = 9$ ist $q = 0$ möglich ($47 = 0 \cdot 9 + 47$), aber das ist nicht das Problem: Es wären mehrere $q$ möglich."})

# ── Seite 8: div und mod ─────────────────────────────────────────────────
k.erklaerung("div und mod (Def. 2.42, Beobachtung 2.43)", r"""
## Quotient und Rest als Abbildungen

**Definition 2.42.** Für $a, b \in \mathbb{N}$, $b \neq 0$ und $q, r$ aus Satz 2.41 sind
$\operatorname{div}\colon \mathbb{N} \times (\mathbb{N} \setminus \{0\}) \to \mathbb{N},\ (a, b) \mapsto q$ und $\bmod\colon (a, b) \mapsto r$.
Man schreibt $a \operatorname{div} b$ und $a \bmod b$.

**Beobachtung 2.43.** $a = (a \operatorname{div} b) \cdot b + (a \bmod b)$. Außerdem: $b \mid a \iff a \bmod b = 0$, und dann ist $a \operatorname{div} b = a / b$.

:::visual modulo_uhr
{"n": 9, "start": 47, "interaktiv": true,
 "unterschrift": "Auf einer Uhr mit $9$ Plätzen landet $47$ bei $2$: $47 \\bmod 9 = 2$. Regler ändern $n$ und $a$."}
:::

:::rechnung $47$ durch $9$ und $54$ durch $9$
47 = 5 \cdot 9 + 2 || also $47 \operatorname{div} 9 = 5$ und $47 \bmod 9 = 2$
54 = 6 \cdot 9 + 0 || Rest $0$: also $9 \mid 54$, und $54 \operatorname{div} 9 = 6 = 54 / 9$
:::

:::alt In Python
`47 // 9` ist $5$, `47 % 9` ist $2$. Für natürliche Zahlen bedeuten `//` und `%` genau $\operatorname{div}$ und $\bmod$. Und `a % b == 0` ist die Teilbarkeitsprüfung.
:::
""")

k.mehrfach("Gegeben ist $a = 100$ und $b = 7$. Welche Aussagen stimmen?",
           [r"$100 \operatorname{div} 7 = 14$", r"$100 \bmod 7 = 2$", r"$7 \nmid 100$"],
           [r"$100 \bmod 7 = 14$", r"$7 \mid 100$"],
           r"$100 = 14 \cdot 7 + 2$ mit $2 < 7$. Also $100 \operatorname{div} 7 = 14$ und $100 \bmod 7 = 2 \neq 0$, und damit teilt $7$ die $100$ nicht.",
           tipps=[r"Finde $q$ mit $q \cdot 7 \le 100 < (q + 1) \cdot 7$.", r"$14 \cdot 7 = 98$", "Der Rest ist die Differenz zu $100$."],
           fehler={r"$100 \bmod 7 = 14$": r"$14$ ist der Quotient $100 \operatorname{div} 7$, nicht der Rest. Der Rest ist stets kleiner als $7$.",
                   r"$7 \mid 100$": r"$100 \bmod 7 = 2 \neq 0$, also teilt $7$ die $100$ nicht (Beob. 2.43)."})

# ── Seite 9: Satz 2.44 ───────────────────────────────────────────────────
k.erklaerung("Rechnen mit Resten (Satz 2.44, Beispiel 2.45)", r"""
## Zwischenergebnisse klein halten

**Satz 2.44.** Für alle $a, b, n \in \mathbb{N}$ mit $n \neq 0$ gilt
$$(a + b) \bmod n = ((a \bmod n) + (b \bmod n)) \bmod n,$$
$$(a \cdot b) \bmod n = ((a \bmod n) \cdot (b \bmod n)) \bmod n.$$

Beweis: Übung (siehe Aufgabe unten). Du darfst also jede Zahl im Rechenausdruck durch ihren Rest ersetzen.

**Beispiel 2.45.** Rest von $(9 + 6) \cdot 23 + 705$ bei Division durch $7$:

:::rechnung Reste statt großer Zahlen
9 \bmod 7 = 2, \quad 6 \bmod 7 = 6 || $9 = 1 \cdot 7 + 2$
(2 + 6) \bmod 7 = 8 \bmod 7 = 1 || Summe in der Klammer, dann Rest
23 \bmod 7 = 2, \quad 705 \bmod 7 = 5 || $23 = 3 \cdot 7 + 2$ und $705 = 100 \cdot 7 + 5$
(1 \cdot 2 + 5) \bmod 7 = 7 \bmod 7 = 0 || also teilt $7$ die Zahl
(9 + 6) \cdot 23 + 705 = 1050 = 7 \cdot 150 || Kontrolle ohne Reste
:::

:::achtung Der letzte Rest nicht vergessen
Nach dem Ersetzen durch Reste musst du am Ende **noch einmal** den Rest nehmen: $(a \bmod n) + (b \bmod n)$ kann größer als $n$ sein.
:::

:::alt Als Uhrzeit
Es ist 10 Uhr. Was zeigt die Uhr in 17 Stunden? Du rechnest nicht $10 + 17 = 27$, sondern drehst nur: $27 \bmod 12 = 3$. Ob du erst addierst und dann reduzierst oder umgekehrt, ändert nichts.
:::
""")

k.zahl(r"Berechne $(23 \cdot 19) \bmod 7$ mit Satz 2.44, indem du zuerst die Faktoren reduzierst.", 3,
       r"$23 \bmod 7 = 2$ und $19 \bmod 7 = 5$. Dann $(2 \cdot 5) \bmod 7 = 10 \bmod 7 = 3$. Kontrolle: $23 \cdot 19 = 437 = 62 \cdot 7 + 3$.",
       tipps=[r"Ersetze $23$ und $19$ durch ihre Reste modulo $7$.", r"$23 = 3 \cdot 7 + 2$ und $19 = 2 \cdot 7 + 5$", r"$2 \cdot 5 = 10$"],
       rechenweg=r"""
:::rechnung
23 = 3 \cdot 7 + 2 || Rest $2$
19 = 2 \cdot 7 + 5 || Rest $5$
2 \cdot 5 = 10 = 1 \cdot 7 + 3 || Rest $3$
23 \cdot 19 = 437 = 62 \cdot 7 + 3 || Kontrolle
:::
""",
       typische_fehler=[(10, r"Du hast vergessen, den Rest von $2 \cdot 5 = 10$ nochmal zu nehmen: $10 \bmod 7 = 3$."),
                        (2, r"Du hast nur einen Faktor reduziert oder die Reste addiert statt multipliziert? $23 \bmod 7 = 2$ ist erst der erste Rest.")])

k.wf(r"Es gilt $(a + b) \bmod n = (a \bmod n) + (b \bmod n)$ für alle $a, b \in \mathbb{N}$, $n \neq 0$.", False,
     r"Falsch. Die Summe der Reste kann $\ge n$ sein. Gegenbeispiel $a = 5$, $b = 6$, $n = 7$: $11 \bmod 7 = 4$, aber $5 + 6 = 11$. Richtig ist $((a \bmod n) + (b \bmod n)) \bmod n$.",
     tipps=["Teste $a = 5$, $b = 6$, $n = 7$."])


# ── Praxis ────────────────────────────────────────────────────────────────
def rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def division_mit_rest(rng):
    b = rng.randint(4, 13)
    a = rng.randint(3 * b, 12 * b + b - 1)
    q, r = divmod(a, b)
    if r == 0:
        a += rng.randint(1, b - 1)
        q, r = divmod(a, b)
    loesung = [[q], [r]]
    fehler = [([q - 1, r + b], f"Rechnerisch stimmt ${q - 1} \\cdot {b} + {r + b} = {a}$, aber der Rest ${r + b}$ ist nicht kleiner als ${b}$. Es passt noch ein ${b}$ hinein."),
              ([q + 1, r - b], "Der Rest darf nicht negativ sein. Der Quotient ist um eins zu groß."),
              ([r, q], "Quotient und Rest sind vertauscht."),
              ([q, a - q * b + 1], f"Die Probe stimmt nicht: ${q} \\cdot {b} + {a - q * b + 1} \\neq {a}$.")]
    return {
        "frage": f"Bestimme $q = {a} \\operatorname{{div}} {b}$ und $r = {a} \\bmod {b}$ nach Satz 2.41.",
        "formel": f"{a} = \\luecke \\cdot {b} + \\luecke",
        "antworten": loesung,
        "tipps": [f"Suche das größte $q$ mit $q \\cdot {b} \\le {a}$.", f"${q} \\cdot {b} = {q * b}$ und ${q + 1} \\cdot {b} = {(q + 1) * b}$.",
                  f"Der Rest ist ${a} - {q * b}$."],
        "rechenweg": rechnung([(f"{q} \\cdot {b} + {r} = {a}", f"Probe, und ${r} < {b}$ ✓")]),
        "erklaerung": f"$q$ ist die größte Zahl mit $q \\cdot {b} \\le {a}$. Der Rest ist ${a} - q \\cdot {b} = {r}$ und kleiner als ${b}$.",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


def rest_rechnen(rng):
    n = rng.randint(5, 13)
    a, b = rng.randint(n + 2, 60), rng.randint(n + 2, 60)
    c, d = rng.randint(n + 2, 60), rng.randint(n + 2, 600)
    wert = ((a + b) * c + d)
    loesung = wert % n
    ra, rb, rc, rd = a % n, b % n, c % n, d % n
    s1 = (ra + rb) % n
    s2 = (s1 * rc) % n
    assert (s2 + rd) % n == loesung
    fehler = [((ra + rb) * rc + rd, "Du hast am Ende **nicht** noch einmal den Rest genommen. Die Summe der Reste kann größer als $n$ sein."),
              (wert // n, "Das ist der Quotient `div`, nicht der Rest."),
              ((s1 * rc + rd) % n if False else (ra + rb + rc + rd) % n, "Du hast die Reste addiert statt zu multiplizieren. Der Ausdruck enthält ein Produkt.")]
    return {
        "frage": f"Bestimme den Rest von $({a} + {b}) \\cdot {c} + {d}$ bei Division durch ${n}$ mit Satz 2.44, ohne die ganze Zahl auszurechnen.",
        "loesung": loesung,
        "tipps": [f"Ersetze jede Zahl durch ihren Rest modulo ${n}$: ${a} \\bmod {n} = {ra}$.", f"Rechne ${ra} + {rb}$, dann $\\bmod {n}$, dann mal ${rc}$, dann $\\bmod {n}$.",
                  f"Addiere zum Schluss ${rd}$ und nimm noch einmal den Rest."],
        "rechenweg": rechnung([(f"({ra} + {rb}) \\bmod {n} = {s1}", f"Reste der Summanden in der Klammer: ${a} \\bmod {n} = {ra}$, ${b} \\bmod {n} = {rb}$"),
                               (f"{s1} \\cdot {rc} \\bmod {n} = {s2}", f"mal ${c} \\bmod {n} = {rc}$ und Rest"),
                               (f"({s2} + {rd}) \\bmod {n} = {loesung}", f"plus ${d} \\bmod {n} = {rd}$ und Rest: Ergebnis")]),
        "erklaerung": "Satz 2.44: Du darfst jede Teilrechnung sofort durch ihren Rest ersetzen. Am Ende nimmst du den Rest noch einmal.",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


def teilbarkeit_pruefen(rng):
    b = rng.randint(3, 9)
    zahlen = sorted(rng.sample(range(b + 1, 90), 5))
    if not any(z % b == 0 for z in zahlen):
        zahlen[rng.randrange(5)] = b * rng.randint(2, 10)
        zahlen = sorted(set(zahlen))
    while len(zahlen) < 5:
        zahlen.append(rng.randint(b + 1, 90))
        zahlen = sorted(set(zahlen))
    richtig = [f"${z}$" for z in zahlen if z % b == 0]
    falsch = [f"${z}$" for z in zahlen if z % b != 0]
    fehler = {f"${z}$": f"${z} = {z // b} \\cdot {b} + {z % b}$: Der Rest ${z % b}$ ist nicht $0$, also gilt ${b} \\nmid {z}$." for z in zahlen if z % b != 0}
    zeilen = [(f"{z} = {z // b} \\cdot {b} + {z % b}", f"Rest ${z % b}$: " + (f"${b} \\mid {z}$" if z % b == 0 else f"${b} \\nmid {z}$")) for z in zahlen]
    return {
        "frage": f"Welche der folgenden Zahlen sind durch ${b}$ teilbar (Def. 2.36, Beobachtung 2.43)?",
        "richtig": richtig, "falsch": falsch, "fehler": fehler,
        "tipps": [f"${b} \\mid a$ gilt genau dann, wenn $a \\bmod {b} = 0$.", f"Dividiere jede Zahl mit Rest durch ${b}$.", "Eine Zahl ist teilbar, wenn kein Rest bleibt."],
        "rechenweg": rechnung(zeilen),
        "erklaerung": "Nach Beobachtung 2.43 gilt $b \\mid a \\iff a \\bmod b = 0$.",
    }


def klassen_zaehlen(rng):
    r, f = rng.randint(5, 13), rng.randint(2, 5)
    nach_rang = rng.random() < 0.5
    gesamt = r * f
    if nach_rang:
        b, loesung, kriterium = f, r, "denselben **Rang**"
    else:
        b, loesung, kriterium = r, f, "dieselbe **Farbe**"
    fehler = [(gesamt, "Das ist $|M|$, die Anzahl aller Karten. Gesucht ist die Anzahl der Klassen."),
              (b, "Das ist die Größe **einer** Klasse $b$, nicht die Anzahl der Klassen."),
              (gesamt - b if gesamt - b != loesung else gesamt + 1, "Du hast subtrahiert. Gesucht ist ein Quotient (Satz 2.39).")]
    return {
        "frage": f"Ein Kartenspiel hat {r} Ränge und {f} Farben, jede Kombination kommt genau einmal vor ($|M| = {gesamt}$). Zwei Karten sind äquivalent, wenn sie {kriterium} haben. "
                 "Wie viele Äquivalenzklassen hat $M/{\\sim}$?",
        "loesung": loesung,
        "tipps": [f"Wie viele Karten enthält eine Klasse? Alle Klassen sind gleich groß: $b = {b}$.", "Satz 2.39: $|M/{\\sim}| = |M| / b$.",
                  f"Rechne ${gesamt} : {b}$."],
        "rechenweg": rechnung([(f"\\frac{{{gesamt}}}{{{b}}} = {loesung}", f"$|M| = {r} \\cdot {f} = {gesamt}$ und Klassengröße $b = {b}$: Satz 2.39")]),
        "erklaerung": "Satz 2.39: Sind alle Klassen gleich groß $b$, ist die Anzahl der Klassen $|M| / b$.",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


k.praxis()

k.generator(division_mit_rest, typ="luecke", titel="Division mit Rest (Satz 2.41)")
k.generator(rest_rechnen, typ="zahl", titel="Rechnen mit Resten (Satz 2.44)")
k.generator(teilbarkeit_pruefen, typ="mehrfach", titel="Teilbarkeit prüfen")
k.generator(klassen_zaehlen, typ="zahl", titel="Äquivalenzklassen zählen (Satz 2.39)")

k.rechenweg_aufgabe(r"""
## Quiz-Stil: Rest bestimmen wie in Beispiel 2.45

Bestimme den Rest von $(17 + 9) \cdot 31 + 502$ bei Division durch $8$, ohne die Zahl auszurechnen.
""",
    [{"typ": "zahl", "frage": r"Wie lautet $(17 + 9) \bmod 8$?", "loesung": 2,
      "tipps": [r"$17 \bmod 8 = 1$ und $9 \bmod 8 = 1$.", r"$1 + 1$"],
      "rechenweg": r"$17 = 2 \cdot 8 + 1$, $9 = 1 \cdot 8 + 1$, also $(1 + 1) \bmod 8 = 2$.",
      "erklaerung": r"Die Klammer hat den Rest $2$ (denn $26 = 3 \cdot 8 + 2$).",
      "typische_fehler": [(26, r"Das ist die Summe selbst, nicht ihr Rest: $26 = 3 \cdot 8 + 2$.")]},
     {"typ": "zahl", "frage": r"Wie lautet $((17 + 9) \cdot 31) \bmod 8$?", "loesung": 6,
      "tipps": [r"Ersetze $(17 + 9)$ durch $2$ und $31$ durch $31 \bmod 8 = 7$.", r"$2 \cdot 7 = 14$, dann $\bmod 8$."],
      "rechenweg": r"$31 = 3 \cdot 8 + 7$, also $(2 \cdot 7) \bmod 8 = 14 \bmod 8 = 6$.",
      "erklaerung": r"Nach Satz 2.44 genügen die Reste $2$ und $7$: $14 = 1 \cdot 8 + 6$.",
      "typische_fehler": [(14, r"Du hast den Rest von $2 \cdot 7 = 14$ nicht nochmal genommen: $14 \bmod 8 = 6$.")]},
     {"typ": "zahl", "frage": r"Wie lautet der gesuchte Rest $((17 + 9) \cdot 31 + 502) \bmod 8$?", "loesung": 4,
      "tipps": [r"$502 = 62 \cdot 8 + 6$", r"$(6 + 6) \bmod 8$"],
      "rechenweg": r"$(6 + 6) \bmod 8 = 12 \bmod 8 = 4$.",
      "erklaerung": r"Kontrolle: $(17 + 9) \cdot 31 + 502 = 806 + 502 = 1308 = 163 \cdot 8 + 4$.",
      "typische_fehler": [(12, r"Du hast den letzten Rest vergessen: $12 \bmod 8 = 4$."),
                          (0, r"$8$ teilt $1308$ nicht: $1308 = 163 \cdot 8 + 4$.")]}],
    r"Der Rest ist $4$. Insbesondere ist die Zahl nicht durch $8$ teilbar (Beobachtung 2.43).",
    uebungsblatt=True,
    tipps=["Reduziere jede Zahl sofort modulo $8$.", "Nach jeder Rechenoperation darfst du wieder den Rest nehmen.", "Am Ende noch einmal den Rest nehmen."],
    rechenweg=r"""
:::rechnung
(17 + 9) \cdot 31 + 502 = 1308 || Kontrolle ohne Reste
1308 = 163 \cdot 8 + 4 || der Rest ist $4$
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Rechnen mit Resten und Kürzungsregel

1. Beweisen Sie Satz 2.44 für die Summe: $(a + b) \bmod n = ((a \bmod n) + (b \bmod n)) \bmod n$ für $n \neq 0$. Benutzen Sie die Eindeutigkeit in Satz 2.41.
2. Beweisen Sie Satz 2.30 (Kürzungsregel) per Induktion über $b$: Für $a \neq 0$ folgt aus $a \cdot b = a \cdot c$ schon $b = c$.
   Sie dürfen Satz 2.29, $a \cdot 0 = 0$ und die Injektivität von $\text{succ}$ benutzen.
""",
    r"""
**1.** Schreibe $a = q_1 n + r_1$ und $b = q_2 n + r_2$ mit $r_1 = a \bmod n$, $r_2 = b \bmod n$ (Satz 2.41). Dann ist $a + b = (q_1 + q_2) n + (r_1 + r_2)$.
Dividiere $r_1 + r_2 = q_3 n + r_3$ mit $r_3 < n$ (Satz 2.41). Dann ist $a + b = (q_1 + q_2 + q_3) n + r_3$ mit $r_3 < n$.
Nach der Eindeutigkeit in Satz 2.41 ist $r_3 = (a + b) \bmod n$. Andererseits ist $r_3 = (r_1 + r_2) \bmod n = ((a \bmod n) + (b \bmod n)) \bmod n$. $\square$

**2. Anfang** ($b = 0$): Aus $a \cdot 0 = a \cdot c$ folgt $a \cdot c = 0$. Wäre $c \neq 0$, so $c = \text{succ}(d)$ (Satz 2.5) und $a \cdot c = a \cdot d + a \ge a > 0$: Widerspruch. Also $c = 0 = b$.
**Annahme:** Für ein $b$ gelte: $a \cdot b = a \cdot c \Rightarrow b = c$ für alle $c$.
**Schritt:** Sei $a \cdot \text{succ}(b) = a \cdot c$. Wäre $c = 0$, so $a \cdot \text{succ}(b) = 0$, aber $a \cdot \text{succ}(b) = a \cdot b + a \ge a > 0$: Widerspruch. Also $c = \text{succ}(d)$, und mit Satz 2.29 gilt $a \cdot b + a = a \cdot d + a$. Die Kürzungsregel der Addition (Satz 2.20) liefert $a \cdot b = a \cdot d$, nach der Annahme $b = d$, also $\text{succ}(b) = \text{succ}(d) = c$. $\square$
""",
    ["In 1.: $a$ und $b$ jeweils mit Quotient und Rest nach Satz 2.41 geschrieben",
     "In 1.: $a + b$ in der Form $(\\ldots) \\cdot n + r_3$ mit $r_3 < n$ gebracht",
     "In 1.: Die Eindeutigkeit aus Satz 2.41 zum Schluss ausdrücklich benutzt",
     "In 2.: Den Anfang $b = 0$ mit $c \\neq 0$ zum Widerspruch geführt",
     "In 2.: Im Schritt Satz 2.29, die Kürzungsregel der Addition und die Annahme benutzt"],
    "Satz 2.44 folgt aus der **Eindeutigkeit** der Division mit Rest: Hat eine Zahl zwei Darstellungen $q n + r$ mit $r < n$, sind sie gleich. Die Kürzungsregel der Multiplikation reduziert sich auf die der Addition.",
    uebungsblatt=True,
    tipps=["Bei 1. brauchst du die Division mit Rest zweimal: für $a$, $b$ und für $r_1 + r_2$.", "Bei 2. gibt es zwei Fälle für $c$: $c = 0$ oder $c$ ist ein Nachfolger."])

k.zusammenfassung(r"""
## Multiplikation, Division, Division mit Rest (Skript Abschn. 2.5)

- **Produkt** (Def. 2.28): $a \cdot b := |a \times b|$. Nachfolgerregel $a \cdot \text{succ}(b) = a \cdot b + a$ (2.29). Kürzungsregel $a \cdot b = a \cdot c \Rightarrow b = c$ für $a \neq 0$ (2.30). $|A \times B| = |A| \cdot |B|$ (2.31).
- **Rechengesetze** (2.32): kommutativ, assoziativ, distributiv; Punkt vor Strich. **Produktzeichen** $\prod_{i=n_0}^{n} a(i)$ (2.33). $\sum_{i=1}^{n} a = a \cdot n$ (2.34), $\sum_{i=1}^{n} 2i = n(n+1)$ (2.35).
- **Teilbarkeit** (2.36): $b \mid a :\iff \exists q : a = b \cdot q$. **Division** (2.37): $a/b := q$, nur für $b \neq 0$ und $b \mid a$. $b \cdot q = a \iff a/b = q$ (2.38).
- **Satz 2.39:** Alle Klassen gleich groß $b$ $\Rightarrow$ $b \mid |M|$ und $|M/{\sim}| = |M| / b$. Beispiel: $52 / 4 = 13$ Ränge (Bsp. 2.40).
- **Division mit Rest** (2.41): $a = q \cdot b + r$, $r < b$, **eindeutig**. $a \operatorname{div} b := q$, $a \bmod b := r$ (2.42). $b \mid a \iff a \bmod b = 0$ (2.43).
- **Rechnen mit Resten** (2.44): $(a + b) \bmod n = ((a \bmod n) + (b \bmod n)) \bmod n$ und ebenso für $\cdot$. Beispiel 2.45: $((9 + 6) \cdot 23 + 705) \bmod 7 = 0$.

!! Nach dem Ersetzen durch Reste musst du am Ende **nochmal** den Rest nehmen. Durch $0$ teilt man nicht, und Kürzen geht nur bei $a \neq 0$.
""")
