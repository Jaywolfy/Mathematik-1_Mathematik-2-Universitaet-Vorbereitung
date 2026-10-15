# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 15: Gruppen (Skript Disser WS 26/27, Abschn. 3.2 bis vor „Untergruppen“, Def. 3.8 bis Def. 3.18)."""
from itertools import permutations, product

from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(
    slug="gruppen",
    titel="Gruppen",
    beschreibung="Gruppenaxiome, abelsche Gruppen, Eindeutigkeit von neutralem und inversem Element, Kürzungsregeln, Beispiele: ℤ, Permutationen, Bitgruppe, ℤ/nℤ",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 3.2",
    icon="🔷")


# ── Python prüft Gruppenaxiome an endlichen Verknüpfungen ────────────────
def pruefe_gruppe(M, op):
    """Liefert (Befund, Begründung) nach Def. 3.8: Assoziativität, linksneutrales Element, Linksinverse."""
    for a, b, c in product(M, repeat=3):
        if op(a, op(b, c)) != op(op(a, b), c):
            return "A", f"$({a} \\ast {b}) \\ast {c} = {op(op(a, b), c)}$, aber ${a} \\ast ({b} \\ast {c}) = {op(a, op(b, c))}$"
    neutral = [e for e in M if all(op(e, a) == a for a in M)]
    if not neutral:
        return "N", "Für kein $e$ gilt $e \\ast a = a$ für alle $a$"
    e = neutral[0]
    for a in M:
        if not any(op(b, a) == e for b in M):
            return "I", f"Das neutrale Element ist ${e}$, aber zu ${a}$ gibt es kein $b$ mit $b \\ast {a} = {e}$"
    return "G", f"neutrales Element ${e}$, alle Inversen vorhanden"


def kommutativ(M, op):
    return all(op(a, b) == op(b, a) for a in M for b in M)


def tafel_tex(M, op, zeichen="\\ast"):
    kopf = "c|" + "c" * len(M)
    zeilen = " & ".join(str(b) for b in M)
    inhalt = "".join(f" {a} & " + " & ".join(str(op(a, b)) for b in M) + " \\\\" for a in M)
    return f"\\begin{{array}}{{{kopf}}} {zeichen} & {zeilen} \\\\ \\hline{inhalt} \\end{{array}}"


def rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def komp(f, g):
    """Verkettung f ∘ g für Permutationen als Dicts: x -> f(g(x))."""
    return {x: f[g[x]] for x in g}


def inv_perm(f):
    return {v: k_ for k_, v in f.items()}


# Beispiele 3.10 bis 3.15 nachrechnen
_Z6 = range(6)
assert pruefe_gruppe(list(_Z6), lambda a, b: (a + b) % 6)[0] == "G"
assert pruefe_gruppe([-1, 1], lambda a, b: a * b)[0] == "G"                 # Bsp. 3.11
_PM = [frozenset(s) for s in [(), (1,), (2,), (1, 2)]]
assert pruefe_gruppe(_PM, lambda a, b: a | b)[0] == "I"                      # Bsp. 3.12
_fa = {"a": "a", "b": "c", "c": "b"}
_ga = {"a": "b", "b": "c", "c": "a"}
assert komp(_fa, _ga) == {"a": "c", "b": "b", "c": "a"} and komp(_ga, _fa) == {"a": "b", "b": "a", "c": "c"}   # Bsp. 3.13
_perms3 = [dict(zip((1, 2, 3), p)) for p in permutations((1, 2, 3))]
assert len(_perms3) == 6 and all(komp(f, g) in _perms3 for f in _perms3 for g in _perms3)
assert not all(komp(f, g) == komp(g, f) for f in _perms3 for g in _perms3)
_B2 = list(product((0, 1), repeat=2))                                          # Bsp. 3.14
assert pruefe_gruppe(_B2, lambda x, y: tuple((a + b) % 2 for a, b in zip(x, y)))[0] == "G"
assert all(tuple((a + a) % 2 for a in x) == (0, 0) for x in _B2)
assert pruefe_gruppe(list(range(4)), lambda a, b: (a + b) % 4)[0] == "G"      # Bsp. 3.15
assert pruefe_gruppe(list(range(4)), lambda a, b: (a * b) % 4)[0] == "I"

k.lernziele([
    "Ich kann die Gruppenaxiome (a), (n), (i) und die Kommutativität (k) hinschreiben und an Verknüpfungstafeln prüfen (Def. 3.8)",
    "Ich kann begründen, warum neutrales und inverses Element eindeutig sind und auch von rechts wirken (Satz 3.9)",
    "Ich erkenne die Beispiele 3.10 bis 3.15: $(\\mathbb{Z}, +)$, $(\\{-1, 1\\}, \\cdot)$, Permutationen, Bitgruppe $B_n$, $\\mathbb{Z}/n\\mathbb{Z}$, und weiß, warum $(\\mathcal{P}(M), \\cup)$ keine Gruppe ist",
    "Ich kann Gleichungen $a \\ast x = b$ lösen, kürzen und Inverse von Produkten bilden (Satz 3.16, 3.17)",
])

k.warum(r"""
Verschlüsseln mit XOR, Bits kippen, Daten umsortieren, mit Uhrzeiten rechnen: Überall wirst du Operationen
verketten und zurückdrehen wollen. Eine Gruppe ist genau die Struktur, in der das immer geht. Alles, was du
einmal über Gruppen beweist, gilt dann für $\mathbb{Z}$, für Permutationen, für XOR auf Bitfolgen und für Rechnen modulo $n$.
RSA (Kap. „Kryptographie“) und Fehlerkorrektur bauen darauf auf. Dieses Kapitel ist dein erster Kontakt mit
einer **Struktur**: Du lernst, aus Axiomen zu beweisen, ohne konkrete Zahlen zu kennen.
""")

# ── Seite 1: Definition 3.8 ──────────────────────────────────────────────
k.erklaerung("Definition 3.8: Gruppe", r"""
## Drei Eigenschaften der Addition

Im Beweis von Satz 3.7 (Kap. „Die ganzen Zahlen“) hast du nur drei Dinge benutzt: Klammern darf man versetzen,
die $0$ ändert nichts, zu jedem $a$ gibt es $-a$. Dasselbe gilt für das Umsortieren von Tupeln und für vieles mehr.

**Definition 3.8.** Ein Tupel $(G, \ast)$ aus einer Menge $G \ne \emptyset$ und einer [[Verknüpfung]] $\ast\colon G^2 \to G$ heißt
[[Gruppe]], falls

- (a) $a \ast (b \ast c) = (a \ast b) \ast c$ für alle $a, b, c \in G$ ([[Assoziativität|Assoziativgesetz]]),
- (n) es ein [[neutrales Element]] $e \in G$ gibt mit $e \ast a = a$ für alle $a \in G$,
- (i) zu jedem $a \in G$ ein [[inverses Element]] $b \in G$ existiert mit $b \ast a = e$.

Sie heißt [[abelsch]], falls zusätzlich (k) $a \ast b = b \ast a$ gilt.

:::rechnung Prüfung an $(\mathbb{Z}, +)$ mit $a = 2$, $b = 3$, $c = 4$
2 + (3 + 4) = 9 || (a): die Klammer rechts zuerst
(2 + 3) + 4 = 9 || (a): die Klammer links zuerst, gleiches Ergebnis
0 + 2 = 2 || (n): $e = 0$
(-2) + 2 = 0 || (i): $b = -2$ ist invers zu $2$
:::

:::alt Als Zauberwürfel
Jeder Dreh ist eine Verknüpfung. Dreh hintereinander ist assoziativ, „nichts tun“ ist das neutrale Element und jeder Dreh lässt
sich rückwärts drehen (Inverses). Eine Gruppe ist abelsch, wenn die Reihenfolge der Drehs egal ist. Beim Würfel ist sie das nicht.
:::
""")

