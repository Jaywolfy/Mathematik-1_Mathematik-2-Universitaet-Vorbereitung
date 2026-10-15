# -*- coding: utf-8 -*-
"""Vorkurs 1: Mengen – Notation, Teilmenge, Gleichheit, Operationen, Zahlenmengen, Intervalle,
Mächtigkeit, Potenzmenge, kartesisches Produkt (MVK 2026, VL 1)."""
import itertools
import json
from fractions import Fraction as F

from .. import pruefer
from ..engine import neues_kapitel

k = neues_kapitel(
    slug="mengen",
    titel="Mengen",
    beschreibung="Mengen angeben, Teilmenge und Gleichheit, Vereinigung, Schnitt, Differenz, Komplement, "
                 "Intervalle, Potenzmenge und kartesisches Produkt",
    teil="vorkurs",
    quelle="MVK 2026, VL 1",
    icon="🧺")

k.lernziele([
    "Ich kann Mengen aufzählend und mit einer Eigenschaft $\\{x \\in G : \\ldots\\}$ angeben und $\\in$, $\\notin$, $\\emptyset$ benutzen",
    "Ich kann prüfen, ob $A \\subseteq B$ oder $A = B$ gilt, und es begründen",
    "Ich kann Vereinigung, Durchschnitt, Differenzmenge und Komplement bilden, auch für Intervalle",
    "Ich kenne $\\mathbb{N}$, $\\mathbb{N}_0$, $\\mathbb{Z}$, $\\mathbb{Q}$, $\\mathbb{R}$ und lese Intervalle wie $(a, b]$",
    "Ich kann Mächtigkeit, Potenzmenge und kartesisches Produkt bestimmen",
])

k.warum(r"""
Mengen sind die Sprache, in der die ganze Uni-Mathematik geschrieben ist. In der Informatik
begegnen sie dir ständig: Ein **Datentyp** ist eine Menge von erlaubten Werten (`bool` ist
$\{\text{True}, \text{False}\}$). Python hat einen eingebauten Typ `set` mit `|` für die
Vereinigung, `&` für den Durchschnitt und `-` für die Differenz. Eine Datenbank-Abfrage mit
`WHERE` beschreibt eine Menge durch eine Eigenschaft, genau wie $\{x \in G : \ldots\}$.
Und eine Tabelle mit zwei Spalten ist ein kartesisches Produkt.
""")

# ── 1: Was ist eine Menge? ────────────────────────────────────────────────
k.erklaerung("Was ist eine Menge?", r"""
    ## Eine Menge fasst Objekte zusammen

    :::analogie 🧺 Der Einkaufskorb
    In deinem Korb liegen ein Apfel, eine Birne und eine Banane. Der Korb ist die
    Menge, die Früchte sind ihre Elemente. Ob die Banane oben oder unten liegt,
    ist egal.
    :::

    Eine [[Menge]] ist eine Zusammenfassung von unterscheidbaren Objekten zu einem
    Ganzen (so hat es Georg Cantor beschrieben). Die Objekte heißen [[Elemente|Element]].
    Man schreibt sie in geschweifte Klammern:
    $M := \{\text{Apfel}, \text{Birne}, \text{Banane}\}$. Das Zeichen $:=$ heißt
    „ist definiert als“.

    - $x \in M$ heißt: $x$ ist Element von $M$.
    - $x \notin M$ heißt: $x$ ist kein Element von $M$.

    !! Reihenfolge und Doppelnennungen spielen in einer Menge keine Rolle.

    :::rechnung Beispiel vorgerechnet
    \{1, 4, 5, 1, 6, 1\} = \{1, 4, 5, 6\} \text{ (doppelt zählt nur einmal)} || die $1$ ist nur einmal Element
    \{a, b, c\} = \{b, a, c\} \text{ (Reihenfolge egal)} || dieselben Elemente
    4 \in \{1, 4, 5, 6\},\ 2 \notin \{1, 4, 5, 6\} || $4$ steht drin, $2$ nicht
    :::

    :::alt Mit einer Gästeliste erklärt
    Eine Menge ist wie die Gästeliste einer Party. Es zählt nur, **wer** drauf steht.
    Steht Anna zweimal drauf, kommt trotzdem nur eine Anna. Ob Anna oben oder unten
    steht, ändert nichts. Die Frage „Steht Tom auf der Liste?“ hat immer eine klare
    Antwort: ja ($\in$) oder nein ($\notin$).
    :::
    ---
    ## Mengen durch eine Eigenschaft beschreiben

    Unendliche oder große Mengen kann man nicht aufzählen. Dann beschreibt man sie
    durch eine Eigenschaft $E$ und wählt die Elemente aus einer [[Grundmenge]] $G$:

    $$M := \{x \in G : x \text{ erfüllt } E\}$$

    Gelesen: „die Menge aller $x$ aus $G$, für die $E$ gilt“. Statt des Doppelpunkts
    steht oft ein senkrechter Strich: $\{x \in G \mid \ldots\}$. Beides heißt „sodass“.

    Die Menge ohne jedes Element heißt [[leere Menge]] und hat das Zeichen $\emptyset$.

    :::rechnung Beispiel vorgerechnet
    \{x \in \mathbb{N} : x \text{ gerade und } x < 10\} || Grundmenge $\mathbb{N} = \{1, 2, 3, \ldots\}$
    = \{2, 4, 6, 8\} || nur gerade Zahlen unter $10$; die $0$ ist nicht in $\mathbb{N}$
    \{x \in \mathbb{N} : x < 1\} = \emptyset || keine natürliche Zahl ist kleiner als $1$
    :::

    :::achtung $\emptyset$ ist nicht $\{0\}$
    $\{0\}$ enthält ein Element, die Zahl $0$. $\emptyset$ enthält gar nichts.
    Auch $\{\emptyset\}$ ist nicht leer: Diese Menge enthält ein Element, nämlich die leere Menge.
    :::

    :::alt Wie ein Filter
    Stell dir einen Filter in einem Onlineshop vor: Grundmenge sind alle Schuhe,
    Eigenschaft ist „Größe 42 und rot“. Was übrig bleibt, ist die Menge. Findet der
    Filter nichts, ist das Ergebnis die leere Menge. In SQL steht das so da:
    `SELECT x FROM G WHERE E`.
    :::
    """)

k.wf("Es gilt $\\{3, 1, 2, 2\\} = \\{1, 2, 3\\}$.", True,
     "Richtig. In einer Menge sind Reihenfolge und Doppelnennungen egal. Beide Mengen haben genau die Elemente $1$, $2$, $3$.",
     tipps=["Vergleiche nur, **welche** Elemente vorkommen."])

k.mc("Welche Aussage ist richtig für $M = \\{1, 2, 3\\}$?",
     ["$3 \\in M$", "$\\{3\\} \\in M$", "$0 \\in M$", "$M \\in M$"],
     "$3$ ist eines der Elemente von $M$. $\\{3\\}$ ist dagegen eine **Menge**, die die $3$ enthält. "
     "Sie steht nicht als Element in $M$ (sie ist aber eine Teilmenge, dazu gleich mehr).",
     tipps=["Schau, was genau zwischen den Klammern von $M$ steht.", "Die Elemente sind die Zahlen $1$, $2$ und $3$."],
     fehler={"$\\{3\\} \\in M$": "Verwechslung von Element und Menge: $\\{3\\}$ ist eine Menge mit der $3$ darin. "
                                 "In $M$ stehen nur Zahlen, keine Mengen. Richtig wäre $3 \\in M$ oder $\\{3\\} \\subseteq M$.",
             "$0 \\in M$": "Die $0$ steht nicht in $M$. Prüfe Element für Element."})

