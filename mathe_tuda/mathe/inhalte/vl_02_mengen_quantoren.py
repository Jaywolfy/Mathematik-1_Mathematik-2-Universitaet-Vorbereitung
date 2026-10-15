# -*- coding: utf-8 -*-
"""Vorlesung 2 (15.10.2026): Mengen und Quantoren, Skript Disser 1.4 und 1.5, Folien VL02.

Folienreihenfolge: Rückblick VL 1, Menge und Russell, Aufzählung, Aussonderung, Vereinigung/Schnitt/Differenz
(Satz 1.23), Tupel und kartesisches Produkt, Potenzmenge, All- und Existenzquantor, Quantoren negieren,
Vereinigung und Schnitt über Mengensysteme."""
import itertools
import json
from fractions import Fraction as F  # noqa: F401  (für Zahl-Lösungen der Generatoren)

from ..engine import neues_kapitel
from ..visuals import logik_parse, logik_wert

k = neues_kapitel(
    slug="vl02",
    titel="Vorlesung 2: Mengen und Quantoren",
    beschreibung="Mengen, Teilmengen, Aussonderung, Vereinigung und Schnitt, Tupel, Potenzmenge, All- und Existenzquantor, von Null erklärt",
    teil="vorlesung",
    quelle="Vorlesung 2 (15.10.2026), Folien VL 02, Skript Disser 1.4 und 1.5",
    icon="🎓")

k.lernziele([
    "Ich kann erklären, was eine Menge ist, und $\\in$, $\\notin$, $\\subseteq$, $=$ und $\\emptyset$ richtig unterscheiden, etwa $0 \\in \\{0, 1\\}$ und $\\{0\\} \\subseteq \\{0, 1\\}$",
    "Ich kann Mengen durch Aufzählung und Aussonderung angeben und weiß, warum die Aussonderung eine Grundmenge braucht",
    "Ich kann $\\cup$, $\\cap$ und $\\setminus$ bestimmen und eine Mengengleichheit über $\\subseteq$ und $\\supseteq$ beweisen (Satz 1.23)",
    "Ich kann Tupel, kartesisches Produkt und Potenzmenge bilden und ihre Elemente zählen",
    "Ich kann $\\forall$ und $\\exists$ lesen, Quantoraussagen prüfen und negieren und $\\bigcup$, $\\bigcap$ über ein Mengensystem bilden",
])

k.warum(r"""
Mengen und Tupel sind die Sprache der Informatik: Ein Datensatz, ein String, ein Array oder eine Parameterliste
ist ein Tupel, und eine Datenbanktabelle ist im Kern eine Menge von Tupeln, auf der Abfragen mit Vereinigung,
Schnitt und Differenz arbeiten (Datenbanken). Formale Sprachen sind Mengen von Wörtern (AFE), und die Bitstrings $\{0, 1\}^n$ kennst du aus
der Digitaltechnik. Quantoren brauchst du für jede Spezifikation: „für alle Eingaben gilt …“ und „es gibt eine
Eingabe, die …“. Wer sie richtig negiert, findet Gegenbeispiele, also Fehler.
""")


# ── Python rechnet alles nach, was in der Lektion steht ──────────────────────────────────────────
def _vis(typ, **daten):
    return ":::visual " + typ + "\n    " + json.dumps(daten, ensure_ascii=False) + "\n    :::"


def _spalte(formel, variablen=("P", "Q")):
    ast = logik_parse(formel)
    return [logik_wert(ast, dict(zip(variablen, w))) for w in itertools.product([True, False], repeat=len(variablen))]


def _tex(m):
    """LaTeX einer endlichen Menge (Elemente sortiert)."""
    els = sorted(m, key=str)
    return "\\emptyset" if not els else "\\{" + ", ".join(str(e) for e in els) + "\\}"


def _text(m):
    """Antwort-Text für eine Mengenfrage: {a; b}."""
    return "{" + "; ".join(str(e) for e in sorted(m, key=str)) + "}"


def _potenz(m):
    m = list(m)
    return [frozenset(c) for r in range(len(m) + 1) for c in itertools.combinations(m, r)]


# Rückblick (Folie 1)
assert _spalte("P ⇒ Q") == [True, False, True, True]               # falsch nur bei P wahr, Q falsch
assert _spalte("¬(P ∧ Q)") == _spalte("¬P ∨ ¬Q")                     # De Morgan
# Folie 4: Teilmengen und Gleichheit
assert {0, 1} <= {0, 1, 2} and not ({0, 1, 2} <= {0, 1})
assert 0 in {0, 1} and {0} <= {0, 1} and frozenset() not in {0, 1} and frozenset() <= {0, 1}
assert {0, 1, 1} == {1, 0} == {0, 1}
assert frozenset({0}) not in {0, 1}                                  # {0} ist kein Element von {0, 1}
assert len({0, frozenset({0}), frozenset({0, 1})}) == 3
# Folie 5: Aussonderung (auf einem Ausschnitt geprüft)
assert {n for n in range(0, 100) if n <= 5} == {0, 1, 2, 3, 4, 5}
assert {n for n in range(-50, 51) if n % 2 == 0} == {n for n in range(-50, 51) if n % 2 == 0 and True}
assert {n for n in range(-50, 51) if n >= 0} == set(range(0, 51))      # ℕ = {n ∈ ℤ | n ≥ 0}
# Folie 6 und 7: Vereinigung, Schnitt, Differenz
_G = {"¬", "∨", "∧", "⇒", "⇔"}
_M, _N = {"¬", "∨", "∧"}, {"∧", "⇒"}
assert _M | _N == {"¬", "∨", "∧", "⇒"} and _M & _N == {"∧"} and _M - _N == {"¬", "∨"} and _N - _M == {"⇒"}
assert all(x in _G for x in _M | _N)
# Satz 1.23 (Distributivgesetz) für alle A, B, C ⊆ {0, 1, 2, 3} nachgerechnet (kein Beweis!)
_ALLE = _potenz(range(4))
assert all(A & (B | C) == (A & B) | (A & C) for A in _ALLE for B in _ALLE for C in _ALLE)
# Folie 8 und 9: Tupel, Produkt
assert (0, 1) != (1, 0) and (0, 0, 1) != (0, 1) and {0, 1} == {1, 0}
assert len(set(itertools.product((0, 1), repeat=3))) == 8
assert sorted(itertools.product((0, 1), repeat=3))[:3] == [(0, 0, 0), (0, 0, 1), (0, 1, 0)]
_TAGE, _ZEITEN = ["Mo", "Di", "Mi", "Do", "Fr"], ["8:00", "9:50", "11:40", "13:30", "15:20", "17:10"]
_SLOTS = list(itertools.product(_TAGE, _ZEITEN))
assert len(_SLOTS) == 30 and _SLOTS[0] == ("Mo", "8:00") and _SLOTS[-1] == ("Fr", "17:10") and ("Do", "9:50") in _SLOTS
assert len(list(itertools.product([0, 1], repeat=0))) == 1                # A⁰ = {()} hat ein Element
assert {a * b for a, b in itertools.product([2, 3], [5])} == {10, 15}      # Beispielrechnung zu A × B
# Folie 10: Potenzmenge
assert set(_potenz({0, 1})) == {frozenset(), frozenset({0}), frozenset({1}), frozenset({0, 1})}
assert len(_potenz({"a", "b", "c"})) == 8 and 2 ** 30 == 1073741824 and 2 ** len(_SLOTS) == 1073741824
# Folie 12: Quantoren
assert not all(n % 2 == 0 for n in range(0, 200)) and any(n % 2 == 0 for n in range(0, 200))
assert not any(n % 2 == 0 for n in (1, 3, 5))
# Folie 13: Quantoren negieren (über allen Teilmengen von {0, 1, 2} und allen Eigenschaften nachgerechnet)
for _bereich in _potenz(range(3)):
    for _eig in itertools.product([False, True], repeat=3):
        _E = dict(zip(range(3), _eig))
        assert (not all(_E[x] for x in _bereich)) == any(not _E[x] for x in _bereich)
        assert (not any(_E[x] for x in _bereich)) == all(not _E[x] for x in _bereich)
# Folie 14: Vereinigung und Schnitt über ein Mengensystem
_GF = {0, 1, 2, 3}
_FAM = [frozenset({0, 1}), frozenset({1, 2}), frozenset({1, 3})]
assert frozenset().union(*_FAM) == frozenset({0, 1, 2, 3}) and frozenset(_GF).intersection(*_FAM) == frozenset({1})
assert {x for x in _GF if all(x in m for m in [])} == _GF and {x for x in _GF if any(x in m for m in [])} == set()


# ═══ Seite 1: Rückblick und Überblick (Folien 1 und 2) ═════════════════════════════════════════════
k.erklaerung("Rückblick auf Vorlesung 1 und Überblick", r"""
    ## Das Fundament prüfen

    :::analogie 🔁 Vor dem Weiterbauen
    Bevor du ein zweites Stockwerk baust, prüfst du, ob das erste trägt. Wann ist ein Versprechen
    gebrochen? Was heißt „nicht beide“? Das sind die beiden Rückblickfragen der Vorlesung.
    :::

    Aussagen sind wahr oder falsch, Aussageformen brauchen eine Belegung. Die Verknüpfungen $\neg, \land, \lor, \oplus,
    \Rightarrow, \Leftrightarrow$ legen Wahrheitstabellen fest. Dazu kommen die fünf Beweisformen der Folie 1. Heute
    folgen im Kapitel 1 (Folie 2) die **Mengen** und die **Quantoren**. Beide stützen sich auf die Logik: Mengen werden mit
    Aussageformen gebildet, und $\cup$ und $\cap$ entsprechen $\lor$ und $\land$.

    """ + _vis("wahrheitstabelle", variablen=["P", "Q"], ausdruecke=["P ⇒ Q", "¬(P ∧ Q)", "¬P ∨ ¬Q"],
               unterschrift="Antworten auf die Rückblickfragen: $P \\Rightarrow Q$ ist nur in Zeile 2 falsch. $\\neg(P \\land Q)$ und $\\neg P \\lor \\neg Q$ haben dieselbe Spalte.") + r"""

    :::rechnung Die Zusammenfassung von Vorlesung 1 (Folie 1)
    P \Rightarrow Q || Direkter Beweis: P annehmen, Q herleiten
    P \Leftrightarrow R_1 \Leftrightarrow \cdots \Leftrightarrow Q || Äquivalenzumformung: Kette, jeder Schritt in beide Richtungen
    (P \Rightarrow Q) \Leftrightarrow (\neg Q \Rightarrow \neg P) || Kontraposition: ¬Q annehmen, ¬P herleiten
    (P \land \neg Q) \Rightarrow (R \land \neg R) || Widerspruch: gilt das, folgt (P ⇒ Q)
    ((P \Rightarrow R) \land (Q \Rightarrow R)) \Rightarrow ((P \lor Q) \Rightarrow R) || Fallunterscheidung: jeder Fall einzeln
    :::

    :::alt Als Bauplan
    Kapitel 1 heißt „Grundlagen“ und hat drei Teile: Logik (Vorlesung 1), Mengen (heute) und Abbildungen (später). Die
    Logik ist das Werkzeug, die Mengen sind das Material. Mit Werkzeug ohne Material kannst du nichts
    bauen, mit Material ohne Werkzeug nichts bearbeiten. Deshalb steht die Logik zuerst.
    :::
    """)

