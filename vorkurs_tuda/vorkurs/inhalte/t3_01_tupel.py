# -*- coding: utf-8 -*-
"""Kapitel: Tupel – Die versiegelte Box (Vorlesung 3, Folien 5–7)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="tupel",
    titel="Tupel – Die versiegelte Box",
    beschreibung="Feste, unveränderliche Wertegruppen",
    quelle="Vorlesung 3",
    teil="tag3",
    icon="🎁")

k.lernziele([
    "Ich kann ein Tupel mit runden Klammern anlegen und mit Index und Slice daraus lesen",
    "Ich kann erklären, warum t[0] = 5 bei einem Tupel einen TypeError auslöst",
    "Ich kann Tupel und Listen mit list() und tuple() ineinander umwandeln",
    "Ich kann ein Tupel in mehrere Variablen auspacken und so auch zwei Werte tauschen",
])

# ── Erklärung 1: Was ist ein Tupel? ───────────────────────────────────────
k.erklaerung("Tupel anlegen und lesen", r"""
    ## Wenn sich nichts ändern soll

    Listen sind praktisch, aber nicht immer braucht man eine Datenstruktur,
    deren Größe sich ändern kann. Ist nur eine **feste Anzahl** von Werten
    gewünscht, nimmt man ein **Tupel** (Typ `tuple`).

    :::analogie 🎫 Ein Tupel ist wie ein Konzertticket
    Auf deinem Ticket stehen Reihe, Platz und Datum: `(12, 7, '24.10.2026')`.
      • Du kannst jede Angabe **ablesen**: „Platz steht an Stelle 1“. Das ist
        der Zugriff mit Index, genau wie bei einer Liste.
      • Du darfst aber nicht mit dem Kuli den Platz **ändern**. Das Ticket
        ist versiegelt. Python meldet dann einen `TypeError`.
      • Willst du einen anderen Platz, bekommst du ein **neues Ticket**. In
        Python heißt das: Die Variable bekommt ein neues Tupel.
      • Am Einlass geht die Kontrolle schnell, weil sich nichts ändern kann.
        Auch Tupel sind etwas schneller als Listen.
    :::

    Beispiele aus dem Alltag:
      • ein Geburtsdatum: `(15, 11, 2006)`
      • GPS-Koordinaten: `(49.877, 8.654)`
      • eine Anmeldung: `('anna@mail.de', 'Anna', 'Informatik')`

    :::info Tuple oder Tupel?
    Auf den Folien steht das englische Wort **Tuple**, hier im Quiz das
    deutsche Wort **Tupel**. Beides meint dasselbe. In Python heißt der Typ `tuple`.
    :::
    ---
    ## Tupel schreiben und lesen

    Tupel schreibt man mit **runden Klammern**. Die Werte trennt man mit Kommas:

        t1 = (wert1, wert2, ..., wertN)
        geburtstag = (15, 11, 2006)

    :::visual variablen
    {"titel": "Ein Tupel ist EIN Wert: eine versiegelte Box mit festen Fächern",
     "vars": [{"name": "geburtstag", "wert": "(15, 11, 2006)", "typ": "tuple"},
              {"name": "einkauf", "wert": "['Milch', 'Brot']", "typ": "list"}]}
    :::

    Zugriffe auf einzelne Einträge und Slices funktionieren **genau wie bei Listen**:

        geburtstag[0]       # → 15
        geburtstag[-1]      # → 2006
        geburtstag[1:]      # → (11, 2006)   ein Slice ist wieder ein Tupel
        len(geburtstag)     # → 3

    :::visual liste
    {"titel": "Die Fächer des Tupels geburtstag", "name": "geburtstag",
     "werte": [15, 11, 2006], "markiert": [0], "negativ": true}
    :::
    ---
    ## Ausprobieren

    :::code
    geburtstag = (15, 11, 2006)
    print(geburtstag[0])
    print(geburtstag[1:])
    print(len(geburtstag))
    print(type(geburtstag))
    :::

    :::achtung Stolperfalle: (5) ist kein Tupel!
    Runde Klammern benutzt man auch beim Rechnen, z. B. `(2 + 3) * 4`.
    Deshalb ist `(5)` einfach die Zahl 5. Für ein Tupel mit **einem**
    Element braucht man ein Komma: `(5,)`. (Das steht nicht auf den Folien,
    ist aber ein Klassiker.)

        print(type((5)))     # <class 'int'>
        print(type((5,)))    # <class 'tuple'>
    :::
    """)

k.ausgabe("t = (4, 5, 6)\nprint(t[1])", "Zugriff wie bei Listen: Index 1 → 5.")
k.ausgabe("t = (4, 5, 6)\nprint(t[1:])", "Ein Slice eines Tupels ist wieder ein Tupel: (5, 6).")
k.mc("Mit welchen Klammern schreibt man ein Tupel?",
     ["Runde Klammern ( )", "Eckige Klammern [ ]", "Geschweifte Klammern { }", "Gar keine"],
     "Tupel: ( ), Listen: [ ], Dictionaries: { }")
k.mc("Wann nimmt man eher ein Tupel statt einer Liste?",
     ["Wenn es eine feste Anzahl von Werten ist, die sich nicht ändern soll",
      "Wenn man ständig Elemente hinzufügen will",
      "Wenn man die Werte sortieren möchte",
      "Nie, Tupel sind veraltet"],
     "Feste, unveränderliche Daten (z.B. Koordinaten, Datum) → Tupel. "
     "Wachsende/schrumpfende Sammlungen → Liste.")
k.mc("Welchen Typ hat x nach   x = (5)   ?",
     ["int – (5) ist einfach die Zahl 5 in Klammern",
      "tuple – ein Tupel mit einem Element",
      "list – eine Liste mit einem Element",
      "Es gibt einen SyntaxError"],
     "Klammern ohne Komma sind Rechenklammern. Ein Tupel mit einem Element schreibt man "
     "`(5,)`. Das Komma macht das Tupel, nicht die Klammer.",
     tipp="Denk an (2 + 3) * 4. Was bedeuten die Klammern dort?")

# ── Erklärung 2: Unveränderlich ──────────────────────────────────────────
k.erklaerung("Unveränderlich: nur überschreiben", r"""
    ## Tupel können nicht verändert werden

    Die Folie sagt es so: **„Wichtiger Unterschied zu Listen: Tuple können
    nicht modifiziert werden, nur überschrieben.“**

        geburtstag = (15, 11, 2006)
        geburtstag[0] = 16        # TypeError: 'tuple' object does not
                                  #            support item assignment
        geburtstag.append(1)      # AttributeError: kein append bei Tupeln

    Die **Variable** darf aber jederzeit ein ganz neues Tupel bekommen:

        geburtstag = (16, 11, 2006)    # ok: neues Ticket statt Kuli

    | Eigenschaft | Liste | Tupel |
    |---|---|---|
    | Klammern | `[1, 2]` | `(1, 2)` |
    | Lesen mit Index und Slice | ja | ja |
    | Ändern (`x[0] = 5`, `append`, `pop`) | ja | nein, Fehler |
    | Größe | kann wachsen und schrumpfen | fest |
    | Geschwindigkeit | gut | etwas besser |
    | typisch für | Einkaufsliste, Messwerte | Datum, Koordinaten, Ticket |
    ---
    ## Umwandeln: list() und tuple()

    Tupel kann man mit `list()` in Listen umwandeln und umgekehrt mit `tuple()`:

        list((1, 2, 3))     # → [1, 2, 3]
        tuple([1, 2, 3])    # → (1, 2, 3)

    Damit kannst du ein Tupel „ändern“: in eine Liste umwandeln, die Liste
    ändern, und daraus ein neues Tupel bauen.

    :::trace
    ticket = (12, 7, '24.10.2026')
    liste = list(ticket)
    liste[1] = 8
    ticket = tuple(liste)
    print(ticket)
    :::

    !! Tupel haben eine bessere Performance: Python muss nicht damit rechnen,
    !! dass sie wachsen oder sich ändern.
    """)

k.ausgabe("t = (4, 5, 6)\nt[0] = 1",
          "Tupel sind unveränderlich → TypeError: 'tuple' object does not support item assignment.")
k.ausgabe("t = (4, 5, 6)\nt = (1, 5, 6)\nprint(t)",
          "Die VARIABLE darf ein neues Tupel bekommen (überschreiben). Nur das Tupel "
          "selbst kann man nicht verändern.")
k.wf("Man kann ein Element eines Tupels mit t[0] = 5 ändern.", False,
     "Tupel können nicht modifiziert werden, nur komplett überschrieben.")
k.wf("Tupel haben eine bessere Performance als Listen.", True,
     "Ja, weil sie unveränderlich sind, kann Python sie effizienter behandeln.")
k.ausgabe("t = (4, 5, 6)\nprint(list(t))", "list() macht aus dem Tupel eine Liste: [4, 5, 6].")
k.ausgabe("print(tuple([1, 2]))", "tuple() macht aus der Liste ein Tupel: (1, 2).")

# ── Erklärung 3: Auspacken ───────────────────────────────────────────────
k.erklaerung("Tupel auspacken", r"""
    ## Auspacken: die Box öffnen

    Man kann ein Tupel direkt in mehrere Variablen **auspacken**. Links vom
    `=` stehen so viele Namen, wie das Tupel Werte hat:

        tag, monat, jahr = (15, 11, 2006)
        print(monat)        # → 11

    :::visual variablen
    {"titel": "Auspacken: Jeder Wert bekommt seine eigene Kiste",
     "schritte": [
       [{"name": "geburtstag", "wert": "(15, 11, 2006)", "typ": "tuple"}],
       [{"name": "geburtstag", "wert": "(15, 11, 2006)", "typ": "tuple"},
        {"name": "tag", "wert": "15", "typ": "int"},
        {"name": "monat", "wert": "11", "typ": "int"},
        {"name": "jahr", "wert": "2006", "typ": "int"}]],
     "texte": ["`geburtstag = (15, 11, 2006)`: eine versiegelte Box",
               "`tag, monat, jahr = geburtstag`: der 1. Wert landet in tag, der 2. in monat, der 3. in jahr"]}
    :::

    :::achtung Die Anzahl muss passen
    Stehen links zu wenige oder zu viele Namen, gibt es einen `ValueError`:
        a, b = (1, 2, 3)     # ValueError: too many values to unpack
    :::
    ---
    ## Trick: zwei Werte tauschen

    Rechts vom `=` entsteht zuerst das Tupel `(b, a)`, dann wird es sofort
    ausgepackt. So tauschst du zwei Variablen in einer Zeile:

    :::trace
    a = 1
    b = 2
    a, b = b, a
    print(a, b)
    :::

    Auspacken wirst du gleich bei den for-Schleifen mit `enumerate()`,
    `zip()` und `d.items()` wiedersehen. Diese Funktionen liefern Tupel.
    """)

k.ausgabe("punkt = (3, 7)\nx, y = punkt\nprint(y)",
          "Auspacken: x bekommt 3, y bekommt 7.")
k.ausgabe("geburtstag = (15, 11, 2006)\ntag, monat, jahr = geburtstag\nprint(f'{tag}.{monat}.{jahr}')",
          "Das Tupel wird in drei Variablen ausgepackt und dann im f-String benutzt.")
k.ausgabe("a, b = (1, 2, 3)\nprint(a)",
          "Links stehen zwei Namen, rechts sind es drei Werte. Das passt nicht → ValueError "
          "(too many values to unpack). Es wird gar nichts ausgegeben.",
          tipp="Zähle die Namen links und die Werte rechts.")
k.ausgabe("x = 'links'\ny = 'rechts'\nx, y = y, x\nprint(x)",
          "Rechts entsteht das Tupel ('rechts', 'links'). Beim Auspacken bekommt x den ersten "
          "Wert, also 'rechts'.")

# ── Praxis ───────────────────────────────────────────────────────────────
k.luecke("Ergänze den Code: Das Tupel datum wird ausgepackt, danach wird das Jahr ausgegeben.",
         """
         datum = (24, 12, 2026)
         tag, monat, ___ = ___
         print(jahr)
         """,
         [["jahr"], ["datum"]],
         "Links stehen die drei neuen Namen, rechts das Tupel. Der dritte Wert (2026) landet in jahr.",
         tipp="Die dritte Variable wird in der letzten Zeile benutzt.")

k.puzzle("Bringe die Zeilen in die richtige Reihenfolge: Auf dem Ticket soll Platz 7 durch "
         "Platz 8 ersetzt und das neue Ticket ausgegeben werden.",
         """
         ticket = (12, 7, "24.10.2026")
         liste = list(ticket)
         liste[1] = 8
         ticket = tuple(liste)
         print(ticket)
         """,
         "Ein Tupel selbst kann man nicht ändern. Darum: in eine Liste umwandeln, die Liste "
         "ändern und daraus ein neues Tupel bauen.",
         tipp="Erst umwandeln, dann ändern, dann zurückwandeln.",
         ablenker=["ticket[1] = 8", "ticket.append(8)"])

k.code(r"""
    ## Punkt spiegeln

    Die Variable `punkt` ist schon vorgegeben, z. B. `punkt = (3, 7)`. Sie
    enthält ein Tupel `(x, y)`.

    Packe das Tupel aus, baue ein **neues Tupel** mit vertauschten Werten und
    gib es mit `print()` aus.

        punkt = (3, 7)        Ausgabe: (7, 3)
        punkt = ('x', 'y')    Ausgabe: ('y', 'x')

    Das Ergebnis soll ein Tupel sein (runde Klammern), keine Liste.
    """,
    [P(vorspann="punkt = (3, 7)", erwartet=["(7, 3)"]),
     P(vorspann="punkt = (5, 5)", erwartet=["(5, 5)"]),
     P(vorspann="punkt = (-2, 0)", erwartet=["(0, -2)"]),
     P(vorspann="punkt = ('x', 'y')", erwartet=["('y', 'x')"])],
    """
    x, y = punkt
    gespiegelt = (y, x)
    print(gespiegelt)
    """,
    "Auspacken liefert die beiden Werte einzeln. Mit runden Klammern entsteht daraus ein neues "
    "Tupel in umgekehrter Reihenfolge. Kürzer geht es mit `print((punkt[1], punkt[0]))`.",
    tipps=["Hol die beiden Werte einzeln aus dem Tupel heraus.",
           "Mit `x, y = punkt` packst du das Tupel aus.",
           "Danach: `gespiegelt = (y, x)` und `print(gespiegelt)`."],
    vorlage="# punkt ist schon vorgegeben, z. B. (3, 7)\n",
    streng=True)

k.code(r"""
    ## Finde den Fehler: Geburtstag

    In `person` steht schon ein Tupel `(name, alter, stadt)`, z. B.
    `('Anna', 19, 'Darmstadt')`. Die Person hat Geburtstag. Das Programm soll
    ein Tupel ausgeben, in dem das Alter um 1 größer ist:

        person = ('Anna', 19, 'Darmstadt')    Ausgabe: ('Anna', 20, 'Darmstadt')

    Der Code in der Vorlage stürzt aber mit einem `TypeError` ab. Repariere ihn!
    """,
    [P(vorspann="person = ('Anna', 19, 'Darmstadt')", erwartet=["('Anna', 20, 'Darmstadt')"]),
     P(vorspann="person = ('Ben', 0, 'Köln')", erwartet=["('Ben', 1, 'Köln')"]),
     P(vorspann="person = ('Deniz', 41, 'Mainz')", erwartet=["('Deniz', 42, 'Mainz')"])],
    """
    name, alter, stadt = person
    person = (name, alter + 1, stadt)
    print(person)
    """,
    "Ein Tupel kann man nicht verändern, man kann die Variable aber mit einem NEUEN Tupel "
    "überschreiben. Auspacken macht das bequem. Auch der Umweg über `list()` und `tuple()` "
    "ist richtig.",
    tipps=["Welche Zeile löst den TypeError aus? Was darf man mit Tupeln nicht tun?",
           "Pack das Tupel in name, alter, stadt aus und baue ein neues Tupel.",
           "`person = (name, alter + 1, stadt)` und danach `print(person)`."],
    vorlage="person[1] = person[1] + 1\nprint(person)\n",
    streng=True)

k.code(r"""
    ## Stoppuhr: Sekunden umrechnen

    Lies eine Anzahl Sekunden (ganze Zahl) mit `input()` ein. Berechne daraus
    Stunden, Minuten und Sekunden und speichere sie in **einem Tupel**
    `zeit = (stunden, minuten, sekunden)`.

    Gib zuerst das Tupel aus. Packe es danach aus und gib die Zeit so aus:

        Eingabe:  3723
        Ausgabe:  (1, 2, 3)
                  1 h 2 min 3 s

    Tipp: `//` ist die ganzzahlige Division, `%` liefert den Rest. Eine Stunde
    hat 3600 Sekunden.
    """,
    [P(["3723"], ["(1, 2, 3)", "1 h 2 min 3 s"]),
     P(["0"], ["(0, 0, 0)", "0 h 0 min 0 s"]),
     P(["59"], ["(0, 0, 59)", "0 h 0 min 59 s"]),
     P(["3600"], ["(1, 0, 0)", "1 h 0 min 0 s"]),
     P(["86399"], ["(23, 59, 59)", "23 h 59 min 59 s"])],
    """
    sekunden = int(input("Sekunden: "))
    stunden = sekunden // 3600
    minuten = sekunden % 3600 // 60
    rest = sekunden % 60
    zeit = (stunden, minuten, rest)
    print(zeit)
    h, m, s = zeit
    print(f"{h} h {m} min {s} s")
    """,
    "Erst die ganzen Stunden (`// 3600`), dann vom Rest der Stunde (`% 3600`) die ganzen "
    "Minuten (`// 60`), am Ende die übrigen Sekunden (`% 60`). Die drei Werte kommen in ein "
    "Tupel, das danach wieder ausgepackt wird.",
    tipps=["Wie viele ganze Stunden passen in 3723 Sekunden? Und was bleibt übrig?",
           "stunden = sekunden // 3600, minuten = sekunden % 3600 // 60, rest = sekunden % 60",
           "zeit = (stunden, minuten, rest), dann print(zeit), dann h, m, s = zeit und ein f-String."],
    streng=True)

k.zusammenfassung(r"""
    ## Tupel auf einen Blick

        geburtstag = (15, 11, 2006)    # Tupel mit runden Klammern
        geburtstag[0]                  # → 15   (Index wie bei Listen)
        geburtstag[1:]                 # → (11, 2006)
        tag, monat, jahr = geburtstag  # auspacken
        a, b = b, a                    # zwei Werte tauschen
        einer = (5,)                   # Tupel mit EINEM Element: Komma!

    | Aktion | Liste | Tupel |
    |---|---|---|
    | lesen `x[0]`, `x[1:]`, `len(x)` | ja | ja |
    | ändern `x[0] = 5`, `append` | ja | nein, `TypeError`/`AttributeError` |
    | Variable neu belegen | ja | ja |
    | aus dem anderen Typ erzeugen | `list(tupel)` | `tuple(liste)` |

    !! Tupel = feste Anzahl von Werten, unveränderlich, etwas schneller.
    !! Ändern geht nur über ein NEUES Tupel.
    """)
