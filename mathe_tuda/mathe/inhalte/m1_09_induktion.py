# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 9: Natürliche Zahlen und vollständige Induktion
(Skript Disser WS 26/27, Abschn. 2.1 und 2.2, dazu Satz 2.34 und 2.35 aus Abschn. 2.5 als Übung der Induktion)."""
from fractions import Fraction as F

from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(
    slug="peano_induktion",
    titel="Natürliche Zahlen und vollständige Induktion",
    beschreibung="Peano-Axiome, ℕ aus Mengen, Nachfolger, Induktionsanfang und -schritt, Abwandlungen der Induktion (Beob. 2.9)",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 2.1 und 2.2",
    icon="🁢")


# ── Python rechnet alles nach ──────────────────────────────────────────────
def von(n):
    """Die Zahl n als Menge (Def. 2.2): 0 = ∅, n+1 = n ∪ {n}."""
    x = frozenset()
    for _ in range(n):
        x = x | {x}
    return x


def mengen_tex(x):
    if not x:
        return "\\emptyset"
    return "\\{" + ", ".join(mengen_tex(y) for y in sorted(x, key=len)) + "\\}"


# Def. 2.2: jedes n ist die Menge der vorigen Zahlen, Satz 2.4: succ(n) = n ∪ {n}
assert von(3) == frozenset({von(0), von(1), von(2)}) and von(4) == von(3) | {von(3)}
assert all(len(von(n)) == n for n in range(12))
# Def. 2.3: ≤ ist ⊆
assert all((von(a) <= von(b)) == (a <= b) for a in range(10) for b in range(10))
# P3 und P4 für das Mengenmodell (endlicher Ausschnitt)
assert all(von(n) | {von(n)} != frozenset() for n in range(10))
assert len({von(n) | {von(n)} for n in range(10)}) == 10
assert von(5) == frozenset(von(i) for i in range(5))


def peano_verletzt(m, succ):
    """Struktur ({0,…,m-1}, 0, succ) mit succ als dict: Liste der verletzten Axiome unter P3, P4, P5."""
    bild = [succ[x] for x in range(m)]
    verl = []
    if 0 in bild:
        verl.append("P3")
    if len(set(bild)) < m:
        verl.append("P4")
    erreicht, rand = {0}, [0]
    while rand:
        y = succ[rand.pop()]
        if y not in erreicht:
            erreicht.add(y)
            rand.append(y)
    if len(erreicht) < m:
        verl.append("P5")
    return verl, erreicht


# die drei Modelle der Seite 2 (je ein Axiom verletzt)
assert peano_verletzt(3, {0: 1, 1: 2, 2: 0})[0] == ["P3"]
assert peano_verletzt(4, {0: 1, 1: 2, 2: 3, 3: 3})[0] == ["P4"]
assert all(x + 2 != 0 for x in range(1000)) and len({x + 2 for x in range(1000)}) == 1000
assert all(x % 2 == 0 for x in range(0, 1000, 2) if (x + 2) % 2 != 0) and 1 % 2 == 1     # (ℕ, 0, +2): nur gerade erreichbar
# Satz 2.35, Satz 2.34, Beispiel 4^n = 3k + 1 und Summenformel der Aufgaben
for _n in range(1, 60):
    assert sum(2 * i for i in range(1, _n + 1)) == _n * (_n + 1)
    assert sum(7 for _ in range(_n)) == 7 * _n
    assert (_n + 1) * (_n + 2) == _n * (_n + 1) + 2 * (_n + 1)
for _n in range(0, 60):
    assert 4 ** _n % 3 == 1 and 4 ** (_n + 1) == 4 * (3 * (4 ** _n // 3) + 1)
    assert sum(2 * i + 1 for i in range(_n + 1)) == (_n + 1) ** 2
    assert 2 * sum(3 * i + 1 for i in range(_n + 1)) == (_n + 1) * (3 * _n + 2)
    assert (_n + 1) * (3 * _n + 2) + 2 * (3 * (_n + 1) + 1) == (_n + 2) * (3 * (_n + 1) + 2)
    assert (_n + 1) ** 2 + 2 * _n + 3 == (_n + 2) ** 2

k.lernziele([
    "Ich kann die fünf Peano-Axiome nennen und an Beispielen entscheiden, welches Axiom eine Struktur verletzt (Def. 2.1)",
    "Ich verstehe, wie ℕ aus der leeren Menge entsteht ($n \\cup \\{n\\}$), und kenne Satz 2.4 und Satz 2.5 (Def. 2.2, 2.3)",
    "Ich beweise Aussagen mit vollständiger Induktion (Satz 2.6) und benenne Induktionsanfang, -annahme und -schritt sauber (Satz 2.7, Bsp. 2.8, Satz 2.35)",
    "Ich kenne die Abwandlungen der Induktion: starke Induktion, anderer Startwert, Bijektion auf eine Teilmenge (Beob. 2.9)",
])

k.warum(r"""
Eine Schleife `for i in range(n)` läuft „für alle $n$“ und gehört doch zu einem Programm
endlicher Länge. Das geht, weil Zählen nur aus einem Start und einem „nächsten“ besteht, genau
wie ein Zeiger `next` in einer verketteten Liste. Die Peano-Axiome sagen präzise, wann so eine Liste
die natürlichen Zahlen ist. Die vollständige Induktion ist daraus der Beweis für Schleifeninvarianten und
rekursive Funktionen. Im Vorkurs hast du Induktion als Rezept gelernt. Hier siehst du, **warum** sie
gilt: Sie ist nichts anderes als das fünfte Peano-Axiom.
""")

# ── Seite 1: Peano-Axiome ─────────────────────────────────────────────────
k.erklaerung("Zählen: die Peano-Axiome (Def. 2.1)", r"""
## Was brauchst du zum Zählen?

:::analogie 🪜 Eine Treppe ohne Ende
Du stehst auf Stufe „Null“. Von jeder Stufe führt genau eine Treppe zur nächsten. Du gehst nie im
Kreis, und jede Stufe erreichst du irgendwann.
:::

**Definition 2.1.** Ein Tupel $(N, n_0, \text{succ})$ erfüllt die [[Peano-Axiome]], wenn gilt:

- **P1:** $n_0 \in N$ (Existenz der Null).
- **P2:** $\text{succ}\colon N \to N$ ist eine Abbildung (jedes $n$ hat einen [[Nachfolger]]).
- **P3:** $\text{succ}(n) \neq n_0$ für alle $n$ (die Null ist kein Nachfolger).
- **P4:** $\text{succ}$ ist injektiv (verschiedene Zahlen haben verschiedene Nachfolger).
- **P5:** Aus $M \subseteq N$, $n_0 \in M$ und $\text{succ}(M) \subseteq M$ folgt $M = N$.

:::rechnung Zählen mit Nachfolgern
\text{succ}(0) = 1 || der Nachfolger der Null heißt $1$
\text{succ}(1) = 2 || der Nachfolger von $1$ heißt $2$
\text{succ}(2) = 3 || und so weiter: jede Zahl entsteht aus der vorigen
:::

