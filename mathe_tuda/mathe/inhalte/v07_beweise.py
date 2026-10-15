# -*- coding: utf-8 -*-
"""Vorkurs 7: Direkter Beweis – Aufbau eines Beweises, Teiler, gerade/ungerade, Gegenbeispiel."""
from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche


def _prim(n):
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


# Behauptungen dieses Kapitels, von Python nachgeprüft
assert all(_prim(n * n + n + 41) for n in range(0, 40)) and 40 * 40 + 40 + 41 == 41 ** 2
assert 10 == 5 * 2 and 42 == 7 * 6 and 33 == 11 * 3 and 91 == 7 * 13
assert 1 + 3 + 5 == 9 and 9 % 2 == 1
for _k in range(-30, 31):
    assert (2 * _k) ** 3 == 2 * (4 * _k ** 3)
    assert (2 * _k + 1) ** 2 == 2 * (2 * _k * _k + 2 * _k) + 1
    for _l in range(-5, 6):
        assert (2 * _k + 1) + (2 * _l + 1) == 2 * (_k + _l + 1)
        assert (2 * _k + 1) * (2 * _l + 1) == 2 * (2 * _k * _l + _k + _l) + 1
    assert _k + (_k + 1) + (_k + 2) == 3 * (_k + 1)

k = neues_kapitel(
    slug="beweise",
    titel="Direkter Beweis",
    beschreibung="Warum Beispiele nicht reichen, wie ein Beweis aufgebaut ist und wie du direkt beweist",
    teil="vorkurs",
    quelle="MVK 2026, VL 3",
    icon="✒️")

k.lernziele([
    "Ich kann erklären, warum Beispiele keine Allaussage beweisen, ein Gegenbeispiel sie aber widerlegt",
    "Ich kann bei einem Satz Voraussetzung und Behauptung benennen",
    "Ich kann mit den Definitionen von gerade, ungerade und Teiler rechnen",
    "Ich kann einen direkten Beweis strukturiert aufschreiben und jeden Schritt begründen",
])

k.warum(r"""
Ein Programm, das bei $1000$ Tests funktioniert, kann beim $1001$. abstürzen.
Wer garantieren will, dass ein Algorithmus **immer** richtig sortiert oder eine
Verschlüsselung **immer** wieder entschlüsselt, braucht einen Beweis. Genau das
macht die Informatik mit Korrektheitsbeweisen und Verifikation. In Mathe 1 sind
in jeder Klausur kurze Beweise dabei, und dort zählt die saubere Struktur.
""")

# ── 1: Warum beweisen ──────────────────────────────────────────────────────
k.erklaerung("Warum Beispiele nicht reichen", r"""
    ## Vierzig Treffer und trotzdem falsch

    :::analogie 🦢 Schwäne
    Du hast tausend weiße Schwäne gesehen. Daraus folgt nicht, dass alle Schwäne
    weiß sind. Ein einziger schwarzer Schwan widerlegt die Behauptung.
    :::

    Behauptung: „Für alle $n \in \mathbb{N}_0$ ist $n^2 + n + 41$ eine Primzahl.“
    Für $n = 0, 1, \ldots, 39$ stimmt das wirklich. Aber:

    :::rechnung Beispiel vorgerechnet
    40^2 + 40 + 41 = 1600 + 40 + 41 || $n = 40$ einsetzen
    = 1681 || addieren
    = 41^2 || keine Primzahl
    :::

    Ein [[Gegenbeispiel]] reicht, um eine Für-alle-Aussage zu widerlegen. Um sie
    zu zeigen, brauchst du einen [[Beweis]], der für **jedes** $n$ funktioniert.

    :::alt Mit Software erklärt
    Tests zeigen nur, dass ein Programm für die getesteten Eingaben läuft. Ein
    Beweis ist wie ein Test für alle unendlich vielen Eingaben auf einmal. Er
    arbeitet nicht mit konkreten Zahlen, sondern mit einem allgemeinen $n$.
    :::
    """)

