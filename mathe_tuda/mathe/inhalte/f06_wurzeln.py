# -*- coding: utf-8 -*-
"""Fundament 6: Wurzeln – Quadratwurzel, Rechenregeln, teilweise Wurzelziehen, n-te Wurzel,
rationale Exponenten, Nenner rational machen."""
import math
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

tex = mathlib.tex


def wz(k, m):
    """k·√m als LaTeX (k = 1 ohne Vorfaktor)."""
    if m == 1:
        return tex(k)
    return f"\\sqrt{{{m}}}" if k == 1 else f"{tex(k)}\\sqrt{{{m}}}"


k = neues_kapitel(
    slug="wurzeln",
    titel="Wurzeln",
    beschreibung="Quadratwurzel, n-te Wurzel, Wurzeln als Potenzen, teilweise Wurzelziehen und Nenner rational machen",
    teil="fundament",
    quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)",
    icon="🌱")

k.lernziele([
    "Ich weiß, was $\\sqrt{a}$ und $\\sqrt[n]{a}$ bedeuten, und ziehe einfache Wurzeln im Kopf",
    "Ich erkenne den Fehler $\\sqrt{a + b} = \\sqrt{a} + \\sqrt{b}$",
    "Ich kann teilweise die Wurzel ziehen, z. B. $\\sqrt{12} = 2\\sqrt{3}$",
    "Ich schreibe Wurzeln als Potenzen mit rationalem Exponenten und rechne damit",
    "Ich kann den Nenner eines Bruchs rational machen",
])

k.warum(r"""
Wurzeln stecken in vielen Algorithmen. Ein Primzahltest muss Teiler nur bis $\sqrt{n}$
prüfen: Für $n = 1\,000\,000$ sind das $1000$ statt einer Million Versuche. Der
Abstand zweier Punkte auf dem Bildschirm ist eine Wurzel, ebenso die Länge eines Vektors
in Mathe 1. In Python schreibst du `x ** 0.5` oder `math.sqrt(x)`: Dahinter steckt die
Regel $\sqrt{x} = x^{1/2}$ aus diesem Kapitel.
""")

# ── 1: Quadratwurzel ───────────────────────────────────────────────────────
k.erklaerung("Die Quadratwurzel", r"""
    ## Quadrieren rückwärts

    :::analogie 🟩 Quadratisches Beet
    Ein quadratisches Beet hat $49$ Quadratmeter Fläche. Wie lang ist eine Seite?
    Gesucht ist die Zahl, die mit sich selbst malgenommen $49$ ergibt: $7$ Meter.
    :::

    Die [[Quadratwurzel]] $\sqrt{a}$ ist die Zahl, die **nicht negativ** ist und
    quadriert $a$ ergibt. Die Zahl unter der Wurzel heißt [[Radikand]].

    :::rechnung Beispiel vorgerechnet
    \sqrt{49} = 7 || denn $7^2 = 49$ und $7 \ge 0$
    \sqrt{0{,}09} = 0{,}3 || denn $0{,}3^2 = 0{,}09$
    \sqrt{\frac{4}{9}} = \frac{2}{3} || Zähler und Nenner einzeln
    :::

    Diese [[Quadratzahlen|Quadratzahl]] solltest du kennen: $1, 4, 9, 16, 25, 36, 49, 64, 81,
    100, 121, 144, 169, 196, 225$.

    :::alt Mit dem Rückwärtsgang erklärt
    Quadrieren ist eine Maschine: $7$ rein, $49$ raus. Die Wurzel lässt die Maschine
    rückwärts laufen: $49$ rein, $7$ raus. Darum gilt $\left(\sqrt{49}\right)^2 = 49$:
    Erst rückwärts, dann vorwärts, und du bist wieder am Anfang.
    :::
    ---
    ## Die Wurzel ist nie negativ

    $x^2 = 9$ hat zwei Lösungen, $3$ und $-3$. Die Wurzel $\sqrt{9}$ ist aber
    festgelegt als die **nicht negative**: $\sqrt{9} = 3$.

    :::visual funktionsgraph
    {"funktionen": [{"term": "x^2", "label": "x^2", "farbe": 1}, {"term": "sqrt(x)", "label": "\\sqrt{x}", "farbe": 2}],
     "x": [-3, 5], "y": [-2, 6], "gleiche_achsen": true,
     "punkte": [{"x": 2, "y": 4}, {"x": -2, "y": 4}, {"x": 4, "y": 2}],
     "unterschrift": "$2^2 = (-2)^2 = 4$, aber $\\sqrt{4} = 2$. Der Graph von $\\sqrt{x}$ liegt nie unter der $x$-Achse und beginnt bei $0$."}
    :::

    :::rechnung Beispiel vorgerechnet
    \sqrt{(-3)^2} = \sqrt{9} || erst quadrieren
    = 3 || die Wurzel ist nicht negativ
    :::

    :::achtung Zwei typische Fehler
    $\sqrt{9} = \pm 3$ ist falsch: Die Wurzel ist eine Zahl, nämlich $3$. Und $\sqrt{-4}$
    gibt es in den reellen Zahlen nicht, denn kein Quadrat ist negativ.
    :::

    :::alt Mit Längen erklärt
    Denk an das Beet: Eine Seitenlänge kann nicht $-7$ Meter sein. Die Wurzel
    beantwortet immer die Frage „Wie lang ist die Seite?“. Darum ist sie nie negativ,
    und aus einer negativen Fläche kann man keine Seite berechnen.
    :::
    """)

