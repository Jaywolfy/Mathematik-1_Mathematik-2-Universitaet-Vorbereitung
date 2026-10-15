# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 1: Aussagen und logische Verknüpfungen (Skript Disser WS 26/27, Abschn. 1.1–1.2).

Deckt ab: Def. 1.1, Bsp. 1.2, Def. 1.3, Bsp. 1.4, Def. 1.5–1.7, Bem. 1.8 (Kontravalenz),
Bem. 1.9, Def. 1.10, Def. 1.11, ex falso quodlibet (Russell), Satz 1.12 (Kontrapositionsgesetz),
Bsp. 1.13, Satz 1.14 (De Morgan). Alle Wahrheitswerte rechnet Python (visuals.logik_*).
"""
import itertools
import json

from ..engine import neues_kapitel
from ..visuals import logik_parse, logik_tex, logik_variablen, logik_wert

k = neues_kapitel(
    slug="uni_aussagen",
    titel="Aussagen und logische Verknüpfungen",
    beschreibung="Aussage, Aussageform, ¬ ∧ ∨ ⊕ ⇒ ⇔, Wahrheitstabellen, Kontrapositionsgesetz und De Morgan nach dem Skript",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 1.1–1.2",
    icon="🔣")

k.lernziele([
    "Ich kann mit Definition 1.1 und 1.3 entscheiden, ob eine Aussage, eine Aussageform oder keins von beiden vorliegt",
    "Ich kenne die Verknüpfungen $\\neg, \\land, \\lor, \\oplus, \\Rightarrow, \\Leftrightarrow$ (Def. 1.5–1.11) mit ihren Wahrheitstabellen",
    "Ich kann „hinreichend“, „notwendig“ und „ex falso quodlibet“ richtig verwenden",
    "Ich kann das Kontrapositionsgesetz (Satz 1.12) und die Regeln von De Morgan (Satz 1.14) mit einer Wahrheitstabelle beweisen",
    "Ich kann prüfen, ob zwei zusammengesetzte Aussagen äquivalent sind",
])

k.warum(r"""
Jedes `if` in einem Programm prüft eine Aussage. Wer $\neg$, $\land$, $\lor$ und $\Rightarrow$
sicher beherrscht, kann Bedingungen vereinfachen, Kontrollfluss verstehen und später Korrektheit
von Algorithmen beweisen. In der Digitaltechnik sind dieselben Verknüpfungen logische Gatter,
und XOR ($\oplus$) steckt in Prüfsummen und Verschlüsselung. Vor allem aber ist dieses Kapitel
die Sprache, in der das ganze Skript von Prof. Disser geschrieben ist: Jeder Satz dort ist eine
Aussage, meist eine Implikation.
""")


# ── Hilfen (Python rechnet alle Wahrheitswerte) ──────────────────────────────
def _vars(*formeln):
    vs = set()
    for f in formeln:
        vs |= logik_variablen(logik_parse(f))
    return sorted(vs)


def _spalte(formel, variablen):
    ast = logik_parse(formel)
    return [logik_wert(ast, dict(zip(variablen, w)))
            for w in itertools.product([True, False], repeat=len(variablen))]


def _aequivalent(f1, f2):
    vs = _vars(f1, f2)
    return _spalte(f1, vs) == _spalte(f2, vs)


def _tautologie(f):
    return all(_spalte(f, _vars(f)))


def _vis(variablen, ausdruecke, einr="    ", **extra):
    """Visual-Block; einr = Einrückung des umgebenden r\"\"\"…\"\"\"-Texts (sonst wird er zum Codeblock)."""
    d = {"variablen": list(variablen), "ausdruecke": list(ausdruecke)}
    d.update(extra)
    return ":::visual wahrheitstabelle\n" + einr + json.dumps(d, ensure_ascii=False) + "\n" + einr + ":::"


def _tex(formel):
    return logik_tex(logik_parse(formel))


def _wf(b):
    return "w" if b else "f"


def _tafel_md(variablen, ausdruecke):
    """Wahrheitstabelle als Markup-Tabelle (w = wahr, f = falsch), Reihenfolge wie im Skript."""
    kopf = "| " + " | ".join(f"${v}$" for v in variablen) + " | " + " | ".join(f"${_tex(a)}$" for a in ausdruecke) + " |"
    trenn = "|" + "---|" * (len(variablen) + len(ausdruecke))
    zeilen = []
    for w in itertools.product([True, False], repeat=len(variablen)):
        bel = dict(zip(variablen, w))
        werte = list(w) + [logik_wert(logik_parse(a), bel) for a in ausdruecke]
        zeilen.append("| " + " | ".join(_wf(x) for x in werte) + " |")
    return "\n".join([kopf, trenn] + zeilen)


# Prüfungen beim Laden: Was im Skript steht, muss Python bestätigen.
_XOR = ["P ⊕ Q", "¬(P ∧ Q) ∧ ¬(¬P ∧ ¬Q)", "¬(¬P ∨ Q) ∨ ¬(P ∨ ¬Q)"]
assert _aequivalent(_XOR[0], _XOR[1]) and _aequivalent(_XOR[0], _XOR[2])          # Bemerkung 1.9
assert _aequivalent("P ⇒ Q", "¬Q ⇒ ¬P") and not _aequivalent("P ⇒ Q", "¬P ⇒ ¬Q")  # Satz 1.12, Bsp. 1.13
assert _aequivalent("¬(P ∨ Q)", "¬P ∧ ¬Q") and _aequivalent("¬(P ∧ Q)", "¬P ∨ ¬Q")  # Satz 1.14
assert _aequivalent("P ⇔ Q", "(P ⇒ Q) ∧ (Q ⇒ P)")                                  # Definition 1.11