:::alt Als verkettete Liste
`succ` ist der `next`-Zeiger. P1: Es gibt einen Listenanfang. P2: Jeder Knoten hat einen Nachfolger.
P3: Auf den Anfang zeigt nichts. P4: Auf keinen Knoten zeigen zwei Zeiger. P5: Jeder Knoten ist vom Anfang aus
erreichbar, es gibt keine losen Knoten.
:::
""")

k.zuordnen("Ordne jedem Peano-Axiom seine Bedeutung zu (Def. 2.1).",
           [("P1", "es gibt eine Null"),
            ("P2", "jede Zahl hat einen Nachfolger"),
            ("P3", "die Null ist kein Nachfolger"),
            ("P4", "verschiedene Zahlen haben verschiedene Nachfolger"),
            ("P5", "es gibt keine überflüssigen Elemente")],
           "P1 und P2 liefern Start und Schritt. P3 und P4 verhindern Kreise und Zusammenläufe. P5 verbietet Elemente, die man vom Start aus nie erreicht.",
           ablenker=["jede Zahl ist ihr eigener Nachfolger"],
           tipps=["Die Klammern hinter den Axiomen im Skript sind schon die Bedeutung.",
                  "P3 und P4 handeln vom Bild von succ, P5 von Teilmengen."])

# ── Seite 2: Modelle, die scheitern ───────────────────────────────────────
k.erklaerung("Fünf Regeln, fünf Fehlermöglichkeiten", r"""
## Jedes Axiom verbietet einen Fehler

Schlechte Zählstrukturen scheitern jeweils an einem Axiom:

| Struktur $(N, n_0, \text{succ})$ | verletzt | Grund |
|---|---|---|
| $(\{0, 1, 2\}, 0,\ x \mapsto (x+1) \bmod 3)$ | P3 | $\text{succ}(2) = 0$: Zählen im Kreis |
| $(\{0, 1, 2, 3\}, 0,\ \text{succ}(3) = 3)$ | P4 | $\text{succ}(2) = \text{succ}(3)$: Zusammenlauf |
| $(\mathbb{N}, 0,\ x \mapsto x + 2)$ | P5 | die ungeraden Zahlen werden nie erreicht |

:::rechnung P5 prüfen am Modell $x \mapsto x + 2$
M := \{0, 2, 4, \ldots\} \text{ mit } 0 \in M || Teilmenge der geraden Zahlen, enthält die Null
\text{succ}(2k) = 2k + 2 \text{ ist gerade} || also $\text{succ}(M) \subseteq M$
\text{aber } 1 \notin M, \text{ also } M \neq \mathbb{N} || P5 ist verletzt: $1$ ist überflüssig
:::

:::achtung Im Endlichen geht es nie
Eine endliche Struktur kann P3 und P4 nicht zugleich erfüllen: Eine injektive Abbildung einer endlichen Menge in sich
trifft jedes Element, auch die Null. Darum braucht man unendlich viele Zahlen.
:::

:::alt Als Eisenbahnnetz
P3: Der Startbahnhof hat keine Einfahrt. P4: In jeden Bahnhof führt höchstens ein Gleis. P5: Jeder Bahnhof ist
vom Start aus mit dem Zug erreichbar. Eine Insel mit eigenem Gleiskreis verletzt P5.
:::
""")

k.mc(r"Die Struktur $(\mathbb{Z}, 0, x \mapsto x + 1)$ ist **keine** Peano-Struktur. Welches Axiom scheitert zuerst und warum?",
     [r"P5 und P3: Von $0$ aus erreichst du die negativen Zahlen nicht, und $\text{succ}(-1) = 0$",
      r"P4: Die Abbildung $x \mapsto x + 1$ ist nicht injektiv",
      r"P2: Nicht jede ganze Zahl hat einen Nachfolger",
      r"Nur P1: Es gibt keine Null in $\mathbb{Z}$"],
     r"$\text{succ}(-1) = 0$ verletzt P3. Außerdem enthält $M = \{0, 1, 2, \ldots\}$ die Null und ist unter succ abgeschlossen, "
     r"ist aber nicht ganz $\mathbb{Z}$: P5 scheitert. Injektiv ist $x \mapsto x + 1$ dagegen.",
     tipps=["Prüfe, ob irgendeine ganze Zahl den Nachfolger $0$ hat.", "Welche Zahlen erreichst du von $0$ aus mit succ?",
            r"Ist $x \mapsto x + 1$ injektiv? Aus $x + 1 = y + 1$ folgt $x = y$."],
     fehler={r"P4: Die Abbildung $x \mapsto x + 1$ ist nicht injektiv": r"Aus $x + 1 = y + 1$ folgt $x = y$: Sie ist injektiv.",
             r"P2: Nicht jede ganze Zahl hat einen Nachfolger": r"Jede ganze Zahl $x$ hat den Nachfolger $x + 1 \in \mathbb{Z}$: P2 gilt.",
             r"Nur P1: Es gibt keine Null in $\mathbb{Z}$": r"$0 \in \mathbb{Z}$: P1 gilt. Schon $\text{succ}(-1) = 0$ verletzt aber P3."})

# ── Seite 3: ℕ aus Mengen ────────────────────────────────────────────────
_ZAHLEN_TABELLE = "\n".join(f"| ${n}$ | ${mengen_tex(von(n))}$ | ${n}$ |" for n in range(4))
k.erklaerung("ℕ aus Mengen gebaut (Def. 2.2, 2.3, Satz 2.4)", r"""
## Zahlen sind Mengen

**Definition 2.2.** Jede Zahl ist die Menge der vorigen Zahlen: $0 := \emptyset$, $1 := \{0\}$, $2 := \{0, 1\}$, $3 := \{0, 1, 2\}$, …
Die Menge aller dieser Zahlen ist $\mathbb{N} = \{0, 1, 2, \ldots\}$ (im Skript beginnt $\mathbb{N}$ bei $0$).

| Zahl | als Menge | Anzahl Elemente |
|---|---|---|
§TABELLE§

**Definition 2.3.** $\le\ := \subseteq$ ist eine [[Totalordnung]] auf $\mathbb{N}$, und $a < b :\iff a \le b \land a \neq b$.
**Satz 2.4.** Mit $\text{succ}(n) := n \cup \{n\}$ erfüllt $(\mathbb{N}, 0, \text{succ})$ die Peano-Axiome.

:::rechnung Der Nachfolger von $2$
\text{succ}(2) = 2 \cup \{2\} || Definition von succ
= \{0, 1\} \cup \{2\} || $2 = \{0, 1\}$
= \{0, 1, 2\} = 3 || das ist die Menge der Zahlen bis $2$
:::

:::alt Mit Türmen aus Bausteinen
$0$ ist das leere Regal. Der Nachfolger legt das **ganze bisherige Regal als einen neuen Baustein** dazu. So wächst die Anzahl
der Bausteine in jedem Schritt um genau $1$, und $a \subseteq b$ heißt: $a$ liegt als Teilturm in $b$.
:::
""".replace("§TABELLE§", _ZAHLEN_TABELLE))

k.menge(r"Im Skript ist $3 := \{0, 1, 2\}$. Schreibe die Zahl $4$ als Menge von Zahlen, zum Beispiel `{0; 1}`.",
        "{0; 1; 2; 3}",
        r"$4 = \text{succ}(3) = 3 \cup \{3\} = \{0, 1, 2\} \cup \{3\} = \{0, 1, 2, 3\}$: die Menge **aller vorigen** Zahlen.",
        tipps=[r"Jede Zahl ist die Menge aller kleineren Zahlen.", r"$\text{succ}(3) = 3 \cup \{3\}$", r"Die vier Elemente sind $0, 1, 2, 3$."],
        rechenweg=r"""
