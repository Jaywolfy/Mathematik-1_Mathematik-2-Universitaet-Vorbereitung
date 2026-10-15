# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 16: Untergruppen und Gruppenhomomorphismen (Skript Disser WS 26/27, Abschn. 3.2, Def. 3.19 bis Bsp. 3.45)."""
from itertools import product
from math import gcd

from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(
    slug="gruppenhomomorphismen",
    titel="Untergruppen und Homomorphismen",
    beschreibung="Untergruppenkriterium, erzeugte Untergruppe, strukturerhaltende Abbildungen, Isomorphismus, Kern, Injektivität über den Kern",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 3.2 (Untergruppen, Gruppenhomomorphismen)",
    icon="🧩")


# ── Python: Permutationen, Untergruppen, Homomorphismen ──────────────────
def pt(p):
    return tuple(sorted(p.items()))


def komp(f, g):
    return {x: f[g[x]] for x in g}


def abgeschlossen_erzeugt(erz, op, neutral, inv):
    """Von erz erzeugte Untergruppe einer endlichen Gruppe (Abschluss unter op und inv)."""
    U = {neutral} | set(erz)
    while True:
        neu = {op(a, b) for a in U for b in U} | {inv(a) for a in U}
        if neu <= U:
            return U
        U |= neu


_ID = {1: 1, 2: 2, 3: 3, 4: 4}
_r = {1: 2, 2: 3, 3: 4, 4: 1}
_s1 = {1: 4, 2: 3, 3: 2, 4: 1}
_s2 = {1: 2, 2: 1, 3: 4, 4: 3}
_inv = lambda f: {v: k_ for k_, v in f.items()}
_rr = komp(_r, _r)
_rrr = komp(_r, _rr)
# Beispiele 3.22 bis 3.30
assert _rr == {1: 3, 2: 4, 3: 1, 4: 2} and _rrr == _inv(_r) == {1: 4, 2: 1, 3: 2, 4: 3}
_perm_op = lambda f, g: pt(komp(dict(f), dict(g)))
_perm_inv = lambda f: pt(_inv(dict(f)))
assert abgeschlossen_erzeugt([pt(_r)], _perm_op, pt(_ID), _perm_inv) == {pt(_ID), pt(_r), pt(_rr), pt(_rrr)}
assert komp(_s1, _s2) == _rr and komp(_s2, _s1) == _rr and pt(_rr) not in {pt(_ID), pt(_s1), pt(_s2)}
assert abgeschlossen_erzeugt([pt(_s1), pt(_s2)], _perm_op, pt(_ID), _perm_inv) == {pt(_ID), pt(_s1), pt(_s2), pt(_rr)}
assert all(_inv(s) == s for s in (_s1, _s2))
# Beispiel 3.31: B3 wird von e1, e2, e3 erzeugt; Isomorphismus ψ aus der Einleitung zu 3.32
_xor = lambda x, y: tuple((a + b) % 2 for a, b in zip(x, y))
_B3 = abgeschlossen_erzeugt([(1, 0, 0), (0, 1, 0), (0, 0, 1)], _xor, (0, 0, 0), lambda x: x)
assert len(_B3) == 8
_psi = {pt(_ID): (0, 0), pt(_s1): (1, 0), pt(_s2): (0, 1), pt(_rr): (1, 1)}
assert all(_psi[_perm_op(a, b)] == _xor(_psi[a], _psi[b]) for a in _psi for b in _psi) and len(set(_psi.values())) == 4
# p: B3 -> B3, (x1, x2, x3) -> (x1, x2, 0)
_p = lambda x: (x[0], x[1], 0)
assert all(_p(_xor(a, b)) == _xor(_p(a), _p(b)) for a in _B3 for b in _B3)
assert {x for x in _B3 if _p(x) == (0, 0, 0)} == {(0, 0, 0), (0, 0, 1)}
# Beispiele 3.43 bis 3.45
assert {a for a in range(-30, 31) if a % 5 == 0} == {5 * m for m in range(-6, 7)}
_f45 = lambda n: (2 * n) % 4
assert [_f45(n) for n in range(4)] == [0, 2, 0, 2] and all(_f45(a + b) == (_f45(a) + _f45(b)) % 4 for a in range(4) for b in range(4))
assert (4 * 3) != (4 * 1) * (4 * 1)       # φ4(1·1) = 4, φ4(1)·φ4(1) = 16: nur Gruppen-, kein Ringhomomorphismus


def rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def mtext(s):
    return "{" + "; ".join(str(x) for x in sorted(s)) + "}"


def mtex(s):
    return "\\{" + ", ".join(str(x) for x in sorted(s)) + "\\}"


k.lernziele([
    "Ich kann mit dem Untergruppenkriterium (Satz 3.24) entscheiden, ob eine Teilmenge einer Gruppe eine Untergruppe ist (Def. 3.19, Bsp. 3.20 bis 3.23)",
    "Ich kann die von einer Menge erzeugte Untergruppe $\\langle M \\rangle$ bestimmen (Def. 3.26, Satz 3.27, Bsp. 3.28 bis 3.31)",
    "Ich kann prüfen, ob eine Abbildung ein Gruppenhomomorphismus ist, und Isomorphismen erkennen (Def. 3.32, Bsp. 3.33 bis 3.37)",
    "Ich kann Kern und Bild bestimmen und Injektivität über $\\ker(f) = \\{e_G\\}$ nachweisen (Satz 3.38, 3.41, 3.42, Bsp. 3.43 bis 3.45)",
])

k.warum(r"""
Wenn eine Funktion `f(a ^ b) == f(a) ^ f(b)` erfüllt, darfst du Operationen vor oder nach `f` ausführen: Das ist die Idee
hinter Hashing mit XOR, Prüfsummen, Verschlüsselung und Parallelisierung. Ein Homomorphismus überträgt Struktur, und der Kern
sagt dir exakt, welche Information dabei verloren geht. Diese Sprache brauchst du später wieder für lineare Abbildungen
(Kern, Bild, Dimensionsformel). Hier lernst du sie in der einfachsten Form.
""")

# ── Seite 1: Untergruppe ─────────────────────────────────────────────────
k.erklaerung("Definition 3.19: Untergruppe", r"""
## Eine Gruppe in der Gruppe

:::analogie 🏠 Haus im Haus
Eine Untergruppe ist ein Teil der Gruppe, der selbst eine Gruppe ist, wenn man nur die Elemente darin zulässt: Wer zwei Elemente aus $U$ verknüpft,
bleibt in $U$. Das Neutrale und alle Inversen sind auch drin.
:::

**Definition 3.19.** $U \subseteq G$ heißt [[Untergruppe]] von $(G, \ast)$, falls $(U, \ast|_{U^2})$ eine Gruppe ist.

Das verlangt: $U$ ist **abgeschlossen** unter $\ast$ ($a, b \in U \Rightarrow a \ast b \in U$), enthält das neutrale Element und zu jedem Element sein Inverses.
Die Assoziativität erbt $U$ von $G$.

**Beispiel 3.20.** $n\mathbb{Z} := \{k \cdot n \mid k \in \mathbb{Z}\}$ ist Untergruppe von $(\mathbb{Z}, +)$. **Beispiel 3.21.** $\mathbb{N} \subseteq \mathbb{Z}$ ist **keine**: Es fehlen die Inversen.

:::rechnung $5\mathbb{Z}$ ist abgeschlossen
15 + (-20) = -5 || zwei Elemente aus $5\mathbb{Z}$ ($3 \cdot 5$ und $-4 \cdot 5$)
3 \cdot 5 + (-4) \cdot 5 = (3 - 4) \cdot 5 || allgemein: $kn + k'n = (k + k')n$
(3 - 4) \cdot 5 = -5 || liegt wieder in $5\mathbb{Z}$
:::

:::alt Als Zugangsliste
$U$ ist wie ein Club, in dem man sich nur mit Mitgliedern „verknüpft“ und wieder Mitglied bleibt. Der Club muss die Null-Aktion
(neutrales Element) kennen und jedes Mitglied rückgängig machen können (Inverse).
:::
""")

