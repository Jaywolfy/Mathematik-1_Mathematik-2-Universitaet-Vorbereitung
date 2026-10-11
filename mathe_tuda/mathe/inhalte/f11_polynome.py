# -*- coding: utf-8 -*-
"""Fundament 11: Polynome – Grad, Nullstellen raten, Polynomdivision, Linearfaktoren, Horner-Schema."""
import textwrap
from fractions import Fraction as F

from .. import mathlib, pruefer
from ..engine import neues_kapitel, ohne_gleiche

tex = mathlib.tex
tk = mathlib.tex_klammer
vz = mathlib.vorzeichen_tex
P = mathlib.Polynom


# ── Hilfen: Polynomdivision als Rechnung und als Papierschema ─────────────
def _glied(c, e, mit_vz):
    """Ein Summand c·x^e als LaTeX, wahlweise mit Rechenzeichen davor."""
    c = F(c)
    if e == 0:
        rumpf = tex(abs(c))
    else:
        rumpf = ("" if abs(c) == 1 else tex(abs(c))) + ("x" if e == 1 else f"x^{{{e}}}")
    if mit_vz:
        return ("- " if c < 0 else "+ ") + rumpf
    return ("-" if c < 0 else "") + rumpf


def divisions_schema(p, d):
    """Schriftliche Polynomdivision als LaTeX-array, so wie man sie auf Papier schreibt."""
    n = p.grad()
    spalten = n + 1
    q, r, schritte = p.divmod(d)

    def zeile(zellen):
        return " & ".join(zellen.get(n - j, "") for j in range(spalten))

    kopf = {e: _glied(p.k.get(e, F(0)), e, e != n) for e in range(n, -1, -1)}
    ergebnis = q.tex() + (f" \\text{{ Rest }} {r.tex()}" if r.k else "")
    zeilen = [zeile(kopf) + f" & : ({d.tex()}) = {ergebnis}"]
    for i, s in enumerate(schritte):
        rv, ab = s["rest_vorher"], s["abzug"]
        oben = rv.grad()
        exps = list(range(oben, oben - d.grad() - 1, -1))
        z = {}
        for j, e in enumerate(exps):
            t = _glied(ab.k.get(e, F(0)), e, j > 0)
            if j == 0:
                t = "-(" + t
            if j == len(exps) - 1:
                t = t + ")"
            z[e] = "\\underline{" + t + "}"
        zeilen.append(zeile(z) + " & ")
        neu = rv - ab
        letzter = i == len(schritte) - 1
        unten = max(0, oben - d.grad() - (0 if letzter else 1))
        z, erste = {}, True
        rest_exps = list(range(oben - 1, unten - 1, -1))
        for e in rest_exps:
            c = neu.k.get(e, F(0))
            if c == 0 and erste:
                continue
            z[e] = _glied(c, e, not erste)
            erste = False
        if not z:
            z[rest_exps[-1] if rest_exps else 0] = "0"
        zeilen.append(zeile(z) + " & ")
    return "$$\n\\begin{array}{" + "r" * spalten + "l}\n" + " \\\\\n".join(zeilen) + "\n\\end{array}\n$$"


def divisions_zeilen(p, d):
    """(Quotient, Rest, Zeilen) einer Polynomdivision; jede Zeile ist nachrechenbar."""
    q, r, schritte = p.divmod(d)
    zeilen = []
    lead_d = _glied(d.lc(), d.grad(), False)
    for s in schritte:
        rv, t, ab = s["rest_vorher"], s["term"], s["abzug"]
        neu = rv - ab
        zeilen.append((f"{_glied(rv.lc(), rv.grad(), False)} : {lead_d} = {t.tex()}",
                       "teilen: höchste Potenz durch höchste Potenz"))
        zeilen.append((f"{t.tex()} \\cdot ({d.tex()}) = {ab.tex()}", "zurückmultiplizieren"))
        zeilen.append((f"({rv.tex()}) - ({ab.tex()}) = {neu.tex()}",
                       "abziehen" + (": Rest $0$, fertig" if not neu.k else "")))
    if r.k:
        zeilen.append((f"({p.tex()}) : ({d.tex()}) = {q.tex()} + \\frac{{{r.tex()}}}{{{d.tex()}}}",
                       f"Ergebnis mit Rest ${r.tex()}$"))
    else:
        zeilen.append((f"({p.tex()}) : ({d.tex()}) = {q.tex()}", "Ergebnis"))
    return q, r, zeilen


def _rechnung(zeilen, titel=""):
    kopf = ":::rechnung" + (f" {titel}" if titel else "")
    return kopf + "\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def _division_markup(p, d, titel=""):
    """Schema + Rechnung als Markup-Block (ohne Einrückung)."""
    _, _, zeilen = divisions_zeilen(p, d)
    return divisions_schema(p, d) + "\n\n" + _rechnung(zeilen, titel)


def _seite(text, **teile):
    """Markup-Text ausrücken und Platzhalter @NAME@ durch erzeugte Blöcke ersetzen."""
    t = textwrap.dedent(text)
    for name, inhalt in teile.items():
        t = t.replace(f"@{name}@", inhalt)
    return t


def _einsetzen(p, x0):
    """p(x0) Summand für Summand als LaTeX: (Aufgabe, Zwischenzeile, Wert)."""
    teile, werte = [], []
    for e in sorted(p.k, reverse=True):
        c = p.k[e]
        if e == 0:
            teile.append(tex(c) if not teile else vz(c))
        else:
            pot = tk(x0) if e == 1 else f"{tk(x0)}^{{{e}}}"
            koeff = "" if abs(c) == 1 else f"{tex(abs(c))} \\cdot "
            vorz = ("-" if c < 0 else "") if not teile else ("- " if c < 0 else "+ ")
            teile.append(vorz + koeff + pot)
        werte.append(c * F(x0) ** e)
    zwischen = " ".join((tex(w) if i == 0 else vz(w)) for i, w in enumerate(werte))
    return " ".join(teile), zwischen, sum(werte)


def _horner(koeff, x0):
    """koeff von der höchsten Potenz abwärts. Rückgabe: Liste b (untere Zeile)."""
    b = [F(koeff[0])]
    for a in koeff[1:]:
        b.append(b[-1] * x0 + a)
    return b