:::rechnung
\text{succ}(3) = 3 \cup \{3\} || Definition
= \{0, 1, 2\} \cup \{3\} || $3 = \{0, 1, 2\}$
= \{0, 1, 2, 3\} || $4$ hat vier Elemente
:::
""",
        typische_fehler=[("{1; 2; 3; 4}", r"Die Zahl $4$ enthält die **kleineren** Zahlen $0, 1, 2, 3$, nicht sich selbst und nicht die $4$."),
                         ("{0; 1; 2}", r"Das ist die Menge $3$. Der Nachfolger $4 = 3 \cup \{3\}$ nimmt die $3$ selbst als Element dazu."),
                         ("{4}", r"Du hast $\{\text{succ}(3)\}$ gebildet. $4$ ist aber die Menge aller vorigen Zahlen.")])

k.zahl(r"Nach Definition 2.2 ist $6 = \{0, 1, 2, 3, 4, 5\}$. Wie viele Elemente hat die Menge $6$?", 6,
       r"Die Zahl $n$ hat genau $n$ Elemente: $0, 1, \ldots, n - 1$. Darum gilt später $|n| = n$ (Def. 2.10).",
       tipps=["Zähle die Elemente von $6$ einzeln.", r"Die Zahl $n$ ist die Menge $\{0, \ldots, n-1\}$.", "Es sind so viele Elemente, wie die Zahl selbst angibt."],
       rechenweg=r"""
:::rechnung
0, 1, 2, 3, 4, 5 \text{ sind sechs Elemente} || Aufzählen
6 = 5 + 1 || der Nachfolger kommt immer genau ein Element dazu
:::
""",
       typische_fehler=[(5, r"Das ist das **größte** Element von $6$. Gezählt werden aber alle Elemente, auch die $0$."),
                        (7, r"Die $6$ ist nicht Element von sich selbst: $6 = \{0, \ldots, 5\}$.")])

k.ordnen(r"Ordne den Beweis von P4 für $(\mathbb{N}, 0, \text{succ})$ (Satz 2.4): $\text{succ}$ ist injektiv.",
         [r"Seien $n, m \in \mathbb{N}$ mit $n \neq m$, wobei $n$ in der Aufzählung vor $m$ steht.",
          r"Nach Definition besteht $\text{succ}(n) = n \cup \{n\}$ aus $n$ und den Zahlen davor.",
          r"Also gilt $m \notin \text{succ}(n)$.",
          r"Andererseits gilt $m \in \text{succ}(m)$.",
          r"Somit ist $\text{succ}(n) \neq \text{succ}(m)$, und $\text{succ}$ ist injektiv. $\square$"],
         r"Man zeigt die Kontraposition: Verschiedene $n \neq m$ haben verschiedene Nachfolger, weil $m$ nur im Nachfolger von $m$ (oder später) liegt.",
         ablenker=[r"Da $m$ nach $n$ kommt, gilt $m \in \text{succ}(n)$.",
                   r"Für $n = 0$ und $m = 1$ stimmt es, also gilt es für alle."],
         tipps=["Der Beweis zeigt: $n \\neq m$ impliziert $\\text{succ}(n) \\neq \\text{succ}(m)$.",
                "Suche ein Element, das in genau einer der beiden Mengen liegt.",
                r"$m \in \text{succ}(m)$, aber $m \notin \text{succ}(n)$, wenn $n$ vor $m$ steht."])

# ── Seite 4: Satz 2.5 ────────────────────────────────────────────────────
k.erklaerung("Satz 2.5: Es gibt nichts Überflüssiges", r"""
## Jede Zahl außer $0$ hat einen Vorgänger

P5 soll überflüssige Elemente verbieten. Das Skript prüft, dass es das wirklich tut:

**Satz 2.5.** Jedes $n \in \mathbb{N} \setminus \{0\}$ ist Nachfolger einer Zahl, es gibt also $m$ mit $\text{succ}(m) = n$.

*Beweisidee.* Setze $M := \{0\} \cup \text{succ}(\mathbb{N})$. Dann liegt $0$ in $M$, und $\text{succ}(M) \subseteq \text{succ}(\mathbb{N}) \subseteq M$.
Nach P5 gilt $M = \mathbb{N}$. Da $0$ nach P3 kein Nachfolger ist, folgt $\text{succ}(\mathbb{N}) = \mathbb{N} \setminus \{0\}$.

:::rechnung Beispiele für Satz 2.5
\text{succ}(0) = 1 || $1$ ist Nachfolger von $0$
\text{succ}(4) = 5 || $5$ ist Nachfolger von $4$
0 \notin \text{succ}(\mathbb{N}) || nur die $0$ hat keinen Vorgänger (P3)
:::

:::alt Als Stammbaum
In einer Familie ohne Adoption hat jeder einen Elternteil außer dem Urahn. P5 sagt: Wer einen Vorgänger hat, stammt vom
Urahn ab. Satz 2.5 folgert: Es gibt keine „Waisen“ außer dem Urahn selbst.
:::
""")

k.ordnen(r"Ordne den Beweis von Satz 2.5: $\text{succ}(\mathbb{N}) = \mathbb{N} \setminus \{0\}$.",
         [r"Setze $M := \{0\} \cup \text{succ}(\mathbb{N})$.",
          r"Dann ist $0 \in M$.",
          r"Außerdem gilt $\text{succ}(M) \subseteq \text{succ}(\mathbb{N}) \subseteq M$.",
          r"Nach P5 (Satz 2.4) ist also $M = \mathbb{N}$.",
          r"Da $0 \notin \text{succ}(\mathbb{N})$ nach P3, folgt $\text{succ}(\mathbb{N}) = \mathbb{N} \setminus \{0\}$. $\square$"],
         r"Der Trick ist die Wahl von $M$: Sie enthält die Null und ist abgeschlossen unter succ, damit P5 greift.",
         ablenker=[r"Setze $M := \mathbb{N} \setminus \{0\}$ und zeige $0 \in M$.",
                   r"Aus P4 folgt, dass jede Zahl einen Vorgänger hat."],
         tipps=["Zuerst muss die Menge $M$ definiert werden, auf die P5 angewendet wird.",
                r"P5 verlangt zwei Dinge von $M$: $n_0 \in M$ und $\text{succ}(M) \subseteq M$.",
                r"Am Schluss braucht man P3, um die $0$ aus $\text{succ}(\mathbb{N})$ auszuschließen."])

# ── Seite 5: Satz 2.6 ────────────────────────────────────────────────────
k.erklaerung("Vollständige Induktion (Satz 2.6)", r"""
## P5 als Beweismethode

Wie beweist man etwas für **alle** $n \in \mathbb{N}$? Man kann nicht jede Zahl einzeln prüfen.

**Satz 2.6 ([[vollständige Induktion]]).** Sei $E(n)$ eine [[Aussageform]] für $n \in \mathbb{N}$. Gelten
der [[Induktionsanfang]] $E(0)$ und der [[Induktionsschritt]] $\forall n \in \mathbb{N} : (E(n) \Rightarrow E(\text{succ}(n)))$,
dann gilt $E(n)$ für alle $n \in \mathbb{N}$.

*Beweis.* $M := \{n \in \mathbb{N} \mid E(n)\}$ enthält $0$ (Anfang) und ist unter succ abgeschlossen (Schritt). Nach P5 ist $M = \mathbb{N}$. $\square$

:::visual induktion_domino
{"anzahl": 8, "anfang": 0, "aussage": "$E(n)$ für $n = 0, 1, 2, \\ldots$",
 "text_anfang": "Induktionsanfang: $E(0)$ gilt, der erste Stein fällt.",
 "text_schritt": "Induktionsschritt: Aus $E(n)$ folgt $E(n+1)$, jeder Stein stößt den nächsten um.",
 "unterschrift": "Im Skript beginnt die Kette bei $n = 0$."}
:::

