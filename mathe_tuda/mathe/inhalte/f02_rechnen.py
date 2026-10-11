# -*- coding: utf-8 -*-
"""Fundament 2: Rechnen mit negativen Zahlen, Punkt vor Strich, Klammern."""
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

tk = mathlib.tex_klammer      # negative Zahlen in Klammern: (-3)

k = neues_kapitel(
    slug="rechnen",
    titel="Plus, Minus, Klammern: Rechnen mit Vorzeichen",
    beschreibung="Negative Zahlen addieren und malnehmen, Punkt vor Strich, Klammern und die Minusklammer",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="➕")

k.lernziele([
    "Ich kann negative Zahlen addieren und subtrahieren",
    "Ich kann mit den Vorzeichenregeln malnehmen und teilen",
    "Ich halte die Reihenfolge ein: Klammern, dann Punkt vor Strich, dann von links nach rechts",
    "Ich kann eine Minusklammer richtig auflösen",
])

k.warum(r"""
Jede Programmiersprache rechnet nach genau diesen Regeln. `2 + 3 * 4` ergibt in
Python $14$, nicht $20$. Ein [[Term]] wird vom Computer in Teile zerlegt, und zwar in
der Reihenfolge „Klammern, Punkt vor Strich, von links nach rechts“. Sogar das
Programm, das deine Antworten hier prüft, arbeitet so. Wer die Regeln kennt,
schreibt Formeln im Code richtig und findet Fehler schneller.
""")

# ── 1: Addieren und Subtrahieren ───────────────────────────────────────────
k.erklaerung("Plus und Minus mit negativen Zahlen", r"""
    ## Rechnen heißt gehen

    :::analogie 🚶 Auf der Zahlengeraden gehen
    Plus heißt: nach rechts gehen. Minus heißt: nach links gehen. Du startest bei
    der ersten Zahl.
    :::

    Bei $3 - 5$ startest du bei $3$ und gehst $5$ Schritte nach links. Du landest
    bei $-2$, also unter null.

    :::visual zahlenstrahl
    {"von": -4, "bis": 5, "punkte": [{"x": 3}, {"x": -2, "farbe": "orange"}],
     "pfeile": [{"von": 3, "bis": -2, "label": "-5"}],
     "unterschrift": "$3 - 5$: Start bei $3$, fünf Schritte nach links, Ziel $-2$."}
    :::

    :::rechnung Beispiel vorgerechnet
    3 - 5 = -2 || $3$ Schritte bis zur $0$, dann noch $2$ weiter nach links
    -4 + 6 = 2 || von $-4$ aus $6$ Schritte nach rechts
    -2 - 3 = -5 || von $-2$ aus $3$ Schritte weiter nach links
    :::

    :::alt Mit dem Kontostand erklärt
    Denk an dein Konto. Du hast $3$ Euro und bezahlst $5$ Euro. Danach stehst du
    bei $-2$ Euro, du schuldest der Bank also $2$ Euro. Bekommst du jetzt $6$ Euro,
    stehst du bei $4$ Euro. Plus ist Geld bekommen, Minus ist Geld ausgeben.
    :::
    ---
    ## Minus eine negative Zahl

    Was bedeutet $4 - (-3)$? Man zieht eine negative Zahl ab.

    :::analogie 🧾 Schulden streichen
    Jemand streicht dir $3$ Euro Schulden. Du hast danach $3$ Euro **mehr**.
    Schulden wegnehmen ist dasselbe wie Geld dazugeben.
    :::

    !! Minus minus wird plus: $a - (-b) = a + b$.

    :::rechnung Beispiel vorgerechnet
    4 - (-3) || eine negative Zahl wird abgezogen
    = 4 + 3 || zwei Minus hintereinander werden zu Plus
    = 7 || ausrechnen
    :::

    :::achtung Ein Minus übersehen
    $4 - (-3) = 1$ ist falsch. Hier wurde nur „$4 - 3$“ gerechnet. Die Klammer mit
    dem zweiten Minus darfst du nicht ignorieren.
    :::

    :::alt Mit Umdrehen erklärt
    Stell dich auf die Zahlengerade, Blick nach rechts. Ein Minus heißt: Dreh dich
    um. Bei $4 - (-3)$ kommen zwei Minus: Du drehst dich zweimal um und schaust
    wieder nach rechts. Dann gehst du $3$ Schritte und landest bei $7$.
    :::
    """)

