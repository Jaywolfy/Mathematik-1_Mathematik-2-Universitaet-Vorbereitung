# -*- coding: utf-8 -*-
"""Vorkurs 10: Funktionen, Bild und Urbild – f: D → W, Definitionsbereich, Zielmenge, Gleichheit,
Bild f(A), Urbild f⁻¹(B) (MVK 2026, VL 4)."""
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel

tex = mathlib.tex
tk = mathlib.tex_klammer

k = neues_kapitel(
    slug="abbildungen",
    titel="Funktionen, Bild und Urbild",
    beschreibung="Die Uni-Schreibweise f: D → W, Definitionsbereich und Zielmenge, Bild f(A) und Urbild f⁻¹(B)",
    teil="vorkurs",
    quelle="MVK 2026, VL 4",
    icon="🎯")

k.lernziele([
    "Ich kann eine Funktion als $f\\colon D \\to W,\\ x \\mapsto f(x)$ aufschreiben und Definitionsbereich, Zielmenge und Vorschrift benennen",
    "Ich kann entscheiden, ob eine Zuordnung eine Funktion ist, und den maximalen Definitionsbereich bestimmen",
    "Ich weiß, wann zwei Funktionen gleich sind",
    "Ich kann das Bild $f(A)$ und das Urbild $f^{-1}(B)$ einer Menge bestimmen",
])

k.warum(r"""
Jede Funktion im Code hat eine Signatur: `def laenge(s: str) -> int`. Der Typ des
Parameters ist der Definitionsbereich, der Rückgabetyp die Zielmenge. Genau das
schreibt die Mathematik als $f\colon D \to W$. Das Bild ist die Menge aller Werte, die
wirklich herauskommen können. Das Urbild ist eine Suchanfrage: „Gib mir alle Einträge,
deren Wert in $B$ liegt“, wie `SELECT * WHERE f(x) IN B` in einer Datenbank.
""")

# ── 1: Schreibweise ────────────────────────────────────────────────────────
k.erklaerung("Die Uni-Schreibweise für Funktionen", r"""
    ## Name, Definitionsbereich, Zielmenge, Vorschrift

    :::analogie 📋 Notenliste
    Jede Person im Kurs bekommt genau eine Note aus $\{1, 2, 3, 4, 5\}$. Die Personen
    sind die erlaubten Eingaben, die Noten die möglichen Ausgaben.
    :::

    Eine [[Funktion]] (auch [[Abbildung]]) $f$ von $D$ nach $W$ ordnet **jedem**
    $x \in D$ **genau ein** $y \in W$ zu. Man schreibt

    $$f\colon D \to W,\quad x \mapsto f(x).$$

    $D$ heißt [[Definitionsbereich|Definitionsmenge]], $W$ heißt [[Zielmenge]]. Das
    eingesetzte $x$ heißt Argument, $f(x)$ der [[Funktionswert]]. Die Vorkurs-Folien
    schreiben die Zielmenge $Z$, viele Bücher $W$. Gemeint ist dasselbe.

    :::rechnung $f\colon [-5, 3) \to \mathbb{R},\ x \mapsto 2x + 3$ an der Stelle $-5$
    2 \cdot (-5) + 3 = -10 + 3 || $-5$ liegt in $D = [-5, 3)$, also einsetzen
    = -7 || also $f(-5) = -7$
    :::

    Die Stelle $3$ darfst du **nicht** einsetzen: $3 \notin [-5, 3)$.

    :::alt Als Programm-Signatur
    `def f(x: float) -> float` sagt: Hinein darf eine Kommazahl, heraus kommt eine
    Kommazahl. Die Mathematik ist genauer: $[-5, 3)$ statt „irgendeine Zahl“. Der Pfeil
    $\to$ verbindet die Mengen, der Pfeil $\mapsto$ (mit Fuß) sagt, was mit einem
    einzelnen $x$ passiert.
    :::
    ---
    ## Nicht nur Zahlen

    Definitionsbereich und Zielmenge dürfen beliebige Mengen sein. Die Folien zeigen

    $$g\colon \{\text{Dreieck}, \text{Quadrat}, \text{Trapez}\} \to \mathbb{N} \times \mathbb{N},\quad x \mapsto (\text{Ecken von } x, \text{Kanten von } x).$$

    Es gilt $g(\text{Dreieck}) = (3, 3)$ und $g(\text{Quadrat}) = g(\text{Trapez}) = (4, 4)$.
    Zwei Eingaben mit demselben Wert sind erlaubt.

    Eine Funktion kann auch ein Paar als Eingabe haben:
    $h\colon \mathbb{R} \times \mathbb{R} \to \mathbb{R},\ (x, y) \mapsto \sqrt{x^2 + y^2}$
    liefert den Abstand des Punktes $(x, y)$ zum Ursprung.

    :::rechnung Abstand von $(3, 4)$ zum Ursprung
    \sqrt{3^2 + 4^2} = \sqrt{9 + 16} || $x = 3$, $y = 4$ einsetzen
    = \sqrt{25} || addieren
    = 5 || also $h(3, 4) = 5$
    :::

    :::alt Als Lagerliste
    Ein Lager ordnet jedem Artikel ein Paar (Regal, Fach) zu. Die Eingabe ist ein
    Artikel, keine Zahl, die Ausgabe ein Paar aus $\mathbb{N} \times \mathbb{N}$. Das
    ist eine Funktion, solange jeder Artikel genau einen Platz hat.
    :::
    """)

k.zahl("Gegeben ist $f\\colon [-5, 3) \\to \\mathbb{R},\\ x \\mapsto 2x + 3$. Berechne $f(-2)$.", -1,
       "Einsetzen: $2 \\cdot (-2) + 3 = -4 + 3 = -1$.",
       tipps=["Ersetze $x$ durch $(-2)$.", "$2 \\cdot (-2) = -4$.", "$-4 + 3$"],
       rechenweg=r"""
       :::rechnung
       2 \cdot (-2) + 3 = -4 + 3 || $-2 \in [-5, 3)$, also einsetzen
       = -1 || addieren
       :::
       """,
       typische_fehler=[(7, "Vorzeichenfehler: $2 \\cdot (-2) = -4$, nicht $+4$."),
                        (1, "Du hast $-3$ statt $+3$ gerechnet. Die Vorschrift lautet $2x + 3$.")])