k.mc("Rückblick, Folie 1: Wann ist $P \\Rightarrow Q$ falsch?",
     ["$P$ wahr und $Q$ falsch.", "$P$ falsch und $Q$ wahr.", "$P$ falsch und $Q$ falsch.", "$P$ wahr und $Q$ wahr."],
     "Ein Versprechen ist nur gebrochen, wenn die Bedingung eintritt ($P$ wahr) und das Versprochene nicht ($Q$ falsch).",
     tipps=["Denk an „Wenn du bestehst, bekommst du ein Eis.“ Wann hat jemand das Versprechen gebrochen?",
            "Ist $P$ falsch, ist die Implikation immer wahr."],
     fehler={"$P$ falsch und $Q$ wahr.": "Ist $P$ falsch, ist die Implikation wahr (ex falso quodlibet), egal was $Q$ ist.",
             "$P$ falsch und $Q$ falsch.": "Auch hier ist $P$ falsch, also ist die Implikation wahr."})

k.mc("Rückblick, Folie 1: Wie lässt sich $\\neg(P \\land Q)$ nur mit $\\neg$ und $\\lor$ ausdrücken?",
     ["$\\neg P \\lor \\neg Q$", "$\\neg P \\land \\neg Q$", "$\\neg(P \\lor Q)$", "$P \\lor Q$"],
     "De Morgan (Satz 1.14): „nicht beide“ heißt „mindestens eines nicht“. Das $\\land$ wird beim Hineinziehen der Negation zu $\\lor$.",
     tipps=["Welche Regel verneint ein „und“?", "Aus $\\land$ wird $\\lor$, und jedes Teilstück wird verneint."],
     fehler={"$\\neg P \\land \\neg Q$": "Das ist die Verneinung von $P \\lor Q$ („keines von beiden“). Beim Verneinen von $\\land$ muss $\\lor$ entstehen.",
             "$P \\lor Q$": "Hier fehlt die Negation: $P \\lor Q$ ist wahr, wenn beide gelten, $\\neg(P \\land Q)$ dann aber falsch."})


# ═══ Seite 2: Menge, Element, Russell (Folie 3, Skript 1.4) ═══════════════════════════════════════
k.erklaerung("Was ist eine Menge? (Skript 1.4)", r"""
    ## Eine Sammlung, in der nur „drin oder nicht“ zählt

    :::analogie 🛍️ Plastiktüte
    In einer Tüte liegen Dinge. Es zählt nur, ob etwas drin ist. Wie oft, und in welcher Reihenfolge,
    ist egal.
    :::

    Eine [[Menge]] ist (ohne formale Definition) eine ungeordnete Sammlung von [[Elementen|Element]]. $e \in M$
    heißt „$e$ ist Element von $M$“, $e \notin M$ heißt „kein Element“. Eine formale Definition ist
    schwierig: Die [[Russellsche Antinomie|Russell'sche Antinomie]] zeigt, dass die Sammlung aller Mengen,
    die sich nicht selbst enthalten, keine Menge sein kann. Deshalb erlauben wir nur unproblematische
    [[Erzeugungsweisen|Erzeugungsweise]].

    :::rechnung Beispiel: Russell'sche Antinomie (Folie 3)
    \text{S: Sammlung aller Mengen, die sich nicht selbst enthalten.} || Annahme: S wäre eine Menge
    \text{Fall 1: } S \in S \Rightarrow S \notin S || S enthält sich selbst, gehört dann nach Definition aber nicht dazu
    \text{Fall 2: } S \notin S \Rightarrow S \in S || S enthält sich nicht, müsste dann aber dazugehören
    \text{Beide Fälle führen zum Widerspruch.} || Fallunterscheidung aus Vorlesung 1
    \text{Also ist S keine Menge.} || Widerspruchsbeweis aus Vorlesung 1
    :::

    :::rechnung Schreibweisen
    2 \in \{1, 2, 3\} || 2 liegt drin
    5 \notin \{1, 2, 3\} || 5 liegt nicht drin
    e_1, \ldots, e_n \in M \text{ steht für } e_1 \in M, \ldots, e_n \in M || Kurzschreibweise
    :::

    :::alt Der Barbier
    Ein Barbier rasiert genau die Männer, die sich nicht selbst rasieren. Rasiert er sich selbst? Dann dürfte er
    es nicht, denn er rasiert nur die, die es nicht selbst tun. Rasiert er sich nicht, müsste er es, weil er
    alle rasiert, die es nicht selbst tun. Beides geht nicht: So einen Barbier kann es nicht geben, und so eine
    Sammlung S ist keine Menge.
    :::
    """)

k.wf("$2 \\in \\{1, 2, 3\\}$ und $5 \\notin \\{1, 2, 3\\}$ sind beide wahr.", True,
     "$2$ ist eines der drei Elemente, $5$ nicht. $e \\notin M$ ist nur die Abkürzung für $\\neg(e \\in M)$.",
     tipps=["Prüfe: Liegt die Zahl in der geschweiften Klammer?"])


# ═══ Seite 3: Aufzählung, Teilmenge, Gleichheit (Folie 4) ═════════════════════════════════════════
k.erklaerung("Aufzählung, Teilmenge, Gleichheit", r"""
    ## Mengen aufschreiben und vergleichen

    :::analogie 🎒 Große und kleine Tüte
    Liegt in der kleinen Tüte nichts, was nicht auch in der großen Tüte läge, ist die kleine eine Teilmenge.
    Eine leere Tüte passt in jede große.
    :::

    Erste Erzeugungsweise: **Aufzählung** der Elemente in $\{\ldots\}$, auch unendlich. $\emptyset := \{\}$ ist die
    [[leere Menge]]. $\mathbb{N} := \{0, 1, 2, \ldots\}$ (mit der $0$) und $\mathbb{Z}$ sind die natürlichen und ganzen
    Zahlen. $N \subseteq M$ heißt: jedes Element von $N$ liegt in $M$, also $e \in N \Rightarrow e \in M$
    ([[Teilmenge]], $M$ ist [[Obermenge]]). $N \not\subseteq M$ steht für $\neg(N \subseteq M)$. $N = M$ heißt: dieselben
    Elemente, also $M \subseteq N$ und $N \subseteq M$ ([[Mengengleichheit]]).

    :::rechnung Beispiele der Folie
    \{0, 1\} \subseteq \{0, 1, 2\} \quad \text{wahr} || 0 und 1 liegen auch rechts
    \{0, 1, 2\} \not\subseteq \{0, 1\} \quad \text{wahr} || die 2 liegt nicht in {0, 1}
    0 \in \{0, 1\} \quad \text{wahr} || 0 ist ein Element
    \{0\} \subseteq \{0, 1\} \quad \text{wahr} || {0} ist eine Menge, und die einzige Zahl darin liegt in {0, 1}
    \emptyset \notin \{0, 1\} \quad \text{wahr} || ∅ ist kein Element von {0, 1}, die Elemente sind nur 0 und 1
    \emptyset \subseteq \{0, 1\} \quad \text{wahr} || es gibt kein Element, das man prüfen müsste (wie ex falso quodlibet)
    \{0, 1, 1\} = \{1, 0\} = \{0, 1\} \quad \text{wahr} || Reihenfolge und Wiederholung zählen bei Mengen nicht
    :::

    :::achtung ∈ und ⊆ sind verschiedene Zeichen
    $0 \in \{0, 1\}$: Das Zeichen $\in$ verbindet ein **Element** mit einer Menge. $\{0\} \subseteq \{0, 1\}$: Das Zeichen
    $\subseteq$ verbindet **zwei Mengen**. $0$ ist die Zahl, $\{0\}$ die Tüte mit der Zahl darin. Deshalb ist
    $\{0\} \in \{0, 1\}$ falsch.
    :::

    :::alt Mit Tüten und Zahlen
    Die Menge {0, 1} ist eine Tüte mit zwei Zetteln, auf denen 0 und 1 stehen. Der Zettel 0 liegt in der Tüte (∈).
    Packst du den Zettel 0 allein in eine kleine Tüte {0}, ist diese kleine Tüte in der Ausgangstüte nicht
    enthalten, weil sie kein Zettel ist. Wohl aber ist ihr Inhalt vollständig in der großen Tüte (⊆).
    :::
    """)

k.mehrfach("Welche Aussagen gelten? (Folie 4)",
           ["$0 \\in \\{0, 1\\}$", "$\\{0\\} \\subseteq \\{0, 1\\}$", "$\\emptyset \\subseteq \\{0, 1\\}$", "$\\{0, 1, 1\\} = \\{1, 0\\}$"],
           ["$\\{0\\} \\in \\{0, 1\\}$", "$\\emptyset \\in \\{0, 1\\}$", "$\\{0, 1, 2\\} \\subseteq \\{0, 1\\}$"],
           "$0$ ist ein Element, $\\{0\\}$ eine Teilmenge. $\\emptyset$ ist Teilmenge jeder Menge, aber kein Element von $\\{0, 1\\}$. "
           "Doppelte Elemente zählen nicht. $\\{0, 1, 2\\}$ enthält die $2$, die nicht in $\\{0, 1\\}$ liegt.",
           tipps=["$\\in$ gilt zwischen Element und Menge, $\\subseteq$ zwischen Mengen.", "Die Elemente von $\\{0, 1\\}$ sind nur $0$ und $1$."],
           fehler={"$\\{0\\} \\in \\{0, 1\\}$": "$\\{0\\}$ ist eine Menge, kein Element von $\\{0, 1\\}$. Dort liegen nur die Zahlen $0$ und $1$.",
                   "$\\emptyset \\in \\{0, 1\\}$": "$\\emptyset$ ist eine Teilmenge von $\\{0, 1\\}$, aber kein Element. Verwechsle $\\in$ und $\\subseteq$ nicht.",
                   "$\\{0, 1, 2\\} \\subseteq \\{0, 1\\}$": "Die $2$ liegt nicht in $\\{0, 1\\}$, also ist es keine Teilmenge."})

