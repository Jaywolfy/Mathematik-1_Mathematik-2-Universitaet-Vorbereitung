# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 7: Äquivalenzrelationen (Skript Disser WS 26/27, Abschn. 1.6, Def. 1.59 bis Bsp. 1.65)."""
import json
from itertools import product

from ..engine import neues_kapitel

k = neues_kapitel(
    slug="aequivalenzrelationen",
    titel="Äquivalenzrelationen",
    beschreibung="Äquivalenzrelation, Äquivalenzklassen, Zerlegung (Satz 1.63), Faktormenge, Q als Faktormenge der Brüche",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 1.6",
    icon="🧩")


# ── Hilfsfunktionen: Python rechnet Eigenschaften und Klassen ─────────────
def rel(m, regel):
    return {(x, y) for x in m for y in m if regel(x, y)}


def ist_refl(m, r):
    return all((x, x) in r for x in m)


def ist_sym(m, r):
    return all((y, x) in r for x, y in r)


def ist_trans(m, r):
    return all((x, z) in r for x, y in r for y2, z in r if y == y2)


def ist_aequ(m, r):
    return ist_refl(m, r) and ist_sym(m, r) and ist_trans(m, r)


def klasse(m, r, a):
    return frozenset(x for x in m if (x, a) in r)


def faktormenge(m, r):
    return {klasse(m, r, a) for a in m}


def mtext(s):
    return "{" + "; ".join(str(x) for x in sorted(s)) + "}"


def mtex(s):
    return "\\emptyset" if not s else "\\{" + ", ".join(str(x) for x in sorted(s)) + "\\}"


def fam_key(f):
    return sorted(f, key=lambda a: (min(a), len(a), sorted(a)))


def fam_text(f):
    return "{" + "; ".join(mtext(a) for a in fam_key(f)) + "}"


def fam_tex(f):
    return "\\{" + ", ".join(mtex(a) for a in fam_key(f)) + "\\}"


# Beispiel 1.60 nachrechnen
_M = [-1, 1, 2, 3, 4]
_vz = lambda x: (x > 0) - (x < 0)
_R1 = rel(_M, lambda x, y: x == y)
_R2 = rel(_M, lambda x, y: x % 2 == y % 2)
_R3 = rel(_M, lambda x, y: _vz(x) == _vz(y))
_R4 = rel(_M, lambda x, y: x % 2 == y % 2 and _vz(x) == _vz(y))
assert all(ist_aequ(_M, r) for r in (_R1, _R2, _R3, _R4))
assert (len(_R1), len(_R2), len(_R3), len(_R4)) == (5, 13, 17, 9)
_KL = {n: {a: klasse(_M, r, a) for a in _M} for n, r in enumerate((_R1, _R2, _R3, _R4), 1)}
assert _KL[2][1] == frozenset({-1, 1, 3}) and _KL[3][2] == frozenset({1, 2, 3, 4})
_TAB = "\n".join(f"| $\\sim_{n}$ | " + " | ".join(f"${mtex(_KL[n][a])}$" for a in _M) + " |" for n in (1, 2, 3, 4))
def _klassen_bild(n):
    """Abbildung 1.4: Relation ~n auf M als Graph, Elemente nach Klassen gruppiert und eingefärbt."""
    kl = sorted({tuple(sorted(_KL[n][a])) for a in _M}, key=lambda k: k[0])
    return ":::visual aequivalenz_klassen\n" + json.dumps({
        "klassen": [list(k) for k in kl], "graph": True, "titel": f"$\\sim_{n}$ auf $M$"}, ensure_ascii=False) + "\n:::"


_BILDER = "\n\n".join(_klassen_bild(n) for n in (1, 2, 3, 4))
_ANZ = {n: len(faktormenge(_M, r)) for n, r in enumerate((_R1, _R2, _R3, _R4), 1)}
assert _ANZ == {1: 5, 2: 2, 3: 2, 4: 3}

k.lernziele([
    "Ich kann prüfen, ob eine Relation eine Äquivalenzrelation ist, und erkläre, was sie festlegt (Def. 1.59, Bsp. 1.60)",
    "Ich kann Äquivalenzklassen $[a]$ bestimmen und die Faktormenge $M/{\\sim}$ aufschreiben (Def. 1.61, 1.64, Bsp. 1.62)",
    "Ich kenne Satz 1.63 (Klassen zerlegen $M$) und kann ihn beweisen",
    "Ich verstehe, wie $\\mathbb{Q}$ als Faktormenge von Brüchen entsteht, und kann die Transitivität dort nachrechnen (Bsp. 1.65)",
])

k.warum(r"""
Wann sind zwei Dinge „dasselbe“? Für den Computer sind `0.5` und `1/2` verschiedene
Darstellungen, für die Mathematik dieselbe Zahl. Äquivalenzrelationen machen das präzise:
Man erzeugt viele Darstellungen und fasst gleichwertige zusammen. Dieselbe Idee steckt in
Hashing (Elemente mit gleichem Hash), Restklassen (Kapitel 2 und 3: $\mathbb{Z}$,
$\mathbb{Z}/n\mathbb{Z}$) und in der Konstruktion von $\mathbb{Z}$ und $\mathbb{Q}$ aus Paaren.
""")

