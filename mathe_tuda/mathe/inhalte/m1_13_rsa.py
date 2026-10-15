# -*- coding: utf-8 -*-
"""Mathe 1, Kapitel 13: Kryptographie RSA (Skript Disser WS 26/27, Abschn. 2.9, Def. 2.65 bis Bsp. 2.69)."""
from math import gcd, factorial

from ..engine import neues_kapitel, ohne_gleiche
from .. import mathlib

k = neues_kapitel(
    slug="rsa",
    titel="Kryptographie: RSA",
    beschreibung="Primzahlen, Primzahllemma, kleiner Satz von Fermat, RSA-Schlüssel, Ver- und Entschlüsseln, Korrektheit, Beispiel n = 55",
    teil="mathe1",
    quelle="Skript Disser WS 26/27, Abschn. 2.9",
    icon="🔐")


# ── Python rechnet alles nach ──────────────────────────────────────────────
def ist_prim(z):
    return z > 1 and all(z % t for t in range(2, z))


def potenz_kette(c, d, n):
    """Square-and-Multiply mit Rest nach jedem Schritt. Ergebnis: (Zeilen [(tex, grund)], Wert c^d mod n)."""
    zeilen = []
    quad = [c % n]
    bits = bin(d)[2:][::-1]
    for i in range(1, len(bits)):
        v = quad[-1]
        neu = v * v % n
        zeilen.append((f"{v} \\cdot {v} = {v * v} = {v * v // n} \\cdot {n} + {neu}", f"$c^{{{2 ** i}}} \\bmod {n}$ durch Quadrieren"))
        quad.append(neu)
    acc, erster = 1, True
    for i, b in enumerate(bits):
        if b == "1":
            if erster:
                acc, erster = quad[i], False
            else:
                neu = acc * quad[i] % n
                zeilen.append((f"{acc} \\cdot {quad[i]} = {acc * quad[i]} = {acc * quad[i] // n} \\cdot {n} + {neu}", f"Faktor $c^{{{2 ** i}}}$ einmultipliziert"))
                acc = neu
    assert acc == pow(c, d, n)
    return zeilen, acc


# Def. 2.65 und Beispiele
assert [z for z in range(2, 14) if ist_prim(z)] == [2, 3, 5, 7, 11, 13] and not ist_prim(1) and not ist_prim(15)
assert (5 * 11, (5 - 1) * (11 - 1)) == (55, 40)
# Satz 2.66: Primzahllemma (und warum "prim" nötig ist)
assert all(not ((a * b) % p == 0) or a % p == 0 or b % p == 0 for p in range(2, 60) if ist_prim(p) for a in range(60) for b in range(60))
assert (3 * 4) % 6 == 0 and 3 % 6 != 0 and 4 % 6 != 0
assert 3 * 10 == 30 == 6 * 5 and 3 == 0 * 5 + 3 and 10 == 2 * 5
for _p in (5, 7, 11, 13):
    for _a in range(1, _p):
        _M = [x for x in range(1, 3 * _p) if (x * _a) % _p == 0]
        assert min(_M) == _p                       # min M = p, wie im Beweis
# Satz 2.67: Fermat
assert all(pow(a, p - 1, p) == 1 for p in range(2, 80) if ist_prim(p) for a in range(1, p))
assert pow(5, 5, 6) == 5 and 5 ** 5 == 3125 == 520 * 6 + 5 and pow(3, 7, 8) == 3
assert [pow(3, e, 7) for e in range(1, 7)] == [3, 2, 6, 4, 5, 1]
_perm = [3 * x % 7 for x in range(1, 7)]
assert _perm == [3, 6, 2, 5, 1, 4] and sorted(_perm) == [1, 2, 3, 4, 5, 6] and 3 * 6 * 2 * 5 * 1 * 4 == 720 == factorial(6)
# Beispiel 2.69
assert (3 * 27) % 40 == 1 and 3 * 27 == 81 == 2 * 40 + 1
assert pow(12, 3, 55) == 23 and 12 ** 2 == 144 == 2 * 55 + 34 and 34 * 12 == 408 == 7 * 55 + 23
assert [pow(23, i, 55) for i in range(1, 5)] == [23, 34, 12, 1] and 23 * 23 == 529 == 9 * 55 + 34
assert 34 * 23 == 782 == 14 * 55 + 12 and 12 * 23 == 276 == 5 * 55 + 1 and 27 == 4 * 6 + 3
assert pow(23, 27, 55) == 12
# Satz 2.68: Korrektheit für alle m < n im Beispiel
assert all(pow(pow(m, 3, 55), 27, 55) == m for m in range(55))
assert 60 % 55 == 5 and pow(pow(60, 3, 55), 27, 55) == 5                       # m >= n: man bekommt m mod n zurück
assert pow(12, 81, 5) == 12 % 5 == 2 and pow(12, 81, 11) == 12 % 11 == 1 and 81 == 1 + 2 * 40
# Aufgaben
assert (7 * 13, (7 - 1) * (13 - 1), 5 * 29 % 72, pow(10, 5, 91)) == (91, 72, 1, 82)
assert pow(7, 3, 55) == 13 and 343 == 6 * 55 + 13
assert (7 * 11, 60, 7 * 43 % 60, pow(2, 7, 77), pow(51, 43, 77)) == (77, 60, 1, 51, 2)
assert pow(3, 100, 101) == 1

k.lernziele([
    "Ich kenne die Definition der Primzahl und das Primzahllemma $p \\mid a \\cdot b \\Rightarrow p \\mid a \\lor p \\mid b$ samt Beweis (Def. 2.65, Satz 2.66)",
    "Ich wende den kleinen Satz von Fermat $a^{p-1} \\bmod p = 1$ an und kenne die Beweisidee mit der Permutation $x \\mapsto ax \\bmod p$ (Satz 2.67)",
    "Ich erzeuge RSA-Schlüssel mit $n = pq$, $t = (p-1)(q-1)$ und $ed \\bmod t = 1$ und ver- und entschlüssele kleine Zahlen von Hand (Bsp. 2.69, $n = 55$)",
    "Ich verstehe, warum $g(f(m)) = m$ für alle $m < n$ gilt, und kann den Beweis von Satz 2.68 Schritt für Schritt nachvollziehen",
])

k.warum(r"""
Jede HTTPS-Verbindung, jede Signatur in Git oder SSH-Schlüssel beruht auf Public-Key-Kryptographie. RSA ist das älteste verbreitete Verfahren,
und seine Sicherheit beruht auf einer Annahme der Informatik: Primfaktorzerlegung großer Zahlen ist (nach heutigem Wissen) schwer, das Multiplizieren aber leicht.
In diesem Kapitel siehst du, dass die Mathematik dahinter nur aus dem besteht, was du in Kapitel 2 aufgebaut hast: Rest, Potenz und Primzahlen.
Dass ein Rechner $m^e \bmod n$ mit riesigen Zahlen schnell ausrechnet, liegt an Satz 2.44 und Satz 2.52: Er nimmt nach jedem Schritt den Rest.
""")

# ── Seite 1: Idee und Primzahlen ─────────────────────────────────────────
k.erklaerung("Schlüssel, die jeder kennen darf (Def. 2.65)", r"""
## Die Idee von Public-Key-Verschlüsselung

:::analogie 📮 Der Briefkasten
In einen Briefkasten kann jeder einen Brief einwerfen, aber nur wer den Schlüssel hat, holt ihn heraus. Beim [[RSA|RSA-Verfahren]] ist der Einwurf öffentlich (öffentlicher Schlüssel), das Herausholen geheim.
:::

**Definition 2.65.** Eine Zahl $p \in \mathbb{N}$ heißt [[Primzahl]], wenn $p > 1$ gilt und $p$ keine Teiler außer $1$ und $p$ hat.

RSA wählt zwei **verschiedene** (große) Primzahlen $p, q$ und berechnet $n := p \cdot q$ und $t := (p-1)(q-1)$. Die einzigen nichttrivialen Teiler von $n$ sind $p$ und $q$.
Wer $n$ kennt, kennt $t$ nur, wenn er $n$ in Primfaktoren zerlegen kann.

:::rechnung Primzahlen und das Beispiel $p = 5$, $q = 11$
15 = 3 \cdot 5 || nicht prim: $3$ ist ein Teiler. Die Zahl $1$ ist auch nicht prim, denn Primzahlen sind größer als $1$
5 \cdot 11 = 55 || $n = p \cdot q$
(5 - 1)(11 - 1) = 40 || $t = (p-1)(q-1)$
:::

:::alt Mit Mischen von Farben
Zwei Farben zu mischen ist leicht. Aus der gemischten Farbe die beiden Ausgangsfarben zu bestimmen ist schwer. $n = p \cdot q$ ist die gemischte Farbe, $p$ und $q$ sind die Ausgangsfarben.
:::
""")

