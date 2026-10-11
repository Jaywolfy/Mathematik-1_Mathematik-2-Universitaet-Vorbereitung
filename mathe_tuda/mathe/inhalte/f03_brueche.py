# -*- coding: utf-8 -*-
"""Fundament 3: Brüche – kürzen, erweitern, addieren, multiplizieren, dividieren."""
import math
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

tex = mathlib.tex


def fr(z, n):
    """Ungekürzter Bruch als LaTeX (Zähler/Nenner so, wie sie dastehen)."""
    if n < 0:
        z, n = -z, -n
    return f"-\\frac{{{-z}}}{{{n}}}" if z < 0 else f"\\frac{{{z}}}{{{n}}}"


k = neues_kapitel(
    slug="brueche",
    titel="Brüche",
    beschreibung="Was ein Bruch ist, kürzen, erweitern, addieren, malnehmen und teilen",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="🥧")

k.lernziele([
    "Ich kann Brüche erweitern und vollständig kürzen",
    "Ich kann Brüche mit verschiedenen Nennern addieren und subtrahieren",
    "Ich kann Brüche malnehmen und durch einen Bruch teilen",
    "Ich erkenne den Fehler $\\frac{1}{2} + \\frac{1}{3} = \\frac{2}{5}$ und weiß, warum er falsch ist",
])

k.warum(r"""
Brüche sind überall, wo genau gerechnet werden muss. Kommazahlen im Computer
(`float`) runden, Brüche nicht: Python hat dafür sogar das Modul `fractions`, und
dieses Lernsystem prüft deine Antworten damit. Beim Kürzen steckt der [[ggT]]
dahinter, beim Hauptnenner das [[kgV]]. Den ggT triffst du in Mathe 1 wieder:
beim euklidischen Algorithmus, einem der ältesten Algorithmen überhaupt.
""")

# ── 1: Was ist ein Bruch ───────────────────────────────────────────────────
k.erklaerung("Was ist ein Bruch?", r"""
    ## Teile von einem Ganzen

    :::analogie 🍕 Pizza
    Eine Pizza wird in $4$ gleich große Stücke geschnitten. Du nimmst $3$ Stücke.
    Das sind $\frac{3}{4}$ der Pizza.
    :::

    Ein [[Bruch]] hat zwei Teile:

    - Der [[Nenner]] unten sagt, in wie viele Teile das Ganze geschnitten ist.
    - Der [[Zähler]] oben sagt, wie viele Teile du nimmst.

    :::visual bruch
    {"zaehler": 3, "nenner": 4, "modell": "kuchen", "interaktiv": true,
     "unterschrift": "Schiebe die Regler: Der Nenner schneidet, der Zähler färbt."}
    :::

    Ein Bruchstrich bedeutet „geteilt durch“.

    :::rechnung Beispiel vorgerechnet
    \frac{3}{4} = 3 : 4 || Bruchstrich heißt geteilt
    = 0{,}75 || als Kommazahl
    :::

    :::alt Mit Schokolade erklärt
    Eine Tafel Schokolade hat $8$ gleiche Stückchen. Du isst $3$ davon. Du hast
    $\frac{3}{8}$ der Tafel gegessen. Unten steht immer, wie viele Stückchen es
    insgesamt gibt. Oben steht, wie viele du davon hast.
    :::
    ---
    ## Erweitern: feiner schneiden

    Du kannst jedes Stück noch einmal durchschneiden. Dann hast du doppelt so viele
    Stücke, aber jedes ist halb so groß. Die Menge Pizza bleibt gleich.

    :::visual bruch
    {"zaehler": 3, "nenner": 4, "modell": "kuchen", "erweitern": 2,
     "unterschrift": "Klick auf „Mit 2 erweitern“: Aus $\\frac{3}{4}$ wird $\\frac{6}{8}$."}
    :::

    [[Erweitern]] heißt: Zähler und Nenner mit **derselben** Zahl malnehmen.

    :::rechnung Beispiel vorgerechnet
    \frac{3}{4} = \frac{3 \cdot 2}{4 \cdot 2} || oben und unten mal $2$
    = \frac{6}{8} || derselbe Wert, feiner geschnitten
    :::

    :::alt Mit Geld erklärt
    Ein halber Euro sind $50$ Cent, also $\frac{1}{2} = \frac{50}{100}$. Du hast
    nichts verändert, nur in kleineren Münzen gezählt. Genau das ist Erweitern:
    gleiche Menge, kleinere Einheiten.
    :::
    ---
    ## Kürzen: gröber schneiden

    [[Kürzen]] ist das Gegenteil: Zähler und Nenner durch **dieselbe** Zahl teilen.
    Kürze möglichst weit: am besten durch den größten gemeinsamen Teiler ([[ggT]]).

    :::visual bruch
    {"zaehler": 6, "nenner": 8, "modell": "balken", "kuerzen": true,
     "unterschrift": "Je zwei Achtel ergeben ein Viertel."}
    :::

    :::rechnung Beispiel vorgerechnet
    \frac{12}{18} = \frac{12 : 6}{18 : 6} || $6$ teilt $12$ und $18$
    = \frac{2}{3} || $2$ und $3$ haben keinen gemeinsamen Teiler außer $1$
    :::

    :::achtung Abziehen statt teilen
    $\frac{12}{18} \to \frac{12 - 6}{18 - 6} = \frac{6}{12}$ ist falsch. Beim Kürzen
    wird **geteilt**, nie abgezogen.
    :::

    :::alt Mit Gruppen erklärt
    Stell dir $12$ Äpfel von $18$ Äpfeln vor. Pack immer $6$ Äpfel in eine Tüte.
    Dann hast du $2$ Tüten von $3$ Tüten. Der Anteil ist gleich geblieben:
    $\frac{12}{18} = \frac{2}{3}$.
    :::
    """)

