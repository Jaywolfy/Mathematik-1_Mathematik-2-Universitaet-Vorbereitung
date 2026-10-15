# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 14: Die ganzen Zahlen (Skript Disser WS 26/27, Abschn. 3.1, Def. 3.1 bis 3.6, Beob. 3.4)."""
from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(
    slug="ganze_zahlen",
    titel="Die ganzen Zahlen",
    beschreibung="ℤ als Paare natürlicher Zahlen modulo Differenz, Addition, Subtraktion, Multiplikation, Vorzeichenregeln, div und mod auf ℤ",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 3.1",
    icon="➖")


# ── Python rechnet mit Paaren (a, b) ∈ ℕ² ───────────────────────────────
def gleich_paar(p, q):
    """(a, b) ~ (c, d) genau dann, wenn a + d = b + c (Def. 3.1)."""
    return p[0] + q[1] == p[1] + q[0]


def paar_wert(p):
    return p[0] - p[1]


def padd(p, q):
    return (p[0] + q[0], p[1] + q[1])


def pmul(p, q):
    return (p[0] * q[0] + p[1] * q[1], p[0] * q[1] + p[1] * q[0])


def pneg(p):
    return (p[1], p[0])


def pt(p):
    return f"({p[0]}, {p[1]})"


def klasse(p):
    return f"[{pt(p)}]"


def rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


# Definition 3.1 und Beobachtung 3.4 nachrechnen
assert gleich_paar((5, 8), (0, 3)) and not gleich_paar((5, 8), (3, 0))
assert paar_wert(padd((5, 8), (7, 2))) == 2 and paar_wert(pmul((0, 3), (0, 2))) == 6
for _a in range(6):
    for _b in range(6):
        for _c in range(6):
            for _d in range(6):
                _p, _q = (_a, _b), (_c, _d)
                assert paar_wert(padd(_p, _q)) == paar_wert(_p) + paar_wert(_q)
                assert paar_wert(pmul(_p, _q)) == paar_wert(_p) * paar_wert(_q)
                assert paar_wert(padd(_p, pneg(_q))) == paar_wert(_p) - paar_wert(_q)
                # unabhängig vom Repräsentanten: (a+1, b+1) ~ (a, b)
                assert gleich_paar(padd(_p, (1, 1)), _p)
                assert gleich_paar(padd(padd(_p, (1, 1)), _q), padd(_p, _q))
                assert gleich_paar(pmul(padd(_p, (1, 1)), _q), pmul(_p, _q))
# div und mod auf ℤ (Def. 3.6 iii)
assert (-7) // 3 == -3 and (-7) % 3 == 2 and (-7) == (-3) * 3 + 2

k.lernziele([
    "Ich kann erklären, warum $\\mathbb{N}$ nicht reicht und wie $\\mathbb{Z} := \\mathbb{N}^2/{\\sim}$ aus Paaren gleicher Differenz entsteht (Def. 3.1)",
    "Ich kann prüfen, ob zwei Paare dieselbe ganze Zahl beschreiben, und zu jedem Paar die Zahl $a$ oder $-a$ angeben",
    "Ich kann Addition, Subtraktion und Multiplikation auf Paaren ausführen und die Vorzeichenregeln begründen (Def. 3.2, 3.3, 3.5, Beob. 3.4)",
    "Ich kann $z \\operatorname{div} n$ und $z \\bmod n$ für negative $z$ bestimmen (Def. 3.6)",
])

k.warum(r"""
Computer kennen beide Seiten dieser Konstruktion: Ein Zähler, der von 8 auf 5 fällt, hat die Änderung $-3$.
Ein Paar aus „Zuwachs“ und „Abnahme“ ist genau die Idee hinter Vorzeichen-Betrag-Darstellungen und
Differenzcodierungen. Dass $-7 \bmod 3$ in Python $2$ ergibt, in manchen anderen Sprachen $-1$, hängt direkt an
Definition 3.6: Der Rest ist immer eine natürliche Zahl. Und das Wort „wohldefiniert“, das hier zum ersten Mal ernsthaft
auftritt, begegnet dir wieder bei Restklassen, Brüchen und Hashing.
""")

# ── Seite 1: Motivation ──────────────────────────────────────────────────
k.erklaerung("Warum ℕ nicht reicht", r"""
## Änderungen eines Bestands

:::analogie 🔋 Akkustand
Dein Akku zeigt $8\,\%$, später $5\,\%$. Die Änderung ist $5 - 8$. Eine Zahl $x$ mit $8 + x = 5$ gibt es in
[[ℕ|natürliche Zahl]] nicht, denn $8 + x \ge 8$.
:::

Die Subtraktion auf $\mathbb{N}$ (Def. 2.24) ist nur **teilweise** definiert: $b - a$ gibt es nur für $a \le b$.
Wir suchen deshalb eine größere Menge $\mathbb{Z}$, in der jede Gleichung $a + x = b$ lösbar ist.

Die Idee des Skripts: Eine Änderung beschreibst du durch ein Paar $(a, b) \in \mathbb{N}^2$ („erst $a$ dazu, dann $b$ weg“).
Die Subtraktion selbst wird dabei **vermieden**, denn sie ist ja gerade das Problem.

:::visual zahlenstrahl
{"von": 0, "bis": 10, "schritt": 1, "pfeile": [{"von": 8, "bis": 5, "label": "x = ?"}],
 "punkte": [{"x": 8, "label": "8"}, {"x": 5, "label": "5", "farbe": "orange"}],
 "unterschrift": "Von $8$ nach $5$ geht der Pfeil nach links. In $\\mathbb{N}$ gibt es dafür keine Zahl."}
:::

:::alt Als Schuldenbuch
Auf deinem Konto sind $5$ Euro, du sollst $8$ zahlen. Das Buch notiert zwei Spalten: Einnahmen $5$, Ausgaben $8$.
Du brauchst kein Minuszeichen, nur zwei natürliche Zahlen nebeneinander. Das ist das Paar $(5, 8)$.
:::
""")

