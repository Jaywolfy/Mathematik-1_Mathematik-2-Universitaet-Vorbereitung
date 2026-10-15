# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 10: Endliche Mengen, Addition und Subtraktion
(Skript Disser WS 26/27, Abschn. 2.3 und 2.4, Def. 2.10 bis Satz 2.27)."""
from fractions import Fraction as F
from itertools import product

from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(
    slug="zaehlen",
    titel="Endliche Mengen, Addition und Subtraktion",
    beschreibung="Kardinalität über Bijektionen, Addition als Vereinigung, Summenzeichen, Subtraktion, |A ∪ B| = |A| + |B| − |A ∩ B|",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 2.3 und 2.4",
    icon="🔢")


# ── Python rechnet alles nach ──────────────────────────────────────────────
def mtex(s):
    return "\\emptyset" if not s else "\\{" + ", ".join(str(x) for x in sorted(s)) + "\\}"


def mtext(s):
    return "{" + "; ".join(str(x) for x in sorted(s)) + "}"


def zahl_als_menge(n):
    return set(range(n))


# Def. 2.17: a + b := |(a × {0}) ∪ (b × {1})|
def plus_mengen(a, b):
    return len({(x, 0) for x in zahl_als_menge(a)} | {(y, 1) for y in zahl_als_menge(b)})


assert all(plus_mengen(a, b) == a + b for a in range(15) for b in range(15))
assert zahl_als_menge(4) | zahl_als_menge(7) == zahl_als_menge(7)          # 4 ∪ 7 = 7: ohne Markierung gehen Elemente verloren
assert plus_mengen(4, 7) == 11
# Def. 2.10 / Satz 2.11 an einem Beispiel
_f = {0: "a", 1: "b", 2: "c"}
assert len(set(_f.values())) == 3 and set(_f) == zahl_als_menge(3)
# Satz 2.12: M ∪ {d}
assert len(set(_f.values()) | {"d"}) == 3 + 1
# Satz 2.15 / 2.16: Minimum und Maximum
_M = {7, 3, 9, 5}
assert (min(_M - {5}), max(_M - {5}), min(_M), max(_M)) == (3, 9, 3, 9)
assert min(n for n in range(100) if n * n > 50) == 8
# Satz 2.18 und 2.20
assert all((a + 1) + b == (a + b) + 1 for a in range(20) for b in range(20))
assert all(a + k_ != a + l_ or k_ == l_ for a in range(10) for k_ in range(10) for l_ in range(10))
# Satz 2.21, Satz 2.26, Satz 2.27
_A, _B = {1, 2, 3, 4, 5}, {4, 5, 6, 7}
assert len(_A | _B) == len(_A) + len(_B) - len(_A & _B) == 7
assert len({"a", "b", "c"} | {"x", "y"}) == 3 + 2
assert len(_A - {4, 5}) == len(_A) - 2 == 3
# Summenzeichen (Def. 2.23)
assert sum(i * i for i in range(2, 6)) == 54 and 4 + 9 + 16 + 25 == 54
assert sum(2 * i + 1 for i in range(3, 7)) == 40
# Beispiel Übungsblatt: 18 Python, 14 Java, 6 beides von 30
assert 18 + 14 - 6 == 26 and 30 - 26 == 4 and 26 - 6 == 20

k.lernziele([
    "Ich kann erklären, was „endlich“ und „$|M| = n$“ über eine Bijektion $n \\to M$ bedeutet und warum Umbenennen nichts ändert (Def. 2.10, Satz 2.11)",
    "Ich kenne die Sätze über endliche Mengen und das Minimum jeder nichtleeren Teilmenge von $\\mathbb{N}$ (Satz 2.12 bis 2.16)",
    "Ich verstehe die Addition als Zählen einer Vereinigung und rechne mit Summenzeichen (Def. 2.17, 2.23, Satz 2.18 bis 2.22)",
    "Ich verstehe die Subtraktion als partielle Umkehrung und wende $|A \\setminus B| = |A| - |B|$ sowie $|A \\cup B| = |A| + |B| - |A \\cap B|$ an (Def. 2.24, Satz 2.26, 2.27)",
])

k.warum(r"""
Wie viele Elemente hat ein Array, eine Datenbanktabelle, eine Menge von Nutzern, die zwei Merkmale erfüllen?
Das Skript führt Rechnen auf Zählen zurück. Wer Nutzer zählt, die „Premium“ **oder** „aktiv“ sind, muss
die doppelt gezählten abziehen: Satz 2.27 ist die Formel hinter jeder `UNION` oder `OR`-Abfrage. Die Bijektion
zwischen Menge und `{0, …, n-1}` ist die Indexierung von Arrays. Und die Aussage „jede nichtleere Menge natürlicher
Zahlen hat ein kleinstes Element“ (Satz 2.16) ist der Grund, warum jede Schleife „suche das kleinste $n$ mit …“ terminiert.
""")

# ── Seite 1: Def. 2.10 ──────────────────────────────────────────────────
k.erklaerung("Was heißt „n Elemente“? (Def. 2.10, Satz 2.11)", r"""
## Zählen ist eine Bijektion

:::analogie 🪑 Stühle und Gäste
Du willst wissen, ob so viele Gäste wie Stühle da sind. Du musst nicht zählen: Jeder Gast setzt sich auf einen Stuhl.
Bleibt kein Gast stehen und kein Stuhl frei, sind es gleich viele.
:::

**Definition 2.10.** Eine Menge $M$ heißt [[endlich|endliche Menge]], wenn es eine Bijektion $f\colon n \to M$ für ein $n \in \mathbb{N}$ gibt.
Dann heißt $|M| := n$ die [[Kardinalität]] von $M$. Es ist $|n| = n$, denn $n = \{0, \ldots, n-1\}$.

