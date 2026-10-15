# -*- coding: utf-8 -*-
"""Fundament 16: Mathematik lesen – Symbole, Quantoren, Pfeile, griechische Buchstaben, Indizes,
Definition/Satz/Beweis und die ℕ-Konventionen der TU-Unterlagen."""
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

tex = mathlib.tex
tk = mathlib.tex_klammer
vz = mathlib.vorzeichen_tex

k = neues_kapitel(
    slug="mathe_lesen",
    titel="Mathematik lesen",
    beschreibung="Die Zeichen der Uni-Mathematik: := ∈ ⊆ ∀ ∃ ⇒ ⇔, griechische Buchstaben, Indizes, Definition, Satz, Beweis",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="📖")

k.lernziele([
    "Ich kann $:=$, $\\in$, $\\notin$ und $\\subseteq$ lesen und Mengen wie $\\{x \\in \\mathbb{Z} : x < 3\\}$ aufzählen",
    "Ich kann Aussagen mit $\\forall$, $\\exists$, $\\Rightarrow$ und $\\Leftrightarrow$ laut vorlesen und prüfen",
    "Ich kenne die wichtigsten griechischen Buchstaben und unterscheide Index $x_2$ und Exponent $x^2$",
    "Ich erkenne in einem Satz Voraussetzung und Behauptung und weiß, was $\\mathbb{N}$ in welcher TU-Veranstaltung bedeutet",
])

k.warum(r"""
Ein Uni-Skript ist in einer eigenen Sprache geschrieben, so wie Code in einer
Programmiersprache. $\forall x \in M$ ist eine Schleife über alle Elemente von $M$,
$\exists x \in M$ eine Suche, die beim ersten Treffer aufhört. $:=$ ist eine Zuweisung,
$x_i$ ist `x[i]`. Wer diese Zeichen fließend liest, versteht die Vorlesung statt sie
nur abzuschreiben. Diese Sprache brauchst du auch in Logik, Algorithmen und
Datenbanken.
""")

# ── 1: Zeichen ─────────────────────────────────────────────────────────────
k.erklaerung("Die Zeichen der Mathematik", r"""
    ## Definieren und Mengen beschreiben

    :::analogie 🐍 Zuweisung in Python
    `A = {1, 2, 3}` legt in Python fest, was `A` ist. In der Mathematik schreibt man
    dafür $A := \{1, 2, 3\}$.
    :::

    | Zeichen | gelesen |
    |---|---|
    | $A := \ldots$ | $A$ ist definiert als … (links steht das Neue) |
    | $x \in A$ | $x$ ist Element von $A$ |
    | $x \notin A$ | $x$ ist nicht Element von $A$ |
    | $A \subseteq B$ | $A$ ist [[Teilmenge]] von $B$ |

    Mengen beschreibt man oft durch eine Eigenschaft. Der senkrechte Strich $\mid$ (so meist im
    TU-Vorkurs, gelesen „sodass“) oder ein Doppelpunkt heißt „für die gilt“:

    $$A := \{x \in \mathbb{Z} : -1 \le x \le 2\} = \{-1, 0, 1, 2\}$$

    :::visual zahlenstrahl
    {"von": -3, "bis": 4, "punkte": [{"x": -1}, {"x": 0}, {"x": 1}, {"x": 2}],
     "unterschrift": "Die ganzen Zahlen von $-1$ bis $2$: genau die Elemente von $A$."}
    :::

    :::alt Mit einem Steckbrief erklärt
    $\{x \in \mathbb{Z} : -1 \le x \le 2\}$ ist ein Steckbrief: „Gesucht sind alle
    ganzen Zahlen, die mindestens $-1$ und höchstens $2$ sind.“ Geh die ganzen Zahlen
    durch und sammle jede ein, auf die der Steckbrief passt.
    :::
    ---
    ## Für alle und es gibt

    Zwei Zeichen heißen [[Quantoren|Quantor]]:

    - $\forall$ heißt „für alle“ (ein umgedrehtes A),
    - $\exists$ heißt „es gibt ein“, also mindestens eins (ein gespiegeltes E).

    $\forall x \in \mathbb{R} : x^2 \ge 0$ liest man: „Für alle reellen $x$ gilt
    $x^2 \ge 0$.“ Eine Aussage mit $\forall$ ist falsch, sobald es **ein**
    [[Gegenbeispiel]] gibt.

    :::rechnung Ist $\forall x \in \mathbb{R} : x^2 > 0$ wahr?
    0^2 = 0 || für $x = 0$ gilt **nicht** $x^2 > 0$
    :::

    Also ist die Aussage falsch. Dagegen ist $\exists x \in \mathbb{Z} : x^2 = 4$
    wahr: $x = 2$ passt.

    :::alt Mit einer Schulklasse erklärt
    „Alle in der Klasse haben ein Handy“ ist falsch, sobald eine Person keins hat.
    „Es gibt jemanden mit Handy“ ist wahr, sobald du **eine** Person mit Handy
    findest. Für „alle“ musst du jeden prüfen, für „es gibt“ reicht ein Treffer.
    :::
    ---
    ## Folgt und genau dann

    | Zeichen | gelesen |
    |---|---|
    | $A \Rightarrow B$ | wenn $A$, dann $B$; aus $A$ folgt $B$ |
    | $A \Leftrightarrow B$ | $A$ genau dann, wenn $B$ (beide Richtungen) |

    $x = 2 \Rightarrow x^2 = 4$ ist wahr. Die Umkehrung $x^2 = 4 \Rightarrow x = 2$ ist falsch:

    :::rechnung Gegenbeispiel für die Umkehrung
    (-2)^2 = 4 || $x = -2$ erfüllt $x^2 = 4$, ist aber nicht $2$
    :::

    :::achtung Nur eine Richtung
    $A \Rightarrow B$ sagt nichts über $B \Rightarrow A$. Ein $\Leftrightarrow$ darfst du
    nur schreiben, wenn **beide** Richtungen stimmen.
    :::

    :::alt Mit Regen erklärt
    „Es regnet $\Rightarrow$ die Straße ist nass.“ Stimmt. Aber „die Straße ist nass
    $\Rightarrow$ es regnet“ stimmt nicht: Vielleicht lief ein Rasensprenger. Der Pfeil
    zeigt nur in eine Richtung.
    :::
    """)

