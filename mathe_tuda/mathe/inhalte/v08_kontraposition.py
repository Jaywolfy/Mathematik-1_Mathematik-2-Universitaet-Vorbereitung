# -*- coding: utf-8 -*-
"""Vorkurs 8: Kontraposition und Widerspruchsbeweis – ¬B ⇒ ¬A, A ∧ ¬B ⇒ ⊥, √2 irrational."""
from fractions import Fraction as F

from ..engine import neues_kapitel

# Behauptungen dieses Kapitels, von Python nachgeprüft
for _k in range(-40, 41):
    assert (2 * _k + 1) ** 2 == 2 * (2 * _k * _k + 2 * _k) + 1
    assert (3 * _k + 1) ** 2 == 3 * (3 * _k * _k + 2 * _k) + 1
    assert (3 * _k + 2) ** 2 == 3 * (3 * _k * _k + 4 * _k + 1) + 1
    assert F((2 * _k) ** 3, 2) == (2 * _k) ** 2 * F(2 * _k, 2)
# √2 und √3 haben keine Bruchdarstellung mit kleinem Nenner (Plausibilitätsprobe, kein Beweis)
assert not any(p * p == 2 * q * q or p * p == 3 * q * q for q in range(1, 300) for p in range(1, 600))
# Wahrheitstafel: A ⇒ B gleich ¬B ⇒ ¬A gleich ¬(A ∧ ¬B), aber nicht B ⇒ A
for _a in (True, False):
    for _b in (True, False):
        assert ((not _a) or _b) == ((not (not _b)) or (not _a)) == (not (_a and not _b))
assert any(((not _a) or _b) != ((not _b) or _a) for _a in (True, False) for _b in (True, False))

k = neues_kapitel(
    slug="kontraposition",
    titel="Kontraposition und Widerspruch",
    beschreibung="Zwei indirekte Beweismethoden: ¬B ⇒ ¬A zeigen oder die Annahme A ∧ ¬B zum Widerspruch führen",
    teil="vorkurs",
    quelle="MVK 2026, VL 3",
    icon="🔄")

k.lernziele([
    "Ich kann zu einer Implikation die Kontrapositionsaussage formulieren und sie von der Umkehrung unterscheiden",
    "Ich kann eine Aussage durch Kontraposition beweisen",
    "Ich kann eine Widerspruchsannahme formulieren und einen Widerspruchsbeweis führen",
    "Ich kann den Beweis, dass $\\sqrt{2}$ irrational ist, Schritt für Schritt erklären",
])

k.warum(r"""
Manche Aussagen lassen sich direkt kaum fassen, ihr Gegenteil aber gut. Die
Informatik nutzt das ständig: Dass es kein Programm gibt, das für jedes Programm
entscheidet, ob es anhält (Halteproblem), ist ein Widerspruchsbeweis. Und wer
beim Debuggen sagt „Wäre der Wert positiv, hätte der Test angeschlagen“, denkt
schon in Kontraposition.
""")

# ── 1: Kontraposition ──────────────────────────────────────────────────────
k.erklaerung("Die Kontraposition", r"""
    ## Umdrehen und verneinen

    :::analogie 🌧️ Nasse Straße
    „Wenn es regnet, ist die Straße nass.“ Ist die Straße trocken, weißt du
    sicher: Es regnet nicht. Ist sie nass, weißt du nichts (Wasserrohrbruch?).
    :::

    Zu einer [[Implikation]] $A \Rightarrow B$ gehört die [[Kontraposition]]
    $\neg B \Rightarrow \neg A$. Beide sind immer gleichzeitig wahr oder falsch:

    $$(A \Rightarrow B) \Leftrightarrow (\neg B \Rightarrow \neg A)$$

    :::visual wahrheitstabelle
    {"variablen": ["A", "B"], "ausdruecke": ["A => B", "!B => !A", "B => A"], "markiert": ["A => B", "!B => !A"],
     "unterschrift": "Die ersten beiden Spalten sind gleich. Die Umkehrung $B \\Rightarrow A$ hat eine andere Spalte."}
    :::

    :::achtung Umkehrung ist nicht Kontraposition
    $B \Rightarrow A$ (Umkehrung) und $\neg A \Rightarrow \neg B$ sagen etwas
    **anderes** als $A \Rightarrow B$. Bei der Kontraposition wird vertauscht
    **und** verneint.
    :::

    :::alt Mit einer Eintrittskarte erklärt
    „Wer drin ist, hat eine Karte.“ Gleichwertig: „Wer keine Karte hat, ist nicht
    drin.“ Nicht gleichwertig: „Wer eine Karte hat, ist drin.“ Vielleicht steht er
    noch draußen in der Schlange.
    :::
    """)