:::visual relation_graph
{"links": [0, 1, 2], "rechts": ["Ada", "Ben", "Cem"], "pfeile": [[0, "Ben"], [1, "Cem"], [2, "Ada"]],
 "namen": ["3", "M"], "zeige": ["bijektiv"],
 "unterschrift": "Eine Bijektion $3 \\to M$: Also ist $M$ endlich mit $|M| = 3$."}
:::

**Satz 2.11.** Ist $A$ endlich und $h\colon A \to B$ bijektiv, so ist $B$ endlich mit $|B| = |A|$. (Beweis: $h \circ f$ ist bijektiv nach Satz 1.82.)

:::alt Als Abzählreim
„Ene, mene, miste“: Du zeigst nacheinander auf ein Element und sagst „Eins, zwei, drei …“. Du ordnest jedem Element **genau eine** Zahl zu
und lässt keine aus. Das ist die Bijektion. Wie die Elemente heißen, ändert nichts an der Anzahl (Satz 2.11).
:::
""")

k.mehrfach("Welche dieser Mengen sind im Sinne von Definition 2.10 endlich?",
           [r"$\emptyset$ (mit $n = 0$)", r"$\{a, b, c\}$", r"die Menge $n$ selbst, für jedes $n \in \mathbb{N}$"],
           [r"$\mathbb{N}$", r"$\mathbb{N} \setminus \{0\}$"],
           r"Für $\emptyset$ ist die leere Abbildung $0 \to \emptyset$ bijektiv, $|\emptyset| = 0$. Für $n$ nimmt man $\mathrm{id}_n$. "
           r"Für $\mathbb{N}$ (und $\mathbb{N} \setminus \{0\}$) gibt es keine Bijektion von einem $n \in \mathbb{N}$ aus: Der Nachfolger $\text{succ}(n)$ von $n$ "
           r"hätte kein Bild, wenn die Elemente schon alle vergeben wären.",
           tipps=["Gibt es zu jeder dieser Mengen eine Bijektion $f\\colon n \\to M$ mit einem festen $n \\in \\mathbb{N}$?", r"Auch $n = 0$ ist erlaubt.",
                  r"$\mathbb{N}$ hört nie auf: Welches $n$ sollte passen?"],
           fehler={r"$\mathbb{N}$": r"$\mathbb{N}$ hat kein letztes Element, also gibt es kein $n \in \mathbb{N}$ mit einer Bijektion $n \to \mathbb{N}$.",
                   r"$\mathbb{N} \setminus \{0\}$": r"Ein Element weniger als $\mathbb{N}$ macht die Menge nicht endlich: Auch hier gibt es kein passendes $n$."})

# ── Seite 2: Satz 2.12, 2.13, 2.14 ───────────────────────────────────────
k.erklaerung("Elemente hinzufügen und weglassen (Satz 2.12 bis 2.14)", r"""
## Endlich bleibt endlich

**Satz 2.12.** Ist $M$ endlich und $a \notin M$, so ist $M \cup \{a\}$ endlich mit $|M \cup \{a\}| = \text{succ}(|M|)$.
*Beweis:* Aus $f\colon n \to M$ wird $\tilde f\colon \text{succ}(n) \to M \cup \{a\}$ mit $\tilde f(x) := f(x)$ für $x \in n$ und $\tilde f(n) := a$.

**Satz 2.13.** Jede Teilmenge einer endlichen Menge ist endlich (Induktion über $n$ für $S \subseteq n$).
**Satz 2.14 (Übung).** $M \cup N$, $M \cap N$, $M \setminus N$, $M \times N$ und $\mathcal{P}(M)$ sind endlich, wenn $M$ und $N$ es sind.

:::rechnung Satz 2.12 an $M = \{a, b, c\}$ und dem neuen Element $d$
f \colon 0 \mapsto a,\ 1 \mapsto b,\ 2 \mapsto c || Bijektion $3 \to M$, also $|M| = 3$
\tilde f(3) := d || das neue Element bekommt die nächste Zahl
3 + 1 = 4 || $\tilde f\colon 4 \to \{a, b, c, d\}$ ist bijektiv, also $|M \cup \{d\}| = \text{succ}(3) = 4$
:::

:::alt Als Gästeliste
Eine Liste mit Gästen von $1$ bis $n$. Kommt ein neuer Gast, schreibst du ihn mit der nächsten Nummer ans Ende. Streichst du Gäste,
bleibt die Liste endlich, sie hat nur Lücken, die du nachnummerierst.
:::
""")

k.ordnen(r"Ordne den Beweis von Satz 2.12: $|M \cup \{a\}| = \text{succ}(|M|)$ für $a \notin M$.",
         [r"Da $M$ endlich ist, gibt es eine Bijektion $f\colon n \to M$ mit $n := |M|$.",
          r"Definiere $\tilde f\colon \text{succ}(n) \to M \cup \{a\}$ durch $\tilde f(x) := f(x)$ für $x \in n$ und $\tilde f(n) := a$.",
          r"Wegen $a \notin M$ wird $a$ nicht doppelt getroffen, also ist $\tilde f$ bijektiv.",
          r"Wegen $\text{succ}(n) = n \cup \{n\}$ ist $\tilde f$ definiert auf allen Elementen von $\text{succ}(n)$.",
          r"Also ist $M \cup \{a\}$ endlich mit $|M \cup \{a\}| = \text{succ}(n)$. $\square$"],
         r"Die Bijektion wird um das neue Element erweitert: Die Zahl $n$ ist gerade der neue Platz, der in $\text{succ}(n)$ dazukommt.",
         ablenker=[r"Wegen $a \in M$ ist $\tilde f$ injektiv.", r"Setze $\tilde f(0) := a$ und verschiebe alle anderen Werte um eins."],
         tipps=["Zuerst braucht man eine Bijektion für $M$, dann erweitert man sie.",
                r"Wo steckt die Voraussetzung $a \notin M$?", r"Die Bedingung $a \notin M$ sichert die Injektivität."])

# ── Seite 3: Min und Max ─────────────────────────────────────────────────
k.erklaerung("Minimum und Maximum (Satz 2.15, 2.16)", r"""
## Jede endliche Menge hat einen Kleinsten