k.menge("Zähle die Menge auf: $M := \\{x \\in \\mathbb{Z} : -2 < x \\le 1\\}$. "
        "Trenne die Elemente mit **;**, zum Beispiel $\\{1; 2\\}$.",
        "{-1; 0; 1}",
        "Ganze Zahlen größer als $-2$ (also ohne $-2$) und höchstens $1$ (also mit $1$): $-1, 0, 1$.",
        tipps=["Der Doppelpunkt heißt „für die gilt“.", "Prüfe die Ränder: Ist $-2$ dabei? Ist $1$ dabei?",
               "$-2$ nicht, $1$ schon."],
        rechenweg=r"""
        - $-2 < x$: Die $-2$ gehört **nicht** dazu.
        - $x \le 1$: Die $1$ gehört dazu.

        Also $M = \{-1, 0, 1\}$.
        """,
        typische_fehler=[("{-2; -1; 0; 1}", "Bei $-2 < x$ ist $-2$ selbst nicht dabei."),
                         ("{-1; 0}", "Bei $x \\le 1$ gehört die $1$ dazu.")])

k.mc("Wie liest man $\\exists x \\in \\mathbb{Z} : x^2 = 4$?",
     ["Es gibt eine ganze Zahl $x$, für die $x^2 = 4$ gilt.",
      "Für alle ganzen Zahlen $x$ gilt $x^2 = 4$.",
      "Es gibt genau eine ganze Zahl $x$ mit $x^2 = 4$.",
      "$x$ ist definiert als $4$."],
     "$\\exists$ heißt „es gibt (mindestens) ein“. Die Aussage ist wahr, denn $x = 2$ passt (und $x = -2$ auch).",
     tipps=["$\\exists$ ist ein gespiegeltes E wie in „existiert“.", "Mindestens eins oder alle?"],
     fehler={"Für alle ganzen Zahlen $x$ gilt $x^2 = 4$.": "Das wäre $\\forall$ (umgedrehtes A). $\\exists$ heißt „es gibt ein“.",
             "Es gibt genau eine ganze Zahl $x$ mit $x^2 = 4$.": "„Genau ein“ schreibt man $\\exists!$. Ohne Ausrufezeichen "
                                                                   "heißt es „mindestens ein“. Hier sind es sogar zwei: $2$ und $-2$."})