_R = ["Wenn ich keinen Regenschirm benutze, dann regnet es nicht.",
      "Wenn ich einen Regenschirm benutze, dann regnet es.",
      "Wenn es nicht regnet, dann benutze ich keinen Regenschirm.",
      "Es regnet und ich benutze keinen Regenschirm."]
k.mc("Was ist die Kontraposition von „Wenn es regnet, dann benutze ich einen Regenschirm“?", _R,
     "$A$: Es regnet. $B$: Ich benutze einen Regenschirm. Kontraposition: $\\neg B \\Rightarrow \\neg A$.",
     tipps=["Benenne $A$ und $B$.", "Vertausche $A$ und $B$ und verneine beide.", "Wenn nicht $B$, dann nicht $A$."],
     fehler={_R[1]: "Das ist die Umkehrung $B \\Rightarrow A$. Sie folgt nicht aus der ursprünglichen Aussage.",
             _R[2]: "Das ist $\\neg A \\Rightarrow \\neg B$: verneint, aber nicht vertauscht.",
             _R[3]: "Das ist $A \\land \\neg B$, die Verneinung der Implikation, also gerade ihr Gegenteil."})

k.wf("Die Aussagen $A \\Rightarrow B$ und $B \\Rightarrow A$ sind gleichwertig.", False,
     "Falsch. $n \\in \\mathbb{N} \\Rightarrow n \\in \\mathbb{Z}$ ist wahr, aber $n \\in \\mathbb{Z} \\Rightarrow n \\in \\mathbb{N}$ "
     "ist falsch ($n = -1$). Gleichwertig zu $A \\Rightarrow B$ ist die Kontraposition $\\neg B \\Rightarrow \\neg A$.",
     tipps=["Teste mit $A$: „$n \\in \\mathbb{N}$“ und $B$: „$n \\in \\mathbb{Z}$“."])

# ── 2: Beweis durch Kontraposition ─────────────────────────────────────────
k.erklaerung("Beweis durch Kontraposition", r"""
    ## Die leichtere Richtung beweisen

    **Satz.** Für alle $n \in \mathbb{Z}$ gilt: Ist $n^2$ gerade, so ist $n$ gerade.

    Direkt ist das schwer: Aus $n^2 = 2k$ folgt nichts Brauchbares für $n$.
    Die Kontrapositionsaussage ist leicht: „Ist $n$ ungerade, so ist $n^2$ ungerade.“

    **Beweis (durch Kontraposition).** Sei $n \in \mathbb{Z}$ ungerade, also
    $n = 2k + 1$ mit $k \in \mathbb{Z}$. Dann gilt:

    :::rechnung
    (2k + 1)^2 = 4k^2 + 4k + 1 || binomische Formel
    = 2(2k^2 + 2k) + 1 || $2$ ausklammern
    :::

    Also ist $n^2$ ungerade. Damit ist die Kontrapositionsaussage gezeigt und mit
    ihr der Satz. $\square$

    :::alt Mit einer Taschenlampe erklärt
    Du suchst im Dunkeln, ob ein Weg vom Ziel zurück zum Start führt. Manchmal
    ist der Rückweg besser beleuchtet. Die Kontraposition ist der Rückweg:
    gleiches Ziel, aber du startest auf der anderen Seite.
    :::
    """)