k.mehrfach("Welche Teilmengen sind Untergruppen von $(\\mathbb{Z}, +)$?",
           ["$5\\mathbb{Z}$", "$2\\mathbb{Z}$ (die geraden Zahlen)", "$\\{0\\}$"],
           ["$\\mathbb{N}$", "die ungeraden Zahlen", "$\\{-1, 0, 1\\}$"],
           "$n\\mathbb{Z}$ und $\\{0\\}$ sind abgeschlossen, enthalten $0$ und alle Inversen. $\\mathbb{N}$ hat keine Inversen (Bsp. 3.21). Die ungeraden Zahlen enthalten $0$ nicht und sind nicht abgeschlossen ($1 + 1 = 2$). $\\{-1, 0, 1\\}$ ist nicht abgeschlossen: $1 + 1 = 2$.",
           tipps=["Prüfe: abgeschlossen unter $+$, enthält $0$, enthält $-a$ zu jedem $a$.", "Welche Elemente fehlen bei den falschen Kandidaten?"],
           fehler={"$\\mathbb{N}$": "Es gilt $1 \\in \\mathbb{N}$, aber $-1 \\notin \\mathbb{N}$: Inverse fehlen.",
                   "die ungeraden Zahlen": "$1 + 1 = 2$ ist gerade: nicht abgeschlossen; auch $0$ fehlt.",
                   "$\\{-1, 0, 1\\}$": "$1 + 1 = 2 \\notin \\{-1, 0, 1\\}$: nicht abgeschlossen."})

# ── Seite 2: Drehungen und Spiegelungen ──────────────────────────────────
k.erklaerung("Beispiele 3.22 und 3.23: Drehungen und Spiegelungen", r"""
## Ein Bild auf vier Ecken

Die Ecken eines Bildes tragen die Nummern $1, 2, 3, 4$. Eine Drehung ist dann eine Permutation von $\{1, 2, 3, 4\}$:

- Drehung um $90^\circ$: $r = (1 \mapsto 2,\ 2 \mapsto 3,\ 3 \mapsto 4,\ 4 \mapsto 1)$.
- Spiegelungen: $\sigma_1 = (1 \mapsto 4,\ 2 \mapsto 3,\ 3 \mapsto 2,\ 4 \mapsto 1)$ und $\sigma_2 = (1 \mapsto 2,\ 2 \mapsto 1,\ 3 \mapsto 4,\ 4 \mapsto 3)$.

**3.22:** $R := \{\mathrm{id}, r, r \circ r, r \circ r \circ r\}$ ist Untergruppe von $(\mathrm{perm}(\{1, 2, 3, 4\}), \circ)$. Drehungen ergeben wieder Drehungen.
**3.23:** $S := \{\mathrm{id}, \sigma_1, \sigma_2\}$ ist **keine** Untergruppe, denn $\sigma_1 \circ \sigma_2 = r \circ r \notin S$.

:::rechnung $\sigma_1 \circ \sigma_2$ auf allen Ecken
1 \mapsto 2 \mapsto 3 || $\sigma_2(1) = 2$, dann $\sigma_1(2) = 3$
2 \mapsto 1 \mapsto 4 || $\sigma_2(2) = 1$, dann $\sigma_1(1) = 4$
3 \mapsto 4 \mapsto 1 || $\sigma_2(3) = 4$, dann $\sigma_1(4) = 1$
4 \mapsto 3 \mapsto 2 || $\sigma_2(4) = 3$, dann $\sigma_1(3) = 2$: das ist $r \circ r$ ($1 \mapsto 3$, $2 \mapsto 4$, $3 \mapsto 1$, $4 \mapsto 2$)
:::

:::alt Als Fotos
Zwei Spiegelungen nacheinander ergeben eine Drehung um $180^\circ$, keine Spiegelung. Spiegelungen allein sind nicht abgeschlossen. Dreht man dagegen ein Foto, bleibt es
bei einer Drehung.
:::
""")

k.mc("Warum ist $S = \\{\\mathrm{id}, \\sigma_1, \\sigma_2\\}$ keine Untergruppe von $\\mathrm{perm}(\\{1, 2, 3, 4\\})$ (Bsp. 3.23)?",
     ["Es ist nicht abgeschlossen: $\\sigma_1 \\circ \\sigma_2 = r \\circ r \\notin S$",
      "Es fehlt das neutrale Element",
      "$\\sigma_1$ hat kein Inverses",
      "$\\circ$ ist nicht assoziativ"],
     "$\\mathrm{id} \\in S$ und $\\sigma_i^{-1} = \\sigma_i$. Die Assoziativität gilt für jede Verkettung. Nur die Abgeschlossenheit scheitert: $\\sigma_1 \\circ \\sigma_2$ ist die Drehung um $180^\\circ$.",
     tipps=["Prüfe die drei Dinge: abgeschlossen, neutrales Element, Inverse.", "Verkette $\\sigma_1$ und $\\sigma_2$."],
     fehler={"Es fehlt das neutrale Element": "$\\mathrm{id} \\in S$ nach Definition.",
             "$\\sigma_1$ hat kein Inverses": "$\\sigma_1^{-1} = \\sigma_1$ liegt in $S$.",
             "$\\circ$ ist nicht assoziativ": "Die Verkettung ist immer assoziativ."})

# ── Seite 3: Satz 3.24 ───────────────────────────────────────────────────
k.erklaerung("Satz 3.24: Das Untergruppenkriterium", r"""
## Eine Bedingung statt drei

**Satz 3.24.** $U \subseteq G$ ist genau dann Untergruppe von $(G, \ast)$, wenn
$$U \ne \emptyset \quad\text{und}\quad a \ast b^{-1} \in U \text{ für alle } a, b \in U.$$

*Beweis „$\Rightarrow$“.* $e_U = e_G$ (Kürzungsregel aus $e_U \ast u = e_G \ast u$), und das Inverse in $U$ ist das Inverse in $G$ (Satz 3.9). Also $a \ast b^{-1} \in U$ wegen Abgeschlossenheit.

*Beweis „$\Leftarrow$“.* Die Schritte stehen unten in der Aufgabe: Neutrales Element, Inverse, Abgeschlossenheit der Reihe nach.

:::rechnung Kriterium an $U = 3\mathbb{Z}$, $a = 9$, $b = -6$
9 - (-6) = 15 || $a \ast b^{-1}$ in der additiven Gruppe: $a + (-b)$
15 = 5 \cdot 3 || $15 \in 3\mathbb{Z}$: die Bedingung ist für dieses Paar erfüllt
0 = 3 - 3 || Nichtleer: $0 = u - u \in U$ für $u = 3$
:::

:::alt Als Abkürzung
Statt drei Dinge einzeln zu prüfen, testest du nur, ob „Element mal Inverses eines Elements“ in $U$ bleibt. Setzt du $a = b$, steht das
Neutrale drin. Mit $a = e$ kommen die Inversen, dann die Produkte. Eine Prüfung liefert alle drei.
:::
""")

