# -*- coding: utf-8 -*-
"""Vorkurs 9: Vollständige Induktion – IA, IV, IS, ISch; Summenformeln, Teilbarkeit, Startwert, Beweisschritte ordnen."""
import math
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche


def _S(f, a, b):
    return sum((F(f(i)) for i in range(a, b + 1)), F(0))


# Summenformeln für Generatoren und Texte:
# (f(k), F(n), f(k) LaTeX, F(n) LaTeX, f(n+1) LaTeX, f(n+1) Text, F(n+1) LaTeX, F(n+1) Text)
_FORMELN = [
    (lambda i: i, lambda n: F(n * (n + 1), 2), "k", r"\frac{n(n+1)}{2}", "(n + 1)", "n+1",
     r"\frac{(n+1)(n+2)}{2}", "(n+1)(n+2)/2"),
    (lambda i: 2 * i - 1, lambda n: n * n, "(2k - 1)", "n^2", "(2n + 1)", "2n+1", "(n+1)^2", "(n+1)^2"),
    (lambda i: i * i, lambda n: F(n * (n + 1) * (2 * n + 1), 6), "k^2", r"\frac{n(n+1)(2n+1)}{6}", "(n + 1)^2",
     "(n+1)^2", r"\frac{(n+1)(n+2)(2n+3)}{6}", "(n+1)(n+2)(2n+3)/6"),
    (lambda i: i ** 3, lambda n: F(n * (n + 1), 2) ** 2, "k^3", r"\left(\frac{n(n+1)}{2}\right)^2", "(n + 1)^3",
     "(n+1)^3", r"\left(\frac{(n+1)(n+2)}{2}\right)^2", "((n+1)(n+2)/2)^2"),
    (lambda i: 2 ** (i - 1), lambda n: 2 ** n - 1, "2^{k-1}", "2^n - 1", "2^n", "2^n", "2^{n+1} - 1", "2^(n+1)-1"),
    (lambda i: i * (i + 1), lambda n: F(n * (n + 1) * (n + 2), 3), "k(k + 1)", r"\frac{n(n+1)(n+2)}{3}",
     "(n + 1)(n + 2)", "(n+1)(n+2)", r"\frac{(n+1)(n+2)(n+3)}{3}", "(n+1)(n+2)(n+3)/3"),
    (lambda i: F(1, i * (i + 1)), lambda n: F(n, n + 1), r"\frac{1}{k(k+1)}", r"\frac{n}{n+1}",
     r"\frac{1}{(n+1)(n+2)}", "1/((n+1)(n+2))", r"\frac{n+1}{n+2}", "(n+1)/(n+2)"),
    (lambda i: 3 ** i, lambda n: F(3 ** (n + 1) - 3, 2), "3^k", r"\frac{3^{n+1} - 3}{2}", "3^{n+1}", "3^(n+1)",
     r"\frac{3^{n+2} - 3}{2}", "(3^(n+2)-3)/2"),
    (lambda i: 4 * i - 1, lambda n: 2 * n * n + n, "(4k - 1)", "2n^2 + n", "(4n + 3)", "4n+3",
     "2(n+1)^2 + (n+1)", "2(n+1)^2+(n+1)"),
    (lambda i: 2 * i, lambda n: n * (n + 1), "2k", "n(n+1)", "2(n + 1)", "2(n+1)", "(n+1)(n+2)", "(n+1)(n+2)"),
    (lambda i: i * 2 ** i, lambda n: (n - 1) * 2 ** (n + 1) + 2, r"k \cdot 2^k", r"(n-1) \cdot 2^{n+1} + 2",
     r"(n+1) \cdot 2^{n+1}", "(n+1)2^(n+1)", r"n \cdot 2^{n+2} + 2", "n*2^(n+2)+2"),
    (lambda i: F(1, 2 ** i), lambda n: 1 - F(1, 2 ** n), r"\frac{1}{2^k}", r"1 - \frac{1}{2^n}", r"\frac{1}{2^{n+1}}",
     "1/2^(n+1)", r"1 - \frac{1}{2^{n+1}}", "1-1/2^(n+1)"),
]

# Jede Formel wird für viele n nachgeprüft (auch der Schritt F(n) + f(n+1) = F(n+1)).
for _f, _Fn, *_ in _FORMELN:
    for _n in range(1, 60):
        assert _S(_f, 1, _n) == _Fn(_n), _n
        assert _Fn(_n) + _f(_n + 1) == _Fn(_n + 1)
for _n in range(0, 60):
    assert (_n * _n + _n) % 2 == 0 and (_n ** 3 + 2 * _n) % 3 == 0
    assert (_n + 1) ** 2 + (_n + 1) == (_n * _n + _n) + 2 * _n + 2
    assert _S(lambda i: 2 ** i, 0, _n - 1) == 2 ** _n - 1
    if _n >= 4:
        assert math.factorial(_n) >= 2 ** _n