k.wf("Die Aussage $\\forall x \\in \\mathbb{R} : x^2 > 0$ ist wahr.", False,
     "Falsch. Gegenbeispiel $x = 0$: $0^2 = 0$, und $0 > 0$ gilt nicht. Ein Gegenbeispiel reicht.",
     tipps=["Suche eine einzige reelle Zahl, für die es nicht klappt."])

k.mc("Welche Aussage ist für reelle Zahlen $x$ wahr?",
     ["$x = 3 \\Rightarrow x^2 = 9$", "$x^2 = 9 \\Rightarrow x = 3$", "$x^2 = 9 \\Leftrightarrow x = 3$"],
     "Aus $x = 3$ folgt $x^2 = 9$. Umgekehrt nicht: $x = -3$ hat auch $x^2 = 9$. Darum ist auch $\\Leftrightarrow$ falsch.",
     tipps=["Prüfe jede Richtung mit $x = -3$.", "$(-3)^2 = 9$, aber $-3 \\neq 3$."],
     fehler={"$x^2 = 9 \\Rightarrow x = 3$": "Gegenbeispiel $x = -3$: $(-3)^2 = 9$, aber $x \\neq 3$.",
             "$x^2 = 9 \\Leftrightarrow x = 3$": "$\\Leftrightarrow$ verlangt beide Richtungen. Die Richtung "
                                                "$x^2 = 9 \\Rightarrow x = 3$ scheitert an $x = -3$."})

k.zuordnen("Ordne jedem Zeichen seine Lesart zu.",
           [("$:=$", "ist definiert als"), ("$\\in$", "ist Element von"), ("$\\subseteq$", "ist Teilmenge von"),
            ("$\\forall$", "für alle"), ("$\\exists$", "es gibt ein"), ("$\\Rightarrow$", "daraus folgt"),
            ("$\\Leftrightarrow$", "genau dann, wenn")],
           "Diese sieben Zeichen stehen in fast jeder Zeile eines Uni-Skripts.",
           ablenker=["ist ungefähr gleich"],
           tipps=["$\\forall$ ist ein umgedrehtes A (alle), $\\exists$ ein gespiegeltes E (existiert)."])

# ── 2: Griechische Buchstaben und Indizes ──────────────────────────────────
k.erklaerung("Griechische Buchstaben und Indizes", r"""
    ## Das griechische Alphabet

    Das lateinische Alphabet reicht für die Mathematik nicht. Diese Buchstaben triffst du ständig:

    | Zeichen | Name | typisch für |
    |---|---|---|
    | $\alpha, \beta, \gamma$ | alpha, beta, gamma | Winkel |
    | $\delta, \varepsilon$ | delta, epsilon | kleine positive Zahlen |
    | $\Delta$ | groß Delta | Differenz, $\Delta x$ |
    | $\lambda$ | lambda | Faktor, Eigenwert |
    | $\pi$ | pi | Kreiszahl $3{,}14159\ldots$ |
    | $\Sigma$, $\Pi$ | groß Sigma, groß Pi | Summe, Produkt |
    | $\varphi$, $\omega$ | phi, omega | Winkel, Frequenz |

    :::rechnung Umfang eines Kreises mit Radius $r = 3$
    2 \cdot \pi \cdot 3 = 6 \pi || $U = 2 \pi r$; $\pi$ ist eine feste Zahl
    :::

    :::alt Wie Variablennamen erklärt
    Im Code nennst du Variablen `zaehler` oder `i`. Mathematiker greifen zu
    griechischen Buchstaben, wenn die lateinischen schon vergeben sind. Ein $\lambda$
    ist nichts Geheimnisvolles, nur ein weiterer Name für eine Zahl.
    :::
    ---
    ## Indizes: tief gestellt

    Ein [[Index]] ist eine tief gestellte Nummer. Er unterscheidet Größen, die
    zusammengehören: $x_1, x_2, x_3$ sind drei verschiedene Zahlen. Bei $a_n = 2n + 1$
    gibt der Index $n$ die Position an.

    :::rechnung Die ersten Glieder von $a_n = 2n + 1$
    2 \cdot 1 + 1 = 3 || $a_1$: für $n$ die $1$ einsetzen
    2 \cdot 2 + 1 = 5 || $a_2$
    2 \cdot 3 + 1 = 7 || $a_3$
    :::

    :::achtung Index ist kein Exponent
    $x_2$ ist „$x$ zwei“, die zweite Zahl. $x^2$ ist „$x$ hoch zwei“, also $x \cdot x$.
    :::

    :::alt Mit einer Liste erklärt
    In Python ist `a[3]` der Eintrag mit dem Index $3$ der Liste `a`. Die Mathematik
    schreibt dafür $a_3$. Der Index ist die Hausnummer, nicht der Inhalt des Hauses.
    Vorsicht: Python zählt ab $0$, also ist `a[3]` dort der vierte Eintrag. In der
    Mathematik beginnt man oft mit $a_1$.
    :::
    """)