k.zahl("Wie viel ist $\\frac{3}{4}$ als Kommazahl?", F(3, 4),
       "Der Bruchstrich bedeutet geteilt: $3 : 4 = 0{,}75$.", form="dezimal",
       tipps=["Der Bruchstrich bedeutet „geteilt durch“.", "Rechne $3 : 4$.", "$3 : 4 = 0{,}75$"],
       rechenweg=r"""
       :::rechnung
       \frac{3}{4} = 3 : 4 || Bruchstrich heißt geteilt
       = 0{,}75 || ausrechnen
       :::
       """,
       typische_fehler=[(F(17, 5), "$3{,}4$ entsteht, wenn man Zähler und Nenner einfach nebeneinanderschreibt. Der Bruchstrich heißt aber „geteilt“."),
                        (F(4, 3), "Das ist $4 : 3$. Rechne Zähler geteilt durch Nenner: $3 : 4$.")])

k.luecke("Erweitere: Welche Zahl gehört in die Lücke?",
         "\\frac{2}{3} = \\frac{\\luecke}{12}", [[8]],
         "Der Nenner wurde mit $4$ malgenommen ($3 \\cdot 4 = 12$). Der Zähler muss auch mal $4$: $2 \\cdot 4 = 8$.",
         tipps=["Womit wurde der Nenner $3$ malgenommen, um $12$ zu erhalten?",
                "Mit $4$. Mach dasselbe mit dem Zähler.", "$2 \\cdot 4$"],
         rechenweg=r"""
         :::rechnung
         3 \cdot 4 = 12 || der Nenner wurde mit $4$ malgenommen
         2 \cdot 4 = 8 || also auch der Zähler
         \frac{2}{3} = \frac{8}{12} || erweitert mit $4$
         :::
         """,
         typische_fehler=[([2], "Du hast den Zähler nicht verändert. Oben und unten muss mit **derselben** Zahl malgenommen werden."),
                          ([11], "Du hast $9$ addiert. Beim Erweitern wird malgenommen, nicht addiert.")])

k.zahl("Kürze $\\frac{12}{18}$ vollständig.", F(12, 18),
       "Der ggT von $12$ und $18$ ist $6$: $\\frac{12 : 6}{18 : 6} = \\frac{2}{3}$.",
       gekuerzt=True, form="bruch",
       tipps=["Suche eine Zahl, die $12$ und $18$ teilt.", "Die größte solche Zahl ist $6$.",
              "$12 : 6 = 2$ und $18 : 6 = 3$."],
       rechenweg=r"""
       :::rechnung
       \frac{12}{18} = \frac{12 : 6}{18 : 6} || ggT von $12$ und $18$ ist $6$
       = \frac{2}{3} || fertig gekürzt
       :::
       """,
       typische_fehler=[(F(6, 12), "Beim Kürzen wird geteilt, nicht abgezogen. $\\frac{12 - 6}{18 - 6}$ ist ein anderer Bruch."),
                        (F(3, 2), "Das ist der Kehrwert. Der Zähler bleibt oben: $12 : 6 = 2$.")])

