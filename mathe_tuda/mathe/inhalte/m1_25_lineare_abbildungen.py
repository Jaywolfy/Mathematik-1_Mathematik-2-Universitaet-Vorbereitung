# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 25: Lineare Abbildungen, Kern, Bild und Rang (Skript Disser WS 26/27, Abschn. 5.1 und 5.2, Def. 5.1 bis Bsp. 5.26)."""
import re
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche
from .glossar import finden

k = neues_kapitel(
    slug="lineare_abbildungen",
    titel="Lineare Abbildungen, Kern, Bild und Rang",
    beschreibung="Linearität, Basisbilder, Hom(V,W), Kern, Bild, Rang, Urbilder, Dimensionsformel, Isomorphie",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 5.1 und 5.2",
    icon="🔀")


# ── Hilfsfunktionen ─────────────────────────────────────────────────────────
def G(text):
    """<<Anzeige|Begriff>> wird zum Glossar-Link, falls der Begriff schon im Glossar steht (Kapitel 4 entsteht parallel)."""
    def ers(m):
        inhalt = m.group(1)
        anzeige, _, name = inhalt.rpartition("|")
        if finden(name.strip()):
            return f"[[{inhalt}]]"
        return anzeige or name
    return re.sub(r"<<(.+?)>>", ers, text)


def vt(v):
    return mathlib.tex_vektor(v)


def mt(m):
    return mathlib.tex_matrix(m)


def R(zeilen, titel="", frei=False):
    """:::rechnung aus (tex, grund)-Paaren. frei=True: Zeilen werden nicht nachgerechnet (Vektoren, Beweistext)."""
    p = "?? " if frei else ""
    kopf = ":::rechnung" + (f" {titel}" if titel else "")
    return kopf + "\n" + "\n".join(f"{p}{t} || {g}" for t, g in zeilen) + "\n:::"


def anwenden(A, v):
    return mathlib.mat_vec(A, v)


