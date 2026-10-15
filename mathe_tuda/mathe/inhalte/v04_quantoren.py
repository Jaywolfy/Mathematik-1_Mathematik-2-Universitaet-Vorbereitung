# -*- coding: utf-8 -*-
"""Vorkurs 4: Quantoren – Allaussagen, Existenzaussagen, Beispiel und Gegenbeispiel,
Negation von Quantoraussagen, mehrere Quantoren (MVK 2026, VL 1)."""
from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(
    slug="quantoren",
    titel="Quantoren",
    beschreibung="Für alle und es gibt: Allaussagen, Existenzaussagen, Gegenbeispiele und richtig negieren",
    teil="vorkurs",
    quelle="MVK 2026, VL 1",
    icon="🔍")

k.lernziele([
    "Ich kann Existenz- und Allaussagen mit $\\exists$ und $\\forall$ formulieren und vorlesen",
    "Ich kann entscheiden, ob eine Quantoraussage wahr ist, und dafür ein Beispiel oder Gegenbeispiel angeben",
    "Ich kann Aussagen mit Quantoren richtig negieren",
    "Ich kenne $\\exists!$ und $\\nexists$ und weiß, dass die Reihenfolge mehrerer Quantoren zählt",
])

k.warum(r"""
Quantoren stecken in jeder Schleife, die etwas prüft. Pythons `all(...)` ist ein Allquantor,
`any(...)` ein Existenzquantor: `all(x > 0 for x in liste)`. Eine Allaussage über eine Liste
prüft man, indem man **ein** Gegenbeispiel sucht und dann abbricht. In SQL heißt der
Existenzquantor `EXISTS`. Und jede Definition in Mathe 1, von „injektiv“ bis „konvergent“,
ist mit $\forall$ und $\exists$ geschrieben. Wer sie nicht negieren kann, kann sie nicht widerlegen.
""")

# Python prüft alle Beispielzahlen selbst nach
_P = lambda n: n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))  # noqa: E731
_EULER = next(n for n in range(1, 1000) if not _P(n * n + n + 41))
assert all(_P(n * n + n + 41) for n in range(1, _EULER))
_EW = _EULER ** 2 + _EULER + 41

# ── 1: Allaussagen ─────────────────────────────────────────────────────────
k.erklaerung("Allaussagen und Existenzaussagen", r"""
    ## $\forall$: für alle

    :::analogie 🎫 Die Fahrkartenkontrolle
    „Alle Fahrgäste haben ein Ticket“ prüft der Kontrolleur, indem er **jeden** fragt.
    Ein einziger Schwarzfahrer reicht, und die Aussage ist falsch.
    :::

    Sei $M$ eine Menge und $E$ eine Eigenschaft. Eine [[Allaussage]] hat die Form

    $$\forall x \in M : x \text{ erfüllt } E$$

    gelesen „für alle $x$ aus $M$ gilt $E$“. Das Zeichen $\forall$ heißt [[Allquantor]].
    Sie ist wahr, wenn **jedes** Element von $M$ die Eigenschaft hat.

    :::rechnung Beispiel vorgerechnet: $\forall x \in \{1, 2, 3\} : x^2 \le 9$
    1^2 = 1 \le 9 || $x = 1$ erfüllt die Eigenschaft
    2^2 = 4 \le 9 || $x = 2$ auch
    3^2 = 9 \le 9 || $x = 3$ auch, also ist die Allaussage wahr
    :::

    Für unendliche Mengen braucht man ein allgemeines Argument, z. B. $\forall x \in \mathbb{R} : x^2 \ge 0$,
    weil ein Produkt zweier Zahlen mit gleichem Vorzeichen nie negativ ist.

    :::alt Mit Code erklärt
    Eine Allaussage ist eine Schleife, die bei jedem Element prüft und beim ersten
    Fehlschlag `False` zurückgibt: `all(x**2 <= 9 for x in [1, 2, 3])`. Nur wenn kein
    Element durchfällt, kommt `True` heraus.
    :::
    ---
    ## $\exists$: es gibt

    Eine [[Existenzaussage]] hat die Form

    $$\exists x \in M : x \text{ erfüllt } E$$

    gelesen „es gibt (mindestens) ein $x$ aus $M$ mit $E$“. Das Zeichen $\exists$ heißt
    [[Existenzquantor]]. Sie ist wahr, sobald **ein** passendes Element existiert.

    - $\exists!$ heißt „es gibt **genau** ein“.
    - $\nexists$ heißt „es gibt kein“.

    :::rechnung Beispiele vorgerechnet
    \exists x \in \mathbb{N} : x^2 = 4 \quad \text{wahr} || Beispiel $x = 2$, denn $2^2 = 4$
    \exists! x \in \mathbb{R} : 2x = 6 \quad \text{wahr} || nur $x = 3$
    \nexists x \in \mathbb{N} : x + 1 = 1 \quad \text{wahr} || nur $x = 0$ passt, und $0 \notin \mathbb{N}$
    :::

    :::alt Mit einer Suche erklärt
    Eine Existenzaussage ist eine Suche: `any(x**2 == 4 for x in zahlen)`. Sobald ein
    Treffer gefunden ist, ist die Antwort `True`. „Genau ein“ heißt: genau ein Treffer,
    nicht null und nicht zwei.
    :::
    """)

