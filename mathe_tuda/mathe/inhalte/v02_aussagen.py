# -*- coding: utf-8 -*-
"""Vorkurs 2: Aussagen und Wahrheitstafeln – Aussage, Aussageform, Negation, Konjunktion,
Disjunktion, Wahrheitstafeln aufstellen (MVK 2026, VL 1–2)."""
import itertools
import json

from ..engine import neues_kapitel
from ..visuals import logik_parse, logik_tex, logik_wert

k = neues_kapitel(
    slug="aussagen",
    titel="Aussagen und Wahrheitstafeln",
    beschreibung="Was eine Aussage ist, Aussageformen, Negation, und, oder und Wahrheitstafeln",
    teil="vorkurs",
    quelle="MVK 2026, VL 1–2",
    icon="💡")

k.lernziele([
    "Ich kann entscheiden, ob eine Aussage, eine Aussageform oder keins von beiden vorliegt",
    "Ich kann eine Aussage richtig negieren",
    "Ich kenne Konjunktion $A \\land B$ und Disjunktion $A \\lor B$ und ihre Wahrheitstafeln",
    "Ich kann für eine zusammengesetzte Aussage eine Wahrheitstafel aufstellen",
    "Ich kann den Wahrheitswert einer Formel ausrechnen, wenn die Wahrheitswerte der Teilaussagen bekannt sind",
])

k.warum(r"""
Jede `if`-Bedingung in einem Programm ist eine Aussage: Sie ist entweder wahr oder falsch.
`and`, `or` und `not` in Python sind genau die Konjunktion, die Disjunktion und die Negation
aus diesem Kapitel. Wer Wahrheitstafeln beherrscht, kann komplizierte Bedingungen vereinfachen
und findet Fehler wie `if x > 0 or x < 10` (das ist für **jede** Zahl wahr). Auch digitale
Schaltungen (UND-, ODER-, NICHT-Gatter) und Datenbank-Filter mit `AND`/`OR` funktionieren so.
""")


def _spalte(formel, variablen=("A", "B")):
    """Wahrheitswerte einer Formel in der TU-Reihenfolge (w w, w f, f w, f f)."""
    ast = logik_parse(formel)
    return [logik_wert(ast, dict(zip(variablen, w))) for w in itertools.product([True, False], repeat=len(variablen))]


def _wf(werte):
    return ", ".join("w" if w else "f" for w in werte)


def _vis(variablen, ausdruecke, **extra):
    d = {"variablen": list(variablen), "ausdruecke": list(ausdruecke)}
    d.update(extra)
    return ":::visual wahrheitstabelle\n" + json.dumps(d, ensure_ascii=False) + "\n:::"


# ── 1: Aussage ─────────────────────────────────────────────────────────────
k.erklaerung("Was ist eine Aussage?", r"""
    ## Wahr oder falsch, sonst nichts

    :::analogie 🚦 Die Ja-Nein-Frage
    „Ist die Ampel grün?“ hat immer eine klare Antwort: ja oder nein. „Fahr los!“ ist
    dagegen ein Befehl. Darauf kann man nicht mit wahr oder falsch antworten.
    :::

    Ein Ausdruck heißt (mathematische) [[Aussage]], wenn man ihm eindeutig einen
    [[Wahrheitswert]] zuordnen kann: **wahr** (w, auch $1$) oder **falsch** (f, auch $0$).
    Auch eine falsche Aussage ist eine Aussage!

    :::rechnung Beispiele vorgerechnet
    2 + 5 = 7 \quad \text{Aussage, wahr} || man kann es nachrechnen
    1 + 1 = 3 \quad \text{Aussage, falsch} || falsch, aber eindeutig entscheidbar
    \text{„Die Zimmertemperatur beträgt 22 Grad.“} \quad \text{Aussage} || zu jedem Zeitpunkt wahr oder falsch
    \text{„Bringe fünf Brötchen mit!“} \quad \text{keine Aussage} || ein Befehl
    \text{„Wie spät ist es?“} \quad \text{keine Aussage} || eine Frage
    :::

    :::alt Mit einem Schalter erklärt
    Eine Aussage ist wie ein Lichtschalter: Er steht entweder auf an (wahr) oder auf aus
    (falsch), nie dazwischen. Ein Befehl oder eine Frage ist gar kein Schalter. Ob du
    den Wert kennst, ist egal: „Am 1. 1. 3000 schneit es in Darmstadt“ ist eine Aussage.
    :::
    ---
    ## Aussageformen: Aussagen mit Lücke

    Enthält ein Ausdruck eine [[Variable]], ist er oft noch nicht wahr oder falsch. Wird
    er nach dem Einsetzen **jedes** Werts aus einer Grundmenge zu einer Aussage, heißt er
    [[Aussageform]].

    :::rechnung Beispiel vorgerechnet: $2x = 6$ mit $x \in \mathbb{R}$
    2 \cdot 3 = 6 || $x = 3$ eingesetzt: wahre Aussage
    2 \cdot 1 = 2 || $x = 1$ eingesetzt: $2 \neq 6$, also falsche Aussage
    :::

    Dagegen ist der Term $x^2 + 3x - 4$ **keine** Aussageform: Auch nach dem Einsetzen
    entsteht nur eine Zahl, kein Satz, der wahr oder falsch ist. Es fehlt ein
    Vergleich wie $=$ oder $<$.

    :::alt Mit einem Lückentext erklärt
    „___ ist die Hauptstadt von Hessen.“ ist ein Lückentext. Erst mit einem Namen wird
    daraus eine Aussage: mit „Wiesbaden“ eine wahre, mit „Darmstadt“ eine falsche. Ein
    Ausdruck wie „$7 + 4x$“ ist dagegen kein Satz, nur ein Rechenausdruck. Egal was du
    einsetzt, heraus kommt eine Zahl, kein wahr oder falsch.
    :::
    """)

