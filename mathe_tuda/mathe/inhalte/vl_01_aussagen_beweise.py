# -*- coding: utf-8 -*-
"""Vorlesung 1 (12.10.2026): Aussagen und Beweise, Skript Disser 1.1 bis 1.3, Folien VL01.

Folienreihenfolge: Aussagen und Aussageformen, logische Verknüpfungen, Kontraposition, De Morgan,
Sätze und Beweise, Schlussregeln, gerade und ungerade Zahlen, die fünf Beweisformen."""
import itertools
import json
import re
from fractions import Fraction as F

from ..engine import neues_kapitel, ohne_gleiche
from ..visuals import logik_parse, logik_wert

k = neues_kapitel(
    slug="vl01",
    titel="Vorlesung 1: Aussagen und Beweise",
    beschreibung="Aussagen, logische Verknüpfungen, Kontraposition, De Morgan und die fünf Beweisformen, von Null erklärt",
    teil="vorlesung",
    quelle="Vorlesung 1 (12.10.2026), Folien VL 01, Skript Disser 1.1 bis 1.3",
    icon="🎓")

k.lernziele([
    "Ich kann entscheiden, ob ein Ausdruck eine Aussage oder eine Aussageform ist, und eine Aussageform belegen",
    "Ich kann $\\neg$, $\\land$, $\\lor$, $\\oplus$, $\\Rightarrow$, $\\Leftrightarrow$ in Worten erklären und ihre Wahrheitstabellen aufstellen",
    "Ich kenne das Kontrapositionsgesetz und die Regeln von De Morgan und wende sie an",
    "Ich kann „gerade“ und „ungerade“ als $n = 2a$ und $n = 2a + 1$ nutzen und die fünf Beweisformen an ihrem Muster erkennen",
    "Ich kann die Beweise der Sätze 1.16, 1.17, 1.18 und 1.20 Schritt für Schritt nachvollziehen",
])

k.warum(r"""
Jede `if`-Bedingung in einem Programm ist eine Aussage, `and`, `or` und `not` sind $\land$, $\lor$ und $\neg$
(Programmierung). Logische Gatter in einer Schaltung rechnen genau diese Wahrheitstabellen (Digitaltechnik).
Wer beweisen kann, dass ein Algorithmus immer das Richtige liefert, braucht die Beweisformen dieser Vorlesung
(Algorithmen und Verifikation), und die Grenzen der Berechenbarkeit zeigt man mit Widerspruchsbeweisen (AFE).
Dazu kommt: In Mathe I geht es weniger ums Rechnen als darum, **sauber und lückenlos zu begründen**.
""")


# ── Python rechnet die Logik ───────────────────────────────────────────────
def _spalte(formel, variablen=("P", "Q")):
    """Wahrheitswerte in Folienreihenfolge (w w, w f, f w, f f)."""
    ast = logik_parse(formel)
    return [logik_wert(ast, dict(zip(variablen, w))) for w in itertools.product([True, False], repeat=len(variablen))]


def _wf(werte):
    return ", ".join("w" if w else "f" for w in werte)


def _gleich(a, b, variablen=("P", "Q")):
    return _spalte(a, variablen) == _spalte(b, variablen)


def _vis(variablen, ausdruecke, **extra):
    d = {"variablen": list(variablen), "ausdruecke": list(ausdruecke)}
    d.update(extra)
    return ":::visual wahrheitstabelle\n    " + json.dumps(d, ensure_ascii=False) + "\n    :::"


# Folienwerte (Wahrheitstabellen), beim Laden nachgerechnet
assert _spalte("P ∧ Q") == [True, False, False, False]
assert _spalte("P ∨ Q") == [True, True, True, False]
assert _spalte("P ⊕ Q") == [False, True, True, False]
assert _spalte("P ⇒ Q") == [True, False, True, True]
assert _spalte("P ⇔ Q") == [True, False, False, True]
assert _spalte("¬P") == [False, False, True, True]
assert 2 ** 4 == 16
# Bemerkung 1.9: XOR nur mit ¬ und ∧ bzw. nur mit ¬ und ∨
assert _gleich("P ⊕ Q", "¬(P ∧ Q) ∧ ¬(¬P ∧ ¬Q)")
assert _gleich("P ⊕ Q", "¬(¬P ∨ Q) ∨ ¬(P ∨ ¬Q)")
# Satz 1.12 Kontrapositionsgesetz, Beweis durch Äquivalenzumformung (Folie 22)
assert _gleich("P ⇒ Q", "¬Q ⇒ ¬P")
assert _gleich("P ⇒ Q", "¬P ∨ Q") and _gleich("¬P ∨ Q", "Q ∨ ¬P") and _gleich("Q ∨ ¬P", "¬(¬Q) ∨ ¬P")
assert not _gleich("P ⇒ Q", "¬P ⇒ ¬Q") and not _gleich("P ⇒ Q", "Q ⇒ P")
# Satz 1.14 De Morgan
assert _gleich("¬(P ∨ Q)", "¬P ∧ ¬Q") and _gleich("¬(P ∧ Q)", "¬P ∨ ¬Q")
# Negation einer Implikation (Widerspruchsbeweis): einzige falsche Zeile ist P wahr, Q falsch
assert _gleich("¬(P ⇒ Q)", "P ∧ ¬Q")
# Satz 1.19 ist eine Tautologie
assert all(logik_wert(logik_parse("((P ⇒ R) ∧ (Q ⇒ R)) ⇒ ((P ∨ Q) ⇒ R)"), dict(zip("PQR", w)))
           for w in itertools.product([True, False], repeat=3))
# Schlussregeln (Folie 19) sind Tautologien
for _regel in ("(P ∧ (P ⇒ Q)) ⇒ Q", "((P ⇒ Q) ∧ ¬Q) ⇒ ¬P", "((P ∨ Q) ∧ ¬P) ⇒ Q", "(P ∧ Q) ⇒ (P ∧ Q)",
               "(P ∧ Q) ⇒ P", "P ⇒ (P ∨ Q)"):
    assert all(logik_wert(logik_parse(_regel), dict(zip("PQ", w))) for w in itertools.product([True, False], repeat=2))

# Folienbeispiele zu gerade/ungerade, Sätze 1.16, 1.17, 1.18, 1.20 an vielen Zahlen geprüft (kein Beweis!)
assert all((n + m) % 2 == 0 for n in range(-20, 21, 2) for m in range(-20, 21, 2))
assert all(n % 2 == 0 for n in range(-50, 51) if (n * n) % 2 == 0)
assert all((n * (n + 1)) % 2 == 0 for n in range(-50, 51))
assert (4 == 2 * 2) and (5 == 2 * 2 + 1)
assert all((2 * a + 1) ** 2 == 2 * (2 * a * a + 2 * a) + 1 for a in range(-30, 31))
assert all(2 * a * (2 * a + 1) == 2 * (2 * a * a + a) for a in range(-30, 31))
assert all((2 * a + 1) * (2 * a + 2) == 2 * (2 * a * a + 3 * a + 1) for a in range(-30, 31))
# kein Bruch n/m mit n^2 = 2 m^2 für kleine Zahlen (Satz 1.18 ist kein Zählbeweis, nur eine Probe)
assert not any(n * n == 2 * m * m for n in range(1, 300) for m in range(1, 300))