k.berechne("-3 + 8",
           erklaerung="Von $-3$ aus $8$ Schritte nach rechts: $3$ Schritte bis zur $0$, dann noch $5$. Ergebnis $5$.",
           tipps=["Starte bei $-3$ und gehe nach rechts.", "Bis zur $0$ sind es $3$ Schritte. Wie viele bleiben übrig?",
                  "$8 - 3 = 5$ Schritte bleiben nach der $0$."],
           rechenweg=r"""
           :::rechnung
           -3 + 3 = 0 || erst $3$ Schritte bis zur $0$
           0 + 5 = 5 || dann die übrigen $5$ Schritte
           -3 + 8 = 5 || zusammen
           :::
           """,
           typische_fehler=[(-11, "Du hast $-3 - 8$ gerechnet. Bei $+8$ geht es nach **rechts**."),
                            (-5, "Das Vorzeichen stimmt nicht: Von $-3$ aus $8$ Schritte nach rechts landest du rechts von der $0$.")])

k.berechne("2 - 7",
           erklaerung="Von $2$ aus $7$ Schritte nach links: $2$ bis zur $0$, dann noch $5$. Ergebnis $-5$.",
           tipps=["Starte bei $2$ und gehe nach links.", "Nach $2$ Schritten bist du bei $0$. Wie viele fehlen noch?",
                  "Noch $5$ Schritte nach links: $-5$."],
           rechenweg=r"""
           :::rechnung
           2 - 2 = 0 || erst bis zur $0$
           0 - 5 = -5 || dann noch $5$ Schritte weiter nach links
           2 - 7 = -5 || zusammen
           :::
           """,
           typische_fehler=[(5, "Der Betrag stimmt, aber du landest **unter** null: Du gehst weiter nach links als bis zur $0$."),
                            (9, "Du hast $2 + 7$ gerechnet. Minus heißt nach links gehen.")])

k.berechne("4 - (-3)",
           erklaerung="Minus minus wird plus: $4 - (-3) = 4 + 3 = 7$.",
           tipps=["Achte auf die zwei Minuszeichen hintereinander.", "Was wird aus $-(-3)$?",
                  "$-(-3) = +3$. Rechne also $4 + 3$."],
           rechenweg=r"""
           :::rechnung
           4 - (-3) = 4 + 3 || Minus minus wird plus
           = 7 || ausrechnen
           :::
           """,
           typische_fehler=[(1, "Du hast $4 - 3$ gerechnet und das Minus in der Klammer übersehen. Minus minus wird plus.")])

k.wf("$-(-5) = -5$", False,
     "Zwei Minus heben sich auf: $-(-5) = 5$. Die Gegenzahl der Gegenzahl ist die Zahl selbst.",
     tipps=["Die Gegenzahl von $-5$ ist …?"])

# ── 2: Malnehmen und Teilen ────────────────────────────────────────────────
k.erklaerung("Mal und geteilt: die Vorzeichenregeln", r"""
    ## Gleiche Vorzeichen: plus. Verschiedene: minus.

    | Rechnung | Ergebnis | Beispiel |
    |---|---|---|
    | plus mal plus | plus | $3 \cdot 4 = 12$ |
    | minus mal plus | minus | $(-3) \cdot 4 = -12$ |
    | plus mal minus | minus | $3 \cdot (-4) = -12$ |
    | minus mal minus | plus | $(-3) \cdot (-4) = 12$ |

    Beim Teilen gilt dieselbe Regel. Rechne erst ohne Vorzeichen, dann bestimme das
    Vorzeichen.

    :::rechnung Beispiel vorgerechnet
    (-12) : 4 = -3 || verschiedene Vorzeichen: minus
    (-12) : (-4) = 3 || gleiche Vorzeichen: plus
    (-2) \cdot (-3) \cdot (-1) = -6 || drei Minus: ungerade Anzahl, also minus
    :::

    :::info Durch null teilen geht nicht
    $0 : 5 = 0$ ist erlaubt. Aber $5 : 0$ hat **kein** Ergebnis: Es gibt keine Zahl,
    die mal $0$ wieder $5$ ergibt. Man sagt: $5 : 0$ ist nicht definiert.
    :::

    :::alt Mit einem Muster erklärt
    Schau dir diese Reihe an. Die linke Zahl wird immer um $1$ kleiner:
    $3 \cdot (-2) = -6$, $2 \cdot (-2) = -4$, $1 \cdot (-2) = -2$, $0 \cdot (-2) = 0$.
    Das Ergebnis wächst jedes Mal um $2$. Rechne weiter: $(-1) \cdot (-2)$ muss also
    $+2$ sein. So kommt „minus mal minus gibt plus“ zustande.
    :::
    """)