k.zuordnen("Ordne jedem Ausdruck zu, was er ist.",
           [("„Frankfurt liegt in Hessen.“", "Aussage, wahr"),
            ("„Alle Vögel können fliegen.“", "Aussage, falsch"),
            ("„$x^2 - 9 = 0$, $x \\in \\mathbb{R}$“", "Aussageform"),
            ("„$5 + 2x$, $x \\in \\mathbb{R}$“", "weder Aussage noch Aussageform")],
           "Frankfurt liegt wirklich in Hessen. Pinguine sind Vögel und können nicht fliegen, also falsch. "
           "$x^2 - 9 = 0$ wird erst durch Einsetzen wahr ($x = 3$) oder falsch. $5 + 2x$ ist ein Term ohne "
           "Vergleich: Es entsteht nie ein wahr oder falsch.",
           tipps=["Frag bei jedem Ausdruck: Kann man direkt wahr oder falsch sagen? Oder erst nach dem Einsetzen? Oder nie?"])

k.mc("Welcher Ausdruck ist **keine** Aussage?",
     ["„Schließ bitte das Fenster!“", "„$3 > 5$“", "„$7$ ist eine Primzahl.“", "„Jede Katze ist schwarz.“"],
     "Ein Befehl kann weder wahr noch falsch sein. $3 > 5$ ist eine falsche Aussage, aber eine Aussage.",
     tipps=["Eine Aussage muss wahr oder falsch sein. Falsch ist erlaubt!", "Suche den Ausdruck, bei dem „wahr“ oder „falsch“ keinen Sinn ergibt."],
     fehler={"„$3 > 5$“": "$3 > 5$ ist falsch, aber eben deshalb eine Aussage: Sie hat den Wahrheitswert f.",
             "„Jede Katze ist schwarz.“": "Das ist eine Aussage mit dem Wahrheitswert falsch. Ein Gegenbeispiel reicht: eine weiße Katze."})

k.wf("„$x + 2 = 5$“ mit $x \\in \\mathbb{R}$ ist eine Aussage.", False,
     "Solange $x$ nicht festgelegt ist, ist das weder wahr noch falsch. Es ist eine **Aussageform**: "
     "Für $x = 3$ wird sie wahr, für jedes andere $x$ falsch.",
     tipps=["Kannst du sofort wahr oder falsch sagen, ohne zu wissen, was $x$ ist?"])