# ── Seite 1: Definition ───────────────────────────────────────────────────
k.erklaerung("Was ist „gleichwertig“?", r"""
## Definition 1.59

:::analogie 🎒 Sortiere nach Farbe
Du packst Socken in Gruppen gleicher Farbe. „Hat dieselbe Farbe wie“ ist immer wahr für
eine Socke und sich selbst, geht in beide Richtungen und überträgt sich über Dritte.
:::

**Definition 1.59.** Eine Relation $R$ auf $M$ heißt [[Äquivalenzrelation]], falls sie
[[reflexiv]], [[symmetrisch]] und [[transitiv]] ist. Man schreibt dann oft $\sim\ := R$.

Warum diese drei? Reflexiv: Jedes Ding ist zu sich gleichwertig. Symmetrisch: Gleichwertig ist
keine Einbahnstraße. Transitiv: Gleichwertig zu etwas Gleichwertigem ist gleichwertig.

:::rechnung Prüfe „gleiche Parität“ auf $\mathbb{Z}$
x - x = 0 = 2 \cdot 0 || reflexiv: $x$ und $x$ haben dieselbe Parität
7 - 3 = 4 = 2 \cdot 2 || Beispiel für $7 \sim 3$; Differenz gerade
3 - 7 = -4 = 2 \cdot (-2) || symmetrisch: die Differenz ändert nur das Vorzeichen
:::

:::achtung Nicht jede Relation, die sich „ähnlich“ anfühlt, ist eine Äquivalenz
„Unterscheidet sich um höchstens $1$“ ist reflexiv und symmetrisch, aber nicht transitiv:
$1 \approx 2$ und $2 \approx 3$, aber nicht $1 \approx 3$.
:::

:::alt Mit Stadtteilen
Jeder Mensch wohnt in genau einem Stadtteil. „Wohnt im selben Stadtteil wie“ ist eine
Äquivalenzrelation, und die Stadtteile sind die Gruppen. Genau das zeigt Satz 1.63 später:
Jede Äquivalenzrelation sortiert die Menge in Gruppen.
:::
---
## Beispiel 1.60: vier Äquivalenzrelationen

Auf $M = \{-1, 1, 2, 3, 4\}$ (Abbildung 1.4 im Skript):

- $\sim_1$: $x = y$,
- $\sim_2$: $x$ und $y$ haben dieselbe Parität,
- $\sim_3$: $x$ und $y$ haben dasselbe Vorzeichen,
- $\sim_4$: dieselbe Parität **und** dasselbe Vorzeichen.

Die Bilder zeigen die vier Relationen als Graph (Abbildung 1.4). Die Farbe verrät, welche
Elemente zusammengehören; an den Pfeilen siehst du Schleifen (reflexiv) und Doppelpfeile (symmetrisch).

§BILDER§

:::rechnung Wie viele Paare haben die Relationen?
5 || $\sim_1$: nur die Schleifen $(x, x)$
5 + 8 = 13 || $\sim_2$: 5 Schleifen und $(-1,1),(1,-1),(-1,3),(3,-1),(1,3),(3,1),(2,4),(4,2)$
5 + 12 = 17 || $\sim_3$: 5 Schleifen und $4 \cdot 3 = 12$ Paare verschiedener positiver Zahlen
5 + 4 = 9 || $\sim_4$: Schleifen sowie $(1,3),(3,1),(2,4),(4,2)$
:::

Alle vier sind reflexiv, symmetrisch und transitiv, auch am Graphen: überall Schleifen, Pfeile
in Gegenpaaren, jede Abkürzung da. Bei $\sim_3$ hängen $1, 2, 3, 4$ vollständig zusammen,
$-1$ steht allein.

:::alt Mit Gruppenfotos
Stell dir vier Fotografen vor, die die fünf Zahlen verschieden gruppieren. $\sim_1$ macht
Einzelporträts. $\sim_2$ fotografiert „gerade“ und „ungerade“ zusammen. $\sim_3$ stellt die
Positiven in eine Reihe und lässt $-1$ allein. $\sim_4$ nimmt beide Kriterien und macht
drei Gruppen.
:::
""".replace("§BILDER§", _BILDER))

_M5 = [1, 2, 3, 4, 5]
_ABS1 = rel(_M5, lambda x, y: abs(x - y) <= 1)
assert ist_refl(_M5, _ABS1) and ist_sym(_M5, _ABS1) and not ist_trans(_M5, _ABS1)

k.mehrfach("Welche dieser Relationen auf $M = \\{1, 2, 3, 4, 5\\}$ sind Äquivalenzrelationen?",
           ["$x \\sim y :\\iff x - y$ ist durch $2$ teilbar",
            "$x \\sim y :\\iff x = y$",
            "$x \\sim y :\\iff \\min(x, 3) = \\min(y, 3)$"],
           ["$x \\sim y :\\iff |x - y| \\le 1$",
            "$x \\sim y :\\iff x \\le y$",
            "$x \\sim y :\\iff x \\neq y$"],
           "Die ersten drei sortieren $M$ nach einem Merkmal (Parität, Identität, „Wert oder ab $3$“) und sind damit reflexiv, "
           "symmetrisch und transitiv. $|x - y| \\le 1$ ist nicht transitiv ($1 \\sim 2 \\sim 3$, aber $1 \\not\\sim 3$), "
           "$\\le$ nicht symmetrisch, $\\neq$ nicht reflexiv.",
           tipps=["Prüfe reflexiv, symmetrisch, transitiv der Reihe nach. Ein Gegenbeispiel genügt.",
                  "Bei „$\\sim$ nach einem Merkmal“ sind alle drei Eigenschaften automatisch erfüllt.",
                  "Suche bei $|x - y| \\le 1$ eine Kette über drei Zahlen."],
           fehler={"$x \\sim y :\\iff |x - y| \\le 1$": "Transitiv scheitert: $1 \\sim 2$ und $2 \\sim 3$, aber $|1 - 3| = 2 > 1$.",
                   "$x \\sim y :\\iff x \\le y$": "Nicht symmetrisch: $1 \\le 2$, aber nicht $2 \\le 1$. $\\le$ ist eine Ordnung.",
                   "$x \\sim y :\\iff x \\neq y$": "Nicht reflexiv: $1 \\neq 1$ ist falsch."})

