# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 2: Logisches Schließen und Beweisformen (Skript Disser WS 26/27, Abschn. 1.3).

Deckt ab: Satz/Theorem/Lemma/Korollar, Beweis, Definition, := (Fußnote 1), Voraussetzung und
Behauptung, die sechs Schlussregeln (Modus ponens, Modus tollens, Elimination, …), Beweis durch
Umformung, direkter Beweis (Def. 1.15, Satz 1.16), Äquivalenzumformung (Beweis von Satz 1.12),
Kontraposition (Satz 1.17), Widerspruch (Satz 1.17 nochmal, Satz 1.18 mit (1.1)),
Fallunterscheidung (Satz 1.19, Satz 1.20). Muster und Schrittnummern wie auf den Folien VL 1.
"""
import itertools
import json

from ..engine import neues_kapitel
from ..visuals import logik_parse, logik_tex, logik_variablen, logik_wert

k = neues_kapitel(
    slug="beweisformen",
    titel="Logisches Schließen und Beweisformen",
    beschreibung="Schlussregeln, direkter Beweis, Äquivalenzumformung, Kontraposition, Widerspruch und Fallunterscheidung nach dem Skript",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 1.3",
    icon="🧩")

k.lernziele([
    "Ich kenne Satz, Theorem, Lemma, Korollar, Definition und das Zeichen $:=$",
    "Ich kann die Schlussregeln (Modus ponens, Modus tollens, Elimination, …) benennen und anwenden",
    "Ich kann direkte Beweise und Beweise durch Kontraposition mit nummerierten, begründeten Schritten aufschreiben",
    "Ich kann einen Widerspruchsbeweis führen und weiß, welche Annahme ich dabei mache",
    "Ich kann eine Fallunterscheidung so wählen, dass sie alle Möglichkeiten abdeckt (Satz 1.19)",
])

k.warum(r"""
In der Zwischenprüfung und in den Quizzen musst du kurze Beweise selbst aufschreiben. Die fünf
Beweisformen dieses Kapitels sind die Werkzeuge dafür, und sie tauchen in der Informatik ständig
auf: Korrektheitsbeweise von Algorithmen, Invarianten von Schleifen, die Unentscheidbarkeit des
Halteproblems (ein Widerspruchsbeweis) und jede Fallunterscheidung in einem `if`/`else`. Wer die
Muster kennt, weiß bei jeder Aufgabe, womit er anfangen darf und wo er ankommen muss.
""")


def _vis(variablen, ausdruecke, einr="    ", **extra):
    """Wahrheitstabellen-Visual; einr = Einrückung des umgebenden Texts."""
    d = {"variablen": list(variablen), "ausdruecke": list(ausdruecke)}
    d.update(extra)
    return ":::visual wahrheitstabelle\n" + einr + json.dumps(d, ensure_ascii=False) + "\n" + einr + ":::"


def _tautologie(formel):
    ast = logik_parse(formel)
    vs = sorted(logik_variablen(ast))
    return all(logik_wert(ast, dict(zip(vs, w))) for w in itertools.product([True, False], repeat=len(vs)))


# Die Schlussregeln als Tautologien (Python prüft beim Laden)
_REGELN_FORMEL = ["(P ∧ (P ⇒ Q)) ⇒ Q", "((P ⇒ Q) ∧ ¬Q) ⇒ ¬P", "((P ∨ Q) ∧ ¬P) ⇒ Q"]
assert all(_tautologie(f) for f in _REGELN_FORMEL)
_FALL = "((P ⇒ R) ∧ (Q ⇒ R)) ⇒ ((P ∨ Q) ⇒ R)"
assert _tautologie(_FALL)                                         # Satz 1.19
assert _tautologie("(P ⇒ Q) ⇔ (¬P ∨ Q)") and _tautologie("¬(P ⇒ Q) ⇔ (P ∧ ¬Q)")

# ── 1: Satz, Beweis, Schlussregeln ───────────────────────────────────────────
k.erklaerung("Satz, Beweis und Schlussregeln", r"""
    ## Was ist ein Satz, was ein Beweis?

    Ein [[Satz]] ist eine mathematische Aussage, oft eine Implikation oder Äquivalenz, deren
    Gültigkeit nachgewiesen ist oder werden kann. Ein [[Beweis]] ist der zweifelsfreie, schriftliche
    Nachweis. Er muss für jeden überzeugend sein, der die Begriffe kennt. Darum legt eine
    [[Definition]] die genaue Bedeutung jedes Begriffs fest.

    :::rechnung Die Wörter im Skript
    \text{Theorem} || besonders wichtiger Satz ([[Theorem]])
    \text{Lemma} || Hilfssatz, Baustein für einen größeren Beweis
    \text{Korollar} || unmittelbare Konsequenz eines Satzes
    c := a + b || „$c$ ist definiert als $a + b$“: [[definierendes Gleichheitszeichen]]
    P \Rightarrow Q: \ P \text{ Voraussetzung}, \ Q \text{ Behauptung} || [[Voraussetzung]] und [[Behauptung]]
    :::

    Um $P \Rightarrow Q$ zu beweisen, **nehmen wir an, dass $P$ gilt**, und zeigen damit $Q$.
    Den Fall „$P$ falsch“ brauchen wir nicht: Dann ist die Implikation ohnehin wahr
    ([[ex falso quodlibet]]). Eine Äquivalenz zeigst du als zwei Implikationen.

    :::alt Mit einem Kochrezept erklärt
    Die Voraussetzung sind die Zutaten, die du auf den Tisch legen darfst. Die Behauptung ist das
    fertige Gericht. Der Beweis ist das Rezept: jeder Schritt nachvollziehbar, keine Zutat aus dem
    Nichts. Hast du die Zutaten nicht (Voraussetzung falsch), verspricht das Rezept nichts.
    :::
    ---
    ## Die logischen Schlussregeln

    Ein Beweis ist eine Kette erlaubter Schlüsse. Die üblichsten ([[Schlussregeln|Schlussregel]]):

    :::rechnung Sechs Regeln aus dem Skript
    P, \ (P \Rightarrow Q) \ \text{ergeben} \ Q || [[Modus ponens]]: Implikation nutzen
    (P \Rightarrow Q), \ \neg Q \ \text{ergeben} \ \neg P || [[Modus tollens]]: Kontraposition nutzen
    (P \lor Q), \ \neg P \ \text{ergeben} \ Q || [[Elimination|Elimination (Schlussregel)]]: einen Fall ausschließen
    P, \ Q \ \text{ergeben} \ P \land Q || Und bilden
    P \land Q \ \text{ergibt} \ P \ \text{(und } Q \text{)} || Und zerlegen
    P \ \text{ergibt} \ P \lor Q || Oder bilden: „Lea liest. Also liest oder schreibt Lea.“
    :::

    Jede Regel ist eine [[Tautologie]], wie die Tabelle für die ersten drei zeigt:

    """ + _vis(["P", "Q"], _REGELN_FORMEL, schrittweise=False,
               unterschrift="Jede Spalte ist in allen Zeilen wahr.") + r"""

    :::alt Mit einem Detektiv erklärt
    Modus ponens: „Wer den Schlüssel hat, war im Raum. Anna hat den Schlüssel. Also war Anna im
    Raum.“ Modus tollens: „Anna war nicht im Raum. Also hat sie den Schlüssel nicht.“ Elimination:
    „Es war Anna oder Ben. Anna war es nicht. Also Ben.“
    :::
    """)

k.mc("Im Skript wird ein Hilfssatz bewiesen, den man nur braucht, um später einen größeren Satz zu zeigen. "
     "Wie heißt so ein Satz?",
     ["Lemma", "Korollar", "Theorem", "Definition"],
     "Lemma = Hilfssatz. Ein Korollar folgt unmittelbar aus einem Satz, ein Theorem ist ein besonders wichtiger Satz. "
     "Eine Definition ist gar kein Satz: Sie wird nicht bewiesen, sondern legt eine Bedeutung fest.",
     tipps=["Hilfssatz, unmittelbare Konsequenz, besonders wichtig: Welches Wort passt zu welchem?",
            "Das Wort stammt aus dem Griechischen und bedeutet „Annahme“ oder „Stichwort“."],
     fehler={"Korollar": "Ein Korollar kommt **nach** einem Satz als unmittelbare Folgerung, nicht davor als Werkzeug.",
             "Definition": "Eine Definition wird nicht bewiesen. Sie legt nur fest, was ein Begriff bedeutet."})

k.wf("Im Skript bedeuten „$c := a + b$“ und „$c = a + b$“ dasselbe.", False,
     "Fußnote 1 im Skript: $:=$ definiert ein neues Symbol (links steht, was erst jetzt einen Namen bekommt). "
     "$=$ drückt die Gleichheit bereits definierter Ausdrücke aus, also eine Aussage, die wahr oder falsch sein kann.",
     tipps=["Bei welchem Zeichen ist $c$ vorher schon bekannt?"])

k.zuordnen("Ordne jedem Schluss den Namen der Schlussregel zu.",
           [("Aus P und (P ⇒ Q) folgt Q.", "Modus ponens"),
            ("Aus (P ⇒ Q) und ¬Q folgt ¬P.", "Modus tollens"),
            ("Aus (P ∨ Q) und ¬P folgt Q.", "Elimination"),
            ("Aus P ∧ Q folgt P.", "Und zerlegen"),
            ("Aus P folgt P ∨ Q.", "Oder bilden")],
           "Modus ponens nutzt eine Implikation vorwärts, Modus tollens rückwärts über die Kontraposition (Satz 1.12), "
           "die Elimination schließt einen Fall eines Oder aus.",
           ablenker=["Und bilden", "kein gültiger Schluss"],
           tipps=["„Ponens“ heißt setzend (man setzt $P$), „tollens“ heißt aufhebend (man hebt $Q$ auf)."])

k.mc("Du willst $P \\Rightarrow Q$ beweisen und beginnst mit „Es gelte $P$.“ Warum darfst du das?",
     ["Ist $P$ falsch, ist $P \\Rightarrow Q$ ohnehin wahr. Nur der Fall „$P$ wahr“ muss untersucht werden.",
      "Weil $P$ in jedem Satz wahr ist.",
      "Weil man in einem Beweis alles annehmen darf, was man braucht.",
      "Weil $P$ und $Q$ äquivalent sind."],
     "Die Wahrheitstabelle der Implikation hat nur eine falsche Zeile: $P$ wahr, $Q$ falsch. "
     "Also genügt es, unter der Annahme $P$ zu zeigen, dass $Q$ gilt.",
     tipps=["Schau dir die Zeilen der Tabelle für $P \\Rightarrow Q$ an, in denen $P$ falsch ist.",
            "In diesen Zeilen ist die Implikation immer wahr. Was bleibt also zu prüfen?"],
     fehler={"Weil $P$ in jedem Satz wahr ist.":
             "Nein, $P$ kann falsch sein. Dann sagt der Satz nichts, ist aber trotzdem wahr (ex falso quodlibet).",
             "Weil man in einem Beweis alles annehmen darf, was man braucht.":
             "Gerade nicht: Die Behauptung $Q$ darfst du nie annehmen. Nur die Voraussetzung."})

# ── 2: Direkter Beweis ───────────────────────────────────────────────────────
k.erklaerung("Direkter Beweis", r"""
    ## Definition 1.15 und Satz 1.16

    Aus der Schule kennst du den Beweis durch Umformung: eine Kette von Gleichungen. Der
    [[direkte Beweis|direkter Beweis]] ist dasselbe mit Implikationen: Voraussetzung annehmen,
    Schritt für Schritt bis zur Behauptung schließen.

    **Definition 1.15.** Eine Zahl $n$ heißt [[gerade|gerade Zahl]], wenn eine ganze Zahl $a$ existiert mit
    $n = 2a$, und ungerade, wenn eine ganze Zahl $a$ existiert mit $n = 2a + 1$. Jede ganze Zahl ist
    entweder gerade oder ungerade, aber nicht beides. Beispiel: $4 = 2 \cdot 2$, $5 = 2 \cdot 2 + 1$.

    **Satz 1.16.** Sind $n, m$ gerade Zahlen, dann ist $n + m$ gerade.

    :::rechnung Beweis (direkt), nummeriert wie auf den Folien
    (1)\ \text{Wir nehmen an, } n \text{ und } m \text{ seien gerade.} || Voraussetzung annehmen
    (2)\ \text{Nach (1): } n = 2b,\ m = 2c \text{ mit ganzen } b, c || Definition 1.15, **zwei** verschiedene Namen
    2b + 2c = 2(b + c) || (3): aus (2) eingesetzt, $2$ ausgeklammert
    (4)\ \text{Nach (2) ist } b + c \text{ ganz.} || Summe ganzer Zahlen
    (5)\ \text{Nach (3), (4): } n + m = 2(b + c) \text{ ist gerade.} \ \square || Definition 1.15, Behauptung erreicht
    :::

    !! Muster: Voraussetzung annehmen, Behauptung herleiten.

    :::alt Mit einer Gleichung erklärt
    Gerade sein heißt: „Ich bin $2$ mal irgendeine ganze Zahl.“ $n$ zeigt seinen Ausweis $2b$, $m$
    zeigt $2c$. Zusammen sind sie $2b + 2c$. Klammere die $2$ aus, und du hast einen neuen Ausweis:
    $2 \cdot (b + c)$. Mehr braucht die Definition nicht.
    :::
    """)

k.ordnen("Bringe den direkten Beweis von Satz 1.16 („Sind $n, m$ gerade, so ist $n + m$ gerade.“) in die richtige "
         "Reihenfolge. Nicht jeder Schritt gehört hinein.",
         ["(1) Wir nehmen an, $n$ und $m$ seien gerade.",
          "(2) Nach (1) und Definition 1.15 gibt es ganze Zahlen $b, c$ mit $n = 2b$ und $m = 2c$.",
          "(3) Nach (2) gilt $n + m = 2b + 2c = 2(b + c)$.",
          "(4) Nach (2) ist $b + c$ eine ganze Zahl.",
          "(5) Nach (3) und (4) ist $n + m$ nach Definition 1.15 gerade. $\\square$"],
         "Erst die Voraussetzung, dann die Definition auspacken, rechnen, Ganzzahligkeit begründen und mit der Definition "
         "wieder einpacken. Mit demselben $a$ für $n$ und $m$ hättest du nur $n = m$ bewiesen.",
         ablenker=["Nach (1) gibt es eine ganze Zahl $a$ mit $n = 2a$ und $m = 2a$.",
                   "Wir nehmen an, $n + m$ sei gerade."],
         tipps=["Womit fängt ein direkter Beweis an?", "Beachte: $n$ und $m$ sind verschiedene Zahlen, sie brauchen verschiedene Hilfszahlen."])

# ── 3: Äquivalenzumformung, Kontraposition, Widerspruch ─────────────────────
k.erklaerung("Äquivalenzumformung, Kontraposition, Widerspruch", r"""
    ## Beweis durch Äquivalenzumformung

    Eine Äquivalenz $P \Leftrightarrow Q$ zeigst du durch eine Kette $P \Leftrightarrow R_1
    \Leftrightarrow \cdots \Leftrightarrow Q$. Jede Umformung muss in **beiden** Richtungen gelten.
    So beweist das Skript das [[Kontrapositionsgesetz]] (Satz 1.12) noch einmal:

    :::rechnung Beweis von Satz 1.12
    (P \Rightarrow Q) \Leftrightarrow (\neg P \lor Q) || Wahrheitstabelle: gleiche Spalten (siehe unten)
    \Leftrightarrow (Q \lor \neg P) || bei $\lor$ ist die Reihenfolge egal
    \Leftrightarrow (\neg(\neg Q) \lor \neg P) || doppelte Negation: $Q = \neg(\neg Q)$
    \Leftrightarrow (\neg Q \Rightarrow \neg P) || erste Zeile rückwärts, mit $\neg Q$ statt $P$ und $\neg P$ statt $Q$
    :::

    """ + _vis(["P", "Q"], ["P ⇒ Q", "¬P ∨ Q"], schrittweise=False,
               unterschrift="P ⇒ Q und ¬P ∨ Q haben dieselbe Spalte.") + r"""

    :::alt Mit Übersetzungen erklärt
    Eine Äquivalenzkette ist wie Übersetzen ohne Bedeutungsverlust: Deutsch, Englisch, Französisch,
    zurück. Jede Übersetzung muss sich exakt zurückübersetzen lassen. Eine Umformung, die nur in
    eine Richtung stimmt, darf nicht in der Kette stehen.
    :::
    ---
    ## Beweis durch Kontraposition: Satz 1.17

    Statt $P \Rightarrow Q$ zeigst du $\neg Q \Rightarrow \neg P$ (erlaubt nach Satz 1.12).

    **Satz 1.17.** Für ganze $n$ gilt: Ist $n^2$ gerade, dann ist auch $n$ gerade.

    :::rechnung Beweis (Kontraposition)
    \text{Sei } n \text{ ungerade, also } n = 2a + 1 \text{ mit ganzem } a || $\neg Q$ annehmen, Def. 1.15
    (2a + 1)^2 = 4a^2 + 4a + 1 = 2(2a^2 + 2a) + 1 || binomische Formel, $2$ ausklammern
    \text{Mit } b := 2a^2 + 2a \text{ ganz: } n^2 = 2b + 1 || also ist $n^2$ ungerade: $\neg P$ gezeigt $\square$
    :::

    !! Muster: $\neg Q$ annehmen und $\neg P$ herleiten.

    :::alt Warum nicht direkt?
    Direkt müsstest du aus „$n^2 = 2a$“ etwas über $n$ lernen, also eine Wurzel ziehen. Das führt
    nirgendwohin. Rückwärts ist es leicht: Aus $n$ selbst lässt sich $n^2$ einfach ausrechnen.
    Kontraposition dreht die Aufgabe in die bequeme Richtung.
    :::
    ---
    ## Beweis durch Widerspruch

    Du nimmst an, $P \Rightarrow Q$ gelte **nicht**. Das heißt $P \land \neg Q$ (die einzige falsche
    Zeile). Daraus leitest du etwas Absurdes $C \land \neg C$ her ([[Widerspruchsbeweis]]).

    """ + _vis(["P", "Q"], ["¬(P ⇒ Q)", "P ∧ ¬Q"], schrittweise=False,
               unterschrift="¬(P ⇒ Q) und P ∧ ¬Q sind äquivalent.") + r"""

    :::rechnung Satz 1.17 nochmal (Widerspruch)
    \text{Angenommen, } n^2 \text{ sei gerade, aber } n = 2a + 1 \text{ ungerade} || $P$ und $\neg Q$ annehmen
    (2a + 1)^2 = 2(2a^2 + 2a) + 1 || ausrechnen wie oben
    \text{Also ist } n^2 \text{ ungerade, und } n^2 \text{ ist gerade} || $C \land \neg C$ mit $C$: „$n^2$ ist gerade“. $\square$
    :::

    !! Muster: $P$ und $\neg Q$ annehmen, einen Widerspruch $C \land \neg C$ herleiten.

    :::alt Mit einem Krimi erklärt
    Der Verdächtige sagt: „Ich war zu Hause.“ Der Kommissar nimmt das an und folgert: Dann war er
    nicht in der Bar. Aber die Kamera zeigt ihn in der Bar. Beides zugleich geht nicht, also war
    die Annahme falsch. Die Kunst ist, die passende Aussage $C$ (die Bar) zu finden.
    :::
    """)

k.luecke("Im Beweis von Satz 1.17 wird $n^2$ für $n = 2a + 1$ umgeformt. Was gehört in die Lücke?",
         "(2a + 1)^2 = 4a^2 + 4a + 1 = 2(\\luecke) + 1", [["2a^2 + 2a"]],
         "$4a^2 + 4a = 2 \\cdot (2a^2 + 2a)$. Die $+1$ bleibt draußen: Genau sie macht $n^2$ ungerade.",
         tipps=["Klammere aus $4a^2 + 4a$ den Faktor $2$ aus.", "$4a^2 = 2 \\cdot 2a^2$ und $4a = 2 \\cdot 2a$.",
                "In die Lücke gehört $2a^2 + 2a$."],
         rechenweg=r"""
         :::rechnung
         (2a + 1)^2 = 4a^2 + 4a + 1 || binomische Formel
         = 2(2a^2 + 2a) + 1 || $2$ aus den ersten beiden Summanden ausklammern
         :::
         """,
         typische_fehler=[(["4a^2 + 4a"], "Du hast die $2$ vor der Klammer vergessen: $2(4a^2 + 4a) = 8a^2 + 8a$."),
                          (["2a^2 + 2a + 1"], "Die $+1$ steht schon hinter der Klammer. In der Klammer stünde sonst $2 \\cdot 1 = 2$ zu viel.")])

k.mc("Du beweist $P \\Rightarrow Q$ durch Widerspruch. Was nimmst du am Anfang an?",
     ["$P$ und $\\neg Q$", "$\\neg P$ und $Q$", "nur $\\neg Q$", "$\\neg P$ und $\\neg Q$"],
     "$\\neg(P \\Rightarrow Q)$ ist äquivalent zu $P \\land \\neg Q$, der einzigen Zeile, in der die Implikation falsch ist. "
     "Du nimmst also die Voraussetzung an (wie direkt) **und** die Negation der Behauptung (wie bei Kontraposition).",
     tipps=["Wann genau ist $P \\Rightarrow Q$ falsch?", "Schau in die Wahrheitstabelle: Zeile 2."],
     fehler={"nur $\\neg Q$": "Mit nur $\\neg Q$ und dem Ziel $\\neg P$ wäre es ein Beweis durch Kontraposition. "
                               "Beim Widerspruch nimmst du zusätzlich $P$ an und suchst ein $C \\land \\neg C$.",
             "$\\neg P$ und $Q$": "Diese Zeile macht $P \\Rightarrow Q$ wahr, nicht falsch. Angenommen wird das Gegenteil der Implikation."})

k.zuordnen("Ordne jeder Beweisform ihr Muster von den Folien zu.",
           [("Direkter Beweis von P ⇒ Q", "P annehmen, Q herleiten"),
            ("Beweis durch Kontraposition von P ⇒ Q", "¬Q annehmen, ¬P herleiten"),
            ("Widerspruchsbeweis von P ⇒ Q", "P und ¬Q annehmen, C ∧ ¬C herleiten"),
            ("Äquivalenzumformung für P ⇔ Q", "Kette P ⇔ R1 ⇔ … ⇔ Q"),
            ("Fallunterscheidung für (P ∨ Q) ⇒ R", "P ⇒ R und Q ⇒ R zeigen")],
           "Das sind die fünf Muster aus der Zusammenfassung von Vorlesung 1.",
           ablenker=["Q annehmen, P herleiten"],
           tipps=["Was ist bei jeder Form die Annahme am Anfang?"])

# ── 4: Satz 1.18 ─────────────────────────────────────────────────────────────
k.erklaerung("Wurzel 2 ist kein Bruch", r"""
    ## Satz 1.18: $\sqrt{2}$ kann nicht als Bruch dargestellt werden

    Ein Beweis der Pythagoräer, diesmal für eine Aussage ohne Voraussetzung. Wir nehmen das
    Gegenteil an und suchen den Widerspruch. Satz 1.17 ist hier ein Werkzeug, er wird zweimal benutzt.

    :::rechnung Beweis (Widerspruch)
    \text{Angenommen, } \sqrt{2} = \tfrac{n}{m} \text{ mit ganzen } n, m \text{, vollständig gekürzt} || Annahme
    \Rightarrow 2 = \tfrac{n^2}{m^2} \Rightarrow n^2 = 2m^2 \quad (1.1) || quadrieren, mit $m^2$ malnehmen
    \Rightarrow n^2 \text{ gerade} \Rightarrow n \text{ gerade} || Definition 1.15, dann Satz 1.17
    \Rightarrow n = 2a \text{ mit ganzem } a || Definition 1.15
    \Rightarrow 2m^2 = 4a^2 \Rightarrow m^2 = 2a^2 || in (1.1) eingesetzt, durch $2$ geteilt
    \Rightarrow m^2 \text{ gerade} \Rightarrow m \text{ gerade} || Definition 1.15, Satz 1.17
    \Rightarrow \tfrac{n}{m} \text{ lässt sich durch 2 kürzen} || Widerspruch zu „vollständig gekürzt“ $\square$
    :::

    Hier ist $C$: „$\frac{n}{m}$ ist vollständig gekürzt.“ Wir haben $C$ angenommen und $\neg C$ gezeigt.
    Also ist $\sqrt{2}$ eine [[irrationale Zahl]].

    :::alt Mit einem Endlosschleifen-Bild erklärt
    Ohne „vollständig gekürzt“ würde der Beweis sagen: Man kann immer weiter durch $2$ kürzen.
    $\frac{n}{m} = \frac{n/2}{m/2} = \frac{n/4}{m/4} = \ldots$, und das unendlich oft. Ganze Zahlen
    können aber nicht unendlich oft halbiert werden und ganz bleiben. Diese Endlosschleife ist der Widerspruch.
    :::
    """)

k.ordnen("Bringe die Schritte des Beweises von Satz 1.18 ($\\sqrt{2}$ ist kein Bruch) in die richtige Reihenfolge.",
         ["Angenommen, $\\sqrt{2} = \\frac{n}{m}$ mit ganzen Zahlen $n, m$, so weit wie möglich gekürzt.",
          "Dann ist $n^2 = 2m^2$, also $n^2$ gerade und nach Satz 1.17 auch $n$ gerade.",
          "Also $n = 2a$ für eine ganze Zahl $a$, eingesetzt $2m^2 = 4a^2$, also $m^2 = 2a^2$.",
          "Damit ist $m^2$ gerade und nach Satz 1.17 auch $m$ gerade.",
          "Also lässt sich $\\frac{n}{m}$ durch $2$ kürzen: Widerspruch zur Wahl von $n$ und $m$. $\\square$"],
         "Annahme, dann zweimal dasselbe Argument (gerades Quadrat, also gerade Zahl), dann der Widerspruch zur Kürzung.",
         ablenker=["Also ist $n$ ungerade, weil $n^2 = 2m^2$ gilt.", "Dann ist $\\sqrt{2} = 1{,}41$, also kein Bruch."],
         tipps=["Der Beweis beginnt mit der Annahme des Gegenteils.", "Erst wird $n$ behandelt, dann $m$."])

# ── 5: Fallunterscheidung ────────────────────────────────────────────────────
k.erklaerung("Fallunterscheidung", r"""
    ## Satz 1.19: Fallunterscheidung ist erlaubt

    **Satz 1.19.** Sind $P$, $Q$, $R$ Aussagen, dann gilt
    $$((P \Rightarrow R) \land (Q \Rightarrow R)) \Longrightarrow ((P \lor Q) \Rightarrow R).$$

    """ + _vis(["P", "Q", "R"], [_FALL], schrittweise=False,
               unterschrift="In allen 8 Zeilen wahr: eine Tautologie.") + r"""

    :::rechnung Beweis (Widerspruch), wie im Skript
    \text{Annahme: } P \Rightarrow R,\ Q \Rightarrow R \text{ gelten, } (P \lor Q) \Rightarrow R \text{ nicht} || zum Widerspruch
    \text{Also gelten } P \lor Q \text{ und } \neg R || Wahrheitstabelle der Implikation
    (P \Rightarrow R),\ \neg R \text{ ergeben } \neg P || Modus tollens (Satz 1.12)
    (P \lor Q),\ \neg P \text{ ergeben } Q || Elimination
    Q,\ (Q \Rightarrow R) \text{ ergeben } R || Modus ponens: Widerspruch zu $\neg R$ $\square$
    :::

    Die Fälle müssen **alle Möglichkeiten abdecken**. Sie **dürfen sich überschneiden**.

    :::alt Mit einer Weggabelung erklärt
    Zwei Wege führen ins Dorf $R$: über die Brücke ($P$) oder über den Pass ($Q$). Du weißt, dass
    jeder Wanderer einen der beiden nimmt. Dann kommt jeder im Dorf an. Geht jemand beide Wege, ist
    das egal. Gäbe es aber einen dritten Weg, wüsstest du nichts.
    :::
    ---
    ## Satz 1.20: Ist $n$ ganz, so ist $n(n + 1)$ gerade

    Form: $P \Rightarrow (A \lor B) \Rightarrow Q$ mit $P$: „$n$ ganz“, $A$: „$n$ gerade“,
    $B$: „$n$ ungerade“, $Q$: „$n(n+1)$ gerade“. Nach Satz 1.19 genügen zwei [[Fälle|Fallunterscheidung]].

    :::rechnung Beweis
    \text{Fall 1: } n = 2a \text{ mit ganzem } a || $A$
    2a(2a + 1) = 2(2a^2 + a) || ausmultipliziert, $2$ ausgeklammert: gerade
    \text{Fall 2: } n = 2a + 1 \text{ mit ganzem } a || $B$
    (2a + 1)(2a + 2) = 4a^2 + 4a + 2a + 2 = 2(2a^2 + 3a + 1) || gerade
    \text{In beiden Fällen ist } n(n + 1) \text{ gerade.} \ \square || Satz 1.19
    :::

    :::achtung Fälle vergessen
    „Fall 1: $n > 0$, Fall 2: $n < 0$“ ist **keine** vollständige Fallunterscheidung: $n = 0$ fehlt.
    Prüfe immer, ob jedes Objekt in mindestens einem Fall landet.
    :::

    :::alt Mit Nachbarn erklärt
    $n$ und $n + 1$ sind Nachbarn auf dem Zahlenstrahl. Von zwei Nachbarn ist immer einer gerade.
    Ein Produkt mit einem geraden Faktor ist gerade. Die Fallunterscheidung schreibt genau diese
    Idee sauber auf: Entweder ist $n$ der gerade Nachbar oder $n + 1$.
    :::
    """)

# Zulässige Fallunterscheidungen für "alle ganzen Zahlen n": Python prüft die Abdeckung.
_FAELLE = [
    ("$n$ gerade / $n$ ungerade", lambda n: n % 2 == 0, lambda n: n % 2 == 1),
    ("$n \\ge 0$ / $n \\le 0$", lambda n: n >= 0, lambda n: n <= 0),
    ("$n < 5$ / $n \\ge 2$", lambda n: n < 5, lambda n: n >= 2),
    ("$n > 0$ / $n < 0$", lambda n: n > 0, lambda n: n < 0),
    ("$n$ durch $3$ teilbar / $n$ gerade", lambda n: n % 3 == 0, lambda n: n % 2 == 0),
]
_f_ok = [t for t, a, b in _FAELLE if all(a(n) or b(n) for n in range(-60, 61))]
_f_nein = [t for t, a, b in _FAELLE if not all(a(n) or b(n) for n in range(-60, 61))]
assert len(_f_ok) == 3 and len(_f_nein) == 2
k.mehrfach("Du willst eine Aussage für **alle** ganzen Zahlen $n$ durch zwei Fälle beweisen. Welche Fallunterscheidungen sind zulässig?",
           _f_ok, _f_nein,
           "Zulässig ist eine Fallunterscheidung, wenn jedes $n$ in mindestens einem Fall liegt. Überschneidungen "
           "($n = 0$ bei $n \\ge 0$ / $n \\le 0$, oder $n = 2, 3, 4$ bei $n < 5$ / $n \\ge 2$) sind erlaubt. "
           "Bei $n > 0$ / $n < 0$ fehlt $n = 0$, bei „durch $3$ teilbar / gerade“ fehlt zum Beispiel $n = 1$.",
           tipps=["Suche bei jedem Vorschlag eine ganze Zahl, die in keinem der beiden Fälle liegt.",
                  "Überschneidungen sind kein Problem (Folie: „Sie dürfen sich überschneiden“)."],
           fehler={"$n > 0$ / $n < 0$": "Die Zahl $0$ liegt in keinem Fall. Die Fälle decken nicht alle Möglichkeiten ab.",
                   "$n$ durch $3$ teilbar / $n$ gerade": "$n = 1$ (oder $5$, $7$, …) liegt in keinem Fall."})

k.wf("Bei einer Fallunterscheidung dürfen sich die Fälle überschneiden.", True,
     "Satz 1.19 verlangt nur $P \\lor Q$, also dass mindestens ein Fall eintritt. Gilt $P$ und $Q$ zugleich, ist $R$ eben doppelt gezeigt.",
     tipps=["$P \\lor Q$ ist auch wahr, wenn $P$ und $Q$ beide gelten."])


# ── Praxis ──────────────────────────────────────────────────────────────────
# (P, Q, tauschbar): bei mathematischen Paaren wird nicht getauscht, damit P ⇒ Q inhaltlich stimmt.
_KONTEXTE = [
    ("Lea liest", "Lea schreibt", True),
    ("$n$ ist durch $4$ teilbar", "$n$ ist gerade", False),
    ("Es regnet", "Die Straße ist nass", False),
    ("Der Server läuft", "Die Webseite ist erreichbar", True),
    ("Das Programm terminiert", "Die Ausgabe ist korrekt", True),
    ("$x > 3$", "$x^2 > 9$", False),
]
# (Prämissen, Schluss, Regelname oder None). Gültigkeit prüft Python per Wahrheitstabelle.
_SCHLUESSE = [
    (["P", "P ⇒ Q"], "Q", "Modus ponens"),
    (["P ⇒ Q", "¬Q"], "¬P", "Modus tollens"),
    (["P ∨ Q", "¬P"], "Q", "Elimination"),
    (["P", "Q"], "P ∧ Q", "Und bilden"),
    (["P ∧ Q"], "Q", "Und zerlegen"),
    (["P"], "P ∨ Q", "Oder bilden"),
    (["P ⇒ Q", "Q"], "P", None),
    (["P ⇒ Q", "¬P"], "¬Q", None),
    (["P ∨ Q", "P"], "¬Q", None),
    (["P ∨ Q"], "P", None),
]
_NAMEN = ["Modus ponens", "Modus tollens", "Elimination", "Und bilden", "Und zerlegen", "Oder bilden"]
_KEIN = "kein gültiger Schluss"
for _p, _s, _n in _SCHLUESSE:
    assert _tautologie("(" + " ∧ ".join(f"({x})" for x in _p) + f") ⇒ ({_s})") == (_n is not None)

_FEHL_NAME = {
    "Modus ponens": "Modus ponens braucht $P$ und $P \\Rightarrow Q$ und liefert $Q$.",
    "Modus tollens": "Modus tollens braucht $P \\Rightarrow Q$ und $\\neg Q$ und liefert $\\neg P$.",
    "Elimination": "Die Elimination braucht $P \\lor Q$ und $\\neg P$ und liefert $Q$.",
    "Und bilden": "„Und bilden“ macht aus $P$ und $Q$ die Aussage $P \\land Q$.",
    "Und zerlegen": "„Und zerlegen“ holt aus $P \\land Q$ einen Teil heraus.",
    "Oder bilden": "„Oder bilden“ macht aus $P$ die schwächere Aussage $P \\lor Q$.",
    _KEIN: "Der Schluss ist gültig: Prüfe mit der Wahrheitstabelle, in jeder Zeile mit wahren Voraussetzungen ist auch der Schluss wahr.",
}


def schluss_erkennen(rng):
    praem, schluss, name = rng.choice(_SCHLUESSE)
    p_text, q_text, tauschbar = rng.choice(_KONTEXTE)
    if tauschbar and rng.random() < 0.5:
        p_text, q_text = q_text, p_text
    korrekt = name if name else _KEIN
    andere = [x for x in _NAMEN + [_KEIN] if x != korrekt]
    rng.shuffle(andere)
    optionen = [korrekt] + andere[:3]
    fehler = {o: _FEHL_NAME[o] for o in optionen[1:]}
    if name is None:
        for o in optionen[1:]:
            fehler[o] = ("Der Schluss ist **nicht** gültig. " + _FEHL_NAME[o]) if o != _KEIN else _FEHL_NAME[o]
    praem_tex = ", ".join(f"${logik_tex(logik_parse(x))}$" for x in praem)
    schluss_tex = logik_tex(logik_parse(schluss))
    if name is None:
        vs = ["P", "Q"]
        gegen = next(w for w in itertools.product([True, False], repeat=2)
                     if all(logik_wert(logik_parse(x), dict(zip(vs, w))) for x in praem)
                     and not logik_wert(logik_parse(schluss), dict(zip(vs, w))))
        bel = f"$P$ {'wahr' if gegen[0] else 'falsch'}, $Q$ {'wahr' if gegen[1] else 'falsch'}"
        erkl = (f"Ungültig: Für {bel} sind alle Voraussetzungen wahr, aber ${schluss_tex}$ ist falsch. "
                "Ein gültiger Schluss darf aus wahren Voraussetzungen nie Falsches liefern.")
    else:
        erkl = f"Das ist {name}: Aus {praem_tex} folgt ${schluss_tex}$."
    return {
        "typ": "mc",
        "frage": (f"Es seien $P$: „{p_text}“ und $Q$: „{q_text}“. Aus {praem_tex} wird ${schluss_tex}$ geschlossen. "
                  "Welche Schlussregel ist das?"),
        "optionen": optionen,
        "fehler": fehler,
        "tipps": ["Schau dir zuerst nur die Formeln an, nicht die Sätze.",
                  "Gültig ist ein Schluss genau dann, wenn in jeder Zeile der Wahrheitstabelle mit wahren Voraussetzungen auch der Schluss wahr ist."],
        "erklaerung": erkl,
        "rechenweg": _vis(["P", "Q"], praem + [schluss], einr="", schrittweise=False,
                          unterschrift="Suche die Zeilen, in denen alle Voraussetzungen wahr sind."),
    }


_BUCHSTABEN = [("n", "m", "a", "b"), ("x", "y", "s", "t"), ("k", "l", "u", "v")]


def _paritaet_teile(op, r1, r2, h1, h2):
    """Liefert (Rechenkette als LaTeX, Hilfsterm c als LaTeX, Rest) für (2h1+r1) op (2h2+r2)."""
    f1 = f"2{h1}" + (" + 1" if r1 else "")
    f2 = f"2{h2}" + (" + 1" if r2 else "")
    if op == "+":
        s = r1 + r2
        mitte = f"2{h1} + 2{h2}" + {0: "", 1: " + 1", 2: " + 2"}[s]
        c = f"{h1} + {h2}" + (" + 1" if s == 2 else "")
        rest = s % 2
        kette = f"{mitte} = 2({c})" + (" + 1" if rest else "")
    elif op == "*":
        if (r1, r2) == (0, 0):
            mitte, c = f"4{h1}{h2}", f"2{h1}{h2}"
        elif (r1, r2) == (0, 1):
            mitte, c = f"4{h1}{h2} + 2{h1}", f"2{h1}{h2} + {h1}"
        elif (r1, r2) == (1, 0):
            mitte, c = f"4{h1}{h2} + 2{h2}", f"2{h1}{h2} + {h2}"
        else:
            mitte, c = f"4{h1}{h2} + 2{h1} + 2{h2} + 1", f"2{h1}{h2} + {h1} + {h2}"
        rest = r1 * r2
        a1 = f"({f1})" if r1 else f1
        a2 = f"({f2})" if r2 else f2
        mal = "" if r1 or r2 else " \\cdot "
        kette = f"{a1}{mal}{a2} = {mitte} = 2({c})" + (" + 1" if rest else "")
    else:   # Quadrat
        if r1:
            mitte, c, rest = f"4{h1}^2 + 4{h1} + 1", f"2{h1}^2 + 2{h1}", 1
            kette = f"(2{h1} + 1)^2 = {mitte} = 2({c}) + 1"
        else:
            mitte, c, rest = f"4{h1}^2", f"2{h1}^2", 0
            kette = f"(2{h1})^2 = {mitte} = 2({c})"
    return kette, c, rest


def paritaet_beweis_ordnen(rng):
    n, m, a, b = rng.choice(_BUCHSTABEN)
    op = rng.choice(["+", "*", "*", "+", "q"])
    r1, r2 = rng.randint(0, 1), rng.randint(0, 1)
    wort = {0: "gerade", 1: "ungerade"}
    kette, c, rest = _paritaet_teile(op, r1, r2, a, b)
    if op == "q":
        ausdruck = f"{n}^2"
        satz = f"Ist ${n}$ {wort[r1]}, dann ist ${ausdruck}$ {wort[rest]}."
        vor = f"(1) Wir nehmen an, ${n}$ sei {wort[r1]}."
        defi = f"(2) Nach (1) und Definition 1.15 gibt es eine ganze Zahl ${a}$ mit ${n} = 2{a}" + (" + 1" if r1 else "") + "$."
        abl_def = f"Nach (1) gibt es eine ganze Zahl ${a}$ mit ${n} = 2{a}" + ("$." if r1 else " + 1$.")
    else:
        ausdruck = f"{n} + {m}" if op == "+" else f"{n} \\cdot {m}"
        if r1 == r2:
            satz = f"Sind ${n}$ und ${m}$ {wort[r1]}, dann ist ${ausdruck}$ {wort[rest]}."
            vor = f"(1) Wir nehmen an, ${n}$ und ${m}$ seien {wort[r1]}."
        else:
            satz = f"Ist ${n}$ {wort[r1]} und ${m}$ {wort[r2]}, dann ist ${ausdruck}$ {wort[rest]}."
            vor = f"(1) Wir nehmen an, ${n}$ sei {wort[r1]} und ${m}$ sei {wort[r2]}."
        defi = (f"(2) Nach (1) und Definition 1.15 gibt es ganze Zahlen ${a}, {b}$ mit ${n} = 2{a}" + (" + 1" if r1 else "")
                + f"$ und ${m} = 2{b}" + (" + 1" if r2 else "") + "$.")
        abl_def = (f"Nach (1) gibt es eine ganze Zahl ${a}$ mit ${n} = 2{a}" + (" + 1" if r1 else "")
                   + f"$ und ${m} = 2{a}" + (" + 1" if r2 else "") + "$.")
    schritte = [
        vor, defi,
        f"(3) Nach (2) gilt ${ausdruck} = {kette}$.",
        f"(4) Nach (2) ist ${c}$ eine ganze Zahl.",
        f"(5) Nach (3) und (4) ist ${ausdruck}$ nach Definition 1.15 {wort[rest]}. $\\square$",
    ]
    ablenker = [abl_def, f"Wir nehmen an, ${ausdruck}$ sei {wort[rest]}."]
    return {
        "typ": "ordnen",
        "frage": f"Satz: {satz} Bringe die Schritte des direkten Beweises in die richtige Reihenfolge. Nicht jeder Schritt gehört hinein.",
        "schritte": schritte,
        "ablenker": ablenker,
        "tipps": ["Muster: Voraussetzung annehmen, Behauptung herleiten.",
                  "Die Behauptung darf nie als Annahme auftauchen. Verschiedene Zahlen brauchen verschiedene Hilfszahlen."],
        "erklaerung": (f"Voraussetzung annehmen, Definition 1.15 auspacken, rechnen, Ganzzahligkeit von ${c}$ begründen, "
                       "Definition 1.15 wieder anwenden. Die Ablenker nehmen die Behauptung an oder benutzen für zwei "
                       "verschiedene Zahlen dieselbe Hilfszahl (das beweist nur einen Spezialfall)."),
        "rechenweg": ":::rechnung Die Rechnung aus Schritt (3)\n" + kette + " || ausmultiplizieren, $2$ ausklammern\n:::",
    }


k.praxis()

k.generator(schluss_erkennen, typ="mc", titel="Schlussregel erkennen oder Fehlschluss entlarven")
k.generator(paritaet_beweis_ordnen, typ="ordnen", titel="Direkte Beweise mit gerade/ungerade ordnen")

k.papier(r"""
    ## Übungsblatt-Stil: Kontraposition

    Sei $n$ eine ganze Zahl. Zeigen Sie durch Kontraposition: Ist $3n + 1$ gerade, so ist $n$ ungerade.
    Nummerieren Sie Ihre Beweisschritte und begründen Sie jeden.
    """,
    r"""