# ═══ Seiten 1 und 2: Aussagen, Aussageformen (Skript 1.1, Folien 5 und 6) ═════════════════════════
k.erklaerung("Aussagen und Aussageformen (Skript 1.1)", r"""
    ## Aussage und Aussageform

    :::analogie 🚦 Ja-Nein-Frage und Lückentext
    „Liegt Frankfurt in Hessen?“ beantwortest du mit ja. „Mach das Fenster zu!“ ist ein Befehl: Er stimmt nicht
    und stimmt nicht nicht. „Hallo ___“ ist ein Satz mit Lücke, erst mit einem Namen ist er vollständig.
    :::

    Mathematik beginnt damit, aus Bekanntem Neues zu schließen. Eine [[Aussage]] (Definition 1.1) ist ein
    Ausdruck, der entweder **wahr** oder **falsch** ist. Eine wahre Aussage **gilt**. Es zählt nur, dass es
    eine eindeutige Antwort *gibt*, auch falsche Aussagen sind Aussagen. Eine [[Aussageform]]
    (Definition 1.3) enthält [[Variablen|Variable]]. Erst eine [[Belegung]] (für jede Variable einen Wert
    einsetzen) macht daraus eine Aussage. $3x < 8$ ist also keine Aussage, sondern eine Aussageform.

    :::rechnung Ein Schluss aus dem Skript (1.1)
    \text{A: Der Einheitskreis hat Radius 1.} || Aussage, wahr
    \text{B: Hat ein Kreis Radius 1, so beträgt seine Fläche } \pi. || Aussage, wahr
    \text{C: Die Fläche des Einheitskreises beträgt } \pi. || folgt aus A und B: so schließt man
    :::

    :::rechnung Beispiel 1.2: Aussagen und Nicht-Aussagen
    \text{Die Zahl 3 ist ungerade.} \quad \text{wahr} || Aussage
    \text{3 + 5 = 9.} \quad \text{falsch} || trotzdem eine Aussage
    \text{Es regnet gerade in Madrid.} \quad \text{unbekannt} || eindeutig, wir kennen den Wert nur nicht
    \text{Guten Morgen.} \quad \text{keine Aussage} || ein Gruß
    \text{Besuchen Sie möglichst alle Vorlesungen!} \quad \text{keine Aussage} || eine Aufforderung
    :::

    :::rechnung Beispiel 1.4: Die drei Aussageformen der Folie
    B_1(x): \text{Die Zahl } x \text{ ist gerade.} || Aussageform mit einer Variablen
    B_2(a, b): \text{Es gilt } a \le b. || Aussageform mit zwei Variablen
    B_3(r): \text{Hat ein Kreis Radius } r \text{, so beträgt seine Fläche } \pi r^2. || das Gesetz von eben, allgemein
    B_1(4) \quad \text{wahr} || 4 ist gerade
    B_1(5) \quad \text{falsch} || 5 ist ungerade
    B_2(4, 5) \quad \text{wahr} || 4 \le 5 stimmt
    B_2(5, 4) \quad \text{falsch} || 5 \le 4 stimmt nicht
    B_3(1) \quad \text{wahr} || das ist genau Aussage B vom Einheitskreis
    :::

    :::rechnung Wo wir stehen: Mathe I im Überblick (Folie 4)
    \text{1 Grundlagen} || Logik, Mengen, Abbildungen: hier fängst du an
    \text{2 Zählen und Arithmetik} || Induktion, Zählen, Arithmetik
    \text{3 Zahlenräume} || Zahlenräume, Strukturen, Homomorphismen
    \text{4 Mehrdimensionale Räume} || Räume, Basen, Projektion
    \text{5 Lineare Abbildungen} || lineare Abbildungen, Matrizen, Basiswechsel
    \text{6 LGS und Eigenwerte} || Gauß-Verfahren, Determinanten, Eigenwerte
    \text{7 Wachstum und Grenzwerte} || Folgen, Reihen, Asymptotik
    :::

    :::alt Mit Prüfstempel und Python erklärt
    Stell dir einen Prüfer vor, der jeden Satz stempeln muss: „stimmt“ oder „stimmt nicht“. Bei „3 + 5 = 9“
    stempelt er „stimmt nicht“, bei „Guten Morgen“ weiß er nicht, was er stempeln soll: keine Aussage. Eine
    Aussageform ist wie `def B1(x): return x % 2 == 0`. Ohne Argument gibt es keinen Wahrheitswert, `B1(4)`
    liefert `True`, `B1(5)` liefert `False`. Die Belegung ist das Argument.
    :::
    """)

k.zuordnen("Ordne jedem Ausdruck zu, was er ist.",
           [("„Die Zahl 3 ist ungerade.“", "Aussage, wahr"),
            ("„$3 + 5 = 9$.“", "Aussage, falsch"),
            ("„Die Zahl $x$ ist gerade.“", "Aussageform"),
            ("„Besuchen Sie möglichst alle Vorlesungen!“", "weder Aussage noch Aussageform")],
           "Die ersten beiden haben eine eindeutige Antwort, auch das falsche $3 + 5 = 9$. „Die Zahl $x$ ist gerade“ "
           "braucht erst eine Belegung (Aussageform). Eine Aufforderung ist weder wahr noch falsch.",
           tipps=["Frag bei jedem Ausdruck: Gibt es sofort eine eindeutige Antwort? Oder erst nach dem Einsetzen? Oder nie?"])

k.mc("Welcher Ausdruck wird durch die Belegung $x = 5$ zu einer **wahren** Aussage?",
     ["„$3x < 20$“", "„$3x < 8$“", "„$3x = 16$“", "„$3x$“"],
     "$3 \\cdot 5 = 15 < 20$ ist wahr. $15 < 8$ und $15 = 16$ sind falsch. $3x$ ist nur ein Term und wird nie wahr oder falsch.",
     tipps=["Setze $x = 5$ ein und prüfe jede Aussage einzeln.", "Rechne zuerst $3 \\cdot 5$."],
     fehler={"„$3x < 8$“": "Mit $x = 5$ steht da $15 < 8$. Das ist falsch, aber eine Aussage. Gefragt war nach der **wahren**.",
             "„$3x$“": "$3x$ ist ein Term ohne Vergleich. Auch nach dem Einsetzen kommt nur eine Zahl heraus, keine Aussage."})


# ═══ Seite 3: ¬ ∧ ∨ ⊕ und die 16 Verknüpfungen (Skript 1.2, Folien 7 bis 10) ══════════════════════
k.erklaerung("Negation, und, oder (Skript 1.2)", r"""
    ## Aus Aussagen neue Aussagen bauen

    :::analogie 🍝 Hunger und Zeit
    P: „Ich habe Hunger.“ Q: „Ich habe Zeit.“ Es gibt vier mögliche Welten: beides, nur P, nur Q,
    keins. Für jede Welt sagt eine Tabelle, ob „P und Q“ stimmt.
    :::

    Die [[Negation]] $\neg P$ (Definition 1.5) sagt „$P$ ist falsch“. Die [[Konjunktion]] $P \land Q$
    (1.6) ist wahr, wenn $P$ **und** $Q$ wahr sind. Die [[Disjunktion]] $P \lor Q$ (1.7) ist wahr, wenn
    $P$ **oder** $Q$ wahr ist. Diese Tabelle heißt [[Wahrheitstabelle|Wahrheitstafel]]: eine Zeile pro Kombination
    der Wahrheitswerte. Reihenfolge: wahr/wahr, wahr/falsch, falsch/wahr, falsch/falsch.

    """ + _vis(["P", "Q"], ["¬P", "P ∧ Q", "P ∨ Q", "P ⊕ Q"],
               unterschrift="Folie 7 bis 9: $\\neg$, $\\land$, $\\lor$ und $\\oplus$. Nur bei $\\text{w}, \\text{w}$ unterscheiden sich $\\lor$ und $\\oplus$.") + r"""

    So liest du eine Zeile: Zeile 2 heißt „$P$ ist wahr und $Q$ ist falsch“. Dann ist $P \land Q$ falsch,
    $P \lor Q$ wahr. Bemerkung 1.8: $P \lor Q$ gilt auch, wenn **beide** gelten. „Genau eine“ heißt Kontravalenz
    (exklusives Oder, [[XOR|Kontravalenz]]) $P \oplus Q$. Bemerkung 1.9: Jede der $2^4 = 16$ Verknüpfungen
    zweier Aussagen lässt sich nur mit $\neg$ und $\land$ ausdrücken, oder nur mit $\neg$ und $\lor$.

    :::rechnung Beispiele: ¬ und XOR
    \text{P: 3 + 5 = 9 (falsch)} || eine Aussage
    \neg P: \text{Die Aussage } 3 + 5 = 9 \text{ ist falsch. (wahr)} || Negation dreht den Wert um
    P \oplus Q = \neg(P \land Q) \land \neg(\neg P \land \neg Q) || „nicht beide“ und „nicht keine“
    P \oplus Q = \neg(\neg P \lor Q) \lor \neg(P \lor \neg Q) || zweite Darstellung, nur mit ¬ und ∨
    :::

    :::alt Mit einem Rabatt erklärt
    Rabatt mit Ausweis **und** Gutschein: Beides muss vorliegen. Rabatt mit Ausweis **oder** Gutschein:
    Eins reicht, und wer beides hat, bekommt ihn natürlich auch. Das alltägliche „Eis oder Kuchen, aber nicht
    beides“ ist dagegen das XOR $\oplus$. Es gibt 16 Verknüpfungen, weil jede der vier Zeilen
    wahr oder falsch sein kann: $2 \cdot 2 \cdot 2 \cdot 2 = 16$.
    :::
    """)

k.mc("Pingo-Frage der Vorlesung: Was bedeutet „$P$ oder $Q$“, also $P \\lor Q$?",
     ["Mindestens eine der beiden Aussagen ist wahr.", "Genau eine der beiden Aussagen ist wahr.",
      "Beide Aussagen sind wahr.", "Keine der beiden Aussagen ist wahr."],
     "Das mathematische „oder“ ist großzügig: Es ist auch wahr, wenn beide Aussagen gelten (Bemerkung 1.8). "
     "Das „genau eine“ ist das XOR $\\oplus$.",
     tipps=["Schau in die Zeile der Tabelle, in der $P$ und $Q$ beide wahr sind.", "In welchen Zeilen ist $P \\lor Q$ falsch?"],
     fehler={"Genau eine der beiden Aussagen ist wahr.": "Das ist $P \\oplus Q$ (Kontravalenz). Bei $P \\lor Q$ ist auch die Zeile wahr/wahr wahr.",
             "Beide Aussagen sind wahr.": "Das ist $P \\land Q$ („und“)."})

k.zahl("Wie viele verschiedene Verknüpfungen zweier Aussagen $P$ und $Q$ gibt es (Bemerkung 1.9)?", 16,
       "Die Wahrheitstabelle hat $4$ Zeilen. In jeder Zeile kann das Ergebnis wahr oder falsch sein: $2^4 = 16$.",
       tipps=["Zähle die Zeilen der Tabelle.", "Jede Zeile hat zwei mögliche Ergebnisse.", "$2 \\cdot 2 \\cdot 2 \\cdot 2$"],
       rechenweg=r"""
       :::rechnung
       2 \cdot 2 \cdot 2 \cdot 2 = 16 || vier Zeilen, je zwei mögliche Ergebnisse
       2^4 = 16 || kürzer geschrieben
       :::
       """,
       typische_fehler=[(8, "$8 = 2^3$ wäre bei **drei** Zeilen richtig. Die Tabelle hat vier Zeilen."),
                        (4, "$4$ ist die Zahl der Zeilen. Jede Zeile hat aber noch zwei mögliche Ergebnisse.")])