k.mc("Was ist bei $f\\colon [-5, 3) \\to \\mathbb{R},\\ x \\mapsto 2x + 3$ der Definitionsbereich?",
     ["$[-5, 3)$", "$\\mathbb{R}$", "$[-7, 9)$", "$2x + 3$"],
     "Der Definitionsbereich steht links vom Pfeil $\\to$: $D = [-5, 3)$. Rechts steht die Zielmenge $\\mathbb{R}$.",
     tipps=["Links vom Pfeil $\\to$ steht, was hinein darf.", "Rechts vom Pfeil steht die Zielmenge."],
     fehler={"$\\mathbb{R}$": "$\\mathbb{R}$ ist die Zielmenge, sie steht rechts vom Pfeil. Hinein dürfen nur Zahlen aus $[-5, 3)$.",
             "$[-7, 9)$": "Das sind die Werte, die herauskommen (das Bild). Gefragt ist, was hinein darf.",
             "$2x + 3$": "Das ist die Vorschrift hinter $\\mapsto$, keine Menge."})

# ── 2: Wann ist es eine Funktion? ──────────────────────────────────────────
k.erklaerung("Wann ist eine Zuordnung keine Funktion?", r"""
    ## Zwei Bedingungen: jedes $x$, genau ein Wert

    Eine Zuordnung ist nur dann eine Funktion $f\colon D \to W$, wenn

    1. **jedes** $x \in D$ einen Wert bekommt und
    2. dieser Wert **eindeutig** ist (nicht zwei Werte).

    Die Folien nennen zwei Gegenbeispiele. „$x \mapsto$ Teiler von $x$“ auf $\mathbb{N}$ ist
    keine Funktion: $6$ hat mehrere Teiler. „$x \mapsto$ Kehrwert von $x$“ auf $\mathbb{R}$
    ist keine Funktion: $0$ hat keinen Kehrwert.

    :::rechnung Warum „Teiler von $6$“ nicht eindeutig ist
    6 = 1 \cdot 6 || $1$ und $6$ teilen $6$
    6 = 2 \cdot 3 || $2$ und $3$ teilen $6$ auch: vier Kandidaten, kein eindeutiger Wert
    :::

    Der [[maximale Definitionsbereich]] ist die größte Menge, auf der die Vorschrift
    sinnvoll ist. Für $x \mapsto \frac{1}{x}$ ist das $\mathbb{R} \setminus \{0\}$.

    :::visual funktionsgraph
    {"funktionen": [{"term": "1/x", "label": "1/x"}], "x": [-4, 4], "y": [-4, 4],
     "unterschrift": "Jede senkrechte Linie bei $x \\ne 0$ trifft den Graphen genau einmal. Bei $x = 0$ trifft sie ihn nie."}
    :::

    :::alt Mit dem Senkrechte-Linien-Test
    Am Graphen siehst du es sofort: Zieh bei jedem $x \in D$ eine senkrechte Linie.
    Trifft sie den Graphen genau einmal, passt alles. Trifft sie ihn zweimal (wie bei
    einem Kreis), gibt es zwei Werte. Trifft sie ihn gar nicht, fehlt der Wert, und
    dieses $x$ muss aus $D$ heraus.
    :::
    """)

k.mehrfach("Welche dieser Angaben sind Funktionen?",
           ["$f\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto x^2$",
            "$g\\colon \\mathbb{R} \\setminus \\{0\\} \\to \\mathbb{R},\\ x \\mapsto \\frac{1}{x}$",
            "$k\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto 5$"],
           ["$h\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto \\frac{1}{x}$",
            "$t\\colon \\mathbb{N} \\to \\mathbb{N},\\ x \\mapsto$ ein Teiler von $x$",
            "$w\\colon \\mathbb{R}_{\\ge 0} \\to \\mathbb{R},\\ x \\mapsto \\pm\\sqrt{x}$"],
           "Eine Funktion braucht für **jedes** $x \\in D$ **genau einen** Wert. Bei $h$ fehlt der Wert für $x = 0$, "
           "bei $t$ und $w$ gibt es mehrere Werte (zum Beispiel $w(4) = \\pm 2$). Eine konstante Vorschrift wie $x \\mapsto 5$ ist erlaubt.",
           tipps=["Prüfe jede Angabe: Hat jedes $x$ aus dem Definitionsbereich einen Wert?",
                  "Prüfe dann: Ist dieser Wert eindeutig?",
                  "Schau besonders auf $x = 0$ und auf Zeichen wie $\\pm$."],
           fehler={"$h\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto \\frac{1}{x}$":
                   "Bei $h$ ist $0 \\in D = \\mathbb{R}$, aber $\\frac{1}{0}$ gibt es nicht. Dann ist $h$ keine Funktion. Mit $D = \\mathbb{R} \\setminus \\{0\\}$ wäre alles in Ordnung.",
                   "$w\\colon \\mathbb{R}_{\\ge 0} \\to \\mathbb{R},\\ x \\mapsto \\pm\\sqrt{x}$":
                   "$\\pm\\sqrt{4}$ sind zwei Werte, $2$ und $-2$. Eine Funktion liefert genau einen."})