_K = ["Ist $n$ ungerade, so ist $n^2$ ungerade.", "Ist $n$ gerade, so ist $n^2$ gerade.",
      "Ist $n^2$ ungerade, so ist $n$ ungerade.", "$n^2$ ist gerade und $n$ ist ungerade."]
k.mc("Wie lautet die Kontrapositionsaussage zu „Ist $n^2$ gerade, so ist $n$ gerade“?", _K,
     "$A$: $n^2$ gerade, $B$: $n$ gerade. $\\neg B \\Rightarrow \\neg A$: Ist $n$ ungerade, so ist $n^2$ ungerade.",
     tipps=["$A$ steht nach „Ist“, $B$ nach „so ist“.", "Nicht gerade heißt bei ganzen Zahlen ungerade.",
            "Wenn nicht $B$, dann nicht $A$."],
     fehler={_K[1]: "Das ist die Umkehrung $B \\Rightarrow A$ (vertauscht, aber nicht verneint).",
             _K[2]: "Das ist $\\neg A \\Rightarrow \\neg B$ (verneint, aber nicht vertauscht).",
             _K[3]: "Das ist $A \\land \\neg B$, die Annahme eines Widerspruchsbeweises."})

k.luecke("Für „$3 \\mid n^2 \\Rightarrow 3 \\mid n$“ zeigst du die Kontraposition. Ein Fall: $n = 3k + 1$ mit $k \\in \\mathbb{Z}$. "
         "Ergänze so, dass man sieht: $3 \\nmid n^2$.",
         r"n^2 = (3k + 1)^2 = 9k^2 + 6k + 1 = 3 \cdot \left(\luecke\right) + 1", [["3k^2 + 2k"]],
         "Aus $9k^2 + 6k$ wird die $3$ ausgeklammert. Es bleibt der Rest $1$, also ist $n^2$ nicht durch $3$ teilbar.",
         tipps=["Klammere aus $9k^2 + 6k$ eine $3$ aus.", "$9k^2 = 3 \\cdot 3k^2$ und $6k = 3 \\cdot 2k$.", "$3k^2 + 2k$"],
         rechenweg=r"""
         :::rechnung
         (3k + 1)^2 = 9k^2 + 6k + 1 || binomische Formel
         = 3(3k^2 + 2k) + 1 || $3$ ausklammern
         :::
         """,
         typische_fehler=[(["9k^2 + 6k"], "Du hast die $3$ nicht herausgeteilt: $3 \\cdot (9k^2 + 6k)$ wäre $27k^2 + 18k$."),
                          (["3k^2 + 6k"], "Auch $6k$ muss durch $3$ geteilt werden: $6k = 3 \\cdot 2k$.")])

# ── 3: Formulieren ─────────────────────────────────────────────────────────
k.erklaerung("Kontrapositionsaussagen formulieren", r"""
    ## Richtig verneinen

    Für die Kontraposition musst du $A$ und $B$ sauber verneinen ([[Negation]]):

    | Aussage | Verneinung |
    |---|---|
    | $2 \mid n$ | $2 \nmid n$ |
    | $x > 1$ | $x \le 1$ |
    | $P$ und $Q$ | nicht $P$ oder nicht $Q$ |
    | $P$ oder $Q$ | nicht $P$ und nicht $Q$ |

    Die letzten zwei Zeilen sind die [[Regeln von De Morgan]].

    **Beispiel.** Für $x, y \in \mathbb{R}$: „$x + y > 2 \Rightarrow x > 1$ oder $y > 1$“.
    Kontraposition: „$x \le 1$ und $y \le 1$ $\Rightarrow$ $x + y \le 2$“. Die ist leicht:

    :::rechnung
    x + y \le 1 + 1 = 2 || beide Summanden höchstens $1$
    :::

    :::alt Mit einem Gegenteil-Spiel erklärt
    Frag dich bei jeder Verneinung: Was muss passieren, damit die Aussage
    **nicht** stimmt? „Einer von beiden ist größer als $1$“ stimmt nicht, wenn
    **keiner** größer als $1$ ist, also beide höchstens $1$ sind.
    :::
    """)