# ═══ Seite 4: Implikation (Definition 1.10, Folie 11) ═════════════════════════════════════════════
k.erklaerung("Die Implikation (Skript 1.2)", r"""
    ## Wenn-dann ist ein Versprechen

    :::analogie 🍦 Das Versprechen
    „Wenn du die Prüfung bestehst, bekommst du ein Eis.“ Gebrochen ist es nur, wenn du bestehst **und**
    kein Eis bekommst. Bestehst du nicht, ist es egal, ob es Eis gibt: Das Versprechen sagte dazu nichts.
    :::

    Die [[Implikation]] $P \Rightarrow Q$ (Definition 1.10) heißt: Wenn $P$ wahr ist, dann ist $Q$ wahr.
    Sie ist **nur** falsch, wenn $P$ wahr und $Q$ falsch ist. Ist $P$ falsch, ist sie immer wahr
    ([[ex falso quodlibet]]: aus Falschem folgt Beliebiges). Sprechweisen: „aus $P$ folgt $Q$“, „$P$ impliziert $Q$“,
    $P$ ist [[hinreichend|hinreichende Bedingung]] für $Q$, $Q$ ist [[notwendig|notwendige Bedingung]] für $P$.

    """ + _vis(["P", "Q"], ["P ⇒ Q", "¬P ∨ Q"],
               unterschrift="Folie 11: Falsch nur in Zeile 2. Die zweite Spalte $\\neg P \\lor Q$ ist identisch. Das brauchen wir bei den Beweisen.") + r"""

    !! $P \Rightarrow Q$ ist nur falsch, wenn $P$ wahr und $Q$ falsch ist. Das ist die wichtigste Zeile dieser Vorlesung.

    :::rechnung Das Beispiel von Bertrand Russell (Folie 11)
    \text{Annahme: } 0 = 1 || eine falsche Aussage
    \text{Addiere 1 auf beiden Seiten: } 1 = 2 || folgt aus der Annahme
    \text{Russell und der Papst sind 2 Personen.} || nach der Annahme 2 = 1:
    \text{Russell und der Papst sind 1 Person.} || also ist Russell der Papst
    \text{Die ganze Kette ist wahr, weil die Annahme falsch ist.} || genau das heißt ex falso quodlibet
    :::

    :::alt Straße und Regen
    „Wenn es regnet, ist die Straße nass.“ Regen **reicht aus** für nasse Straße: hinreichend. Nass kann die
    Straße auch ohne Regen sein (Gießwagen). Aber ohne nasse Straße kann es nicht geregnet haben: Die nasse
    Straße ist **nötig** für Regen, also notwendig. Und ein Programm, das nicht terminiert, widerlegt
    „Wenn es terminiert, ist das Ergebnis richtig“ nicht.
    :::
    """)

k.mc("Pingo-Frage: In welchem Fall ist $P \\Rightarrow Q$ falsch?",
     ["$P$ wahr und $Q$ falsch.", "$P$ falsch und $Q$ wahr.", "$P$ falsch und $Q$ falsch.", "$P$ wahr und $Q$ wahr."],
     "Das Versprechen ist nur gebrochen, wenn die Bedingung eintritt ($P$ wahr) und das Versprochene nicht ($Q$ falsch). "
     "Ist $P$ falsch, ist die Implikation wahr (ex falso quodlibet).",
     tipps=["Denk an das Eis-Versprechen: Wann hat jemand es gebrochen?", "Die Bedingung muss eintreten, sonst ist nichts versprochen."],
     fehler={"$P$ falsch und $Q$ wahr.": "Ist $P$ falsch, kann das Versprechen nicht gebrochen werden. Die Implikation ist dann wahr.",
             "$P$ falsch und $Q$ falsch.": "Auch hier ist $P$ falsch, also ist die Implikation wahr. „Aus Falschem folgt alles.“"})

k.mc("Pingo-Frage: „Wenn ein Programm terminiert, liefert es das richtige Ergebnis.“ Wann ist diese Aussage **widerlegt**?",
     ["Das Programm terminiert, liefert aber ein falsches Ergebnis.",
      "Das Programm terminiert nicht.",
      "Das Programm terminiert und liefert das richtige Ergebnis.",
      "Das Programm terminiert nicht und liefert ein falsches Ergebnis."],
     "$P$: „Das Programm terminiert.“ $Q$: „Das Programm liefert das richtige Ergebnis.“ Widerlegt ist $P \\Rightarrow Q$ nur bei "
     "$P$ wahr und $Q$ falsch. Es gilt $\\neg(P \\Rightarrow Q) \\Leftrightarrow (P \\land \\neg Q)$.",
     tipps=["Schreibe die Aussage als $P \\Rightarrow Q$.", "Eine Implikation ist nur in einer Zeile falsch: $P$ wahr, $Q$ falsch."],
     fehler={"Das Programm terminiert nicht.": "Wenn es nicht terminiert, ist die Bedingung $P$ nicht erfüllt. Dann sagt die Aussage nichts, sie wird nicht widerlegt.",
             "Das Programm terminiert nicht und liefert ein falsches Ergebnis.": "Auch hier gilt $P$ nicht. Widerlegen kann nur ein Programm, bei dem $P$ stimmt und $Q$ nicht."})


# ═══ Seite 5: Äquivalenz, Kontrapositionsgesetz (Definition 1.11, Satz 1.12, Beispiel 1.13) ═══════
k.erklaerung("Äquivalenz und Kontraposition (Skript 1.2)", r"""
    ## Genau dasselbe, nur andersherum aufgeschrieben

    :::analogie 🌧️ Regen und Straße
    „Regnet es, ist die Straße nass“ sagt dasselbe wie „Ist die Straße trocken, regnet es nicht“. Nur
    verneint und umgedreht. „Ist die Straße nass, regnet es“ sagt etwas anderes.
    :::

    Die [[Äquivalenz]] $P \Leftrightarrow Q$ (Definition 1.11) heißt: $P \Rightarrow Q$ **und** $Q \Rightarrow P$.
    Man sagt „$P$ gilt genau dann, wenn $Q$ gilt“. $P$ und $Q$ haben in jeder Zeile denselben Wert. Satz 1.12
    ([[Kontrapositionsgesetz]]): $(P \Rightarrow Q) \Leftrightarrow (\neg Q \Rightarrow \neg P)$. Beweis: Die
    beiden Spalten der Tabelle stimmen überein.

    """ + _vis(["P", "Q"], ["P ⇒ Q", "¬Q ⇒ ¬P", "¬P ⇒ ¬Q"], markiert=["¬Q ⇒ ¬P"],
               unterschrift="Folie 13: Spalte 1 und 2 sind gleich (Kontraposition). Spalte 3 weicht ab: $\\neg P \\Rightarrow \\neg Q$ ist **nicht** gleichwertig.") + r"""

    :::rechnung Beispiel 1.13 (Folie 14)
    \text{P: Jemand im Vorlesungssaal heißt Anna.} || der Saal liegt in Darmstadt
    \text{Q: Jemand in Darmstadt heißt Anna.} ||
    P \Rightarrow Q \quad \text{gilt} || eine Anna im Saal ist auch eine Anna in Darmstadt
    \neg Q \Rightarrow \neg P \quad \text{gilt} || heißt niemand in Darmstadt Anna, dann auch niemand im Saal
    \neg P \Rightarrow \neg Q \quad \text{gilt nicht} || eine Anna in Darmstadt muss nicht in unserem Saal sitzen
    :::

    :::achtung Zwei verbreitete Denkfehler
    Nur **verneinen** (aus $P \Rightarrow Q$ wird $\neg P \Rightarrow \neg Q$) oder nur **umdrehen** (aus $P \Rightarrow Q$
    wird $Q \Rightarrow P$) ändert die Aussage. Erst beides zusammen ergibt die Kontraposition.
    :::

    :::alt Mit Spielkarten erklärt
    „Jede Herzkarte ist rot.“ Dann ist auch jede **nicht-rote** Karte nicht Herz (Kontraposition). Aber aus
    „nicht Herz“ darfst du nicht auf „nicht rot“ schließen: Karo ist nicht Herz und trotzdem rot.
    Merke: Zuerst umdrehen **und** beides verneinen.
    :::
    """)

k.mehrfach("Welche Aussagen sind gleichwertig zu $P \\Rightarrow Q$?",
           ["$\\neg Q \\Rightarrow \\neg P$", "$\\neg P \\lor Q$"],
           ["$Q \\Rightarrow P$", "$\\neg P \\Rightarrow \\neg Q$", "$P \\land \\neg Q$"],
           "Gleichwertig sind die Kontraposition $\\neg Q \\Rightarrow \\neg P$ (Satz 1.12) und $\\neg P \\lor Q$ (gleiche Spalte der Tabelle). "
           "Die Umkehrung $Q \\Rightarrow P$ und $\\neg P \\Rightarrow \\neg Q$ sind verschiedene Aussagen. $P \\land \\neg Q$ ist die **Negation** von $P \\Rightarrow Q$.",
           tipps=["Vergleiche die Spalten in der Wahrheitstabelle.", "Zeile 2 ($P$ wahr, $Q$ falsch) ist bei $P \\Rightarrow Q$ falsch. Wo sonst noch?"],
           fehler={"$Q \\Rightarrow P$": "Das ist die Umkehrung, nicht die Kontraposition. Sie ist in Zeile 3 falsch, $P \\Rightarrow Q$ dort aber wahr.",
                   "$\\neg P \\Rightarrow \\neg Q$": "Das ist die Umkehrung in verneinter Form (Anna-Beispiel): Nur verneinen, nicht umdrehen, geht nicht.",
                   "$P \\land \\neg Q$": "Das ist genau der Fall, in dem $P \\Rightarrow Q$ **falsch** ist, also die Negation."})