k.mc("Für $\\sim_3$ aus Beispiel 1.60 (dasselbe Vorzeichen) auf $M = \\{-1, 1, 2, 3, 4\\}$: Wie viele Paare enthält die Relation?",
     [str(len(_R3)) + " Paare", str(len(_R2)) + " Paare", str(len(_R4)) + " Paare", "20 Paare"],
     "Die vier positiven Zahlen bilden $4 \\cdot 4 = 16$ Paare, dazu kommt $(-1, -1)$: $17$ Paare.",
     tipps=["Zähle getrennt: Paare unter positiven Zahlen und Paare mit $-1$.", "Mit $-1$ geht nur $(-1, -1)$."],
     fehler={str(len(_R2)) + " Paare": "Das sind die Paare von $\\sim_2$ (Parität).",
             str(len(_R4)) + " Paare": "Das sind die Paare von $\\sim_4$ (Parität und Vorzeichen).",
             "20 Paare": "Nur $(-1, -1)$ enthält die $-1$. Paare wie $(-1, 1)$ haben verschiedene Vorzeichen."})

# ── Seite 3: Klassen ──────────────────────────────────────────────────────
k.erklaerung("Äquivalenzklassen", r"""
## Definition 1.61 und Beispiel 1.62

**Definition 1.61.** Die [[Äquivalenzklasse]] von $a \in M$ bezüglich $\sim$ ist
$$[a] := \{x \in M \mid x \sim a\}.$$
Das ist die Gruppe aller Elemente, die zu $a$ gleichwertig sind. Jedes Element einer Klasse ist
ein [[Repräsentant]]: Ist $b \in [a]$, so ist $[b] = [a]$.

**Beispiel 1.62.** Die Klassen aus Beispiel 1.60:

| | $[-1]$ | $[1]$ | $[2]$ | $[3]$ | $[4]$ |
|---|---|---|---|---|---|
§TAB§

:::rechnung Klasse $[1]$ bezüglich $\sim_2$ bestimmen
-1 \equiv 1 \pmod 2 || „$\equiv \pmod 2$“ heißt hier nur „gleiche Parität“: $-1$ ist ungerade wie $1$, also $-1 \in [1]$
3 - 1 = 2 || $3$ ist ungerade: $3 \in [1]$
4 - 1 = 3 || $4$ ist gerade: $4 \notin [1]$; ebenso $2 \notin [1]$, also $[1] = \{-1, 1, 3\}$
:::

:::achtung Auf die Reihenfolge im Paar achten
$[a]$ enthält alle $x$ mit $x \sim a$. Weil $\sim$ symmetrisch ist, ist das dasselbe wie alle $x$
mit $a \sim x$. Bei Relationen, die nicht symmetrisch sind, wäre das ein Unterschied.
:::

:::alt Mit Telefonbuch
Du schlägst „Familie Meyer“ nach: Du bekommst alle, die zur selben Familie gehören. Egal,
welches Mitglied du nachschlägst, du bekommst dieselbe Liste. So ist es mit
$[1] = [3] = [-1]$ bei $\sim_2$.
:::
""".replace("§TAB§", _TAB))

k.menge("Bestimme die Äquivalenzklasse $[2]$ bezüglich $\\sim_4$ (dieselbe Parität **und** dasselbe Vorzeichen) auf "
        "$M = \\{-1, 1, 2, 3, 4\\}$.",
        mtext(_KL[4][2]),
        "Gesucht sind alle $x \\in M$, die gerade und positiv sind wie $2$: $2$ und $4$.",
        tipps=["Prüfe jedes $x \\in M$: dieselbe Parität wie $2$ und dasselbe Vorzeichen?",
               "Gerade Zahlen in $M$ sind $2$ und $4$.", "Beide sind positiv."],
        rechenweg=r"""
:::rechnung
2 \equiv 2 \pmod 2 || $2$ selbst gehört dazu ($[a] \ni a$)
4 \equiv 2 \pmod 2 || $4$ ist gerade und positiv wie $2$
:::

Die ungeraden Zahlen $-1, 1, 3$ haben eine andere Parität.
""",
        typische_fehler=[(mtext(_KL[4][1]), "Das ist $[1]$ (ungerade und positiv). $2$ ist gerade."),
                         ("{2}", "Auch $4$ ist gerade und positiv wie $2$."),
                         (mtext(_KL[3][2]), "Das ist $[2]$ bei $\\sim_3$ (nur Vorzeichen).")])

k.menge("Bestimme $[-1]$ bezüglich $\\sim_3$ (dasselbe Vorzeichen) auf $M = \\{-1, 1, 2, 3, 4\\}$.",
        mtext(_KL[3][-1]),
        "Außer $-1$ selbst hat keine Zahl in $M$ ein negatives Vorzeichen.",
        tipps=["Welche Zahlen in $M$ sind negativ?", "Jede Klasse enthält ihren Repräsentanten.", "Nur $-1$ ist negativ."],
        rechenweg=r"""
:::rechnung
-1 < 0 || $-1$ ist negativ
1, 2, 3, 4 > 0 || alle anderen sind positiv, also nicht in $[-1]$
:::
""",
        typische_fehler=[("{}", "Eine Äquivalenzklasse ist nie leer: Wegen der Reflexivität gilt $-1 \\in [-1]$ (Satz 1.63 (i))."),
                         (mtext(_KL[3][1]), "Das ist $[1]$, die Klasse der positiven Zahlen.")])