k.berechne("(-6)*(-7)",
           erklaerung="Gleiche Vorzeichen ergeben plus: $(-6) \\cdot (-7) = 42$.",
           tipps=["Rechne zuerst ohne Vorzeichen.", "$6 \\cdot 7 = 42$. Jetzt das Vorzeichen: zwei Minus.",
                  "Minus mal minus gibt plus."],
           rechenweg=r"""
           :::rechnung
           6 \cdot 7 = 42 || erst ohne Vorzeichen
           (-6) \cdot (-7) = 42 || zwei gleiche Vorzeichen: plus
           :::
           """,
           typische_fehler=[(-42, "Minus mal minus ergibt **plus**. Zwei gleiche Vorzeichen heben sich auf."),
                            (-13, "Du hast addiert statt malgenommen: $(-6) + (-7) = -13$.")])

k.mc("Welches Vorzeichen hat $(-2) \\cdot (-3) \\cdot (-1)$?",
     ["negativ", "positiv", "Das kann man nicht sagen"],
     "Drei Minuszeichen: Zwei davon ergeben plus, das dritte macht wieder minus. Ergebnis $-6$.",
     tipps=["Zähle die Minuszeichen.", "Je zwei Minus ergeben plus. Bleibt eins übrig?"],
     fehler={"positiv": "Zähle die Minuszeichen: Es sind drei. Zwei ergeben plus, das dritte macht wieder minus."})

k.wf("$7 : 0 = 0$", False,
     "Durch $0$ kann man nicht teilen. Es gibt keine Zahl, die mal $0$ wieder $7$ ergibt. Umgekehrt ist $0 : 7 = 0$ richtig.",
     tipps=["Welche Zahl mal $0$ ergibt $7$?"])