# ── 1: Aussagen und Aussageformen ────────────────────────────────────────────
k.erklaerung("Aussagen und Aussageformen", r"""
    ## Definition 1.1: Aussage

    :::analogie 🧾 Das Behördenformular
    Ein Formular fragt „Wohnsitz in Hessen? Ja / Nein“. Darauf gibt es genau eine richtige
    Antwort, auch wenn der Sachbearbeiter sie noch nicht kennt. „Füllen Sie das Formular aus!“
    kann man dagegen nicht ankreuzen.
    :::

    Eine [[Aussage]] ist ein Satz oder mathematischer Ausdruck, der **entweder eindeutig wahr
    oder eindeutig falsch** ist. Ist sie wahr, sagen wir: Sie **gilt**. Ob wir den
    [[Wahrheitswert]] schon kennen, ist egal.

    :::rechnung Beispiel 1.2 aus dem Skript
    A_1: \text{ Die Zahl 3 ist ungerade.} || Aussage, wahr
    A_2: \text{ } 3 + 5 = 9 || Aussage, falsch
    A_3: \text{ Hat ein Kreis Radius 3, so beträgt seine Fläche } 9\pi. || Aussage, wahr ($\pi r^2$ mit $r = 3$)
    A_4: \text{ Es regnet gerade in Madrid.} || Aussage, Wert unbekannt (aber eindeutig)
    A_5: \text{ Der Himmel ist blau.} || Aussage, wahr
    A_6: \text{ Jede natürliche Zahl ist gerade.} || Aussage, falsch ($1$ ist ungerade)
    A_7: \text{ Jede gerade natürliche Zahl größer 2 ist Summe zweier Primzahlen.} || Aussage, unbekannt (Goldbach-Vermutung)
    \text{Guten Morgen.} \quad \text{Besuchen Sie alle Vorlesungen!} \quad 3x < 8 || keine Aussagen
    :::

    :::achtung $\mathbb{N}$ beginnt im Skript bei $0$
    Prof. Disser setzt $\mathbb{N} = \{0, 1, 2, \ldots\}$, der Vorkurs $\mathbb{N} = \{1, 2, \ldots\}$.
    Lies bei jeder Quelle nach, welche Konvention gilt. Details im Kapitel Mengen.
    :::

    :::alt Mit einem Lichtschalter erklärt
    Eine Aussage ist ein Schalter, der fest auf „an“ (wahr) oder „aus“ (falsch) steht. Vielleicht
    ist der Raum dunkel und du siehst den Schalter nicht (wie bei $A_4$ oder $A_7$): Er steht trotzdem
    auf genau einer Position. Ein Gruß oder ein Befehl ist gar kein Schalter.
    :::
    ---
    ## Definition 1.3: Aussageform

    Eine [[Aussageform]] ist ein Ausdruck mit einer oder mehreren [[Variablen|Variable]], der durch
    **Belegung** der Variablen zu einer Aussage wird. Darum war $3x < 8$ in Beispiel 1.2 keine
    Aussage: $x$ ist nicht belegt.

    :::rechnung Beispiel 1.4 aus dem Skript
    B_1(x): \text{ Die Zahl } x \text{ ist gerade.} || Aussageform mit einer Variablen
    B_1(4) \text{ wahr}, \quad B_1(5) \text{ falsch} || $x = 4$ bzw. $x = 5$ eingesetzt
    B_2(a, b): \ a \le b || zwei Variablen
    B_2(4, 5) \text{ gilt}, \quad B_2(5, 4) \text{ gilt nicht} || Reihenfolge der Belegung zählt
    B_3(r): \text{ Hat ein Kreis Radius } r \text{, so ist seine Fläche } \pi r^2. || eine Variable
    B_3(1) \text{ ist genau die Aussage } B || „Radius 1, Fläche $\pi$“ vom Kapitelanfang
    :::

    !! Aussageform + Belegung = Aussage.

    :::alt Wie eine Funktion in Python
    Eine Aussageform ist wie `def B2(a, b): return a <= b`. Die Funktion selbst ist weder `True`
    noch `False`. Erst der Aufruf `B2(4, 5)` liefert einen Wahrheitswert, hier `True`, und
    `B2(5, 4)` liefert `False`.
    :::
    """)

k.zuordnen("Ordne jeden Ausdruck nach Definition 1.1 und 1.3 ein.",
           [("„$3 + 5 = 9$“", "Aussage, falsch"),
            ("„Die Zahl $3$ ist ungerade.“", "Aussage, wahr"),
            ("„Es regnet gerade in Madrid.“", "Aussage, Wahrheitswert unbekannt"),
            ("„$3x < 8$“", "Aussageform (Variable nicht belegt)"),
            ("„Besuchen Sie möglichst alle Vorlesungen!“", "weder Aussage noch Aussageform")],
           "Eine Aussage muss eindeutig wahr oder falsch sein, bekannt sein muss der Wert nicht. "
           "$3x < 8$ wird erst durch eine Belegung von $x$ zur Aussage. Eine Aufforderung hat nie einen Wahrheitswert.",
           tipps=["Frage dich bei jedem Ausdruck: eindeutig wahr oder falsch? Erst nach dem Einsetzen? Oder nie?"])