k.wf("Stimmt eine Aussage über natürliche Zahlen für $n = 1, 2, \\ldots, 1000$, so ist sie für alle $n \\in \\mathbb{N}$ bewiesen.",
     False,
     "Falsch. Beispiele beweisen keine Für-alle-Aussage. $n^2 + n + 41$ ist für $n = 0, \\ldots, 39$ prim, für $n = 40$ aber nicht.",
     tipps=["Denk an $n^2 + n + 41$: Wie lange geht es gut?"])

k.mc("Welches $n$ ist ein Gegenbeispiel zu „Für alle $n \\in \\mathbb{N}$ ist $n^2 + n + 41$ eine Primzahl“?",
     ["$n = 40$", "$n = 1$", "$n = 2$", "Es gibt keins, die Aussage stimmt."],
     "$40^2 + 40 + 41 = 1681 = 41^2$ ist keine Primzahl.",
     tipps=["Ein Gegenbeispiel ist ein $n$, für das das Ergebnis **keine** Primzahl ist.",
            "Probiere eine Zahl, bei der $41$ als Teiler entstehen kann.", "$n^2 + n = n(n+1)$. Für $n = 40$ ist das $40 \\cdot 41$."],
     fehler={"$n = 1$": "$1 + 1 + 41 = 43$ ist eine Primzahl. Das ist ein Beispiel, kein Gegenbeispiel.",
             "$n = 2$": "$4 + 2 + 41 = 47$ ist eine Primzahl. Das bestätigt die Aussage nur für $n = 2$.",
             "Es gibt keins, die Aussage stimmt.": "Viele Beispiele beweisen nichts. Rechne $n = 40$ nach."})

# ── 2: Aufbau ──────────────────────────────────────────────────────────────
k.erklaerung("Aufbau eines Beweises", r"""
    ## Drei Schritte

    1. **Behauptung formulieren:** Was gilt als gegeben ([[Voraussetzung]])?
       Was ist zu zeigen ([[Behauptung]])?
    2. **Beweis durchführen:** eine Kette von Schritten, jeder begründet.
       Markiere, wo die Voraussetzung eingeht.
    3. **Schluss:** Fasse zusammen, was gezeigt ist, und setze $\square$ oder „q.e.d.“.

    Gib jedem Objekt einen Namen und sag, was es ist: „Seien $m, n \in \mathbb{Z}$ gerade.“

    :::rechnung Beispiel: Die Summe zweier gerader Zahlen ist gerade
    2a + 2b = 2(a + b) || Voraussetzung: $m = 2a$, $n = 2b$ mit $a, b \in \mathbb{Z}$; ausklammern
    :::

    Da $a + b \in \mathbb{Z}$ ist, ist $m + n = 2(a + b)$ gerade. $\square$

    :::alt Mit einem Kochrezept erklärt
    Zutaten (Voraussetzung) liegen auf dem Tisch. Das Gericht (Behauptung) steht
    im Titel. Das Rezept führt Schritt für Schritt von den Zutaten zum Gericht.
    Ein Schritt ohne Begründung ist wie „und dann zaubern“.
    :::
    """)

_V_OPT = ["$2$ teilt $n$", "$2$ teilt $n^3$", "$n \\in \\mathbb{N}$ ist gerade und $n^3$ ist gerade", "$n = 2$"]
k.mc("Satz: „Für alle $n \\in \\mathbb{N}$ gilt: Wenn $2$ ein Teiler von $n$ ist, dann ist $2$ ein Teiler von $n^3$.“ "
     "Was ist die Voraussetzung?", _V_OPT,
     "Die Voraussetzung steht nach „wenn“: $2 \\mid n$. Die Behauptung ist $2 \\mid n^3$.",
     tipps=["Die Voraussetzung ist das, was du benutzen darfst.", "Sie steht zwischen „wenn“ und „dann“.",
            "Was steht direkt nach „Wenn“?"],
     fehler={_V_OPT[1]: "Das ist die Behauptung, also das, was gezeigt werden soll.",
             _V_OPT[2]: "Damit hättest du die Behauptung schon vorausgesetzt. Das wäre ein Zirkelschluss.",
             _V_OPT[3]: "$n$ ist beliebig. $n = 2$ wäre nur ein Beispiel."})