**Behauptung in Kontraposition:** Ist $n$ gerade, so ist $3n + 1$ ungerade (Satz 1.12: $\neg Q \Rightarrow \neg P$).

**(1)** Sei $n$ gerade (wir nehmen $\neg Q$ an).

**(2)** Nach (1) und Definition 1.15 gibt es eine ganze Zahl $a$ mit $n = 2a$.

**(3)** Nach (2) gilt $3n + 1 = 6a + 1 = 2(3a) + 1$.

**(4)** Nach (2) ist $b := 3a$ eine ganze Zahl.

**(5)** Nach (3), (4) und Definition 1.15 ist $3n + 1 = 2b + 1$ ungerade ($\neg P$ gezeigt).

Nach dem Kontrapositionsgesetz gilt damit die ursprüngliche Aussage. $\square$
""",
    ["Ich habe die Kontraposition richtig formuliert: $n$ gerade $\\Rightarrow$ $3n + 1$ ungerade",
     "Ich habe Definition 1.15 benutzt, um $n = 2a$ mit ganzem $a$ zu schreiben",
     "Ich habe $3n + 1 = 2(3a) + 1$ gerechnet und begründet, dass $3a$ ganz ist",
     "Ich habe am Ende gesagt, warum daraus die ursprüngliche Aussage folgt (Satz 1.12)"],
    "Kontraposition lohnt sich hier, weil man aus „$n$ gerade“ sofort etwas über $3n + 1$ ausrechnen kann.",
    uebungsblatt=True,
    tipps=["Negiere beide Teile und tausche die Richtung: Was ist $\\neg Q \\Rightarrow \\neg P$?"])

for _n in range(-50, 51):                       # Python prüft die Aussage aus der nächsten Aufgabe
    assert (_n * _n + 3 * _n) % 2 == 0
k.papier(r"""
    ## Übungsblatt-Stil: Fallunterscheidung

    Zeigen Sie: Für jede ganze Zahl $n$ ist $n^2 + 3n$ gerade. Geben Sie an, warum Ihre Fälle alle Möglichkeiten abdecken.
    """,
    r"""