k.mc("Die Goldbach-Vermutung $A_7$ aus Beispiel 1.2 lautet: „Jede gerade natürliche Zahl größer $2$ ist die "
     "Summe zweier Primzahlen.“ Ist $A_7$ eine Aussage?",
     ["Ja. Sie ist eindeutig wahr oder falsch, auch wenn bis heute niemand weiß, was davon.",
      "Nein, weil ihr Wahrheitswert unbekannt ist.",
      "Nein, weil sie über unendlich viele Zahlen spricht.",
      "Ja, und sie ist wahr, weil sie für alle bisher getesteten Zahlen stimmt."],
     "Definition 1.1 verlangt nur, dass genau einer der beiden Wahrheitswerte zutrifft. Ob wir ihn kennen, spielt keine Rolle.",
     tipps=["Lies Definition 1.1 genau: Steht dort, dass man den Wert kennen muss?",
            "Vergleiche mit $A_4$ (Regen in Madrid)."],
     fehler={"Nein, weil ihr Wahrheitswert unbekannt ist.":
             "Unbekannt heißt nicht unbestimmt. Wie bei $A_4$ steht der Wert fest, wir kennen ihn nur nicht.",
             "Nein, weil sie über unendlich viele Zahlen spricht.":
             "Auch $A_6$ („Jede natürliche Zahl ist gerade“) spricht über unendlich viele Zahlen und ist eine (falsche) Aussage.",
             "Ja, und sie ist wahr, weil sie für alle bisher getesteten Zahlen stimmt.":
             "Viele Beispiele sind kein Beweis. Ein einziges Gegenbeispiel könnte sie widerlegen. Ihr Wert ist offen."})

k.wf("Für die Aussageform $B_2(a, b)$: $a \\le b$ aus Beispiel 1.4 gilt die Aussage $B_2(5, 4)$.", False,
     "Eingesetzt wird in der Reihenfolge der Variablen: $a = 5$, $b = 4$. Dann steht da $5 \\le 4$, und das ist falsch.",
     tipps=["Setze $a = 5$ und $b = 4$ ein."])

# ── 2: Negation, Konjunktion, Disjunktion, Kontravalenz ─────────────────────
k.erklaerung("Negation, Konjunktion, Disjunktion", r"""
    ## Definitionen 1.5 bis 1.7

    Aus einfachen Aussagen bauen wir neue. Für Aussagen $P$, $Q$:

    :::rechnung Die drei Grundverknüpfungen
    \neg P: \ \text{Die Aussage } P \text{ ist falsch.} || Def. 1.5, [[Negation]] („nicht $P$“)
    P \land Q: \ \text{P ist wahr und Q ist wahr.} || Def. 1.6, [[Konjunktion]] („$P$ und $Q$“)
    P \lor Q: \ \text{P ist wahr oder Q ist wahr.} || Def. 1.7, [[Disjunktion]] („$P$ oder $Q$“)
    \neg A_2: \ \text{Die Aussage } 3 + 5 = 9 \text{ ist falsch.} || Beispiel aus dem Skript: wahr
    :::

    Eine [[Wahrheitstabelle|Wahrheitstafel]] hat für **jede** Kombination der Wahrheitswerte von
    $P$ und $Q$ eine Zeile, bei zwei Aussagen also $4$. Das Skript ordnet die Zeilen immer so:
    (wahr, wahr), (wahr, falsch), (falsch, wahr), (falsch, falsch). Hier steht w für wahr, f für falsch.

    """ + _vis(["P", "Q"], ["¬P", "P ∧ Q", "P ∨ Q"],
               unterschrift="Klicke dich Spalte für Spalte durch.") + r"""

    :::alt Mit Schaltern erklärt
    $P \land Q$ ist eine Lampe hinter zwei hintereinander geschalteten Schaltern: Sie leuchtet nur,
    wenn beide an sind. $P \lor Q$ ist eine Lampe hinter zwei parallelen Schaltern: Ein Schalter
    reicht. $\neg P$ ist ein Schalter, der verkehrt herum eingebaut wurde.
    :::
    ---
    ## Bemerkung 1.8 und 1.9: Kontravalenz und Ausdrückbarkeit

    $P \lor Q$ ist auch wahr, wenn **beide** wahr sind. Die Verknüpfung, die diesen Fall
    ausschließt, heißt [[Kontravalenz]] (exklusives Oder, XOR), Zeichen $P \oplus Q$:
    genau eine der beiden Aussagen gilt.

    Bemerkung 1.9: Jede der $16$ möglichen Verknüpfungen zweier Aussagen lässt sich allein mit
    $\neg$ und $\land$ ausdrücken (oder allein mit $\neg$ und $\lor$). Für XOR:

    """ + _vis(["P", "Q"], _XOR, markiert=[0],
               unterschrift="Alle drei Spalten sind gleich, also beschreiben sie dieselbe Verknüpfung.") + r"""

    :::rechnung Die erste Darstellung gelesen
    \neg(P \land Q) || „nicht beide“
    \neg(\neg P \land \neg Q) || „nicht keins von beiden“, also mindestens eins
    \neg(P \land Q) \land \neg(\neg P \land \neg Q) || zusammen: genau eins, das ist $P \oplus Q$
    :::

    :::alt Mit Zählen erklärt
    Warum $16$? Eine Verknüpfung legt für jede der $4$ Zeilen fest, ob w oder f herauskommt.
    Das sind $2 \cdot 2 \cdot 2 \cdot 2 = 16$ mögliche Ergebnisspalten. $\oplus$ ist die Spalte
    f, w, w, f. In Python ist das für Wahrheitswerte `p != q`.
    :::
    """)

_XOR_KAND = ["¬(P ⇔ Q)", "(P ∨ Q) ∧ ¬(P ∧ Q)", "(P ∧ ¬Q) ∨ (¬P ∧ Q)", "¬P ⊕ ¬Q", "P ∨ Q", "¬(P ∧ Q)", "P ⇔ Q"]
_xr = [f"${_tex(f)}$" for f in _XOR_KAND if _aequivalent(f, "P ⊕ Q")]
_xf = [f"${_tex(f)}$" for f in _XOR_KAND if not _aequivalent(f, "P ⊕ Q")]
assert len(_xr) == 4 and len(_xf) == 3
k.mehrfach("Welche Aussagen haben dieselbe Wahrheitstabelle wie $P \\oplus Q$?", _xr, _xf,
           "$P \\oplus Q$ hat die Spalte f, w, w, f. $\\neg(P \\Leftrightarrow Q)$, „mindestens eins, aber nicht beide“ "
           "und „$P$ ohne $Q$ oder $Q$ ohne $P$“ liefern genau diese Spalte. Auch $\\neg P \\oplus \\neg Q$: "
           "Negiert man beide, bleibt „verschieden“ verschieden. $P \\lor Q$ ist bei (w, w) wahr, $\\neg(P \\land Q)$ bei (f, f).",
           tipps=["Schreibe die Spalte von $P \\oplus Q$ auf: f, w, w, f.",
                  "Prüfe bei jeder Formel nur die Zeilen (w, w) und (f, f): Dort muss f herauskommen."],
           fehler={f"${_tex('P ∨ Q')}$": "Das ist das einschließende Oder (Bemerkung 1.8): Es ist auch wahr, wenn beide gelten.",
                   f"${_tex('¬(P ∧ Q)')}$": "„Nicht beide“ ist auch wahr, wenn keine der beiden gilt. XOR ist dann falsch."})