k.ordnen("Ordne den Beweis von Satz 3.24, Richtung „$\\Leftarrow$“: Es gelte $U \\ne \\emptyset$ und $a \\ast b^{-1} \\in U$ für alle $a, b \\in U$.",
         ["Die Assoziativität von $\\ast|_{U^2}$ überträgt sich von $G$.",
          "Wähle $u \\in U$. Mit $a = b = u$ folgt $e = u \\ast u^{-1} \\in U$.",
          "Mit $a = e$ und $b = u$ folgt $u^{-1} = e \\ast u^{-1} \\in U$ für jedes $u \\in U$.",
          "Für $u, v \\in U$ ist $v^{-1} \\in U$, und mit $a = u$, $b = v^{-1}$ folgt $u \\ast v = u \\ast (v^{-1})^{-1} \\in U$ (Satz 3.17).",
          "Also ist $U$ abgeschlossen, enthält $e$ und alle Inversen: $(U, \\ast|_{U^2})$ ist eine Gruppe."],
         "Erst das Neutrale (mit $a = b$), dann die Inversen (mit $a = e$), zuletzt die Abgeschlossenheit (mit $b$ durch $v^{-1}$ ersetzt, benutzt Satz 3.17).",
         ablenker=["Aus $a = b = u$ folgt $u \\ast u \\in U$, also ist $U$ abgeschlossen.", "Da $G$ abelsch ist, folgt die Behauptung."],
         tipps=["Beginne mit einem Element $u \\in U$. Welches Element liegt wegen $a = b = u$ in $U$?", "Wann brauchst du $(v^{-1})^{-1} = v$?",
                "Die Abgeschlossenheit kommt zuletzt: Sie braucht schon die Inversen."])

k.papier(r"""
## Übung zu Satz 3.25: Schnitte von Untergruppen

Sei $\mathcal{U}$ eine nichtleere Menge von Untergruppen einer Gruppe $G$. Zeigen Sie mit dem Untergruppenkriterium, dass $\bigcap_{U \in \mathcal{U}} U$ eine Untergruppe von $G$ ist.
""",
    r"""
Sei $D := \bigcap_{U \in \mathcal{U}} U$. Jede Untergruppe enthält das neutrale Element $e$ von $G$ (Beweis zu Satz 3.24), also $e \in D$ und $D \ne \emptyset$
(hier wird benutzt, dass $\mathcal{U} \ne \emptyset$).
Seien $a, b \in D$. Für jedes $U \in \mathcal{U}$ gilt $a, b \in U$, also nach Satz 3.24 $a \ast b^{-1} \in U$. Damit liegt $a \ast b^{-1}$ in jedem $U$, also in $D$.
Nach Satz 3.24 ist $D$ eine Untergruppe. $\square$
""",
    ["$e \\in D$ begründet, also $D \\ne \\emptyset$ (nutzt $\\mathcal{U} \\ne \\emptyset$)",
     "Für beliebige $a, b \\in D$ das Kriterium in jeder einzelnen Untergruppe $U$ angewendet",
     "Geschlossen, dass $a \\ast b^{-1}$ im ganzen Schnitt liegt"],
    "Ein Schnitt von Untergruppen ist wieder eine Untergruppe: Die Eigenschaft „liegt in jedem $U$“ erbt sich.",
    tipps=["Welche Bedingungen verlangt Satz 3.24? Weise beide für $D$ nach."])

# ── Seite 4: Erzeugte Untergruppe ────────────────────────────────────────
k.erklaerung("Definition 3.26: Die erzeugte Untergruppe", r"""
## Die kleinste Untergruppe um $M$

Ist $M \subseteq G$ keine Untergruppe, ergänzt du es um alles, was nötig ist.

**Definition 3.26.** $\langle M \rangle := \bigcap \{U \subseteq G \mid U \text{ Untergruppe von } G,\ M \subseteq U\}$.

**Satz 3.27.** $\langle M \rangle$ ist die **kleinste** [[Untergruppe]], die $M$ enthält, und $\langle M \rangle = M$, falls $M$ schon Untergruppe ist.

**Beispiele.** $\langle \{n\} \rangle_{(\mathbb{Z}, +)} = n\mathbb{Z}$ (3.28), $\langle \{r\} \rangle = R$ (3.29), $\langle S \rangle = S \cup \{r \circ r\}$ (3.30), $B_n = \langle \{e_1, \ldots, e_n\} \rangle$ (3.31).

:::rechnung $\langle \{[4]_{12}\} \rangle$ in $(\mathbb{Z}/12\mathbb{Z}, +)$
4 + 4 = 8 || $[4] + [4] = [8]$
8 + 4 = 12 || $[8] + [4] = [12] = [0]$: das Neutrale ist erreicht
0 + 4 = 4 || ab hier wiederholt sich alles: $\langle \{[4]_{12}\} \rangle = \{[0], [4], [8]\}$
:::

:::alt Als Baukasten
$M$ sind die Bausteine. $\langle M \rangle$ ist alles, was du durch beliebiges Zusammenfügen der Bausteine und ihrer Umkehrungen bauen kannst. Mehr geht nicht, weniger reicht nicht.
:::
""")

k.mc("Was ist $\\langle \\{[2]_6\\} \\rangle$ in $(\\mathbb{Z}/6\\mathbb{Z}, +)$?",
     ["$\\{[0]_6, [2]_6, [4]_6\\}$", "$\\{[2]_6\\}$", "$\\{[0]_6, [2]_6\\}$", "$\\mathbb{Z}/6\\mathbb{Z}$"],
     "Von $[2]$ aus: $[2] + [2] = [4]$, $[4] + [2] = [0]$. Dann wiederholt es sich. Die kleinste Untergruppe mit $[2]$ ist $\\{[0], [2], [4]\\}$.",
     tipps=["Addiere $[2]$ wiederholt zu sich, bis du wieder bei $[0]$ ankommst.", "$2 + 2 = 4$, $4 + 2 = 6 \\equiv 0$."],
     fehler={"$\\{[2]_6\\}$": "Diese Menge ist nicht abgeschlossen ($[2] + [2] = [4]$) und enthält $[0]$ nicht.",
             "$\\{[0]_6, [2]_6\\}$": "$[2] + [2] = [4]$ muss auch drin sein.",
             "$\\mathbb{Z}/6\\mathbb{Z}$": "Alles zu nehmen wäre eine Untergruppe, aber nicht die **kleinste**: $[1]$ wird nie erreicht."})

k.wf("Die von $\\{e_1, e_2\\}$ erzeugte Untergruppe $\\langle \\{e_1, e_2\\} \\rangle \\subseteq B_3$ hat $4$ Elemente.", True,
     "Mit $e_1 = (1, 0, 0)$, $e_2 = (0, 1, 0)$ entstehen $e_0 = (0, 0, 0)$, $e_1$, $e_2$, $e_1 \\oplus e_2 = (1, 1, 0)$ (Abb. 3.2). Das entspricht $B_2$, eingebettet in $B_3$.",
     tipps=["Verknüpfe $e_1$ und $e_2$ mit $\\oplus$ und denke an das Neutrale."])