k.menge(r"""Gib die Menge $\{x \in \mathbb{N} : x^2 < 20\}$ in aufzählender Form an.
    Trenne die Elemente mit **;**, z. B. $\{1; 2\}$.""",
        "{1; 2; 3; 4}",
        "$1^2 = 1$, $2^2 = 4$, $3^2 = 9$, $4^2 = 16$ sind kleiner als $20$, aber $5^2 = 25$ nicht. "
        "Die $0$ gehört im Vorkurs nicht zu $\\mathbb{N}$.",
        tipps=["Setze $x = 1, 2, 3, \\ldots$ ein und prüfe $x^2 < 20$.",
               "Ab welcher Zahl ist $x^2$ zu groß?", "$4^2 = 16 < 20$, aber $5^2 = 25$."],
        rechenweg=r"""
        :::rechnung
        4^2 = 16 < 20 || $4$ gehört dazu
        5^2 = 25 > 20 || ab $5$ ist $x^2$ zu groß
        :::

        Also ist die Menge $\{1, 2, 3, 4\}$.
        """,
        typische_fehler=[("{0; 1; 2; 3; 4}", "Im Vorkurs ist $\\mathbb{N} = \\{1, 2, 3, \\ldots\\}$ ohne die $0$. "
                                              "Die $0$ steckt erst in $\\mathbb{N}_0$."),
                         ("{1; 2; 3; 4; 5}", "$5^2 = 25$ ist nicht kleiner als $20$.")])

# ── 2: Zahlenmengen und Intervalle ────────────────────────────────────────
k.erklaerung("Zahlenmengen und Intervalle", r"""
    ## Die Zahlenmengen des Vorkurses

    | Zeichen | Menge |
    |---|---|
    | $\mathbb{N} = \{1, 2, 3, \ldots\}$ | natürliche Zahlen |
    | $\mathbb{N}_0 = \{0, 1, 2, 3, \ldots\}$ | natürliche Zahlen mit Null |
    | $\mathbb{Z} = \{\ldots, -2, -1, 0, 1, 2, \ldots\}$ | ganze Zahlen |
    | $\mathbb{Q} = \{\frac{p}{q} : p \in \mathbb{Z} \text{ und } q \in \mathbb{N}\}$ | rationale Zahlen |
    | $\mathbb{R}$ | reelle Zahlen |
    | $\mathbb{R}_{>0} := \{x \in \mathbb{R} : x > 0\}$ | positive reelle Zahlen |
    | $\mathbb{R}_{<0} := \{x \in \mathbb{R} : x < 0\}$ | negative reelle Zahlen |

    Allgemein: $\mathbb{R}_{>0} \subseteq \mathbb{R}$, aber $0 \notin \mathbb{R}_{>0}$.

    :::achtung Ist die 0 eine natürliche Zahl?
    Im Vorkurs nicht: $0 \notin \mathbb{N}$, aber $0 \in \mathbb{N}_0$. Das Skript zu Mathe 1 und 2 zählt sie dazu.
    :::

    ### Intervalle: lückenlose Stücke von $\mathbb{R}$

    Ein [[Intervall]] enthält **alle** reellen Zahlen zwischen $a < b$. Eckige Klammer: Grenze gehört dazu.

    | Intervall | Menge | Name |
    |---|---|---|
    | $[a, b]$ | $\{x \in \mathbb{R} : a \le x \le b\}$ | abgeschlossen |
    | $(a, b)$ | $\{x \in \mathbb{R} : a < x < b\}$ | offen |
    | $(a, b]$ | $\{x \in \mathbb{R} : a < x \le b\}$ | halboffen, mit Endpunkt |
    | $[a, b)$ | $\{x \in \mathbb{R} : a \le x < b\}$ | halboffen, mit Anfangspunkt |

    Statt $(a, b]$ schreibt man auch $]a, b]$. Bei $\infty$ immer rund: $[2, \infty)$.

    :::visual zahlenstrahl
    {"von": -3, "bis": 5, "intervalle": [{"von": -2, "bis": 1, "von_zu": false, "bis_zu": true, "label": "(-2, 1]"}, {"von": 3, "bis": "inf", "von_zu": true, "label": "[3, \\infty)"}],
     "unterschrift": "Voller Punkt: Grenze gehört dazu. Leerer Kreis: Grenze gehört nicht dazu."}
    :::

    :::alt Mit Werkzeugkästen und Altersangaben erklärt
    Die Zahlenmengen sind wie immer größere Werkzeugkästen: $\mathbb{N}$ zum Zählen,
    $\mathbb{Z}$ mit negativen Zahlen, $\mathbb{Q}$ mit Brüchen, $\mathbb{R}$ auch mit
    $\sqrt{2}$ und $\pi$. Ein Intervall ist ein Stück von $\mathbb{R}$:
    „Für Kinder von 6 bis unter 12 Jahren“ ist das Intervall $[6, 12)$: Mit $6$ darfst
    du mitmachen, mit $12$ nicht mehr. Die eckige Klammer umarmt die Grenze und holt
    sie herein. Die runde Klammer ist offen und lässt sie draußen.
    :::
    """)

k.loesungsmenge(r"""Schreibe die Menge $\{x \in \mathbb{R} : -1 < x \le 4\}$ als Intervall.
    Tippe zum Beispiel `[0; 3)`.""",
    "(-1; 4]",
    "Bei $-1$ steht $<$: Die Grenze gehört nicht dazu, also runde Klammer. Bei $4$ steht $\\le$: eckige Klammer.",
    tipps=["Schau dir jede Grenze einzeln an: $<$ oder $\\le$?", "$<$ bedeutet runde Klammer, $\\le$ eckige Klammer.",
           "Links rund, rechts eckig."],
    rechenweg=r"""Links steht $-1 < x$: Die $-1$ gehört nicht dazu, also runde Klammer.
    Rechts steht $x \le 4$: Die $4$ gehört dazu, also eckige Klammer.

    $$\{x \in \mathbb{R} : -1 < x \le 4\} = (-1, 4]$$""",
    typische_fehler=[("[-1; 4]", "Bei $-1$ steht $<$, nicht $\\le$. Die $-1$ gehört also **nicht** dazu: runde Klammer."),
                     ("(-1; 4)", "Bei $4$ steht $\\le$. Die $4$ gehört dazu: eckige Klammer.")])

k.zuordnen("Ordne jeder Menge ihre Bezeichnung zu.",
           [("$[0, 1]$", "abgeschlossenes Intervall"), ("$(0, 1)$", "offenes Intervall"),
            ("$(0, 1]$", "halboffen, Endpunkt gehört dazu"), ("$[0, 1)$", "halboffen, Anfangspunkt gehört dazu"),
            ("$\\{0, 1\\}$", "zwei einzelne Zahlen, kein Intervall")],
           "Eckige Klammer: Grenze gehört dazu. Runde Klammer: Grenze gehört nicht dazu. Geschweifte Klammern "
           "zählen Elemente auf: $\\{0, 1\\}$ enthält nur die zwei Zahlen $0$ und $1$, nichts dazwischen.",
           tipps=["Achte auf die Form der Klammern: eckig, rund oder geschweift."])