k.mc("Pingo-Frage: „Wenn jemand Zugriff hat, ist er angemeldet.“ Welche Aussage bedeutet dasselbe?",
     ["Ist jemand nicht angemeldet, hat er keinen Zugriff.",
      "Ist jemand angemeldet, hat er Zugriff.",
      "Hat jemand keinen Zugriff, ist er nicht angemeldet.",
      "Ist jemand angemeldet, hat er keinen Zugriff."],
     "$P$: „hat Zugriff“, $Q$: „ist angemeldet“. Die Kontraposition $\\neg Q \\Rightarrow \\neg P$ lautet: nicht angemeldet, dann kein Zugriff.",
     tipps=["Aus $P \\Rightarrow Q$ wird $\\neg Q \\Rightarrow \\neg P$: verneinen **und** umdrehen.", "Wer ist die Voraussetzung der neuen Aussage? Das Verneinte aus dem Ende der alten."],
     fehler={"Ist jemand angemeldet, hat er Zugriff.": "Das ist die Umkehrung $Q \\Rightarrow P$. Angemeldet zu sein reicht vielleicht nicht für Zugriff.",
             "Hat jemand keinen Zugriff, ist er nicht angemeldet.": "Das ist $\\neg P \\Rightarrow \\neg Q$: Du hast verneint, aber nicht umgedreht."})


# ═══ Seite 6: De Morgan, Satz/Beweis/Definition (Satz 1.14; Skript 1.3 Anfang, Folien 15 und 17) ═════
k.erklaerung("De Morgan und was ein Beweis ist", r"""
    ## Wie man „und“ und „oder“ verneint

    :::analogie ☔ Weder noch
    „Es regnet **oder** es schneit“ stimmt nicht. Dann regnet es nicht **und** es schneit nicht: weder noch.
    „Anna **und** Ben haben gelöst“ stimmt nicht. Dann hat mindestens einer nicht gelöst.
    :::

    [[De Morgan|Regeln von De Morgan]] (Satz 1.14): $\neg(P \lor Q) \Leftrightarrow \neg P \land \neg Q$ und
    $\neg(P \land Q) \Leftrightarrow \neg P \lor \neg Q$. Das Negationszeichen geht nach innen, dabei
    wechseln $\land$ und $\lor$. Der Beweis steht auf der Folie als **Übung**: Er ist eine Wahrheitstabelle.

    """ + _vis(["P", "Q"], ["¬(P ∨ Q)", "¬P ∧ ¬Q", "¬(P ∧ Q)", "¬P ∨ ¬Q"],
               unterschrift="Spalte 1 = Spalte 2 und Spalte 3 = Spalte 4. Damit ist Satz 1.14 bewiesen.") + r"""

    Das waren unsere ersten [[Sätze|Satz]] (1.12 und 1.14). Ein Satz ist eine Aussage, die nachgewiesen ist.
    [[Theorem]]: besonders wichtiger Satz. [[Lemma|Satz]]: Hilfssatz. [[Korollar|Satz]]: unmittelbare Folgerung. Ein [[Beweis]]
    ist ein zweifelsfreier, schriftlicher Nachweis. Eine [[Definition]] legt einen Begriff fest, $:=$ heißt
    „ist definiert als“ ([[definierendes Gleichheitszeichen]]).

    :::rechnung Die mathematische Methode (Folie 17)
    \text{1. Begriffe präzisieren} || durch Definitionen
    \text{2. Voraussetzungen offenlegen} || im Satz: Was wird angenommen?
    \text{3. Schlussfolgerungen begründen} || im Beweis: jeder Schritt mit Grund
    :::

    :::alt Mit einem Gerichtsurteil erklärt
    Ein Beweis ist wie eine Urteilsbegründung: Wer sie liest, soll keinen Ansatzpunkt für Widerspruch
    finden. Dafür müssen alle dieselben Wörter gleich benutzen. Das leisten die Definitionen.
    :::
    """)

k.mc("Pingo-Frage: Wie lautet die Verneinung von „Anna und Ben haben die Aufgabe gelöst“?",
     ["Mindestens einer von beiden hat die Aufgabe nicht gelöst.",
      "Weder Anna noch Ben haben die Aufgabe gelöst.",
      "Anna hat die Aufgabe nicht gelöst.",
      "Anna und Ben haben die Aufgabe beide nicht gelöst."],
     "$P$: Anna hat gelöst, $Q$: Ben hat gelöst. $\\neg(P \\land Q) \\Leftrightarrow \\neg P \\lor \\neg Q$: Anna hat nicht gelöst **oder** Ben hat nicht gelöst, "
     "also mindestens einer.",
     tipps=["De Morgan: Aus $\\land$ wird beim Verneinen $\\lor$.", "„Nicht beide“ ist etwas anderes als „keiner von beiden“."],
     fehler={"Weder Anna noch Ben haben die Aufgabe gelöst.": "Das wäre $\\neg P \\land \\neg Q$, also $\\neg(P \\lor Q)$. Du hast „und“ beim Verneinen nicht in „oder“ getauscht.",
             "Anna und Ben haben die Aufgabe beide nicht gelöst.": "Auch das ist $\\neg P \\land \\neg Q$. Es reicht, wenn einer von beiden nicht gelöst hat.",
             "Anna hat die Aufgabe nicht gelöst.": "Das ist nur ein möglicher Fall. Auch wenn nur Ben nicht gelöst hat, stimmt die Aussage nicht."})


# ═══ Seite 7: Implikation beweisen, Schlussregeln (Folien 18 und 19) ═══════════════════════════════
k.erklaerung("Implikationen beweisen und Schlussregeln", r"""
    ## Was darf ich annehmen? Wo will ich hin?

    :::analogie 🧭 Start und Ziel
    Ein Beweis ist eine Wegbeschreibung. Start: das, was gegeben ist. Ziel: das, was gezeigt werden soll.
    Jeder Schritt dazwischen braucht einen Grund, sonst fehlt ein Wegstück.
    :::

    Fast jeder Satz hat die Form $P \Rightarrow Q$. $P$ ist die **Voraussetzung**, $Q$ die **Behauptung**. Ist $P$
    falsch, ist die Implikation schon wahr. Deshalb nehmen wir **an, dass $P$ gilt**, und zeigen unter dieser
    Annahme, dass $Q$ gilt. Eine Äquivalenz $P \Leftrightarrow Q$ zeigt man in beiden Richtungen:
    $P \Rightarrow Q$ und $Q \Rightarrow P$. Erlaubte Schritte sind die logischen [[Schlussregeln|Schlussregel]]:

    :::rechnung Die sechs Schlussregeln (Folie 19)
    P,\ (P \Rightarrow Q) \ \text{ergibt}\ Q || Modus ponens: Implikation nutzen
    (P \Rightarrow Q),\ \neg Q \ \text{ergibt}\ \neg P || Modus tollens: Kontraposition nutzen
    (P \lor Q),\ \neg P \ \text{ergibt}\ Q || Elimination: einen Fall ausschließen
    P,\ Q \ \text{ergibt}\ (P \land Q) || Und bilden
    (P \land Q) \ \text{ergibt}\ P \ \text{und}\ Q || Und zerlegen
    P \ \text{ergibt}\ (P \lor Q) || Oder bilden, für beliebiges Q
    :::

    Beispiel der Folie: „Lea liest. Also liest oder schreibt Lea.“ (Oder bilden, $Q$: „Lea schreibt“). Ihre Namen
    sind nicht wichtig. Die Gültigkeit lässt sich an den Wahrheitstabellen nachvollziehen.

    :::alt Mit einem Rezept erklärt
    Schlussregeln sind die erlaubten Handgriffe beim Kochen eines Beweises. „Und zerlegen“ heißt: Aus
    „Anna hat Hunger und Zeit“ darfst du „Anna hat Zeit“ entnehmen. „Elimination“: Aus „Tee oder Kaffee“ und
    „kein Tee“ bleibt Kaffee. Hast du nur diese Handgriffe, kann niemand dein Ergebnis anzweifeln.
    :::
    """)

k.mc("Welche Schlussregel steckt in: „Es regnet oder es schneit. Es regnet nicht. Also schneit es.“?",
     ["Elimination", "Modus ponens", "Modus tollens", "Und zerlegen"],
     "Aus $P \\lor Q$ und $\\neg P$ folgt $Q$: Ein Fall wird ausgeschlossen (Elimination).",
     tipps=["Welche der beiden Möglichkeiten wird ausgeschlossen?", "Was bleibt dann übrig?"],
     fehler={"Modus ponens": "Dafür brauchst du eine Implikation $P \\Rightarrow Q$ und $P$. Hier steht ein „oder“.",
             "Modus tollens": "Dafür brauchst du eine Implikation und ein verneintes Ende $\\neg Q$. Hier steht ein „oder“."})


