# -*- coding: utf-8 -*-
"""Vorkurs 3: Implikation, Äquivalenz, Tautologie – Wenn-dann, genau dann wenn, notwendig und
hinreichend, Tautologie und Widerspruch, De Morgan (MVK 2026, VL 1–2)."""
import itertools
import json

from ..engine import neues_kapitel
from ..visuals import logik_parse, logik_tex, logik_wert

k = neues_kapitel(
    slug="implikation",
    titel="Implikation, Äquivalenz, Tautologie",
    beschreibung="Wenn-dann und genau-dann-wenn, notwendig und hinreichend, Tautologie, Widerspruch und De Morgan",
    teil="vorkurs",
    quelle="MVK 2026, VL 1–2",
    icon="➡️")

k.lernziele([
    "Ich kenne die Wahrheitstafeln von $A \\Rightarrow B$ und $A \\Leftrightarrow B$ und kann den Unterschied beschreiben",
    "Ich kann Wenn-dann-Sätze mit „hinreichend“ und „notwendig“ lesen und von ihrer Umkehrung unterscheiden",
    "Ich erkenne Tautologien und Widersprüche",
    "Ich kann mit einer Wahrheitstafel beweisen, dass zwei Aussagen äquivalent sind",
    "Ich kann „und“, „oder“ und „wenn, dann“ korrekt negieren (De Morgan)",
])

k.warum(r"""
Mathematische Sätze sind fast immer Implikationen: „Wenn Voraussetzung, dann Behauptung.“
Wer die Implikation mit ihrer Umkehrung verwechselt, beweist das Falsche. In der Informatik
steckt sie in jeder Spezifikation („Wenn die Eingabe sortiert ist, dann liefert die Suche …“)
und in Tests. Die Regeln von De Morgan brauchst du ständig, um Bedingungen umzuschreiben:
`not (a and b)` ist dasselbe wie `(not a) or (not b)`. Und Tautologien sind genau die
Bedingungen, die ein Compiler als „immer wahr“ wegoptimieren darf.
""")


def _spalte(formel, variablen=("A", "B")):
    ast = logik_parse(formel)
    return [logik_wert(ast, dict(zip(variablen, w))) for w in itertools.product([True, False], repeat=len(variablen))]


def _vis(variablen, ausdruecke, **extra):
    d = {"variablen": list(variablen), "ausdruecke": list(ausdruecke)}
    d.update(extra)
    return ":::visual wahrheitstabelle\n" + json.dumps(d, ensure_ascii=False) + "\n:::"


# ── 1: Implikation ─────────────────────────────────────────────────────────
k.erklaerung("Die Implikation: wenn, dann", r"""
    ## $A \Rightarrow B$

    :::analogie 🤝 Ein Versprechen
    Deine Freundin sagt: „Wenn morgen die Sonne scheint, dann gehen wir schwimmen.“
    Gebrochen ist das Versprechen nur, wenn die Sonne scheint und ihr **nicht** schwimmen
    geht. Regnet es, hat sie nichts versprochen, egal was ihr dann macht.
    :::

    Die [[Implikation]] $A \Rightarrow B$ („wenn $A$, dann $B$“) schließt von $A$ auf $B$.
    $A$ heißt Voraussetzung (Prämisse), $B$ Folgerung. Sie ist **nur** falsch, wenn $A$
    wahr und $B$ falsch ist.

    """ + _vis(["A", "B"], ["A ⇒ B"], unterschrift="Nur in der zweiten Zeile (w, f) ist die Implikation falsch.") + r"""

    :::rechnung Beispiele vorgerechnet
    n \in \mathbb{N} \Rightarrow n \in \mathbb{Z} || wahr: Jede natürliche Zahl ist ganz
    2 + 2 = 5 \Rightarrow \text{Der Mond ist aus Käse.} || wahr: Die Voraussetzung ist falsch
    :::

    :::achtung Falsche Voraussetzung
    Ist $A$ falsch, ist $A \Rightarrow B$ immer wahr („aus Falschem folgt Beliebiges“).
    Das fühlt sich seltsam an, ist aber genau das Versprechen von oben: Bei Regen wurde nichts zugesagt.
    :::

    :::alt Mit einer Regel im Programm erklärt
    Die Regel „Wenn das Passwort falsch ist, dann wird der Login abgelehnt“ wird nur
    verletzt, wenn jemand mit falschem Passwort hereinkommt. Wird ein Login mit
    **richtigem** Passwort abgelehnt (etwa wegen Wartung), verletzt das diese Regel nicht.
    Sie sagt über richtige Passwörter gar nichts.
    :::
    ---
    ## Hinreichend und notwendig

    Für $A \Rightarrow B$ gibt es viele Sprechweisen:

    - „Wenn $A$, dann $B$“, „aus $A$ folgt $B$“, „$A$ impliziert $B$“.
    - „$A$ ist [[hinreichend|hinreichende Bedingung]] für $B$“: $A$ allein reicht schon, damit $B$ gilt.
    - „$B$ ist [[notwendig|notwendige Bedingung]] für $A$“: Ohne $B$ kann $A$ nicht gelten.

    :::rechnung Beispiel vorgerechnet
    x = 3 \Rightarrow x^2 = 9 || wahr für alle $x \in \mathbb{R}$
    \text{„x = 3“ ist hinreichend für „}x^2 = 9\text{“} || $x = 3$ reicht schon
    \text{„x = 3“ ist nicht notwendig für „}x^2 = 9\text{“} || auch $x = -3$ liefert $x^2 = 9$
    :::

    :::alt Mit dem Führerschein erklärt
    Einen Führerschein haben ist **notwendig** dafür, legal Auto zu fahren: ohne ihn geht
    es nicht. Er ist aber nicht **hinreichend**: Du brauchst auch ein Auto. Kurz:
    „legal fahren $\Rightarrow$ Führerschein“. Die Folgerung ist das Notwendige.
    :::
    """)