# ── 3: Teilmenge und Gleichheit ───────────────────────────────────────────
k.erklaerung("Teilmenge und Mengengleichheit", r"""
    ## $A \subseteq B$: alles aus $A$ liegt auch in $B$

    :::analogie 🎒 Rucksack im Koffer
    Packst du deinen Rucksack komplett in den Koffer, ist alles aus dem Rucksack
    auch im Koffer. Der Rucksackinhalt ist eine Teilmenge des Kofferinhalts.
    :::

    $A$ heißt [[Teilmenge]] von $B$, geschrieben $A \subseteq B$, wenn **jedes** Element
    von $A$ auch Element von $B$ ist. Jede Menge hat sich selbst und die leere Menge als
    Teilmenge: $A \subseteq A$ und $\emptyset \subseteq A$.

    :::visual venn
    {"mengen": [{"name": "A", "elemente": ["r", "g"]}, {"name": "B", "elemente": ["r", "g", "b"]}],
     "markiert": "A",
     "unterschrift": "$\\{r, g\\} \\subseteq \\{r, g, b\\}$: Die Fläche „$A$ ohne $B$“ ist leer."}
    :::

    :::rechnung Beispiele vorgerechnet
    \{r, g\} \subseteq \{r, g, b\} || $r$ und $g$ liegen beide in der rechten Menge
    \mathbb{N} \subseteq \mathbb{Z} || jede natürliche Zahl ist eine ganze Zahl
    (-4, 2) \subseteq \mathbb{R} || ein Intervall besteht aus reellen Zahlen
    :::

    :::achtung $\in$ oder $\subseteq$?
    $\in$ steht zwischen einem **Element** und einer Menge: $2 \in \{1, 2\}$.
    $\subseteq$ steht zwischen zwei **Mengen**: $\{2\} \subseteq \{1, 2\}$.
    $2 \subseteq \{1, 2\}$ ist sinnlos, $\{2\} \in \{1, 2\}$ ist falsch.
    :::

    :::alt Mit einem Typen-Bild erklärt
    Stell dir die Mengen als Datentypen vor. Jeder Wert vom Typ „natürliche Zahl“ ist
    auch ein gültiger Wert vom Typ „ganze Zahl“. Darum $\mathbb{N} \subseteq \mathbb{Z}$.
    Umgekehrt nicht: $-3$ ist eine ganze Zahl, aber keine natürliche.
    :::
    ---
    ## Wann sind zwei Mengen gleich?

    $A = B$ heißt: $A$ und $B$ enthalten **dieselben** Elemente. Das prüft man in zwei Richtungen:

    !! $A = B$ genau dann, wenn $A \subseteq B$ und $B \subseteq A$.

    :::rechnung Beispiel und Gegenbeispiel
    \{3, 4, 5, 6\} = \{x \in \mathbb{N} : 3 \le x \le 6\} || beide Richtungen stimmen
    \{x \in \mathbb{R} : x > 120\} \subseteq [120, \infty) || jedes $x > 120$ ist auch $\ge 120$
    120 \in [120, \infty),\ 120 \notin \{x \in \mathbb{R} : x > 120\} || die andere Richtung scheitert an $120$
    :::

    Also ist $\{x \in \mathbb{R} : x > 120\} \neq [120, \infty)$: Ein einziges Element,
    das nur in einer der Mengen liegt, genügt als Gegenbeispiel.

    :::alt Mit zwei Klassenlisten erklärt
    Zwei Lehrer haben je eine Liste ihrer Klasse. Sind es dieselben Kinder? Du hakst
    jedes Kind der ersten Liste auf der zweiten ab, dann jedes Kind der zweiten auf der
    ersten. Klappt beides, sind die Listen gleich. Fehlt auf einer Seite ein Kind, nicht.
    :::
    """)

k.mc("Welche Schreibweise ist richtig?",
     ["$\\{2\\} \\subseteq \\{1, 2, 3\\}$", "$2 \\subseteq \\{1, 2, 3\\}$", "$\\{2\\} \\in \\{1, 2, 3\\}$",
      "$\\{1, 2, 3\\} \\subseteq \\{2\\}$"],
     "$\\{2\\}$ ist eine Menge, deren einziges Element $2$ in $\\{1, 2, 3\\}$ liegt. Also Teilmenge.",
     tipps=["Links von $\\subseteq$ muss eine Menge stehen.", "Links von $\\in$ muss ein Element stehen."],
     fehler={"$2 \\subseteq \\{1, 2, 3\\}$": "$2$ ist eine Zahl, keine Menge. Für Elemente benutzt man $\\in$: $2 \\in \\{1, 2, 3\\}$.",
             "$\\{2\\} \\in \\{1, 2, 3\\}$": "Die Elemente von $\\{1, 2, 3\\}$ sind Zahlen. Die Menge $\\{2\\}$ ist keins davon.",
             "$\\{1, 2, 3\\} \\subseteq \\{2\\}$": "Die Richtung stimmt nicht: $1$ liegt nicht in $\\{2\\}$."})


def _menge_pingo():
    """Welche Mengen sind gleich M = {x ∈ ℕ : x ungerade und x < 8}? (Python rechnet jede Menge aus.)"""
    M = {x for x in range(1, 100) if x % 2 == 1 and x < 8}
    kandidaten = [
        ("$\\{2n - 1 : n \\in \\mathbb{N},\\ n \\le 4\\}$", {2 * n - 1 for n in range(1, 5)}),
        ("$\\{1, 3, 5, 7\\}$", {1, 3, 5, 7}),
        ("$\\{x \\in \\mathbb{Z} : x \\text{ ungerade und } 0 < x < 8\\}$",
         {x for x in range(-50, 50) if x % 2 == 1 and 0 < x < 8}),
        ("$\\{2n + 1 : n \\in \\mathbb{N},\\ n < 4\\}$", {2 * n + 1 for n in range(1, 4)}),
        ("$\\{x \\in \\mathbb{Z} : x \\text{ ungerade und } x < 8\\}$",
         {x for x in range(-50, 50) if x % 2 == 1 and x < 8}),
        ("$\\{x \\in \\mathbb{N} : x \\text{ ungerade und } x \\le 9\\}$",
         {x for x in range(1, 100) if x % 2 == 1 and x <= 9}),
    ]
    richtig = [t for t, s in kandidaten if s == M]
    falsch = [t for t, s in kandidaten if s != M]
    return richtig, falsch


_r, _f = _menge_pingo()
k.mehrfach("Es sei $M := \\{x \\in \\mathbb{N} : x \\text{ ungerade und } x < 8\\}$. Welche Mengen sind gleich $M$?",
           _r, _f,
           "$M = \\{1, 3, 5, 7\\}$. Schreibe jede Menge aufzählend hin und vergleiche. "
           "$\\{2n + 1 : n \\in \\mathbb{N}, n < 4\\} = \\{3, 5, 7\\}$, weil $n$ erst bei $1$ beginnt. "
           "In $\\mathbb{Z}$ ohne untere Grenze kommen auch $-1, -3, \\ldots$ dazu. Mit $x \\le 9$ ist die $9$ zu viel.",
           tipps=["Schreibe zuerst $M$ aufzählend hin.", "Setze bei $2n + 1$ und $2n - 1$ die Werte $n = 1, 2, 3, \\ldots$ ein.",
                  "Achte bei $\\mathbb{Z}$ auf negative Zahlen."],
           fehler={"$\\{2n + 1 : n \\in \\mathbb{N},\\ n < 4\\}$": "Setze ein: $n = 1, 2, 3$ ergibt $3, 5, 7$. Die $1$ fehlt, "
                                                                   "weil $0 \\notin \\mathbb{N}$.",
                   "$\\{x \\in \\mathbb{Z} : x \\text{ ungerade und } x < 8\\}$": "In $\\mathbb{Z}$ gibt es auch $-1, -3, -5, \\ldots$ "
                                                                                 "Ohne untere Grenze sind die alle dabei."})