assert math.factorial(3) < 2 ** 3          # Startwert 4 ist nötig
assert (2 * 1 + 1) % 2 == 1                # 2 | 2n + 1 scheitert schon am IA

k = neues_kapitel(
    slug="induktion",
    titel="Vollständige Induktion",
    beschreibung="Aussagen für alle natürlichen Zahlen beweisen: Induktionsanfang, -voraussetzung, -schritt und -schluss",
    teil="vorkurs",
    quelle="MVK 2026, VL 3 und Moodle-Aufgabe „Induktion: Beweisschritte sortieren“",
    icon="🁢")

k.lernziele([
    "Ich kann das Prinzip der vollständigen Induktion mit Induktionsanfang, -voraussetzung, -schritt und -schluss erklären",
    "Ich kann Summenformeln per Induktion beweisen und markiere, wo die IV eingeht",
    "Ich kann Teilbarkeitsaussagen und Ungleichungen per Induktion beweisen, auch mit Startwert $n_0 \\neq 1$",
    "Ich erkenne typische Fehler: IA vergessen, IV „für alle n“, IV gar nicht benutzt",
])

k.warum(r"""
Induktion ist das mathematische Gegenstück zu Schleifen und Rekursion. Eine
**Schleifeninvariante** beweist du genauso: Sie gilt vor dem ersten Durchlauf
(IA), und wenn sie vor einem Durchlauf gilt, dann auch danach (IS). Rekursive
Funktionen wie `fak(n) = n * fak(n - 1)` sind korrekt, weil der Basisfall stimmt
und jeder Aufruf sich auf den kleineren verlassen kann. In Mathe 1 ist ein
Induktionsbeweis fast sicher Teil der Klausur.
""")

# ── 1: Idee ────────────────────────────────────────────────────────────────
k.erklaerung("Die Idee: Dominosteine", r"""
    ## Unendlich viele Fälle in zwei Schritten

    Jede natürliche Zahl $n > 1$ entsteht aus ihrem Vorgänger durch $+1$:
    $2 = 1 + 1$, $3 = 2 + 1$, … Das nutzt die [[vollständige Induktion]].

    :::visual induktion_domino
    {"anzahl": 8, "anfang": 1, "aussage": "$A(n)$: $1 + 2 + \\ldots + n = \\frac{n(n+1)}{2}$",
     "text_anfang": "Der erste Stein fällt: $A(1)$ stimmt.",
     "text_schritt": "Fällt Stein $n$, dann stößt er Stein $n + 1$ um: $A(n) \\Rightarrow A(n+1)$.",
     "unterschrift": "Erst der Anfang, dann der Schritt: Dann fallen alle Steine."}
    :::

    Zwei Dinge reichen, damit **alle** Steine fallen:

    - Der erste Stein fällt.
    - Jeder fallende Stein stößt seinen Nachfolger um.

    :::alt Mit einer Leiter erklärt
    Du kommst auf jede Sprosse einer unendlich hohen Leiter, wenn du auf die
    erste Sprosse kommst und von jeder Sprosse auf die nächste. Du musst nicht
    jede Sprosse einzeln prüfen, nur den Einstieg und das Weitersteigen.
    :::
    """)

# ── 2: Schema ──────────────────────────────────────────────────────────────
k.erklaerung("Das Schema: IA, IV, IS, ISch", r"""
    ## Vier Bausteine

    Sei $A(n)$ für jedes $n \in \mathbb{N}$ eine Aussage.

    1. **[[Induktionsanfang]] (IA):** Prüfe, dass $A(1)$ wahr ist.
    2. **[[Induktionsvoraussetzung]] (IV):** Nimm an, $A(n)$ gilt für ein
       beliebiges, aber festes $n \in \mathbb{N}$.
    3. **[[Induktionsschritt]] (IS), $n \to n + 1$:** Zeige mit der IV, dass
       auch $A(n + 1)$ gilt.
    4. **[[Induktionsschluss]] (ISch):** Nach dem Prinzip der vollständigen
       Induktion gilt $A(n)$ für alle $n \in \mathbb{N}$.

    :::rechnung IA für $A(n)$: $\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$
    \sum_{i=1}^{1} i = 1 || linke Seite für $n = 1$
    \frac{1 \cdot (1 + 1)}{2} = 1 || rechte Seite für $n = 1$, beide gleich ✓
    :::

    :::alt Mit einem Staffellauf erklärt
    Der IA ist der Startschuss: Die erste Läuferin läuft los. Die IV sagt:
    Angenommen, Läuferin $n$ ist angekommen. Der IS zeigt: Dann bekommt
    Läuferin $n + 1$ den Stab. Der ISch: Also kommt jede an.
    :::
    """)