k.mc("Welche Eigenschaft wird in Definition 3.8 **nicht** für jede Gruppe gefordert?",
     ["Kommutativität: $a \\ast b = b \\ast a$", "Assoziativität", "Existenz eines neutralen Elements", "Existenz inverser Elemente"],
     "Assoziativität, neutrales Element und Inverse (a), (n), (i) sind die Gruppenaxiome. Kommutativität (k) ist nur für **abelsche** Gruppen verlangt. "
     "Die Permutationen aus Beispiel 3.13 bilden eine Gruppe, die nicht abelsch ist.",
     tipps=["Welche der vier Eigenschaften trägt in der Definition den Namen „abelsch“?", "Denk an das Zusammensetzen von Umsortierungen: Ist die Reihenfolge egal?"],
     fehler={"Assoziativität": "Die Assoziativität (a) ist das erste Axiom jeder Gruppe.",
             "Existenz eines neutralen Elements": "(n) ist ein Gruppenaxiom.",
             "Existenz inverser Elemente": "(i) ist ein Gruppenaxiom."})

# ── Seite 2: Verknüpfungstafeln ──────────────────────────────────────────
k.erklaerung("Verknüpfungstafeln lesen", r"""
## Eine Gruppe als Tabelle

Bei endlichen Mengen schreibst du die Verknüpfung in eine [[Verknüpfungstafel]]: Zeile $a$, Spalte $b$, Eintrag $a \ast b$.

Tafel von $(\{-1, 1\}, \cdot)$ (Beispiel 3.11) und von $(\mathbb{Z}/3\mathbb{Z}, +)$:

| $\cdot$ | $1$ | $-1$ |
|---|---|---|
| $1$ | $1$ | $-1$ |
| $-1$ | $-1$ | $1$ |

| $+$ | $[0]_3$ | $[1]_3$ | $[2]_3$ |
|---|---|---|---|
| $[0]_3$ | $[0]_3$ | $[1]_3$ | $[2]_3$ |
| $[1]_3$ | $[1]_3$ | $[2]_3$ | $[0]_3$ |
| $[2]_3$ | $[2]_3$ | $[0]_3$ | $[1]_3$ |

**Neutrales Element:** die Zeile, die der Kopfzeile gleicht. **Inverses:** in Zeile $a$ das $e$ suchen, die Spalte nennt $b$ mit $a \ast b = e$. **Abelsch:** Tafel symmetrisch zur Diagonale.

:::rechnung Inverses von $[2]_3$ ablesen
\text{Zeile } [2]_3 \text{: der Eintrag } [0]_3 \text{ steht in der Spalte } [1]_3 || $[2]_3 + [1]_3 = [0]_3$
\text{also } [2]_3^{-1} = [1]_3 || Probe: $2 + 1 = 3 \equiv 0$
:::

:::achtung Assoziativität steht nicht in der Tafel
Dass jede Zeile und Spalte alle Elemente enthält, sieht man schnell. Die Assoziativität musst du mit **allen** Tripeln prüfen
oder aus dem Zusammenhang wissen.
:::

:::alt Als Sudoku
In einer Gruppentafel kommt in jeder Zeile und Spalte jedes Element genau einmal vor (das ist Satz 3.16 (i)).
Fehlt irgendwo ein Element oder steht es doppelt, ist es keine Gruppe.
:::
""")