# ── 2: Negation ────────────────────────────────────────────────────────────
k.erklaerung("Die Negation", r"""
    ## „Es stimmt nicht, dass …“

    Die [[Negation]] (Verneinung) einer Aussage $A$ wird $\neg A$ geschrieben, gelesen
    „nicht $A$“. Sie hat immer den **umgekehrten** Wahrheitswert. Eine Tabelle, die für
    alle Fälle die Wahrheitswerte festhält, heißt [[Wahrheitstafel]].

    """ + _vis(["A"], ["¬A"], unterschrift="Ist $A$ wahr, ist $\\neg A$ falsch, und umgekehrt.") + r"""

    :::rechnung Beispiel vorgerechnet
    \text{A: „4 ist durch 2 teilbar.“ (w)} || stimmt
    \text{¬A: „4 ist nicht durch 2 teilbar.“ (f)} || umgekehrter Wert
    \neg(x > 3) \text{ heißt } x \le 3 || das Gegenteil von „größer“ ist „kleiner oder gleich“
    :::

    :::achtung Negation ist nicht das Gegenteil im Alltag
    „Das Auto ist rot.“ wird zu „Das Auto ist **nicht** rot.“, nicht zu „Das Auto ist
    blau.“ Und $\neg(x > 3)$ ist $x \le 3$, nicht $x < 3$: Die $3$ selbst erfüllt
    $x > 3$ nicht, gehört also zur Negation.
    :::

    :::alt Mit einer Mengen-Hälfte erklärt
    Teile alle Möglichkeiten in zwei Hälften: die, in denen $A$ gilt, und **alle
    anderen**. Die Negation ist die ganze zweite Hälfte. Bei $x > 3$ sind das alle
    Zahlen bis einschließlich $3$. „Blau“ wäre nur ein kleiner Teil der Nicht-Rot-Hälfte.
    :::
    """)

k.mc("Wie lautet die Negation von „Das Auto ist rot.“?",
     ["„Das Auto ist nicht rot.“", "„Das Auto ist blau.“", "„Kein Auto ist rot.“", "„Das Auto ist rot und nicht rot.“"],
     "Die Negation sagt nur: Die Aussage stimmt nicht. Welche Farbe das Auto stattdessen hat, bleibt offen.",
     tipps=["Die Negation hat genau den umgekehrten Wahrheitswert.", "Ist ein grünes Auto mit „blau“ erfasst?"],
     fehler={"„Das Auto ist blau.“": "„Blau“ ist nur **eine** Möglichkeit. Ein grünes Auto ist auch nicht rot. "
                                    "Die Negation muss alle anderen Fälle abdecken.",
             "„Kein Auto ist rot.“": "Es geht um **ein** bestimmtes Auto, nicht um alle Autos."})

k.mc("Wie lautet die Negation von $x > 3$ (für $x \\in \\mathbb{R}$)?",
     ["$x \\le 3$", "$x < 3$", "$x \\ge 3$", "$x < -3$"],
     "Für jedes $x$ gilt genau eins von beiden: $x > 3$ oder $x \\le 3$. Die $3$ selbst gehört zur Negation.",
     tipps=["Welche Zahlen erfüllen $x > 3$ **nicht**?", "Prüfe die Zahl $3$: Erfüllt sie $x > 3$?"],
     fehler={"$x < 3$": "Die $3$ fehlt: $3 > 3$ ist falsch, also muss $x = 3$ die Negation erfüllen. Richtig ist $x \\le 3$.",
             "$x \\ge 3$": "$x = 4$ erfüllt sowohl $x > 3$ als auch $x \\ge 3$. Eine Negation muss immer den umgekehrten Wert haben."})