k.zuordnen("Ordne jedem Baustein seinen Inhalt zu.",
           [("Induktionsanfang (IA)", "A(1) direkt nachrechnen"),
            ("Induktionsvoraussetzung (IV)", "A(n) gilt für ein beliebiges, aber festes n"),
            ("Induktionsschritt (IS)", "mit der IV zeigen: A(n+1) gilt"),
            ("Induktionsschluss (ISch)", "also gilt A(n) für alle n ∈ ℕ")],
           "IA prüft den Start, IV nimmt einen Fall an, IS folgert den nächsten, ISch fasst zusammen.",
           ablenker=["A(n) gilt für alle n ∈ ℕ (als Annahme)"],
           tipps=["Die IV nimmt die Aussage für **ein** $n$ an, nicht für alle."])

_IV = ["Für ein beliebiges, aber festes $n \\in \\mathbb{N}$ gelte $\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$.",
       "Für alle $n \\in \\mathbb{N}$ gilt $\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$.",
       "Für $n = 1$ gilt $\\sum_{i=1}^{1} i = 1$.",
       "Es gilt $\\sum_{i=1}^{n+1} i = \\frac{(n+1)(n+2)}{2}$."]
k.mc("Welche Formulierung ist eine korrekte Induktionsvoraussetzung für $\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$?", _IV,
     "Die IV nimmt die Aussage für **ein** beliebiges, aber festes $n$ an. Daraus wird im IS die Aussage für $n + 1$ gefolgert.",
     tipps=["Die IV ist eine Annahme über ein einzelnes $n$.", "„Für alle $n$“ ist das, was am Ende herauskommen soll.",
            "beliebig, aber fest"],
     fehler={_IV[1]: "Das ist die Behauptung selbst. Wer sie voraussetzt, dreht sich im Kreis (Zirkelschluss).",
             _IV[2]: "Das ist der Induktionsanfang.",
             _IV[3]: "Das ist die Aussage $A(n + 1)$, die der Induktionsschritt zeigen soll."})

# ── 3: Gauß-Summe ──────────────────────────────────────────────────────────
k.erklaerung("Beispiel: Die Summe der ersten n Zahlen", r"""
    ## Der Beweis aus der Vorlesung

    **Satz.** Für alle $n \in \mathbb{N}$ gilt $\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$.

    **IA** ($n = 1$): $\sum_{i=1}^{1} i = 1 = \frac{1 \cdot 2}{2}$ ✓

    **IV:** Für ein beliebiges, aber festes $n \in \mathbb{N}$ gelte
    $\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$.

    **IS** ($n \to n + 1$):

    :::rechnung
    \sum_{i=1}^{n+1} i = \sum_{i=1}^{n} i + (n + 1) || letzten Summanden abspalten
    = \frac{n(n+1)}{2} + (n + 1) || einsetzen der (IV)
    = \frac{n(n+1) + 2(n+1)}{2} || Hauptnenner $2$
    = \frac{(n+1)(n+2)}{2} || $(n + 1)$ ausklammern
    :::

    Das ist die Formel für $n + 1$. **ISch:** Nach dem Prinzip der vollständigen
    Induktion gilt sie für alle $n \in \mathbb{N}$. $\square$

    :::alt Mit Zielvorstellung erklärt
    Schreib dir vor dem IS auf, wo du hin willst: $\frac{(n+1)(n+2)}{2}$, also
    die Formel mit $n + 1$ statt $n$. Dann rechnest du von links so lange, bis
    genau das dasteht.
    :::
    """)

k.zahl("Prüfe die Formel $\\sum_{k=1}^{n} k^3 = \\left(\\frac{n(n+1)}{2}\\right)^2$ für $n = 2$: Welchen Wert hat die rechte Seite?",
       F(2 * 3, 2) ** 2,
       "$\\left(\\frac{2 \\cdot 3}{2}\\right)^2 = 3^2 = 9$. Links: $1^3 + 2^3 = 9$. Beide Seiten stimmen.",
       tipps=["Setze $n = 2$ in die rechte Seite ein.", "$\\frac{2 \\cdot 3}{2} = 3$", "Jetzt noch quadrieren."],
       rechenweg=r"""
       :::rechnung
       \left(\frac{2 \cdot 3}{2}\right)^2 = 3^2 || $n = 2$ eingesetzt
       = 9 || quadrieren
       1^3 + 2^3 = 9 || linke Seite zur Kontrolle
       :::
       """,
       typische_fehler=[(3, "Das Quadrat außen fehlt: $\\left(\\frac{2 \\cdot 3}{2}\\right)^2 = 3^2$."),
                        (36, "Für $n = 2$ ist $n + 1 = 3$, nicht $4$. Rechne $\\frac{2 \\cdot 3}{2}$.")])