# ── 3: Reihenfolge ─────────────────────────────────────────────────────────
k.erklaerung("Punkt vor Strich", r"""
    ## Erst malnehmen, dann addieren

    **Punktrechnung** ($\cdot$ und $:$) kommt vor **Strichrechnung** ($+$ und $-$).

    :::analogie 📦 Pakete packen
    Ein Mal-Ausdruck wie $3 \cdot 4$ ist ein Paket, das zuerst zugeschnürt wird. Erst
    wenn alle Pakete fertig sind, wird zusammengezählt.
    :::

    :::rechnung Beispiel vorgerechnet
    2 + \hl{3 \cdot 4} || das Mal-Paket zuerst
    = 2 + 12 || $3 \cdot 4 = 12$
    = 14 || jetzt addieren
    :::

    :::achtung Stur von links nach rechts
    $2 + 3 \cdot 4 = 5 \cdot 4 = 20$ ist falsch. Hier wurde zuerst addiert.
    :::

    :::alt Mit Einkaufen erklärt
    Du kaufst $1$ Brot für $2$ Euro und $3$ Äpfel zu je $4$ Euro. Was kostet alles?
    Die Äpfel kosten $3 \cdot 4 = 12$ Euro, dazu das Brot: $2 + 12 = 14$ Euro. Niemand
    würde rechnen: Brot plus $3$ Äpfel, das Ganze mal $4$.
    :::
    ---
    ## Klammern zuerst

    Was in einer Klammer steht, wird **vor allem anderen** ausgerechnet.

    :::rechnung Beispiel vorgerechnet
    18 - 2 \cdot \hl{(3 + 4)} || Klammer zuerst
    = 18 - \hl{2 \cdot 7} || dann Punkt vor Strich
    = 18 - 14 || $2 \cdot 7 = 14$
    = 4 || zum Schluss die Strichrechnung
    :::

    !! Reihenfolge: Klammern, dann Punkt vor Strich, dann von links nach rechts.

    :::alt Mit einem Schild erklärt
    Eine Klammer ist wie ein Schild mit der Aufschrift „Das hier zuerst!“. Sie
    steht über allen anderen Regeln. Ohne Klammer gilt Punkt vor Strich. Mit
    Klammer kannst du diese Regel absichtlich umgehen: $(2 + 3) \cdot 4 = 20$.
    :::
    ---
    ## Gleicher Rang: von links nach rechts

    Mal und geteilt sind **gleichrangig**. Plus und minus auch. Dann rechnest du
    einfach von links nach rechts.

    :::rechnung Beispiel vorgerechnet
    12 : 3 \cdot 2 = 4 \cdot 2 || links anfangen: $12 : 3 = 4$
    = 8 || dann mal $2$
    10 - 4 - 3 = 6 - 3 || links anfangen: $10 - 4 = 6$
    = 3 || dann minus $3$
    :::

    :::achtung Rechts anfangen
    $10 - 4 - 3 = 10 - 1 = 9$ ist falsch. Hier wurde $4 - 3$ zuerst gerechnet.
    Ohne Klammer gilt: von links nach rechts.
    :::

    :::alt Warum die Reihenfolge zählt
    Probier $8 : 4 : 2$ auf zwei Arten. Von links: $8 : 4 = 2$, dann $2 : 2 = 1$.
    Von rechts: $4 : 2 = 2$, dann $8 : 2 = 4$. Zwei verschiedene Ergebnisse!
    Damit alle dasselbe herausbekommen, gibt es eine feste Abmachung: Ohne
    Klammer wird von links nach rechts gerechnet. Ergebnis: $1$.
    :::
    """)

k.berechne("2 + 3*4",
           erklaerung="Punkt vor Strich: $3 \\cdot 4 = 12$, dann $2 + 12 = 14$.",
           tipps=["Welche Rechnung kommt zuerst: plus oder mal?", "Rechne zuerst $3 \\cdot 4$.",
                  "$2 + 12$"],
           rechenweg=r"""
           :::rechnung
           2 + \hl{3 \cdot 4} = 2 + 12 || Punkt vor Strich
           = 14 || addieren
           :::
           """,
           typische_fehler=[(20, "Du hast von links nach rechts gerechnet: $(2 + 3) \\cdot 4$. Punkt vor Strich: erst $3 \\cdot 4 = 12$.")])

k.berechne("18 - 2*(3+4)",
           erklaerung="Klammer: $3 + 4 = 7$. Punkt vor Strich: $2 \\cdot 7 = 14$. Dann $18 - 14 = 4$.",
           tipps=["Was steht in der Klammer?", "Nach der Klammer: $18 - 2 \\cdot 7$. Was kommt jetzt zuerst?",
                  "$2 \\cdot 7 = 14$, dann $18 - 14$."],
           rechenweg=r"""
           :::rechnung
           18 - 2 \cdot (3 + 4) = 18 - 2 \cdot 7 || Klammer zuerst
           = 18 - 14 || Punkt vor Strich
           = 4 || subtrahieren
           :::
           """,
           typische_fehler=[(112, "Du hast $18 - 2 = 16$ zuerst gerechnet. Punkt vor Strich: erst $2 \\cdot 7$."),
                            (16, "Du hast die Klammer weggelassen: $18 - 2 \\cdot 3 + 4$. Die Klammer gilt als Ganzes.")])

k.zahl("Berechne $12 : 3 \\cdot 2$.", F(12, 3) * 2,
       "Mal und geteilt sind gleichrangig: von links nach rechts. $12 : 3 = 4$, dann $4 \\cdot 2 = 8$.",
       tipps=["Mal und geteilt haben denselben Rang.", "Bei gleichem Rang: von links nach rechts.",
              "Erst $12 : 3$."],
       rechenweg=r"""
       :::rechnung
       12 : 3 \cdot 2 = 4 \cdot 2 || von links: $12 : 3 = 4$
       = 8 || dann malnehmen
       :::
       """,
       typische_fehler=[(2, "Du hast $3 \\cdot 2$ zuerst gerechnet. Mal und geteilt sind gleichrangig: von links nach rechts.")])