k.zuordnen("Ordne jedem Zeichen seine Bedeutung zu.",
           [("$\\forall$", "für alle"), ("$\\exists$", "es gibt mindestens ein"),
            ("$\\exists!$", "es gibt genau ein"), ("$\\nexists$", "es gibt kein")],
           "$\\forall$ ist ein umgedrehtes A (wie „alle“), $\\exists$ ein gespiegeltes E (wie „existiert“).",
           tipps=["Denk an die Buchstaben: A für alle, E für existiert."])

k.wf("$\\forall x \\in \\mathbb{Z} : x^2 \\ge x$", True,
     "Für $x \\le 0$ ist $x^2 \\ge 0 \\ge x$. Für $x \\ge 1$ ist $x^2 = x \\cdot x \\ge 1 \\cdot x = x$. "
     "Es gibt also kein Gegenbeispiel in $\\mathbb{Z}$. (In $\\mathbb{R}$ wäre $x = \\frac{1}{2}$ eins.)",
     tipps=["Probiere negative Zahlen, $0$, $1$ und große Zahlen aus."])

k.wf("$\\exists x \\in \\mathbb{N} : x + 1 = 1$", False,
     "Nur $x = 0$ erfüllt $x + 1 = 1$. Im Vorkurs ist aber $0 \\notin \\mathbb{N}$. In $\\mathbb{N}_0$ wäre die Aussage wahr.",
     tipps=["Welche Zahl erfüllt $x + 1 = 1$? Liegt sie in $\\mathbb{N}$?"])

k.mc("Wie schreibt man „Jede natürliche Zahl ist größer als $0$.“ mit Quantoren?",
     ["$\\forall n \\in \\mathbb{N} : n > 0$", "$\\exists n \\in \\mathbb{N} : n > 0$",
      "$\\forall n \\in \\mathbb{N} : n \\ge 0$ und $\\exists n : n > 0$", "$\\exists! n \\in \\mathbb{N} : n > 0$"],
     "„Jede“ heißt „für alle“: $\\forall$. Die Eigenschaft hinter dem Doppelpunkt ist $n > 0$.",
     tipps=["„Jede“ und „alle“ bedeuten dasselbe.", "Welcher Quantor steht für „alle“?"],
     fehler={"$\\exists n \\in \\mathbb{N} : n > 0$": "$\\exists$ sagt nur: **mindestens eine** Zahl ist größer als $0$. "
                                                     "Gemeint ist aber jede.",
             "$\\exists! n \\in \\mathbb{N} : n > 0$": "$\\exists!$ hieße „genau eine“. Es sind aber alle."})

# ── 2: Beispiel und Gegenbeispiel ─────────────────────────────────────────
k.erklaerung("Beispiel und Gegenbeispiel", r"""
    ## Was beweist ein Beispiel?

    | Aussage | wahr zeigen | falsch zeigen |
    |---|---|---|
    | $\forall x \in M : E$ | allgemeines Argument für **jedes** $x$ | **ein** [[Gegenbeispiel]] |
    | $\exists x \in M : E$ | **ein** Beispiel | allgemeines Argument: **kein** $x$ passt |

    :::rechnung Gegenbeispiel vorgerechnet: $\forall n \in \mathbb{N} : n^2 + n + 41$ ist eine Primzahl
    1^2 + 1 + 41 = 43 || Primzahl
    2^2 + 2 + 41 = 47 || Primzahl
    """ + f"{_EULER}^2 + {_EULER} + 41 = {_EW} = 41^2" + r""" || keine Primzahl: Gegenbeispiel
    :::

    Für $n = 1$ bis $n = """ + str(_EULER - 1) + r"""$ entsteht jedes Mal eine Primzahl. Trotzdem ist die
    Allaussage falsch: ein Gegenbeispiel genügt.

    :::achtung Beispiele beweisen keine Allaussage
    $""" + str(_EULER - 1) + r"""$ passende Beispiele zeigen nicht, dass etwas für **alle** $n$ gilt.
    Umgekehrt widerlegt ein einzelnes Beispiel ohne die Eigenschaft keine Existenzaussage.
    :::

    :::alt Mit Schwänen erklärt
    Du siehst tausend weiße Schwäne. Sind alle Schwäne weiß? Nein: In Australien gibt es
    schwarze. Ein schwarzer Schwan widerlegt „alle Schwäne sind weiß“ sofort. Tausend weiße
    beweisen es nicht. Umgekehrt beweist ein schwarzer Schwan „es gibt schwarze Schwäne“.
    :::
    """)