def ganz(v):
    """Primitiver ganzzahliger Vektor in Richtung von v."""
    v = [F(x) for x in v]
    nenner = 1
    for x in v:
        nenner = nenner * x.denominator // mathlib.ggt(nenner, x.denominator)
    w = [int(x * nenner) for x in v]
    g = 0
    for x in w:
        g = mathlib.ggt(g, abs(x))
    return [x // g for x in w] if g else w


# ── Nachgerechnet beim Laden ───────────────────────────────────────────────
_A1 = [[2, 1], [1, -1]]                             # f(x, y) = (2x + y, x - y)
_v, _w = [1, 2], [3, -1]
assert anwenden(_A1, _v) == [4, -1] and anwenden(_A1, _w) == [5, 4]
assert anwenden(_A1, [4, 1]) == [9, 3] and anwenden(_A1, [3, 6]) == [12, -3]
assert (2 * 3) ** 2 == 36 and 2 * 3 ** 2 == 18
# Beispiel 5.22 und 5.34: f(x, y, z) = (x + y, z), Matrix (1 1 0 / 0 0 1)
_A22 = [[1, 1, 0], [0, 0, 1]]
assert mathlib.rang(_A22) == 2 and mathlib.kern(_A22) == [[-1, 1, 0]] and anwenden(_A22, [2, 0, 5]) == [2, 5]
# Projektion auf <(1, 1)> und Spiegelung (Bsp. 5.16, 5.12)
_P = [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]
assert anwenden(_P, [2, 1]) == [F(3, 2), F(3, 2)] and mathlib.rang(_P) == 1
assert [2 * a - b for a, b in zip(anwenden(_P, [2, 1]), [2, 1])] == [1, 2]
assert [x for x in mathlib.kern(_P)] == [[F(-1), F(1)]]
# Satz 5.9, Beispiel: Basis b1 = (1, 1), b2 = (1, 0); f(b1) = (2, 0), f(b2) = (1, 3); x = (2, 1) = 1 b1 + 1 b2
assert [1 * 1 + 1 * 1, 1 * 1 + 1 * 0] == [2, 1] and [1 * 2 + 1 * 1, 1 * 0 + 1 * 3] == [3, 3]
# Satz 5.8, Beispiel
assert [2 * 1 - 0 + 3 * 2, 2 * 0 - 1 + 3 * 1] == [8, 2]
# Funktionenraum Bsp. 5.4: f(t) = 3 + 2t hat Koordinaten (3, 2)
# Bsp. 5.12: s = 2 pi - id wirkt als (x, y) -> (y, x)
assert all([2 * a - b for a, b in zip(anwenden(_P, v), v)] == [v[1], v[0]] for v in ([2, 1], [1, 0], [0, 1], [3, -5]))

k.lernziele([
    "Ich kann prüfen, ob eine Abbildung zwischen Vektorräumen linear ist, und Gegenbeispiele angeben (Def. 5.1, Bsp. 5.2 bis 5.7)",
    "Ich kann eine lineare Abbildung aus den Bildern einer Basis berechnen und weiß, warum sie dadurch festliegt (Satz 5.8, 5.9)",
    "Ich kann Kern, Bild und Rang bestimmen und Urbilder als $v^{(0)} + \\ker(f)$ beschreiben (Satz 5.14, Def. 5.15, Satz 5.18)",
    "Ich kann die Dimensionsformel $\\dim V = \\dim \\ker(f) + \\mathrm{rang}(f)$ anwenden und erklären (Satz 5.20, 5.23, Kor. 5.25)",
])

k.warum(r"""
Jede Transformation in der Computergrafik (Drehen, Skalieren, Spiegeln, Projizieren) ist eine lineare Abbildung,
und jede Schicht eines neuronalen Netzes beginnt mit einer. Linear heißt: Du musst nur wissen, was mit den
Basisvektoren passiert, der Rest folgt. Der Kern sagt, welche Information beim Berechnen verloren geht,
das Bild, welche Ausgaben überhaupt vorkommen. Die Dimensionsformel ist die Buchhaltung dazu:
Was der Kern verschluckt, fehlt im Bild. Verlustfreie Kompression verlangt Kern $= \{0\}$.
""")

# ── Seite 1: Definition 5.1 ─────────────────────────────────────────────────
k.erklaerung("Definition 5.1: linear", G(r"""
## Was linear heißt

:::analogie 💱 Währungsrechner
Ein Wechselkurs ist linear. Zwei Preise einzeln umrechnen und addieren gibt dasselbe wie erst addieren und dann
umrechnen. Der doppelte Preis ergibt den doppelten Betrag.
:::

**Definition 5.1.** Eine Abbildung $f\colon V \to W$ zwischen <<Vektorräumen|Vektorraum>> über demselben [[Körper]] $K$ heißt
[[lineare Abbildung]] (Vektorraumhomomorphismus), falls für alle $v, w \in V$ und $\lambda \in K$ gilt:
$$f(v + w) = f(v) + f(w) \quad\text{und}\quad f(\lambda \cdot v) = \lambda \cdot f(v).$$
Ein bijektiver Homomorphismus heißt [[Isomorphismus]], einer von $V$ nach $V$ Automorphismus.
Beide Bedingungen zusammen besagen $f(\lambda v + \mu w) = \lambda f(v) + \mu f(w)$.

""") + R([
    (r"f\begin{pmatrix}x\\y\end{pmatrix} = \begin{pmatrix}2x + y\\x - y\end{pmatrix}", "unser Beispiel $f\\colon \\mathbb{R}^2 \\to \\mathbb{R}^2$"),
    (r"v + w = \begin{pmatrix}1\\2\end{pmatrix} + \begin{pmatrix}3\\-1\end{pmatrix} = \begin{pmatrix}4\\1\end{pmatrix}", "erst addieren"),
    (r"f(v + w) = \begin{pmatrix}2 \cdot 4 + 1\\4 - 1\end{pmatrix} = \begin{pmatrix}9\\3\end{pmatrix}", "dann abbilden"),
    (r"f(v) + f(w) = \begin{pmatrix}4\\-1\end{pmatrix} + \begin{pmatrix}5\\4\end{pmatrix} = \begin{pmatrix}9\\3\end{pmatrix}", "erst abbilden, dann addieren: gleich"),
    (r"f(3v) = \begin{pmatrix}12\\-3\end{pmatrix} = 3 \begin{pmatrix}4\\-1\end{pmatrix} = 3 f(v)", "auch die Skalarmultiplikation passt"),
], "Beide Bedingungen an einem Beispiel (kein Beweis, nur ein Test)", frei=True) + G(r"""

:::alt Als Fotokopierer
Ein linearer Kopierer vergrößert jedes Bild um denselben Faktor und legt Überlagerungen zweier Vorlagen
genauso übereinander wie die Originale. Eine Abbildung, die bei Überlagerung etwas Neues erfindet,
ist nicht linear.
:::
"""))

k.mc("Welche Aussage über $f\\colon V \\to W$ ist gleichwertig dazu, dass $f$ linear ist?",
     ["$f(\\lambda v + \\mu w) = \\lambda f(v) + \\mu f(w)$ für alle $v, w \\in V$ und $\\lambda, \\mu \\in K$",
      "$f(v \\cdot w) = f(v) \\cdot f(w)$ für alle $v, w \\in V$",
      "$f(v + w) = f(v) + f(w)$ für alle $v, w \\in V$ (Skalare sind egal)",
      "$f$ ist bijektiv"],
     "Das Skript begründet es nach Def. 5.1: Die beiden Bedingungen zusammen bedeuten genau, dass Linearkombinationen zweier Vektoren erhalten bleiben. "
     "Ein Produkt $v \\cdot w$ gibt es in einem Vektorraum gar nicht.",
     tipps=["Linear verlangt zwei Dinge: Addition und Skalarmultiplikation.", "Eine einzige Gleichung kann beides gleichzeitig ausdrücken, wenn sie eine Linearkombination enthält."],
     fehler={"$f(v \\cdot w) = f(v) \\cdot f(w)$ für alle $v, w \\in V$": "Das wäre ein Homomorphismus für ein Produkt. Im Vektorraum gibt es kein Produkt zweier Vektoren, nur Summe und Skalarmultiplikation.",
             "$f(v + w) = f(v) + f(w)$ für alle $v, w \\in V$ (Skalare sind egal)": "Die Verträglichkeit mit der Skalarmultiplikation, $f(\\lambda v) = \\lambda f(v)$, fehlt. Beide Bedingungen sind Teil von Def. 5.1.",
             "$f$ ist bijektiv": "Bijektiv ist nur für Isomorphismen verlangt. Die Nullabbildung ist linear und nicht bijektiv."})

# ── Seite 2: Beispiele 5.2, 5.3, 5.6 ────────────────────────────────────────
k.erklaerung("Linear oder nicht: Beispiele 5.2, 5.3, 5.6", G(r"""
## Beispiele und Gegenbeispiele

- **Streckung** $s_\alpha\colon V \to V,\ v \mapsto \alpha v$ ist linear (Bsp. 5.2), für $\alpha \neq 0$ sogar ein Automorphismus.
- **Nullabbildung** $v \mapsto 0_W$ ist linear. Eine konstante Abbildung mit Wert $w \neq 0_W$ nicht, denn $f(0 \cdot v) = w \neq 0 = 0 \cdot f(v)$ (Bsp. 5.3).
- **Verschiebung** $\tau_a\colon v \mapsto v + a$ mit $a \neq 0_V$ ist nicht linear (Bsp. 5.6): Das Skript nutzt dafür den Skalar $0$.
- Für lineares $f\colon \mathbb{R} \to \mathbb{R}$ gilt $f(x) = x \cdot f(1)$. Der Graph ist eine Gerade durch den Ursprung.

:::achtung f(0) = 0 ist nur ein Vortest
Aus $f(0) \neq 0$ folgt: nicht linear. Aus $f(0) = 0$ folgt noch nichts: $x \mapsto x^2$ hat $f(0) = 0$ und ist trotzdem nicht linear.
:::

""") + R([
    (r"f(0) = 0 + 1 = 1", r"$f(x) = x + 1$: Der Nullvektor geht nicht auf null, also nicht linear (Satz 5.8)"),
    (r"(2 \cdot 3)^2 = 36", r"$g(x) = x^2$: $g(2 \cdot 3)$ mit $\lambda = 2$, $v = 3$"),
    (r"2 \cdot 3^2 = 18", r"$2 \cdot g(3)$: $36 \neq 18$, also verletzt $x^2$ die Skalarmultiplikation"),
    (r"f(5) = 5 \cdot f(1) = 5 \cdot 4 = 20", r"jedes lineare $f\colon \mathbb{R} \to \mathbb{R}$ mit $f(1) = 4$ ist $x \mapsto 4x$"),
], "Vier Tests", frei=True) + G(r"""

:::alt Als Gummiband
Eine lineare Abbildung dehnt und dreht das ganze Koordinatennetz, hält aber den Ursprung fest und lässt Geraden
gerade. Eine Verschiebung reißt den Ursprung mit, eine Quadrierung krümmt das Netz.
:::
"""))

_f_lin = [
    "$f\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto 5x$",
    "$g\\colon \\mathbb{R}^2 \\to \\mathbb{R},\\ (x, y)^\\top \\mapsto x - 3y$",
    "$s\\colon \\mathbb{R}^2 \\to \\mathbb{R}^2,\\ v \\mapsto 7v$",
    "die Nullabbildung $\\mathbb{R}^3 \\to \\mathbb{R}^2$",
]
k.mehrfach("Welche dieser Abbildungen sind linear?", _f_lin,
           ["$h\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto x + 1$",
            "$q\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto x^2$",
            "$\\tau\\colon \\mathbb{R}^2 \\to \\mathbb{R}^2,\\ v \\mapsto v + (1, 0)^\\top$"],
           "Linear sind Streckungen, Linearkombinationen der Koordinaten und die Nullabbildung. Bei $x + 1$ und der Verschiebung geht $0$ nicht auf $0$, "
           "bei $x^2$ gilt $q(2 \\cdot 3) = 36 \\neq 18 = 2 \\cdot q(3)$.",
           tipps=["Teste zuerst $f(0) = 0$.", "Rechne $f(2v)$ und $2f(v)$ für eine konkrete Zahl aus.", "Linear sind genau die Abbildungen ohne konstanten Summanden und ohne Potenzen oder Produkte der Koordinaten."],
           fehler={"$h\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto x + 1$": "$h(0) = 1 \\neq 0$. Eine lineare Abbildung hat immer $f(0_V) = 0_W$.",
                   "$q\\colon \\mathbb{R} \\to \\mathbb{R},\\ x \\mapsto x^2$": "$q(2 \\cdot 3) = 36$, aber $2 \\cdot q(3) = 18$.",
                   "$\\tau\\colon \\mathbb{R}^2 \\to \\mathbb{R}^2,\\ v \\mapsto v + (1, 0)^\\top$": "Eine Verschiebung um $a \\neq 0$ ist nicht linear (Bsp. 5.6): $\\tau(0) = a \\neq 0$."})

k.zahl("$f\\colon \\mathbb{R} \\to \\mathbb{R}$ sei linear mit $f(1) = 4$. Berechne $f(7)$.", 28,
       "Für lineares $f\\colon \\mathbb{R} \\to \\mathbb{R}$ gilt $f(x) = x \\cdot f(1)$, hier $f(7) = 7 \\cdot 4 = 28$.",
       tipps=["Schreibe $7$ als Vielfaches von $1$.", "Nutze $f(\\lambda v) = \\lambda f(v)$ mit $\\lambda = 7$ und $v = 1$.", "$f(7) = 7 \\cdot f(1)$."],
       rechenweg=r"""
:::rechnung
?? f(7) = f(7 \cdot 1) || $7 = 7 \cdot 1$
?? = 7 \cdot f(1) || Skalarmultiplikation
?? = 7 \cdot 4 = 28 || $f(1) = 4$ einsetzen
:::
""",
       typische_fehler=[(11, "Das wäre $7 + f(1)$. Linear heißt: $f(7 \\cdot 1) = 7 \\cdot f(1)$, nicht plus."),
                        (4, "$f(1) = 4$ ist gegeben. Gesucht ist $f(7)$, und das Skalar $7$ kommt als Faktor heraus.")])

# ── Seite 3: Beispiele 5.4, 5.5, 5.7 ────────────────────────────────────────
k.erklaerung("Beispiele 5.4, 5.5, 5.7: Koordinaten, Projektion, Konjugation", G(r"""
## Drei Beispiele aus dem Skript

- **Koordinaten** (Bsp. 5.4): Im Funktionenraum $\mathcal{F}$ der Funktionen $t \mapsto a + bt$ ist $\kappa\colon f \mapsto (a, b)^\top$ linear und bijektiv, also ein Isomorphismus $\mathcal{F} \to \mathbb{R}^2$.
- **Orthogonalprojektion** (Bsp. 5.5): $v = u + w$ mit $u \in U$, $w \in U^\perp$ ist eindeutig, daher gilt $\pi_U(\alpha v + \beta v') = \alpha \pi_U(v) + \beta \pi_U(v')$.
- **Konjugation** $c\colon z \mapsto \bar z$ (Bsp. 5.7): über $\mathbb{R}$ linear, über $\mathbb{C}$ nicht. Die Multiplikation $m_z\colon w \mapsto zw$ ist über beiden linear.

:::visual vektoren2d
{"vektoren": [{"x": "3/2", "y": "3/2", "label": "u"}, {"x": "1/2", "y": "-1/2", "label": "w"}], "zeige": ["summe"],
 "unterschrift": "$v = (2, 1)^\\top = u + w$ mit $u \\in G = \\langle (1, 1)^\\top \\rangle$ und $w \\perp G$: die eindeutige Zerlegung aus Bsp. 5.5."}
:::

""") + R([
    (r"\kappa(3 + 2t) = \begin{pmatrix}3\\2\end{pmatrix}", "Koeffizient vor $1$, dann vor $t$"),
    (r"c(i \cdot 1) = \overline{i} = -i", "über $\\mathbb{C}$ wäre $\\lambda = i$ erlaubt"),
    (r"i \cdot c(1) = i \cdot 1 = i", "$-i \\neq i$: über $\\mathbb{C}$ nicht linear. Mit reellem $\\lambda$ geht es."),
], "Koordinaten und Konjugation", frei=True) + G(r"""

:::alt Als Dolmetscher
$\kappa$ übersetzt eine Funktion in ihr Zahlenpaar und verliert nichts. Die Projektion wirft den senkrechten Anteil weg,
die Konjugation spiegelt die komplexe Ebene. Welche Zahlen als Faktoren erlaubt sind, bestimmt der Körper des Raums.
:::
"""))

k.mc("Welche Aussage über die Konjugation $c\\colon \\mathbb{C} \\to \\mathbb{C},\\ z \\mapsto \\bar z$ stimmt (Bsp. 5.7)?",
     ["Sie ist linear als Abbildung reeller Vektorräume, aber nicht als Abbildung komplexer Vektorräume",
      "Sie ist linear als Abbildung komplexer Vektorräume, aber nicht als Abbildung reeller Vektorräume",
      "Sie ist weder über $\\mathbb{R}$ noch über $\\mathbb{C}$ linear",
      "Sie ist über $\\mathbb{R}$ und über $\\mathbb{C}$ linear"],
     "$\\overline{z + w} = \\bar z + \\bar w$ und $\\overline{\\lambda z} = \\lambda \\bar z$ gelten für reelles $\\lambda$. Für $\\lambda = i$ gilt aber $c(i \\cdot 1) = -i \\neq i = i \\cdot c(1)$. "
     "Die Linearität hängt also vom Skalarkörper ab.",
     tipps=["Teste die Skalarmultiplikation mit $\\lambda = i$ und $z = 1$.", "$\\overline{i \\cdot 1} = \\bar i = -i$, aber $i \\cdot \\bar 1 = i$."],
     fehler={"Sie ist linear als Abbildung komplexer Vektorräume, aber nicht als Abbildung reeller Vektorräume": "Genau umgekehrt: Für reelle $\\lambda$ ist $\\overline{\\lambda z} = \\lambda \\bar z$, nur $\\lambda = i$ macht Probleme.",
             "Sie ist weder über $\\mathbb{R}$ noch über $\\mathbb{C}$ linear": "Über $\\mathbb{R}$ ist sie linear: Nach Satz 3.103 gilt $\\overline{z + w} = \\bar z + \\bar w$ und $\\overline{\\lambda z} = \\lambda \\bar z$ für reelles $\\lambda$.",
             "Sie ist über $\\mathbb{R}$ und über $\\mathbb{C}$ linear": "Mit $\\lambda = i$ und $z = 1$: $c(i) = -i$, aber $i \\cdot c(1) = i$. Über $\\mathbb{C}$ ist $c$ nicht linear."})

k.vektor("Die Abbildung $\\kappa\\colon \\mathcal{F} \\to \\mathbb{R}^2$ ordnet $f(t) = a + bt$ den Vektor $(a, b)^\\top$ zu (Bsp. 5.4). Bestimme $\\kappa(f)$ für $f(t) = 3 - 5t$.",
         [3, -5],
         "Der Koordinatenvektor bezüglich der Basis $(1, t)$ hat zuerst den konstanten Anteil $a = 3$, dann den Faktor vor $t$, also $b = -5$.",
         tipps=["Lies $a$ und $b$ aus $f(t) = a + bt$ ab.", "$a$ ist der konstante Summand, $b$ der Faktor von $t$.", "$a = 3$, und beim $t$ steht $-5$."],
         rechenweg=R([(r"3 - 5t = 3 \cdot 1 + (-5) \cdot t", "nach der Basis $(1, t)$ sortiert"), (r"\kappa(f) = (3, -5)^\top", "die Koeffizienten werden zum Vektor")], frei=True),
         typische_fehler=[([-5, 3], "Die Reihenfolge ist durch die geordnete Basis $(1, t)$ festgelegt: zuerst der Anteil von $1$, dann der von $t$.")])

# ── Seite 4: Satz 5.8 ───────────────────────────────────────────────────────
k.erklaerung("Satz 5.8: Linearkombinationen bleiben erhalten", G(r"""
## Satz 5.8

Für jede lineare Abbildung $f\colon V \to W$ gilt $f(0_V) = 0_W$, $f(-v) = -f(v)$ und für alle $m \in \mathbb{N}$,
$v^{(1)}, \dots, v^{(m)} \in V$, $\lambda_1, \dots, \lambda_m \in K$
$$f\Big(\sum_{j=1}^m \lambda_j v^{(j)}\Big) = \sum_{j=1}^m \lambda_j f(v^{(j)}).$$
Umgekehrt ist jede Abbildung, die alle endlichen Linearkombinationen erhält, linear.

*Beweis.* Die ersten beiden Gleichungen folgen aus Satz 3.38, weil $f$ ein Gruppenhomomorphismus ist.
Die Summenformel folgt per Induktion über $m$. Umgekehrt liefert $m = 1$ die Skalarmultiplikation, $m = 2$ mit $\lambda_1 = \lambda_2 = 1$ die Addition. $\square$

""") + R([
    (r"f(v^{(1)}) = \begin{pmatrix}1\\0\end{pmatrix},\ f(v^{(2)}) = \begin{pmatrix}0\\1\end{pmatrix},\ f(v^{(3)}) = \begin{pmatrix}2\\1\end{pmatrix}", "drei bekannte Bilder"),
    (r"f(2v^{(1)} - v^{(2)} + 3v^{(3)}) = 2\begin{pmatrix}1\\0\end{pmatrix} - \begin{pmatrix}0\\1\end{pmatrix} + 3\begin{pmatrix}2\\1\end{pmatrix}", "Satz 5.8: Koeffizienten bleiben, nur die Vektoren werden ersetzt"),
    (r"= \begin{pmatrix}8\\2\end{pmatrix}", "komponentenweise: $2 - 0 + 6 = 8$ und $0 - 1 + 3 = 2$"),
], "Satz 5.8 anwenden", frei=True) + G(r"""

:::alt Als Rezept
Kennst du von drei Zutaten, was der Mixer jeweils daraus macht, dann kennst du auch das Ergebnis jeder Mischung
aus diesen Zutaten: gleiche Mengen, nur die Ergebnisse statt der Zutaten.
:::
"""))

k.ordnen("Ordne den Induktionsschritt im Beweis von Satz 5.8: Aus der Aussage für $m$ folgt die für $m + 1$.",
         ["Zu zeigen: $f\\big(\\sum_{j=1}^{m+1} \\lambda_j v^{(j)}\\big) = \\sum_{j=1}^{m+1} \\lambda_j f(v^{(j)})$.",
          "Wir spalten den letzten Summanden ab: $f\\big(\\sum_{j=1}^{m+1} \\lambda_j v^{(j)}\\big) = f\\big(\\sum_{j=1}^{m} \\lambda_j v^{(j)}\\big) + f(\\lambda_{m+1} v^{(m+1)})$ (Additivität).",
          "Auf die erste Summe wenden wir die Induktionsvoraussetzung an, auf den letzten Summanden die Verträglichkeit mit der Skalarmultiplikation.",
          "Das ergibt $\\sum_{j=1}^{m} \\lambda_j f(v^{(j)}) + \\lambda_{m+1} f(v^{(m+1)})$.",
          "Das ist $\\sum_{j=1}^{m+1} \\lambda_j f(v^{(j)})$. $\\square$"],
         "Erst abspalten (Additivität), dann Induktionsvoraussetzung und Skalarmultiplikation, dann wieder zusammenfassen.",
         ablenker=["Da $f$ bijektiv ist, folgt die Behauptung sofort.", "Wir nehmen $m = n$ an und setzen $m + 1 = n$ ein."],
         tipps=["Der Beweis beginnt mit der Behauptung für $m + 1$ und endet mit ihrer Rechten Seite.", "Die Induktionsvoraussetzung gilt für Summen mit $m$ Summanden.",
                "Bijektivität wird in Satz 5.8 nicht vorausgesetzt."])

# ── Seite 5: Satz 5.9 ───────────────────────────────────────────────────────
k.erklaerung("Satz 5.9: Basisbilder legen alles fest", G(r"""
## Satz 5.9

Wie viele Bilder muss man kennen? Nur die einer <<Basis|Basis>>.

**Satz 5.9.** Sei $\mathfrak{B} = (b^{(1)}, \dots, b^{(n)})$ eine geordnete Basis von $V$ und $w^{(1)}, \dots, w^{(n)} \in W$ beliebig.
Dann gibt es **genau eine** lineare Abbildung $f\colon V \to W$ mit $f(b^{(j)}) = w^{(j)}$, und es gilt
$f\big(\sum_j x_j b^{(j)}\big) = \sum_j x_j w^{(j)}$.

:::achtung Bemerkung 5.10
Die Bilder $w^{(j)}$ dürfen gleich, null oder linear abhängig sein. Dann ist $f$ nicht injektiv: Bei der Projektion $\pi_G$ haben $e^{(1)}$ und $e^{(2)}$
dasselbe Bild, also $\pi_G((1, -1)^\top) = 0$.
:::

""") + R([
    (r"\mathfrak{B} = \left(\begin{pmatrix}1\\1\end{pmatrix}, \begin{pmatrix}1\\0\end{pmatrix}\right),\ f(b^{(1)}) = \begin{pmatrix}2\\0\end{pmatrix},\ f(b^{(2)}) = \begin{pmatrix}1\\3\end{pmatrix}", "Basis (Bsp. 5.70) und frei gewählte Bilder"),
    (r"\begin{pmatrix}2\\1\end{pmatrix} = 1 \cdot b^{(1)} + 1 \cdot b^{(2)}", "Koordinaten von $x$ bezüglich $\\mathfrak{B}$"),
    (r"f(x) = 1 \cdot \begin{pmatrix}2\\0\end{pmatrix} + 1 \cdot \begin{pmatrix}1\\3\end{pmatrix} = \begin{pmatrix}3\\3\end{pmatrix}", "dieselben Koordinaten, nur mit den Bildern"),
], "Satz 5.9 anwenden", frei=True) + G(r"""

:::alt Als Stadtplan
Hast du die Bilder der Basis, dann hast du in jedem Planquadrat die Verschiebung des Straßennetzes,
und jeder andere Ort wird mit denselben Koordinaten wiedergefunden. Du musst nur die Koordinaten kennen und
die Bilder der Gitterpunkte.
:::
"""))

k.vektor("Sei $f\\colon \\mathbb{R}^2 \\to \\mathbb{R}^2$ linear mit $f\\big((1, 1)^\\top\\big) = (2, 0)^\\top$ und $f\\big((1, 0)^\\top\\big) = (1, 3)^\\top$. Bestimme $f\\big((3, 2)^\\top\\big)$.",
         [4, 6],
         "$(3, 2)^\\top = 2 \\cdot (1, 1)^\\top + 1 \\cdot (1, 0)^\\top$, also $f = 2 \\cdot (2, 0)^\\top + 1 \\cdot (1, 3)^\\top = (5, 3)^\\top$. "
         "Nachgerechnet mit der Formel $(u, v) \\mapsto (u + v,\\ 3u - 3v)$: $(3 + 2,\\ 9 - 6) = (5, 3)$.",
         tipps=["Schreibe $(3, 2)^\\top$ als Linearkombination der beiden Basisvektoren.", "$(3, 2)^\\top = 2 \\cdot (1, 1)^\\top + 1 \\cdot (1, 0)^\\top$.", "Ersetze die Basisvektoren durch ihre Bilder."],
         rechenweg=R([(r"\begin{pmatrix}3\\2\end{pmatrix} = 2\begin{pmatrix}1\\1\end{pmatrix} + 1\begin{pmatrix}1\\0\end{pmatrix}", "zweite Komponente $= 2$ legt den ersten Koeffizienten fest, dann der Rest"),
                      (r"f = 2\begin{pmatrix}2\\0\end{pmatrix} + \begin{pmatrix}1\\3\end{pmatrix} = \begin{pmatrix}5\\3\end{pmatrix}", "Satz 5.9")], frei=True),
         typische_fehler=[([8, 6], "Das ist $3 \\cdot f(b^{(1)}) + 2 \\cdot f(b^{(2)}) = (6 + 2,\\ 0 + 6)$. Die Zahlen $3, 2$ sind die Standardkoordinaten, nicht die Koordinaten bezüglich $\\mathfrak{B}$.")])

# ── Seite 6: Hom, Spiegelung, Beobachtung 5.13 ───────────────────────────────
k.erklaerung("Beispiele 5.11, 5.12 und Beobachtung 5.13", G(r"""
## Rechnen mit linearen Abbildungen

Die Menge $\mathrm{Hom}_K(V, W)$ aller linearen Abbildungen $V \to W$ ist mit $(f + g)(v) := f(v) + g(v)$ und $(\lambda f)(v) := \lambda f(v)$
selbst ein Vektorraum (Bsp. 5.11).

**Beispiel 5.12.** Mit der Projektion $\pi_G$ auf $G = \langle (1, 1)^\top \rangle$ ist $s_G := 2\pi_G - \mathrm{id}_{\mathbb{R}^2}$ linear.
Für $v = u + w$ mit $u \in G$, $w \perp G$ gilt $s_G(v) = u - w$: die [[Spiegelung]] an $G$.

**Beobachtung 5.13.** Verkettungen linearer Abbildungen sind linear. Die Umkehrabbildung eines Isomorphismus ist linear.

:::visual vektoren2d
{"vektoren": [{"x": 2, "y": 1, "label": "x"}, {"x": "3/2", "y": "3/2", "label": "\\pi_G(x)"}, {"x": 1, "y": 2, "label": "s_G(x)"}],
 "unterschrift": "$x = (2, 1)^\\top$, Projektion $\\pi_G(x) = (\\frac32, \\frac32)^\\top$ und Spiegelung $s_G(x) = 2\\pi_G(x) - x = (1, 2)^\\top$."}
:::

""") + R([
    (r"2\pi_G(x) = 2\begin{pmatrix}3/2\\3/2\end{pmatrix} = \begin{pmatrix}3\\3\end{pmatrix}", "$\\pi_G(x) = (\\frac32, \\frac32)^\\top$ aus Bsp. 5.77"),
    (r"s_G(x) = \begin{pmatrix}3\\3\end{pmatrix} - \begin{pmatrix}2\\1\end{pmatrix} = \begin{pmatrix}1\\2\end{pmatrix}", "minus $\\mathrm{id}(x) = x$"),
    (r"s_G(s_G(x)) = x", "zweimal spiegeln bringt jeden Vektor zurück: $s_G$ ist sein eigenes Inverses, also Automorphismus"),
], "Spiegelung aus Projektion", frei=True) + G(r"""

:::alt Als Spiegel im Zimmer
Die Projektion ist der Schatten auf die Wand $G$. Der Spiegel zeigt das Bild so weit hinter der Wand, wie der Gegenstand davor steht:
einmal den Schatten doppelt nehmen und den Gegenstand abziehen.
:::
"""))

k.mehrfach("Welche Aussagen über lineare Abbildungen stimmen?",
           ["Sind $f\\colon V \\to W$ und $g\\colon W \\to X$ linear, so ist $g \\circ f$ linear",
            "Die Summe $f + g$ zweier linearer Abbildungen $V \\to W$ ist linear",
            "Die Umkehrabbildung eines Isomorphismus ist linear",
            "$2\\pi_G - \\mathrm{id}$ ist wieder linear"],
           ["Jede bijektive Abbildung zwischen Vektorräumen ist ein Isomorphismus",
            "Die konstante Abbildung $v \\mapsto w$ mit $w \\neq 0$ ist ein Element von $\\mathrm{Hom}_K(V, W)$"],
           "Beobachtung 5.13 und Beispiel 5.11 und 5.12 liefern die ersten vier Aussagen. Ein Isomorphismus muss linear **und** bijektiv sein: Die Bijektivität allein reicht nicht. "
           "Eine konstante Abbildung mit Wert $\\neq 0$ ist nicht linear (Bsp. 5.3).",
           tipps=["Ein Isomorphismus ist ein bijektiver Homomorphismus: beides muss gelten.", "Teste die konstante Abbildung mit dem Skalar $0$."],
           fehler={"Jede bijektive Abbildung zwischen Vektorräumen ist ein Isomorphismus": "Die Abbildung muss auch linear sein. $x \\mapsto x + 1$ ist bijektiv auf $\\mathbb{R}$, aber nicht linear.",
                   "Die konstante Abbildung $v \\mapsto w$ mit $w \\neq 0$ ist ein Element von $\\mathrm{Hom}_K(V, W)$": "Für $\\lambda = 0$ gilt $f(0 \\cdot v) = w \\neq 0 = 0 \\cdot f(v)$ (Bsp. 5.3)."})

# ── Seite 7: Kern, Bild, Rang ───────────────────────────────────────────────
k.erklaerung("Kern, Bild und Rang (Satz 5.14 bis Beobachtung 5.17)", G(r"""
## Was wird auf null geschickt, was wird getroffen?

Für lineares $f\colon V \to W$ heißt $\ker(f) = \{v \in V \mid f(v) = 0_W\}$ der [[Kern einer linearen Abbildung|Kern]], $f(V)$ das [[Bild]].

**Satz 5.14.** $\ker(f)$ und $f(V)$ sind Untervektorräume. Ist $(b^{(1)}, \dots, b^{(n)})$ eine Basis von $V$, so gilt $f(V) = \langle f(b^{(1)}), \dots, f(b^{(n)}) \rangle$.

**Definition 5.15.** $\mathrm{rang}(f) := \dim f(V)$ ([[Rang]]).

**Beobachtung 5.17.** $f(v) = f(w) \iff v - w \in \ker(f)$. Insbesondere ist $f$ genau dann injektiv, wenn $\ker(f) = \{0_V\}$.

""") + R([
    (r"\pi_G\begin{pmatrix}x_1\\x_2\end{pmatrix} = \frac{x_1 + x_2}{2}\begin{pmatrix}1\\1\end{pmatrix}", "Projektion auf $G = \\langle (1, 1)^\\top \\rangle$ (Bsp. 5.16)"),
    (r"x_1 + x_2 = 0 \iff x = x_1 \begin{pmatrix}1\\-1\end{pmatrix}", "Vektor auf null genau dann, wenn die Klammer verschwindet: $\\ker(\\pi_G) = \\langle (1, -1)^\\top \\rangle$"),
    (r"\pi_G(\mathbb{R}^2) = G", "alle Bilder liegen in $G$, jeder Vektor aus $G$ ist sein eigenes Bild"),
    (r"\mathrm{rang}(\pi_G) = \dim G = 1", "Kern und Bild sind beide eindimensional"),
], "Kern, Bild, Rang der Projektion", frei=True) + G(r"""

:::alt Als Schatten
Der Kern sind alle Dinge, die bei der Projektion keinen Schatten werfen, also gleich wirken wie nichts. Das Bild ist die Wand mit allen
möglichen Schatten. Zwei Dinge werfen denselben Schatten genau dann, wenn ihr Unterschied im Kern liegt.
:::
"""))

k.vektor("$f\\colon \\mathbb{R}^2 \\to \\mathbb{R}^2,\\ (x, y)^\\top \\mapsto (x - y,\\ 2x - 2y)^\\top$ ist linear. Gib einen Vektor $\\ne 0$ an, der den Kern von $f$ aufspannt.",
         [1, 1],
         "$f(x, y) = 0$ heißt $x - y = 0$ und $2x - 2y = 0$, beides gleichwertig zu $x = y$. Der Kern ist $\\langle (1, 1)^\\top \\rangle$ und hat Dimension $1$.",
         vielfaches=True,
         tipps=["Setze $f(x, y) = (0, 0)^\\top$ und löse.", "Beide Komponenten sagen dasselbe.", "$x = y$: Der Vektor $(1, 1)^\\top$ löst es."],
         rechenweg=R([(r"x - y = 0", "erste Komponente gleich $0$"), (r"2x - 2y = 0", "zweite Komponente: dieselbe Bedingung"),
                      (r"x = y", "also $\\ker(f) = \\{(t, t)^\\top \\mid t \\in \\mathbb{R}\\} = \\langle (1, 1)^\\top \\rangle$")], frei=True),
         typische_fehler=[([1, -1], "$f((1, -1)^\\top) = (2, 4)^\\top \\neq 0$. Setze deinen Vektor in beide Komponenten ein.")])

k.mc("Wann gilt $f(v) = f(w)$ für eine lineare Abbildung $f$ (Beobachtung 5.17)?",
     ["genau dann, wenn $v - w \\in \\ker(f)$", "genau dann, wenn $v = w$", "genau dann, wenn $v + w \\in \\ker(f)$", "genau dann, wenn $v, w \\in \\ker(f)$"],
     "Wegen der Linearität gilt $f(v) = f(w) \\iff f(v) - f(w) = 0 \\iff f(v - w) = 0$. Daraus folgt: $f$ ist genau dann injektiv, wenn nur $v = w$ diese Gleichung erfüllt, also $\\ker(f) = \\{0\\}$.",
     tipps=["Bringe $f(w)$ auf die linke Seite und fasse mit der Linearität zusammen.", "$f(v) - f(w) = f(v - w)$."],
     fehler={"genau dann, wenn $v = w$": "Das gilt nur bei injektivem $f$. Bei $\\pi_G$ haben $(1, 0)^\\top$ und $(0, 1)^\\top$ dasselbe Bild.",
             "genau dann, wenn $v + w \\in \\ker(f)$": "Das wäre $f(v) = -f(w)$. Für gleiche Bilder zählt die Differenz.",
             "genau dann, wenn $v, w \\in \\ker(f)$": "Dann haben beide das Bild $0$, aber auch Vektoren außerhalb des Kerns können gleiche Bilder haben."})

# ── Seite 8: Satz 5.18 ──────────────────────────────────────────────────────
k.erklaerung("Urbilder: Satz 5.18, Korollar 5.21, Beispiel 5.22", G(r"""
## Alle Vektoren mit Bild $y$

:::analogie 🧭 Eine Lösung plus alle Verschiebungen
Kennst du einen Weg zu einem Ziel, dann kommst du auf alle anderen Wege, indem du Umwege addierst, die nirgends hin führen.
Die Umwege sind der Kern.
:::

**Satz 5.18.** Ist $y = f(v^{(0)})$, so gilt $f^{-1}(\{y\}) = v^{(0)} + \ker(f) := \{v^{(0)} + u \mid u \in \ker(f)\}$, ein affiner Raum mit Richtung $\ker(f)$.
*Beweis.* $v \in f^{-1}(\{y\}) \iff f(v) = f(v^{(0)}) \iff v - v^{(0)} \in \ker(f)$ nach Beobachtung 5.17.

""") + R([
    (r"f\begin{pmatrix}x\\y\\z\end{pmatrix} = \begin{pmatrix}x + y\\z\end{pmatrix}", "Beispiel 5.22, $f\\colon \\mathbb{R}^3 \\to \\mathbb{R}^2$"),
    (r"x + y = 0,\ z = 0 \Rightarrow \ker(f) = \left\langle \begin{pmatrix}-1\\1\\0\end{pmatrix} \right\rangle", "$y = t$ frei, $x = -t$"),
    (r"f\begin{pmatrix}u\\0\\v\end{pmatrix} = \begin{pmatrix}u\\v\end{pmatrix}", "jedes $(u, v)^\\top$ hat ein Urbild: $f(\\mathbb{R}^3) = \\mathbb{R}^2$, Rang $2$"),
    (r"f^{-1}(\{(2, 5)^\top\}) = \begin{pmatrix}2\\0\\5\end{pmatrix} + \left\langle \begin{pmatrix}-1\\1\\0\end{pmatrix} \right\rangle", "Satz 5.18: eine Gerade, Dimension $3 - 2 = 1$ (Kor. 5.21)"),
], "Beispiel 5.22 komplett", frei=True) + G(r"""

:::alt Als Gleichungssystem
$f(v) = y$ ist ein Gleichungssystem. Seine Lösungen sind eine spezielle Lösung plus alle Lösungen des zugehörigen
homogenen Systems $f(u) = 0$. Genau das sagt Satz 5.18.
:::
"""))

k.zahl("Sei $f\\colon \\mathbb{R}^3 \\to \\mathbb{R}^2,\\ (x, y, z)^\\top \\mapsto (x + y,\\ z)^\\top$ mit $\\ker(f) = \\langle (-1, 1, 0)^\\top \\rangle$. Welche Dimension hat $f^{-1}(\\{(2, 5)^\\top\\})$ (Korollar 5.21)?",
       1,
       "Das Urbild ist $v^{(0)} + \\ker(f)$ mit dem Richtungsraum $\\ker(f)$, also $\\dim = \\dim\\ker(f) = 1$. Es ist eine Gerade im $\\mathbb{R}^3$.",
       tipps=["Satz 5.18: Das Urbild ist ein affiner Raum mit Richtungsraum $\\ker(f)$.", "Die Dimension eines affinen Raums ist die seines Richtungsraums.", "$\\dim\\ker(f) = 1$ ist gegeben."],
       rechenweg=R([(r"\dim f^{-1}(\{y\}) = \dim V - \mathrm{rang}(f)", "Korollar 5.21"), (r"3 - 2 = 1", "$\\dim V = 3$, $\\mathrm{rang}(f) = 2$")], frei=True),
       typische_fehler=[(2, "Das ist der Rang von $f$, nicht die Dimension des Urbilds. Das Urbild hat Richtungsraum $\\ker(f)$."),
                        (3, "Das wäre $\\dim V$. Ein einzelnes Urbild ist nur eine Gerade in diesem Raum."),
                        (0, "Das Urbild ist nicht ein einzelner Punkt: $(2, 0, 5)$ und $(1, 1, 5)$ haben beide das Bild $(2, 5)$.")])

# ── Seite 9: Satz 5.20 ──────────────────────────────────────────────────────
k.erklaerung("Satz 5.20: Dimensionsformel", G(r"""
## Satz 5.20

**Satz 5.20 (Dimensionsformel).** Für lineares $f\colon V \to W$ mit $\dim V < \infty$ gilt
$$\dim V = \dim \ker(f) + \mathrm{rang}(f).$$

*Beweisidee.* Eine Basis $b^{(1)}, \dots, b^{(k)}$ von $\ker(f)$ wird zu einer Basis $b^{(1)}, \dots, b^{(n)}$ von $V$ ergänzt (Kor. 4.66).
Dann ist $f(b^{(k+1)}), \dots, f(b^{(n)})$ eine Basis von $f(V)$: Sie erzeugt $f(V)$, weil $f(b^{(j)}) = 0$ für $j \le k$ (Satz 5.14), und sie ist linear unabhängig,
weil eine verschwindende Kombination einen Vektor im Kern liefern würde. Das sind $n - k$ Stück.

""") + R([
    (r"\dim \mathbb{R}^2 = 2 = 1 + 1 = \dim\ker(\pi_G) + \mathrm{rang}(\pi_G)", "Projektion auf eine Gerade (Bsp. 5.16)"),
    (r"3 = 1 + 2", "Beispiel 5.22: $\\dim\\ker(f) = 1$, $\\mathrm{rang}(f) = 2$"),
    (r"\dim\ker(f) = 3 - 2 = 1", "aus $\\dim V = 3$ und dem Rang gewonnen: der Kern muss die fehlende Dimension haben"),
], "Dimensionsformel in den bekannten Beispielen") + G(r"""

:::alt Als Wasserhahn
Von $n$ Dimensionen Eingang geht ein Teil verloren (Kern, bei dem nichts herauskommt). Der Rest kommt als Rang am Ausgang an:
Der Hahn kann nicht mehr abgeben, als hineinfließt, und was verloren geht, fehlt am Ausgang.
:::
"""))

k.ordnen("Ordne den Beweis der Dimensionsformel (Satz 5.20).",
         ["Sei $n = \\dim V$ und $b^{(1)}, \\dots, b^{(k)}$ eine Basis von $\\ker(f)$, ergänzt zu einer Basis $b^{(1)}, \\dots, b^{(n)}$ von $V$.",
          "Wegen $f(b^{(j)}) = 0$ für $j \\le k$ und Satz 5.14 gilt $f(V) = \\langle f(b^{(k+1)}), \\dots, f(b^{(n)}) \\rangle$.",
          "Aus $\\sum_{j=k+1}^n \\lambda_j f(b^{(j)}) = 0$ folgt $\\sum_{j=k+1}^n \\lambda_j b^{(j)} \\in \\ker(f)$, also $= \\sum_{j=1}^k \\mu_j b^{(j)}$.",
          "Die lineare Unabhängigkeit von $b^{(1)}, \\dots, b^{(n)}$ erzwingt, dass alle $\\lambda_j$ und $\\mu_j$ null sind.",
          "Also ist $f(b^{(k+1)}), \\dots, f(b^{(n)})$ eine Basis von $f(V)$, und $\\mathrm{rang}(f) = n - k$. Das ist die Behauptung. $\\square$"],
         "Erst Ergänzung zur Basis, dann Erzeugendensystem, dann lineare Unabhängigkeit über den Kern, am Ende Zählen.",
         ablenker=["Da $f$ injektiv ist, ist $k = 0$.", "Wir setzen $\\dim W = n$ voraus."],
         tipps=["Der Beweis zählt Basisvektoren: $k$ im Kern, $n - k$ bleiben für das Bild.", "Erzeugung und lineare Unabhängigkeit gehören zusammen zur Basis.",
                "Von Injektivität oder $\\dim W$ ist im Satz nichts vorausgesetzt."])

k.zahl("$f\\colon \\mathbb{R}^5 \\to \\mathbb{R}^3$ sei linear mit $\\mathrm{rang}(f) = 2$. Welche Dimension hat $\\ker(f)$?", 3,
       "Die Dimensionsformel liefert $5 = \\dim\\ker(f) + 2$, also $\\dim\\ker(f) = 3$.",
       tipps=["Satz 5.20 verbindet drei Dimensionen.", "Satz 5.20: $\\dim V = \\dim\\ker(f) + \\mathrm{rang}(f)$.", "Setze $\\dim V = 5$ und $\\mathrm{rang}(f) = 2$ ein."],
       rechenweg=R([(r"5 = \dim\ker(f) + 2", "Dimensionsformel"), (r"\dim\ker(f) = 5 - 2 = 3", "umstellen")], frei=True),
       typische_fehler=[(1, "Das wäre $3 - 2$ mit der Dimension des Zielraums. In die Formel gehört die Dimension von $V$, hier $5$."),
                        (2, "Das ist der Rang. Der Kern hat die **fehlende** Dimension: $5 - 2$."),
                        (5, "Das ist $\\dim V$, nicht $\\dim\\ker(f)$.")])

# ── Seite 10: Satz 5.23, 5.25 ───────────────────────────────────────────────
k.erklaerung("Injektiv gleich surjektiv? Satz 5.23 und Korollar 5.25", G(r"""
## Gleiche Dimension

**Satz 5.23.** Für lineares $f\colon V \to W$ mit $\dim V = \dim W < \infty$ gilt: $f$ ist genau dann injektiv, wenn $f$ surjektiv ist.

*Beweis.* Injektiv $\iff \ker(f) = \{0\} \iff \dim\ker(f) = 0 \iff \mathrm{rang}(f) = \dim V = \dim W \iff f(V) = W$ (Satz 4.74, Dimensionsformel).

**Bemerkung 5.24.** Gleiche Dimension ist wesentlich: $(x, y, z)^\top \mapsto (x + y, z)^\top$ ist surjektiv, nicht injektiv; $(u, v)^\top \mapsto (u, 0, v)^\top$ ist injektiv, nicht surjektiv.

**Korollar 5.25.** Endlichdimensionale Räume über $K$ sind genau dann isomorph, wenn ihre Dimensionen gleich sind.

""") + R([
    (r"\dim \mathcal{F} = 2 = \dim \mathbb{R}^2", "Bsp. 5.26: $\\mathcal{F}$ und $\\mathbb{R}^2$ sind isomorph, $\\kappa$ ist ein Isomorphismus"),
    (r"3 = 1 + 2", "$f$ aus Bem. 5.24 (erste): surjektiv, Kern $\\neq 0$, weil $3 \\neq 2$"),
    (r"2 = 0 + 2", "zweite Abbildung: Kern $0$, Rang $2 < 3$"),
], "Räume gleicher Dimension", frei=True) + G(r"""

:::alt Als Sitzplätze
Sind Gäste und Stühle gleich viele, dann sitzt jeder Gast genau dann auf einem eigenen Stuhl, wenn kein Stuhl leer bleibt.
Bei ungleich vielen geht das nicht: Es bleibt entweder ein Stuhl leer oder zwei teilen sich einen.
:::
"""))

k.mehrfach("Welche dieser Räume sind (über $\\mathbb{R}$) isomorph zu $\\mathbb{R}^2$?",
           ["$\\mathcal{F}$ der Funktionen $t \\mapsto a + bt$ (Bsp. 5.26)", "$\\mathbb{C}$ als reeller Vektorraum", "$\\{(x, y, 0)^\\top \\mid x, y \\in \\mathbb{R}\\} \\subseteq \\mathbb{R}^3$"],
           ["$\\mathbb{R}^3$", "$\\mathbb{R}^{2 \\times 2}$ (reelle $2 \\times 2$-Matrizen)"],
           "Nach Korollar 5.25 zählt nur die Dimension: $\\dim \\mathcal{F} = 2$, $\\dim_{\\mathbb{R}} \\mathbb{C} = 2$ (Basis $1, i$), die Ebene $z = 0$ hat Dimension $2$. "
           "$\\mathbb{R}^3$ hat Dimension $3$ und $\\mathbb{R}^{2 \\times 2}$ nach Beobachtung 5.43 Dimension $4$.",
           tipps=["Zähle jeweils eine Basis.", "Korollar 5.25: isomorph genau dann, wenn die Dimension gleich ist."],
           fehler={"$\\mathbb{R}^3$": "Eine lineare Abbildung $\\mathbb{R}^2 \\to \\mathbb{R}^3$ kann nicht surjektiv sein, $\\mathbb{R}^3 \\to \\mathbb{R}^2$ nicht injektiv. Die Dimensionen $2 \\neq 3$ sind verschieden.",
                   "$\\mathbb{R}^{2 \\times 2}$ (reelle $2 \\times 2$-Matrizen)": "Eine Matrix hat vier Einträge, die Basis aus vier Matrizen mit einer $1$ (Beob. 5.43) zeigt Dimension $4$."})

# ── Praxis ──────────────────────────────────────────────────────────────────
k.praxis()


def _lin_text(a, b, c, d):
    def lin(p, q):
        t = []
        if p:
            t.append("x" if p == 1 else ("-x" if p == -1 else f"{p}x"))
        if q:
            s = "y" if q == 1 else ("-y" if q == -1 else f"{q}y")
            t.append(("+ " + s) if t and not s.startswith("-") else (("- " + s[1:]) if t else s))
        return " ".join(t) if t else "0"
    return lin(a, b), lin(c, d)


def linear_test(rng):
    art = rng.choice(["linear", "linear", "affin", "produkt", "betrag"])
    a, b, c, d = (rng.choice([-2, -1, 0, 1, 2, 3]) for _ in range(4))
    if (a, b, c, d) == (0, 0, 0, 0):
        a = 1
    t1, t2 = _lin_text(a, b, c, d)
    e = rng.choice([-2, -1, 1, 2, 3])
    if art == "linear":
        comp = (t1, t2)
        lin, f0 = True, True
    elif art == "affin":
        comp = (t1 + (f" + {e}" if e > 0 else f" - {-e}") if t1 != "0" else str(e), t2)
        lin, f0 = False, False
    elif art == "produkt":
        comp = ("xy", t2)
        lin, f0 = False, True
    else:
        comp = ("|x|", t2)
        lin, f0 = False, True
    opt_lin = "linear"
    opt_f0 = "nicht linear: $f(0) \\neq 0$"
    opt_gegen = "nicht linear, obwohl $f(0) = 0$ (ein anderes Gegenbeispiel verletzt eine Bedingung)"
    loesung = opt_lin if lin else (opt_f0 if not f0 else opt_gegen)
    if art == "linear":
        zeilen = [(r"v = (1, 2)^\top,\ w = (3, -1)^\top", "zwei Testvektoren")]
        fa = lambda x, y: (a * x + b * y, c * x + d * y)
        fv, fw, fvw = fa(1, 2), fa(3, -1), fa(4, 1)
        zeilen += [(f"f(v) + f(w) = {vt(fv)} + {vt(fw)} = {vt([fv[0] + fw[0], fv[1] + fw[1]])}", "Bilder addieren"),
                   (f"f(v + w) = f\\left({vt([4, 1])}\\right) = {vt(fvw)}", "gleich: Additivität erfüllt (jede Komponente ist eine Linearkombination von $x, y$)")]
        grund = "Jede Komponente ist eine Linearkombination von $x$ und $y$ ohne konstanten Summanden: Addition und Skalarmultiplikation bleiben erhalten (Satz 5.31 zeigt später: jede solche Abbildung ist linear)."
    elif art == "affin":
        zeilen = [(f"f(0) = {vt([e, 0])}", f"$f(0) \\neq 0$ wegen des konstanten Summanden $+{e}$, also nicht linear (Satz 5.8)")]
        grund = f"Der konstante Summand ${e}$ in der ersten Komponente macht $f(0) = ({e}, 0)^\\top \\neq 0$. Eine lineare Abbildung hat $f(0_V) = 0_W$."
    elif art == "produkt":
        zeilen = [(r"f\begin{pmatrix}2\\1\end{pmatrix} = " + vt([2, c * 2 + d * 1]) , "$xy = 2$ bei $x = 2$, $y = 1$"),
                  (r"f\begin{pmatrix}4\\2\end{pmatrix} = " + vt([8, c * 4 + d * 2]), "$x y = 8$ bei doppelter Eingabe: das Doppelte von $2$ wäre $4$")]
        grund = "Bei $v = (2, 1)^\\top$ und $2v = (4, 2)^\\top$ ist die erste Komponente $2$ bzw. $8$, aber $f(2v) = 2f(v)$ verlangt $4$. Das Produkt $xy$ ist nicht linear."
    else:
        zeilen = [(r"f\begin{pmatrix}-1\\0\end{pmatrix} = " + vt([1, -c]), "$|-1| = 1$ in der ersten Komponente"),
                  (r"-f\begin{pmatrix}1\\0\end{pmatrix} = " + vt([-1, -c]), "$f(-v)$ müsste $-f(v)$ sein: die erste Komponente hat $1$ statt $-1$")]
        grund = "Für $v = (1, 0)^\\top$ ist $f(-v)$ in der ersten Komponente $|-1| = 1$, aber $-f(v)$ hat dort $-1$. Der Betrag ist nicht linear."
    optionen = [loesung] + [o for o in (opt_lin, opt_f0, opt_gegen) if o != loesung]
    fehler = {o: ("Das stimmt nicht. " + grund) for o in optionen[1:]}
    return {"typ": "mc",
            "frage": f"Ist $f\\colon \\mathbb{{R}}^2 \\to \\mathbb{{R}}^2,\\ (x, y)^\\top \\mapsto \\left({comp[0]},\\ {comp[1]}\\right)^\\top$ linear?",
            "optionen": optionen, "fehler": fehler,
            "tipps": ["Teste zuerst, ob $f(0) = 0$ gilt.", "Enthält eine Komponente ein Produkt, einen Betrag, eine Potenz oder eine Konstante, ist es verdächtig.",
                      "Sind alle Komponenten Linearkombinationen von $x$ und $y$ ohne konstanten Summanden, ist $f$ linear."],
            "rechenweg": R(zeilen, "Test", frei=True),
            "erklaerung": grund}


def bild_aus_basisbildern(rng):
    while True:
        b1 = [rng.randint(-2, 3), rng.randint(-2, 3)]
        b2 = [rng.randint(-2, 3), rng.randint(-2, 3)]
        if b1[0] * b2[1] - b1[1] * b2[0] not in (0,):
            break
    w1 = [rng.randint(-3, 3), rng.randint(-3, 3)]
    w2 = [rng.randint(-3, 3), rng.randint(-3, 3)]
    x1, x2 = rng.choice([-2, -1, 1, 2, 3]), rng.choice([-2, -1, 1, 2, 3])
    v = [x1 * b1[0] + x2 * b2[0], x1 * b1[1] + x2 * b2[1]]
    erg = [x1 * w1[0] + x2 * w2[0], x1 * w1[1] + x2 * w2[1]]
    falsch1 = [v[0] * w1[0] + v[1] * w2[0], v[0] * w1[1] + v[1] * w2[1]]
    falsch2 = [x1 * w1[0] - x2 * w2[0], x1 * w1[1] - x2 * w2[1]]
    fehler = ohne_gleiche(erg, [(falsch1, "Du hast die Standardkoordinaten $v_1, v_2$ als Koeffizienten der Bilder benutzt. Nötig sind die Koordinaten von $v$ bezüglich der Basis $(b^{(1)}, b^{(2)})$."),
                                (falsch2, "Ein Vorzeichen ist falsch: $f(v) = x_1 f(b^{(1)}) + x_2 f(b^{(2)})$, beide mit ihren Koeffizienten.")])
    det = b1[0] * b2[1] - b1[1] * b2[0]
    return {"typ": "vektor",
            "frage": (f"$f\\colon \\mathbb{{R}}^2 \\to \\mathbb{{R}}^2$ sei linear mit $f\\left({vt(b1)}\\right) = {vt(w1)}$ und $f\\left({vt(b2)}\\right) = {vt(w2)}$. "
                      f"Bestimme $f\\left({vt(v)}\\right)$."),
            "loesung": erg,
            "tipps": ["Schreibe $v$ als Linearkombination der beiden Basisvektoren: $v = x_1 b^{(1)} + x_2 b^{(2)}$.",
                      f"Hier ist $v = {x1} \\cdot b^{{(1)}} + {x2} \\cdot b^{{(2)}}$ (löse das $2 \\times 2$-System).",
                      "Ersetze dann $b^{(1)}, b^{(2)}$ durch $f(b^{(1)}), f(b^{(2)})$ (Satz 5.9)."],
            "rechenweg": R([(f"{vt(v)} = {x1} \\cdot {vt(b1)} + {x2} \\cdot {vt(b2)}", f"Koordinaten von $v$ bezüglich $\\mathfrak{{B}}$ (Determinante der Basis: ${det}$)"),
                            (f"f(v) = {x1} \\cdot {vt(w1)} + {x2} \\cdot {vt(w2)} = {vt(erg)}", "Satz 5.9: gleiche Koeffizienten, die Bilder statt der Basisvektoren")], frei=True),
            "erklaerung": "Eine lineare Abbildung ist durch die Bilder einer Basis festgelegt (Satz 5.9). Erst die Koordinaten bestimmen, dann die Bilder mischen.",
            "typische_fehler": fehler}


def _abbildung_ohne_hinweis(rng, n, m, rang_ziel):
    """Zufällige ganzzahlige (m x n)-Matrix mit vorgegebenem Rang."""
    while True:
        basis = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(rang_ziel)]
        zeilen = []
        for i in range(m):
            if i < rang_ziel:
                zeilen.append(basis[i][:])
            else:
                koef = [rng.randint(-1, 2) for _ in range(rang_ziel)]
                zeilen.append([sum(kk * basis[j][s] for j, kk in enumerate(koef)) for s in range(n)])
        rng.shuffle(zeilen)
        if mathlib.rang(zeilen) == rang_ziel:
            return zeilen