**Satz 2.15.** Jede nichtleere endliche total geordnete Menge $(M, \preccurlyeq)$ besitzt ein [[Minimum]] und ein Maximum.
*Beweis (Induktion über $|M|$):* Sei $|M| = \text{succ}(n)$, $a$ ein Element und $A := M \setminus \{a\}$. Hat $A$ das Minimum $u$ und das
Maximum $v$, so ist das Minimum von $M$ gleich $a$ (falls $a \preccurlyeq u$) oder $u$, das Maximum gleich $v$ (falls $a \preccurlyeq v$) oder $a$.

**Satz 2.16.** Jede nichtleere Teilmenge $N \subseteq \mathbb{N}$ besitzt ein Minimum ([[Wohlordnungsprinzip]]).

:::rechnung Der Schritt an $M = \{7, 3, 9, 5\}$ mit $a = 5$
\text{Minimum und Maximum von } A = \{7, 3, 9\} \text{: } 3 \text{ und } 9 || Induktionsannahme für drei Elemente
5 \le 3 \text{ gilt nicht, also Minimum von } M = 3 || $a \preccurlyeq u$ ist falsch: das alte Minimum bleibt
5 \le 9 \text{ gilt, also Maximum von } M = 9 || $a \preccurlyeq v$ ist wahr, dann ist $v$ das Maximum: es bleibt bei $9$
:::

:::alt Als Wettlauf
Jeder neue Läufer misst sich nur mit dem bisher Schnellsten und dem bisher Langsamsten. Danach kennst du wieder Schnellsten und Langsamsten.
Bei endlich vielen Läufern bist du nach endlich vielen Schritten fertig.
:::
""")

k.menge(r"Bestimme das kleinste Element von $\{n \in \mathbb{N} \mid n^2 > 50\}$ (Satz 2.16 sagt: Es existiert). Eingabe als Zahl in Mengenklammern, z. B. `{3}`.",
        "{8}",
        r"$7^2 = 49 \not> 50$, $8^2 = 64 > 50$. Alle kleineren Zahlen scheitern, also ist $8$ das Minimum.",
        tipps=["Probiere die Quadrate der Reihe nach aus, bis das erste $> 50$ erscheint.", r"$7^2 = 49$", r"Und $8^2 = 64$."],
        rechenweg=r"""
:::rechnung
7^2 = 49 || nicht größer als $50$
8^2 = 64 || größer als $50$: also ist $8$ das Minimum
:::
""",
        typische_fehler=[("{7}", r"$7^2 = 49$ ist **nicht** größer als $50$. Die Bedingung ist $n^2 > 50$."),
                         ("{64}", r"$64$ ist $8^2$. Gefragt ist das kleinste $n$, nicht das Quadrat.")])

# ── Seite 4: Addition ────────────────────────────────────────────────────
k.erklaerung("Addition als Zählen einer Vereinigung (Def. 2.17)", r"""
## Warum man markieren muss

$a + b$ soll die Anzahl der Elemente von „$a$ und $b$ zusammen“ sein. Aber Zahlen sind Mengen mit gemeinsamen Elementen: $4 = \{0, 1, 2, 3\}$ steckt in $7 = \{0, \ldots, 6\}$, also ist $4 \cup 7 = 7$.
Das Skript trennt die beiden Mengen mit Marken.

**Definition 2.17.** $+\colon \mathbb{N}^2 \to \mathbb{N},\ (a, b) \mapsto |(a \times \{0\}) \cup (b \times \{1\})|$. Die Zahl $a + b$ heißt [[Summe]].
Insbesondere gilt $a + 0 = a$.

:::rechnung $4 + 7$ mit Marken
4 \cup 7 = 7 || ohne Marken verschwinden die Elemente von $4$ in $7$
|4 \times \{0\}| = 4 \text{ und } |7 \times \{1\}| = 7 || Paare $(x, 0)$ und $(y, 1)$ sind alle verschieden, denn $0 \neq 1$
4 + 7 = 11 || die Vereinigung hat $4 + 7$ Elemente
:::

:::alt Mit zwei Farben
Stell dir vier rote und sieben blaue Murmeln vor. Auch wenn beide Tüten dieselben Nummern $0, 1, 2, \ldots$ tragen, sind es verschiedene Murmeln, weil sie
verschiedene Farben haben. Die Farbe ist die Marke $0$ oder $1$.
:::
""")

k.zahl(r"Berechne $|(4 \times \{0\}) \cup (7 \times \{1\})|$ (Definition 2.17).", 11,
       r"Die Paare $(x, 0)$ und $(y, 1)$ sind alle verschieden: $4 + 7 = 11$ Elemente. Ohne Marken wäre $4 \cup 7 = 7$ nur $7$ Elemente.",
       tipps=["Zähle erst die Elemente von $4 \\times \\{0\\}$, dann von $7 \\times \\{1\\}$.", "Wegen der verschiedenen Marken überlappen sie nicht.", "Addiere beide Anzahlen."],
       rechenweg=r"""
:::rechnung
4 + 7 = 11 || beide Teilmengen sind disjunkt, die Anzahlen addieren sich
:::
""",
       typische_fehler=[(7, r"Das wäre $|4 \cup 7|$ ohne Marken. Die Marken $0$ und $1$ halten die Elemente auseinander."),
                        (28, r"Das ist $4 \cdot 7 = |4 \times 7|$. Hier wird vereinigt, nicht das Produkt gebildet.")])

# ── Seite 5: Satz 2.18 bis 2.20 ──────────────────────────────────────────
k.erklaerung("Nachfolgerregel und Kürzungsregel (Satz 2.18 bis 2.20)", r"""
## Rechengesetze aus dem Zählen