# ── 2: Addieren ────────────────────────────────────────────────────────────
k.erklaerung("Brüche addieren und subtrahieren", r"""
    ## Gleicher Nenner: einfach zählen

    Haben zwei Brüche denselben Nenner (sie sind [[gleichnamig]]), sind alle Stücke
    gleich groß. Dann zählst du nur die Stücke zusammen. Der Nenner bleibt.

    :::rechnung Beispiel vorgerechnet
    \frac{1}{5} + \frac{2}{5} = \frac{1 + 2}{5} || Zähler addieren, Nenner bleibt
    = \frac{3}{5} || ausrechnen
    :::

    :::visual bruch
    {"zaehler": 1, "nenner": 5, "modell": "balken", "plus": [[1, 5], [2, 5]],
     "unterschrift": "Fünftel plus Fünftel: Die Stücke sind schon gleich groß."}
    :::

    :::alt Mit Münzen erklärt
    $1$ Fünf-Cent-Münze plus $2$ Fünf-Cent-Münzen sind $3$ Fünf-Cent-Münzen. Die
    Sorte (der Nenner) ändert sich nicht. Du zählst nur, wie viele es sind.
    :::
    ---
    ## Verschiedene Nenner: erst gleich machen

    $\frac{1}{2}$ und $\frac{1}{3}$ sind verschieden große Stücke. Man kann sie nicht
    direkt zählen. Erst schneidest du beide in gleich große Stücke: in Sechstel.
    $6$ ist der kleinste gemeinsame Nenner, der [[Hauptnenner]].

    :::visual bruch
    {"zaehler": 1, "nenner": 2, "modell": "balken", "plus": [[1, 2], [1, 3]]}
    :::

    :::rechnung Beispiel vorgerechnet
    \frac{1}{2} + \frac{1}{3} || verschiedene Nenner
    = \frac{1 \cdot 3}{2 \cdot 3} + \frac{1 \cdot 2}{3 \cdot 2} || beide auf $6$ erweitern
    = \frac{\hl{3}}{6} + \frac{\hl{2}}{6} || jetzt gleichnamig
    = \frac{5}{6} || Zähler addieren
    !\frac{1}{2} + \frac{1}{3} = \frac{2}{5} || Zähler und Nenner einzeln addiert
    :::

    :::achtung Der häufigste Bruchfehler
    $\frac{1}{2} + \frac{1}{3} = \frac{2}{5}$ ist falsch. Prüfe: $\frac{2}{5}$ ist
    **kleiner** als $\frac{1}{2}$. Wenn du zur Hälfte etwas dazugibst, kann es nicht
    weniger werden. Nenner werden nie addiert.
    :::

    :::alt Mit Uhrzeiten erklärt
    Eine halbe Stunde plus eine Drittelstunde: Rechne in Minuten. $\frac{1}{2}$
    Stunde sind $30$ Minuten, $\frac{1}{3}$ Stunde sind $20$ Minuten. Zusammen
    $50$ Minuten, also $\frac{50}{60} = \frac{5}{6}$ Stunde. Die Minuten sind die
    gleich großen Stücke, die man zum Zählen braucht.
    :::
    """)

k.berechne("1/5 + 2/5", gekuerzt=True,
           erklaerung="Gleiche Nenner: Zähler addieren, Nenner bleibt. $\\frac{3}{5}$.",
           tipps=["Die Nenner sind gleich.", "Addiere nur die Zähler.", "$1 + 2 = 3$, der Nenner bleibt $5$."],
           rechenweg=r"""
           :::rechnung
           \frac{1}{5} + \frac{2}{5} = \frac{1 + 2}{5} || Zähler addieren
           = \frac{3}{5} || Nenner bleibt
           :::
           """,
           typische_fehler=[(F(3, 10), "Der Nenner wird nicht addiert. Fünftel plus Fünftel bleiben Fünftel.")])