k.berechne("10 - 4 - 3",
           erklaerung="Von links nach rechts: $10 - 4 = 6$, dann $6 - 3 = 3$.",
           tipps=["Beide Rechenzeichen sind minus, also gleichrangig.", "Von links nach rechts: zuerst $10 - 4$.",
                  "$6 - 3$"],
           rechenweg=r"""
           :::rechnung
           10 - 4 - 3 = 6 - 3 || von links: $10 - 4 = 6$
           = 3 || dann minus $3$
           :::
           """,
           typische_fehler=[(9, "Du hast $4 - 3$ zuerst gerechnet. Ohne Klammer: von links nach rechts.")])

# ── 4: Minusklammer ────────────────────────────────────────────────────────
k.erklaerung("Minus vor der Klammer", r"""
    ## Die Minusklammer dreht alles um

    Steht ein Minus vor einer Klammer, hast du zwei Wege. Beide geben dasselbe.

    :::rechnung Weg 1: Klammer zuerst ausrechnen
    10 - (3 - 5) = 10 - (-2) || Klammer: $3 - 5 = -2$
    = 10 + 2 || Minus minus wird plus
    = 12 || ausrechnen
    :::

    :::rechnung Weg 2: Klammer auflösen
    10 - (3 - 5) = 10 - 3 + 5 || jedes Vorzeichen in der Klammer umdrehen
    = 7 + 5 || von links nach rechts
    = 12 || dasselbe Ergebnis
    :::

    !! Ein Minus vor der Klammer dreht **jedes** Vorzeichen in der Klammer um.

    :::achtung Nur das erste Vorzeichen umdrehen
    $10 - (3 - 5) = 10 - 3 - 5 = 2$ ist falsch. Das zweite Vorzeichen wurde nicht
    umgedreht.
    :::

    :::alt Mit einer Tüte erklärt
    Du hast $10$ Euro. In einer Tüte liegt Ware für $3$ Euro (zählt $+3$) und
    eine offene Rechnung über $5$ Euro (zählt $-5$). Jetzt gibst du die ganze
    Tüte weg, das ist das Minus vor der Klammer. Die Ware ist weg: $-3$. Die
    Rechnung ist auch weg, du musst die $5$ Euro nicht mehr zahlen: $+5$. Also
    $10 - (3 - 5) = 10 - 3 + 5 = 12$.
    :::
    """)

k.berechne("10 - (3 - 5)",
           erklaerung="Klammer zuerst: $3 - 5 = -2$. Dann $10 - (-2) = 12$. Oder Klammer auflösen: $10 - 3 + 5 = 12$.",
           tipps=["Rechne zuerst die Klammer aus.", "$3 - 5 = -2$. Was ist $10 - (-2)$?",
                  "Minus minus wird plus: $10 + 2$."],
           rechenweg=r"""
           :::rechnung
           10 - (3 - 5) = 10 - (-2) || Klammer zuerst
           = 10 + 2 || Minus minus wird plus
           = 12 || ausrechnen
           :::
           """,
           typische_fehler=[(2, "Du hast nur das erste Vorzeichen umgedreht: $10 - 3 - 5$. Die Minusklammer dreht **jedes** Vorzeichen: $10 - 3 + 5$."),
                            (8, "Du hast $10 + (-2)$ gerechnet. Es heißt aber $10 - (-2)$: Minus minus wird plus.")])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