k.berechne("sqrt(144)",
           erklaerung="$12^2 = 144$, also $\\sqrt{144} = 12$.",
           tipps=["Welche Zahl mal sich selbst ergibt $144$?", "Probiere $10^2 = 100$ und $13^2 = 169$.", "$12 \\cdot 12$"],
           rechenweg=r"""
           :::rechnung
           12^2 = 144 || Probe durch Quadrieren
           \sqrt{144} = 12 || also ist $12$ die Wurzel
           :::
           """,
           typische_fehler=[(72, "Du hast halbiert. Die Wurzel sucht die Zahl, die **mit sich selbst** malgenommen $144$ ergibt."),
                            (-12, "$(-12)^2$ ist zwar auch $144$, aber die Wurzel ist als nicht negative Zahl festgelegt.")])

k.wf("$\\sqrt{16} = \\pm 4$", False,
     "Die Wurzel ist eine einzige, nicht negative Zahl: $\\sqrt{16} = 4$. Die Gleichung $x^2 = 16$ hat dagegen zwei Lösungen, $x = 4$ und $x = -4$.",
     tipps=["Ist $\\sqrt{16}$ eine Zahl oder zwei?"])

k.zahl("Berechne $\\sqrt{0{,}09}$.", F(3, 10),
       "$0{,}3^2 = 0{,}09$, also $\\sqrt{0{,}09} = 0{,}3$.",
       tipps=["Schreibe $0{,}09$ als Bruch.", "$0{,}09 = \\frac{9}{100}$.", "$\\sqrt{9} = 3$ und $\\sqrt{100} = 10$."],
       rechenweg=r"""
       :::rechnung
       \sqrt{0{,}09} = \sqrt{\frac{9}{100}} || als Bruch
       = \frac{3}{10} || Zähler und Nenner einzeln
       = 0{,}3 || als Dezimalzahl
       :::
       """,
       typische_fehler=[(F(3, 100), "$0{,}03^2 = 0{,}0009$. Prüfe durch Quadrieren: $0{,}3^2 = 0{,}09$."),
                        (3, "$3^2 = 9$, nicht $0{,}09$. Das Komma gehört dazu.")])

# ── 2: Rechenregeln ────────────────────────────────────────────────────────
k.erklaerung("Rechnen mit Wurzeln", r"""
    ## Malnehmen und Teilen

    Für $a, b \ge 0$ darfst du Wurzeln zusammenfassen oder auseinanderziehen:

    $$\sqrt{a} \cdot \sqrt{b} = \sqrt{a \cdot b} \qquad \frac{\sqrt{a}}{\sqrt{b}} = \sqrt{\frac{a}{b}} \quad (b > 0)$$

    :::rechnung Beispiel vorgerechnet
    \sqrt{2} \cdot \sqrt{8} = \sqrt{2 \cdot 8} || unter eine Wurzel
    = \sqrt{16} = 4 || jetzt geht sie auf
    \frac{\sqrt{75}}{\sqrt{3}} = \sqrt{\frac{75}{3}} || unter eine Wurzel
    = \sqrt{25} = 5 || ausrechnen
    :::

    :::alt Mit Quadrieren erklärt
    Warum stimmt $\sqrt{2} \cdot \sqrt{8} = \sqrt{16}$? Quadriere die linke Seite:
    $(\sqrt{2} \cdot \sqrt{8})^2 = (\sqrt{2})^2 \cdot (\sqrt{8})^2 = 2 \cdot 8 = 16$.
    Die linke Seite ist nicht negativ und hat das Quadrat $16$. Also ist sie $\sqrt{16} = 4$.
    :::
    ---
    ## Bei Plus und Minus: keine Regel

    :::rechnung So nicht!
    \sqrt{9 + 16} = \sqrt{25} || erst die Summe
    = 5 || richtig
    !\sqrt{9 + 16} = \sqrt{9} + \sqrt{16} = 7 || Wurzel auf die Summanden verteilt
    :::

    :::achtung Der häufigste Wurzelfehler
    $\sqrt{a + b} \neq \sqrt{a} + \sqrt{b}$ und $\sqrt{a - b} \neq \sqrt{a} - \sqrt{b}$.
    Ein Gegenbeispiel reicht: $\sqrt{9 + 16} = 5$, aber $\sqrt{9} + \sqrt{16} = 7$.
    :::

    :::alt Mit einem Dreieck erklärt
    Gehe $3$ Meter nach Osten und $4$ Meter nach Norden. Du bist $3 + 4 = 7$ Meter
    gelaufen. Die Luftlinie zum Start ist aber nur $\sqrt{3^2 + 4^2} = \sqrt{25} = 5$ Meter.
    Wäre $\sqrt{9 + 16} = \sqrt{9} + \sqrt{16}$, wäre die Abkürzung so lang wie der Umweg.
    :::
    """)

k.zahl("Berechne $\\sqrt{2} \\cdot \\sqrt{18}$.", 6,
       "$\\sqrt{2} \\cdot \\sqrt{18} = \\sqrt{36} = 6$.",
       tipps=["Fasse beide Wurzeln zu einer zusammen.", "$\\sqrt{2 \\cdot 18}$", "$\\sqrt{36}$"],
       rechenweg=r"""
       :::rechnung
       \sqrt{2} \cdot \sqrt{18} = \sqrt{2 \cdot 18} || unter eine Wurzel
       = \sqrt{36} || ausrechnen
       = 6 || $6^2 = 36$
       :::
       """,
       typische_fehler=[(36, "Du hast die Wurzel vergessen: $\\sqrt{2 \\cdot 18} = \\sqrt{36} = 6$."),
                        (F(20), "Du hast $2 + 18$ gerechnet. Unter der Wurzel wird malgenommen.")])