def _horner_markup(koeff, x0):
    b = _horner(koeff, x0)
    kopf = "| | " + " | ".join(f"${tex(a)}$" for a in koeff) + " |"
    trenner = "|---" * (len(koeff) + 1) + "|"
    mitte = f"| $x_0 = {tex(x0)}$ | | " + " | ".join(f"${tex(v * x0)}$" for v in b[:-1]) + " |"
    unten = "| | " + " | ".join(f"${tex(v)}$" for v in b) + " |"
    zeilen = [(f"{tex(b[0])}", "erster Koeffizient: herunterschreiben")]
    for i, a in enumerate(koeff[1:], 1):
        zeilen.append((f"{tk(b[i - 1])} \\cdot {tk(x0)} + {tk(a)} = {tex(b[i])}",
                       "mal $x_0$, plus nächster Koeffizient" + (": das ist $p(x_0)$" if i == len(koeff) - 1 else "")))
    return "\n".join([kopf, trenner, mitte, unten]) + "\n\n" + _rechnung(zeilen), b


def _ohne_gleiche_term(loesung, fehler, var="x"):
    """Wie engine.ohne_gleiche, aber für Terme (Äquivalenz statt Zahlvergleich)."""
    soll = pruefer.parse(loesung, [var]).ast
    erg, gesehen = [], []
    for w, m in fehler:
        a = pruefer.parse(w, [var]).ast
        if pruefer.aequivalent(a, soll, [var]).ok or any(pruefer.aequivalent(a, g, [var]).ok for g in gesehen):
            continue
        gesehen.append(a)
        erg.append((w, m))
    return erg


def _ohne_gleiche_menge(loesung, fehler):
    soll = pruefer.bereich_parsen(loesung)
    erg, gesehen = [], []
    for w, m in fehler:
        v = pruefer.bereich_parsen(w)
        if pruefer.bereiche_gleich(v, soll) or any(pruefer.bereiche_gleich(v, g) for g in gesehen):
            continue
        gesehen.append(v)
        erg.append((w, m))
    return erg


def _faktor(r):
    return "x" if r == 0 else f"(x {vz(-r)})"


k = neues_kapitel(
    slug="polynome",
    titel="Polynome und Polynomdivision",
    beschreibung="Grad und Koeffizienten, Nullstellen raten, Polynomdivision, Linearfaktoren, Horner-Schema",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="🧱")

k.lernziele([
    "Ich erkenne Polynome und bestimme Grad, Koeffizienten und Leitkoeffizient",
    "Ich finde ganzzahlige Nullstellen durch Raten unter den Teilern des Absolutglieds",
    "Ich führe eine Polynomdivision mit allen Zwischenschritten durch, auch mit Rest",
    "Ich zerlege ein Polynom in Linearfaktoren",
    "Ich werte Polynome mit dem Horner-Schema aus und teile damit durch $(x - x_0)$",
])

k.warum(r"""
Polynome sind die Lieblingsfunktionen der Informatik, weil ein Computer sie nur mit
Plus und Mal ausrechnen kann. Das [[Horner-Schema]] ist der schnellste Weg dazu und
steckt in jeder Hashfunktion für Texte (Rabin-Karp-Suche). Prüfsummen wie CRC, die
Fehler in Netzwerkpaketen finden, sind eine [[Polynomdivision]] mit Rest. In Mathe 1
sind Eigenwerte die Nullstellen eines Polynoms, im Vorkurs brauchst du Nullstellen für
Kurvendiskussionen und die Polynomdivision für Grenzwerte und Integrale.
""")

# ── 1: Was ist ein Polynom ────────────────────────────────────────────────
k.erklaerung("Was ist ein Polynom?", r"""
    ## Ein Baukasten aus Potenzen

    :::analogie 🧱 Bausteine
    Du hast Bausteine $1, x, x^2, x^3, \ldots$ Von jedem nimmst du eine feste Anzahl
    und zählst alles zusammen. Was herauskommt, ist ein Polynom.
    :::

    Ein [[Polynom]] ist eine Summe $a_n x^n + \ldots + a_1 x + a_0$. Die Zahlen $a_i$
    heißen [[Koeffizienten|Koeffizient]]. Die höchste Potenz mit $a_n \neq 0$ ist der
    [[Grad]], $a_n$ der [[Leitkoeffizient]], $a_0$ das [[Absolutglied]].

    Bei $p(x) = 2x^3 - x + 5$ ist der Grad $3$, der Leitkoeffizient $2$, das
    Absolutglied $5$. Der Koeffizient von $x^2$ ist $0$.

    :::rechnung $p(2)$ ausrechnen
    2 \cdot 2^3 - 2 + 5 = 16 - 2 + 5 || $x = 2$ einsetzen
    = 19 || ausrechnen
    :::

    :::alt Mit dem Zehnersystem erklärt
    Die Zahl $345$ ist $3 \cdot 10^2 + 4 \cdot 10 + 5$. Ersetze die $10$ durch $x$:
    $3x^2 + 4x + 5$. Ein Polynom ist also wie eine Zahl mit Ziffern, nur dass die
    Basis $x$ frei wählbar ist und die Ziffern beliebige Zahlen sein dürfen.
    :::
    ---
    ## Höchstens $n$ Nullstellen

    Eine [[Nullstelle]] von $p$ ist eine Zahl $x_0$ mit $p(x_0) = 0$.

    !! Ein Polynom vom Grad $n \ge 1$ hat höchstens $n$ Nullstellen.

    :::visual funktionsgraph
    {"funktionen": [{"term": "x^3 - 6*x^2 + 11*x - 6", "label": "p(x)"}],
     "nullstellen": true, "x": [-1, 5], "y": [-4, 4],
     "unterschrift": "Grad $3$, drei Nullstellen: $1$, $2$ und $3$. Mehr geht nicht."}
    :::

    :::rechnung Ist $1$ eine Nullstelle von $x^3 - 6x^2 + 11x - 6$?
    1^3 - 6 \cdot 1^2 + 11 \cdot 1 - 6 = 1 - 6 + 11 - 6 || einsetzen
    = 0 || ja, $1$ ist eine Nullstelle
    :::

    :::alt Mit einer Achterbahn erklärt
    Stell dir den Graphen als Achterbahn vor. Ein Polynom vom Grad $3$ kann höchstens
    zweimal die Richtung wechseln (einmal hoch, einmal runter). Damit kreuzt die Bahn
    den Boden, also die $x$-Achse, höchstens dreimal. Je höher der Grad, desto mehr
    Kurven sind möglich.
    :::
    """)