# ── 4: Operationen ─────────────────────────────────────────────────────────
k.erklaerung("Vereinigung, Durchschnitt, Differenz, Komplement", r"""
    ## Vereinigung und Durchschnitt

    Seien $A, B$ Mengen einer Grundmenge $G$.

    - [[Vereinigung]]: $A \cup B := \{x \in G : x \in A \text{ oder } x \in B\}$. Alles, was in mindestens einer der Mengen liegt.
    - [[Durchschnitt]]: $A \cap B := \{x \in G : x \in A \text{ und } x \in B\}$. Nur das, was in beiden liegt.

    :::visual venn
    {"mengen": [{"name": "M1", "elemente": ["a", "b", "c", "d"]}, {"name": "M2", "elemente": ["c", "d", "f"]}],
     "markiert": "M1 ∩ M2",
     "unterschrift": "Markiert ist $M_1 \\cap M_2$. Tippe auf die Flächen, um die anderen Teile zu sehen."}
    :::

    :::rechnung Beispiel vorgerechnet
    M_1 \cup M_2 = \{a, b, c, d, f\} || alles aus beiden, $c$ und $d$ nur einmal
    M_1 \cap M_2 = \{c, d\} || nur, was in beiden steht
    :::

    Es gilt $A \cup B = B \cup A$ und $A \cap B = B \cap A$ ([[Kommutativgesetz]]).

    :::alt Mit zwei Freundeskreisen erklärt
    Du lädst die Freunde aus dem Sportverein **und** die aus der Schule ein: Das ist die
    Vereinigung, wer in beiden Gruppen ist, kommt einmal. Fragst du, wer in **beiden**
    Gruppen ist, bekommst du den Durchschnitt.
    :::
    ---
    ## Differenzmenge und Komplement

    - [[Differenzmenge]]: $A \setminus B := \{x \in G : x \in A \text{ und } x \notin B\}$, gelesen „$A$ ohne $B$“.
    - [[Komplement]] von $A$ in $G$: $A^C := \{x \in G : x \notin A\}$ (auch $\overline{A}$). Alles aus $G$, was nicht in $A$ liegt.

    :::visual venn
    {"mengen": [{"name": "A", "elemente": [1, 2, 3, 4]}, {"name": "B", "elemente": [3, 4, 5]}],
     "universum": [1, 2, 3, 4, 5, 6, 7], "universum_name": "G", "markiert": "A \\ B",
     "unterschrift": "Markiert ist $A \\setminus B = \\{1, 2\\}$. Tippe auf die Fläche außerhalb: Das ist $(A \\cup B)^C$."}
    :::

    :::rechnung Beispiel vorgerechnet
    A \setminus B = \{1, 2\} || aus $A$ die Elemente von $B$ streichen
    B \setminus A = \{5\} || andersherum kommt etwas anderes heraus
    A^C = \{5, 6, 7\} \text{ bezüglich } G || alles aus $G$ außer $1, 2, 3, 4$
    :::

    :::achtung Reihenfolge und Grundmenge
    Im Allgemeinen ist $A \setminus B \neq B \setminus A$. Und das Komplement hängt von $G$
    ab: $\{x \in \mathbb{N} : x \ge 5\}^C$ ist in $\mathbb{N}$ gleich $\{1, 2, 3, 4\}$,
    in $\mathbb{Z}$ aber $\{\ldots, -1, 0, 1, 2, 3, 4\}$.
    :::

    :::alt Mit einer Einkaufsliste erklärt
    $A$ ist deine Einkaufsliste, $B$ das, was schon im Kühlschrank ist. $A \setminus B$
    ist, was du wirklich kaufen musst. Das Komplement fragt: Was gibt es im ganzen
    Laden ($G$), das **nicht** auf deiner Liste steht?
    :::
    """)

k.menge(r"""Es seien $M_1 := \{a, b, c, d\}$ und $M_2 := \{c, d, f, g\}$. Gib $M_1 \cup M_2$ an.
    Trenne mit **;**, z. B. $\{a; b\}$.""",
        "{a; b; c; d; f; g}",
        "Die Vereinigung enthält alles, was in $M_1$ **oder** in $M_2$ steht. $c$ und $d$ stehen nur einmal da.",
        tipps=["Vereinigung: alles aus beiden Mengen zusammen.", "Doppelte Elemente schreibst du nur einmal.",
               "$a, b, c, d$ aus $M_1$, dazu $f, g$ aus $M_2$."],
        rechenweg=r"""Alle Elemente von $M_1$: $a, b, c, d$. Aus $M_2$ kommen $f$ und $g$ neu dazu.

        $$M_1 \cup M_2 = \{a, b, c, d, f, g\}$$""",
        typische_fehler=[("{c; d}", "Das ist der Durchschnitt $M_1 \\cap M_2$. Bei $\\cup$ gehört **alles** aus beiden Mengen dazu.")])

k.menge(r"""Es seien $A := \{1, 2, 3, 4, 5\}$ und $B := \{2, 4, 6, 8\}$. Gib $A \setminus B$ an.""",
        "{1; 3; 5}",
        "$A \\setminus B$: Aus $A$ werden alle Elemente gestrichen, die auch in $B$ liegen ($2$ und $4$).",
        tipps=["Starte mit $A$.", "Streiche alles, was auch in $B$ vorkommt.", "In beiden Mengen liegen $2$ und $4$."],
        rechenweg=r"""$A = \{1, 2, 3, 4, 5\}$. Gestrichen werden $2$ und $4$, weil sie in $B$ liegen.

        $$A \setminus B = \{1, 3, 5\}$$""",
        typische_fehler=[("{6; 8}", "Das ist $B \\setminus A$. Bei $A \\setminus B$ startest du mit $A$."),
                         ("{2; 4}", "Das ist $A \\cap B$, also genau das, was gestrichen werden muss.")])

k.menge(r"""Es sei $A := \{x \in \mathbb{N} : x \ge 4\}$. Gib das Komplement $A^C$ bezüglich der Grundmenge $\mathbb{N}$ an.""",
        "{1; 2; 3}",
        "In $\\mathbb{N} = \\{1, 2, 3, \\ldots\\}$ fehlen in $A$ genau $1, 2, 3$.",
        tipps=["Das Komplement enthält alles aus der Grundmenge, was **nicht** in $A$ liegt.",
               "Welche natürlichen Zahlen sind kleiner als $4$?", "Denk daran: $0 \\notin \\mathbb{N}$."],
        rechenweg=r"""$A = \{4, 5, 6, \ldots\}$. In $\mathbb{N} = \{1, 2, 3, \ldots\}$ fehlen davon:

        $$A^C = \{1, 2, 3\}$$""",
        typische_fehler=[("{0; 1; 2; 3}", "Die Grundmenge ist $\\mathbb{N}$, und im Vorkurs gilt $0 \\notin \\mathbb{N}$. "
                                           "Bezüglich $\\mathbb{N}_0$ wäre die $0$ dabei.")])