# ── 4: IV einsetzen ────────────────────────────────────────────────────────
k.erklaerung("Die IV im Induktionsschritt finden", r"""
    ## Das Alte im Neuen suchen

    Im IS steht links die Summe bis $n + 1$. Spalte den letzten Summanden ab,
    dann steht die Summe bis $n$ da, und für sie gilt die IV.

    **Satz.** $\sum_{k=1}^{n} (2k - 1) = n^2$ für alle $n \in \mathbb{N}$.
    IA: $2 \cdot 1 - 1 = 1 = 1^2$ ✓. IV: Für ein festes $n$ gelte die Formel.

    :::rechnung IS
    \sum_{k=1}^{n+1} (2k - 1) = \sum_{k=1}^{n} (2k - 1) + (2(n+1) - 1) || letzten Summanden abspalten
    = n^2 + 2(n + 1) - 1 || einsetzen der (IV)
    = n^2 + 2n + 1 || ausrechnen
    = (n + 1)^2 || binomische Formel
    :::

    :::achtung Die IV muss vorkommen
    Kommt im IS die IV nirgends vor, ist es kein Induktionsbeweis. Markiere die
    Stelle mit „(IV)“ über dem Gleichheitszeichen.
    :::

    :::alt Mit einem Kontoauszug erklärt
    Der Kontostand nach $n + 1$ Monaten ist der Stand nach $n$ Monaten plus die
    letzte Buchung. Den Stand nach $n$ Monaten kennst du schon (IV). Du musst
    nur noch die letzte Buchung dazurechnen.
    :::
    """)

k.luecke("Im Induktionsschritt spaltest du den letzten Summanden ab. Was gehört in die Lücke?",
         r"\sum_{k=1}^{n+1} (2k - 1) = \sum_{k=1}^{n} (2k - 1) + \luecke", [["2n + 1"]],
         "Der letzte Summand entsteht aus $2k - 1$ mit $k = n + 1$: $2(n + 1) - 1 = 2n + 1$.",
         tipps=["Setze $k = n + 1$ in $2k - 1$ ein.", "$2(n + 1) - 1$", "Ausmultiplizieren."],
         rechenweg=r"""
         :::rechnung
         2(n + 1) - 1 = 2n + 1 || $k = n + 1$ eingesetzt
         :::
         """,
         typische_fehler=[(["2n - 1"], "Das ist der Summand für $k = n$, er steckt schon in der Summe bis $n$."),
                          (["2n"], "Klammer vergessen? $2(n + 1) - 1 = 2n + 2 - 1 = 2n + 1$.")])

k.term("Fasse zusammen (das ist der letzte Teil eines Induktionsschritts): $n^2 + 2n + 1$ als Quadrat.", "(n+1)^2",
       "Erste binomische Formel: $n^2 + 2n + 1 = (n + 1)^2$.", variablen="n", form="faktorisiert",
       tipps=["Welche binomische Formel passt?", "$(a + b)^2 = a^2 + 2ab + b^2$", "$a = n$, $b = 1$"],
       rechenweg=r"""
       :::rechnung
       n^2 + 2n + 1 = (n + 1)^2 || erste binomische Formel
       :::
       """,
       typische_fehler=[("(n+1)^2+1", "Die $1$ steckt schon im Quadrat: $(n+1)^2 = n^2 + 2n + 1$."),
                        ("n^2+1", "Der mittlere Summand $2n$ ist verschwunden.")])

# ── 5: Teilbarkeit ─────────────────────────────────────────────────────────
k.erklaerung("Teilbarkeit per Induktion", r"""
    ## Beispiel aus dem Moodle-Kurs

    **Satz.** Für alle $n \in \mathbb{N}$ existiert ein $k \in \mathbb{N}$ mit $n^2 + n = 2k$.

    **IA** ($n = 1$): $1^2 + 1 = 2 = 2 \cdot 1$, setze $k = 1$ ✓

    **IV:** Für ein beliebiges, aber festes $n \in \mathbb{N}$ gebe es ein
    $k \in \mathbb{N}$ mit $n^2 + n = 2k$.

    **IS:** Zu zeigen ist: $(n+1)^2 + (n+1)$ ist das Doppelte einer natürlichen Zahl.

    :::rechnung
    (n + 1)^2 + (n + 1) = n^2 + 2n + 1 + n + 1 || binomische Formel
    = (n^2 + n) + 2n + 2 || umsortieren, um die IV zu finden
    = 2k + 2n + 2 \quad \text{(IV)} || einsetzen der (IV): $n^2 + n = 2k$
    2k + 2n + 2 = 2(k + n + 1) || $2$ ausklammern
    :::

    Mit $\ell := k + n + 1 \in \mathbb{N}$ gilt $(n+1)^2 + (n+1) = 2\ell$.
    **ISch:** Die Aussage gilt für alle $n \in \mathbb{N}$. $\square$

    :::alt Mit Paaren erklärt
    $n^2 + n = n(n+1)$ ist das Produkt zweier Nachbarzahlen. Eine davon ist
    immer gerade. Das ist ein direkter Beweis. Die Induktion zeigt dasselbe,
    indem sie nur vom einen $n$ zum nächsten schaut.
    :::
    """)