k.mc("Warum hat die Gleichung $8 + x = 5$ keine Lösung in $\\mathbb{N}$?",
     ["Weil $8 + x \\ge 8 > 5$ für jedes $x \\in \\mathbb{N}$ gilt, also kann nie $5$ herauskommen",
      "Weil $5$ keine natürliche Zahl ist",
      "Weil die Addition auf $\\mathbb{N}$ nicht kommutativ ist",
      "Weil $8 - 5$ nicht definiert ist"],
     "Auf $\\mathbb{N}$ wird beim Addieren nie etwas kleiner. Die Differenz $b - a$ aus Definition 2.24 existiert nur für $a \\le b$; hier wäre es $5 - 8$.",
     tipps=["Setze kleine Werte für $x$ ein: $x = 0, 1, 2$. Was passiert mit der Summe?",
            "Natürliche Zahlen sind $\\ge 0$. Wie klein kann $8 + x$ werden?"],
     fehler={"Weil $5$ keine natürliche Zahl ist": "$5 \\in \\mathbb{N}$. Das Problem ist die Gleichung, nicht die Zahl $5$.",
             "Weil die Addition auf $\\mathbb{N}$ nicht kommutativ ist": "Die Addition auf $\\mathbb{N}$ ist kommutativ. Das ist nicht der Grund.",
             "Weil $8 - 5$ nicht definiert ist": "$8 - 5 = 3$ ist in $\\mathbb{N}$ definiert. Hier wäre $5 - 8$ nötig, und das fehlt."})

# ── Seite 2: Definition 3.1 ──────────────────────────────────────────────
k.erklaerung("Definition 3.1: Paare gleicher Differenz", r"""
## ℤ := ℕ² / ∼

**Definition 3.1.** Zwei Paare $(a, b), (c, d) \in \mathbb{N}^2$ heißen gleichwertig, $(a, b) \sim (c, d)$, wenn

$$a + d = b + c.$$

Das ist eine [[Äquivalenzrelation]] (Kap. „Äquivalenzrelationen“). Die [[Faktormenge]] $\mathbb{Z} := \mathbb{N}^2/{\sim}$
ist die Menge der [[ganzen Zahlen|ganze Zahl]]. Eine Klasse schreibst du $[(a, b)]$.

Warum so? $a - b = c - d$ ist äquivalent zu $a + d = c + b$, aber die zweite Form kommt ohne Subtraktion aus.

:::rechnung Sind $(5, 8)$ und $(0, 3)$ gleichwertig?
5 + 3 = 8 + 0 || $a + d$ mit $(a, b) = (5, 8)$ und $(c, d) = (0, 3)$ gegen $b + c$
8 = 8 || beide Seiten sind $8$: also $(5, 8) \sim (0, 3)$
:::

Zum Vergleich $(5, 8)$ und $(3, 0)$: $a + d = 5 + 0 = 5$, aber $b + c = 8 + 3 = 11$. Nicht gleichwertig.

:::achtung Tauschen geht nicht
$(a, b)$ und $(b, a)$ sind **nicht** gleichwertig (außer bei $a = b$). Es kommt auf die Reihenfolge an: $(5, 8)$ ist $-3$, $(8, 5)$ ist $+3$.
:::

:::alt Als Waage
Lege auf die linke Schale $a$ und $d$, auf die rechte $b$ und $c$. Sind beide Seiten gleich schwer, beschreiben
$(a, b)$ und $(c, d)$ denselben Unterschied. Verschiebst du beide Zahlen eines Paars um denselben Betrag, ändert sich der
Unterschied nicht: $(5, 8) \sim (6, 9) \sim (0, 3)$.
:::
""")

k.wf("Es gilt $(2, 5) \\sim (4, 7)$.", True,
     "Prüfe $a + d = b + c$: $2 + 7 = 9$ und $5 + 4 = 9$. Beide Paare beschreiben $-3$.",
     tipps=["Setze $a = 2$, $b = 5$, $c = 4$, $d = 7$ in $a + d = b + c$ ein."])

k.mehrfach("Welche Paare sind gleichwertig zu $(0, 3)$, beschreiben also $-3$?",
           ["$(5, 8)$", "$(2, 5)$", "$(10, 13)$"],
           ["$(3, 0)$", "$(3, 7)$", "$(0, 0)$"],
           "Bei $(c, d) = (0, 3)$ lautet die Bedingung $a + 3 = b + 0$, also $b = a + 3$. Das erfüllen $(5, 8)$, $(2, 5)$, $(10, 13)$. "
           "Bei $(3, 0)$ wäre $b = a - 3$ nötig, $(3, 7)$ hat $7 \\ne 6$ und $(0, 0)$ hat $0 \\ne 3$.",
           tipps=["Die Bedingung ist $a + 3 = b$.", "Die zweite Zahl muss genau $3$ größer sein als die erste."],
           fehler={"$(3, 0)$": "Hier ist $a + 3 = 6 \\ne 0 = b$. $(3, 0)$ ist $+3$, nicht $-3$.",
                   "$(3, 7)$": "$3 + 3 = 6 \\ne 7$: Die Differenz ist $-4$.",
                   "$(0, 0)$": "$(0, 0)$ ist die Null, $0 + 3 \\ne 0$."})