k.wf("Ist $P$ wahr und $Q$ wahr, dann ist $P \\lor Q$ falsch.", False,
     "Bemerkung 1.8: Die Disjunktion ist auch wahr, wenn beide Teilaussagen gelten. Falsch wäre in dieser Zeile $P \\oplus Q$.",
     tipps=["Erste Zeile der Tabelle für $P \\lor Q$."])

# ── 3: Implikation, Äquivalenz, ex falso ─────────────────────────────────────
k.erklaerung("Implikation und Äquivalenz", r"""
    ## Definition 1.10: Implikation

    :::analogie 🎟️ Das Versprechen
    „Wenn du die Klausur bestehst, bekommst du ein Eis.“ Gebrochen ist das Versprechen nur, wenn
    du bestehst und **kein** Eis bekommst. Fällst du durch, ist es nicht gebrochen, egal was passiert.
    :::

    $P \Rightarrow Q$: Wenn $P$ wahr ist, dann ist auch $Q$ wahr ([[Implikation]]). Sprechweisen
    für $P \Rightarrow Q$: „Aus $P$ folgt $Q$“, „$P$ impliziert $Q$“, „$P$ ist
    [[hinreichende Bedingung]] für $Q$“, „$Q$ ist [[notwendige Bedingung]] für $P$“.

    """ + _vis(["P", "Q"], ["P ⇒ Q"], unterschrift="Nur in Zeile 2 (P wahr, Q falsch) ist die Implikation falsch.") + r"""

    :::rechnung Notwendig und hinreichend an einem Beispiel
    P: \ n \text{ ist durch 4 teilbar}, \quad Q: \ n \text{ ist gerade} || $P \Rightarrow Q$ gilt
    \text{4 teilt } n \text{ ist hinreichend für „} n \text{ gerade“} || es reicht, um $Q$ zu sichern
    \text{„} n \text{ gerade“ ist notwendig für „4 teilt } n \text{“} || ohne $Q$ kein $P$
    n = 6 || gerade, aber nicht durch 4 teilbar: $Q$ ohne $P$ ist erlaubt
    :::

    :::alt Mit Mengen erklärt
    Stell dir alle Fälle vor, in denen $P$ gilt, als kleinen Kreis in einem großen Kreis $Q$.
    Wer im kleinen Kreis steht, steht auch im großen ($P$ hinreichend). Wer nicht im großen Kreis
    steht, kann nicht im kleinen stehen ($Q$ notwendig). Im großen Kreis außerhalb des kleinen zu
    stehen, ist erlaubt.
    :::
    ---
    ## Definition 1.11: Äquivalenz, und ex falso quodlibet

    $P \Leftrightarrow Q$: Die Aussagen $P \Rightarrow Q$ und $Q \Rightarrow P$ sind beide wahr
    ([[Äquivalenz]]). Sprechweisen: „$P$ gilt genau dann, wenn $Q$ gilt“, „$P$ und $Q$ sind
    äquivalent“, „$P$ ist notwendig und hinreichend für $Q$“.

    """ + _vis(["P", "Q"], ["P ⇒ Q", "Q ⇒ P", "P ⇔ Q"],
               unterschrift="P ⇔ Q ist genau dort wahr, wo beide Implikationen wahr sind.") + r"""

    Zeilen 3 und 4 zeigen: Aus einer falschen Aussage folgt jede Aussage, lateinisch
    [[ex falso quodlibet]].

    :::rechnung Russells Beweis, dass er der Papst ist
    0 = 1 \text{ (Annahme)} || falsche Annahme
    1 = 2 \text{ (folgt daraus)} || auf beiden Seiten $1$ addiert
    \text{Russell und der Papst sind 2 Personen, also 1 Person.} || wegen $2 = 1$
    \text{Also ist Russell der Papst.} || Die Implikation ist wahr, die Folgerung trotzdem Unsinn.
    :::

    :::alt Mit dem Versprechen erklärt
    „Wenn $0 = 1$ ist, ist Russell der Papst“ ist ein Versprechen, das nie eingelöst werden muss,
    weil die Bedingung nie eintritt. Ein nie geprüftes Versprechen kann nicht gebrochen werden,
    also gilt es als wahr. Mehr sagt ex falso quodlibet nicht.
    :::
    """)

k.mc("Es gelte $P \\Rightarrow Q$. Welche Sprechweise passt?",
     ["$Q$ ist notwendige Bedingung für $P$.", "$Q$ ist hinreichende Bedingung für $P$.",
      "$P$ ist notwendige Bedingung für $Q$.", "$P$ und $Q$ sind äquivalent."],
     "Ohne $Q$ kein $P$: $Q$ ist notwendig für $P$. Umgekehrt ist $P$ hinreichend für $Q$.",
     tipps=["Hinreichend heißt: reicht aus, um das andere zu sichern.", "Was passiert, wenn $Q$ falsch ist?"],
     fehler={"$Q$ ist hinreichende Bedingung für $P$.":
             "Das wäre $Q \\Rightarrow P$. Aus „$n$ gerade“ folgt nicht „$4$ teilt $n$“ ($n = 6$).",
             "$P$ ist notwendige Bedingung für $Q$.":
             "Auch das wäre $Q \\Rightarrow P$. $Q$ kann ohne $P$ gelten (Zeile 3 der Tabelle)."})