def vorzeichen_rechnen(rng):
    op = rng.choice(["+", "-", "*", ":"])
    nz = [z for z in range(-12, 13) if z not in (0, 1, -1)]
    if op == ":":
        b, q = rng.choice(nz[2:-2]), rng.choice(nz[2:-2])
        if b > 0 and q > 0:
            b = -b                # mindestens eine negative Zahl
        a = b * q
    else:
        a = rng.choice([z for z in range(-15, 16) if z])
        b = rng.choice(nz)
        if a > 0 and b > 0:
            b = -b                # mindestens eine negative Zahl
    if op in "+-":
        w = a + b if op == "+" else a - b
        schritte = abs(b)
        nach = "rechts" if (op == "+") == (b > 0) else "links"
        if b < 0:
            umform = f"{a} {op} {tk(b)} = {a} {'-' if op == '+' else '+'} {abs(b)}"
            grund = "Plus minus wird minus" if op == "+" else "Minus minus wird plus"
            weg = _zeilen((umform, grund), (f"= {w}", f"von ${a}$ aus ${schritte}$ Schritte nach {nach}"))
        else:
            weg = _zeilen((f"{a} {op} {b} = {w}", f"von ${a}$ aus ${schritte}$ Schritte nach {nach}"))
        regel = ("Plus eine negative Zahl heißt: nach links gehen." if op == "+" else
                 "Minus eine negative Zahl ist dasselbe wie plus.") if b < 0 else \
            ("Plus heißt: nach rechts gehen." if op == "+" else "Minus heißt: nach links gehen.")
        tipps = [f"Starte bei ${a}$ auf der Zahlengeraden.", regel, f"Gehe ${schritte}$ Schritte nach {nach}."]
        if op == "+":
            fehler = [(-w, "Das Vorzeichen stimmt nicht. Geh auf der Zahlengeraden nach: Wo landest du?"),
                      (a - b, "Du hast subtrahiert statt addiert.")]
        else:
            fehler = [(a + b, "Minus minus wird plus! $a - (-b) = a + b$." if b < 0 else "Du hast addiert statt subtrahiert."),
                      (-w, "Das Vorzeichen stimmt nicht. Geh auf der Zahlengeraden nach.")]
    else:
        w = a * b if op == "*" else a // b
        zeichen = "\\cdot" if op == "*" else ":"
        regel = ("Gleiche Vorzeichen: plus. Verschiedene Vorzeichen: minus." if op == "*" else
                 "Beim Teilen gilt dieselbe Vorzeichenregel wie beim Malnehmen.")
        weg = _zeilen((f"{abs(a)} {zeichen} {abs(b)} = {abs(w)}", "erst ohne Vorzeichen"),
                      (f"{tk(a)} {zeichen} {tk(b)} = {w}", "gleiche Vorzeichen: plus" if w > 0 else "verschiedene Vorzeichen: minus"))
        tipps = ["Rechne zuerst ohne Vorzeichen.", regel, "Bestimme am Ende das Vorzeichen."]
        fehler = [(-w, "Vorzeichenregel: gleiche Vorzeichen ergeben plus, verschiedene minus.")]
        if op == "*":
            fehler.append((a + b, "Du hast addiert statt malgenommen."))
    op_tex = {"+": "+", "-": "-", "*": "\\cdot", ":": ":"}[op]
    return {
        "frage": f"Berechne ${tk(a) if op in '*:' else a} {op_tex} {tk(b)}$.",
        "loesung": w,
        "tipps": tipps,
        "rechenweg": weg,
        "erklaerung": regel,
        "typische_fehler": ohne_gleiche(w, fehler),
    }


k.praxis()

k.generator(vorzeichen_rechnen, typ="zahl", titel="Rechnen mit Vorzeichen", glatt=True)