k.zahl("Berechne $\\sqrt{9 + 16}$.", 5,
       "Erst die Summe: $9 + 16 = 25$, dann $\\sqrt{25} = 5$. Die Wurzel darf man nicht auf die Summanden verteilen.",
       tipps=["Was steht unter der Wurzel?", "Rechne zuerst $9 + 16$.", "$\\sqrt{25}$"],
       rechenweg=r"""
       :::rechnung
       \sqrt{9 + 16} = \sqrt{25} || erst die Summe unter der Wurzel
       = 5 || dann die Wurzel
       :::
       """,
       typische_fehler=[(7, "Du hast $\\sqrt{9} + \\sqrt{16}$ gerechnet. Bei einer Summe darf die Wurzel nicht verteilt werden."),
                        (25, "Die Wurzel fehlt noch: $\\sqrt{25} = 5$.")])

k.mc("Welche Gleichung stimmt für alle $a, b > 0$?",
     ["$\\sqrt{a} \\cdot \\sqrt{b} = \\sqrt{ab}$", "$\\sqrt{a} + \\sqrt{b} = \\sqrt{a + b}$",
      "$\\sqrt{a} - \\sqrt{b} = \\sqrt{a - b}$", "$\\sqrt{a^2 + b^2} = a + b$"],
     "Nur beim Malnehmen (und Teilen) darf man Wurzeln zusammenfassen. Bei Summen und Differenzen gibt es keine solche Regel.",
     tipps=["Teste jede Gleichung mit $a = 9$ und $b = 16$.", "Rechne beide Seiten getrennt aus."],
     fehler={"$\\sqrt{a} + \\sqrt{b} = \\sqrt{a + b}$": "Teste $a = 9$, $b = 16$: links $7$, rechts $5$.",
             "$\\sqrt{a} - \\sqrt{b} = \\sqrt{a - b}$": "Teste $a = 25$, $b = 9$: links $2$, rechts $4$.",
             "$\\sqrt{a^2 + b^2} = a + b$": "Teste $a = 3$, $b = 4$: links $5$, rechts $7$."})

# ── 3: Teilweise Wurzelziehen ──────────────────────────────────────────────
k.erklaerung("Teilweise die Wurzel ziehen", r"""
    ## Quadratzahlen herausholen

    Viele Wurzeln gehen nicht ganz auf, aber zum Teil. Zerlege den Radikanden so,
    dass ein Faktor eine möglichst große Quadratzahl ist. Das heißt
    [[teilweise Wurzelziehen]].

    :::rechnung Beispiel vorgerechnet
    \sqrt{12} = \sqrt{4 \cdot 3} || $4$ ist die größte Quadratzahl in $12$
    = \sqrt{4} \cdot \sqrt{3} || Wurzel eines Produkts
    = 2\sqrt{3} || $\sqrt{4} = 2$
    \sqrt{72} = \sqrt{36 \cdot 2} || $36$ ist die größte Quadratzahl in $72$
    = 6\sqrt{2} || $\sqrt{36} = 6$
    :::

    :::achtung Nicht die größte Quadratzahl
    $\sqrt{72} = \sqrt{4 \cdot 18} = 2\sqrt{18}$ stimmt, ist aber nicht fertig. In
    $18$ steckt noch die $9$. Prüfe am Ende: Unter der Wurzel darf keine Quadratzahl
    größer als $1$ mehr als Faktor stecken.
    :::

    :::alt Mit Paaren erklärt
    Zerlege in Primfaktoren: $72 = 2 \cdot 2 \cdot 2 \cdot 3 \cdot 3$. Jedes Paar
    gleicher Faktoren darf als **ein** Faktor vor die Wurzel. Das Paar $2 \cdot 2$ gibt
    eine $2$, das Paar $3 \cdot 3$ eine $3$. Übrig bleibt eine einzelne $2$. Also
    $\sqrt{72} = 2 \cdot 3 \cdot \sqrt{2} = 6\sqrt{2}$.
    :::
    """)

k.luecke("Ziehe teilweise die Wurzel.",
         "\\sqrt{50} = \\luecke \\sqrt{2}", [[5]],
         "$50 = 25 \\cdot 2$, also $\\sqrt{50} = \\sqrt{25} \\cdot \\sqrt{2} = 5\\sqrt{2}$.",
         tipps=["Welche Quadratzahl steckt in $50$?", "$50 = 25 \\cdot 2$.", "$\\sqrt{25} = 5$."],
         rechenweg=r"""
         :::rechnung
         \sqrt{50} = \sqrt{25 \cdot 2} || größte Quadratzahl $25$
         = \sqrt{25} \cdot \sqrt{2} || Wurzel eines Produkts
         = 5\sqrt{2} || $\sqrt{25} = 5$
         :::
         """,
         typische_fehler=[([25], "Vor die Wurzel kommt $\\sqrt{25} = 5$, nicht $25$."),
                          ([50], "Vor die Wurzel kommt nur die Wurzel des Quadratfaktors: $50 = 25 \\cdot 2$, also $\\sqrt{25} = 5$.")])