# ── Seite 4: Satz 1.63 ───────────────────────────────────────────────────
k.erklaerung("Satz 1.63: Klassen zerlegen die Menge", r"""
## Drei Aussagen

**Satz 1.63.** Für jede Äquivalenzrelation $\sim$ auf $M$ gilt:

- (i) $a \in [a]$ für jedes $a \in M$, insbesondere $[a] \neq \emptyset$,
- (ii) $\bigcup_{a \in M} [a] = M$,
- (iii) für alle $a, b \in M$ mit $[a] \neq [b]$ gilt $[a] \cap [b] = \emptyset$.

Zwei Klassen sind also gleich oder disjunkt. Nichts überlappt teilweise.

*Beweis.* (i) Reflexivität: $a \sim a$, also $a \in [a]$. (ii) „$\subseteq$“ (links in rechts): Jede Klasse ist Teilmenge von $M$, also auch ihre Vereinigung.
„$\supseteq$“ (rechts in links): Jedes $a \in M$ liegt wegen (i) in $[a]$. (iii) Kontraposition: Sei $[a] \cap [b] \neq \emptyset$, etwa
$x \in [a] \cap [b]$. Dann $x \sim a$ und $x \sim b$. Symmetrie: $a \sim x$. Transitivität: $a \sim b$.
Ist $y \in [a]$, so $y \sim a \sim b$, also $y \in [b]$. Somit $[a] \subseteq [b]$, analog $[b] \subseteq [a]$. $\square$

:::rechnung Satz 1.63 an $\sim_2$
\{-1, 1, 3\} \cup \{2, 4\} = \{-1, 1, 2, 3, 4\} || (ii): die Klassen decken $M$ ab
\{-1, 1, 3\} \cap \{2, 4\} = \emptyset || (iii): verschiedene Klassen sind disjunkt
:::

:::alt Mit Schubladen
Die Äquivalenzklassen sind Schubladen. Jedes Element liegt in mindestens einer (nämlich
seiner eigenen), und es liegt nie in zwei verschiedenen Schubladen. Wäre ein Element in zwei,
würden die Schubladen wegen Symmetrie und Transitivität zu einer verschmelzen.
:::
""")

k.ordnen("Ordne den Beweis von Satz 1.63 (iii) (per Kontraposition): Aus $[a] \\cap [b] \\neq \\emptyset$ folgt $[a] = [b]$.",
         ["Sei $[a] \\cap [b] \\neq \\emptyset$. Dann gibt es ein $x \\in [a] \\cap [b]$, also $x \\sim a$ und $x \\sim b$.",
          "Mit Symmetrie folgt $a \\sim x$, mit Transitivität dann $a \\sim b$.",
          "Sei $y \\in [a]$, also $y \\sim a$. Mit $a \\sim b$ folgt $y \\sim b$, also $y \\in [b]$.",
          "Damit ist $[a] \\subseteq [b]$. Analog folgt $[b] \\subseteq [a]$, also $[a] = [b]$. $\\square$"],
         "Man nimmt ein gemeinsames Element $x$, macht daraus $a \\sim b$ und zeigt dann beide Inklusionen.",
         ablenker=["Wegen der Reflexivität gilt $a \\sim b$ für alle $a, b \\in M$.",
                   "Da $[a] \\neq [b]$, existiert ein $x$ mit $x \\in [a] \\cap [b]$."],
         tipps=["Kontraposition: Wenn nicht-disjunkt, dann gleich.",
                "Zuerst $a \\sim b$ herleiten, erst danach Elemente von $[a]$ betrachten.",
                "Symmetrie und Transitivität liefern $a \\sim b$ aus $x \\sim a$ und $x \\sim b$."])

# ── Seite 5: Faktormenge ─────────────────────────────────────────────────
k.erklaerung("Die Faktormenge", r"""
## Definition 1.64

Die Menge aller Äquivalenzklassen heißt [[Faktormenge]]:
$$M/{\sim}\ :=\ \{U \in \mathcal{P}(M) \mid \exists a \in M : U = [a]\}.$$
Jede Klasse zählt **einmal**, auch wenn sie viele Repräsentanten hat. Die Elemente der
Faktormenge sind selbst Mengen.

:::rechnung Faktormengen aus Beispiel 1.62
M/{\sim_2} = \{\{-1, 1, 3\}, \{2, 4\}\} || zwei Klassen: ungerade und gerade
M/{\sim_3} = \{\{-1\}, \{1, 2, 3, 4\}\} || zwei Klassen: negativ und positiv
M/{\sim_4} = \{\{-1\}, \{1, 3\}, \{2, 4\}\} || drei Klassen
M/{\sim_1} = \{\{-1\}, \{1\}, \{2\}, \{3\}, \{4\}\} || fünf Klassen: jedes Element allein
:::

Die kanonische Abbildung $\nu\colon M \to M/{\sim},\ x \mapsto [x]$ (Beispiel 1.68, nächstes Kapitel)
schickt jedes Element in seine Klasse.

:::achtung $[1]$ und $\{[1]\}$ sind verschieden
$[1] = \{-1, 1, 3\}$ ist eine Menge von Zahlen und ein **Element** von $M/{\sim_2}$.
Die Faktormenge hat hier nur die zwei Elemente $[1]$ und $[2]$, nicht fünf.
:::

:::alt Mit Karteikarten
Du hast fünf Karteikarten, aber auf manchen steht dasselbe. Die Faktormenge ist der
Stapel, wenn du Doppelte wegwirfst. Hier bleiben für „dieselbe Parität“ nur zwei
Stapel übrig: der Stapel der ungeraden und der der geraden Zahlen.
:::
""")