# ═══ Seite 8: gerade/ungerade, direkter Beweis (Definition 1.15, Satz 1.16, Folien 20 und 21) ══════
k.erklaerung("Gerade und ungerade, der direkte Beweis", r"""
    ## Das Werkzeug für alle Beweise heute

    :::analogie 🧱 Zweierpäckchen
    Gerade Zahlen lassen sich in Zweierpäckchen aufteilen, ohne dass etwas übrig bleibt: 6 ist 3 Päckchen.
    Ungerade Zahlen lassen genau einen Rest: 7 ist 3 Päckchen und 1.
    :::

    Definition 1.15: Eine Zahl $n$ heißt **gerade**, wenn $n = 2a$ für ein ganzes $a$, und **ungerade**, wenn
    $n = 2a + 1$ für ein ganzes $a$. Jede ganze Zahl ist [[gerade|gerade Zahl]] oder ungerade, aber nicht beides. Das $a$ ist
    ein Platzhalter für „irgendeine ganze Zahl“. Satz 1.16: Sind $n, m$ gerade, so ist $n + m$ gerade.
    Beweis: [[direkt|direkter Beweis]]. Muster: Voraussetzung annehmen, Behauptung herleiten. Hier geht das,
    weil aus „$n$ gerade“ sofort $n = 2b$ abzulesen ist.

    :::rechnung Satz 1.16, Zeile für Zeile (Folie 21)
    \text{Annahme (1): } n \text{ und } m \text{ sind gerade.} || die Voraussetzung wird angenommen
    \text{(2) Also } n = 2b \text{ und } m = 2c \text{ mit ganzen } b, c. || Definition 1.15
    2b + 2c = 2(b + c) || (3): 2 ausklammern, daher n + m = 2(b + c)
    \text{(4) } b + c \text{ ist ganz.} || Summe ganzer Zahlen
    \text{(5) } n + m = 2 \cdot (\text{ganze Zahl}) \text{ ist gerade.} || (3) und (4), Definition 1.15: Behauptung gezeigt \ \square
    :::

    :::achtung Ein Beispiel ist kein Beweis
    $4 + 6 = 10$ zeigt nur, dass der Satz für dieses Paar stimmt. Ein Beweis rechnet mit $b$ und $c$ statt
    mit konkreten Zahlen, damit er für **jedes** Paar gilt.
    :::

    :::alt Mit konkreten Zahlen vorab
    Probiere 4 + 6 = 10: gerade. Das ist aber **kein** Beweis, nur ein Test. Der Beweis arbeitet mit b und c
    statt mit 2 und 3, damit er für jedes Paar gilt. Beim Ausklammern passiert dasselbe wie bei 2·2 + 2·3 =
    2·(2 + 3) = 10.
    :::
    """)

k.ordnen("Bringe den Beweis von Satz 1.16 in die richtige Reihenfolge. Satz: Sind $n, m$ gerade, so ist $n + m$ gerade.",
         ["Seien $n$ und $m$ gerade Zahlen (Voraussetzung angenommen).",
          "Nach Definition 1.15 gibt es ganze Zahlen $b, c$ mit $n = 2b$ und $m = 2c$.",
          "Dann gilt $n + m = 2b + 2c = 2(b + c)$.",
          "Die Zahl $b + c$ ist ganz.",
          "Also ist $n + m$ gerade. $\\square$"],
         "Muster des direkten Beweises: Voraussetzung annehmen, Definition anwenden, umformen, die Definition der Behauptung wiedererkennen.",
         ablenker=["Probe: $4 + 6 = 10$ ist gerade, also stimmt der Satz.",
                   "Sei $n = 2b$ und $m = 2b$ mit derselben ganzen Zahl $b$."],
         tipps=["Zuerst wird gesagt, was angenommen wird.", "Zwei verschiedene gerade Zahlen brauchen zwei verschiedene Hilfszahlen.",
                "Ein Beispiel ist kein Beweis."])


# ═══ Seite 9: Äquivalenzumformung, Kontraposition (Satz 1.12 nochmal, Satz 1.17, Folien 22 und 23) ═
k.erklaerung("Äquivalenzumformung und Kontraposition", r"""
    ## Zwei Wege zum Gleichen

    :::analogie ⛓️ Kette ohne Sprung
    Bei einer Gleichungsumformung darf jeder Schritt rückwärts gelesen werden. So ist es auch bei
    Aussagen: Jedes Glied der Kette sagt **genau dasselbe** wie das vorige.
    :::

    [[Äquivalenzumformung]]: Beweis von Satz 1.12 durch eine Kette von $\Leftrightarrow$. Jede Umformung gilt in
    beiden Richtungen. Beweis durch [[Kontraposition]]: Statt $P \Rightarrow Q$ beweist du $\neg Q \Rightarrow \neg P$. Muster:
    $\neg Q$ annehmen und $\neg P$ herleiten. Satz 1.17: Ist $n^2$ gerade, so ist $n$ gerade. Direkt ist
    das schwer: Aus $n^2 = 2k$ liest du $n$ nicht ab. Also nimm an, $n$ sei **ungerade**, und zeige: dann ist $n^2$ ungerade.

    :::rechnung Satz 1.12 durch Äquivalenzumformung (Folie 22)
    (P \Rightarrow Q) \Leftrightarrow (\neg P \lor Q) || „wenn P, dann Q“ ist „nicht P oder Q“ (Tabelle von Folie 22)
    \Leftrightarrow (Q \lor \neg P) || Vertauschen bei „oder“
    \Leftrightarrow (\neg(\neg Q) \lor \neg P) || doppelte Verneinung
    \Leftrightarrow (\neg Q \Rightarrow \neg P) || wieder: „wenn A, dann B“ ist „nicht A oder B“
    :::

    :::rechnung Satz 1.17 durch Kontraposition (Folie 23)
    \text{Sei } n \text{ ungerade, also } n = 2a + 1. || Annahme: ¬Q (Behauptung falsch)
    \text{Quadrieren: } n^2 = (2a + 1)^2 || Quadrat bilden
    (2a + 1)^2 = 4a^2 + 4a + 1 || binomische Formel
    4a^2 + 4a + 1 = 2(2a^2 + 2a) + 1 || 2 aus den ersten beiden Termen ausklammern
    \text{Also ist } n^2 \text{ ungerade.} || Definition 1.15 mit der ganzen Zahl 2a² + 2a: ¬P gezeigt \ \square
    :::

    :::alt Mit der Anna-Idee erklärt
    Wie bei „heißt in Darmstadt niemand Anna, dann auch niemand im Saal“: Statt von hinten nach vorn zu
    zweifeln, gehst du vom verneinten Ende aus zum verneinten Anfang. Bei „n² gerade, dann n gerade“
    startest du bei „n nicht gerade“ und endest bei „n² nicht gerade“. Der Weg ist leichter.
    :::
    """)

k.luecke("Beweis von Satz 1.17 durch Kontraposition. Sei $n = 2a + 1$ ungerade. Ergänze die Lücke.",
         r"n^2 = (2a + 1)^2 = 4a^2 + 4a + 1 = 2\left(\luecke\right) + 1", [["2a^2 + 2a"]],
         "$4a^2 + 4a = 2 \\cdot (2a^2 + 2a)$. Weil $2a^2 + 2a$ ganz ist, hat $n^2$ die Form $2b + 1$ und ist ungerade. "
         "Das ist die Kontraposition: $n$ ungerade ergibt $n^2$ ungerade, also folgt aus $n^2$ gerade, dass $n$ gerade ist.",
         tipps=["Klammere aus $4a^2 + 4a$ eine $2$ aus.", "$4a^2 = 2 \\cdot 2a^2$ und $4a = 2 \\cdot 2a$.", "$2a^2 + 2a$"],
         rechenweg=r"""
         :::rechnung
         4a^2 + 4a = 2 \cdot 2a^2 + 2 \cdot 2a || beide Summanden enthalten eine 2
         = 2(2a^2 + 2a) || ausklammern
         :::
         """,
         typische_fehler=[(["a^2 + a"], "Hier hast du $4a^2 + 4a = 2(a^2 + a)$ gerechnet. Das stimmt nicht: $2(a^2 + a) = 2a^2 + 2a$."),
                          (["4a^2 + 4a"], "Du hast nicht ausgeklammert. In der Klammer soll das stehen, was nach dem Ausklammern der $2$ übrig bleibt.")])

k.zuordnen("Welche Annahme macht welche Beweisform? Ordne zu (Muster der Folien).",
           [("Direkter Beweis (Satz 1.16)", "$P$ annehmen, $Q$ herleiten"),
            ("Kontraposition (Satz 1.17)", "$\\neg Q$ annehmen, $\\neg P$ herleiten"),
            ("Widerspruch (Satz 1.17 nochmal)", "$P$ und $\\neg Q$ annehmen, $C \\land \\neg C$ herleiten"),
            ("Äquivalenzumformung (Satz 1.12)", "Kette von $\\Leftrightarrow$, jeder Schritt in beide Richtungen")],
           "Direkt: Voraussetzung rein, Behauptung raus. Kontraposition: vom verneinten Ende zum verneinten Anfang. Widerspruch: das Schlimmste annehmen "
           "(Voraussetzung gilt, Behauptung nicht) und etwas Unmögliches finden. Umformung: lauter Äquivalenzen.",
           tipps=["Was nimmt man jeweils zu Beginn des Beweises an?"])