def erzeugte_untergruppe(rng):
    n = rng.choice([6, 8, 9, 10, 12, 14, 15, 16, 18])
    while True:
        a = rng.randint(2, n - 1)
        U = {(a * j) % n for j in range(n)}
        if len(U) not in (1, n) and gcd(a, n) > 1:
            break
    d = gcd(a, n)
    falsch = [(mtext({a}), "Das ist nur $M$ selbst. Eine Untergruppe muss $[0]$, alle Summen und alle Inversen enthalten."),
              (mtext(set(range(n))), "Das ist ganz $\\mathbb{Z}/n\\mathbb{Z}$. Gesucht ist die **kleinste** Untergruppe mit $M$."),
              (mtext(U - {0}), "Das Neutrale $[0]$ gehört immer dazu.")]
    ketten = []
    x = a
    while x % n != 0:
        ketten.append(x)
        x = (x + a) % n
    zeilen = [(f"{u} + {a} = {u + a}", f"$[{u + a}] = [{(u + a) % n}]$") for u in ketten[:4]]
    return {"frage": f"Bestimme $\\langle \\{{[{a}]_{{{n}}}\\}} \\rangle \\subseteq (\\mathbb{{Z}}/{n}\\mathbb{{Z}}, +)$. Gib die Vertreter $r \\in \\{{0, \\ldots, {n - 1}\\}}$ als Menge an, zum Beispiel `{{0; 2; 4}}`.",
            "loesung": mtext(U),
            "tipps": [f"Addiere $[{a}]$ immer wieder zu sich, bis du bei $[0]$ ankommst.", f"Die Elemente sind die Vielfachen von ${a}$ modulo ${n}$.",
                      f"Es sind genau $n / \\operatorname{{ggT}}(a, n) = {n // d}$ Elemente, nämlich die Vielfachen von ${d}$ in $\\{{0, \\ldots, {n - 1}\\}}$."],
            "rechenweg": rechnung(zeilen + [(f"{n // d} \\cdot {a} = {(n // d) * a}", f"nach ${n // d}$ Schritten wieder $[0]$: Vielfaches von ${n}$")]),
            "erklaerung": f"Die von $[{a}]$ erzeugte Untergruppe besteht aus den Vielfachen von $\\operatorname{{ggT}}({a}, {n}) = {d}$.",
            "typische_fehler": ohne_gleiche(mtext(U), falsch)}