k.mehrfach("Welche dieser Zahlen sind Primzahlen (Definition 2.65)?",
           ["$2$", "$13$", "$53$"], ["$1$", "$51$", "$91$"],
           r"$1$ ist keine Primzahl ($p > 1$ ist verlangt). $51 = 3 \cdot 17$ und $91 = 7 \cdot 13$ haben echte Teiler. $2$, $13$ und $53$ haben nur die Teiler $1$ und sich selbst.",
           tipps=["Suche für jede Zahl einen Teiler zwischen $2$ und der Zahl.", r"$51 = 3 \cdot 17$", r"$91 = 7 \cdot 13$, und die $1$ ist nach Definition nicht prim."],
           fehler={"$1$": r"Definition 2.65 verlangt $p > 1$. Die Zahl $1$ ist keine Primzahl.",
                   "$51$": r"$51 = 3 \cdot 17$: $3$ ist ein echter Teiler.",
                   "$91$": r"$91 = 7 \cdot 13$: Das sieht nach Primzahl aus, ist aber ein Produkt."})

# ── Seite 2: Schlüsselerzeugung ──────────────────────────────────────────
k.erklaerung("RSA im Überblick: Schlüssel, Ver- und Entschlüsseln", r"""
## Zahlen für den öffentlichen und den geheimen Schlüssel

Zu $p, q$ mit $n = pq$ und $t = (p-1)(q-1)$ bestimmt RSA $e, d \in \mathbb{N} \setminus \{0\}$ mit $(e \cdot d) \bmod t = 1$. Das ist effizient möglich (Seite 10 zeigt mit dem [[euklidischen Algorithmus|euklidischer Algorithmus]] einen Weg).

- **Öffentlicher Schlüssel:** $(n, e)$. **Geheim:** $d$ (und $p$, $q$).
- **Verschlüsseln** einer Zahl $m$: $f\colon \mathbb{N} \to \mathbb{N},\ m \mapsto m^e \bmod n$.
- **Entschlüsseln** von $c$: $g\colon \mathbb{N} \to \mathbb{N},\ c \mapsto c^d \bmod n$.

Eine Nachricht ist ein Tupel natürlicher Zahlen, jede Zahl wird einzeln verschlüsselt.

:::rechnung Das Beispiel 2.69: $p = 5$, $q = 11$, $e = 3$, $d = 27$
5 \cdot 11 = 55 || $n$
4 \cdot 10 = 40 || $t$
3 \cdot 27 = 81 = 2 \cdot 40 + 1 || $e \cdot d \bmod t = 1$ ✓: $e$ und $d$ passen zusammen
:::

:::achtung Die Rollen
$e$ und $n$ dürfen alle kennen, $d$, $p$ und $q$ nicht. Wer $n$ zerlegen kann, kann $t$ und daraus $d$ berechnen: Dann ist RSA gebrochen.
:::

:::alt Als Vorhängeschloss
Du verteilst offene Vorhängeschlösser $(n, e)$. Jeder kann damit eine Kiste abschließen, aber nur du hast den Schlüssel $d$ zum Aufschließen.
:::
""")

k.zuordnen("Ordne die RSA-Bestandteile ihrer Rolle zu (Abschnitt 2.9).",
           [("$(n, e)$", "öffentlicher Schlüssel"),
            ("$d$", "geheimer Schlüssel"),
            ("$m \\mapsto m^e \\bmod n$", "Verschlüsseln"),
            ("$c \\mapsto c^d \\bmod n$", "Entschlüsseln"),
            ("$t = (p-1)(q-1)$", "Modul für $e \\cdot d \\bmod t = 1$")],
           "Der öffentliche Schlüssel verschlüsselt, der geheime entschlüsselt. $t$ taucht nur bei der Schlüsselerzeugung auf.",
           ablenker=["Modul der Verschlüsselung ist $t$"],
           tipps=["Wer darf den Schlüssel kennen: jeder oder nur der Empfänger?", "Zum Verschlüsseln braucht man $n$ und $e$."])

k.luecke(r"RSA-Schlüssel für $p = 7$ und $q = 13$: Berechne $n$ und $t$.",
         r"n = \luecke \quad \text{und} \quad t = \luecke",
         [[91], [72]],
         r"$n = 7 \cdot 13 = 91$ und $t = (7 - 1)(13 - 1) = 6 \cdot 12 = 72$.",
         tipps=[r"$n = p \cdot q$", r"$t = (p-1)(q-1)$, nicht $p \cdot q - 1$.", r"$6 \cdot 12$"],
         rechenweg=r"""
:::rechnung
7 \cdot 13 = 91 || $n = p \cdot q$
(7 - 1)(13 - 1) = 6 \cdot 12 = 72 || $t = (p-1)(q-1)$
:::
""",
         typische_fehler=[([91, 90], r"Du hast $n - 1$ statt $(p-1)(q-1)$ gerechnet. $n - 1 = 90$ ist nur für **prime** $n$ das passende $t$."),
                          ([20, 72], r"Du hast $p + q$ gerechnet. Der Modul ist das **Produkt**.")])

# ── Seite 3: Primzahllemma ───────────────────────────────────────────────
k.erklaerung("Das Primzahllemma (Satz 2.66)", r"""
## Teilt eine Primzahl ein Produkt, teilt sie einen Faktor

**Satz 2.66 (Primzahllemma).** Für jede Primzahl $p$ und alle $a, b \in \mathbb{N}$ gilt
$$p \mid a \cdot b \quad \Rightarrow \quad p \mid a \ \text{ oder } \ p \mid b.$$

Für Primzahlen ist das ein Verbot: Die Primzahl kann nicht „auf zwei Faktoren verteilt“ sein. Bei zusammengesetzten Zahlen geht das, deshalb braucht der Satz $p$ prim.

:::rechnung Beispiel $p = 5$ und Gegenbeispiel $6$
3 \cdot 10 = 30 = 6 \cdot 5 || $5 \mid 30$
3 = 0 \cdot 5 + 3 || Rest $3 \neq 0$, also $5 \nmid 3$
10 = 2 \cdot 5 || also $5 \mid 10$, wie der Satz verlangt
3 \cdot 4 = 12 = 2 \cdot 6 || $6 \mid 12$, aber $6 \nmid 3$ und $6 \nmid 4$: $6$ ist nicht prim
:::

:::alt Mit Zutaten
Die Primzahl $5$ ist wie eine unteilbare Zutat. Steckt sie im Produkt, steckt sie in einem der Faktoren. Die $6 = 2 \cdot 3$ besteht aus zwei Zutaten, die sich auf zwei Faktoren verteilen können.
:::
""")

k.wf(r"Für jede Zahl $z \in \mathbb{N}$ gilt: $z \mid a \cdot b \Rightarrow z \mid a$ oder $z \mid b$.", False,
     r"Falsch. Das Primzahllemma gilt nur für Primzahlen. Gegenbeispiel: $z = 6$, $a = 3$, $b = 4$: $6 \mid 12$, aber $6 \nmid 3$ und $6 \nmid 4$.",
     tipps=["Probiere eine Zahl, die keine Primzahl ist, zum Beispiel $6$."])

