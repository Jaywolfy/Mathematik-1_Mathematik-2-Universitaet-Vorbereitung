# -*- coding: utf-8 -*-
"""Vorkurs 11: Injektiv, surjektiv, bijektiv – Definitionen, Nachweis, Gegenbeispiel, Umkehrfunktion
(MVK 2026, VL 4–5)."""
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

tex = mathlib.tex
tk = mathlib.tex_klammer

k = neues_kapitel(
    slug="injektiv",
    titel="Injektiv, surjektiv, bijektiv",
    beschreibung="Wann eine Funktion keine Werte doppelt trifft, alles trifft oder umkehrbar ist",
    teil="vorkurs",
    quelle="MVK 2026, VL 4–5",
    icon="🔀")

k.lernziele([
    "Ich kann injektiv, surjektiv und bijektiv in Worten und mit Quantoren erklären",
    "Ich erkenne an Pfeildiagrammen und Graphen, welche der drei Eigenschaften vorliegen",
    "Ich kann Injektivität beweisen und mit einem Gegenbeispiel widerlegen, ebenso Surjektivität",
    "Ich kann entscheiden, ob eine Funktion umkehrbar ist, und die Umkehrfunktion bestimmen",
])

k.warum(r"""
Eine Hashfunktion bildet riesig viele Texte auf wenige Hashwerte ab. Sie **kann** nicht
injektiv sein, deshalb gibt es Kollisionen, und Hashtabellen müssen damit umgehen.
Eine Verschlüsselung dagegen **muss** injektiv sein: Würden zwei Klartexte denselben
Geheimtext ergeben, wüsste niemand, was gemeint war. Entschlüsseln ist dann die
Umkehrfunktion. Ein Primärschlüssel in einer Datenbank ist eine injektive Zuordnung von
Datensätzen auf Schlüssel.
""")

# ── 1: injektiv ────────────────────────────────────────────────────────────
k.erklaerung("Injektiv: kein Wert wird doppelt getroffen", r"""
    ## Höchstens ein Pfeil pro Ziel

    :::analogie 🧥 Garderobe
    Jede Jacke bekommt eine Marke. Zwei Jacken mit derselben Nummer wären ein Problem:
    Bei der Rückgabe wüsste niemand, welche gemeint ist.
    :::

    $f\colon D \to W$ heißt [[injektiv]], wenn für alle $x, \tilde{x} \in D$ gilt:

    $$f(x) = f(\tilde{x}) \ \Rightarrow\ x = \tilde{x}.$$

    In Worten: Gleiche Werte kommen nur von gleichen Stellen. Gleichwertig:
    Verschiedene Stellen haben verschiedene Werte.

    :::visual relation_graph
    {"links": [1, 2, 3, 4], "rechts": ["a", "b", "c", "d"], "pfeile": [[1, "a"], [2, "b"], [3, "b"], [4, "d"]],
     "namen": ["D", "W"], "zeige": ["injektiv"],
     "unterschrift": "Tippe auf „injektiv“: $b$ wird von $2$ und $3$ getroffen. Das verletzt die Injektivität."}
    :::

    :::rechnung $x \mapsto x^2$ auf $\mathbb{R}$ ist nicht injektiv
    (-1)^2 = 1 || Wert an der Stelle $-1$
    1^2 = 1 || derselbe Wert an der Stelle $1 \ne -1$
    :::

    :::alt Mit Matrikelnummern erklärt
    Jede Person an der TU hat eine Matrikelnummer, und keine Nummer gehört zwei
    Personen. Die Zuordnung Person $\mapsto$ Nummer ist injektiv. Vom Wert kommst du
    eindeutig zurück zur Person. Bei „Person $\mapsto$ Geburtstag“ geht das nicht: Viele
    teilen sich einen Geburtstag.
    :::
    """)

k.mehrfach("$f\\colon \\{1, 2, 3, 4\\} \\to \\{a, b, c\\}$ mit $f(1) = a$, $f(2) = b$, $f(3) = b$, $f(4) = c$. "
           "Welche Eigenschaften hat $f$?",
           ["surjektiv"], ["injektiv", "bijektiv"],
           "$a$, $b$ und $c$ werden alle getroffen, also ist $f$ surjektiv. $b$ wird zweimal getroffen "
           "($f(2) = f(3)$), also ist $f$ nicht injektiv und damit auch nicht bijektiv.",
           tipps=["Wird ein Element rechts mehrfach getroffen?", "Wird jedes Element rechts getroffen?",
                  "Bijektiv heißt: beides zugleich."],
           fehler={"injektiv": "$f(2) = b = f(3)$, aber $2 \\ne 3$. Zwei Stellen mit demselben Wert: nicht injektiv.",
                   "bijektiv": "Bijektiv verlangt injektiv **und** surjektiv. Injektiv ist $f$ nicht."})