def reihenfolge(rng):
    art = rng.choice(["a+bc", "a-bc", "a(b+c)-d", "(a-b)c+d", "a:bc"])
    z = lambda lo, hi: rng.randint(lo, hi)  # noqa: E731
    if art == "a+bc":
        a, b, c = z(1, 20), z(2, 9), rng.choice([x for x in range(-6, 10) if x not in (0, 1)])
        w, links = a + b * c, (a + b) * c
        frage = f"{a} + {b} \\cdot {tk(c)}"
        weg = _zeilen((f"{a} + \\hl{{{b} \\cdot {tk(c)}}}", "Punkt vor Strich"),
                      (f"= {a} + {tk(b * c)}", f"${b} \\cdot {tk(c)} = {b * c}$"), (f"= {w}", "addieren"))
        fehler = [(links, "Du hast von links nach rechts gerechnet. Punkt vor Strich: erst das Mal.")]
    elif art == "a-bc":
        a, b, c = z(1, 20), z(2, 9), rng.choice([x for x in range(-6, 10) if x not in (0, 1)])
        w, links = a - b * c, (a - b) * c
        frage = f"{a} - {b} \\cdot {tk(c)}"
        weg = _zeilen((f"{a} - \\hl{{{b} \\cdot {tk(c)}}}", "Punkt vor Strich"),
                      (f"= {a} - {tk(b * c)}", f"${b} \\cdot {tk(c)} = {b * c}$"), (f"= {w}", "subtrahieren"))
        fehler = [(links, "Du hast von links nach rechts gerechnet. Punkt vor Strich: erst das Mal."),
                  (a + b * c, f"Minus minus wird plus: ${a} - ({b * c}) = {a} + {-b * c}$." if c < 0
                   else "Achte auf das Vorzeichen: Das Produkt wird **abgezogen**.")]
    elif art == "a(b+c)-d":
        a, b, c, d = z(2, 6), z(-5, 8), z(-5, 8), z(1, 15)
        if b + c == 0:
            c += 1
        w = a * (b + c) - d
        frage = f"{a} \\cdot ({b} + {tk(c)}) - {d}"
        weg = _zeilen((f"{a} \\cdot \\hl{{({b} + {tk(c)})}} - {d}", "Klammer zuerst"),
                      (f"= {a} \\cdot {tk(b + c)} - {d}", f"${b} + {tk(c)} = {b + c}$"),
                      (f"= {a * (b + c)} - {d}", "Punkt vor Strich"), (f"= {w}", "subtrahieren"))
        fehler = [(a * b + c - d, "Du hast die Klammer weggelassen. Die Klammer wird als Ganzes malgenommen."),
                  (a * (b + c) + d, "Am Ende wird $" + str(d) + "$ **abgezogen**.")]
    elif art == "(a-b)c+d":
        a, b, c = z(-5, 10), z(1, 12), rng.choice([x for x in range(-4, 7) if x not in (0, 1)])
        d = rng.choice([x for x in range(-10, 11) if x])
        if a == b:
            a += 1
        w = (a - b) * c + d
        frage = f"({a} - {b}) \\cdot {tk(c)} + {tk(d)}"
        weg = _zeilen((f"\\hl{{({a} - {b})}} \\cdot {tk(c)} + {tk(d)}", "Klammer zuerst"),
                      (f"= {tk(a - b)} \\cdot {tk(c)} + {tk(d)}", f"${a} - {b} = {a - b}$"),
                      (f"= {tk((a - b) * c)} + {tk(d)}", "Punkt vor Strich, Vorzeichenregel"), (f"= {w}", "addieren"))
        fehler = [(a - b * c + d, "Du hast die Klammer weggelassen. Erst $" + f"{a} - {b}" + "$ ausrechnen."),
                  (-(a - b) * c + d, "Vorzeichenregel beim Malnehmen beachten.")]
    else:
        b, c = z(2, 6), z(2, 5)
        a = b * z(2, 9) * (1 if rng.random() < 0.6 else -1)
        w = F(a, b) * c
        frage = f"{a} : {b} \\cdot {c}"
        weg = _zeilen((f"{a} : {b} \\cdot {c} = {a // b} \\cdot {c}", f"von links: ${a} : {b} = {a // b}$"),
                      (f"= {w}", "dann malnehmen"))
        fehler = [(F(a, b * c), f"Mal und geteilt sind gleichrangig: von links nach rechts, nicht erst ${b} \\cdot {c}$.")]
    return {
        "frage": f"Berechne ${frage}$.",
        "loesung": w,
        "tipps": ["Gibt es eine Klammer? Die kommt zuerst.", "Danach Punkt vor Strich.",
                  "Bei gleichem Rang: von links nach rechts."],
        "rechenweg": weg,
        "erklaerung": "Reihenfolge: Klammern, dann Punkt vor Strich, dann von links nach rechts.",
        "typische_fehler": ohne_gleiche(w, fehler),
    }


k.generator(reihenfolge, typ="zahl", titel="Reihenfolge der Rechenarten", glatt=True)