k.zahl("Die Aussage „$\\forall n \\in \\mathbb{N} : n^2 + n + 41$ ist eine Primzahl“ ist falsch. "
       "Welches ist das **kleinste** Gegenbeispiel $n$?", _EULER,
       f"Für $n = 1, \\ldots, {_EULER - 1}$ entstehen Primzahlen. Bei $n = {_EULER}$: "
       f"${_EULER}^2 + {_EULER} + 41 = {_EULER} \\cdot {_EULER + 1} + 41 = {_EW} = 41^2$.",
       tipps=["Probieren dauert lange. Such eine Zahl, bei der man $41$ ausklammern kann.",
              "Für welches $n$ ist $n^2 + n = n(n + 1)$ ein Vielfaches von $41$?",
              f"Bei $n = {_EULER}$ ist $n + 1 = 41$."],
       rechenweg=r"""
       :::rechnung
       """ + f"{_EULER}^2 + {_EULER} + 41 = {_EULER} \\cdot {_EULER + 1} + 41 || ausklammern: $n^2 + n = n(n + 1)$\n"
       f"       = 41 \\cdot {_EULER} + 41 || weil ${_EULER + 1} = 41$\n"
       f"       = 41 \\cdot 41 || $41$ ausklammern\n"
       f"       = {_EW} || keine Primzahl\n" + r"""       :::
       """,
       typische_fehler=[(41, f"Bei $n = 41$ klappt es auch ($41 \\cdot 43$), aber $n = {_EULER}$ ist kleiner."),
                        (0, "$0 \\notin \\mathbb{N}$, und $0^2 + 0 + 41 = 41$ ist sogar eine Primzahl.")])

_M = [-2, -1, 0, 1, 2]
_AUSSAGEN = [
    ("$\\forall x \\in M : x^2 \\le 4$", all(x * x <= 4 for x in _M)),
    ("$\\exists x \\in M : x^3 = -8$", any(x ** 3 == -8 for x in _M)),
    ("$\\exists! x \\in M : x^2 = 0$", sum(1 for x in _M if x * x == 0) == 1),
    ("$\\nexists x \\in M : x > 2$", not any(x > 2 for x in _M)),
    ("$\\forall x \\in M : x < 2$", all(x < 2 for x in _M)),
    ("$\\exists! x \\in M : x^2 = 1$", sum(1 for x in _M if x * x == 1) == 1),
    ("$\\forall x \\in M : x \\ge 0$", all(x >= 0 for x in _M)),
]
k.mehrfach("Es sei $M := \\{-2, -1, 0, 1, 2\\}$. Welche Aussagen sind wahr?",
           [t for t, w in _AUSSAGEN if w], [t for t, w in _AUSSAGEN if not w],
           "Prüfe jede Aussage an allen fünf Elementen. Gegenbeispiele: $x = 2$ für $x < 2$, $x = -1$ für $x \\ge 0$. "
           "$x^2 = 1$ hat in $M$ **zwei** Lösungen ($1$ und $-1$), also nicht genau eine.",
           tipps=["$\\forall$: Suche ein Gegenbeispiel. $\\exists$: Suche ein Beispiel.",
                  "Bei $\\exists!$ musst du zählen: genau ein passendes Element?"],
           fehler={"$\\exists! x \\in M : x^2 = 1$": "Es gibt zwei solche Elemente: $1$ und $-1$. $\\exists!$ verlangt genau eins.",
                   "$\\forall x \\in M : x < 2$": "Gegenbeispiel $x = 2$: $2 < 2$ ist falsch."})