# ── 2: surjektiv ───────────────────────────────────────────────────────────
k.erklaerung("Surjektiv: jeder Wert wird getroffen", r"""
    ## Mindestens ein Pfeil pro Ziel

    :::analogie 🎬 Kinosaal
    Jeder Platz ist besetzt. Dann ist die Zuordnung Person $\mapsto$ Platz surjektiv,
    egal ob zwei Kinder auf einem Platz sitzen.
    :::

    $f\colon D \to W$ heißt [[surjektiv]], wenn das Bild die ganze Zielmenge ist:
    $f(D) = W$. Mit Quantoren:

    $$\forall y \in W\ \exists x \in D : f(x) = y.$$

    Ob $f$ surjektiv ist, hängt also an der Zielmenge. $x \mapsto x^2$ ist als
    Funktion $\mathbb{R} \to \mathbb{R}$ nicht surjektiv, denn $-2$ wird nie getroffen:

    :::rechnung Ein Wert ohne Urbild
    0^2 = 0 || Quadrate sind nie negativ, also $x^2 \ge 0$ für alle $x$
    (\sqrt{7})^2 = 7 || jede Zahl $y \ge 0$ wird dagegen getroffen, hier $y = 7$
    :::

    Als Funktion $\mathbb{R} \to \mathbb{R}_{\ge 0}$ ist dieselbe Vorschrift surjektiv.
    Jede Funktion ist surjektiv auf ihr Bild.

    :::alt Mit Farbeimern erklärt
    Du hast Kinder ($D$) und Farbeimer ($W$). Jedes Kind taucht den Pinsel in genau einen
    Eimer. Surjektiv heißt: Am Ende ist **jeder** Eimer benutzt. Bleibt ein Eimer sauber,
    ist die Zuordnung nicht surjektiv.
    :::
    ---
    ## Bijektiv: genau ein Pfeil pro Ziel

    $f$ heißt [[bijektiv]], wenn $f$ injektiv **und** surjektiv ist. Zählst du die
    Urbilder eines $y \in W$:

    | Eigenschaft | jedes $y \in W$ hat … Urbilder |
    |---|---|
    | injektiv | höchstens ein |
    | surjektiv | mindestens ein |
    | bijektiv | genau ein: $\forall y \in W\ \exists!\, x \in D : f(x) = y$ |

    $\exists!$ liest man „es gibt genau ein“. Jede injektive Funktion ist auf ihrem
    Bild bijektiv.

    :::visual relation_graph
    {"links": [1, 2, 3], "rechts": ["a", "b", "c"], "pfeile": [[1, "b"], [2, "c"], [3, "a"]],
     "namen": ["D", "W"], "zeige": ["injektiv", "surjektiv", "bijektiv"],
     "unterschrift": "Jedes Ziel hat genau einen Pfeil: bijektiv."}
    :::

    :::alt Mit Tanzpaaren erklärt
    Beim Tanzkurs bekommt jede Person links genau eine Person rechts. Niemand rechts
    tanzt mit zwei (injektiv), und niemand rechts bleibt allein (surjektiv). Dann gehen
    alle Paare glatt auf: bijektiv. Das geht nur, wenn beide Seiten gleich viele
    Personen haben.
    :::
    """)

k.wf("Eine Funktion $f\\colon \\{1, 2, 3, 4\\} \\to \\{a, b, c\\}$ kann injektiv sein.", False,
     "Vier Stellen, aber nur drei Werte: Mindestens ein Wert wird doppelt getroffen (Schubfachprinzip). "
     "Darum kann eine Hashfunktion von vielen Texten auf wenige Hashwerte nie injektiv sein.",
     tipps=["Verteile vier Pfeile auf drei Ziele. Muss eines doppelt getroffen werden?"])

k.zuordnen("Ordne jeder Funktion ihre Eigenschaften zu.",
           [("$f\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto x^2$", "weder injektiv noch surjektiv"),
            ("$f\\colon \\mathbb{R}_{\\ge 0} \\to \\mathbb{R},\\ x \\mapsto x^2$", "injektiv, nicht surjektiv"),
            ("$f\\colon \\mathbb{R} \\to \\mathbb{R}_{\\ge 0},\\ x \\mapsto x^2$", "surjektiv, nicht injektiv"),
            ("$f\\colon \\mathbb{R}_{\\ge 0} \\to \\mathbb{R}_{\\ge 0},\\ x \\mapsto x^2$", "bijektiv")],
           "Injektiv wird $x^2$ erst, wenn negative Stellen fehlen ($D = \\mathbb{R}_{\\ge 0}$). "
           "Surjektiv wird es erst, wenn die Zielmenge nur $\\mathbb{R}_{\\ge 0}$ ist.",
           tipps=["Nur Definitionsbereich und Zielmenge ändern sich, die Vorschrift bleibt $x^2$."])