k.berechne("1/2 + 1/3", gekuerzt=True,
           erklaerung="Hauptnenner $6$: $\\frac{3}{6} + \\frac{2}{6} = \\frac{5}{6}$.",
           tipps=["Die Nenner sind verschieden. Finde einen gemeinsamen Nenner.",
                  "Der kleinste gemeinsame Nenner von $2$ und $3$ ist $6$.",
                  "$\\frac{1}{2} = \\frac{3}{6}$ und $\\frac{1}{3} = \\frac{2}{6}$."],
           rechenweg=r"""
           :::rechnung
           \frac{1}{2} + \frac{1}{3} = \frac{3}{6} + \frac{2}{6} || auf den Hauptnenner $6$ erweitern
           = \frac{5}{6} || Zähler addieren
           :::
           """,
           typische_fehler=[(F(2, 5), "Du hast Zähler plus Zähler und Nenner plus Nenner gerechnet. Das geht nicht: Erst gleichnamig machen."),
                            (F(2, 6), "Du hast die Nenner gleich gemacht, aber die Zähler nicht mit erweitert: $\\frac{1}{2} = \\frac{3}{6}$.")])

k.berechne("3/4 - 1/6", gekuerzt=True,
           erklaerung="Hauptnenner $12$: $\\frac{9}{12} - \\frac{2}{12} = \\frac{7}{12}$.",
           tipps=["Finde den kleinsten gemeinsamen Nenner von $4$ und $6$.",
                  "Es ist $12$. Erweitere beide Brüche auf Zwölftel.",
                  "$\\frac{3}{4} = \\frac{9}{12}$ und $\\frac{1}{6} = \\frac{2}{12}$."],
           rechenweg=r"""
           :::rechnung
           \frac{3}{4} - \frac{1}{6} = \frac{9}{12} - \frac{2}{12} || Hauptnenner $12$: mit $3$ bzw. $2$ erweitern
           = \frac{7}{12} || Zähler subtrahieren
           :::
           """,
           typische_fehler=[(-1, "Du hast Zähler minus Zähler und Nenner minus Nenner gerechnet: $\\frac{3 - 1}{4 - 6}$. Erst gleichnamig machen."),
                            (F(2, 24), "Den Nenner $24$ darfst du nehmen, aber dann müssen auch die Zähler erweitert werden: $\\frac{18}{24} - \\frac{4}{24}$.")])

# ── 3: Malnehmen und Teilen ────────────────────────────────────────────────
k.erklaerung("Brüche malnehmen und teilen", r"""
    ## Malnehmen: oben mal oben, unten mal unten

    :::analogie 🍕 Die Hälfte von einem Viertel
    Von einem Viertel Pizza isst du die Hälfte. Das ist ein Achtel der ganzen Pizza:
    $\frac{1}{2} \cdot \frac{1}{4} = \frac{1}{8}$. „Von“ bedeutet hier „mal“.
    :::

    Beim Malnehmen braucht man **keinen** gemeinsamen Nenner.

    :::rechnung Beispiel vorgerechnet
    \frac{2}{3} \cdot \frac{3}{4} = \frac{2 \cdot 3}{3 \cdot 4} || Zähler mal Zähler, Nenner mal Nenner
    = \frac{6}{12} || ausrechnen
    = \frac{1}{2} || kürzen mit $6$
    :::

    :::alt Mit einer Fläche erklärt
    Zeichne ein Quadrat. Färbe $\frac{2}{3}$ der Breite und $\frac{3}{4}$ der Höhe.
    Die doppelt gefärbte Ecke besteht aus $2 \cdot 3 = 6$ von insgesamt
    $3 \cdot 4 = 12$ kleinen Kästchen. Also $\frac{6}{12}$.
    :::
    ---
    ## Teilen: mit dem Kehrwert malnehmen

    Den [[Kehrwert]] eines Bruchs bekommst du, wenn du Zähler und Nenner tauschst:
    Der Kehrwert von $\frac{1}{4}$ ist $\frac{4}{1} = 4$.

    !! Durch einen Bruch teilen heißt: mit seinem Kehrwert malnehmen.

    :::rechnung Beispiel vorgerechnet
    3 : \frac{1}{4} = 3 \cdot \frac{4}{1} || mit dem Kehrwert malnehmen
    = 12 || in $3$ Pizzen stecken $12$ Viertel
    \frac{3}{4} : \frac{1}{2} = \frac{3}{4} \cdot \frac{2}{1} || Kehrwert des **zweiten** Bruchs
    = \frac{6}{4} = \frac{3}{2} || ausrechnen und kürzen
    :::

    :::achtung Den falschen Bruch umdrehen
    Nur der Bruch **hinter** dem Geteilt-Zeichen wird umgedreht. Der erste Bruch
    bleibt, wie er ist.
    :::

    :::alt Mit Messbechern erklärt
    Teilen fragt: Wie oft passt das eine ins andere? Du hast $\frac{3}{4}$ Liter
    Saft und füllst Becher mit je $\frac{1}{2}$ Liter. Ein Becher wird voll, dann
    bleibt $\frac{1}{4}$ Liter übrig, das ist ein halber Becher. Zusammen also
    eineinhalb Becher, also $\frac{3}{2}$. Genau das liefert $\frac{3}{4} \cdot \frac{2}{1}$.
    :::
    """)