# ── 3: Teiler, gerade, ungerade ────────────────────────────────────────────
k.erklaerung("Teiler, gerade und ungerade", r"""
    ## Definitionen sind Werkzeuge

    Seien $n, k \in \mathbb{N}$. $k$ ist ein [[Teiler]] von $n$, wenn es ein
    $m \in \mathbb{N}$ gibt mit $n = k \cdot m$. Man schreibt $k \mid n$
    („$k$ teilt $n$“) und sagt auch: $n$ ist durch $k$ teilbar.

    :::rechnung Beispiele vorgerechnet
    10 = 5 \cdot 2 || also $5 \mid 10$
    42 = 7 \cdot 6 || also $7 \mid 42$
    33 = 11 \cdot 3 || also $33$ ist durch $11$ teilbar
    :::

    Eine ganze Zahl $n$ ist [[gerade|gerade Zahl]], wenn $n = 2k$ für ein $k \in \mathbb{Z}$,
    und ungerade, wenn $n = 2k + 1$ für ein $k \in \mathbb{Z}$.

    :::achtung Aussage, keine Zahl
    $5 \mid 10$ ist eine Aussage (wahr oder falsch), kein Bruch. $\frac{10}{5} = 2$
    ist eine Zahl. Und $k$ steht für eine ganze Zahl, nicht für eine bestimmte.
    :::

    :::alt Mit Schokoriegeln erklärt
    $3 \mid 12$ heißt: $12$ Riegel lassen sich gerecht an $3$ Leute verteilen,
    ohne Rest. Gerade heißt: gerecht an $2$ Leute verteilbar. Ungerade heißt:
    Beim Verteilen an $2$ Leute bleibt genau einer übrig, das ist die $+1$.
    :::
    """)

k.zahl("Zeige $7 \\mid 91$: Gib die Zahl $m \\in \\mathbb{N}$ an, für die $91 = 7 \\cdot m$ gilt.", 13,
       "$91 = 7 \\cdot 13$, also ist $7$ ein Teiler von $91$.",
       tipps=["Gesucht ist $91 : 7$.", "$7 \\cdot 10 = 70$, es fehlen noch $21$.", "$21 = 7 \\cdot 3$"],
       rechenweg=r"""
       :::rechnung
       7 \cdot 13 = 91 || Probe
       :::
       """,
       typische_fehler=[(84, "Du hast $91 - 7$ gerechnet. Gesucht ist $m$ mit $7 \\cdot m = 91$."),
                        (637, "Das ist $7 \\cdot 91$. Gesucht ist die Zahl, die mit $7$ malgenommen $91$ ergibt.")])

k.wf("$0$ ist eine gerade Zahl.", True,
     "Wahr. $0 = 2 \\cdot 0$ und $0 \\in \\mathbb{Z}$. Die Definition ist erfüllt.",
     tipps=["Prüfe die Definition: Gibt es ein $k \\in \\mathbb{Z}$ mit $0 = 2k$?"])