# ── 3: Ein Beispiel, drei Ergebnisse ───────────────────────────────────────
k.erklaerung("Dieselbe Vorschrift, andere Mengen", r"""
    ## $x \mapsto x^2$ dreimal

    Die Folien zeigen, dass Definitionsbereich und Zielmenge die Eigenschaften
    entscheiden:

    | Funktion | Ergebnis |
    |---|---|
    | $\mathbb{R} \to \mathbb{R}$ | weder injektiv noch surjektiv |
    | $\mathbb{R}_{\ge 0} \to \mathbb{R}$ | injektiv, nicht surjektiv |
    | $\mathbb{R}_{\ge 0} \to \mathbb{R}_{\ge 0}$ | bijektiv |

    :::visual funktionsgraph
    {"funktionen": [{"term": "x^2", "label": "x^2"}, {"term": "1", "label": "y = 1", "farbe": 2}],
     "x": [-3, 3], "y": [-3, 6], "punkte": [{"x": -1, "y": 1}, {"x": 1, "y": 1}],
     "unterschrift": "Die Linie $y = 1$ trifft den Graphen zweimal. Streichst du die linke Hälfte ($x < 0$), trifft jede Linie $y \\ge 0$ genau einmal."}
    :::

    :::rechnung Warum $\mathbb{R}_{\ge 0} \to \mathbb{R}_{\ge 0}$ surjektiv ist
    (\sqrt{5})^2 = 5 || zu $y = 5$ ist $x = \sqrt{5} \ge 0$ ein Urbild
    (\sqrt{0})^2 = 0 || auch $y = 0$ wird getroffen
    :::

    !! Waagerechte-Linien-Test: Jede waagerechte Linie auf Höhe $y \in W$ trifft den Graphen bei injektiv höchstens einmal, bei surjektiv mindestens einmal.

    :::alt Mit einem Zuschnitt erklärt
    Stell dir die Parabel als Draht vor. Schneidest du die linke Hälfte ab, gibt es zu
    jeder Höhe nur noch einen Punkt: injektiv. Dann schneidest du die Zielmenge zu, bis
    sie nur noch die Höhen enthält, die der Draht erreicht. Jetzt passt alles genau:
    bijektiv.
    :::
    """)

k.mc("Für welche Wahl ist $f\\colon D \\to W,\\ x \\mapsto \\sin(x)$ bijektiv?",
     ["$D = [-\\frac{\\pi}{2}, \\frac{\\pi}{2}]$, $W = [-1, 1]$",
      "$D = [-\\pi, \\pi]$, $W = [-1, 1]$",
      "$D = [-\\frac{\\pi}{2}, \\frac{\\pi}{2}]$, $W = \\mathbb{R}$",
      "$D = \\mathbb{R}$, $W = \\mathbb{R}$"],
     "Auf $[-\\frac{\\pi}{2}, \\frac{\\pi}{2}]$ steigt der Sinus streng von $-1$ bis $1$: jeder Wert einmal. "
     "Mit $W = [-1, 1]$ wird auch jeder Wert getroffen.",
     tipps=["Skizziere den Sinus von $-\\pi$ bis $\\pi$.", "Wo steigt er nur, ohne umzukehren?",
            "Die Zielmenge darf nur die Werte enthalten, die wirklich vorkommen."],
     fehler={"$D = [-\\pi, \\pi]$, $W = [-1, 1]$": "Surjektiv ja, aber nicht injektiv: $\\sin(0) = \\sin(\\pi) = 0$.",
             "$D = [-\\frac{\\pi}{2}, \\frac{\\pi}{2}]$, $W = \\mathbb{R}$": "Injektiv ja, aber $2 \\in \\mathbb{R}$ wird nie getroffen: nicht surjektiv.",
             "$D = \\mathbb{R}$, $W = \\mathbb{R}$": "Weder noch: $\\sin(0) = \\sin(\\pi)$, und Werte über $1$ kommen nie vor."})

k.erklaerung("Der Sinus aus den Folien", r"""
    ## Mengen passend wählen

    Die Folien stellen die Aufgabe: Wähle $D$ und $W$ so, dass $x \mapsto \sin(x)$
    (i) surjektiv, aber nicht injektiv, (ii) injektiv, aber nicht surjektiv,
    (iii) bijektiv ist.

    | $f\colon D \to W$ | Ergebnis | Grund |
    |---|---|---|
    | $[-\pi, \pi] \to [-1, 1]$ | surjektiv, nicht injektiv | $\sin(0) = \sin(\pi) = 0$ |
    | $[-\frac{\pi}{2}, \frac{\pi}{2}] \to \mathbb{R}$ | injektiv, nicht surjektiv | $2$ wird nie getroffen |
    | $[-\frac{\pi}{2}, \frac{\pi}{2}] \to [-1, 1]$ | bijektiv | steigt einmal von $-1$ bis $1$ |

    :::visual funktionsgraph
    {"funktionen": [{"term": "sin(x)", "label": "sin(x)"}], "x": [-3.5, 3.5], "y": [-2, 2],
     "punkte": [{"x": "-pi/2", "y": -1, "label": "(-π/2 | -1)"}, {"x": "pi/2", "y": 1, "label": "(π/2 | 1)"}],
     "unterschrift": "Zwischen den markierten Punkten steigt der Sinus nur. Dort ist er injektiv."}
    :::

    :::alt Mit einer Achterbahn erklärt
    Die Sinuskurve ist eine Achterbahn, die auf und ab fährt. Auf einer langen Strecke
    erreicht sie dieselbe Höhe mehrmals. Nimmst du nur ein Stück, auf dem sie immer
    bergauf fährt, kommt jede Höhe einmal vor. Genau so ein Stück ist
    $[-\frac{\pi}{2}, \frac{\pi}{2}]$.
    :::
    """)