# ── 3: Konjunktion und Disjunktion ────────────────────────────────────────
k.erklaerung("Und und oder", r"""
    ## Konjunktion: $A \land B$

    Die Verknüpfung mit **und** heißt [[Konjunktion]], Zeichen $\land$. Sie ist nur wahr,
    wenn **beide** Teilaussagen wahr sind.

    """ + _vis(["A", "B"], ["A ∧ B"], unterschrift="Nur in der ersten Zeile (beide wahr) ist $A \\land B$ wahr.") + r"""

    :::rechnung Beispiel vorgerechnet
    \text{„4 ist gerade (w) und 4 > 5 (f)“} \quad \text{ist f} || eine Teilaussage ist falsch
    \text{„4 ist gerade (w) und 4 > 3 (w)“} \quad \text{ist w} || beide wahr
    :::

    :::alt Mit einer Tür mit zwei Schlössern erklärt
    Eine Tür hat zwei Schlösser. Sie geht nur auf, wenn Schloss $A$ **und** Schloss $B$
    offen sind. Ist auch nur eins zu, bleibt die Tür zu. In Python: `a and b`.
    :::
    ---
    ## Disjunktion: $A \lor B$

    Die Verknüpfung mit **oder** heißt [[Disjunktion]], Zeichen $\lor$. Sie ist wahr, wenn
    **mindestens eine** Teilaussage wahr ist. Auch wenn beide wahr sind!

    """ + _vis(["A", "B"], ["A ∨ B", "A ⊕ B"],
               unterschrift="$A \\lor B$ ist nur in der letzten Zeile falsch. Daneben XOR: entweder oder.") + r"""

    :::rechnung Beispiel vorgerechnet
    \text{„2 ist gerade (w) oder 2 ist eine Primzahl (w)“} \quad \text{ist w} || beide wahr reicht auch
    \text{„3 ist gerade (f) oder 3 > 5 (f)“} \quad \text{ist f} || keine Teilaussage ist wahr
    :::

    :::achtung Oder heißt nicht entweder oder
    Im Alltag meint „Tee oder Kaffee?“ oft „eins von beiden“. In der Mathematik ist
    $\lor$ auch wahr, wenn beide stimmen. Das ausschließende „entweder oder“ (in der
    Informatik XOR) ist eine andere Verknüpfung.
    :::

    :::alt Mit zwei Lichtschaltern erklärt
    Eine Flurlampe hat zwei Schalter, die parallel geschaltet sind. Sie leuchtet, sobald
    Schalter $A$ **oder** Schalter $B$ an ist, natürlich auch, wenn beide an sind. Nur
    wenn beide aus sind, bleibt es dunkel. In Python: `a or b`.
    :::
    """)

k.wf("Ist $A$ wahr und $B$ falsch, dann ist $A \\land B$ wahr.", False,
     "Eine Konjunktion ist nur wahr, wenn **beide** Teilaussagen wahr sind. Hier ist $B$ falsch, also ist $A \\land B$ falsch.",
     tipps=["Denk an die Tür mit zwei Schlössern."])

k.mc("Welchen Wahrheitswert hat „$2$ ist gerade oder $2$ ist eine Primzahl.“?",
     ["wahr", "falsch"],
     "Beide Teilaussagen sind wahr. Das mathematische „oder“ ist dann wahr. Es schließt den Fall „beide“ nicht aus.",
     tipps=["Bestimme zuerst die Wahrheitswerte der beiden Teilaussagen.", "Wann ist $A \\lor B$ falsch?"],
     fehler={"falsch": "Du hast „oder“ als „entweder oder“ gelesen. In der Mathematik ist $A \\lor B$ auch wahr, "
                       "wenn beide Teilaussagen wahr sind."})

# ── 4: Wahrheitstafeln aufstellen ─────────────────────────────────────────
_F1 = "A ∧ ¬B"
k.erklaerung("Wahrheitstafeln aufstellen", r"""
    ## Alle Fälle systematisch durchgehen

    :::analogie 🧪 Jede Kombination testen
    Ein Softwaretester probiert bei zwei Häkchen in einem Formular alle Kombinationen aus:
    beide an, nur das erste, nur das zweite, keins. Genau das macht eine Wahrheitstafel.
    :::

    So gehst du vor:

    1. Schreibe für jede Grundaussage eine Spalte. Bei $n$ Grundaussagen gibt es $2^n$ Zeilen.
    2. Fülle die Zeilen in fester Reihenfolge: $A$: w, w, f, f und $B$: w, f, w, f.
    3. Füge Spalten für die Teilformeln hinzu, von innen nach außen.
    4. Die letzte Spalte ist die gesuchte Formel.

    """ + _vis(["A", "B"], ["¬B", _F1], markiert=[_F1],
               unterschrift="Erst $\\neg B$, dann $A \\land \\neg B$. Klicke dich Spalte für Spalte durch.") + r"""

    :::rechnung Beispiel vorgerechnet: Zeile $A$ = w, $B$ = f
    \neg B = \neg \text{f} = \text{w} || Negation dreht um
    A \land \neg B = \text{w} \land \text{w} = \text{w} || beide wahr
    :::

    :::alt Mit einem Baum erklärt
    Stell dir einen Entscheidungsbaum vor: Erst teilt sich der Weg bei $A$ in w und f,
    dann jeder Ast bei $B$ wieder in w und f. Am Ende hast du $2 \cdot 2 = 4$ Blätter,
    das sind die vier Zeilen. Bei drei Aussagen teilt sich jedes Blatt nochmal: $8$ Zeilen.
    :::
    ---
    ## Wahrheitswerte ausrechnen

    Kennst du die Werte der Grundaussagen, rechnest du eine Formel wie einen Term aus:
    innen anfangen, Klammern zuerst. Ohne Klammern bindet $\neg$ am stärksten, dann $\land$, dann $\lor$.

    :::rechnung Beispiel: $A$ = w, $B$ = f, $C$ = w
    (A \lor B) \land \neg C || Formel
    = (\text{w} \lor \text{f}) \land \neg \text{w} || Werte einsetzen
    = \text{w} \land \text{f} || Klammer: mindestens eins wahr; Negation von w
    = \text{f} || Konjunktion mit einem f
    :::

    :::alt Wie in Python
    Setze in Python `A, B, C = True, False, True` und tippe
    `(A or B) and not C`. Python rechnet von innen nach außen genauso: `A or B` ist `True`,
    `not C` ist `False`, `True and False` ist `False`.
    :::
    """)