k.zahl("Welchen Grad hat $p(x) = 3x^4 - x^7 + 2$?", 7,
       "Der Grad ist die höchste vorkommende Potenz: $x^7$. Die Reihenfolge der Summanden spielt keine Rolle.",
       tipps=["Der Grad ist die **höchste** Potenz von $x$.", "Schau dir alle Exponenten an: $4$, $7$ und $0$.",
              "Der größte Exponent ist $7$."],
       rechenweg=r"""
       :::rechnung
       -x^7 + 3x^4 + 2 = 3x^4 - x^7 + 2 || nach Potenzen sortiert: Die höchste ist $x^7$
       :::
       """,
       typische_fehler=[(4, "Du hast den Exponenten des ersten Summanden genommen. Der Grad ist die **höchste** Potenz, egal wo sie steht."),
                        (3, "Das ist ein Koeffizient. Gefragt ist der höchste **Exponent**.")])

k.zahl("Wie heißt der Leitkoeffizient von $p(x) = 3x^4 - x^7 + 2$?", -1,
       "Der Leitkoeffizient gehört zur höchsten Potenz $x^7$. Vor $x^7$ steht $-1$.",
       tipps=["Erst die höchste Potenz suchen.", "Die höchste Potenz ist $x^7$. Welche Zahl steht davor?",
              "$-x^7 = -1 \\cdot x^7$"],
       rechenweg=r"""
       :::rechnung
       -x^7 + 3x^4 + 2 = -1 \cdot x^7 + 3x^4 + 2 || vor der höchsten Potenz steht $-1$
       :::
       """,
       typische_fehler=[(3, "$3$ steht vor $x^4$. Der Leitkoeffizient gehört zur **höchsten** Potenz $x^7$."),
                        (1, "Das Vorzeichen gehört dazu: $-x^7 = -1 \\cdot x^7$.")])

k.mehrfach("Welche Ausdrücke sind Polynome in $x$?",
           ["$3x^2 - 1$", "$\\frac{1}{2}x^5 + x$", "$7$"],
           ["$\\frac{1}{x} + x$", "$\\sqrt{x} + 1$", "$2^x$"],
           "Polynome haben nur Potenzen $x^0, x^1, x^2, \\ldots$ mit natürlichen Exponenten. "
           "$\\frac{1}{x} = x^{-1}$, $\\sqrt{x} = x^{1/2}$ und $2^x$ (Variable im Exponenten) gehören nicht dazu. "
           "Eine Zahl wie $7 = 7x^0$ ist ein Polynom vom Grad $0$.",
           tipps=["Erlaubt sind nur $x^0, x^1, x^2, \\ldots$, also Exponenten $0, 1, 2, \\ldots$",
                  "Schreibe $\\frac{1}{x}$ und $\\sqrt{x}$ als Potenz."],
           fehler={"$\\frac{1}{x} + x$": "$\\frac{1}{x} = x^{-1}$ hat einen negativen Exponenten. Das ist kein Polynom.",
                   "$\\sqrt{x} + 1$": "$\\sqrt{x} = x^{1/2}$: Der Exponent ist keine natürliche Zahl.",
                   "$2^x$": "Hier steht $x$ im Exponenten. Bei Polynomen ist $x$ die Basis, der Exponent eine feste Zahl."})

k.zahl("Berechne $p(-1)$ für $p(x) = x^3 - 2x^2 - 5x + 6$.", P.aus_text("x^3 - 2x^2 - 5x + 6")(-1),
       "$(-1)^3 = -1$ und $(-1)^2 = 1$. Also $-1 - 2 + 5 + 6 = 8$.",
       tipps=["Setze $(-1)$ mit Klammern ein.", "Ungerade Potenz von $-1$ ist $-1$, gerade ist $1$.",
              "$-1 - 2 \\cdot 1 - 5 \\cdot (-1) + 6$"],
       rechenweg=r"""
       :::rechnung
       (-1)^3 - 2 \cdot (-1)^2 - 5 \cdot (-1) + 6 = -1 - 2 + 5 + 6 || einsetzen, Potenzen zuerst
       = 8 || zusammenzählen
       :::
       """,
       typische_fehler=[(10, "$(-1)^3 = -1$, nicht $1$: Drei Minus ergeben minus."),
                        (12, "$(-1)^2 = 1$, nicht $-1$: Zwei Minus ergeben plus.")])

k.wf("Ein Polynom vom Grad $3$ kann vier verschiedene Nullstellen haben.", False,
     "Falsch. Ein Polynom vom Grad $n \\ge 1$ hat höchstens $n$ Nullstellen, bei Grad $3$ also höchstens drei.",
     tipps=["Denk an die Regel: Grad $n$, höchstens … Nullstellen."])

# ── 2: Nullstellen raten ──────────────────────────────────────────────────
k.erklaerung("Nullstellen raten", r"""
    ## Kandidaten: die Teiler des Absolutglieds

    Für Grad $3$ und höher gibt es keine einfache Formel wie die pq-Formel. Man rät
    eine Nullstelle, aber mit System:

    !! Sind alle Koeffizienten ganze Zahlen und ist der Leitkoeffizient $1$, dann ist jede ganzzahlige Nullstelle ein Teiler des Absolutglieds.

    Teiler heißt: positive **und** negative.

    :::rechnung $x^3 - 2x^2 - 5x + 6$: Kandidaten $\pm 1, \pm 2, \pm 3, \pm 6$
    1^3 - 2 \cdot 1^2 - 5 \cdot 1 + 6 = 1 - 2 - 5 + 6 || $x = 1$ probieren
    = 0 || Treffer: $1$ ist eine Nullstelle
    :::

    :::achtung Nur positive Teiler probiert
    Die Teiler von $6$ sind $\pm 1, \pm 2, \pm 3, \pm 6$. Wer nur $1, 2, 3, 6$ probiert,
    übersieht hier die Nullstelle $-2$.
    :::

    :::alt Warum das funktioniert
    Ist $x_0$ eine ganze Nullstelle, dann gilt $x_0^3 - 2x_0^2 - 5x_0 + 6 = 0$, also
    $x_0 \cdot (x_0^2 - 2x_0 - 5) = -6$. Links steht $x_0$ mal eine ganze Zahl. Also
    teilt $x_0$ die Zahl $6$. Das klappt bei jedem Polynom dieser Art: Man klammert
    $x_0$ aus allen Summanden außer dem Absolutglied aus.
    :::
    """)