# ── 4: Beweisen und widerlegen ─────────────────────────────────────────────
k.erklaerung("Injektivität beweisen oder widerlegen", r"""
    ## Das Rezept

    **Beweisen:** Nimm zwei beliebige Stellen $x_1, x_2 \in D$ mit $f(x_1) = f(x_2)$.
    Forme um, bis $x_1 = x_2$ dasteht.

    :::rechnung $f\colon \mathbb{R} \to \mathbb{R},\ x \mapsto 3x - 2$
    3x_1 - 2 = 3x_2 - 2 || Annahme $f(x_1) = f(x_2)$
    3x_1 = 3x_2 || $+2$ auf beiden Seiten
    x_1 = x_2 || durch $3 \ne 0$ teilen, also ist $f$ injektiv
    :::

    **Widerlegen:** Ein einziges Gegenbeispiel genügt: zwei verschiedene Stellen mit
    gleichem Wert, zum Beispiel $f(-1) = f(1)$ bei $x^2$ auf $\mathbb{R}$.

    :::achtung Beispiele beweisen nichts
    $f(1) \ne f(2)$ zeigt nicht, dass $f$ injektiv ist. Die Aussage gilt für **alle**
    Paare. Ein Beweis muss mit beliebigen $x_1, x_2$ arbeiten. Nur das Widerlegen geht
    mit einem einzigen Beispiel.
    :::

    :::alt Wie ein Test im Code
    Ein Unit-Test mit zwei Eingaben findet Fehler, beweist aber keine Korrektheit. Für
    „nicht injektiv“ reicht ein fehlschlagender Test: zwei Eingaben, gleiche Ausgabe.
    Für „injektiv“ brauchst du ein Argument, das für jede Eingabe gilt, wie die
    Umformung links.
    :::
    ---
    ## Ein Beweis aus den Folien

    Die Folien zeigen: $x \mapsto x^2$ ist auf $\mathbb{R}_{\ge 0}$ injektiv. Seien
    $x_1, x_2 \ge 0$ mit $x_1^2 = x_2^2$. Ist $x_1 = x_2 = 0$, ist nichts zu zeigen. Sonst
    ist $x_1 + x_2 > 0$, und du darfst durch $x_1 + x_2$ teilen:

    :::rechnung
    x_1^2 = x_2^2 || Annahme
    x_1^2 - x_2^2 = 0 || alles auf eine Seite
    (x_1 - x_2)(x_1 + x_2) = 0 || dritte binomische Formel
    x_1 - x_2 = 0 || durch $x_1 + x_2 > 0$ teilen
    x_1 = x_2 || also injektiv
    :::

    Auf ganz $\mathbb{R}$ scheitert genau der vorletzte Schritt: $x_1 + x_2$ kann $0$
    sein, etwa bei $x_1 = -1$, $x_2 = 1$.

    :::alt Mit Abständen erklärt
    $x^2$ misst, wie weit $x$ von $0$ entfernt ist (im Quadrat). Zwei Zahlen haben
    denselben Abstand, wenn sie gleich sind oder Spiegelbilder wie $-1$ und $1$. Sind
    nur Zahlen $\ge 0$ erlaubt, gibt es keine Spiegelbilder mehr.
    :::
    """)

k.ordnen("Bringe den Beweis, dass $f\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto 5x + 1$ injektiv ist, in die richtige Reihenfolge. "
         "Zwei Zeilen gehören nicht dazu.",
         ["Seien $x_1, x_2 \\in \\mathbb{R}$ mit $f(x_1) = f(x_2)$.",
          "Dann gilt $5x_1 + 1 = 5x_2 + 1$.",
          "Auf beiden Seiten $1$ abziehen: $5x_1 = 5x_2$.",
          "Durch $5 \\ne 0$ teilen: $x_1 = x_2$.",
          "Also ist $f$ injektiv. $\\square$"],
         "Ein Injektivitätsbeweis startet mit beliebigen $x_1, x_2$ und gleichen Werten und endet bei $x_1 = x_2$.",
         ablenker=["Es ist $f(1) = 6 \\ne 11 = f(2)$, also ist $f$ injektiv.",
                   "Setze $x_1 = 0$ und $x_2 = 1$."],
         tipps=["Am Anfang steht die Annahme mit beliebigen Stellen.", "Konkrete Zahlen beweisen nichts."])

k.zahl("$f\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto x^2 - 4x$ ist nicht injektiv. Finde eine Stelle $x \\ne 1$ mit $f(x) = f(1)$.",
       3,
       "$f(1) = -3$. Gesucht ist $x^2 - 4x = -3$, also $x^2 - 4x + 3 = (x - 1)(x - 3) = 0$. Neben $1$ ist $x = 3$ eine Lösung. "
       "Damit ist $f(1) = f(3)$ ein Gegenbeispiel.",
       tipps=["Berechne zuerst $f(1)$.", "Löse $x^2 - 4x = -3$.", "$x^2 - 4x + 3 = (x - 1)(x - 3)$."],
       rechenweg=r"""
       :::rechnung
       1^2 - 4 \cdot 1 = -3 || Wert an der Stelle $1$
       x^2 - 4x = -3 || gleicher Wert gesucht
       x^2 - 4x + 3 = 0 || $+3$
       (x - 1)(x - 3) = 0 || faktorisieren
       x_1 = 1 || die Stelle, die wir schon kennen
       x_2 = 3 || die gesuchte zweite Stelle
       :::
       """,
       typische_fehler=[(-3, "$-3$ ist der **Wert** $f(1)$. Gesucht ist eine zweite **Stelle** mit diesem Wert."),
                        (1, "Die Stelle $1$ selbst zählt nicht. Gesucht ist ein $x \\ne 1$.")])