k.text("Wie heißt der griechische Buchstabe $\\varepsilon$?", ["Epsilon"],
       "$\\varepsilon$ ist ein Epsilon. In der Analysis steht es für eine kleine positive Zahl.",
       tipps=["Es ist das griechische E.", "Beginnt mit „Eps…“."])

k.zuordnen("Ordne jedem Buchstaben seinen Namen zu.",
           [("$\\alpha$", "alpha"), ("$\\lambda$", "lambda"), ("$\\Sigma$", "groß Sigma"),
            ("$\\varphi$", "phi"), ("$\\delta$", "delta")],
           "$\\Sigma$ ist das große Sigma, das Summenzeichen. Das kleine Sigma sieht so aus: $\\sigma$.",
           ablenker=["omega", "groß Pi"],
           tipps=["$\\Sigma$ ist ein großes S wie in Summe."])

k.zahl("Es sei $x = 3$ und außerdem $x_1 = 4$, $x_2 = 7$. Berechne $x_2 - x^2$.", 7 - 3 ** 2,
       "$x_2 = 7$ ist die zweite Zahl, $x^2 = 3^2 = 9$. Also $7 - 9 = -2$.",
       tipps=["$x_2$ (unten) und $x^2$ (oben) sind verschiedene Dinge.", "$x_2 = 7$, $x^2 = 3 \\cdot 3$.", "$7 - 9$"],
       rechenweg=r"""
       :::rechnung
       7 - 3^2 || $x_2 = 7$ und $x^2 = 3^2$
       = 7 - 9 || quadrieren
       = -2 || abziehen
       :::
       """,
       typische_fehler=[(0, "Du hast $x_2$ auch als $x^2 = 9$ gelesen. Der tiefe Index ist nur eine Nummer: $x_2 = 7$."),
                        (3, "Du hast $x^2$ mit $x_1 = 4$ verwechselt und $7 - 4$ gerechnet. Oben heißt hoch: $x^2 = 3^2 = 9$."),
                        (-42, "Du hast $x^2$ mit dem Wert von $x_2$ gerechnet. $x^2$ bezieht sich auf $x = 3$.")])