**Beweis.** Sei $n$ eine ganze Zahl. Nach Definition 1.15 ist $n$ gerade oder ungerade, die Fälle decken also alle ganzen Zahlen ab (Satz 1.19).

**Fall 1:** $n$ gerade, also $n = 2a$ mit ganzem $a$. Dann ist
$$n^2 + 3n = 4a^2 + 6a = 2(2a^2 + 3a),$$
und $2a^2 + 3a$ ist ganz. Also ist $n^2 + 3n$ gerade.

**Fall 2:** $n$ ungerade, also $n = 2a + 1$ mit ganzem $a$. Dann ist
$$n^2 + 3n = 4a^2 + 4a + 1 + 6a + 3 = 4a^2 + 10a + 4 = 2(2a^2 + 5a + 2),$$
und $2a^2 + 5a + 2$ ist ganz. Also ist $n^2 + 3n$ gerade.

In beiden Fällen ist $n^2 + 3n$ gerade. $\square$

(Kürzer: $n^2 + 3n = n(n + 3)$, und von $n$ und $n + 3$ ist immer einer gerade.)
""",
    ["Ich habe gesagt, dass jede ganze Zahl gerade oder ungerade ist (Fälle vollständig)",
     "Fall 1 richtig: $4a^2 + 6a = 2(2a^2 + 3a)$",
     "Fall 2 richtig: $(2a+1)^2 + 3(2a+1) = 2(2a^2 + 5a + 2)$",
     "Ich habe in jedem Fall begründet, dass der Ausdruck in der Klammer ganz ist, und mit $\\square$ abgeschlossen"],
    "Das ist dieselbe Struktur wie der Beweis von Satz 1.20.",
    uebungsblatt=True,
    tipps=["Unterscheide $n = 2a$ und $n = 2a + 1$ und rechne jeweils $n^2 + 3n$ aus."])

k.papier(r"""
    ## Übungsblatt-Stil: Widerspruch

    Zeigen Sie durch Widerspruch: Es gibt keine größte ganze Zahl. Benennen Sie die Aussage $C$, für die Sie $C \land \neg C$ herleiten.
    """,
    r"""