:::alt Als Rekursion
Eine rekursive Funktion `f(n)` ist korrekt, wenn der Basisfall `f(0)` stimmt (Induktionsanfang) und `f(n+1)` korrekt ist,
sobald `f(n)` korrekt ist (Induktionsschritt). Dann stimmt jeder Aufruf, auch für riesige $n$.
:::
""")

k.ordnen(r"Ordne den Beweis von Satz 2.6 (vollständige Induktion) mit $M := \{n \in \mathbb{N} \mid E(n)\}$.",
         [r"Setze $M := \{n \in \mathbb{N} \mid E(n)\}$, die Menge aller $n$, für die $E(n)$ gilt.",
          r"Nach dem Induktionsanfang gilt $E(0)$, also $0 \in M$.",
          r"Für $n \in M$ gilt $E(n)$, nach dem Induktionsschritt also $E(\text{succ}(n))$, das heißt $\text{succ}(n) \in M$.",
          r"Damit ist $\text{succ}(M) \subseteq M$, außerdem $M \subseteq \mathbb{N}$ und $0 \in M$.",
          r"Nach P5 gilt $M = \mathbb{N}$, also gilt $E(n)$ für alle $n \in \mathbb{N}$. $\square$"],
         r"Die Induktion ist P5 für die Menge $M$ aller Zahlen mit der Eigenschaft: Anfang liefert $0 \in M$, Schritt liefert $\text{succ}(M) \subseteq M$.",
         ablenker=[r"Für alle $n \in \mathbb{N}$ gelte $E(n)$ (Induktionsannahme).",
                   r"Wir prüfen $E(0), E(1), E(2), E(3)$. Es gilt jedes Mal, also gilt $E(n)$ immer."],
         tipps=["Der Beweis ist P5, angewendet auf eine passend gewählte Menge.",
                r"Welche zwei Eigenschaften muss $M$ haben, damit P5 anwendbar ist?",
                "Die Ablenker setzen die Behauptung voraus oder prüfen nur endlich viele Fälle."])

# ── Seite 6: Satz 2.7, Beispiel 2.8 ──────────────────────────────────────
k.erklaerung("Satz 2.7 und Beispiel 2.8", r"""
## Der Anfang gehört dazu

**Satz 2.7.** Für alle $n \in \mathbb{N}$ gilt $n \neq \text{succ}(n)$. Beweis mit $E(n) := (n \neq \text{succ}(n))$:

- **Induktionsanfang:** $0 \neq \text{succ}(0)$ wegen P3.
- **Induktionsannahme:** Sei $n \in \mathbb{N}$ mit $n \neq \text{succ}(n)$.
- **Induktionsschritt:** Da succ injektiv ist (P4), folgt $\text{succ}(n) \neq \text{succ}(\text{succ}(n))$, also $E(\text{succ}(n))$.

**Beispiel 2.8.** Der Schritt allein genügt nicht: Für $E'(n) := (n = \text{succ}(n))$ gilt der Schritt (aus $n = \text{succ}(n)$
folgt $\text{succ}(n) = \text{succ}(\text{succ}(n))$), aber $E'(0)$ ist falsch, und $E'(n)$ ist für **alle** $n$ falsch.

:::rechnung Schritt ohne Anfang
\text{Schritt: } n = \text{succ}(n) \Rightarrow \text{succ}(n) = \text{succ}(\text{succ}(n)) || mit dem Anwenden von succ auf beiden Seiten
\text{Anfang: } 0 \neq 1 = \text{succ}(0) || $E'(0)$ ist falsch: die Kette hat keinen ersten Stein
:::

:::alt Als Kartenhaus
Ein Kartenhaus, in dem jede Etage die nächste trägt, steht erst, wenn die unterste Etage steht. Der Schritt „Etage $n$ trägt
$n + 1$“ gilt auch in einem Haus, das nie gebaut wurde.
:::
""")

k.mc(r"Welche Aussageform zeigt, dass der Induktionsschritt ohne Induktionsanfang nichts beweist (Beispiel 2.8)?",
     [r"$E'(n) := (n = \text{succ}(n))$: Der Schritt gilt, aber $E'(0)$ ist falsch",
      r"$E(n) := (n \neq \text{succ}(n))$: Der Anfang fehlt",
      r"$E''(n) := (n \leq \text{succ}(n))$: Der Schritt gilt nicht",
      r"Keine: Der Schritt allein genügt immer"],
     r"Bei $E'(n) = (n = \text{succ}(n))$ folgt aus $n = \text{succ}(n)$ durch Anwenden von succ auf beiden Seiten $\text{succ}(n) = \text{succ}(\text{succ}(n))$. "
     r"Trotzdem gilt $E'(n)$ für kein $n$, weil schon $E'(0)$ scheitert.",
     tipps=["Gesucht ist eine Aussage, die für jedes $n$ falsch ist, bei der aber der Schritt „wenn $E(n)$, dann $E(n+1)$“ stimmt.",
            r"Eine falsche Voraussetzung impliziert alles.", r"Betrachte $n = \text{succ}(n)$."],
     fehler={r"$E(n) := (n \neq \text{succ}(n))$: Der Anfang fehlt": r"Bei $E(n) = (n \neq \text{succ}(n))$ ist der Anfang gerade **gezeigt** (Satz 2.7). Gesucht ist eine falsche Aussage.",
             r"$E''(n) := (n \leq \text{succ}(n))$: Der Schritt gilt nicht": r"Die Aussage $n \le \text{succ}(n)$ ist wahr. Sie zeigt nichts über einen fehlenden Anfang.",
             "Keine: Der Schritt allein genügt immer": "Genau das widerlegt Beispiel 2.8: Ohne Anfang sind alle Steine umgefallen, bevor der erste fällt, also nie."})

k.wf(r"Gilt $\forall n \in \mathbb{N} : (E(n) \Rightarrow E(n+1))$, dann gilt $E(n)$ für alle $n \in \mathbb{N}$.", False,
     r"Falsch. Es fehlt der Induktionsanfang $E(0)$. Gegenbeispiel: $E'(n) := (n = n + 1)$ erfüllt den Schritt (aus Falschem folgt alles) und ist für jedes $n$ falsch.",
     tipps=["Fehlt etwas zum Beweisprinzip in Satz 2.6?"])

# ── Seite 7: Satz 2.35 ───────────────────────────────────────────────────
k.erklaerung("Induktion in Aktion: Satz 2.35", r"""
## Eine Summenformel

**Satz 2.35.** Für alle $n \ge 1$ gilt $\sum_{i=1}^{n} 2i = n(n+1)$.

Der Beweis im Skript hat drei Teile: den Anfang für $n = 1$, die Annahme für ein festes $n$ und den Schritt auf $n + 1$.
Das ist Beobachtung 2.9 (ii): ein Startwert ungleich $0$.

:::rechnung Beweis von Satz 2.35
\sum_{i=1}^{1} 2i = 2 = 1 \cdot (1 + 1) || Induktionsanfang $n = 1$
\sum_{i=1}^{n+1} 2i = \sum_{i=1}^{n} 2i + 2(n+1) || Schritt: letzten Summanden abspalten
n(n+1) + 2(n+1) = (n+1)(n+2) || Induktionsannahme eingesetzt, dann $(n+1)$ ausklammern (Distributivität)
:::

Die rechte Seite ist die Formel für $n + 1$, denn $(n+1)((n+1)+1) = (n+1)(n+2)$.