# ── Seite 3: Standardvertreter ───────────────────────────────────────────
k.erklaerung("Jede Klasse hat einen einfachen Vertreter", r"""
## a = [(a, 0)] und −a = [(0, a)]

Das Skript identifiziert für $a \in \mathbb{N}$:
$$a = [(a, 0)], \qquad -a = [(0, a)].$$

Jede Klasse enthält ein Paar, in dem eine Seite $0$ ist: Von $(a, b)$ ziehst du auf beiden Seiten $\min(a, b)$ ab.
So entsteht die vertraute Form
$$\mathbb{Z} = \{\ldots, -3, -2, -1, 0, 1, 2, 3, \ldots\}.$$

:::rechnung Welche Zahl ist $[(9, 4)]$, welche $[(2, 7)]$?
9 - 4 = 5 || beide Seiten um $4$ kleiner: $(9, 4) \sim (5, 0)$, also die Zahl $5$
2 - 2 = 0 || beide Seiten um $2$ kleiner: $(2, 7) \sim (0, 5)$
7 - 2 = 5 || die Klasse $[(0, 5)]$ ist $-5$
:::

Dass die Zahl $a \in \mathbb{N}$ mit $[(a, 0)]$ identifiziert wird, heißt: $\mathbb{N}$ steckt in $\mathbb{Z}$, ohne dass sich etwas an der Rechnung ändert.

:::alt Als Kontostand
Zwei Spalten „Haben“ und „Soll“. Ein Konto mit Haben $9$ und Soll $4$ hat denselben Stand wie eines mit Haben $5$ und Soll $0$.
Du kürzt beide Spalten um den kleineren Wert, bis eine Spalte leer ist. Ist Haben leer, liegt der Stand im Minus.
:::
""")


def ganze_paar_wert(rng):
    a, b = rng.randint(1, 12), rng.randint(1, 12)
    if a == b:
        b += rng.randint(1, 4)
    w = a - b
    return {"frage": f"Welche ganze Zahl beschreibt die Klasse $[({a}, {b})] \\in \\mathbb{{Z}}$? (Eingabe mit Vorzeichen, zum Beispiel `-3`.)",
            "loesung": w,
            "tipps": ["Ziehe von beiden Zahlen des Paars dieselbe Zahl ab, bis eine davon $0$ ist.",
                      f"Der kleinere Eintrag ist ${min(a, b)}$. Ziehe ihn von beiden ab.",
                      f"Es bleibt $({a - min(a, b)}, {b - min(a, b)})$. Steht die Zahl links, ist sie positiv, steht sie rechts, negativ."],
            "rechenweg": rechnung([(f"({a}, {b}) \\sim ({a - min(a, b)}, {b - min(a, b)})", f"beide Seiten um ${min(a, b)}$ kleiner: $a + d = b + c$ bleibt wahr"),
                                   (f"{a} - {b} = {w}", "Steht die Zahl links, ist sie positiv, rechts negativ")]),
            "erklaerung": "$[(a, b)]$ ist $a - b$, auch wenn das Skript die Subtraktion vermeidet. Die Zahl steht links: positiv, rechts: negativ.",
            "typische_fehler": ohne_gleiche(w, [(-w, "Vorzeichen vertauscht: $(a, b)$ ist $a - b$, die **erste** Zahl ist der positive Anteil."),
                                                 (a + b, "Du hast addiert. Die beiden Einträge wirken gegeneinander, du musst subtrahieren.")])}


k.generator(ganze_paar_wert, typ="zahl", titel="Welche ganze Zahl beschreibt das Paar?")

# ── Seite 4: Addition und Subtraktion ────────────────────────────────────
k.erklaerung("Addition und Subtraktion", r"""
## Definition 3.2, Definition 3.3, Beobachtung 3.4

**Definition 3.2.** $[(a, b)] + [(c, d)] := [(a + c,\ b + d)]$. Du addierst komplett getrennt „Zuwächse“ und „Abnahmen“.

Die Summe hängt nicht vom gewählten [[Repräsentanten|Repräsentant]] ab (sie ist [[wohldefiniert]]) und setzt die Addition von $\mathbb{N}$ fort.

**Definition 3.3.** Die Subtraktion ist $b - a := T_a^{-1}(b)$ mit der Bijektion $T_a\colon \mathbb{Z} \to \mathbb{Z},\ x \mapsto x + a$.
Das ist genau die eindeutige Lösung von $a + x = b$ (Satz 3.7).

**Beobachtung 3.4.** $-[(c, d)] = [(d, c)]$ und $b - a = b + (-a)$. Subtrahieren heißt: das Paar umdrehen und addieren.

:::rechnung $[(5, 8)] + [(7, 2)]$ und $[(5, 8)] - [(7, 2)]$
(5 + 7,\ 8 + 2) = (12, 10) || Addition komponentenweise
12 - 10 = 2 || die Zahl: $-3 + 5 = 2$
(5 + 2,\ 8 + 7) = (7, 15) || Subtraktion: $[(7, 2)]$ umdrehen zu $[(2, 7)]$, dann addieren
7 - 15 = -8 || die Zahl: $-3 - 5 = -8$
:::

:::alt Als Tagebuch
Zwei Tage, zwei Einträge „Zuwachs / Abnahme“. Zusammen: alle Zuwächse addieren, alle Abnahmen addieren. Rückgängig machen
heißt: Zuwachs und Abnahme tauschen. Daher $-[(c, d)] = [(d, c)]$.
:::
""")