k.menge("Welche ganzen Zahlen kommen als Nullstellen von $x^3 + x^2 - 4x - 4$ in Frage? Gib alle Kandidaten an.",
        "{-4; -2; -1; 1; 2; 4}",
        "Kandidaten sind alle Teiler des Absolutglieds $-4$: $\\pm 1, \\pm 2, \\pm 4$. "
        "(Wirklich Nullstellen sind davon $-2$, $-1$ und $2$.)",
        tipps=["Schau auf das Absolutglied, die Zahl ohne $x$.", "Das Absolutglied ist $-4$. Welche Zahlen teilen $4$?",
               "Positive und negative Teiler: $\\pm 1, \\pm 2, \\pm 4$."],
        rechenweg=r"""
        :::rechnung
        4 = 1 \cdot 4 = 2 \cdot 2 || Teiler von $4$: $1$, $2$, $4$
        (-1) \cdot (-4) = 4 || auch die negativen Teiler zählen
        :::

        Kandidaten: $\{-4; -2; -1; 1; 2; 4\}$.
        """,
        typische_fehler=[("{1; 2; 4}", "Die negativen Teiler fehlen. Auch $-1$, $-2$ und $-4$ teilen $-4$."),
                         ("{-2; -1; 2}", "Das sind die echten Nullstellen. Gefragt waren alle **Kandidaten**, also alle Teiler von $-4$.")])

# ── 3: Polynomdivision ────────────────────────────────────────────────────
_p_a, _d_a = P.aus_text("x^2 + 5x + 6"), P.aus_text("x + 2")
_p_b, _d_b = P.aus_text("x^3 - 2x^2 - 5x + 6"), P.aus_text("x - 1")
_p_c, _d_c = P.aus_text("x^3 - 7x + 6"), P.aus_text("x - 2")
_p_d, _d_d = P.aus_text("x^2 + 3x + 5"), P.aus_text("x + 1")

k.erklaerung("Polynomdivision", _seite(r"""
    ## Teilen wie in der Grundschule

    Kennst du eine Nullstelle $x_0$, kannst du $p$ durch $(x - x_0)$ teilen. Die
    [[Polynomdivision]] läuft wie schriftliches Teilen, immer mit drei Schritten:

    1. **Teilen:** höchste Potenz durch höchste Potenz.
    2. **Zurückmultiplizieren:** das Ergebnis mal den ganzen Teiler.
    3. **Abziehen:** und mit dem Rest von vorn beginnen.

    Du hörst auf, wenn der Rest einen kleineren Grad hat als der Teiler.

    @A@

    :::alt Mit Zahlen erklärt
    So teilst du $672 : 3$ schriftlich: $6 : 3 = 2$, zurück $2 \cdot 3 = 6$,
    abziehen gibt $0$, die $7$ herunterholen. $7 : 3 = 2$, zurück $6$, Rest $1$,
    die $2$ herunterholen: $12 : 3 = 4$. Ergebnis $224$. Bei Polynomen teilst du
    genauso, nur dass die „Ziffern“ jetzt $x^2$, $x$ und $1$ heißen.
    :::
    ---
    ## Ein Beispiel vom Grad 3

    Weil $1$ eine Nullstelle von $x^3 - 2x^2 - 5x + 6$ ist, geht die Division durch
    $(x - 1)$ ohne Rest auf. Auf Papier schreibst du es so:

    @B@

    :::achtung Vorzeichen beim Abziehen
    Abziehen heißt: **jedes** Vorzeichen in der Klammer umdrehen.
    $(-x^2 - 5x) - (-x^2 + x) = -6x$, nicht $-4x$. Setz die Klammer immer hin.
    :::

    :::alt Als Kontrolle rückwärts
    Teilen ist die Umkehrung von Malnehmen. Prüfe dein Ergebnis darum immer mit
    $(x - 1)(x^2 - x - 6)$. Ausmultipliziert: $x^3 - x^2 - 6x - x^2 + x + 6$,
    zusammengefasst $x^3 - 2x^2 - 5x + 6$. Stimmt. So findest du jeden
    Vorzeichenfehler, bevor er weiterwandert.
    :::
    ---
    ## Lücken füllen

    Fehlt eine Potenz, schreibst du sie mit dem Koeffizienten $0$ hin. Bei
    $x^3 - 7x + 6$ fehlt $x^2$: Du rechnest mit $x^3 + 0x^2 - 7x + 6$. Sonst rutschen
    die Spalten durcheinander. Die Probe $2^3 - 7 \cdot 2 + 6 = 0$ zeigt: $2$ ist
    eine Nullstelle.

    @C@

    :::alt Mit einem Regal erklärt
    Stell dir ein Regal mit beschrifteten Fächern vor: $x^3$, $x^2$, $x$, $1$. Jeder
    Koeffizient kommt in sein Fach. Ist ein Fach leer, bleibt es trotzdem stehen, und
    du legst eine $0$ hinein. Würdest du das Fach weglassen, landet $-7x$ im Fach für
    $x^2$, und die ganze Rechnung stimmt nicht mehr.
    :::
    ---
    ## Division mit Rest

    Ist $x_0$ **keine** Nullstelle, bleibt ein Rest. Dann gilt wie bei Zahlen
    ($7 = 2 \cdot 3 + 1$):

    !! Dividend = Quotient · Teiler + Rest

    @D@

    :::rechnung Probe
    (x + 2)(x + 1) + 3 = x^2 + 3x + 2 + 3 || zurückrechnen
    = x^2 + 3x + 5 || stimmt
    :::

    :::alt Mit Kekspackungen erklärt
    $17$ Kekse in Packungen zu $5$: drei volle Packungen, $2$ Kekse bleiben übrig,
    also $17 = 3 \cdot 5 + 2$. Der Rest ist kleiner als eine Packung, sonst hättest
    du noch eine Packung füllen können. Bei Polynomen heißt „kleiner“: kleinerer Grad.
    Teilst du durch $(x + 1)$ (Grad $1$), ist der Rest eine Zahl (Grad $0$).
    :::
    """, A=_division_markup(_p_a, _d_a, "$(x^2 + 5x + 6) : (x + 2)$"),
    B=_division_markup(_p_b, _d_b, "Die Schritte einzeln"),
    C=_division_markup(_p_c, _d_c, "Die Schritte einzeln"),
    D=_division_markup(_p_d, _d_d, "$(x^2 + 3x + 5) : (x + 1)$")))