# ── Seite 4: Beweis ──────────────────────────────────────────────────────
k.erklaerung("Beweis des Primzahllemmas", r"""
## Die kleinste Zahl mit $p \mid x \cdot a$

Gelte $p \mid a \cdot b$ und $p \nmid a$. Wir zeigen $p \mid b$.

1. $M := \{x \in \mathbb{N} \setminus \{0\} \mid p \mid x \cdot a\}$ enthält $p$, hat also ein Minimum $m$ (Satz 2.16). Es ist $1 \notin M$, da $p \nmid a$.
2. Division mit Rest $p = q \cdot m + r$, $r < m$: Aus $p \mid p \cdot a$ und $p \mid q \cdot m \cdot a$ folgt $p \mid r \cdot a$. Wäre $r \neq 0$, läge $r$ in $M$, aber $r < m$. Also $r = 0$.
3. Dann gilt $m \mid p$. Da $p$ prim und $m \neq 1$ ist, ist $m = p$.
4. Division $b = s \cdot p + t$, $t < p = m$: Aus $p \mid a \cdot b$ folgt $p \mid a \cdot t$. Wäre $t \neq 0$, läge $t$ in $M$: Widerspruch. Also $t = 0$ und $p \mid b$. $\square$

:::rechnung Das Minimum von $M$ für $p = 7$, $a = 3$
3 \cdot x \text{ für } x = 1, \ldots, 6 \text{ ist } 3, 6, 9, 12, 15, 18 || keine dieser Zahlen ist durch $7$ teilbar: kein $x < 7$ liegt in $M$
21 = 3 \cdot 7 || $x = 7$ liegt in $M$: $7 \mid 21$, also $\min M = 7 = p$
:::

:::alt Als Wecker
Du stellst $a$-mal Wecker im Abstand $x$ und fragst, wann zum ersten Mal die Primzahl $p$ den Gesamtabstand teilt. Das passiert zum ersten Mal bei $x = p$. Genau das benutzt der Beweis.
:::
""")

k.ordnen(r"Ordne den Beweis des Primzahllemmas (Satz 2.66): $p \mid a \cdot b$ und $p \nmid a$ ergeben $p \mid b$.",
         [r"Setze $M := \{x \in \mathbb{N} \setminus \{0\} \mid p \mid x \cdot a\}$. Es gilt $p \in M$, also hat $M$ ein Minimum $m$, und $1 \notin M$ wegen $p \nmid a$.",
          r"Division mit Rest: $p = q \cdot m + r$ mit $r < m$. Aus $p \mid p \cdot a$ und $p \mid q \cdot m \cdot a$ folgt $p \mid r \cdot a$.",
          r"Wäre $r \neq 0$, so $r \in M$ mit $r < m$, im Widerspruch zur Minimalität. Also $r = 0$ und $m \mid p$.",
          r"Da $p$ prim ist und $m \neq 1$ gilt, folgt $m = p$.",
          r"Division $b = s \cdot p + t$ mit $t < p$. Aus $p \mid a \cdot b$ und $p \mid a \cdot s \cdot p$ folgt $p \mid a \cdot t$. Wäre $t \neq 0$, läge $t$ in $M$ mit $t < m$: Widerspruch. Also $t = 0$, das heißt $p \mid b$. $\square$"],
         r"Der Trick ist die Menge $M$: Ihr Minimum erweist sich als $p$, und die Division von $b$ durch $p$ liefert den Rest $0$.",
         ablenker=[r"Setze $M := \{x \in \mathbb{N} \mid x \cdot a \le p\}$ und bestimme ihr Maximum.",
                   r"Da $p$ prim ist, gilt $m = 1$."],
         tipps=["Der Beweis führt eine neue Menge ein, deren Minimum untersucht wird.", "Warum kann $m$ nicht $1$ sein?",
                "Am Ende wird $b$ durch $p$ mit Rest geteilt."])

# ── Seite 5: Fermat ──────────────────────────────────────────────────────
k.erklaerung("Der kleine Satz von Fermat (Satz 2.67)", r"""
## Potenzen modulo einer Primzahl wiederholen sich

**Satz 2.67 (kleiner Satz von Fermat).** Ist $p$ eine Primzahl und $p \nmid a$, so gilt $a^{p-1} \bmod p = 1$.

:::visual modulo_uhr
{"n": 7, "start": 3, "potenz": 6, "interaktiv": true,
 "unterschrift": "Potenzen von $3$ modulo $7$: $3, 2, 6, 4, 5, 1$. Nach $p - 1 = 6$ Schritten steht dort $1$."}
:::

:::rechnung Fermat gilt für Primzahlen, nicht für beliebige Zahlen
3^6 = 729 = 104 \cdot 7 + 1 || $p = 7$ ist prim: $3^{p-1} \bmod p = 1$ ✓
5^5 = 3125 = 520 \cdot 6 + 5 || $6$ ist nicht prim: der Rest ist $5$, nicht $1$
:::

:::achtung Die Voraussetzung $p \nmid a$
Für Vielfache von $p$ gilt $a^{p-1} \bmod p = 0$, nicht $1$. Und die Aussage gilt nur für Primzahlen $p$.
:::

:::alt Als Kreisverkehr
Die Potenzen $a, a^2, a^3, \ldots$ laufen modulo $p$ im Kreis. Fermat sagt: Spätestens nach $p - 1$ Schritten stehst du wieder bei $1$.
:::
""")

k.zahl(r"Berechne $3^{100} \bmod 101$. Es ist $101$ eine Primzahl.", 1,
       r"$101$ ist prim und $101 \nmid 3$, also gilt nach Satz 2.67 $3^{101-1} \bmod 101 = 3^{100} \bmod 101 = 1$.",
       tipps=[r"Vergleiche den Exponenten mit $p - 1$.", r"$p = 101$, also $p - 1 = 100$.", "Satz 2.67 liefert direkt den Rest."],
       rechenweg=r"""
:::rechnung
101 - 1 = 100 || der Exponent ist genau $p - 1$
3^{100} \bmod 101 = 1 \text{ nach Satz 2.67} || $101$ prim, $101 \nmid 3$
:::
""",
       typische_fehler=[(3, r"Der Rest ist nicht die Basis. Fermat sagt $a^{p-1} \equiv 1$, nicht $a^p \equiv a^{p-1}$."),
                        (100, r"$100 = p - 1$ ist der Exponent, nicht der Rest.")])

k.mc(r"Warum gilt $a^{p-1} \bmod p = 1$ für $p = 6$ und $a = 5$ **nicht**?",
     [r"Weil $6$ keine Primzahl ist: $5^5 = 3125 = 520 \cdot 6 + 5$ hat den Rest $5$",
      r"Weil $5$ größer als $p - 1$ ist",
      r"Weil $a$ durch $p$ teilbar sein muss",
      r"Weil der Satz nur für $p > 100$ gilt"],
     r"Satz 2.67 braucht $p$ prim. Für $6 = 2 \cdot 3$ gilt es nicht: $5^5 \bmod 6 = 5$. $5 < 6$ ist kein Problem, und $p \nmid a$ ist gerade verlangt.",
     tipps=[r"Berechne $5^5 \bmod 6$ (mit $5 \equiv -1$ oder Stück für Stück).", "Welche Voraussetzung an $p$ steht im Satz?", r"Ist $6$ prim?"],
     fehler={r"Weil $5$ größer als $p - 1$ ist": r"$5 = p - 1$. Das ist erlaubt, es kommt nur auf $p \nmid a$ und $p$ prim an.",
             r"Weil $a$ durch $p$ teilbar sein muss": r"Genau umgekehrt: Der Satz verlangt $p \nmid a$.",
             r"Weil der Satz nur für $p > 100$ gilt": r"Der Satz gilt für jede Primzahl, etwa $3^6 \bmod 7 = 1$."})