# ── 5: Intervalle verknüpfen ──────────────────────────────────────────────
k.erklaerung("Mengenoperationen mit Intervallen", r"""
    ## Am Zahlenstrahl ablesen

    Bei Intervallen zeichnest du beide Mengen übereinander auf einen Zahlenstrahl und
    liest das Ergebnis ab. Wichtig sind die Grenzen: Gehört die Zahl dazu oder nicht?

    :::visual zahlenstrahl
    {"von": -3, "bis": 6, "intervalle": [{"von": -2, "bis": 3, "label": "A = (-2, 3)"}, {"von": 1, "bis": 5, "von_zu": true, "label": "B = [1, 5)"}],
     "unterschrift": "$A = (-2, 3)$ und $B = [1, 5)$ überlappen zwischen $1$ und $3$."}
    :::

    :::rechnung Beispiel vorgerechnet
    A \cup B = (-2, 5) || von der kleinsten bis zur größten Grenze, ohne Lücke
    A \cap B = [1, 3) || $1 \in B$ und $1 \in A$; $3 \notin A$
    A \setminus B = (-2, 1) || $1$ wird mit $B$ weggenommen, also runde Klammer
    B \setminus A = [3, 5) || $3 \notin A$, also bleibt $3$ in $B \setminus A$
    :::

    :::achtung Die Grenzen beim Abziehen
    Bei $A \setminus B$ dreht sich die Klammer an der Grenze von $B$ um: Gehört $1$ zu
    $B$, wird $1$ entfernt. Darum $(-2, 1)$ und nicht $(-2, 1]$.
    :::

    :::alt Mit Öffnungszeiten erklärt
    Laden $A$ hat von 8 bis 15 Uhr offen, Laden $B$ von 13 bis 18 Uhr. „Mindestens einer
    hat offen“ ist die Vereinigung: 8 bis 18 Uhr. „Beide haben offen“ ist der
    Durchschnitt: 13 bis 15 Uhr. „Nur $A$ hat offen“ ist $A \setminus B$: 8 bis 13 Uhr.
    :::
    """)

k.loesungsmenge(r"""Es seien $A := [-1, 4)$ und $B := (2, 6]$. Gib $A \cap B$ als Intervall an.""",
                "(2; 4)",
                "Beide Mengen enthalten genau die Zahlen zwischen $2$ und $4$. $2 \\notin B$ und $4 \\notin A$, also offen.",
                tipps=["Zeichne beide Intervalle auf einen Zahlenstrahl.", "Wo überlappen sie?",
                       "Prüfe die Grenzen $2$ und $4$ einzeln: Liegen sie in **beiden** Mengen?"],
                rechenweg=r"""
                :::visual zahlenstrahl
                {"von": -2, "bis": 7, "intervalle": [{"von": -1, "bis": 4, "von_zu": true, "label": "A"}, {"von": 2, "bis": 6, "bis_zu": true, "label": "B"}]}
                :::

                Überlappung von $2$ bis $4$. $2 \notin B$, $4 \notin A$. Also $A \cap B = (2, 4)$.
                """,
                typische_fehler=[("[2; 4]", "Die Grenzen gehören nicht dazu: $2 \\notin B$ und $4 \\notin A$. "
                                            "Für den Durchschnitt muss eine Zahl in **beiden** Mengen liegen."),
                                 ("[-1; 6]", "Das ist die Vereinigung $A \\cup B$. Gefragt ist der Durchschnitt.")])

# ── 6: Mächtigkeit, Potenzmenge, kartesisches Produkt ─────────────────────
_A = ["1", "2", "3"]
_P = [set(c) for r in range(4) for c in itertools.combinations(_A, r)]


def _set_tex(s):
    return "\\emptyset" if not s else "\\{" + ", ".join(sorted(s)) + "\\}"


_P_TEX = ", ".join(_set_tex(s) for s in _P)

k.erklaerung("Mächtigkeit, Potenzmenge und kartesisches Produkt", r"""
    ## Wie viele Elemente? Welche Teilmengen?

    Die [[Mächtigkeit]] $|A|$ einer endlichen Menge ist die Anzahl ihrer Elemente. Es gilt
    $|A| \in \mathbb{N}_0$, denn $|\emptyset| = 0$.

    Die [[Potenzmenge]] $\mathcal{P}(A)$ ist die Menge **aller** Teilmengen von $A$. Ihre
    Elemente sind selbst Mengen.

    :::rechnung Beispiel vorgerechnet
    A = \{1, 2, 5, 9\} \Rightarrow |A| = 4 || vier Elemente
    \mathcal{P}(\{a, b\}) = \{\emptyset, \{a\}, \{b\}, \{a, b\}\} || keins, je eins, beide
    \mathcal{P}(\{1, 2, 3\}) = \{""" + _P_TEX + r"""\} || leere Menge, drei einzelne, drei Paare, ganz $A$
    2^3 = 8 || jedes Element: drin oder nicht drin
    :::

    !! Hat $A$ genau $n$ Elemente, so hat $\mathcal{P}(A)$ genau $2^n$ Elemente.

    :::alt Mit Pizzabelag erklärt
    Du hast drei Beläge: Salami, Pilze, Paprika. Bei jedem Belag entscheidest du: drauf
    oder nicht. Das sind $2 \cdot 2 \cdot 2 = 8$ mögliche Pizzen, von „ohne alles“
    ($\emptyset$) bis „mit allem“. Jede Pizza ist eine Teilmenge der Beläge.
    :::
    ---
    ## Paare bilden: das kartesische Produkt

    Das [[kartesische Produkt|kartesisches Produkt]] von $A$ und $B$ ist die Menge aller [[geordneten Paare|geordnetes Paar]]:

    $$A \times B := \{(a, b) : a \in A \text{ und } b \in B\}$$

    Gelesen: „$A$ kreuz $B$“. Bei einem Paar zählt die Reihenfolge: $(1, a) \neq (a, 1)$.
    Für $A \times A$ schreibt man auch $A^2$, zum Beispiel $\mathbb{R} \times \mathbb{R} = \mathbb{R}^2$
    (die Ebene).

    :::rechnung Beispiel vorgerechnet
    \{1, 2\} \times \{a, b, c\} = \{(1, a), (1, b), (1, c), (2, a), (2, b), (2, c)\} || jedes Element links mit jedem rechts
    |A \times B| = |A| \cdot |B| \text{, hier } 2 \cdot 3 = 6 || darum heißt es Produkt
    :::

    :::alt Mit einer Speisekarte erklärt
    Ein Menü besteht aus einer Vorspeise und einem Hauptgericht. Bei $2$ Vorspeisen und
    $3$ Hauptgerichten gibt es $2 \cdot 3 = 6$ Menüs. Jedes Menü ist ein Paar
    (Vorspeise, Hauptgericht). Eine Tabelle mit den Spalten „Name“ und „Note“ ist genauso
    eine Menge von Paaren.
    :::
    """)