# ── 4: Direkter Beweis ─────────────────────────────────────────────────────
k.erklaerung("Der direkte Beweis", r"""
    ## Von der Voraussetzung zur Behauptung

    :::analogie 🧗 Kletterroute
    Du startest unten (Voraussetzung $A$) und kletterst Griff für Griff nach
    oben (Behauptung $B$). Jeder Griff muss halten.
    :::

    Beim [[direkten Beweis|direkter Beweis]] von $A \Rightarrow B$ baust du eine Kette
    $A \Rightarrow Z_1 \Rightarrow Z_2 \Rightarrow \ldots \Rightarrow B$.

    **Satz.** Für alle $n \in \mathbb{N}$ gilt: $2 \mid n \Rightarrow 2 \mid n^3$.

    **Beweis.** Sei $n \in \mathbb{N}$ mit $2 \mid n$. Dann gibt es ein
    $k \in \mathbb{N}$ mit $n = 2k$. Mit den Potenzgesetzen folgt:

    :::rechnung
    (2k)^3 = 2^3 \cdot k^3 || $n = 2k$ einsetzen, Potenzgesetz
    = 2 \cdot (4k^3) || $2^3 = 2 \cdot 4$
    :::

    Da $k \in \mathbb{N}$, ist auch $4k^3 \in \mathbb{N}$. Also $2 \mid n^3$. $\square$

    :::alt Mit Dominosteinen erklärt
    Jeder Satz im Beweis stößt den nächsten an. Der erste Stein ist die
    Voraussetzung $n = 2k$. Der letzte ist $n^3 = 2 \cdot (\text{etwas Natürliches})$.
    Fehlt ein Stein, bleibt die Kette stehen.
    :::
    """)

k.ordnen("Bringe den Beweis in die richtige Reihenfolge. Satz: Die Summe zweier ungerader Zahlen ist gerade.",
         ["Seien $m, n \\in \\mathbb{Z}$ ungerade.",
          "Dann gibt es $a, b \\in \\mathbb{Z}$ mit $m = 2a + 1$ und $n = 2b + 1$.",
          "Es folgt $m + n = 2a + 1 + 2b + 1 = 2a + 2b + 2$.",
          "Ausklammern ergibt $m + n = 2(a + b + 1)$.",
          "Da $a + b + 1 \\in \\mathbb{Z}$ ist, ist $m + n$ gerade. $\\square$"],
         "Erst die Objekte einführen, dann die Definition anwenden, rechnen und zum Schluss die Definition von „gerade“ wiedererkennen.",
         ablenker=["Seien $m = n = 2k + 1$ mit $k \\in \\mathbb{Z}$.",
                   "Für $m = 3$ und $n = 5$ ist $m + n = 8$ gerade, also stimmt die Aussage."],
         tipps=["Zuerst wird gesagt, worüber der Beweis spricht.",
                "Zwei verschiedene Zahlen brauchen zwei verschiedene Hilfszahlen $a$ und $b$.",
                "Ein Beispiel ist kein Beweis."])

k.luecke("Sei $n = 2k + 1$ mit $k \\in \\mathbb{Z}$. Ergänze so, dass man sieht: $n^2$ ist ungerade.",
         r"n^2 = (2k + 1)^2 = 4k^2 + 4k + 1 = 2 \cdot \left(\luecke\right) + 1", [["2k^2 + 2k"]],
         "Aus $4k^2 + 4k$ wird die $2$ ausgeklammert: $2(2k^2 + 2k)$. Weil $2k^2 + 2k \\in \\mathbb{Z}$, ist $n^2$ ungerade.",
         tipps=["Klammere aus $4k^2 + 4k$ eine $2$ aus.", "$4k^2 = 2 \\cdot 2k^2$ und $4k = 2 \\cdot 2k$.", "$2k^2 + 2k$"],
         rechenweg=r"""
         :::rechnung
         (2k + 1)^2 = 4k^2 + 4k + 1 || binomische Formel
         = 2(2k^2 + 2k) + 1 || $2$ ausklammern
         :::
         """,
         typische_fehler=[(["4k^2 + 4k"], "Du hast die $2$ vor der Klammer nicht herausgerechnet: $2 \\cdot (4k^2 + 4k) = 8k^2 + 8k$."),
                          (["2k^2"], "$(2k + 1)^2$ hat drei Summanden: $4k^2 + 4k + 1$. Der mittlere fehlt.")])