:::alt Mit Gauß in Paaren
Schreibe $2 + 4 + \ldots + 2n$ vorwärts und rückwärts untereinander. Jede Spalte hat die Summe $2n + 2$, und es gibt $n$ Spalten.
Beide Zeilen zusammen ergeben $n(2n+2)$, eine Zeile also $n(n+1)$. Die Induktion zeigt dasselbe ohne Trick.
:::
""")

k.ordnen(r"Ordne den Induktionsbeweis von Satz 2.35: $\sum_{i=1}^{n} 2i = n(n+1)$ für $n \ge 1$.",
         [r"Wir beweisen die Aussage per Induktion über $n \ge 1$.",
          r"Induktionsanfang: Für $n = 1$ ist $\sum_{i=1}^{1} 2i = 2 = 1 \cdot (1 + 1)$.",
          r"Induktionsannahme: Für ein $n \ge 1$ gelte $\sum_{i=1}^{n} 2i = n(n+1)$.",
          r"Induktionsschritt: $\sum_{i=1}^{n+1} 2i = \sum_{i=1}^{n} 2i + 2(n+1)$.",
          r"Mit der Induktionsannahme folgt $\sum_{i=1}^{n+1} 2i = n(n+1) + 2(n+1) = (n+1)(n+2)$.",
          r"Das ist die Formel für $n + 1$. Also gilt die Aussage für alle $n \ge 1$. $\square$"],
         "Reihenfolge: Ankündigung, Anfang, Annahme, Schritt (Summand abspalten, Annahme einsetzen, umformen), Schluss.",
         ablenker=[r"Induktionsannahme: Für alle $n \ge 1$ gelte $\sum_{i=1}^{n} 2i = n(n+1)$.",
                   r"Wir setzen $n + 1$ ein: $\sum_{i=1}^{n+1} 2i = (n+1)(n+2)$ stimmt, weil beide Seiten gleich sind."],
         tipps=["Der Beweis beginnt mit der Ankündigung der Methode und endet mit dem Schluss für alle $n$.",
                "Die Annahme gilt für **ein** festes $n$. Wer sie für alle $n$ annimmt, nimmt die Behauptung an.",
                "Im Schritt kommt die Annahme genau bei „$n(n+1)$“ ins Spiel."])

k.luecke(r"Induktionsschritt zu Satz 2.35. Aus der Annahme $\sum_{i=1}^{n} 2i = n(n+1)$ folgt: Fülle die Lücken.",
         r"\sum_{i=1}^{n+1} 2i = n(n+1) + \luecke = (n+1) \cdot (\luecke)",
         [["2(n+1)"], ["n+2"]],
         r"Der abgespaltene Summand ist $2(n+1)$. Dann ist $n(n+1) + 2(n+1) = (n+1)(n+2)$: Ausklammern von $(n+1)$ lässt $n + 2$ übrig.",
         tipps=[r"Der letzte Summand gehört zu $i = n + 1$.", r"Klammere $(n+1)$ aus: $(n+1) \cdot (n + \ldots)$.", r"$n + 2$"],
         rechenweg=r"""
:::rechnung
2(n+1) || letzter Summand für $i = n + 1$
n(n+1) + 2(n+1) = (n+1)(n+2) || $(n+1)$ ausklammern
:::
""",
         typische_fehler=[(["2n", "n+1"], r"Für $i = n + 1$ ist der Summand $2(n+1)$, nicht $2n$. Der Summand $2n$ steckt schon in der Summe bis $n$."),
                          (["2(n+1)", "n+1"], r"Nach dem Ausklammern bleibt $n + 2$ übrig: $n(n+1) + 2(n+1) = (n+1)(n+2)$.")])

# ── Seite 8: Satz 2.34 ───────────────────────────────────────────────────
k.erklaerung("Satz 2.34: Multiplikation als wiederholte Addition", r"""
## Induktion mit einer Konstanten

**Satz 2.34.** Für alle $n, a \in \mathbb{N}$ mit $n \ge 1$ gilt $\sum_{i=1}^{n} a = a \cdot n$.

Die Summe hat $n$ gleiche Summanden $a$. Das Skript beweist die Aussage über $n$ ($a$ bleibt fest). Die Multiplikation $a \cdot n$
ist erst in Abschnitt 2.5 definiert, hier genügt die Schulregel $a \cdot (n+1) = a \cdot n + a$ (Satz 2.29).

:::rechnung Beweis von Satz 2.34
\sum_{i=1}^{1} a = a = a \cdot 1 || Induktionsanfang $n = 1$
\sum_{i=1}^{n+1} a = a + \sum_{i=1}^{n} a || Schritt: einen Summanden abspalten
a + a \cdot n = a \cdot (n + 1) || Induktionsannahme eingesetzt, Nachfolgerregel (Satz 2.29)
:::

Zahlenprobe für $a = 7$, $n = 4$: $7 + 7 + 7 + 7 = 28 = 7 \cdot 4$.

:::alt Mit Gleisen
Du legst $n$ gleich lange Gleisstücke der Länge $a$ hintereinander. Kommt ein Stück dazu, wird die Strecke um $a$ länger.
Genau das ist $a \cdot (n+1) = a \cdot n + a$.
:::
""")

k.zahl(r"Satz 2.34 mit $a = 7$ und $n = 4$: Berechne $\sum_{i=1}^{4} 7$.", 28,
       r"Vier Summanden $7$: $7 + 7 + 7 + 7 = 28 = 7 \cdot 4$. Man muss nicht addieren, sondern darf $a \cdot n$ rechnen.",
       tipps=["Wie viele Summanden stehen da, und wie groß ist jeder?", r"Satz 2.34: $\sum_{i=1}^{n} a = a \cdot n$", r"$7 \cdot 4$"],
       rechenweg=r"""
:::rechnung
7 + 7 + 7 + 7 = 28 || vier gleiche Summanden
7 \cdot 4 = 28 || Satz 2.34
:::
""",
       typische_fehler=[(11, "Du hast $a + n = 7 + 4$ gerechnet. Die Summe hat $n$ Summanden, jeder ist $a$: also $a \\cdot n$."),
                        (7, r"Die Summe läuft über $i = 1, \ldots, 4$, und der Summand $7$ hängt nicht von $i$ ab. Er wird viermal addiert.")])

# ── Seite 9: Beobachtung 2.9 ─────────────────────────────────────────────
k.erklaerung("Abwandlungen der Induktion (Beobachtung 2.9)", r"""
## Drei Varianten

**(i) Starke Induktion.** Als Annahme nimmst du $F(m)$ für **alle** $m \le n$. Nützlich, wenn $F(n+1)$ von beliebigen kleineren Fällen abhängt, etwa „jedes $n \ge 2$ ist ein Produkt von Primzahlen“.

**(ii) Anderer Startwert $n_0$.** Für alle $n \ge n_0$ nimmst du $E(n) := F(n_0 + n)$.

**(iii) Teilmenge $M \neq \mathbb{N}$.** Mit einer Bijektion $f\colon \mathbb{N} \to M$ setzt du $E(n) := F(f(n))$.

:::rechnung Varianten (ii) und (iii) in Zahlen
0 + 3 = 3 || (ii) mit $n_0 = 3$: $E(0) = F(3)$ ist der Anfang
1 + 3 = 4 || $E(1) = F(4)$
2 \cdot 0 + 1 = 1 || (iii) mit $f(n) = 2n + 1$ für die ungeraden Zahlen: $E(0) = F(1)$
2 \cdot 3 + 1 = 7 || $E(3) = F(7)$: jede ungerade Zahl wird genau einmal getroffen (bijektiv)
:::