k.zahl("Wie viele Elemente hat die Menge $\\{0, \\{0\\}, \\{0, 1\\}\\}$?", 3,
       "Die Elemente sind die Zahl $0$, die Menge $\\{0\\}$ und die Menge $\\{0, 1\\}$. Mengen dürfen andere Mengen als Elemente enthalten. "
       "Das ist nicht dasselbe wie die Elemente der inneren Mengen zu zählen.",
       tipps=["Zähle nur, was direkt zwischen den äußeren Klammern steht, durch Kommas getrennt.", "Eine innere Menge zählt als ein Element.", "Es stehen drei Dinge dort: eine Zahl und zwei Mengen."],
       rechenweg=r"""
       :::rechnung
       0 || erstes Element: eine Zahl
       \{0\} || zweites Element: eine Menge mit einem Element
       \{0, 1\} || drittes Element: eine Menge mit zwei Elementen
       :::
       """,
       typische_fehler=[(2, "Du hast die Zahl $0$ doppelt gerechnet: $0$ steht allein und auch in $\\{0\\}$ und $\\{0, 1\\}$, aber Elemente zählen nur, was außen steht."),
                        (4, "Du hast die Zahlen innerhalb der inneren Mengen mitgezählt. Gezählt wird nur, was direkt in der äußeren Klammer steht.")])


# ═══ Seite 4: Aussonderung (Folie 5) ═════════════════════════════════════════════════════════════
k.erklaerung("Aussonderung", r"""
    ## Aus einem Korb auswählen

    :::analogie 🍎 Obstkorb
    Aus einem Obstkorb suchst du alle Äpfel heraus. Du brauchst einen Korb, aus dem du auswählst. „Alle
    Äpfel der Welt“ ist keine Sammlung, die du in der Hand hältst.
    :::

    Zweite Erzeugungsweise: Aus einer [[Grundmenge]] $G$ werden alle $x$ ausgesondert, für die die
    [[Aussageform]] $E(x)$ wahr ist: $\{x \in G \mid E(x)\}$. Gelesen: „alle $x$ aus $G$, für die $E(x)$ gilt“.
    Warum $G$? Die Sammlung $\{x \mid x \notin x\}$ ohne Grundmenge ist genau die Sammlung aus Russells Antinomie: keine
    Menge. Mit einer Grundmenge sonderst du nur aus schon Vorhandenem aus, das ist unproblematisch.

    :::rechnung Beispiele der Folie
    \{0, 1, 2, 3, 4, 5\} = \{n \in \mathbb{N} \mid n \le 5\} || alle natürlichen Zahlen bis 5
    \{\ldots, -4, -2, 0, 2, 4, \ldots\} = \{n \in \mathbb{Z} \mid n \text{ ist gerade}\} || alle geraden ganzen Zahlen
    \mathbb{N} = \{n \in \mathbb{Z} \mid n \ge 0\} || alle nicht negativen ganzen Zahlen
    \mathbb{Q} := \{x \in \mathbb{R} \mid x = \tfrac{a}{b} \text{ für } a \in \mathbb{Z},\ b \in \mathbb{N} \setminus \{0\}\} || Vorgriff: Brüche, ausgesondert aus ℝ
    :::

    Die Menge $\mathbb{R}$ der reellen Zahlen setzen wir voraus. Sie kommt später (Kapitel 3).

    :::alt Warum die Grundmenge nötig ist
    Deine Frage aus der Vorlesung: Ohne Grundmenge fragst du nach „allem, was es gibt“. Dann kannst du die
    Eigenschaft „enthält sich nicht selbst“ auf die ganze Welt loslassen und landest beim Barbier-Paradox.
    Mit Grundmenge fragst du nur: „Welche Dinge aus diesem Korb erfüllen die Eigenschaft?“ Der Korb ist
    schon da, du schaffst keine neue riesige Sammlung aus dem Nichts.
    :::
    """)

k.mc("Warum braucht die Aussonderung $\\{x \\in G \\mid E(x)\\}$ eine Grundmenge $G$?",
     ["Ohne Grundmenge entstünden Sammlungen wie $\\{x \\mid x \\notin x\\}$ (Russell), die keine Mengen sind.",
      "Damit man die Elemente aufzählen kann.",
      "Damit $E(x)$ eine Aussage wird.",
      "Eine Grundmenge braucht man nur für die Vereinigung, nicht für die Aussonderung."],
     "Aussonderung bedeutet: aus einer schon vorhandenen Menge $G$ auswählen. Ohne $G$ ist $\\{x \\mid x \\notin x\\}$ genau Russells Sammlung, "
     "und die ist keine Menge. (Für Schnitt und Differenz kann man $G$ weglassen, weil $M \\cap N = \\{x \\in M \\mid x \\in N\\}$ schon aus $M$ aussondert.)",
     tipps=["Erinnere dich an die Sammlung der Mengen, die sich nicht selbst enthalten.", "Aus welchem Bestand wird ausgesondert?"],
     fehler={"Damit man die Elemente aufzählen kann.": "Aufzählen kann man auch unendliche Mengen nicht. Die Grundmenge schützt vor Widersprüchen, sie hilft nicht beim Aufzählen.",
             "Damit $E(x)$ eine Aussage wird.": "Eine Aussage wird $E(x)$ erst durch Einsetzen eines $x$ (Belegung). Die Grundmenge sagt, welche $x$ erlaubt sind.",
             "Eine Grundmenge braucht man nur für die Vereinigung, nicht für die Aussonderung.": "Bei der Aussonderung ist die Grundmenge Teil der Schreibweise, sonst fehlt der Bestand, aus dem ausgewählt wird."})

k.menge(r"""Gib die Menge $\{n \in \mathbb{N} \mid n \text{ ist gerade und } n \le 9\}$ in aufzählender Form an. Trenne die Elemente mit **;**, z. B. $\{1; 2\}$.""",
        "{0; 2; 4; 6; 8}",
        "In diesem Skript gehört die $0$ zu $\\mathbb{N}$, und $0 = 2 \\cdot 0$ ist gerade. Die geraden Zahlen von $0$ bis $9$ sind $0, 2, 4, 6, 8$.",
        tipps=["Prüfe jede natürliche Zahl von $0$ bis $9$: gerade oder nicht?", "$0 \\in \\mathbb{N}$ und $0$ ist gerade.", "Gesucht sind fünf Zahlen."],
        rechenweg=r"""$n \le 9$ liefert $0, 1, \ldots, 9$. Davon sind gerade: $0, 2, 4, 6, 8$.""",
        typische_fehler=[("{2; 4; 6; 8}", "Du hast die $0$ vergessen. Im Skript ist $0 \\in \\mathbb{N}$, und $0$ ist gerade, denn $0 = 2 \\cdot 0$."),
                         ("{0; 2; 4; 6; 8; 10}", "Die $10$ erfüllt $n \\le 9$ nicht.")])


# ═══ Seite 5: Vereinigung, Schnitt, Differenz (Definition 1.21 und 1.22, Folien 6 und 7) ══════════
k.erklaerung("Vereinigung, Schnitt, Differenz", r"""
    ## Zwei Tüten kombinieren

    :::analogie 🛍️ Tüten zusammenkippen
    Zwei Tüten: Kippst du sie zusammen, hast du die **Vereinigung**. Was in beiden liegt, ist der **Schnitt**.
    Was in der ersten liegt, aber nicht in der zweiten, ist die **Differenz**.
    :::

    Definition 1.21: Für $M, N \subseteq G$ ist $M \cup N := \{x \in G \mid x \in M \lor x \in N\}$ die [[Vereinigung]],
    $M \cap N := \{x \in G \mid x \in M \land x \in N\}$ der [[Schnitt|Durchschnitt]] und
    $M \setminus N := \{x \in G \mid x \in M \land x \notin N\}$ die [[Mengendifferenz|Differenzmenge]]. Beachte: $\cup$ gehört zu
    $\lor$, $\cap$ zu $\land$. Gilt $M \cap N = \emptyset$, heißen $M$ und $N$ [[disjunkt]]. Das ist keine neue
    Erzeugungsweise, sondern Aussonderung. Schnitt und Differenz brauchen keine Grundmenge, die Vereinigung schon.

    """ + _vis("venn", mengen=[{"name": "M", "elemente": ["¬", "∨", "∧"]}, {"name": "N", "elemente": ["∧", "⇒"]}],
               universum=["¬", "∨", "∧", "⇒", "⇔"], universum_name="G", markiert="M ∪ N",
               unterschrift="Folie 6 und 7 mit $M = \\{\\neg, \\lor, \\land\\}$ und $N = \\{\\land, \\Rightarrow\\}$. Tippe auf die Flächen. $G$ ist die Menge der Verknüpfungen aus 1.2.") + r"""

    :::rechnung Beispiel mit M = {¬, ∨, ∧} und N = {∧, ⇒}
    M \cup N = \{\neg, \lor, \land, \Rightarrow\} || alles, was in M oder in N liegt
    M \cap N = \{\land\} || nur ∧ liegt in beiden
    M \setminus N = \{\neg, \lor\} || aus M ohne das ∧
    N \setminus M = \{\Rightarrow\} || aus N ohne das ∧
    \mathbb{Z}_{\ge 0} = \mathbb{Z} \cap \{x \in \mathbb{R} \mid x \ge 0\} = \{0, 1, 2, \ldots\} = \mathbb{N} || Definition 1.22: Z≥0 für Z ∈ {ℤ, ℚ, ℝ}
    :::

    :::alt Mit Wörtern
    Vereinigung heißt „oder“: Wer in Kurs M oder in Kurs N ist, steht auf der Gesamtliste. Schnitt heißt „und“: Wer
    in beiden Kursen ist, steht auf beiden Listen. Differenz heißt „und nicht“: Wer in M ist, aber nicht in N.
    Zwei Kurse ohne gemeinsame Teilnehmer sind disjunkt.
    :::
    """)