k.zahl("Es sei $A := \\{a, b, c, d\\}$. Wie viele Elemente hat die Potenzmenge $\\mathcal{P}(A)$?", 2 ** 4,
       "Jedes der $4$ Elemente ist in einer Teilmenge drin oder nicht: $2^4 = 16$ Teilmengen. "
       "Dazu gehören auch $\\emptyset$ und $A$ selbst.",
       tipps=["Die Potenzmenge enthält **alle** Teilmengen, auch $\\emptyset$ und $A$.",
              "Für jedes Element gibt es zwei Möglichkeiten: drin oder nicht drin.", "$2 \\cdot 2 \\cdot 2 \\cdot 2$"],
       rechenweg=r"""
       :::rechnung
       |A| = 4 \Rightarrow |\mathcal{P}(A)| = 2^4 || jedes Element: drin oder nicht
       2^4 = 16 || ausrechnen
       :::
       """,
       typische_fehler=[(14, "Du hast $\\emptyset$ und $A$ selbst vergessen. Beide sind Teilmengen von $A$."),
                        (8, "$8 = 2 \\cdot 4$. Richtig ist $2^4$: Für **jedes** Element verdoppelt sich die Anzahl."),
                        (4, "$4$ ist die Mächtigkeit von $A$, nicht die von $\\mathcal{P}(A)$.")])

k.menge(r"""Es seien $A := \{1, 2\}$ und $B := \{x, y\}$. Gib $A \times B$ an.
    Schreibe Paare in runden Klammern, z. B. $\{(1; x); (2; x)\}$.""",
        "{(1; x); (1; y); (2; x); (2; y)}",
        "Jedes Element aus $A$ steht an erster Stelle, jedes aus $B$ an zweiter. Das ergibt $2 \\cdot 2 = 4$ Paare.",
        tipps=["Ein Paar $(a, b)$ hat links ein Element aus $A$, rechts eins aus $B$.",
               "Nimm die $1$ und kombiniere sie mit $x$ und mit $y$. Dann dasselbe mit der $2$.",
               "Es sind $4$ Paare."],
        rechenweg=r"""Mit $1$: $(1, x)$, $(1, y)$. Mit $2$: $(2, x)$, $(2, y)$.

        $$A \times B = \{(1, x), (1, y), (2, x), (2, y)\}$$""",
        typische_fehler=[("{(x; 1); (y; 1); (x; 2); (y; 2)}", "Das ist $B \\times A$. Bei $A \\times B$ steht das Element aus $A$ vorn."),
                         ("{1; 2; x; y}", "Das ist $A \\cup B$. Das kartesische Produkt besteht aus **Paaren**.")])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _liste(s):
    return sorted(s)


def _eingabe(s):
    return "{" + "; ".join(str(x) for x in _liste(s)) + "}" if s else "{}"


def _tex(s):
    return "\\{" + ", ".join(str(x) for x in _liste(s)) + "\\}" if s else "\\emptyset"


_OPS = {
    "A ∪ B": ("A \\cup B", "Vereinigung: alles, was in $A$ **oder** in $B$ liegt.", lambda A, B, G: A | B),
    "A ∩ B": ("A \\cap B", "Durchschnitt: nur, was in $A$ **und** in $B$ liegt.", lambda A, B, G: A & B),
    "A \\ B": ("A \\setminus B", "Differenz: aus $A$ alles streichen, was in $B$ liegt.", lambda A, B, G: A - B),
    "B \\ A": ("B \\setminus A", "Differenz: aus $B$ alles streichen, was in $A$ liegt.", lambda A, B, G: B - A),
    "Komplement A": ("A^C", "Komplement: alles aus $G$, was nicht in $A$ liegt.", lambda A, B, G: G - A),
    "Komplement (A ∪ B)": ("(A \\cup B)^C", "Erst $A \\cup B$ bilden, dann alles aus $G$ nehmen, was nicht darin liegt.",
                           lambda A, B, G: G - (A | B)),
    "A ∩ Komplement B": ("A \\cap B^C", "Elemente von $A$, die nicht in $B$ liegen (das ist dasselbe wie $A \\setminus B$).",
                         lambda A, B, G: A & (G - B)),
}

_VERWECHSLUNG = {
    "A ∪ B": [("A ∩ B", "Das ist der Durchschnitt. Bei $\\cup$ gehört alles aus **beiden** Mengen dazu.")],
    "A ∩ B": [("A ∪ B", "Das ist die Vereinigung. Bei $\\cap$ bleibt nur, was in **beiden** Mengen liegt.")],
    "A \\ B": [("B \\ A", "Das ist $B \\setminus A$. Bei $A \\setminus B$ startest du mit $A$."),
               ("A ∩ B", "Das sind genau die Elemente, die gestrichen werden müssen.")],
    "B \\ A": [("A \\ B", "Das ist $A \\setminus B$. Bei $B \\setminus A$ startest du mit $B$."),
               ("A ∩ B", "Das sind genau die Elemente, die gestrichen werden müssen.")],
    "Komplement A": [("A ∪ B", "Das Komplement von $A$ enthält, was **nicht** in $A$ liegt."),
                     ("B \\ A", "Das Komplement bezieht sich auf die ganze Grundmenge $G$, nicht nur auf $B$.")],
    "Komplement (A ∪ B)": [("A ∪ B", "Das ist $A \\cup B$ selbst. Das Komplement ist der Rest von $G$."),
                           ("Komplement A", "Du hast nur $A$ herausgenommen. Auch die Elemente von $B$ müssen weg.")],
    "A ∩ Komplement B": [("A ∩ B", "Du hast das Komplement von $B$ vergessen."),
                         ("Komplement B", "Du hast nur $B^C$ gebildet. Es müssen auch noch Elemente in $A$ sein.")],
}


def mengen_operation(rng):
    G = set(range(1, 11))
    while True:
        A = set(rng.sample(sorted(G), rng.randint(3, 6)))
        B = set(rng.sample(sorted(G), rng.randint(3, 6)))
        if A & B and A - B and B - A and G - (A | B):
            break
    name = rng.choice(sorted(_OPS))
    tex, regel, fn = _OPS[name]
    erg = fn(A, B, G)
    fehler, gesehen = [], [erg]
    for andere, meldung in _VERWECHSLUNG[name]:
        if andere == "Komplement B":
            w = G - B
        else:
            w = _OPS[andere][2](A, B, G)
        if w not in gesehen:
            gesehen.append(w)
            fehler.append((_eingabe(w), meldung))
    markiert = {"Komplement A": "Komplement A", "Komplement (A ∪ B)": "Komplement (A ∪ B)",
                "A ∩ Komplement B": "A ∩ Komplement B"}.get(name, name)
    venn = {"mengen": [{"name": "A", "elemente": _liste(A)}, {"name": "B", "elemente": _liste(B)}],
            "universum": _liste(G), "universum_name": "G", "markiert": markiert}
    return {
        "frage": f"Es sei $G := \\{{1, 2, \\ldots, 10\\}}$ mit $A := {_tex(A)}$ und $B := {_tex(B)}$. "
                 f"Gib ${tex}$ an (Elemente mit **;** trennen, leere Menge als {{}}).",
        "loesung": _eingabe(erg),
        "tipps": [regel, "Gehe die Zahlen $1$ bis $10$ einzeln durch und prüfe, ob sie dazugehören.",
                  f"Es sind {len(erg)} Elemente." if erg else "Es bleibt kein Element übrig."],
        "rechenweg": f"{regel}\n\n:::visual venn\n{json.dumps(venn, ensure_ascii=False)}\n:::\n\n"
                     f"$${tex} = {_tex(erg)}$$",
        "erklaerung": regel,
        "typische_fehler": fehler,
    }