def _formeln(A):
    namen = ["x", "y", "z", "w"][:len(A[0])]
    out = []
    for z in A:
        t = ""
        for c, nm in zip(z, namen):
            if c == 0:
                continue
            term = nm if abs(c) == 1 else f"{abs(c)}{nm}"
            if not t:
                t = ("-" if c < 0 else "") + term
            else:
                t += (" - " if c < 0 else " + ") + term
        out.append(t or "0")
    return out


def kern_dimension(rng):
    n = rng.choice([3, 4])
    m = rng.choice([2, 3])
    r = rng.randint(1, min(m, n) - 0)
    if r == min(m, n) and n == m:
        r = rng.randint(1, n - 1)
    A = _abbildung_ohne_hinweis(rng, n, m, r)
    d = n - r
    namen = ["x", "y", "z", "w"][:n]
    f = _formeln(A)
    abb = f"\\left({', '.join(f)}\\right)^\\top"
    spalten = [[A[i][j] for i in range(m)] for j in range(n)]
    fehler = ohne_gleiche(d, [(r, "Das ist der Rang, nicht die Dimension des Kerns. $\\dim\\ker(f) = n - \\mathrm{rang}(f)$."),
                              (n, "Das ist $\\dim V$. Davon geht der Rang ab."),
                              (m - r if m - r != d else n + 1, "Der Rang gehört zur Dimensionsformel für $V$, nicht für den Zielraum: $\\dim\\ker(f) = n - \\mathrm{rang}(f)$.")])
    return {"frage": (f"$f\\colon \\mathbb{{R}}^{n} \\to \\mathbb{{R}}^{m},\\ ({', '.join(namen)})^\\top \\mapsto {abb}$ ist linear. Bestimme $\\dim \\ker(f)$. "
                      "Tipp: Die Bilder der Standardbasisvektoren sind die Spalten der Koeffizienten, der Rang ist die Zahl linear unabhängiger Spalten."),
            "loesung": d,
            "tipps": ["Bestimme zuerst den Rang: die Dimension der linearen Hülle der Bilder $f(e^{(1)}), \\dots, f(e^{(n)})$ (Satz 5.14).",
                      f"Die Bilder sind ${', '.join(vt(s) for s in spalten)}$. Wie viele davon sind linear unabhängig?",
                      f"Der Rang ist ${r}$. Nutze nun $\\dim V = \\dim\\ker(f) + \\mathrm{{rang}}(f)$."],
            "rechenweg": R([(f"\\mathrm{{rang}}(f) = \\dim\\langle {', '.join(vt(s) for s in spalten)} \\rangle = {r}", "Anzahl linear unabhängiger Spalten (Satz 5.14)"),
                            (f"{n} = \\dim\\ker(f) + {r}", f"Dimensionsformel (Satz 5.20), $\\dim V = {n}$"),
                            (f"\\dim\\ker(f) = {n} - {r} = {d}", "umstellen")], frei=True),
            "erklaerung": "Die Spalten sind die Bilder der Standardbasis und erzeugen das Bild. Ihre unabhängige Anzahl ist der Rang, den Rest zu $n$ liefert die Dimensionsformel.",
            "typische_fehler": fehler}