# ── 5: Umkehrfunktion ──────────────────────────────────────────────────────
k.erklaerung("Die Umkehrfunktion", r"""
    ## Rückwärts rechnen

    Ist $f\colon D \to W$ bijektiv, hat jedes $y \in W$ genau ein Urbild. Dann definiert

    $$f^{-1}\colon W \to D,\quad y \mapsto \text{das } x \in D \text{ mit } f(x) = y$$

    eine Funktion, die [[Umkehrfunktion]]. Es gilt $f^{-1}(f(x)) = x$ für alle $x \in D$,
    $f(f^{-1}(y)) = y$ für alle $y \in W$, und $f^{-1}$ ist wieder bijektiv mit
    $(f^{-1})^{-1} = f$.

    **Bestimmen:** Löse $y = f(x)$ nach $x$ auf.

    :::rechnung $f\colon \mathbb{R} \to \mathbb{R},\ x \mapsto 3x - 2$
    y = 3x - 2 || Ansatz
    y + 2 = 3x || $+2$
    x = \frac{y + 2}{3} || durch $3$, also $f^{-1}(y) = \frac{y + 2}{3}$
    :::

    Probe: $3 \cdot \frac{y + 2}{3} - 2 = y$. Aus den Folien: $x^2$ auf $\mathbb{R}_{\ge 0} \to \mathbb{R}_{\ge 0}$
    hat $f^{-1}(y) = \sqrt{y}$, und $x \mapsto 3x$ hat $y \mapsto \frac{1}{3}y$.

    :::achtung Zwei Verwechslungen
    $f^{-1}(y)$ ist **nicht** $\frac{1}{f(y)}$. Und das Urbild $f^{-1}(B)$ einer Menge gibt
    es immer, die Umkehrfunktion $f^{-1}$ nur, wenn $f$ bijektiv ist.
    :::

    :::alt Mit Verschlüsselung erklärt
    Die Caesar-Verschiebung macht aus jedem Buchstaben den dritten danach: A wird D.
    Das ist bijektiv auf dem Alphabet. Entschlüsseln heißt drei zurück: D wird A. Das
    Entschlüsseln ist die Umkehrfunktion. Erst ver-, dann entschlüsseln gibt den
    Klartext zurück: $f^{-1}(f(x)) = x$.
    :::
    """)

k.term("Bestimme die Umkehrfunktion von $f\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto 4x + 6$. "
       "Gib $f^{-1}(y)$ als Term in $y$ an.",
       "(y - 6)/4",
       "Aus $y = 4x + 6$ folgt $y - 6 = 4x$ und $x = \\frac{y - 6}{4}$.",
       variablen="y",
       tipps=["Setze $y = 4x + 6$ an.", "Bring die $6$ auf die andere Seite.", "Teile durch $4$."],
       rechenweg=r"""
       :::rechnung
       y = 4x + 6 || Ansatz
       y - 6 = 4x || $-6$
       x = \frac{y - 6}{4} || durch $4$
       :::
       """,
       typische_fehler=[("(y + 6)/4", "Vorzeichen: Die $+6$ wird durch $-6$ rückgängig gemacht."),
                        ("y/4 - 6", "Reihenfolge: Erst $6$ abziehen, dann durch $4$ teilen. $\\frac{y}{4} - 6$ macht es umgekehrt."),
                        ("1/(4y + 6)", "$f^{-1}$ ist nicht der Kehrwert $\\frac{1}{f}$. Löse $y = 4x + 6$ nach $x$ auf.")])

k.mc("Welche Aussage über $f\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto x^2$ stimmt?",
     ["$f$ hat keine Umkehrfunktion, aber $f^{-1}(\\{4\\}) = \\{-2, 2\\}$",
      "$f^{-1}(y) = \\sqrt{y}$ ist die Umkehrfunktion",
      "$f^{-1}(\\{4\\})$ existiert nicht",
      "$f^{-1}(x) = \\frac{1}{x^2}$"],
     "$f$ ist auf $\\mathbb{R}$ weder injektiv noch surjektiv, also nicht umkehrbar. Das Urbild einer Menge existiert trotzdem.",
     tipps=["Ist $f$ bijektiv?", "Das Urbild einer Menge braucht keine Umkehrfunktion."],
     fehler={"$f^{-1}(y) = \\sqrt{y}$ ist die Umkehrfunktion": "$\\sqrt{y}$ liefert nur die positive Stelle, und für $y < 0$ gar nichts. "
             "Umkehrfunktion ist $\\sqrt{y}$ erst für $f\\colon \\mathbb{R}_{\\ge 0} \\to \\mathbb{R}_{\\ge 0}$.",
             "$f^{-1}(\\{4\\})$ existiert nicht": "Das Urbild einer Menge gibt es immer: alle $x$ mit $x^2 \\in \\{4\\}$.",
             "$f^{-1}(x) = \\frac{1}{x^2}$": "Die $-1$ oben heißt „Umkehrung“, nicht „Kehrwert“."})