# ── Seite 6: Beweis Fermat ───────────────────────────────────────────────
k.erklaerung("Beweis des kleinen Satzes von Fermat", r"""
## Eine Permutation, zwei Produkte

Multipliziere die Zahlen $1, \ldots, p-1$ mit $a$ und nimm den Rest. Weil $p \nmid a$, kommt dabei nie $0$ heraus (Satz 2.66), und zwei verschiedene Zahlen landen nie beim selben Rest.
Die Abbildung $f\colon x \mapsto (a \cdot x) \bmod p$ ist also eine Permutation von $\{1, \ldots, p-1\}$: Sie **ordnet nur um**. Deshalb haben $\prod ((a x) \bmod p)$ und $\prod x$ dieselben Faktoren.

Mit Satz 2.44 folgt $(p-1)! \equiv a^{p-1} \cdot (p-1)! \pmod p$. Da $p \nmid (p-1)!$, darf man durch $(p-1)!$ „kürzen“ (Satz 2.66).

:::rechnung $p = 7$, $a = 3$
3 \cdot 1 = 3 = 0 \cdot 7 + 3 || $f(1) = 3$
3 \cdot 3 = 9 = 1 \cdot 7 + 2 || $f(3) = 2$
3 \cdot 5 = 15 = 2 \cdot 7 + 1 || $f(5) = 1$; ebenso $f(2) = 6$, $f(4) = 5$, $f(6) = 4$
3 \cdot 6 \cdot 2 \cdot 5 \cdot 1 \cdot 4 = 720 = 1 \cdot 2 \cdot 3 \cdot 4 \cdot 5 \cdot 6 || dieselben Faktoren in anderer Reihenfolge, also dasselbe Produkt $6!$
:::

:::alt Als Tischordnung
Sechs Gäste sitzen in Reihenfolge $1, \ldots, 6$. Das Multiplizieren mit $3$ (mod $7$) mischt sie neu, aber es sitzen noch immer genau dieselben sechs Gäste da.
:::
""")

k.ordnen(r"Ordne den Beweis des kleinen Satzes von Fermat (Satz 2.67): $p$ prim und $p \nmid a$ ergeben $a^{p-1} \bmod p = 1$.",
         [r"Wegen Satz 2.66 und $p \nmid a$ gilt $p \nmid a \cdot x$ für $0 < x < p$. Also ist $f\colon p \setminus \{0\} \to p \setminus \{0\}$, $x \mapsto (a \cdot x) \bmod p$ wohldefiniert.",
          r"$f$ ist injektiv: Aus $f(x) = f(y)$ und $x \le y$ folgt $p \mid a \cdot (y - x)$, also $p \mid y - x$, und wegen $y - x < p$ ist $x = y$.",
          r"Damit ist $f$ eine Permutation von $\{1, \ldots, p-1\}$, und es gilt $\prod_{x=1}^{p-1} ((a x) \bmod p) = \prod_{x=1}^{p-1} x$.",
          r"Mit Satz 2.44 folgt $(p-1)! \bmod p = (a^{p-1} \cdot (p-1)!) \bmod p$, also $p \mid (p-1)! \cdot (a^{p-1} - 1)$.",
          r"Keiner der Faktoren $1, \ldots, p-1$ ist durch $p$ teilbar, also $p \nmid (p-1)!$ (Satz 2.66). Eine weitere Anwendung von Satz 2.66 liefert $p \mid a^{p-1} - 1$, das heißt $a^{p-1} \bmod p = 1$. $\square$"],
         r"Die Multiplikation mit $a$ vertauscht nur die Zahlen $1, \ldots, p-1$. Die beiden Produkte stimmen überein, und man kann durch $(p-1)!$ teilen, weil $p$ ihn nicht teilt.",
         ablenker=[r"Für $p = 6$ und $a = 5$ stimmt die Aussage auch, also braucht man $p$ nicht prim.",
                   r"Wir testen alle $a < p$ für $p = 7$. Es stimmt jedes Mal, also stimmt es immer."],
         tipps=["Zuerst muss gezeigt werden, dass $f$ auf $\\{1, \\ldots, p-1\\}$ überhaupt abbildet.", "Aus Injektivität folgt hier Bijektivität (endliche Menge).",
                "Am Ende wird zweimal Satz 2.66 benutzt."])

# ── Seite 7: Verschlüsseln ───────────────────────────────────────────────
k.erklaerung("Verschlüsseln von Hand (Beispiel 2.69, Teil 1)", r"""
## $f(m) = m^e \bmod n$ mit $n = 55$, $e = 3$

Die Nachricht ist $m = 12$. Das Skript rechnet $12^3 \bmod 55$ mit Satz 2.44:

Du multiplizierst schrittweise und nimmst nach jedem Schritt den Rest. So bleiben alle Zahlen kleiner als $n^2$.

:::rechnung $12^3 \bmod 55$
12 \cdot 12 = 144 = 2 \cdot 55 + 34 || $12^2 \bmod 55 = 34$
34 \cdot 12 = 408 = 7 \cdot 55 + 23 || $12^3 \bmod 55 = (34 \cdot 12) \bmod 55 = 23$
12^3 = 1728 = 31 \cdot 55 + 23 || Kontrolle ohne Reste: Rest $23$
:::

Die verschlüsselte Zahl ist $c = 23$. Man sieht ihr $m$ nicht an. Rückwärts, ohne $d$, kennst du nur $c^{1/3}$ modulo $55$.

:::alt Als Uhr mit 55 Plätzen
Du multiplizierst auf einer Uhr mit $55$ Plätzen. Nach jedem Mal Multiplizieren landest du wieder auf einem Platz zwischen $0$ und $54$. Nach drei Multiplikationen mit $12$ stehst du auf Platz $23$.
:::
""")

k.zahl(r"Verschlüssele $m = 7$ mit dem öffentlichen Schlüssel $(n, e) = (55, 3)$: Berechne $7^3 \bmod 55$.", 13,
       r"$7^2 = 49$, $49 \cdot 7 = 343 = 6 \cdot 55 + 13$. Also $c = 13$.",
       tipps=[r"Berechne zuerst $7^3 = 343$.", r"Dividiere $343$ durch $55$ mit Rest.", r"$6 \cdot 55 = 330$"],
       rechenweg=r"""
:::rechnung
7 \cdot 7 = 49 = 0 \cdot 55 + 49 || $7^2 \bmod 55 = 49$
49 \cdot 7 = 343 = 6 \cdot 55 + 13 || $7^3 \bmod 55 = 13$
:::
""",
       typische_fehler=[(343, r"Das ist $7^3$ selbst. Es fehlt der Rest bei Division durch $55$."),
                        (21, r"Du hast $7 \cdot 3$ gerechnet. $m^e$ ist eine **Potenz**, kein Produkt."),
                        (49, r"Das ist $7^2 \bmod 55$. Es fehlt noch eine Multiplikation mit $7$.")])

# ── Seite 8: Entschlüsseln ───────────────────────────────────────────────
k.erklaerung("Entschlüsseln von Hand (Beispiel 2.69, Teil 2)", r"""
## $g(c) = c^d \bmod n$ mit $d = 27$

Der Exponent $27$ ist groß. Du berechnest nur kleine Potenzen von $c = 23$ modulo $55$ und suchst, wann die $1$ erscheint:

:::rechnung Potenzen von $23$ modulo $55$
23 \cdot 23 = 529 = 9 \cdot 55 + 34 || $23^2 \bmod 55 = 34$
34 \cdot 23 = 782 = 14 \cdot 55 + 12 || $23^3 \bmod 55 = 12$
12 \cdot 23 = 276 = 5 \cdot 55 + 1 || $23^4 \bmod 55 = 1$
27 = 4 \cdot 6 + 3 || also $23^{27} = (23^4)^6 \cdot 23^3$
1 \cdot 12 = 12 || $\equiv 1^6 \cdot 12 = 12$: das ist die Originalnachricht $m = 12$ ✓
:::

Die Potenzregel (Satz 2.52) und die Produktregel (Satz 2.44) reichen. Der Rest $1$ bei $23^4$ spart alle weiteren Schritte.

:::alt Mit einem Zahnrad
Nach vier Schritten steht das Zahnrad wieder auf $1$. Du musst $27$ Schritte nicht gehen, sondern nur die $27 \bmod 4 = 3$ überzähligen.
:::
""")