def kern_vektor(rng):
    while True:
        kv = [rng.randint(-2, 2) for _ in range(3)]
        if any(kv):
            break
    kv = ganz(kv)
    while True:
        zeilen = []
        for _ in range(2):
            while True:
                r = [rng.randint(-2, 2) for _ in range(3)]
                if sum(x * y for x, y in zip(r, kv)) == 0 and any(r):
                    break
            zeilen.append(r)
        if mathlib.rang(zeilen) == 2:
            break
    ker = mathlib.kern(zeilen)
    assert len(ker) == 1
    loes = ganz(ker[0])
    f = _formeln(zeilen)
    abb = f"\\left({f[0]},\\ {f[1]}\\right)^\\top"
    kandidaten = [([loes[0], -loes[1], loes[2]], "Ein Vorzeichen stimmt nicht: Setze deinen Vektor in beide Gleichungen ein."),
                  (loes[::-1], "Die Einträge stehen in falscher Reihenfolge: Setze deinen Vektor in beide Gleichungen ein."),
                  (list(zeilen[0]), "Das ist die erste Zeile der Koeffizienten. Der Kern löst $f(v) = 0$: Setze in beide Komponenten ein.")]
    fehler = [(w, t) for w, t in kandidaten if any(mathlib.skalarprodukt(w, z) != 0 for z in zeilen)]
    return {"frage": f"$f\\colon \\mathbb{{R}}^3 \\to \\mathbb{{R}}^2,\\ (x, y, z)^\\top \\mapsto {abb}$ ist linear. Gib einen Vektor $\\neq 0$ an, der $\\ker(f)$ aufspannt (jedes Vielfache $\\neq 0$ gilt).",
            "loesung": loes, "vielfaches": True,
            "tipps": ["Der Kern besteht aus allen $v$ mit $f(v) = 0$: Beide Komponenten gleich $0$ setzen.",
                      "Löse das homogene Gleichungssystem aus zwei Gleichungen in drei Unbekannten: eine Variable bleibt frei.",
                      f"Probe: Der Vektor $\\left({loes[0]}, {loes[1]}, {loes[2]}\\right)^\\top$ erfüllt beide Gleichungen."],
            "rechenweg": R([(f"{f[0]} = 0", "erste Komponente $= 0$"), (f"{f[1]} = 0", "zweite Komponente $= 0$"),
                            (f"v = t \\cdot {vt(loes)}", "eine freie Variable, Rest durch Einsetzen; $\\dim\\ker(f) = 3 - 2 = 1$"),
                            (f"f(v) = {vt([sum(a * b for a, b in zip(z, loes)) for z in zeilen])}", "Probe: beide Komponenten null")], frei=True),
            "erklaerung": "Der Kern ist die Lösungsmenge des homogenen Systems. Zwei unabhängige Gleichungen in drei Unbekannten lassen genau eine Richtung übrig (Dimensionsformel: $3 = 1 + 2$).",
            "typische_fehler": fehler}