k.zahl("Eine Formel enthält die drei Grundaussagen $A$, $B$ und $C$. Wie viele Zeilen hat ihre Wahrheitstafel?", 2 ** 3,
       "Jede Grundaussage kann w oder f sein: $2 \\cdot 2 \\cdot 2 = 2^3 = 8$ Zeilen.",
       tipps=["Jede Aussage hat zwei mögliche Werte.", "Bei zwei Aussagen sind es $2 \\cdot 2 = 4$ Zeilen.",
              "Bei drei Aussagen: $2 \\cdot 2 \\cdot 2$."],
       rechenweg=r"""
       :::rechnung
       2 \cdot 2 \cdot 2 = 8 || je zwei Möglichkeiten für $A$, $B$ und $C$
       :::
       """,
       typische_fehler=[(6, "$6 = 2 \\cdot 3$. Die Möglichkeiten werden aber **malgenommen**: $2 \\cdot 2 \\cdot 2$."),
                        (3, "Das ist die Zahl der Grundaussagen. Jede davon hat aber zwei Werte.")])

_s = _spalte("¬A ∨ B")
_falsch1 = _spalte("¬A ∧ B")
_falsch2 = _spalte("A ∨ B")
_falsch3 = _spalte("¬(A ∨ B)")
k.mc("Welche Spalte gehört zu $\\neg A \\lor B$? Die Zeilen sind wie üblich ($A$, $B$) = (w, w), (w, f), (f, w), (f, f).",
     [_wf(_s), _wf(_falsch1), _wf(_falsch2), _wf(_falsch3)],
     "Bilde zuerst $\\neg A$: f, f, w, w. Dann „oder“ mit $B$ (w, f, w, f): Nur in der zweiten Zeile sind beide falsch.",
     tipps=["Schreibe zuerst die Spalte $\\neg A$ auf.", "$\\neg A$ = f, f, w, w und $B$ = w, f, w, f.",
            "Eine Disjunktion ist nur falsch, wenn beide Teile falsch sind."],
     fehler={_wf(_falsch1): "Das ist $\\neg A \\land B$. Bei $\\lor$ reicht ein wahrer Teil.",
             _wf(_falsch2): "Du hast die Negation vor $A$ vergessen.",
             _wf(_falsch3): "Das ist $\\neg(A \\lor B)$. Die Negation bezieht sich nur auf $A$."})

k.mc("Es sei $A$ wahr, $B$ falsch und $C$ falsch. Welchen Wahrheitswert hat $A \\land (B \\lor \\neg C)$?",
     ["wahr" if logik_wert(logik_parse("A ∧ (B ∨ ¬C)"), {"A": True, "B": False, "C": False}) else "falsch",
      "falsch" if logik_wert(logik_parse("A ∧ (B ∨ ¬C)"), {"A": True, "B": False, "C": False}) else "wahr"],
     "$\\neg C$ = w, also $B \\lor \\neg C$ = f $\\lor$ w = w. Dann $A \\land$ w = w $\\land$ w = w.",
     tipps=["Fang ganz innen an: Was ist $\\neg C$?", "$\\neg C$ ist w. Was ist dann $B \\lor \\neg C$?"],
     fehler={"falsch": "Hast du $\\neg C$ als f gerechnet? $C$ ist falsch, also ist $\\neg C$ **wahr**."})


