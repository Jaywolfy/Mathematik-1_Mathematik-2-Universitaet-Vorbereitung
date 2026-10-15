# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 4: All- und Existenzquantor (Skript Disser WS 26/27, Abschn. 1.5).

Deckt ab: Def. 1.32 (∀, ∃), Bsp. 1.33 (B1, B3, A6), die beiden Negationsregeln (ohne Nummer im Skript),
Def. 1.34 (Vereinigung und Schnitt über ein Mengensystem), Bemerkung zum leeren Schnitt ⋂_{M∈∅} M = G.
Alle Wahrheitswerte und Mengen rechnet Python (all/any, frozenset).
"""
import itertools
import json

from ..engine import neues_kapitel

k = neues_kapitel(
    slug="uni_quantoren",
    titel="All- und Existenzquantor",
    beschreibung="∀ und ∃, Negation von Quantoren, Vereinigung und Schnitt über Mengensysteme, leerer Schnitt nach dem Skript",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 1.5",
    icon="∀")

k.lernziele([
    "Ich kann Aussagen mit $\\forall$ und $\\exists$ lesen, übersetzen und über einer endlichen Menge auswerten (Def. 1.32)",
    "Ich kann Quantoraussagen richtig negieren: $\\forall$ wird zu $\\exists$ und umgekehrt, die Aussageform wird negiert",
    "Ich weiß, wann ein Gegenbeispiel eine Allaussage widerlegt und ein Beispiel eine Existenzaussage beweist",
    "Ich kann Vereinigung und Schnitt über ein Mengensystem (Def. 1.34) bilden und kenne den leeren Schnitt",
])

k.warum(r"""
`all(...)` und `any(...)` in Python sind genau $\forall$ und $\exists$ über eine Liste. Fast jeder Satz
in Mathe 1 hat einen Quantor: „für alle Matrizen gilt“, „es existiert eine Basis“, die
$\varepsilon$-Definition des Grenzwerts. Wer Quantoren sicher negiert, versteht, wann ein Programm
**nicht** korrekt ist: Ein einziger Testfall, der scheitert, widerlegt eine „für alle Eingaben“-Behauptung.
""")


# ── Hilfen ──────────────────────────────────────────────────────────────────
def _tex(x):
    if isinstance(x, frozenset):
        return "\\{" + ", ".join(_tex(y) for y in sorted(x, key=lambda z: (isinstance(z, frozenset), str(z)))) + "\\}" if x else "\\emptyset"
    return str(x)


def _txt(x):
    if isinstance(x, frozenset):
        return "{" + "; ".join(_txt(y) for y in sorted(x, key=lambda z: (isinstance(z, frozenset), str(z)))) + "}" if x else "{}"
    return str(x)


def _venn(mengen, markiert, universum, einr="    ", **extra):
    d = {"mengen": [{"name": n, "elemente": sorted(e)} for n, e in mengen], "universum": sorted(universum), "markiert": markiert}
    d.update(extra)
    return ":::visual venn\n" + einr + json.dumps(d, ensure_ascii=False) + "\n" + einr + ":::"


def _vereinigung(system):
    return frozenset().union(*system) if system else frozenset()


def _schnitt(system, grundmenge):
    # Def. 1.34: {x ∈ G | ∀M ∈ system: x ∈ M}; für das leere System ist das G
    return frozenset(x for x in grundmenge if all(x in m for m in system))


# Prüfung der Aussagen aus dem Skript
assert _schnitt([], frozenset(range(5))) == frozenset(range(5))
assert _vereinigung([]) == frozenset()
_E = {"even": lambda n: n % 2 == 0}
assert not all(_E["even"](n) for n in range(0, 50)) and any(_E["even"](n) for n in range(0, 50))   # Bsp. 1.33

# ── 1: Definition 1.32 ───────────────────────────────────────────────────────
k.erklaerung("Für alle und es existiert", r"""
    ## Definition 1.32

    Für eine [[Aussageform]] $E(x)$ und eine Menge $M$ erzeugen der Allquantor $\forall$ und der
    Existenzquantor $\exists$ ([[Quantor]]) Aussagen:

    :::rechnung Die beiden Quantoren
    \forall x \in M : E(x) || Für alle $x \in M$ gilt $E(x)$ ([[Allaussage]])
    \exists x \in M : E(x) || Es existiert mindestens ein $x \in M$, für das $E(x)$ gilt ([[Existenzaussage]])
    :::

    „Mindestens ein“ heißt: Es dürfen auch mehrere sein. Jede dieser Aussagen ist wahr oder falsch,
    die Variable $x$ ist durch den Quantor **gebunden** und braucht keine Belegung mehr.

    :::alt Mit all und any erklärt
    In Python ist `all(E(x) for x in M)` die Allaussage und `any(E(x) for x in M)` die
    Existenzaussage. `all` prüft jedes Element, `any` hört beim ersten Treffer auf.
    :::
    ---
    ## Beispiel 1.33

    Aus Abschnitt 1.1: $B_1(x)$: „Die Zahl $x$ ist gerade.“ und $B_3(r)$: „Hat ein Kreis Radius $r$,
    so ist seine Fläche $\pi r^2$.“

    :::rechnung Auswertung
    \forall n \in \mathbb{N} : B_1(n) || falsch: $1$ ist ein [[Gegenbeispiel]]. Das ist die Aussage $A_6$ aus Beispiel 1.2
    \exists n \in \mathbb{N} : B_1(n) || wahr: $n = 0$ (oder $2$, $4$) ist ein Beispiel
    \forall r \in \{x \in \mathbb{R} \mid x > 0\} : B_3(r) || wahr: die Kreisformel gilt für jeden positiven Radius
    :::

    :::achtung Beispiele beweisen nur Existenz
    Dass $B_1(0)$, $B_1(2)$, $B_1(4)$ wahr sind, beweist $\forall n \in \mathbb{N} : B_1(n)$ **nicht**.
    Eine Allaussage über unendlich viele Elemente braucht einen Beweis für ein beliebiges $x$.
    Zum Widerlegen genügt dagegen **ein** Gegenbeispiel.
    :::

    :::alt Mit einer Prüfung erklärt
    „Alle Teilnehmer haben bestanden“ ist widerlegt, sobald einer durchgefallen ist. „Mindestens ein
    Teilnehmer hat bestanden“ ist bewiesen, sobald du einen bestandenen Zettel findest.
    :::
    """)

_ZEILEN = [("$\\forall n \\in \\mathbb{N} : n \\text{ ist gerade}$", "falsch"),
           ("$\\exists n \\in \\mathbb{N} : n \\text{ ist gerade}$", "wahr"),
           ("$\\forall n \\in \\mathbb{N} : n \\ge 0$", "wahr"),
           ("$\\exists n \\in \\mathbb{N} : n < 0$", "falsch")]
k.zuordnen("Ordne jeder Aussage ihren Wahrheitswert zu (im Skript gilt $\\mathbb{N} = \\{0, 1, 2, \\ldots\\}$).", _ZEILEN,
           "Nicht jede Zahl ist gerade ($1$), aber $0$ ist gerade. Im Skript ist $0 \\in \\mathbb{N}$, also gilt $n \\ge 0$ für alle $n$. "
           "Negative natürliche Zahlen gibt es nicht.",
           tipps=["Suche bei $\\forall$ ein Gegenbeispiel, bei $\\exists$ ein Beispiel.", "Gehört die $0$ zu $\\mathbb{N}$?"])

k.wf("Die Aussage $\\forall n \\in \\mathbb{N} : n \\text{ ist gerade}$ ist falsch.", True,
     "Das ist Aussage $A_6$ aus Beispiel 1.2: Schon $n = 1$ ist ein Gegenbeispiel.",
     tipps=["Eine Allaussage ist falsch, sobald ein einziges Element die Aussageform nicht erfüllt."])

k.wf("Für die leere Menge gilt $\\forall x \\in \\emptyset : x > 5$.", True,
     "Es gibt in $\\emptyset$ kein $x$, das die Aussage verletzt. Eine Allaussage über die leere Menge ist immer wahr "
     "(wie bei ex falso quodlibet: „$x \\in \\emptyset \\Rightarrow x > 5$“). Die Existenzaussage $\\exists x \\in \\emptyset : x > 5$ ist dagegen falsch.",
     tipps=["Gibt es ein Gegenbeispiel in $\\emptyset$?", "Python: `all([])` ist `True`, `any([])` ist `False`."])

# ── 2: Negation ──────────────────────────────────────────────────────────────
k.erklaerung("Quantoren negieren", r"""
    ## Die beiden Regeln

    Um zu zeigen, dass eine Aussage mit Quantor **nicht** gilt, helfen die Zusammenhänge. Für eine
    Aussageform $E(x)$ und eine Menge $M$ gilt:
    $$\neg(\forall x \in M : E(x)) \Leftrightarrow \exists x \in M : \neg E(x)$$
    $$\neg(\exists x \in M : E(x)) \Leftrightarrow \forall x \in M : \neg E(x)$$

    Merke: Der Quantor **kippt**, die Menge bleibt, die Aussageform wird **negiert**. Das ist die
    Verallgemeinerung von De Morgan: $\forall$ ist ein großes $\land$, $\exists$ ein großes $\lor$.

    :::rechnung Beispiel vorgerechnet
    \neg(\forall n \in \mathbb{N} : n \text{ ist gerade}) || zu negieren
    \exists n \in \mathbb{N} : \neg(n \text{ ist gerade}) || $\forall$ kippt zu $\exists$, $E$ wird negiert
    \exists n \in \mathbb{N} : n \text{ ist ungerade} || ausgeschrieben, wahr mit $n = 1$
    :::

    :::alt Mit Nein-Sagen erklärt
    Jemand behauptet: „Alle Studierenden mögen Mathe.“ Du widersprichst nicht mit „Alle mögen Mathe
    nicht“, sondern mit „Einer mag Mathe nicht“. Und wer behauptet „Keiner mag Mathe“, wird
    widerlegt durch „Mindestens einer mag es“, das ist $\neg \forall \neg$.
    :::
    ---
    ## Typische Fehler beim Negieren

    :::achtung Nur ein Teil wird negiert
    „Nicht alle Zahlen sind gerade“ heißt **nicht** „alle Zahlen sind ungerade“. Richtig ist: „Es gibt
    eine ungerade Zahl.“ Beides auf einmal zu ändern (Quantor kippen **und** $E$ negieren) ist
    die Regel. Wer nur $E$ negiert ($\forall n : n$ ungerade) oder nur den Quantor kippt
    ($\exists n : n$ gerade), macht einen Fehler.
    :::

    :::rechnung Probe mit $M = \{1, 2, 3\}$ und $E(x)$: $x \le 2$
    \forall x \in M : x \le 2 || falsch ($3 \le 2$ stimmt nicht)
    \exists x \in M : x > 2 || wahr, das ist die richtige Negation: $x = 3$
    \forall x \in M : x > 2 || falsch, also **nicht** die Negation
    :::

    :::alt Mit einer Wahrheitstabelle erklärt
    Über $M = \{1, 2\}$ ist $\forall x : E(x)$ dasselbe wie $E(1) \land E(2)$. Negiert nach De Morgan
    (Satz 1.14): $\neg E(1) \lor \neg E(2)$, und das ist $\exists x : \neg E(x)$. Genau dieselbe
    Rechnung steckt hinter der Quantorenregel, nur mit beliebig vielen Elementen.
    :::
    """)

k.mc("Wie lautet die Negation von $\\forall x \\in M : E(x)$?",
     ["$\\exists x \\in M : \\neg E(x)$", "$\\forall x \\in M : \\neg E(x)$",
      "$\\exists x \\in M : E(x)$", "$\\neg \\exists x \\in M : \\neg E(x)$"],
     "Der Quantor kippt zu $\\exists$ und die Aussageform wird negiert: $\\exists x \\in M : \\neg E(x)$.",
     tipps=["Es gibt zwei Änderungen: eine am Quantor, eine an $E$.", "Eine Allaussage wird durch **ein** Gegenbeispiel widerlegt."],
     fehler={"$\\forall x \\in M : \\neg E(x)$": "Das sagt „kein $x$ erfüllt $E$“. Es genügt aber, dass **nicht alle** $E$ erfüllen.",
             "$\\exists x \\in M : E(x)$": "Der Quantor ist gekippt, aber $E$ nicht negiert. Hier würde ein einziges Beispiel schon reichen, ein Gegenbeispiel wird aber gebraucht."})

k.mc("Wie lautet die Negation von „Es gibt eine natürliche Zahl, die kleiner als $0$ ist.“ ($\\mathbb{N} = \\{0, 1, \\ldots\\})$?",
     ["Für alle $n \\in \\mathbb{N}$ gilt $n \\ge 0$.", "Für alle $n \\in \\mathbb{N}$ gilt $n < 0$.",
      "Es gibt ein $n \\in \\mathbb{N}$ mit $n \\ge 0$.", "Es gibt ein $n \\in \\mathbb{N}$ mit $n > 0$."],
     "$\\neg \\exists n : n < 0 \\Leftrightarrow \\forall n : \\neg(n < 0)$, und $\\neg(n < 0)$ ist $n \\ge 0$.",
     tipps=["Quantor kippen und die Aussageform negieren.", "Was ist das Gegenteil von $n < 0$? Prüfe $n = 0$."],
     fehler={"Für alle $n \\in \\mathbb{N}$ gilt $n < 0$.": "Hier wurde nur der Quantor gekippt, die Aussageform aber nicht negiert.",
             "Es gibt ein $n \\in \\mathbb{N}$ mit $n \\ge 0$.": "Der Quantor muss kippen: Aus „es gibt“ wird „für alle“.",
             "Es gibt ein $n \\in \\mathbb{N}$ mit $n > 0$.": "Weder der Quantor gekippt noch richtig negiert ($0$ erfüllt $n \\ge 0$, aber nicht $n > 0$)."})

k.wf("$\\neg(\\exists x \\in M : E(x))$ ist äquivalent zu $\\forall x \\in M : \\neg E(x)$.", True,
     "Das ist die zweite Regel im Skript: Gibt es kein $x$ mit $E(x)$, dann erfüllt jedes $x$ die Negation $\\neg E(x)$.",
     tipps=["„Es gibt keinen Fehler“ heißt „alles ist fehlerfrei“."])

# ── 3: Vereinigung und Schnitt über Mengensysteme ────────────────────────────
_SA, _SB, _SC = frozenset({1, 2, 3, 4}), frozenset({2, 3, 4, 5}), frozenset({3, 4, 5, 6})
_SG = frozenset(range(1, 8))
assert _vereinigung([_SA, _SB, _SC]) == frozenset(range(1, 7)) and _schnitt([_SA, _SB, _SC], _SG) == frozenset({3, 4})
k.erklaerung("Vereinigung und Schnitt über viele Mengen", r"""
    ## Definition 1.34

    Sei $\mathcal{M}$ eine Menge von Teilmengen einer Grundmenge $G$ (ein [[Mengensystem]]). Dann ist
    $$\bigcup_{M \in \mathcal{M}} M := \{x \in G \mid \exists M \in \mathcal{M} : x \in M\},$$
    $$\bigcap_{M \in \mathcal{M}} M := \{x \in G \mid \forall M \in \mathcal{M} : x \in M\}.$$

    Die Vereinigung enthält, was in **mindestens einer** Menge liegt, der Schnitt, was in **allen**
    liegt. Mit drei Mengen $A, B, C$ ist das $A \cup B \cup C$ und $A \cap B \cap C$.

    """ + _venn([("A", _SA), ("B", _SB), ("C", _SC)], "A ∩ B ∩ C", _SG,
                unterschrift="Markiert ist der Schnitt aller drei Mengen. Tippe auf andere Flächen.") + r"""

    :::rechnung Beispiel mit $\mathcal{M} = \{A, B, C\}$
    """ + f"A = {_tex(_SA)},\\ B = {_tex(_SB)},\\ C = {_tex(_SC)}" + r""" || drei Mengen
    """ + f"\\bigcup_{{M \\in \\mathcal{{M}}}} M = {_tex(_vereinigung([_SA, _SB, _SC]))}" + r""" || jedes Element, das irgendwo vorkommt
    """ + f"\\bigcap_{{M \\in \\mathcal{{M}}}} M = {_tex(_schnitt([_SA, _SB, _SC], _SG))}" + r""" || nur Elemente, die in allen drei liegen
    :::

    :::alt Mit Gruppen erklärt
    Mehrere Gruppenchats bilden ein System. Die Vereinigung sind alle Personen, die in mindestens einem
    Chat sind. Der Schnitt sind die Personen, die in jedem einzelnen Chat sind.
    :::
    ---
    ## Der leere Schnitt

    Beachte: Der **leere Schnitt** $\bigcap_{M \in \emptyset} M = G$ hängt von der Grundmenge $G$ ab.

    :::rechnung Warum ist das so?
    \bigcap_{M \in \emptyset} M = \{x \in G \mid \forall M \in \emptyset : x \in M\} || Definition 1.34 mit $\mathcal{M} = \emptyset$
    \forall M \in \emptyset : x \in M \text{ ist wahr für jedes } x || keine Menge im System kann $x$ verfehlen
    \bigcap_{M \in \emptyset} M = G || [[leerer Schnitt]]: alle $x \in G$ erfüllen die Bedingung
    \bigcup_{M \in \emptyset} M = \emptyset || kein $M$ im System, also kein Element, das irgendwo liegt
    :::

    :::achtung Ohne Grundmenge geht es nicht
    Der leere Schnitt wäre „alles“, und „die Menge aller Dinge“ gibt es nach der Russell'schen Antinomie
    nicht. Darum steht in Definition 1.34 die Grundmenge $G$: Der Schnitt wird daraus ausgesondert.
    :::

    :::alt Mit Türstehern erklärt
    Der Schnitt verlangt „besteht jede Kontrolle“. Gibt es gar keine Kontrolle, besteht jeder, der
    auf dem Gelände (in $G$) steht. Bei der Vereinigung lautet die Frage „besteht eine Kontrolle“.
    Ohne Kontrolle besteht keiner.
    :::
    """)

_S1 = [frozenset({1, 2, 3}), frozenset({2, 3, 4}), frozenset({3, 4, 5})]
k.menge(f"Es sei $\\mathcal{{M}} := \\{{{', '.join(_tex(m) for m in _S1)}\\}}$ eine Menge von Teilmengen von $G := \\{{1, \\ldots, 6\\}}$. "
        "Gib $\\bigcup_{M \\in \\mathcal{M}} M$ an.",
        _txt(_vereinigung(_S1)),
        "Die Vereinigung enthält alle Elemente, die in mindestens einer der drei Mengen liegen: $1, \\ldots, 5$. Die $6$ liegt in keiner.",
        tipps=["Gesucht: alle $x$, die in **mindestens einer** Menge liegen.", "Gehe die drei Mengen nacheinander durch.",
               "Die Elemente $1, \\ldots, 5$ liegen jeweils in mindestens einer Menge."],
        rechenweg=r"""
        :::rechnung
        """ + f"\\bigcup_{{M \\in \\mathcal{{M}}}} M = {_tex(_vereinigung(_S1))}" + r""" || ein Element, das irgendwo vorkommt, gehört dazu
        :::
        """,
        typische_fehler=[(_txt(_schnitt(_S1, frozenset(range(1, 7)))), "Das ist der Schnitt. Die Vereinigung nimmt alles, was in **mindestens einer** Menge liegt."),
                         (_txt(frozenset(range(1, 7))), "Die $6$ liegt in keiner der drei Mengen, also nicht in der Vereinigung.")])

k.mc("Es sei $G$ eine Grundmenge. Was ist der leere Schnitt $\\bigcap_{M \\in \\emptyset} M$?",
     ["$G$", "$\\emptyset$", "$\\{\\emptyset\\}$", "Er ist nicht definiert."],
     "Nach Definition 1.34 gilt $x \\in \\bigcap$ genau dann, wenn $\\forall M \\in \\emptyset : x \\in M$. Das ist für jedes $x \\in G$ wahr (leere Allaussage). Also ist der leere Schnitt $G$.",
     tipps=["Setze die Definition mit $\\mathcal{M} = \\emptyset$ ein.", "Welche $x$ erfüllen $\\forall M \\in \\emptyset : x \\in M$?"],
     fehler={"$\\emptyset$": "Das ist die leere **Vereinigung**. Beim Schnitt ist die Bedingung „in allen Mengen“ für ein leeres System immer erfüllt.",
             "Er ist nicht definiert.": "Er ist definiert, weil die Grundmenge $G$ in der Definition steht. Der Wert hängt von $G$ ab."})

# ── 4: Reihenfolge der Quantoren ─────────────────────────────────────────────
k.erklaerung("Mehrere Quantoren", r"""
    ## Die Reihenfolge zählt

    Quantoren dürfen hintereinander stehen. Dann gilt: Von links nach rechts lesen, und jede
    Variable ist ab ihrem Quantor festgelegt.

    :::rechnung Gleiche Aussageform, verschiedene Reihenfolge, $M = \{1, 2, 3\}$
    \forall x \in M\ \exists y \in M : y > x || Zu jedem $x$ gibt es ein größeres $y$: falsch, für $x = 3$ gibt es keins
    \exists y \in M\ \forall x \in M : y \ge x || Es gibt ein $y$, das größer-gleich allen ist: wahr mit $y = 3$
    \forall x \in M\ \exists y \in M : y \ge x || mit $y := x$ wahr, aber schwächer als die vorige Zeile
    :::

    Kurzschreibweise (so steht es später im Skript): $\forall x, y \in M : E(x, y)$ bedeutet
    $\forall x \in M\ \forall y \in M : E(x, y)$, und $\exists a \in A, b \in B : E(a, b)$ bedeutet
    $\exists a \in A\ \exists b \in B : E(a, b)$.

    $\forall x\ \exists y$ erlaubt, dass $y$ **von $x$ abhängt**. Bei $\exists y\ \forall x$ muss ein
    einziges $y$ für alle $x$ passen.

    :::achtung ∀∃ ist nicht ∃∀
    Aus „$\exists y\ \forall x : E(x, y)$“ folgt „$\forall x\ \exists y : E(x, y)$“, aber nicht umgekehrt. Jeder Mensch hat eine Mutter ($\forall\exists$), aber es
    gibt keine Person, die Mutter aller ist ($\exists\forall$).
    :::

    :::alt Mit Schlüsseln erklärt
    $\forall x\ \exists y$: Zu jedem Schloss gibt es einen passenden Schlüssel (es darf für jedes
    Schloss ein anderer sein). $\exists y\ \forall x$: Es gibt einen Generalschlüssel, der in alle Schlösser passt.
    :::
    """)

_MM = [1, 2, 3, 4]


def _ae(f):
    return all(any(f(x, y) for y in _MM) for x in _MM)


def _ea(f):
    return any(all(f(x, y) for x in _MM) for y in _MM)


assert not _ae(lambda x, y: y > x) and _ea(lambda x, y: y >= x) and _ae(lambda x, y: y >= x)
k.mc("Für $M = \\{1, 2, 3, 4\\}$: Welche Aussage ist wahr?",
     ["$\\exists y \\in M\\ \\forall x \\in M : y \\ge x$", "$\\forall x \\in M\\ \\exists y \\in M : y > x$",
      "$\\exists y \\in M\\ \\forall x \\in M : y > x$", "$\\forall x \\in M\\ \\exists y \\in M : y < x - 3$"],
     "$y = 4$ ist größer-gleich allen $x \\in M$. Bei „$\\forall x\\ \\exists y : y > x$“ scheitert $x = 4$ (kein größeres $y$), und bei „$\\exists y\\ \\forall x : y > x$“ scheitert $x = y$.",
     tipps=["Lies von links nach rechts: Welche Variable wird zuerst gewählt?", "Teste das größte Element von $M$."],
     fehler={"$\\forall x \\in M\\ \\exists y \\in M : y > x$": "Für $x = 4$ gibt es kein $y \\in M$ mit $y > 4$.",
             "$\\exists y \\in M\\ \\forall x \\in M : y > x$": "Für $x = y$ gilt $y > y$ nicht, also kann kein $y$ größer als alle $x$ sein."})

# ── Praxis ──────────────────────────────────────────────────────────────────
_PRAED = [
    ("x \\text{ ist gerade}", "x \\text{ ist ungerade}", lambda x: x % 2 == 0),
    ("x > 3", "x \\le 3", lambda x: x > 3),
    ("x^2 < 20", "x^2 \\ge 20", lambda x: x * x < 20),
    ("x \\le 5", "x > 5", lambda x: x <= 5),
    ("x \\text{ ist durch } 3 \\text{ teilbar}", "x \\text{ ist nicht durch } 3 \\text{ teilbar}", lambda x: x % 3 == 0),
    ("x + 2 \\ge 4", "x + 2 < 4", lambda x: x + 2 >= 4),
]


def quantor_auswerten(rng):
    ep, np_, f = rng.choice(_PRAED)
    quant = rng.choice(["\\forall", "\\exists"])
    n = rng.randint(3, 6)
    m = sorted(rng.sample(range(0, 10), n))
    werte = [f(x) for x in m]
    wahr = all(werte) if quant == "\\forall" else any(werte)
    if quant == "\\forall":
        beleg = next((x for x in m if not f(x)), None)
        erkl = (f"Alle ${n}$ Elemente erfüllen $E$, also ist die Aussage wahr." if wahr
                else f"Gegenbeispiel: $x = {beleg}$ erfüllt $E$ nicht. Ein Gegenbeispiel widerlegt eine Allaussage.")
    else:
        beleg = next((x for x in m if f(x)), None)
        erkl = (f"Beispiel: $x = {beleg}$ erfüllt $E$. Ein Beispiel beweist eine Existenzaussage." if wahr
                else f"Kein Element von ${{{', '.join(map(str, m))}}}$ erfüllt $E$, also ist die Aussage falsch.")
    erkl = erkl.replace("${" + ", ".join(map(str, m)) + "}$", "$\\{" + ", ".join(map(str, m)) + "\\}$")
    return {
        "typ": "wf",
        "frage": f"Es sei $M := \\{{{', '.join(map(str, m))}\\}}$. Die Aussage ${quant} x \\in M : {ep}$ ist wahr.",
        "wahr": wahr,
        "tipps": ["Prüfe die Elemente von $M$ der Reihe nach.",
                  "$\\forall$: ein Gegenbeispiel genügt zum Widerlegen. $\\exists$: ein Beispiel genügt zum Beweisen."],
        "rechenweg": "Wahrheitswerte von $E$:\n\n" + "\n".join(f"- $x = {x}$: {'wahr' if w else 'falsch'}" for x, w in zip(m, werte)),
        "erklaerung": erkl,
    }


def quantor_negation(rng):
    ep, np_, f = rng.choice(_PRAED)
    quant, gekippt = rng.choice([("\\forall", "\\exists"), ("\\exists", "\\forall")])
    n = rng.randint(3, 6)
    m = sorted(rng.sample(range(0, 10), n))
    orig = f"{quant} x \\in M : {ep}"
    richtig = f"{gekippt} x \\in M : {np_}"
    nur_quantor = f"{gekippt} x \\in M : {ep}"
    nur_praed = f"{quant} x \\in M : {np_}"
    keine = f"\\neg({gekippt} x \\in M : {np_})"
    # Python prüft: die richtige Negation hat in jedem Modell den umgekehrten Wert
    werte = [f(x) for x in m]
    w_orig = all(werte) if quant == "\\forall" else any(werte)
    w_richtig = (any(not w for w in werte) if gekippt == "\\exists" else all(not w for w in werte))
    assert w_orig != w_richtig
    optionen = [f"${richtig}$", f"${nur_quantor}$", f"${nur_praed}$", f"${keine}$"]
    return {
        "typ": "mc",
        "frage": f"Wie lautet die Negation von ${orig}$ (mit $M := \\{{{', '.join(map(str, m))}\\}}$)?",
        "optionen": optionen,
        "fehler": {optionen[1]: "Der Quantor ist gekippt, aber die Aussageform wurde nicht negiert.",
                   optionen[2]: "Die Aussageform ist negiert, aber der Quantor ist nicht gekippt.",
                   optionen[3]: "Das ist die Negation der **richtigen** Negation, also wieder die Ausgangsaussage."},
        "tipps": ["Quantor kippen **und** Aussageform negieren.", f"Die Negation von ${ep}$ ist ${np_}$.",
                  f"Die richtige Antwort beginnt mit ${gekippt}$ und enthält ${np_}$."],
        "rechenweg": f":::rechnung\n\\neg({orig}) || zu negieren\n{richtig} || Quantor kippt, $E$ wird negiert\n:::",
        "erklaerung": f"${richtig}$: $\\forall \\leftrightarrow \\exists$ und ${ep}$ wird zu ${np_}$. "
                      f"Probe: Die Ausgangsaussage ist {'wahr' if w_orig else 'falsch'}, die Negation {'falsch' if w_orig else 'wahr'}.",
    }


def mengensystem(rng):
    g = frozenset(range(1, 9))
    anzahl = rng.randint(2, 4)
    while True:
        sys = [frozenset(x for x in g if rng.random() < 0.6) for _ in range(anzahl)]
        sys = list(dict.fromkeys(sys))
        if len(sys) >= 2 and all(2 <= len(s) <= 6 for s in sys):
            break
    vereinigung = rng.random() < 0.5
    soll = _vereinigung(sys) if vereinigung else _schnitt(sys, g)
    andere = _schnitt(sys, g) if vereinigung else _vereinigung(sys)
    zeichen = "\\bigcup" if vereinigung else "\\bigcap"
    fehler = []
    if andere != soll:
        fehler.append((_txt(andere), "Vereinigung und Schnitt verwechselt: ∪ = in mindestens einer, ∩ = in allen." ))
    ohne_letzte = _vereinigung(sys[:-1]) if vereinigung else _schnitt(sys[:-1], g)
    if ohne_letzte != soll:
        fehler.append((_txt(ohne_letzte), "Die letzte Menge des Systems fehlt in deiner Rechnung."))
    sys_tex = "\\{" + ", ".join(_tex(s) for s in sys) + "\\}"
    return {
        "typ": "menge",
        "frage": f"Es sei $G := \\{{1, \\ldots, 8\\}}$ und $\\mathcal{{M}} := {sys_tex}$. Gib ${zeichen}_{{M \\in \\mathcal{{M}}}} M$ an.",
        "loesung": _txt(soll),
        "tipps": ["Vereinigung: in mindestens einer Menge. Schnitt: in allen Mengen.",
                  "Prüfe jedes Element von $G$ einzeln: In wie vielen Mengen des Systems liegt es?",
                  "Die leere Menge schreibst du als `{}`. Sie ist möglich, etwa wenn kein Element in allen Mengen liegt."],
        "rechenweg": f":::rechnung\n{zeichen}_{{M \\in \\mathcal{{M}}}} M = {_tex(soll)} || Definition 1.34, jedes $x \\in G$ geprüft\n:::",
        "erklaerung": f"${zeichen}_{{M \\in \\mathcal{{M}}}} M = {_tex(soll)}$.",
        "typische_fehler": fehler,
    }


k.praxis()

k.generator(quantor_auswerten, typ="wf", titel="Quantoraussagen über endlichen Mengen auswerten")
k.generator(quantor_negation, typ="mc", titel="Quantoraussagen negieren")
k.generator(mengensystem, typ="menge", titel="Vereinigung und Schnitt über Mengensysteme")

k.papier(r"""
    ## Übungsblatt-Stil: Quantoraussage negieren

    Es sei $f\colon \mathbb{N} \to \mathbb{N}$ eine Funktion. Negieren Sie die Aussage
    $$\forall m \in \mathbb{N}\ \exists n \in \mathbb{N} : f(n) > m$$
    („$f$ ist unbeschränkt“) schrittweise und geben Sie das Ergebnis in Worten an. Zeigen Sie dann, dass
    $f(n) = n \bmod 3$ die negierte Aussage erfüllt.
    """,
    r"""