k.zahl("Rechne mit den Repräsentanten: $[(4, 9)] + [(6, 1)] = [(a, b)]$. Welche ganze Zahl ist das Ergebnis? (Eingabe mit Vorzeichen.)",
       paar_wert(padd((4, 9), (6, 1))),
       "Addiere komponentenweise: $(4 + 6, 9 + 1) = (10, 10)$. Das ist $10 - 10 = 0$. Zur Probe: $-5 + 5 = 0$.",
       tipps=["Addiere die ersten Einträge und die zweiten Einträge getrennt.", "$(4 + 6, 9 + 1)$.", "Die Zahl ist erster Eintrag minus zweiter Eintrag."],
       rechenweg=rechnung([("(4 + 6,\\ 9 + 1) = (10, 10)", "Definition 3.2"), ("10 - 10 = 0", "beide Seiten gleich: die Zahl $0$")]),
       typische_fehler=[(10, "Du hast nur die ersten Einträge addiert. Auch die zweiten ($9 + 1 = 10$) gehören dazu, und die Differenz ist dann $0$.")])


def ganze_paar_rechnen(rng):
    op = rng.choice(["+", "-", "*"])
    while True:
        p = (rng.randint(0, 8), rng.randint(0, 8))
        q = (rng.randint(0, 8), rng.randint(0, 8))
        if paar_wert(p) != 0 and paar_wert(q) != 0 and paar_wert(p) != paar_wert(q) and \
                (op != "*" or abs(paar_wert(p)) != 1 and abs(paar_wert(q)) != 1) and \
                paar_wert(padd(p, q if op == "+" else pneg(q) if op == "-" else (0, 0))) != 0:
            break
    if op == "+":
        r, name = padd(p, q), "Addition"
        formel = f"({p[0]} + {q[0]},\\ {p[1]} + {q[1]})"
        regel = "Definition 3.2: komponentenweise addieren"
        symbol = "+"
    elif op == "-":
        r, name = padd(p, pneg(q)), "Subtraktion"
        formel = f"({p[0]} + {q[1]},\\ {p[1]} + {q[0]})"
        regel = "Beobachtung 3.4: zweites Paar umdrehen und addieren"
        symbol = "-"
    else:
        r, name = pmul(p, q), "Multiplikation"
        formel = f"({p[0]} \\cdot {q[0]} + {p[1]} \\cdot {q[1]},\\ {p[0]} \\cdot {q[1]} + {p[1]} \\cdot {q[0]})"
        regel = "Definition 3.5: $(ac + bd,\\ ad + bc)$"
        symbol = "\\cdot"
    w = paar_wert(r)
    falsch = []
    if op == "*":
        falsch.append((paar_wert((p[0] * q[0], p[1] * q[1])), "Du hast komponentenweise multipliziert. Das ist nicht Definition 3.5: Es gilt $(ac + bd,\\ ad + bc)$."))
    if op == "+":
        falsch.append((paar_wert(p) - paar_wert(q), "Das ist $x - y$. Bei der Addition werden beide Klassen addiert."))
    if op == "-":
        falsch.append((paar_wert(p) + paar_wert(q), "Das ist die Summe. Bei der Subtraktion musst du das zweite Paar vorher umdrehen."))
    falsch.append((-w, "Vorzeichen vertauscht: Die erste Zahl eines Paars ist der positive Anteil."))
    return {"frage": f"Berechne die {name} $[{pt(p)}] {symbol} [{pt(q)}]$ mit den Regeln aus Abschnitt 3.1 und gib die entstehende ganze Zahl an. (Eingabe mit Vorzeichen.)",
            "loesung": w,
            "tipps": [f"Welche Definition passt zur {name}? ({regel})",
                      f"Das Ergebnispaar ist ${formel}$.",
                      f"Das Paar ist ${pt(r)}$. Die Zahl ist erster Eintrag minus zweiter Eintrag."],
            "rechenweg": rechnung([(f"{formel} = {pt(r)}", regel), (f"{r[0]} - {r[1]} = {w}", "erster minus zweiter Eintrag")]),
            "erklaerung": f"Kontrolle mit den Zahlen: ${paar_wert(p)} {symbol} ({paar_wert(q)}) = {w}$.",
            "typische_fehler": ohne_gleiche(w, falsch)}


k.generator(ganze_paar_rechnen, typ="zahl", titel="Mit Paaren rechnen: Addition, Subtraktion, Multiplikation")

# ── Seite 5: Satz 3.7 ───────────────────────────────────────────────────
k.erklaerung("Satz 3.7: a + x = b ist eindeutig lösbar", r"""
## Der Anlass

**Satz 3.7.** Für alle $a, b \in \mathbb{Z}$ hat $a + x = b$ genau eine Lösung $x \in \mathbb{Z}$, nämlich $x = b - a$.

*Beweis.* **Existenz:** $x = (-a) + b$ löst die Gleichung. **Eindeutigkeit:** Ist $y$ eine weitere Lösung, so folgt
$y = 0 + y = ((-a) + a) + y = (-a) + (a + y) = (-a) + b = x$. $\square$

Benutzt wurden nur drei Eigenschaften der Addition: Assoziativität, die Null und das Gegenelement $-a$.
Genau diese drei Eigenschaften greifst du in Kapitel „Gruppen“ heraus.

:::rechnung Der Beweis an $a = 8$, $b = 5$
8 + (-8 + 5) = (8 + (-8)) + 5 || Assoziativität
(8 + (-8)) + 5 = 0 + 5 = 5 || Gegenelement, dann Null
x = -8 + 5 = -3 || die Lösung $x = (-a) + b$
:::

:::alt Als Rückwärtsgang
Eine Gleichung $a + x = b$ fragt: „Was muss ich zu $a$ addieren, um $b$ zu erreichen?“ Du addierst $-a$ auf beiden Seiten.
Dass das **genau eine** Antwort liefert, liegt daran, dass „$+(-a)$“ den Schritt „$+a$“ rückgängig macht.
:::
""")