k.wf("Die Aussage „Wenn $2 + 2 = 5$ ist, dann ist der Mond aus Käse.“ ist wahr.", True,
     "Die Voraussetzung $2 + 2 = 5$ ist falsch. Eine Implikation mit falscher Voraussetzung ist immer wahr.",
     tipps=["Wann genau ist $A \\Rightarrow B$ falsch?"])

k.mc("Wann ist $A \\Rightarrow B$ falsch?",
     ["Nur wenn $A$ wahr und $B$ falsch ist", "Wenn $A$ falsch ist", "Wenn $B$ wahr und $A$ falsch ist",
      "Wenn $A$ und $B$ beide falsch sind"],
     "Ein Versprechen „wenn $A$, dann $B$“ ist nur gebrochen, wenn $A$ eintritt und $B$ nicht.",
     tipps=["Denk an das Versprechen mit der Sonne.", "Bei Regen ($A$ falsch) wurde nichts versprochen."],
     fehler={"Wenn $A$ falsch ist": "Ist die Voraussetzung falsch, ist die Implikation immer **wahr**.",
             "Wenn $B$ wahr und $A$ falsch ist": "In dieser Zeile ist $A \\Rightarrow B$ wahr: Die Voraussetzung ist falsch."})

k.mc("„$x = 3$“ und „$x^2 = 9$“ (für $x \\in \\mathbb{R}$). Was stimmt?",
     ["„$x = 3$“ ist hinreichend, aber nicht notwendig für „$x^2 = 9$“",
      "„$x = 3$“ ist notwendig, aber nicht hinreichend für „$x^2 = 9$“",
      "„$x = 3$“ ist notwendig und hinreichend für „$x^2 = 9$“",
      "„$x = 3$“ ist weder notwendig noch hinreichend für „$x^2 = 9$“"],
     "Aus $x = 3$ folgt $x^2 = 9$: hinreichend. Aber $x^2 = 9$ geht auch mit $x = -3$: nicht notwendig.",
     tipps=["Prüfe: Folgt aus $x = 3$ immer $x^2 = 9$?", "Prüfe die andere Richtung mit $x = -3$."],
     fehler={"„$x = 3$“ ist notwendig, aber nicht hinreichend für „$x^2 = 9$“":
             "Notwendig hieße: Ohne $x = 3$ kann $x^2 = 9$ nicht gelten. Aber $x = -3$ geht auch.",
             "„$x = 3$“ ist notwendig und hinreichend für „$x^2 = 9$“":
             "Dann müssten beide Aussagen äquivalent sein. $x = -3$ ist ein Gegenbeispiel für die Rückrichtung."})