k.mc("Wie viele Elemente hat die Faktormenge $M/{\\sim_2}$ für $M = \\{-1, 1, 2, 3, 4\\}$ (dieselbe Parität)?",
     ["2", "5", "3", "1"],
     "Es gibt nur die Klassen $[1] = [-1] = [3] = \\{-1, 1, 3\\}$ und $[2] = [4] = \\{2, 4\\}$. Die Faktormenge zählt Klassen, nicht Repräsentanten.",
     tipps=["Zähle verschiedene Klassen, nicht Elemente von $M$.", "Wie viele verschiedene Mengen stehen in der $\\sim_2$-Zeile von Beispiel 1.62?"],
     fehler={"5": "Das sind die Elemente von $M$. Mehrere von ihnen haben dieselbe Klasse.",
             "3": "Das wäre die Anzahl bei $\\sim_4$ (Parität und Vorzeichen)."})

k.wf("Die Faktormenge $M/{\\sim}$ ist immer eine Teilmenge von $M$.", False,
     "Ihre Elemente sind Klassen, also Teilmengen von $M$. Sie ist eine Teilmenge der Potenzmenge $\\mathcal{P}(M)$, nicht von $M$.",
     tipps=["Aus welchen Objekten besteht $M/{\\sim_2}$? Zahlen oder Mengen?"])

# ── Seite 6: Q als Faktormenge ───────────────────────────────────────────
k.erklaerung("Beispiel 1.65: ℚ als Faktormenge", r"""
## Brüche, die dieselbe Zahl sind

Sei $B := \{(z, n) \in \mathbb{Z}^2 \mid n > 0\}$ die Menge der Brüche mit Zähler $z$ und Nenner $n$,
und $(z_1, n_1) \sim (z_2, n_2) :\iff z_1 n_2 = z_2 n_1$. Das ist die Gleichheit von Brüchen nach Kreuzmultiplizieren.
Dann ist $\mathbb{Q}$ als Menge die Faktormenge $B/{\sim}$: Eine rationale Zahl ist die
Klasse aller Darstellungen desselben Bruchs, etwa $[(1, 2)] = \{(1, 2), (2, 4), (3, 6), \ldots\}$.

:::rechnung Beispiele
1 \cdot 4 = 2 \cdot 2 || $(1, 2) \sim (2, 4)$ nach Definition
1 \cdot 6 = 3 \cdot 2 || $(1, 2) \sim (3, 6)$
2 \cdot 6 = 3 \cdot 4 || $(2, 4) \sim (3, 6)$: passt zur Transitivität
1 \cdot 3 \neq 2 \cdot 2 || $(1, 2) \not\sim (2, 3)$: $\frac12 \neq \frac23$
:::

Reflexiv ($z n = z n$) und symmetrisch sind offensichtlich. Für die Transitivität sei
$(z_1, n_1) \sim (z_2, n_2) \sim (z_3, n_3)$. Dann gilt
$$n_2 (z_1 n_3) = (z_1 n_2) n_3 = (z_2 n_1) n_3 = (z_2 n_3) n_1 = (z_3 n_2) n_1 = n_2 (z_3 n_1),$$
und wegen $n_2 > 0$ darf man kürzen: $z_1 n_3 = z_3 n_1$.

:::achtung Warum $n_2 > 0$ wichtig ist
Wäre $n = 0$ erlaubt, könnte man nicht kürzen, und die Relation wäre nicht transitiv:
$(1, 0) \sim (0, 0)$ und $(0, 0) \sim (3, 1)$ (beide Gleichungen lauten $0 = 0$), aber $(1, 0) \not\sim (3, 1)$,
denn $1 \cdot 1 \neq 3 \cdot 0$. Darum verlangt $B$ immer $n > 0$.
:::

:::alt Mit Tortenstücken
$\frac12$, $\frac24$ und $\frac36$ sind verschieden geschriebene Brüche, aber gleich viel
Torte. Die Klasse $[(1, 2)]$ ist der Zettelstapel aller Schreibweisen von „einer halben
Torte“. Die Zahl $\frac12$ **ist** dieser Stapel, nicht eine einzelne Schreibweise.
:::
""")

_Bsp = [(1, 2), (2, 4), (3, 6), (-1, -2)]

k.luecke("Zeige $(3, 4) \\sim (9, 12)$ in $B$: Setze in die Definition $z_1 n_2 = z_2 n_1$ ein.",
         "3 \\cdot \\luecke = \\luecke \\cdot 4", [[12], [9]],
         "Mit $(z_1, n_1) = (3, 4)$ und $(z_2, n_2) = (9, 12)$ ist $z_1 n_2 = 3 \\cdot 12 = 36$ und $z_2 n_1 = 9 \\cdot 4 = 36$.",
         tipps=["$z_1 = 3$, $n_1 = 4$, $z_2 = 9$, $n_2 = 12$.", "Links steht $z_1 \\cdot n_2$, rechts $z_2 \\cdot n_1$.", "$n_2 = 12$ und $z_2 = 9$."],
         rechenweg=r"""
:::rechnung
3 \cdot 12 = 36 || $z_1 n_2$
9 \cdot 4 = 36 || $z_2 n_1$, beide Seiten gleich
:::
""",
         typische_fehler=[([4, 9], "Du hast $n_1$ statt $n_2$ links eingesetzt. Gekreuzt: $z_1$ mal **zweiter** Nenner.")])