k.berechne("(2/3) * (3/4)", gekuerzt=True,
           erklaerung="$\\frac{2 \\cdot 3}{3 \\cdot 4} = \\frac{6}{12} = \\frac{1}{2}$.",
           tipps=["Beim Malnehmen braucht man keinen gemeinsamen Nenner.", "Zähler mal Zähler, Nenner mal Nenner.",
                  "$\\frac{6}{12}$. Jetzt noch kürzen."],
           rechenweg=r"""
           :::rechnung
           \frac{2}{3} \cdot \frac{3}{4} = \frac{2 \cdot 3}{3 \cdot 4} || oben mal oben, unten mal unten
           = \frac{6}{12} || ausrechnen
           = \frac{1}{2} || kürzen mit $6$
           :::
           """,
           typische_fehler=[(F(17, 12), "Das ist $\\frac{2}{3} + \\frac{3}{4}$. Gefragt ist **mal**."),
                            (F(8, 9), "Du hast jeden Zähler mit dem **anderen** Nenner malgenommen (über Kreuz). Das gehört zum **Teilen**.")])

k.wf("Beim Malnehmen von zwei Brüchen muss man sie zuerst auf einen gemeinsamen Nenner bringen.", False,
     "Nein. Beim Malnehmen rechnest du einfach Zähler mal Zähler und Nenner mal Nenner. Den gemeinsamen Nenner braucht man nur beim Addieren und Subtrahieren.",
     tipps=["Denk an $\\frac{1}{2} \\cdot \\frac{1}{4} = \\frac{1}{8}$: Gab es da einen gemeinsamen Nenner?"])

k.zahl("Berechne $\\frac{3}{4} : \\frac{1}{2}$.", F(3, 4) / F(1, 2),
       "Teilen durch $\\frac{1}{2}$ heißt mal $\\frac{2}{1}$: $\\frac{3}{4} \\cdot 2 = \\frac{6}{4} = \\frac{3}{2}$.",
       gekuerzt=True,
       tipps=["Durch einen Bruch teilen heißt mit dem Kehrwert malnehmen.",
              "Der Kehrwert von $\\frac{1}{2}$ ist $\\frac{2}{1}$.", "$\\frac{3}{4} \\cdot \\frac{2}{1}$, dann kürzen."],
       rechenweg=r"""
       :::rechnung
       \frac{3}{4} : \frac{1}{2} = \frac{3}{4} \cdot \frac{2}{1} || Kehrwert des zweiten Bruchs
       = \frac{6}{4} || malnehmen
       = \frac{3}{2} || kürzen mit $2$
       :::
       """,
       typische_fehler=[(F(3, 8), "Du hast malgenommen statt geteilt. Teilen heißt: mit dem **Kehrwert** malnehmen."),
                        (F(2, 3), "Du hast den ersten Bruch umgedreht. Nur der Bruch **hinter** dem Geteilt-Zeichen wird umgedreht.")])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


def _bruch(rng, max_nenner=12):
    """Echter, schon gekürzter Bruch z/n."""
    while True:
        n = rng.randint(2, max_nenner)
        z = rng.randint(1, n - 1)
        if math.gcd(z, n) == 1:
            return z, n