k.loesungsmenge("Bestimme den maximalen Definitionsbereich der Vorschrift $x \\mapsto \\sqrt{x - 3}$ "
                "(Eingabe als Intervall, zum Beispiel `[1; inf)`).",
                "[3; inf)",
                "Unter der Wurzel darf nichts Negatives stehen: $x - 3 \\ge 0$, also $x \\ge 3$. "
                "Der maximale Definitionsbereich ist $[3, \\infty)$.",
                tipps=["Wann ist $\\sqrt{\\ldots}$ erlaubt?", "Der Radikand muss $\\ge 0$ sein: $x - 3 \\ge 0$.",
                       "Löse nach $x$ auf. Die $3$ selbst ist erlaubt."],
                rechenweg=r"""
                :::rechnung
                x - 3 \ge 0 || Radikand nicht negativ
                x \ge 3 || $+3$ auf beiden Seiten
                :::

                Also $D = [3, \infty)$.
                """,
                typische_fehler=[("(3; inf)", "Die $3$ gehört dazu: $\\sqrt{3 - 3} = \\sqrt{0} = 0$ ist erlaubt."),
                                 ("[-3; inf)", "Vorzeichen: $x - 3 \\ge 0$ heißt $x \\ge 3$, nicht $x \\ge -3$.")])

# ── 3: Gleichheit ──────────────────────────────────────────────────────────
k.erklaerung("Wann sind zwei Funktionen gleich?", r"""
    ## Drei Dinge müssen passen

    Zwei Funktionen sind **gleich**, wenn Definitionsbereich, Zielmenge **und** alle
    Funktionswerte übereinstimmen. Die Vorschrift darf verschieden aussehen.

    $f, g\colon \mathbb{R} \to \mathbb{R}$ mit $f(x) = x^2 - 2x + 1$ und $g(x) = (x - 1)^2$
    sind gleich, denn die zweite binomische Formel macht aus dem einen Term den anderen:

    :::rechnung Gleiche Werte für jedes $x$
    (x - 1)^2 = x^2 - 2x + 1 || zweite binomische Formel
    :::

    Dagegen sind $f_1\colon \mathbb{R}_{\ge 0} \to \mathbb{R},\ x \mapsto x^2$ und
    $f_2\colon \mathbb{R} \to \mathbb{R},\ x \mapsto x^2$ **nicht** gleich, obwohl die
    Vorschrift dieselbe ist: $f_2(-1)$ gibt es, $f_1(-1)$ nicht.

    :::alt Mit zwei Programmen erklärt
    Zwei Programme sind austauschbar, wenn sie dieselben Eingaben annehmen und zu jeder
    Eingabe dasselbe ausgeben. Ob innen `(x-1)**2` oder `x*x - 2*x + 1` steht, ist egal.
    Nimmt aber eines nur positive Zahlen an, kannst du es nicht überall einsetzen, wo
    das andere stand.
    :::
    """)

k.wf("$f_1\\colon \\mathbb{R}_{\\ge 0} \\to \\mathbb{R},\\ x \\mapsto x^2$ und $f_2\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto x^2$ "
     "sind dieselbe Funktion.", False,
     "Die Vorschrift ist gleich, aber die Definitionsbereiche nicht: $-1$ liegt in $\\mathbb{R}$, aber nicht in $\\mathbb{R}_{\\ge 0}$. "
     "Zur Funktion gehören Definitionsbereich, Zielmenge und Vorschrift.",
     tipps=["Vergleiche nicht nur die Vorschrift, sondern auch die Mengen links vom Pfeil."])

# ── 4: Bild ────────────────────────────────────────────────────────────────
k.erklaerung("Das Bild einer Funktion", r"""
    ## Was kommt wirklich heraus?

    :::analogie 📽️ Beamer
    Die Leinwand ist die Zielmenge. Der Lichtfleck, den der Beamer wirklich erzeugt,
    ist das Bild. Oft ist er kleiner als die Leinwand.
    :::

    Zu $x \in D$ heißt $f(x)$ das **Bild von $x$**. Die Menge aller Funktionswerte heißt
    [[Bild]] (oder Bildmenge) von $f$:

    $$f(D) := \{f(x) : x \in D\} \subseteq W.$$

    Für eine Teilmenge $A \subseteq D$ ist $f(A) := \{f(x) : x \in A\}$.

    :::rechnung $f\colon \{-2, -1, 0, 1, 2\} \to \mathbb{Z},\ x \mapsto x^2$
    (-2)^2 = 4 || Bild von $-2$
    (-1)^2 = 1 || Bild von $-1$
    0^2 = 0 || Bild von $0$
    1^2 = 1 || schon dabei
    2^2 = 4 || schon dabei, also $f(D) = \{0, 1, 4\}$
    :::

    :::visual relation_graph
    {"links": [-2, -1, 0, 1, 2], "rechts": [0, 1, 2, 3, 4], "pfeile": [[-2, 4], [-1, 1], [0, 0], [1, 1], [2, 4]],
     "namen": ["D", "W"], "zeige": ["abbildung"],
     "unterschrift": "Getroffen werden nur $0$, $1$ und $4$. Das ist das Bild. $2$ und $3$ liegen in $W$, aber nicht im Bild."}
    :::

    :::alt Mit einer Strichliste erklärt
    Geh alle Eingaben durch und schreib jedes Ergebnis auf einen Zettel. Doppelte
    schreibst du nur einmal. Der Zettel ist das Bild. Bei $f\colon \mathbb{R} \to \mathbb{R},\ x \mapsto x^2$
    landen nur Zahlen $\ge 0$ darauf: $f(\mathbb{R}) = \mathbb{R}_{\ge 0}$. Die $-5$
    liegt nicht im Bild, weil kein $x$ mit $x^2 = -5$ existiert.
    :::
    ---
    ## Das Bild eines Intervalls

    Bei Intervallen hilft der Graph. Beispiel aus den Folien:
    $f\colon [-2, 6) \to \mathbb{R},\ x \mapsto x^2 - 4$.

    :::rechnung Die entscheidenden Stellen
    0^2 - 4 = -4 || tiefster Punkt, bei $x = 0 \in D$
    (-2)^2 - 4 = 0 || linker Rand
    6^2 - 4 = 32 || rechter Rand, wird nicht erreicht: $6 \notin D$
    :::

    Also ist $f([-2, 6)) = [-4, 32)$.

    :::visual funktionsgraph
    {"funktionen": [{"term": "x^2 - 4", "label": "f(x)"}], "x": [-3, 7], "y": [-6, 34],
     "punkte": [{"x": -2, "y": 0}, {"x": 0, "y": -4}, {"x": 6, "y": 32, "label": "(6 | 32), nicht erreicht"}],
     "unterschrift": "Nur der Teil über $[-2, 6)$ zählt. Lies auf der $y$-Achse ab, welche Höhen vorkommen."}
    :::

    :::achtung Nur die Ränder einsetzen
    Aus $f(-2) = 0$ und $f(6) = 32$ folgt **nicht** $[0, 32)$. Der Graph geht dazwischen
    bis $-4$ hinunter. Suche immer auch Tiefpunkte und Hochpunkte im Inneren.
    :::

    :::alt Mit Taschenlampe erklärt
    Leuchte vom Graphen waagerecht nach links auf die $y$-Achse. Jeder Punkt des
    Graphen wirft dort einen Schatten. Der ganze Schatten ist das Bild: von $-4$
    (Scheitel) bis knapp unter $32$.
    :::
    """)