# ── 3: Negation ────────────────────────────────────────────────────────────
k.erklaerung("Quantoraussagen negieren", r"""
    ## Quantor tauschen, Eigenschaft negieren

    Sei $M$ eine Menge und $E$ eine Eigenschaft.

    $$\neg(\forall x \in M : E) \quad \Leftrightarrow \quad \exists x \in M : \neg E$$
    $$\neg(\exists x \in M : E) \quad \Leftrightarrow \quad \forall x \in M : \neg E \quad (\text{bzw. } \nexists x \in M : E)$$

    !! Beim Negieren wird aus $\forall$ ein $\exists$ und umgekehrt. Die Eigenschaft wird negiert, die Menge $M$ bleibt.

    :::rechnung Beispiele vorgerechnet
    \text{„Alle Tiere können schwimmen.“} || Allaussage
    \text{„Es gibt (mindestens) ein Tier, das nicht schwimmen kann.“} || Negation
    \forall x \in \mathbb{N} : \tfrac{x}{2} \in \mathbb{N} \quad\text{wird}\quad \exists x \in \mathbb{N} : \tfrac{x}{2} \notin \mathbb{N} || die Negation ist wahr: $x = 1$
    \exists x \in \mathbb{Z} : x^2 = 0 \quad\text{wird}\quad \forall x \in \mathbb{Z} : x^2 \neq 0 || die Negation ist falsch: $x = 0$
    :::

    :::achtung „Kein“ ist nicht die Negation von „alle“
    Die Negation von „Alle Tiere können schwimmen“ ist **nicht** „Kein Tier kann
    schwimmen“. Um „alle“ zu widerlegen, reicht **ein** Nichtschwimmer.
    :::

    :::alt Mit dem Kontrolleur erklärt
    „Alle haben ein Ticket“ ist falsch, sobald der Kontrolleur **einen** ohne Ticket findet.
    Also heißt „nicht alle haben ein Ticket“: „Es gibt jemanden ohne Ticket“. Und „Es gibt
    jemanden ohne Ticket“ ist falsch, wenn wirklich **alle** eins haben.
    :::
    ---
    ## Zusammengesetzte Eigenschaften negieren

    Steht hinter dem Doppelpunkt ein $\land$, $\lor$ oder $\Rightarrow$, negierst du in
    zwei Schritten: erst den Quantor tauschen, dann die Eigenschaft mit De Morgan bzw.
    $\neg(A \Rightarrow B) \Leftrightarrow A \land \neg B$ umformen.

    :::rechnung Beispiel vorgerechnet
    \neg\big(\forall x \in \mathbb{R} : (x > 1 \Rightarrow x^2 > 1)\big) || Ausgangsaussage verneint
    \Leftrightarrow \exists x \in \mathbb{R} : \neg(x > 1 \Rightarrow x^2 > 1) || Quantor tauschen
    \Leftrightarrow \exists x \in \mathbb{R} : x > 1 \land \neg(x^2 > 1) || $\neg(A \Rightarrow B) \Leftrightarrow A \land \neg B$
    \Leftrightarrow \exists x \in \mathbb{R} : x > 1 \land x^2 \le 1 || $\neg(x^2 > 1)$ ist $x^2 \le 1$
    :::

    Die Negation ist falsch (für $x > 1$ ist stets $x^2 > 1$), also ist die Ausgangsaussage wahr.

    :::alt Wie beim Debuggen
    Du willst einen Fehlerfall finden, der die Regel „für alle $x$: wenn $x > 1$, dann
    $x^2 > 1$“ bricht. Gesucht ist ein **konkretes** $x$, bei dem die Bedingung erfüllt ist,
    das Ergebnis aber nicht. Genau das beschreibt die Negation: $x > 1$ und $x^2 \le 1$.
    :::
    """)

k.mc("Wie lautet die Negation von „Alle Studierenden haben einen Laptop.“?",
     ["„Es gibt mindestens eine studierende Person ohne Laptop.“", "„Keine studierende Person hat einen Laptop.“",
      "„Alle Studierenden haben keinen Laptop.“", "„Es gibt eine studierende Person mit Laptop.“"],
     "Aus „alle“ wird „es gibt“, aus „hat einen Laptop“ wird „hat keinen Laptop“.",
     tipps=["Wie widerlegst du „alle haben einen Laptop“?", "Ein einziges Gegenbeispiel genügt."],
     fehler={"„Keine studierende Person hat einen Laptop.“": "Das ist viel stärker als nötig. Um „alle“ zu widerlegen, "
                                                           "reicht **eine** Person ohne Laptop.",
             "„Alle Studierenden haben keinen Laptop.“": "Du hast die Eigenschaft negiert, aber den Quantor nicht getauscht.",
             "„Es gibt eine studierende Person mit Laptop.“": "Du hast den Quantor getauscht, aber die Eigenschaft nicht negiert."})