# Intervall-Operationen: Python bestimmt das Ergebnis exakt über Stichpunkte k/2.
# Bei ganzzahligen Grenzen ist die Zugehörigkeit auf jedem offenen Stück (k, k+1) konstant.
def _iv_enthaelt(iv, x):
    a, b, a_zu, b_zu = iv
    return (a < x or (a_zu and x == a)) and (x < b or (b_zu and x == b))


def _iv_tex(iv):
    a, b, a_zu, b_zu = iv
    return ("[" if a_zu else "(") + f"{a}, {b}" + ("]" if b_zu else ")")


def _bereich_aus(drin):
    """drin: Funktion x -> bool. Ergebnis (eingabe, tex, stuecke) für Stichpunkte -8 … 8."""
    punkte = [F(k, 2) for k in range(-16, 17)]
    laeufe, aktuell = [], []
    for p in punkte:
        if drin(p):
            aktuell.append(p)
        elif aktuell:
            laeufe.append(aktuell)
            aktuell = []
    if aktuell:
        laeufe.append(aktuell)
    teile_e, teile_t, stuecke = [], [], []
    for lauf in laeufe:
        lo, hi = lauf[0], lauf[-1]
        if len(lauf) == 1 and lo.denominator == 1:
            teile_e.append(f"{{{int(lo)}}}")
            teile_t.append(f"\\{{{int(lo)}\\}}")
            stuecke.append(("punkt", int(lo)))
            continue
        lo_zu, hi_zu = lo.denominator == 1, hi.denominator == 1
        a = int(lo) if lo_zu else int(lo - F(1, 2))
        b = int(hi) if hi_zu else int(hi + F(1, 2))
        teile_e.append(("[" if lo_zu else "(") + f"{a}; {b}" + ("]" if hi_zu else ")"))
        teile_t.append(_iv_tex((a, b, lo_zu, hi_zu)))
        stuecke.append(("iv", (a, b, lo_zu, hi_zu)))
    if not teile_e:
        return "{}", "\\emptyset", []
    return " ∪ ".join(teile_e), " \\cup ".join(teile_t), stuecke


def _zufalls_iv(rng):
    a = rng.randint(-5, 3)
    b = rng.randint(a + 2, a + 6)
    return (a, b, rng.random() < 0.5, rng.random() < 0.5)


_IV_OPS = {
    "∪": ("\\cup", lambda p, q: p or q, "Vereinigung: alles, was in mindestens einem Intervall liegt."),
    "∩": ("\\cap", lambda p, q: p and q, "Durchschnitt: nur, was in beiden Intervallen liegt."),
    "A\\B": ("\\setminus", lambda p, q: p and not q, "Differenz: aus $A$ alles entfernen, was in $B$ liegt."),
}


def intervall_operation(rng):
    while True:
        A, B = _zufalls_iv(rng), _zufalls_iv(rng)
        # überlappend, aber keins im anderen enthalten, Grenzen verschieden
        if A[0] < B[0] < A[1] < B[1] or B[0] < A[0] < B[1] < A[1]:
            break
    op = rng.choice(sorted(_IV_OPS))
    optex, fn, regel = _IV_OPS[op]
    erg_e, erg_t, stuecke = _bereich_aus(lambda x: fn(_iv_enthaelt(A, x), _iv_enthaelt(B, x)))
    soll = pruefer.bereich_parsen(erg_e)
    kandidaten = []
    # Verwechslung der Operation
    for anderes, (ot, f2, _) in sorted(_IV_OPS.items()):
        if anderes != op:
            kandidaten.append((_bereich_aus(lambda x, f2=f2: f2(_iv_enthaelt(A, x), _iv_enthaelt(B, x)))[0],
                               f"Das wäre ${'A ' + ot + ' B'}$. Gefragt ist $A {optex} B$."))
    if op == "A\\B":
        kandidaten.append((_bereich_aus(lambda x: _iv_enthaelt(B, x) and not _iv_enthaelt(A, x))[0],
                           "Das ist $B \\setminus A$. Bei $A \\setminus B$ startest du mit $A$."))
    # Klammer an einer Grenze falsch
    grenzen = sorted({A[0], A[1], B[0], B[1]})
    def erg_drin(x):
        return fn(_iv_enthaelt(A, x), _iv_enthaelt(B, x))
    for g in grenzen:
        links, rechts = erg_drin(g - F(1, 2)), erg_drin(g + F(1, 2))
        if links == rechts:          # kein Randpunkt eines Ergebnis-Stücks
            continue
        def gekippt(x, g=g):
            w = fn(_iv_enthaelt(A, x), _iv_enthaelt(B, x))
            return (not w) if x == g else w
        kandidaten.append((_bereich_aus(gekippt)[0],
                           f"Fast: Die Grenzen stimmen, aber bei ${g}$ ist die Klammer falsch. "
                           f"Prüfe, ob ${g}$ wirklich dazugehört."))
    fehler, gesehen = [], [soll]
    for wert, meldung in kandidaten:
        try:
            b = pruefer.bereich_parsen(wert)
        except pruefer.TermFehler:
            continue
        if any(pruefer.bereiche_gleich(b, s) for s in gesehen):
            continue
        gesehen.append(b)
        fehler.append((wert, meldung))
        if len(fehler) >= 4:
            break
    zs = {"von": min(A[0], B[0]) - 1, "bis": max(A[1], B[1]) + 1,
          "intervalle": [{"von": A[0], "bis": A[1], "von_zu": A[2], "bis_zu": A[3], "label": "A"},
                         {"von": B[0], "bis": B[1], "von_zu": B[2], "bis_zu": B[3], "label": "B"}]}
    erg_vis = {"von": zs["von"], "bis": zs["bis"], "intervalle": [], "punkte": []}
    for art, w in stuecke:
        if art == "punkt":
            erg_vis["punkte"].append({"x": w, "label": str(w)})
        else:
            erg_vis["intervalle"].append({"von": w[0], "bis": w[1], "von_zu": w[2], "bis_zu": w[3]})
    if not erg_vis["punkte"]:
        del erg_vis["punkte"]
    if not erg_vis["intervalle"]:
        del erg_vis["intervalle"]
    zeile_erg = "$$A " + optex + " B = " + erg_t + "$$"
    return {
        "frage": f"Es seien $A := {_iv_tex(A)}$ und $B := {_iv_tex(B)}$. Gib $A {optex} B$ an. "
                 "Tippe Intervalle wie `[0; 3)` und verbinde mehrere Teile mit ∪.",
        "loesung": erg_e,
        "tipps": [regel, "Zeichne beide Intervalle übereinander auf einen Zahlenstrahl.",
                  "Prüfe jede Grenze einzeln: Liegt sie in $A$? Liegt sie in $B$?"],
        "rechenweg": f"{regel}\n\n:::visual zahlenstrahl\n{json.dumps(zs)}\n:::\n\n"
                     + (f":::visual zahlenstrahl\n{json.dumps(erg_vis)}\n:::\n\n" if stuecke else "")
                     + zeile_erg,
        "erklaerung": regel + " An jeder Grenze entscheidet die Klammer, ob die Zahl dazugehört.",
        "typische_fehler": fehler,
    }