def brueche_addieren(rng):
    while True:
        (a, b), (c, d) = _bruch(rng), _bruch(rng)
        if b != d and F(a, b) != F(c, d) and mathlib.kgv(b, d) <= 36:
            break
    op = rng.choice(["+", "-"])
    if op == "-" and F(a, b) < F(c, d):          # keine negativen Ergebnisse (kommen erst später)
        (a, b), (c, d) = (c, d), (a, b)
    hn = mathlib.kgv(b, d)
    ea, ec = hn // b, hn // d
    w = F(a, b) + F(c, d) if op == "+" else F(a, b) - F(c, d)
    z = a * ea + c * ec if op == "+" else a * ea - c * ec
    if ea > 1 and ec > 1:
        wie = f"Hauptnenner ${hn}$: den ersten Bruch mit ${ea}$, den zweiten mit ${ec}$ erweitern"
    elif ea > 1:
        wie = f"Hauptnenner ${hn}$: den ersten Bruch mit ${ea}$ erweitern, der zweite hat schon den Nenner ${hn}$"
    else:
        wie = f"Hauptnenner ${hn}$: den zweiten Bruch mit ${ec}$ erweitern, der erste hat schon den Nenner ${hn}$"
    zeilen = [(f"{fr(a, b)} {op} {fr(c, d)} = {fr(a * ea, hn)} {op} {fr(c * ec, hn)}", wie),
              (f"= {fr(z, hn)}", "Zähler " + ("addieren" if op == "+" else "subtrahieren"))]
    if math.gcd(abs(z), hn) > 1:
        zeilen.append((f"= {tex(w)}", f"kürzen mit ${math.gcd(abs(z), hn)}$"))
    fehler = [(F(a + c, b + d) if op == "+" else F(a - c, b - d) if b != d else None,
               "Zähler und Nenner einzeln " + ("addiert" if op == "+" else "subtrahiert") + ". Erst gleichnamig machen!"),
              (F(a + c if op == "+" else a - c, hn), "Du hast die Nenner gleichnamig gemacht, aber die Zähler nicht mit erweitert.")]
    fehler = [(f, m) for f, m in fehler if f is not None]
    return {
        "frage": f"Berechne und kürze vollständig: ${fr(a, b)} {op} {fr(c, d)}$.",
        "loesung": w, "gekuerzt": True,
        "tipps": ["Die Nenner sind verschieden. Finde den Hauptnenner.",
                  f"Der Hauptnenner von ${b}$ und ${d}$ ist ${hn}$.",
                  " und ".join(f"${fr(x, y)} = {fr(x * e, hn)}$" for x, y, e in ((a, b, ea), (c, d, ec)) if e > 1) + "."],
        "rechenweg": _zeilen(*zeilen),
        "erklaerung": "Erst gleichnamig machen (Hauptnenner), dann Zähler verrechnen, zum Schluss kürzen.",
        "typische_fehler": ohne_gleiche(w, fehler),
    }


k.praxis()

k.generator(brueche_addieren, typ="zahl", titel="Brüche addieren und subtrahieren", glatt=True)


def brueche_mal_geteilt(rng):
    (a, b), (c, d) = _bruch(rng, 9), _bruch(rng, 9)
    op = rng.choice(["mal", "geteilt"])
    if op == "mal":
        w = F(a, b) * F(c, d)
        zeilen = [(f"{fr(a, b)} \\cdot {fr(c, d)} = \\frac{{{a} \\cdot {c}}}{{{b} \\cdot {d}}}", "Zähler mal Zähler, Nenner mal Nenner"),
                  (f"= {fr(a * c, b * d)}", "ausrechnen")]
        fehler = [(F(a * d, b * c), "Du hast jeden Zähler mit dem **anderen** Nenner malgenommen (über Kreuz). Das gehört zum **Teilen**."),
                  (F(a, b) + F(c, d), "Du hast addiert statt malgenommen.")]
        zeichen = "\\cdot"
    else:
        w = F(a, b) / F(c, d)
        zeilen = [(f"{fr(a, b)} : {fr(c, d)} = {fr(a, b)} \\cdot {fr(d, c)}", "mit dem Kehrwert malnehmen"),
                  (f"= {fr(a * d, b * c)}", "ausrechnen")]
        fehler = [(F(a * c, b * d), "Du hast malgenommen statt geteilt. Teilen heißt: mit dem **Kehrwert** malnehmen."),
                  (F(b * c, a * d), "Du hast den falschen Bruch umgedreht. Nur der Bruch hinter dem Geteilt-Zeichen wird umgedreht.")]
        zeichen = ":"
    letzter = fr(a * c, b * d) if op == "mal" else fr(a * d, b * c)
    if letzter != tex(w):
        zeilen.append((f"= {tex(w)}", "vollständig kürzen"))
    return {
        "frage": f"Berechne und kürze vollständig: ${fr(a, b)} {zeichen} {fr(c, d)}$.",
        "loesung": w, "gekuerzt": True,
        "tipps": ["Malnehmen: oben mal oben, unten mal unten." if op == "mal" else "Teilen: mit dem Kehrwert des zweiten Bruchs malnehmen.",
                  "Du brauchst keinen gemeinsamen Nenner.", "Am Ende vollständig kürzen."],
        "rechenweg": _zeilen(*zeilen),
        "erklaerung": "Malnehmen: Zähler mal Zähler, Nenner mal Nenner. Teilen: mit dem Kehrwert malnehmen.",
        "typische_fehler": ohne_gleiche(w, fehler),
    }