# ── 2: Umkehrung und Äquivalenz ────────────────────────────────────────────
k.erklaerung("Umkehrung und Äquivalenz", r"""
    ## $A \Rightarrow B$ ist nicht $B \Rightarrow A$

    Die Umkehrung von $A \Rightarrow B$ ist $B \Rightarrow A$. Das ist eine **andere**
    Aussage. Vergleiche die Spalten:

    """ + _vis(["A", "B"], ["A ⇒ B", "B ⇒ A"], unterschrift="Die Spalten unterscheiden sich in Zeile 2 und 3.") + r"""

    :::rechnung Beispiel vorgerechnet
    x = 2 \Rightarrow x^2 = 4 || wahr
    x^2 = 4 \Rightarrow x = 2 \quad \text{falsch} || Gegenbeispiel $x = -2$: $(-2)^2 = 4$, aber $-2 \neq 2$
    :::

    :::achtung Die Umkehrung ist kein Beweis
    „Wenn es regnet, ist die Straße nass“ heißt nicht „Wenn die Straße nass ist, regnet es“.
    Vielleicht fährt nur ein Sprengwagen vorbei. Wer im Beweis die Richtung vertauscht, hat
    etwas anderes gezeigt.
    :::

    :::alt Mit Tieren erklärt
    „Wenn ein Tier ein Hund ist, dann hat es vier Beine“ stimmt. „Wenn ein Tier vier Beine
    hat, dann ist es ein Hund“ stimmt nicht: Katzen haben auch vier Beine. Die Richtung des
    Pfeils macht den Unterschied.
    :::
    ---
    ## $A \Leftrightarrow B$: genau dann, wenn

    Die [[Äquivalenz]] $A \Leftrightarrow B$ („$A$ genau dann, wenn $B$“) schließt in
    **beide** Richtungen. Sie ist wahr, wenn $A$ und $B$ denselben Wahrheitswert haben.

    """ + _vis(["A", "B"], ["A ⇔ B", "(A ⇒ B) ∧ (B ⇒ A)"],
               unterschrift="Gleiche Spalten: $A \\Leftrightarrow B$ bedeutet dasselbe wie $(A \\Rightarrow B) \\land (B \\Rightarrow A)$.") + r"""

    :::rechnung Beispiel vorgerechnet
    (A \subseteq B) \land (B \subseteq A) \Leftrightarrow A = B || Mengengleichheit in beiden Richtungen
    x + 1 = 4 \Leftrightarrow x = 3 || Äquivalenzumformung: $-1$ auf beiden Seiten
    :::

    :::alt Mit einem Ticket erklärt
    „Du kommst genau dann ins Konzert, wenn du ein Ticket hast.“ Das heißt zweierlei: Mit
    Ticket kommst du rein ($\Rightarrow$), und wer drin ist, hat ein Ticket ($\Leftarrow$).
    Ticket ist also notwendig **und** hinreichend.
    :::
    """)

k.wf("Ist $A$ falsch und $B$ falsch, dann ist $A \\Leftrightarrow B$ wahr.", True,
     "$A \\Leftrightarrow B$ ist wahr, wenn beide denselben Wahrheitswert haben. Beide sind falsch, also gleich.",
     tipps=["Die Äquivalenz vergleicht nur, ob die Werte gleich sind."])

k.zuordnen("Es seien $A$: „Die Sonne scheint.“ und $B$: „Ich gehe ins Freibad.“ Ordne jedem Satz die passende Form zu.",
           [("„Wenn die Sonne scheint, gehe ich ins Freibad.“", "Implikation A ⇒ B"),
            ("„Wenn ich ins Freibad gehe, scheint die Sonne.“", "Implikation B ⇒ A"),
            ("„Die Sonne scheint und ich gehe ins Freibad.“", "Konjunktion A ∧ B"),
            ("„Die Sonne scheint oder ich gehe ins Freibad.“", "Disjunktion A ∨ B"),
            ("„Genau dann, wenn die Sonne scheint, gehe ich ins Freibad.“", "Äquivalenz A ⇔ B")],
           "Achte auf die Signalwörter: „wenn … dann“ (Richtung beachten!), „und“, „oder“, „genau dann, wenn“.",
           tipps=["Bei „wenn …“ ist der Teil direkt nach „wenn“ die Voraussetzung, also links vom Pfeil."])