_p1, _d1 = P.aus_text("x^2 + 7x + 10"), P.aus_text("x + 2")
k.term("Berechne $(x^2 + 7x + 10) : (x + 2)$.", "x + 5",
       "$x^2 : x = x$, zurück $x^2 + 2x$, abziehen gibt $5x + 10$. Dann $5x : x = 5$, zurück $5x + 10$, Rest $0$.",
       variablen="x", form="ausmultipliziert",
       tipps=["Erster Schritt: $x^2 : x$.", "$x \\cdot (x + 2) = x^2 + 2x$. Zieh das von $x^2 + 7x + 10$ ab.",
              "Es bleibt $5x + 10$. Jetzt $5x : x$."],
       rechenweg=_division_markup(_p1, _d1),
       typische_fehler=[("x + 9", "Beim Abziehen ist ein Vorzeichen gekippt: $7x - 2x = 5x$, nicht $9x$."),
                        ("x - 5", "Vorzeichen: $5x : x = +5$.")])

k.luecke("Vervollständige das Ergebnis der Polynomdivision.",
         "(x^3 + 2x^2 - 5x - 6) : (x - 2) = x^2 + \\luecke \\, x + \\luecke", [[4], [3]],
         "Ergebnis $x^2 + 4x + 3$. Probe: $(x - 2)(x^2 + 4x + 3) = x^3 + 2x^2 - 5x - 6$.",
         tipps=["Erster Schritt: $x^3 : x = x^2$, zurück $x^3 - 2x^2$.",
                "Abziehen: $2x^2 - (-2x^2) = 4x^2$. Also ist der nächste Term $4x$.",
                "Rest nach dem zweiten Schritt: $3x - 6$. Dann $3x : x = 3$."],
         rechenweg=_division_markup(P.aus_text("x^3 + 2x^2 - 5x - 6"), P.aus_text("x - 2")),
         typische_fehler=[([0, -5], "Beim Abziehen: $2x^2 - (-2x^2) = 4x^2$. Minus minus wird plus."),
                          ([-4, 3], "Du hast durch $(x + 2)$ statt $(x - 2)$ geteilt: Das Vorzeichen im Teiler zählt.")])

# ── 4: Linearfaktoren ─────────────────────────────────────────────────────
k.erklaerung("Linearfaktoren und Vielfachheit", r"""
    ## Komplett zerlegen

    Ein Faktor $(x - x_0)$ heißt [[Linearfaktor]]. Ist $x_0$ eine Nullstelle von $p$,
    dann gilt $p(x) = (x - x_0) \cdot q(x)$, und $q$ hat einen Grad weniger. Das
    wiederholst du, bis nur noch Linearfaktoren dastehen. Ab Grad $2$ hilft die
    pq-Formel.

    :::rechnung $x^3 - 2x^2 - 5x + 6$ zerlegen
    (x^3 - 2x^2 - 5x + 6) : (x - 1) = x^2 - x - 6 || Nullstelle $1$ geraten, geteilt
    -\frac{-1}{2} + \sqrt{\frac{1}{4} + 6} = \frac{1}{2} + \frac{5}{2} = 3 || pq-Formel für $x^2 - x - 6$: $x_1 = 3$
    \frac{1}{2} - \frac{5}{2} = -2 || $x_2 = -2$
    x^3 - 2x^2 - 5x + 6 = (x - 1)(x - 3)(x + 2) || alle Linearfaktoren
    :::

    :::alt Wie Primfaktoren
    $12 = 2 \cdot 2 \cdot 3$ zerlegt eine Zahl in Primfaktoren, die man nicht
    weiter zerlegen kann. Linearfaktoren sind die „Primfaktoren“ von Polynomen. Und
    so wie die $2$ in der $12$ doppelt vorkommt, kann auch ein Linearfaktor doppelt
    vorkommen.
    :::
    ---
    ## Doppelte Nullstellen

    Kommt $(x - x_0)$ genau $k$-mal vor, hat $x_0$ die [[Vielfachheit]] $k$. Bei
    einer doppelten Nullstelle berührt der Graph die $x$-Achse nur, statt sie zu
    schneiden.

    :::visual funktionsgraph
    {"funktionen": [{"term": "x^3 - 3*x + 2", "label": "p(x)"}],
     "nullstellen": true, "x": [-3, 3], "y": [-2, 6],
     "unterschrift": "Bei $x = 1$ berührt der Graph die Achse: doppelte Nullstelle."}
    :::

    :::rechnung $x^3 - 3x + 2$ zerlegen
    (x^3 - 3x + 2) : (x - 1) = x^2 + x - 2 || $1^3 - 3 + 2 = 0$: Nullstelle $1$
    x^2 + x - 2 = (x - 1)(x + 2) || Vieta: $1 \cdot (-2) = -2$, $1 + (-2) = -1$
    x^3 - 3x + 2 = (x - 1)^2 (x + 2) || $1$ ist doppelte Nullstelle
    :::

    :::alt Mit einem Ball erklärt
    Ein Ball, der den Boden nur kurz berührt und wieder hochspringt, bleibt auf
    derselben Seite. Das ist eine doppelte Nullstelle: Der Graph kommt von oben, tippt
    die Achse an und geht wieder nach oben. Bei einer einfachen Nullstelle rollt der
    Ball dagegen durch den Boden auf die andere Seite.
    :::
    """)

k.gleichung("x^3 - 2x^2 - 5x + 6 = 0",
            erklaerung="Nullstelle $1$ raten, durch $(x - 1)$ teilen: $x^2 - x - 6$, dessen Nullstellen $3$ und $-2$ sind.",
            tipps=["Probiere die Teiler von $6$: $\\pm 1, \\pm 2, \\pm 3, \\pm 6$.",
                   "$1$ ist eine Nullstelle. Teile durch $(x - 1)$.",
                   "Es bleibt $x^2 - x - 6 = 0$. Löse mit pq-Formel oder Vieta."],
            rechenweg=r"""
            :::rechnung
            1 - 2 - 5 + 6 = 0 || $x = 1$ eingesetzt: Nullstelle
            (x^3 - 2x^2 - 5x + 6) : (x - 1) = x^2 - x - 6 || Polynomdivision
            x^2 - x - 6 = (x - 3)(x + 2) || Vieta: $3 \cdot (-2) = -6$, $3 + (-2) = 1$
            :::

            Also $\mathbb{L} = \{-2; 1; 3\}$.
            """,
            typische_fehler=[("{-1; -3; 2}", "Die Vorzeichen sind vertauscht. Prüfe durch Einsetzen: Bei $x = -1$ kommt $8$ heraus, nicht $0$."),
                             ("{3; -2}", "Die geratene Nullstelle $1$ gehört auch zur Lösungsmenge.")])