# ── 5: Sauber aufschreiben ─────────────────────────────────────────────────
k.erklaerung("Einen Beweis sauber aufschreiben", r"""
    ## Satz für Satz

    **Satz.** Ist $n \in \mathbb{Z}$ ungerade, so ist auch $n^2$ ungerade.

    **Beweis.** Sei $n \in \mathbb{Z}$ ungerade. Nach Definition gibt es ein
    $k \in \mathbb{Z}$ mit $n = 2k + 1$. Dann gilt:

    :::rechnung
    (2k + 1)^2 = 4k^2 + 4k + 1 || $n = 2k + 1$ einsetzen, binomische Formel
    = 2(2k^2 + 2k) + 1 || $2$ ausklammern
    :::

    Mit $\ell := 2k^2 + 2k \in \mathbb{Z}$ ist $n^2 = 2\ell + 1$, also ungerade. $\square$

    :::achtung Drei typische Fehler
    - Nur Beispiele rechnen: $3^2 = 9$ beweist nichts.
    - Die Behauptung schon benutzen („Da $n^2$ ungerade ist, …“).
    - Zwei Zahlen mit demselben $k$ schreiben: $m = 2k$, $n = 2k$ hieße $m = n$.
    :::

    :::alt Mit einem Gerichtsverfahren erklärt
    Vor Gericht zählt nur, was bewiesen ist. Du darfst Fakten (Voraussetzung)
    und Gesetze (Definitionen, bekannte Regeln) benutzen. Das Urteil
    (Behauptung) darfst du nicht schon vorher als Beweismittel verwenden.
    :::
    """)

_W = ["$\\forall n \\in \\mathbb{N} : n \\text{ gerade} \\Rightarrow n^2 \\text{ gerade}$",
      "$\\sqrt{2}$ ist irrational.",
      "$\\sum_{k=1}^{N} (2k - 1) = N^2$ für alle $N \\in \\mathbb{N}$",
      "$a, b \\in 2\\mathbb{Z} \\Rightarrow a \\cdot b$ gerade",
      "Es gibt unendlich viele Primzahlen."]
_F = ["Die Summe ungerader Zahlen ist gerade.", "Für alle $n \\in \\mathbb{N}$ ist $n^2 + n + 41$ eine Primzahl."]
k.mehrfach("Wahr oder falsch? Kreuze alle **wahren** Aussagen an. (Aussagen aus der Vorkurs-Vorlesung)", _W, _F,
           "Die wahren Aussagen werden im Vorkurs bewiesen (einige erst mit Widerspruch oder Induktion). "
           "Die Summe von **drei** ungeraden Zahlen ist ungerade: $1 + 3 + 5 = 9$. Und $n = 40$ widerlegt die Primzahlformel.",
           tipps=["Suche bei jeder Aussage zuerst ein Gegenbeispiel.", "Probiere bei der Summe ungerader Zahlen drei Summanden.",
                  "$1 + 3 + 5 = 9$"],
           fehler={_F[0]: "Für zwei ungerade Zahlen stimmt es, aber nicht für drei: $1 + 3 + 5 = 9$.",
                   _F[1]: "$n = 40$ ist ein Gegenbeispiel: $1681 = 41^2$."})