_MOODLE = [
    "Wir beweisen die Aussage mittels vollständiger Induktion über $n \\in \\mathbb{N}$.",
    "Induktionsanfang: Für $n = 1$ gilt $1^2 + 1 = 2$ ✓ (setze $k = 1$).",
    "Induktionsvoraussetzung: Für ein beliebiges, aber festes $n \\in \\mathbb{N}$ existiere ein $k \\in \\mathbb{N}$ mit $n^2 + n = 2k$.",
    "Induktionsschritt: Wir zeigen nun, dass die Aussage dann auch für $n + 1$ gilt.",
    "Unter Verwendung gängiger Rechenregeln und durch Einsetzen der (IV) erhalten wir: "
    "$(n+1)^2 + (n+1) = n^2 + 2n + 1 + n + 1 = n^2 + n + 2n + 2 = 2k + 2n + 2 = 2 \\cdot (k + n + 1)$.",
    "Setze $\\ell := k + n + 1$. Dann gilt $(n+1)^2 + (n+1) = 2 \\cdot \\ell$ mit $\\ell \\in \\mathbb{N}$, d. h. unter Annahme "
    "der IV stimmt die Behauptung auch für $n + 1$.",
    "Induktionsschluss: Nach dem Prinzip der vollständigen Induktion gilt die Aussage für alle $n \\in \\mathbb{N}$.",
]
k.ordnen("Sortiere die Beweisschritte des Induktionsbeweises. Zu zeigen: Für alle $n \\in \\mathbb{N}$ existiert ein "
         "$k \\in \\mathbb{N}$ mit $n^2 + n = 2k$. (Nach der Moodle-Aufgabe „Induktion: Beweisschritte sortieren“)",
         _MOODLE,
         "Reihenfolge wie in jedem Induktionsbeweis: Ankündigung, IA, IV, IS (Rechnung mit IV, Fazit für $n + 1$), ISch.",
         ablenker=["Induktionsvoraussetzung: Für alle $n \\in \\mathbb{N}$ existiert ein $k \\in \\mathbb{N}$ mit $n^2 + n = 2k$.",
                   "Für $n = 2$ gilt $4 + 2 = 6 = 2 \\cdot 3$, also gilt die Aussage für alle $n$."],
         tipps=["Der Beweis beginnt mit der Ankündigung der Methode und endet mit dem Induktionsschluss.",
                "Die IV gilt für **ein** festes $n$, nicht für alle.",
                "Erst rechnen, dann $\\ell$ benennen und das Ergebnis für $n + 1$ festhalten."])

# ── 6: Anderer Startwert ───────────────────────────────────────────────────
k.erklaerung("Anderer Startwert und Ungleichungen", r"""
    ## Wenn die Aussage erst ab n₀ gilt

    Soll $A(n)$ für alle $n \ge n_0$ gelten, machst du den IA für $n = n_0$ und
    nimmst in der IV ein festes $n \ge n_0$ an.

    **Satz.** Für alle $n \in \mathbb{N}$ mit $n \ge 4$ gilt $n! \ge 2^n$.
    (Für $n = 3$ ist es falsch: $6 < 8$.)

    :::visual induktion_domino
    {"anzahl": 8, "anfang": 4, "aussage": "$n! \\ge 2^n$", "text_anfang": "IA bei $n = 4$: $24 \\ge 16$."}
    :::

    :::rechnung IA und IS
    4! = 24 \ge 16 = 2^4 || IA für $n = 4$
    (n + 1)! = (n + 1) \cdot n! || Definition der Fakultät
    (n + 1) \cdot n! \ge (n + 1) \cdot 2^n || einsetzen der (IV) $n! \ge 2^n$
    (n + 1) \cdot 2^n \ge 2 \cdot 2^n = 2^{n+1} || $n + 1 \ge 5 \ge 2$
    :::

    :::alt Mit einem Rennen erklärt
    $n!$ wird in jedem Schritt mit $n + 1$ malgenommen, $2^n$ nur mit $2$. Ab
    $n = 4$ ist $n!$ vorne und vergrößert seinen Vorsprung jedes Mal.
    :::
    """)

k.mc("Die Aussage $2^n > n^2$ gilt für alle $n \\ge 5$. Womit beginnt der Induktionsbeweis?",
     ["IA für $n = 5$: $32 > 25$", "IA für $n = 1$: $2 > 1$", "IV für alle $n \\ge 5$", "IA für $n = 4$: $16 > 16$"],
     "Der Induktionsanfang ist beim kleinsten Wert, für den die Aussage behauptet wird: $n_0 = 5$.",
     tipps=["Für welches $n$ soll die Aussage zum ersten Mal gelten?", "$n_0 = 5$", "$2^5 = 32$ und $5^2 = 25$."],
     fehler={"IA für $n = 1$: $2 > 1$": "Für $n = 1$ stimmt es zwar, aber die Kette reißt: Für $n = 3$ ist $8 > 9$ falsch. Der IA gehört zu $n_0 = 5$.",
             "IV für alle $n \\ge 5$": "Ein Induktionsbeweis beginnt mit dem IA, und die IV gilt nur für ein festes $n$.",
             "IA für $n = 4$: $16 > 16$": "$16 > 16$ ist falsch. Die Aussage wird erst ab $n = 5$ behauptet."})