k.term("Zerlege $x^3 - 3x^2 - 4x + 12$ vollständig in Linearfaktoren. (Tipp: $2$ ist eine Nullstelle.)",
       "(x - 2)(x - 3)(x + 2)",
       "$(x^3 - 3x^2 - 4x + 12) : (x - 2) = x^2 - x - 6 = (x - 3)(x + 2)$.",
       variablen="x", form="faktorisiert",
       tipps=["Teile durch $(x - 2)$.", "Du erhältst $x^2 - x - 6$.",
              "Vieta: zwei Zahlen mit Produkt $-6$ und Summe $1$."],
       rechenweg=_division_markup(P.aus_text("x^3 - 3x^2 - 4x + 12"), P.aus_text("x - 2")) + r"""

       :::rechnung Rest zerlegen
       x^2 - x - 6 = (x - 3)(x + 2) || Vieta: $3 \cdot (-2) = -6$ und $3 + (-2) = 1$
       x^3 - 3x^2 - 4x + 12 = (x - 2)(x - 3)(x + 2) || alles zusammen
       :::
       """,
       typische_fehler=[("(x + 2)(x + 3)(x - 2)", "Die Vorzeichen sind vertauscht. Zur Nullstelle $3$ gehört $(x - 3)$."),
                        ("(x - 2)(x - 3)(x - 2)", "Die Nullstellen von $x^2 - x - 6$ sind $3$ und $-2$. Zur Nullstelle $-2$ gehört der Faktor $(x + 2)$.")])

# ── 5: Horner-Schema ──────────────────────────────────────────────────────
_h_tab, _ = _horner_markup([2, -3, 0, 5], 2)
k.erklaerung("Das Horner-Schema", _seite(r"""
    ## Schnell einsetzen und nebenbei teilen

    Klammert man geschickt aus, wird aus $2x^3 - 3x^2 + 0x + 5$ der Ausdruck
    $((2x - 3)x + 0)x + 5$. Das [[Horner-Schema]] rechnet genau so: Koeffizient
    herunterschreiben, mal $x_0$, nächsten Koeffizienten addieren, und so weiter.
    Fehlende Potenzen bekommen eine $0$.

    Beispiel $p(x) = 2x^3 - 3x^2 + 5$ an der Stelle $x_0 = 2$:

    @TAB@

    Also $p(2) = 9$. Probe: $16 - 12 + 5 = 9$. Die untere Zeile liefert nebenbei die
    Division: $p(x) = (2x^2 + x + 2)(x - 2) + 9$.

    :::alt Als Programm erklärt
    Im Code ist Horner eine einzige Schleife: Starte mit `w = 0` und rechne für jeden
    Koeffizienten `a` von oben nach unten `w = w * x + a`. Das braucht nur so viele
    Multiplikationen, wie der Grad groß ist. Wer jede Potenz einzeln ausrechnet,
    braucht viel mehr. Darum werten Computer Polynome so aus.
    :::
    """, TAB=_h_tab))

k.zahl("Berechne $p(3)$ mit dem Horner-Schema für $p(x) = x^3 - 4x^2 + x + 6$.",
       P.aus_text("x^3 - 4x^2 + x + 6")(3),
       "Untere Zeile: $1$, $1 \\cdot 3 - 4 = -1$, $-1 \\cdot 3 + 1 = -2$, $-2 \\cdot 3 + 6 = 0$. "
       "Also $p(3) = 0$: $3$ ist sogar eine Nullstelle.",
       tipps=["Koeffizienten: $1$, $-4$, $1$, $6$. Den ersten herunterschreiben.",
              "Dann immer: mal $3$, nächsten Koeffizienten addieren.",
              "$1$, dann $1 \\cdot 3 - 4 = -1$, dann $-1 \\cdot 3 + 1 = -2$, …"],
       rechenweg=_horner_markup([1, -4, 1, 6], 3)[0],
       typische_fehler=[(-60, "Das ist $p(-3)$. Im Horner-Schema rechnest du mit $x_0 = 3$, nicht $-3$."),
                        (72, "Du hast das Minus vor der $4$ verloren. Der Koeffizient ist $-4$: $1 \\cdot 3 + (-4) = -1$.")])


# ── Praxis ────────────────────────────────────────────────────────────────
def polynomdivision(rng):
    r = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
    a = rng.choice([1, 1, 1, 2])
    while True:
        b, c = rng.randint(-6, 6), rng.randint(-6, 6)
        if c != 0:
            break
    quot = P({2: a, 1: b, 0: c})
    d = P({1: 1, 0: -r})
    p = d * quot
    falsch_q, _, _ = p.divmod(P({1: 1, 0: r}))
    fehler = [(falsch_q.term(), "Du hast durch $(x " + ("+" if r > 0 else "-") + f" {abs(r)})$ geteilt. "
                                "Achte auf das Vorzeichen im Teiler.")]
    zweiter = P({2: a, 1: b, 0: -c})
    fehler.append((zweiter.term(), "Beim letzten Abziehen ist ein Vorzeichen gekippt. Prüfe mit Zurückmultiplizieren."))
    loesung = quot.term()
    return {
        "frage": f"Berechne $({p.tex()}) : ({d.tex()})$. Die Division geht ohne Rest auf.",
        "loesung": loesung, "variablen": "x", "form": "ausmultipliziert",
        "tipps": [f"Erster Schritt: ${_glied(a, 3, False)} : x$.",
                  "Teilen, zurückmultiplizieren, abziehen. Dreimal.",
                  f"Das Ergebnis beginnt mit ${_glied(a, 2, False)}$."],
        "rechenweg": _division_markup(p, d),
        "erklaerung": "Teilen, zurückmultiplizieren, abziehen, bis der Rest $0$ ist. Probe durch Ausmultiplizieren.",
        "typische_fehler": _ohne_gleiche_term(loesung, fehler),
    }


k.praxis()

k.generator(polynomdivision, typ="term", titel="Polynomdivision ohne Rest")