# ── 6: Äquivalenz und Gegenbeispiel ────────────────────────────────────────
k.erklaerung("Äquivalenzen und Gegenbeispiele", r"""
    ## Zwei Richtungen

    Eine [[Äquivalenz]] $A \Leftrightarrow B$ zeigst du am einfachsten in zwei
    Teilen: erst $A \Rightarrow B$, dann $B \Rightarrow A$.

    **Satz.** Für $n \in \mathbb{Z}$ gilt: $n$ gerade $\Leftrightarrow$ $n + 1$ ungerade.

    :::rechnung Beide Richtungen
    2k + 1 = 2k + 1 || „$\Rightarrow$“: $n = 2k$, also $n + 1 = 2k + 1$, ungerade
    (2k + 1) - 1 = 2k || „$\Leftarrow$“: $n + 1 = 2k + 1$, also $n = 2k$, gerade
    :::

    Eine Für-alle-Aussage **widerlegst** du mit einem einzigen Gegenbeispiel:
    „Die Summe ungerader Zahlen ist gerade“ ist falsch, denn $1 + 3 + 5 = 9$.

    Kommst du mit einer Methode nicht weiter, probiere eine andere. Eine reicht.

    :::alt Mit einer Brücke erklärt
    Eine Äquivalenz ist eine Brücke mit zwei Fahrspuren. Dass man von $A$ nach
    $B$ kommt, sagt nichts über den Rückweg. Deshalb prüfst du beide Spuren
    einzeln.
    :::
    """)


# ── Praxis ─────────────────────────────────────────────────────────────────
def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


def _poly(koeff, var="k", tex=True):
    """koeff = [(c, e), …] -> c·var^e + …  (LaTeX oder Term-Text)."""
    teile = []
    for c, e in koeff:
        if c == 0:
            continue
        mono = "" if e == 0 else var if e == 1 else f"{var}^{e}"
        zahl = str(abs(c)) if (abs(c) != 1 or e == 0) else ""
        s = zahl + mono
        if not teile:
            teile.append(("-" if c < 0 else "") + s)
        else:
            teile.append((" - " if c < 0 else " + ") + s)
    out = "".join(teile) or "0"
    return out if tex else out.replace(" ", "")