# ═══ Seite 6: Satz 1.23 (Folien 7 und 15, Leseaufgabe) ════════════════════════════════════════════
k.erklaerung("Beweis des Distributivgesetzes (Satz 1.23)", r"""
    ## Wie man „gleich“ beweist: ⊆ und ⊇

    :::analogie 🧾 Zwei Einkaufszettel
    Zwei Einkaufszettel sind gleich, wenn alles von Zettel 1 auch auf Zettel 2 steht **und** umgekehrt.
    Es reicht nicht, nur eine Richtung zu prüfen.
    :::

    Satz 1.23 (Distributivgesetz): $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$. Mengen sind gleich, wenn jede
    Teilmenge der anderen ist. Also zwei Richtungen: Zeige $\subseteq$, dann $\supseteq$. Jedes Mal nimmst du ein
    **beliebiges** Element $x$ der linken Seite und zeigst, dass es auf der rechten liegt. Das „oder“ in
    $x \in B \cup C$ führt zu einer Fallunterscheidung aus Vorlesung 1.

    """ + _vis("venn", mengen=[{"name": "A", "elemente": [1, 2, 3, 4]}, {"name": "B", "elemente": [2, 3, 5, 6]}, {"name": "C", "elemente": [3, 4, 6, 7]}],
               universum=[1, 2, 3, 4, 5, 6, 7, 8], markiert="A ∩ (B ∪ C)",
               unterschrift="Links: $A \\cap (B \\cup C)$.") + "\n\n    " + _vis("venn", mengen=[{"name": "A", "elemente": [1, 2, 3, 4]}, {"name": "B", "elemente": [2, 3, 5, 6]}, {"name": "C", "elemente": [3, 4, 6, 7]}],
               universum=[1, 2, 3, 4, 5, 6, 7, 8], markiert="(A ∩ B) ∪ (A ∩ C)",
               unterschrift="Rechts: $(A \\cap B) \\cup (A \\cap C)$. Dieselbe Fläche, hier an einem Beispiel mit Zahlen.") + r"""

    :::rechnung Richtung ⊆ (Skript Seite 10)
    \text{Sei } x \in A \cap (B \cup C). || ein beliebiges Element der linken Seite
    \text{Dann } x \in A \text{ und } x \in B \cup C, \text{ also } x \in B \text{ oder } x \in C. || Definition von ∩ und ∪
    \text{Fall 1: } x \in B. \text{ Mit } x \in A \text{ folgt } x \in A \cap B. || beide Bedingungen erfüllt
    \text{Fall 2: } x \in C. \text{ Mit } x \in A \text{ folgt } x \in A \cap C. || ebenso
    \text{In beiden Fällen } x \in (A \cap B) \cup (A \cap C). || Definition von ∪: ⊆ gezeigt
    :::

    :::rechnung Richtung ⊇ (Skript Seite 10)
    \text{Sei } x \in (A \cap B) \cup (A \cap C). || ein beliebiges Element der rechten Seite
    \text{Dann } x \in A \cap B \text{ oder } x \in A \cap C. || Definition von ∪
    \text{Fall 1: } x \in A \cap B. \text{ Dann } x \in A \text{ und } x \in B, \text{ insbesondere } x \in B \cup C. || x ∈ B reicht für B ∪ C
    \text{Fall 2: } x \in A \cap C. \text{ Dann } x \in A \text{ und } x \in C, \text{ also ebenfalls } x \in B \cup C. || ebenso
    \text{In beiden Fällen } x \in A \cap (B \cup C). || ⊇ gezeigt, also Gleichheit \ \square
    :::

    :::alt Wie das Distributivgesetz in der Logik
    Dasselbe kennst du aus Vorlesung 1: „$x$ ist in $A$ und ($x$ ist in $B$ oder $x$ ist in $C$)“ sagt dasselbe wie
    „($x$ ist in $A$ und in $B$) oder ($x$ ist in $A$ und in $C$)“. Die Mengenaussage ist die Logikaussage
    $P \land (Q \lor R) \Leftrightarrow (P \land Q) \lor (P \land R)$ mit $P$, $Q$, $R$ für „$x \in A$“, „$x \in B$“, „$x \in C$“.
    :::
    """)

k.ordnen("Bringe die Richtung ⊆ des Beweises von Satz 1.23 in die richtige Reihenfolge.",
         ["Sei $x \\in A \\cap (B \\cup C)$ beliebig.",
          "Dann ist $x \\in A$ und $x \\in B \\cup C$, also $x \\in B$ oder $x \\in C$.",
          "Fall 1: $x \\in B$. Mit $x \\in A$ folgt $x \\in A \\cap B$.",
          "Fall 2: $x \\in C$. Mit $x \\in A$ folgt $x \\in A \\cap C$.",
          "In beiden Fällen gilt $x \\in (A \\cap B) \\cup (A \\cap C)$."],
         "Muster: ein beliebiges Element der linken Seite nehmen, die Definitionen von $\\cap$ und $\\cup$ auspacken, das „oder“ durch Fälle behandeln und in jedem Fall die rechte Seite erreichen.",
         alternativen=[["Sei $x \\in A \\cap (B \\cup C)$ beliebig.",
                        "Dann ist $x \\in A$ und $x \\in B \\cup C$, also $x \\in B$ oder $x \\in C$.",
                        "Fall 2: $x \\in C$. Mit $x \\in A$ folgt $x \\in A \\cap C$.",
                        "Fall 1: $x \\in B$. Mit $x \\in A$ folgt $x \\in A \\cap B$.",
                        "In beiden Fällen gilt $x \\in (A \\cap B) \\cup (A \\cap C)$."]],
         ablenker=["Sei $A = \\{1, 2\\}$, $B = \\{2\\}$, $C = \\{3\\}$. Dann stimmt die Gleichung.",
                   "Aus $x \\in B \\cup C$ folgt $x \\in B$ und $x \\in C$."],
         tipps=["Ein Beweis beginnt mit einem beliebigen Element, nicht mit konkreten Mengen.", "Erst die Voraussetzung auspacken, dann die Fälle.",
                "Der letzte Satz fasst die Fälle zusammen."])

k.mc("Wie beweist man $M = N$ für zwei Mengen? (Skript 1.4, Folie 4 und 15)",
     ["Man zeigt $M \\subseteq N$ und $N \\subseteq M$.", "Man zeigt nur $M \\subseteq N$.",
      "Man prüft es an einem Beispiel.", "Man zeigt $M \\in N$ und $N \\in M$."],
     "Zwei Mengen sind gleich, wenn sie dieselben Elemente haben, also wenn $M \\subseteq N$ und $N \\subseteq M$ gilt. Beide Richtungen sind nötig.",
     tipps=["Gleich bedeutet: Jedes Element von $M$ liegt in $N$ und jedes von $N$ in $M$.", "Wie viele Richtungen sind das?"],
     fehler={"Man zeigt nur $M \\subseteq N$.": "Das wäre nur „$M$ ist in $N$ enthalten“. $N$ könnte noch mehr Elemente haben.",
             "Man prüft es an einem Beispiel.": "Ein Beispiel ist kein Beweis. Man arbeitet mit einem beliebigen Element $x$.",
             "Man zeigt $M \\in N$ und $N \\in M$.": "$\\in$ verbindet ein Element mit einer Menge, nicht zwei Mengen."})


# ═══ Seite 7: Tupel und kartesisches Produkt (Definition 1.24, 1.26, Folien 8 und 9) ══════════════
k.erklaerung("Tupel und kartesisches Produkt", r"""
    ## Reihenfolge und Wiederholung zählen

    :::analogie 🏠 Adresse
    „Hauptstraße 5“ und „5 Hauptstraße“ sind nicht dasselbe, und bei „Wiesenweg 11, Haus 11“ zählt, dass die 11
    zweimal vorkommt. Eine Adresse ist ein Tupel, die Menge {Straße, Nummer} wäre es nicht.
    :::

    Ein [[Tupel]] $(a_1, a_2, \ldots, a_n)$ mit $n \in \mathbb{N}$ (Definition 1.24) ist eine endliche
    Aneinanderreihung, **geordnet**, und ein Element darf mehrfach vorkommen. Beispiele: Datensätze, Strings,
    Arrays, Parameterlisten, Bildschirmkoordinaten. Das [[kartesische Produkt|kartesisches Produkt]]
    $A_1 \times \cdots \times A_n$ (1.26) ist die Menge aller Tupel $(a_1, \ldots, a_n)$ mit $a_1 \in A_1, \ldots, a_n \in A_n$.
    Es liefert **neue Grundmengen**. $A^n := A \times \cdots \times A$ ($n$-mal), $A^0 := \{()\}$ (nur das leere Tupel).

    :::rechnung Tupel gegen Mengen (Beispiel zu 1.24)
    \{0, 1\} = \{1, 0\}, \text{ aber } (0, 1) \neq (1, 0) || bei Tupeln zählt die Position
    \{0, 0, 1\} = \{0, 1\}, \text{ aber } (0, 0, 1) \neq (0, 1) || bei Tupeln zählt die Wiederholung
    :::

    :::rechnung Beispiel 1.27: Bitstrings aus 3 Bits
    \{0, 1\}^3 = \{(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)\} || 2 \cdot 2 \cdot 2 = 8 Tupel
    2 \cdot 2 \cdot 2 = 8 || je Position zwei Möglichkeiten
    :::

    :::rechnung Beispiel 1.28: Vorlesungsslots der TU Darmstadt
    \{\text{Mo, Di, Mi, Do, Fr}\} \times \{\text{8:00, 9:50, 11:40, 13:30, 15:20, 17:10}\} || alle Paare aus Wochentag und Uhrzeit
    5 \cdot 6 = 30 || 30 Slots, darunter (Mo, 8:00), (Do, 9:50) und (Fr, 17:10)
    :::

    :::alt Für Interessierte (Bemerkung 1.25)
    Auch ein Tupel lässt sich als Menge schreiben: (a, b) wird zu { {1}, {1, a} } und { {2}, {2, b} }. Jeder
    Eintrag bekommt seine Position mitgeschrieben. Das ist nicht prüfungsrelevant, zeigt aber: Alles lässt sich
    auf Mengen zurückführen. Anschaulich: Ein Stundenplan ist ein Gitter aus Tag mal Uhrzeit, und jede
    Zelle ist ein Paar.
    :::
    """)