# ── 3: Tautologie und Widerspruch ─────────────────────────────────────────
k.erklaerung("Tautologie und Widerspruch", r"""
    ## Immer wahr, immer falsch

    - Eine Aussage, die **immer** wahr ist, egal welche Werte die Teilaussagen haben,
      heißt [[Tautologie]]. Symbol ⊤.
    - Eine Aussage, die **immer** falsch ist, heißt [[Widerspruch]]. Symbol ⊥.

    In der Wahrheitstafel steht bei einer Tautologie in der letzten Spalte nur w, bei einem
    Widerspruch nur f.

    """ + _vis(["A"], ["¬A", "A ∨ ¬A", "A ∧ ¬A"],
               unterschrift="$A \\lor \\neg A$ ist immer wahr, $A \\land \\neg A$ immer falsch.") + r"""

    :::rechnung Beispiele vorgerechnet
    \text{„Es regnet oder es regnet nicht.“} \quad \text{Tautologie} || Disjunktion mit der eigenen Negation
    \text{„Hier schneit es und hier schneit es nicht.“} \quad \text{Widerspruch} || Konjunktion mit der eigenen Negation
    :::

    :::alt Mit Programmcode erklärt
    `if x > 5 or x <= 5:` ist für jede Zahl wahr: eine Tautologie, der `if` ist überflüssig.
    `if x > 5 and x <= 5:` ist nie wahr: ein Widerspruch, der Block wird nie ausgeführt.
    Solche Bedingungen sind fast immer ein Programmierfehler.
    :::
    ---
    ## Wahrheitstafel als Beweis

    Zwei Formeln heißen äquivalent, wenn ihre Spalten in der Wahrheitstafel **in jeder Zeile**
    übereinstimmen. Gleichwertig: $F \Leftrightarrow G$ ist eine Tautologie. Weil die Tafel
    alle Fälle abdeckt, ist das ein vollständiger Beweis.

    """ + _vis(["A", "B"], ["A ⇒ B", "¬A ∨ B", "(A ⇒ B) ⇔ (¬A ∨ B)"],
               unterschrift="Die ersten beiden Spalten sind gleich, die dritte ist nur w.") + r"""

    :::rechnung Ergebnis
    A \Rightarrow B \Leftrightarrow \neg A \lor B || „wenn $A$, dann $B$“ heißt: „nicht $A$ oder $B$“
    :::

    :::alt Mit einem Abgleich erklärt
    Stell dir zwei Funktionen `f(a, b)` und `g(a, b)` vor, die `True` oder `False` liefern.
    Es gibt nur vier mögliche Eingaben. Testest du alle vier und beide liefern jedes Mal
    dasselbe, sind sie gleichwertig. Mehr als vier Fälle gibt es nicht, also ist das ein Beweis.
    :::
    """)

_ART = {}
for _f in ("A ∨ ¬A", "A ∧ ¬A", "A ⇒ ¬A"):
    _s = _spalte(_f, ("A",))
    _ART[_f] = "Tautologie" if all(_s) else "Widerspruch" if not any(_s) else "weder noch"
k.zuordnen("Ordne jeder Aussage zu, ob sie eine Tautologie, ein Widerspruch oder keins von beiden ist.",
           [(f"${logik_tex(logik_parse(f))}$", a) for f, a in _ART.items()],
           "$A \\lor \\neg A$ ist immer wahr, $A \\land \\neg A$ immer falsch. $A \\Rightarrow \\neg A$ ist wahr, wenn $A$ "
           "falsch ist, und falsch, wenn $A$ wahr ist: Sie hängt von $A$ ab.",
           tipps=["Stelle für jede Aussage die Tafel mit zwei Zeilen auf: $A$ = w und $A$ = f."])

k.mc("Welche Aussage ist äquivalent zu $A \\Rightarrow B$?",
     ["$\\neg B \\Rightarrow \\neg A$", "$B \\Rightarrow A$", "$\\neg A \\Rightarrow \\neg B$", "$A \\land B$"],
     "$\\neg B \\Rightarrow \\neg A$ (die Kontraposition) hat dieselbe Spalte w, f, w, w. Sie ist nur falsch, wenn $B$ "
     "falsch und $A$ wahr ist, genau wie $A \\Rightarrow B$.",
     tipps=["Stelle die Spalten auf und vergleiche sie mit w, f, w, w.",
            "Wann ist $\\neg B \\Rightarrow \\neg A$ falsch?"],
     fehler={"$B \\Rightarrow A$": "Das ist die Umkehrung. Sie ist in der Zeile $A$ = f, $B$ = w falsch, $A \\Rightarrow B$ dort aber wahr.",
             "$\\neg A \\Rightarrow \\neg B$": "Das ist dieselbe Spalte wie die Umkehrung $B \\Rightarrow A$, nicht wie $A \\Rightarrow B$."})