# ═══ Seite 10: Widerspruch und √2 (Satz 1.17 nochmal, Satz 1.18, Folien 24 und 25) ════════════════
k.erklaerung("Widerspruch und die Wurzel aus 2", r"""
    ## Der Detektiv

    :::analogie 🕵️ Alibi
    „Angenommen, er war am Tatort. Dann hätte er gleichzeitig in Berlin und in München sein müssen. Das ist
    unmöglich. Also war er nicht am Tatort.“ Eine Annahme, die zu Unsinn führt, kann nicht stimmen.
    :::

    [[Widerspruch|Widerspruchsbeweis]]: Du nimmst an, die Implikation $P \Rightarrow Q$ sei falsch, also $P \land \neg Q$ (das ist die einzige
    falsche Zeile). Daraus leitest du einen Widerspruch $C \land \neg C$ her, eine Aussage, die nicht stimmen kann.
    Schwierig ist dabei, dass du vorher oft nicht weißt, welches $C$ den Widerspruch liefert. Dieselbe
    Behauptung wie vorher, Satz 1.17, geht so: Nimm $n^2$ gerade **und** $n$ ungerade an. Dann ist
    $n^2$ ungerade, das widerspricht „$n^2$ ist gerade“.

    :::rechnung Satz 1.18: Die Zahl √2 ist kein Bruch (Folie 25, Voraussetzung P ist wahr)
    \text{Annahme: } \sqrt{2} = \tfrac{n}{m} \text{, vollständig gekürzt.} || Gegenteil der Behauptung
    n^2 = 2m^2 \quad \text{(1)} || Quadrieren und mit m² multiplizieren
    \text{(1) zeigt: } n^2 \text{ gerade, mit Satz 1.17: } n \text{ gerade.} || also n = 2a
    \text{Einsetzen in (1): } 2m^2 = (2a)^2 = 4a^2 || n = 2a
    m^2 = 2a^2 \quad \text{(2)} || durch 2 geteilt
    \text{Also } m^2 \text{ gerade, mit Satz 1.17: } m \text{ gerade.} || zweites Mal Satz 1.17
    \text{n und m beide durch 2 teilbar: der Bruch ließe sich kürzen.} || Widerspruch C ∧ ¬C mit C: n/m ist vollständig gekürzt \ \square
    :::

    :::alt Warum „vollständig gekürzt“?
    Ohne diese Annahme gäbe es keinen Widerspruch: 6/4 ist auch „ein Bruch“ und hat gerade Zahlen oben und
    unten. Jeder Bruch lässt sich aber so weit kürzen, bis Zähler und Nenner keinen gemeinsamen Teiler mehr
    haben. Genau das wird am Ende verletzt: Beide wären durch 2 teilbar. C ist „der Bruch ist vollständig
    gekürzt“, und wir haben C und ¬C gezeigt.
    :::
    """)

# ═══ Seite 10: Fallunterscheidung (Satz 1.19 und 1.20, Folien 26 bis 28) ═
k.erklaerung("Fallunterscheidung", r"""
    ## Alle Fälle durchgehen

    :::analogie ☂️ Schirm immer dabei
    „Egal ob es regnet oder die Sonne scheint, ich nehme den Schirm mit.“ Der Schirm hilft gegen Regen **und**
    gegen Sonne. Mit zwei Begründungen deckst du beide Wetterlagen ab.
    :::

    Satz 1.19: $\bigl((P \Rightarrow R) \land (Q \Rightarrow R)\bigr) \Rightarrow \bigl((P \lor Q) \Rightarrow R\bigr)$.
    Bei der [[Fallunterscheidung]] genügen für $(P \lor Q) \Rightarrow R$ zwei Beweise: $P \Rightarrow R$ (Fall 1) und $Q \Rightarrow R$ (Fall 2).
    Die Fälle müssen **alle Möglichkeiten abdecken**, sie dürfen sich überschneiden. Satz 1.20: Ist $n$ ganz,
    so ist $n(n + 1)$ gerade. $P$: $n$ ganz, $A$: gerade, $B$: ungerade, $Q$: $n(n+1)$ gerade.

    :::rechnung Beweis von Satz 1.19 durch Widerspruch (Folie 26)
    \text{Annahme: } P \Rightarrow R \text{ und } Q \Rightarrow R \text{ gelten, aber } (P \lor Q) \Rightarrow R \text{ nicht.} || Gegenteil der Behauptung
    \text{Dann gelten } P \lor Q \text{ und } \neg R. || die einzige falsche Zeile einer Implikation
    \text{Aus } P \Rightarrow R \text{ und } \neg R \text{ folgt } \neg P. || Kontraposition (Modus tollens)
    \text{Aus } P \lor Q \text{ und } \neg P \text{ folgt } Q. || Elimination
    \text{Aus } Q \text{ und } Q \Rightarrow R \text{ folgt } R. || Modus ponens, das widerspricht \neg R \ \square
    :::

    :::rechnung Satz 1.20 (Folie 28): n(n+1) ist gerade
    \text{Jede ganze Zahl ist gerade oder ungerade.} || die zwei Fälle decken alles ab (Definition 1.15)
    \text{Fall 1: } n = 2a. || n gerade
    \text{Dann ist } n(n + 1) = 2a(2a + 1) \text{ und} || n durch 2a ersetzt
    2a(2a + 1) = 2(2a^2 + a) || 2 ausklammern, in der Klammer steht eine ganze Zahl: gerade
    \text{Fall 2: } n = 2a + 1. || n ungerade
    \text{Dann ist } n(n + 1) = (2a + 1)(2a + 2) \text{ und} || n durch 2a + 1 ersetzt
    (2a + 1)(2a + 2) = 2(2a^2 + 3a + 1) || 2 ausklammern, in der Klammer steht eine ganze Zahl: gerade
    \text{In beiden Fällen ist } n(n + 1) \text{ gerade.} || Behauptung gezeigt \ \square
    :::

    :::alt Zwei Nachbarn
    Von zwei Zahlen, die nebeneinander stehen (wie 7 und 8), ist immer eine gerade. Ist ein Faktor gerade,
    ist das ganze Produkt gerade. Fall 1: n ist schon gerade. Fall 2: n ist ungerade, dann ist der Nachbar
    n + 1 gerade. Probe: 3·4 = 12, 5·6 = 30, 7·8 = 56.
    :::
    """)

k.mc("Du willst $(P \\lor Q) \\Rightarrow R$ durch Fallunterscheidung zeigen. Was **musst** du dafür beweisen?",
     ["$P \\Rightarrow R$ und $Q \\Rightarrow R$, und die Fälle $P$ und $Q$ decken alle Möglichkeiten ab.",
      "Nur $P \\Rightarrow R$, der andere Fall ist ähnlich.",
      "$R \\Rightarrow P$ und $R \\Rightarrow Q$.",
      "$P \\Rightarrow R$ und $Q \\Rightarrow R$, die Fälle dürfen sich dabei nicht überschneiden."],
     "Satz 1.19: Aus $P \\Rightarrow R$ und $Q \\Rightarrow R$ folgt $(P \\lor Q) \\Rightarrow R$. Die Fälle müssen alles abdecken, "
     "dürfen sich aber überschneiden (z. B. bei $n \\ge 0$ und $n \\le 0$ liegt die $0$ in beiden).",
     tipps=["Wie viele Beweise braucht man bei zwei Fällen?", "Eine Überschneidung ist erlaubt, ein fehlender Fall nicht."],
     fehler={"Nur $P \\Rightarrow R$, der andere Fall ist ähnlich.": "Jeder Fall braucht seinen eigenen Beweis. „Ähnlich“ ist keine Begründung.",
             "$P \\Rightarrow R$ und $Q \\Rightarrow R$, die Fälle dürfen sich dabei nicht überschneiden.": "Überschneiden dürfen sie sich. Nur eine Lücke ist verboten.",
             "$R \\Rightarrow P$ und $R \\Rightarrow Q$.": "Die Pfeile laufen falsch herum. $R$ soll am Ende folgen."})


# ═══ Praxis ════════════════════════════════════════════════════════════════════════════════════════
def _formel_tex(f):
    return (f.replace("¬", "\\neg ").replace("∧", "\\land").replace("∨", "\\lor").replace("⇒", "\\Rightarrow")
            .replace("⇔", "\\Leftrightarrow").replace("⊕", "\\oplus"))