_D = ["Wenn $x \\le 1$ und $y \\le 1$, dann $x + y \\le 2$.",
      "Wenn $x \\le 1$ oder $y \\le 1$, dann $x + y \\le 2$.",
      "Wenn $x < 1$ und $y < 1$, dann $x + y < 2$.",
      "Wenn $x > 1$ oder $y > 1$, dann $x + y > 2$."]
k.mc("Kontraposition von „Für $x, y \\in \\mathbb{R}$: Ist $x + y > 2$, so ist $x > 1$ oder $y > 1$“?", _D,
     "Verneinung von „$x > 1$ oder $y > 1$“ ist „$x \\le 1$ und $y \\le 1$“ (De Morgan). Verneinung von $x + y > 2$ ist $x + y \\le 2$.",
     tipps=["Verneine „oder“ mit De Morgan.", "Die Verneinung von $>$ ist $\\le$.", "„oder“ wird zu „und“."],
     fehler={_D[1]: "Bei der Verneinung von „oder“ wird daraus „und“ (De Morgan).",
             _D[2]: "Die Verneinung von $x > 1$ ist $x \\le 1$, nicht $x < 1$. Der Fall $x = 1$ fehlt sonst.",
             _D[3]: "Das ist die Umkehrung. Sie ist sogar falsch: $x = 5$, $y = -10$."})

# ── 4: Widerspruchsbeweis ──────────────────────────────────────────────────
k.erklaerung("Der Widerspruchsbeweis", r"""
    ## Annehmen, dass es schiefgeht

    :::analogie 🕵️ Alibi
    Die Detektivin nimmt an, der Verdächtige war am Tatort. Dann müsste er zur
    selben Zeit in zwei Städten gewesen sein. Unmöglich, also war die Annahme falsch.
    :::

    Beim [[Widerspruchsbeweis]] von $A \Rightarrow B$ nimmst du an: $A$ gilt,
    aber $B$ nicht ([[Widerspruchsannahme]]). Daraus leitest du einen
    [[Widerspruch]] $\bot$ her:

    $$(A \Rightarrow B) \Leftrightarrow \big((A \land \neg B) \Rightarrow \bot\big)$$

    **Satz.** Für alle $n \in \mathbb{N}$: $2 \mid n \Rightarrow 2 \mid n^3$.

    **Beweis.** Sei $n \in \mathbb{N}$. Angenommen, $2 \mid n$, aber $2 \nmid n^3$.
    Dann ist $\frac{n}{2} \in \mathbb{N}$, aber $\frac{n^3}{2} \notin \mathbb{N}$. Doch:

    :::rechnung
    \frac{n^3}{2} = n^2 \cdot \frac{n}{2} || Potenzgesetz; rechts steht natürlich mal natürlich
    :::

    Also $\frac{n^3}{2} \in \mathbb{N}$. Widerspruch! Die Annahme war falsch. $\square$

    :::alt Mit einem Sudoku erklärt
    Du setzt probeweise eine $5$ in ein Feld. Ein paar Züge später stehen zwei
    $5$en in einer Zeile. Das darf nicht sein, also war die $5$ falsch. Genauso
    arbeitet der Widerspruchsbeweis.
    :::
    """)

_A = ["Angenommen, $2 \\mid n$, aber $2 \\nmid n^3$.", "Angenommen, $2 \\nmid n$ und $2 \\mid n^3$.",
      "Angenommen, $2 \\mid n$ und $2 \\mid n^3$.", "Angenommen, $2 \\nmid n^3$."]
