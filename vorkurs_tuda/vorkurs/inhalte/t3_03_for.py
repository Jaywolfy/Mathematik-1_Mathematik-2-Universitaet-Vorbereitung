# -*- coding: utf-8 -*-
"""Kapitel: for-Schleifen, range, enumerate, zip (Vorlesung 3, Folien 12–23; Livecoding 3.2)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="for_schleifen",
    titel="for-Schleifen, range, enumerate, zip",
    beschreibung="Bequem über Listen, Strings und Zahlenbereiche laufen",
    quelle="Vorlesung 3, Livecoding 3",
    teil="tag3",
    icon="🔂")

k.lernziele([
    "Ich kann mit for jedes Element einer Liste, eines Strings oder Dictionaries durchgehen",
    "Ich kann mit range(start, stop, step) Zahlenfolgen erzeugen, auch rückwärts",
    "Ich kann mit enumerate() Index und Element und mit zip() zwei Listen gleichzeitig durchlaufen",
    "Ich kann in einer Schleife ein Ergebnis aufbauen (Summe, Produkt, Liste, Zähl-Dictionary)",
])

# ── Erklärung 1: for-each ────────────────────────────────────────────────
k.erklaerung("Die for-Schleife", r"""
    ## Warum noch eine Schleife?

    Häufig will man über eine Liste oder einen String **iterieren**, also
    jedes Element der Reihe nach bearbeiten. Mit `while` muss man dafür selbst
    hochzählen. Die Folie sagt: **„Manuelles Hochzählen ist unpraktisch und ein
    Vergessen resultiert in Endlosschleifen.“**

    :::vergleich while (selbst zählen) | for (Python zählt)
    Drei Zeilen kümmern sich nur ums Zählen:
        i = 0
        s = 'Lorem'
        while i < len(s):
            print(f'Buchstabe an Stelle {i}: {s[i]}')
            i += 1
    |||
    Das Zählen übernimmt `range()`:
        s = 'Lorem'
        for i in range(len(s)):
            print(f'Buchstabe an Stelle {i}: {s[i]}')
    :::

    Der grundsätzliche Aufbau:

        for var in <iterable>:
            do_something(var)

    *Iterable* (durchlaufbar) ist alles, was man Element für Element
    durchgehen kann: Listen, Strings, Tupel, Dictionaries und `range(...)`.
    ---
    ## for-each: jedes Element durchgehen

    :::analogie 🍽️ Für jeden Teller im Stapel: abwaschen
    Du stehst vor einem Stapel Teller (der Liste).
      • Du nimmst **einen Teller nach dem anderen** in die Hand. Der Teller in
        deiner Hand ist die Schleifenvariable.
      • Mit jedem Teller machst du dasselbe: abwaschen (der eingerückte Körper).
      • Du musst **nicht mitzählen**, welcher Teller dran ist.
      • Ist der Stapel leer, bist du fertig, und es geht mit dem Code nach der
        Schleife weiter.
    :::

        einkauf = ["Milch", "Brot", "Eier"]
        for artikel in einkauf:
            print(f"Nicht vergessen: {artikel}")

    Der Name nach `for` (hier `artikel`) ist frei wählbar. In jeder Runde
    steckt darin das nächste Element. Bei einem String ist es das nächste Zeichen.

    :::visual schleife
    {"titel": "Ablauf einer for-Schleife", "bedingung": "artikel in einkauf",
     "koerper": ["print(f\"Nicht vergessen: {artikel}\")"],
     "danach": "print(\"Fertig!\")", "art": "for"}
    :::
    ---
    ## Schritt für Schritt: eine Summe aufbauen

    :::visual variablen
    {"titel": "for x in [3, 5, 2]: summe += x",
     "schritte": [
       [{"name": "summe", "wert": "0", "typ": "int"}],
       [{"name": "summe", "wert": "0", "typ": "int"}, {"name": "x", "wert": "3", "typ": "int"}],
       [{"name": "summe", "wert": "3", "typ": "int"}, {"name": "x", "wert": "3", "typ": "int"}],
       [{"name": "summe", "wert": "3", "typ": "int"}, {"name": "x", "wert": "5", "typ": "int"}],
       [{"name": "summe", "wert": "8", "typ": "int"}, {"name": "x", "wert": "5", "typ": "int"}],
       [{"name": "summe", "wert": "8", "typ": "int"}, {"name": "x", "wert": "2", "typ": "int"}],
       [{"name": "summe", "wert": "10", "typ": "int"}, {"name": "x", "wert": "2", "typ": "int"}]],
     "texte": ["`summe = 0` vor der Schleife",
               "Runde 1: x bekommt das erste Element, 3",
               "`summe += x` → 0 + 3 = 3",
               "Runde 2: x bekommt 5",
               "`summe += x` → 3 + 5 = 8",
               "Runde 3: x bekommt 2",
               "`summe += x` → 8 + 2 = 10. Keine Elemente mehr, die Schleife ist fertig."]}
    :::

    :::trace
    summe = 0
    for x in [3, 5, 2]:
        summe += x
    print(summe)
    :::

    :::achtung Die Schleifenvariable IST schon das Element
    Bei `for x in zahlen:` ist `x` der Wert, nicht der Index. `zahlen[x]`
    ist dann meistens falsch und gibt oft einen `IndexError`. Brauchst du den
    Index, nimm `range(len(zahlen))` oder `enumerate(zahlen)`.
    :::
    """)

k.ausgabe("for c in 'abc':\n    print(c)", "for-each über einen String: jedes Zeichen einzeln.")
k.mc("Was ist der Hauptvorteil von for gegenüber while beim Durchlaufen einer Liste?",
     ["Man kann das Hochzählen des Index nicht vergessen",
      "for ist immer schneller",
      "while kann keine Listen durchlaufen",
      "for braucht keine Einrückung"],
     "Bei for kümmert sich Python ums Weiterzählen – keine vergessenen i += 1 und keine "
     "Endlosschleifen dadurch.")
k.ausgabe("summe = 0\nfor x in [10, 2, 7, 4, 3, 5, 8]:\n    summe += x\nprint(summe)",
          "10 + 2 + 7 + 4 + 3 + 5 + 8 = 39.")
k.ausgabe("quadrate = []\nfor x in [1, 2, 3]:\n    quadrate.append(x ** 2)\nprint(quadrate)",
          "Für jedes Element wird das Quadrat hinten angehängt.")
k.ausgabe("zahlen = [10, 20, 30]\nfor x in zahlen:\n    print(zahlen[x])",
          "x ist das ELEMENT (10, 20, 30), nicht der Index. zahlen[10] gibt es nicht → "
          "IndexError. Richtig wäre einfach print(x).",
          tipp="Welchen Wert hat x in der ersten Runde?")

# ── Erklärung 2: range ───────────────────────────────────────────────────
k.erklaerung("range(): Zahlenfolgen", r"""
    ## for-range statt while

    Die Zählschleife mit while aus Tag 2 …

        i = 0
        while i < len(s):
            print(s[i])
            i += 1

    … wird mit `range()` viel kürzer. **Hierbei kann man das Hochzählen des
    Index nicht vergessen.**

        for i in range(len(s)):
            print(s[i])

    (Auf Folie 18 steht `while i < num:`. `num` ist dort nicht definiert,
    gemeint ist `len(s)`.)
    ---
    ## range(start, stop, step) funktioniert wie Slices

    Allgemein: `range(start, stop, step)`. Wie beim Slicing ist **start dabei,
    stop nicht mehr**. Lässt man etwas weg, gilt: start = 0, step = 1.

        lst = [9, 1, 8, 6, 7, 2, 1, 8]
        lst[1:7:2]               # → [1, 6, 2]  Werte an den Indizes 1, 3, 5
        list(range(1, 7, 2))     # → [1, 3, 5]  genau diese Indizes

    | Aufruf | Zahlen |
    |---|---|
    | `range(5)` | 0, 1, 2, 3, 4 |
    | `range(2, 6)` | 2, 3, 4, 5 |
    | `range(1, 7, 2)` | 1, 3, 5 |
    | `range(len("Lorem"))` | 0, 1, 2, 3, 4 |

    `range()` liefert keine Liste. Zum Anschauen wandelt man es mit `list()` um.

    :::code
    for i in range(10):
        print(i)
    print(list(range(2, 6)))
    :::
    """)

k.ausgabe("print(list(range(5)))", "range(5) liefert 0 bis 4 – die 5 ist exklusiv.")
k.ausgabe("print(list(range(2, 6)))", "Von 2 bis VOR 6: [2, 3, 4, 5].")
k.ausgabe("s = 'Lorem'\nfor i in range(len(s)):\n    print(s[i])",
          "range(len(s)) ist range(5) → i = 0, 1, 2, 3, 4. So bekommt man jeden Buchstaben.")
k.mc("Welche Zahlen durchläuft   for i in range(3, 10, 3):  ?",
     ["3, 6, 9", "3, 6, 9, 12", "3, 4, 5, 6, 7, 8, 9", "0, 3, 6, 9"],
     "Start 3, dann +3 → 6, +3 → 9. 12 ist nicht mehr kleiner als 10.")

# ── Erklärung 3: Schrittweite ────────────────────────────────────────────
k.erklaerung("Schrittweite und rückwärts zählen", r"""
    ## Hüpfen auf dem Zahlenstrahl

    Stell dir `range` als Hüpfspiel vor: Du startest am Pfosten **start**,
    springst immer **step** weit und darfst den Zaun bei **stop** nie
    betreten. Schiebe die Regler und probiere es aus:

    :::visual zahlenstrahl
    {"titel": "range(2, 10, 3) auf dem Zahlenstrahl", "start": 2, "stop": 10, "step": 3,
     "interaktiv": true}
    :::

    Beispiele aus dem Livecoding:

        for i in range(2, 10, 3):
            print(i)              # 2, 5, 8
        for i in range(10, 2, -3):
            print(i)              # 10, 7, 4   (negativer Schritt: rückwärts!)

    Bei negativem Schritt muss start **größer** als stop sein. Auch hier ist
    stop nicht dabei: Nach 4 käme 1, aber 1 liegt schon hinter dem Zaun bei 2.
    ---
    ## Typische Fehler

    :::achtung Um eins daneben
    Du willst 1 bis n? Dann brauchst du `range(1, n + 1)`, denn stop ist
    nicht dabei. `range(1, n)` hört bei n − 1 auf.

    Rückwärts ohne negativen Schritt geht nicht: `range(10, 0)` ist **leer**,
    weil man von 10 mit +1 nie unter 0 kommt. Richtig: `range(10, 0, -1)`.
    :::

    :::code
    print(list(range(1, 5)))
    print(list(range(1, 5 + 1)))
    print(list(range(10, 0)))
    print(list(range(10, 0, -1)))
    :::
    """)

k.ausgabe("print(list(range(1, 7, 2)))", "Von 1 bis vor 7 in 2er-Schritten: [1, 3, 5].")
k.ausgabe("for i in range(1, 8, 3):\n    print(i)",
          "Quiz aus Vorlesung 3: 1, dann 1 + 3 = 4, dann 4 + 3 = 7. Die 10 wäre zu groß.",
          tipp="Start 1, Schrittweite 3, Ende 8 (exklusiv).")
k.ausgabe("for i in range(2, 10, 3):\n    print(i)",
          "Livecoding: Start 2, dann 5, dann 8. Die 11 wäre schon hinter dem Zaun bei 10.",
          tipp="Start 2, immer +3, Stop 10 ist nicht dabei.")
k.ausgabe("for i in range(10, 2, -3):\n    print(i)",
          "Livecoding: Rückwärts in 3er-Schritten: 10, 7, 4. Die 1 wäre schon kleiner als "
          "der Stop 2.",
          tipp="Negativer Schritt: Es geht rückwärts, solange die Zahl größer als 2 ist.")
k.ausgabe("print(list(range(10, 0, -3)))",
          "Rückwärts in 3er-Schritten: 10, 7, 4, 1. (-2 wäre schon hinter der 0.)")

# ── Erklärung 4: enumerate, zip, dict ────────────────────────────────────
k.erklaerung("enumerate(), zip() und Dictionaries", r"""
    ## enumerate(): Index UND Element

    Manchmal braucht man zum Element auch seinen Index, will aber keine
    range-Schleife schreiben. `enumerate()` liefert in jeder Runde ein Tupel
    `(index, element)`, das direkt ausgepackt wird:

        for i, c in enumerate("Hi!"):
            print(i, c)

    | Runde | i | c | Ausgabe |
    |---|---|---|---|
    | 1 | 0 | `'H'` | `0 H` |
    | 2 | 1 | `'i'` | `1 i` |
    | 3 | 2 | `'!'` | `2 !` |

    Alltag: Startnummern beim Marathon. Alle Laufenden bekommen der Reihe
    nach eine Nummer, ab 0.

    Im Livecoding liefern beide Schleifen dieselbe Ausgabe:

    :::code
    a = [6, 9, 1, 2]
    for i in range(len(a)):
        print(f'Element an Index {i} ist {a[i]}')
    for k, e in enumerate(a):
        print(f'Element an Index {k} ist {e}')
    :::
    ---
    ## zip(): zwei Listen gleichzeitig

    `zip()` arbeitet wie ein **Reißverschluss**: Es nimmt immer ein Element
    von links und eins von rechts und macht daraus ein Paar.

        a = [6, 9, 1, 2]
        b = [1, 3, 2, 4]
        for i, j in zip(a, b):
            print(i + j)

    | Runde | i (aus a) | j (aus b) | i + j |
    |---|---|---|---|
    | 1 | 6 | 1 | 7 |
    | 2 | 9 | 3 | 12 |
    | 3 | 1 | 2 | 3 |
    | 4 | 2 | 4 | 6 |

    :::info Auf der Folie steht „zwei gleich lange Listen“
    zip funktioniert auch bei **unterschiedlich langen** Listen. Es hört dann
    bei der **kürzeren** auf, der Rest der längeren wird ignoriert (wie beim
    Tanzen: Wer keinen Partner hat, tanzt nicht mit).
        list(zip([1, 2, 3], [4, 5]))    # → [(1, 4), (2, 5)]
    :::
    ---
    ## Dictionaries durchlaufen

    Läuft man mit for über ein Dictionary, bekommt man die **Schlüssel**
    (Folie 22):

        for key in dictionary:
            value = dictionary[key]

    Bequemer geht es mit `items()`, das liefert gleich beide (Livecoding 3.1):

    :::code
    lager = {"Äpfel": 3, "Birnen": 0, "Kiwis": 5}
    for key in lager:
        print(key)
    for artikel, anzahl in lager.items():
        print(f"{artikel}: {anzahl} Stück")
    :::
    """)

k.ausgabe("for i, c in enumerate('hi'):\n    print(i, c)",
          "enumerate liefert Paare aus Index und Element: (0, 'h') und (1, 'i').")
k.mc("Du brauchst in der Schleife Index UND Element einer Liste. Was ist am elegantesten?",
     ["for i, x in enumerate(liste):",
      "for i, x in zip(liste):",
      "for i in liste.index():",
      "while liste:"],
     "enumerate liefert Paare aus Index und Element.")
k.ausgabe('namen = ["Ali", "Bea"]\nnoten = [2, 1]\nfor n, x in zip(namen, noten):\n    print(n, x)',
          "zip fügt die Listen paarweise zusammen: (Ali, 2) und (Bea, 1).")
k.ausgabe("print(list(zip([1, 2, 3], [4, 5])))",
          "zip hört bei der kürzeren Liste auf. Die 3 hat keinen Partner und fällt weg: "
          "[(1, 4), (2, 5)].",
          tipp="Wie viele Paare kann ein Reißverschluss bilden, wenn eine Seite nur 2 Zähne hat?")
k.ausgabe('lager = {"Äpfel": 3, "Birnen": 0, "Kiwis": 5}\nfor k in lager:\n'
          '    if lager[k] == 0:\n        print(k, "nachbestellen")',
          "Die Schleife geht alle Schlüssel durch. Nur bei Birnen ist der Bestand 0.")
k.ausgabe("d = {'Anna': 19, 'Ben': 21}\nfor name, alter in d.items():\n    print(f'{name} ist {alter}')",
          "items() liefert die Paare ('Anna', 19) und ('Ben', 21). Sie werden in name und "
          "alter ausgepackt.")

# ── Erklärung 5: Muster ──────────────────────────────────────────────────
k.erklaerung("Muster: Ergebnisse aufbauen und suchen", r"""
    ## Das Akkumulator-Muster

    Oft gibt es eine Variable, in der das Ergebnis **langsam aufgebaut** wird
    (der *Akkumulator*, auf Deutsch „Sammler“). Sie bekommt vor der Schleife
    einen Startwert und wird in jeder Runde verändert. Wie ein Einkaufswagen
    an der Kasse: Die Summe startet bei 0, und jeder Artikel kommt dazu.

    | Was baust du auf? | Startwert | in der Schleife |
    |---|---|---|
    | Summe | `summe = 0` | `summe += x` |
    | Produkt | `produkt = 1` | `produkt *= x` |
    | Liste | `ergebnis = []` | `ergebnis.append(...)` |
    | Text | `text = ""` | `text += ...` |
    | Zählung | `anzahl = {}` | `anzahl[x] = anzahl.get(x, 0) + 1` |

    !! Ein Produkt muss bei 1 starten. Mit 0 wäre alles 0!

    Mehrere Akkumulatoren passen in **eine** Schleife. Genau das übst du im
    Kapitel „Übungsblatt 3“ (Aufgabe 1.3).
    ---
    ## Suchen und abbrechen

    Fakultät: n! = 1 · 2 · 3 · … · n, z. B. 5! = 120. Ein Produkt-Akkumulator:

        ergebnis = 1
        for i in range(1, n + 1):
            ergebnis *= i

    Suchen: Probiere alle Kandidaten durch. Sobald einer passt, ist man fertig.
    `break` beendet die Schleife sofort (bekannt aus Tag 2). So prüft man z. B.,
    ob eine Zahl einen Teiler hat (Idee für die Primzahl-Aufgabe):

    :::code
    n = 91
    teiler_gefunden = False
    for t in range(2, n):
        if n % t == 0:
            print("Teiler gefunden:", t)
            teiler_gefunden = True
            break
    print(teiler_gefunden)
    :::

    `break` und `continue` wirken immer nur auf die **innerste** Schleife.
    """)

k.mc("Welchen Startwert braucht eine Variable, in der ein PRODUKT aufgebaut wird?",
     ["1", "0", "None", "Eine leere Liste"],
     "Mit 0 wäre jedes Produkt 0. Die 1 verändert beim Multiplizieren nichts.")
k.ausgabe("produkt = 0\nfor x in [10, 2, 7]:\n    produkt *= x\nprint(produkt)",
          "Klassischer Fehler: Startwert 0! 0 · irgendwas = 0. Ein Produkt muss bei 1 starten.",
          tipp="Was ist 0 mal irgendwas?")
k.ausgabe("ergebnis = 1\nfor i in range(1, 6):\n    ergebnis *= i\nprint(ergebnis)",
          "5! = 1 · 2 · 3 · 4 · 5 = 120.")
k.ausgabe("for i in range(3):\n    for j in range(3):\n        if j == 1:\n            break\n"
          "        print(i, j)",
          "break beendet nur die INNERE Schleife. Die äußere läuft weiter. Bei jedem i wird "
          "nur j = 0 ausgegeben, bei j = 1 bricht die innere Schleife ab.",
          tipp="Welche Schleife beendet break?")
k.ausgabe("for i in range(5):\n    if i % 2 == 0:\n        continue\n    print(i)",
          "continue überspringt die geraden Zahlen. Es bleiben 1 und 3.")

# ── Praxis ───────────────────────────────────────────────────────────────
k.luecke("Ergänze den Code: Die erste Schleife soll Index und Namen ausgeben, die zweite "
         "jeden Namen mit dem passenden Alter.",
         """
         namen = ["Anna", "Ben"]
         alter = [19, 21]
         for i, name in ___(namen):
             print(i, name)
         for name, a in ___(namen, alter):
             print(name, a)
         """,
         [["enumerate"], ["zip"]],
         "enumerate liefert (Index, Element), zip liefert Paare aus zwei Listen.",
         tipp="Startnummern beim Marathon … und ein Reißverschluss.")

k.puzzle("Bringe die Zeilen in die richtige Reihenfolge: Der Notendurchschnitt soll berechnet "
         "und ausgegeben werden.",
         """
         noten = [2, 1, 3]
         summe = 0
         for note in noten:
             summe += note
         print(summe / len(noten))
         """,
         "Erst der Startwert 0, dann in der Schleife aufsummieren, NACH der Schleife (nicht "
         "eingerückt) einmal teilen und ausgeben.",
         tipp="Was muss vor der Schleife stehen, was danach?",
         ablenker=["    summe = 0", "summe = 1"])

k.code(r"""
    ## Countdown

    Die Variable `n` ist schon vorgegeben (eine ganze Zahl, mindestens 0).
    Zähle mit einer **for-Schleife** von n bis 1 herunter (jede Zahl in eine
    eigene Zeile) und gib danach `Start!` aus.

        n = 3     Ausgabe:  3
                            2
                            1
                            Start!

    Bei `n = 0` erscheint nur `Start!`.
    """,
    [P(vorspann="n = 3", exakt=["3", "2", "1", "Start!"]),
     P(vorspann="n = 1", exakt=["1", "Start!"]),
     P(vorspann="n = 0", exakt=["Start!"]),
     P(vorspann="n = 5", exakt=["5", "4", "3", "2", "1", "Start!"])],
    """
    for i in range(n, 0, -1):
        print(i)
    print("Start!")
    """,
    "range(n, 0, -1) zählt rückwärts: start n ist dabei, stop 0 nicht mehr. Bei n = 0 ist "
    "der Bereich leer, die Schleife läuft gar nicht, und es kommt direkt `Start!`.",
    pflicht=["for"],
    verboten=["while"],
    tipps=["Welche drei Werte brauchst du in range(): start, stop und step?",
           "Rückwärts heißt: negativer Schritt. Stop ist nicht dabei, also 0 statt 1.",
           "for i in range(n, 0, -1): print(i) und danach (nicht eingerückt) print('Start!')"],
    vorlage="# n ist schon vorgegeben, z. B. 3\n")

k.code(r"""
    ## Nummerierte Einkaufsliste

    Die Liste `einkauf` ist schon vorgegeben, z. B. `["Milch", "Brot", "Eier"]`.
    Gib jeden Artikel mit einer Nummer **ab 1** aus:

        1. Milch
        2. Brot
        3. Eier

    Ist die Liste leer, wird gar nichts ausgegeben.
    """,
    [P(vorspann='einkauf = ["Milch", "Brot", "Eier"]', exakt=["1. Milch", "2. Brot", "3. Eier"]),
     P(vorspann='einkauf = ["Käse"]', exakt=["1. Käse"]),
     P(vorspann='einkauf = []', exakt=[], beschreibung="leere Liste"),
     P(vorspann='einkauf = ["A", "B", "C", "D"]', exakt=["1. A", "2. B", "3. C", "4. D"])],
    """
    for i, artikel in enumerate(einkauf):
        print(f"{i + 1}. {artikel}")
    """,
    "enumerate zählt ab 0, für die Anzeige rechnet man + 1. (Profi-Variante: "
    "`enumerate(einkauf, 1)` startet direkt bei 1.) Auch `for i in range(len(einkauf)):` "
    "ist richtig.",
    tipps=["Du brauchst zu jedem Artikel auch seine Position.",
           "enumerate(einkauf) liefert (0, 'Milch'), (1, 'Brot'), …",
           'for i, artikel in enumerate(einkauf): print(f"{i + 1}. {artikel}")'],
    vorlage="# einkauf ist schon vorgegeben\n")

_BON = 'artikel = ["Milch", "Brot", "Käse"]\npreise = [1.19, 2.5, 3.49]'

k.code(r"""
    ## Kassenbon mit zip

    Vorgegeben sind zwei Listen, z. B.

        artikel = ["Milch", "Brot", "Käse"]
        preise = [1.19, 2.5, 3.49]

    Gib mit `zip()` für jeden Artikel eine Zeile `Artikel: Preis` aus und am
    Ende die Summe. Alle Preise mit **zwei Nachkommastellen** (`{wert:.2f}`):

        Milch: 1.19
        Brot: 2.50
        Käse: 3.49
        Summe: 7.18

    Sind die Listen unterschiedlich lang, zählen nur die Paare, die zip bildet.
    """,
    [P(vorspann=_BON, erwartet=["Milch: 1.19", "Brot: 2.50", "Käse: 3.49", "Summe: 7.18"]),
     P(vorspann='artikel = []\npreise = []', exakt=["Summe: 0.00"], beschreibung="leerer Bon"),
     P(vorspann='artikel = ["Tee", "Kekse"]\npreise = [2.0, 1.5, 9.99]',
       exakt=["Tee: 2.00", "Kekse: 1.50", "Summe: 3.50"], beschreibung="unterschiedlich lang"),
     P(vorspann='artikel = ["Saft"]\npreise = [0.99]', exakt=["Saft: 0.99", "Summe: 0.99"])],
    """
    summe = 0
    for name, preis in zip(artikel, preise):
        print(f"{name}: {preis:.2f}")
        summe += preis
    print(f"Summe: {summe:.2f}")
    """,
    "zip bildet die Paare (Artikel, Preis). In derselben Schleife wird die Summe aufgebaut "
    "(Startwert 0). Die Summe wird erst NACH der Schleife ausgegeben.",
    pflicht=["zip"],
    tipps=["Du brauchst eine Schleife über zwei Listen gleichzeitig und einen Akkumulator.",
           "for name, preis in zip(artikel, preise): … und summe += preis",
           'Nach der Schleife: print(f"Summe: {summe:.2f}")'],
    vorlage="# artikel und preise sind schon vorgegeben\nsumme = 0\n",
    streng=True)

k.code(r"""
    ## Wörter zählen

    Die Variable `text` ist schon vorgegeben, z. B. `"der hund und der ball"`.
    Zähle mit einem Dictionary, wie oft jedes Wort vorkommt, und gib für jedes
    Wort eine Zeile `wort: anzahl` aus:

        der: 2
        hund: 1
        und: 1
        ball: 1

    Die Reihenfolge der Zeilen ist egal. Groß-/Kleinschreibung zählt
    (`Hallo` und `hallo` sind verschiedene Wörter). Mit `text.split()` (ohne
    Argument) bekommst du die Liste der Wörter. Bei leerem Text ist sie leer,
    und es wird nichts ausgegeben.
    """,
    [P(vorspann='text = "der hund und der ball"',
       erwartet=["der: 2", "hund: 1", "und: 1", "ball: 1"], nicht=["der: 1"]),
     P(vorspann='text = "a a a"', exakt=["a: 3"]),
     P(vorspann='text = ""', exakt=[], beschreibung="leerer Text"),
     P(vorspann='text = "Hallo hallo Welt"', erwartet=["Hallo: 1", "hallo: 1", "Welt: 1"],
       nicht=["hallo: 2"],
       beschreibung="Groß-/Kleinschreibung")],
    """
    anzahl = {}
    for wort in text.split():
        anzahl[wort] = anzahl.get(wort, 0) + 1
    for wort, n in anzahl.items():
        print(f"{wort}: {n}")
    """,
    "Das Zählmuster: Für jedes Wort `anzahl.get(wort, 0) + 1`. Die Ausgabe passiert in einer "
    "ZWEITEN Schleife, nachdem alles gezählt ist. Sonst würde jedes Wort mehrfach mit "
    "Zwischenständen erscheinen.",
    tipps=["Erst zählen, dann ausgeben: zwei Schleifen nacheinander.",
           "anzahl = {} und für jedes wort in text.split(): anzahl[wort] = anzahl.get(wort, 0) + 1",
           'for wort, n in anzahl.items(): print(f"{wort}: {n}")'],
    vorlage="# text ist schon vorgegeben\nanzahl = {}\n",
    streng=True)

k.zusammenfassung(r"""
    ## for-Schleifen auf einen Blick

        for x in liste:                  # jedes Element (for-each)
        for c in "Hallo":                # jedes Zeichen
        for i in range(len(liste)):      # jeder Index
        for i, x in enumerate(liste):    # Index UND Element
        for a, b in zip(liste1, liste2): # zwei Listen gleichzeitig
        for key in d:                    # Schlüssel eines Dictionaries
        for key, value in d.items():     # Schlüssel UND Wert

    | Aufruf | Zahlen |
    |---|---|
    | `range(5)` | 0, 1, 2, 3, 4 |
    | `range(2, 10, 3)` | 2, 5, 8 |
    | `range(10, 2, -3)` | 10, 7, 4 |
    | `range(1, n + 1)` | 1 bis n |
    | `range(10, 0)` | nichts (Schritt fehlt) |

    !! range: start ist dabei, stop nicht. Standard: start = 0, step = 1.
    !! zip hört bei der kürzeren Liste auf.
    !! Akkumulator: Summe startet bei 0, Produkt bei 1, Liste bei [].
    """)
