# -*- coding: utf-8 -*-
"""Kapitel: Logische Operatoren – and, or, not (Vorlesung 2, Folien 5–9; Livecoding 2.1)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="logik",
    titel="Logische Operatoren – and, or, not",
    beschreibung="Vergleiche, Wahrheitswerte und Bedingungen kombinieren",
    quelle="Vorlesung 2, Livecoding 2",
    teil="tag2",
    icon="🔀")

k.lernziele([
    "Ich kann Vergleiche wie ==, !=, < und >= schreiben und ihr Ergebnis (True/False) vorhersagen",
    "Ich kann Bedingungen mit and, or und not kombinieren",
    "Ich kann eine Wahrheitstabelle lesen und selbst ausfüllen",
    "Ich kann die Reihenfolge (Präzedenz) Rechnen → Vergleich → not → and → or anwenden",
])

# ── Erklärung 1: Vergleiche ─────────────────────────────────────────────────
k.erklaerung("Vergleiche und Wahrheitswerte", r"""
    ## Fragen, auf die Python mit Ja oder Nein antwortet

    Ein **Vergleich** stellt Python eine Ja/Nein-Frage. Die Antwort ist ein
    **Wahrheitswert** vom Datentyp `bool`: entweder `True` (wahr) oder
    `False` (falsch).

    | Operator | Bedeutung | Beispiel | Ergebnis |
    |---|---|---|---|
    | `==` | gleich | `5 + 4 == 9` | `True` |
    | `!=` | ungleich | `1 != 2` | `True` |
    | `<` | kleiner | `-5 < 0` | `True` |
    | `>` | größer | `5.5 > 5.4` | `True` |
    | `<=` | kleiner oder gleich | `3 <= 2` | `False` |
    | `>=` | größer oder gleich | `4 >= 3` | `True` |

    Das Ergebnis kannst du ausgeben oder in einer Variable speichern:

    :::code
    print(5 + 4 == 10)
    print(5 + 4 == 9)
    volljaehrig = 19 >= 18
    print(volljaehrig)
    print(type(volljaehrig))
    :::
    ---
    ## Zwei Stolpersteine

    :::achtung = ist nicht ==
    Ein einzelnes `=` **speichert** einen Wert (Zuweisung). Zwei `==`
    **vergleichen** zwei Werte. `x = 5` legt 5 in x. `x == 5` fragt
    „Ist x gleich 5?“.
    :::

    :::achtung Kommazahlen sind nicht ganz genau
    Im Livecoding gab es diese Überraschung:

        print(0.1 + 0.2 == 0.3)    # False!
        print(0.1 + 0.2)           # 0.30000000000000004

    Der Computer speichert Kommazahlen im Binärsystem und muss dabei
    winzig runden. Vergleiche Kommazahlen deshalb nie mit `==`, sondern
    prüfe, ob sie „nah genug“ beieinander liegen.
    :::

    Auch `True` und `False` schreibst du immer mit großem Anfangsbuchstaben.
    `true` kennt Python nicht (NameError).
    """)

k.ausgabe("print(5 + 4 == 10)",
          "Erst wird gerechnet: 5 + 4 = 9. Dann wird verglichen: 9 == 10 ist falsch → False.")
k.ausgabe("print(0.1 + 0.2 == 0.3)",
          "Überraschung aus dem Livecoding: 0.1 + 0.2 ergibt 0.30000000000000004. Das ist "
          "nicht exakt 0.3 → False. Kommazahlen werden intern gerundet gespeichert.",
          tipp="Rechne nicht im Kopf, sondern denk daran, wie der Computer Kommazahlen speichert.")
k.wf("Der Ausdruck   x = 5   prüft, ob x gleich 5 ist.", False,
     "Ein einfaches `=` ist eine **Zuweisung**: Es legt 5 in x. Vergleichen geht mit `==`.")
k.mc("Welchen Datentyp hat das Ergebnis von   3 < 7  ?",
     ["bool", "int", "str", "float"],
     "Ein Vergleich liefert immer einen Wahrheitswert: `True` oder `False`. Dieser Datentyp "
     "heißt `bool`.")

# ── Erklärung 2: and, or, not ───────────────────────────────────────────────
k.erklaerung("and, or, not", r"""
    ## Bedingungen kombinieren

    Wie prüft man, ob x zwischen 3 und 7 liegt? Dafür braucht man ZWEI
    Vergleiche: `3 < x` und `x < 7`. Verbunden werden sie mit
    **logischen Operatoren**. Sie arbeiten auf dem Datentyp `bool`: Sie
    nehmen Wahrheitswerte und liefern wieder einen Wahrheitswert.

    | Operator | Ergebnis ist True, wenn … | Beispiel |
    |---|---|---|
    | `and` | BEIDE Seiten True sind | `is_car and is_boat` |
    | `or` | MINDESTENS EINE Seite True ist | `is_car or is_boat` |
    | `not` | der Wert False ist (dreht um) | `not is_car` |

    Beispiel aus der Vorlesung: Ein regnerischer Tag hat Wolken UND Regen.

    :::code
    raining = False
    cloudy = True
    rainyday = raining and cloudy
    print(rainyday)
    print(raining or cloudy)
    print(not raining)
    :::
    ---
    ## Der Club an der Ecke

    :::analogie 🚪 Die Tür zum Club
    Am Eingang eines Clubs stehen drei Regeln:

      • **and**: „Du kommst nur rein, wenn du einen Ausweis hast UND auf
        der Gästeliste stehst.“ Fehlt eins von beiden, bleibt die Tür zu.
      • **or**: „Für die Garderobe brauchst du eine Jacke ODER eine Tasche.“
        Eins reicht. Hast du beides, darfst du trotzdem abgeben. Das
        Python-`or` ist also kein „entweder-oder“.
      • **not**: „Wer NICHT nüchtern ist, fliegt raus.“ `not` dreht die
        Antwort einfach um, wie ein Lichtschalter.

    Kim hat einen Ausweis (True), steht aber nicht auf der Liste (False):
    `True and False` ergibt `False`. Kim bleibt draußen.
    :::
    ---
    ## Wahrheitstabellen

    Eine **Wahrheitstabelle** zeigt für alle Kombinationen von a und b,
    was herauskommt. Bei zwei Variablen gibt es genau 4 Zeilen.

    :::visual wahrheitstabelle
    {"variablen": ["a", "b"], "ausdruecke": ["a and b", "a or b", "not a"]}
    :::

    !! and ist nur True, wenn BEIDE True sind. or ist nur False, wenn BEIDE False sind.
    """)

k.ausgabe("print(True and False)", "and braucht BEIDE Seiten als True. Eine ist False → False.")
k.ausgabe("print(True or False)", "or braucht nur EINE Seite als True → True.")
k.ausgabe("print(not True)", "not dreht den Wert um: aus True wird False.")
k.ausgabe("print(False or False)", "Keine der beiden Seiten ist True → False.")
k.ausgabe("raining = False\ncloudy = True\nrainyday = raining and cloudy\nprint(rainyday)",
          "Es regnet nicht (False). `False and …` ist immer False, egal was rechts steht.")
k.wf("x or y ist nur dann True, wenn GENAU EINER von beiden True ist.", False,
     "`or` ist True, wenn MINDESTENS einer True ist, also auch, wenn beide True sind. "
     "Das umgangssprachliche „entweder-oder“ ist etwas anderes.")
k.mc("Mit welcher Bedingung prüfst du, ob x zwischen 3 und 7 liegt (3 und 7 nicht eingeschlossen)?",
     ["3 < x and x < 7", "3 < x or x < 7", "not 3 < x", "3 > x and x > 7"],
     "Beide Bedingungen müssen gelten → `and`. Mit `or` wäre zum Beispiel auch x = 100 "
     "„drin“, weil 3 < 100 gilt. Python erlaubt übrigens auch die Kurzform `3 < x < 7`.")
k.mc("Kino: Einlass ab 18 ODER in Begleitung eines Erwachsenen. Welche Bedingung passt?",
     ["alter >= 18 or begleitet", "alter >= 18 and begleitet",
      "not alter >= 18", "alter > 18 and not begleitet"],
     "Eins von beiden reicht → `or`. Mit `and` müssten auch Volljährige jemanden mitbringen.")
k.mc("Ben möchte prüfen, ob die Variable wahl gleich 1 oder gleich 2 ist. Welche Bedingung ist richtig?",
     ["wahl == 1 or wahl == 2", "wahl == 1 or 2", "wahl == (1 or 2)", "wahl == 1 and wahl == 2"],
     "Jede Seite von `or` muss ein vollständiger Vergleich sein. `wahl == 1 or 2` bedeutet "
     "`(wahl == 1) or 2`, und die 2 zählt als „wahr“. Die Bedingung wäre also IMMER erfüllt. "
     "`and` geht auch nicht: wahl kann nicht gleichzeitig 1 und 2 sein.",
     tipp="Schreibe auf beide Seiten von or einen ganzen Vergleich.")

# ── Erklärung 3: Präzedenz ──────────────────────────────────────────────────
k.erklaerung("Reihenfolge (Präzedenz) und XOR", r"""
    ## Was wird zuerst ausgewertet?

    Wie bei „Punkt vor Strich“ gibt es eine feste Reihenfolge, die
    **Präzedenz**. Von „zuerst“ nach „zuletzt“:

    | Rang | Was | Beispiele |
    |---|---|---|
    | 1 | Klammern | `( … )` |
    | 2 | Rechnen | `*`, `/`, `//`, `%`, dann `+`, `-` |
    | 3 | Vergleiche | `==`, `!=`, `<`, `>`, `<=`, `>=` |
    | 4 | `not` | `not a` |
    | 5 | `and` | `a and b` |
    | 6 | `or` | `a or b` |

    Merkhilfe: `and` ist wie „mal“, `or` ist wie „plus“. Deshalb bindet
    `and` stärker.

        True or False and False
        = True or (False and False)
        = True or False
        = True

    Weil Vergleiche vor `not` kommen, bedeutet `not x == y` dasselbe wie
    `not (x == y)`.

    !! Im Zweifel: Klammern setzen! Das macht den Code auch für Menschen lesbarer.
    ---
    ## Schritt für Schritt (Beispiel aus der Vorlesung)

    :::trace
    x = 10
    a = (x == 60)
    b = 5 > 3
    print(not (a or b))
    print(b or (x > 50) and a)
    :::

    In der letzten Zeile wird zuerst `(x > 50) and a` ausgewertet
    (`False and False` = `False`). Danach `b or False` = `True`.
    ---
    ## Bonus aus dem Livecoding: XOR mit ^

    :::info Entweder-oder: der Operator ^
    Im Livecoding kam noch `^` vor. Bei Wahrheitswerten bedeutet es
    **XOR** („exklusives Oder“): Ergebnis True, wenn GENAU EINE Seite
    True ist.

        print(True ^ False)    # True
        print(True ^ True)     # False

    Bei `True` und `False` liefert `a ^ b` dasselbe wie `a != b`. Auf den
    Folien steht `^` nicht. Für den Vorkurs reichen `and`, `or`, `not`.
    :::

    :::achtung ^ ist KEIN Hoch-Zeichen
    `2 ^ 3` ist in Python **nicht** 8. Potenzieren geht mit `**`, also
    `2 ** 3`. Bei ganzen Zahlen rechnet `^` mit den Bits und liefert hier 1.
    :::
    """)

k.ausgabe("x = 10\na = (x == 60)\nb = 5 > 3\nprint(not (a or b))",
          "a = (10 == 60) = False, b = (5 > 3) = True. Die Klammer zuerst: a or b = True. "
          "not True = False. (Beispiel aus Vorlesung 2)")
k.ausgabe("x = 10\na = (x == 60)\nb = 5 > 3\nprint(b or (x > 50) and a)",
          "and zuerst: (x > 50) and a = False and False = False. Dann b or False = "
          "True or False = True.")
k.ausgabe("print(True or False and False)",
          "and bindet stärker: True or (False and False) = True or False = True.")
k.ausgabe("print(not False and False)",
          "not zuerst: (not False) = True. Dann True and False = False.")
k.mc("Was wird in   a or b and c   zuerst ausgewertet?",
     ["b and c", "a or b", "Alles gleichzeitig", "Von rechts nach links: c zuerst allein"],
     "and bindet stärker als or (wie mal vor plus): `a or (b and c)`.")
k.ausgabe("x = 3\ny = 4\nprint(not x == y)",
          "Vergleiche kommen VOR not. Also `not (x == y)` = `not (3 == 4)` = `not False` = True.",
          tipp="Was wird zuerst ausgewertet: der Vergleich oder das not?")
k.ausgabe("print(True ^ True)",
          "^ ist XOR (entweder-oder): True nur, wenn GENAU eine Seite True ist. Hier sind beide "
          "True → False.")
k.wf("Logische Operatoren arbeiten auf dem Datentyp bool.", True,
     "Ja: Sie kombinieren oder verändern Wahrheitswerte. Das unterscheidet sie von "
     "den Rechenoperatoren.")

# ── Praxisteil ──────────────────────────────────────────────────────────────
k.luecke("Vervollständige die Wahrheitstabelle für   a or b  . Schreibe True oder False in die Lücken.",
         """
         # a      b      a or b
         # True   True   ___
         # True   False  ___
         # False  True   ___
         # False  False  ___
         """,
         [["True"], ["True"], ["True"], ["False"]],
         "`or` ist nur dann False, wenn BEIDE Seiten False sind. In allen anderen Zeilen ist "
         "es True, auch in der ersten (beide True).",
         tipp="Bei or reicht EINE wahre Seite.")

k.code(r"""
    ## Zwischen 3 und 7?

    Lies eine ganze Zahl `x` ein. Gib `True` aus, wenn x **echt** zwischen
    3 und 7 liegt (3 und 7 selbst zählen nicht), sonst `False`.
    Benutze `and` (noch kein `if` nötig: ein Vergleich liefert schon True/False).

        Eingabe:  5      Ausgabe:  True
        Eingabe:  7      Ausgabe:  False
    """,
    [P(["5"], ["True"], nicht=["False"]),
     P(["3"], ["False"], nicht=["True"], beschreibung="Randfall: 3 zählt nicht"),
     P(["7"], ["False"], nicht=["True"], beschreibung="Randfall: 7 zählt nicht"),
     P(["6"], ["True"], nicht=["False"]),
     P(["100"], ["False"], nicht=["True"]),
     P(["-4"], ["False"], nicht=["True"])],
    """
    x = int(input("Zahl: "))
    print(3 < x and x < 7)
    """,
    "`3 < x and x < 7` ist nur True, wenn beide Vergleiche stimmen. Mit `<=` wären 3 und 7 "
    "fälschlich dabei. Mit `or` wäre fast jede Zahl „dazwischen“.",
    tipps=["Du brauchst zwei Vergleiche: einen mit 3 und einen mit 7.",
           "Verbinde `3 < x` und `x < 7` mit dem passenden logischen Operator.",
           "print(3 < x and x < 7)"],
    pflicht=["and"],
    vorlage="x = int(input(\"Zahl: \"))\n",
    streng=True)

k.code(r"""
    ## Kino-Einlass

    Lies zuerst das Alter (ganze Zahl) und dann `ja` oder `nein` ein (ist
    eine erwachsene Begleitung dabei?). Gib `True` aus, wenn die Person
    in den Film darf, sonst `False`. Regel: ab 18 Jahren ODER mit Begleitung.

        Eingaben:  16, ja      Ausgabe:  True
        Eingaben:  16, nein    Ausgabe:  False
    """,
    [P(["18", "nein"], ["True"], nicht=["False"], beschreibung="genau 18 reicht"),
     P(["16", "ja"], ["True"], nicht=["False"]),
     P(["16", "nein"], ["False"], nicht=["True"]),
     P(["30", "ja"], ["True"], nicht=["False"], beschreibung="beides erfüllt"),
     P(["17", "nein"], ["False"], nicht=["True"])],
    """
    alter = int(input("Alter: "))
    begleitet = input("Begleitung (ja/nein): ") == "ja"
    print(alter >= 18 or begleitet)
    """,
    "`input(...) == \"ja\"` ist selbst schon ein Wahrheitswert. Dann reicht `or`: Eine der "
    "beiden Bedingungen genügt. Achte auf `>=`, damit 18-Jährige auch reindürfen.",
    tipps=["Speichere die zweite Eingabe als Wahrheitswert: Vergleiche sie mit \"ja\".",
           "Eine der beiden Bedingungen reicht – welcher Operator passt?",
           "print(alter >= 18 or begleitet)"],
    streng=True)

k.code(r"""
    ## Schaltjahr-Prüfer

    Lies eine Jahreszahl ein und gib `True` aus, wenn es ein Schaltjahr
    ist, sonst `False`. Die Regel:
      • durch 4 teilbar UND nicht durch 100 teilbar, ODER
      • durch 400 teilbar.

    Teilbar heißt: Der Rest der Division ist 0, also `jahr % 4 == 0`.

        2024 → True     1900 → False     2000 → True     2023 → False
    """,
    [P(["2024"], ["True"], nicht=["False"]),
     P(["1900"], ["False"], nicht=["True"], beschreibung="durch 100, aber nicht durch 400"),
     P(["2000"], ["True"], nicht=["False"], beschreibung="durch 400 teilbar"),
     P(["2023"], ["False"], nicht=["True"]),
     P(["2100"], ["False"], nicht=["True"])],
    """
    jahr = int(input("Jahr: "))
    schaltjahr = (jahr % 4 == 0 and jahr % 100 != 0) or jahr % 400 == 0
    print(schaltjahr)
    """,
    "Die Klammern sind hier nicht nötig (and bindet ohnehin stärker als or), machen die "
    "Regel aber viel besser lesbar. 1900 ist durch 4 und durch 100 teilbar, aber nicht "
    "durch 400 → kein Schaltjahr.",
    tipps=["Teilbarkeit prüfst du mit dem Rest: `jahr % 4 == 0`.",
           "Der erste Teil: `jahr % 4 == 0 and jahr % 100 != 0`. Wie hängst du den 400er-Fall an?",
           "(jahr % 4 == 0 and jahr % 100 != 0) or jahr % 400 == 0"],
    streng=True)

k.zusammenfassung(r"""
    ## Logik auf einen Blick

    | Ausdruck | True, wenn … |
    |---|---|
    | `a and b` | beide True |
    | `a or b` | mindestens einer True (auch beide) |
    | `not a` | a False ist |
    | `a ^ b` (Bonus, XOR) | genau einer True |

    Reihenfolge: **Klammern → Rechnen → Vergleiche → not → and → or**

        3 < x and x < 7          # liegt x zwischen 3 und 7?
        wahl == 1 or wahl == 2   # NICHT: wahl == 1 or 2
        not x == y               # bedeutet not (x == y)

    !! `=` speichert, `==` vergleicht. `True`/`False` immer groß schreiben.
    !! Kommazahlen nicht mit == vergleichen: 0.1 + 0.2 == 0.3 ist False.
    """)