k.mc("Wie lautet die Negation von $\\exists x \\in \\mathbb{Z} : x^2 = 2$?",
     ["$\\forall x \\in \\mathbb{Z} : x^2 \\neq 2$", "$\\exists x \\in \\mathbb{Z} : x^2 \\neq 2$",
      "$\\forall x \\in \\mathbb{Z} : x^2 = 2$", "$\\exists x \\notin \\mathbb{Z} : x^2 = 2$"],
     "Quantor tauschen ($\\exists \\to \\forall$), Eigenschaft negieren ($= \\to \\neq$). Die Menge $\\mathbb{Z}$ bleibt.",
     tipps=["Zwei Dinge ändern sich: der Quantor und die Eigenschaft.", "Was passiert mit der Menge $\\mathbb{Z}$?"],
     fehler={"$\\exists x \\in \\mathbb{Z} : x^2 \\neq 2$": "Der Quantor muss getauscht werden: aus $\\exists$ wird $\\forall$.",
             "$\\forall x \\in \\mathbb{Z} : x^2 = 2$": "Die Eigenschaft muss auch negiert werden.",
             "$\\exists x \\notin \\mathbb{Z} : x^2 = 2$": "Die Menge wird nie negiert. Es geht weiter um ganze Zahlen."})

k.mc("Wie lautet die Negation von $\\forall x \\in \\mathbb{R} : (x > 2 \\Rightarrow x^2 > 4)$?",
     ["$\\exists x \\in \\mathbb{R} : x > 2 \\land x^2 \\le 4$", "$\\exists x \\in \\mathbb{R} : (x > 2 \\Rightarrow x^2 \\le 4)$",
      "$\\exists x \\in \\mathbb{R} : x \\le 2 \\land x^2 \\le 4$", "$\\forall x \\in \\mathbb{R} : (x \\le 2 \\Rightarrow x^2 \\le 4)$"],
     "Quantor tauschen, dann $\\neg(A \\Rightarrow B) \\Leftrightarrow A \\land \\neg B$ mit $A$: $x > 2$ und $B$: $x^2 > 4$.",
     tipps=["Erst den Quantor tauschen.", "Wie verneint man eine Implikation $A \\Rightarrow B$?",
            "$\\neg(A \\Rightarrow B)$ ist $A \\land \\neg B$."],
     fehler={"$\\exists x \\in \\mathbb{R} : (x > 2 \\Rightarrow x^2 \\le 4)$":
             "Die Negation einer Implikation ist keine Implikation, sondern $A \\land \\neg B$.",
             "$\\exists x \\in \\mathbb{R} : x \\le 2 \\land x^2 \\le 4$":
             "Die Voraussetzung $x > 2$ bleibt stehen. Negiert wird nur die Folgerung."})

# ── 4: Mehrere Quantoren ──────────────────────────────────────────────────
k.erklaerung("Mehrere Quantoren", r"""
    ## Die Reihenfolge zählt

    Stehen mehrere Quantoren hintereinander, liest man sie von links nach rechts. Ein
    später gewähltes Element darf von den früheren abhängen.

    :::rechnung Beispiel vorgerechnet
    \forall x \in \mathbb{Z}\ \exists y \in \mathbb{Z} : x + y = 0 \quad \text{wahr} || zu jedem $x$ passt $y = -x$
    \exists y \in \mathbb{Z}\ \forall x \in \mathbb{Z} : x + y = 0 \quad \text{falsch} || ein $y$ für alle $x$ gibt es nicht
    :::

    Beim Negieren wird **jeder** Quantor getauscht, die Reihenfolge bleibt:

    $$\neg(\forall x \in \mathbb{Z}\ \exists y \in \mathbb{Z} : x + y = 0) \Leftrightarrow \exists x \in \mathbb{Z}\ \forall y \in \mathbb{Z} : x + y \neq 0$$

    :::achtung Quantoren nicht vertauschen
    „Jeder Topf hat einen Deckel“ ist etwas anderes als „Es gibt einen Deckel, der auf
    jeden Topf passt“. Gleiche Quantoren ($\forall\forall$ oder $\exists\exists$) darf man
    tauschen, verschiedene nicht.
    :::

    :::alt Mit Schlüsseln erklärt
    „Für jede Tür gibt es einen Schlüssel“: Jede Tür hat ihren eigenen. „Es gibt einen
    Schlüssel für jede Tür“: ein Generalschlüssel. Der zweite Satz ist viel stärker. Im
    Code: Bei $\forall x\ \exists y$ steht die Suche nach $y$ **innerhalb** der Schleife über $x$.
    :::
    """)