:::alt Mit Treppen verschiedener Länge
(ii) Eine Treppe, die erst im zweiten Stock beginnt: Du steigst dort ein und gehst Stufe für Stufe nach oben. (iii) Eine Treppe, die
nur jede zweite Stufe hat: Du nummerierst die vorhandenen Stufen $0, 1, 2, \ldots$ neu und steigst auf der Neunummerierung.
:::
""")

k.mc(r"Du willst zeigen: Jedes $n \ge 2$ ist ein Produkt von Primzahlen. Warum braucht man dafür die starke Induktion (Beob. 2.9 (i))?",
     [r"Ist $n + 1 = a \cdot b$ mit $a, b \ge 2$, liegen $a$ und $b$ irgendwo unterhalb von $n + 1$, nicht nur bei $n$",
      r"Weil $n + 1$ immer eine Primzahl ist",
      r"Weil der Induktionsanfang sonst falsch wäre",
      r"Weil die normale Induktion nur für gerade $n$ funktioniert"],
     r"Die Faktoren $a, b$ von $n + 1$ sind kleiner als $n + 1$, aber nicht unbedingt gleich $n$. Darum braucht der Schritt die Aussage für **alle** kleineren Zahlen.",
     tipps=[r"Schreibe $12 = 3 \cdot 4$. Welche kleineren Zahlen werden benutzt?", r"Ist $n$ ein Faktor von $n + 1$?",
            "Die Annahme muss alle möglichen Faktoren abdecken."],
     fehler={r"Weil $n + 1$ immer eine Primzahl ist": r"Nein, $n + 1 = 12$ zum Beispiel ist es nicht. Und wäre es immer eine Primzahl, gäbe es nichts zu zerlegen.",
             r"Weil der Induktionsanfang sonst falsch wäre": "Der Anfang $n = 2$ ist bei beiden Varianten dieselbe Rechnung. Der Unterschied liegt in der Annahme.",
             r"Weil die normale Induktion nur für gerade $n$ funktioniert": "Normale Induktion hat nichts mit gerade oder ungerade zu tun."})

# ── Seite 10: Teilbarkeit ────────────────────────────────────────────────
k.erklaerung("Teilbarkeit per Induktion", r"""
## Ohne Subtraktion in $\mathbb{N}$

In $\mathbb{N}$ gibt es noch keine negativen Zahlen. Statt „$3 \mid 4^n - 1$“ schreibst du: Es gibt $k \in \mathbb{N}$ mit $4^n = 3k + 1$.

**Behauptung.** Für alle $n \in \mathbb{N}$ gibt es $k \in \mathbb{N}$ mit $4^n = 3k + 1$.

- **Anfang** ($n = 0$): $4^0 = 1 = 3 \cdot 0 + 1$ mit $k = 0$.
- **Annahme:** Für ein $n$ gelte $4^n = 3k + 1$ mit einem $k \in \mathbb{N}$.
- **Schritt:** $4^{n+1} = 4 \cdot 4^n$ und dann die Annahme einsetzen.

:::rechnung Der Schritt
4^{n+1} = 4 \cdot 4^n || Potenzgesetz
4 \cdot (3k + 1) = 12k + 4 || Annahme eingesetzt
12k + 4 = 3(4k + 1) + 1 || $3$ herausziehen: $12k + 3 + 1$
:::

Mit $k' := 4k + 1 \in \mathbb{N}$ gilt $4^{n+1} = 3k' + 1$.

:::alt Als Tabelle
$4^0 = 1$, $4^1 = 4 = 3 \cdot 1 + 1$, $4^2 = 16 = 3 \cdot 5 + 1$, $4^3 = 64 = 3 \cdot 21 + 1$. Das neue $k'$ ist immer vier mal das alte plus eins: $1 \to 5 \to 21$.
:::
""")

k.luecke(r"Ergänze den Schritt: Aus $4^n = 3k + 1$ folgt $4^{n+1} = 4(3k + 1) = 3 \cdot (\luecke) + 1$.",
         r"4^{n+1} = 4(3k+1) = 3 \cdot (\luecke) + 1",
         [["4k+1"]],
         r"$4(3k + 1) = 12k + 4 = 12k + 3 + 1 = 3(4k + 1) + 1$. Das neue $k' = 4k + 1$ liegt in $\mathbb{N}$.",
         tipps=[r"Multipliziere $4(3k + 1)$ aus.", r"$12k + 4$ lässt sich als $3 \cdot \ldots + 1$ schreiben: $4 = 3 + 1$.", r"$12k + 3 = 3(4k + 1)$"],
         rechenweg=r"""