k.menge("Gegeben ist $f\\colon \\{-2, -1, 0, 1, 2, 3\\} \\to \\mathbb{Z},\\ x \\mapsto x^2 + 1$. "
        "Bestimme das Bild $f(D)$. Eingabe zum Beispiel `{1; 2}`.",
        "{1; 2; 5; 10}",
        "Alle Werte: $f(-2) = 5$, $f(-1) = 2$, $f(0) = 1$, $f(1) = 2$, $f(2) = 5$, $f(3) = 10$. "
        "Jeder Wert zählt nur einmal: $f(D) = \\{1, 2, 5, 10\\}$.",
        tipps=["Setze jedes Element von $D$ ein.", "$(-2)^2 + 1 = 5$ und $2^2 + 1 = 5$: Doppelte zählen einmal.",
               "Es kommen vier verschiedene Werte heraus."],
        rechenweg=r"""
        :::rechnung
        (-2)^2 + 1 = 5 || Bild von $-2$
        (-1)^2 + 1 = 2 || Bild von $-1$
        0^2 + 1 = 1 || Bild von $0$
        1^2 + 1 = 2 || wie bei $-1$
        2^2 + 1 = 5 || wie bei $-2$
        3^2 + 1 = 10 || Bild von $3$
        :::
        """,
        typische_fehler=[("{-2; -1; 0; 1; 2; 3}", "Das ist der Definitionsbereich. Das Bild besteht aus den **Funktionswerten**."),
                         ("{5; 2; 1; 10; 0}", "Die $0$ kommt nicht heraus: $x^2 + 1 \\ge 1$ für jedes $x$.")])

k.loesungsmenge("Bestimme das Bild von $f\\colon [-1, 2] \\to \\mathbb{R},\\ x \\mapsto x^2$ als Intervall.",
                "[0; 4]",
                "Der Graph fällt von $f(-1) = 1$ bis zum Scheitel $f(0) = 0$ und steigt dann bis $f(2) = 4$. "
                "Alle Höhen von $0$ bis $4$ kommen vor: $f([-1, 2]) = [0, 4]$.",
                tipps=["Zeichne die Normalparabel nur über $[-1, 2]$.", "Der tiefste Punkt liegt bei $x = 0$, und $0 \\in [-1, 2]$.",
                       "Der höchste Punkt liegt am rechten Rand."],
                rechenweg=r"""
                :::rechnung
                0^2 = 0 || tiefster Wert, Scheitel bei $x = 0$
                (-1)^2 = 1 || linker Rand
                2^2 = 4 || rechter Rand, höchster Wert
                :::

                Also $f([-1, 2]) = [0, 4]$.
                """,
                typische_fehler=[("[1; 4]", "Du hast nur die Ränder eingesetzt. Dazwischen liegt der Scheitel mit $f(0) = 0$."),
                                 ("[-1; 2]", "Das ist der Definitionsbereich. Gefragt sind die Funktionswerte.")])

k.mc("Was ist das Bild von $f\\colon [-2, 6) \\to \\mathbb{R},\\ f(x) = x^2 - 4$?",
     ["$[-4, 32)$", "$[0, 32)$", "$[-4, \\infty)$", "$\\mathbb{R}$"],
     "Tiefster Wert $f(0) = -4$, der rechte Rand $f(6) = 32$ wird wegen $6 \\notin D$ nicht erreicht: $[-4, 32)$.",
     tipps=["Wo liegt der Scheitel der Parabel?", "$f(0) = -4$ ist der kleinste Wert.", "Wird $f(6) = 32$ erreicht?"],
     fehler={"$[0, 32)$": "Du hast nur die Ränder eingesetzt. Bei $x = 0$ ist $f(0) = -4$.",
             "$[-4, \\infty)$": "Das wäre das Bild auf ganz $\\mathbb{R}$. Hier ist $D = [-2, 6)$, größer als $32$ wird es nicht.",
             "$\\mathbb{R}$": "$\\mathbb{R}$ ist die Zielmenge. Das Bild ist meist kleiner."})