k.mc("Welche Aussage ist wahr?",
     ["$\\forall x \\in \\mathbb{N}\\ \\exists y \\in \\mathbb{N} : y > x$",
      "$\\exists y \\in \\mathbb{N}\\ \\forall x \\in \\mathbb{N} : y > x$",
      "$\\forall x \\in \\mathbb{N}\\ \\forall y \\in \\mathbb{N} : y > x$",
      "$\\exists x \\in \\mathbb{N}\\ \\forall y \\in \\mathbb{N} : y > x$"],
     "Zu jedem $x$ ist $y = x + 1$ größer. Eine Zahl $y$, die größer als **alle** natürlichen Zahlen ist, gibt es nicht "
     "($x = y$ ist ein Gegenbeispiel). Und für $x = 1$, $y = 1$ ist $y > x$ falsch.",
     tipps=["Lies von links nach rechts: Wer wird zuerst gewählt?", "Darf $y$ von $x$ abhängen?"],
     fehler={"$\\exists y \\in \\mathbb{N}\\ \\forall x \\in \\mathbb{N} : y > x$":
             "Hier müsste **ein** $y$ größer als alle $x$ sein, auch größer als $x = y$ selbst. Die Reihenfolge der Quantoren zählt.",
             "$\\exists x \\in \\mathbb{N}\\ \\forall y \\in \\mathbb{N} : y > x$":
             "Fast: Mit $x = 1$ ist $y > 1$ für $y = 1$ falsch. Mit $\\ge$ statt $>$ wäre es wahr."})


# ── Praxis ─────────────────────────────────────────────────────────────────
# Eigenschaften: (LaTeX mit {c}, Prüffunktion, Negation, falsche Negation, Meldung zur falschen Negation)
_EIG = [
    ("x > {c}", lambda x, c: x > c, "x \\le {c}", "x < {c}", "$\\neg(x > c)$ ist $x \\le c$: Die Grenze $c$ selbst gehört zur Negation."),
    ("x \\ge {c}", lambda x, c: x >= c, "x < {c}", "x \\le {c}", "$\\neg(x \\ge c)$ ist $x < c$: Die Grenze $c$ erfüllt ja $x \\ge c$."),
    ("x < {c}", lambda x, c: x < c, "x \\ge {c}", "x > {c}", "$\\neg(x < c)$ ist $x \\ge c$: Die Grenze $c$ selbst gehört zur Negation."),
    ("x^2 \\le {c}", lambda x, c: x * x <= c, "x^2 > {c}", "x^2 \\ge {c}", "$\\neg(x^2 \\le c)$ ist $x^2 > c$, nicht $x^2 \\ge c$."),
    ("x^2 = {c}", lambda x, c: x * x == c, "x^2 \\neq {c}", "x^2 > {c}", "Die Negation von $=$ ist $\\neq$. Auch $x^2 < c$ erfüllt $x^2 \\neq c$."),
    ("2x + 1 \\neq {c}", lambda x, c: 2 * x + 1 != c, "2x + 1 = {c}", "2x + 1 < {c}", "Die Negation von $\\neq$ ist $=$."),
]
_EIG_GERADE = ("x \\text{ ist gerade}", "x \\text{ ist ungerade}")


def _menge(rng):
    a = rng.randint(-4, 2)
    return list(range(a, a + rng.randint(4, 6)))


def _mtex(m):
    return "\\{" + ", ".join(str(x) for x in m) + "\\}"