k.generator(linear_test, typ="mc", titel="Ist die Abbildung linear?")
k.generator(bild_aus_basisbildern, typ="vektor", titel="Bild aus Basisbildern (Satz 5.9)")
k.generator(kern_dimension, typ="zahl", titel="Dimension des Kerns über die Dimensionsformel")
k.generator(kern_vektor, typ="vektor", titel="Kern einer linearen Abbildung bestimmen")

k.wf("Es gibt eine injektive lineare Abbildung $\\mathbb{R}^3 \\to \\mathbb{R}^2$.", False,
     "Nach der Dimensionsformel gilt $3 = \\dim\\ker(f) + \\mathrm{rang}(f)$ mit $\\mathrm{rang}(f) \\le 2$ (das Bild liegt im $\\mathbb{R}^2$). Also ist $\\dim\\ker(f) \\ge 1$, der Kern enthält einen Vektor $\\neq 0$, und $f$ ist nach Beobachtung 5.17 nicht injektiv.",
     tipps=["Wie groß kann der Rang höchstens sein?", "Injektiv bedeutet $\\ker(f) = \\{0\\}$."])

k.rechenweg_aufgabe(r"""
## Quiz-Stil: Kern, Bild und Urbild

Sei $f\colon \mathbb{R}^3 \to \mathbb{R}^2,\ (x, y, z)^\top \mapsto (x - y,\ y + z)^\top$. Beantworte der Reihe nach.
""",
    [{"typ": "wf", "frage": "$f$ ist linear.", "wahr": True,
      "tipps": ["Sind beide Komponenten Linearkombinationen von $x, y, z$ ohne konstanten Summanden?"],
      "erklaerung": "Jede Komponente ist eine Linearkombination der Koordinaten, also erhält $f$ Summen und Skalare."},
     {"typ": "vektor", "frage": "Gib einen Vektor $\\neq 0$ an, der $\\ker(f)$ aufspannt.", "loesung": [1, 1, -1], "vielfaches": True,
      "tipps": ["Setze $x - y = 0$ und $y + z = 0$.", "$y = t$ frei, dann $x = t$ und $z = -t$."],
      "rechenweg": "$x = y$ und $z = -y$, also $\\ker(f) = \\langle (1, 1, -1)^\\top \\rangle$.",
      "typische_fehler": [([1, -1, 1], "Setze in $x - y$ ein: $1 - (-1) = 2 \\neq 0$.")]},
     {"typ": "zahl", "frage": "Welchen Rang hat $f$?", "loesung": 2,
      "tipps": ["Dimensionsformel: $3 = \\dim\\ker(f) + \\mathrm{rang}(f)$.", "Der Kern hat Dimension $1$."],
      "rechenweg": "$\\mathrm{rang}(f) = 3 - 1 = 2$.",
      "typische_fehler": [(1, "Das ist $\\dim\\ker(f)$. Der Rang ist $\\dim V - \\dim\\ker(f)$.")]},
     {"typ": "zahl", "frage": "Welche Dimension hat das Urbild $f^{-1}(\\{(1, 2)^\\top\\})$ (Korollar 5.21)?", "loesung": 1,
      "tipps": ["Das Urbild hat die Dimension des Kerns, wenn es nicht leer ist.", "$(1, 2)^\\top$ wird getroffen, da $f$ surjektiv ist ($\\mathrm{rang} = 2 = \\dim\\mathbb{R}^2$)."],
      "rechenweg": "$\\dim f^{-1}(\\{y\\}) = \\dim V - \\mathrm{rang}(f) = 3 - 2 = 1$.",
      "typische_fehler": [(2, "Das ist der Rang. Gefragt ist die Dimension $3 - 2$.")]}],
    "$\\ker(f) = \\langle (1, 1, -1)^\\top \\rangle$, $\\mathrm{rang}(f) = 2$ ($f$ surjektiv), und jedes Urbild ist eine Gerade $v^{(0)} + \\ker(f)$ (Satz 5.18).",
    uebungsblatt=True,
    tipps=["Für den Kern setzt du $f(v) = 0$.", "Dimensionsformel für den Rang.", "Satz 5.18 und Korollar 5.21 für das Urbild."],
    rechenweg=r"""
:::rechnung
?? x - y = 0,\ y + z = 0 \Rightarrow v = t \cdot (1, 1, -1)^\top || Kern: eine freie Variable
?? 3 = 1 + \mathrm{rang}(f) \Rightarrow \mathrm{rang}(f) = 2 || Dimensionsformel
?? \dim f^{-1}(\{y\}) = 3 - 2 = 1 || Korollar 5.21
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Satz 5.9 beweisen

Seien $V$, $W$ Vektorräume über $K$, $\mathfrak{B} = (b^{(1)}, \dots, b^{(n)})$ eine geordnete Basis von $V$ mit $n \ge 1$ und $w^{(1)}, \dots, w^{(n)} \in W$.
Zeigen Sie, dass es genau eine lineare Abbildung $f\colon V \to W$ mit $f(b^{(j)}) = w^{(j)}$ für alle $j$ gibt.
""",
    r"""
**Existenz.** Nach Satz 4.55 hat jedes $v \in V$ eine eindeutige Darstellung $v = \sum_{j=1}^n x_j b^{(j)}$. Daher ist $f(v) := \sum_{j=1}^n x_j w^{(j)}$ wohldefiniert.
Für $b^{(j)}$ ist der Koeffizient an Stelle $j$ gleich $1$, sonst $0$, also $f(b^{(j)}) = w^{(j)}$.

**Linearität.** Für $v = \sum x_j b^{(j)}$, $v' = \sum y_j b^{(j)}$ und $\lambda \in K$ gilt $v + v' = \sum (x_j + y_j) b^{(j)}$ und $\lambda v = \sum (\lambda x_j) b^{(j)}$.
Also $f(v + v') = \sum (x_j + y_j) w^{(j)} = f(v) + f(v')$ und $f(\lambda v) = \sum \lambda x_j w^{(j)} = \lambda f(v)$.

**Eindeutigkeit.** Ist $g$ linear mit $g(b^{(j)}) = w^{(j)}$, so gilt nach Satz 5.8 $g(v) = \sum x_j g(b^{(j)}) = \sum x_j w^{(j)} = f(v)$. Also $g = f$. $\square$
""",
    ["Die eindeutige Basisdarstellung (Satz 4.55) wird für die Wohldefiniertheit genannt",
     "Es wird nachgerechnet, dass $f(b^{(j)}) = w^{(j)}$ gilt",
     "Beide Linearitätsbedingungen werden über die Koordinaten gezeigt (Addition und Skalar)",
     "Die Eindeutigkeit wird mit Satz 5.8 begründet"],
    "Erst Existenz durch Definition über die Koordinaten, dann Linearität, dann Eindeutigkeit über Satz 5.8.",
    tipps=["Warum ist die Vorschrift $\\sum x_j b^{(j)} \\mapsto \\sum x_j w^{(j)}$ überhaupt eine Abbildung?"])