k.mc("Wie lautet die Widerspruchsannahme für „Sei $n \\in \\mathbb{N}$. Wenn $2 \\mid n$, dann $2 \\mid n^3$“?", _A,
     "Widerspruchsannahme: $A \\land \\neg B$, also die Voraussetzung gilt, die Behauptung nicht.",
     tipps=["Die Voraussetzung $A$ bleibt erhalten.", "Die Behauptung $B$ wird verneint.", "$A$ und nicht $B$."],
     fehler={_A[1]: "Hier sind beide Teile vertauscht. Die Voraussetzung $2 \\mid n$ bleibt, nur die Behauptung wird verneint.",
             _A[2]: "Das ist genau die Situation, die du zeigen willst. Annehmen musst du das Gegenteil der Behauptung.",
             _A[3]: "Die Voraussetzung $2 \\mid n$ fehlt. Ohne sie kommst du nicht zum Widerspruch."})

# ── 5: √2 ist irrational ───────────────────────────────────────────────────
k.erklaerung("Klassiker: Wurzel 2 ist irrational", r"""
    ## Der berühmteste Widerspruchsbeweis

    **Satz.** $\sqrt{2}$ ist eine [[irrationale Zahl]].

    **Beweis.** Angenommen, $\sqrt{2}$ ist rational. Dann gibt es $p, q \in \mathbb{N}$
    mit $\sqrt{2} = \frac{p}{q}$, und der Bruch ist vollständig [[gekürzt|Kürzen]].

    :::rechnung
    \sqrt{2} = \frac{p}{q} \Rightarrow 2 = \frac{p^2}{q^2} \Rightarrow p^2 = 2q^2 || quadrieren, mal $q^2$
    p^2 \text{ gerade} \Rightarrow p \text{ gerade, } p = 2m || Kontraposition von oben
    (2m)^2 = 4m^2 || einsetzen
    4m^2 = 2q^2 \Rightarrow q^2 = 2m^2 || durch $2$ teilen; also $q$ gerade
    :::

    Dann sind $p$ und $q$ beide gerade, der Bruch ließe sich mit $2$ kürzen.
    Widerspruch zu „vollständig gekürzt“. Also ist $\sqrt{2}$ irrational. $\square$

    :::alt Mit einer Treppe erklärt
    Wäre $\sqrt{2} = \frac{p}{q}$, könntest du durch $2$ kürzen und bekämst
    $\frac{p/2}{q/2}$, wieder mit geradem Zähler und Nenner, und so weiter. Eine
    Treppe natürlicher Zahlen kann aber nicht unendlich weit abwärts führen.
    :::
    """)

k.ordnen("Bringe den Beweis „$\\sqrt{2}$ ist irrational“ in die richtige Reihenfolge.",
         ["Angenommen, $\\sqrt{2} = \\frac{p}{q}$ mit $p, q \\in \\mathbb{N}$, vollständig gekürzt.",
          "Quadrieren ergibt $p^2 = 2q^2$, also ist $p^2$ gerade.",
          "Dann ist $p$ gerade, also $p = 2m$ mit $m \\in \\mathbb{N}$.",
          "Einsetzen: $4m^2 = 2q^2$, also $q^2 = 2m^2$ und damit $q$ gerade.",
          "$p$ und $q$ sind beide gerade. Das widerspricht „vollständig gekürzt“. $\\square$"],
         "Annahme, Quadrieren, $p$ gerade, $q$ gerade, Widerspruch.",
         ablenker=["Es gilt $\\sqrt{2} \\approx 1{,}41421$, und das ist kein Bruch.",
                   "Angenommen, $\\sqrt{2}$ ist irrational."],
         tipps=["Ein Widerspruchsbeweis beginnt mit dem Gegenteil der Behauptung.",
                "Aus „$p^2$ gerade“ folgt „$p$ gerade“: das ist die Kontraposition von vorhin.",
                "Endlich viele Nachkommastellen beweisen nichts."])