# ── 3: Definition, Satz, Beweis ────────────────────────────────────────────
k.erklaerung("Definition, Satz, Beweis", r"""
    ## So ist ein Skript gebaut

    - Eine [[Definition]] gibt etwas einen Namen. Dabei schreibt man oft $:\Leftrightarrow$.
    - Ein [[Satz]] ist eine bewiesene Aussage: **Voraussetzung** $\Rightarrow$ **Behauptung**.
    - Ein [[Beweis]] zeigt Schritt für Schritt, warum der Satz stimmt. Er beginnt mit „z. z.:“ (zu zeigen) und
      der Behauptung, startet dann bei der Voraussetzung und endet mit $\square$, „q.e.d.“ oder „w.z.z.w.“.

    **Definition.** $n \in \mathbb{Z}$ heißt gerade $:\Leftrightarrow \exists k \in \mathbb{Z} : n = 2k$.

    **Satz.** Sind $m, n \in \mathbb{Z}$ gerade, so ist $m + n$ gerade.

    :::rechnung Beweis
    m = 2k \text{ und } n = 2l || Voraussetzung: es gibt $k, l \in \mathbb{Z}$; z. z.: $m + n$ ist gerade
    m + n = 2k + 2l,\quad k, l \in \mathbb{Z} || einsetzen
    2k + 2l = 2(k + l) || $2$ ausklammern
    :::

    Mit $k + l \in \mathbb{Z}$ hat $m + n$ die Form aus der Definition. $\square$

    :::alt Mit Spielregeln erklärt
    Die Definition ist eine Spielregel: „Ein Tor zählt, wenn der Ball ganz hinter der
    Linie ist.“ Der Satz ist eine Behauptung über das Spiel. Der Beweis ist die
    Videoanalyse: Bild für Bild, nur mit den Regeln.
    :::
    ---
    ## Was ist ℕ?

    Die TU-Unterlagen setzen $\mathbb{N}$ verschieden fest. Das ist keine Schlamperei,
    beide Konventionen sind verbreitet.

    :::visual zahlenstrahl
    {"von": -1, "bis": 6, "punkte": [{"x": 0, "label": "0\\,?", "farbe": "orange"}, {"x": 1}, {"x": 2}, {"x": 3}, {"x": 4}, {"x": 5}],
     "unterschrift": "Ob die $0$ zu $\\mathbb{N}$ gehört, legt jede Vorlesung selbst fest."}
    :::

    :::achtung ℕ mit oder ohne Null
    - **TU-Vorkurs** (und dieses Fundament): $\mathbb{N} = \{1, 2, 3, \ldots\}$, mit Null: $\mathbb{N}_0 = \{0, 1, 2, \ldots\}$.
    - **Skript Mathe I/II**: $\mathbb{N} = \{0, 1, 2, \ldots\}$, ohne Null: $\mathbb{N}^* = \{1, 2, 3, \ldots\}$.

    Schau in jeder Vorlesung nach, was festgelegt ist. Wo es zählt, schreib eindeutig $\mathbb{N}_0$, $\mathbb{N}^*$ oder „$n \ge 1$“.
    :::

    :::alt Wie Etagen erklärt
    In Deutschland heißt das Erdgeschoss „0“ und die nächste Etage „1“. In den USA
    ist das Erdgeschoss schon der „1st floor“. Beide zählen richtig, nur ab
    verschiedenen Startpunkten. Vor dem Treffen fragst du, welche Zählung gilt.
    :::
    """)

k.mc("Im Satz „Sind $m, n \\in \\mathbb{Z}$ gerade, so ist $m + n$ gerade.“ ist die **Voraussetzung**:",
     ["$m$ und $n$ sind gerade ganze Zahlen", "$m + n$ ist gerade", "$m + n$ ist eine ganze Zahl"],
     "Die Voraussetzung steht im „Wenn“-Teil (hier: „Sind …“). Die Behauptung ist das, was folgt: $m + n$ ist gerade.",
     tipps=["Satz = Voraussetzung $\\Rightarrow$ Behauptung.", "Was wird angenommen, was wird gezeigt?"],
     fehler={"$m + n$ ist gerade": "Das ist die **Behauptung**, also das, was bewiesen wird. Die Voraussetzung ist der „Sind …“-Teil."})

k.mc("Im **TU-Vorkurs** gilt $\\mathbb{N} = \\{1, 2, 3, \\ldots\\}$. Wie heißt dort die Menge $\\{0, 1, 2, 3, \\ldots\\}$?",
     ["$\\mathbb{N}_0$", "$\\mathbb{N}$", "$\\mathbb{N}^*$", "$\\mathbb{Z}$"],
     "Im Vorkurs schreibt man die natürlichen Zahlen mit Null als $\\mathbb{N}_0$.",
     tipps=["Die kleine $0$ unten heißt: mit Null.", "Im Vorkurs beginnt $\\mathbb{N}$ bei $1$."],
     fehler={"$\\mathbb{N}$": "Das wäre im **Skript Mathe I/II** richtig. Im Vorkurs beginnt $\\mathbb{N}$ bei $1$, "
                            "deshalb braucht die Menge mit Null den Namen $\\mathbb{N}_0$.",
             "$\\mathbb{N}^*$": "$\\mathbb{N}^*$ ist im Skript die Menge **ohne** Null, $\\{1, 2, 3, \\ldots\\}$.",
             "$\\mathbb{Z}$": "$\\mathbb{Z}$ enthält auch die negativen Zahlen."})

k.wf("Im Skript Mathe I/II gilt $0 \\in \\mathbb{N}$.", True,
     "Ja. Das Skript setzt $\\mathbb{N} = \\{0, 1, 2, \\ldots\\}$ und schreibt $\\mathbb{N}^* = \\{1, 2, \\ldots\\}$ für die Zahlen ohne Null.",
     tipps=["Erinnere dich an die Achtung-Box: Vorkurs und Skript unterscheiden sich."])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