k.mehrfach("Welche Paare liegen in der Klasse $[(2, 3)]$ in $B$ (Beispiel 1.65)? Bedingung: $2 n = 3 z$.",
           ["$(4, 6)$", "$(6, 9)$"],
           ["$(3, 2)$", "$(2, 6)$", "$(-4, 6)$"],
           "$(z, n) \\in [(2, 3)]$ heißt $2n = 3z$. Das trifft auf $(4, 6)$ ($12 = 12$) und $(6, 9)$ ($18 = 18$) zu. "
           "$(3, 2)$ ist der Kehrwert, $(2, 6)$ gibt $12 \\neq 6$, und $(-4, 6)$ gibt $12 \\neq -12$.",
           tipps=["Die Bedingung ist $2 \\cdot n = 3 \\cdot z$.", "Prüfe jedes Paar $(z, n)$ einzeln.", "Die Brüche müssen den Wert $\\frac23$ haben."],
           fehler={"$(3, 2)$": "Das ist der Kehrwert: $2 \\cdot 2 = 4 \\neq 9 = 3 \\cdot 3$.",
                   "$(-4, 6)$": "$\\frac{-4}{6} = -\\frac23$, das Vorzeichen stimmt nicht."})


# ── Praxis ────────────────────────────────────────────────────────────────
def _rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def _zufall_aequ(rng):
    """Zufällige Äquivalenzrelation auf kleiner Menge ganzer Zahlen: (M, r, beschreibung_tex, merkmal)."""
    art = rng.choice(["mod", "betrag", "vorzeichen", "mod_vz"])
    if art == "mod":
        n = rng.choice([2, 3, 4])
        m = sorted(rng.sample(range(-4, 9), rng.randint(6, 8)))
        f = lambda x: x % n
        beschr = f"$x \\sim y :\\iff x - y$ ist durch ${n}$ teilbar (gleicher Rest bei Division durch ${n}$)"
        grund = lambda x: f"${x} = {x // n} \\cdot {n} + {x % n}$: Rest ${x % n}$"
    elif art == "betrag":
        m = sorted(rng.sample(range(-4, 5), rng.randint(6, 8)))
        f = abs
        beschr = "$x \\sim y :\\iff |x| = |y|$"
        grund = lambda x: f"$|{x}| = {abs(x)}$"
    elif art == "vorzeichen":
        m = sorted(rng.sample(range(-4, 6), rng.randint(6, 8)))
        f = lambda x: (x > 0) - (x < 0)
        beschr = "$x \\sim y :\\iff$ $x$ und $y$ haben dasselbe Vorzeichen (negativ, $0$, positiv)"
        grund = lambda x: f"${x}$ hat Vorzeichen {'minus' if x < 0 else 'null' if x == 0 else 'plus'}"
    else:
        m = sorted(rng.sample(range(-4, 8), rng.randint(6, 8)))
        f = lambda x: (x % 2, (x > 0) - (x < 0))
        beschr = "$x \\sim y :\\iff$ gleiche Parität **und** gleiches Vorzeichen"
        grund = lambda x: f"${x}$: Parität {'gerade' if x % 2 == 0 else 'ungerade'}, Vorzeichen {'minus' if x < 0 else 'null' if x == 0 else 'plus'}"
    r = rel(m, lambda x, y: f(x) == f(y))
    assert ist_aequ(m, r)
    return m, r, beschr, grund


def klasse_bestimmen(rng):
    while True:
        m, r, beschr, grund = _zufall_aequ(rng)
        a = rng.choice(m)
        kl = klasse(m, r, a)
        if 2 <= len(kl) < len(m):
            break
    andere = [x for x in m if x not in kl]
    fehler = [("{" + str(a) + "}", f"Die Klasse enthält mehr als $a$ selbst: Prüfe jedes $x \\in M$."),
              (mtext(set(m) - kl), "Das ist das Komplement der Klasse: die Elemente, die **nicht** zu $a$ gleichwertig sind.")]
    if len(kl) > 2:
        fehler.append((mtext(set(sorted(kl)[:-1])), "Es fehlt noch ein Element. Prüfe jedes $x \\in M$ einzeln."))
    fehler.append((mtext(kl | {andere[0]}), f"${andere[0]}$ gehört nicht dazu: ${andere[0]} \\not\\sim {a}$."))
    gesehen, tf = {mtext(kl)}, []
    for w, t in fehler:
        if w not in gesehen:
            gesehen.add(w)
            tf.append((w, t))
    zeilen = [(f"{grund(a)}", f"Merkmal von $a = {a}$")]
    zeilen += [(f"{x} \\sim {a}", "gleiches Merkmal, also $x \\in [a]$") for x in sorted(kl) if x != a][:3]
    return {"frage": f"Auf $M = {mtex(m)}$ sei {beschr}. Bestimme die Äquivalenzklasse $[{a}]$. "
                     "Eingabe zum Beispiel `{1; 2}`.",
            "loesung": mtext(kl),
            "tipps": [f"Prüfe jedes $x \\in M$: Ist $x \\sim {a}$?", f"Berechne das Merkmal von ${a}$ und vergleiche mit allen anderen.",
                      f"Die Klasse enthält ${a}$ selbst (Reflexivität)."],
            "rechenweg": _rechnung(zeilen) + f"\n\nAlso $[{a}] = {mtex(kl)}$.",
            "erklaerung": "Die Klasse $[a]$ sammelt alle $x \\in M$ mit $x \\sim a$, also gleichem Merkmal wie $a$.",
            "typische_fehler": tf}