:::rechnung
4(3k + 1) = 12k + 4 || ausmultiplizieren
12k + 4 = 3(4k + 1) + 1 || $12k + 3 = 3(4k+1)$ und $+1$ bleibt
:::
""",
         typische_fehler=[(["4k"], r"$3 \cdot 4k + 1 = 12k + 1 \neq 12k + 4$. Es fehlt noch $3$ in der Klammer."),
                          (["k+1"], r"$3(k + 1) + 1 = 3k + 4 \neq 12k + 4$. Der Faktor $4$ muss mit.")])



# ── Praxis ────────────────────────────────────────────────────────────────
def rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def peano_modell_pruefen(rng):
    m = rng.choice([4, 5])
    while True:
        succ = {x: rng.randrange(m) for x in range(m)}
        verl, erreicht = peano_verletzt(m, succ)
        if 1 <= len(verl) <= 2:
            break
    tab = ", ".join(f"\\text{{succ}}({x}) = {succ[x]}" for x in range(m))
    namen = {"P3": "P3: die Null ist kein Nachfolger", "P4": "P4: succ ist injektiv",
             "P5": "P5: es gibt keine überflüssigen Elemente"}
    bild = sorted(set(succ.values()))
    doppelt = next(((a, b) for a in range(m) for b in range(a + 1, m) if succ[a] == succ[b]), None)
    nicht_erreicht = sorted(set(range(m)) - erreicht)
    erkl = {"P3": f"Es gibt $x$ mit $\\text{{succ}}(x) = 0$: P3 gilt nicht." if "P3" in verl else
            f"Kein $x$ hat den Nachfolger $0$, die Bilder sind ${', '.join(str(b) for b in bild)}$: P3 gilt.",
            "P4": (f"$\\text{{succ}}({doppelt[0]}) = \\text{{succ}}({doppelt[1]}) = {succ[doppelt[0]]}$: P4 gilt nicht." if doppelt else
                   "Alle Nachfolger sind verschieden: P4 gilt."),
            "P5": (f"Von $0$ aus erreichst du ${', '.join(str(x) for x in sorted(erreicht))}$, nicht aber "
                   f"${', '.join(str(x) for x in nicht_erreicht)}$: P5 gilt nicht." if nicht_erreicht else
                   "Von $0$ aus erreichst du alle Elemente: P5 gilt.")}
    zeilen = []
    for a in ("P3", "P4", "P5"):
        zeilen.append((f"\\text{{{a}: {'verletzt' if a in verl else 'erfüllt'}}}", erkl[a]))
    return {
        "frage": f"Gegeben ist $N = \\{{0, \\ldots, {m - 1}\\}}$ mit $n_0 = 0$ und ${tab}$. P1 und P2 gelten. "
                 "Welche der folgenden Axiome sind **verletzt**?",
        "richtig": [namen[a] for a in verl],
        "falsch": [namen[a] for a in ("P3", "P4", "P5") if a not in verl],
        "fehler": {namen[a]: erkl[a] for a in ("P3", "P4", "P5") if a not in verl},
        "tipps": ["P3: Kommt die $0$ unter den Nachfolgern vor? P4: Haben zwei Zahlen denselben Nachfolger?",
                  "P5: Folge den Nachfolgern ab $0$ und schreibe alle erreichten Zahlen auf.",
                  "Eine Zahl, die du von $0$ aus nie erreichst, ist überflüssig (P5)."],
        "rechenweg": rechnung(zeilen),
        "erklaerung": "Jedes Axiom prüfst du einzeln: P3 am Bild von succ, P4 an gleichen Bildern, P5 durch Weiterzählen ab $0$.",
    }


def _lin(a, b, v):
    s = ("" if a == 1 else str(a)) + v
    return s + (f" + {b}" if b else "")


def induktion_schritt_summe(rng):
    a, b = rng.choice([1, 2, 3, 4, 5, 6]), rng.choice([0, 1, 2, 3])
    if (a, b) == (1, 0):
        b = 2
    for n in range(1, 40):
        assert sum(a * i + b for i in range(1, n + 1)) * 2 == a * n * (n + 1) + 2 * b * n
    ca = "" if a == 1 else str(a)
    letzter, ziel = f"{ca}(n+1)" + (f" + {b}" if b else ""), f"{ca}(n+1)(n+2)/2" + (f" + {b}(n+1)" if b else "")
    letzter_text = letzter.replace("(n+1)", "(n + 1)")
    Fn = f"\\frac{{{a if a != 1 else ''}n(n+1)}}{{2}}" + (f" + {b}n" if b else "")
    Fn1 = f"\\frac{{{a if a != 1 else ''}(n+1)(n+2)}}{{2}}" + (f" + {b}(n+1)" if b else "")
    summand = _lin(a, b, "i")
    loesung = [[letzter], [ziel]]
    fehler = [([[f"{ca}n" + (f" + {b}" if b else "")], [ziel]], "Der abgespaltene Summand gehört zu $i = n + 1$, nicht zu $i = n$."),
              ([[letzter], [f"{ca}n(n+1)/2" + (f" + {b}n" if b else "")]],
               "Rechts muss die Formel mit $n + 1$ statt $n$ stehen. Ersetze **jedes** $n$ durch $n + 1$.")]
    return {
        "frage": f"Induktionsschritt für $\\sum_{{i=1}}^{{n}} ({summand}) = {Fn}$. Spalte den letzten Summanden ab, setze die "
                 "Induktionsannahme ein und gib an, was am Ende herauskommen muss.",
        "formel": f"\\sum_{{i=1}}^{{n+1}} ({summand}) = {Fn} + \\luecke = \\luecke",
        "antworten": loesung,
        "tipps": ["Der abgespaltene Summand ist der für $i = n + 1$.", f"Er lautet ${letzter_text}$.",
                  f"Rechts steht die Formel ${Fn}$ mit $n + 1$ statt $n$, also ${Fn1}$."],
        "rechenweg": rechnung([(f"{Fn} + {letzter_text} = {Fn1}", "Annahme eingesetzt und umgeformt (der Selbsttest prüft das als Termgleichung)")]),
        "erklaerung": "Im Schritt: Summe bis $n + 1$ = Summe bis $n$ plus letzter Summand. Dann die Annahme einsetzen und zur Formel für $n + 1$ umformen.",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


def induktion_teilbarkeit_schritt(rng):
    m, n = rng.choice([3, 4, 5, 6, 7]), rng.randint(1, 4)
    K = (m ** n - 1) // (m - 1)
    assert m ** n == (m - 1) * K + 1
    K2 = m * K + 1
    assert m ** (n + 1) == (m - 1) * K2 + 1
    fehler = [(m * K, f"Du hast $m \\cdot ((m-1)K)$ gebildet und das $+1$ vergessen. $m \\cdot ((m-1)K + 1) = (m-1) \\cdot mK + m$, und $m = (m-1) + 1$."),
              (K + 1, f"Die Annahme muss mit $m = {m}$ multipliziert werden: $m^{{n+1}} = m \\cdot m^n$."),
              ((m - 1) * K + 1, f"Das ist $m^{{n}}$, nicht der Faktor $k'$ für $m^{{n+1}}$.")]
    return {
        "frage": f"Für $n = {n}$ gilt $m^n = (m - 1) \\cdot k + 1$ mit $m = {m}$ und $k = {K}$ (also ${m}^{{{n}}} = {m ** n}$). "
                 f"Welches $k' \\in \\mathbb{{N}}$ erfüllt dann ${m}^{{{n + 1}}} = {m - 1} \\cdot k' + 1$? (Induktionsschritt)",
        "loesung": K2,
        "tipps": [f"Schreibe ${m}^{{{n + 1}}} = {m} \\cdot {m}^{{{n}}}$ und setze ${m}^{{{n}}} = {m - 1} \\cdot {K} + 1$ ein.",
                  f"${m} \\cdot ({m - 1} \\cdot {K} + 1) = {m - 1} \\cdot {m * K} + {m}$.",
                  f"Es ist ${m} = {m - 1} + 1$, also bleibt $+1$ übrig und $k' = {m} \\cdot {K} + 1$."],
        "rechenweg": rechnung([(f"{m} \\cdot ({m - 1} \\cdot {K} + 1) = {m ** (n + 1)} = {m - 1} \\cdot {K2} + 1",
                                f"Allgemein: $m((m-1)k+1) = (m-1) \\cdot mk + m = (m-1)(mk+1) + 1$, also $k' = mk + 1 = {K2}$")]),
        "erklaerung": "Im Schritt: $m^{n+1} = m \\cdot m^n = m((m-1)k + 1) = (m-1)(mk + 1) + 1$. Das neue $k'$ ist $m k + 1$.",
        "typische_fehler": ohne_gleiche(K2, fehler),
    }


k.praxis()

k.generator(peano_modell_pruefen, typ="mehrfach", titel="Peano-Axiome an einer Struktur prüfen")
k.generator(induktion_schritt_summe, typ="luecke", titel="Induktionsschritt einer Summenformel")
k.generator(induktion_teilbarkeit_schritt, typ="zahl", titel="Induktionsschritt bei Teilbarkeit", glatt=False)

k.mc("Ein Beweis zeigt: „In jeder Menge von $n$ Pferden haben alle Pferde dieselbe Farbe.“ Anfang $n = 1$: Ein Pferd hat eine Farbe. "
     "Schritt $n \\to n + 1$: Bei $n + 1$ Pferden lass das erste Pferd weg, die übrigen $n$ haben dieselbe Farbe, lass das letzte weg, "
     "wieder dieselbe Farbe, also alle. Wo steckt der Fehler?",
     [r"Beim Schritt von $n = 1$ auf $n = 2$: Die beiden Teilmengen mit einem Pferd haben kein gemeinsames Pferd",
      r"Der Induktionsanfang fehlt",
      r"Die Induktionsannahme wird für alle $n$ vorausgesetzt",
      r"Induktion funktioniert nicht für Mengen von Tieren"],
     r"Der Beweis nimmt stillschweigend an, dass sich die beiden Teilmengen überlappen. Für $n = 1$ ist das falsch. "
     r"Der Schritt $E(n) \Rightarrow E(n+1)$ ist also nicht für **alle** $n \in \mathbb{N}$ gezeigt: Er ist für $n = 1$ falsch.",
     tipps=["Teste den Schritt mit konkreten kleinen Zahlen: $n = 1$ und $n + 1 = 2$ Pferde.",
            "Haben die beiden Teilmengen mit je einem Pferd ein Pferd gemeinsam?",
            "Der Schritt muss für jedes $n$ gelten, nicht nur für große."],
     fehler={r"Der Induktionsanfang fehlt": "Der Anfang ist da und stimmt: Ein Pferd hat eine Farbe.",
             r"Die Induktionsannahme wird für alle $n$ vorausgesetzt": "Die Annahme gilt hier nur für ein festes $n$, das ist korrekt formuliert.",
             r"Induktion funktioniert nicht für Mengen von Tieren": "Induktion funktioniert für jede Aussage $E(n)$, wenn Anfang und Schritt wirklich stimmen."})

k.rechenweg_aufgabe(r"""
## Quiz-Stil: Summe der ungeraden Zahlen