def nullstellen_finden(rng):
    r1, r2, r3 = rng.sample([-4, -3, -2, -1, 1, 2, 3, 4], 3)
    p = P({1: 1, 0: -r1}) * P({1: 1, 0: -r2}) * P({1: 1, 0: -r3})
    a0 = p.k.get(0, F(0))
    teiler = [t for t in range(1, abs(int(a0)) + 1) if a0 % t == 0]
    # geraten wird der betragsmäßig kleinste Kandidat, der passt
    kandidaten = sorted([s * t for t in teiler for s in (1, -1)], key=lambda z: (abs(z), -z))
    geraten = next(z for z in kandidaten if p(z) == 0)
    rest = sorted(x for x in (r1, r2, r3) if x != geraten)
    d = P({1: 1, 0: -geraten})
    q, _, zeilen = divisions_zeilen(p, d)
    aufg, zw, wert = _einsetzen(p, geraten)
    s, pr = rest[0] + rest[1], rest[0] * rest[1]
    zeilen = [(f"{aufg} = {zw}", f"Kandidat ${geraten}$ einsetzen"), (f"= {tex(wert)}", "Treffer: Nullstelle")] + zeilen
    zeilen.append((f"{q.tex()} = {_faktor(rest[0])}{_faktor(rest[1])}",
                   f"Vieta: ${tk(rest[0])} \\cdot {tk(rest[1])} = {pr}$ und ${tk(rest[0])} + {tk(rest[1])} = {s}$"))
    alle = sorted([r1, r2, r3])
    loesung = "{" + "; ".join(str(x) for x in alle) + "}"
    fehler = [("{" + "; ".join(str(-x) for x in alle) + "}",
               "Die Vorzeichen sind vertauscht. Zum Faktor $(x - a)$ gehört die Nullstelle $a$, nicht $-a$."),
              ("{" + "; ".join(str(x) for x in rest) + "}",
               f"Die geratene Nullstelle ${geraten}$ gehört auch zur Lösungsmenge.")]
    return {
        "frage": f"Bestimme alle Lösungen von ${p.tex()} = 0$.",
        "loesung": loesung,
        "tipps": [f"Kandidaten sind die Teiler von ${tex(a0)}$, positiv und negativ.",
                  f"Probiere ${geraten}$.",
                  f"Teile durch ${_faktor(geraten)}$ und löse die quadratische Gleichung, die übrig bleibt."],
        "rechenweg": _rechnung(zeilen) + "\n\n" + f"Also $\\mathbb{{L}} = \\{{{'; '.join(str(x) for x in alle)}\\}}$.",
        "erklaerung": "Nullstelle raten (Teiler des Absolutglieds), Polynomdivision, Rest mit pq-Formel oder Vieta lösen.",
        "typische_fehler": _ohne_gleiche_menge(loesung, fehler),
    }


k.generator(nullstellen_finden, typ="loesungsmenge", titel="Nullstellen von Polynomen 3. Grades")


def horner_auswerten(rng):
    while True:
        grad = rng.choice([3, 3, 4])
        koeff = [rng.choice([1, 1, 2, -1, 3, -2])] + [rng.randint(-5, 5) for _ in range(grad)]
        if rng.random() < 0.4:
            koeff[rng.randint(1, grad - 1)] = 0
        x0 = rng.choice([-3, -2, -1, 2, 3] if grad == 3 else [-2, -1, 2])
        p = P({grad - i: c for i, c in enumerate(koeff)})
        wert = p(x0)
        fehler = [(p(-x0), f"Das ist $p({-x0})$. Rechne im Schema mit $x_0 = {x0}$."),
                  (sum(koeff), f"Du hast nur die Koeffizienten addiert. Vor jedem Addieren kommt das Malnehmen mit ${tk(x0)}$.")]
        if 0 in koeff[1:]:
            ohne = [c for i, c in enumerate(koeff) if i == 0 or c != 0]
            fehler.append((_horner(ohne, x0)[-1], "Du hast die fehlende Potenz übersprungen. Für sie gehört eine $0$ ins Schema."))
        if ohne_gleiche(wert, fehler):
            break
    tab, _ = _horner_markup(koeff, x0)
    return {
        "frage": f"Berechne $p({x0})$ für $p(x) = {p.tex()}$ mit dem Horner-Schema.",
        "loesung": wert,
        "tipps": ["Schreibe alle Koeffizienten der Reihe nach auf, fehlende Potenzen mit $0$.",
                  f"Ersten Koeffizienten herunterschreiben, dann immer: mal ${tk(x0)}$, nächsten Koeffizienten addieren.",
                  "Die letzte Zahl der unteren Zeile ist das Ergebnis."],
        "rechenweg": f"Koeffizienten: {', '.join('$' + tex(c) + '$' for c in koeff)}\n\n" + tab,
        "erklaerung": "Horner: $b_n = a_n$, dann $b_{i} = b_{i+1} \\cdot x_0 + a_i$. Die letzte Zahl ist $p(x_0)$.",
        "typische_fehler": ohne_gleiche(wert, fehler),
    }


k.generator(horner_auswerten, typ="zahl", titel="Horner-Schema", glatt=True)

_p_rest = P.aus_text("x^3 + 2x + 5")
k.zahl("Welchen Rest lässt $x^3 + 2x + 5$ bei der Division durch $(x - 1)$?", _p_rest(1),
       "Der Rest bei Division durch $(x - x_0)$ ist $p(x_0)$, hier $p(1) = 1 + 2 + 5 = 8$. "
       "Die Polynomdivision liefert dasselbe.",
       tipps=["Du kannst die Division ausführen oder das Horner-Schema mit $x_0 = 1$ nehmen.",
              "Der Rest ist die letzte Zahl im Horner-Schema, also $p(1)$.",
              "$1^3 + 2 \\cdot 1 + 5$"],
       rechenweg=_division_markup(_p_rest, P.aus_text("x - 1")),
       typische_fehler=[(_p_rest(-1), "Das ist $p(-1)$. Bei Division durch $(x - 1)$ ist $x_0 = +1$."),
                        (0, "Der Rest ist nur $0$, wenn $1$ eine Nullstelle ist. Rechne $p(1)$ aus.")])