k.mc("In welcher Zeile der Wahrheitstabelle ist $P \\Rightarrow Q$ falsch?",
     ["$P$ wahr, $Q$ falsch", "$P$ falsch, $Q$ wahr", "$P$ falsch, $Q$ falsch", "$P$ wahr, $Q$ wahr"],
     "Definition 1.10 verspricht nur: Wenn $P$ wahr ist, ist $Q$ wahr. Gebrochen ist das nur bei $P$ wahr und $Q$ falsch.",
     tipps=["Denk an das Eis-Versprechen.", "Ist $P$ falsch, gilt die Implikation immer (ex falso quodlibet)."],
     fehler={"$P$ falsch, $Q$ wahr": "Ist $P$ falsch, ist die Implikation wahr: ex falso quodlibet.",
             "$P$ falsch, $Q$ falsch": "Ist $P$ falsch, ist die Implikation wahr, egal was $Q$ ist."})

k.wf("Die Aussage „Wenn $0 = 1$ gilt, dann ist Russell der Papst.“ ist wahr.", True,
     "Die Voraussetzung $0 = 1$ ist falsch. Nach der Wahrheitstabelle ist die Implikation dann wahr (ex falso quodlibet).",
     tipps=["Welchen Wahrheitswert hat $0 = 1$? Schau in Zeile 3 und 4 der Tabelle."])

# ── 4: Kontrapositionsgesetz und De Morgan ───────────────────────────────────
k.erklaerung("Kontrapositionsgesetz und De Morgan", r"""
    ## Satz 1.12: Kontrapositionsgesetz

    Für Aussagen $P$ und $Q$ gilt
    $$(P \Rightarrow Q) \Leftrightarrow ((\neg Q) \Rightarrow (\neg P)).$$

    Beweis: Vergleiche die Spalten. Sie stimmen in allen vier Zeilen überein. $\square$

    """ + _vis(["P", "Q"], ["P ⇒ Q", "¬Q", "¬P", "¬Q ⇒ ¬P", "¬P ⇒ ¬Q"], markiert=[0, 3],
               unterschrift="Spalte P ⇒ Q = Spalte ¬Q ⇒ ¬P. Die letzte Spalte ist anders.") + r"""

    :::rechnung Beispiel 1.13 aus dem Skript
    P: \text{ Jemand im Vorlesungssaal heißt Anna.} || der Saal liegt in Darmstadt
    Q: \text{ Jemand in Darmstadt heißt Anna.} ||
    P \Rightarrow Q \text{ gilt} || eine Anna im Saal ist eine Anna in Darmstadt
    \neg Q \Rightarrow \neg P \text{ gilt} || heißt niemand in Darmstadt Anna, dann auch niemand im Saal
    \neg P \Rightarrow \neg Q \text{ gilt nicht} || eine Anna kann in Darmstadt sein, aber nicht im Saal
    :::

    :::achtung Nur negieren reicht nicht
    Aus $P \Rightarrow Q$ folgt **nicht** $\neg P \Rightarrow \neg Q$ und auch nicht $Q \Rightarrow P$.
    Beim [[Kontrapositionsgesetz]] wird negiert **und** die Richtung getauscht.
    :::

    :::alt Mit Regen erklärt
    „Wenn es regnet, ist die Straße nass.“ Dann gilt auch: „Ist die Straße trocken, hat es nicht
    geregnet.“ Aber „Hat es nicht geregnet, ist die Straße trocken“ stimmt nicht: Ein Wasserrohr
    kann geplatzt sein.
    :::
    ---
    ## Satz 1.14: Die Regeln von De Morgan

    Für Aussagen $P$ und $Q$ gelten ([[Regeln von De Morgan]]):
    $$\neg(P \lor Q) \Leftrightarrow (\neg P) \land (\neg Q) \qquad \neg(P \land Q) \Leftrightarrow (\neg P) \lor (\neg Q)$$

    „Nicht mindestens eines“ heißt „keines von beiden“. „Nicht beide“ heißt „mindestens eines nicht“.
    Den Beweis per Wahrheitstabelle lässt das Skript als Übung, du findest ihn in den Praxisaufgaben.

    """ + _vis(["P", "Q"], ["¬(P ∨ Q)", "¬P ∧ ¬Q", "¬(P ∧ Q)", "¬P ∨ ¬Q"], schrittweise=False,
               unterschrift="Spalte 1 = Spalte 2 und Spalte 3 = Spalte 4.") + r"""

    :::rechnung Negieren mit De Morgan
    \neg(n \text{ ist gerade} \lor n > 5) || Negation einer Disjunktion
    \neg(n \text{ ist gerade}) \land \neg(n > 5) || $\lor$ wird zu $\land$
    n \text{ ist ungerade} \land n \le 5 || jede Teilaussage einzeln negiert
    :::

    :::alt Mit einem Türsteher erklärt
    Der Türsteher lässt rein, wer auf der Liste steht **oder** einen VIP-Pass hat. Wer nicht
    reinkommt, steht nicht auf der Liste **und** hat keinen Pass. Das ist die erste Regel: Das „oder“
    wird beim Verneinen zum „und“.
    :::
    """)