k.ordnen("Ordne den Beweis von Satz 3.7 (Existenz und Eindeutigkeit von $a + x = b$).",
         ["Setze $x := (-a) + b$.",
          "Dann ist $a + x = a + ((-a) + b) = (a + (-a)) + b = 0 + b = b$, also löst $x$ die Gleichung.",
          "Sei $y \\in \\mathbb{Z}$ eine weitere Lösung, also $a + y = b$.",
          "Dann gilt $y = 0 + y = ((-a) + a) + y = (-a) + (a + y) = (-a) + b = x$.",
          "Also ist die Lösung eindeutig. $\\square$"],
         "Zuerst wird eine Lösung angegeben (Existenz), dann gezeigt, dass jede andere gleich ist (Eindeutigkeit). Benutzt: Assoziativität, $0$ und $-a$.",
         ablenker=["Da $\\mathbb{Z}$ unendlich ist, gibt es mehrere Lösungen.", "Dann gilt $y = x$, weil beide Zahlen gleich aussehen."],
         tipps=["Existenz zuerst: Eine Lösung angeben und einsetzen.", "Eindeutigkeit: Eine **beliebige** zweite Lösung $y$ annehmen und $y = x$ zeigen.",
                "Zum Umformen von $y$ benutzt du $0 + y$, dann $(-a) + a = 0$."])

# ── Seite 6: Multiplikation ─────────────────────────────────────────────
k.erklaerung("Multiplikation und Vorzeichenregeln", r"""
## Definition 3.5

Multiplizieren mit $n \in \mathbb{N}$ heißt: dieselbe Änderung $n$-mal ausführen. Mit $-n$: die **entgegengesetzte**
Änderung $n$-mal ausführen.

**Definition 3.5.** $[(a, b)] \cdot [(c, d)] := [(ac + bd,\ ad + bc)]$.

Das setzt die Multiplikation auf $\mathbb{N}$ fort: $[(a, 0)] \cdot [(c, 0)] = [(ac + 0,\ 0 + 0)] = [(ac, 0)]$.

Die [[Vorzeichenregeln]] stehen schon im Skript: Für $z = [(a, b)]$ und $q = [(c, d)]$ ist $(-z)q = -(zq)$ und $(-z)(-q) = zq$.

:::rechnung $(-3) \cdot (-2)$ mit $-3 = [(0, 3)]$ und $-2 = [(0, 2)]$
0 \cdot 0 + 3 \cdot 2 = 6 || erster Eintrag: $ac + bd$ mit $(a, b) = (0, 3)$, $(c, d) = (0, 2)$
0 \cdot 2 + 3 \cdot 0 = 0 || zweiter Eintrag: $ad + bc$
6 - 0 = 6 || das Paar $(6, 0)$ ist die Zahl $6$
:::

:::achtung Nicht komponentenweise
$[(a, b)] \cdot [(c, d)]$ ist **nicht** $[(ac, bd)]$. Teste mit $(0, 3) \cdot (0, 2)$: komponentenweise gäbe $(0, 6) = -6$, richtig ist $+6$.
:::

:::alt Als Richtung und Wiederholung
$(-3) \cdot (-2)$: Zweimal „entgegengesetzt“ von $-3$. Die Änderung $-3$ wird zweimal rückwärts ausgeführt, also
zweimal $+3$. Zusammen $+6$.
:::
""")

k.luecke("Beweis von $(-z)(-q) = zq$ mit $z = [(a, b)]$ und $q = [(c, d)]$. Es ist $-z = [(b, a)]$ und $-q = [(d, c)]$. Fülle die Lücken.",
         "(-z)(-q) = [(b, a)] \\cdot [(d, c)] = [(\\luecke,\\ \\luecke)] = [(a, b)] \\cdot [(c, d)]",
         [["b*d + a*c", "a*c + b*d"], ["b*c + a*d", "a*d + b*c"]],
         "Nach Definition 3.5 mit $(a, b) \\to (b, a)$ und $(c, d) \\to (d, c)$: erster Eintrag $b \\cdot d + a \\cdot c$, zweiter $b \\cdot c + a \\cdot d$. "
         "Das ist $[(ac + bd,\\ ad + bc)] = zq$ (Addition in $\\mathbb{N}$ ist kommutativ).",
         tipps=["Wende $[(x, y)] \\cdot [(u, v)] = [(xu + yv,\\ xv + yu)]$ mit $(x, y) = (b, a)$ und $(u, v) = (d, c)$ an.",
                "Erster Eintrag: $x u + y v$ mit $x = b$, $u = d$, $y = a$, $v = c$.",
                "Erster Eintrag $bd + ac$, zweiter $bc + ad$."],
         rechenweg=rechnung([("b d + a c", "erster Eintrag nach Definition 3.5"), ("b c + a d", "zweiter Eintrag"),
                             ("a c + b d", "Kommutativität der Addition auf $\\mathbb{N}$: dasselbe Paar wie bei $zq$")]),
         typische_fehler=[(["b*d", "b*c"], "Du hast nur einen Summanden gezählt. Der erste Eintrag ist eine Summe aus zwei Produkten: $bd + ac$.")])