**Satz 2.18 (Nachfolgerregel).** $\text{succ}(a) + b = \text{succ}(a + b)$. Insbesondere $\text{succ}(b) = 1 + b$.
*Beweis:* $\text{succ}(a) \times \{0\}$ hat genau das Element $(a, 0)$ mehr als $a \times \{0\}$. Nach Satz 2.12 wächst die Anzahl um einen Nachfolger.

**Satz 2.19.** $a \le b \iff \exists k \in \mathbb{N} : b = a + k$ (Übung). So wird die Relation $\le$ aus Definition 1.36 jetzt „von unten“ erklärt.
**Satz 2.20 (Kürzungsregel).** Aus $a + k = a + \ell$ folgt $k = \ell$ (Übung).

:::rechnung Satz 2.18 an Zahlen
3 + 2 = 5 || zuerst $a + b$ für $a = 3$, $b = 2$
\text{succ}(5) = 6 || Nachfolger der Summe
4 + 2 = 6 || $\text{succ}(3) = 4$, also $\text{succ}(3) + 2 = 6 = \text{succ}(3 + 2)$ ✓
:::

:::alt Als Zählstab
Du hast einen Stab mit $a$ Kerben und einen mit $b$ Kerben. Machst du in den ersten eine Kerbe mehr, ist die Gesamtzahl der Kerben um genau eins größer.
:::
""")

k.zuordnen("Ordne die Sätze ihrer Aussage zu.",
           [("Satz 2.18 (Nachfolgerregel)", "succ(a) + b = succ(a + b)"),
            ("Satz 2.20 (Kürzungsregel)", "aus a + k = a + ℓ folgt k = ℓ"),
            ("Satz 2.21", "|A ∪ B| = |A| + |B| für disjunkte A, B"),
            ("Satz 2.26", "|A \\ B| = |A| − |B| für B ⊆ A"),
            ("Satz 2.27", "|A ∪ B| = |A| + |B| − |A ∩ B|")],
           "Merke die Voraussetzungen: 2.21 braucht disjunkte Mengen, 2.26 braucht $B \\subseteq A$, 2.27 gilt immer.",
           ablenker=["|A ∪ B| = |A| · |B|"],
           tipps=["Sätze mit Voraussetzung („disjunkt“, „$B \\subseteq A$“) sind einfacher als der allgemeine Satz.", "Satz 2.27 enthält einen Korrekturterm."])

# ── Seite 6: Satz 2.21 ───────────────────────────────────────────────────
k.erklaerung("Disjunkte Vereinigung (Satz 2.21, Korollar 2.22)", r"""
## Marken sind nicht nötig, wenn nichts überlappt

**Satz 2.21.** Für [[disjunkte|disjunkt]] endliche Mengen $A$ und $B$ gilt $|A \cup B| = |A| + |B|$.
*Beweis:* Aus Bijektionen $f\colon |A| \to A$ und $g\colon |B| \to B$ baut man eine Bijektion $(|A| \times \{0\}) \cup (|B| \times \{1\}) \to A \cup B$
(Satz 1.82 (iii)). Nach Satz 2.11 und Definition 2.17 folgt die Behauptung.

**Korollar 2.22.** $n + m = m + n$ (kommutativ), $(n + m) + r = n + (m + r)$ (assoziativ). Das folgt, weil $A \cup B = B \cup A$ und $(A \cup B) \cup C = A \cup (B \cup C)$.

:::rechnung $A = \{a, b, c\}$ und $B = \{x, y\}$
|A \cup B| = |\{a, b, c, x, y\}| = 5 || $A \cap B = \emptyset$, alle Elemente sind verschieden
3 + 2 = 5 || $|A| + |B|$
2 + 3 = 5 || Kommutativität: Reihenfolge ist egal
:::

:::alt Als zwei Regale
Zwei Regale mit verschiedenen Büchern: Die Gesamtzahl ist die Summe. Stehen dieselben Bücher in beiden, hast du sie doppelt gezählt.
:::
""")

k.wf(r"Für alle endlichen Mengen $A$ und $B$ gilt $|A \cup B| = |A| + |B|$.", False,
     r"Falsch. Satz 2.21 verlangt $A \cap B = \emptyset$. Gegenbeispiel: $A = B = \{1\}$ hat $|A \cup B| = 1 \neq 2$. "
     r"Der allgemeine Fall ist Satz 2.27 mit dem Korrekturterm $-|A \cap B|$.",
     tipps=["Teste $A = B$."])

# ── Seite 7: Summenzeichen ───────────────────────────────────────────────
k.erklaerung("Das Summenzeichen (Def. 2.23)", r"""
## Vielfache Summen aus einer Abbildung

**Definition 2.23.** Seien $n_0, n \in \mathbb{N}$ und $a\colon \{n_0, n_0 + 1, \ldots, n\} \to Z$ eine Abbildung, wobei auf $Z$ eine Addition definiert ist. Dann
$$\sum_{i=n_0}^{n} a(i) := a(n_0) + a(n_0 + 1) + \cdots + a(n).$$

Das [[Summenzeichen]] ist also eine Abkürzung: Die Abbildung $a$ liefert die Summanden. Wegen der Assoziativität (Korollar 2.22) ist die Klammerung egal. Im Vorkurs kennst du den [[Laufindex]] und die [[leere Summe]].

:::rechnung $\sum_{i=2}^{5} i^2$ mit $a(i) = i^2$
2^2 + 3^2 + 4^2 + 5^2 || $i$ läuft von $n_0 = 2$ bis $n = 5$: vier Summanden
= 4 + 9 + 16 + 25 || Quadrate ausrechnen
= 54 || addieren
:::

:::achtung Wie viele Summanden?
Es sind $n - n_0 + 1$, nicht $n - n_0$: Von $i = 2$ bis $i = 5$ sind es vier Summanden, denn beide Grenzen zählen mit.
:::