k.mehrfach("Welche Gleichungen gelten?",
           ["$\\{0, 1\\} = \\{1, 0\\}$", "$\\{0, 0, 1\\} = \\{0, 1\\}$"],
           ["$(0, 1) = (1, 0)$", "$(0, 0, 1) = (0, 1)$"],
           "Bei Mengen zählen weder Reihenfolge noch Wiederholungen, bei Tupeln beides.",
           tipps=["Bei Mengen zählt nur: drin oder nicht.", "Bei Tupeln zählt jede Stelle."],
           fehler={"$(0, 1) = (1, 0)$": "Tupel sind geordnet: Die erste Stelle ist links $0$ und rechts $1$.",
                   "$(0, 0, 1) = (0, 1)$": "Ein Tupel mit drei Stellen ist nicht gleich einem mit zwei Stellen. Wiederholungen zählen."})

k.zahl("Wie viele Elemente hat $\\{0, 1\\}^3$, die Menge der Bitstrings aus $3$ Bits?", 8,
       "Jede der $3$ Stellen hat $2$ Möglichkeiten: $2 \\cdot 2 \\cdot 2 = 2^3 = 8$ Tupel (Beispiel 1.27).",
       tipps=["Wie viele Möglichkeiten hat jede Stelle?", "Die Möglichkeiten werden multipliziert.", "$2 \\cdot 2 \\cdot 2$"],
       rechenweg=r"""
       :::rechnung
       2 \cdot 2 \cdot 2 = 8 || je Stelle zwei Möglichkeiten, drei Stellen
       :::
       """,
       typische_fehler=[(6, "$6 = 2 \\cdot 3$ wäre die Zahl der Möglichkeiten, wenn man addiert statt malnimmt. Pro Stelle $2$, bei drei Stellen: $2^3$."),
                        (9, "$9 = 3^2$ hast du die Rollen von Basis und Exponent vertauscht: Es gibt $2$ Möglichkeiten, $3$-mal.")])


# ═══ Seite 8: Potenzmenge (Definition 1.29, Beispiele 1.30 und 1.31, Folie 10) ════════════════════
k.erklaerung("Die Potenzmenge", r"""
    ## Alle Auswahlen auf einmal

    :::analogie 🍕 Pizza
    Du hast drei Zutaten. Jede kommt auf die Pizza oder nicht. Jede Auswahl ist eine mögliche Pizza,
    auch die ohne alles. Die Menge aller Pizzen ist die Potenzmenge der Zutatenmenge.
    :::

    Die [[Potenzmenge]] $\mathcal{P}(M)$ (Definition 1.29) enthält alle Teilmengen von $M$:
    $N \in \mathcal{P}(M) \Leftrightarrow N \subseteq M$. Während die Aussonderung eine Auswahl der Elemente vornimmt,
    macht die Potenzmenge **alle möglichen Auswahlen** zu Elementen der neuen Menge. Dabei werden Mengen
    zu Elementen. Auch $\emptyset$ und $M$ selbst gehören immer dazu. Hat $M$ genau $n$ Elemente, hat
    $\mathcal{P}(M)$ genau $2^n$ Elemente: Pro Element „dabei“ oder „nicht dabei“.

    :::rechnung Beispiel 1.30 und die Zählregel
    \mathcal{P}(\{0, 1\}) = \{\emptyset, \{0\}, \{1\}, \{0, 1\}\} || vier Teilmengen
    2^2 = 4 || zwei Elemente, je dabei oder nicht
    \mathcal{P}(\{a, b, c\}) = \{\emptyset, \{a\}, \{b\}, \{c\}, \{a, b\}, \{a, c\}, \{b, c\}, \{a, b, c\}\} || acht Teilmengen
    2^3 = 8 || drei Elemente
    :::

    :::rechnung Beispiel 1.31: Belegungspläne eines Raums
    \text{Die Slotmenge aus 1.28 hat } 5 \cdot 6 = 30 \text{ Elemente.} || Tage mal Uhrzeiten
    \text{Ein Belegungsplan ist eine Teilmenge der Slotmenge.} || jeder Slot ist belegt oder frei
    2^{30} = 1073741824 || so viele mögliche Pläne, über eine Milliarde
    :::

    :::alt Als Bitstring
    Eine Teilmenge von {a, b, c} ist ein Bitstring aus drei Bits: 101 heißt „a dabei, b nicht, c dabei“, also
    {a, c}. Es gibt 2³ = 8 Bitstrings, also 8 Teilmengen. So hängen Bitstrings aus Beispiel 1.27 und die
    Potenzmenge zusammen: Ein Raum mit 30 Slots hat 30 Bits, jeder Belegungsplan ist ein Bitstring.
    :::
    """)

k.menge(r"""Gib $\mathcal{P}(\{a, b\})$ an. Schreibe die leere Menge als **{}**, trenne die Elemente mit **;**, z. B. $\{\{a\}; \{\}\}$.""",
        "{{}; {a}; {b}; {a; b}}",
        "Die Teilmengen von $\\{a, b\\}$ sind $\\emptyset$, $\\{a\\}$, $\\{b\\}$ und $\\{a, b\\}$: Das sind $2^2 = 4$.",
        tipps=["Gehe die Auswahlen durch: nichts, nur $a$, nur $b$, beide.", "Vergiss die leere Menge und $\\{a, b\\}$ selbst nicht.", "Es sind $2^2 = 4$ Elemente, jedes ist selbst eine Menge."],
        rechenweg=r"""Auswahlen: nichts, nur $a$, nur $b$, beide. Das sind $\emptyset, \{a\}, \{b\}, \{a, b\}$.""",
        typische_fehler=[("{{a}; {b}; {a; b}}", "Die leere Menge ist auch eine Teilmenge von $\\{a, b\\}$ und gehört zur Potenzmenge."),
                         ("{{}; {a}; {b}}", "Auch $\\{a, b\\}$ selbst ist eine Teilmenge von $\\{a, b\\}$."),
                         ("{a; b}", "Das ist $\\{a, b\\}$ selbst. Die Potenzmenge enthält Mengen als Elemente, nicht $a$ und $b$ direkt.")])


# ═══ Seite 9: Quantoren (Definition 1.32, Beispiel 1.33, Folie 12) ═══════════════════════════════
k.erklaerung("All- und Existenzquantor (Skript 1.5)", r"""
    ## „Für alle“ und „es gibt“

    :::analogie 🎓 Hörsaal
    „Alle im Hörsaal sind angemeldet“ ist falsch, sobald eine einzige Person nicht angemeldet ist.
    „Es gibt jemanden im Hörsaal, der Anna heißt“ ist wahr, sobald du eine Anna findest.
    :::

    Zweite Möglichkeit, aus einer [[Aussageform]] $E(x)$ eine Aussage zu machen, ohne ein $x$ einzusetzen: sagen, für
    wie viele $x$ sie gilt (Definition 1.32). $\forall x \in M : E(x)$ heißt „für alle $x \in M$ gilt $E(x)$“
    ([[Quantoren|Quantor]] $\forall$, Allquantor). $\exists x \in M : E(x)$ heißt „für mindestens ein $x \in M$ gilt $E(x)$“
    ($\exists$, Existenzquantor). Danach ist $x$ eine [[gebundene Variable]], und beide Ausdrücke sind Aussagen.

    :::rechnung Beispiel 1.33 mit B₁(n): Die Zahl n ist gerade
    \forall n \in \mathbb{N} : B_1(n) \quad \text{gilt nicht} || Gegenbeispiel: 1 ist nicht gerade
    \exists n \in \mathbb{N} : B_1(n) \quad \text{gilt} || Zeuge: 0 ist gerade
    \exists n \in \{1, 3, 5\} : B_1(n) \quad \text{gilt nicht} || 1, 3 und 5 sind ungerade, keine gerade Zahl in der Menge
    \forall r \in \mathbb{R}_{\ge 0} \setminus \{0\} : B_3(r) \quad \text{gilt} || für jeden positiven Radius ist die Fläche πr²
    :::

    :::achtung Beweisen und widerlegen
    $\exists$ beweist du mit **einem** passenden Element, dem [[Zeugen|Zeuge]]. $\forall$ widerlegst du mit **einem**
    [[Gegenbeispiel]]. Umgekehrt ist es viel Arbeit: $\forall$ beweisen heißt, ein Argument für jedes Element zu
    haben („sei $n$ beliebig“).
    :::

    :::alt Als Schleifen
    ∀ ist wie `all(...)`, ∃ wie `any(...)` in Python: `all(n % 2 == 0 for n in menge)` ist `False`, sobald
    ein einziges `n` durchfällt. `any(n % 2 == 0 for n in menge)` ist `True`, sobald ein einziges `n` besteht. Bei
    {1, 3, 5} findet `any` keins und bleibt `False`.
    :::
    """)

k.mehrfach("Welche Aussagen gelten? (Beispiel 1.33, $B_1(n)$: „$n$ ist gerade“)",
           ["$\\exists n \\in \\mathbb{N} : B_1(n)$", "$\\forall n \\in \\{0, 2, 4\\} : B_1(n)$"],
           ["$\\forall n \\in \\mathbb{N} : B_1(n)$", "$\\exists n \\in \\{1, 3, 5\\} : B_1(n)$"],
           "Für $\\exists$ reicht ein Zeuge: $0$ ist gerade. $0, 2, 4$ sind alle gerade, also gilt die $\\forall$-Aussage. "
           "$\\forall n \\in \\mathbb{N}$ scheitert an $n = 1$. In $\\{1, 3, 5\\}$ gibt es keine gerade Zahl.",
           tipps=["Für $\\exists$ suche ein passendes Element, für $\\forall$ ein Gegenbeispiel.", "Prüfe jede Menge einzeln."],
           fehler={"$\\forall n \\in \\mathbb{N} : B_1(n)$": "$n = 1$ ist ein Gegenbeispiel: $1$ ist nicht gerade.",
                   "$\\exists n \\in \\{1, 3, 5\\} : B_1(n)$": "Alle drei Zahlen sind ungerade. Es gibt keine, die gerade ist."})