_SPALTEN = [
    ("P ⇒ Q", [("Q ⇒ P", "Das ist die Umkehrung, die Richtung ist vertauscht."), ("P ∧ Q", "„Wenn-dann“ ist nicht „und“: Bei falschem $P$ ist die Implikation wahr."),
               ("¬P ∧ Q", "Das ist keine Implikation, die Zeile mit $P$ falsch ist dort nur teilweise wahr.")]),
    ("¬Q ⇒ ¬P", [("¬P ⇒ ¬Q", "Das ist die Umkehrung in verneinter Form, nicht die Kontraposition."), ("Q ⇒ P", "Hier wurde nur umgedreht, nicht verneint."),
                 ("¬P ∧ ¬Q", "Das ist keine Implikation.")]),
    ("P ⇔ Q", [("P ⇒ Q", "Eine Äquivalenz braucht beide Richtungen."), ("P ⊕ Q", "Das ist das Gegenteil: XOR ist falsch, wenn beide gleich sind."),
               ("P ∧ Q", "Bei beiden falsch ist $P \\Leftrightarrow Q$ wahr, $P \\land Q$ aber falsch.")]),
    ("¬(P ∧ Q)", [("¬P ∧ ¬Q", "Bei De Morgan wechselt $\\land$ zu $\\lor$."), ("P ∧ Q", "Die Negation fehlt."), ("¬P ∧ Q", "Die Negation gilt für die ganze Klammer.")]),
    ("¬(P ∨ Q)", [("¬P ∨ ¬Q", "Bei De Morgan wechselt $\\lor$ zu $\\land$."), ("P ∨ Q", "Die Negation fehlt."), ("¬P ∨ Q", "Die Negation gilt für die ganze Klammer.")]),
    ("P ⊕ Q", [("P ∨ Q", "Bei wahr/wahr ist $\\lor$ wahr, $\\oplus$ aber falsch."), ("P ⇔ Q", "Das ist das Gegenteil von XOR."), ("P ∧ Q", "Das ist $P \\land Q$, nicht „genau eine“.")]),
    ("P ∧ ¬Q", [("¬P ∨ Q", "Das ist genau die Negation davon."), ("P ∨ ¬Q", "Hier steht $\\lor$ statt $\\land$."), ("¬P ∧ Q", "Beide Teile verneint statt nur $Q$.")]),
    ("¬P ∨ Q", [("P ∨ ¬Q", "Die Negation steht am falschen Teil."), ("¬P ∧ Q", "Hier steht $\\land$ statt $\\lor$."), ("P ∧ ¬Q", "Das ist die Negation von $\\neg P \\lor Q$.")]),
]


def _tausch(text):
    """Vertauscht die Variablen P und Q in einem Text (Formel oder Meldung)."""
    return re.sub(r"(?<![A-Za-zäöüÄÖÜß])[PQ](?![A-Za-zäöüÄÖÜß])", lambda m: "Q" if m.group(0) == "P" else "P", text)


def wahrheitstabelle_spalte(rng):
    formel, varianten = rng.choice(_SPALTEN)
    if rng.random() < 0.5:
        formel = _tausch(formel)
        varianten = [(_tausch(v), _tausch(m)) for v, m in varianten]
    soll = _wf(_spalte(formel))
    optionen, fehler = [soll], {}
    for v, meldung in varianten:
        o = _wf(_spalte(v))
        if o not in optionen:
            optionen.append(o)
            fehler[o] = meldung
    alle = [", ".join(z) for z in itertools.product("wf", repeat=4)]
    rng.shuffle(alle)
    for o in alle:
        if len(optionen) >= 4:
            break
        if o not in optionen:
            optionen.append(o)
    tex = _formel_tex(formel)
    return {
        "typ": "mc",
        "frage": f"Welche Spalte gehört zu ${tex}$? Zeilen wie auf den Folien: ($P$, $Q$) = (w, w), (w, f), (f, w), (f, f).",
        "optionen": optionen,
        "fehler": fehler,
        "tipps": ["Rechne Zeile für Zeile, von innen nach außen.", "Verneine zuerst, was verneint ist.",
                  "$P \\Rightarrow Q$ ist nur in der Zeile (w, f) falsch, $P \\oplus Q$ nur in (w, w) und (f, f)."],
        "rechenweg": _vis(["P", "Q"], [formel], schrittweise=False),
        "erklaerung": f"Die Spalte von ${tex}$ lautet {soll}.",
    }


_AEQUIV = [
    ("¬(P ∧ Q)", "¬P ∨ ¬Q", ["¬P ∧ ¬Q", "P ∨ Q", "¬P ∨ Q"], "De Morgan: „nicht beide“ ist „mindestens eines nicht“."),
    ("¬(P ∨ Q)", "¬P ∧ ¬Q", ["¬P ∨ ¬Q", "P ∧ Q", "¬P ∧ Q"], "De Morgan: „nicht mindestens eines“ ist „keines von beiden“."),
    ("P ⇒ Q", "¬Q ⇒ ¬P", ["¬P ⇒ ¬Q", "Q ⇒ P", "P ∧ ¬Q"], "Kontrapositionsgesetz: verneinen und umdrehen."),
    ("P ⇒ Q", "¬P ∨ Q", ["P ∨ ¬Q", "¬P ∧ Q", "P ∧ Q"], "Die Tabelle von $P \\Rightarrow Q$ stimmt mit $\\neg P \\lor Q$ überein."),
    ("¬(P ⇒ Q)", "P ∧ ¬Q", ["¬P ∧ Q", "¬P ⇒ ¬Q", "P ∨ ¬Q"], "Eine Implikation ist nur bei $P$ wahr und $Q$ falsch falsch."),
    ("¬(¬P ∨ Q)", "P ∧ ¬Q", ["¬P ∧ Q", "P ∨ ¬Q", "¬P ∨ ¬Q"], "De Morgan: $\\neg(\\neg P \\lor Q) \\Leftrightarrow \\neg\\neg P \\land \\neg Q = P \\land \\neg Q$."),
    ("¬(P ∧ ¬Q)", "¬P ∨ Q", ["¬P ∧ Q", "P ∨ ¬Q", "P ∧ Q"], "De Morgan mit doppelter Verneinung: $\\neg(P \\land \\neg Q) \\Leftrightarrow \\neg P \\lor Q$."),
    ("P ⊕ Q", "(P ∨ Q) ∧ ¬(P ∧ Q)", ["(P ∨ Q) ∧ (P ∧ Q)", "(P ∧ Q) ∨ ¬(P ∨ Q)", "P ∨ Q"], "XOR: mindestens eine, aber nicht beide."),
]
for _a, _b, _falsche, _m in _AEQUIV:
    assert _gleich(_a, _b), (_a, _b)
    assert all(not _gleich(_a, f) for f in _falsche), (_a, _falsche)


def aequivalente_formel(rng):
    a, b, falsche, grund = rng.choice(_AEQUIV)
    if rng.random() < 0.5:
        a, b, falsche, grund = _tausch(a), _tausch(b), [_tausch(f) for f in falsche], _tausch(grund)
    optionen = [f"${_formel_tex(b)}$"] + [f"${_formel_tex(f)}$" for f in falsche]
    fehler = {f"${_formel_tex(f)}$": "Die Wahrheitstabelle dieser Aussage stimmt in mindestens einer Zeile nicht mit der gesuchten überein."
              for f in falsche}
    return {
        "typ": "mc",
        "frage": f"Welche Aussage ist gleichwertig zu ${_formel_tex(a)}$?",
        "optionen": optionen,
        "fehler": fehler,
        "tipps": ["Stelle beide Wahrheitstabellen auf und vergleiche die Spalten.", "Denk an De Morgan, Kontraposition und $P \\Rightarrow Q$ = $\\neg P \\lor Q$.",
                  "Bei einer Verneinung von $\\land$ oder $\\lor$ tauschen die beiden Zeichen."],
        "rechenweg": _vis(["P", "Q"], [a, b], schrittweise=False),
        "erklaerung": grund,
    }


def gerade_ungerade(rng):
    n = rng.choice([x for x in range(-17, 40) if x != 0])
    a = n // 2
    gerade = n % 2 == 0
    assert (n == 2 * a) if gerade else (n == 2 * a + 1)
    if gerade:
        fehler = [(F(n - 1, 2), "Das wäre die Form $n = 2a + 1$. Hier ist $n$ gerade, also $n = 2a$."),
                  (a + 1, "Probe: $2(a + 1)$ ist um $2$ zu groß. Setze $a$ in $2a$ ein.")]
    else:
        fehler = [(F(n, 2), "Das wäre $n = 2a$ mit einem Bruch $a$. Bei ungeraden Zahlen gehört noch $+1$ dazu."),
                  (a + 1, "Probe: $2(a + 1) + 1$ ist um $2$ zu groß. Setze $a$ in $2a + 1$ ein.")]
    form = "n = 2a" if gerade else "n = 2a + 1"
    return {
        "frage": f"Die Zahl $n = {n}$ ist {'gerade' if gerade else 'ungerade'}. Gib die ganze Zahl $a$ an mit ${form}$ (Definition 1.15).",
        "loesung": a,
        "tipps": ["Welche Form hat $n$: $2a$ oder $2a + 1$?", f"Bei {'$n = 2a$' if gerade else '$n = 2a + 1$'} stellst du nach $a$ um.",
                  f"{'$a = n / 2$' if gerade else '$a = (n - 1) / 2$'}"],
        "rechenweg": (":::rechnung\n" + (f"{n} = 2 \\cdot a || n = 2a\na = {a} || nach a aufgelöst, {n} ist gerade\n" if gerade else
                                          f"{n} = 2a + 1 || n = 2a + 1\n{n - 1} = 2a || minus 1\na = {a} || durch 2\n") + ":::"),
        "erklaerung": f"${n} = 2 \\cdot {a}{'' if gerade else ' + 1'}$ mit $a = {a}$ ganz.",
        "typische_fehler": ohne_gleiche(a, fehler),
    }


k.praxis()

k.generator(wahrheitstabelle_spalte, typ="mc", titel="Wahrheitstabelle: Spalte bestimmen")
k.generator(aequivalente_formel, typ="mc", titel="Gleichwertige Aussage erkennen")
k.generator(gerade_ungerade, typ="zahl", titel="Gerade und ungerade: a bestimmen")