def quantor_auswerten(rng):
    m = _menge(rng)
    quantor = rng.choice(["forall", "exists"])
    if rng.random() < 0.2:
        tex = _EIG_GERADE[0]
        pruef = [x % 2 == 0 for x in m]
        einzel = [f"${x}$ ist {'gerade' if p else 'ungerade'}" for x, p in zip(m, pruef)]
    else:
        vorlage, fn, *_ = rng.choice(_EIG)
        c = rng.randint(min(m), max(m) + 1) if "x^2" not in vorlage else rng.choice([0, 1, 4, 9])
        if "2x" in vorlage:
            c = rng.choice([2 * x + 1 for x in m] + [2 * max(m) + 3])
        tex = vorlage.format(c=c)
        pruef = [fn(x, c) for x in m]
        einzel = [f"$x = {x}$: {'erfüllt' if p else 'erfüllt nicht'}" for x, p in zip(m, pruef)]
    wahr = all(pruef) if quantor == "forall" else any(pruef)
    q = "\\forall" if quantor == "forall" else "\\exists"
    if quantor == "forall":
        zeuge = next((x for x, p in zip(m, pruef) if not p), None)
        fazit = (f"Gegenbeispiel $x = {zeuge}$, also falsch." if zeuge is not None
                 else "Alle Elemente erfüllen die Eigenschaft, also wahr.")
    else:
        zeuge = next((x for x, p in zip(m, pruef) if p), None)
        fazit = (f"Beispiel $x = {zeuge}$, also wahr." if zeuge is not None
                 else "Kein Element erfüllt die Eigenschaft, also falsch.")
    return {
        "typ": "wf",
        "frage": f"Es sei $M := {_mtex(m)}$. Die Aussage ${q} x \\in M : {tex}$ ist wahr.",
        "wahr": wahr,
        "tipps": ["$\\forall$: Ein Gegenbeispiel macht die Aussage falsch. $\\exists$: Ein Beispiel macht sie wahr."],
        "rechenweg": "Jedes Element prüfen:\n\n" + "\n".join("- " + e for e in einzel) + "\n\n" + fazit,
        "erklaerung": fazit,
    }


def quantor_negieren(rng):
    menge = rng.choice(["\\mathbb{N}", "\\mathbb{Z}", "\\mathbb{R}"])
    q = rng.choice(["\\forall", "\\exists"])
    q_neu = "\\exists" if q == "\\forall" else "\\forall"
    art = rng.random()
    if art < 0.6:
        vorlage, _, neg, falsch_neg, meldung = rng.choice(_EIG)
        c = rng.randint(-3, 9)
        e, n, fn_ = vorlage.format(c=c), neg.format(c=c), falsch_neg.format(c=c)
    elif art < 0.8:                               # Konjunktion/Disjunktion (De Morgan)
        c1, c2 = rng.randint(-3, 2), rng.randint(3, 9)
        if rng.random() < 0.5:
            e, n, fn_ = f"x > {c1} \\land x < {c2}", f"x \\le {c1} \\lor x \\ge {c2}", f"x \\le {c1} \\land x \\ge {c2}"
        else:
            e, n, fn_ = f"x < {c1} \\lor x > {c2}", f"x \\ge {c1} \\land x \\le {c2}", f"x \\ge {c1} \\lor x \\le {c2}"
        meldung = "De Morgan: Beim Negieren kippt $\\land$ zu $\\lor$ und umgekehrt."
    else:                                          # Implikation
        c = rng.randint(1, 5)
        e = f"(x > {c} \\Rightarrow x^2 > {c * c})"
        n = f"x > {c} \\land x^2 \\le {c * c}"
        fn_ = f"(x > {c} \\Rightarrow x^2 \\le {c * c})"
        meldung = "Die Negation einer Implikation ist keine Implikation: $\\neg(A \\Rightarrow B) \\Leftrightarrow A \\land \\neg B$."
    richtig = f"${q_neu} x \\in {menge} : {n}$"
    optionen = [richtig, f"${q} x \\in {menge} : {n}$", f"${q_neu} x \\in {menge} : {e}$", f"${q_neu} x \\in {menge} : {fn_}$"]
    fehler = {optionen[1]: "Die Eigenschaft ist richtig negiert, aber der Quantor muss getauscht werden.",
              optionen[2]: "Der Quantor ist getauscht, aber die Eigenschaft wurde nicht negiert.",
              optionen[3]: "Der Quantor stimmt, aber die Eigenschaft ist falsch negiert. " + meldung}
    return {
        "typ": "mc",
        "frage": f"Wie lautet die Negation von ${q} x \\in {menge} : {e}$?",
        "optionen": optionen,
        "fehler": fehler,
        "tipps": ["Zwei Schritte: Quantor tauschen, Eigenschaft negieren. Die Menge bleibt.",
                  "Aus $\\forall$ wird $\\exists$ und umgekehrt.",
                  "Achte bei $<$, $\\le$ und bei $\\land$, $\\lor$, $\\Rightarrow$ auf die genaue Negation."],
        "rechenweg": f"Quantor ${q}$ wird zu ${q_neu}$. Die Eigenschaft ${e}$ wird zu ${n}$.\n\nErgebnis: {richtig}",
        "erklaerung": "$\\neg(\\forall x : E) \\Leftrightarrow \\exists x : \\neg E$ und $\\neg(\\exists x : E) \\Leftrightarrow \\forall x : \\neg E$.",
    }