:::alt Als Schleife
`s = 0; for i in range(2, 6): s += i*i` rechnet genau diese Summe: Der Startwert `2` ist $n_0$, und `range` hört **vor** $6$ auf, also bei $n = 5$.
:::
""")

k.zahl(r"Berechne $\sum_{i=3}^{6} (2i + 1)$ nach Definition 2.23.", 40,
       r"Vier Summanden für $i = 3, 4, 5, 6$: $7 + 9 + 11 + 13 = 40$.",
       tipps=[r"Setze $i = 3, 4, 5, 6$ in $2i + 1$ ein.", r"$7, 9, 11, 13$", "Addiere die vier Werte."],
       rechenweg=r"""
:::rechnung
2 \cdot 3 + 1 + (2 \cdot 4 + 1) + (2 \cdot 5 + 1) + (2 \cdot 6 + 1) = 7 + 9 + 11 + 13 || vier Summanden
7 + 9 + 11 + 13 = 40 || addieren
:::
""",
       typische_fehler=[(27, r"Du hast den letzten Summanden für $i = 6$ vergessen. Die obere Grenze gehört dazu."),
                        (33, r"Du hast den ersten Summanden für $i = 3$ vergessen. Die untere Grenze gehört dazu."),
                        (48, r"Die Summe beginnt bei $i = 3$, nicht bei $i = 1$: Du hast $3 + 5$ zu viel addiert.")])

# ── Seite 8: Subtraktion ─────────────────────────────────────────────────
k.erklaerung("Subtraktion als partielle Umkehrung (Def. 2.24 bis Satz 2.26)", r"""
## Nur wenn es aufgeht

Die Abbildung $n \mapsto n + a$ trifft nicht jede Zahl: $2$ liegt nicht im Bild von $n \mapsto n + 5$. Eine Umkehrung gibt es nur dort, wo es aufgeht.

**Definition 2.24.** Auf $R := \{(a, b) \in \mathbb{N}^2 \mid a \le b\}$ ist $-\colon R \to \mathbb{N},\ (a, b) \mapsto k$ mit dem eindeutigen $k$ aus $b = a + k$
(Satz 2.19, 2.20). Man schreibt $b - a := k$.
**Beobachtung 2.25.** Für $a \le c$: $a + b = c \iff c - a = b$.
**Satz 2.26.** Für endliche $B \subseteq A$ gilt $|A \setminus B| = |A| - |B|$.

:::rechnung Beispiele
5 + 3 = 8 || also ist $8 - 5 = 3$ (Beobachtung 2.25)
8 - 8 = 0 || denn $8 = 8 + 0$
\text{(5, 8) liegt in } R, \text{ aber } (8, 5) \text{ nicht } || $5 - 8$ gibt es in $\mathbb{N}$ nicht: Es gibt kein $k$ mit $5 = 8 + k$
:::

:::alt Als Kontostand
Du darfst nur abheben, was da ist. Von $5$ Euro lassen sich $8$ nicht abheben. Das Ergebnis müsste negativ sein, und das gibt es (noch) nicht. Kapitel 3 erfindet die ganzen Zahlen genau dafür.
:::
""")

k.ordnen(r"Ordne den Beweis von Satz 2.26: Für endliche Mengen $B \subseteq A$ gilt $|A \setminus B| = |A| - |B|$.",
         [r"Die Mengen $B$ und $A \setminus B$ sind disjunkt, und es gilt $A = B \cup (A \setminus B)$.",
          r"Nach Satz 2.21 folgt $|A| = |B| + |A \setminus B|$.",
          r"Insbesondere ist $|B| \le |A|$ (Satz 2.19).",
          r"Nach Beobachtung 2.25 folgt $|A \setminus B| = |A| - |B|$. $\square$"],
         r"Die Differenzmenge ergänzt $B$ zu $A$. Satz 2.21 liefert die Summe, Beobachtung 2.25 macht daraus die Differenz.",
         ablenker=[r"Nach Satz 2.27 gilt $|A \setminus B| = |A| + |B| - |A \cap B|$.",
                   r"Die Mengen $A$ und $B$ sind disjunkt, also $|A| = |B| + |A \setminus B|$."],
         tipps=["Zerlege $A$ in zwei Teile, die sich nicht überlappen.", "Welcher Satz zählt eine disjunkte Vereinigung?",
                "Die Subtraktion ist die Umkehrung der Addition (Beobachtung 2.25)."])

k.mc(r"Welche der folgenden Differenzen existieren in $\mathbb{N}$ nach Definition 2.24?",
     [r"$12 - 5$ und $7 - 7$", r"$5 - 12$", r"$5 - 12 = -7$", r"keine der Differenzen"],
     r"Es muss $a \le b$ gelten. $12 - 5 = 7$ und $7 - 7 = 0$ sind erlaubt. $5 - 12$ gibt es in $\mathbb{N}$ nicht: $5 = 12 + k$ hat keine Lösung in $\mathbb{N}$.",
     tipps=["Prüfe die Bedingung $a \\le b$ für $b - a$.", "Ist $0$ als Ergebnis erlaubt?", r"Zahlen wie $-7$ gibt es in $\mathbb{N}$ nicht."],
     fehler={r"$5 - 12$": r"Es gibt kein $k \in \mathbb{N}$ mit $5 = 12 + k$: Die Differenz ist nicht definiert.",
             r"$5 - 12 = -7$": r"$-7 \notin \mathbb{N}$. Das Ergebnis müsste in $\mathbb{N}$ liegen.",
             "keine der Differenzen": r"$12 = 5 + 7$ und $7 = 7 + 0$: Beide Differenzen existieren."})

# ── Seite 9: Satz 2.27 ───────────────────────────────────────────────────
k.erklaerung("Inklusion und Exklusion (Satz 2.27)", r"""
## Doppelt gezählte abziehen

**Satz 2.27.** Für endliche Mengen $A$ und $B$ gilt $|A \cup B| = |A| + |B| - |A \cap B|$.