k.luecke(r"Entschlüsselung im Beispiel 2.69: Es ist $23^4 \bmod 55 = 1$ und $23^3 \bmod 55 = 12$. Fülle die Lücken.",
         r"23^{27} \bmod 55 = \left( (23^4)^6 \cdot 23^3 \right) \bmod 55 = (\luecke \cdot \luecke) \bmod 55 = \luecke",
         [[1], [12], [12]],
         r"$(23^4 \bmod 55)^6 = 1^6 = 1$. Mit $23^3 \bmod 55 = 12$ ist das Produkt $1 \cdot 12 = 12$, die ursprüngliche Nachricht.",
         tipps=[r"Ersetze $23^4$ durch seinen Rest.", r"$1^6 = 1$", r"$1 \cdot 12$"],
         rechenweg=r"""
:::rechnung
1^6 = 1 || $(23^4 \bmod 55)^6$ nach Satz 2.52
1 \cdot 12 = 12 || Produkt der Reste, bereits kleiner als $55$
:::
""",
         typische_fehler=[([23, 12, 12], r"$23^4 \bmod 55$ ist $1$, nicht $23$. Die Potenzen von $23$ sind $23, 34, 12, 1$."),
                          ([1, 12, 1], r"Das Produkt $1 \cdot 12$ ist $12$, nicht $1$.")])

# ── Seite 9: Satz 2.68 ───────────────────────────────────────────────────
k.erklaerung("Warum RSA funktioniert (Satz 2.68)", r"""
## $g(f(m)) = m$ für alle $m < n$

**Satz 2.68.** Mit den Bezeichnungen von oben gilt $g(f(m)) = m$ für alle $m \in \mathbb{N}$ mit $m < n$.

Idee: $g(f(m)) = m^{ed} \bmod n$. Wegen $ed \bmod t = 1$ ist $ed = 1 + k(p-1)(q-1)$, also $m^{ed} = m \cdot (m^{p-1})^{k(q-1)}$. Fermat liefert $m^{ed} \equiv m$ modulo $p$ (und ebenso modulo $q$). Beide Primzahlen teilen $m^{ed} - m$, also auch $pq = n$.

:::rechnung Das Beispiel $m = 12$, $n = 55$, $ed = 81$
81 = 1 + 2 \cdot 40 || $ed = 1 + k(p-1)(q-1)$ mit $k = 2$
12 \bmod 5 = 2 \text{ und } 12^{81} \bmod 5 = 2 || modulo $p = 5$ stimmen $m^{ed}$ und $m$ überein (Fermat: $2^4 \equiv 1$)
12 \bmod 11 = 1 \text{ und } 12^{81} \bmod 11 = 1 || modulo $q = 11$ ebenso
12^{81} \bmod 55 = 12 || beide Primzahlen teilen die Differenz, also auch $55$; und $12 < 55$
:::

:::achtung Warum $m < n$?
Ist $m \ge n$, bekommst du nur $m \bmod n$ zurück: $g(f(60)) = 5$ für $n = 55$. Lange Nachrichten zerlegt man deshalb in Stücke kleiner als $n$.
:::

:::alt Mit zwei Zählern
Du zählst auf einer $5$er-Uhr und auf einer $11$er-Uhr gleichzeitig. Zeigen beide Uhren dieselbe Zeit wie vorher, ist auch die $55$er-Uhr wieder am selben Punkt, weil $5$ und $11$ verschieden prim sind.
:::
""")

k.ordnen(r"Ordne den Beweis von Satz 2.68 (Korrektheit von RSA): $g(f(m)) = m$ für alle $m < n$.",
         [r"Es gilt $g(f(m)) = (m^e \bmod n)^d \bmod n = m^{ed} \bmod n$ (Satz 2.52).",
          r"Wegen $ed \bmod t = 1$ gibt es $k$ mit $ed = 1 + k(p-1)(q-1)$, also $m^{ed} = m \cdot (m^{p-1})^{k(q-1)}$.",
          r"Ist $p \mid m$, so folgt $m^{ed} \bmod p = 0 = m \bmod p$. Andernfalls ist $m^{p-1} \bmod p = 1$ (Satz 2.67), und mit Satz 2.52 und 2.44 folgt $m^{ed} \bmod p = m \bmod p$.",
          r"Dasselbe Argument mit $q$ liefert $m^{ed} \bmod q = m \bmod q$.",
          r"Also teilen $p$ und $q$ die Zahl $x := m^{ed} - m$. Wegen $q \nmid p$ und Satz 2.66 folgt $pq \mid x$, das heißt $m^{ed}$ und $m$ haben denselben Rest modulo $n$.",
          r"Wegen $m < n$ ist $m \bmod n = m$, also $g(f(m)) = m$. $\square$"],
         r"Der Beweis zeigt erst $m^{ed} \equiv m$ modulo $p$ und modulo $q$ getrennt (mit Fermat) und setzt beides mit Satz 2.66 zu $n = pq$ zusammen.",
         ablenker=[r"Wegen $e \cdot d = 1$ ist $m^{ed} = m$.",
                   r"Nach Satz 2.67 gilt $m^{n-1} \bmod n = 1$."],
         tipps=["Der Beweis beginnt mit dem Zusammenfassen von $g(f(m))$ zu einer Potenz.", "Fermat wird einmal für $p$ und einmal für $q$ angewendet.",
                r"Die Ablenker verwechseln $ed \bmod t = 1$ mit $ed = 1$ und wenden Fermat auf die nicht-prime Zahl $n$ an."])

k.mc(r"Warum verlangt Satz 2.68 die Bedingung $m < n$?",
     [r"Für $m \ge n$ liefert $g(f(m))$ nur $m \bmod n$, nicht $m$ selbst",
      r"Weil sonst $m^e$ nicht berechenbar wäre",
      r"Weil sonst $p \mid m$ gelten müsste",
      r"Weil Fermat nur für $m < n$ gilt"],
     r"Es gilt immer $g(f(m)) = m \bmod n$. Nur für $m < n$ ist $m \bmod n = m$. Für $n = 55$ liefert $m = 60$ als Ergebnis $5$.",
     tipps=[r"Berechne $g(f(60))$ für $n = 55$.", r"Was ist $60 \bmod 55$?", r"Entschlüsselung liefert immer einen Rest modulo $n$."],
     fehler={r"Weil sonst $m^e$ nicht berechenbar wäre": r"$m^e \bmod n$ ist für jedes $m$ berechenbar. Die Schwierigkeit liegt beim Zurückrechnen.",
             r"Weil sonst $p \mid m$ gelten müsste": r"Für $m < n$ kann $p \mid m$ sehr wohl gelten (etwa $m = 10$ und $p = 5$). Der Beweis behandelt diesen Fall extra.",
             r"Weil Fermat nur für $m < n$ gilt": r"Fermat gilt für jede Zahl $a$ mit $p \nmid a$, unabhängig von $n$."})