# ── Praxis ─────────────────────────────────────────────────────────────────
# Formeln mit typischen Fehlvarianten (Verwechslung ∧/∨, vergessene oder falsch gesetzte Negation)
_FORMELN = [
    ("A ∧ ¬B", [("A ∨ ¬B", "Das ist $A \\lor \\neg B$: ∧ und ∨ verwechselt."),
                ("A ∧ B", "Die Negation vor $B$ fehlt."), ("¬(A ∧ B)", "Die Negation gehört nur vor $B$, nicht vor die ganze Klammer.")]),
    ("¬A ∨ B", [("¬A ∧ B", "∧ und ∨ verwechselt: Bei ∨ reicht ein wahrer Teil."),
                ("A ∨ B", "Die Negation vor $A$ fehlt."), ("¬(A ∨ B)", "Die Negation gehört nur vor $A$.")]),
    ("¬(A ∧ B)", [("¬A ∧ ¬B", "So darf man die Negation nicht in die Klammer ziehen: Aus ∧ wird dabei ∨ (De Morgan)."),
                  ("A ∧ B", "Die Negation vor der Klammer fehlt."), ("¬A ∧ B", "Die Negation gilt für die ganze Klammer.")]),
    ("¬(A ∨ B)", [("¬A ∨ ¬B", "So darf man die Negation nicht in die Klammer ziehen: Aus ∨ wird dabei ∧ (De Morgan)."),
                  ("A ∨ B", "Die Negation vor der Klammer fehlt."), ("¬A ∨ B", "Die Negation gilt für die ganze Klammer.")]),
    ("¬A ∧ ¬B", [("¬A ∨ ¬B", "∧ und ∨ verwechselt."), ("A ∧ ¬B", "Die Negation vor $A$ fehlt."),
                 ("¬(A ∧ B)", "Das ist $\\neg(A \\land B)$, eine andere Formel.")]),
    ("(A ∨ B) ∧ ¬A", [("(A ∧ B) ∧ ¬A", "In der Klammer steht ∨, nicht ∧."), ("(A ∨ B) ∧ A", "Die Negation vor $A$ fehlt."),
                      ("(A ∨ B) ∨ ¬A", "Zwischen Klammer und $\\neg A$ steht ∧.")]),
    ("(A ∧ B) ∨ ¬B", [("(A ∨ B) ∨ ¬B", "In der Klammer steht ∧."), ("(A ∧ B) ∧ ¬B", "Zwischen Klammer und $\\neg B$ steht ∨."),
                      ("(A ∧ B) ∨ B", "Die Negation vor $B$ fehlt.")]),
    ("¬A ∧ B", [("¬A ∨ B", "∧ und ∨ verwechselt."), ("A ∧ B", "Die Negation vor $A$ fehlt."),
                ("¬(A ∧ B)", "Die Negation gilt nur für $A$.")]),
    ("A ∨ (¬A ∧ B)", [("A ∧ (¬A ∧ B)", "Außen steht ∨."), ("A ∨ (A ∧ B)", "Die Negation vor dem zweiten $A$ fehlt."),
                      ("A ∨ (¬A ∨ B)", "In der Klammer steht ∧.")]),
    ("¬(A ∧ ¬B)", [("A ∧ ¬B", "Die äußere Negation fehlt."), ("¬A ∧ B", "Die Negation darf man so nicht in die Klammer ziehen."),
                   ("¬(A ∨ ¬B)", "In der Klammer steht ∧.")]),
    ("(A ∨ ¬B) ∧ B", [("(A ∨ B) ∧ B", "Die Negation vor dem ersten $B$ fehlt."), ("(A ∧ ¬B) ∧ B", "In der Klammer steht ∨."),
                      ("(A ∨ ¬B) ∨ B", "Außen steht ∧.")]),
    ("¬A ∨ ¬B", [("¬A ∧ ¬B", "∧ und ∨ verwechselt."), ("¬(A ∨ B)", "Das ist $\\neg(A \\lor B)$, eine andere Formel."),
                 ("A ∨ ¬B", "Die Negation vor $A$ fehlt.")]),
]


def _teilformeln(ast):
    """Teilformeln von innen nach außen (ohne Variablen), ohne Doppelte."""
    erg = []

    def geh(a):
        if a[0] in ("var", "konst"):
            return
        for kind in a[1:]:
            if isinstance(kind, tuple):
                geh(kind)
        t = logik_tex(a)
        if t not in erg:
            erg.append(t)
    geh(ast)
    return erg