k.papier(r"""
## Übungsblatt-Stil: Kern, Injektivität und gleiche Dimension

Sei $f\colon V \to W$ linear zwischen endlichdimensionalen Vektorräumen.

1. Zeigen Sie: $f$ ist genau dann injektiv, wenn $\ker(f) = \{0_V\}$ gilt.
2. Sei zusätzlich $\dim V = \dim W$. Zeigen Sie: $f$ ist genau dann injektiv, wenn $f$ surjektiv ist.
3. Geben Sie eine lineare Abbildung $\mathbb{R}^2 \to \mathbb{R}^3$ an, die injektiv, aber nicht surjektiv ist.
""",
    r"""
**1.** „$\Rightarrow$“: Ist $v \in \ker(f)$, so gilt $f(v) = 0 = f(0)$, wegen der Injektivität also $v = 0$. „$\Leftarrow$“: Aus $f(v) = f(w)$ folgt $f(v - w) = f(v) - f(w) = 0$, also $v - w \in \ker(f) = \{0\}$ und $v = w$.

**2.** Nach Teil 1 und der Dimensionsformel gilt $f$ injektiv $\iff \dim\ker(f) = 0 \iff \mathrm{rang}(f) = \dim V = \dim W$. Ein Untervektorraum von $W$ mit Dimension $\dim W$ ist ganz $W$ (Satz 4.74). Also $f(V) = W$, d. h. $f$ ist surjektiv. Die Rückrichtung geht ebenso: $f(V) = W$ gibt $\mathrm{rang}(f) = \dim W = \dim V$, also $\dim\ker(f) = 0$.

**3.** $(u, v)^\top \mapsto (u, 0, v)^\top$: Der Kern ist $\{0\}$, aber $(0, 1, 0)^\top$ wird nicht getroffen (Bemerkung 5.24). $\square$
""",
    ["Bei 1 beide Richtungen gezeigt, die Rückrichtung über $f(v - w) = 0$",
     "Bei 2 die Dimensionsformel eingesetzt und $\\mathrm{rang}(f) = \\dim W$ gefolgert",
     "Bei 2 benutzt, dass ein Untervektorraum von voller Dimension der ganze Raum ist",
     "Bei 3 ein Beispiel genannt, Injektivität begründet und ein nicht getroffenes Element angegeben"],
    "Kernkriterium für Injektivität, danach Dimensionsformel: Kern $0$ heißt Rang gleich $\\dim V$.",
    uebungsblatt=True,
    tipps=["Für 1: Wende die Linearität auf $f(v) - f(w)$ an.", "Für 2: Dimensionsformel, dann Satz 4.74.", "Für 3: Füge eine feste Null-Koordinate ein."])