# ── 5: Urbild ──────────────────────────────────────────────────────────────
k.erklaerung("Das Urbild einer Menge", r"""
    ## Rückwärts fragen: Wer landet in $B$?

    :::analogie 🔎 Suchfilter
    In einem Onlineshop filterst du „Preis zwischen 10 und 20 Euro“. Angezeigt werden
    alle Artikel, deren Preis im Filter liegt. Das ist ein Urbild.
    :::

    Für $B \subseteq W$ heißt

    $$f^{-1}(B) := \{x \in D : f(x) \in B\} \subseteq D$$

    das [[Urbild]] von $B$. Ein $x$ mit $f(x) = y$ heißt Urbild von $y$. Ein $y$ kann
    **kein**, **genau ein** oder **mehrere** Urbilder haben.

    :::rechnung $f\colon \mathbb{R} \to \mathbb{R},\ x \mapsto x^2$: Urbild von $\{4\}$
    x^2 = 4 || alle $x$ mit $f(x) = 4$
    x_1 = -2 || erstes Urbild
    x_2 = 2 || zweites Urbild, also $f^{-1}(\{4\}) = \{-2, 2\}$
    :::

    Für $y < 0$ gibt es kein Urbild: $f^{-1}(\{-1\}) = \emptyset$.

    :::achtung $f^{-1}(B)$ ist keine Umkehrfunktion
    Das Urbild $f^{-1}(B)$ gibt es für **jede** Funktion und jede Menge $B$. Es ist eine
    Menge. Eine Umkehrfunktion braucht dagegen eine bijektive Funktion (nächstes Kapitel).
    $x^2$ hat auf $\mathbb{R}$ keine Umkehrfunktion, das Urbild $\{-2, 2\}$ trotzdem.
    :::

    :::alt Mit Höhenlinien erklärt
    Zeichne bei der Höhe $y = 4$ eine waagerechte Linie. Wo sie den Graphen schneidet,
    lies die $x$-Werte ab: $-2$ und $2$. Bei $y = -1$ schneidet sie nichts, bei $y = 0$
    genau einmal. Für eine Menge $B = [1, 4]$ nimmst du den ganzen Streifen zwischen
    den Höhen $1$ und $4$: $f^{-1}([1, 4]) = [-2, -1] \cup [1, 2]$.
    :::

    :::visual funktionsgraph
    {"funktionen": [{"term": "x^2", "label": "x^2"}, {"term": "4", "label": "y = 4", "farbe": 2},
                    {"term": "1", "label": "y = 1", "farbe": 3}],
     "x": [-3, 3], "y": [-2, 6], "punkte": [{"x": -2, "y": 4}, {"x": 2, "y": 4}],
     "unterschrift": "Alle $x$, deren Graphpunkt zwischen den Linien $y = 1$ und $y = 4$ liegt, bilden $f^{-1}([1, 4])$."}
    :::
    """)

k.menge("Gegeben ist $f\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto x^2$. Bestimme das Urbild $f^{-1}(\\{9\\})$.",
        "{-3; 3}",
        "Gesucht sind alle $x$ mit $x^2 = 9$. Das sind $-3$ und $3$.",
        tipps=["Gesucht sind alle $x$, deren Funktionswert $9$ ist.", "Löse $x^2 = 9$.",
               "Vergiss die negative Lösung nicht."],
        rechenweg=r"""
        :::rechnung
        x^2 = 9 || alle $x$ mit $f(x) = 9$
        x_1 = -3 || negative Lösung
        x_2 = 3 || positive Lösung
        :::
        """,
        typische_fehler=[("{3}", "Auch $(-3)^2 = 9$. Das Urbild enthält beide Lösungen."),
                         ("{81}", "Das ist das Bild von $9$, also $f(9)$. Beim Urbild fragst du rückwärts: Wer wird auf $9$ abgebildet?")])

k.mc("$f\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto x^2$ hat keine Umkehrfunktion. Was gilt für $f^{-1}(\\{4\\})$?",
     ["Es ist die Menge $\\{-2, 2\\}$",
      "Es existiert nicht, weil $f$ nicht umkehrbar ist",
      "Es ist die Zahl $2$",
      "Es ist $\\frac{1}{4}$"],
     "Das Urbild einer Menge existiert für jede Funktion. Es ist eine Menge: alle $x$ mit $x^2 = 4$, also $\\{-2, 2\\}$.",
     tipps=["$f^{-1}(B)$ ist als Menge $\\{x \\in D : f(x) \\in B\\}$ definiert.", "Braucht diese Definition eine Umkehrfunktion?"],
     fehler={"Es existiert nicht, weil $f$ nicht umkehrbar ist":
             "Das verwechselt Urbild und Umkehrfunktion. Das Urbild $\\{x \\in D : f(x) \\in B\\}$ gibt es immer.",
             "Es ist die Zahl $2$": "Ein Urbild ist eine Menge. Und $-2$ gehört auch dazu.",
             "Es ist $\\frac{1}{4}$": "$f^{-1}$ ist hier kein Kehrwert. Die hochgestellte $-1$ bedeutet „rückwärts“, nicht „hoch minus eins“."})

k.menge("$f\\colon \\{1, 2, 3, 4, 5, 6\\} \\to \\mathbb{N}_0$ ordnet jeder Zahl ihren Rest bei Division durch $3$ zu. "
        "Bestimme das Urbild $f^{-1}(\\{0\\})$.",
        "{3; 6}",
        "Rest $0$ heißt: durch $3$ teilbar. In $\\{1, \\ldots, 6\\}$ sind das $3$ und $6$.",
        tipps=["Berechne für jedes $x$ den Rest bei Division durch $3$.", "Rest $0$ heißt: $3$ teilt $x$.",
               "Zwei Zahlen erfüllen das."],
        rechenweg=r"""
        :::rechnung
        3 = 1 \cdot 3 + 0 || Rest $0$
        6 = 2 \cdot 3 + 0 || Rest $0$
        4 = 1 \cdot 3 + 1 || Rest $1$, wie bei $1$
        5 = 1 \cdot 3 + 2 || Rest $2$, wie bei $2$
        :::
        """,
        typische_fehler=[("{0}", "$\\{0\\}$ ist die Menge $B$ selbst. Gesucht sind die $x$, die auf $0$ abgebildet werden.")])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def _menge_tex(werte):
    return "\\{" + ", ".join(tex(F(w)) for w in sorted(werte)) + "\\}" if werte else "\\emptyset"


def _menge_text(werte):
    return "{" + "; ".join(str(w) for w in sorted(werte)) + "}"