# ── 4: De Morgan und Negation der Implikation ─────────────────────────────
k.erklaerung("Negieren: De Morgan und die Implikation", r"""
    ## Die Regeln von De Morgan

    Steht eine Negation vor einer Klammer, darfst du sie hineinziehen. Dabei **kippt** das
    Zeichen: Aus $\land$ wird $\lor$ und umgekehrt ([[Regeln von De Morgan]]).

    $$\neg(A \land B) \Leftrightarrow \neg A \lor \neg B \qquad \neg(A \lor B) \Leftrightarrow \neg A \land \neg B$$

    """ + _vis(["A", "B"], ["¬(A ∧ B)", "¬A ∨ ¬B", "¬(A ∨ B)", "¬A ∧ ¬B"],
               unterschrift="Spalte 1 = Spalte 2 und Spalte 3 = Spalte 4.") + r"""

    :::rechnung Beispiel vorgerechnet
    \neg(\text{„Es regnet und es ist kalt.“}) || Negation einer Konjunktion
    \text{„Es regnet nicht oder es ist nicht kalt.“} || $\land$ kippt zu $\lor$
    :::

    :::achtung Falsch negiert
    „Es regnet nicht **und** es ist nicht kalt“ ist **nicht** die Negation. An einem
    warmen Regentag ist die Ausgangsaussage falsch, diese Aussage aber auch.
    :::

    :::alt Mit Mengen erklärt
    Denk an Mengen: $\neg$ ist das Komplement, $\land$ der Durchschnitt, $\lor$ die
    Vereinigung. Alles außerhalb von $A \cap B$ liegt außerhalb von $A$ **oder** außerhalb
    von $B$. Male es im Venn-Diagramm aus: $(A \cap B)^C = A^C \cup B^C$.
    :::
    ---
    ## Eine Implikation verneinen

    $A \Rightarrow B$ ist nur in einem Fall falsch: $A$ wahr, $B$ falsch. Also:

    $$\neg(A \Rightarrow B) \Leftrightarrow A \land \neg B$$

    """ + _vis(["A", "B"], ["¬(A ⇒ B)", "A ∧ ¬B"], unterschrift="Beide Spalten sind nur in Zeile 2 wahr.") + r"""

    :::rechnung Beispiel vorgerechnet
    \neg(\text{„Wenn es regnet, wird die Straße nass.“}) || Negation einer Implikation
    \text{„Es regnet und die Straße wird nicht nass.“} || $A \land \neg B$
    :::

    Die Negation einer Wenn-dann-Aussage ist also **keine** Wenn-dann-Aussage.

    :::alt Mit einer Wette erklärt
    Du wettest gegen die Behauptung „Wenn es regnet, wird die Straße nass“. Um zu
    gewinnen, musst du einen Tag vorzeigen, an dem es regnet **und** die Straße trotzdem
    trocken bleibt (etwa unter einem Dach). Genau das ist $A \land \neg B$.
    :::
    """)

k.mc("Wie lautet die Negation von „Es regnet und es ist kalt.“?",
     ["„Es regnet nicht oder es ist nicht kalt.“", "„Es regnet nicht und es ist nicht kalt.“",
      "„Es regnet oder es ist kalt.“", "„Wenn es regnet, ist es nicht kalt.“"],
     "De Morgan: $\\neg(A \\land B) \\Leftrightarrow \\neg A \\lor \\neg B$. Es reicht, dass **eins** von beiden nicht stimmt.",
     tipps=["Die Ausgangsaussage ist falsch, sobald eine der beiden Teilaussagen falsch ist.",
            "Beim Hineinziehen der Negation kippt $\\land$ zu $\\lor$."],
     fehler={"„Es regnet nicht und es ist nicht kalt.“": "Du hast nur die Teilaussagen verneint, aber $\\land$ nicht "
                                                        "zu $\\lor$ gekippt. Ein warmer Regentag macht beide Aussagen falsch."})