:::visual venn
{"mengen": [{"name": "A", "elemente": [1, 2, 3, 4, 5]}, {"name": "B", "elemente": [4, 5, 6, 7]}],
 "universum": [1, 2, 3, 4, 5, 6, 7, 8], "markiert": "A ∩ B",
 "unterschrift": "$|A| = 5$ und $|B| = 4$ zählen die Elemente $4$ und $5$ zweimal. Der Schnitt wird einmal abgezogen."}
:::

Das Skript beweist es als Bild: Zerlege $A \cup B$ in $A$ und $B \setminus A$, und $B \setminus A$ ist $B$ ohne $A \cap B$.

:::rechnung Beispiel mit $A = \{1, \ldots, 5\}$ und $B = \{4, 5, 6, 7\}$
5 + 4 = 9 || $|A| + |B|$ zählt $4$ und $5$ doppelt
9 - 2 = 7 || $|A \cap B| = |\{4, 5\}| = 2$ abziehen
|\{1, 2, 3, 4, 5, 6, 7\}| = 7 || Kontrolle durch Aufzählen
:::

:::alt Mit zwei Fanclubs
Ein Verein hat 5 Mitglieder im Schach-Club und 4 im Go-Club, 2 sind in beiden. Wie viele Personen sind in mindestens einem Club?
Nicht $9$, denn zwei haben sich doppelt angemeldet.
:::
""")

k.zahl(r"$A = \{1, 2, 3, 4, 5\}$ und $B = \{4, 5, 6, 7\}$. Berechne $|A \cup B|$ **mit** Satz 2.27.", 7,
       r"$|A| + |B| - |A \cap B| = 5 + 4 - 2 = 7$.",
       tipps=[r"Bestimme $|A|$, $|B|$ und $|A \cap B|$.", r"$A \cap B = \{4, 5\}$", "Rechne $5 + 4 - 2$."],
       rechenweg=r"""
:::rechnung
5 + 4 - 2 = 7 || $|A| + |B| - |A \cap B|$
:::
""",
       typische_fehler=[(9, "Du hast nur $|A| + |B|$ gerechnet. Die Elemente $4$ und $5$ sind dann doppelt gezählt."),
                        (11, "Du hast den Schnitt addiert statt abgezogen. Er wurde ja schon zu viel gezählt.")])

k.luecke(r"Satz 2.27 an einer Kursliste: 14 Studierende belegen Analysis, 11 belegen Lineare Algebra, 6 belegen beides. Fülle die Lücken.",
         r"|A \cup B| = 14 + \luecke - \luecke = \luecke",
         [[11], [6], [19]],
         r"$|A \cup B| = |A| + |B| - |A \cap B| = 14 + 11 - 6 = 19$. Mindestens einen der beiden Kurse belegen $19$ Personen.",
         tipps=[r"$|B| = 11$ und $|A \cap B| = 6$.", r"$14 + 11 = 25$", r"$25 - 6 = 19$"],
         rechenweg=r"""