k.praxis()

k.generator(quantor_auswerten, typ="wf", titel="Quantoraussage auf einer Menge prüfen")
k.generator(quantor_negieren, typ="mc", titel="Quantoraussagen negieren")

k.papier(r"""
    ## Übungsblatt-Stil: Negieren und entscheiden

    Formulieren Sie zu den folgenden Aussagen die Negation. Entscheiden Sie jeweils, ob die
    Aussage oder ihre Negation wahr ist, und begründen Sie kurz.

    a) $\forall x \in \mathbb{R}\ \exists y \in \mathbb{R} : y > x$

    b) $\exists x \in \mathbb{N}\ \forall y \in \mathbb{N} : x \le y$

    c) $\forall \varepsilon \in \mathbb{R}_{>0}\ \exists n \in \mathbb{N} : \frac{1}{n} < \varepsilon$
    """,
    r"""
    **a)** Negation: $\exists x \in \mathbb{R}\ \forall y \in \mathbb{R} : y \le x$.
    Die Aussage ist wahr: Zu jedem $x$ wähle $y := x + 1 > x$.

    **b)** Negation: $\forall x \in \mathbb{N}\ \exists y \in \mathbb{N} : x > y$.
    Die Aussage ist wahr: $x := 1$ erfüllt $1 \le y$ für alle $y \in \mathbb{N}$. (In der Negation
    scheitert $x = 1$: Es gibt kein $y \in \mathbb{N}$ mit $y < 1$.)

    **c)** Negation: $\exists \varepsilon \in \mathbb{R}_{>0}\ \forall n \in \mathbb{N} : \frac{1}{n} \ge \varepsilon$.
    Die Aussage ist wahr: Zu $\varepsilon > 0$ wähle eine natürliche Zahl $n > \frac{1}{\varepsilon}$.
    Dann ist $\frac{1}{n} < \varepsilon$. (Diese Aussage begegnet dir wieder bei Grenzwerten.)
    """,
    ["Ich habe bei jeder Aussage **alle** Quantoren getauscht und die Reihenfolge beibehalten",
     "Ich habe $>$ zu $\\le$, $\\le$ zu $>$ und $<$ zu $\\ge$ negiert",
     "Bei a) habe ich $y = x + 1$ (oder Ähnliches) als Begründung angegeben",
     "Bei b) habe ich $x = 1$ gefunden",
     "Bei c) habe ich $n$ abhängig von $\\varepsilon$ gewählt"],
    "Bei $\\forall\\ \\exists$ darf das zweite Element vom ersten abhängen. Genau das nutzt jede Begründung hier.",
    uebungsblatt=True,
    tipps=["Negiere von außen nach innen: jeden Quantor tauschen, am Ende die Ungleichung negieren."])

k.zusammenfassung(r"""
    ## Quantoren

    | Zeichen | gelesen | wahr zeigen | falsch zeigen |
    |---|---|---|---|
    | $\forall x \in M : E$ | für alle $x$ aus $M$ gilt $E$ | Argument für jedes $x$ | ein Gegenbeispiel |
    | $\exists x \in M : E$ | es gibt (mindestens) ein $x$ aus $M$ mit $E$ | ein Beispiel | Argument: kein $x$ passt |
    | $\exists! x \in M : E$ | es gibt genau ein $x$ | eins finden, Eindeutigkeit zeigen | keins oder zwei finden |
    | $\nexists x \in M : E$ | es gibt kein $x$ | Argument für jedes $x$ | ein Beispiel |

    !! $\neg(\forall x \in M : E) \Leftrightarrow \exists x \in M : \neg E$ und $\neg(\exists x \in M : E) \Leftrightarrow \forall x \in M : \neg E$.

    - Die Menge $M$ wird beim Negieren nie verändert.
    - $\neg(x > c)$ ist $x \le c$; De Morgan für $\land$, $\lor$; $\neg(A \Rightarrow B) \Leftrightarrow A \land \neg B$.
    - Reihenfolge verschiedener Quantoren nie vertauschen: $\forall x\ \exists y$ ist schwächer als $\exists y\ \forall x$.
""")