# ── 6: Methoden im Überblick ───────────────────────────────────────────────
k.erklaerung("Welche Methode wann?", r"""
    ## Drei Wege zu A ⇒ B

    | Methode | Was du zeigst | gut, wenn … |
    |---|---|---|
    | direkt | $A \Rightarrow Z_1 \Rightarrow \ldots \Rightarrow B$ | $A$ eine gute Formel liefert |
    | Kontraposition | $\neg B \Rightarrow \neg A$ | $\neg B$ eine gute Formel liefert |
    | Widerspruch | $A \land \neg B \Rightarrow \bot$ | du beide Annahmen brauchst |

    Eine Methode reicht. Kommst du nicht weiter, probiere eine andere.
    Die Vorlesung beweist $2 \mid n \Rightarrow 2 \mid n^3$ mit allen dreien.
    Die Kontraposition („$2 \nmid n^3 \Rightarrow 2 \nmid n$“) nutzt dieselbe Zerlegung:

    :::rechnung
    \frac{n^3}{2} = n^2 \cdot \frac{n}{2} || ist links keine natürliche Zahl, dann auch $\frac{n}{2}$ nicht
    :::

    :::alt Mit Navigation erklärt
    Drei Routen führen ans selbe Ziel: die direkte Straße, der Rückweg vom Ziel
    aus (Kontraposition) und der Umweg „Was, wenn ich nicht ankomme?“
    (Widerspruch). Du nimmst die Route, die gerade frei ist.
    :::
    """)

k.zuordnen("Ordne jeder Beweismethode zu, was du für $A \\Rightarrow B$ zeigst.",
           [("direkter Beweis", "A ⇒ Z₁ ⇒ … ⇒ B"), ("Beweis durch Kontraposition", "¬B ⇒ ¬A"),
            ("Widerspruchsbeweis", "A ∧ ¬B führt auf einen Widerspruch"),
            ("Gegenbeispiel (für eine Allaussage)", "ein Element, für das die Aussage nicht gilt")],
           "Direkt: Kette von $A$ nach $B$. Kontraposition: $\\neg B \\Rightarrow \\neg A$. Widerspruch: $A \\land \\neg B \\Rightarrow \\bot$.",
           ablenker=["B ⇒ A"],
           tipps=["$B \\Rightarrow A$ ist die Umkehrung und beweist $A \\Rightarrow B$ nicht."])


# ── Praxis ─────────────────────────────────────────────────────────────────
_VORLAGEN = [
    ("$n^2$ ist gerade", "$n$ ist gerade", "$n^2$ ist ungerade", "$n$ ist ungerade"),
    ("$3 \\mid n^2$", "$3 \\mid n$", "$3 \\nmid n^2$", "$3 \\nmid n$"),
    ("$x > 3$", "$x^2 > 9$", "$x \\le 3$", "$x^2 \\le 9$"),
    ("$4 \\mid n$", "$n$ ist gerade", "$4 \\nmid n$", "$n$ ist ungerade"),
    ("$a \\cdot b$ ist ungerade", "$a$ und $b$ sind ungerade", "$a \\cdot b$ ist gerade", "$a$ oder $b$ ist gerade"),
    ("$x + y > 2$", "$x > 1$ oder $y > 1$", "$x + y \\le 2$", "$x \\le 1$ und $y \\le 1$"),
    ("$x^2 = x$", "$x = 0$ oder $x = 1$", "$x^2 \\neq x$", "$x \\neq 0$ und $x \\neq 1$"),
    ("$n$ ist eine Primzahl größer als $2$", "$n$ ist ungerade", "$n$ ist keine Primzahl oder $n \\le 2$", "$n$ ist gerade"),
    ("$\\sqrt{n} \\in \\mathbb{N}$", "$n$ ist eine Quadratzahl", "$\\sqrt{n} \\notin \\mathbb{N}$", "$n$ ist keine Quadratzahl"),
]