:::rechnung
14 + 11 - 6 = 19 || $|A| + |B| - |A \cap B|$
:::
""",
         typische_fehler=[([11, 6, 25], r"$14 + 11 = 25$ zählt die Personen, die beides belegen, doppelt. Ziehe $6$ ab, dann sind es $19$.")])


# ── Praxis ────────────────────────────────────────────────────────────────
def rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def kardinalitaet_vereinigung(rng):
    gross = rng.randint(7, 12)
    a = set(rng.sample(range(1, gross + 1), rng.randint(3, 6)))
    b = set(rng.sample(range(1, gross + 1), rng.randint(3, 6)))
    while len(a & b) < 1 or len(a & b) == min(len(a), len(b)):
        a = set(rng.sample(range(1, gross + 1), rng.randint(3, 6)))
        b = set(rng.sample(range(1, gross + 1), rng.randint(3, 6)))
    na, nb, ns = len(a), len(b), len(a & b)
    assert len(a | b) == na + nb - ns
    loesung = na + nb - ns
    fehler = [(na + nb, f"Du hast $|A| + |B| = {na + nb}$ gerechnet. Die Elemente von $A \\cap B$ sind dann doppelt gezählt."),
              (na + nb + ns, "Der Schnitt wird abgezogen, nicht addiert."),
              (ns, "Das ist $|A \\cap B|$. Gefragt ist die Anzahl der Elemente der Vereinigung."),
              (na + nb - 2 * ns, f"Der Schnitt wird nur **einmal** abgezogen (nach der Doppelzählung bleibt er einmal stehen).")]
    return {
        "frage": f"Gegeben sind $A = {mtex(a)}$ und $B = {mtex(b)}$. Bestimme $|A \\cup B|$ mit Satz 2.27.",
        "loesung": loesung,
        "tipps": ["Bestimme $|A|$, $|B|$ und den Schnitt $A \\cap B$.", f"$A \\cap B = {mtex(a & b)}$, also $|A \\cap B| = {ns}$.",
                  f"Rechne $|A| + |B| - |A \\cap B| = {na} + {nb} - {ns}$."],
        "rechenweg": rechnung([(f"{na} + {nb} - {ns} = {loesung}", f"$|A| + |B| - |A \\cap B|$ mit $A \\cap B = {mtex(a & b)}$")]),
        "erklaerung": "Satz 2.27: Elemente im Schnitt werden von $|A| + |B|$ doppelt gezählt, darum zieht man $|A \\cap B|$ einmal ab.",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


def summenzeichen_wert(rng):
    n0 = rng.randint(0, 4)
    n = n0 + rng.randint(2, 5)
    a, b = rng.randint(1, 4), rng.randint(0, 3)
    art = rng.choice(["linear", "quadrat"])
    if art == "linear":
        term = f"{a if a != 1 else ''}i" + (f" + {b}" if b else "")
        werte = [a * i + b for i in range(n0, n + 1)]
        f = lambda i: a * i + b  # noqa: E731
    else:
        term = f"{a if a != 1 else ''}i^2" + (f" + {b}" if b else "")
        werte = [a * i * i + b for i in range(n0, n + 1)]
        f = lambda i: a * i * i + b  # noqa: E731
    loesung = sum(werte)
    assert loesung == sum(f(i) for i in range(n0, n + 1))
    fehler = [(sum(f(i) for i in range(n0 + 1, n + 1)), f"Du hast den ersten Summanden für $i = {n0}$ vergessen. Der Index beginnt bei $n_0 = {n0}$ und dieser Wert gehört dazu."),
              (sum(f(i) for i in range(n0, n)), f"Du hast den letzten Summanden für $i = {n}$ vergessen. Die obere Grenze gehört dazu."),
              (sum(f(i) for i in range(1, n + 1)), f"Du hast bei $i = 1$ statt bei $i = {n0}$ begonnen. Die untere Grenze ist $n_0 = {n0}$.")]
    zeile = " + ".join(f"({f(i)})" if False else str(f(i)) for i in range(n0, n + 1))
    return {
        "frage": f"Berechne $\\sum_{{i={n0}}}^{{{n}}} ({term})$ nach Definition 2.23.",
        "loesung": loesung,
        "tipps": [f"Die Summe hat $n - n_0 + 1 = {n - n0 + 1}$ Summanden: $i$ läuft von ${n0}$ bis ${n}$.",
                  f"Berechne den Summanden $a(i) = {term}$ für jedes $i$ einzeln.", f"Die Summanden sind ${', '.join(str(w) for w in werte)}$."],
        "rechenweg": rechnung([(f"{zeile} = {loesung}", f"Summanden für $i = {n0}, \\ldots, {n}$ ausgerechnet und addiert")]),
        "erklaerung": "Das Summenzeichen ist eine Abkürzung für $a(n_0) + a(n_0 + 1) + \\cdots + a(n)$ (Def. 2.23).",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


def differenzmenge_zaehlen(rng):
    na = rng.randint(7, 15)
    nb = rng.randint(2, na - 2)
    A = list(range(1, na + 1))
    B = sorted(rng.sample(A, nb))
    loesung = na - nb
    assert len(set(A) - set(B)) == loesung
    fehler = [(na + nb, "Du hast addiert. Beim Entfernen von $B$ aus $A$ wird abgezogen: $|A \\setminus B| = |A| - |B|$."),
              (nb, "Das ist $|B|$. Gefragt ist, wie viele Elemente **übrig bleiben**."),
              (na, "Das ist $|A|$. Die Elemente von $B$ müssen aber entfernt werden.")]
    return {
        "frage": f"Sei $A = \\{{1, 2, \\ldots, {na}\\}}$ und $B = {mtex(B)} \\subseteq A$. Bestimme $|A \\setminus B|$ mit Satz 2.26.",
        "loesung": loesung,
        "tipps": [f"Bestimme $|A| = {na}$ und zähle die Elemente von $B$.", "Satz 2.26: Für $B \\subseteq A$ gilt $|A \\setminus B| = |A| - |B|$.",
                  f"Rechne ${na} - {nb}$."],
        "rechenweg": rechnung([(f"{na} - {nb} = {loesung}", "$|A| - |B|$ nach Satz 2.26")]),
        "erklaerung": "Wegen $B \\subseteq A$ zerlegt $A$ in $B$ und $A \\setminus B$ (disjunkt), also $|A| = |B| + |A \\setminus B|$.",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


k.praxis()

k.generator(kardinalitaet_vereinigung, typ="zahl", titel="Kardinalität einer Vereinigung (Satz 2.27)")
k.generator(summenzeichen_wert, typ="zahl", titel="Summenzeichen ausrechnen")
k.generator(differenzmenge_zaehlen, typ="zahl", titel="Kardinalität einer Differenzmenge (Satz 2.26)")

k.rechenweg_aufgabe(r"""
## Quiz-Stil: Anmeldungen zählen

In einem Jahrgang mit $30$ Studierenden belegen $18$ den Kurs „Python“ ($P$) und $14$ den Kurs „Java“ ($J$). Genau $6$ belegen beide.
""",
    [{"typ": "zahl", "frage": r"Wie viele belegen mindestens einen der beiden Kurse, also $|P \cup J|$?", "loesung": 26,
      "tipps": ["Satz 2.27 anwenden.", r"$18 + 14 - 6$"],
      "rechenweg": r"$|P \cup J| = 18 + 14 - 6 = 26$.",
      "erklaerung": r"Die $6$ sind in $18 + 14$ doppelt gezählt.",
      "typische_fehler": [(32, "Die $6$ Studierenden, die beide Kurse belegen, sind doppelt gezählt: ziehe $|P \\cap J| = 6$ ab.")]},
     {"typ": "zahl", "frage": r"Wie viele belegen **keinen** der beiden Kurse?", "loesung": 4,
      "tipps": [r"Satz 2.26 mit $B = P \cup J \subseteq$ Jahrgang.", r"$30 - 26$"],
      "rechenweg": r"$30 - 26 = 4$.",
      "erklaerung": r"Der Jahrgang ist die Obermenge, $P \cup J$ die Teilmenge: $|\text{Jahrgang} \setminus (P \cup J)| = 30 - 26$.",
      "typische_fehler": [(12, r"Das sind $30 - 18$, also die ohne Python. Keinen der **beiden** Kurse heißt: nicht in $P \cup J$.")]},
     {"typ": "zahl", "frage": r"Wie viele belegen **genau einen** der beiden Kurse?", "loesung": 20,
      "tipps": [r"$|P \cup J| - |P \cap J|$", r"$26 - 6$"],
      "rechenweg": r"$|P \cup J| - |P \cap J| = 26 - 6 = 20$ (Satz 2.26 mit $P \cap J \subseteq P \cup J$).",
      "erklaerung": r"Wer in beiden ist, belegt nicht **genau** einen.",
      "typische_fehler": [(26, "Das ist mindestens einer (inklusive der $6$, die beide belegen).")]}],
    r"$|P \cup J| = 26$, keinen Kurs belegen $4$, genau einen Kurs $20$ Studierende.",
    uebungsblatt=True,
    tipps=["Zeichne ein Venn-Diagramm mit zwei Kreisen und trage zuerst die $6$ in den Schnitt ein.", "Beschrifte danach $P$ ohne $J$ und $J$ ohne $P$ mit Satz 2.26."],
    rechenweg=r"""