def paritaet_luecke(rng):
    while True:
        a, b, c = rng.choice([0, 1, 1, 2, 3]), rng.randint(-4, 5), rng.randint(-6, 7)
        if a or b:
            break
    p = rng.choice([0, 1])
    n_tex = "2k" if p == 0 else "2k + 1"
    term_tex = _poly([(a, 2), (b, 1), (c, 0)], "n")
    # e(2k + p) = 4a k^2 + (4ap + 2b) k + (a p^2 + b p + c)
    k2, k1, k0 = 4 * a, 4 * a * p + 2 * b, a * p * p + b * p + c
    q, r = divmod(k0, 2)
    innen = [(k2 // 2, 2), (k1 // 2, 1), (q, 0)]
    innen_txt = _poly(innen, tex=False)
    eingesetzt = " + ".join(x for x in [
        f"{'' if a == 1 else a}({n_tex})^2" if a else "",
        f"{b}({n_tex})" if b else "",
        str(c) if c else ""] if x).replace("+ -", "- ")
    fehler = [([[innen_txt], [1 - r]], "Der Rest stimmt nicht. Schau auf die Zahl ohne $k$: Ist sie gerade oder ungerade?")]
    if a and p == 1:
        falsch = _poly([(k2 // 2, 2), ((k1 - 4 * a) // 2, 1), ((a + b + c) // 2, 0)], tex=False)
        fehler.append(([[falsch], [(a + b + c) % 2]],
                       "$(2k + 1)^2 = 4k^2 + 4k + 1$. Der mittlere Summand $4k$ fehlt bei dir."))
    fehler.append(([[_poly([(k2, 2), (k1, 1), (k0 - r, 0)], tex=False)], [r]],
                   "Du hast vergessen, durch $2$ zu teilen: In die Klammer gehört die Hälfte."))
    loesung = [[innen_txt], [r]]
    art = "gerade" if r == 0 else "ungerade"
    return {
        "frage": f"Sei $n \\in \\mathbb{{Z}}$ {'gerade' if p == 0 else 'ungerade'}, also $n = {n_tex}$ mit $k \\in \\mathbb{{Z}}$. "
                 f"Schreibe ${term_tex}$ in der Form $2 \\cdot (\\ldots) + r$ mit $r \\in \\{{0, 1\\}}$.",
        "formel": f"{term_tex} = 2 \\cdot \\left(\\luecke\\right) + \\luecke",
        "antworten": loesung,
        "tipps": [f"Setze $n = {n_tex}$ ein und multipliziere aus.",
                  f"Du erhältst ${_poly([(k2, 2), (k1, 1), (k0, 0)])}$.",
                  f"Die Zahl ohne $k$ ist ${k0} = 2 \\cdot {mathlib.tex_klammer(q)} + {r}$. Klammere aus dem Rest die $2$ aus."],
        "rechenweg": _zeilen((f"{eingesetzt} = {_poly([(k2, 2), (k1, 1), (k0, 0)])}", f"$n = {n_tex}$ eingesetzt, ausmultiplizieren"),
                             (f"= 2\\left({_poly(innen)}\\right) + {r}", "$2$ ausklammern, Rest $0$ oder $1$")),
        "erklaerung": f"Weil die Klammer eine ganze Zahl ist, ist ${term_tex}$ hier {art}.",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


def teiler_zeuge(rng):
    d = rng.randint(3, 13)
    m = rng.randint(4, 19)
    n = d * m
    return {
        "frage": f"Zeige ${d} \\mid {n}$: Gib die Zahl $m \\in \\mathbb{{N}}$ an, für die ${n} = {d} \\cdot m$ gilt.",
        "loesung": m,
        "tipps": [f"Gesucht ist ${n} : {d}$.", f"${d} \\cdot 10 = {d * 10}$.", f"Probe: ${d} \\cdot {m}$"],
        "rechenweg": _zeilen((f"{d} \\cdot {m} = {n}", f"also ${d} \\mid {n}$")),
        "erklaerung": "$k \\mid n$ heißt: Es gibt ein $m \\in \\mathbb{N}$ mit $n = k \\cdot m$. Dieses $m$ ist der Beleg.",
        "typische_fehler": ohne_gleiche(m, [(n - d, f"Du hast ${n} - {d}$ gerechnet. Gesucht ist $m$ mit ${d} \\cdot m = {n}$."),
                                            (n * d, f"Das ist ${n} \\cdot {d}$. Gesucht ist ${n} : {d}$.")]),
    }


k.praxis()

k.generator(teiler_zeuge, typ="zahl", titel="Teiler belegen", glatt=True)
k.generator(paritaet_luecke, typ="luecke", titel="Gerade oder ungerade?")

k.ordnen("Bringe den Beweis in die richtige Reihenfolge. Satz: Die Summe von drei aufeinanderfolgenden ganzen Zahlen ist durch $3$ teilbar.",
         ["Sei $n \\in \\mathbb{Z}$. Die drei aufeinanderfolgenden Zahlen sind $n$, $n + 1$ und $n + 2$.",
          "Ihre Summe ist $n + (n + 1) + (n + 2) = 3n + 3$.",
          "Ausklammern ergibt $3n + 3 = 3(n + 1)$.",
          "Da $n + 1 \\in \\mathbb{Z}$ ist, ist die Summe ein Vielfaches von $3$. $\\square$"],
         "Erst die Zahlen allgemein benennen, dann rechnen, dann die Teilbarkeit ablesen.",
         ablenker=["Es gilt $1 + 2 + 3 = 6 = 3 \\cdot 2$, also ist die Summe durch $3$ teilbar.",
                   "Seien $n$, $m$ und $\\ell$ drei beliebige ganze Zahlen."],
         tipps=["„Aufeinanderfolgend“ heißt: Jede Zahl ist um $1$ größer als die vorige.",
                "Ein konkretes Beispiel ist kein Beweis."])

k.papier(r"""
    ## Übungsblatt-Stil: Direkte Beweise

    Beweisen Sie direkt. Geben Sie bei jedem Schritt die Begründung an.

    a) Für alle $n \in \mathbb{N}$ gilt: Ist $n$ gerade, so ist auch $n^2$ gerade.

    b) Das Produkt zweier ungerader ganzer Zahlen ist ungerade.

    c) Widerlegen Sie: „Für alle $a, b \in \mathbb{N}$ gilt: Ist $a + b$ gerade, so sind $a$ und $b$ gerade.“
    """,
    r"""
    **a)** Sei $n \in \mathbb{N}$ gerade. Dann gibt es $k \in \mathbb{N}$ mit $n = 2k$.

    :::rechnung
    (2k)^2 = 4k^2 || $n = 2k$ eingesetzt, Potenzgesetz
    = 2 \cdot (2k^2) || $4 = 2 \cdot 2$
    :::

    Da $2k^2 \in \mathbb{N}$, ist $n^2$ gerade. $\square$

    **b)** Seien $m, n \in \mathbb{Z}$ ungerade. Dann gibt es $a, b \in \mathbb{Z}$
    mit $m = 2a + 1$ und $n = 2b + 1$ (zwei **verschiedene** Hilfszahlen).

    :::rechnung
    (2a + 1)(2b + 1) = 4ab + 2a + 2b + 1 || ausmultiplizieren
    = 2(2ab + a + b) + 1 || $2$ ausklammern
    :::

    Da $2ab + a + b \in \mathbb{Z}$, ist $m \cdot n$ ungerade. $\square$

    **c)** Gegenbeispiel: $a = 1$, $b = 3$. Dann ist $a + b = 4$ gerade, aber $a$
    und $b$ sind ungerade. Also ist die Aussage falsch.
    """,
    ["a) Ich habe mit „Sei $n$ gerade“ begonnen und $n = 2k$ mit $k \\in \\mathbb{N}$ benutzt",
     "a) Ich habe $n^2 = 2 \\cdot (2k^2)$ gezeigt und gesagt, warum $2k^2 \\in \\mathbb{N}$ ist",
     "b) Ich habe zwei verschiedene Hilfszahlen $a$ und $b$ verwendet",
     "b) Ich habe $mn = 2(2ab + a + b) + 1$ hergeleitet",
     "c) Ich habe ein konkretes Gegenbeispiel angegeben und geprüft"],
    "Ein direkter Beweis setzt die Definition ein, rechnet und erkennt am Ende wieder eine Definition. "
    "Eine Für-alle-Aussage fällt mit einem einzigen Gegenbeispiel.",
    uebungsblatt=True,
    tipps=["Schreibe zuerst auf, was „gerade“ bzw. „ungerade“ nach Definition bedeutet."])

k.zusammenfassung(r"""
    ## Direkter Beweis

    | Begriff | Bedeutung |
    |---|---|
    | Voraussetzung | was gegeben ist, darf benutzt werden |
    | Behauptung | was zu zeigen ist, darf nicht benutzt werden |
    | $k \mid n$ | es gibt $m \in \mathbb{N}$ mit $n = k \cdot m$ |
    | $n$ gerade / ungerade | $n = 2k$ bzw. $n = 2k + 1$ mit $k \in \mathbb{Z}$ |
    | direkter Beweis | $A \Rightarrow Z_1 \Rightarrow \ldots \Rightarrow B$, jeder Schritt begründet |
    | Gegenbeispiel | ein Fall, der eine Für-alle-Aussage widerlegt |

    !! Beispiele beweisen keine Für-alle-Aussage. Ein Gegenbeispiel widerlegt sie.

    - Aufbau: Behauptung formulieren, Beweis mit Begründungen, Schluss mit $\square$.
    - Objekte benennen („Sei $n \in \mathbb{Z}$ …“), verschiedene Zahlen bekommen verschiedene Hilfsvariablen.
    - Äquivalenz: beide Richtungen einzeln zeigen.
""")