# Vorschrift: (TeX mit X als Platzhalter, Python-Funktion)
_REGELN = [
    ("X^2", lambda x: x * x),
    ("|X|", abs),
    ("X^2 - 2 \\cdot X", lambda x: x * x - 2 * x),
    ("(X - 1)^2", lambda x: (x - 1) ** 2),
    ("3 - |X|", lambda x: 3 - abs(x)),
    ("X^2 + X", lambda x: x * x + x),
]


def _einsetzen(muster, x):
    return muster.replace("X", tk(F(x)))


def bild_urbild_endlich(rng):
    muster, fn = rng.choice(_REGELN)
    vorschrift = muster.replace("X", "x").replace("\\cdot x", "x")
    d = sorted(rng.sample(range(-3, 5), rng.randint(5, 7)))
    d_tex = _menge_tex(d)
    kopf = f"Gegeben ist $f\\colon D \\to \\mathbb{{Z}},\\ x \\mapsto {vorschrift}$ mit $D = {d_tex}$. "
    if rng.random() < 0.5:
        a = sorted(rng.sample(d, rng.randint(3, 4)))
        loesung = {fn(x) for x in a}
        zeilen = [(f"{_einsetzen(muster, x)} = {tex(F(fn(x)))}", f"Bild von ${tex(F(x))}$") for x in a]
        fehler = [(set(a), "Das ist die Menge $A$ selbst. Das Bild $f(A)$ besteht aus den **Funktionswerten** der Elemente von $A$."),
                  ({fn(x) for x in d}, "Das ist das Bild von ganz $D$. Gefragt ist nur $f(A)$.")]
        frage = kopf + f"Bestimme das Bild $f(A)$ für $A = {_menge_tex(a)}$. Eingabe zum Beispiel `{{1; 4}}`."
        tipps = ["Setze jedes Element von $A$ in die Vorschrift ein.",
                 f"Zum Beispiel ist $f({tex(F(a[0]))}) = {tex(F(fn(a[0])))}$.",
                 "Sammle alle Ergebnisse in einer Menge, Doppelte zählen einmal."]
        erkl = "Das Bild $f(A) = \\{f(x) : x \\in A\\}$ sammelt die Funktionswerte aller $x \\in A$."
    else:
        werte = sorted({fn(x) for x in d})
        b = set(rng.sample(werte, min(len(werte), rng.randint(1, 2))))
        if rng.random() < 0.5:
            b.add(min(werte) - rng.randint(1, 3))       # ein Wert ohne Urbild
        b = sorted(b)
        loesung = {x for x in d if fn(x) in b}
        zeilen = []
        for x in d:
            y = fn(x)
            grund = f"${tex(F(y))} \\in B$, also gehört ${tex(F(x))}$ dazu" if y in b else f"${tex(F(y))} \\notin B$"
            zeilen.append((f"{_einsetzen(muster, x)} = {tex(F(y))}", grund))
        fehler = [(set(b), "Das ist die Menge $B$ selbst. Das Urbild besteht aus den $x \\in D$, deren Wert in $B$ liegt."),
                  ({fn(x) for x in loesung}, "Das sind Funktionswerte. Gesucht sind die **Stellen** $x$, nicht die Werte."),
                  ({x for x in loesung if x >= 0}, "Es fehlen negative Stellen. Prüfe jedes Element von $D$, auch die negativen.")]
        frage = kopf + (f"Bestimme das Urbild $f^{{-1}}(B)$ für $B = {_menge_tex(b)}$. "
                        "Eingabe zum Beispiel `{-1; 2}`, leere Menge als `{}`.")
        tipps = ["Berechne $f(x)$ für jedes $x \\in D$.",
                 "Behalte genau die $x$, deren Funktionswert in $B$ liegt.",
                 f"Zum Beispiel ist $f({tex(F(d[0]))}) = {tex(F(fn(d[0])))}$."]
        erkl = "Das Urbild $f^{-1}(B) = \\{x \\in D : f(x) \\in B\\}$ sammelt alle Stellen, deren Wert in $B$ liegt."
    rest = [x for x in d if x not in loesung] if "Urbild" in frage else []
    if rest:
        x0 = rest[0]
        fehler.append((loesung | {x0}, f"${tex(F(x0))}$ gehört nicht dazu: $f({tex(F(x0))}) = {tex(F(fn(x0)))} \\notin B$."))
    if len(loesung) > 1:
        fehler.append((set(sorted(loesung)[:-1]), "Es fehlt ein Element. Prüfe jedes Element einzeln."))
    fehler = [(_menge_text(m), t) for m, t in fehler if m != loesung]
    gesehen, eindeutig = set(), []
    for m, t in fehler:
        if m not in gesehen:
            gesehen.add(m)
            eindeutig.append((m, t))
    return {"frage": frage, "loesung": _menge_text(loesung), "tipps": tipps,
            "rechenweg": _rechnung(zeilen), "erklaerung": erkl, "typische_fehler": eindeutig}


def _lin_tex(a):
    """x - a als TeX."""
    if a == 0:
        return "x"
    return f"x - {a}" if a > 0 else f"x + {-a}"