# ── 7: Typische Fehler ─────────────────────────────────────────────────────
k.erklaerung("Typische Fehler", r"""
    ## Ohne Anfang fällt nichts

    Behauptung: „$2 \mid 2n + 1$ für alle $n \in \mathbb{N}$.“ Der IS klappt sogar:

    :::rechnung Scheinbarer IS
    2(n + 1) + 1 = (2n + 1) + 2 || Gilt $2 \mid 2n + 1$, dann auch $2 \mid (2n+1) + 2$
    :::

    Aber der IA scheitert: $2 \cdot 1 + 1 = 3$ ist ungerade. Die Aussage ist für
    jedes $n$ falsch. Der erste Dominostein fällt nicht.

    :::achtung Die drei häufigsten Fehler
    - IA vergessen: Dann ist nichts bewiesen.
    - IV „für alle $n$“ formuliert: Das ist die Behauptung selbst.
    - Im IA die IV benutzen oder im IS die IV gar nicht benutzen.
    :::

    :::alt Mit einer Kettenreaktion erklärt
    Eine perfekt aufgebaute Dominoreihe nützt nichts, wenn niemand den ersten
    Stein anstößt. Der IS ist der Aufbau, der IA der Anstoß. Beides gehört dazu.
    :::
    """)

k.wf("Im Induktionsanfang darf man die Induktionsvoraussetzung benutzen.", False,
     "Falsch. Der IA wird ohne jede Annahme direkt nachgerechnet. Die IV kommt erst im Induktionsschritt zum Einsatz.",
     tipps=["Woher käme im IA die Aussage, die man voraussetzt?"])


# ── Praxis ─────────────────────────────────────────────────────────────────
def _zeilen(*paare):
    return ":::rechnung\n" + "\n".join(f"{t} || {g}" for t, g in paare) + "\n:::"


def induktionsschritt_luecke(rng):
    f, Fn, ftex, Ftex, fn1, fn1_txt, Fn1, Fn1_txt = rng.choice(_FORMELN)
    loesung = [[fn1_txt], [Fn1_txt]]
    f_n = fn1_txt.replace("n", "(n-1)")          # f(n): in f(n+1) jedes n durch n - 1 ersetzt
    F_n = Fn1_txt.replace("n", "(n-1)")          # F(n)
    fehler = [([[f_n], [Fn1_txt]], "Der abgespaltene Summand gehört zu $k = n + 1$, nicht zu $k = n$."),
              ([[fn1_txt], [F_n]], "Rechts muss die Formel mit $n + 1$ statt $n$ stehen: Ersetze **jedes** $n$ durch $n + 1$.")]
    return {
        "frage": f"Induktionsschritt für $\\sum_{{k=1}}^{{n}} {ftex} = {Ftex}$: Spalte den letzten Summanden ab, setze die IV "
                 "ein und gib an, was am Ende herauskommen muss.",
        "formel": f"\\sum_{{k=1}}^{{n+1}} {ftex} = {Ftex} + \\luecke = \\luecke",
        "antworten": loesung,
        "tipps": ["Der abgespaltene Summand ist der für $k = n + 1$.", f"Er lautet ${fn1}$.",
                  f"Rechts steht die Formel ${Ftex}$ mit $n + 1$ statt $n$."],
        "rechenweg": f"Letzter Summand: ${fn1}$. Ziel: ${Fn1}$. "
                     f"(Python prüft $({Ftex}) + {fn1} = {Fn1}$ für $n = 1, \\ldots, 59$.)",
        "erklaerung": "Im IS: Summe bis $n + 1$ = Summe bis $n$ + letzter Summand, dann die IV einsetzen und auf die Formel für $n + 1$ hinrechnen.",
        "typische_fehler": ohne_gleiche(loesung, fehler),
    }


def formel_anwenden(rng):
    f, Fn, ftex, Ftex, *_ = rng.choice(_FORMELN[:6] + _FORMELN[8:10])
    N = rng.randint(6, 25)
    w = Fn(N)
    assert w == _S(f, 1, N)
    return {
        "frage": f"Für alle $n \\in \\mathbb{{N}}$ gilt $\\sum_{{k=1}}^{{n}} {ftex} = {Ftex}$ (per Induktion bewiesen). "
                 f"Berechne damit $\\sum_{{k=1}}^{{{N}}} {ftex}$.",
        "loesung": w,
        "tipps": [f"Setze $n = {N}$ in die Formel ${Ftex}$ ein.", "Du musst die Summanden nicht einzeln addieren.",
                  "Achte auf Klammern und Potenzen."],
        "rechenweg": f"Mit $n = {N}$ in ${Ftex}$ eingesetzt ergibt sich ${mathlib.tex(w)}$.",
        "erklaerung": "Eine bewiesene Summenformel erspart das Addieren aller Summanden.",
        "typische_fehler": ohne_gleiche(w, [(Fn(N - 1), f"Das ist die Formel für $n = {N - 1}$."),
                                            (Fn(N + 1), f"Das ist die Formel für $n = {N + 1}$."),
                                            (f(N), "Das ist nur der letzte Summand, nicht die ganze Summe.")]),
    }