def kontraposition_bilden(rng):
    a, b, na, nb = rng.choice(_VORLAGEN)
    if rng.random() < 0.5:
        opt = [f"Wenn {nb}, dann {na}.", f"Wenn {b}, dann {a}.", f"Wenn {na}, dann {nb}.", f"Wenn {a}, dann {nb}."]
        return {
            "frage": f"Wie lautet die Kontrapositionsaussage zu „Wenn {a}, dann {b}“?",
            "optionen": opt,
            "fehler": {opt[1]: "Das ist die Umkehrung $B \\Rightarrow A$: vertauscht, aber nicht verneint.",
                       opt[2]: "Das ist $\\neg A \\Rightarrow \\neg B$: verneint, aber nicht vertauscht.",
                       opt[3]: "Hier ist nur $B$ verneint. Die Kontraposition ist $\\neg B \\Rightarrow \\neg A$."},
            "tipps": ["Benenne $A$ (nach „Wenn“) und $B$ (nach „dann“).", "Vertausche und verneine beide.",
                      f"Wenn {nb}, dann …"],
            "erklaerung": "Kontraposition: $\\neg B \\Rightarrow \\neg A$. Sie ist gleichwertig zu $A \\Rightarrow B$.",
        }
    opt = [f"Angenommen, {a} und {nb}.", f"Angenommen, {na} und {b}.", f"Angenommen, {a} und {b}.",
           f"Angenommen, {na} und {nb}."]
    return {
        "frage": f"Du willst „Wenn {a}, dann {b}“ durch Widerspruch beweisen. Wie lautet die Widerspruchsannahme?",
        "optionen": opt,
        "fehler": {opt[1]: "Die Voraussetzung $A$ wird nicht verneint, sie bleibt erhalten. Verneint wird nur $B$.",
                   opt[2]: "Das ist genau das, was du zeigen willst. Angenommen wird das Gegenteil der Behauptung.",
                   opt[3]: "Die Voraussetzung $A$ muss in der Annahme gelten, sonst kannst du sie nicht benutzen."},
        "tipps": ["Die Widerspruchsannahme ist $A \\land \\neg B$.", "Die Voraussetzung bleibt.", f"… und {nb}."],
        "erklaerung": "Widerspruchsannahme: Die Voraussetzung gilt, die Behauptung nicht ($A \\land \\neg B$).",
    }


k.praxis()

k.generator(kontraposition_bilden, typ="mc", titel="Kontraposition und Widerspruchsannahme")

k.papier(r"""
    ## Übungsblatt-Stil: Kontraposition und Widerspruch

    a) Zeigen Sie durch Kontraposition: Für alle $n \in \mathbb{Z}$ gilt $3 \mid n^2 \Rightarrow 3 \mid n$.

    b) Zeigen Sie durch Widerspruch: $\sqrt{3}$ ist irrational. Sie dürfen a) benutzen.
    """,
    r"""
    **a)** Kontrapositionsaussage: $3 \nmid n \Rightarrow 3 \nmid n^2$.
    Sei $n \in \mathbb{Z}$ mit $3 \nmid n$. Dann lässt $n$ beim Teilen durch $3$
    den Rest $1$ oder $2$. Fallunterscheidung:

    :::rechnung Fall 1: $n = 3k + 1$ mit $k \in \mathbb{Z}$
    (3k + 1)^2 = 9k^2 + 6k + 1 || binomische Formel
    = 3(3k^2 + 2k) + 1 || Rest $1$, also $3 \nmid n^2$
    :::

    :::rechnung Fall 2: $n = 3k + 2$ mit $k \in \mathbb{Z}$
    (3k + 2)^2 = 9k^2 + 12k + 4 || binomische Formel
    = 3(3k^2 + 4k + 1) + 1 || Rest $1$, also $3 \nmid n^2$
    :::

    In beiden Fällen gilt $3 \nmid n^2$. Damit ist die Kontraposition und so die
    Behauptung bewiesen. $\square$

    **b)** Angenommen, $\sqrt{3} = \frac{p}{q}$ mit $p, q \in \mathbb{N}$ vollständig
    gekürzt. Quadrieren: $p^2 = 3q^2$, also $3 \mid p^2$, nach a) $3 \mid p$.
    Mit $p = 3m$: $9m^2 = 3q^2$, also $q^2 = 3m^2$, also $3 \mid q^2$ und nach a)
    $3 \mid q$. Dann ist der Bruch mit $3$ kürzbar. Widerspruch. $\square$
    """,
    ["a) Ich habe die Kontrapositionsaussage $3 \\nmid n \\Rightarrow 3 \\nmid n^2$ ausdrücklich hingeschrieben",
     "a) Ich habe beide Fälle $n = 3k + 1$ und $n = 3k + 2$ behandelt",
     "a) Ich habe jeweils $n^2 = 3 \\cdot (\\ldots) + 1$ gezeigt",
     "b) Ich habe die Widerspruchsannahme mit „vollständig gekürzt“ formuliert",
     "b) Ich habe a) zweimal benutzt und den Widerspruch benannt"],
    "Wie bei $\\sqrt{2}$: Erst die Teilbarkeitsaussage über Quadrate, dann der Widerspruch zum gekürzten Bruch.",
    uebungsblatt=True,
    tipps=["Für a): $3 \\nmid n$ heißt Rest $1$ oder Rest $2$ beim Teilen durch $3$."])