Behauptung $E(n)$: $\sum_{i=0}^{n} (2i + 1) = (n + 1)^2$ für alle $n \in \mathbb{N}$.
""",
    [{"typ": "zahl", "frage": r"Induktionsanfang: Welchen Wert haben beide Seiten von $E(0)$?", "loesung": 1,
      "tipps": [r"Für $n = 0$ besteht die Summe nur aus dem Summanden $i = 0$.", r"Rechte Seite: $(0 + 1)^2$."],
      "rechenweg": r"Links $2 \cdot 0 + 1 = 1$, rechts $(0+1)^2 = 1$.",
      "erklaerung": "Beide Seiten sind gleich $1$.",
      "typische_fehler": [(0, "Die Summe läuft ab $i = 0$ und enthält den Summanden $2 \\cdot 0 + 1 = 1$.")]},
     {"typ": "term", "frage": r"Schritt $n \to n + 1$: Welcher Summand wird abgespalten, also $\sum_{i=0}^{n+1} (2i+1) = \sum_{i=0}^{n} (2i+1) + \ldots$?",
      "loesung": "2n+3", "variablen": "n", "tipps": [r"Setze $i = n + 1$ in $2i + 1$ ein.", r"$2(n+1) + 1$"],
      "rechenweg": r"$2(n + 1) + 1 = 2n + 3$.", "erklaerung": "Für $i = n + 1$ ist der Summand $2(n+1) + 1 = 2n + 3$.",
      "typische_fehler": [("2n+1", r"Das ist der Summand für $i = n$. Er steckt schon in der Summe bis $n$.")]},
     {"typ": "term", "frage": r"Setze die Annahme ein: $(n+1)^2 + (2n+3)$ ist ein Quadrat. Welches?", "loesung": "(n+2)^2",
      "variablen": "n", "form": "faktorisiert", "tipps": [r"Multipliziere $(n+1)^2$ aus.", r"$n^2 + 4n + 4$", "Erste binomische Formel."],
      "rechenweg": r"$(n+1)^2 + 2n + 3 = n^2 + 2n + 1 + 2n + 3 = n^2 + 4n + 4 = (n+2)^2$.",
      "erklaerung": "Das ist genau $((n+1)+1)^2$, die rechte Seite von $E(n+1)$.",
      "typische_fehler": [("(n+1)^2", r"Der Summand $2n + 3$ ist verschwunden.")]}],
    r"Damit gilt $E(0)$ und $E(n) \Rightarrow E(n+1)$, also $E(n)$ für alle $n \in \mathbb{N}$ (Satz 2.6).",
    uebungsblatt=True,
    tipps=["Schreibe E(n+1) auf, bevor du rechnest: Du willst bei $(n+2)^2$ ankommen.", "Die Annahme ersetzt die Summe bis $n$ durch $(n+1)^2$."],
    rechenweg=r"""
:::rechnung
(n+1)^2 + 2n + 3 = n^2 + 4n + 4 || Annahme eingesetzt und ausmultipliziert
n^2 + 4n + 4 = (n+2)^2 || erste binomische Formel
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Induktion

1. Zeigen Sie per vollständiger Induktion: Für alle $n \in \mathbb{N}$ gilt $2 \cdot \sum_{i=0}^{n} (3i + 1) = (n+1)(3n+2)$.
2. Zeigen Sie mit starker Induktion (Beobachtung 2.9 (i)): Jedes $n \in \mathbb{N}$ mit $n \ge 2$ ist ein Produkt von Primzahlen.
   (Eine Primzahl zählt als Produkt mit einem Faktor.)
""",
    r"""
**1. Anfang** ($n = 0$): Links $2 \cdot (3 \cdot 0 + 1) = 2$, rechts $1 \cdot 2 = 2$ ✓.
**Annahme:** Für ein festes $n \in \mathbb{N}$ gelte $2 \sum_{i=0}^{n} (3i+1) = (n+1)(3n+2)$.
**Schritt:** $2 \sum_{i=0}^{n+1} (3i+1) = 2 \sum_{i=0}^{n} (3i+1) + 2(3(n+1)+1)$, also nach Annahme
$= (n+1)(3n+2) + 2(3n+4) = 3n^2 + 5n + 2 + 6n + 8 = 3n^2 + 11n + 10 = (n+2)(3n+5) = ((n+1)+1)(3(n+1)+2)$.
Das ist die Aussage für $n + 1$. Nach Satz 2.6 gilt sie für alle $n \in \mathbb{N}$. $\square$

**2.** Sei $n \ge 2$ und die Aussage gelte für alle $m$ mit $2 \le m < n$ (starke Annahme).
*Fall 1:* $n$ ist Primzahl: Produkt mit einem Faktor.
*Fall 2:* $n$ ist keine Primzahl. Dann gibt es einen Teiler $a$ mit $1 < a < n$, also $n = a \cdot b$ mit $2 \le a, b < n$.
Nach der Annahme sind $a$ und $b$ Produkte von Primzahlen, also auch $n = a \cdot b$. Der Anfang $n = 2$ ist Fall 1. $\square$
""",
    ["Anfang bei $n = 0$ (nicht $n = 1$) nachgerechnet",
     "Induktionsannahme nur für ein festes $n$ formuliert und im Schritt benutzt",
     "Den abgespaltenen Summanden $2(3(n+1)+1) = 2(3n+4)$ richtig bestimmt und ausmultipliziert",
     "In Aufgabe 2 die Annahme für alle $m < n$ formuliert (starke Induktion)",
     "In Aufgabe 2 beide Fälle (prim, nicht prim) behandelt und $a, b < n$ begründet"],
    r"Der Schritt ist immer: Summand für $n + 1$ abspalten, Annahme einsetzen, auf die Form für $n + 1$ umformen. Bei starker Induktion brauchst du die Annahme für alle kleineren Zahlen.",
    uebungsblatt=True,
    tipps=[r"Schreibe zuerst die Behauptung für $n + 1$ auf: $(n+2)(3n+5)$.", "Wo die Annahme eingeht, markierst du sie mit „(IA)“ am Gleichheitszeichen.",
           "Bei 2: Zerlege $n = a \\cdot b$, wenn $n$ keine Primzahl ist."])

k.zusammenfassung(r"""
## Natürliche Zahlen und vollständige Induktion (Skript Abschn. 2.1 und 2.2)

| Axiom (Def. 2.1) | Inhalt |
|---|---|
| P1 | $n_0 \in N$ (Null) |
| P2 | $\text{succ}\colon N \to N$ ist eine Abbildung |
| P3 | $\text{succ}(n) \neq n_0$ (die Null ist kein Nachfolger) |
| P4 | succ ist injektiv |
| P5 | $M \subseteq N$, $n_0 \in M$, $\text{succ}(M) \subseteq M$ $\Rightarrow$ $M = N$ |

- **ℕ aus Mengen** (Def. 2.2): $0 := \emptyset$, $\text{succ}(n) = n \cup \{n\}$, jede Zahl ist die Menge der vorigen. $\le\ :=\ \subseteq$ (Def. 2.3). Satz 2.4: Das erfüllt P1 bis P5.
- **Satz 2.5:** $\text{succ}(\mathbb{N}) = \mathbb{N} \setminus \{0\}$.
- **Vollständige Induktion** (Satz 2.6): $E(0)$ und $\forall n : (E(n) \Rightarrow E(\text{succ}(n)))$ liefern $E(n)$ für alle $n \in \mathbb{N}$.
- **Der Schritt allein genügt nicht** (Bsp. 2.8): $E'(n) := (n = \text{succ}(n))$.
- **Satz 2.7:** $n \neq \text{succ}(n)$. **Satz 2.34:** $\sum_{i=1}^{n} a = a \cdot n$. **Satz 2.35:** $\sum_{i=1}^{n} 2i = n(n+1)$.
- **Abwandlungen** (Beob. 2.9): (i) starke Induktion, (ii) Startwert $n_0$, (iii) Bijektion $\mathbb{N} \to M$.

!! Aufbau jedes Beweises: Anfang, Annahme für **ein** festes $n$, Schritt (Annahme benutzen!), Schluss für alle $n$.
""")