k.mc("Wie lautet die Negation von „Wenn eine Zahl durch $4$ teilbar ist, dann ist sie gerade.“ (für eine feste Zahl $n$)?",
     ["„$n$ ist durch $4$ teilbar und $n$ ist nicht gerade.“",
      "„Wenn $n$ nicht durch $4$ teilbar ist, dann ist $n$ nicht gerade.“",
      "„Wenn $n$ durch $4$ teilbar ist, dann ist $n$ nicht gerade.“",
      "„$n$ ist nicht durch $4$ teilbar oder $n$ ist gerade.“"],
     "$\\neg(A \\Rightarrow B) \\Leftrightarrow A \\land \\neg B$: Die Voraussetzung gilt und die Folgerung nicht.",
     tipps=["Wann ist eine Implikation falsch?", "Nur wenn $A$ wahr und $B$ falsch ist."],
     fehler={"„Wenn $n$ nicht durch $4$ teilbar ist, dann ist $n$ nicht gerade.“":
             "Das ist keine Negation, sondern eine andere Implikation ($\\neg A \\Rightarrow \\neg B$).",
             "„Wenn $n$ durch $4$ teilbar ist, dann ist $n$ nicht gerade.“":
             "Die Negation einer Implikation ist keine Implikation. Für $n = 1$ wären beide Aussagen wahr.",
             "„$n$ ist nicht durch $4$ teilbar oder $n$ ist gerade.“":
             "Das ist $\\neg A \\lor B$, also gleichwertig zur Ausgangsaussage selbst, nicht ihre Negation."})


# ── Praxis ─────────────────────────────────────────────────────────────────
_ARTEN = ["Tautologie", "Widerspruch", "weder noch (mal wahr, mal falsch)"]
_KANDIDATEN = ["A ∨ ¬A", "A ∧ ¬A", "A ⇒ A", "A ⇔ ¬A", "(A ∧ B) ⇒ A", "A ⇒ (A ∨ B)", "(A ⇒ B) ∨ (B ⇒ A)",
               "(A ∧ B) ∧ ¬A", "¬(A ⇒ A)", "A ⇒ B", "(A ∨ B) ⇒ A", "(A ⇒ B) ⇔ (¬B ⇒ ¬A)", "(A ⇒ B) ⇔ (B ⇒ A)",
               "(A ∧ ¬B) ∧ (A ⇒ B)", "¬(A ∧ B) ⇔ (¬A ∨ ¬B)", "(A ∨ B) ∧ (¬A ∧ ¬B)", "A ∨ (A ⇒ B)", "A ∧ (A ⇒ B)"]


def _art(formel):
    s = _spalte(formel)
    return _ARTEN[0] if all(s) else _ARTEN[1] if not any(s) else _ARTEN[2]


def _teile(ast):
    erg = []

    def geh(a):
        if a[0] in ("var", "konst"):
            return
        for kind in a[1:]:
            if isinstance(kind, tuple):
                geh(kind)
        t = logik_tex(a)
        for x, y in (("\\neg ", "¬"), ("\\land", "∧"), ("\\lor", "∨"), ("\\Rightarrow", "⇒"), ("\\Leftrightarrow", "⇔")):
            t = t.replace(x, y)
        if t not in erg:
            erg.append(t)
    geh(ast)
    return erg


def formel_art(rng):
    formel = rng.choice(_KANDIDATEN)
    ast = logik_parse(formel)
    art = _art(formel)
    andere = [a for a in _ARTEN if a != art]
    fehler = {}
    for a in andere:
        if a == _ARTEN[0]:
            fehler[a] = "Eine Tautologie braucht in **jeder** Zeile ein w. Suche eine Zeile mit f."
        elif a == _ARTEN[1]:
            fehler[a] = "Ein Widerspruch braucht in **jeder** Zeile ein f. Suche eine Zeile mit w."
        else:
            fehler[a] = "Prüfe alle vier Zeilen: Die Werte sind überall gleich."
    teile = _teile(ast)
    return {
        "typ": "mc",
        "frage": f"Ist ${logik_tex(ast)}$ eine Tautologie, ein Widerspruch oder keins von beiden?",
        "optionen": [art] + andere,
        "fehler": fehler,
        "tipps": ["Stelle die Wahrheitstafel mit den Zeilen (w, w), (w, f), (f, w), (f, f) auf.",
                  "Baue die Spalten von innen nach außen auf.",
                  "Steht in der letzten Spalte nur w, nur f oder beides?"],
        "rechenweg": _vis(["A", "B"], teile, markiert=[teile[-1]], schrittweise=False),
        "erklaerung": f"Die letzte Spalte zeigt: ${logik_tex(ast)}$ ist {'eine Tautologie' if art == _ARTEN[0] else 'ein Widerspruch' if art == _ARTEN[1] else 'mal wahr, mal falsch'}.",
    }