k.luecke("Ziehe die Wurzel so weit wie möglich.",
         "\\sqrt{72} = \\luecke \\sqrt{\\luecke}", [[6], [2]],
         "$72 = 36 \\cdot 2$ und $\\sqrt{36} = 6$. Also $\\sqrt{72} = 6\\sqrt{2}$.",
         tipps=["Suche die größte Quadratzahl, die $72$ teilt.", "Probiere $36$.", "$72 = 36 \\cdot 2$."],
         rechenweg=r"""
         :::rechnung
         \sqrt{72} = \sqrt{36 \cdot 2} || größte Quadratzahl $36$
         = 6\sqrt{2} || $\sqrt{36} = 6$
         :::
         """,
         typische_fehler=[([2, 18], "Richtig, aber nicht fertig: In $18$ steckt noch die Quadratzahl $9$."),
                          ([3, 8], "Richtig, aber nicht fertig: In $8$ steckt noch die Quadratzahl $4$."),
                          ([36, 2], "Vor die Wurzel kommt $\\sqrt{36} = 6$.")])

# ── 4: n-te Wurzel und rationale Exponenten ────────────────────────────────
k.erklaerung("n-te Wurzel und Wurzeln als Potenzen", r"""
    ## Die n-te Wurzel

    :::analogie 🧊 Würfel
    Ein Würfel hat $8$ Kubikzentimeter Volumen. Wie lang ist eine Kante? Gesucht ist
    die Zahl, die dreimal malgenommen $8$ ergibt: $2$ Zentimeter.
    :::

    Für $a \ge 0$ ist die [[n-te Wurzel]] $\sqrt[n]{a}$ die nicht negative Zahl, deren
    $n$-te Potenz $a$ ergibt. Bei ungeradem $n$ schreibt man auch $\sqrt[3]{-8} = -2$.
    Viele Uni-Skripte definieren $\sqrt[n]{a}$ aber nur für $a \ge 0$.

    :::rechnung Beispiel vorgerechnet
    \sqrt[3]{8} = 2 || denn $2^3 = 8$
    \sqrt[4]{81} = 3 || denn $3^4 = 81$
    \sqrt[3]{-8} = -2 || ungerade: $(-2)^3 = -8$
    :::

    :::alt Mit Zweierpotenzen erklärt
    Die Wurzel fragt nach der Basis, wenn Potenz und Exponent bekannt sind. Aus der
    Tabelle der Zweierpotenzen liest du ab: $2^{10} = 1024$, also $\sqrt[10]{1024} = 2$.
    Bei der Quadratwurzel ist $n = 2$, das schreibt man einfach nicht hin.
    :::
    ---
    ## Wurzeln als Potenzen

    Nach dem Potenzgesetz ist $\left(a^{\frac{1}{2}}\right)^2 = a^1 = a$. Also muss
    $a^{\frac{1}{2}} = \sqrt{a}$ sein. Allgemein gilt für $a \ge 0$ (bei negativem
    Exponenten $a > 0$) ein [[rationaler Exponent]]:

    $$a^{\frac{1}{n}} = \sqrt[n]{a} \qquad a^{\frac{m}{n}} = \left(\sqrt[n]{a}\right)^m$$

    :::rechnung Beispiel vorgerechnet
    8^{\frac{2}{3}} = (\sqrt[3]{8})^2 || erst die Wurzel
    = 2^2 = 4 || dann die Potenz
    16^{-\frac{1}{2}} = \frac{1}{\sqrt{16}} || negativ: Kehrwert
    = \frac{1}{4} || ausrechnen
    :::

    :::achtung Exponent als Faktor
    $8^{\frac{1}{3}} = \frac{8}{3}$ ist falsch. Der Exponent $\frac{1}{3}$ bedeutet
    dritte Wurzel: $8^{\frac{1}{3}} = 2$.
    :::

    :::alt Mit Halbschritten erklärt
    $9^1 = 9$ ist ein ganzer Schritt, $9^0 = 1$ gar keiner. $9^{\frac{1}{2}}$ ist ein
    halber Schritt: Zweimal hintereinander ergibt er einen ganzen. Welche Zahl mal sich
    selbst ergibt $9$? Die $3$. Also $9^{\frac{1}{2}} = 3$.
    :::
    """)

k.berechne("27^(1/3)",
           erklaerung="$27^{\\frac{1}{3}} = \\sqrt[3]{27} = 3$, denn $3^3 = 27$.",
           tipps=["Hoch $\\frac{1}{3}$ heißt dritte Wurzel.", "Welche Zahl hoch $3$ ergibt $27$?", "$3 \\cdot 3 \\cdot 3$"],
           rechenweg=r"""
           :::rechnung
           27^{\frac{1}{3}} = \sqrt[3]{27} || hoch ein Drittel: dritte Wurzel
           = 3 || denn $3^3 = 27$
           :::
           """,
           typische_fehler=[(9, "Du hast durch $3$ geteilt. Hoch $\\frac{1}{3}$ heißt dritte Wurzel: $3^3 = 27$."),
                            (F(1, 27), "Das wäre $27^{-1}$. Ein Bruch im Exponenten bedeutet Wurzel.")])

k.berechne("16^(3/4)",
           erklaerung="$16^{\\frac{3}{4}} = \\left(\\sqrt[4]{16}\\right)^3 = 2^3 = 8$.",
           tipps=["Erst die Wurzel, dann die Potenz.", "$\\sqrt[4]{16} = 2$, denn $2^4 = 16$.", "$2^3$"],
           rechenweg=r"""
           :::rechnung
           16^{\frac{3}{4}} = (\sqrt[4]{16})^3 || Nenner: Wurzel, Zähler: Potenz
           = 2^3 || $2^4 = 16$
           = 8 || ausrechnen
           :::
           """,
           typische_fehler=[(12, "Du hast $16 \\cdot \\frac{3}{4}$ gerechnet. Der Exponent ist kein Faktor."),
                            (2, "Du hast nur die vierte Wurzel gezogen. Danach noch hoch $3$.")])