**Negation, ein Quantor nach dem anderen** (jedes Mal: Quantor kippen, Rest negieren):

$$\neg\bigl(\forall m \in \mathbb{N}\ \exists n \in \mathbb{N} : f(n) > m\bigr)$$
$$\Leftrightarrow \exists m \in \mathbb{N}\ \neg\bigl(\exists n \in \mathbb{N} : f(n) > m\bigr)$$
$$\Leftrightarrow \exists m \in \mathbb{N}\ \forall n \in \mathbb{N} : \neg\bigl(f(n) > m\bigr)$$
$$\Leftrightarrow \exists m \in \mathbb{N}\ \forall n \in \mathbb{N} : f(n) \le m.$$

In Worten: Es gibt eine Schranke $m$, die kein Funktionswert überschreitet ($f$ ist beschränkt).

**Nachweis für $f(n) = n \bmod 3$:** Wähle $m := 2$. Für jedes $n \in \mathbb{N}$ ist der Rest bei Division durch $3$ eines
aus $0, 1, 2$, also $f(n) \le 2 = m$. Damit gilt $\exists m\ \forall n : f(n) \le m$, und die ursprüngliche
Aussage ist falsch. $\square$
""",
    ["Ich habe in jedem Schritt genau einen Quantor gekippt und die Aussageform negiert",
     "Mein Ergebnis lautet $\\exists m\\ \\forall n : f(n) \\le m$ (die Reihenfolge der Quantoren ist erhalten geblieben)",
     "Ich habe ein konkretes $m$ angegeben ($m = 2$) und für **alle** $n$ begründet",
     "Ich habe in Worten gesagt, was die Negation bedeutet (beschränkt)"],
    "Beim Negieren bleibt die Reihenfolge der Quantoren, nur jeder Quantor kippt.",
    uebungsblatt=True,
    tipps=["Negiere von außen nach innen: erst $\\forall m$, dann $\\exists n$."])

_G1 = frozenset(range(1, 7))
_SY = [frozenset({1, 2, 3, 4}), frozenset({2, 3, 4, 5}), frozenset({2, 4, 6})]
assert _schnitt(_SY, _G1) == frozenset({2, 4}) and _vereinigung(_SY) == _G1
k.papier(r"""
    ## Übungsblatt-Stil: Schnitt über ein Mengensystem

    Sei $G := \{1, \ldots, 6\}$ und $\mathcal{M} := \{\{1, 2, 3, 4\}, \{2, 3, 4, 5\}, \{2, 4, 6\}\}$. Bestimmen Sie
    $\bigcap_{M \in \mathcal{M}} M$ und $\bigcup_{M \in \mathcal{M}} M$ mit Hilfe der Definition 1.34 und begründen Sie
    jedes Element. Was ist $\bigcap_{M \in \emptyset} M$?
    """,
    r"""