def max_definitionsbereich(rng):
    a = rng.choice([v for v in range(-6, 7) if v != 0])
    art = rng.choice(["wurzel", "wurzel_minus", "bruch", "bruch_quadrat", "wurzel_bruch"])
    if art == "wurzel":
        vor = f"\\sqrt{{{_lin_tex(a)}}}"
        loes, fehl = f"[{a}; inf)", [(f"(-inf; {a}]", "Falsche Richtung: $x - a \\ge 0$ heißt $x \\ge a$."),
                                     (f"[{-a}; inf)", "Vorzeichen: Die Grenze ist die Zahl, für die der Radikand $0$ wird.")]
        rw = [(f"{_lin_tex(a)} \\ge 0", "Radikand nicht negativ"), (f"x \\ge {a}", "nach $x$ auflösen")]
        tipps = ["Unter einer Wurzel darf nichts Negatives stehen.", f"Löse ${_lin_tex(a)} \\ge 0$.",
                 "Die Grenze selbst ist erlaubt: $\\sqrt{0} = 0$."]
    elif art == "wurzel_minus":
        vor = f"\\sqrt{{{a} - x}}"
        loes, fehl = f"(-inf; {a}]", [(f"[{a}; inf)", "Falsche Richtung: $a - x \\ge 0$ heißt $x \\le a$.")]
        rw = [(f"{a} - x \\ge 0", "Radikand nicht negativ"), (f"x \\le {a}", "$x$ auf die andere Seite bringen")]
        tipps = ["Unter einer Wurzel darf nichts Negatives stehen.", f"Löse ${a} - x \\ge 0$.",
                 "Beim Auflösen nach $x$ auf die Richtung achten."]
    elif art == "bruch":
        vor = f"\\frac{{1}}{{{_lin_tex(a)}}}"
        loes, fehl = f"R \\ {{{a}}}", [(f"{{{a}}}", "Das ist die **verbotene** Zahl. Gesucht sind alle erlaubten."),
                                        (f"R \\ {{{-a}}}", "Vorzeichen: Der Nenner wird $0$ für $x = " + str(a) + "$.")]
        rw = [(f"{_lin_tex(a)} = 0", "Nenner null setzen"), (f"x = {a}", "diese Stelle ist verboten")]
        tipps = ["Durch $0$ darf man nicht teilen.", f"Wann ist ${_lin_tex(a)} = 0$?", f"Nur $x = {a}$ ist verboten."]
    elif art == "bruch_quadrat":
        a = abs(a)
        vor = f"\\frac{{1}}{{x^2 - {a * a}}}"
        loes, fehl = f"R \\ {{-{a}; {a}}}", [(f"R \\ {{{a}}}", f"Auch $(-{a})^2 = {a * a}$. Es gibt zwei verbotene Stellen."),
                                             (f"R \\ {{{a * a}}}", f"Verboten sind die $x$ mit $x^2 = {a * a}$, nicht $x = {a * a}$.")]
        rw = [(f"x^2 - {a * a} = 0", "Nenner null setzen"), (f"x_1 = -{a}", "erste verbotene Stelle"),
              (f"x_2 = {a}", "zweite verbotene Stelle")]
        tipps = ["Durch $0$ darf man nicht teilen.", f"Löse $x^2 = {a * a}$.", "Es gibt zwei Lösungen."]
    else:
        b = a + rng.randint(1, 4)
        vor = f"\\frac{{\\sqrt{{{_lin_tex(a)}}}}}{{{_lin_tex(b)}}}"
        loes = f"[{a}; {b}) ∪ ({b}; inf)"
        fehl = [(f"[{a}; inf)", f"Der Nenner ${_lin_tex(b)}$ wird bei $x = {b}$ null. Diese Stelle muss heraus."),
                (f"R \\ {{{b}}}", f"Die Wurzel verlangt zusätzlich $x \\ge {a}$.")]
        rw = [(f"{_lin_tex(a)} \\ge 0", "Wurzel: Radikand nicht negativ"), (f"x \\ge {a}", "erste Bedingung")]
        tipps = ["Zwei Bedingungen: Wurzel und Nenner.", f"Wurzel: $x \\ge {a}$. Nenner: $x \\ne {b}$.",
                 "Nimm $[" + str(a) + ", \\infty)$ und entferne die verbotene Stelle."]
    rechenweg = _rechnung(rw)
    if art == "wurzel_bruch":
        rechenweg += f"\n\nDazu kommt der Nenner: ${_lin_tex(b)} \\ne 0$, also $x \\ne {b}$."
    return {"frage": f"Bestimme den maximalen Definitionsbereich der Vorschrift $x \\mapsto {vor}$. "
                     "Eingabe zum Beispiel `[2; inf)` oder `R \\ {1}`.",
            "loesung": loes, "tipps": tipps, "rechenweg": rechenweg,
            "erklaerung": "Der maximale Definitionsbereich enthält alle $x$, für die die Vorschrift einen Wert liefert: "
                          "kein Nenner $0$, nichts Negatives unter einer Wurzel.",
            "typische_fehler": fehl}


k.praxis()

k.generator(bild_urbild_endlich, typ="menge", titel="Bild und Urbild endlicher Funktionen")
k.generator(max_definitionsbereich, typ="loesungsmenge", titel="Maximaler Definitionsbereich")