def gruppe_tafel_pruefen(rng):
    n = rng.choice([3, 4, 5])
    M = list(range(n))
    wahl = rng.choice(["add", "mul", "sub", "max", "shift", "links"])
    ops = {"add": (lambda a, b: (a + b) % n, f"(a + b) \\bmod {n}"),
           "mul": (lambda a, b: (a * b) % n, f"(a \\cdot b) \\bmod {n}"),
           "sub": (lambda a, b: (a - b) % n, f"(a - b) \\bmod {n}"),
           "max": (lambda a, b: max(a, b), "\\max(a, b)"),
           "shift": (lambda a, b: (a + b + 1) % n, f"(a + b + 1) \\bmod {n}"),
           "links": (lambda a, b: a, "a")}
    op, beschr = ops[wahl]
    befund, grund = pruefe_gruppe(M, op)
    if wahl == "sub" and befund == "G":
        return gruppe_tafel_pruefen(rng)
    G = "Gruppe"
    A = "keine Gruppe: nicht assoziativ"
    N = "keine Gruppe: kein neutrales Element"
    I = "keine Gruppe: nicht jedes Element hat ein inverses Element"
    korrekt = {"G": G, "A": A, "N": N, "I": I}[befund]
    optionen = [korrekt] + [o for o in (G, A, N, I) if o != korrekt]
    fehler = {o: f"Prüfe die Axiome der Reihe nach. Hier: {grund}." for o in optionen[1:]}
    zeilen = [(f"\\text{{Axiom (a), (n), (i) der Reihe nach prüfen}}", grund)]
    return {"typ": "mc",
            "frage": f"Auf $G = \\{{0, 1, \\ldots, {n - 1}\\}}$ ist $a \\ast b := {beschr}$ gegeben. Die Tafel ist ${tafel_tex(M, op)}$. Was gilt?",
            "optionen": optionen, "fehler": fehler,
            "tipps": ["Prüfe der Reihe nach: (a) Assoziativität, dann (n) neutrales Element, dann (i) Inverse.",
                      "Das neutrale Element ist die Zeile, die genauso aussieht wie die Kopfzeile. Gibt es sie?",
                      "Hat jede Zeile den Eintrag $e$ (das neutrale Element) irgendwo? Sonst fehlt ein Inverses."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Nach Definition 3.8 prüfst du (a), (n) und (i). Schon ein Verstoß genügt für „keine Gruppe“."}



k.luecke("Ergänze die Verknüpfungstafel von $(\\mathbb{Z}/4\\mathbb{Z}, +)$ aus Beispiel 3.15: $[3]_4 + [2]_4 = [\\luecke]_4$ und $[3]_4 + [1]_4 = [\\luecke]_4$.",
         "[3]_4 + [2]_4 = [\\luecke]_4 \\quad\\text{und}\\quad [3]_4 + [1]_4 = [\\luecke]_4",
         [[1], [0]],
         "$3 + 2 = 5$ und $5 \\bmod 4 = 1$. $3 + 1 = 4$ und $4 \\bmod 4 = 0$.",
         tipps=["Addiere die Zahlen und nimm den Rest modulo $4$.", "$3 + 2 = 5$.", "$5 \\bmod 4 = 1$, und $3 + 1 = 4 \\equiv 0$."],
         rechenweg=rechnung([("(3 + 2) \\bmod 4 = 1", "$5 = 1 \\cdot 4 + 1$"), ("(3 + 1) \\bmod 4 = 0", "$4 = 1 \\cdot 4 + 0$")]),
         typische_fehler=[([5, 4], "Du hast nur addiert. Ein Eintrag in der Tafel von $\\mathbb{Z}/4\\mathbb{Z}$ liegt immer in $\\{0, 1, 2, 3\\}$: Rest nehmen.")])

# ── Seite 3: Satz 3.9 ────────────────────────────────────────────────────
k.erklaerung("Satz 3.9: Eindeutigkeit und Wirkung von rechts", r"""
## Mehr als man fordert

Definition 3.8 fordert $e \ast a = a$ und $b \ast a = e$ nur **von links**. Der Satz zeigt, dass alles auch von rechts gilt.

**Satz 3.9.** In jeder Gruppe ist das neutrale Element eindeutig, jedes $a$ hat genau ein inverses Element $b$, und es gilt $a \ast e = a$ sowie $a \ast b = e$.

*Beweisplan.*
1. Zu $b \ast a = e$ und $c \ast b = e$: $a \ast b = e$ (Inverses wirkt auch von rechts).
2. Daraus $a \ast e = a$ (neutrales Element wirkt auch von rechts).
3. Zwei neutrale $e, e'$: $e = e' \ast e = e'$.
4. Zwei inverse $b, c$ zu $a$: $b = b \ast (a \ast c) = (b \ast a) \ast c = c$.

:::rechnung Schritt 2 an $(\mathbb{Z}/5\mathbb{Z}, +)$ mit $a = [3]$, $b = [2]$
\text{(i): } [2] + [3] = [0] || $b$ ist Inverses von $a$
\text{Schritt 1: } [3] + [2] = [0] || auch von rechts, $a \ast b = e$
\text{(i), Schritt 1: } [3] + [0] = [3] + ([2] + [3]) = ([3] + [2]) + [3] = [0] + [3] = [3] || $a \ast e = a$
:::

:::alt Als Treppe
Zuerst zeigst du die rechte Inverse-Eigenschaft, mit ihr die rechte Neutralität, mit beiden die Eindeutigkeit. Jeder Schritt benutzt
nur die vorherigen und die drei Axiome. Das ist die Kunst: nie mehr benutzen, als du hast.
:::
""")

k.ordnen("Ordne den ersten Teil des Beweises von Satz 3.9: Aus $b \\ast a = e$ folgt $a \\ast b = e$. Dabei sei $c$ ein inverses Element zu $b$, also $c \\ast b = e$.",
         ["$a \\ast b = (e \\ast a) \\ast b$ nach (n), denn $e \\ast a = a$.",
          "$(e \\ast a) \\ast b = ((c \\ast b) \\ast a) \\ast b$ nach (i), denn $e = c \\ast b$.",
          "$((c \\ast b) \\ast a) \\ast b = (c \\ast (b \\ast a)) \\ast b$ nach (a).",
          "$(c \\ast (b \\ast a)) \\ast b = (c \\ast e) \\ast b$ nach Voraussetzung $b \\ast a = e$.",
          "$(c \\ast e) \\ast b = c \\ast (e \\ast b)$ nach (a).",
          "$c \\ast (e \\ast b) = c \\ast b = e$ nach (n) und (i)."],
         "Die Kette beginnt bei $a \\ast b$ und endet bei $e$. Jeder Schritt benutzt genau ein Axiom oder die Voraussetzung. Neu eingeführt wird nur das Inverse $c$ von $b$.",
         ablenker=["$a \\ast b = b \\ast a$ nach (k), denn die Gruppe ist abelsch.", "$(c \\ast e) \\ast b = c \\ast e$ nach (n)."],
         tipps=["Starte bei $a \\ast b$ und füge mit (n) das $e$ vor $a$ ein.", "Ersetze dieses $e$ durch $c \\ast b$ und verschiebe dann die Klammer.",
                "Kommutativität darf **nicht** benutzt werden: Die Gruppe muss nicht abelsch sein."])

k.ordnen("Ordne den zweiten Teil von Satz 3.9: Das Inverse ist eindeutig. Seien $b, c$ inverse Elemente zu $a$, also $b \\ast a = e$ und $c \\ast a = e$.",
         ["Aus dem ersten Teil gilt auch $a \\ast c = e$ (Inverses wirkt von rechts) und $b \\ast e = b$ (Neutrales wirkt von rechts).",
          "Es ist $b = b \\ast e$.",
          "Es ist $b \\ast e = b \\ast (a \\ast c)$, denn $a \\ast c = e$.",
          "Es ist $b \\ast (a \\ast c) = (b \\ast a) \\ast c$ nach (a).",
          "Es ist $(b \\ast a) \\ast c = e \\ast c = c$ nach Voraussetzung und (n).",
          "Also $b = c$. $\\square$"],
         "Du schiebst $b$ in einer Kette bis zu $c$: Mit $e$ einfügen, Klammer verschieben, $b \\ast a = e$ benutzen. Dafür braucht man die rechte Seite der Axiome aus dem ersten Teil.",
         ablenker=["Da $b$ und $c$ in derselben Gruppe liegen, sind sie gleich.", "Aus $b \\ast a = c \\ast a$ folgt $b = c$ nach der Kürzungsregel, die schon bekannt ist."],
         tipps=["Starte mit $b = b \\ast e$ und ersetze $e$ durch $a \\ast c$.", "Ziehe die Klammer nach links: $(b \\ast a) \\ast c$.",
                "Die Kürzungsregel (Satz 3.16) folgt erst **aus** Satz 3.9. Hier darfst du sie nicht benutzen."])

k.wf("In einer Gruppe $(G, \\ast)$ mit neutralem Element $e$ gilt aus den Axiomen (a), (n), (i) allein auch $a \\ast e = a$ für alle $a \\in G$.", True,
     "Das ist die Aussage von Satz 3.9: Das neutrale Element wirkt auch von rechts, obwohl (n) nur $e \\ast a = a$ fordert. "
     "Man benutzt $a \\ast e = a \\ast (b \\ast a) = (a \\ast b) \\ast a = e \\ast a = a$ mit $b = a^{-1}$.",
     tipps=["Die Definition fordert nur eine Seite. Folgt die andere automatisch?"])

# ── Seite 4: Beispiele 3.10 bis 3.12 ────────────────────────────────────
k.erklaerung("Beispiele 3.10 bis 3.12", r"""
## Gruppe oder keine Gruppe?

- **3.10:** $(\mathbb{Z}, +)$ ist abelsch, neutral $0$, invers zu $a$ ist $-a$.
- **3.11:** $(\{-1, 1\}, \cdot)$ ist abelsch, neutral $1$, jedes Element ist sein eigenes Inverses.
- **3.12:** $(\mathcal{P}(M), \cup)$ mit $M \ne \emptyset$ ist **keine** Gruppe.

Bei 3.12 ist $\cup$ assoziativ und $\emptyset$ ist neutral. Aber ein nichtleeres $A$ hat kein Inverses, denn $A \cup B \ne \emptyset$ für jedes $B$.
Die Gleichung $A \cup X = B$ ist nicht immer lösbar und nicht immer eindeutig lösbar.

:::rechnung $A \cup X = B$ ohne eindeutige Lösung
\{2\} \cup \{1\} = \{1, 2\} || $X = \{1\}$ löst $A \cup X = B$ für $A = \{2\}$, $B = \{1, 2\}$
\{2\} \cup \{1, 2\} = \{1, 2\} || auch $X = \{1, 2\}$ löst sie: Lösung nicht eindeutig
\{1, 2\} \cup X \ne \{2\} || für $A = \{1, 2\}$, $B = \{2\}$ gibt es gar keine Lösung
:::

:::alt Als Mülleimer
Die Vereinigung verliert Information: Aus $A \cup X$ kannst du nicht rekonstruieren, was $X$ war, so wie du aus einem
gemischten Eimer nicht mehr siehst, wer was reingeworfen hat. Eine Gruppenoperation dagegen ist umkehrbar.
:::
""")

k.mehrfach("Welche der folgenden Strukturen sind Gruppen?",
           ["$(\\mathbb{Z}, +)$", "$(\\{-1, 1\\}, \\cdot)$", "$(\\mathbb{Z}/5\\mathbb{Z}, +)$"],
           ["$(\\mathbb{N}, +)$", "$(\\mathcal{P}(\\{1, 2\\}), \\cup)$", "$(\\mathbb{Z}, \\cdot)$"],
           "$(\\mathbb{N}, +)$: $1$ hat kein Inverses in $\\mathbb{N}$. $(\\mathcal{P}(M), \\cup)$: Beispiel 3.12. $(\\mathbb{Z}, \\cdot)$: neutral $1$, aber $2$ hat in $\\mathbb{Z}$ kein Inverses.",
           tipps=["Prüfe zu jeder Struktur: gibt es ein neutrales Element? Hat jedes Element ein Inverses?", "Hat $2$ ein Inverses bezüglich $\\cdot$ in $\\mathbb{Z}$?"],
           fehler={"$(\\mathbb{N}, +)$": "Es gibt kein $b \\in \\mathbb{N}$ mit $b + 1 = 0$. Die Inversen fehlen.",
                   "$(\\mathcal{P}(\\{1, 2\\}), \\cup)$": "Kein nichtleeres $A$ hat ein Inverses (Beispiel 3.12).",
                   "$(\\mathbb{Z}, \\cdot)$": "Das neutrale Element ist $1$, aber $b \\cdot 2 = 1$ hat keine Lösung in $\\mathbb{Z}$."})

# ── Seite 5: Beispiel 3.13 Permutationen ────────────────────────────────
k.erklaerung("Beispiel 3.13: Permutationen", r"""
## Umsortieren ist eine Gruppe, aber keine abelsche

Eine Permutation von $M$ ist eine bijektive Abbildung $M \to M$ (Abschn. 2.7). Mit der Menge $\mathrm{perm}(M)$ aller Permutationen ist $(\mathrm{perm}(M), \circ)$ eine Gruppe:

- $\circ$ ist eine Verknüpfung nach Satz 1.82 (Verkettung von Bijektionen ist bijektiv),
- (a) gilt, denn $f \circ (g \circ h) = (x \mapsto f(g(h(x)))) = (f \circ g) \circ h$,
- (n) $e = \mathrm{id}_M$, (i) $f^{-1}$ nach Satz 1.76.

Nicht abelsch: Für $M = \{a, b, c\}$, $f = (b \leftrightarrow c)$ und $g = (a \to b \to c \to a)$ ist $f \circ g \ne g \circ f$.

:::rechnung $f \circ g$ und $g \circ f$ auf $\{a, b, c\}$
a \mapsto b \mapsto c || $(f \circ g)(a) = f(g(a)) = f(b) = c$ (erst $g$, dann $f$)
c \mapsto a \mapsto a || $(f \circ g)(c) = f(g(c)) = f(a) = a$, also $f \circ g$ vertauscht $a \leftrightarrow c$
a \mapsto a \mapsto b || $(g \circ f)(a) = g(f(a)) = g(a) = b$: ein anderes Ergebnis
:::

:::alt Als Anziehen
Erst Socken, dann Schuhe ist etwas anderes als erst Schuhe, dann Socken. Zwei Umsortierungen hintereinander hängen
von der Reihenfolge ab. Umkehren musst du in umgekehrter Reihenfolge (Satz 3.16 (iii)).
:::
""")


def perm_verkettung(rng):
    X = [1, 2, 3]
    while True:
        f = dict(zip(X, rng.sample(X, 3)))
        g = dict(zip(X, rng.sample(X, 3)))
        if komp(f, g) != komp(g, f) and f != {1: 1, 2: 2, 3: 3} and g != {1: 1, 2: 2, 3: 3}:
            break
    fg = komp(f, g)
    gf = komp(g, f)
    ft = "(" + ", ".join(str(f[x]) for x in X) + ")"
    gt = "(" + ", ".join(str(g[x]) for x in X) + ")"
    falsch = [([gf[x] for x in X], "Das ist $g \\circ f$. Bei $f \\circ g$ wirkt $g$ **zuerst**."),
              ([f[x] for x in X], "Das ist nur $f$. Danach muss noch $g$ nachgeschaltet werden, und zwar vorher.")]
    zeilen = [(f"{x} \\mapsto {g[x]} \\mapsto {fg[x]}", f"$g({x}) = {g[x]}$, dann $f({g[x]}) = {fg[x]}$") for x in X]
    return {"typ": "vektor",
            "frage": f"Seien $f = {ft}$ und $g = {gt}$ Permutationen von $\\{{1, 2, 3\\}}$, gegeben als Tupel $(f(1), f(2), f(3))$ und $(g(1), g(2), g(3))$. Bestimme $f \\circ g$ als Tupel $((f \\circ g)(1), (f \\circ g)(2), (f \\circ g)(3))$.",
            "loesung": [fg[x] for x in X],
            "tipps": ["$(f \\circ g)(x) = f(g(x))$: erst $g$, dann $f$.", f"Für $x = 1$: $g(1) = {g[1]}$ und dann $f({g[1]}) = {f[g[1]]}$.", "Gehe so für $x = 1, 2, 3$ durch."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Die Verkettung zweier Permutationen ist wieder eine Permutation (Satz 1.82). Die Reihenfolge ist wichtig: im Allgemeinen $f \\circ g \\ne g \\circ f$.",
            "typische_fehler": ohne_gleiche([fg[x] for x in X], falsch)}



# ── Seite 6: Beispiel 3.14 Bitgruppe ────────────────────────────────────
k.erklaerung("Beispiel 3.14: Die Bitgruppe", r"""
## XOR auf Bitfolgen

Für festes $n \in \mathbb{N}\setminus\{0\}$ ist $B_n := (\{0, 1\}^n, \oplus)$ mit
$$(x_1, \ldots, x_n) \oplus (y_1, \ldots, y_n) := \big((x_1 + y_1) \bmod 2,\ \ldots,\ (x_n + y_n) \bmod 2\big)$$
eine abelsche Gruppe. Assoziativität und Kommutativität folgen aus Satz 2.44. Das neutrale Element ist $(0, \ldots, 0)$, und
**jedes Element ist sein eigenes Inverses**: $x \oplus x = (0, \ldots, 0)$.

:::rechnung In $B_3$: $(1, 0, 1) \oplus (1, 1, 0)$
(1 + 1) \bmod 2 = 0 || erste Stelle
(0 + 1) \bmod 2 = 1 || zweite Stelle
(1 + 0) \bmod 2 = 1 || dritte Stelle: Ergebnis $(0, 1, 1)$
(1 + 1) \bmod 2 = 0 || Probe: $x \oplus x$ ist stellenweise $0$
:::

Das ist die Operation XOR: Du kippst Bits dort, wo das zweite Argument eine $1$ hat. Zweimal kippen stellt den Ausgangszustand wieder her.

:::alt Als Lichtschalter
$n$ Schalter. Ein Element der Gruppe sagt, welche Schalter du umlegst. Zweimal dieselben umlegen heißt: nichts verändert. Daher ist jedes Element selbstinvers,
und die Reihenfolge der Umlegungen spielt keine Rolle.
:::
""")


def bitgruppe_xor(rng):
    n = rng.choice([3, 4, 5])
    x = [rng.randint(0, 1) for _ in range(n)]
    y = [rng.randint(0, 1) for _ in range(n)]
    while x == y or all(v == 0 for v in x) or all(v == 0 for v in y):
        x = [rng.randint(0, 1) for _ in range(n)]
        y = [rng.randint(0, 1) for _ in range(n)]
    z = [(a + b) % 2 for a, b in zip(x, y)]
    falsch = [([a + b for a, b in zip(x, y)], "Du hast ohne Rest addiert. In $B_n$ rechnest du jede Stelle modulo $2$: $1 + 1 = 0$."),
              ([a * b for a, b in zip(x, y)], "Das ist das stellenweise UND. Gefragt ist $\\oplus$: jede Stelle $(x_i + y_i) \\bmod 2$."),
              (x, "Das ist nur das erste Tupel. Verknüpfe beide stellenweise.")]
    tup = lambda v: "(" + ", ".join(str(t) for t in v) + ")"
    zeilen = [(f"({a} + {b}) \\bmod 2 = {c}", f"Stelle {i + 1}") for i, (a, b, c) in enumerate(zip(x, y, z))]
    return {"typ": "vektor",
            "frage": f"Berechne in der Bitgruppe $B_{n}$ die Verknüpfung ${tup(x)} \\oplus {tup(y)}$.",
            "loesung": z,
            "tipps": ["$\\oplus$ wirkt stellenweise: $(x_i + y_i) \\bmod 2$.", f"Erste Stelle: $({x[0]} + {y[0]}) \\bmod 2 = {z[0]}$.", "Zwei Einsen ergeben $0$, sonst die Summe."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "In $B_n$ gilt $x \\oplus x = (0, \\ldots, 0)$: XOR mit demselben Wert macht sich selbst rückgängig.",
            "typische_fehler": ohne_gleiche(z, falsch)}



k.mc("Was ist das inverse Element von $x = (1, 0, 1, 1)$ in $B_4$?",
     ["$(1, 0, 1, 1)$ selbst", "$(0, 1, 0, 0)$", "$(-1, 0, -1, -1)$", "$(0, 0, 0, 0)$"],
     "In $B_n$ ist jedes Element sein eigenes Inverses, denn $x \\oplus x = (0, 0, 0, 0)$. $(0, 1, 0, 0)$ ist das bitweise Komplement, nicht das Inverse. "
     "$(-1, 0, -1, -1)$ liegt nicht in $\\{0, 1\\}^4$.",
     tipps=["Gesucht ist $y$ mit $y \\oplus x = (0, 0, 0, 0)$.", "$1 \\oplus 1 = 0$ und $0 \\oplus 0 = 0$."],
     fehler={"$(0, 1, 0, 0)$": "Das ist das bitweise NICHT. $x \\oplus (0, 1, 0, 0) = (1, 1, 1, 1) \\ne (0, 0, 0, 0)$.",
             "$(-1, 0, -1, -1)$": "Das wäre das Inverse in $(\\mathbb{Z}^4, +)$. In $B_4$ sind nur Einträge $0$ und $1$ erlaubt.",
             "$(0, 0, 0, 0)$": "Das ist das neutrale Element, nicht das Inverse. $x \\oplus (0, 0, 0, 0) = x \\ne (0, 0, 0, 0)$."})

# ── Seite 7: Beispiel 3.15 Z/nZ ─────────────────────────────────────────
k.erklaerung("Beispiel 3.15: Restklassen Z/nZ", r"""
## Rechnen auf der Uhr

Für $n \in \mathbb{N}\setminus\{0\}$ und $a \in \mathbb{Z}$ heißt $[a]_n := \{b \in \mathbb{Z} \mid b \bmod n = a \bmod n\}$ die [[Restklasse]] von $a$ modulo $n$.
$$\mathbb{Z}/n\mathbb{Z} := \{[a]_n \mid a \in \mathbb{Z}\} = \{[0]_n, \ldots, [n-1]_n\}, \qquad [a]_n + [b]_n := [a + b]_n.$$

Die Addition ist [[wohldefiniert]]: Unterscheiden sich $a, a'$ sowie $b, b'$ um Vielfache von $n$, dann auch $a + b$ und $a' + b'$.
Neutral ist $[0]_n$, invers zu $[a]_n$ ist $[-a]_n$. Also ist $(\mathbb{Z}/n\mathbb{Z}, +)$ eine abelsche Gruppe.

:::visual modulo_uhr
{"n": 12, "start": 7, "plus": 8, "unterschrift": "$[7]_{12} + [8]_{12} = [15]_{12} = [3]_{12}$: Die Uhr springt von $7$ acht Plätze weiter."}
:::

:::rechnung Rechnen in $\mathbb{Z}/12\mathbb{Z}$
(7 + 8) \bmod 12 = 3 || $[7]_{12} + [8]_{12} = [15]_{12} = [3]_{12}$
(-7) \bmod 12 = 5 || $[7]_{12}^{-1} = [-7]_{12} = [5]_{12}$
(7 + 5) \bmod 12 = 0 || Probe: $[7]_{12} + [5]_{12} = [0]_{12}$
:::

:::alt Als Zifferblatt
Die Elemente sind Zeigerstellungen, die Addition ist Weiterdrehen. Das Inverse zu „$7$ Uhr“ ist die Stellung, die dich zurück zur $12$
bringt: „$5$ Stunden weiter“.
:::
""")


def restklassen_rechnen(rng):
    n = rng.randint(5, 12)
    a, b = rng.randint(1, n - 1), rng.randint(1, n - 1)
    art = rng.choice(["add", "inv", "viel"])
    if art == "add":
        while (a + b) % n == 0 or a + b < n:
            a, b = rng.randint(1, n - 1), rng.randint(1, n - 1)
        w = (a + b) % n
        frage = f"Berechne $[{a}]_{{{n}}} + [{b}]_{{{n}}}$ in $\\mathbb{{Z}}/{n}\\mathbb{{Z}}$ und gib den Vertreter $r \\in \\{{0, \\ldots, {n - 1}\\}}$ an."
        zeilen = [(f"({a} + {b}) \\bmod {n} = {w}", f"$[{a}]_{{{n}}} + [{b}]_{{{n}}} = [{a + b}]_{{{n}}} = [{w}]_{{{n}}}$")]
        falsch = [(a + b, f"Du hast nur addiert. Der Vertreter muss in $\\{{0, \\ldots, {n - 1}\\}}$ liegen: ${a + b} - {n} = {w}$."),
                  ((a - b) % n, "Das ist die Differenz. Gefragt ist die Summe.")]
        tipps = ["Addiere $a$ und $b$ wie in $\\mathbb{Z}$.", f"Nimm das Ergebnis modulo ${n}$.", f"${a} + {b} = {a + b}$."]
    elif art == "inv":
        w = (-a) % n
        frage = f"Bestimme das additive Inverse von $[{a}]_{{{n}}}$ in $\\mathbb{{Z}}/{n}\\mathbb{{Z}}$, also $-[{a}]_{{{n}}} = [r]_{{{n}}}$ mit $r \\in \\{{0, \\ldots, {n - 1}\\}}$."
        zeilen = [(f"(-{a}) \\bmod {n} = {w}", f"$[{a}]_{{{n}}}^{{-1}} = [-{a}]_{{{n}}} = [{w}]_{{{n}}}$"),
                  (f"({a} + {w}) \\bmod {n} = 0", "Probe: Summe ist das neutrale Element")]
        falsch = [(-a, f"Das ist der Vertreter $-{a}$, liegt aber nicht in $\\{{0, \\ldots, {n - 1}\\}}$. Rechne $-{a} + {n}$."),
                  (a, "Das ist $[a]_n$ selbst, nicht sein Inverses (außer wenn $2a \\equiv 0$).")]
        tipps = ["Gesucht ist $r$ mit $a + r \\equiv 0 \\pmod n$.", f"Rechne ${n} - {a}$.", f"${a} + {w} = {a + w}$ ist durch ${n}$ teilbar."]
    else:
        m = rng.randint(3, 9)
        w = (m * a) % n
        while w == (m * a) or w == 0:
            a, m = rng.randint(2, n - 1), rng.randint(3, 9)
            w = (m * a) % n
        frage = f"Berechne ${m} \\cdot [{a}]_{{{n}}} := [{a}]_{{{n}}} + \\ldots + [{a}]_{{{n}}}$ ({m} Summanden) in $\\mathbb{{Z}}/{n}\\mathbb{{Z}}$ und gib den Vertreter $r \\in \\{{0, \\ldots, {n - 1}\\}}$ an."
        zeilen = [(f"({m} \\cdot {a}) \\bmod {n} = {w}", f"$m$-fache Summe: ${m} \\cdot {a} = {m * a}$, Rest modulo ${n}$")]
        falsch = [(m * a, f"Du hast nicht modulo ${n}$ gerechnet. Der Vertreter liegt in $\\{{0, \\ldots, {n - 1}\\}}$."),
                  ((m + a) % n, "Das ist die Summe $m + a$, nicht die $m$-fache Summe von $a$.")]
        tipps = [f"Die $m$-fache Summe von $[a]_n$ ist $[m \\cdot a]_n$.", f"${m} \\cdot {a} = {m * a}$.", f"Rest von ${m * a}$ bei Division durch ${n}$."]
    return {"frage": frage, "loesung": w, "tipps": tipps, "rechenweg": rechnung(zeilen),
            "erklaerung": "Auf Restklassen wird auf Vertretern gerechnet und am Ende modulo $n$ reduziert (Beispiel 3.15).",
            "typische_fehler": ohne_gleiche(w, falsch)}



k.zuordnen("Ordne jede Struktur ihrem Befund zu (Beispiele 3.10 bis 3.15).",
           [("$(\\mathbb{Z}, +)$", "abelsche Gruppe mit neutralem Element $0$"),
            ("$(\\mathrm{perm}(\\{a, b, c\\}), \\circ)$", "Gruppe, nicht abelsch"),
            ("$(\\{0, 1\\}^n, \\oplus)$", "abelsche Gruppe, jedes Element ist selbstinvers"),
            ("$(\\mathcal{P}(M), \\cup)$ mit $M \\ne \\emptyset$", "keine Gruppe: keine Inversen"),
            ("$(\\mathbb{N}, +)$", "keine Gruppe: keine Inversen")],
           "Permutationen vertauschen nicht, $\\oplus$ ist selbstinvers, bei Vereinigung und $\\mathbb{N}$ fehlen die Inversen.",
           ablenker=["keine Gruppe: nicht assoziativ"],
           tipps=["Prüfe: Gibt es ein neutrales Element, gibt es zu jedem Element ein Inverses, ist es kommutativ?", "Bei $\\mathcal{P}(M)$ und $\\mathbb{N}$ scheitert dieselbe Eigenschaft."])

# ── Seite 8: Satz 3.16 ──────────────────────────────────────────────────
k.erklaerung("Satz 3.16: Gleichungen lösen, kürzen, invertieren", r"""
## Drei Folgerungen

**Satz 3.16.** Sei $(G, \ast)$ eine Gruppe und $a, b, c \in G$.

(i) $a \ast x = b$ und $x \ast a = b$ haben jeweils genau eine Lösung: $x = a^{-1} \ast b$ bzw. $x = b \ast a^{-1}$.
(ii) [[Kürzungsregeln]]: $a \ast b = a \ast c \Rightarrow b = c$ und $b \ast a = c \ast a \Rightarrow b = c$.
(iii) $(a \ast b)^{-1} = b^{-1} \ast a^{-1}$.

*Beweis (i).* $a \ast (a^{-1} \ast b) = (a \ast a^{-1}) \ast b = e \ast b = b$, also Lösung. Ist $y$ eine Lösung, dann $y = e \ast y = (a^{-1} \ast a) \ast y = a^{-1} \ast (a \ast y) = a^{-1} \ast b$.
(ii) folgt aus (i): $b$ und $c$ lösen dieselbe Gleichung $a \ast x = a \ast b$.

:::rechnung (iii) an $(\mathbb{Z}/6\mathbb{Z}, +)$ mit $a = [4]$, $b = [5]$
(4 + 5) \bmod 6 = 3 || $a \ast b = [4] + [5] = [9] = [3]$
(-3) \bmod 6 = 3 || $(a \ast b)^{-1} = [-3] = [3]$
(1 + 2) \bmod 6 = 3 || $b^{-1} + a^{-1} = [1] + [2] = [3]$: stimmt
:::

:::alt Als Socken und Schuhe
Zieht man erst Socken, dann Schuhe an ($a \ast b$), muss man erst die Schuhe ausziehen, dann die Socken ($b^{-1} \ast a^{-1}$).
Ein Inverses dreht die Reihenfolge um.
:::
""")

k.ordnen("Ordne den Beweis von Satz 3.16 (iii): $(a \\ast b)^{-1} = b^{-1} \\ast a^{-1}$ (erste Gleichung).",
         ["Wir zeigen $(a \\ast b) \\ast (b^{-1} \\ast a^{-1}) = e$.",
          "$(a \\ast b) \\ast (b^{-1} \\ast a^{-1}) = a \\ast ((b \\ast b^{-1}) \\ast a^{-1})$ nach (a).",
          "$a \\ast ((b \\ast b^{-1}) \\ast a^{-1}) = a \\ast (e \\ast a^{-1})$, denn $b \\ast b^{-1} = e$ (Satz 3.9).",
          "$a \\ast (e \\ast a^{-1}) = a \\ast a^{-1}$ nach (n).",
          "$a \\ast a^{-1} = e$ nach Satz 3.9. Analog $(b^{-1} \\ast a^{-1}) \\ast (a \\ast b) = e$; nach Eindeutigkeit des Inversen folgt die Behauptung."],
         "Du rechnest nach, dass $b^{-1} \\ast a^{-1}$ das Inverse von $a \\ast b$ ist, und benutzt die Eindeutigkeit aus Satz 3.9. Das Neutrale und das Inverse wirken dabei auch von rechts.",
         ablenker=["$(a \\ast b) \\ast (a^{-1} \\ast b^{-1}) = e$ nach Kommutativität."],
         tipps=["Zeige, dass $b^{-1} \\ast a^{-1}$ mit $a \\ast b$ verknüpft $e$ ergibt.", "Verschiebe Klammern, bis $b \\ast b^{-1}$ in der Mitte steht.", "Die Reihenfolge $a^{-1} \\ast b^{-1}$ wäre ohne Kommutativität falsch."])

k.mc("In einer Gruppe $(G, \\ast)$ gilt $a \\ast x = b$. Welche Aussage über $x$ ist richtig?",
     ["$x = a^{-1} \\ast b$", "$x = b \\ast a^{-1}$", "$x = b \\ast a$", "Es gibt im Allgemeinen mehrere Lösungen"],
     "Nach Satz 3.16 (i): Von links multiplizieren mit $a^{-1}$ gibt $x = a^{-1} \\ast b$. $b \\ast a^{-1}$ löst $x \\ast a = b$, nicht $a \\ast x = b$, und das ist im nicht abelschen Fall ein anderes Element.",
     tipps=["Multipliziere beide Seiten **von links** mit $a^{-1}$.", "Wo steht $a$ in der Gleichung: vor oder nach dem $x$?"],
     fehler={"$x = b \\ast a^{-1}$": "Das löst $x \\ast a = b$. In einer nicht abelschen Gruppe steht $a^{-1}$ auf der Seite, auf der $a$ stand.",
             "$x = b \\ast a$": "Dann wäre $a \\ast (b \\ast a) = b$ nötig. Du hast nicht invertiert.",
             "Es gibt im Allgemeinen mehrere Lösungen": "Satz 3.16 (i): Es gibt genau **eine** Lösung."})

k.wf("In jeder Gruppe gilt $(a \\ast b)^{-1} = a^{-1} \\ast b^{-1}$.", False,
     "Richtig ist $(a \\ast b)^{-1} = b^{-1} \\ast a^{-1}$ (Satz 3.16 (iii)). Gegenbeispiel in einer nicht abelschen Gruppe: Permutationen, bei denen $a^{-1} \\ast b^{-1} \\ne b^{-1} \\ast a^{-1}$. In abelschen Gruppen stimmen beide Formen überein.",
     tipps=["Denke an Socken und Schuhe: Was musst du zuerst ausziehen?"])

# ── Seite 9: Satz 3.17 und Def. 3.18 ────────────────────────────────────
k.erklaerung("Satz 3.17 und Definition 3.18", r"""
## Inverse des Inversen, leere Summe

**Satz 3.17.** In jeder Gruppe gilt $e^{-1} = e$ und $(a^{-1})^{-1} = a$.

*Beweis.* $e \ast e = e$, also ist $e$ sein eigenes Inverses. Nach Satz 3.9 gilt $g \ast g^{-1} = e$, also ist $g$ ein Inverses zu $g^{-1}$.
Die Eindeutigkeit des Inversen gibt $(g^{-1})^{-1} = g$. $\square$

**Definition 3.18.** In einer additiv geschriebenen Gruppe $(G, +)$ ist die [[leere Summe|leere Summe]] $\sum_{j=i}^{m}$ mit $m < i$ das neutrale Element $0$.

:::rechnung In $(\mathbb{Z}/7\mathbb{Z}, +)$
(-3) \bmod 7 = 4 || $[3]^{-1} = [4]$
(-4) \bmod 7 = 3 || $([3]^{-1})^{-1} = [4]^{-1} = [3]$: zurück zum Start
\sum_{j=1}^{0} j = 0 || leere Summe ist das neutrale Element $0$
:::

:::alt Als Umschalten
Zweimal „umkehren“ bringt dich dorthin zurück, wo du gestartet bist: Spiegelst du ein Bild zweimal, bekommst du das Original.
Der Nullzustand „nichts getan“ ist das Ergebnis einer Summe ohne Summanden.
:::
""")

k.luecke("Löse in $(\\mathbb{Z}/7\\mathbb{Z}, +)$ die Gleichung $[3]_7 + x = [2]_7$ mit $x = [-3]_7 + [2]_7$. Fülle die Lücken.",
         "x = [-3]_7 + [2]_7 = [\\luecke]_7 + [2]_7 = [\\luecke]_7",
         [[4], [6]],
         "$-3 \\equiv 4 \\pmod 7$, also $x = [4]_7 + [2]_7 = [6]_7$. Probe: $3 + 6 = 9 \\equiv 2$.",
         tipps=["Rechne $-3 \\bmod 7$ aus.", "$-3 + 7 = 4$.", "$4 + 2 = 6$."],
         rechenweg=rechnung([("(-3) \\bmod 7 = 4", "$-3 = (-1) \\cdot 7 + 4$"), ("(4 + 2) \\bmod 7 = 6", "Summe"), ("(3 + 6) \\bmod 7 = 2", "Probe")]),
         typische_fehler=[([-3, -1], "Du hast nicht auf den Vertreter in $\\{0, \\ldots, 6\\}$ reduziert. $[-3]_7 = [4]_7$.")])

k.praxis()

k.generator(gruppe_tafel_pruefen, typ="mc", titel="Verknüpfungstafel: Gruppe oder nicht?")
k.generator(perm_verkettung, typ="vektor", titel="Permutationen verketten")
k.generator(bitgruppe_xor, typ="vektor", titel="Bitgruppe: XOR rechnen")
k.generator(restklassen_rechnen, typ="zahl", titel="Rechnen in Z/nZ")

k.rechenweg_aufgabe(r"""
## Quiz-Stil: Rechnen in $(\mathbb{Z}/6\mathbb{Z}, +)$

Gegeben ist die Gruppe $(\mathbb{Z}/6\mathbb{Z}, +)$ mit $G = \{[0], [1], \ldots, [5]\}$ (Index $6$ weggelassen).
""",
    [{"typ": "zahl", "frage": "Bestimme $r \\in \\{0, \\ldots, 5\\}$ mit $[4] + [5] = [r]$.", "loesung": 3,
      "tipps": ["$4 + 5 = 9$.", "$9 \\bmod 6$."], "rechenweg": ":::rechnung\n(4 + 5) \\bmod 6 = 3 || Summe, Rest modulo 6\n:::",
      "erklaerung": "$9 = 1 \\cdot 6 + 3$."},
     {"typ": "zahl", "frage": "Bestimme $r$ mit $[4]^{-1} = [r]$ in $(\\mathbb{Z}/6\\mathbb{Z}, +)$.", "loesung": 2,
      "tipps": ["Gesucht: $r$ mit $4 + r \\equiv 0 \\pmod 6$.", "$6 - 4$."], "rechenweg": ":::rechnung\n(4 + 2) \\bmod 6 = 0 || $[4] + [2] = [0]$\n:::",
      "erklaerung": "$[4] + [2] = [0]$, also ist $[2]$ das Inverse.", "typische_fehler": [(4, "$[4] + [4] = [2] \\ne [0]$. In $\\mathbb{Z}/6\\mathbb{Z}$ ist nicht jedes Element selbstinvers.")]},
     {"typ": "zahl", "frage": "Löse $[5] + x = [1]$ und gib $r \\in \\{0, \\ldots, 5\\}$ mit $x = [r]$ an (Satz 3.16 (i)).", "loesung": 2,
      "tipps": ["$x = [5]^{-1} + [1]$.", "$[5]^{-1} = [1]$."], "rechenweg": ":::rechnung\n(-5 + 1) \\bmod 6 = 2 || $x = a^{-1} + b$\n(5 + 2) \\bmod 6 = 1 || Probe\n:::",
      "erklaerung": "$x = [1] + [1] = [2]$."}],
    "Die Gruppe $\\mathbb{Z}/6\\mathbb{Z}$ ist abelsch, Inverse und Lösungen von $a + x = b$ liest du mit $-a + b$ ab.",
    uebungsblatt=True,
    tipps=["Rechne immer mit Vertretern in $\\{0, \\ldots, 5\\}$.", "Das Inverse von $[a]$ ist $[-a] = [6 - a]$."],
    rechenweg=r"""
:::rechnung
(4 + 5) \bmod 6 = 3 || Summe
(-4) \bmod 6 = 2 || $[4]^{-1} = [-4] = [2]$
(-5 + 1) \bmod 6 = 2 || $x = [-5] + [1] = [1] + [1]$
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Eine Gruppe auf ℤ

Auf $\mathbb{Z}$ sei $a \ast b := a + b + 1$. Zeigen Sie, dass $(\mathbb{Z}, \ast)$ eine abelsche Gruppe ist. Bestimmen Sie das neutrale Element und das Inverse von $a \in \mathbb{Z}$.
""",
    r"""
**(a)** $(a \ast b) \ast c = (a + b + 1) + c + 1 = a + b + c + 2$ und $a \ast (b \ast c) = a + (b + c + 1) + 1 = a + b + c + 2$.
**(n)** Gesucht $e$ mit $e \ast a = a$: $e + a + 1 = a \iff e = -1$. Das neutrale Element ist $e = -1$ (und $a \ast (-1) = a$ auch).
**(i)** Gesucht $b$ mit $b \ast a = -1$: $b + a + 1 = -1 \iff b = -a - 2$. Das Inverse zu $a$ ist $-a - 2 \in \mathbb{Z}$. Probe: $(-a - 2) \ast a = -a - 2 + a + 1 = -1$.
**(k)** $a \ast b = a + b + 1 = b + a + 1 = b \ast a$. Also abelsch. $\square$
""",
    ["Assoziativität durch Ausrechnen beider Klammerungen gezeigt",
     "Neutrales Element $e = -1$ aus der Gleichung $e \\ast a = a$ bestimmt",
     "Inverses $-a - 2$ bestimmt und in $\\mathbb{Z}$ liegend begründet",
     "Kommutativität gezeigt (abelsch)"],
    "Neutrales Element und Inverses musst du nicht erraten: Löse die Axiomgleichung $e \\ast a = a$ bzw. $b \\ast a = e$ nach $e$ bzw. $b$.",
    uebungsblatt=True,
    tipps=["Rechne bei (a) beide Seiten getrennt aus und vergleiche.", "Für (n) löse $e + a + 1 = a$ nach $e$.", "Für (i) löse $b + a + 1 = e$ mit dem gefundenen $e$."])

k.papier(r"""
## Übungsblatt-Stil: Selbstinverse Elemente

Sei $(G, \ast)$ eine Gruppe mit $a \ast a = e$ für alle $a \in G$. Zeigen Sie, dass $G$ abelsch ist. (Hinweis: Satz 3.16 (iii).)
""",
    r"""
Aus $a \ast a = e$ folgt $a^{-1} = a$ für jedes $a \in G$ (Eindeutigkeit des Inversen, Satz 3.9).
Seien $a, b \in G$. Dann ist $a \ast b \in G$ und daher $(a \ast b)^{-1} = a \ast b$.
Nach Satz 3.16 (iii) ist $(a \ast b)^{-1} = b^{-1} \ast a^{-1} = b \ast a$.
Zusammen: $a \ast b = (a \ast b)^{-1} = b \ast a$. Also ist $G$ abelsch. $\square$
""",
    ["Erkannt: $a \\ast a = e$ heißt $a^{-1} = a$ für **jedes** Element",
     "Auch $a \\ast b$ als Element der Gruppe selbstinvers genutzt",
     "Satz 3.16 (iii) richtig angewendet: $(a \\ast b)^{-1} = b^{-1} \\ast a^{-1}$",
     "Beide Ausdrücke gleichgesetzt: $a \\ast b = b \\ast a$"],
    "Selbstinverse Elemente zusammen mit der Umkehrregel $(a \\ast b)^{-1} = b^{-1} \\ast a^{-1}$ erzwingen Kommutativität. Das gilt für die Bitgruppe $B_n$.",
    uebungsblatt=True,
    tipps=["Was bedeutet $a \\ast a = e$ für $a^{-1}$?", "Wende die Voraussetzung auch auf das Element $a \\ast b$ an.", "Nutze Satz 3.16 (iii) für $(a \\ast b)^{-1}$."])

k.papier(r"""
## Beweis: Kürzungsregel aus Satz 3.16 (ii)

Zeigen Sie: Aus $b \ast a = c \ast a$ in einer Gruppe $(G, \ast)$ folgt $b = c$. Benutzen Sie dabei nur die Axiome und Satz 3.9.
""",
    r"""
Multiplikation von rechts mit $a^{-1}$: $(b \ast a) \ast a^{-1} = (c \ast a) \ast a^{-1}$.
Mit (a): $b \ast (a \ast a^{-1}) = c \ast (a \ast a^{-1})$. Mit Satz 3.9 ($a \ast a^{-1} = e$): $b \ast e = c \ast e$.
Mit Satz 3.9 ($x \ast e = x$): $b = c$. $\square$
""",
    ["Von rechts mit $a^{-1}$ verknüpft (nicht von links)",
     "Mit Assoziativität die Klammer verschoben",
     "$a \\ast a^{-1} = e$ und $b \\ast e = b$ aus Satz 3.9 begründet (rechte Wirkung)"],
    "Hier brauchst du Satz 3.9: Inverse und Neutrales wirken auch von rechts.",
    tipps=["Für $b \\ast a = c \\ast a$ verknüpfst du beide Seiten mit $a^{-1}$ auf der rechten Seite."])

k.zusammenfassung(r"""
## Gruppen (Skript Abschn. 3.2, Def. 3.8 bis Def. 3.18)

- **Gruppe** (Def. 3.8): $(G, \ast)$, $G \ne \emptyset$, $\ast\colon G^2 \to G$ mit (a) $a \ast (b \ast c) = (a \ast b) \ast c$, (n) $e \ast a = a$, (i) zu jedem $a$ ein $b$ mit $b \ast a = e$. **Abelsch:** zusätzlich (k) $a \ast b = b \ast a$.
- **Satz 3.9:** $e$ und $a^{-1}$ sind eindeutig; $a \ast e = a$ und $a \ast a^{-1} = e$ gelten auch von rechts.
- **Beispiele:** 3.10 $(\mathbb{Z}, +)$; 3.11 $(\{-1, 1\}, \cdot)$; 3.12 $(\mathcal{P}(M), \cup)$ keine Gruppe; 3.13 $(\mathrm{perm}(M), \circ)$ nicht abelsch; 3.14 Bitgruppe $B_n = (\{0, 1\}^n, \oplus)$ mit $x \oplus x = 0$; 3.15 $(\mathbb{Z}/n\mathbb{Z}, +)$, $[a]_n + [b]_n = [a + b]_n$.
- **Satz 3.16:** (i) $a \ast x = b$ hat genau die Lösung $x = a^{-1} \ast b$ (analog $x \ast a = b$); (ii) Kürzungsregeln; (iii) $(a \ast b)^{-1} = b^{-1} \ast a^{-1}$.
- **Satz 3.17:** $e^{-1} = e$, $(a^{-1})^{-1} = a$. **Def. 3.18:** Die leere Summe in $(G, +)$ ist $0$.

!! Beweise in Gruppen: nur (a), (n), (i), Satz 3.9 und Satz 3.16 benutzen, nie Kommutativität.
""")