**Schnitt:** $x \in \bigcap M$ gilt genau dann, wenn $x$ in **allen** drei Mengen liegt.

| $x$ | in $\{1,2,3,4\}$ | in $\{2,3,4,5\}$ | in $\{2,4,6\}$ | im Schnitt |
|---|---|---|---|---|
| 1 | ja | nein | nein | nein |
| 2 | ja | ja | ja | **ja** |
| 3 | ja | ja | nein | nein |
| 4 | ja | ja | ja | **ja** |
| 5 | nein | ja | nein | nein |
| 6 | nein | nein | ja | nein |

Also $\bigcap_{M \in \mathcal{M}} M = \{2, 4\}$. Die **Vereinigung** enthält jedes $x$, das in mindestens einer Menge liegt: Jede Zahl von $1$ bis $6$ liegt in einer, also $\bigcup_{M \in \mathcal{M}} M = \{1, \ldots, 6\} = G$.

**Leerer Schnitt:** $\forall M \in \emptyset : x \in M$ ist für jedes $x \in G$ wahr, also $\bigcap_{M \in \emptyset} M = G$.
""",
    ["Ich habe jedes Element von $G$ einzeln geprüft (Tabelle oder Aufzählung)",
     "Mein Schnitt ist $\\{2, 4\\}$ und meine Vereinigung ist $\\{1, \\ldots, 6\\}$",
     "Ich habe den leeren Schnitt als $G$ angegeben und begründet (leere Allaussage ist wahr)"],
    "Der Schnitt ist eine Allaussage, die Vereinigung eine Existenzaussage. Alles andere folgt aus Definition 1.32.",
    uebungsblatt=True,
    tipps=["Prüfe für jedes $x$: Liegt es in allen Mengen? Liegt es in mindestens einer?"])

k.zusammenfassung(r"""
    ## All- und Existenzquantor (Skript 1.5)

    | Schreibweise | Bedeutung |
    |---|---|
    | $\forall x \in M : E(x)$ | für alle $x \in M$ gilt $E(x)$ (widerlegt durch **ein** Gegenbeispiel) |
    | $\exists x \in M : E(x)$ | es gibt mindestens ein $x \in M$ mit $E(x)$ (bewiesen durch **ein** Beispiel) |

    !! $\neg(\forall x \in M : E(x)) \Leftrightarrow \exists x \in M : \neg E(x)$ und $\neg(\exists x \in M : E(x)) \Leftrightarrow \forall x \in M : \neg E(x)$. Quantor kippt, $E$ wird negiert.

    - Beispiel 1.33: $\forall n \in \mathbb{N} : B_1(n)$ ist falsch ($A_6$), $\exists n \in \mathbb{N} : B_1(n)$ ist wahr.
    - Über der leeren Menge ist jede Allaussage wahr, jede Existenzaussage falsch (`all([])`, `any([])`).
    - Definition 1.34: $\bigcup_{M \in \mathcal{M}} M := \{x \in G \mid \exists M \in \mathcal{M} : x \in M\}$, $\bigcap_{M \in \mathcal{M}} M := \{x \in G \mid \forall M \in \mathcal{M} : x \in M\}$.
    - Leerer Schnitt $\bigcap_{M \in \emptyset} M = G$ (hängt von der Grundmenge ab), leere Vereinigung $= \emptyset$.
    - Reihenfolge zählt: aus $\exists y\ \forall x$ folgt $\forall x\ \exists y$, nicht umgekehrt.
""")