def faktormenge_bestimmen(rng):
    m, r, beschr, grund = _zufall_aequ(rng)
    fm = faktormenge(m, r)
    n = len(fm)
    fehler = [(fam_text({frozenset({x}) for x in m}), "Das wäre die Faktormenge für die Gleichheit $\\sim_1$. Hier werden gleichwertige Elemente zusammengefasst."),
              ("{" + mtext(m) + "}", "Das wäre eine einzige Klasse. Es gibt mehrere verschiedene.")]
    gesehen, tf = {fam_text(fm)}, []
    for w, t in fehler:
        if w not in gesehen:
            gesehen.add(w)
            tf.append((w, t))
    zeilen = [(f"[{min(c)}] = {mtex(c)}", "Klasse von " + str(min(c))) for c in fam_key(fm)]
    zeilen.append((f"{n}", "Anzahl der Klassen: so viele Elemente hat $M/{\\sim}$"))
    return {"frage": f"Auf $M = {mtex(m)}$ sei {beschr}. Bestimme die Faktormenge $M/{{\\sim}}$ als Menge von Mengen, "
                     "zum Beispiel `{{1; 2}; {3}}`.",
            "loesung": fam_text(fm),
            "tipps": ["Bestimme zuerst die Klasse des kleinsten Elements, dann die Klasse eines Elements, das nicht darin liegt.",
                      "Jedes Element von $M$ liegt in genau einer Klasse (Satz 1.63).", "Schreibe jede Klasse nur einmal auf."],
            "rechenweg": _rechnung(zeilen),
            "erklaerung": "Die Faktormenge enthält jede Äquivalenzklasse genau einmal.",
            "typische_fehler": tf}


def ist_aequivalenz(rng):
    m = [1, 2, 3, 4]
    while True:
        art = rng.choice(["aequ", "aequ", "zufall", "fast"])
        if art == "aequ":
            f = {x: rng.randint(0, 2) for x in m}
            r = rel(m, lambda x, y: f[x] == f[y])
        elif art == "fast":
            f = {x: rng.randint(0, 2) for x in m}
            r = rel(m, lambda x, y: f[x] == f[y])
            r ^= {rng.choice(list(product(m, m)))}
        else:
            r = {p for p in product(m, m) if rng.random() < 0.35}
        if 3 <= len(r) <= 12:
            break
    ok = ist_aequ(m, r)
    eig = {"reflexiv": ist_refl(m, r), "symmetrisch": ist_sym(m, r), "transitiv": ist_trans(m, r)}
    falsch = [e for e, v in eig.items() if not v]
    opt = ["Ja, es ist eine Äquivalenzrelation"] + [f"Nein, nicht {e}" for e in eig]
    if ok:
        richtig = opt[0]
        fehler = {o: "Alle drei Eigenschaften sind erfüllt. Prüfe nochmals: Gegenbeispiele gibt es nicht." for o in opt[1:]}
        erkl = "Reflexiv, symmetrisch und transitiv: eine Äquivalenzrelation."
    else:
        richtig = f"Nein, nicht {falsch[0]}"
        opt = [richtig] + [o for o in opt if o != richtig]
        fehler = {}
        for o in opt[1:]:
            if o.startswith("Ja"):
                fehler[o] = f"Die Eigenschaft {falsch[0]} ist verletzt, also keine Äquivalenzrelation."
            else:
                e = o.replace("Nein, nicht ", "")
                if eig[e]:
                    fehler[o] = f"{e.capitalize()} gilt hier sogar. Gesucht ist die erste verletzte Eigenschaft in der Reihenfolge reflexiv, symmetrisch, transitiv."
                else:
                    fehler[o] = f"{e.capitalize()} ist zwar auch verletzt, aber die erste verletzte Eigenschaft ist {falsch[0]}."
        erkl = f"Die Eigenschaft {falsch[0]} ist verletzt, also ist $R$ keine Äquivalenzrelation."
    # Wenn mehrere verletzt sind, ist die Antwortauswahl eindeutig durch Reihenfolge
    rt = "{" + "; ".join(f"({a}; {b})" for a, b in sorted(r)) + "}"
    paare = "\\{" + ", ".join(f"({a}, {b})" for a, b in sorted(r)) + "\\}"
    zeilen = [(f"\\text{{{e}: {'ja' if v else 'nein'}}}", "Prüfung") for e, v in eig.items()]
    return {"typ": "mc", "frage": f"Gegeben ist $R = {paare}$ auf $M = \\{{1, 2, 3, 4\\}}$. Ist $R$ eine Äquivalenzrelation? "
                                  "Falls nein: Welche Eigenschaft (in der Reihenfolge reflexiv, symmetrisch, transitiv) ist als erste verletzt?",
            "optionen": opt, "fehler": fehler,
            "tipps": ["Prüfe reflexiv: alle $(x, x)$ da? Dann symmetrisch, dann transitiv.",
                      "Für „nein“ brauchst du ein Gegenbeispiel.", "Bei transitiv: auch Ketten mit $x = z$ prüfen."],
            "rechenweg": _rechnung(zeilen), "erklaerung": erkl}


k.praxis()

k.generator(klasse_bestimmen, typ="menge", titel="Äquivalenzklasse bestimmen")
k.generator(faktormenge_bestimmen, typ="menge", titel="Faktormenge bestimmen")
k.generator(ist_aequivalenz, typ="mc", titel="Ist es eine Äquivalenzrelation?")