k.luecke("Satz 1.20, Fall 2: Sei $n = 2a + 1$ ungerade. Ergänze, damit man sieht, dass $n(n+1)$ gerade ist.",
         r"n(n + 1) = (2a + 1)(2a + 2) = 2\left(\luecke\right)", [["(2a + 1)(a + 1)", "2a^2 + 3a + 1"]],
         "$2a + 2 = 2(a + 1)$. Damit ist $n(n+1) = 2 \\cdot (2a + 1)(a + 1)$ und $(2a+1)(a+1) = 2a^2 + 3a + 1$ ist eine ganze Zahl. "
         "Also ist $n(n+1)$ gerade.",
         tipps=["Klammere die $2$ aus $2a + 2$ aus.", "Multipliziere aus: $(2a + 1) \\cdot 2(a + 1)$.", "$2a^2 + 3a + 1$"],
         rechenweg=r"""
         :::rechnung
         (2a + 1)(2a + 2) = 4a^2 + 4a + 2a + 2 || ausmultipliziert
         = 4a^2 + 6a + 2 || zusammengefasst
         = 2(2a^2 + 3a + 1) || 2 ausklammern
         :::
         """,
         typische_fehler=[(["2a^2 + 3a"], "Du hast die $+1$ vergessen: $2(2a^2 + 3a + 1) = 4a^2 + 6a + 2$.")])

k.ordnen("Bringe den Widerspruchsbeweis von Satz 1.18 in die richtige Reihenfolge.",
         ["Angenommen, $\\sqrt{2} = \\frac{n}{m}$ mit einem vollständig gekürzten Bruch.",
          "Dann gilt $n^2 = 2m^2$, also ist $n^2$ gerade.",
          "Nach Satz 1.17 ist $n$ gerade, also $n = 2a$ mit einer ganzen Zahl $a$.",
          "Einsetzen ergibt $2m^2 = 4a^2$, also $m^2 = 2a^2$ und $m^2$ ist gerade.",
          "Nach Satz 1.17 ist auch $m$ gerade.",
          "Dann sind $n$ und $m$ durch $2$ teilbar, der Bruch lässt sich kürzen. Das ist ein Widerspruch. $\\square$"],
         "Muster: Das Gegenteil der Behauptung annehmen (hier: vollständig gekürzter Bruch), daraus folgern, bis das Gegenteil der Annahme herauskommt.",
         ablenker=["Probe: $1{,}41^2 = 1{,}9881$ ist fast $2$, also ist $\\sqrt{2}$ ein Bruch.",
                   "Dann ist $n = 2a$, also ist auch $m = 2a$."],
         tipps=["Zuerst steht die Annahme, die später widerlegt wird.", "Satz 1.17 wird zweimal benutzt: erst für $n$, dann für $m$.",
                "Am Ende steht, was dem Anfang widerspricht."])

k.mc("Im Beweis von Satz 1.18 ($\\sqrt{2}$ ist kein Bruch) wird Satz 1.17 benutzt. Wie oft?",
     ["Zweimal: für $n^2 = 2m^2$ (also $n$ gerade) und für $m^2 = 2a^2$ (also $m$ gerade).",
      "Einmal: nur für $n$.",
      "Gar nicht, der Beweis rechnet nur mit Brüchen.",
      "Dreimal: für $n$, $m$ und $a$."],
     "Erst ist $n^2 = 2m^2$ gerade, also $n$ gerade, $n = 2a$. Dann ist $m^2 = 2a^2$ gerade, also $m$ gerade. "
     "Daraus folgt: Beide sind durch $2$ teilbar, der Bruch war nicht vollständig gekürzt.",
     tipps=["Wo steht im Beweis „gerade, also …“?", "Es gibt zwei Quadrate, die als gerade erkannt werden."],
     fehler={"Einmal: nur für $n$.": "Für $n$ allein gäbe es noch keinen Widerspruch. Erst wenn auch $m$ gerade ist, ist der Bruch kürzbar.",
             "Dreimal: für $n$, $m$ und $a$.": "$a$ ist nur der Hilfswert für $n = 2a$. Für $a$ braucht man Satz 1.17 nicht."})

k.papier(r"""
    ## Übungsblatt-Stil: Wahrheitstabelle und Beweis

    1. Zeigen Sie mit einer Wahrheitstabelle: $\neg(P \Rightarrow Q) \Leftrightarrow (P \land \neg Q)$.
    2. Beweisen Sie direkt: Ist $n$ ungerade, so ist $n + 1$ gerade.
    """,
    "**1.** Spalten von innen nach außen:\n\n"
    "| $P$ | $Q$ | $P \\Rightarrow Q$ | $\\neg(P \\Rightarrow Q)$ | $\\neg Q$ | $P \\land \\neg Q$ |\n|---|---|---|---|---|---|\n"
    + "\n".join("| " + " | ".join("w" if z else "f" for z in (p, q, (not p) or q, not ((not p) or q), not q, p and (not q))) + " |"
              for p, q in itertools.product([True, False], repeat=2))
    + "\n\nDie 4. und die 6. Spalte stimmen in jeder Zeile überein ("
    + _wf(_spalte("¬(P ⇒ Q)")) + "). Also gilt die Äquivalenz. $\\square$\n\n"
    + r"""**2.** Direkter Beweis. Sei $n$ ungerade. Nach Definition 1.15 gibt es eine ganze Zahl $a$ mit $n = 2a + 1$.
    Dann ist $n + 1 = 2a + 2 = 2(a + 1)$. Weil $a + 1$ ganz ist, ist $n + 1$ gerade. $\square$""",
    ["Meine Tabelle hat 4 Zeilen in der Reihenfolge (w, w), (w, f), (f, w), (f, f)",
     "Ich habe Hilfsspalten für $P \\Rightarrow Q$ und $\\neg Q$ und alle Werte stimmen",
     "Ich habe erkannt: Beide Spalten sind gleich, also gilt die Äquivalenz",
     "Mein Beweis beginnt mit der Annahme „$n$ ist ungerade“ und der Form $n = 2a + 1$",
     "Ich habe $n + 1 = 2(a + 1)$ gerechnet und begründet, dass $a + 1$ ganz ist"],
    "Eine Wahrheitstabelle ist bei wenigen Aussagen ein vollständiger Beweis, weil alle Fälle geprüft werden.",
    uebungsblatt=True,
    tipps=["Lege Hilfsspalten für die Teilformeln an.", "Nimm bei Teil 2 die Voraussetzung an und forme um, bis die Form $2 \\cdot (\\text{ganze Zahl})$ dasteht."])

k.zusammenfassung(r"""
    ## Das musst du nach Vorlesung 1 können

    - **Aussage** (Def. 1.1): eindeutig wahr oder falsch, auch wenn du den Wert nicht kennst. **Aussageform** (Def. 1.3):
      Ausdruck mit Variablen, wird durch eine Belegung zur Aussage.
    - Wahrheitstabelle, Reihenfolge der Zeilen: (w, w), (w, f), (f, w), (f, f).

    | $P$ | $Q$ | $P \land Q$ | $P \lor Q$ | $P \oplus Q$ | $P \Rightarrow Q$ | $P \Leftrightarrow Q$ |
    |---|---|---|---|---|---|---|
    | w | w | w | w | f | w | w |
    | w | f | f | w | w | f | f |
    | f | w | f | w | w | w | f |
    | f | f | f | f | f | w | w |

    - $P \Rightarrow Q$ ist **nur** falsch, wenn $P$ wahr und $Q$ falsch ist. $\neg(P \Rightarrow Q) \Leftrightarrow P \land \neg Q$.
    - Satz 1.12: $(P \Rightarrow Q) \Leftrightarrow (\neg Q \Rightarrow \neg P)$. Satz 1.14 (De Morgan): $\neg(P \lor Q) \Leftrightarrow \neg P \land \neg Q$, $\neg(P \land Q) \Leftrightarrow \neg P \lor \neg Q$.
    - Gerade: $n = 2a$, ungerade: $n = 2a + 1$, jeweils mit ganzem $a$.

    | Beweisform | Man nimmt an | Man zeigt | Beispiel |
    |---|---|---|---|
    | direkt | $P$ | $Q$ | 1.16 |
    | Äquivalenzumformung | nichts, Kette von $\Leftrightarrow$ | $P \Leftrightarrow Q$ | 1.12 |
    | Kontraposition | $\neg Q$ | $\neg P$ | 1.17 |
    | Widerspruch | $P$ und $\neg Q$ | $C \land \neg C$ | 1.17, 1.18 |
    | Fallunterscheidung | $P \lor Q$, dann je Fall | $R$ in jedem Fall | 1.20 |

    **Querbezüge laut Folie:** Programmierung (Bedingungen und Kontrollfluss), Digitaltechnik (logische Gatter und
    Schaltnetze), AFE (Grenzen von Berechenbarkeit), Algorithmen und Verifikation (Korrektheitsbeweise).
    Vertiefung: Kapitel „Aussagen und logische Verknüpfungen“, „Logisches Schließen und Beweisformen“ und die Vorkurs-Kapitel zu Aussagen und Beweisen.

    !! Ein Beispiel ist kein Beweis. Beweise arbeiten mit $n = 2a$ statt mit $n = 4$.
""")