def folge_glied(rng):
    art = rng.choice(["linear", "linear", "quadrat", "potenz"])
    i = rng.randint(2, 6)
    buchstabe = rng.choice(["a", "b", "x", "c"])
    if art == "linear":
        p = rng.choice([z for z in range(-4, 6) if z not in (0, 1)])
        q = rng.choice([z for z in range(-5, 6) if z != 0])
        term = ("-n" if p == -1 else f"{p}n") + f" {vz(F(q))}"
        w = p * i + q
        zeilen = [(f"{p} \\cdot {i} {vz(F(q))} = {w}", f"für $n$ die ${i}$ einsetzen")]
        fehler = [(p * (i + 1) + q, f"Das ist ${buchstabe}_{{{i + 1}}}$. Der Index sagt: $n = {i}$."),
                  (i, "Der Index ist nur die Position. Setze ihn für $n$ in die Formel ein.")]
    elif art == "quadrat":
        q = rng.choice([z for z in range(-5, 6) if z != 0])
        term = f"n^2 {vz(F(q))}"
        w = i * i + q
        zeilen = [(f"{i}^2 {vz(F(q))} = {w}", f"für $n$ die ${i}$ einsetzen")]
        fehler = [(2 * i + q, f"$n^2$ heißt $n \\cdot n$, nicht $2 \\cdot n$: ${i}^2 = {i * i}$."),
                  ((i + 1) ** 2 + q, f"Das ist ${buchstabe}_{{{i + 1}}}$. Der Index sagt: $n = {i}$."),
                  (i, "Der Index ist nur die Position. Setze ihn für $n$ in die Formel ein.")]
    else:
        basis = rng.choice([2, 3])
        term = f"{basis}^n"
        w = basis ** i
        zeilen = [(f"{basis}^{{{i}}} = {w}", f"für $n$ die ${i}$ einsetzen")]
        fehler = [(basis * i, f"${basis}^{{{i}}}$ heißt ${i}$-mal die ${basis}$ malnehmen, nicht ${basis} \\cdot {i}$."),
                  (i, "Der Index ist nur die Position. Setze ihn für $n$ in die Formel ein.")]
    return {
        "frage": f"Für $n \\ge 1$ sei ${buchstabe}_n = {term}$. Berechne ${buchstabe}_{{{i}}}$.",
        "loesung": w,
        "tipps": [f"Der Index ${i}$ unten sagt dir, welches $n$ du einsetzt.",
                  f"Setze $n = {i}$ in ${term}$ ein.", f"Rechne ${zeilen[0][0].split(' = ')[0]}$ aus."],
        "rechenweg": _zeilen(*zeilen),
        "erklaerung": f"${buchstabe}_{{{i}}}$ ist das Glied an Position ${i}$: In die Formel kommt $n = {i}$.",
        "typische_fehler": ohne_gleiche(w, fehler),
    }


k.praxis()

k.generator(folge_glied, typ="zahl", titel="Indizes lesen", glatt=True)