def induktion_ordnen(rng):
    f, Fn, ftex, Ftex, fn1, _, Fn1, _ = rng.choice(_FORMELN)
    a1 = mathlib.tex(F(f(1)))
    behauptung = f"\\sum_{{k=1}}^{{n}} {ftex} = {Ftex}"
    schritte = [
        f"Induktionsanfang ($n = 1$): $\\sum_{{k=1}}^{{1}} {ftex} = {a1}$, und die rechte Seite ergibt für $n = 1$ ebenfalls ${a1}$ ✓",
        f"Induktionsvoraussetzung: Für ein beliebiges, aber festes $n \\in \\mathbb{{N}}$ gelte ${behauptung}$.",
        f"Induktionsschritt ($n \\to n + 1$): $\\sum_{{k=1}}^{{n+1}} {ftex} = \\sum_{{k=1}}^{{n}} {ftex} + {fn1}$.",
        f"Einsetzen der (IV) ergibt ${Ftex} + {fn1}$.",
        f"Zusammenfassen ergibt ${Fn1}$. Das ist die Behauptung für $n + 1$.",
        "Induktionsschluss: Nach dem Prinzip der vollständigen Induktion gilt die Formel für alle $n \\in \\mathbb{N}$.",
    ]
    return {
        "frage": f"Bringe den Induktionsbeweis von ${behauptung}$ in die richtige Reihenfolge.",
        "schritte": schritte,
        "ablenker": [f"Induktionsvoraussetzung: Für alle $n \\in \\mathbb{{N}}$ gilt ${behauptung}$.",
                     "Für $n = 2$ stimmt die Formel auch. Damit ist sie bewiesen."],
        "tipps": ["IA, IV, IS, ISch.", "Im IS: erst abspalten, dann die IV einsetzen, dann zusammenfassen.",
                  "Die IV gilt nur für ein festes $n$."],
        "erklaerung": "Jeder Induktionsbeweis hat dieselbe Gliederung. Die IV geht genau beim Einsetzen ein.",
    }


k.praxis()

k.generator(formel_anwenden, typ="zahl", titel="Summenformeln anwenden")
k.generator(induktionsschritt_luecke, typ="luecke", titel="Induktionsschritt vorbereiten")
k.generator(induktion_ordnen, typ="ordnen", titel="Induktionsbeweise ordnen")

k.papier(r"""
    ## Übungsblatt-Stil: Summenformel per Induktion

    Zeigen Sie mittels vollständiger Induktion, dass für alle $n \in \mathbb{N}$ gilt:
    $$\sum_{k=1}^{n} k^2 = \frac{n(n+1)(2n+1)}{6}.$$
    Kennzeichnen Sie Induktionsanfang, -voraussetzung, -schritt und -schluss sowie die Stelle, an der die IV eingeht.
    """,
    r"""
    **IA** ($n = 1$): $\sum_{k=1}^{1} k^2 = 1$ und $\frac{1 \cdot 2 \cdot 3}{6} = 1$ ✓

    **IV:** Für ein beliebiges, aber festes $n \in \mathbb{N}$ gelte $\sum_{k=1}^{n} k^2 = \frac{n(n+1)(2n+1)}{6}$.

    **IS** ($n \to n + 1$): Zu zeigen ist $\sum_{k=1}^{n+1} k^2 = \frac{(n+1)(n+2)(2n+3)}{6}$.

    :::rechnung
    \sum_{k=1}^{n+1} k^2 = \sum_{k=1}^{n} k^2 + (n + 1)^2 || letzten Summanden abspalten
    = \frac{n(n+1)(2n+1)}{6} + (n + 1)^2 || einsetzen der (IV)
    = \frac{(n+1)(n(2n+1) + 6(n+1))}{6} || Hauptnenner, $(n+1)$ ausklammern
    = \frac{(n+1)(2n^2 + 7n + 6)}{6} || ausmultiplizieren
    = \frac{(n+1)(n+2)(2n+3)}{6} || $2n^2 + 7n + 6 = (n+2)(2n+3)$
    :::

    **ISch:** Nach dem Prinzip der vollständigen Induktion gilt die Formel für alle $n \in \mathbb{N}$. $\square$
    """,
    ["IA: beide Seiten für $n = 1$ ausgerechnet",
     "IV: „für ein beliebiges, aber festes $n$“ formuliert",
     "IS: Ziel für $n + 1$ hingeschrieben und den letzten Summanden abgespalten",
     "IS: Stelle mit „(IV)“ markiert",
     "IS: korrekt zu $\\frac{(n+1)(n+2)(2n+3)}{6}$ umgeformt",
     "ISch formuliert"],
    "Tipp für das Umformen: $(n+1)$ früh ausklammern, dann bleibt ein quadratischer Term, den man faktorisiert.",
    uebungsblatt=True,
    tipps=["Schreibe zuerst auf, was im IS herauskommen muss: die Formel mit $n + 1$."])