k.wf("Für $z = [(2, 5)]$ und $q = [(1, 4)]$ gilt $z \\cdot q = [(2 \\cdot 1,\\ 5 \\cdot 4)]$.", False,
     "Die Multiplikation ist **nicht** komponentenweise. Richtig ist $[(2 \\cdot 1 + 5 \\cdot 4,\\ 2 \\cdot 4 + 5 \\cdot 1)] = [(22, 13)] = 9$, passend zu $(-3) \\cdot (-3) = 9$.",
     tipps=["Rechne mit den Zahlen: $-3 \\cdot (-3)$. Kommt $-18$ heraus?"])

# ── Seite 7: Definition 3.6 ─────────────────────────────────────────────
k.erklaerung("Ordnung, Teilbarkeit, div und mod auf ℤ", r"""
## Definition 3.6

Das Skript setzt weitere Begriffe von $\mathbb{N}$ auf $\mathbb{Z}$ fort:

- **Ordnung:** $[(a, b)] \le [(c, d)]$, falls $a + d \le b + c$.
- **Teilbarkeit:** $q \mid z$, falls $z = k \cdot q$ für ein $k \in \mathbb{Z}$ ($q \ne 0$).
- **Division mit Rest:** Zu $z \in \mathbb{Z}$, $n \in \mathbb{N}\setminus\{0\}$ gibt es eindeutige $q \in \mathbb{Z}$ und $r \in \mathbb{N}$ mit $z = qn + r$ und $r < n$. Dann $z \operatorname{div} n := q$, $z \bmod n := r$.
- **Potenz:** $a^0 := 1$, $a^n := \prod_{i=1}^{n} a$.

Der Rest ist **immer** $0 \le r < n$, auch für negatives $z$.

:::rechnung $-7$ geteilt durch $3$ mit Rest
-7 = (-3) \cdot 3 + 2 || $q = -3$ und $r = 2$ mit $0 \le 2 < 3$
-7 = (-2) \cdot 3 + (-1) || ! $r = -1$ ist nicht in $\mathbb{N}$: nicht erlaubt
-3 \cdot 3 + 2 = -7 || Probe: $-9 + 2$
:::

:::alt Als Uhr
Auf einer Uhr mit $n$ Positionen drehst du von $0$ aus $z$ Schritte, rückwärts bei negativem $z$. Dann liegst du bei Position
$z \bmod n$. Bei $-7$ und $n = 3$: sieben Schritte zurück von $0$, das ist Position $2$.
:::
""")

k.zahl("Bestimme $(-7) \\bmod 3$.", (-7) % 3,
       "Es ist $-7 = (-3) \\cdot 3 + 2$ mit $0 \\le 2 < 3$. Also $(-7) \\operatorname{div} 3 = -3$ und $(-7) \\bmod 3 = 2$.",
       tipps=["Der Rest muss in $\\{0, 1, 2\\}$ liegen.", "Suche ein Vielfaches von $3$, das kleiner oder gleich $-7$ und möglichst nah ist: $-9$.", "$-7 = -9 + 2$."],
       rechenweg=rechnung([("-9 + 2 = -7", "$-9 = (-3) \\cdot 3$ ist das größte Vielfache von $3$ unter $-7$, bleibt $r = 2$")]),
       typische_fehler=[(-1, "Rest $-1$ ist nicht erlaubt: Nach Definition 3.6 ist $r \\in \\mathbb{N}$ mit $r < n$."),
                        (1, "Du hast $|{-7}| \\bmod 3 = 1$ gerechnet. Für negative $z$ muss man das nächste Vielfache **unterhalb** von $z$ nehmen.")])