# ═══ Seite 10: Quantoren negieren, Mengensysteme (Folien 13 und 14, Definition 1.34) ═════════════
k.erklaerung("Quantoren negieren, Vereinigung über viele Mengen", r"""
    ## Tauschen und verneinen

    :::analogie 🍎 Tüten mit Apfel
    „In jeder Tüte liegt ein Apfel“ stimmt nicht? Dann gibt es mindestens eine Tüte ohne Apfel. „In keiner
    Tüte liegt ein Apfel“ stimmt nicht? Dann liegt in mindestens einer ein Apfel.
    :::

    Beim Verneinen wird aus $\forall$ ein $\exists$ und umgekehrt, und die Eigenschaft wird verneint. Das ist
    De Morgan für „viele“. Eine Allaussage ist falsch, sobald ein Gegenbeispiel existiert. Eine Existenzaussage ist
    falsch, wenn kein Element die Eigenschaft erfüllt. Für ein [[Familie|Mengensystem]] $\mathcal{F}$ von Teilmengen einer Grundmenge $G$ (Definition 1.34)
    gilt: $x$ liegt in der Vereinigung, wenn es **ein** $M \in \mathcal{F}$ mit $x \in M$ gibt ($\exists$), und im Schnitt, wenn
    $x$ in **jedem** $M \in \mathcal{F}$ liegt ($\forall$).

    $$\neg(\forall x \in M : E(x)) \Leftrightarrow \exists x \in M : \neg E(x) \qquad \neg(\exists x \in M : E(x)) \Leftrightarrow \forall x \in M : \neg E(x)$$

    $$\bigcup_{M \in \mathcal{F}} M := \{x \in G \mid \exists M \in \mathcal{F} : x \in M\} \qquad \bigcap_{M \in \mathcal{F}} M := \{x \in G \mid \forall M \in \mathcal{F} : x \in M\}$$

    :::rechnung Beispiel: „Nicht alle natürlichen Zahlen sind gerade“ (Folie 13)
    \neg(\forall n \in \mathbb{N} : n \text{ ist gerade}) || die Aussage
    \Leftrightarrow \exists n \in \mathbb{N} : \neg(n \text{ ist gerade}) || ∀ wird ∃, die Eigenschaft verneint
    \Leftrightarrow \exists n \in \mathbb{N} : n \text{ ist ungerade} || nicht gerade heißt ungerade
    \text{Die Aussage gilt: } n = 1 \text{ ist ungerade.} || ein Zeuge reicht
    :::

    :::rechnung Beispiel 1.34: G = {0, 1, 2, 3} und F = { {0, 1}, {1, 2}, {1, 3} }
    \bigcup_{M \in \mathcal{F}} M = \{0, 1, 2, 3\} || alles, was in mindestens einer der drei Mengen liegt
    \bigcap_{M \in \mathcal{F}} M = \{1\} || nur die 1 liegt in allen drei
    \text{Für } \mathcal{F} = \emptyset: \bigcup_{M \in \emptyset} M = \emptyset, \ \bigcap_{M \in \emptyset} M = G || für Interessierte: der leere Schnitt hängt von G ab
    :::

    :::alt Mit Tüten
    ℱ ist ein Beutel mit mehreren Tüten. Die Vereinigung kippt alle Tüten in eine große: Was in mindestens einer lag,
    ist jetzt drin. Der Schnitt ist, was in **jeder** Tüte liegt. Ein Beutel ganz ohne Tüten: Aus keiner Tüte kommt
    etwas, die Vereinigung ist leer. Aber „liegt in jeder Tüte“ stimmt dann für alles, es gibt ja keine Tüte,
    die widerspricht: der Schnitt ist ganz G.
    :::
    """)

k.mc("Wie lautet die Verneinung von „Alle natürlichen Zahlen sind gerade“?",
     ["Es gibt eine natürliche Zahl, die nicht gerade ist.", "Alle natürlichen Zahlen sind ungerade.",
      "Es gibt eine natürliche Zahl, die gerade ist.", "Keine natürliche Zahl ist ungerade."],
     "$\\neg(\\forall n : n \\text{ gerade}) \\Leftrightarrow \\exists n : \\neg(n \\text{ gerade})$. Ein einziges Gegenbeispiel (etwa $1$) reicht. Der Quantor wird getauscht und die Eigenschaft verneint.",
     tipps=["Beim Verneinen wird aus $\\forall$ ein $\\exists$.", "Auch die Eigenschaft wird verneint."],
     fehler={"Alle natürlichen Zahlen sind ungerade.": "Das ist zu stark: Es müssen nicht **alle** ungerade sein, mindestens eine reicht. Du hast den Quantor nicht getauscht.",
             "Es gibt eine natürliche Zahl, die gerade ist.": "Der Quantor ist getauscht, aber die Eigenschaft nicht verneint. Außerdem ist diese Aussage wahr, obwohl die Ausgangsaussage falsch ist: so kann keine Verneinung aussehen.",
             "Keine natürliche Zahl ist ungerade.": "Das ist $\\forall n : n$ gerade, also die Ausgangsaussage selbst."})


# ═══ Praxis ════════════════════════════════════════════════════════════════════════════════════════
def mengenverknuepfung(rng):
    while True:
        A = frozenset(rng.sample(range(1, 10), rng.randint(3, 5)))
        B = frozenset(rng.sample(range(1, 10), rng.randint(3, 5)))
        if A & B and A - B and B - A:
            break
    op = rng.choice(["vereinigung", "schnitt", "differenz"])
    erg = {"vereinigung": A | B, "schnitt": A & B, "differenz": A - B}
    zeichen = {"vereinigung": "\\cup", "schnitt": "\\cap", "differenz": "\\setminus"}
    name = {"vereinigung": "Vereinigung", "schnitt": "Schnitt", "differenz": "Differenz"}
    soll = erg[op]
    meldung = {"vereinigung": "Das ist die Vereinigung $A \\cup B$: alles aus beiden Mengen.",
               "schnitt": "Das ist der Schnitt $A \\cap B$: nur, was in beiden liegt.",
               "differenz": "Das ist $A \\setminus B$: Elemente aus $A$, die nicht in $B$ liegen."}
    kandidaten = [(erg[o], meldung[o]) for o in erg if o != op]
    kandidaten.append((B - A, "Das ist $B \\setminus A$, die Differenz in der anderen Richtung."))
    fehler, gesehen = [], []
    for menge, m in kandidaten:
        if menge != soll and menge not in gesehen:
            gesehen.append(menge)
            fehler.append((_text(menge), m))
    zeile = {"vereinigung": f"Vereinigt: alles aus $A$ und alles aus $B$, jedes Element nur einmal. Ergebnis ${_tex(soll)}$.",
             "schnitt": f"Nur die Elemente, die in $A$ **und** in $B$ liegen: ${_tex(soll)}$.",
             "differenz": f"Aus $A$ werden die Elemente gestrichen, die in $B$ liegen. Es bleibt ${_tex(soll)}$."}[op]
    tipps = {"vereinigung": ["Alles aus beiden Mengen, doppelte Elemente nur einmal.", "Schreibe zuerst $A$ hin, ergänze dann, was in $B$ neu ist."],
             "schnitt": ["Gesucht ist, was in beiden Mengen liegt.", "Gehe die Elemente von $A$ durch und prüfe, ob sie auch in $B$ liegen."],
             "differenz": ["Starte mit $A$ und streiche, was in $B$ liegt.", "Die Reihenfolge ist wichtig: $A \\setminus B$ ist nicht $B \\setminus A$."]}[op]
    return {
        "frage": f"Es seien $A := {_tex(A)}$ und $B := {_tex(B)}$. Gib die {name[op]} $A {zeichen[op]} B$ an. Trenne mit **;**, z. B. $\\{{1; 2\\}}$.",
        "loesung": _text(soll),
        "tipps": tipps + [zeile],
        "rechenweg": zeile,
        "erklaerung": zeile,
        "typische_fehler": fehler,
    }


def potenzmenge_und_produkt(rng):
    art = rng.choice(["potenz", "produkt", "bits"])
    if art == "potenz":
        n = rng.randint(2, 6)
        elem = rng.sample(["a", "b", "c", "d", "e", "f", "g"], n)
        loesung = 2 ** n
        frage = f"Die Menge $M := {_tex(elem)}$ hat {n} Elemente. Wie viele Elemente hat die Potenzmenge $\\mathcal{{P}}(M)$?"
        fehler = [(2 * n, f"$2 \\cdot {n}$ addiert die Möglichkeiten. Jedes der {n} Elemente ist „dabei“ oder „nicht dabei“, und das wird malgenommen."),
                  (n * n, f"${n}^2$ vertauscht Basis und Exponent. Es sind $2$ Möglichkeiten, {n}-mal: $2^{{{n}}}$."), (n, f"Das ist nur die Zahl der Elemente von $M$.")]
        rechnung = f"2^{{{n}}} = {loesung} || jedes der {n} Elemente ist dabei oder nicht dabei"
        tipps = ["Jedes Element ist entweder in der Teilmenge oder nicht.", f"Das sind $2$ Möglichkeiten pro Element, bei {n} Elementen.", f"$2^{{{n}}}$"]
        erkl = f"Hat $M$ genau $n$ Elemente, hat $\\mathcal{{P}}(M)$ genau $2^n$ Elemente. Hier ${loesung}$."
    elif art == "produkt":
        a, b = rng.randint(2, 6), rng.randint(2, 6)
        if a == b:
            b += 1
        A, B = rng.sample(range(1, 12), a), rng.sample(range(1, 12), b)
        loesung = a * b
        frage = f"Es sei $A := {_tex(A)}$ und $B := {_tex(B)}$. Wie viele Elemente hat das kartesische Produkt $A \\times B$?"
        fehler = [(a + b, "Du hast addiert. Zu jedem Element von $A$ gibt es jedes Element von $B$: Die Tupel werden gezählt, also malgenommen."),
                  (a ** 2, f"Das wäre $|A|^2$. Hier haben $A$ und $B$ verschieden viele Elemente: {a} und {b}.")]
        rechnung = f"{a} \\cdot {b} = {loesung} || {a} Möglichkeiten für die erste, {b} für die zweite Stelle"
        tipps = ["Ein Element von $A \\times B$ ist ein Paar $(a, b)$.", "Wie viele Möglichkeiten gibt es für $a$, wie viele für $b$?", f"{a} mal {b}"]
        erkl = f"Ein Paar $(a, b)$ hat {a} Möglichkeiten für $a$ und {b} für $b$, also ${a} \\cdot {b} = {loesung}$."
    else:
        basis = rng.randint(2, 4)
        n = rng.randint(2, 4)
        loesung = basis ** n
        elem = list(range(basis))
        frage = f"Wie viele Elemente hat ${_tex(elem)}^{n}$, also die Menge aller Tupel mit {n} Stellen aus den Zahlen {', '.join(str(e) for e in elem)}?"
        fehler = [(basis * n, f"${basis} \\cdot {n}$ addiert die Möglichkeiten. Sie werden malgenommen: ${basis}^{n}$."),
                  (n ** basis, f"Das vertauscht Basis und Exponent: {n} Stellen mit je {basis} Möglichkeiten sind ${basis}^{n}$.")]
        rechnung = f"{basis}^{n} = {loesung} || je Stelle {basis} Möglichkeiten, {n} Stellen"
        tipps = ["Wie viele Möglichkeiten hat jede Stelle?", "Die Möglichkeiten werden multipliziert.", f"${basis}$ hoch ${n}$"]
        erkl = f"Jede der {n} Stellen hat {basis} Möglichkeiten, insgesamt ${basis}^{n} = {loesung}$ Tupel."
    fehler = [(w, m) for w, m in fehler if w != loesung]
    return {"frage": frage, "loesung": loesung, "tipps": tipps, "rechenweg": ":::rechnung\n" + rechnung + "\n:::",
            "erklaerung": erkl, "typische_fehler": fehler}