def quantor_aussage(rng):
    m = sorted(rng.sample(range(-4, 9), rng.randint(3, 5)))
    mtex = "\\{" + ", ".join(str(z) for z in m) + "\\}"
    art = rng.choice(["alle_kleiner", "gibt_gleich", "alle_gerade", "gibt_quadrat", "alle_positiv"])
    if art == "alle_kleiner":
        c = rng.choice([max(m), max(m) + 1, max(m) + rng.randint(1, 3)])
        aussage = f"\\forall x \\in M : x < {c}"
        wahr = max(m) < c
        grund = (f"Alle Elemente sind kleiner als ${c}$; das größte ist ${max(m)}$." if wahr
                 else f"Gegenbeispiel: $x = {max(m)}$ ist nicht kleiner als ${c}$.")
    elif art == "gibt_gleich":
        c = rng.choice([rng.choice(m), rng.randint(-4, 8)])
        aussage = f"\\exists x \\in M : x + 2 = {c + 2}"
        wahr = c in m
        grund = (f"$x = {c}$ liegt in $M$ und erfüllt $x + 2 = {c + 2}$." if wahr
                 else f"Nur $x = {c}$ erfüllt $x + 2 = {c + 2}$, und ${c} \\notin M$.")
    elif art == "alle_gerade":
        aussage = "\\forall x \\in M : x \\text{ ist gerade}"
        ungerade = [z for z in m if z % 2]
        wahr = not ungerade
        grund = "Alle Elemente sind gerade." if wahr else f"Gegenbeispiel: ${ungerade[0]}$ ist ungerade."
    elif art == "gibt_quadrat":
        c = rng.choice([z * z for z in m] + [rng.choice([2, 3, 5, 7, 10])])
        aussage = f"\\exists x \\in M : x^2 = {c}"
        treffer = [z for z in m if z * z == c]
        wahr = bool(treffer)
        grund = (f"$x = {treffer[0]}$ liegt in $M$: ${tk(treffer[0])}^2 = {c}$." if wahr
                 else f"Kein Element von $M$ hat das Quadrat ${c}$.")
    else:
        aussage = "\\forall x \\in M : x > 0"
        nicht = [z for z in m if z <= 0]
        wahr = not nicht
        grund = "Alle Elemente sind größer als $0$." if wahr else f"Gegenbeispiel: $x = {nicht[0]}$ ist nicht größer als $0$."
    return {
        "typ": "wf",
        "frage": f"Es sei $M := {mtex}$. Ist die Aussage ${aussage}$ wahr?",
        "wahr": wahr,
        "tipps": ["$\\forall$: Prüfe **jedes** Element, ein Gegenbeispiel macht die Aussage falsch."
                  if "forall" in aussage else "$\\exists$: Ein einziges passendes Element reicht."],
        "erklaerung": grund,
    }


k.generator(quantor_aussage, typ="wf", titel="Quantoren prüfen")


def menge_lesen(rng):
    art = rng.choice(["n0_kleiner", "z_zwischen", "doppelt", "n_zwischen"])
    if art == "n0_kleiner":
        c = rng.randint(2, 6)
        beschr = f"\\{{n \\in \\mathbb{{N}}_0 : n < {c}\\}}"
        elemente = list(range(0, c))
        fehler = [(list(range(1, c)), "$\\mathbb{N}_0$ enthält die $0$."),
                  (list(range(0, c + 1)), f"Bei $n < {c}$ gehört ${c}$ nicht dazu.")]
        tipp = "$\\mathbb{N}_0$ beginnt bei $0$."
    elif art == "z_zwischen":
        a = rng.randint(-4, 1)
        b = a + rng.randint(2, 4)
        beschr = f"\\{{x \\in \\mathbb{{Z}} : {a} \\le x < {b}\\}}"
        elemente = list(range(a, b))
        fehler = [(list(range(a, b + 1)), f"Bei $x < {b}$ gehört ${b}$ nicht dazu."),
                  (list(range(a + 1, b)), f"Bei ${a} \\le x$ gehört ${a}$ dazu.")]
        tipp = "Prüfe beide Ränder: $\\le$ mit Rand, $<$ ohne."
    elif art == "doppelt":
        c = rng.randint(2, 5)
        beschr = f"\\{{2k : k \\in \\mathbb{{Z}},\\ 1 \\le k \\le {c}\\}}"
        elemente = [2 * j for j in range(1, c + 1)]
        fehler = [(list(range(1, c + 1)), "Das sind die $k$. In der Menge stehen aber die Werte $2k$."),
                  ([2 * j for j in range(0, c + 1)], "$k = 0$ ist nicht erlaubt, denn $1 \\le k$.")]
        tipp = "Vor dem Doppelpunkt steht, **was** in die Menge kommt: $2k$."
    else:
        a = rng.randint(2, 4)
        b = a + rng.randint(1, 3)
        beschr = f"\\{{n \\in \\mathbb{{N}} : {a} \\le n \\le {b}\\}}"
        elemente = list(range(a, b + 1))
        fehler = [(list(range(a + 1, b)), "Bei $\\le$ gehören beide Ränder dazu."),
                  (list(range(a, b)), f"Bei $n \\le {b}$ gehört ${b}$ dazu."),
                  (list(range(1, b + 1)), f"Die Bedingung $n \\ge {a}$ schließt die kleineren Zahlen aus.")]
        tipp = "Hier ist es egal, ob $0 \\in \\mathbb{N}$: Die Bedingung beginnt erst bei " + f"${a}$."
    loesung = "{" + "; ".join(str(z) for z in elemente) + "}"
    fehler_txt = [("{" + "; ".join(str(z) for z in f) + "}", t) for f, t in fehler if sorted(f) != elemente and f]
    return {
        "typ": "menge",
        "frage": f"Zähle die Menge ${beschr}$ auf. Trenne die Elemente mit **;**.",
        "loesung": loesung,
        "tipps": ["Der Doppelpunkt heißt „für die gilt“.", tipp,
                  "Es sind " + str(len(elemente)) + " Elemente."],
        "rechenweg": f"Gesucht sind alle Elemente, auf die die Bedingung passt: $\\{{{', '.join(str(z) for z in elemente)}\\}}$.",
        "erklaerung": f"${beschr} = \\{{{', '.join(str(z) for z in elemente)}\\}}$",
        "typische_fehler": fehler_txt,
    }