def ganze_div_mod(rng):
    n = rng.randint(3, 9)
    z = -rng.randint(1, 40)
    if z % n == 0:
        z -= 1
    q, r = z // n, z % n
    frage_mod = rng.random() < 0.5
    trunc_q = -((-z) // n)
    trunc_r = z - n * trunc_q
    if frage_mod:
        w = r
        falsch = [(trunc_r, "Das ist der Rest bei Abrunden **Richtung Null**. Nach Definition 3.6 muss $0 \\le r < n$ gelten."),
                  ((-z) % n, "Du hast mit $|z|$ gerechnet. Für negatives $z$ ist der Rest ein anderer.")]
        frage = f"Bestimme $({z}) \\bmod {n}$."
    else:
        w = q
        falsch = [(trunc_q, "Du hast Richtung Null gerundet. Weil der Rest $r \\ge 0$ sein muss, muss $q$ nach **unten** gerundet werden."),
                  (-((-z) // n), "Das ist dasselbe: Richtung Null gerundet. Der Rest wäre negativ.")]
        frage = f"Bestimme $({z}) \\operatorname{{div}} {n}$."
    return {"frage": frage, "loesung": w,
            "tipps": ["Suche $q \\in \\mathbb{Z}$ und $r \\in \\{0, \\ldots, n-1\\}$ mit $z = qn + r$.",
                      f"Das größte Vielfache von ${n}$, das nicht größer als ${z}$ ist, ist ${q * n}$.",
                      f"${z} = {q} \\cdot {n} + {r}$."],
            "rechenweg": rechnung([(f"{q} \\cdot {n} + {r} = {z}", f"$q = {q}$, $r = {r}$ mit $0 \\le {r} < {n}$"),
                                   (f"{q} \\cdot {n} = {q * n}", f"größtes Vielfache von ${n}$ mit $\\le {z}$")]),
            "erklaerung": "Definition 3.6 (iii): Der Rest ist immer nichtnegativ. Python rechnet `z // n` und `z % n` genau so.",
            "typische_fehler": ohne_gleiche(w, falsch)}


k.generator(ganze_div_mod, typ="zahl", titel="div und mod mit negativen Zahlen")

k.mc("In welcher Aussage liegt der Rest $r$ in $z = q \\cdot n + r$ nach Definition 3.6?",
     ["$-11 = (-4) \\cdot 3 + 1$", "$-11 = (-3) \\cdot 3 + (-2)$", "$-11 = (-5) \\cdot 3 + 4$", "$-11 = 3 \\cdot (-4)$ ohne Rest"],
     "Der Rest muss $0 \\le r < 3$ erfüllen. Das trifft nur auf $r = 1$ zu. $-2$ ist negativ, $4$ ist zu groß, und $-11$ ist nicht durch $3$ teilbar.",
     tipps=["Prüfe bei jeder Zeile zuerst, ob $0 \\le r < 3$ gilt.", "Rechne zur Probe $q \\cdot 3 + r$ aus."],
     fehler={"$-11 = (-3) \\cdot 3 + (-2)$": "Rest $-2$ ist negativ. Nach Definition 3.6 muss $r \\in \\mathbb{N}$ sein.",
             "$-11 = (-5) \\cdot 3 + 4$": "Rest $4 \\ge 3 = n$. Der Rest muss kleiner als $n$ sein.",
             "$-11 = 3 \\cdot (-4)$ ohne Rest": "$3 \\cdot (-4) = -12 \\ne -11$."})

k.praxis()

k.rechenweg_aufgabe(r"""
## Quiz-Stil: Rechnen mit Paaren

Sei $z = [(3, 7)]$ und $q = [(5, 2)]$ in $\mathbb{Z} = \mathbb{N}^2/{\sim}$.
""",
    [{"typ": "zahl", "frage": "Welche ganze Zahl ist $z$?", "loesung": -4,
      "tipps": ["$[(a, b)]$ ist $a - b$.", "$3 - 7$."], "erklaerung": "$3 + 4 = 7 + 0$: $(3, 7) \\sim (0, 4)$, also $-4$.",
      "rechenweg": ":::rechnung\n3 - 7 = -4 || erster minus zweiter Eintrag\n:::"},
     {"typ": "zahl", "frage": "Welche ganze Zahl ist $z + q$ (rechne mit Paaren)?", "loesung": paar_wert(padd((3, 7), (5, 2))),
      "tipps": ["Addiere komponentenweise: $(3 + 5,\\ 7 + 2)$.", "$(8, 9)$."], "erklaerung": "$(8, 9) \\sim (0, 1)$, also $-1$.",
      "rechenweg": ":::rechnung\n(3 + 5,\\ 7 + 2) = (8, 9) || komponentenweise\n8 - 9 = -1 || die Zahl\n:::",
      "typische_fehler": [(paar_wert(padd((3, 7), pneg((5, 2)))), "Das ist $z - q$.")]},
     {"typ": "zahl", "frage": "Welche ganze Zahl ist $z \\cdot q$ (Definition 3.5)?", "loesung": paar_wert(pmul((3, 7), (5, 2))),
      "tipps": ["Der Ergebnis-Eintrag links ist $ac + bd = 3 \\cdot 5 + 7 \\cdot 2$.", "Rechts: $ad + bc = 3 \\cdot 2 + 7 \\cdot 5$."],
      "erklaerung": "$(29, 41) \\sim (0, 12)$, also $-12 = -4 \\cdot 3$.",
      "rechenweg": ":::rechnung\n3 \\cdot 5 + 7 \\cdot 2 = 29 || ac + bd\n3 \\cdot 2 + 7 \\cdot 5 = 41 || ad + bc\n29 - 41 = -12 || die Zahl\n:::",
      "typische_fehler": [(paar_wert((15, 14)), "Komponentenweise gerechnet: $(3 \\cdot 5,\\ 7 \\cdot 2)$. Richtig ist $(ac + bd,\\ ad + bc)$.")]}],
    "$z = -4$ und $q = 3$. Es gilt $z + q = -1$ und $z \\cdot q = -12$.",
    uebungsblatt=True,
    tipps=["Wandle die Paare zuerst in Zahlen um, um dein Ergebnis zu prüfen.", "Nutze die Definitionen 3.2 und 3.5 auf den Paaren selbst."],
    rechenweg=r"""
:::rechnung
3 - 7 = -4 || $z = [(3, 7)]$
(3 + 5,\ 7 + 2) = (8, 9) || Addition, $8 - 9 = -1$
3 \cdot 5 + 7 \cdot 2 = 29 || erster Eintrag der Multiplikation
3 \cdot 2 + 7 \cdot 5 = 41 || zweiter Eintrag, $29 - 41 = -12$
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Die Addition ist wohldefiniert

Zeigen Sie: Gilt $(a, b) \sim (a', b')$ und $(c, d) \sim (c', d')$, so gilt
$(a + c,\ b + d) \sim (a' + c',\ b' + d')$. Die Addition $+\colon \mathbb{Z}^2 \to \mathbb{Z}$ aus Definition 3.2 hängt also nicht von den gewählten Repräsentanten ab.
""",
    r"""
Nach Voraussetzung gilt $a + b' = b + a'$ und $c + d' = d + c'$ (Definition 3.1).
Addition der beiden Gleichungen in $\mathbb{N}$ ergibt
$$(a + c) + (b' + d') = (a + b') + (c + d') = (b + a') + (d + c') = (b + d) + (a' + c').$$
Das ist genau die Bedingung $(a + c) + (b' + d') = (b + d) + (a' + c')$ für $(a + c,\ b + d) \sim (a' + c',\ b' + d')$. $\square$
""",
    ["Die Voraussetzungen $a + b' = b + a'$ und $c + d' = d + c'$ korrekt aus Definition 3.1 hingeschrieben",
     "Beide Gleichungen addiert (nur Addition in $\\mathbb{N}$, keine Subtraktion benutzt)",
     "Assoziativität und Kommutativität der Addition in $\\mathbb{N}$ zum Umordnen genannt",
     "Das Ergebnis als Äquivalenzbedingung $a + d = b + c$ für die Paare $(a + c,\\ b + d)$ und $(a' + c',\\ b' + d')$ gelesen"],
    "Wohldefiniert heißt: Das Ergebnis ändert sich nicht, wenn du einen anderen Repräsentanten derselben Klasse wählst. "
    "Hier folgt es aus der Äquivalenzbedingung, ohne zu subtrahieren.",
    uebungsblatt=True,
    tipps=["Schreibe die Bedingung für $(a, b) \\sim (a', b')$ und für $(c, d) \\sim (c', d')$ hin.", "Addiere die beiden Gleichungen und ordne um.",
           "Vergleiche das Ergebnis mit der Definition von $\\sim$ für die Paare $(a + c,\\ b + d)$ und $(a' + c',\\ b' + d')$."])

k.papier(r"""
## Übungsblatt-Stil: Vorzeichenregel $(-z)q = -(zq)$

Seien $z = [(a, b)]$, $q = [(c, d)] \in \mathbb{Z}$. Zeigen Sie mit den Definitionen 3.5 und Beobachtung 3.4: $(-z)q = -(zq)$.
""",
    r"""
Nach Beobachtung 3.4 ist $-z = [(b, a)]$. Mit Definition 3.5 folgt
$$(-z)q = [(b, a)] \cdot [(c, d)] = [(bc + ad,\ bd + ac)].$$
Andererseits ist $zq = [(ac + bd,\ ad + bc)]$ und daher, wieder nach Beobachtung 3.4,
$-(zq) = [(ad + bc,\ ac + bd)]$.
Wegen der Kommutativität der Addition in $\mathbb{N}$ sind $(bc + ad,\ bd + ac)$ und $(ad + bc,\ ac + bd)$ dasselbe Paar.
Also $(-z)q = -(zq)$. $\square$
""",
    ["$-z = [(b, a)]$ aus Beobachtung 3.4 benutzt",
     "$(-z)q$ mit Definition 3.5 ausgerechnet: erster Eintrag $bc + ad$, zweiter $bd + ac$",
     "$-(zq)$ durch Vertauschen der Einträge von $zq = [(ac + bd,\\ ad + bc)]$ gebildet",
     "Mit Kommutativität der Addition gezeigt, dass beide Paare übereinstimmen"],
    "Vorzeichenregeln sind keine Rechentricks: Sie folgen aus den Definitionen mit Paaren.",
    uebungsblatt=True,
    tipps=["Schreibe $-z$ als Paar mit vertauschten Einträgen.", "Wende Definition 3.5 an: $(x, y) \\cdot (u, v) = (xu + yv,\\ xv + yu)$."])

k.zusammenfassung(r"""
## Die ganzen Zahlen (Skript Abschn. 3.1, Def. 3.1 bis 3.6)

- **Idee:** Änderungen als Paare $(a, b) \in \mathbb{N}^2$, ohne Subtraktion zu benutzen. $(a, b) \sim (c, d) :\iff a + d = b + c$ (Def. 3.1).
- $\mathbb{Z} := \mathbb{N}^2/{\sim}$. Für $a \in \mathbb{N}$: $a = [(a, 0)]$ und $-a = [(0, a)]$.
- **Addition** (Def. 3.2): $[(a, b)] + [(c, d)] = [(a + c,\ b + d)]$, wohldefiniert und Fortsetzung von $+$ auf $\mathbb{N}$.
- **Subtraktion** (Def. 3.3, Beob. 3.4): $b - a = T_a^{-1}(b)$ mit $T_a\colon x \mapsto x + a$; $-[(c, d)] = [(d, c)]$; $b - a = b + (-a)$.
- **Multiplikation** (Def. 3.5): $[(a, b)] \cdot [(c, d)] = [(ac + bd,\ ad + bc)]$; $(-z)q = -(zq)$, $(-z)(-q) = zq$.
- **Def. 3.6:** $\le$ via $a + d \le b + c$; $q \mid z \iff \exists k \in \mathbb{Z} : z = kq$; $z = qn + r$ mit $0 \le r < n$ gibt $z \operatorname{div} n = q$, $z \bmod n = r$; $a^0 = 1$.
- **Satz 3.7:** $a + x = b$ hat genau eine Lösung $x = b - a$ (aus Assoziativität, Null und Gegenelement).

!! Der Rest bei $z \bmod n$ ist immer nichtnegativ: $(-7) \bmod 3 = 2$.
""")