_EIGENSCHAFTEN = [
    ("x \\text{ ist gerade}", lambda x: x % 2 == 0), ("x \\text{ ist ungerade}", lambda x: x % 2 == 1),
    ("x > 3", lambda x: x > 3), ("x \\le 6", lambda x: x <= 6), ("x^2 < 30", lambda x: x * x < 30),
    ("x \\text{ ist durch } 3 \\text{ teilbar}", lambda x: x % 3 == 0),
]


def quantor_aussage(rng):
    M = sorted(rng.sample(range(0, 10), rng.randint(4, 5)))
    tex_e, e = rng.choice(_EIGENSCHAFTEN)
    quant = rng.choice(["alle", "exists"])
    trifft = [x for x in M if e(x)]
    kein = [x for x in M if not e(x)]
    if quant == "alle":
        wahr = not kein
        grund = ("Alle Elemente erfüllen die Eigenschaft." if wahr else
                 f"Gegenbeispiel: ${kein[0]}$ erfüllt sie nicht, also ist die $\\forall$-Aussage falsch.")
    else:
        wahr = bool(trifft)
        grund = (f"Zeuge: ${trifft[0]}$ erfüllt die Eigenschaft." if wahr else "Kein Element erfüllt die Eigenschaft, also ist die $\\exists$-Aussage falsch.")
    zeichen = "\\forall" if quant == "alle" else "\\exists"
    return {
        "typ": "wf",
        "frage": f"Die Aussage ${zeichen} x \\in {_tex(M)} : {tex_e}$ ist wahr.",
        "wahr": wahr,
        "tipps": ["Prüfe jedes Element der Menge einzeln.", "Für $\\forall$ suchst du ein Gegenbeispiel, für $\\exists$ einen Zeugen."],
        "erklaerung": grund,
    }


_NEG_EIGENSCHAFTEN = [
    ("x > 3", "x \\le 3", "N"), ("x < 5", "x \\ge 5", "N"), ("x^2 = 4", "x^2 \\neq 4", "Z"),
    ("x \\text{ ist gerade}", "x \\text{ ist ungerade}", "N"), ("x \\text{ ist gerade}", "x \\text{ ist ungerade}", "Z"),
    ("x \\in A", "x \\notin A", "M"),
]


def quantor_negation(rng):
    e, ne, bereich = rng.choice(_NEG_EIGENSCHAFTEN)
    b = {"N": "\\mathbb{N}", "Z": "\\mathbb{Z}", "M": "M"}[bereich]
    erste = rng.choice(["alle", "exists"])
    q, qq = ("\\forall", "\\exists") if erste == "alle" else ("\\exists", "\\forall")
    wort = "alle" if erste == "alle" else "mindestens ein"
    richtig = f"${qq} x \\in {b} : {ne}$"
    optionen = [richtig, f"${q} x \\in {b} : {ne}$", f"${qq} x \\in {b} : {e}$", f"$\\neg ({q} x \\in {b} : {ne})$"]
    fehler = {optionen[1]: "Der Quantor wurde nicht getauscht, nur die Eigenschaft verneint.",
              optionen[2]: "Der Quantor wurde getauscht, aber die Eigenschaft nicht verneint.",
              optionen[3]: "Das ist keine fertige Verneinung. Es steht noch ein $\\neg$ vor der Aussage, und sie ist außerdem nicht die gesuchte."}
    return {
        "typ": "mc",
        "frage": f"Es gilt nicht: ${q} x \\in {b} : {e}$ (also nicht für {wort} $x$). Was gilt stattdessen?",
        "optionen": optionen,
        "fehler": fehler,
        "tipps": ["Verneine den Quantor: aus $\\forall$ wird $\\exists$ und umgekehrt.", "Verneine auch die Eigenschaft."],
        "erklaerung": f"$\\neg({q} x \\in {b} : {e}) \\Leftrightarrow {qq} x \\in {b} : {ne}$: Quantor tauschen, Eigenschaft verneinen.",
    }


k.praxis()

k.generator(mengenverknuepfung, typ="menge", titel="Vereinigung, Schnitt, Differenz bestimmen")
k.generator(potenzmenge_und_produkt, typ="zahl", titel="Elemente von Produkt, Potenz und Potenzmenge zählen")
k.generator(quantor_aussage, typ="wf", titel="Quantoraussage prüfen")
k.generator(quantor_negation, typ="mc", titel="Quantoren negieren")

k.ordnen("Bringe die Richtung ⊇ des Beweises von Satz 1.23 in die richtige Reihenfolge.",
         ["Sei $x \\in (A \\cap B) \\cup (A \\cap C)$ beliebig.",
          "Dann ist $x \\in A \\cap B$ oder $x \\in A \\cap C$.",
          "Fall 1: $x \\in A \\cap B$. Dann $x \\in A$ und $x \\in B$, insbesondere $x \\in B \\cup C$.",
          "Fall 2: $x \\in A \\cap C$. Dann $x \\in A$ und $x \\in C$, also ebenfalls $x \\in B \\cup C$.",
          "In beiden Fällen gilt $x \\in A$ und $x \\in B \\cup C$, also $x \\in A \\cap (B \\cup C)$."],
         "Die Richtung ⊇ läuft rückwärts: Jetzt startet man auf der rechten Seite und muss auf der linken landen. Aus $x \\in B$ folgt $x \\in B \\cup C$ (Oder bilden aus Vorlesung 1).",
         ablenker=["Probe: Für $A = \\{1\\}$, $B = \\{1\\}$, $C = \\emptyset$ stimmen beide Seiten überein.",
                   "Aus $x \\in A \\cap B$ folgt $x \\in C$."],
         alternativen=[["Sei $x \\in (A \\cap B) \\cup (A \\cap C)$ beliebig.",
                        "Dann ist $x \\in A \\cap B$ oder $x \\in A \\cap C$.",
                        "Fall 2: $x \\in A \\cap C$. Dann $x \\in A$ und $x \\in C$, also ebenfalls $x \\in B \\cup C$.",
                        "Fall 1: $x \\in A \\cap B$. Dann $x \\in A$ und $x \\in B$, insbesondere $x \\in B \\cup C$.",
                        "In beiden Fällen gilt $x \\in A$ und $x \\in B \\cup C$, also $x \\in A \\cap (B \\cup C)$."]],
         tipps=["Hier startest du auf der rechten Seite der Gleichung.", "Aus $x \\in B$ folgt immer $x \\in B \\cup C$.",
                "Am Ende steht, dass $x$ in $A$ liegt und in $B \\cup C$."])

k.papier(r"""
    ## Leseaufgabe der Vorlesung: Beweis von Satz 1.23 (⊆ und ⊇)

    Schreibe den Beweis von $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$ ohne Hinschauen auf. Gehe in zwei Richtungen
    vor ($\subseteq$ und $\supseteq$) und benenne bei jedem Schritt, welche Definition du benutzt.
    """,
    r"""
    **Beweis.** Wir zeigen $\subseteq$ und $\supseteq$.

    **(⊆)** Sei $x \in A \cap (B \cup C)$ beliebig. Dann ist $x \in A$ und $x \in B \cup C$, also $x \in B$ oder $x \in C$.
    Ist $x \in B$, folgt mit $x \in A$ zunächst $x \in A \cap B$ und damit $x \in (A \cap B) \cup (A \cap C)$. Ist $x \in C$, folgt mit
    $x \in A$ zunächst $x \in A \cap C$ und damit $x \in (A \cap B) \cup (A \cap C)$. In beiden Fällen gilt also $x \in (A \cap B) \cup (A \cap C)$.

    **(⊇)** Sei nun $x \in (A \cap B) \cup (A \cap C)$ beliebig. Dann ist $x \in A \cap B$ oder $x \in A \cap C$. Ist $x \in A \cap B$, gilt $x \in A$ und
    $x \in B$, insbesondere $x \in B \cup C$ und damit $x \in A \cap (B \cup C)$. Ist $x \in A \cap C$, gilt $x \in A$ und $x \in C$, also ebenfalls
    $x \in B \cup C$ und $x \in A \cap (B \cup C)$.

    Beide Teilmengenbeziehungen gelten, also sind die Mengen gleich. $\square$
    """,
    ["Ich habe gesagt, dass Gleichheit durch zwei Teilmengenbeziehungen ($\\subseteq$ und $\\supseteq$) gezeigt wird",
     "Bei $\\subseteq$ starte ich mit einem beliebigen $x$ der linken Seite, nicht mit einem Zahlenbeispiel",
     "Ich habe $x \\in A$ und $x \\in B \\cup C$ getrennt und das „oder“ mit zwei Fällen behandelt",
     "In beiden Fällen komme ich bei $x \\in (A \\cap B) \\cup (A \\cap C)$ an",
     "Bei $\\supseteq$ starte ich mit einem beliebigen $x$ der rechten Seite und zeige $x \\in A$ und $x \\in B \\cup C$",
     "Ich kann erklären, wo die Fallunterscheidung aus Vorlesung 1 steckt"],
    "Die Leseaufgabe aus der Vorlesung: Wie zeigt man $\\subseteq$ und $\\supseteq$? Mit einem beliebigen Element und den Definitionen von $\\cap$ und $\\cup$.",
    tipps=["Starte mit „Sei $x \\in \\ldots$ beliebig“.", "Pack $\\cap$ und $\\cup$ nach ihrer Definition aus: „und“ und „oder“.",
           "Bei „oder“ brauchst du zwei Fälle, bei „und“ nur eine Aussage."])