k.mc("Welche Aussage ist nach Satz 1.12 äquivalent zu „Wenn jemand im Saal Anna heißt, dann heißt jemand in Darmstadt Anna.“?",
     ["Wenn niemand in Darmstadt Anna heißt, dann heißt niemand im Saal Anna.",
      "Wenn niemand im Saal Anna heißt, dann heißt niemand in Darmstadt Anna.",
      "Wenn jemand in Darmstadt Anna heißt, dann heißt jemand im Saal Anna.",
      "Jemand im Saal heißt Anna und jemand in Darmstadt heißt Anna."],
     "Kontraposition: $\\neg Q \\Rightarrow \\neg P$. Aus „niemand in Darmstadt“ folgt „niemand im Saal“ (Beispiel 1.13).",
     tipps=["Satz 1.12: $(P \\Rightarrow Q) \\Leftrightarrow (\\neg Q \\Rightarrow \\neg P)$.",
            "Negiere beide Teile **und** tausche die Richtung."],
     fehler={"Wenn niemand im Saal Anna heißt, dann heißt niemand in Darmstadt Anna.":
             "Das ist $\\neg P \\Rightarrow \\neg Q$. Du hast negiert, aber die Richtung nicht getauscht. Es gibt sicher eine Anna in Darmstadt außerhalb des Saals.",
             "Wenn jemand in Darmstadt Anna heißt, dann heißt jemand im Saal Anna.":
             "Das ist die Umkehrung $Q \\Rightarrow P$. Sie ist nicht äquivalent zu $P \\Rightarrow Q$."})

k.mc("Wie lautet die Negation von „$n$ ist gerade oder $n > 5$“ (für eine feste ganze Zahl $n$)?",
     ["$n$ ist ungerade und $n \\le 5$", "$n$ ist ungerade oder $n \\le 5$",
      "$n$ ist ungerade und $n < 5$", "$n$ ist gerade und $n \\le 5$"],
     "De Morgan (Satz 1.14): $\\neg(P \\lor Q) \\Leftrightarrow \\neg P \\land \\neg Q$. Die Negation von $n > 5$ ist $n \\le 5$.",
     tipps=["Satz 1.14: Aus $\\lor$ wird beim Negieren $\\land$.", "Was ist das Gegenteil von $n > 5$? Prüfe $n = 5$."],
     fehler={"$n$ ist ungerade oder $n \\le 5$": "Beim Hineinziehen der Negation kippt $\\lor$ zu $\\land$ (De Morgan).",
             "$n$ ist ungerade und $n < 5$": "Die $5$ fehlt: $5 > 5$ ist falsch, also gehört $n = 5$ zur Negation. Richtig ist $n \\le 5$."})


# ── Praxis ──────────────────────────────────────────────────────────────────
_OPS2 = ["∧", "∨", "⇒", "⇔", "⊕"]


def _zufall_formel(rng, tiefe, variablen):
    if tiefe == 0:
        v = rng.choice(variablen)
        return f"¬{v}" if rng.random() < 0.3 else v
    op = rng.choice(_OPS2)
    a = _zufall_formel(rng, tiefe - 1 if rng.random() < 0.7 else 0, variablen)
    b = _zufall_formel(rng, tiefe - 1 if rng.random() < 0.5 else 0, variablen)
    s = f"({a} {op} {b})"
    return f"¬{s}" if rng.random() < 0.2 else s


def aussage_auswerten(rng):
    while True:
        formel = _zufall_formel(rng, 2, ["P", "Q", "R"])
        ast = logik_parse(formel)
        if len(logik_variablen(ast)) >= 2 and formel.count("(") >= 2:
            break
    werte = {v: rng.random() < 0.5 for v in "PQR"}
    ergebnis = logik_wert(ast, werte)
    schritte = []

    def geh(a):
        if a[0] == "var":
            return
        for kind in a[1:]:
            if isinstance(kind, tuple):
                geh(kind)
        zeile = f"- ${logik_tex(a)}$ ist **{'wahr' if logik_wert(a, werte) else 'falsch'}**"
        if zeile not in schritte:
            schritte.append(zeile)
    geh(ast)
    vs = sorted(logik_variablen(ast))
    belegung = ", ".join(f"${v}$ {'wahr' if werte[v] else 'falsch'}" for v in vs)
    return {
        "typ": "wf",
        "frage": f"Es sei {belegung}. Die Aussage ${logik_tex(ast)}$ ist wahr.",
        "wahr": ergebnis,
        "tipps": ["Rechne von innen nach außen. $\\Rightarrow$ ist nur bei (wahr, falsch) falsch, "
                  "$\\Leftrightarrow$ ist wahr bei gleichen Werten, $\\oplus$ bei verschiedenen."],
        "rechenweg": "Von innen nach außen:\n\n" + "\n".join(schritte),
        "erklaerung": f"Mit {belegung} ist ${logik_tex(ast)}$ {'wahr' if ergebnis else 'falsch'}.",
    }


# Paare: links Muster, rechts Umformung (richtig oder typischer Fehler). Ob sie äquivalent
# sind, entscheidet allein die Wahrheitstabelle (Python), nicht diese Liste.
_PAARE = [
    ("¬(X ∧ Y)", "¬X ∨ ¬Y"), ("¬(X ∨ Y)", "¬X ∧ ¬Y"), ("X ⇒ Y", "¬Y ⇒ ¬X"), ("X ⇒ Y", "¬X ∨ Y"),
    ("¬(X ⇒ Y)", "X ∧ ¬Y"), ("X ⇔ Y", "(X ⇒ Y) ∧ (Y ⇒ X)"), ("X ⊕ Y", "¬(X ⇔ Y)"),
    ("X ∧ (Y ∨ Z)", "(X ∧ Y) ∨ (X ∧ Z)"), ("X ∨ (Y ∧ Z)", "(X ∨ Y) ∧ (X ∨ Z)"),
    ("(X ∨ Y) ⇒ Z", "(X ⇒ Z) ∧ (Y ⇒ Z)"),
    ("¬(X ∧ Y)", "¬X ∧ ¬Y"), ("¬(X ∨ Y)", "¬X ∨ ¬Y"), ("X ⇒ Y", "Y ⇒ X"), ("X ⇒ Y", "¬X ⇒ ¬Y"),
    ("¬(X ⇒ Y)", "¬X ⇒ ¬Y"), ("X ⊕ Y", "X ∨ Y"), ("X ∧ (Y ∨ Z)", "(X ∧ Y) ∨ Z"),
    ("(X ⇒ Y) ⇒ Z", "X ⇒ (Y ⇒ Z)"), ("(X ∨ Y) ⇒ Z", "(X ⇒ Z) ∨ (Y ⇒ Z)"), ("X ⇔ Y", "(X ∧ Y) ∨ (¬X ∧ ¬Y)"),
]