k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: Bild und Urbild einer Parabel

    Gegeben ist $f\colon \mathbb{R} \to \mathbb{R},\ x \mapsto x^2 - 2x$.
    Bestimmen Sie das Bild $f([0, 3])$ und das Urbild $f^{-1}([0, 3])$.

    Hinweis: $f(x) = (x - 1)^2 - 1$.
    """,
    [{"typ": "zahl", "frage": "Welchen kleinsten Wert nimmt $f$ auf $[0, 3]$ an?", "loesung": -1,
      "tipps": ["Benutze $f(x) = (x - 1)^2 - 1$.", "Das Quadrat ist am kleinsten, wenn $x - 1 = 0$ ist.",
                "$x = 1$ liegt in $[0, 3]$."],
      "rechenweg": ":::rechnung\n1^2 - 2 \\cdot 1 = -1 || Scheitel bei $x = 1$\n:::",
      "typische_fehler": [(0, "$f(0) = 0$ ist der Wert am linken Rand. Im Inneren, bei $x = 1$, wird es kleiner.")]},
     {"typ": "loesungsmenge", "frage": "Gib das Bild $f([0, 3])$ als Intervall an.", "loesung": "[-1; 3]",
      "tipps": ["Der kleinste Wert ist $-1$.", "Berechne $f(0)$ und $f(3)$. Der größere ist der höchste Wert."],
      "rechenweg": ":::rechnung\n0^2 - 2 \\cdot 0 = 0 || linker Rand\n3^2 - 2 \\cdot 3 = 3 || rechter Rand, höchster Wert\n:::",
      "typische_fehler": [("[0; 3]", "Du hast nur die Randwerte genommen. Der Scheitelwert $-1$ gehört dazu.")]},
     {"typ": "loesungsmenge", "frage": "Gib das Urbild $f^{-1}([0, 3])$ an (zum Beispiel `[1; 2] ∪ [4; 5]`).",
      "loesung": "[-1; 0] ∪ [2; 3]",
      "tipps": ["Gesucht sind alle $x \\in \\mathbb{R}$ mit $0 \\le (x - 1)^2 - 1 \\le 3$.",
                "Das heißt $1 \\le (x - 1)^2 \\le 4$, also $1 \\le |x - 1| \\le 2$.",
                "Der Abstand von $x$ zur $1$ liegt zwischen $1$ und $2$."],
      "rechenweg": ":::rechnung\n(-1)^2 - 2 \\cdot (-1) = 3 || $x = -1$ landet auf $3$\n"
                   "2^2 - 2 \\cdot 2 = 0 || $x = 2$ landet auf $0$\n:::",
      "typische_fehler": [("[-1; 3]", "Du hast nur $f(x) \\le 3$ benutzt. Es muss auch $f(x) \\ge 0$ gelten, das schließt $(0, 2)$ aus."),
                          ("[0; 3]", "Das ist die Menge $B$ selbst. Gesucht sind die $x$, deren Wert in $[0, 3]$ liegt.")]}],
    "Das Bild findest du über Scheitel und Ränder. Beim Urbild löst du $0 \\le f(x) \\le 3$: "
    "$1 \\le |x - 1| \\le 2$ ergibt $[-1, 0] \\cup [2, 3]$. Das Urbild existiert, obwohl $f$ nicht umkehrbar ist.",
    uebungsblatt=True,
    tipps=["Schreibe $f$ in Scheitelpunktform.", "Für das Urbild: Wann liegt $(x - 1)^2 - 1$ zwischen $0$ und $3$?"],
    rechenweg=r"""
    :::rechnung
    x^2 - 2x = (x - 1)^2 - 1 || quadratische Ergänzung
    :::

    **Bild:** Auf $[0, 3]$ ist der kleinste Wert $f(1) = -1$, der größte $f(3) = 3$. Also $f([0, 3]) = [-1, 3]$.

    **Urbild:** $0 \le (x - 1)^2 - 1 \le 3 \iff 1 \le (x - 1)^2 \le 4 \iff 1 \le |x - 1| \le 2$.
    Das heißt $x \in [-1, 0]$ oder $x \in [2, 3]$, also $f^{-1}([0, 3]) = [-1, 0] \cup [2, 3]$.
    """)

k.papier(r"""
    ## Erklären wie in der Übung

    Betrachten Sie $f\colon \mathbb{R} \to \mathbb{R},\ x \mapsto x^2$.

    1. Geben Sie für jedes $y \in \mathbb{R}$ an, wie viele Urbilder $y$ hat (Fallunterscheidung).
    2. Bestimmen Sie $f^{-1}([1, 4])$ und $f(f^{-1}([1, 4]))$.
    3. Bestimmen Sie $f^{-1}(f([0, 1]))$. Ist das wieder $[0, 1]$?
    """,
    r"""
    **1.** $y < 0$: kein Urbild, denn $x^2 \ge 0$. $y = 0$: genau ein Urbild, $x = 0$.
    $y > 0$: zwei Urbilder, $x = \sqrt{y}$ und $x = -\sqrt{y}$.

    **2.** $1 \le x^2 \le 4 \iff 1 \le |x| \le 2$, also $f^{-1}([1, 4]) = [-2, -1] \cup [1, 2]$.
    Davon das Bild: $f([-2, -1] \cup [1, 2]) = [1, 4]$.

    **3.** $f([0, 1]) = [0, 1]$. Dann $f^{-1}([0, 1]) = \{x : x^2 \le 1\} = [-1, 1]$.
    Das ist **größer** als $[0, 1]$: Die negativen Zahlen kommen dazu, weil $f$ nicht
    injektiv ist. Im Allgemeinen gilt nur $A \subseteq f^{-1}(f(A))$.
    """,
    ["Ich habe die drei Fälle $y < 0$, $y = 0$, $y > 0$ unterschieden",
     "Ich habe $f^{-1}([1, 4]) = [-2, -1] \\cup [1, 2]$ mit beiden Teilen angegeben",
     "Ich habe erkannt, dass $f^{-1}(f([0, 1])) = [-1, 1]$ größer als $[0, 1]$ ist"],
    "Urbilder sind Mengen. Hin und zurück landet man nicht immer bei der Ausgangsmenge.",
    tipps=["Für 3.: Rechne erst $f([0, 1])$ aus und frage dann, welche $x \\in \\mathbb{R}$ dort landen."])

k.zusammenfassung(r"""
    ## Funktionen, Bild und Urbild

    | Begriff | Schreibweise | Bedeutung |
    |---|---|---|
    | Funktion | $f\colon D \to W,\ x \mapsto f(x)$ | jedem $x \in D$ genau ein $f(x) \in W$ |
    | Definitionsbereich | $D$ | was hinein darf |
    | Zielmenge | $W$ (Folien: $Z$) | wo die Werte liegen dürfen |
    | Bild | $f(A) = \{f(x) : x \in A\}$ | was herauskommt |
    | Urbild | $f^{-1}(B) = \{x \in D : f(x) \in B\}$ | wer in $B$ landet |

    - Gleich sind zwei Funktionen nur bei gleichem $D$, gleichem $W$ und gleichen Werten.
    - Maximaler Definitionsbereich: kein Nenner $0$, nichts Negatives unter $\sqrt{\phantom{x}}$.
    - Bild eines Intervalls: Ränder **und** Scheitel bzw. Hoch- und Tiefpunkte prüfen.

    !! Das Urbild $f^{-1}(B)$ gibt es immer. Es ist eine Menge, keine Umkehrfunktion.
""")