_PAARE = [
    ("¬(A ∧ B)", "¬A ∨ ¬B"), ("¬(A ∧ B)", "¬A ∧ ¬B"), ("¬(A ∨ B)", "¬A ∧ ¬B"), ("¬(A ∨ B)", "¬A ∨ ¬B"),
    ("A ⇒ B", "¬B ⇒ ¬A"), ("A ⇒ B", "B ⇒ A"), ("A ⇒ B", "¬A ⇒ ¬B"), ("A ⇒ B", "¬A ∨ B"), ("A ⇒ B", "A ∨ ¬B"),
    ("¬(A ⇒ B)", "A ∧ ¬B"), ("¬(A ⇒ B)", "¬A ⇒ ¬B"), ("¬(A ⇒ B)", "A ⇒ ¬B"), ("A ⇔ B", "(A ⇒ B) ∧ (B ⇒ A)"),
    ("A ⇔ B", "(A ∧ B) ∨ (¬A ∧ ¬B)"), ("A ⇔ B", "(A ⇒ B) ∨ (B ⇒ A)"), ("¬(A ⇔ B)", "¬A ⇔ B"),
    ("A ∧ (A ∨ B)", "A"), ("A ∨ (A ∧ B)", "B"), ("¬¬A", "A"), ("A ⇒ (B ⇒ A)", "A ∨ ¬A"),
]


def aequivalenz_pruefen(rng):
    f, g = rng.choice(_PAARE)
    if rng.random() < 0.5:
        f, g = g, f
    gleich = _spalte(f) == _spalte(g)
    tf, tg = logik_tex(logik_parse(f)), logik_tex(logik_parse(g))
    zeilen = [z for z, (x, y) in zip(["(w, w)", "(w, f)", "(f, w)", "(f, f)"], zip(_spalte(f), _spalte(g))) if x != y]
    ausdruecke = list(dict.fromkeys([f, g]))
    return {
        "typ": "wf",
        "frage": f"Die Aussagen ${tf}$ und ${tg}$ sind äquivalent.",
        "wahr": gleich,
        "tipps": ["Stelle für beide eine Wahrheitstafel auf und vergleiche die Spalten Zeile für Zeile."],
        "rechenweg": _vis(["A", "B"], ausdruecke, schrittweise=False) + "\n\n"
                     + ("Die Spalten stimmen in allen vier Zeilen überein." if gleich
                        else "Die Spalten unterscheiden sich in der Zeile ($A$, $B$) = " + " und ".join(zeilen) + "."),
        "erklaerung": "Äquivalent heißt: in **jeder** Zeile derselbe Wahrheitswert. Eine abweichende Zeile genügt als Gegenbeispiel.",
    }


k.praxis()

k.generator(formel_art, typ="mc", titel="Tautologie, Widerspruch oder keins?")
k.generator(aequivalenz_pruefen, typ="wf", titel="Äquivalent oder nicht?")

k.mehrfach("Es sei $n$ eine natürliche Zahl. Welche der folgenden Implikationen sind für **jedes** $n \\in \\mathbb{N}$ wahr?",
           ["„$n$ ist durch $6$ teilbar $\\Rightarrow$ $n$ ist durch $3$ teilbar“",
            "„$n$ ist durch $6$ teilbar $\\Rightarrow$ $n$ ist gerade“",
            "„$n^2$ ist ungerade $\\Rightarrow$ $n$ ist ungerade“"],
           ["„$n$ ist durch $3$ teilbar $\\Rightarrow$ $n$ ist durch $6$ teilbar“",
            "„$n$ ist gerade $\\Rightarrow$ $n$ ist durch $4$ teilbar“"],
           "Durch $6$ teilbar heißt $n = 6k = 3 \\cdot 2k = 2 \\cdot 3k$. Ist $n^2$ ungerade, kann $n$ nicht gerade sein "
           "(sonst wäre $n^2$ gerade). Gegenbeispiele: $n = 3$ ist durch $3$, aber nicht durch $6$ teilbar; "
           "$n = 2$ ist gerade, aber nicht durch $4$ teilbar.",
           tipps=["Eine Implikation „für jedes $n$“ ist falsch, sobald ein $n$ die Voraussetzung erfüllt, die Folgerung aber nicht.",
                  "Probiere kleine Zahlen wie $n = 2$ und $n = 3$."],
           fehler={"„$n$ ist durch $3$ teilbar $\\Rightarrow$ $n$ ist durch $6$ teilbar“":
                   "Das ist die Umkehrung einer wahren Aussage. Gegenbeispiel $n = 3$.",
                   "„$n$ ist gerade $\\Rightarrow$ $n$ ist durch $4$ teilbar“": "Gegenbeispiel $n = 2$."})