_ub = P.aus_text("x^3 - 3x^2 - 4x + 12")
k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: Linearfaktorzerlegung

    Gegeben ist $p(x) = x^3 - 3x^2 - 4x + 12$.

    (a) Zeigen Sie, dass $x_0 = 2$ eine Nullstelle von $p$ ist.
    (b) Führen Sie die Polynomdivision $p(x) : (x - 2)$ durch.
    (c) Geben Sie die vollständige Zerlegung von $p$ in Linearfaktoren an.
    """,
    [{"typ": "zahl", "frage": "(a) Berechne $p(2)$.", "loesung": _ub(2),
      "tipps": ["$2^3 - 3 \\cdot 2^2 - 4 \\cdot 2 + 12$", "$8 - 12 - 8 + 12$"],
      "rechenweg": "$p(2) = 8 - 12 - 8 + 12 = 0$, also ist $2$ eine Nullstelle.",
      "typische_fehler": [(16, "$-4 \\cdot 2 = -8$: Das Minus gehört dazu.")]},
     {"typ": "term", "frage": "(b) Gib das Ergebnis von $p(x) : (x - 2)$ an.", "loesung": "x^2 - x - 6",
      "variablen": "x", "form": "ausmultipliziert",
      "tipps": ["Erster Schritt: $x^3 : x = x^2$, zurück $x^3 - 2x^2$.", "Abziehen: $-3x^2 - (-2x^2) = -x^2$."],
      "rechenweg": _division_markup(_ub, P.aus_text("x - 2")),
      "typische_fehler": [("x^2 - 5x + 6", "Beim Abziehen: $-3x^2 - (-2x^2) = -x^2$, nicht $-5x^2$.")]},
     {"typ": "term", "frage": "(c) Gib $p(x)$ vollständig als Produkt von Linearfaktoren an.",
      "loesung": "(x - 2)(x - 3)(x + 2)", "variablen": "x", "form": "faktorisiert",
      "tipps": ["Zerlege $x^2 - x - 6$ mit Vieta.", "Produkt $-6$, Summe $1$: $3$ und $-2$."],
      "rechenweg": "$p(x) = (x - 2)(x^2 - x - 6) = (x - 2)(x - 3)(x + 2)$",
      "typische_fehler": [("(x - 2)(x + 3)(x - 2)", "Vorzeichen: Die Nullstellen von $x^2 - x - 6$ sind $3$ und $-2$, "
                                                     "also $(x - 3)(x + 2)$.")]}],
    "Probe einsetzen, Polynomdivision, Rest mit Vieta zerlegen. Genau dieses Vorgehen brauchst du später "
    "für charakteristische Polynome in Mathe 1.",
    uebungsblatt=True,
    tipps=["Schritt für Schritt: erst einsetzen, dann teilen, dann zerlegen.", "Am Ende bleibt eine quadratische Gleichung."],
    rechenweg=_seite(r"""
    :::rechnung (a) Nullstelle prüfen
    2^3 - 3 \cdot 2^2 - 4 \cdot 2 + 12 = 8 - 12 - 8 + 12 || einsetzen
    = 0 || also ist $2$ eine Nullstelle
    :::

    (b) Polynomdivision:

    @DIV@

    :::rechnung (c) Zerlegen
    x^2 - x - 6 = (x - 3)(x + 2) || Vieta: $3 \cdot (-2) = -6$, $3 + (-2) = 1$
    x^3 - 3x^2 - 4x + 12 = (x - 2)(x - 3)(x + 2) || zusammensetzen
    :::
    """, DIV=_division_markup(_ub, P.aus_text("x - 2"))))

k.papier(r"""
    ## Beweisen wie in der Übung: Nullstelle und Linearfaktor

    Sei $p$ ein Polynom und $x_0$ eine Zahl mit $p(x_0) = 0$. Zeigen Sie, dass $p$ ohne
    Rest durch $(x - x_0)$ teilbar ist.

    Sie dürfen benutzen: Für jedes Polynom $p$ gibt es Polynome $q$ und $r$ mit
    $p(x) = q(x) \cdot (x - x_0) + r(x)$, wobei der Grad von $r$ kleiner als $1$ ist
    (Division mit Rest).
    """,
    r"""
    **Voraussetzung:** $p(x_0) = 0$.

    **Schritt 1:** Nach der Division mit Rest gilt $p(x) = q(x)(x - x_0) + r(x)$ mit
    $\deg r < 1$. Also ist $r$ eine Konstante, $r(x) = c$ für eine Zahl $c$.

    **Schritt 2:** Setze $x = x_0$ ein:
    $$p(x_0) = q(x_0) \cdot (x_0 - x_0) + c = q(x_0) \cdot 0 + c = c$$

    **Schritt 3:** Nach Voraussetzung ist $p(x_0) = 0$, also $c = 0$.

    **Ergebnis:** $p(x) = q(x)(x - x_0)$. Die Division geht ohne Rest auf. $\square$

    Nebenbei sieht man: Der Rest bei Division durch $(x - x_0)$ ist immer $p(x_0)$.
    """,
    ["Ich habe die Division mit Rest hingeschrieben",
     "Ich habe begründet, warum der Rest eine Konstante ist (Grad kleiner als $1$)",
     "Ich habe $x = x_0$ eingesetzt und $(x_0 - x_0) = 0$ benutzt",
     "Ich habe aus $p(x_0) = 0$ geschlossen, dass der Rest $0$ ist"],
    "Dieser kleine Satz rechtfertigt das ganze Verfahren: Nullstelle raten, dann geht die Division auf.",
    tipps=["Setze in $p(x) = q(x)(x - x_0) + r$ die Zahl $x_0$ ein."])

k.zusammenfassung(r"""
    ## Polynome

    | Begriff | Bedeutung | Beispiel $2x^3 - x + 5$ |
    |---|---|---|
    | Grad | höchste Potenz | $3$ |
    | Leitkoeffizient | Zahl vor der höchsten Potenz | $2$ |
    | Absolutglied | Zahl ohne $x$ | $5$ |

    !! Ist $p(x_0) = 0$, dann ist $p(x) = (x - x_0) \cdot q(x)$, und $q$ hat einen Grad weniger.

    - Nullstellen raten: Teiler des Absolutglieds, **positiv und negativ** (Leitkoeffizient $1$, ganze Koeffizienten).
    - Polynomdivision: teilen, zurückmultiplizieren, abziehen (jedes Vorzeichen umdrehen!), wiederholen.
    - Fehlende Potenzen mit $0$ auffüllen: $x^3 - 7x + 6 = x^3 + 0x^2 - 7x + 6$.
    - Mit Rest: Dividend = Quotient · Teiler + Rest; der Rest bei $(x - x_0)$ ist $p(x_0)$.
    - Horner: herunterschreiben, mal $x_0$, plus nächster Koeffizient. Letzte Zahl $= p(x_0)$.
    - Grad $n$: höchstens $n$ Nullstellen.
""")