def _a_b_aufgabe():
    A, B = {1, 2, 3, 4}, {3, 4, 5}
    pot = _potenz(B)
    assert len(pot) == 8
    return A, B, pot


_A, _B, _POT = _a_b_aufgabe()
_NEG = [x for x in sorted(_A) if not (x >= 2)]
assert _NEG == [1] and not all(x >= 2 for x in _A) and any(x >= 2 for x in _A)
assert _A & _B <= _A and _A - _B == {1, 2} and _B - _A == {5} and _A | _B == {1, 2, 3, 4, 5} and _A & _B == {3, 4}

k.papier(r"""
    ## Übungsblatt-Stil: Mengen und Quantoren

    Es seien $A := \{1, 2, 3, 4\}$ und $B := \{3, 4, 5\}$.

    1. Bestimmen Sie $A \cup B$, $A \cap B$, $A \setminus B$ und $B \setminus A$.
    2. Geben Sie $\mathcal{P}(B)$ an. Wie viele Elemente hat $\mathcal{P}(B)$?
    3. Gilt $\forall x \in A : x \ge 2$? Gilt $\exists x \in A : x \ge 2$? Negieren Sie die erste Aussage und begründen Sie Ihre Antworten.
    4. Beweisen Sie $A \cap B \subseteq A$.
    """,
    f"""**1.** $A \\cup B = {_tex(_A | _B)}$, $A \\cap B = {_tex(_A & _B)}$, $A \\setminus B = {_tex(_A - _B)}$, $B \\setminus A = {_tex(_B - _A)}$.

    **2.** $\\mathcal{{P}}(B) = \\{{{', '.join(_tex(s) for s in sorted(_POT, key=lambda s: (len(s), sorted(s))))}\\}}$. Es sind $2^3 = {len(_POT)}$ Elemente.

    **3.** $\\forall x \\in A : x \\ge 2$ gilt nicht, Gegenbeispiel $x = 1$. $\\exists x \\in A : x \\ge 2$ gilt, Zeuge $x = 2$. Negation: $\\neg(\\forall x \\in A : x \\ge 2) \\Leftrightarrow \\exists x \\in A : x < 2$.
    Diese Aussage gilt (Zeuge $x = 1$), passend dazu, dass die Ausgangsaussage falsch ist.

    **4.** Sei $x \\in A \\cap B$ beliebig. Dann ist $x \\in A$ und $x \\in B$ (Definition des Schnitts). Insbesondere gilt $x \\in A$. Also ist $A \\cap B \\subseteq A$. $\\square$""",
    ["Meine Vereinigung enthält jedes Element nur einmal, und $B \\setminus A$ ist $\\{5\\}$",
     "$\\mathcal{P}(B)$ hat $8$ Elemente, darunter $\\emptyset$ und $B$ selbst",
     "Ich habe für $\\forall$ ein Gegenbeispiel und für $\\exists$ einen Zeugen angegeben",
     "Meine Negation lautet $\\exists x \\in A : x < 2$ (Quantor getauscht, Eigenschaft verneint)",
     "Mein Beweis beginnt mit einem beliebigen $x \\in A \\cap B$ und benutzt die Definition des Schnitts"],
    "Das sind alle Bausteine der Vorlesung in einer Aufgabe: Operationen, Potenzmenge, Quantoren, ein kleiner Mengenbeweis.",
    uebungsblatt=True,
    tipps=["Schreibe die Mengen zuerst vollständig auf.", "Bei der Potenzmenge: alle Auswahlen, auch nichts und alles.",
           "Bei Teil 4 reicht die Definition von $\\cap$."])

k.rechenweg_aufgabe(
    "Es sei $G := \\{1, 2, 3, 4, 5\\}$ und das Mengensystem $\\mathcal{F} := \\{\\{1, 2, 3\\}, \\{2, 3, 4\\}, \\{3, 4, 5\\}\\}$. Bestimme Vereinigung und Schnitt über $\\mathcal{F}$.",
    [{"typ": "menge", "frage": "Schritt 1: $\\bigcup_{M \\in \\mathcal{F}} M$ (alles, was in **mindestens einer** Menge liegt). Trenne mit **;**.",
      "loesung": "{1; 2; 3; 4; 5}", "tipps": ["Sammle alle Elemente aus den drei Mengen.", "Jedes Element nur einmal."],
      "rechenweg": "Aus $\\{1, 2, 3\\}$, $\\{2, 3, 4\\}$ und $\\{3, 4, 5\\}$ kommen zusammen die Zahlen $1$ bis $5$.",
      "typische_fehler": [("{3}", "Das ist der Schnitt. Die Vereinigung sammelt alles, was in mindestens einer Menge liegt.")]},
     {"typ": "menge", "frage": "Schritt 2: $\\bigcap_{M \\in \\mathcal{F}} M$ (was in **jeder** Menge liegt). Trenne mit **;**.",
      "loesung": "{3}", "tipps": ["Prüfe jedes Element von $G$: Liegt es in allen drei Mengen?", "Die $1$ fehlt in der zweiten Menge."],
      "rechenweg": "Nur die $3$ liegt in allen drei Mengen. Die $2$ fehlt in $\\{3, 4, 5\\}$, die $4$ fehlt in $\\{1, 2, 3\\}$.",
      "typische_fehler": [("{1; 2; 3; 4; 5}", "Das ist die Vereinigung. Der Schnitt verlangt, dass das Element in **jeder** Menge liegt.")]}],
    "Vereinigung heißt $\\exists M \\in \\mathcal{F} : x \\in M$, Schnitt heißt $\\forall M \\in \\mathcal{F} : x \\in M$ (Definition 1.34). Mit dem Folienbeispiel haben wir dasselbe in klein gerechnet.",
    tipps=["Vereinigung: mindestens eine Menge, Schnitt: jede Menge.", "Prüfe jedes Element von $G$ einzeln."],
    rechenweg="$\\bigcup M = \\{1, 2, 3, 4, 5\\}$ und $\\bigcap M = \\{3\\}$.")

k.zusammenfassung(r"""
    ## Das musst du nach Vorlesung 2 können

    - **Menge:** ungeordnete Sammlung, nur „drin oder nicht“ zählt. $e \in M$, $e \notin M$. Die Sammlung aller Mengen, die sich nicht selbst enthalten, ist keine Menge (Russell).
    - $N \subseteq M$: jedes Element von $N$ liegt in $M$. $N = M$ genau dann, wenn $N \subseteq M$ und $M \subseteq N$. $\emptyset \subseteq M$ für jede Menge.
    - **Achtung:** $0 \in \{0, 1\}$ (Element) und $\{0\} \subseteq \{0, 1\}$ (Teilmenge). $\{0\} \in \{0, 1\}$ und $\emptyset \in \{0, 1\}$ sind falsch.
    - $\mathbb{N} = \{0, 1, 2, \ldots\}$, $\mathbb{Z} = \{\ldots, -1, 0, 1, \ldots\}$, $\mathbb{Z}_{\ge 0} = \mathbb{Z} \cap \{x \in \mathbb{R} \mid x \ge 0\}$.

    | Erzeugungsweise | Schreibweise | Beispiel |
    |---|---|---|
    | Aufzählung | $\{a, b, c\}$ | $\{0, 1, 2, 3\}$ |
    | Aussonderung | $\{x \in G \mid E(x)\}$ | $\{n \in \mathbb{N} \mid n \le 5\}$ |
    | Vereinigung, Schnitt, Differenz | $M \cup N$, $M \cap N$, $M \setminus N$ | $\{a, b\} \cap \{b, c\} = \{b\}$ |
    | kartesisches Produkt | $A_1 \times \cdots \times A_n$ | $\{0, 1\}^3$ hat $8$ Tupel |
    | Potenzmenge | $\mathcal{P}(M)$ | $\mathcal{P}(\{a, b\})$ hat $4$ Elemente, $\mathcal{P}(M)$ hat $2^{\lvert M \rvert}$ |

    - **Tupel:** geordnet, Wiederholungen zählen: $(0, 1) \neq (1, 0)$, $(0, 0, 1) \neq (0, 1)$. Menge: $\{0, 1\} = \{1, 0\}$, $\{0, 0, 1\} = \{0, 1\}$.
    - **Satz 1.23:** $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$. Beweis: $\subseteq$ und $\supseteq$, je mit einem beliebigen $x$ und einer Fallunterscheidung.
    - $\forall x \in M : E(x)$: für alle. $\exists x \in M : E(x)$: für mindestens ein. $\forall$ widerlegt man mit einem Gegenbeispiel, $\exists$ beweist man mit einem Zeugen.
    - $\neg(\forall x \in M : E(x)) \Leftrightarrow \exists x \in M : \neg E(x)$ und $\neg(\exists x \in M : E(x)) \Leftrightarrow \forall x \in M : \neg E(x)$.
    - $\bigcup_{M \in \mathcal{F}} M$: $\exists M$ mit $x \in M$. $\bigcap_{M \in \mathcal{F}} M$: $\forall M$ mit $x \in M$. Für $\mathcal{F} = \emptyset$ ist die Vereinigung $\emptyset$ und der Schnitt $G$.

    **Querbezüge laut Folie:** AFE (formale Sprachen als Mengen von Wörtern), Datenbanken (Tupel und Mengenoperationen).
    Vertiefung: Kapitel „Mengen“, „All- und Existenzquantor“ und die Vorkurs-Kapitel zu Mengen und Quantoren.

    !! $\in$ verbindet ein Element mit einer Menge, $\subseteq$ verbindet zwei Mengen.
""")