k.generator(brueche_mal_geteilt, typ="zahl", titel="Brüche malnehmen und teilen", glatt=True)


def kuerzen(rng):
    while True:
        p, q = rng.randint(1, 9), rng.randint(2, 12)
        if math.gcd(p, q) == 1 and p != q:
            break
    g = rng.choice([2, 3, 4, 5, 6, 8, 9, 12])
    z, n = p * g, q * g
    fehler = [(F(q, p), "Das ist der Kehrwert. Der Zähler bleibt oben.")]
    return {
        "frage": f"Kürze ${fr(z, n)}$ vollständig.",
        "loesung": F(p, q), "gekuerzt": True, "form": "bruch",
        "tipps": [f"Suche eine Zahl, die ${z}$ und ${n}$ beide teilt.", f"Der größte gemeinsame Teiler ist ${g}$.",
                  f"${z} : {g} = {p}$ und ${n} : {g} = {q}$."],
        "rechenweg": _zeilen((f"{fr(z, n)} = \\frac{{{z} : {g}}}{{{n} : {g}}}", f"ggT von ${z}$ und ${n}$ ist ${g}$"),
                             (f"= {fr(p, q)}", "vollständig gekürzt")),
        "erklaerung": "Zähler und Nenner durch den ggT teilen.",
        "typische_fehler": ohne_gleiche(F(p, q), fehler),
    }


k.generator(kuerzen, typ="zahl", titel="Brüche kürzen", glatt=True)

