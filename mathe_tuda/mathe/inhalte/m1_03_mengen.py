# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 3: Mengen (Skript Disser WS 26/27, Abschn. 1.4).

Deckt ab: Element, ∉ := ¬(e ∈ M), leere Menge, Teil-/Obermenge, Gleichheit, Russell'sche Antinomie,
Aufzählung, ℕ := {0, 1, 2, …}, ℤ, Aussonderung {x ∈ G | E(x)}, ℝ, ℚ, Def. 1.21 (∪, ∩, \\, disjunkt),
Abb. 1.1, Def. 1.22 (Z_{≥0}), Satz 1.23 (Distributivgesetz) mit Beweis, Def. 1.24 (Tupel),
Bem. 1.25, Def. 1.26 (kartesisches Produkt, A^n, A^0 = {()}), Bsp. 1.27, 1.28, Def. 1.29 (Potenzmenge),
Bsp. 1.30, 1.31. Alle Mengen rechnet Python (frozenset, itertools).
"""
import itertools
import json

from ..engine import neues_kapitel

k = neues_kapitel(
    slug="uni_mengen",
    titel="Mengen",
    beschreibung="Aufzählung, Aussonderung, Vereinigung, Schnitt, Differenz, Distributivgesetz, Tupel, kartesisches Produkt und Potenzmenge nach dem Skript",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 1.4",
    icon="🫧")

k.lernziele([
    "Ich kann Mengen durch Aufzählung und durch Aussonderung $\\{x \\in G \\mid E(x)\\}$ angeben und weiß, dass im Skript $0 \\in \\mathbb{N}$ gilt",
    "Ich unterscheide sicher zwischen $\\in$ und $\\subseteq$ und kann Mengengleichheit über zwei Teilmengenbeziehungen zeigen",
    "Ich kann $\\cup$, $\\cap$ und $\\setminus$ (Def. 1.21) berechnen und das Distributivgesetz (Satz 1.23) elementweise beweisen",
    "Ich kann Tupel, kartesische Produkte $A^n$ (auch $A^0$) und Potenzmengen bilden und abzählen",
])

k.warum(r"""
Datenbanken sind Mengen von Tupeln (Zeilen einer Tabelle), SQL-Abfragen sind Aussonderung,
`UNION`, `INTERSECT` und `EXCEPT` sind $\cup$, $\cap$ und $\setminus$. Ein Bitstring aus $n$ Bits
ist ein Element von $\{0, 1\}^n$, und die Potenzmenge beschreibt alle möglichen Auswahlen, etwa
alle Belegungspläne eines Hörsaals. In Python heißen die Werkzeuge `set`, `frozenset` und
`itertools.product`. Das Skript baut später sogar die natürlichen Zahlen aus Mengen.
""")


# ── Hilfen ──────────────────────────────────────────────────────────────────
def _txt(x):
    """Element -> Eingabe-/Anzeigetext im Format des Prüfers."""
    if isinstance(x, frozenset):
        return "{" + "; ".join(_txt(y) for y in sorted(x, key=_sortkey)) + "}" if x else "{}"
    if isinstance(x, tuple):
        return "(" + "; ".join(_txt(y) for y in x) + ")"
    return str(x)


def _sortkey(x):
    if isinstance(x, frozenset):
        return (1, len(x), str(sorted(_sortkey(y) for y in x)))
    if isinstance(x, tuple):
        return (2, len(x), str([_sortkey(y) for y in x]))
    return (0, 0, x) if isinstance(x, int) else (0, 1, str(x))


def _menge(it):
    return _txt(frozenset(it))


def _tex(x):
    """Element/Menge -> LaTeX im Stil des Skripts (Komma, \\emptyset)."""
    if isinstance(x, frozenset):
        return "\\{" + ", ".join(_tex(y) for y in sorted(x, key=_sortkey)) + "\\}" if x else "\\emptyset"
    if isinstance(x, tuple):
        return "(" + ", ".join(_tex(y) for y in x) + ")"
    return str(x)


def _potenzmenge(m):
    m = sorted(m, key=_sortkey)
    return frozenset(frozenset(c) for r in range(len(m) + 1) for c in itertools.combinations(m, r))


def _venn(mengen, markiert=None, universum=None, einr="    ", **extra):
    d = {"mengen": [{"name": n, "elemente": sorted(e)} for n, e in mengen]}
    if universum is not None:
        d["universum"] = sorted(universum)
    if markiert:
        d["markiert"] = markiert
    d.update(extra)
    return ":::visual venn\n" + einr + json.dumps(d, ensure_ascii=False) + "\n" + einr + ":::"


# Beispiele aus dem Skript, von Python nachgerechnet
_B3 = frozenset(itertools.product([0, 1], repeat=3))                  # Beispiel 1.27
assert len(_B3) == 8
_TAGE = ["Mo", "Di", "Mi", "Do", "Fr"]
_ZEITEN = ["8:00", "9:50", "11:40", "13:30", "15:20", "17:10"]
_SLOTS = list(itertools.product(_TAGE, _ZEITEN))                       # Beispiel 1.28
assert len(_SLOTS) == 30
_P01 = _potenzmenge({0, 1})                                            # Beispiel 1.30
assert len(_P01) == 4

# ── 1: Menge, Element, Teilmenge ─────────────────────────────────────────────
k.erklaerung("Mengen, Elemente, Teilmengen", r"""
    ## Was eine Menge ist

    Anschaulich ist eine [[Menge]] eine **ungeordnete** Sammlung von [[Elementen|Element]]. Reihenfolge
    und Wiederholungen spielen keine Rolle. Das Skript benutzt diese Schreibweisen:

    :::rechnung Grundbegriffe aus dem Skript
    e_1, \ldots, e_n \in M || die Elemente $e_1, \ldots, e_n$ liegen in $M$
    (e \notin M) := \neg(e \in M) || „$e$ ist nicht Element von $M$“, als Negation definiert
    \emptyset = \{\} || [[leere Menge]]: enthält kein Element
    M_1, \ldots, M_n \subseteq M \text{ bzw. } M \supseteq M_1, \ldots, M_n || [[Teilmengen|Teilmenge]] von $M$, $M$ ist [[Obermenge]]
    M' = M \ :\Leftrightarrow\ M' \subseteq M \text{ und } M \subseteq M' || gleich heißt: dieselben Elemente
    :::

    Gleichheit zeigst du also immer in **zwei Richtungen**. Das ist das Muster für Satz 1.23.

    :::achtung $\in$ und $\subseteq$ verwechseln
    Für $M = \{1, \{1, 2\}\}$ gilt $\{1, 2\} \in M$ (es ist ein Element), aber $\{1, 2\} \not\subseteq M$,
    denn $2 \notin M$. Dagegen gilt $\{1\} \subseteq M$ und $\emptyset \subseteq M$.
    :::

    :::alt Mit Kisten erklärt
    Eine Menge ist eine Kiste. $\in$ fragt: Liegt dieser Gegenstand in der Kiste? $\subseteq$ fragt:
    Liegt **jeder** Gegenstand aus der kleinen Kiste auch in der großen? Eine Kiste darf selbst in
    einer Kiste liegen, dann ist sie ein Element, ihr Inhalt aber nicht automatisch.
    :::
    ---
    ## Die Russell'sche Antinomie

    Das Skript definiert „Menge“ bewusst nicht formal, denn das ist überraschend schwierig. Die
    Sammlung $S$ aller Mengen, die sich nicht selbst enthalten, **kann keine Menge sein**:

    :::rechnung Fallunterscheidung: $S \in S$ oder $S \notin S$
    S \in S \Rightarrow S \notin S || $S$ enthält nur Mengen, die sich nicht selbst enthalten
    S \notin S \Rightarrow S \in S || $S$ erfüllt die Bedingung, gehört also hinein
    \text{Beide Fälle: Widerspruch} || also ist $S$ keine Menge ([[Russell'sche Antinomie]])
    :::

    Diese Krise der Mathematik führte dazu, nur bestimmte Erzeugungsweisen von Mengen zu erlauben.
    Genau die lernst du jetzt: Aufzählung, Aussonderung, Produkt, Potenzmenge.

    :::alt Mit dem Barbier erklärt
    Im Dorf rasiert der Barbier genau alle Männer, die sich nicht selbst rasieren. Rasiert er sich
    selbst? Wenn ja, gehört er nicht zu seinen Kunden, darf sich also nicht rasieren. Wenn nein,
    gehört er dazu und muss sich rasieren. Den Barbier kann es nicht geben, genauso wenig wie $S$.
    :::
    """)

_M = frozenset({1, frozenset({1, 2})})
_kand = [("$1 \\in M$", 1 in _M), ("$\\{1, 2\\} \\in M$", frozenset({1, 2}) in _M),
         ("$\\{1\\} \\subseteq M$", frozenset({1}) <= _M), ("$\\emptyset \\subseteq M$", frozenset() <= _M),
         ("$2 \\in M$", 2 in _M), ("$\\{1, 2\\} \\subseteq M$", frozenset({1, 2}) <= _M)]
k.mehrfach("Es sei $M := \\{1, \\{1, 2\\}\\}$. Welche Aussagen gelten?",
           [t for t, w in _kand if w], [t for t, w in _kand if not w],
           "$M$ hat genau zwei Elemente: die Zahl $1$ und die Menge $\\{1, 2\\}$. Die $2$ steckt nur **in** einem Element, "
           "sie ist selbst kein Element von $M$. Darum ist $\\{1, 2\\}$ Element, aber keine Teilmenge. "
           "$\\emptyset$ ist Teilmenge jeder Menge.",
           tipps=["Zähle zuerst die Elemente von $M$: Es sind zwei.",
                  "$X \\subseteq M$ heißt: **jedes** Element von $X$ ist Element von $M$."],
           fehler={"$2 \\in M$": "Die $2$ liegt in der inneren Menge $\\{1, 2\\}$, nicht direkt in $M$.",
                   "$\\{1, 2\\} \\subseteq M$": "Dafür müsste $2 \\in M$ gelten. $\\{1, 2\\}$ ist ein **Element** von $M$, keine Teilmenge."})

k.wf("Für jede Menge $M$ gilt $\\emptyset \\subseteq M$.", True,
     "$\\emptyset \\subseteq M$ heißt: Jedes Element von $\\emptyset$ liegt in $M$. Da $\\emptyset$ keine Elemente hat, "
     "gibt es nichts zu prüfen (wie bei ex falso quodlibet: „$e \\in \\emptyset \\Rightarrow e \\in M$“ ist immer wahr).",
     tipps=["Suche ein Element von $\\emptyset$, das nicht in $M$ liegt. Gibt es eins?"])

k.mc("Warum kann die Sammlung $S$ aller Mengen, die sich nicht selbst enthalten, keine Menge sein?",
     ["Sowohl $S \\in S$ als auch $S \\notin S$ führen zu einem Widerspruch.",
      "Weil $S$ unendlich viele Elemente hätte.",
      "Weil $S$ leer ist.",
      "Weil eine Menge sich nie selbst enthalten darf."],
     "Russell'sche Antinomie: Aus $S \\in S$ folgt $S \\notin S$, aus $S \\notin S$ folgt $S \\in S$. "
     "Da einer der beiden Fälle eintreten müsste (Fallunterscheidung), ist die Annahme „$S$ ist eine Menge“ falsch.",
     tipps=["Prüfe beide Fälle: $S \\in S$ und $S \\notin S$.", "Das ist ein Widerspruchsbeweis mit Fallunterscheidung."],
     fehler={"Weil $S$ unendlich viele Elemente hätte.": "Unendliche Mengen sind erlaubt, etwa $\\mathbb{N}$. Das Problem ist der Selbstbezug.",
             "Weil $S$ leer ist.": "$S$ ist nicht leer: $\\emptyset$ enthält sich nicht selbst, wäre also ein Element von $S$."})

# ── 2: Aufzählung, Aussonderung, Zahlenmengen ────────────────────────────────
k.erklaerung("Aufzählung und Aussonderung", r"""
    ## Aufzählung

    Die einfachste Art, eine Menge zu erzeugen: Elemente in geschweiften Klammern aufzählen,
    auch unendlich mit Pünktchen.

    :::rechnung Aufzählungen aus dem Skript
    \{0, 1, 2, 3, 4, 5\} || natürliche Zahlen kleiner $6$
    \{\neg, \lor, \land, \Rightarrow, \Leftrightarrow\} || die Verknüpfungen aus Abschnitt 1.2
    \{\ldots, -4, -2, 0, 2, 4, 6, \ldots\} || die geraden Zahlen
    \mathbb{N} := \{0, 1, 2, 3, \ldots\} || [[natürliche Zahlen|natürliche Zahl]], **mit** $0$
    \mathbb{Z} := \{\ldots, -2, -1, 0, 1, 2, \ldots\} || [[ganze Zahlen|ganze Zahl]]
    :::

    :::achtung $\mathbb{N}$ im Skript von Prof. Disser enthält die $0$
    Im Vorkurs galt $\mathbb{N} = \{1, 2, 3, \ldots\}$ und $\mathbb{N}_0 = \{0, 1, 2, \ldots\}$.
    In Mathe 1 gilt $\mathbb{N} = \{0, 1, 2, \ldots\}$, die positiven natürlichen Zahlen heißen
    $\mathbb{N} \setminus \{0\}$. Beide Konventionen sind in der Literatur üblich. Lies bei jeder
    Aufgabe nach, welche gilt. In Quiz und Klausur zählt die des Skripts.
    :::

    :::alt Mit Programmieren erklärt
    Eine Aufzählung ist ein Literal wie `{0, 1, 2, 3, 4, 5}` in Python. Eine unendliche
    Aufzählung mit Pünktchen ist eher wie `range` ohne Ende: Man gibt den Anfang und das Muster an,
    und jeder weiß, wie es weitergeht. In Python startet `range(6)` übrigens auch bei $0$.
    :::
    ---
    ## Aussonderung

    Aus einer [[Grundmenge]] $G$ sondern wir alle Elemente mit einer Eigenschaft aus ([[Aussonderung]]):
    $$\{x \in G \mid E(x)\},$$
    wobei $E(x)$ eine [[Aussageform]] ist. Gelesen: „alle $x$ aus $G$, für die $E(x)$ gilt“.

    :::rechnung Beispiele aus dem Skript
    \{0, 1, 2, 3, 4, 5\} = \{n \in \mathbb{N} \mid n \le 5\} || die $0$ gehört dazu
    \{\ldots, -2, 0, 2, \ldots\} = \{n \in \mathbb{Z} \mid n \text{ ist gerade}\} || $E(n)$: Def. 1.15
    \mathbb{N} = \{n \in \mathbb{Z} \mid n \ge 0\} || $\mathbb{N}$ als Teil von $\mathbb{Z}$
    \mathbb{Q} := \{x \in \mathbb{R} \mid x = \tfrac{a}{b} \text{ mit } a \in \mathbb{Z},\ b \in \mathbb{N},\ b > 0\} || [[rationale Zahlen|rationale Zahl]] aus den [[reellen Zahlen|reelle Zahl]] $\mathbb{R}$
    :::

    :::alt Mit einem Filter erklärt
    Aussonderung ist ein Filter, wie `[x for x in G if E(x)]` in Python oder `SELECT * FROM G WHERE E`
    in SQL. Ohne Grundmenge wüsstest du nicht, woraus du filterst. Genau das verhindert Mengen wie
    $S$ aus der Russell'schen Antinomie.
    :::
    """)

_N5 = list(range(0, 6))
k.menge("Gib $\\{n \\in \\mathbb{N} \\mid n \\le 5\\}$ in aufzählender Form an (Konvention des Skripts).",
        _menge(_N5),
        "Im Skript ist $\\mathbb{N} = \\{0, 1, 2, \\ldots\\}$. Also gehören $0, 1, 2, 3, 4, 5$ dazu.",
        tipps=["Mit welcher Zahl beginnt $\\mathbb{N}$ im Skript?", "Prüfe $n = 0$: Ist $0 \\le 5$?",
               "Sechs Elemente: von $0$ bis $5$."],
        rechenweg=r"""
        :::rechnung
        \mathbb{N} = \{0, 1, 2, \ldots\} || Konvention des Skripts
        \{n \in \mathbb{N} \mid n \le 5\} = \{0, 1, 2, 3, 4, 5\} || alle $n$ mit $n \le 5$
        :::
        """,
        typische_fehler=[(_menge(range(1, 6)), "Die $0$ fehlt. Du hast die Vorkurs-Konvention $\\mathbb{N} = \\{1, 2, \\ldots\\}$ benutzt."),
                         (_menge(range(0, 5)), "Bei $\\le$ gehört die $5$ dazu.")])

_Q4 = [n for n in range(-10, 11) if n * n <= 4]
k.menge("Gib $\\{n \\in \\mathbb{Z} \\mid n^2 \\le 4\\}$ in aufzählender Form an.",
        _menge(_Q4),
        "Für ganze $n$ gilt $n^2 \\le 4$ genau für $-2 \\le n \\le 2$.",
        tipps=["Die Grundmenge ist $\\mathbb{Z}$, also auch negative Zahlen.", "$(-2)^2 = 4$ und $(-3)^2 = 9$.",
               "Fünf Elemente."],
        rechenweg=r"""
        :::rechnung
        (-2)^2 = 4 || erfüllt $n^2 \le 4$
        (-3)^2 = 9 || erfüllt es nicht, ebenso $3^2 = 9$
        \{n \in \mathbb{Z} \mid n^2 \le 4\} = \{-2, -1, 0, 1, 2\} || alle ganzen Zahlen dazwischen
        :::
        """,
        typische_fehler=[(_menge([n for n in _Q4 if n >= 0]), "Die Grundmenge ist $\\mathbb{Z}$: Auch $-1$ und $-2$ erfüllen $n^2 \\le 4$."),
                         (_menge([n for n in _Q4 if n * n < 4]), "Bei $\\le$ gehören $\\pm 2$ dazu, denn $(\\pm 2)^2 = 4$.")])

# ── 3: Vereinigung, Schnitt, Differenz ───────────────────────────────────────
_A = frozenset({1, 2, 3, 4})
_B = frozenset({3, 4, 5})
_G = frozenset(range(1, 8))
k.erklaerung("Vereinigung, Schnitt, Mengendifferenz", r"""
    ## Definition 1.21

    Seien $M$ und $N$ Teilmengen einer Grundmenge $G$. Dann ist

    :::rechnung Die drei Operationen per Aussonderung
    M \cup N := \{x \in G \mid x \in M \lor x \in N\} || [[Vereinigung]]
    M \cap N := \{x \in G \mid x \in M \land x \in N\} || [[Schnitt|Durchschnitt]]
    M \setminus N := \{x \in G \mid x \in M \land x \notin N\} || [[Mengendifferenz|Differenzmenge]]
    M \cap N = \emptyset \ :\Leftrightarrow\ M, N \text{ disjunkt} || [[disjunkt]]: keine gemeinsamen Elemente
    """ + f"{_tex(_A)} \\cup {_tex(_B)} = {_tex(_A | _B)}" + r""" || alles, was in einer der beiden liegt
    """ + f"{_tex(_A)} \\cap {_tex(_B)} = {_tex(_A & _B)}" + r""" || nur das Gemeinsame
    """ + f"{_tex(_A)} \\setminus {_tex(_B)} = {_tex(_A - _B)}" + r""" || aus $M$ das entfernen, was in $N$ liegt
    :::

    """ + _venn([("M", _A), ("N", _B)], markiert="M ∩ N", universum=_G,
                unterschrift="Tippe die Flächen an: M ∩ N, M \\ N, N \\ M und außerhalb.") + r"""

    Beachte die Parallele: $\cup$ gehört zu $\lor$, $\cap$ zu $\land$. Schnitt und Differenz brauchen
    keine Grundmenge (man sondert aus $M$ aus), die Vereinigung schon.

    :::alt Mit Kursen erklärt
    $M$ sind die Leute im Mathekurs, $N$ die im Programmierkurs. $M \cup N$: wer in mindestens einem
    sitzt. $M \cap N$: wer in beiden sitzt. $M \setminus N$: wer nur Mathe hat. Disjunkt wären die
    Kurse, wenn niemand beide belegt.
    :::
    ---
    ## Definition 1.22: $Z_{\geq 0}$

    Für $Z \in \{\mathbb{Z}, \mathbb{Q}, \mathbb{R}\}$ definieren wir
    $$Z_{\geq 0} := Z \cap \{x \in Z \mid x \ge 0\}.$$
    Das ist ein Schnitt zweier Mengen: die nichtnegativen Elemente von $Z$.

    :::rechnung Beispiele
    \mathbb{Z}_{\geq 0} = \{0, 1, 2, \ldots\} = \mathbb{N} || nichtnegative ganze Zahlen
    \tfrac{1}{2} \in \mathbb{Q}_{\geq 0},\ -\tfrac{1}{2} \notin \mathbb{Q}_{\geq 0} || Vorzeichen entscheidet
    \sqrt{2} \in \mathbb{R}_{\geq 0},\ \sqrt{2} \notin \mathbb{Q}_{\geq 0} || Satz 1.18
    :::

    :::alt Mit einem Thermometer erklärt
    $\mathbb{R}_{\geq 0}$ sind alle Temperaturen ab dem Gefrierpunkt aufwärts, $0$ eingeschlossen.
    $\mathbb{Z}_{\geq 0}$ sind davon nur die ganzen Grade. Der Index $\geq 0$ schneidet die
    Minusgrade ab, mehr nicht.
    :::
    """)

_M1, _N1 = frozenset({0, 1, 2, 3}), frozenset({2, 3, 4})
k.menge(f"Es seien $M := {_tex(_M1)}$ und $N := {_tex(_N1)}$. Gib $M \\setminus N$ an.",
        _txt(_M1 - _N1),
        "Aus $M$ werden die Elemente entfernt, die auch in $N$ liegen: $2$ und $3$.",
        tipps=["$M \\setminus N = \\{x \\in M \\mid x \\notin N\\}$.", "Welche Elemente von $M$ liegen auch in $N$?",
               "$2$ und $3$ fallen weg."],
        rechenweg=r"""
        :::rechnung
        """ + f"{_tex(_M1)} \\setminus {_tex(_N1)} = {_tex(_M1 - _N1)}" + r""" || $2, 3 \in N$ werden entfernt, die $4$ war nie in $M$
        :::
        """,
        typische_fehler=[(_txt(_N1 - _M1), "Das ist $N \\setminus M$. Die Reihenfolge zählt: Von $M$ wird abgezogen."),
                         (_txt((_M1 - _N1) | (_N1 - _M1)), "Die $4$ liegt gar nicht in $M$, sie kann in $M \\setminus N$ nicht vorkommen.")])

k.wf("Die Mengen $\\{n \\in \\mathbb{Z} \\mid n \\text{ ist gerade}\\}$ und $\\{n \\in \\mathbb{Z} \\mid n \\text{ ist ungerade}\\}$ sind disjunkt.",
     True,
     "Nach Definition 1.15 ist jede ganze Zahl entweder gerade oder ungerade, aber nicht beides. Der Schnitt ist also leer.",
     tipps=["Disjunkt heißt: Der Schnitt ist leer."])

k.mc("Was ist $\\mathbb{Z}_{\\geq 0}$ nach Definition 1.22?",
     ["$\\mathbb{N}$", "$\\mathbb{N} \\setminus \\{0\\}$", "$\\mathbb{Z}$", "$\\{x \\in \\mathbb{R} \\mid x \\ge 0\\}$"],
     "$\\mathbb{Z}_{\\geq 0} = \\{0, 1, 2, \\ldots\\}$, und das ist im Skript genau $\\mathbb{N}$.",
     tipps=["Schreibe die Elemente auf: nichtnegative ganze Zahlen.", "Gehört die $0$ dazu? Gehört sie zu $\\mathbb{N}$?"],
     fehler={"$\\mathbb{N} \\setminus \\{0\\}$": "$0 \\ge 0$ ist wahr, also $0 \\in \\mathbb{Z}_{\\geq 0}$. Im Skript ist auch $0 \\in \\mathbb{N}$.",
             "$\\{x \\in \\mathbb{R} \\mid x \\ge 0\\}$": "Das ist $\\mathbb{R}_{\\geq 0}$. Bei $\\mathbb{Z}_{\\geq 0}$ bleiben nur ganze Zahlen."})

# ── 4: Satz 1.23 ─────────────────────────────────────────────────────────────
_DA, _DB, _DC = frozenset({1, 2, 4, 5}), frozenset({2, 3, 5, 6}), frozenset({4, 5, 6, 7})
assert _DA & (_DB | _DC) == (_DA & _DB) | (_DA & _DC)
k.erklaerung("Das Distributivgesetz beweisen", r"""
    ## Satz 1.23 (Distributivgesetz)

    Für drei Mengen $A, B, C$ gilt $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$ (Distributivgesetz).

    """ + _venn([("A", _DA), ("B", _DB), ("C", _DC)], markiert="A ∩ (B ∪ C)",
                unterschrift="Markiert ist A ∩ (B ∪ C). Vergleiche mit (A ∩ B) ∪ (A ∩ C): dieselbe Fläche.") + r"""

    Ein Bild ist kein Beweis. Gleichheit heißt: **beide** Teilmengenbeziehungen zeigen, elementweise.

    :::rechnung Beweis, Richtung „$\subseteq$“
    (1)\ x \in A \cap (B \cup C) || beliebiges Element links wählen
    (2)\ x \in A \text{ und } x \in B \cup C || Def. 1.21 ($\cap$)
    (3)\ x \in B \text{ oder } x \in C || aus (2), Def. 1.21 ($\cup$): Fallunterscheidung
    (4)\ \text{Fall } x \in B: x \in A \cap B \subseteq (A \cap B) \cup (A \cap C) || mit $x \in A$ aus (2)
    (5)\ \text{Fall } x \in C: x \in A \cap C \subseteq (A \cap B) \cup (A \cap C) || ebenso
    :::

    :::rechnung Beweis, Richtung „$\supseteq$“
    (1)\ x \in (A \cap B) \cup (A \cap C) || beliebiges Element rechts
    (2)\ \text{Fall } x \in A \cap B: x \in A,\ x \in B \subseteq B \cup C || also $x \in A \cap (B \cup C)$
    (3)\ \text{Fall } x \in A \cap C: x \in A,\ x \in C \subseteq B \cup C || also $x \in A \cap (B \cup C)$ $\square$
    :::

    :::alt Mit Logik erklärt
    Übersetze in Aussagen: $a$: „$x \in A$“, $b$, $c$ ebenso. Links steht $a \land (b \lor c)$, rechts
    $(a \land b) \lor (a \land c)$. Diese beiden Aussagen sind äquivalent, das zeigt eine
    Wahrheitstabelle mit $8$ Zeilen. Mengengesetze sind Logikgesetze im Mengenkostüm.
    :::
    """)

k.ordnen("Bringe die Schritte der Richtung $A \\cap (B \\cup C) \\subseteq (A \\cap B) \\cup (A \\cap C)$ aus dem Beweis von Satz 1.23 "
         "in die richtige Reihenfolge.",
         ["Sei $x \\in A \\cap (B \\cup C)$.",
          "Nach Definition 1.21 ist $x \\in A$ und $x \\in B \\cup C$, also $x \\in B$ oder $x \\in C$.",
          "Ist $x \\in B$, so folgt mit $x \\in A$, dass $x \\in A \\cap B$, also $x \\in (A \\cap B) \\cup (A \\cap C)$.",
          "Ist $x \\in C$, so folgt mit $x \\in A$, dass $x \\in A \\cap C$, also $x \\in (A \\cap B) \\cup (A \\cap C)$.",
          "In beiden Fällen gilt $x \\in (A \\cap B) \\cup (A \\cap C)$."],
         "Ein beliebiges Element links wählen, Definitionen auspacken, Fallunterscheidung (Satz 1.19), in jedem Fall rechts ankommen.",
         ablenker=["Sei $x \\in (A \\cap B) \\cup (A \\cap C)$.", "Also ist $x \\in B$ und $x \\in C$."],
         tipps=["Für „links $\\subseteq$ rechts“ startest du mit einem Element von links.",
                "$x \\in B \\cup C$ heißt **oder**, nicht und."])

# ── 5: Tupel und kartesisches Produkt ────────────────────────────────────────
k.erklaerung("Tupel und kartesisches Produkt", r"""
    ## Definitionen 1.24 und 1.26

    Ein [[Tupel]] ist eine Aneinanderreihung endlich vieler Elemente $(a_1, a_2, \ldots, a_n)$ mit
    $n \in \mathbb{N}$. **Im Gegensatz zu einer Menge** ist ein Tupel geordnet und darf Elemente
    mehrfach enthalten. Das [[kartesische Produkt|kartesisches Produkt]] $A_1 \times \cdots \times A_n$
    besteht aus allen Tupeln $(a_1, \ldots, a_n)$ mit $a_1 \in A_1, \ldots, a_n \in A_n$.

    :::rechnung Unterschiede und Abkürzungen
    \{1, 2\} = \{2, 1\} = \{1, 1, 2\} || Mengen: ungeordnet, Doppeltes zählt nicht
    (1, 2) \neq (2, 1) \neq (1, 1, 2) || Tupel: Reihenfolge und Länge zählen
    A^n := A \times \cdots \times A \ (n \text{ Faktoren}) || Abkürzung, wenn alle $A_i = A$
    A^0 := \{()\} || genau ein Element: das leere Tupel ($n = 0 \in \mathbb{N}$)
    """ + "\\{0, 1\\}^3 = \\{" + ", ".join(_tex(t) for t in sorted(_B3)) + "\\}" + r""" || Beispiel 1.27: alle Bitstrings aus $3$ Bits
    :::

    Bemerkung 1.25 (für Interessierte): $(a_1, \ldots, a_n)$ lässt sich als Menge
    $\{(1, a_1), \ldots, (n, a_n)\}$ schreiben, und jedes Paar $(i, a_i)$ als $\{\{i\}, \{i, a_i\}\}$.
    So wird alles auf Mengen zurückgeführt.

    :::alt Mit Passwörtern erklärt
    Ein Passwort ist ein Tupel aus Zeichen: „abba“ und „baab“ sind verschieden, und das „b“ darf
    doppelt vorkommen. Als Menge wären beide nur $\{a, b\}$. Alle Passwörter der Länge $3$ aus den
    Zeichen $0$ und $1$ sind genau $\{0, 1\}^3$. Das leere Passwort ist das leere Tupel $()$.
    :::
    ---
    ## Beispiel 1.28 und die Potenzmenge

    :::rechnung Beispiel 1.28: Vorlesungsslots
    \{\text{Mo}, \ldots, \text{Fr}\} \times \{8{:}00, 9{:}50, 11{:}40, 13{:}30, 15{:}20, 17{:}10\} || jeder Tag mit jeder Zeit
    5 \cdot 6 = 30 || so viele Paare, von $(\text{Mo}, 8{:}00)$ bis $(\text{Fr}, 17{:}10)$
    :::

    **Definition 1.29.** Die [[Potenzmenge]] $\mathcal{P}(M)$ ist die Menge aller Teilmengen von $M$:
    $N \in \mathcal{P}(M) \Leftrightarrow N \subseteq M$.

    :::rechnung Beispiele 1.30 und 1.31
    """ + f"\\mathcal{{P}}(\\{{0, 1\\}}) = {_tex(_P01)}" + r""" || Beispiel 1.30: keins, je eins, beide
    \mathcal{P}(\{\text{Mo}, \ldots, \text{Fr}\} \times \{8{:}00, \ldots, 17{:}10\}) || Beispiel 1.31: alle Belegungspläne eines Raums
    2^{30} = 1073741824 || so viele Belegungspläne (Abzählen kommt in Kapitel 2)
    :::

    :::alt Mit Häkchen erklärt
    Ein Belegungsplan ist eine Liste von $30$ Kästchen, in jedes setzt du ein Häkchen oder nicht.
    Jede Häkchen-Auswahl ist eine Teilmenge der Slots, also ein Element der Potenzmenge.
    Bei zwei Kästchen ($0$ und $1$) gibt es genau die vier Auswahlen aus Beispiel 1.30.
    :::
    """)

k.menge("Gib $\\{0, 1\\}^2$ an. Schreibe Tupel mit runden Klammern und Semikolon, z. B. $(0; 1)$.",
        _txt(frozenset(itertools.product([0, 1], repeat=2))),
        "Alle Paare mit beiden Einträgen aus $\\{0, 1\\}$: $2 \\cdot 2 = 4$ Stück. $(0, 1)$ und $(1, 0)$ sind verschiedene Tupel.",
        tipps=["Ein Element von $\\{0, 1\\}^2$ ist ein Paar $(a_1, a_2)$ mit $a_1, a_2 \\in \\{0, 1\\}$.",
               "Es sind $2 \\cdot 2$ Paare.", "$(0; 0), (0; 1), (1; 0), (1; 1)$"],
        rechenweg=r"""
        :::rechnung
        2 \cdot 2 = 4 || zwei Möglichkeiten je Position
        \{0, 1\}^2 = \{(0, 0), (0, 1), (1, 0), (1, 1)\} || alle aufgezählt
        :::
        """,
        typische_fehler=[("{(0; 0); (0; 1); (1; 1)}", "$(0, 1)$ und $(1, 0)$ sind verschiedene Tupel: Bei Tupeln zählt die Reihenfolge."),
                         ("{0; 1}", "Die Elemente von $\\{0, 1\\}^2$ sind Paare, nicht einzelne Zahlen.")])

k.zahl("Wie viele Elemente hat $A^0$ für eine beliebige Menge $A$ (Definition 1.26)?", 1,
       "$A^0 := \\{()\\}$ enthält genau ein Element: das leere Tupel. Das passt zu $|A|^0 = 1$.",
       tipps=["Schau in Definition 1.26 nach, was $A^0$ ist.", "$A^0$ ist **nicht** die leere Menge.",
              "Das leere Tupel $()$ ist ein Element."],
       rechenweg=r"""
       :::rechnung
       A^0 = \{()\} || Definition 1.26
       2^0 = 1 || passt zur Regel $|A^n| = |A|^n$, z. B. mit $|A| = 2$
       :::
       """,
       typische_fehler=[(0, "$A^0$ ist nicht leer: Es enthält das leere Tupel $()$. $\\{()\\} \\neq \\emptyset$.")])

k.menge("Gib die Potenzmenge $\\mathcal{P}(\\{0, 1\\})$ an (Beispiel 1.30). Die leere Menge kannst du als $\\{\\}$ oder $\\emptyset$ eingeben.",
        _txt(_P01),
        "Alle Teilmengen von $\\{0, 1\\}$: keine Zahl, nur $0$, nur $1$, beide.",
        tipps=["Die Elemente der Potenzmenge sind Mengen.", "Vergiss $\\emptyset$ und $\\{0, 1\\}$ selbst nicht.",
               "Es sind $4$ Teilmengen."],
        rechenweg=r"""
        :::rechnung
        """ + f"\\mathcal{{P}}(\\{{0, 1\\}}) = {_tex(_P01)}" + r""" || keins, je eins, beide
        2^2 = 4 || jedes Element: drin oder nicht
        :::
        """,
        typische_fehler=[(_txt(_P01 - {frozenset()}), "Die leere Menge fehlt. $\\emptyset \\subseteq \\{0, 1\\}$, also $\\emptyset \\in \\mathcal{P}(\\{0, 1\\})$."),
                         (_txt(_P01 - {frozenset({0, 1})}), "$\\{0, 1\\}$ selbst fehlt. Jede Menge ist Teilmenge von sich selbst."),
                         ("{0; 1}", "Die Elemente der Potenzmenge sind **Mengen**: $\\{0\\}$, nicht $0$.")])


# ── Praxis ──────────────────────────────────────────────────────────────────
# (Anzeige-LaTeX, Venn-Ausdruck, Funktion, [(Fehlfunktion, Meldung)])
_AUSDRUECKE = [
    ("A \\cap (B \\cup C)", "A ∩ (B ∪ C)", lambda a, b, c, g: a & (b | c),
     [(lambda a, b, c, g: (a & b) | c, "Du hast $(A \\cap B) \\cup C$ gerechnet. Die Klammer gehört um $B \\cup C$."),
      (lambda a, b, c, g: a | (b & c), "$\\cap$ und $\\cup$ vertauscht.")]),
    ("(A \\cap B) \\cup C", "(A ∩ B) ∪ C", lambda a, b, c, g: (a & b) | c,
     [(lambda a, b, c, g: a & (b | c), "Die Klammer steht um $A \\cap B$, nicht um $B \\cup C$."),
      (lambda a, b, c, g: a & b & c, "Am Ende wird mit $C$ **vereinigt**, nicht geschnitten.")]),
    ("A \\setminus (B \\cup C)", "A \\ (B ∪ C)", lambda a, b, c, g: a - (b | c),
     [(lambda a, b, c, g: (a - b) | c, "Du hast $(A \\setminus B) \\cup C$ gerechnet. Abgezogen wird alles aus $B \\cup C$."),
      (lambda a, b, c, g: a - (b & c), "Abgezogen wird $B \\cup C$, nicht nur $B \\cap C$.")]),
    ("(A \\setminus B) \\cap C", "(A \\ B) ∩ C", lambda a, b, c, g: (a - b) & c,
     [(lambda a, b, c, g: (a - b) | c, "Am Ende wird geschnitten, nicht vereinigt."),
      (lambda a, b, c, g: (b - a) & c, "$A \\setminus B$ und $B \\setminus A$ verwechselt.")]),
    ("A \\cup (B \\cap C)", "A ∪ (B ∩ C)", lambda a, b, c, g: a | (b & c),
     [(lambda a, b, c, g: (a | b) & c, "Die Klammer steht um $B \\cap C$."),
      (lambda a, b, c, g: a & (b | c), "$\\cap$ und $\\cup$ vertauscht.")]),
    ("(A \\cup B) \\setminus C", "(A ∪ B) \\ C", lambda a, b, c, g: (a | b) - c,
     [(lambda a, b, c, g: a | (b - c), "Von **ganz** $A \\cup B$ wird $C$ abgezogen, nicht nur von $B$."),
      (lambda a, b, c, g: c - (a | b), "Die Reihenfolge der Differenz ist vertauscht.")]),
    ("(A \\setminus B) \\cup (B \\setminus A)", "(A \\ B) ∪ (B \\ A)", lambda a, b, c, g: (a - b) | (b - a),
     [(lambda a, b, c, g: a | b, "Die Elemente, die in **beiden** liegen, gehören nicht dazu."),
      (lambda a, b, c, g: a - b, "Der Teil $B \\setminus A$ fehlt.")]),
    ("(G \\setminus A) \\cap B", "A' ∩ B", lambda a, b, c, g: (g - a) & b,
     [(lambda a, b, c, g: a & b, "$G \\setminus A$ sind die Elemente **außerhalb** von $A$."),
      (lambda a, b, c, g: g - (a & b), "Du hast $G \\setminus (A \\cap B)$ gerechnet.")]),
]


def mengen_ausdruck(rng):
    g = frozenset(range(1, 10))
    while True:
        a, b, c = (frozenset(x for x in g if rng.random() < 0.45) for _ in range(3))
        if all(3 <= len(m) <= 6 for m in (a, b, c)):
            break
    tex, markiert, fn, fehl = rng.choice(_AUSDRUECKE)
    soll = fn(a, b, c, g)
    fehler = []
    for f, meldung in fehl:
        w = f(a, b, c, g)
        if w != soll and all(w != x for x, _ in fehler):
            fehler.append((w, meldung))
    nutzt_c = "C" in tex
    mengen = [("A", a), ("B", b)] + ([("C", c)] if nutzt_c else [])
    gegeben = ", ".join(f"${n} := {_tex(m)}$" for n, m in mengen)
    return {
        "typ": "menge",
        "frage": f"Es sei $G := {_tex(g)}$ und {gegeben}. Gib ${tex}$ an.",
        "loesung": _txt(soll),
        "tipps": ["Rechne die Klammer zuerst aus.",
                  "$\\cup$: in mindestens einer Menge; $\\cap$: in beiden; $\\setminus$: in der ersten, aber nicht in der zweiten.",
                  "Prüfe am Ende jedes Element von $G$ einzeln: gehört es dazu?"],
        "rechenweg": (_venn(mengen, markiert=markiert, universum=g, einr="", interaktiv=False,
                            unterschrift="Die markierte Fläche ist die gesuchte Menge.")
                      + f"\n\n:::rechnung\n{tex} = {_tex(soll)} || elementweise nach Def. 1.21\n:::"),
        "erklaerung": f"${tex} = {_tex(soll)}$.",
        "typische_fehler": [(_txt(w), m) for w, m in fehler],
    }


def abzaehlen(rng):
    art = rng.choice(["potenz", "produkt", "hoch", "hoch", "potenz_liste", "produkt_liste"])
    buchst = ["a", "b", "c", "d", "x", "y"]
    if art == "potenz":
        n = rng.randint(2, 6)
        m = frozenset(rng.sample(range(0, 10), n))
        wert = len(_potenzmenge(m))
        return {"typ": "zahl", "frage": f"Wie viele Elemente hat $\\mathcal{{P}}({_tex(m)})$?", "loesung": wert,
                "tipps": ["Jedes Element ist in einer Teilmenge drin oder nicht.", f"Die Menge hat ${n}$ Elemente.",
                          f"$2^{{{n}}}$"],
                "rechenweg": f":::rechnung\n2^{{{n}}} = {wert} || ${n}$-mal: drin oder nicht drin\n:::",
                "erklaerung": f"Eine Menge mit ${n}$ Elementen hat $2^{{{n}}} = {wert}$ Teilmengen, $\\emptyset$ und die Menge selbst mitgezählt.",
                "typische_fehler": [(x, msg) for x, msg in [(2 * n, f"Das ist $2 \\cdot {n}$. Die Anzahl verdoppelt sich mit **jedem** Element: $2^{{{n}}}$."),
                                                            (wert - 2, "Du hast $\\emptyset$ und die Menge selbst vergessen."),
                                                            (n * n, f"Das ist ${n}^2$, nicht $2^{{{n}}}$.")] if x != wert]}
    if art == "produkt":
        p, q = rng.randint(2, 6), rng.randint(2, 6)
        a = frozenset(range(1, p + 1))
        b = frozenset(buchst[:q])
        wert = len(list(itertools.product(a, b)))
        return {"typ": "zahl", "frage": f"Wie viele Elemente hat ${_tex(a)} \\times {_tex(b)}$?", "loesung": wert,
                "tipps": ["Jedes Element links wird mit jedem rechts kombiniert.", f"${p}$ Möglichkeiten vorn, ${q}$ hinten.",
                          f"${p} \\cdot {q}$"],
                "rechenweg": f":::rechnung\n{p} \\cdot {q} = {wert} || jedes Paar $(x, y)$ einmal, wie in Beispiel 1.28\n:::",
                "erklaerung": f"Für jedes der ${p}$ ersten Elemente gibt es ${q}$ zweite: ${p} \\cdot {q} = {wert}$ Paare.",
                "typische_fehler": [(x, msg) for x, msg in [(p + q, "Du hast addiert. Gezählt werden **Paare**: jedes mit jedem, also malnehmen."),
                                                            (2 ** (p * q), "Das wäre die Potenzmenge des Produkts (Beispiel 1.31).")] if x != wert]}
    if art == "hoch":
        g = rng.randint(2, 4)
        n = rng.randint(0, 5)
        while (g, n) == (2, 2):          # dort fallen alle typischen Fehler (g*n, n**g) mit dem Wert 4 zusammen
            n = rng.randint(0, 5)
        a = frozenset(range(g))
        wert = len(list(itertools.product(sorted(a), repeat=n)))
        return {"typ": "zahl", "frage": f"Wie viele Elemente hat ${_tex(a)}^{{{n}}}$ (Definition 1.26)?", "loesung": wert,
                "tipps": ["Ein Element ist ein Tupel der Länge " + f"${n}$" + ".", f"Jede Position hat ${g}$ Möglichkeiten.",
                          f"${g}^{{{n}}}$" + (", und $A^0 = \\{()\\}$" if n == 0 else "")],
                "rechenweg": f":::rechnung\n{g}^{{{n}}} = {wert} || ${n}$ Positionen mit je ${g}$ Möglichkeiten\n:::",
                "erklaerung": (f"${_tex(a)}^{{{n}}}$ besteht aus allen Tupeln der Länge ${n}$: ${g}^{{{n}}} = {wert}$."
                               + (" Für $n = 0$ ist das genau das leere Tupel $()$." if n == 0 else "")),
                "typische_fehler": [(x, msg) for x, msg in [(g * n, f"Das ist ${g} \\cdot {n}$. Bei Tupeln wird je Position malgenommen: ${g}^{{{n}}}$."),
                                                            (0, "$A^0 = \\{()\\}$ ist nicht leer.") if n == 0 else (n ** g, f"Basis und Exponent vertauscht: richtig ist ${g}^{{{n}}}$.")] if x != wert]}
    if art == "potenz_liste":
        m = frozenset(rng.sample(range(0, 10), 2) if rng.random() < 0.5 else rng.sample(buchst, 2))
        p = _potenzmenge(m)
        fehl = [(_txt(p - {frozenset()}), "Die leere Menge fehlt: $\\emptyset$ ist Teilmenge jeder Menge."),
                (_txt(p - {m}), "Die Menge selbst fehlt: Jede Menge ist Teilmenge von sich selbst.")]
        return {"typ": "menge", "frage": f"Gib $\\mathcal{{P}}({_tex(m)})$ an. Die leere Menge kannst du als $\\{{\\}}$ oder $\\emptyset$ eingeben.",
                "loesung": _txt(p),
                "tipps": ["Die Elemente der Potenzmenge sind Mengen.", "Denk an $\\emptyset$ und die ganze Menge.", "Es sind $4$ Teilmengen."],
                "rechenweg": f":::rechnung\n\\mathcal{{P}}({_tex(m)}) = {_tex(p)} || keins, je eins, beide\n:::",
                "erklaerung": f"$\\mathcal{{P}}({_tex(m)}) = {_tex(p)}$.",
                "typische_fehler": fehl}
    # produkt_liste
    a = frozenset(rng.sample(range(1, 6), 2))
    b = frozenset(rng.sample(buchst[:4], rng.randint(1, 2)))
    prod = frozenset(itertools.product(sorted(a), sorted(b)))
    umgedreht = frozenset((y, x) for x, y in prod)
    return {"typ": "menge", "frage": f"Gib ${_tex(a)} \\times {_tex(b)}$ an. Tupel schreibst du mit runden Klammern und Semikolon, z. B. $(1; a)$.",
            "loesung": _txt(prod),
            "tipps": ["Der erste Eintrag kommt aus der ersten Menge, der zweite aus der zweiten.",
                      "Kombiniere jedes Element links mit jedem rechts.", f"Es sind ${len(prod)}$ Paare."],
            "rechenweg": f":::rechnung\n{_tex(a)} \\times {_tex(b)} = {_tex(prod)} || jedes mit jedem\n:::",
            "erklaerung": f"${_tex(a)} \\times {_tex(b)} = {_tex(prod)}$.",
            "typische_fehler": [(_txt(umgedreht), "Die Reihenfolge im Tupel ist vertauscht: Zuerst kommt das Element aus der ersten Menge."),
                                (_txt(a | b), "Gesucht sind Paare, nicht die Vereinigung der beiden Mengen.")]}


k.praxis()

k.generator(mengen_ausdruck, typ="menge", titel="Mengenausdrücke mit drei Mengen berechnen")
k.generator(abzaehlen, typ="zahl", titel="Tupel, Produkte und Potenzmengen")

k.papier(r"""
    ## Übungsblatt-Stil: das zweite Distributivgesetz

    Zeigen Sie für Mengen $A, B, C$:
    $$A \cup (B \cap C) = (A \cup B) \cap (A \cup C).$$
    Führen Sie den Beweis elementweise wie im Beweis von Satz 1.23, mit beiden Inklusionen.
    """,
    r"""
**„$\subseteq$“:** Sei $x \in A \cup (B \cap C)$. Dann ist $x \in A$ oder $x \in B \cap C$ (Def. 1.21).

- Fall $x \in A$: Dann $x \in A \cup B$ und $x \in A \cup C$, also $x \in (A \cup B) \cap (A \cup C)$.
- Fall $x \in B \cap C$: Dann $x \in B$ und $x \in C$, also $x \in A \cup B$ und $x \in A \cup C$, also $x \in (A \cup B) \cap (A \cup C)$.

**„$\supseteq$“:** Sei $x \in (A \cup B) \cap (A \cup C)$. Dann $x \in A \cup B$ und $x \in A \cup C$.

- Fall $x \in A$: Dann $x \in A \cup (B \cap C)$.
- Fall $x \notin A$: Aus $x \in A \cup B$ folgt per Elimination $x \in B$, aus $x \in A \cup C$ ebenso $x \in C$. Also $x \in B \cap C \subseteq A \cup (B \cap C)$.

Beide Fälle decken alles ab ($x \in A$ oder $x \notin A$). Damit gelten beide Inklusionen, also die Gleichheit. $\square$
""",
    ["Ich habe beide Richtungen ($\\subseteq$ und $\\supseteq$) gezeigt",
     "Ich habe mit einem beliebigen Element $x$ angefangen, nicht mit einem Venn-Diagramm",
     "Ich habe in der Richtung „$\\supseteq$“ die Fälle $x \\in A$ und $x \\notin A$ unterschieden (vollständig!)",
     "Ich habe jeden Schritt mit Definition 1.21 oder einer Schlussregel begründet"],
    "Bilder helfen beim Finden, aber der Beweis ist elementweise. Das Muster ist dasselbe wie bei Satz 1.23.",
    uebungsblatt=True,
    tipps=["In der Richtung „$\\supseteq$“ hilft die Fallunterscheidung $x \\in A$ oder $x \\notin A$."])

_ta, _tb = frozenset({1, 2}), frozenset({2, 3})
k.papier(r"""
    ## Übungsblatt-Stil: De Morgan für Mengen

    Zeigen Sie für Mengen $A, B, C$:
    $$A \setminus (B \cup C) = (A \setminus B) \cap (A \setminus C).$$
    Übersetzen Sie dazu „$x \in \ldots$“ in Aussagen und benutzen Sie eine Regel aus Satz 1.14.
    """,
    r"""
Für ein beliebiges $x$ gilt (jede Zeile ist eine Äquivalenz, also zeigt die Kette beide Inklusionen):

$$x \in A \setminus (B \cup C) \Leftrightarrow x \in A \land \neg(x \in B \lor x \in C) \qquad \text{(Def. 1.21)}$$
$$\Leftrightarrow x \in A \land (x \notin B \land x \notin C) \qquad \text{(De Morgan, Satz 1.14)}$$
$$\Leftrightarrow (x \in A \land x \notin B) \land (x \in A \land x \notin C) \qquad (P \Leftrightarrow P \land P)$$
$$\Leftrightarrow x \in (A \setminus B) \cap (A \setminus C) \qquad \text{(Def. 1.21)}$$

Da dies für jedes $x$ gilt, enthalten beide Seiten dieselben Elemente. $\square$
""",
    ["Ich habe $x \\in A \\setminus (B \\cup C)$ mit Definition 1.21 in eine Aussage übersetzt",
     "Ich habe die De-Morgan-Regel $\\neg(P \\lor Q) \\Leftrightarrow \\neg P \\land \\neg Q$ benutzt",
     "Ich habe begründet, warum eine Äquivalenzkette beide Inklusionen liefert",
     "Ich habe mit „für jedes $x$“ und $\\square$ abgeschlossen"],
    "Mengengesetze lassen sich oft mit einer Äquivalenzkette aus der Logik beweisen (Beweis durch Äquivalenzumformung).",
    uebungsblatt=True,
    tipps=["$x \\notin B \\cup C$ ist $\\neg(x \\in B \\lor x \\in C)$."])

k.zusammenfassung(r"""
    ## Mengen (Skript 1.4)

    - $e \in M$: Element; $e \notin M := \neg(e \in M)$; $\emptyset = \{\}$; $N \subseteq M$: jedes Element von $N$ liegt in $M$.
    - $M = M'$ genau dann, wenn $M \subseteq M'$ und $M' \subseteq M$ (zwei Richtungen zeigen).
    - Russell'sche Antinomie: Die Sammlung aller Mengen, die sich nicht selbst enthalten, ist keine Menge.

    !! Im Skript: $\mathbb{N} := \{0, 1, 2, \ldots\}$, positive natürliche Zahlen: $\mathbb{N} \setminus \{0\}$. Im Vorkurs fehlte die $0$.

    | Bildung | Schreibweise |
    |---|---|
    | Aussonderung | $\{x \in G \mid E(x)\}$ |
    | Vereinigung, Schnitt, Differenz | $\{x \in G \mid x \in M \lor x \in N\}$, mit $\land$, mit $\land\ x \notin N$ |
    | disjunkt | $M \cap N = \emptyset$ |
    | $Z_{\geq 0}$ | $Z \cap \{x \in Z \mid x \ge 0\}$, z. B. $\mathbb{Z}_{\geq 0} = \mathbb{N}$ |
    | Tupel | $(a_1, \ldots, a_n)$: geordnet, Wiederholung erlaubt |
    | kartesisches Produkt | $A_1 \times \cdots \times A_n$, $A^n$, $A^0 = \{()\}$ |
    | Potenzmenge | $N \in \mathcal{P}(M) \Leftrightarrow N \subseteq M$ |

    - Satz 1.23: $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$, Beweis elementweise in beide Richtungen.
    - Beispiele: $\{0,1\}^3$ hat $8$ Bitstrings, $5 \cdot 6 = 30$ Vorlesungsslots, $\mathcal{P}(\{0, 1\}) = \{\emptyset, \{0\}, \{1\}, \{0, 1\}\}$.
""")