k.luecke("Schreibe als Potenz von $x$ ($x > 0$).",
         "\\sqrt[5]{x^{2}} = x^{\\luecke}", [[F(2, 5)]],
         "Die fünfte Wurzel ist hoch $\\frac{1}{5}$: $(x^2)^{\\frac{1}{5}} = x^{\\frac{2}{5}}$.",
         tipps=["Die fünfte Wurzel ist hoch $\\frac{1}{5}$.", "$(x^2)^{\\frac{1}{5}}$", "Exponenten malnehmen: $2 \\cdot \\frac{1}{5}$."],
         rechenweg=r"""
         :::rechnung
         \sqrt[5]{x^2} = (x^2)^{\frac{1}{5}} || Wurzel als Potenz
         = x^{\frac{2}{5}} || Exponenten malnehmen
         :::
         """,
         typische_fehler=[([F(5, 2)], "Der Wurzelexponent kommt in den **Nenner**: $\\frac{2}{5}$."),
                          ([F(-3)], "Bei Potenz einer Potenz wird malgenommen, nicht abgezogen.")])

# ── 5: Nenner rational machen ──────────────────────────────────────────────
k.erklaerung("Den Nenner rational machen", r"""
    ## Wurzel im Nenner wegschaffen

    Die übliche Endform hat keine Wurzel im Nenner. Du [[erweiterst|Erweitern]] mit der Wurzel
    selbst, denn $\sqrt{a} \cdot \sqrt{a} = a$. Das heißt [[Nenner rational machen]].

    :::rechnung Beispiel vorgerechnet
    \frac{1}{\sqrt{2}} = \frac{1 \cdot \sqrt{2}}{\sqrt{2} \cdot \sqrt{2}} || erweitern mit $\sqrt{2}$
    = \frac{\sqrt{2}}{2} || $\sqrt{2} \cdot \sqrt{2} = 2$
    \frac{6}{\sqrt{3}} = \frac{6\sqrt{3}}{3} || erweitern mit $\sqrt{3}$
    = 2\sqrt{3} || kürzen mit $3$
    :::

    :::alt Mit Kopfrechnen erklärt
    Ohne Taschenrechner: Was ist $\frac{1}{\sqrt{2}}$? $1 : 1{,}414\ldots$ rechnet
    sich schlecht. Aber $\frac{\sqrt{2}}{2} = 1{,}414\ldots : 2 = 0{,}707\ldots$ ist leicht.
    Beide Formen haben denselben Wert. Die zweite ist nur bequemer.
    :::
    ---
    ## Summe im Nenner

    Steht $\sqrt{3} - 1$ im Nenner, erweitere mit $\sqrt{3} + 1$. Beim Ausmultiplizieren
    heben sich die gemischten Glieder weg:

    :::rechnung Beispiel vorgerechnet
    (\sqrt{3} - 1)(\sqrt{3} + 1) = \sqrt{3}\sqrt{3} + \sqrt{3} - \sqrt{3} - 1 || jedes mit jedem
    = 3 - 1 = 2 || die Wurzeln heben sich weg
    \frac{4}{\sqrt{3} - 1} = \frac{4(\sqrt{3} + 1)}{2} || erweitern mit $\sqrt{3} + 1$
    = 2\sqrt{3} + 2 || kürzen mit $2$
    :::

    :::achtung Nicht nur den Nenner erweitern
    Den **Zähler** musst du auch mit $\sqrt{3} + 1$ malnehmen. Sonst ändert sich der Wert.
    :::

    :::alt Mit Rechteckflächen erklärt
    Ein Rechteck mit den Seiten $\sqrt{3} + 1$ und $\sqrt{3} - 1$ hat die Fläche
    $3 - 1 = 2$. Das ist das Quadrat mit Seite $\sqrt{3}$ minus ein Quadrat mit Seite
    $1$. Genau so verschwindet die Wurzel aus dem Nenner.
    :::
    """)

k.luecke("Mache den Nenner rational.",
         "\\frac{6}{\\sqrt{3}} = \\luecke \\sqrt{3}", [[2]],
         "Erweitern mit $\\sqrt{3}$: $\\frac{6\\sqrt{3}}{3} = 2\\sqrt{3}$.",
         tipps=["Erweitere mit $\\sqrt{3}$.", "Im Nenner steht dann $\\sqrt{3} \\cdot \\sqrt{3} = 3$.", "$\\frac{6}{3} = 2$."],
         rechenweg=r"""
         :::rechnung
         \frac{6}{\sqrt{3}} = \frac{6\sqrt{3}}{\sqrt{3}\sqrt{3}} || erweitern mit $\sqrt{3}$
         = \frac{6\sqrt{3}}{3} || $\sqrt{3}\sqrt{3} = 3$
         = 2\sqrt{3} || kürzen
         :::
         """,
         typische_fehler=[([6], "Im Nenner bleibt $3$ stehen: $\\frac{6\\sqrt{3}}{3}$. Noch kürzen."),
                          ([F(2, 3)], "$\\sqrt{3} \\cdot \\sqrt{3} = 3$, nicht $9$.")])