def aequivalenz_pruefen(rng):
    links, rechts = rng.choice(_PAARE)
    namen = ["P", "Q", "R"]
    rng.shuffle(namen)
    ersetzen = {"X": namen[0], "Y": namen[1], "Z": namen[2]}
    if rng.random() < 0.35:                       # ein Platzhalter wird zu einem negierten Buchstaben
        x = rng.choice(["X", "Y"])
        ersetzen[x] = "(¬" + ersetzen[x] + ")"
    f1 = "".join(ersetzen.get(c, c) for c in links)
    f2 = "".join(ersetzen.get(c, c) for c in rechts)
    if rng.random() < 0.5:
        f1, f2 = f2, f1
    vs = _vars(f1, f2)
    s1, s2 = _spalte(f1, vs), _spalte(f2, vs)
    gleich = s1 == s2
    t1, t2 = _tex(f1), _tex(f2)
    if gleich:
        erkl = f"Die Spalten von ${t1}$ und ${t2}$ stimmen in allen ${len(s1)}$ Zeilen überein, also sind die Aussagen äquivalent."
    else:
        i = next(j for j in range(len(s1)) if s1[j] != s2[j])
        zeile = list(itertools.product([True, False], repeat=len(vs)))[i]
        bel = ", ".join(f"${v}$ {'wahr' if w else 'falsch'}" for v, w in zip(vs, zeile))
        erkl = (f"Nicht äquivalent: Für {bel} ist ${t1}$ {'wahr' if s1[i] else 'falsch'}, "
                f"aber ${t2}$ {'wahr' if s2[i] else 'falsch'}. Eine einzige abweichende Zeile genügt.")
    return {
        "typ": "wf",
        "frage": f"Die Aussagen ${t1}$ und ${t2}$ sind äquivalent (sie haben dieselbe Wahrheitstabelle).",
        "wahr": gleich,
        "tipps": ["Stelle die Wahrheitstabelle für beide Aussagen auf oder suche eine Belegung, in der sie sich unterscheiden."],
        "rechenweg": _vis(vs, [f1, f2], einr="", schrittweise=False,
                          unterschrift="Gleiche Spalten bedeuten äquivalent."),
        "erklaerung": erkl,
    }


k.praxis()

k.generator(aussage_auswerten, typ="wf", titel="Zusammengesetzte Aussagen auswerten")
k.generator(aequivalenz_pruefen, typ="wf", titel="Äquivalent oder nicht? (Wahrheitstabelle)")

_TAUT_KAND = ["(P ⇒ Q) ⇔ (¬Q ⇒ ¬P)", "P ∨ ¬P", "(P ∧ ¬P) ⇒ Q", "¬(P ∧ ¬P)",
              "(P ⇒ Q) ⇔ (Q ⇒ P)", "(P ⇒ Q) ⇒ (¬P ⇒ ¬Q)", "P ⊕ ¬P ⊕ Q"]
_tr = [f"${_tex(f)}$" for f in _TAUT_KAND if _tautologie(f)]
_tf = [f"${_tex(f)}$" for f in _TAUT_KAND if not _tautologie(f)]
assert len(_tr) == 4 and len(_tf) == 3
k.mehrfach("Welche Aussagen sind für **alle** Wahrheitswerte von $P$ und $Q$ wahr (also Tautologien)?", _tr, _tf,
           "Satz 1.12 ist eine Tautologie, ebenso „$P$ oder nicht $P$“ und „nicht ($P$ und nicht $P$)“. "
           "$(P \\land \\neg P) \\Rightarrow Q$ ist ex falso quodlibet: Die Voraussetzung ist nie wahr. "
           "Die Umkehrung und die bloße Negation beider Seiten (Bsp. 1.13) sind keine Tautologien. "
           "$P \\oplus \\neg P$ ist immer wahr, danach $\\oplus Q$ ergibt $\\neg Q$.",
           tipps=["Suche bei jeder Aussage eine Belegung, die sie falsch macht. Findest du keine, ist sie eine Tautologie.",
                  "Für $(P \\Rightarrow Q) \\Rightarrow (\\neg P \\Rightarrow \\neg Q)$ probiere $P$ falsch, $Q$ wahr."],
           fehler={f"${_tex('(P ⇒ Q) ⇒ (¬P ⇒ ¬Q)')}$":
                   "Bei $P$ falsch, $Q$ wahr ist $P \\Rightarrow Q$ wahr, aber $\\neg P \\Rightarrow \\neg Q$ falsch (Beispiel 1.13).",
                   f"${_tex('(P ⇒ Q) ⇔ (Q ⇒ P)')}$": "Eine Implikation ist nicht äquivalent zu ihrer Umkehrung."})