k.praxis()

k.generator(mengen_operation, typ="menge", titel="Mengenoperationen mit endlichen Mengen")
k.generator(intervall_operation, typ="loesungsmenge", titel="Mengenoperationen mit Intervallen")

_PA = [set(c) for r in range(3) for c in itertools.combinations(["1", "2"], r)]
k.mehrfach("Es sei $A := \\{1, 2\\}$. Welche Aussagen sind wahr?",
           ["$\\emptyset \\in \\mathcal{P}(A)$", "$\\{1\\} \\in \\mathcal{P}(A)$", "$A \\in \\mathcal{P}(A)$",
            "$\\emptyset \\subseteq A$", f"$|\\mathcal{{P}}(A)| = {len(_PA)}$"],
           ["$1 \\in \\mathcal{P}(A)$", "$\\{1\\} \\in A$", "$|\\mathcal{P}(A)| = 2$"],
           "$\\mathcal{P}(A) = \\{" + ", ".join(_set_tex(s) for s in _PA) + "\\}$. Die Elemente der Potenzmenge sind "
           "**Mengen**. Die Zahl $1$ ist kein Element davon, die Menge $\\{1\\}$ schon.",
           tipps=["Schreibe $\\mathcal{P}(A)$ vollständig hin.", "Die Elemente der Potenzmenge sind Mengen, keine Zahlen."],
           fehler={"$1 \\in \\mathcal{P}(A)$": "$1$ ist eine Zahl. In $\\mathcal{P}(A)$ liegen nur Mengen, z. B. $\\{1\\}$.",
                   "$\\{1\\} \\in A$": "Die Elemente von $A$ sind die Zahlen $1$ und $2$. Richtig wäre $\\{1\\} \\subseteq A$."})

k.loesungsmenge(r"""
    ## Übungsblatt-Stil: Intervalle

    Gegeben seien die Teilmengen $A := \{x \in \mathbb{R} : -4 < x \le 1\}$ und
    $B := \{x \in \mathbb{R} : 3 > x \ge -1\}$ der reellen Zahlen.
    Bestimmen Sie $B \setminus A$.
    """,
    "(1; 3)",
    "$A = (-4, 1]$, $B = [-1, 3)$. Aus $B$ wird alles bis einschließlich $1$ entfernt. Es bleibt $(1, 3)$.",
    uebungsblatt=True,
    tipps=["Schreibe $A$ und $B$ zuerst als Intervalle. Achtung: Bei $B$ steht $3 > x$, also $x < 3$.",
           "$A = (-4, 1]$ und $B = [-1, 3)$.", "Die $1$ gehört zu $A$, wird also aus $B$ entfernt."],
    rechenweg=r"""
    :::rechnung
    A = (-4, 1] || $-4 < x \le 1$
    B = [-1, 3) || $3 > x \ge -1$ heißt $-1 \le x < 3$
    B \setminus A = (1, 3) || $1 \in A$ wird entfernt, $3 \notin B$
    :::
    """,
    typische_fehler=[("[1; 3)", "Die $1$ liegt in $A = (-4, 1]$ und wird deshalb aus $B$ entfernt: runde Klammer."),
                     ("(-4; -1)", "Das ist $A \\setminus B$. Gefragt ist $B \\setminus A$."),
                     ("(1; 3]", "Die $3$ gehört nicht zu $B$, denn $3 > x$.")])

k.papier(r"""
    ## Übungsblatt-Stil: Mengengleichheit zeigen

    Seien $A$ und $B$ Teilmengen einer Grundmenge $G$. Zeigen Sie
    $$A \setminus B = A \cap B^C.$$

    Tipp zum Aufbau: Zeige zwei Inklusionen, $A \setminus B \subseteq A \cap B^C$ und
    $A \cap B^C \subseteq A \setminus B$. Für jede nimmst du ein beliebiges Element der linken
    Menge und zeigst, dass es in der rechten liegt.
    """,
    r"""
    **„$\subseteq$“:** Sei $x \in A \setminus B$. Nach Definition der Differenz gilt $x \in A$
    und $x \notin B$. Wegen $x \in G$ und $x \notin B$ ist $x \in B^C$. Also $x \in A$ und
    $x \in B^C$, das heißt $x \in A \cap B^C$.

    **„$\supseteq$“:** Sei $x \in A \cap B^C$. Dann gilt $x \in A$ und $x \in B^C$. Aus
    $x \in B^C$ folgt $x \notin B$. Also $x \in A$ und $x \notin B$, das heißt $x \in A \setminus B$.

    Beide Inklusionen zusammen ergeben $A \setminus B = A \cap B^C$. $\square$
    """,
    ["Ich habe zwei Richtungen ($\\subseteq$ und $\\supseteq$) gezeigt",
     "Ich habe jeweils mit „Sei $x \\in \\ldots$“ ein beliebiges Element genommen",
     "Ich habe die Definitionen von $\\setminus$, $\\cap$ und $^C$ ausdrücklich benutzt",
     "Ich habe am Ende gesagt, warum daraus die Gleichheit folgt"],
    "Mengengleichheit zeigt man fast immer so: zwei Teilmengen-Beziehungen, jede mit einem beliebigen Element.",
    uebungsblatt=True,
    tipps=["Schreibe zuerst auf, was $x \\in A \\setminus B$ und $x \\in A \\cap B^C$ nach Definition bedeuten."])

k.zusammenfassung(r"""
    ## Mengen

    | Begriff | Zeichen | Bedeutung |
    |---|---|---|
    | Element | $x \in A$, $x \notin A$ | $x$ liegt (nicht) in $A$ |
    | leere Menge | $\emptyset$ | Menge ohne Elemente |
    | beschreibende Form | $\{x \in G : E\}$ | alle $x$ aus $G$ mit Eigenschaft $E$ |
    | Teilmenge | $A \subseteq B$ | jedes Element von $A$ liegt in $B$ |
    | Gleichheit | $A = B$ | $A \subseteq B$ und $B \subseteq A$ |
    | Vereinigung | $A \cup B$ | in $A$ oder in $B$ |
    | Durchschnitt | $A \cap B$ | in $A$ und in $B$ |
    | Differenz | $A \setminus B$ | in $A$, aber nicht in $B$ |
    | Komplement | $A^C$ | in $G$, aber nicht in $A$ |
    | Mächtigkeit | $\lvert A \rvert$ | Anzahl der Elemente |
    | Potenzmenge | $\mathcal{P}(A)$ | Menge aller Teilmengen, $2^n$ Stück |
    | kartesisches Produkt | $A \times B$ | alle Paare $(a, b)$ mit $a \in A$, $b \in B$ |

    - $\mathbb{N} = \{1, 2, 3, \ldots\}$, $\mathbb{N}_0 = \{0, 1, 2, \ldots\}$, $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{R}$, $\mathbb{R}_{>0}$.
    - Intervalle: $[a, b]$ abgeschlossen, $(a, b)$ offen, $(a, b]$ und $[a, b)$ halboffen. Bei $\infty$ immer runde Klammer.

    !! Reihenfolge und Doppelnennungen sind in Mengen egal, in Paaren zählt die Reihenfolge.
""")