**Beweis (Widerspruch).** Angenommen, es gibt eine größte ganze Zahl $g$. Das heißt: $g$ ist ganz, und für jede ganze Zahl $z$ gilt $z \le g$.

Dann ist $z := g + 1$ eine ganze Zahl (Summe ganzer Zahlen). Nach der Annahme gilt $g + 1 \le g$. Abziehen von $g$ liefert $1 \le 0$.

Mit $C$: „$1 \le 0$“ haben wir $C$ hergeleitet. Zugleich gilt $\neg C$, denn $0 < 1$. Das ist der Widerspruch $C \land \neg C$, also war die Annahme falsch. $\square$
""",
    ["Ich habe das Gegenteil sauber formuliert: Es gibt ein ganzes $g$ mit $z \\le g$ für alle ganzen $z$",
     "Ich habe $g + 1$ als ganze Zahl in die Annahme eingesetzt",
     "Ich habe die Aussage $C$ benannt und $C \\land \\neg C$ gezeigt",
     "Ich habe ausdrücklich geschlossen, dass die Annahme falsch ist"],
    "Muster der Folien: Gegenteil annehmen, einen Widerspruch $C \\land \\neg C$ herleiten.",
    uebungsblatt=True,
    tipps=["Wenn $g$ die größte ganze Zahl wäre: Was ist mit $g + 1$?"])

k.zusammenfassung(r"""
    ## Beweisformen (Skript 1.3)

    - **Satz:** bewiesene Aussage. **Theorem:** wichtiger Satz, **Lemma:** Hilfssatz, **Korollar:** unmittelbare Folgerung.
    - $:=$ definiert ein neues Symbol, $=$ vergleicht bekannte Ausdrücke. Beweisende: $\square$.
    - $P \Rightarrow Q$ beweisen: $P$ annehmen (ist $P$ falsch, gilt die Implikation ohnehin), $Q$ herleiten.

    | Schlussregel | aus | folgt |
    |---|---|---|
    | Modus ponens | $P$, $P \Rightarrow Q$ | $Q$ |
    | Modus tollens | $P \Rightarrow Q$, $\neg Q$ | $\neg P$ |
    | Elimination | $P \lor Q$, $\neg P$ | $Q$ |
    | Und bilden / zerlegen, Oder bilden | $P, Q$ / $P \land Q$ / $P$ | $P \land Q$ / $P$ / $P \lor Q$ |

    | Beweisform | Muster |
    |---|---|
    | direkt | Voraussetzung annehmen, Behauptung herleiten |
    | Äquivalenzumformung | $P \Leftrightarrow R_1 \Leftrightarrow \cdots \Leftrightarrow Q$, jeder Schritt in beide Richtungen |
    | Kontraposition | $\neg Q$ annehmen, $\neg P$ herleiten |
    | Widerspruch | $P$ und $\neg Q$ annehmen, $C \land \neg C$ herleiten |
    | Fallunterscheidung | $P \Rightarrow R$ und $Q \Rightarrow R$ zeigen; Fälle decken alles ab, dürfen sich überschneiden |

    !! Def. 1.15: $n$ gerade $:\Leftrightarrow n = 2a$, ungerade $:\Leftrightarrow n = 2a + 1$ (für ein ganzes $a$). Zwei Zahlen brauchen zwei Hilfszahlen.

    - Satz 1.16: gerade + gerade = gerade. Satz 1.17: $n^2$ gerade $\Rightarrow$ $n$ gerade. Satz 1.18: $\sqrt{2}$ ist kein Bruch. Satz 1.20: $n(n + 1)$ ist gerade.
""")