_V = ["A", "B", "C"]
_T = "((A ⇒ B) ∧ (B ⇒ C)) ⇒ (A ⇒ C)"
_hilf = ["A ⇒ B", "B ⇒ C", "(A ⇒ B) ∧ (B ⇒ C)", "A ⇒ C", _T]
_asts = [logik_parse(h) for h in _hilf]
_tab = "| $A$ | $B$ | $C$ | " + " | ".join(f"${logik_tex(a)}$" for a in _asts) + " |\n|" + "---|" * (3 + len(_asts)) + "\n"
_alle_w = True
for _w in itertools.product([True, False], repeat=3):
    _b = dict(zip(_V, _w))
    _werte = [logik_wert(a, _b) for a in _asts]
    _alle_w = _alle_w and _werte[-1]
    _tab += "| " + " | ".join("w" if z else "f" for z in list(_w) + _werte) + " |\n"
assert _alle_w, "Kettenschluss muss eine Tautologie sein"

k.papier(r"""
    ## Übungsblatt-Stil: Tautologie nachweisen

    Zeigen Sie mit einer Wahrheitstafel, dass die Aussage
    $$((A \Rightarrow B) \land (B \Rightarrow C)) \Rightarrow (A \Rightarrow C)$$
    eine Tautologie ist. Erklären Sie anschließend in einem Satz, was sie im Alltag bedeutet.
    """,
    "Die Tafel hat $2^3 = 8$ Zeilen:\n\n" + _tab + r"""
    In der letzten Spalte steht nur w, also ist die Aussage eine Tautologie. $\square$

    Bedeutung (Kettenschluss): Wenn aus $A$ immer $B$ folgt und aus $B$ immer $C$, dann folgt
    aus $A$ auch $C$. Genau so verkettet man Schritte in einem Beweis.
    """,
    ["Meine Tafel hat $8$ Zeilen und alle Kombinationen von $A$, $B$, $C$",
     "Ich habe Hilfsspalten für $A \\Rightarrow B$, $B \\Rightarrow C$, ihre Konjunktion und $A \\Rightarrow C$",
     "In meiner letzten Spalte steht in jeder Zeile w",
     "Ich habe ausdrücklich geschlossen: nur w, also Tautologie"],
    "Eine Wahrheitstafel ist ein vollständiger Beweis, weil sie alle Fälle prüft.",
    uebungsblatt=True,
    tipps=["Eine Implikation ist nur falsch bei (w, f). Nutze das, um die Spalten schnell zu füllen."])

k.zusammenfassung(r"""
    ## Implikation, Äquivalenz, Tautologie

    | $A$ | $B$ | $A \Rightarrow B$ | $B \Rightarrow A$ | $A \Leftrightarrow B$ |
    |---|---|---|---|---|
    | w | w | w | w | w |
    | w | f | f | w | f |
    | f | w | w | f | f |
    | f | f | w | w | w |

    - $A \Rightarrow B$: $A$ ist hinreichend für $B$, $B$ ist notwendig für $A$. Nur falsch bei $A$ wahr, $B$ falsch.
    - Die Umkehrung $B \Rightarrow A$ ist eine andere Aussage.
    - $A \Leftrightarrow B$ heißt $(A \Rightarrow B) \land (B \Rightarrow A)$: gleiche Wahrheitswerte.
    - Tautologie (⊤): immer wahr, z. B. $A \lor \neg A$. Widerspruch (⊥): immer falsch, z. B. $A \land \neg A$.
    - Äquivalent: gleiche Spalte in der Wahrheitstafel, z. B. $A \Rightarrow B \Leftrightarrow \neg A \lor B \Leftrightarrow \neg B \Rightarrow \neg A$.

    !! De Morgan: $\neg(A \land B) \Leftrightarrow \neg A \lor \neg B$ und $\neg(A \lor B) \Leftrightarrow \neg A \land \neg B$.

    !! $\neg(A \Rightarrow B) \Leftrightarrow A \land \neg B$.
""")
