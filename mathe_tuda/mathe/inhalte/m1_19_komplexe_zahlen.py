# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 19: Die komplexen Zahlen (Skript Disser WS 26/27, Abschn. 3.7 und 3.8, Def. 3.94 bis Bsp. 3.110)."""
from fractions import Fraction as F
from itertools import product
from math import isqrt

from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(
    slug="komplexe_zahlen_uni",
    titel="Die komplexen Zahlen",
    beschreibung="ℂ = ℝ², Rechnen in kartesischer Darstellung, Konjugation, Betrag, Inverse und Division, keine Anordnung, Fundamentalsatz der Algebra, Zahlbereiche",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 3.7 und 3.8",
    icon="🌀")


# ── Python: ℂ als Paare über ℚ ───────────────────────────────────────────
def cadd(z, w):
    return (z[0] + w[0], z[1] + w[1])


def csub(z, w):
    return (z[0] - w[0], z[1] - w[1])


def cmul(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def cconj(z):
    return (z[0], -z[1])


def cabs2(z):
    return z[0] ** 2 + z[1] ** 2


def cinv(z):
    n = cabs2(z)
    return (z[0] / n, -z[1] / n)


def cdiv(w, z):
    return cmul(w, cinv(z))


def ctex(z, mit_klammer=False):
    """Komplexe Zahl als x + yi im LaTeX-Format."""
    x, y = F(z[0]), F(z[1])

    def num(v):
        v = abs(v)
        return str(v.numerator) if v.denominator == 1 else f"\\frac{{{v.numerator}}}{{{v.denominator}}}"
    if y == 0:
        t = ("-" if x < 0 else "") + num(x)
    elif x == 0:
        t = ("-" if y < 0 else "") + ("" if abs(y) == 1 else num(y)) + "i"
    else:
        t = ("-" if x < 0 else "") + num(x) + (" - " if y < 0 else " + ") + ("" if abs(y) == 1 else num(y)) + "i"
    return f"({t})" if mit_klammer else t


def vtext(z):
    return [str(F(z[0])), str(F(z[1]))]


def rechnung(zeilen):
    """Zeilen mit komplexen Termen werden nicht automatisch nachgerechnet ('?? ' davor)."""
    return ":::rechnung\n" + "\n".join(f"?? {t} || {g}" for t, g in zeilen) + "\n:::"


def rechnung_zahlen(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


_Z = [(F(a), F(b)) for a in range(-3, 4) for b in range(-3, 4)]
# Körperaxiome (Satz 3.96) und Rechenregeln (Satz 3.103) an Stichproben
for z, w in product(_Z[::4], repeat=2):
    assert cmul(z, w) == cmul(w, z) and cadd(z, w) == cadd(w, z)
    assert cconj(cadd(z, w)) == cadd(cconj(z), cconj(w)) and cconj(cmul(z, w)) == cmul(cconj(z), cconj(w))
    assert cabs2(cmul(z, w)) == cabs2(z) * cabs2(w)                       # |zw|² = |z|²|w|²
    assert cabs2(cadd(z, w)) <= (cabs2(z) ** F(1, 2) + cabs2(w) ** F(1, 2)) ** 2 + F(1, 10 ** 9)
for z in _Z:
    assert cmul(z, cconj(z)) == (cabs2(z), F(0))
    if z != (0, 0):
        assert cmul(z, cinv(z)) == (1, 0) and cinv(z) == (cconj(z)[0] / cabs2(z), cconj(z)[1] / cabs2(z))
for z, w, t in product(_Z[::7], repeat=3):
    assert cmul(cmul(z, w), t) == cmul(z, cmul(w, t)) and cmul(z, cadd(w, t)) == cadd(cmul(z, w), cmul(z, t))
_i = (F(0), F(1))
assert cmul(_i, _i) == (-1, 0) and cadd(cmul(_i, _i), (1, 0)) == (0, 0)
# Beispiele 3.100 und 3.104
assert cadd((2, 3), (1, -5)) == (3, -2) and cmul((2, 3), (1, -5)) == (17, -7)
assert cconj((3, 4)) == (3, -4) and cabs2((3, 4)) == 25 and cinv((F(3), F(4))) == (F(3, 25), F(-4, 25))
# Einleitung zu 3.7: a_n = ½ (q^n + (-q)^n) mit q = i gibt 1, 0, -1, 0, ...
_q = 1j
assert [round((0.5 * (_q ** n + (-_q) ** n)).real) for n in range(8)] == [1, 0, -1, 0, 1, 0, -1, 0]
assert all(abs((0.5 * (_q ** n + (-_q) ** n)).imag) < 1e-12 for n in range(8))
# Beispiel 3.110 und X^4 - 1
assert cmul((0, 1), (0, -1)) == (1, 0) and cadd(cmul((0, 1), (0, 1)), (1, 0)) == (0, 0)
# Beobachtung 3.107: über Z/2Z haben X² und X dieselbe Funktion
assert all((x * x) % 2 == x % 2 for x in range(2))
# Satz 3.101: -1 wäre sonst negativ, aber i² = -1
assert cmul(_i, _i) == (-1, 0)

k.lernziele([
    "Ich kann $\\mathbb{C} = \\mathbb{R}^2$ definieren und mit Paaren und in kartesischer Form $z = x + yi$ addieren und multiplizieren (Def. 3.94, 3.95, 3.97, Satz 3.99)",
    "Ich kann die konjugiert komplexe Zahl, den Betrag und das Inverse bestimmen und komplexe Zahlen dividieren (Def. 3.102, Satz 3.96, 3.103)",
    "Ich kann begründen, warum $\\mathbb{C}$ ein Körper ist, aber nicht angeordnet werden kann (Satz 3.96, 3.101)",
    "Ich kenne den Fundamentalsatz der Algebra, kann quadratische Gleichungen mit negativer Diskriminante lösen und die Zahlbereiche $\\mathbb{N} \\subseteq \\mathbb{Z} \\subseteq \\mathbb{Q} \\subseteq \\mathbb{R} \\subseteq \\mathbb{C}$ einordnen (Satz 3.109, Abschn. 3.8)",
])

k.warum(r"""
Signale, Schwingungen und Fourier-Transformation (Audio, Bild, WLAN) werden mit komplexen Zahlen beschrieben:
Sie machen aus „sin und cos“ eine einzige Exponentialfunktion. In der Informatik begegnen sie dir in der schnellen
Fourier-Transformation (FFT), in der Computergrafik (Drehungen in der Ebene), in der Quanteninformatik und in der
Eigenwerttheorie: Eine reelle Matrix kann komplexe Eigenwerte haben (Kap. „Eigenwerte“). Dieses Kapitel ist auch dein
einziger Einstieg in komplexe Zahlen im Lernsystem. Es enthält deshalb alles, was du für Mathe 1 und 2 rechnen können musst.
""")

# ── Seite 1: Motivation ──────────────────────────────────────────────────
k.erklaerung("Warum noch eine Erweiterung?", r"""
## Eine Wurzel aus −1

In einem [[angeordneten Körper|angeordneter Körper]] sind Quadrate nie negativ (Satz 3.78). Deshalb hat $x^2 + 1 = 0$ **keine** reelle Lösung.

Warum sollte man trotzdem eine Zahl $q$ mit $q^2 + 1 = 0$ wollen? Das Skript zeigt ein Beispiel aus der Signalverarbeitung:
$$a_0 = 1,\ a_1 = 0,\ a_2 = -1,\ a_3 = 0,\ a_4 = 1,\ \ldots \quad\text{ist}\quad a_n = \tfrac12\left(q^n + (-q)^n\right).$$
Ohne $q$ brauchst du eine Fallunterscheidung ($a_{4k} = 1$, $a_{4k+2} = -1$, $a_{2k+1} = 0$). Mit $q$ ist es eine Formel.

:::rechnung Die Formel für $n = 0, 1, 2, 3$ mit $q^2 = -1$
(1 + 1)/2 = 1 || $n = 0$: $q^0 + (-q)^0 = 1 + 1$
?? (q + (-q))/2 = 0 || $n = 1$: $q + (-q) = 0$
?? (q^2 + q^2)/2 = -1 || $n = 2$: $(-q)^2 = q^2 = -1$, also $\frac12(-1 + -1)$
?? (q^3 + (-q)^3)/2 = 0 || $n = 3$: $(-q)^3 = -q^3$, die beiden Summanden heben sich auf
:::

Wir suchen also einen Zahlbereich, der $\mathbb{R}$ enthält und in dem $x^2 + 1 = 0$ lösbar ist: die **komplexen Zahlen**.

:::alt Als Drehung
Die Multiplikation mit $q$ soll „zweimal angewendet“ die Zahl umdrehen ($q \cdot q = -1$). Auf einer Geraden gibt es nur vorwärts und rückwärts. Doch in der Ebene kann man **um $90^\circ$ drehen**: Zweimal gedreht ist wie $180^\circ$, also umgedreht. $q$ ist die Drehung um $90^\circ$.
:::
""")

k.mc("Warum hat $x^2 + 1 = 0$ keine Lösung in $\\mathbb{R}$?",
     ["In einem angeordneten Körper ist $x^2 \\ge 0$, also $x^2 + 1 \\ge 1 > 0$",
      "Weil $\\sqrt{-1}$ nicht auf dem Taschenrechner steht",
      "Weil $\\mathbb{R}$ nicht vollständig ist",
      "Weil $x^2 + 1$ nicht assoziativ ist"],
     "Nach Satz 3.78 gilt $x^2 \\ge 0$ in jedem angeordneten Körper, also $x^2 + 1 \\ge 1$. Vollständigkeit hilft dabei nicht, $\\mathbb{R}$ ist vollständig.",
     tipps=["Welches Vorzeichen kann $x^2$ in $\\mathbb{R}$ haben?", "Was folgt für $x^2 + 1$?"],
     fehler={"Weil $\\sqrt{-1}$ nicht auf dem Taschenrechner steht": "Das ist ein Symptom, nicht der mathematische Grund. Der Grund ist $x^2 \\ge 0$.",
             "Weil $\\mathbb{R}$ nicht vollständig ist": "$\\mathbb{R}$ ist vollständig (R2). Es fehlen trotzdem Lösungen, weil Quadrate nie negativ sind.",
             "Weil $x^2 + 1$ nicht assoziativ ist": "Assoziativität ist eine Eigenschaft einer Verknüpfung, nicht eines Terms."})

# ── Seite 2: Definition 3.94 und 3.95 ────────────────────────────────────
k.erklaerung("Definition 3.94 und 3.95: ℂ als Ebene", r"""
## Paare reeller Zahlen

**Definition 3.94.** $\mathbb{C} := \mathbb{R}^2$. Jede reelle Zahl $x$ wird mit $(x, 0) \in \mathbb{C}$ identifiziert. Zahlen $(x, 0)$ heißen **reell**, Zahlen $(0, y)$ **imaginär**.

**Definition 3.95.** Für $(x_1, y_1), (x_2, y_2) \in \mathbb{C}$ ist
$$(x_1, y_1) + (x_2, y_2) := (x_1 + x_2,\ y_1 + y_2),$$
$$(x_1, y_1) \cdot (x_2, y_2) := (x_1 x_2 - y_1 y_2,\ x_1 y_2 + y_1 x_2).$$

Die Addition ist die Vektoraddition der Ebene. Die Multiplikation ist neu: Sie dreht und streckt.

:::visual komplexe_ebene
{"z": [2, 3], "w": [1, -5], "op": "mal", "interaktiv": true,
 "unterschrift": "Ein Punkt der Ebene ist eine komplexe Zahl. Die Multiplikation $(2, 3) \\cdot (1, -5) = (17, -7)$ ist eine Drehstreckung."}
:::

:::rechnung Summe und Produkt von $(2, 3)$ und $(1, -5)$
(2 + 1,\ 3 + (-5)) = (3, -2) || Addition komponentenweise
2 \cdot 1 - 3 \cdot (-5) = 17 || erster Eintrag des Produkts: $x_1 x_2 - y_1 y_2$
2 \cdot (-5) + 3 \cdot 1 = -7 || zweiter Eintrag: $x_1 y_2 + y_1 x_2$, also $(17, -7)$
:::

:::achtung Nicht komponentenweise multiplizieren
$(x_1, y_1) \cdot (x_2, y_2)$ ist **nicht** $(x_1 x_2,\ y_1 y_2)$. Das Minuszeichen in $x_1 x_2 - y_1 y_2$ kommt von $i^2 = -1$ (nächste Seite).
:::

:::alt Als Ebenenrechner
Die Addition legt Pfeile aneinander. Die Multiplikation multipliziert die Längen (Beträge) und addiert die Drehwinkel. Dass dabei komponentenweises Multiplizieren **nicht** herauskommt, siehst du am Bild: Es entstünde keine Drehung.
:::
""")

# ── Seite 3: Satz 3.96 ───────────────────────────────────────────────────
k.erklaerung("Satz 3.96: ℂ ist ein Körper", r"""
## Auch das Inverse existiert

**Satz 3.96.** $(\mathbb{C}, +, \cdot)$ ist ein [[Körper]] mit Nullelement $(0, 0)$ und Einselement $(1, 0)$. Für $(x, y) \ne (0, 0)$ gilt
$$(x, y)^{-1} = \left(\frac{x}{x^2 + y^2},\ \frac{-y}{x^2 + y^2}\right).$$

*Beweis (Auszug).* $(\mathbb{C}, +)$ ist abelsche Gruppe, $\cdot$ ist assoziativ, kommutativ, distributiv, und $z \cdot (1, 0) = (a \cdot 1 - b \cdot 0,\ a \cdot 0 + b \cdot 1) = z$.
Für $(x, y) \ne (0, 0)$ ist $x^2 + y^2 > 0$ (Satz 3.78), und
$$(x, y)\left(\tfrac{x}{x^2 + y^2}, \tfrac{-y}{x^2 + y^2}\right) = \left(\tfrac{x^2 + y^2}{x^2 + y^2},\ \tfrac{-xy + yx}{x^2 + y^2}\right) = (1, 0).$$

:::rechnung Inverses von $(3, 4)$
3^2 + 4^2 = 25 || $x^2 + y^2$ mit $x = 3$, $y = 4$
?? (3/25,\ -4/25) || das Inverse $(\frac{3}{25}, \frac{-4}{25})$
3 \cdot (3/25) - 4 \cdot (-4/25) = 1 || Probe, erster Eintrag: $\frac{9 + 16}{25} = 1$
3 \cdot (-4/25) + 4 \cdot (3/25) = 0 || Probe, zweiter Eintrag: $\frac{-12 + 12}{25} = 0$
:::

:::alt Als Rückdrehung
Das Inverse macht rückgängig, was $z$ getan hat: Es dreht zurück und streckt auf die Länge $1/|z|$. Deshalb steht der Betrag im Nenner.
:::
""")

k.vektor("Bestimme das Inverse von $z = (0, 2)$ in $\\mathbb{C}$ nach Satz 3.96, als Paar $(x, y)$. Eintrag 1 ist der Realteil, Eintrag 2 der Imaginärteil.",
         [0, F(-1, 2)],
         "$x^2 + y^2 = 0 + 4 = 4$. Also $z^{-1} = (\\frac{0}{4}, \\frac{-2}{4}) = (0, -\\frac12)$. Probe: $(0, 2)(0, -\\frac12) = (0 \\cdot 0 - 2 \\cdot (-\\frac12),\\ 0 \\cdot (-\\frac12) + 2 \\cdot 0) = (1, 0)$.",
         tipps=["Formel: $(x, y)^{-1} = (\\frac{x}{x^2 + y^2}, \\frac{-y}{x^2 + y^2})$.", "Hier $x = 0$, $y = 2$, $x^2 + y^2 = 4$.", "$\\frac{-2}{4} = -\\frac12$."],
         rechenweg=rechnung_zahlen([("0^2 + 2^2 = 4", "$x^2 + y^2$"), ("-2/4 = -1/2", "zweiter Eintrag $\\frac{-y}{x^2 + y^2}$")]),
         typische_fehler=[([0, F(1, 2)], "Das Vorzeichen des Imaginärteils fehlt: Im Zähler steht $-y$."),
                          ([0, F(1, 2) * -1 * 2], "Du hast nicht durch $x^2 + y^2 = 4$ geteilt, sondern nur $-y$ genommen.")])

# ── Seite 4: i und kartesische Darstellung ───────────────────────────────
k.erklaerung("Definition 3.97 bis Satz 3.99: i und die kartesische Darstellung", r"""
## Aus Paaren wird $x + yi$

**Definition 3.97.** Die [[imaginäre Einheit]] ist $i := (0, 1)$. Für $z = (x, y)$ ist $\operatorname{Re}(z) := x$ der [[Realteil|Realteil]] und $\operatorname{Im}(z) := y$ der [[Imaginärteil]].

**Beobachtung 3.98.** $i^2 = -1$, und jedes $z \in \mathbb{C}$ hat genau eine Darstellung $z = x + yi$ mit $x, y \in \mathbb{R}$ (kartesische Darstellung).

*Warum:* $i \cdot i = (0 \cdot 0 - 1 \cdot 1,\ 0 \cdot 1 + 1 \cdot 0) = (-1, 0) = -1$ und $x + yi = (x, 0) + (y, 0)(0, 1) = (x, y)$.

**Satz 3.99.** Für $z = x + yi$, $w = u + vi$:
$$z + w = (x + u) + (y + v)i,\qquad zw = (xu - yv) + (xv + yu)i.$$
Das ist einfach Ausmultiplizieren mit $i^2 = -1$.

:::rechnung Beispiel 3.100
?? (2 + 3i) + (1 - 5i) = 3 - 2i || Real- und Imaginärteile getrennt addieren
?? (2 + 3i)(1 - 5i) = 2 - 10i + 3i - 15i^2 || ausmultiplizieren, wie bei zwei Klammern
?? 2 - 10i + 3i - 15i^2 = 2 - 7i + 15 || $i^2 = -1$ einsetzen: $-15 \cdot (-1) = +15$
?? 2 - 7i + 15 = 17 - 7i || Realteile ($2 + 15$) und Imaginärteile ($-10 + 3$) zusammenfassen
:::

$i$ und $-i$ lösen $x^2 + 1 = 0$: $i^2 = -1$ und $(-i)^2 = (-1)^2 i^2 = -1$.

:::alt Als Polynomrechnung
Rechne einfach wie mit Buchstaben, ersetze am Ende $i^2$ durch $-1$ und sortiere in Teile mit und ohne $i$. Das ist wie $(a + b\sqrt{2})(c + d\sqrt{2})$ mit $\sqrt{2}^2 = 2$.
:::
""")

k.vektor("Berechne $(2 + 3i)(1 - 5i)$ mit Satz 3.99 und gib das Ergebnis als Paar (Realteil, Imaginärteil) an.", [17, -7],
         "$(2 + 3i)(1 - 5i) = 2 - 10i + 3i - 15i^2 = 2 + 15 + (-10 + 3)i = 17 - 7i$ (Beispiel 3.100).",
         tipps=["Multipliziere jeden Summanden mit jedem: Es sind vier Produkte.", "$-15i^2 = +15$.", "Realteil $2 + 15$, Imaginärteil $-10 + 3$."],
         rechenweg=rechnung([("(2 + 3i)(1 - 5i) = 2 - 10i + 3i - 15i^2", "vier Produkte"), ("2 - 10i + 3i - 15i^2 = 17 - 7i", "$i^2 = -1$ und zusammenfassen")]),
         typische_fehler=[([-13, -7], "Du hast $-15i^2 = -15$ gerechnet statt $+15$. Wegen $i^2 = -1$ wechselt das Vorzeichen."),
                          ([2, -15], "Komponentenweise multipliziert. Richtig ist: alle vier Produkte, dann $i^2 = -1$.")])

k.wf("$i$ und $-i$ sind beide Lösungen von $x^2 + 1 = 0$ in $\\mathbb{C}$.", True,
     "$i^2 = -1$, also $i^2 + 1 = 0$. Ebenso $(-i)^2 = (-1)^2 \\cdot i^2 = -1$ (Beispiel 3.100).",
     tipps=["Quadriere $-i$: $(-i)^2 = (-1)^2 i^2$."])

# ── Seite 5: Konjugation und Betrag ──────────────────────────────────────
k.erklaerung("Definition 3.102 und Satz 3.103: Konjugation und Betrag", r"""
## Spiegeln und Messen

**Definition 3.102.** Für $z = x + yi$ ist die konjugiert komplexe Zahl $\bar z := x - yi$ und der Betrag $|z| := \sqrt{x^2 + y^2}$. Der [[Betrag]] setzt den reellen Betrag fort: $|(x, 0)| = \sqrt{x^2} = |x|$.

**Satz 3.103.** Für alle $z, w \in \mathbb{C}$:
$$\bar{\bar z} = z,\quad \overline{z + w} = \bar z + \bar w,\quad \overline{zw} = \bar z\,\bar w,\quad z\bar z = |z|^2,\quad |zw| = |z||w|,\quad |z + w| \le |z| + |w|.$$
$|z| = 0 \iff z = 0$, und für $z \ne 0$ ist $z^{-1} = \dfrac{\bar z}{|z|^2}$.

*Beweis von $z\bar z = |z|^2$:* $(x + yi)(x - yi) = x^2 - xyi + xyi - y^2 i^2 = x^2 + y^2$.

:::visual komplexe_ebene
{"z": [3, 4], "op": "konjugiert", "interaktiv": true,
 "unterschrift": "$\\bar z$ ist die Spiegelung von $z$ an der reellen Achse. $|z|$ ist der Abstand zum Ursprung: $|3 + 4i| = 5$."}
:::

:::rechnung Beispiel 3.104 mit $z = 3 + 4i$
?? \bar z = 3 - 4i || Vorzeichen des Imaginärteils wechseln
\sqrt{3^2 + 4^2} = 5 || $|z| = \sqrt{x^2 + y^2}$
?? z \bar z = (3 + 4i)(3 - 4i) = 9 + 16 = 25 || $= |z|^2$: reell und nichtnegativ
?? z^{-1} = (3 - 4i)/25 || $\bar z / |z|^2$
:::

:::alt Als Spiegel und Lineal
$\bar z$ ist das Spiegelbild von $z$ an der waagerechten Achse. $|z|$ ist die Länge des Pfeils vom Ursprung zu $z$, also der Satz des Pythagoras. $z \bar z$ ist das Quadrat dieser Länge, immer eine reelle Zahl.
:::
""")

k.luecke("Für $z = 3 + 4i$ gilt $|z| = \\sqrt{3^2 + \\luecke} = \\luecke$.",
         "|z| = \\sqrt{3^2 + \\luecke} = \\luecke",
         [[16], [5]],
         "$|z| = \\sqrt{x^2 + y^2} = \\sqrt{9 + 16} = \\sqrt{25} = 5$ (Beispiel 3.104).",
         tipps=["Der Imaginärteil ist $4$, quadriert $16$.", "$9 + 16 = 25$.", "Die Lücken sind $16$ und $5$."],
         rechenweg=rechnung_zahlen([("3^2 + 4^2 = 25", "$x^2 + y^2$"), ("\\sqrt{25} = 5", "Wurzel")]),
         typische_fehler=[([4, 7], "Du hast $4$ statt $4^2 = 16$ eingesetzt: Der Imaginärteil wird quadriert.")])

k.zahl("Bestimme $|5 - 12i|$.", 13,
       "$|5 - 12i| = \\sqrt{5^2 + (-12)^2} = \\sqrt{25 + 144} = \\sqrt{169} = 13$. Das Vorzeichen des Imaginärteils verschwindet beim Quadrieren.",
       tipps=["Formel $\\sqrt{x^2 + y^2}$ mit $x = 5$, $y = -12$.", "$(-12)^2 = 144$.", "$\\sqrt{169}$."],
       rechenweg=rechnung_zahlen([("5^2 + (-12)^2 = 169", "$25 + 144$"), ("\\sqrt{169} = 13", "Wurzel")]),
       typische_fehler=[(7, "Das ist $5 + (-12)$ in Betrag... Der Betrag ist $\\sqrt{x^2 + y^2}$, nicht $x + y$."),
                        (169, "Das ist $x^2 + y^2 = |z|^2$. Es fehlt die Wurzel.")])

k.mehrfach("Welche Aussagen gelten für alle $z, w \\in \\mathbb{C}$?",
           ["$z\\bar z = |z|^2$", "$|zw| = |z||w|$", "$\\overline{zw} = \\bar z\\,\\bar w$"],
           ["$|z + w| = |z| + |w|$", "$z\\bar z = z^2$", "$\\bar z = -z$"],
           "Satz 3.103 liefert die ersten drei. $|z + w| \\le |z| + |w|$ ist nur eine Ungleichung (Gleichheit bei gleicher Richtung). $z\\bar z = |z|^2 \\ne z^2$ im Allgemeinen: $i \\cdot (-i) = 1$, aber $i^2 = -1$. $\\bar z = -z$ gilt nur für rein imaginäre $z$.",
           tipps=["Teste mit $z = i$ und $w = 1$.", "Für $z = i$: $z\\bar z = i \\cdot (-i) = 1$ und $z^2 = -1$."],
           fehler={"$|z + w| = |z| + |w|$": "Für $z = 1$ und $w = i$ ist $|1 + i| = \\sqrt{2} < 2 = |1| + |i|$.",
                   "$z\\bar z = z^2$": "$i \\cdot \\bar i = 1$, aber $i^2 = -1$.",
                   "$\\bar z = -z$": "Für $z = 1$ ist $\\bar z = 1 \\ne -1$."})

# ── Seite 6: Division ────────────────────────────────────────────────────
k.erklaerung("Division komplexer Zahlen", r"""
## Mit dem Konjugierten erweitern

Weil $z^{-1} = \bar z / |z|^2$ (Satz 3.103), dividierst du so:
$$\frac{w}{z} = w \cdot z^{-1} = \frac{w\,\bar z}{z\,\bar z} = \frac{w\,\bar z}{|z|^2}.$$
Du **erweiterst** den Bruch mit $\bar z$. Der Nenner wird reell.

:::rechnung $\dfrac{1 + 2i}{3 - i}$
?? (1 + 2i)/(3 - i) = ((1 + 2i)(3 + i))/((3 - i)(3 + i)) || mit dem Konjugierten $3 + i$ des Nenners erweitern
?? (1 + 2i)(3 + i) = 3 + i + 6i + 2i^2 = 1 + 7i || Zähler: $3 + 7i - 2$
?? (3 - i)(3 + i) = 9 + 1 = 10 || Nenner: $|3 - i|^2 = 10$, reell
?? (1 + 7i)/10 = 1/10 + (7/10)i || Realteil $\frac1{10}$, Imaginärteil $\frac7{10}$
:::

:::achtung Nicht komponentenweise teilen
$\frac{1 + 2i}{3 - i}$ ist **nicht** $\frac13 + \frac{2}{-1}i$. Immer mit dem Konjugierten des **Nenners** erweitern.
:::

:::alt Als Wurzelnenner
Wie bei $\frac{1}{1 + \sqrt{2}}$, wo du mit $1 - \sqrt{2}$ erweiterst, damit die Wurzel verschwindet (dritte binomische Formel). Hier verschwindet $i$, weil $(a + bi)(a - bi) = a^2 + b^2$.
:::
""")

k.vektor("Berechne $\\dfrac{1 + 2i}{3 - i}$ und gib das Ergebnis als Paar (Realteil, Imaginärteil) an (Brüche wie `1/10` sind erlaubt).", [F(1, 10), F(7, 10)],
         "Erweitere mit $3 + i$: $\\frac{(1 + 2i)(3 + i)}{(3 - i)(3 + i)} = \\frac{3 + i + 6i + 2i^2}{9 + 1} = \\frac{1 + 7i}{10}$.",
         tipps=["Erweitere mit dem Konjugierten des Nenners: $3 + i$.", "Nenner: $(3 - i)(3 + i) = 9 + 1 = 10$.", "Zähler: $3 + i + 6i - 2 = 1 + 7i$."],
         rechenweg=rechnung([("(1 + 2i)(3 + i) = 3 + 7i - 2 = 1 + 7i", "Zähler"), ("(3 - i)(3 + i) = 10", "Nenner reell")]),
         typische_fehler=[([F(1, 3), -2], "Komponentenweise geteilt. Du musst mit dem Konjugierten des Nenners erweitern."),
                          ([F(7, 10), F(1, 10)], "Real- und Imaginärteil vertauscht: $\\frac{1 + 7i}{10}$ hat Realteil $\\frac1{10}$.")])

# ── Seite 7: nicht anordenbar; Konjugation als Automorphismus ───────────
k.erklaerung("Satz 3.101 und 3.105: Keine Ordnung, aber ein Automorphismus", r"""
## Was ℂ nicht kann und was es dafür hat

**Satz 3.101.** Es gibt keine Totalordnung auf $\mathbb{C}$, die $(\mathbb{C}, +, \cdot)$ zu einem [[angeordneten Körper|angeordneter Körper]] macht.

*Beweis.* In einem angeordneten Körper gilt $1 > 0$, also $-1 < 0$, und alle Quadrate sind $\ge 0$ (Satz 3.78). Aber $i^2 = -1 < 0$. Widerspruch.

**Satz 3.105.** Die Konjugation $z \mapsto \bar z$ ist ein nichttrivialer Körperautomorphismus von $\mathbb{C}$. Es gilt $z = \bar z$ genau dann, wenn $z$ reell ist.

*Beweis.* Sie erhält $+$ und $\cdot$ (Satz 3.103) und $\bar 1 = 1$, ist wegen $\bar{\bar z} = z$ bijektiv, und $\bar i = -i \ne i$. Außerdem: $x + yi = x - yi \iff y = 0$.

:::rechnung Quadrat-Test und Spiegelbild
?? i^2 = -1 || ein Quadrat ist negativ: in einem angeordneten Körper unmöglich
?? \overline{i} = -i || die Konjugation ist nicht die Identität
?? \overline{(1 + i)(2 - i)} = (1 - i)(2 + i) = 3 - i || erst multiplizieren und konjugieren oder umgekehrt: gleich ($(1 + i)(2 - i) = 3 + i$)
:::

:::alt Als Zahlengerade
Eine Anordnung stellt alle Zahlen auf eine Gerade. $\mathbb{C}$ ist eine Ebene, und die Quadrate von $i$ landen bei $-1$ links von der $0$. Das passt nicht zusammen. Man kann komplexe Zahlen nach Betrag oder Richtung sortieren, aber nicht so, dass Rechnen und Ordnung zusammenspielen.
:::
""")

k.ordnen("Ordne den Beweis von Satz 3.101: $\\mathbb{C}$ lässt sich nicht zu einem angeordneten Körper machen.",
         ["Angenommen, es gäbe eine Totalordnung $\\le$, die $(\\mathbb{C}, +, \\cdot, \\le)$ zu einem angeordneten Körper macht.",
          "Nach Satz 3.78 gilt dann $1 > 0$ und damit $-1 < 0$.",
          "Nach Satz 3.78 (ii) ist außerdem jedes Quadrat $\\ge 0$.",
          "Wegen $i^2 = -1$ wäre das Quadrat $i^2$ negativ. Das ist ein Widerspruch.",
          "Also gibt es keine solche Ordnung. $\\square$"],
         "Widerspruchsbeweis: Annahme, zwei Folgerungen aus Satz 3.78 und das Quadrat $i^2 = -1$ als Widerspruch.",
         ablenker=["Da $\\mathbb{C}$ zweidimensional ist, lässt es sich nicht ordnen."],
         tipps=["Beginne mit der Annahme, dass es eine Ordnung gibt.", "Welche beiden Aussagen kennst du aus Satz 3.78?", "Welche Zahl hat das Quadrat $-1$?"])

k.wf("Man kann $\\mathbb{C}$ so anordnen, dass $(\\mathbb{C}, +, \\cdot, \\le)$ ein angeordneter Körper ist.", False,
     "Satz 3.101: Wegen $i^2 = -1 < 0$ ist das unmöglich. Es gibt Ordnungen auf der **Menge** $\\mathbb{C}$ (z. B. lexikographisch), aber keine, die mit $+$ und $\\cdot$ verträglich ist.",
     tipps=["Quadrate sind in angeordneten Körpern nichtnegativ. Was ist $i^2$?"])

# ── Seite 8: Polynome und Fundamentalsatz ────────────────────────────────
k.erklaerung("Definition 3.106 bis Satz 3.109: Polynome und der Fundamentalsatz", r"""
## Jedes Polynom zerfällt in Linearfaktoren

**Definition 3.106.** Ein [[Polynom]] über einem Körper $K$ ist $\sum_{j=0}^{n} a_j X^j$ mit Koeffizienten $a_j \in K$ ($a_n \ne 0$ oder $n = 0$), Grad $n$, Nullstelle $c$ mit $p(c) = 0$. Zwei Polynome sind gleich, wenn ihre Koeffizienten übereinstimmen.

**Beobachtung 3.107.** Verschiedene Polynome können dieselbe Funktion beschreiben: Über $\mathbb{Z}/2\mathbb{Z}$ sind $X^2$ und $X$ verschieden, aber $0^2 = 0$ und $1^2 = 1$.

**Definition 3.108.** $K$ heißt algebraisch abgeschlossen, falls jedes Polynom positiven Grades eine Nullstelle in $K$ hat. $\mathbb{R}$ ist es nicht.

**Satz 3.109 (Fundamentalsatz der Algebra, ohne Beweis).** $\mathbb{C}$ ist algebraisch abgeschlossen: Jedes Polynom ist $p(X) = a \prod_{j=1}^{n}(X - z_j)$ mit $a, z_j \in \mathbb{C}$.

:::rechnung Beispiel 3.110 und eine quadratische Gleichung
?? X^2 + 1 = (X - i)(X + i) || ausmultiplizieren: $X^2 - i^2 = X^2 + 1$
?? x^2 + 2x + 5 = 0 \Rightarrow x = -1 \pm \sqrt{1 - 5} || pq-Formel mit $p = 2$, $q = 5$
?? \sqrt{-4} = 2i || $(2i)^2 = 4i^2 = -4$
?? x = -1 \pm 2i || beide Lösungen, zueinander konjugiert
:::

:::achtung Reelle Koeffizienten, komplexe Nullstellen
Hat ein reelles Polynom die Nullstelle $z$, so ist auch $\bar z$ eine (die Konjugation ist ein Automorphismus). Komplexe Nullstellen reeller Polynome kommen in Paaren.
:::

:::alt Als Zerlegung
Wie jede natürliche Zahl ein Produkt von Primzahlen ist, ist jedes Polynom über $\mathbb{C}$ ein Produkt von Linearfaktoren $(X - z)$. Über $\mathbb{R}$ bleiben manchmal quadratische Faktoren übrig, die sich nicht weiter zerlegen lassen.
:::
""")

k.vektor("Die Gleichung $x^2 + 2x + 5 = 0$ hat zwei komplexe Lösungen. Gib die Lösung mit **positivem** Imaginärteil als Paar (Realteil, Imaginärteil) an.", [-1, 2],
         "pq-Formel: $x = -1 \\pm \\sqrt{1 - 5} = -1 \\pm \\sqrt{-4} = -1 \\pm 2i$. Mit positivem Imaginärteil: $-1 + 2i$. Probe: $(-1 + 2i)^2 = 1 - 4i + 4i^2 = -3 - 4i$ und $-3 - 4i + 2(-1 + 2i) + 5 = 0$.",
         tipps=["Wende die pq-Formel an: $x = -\\frac p2 \\pm \\sqrt{\\frac{p^2}{4} - q}$.", "Der Ausdruck unter der Wurzel ist $1 - 5 = -4$.", "$\\sqrt{-4} = 2i$."],
         rechenweg=rechnung([("x = -1 \\pm \\sqrt{1 - 5} = -1 \\pm \\sqrt{-4}", "pq-Formel"), ("\\sqrt{-4} = 2i", "$(2i)^2 = -4$")]),
         typische_fehler=[([1, 2], "Das Vorzeichen des Realteils ist falsch: $-\\frac p2 = -1$."),
                          ([-1, -2], "Das ist die andere Lösung (negativer Imaginärteil). Gefragt war die mit positivem Imaginärteil.")])

k.mc("Welche Aussage über $p(X) = X^2 + 4$ ist richtig?",
     ["Über $\\mathbb{R}$ hat $p$ keine Nullstelle, über $\\mathbb{C}$ hat $p$ die Nullstellen $2i$ und $-2i$", "$p$ hat über $\\mathbb{R}$ die Nullstellen $2$ und $-2$", "$p$ hat über $\\mathbb{C}$ nur die Nullstelle $2i$", "$p$ hat über keinem Körper eine Nullstelle"],
     "$x^2 + 4 \\ge 4 > 0$ in $\\mathbb{R}$. In $\\mathbb{C}$: $(2i)^2 = -4$ und $(-2i)^2 = -4$, also $X^2 + 4 = (X - 2i)(X + 2i)$.",
     tipps=["Setze $x = 2$ in $x^2 + 4$ ein.", "Quadriere $2i$ und $-2i$."],
     fehler={"$p$ hat über $\\mathbb{R}$ die Nullstellen $2$ und $-2$": "$2^2 + 4 = 8 \\ne 0$. Das wären die Nullstellen von $X^2 - 4$.",
             "$p$ hat über $\\mathbb{C}$ nur die Nullstelle $2i$": "Auch $-2i$ ist Nullstelle: $(-2i)^2 = -4$. Nullstellen komplexer Polynome zählen mit Vielfachheit: Grad $2$ gibt zwei Nullstellen.",
             "$p$ hat über keinem Körper eine Nullstelle": "Über $\\mathbb{C}$ hat jedes Polynom positiven Grades eine Nullstelle (Satz 3.109)."})

# ── Seite 9: Zahlbereiche ────────────────────────────────────────────────
k.erklaerung("Abschnitt 3.8: Die Zahlbereiche im Überblick", r"""
## Fünf Stufen, jede löst ein Problem

Jeder Zahlbereich wurde durch eine **injektive, strukturerhaltende** Abbildung in den nächsten eingebettet und identifiziert:
$n \in \mathbb{N} \leftrightarrow [(n, 0)] \in \mathbb{Z}$, $z \in \mathbb{Z} \leftrightarrow [(z, 1)] \in \mathbb{Q}$, $q \in \mathbb{Q} \leftrightarrow \iota(q) \in \mathbb{R}$, $r \in \mathbb{R} \leftrightarrow (r, 0) \in \mathbb{C}$. So gilt
$$\mathbb{N} \subseteq \mathbb{Z} \subseteq \mathbb{Q} \subseteq \mathbb{R} \subseteq \mathbb{C}.$$

| Bereich | Neu gegenüber dem vorigen | Struktur |
|---|---|---|
| $\mathbb{N}$ | Zählen, $a + b$, $a \cdot b$ | Halbgruppe, Peano-Axiome |
| $\mathbb{Z}$ | $a + x = b$ lösbar | kommutativer Ring |
| $\mathbb{Q}$ | $ax = b$ lösbar ($a \ne 0$) | angeordneter Körper |
| $\mathbb{R}$ | Suprema (R2), $\sqrt{2}$ | vollständiger angeordneter Körper |
| $\mathbb{C}$ | $x^2 + 1 = 0$, alle Polynome | algebraisch abgeschlossener Körper, nicht anordenbar |

:::rechnung Einbettung nachgeprüft
?? 3 \in \mathbb{N} \mapsto [(3, 0)] \in \mathbb{Z} || $a = [(a, 0)]$
?? 2 \in \mathbb{Z} \mapsto [(2, 1)] = 2/1 \in \mathbb{Q} || $a = [(a, 1)]$
?? 3 \in \mathbb{R} \mapsto (3, 0) = 3 + 0i \in \mathbb{C} || $x = (x, 0)$
:::

Mit den Identifikationen schreibt das Skript kurz $\mathbb{Z}$ für $(\mathbb{Z}, +)$ oder $\mathbb{R}$ für $(\mathbb{R}, +, \cdot, \le)$, wenn klar ist, welche Struktur gemeint ist.

:::alt Als Werkzeugkasten
Jede Stufe liefert ein Werkzeug, das die vorige noch nicht hatte: Subtrahieren, Dividieren, Grenzwerte, Wurzeln aus Negativem. Dafür geht jeweils etwas verloren: $\mathbb{N}$ ist nicht umkehrbar, $\mathbb{Z}/n\mathbb{Z}$ ist kein Körper, $\mathbb{C}$ ist nicht geordnet.
:::
""")

k.zuordnen("Ordne jeden Zahlbereich dem Problem zu, das mit ihm lösbar wird (Abschn. 3.1 bis 3.7).",
           [("$\\mathbb{Z}$", "$a + x = b$ ist immer lösbar"),
            ("$\\mathbb{Q}$", "$a x = b$ ist lösbar für $a \\ne 0$"),
            ("$\\mathbb{R}$", "jede nichtleere, nach oben beschränkte Menge hat ein Supremum"),
            ("$\\mathbb{C}$", "jedes Polynom positiven Grades hat eine Nullstelle")],
           "Jede Erweiterung behebt ein konkretes Defizit: Differenzen (ℤ), Quotienten (ℚ), Lücken (ℝ), fehlende Nullstellen (ℂ).",
           ablenker=["$x^2 = 2$ ist in $\\mathbb{Q}$ lösbar"],
           tipps=["Wo hast du in den vorigen Kapiteln einen Mangel gesehen?", "$\\sqrt{2}$ gibt es in $\\mathbb{Q}$ nicht."])

k.praxis()


def komplex_grundrechnen(rng):
    op = rng.choice(["+", "-", "*", "*"])
    while True:
        z = (F(rng.randint(-5, 5)), F(rng.randint(-5, 5)))
        w = (F(rng.randint(-5, 5)), F(rng.randint(-5, 5)))
        if z[1] != 0 and w[1] != 0 and z[0] != 0 and w[0] != 0:
            break
    if op == "+":
        r, name = cadd(z, w), "Summe"
        falsch = [(vtext(csub(z, w)), "Das ist die Differenz $z - w$."), ([str(z[0] + w[0]), str(z[1] * w[1])], "Der Imaginärteil wird ebenfalls addiert, nicht multipliziert.")]
        zeilen = [(f"{ctex(z, True)} + {ctex(w, True)} = {ctex(r)}", "Real- und Imaginärteile getrennt addieren")]
    elif op == "-":
        r, name = csub(z, w), "Differenz"
        falsch = [(vtext(cadd(z, w)), "Das ist die Summe $z + w$."), ([str(z[0] - w[0]), str(z[1] + w[1])], "Auch der Imaginärteil wird subtrahiert: $\\operatorname{Im} z - \\operatorname{Im} w$.")]
        zeilen = [(f"{ctex(z, True)} - {ctex(w, True)} = {ctex(r)}", "Real- und Imaginärteile getrennt subtrahieren")]
    else:
        r, name = cmul(z, w), "Produkt"
        falsch = [([str(z[0] * w[0]), str(z[1] * w[1])], "Komponentenweise multipliziert. Richtig ist $(xu - yv) + (xv + yu)i$."),
                  ([str(z[0] * w[0] + z[1] * w[1]), str(z[0] * w[1] + z[1] * w[0])], "Das Vorzeichen von $i^2 = -1$ fehlt: Der Realteil ist $xu - yv$, nicht $xu + yv$.")]
        zeilen = [(f"{ctex(z, True)}{ctex(w, True)} = {ctex(r)}", "ausmultiplizieren, $i^2 = -1$ einsetzen, zusammenfassen")]
    symb = {"+": "+", "-": "-", "*": "\\cdot"}[op]
    fehler = [(a, b) for a, b in falsch if [str(F(x)) for x in a] != vtext(r)]
    return {"typ": "vektor",
            "frage": f"Berechne die {name} ${ctex(z, True)} {symb} {ctex(w, True)}$ und gib sie als Paar (Realteil, Imaginärteil) an.",
            "loesung": vtext(r),
            "tipps": ["Rechne wie mit Buchstaben und ersetze am Ende $i^2$ durch $-1$.", "Bei der Multiplikation gibt es vier Teilprodukte.", f"Das Ergebnis ist ${ctex(r)}$."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Satz 3.99: $z + w = (x + u) + (y + v)i$ und $zw = (xu - yv) + (xv + yu)i$.",
            "typische_fehler": fehler}


def komplex_betrag(rng):
    a, b, c = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (20, 21, 29)])
    if rng.random() < 0.5:
        a, b = b, a
    z = (F(rng.choice([-1, 1]) * a), F(rng.choice([-1, 1]) * b))
    if rng.random() < 0.5:
        w, fragestelle = F(c), f"Bestimme $|{ctex(z)}|$."
        falsch = [(abs(z[0]) + abs(z[1]), "Das ist $|x| + |y|$. Der Betrag ist $\\sqrt{x^2 + y^2}$."), (c * c, "Das ist $|z|^2 = x^2 + y^2$. Es fehlt die Wurzel.")]
        zeilen = [(f"{a}^2 + {b}^2 = {c * c}", "$x^2 + y^2$ (Vorzeichen fallen beim Quadrieren weg)"), (f"\\sqrt{{{c * c}}} = {c}", "Wurzel")]
    else:
        w, fragestelle = F(c * c), f"Berechne $z \\bar z$ für $z = {ctex(z)}$ (das Ergebnis ist reell)."
        falsch = [(c, "Das ist $|z|$. Es gilt $z\\bar z = |z|^2$."), (z[0] ** 2 - z[1] ** 2, "Das ist der Realteil von $z^2$. Für $z\\bar z$ gilt $x^2 + y^2$.")]
        zeilen = [(f"{a}^2 + {b}^2 = {c * c}", "$z\\bar z = (x + yi)(x - yi) = x^2 + y^2$")]
    return {"frage": fragestelle, "loesung": w,
            "tipps": ["$|x + yi| = \\sqrt{x^2 + y^2}$ und $z\\bar z = |z|^2$.", f"Quadriere beide Teile: ${a}^2 = {a * a}$ und ${b}^2 = {b * b}$.", f"${a * a} + {b * b} = {c * c}$."],
            "rechenweg": rechnung_zahlen(zeilen),
            "erklaerung": "Satz 3.103: $z\\bar z = |z|^2$ mit $|z| = \\sqrt{x^2 + y^2}$.",
            "typische_fehler": ohne_gleiche(w, falsch)}


def komplex_division(rng):
    while True:
        w = (F(rng.randint(-5, 5)), F(rng.randint(-5, 5)))
        z = (F(rng.randint(-3, 3)), F(rng.randint(-3, 3)))
        if z != (0, 0) and z[0] != 0 and z[1] != 0 and w != (0, 0):
            break
    r = cdiv(w, z)
    n = cabs2(z)
    zahler = cmul(w, cconj(z))
    falsch = [([str(w[0] / z[0]), str(w[1] / z[1])], "Komponentenweise geteilt. Du musst mit dem Konjugierten des Nenners erweitern."),
              (vtext(cmul(w, z)) if cabs2(z) != 1 else vtext(cmul(w, cconj(z))), "Das ist $wz$, nicht $w/z$. Erweitere mit $\\bar z$ und teile durch $|z|^2$."),
              ([str(zahler[0]), str(zahler[1])], f"Es fehlt die Division durch $|z|^2 = {n}$.")]
    fehler = [(a, b) for a, b in falsch if a != vtext(r)]
    zeilen = [(f"({ctex(w, True)}({ctex(cconj(z), True)}))/({ctex(z, True)}({ctex(cconj(z), True)})) = {ctex(zahler, True)}/{n}", f"mit $\\bar z = {ctex(cconj(z))}$ erweitern: Nenner $|z|^2 = {n}$"),
              (f"{ctex(zahler, True)}/{n} = {ctex(r)}", "Real- und Imaginärteil getrennt teilen")]
    return {"typ": "vektor",
            "frage": f"Berechne $\\dfrac{{{ctex(w)}}}{{{ctex(z)}}}$ und gib das Ergebnis als Paar (Realteil, Imaginärteil) an. Brüche wie `3/5` sind erlaubt.",
            "loesung": vtext(r),
            "tipps": [f"Erweitere mit dem Konjugierten des Nenners: ${ctex(cconj(z))}$.", f"Der Nenner wird $|z|^2 = {n}$.", f"Der Zähler ist ${ctex(zahler)}$."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "$\\frac{w}{z} = \\frac{w\\bar z}{|z|^2}$ (Satz 3.103): Der Nenner wird reell.",
            "typische_fehler": fehler}


def komplex_nullstelle(rng):
    s, t = rng.randint(-3, 3), rng.randint(1, 4)
    while s == 0:
        s = rng.randint(-3, 3)
    p, q = 2 * s, s * s + t * t
    gl = "x^2" + (f" + {p}x" if p > 0 else f" - {-p}x") + f" + {q}"
    zeilen = [(f"x = {-s} \\pm \\sqrt{{{s * s} - {q}}} = {-s} \\pm \\sqrt{{-{t * t}}}", f"pq-Formel mit $p = {p}$, $q = {q}$"),
              (f"\\sqrt{{-{t * t}}} = {t}i", f"$({t}i)^2 = -{t * t}$"), (f"x = {-s} \\pm {t}i", "zwei zueinander konjugierte Lösungen")]
    return {"typ": "vektor",
            "frage": f"Die Gleichung ${gl} = 0$ hat zwei komplexe Lösungen. Gib die Lösung mit **positivem** Imaginärteil als Paar (Realteil, Imaginärteil) an.",
            "loesung": [-s, t],
            "tipps": ["Wende die pq-Formel an: $x = -\\frac p2 \\pm \\sqrt{\\frac{p^2}{4} - q}$.", f"Unter der Wurzel steht ${s * s} - {q} = -{t * t}$.", f"$\\sqrt{{-{t * t}}} = {t}i$."],
            "rechenweg": rechnung(zeilen),
            "erklaerung": "Eine negative Diskriminante liefert zwei komplexe Lösungen $-\\frac p2 \\pm bi$. Sie sind konjugiert zueinander.",
            "typische_fehler": [f for f in [([s, t], "Das Vorzeichen des Realteils ist falsch: Er ist $-\\frac p2$."), ([-s, -t], "Das ist die Lösung mit negativem Imaginärteil."),
                                            ([-s, t * t], f"$\\sqrt{{-{t * t}}} = {t}i$, nicht ${t * t}i$.")] if f[0] != [-s, t]]}


k.generator(komplex_grundrechnen, typ="vektor", titel="Komplexe Zahlen: plus, minus, mal")
k.generator(komplex_betrag, typ="zahl", titel="Betrag und z mal konjugiert")
k.generator(komplex_division, typ="vektor", titel="Komplexe Division")
k.generator(komplex_nullstelle, typ="vektor", titel="Komplexe Nullstellen quadratischer Gleichungen")

k.rechenweg_aufgabe(r"""
## Quiz-Stil: Rechnen in $\mathbb{C}$

Seien $z = 1 + 2i$ und $w = 3 - i$. Geben Sie jeweils (Realteil, Imaginärteil) bzw. den Betrag an.
""",
    [{"typ": "vektor", "frage": "Berechnen Sie $z + w$.", "loesung": [4, 1], "tipps": ["Real- und Imaginärteile getrennt addieren.", "$1 + 3$ und $2 + (-1)$."],
      "rechenweg": ":::rechnung\n1 + 3 = 4 || Realteil\n2 + (-1) = 1 || Imaginärteil\n:::", "erklaerung": "$z + w = 4 + i$."},
     {"typ": "vektor", "frage": "Berechnen Sie $z \\cdot w$.", "loesung": [5, 5], "tipps": ["Vier Produkte, dann $i^2 = -1$.", "$(1 + 2i)(3 - i) = 3 - i + 6i - 2i^2$."],
      "rechenweg": ":::rechnung\n?? (1 + 2i)(3 - i) = 3 - i + 6i - 2i^2 || ausmultiplizieren\n?? 3 - i + 6i + 2 = 5 + 5i || $-2i^2 = +2$\n:::",
      "erklaerung": "$zw = 5 + 5i$.", "typische_fehler": [([1, 3], "Komponentenweise multipliziert ($1 \\cdot 3$ und $2 \\cdot (-1)$ kombiniert). Multipliziere alle vier Teilprodukte.")]},
     {"typ": "zahl", "frage": "Berechnen Sie $|z|^2 \\cdot |w|^2$.", "loesung": 50, "tipps": ["$|z|^2 = 1 + 4$ und $|w|^2 = 9 + 1$.", "$5 \\cdot 10$."],
      "rechenweg": ":::rechnung\n1^2 + 2^2 = 5 || $|z|^2$\n3^2 + 1^2 = 10 || $|w|^2$\n5 \\cdot 10 = 50 || Produkt\n:::",
      "erklaerung": "Es ist $|zw|^2 = |z|^2|w|^2 = 50$; Kontrolle: $|5 + 5i|^2 = 25 + 25 = 50$."},
     {"typ": "vektor", "frage": "Berechnen Sie $z / w$ (Brüche wie `1/10` erlaubt).", "loesung": [F(1, 10), F(7, 10)], "tipps": ["Mit $\\bar w = 3 + i$ erweitern.", "Nenner $10$."],
      "rechenweg": ":::rechnung\n?? (1 + 2i)(3 + i) = 1 + 7i || Zähler\n3^2 + 1^2 = 10 || Nenner $|w|^2$\n:::", "erklaerung": "$\\frac{z}{w} = \\frac{1 + 7i}{10}$."}],
    "$z + w = 4 + i$, $zw = 5 + 5i$ und $z/w = \\frac1{10} + \\frac7{10}i$. Der Betrag ist multiplikativ: $|zw|^2 = 50 = |z|^2|w|^2$.",
    uebungsblatt=True,
    tipps=["Rechne wie mit Buchstaben und ersetze $i^2$ durch $-1$.", "Zum Dividieren erweiterst du mit dem Konjugierten des Nenners."],
    rechenweg=r"""
:::rechnung
1 + 3 = 4 || Realteil der Summe
2 - 1 = 1 || Imaginärteil der Summe
1^2 + 2^2 = 5 || $|z|^2$
3^2 + 1^2 = 10 || $|w|^2$
:::
""")

k.papier(r"""
## Übungsblatt-Stil: Betrag und Konjugation (Satz 3.103)

Zeigen Sie für alle $z, w \in \mathbb{C}$: $|zw| = |z||w|$. Benutzen Sie $z\bar z = |z|^2$ und $\overline{zw} = \bar z\,\bar w$.
""",
    r"""
Es gilt $|zw|^2 = (zw)\overline{(zw)} = zw\,\bar z\,\bar w = (z\bar z)(w\bar w) = |z|^2|w|^2 = (|z||w|)^2$ (Kommutativität und Assoziativität in $\mathbb{C}$).
Sowohl $|zw|$ als auch $|z||w|$ sind nichtnegativ. Nach der Eindeutigkeit der nichtnegativen Wurzel (Satz 3.87) sind sie gleich. $\square$
""",
    ["$|zw|^2 = (zw)\\overline{(zw)}$ geschrieben",
     "$\\overline{zw} = \\bar z\\,\\bar w$ benutzt und die Faktoren umgeordnet",
     "$z\\bar z = |z|^2$ und $w\\bar w = |w|^2$ angewendet",
     "Wurzelziehen mit Nichtnegativität und Eindeutigkeit begründet"],
    "Die Rechenregeln für Konjugation machen den Beweis kurz: Der Betrag ist multiplikativ, weil er sich als $\\sqrt{z\\bar z}$ schreiben lässt.",
    uebungsblatt=True,
    tipps=["Starte mit dem Quadrat: $|zw|^2 = (zw)\\overline{(zw)}$.", "Warum darfst du am Ende die Wurzel ziehen?"])

k.papier(r"""
## Übungsblatt-Stil: Distributivgesetz in ℂ (Beweis von Satz 3.96)

Seien $z = (a, b)$, $w = (c, d)$, $t = (e, f) \in \mathbb{C}$. Zeigen Sie mit Definition 3.95: $z(w + t) = zw + zt$.
""",
    r"""
$z(w + t) = (a, b)(c + e,\ d + f) = (a(c + e) - b(d + f),\ a(d + f) + b(c + e))$
$= (ac - bd + ae - bf,\ ad + bc + af + be)$
$= (ac - bd,\ ad + bc) + (ae - bf,\ af + be) = zw + zt$. $\square$
""",
    ["Summe $w + t$ komponentenweise gebildet",
     "Definition 3.95 (Multiplikation) korrekt angewandt",
     "Mit dem Distributivgesetz in $\\mathbb{R}$ ausmultipliziert",
     "Die Terme in zwei Paare $zw$ und $zt$ zerlegt"],
    "Das Distributivgesetz in $\\mathbb{C}$ folgt aus dem in $\\mathbb{R}$, komponentenweise.",
    uebungsblatt=True,
    tipps=["Wende zuerst $w + t = (c + e,\\ d + f)$ an.", "Multipliziere dann nach Definition 3.95 und sortiere."])

k.papier(r"""
## Übungsblatt-Stil: Linearfaktoren über ℂ

Zerlegen Sie $p(X) = X^4 - 1$ über $\mathbb{R}$ so weit wie möglich und über $\mathbb{C}$ in Linearfaktoren. Geben Sie alle Nullstellen an.
""",
    r"""
Über $\mathbb{R}$: $X^4 - 1 = (X^2 - 1)(X^2 + 1) = (X - 1)(X + 1)(X^2 + 1)$. Der Faktor $X^2 + 1$ hat keine reelle Nullstelle, ist also über $\mathbb{R}$ nicht weiter zerlegbar.
Über $\mathbb{C}$: $X^2 + 1 = (X - i)(X + i)$ (Beispiel 3.110). Also $X^4 - 1 = (X - 1)(X + 1)(X - i)(X + i)$ mit den Nullstellen $1, -1, i, -i$.
Probe: $i^4 = (i^2)^2 = (-1)^2 = 1$ und $(-i)^4 = 1$. $\square$
""",
    ["Binomische Formel $X^4 - 1 = (X^2 - 1)(X^2 + 1)$ benutzt",
     "Über $\\mathbb{R}$ den Faktor $X^2 + 1$ als nicht zerlegbar erkannt",
     "$X^2 + 1 = (X - i)(X + i)$ eingesetzt",
     "Alle vier Nullstellen $1, -1, i, -i$ genannt"],
    "Der Fundamentalsatz garantiert vier Nullstellen (mit Vielfachheit) bei Grad $4$. Sie liegen auf dem Einheitskreis.",
    tipps=["Benutze die dritte binomische Formel zweimal.", "Welche Zahlen haben $z^4 = 1$?"])

k.zusammenfassung(r"""
## Die komplexen Zahlen (Skript Abschn. 3.7 und 3.8, Def. 3.94 bis Bsp. 3.110)

- $\mathbb{C} := \mathbb{R}^2$, $x \leftrightarrow (x, 0)$ (Def. 3.94). $(x_1, y_1) + (x_2, y_2) = (x_1 + x_2,\ y_1 + y_2)$, $(x_1, y_1)(x_2, y_2) = (x_1x_2 - y_1y_2,\ x_1y_2 + y_1x_2)$ (Def. 3.95).
- **Körper** (Satz 3.96): $0 = (0, 0)$, $1 = (1, 0)$, $(x, y)^{-1} = (\frac{x}{x^2 + y^2}, \frac{-y}{x^2 + y^2})$.
- $i := (0, 1)$, $i^2 = -1$, $z = x + yi$ mit $\operatorname{Re} z = x$, $\operatorname{Im} z = y$ (Def. 3.97, Beob. 3.98). $z + w$, $zw$ durch Ausmultiplizieren (Satz 3.99).
- **Nicht anordenbar** (Satz 3.101): $i^2 = -1 < 0$ widerspricht $a^2 \ge 0$.
- **Konjugation und Betrag** (Def. 3.102): $\bar z = x - yi$, $|z| = \sqrt{x^2 + y^2}$. Satz 3.103: $z\bar z = |z|^2$, $|zw| = |z||w|$, $|z + w| \le |z| + |w|$, $z^{-1} = \bar z / |z|^2$. Satz 3.105: $z \mapsto \bar z$ ist Körperautomorphismus; $z$ reell $\iff z = \bar z$.
- **Division:** $\frac{w}{z} = \frac{w\bar z}{|z|^2}$. **Quadratische Gleichung** mit $D < 0$: $x = -\frac p2 \pm i\sqrt{q - \frac{p^2}{4}}$.
- **Polynome** (Def. 3.106), **algebraisch abgeschlossen** (Def. 3.108), **Fundamentalsatz** (Satz 3.109): jedes Polynom zerfällt über $\mathbb{C}$ in Linearfaktoren. $X^2 + 1 = (X - i)(X + i)$ (Bsp. 3.110).
- **Zahlbereiche** (Abschn. 3.8): $\mathbb{N} \subseteq \mathbb{Z} \subseteq \mathbb{Q} \subseteq \mathbb{R} \subseteq \mathbb{C}$ durch injektive, strukturerhaltende Einbettungen.

!! $(x + yi)(u + vi)$: vier Produkte, dann $i^2 = -1$. Dividieren: mit dem Konjugierten des Nenners erweitern.
""")