# ── Praxis ─────────────────────────────────────────────────────────────────
def _rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def injektiv_pfeile(rng):
    fall = rng.choice(["inj", "sur", "bij", "keins"])
    while True:
        n = rng.randint(3, 5)
        if fall == "bij":
            m = n
        elif fall == "inj":
            m = n + rng.randint(1, 2)
        elif fall == "sur":
            m = max(2, n - rng.randint(1, 2))
        else:
            m = rng.randint(3, 5)
        links = list(range(1, n + 1))
        rechts = ["a", "b", "c", "d", "p", "q", "r"][:m]
        if fall in ("inj", "bij"):
            werte = rng.sample(rechts, n)
        else:
            werte = [rng.choice(rechts) for _ in links]
        inj = len(set(werte)) == n
        sur = set(werte) == set(rechts)
        ist = "bij" if inj and sur else "inj" if inj else "sur" if sur else "keins"
        if ist == fall:
            break
    zuordnung = ",\\ ".join(f"f({x}) = {y}" for x, y in zip(links, werte))
    richtig = [e for e, ok in (("injektiv", inj), ("surjektiv", sur), ("bijektiv", inj and sur)) if ok]
    falsch = [e for e in ("injektiv", "surjektiv", "bijektiv") if e not in richtig]
    doppelt = next((y for y in rechts if werte.count(y) > 1), None)
    fehlt = next((y for y in rechts if y not in werte), None)
    fehler = {}
    if doppelt:
        stellen = [str(x) for x, y in zip(links, werte) if y == doppelt]
        fehler["injektiv"] = f"${doppelt}$ wird von ${stellen[0]}$ und ${stellen[1]}$ getroffen. Das ist nicht injektiv."
    if fehlt:
        fehler["surjektiv"] = f"${fehlt}$ wird von keinem Pfeil getroffen. Das ist nicht surjektiv."
    if "bijektiv" in falsch:
        fehler["bijektiv"] = "Bijektiv verlangt injektiv **und** surjektiv. Mindestens eins davon fehlt."
    erkl = []
    erkl.append("Kein Wert wird doppelt getroffen: injektiv." if inj else f"${doppelt}$ wird mehrfach getroffen: nicht injektiv.")
    erkl.append("Jeder Wert wird getroffen: surjektiv." if sur else f"${fehlt}$ wird nie getroffen: nicht surjektiv.")
    rechts_tex = "\\{" + ", ".join(rechts) + "\\}"
    return {"typ": "mehrfach",
            "frage": f"$f\\colon \\{{1, \\ldots, {n}\\}} \\to {rechts_tex}$ ist gegeben durch ${zuordnung}$. "
                     "Welche Eigenschaften hat $f$? (Es kann auch keine zutreffen.)",
            "richtig": richtig, "falsch": falsch, "fehler": fehler,
            "tipps": ["Zeichne ein Pfeildiagramm.", "Injektiv: Wird ein Wert rechts doppelt getroffen?",
                      "Surjektiv: Bleibt rechts ein Wert ohne Pfeil?"],
            "erklaerung": " ".join(erkl)}


def _lin(a, b, var="x"):
    """a·var + b als TeX."""
    t = (f"{var}" if a == 1 else f"-{var}" if a == -1 else f"{a}{var}")
    return t if b == 0 else f"{t} + {b}" if b > 0 else f"{t} - {-b}"