# Übungsblatt-Stil: Punkt vor Strich mit Brüchen, in Teilschritten
_prod = F(1, 4) * F(8, 9)
_erg = F(2, 3) + _prod
k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: Brüche mit Punkt vor Strich

    Berechne und kürze vollständig:
    $$\frac{2}{3} + \frac{1}{4} \cdot \frac{8}{9}$$
    """,
    [{"typ": "zahl", "frage": "Welche Rechnung kommt zuerst? Berechne $\\frac{1}{4} \\cdot \\frac{8}{9}$ (gekürzt).",
      "loesung": _prod, "gekuerzt": True,
      "tipps": ["Punkt vor Strich: zuerst das Produkt.", "$\\frac{1 \\cdot 8}{4 \\cdot 9} = \\frac{8}{36}$, jetzt kürzen."],
      "rechenweg": "$\\frac{1}{4} \\cdot \\frac{8}{9} = \\frac{8}{36} = \\frac{2}{9}$",
      "typische_fehler": [(F(11, 12), "Punkt vor Strich: zuerst nur $\\frac{1}{4} \\cdot \\frac{8}{9}$ ausrechnen.")]},
     {"typ": "zahl", "frage": "Welcher Hauptnenner passt für $\\frac{2}{3} + \\frac{2}{9}$?", "loesung": 9,
      "tipps": ["Die $9$ ist durch $3$ teilbar.", "Der kleinste gemeinsame Nenner ist die $9$ selbst."],
      "rechenweg": "$9$ ist ein Vielfaches von $3$: Der Hauptnenner ist $9$.",
      "typische_fehler": [(27, "$27$ geht auch, ist aber nicht der kleinste. $9$ ist schon durch $3$ teilbar.")]},
     {"typ": "zahl", "frage": "Berechne $\\frac{2}{3} + \\frac{2}{9}$ (gekürzt).", "loesung": _erg, "gekuerzt": True,
      "tipps": ["$\\frac{2}{3} = \\frac{6}{9}$", "$\\frac{6}{9} + \\frac{2}{9}$"],
      "rechenweg": "$\\frac{2}{3} + \\frac{2}{9} = \\frac{6}{9} + \\frac{2}{9} = \\frac{8}{9}$",
      "typische_fehler": [(F(4, 12), "Zähler und Nenner einzeln addiert. Erst gleichnamig machen.")]}],
    "Punkt vor Strich gilt auch bei Brüchen: erst das Produkt, dann die Summe mit Hauptnenner.",
    uebungsblatt=True,
    tipps=["Punkt vor Strich!", "Nach dem Produkt bleibt eine Summe mit verschiedenen Nennern."],
    rechenweg=r"""
    :::rechnung
    \frac{2}{3} + \hl{\frac{1}{4} \cdot \frac{8}{9}} || Punkt vor Strich
    = \frac{2}{3} + \frac{8}{36} || Zähler mal Zähler, Nenner mal Nenner
    = \frac{2}{3} + \frac{2}{9} || kürzen mit $4$
    = \frac{6}{9} + \frac{2}{9} || Hauptnenner $9$
    = \frac{8}{9} || Zähler addieren
    :::
    """)

k.papier(r"""
    ## Erklären wie in der Übung

    Ein Mitschüler behauptet: $\frac{1}{2} + \frac{1}{3} = \frac{2}{5}$.

    Schreibe auf Papier eine kurze Begründung, warum das **nicht** stimmen kann.
    Gib zwei verschiedene Argumente an und rechne das richtige Ergebnis vor.
    """,
    r"""
    **Argument 1 (Größenvergleich):** $\frac{2}{5} = 0{,}4$ ist kleiner als
    $\frac{1}{2} = 0{,}5$. Wenn man zu $\frac{1}{2}$ eine positive Zahl addiert,
    muss das Ergebnis größer als $\frac{1}{2}$ werden. Also kann $\frac{2}{5}$
    nicht stimmen.

    **Argument 2 (Bedeutung des Nenners):** Der Nenner gibt die Größe der Stücke an.
    Halbe und Drittel sind verschieden große Stücke, man kann sie nicht einfach
    zählen. Erst muss man beide in gleich große Stücke (Sechstel) schneiden.

    **Richtige Rechnung:**
    $$\frac{1}{2} + \frac{1}{3} = \frac{3}{6} + \frac{2}{6} = \frac{5}{6}$$
    """,
    ["Ich habe ein Argument über die Größe ($\\frac{2}{5} < \\frac{1}{2}$) angegeben",
     "Ich habe erklärt, dass Nenner die Stückgröße angeben und nicht addiert werden",
     "Ich habe auf den Hauptnenner $6$ erweitert",
     "Mein Ergebnis ist $\\frac{5}{6}$"],
    "Gute Begründungen nennen ein Gegenargument und rechnen das richtige Ergebnis vor.",
    tipps=["Vergleiche $\\frac{2}{5}$ mit $\\frac{1}{2}$: Was ist größer?"])

k.zusammenfassung(r"""
    ## Bruchrechnen

    | Was | Regel | Beispiel |
    |---|---|---|
    | Erweitern | oben und unten mal dieselbe Zahl | $\frac{3}{4} = \frac{6}{8}$ |
    | Kürzen | oben und unten durch dieselbe Zahl (ggT) | $\frac{12}{18} = \frac{2}{3}$ |
    | Addieren | erst Hauptnenner, dann Zähler addieren | $\frac{1}{2} + \frac{1}{3} = \frac{3}{6} + \frac{2}{6} = \frac{5}{6}$ |
    | Malnehmen | oben mal oben, unten mal unten | $\frac{2}{3} \cdot \frac{3}{4} = \frac{6}{12} = \frac{1}{2}$ |
    | Teilen | mit dem Kehrwert malnehmen | $\frac{3}{4} : \frac{1}{2} = \frac{3}{4} \cdot \frac{2}{1} = \frac{3}{2}$ |

    !! Nenner werden nie addiert: $\frac{1}{2} + \frac{1}{3} \neq \frac{2}{5}$.

    - Bruchstrich heißt geteilt: $\frac{3}{4} = 3 : 4 = 0{,}75$.
    - Ergebnis immer vollständig kürzen.
""")