# ── Seite 10: Grenzen ────────────────────────────────────────────────────
k.erklaerung("Den geheimen Schlüssel finden und Sicherheit", r"""
## Wo die Schwierigkeit liegt

Zum Schlüssel $(n, e)$ gehört $d$ mit $e \cdot d \bmod t = 1$. Das findest du mit dem erweiterten euklidischen Algorithmus (ergänzend zum Skript, das nur „effizient möglich“ sagt): Er liefert Zahlen $s, u$ mit $e \cdot s + t \cdot u = 1$, also $d = s \bmod t$.

:::visual euklid
{"a": 40, "b": 3, "erweitert": true,
 "unterschrift": "Erweiterter euklidischer Algorithmus für $t = 40$ und $e = 3$: Rückwärts eingesetzt ergibt sich $3 \\cdot 27 - 2 \\cdot 40 = 1$, also $d = 27$."}
:::

:::rechnung Suche von $d$ ohne Algorithmus (kleine Zahlen)
1 \cdot 40 + 1 = 41 || $k = 1$: $41$ ist nicht durch $3$ teilbar (Rest $2$)
2 \cdot 40 + 1 = 81 = 3 \cdot 27 || $k = 2$: $81$ ist durch $3$ teilbar, also $d = 27$
:::

**Sicherheit.** Wer $n = 55$ sieht, zerlegt es sofort in $5 \cdot 11$. Echte $n$ haben Hunderte Stellen, und für die kennt man keinen effizienten Faktorisierungsalgorithmus. Ob es einen gibt, ist ein offenes Problem der Komplexitätstheorie.

:::alt Wie Zahlen knacken
Das Produkt zweier Primzahlen mit je 300 Stellen zu bilden dauert Millisekunden. Aus dem Ergebnis die beiden Faktoren zu bestimmen dauert mit allen bekannten Verfahren länger als das Alter des Universums.
:::
""")

k.mehrfach("Welche Aussagen zum RSA-Verfahren (Abschnitt 2.9) stimmen?",
           [r"Zum Entschlüsseln braucht man den geheimen Exponenten $d$",
            r"Wer $n$ in $p \cdot q$ zerlegen kann, kann $t$ und damit $d$ berechnen",
            r"$e \cdot d \bmod t = 1$ ist die Bedingung an die beiden Exponenten"],
           [r"Der öffentliche Schlüssel enthält $d$",
            r"Das Verfahren funktioniert für beliebige (nicht prime) Faktoren $p$ und $q$"],
           r"$(n, e)$ ist öffentlich, $d$ geheim. Die Korrektheit (Satz 2.68) benutzt Fermat und das Primzahllemma, also müssen $p$ und $q$ verschiedene Primzahlen sein.",
           tipps=["Was wird veröffentlicht, was bleibt geheim?", "Wo wird im Beweis von Satz 2.68 benutzt, dass $p$ und $q$ prim sind?", r"Fermat gilt nur für Primzahlen."],
           fehler={r"Der öffentliche Schlüssel enthält $d$": r"Der öffentliche Schlüssel ist $(n, e)$. $d$ bleibt geheim, sonst könnte jeder entschlüsseln.",
                   r"Das Verfahren funktioniert für beliebige (nicht prime) Faktoren $p$ und $q$": r"Der Beweis von Satz 2.68 braucht Fermat und das Primzahllemma, beide verlangen Primzahlen."})


# ── Praxis ────────────────────────────────────────────────────────────────
def rechnung(zeilen):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in zeilen) + "\n:::"


def _schluessel(rng, primzahlen, e_liste):
    while True:
        p, q = rng.sample(primzahlen, 2)
        p, q = min(p, q), max(p, q)
        n, t = p * q, (p - 1) * (q - 1)
        e = rng.choice(e_liste)
        if e < t and gcd(e, t) == 1:
            d = pow(e, -1, t)
            if d != e and d > 1:
                return p, q, n, t, e, d