k.rechenweg_aufgabe(r"""
## Quiz-Stil: Gleiche Länge

Auf der Menge $W$ aller Wörter über $\{a, b\}$ mit höchstens $3$ Buchstaben sei $v \sim w :\iff$ $v$ und $w$ haben gleich viele Buchstaben.
""",
    [{"typ": "wf", "frage": "$\\sim$ ist eine Äquivalenzrelation.", "wahr": True,
      "tipps": ["Prüfe die drei Eigenschaften: Wo kommt jedesmal die Länge ins Spiel?"],
      "erklaerung": "Sie vergleicht nur die Länge. Gleichheit von Zahlen ist reflexiv, symmetrisch und transitiv."},
     {"typ": "zahl", "frage": "Wie viele Elemente hat die Klasse $[ab]$ (alle Wörter der Länge $2$)?", "loesung": 4,
      "tipps": ["Jede der $2$ Stellen hat $2$ Möglichkeiten.", "$2 \\cdot 2$"],
      "rechenweg": "Wörter der Länge $2$: $aa, ab, ba, bb$, das sind $2 \\cdot 2 = 4$.",
      "typische_fehler": [(2, "Es gibt $2$ Buchstaben, aber $2$ Positionen: $2 \\cdot 2$.")]},
     {"typ": "zahl", "frage": "Wie viele Elemente hat $W/{\\sim}$? Das Leerwort der Länge $0$ zählt mit.", "loesung": 4,
      "tipps": ["Eine Klasse pro Länge.", "Länge $0, 1, 2, 3$."],
      "rechenweg": "Eine Klasse für jede Länge $0, 1, 2, 3$: vier Klassen.",
      "typische_fehler": [(15, "$15$ ist die Anzahl der Wörter. Die Faktormenge zählt Klassen.")]}],
    "$W/{\\sim}$ hat $4$ Klassen mit $1 + 2 + 4 + 8 = 15$ Wörtern insgesamt, passend zu Satz 1.63.",
    uebungsblatt=True,
    tipps=["Eine Klasse enthält alle Wörter gleicher Länge.", "Zähle erst die Klassen, dann die Wörter je Klasse."],
    rechenweg=r"""
:::rechnung
2 \cdot 2 = 4 || Wörter der Länge $2$
1 + 2 + 4 + 8 = 15 || alle Klassen zusammen decken $W$ ab
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Eine Relation auf ℝ

Auf $\mathbb{R}$ sei $x \sim y :\iff x - y \in \mathbb{Z}$.

1. Zeigen Sie, dass $\sim$ eine Äquivalenzrelation ist.
2. Bestimmen Sie $[0]$ und $[\tfrac12]$. Wie viele Elemente einer Klasse liegen im Intervall $[0, 1)$?
3. Zeigen Sie: Jedes $x \in \mathbb{R}$ liegt in der Klasse genau eines Elements von $[0, 1)$.
""",
    r"""
**1.** *Reflexiv:* $x - x = 0 \in \mathbb{Z}$. *Symmetrisch:* Ist $x - y = k \in \mathbb{Z}$, dann $y - x = -k \in \mathbb{Z}$.
*Transitiv:* Aus $x - y = k$, $y - z = l$ mit $k, l \in \mathbb{Z}$ folgt $x - z = k + l \in \mathbb{Z}$.

**2.** $[0] = \mathbb{Z}$, $[\tfrac12] = \{\ldots, -\tfrac12, \tfrac12, \tfrac32, \ldots\} = \{n + \tfrac12 \mid n \in \mathbb{Z}\}$.
Jede Klasse hat genau einen Repräsentanten in $[0, 1)$.

**3.** Für $x \in \mathbb{R}$ sei $r := x - \lfloor x \rfloor \in [0, 1)$. Dann $x - r = \lfloor x \rfloor \in \mathbb{Z}$, also $x \in [r]$.
Eindeutigkeit: Sind $r, s \in [0, 1)$ mit $r \sim s$, dann $r - s \in \mathbb{Z}$ und $|r - s| < 1$, also $r - s = 0$.
Mit Satz 1.63 (iii) liegt $x$ in keiner weiteren Klasse. $\square$
""",
    ["Alle drei Eigenschaften einzeln begründet (Transitivität mit $k + l$)",
     "$[0] = \\mathbb{Z}$ und $[\\frac12]$ richtig bestimmt",
     "Für $x$ den Repräsentanten $x - \\lfloor x \\rfloor$ angegeben",
     "Eindeutigkeit über $|r - s| < 1$ und $r - s \\in \\mathbb{Z}$ gezeigt"],
    "Äquivalenzrelation beweist man mit drei einzelnen Prüfungen, jede mit einer Gleichung, die in $\\mathbb{Z}$ liegt.",
    uebungsblatt=True,
    tipps=["Bei Transitivität: Addiere die beiden ganzen Zahlen $k$ und $l$."])

k.zusammenfassung(r"""
## Äquivalenzrelationen (Skript Abschn. 1.6, Def. 1.59 bis Bsp. 1.65)

- **Äquivalenzrelation** $\sim$: reflexiv, symmetrisch, transitiv (Def. 1.59).
- **Äquivalenzklasse** $[a] := \{x \in M \mid x \sim a\}$ (Def. 1.61).
- **Satz 1.63:** (i) $a \in [a]$, also $[a] \neq \emptyset$; (ii) $\bigcup_{a \in M} [a] = M$; (iii) $[a] \neq [b] \Rightarrow [a] \cap [b] = \emptyset$.
- **Faktormenge** $M/{\sim} := \{U \in \mathcal{P}(M) \mid \exists a \in M : U = [a]\}$ (Def. 1.64): jede Klasse einmal.
- Beispiel 1.60: auf $\{-1, 1, 2, 3, 4\}$ hat $\sim_1$ (Gleichheit) $5$, $\sim_2$ (Parität) $2$, $\sim_3$ (Vorzeichen) $2$, $\sim_4$ (beides) $3$ Klassen.
- Beispiel 1.65: $\mathbb{Q} = B/{\sim}$ mit $B = \{(z, n) \in \mathbb{Z}^2 \mid n > 0\}$, $(z_1, n_1) \sim (z_2, n_2) :\iff z_1 n_2 = z_2 n_1$.

!! Äquivalenzklassen sind entweder gleich oder disjunkt. Die Faktormenge zählt Klassen, nicht Elemente.
""")