k.papier(r"""
    ## Widerspruch: Keine größte Zahl

    Zeigen Sie durch Widerspruch: Es gibt keine größte natürliche Zahl.
    """,
    r"""
    **Widerspruchsannahme:** Es gibt eine größte natürliche Zahl $N$, also
    $n \le N$ für alle $n \in \mathbb{N}$.

    Dann ist auch $N + 1 \in \mathbb{N}$, denn natürliche Zahlen plus $1$ bleiben
    natürlich. Nach Annahme gilt also $N + 1 \le N$. Subtrahieren von $N$ ergibt
    $1 \le 0$. Das ist falsch, ein Widerspruch.

    :::rechnung
    #1 \le 0 || folgt aus $N + 1 \le N$, ist aber falsch
    :::

    Also war die Annahme falsch: Es gibt keine größte natürliche Zahl. $\square$
    """,
    ["Ich habe die Widerspruchsannahme ausdrücklich formuliert (es gibt ein größtes $N$)",
     "Ich habe $N + 1$ betrachtet und begründet, warum $N + 1 \\in \\mathbb{N}$ ist",
     "Ich habe den Widerspruch $1 \\le 0$ (oder $N + 1 > N$) klar benannt"],
    "Der Trick: Zu jeder Zahl kann man $1$ addieren. Damit kann es keine größte geben.",
    tipps=["Was passiert, wenn du zur größten Zahl $1$ addierst?"])

k.zusammenfassung(r"""
    ## Kontraposition und Widerspruch

    | Methode | Logik | Start des Beweises |
    |---|---|---|
    | Kontraposition | $(A \Rightarrow B) \Leftrightarrow (\neg B \Rightarrow \neg A)$ | „Sei $\neg B$ …, zu zeigen $\neg A$.“ |
    | Widerspruch | $(A \Rightarrow B) \Leftrightarrow (A \land \neg B \Rightarrow \bot)$ | „Angenommen, $A$ und $\neg B$ …“ |

    !! Kontraposition: vertauschen **und** verneinen. Die Umkehrung $B \Rightarrow A$ ist etwas anderes.

    - Verneinen: $>$ wird $\le$, „und“ wird „oder“ und umgekehrt (De Morgan), $\mid$ wird $\nmid$.
    - $n^2$ gerade $\Rightarrow n$ gerade (per Kontraposition), $\sqrt{2}$ irrational (per Widerspruch).
    - Am Ende eines Widerspruchsbeweises den Widerspruch benennen und sagen: Die Annahme war falsch.
""")