def _als_text(tex):
    """LaTeX einer Formel -> Unicode-Text für die Wahrheitstabelle."""
    for a, b in (("\\neg ", "¬"), ("\\land", "∧"), ("\\lor", "∨"), ("\\Rightarrow", "⇒"), ("\\Leftrightarrow", "⇔"),
                 ("\\oplus", "⊕")):
        tex = tex.replace(a, b)
    return tex


def wahrheitstafel_spalte(rng):
    formel, varianten = rng.choice(_FORMELN)
    if rng.random() < 0.5:                       # Variablennamen tauschen für mehr Vielfalt
        tausch = {"A": "B", "B": "A"}
        formel = "".join(tausch.get(c, c) for c in formel)
        varianten = [("".join(tausch.get(c, c) for c in v), m.replace("$A$", "$X$").replace("$B$", "$A$").replace("$X$", "$B$"))
                     for v, m in varianten]
    ast = logik_parse(formel)
    tex = logik_tex(ast)
    soll = _wf(_spalte(formel))
    optionen, fehler = [soll], {}
    for v, meldung in varianten:
        o = _wf(_spalte(v))
        if o not in optionen:
            optionen.append(o)
            fehler[o] = meldung
    # mit weiteren Spalten auf 4 Optionen auffüllen
    alle = [", ".join(z) for z in itertools.product("wf", repeat=4)]
    rng.shuffle(alle)
    for o in alle:
        if len(optionen) >= 4:
            break
        if o not in optionen:
            optionen.append(o)
    teile = [_als_text(t) for t in _teilformeln(ast)]
    return {
        "typ": "mc",
        "frage": f"Welche Spalte hat die Wahrheitstafel von ${tex}$? Zeilen wie üblich: "
                 "($A$, $B$) = (w, w), (w, f), (f, w), (f, f).",
        "optionen": optionen,
        "fehler": fehler,
        "tipps": ["Stelle die Tafel Spalte für Spalte auf, von innen nach außen.",
                  "Bilde zuerst die Negationen, dann die Klammern.",
                  "$\\land$ ist nur wahr, wenn beide Teile wahr sind; $\\lor$ ist nur falsch, wenn beide falsch sind."],
        "rechenweg": _vis(["A", "B"], teile, markiert=[teile[-1]], schrittweise=False),
        "erklaerung": f"Die letzte Spalte der Tafel ist ${tex}$: {soll}.",
    }


_DREI = ["(A ∨ B) ∧ ¬C", "A ∧ (B ∨ ¬C)", "¬A ∨ (B ∧ C)", "¬(A ∧ B) ∨ C", "(A ∧ ¬B) ∨ (¬A ∧ C)",
         "¬(A ∨ C) ∨ B", "(¬A ∨ ¬B) ∧ C", "A ∨ ¬(B ∨ C)", "(A ∨ ¬C) ∧ (B ∨ C)", "¬(¬A ∧ B) ∧ ¬C"]


def wahrheitswert_auswerten(rng):
    formel = rng.choice(_DREI)
    werte = {v: rng.random() < 0.5 for v in "ABC"}
    ast = logik_parse(formel)
    ergebnis = logik_wert(ast, werte)
    schritte = []

    def geh(a):
        if a[0] == "var":
            return
        for kind in a[1:]:
            if isinstance(kind, tuple):
                geh(kind)
        schritte.append(f"- ${logik_tex(a)}$ ist **{'w' if logik_wert(a, werte) else 'f'}**")
    geh(ast)
    belegung = ", ".join(f"${v}$ = {'w' if werte[v] else 'f'}" for v in "ABC")
    return {
        "typ": "wf",
        "frage": f"Es sei {belegung}. Die Aussage ${logik_tex(ast)}$ ist wahr.",
        "wahr": ergebnis,
        "tipps": ["Rechne von innen nach außen, Negationen zuerst."],
        "rechenweg": "Von innen nach außen:\n\n" + "\n".join(schritte),
        "erklaerung": f"Mit {belegung} hat ${logik_tex(ast)}$ den Wert {'w' if ergebnis else 'f'}.",
    }


k.praxis()

k.generator(wahrheitstafel_spalte, typ="mc", titel="Wahrheitstafel-Spalte bestimmen")
k.generator(wahrheitswert_auswerten, typ="wf", titel="Wahrheitswert ausrechnen")

