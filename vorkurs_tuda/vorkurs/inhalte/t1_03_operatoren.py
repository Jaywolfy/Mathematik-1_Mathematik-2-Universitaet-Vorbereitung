# -*- coding: utf-8 -*-
"""Kapitel: Rechnen mit Python – Operatoren (Vorlesung 1, Folien 15–22, Livecoding 1)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="operatoren",
    titel="Rechnen mit Python – Operatoren",
    beschreibung="+ - * / // % **, Reihenfolge der Auswertung und Vergleiche",
    quelle="Vorlesung 1, Livecoding 1",
    teil="tag1",
    icon="➗")

k.lernziele([
    "Ich kann mit + - * / // % ** rechnen und weiß, welchen Typ das Ergebnis hat",
    "Ich kann mit // und % Aufgaben wie „volle Kartons und Rest“ lösen",
    "Ich kann bestimmen, in welcher Reihenfolge Python einen Ausdruck auswertet",
    "Ich kann Werte vergleichen und weiß, warum man Kommazahlen nicht mit == vergleicht",
])

# ── Erklärung 1: Die Rechenoperatoren ────────────────────────────────────
k.erklaerung("Mathematische Operatoren", r"""
    ## Python als Taschenrechner

    Ein **Operator** ist ein Rechenzeichen. Die Werte links und rechts davon
    heißen **Operanden**.

    | Operator | Bedeutung | Beispiel | Ergebnis |
    |---|---|---|---|
    | `+` | Addition | `5 + 2` | `7` |
    | `-` | Subtraktion | `5 - 2` | `3` |
    | `*` | Multiplikation | `5 * 2` | `10` |
    | `/` | Division (immer float!) | `5 / 2` | `2.5` |
    | `//` | Ganzzahl-Division (abrunden) | `5 // 2` | `2` |
    | `%` | Modulo (der Rest) | `5 % 2` | `1` |
    | `**` | Potenz | `5 ** 2` | `25` |

    :::code
    print(7 / 2)
    print(7 // 2)
    print(7 % 2)
    print(2 ** 10)
    :::

    `//` rundet immer AB, also zur kleineren Zahl hin – auch bei negativen
    Zahlen: `-7 // 2` ergibt `-4` (denn -3,5 abgerundet ist -4).
    ---
    ## Welcher Typ kommt heraus?

      • int und int ergibt int – außer bei `/`.
      • `/` liefert IMMER einen float, auch bei `4 / 2` (→ `2.0`).
      • Ist ein float beteiligt, ist das Ergebnis ein float: `1 + 2.0` → `3.0`.

    :::code
    print(4 / 2)
    print(type(1 + 2.0))
    :::

    :::achtung In anderen Sprachen ist / anders
    In C, C++ oder Java ergibt `5 / 2` mit zwei Ganzzahlen einfach `2`. In
    Python ist es `2.5`. Den Operator `//` gibt es so meist nur in Python.
    In anderen Sprachen schreibt man die Potenz oft als Funktion: `pow(5, 2)`.
    :::
    """)

k.ausgabe("print(5 / 2)", "Die normale Division / ergibt eine Kommazahl: 2.5.")
k.ausgabe("print(4 / 2)",
          "Achtung Falle! / liefert IMMER einen float – also 2.0 und nicht 2.",
          tipp="Welchen Typ liefert der Operator / immer?")
k.ausgabe("print(5 // 2)", "// teilt und rundet ab: 5 // 2 = 2 (2.5 abgerundet).")
k.ausgabe("print(-7 // 2)",
          "-7 / 2 wäre -3.5. // rundet AB, also zur kleineren Zahl: -4 (nicht -3!). "
          "Abrunden heißt bei negativen Zahlen: weiter weg von 0.",
          tipp="Welche ganze Zahl liegt direkt UNTER -3.5?")
k.ausgabe("print(5 % 2)", "5 geteilt durch 2 ist 2 Rest 1. Modulo gibt den Rest: 1.")
k.ausgabe("print(5 ** 2)", "** ist die Potenz: 5 hoch 2 = 5 · 5 = 25.")
k.ausgabe("print(type(1 + 2.0))",
          "Sobald ein float an der Rechnung beteiligt ist, ist das Ergebnis ein float "
          "(hier 3.0). Python wählt den „genaueren“ Typ.",
          akzeptiert=["float"],
          tipp="Welcher der beiden Operanden ist eine Kommazahl?")
k.mc("Was ergibt 5 / 2 in den Sprachen C oder Java (mit Ganzzahlen)?",
     ["2", "2.5", "3", "Einen Fehler"],
     "In C, C++ und Java ist die Division zweier Ganzzahlen wieder eine Ganzzahl: 2. "
     "In Python ergibt 5 / 2 dagegen 2.5.")

# ── Erklärung 2: // und % im Alltag ──────────────────────────────────────
k.erklaerung("Die drei Divisionen im Alltag", r"""
    ## Pizza, Eierkartons und übrige Eier

    :::analogie 🥚 Teilen auf drei Arten
    Du hast **20 Eier** und Kartons für je **6 Eier**.

      • `20 / 6` → `3.3333333333333335`: So viele Kartons wären es,
        wenn man Kartons zerschneiden könnte – „gerecht teilen“ wie bei Pizza.
      • `20 // 6` → `3`: So viele Kartons werden **ganz voll**.
      • `20 % 6` → `2`: So viele Eier **bleiben übrig**.

    Kontrolle: 3 volle Kartons · 6 + 2 übrige Eier = 20. Das passt immer:
    `(a // b) * b + a % b == a`.
    :::

    Noch ein Beispiel: Du hast 17 €, eine Kinokarte kostet 5 €.
    `17 // 5` → 3 Karten, `17 % 5` → 2 € bleiben übrig.
    ---
    ## Wofür braucht man Modulo (%)?

    **Teilbarkeit prüfen:** Ist der Rest 0, ist die Zahl teilbar.

        10 % 5   → 0    (10 ist durch 5 teilbar)
        7 % 2    → 1    (7 ist ungerade)
        8 % 2    → 0    (8 ist gerade)

    **Uhrzeiten:** Es ist 22 Uhr. Wie spät ist es in 5 Stunden?
    `(22 + 5) % 24` → `3`, also 3 Uhr nachts. Modulo 24 springt nach 23
    wieder auf 0 – wie das Ziffernblatt einer Uhr.

    :::achtung Teilen durch 0
    Durch 0 kann man nicht teilen – auch nicht mit `//` oder `%`:
    `7 / 0` und `7 % 0` brechen mit einem **ZeroDivisionError** ab.
    :::

    :::code
    print((22 + 5) % 24)
    print(7 % 0)
    :::
    """)

k.ausgabe("print(17 // 5)",
          "Kino-Beispiel: Mit 17 € kannst du 3 Karten zu je 5 € kaufen. 17 // 5 = 3.")
k.ausgabe("print(17 % 5)",
          "Und es bleiben 17 - 3·5 = 2 € übrig. 17 % 5 = 2.")
k.ausgabe("print(20 // 6)\nprint(20 % 6)",
          "20 Eier, Kartons für je 6 Eier: 3 volle Kartons (20 // 6 = 3), "
          "2 Eier bleiben übrig (20 % 6 = 2).",
          tipp="Wie viele volle 6er-Kartons, wie viele Eier übrig?")
k.text("20 Eier sollen in 6er-Kartons. Welchen Operator benutzt du, um die Anzahl "
       "VOLLER Kartons zu berechnen? (Nur den Operator eintippen)",
       ["//"],
       "20 // 6 = 3 volle Kartons. Für die übrigen Eier nähme man % (20 % 6 = 2).",
       tipp="Ganzzahl-Division.")
k.text("Und welchen Operator benutzt du, um zu berechnen, wie viele Eier ÜBRIG bleiben?",
       ["%"],
       "Modulo % liefert den Rest: 20 % 6 = 2.")
k.ausgabe("print((22 + 5) % 24)",
          "Uhrzeit-Rechnung: 27 % 24 = 3. Fünf Stunden nach 22 Uhr ist es 3 Uhr.")
k.ausgabe("print(7 % 0)",
          "Auch Modulo braucht eine Division – und durch 0 kann man nicht teilen. "
          "Python bricht mit einem ZeroDivisionError ab.",
          tipp="Was ist der Rest beim Teilen durch 0?")

# ── Erklärung 3: Präzedenz ───────────────────────────────────────────────
k.erklaerung("Reihenfolge der Auswertung (Operatorpräzedenz)", r"""
    ## Punkt vor Strich – und noch ein bisschen mehr

    Operatoren haben eine feste Reihenfolge, die **Operatorpräzedenz**.
    Von „zuerst“ nach „zuletzt“:

    | Rang | Operatoren | Name |
    |---|---|---|
    | 1 | `( )` | Klammern |
    | 2 | `**` | Potenz |
    | 3 | `*` `/` `//` `%` | Punktrechnung |
    | 4 | `+` `-` | Strichrechnung |
    | 5 | `==` `!=` `<` `>` `<=` `>=` | Vergleiche |
    | 6 | `not`, dann `and`, dann `or` | Logik (kommt an Tag 2) |

    !! Bei gleichem Rang rechnet Python von links nach rechts.

    So wertet Python `12 * 123 // 28 - 15` aus (`*` und `//` sind gleichrangig):

    :::visual ablauf
    {"schritte": [{"icon": "1️⃣", "text": "12 * 123 // 28 - 15"},
                  {"icon": "2️⃣", "text": "1476 // 28 - 15"},
                  {"icon": "3️⃣", "text": "52 - 15"},
                  {"icon": "✅", "text": "37"}]}
    :::

    Tipp aus der Vorlesung: Schau dir die Tabelle „Operator Precedence“ in
    der Python-Dokumentation einmal an. Und im Zweifel: **Klammern setzen!**
    """)

k.ausgabe("print(3 + 5 * 2)", "Punkt vor Strich: 5 * 2 = 10, dann 3 + 10 = 13.")
k.ausgabe("print((3 + 5) * 2)", "Klammern zuerst: 3 + 5 = 8, dann 8 * 2 = 16.")
k.ausgabe("print(2 + 3 * 4 ** 2)",
          "Potenz zuerst: 4 ** 2 = 16. Dann Punkt: 3 * 16 = 48. Dann Strich: 2 + 48 = 50.",
          tipp="Reihenfolge: **, dann *, dann +.")
k.ausgabe("print(20 - 8 - 2)",
          "Gleicher Rang → von links nach rechts: (20 - 8) - 2 = 10. "
          "Nicht 20 - (8 - 2) = 14!")
k.mc("In welcher Reihenfolge rechnet Python   8 // 3 * 2   ?",
     ["Von links nach rechts: erst 8 // 3 = 2, dann 2 * 2 = 4",
      "Erst 3 * 2 = 6, dann 8 // 6 = 1",
      "Python meldet einen Fehler, weil // und * gemischt sind",
      "Erst 8 * 2 = 16, dann 16 // 3 = 5"],
     "// und * haben den gleichen Rang. Dann wird von links nach rechts gerechnet.")

# ── Erklärung 4: Grenzen ─────────────────────────────────────────────────
k.erklaerung("Grenzen von Zahlen", r"""
    ## Wie groß, wie genau?

    **Ganzzahlen (int)** sind in Python nur durch den Arbeitsspeicher
    begrenzt. `2 ** 100` ist kein Problem:

    :::code
    print(2 ** 100)
    print(1.6e6)
    :::

    Die Kurzschreibweise `1.6e6` bedeutet 1,6 · 10⁶ = 1600000. Weil es eine
    Kommazahl-Schreibweise ist, kommt ein float heraus: `1600000.0`.

    **Fließkommazahlen (float)** sind begrenzt: Die größte ist etwa
    `1.8e308`. Rechnet man darüber hinaus, kommt meist `inf` (unendlich)
    heraus. Und floats sind nicht beliebig **genau**.

    :::info Auf Folie 19 steht …
    „In den meisten Sprachen (so auch Python) sind die darstellbaren Zahlen
    nach oben und unten begrenzt.“ Für Python gilt das genau genommen nur für
    **float**. Ganzzahlen (int) können in Python beliebig groß werden. In
    Sprachen wie Java oder C sind dagegen auch Ganzzahlen begrenzt.
    :::
    ---
    ## 0.1 + 0.2 ist nicht 0.3

    :::analogie ✏️ 1/3 auf Papier
    Schreib 1/3 als Dezimalzahl: 0,3333… Irgendwann musst du aufhören. Dann
    ergibt 0,3333 + 0,3333 + 0,3333 nur 0,9999 statt 1. Der Computer speichert
    Zahlen binär (mit 0 und 1). Darin lassen sich 0.1 und 0.2 genauso wenig
    exakt aufschreiben wie 1/3 im Dezimalsystem – es bleibt ein winziger Rest.
    :::

    :::code
    print(0.1 + 0.2)
    print(0.1 + 0.2 == 0.3)
    :::

    :::achtung Kommazahlen nie mit == vergleichen
    `0.1 + 0.2 == 0.3` ergibt **False**! Prüfe stattdessen, ob der Abstand
    winzig ist: `abs((0.1 + 0.2) - 0.3) < 0.000001` ergibt True.
    (`abs()` liefert den Betrag einer Zahl, also den Wert ohne Vorzeichen.)
    :::
    """)

k.ausgabe("print(0.1 + 0.2)",
          "Das klassische Beispiel für die begrenzte Genauigkeit von "
          "Fließkommazahlen: 0.30000000000000004.",
          tipp="Es ist NICHT einfach 0.3 ...")
k.ausgabe("print(0.1 + 0.2 == 0.3)",
          "0.1 + 0.2 ergibt 0.30000000000000004 – und das ist eben nicht genau 0.3. "
          "Deshalb ist der Vergleich False. Kommazahlen vergleicht man nicht mit ==.",
          tipp="Was kam bei 0.1 + 0.2 heraus?")
k.ausgabe("print(1.6e6)",
          "1.6e6 bedeutet 1.6 · 10^6 = 1600000. Weil es eine Kommazahl-"
          "Schreibweise ist, kommt ein float heraus: 1600000.0")
k.wf("Ganzzahlen (int) haben in Python eine feste Obergrenze – zu große Zahlen führen zu einem Fehler.",
     False,
     "In Python können ints beliebig groß werden (nur der Arbeitsspeicher begrenzt sie). "
     "2 ** 100 ergibt eine exakte 31-stellige Zahl. Begrenzt sind dagegen floats.")
k.mc("Was passiert bei   print(2 ** 100)   ?",
     ["Python gibt die exakte 31-stellige Zahl aus",
      "Python meldet einen OverflowError",
      "Python gibt inf (unendlich) aus",
      "Python gibt eine negative Zahl aus, weil die Zahl „überläuft“"],
     "Python-Ganzzahlen sind nicht begrenzt: 1267650600228229401496703205376. "
     "Ein „Überlauf“ wie in C oder Java passiert hier nicht.")

# ── Erklärung 5: Vergleiche ──────────────────────────────────────────────
k.erklaerung("Vergleichsoperatoren", r"""
    ## Vergleichen: Ja oder nein?

    Vergleichsoperatoren liefern IMMER einen Wahrheitswert (`True` oder `False`).

    | Schreibweise | Bedeutung | Beispiel | Ergebnis |
    |---|---|---|---|
    | `==` | gleich | `3 == 3` | `True` |
    | `!=` | ungleich | `5 != 5` | `False` |
    | `>` | größer als | `7 > 7` | `False` |
    | `>=` | größer gleich | `5 >= 5` | `True` |
    | `<` | kleiner als | `2 < 5` | `True` |
    | `<=` | kleiner gleich | `4 <= 4` | `True` |

    Gerechnet wird VOR dem Vergleichen: `5 * 3 > 2 - 1` → `15 > 1` → `True`.

    Teilbarkeit: `10 % 5 == 0` → `True`, denn der Rest ist 0.
    ---
    ## = oder == ?

    !! = ist eine ZUWEISUNG („leg den Wert in die Kiste“).
    !! == ist eine FRAGE („Sind die beiden gleich?“).

    (Variablen lernst du im nächsten Kapitel genauer kennen. Hier reicht:
    `y = 24` speichert den Wert 24 unter dem Namen `y`.)

    Ein Vergleich ist auch nur ein Wert – man kann ihn speichern. Bei
    `x = y == 24` rechnet Python zuerst rechts `y == 24` aus und legt das
    Ergebnis (True oder False) in `x`. `x` ist danach ein **bool**.

    :::visual variablen
    {"vars": [{"name": "y", "wert": "24", "typ": "int"}, {"name": "x", "wert": "True", "typ": "bool"}],
     "schritte": [[{"name": "y", "wert": "24", "typ": "int"}],
                  [{"name": "y", "wert": "24", "typ": "int"}, {"name": "x", "wert": "True", "typ": "bool"}]],
     "texte": ["y = 24", "x = y == 24   (rechts: 24 == 24 → True)"]}
    :::

    :::trace
    y = 24
    x = y == 24
    print(x)
    print(type(x))
    :::
    """)

k.ausgabe("print(3 == 3)\nprint(5 != 5)",
          "3 == 3 ist True. 5 != 5 fragt 'Ist 5 ungleich 5?' → False.")
k.ausgabe("print(7 > 7)\nprint(5 >= 5)",
          "7 ist nicht GRÖSSER als 7 → False. Aber 5 ist größer ODER GLEICH 5 → True.")
k.ausgabe("print(5 * 3 > 2 - 1)",
          "Erst wird gerechnet (15 und 1), dann verglichen: 15 > 1 ist True.")
k.ausgabe("print(10 % 5 == 0)",
          "10 % 5 ist 0 (kein Rest), und 0 == 0 ist True → 10 ist durch 5 teilbar.")
k.ausgabe("y = 12\nx = y * 2 == 24\nprint(x)",
          "Rechts vom = wird zuerst alles ausgerechnet: y * 2 ist 24, und 24 == 24 "
          "ist True. Dieses True landet in x.",
          tipp="Erst rechnen, dann vergleichen, dann speichern.")
k.mc("Mit welchem Ausdruck prüfst du, ob eine Zahl x gerade ist?",
     ["x % 2 == 0", "x / 2 == 0", "x // 2 == 1", "x ** 2 == 0"],
     "Gerade Zahlen lassen beim Teilen durch 2 keinen Rest: x % 2 == 0.")
k.mc("Was ist der Unterschied zwischen = und == ?",
     ["= weist einen Wert zu, == vergleicht zwei Werte",
      "Es gibt keinen Unterschied",
      "= vergleicht, == weist zu",
      "== ist nur in Java erlaubt"],
     "x = 5 legt 5 in die Variable x. x == 5 fragt: 'Ist x gleich 5?' und ergibt True/False.")
k.mc("Was liefert ein Vergleich wie 3 < 7 immer?",
     ["Einen Wahrheitswert (True oder False)", "Eine Zahl", "Einen Text", "None"],
     "Vergleichsoperatoren liefern immer einen bool.")

# ── Praxisteil ───────────────────────────────────────────────────────────
k.luecke("Ergänze die Operatoren: 20 Eier werden in 6er-Kartons verpackt. Das Programm "
         "soll erst die Anzahl voller Kartons (3) und dann die übrigen Eier (2) ausgeben.",
         """
         print(20 ___ 6)
         print(20 ___ 6)
         """,
         [["//"], ["%"]],
         "// liefert, wie oft die 6 ganz in die 20 passt (3). % liefert den Rest (2).",
         tipp="Ganzzahl-Division und Rest.")

k.code(r"""
    ## Pizza-Party

    Bei einer Party gibt es **7 Pizzen** für **3 Personen**. Lass Python
    rechnen und gib drei Zeilen aus:

      1. Wie viele Pizzen bekommt jede Person, wenn man gerecht teilt?
      2. Wie viele GANZE Pizzen bekommt jede Person?
      3. Wie viele ganze Pizzen bleiben dann übrig?

    Erwartete Ausgabe:

        2.3333333333333335
        2
        1

    Benutze nur die Zahlen 7 und 3 – die Ergebnisse darfst du nicht selbst
    eintippen.
    """,
    [P(exakt=["2.3333333333333335", "2", "1"], beschreibung="drei Zeilen"),
     P(erwartet=["2.3333333333333335"], beschreibung="gerecht geteilt mit /")],
    """
    print(7 / 3)
    print(7 // 3)
    print(7 % 3)
    """,
    "/ teilt „gerecht“ und liefert einen float. // zählt die ganzen Pizzen pro "
    "Person, % den Rest. Kontrolle: 2 · 3 + 1 = 7.",
    verboten=["1", "2"],
    tipps=["Für jede Zeile brauchst du einen der drei Divisionsoperatoren.",
           "Reihenfolge: /, dann //, dann %.",
           "print(7 / 3), print(7 // 3) und print(7 % 3)"])

k.code(r"""
    ## Teilbarkeits-Check

    Prüfe mit Python, ob das Jahr **2026**

      1. durch 4 teilbar ist (Schaltjahr-Kandidat?) und
      2. eine gerade Zahl ist.

    Gib die beiden Antworten als Wahrheitswerte untereinander aus:

        False
        True

    Benutze `%` und `==`. Die Wörter True und False darfst du nicht selbst
    hinschreiben.
    """,
    [P(exakt=["False", "True"], beschreibung="zwei Wahrheitswerte"),
     P(nicht=["0", "2"], beschreibung="Ausgabe sind Wahrheitswerte, keine Reste")],
    """
    print(2026 % 4 == 0)
    print(2026 % 2 == 0)
    """,
    "Eine Zahl ist durch 4 teilbar, wenn beim Teilen durch 4 kein Rest bleibt: "
    "2026 % 4 ist 2, also False. 2026 % 2 ist 0, also gerade → True.",
    verboten=["True", "False"],
    tipps=["Teilbar heißt: Der Rest ist 0.",
           "Den Rest bekommst du mit %, den Vergleich mit ==.",
           "print(2026 % 4 == 0) und print(2026 % 2 == 0)"])

k.code(r"""
    ## Sekunden zerlegen

    Ein Video dauert **3725 Sekunden**. Wie viele Stunden, Minuten und
    Sekunden sind das? Gib die drei Zahlen untereinander aus:

        1
        2
        5

    (1 Stunde = 3600 Sekunden, 1 Minute = 60 Sekunden.) Lass Python
    rechnen – die Ergebnisse 1, 2 und 5 darfst du nicht eintippen.
    """,
    [P(exakt=["1", "2", "5"], beschreibung="Stunden, Minuten, Sekunden")],
    """
    print(3725 // 3600)
    print(3725 % 3600 // 60)
    print(3725 % 60)
    """,
    "Stunden: 3725 // 3600 = 1. Was nach den vollen Stunden übrig bleibt, ist "
    "3725 % 3600 = 125 Sekunden – davon sind 125 // 60 = 2 volle Minuten. "
    "Die restlichen Sekunden: 3725 % 60 = 5. Achtung Präzedenz: % und // sind "
    "gleichrangig, also wird 3725 % 3600 // 60 von links nach rechts gerechnet.",
    verboten=["1", "2", "5"],
    tipps=["Volle Stunden: Wie oft passen 3600 Sekunden in 3725?",
           "Für die Minuten brauchst du erst den Rest nach den Stunden (% 3600) "
           "und davon die vollen Minuten (// 60).",
           "print(3725 // 3600), print(3725 % 3600 // 60), print(3725 % 60)"])

k.zusammenfassung(r"""
    ## Das Wichtigste aus Kapitel 3

    | Operator | Bedeutung | Beispiel |
    |---|---|---|
    | `/` | Division, immer float | `7 / 2` → `3.5` |
    | `//` | Ganzzahl-Division | `7 // 2` → `3` |
    | `%` | Rest (Modulo) | `7 % 2` → `1` |
    | `**` | Potenz | `2 ** 3` → `8` |
    | `==` `!=` `<` `>` `<=` `>=` | Vergleiche → bool | `3 == 3` → `True` |

      • Präzedenz: Klammern → `**` → `* / // %` → `+ -` → Vergleiche.
        Gleicher Rang: von links nach rechts.
      • int + float → float. Teilen durch 0 (auch `% 0`) → ZeroDivisionError.
      • int ist in Python unbegrenzt, float ist begrenzt und ungenau.

    !! 0.1 + 0.2 == 0.3 ist False – Kommazahlen nie mit == vergleichen.

        print(20 // 6, 20 % 6)    # 3 2   (volle Kartons, übrige Eier)
        x = 24 == 24              # x ist True (bool)
    """)