def untergruppe_pruefen(rng):
    n = rng.choice([8, 9, 10, 12, 15, 16])
    teiler = [d for d in range(2, n) if n % d == 0]
    d = rng.choice(teiler)
    basis = {x for x in range(n) if x % d == 0}
    art = rng.choice(["ug", "ohne0", "plus", "zufall"])
    if art == "ug":
        U = basis
    elif art == "ohne0":
        U = basis - {0}
    elif art == "plus":
        extra = rng.choice([x for x in range(n) if x not in basis])
        U = basis | {extra}
    else:
        U = set(rng.sample(range(n), rng.randint(2, 4)))
    if not U:
        U = {0, d}
    if 0 not in U:
        befund = "N"
        zeuge = "$[0]$ fehlt"
    else:
        paar = next(((a, b) for a in sorted(U) for b in sorted(U) if (a + b) % n not in U), None)
        if paar:
            befund = "A"
            zeuge = f"$[{paar[0]}] + [{paar[1]}] = [{(paar[0] + paar[1]) % n}] \\notin U$"
        else:
            befund = "G"
            zeuge = "$U$ ist nichtleer und abgeschlossen"
    G_ = "$U$ ist eine Untergruppe"
    N_ = "keine Untergruppe: das neutrale Element $[0]$ liegt nicht in $U$"
    A_ = "keine Untergruppe: $U$ ist nicht abgeschlossen unter $+$"
    korrekt = {"G": G_, "N": N_, "A": A_}[befund]
    optionen = [korrekt] + [o for o in (G_, N_, A_) if o != korrekt]
    fehler = {o: f"Prüfe die Bedingungen der Reihe nach. Hier gilt: {zeuge}." for o in optionen[1:]}
    zeilen = [("\\text{Untergruppenkriterium prüfen}", zeuge)]
    return {"typ": "mc",
            "frage": f"Sei $U = {mtex(U)} \\subseteq \\mathbb{{Z}}/{n}\\mathbb{{Z}}$ (geschrieben sind die Vertreter, also $r$ für $[r]_{{{n}}}$). Was gilt bezüglich $+$?",
            "optionen": optionen, "fehler": fehler,
            "tipps": ["Liegt $[0]$ in $U$? Wenn nicht, ist es keine Untergruppe.", "Addiere je zwei Elemente aus $U$ (auch ein Element mit sich selbst) und rechne modulo $n$.",
                      "In einer endlichen Gruppe genügen Nichtleerheit und Abgeschlossenheit: Die Inversen ergeben sich dann von selbst."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "In einer endlichen Gruppe ist eine nichtleere, abgeschlossene Teilmenge immer eine Untergruppe (Satz 3.24)."}


# ── Seite 5: Homomorphismus ──────────────────────────────────────────────
k.erklaerung("Definition 3.32: Gruppenhomomorphismus", r"""
## Strukturerhaltende Abbildungen

:::analogie 🌐 Übersetzer
Ein Übersetzer ist verlässlich, wenn „erst rechnen, dann übersetzen“ dasselbe ergibt wie „erst übersetzen, dann rechnen“.
Das ist die Idee eines Homomorphismus.
:::

**Definition 3.32.** $f\colon G \to H$ ist ein [[Gruppenhomomorphismus]] zwischen $(G, \ast)$ und $(H, \star)$, falls
$$f(a \ast b) = f(a) \star f(b) \quad \text{für alle } a, b \in G.$$
Bijektiv heißt [[Isomorphismus]], $G$ und $H$ sind dann **isomorph**. Ein Isomorphismus $G \to G$ heißt Automorphismus.

**3.33:** $\mathrm{id}_G$ ist Automorphismus. **3.34:** $g \circ f$ ist Homomorphismus. **3.35:** $f^{-1}$ ist Isomorphismus.
**3.36:** $\alpha\colon \langle S \rangle \to \langle S \rangle,\ f \mapsto r \circ f \circ r^{-1}$ ist ein Automorphismus. **3.37:** $\pi_n\colon (\mathbb{Z}, +) \to (\mathbb{Z}/n\mathbb{Z}, +),\ a \mapsto [a]_n$.

:::rechnung $\pi_5(a + b) = \pi_5(a) + \pi_5(b)$ mit $a = 7$, $b = 9$
7 + 9 = 16 || zuerst addieren in $\mathbb{Z}$
16 \bmod 5 = 1 || dann $\pi_5(16) = [16]_5 = [1]_5$
(7 \bmod 5) + (9 \bmod 5) = 2 + 4 || erst abbilden: $[7]_5 + [9]_5 = [2]_5 + [4]_5$
2 + 4 = 6 || $[6]_5 = [1]_5$: beide Wege geben dasselbe
:::

:::achtung Mal und plus verwechseln
Hier ist $\ast$ die Verknüpfung in $G$ und $\star$ die in $H$. Bei $(\mathbb{Z}, +) \to (\mathbb{Z}/n\mathbb{Z}, +)$ sind beide Addition. $f(a \cdot b) = f(a) \cdot f(b)$ wäre eine **andere** Bedingung, für $\cdot$ als Verknüpfung.
:::

:::alt Als Kopiergerät
Ein Homomorphismus ist wie ein Kopierer mit Verkleinern: Rechnest du vor dem Kopieren oder danach, bekommst du dieselbe Seite.
Ein Isomorphismus kopiert verlustfrei, jede Seite hat genau ein Original.
:::
""")

k.luecke("Der Isomorphismus $\\psi\\colon \\langle S \\rangle \\to B_2$ aus der Einleitung zu Def. 3.32 schickt $\\mathrm{id} \\mapsto (0, 0)$, $\\sigma_1 \\mapsto (1, 0)$, $\\sigma_2 \\mapsto (0, 1)$ und $r \\circ r \\mapsto (1, 1)$. Wegen $\\sigma_1 \\circ \\sigma_2 = r \\circ r$ muss $\\psi(\\sigma_1) \\oplus \\psi(\\sigma_2) = \\psi(r \\circ r)$ gelten. Berechne $(1, 0) \\oplus (0, 1) = (\\luecke, \\luecke)$.",
         "(1, 0) \\oplus (0, 1) = (\\luecke, \\luecke)",
         [[1], [1]],
         "Stellenweise: $(1 + 0) \\bmod 2 = 1$ und $(0 + 1) \\bmod 2 = 1$. Das ist $\\psi(r \\circ r) = (1, 1)$: Die Homomorphieeigenschaft stimmt für dieses Paar.",
         tipps=["XOR wirkt stellenweise.", "Erste Stelle: $(1 + 0) \\bmod 2$.", "$1 + 0 = 1$ und $0 + 1 = 1$, beide modulo $2$."],
         rechenweg=rechnung([("(1 + 0) \\bmod 2 = 1", "erste Stelle"), ("(0 + 1) \\bmod 2 = 1", "zweite Stelle")]),
         typische_fehler=[([0, 0], "$1 \\oplus 0 = 1$, nicht $0$: XOR ist $0$ nur bei zwei gleichen Bits.")])

k.mehrfach("Welche der folgenden Abbildungen $(\\mathbb{Z}, +) \\to (\\mathbb{Z}, +)$ sind Gruppenhomomorphismen?",
           ["$k \\mapsto 4k$ ($\\phi_4$, Bsp. 3.44)", "$k \\mapsto -k$", "$k \\mapsto 0$"],
           ["$k \\mapsto k + 1$", "$k \\mapsto k^2$"],
           "Für $k \\mapsto ck$ gilt $f(a + b) = c(a + b) = ca + cb$. $k \\mapsto k + 1$ schickt $0$ auf $1 \\ne 0$ (Satz 3.38 (i)). Bei $k \\mapsto k^2$ gilt $(1 + 1)^2 = 4 \\ne 1 + 1 = 2$.",
           tipps=["Setze zwei Zahlen $a, b$ ein und prüfe $f(a + b) = f(a) + f(b)$.", "Ein Homomorphismus muss $0$ auf $0$ schicken (Satz 3.38 (i))."],
           fehler={"$k \\mapsto k + 1$": "$f(0) = 1 \\ne 0$: das Neutrale wird nicht auf das Neutrale abgebildet. Außerdem $f(1 + 1) = 3 \\ne f(1) + f(1) = 4$.",
                   "$k \\mapsto k^2$": "$f(1 + 1) = 4$, aber $f(1) + f(1) = 2$."})

# ── Seite 6: Satz 3.38 ───────────────────────────────────────────────────
k.erklaerung("Satz 3.38: Was ein Homomorphismus mitbringt", r"""
## Vier Folgerungen

**Satz 3.38.** Sei $f\colon (G, \ast) \to (H, \star)$ ein Gruppenhomomorphismus. Dann:

(i) $f(e_G) = e_H$. (ii) $f(g^{-1}) = f(g)^{-1}$. (iii) $f(G)$ ist Untergruppe von $H$. (iv) Ist $G$ abelsch, ist auch $f(G)$ abelsch.

*Beweis (i).* $f(e_G) = f(e_G \ast e_G) = f(e_G) \star f(e_G)$ und $f(e_G) = f(e_G) \star e_H$. Kürzungsregel (Satz 3.16 (ii)) liefert $f(e_G) = e_H$.
*Beweis (ii).* $f(g^{-1}) \star f(g) = f(g^{-1} \ast g) = f(e_G) = e_H$. Eindeutigkeit des Inversen (Satz 3.9) gibt $f(g^{-1}) = f(g)^{-1}$.

:::rechnung Beispiel 3.39 mit $p\colon B_3 \to B_3$, $(x_1, x_2, x_3) \mapsto (x_1, x_2, 0)$
p(0, 0, 0) = (0, 0, 0) || (i): das Neutrale bleibt
p(1, 1, 1) = (1, 1, 0) || ein Element
p(1, 1, 0) = (1, 1, 0) || (ii): $p(x)^{-1} = p(x) = p(x^{-1})$ in $B_3$, da jedes Element selbstinvers ist
:::

(iii) und (iv) beweist du in der Praxis (siehe Aufgaben unten).

:::alt Als Fotografie
Ein Foto zeigt dir „nichts passiert“ (das Neutrale) auch als „nichts passiert“, und eine Rückwärtsbewegung bleibt eine Rückwärtsbewegung. Daraus folgt: Das, was am Ziel ankommt, ist wieder ein sauberer
Teil der Struktur, nämlich eine Untergruppe.
:::
""")

k.ordnen("Ordne den Beweis von Satz 3.38 (i): $f(e_G) = e_H$.",
         ["Es ist $f(e_G) = f(e_G \\ast e_G)$, denn $e_G \\ast e_G = e_G$.",
          "Nach der Homomorphieeigenschaft ist $f(e_G \\ast e_G) = f(e_G) \\star f(e_G)$.",
          "Andererseits ist $f(e_G) = f(e_G) \\star e_H$ (Satz 3.9).",
          "Also $f(e_G) \\star e_H = f(e_G) \\star f(e_G)$.",
          "Mit der Kürzungsregel (Satz 3.16 (ii)) folgt $f(e_G) = e_H$."],
         "Der Trick: $f(e)$ löst die Gleichung $x = x \\star x$, und in einer Gruppe hat sie nur die Lösung $e_H$ (Kürzungsregel).",
         ablenker=["Da $f$ injektiv ist, gilt $f(e_G) = e_H$."],
         tipps=["Schreibe $e_G$ als $e_G \\ast e_G$ und wende $f$ an.", "Vergleiche beide Ausdrücke für $f(e_G)$ und kürze.", "Injektivität wird nicht vorausgesetzt."])

# ── Seite 7: Kern ────────────────────────────────────────────────────────
k.erklaerung("Der Kern misst den Informationsverlust", r"""
## Definition 3.40, Satz 3.41, Satz 3.42

**Definition 3.40.** $\ker(f) := \{g \in G \mid f(g) = e_H\}$ ist der [[Kern|Kern (Gruppenhomomorphismus)]] von $f\colon G \to H$.

**Satz 3.41.** $\ker(f)$ ist Untergruppe von $G$ (Kriterium: $f(a \ast b^{-1}) = f(a) \star f(b)^{-1} = e_H$).

**Satz 3.42.** $f$ ist genau dann injektiv, wenn $\ker(f) = \{e_G\}$.

:::rechnung $f\colon \mathbb{Z}/4\mathbb{Z} \to \mathbb{Z}/4\mathbb{Z}$, $[n] \mapsto [2n]$ (Bsp. 3.45)
2 \cdot 0 = 0 || $f([0]) = [0]$
2 \cdot 1 = 2 || $f([1]) = [2]$
(2 \cdot 2) \bmod 4 = 0 || $f([2]) = [4] = [0]$
(2 \cdot 3) \bmod 4 = 2 || $f([3]) = [6] = [2]$; also $\ker(f) = \{[0], [2]\}$ und $f$ ist nicht injektiv
:::

**Weitere Beispiele:** $\ker(\pi_n) = n\mathbb{Z}$ (Bsp. 3.43), $\ker(\phi_4) = \{0\}$ für $\phi_4\colon k \mapsto 4k$ (Bsp. 3.44, also injektiv, Bild $4\mathbb{Z}$).

:::alt Als Radiergummi
Der Kern ist alles, was die Abbildung „wegradiert“, also auf das Neutrale schickt. Radiert sie gar nichts weg (nur das Neutrale), werden keine zwei Elemente verwechselt. Dann ist sie injektiv.
:::
""")

k.ordnen("Ordne den Beweis von Satz 3.42, Richtung „$\\Leftarrow$“: Gilt $\\ker(f) = \\{e_G\\}$, so ist $f$ injektiv.",
         ["Seien $a, b \\in G$ mit $f(a) = f(b)$.",
          "Dann ist $f(a \\ast b^{-1}) = f(a) \\star f(b)^{-1}$ (Homomorphie und Satz 3.38 (ii)).",
          "Wegen $f(b) = f(a)$ ist $f(a) \\star f(b)^{-1} = f(a) \\star f(a)^{-1} = e_H$.",
          "Also $a \\ast b^{-1} \\in \\ker(f) = \\{e_G\\}$, das heißt $a \\ast b^{-1} = e_G$.",
          "Es folgt $a = (a \\ast b^{-1}) \\ast b = e_G \\ast b = b$. Also ist $f$ injektiv."],
         "Du zeigst: Zwei Elemente mit gleichem Bild unterscheiden sich um ein Element des Kerns. Ist der Kern trivial, sind sie gleich.",
         ablenker=["Da $f$ ein Homomorphismus ist, ist $f$ injektiv.", "Dann ist $f(a) \\ast f(b) = e_H$."],
         tipps=["Nimm $f(a) = f(b)$ an und bilde $a \\ast b^{-1}$.", "Rechne $f(a \\ast b^{-1})$ aus.", "Der Kern enthält nur $e_G$, also kennst du das Element $a \\ast b^{-1}$."])

k.zahl("Sei $\\phi\\colon \\mathbb{Z}/12\\mathbb{Z} \\to \\mathbb{Z}/12\\mathbb{Z}$, $[n] \\mapsto [3n]$ (ein Gruppenhomomorphismus). Wie viele Elemente hat $\\ker(\\phi)$?",
       len([n for n in range(12) if (3 * n) % 12 == 0]),
       "$[n] \\in \\ker(\\phi) \\iff 3n \\equiv 0 \\pmod{12} \\iff 4 \\mid n$. Das sind $[0], [4], [8]$, also $3$ Elemente. Insbesondere ist $\\phi$ nicht injektiv.",
       tipps=["Gesucht sind die $[n]$ mit $[3n] = [0]$.", "Probiere $n = 0, \\ldots, 11$: wann ist $3n$ durch $12$ teilbar?", "$n = 0, 4, 8$."],
       rechenweg=rechnung([("3 \\cdot 4 = 12", "$12 \\equiv 0$: $[4] \\in \\ker$"), ("3 \\cdot 8 = 24", "$24 \\equiv 0$: $[8] \\in \\ker$"), ("3 \\cdot 1 = 3", "$3 \\not\\equiv 0$: $[1] \\notin \\ker$")]),
       typische_fehler=[(1, "Der Kern enthält nicht nur $[0]$: Auch $[4]$ und $[8]$ werden auf $[0]$ geschickt."),
                        (4, "Du hast vermutlich $12 / 3$ gerechnet. Der Kern besteht aus den $n$ mit $4 \\mid n$, im Bereich $0, \\ldots, 11$ sind das $0, 4, 8$.")])

k.wf("Ein Gruppenhomomorphismus $f\\colon G \\to H$ mit $\\ker(f) \\ne \\{e_G\\}$ ist nicht injektiv.", True,
     "Satz 3.42 liefert die Äquivalenz. Enthält der Kern ein $g \\ne e_G$, so gilt $f(g) = e_H = f(e_G)$ mit $g \\ne e_G$.",
     tipps=["Wende Satz 3.42 an (Kontraposition)."])

k.luecke("Für $f\\colon \\mathbb{Z}/4\\mathbb{Z} \\to \\mathbb{Z}/4\\mathbb{Z}$, $[n] \\mapsto [2n]$ gilt: $f([0]) = [\\luecke]$, $f([1]) = [\\luecke]$, $f([2]) = [\\luecke]$, $f([3]) = [\\luecke]$.",
         "f([0]) = [\\luecke],\\ f([1]) = [\\luecke],\\ f([2]) = [\\luecke],\\ f([3]) = [\\luecke]",
         [[0], [2], [0], [2]],
         "$2 \\cdot 0 = 0$, $2 \\cdot 1 = 2$, $2 \\cdot 2 = 4 \\equiv 0$, $2 \\cdot 3 = 6 \\equiv 2$. Der Kern ist $\\{[0], [2]\\}$ und das Bild $\\{[0], [2]\\}$.",
         tipps=["Rechne $2n$ und reduziere modulo $4$.", "$2 \\cdot 2 = 4 \\equiv 0$.", "Die Werte sind $0, 2, 0, 2$."],
         rechenweg=rechnung([("2 \\cdot 2 = 4", "$[4]_4 = [0]_4$"), ("2 \\cdot 3 = 6", "$[6]_4 = [2]_4$")]),
         typische_fehler=[([0, 2, 4, 6], "Nicht reduziert: Die Vertreter liegen in $\\{0, 1, 2, 3\\}$ ($[4] = [0]$, $[6] = [2]$).")])

k.praxis()


def kern_bestimmen(rng):
    while True:
        n = rng.choice([4, 6, 8, 9, 10, 12])
        m = rng.choice([2, 3, 4, 5, 6])
        c = rng.randint(1, 5)
        if (c * n) % m == 0 and c % m != 0:        # wohldefiniert: m | c n; nicht alles im Kern
            break
    kern = {x for x in range(n) if (c * x) % m == 0}
    bild = {(c * x) % m for x in range(n)}
    zeilen = [(f"{c} \\cdot {x} = {c * x}", f"$[{c * x}]_{{{m}}}$, " + ("gleich $[0]$: gehört zum Kern" if (c * x) % m == 0 else "ungleich $[0]$")) for x in range(min(n, 5))]
    falsch = [(mtext({0}), "Der Kern ist nicht nur $\\{[0]\\}$: Prüfe weitere Elemente, die auf $[0]$ abgebildet werden."),
              (mtext(bild), "Das ist das Bild $f(G)$, nicht der Kern."),
              (mtext(set(range(n))), "Das ist ganz $G$. Nur Elemente mit $c x \\equiv 0$ gehören zum Kern.")]
    return {"frage": f"Die Abbildung $f\\colon \\mathbb{{Z}}/{n}\\mathbb{{Z}} \\to \\mathbb{{Z}}/{m}\\mathbb{{Z}}$, $[x]_{{{n}}} \\mapsto [{c}x]_{{{m}}}$ ist ein Gruppenhomomorphismus. Bestimme $\\ker(f)$ als Menge der Vertreter $r \\in \\{{0, \\ldots, {n - 1}\\}}$, zum Beispiel `{{0; 3}}`.",
            "loesung": mtext(kern),
            "tipps": ["Gesucht sind alle $[x]$, die auf $[0]$ abgebildet werden.", f"Prüfe für $x = 0, 1, 2, \\ldots$, ob ${c}x$ durch ${m}$ teilbar ist.", f"Die Vertreter sind {mtex(kern)}."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Der Kern ist die Urbildmenge von $e_H = [0]$: $\\ker(f) = \\{g \\in G \\mid f(g) = e_H\\}$ (Def. 3.40).",
            "typische_fehler": ohne_gleiche(mtext(kern), falsch)}


def hom_pruefen(rng):
    c = rng.randint(2, 7)
    wahl = rng.choice(["mal", "neg", "plus", "quad", "betrag", "linpl"])
    fs = {"mal": (lambda x: c * x, f"{c}k"), "neg": (lambda x: -c * x, f"-{c}k"), "plus": (lambda x: x + c, f"k + {c}"),
          "quad": (lambda x: x * x, "k^2"), "betrag": (lambda x: abs(x) * c, f"{c}|k|"), "linpl": (lambda x: c * x + 1, f"{c}k + 1")}
    f, term = fs[wahl]
    R = range(-6, 7)
    if f(0) != 0:
        befund, zeuge = "N", f"$f(0) = {f(0)} \\ne 0$"
    else:
        paar = next(((a, b) for a in R for b in R if f(a + b) != f(a) + f(b)), None)
        if paar:
            a, b = paar
            befund, zeuge = "G", f"$f({a} + {b}) = {f(a + b)}$, aber $f({a}) + f({b}) = {f(a) + f(b)}$"
        else:
            befund, zeuge = "H", "Es gilt $f(a + b) = f(a) + f(b)$"
    H_ = "ein Gruppenhomomorphismus"
    N_ = "kein Homomorphismus: $f(0) \\ne 0$"
    G_ = "kein Homomorphismus: es gibt $a, b$ mit $f(a + b) \\ne f(a) + f(b)$, obwohl $f(0) = 0$"
    korrekt = {"H": H_, "N": N_, "G": G_}[befund]
    optionen = [korrekt] + [o for o in (H_, N_, G_) if o != korrekt]
    fehler = {o: f"Prüfe zuerst $f(0)$, dann ein Paar $a, b$. Hier gilt: {zeuge}." for o in optionen[1:]}
    return {"typ": "mc",
            "frage": f"Die Abbildung $f\\colon (\\mathbb{{Z}}, +) \\to (\\mathbb{{Z}}, +)$, $k \\mapsto {term}$ ist …",
            "optionen": optionen, "fehler": fehler,
            "tipps": ["Ein Homomorphismus muss $0$ auf $0$ schicken. Berechne $f(0)$.", "Wenn $f(0) = 0$: Probiere kleine Zahlen für $f(a + b)$ gegen $f(a) + f(b)$.", "Beachte negative Zahlen."],
            "rechenweg": rechnung([("\\text{Homomorphiebedingung prüfen}", zeuge)]),
            "erklaerung": "Jede Abbildung $k \\mapsto ck$ ist ein Homomorphismus von $(\\mathbb{Z}, +)$ nach $(\\mathbb{Z}, +)$. Verschiebungen, Quadrate und Beträge erhalten die Addition nicht."}


k.generator(untergruppe_pruefen, typ="mc", titel="Untergruppe von Z/nZ oder nicht?")
k.generator(erzeugte_untergruppe, typ="menge", titel="Erzeugte Untergruppe in Z/nZ")
k.generator(hom_pruefen, typ="mc", titel="Homomorphismus (Z,+) nach (Z,+)?")
k.generator(kern_bestimmen, typ="menge", titel="Kern eines Homomorphismus Z/nZ nach Z/mZ")

k.rechenweg_aufgabe(r"""
## Quiz-Stil: Ein Homomorphismus auf $\mathbb{Z}/6\mathbb{Z}$

Sei $f\colon (\mathbb{Z}/6\mathbb{Z}, +) \to (\mathbb{Z}/6\mathbb{Z}, +)$, $[n] \mapsto [2n]$. (Das ist ein Gruppenhomomorphismus.)
""",
    [{"typ": "menge", "frage": "Bestimme $\\ker(f)$ als Menge der Vertreter $r \\in \\{0, \\ldots, 5\\}$.", "loesung": "{0; 3}",
      "tipps": ["Gesucht: $2n \\equiv 0 \\pmod 6$.", "$n = 3$: $2 \\cdot 3 = 6$."], "rechenweg": ":::rechnung\n2 \\cdot 3 = 6 || $[6]_6 = [0]_6$, also $[3] \\in \\ker(f)$\n:::",
      "erklaerung": "$2n \\equiv 0 \\pmod 6 \\iff 3 \\mid n$."},
     {"typ": "menge", "frage": "Bestimme das Bild $f(\\mathbb{Z}/6\\mathbb{Z})$ als Menge der Vertreter.", "loesung": "{0; 2; 4}",
      "tipps": ["Rechne $2n \\bmod 6$ für $n = 0, \\ldots, 5$.", "Werte doppelte Ergebnisse nur einmal."], "rechenweg": ":::rechnung\n(2 \\cdot 5) \\bmod 6 = 4 || $f([5]) = [4]$\n:::",
      "erklaerung": "Werte $0, 2, 4, 0, 2, 4$: Bild $\\{[0], [2], [4]\\}$, eine Untergruppe von $\\mathbb{Z}/6\\mathbb{Z}$ (Satz 3.38 (iii))."},
     {"typ": "wf", "frage": "$f$ ist injektiv.", "wahr": False,
      "tipps": ["Satz 3.42: Injektiv genau dann, wenn $\\ker(f)$ trivial ist."], "erklaerung": "$\\ker(f) = \\{[0], [3]\\} \\ne \\{[0]\\}$: nicht injektiv, denn $f([0]) = f([3]) = [0]$."}],
    "Der Kern ist $\\{[0], [3]\\}$, das Bild $\\{[0], [2], [4]\\}$. Wegen $3 \\cdot 2 = 6$ passen beide in die Formel $|G| = |\\ker| \\cdot |\\mathrm{Bild}|$ (später: Dimensionsformel für Vektorräume).",
    uebungsblatt=True,
    tipps=["Berechne $f$ auf allen sechs Elementen.", "Der Kern besteht aus allen $[n]$ mit $f([n]) = [0]$."],
    rechenweg=r"""
:::rechnung
2 \cdot 0 = 0 || $f([0]) = [0]$
2 \cdot 3 = 6 || $f([3]) = [6] = [0]$
2 \cdot 4 = 8 || $f([4]) = [8] = [2]$
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Der Kern ist eine Untergruppe (Satz 3.41)

Sei $f\colon (G, \ast) \to (H, \star)$ ein Gruppenhomomorphismus. Zeigen Sie mit dem Untergruppenkriterium, dass $\ker(f)$ eine Untergruppe von $G$ ist.
""",
    r"""
Nach Satz 3.38 (i) gilt $f(e_G) = e_H$, also $e_G \in \ker(f)$ und $\ker(f) \ne \emptyset$.
Seien $a, b \in \ker(f)$. Mit der Homomorphieeigenschaft und Satz 3.38 (ii) gilt
$$f(a \ast b^{-1}) = f(a) \star f(b^{-1}) = f(a) \star f(b)^{-1} = e_H \star e_H^{-1} = e_H.$$
(Letzter Schritt: $e_H^{-1} = e_H$ nach Satz 3.17.) Also $a \ast b^{-1} \in \ker(f)$. Mit Satz 3.24 folgt: $\ker(f)$ ist Untergruppe. $\square$
""",
    ["$\\ker(f) \\ne \\emptyset$ über $f(e_G) = e_H$ begründet",
     "$f(a \\ast b^{-1})$ mit der Homomorphieeigenschaft und $f(b^{-1}) = f(b)^{-1}$ umgeformt",
     "$f(a) = f(b) = e_H$ eingesetzt und $e_H \\star e_H^{-1} = e_H$ gerechnet",
     "Mit Satz 3.24 abgeschlossen"],
    "Bei Homomorphismen reicht es, mit Satz 3.38 (i) und (ii) umzuformen und dann das Untergruppenkriterium zu benutzen.",
    uebungsblatt=True,
    tipps=["Welche beiden Bedingungen verlangt das Untergruppenkriterium?", "Benutze Satz 3.38 (ii), um $f(b^{-1})$ umzuschreiben."])

k.papier(r"""
## Übungsblatt-Stil: Bild und Abelsch-Sein (Satz 3.38 (iii) und (iv))

Sei $f\colon (G, \ast) \to (H, \star)$ ein Gruppenhomomorphismus.

1. Zeigen Sie, dass $f(G)$ eine Untergruppe von $H$ ist.
2. Zeigen Sie: Ist $G$ abelsch, so ist $f(G)$ abelsch.
""",
    r"""
**1.** Nach Satz 3.38 (i) ist $e_H = f(e_G) \in f(G)$, also $f(G) \ne \emptyset$. Seien $x, y \in f(G)$, etwa $x = f(a)$, $y = f(b)$.
Dann $x \star y^{-1} = f(a) \star f(b)^{-1} = f(a) \star f(b^{-1}) = f(a \ast b^{-1}) \in f(G)$ (Satz 3.38 (ii) und Homomorphie). Mit Satz 3.24 ist $f(G)$ eine Untergruppe.
**2.** Für $x = f(a)$, $y = f(b)$ gilt $x \star y = f(a \ast b) = f(b \ast a) = y \star x$, denn $G$ ist abelsch. $\square$
""",
    ["Nichtleerheit von $f(G)$ über $e_H = f(e_G)$ begründet",
     "Beliebige $x, y \\in f(G)$ als $f(a)$, $f(b)$ geschrieben und $x \\star y^{-1}$ als $f(a \\ast b^{-1})$ erkannt",
     "Untergruppenkriterium Satz 3.24 abschließend benutzt",
     "Für (2) die Kommutativität von $G$ **vor** dem Zurückübersetzen benutzt"],
    "Das Bild eines Homomorphismus ist immer eine Struktur derselben Art (Untergruppe, abelsch). Diese Beweise arbeiten mit Vertretern $a, b$ der Elemente von $f(G)$.",
    uebungsblatt=True,
    tipps=["Jedes Element von $f(G)$ hat die Form $f(a)$ mit $a \\in G$.", "Das Ziel ist, $x \\star y^{-1}$ als $f$ von etwas zu schreiben."])

k.papier(r"""
## Übung zu Satz 3.27: Die erzeugte Untergruppe ist die kleinste

Zeigen Sie: Für $M \subseteq G$ ist $\langle M \rangle$ eine Untergruppe von $G$ mit $M \subseteq \langle M \rangle$, und für jede Untergruppe $U$ mit $M \subseteq U$ gilt $\langle M \rangle \subseteq U$.
""",
    r"""
Die Menge $\mathcal{U} := \{U \subseteq G \mid U \text{ Untergruppe}, M \subseteq U\}$ ist nichtleer, denn $G \in \mathcal{U}$.
Nach Satz 3.25 ist $\langle M \rangle = \bigcap_{U \in \mathcal{U}} U$ eine Untergruppe. Jedes $U \in \mathcal{U}$ enthält $M$, also auch der Schnitt: $M \subseteq \langle M \rangle$.
Ist $U'$ eine Untergruppe mit $M \subseteq U'$, so ist $U' \in \mathcal{U}$ und daher $\langle M \rangle \subseteq U'$ (ein Schnitt liegt in jeder beteiligten Menge). $\square$
""",
    ["$\\mathcal{U} \\ne \\emptyset$ durch $G \\in \\mathcal{U}$ begründet",
     "Satz 3.25 auf den Schnitt angewendet",
     "$M \\subseteq \\langle M \\rangle$ aus $M \\subseteq U$ für alle $U \\in \\mathcal{U}$ geschlossen",
     "Minimalität: $U' \\in \\mathcal{U}$ und daher $\\langle M \\rangle \\subseteq U'$"],
    "Die erzeugte Untergruppe ist ein Schnitt aller Untergruppen, die $M$ enthalten. Deshalb ist sie in jeder von ihnen enthalten.",
    tipps=["Welche Mengen werden geschnitten? Ist ihre Familie nichtleer?", "Ein Schnitt ist in jeder geschnittenen Menge enthalten."])

k.zusammenfassung(r"""
## Untergruppen und Gruppenhomomorphismen (Skript Abschn. 3.2, Def. 3.19 bis Bsp. 3.45)

- **Untergruppe** (Def. 3.19): $U \subseteq G$ mit $(U, \ast|_{U^2})$ Gruppe. $n\mathbb{Z} \le \mathbb{Z}$ (3.20), $\mathbb{N}$ nicht (3.21), $R$ ja (3.22), $S$ nein (3.23).
- **Untergruppenkriterium** (Satz 3.24): $U \ne \emptyset$ und $a \ast b^{-1} \in U$ für alle $a, b \in U$. Schnitte von Untergruppen sind Untergruppen (Satz 3.25).
- **Erzeugte Untergruppe** (Def. 3.26): $\langle M \rangle = \bigcap\{U \mid U \text{ Untergruppe},\ M \subseteq U\}$, kleinste Untergruppe mit $M$ (Satz 3.27). $\langle \{n\} \rangle = n\mathbb{Z}$, $\langle \{r\} \rangle = R$, $B_n = \langle \{e_1, \ldots, e_n\} \rangle$.
- **Gruppenhomomorphismus** (Def. 3.32): $f(a \ast b) = f(a) \star f(b)$. Isomorphismus = bijektiv, Automorphismus = Isomorphismus $G \to G$. Beispiele: $\mathrm{id}$, $g \circ f$, $f^{-1}$, $\pi_n\colon a \mapsto [a]_n$.
- **Satz 3.38:** $f(e_G) = e_H$; $f(g^{-1}) = f(g)^{-1}$; $f(G)$ Untergruppe; $G$ abelsch $\Rightarrow$ $f(G)$ abelsch.
- **Kern** (Def. 3.40): $\ker(f) = \{g \mid f(g) = e_H\}$, Untergruppe (Satz 3.41). **Satz 3.42:** $f$ injektiv $\iff \ker(f) = \{e_G\}$. $\ker(\pi_n) = n\mathbb{Z}$.

!! Injektivität eines Homomorphismus prüfst du nur am Kern: $\ker(f) = \{e_G\}$.
""")