k.mehrfach("Es sei $A$: „$6$ ist durch $3$ teilbar“ und $B$: „$6$ ist eine Primzahl“. Welche Aussagen sind wahr?",
           ["$A \\lor B$", "$A \\land \\neg B$", "$\\neg B$"],
           ["$A \\land B$", "$\\neg A \\lor B$", "$\\neg (A \\lor B)$"],
           "$A$ ist wahr, $B$ ist falsch ($6 = 2 \\cdot 3$). Damit: $A \\lor B$ = w, $A \\land \\neg B$ = w $\\land$ w = w, "
           "$\\neg B$ = w. Dagegen $A \\land B$ = f, $\\neg A \\lor B$ = f $\\lor$ f = f, $\\neg(A \\lor B)$ = f.",
           tipps=["Bestimme zuerst die Wahrheitswerte von $A$ und $B$.", "$A$ ist w, $B$ ist f. Setze ein."],
           fehler={"$A \\land B$": "Für $\\land$ müssen beide wahr sein. $6$ ist keine Primzahl.",
                   "$\\neg (A \\lor B)$": "$A \\lor B$ ist wahr, also ist die Negation falsch."})

_X = "(A ∨ B) ∧ ¬(A ∧ B)"
_xs = _spalte(_X)
_tabelle = "| $A$ | $B$ | $A \\lor B$ | $A \\land B$ | $\\neg(A \\land B)$ | $(A \\lor B) \\land \\neg(A \\land B)$ |\n|---|---|---|---|---|---|\n"
for _w, _e in zip(itertools.product([True, False], repeat=2), _xs):
    _b = dict(zip("AB", _w))
    _zeile = [_w[0], _w[1], _b["A"] or _b["B"], _b["A"] and _b["B"], not (_b["A"] and _b["B"]), _e]
    _tabelle += "| " + " | ".join("w" if z else "f" for z in _zeile) + " |\n"

k.papier(r"""
    ## Übungsblatt-Stil: Wahrheitstafel aufstellen

    Stellen Sie die Wahrheitstafel der Aussage
    $$(A \lor B) \land \neg(A \land B)$$
    auf. Beschreiben Sie anschließend in einem Satz, wann die Aussage wahr ist.
    """,
    "Spalten von innen nach außen:\n\n" + _tabelle + r"""
    Die Aussage ist genau dann wahr, wenn **genau eine** der beiden Aussagen $A$, $B$ wahr ist.
    Das ist das ausschließende „entweder oder“ (XOR, in Python `a != b` für Wahrheitswerte).
    """,
    ["Meine Tafel hat $4$ Zeilen in der Reihenfolge (w, w), (w, f), (f, w), (f, f)",
     "Ich habe Hilfsspalten für $A \\lor B$, $A \\land B$ und $\\neg(A \\land B)$",
     f"Meine letzte Spalte lautet {_wf(_xs)}",
     "Ich habe erkannt: wahr genau dann, wenn genau eine der Aussagen wahr ist"],
    "Mit Hilfsspalten für jede Teilformel machst du kaum Fehler.",
    uebungsblatt=True,
    tipps=["Lege zuerst die Spalten $A \\lor B$ und $A \\land B$ an."])

k.zusammenfassung(r"""
    ## Aussagen und Wahrheitstafeln

    - **Aussage:** hat eindeutig den Wahrheitswert w (wahr, $1$) oder f (falsch, $0$). Befehle, Fragen und Terme sind keine Aussagen.
    - **Aussageform:** enthält Variablen und wird nach dem Einsetzen zur Aussage, z. B. $2x = 6$.

    | $A$ | $B$ | $\neg A$ | $A \land B$ | $A \lor B$ |
    |---|---|---|---|---|
    | w | w | f | w | w |
    | w | f | f | f | w |
    | f | w | w | f | w |
    | f | f | w | f | f |

    - $\land$ (und, Konjunktion): nur wahr, wenn beide wahr sind.
    - $\lor$ (oder, Disjunktion): wahr, wenn mindestens eine wahr ist, auch beide.
    - Wahrheitstafel mit $n$ Grundaussagen: $2^n$ Zeilen, Teilformeln von innen nach außen.

    !! $\neg(x > 3)$ ist $x \le 3$, nicht $x < 3$.
""")