:::rechnung
18 + 14 - 6 = 26 || mindestens einen Kurs (Satz 2.27)
30 - 26 = 4 || keinen Kurs (Satz 2.26)
26 - 6 = 20 || genau einen Kurs
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Satz 2.27 beweisen und die Kürzungsregel

1. Beweisen Sie Satz 2.27: Für endliche Mengen $A, B$ gilt $|A \cup B| = |A| + |B| - |A \cap B|$. Verwenden Sie nur Satz 2.21 und Satz 2.26.
2. Beweisen Sie Satz 2.20 (Kürzungsregel) per Induktion über $a$: Aus $a + k = a + \ell$ folgt $k = \ell$. Sie dürfen $0 + b = b$,
   Satz 2.18 und die Injektivität von $\text{succ}$ (P4) benutzen.
""",
    r"""
**1.** Es gilt $A \cup B = A \cup (B \setminus A)$ und $A \cap (B \setminus A) = \emptyset$, nach Satz 2.21 also $|A \cup B| = |A| + |B \setminus A|$.
Außerdem ist $B \setminus A = B \setminus (A \cap B)$ mit $A \cap B \subseteq B$, nach Satz 2.26 also $|B \setminus A| = |B| - |A \cap B|$.
Einsetzen: $|A \cup B| = |A| + (|B| - |A \cap B|) = |A| + |B| - |A \cap B|$ (Beobachtung 2.25). $\square$

**2. Anfang** ($a = 0$): Aus $0 + k = 0 + \ell$ folgt wegen $0 + b = b$ sofort $k = \ell$.
**Annahme:** Für ein $a$ gelte: $a + k = a + \ell \Rightarrow k = \ell$ (für alle $k, \ell$).
**Schritt:** Sei $\text{succ}(a) + k = \text{succ}(a) + \ell$. Nach Satz 2.18 ist das $\text{succ}(a + k) = \text{succ}(a + \ell)$.
Da $\text{succ}$ injektiv ist (P4), folgt $a + k = a + \ell$, nach der Annahme also $k = \ell$. Nach Satz 2.6 gilt die Aussage für alle $a$. $\square$
""",
    ["In 1.: $A \\cup B = A \\cup (B \\setminus A)$ als disjunkte Zerlegung erkannt und Satz 2.21 angewendet",
     "In 1.: $|B \\setminus A| = |B| - |A \\cap B|$ mit Satz 2.26 begründet (Teilmengenbedingung geprüft)",
     "In 2.: Anfang für $a = 0$ korrekt",
     "In 2.: Nachfolgerregel (Satz 2.18) und Injektivität von succ (P4) im Schritt benutzt",
     "In 2.: Die Annahme gilt für festes $a$ und **alle** $k, \\ell$"],
    "Satz 2.27 folgt aus den einfacheren Sätzen 2.21 und 2.26 durch geschicktes Zerlegen. Die Kürzungsregel ist eine Induktion über $a$, die Nachfolgerregel und P4 braucht.",
    uebungsblatt=True,
    tipps=["Zerlege $A \\cup B$ in zwei Teile ohne gemeinsame Elemente.", "Welcher Teil von $B$ liegt schon in $A$?",
           "Bei Aufgabe 2 ist P4 der Schritt, der aus $\\text{succ}(x) = \\text{succ}(y)$ ein $x = y$ macht."])

k.zusammenfassung(r"""
## Endliche Mengen, Addition und Subtraktion (Skript Abschn. 2.3 und 2.4)

- **Endlich** (Def. 2.10): Bijektion $f\colon n \to M$; $|M| := n$ (Kardinalität). $|n| = n$. Umbenennen ändert nichts (Satz 2.11).
- $|M \cup \{a\}| = \text{succ}(|M|)$ für $a \notin M$ (Satz 2.12). Teilmengen endlicher Mengen sind endlich (Satz 2.13); ebenso $\cup, \cap, \setminus, \times, \mathcal{P}$ (Satz 2.14).
- Endlich und total geordnet: Minimum und Maximum (Satz 2.15). Jede nichtleere Teilmenge von $\mathbb{N}$ hat ein Minimum (Satz 2.16, Wohlordnung).
- **Addition** (Def. 2.17): $a + b := |(a \times \{0\}) \cup (b \times \{1\})|$. $\text{succ}(a) + b = \text{succ}(a + b)$ (2.18), $a \le b \iff \exists k : b = a + k$ (2.19), Kürzungsregel (2.20).
- **Disjunkte Vereinigung** (Satz 2.21): $|A \cup B| = |A| + |B|$. Kommutativ und assoziativ (Kor. 2.22).
- **Summenzeichen** (Def. 2.23): $\sum_{i=n_0}^{n} a(i) = a(n_0) + \cdots + a(n)$.
- **Subtraktion** (Def. 2.24): $b - a := k$ mit $b = a + k$, nur für $a \le b$. $a + b = c \iff c - a = b$ (2.25). $|A \setminus B| = |A| - |B|$ für $B \subseteq A$ (2.26).
- **Satz 2.27:** $|A \cup B| = |A| + |B| - |A \cap B|$.

!! Wer zwei Mengen vereinigt, darf nur dann addieren, wenn sie disjunkt sind. Sonst den Schnitt einmal abziehen.
""")