_DM = ["¬(P ∨ Q)", "¬P", "¬Q", "¬P ∧ ¬Q", "¬(P ∧ Q)", "¬P ∨ ¬Q"]
k.papier(r"""
    ## Übungsblatt-Stil: De Morgan'sche Regeln

    Beweisen Sie Satz 1.14: Für Aussagen $P$ und $Q$ gelten
    $$\neg(P \lor Q) \Leftrightarrow (\neg P) \land (\neg Q) \quad \text{und} \quad \neg(P \land Q) \Leftrightarrow (\neg P) \lor (\neg Q).$$
    Verwenden Sie eine Wahrheitstabelle mit Hilfsspalten und formulieren Sie den Schluss.
    """,
    "**Beweis.** Seien $P$ und $Q$ Aussagen. Wir stellen die Wahrheitstabelle auf (w = wahr, f = falsch):\n\n"
    + _tafel_md(["P", "Q"], ["P ∨ Q"] + _DM[:4]) + "\n\n" + _tafel_md(["P", "Q"], ["P ∧ Q", "¬(P ∧ Q)", "¬P", "¬Q", "¬P ∨ ¬Q"])
    + r"""

In der ersten Tabelle stimmen die Spalten $\neg(P \lor Q)$ und $\neg P \land \neg Q$ in allen vier Zeilen überein,
in der zweiten die Spalten $\neg(P \land Q)$ und $\neg P \lor \neg Q$. Zwei Aussagen mit gleicher Spalte sind in
jeder Belegung beide wahr oder beide falsch, also gilt jeweils die Äquivalenz. $\square$
""",
    ["Meine Tabellen haben alle $4$ Zeilen in der Reihenfolge des Skripts",
     "Ich habe Hilfsspalten ($P \\lor Q$, $\\neg P$, $\\neg Q$, …) statt im Kopf zu rechnen",
     "Ich habe beide Regeln gezeigt, nicht nur eine",
     "Ich habe den Schluss ausdrücklich formuliert: gleiche Spalten, also äquivalent, mit $\\square$"],
    "Eine Wahrheitstabelle ist ein vollständiger Beweis, weil sie jede mögliche Belegung prüft.",
    uebungsblatt=True,
    tipps=["Baue die Spalten von innen nach außen auf: zuerst $P \\lor Q$, dann die Negation."])

_NU = {"P ⇒ Q": "¬(P ∧ ¬Q)", "P ∨ Q": "¬(¬P ∧ ¬Q)", "P ⇔ Q": "¬(P ∧ ¬Q) ∧ ¬(Q ∧ ¬P)"}
for _a, _b in _NU.items():
    assert _aequivalent(_a, _b)
k.papier(r"""
    ## Übungsblatt-Stil: Bemerkung 1.9

    Drücken Sie $P \Rightarrow Q$, $P \lor Q$ und $P \Leftrightarrow Q$ jeweils nur mit $\neg$ und $\land$ aus.
    Begründen Sie jede Darstellung mit einer Wahrheitstabelle.
    """,
    "Mögliche Darstellungen (andere gleichwertige sind auch richtig):\n\n"
    + "\n".join(f"- ${_tex(a)}$ ist äquivalent zu ${_tex(b)}$" for a, b in _NU.items()) + "\n\n"
    + "Idee: $P \\Rightarrow Q$ ist nur falsch, wenn $P \\land \\neg Q$ gilt. Also ist es die Negation davon. "
      "$P \\lor Q$ ist „nicht keins von beiden“ (De Morgan). $P \\Leftrightarrow Q$ sind zwei Implikationen mit $\\land$.\n\n"
    + _tafel_md(["P", "Q"], list(_NU.keys()) + list(_NU.values()))
    + "\n\nDie Spalten 1 und 4, 2 und 5, 3 und 6 stimmen jeweils überein. $\\square$",
    ["Meine Darstellung von $P \\Rightarrow Q$ benutzt nur $\\neg$, $\\land$ und Klammern",
     "Meine Darstellung von $P \\lor Q$ benutzt nur $\\neg$, $\\land$ und Klammern",
     "Meine Darstellung von $P \\Leftrightarrow Q$ benutzt nur $\\neg$, $\\land$ und Klammern",
     "Ich habe jede Darstellung mit einer vollständigen Wahrheitstabelle geprüft"],
    "Mit diesem Trick lässt sich jede der $16$ Verknüpfungen bauen. In der Digitaltechnik reicht deshalb ein einziger Gattertyp (NAND).",
    uebungsblatt=True,
    tipps=["Wann ist $P \\Rightarrow Q$ falsch? Negiere genau diesen Fall."])

k.zusammenfassung(r"""
    ## Aussagen und logische Verknüpfungen (Skript 1.1–1.2)

    - **Def. 1.1 Aussage:** eindeutig wahr oder falsch (Wert darf unbekannt sein). Wahr heißt: sie gilt.
    - **Def. 1.3 Aussageform:** Ausdruck mit Variablen, wird durch Belegung zur Aussage, z. B. $B_1(4)$.

    | $P$ | $Q$ | $\neg P$ | $P \land Q$ | $P \lor Q$ | $P \oplus Q$ | $P \Rightarrow Q$ | $P \Leftrightarrow Q$ |
    |---|---|---|---|---|---|---|---|
    | w | w | f | w | w | f | w | w |
    | w | f | f | f | w | w | f | f |
    | f | w | w | f | w | w | w | f |
    | f | f | w | f | f | f | w | w |

    - $P \Rightarrow Q$: $P$ hinreichend für $Q$, $Q$ notwendig für $P$. Aus Falschem folgt alles (ex falso quodlibet).
    - Bem. 1.9: Alles geht mit $\neg$ und $\land$ (oder $\neg$ und $\lor$), z. B. $P \oplus Q = \neg(P \land Q) \land \neg(\neg P \land \neg Q)$.

    !! Satz 1.12: $(P \Rightarrow Q) \Leftrightarrow (\neg Q \Rightarrow \neg P)$. Aber $\neg P \Rightarrow \neg Q$ folgt nicht.

    !! Satz 1.14: $\neg(P \lor Q) \Leftrightarrow \neg P \land \neg Q$ und $\neg(P \land Q) \Leftrightarrow \neg P \lor \neg Q$.
""")