def umkehrfunktion_bestimmen(rng):
    art = rng.choice(["linear", "linear", "bruch"])
    if art == "linear":
        a = rng.choice([v for v in range(-6, 7) if v not in (0, 1, -1)])
        b = rng.choice([v for v in range(-9, 10) if v != 0])
        f_tex, d_tex, w_tex = _lin(a, b), "\\mathbb{R}", "\\mathbb{R}"
        loes = f"(y - ({b}))/({a})"
        rw = [(f"y = {_lin(a, b)}", "Ansatz $y = f(x)$"),
              (f"y {'-' if b > 0 else '+'} {abs(b)} = {a}x", f"${'-' if b > 0 else '+'}{abs(b)}$ auf beiden Seiten"),
              (f"x = \\frac{{y {'-' if b > 0 else '+'} {abs(b)}}}{{{a}}}", f"durch ${a}$ teilen")]
        fehler = [(f"(y + ({b}))/({a})", f"Vorzeichen: ${'+' if b > 0 else '-'}{abs(b)}$ wird durch die Gegenoperation rückgängig gemacht."),
                  (f"y/({a}) - ({b})", "Reihenfolge: Erst die Zahl auf die andere Seite bringen, dann teilen."),
                  (f"1/({a}y + ({b}))", "$f^{-1}$ ist nicht der Kehrwert von $f$.")]
        tipps = [f"Setze $y = {_lin(a, b)}$ an.", "Bring die Zahl ohne $x$ auf die andere Seite.", f"Teile durch ${a}$."]
    else:
        a = rng.choice([v for v in range(-6, 7) if v != 0])
        c = rng.choice(range(-4, 5))
        b = rng.choice(range(-4, 5))
        nenner = _lin(1, -c)
        f_tex = f"\\frac{{{a}}}{{{nenner}}}" + ("" if b == 0 else f" + {b}" if b > 0 else f" - {-b}")
        d_tex = f"\\mathbb{{R}} \\setminus \\{{{c}\\}}"
        w_tex = f"\\mathbb{{R}} \\setminus \\{{{b}\\}}"
        loes = f"({c}) + ({a})/(y - ({b}))"
        yb = _lin(1, -b, "y")
        rw = [(f"y = {f_tex}", "Ansatz $y = f(x)$"),
              (f"{yb} = \\frac{{{a}}}{{{nenner}}}", f"${'-' if b > 0 else '+'}{abs(b)}$ auf beiden Seiten" if b else "der Bruch steht schon allein"),
              (f"{nenner} = \\frac{{{a}}}{{{yb}}}", f"Kehrwert auf beiden Seiten, erlaubt wegen $y \\ne {b}$"),
              (f"x = {c} + \\frac{{{a}}}{{{yb}}}" if c else f"x = \\frac{{{a}}}{{{yb}}}",
               f"${'+' if c > 0 else '-'}{abs(c)}$ auf beiden Seiten" if c else "fertig")]
        fehler = [(f"({a})/(y - ({b})) - ({c})", f"Vorzeichen: Aus $x - {tk(F(c))}$ wird $x$, indem du ${tk(F(c))}$ **addierst**."),
                  (f"1/({a}/(y - ({c})) + ({b}))", "$f^{-1}$ ist nicht der Kehrwert von $f$.")]
        tipps = ["Setze $y = f(x)$ an und isoliere den Bruch.", "Nimm auf beiden Seiten den Kehrwert.",
                 f"Am Ende ${tk(F(c))}$ addieren."]
    return {"frage": f"$f\\colon {d_tex} \\to {w_tex},\\ x \\mapsto {f_tex}$ ist bijektiv. "
                     "Bestimme die Umkehrfunktion und gib $f^{-1}(y)$ als Term in $y$ an.",
            "loesung": loes, "variablen": "y", "tipps": tipps, "rechenweg": _rechnung(rw),
            "erklaerung": "Umkehrfunktion: $y = f(x)$ nach $x$ auflösen. Probe: $f(f^{-1}(y)) = y$.",
            "typische_fehler": ohne_gleiche(loes, fehler)}


def _probe_umkehr(d):
    """Gegenprobe: f(f^{-1}(y)) = y an einigen Stellen (aus dem Rechenweg-Ansatz)."""
    from .. import pruefer
    ansatz = d["rechenweg"].split("\n")[1].split("||")[0].strip()
    rechts = ansatz.split("=", 1)[1]
    f_ast = pruefer.parse(pruefer.latex_zu_term(rechts), ["x"]).ast
    g_ast = pruefer.parse(d["loesung"], ["y"]).ast
    for y in (F(7, 3), F(-5, 2), F(11, 7)):
        try:
            x = pruefer.wert(g_ast, {"y": y})
            if not pruefer.gleich(pruefer.wert(f_ast, {"x": x}), y):
                return False
        except pruefer.Undefiniert:
            continue
    return True


k.praxis()

k.generator(injektiv_pfeile, typ="mehrfach", titel="Injektiv, surjektiv, bijektiv an Pfeildiagrammen")
k.generator(umkehrfunktion_bestimmen, typ="term", titel="Umkehrfunktion bestimmen", probe=_probe_umkehr)

k.rechenweg_aufgabe(r"""
    ## Surjektivität nachweisen

    Zeige, dass $f\colon \mathbb{R} \to \mathbb{R},\ x \mapsto 2x + 5$ surjektiv ist:
    Zu jedem $y \in \mathbb{R}$ brauchst du ein $x$ mit $f(x) = y$.
    """,
    [{"typ": "term", "frage": "Löse $y = 2x + 5$ nach $x$ auf. Gib $x$ als Term in $y$ an.", "loesung": "(y - 5)/2",
      "variablen": "y",
      "tipps": ["Erst $5$ abziehen.", "Dann durch $2$ teilen."],
      "rechenweg": ":::rechnung\ny = 2x + 5 || Ansatz\ny - 5 = 2x || $-5$\nx = \\frac{y - 5}{2} || durch $2$\n:::",
      "typische_fehler": [("y/2 - 5", "Erst $5$ abziehen, dann teilen: $\\frac{y - 5}{2}$.")]},
     {"typ": "zahl", "frage": "Probe für $y = 11$: Welches $x$ liefert dein Term, und ist $f(x) = 11$? Gib das $x$ an.",
      "loesung": 3,
      "tipps": ["Setze $y = 11$ in $\\frac{y - 5}{2}$ ein.", "$\\frac{6}{2}$"],
      "rechenweg": ":::rechnung\n\\frac{11 - 5}{2} = 3 || $x$ für $y = 11$\n2 \\cdot 3 + 5 = 11 || Probe stimmt\n:::",
      "typische_fehler": [(8, "Du hast $11 - 5 + 2$ gerechnet. Es wird durch $2$ geteilt.")]}],
    "Für jedes $y$ ist $x = \\frac{y - 5}{2}$ eine reelle Zahl mit $f(x) = y$. Also ist $f$ surjektiv.",
    tipps=["Surjektiv: Zu jedem $y$ ein passendes $x$ finden.", "Das $x$ bekommst du durch Auflösen von $y = f(x)$."],
    rechenweg=r"""
    :::rechnung
    y = 2x + 5 || zu beliebigem $y \in \mathbb{R}$
    x = \frac{y - 5}{2} || Kandidat für das Urbild
    :::

    Probe: $f\left(\frac{y - 5}{2}\right) = 2 \cdot \frac{y - 5}{2} + 5 = y$. Und $\frac{y - 5}{2} \in \mathbb{R} = D$.
    """)