k.zusammenfassung(G(r"""
## Lineare Abbildungen (Skript Abschn. 5.1 und 5.2)

- **Linear** (Def. 5.1): $f(v + w) = f(v) + f(w)$ und $f(\lambda v) = \lambda f(v)$, gleichwertig $f(\lambda v + \mu w) = \lambda f(v) + \mu f(w)$. Bijektiv: **Isomorphismus**.
- Beispiele: Streckung, Nullabbildung, Projektion, Spiegelung $s_G = 2\pi_G - \mathrm{id}$, Koordinatenabbildung $\kappa$, $m_z$. **Nicht** linear: Verschiebung, konstant $\neq 0$, $x^2$. Die Konjugation ist über $\mathbb{R}$, nicht über $\mathbb{C}$ linear.
- **Satz 5.8:** $f(0) = 0$, $f(-v) = -f(v)$, $f(\sum \lambda_j v^{(j)}) = \sum \lambda_j f(v^{(j)})$.
- **Satz 5.9:** Zu einer Basis $b^{(1)}, \dots, b^{(n)}$ und beliebigen $w^{(j)}$ gibt es genau eine lineare $f$ mit $f(b^{(j)}) = w^{(j)}$.
- $\mathrm{Hom}_K(V, W)$ ist ein Vektorraum; Verkettungen und Umkehrungen linearer Abbildungen sind linear (Bsp. 5.11, Beob. 5.13).
- **Kern, Bild, Rang** (Satz 5.14, Def. 5.15): $\ker(f)$ und $f(V) = \langle f(b^{(1)}), \dots, f(b^{(n)}) \rangle$ sind Untervektorräume, $\mathrm{rang}(f) = \dim f(V)$.
- **Beob. 5.17:** $f(v) = f(w) \iff v - w \in \ker(f)$. $f$ injektiv $\iff \ker(f) = \{0\}$.
- **Satz 5.18:** $f^{-1}(\{y\}) = v^{(0)} + \ker(f)$, Dimension $\dim V - \mathrm{rang}(f)$ (Kor. 5.21).
- **Satz 5.20 (Dimensionsformel):** $\dim V = \dim\ker(f) + \mathrm{rang}(f)$.
- **Satz 5.23:** Bei $\dim V = \dim W < \infty$ gilt injektiv $\iff$ surjektiv. **Kor. 5.25:** isomorph $\iff$ gleiche Dimension.

!! Linear heißt: nur die Basisbilder zählen. Der Kern verschluckt Dimensionen, der Rest ist der Rang.
"""))