k.luecke("Mache den Nenner rational.",
         "\\frac{1}{\\sqrt{2}} = \\frac{\\sqrt{2}}{\\luecke}", [[2]],
         "$\\frac{1 \\cdot \\sqrt{2}}{\\sqrt{2} \\cdot \\sqrt{2}} = \\frac{\\sqrt{2}}{2}$.",
         tipps=["Erweitere mit $\\sqrt{2}$.", "Was ist $\\sqrt{2} \\cdot \\sqrt{2}$?", "Es ist $2$."],
         rechenweg=r"""
         :::rechnung
         \frac{1}{\sqrt{2}} = \frac{\sqrt{2}}{\sqrt{2}\sqrt{2}} || erweitern mit $\sqrt{2}$
         = \frac{\sqrt{2}}{2} || $\sqrt{2}\sqrt{2} = 2$
         :::
         """,
         typische_fehler=[([4], "$\\sqrt{2} \\cdot \\sqrt{2} = 2$, nicht $4$. Die Wurzel macht das Quadrieren rückgängig."),
                          ([1], "Erweitern heißt: oben **und** unten mit $\\sqrt{2}$ malnehmen.")])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


_QUADRATFREI = [2, 3, 5, 6, 7, 10, 11, 13, 14, 15]


def wurzel_teilweise(rng):
    while True:
        kk = rng.randint(2, 10)
        m = rng.choice(_QUADRATFREI)
        n = kk * kk * m
        if n <= 500:
            break
    assert mathlib.wurzel_vereinfachen(n) == (kk, m)
    fehler = [([kk * kk, m], f"Vor die Wurzel kommt $\\sqrt{{{kk * kk}}} = {kk}$, nicht ${kk * kk}$.")]
    for p in (2, 3, 5):
        if kk % p == 0 and kk != p:
            rest = (kk // p) ** 2 * m
            fehler.append(([p, rest], f"Richtig, aber nicht fertig: In ${rest}$ steckt noch die Quadratzahl ${(kk // p) ** 2}$."))
            break
    fehler.append(([m, kk * kk], "Vertauscht: Vor die Wurzel kommt die Wurzel der Quadratzahl, darunter der Rest."))
    gesehen, fe = set(), []
    for w, t in fehler:
        if tuple(w) != (kk, m) and tuple(w) not in gesehen:
            gesehen.add(tuple(w))
            fe.append((w, t))
    return {
        "typ": "luecke",
        "frage": "Ziehe die Wurzel so weit wie möglich.",
        "formel": f"\\sqrt{{{n}}} = \\luecke \\sqrt{{\\luecke}}", "antworten": [[kk], [m]],
        "tipps": [f"Suche die größte Quadratzahl, die ${n}$ teilt.", f"Es ist ${kk * kk}$.", f"${n} = {kk * kk} \\cdot {m}$."],
        "rechenweg": _zeilen((f"\\sqrt{{{n}}} = \\sqrt{{{kk * kk} \\cdot {m}}}", f"größte Quadratzahl ${kk * kk}$"),
                             (f"= \\sqrt{{{kk * kk}}} \\cdot \\sqrt{{{m}}}", "Wurzel eines Produkts"),
                             (f"= {wz(kk, m)}", f"$\\sqrt{{{kk * kk}}} = {kk}$")),
        "erklaerung": "Größte Quadratzahl als Faktor abspalten und ihre Wurzel vor die Wurzel schreiben.",
        "typische_fehler": fe,
    }


def rationaler_exponent(rng):
    while True:
        b = rng.randint(2, 5)
        n = rng.choice([2, 3, 4])
        m = rng.choice([1, 2, 3, -1, -2])
        a = b ** n
        if a <= 625 and F(b) ** abs(m) <= 125 and F(m, n).denominator == n and (b, n, m) != (2, 2, 1):
            break
    w = F(b) ** m
    wurzel = f"\\sqrt{{{a}}}" if n == 2 else f"\\sqrt[{n}]{{{a}}}"
    wname = "Quadratwurzel" if n == 2 else f"{n}. Wurzel"
    zeile1 = (f"{a}^{{{tex(F(m, n))}}} = \\left({wurzel}\\right)^{{{m}}}", f"Nenner ${n}$: {wname}, Zähler ${m}$: Potenz")
    zeilen = [zeile1, (f"= {b}^{{{m}}}", f"${b}^{{{n}}} = {a}$")]
    if m != 1:
        zeilen.append((f"= {tex(w)}", "ausrechnen" if m > 0 else "negativer Exponent: Kehrwert"))
    fehler = [(F(a * m, n), f"Der Exponent ist kein Faktor: ${a}^{{{tex(F(m, n))}}} \\neq {a} \\cdot {tex(F(m, n))}$."),
              (F(b), f"Du hast nur die {wname} gezogen. Danach noch hoch ${m}$.")]
    if m < 0:
        fehler += [(-w, "Ein negativer Exponent macht das Ergebnis nicht negativ. Er bildet den Kehrwert."),
                   (F(b) ** (-m), "Du hast den Kehrwert vergessen: Ein negativer Exponent bildet den Kehrwert.")]
    return {
        "frage": f"Berechne ${a}^{{{tex(F(m, n))}}}$.",
        "loesung": w, "gekuerzt": True,
        "tipps": [f"Der Nenner ${n}$ im Exponenten bedeutet {wname}.",
                  f"${wurzel} = {b}$, denn ${b}^{{{n}}} = {a}$.",
                  f"Jetzt noch ${b}^{{{m}}}$ ausrechnen."],
        "rechenweg": _zeilen(*zeilen),
        "erklaerung": "$a^{\\frac{m}{n}} = (\\sqrt[n]{a})^m$: erst die Wurzel, dann die Potenz.",
        "typische_fehler": ohne_gleiche(w, fehler),
    }


def nenner_rational(rng):
    m = rng.choice([2, 3, 5, 6, 7, 10])
    c = rng.choice([x for x in range(1, 13) if x % m != 0] + [m * j for j in range(1, 5)] * 2)
    w = F(c, m)
    zeilen = [(f"\\frac{{{c}}}{{\\sqrt{{{m}}}}} = \\frac{{{c}\\sqrt{{{m}}}}}{{\\sqrt{{{m}}}\\sqrt{{{m}}}}}", f"erweitern mit $\\sqrt{{{m}}}$"),
              (f"= \\frac{{{c}\\sqrt{{{m}}}}}{{{m}}}", f"$\\sqrt{{{m}}}\\sqrt{{{m}}} = {m}$")]
    if math.gcd(c, m) > 1:
        vor = "" if w == 1 else tex(w)
        zeilen.append((f"= {vor}\\sqrt{{{m}}}", "kürzen"))
    fehler = [([F(c, m * m)], f"$\\sqrt{{{m}}} \\cdot \\sqrt{{{m}}} = {m}$, nicht ${m * m}$."),
              ([c], f"Der Nenner ${m}$ fehlt noch.")]
    fehler = [(f, t) for f, t in fehler if f[0] != w]
    return {
        "typ": "luecke",
        "frage": "Mache den Nenner rational. Gib den Vorfaktor gekürzt an (Bruch oder ganze Zahl).",
        "formel": f"\\frac{{{c}}}{{\\sqrt{{{m}}}}} = \\luecke \\cdot \\sqrt{{{m}}}", "antworten": [[w]],
        "formen": ["gekuerzt"],
        "tipps": [f"Erweitere mit $\\sqrt{{{m}}}$.", f"Im Nenner steht dann ${m}$.", f"Vorfaktor: $\\frac{{{c}}}{{{m}}}$, gekürzt."],
        "rechenweg": _zeilen(*zeilen),
        "erklaerung": "Mit der Wurzel im Nenner erweitern, denn $\\sqrt{a} \\cdot \\sqrt{a} = a$.",
        "typische_fehler": fehler,
    }


k.praxis()

k.generator(wurzel_teilweise, typ="luecke", titel="Teilweise Wurzelziehen")
k.generator(rationaler_exponent, typ="zahl", titel="Rationale Exponenten", glatt=True)
k.generator(nenner_rational, typ="luecke", titel="Nenner rational machen")

k.luecke("Mache den Nenner rational (Summe im Nenner).",
         "\\frac{2}{\\sqrt{3} - 1} = \\sqrt{3} + \\luecke", [[1]],
         "Erweitern mit $\\sqrt{3} + 1$: Nenner $(\\sqrt{3} - 1)(\\sqrt{3} + 1) = 2$, Zähler $2(\\sqrt{3} + 1)$. Kürzen mit $2$.",
         tipps=["Erweitere mit $\\sqrt{3} + 1$.", "Der Nenner wird $3 - 1 = 2$.", "$\\frac{2(\\sqrt{3} + 1)}{2}$"],
         rechenweg=r"""
         :::rechnung
         \frac{2}{\sqrt{3} - 1} = \frac{2(\sqrt{3} + 1)}{(\sqrt{3} - 1)(\sqrt{3} + 1)} || erweitern mit $\sqrt{3} + 1$
         = \frac{2(\sqrt{3} + 1)}{3 - 1} || gemischte Glieder heben sich weg
         = \sqrt{3} + 1 || kürzen mit $2$
         :::
         """,
         typische_fehler=[([-1], "Erweitere mit $\\sqrt{3} + 1$, nicht mit $\\sqrt{3} - 1$. Dann bleibt im Zähler $+1$."),
                          ([2], "Der Nenner wird $2$, also kürzt sich die $2$ im Zähler weg: $\\sqrt{3} + 1$.")])

# Übungsblatt-Stil
_a, _b, _c = 50, 18, 8
_ka, _kb, _kc = (mathlib.wurzel_vereinfachen(x)[0] for x in (_a, _b, _c))
_summe = _ka + _kb - _kc
k.rechenweg_aufgabe(r"""
    ## Übungsblatt-Stil: Wurzelterme zusammenfassen

    Vereinfache so weit wie möglich und gib alle Zwischenschritte an:
    $$\sqrt{50} + \sqrt{18} - \sqrt{8}$$
    """,
    [{"typ": "luecke", "frage": "Ziehe teilweise die Wurzel.", "formel": "\\sqrt{50} = \\luecke \\sqrt{2}", "antworten": [[_ka]],
      "tipps": ["$50 = 25 \\cdot 2$", "$\\sqrt{25} = 5$"], "rechenweg": "$\\sqrt{50} = \\sqrt{25 \\cdot 2} = 5\\sqrt{2}$",
      "typische_fehler": [([25], "Vor die Wurzel kommt $\\sqrt{25} = 5$.")]},
     {"typ": "luecke", "frage": "Ziehe teilweise die Wurzel.", "formel": "\\sqrt{18} = \\luecke \\sqrt{2}", "antworten": [[_kb]],
      "tipps": ["$18 = 9 \\cdot 2$", "$\\sqrt{9} = 3$"], "rechenweg": "$\\sqrt{18} = \\sqrt{9 \\cdot 2} = 3\\sqrt{2}$",
      "typische_fehler": [([9], "Vor die Wurzel kommt $\\sqrt{9} = 3$.")]},
     {"typ": "luecke", "frage": "Ziehe teilweise die Wurzel.", "formel": "\\sqrt{8} = \\luecke \\sqrt{2}", "antworten": [[_kc]],
      "tipps": ["$8 = 4 \\cdot 2$", "$\\sqrt{4} = 2$"], "rechenweg": "$\\sqrt{8} = \\sqrt{4 \\cdot 2} = 2\\sqrt{2}$",
      "typische_fehler": [([4], "Vor die Wurzel kommt $\\sqrt{4} = 2$.")]},
     {"typ": "luecke", "frage": "Fasse zusammen.", "formel": "5\\sqrt{2} + 3\\sqrt{2} - 2\\sqrt{2} = \\luecke \\sqrt{2}",
      "antworten": [[_summe]],
      "tipps": ["$\\sqrt{2}$ ist wie eine Einheit: $5$ Stück plus $3$ Stück minus $2$ Stück.", "$5 + 3 - 2$"],
      "rechenweg": "$5\\sqrt{2} + 3\\sqrt{2} - 2\\sqrt{2} = (5 + 3 - 2)\\sqrt{2} = 6\\sqrt{2}$",
      "typische_fehler": [([10], "Minus $2\\sqrt{2}$: abziehen, nicht addieren.")]}],
    "Erst jede Wurzel teilweise ziehen. Gleiche Wurzeln fasst du dann wie gleiche Einheiten zusammen.",
    uebungsblatt=True,
    tipps=["Ziehe aus jeder Wurzel die größte Quadratzahl heraus.", "Überall bleibt $\\sqrt{2}$ übrig."],
    rechenweg=r"""
    :::rechnung
    \sqrt{50} + \sqrt{18} - \sqrt{8} = \sqrt{25 \cdot 2} + \sqrt{9 \cdot 2} - \sqrt{4 \cdot 2} || größte Quadratzahlen
    = 5\sqrt{2} + 3\sqrt{2} - 2\sqrt{2} || teilweise Wurzel ziehen
    = 6\sqrt{2} || zusammenfassen
    :::
    """)

k.papier(r"""
    ## Erklären wie in der Übung

    Jemand behauptet: „Für alle $a, b \ge 0$ gilt $\sqrt{a + b} = \sqrt{a} + \sqrt{b}$.“

    Widerlege die Aussage auf Papier. Zeige dann, dass für $a, b \ge 0$ immer
    $\sqrt{a + b} \le \sqrt{a} + \sqrt{b}$ gilt.
    """,
    r"""
    **Widerlegung:** Ein Gegenbeispiel genügt. Für $a = 9$, $b = 16$ ist
    $\sqrt{9 + 16} = \sqrt{25} = 5$, aber $\sqrt{9} + \sqrt{16} = 3 + 4 = 7$.

    **Ungleichung:** Beide Seiten sind nicht negativ. Daher darf man quadrieren, ohne
    dass sich das Ungleichheitszeichen umdreht:
    $$\left(\sqrt{a} + \sqrt{b}\right)^2 = a + 2\sqrt{a}\sqrt{b} + b \ge a + b = \left(\sqrt{a + b}\right)^2,$$
    denn $2\sqrt{a}\sqrt{b} \ge 0$. Aus dem Vergleich der Quadrate nicht negativer Zahlen
    folgt $\sqrt{a + b} \le \sqrt{a} + \sqrt{b}$.
    """,
    ["Ich habe ein konkretes Gegenbeispiel mit Zahlen angegeben",
     "Ich habe begründet, warum ich quadrieren darf (beide Seiten nicht negativ)",
     "Ich habe $(\\sqrt{a} + \\sqrt{b})^2$ richtig ausmultipliziert"],
    "Eine Allaussage widerlegt man mit einem einzigen Gegenbeispiel.",
    tipps=["Probiere Quadratzahlen für $a$ und $b$."])

k.zusammenfassung(r"""
    ## Wurzeln

    | Regel | Formel | Beispiel |
    |---|---|---|
    | Quadratwurzel | $\sqrt{a} \ge 0$ und $(\sqrt{a})^2 = a$ | $\sqrt{49} = 7$ |
    | n-te Wurzel ($a \ge 0$) | $(\sqrt[n]{a})^n = a$ | $\sqrt[3]{8} = 2$ |
    | Produkt ($a, b \ge 0$) | $\sqrt{a} \cdot \sqrt{b} = \sqrt{ab}$ | $\sqrt{2} \cdot \sqrt{8} = 4$ |
    | Quotient ($a \ge 0$, $b > 0$) | $\frac{\sqrt{a}}{\sqrt{b}} = \sqrt{\frac{a}{b}}$ | $\frac{\sqrt{75}}{\sqrt{3}} = 5$ |
    | teilweise ziehen | größte Quadratzahl herausholen | $\sqrt{72} = 6\sqrt{2}$ |
    | als Potenz ($a > 0$) | $a^{\frac{m}{n}} = (\sqrt[n]{a})^m$ | $8^{\frac{2}{3}} = 4$ |
    | Nenner rational | mit der Wurzel erweitern | $\frac{6}{\sqrt{3}} = 2\sqrt{3}$ |

    !! $\sqrt{a + b} \neq \sqrt{a} + \sqrt{b}$: $\sqrt{9 + 16} = 5$, nicht $7$.

    - $\sqrt{9} = 3$, nicht $\pm 3$. Aber $x^2 = 9$ hat die Lösungen $3$ und $-3$.
    - Aus negativen Zahlen gibt es keine Quadratwurzel in $\mathbb{R}$.
    - Steht $\sqrt{a} - b$ im Nenner, erweitere mit $\sqrt{a} + b$; steht $\sqrt{a} + b$ dort, mit $\sqrt{a} - b$.
""")