k.papier(r"""
    ## Übungsblatt-Stil: Bijektivität und Umkehrfunktion

    Gegeben ist
    $$f\colon \mathbb{R} \setminus \{1\} \to \mathbb{R} \setminus \{2\},\quad x \mapsto \frac{2x + 1}{x - 1}.$$

    a) Zeigen Sie, dass $f$ injektiv ist.

    b) Zeigen Sie, dass $f$ surjektiv ist, und bestimmen Sie die Umkehrfunktion $f^{-1}$.

    c) Warum muss die $2$ aus der Zielmenge heraus?
    """,
    r"""
    **a) Injektiv.** Seien $x_1, x_2 \in \mathbb{R} \setminus \{1\}$ mit $f(x_1) = f(x_2)$.
    Mit den Nennern $x_1 - 1 \ne 0$ und $x_2 - 1 \ne 0$ malnehmen:

    :::rechnung
    (2x_1 + 1)(x_2 - 1) = (2x_2 + 1)(x_1 - 1) || über Kreuz malnehmen
    2x_1x_2 - 2x_1 + x_2 - 1 = 2x_1x_2 - 2x_2 + x_1 - 1 || ausmultiplizieren
    -3x_1 = -3x_2 || $2x_1x_2 - 1$ fällt weg, $x$-Terme sortieren
    x_1 = x_2 || durch $-3$ teilen
    :::

    **b) Surjektiv.** Sei $y \in \mathbb{R} \setminus \{2\}$. Löse $y = f(x)$:

    :::rechnung
    y = \frac{2x + 1}{x - 1} || Ansatz
    y(x - 1) = 2x + 1 || mal $(x - 1)$
    yx - 2x = y + 1 || $x$-Terme nach links
    x(y - 2) = y + 1 || $x$ ausklammern
    x = \frac{y + 1}{y - 2} || durch $y - 2 \ne 0$ teilen
    :::

    Dieses $x$ liegt in $D$: Wäre $\frac{y + 1}{y - 2} = 1$, dann $y + 1 = y - 2$, also
    $1 = -2$, Widerspruch. Damit ist $f$ bijektiv und
    $f^{-1}\colon \mathbb{R} \setminus \{2\} \to \mathbb{R} \setminus \{1\},\ y \mapsto \frac{y + 1}{y - 2}$.

    **c)** Für $y = 2$ führt die Rechnung auf $x \cdot 0 = 3$: Es gibt kein Urbild. Mit der
    $2$ in der Zielmenge wäre $f$ nicht surjektiv.
    """,
    ["Ich habe mit beliebigen $x_1, x_2$ und $f(x_1) = f(x_2)$ begonnen und bei $x_1 = x_2$ geendet",
     "Ich habe $y = f(x)$ korrekt nach $x = \\frac{y + 1}{y - 2}$ aufgelöst",
     "Ich habe geprüft, dass das gefundene $x$ nicht $1$ ist",
     "Ich habe begründet, warum $y = 2$ kein Urbild hat"],
    "Bijektiv nachweisen heißt: Injektivität per Umformung, Surjektivität durch Angabe eines Urbilds im Definitionsbereich.",
    uebungsblatt=True,
    tipps=["Für a) mit beiden Nennern malnehmen.", "Für b) $y(x - 1) = 2x + 1$ nach $x$ auflösen."])

k.zusammenfassung(r"""
    ## Injektiv, surjektiv, bijektiv

    | Eigenschaft | Definition | Urbilder je $y \in W$ | widerlegen durch |
    |---|---|---|---|
    | injektiv | $f(x_1) = f(x_2) \Rightarrow x_1 = x_2$ | höchstens eins | $x_1 \ne x_2$ mit $f(x_1) = f(x_2)$ |
    | surjektiv | $f(D) = W$ | mindestens eins | ein $y \in W$ ohne Urbild |
    | bijektiv | injektiv und surjektiv | genau eins | eins von beiden widerlegen |

    - Die Eigenschaften hängen an $D$ und $W$, nicht nur an der Vorschrift.
    - Injektiv beweisen: $f(x_1) = f(x_2)$ annehmen, bis $x_1 = x_2$ umformen.
    - Surjektiv beweisen: $y = f(x)$ nach $x$ auflösen, prüfen, dass $x \in D$.
    - Umkehrfunktion $f^{-1}\colon W \to D$ nur bei bijektivem $f$: $f^{-1}(f(x)) = x$, $f(f^{-1}(y)) = y$.

    !! $f^{-1}(y)$ ist nicht $\frac{1}{f(y)}$, und das Urbild $f^{-1}(B)$ gibt es immer.
""")