k.generator(menge_lesen, typ="menge", titel="Mengen aufzählen")

k.ordnen(r"""
    ## Übungsblatt-Stil: Einen Beweis lesen

    **Satz.** Ist $n \in \mathbb{Z}$ ungerade, so ist auch $n^2$ ungerade.

    Bringe die Beweisschritte in die richtige Reihenfolge. Zwei Zeilen gehören nicht in den Beweis.
    """,
    ["z. z.: Ist $n \\in \\mathbb{Z}$ ungerade, so ist $n^2$ ungerade.",
     "Sei $n \\in \\mathbb{Z}$ ungerade.",
     "Dann gibt es ein $k \\in \\mathbb{Z}$ mit $n = 2k + 1$.",
     "Es folgt $n^2 = (2k + 1)^2 = 4k^2 + 4k + 1$.",
     "Also ist $n^2 = 2(2k^2 + 2k) + 1$.",
     "Da $2k^2 + 2k \\in \\mathbb{Z}$ ist, ist $n^2$ ungerade. $\\square$"],
    "Der Beweis beginnt mit der Voraussetzung, schreibt sie mit der Definition um, rechnet und endet mit der Behauptung.",
    ablenker=["Sei $n^2$ ungerade.", "Dann gibt es ein $k \\in \\mathbb{Z}$ mit $n = 2k$."],
    uebungsblatt=True,
    tipps=["Zuerst steht, was zu zeigen ist (z. z.). Die Argumentation startet dann bei der Voraussetzung. "
           "Die Behauptung darfst du nicht annehmen, sie ist das Ziel.",
           "Ungerade heißt: $n = 2k + 1$. Danach wird $n^2$ ausgerechnet.",
           "Ganz am Ende steht die Behauptung und $\\square$."],
    rechenweg=r"""
    :::rechnung Die Rechnung im Beweis
    (2k + 1)^2 = 4k^2 + 4k + 1 || binomische Formel
    = 2(2k^2 + 2k) + 1 || $2$ ausklammern: Form $2 \cdot \text{ganz} + 1$
    :::
    """)

k.zusammenfassung(r"""
    ## Mathematik lesen

    | Zeichen | gelesen |
    |---|---|
    | $:=$ | ist definiert als |
    | $\in$, $\notin$ | ist (nicht) Element von |
    | $\subseteq$ | ist Teilmenge von |
    | $\{x \in M : \ldots\}$ | alle $x$ aus $M$, für die gilt … |
    | $\forall$ | für alle |
    | $\exists$, $\exists!$ | es gibt (mindestens) ein, es gibt genau ein |
    | $\Rightarrow$ | daraus folgt (eine Richtung) |
    | $\Leftrightarrow$ | genau dann, wenn (beide Richtungen) |
    | $\square$ | Ende des Beweises |

    - $\forall$-Aussage: Ein Gegenbeispiel macht sie falsch. $\exists$-Aussage: Ein Beispiel macht sie wahr.
    - Index $x_2$ = zweite Zahl; Exponent $x^2 = x \cdot x$.
    - Satz = Voraussetzung $\Rightarrow$ Behauptung. Beweis: „z. z.: …“, dann von der Voraussetzung aus argumentieren
      (nie die Behauptung annehmen), Ende mit $\square$, „q.e.d.“ oder „w.z.z.w.“.

    !! Vorkurs: $\mathbb{N} = \{1, 2, \ldots\}$, $\mathbb{N}_0 = \{0, 1, \ldots\}$. Skript Mathe I/II: $\mathbb{N} = \{0, 1, \ldots\}$, $\mathbb{N}^* = \{1, 2, \ldots\}$. Immer nachschauen!
""")