# Übungsblatt: lange Rechnung in Teilschritten (alle Werte rechnet Python)
_k1 = 4 - 7
_p1 = -3 * _k1
_q1 = F(12, -4)
_p2 = (-2) * (-5)
_ges = _p1 - _q1 + _p2
k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: ohne Taschenrechner, jeder Zwischenschritt

    Berechne
    $$-3 \cdot (4 - 7) - 12 : (-4) + (-2) \cdot (-5)$$
    Gehe Schritt für Schritt vor: erst die Klammer, dann alle Punktrechnungen,
    zum Schluss die Strichrechnung.
    """,
    [{"typ": "zahl", "frage": "Berechne die Klammer $4 - 7$.", "loesung": _k1,
      "tipps": ["Von $4$ aus $7$ nach links.", "Das Ergebnis ist negativ."],
      "rechenweg": "$4 - 7 = -3$", "typische_fehler": [(3, "Vorzeichen: Du landest unter null.")]},
     {"typ": "zahl", "frage": "Berechne $-3 \\cdot (-3)$.", "loesung": _p1,
      "tipps": ["Minus mal minus …", "… gibt plus."], "rechenweg": "$-3 \\cdot (-3) = 9$",
      "typische_fehler": [(-9, "Minus mal minus gibt plus.")]},
     {"typ": "zahl", "frage": "Berechne $12 : (-4)$.", "loesung": _q1,
      "tipps": ["Erst ohne Vorzeichen: $12 : 4$.", "Verschiedene Vorzeichen: minus."], "rechenweg": "$12 : (-4) = -3$",
      "typische_fehler": [(3, "Verschiedene Vorzeichen ergeben minus.")]},
     {"typ": "zahl", "frage": "Berechne $(-2) \\cdot (-5)$.", "loesung": _p2,
      "tipps": ["Zwei gleiche Vorzeichen.", "$2 \\cdot 5 = 10$, Vorzeichen plus."], "rechenweg": "$(-2) \\cdot (-5) = 10$",
      "typische_fehler": [(-10, "Minus mal minus gibt plus.")]},
     {"typ": "zahl", "frage": "Setze zusammen: $9 - (-3) + 10$.", "loesung": _ges,
      "tipps": ["$-(-3)$ wird zu $+3$.", "$9 + 3 + 10$"], "rechenweg": "$9 - (-3) + 10 = 9 + 3 + 10 = 22$",
      "typische_fehler": [(16, "Minus minus wird plus: $9 - (-3) = 12$, nicht $6$.")]}],
    "Klammer, dann alle Punktrechnungen, dann von links nach rechts zusammenzählen.",
    uebungsblatt=True,
    tipps=["Arbeite die Reihenfolge ab: Klammer, Punkt, Strich.", "Schreib dir jedes Zwischenergebnis auf."],
    rechenweg=r"""
    :::rechnung
    -3 \cdot \hl{(4 - 7)} - 12 : (-4) + (-2) \cdot (-5) || Klammer zuerst
    = \hl{-3 \cdot (-3)} - \hl{12 : (-4)} + \hl{(-2) \cdot (-5)} || alle Punktrechnungen
    = 9 - (-3) + 10 || Zwischenergebnisse einsetzen
    = 9 + 3 + 10 || Minus minus wird plus
    = 22 || zusammenzählen
    :::
    """)

k.zusammenfassung(r"""
    ## Rechnen mit Vorzeichen

    | Regel | Beispiel |
    |---|---|
    | Plus: nach rechts, Minus: nach links | $3 - 5 = -2$ |
    | Minus minus wird plus | $4 - (-3) = 7$ |
    | gleiche Vorzeichen: plus | $(-3) \cdot (-4) = 12$ |
    | verschiedene Vorzeichen: minus | $(-12) : 4 = -3$ |
    | durch $0$ teilen geht nicht | $5 : 0$ ist nicht definiert |

    !! Reihenfolge: Klammern, dann Punkt vor Strich, dann von links nach rechts.

    - Minus vor der Klammer dreht **jedes** Vorzeichen um: $10 - (3 - 5) = 10 - 3 + 5$.
    - Gerade Anzahl Minus beim Malnehmen: plus. Ungerade Anzahl: minus.
""")