k.papier(r"""
    ## Übungsblatt-Stil: Teilbarkeit und geometrische Summe

    a) Zeigen Sie per Induktion: Für alle $n \in \mathbb{N}$ ist $n^3 + 2n$ durch $3$ teilbar.

    b) Zeigen Sie per Induktion die [[geometrische Summe]] für $q = 2$: $\displaystyle\sum_{k=0}^{n-1} 2^k = 2^n - 1$ für alle $n \in \mathbb{N}$.
    Was bedeutet das für die größte Zahl, die man mit $n$ Bits darstellen kann?
    """,
    r"""
    **a)** **IA** ($n = 1$): $1 + 2 = 3 = 3 \cdot 1$ ✓

    **IV:** Für ein beliebiges, aber festes $n \in \mathbb{N}$ gebe es $m \in \mathbb{N}$ mit $n^3 + 2n = 3m$.

    **IS:**

    :::rechnung
    (n + 1)^3 + 2(n + 1) = n^3 + 3n^2 + 3n + 1 + 2n + 2 || ausmultiplizieren
    = (n^3 + 2n) + 3n^2 + 3n + 3 || umsortieren, um die IV zu finden
    = 3m + 3n^2 + 3n + 3 \quad \text{(IV)} || einsetzen der (IV)
    3m + 3n^2 + 3n + 3 = 3(m + n^2 + n + 1) || $3$ ausklammern
    :::

    Da $m + n^2 + n + 1 \in \mathbb{N}$, gilt $3 \mid (n+1)^3 + 2(n+1)$.
    **ISch:** Die Aussage gilt für alle $n \in \mathbb{N}$. $\square$

    **b)** **IA** ($n = 1$): $\sum_{k=0}^{0} 2^k = 2^0 = 1 = 2^1 - 1$ ✓

    **IV:** Für ein festes $n$ gelte $\sum_{k=0}^{n-1} 2^k = 2^n - 1$.

    **IS:** $\sum_{k=0}^{n} 2^k = \sum_{k=0}^{n-1} 2^k + 2^n \overset{(IV)}{=} 2^n - 1 + 2^n = 2 \cdot 2^n - 1 = 2^{n+1} - 1$.

    **ISch:** gilt für alle $n \in \mathbb{N}$. $\square$

    Mit $n$ Bits, alle auf $1$, stellt man $\sum_{k=0}^{n-1} 2^k = 2^n - 1$ dar, zum Beispiel $255$ bei $8$ Bits.
    """,
    ["a) IA gerechnet und IV mit einer Hilfszahl $m$ formuliert",
     "a) $(n+1)^3$ korrekt ausmultipliziert und $n^3 + 2n$ wiedergefunden",
     "a) IV markiert eingesetzt und $3$ ausgeklammert",
     "b) IA mit der Summe von $k = 0$ bis $0$ gerechnet",
     "b) im IS den Summanden $2^n$ abgespalten und $2 \\cdot 2^n = 2^{n+1}$ benutzt",
     "b) Bedeutung $2^n - 1$ für $n$ Bits erklärt"],
    "Bei Teilbarkeit per Induktion suchst du im Term für $n + 1$ den alten Term $n^3 + 2n$, denn über ihn weiß die IV etwas.",
    uebungsblatt=True,
    tipps=["Schreibe $(n+1)^3 + 2(n+1)$ so um, dass $n^3 + 2n$ als Teil darin steht."])

k.zusammenfassung(r"""
    ## Vollständige Induktion

    | Baustein | Inhalt |
    |---|---|
    | IA | $A(n_0)$ direkt nachrechnen (meist $n_0 = 1$) |
    | IV | $A(n)$ gelte für ein beliebiges, aber festes $n \ge n_0$ |
    | IS ($n \to n+1$) | mit der IV zeigen, dass $A(n+1)$ gilt; „(IV)“ markieren |
    | ISch | nach dem Prinzip der vollständigen Induktion gilt $A(n)$ für alle $n \ge n_0$ |

    !! Bei Summen: $\sum_{k=1}^{n+1} a_k = \sum_{k=1}^{n} a_k + a_{n+1}$, dann die IV einsetzen.

    - Bekannte Formeln: $\sum_{k=1}^{n} k = \frac{n(n+1)}{2}$, $\sum_{k=1}^{n} (2k-1) = n^2$,
      $\sum_{k=1}^{n} k^2 = \frac{n(n+1)(2n+1)}{6}$, $\sum_{k=0}^{n-1} 2^k = 2^n - 1$.
    - Teilbarkeit: im Term für $n + 1$ den alten Term suchen.
    - Fehler: IA vergessen, IV „für alle $n$“, IV nicht benutzt.
""")