def rsa_schluessel_erzeugen(rng):
    p, q, n, t, e, d = _schluessel(rng, [3, 5, 7, 11, 13], [3, 5, 7, 9, 11])
    k_ = (e * d - 1) // t
    assert e * d == k_ * t + 1
    loesung = [[n], [t], [d]]
    fehler = [([n, n - 1, d], "$t$ ist $(p-1)(q-1)$, nicht $n - 1$. Nur für **prime** $n$ wäre $n - 1$ passend."),
              ([p + q, t, d], "$n$ ist das **Produkt** $p \\cdot q$, nicht die Summe."),
              ([n, t, e], f"$d$ ist das Inverse von $e$ modulo $t$: Gesucht ist $d$ mit $e \\cdot d \\bmod {t} = 1$, nicht $e$ selbst."),
              ([n, t, t - e], "$t - e$ ist nur in Sonderfällen das Inverse. Prüfe $e \\cdot d \\bmod t = 1$.")]
    return {
        "frage": f"RSA mit den Primzahlen $p = {p}$, $q = {q}$ und $e = {e}$: Berechne $n$, $t$ und den geheimen Schlüssel $d$ mit $1 \\le d < t$ und $(e \\cdot d) \\bmod t = 1$.",
        "formel": "n = \\luecke, \\quad t = \\luecke, \\quad d = \\luecke",
        "antworten": loesung,
        "tipps": [f"$n = p \\cdot q$ und $t = (p-1)(q-1)$.", f"Suche $k$ mit $e \\cdot d = k \\cdot t + 1$, also $d = \\frac{{k \\cdot {t} + 1}}{{{e}}}$: probiere $k = 1, 2, \\ldots$ bis es aufgeht.",
                  f"Für $k = {k_}$ ist ${k_} \\cdot {t} + 1 = {k_ * t + 1} = {e} \\cdot {d}$."],
        "rechenweg": rechnung([(f"{p} \\cdot {q} = {n}", "$n = p \\cdot q$"),
                               (f"({p} - 1)({q} - 1) = {(p - 1) * (q - 1)}", "$t = (p-1)(q-1)$"),
                               (f"{e} \\cdot {d} = {e * d} = {k_} \\cdot {t} + 1", f"Probe: $e \\cdot d \\bmod t = 1$ mit $d = {d}$")]),
        "erklaerung": "$d$ ist das Inverse von $e$ modulo $t$. Man findet es, indem man $k \\cdot t + 1$ für $k = 1, 2, \\ldots$ durch $e$ teilt, bis es aufgeht (oder mit dem erweiterten euklidischen Algorithmus).",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


def rsa_verschluesseln(rng):
    p, q, n, t, e, d = _schluessel(rng, [5, 7, 11, 13], [3, 5])
    while True:
        m = rng.randint(2, n - 2)
        c = pow(m, e, n)
        if c != m and c > 1:
            break
    zeilen, v = [], m
    for j in range(2, e + 1):
        neu = v * m % n
        zeilen.append((f"{v} \\cdot {m} = {v * m} = {v * m // n} \\cdot {n} + {neu}", f"$m^{{{j}}} \\bmod n$: nach jedem Schritt den Rest nehmen"))
        v = neu
    assert v == c
    fehler = [(m ** e, f"Das ist $m^e = {m ** e}$ selbst. Es fehlt der Rest bei Division durch $n = {n}$."),
              (m * e % n, f"Du hast ${m} \\cdot {e}$ gerechnet. $m^e$ ist eine **Potenz**."),
              (pow(m, d, n) if pow(m, d, n) != c else (c + 1) % n, "Du hast mit dem geheimen Exponenten $d$ gerechnet. Verschlüsseln geht mit dem öffentlichen $e$.")]
    return {
        "frage": f"Der öffentliche Schlüssel ist $(n, e) = ({n}, {e})$. Verschlüssele die Nachricht $m = {m}$, also $f(m) = m^e \\bmod n$.",
        "loesung": c,
        "tipps": [f"Berechne ${m}^{{{e}}}$ schrittweise und nimm nach jedem Schritt den Rest modulo ${n}$.", f"${m} \\cdot {m} = {m * m}$, und davon der Rest modulo ${n}$.",
                  f"Das Ergebnis liegt zwischen $0$ und ${n - 1}$."],
        "rechenweg": rechnung(zeilen),
        "erklaerung": "Verschlüsseln: $c = m^e \\bmod n$. Mit Satz 2.44 darfst du nach jeder Multiplikation den Rest nehmen.",
        "typische_fehler": ohne_gleiche(c, fehler),
    }


def rsa_entschluesseln(rng):
    while True:
        p, q, n, t, e, d = _schluessel(rng, [5, 7, 11], [3, 5, 7])
        if 8 <= d <= 59:
            break
    while True:
        m = rng.randint(2, n - 2)
        c = pow(m, e, n)
        if c != m and c > 1:
            break
    zeilen, wert = potenz_kette(c, d, n)
    assert wert == m
    fehler = [(c, "Das ist die Chiffre selbst. Es fehlt das Potenzieren mit $d$."),
              (pow(c, e, n) if pow(c, e, n) != m else (m + 1) % n, "Du hast mit dem öffentlichen Exponenten $e$ statt mit dem geheimen $d$ potenziert."),
              (c * d % n if c * d % n != m else (m + 1) % n, f"Du hast ${c} \\cdot {d}$ gerechnet. Entschlüsseln heißt potenzieren: $c^d \\bmod n$.")]
    return {
        "frage": f"Zum RSA-Schlüssel $(n, e) = ({n}, {e})$ gehört der geheime Schlüssel $d = {d}$. Entschlüssele $c = {c}$, also $g(c) = c^d \\bmod n$.",
        "loesung": m,
        "tipps": [f"Zerlege den Exponenten ${d}$ in Summen von Zweierpotenzen: ${' + '.join(str(2 ** i) for i, b in enumerate(bin(d)[2:][::-1]) if b == '1')}$.",
                  f"Berechne ${c}^2, {c}^4, {c}^8, \\ldots$ jeweils modulo ${n}$, indem du jede Zahl quadrierst und den Rest nimmst.",
                  "Multipliziere die benötigten Potenzen und nimm nach jedem Produkt den Rest. Das Ergebnis ist die Originalnachricht, kleiner als $n$."],
        "rechenweg": rechnung(zeilen + [(f"{m} < {n}", "Das Ergebnis ist die Originalnachricht (Satz 2.68)")]),
        "erklaerung": "Entschlüsseln: $m = c^d \\bmod n$. Quadriere schrittweise und multipliziere die nötigen Potenzen, immer mit Rest.",
        "typische_fehler": ohne_gleiche(m, fehler),
    }


def fermat_anwenden(rng):
    p = rng.choice([7, 11, 13, 17, 19, 23])
    a = rng.randint(2, p - 1)
    j, r = rng.randint(2, 9), rng.randint(2, 4)
    kk = j * (p - 1) + r
    loesung = pow(a, kk, p)
    zeilen = [(f"{j} \\cdot {p - 1} + {r} = {kk}", f"Exponent zerlegen: $k = j \\cdot (p-1) + r$ mit $j = {j}$, $r = {r}$"),
              (f"{a}^{{{kk}}} = ({a}^{{{p - 1}}})^{{{j}}} \\cdot {a}^{{{r}}}", f"Potenzgesetz; nach Fermat ist ${a}^{{{p - 1}}} \\bmod {p} = 1$, also bleibt $1^{{{j}}} \\cdot {a}^{{{r}}}$")]
    v = a
    for e in range(2, r + 1):
        neu = v * a % p
        zeilen.append((f"{v} \\cdot {a} = {v * a} = {v * a // p} \\cdot {p} + {neu}", f"${a}^{{{e}}} \\bmod {p}$"))
        v = neu
    assert v == loesung
    fehler = [(pow(a, kk % p, p), f"Du hast den Exponenten modulo ${p}$ reduziert. Fermat reduziert ihn modulo $p - 1 = {p - 1}$."),
              (1, f"Das wäre ${a}^{{{p - 1}}} \\bmod {p}$. Der Exponent ${kk}$ ist aber nicht ein Vielfaches von ${p - 1}$: Es bleibt noch ${a}^{{{r}}}$ übrig."),
              (a, f"Es bleibt der Rest ${a}^{{{r}}}$ mit $r = {r}$, nicht nur ${a}^1$.")]
    return {
        "frage": f"Berechne ${a}^{{{kk}}} \\bmod {p}$ ohne Taschenrechner. Es ist ${p}$ eine Primzahl.",
        "loesung": loesung,
        "tipps": [f"Schreibe ${kk} = j \\cdot {p - 1} + r$ mit $r < {p - 1}$ (Division mit Rest).", f"Nach Fermat ist ${a}^{{{p - 1}}} \\bmod {p} = 1$, also fallen die ersten Faktoren weg.",
                  f"Es bleibt nur ${a}^{{{r}}} \\bmod {p}$ zu berechnen."],
        "rechenweg": rechnung(zeilen),
        "erklaerung": "Nach dem kleinen Satz von Fermat kann man den Exponenten modulo $p - 1$ reduzieren, sofern $p \\nmid a$.",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


def primzahlen_erkennen(rng):
    while True:
        zahlen = sorted(rng.sample(range(20, 100), 6))
        pr = [z for z in zahlen if ist_prim(z)]
        if 1 <= len(pr) <= 4:
            break
    kleinster = {z: next(t for t in range(2, z) if z % t == 0) for z in zahlen if not ist_prim(z)}
    zeilen = [(f"{z} = {kleinster[z]} \\cdot {z // kleinster[z]}", f"${kleinster[z]}$ ist ein Teiler: ${z}$ ist nicht prim") for z in zahlen if not ist_prim(z)]
    zeilen += [(f"\\text{{{z} hat keinen Teiler zwischen 2 und {z - 1}}}", f"${z}$ ist prim") for z in zahlen if ist_prim(z)]
    return {
        "frage": "Welche der folgenden Zahlen sind Primzahlen (Definition 2.65)?",
        "richtig": [f"${z}$" for z in pr], "falsch": [f"${z}$" for z in zahlen if not ist_prim(z)],
        "fehler": {f"${z}$": f"${z} = {kleinster[z]} \\cdot {z // kleinster[z]}$: Der Teiler ${kleinster[z]}$ zeigt, dass ${z}$ keine Primzahl ist." for z in kleinster},
        "tipps": ["Teste kleine Teiler: $2$, $3$, $5$, $7$.", "Quersumme durch $3$ teilbar? Endziffer $0, 5$ oder gerade?", "Ist $z$ nicht prim, hat es einen Teiler $\\le \\sqrt{z}$, also $\\le 9$ für $z < 100$."],
        "rechenweg": rechnung(zeilen),
        "erklaerung": "Eine Primzahl hat keine Teiler außer $1$ und sich selbst. Für $z < 100$ genügt es, die Teiler $2, 3, 5, 7$ zu testen.",
    }


k.praxis()

k.generator(rsa_schluessel_erzeugen, typ="luecke", titel="RSA-Schlüssel erzeugen")
k.generator(rsa_verschluesseln, typ="zahl", titel="Mit RSA verschlüsseln")
k.generator(rsa_entschluesseln, typ="zahl", titel="Mit RSA entschlüsseln")
k.generator(fermat_anwenden, typ="zahl", titel="Kleiner Satz von Fermat anwenden")
k.generator(primzahlen_erkennen, typ="mehrfach", titel="Primzahlen erkennen")

k.rechenweg_aufgabe(r"""
## Quiz-Stil: RSA mit $p = 7$ und $q = 13$

Alice wählt $p = 7$, $q = 13$ und $e = 5$. Bob will die Nachricht $m = 10$ verschlüsselt schicken.
""",
    [{"typ": "zahl", "frage": r"Berechne $t = (p-1)(q-1)$.", "loesung": 72,
      "tipps": [r"$(7 - 1)(13 - 1)$", r"$6 \cdot 12$"],
      "rechenweg": r"$t = 6 \cdot 12 = 72$.", "erklaerung": r"Es ist $n = 91$ und $t = 72$.",
      "typische_fehler": [(90, r"$n - 1 = 90$ wäre $t$ nur für eine Primzahl $n$.")]},
     {"typ": "zahl", "frage": r"Bestimme den geheimen Schlüssel $d$ mit $1 \le d < 72$ und $(5 \cdot d) \bmod 72 = 1$.", "loesung": 29,
      "tipps": [r"Suche $k$ mit $5 \cdot d = k \cdot 72 + 1$.", r"$k = 2$: $2 \cdot 72 + 1 = 145 = 5 \cdot 29$"],
      "rechenweg": r"$5 \cdot 29 = 145 = 2 \cdot 72 + 1$.", "erklaerung": r"$d = 29$, denn $145 \bmod 72 = 1$.",
      "typische_fehler": [(14, r"$5 \cdot 14 = 70 = 0 \cdot 72 + 70$: Der Rest ist $70$, nicht $1$."),
                          (67, r"$72 - 5 = 67$ gilt nur in Sonderfällen als Inverses. Prüfe $5 \cdot 67 = 335 = 4 \cdot 72 + 47$.")]},
     {"typ": "zahl", "frage": r"Bob verschlüsselt $m = 10$ mit $(n, e) = (91, 5)$. Berechne $c = 10^5 \bmod 91$.", "loesung": 82,
      "tipps": [r"$10^2 = 100 = 1 \cdot 91 + 9$.", r"$10^3 \equiv 90$, dann $10^4 \equiv 90 \cdot 10 \bmod 91$.", r"$10^5 = 100000$, davon der Rest modulo $91$."],
      "rechenweg": r"$10^2 \equiv 9$, $10^3 \equiv 90$, $10^4 \equiv 900 = 9 \cdot 91 + 81 \equiv 81$, $10^5 \equiv 810 = 8 \cdot 91 + 82 \equiv 82$.",
      "erklaerung": r"Kontrolle: $100000 = 1098 \cdot 91 + 82$.",
      "typische_fehler": [(100000, r"Das ist $10^5$ selbst. Es fehlt der Rest modulo $91$."),
                          (50, r"Das ist $10 \cdot 5$. Du musst potenzieren.")]}],
    r"$n = 91$, $t = 72$, $d = 29$ und die Chiffre ist $c = 82$.",
    uebungsblatt=True,
    tipps=["Berechne zuerst $n$ und $t$.", r"Für $d$ probierst du $k \cdot 72 + 1$ für $k = 1, 2, \ldots$ und teilst durch $5$.", "Nach jeder Multiplikation den Rest modulo $91$ nehmen."],
    rechenweg=r"""
:::rechnung
7 \cdot 13 = 91 || $n$
6 \cdot 12 = 72 || $t$
5 \cdot 29 = 145 = 2 \cdot 72 + 1 || $d = 29$
10^5 = 100000 = 1098 \cdot 91 + 82 || $c = 82$
:::
""")

_Z77, _D77 = potenz_kette(51, 43, 77)
k.papier(r"""
## Übungsblatt-Stil: RSA und Beweis

1. Gegeben sind $p = 7$, $q = 11$ und $e = 7$. Bestimmen Sie $n$, $t$ und $d$. Verschlüsseln Sie $m = 2$ und entschlüsseln Sie das Ergebnis wieder.
2. Beweisen Sie den Teil von Satz 2.68 für den Fall $p \nmid m$ und $q \nmid m$: Es gilt $m^{ed} \bmod n = m \bmod n$ für $ed = 1 + k(p-1)(q-1)$.
""",
    r"""
**1.** $n = 7 \cdot 11 = 77$, $t = 6 \cdot 10 = 60$. Für $d$: $7 \cdot d = k \cdot 60 + 1$. Mit $k = 5$ ist $301 = 7 \cdot 43$, also $d = 43$ und $7 \cdot 43 = 301 = 5 \cdot 60 + 1$.
**Verschlüsseln:** $2^7 = 128 = 1 \cdot 77 + 51$, also $c = 51$.
**Entschlüsseln:** $51^{43} \bmod 77$ mit $43 = 1 + 2 + 8 + 32$. Quadrieren und Rest:
§KETTE§
Das Ergebnis ist $2 = m$ (Satz 2.68).

**2.** Nach Fermat gilt $m^{p-1} \bmod p = 1$ und $m^{q-1} \bmod q = 1$. Mit Satz 2.52 folgt $(m^{p-1})^{k(q-1)} \bmod p = 1$, also (Satz 2.44)
$m^{ed} \bmod p = (m \cdot (m^{p-1})^{k(q-1)}) \bmod p = m \bmod p$. Ebenso $m^{ed} \bmod q = m \bmod q$.
Daher teilen $p$ und $q$ die Zahl $x := m^{ed} - m$ (nach Beobachtung 2.43). Aus $p \mid x$ folgt $x = p \cdot l$. Weil $q \mid p \cdot l$ und $q \nmid p$ (verschiedene Primzahlen), liefert Satz 2.66 $q \mid l$, also $pq \mid x$.
Damit haben $m^{ed}$ und $m$ denselben Rest modulo $n = pq$. $\square$
""".replace("§KETTE§", "\n".join(f"- ${t}$" for t, _ in _Z77)),
    ["Bei 1.: $n = 77$ und $t = 60$ richtig berechnet",
     "Bei 1.: $d = 43$ mit der Probe $e \\cdot d \\bmod t = 1$ bestimmt",
     "Bei 1.: $c = 51$ berechnet und mit Rest nach jedem Schritt entschlüsselt (Ergebnis $m = 2$)",
     "Bei 2.: Fermat für $p$ und $q$ getrennt angewendet und mit Satz 2.52 auf $m^{ed}$ übertragen",
     "Bei 2.: Aus $p \\mid x$ und $q \\mid x$ mit Satz 2.66 auf $pq \\mid x$ geschlossen (dabei $p \\neq q$ benutzt)"],
    "Bei kleinen Zahlen darfst du alles von Hand nachrechnen. Der allgemeine Beweis zeigt erst die Gleichheit der Reste modulo $p$ und modulo $q$ und setzt sie dann zusammen.",
    uebungsblatt=True,
    tipps=["Für $d$: Teile $k \\cdot 60 + 1$ für $k = 1, 2, \\ldots$ durch $7$, bis es aufgeht.", "Bei der Entschlüsselung: Quadriere $51$ mehrmals modulo $77$ und multipliziere die Potenzen, die zu $43 = 32 + 8 + 2 + 1$ gehören.",
           "Bei 2.: Wo wird $p \\neq q$ gebraucht? Beim Schluss von $q \\mid p \\cdot l$ auf $q \\mid l$."])

k.zusammenfassung(r"""
## Kryptographie: RSA (Skript Abschn. 2.9)

- **Primzahl** (Def. 2.65): $p > 1$ ohne Teiler außer $1$ und $p$. RSA: $p \neq q$ prim, $n := pq$, $t := (p-1)(q-1)$.
- **Primzahllemma** (Satz 2.66): $p$ prim, $p \mid ab \Rightarrow p \mid a \lor p \mid b$. Beweis über $M = \{x \geq 1 \mid p \mid xa\}$ und sein Minimum.
- **Kleiner Satz von Fermat** (Satz 2.67): $p$ prim, $p \nmid a \Rightarrow a^{p-1} \bmod p = 1$. Beweis: $x \mapsto ax \bmod p$ ist eine Permutation von $1, \ldots, p-1$.
- **RSA:** $e \cdot d \bmod t = 1$; öffentlich $(n, e)$, geheim $d$. $f(m) = m^e \bmod n$ (verschlüsseln), $g(c) = c^d \bmod n$ (entschlüsseln).
- **Korrektheit** (Satz 2.68): $g(f(m)) = m$ für alle $m < n$. Beweis: $m^{ed} \equiv m$ modulo $p$ und modulo $q$ (Fermat), dann $pq \mid m^{ed} - m$ (Satz 2.66).
- **Beispiel 2.69:** $p = 5$, $q = 11$, $n = 55$, $t = 40$, $e = 3$, $d = 27$, $m = 12 \mapsto c = 23 \mapsto 12$. Potenzen von $23$ mod $55$: $34, 12, 1$.

!! Nach jeder Multiplikation sofort den Rest nehmen (Satz 2.44 und Satz 2.52). Große Primfaktoren machen $d$ nicht aus $n$ erschließbar.
""")
