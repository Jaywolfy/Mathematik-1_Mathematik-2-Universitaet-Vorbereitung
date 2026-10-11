# -*- coding: utf-8 -*-
"""Kapitel: Funktionen – Eigene Maschinen bauen (Vorlesung 3, Folien 36–48; Livecoding 3.4)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="funktionen",
    titel="Funktionen – Eigene Maschinen bauen",
    beschreibung="def, Parameter, return, Aufrufstapel, lokale & globale Variablen",
    quelle="Vorlesung 3, Livecoding 3, Übung 3",
    teil="tag3",
    icon="⚙️")

k.lernziele([
    "Ich kann eine Funktion mit def, Parametern und return definieren und aufrufen",
    "Ich kann den Unterschied zwischen print und return erklären",
    "Ich kann verfolgen, wie Funktionen andere Funktionen aufrufen (Aufrufstapel)",
    "Ich kann erklären, was lokale und globale Variablen sind und wann man global braucht",
])

# ── Erklärung 1: Warum Funktionen ────────────────────────────────────────
k.erklaerung("Warum Funktionen?", r"""
    ## Funktionen kennst du schon!

    `print()`, `input()`, `int()`, `len()` … das sind alles Funktionen. Jetzt
    lernst du, EIGENE Funktionen zu schreiben. Aber warum?

    Stell dir vor, du begrüßt Gäste (Folie 38):

        counter = 1

        name = input('Name: ')
        print(f'Hallo {name}, du bist der {counter}. Besucher')
        counter += 1

        name = input('Name: ')
        print(f'Hallo {name}, du bist der {counter}. Besucher')
        counter += 1

    Immer derselbe Code, kopiert. **Das geht schöner!**
    ---
    ## Funktionen sind eigene kleine Maschinen

    :::analogie ☕ Die Kaffeemaschine
      • Du gibst etwas hinein (Bohnen, Wasser). Das sind die **Parameter**.
      • Drinnen passiert etwas, das du nicht sehen musst. Das ist der
        **Funktionskörper**.
      • Heraus kommt etwas (Kaffee). Das ist der **Rückgabewert** (`return`).
      • Der **Bauplan** der Maschine ist die Definition mit `def`. Kaffee gibt
        es aber erst, wenn du auf den Knopf drückst: den **Aufruf**.
      • Einmal gebaut, kannst du sie so oft benutzen, wie du willst.
    :::

    :::visual funktion
    {"name": "verdoppeln", "eingaben": ["x = 4"], "ausgabe": "8", "innen": "return x * 2"}
    :::

    Vorteile von Funktionen (Folie 40):
      • Funktionen **reduzieren Redundanz** (doppelten Code) und sparen Programmierzeit.
      • Code wird **lesbarer**, solange sinnvolle Namen gewählt werden.
      • **Lokale Variablen und Logik werden abgekapselt.**
      • **Unnötige Details werden nach außen versteckt.** Du musst nicht
        wissen, wie die Kaffeemaschine innen funktioniert.
    """)

k.mc("Welcher Vorteil von Funktionen wird in der Vorlesung NICHT genannt?",
     ["Funktionen machen jedes Programm automatisch fehlerfrei",
      "Sie reduzieren Redundanz",
      "Code wird lesbarer",
      "Unnötige Details werden nach außen versteckt"],
     "Leider macht nichts Programme automatisch fehlerfrei. Die anderen drei sind "
     "echte Vorteile.")
k.mc("Mit welchem Schlüsselwort definiert man eine Funktion?",
     ["def", "function", "func", "define"],
     "def name(parameter): ...")
k.ausgabe("def fun1():\n    print('Keine Parameter')\n\nprint('Start')",
          "Die Funktion wird nur DEFINIERT, aber nie AUFGERUFEN. Daher wird nur 'Start' ausgegeben.",
          tipp="Wird fun1 irgendwo aufgerufen?")

# ── Erklärung 2: Definieren und aufrufen ─────────────────────────────────
k.erklaerung("Definieren und aufrufen", r"""
    ## So definiert man eine Funktion

        def name(parameter1, parameter2):
            anweisungen
            return ergebnis

      • `def` („define“) leitet die Funktion ein, dann Name, Klammern, Doppelpunkt.
      • Der **Körper** ist eingerückt.
      • `return` gibt einen Wert zurück UND beendet die Funktion sofort.
      • Die erste Zeile `def name(parameter1, parameter2):` heißt **Funktionssignatur**.

    Beispiele von Folie 41 und 42:

        def fun1():                        # keine Parameter, kein Rückgabewert
            print('Keine Parameter')

        def fun2(param1):                  # ein Parameter, kein Rückgabewert
            print(f'Nur ein Parameter: {param1}')

        def fun3(param1, param2):          # mit Rückgabewert
            print(f'Zwei Parameter: {param1} und {param2}')
            return param1 + param2

    !! Die Definition allein tut noch NICHTS. Erst der AUFRUF fun1() führt den Code aus.
    ---
    ## Funktionen aufrufen

    Syntax: `rückgabewert = funktionsname(parameter)`

    :::code
    def add1(a, b):
        return a + b + 1

    c = add1(5, 3)
    print(c)
    x = 10
    print(add1(x, 5))
    :::

      • Je nach Definition braucht man Parameter oder nicht.
      • Den Rückgabewert MUSS man nicht nutzen, will es aber meistens.
      • Die **Namen** der übergebenen Variablen und der Parameter müssen
        **nicht gleich** sein: `c = add1(x, 5)` passt zu `def add1(a, b):`.
        Der Wert von x landet einfach in a.

    Aus dem Livecoding: Eine Funktion kann auch eine Schleife enthalten.

    :::code
    def fun(name, n):
        msg = "Hallo, " + name
        for i in range(n):
            print(msg)

    fun("Thorsten", 2)
    fun("Anna", 3)
    :::
    """)

k.ausgabe("def add1(a, b):\n    return a + b + 1\n\nc = add1(5, 3)\nprint(c)",
          "5 + 3 + 1 = 9. Der Rückgabewert landet in c. (Vorlesung 3)")
k.ausgabe("def fun3(param1, param2):\n    print(f'Zwei Parameter: {param1} und {param2}')\n"
          "    return param1 + param2\n\nergebnis = fun3(2, 3)\nprint(ergebnis)",
          "Erst gibt die Funktion selbst eine Zeile aus. Dann wird der Rückgabewert 5 "
          "ausgegeben.")
k.ausgabe("def doppelt(zahl):\n    return zahl * 2\n\nx = 7\nprint(doppelt(x))",
          "Der Parameter heißt zahl, die Variable x – das ist egal. 7 * 2 = 14.")
k.wf("Beim Aufruf müssen die Variablen genauso heißen wie die Parameter in der Definition.", False,
     "Nein! c = add1(x, 5) funktioniert mit def add1(a, b). Der Wert von x landet einfach in a.")
k.ausgabe("def quadrat(x):\n    return x * x\n\nprint(quadrat(3) + quadrat(4))",
          "quadrat(3) = 9, quadrat(4) = 16, zusammen 25.")
k.ausgabe("def begruessung(name, gruss='Hallo'):\n    return f'{gruss}, {name}!'\n\n"
          "print(begruessung('Tom'))\nprint(begruessung('Tom', 'Moin'))",
          "Bonus-Wissen (nicht aus Vorlesung 3): Parameter können Standardwerte haben. Ohne "
          "zweiten Wert wird 'Hallo' benutzt, mit zweitem Wert 'Moin'.",
          frage="Bonus-Wissen (kommt in Vorlesung 3 nicht vor): Was gibt dieser Code aus?")

# ── Erklärung 3: print oder return ───────────────────────────────────────
k.erklaerung("print oder return?", r"""
    ## Der Klassiker beim Einstieg

      • `print()` ZEIGT etwas in der Konsole an, für den Menschen.
      • `return` GIBT einen Wert an den Aufrufer ZURÜCK, fürs Programm.

    :::vergleich print: nur anzeigen | return: Wert zurückgeben
    Die Maschine blinkt eine Anzeige. Mitnehmen kann man nichts.
        def doppelt_print(x):
            print(x * 2)

        a = doppelt_print(4)   # zeigt 8 an
        print(a)               # None!
    |||
    Die Maschine gibt einen Becher heraus, den man weiterverwenden kann.
        def doppelt_return(x):
            return x * 2

        b = doppelt_return(4)  # zeigt nichts an
        print(b + 1)           # 9
    :::

    !! Eine Funktion ohne return liefert automatisch None.

    :::achtung return beendet die Funktion sofort
    Alles, was nach einem ausgeführten `return` im Körper steht, wird nicht
    mehr ausgeführt. Ein `return` mitten in einer Schleife beendet also auch
    die Schleife.
    :::

    :::code
    def test():
        return 1
        print('nie')

    x = test()
    print(x)
    :::
    """)

k.mc("Was ist der Unterschied zwischen print und return in einer Funktion?",
     ["print zeigt etwas in der Konsole an, return gibt einen Wert an den Aufrufer zurück",
      "Es gibt keinen Unterschied",
      "return zeigt etwas an, print gibt einen Wert zurück",
      "print beendet die Funktion, return nicht"],
     "print = Anzeige für den Menschen. return = Ergebnis für das Programm "
     "(und Funktion beenden).")
k.mc("Was liefert eine Funktion, die kein return enthält?",
     ["None", "0", "Einen Fehler", "Den letzten berechneten Wert"],
     "Ohne return liefert jede Funktion automatisch None.")
k.ausgabe("def f():\n    print('hi')\n\nx = f()\nprint(x)",
          "f() gibt 'hi' aus, hat aber kein return → liefert None. x ist also None.")
k.ausgabe("def test():\n    return 1\n    print('nie')\n\nprint(test())",
          "return beendet die Funktion sofort. Die Zeile danach wird nie erreicht.")

# ── Erklärung 4: Funktionen rufen Funktionen auf ─────────────────────────
k.erklaerung("Funktionen rufen Funktionen auf", r"""
    ## Eine Funktion benutzt eine andere

    Im Livecoding ruft die Funktion `hi()` die Funktion `fun()` auf:
    „Diese können wir auch wiederum in anderen Funktionen referenzieren.“

        def hi():
            name = input("Name: ")
            n = input("Anzahl: ")
            fun(name, int(n))

    Ein kleineres Beispiel: Eine Pizza kostet 8 Euro.

    :::trace
    def preis(anzahl):
        return anzahl * 8

    def bestellung(name, anzahl):
        betrag = preis(anzahl)
        return f"{name} zahlt {betrag} Euro"

    print(bestellung("Kim", 3))
    :::
    ---
    ## Der Aufrufstapel

    Python merkt sich, wer gerade wen aufgerufen hat, in einem **Aufrufstapel**
    (wie ein Stapel Teller):
      1. `bestellung('Kim', 3)` wird aufgerufen und kommt auf den Stapel.
      2. Darin wird `preis(3)` aufgerufen und kommt **oben drauf**. Jetzt
         arbeitet nur `preis`. `bestellung` wartet.
      3. `preis(3)` ist fertig, gibt `24` zurück und wird abgeräumt.
      4. `bestellung` arbeitet mit `betrag = 24` weiter und gibt den Text zurück.

    :::visual stapel
    {"titel": "Aufrufstapel beim Pizza-Beispiel",
     "rahmen": ["bestellung('Kim', 3)", "preis(3)"],
     "rueckgaben": ["'Kim zahlt 24 Euro'", "24"]}
    :::

    Jede Funktion bekommt auf dem Stapel ihren **eigenen Rahmen** mit ihren
    eigenen Variablen. In der Schritt-für-Schritt-Ansicht oben siehst du das.

    :::info Ausblick: Rekursion
    Eine Funktion darf sich sogar selbst aufrufen. Dann wächst der Stapel
    mit jedem Aufruf. Die Folie warnt: „Wichtig ist, dass sich eine Funktion
    nicht unendlich selbst aufruft.“ Mehr dazu morgen im Kapitel Rekursion.
    :::
    """)

k.ausgabe('def fun(name, n):\n    msg = "Hallo, " + name\n    for i in range(n):\n'
          '        print(msg)\n\ndef hi():\n    fun("Anna", 2)\n    print("fertig")\n\nhi()',
          "hi() ruft fun('Anna', 2) auf. fun gibt zweimal 'Hallo, Anna' aus und ist fertig. "
          "Danach macht hi() weiter und gibt 'fertig' aus.",
          tipp="Erst wenn fun fertig ist, geht es in hi() mit der nächsten Zeile weiter.")
k.mc("Im Pizza-Beispiel rechnet gerade preis(3). Welcher Rahmen liegt ganz oben auf dem Aufrufstapel?",
     ["preis(3)", "bestellung('Kim', 3)", "das Hauptprogramm", "print(...)"],
     "Der zuletzt aufgerufene Rahmen liegt oben und arbeitet. bestellung wartet darunter, "
     "bis preis sein Ergebnis zurückgibt.")
k.mc("In welcher Reihenfolge werden die beiden Funktionen im Pizza-Beispiel FERTIG?",
     ["Erst preis, dann bestellung",
      "Erst bestellung, dann preis",
      "Beide gleichzeitig",
      "preis wird nie fertig"],
     "Wer zuletzt auf den Stapel kam, wird zuerst abgeräumt. bestellung braucht das Ergebnis "
     "von preis, bevor sie selbst fertig werden kann.")
k.ausgabe('def zaehlen(name, buchstabe):\n    zaehler = 0\n    for zeichen in name:\n'
          '        if zeichen.lower() == buchstabe:\n            zaehler += 1\n    return zaehler\n\n'
          'zahl = zaehlen("Anna", "a")\nprint(f"Du hast {zahl} A\'s im Namen")',
          "Beispiel aus Vorlesung 4: 'A' wird durch .lower() zu 'a' und zählt mit. Also 2.")

# ── Erklärung 5: Lokal und global ────────────────────────────────────────
k.erklaerung("Lokale und globale Variablen", r"""
    ## Was in der Funktion passiert, bleibt in der Funktion

    Variablen, die IN einer Funktion entstehen, sind **lokal**. Außerhalb der
    Funktion sind sie nicht sichtbar bzw. benutzbar (Folie 43):

        def greet():
            name = input()
            print(f'Hallo, {name}')

        greet()
        print(name)     # → NameError: name 'name' is not defined

    :::analogie 🚪 Zimmer und Pinnwand
    Jede Funktion ist ein **Zimmer mit eigenen Notizzetteln** (lokale
    Variablen). Die **globalen** Variablen hängen an der **Pinnwand im Flur**.
      • Im Zimmer kann man die Pinnwand lesen.
      • Schreibt man im Zimmer einen Zettel mit demselben Namen, hängt er nur
        im Zimmer und **verdeckt** die Pinnwand.
      • Verlässt man das Zimmer (die Funktion ist fertig), wird es geräumt.
        Die Zettel sind weg.
      • `global counter` heißt: „Ich gehe raus in den Flur und ändere den
        Zettel an der Pinnwand.“
    :::

    :::trace
    counter = 1
    def greet():
        counter = 1
        counter += 1
        print("in greet:", counter)
    greet()
    print("draußen:", counter)
    :::
    In der Schritt-für-Schritt-Ansicht siehst du zwei verschiedene `counter`:
    einen im Rahmen von `greet` und einen globalen.
    ---
    ## Verdecken und global

    Eine einfache Zuweisung in einer Funktion erzeugt eine NEUE lokale
    Variable, die eine gleichnamige globale **verdeckt** (Folie 44):

        counter = 1
        def greet():
            counter = 1        # neue, LOKALE Variable
            counter += 1       # ändert nur die lokale
        greet()
        print(counter)         # → 1  (die globale ist unverändert!)

    Möchte man die globale Variable ändern, braucht man eine Deklaration mit
    `global` (Folie 45):

        counter = 1
        def greet():
            global counter
            counter += 1
        greet()
        print(counter)         # → 2

    Das Besucher-Beispiel wird damit kurz (Folie 39):

    :::code eingaben=Anna|Ben
    counter = 1
    def greet():
        global counter
        name = input('Name: ')
        print(f'Hallo {name}, du bist der {counter}. Besucher')
        counter += 1
    greet()
    greet()
    :::

    Tipp: Meistens ist es sauberer, Werte als Parameter hinein- und mit
    `return` herauszugeben, statt `global` zu benutzen.
    ---
    ## Zwei Fallen (Bonus-Wissen)

    :::achtung UnboundLocalError
    Liest du in einer Funktion eine globale Variable und weist ihr **danach**
    etwas zu, behandelt Python sie in der ganzen Funktion als lokal. Beim
    Lesen ist sie dann noch leer:
        counter = 1
        def g():
            print(counter)     # UnboundLocalError!
            counter = 5
    Abhilfe: `global counter` oder einen anderen Namen benutzen.
    :::

    :::info Listen als Parameter (Bonus-Wissen, kommt nicht in VL 3 vor)
    Übergibst du einer Funktion eine Liste, zeigen der Parameter und deine
    Variable auf **dieselbe** Liste (Aliasing, kennst du aus Tag 2). Ein
    `append` in der Funktion verändert also auch deine Liste draußen:
        def hinzufuegen(liste):
            liste.append("Eier")
        einkauf = ["Milch"]
        hinzufuegen(einkauf)
        print(einkauf)        # ['Milch', 'Eier']
    :::

    :::visual referenz
    {"titel": "Zwei Namen, eine Liste", "namen": {"einkauf": 0, "liste (in der Funktion)": 0},
     "objekte": [["Milch", "Eier"]]}
    :::
    """)

k.ausgabe("def greet():\n    name = 'Lea'\n\ngreet()\nprint(name)",
          "name ist eine LOKALE Variable der Funktion. Außerhalb gibt es sie nicht → NameError.")
k.ausgabe("counter = 1\ndef greet():\n    counter = 1\n    counter += 1\n\ngreet()\nprint(counter)",
          "In der Funktion wird eine neue LOKALE Variable counter erzeugt. Die globale "
          "bleibt 1. (Vorlesung 3)",
          tipp="Wird hier die globale oder eine lokale Variable verändert?")
k.ausgabe("counter = 1\ndef greet():\n    global counter\n    counter += 1\n\ngreet()\nprint(counter)",
          "Mit global counter wird die GLOBALE Variable verändert → 2. (Vorlesung 3)")
k.ausgabe("counter = 1\ndef greet():\n    global counter\n    counter += 1\n\ngreet()\ngreet()\ngreet()\nprint(counter)",
          "Drei Aufrufe, jedes Mal + 1: 1 → 2 → 3 → 4.")
k.mc("Wozu dient das Schlüsselwort global in einer Funktion?",
     ["Um eine globale Variable in der Funktion verändern zu können",
      "Um eine Funktion überall im Internet verfügbar zu machen",
      "Um eine Variable zu löschen",
      "Um eine Funktion schneller zu machen"],
     "Ohne global würde eine Zuweisung eine neue lokale Variable erzeugen.")
k.ausgabe("counter = 1\ndef g():\n    print(counter)\n    counter = 5\n\ng()",
          "Bonus-Wissen: Weil counter in g zugewiesen wird, ist counter in der GANZEN Funktion "
          "lokal. Beim print hat die lokale Variable noch keinen Wert → UnboundLocalError.",
          frage="Bonus-Wissen: Was passiert bei diesem Code?",
          tipp="Gibt es in g eine Zuweisung an counter?")

# ── Praxis ───────────────────────────────────────────────────────────────
k.luecke("Ergänze den Code: Die Funktion soll die Fläche eines Rechtecks ZURÜCKGEBEN.",
         """
         ___ flaeche(breite, hoehe):
             ___ breite * hoehe

         print(flaeche(3, 4))
         """,
         [["def"], ["return"]],
         "def leitet die Definition ein, return gibt das Ergebnis an den Aufrufer zurück.",
         tipp="Ein Schlüsselwort zum Definieren, eins zum Zurückgeben.")

k.puzzle("Bringe die Zeilen in die richtige Reihenfolge: Ein Besucherzähler, der zwei Personen "
         "begrüßt (Hallo Anna … Nr. 1, Hallo Ben … Nr. 2).",
         """
         counter = 1
         def greet(name):
             global counter
             print(f"Hallo {name}, du bist Gast Nr. {counter}")
             counter += 1
         greet("Anna")
         greet("Ben")
         """,
         "Erst die globale Variable, dann die Definition (global steht ganz oben im Körper), "
         "zum Schluss die Aufrufe.",
         tipp="Eine Funktion muss definiert sein, bevor man sie aufruft.",
         ablenker=["    counter = 1"])

k.code(r"""
    ## Teilbar?

    Schreibe eine Funktion   ist_teilbar(a, b)   , die True zurückgibt,
    wenn a durch b teilbar ist, und sonst False.

    Beispiele:  ist_teilbar(10, 5) → True     ist_teilbar(10, 3) → False
    """,
    [F("ist_teilbar(10, 5)", True), F("ist_teilbar(10, 3)", False),
     F("ist_teilbar(21, 7)", True), F("ist_teilbar(7, 21)", False),
     F("ist_teilbar(0, 5)", True), F("ist_teilbar(-10, 5)", True)],
    """
    def ist_teilbar(a, b):
        return a % b == 0
    """,
    "Der Vergleich a % b == 0 ist selbst schon True oder False – man braucht kein if! "
    "Auch 0 ist durch 5 teilbar (Rest 0).",
    tipps=["Wann ist a durch b teilbar? Denk an den Rest.",
           "Modulo! Und ein Vergleich liefert schon True/False.",
           "return a % b == 0"],
    vorlage="def ist_teilbar(a, b):\n    ...")

k.code(r"""
    ## Besucherzähler mit global

    Die Vorlage enthält schon die globale Variable `zaehler = 0`. Schreibe eine
    Funktion `besuch()` ohne Parameter, die den **globalen** `zaehler` um 1
    erhöht und den neuen Wert zurückgibt.

        besuch()   # → 1
        besuch()   # → 2
        print(zaehler)   # → 2
    """,
    [P(nachspann="zaehler = 0\nbesuch()\nbesuch()\nprint(besuch(), zaehler)", erwartet=["3 3"],
       beschreibung="drei Besuche"),
     P(nachspann="zaehler = 10\nprint(besuch())\nprint(zaehler)", exakt=["11", "11"],
       beschreibung="Start bei 10"),
     P(nachspann="zaehler = 0\nprint(besuch())", exakt=["1"], beschreibung="ein Besuch")],
    """
    zaehler = 0

    def besuch():
        global zaehler
        zaehler += 1
        return zaehler
    """,
    "Ohne `global zaehler` gäbe `zaehler += 1` einen UnboundLocalError, weil Python zaehler "
    "dann für lokal hält. Mit global wird die Variable an der „Pinnwand“ geändert.",
    pflicht=["global"],
    tipps=["Die Funktion soll eine Variable AUSSERHALB von sich verändern.",
           "Erste Zeile im Körper: global zaehler",
           "global zaehler, dann zaehler += 1, dann return zaehler"],
    vorlage="zaehler = 0\n\ndef besuch():\n    ...\n")

k.code(r"""
    ## Größtes Element zurückgeben (Variante zu Übung 3, Aufgabe 3.1)

    **Hinweis:** Auf dem Übungsblatt soll das größte Element samt Index auf der
    Konsole **ausgegeben** werden. Diese Aufgabe findest du blattgetreu im
    Kapitel „Übungsblatt 3“. Hier übst du die Variante mit **Rückgabe**.

    Schreibe eine Funktion   groesstes_element(liste)   , die das größte
    Element und seinen Index als Tupel (wert, index) ZURÜCKGIBT.
      • Kommt das Maximum mehrfach vor, nimm den ERSTEN Index.
      • Ist die Liste leer, gib None zurück.

    Beispiel:  groesstes_element([3, 9, 2]) → (9, 1)
    """,
    [F("groesstes_element([3, 9, 2])", (9, 1)),
     F("groesstes_element([5])", (5, 0)),
     F("groesstes_element([-3, -1, -7])", (-1, 1)),
     F("groesstes_element([4, 4, 1])", (4, 0)),
     F("groesstes_element([])", None)],
    """
    def groesstes_element(liste):
        if len(liste) == 0:
            return None
        max_wert = liste[0]
        max_index = 0
        for i, wert in enumerate(liste):
            if wert > max_wert:
                max_wert = wert
                max_index = i
        return (max_wert, max_index)
    """,
    "Sonderfälle: Leere Liste (sonst IndexError bei liste[0]) und NEGATIVE Zahlen: "
    "Wer mit max_wert = 0 startet, findet bei [-3, -1, -7] fälschlich 0! Darum mit dem "
    "ersten Element starten. Mit > (nicht >=) bleibt bei Gleichstand der erste Index.",
    tipps=["Welche Sonderfälle gibt es? Denk an [] und an [-3, -1, -7].",
           "Starte mit max_wert = liste[0] (nicht 0!) und laufe mit enumerate durch die Liste.",
           "if wert > max_wert: max_wert = wert; max_index = i – am Ende return (max_wert, max_index)"],
    vorlage="def groesstes_element(liste):\n    if len(liste) == 0:\n        return None\n    ...")

k.code(r"""
    ## Primzahlen bis n (Funktion ruft Funktion)

    Schreibe zwei Funktionen:
      1. `ist_primzahl(n)` gibt True zurück, wenn n eine Primzahl ist, sonst
         False. Primzahlen sind größer als 1 und nur durch 1 und sich selbst
         teilbar. 0, 1 und negative Zahlen sind keine Primzahlen.
      2. `primzahlen_bis(n)` gibt eine Liste aller Primzahlen von 2 bis n
         (einschließlich) zurück und **benutzt dafür** `ist_primzahl`.

        primzahlen_bis(20) → [2, 3, 5, 7, 11, 13, 17, 19]
        primzahlen_bis(1)  → []
    """,
    [F("primzahlen_bis(20)", [2, 3, 5, 7, 11, 13, 17, 19]),
     F("primzahlen_bis(1)", []),
     F("primzahlen_bis(2)", [2]),
     F("primzahlen_bis(30)"),
     F("ist_primzahl(97)", True),
     F("ist_primzahl(1)", False),
     F("ist_primzahl(-7)", False),
     F("ist_primzahl(25)", False)],
    """
    def ist_primzahl(n):
        if n < 2:
            return False
        for t in range(2, n):
            if n % t == 0:
                return False
        return True

    def primzahlen_bis(n):
        ergebnis = []
        for z in range(2, n + 1):
            if ist_primzahl(z):
                ergebnis.append(z)
        return ergebnis
    """,
    "ist_primzahl kann mit return False sofort aufhören, sobald ein Teiler gefunden ist. Erst "
    "NACH der Schleife steht return True. primzahlen_bis baut eine Liste auf (Akkumulator) "
    "und fragt für jede Zahl die andere Funktion.",
    tipps=["Erst ist_primzahl fertig schreiben und testen, dann primzahlen_bis.",
           "In ist_primzahl: Zahlen unter 2 sofort False; sonst alle Teiler von 2 bis n-1 probieren.",
           "In primzahlen_bis: for z in range(2, n + 1): if ist_primzahl(z): ergebnis.append(z)"],
    vorlage="def ist_primzahl(n):\n    ...\n\n\ndef primzahlen_bis(n):\n    ...\n")

k.zusammenfassung(r"""
    ## Funktionen auf einen Blick

        def add1(a, b):          # Definition: Name, Parameter
            return a + b + 1     # Rückgabewert, beendet die Funktion

        c = add1(5, 3)           # Aufruf → c = 9
        c = add1(x, 5)           # Namen müssen nicht zu den Parametern passen

    | Begriff | Bedeutung |
    |---|---|
    | Parameter | Eingang der Funktion, z. B. `a`, `b` |
    | Rückgabewert | was `return` liefert (ohne return: `None`) |
    | Funktionssignatur | die Zeile `def add1(a, b):` |
    | lokale Variable | entsteht in der Funktion, außen unsichtbar |
    | globale Variable | steht außerhalb, ändern nur mit `global` |
    | Aufrufstapel | wer gerade wen aufgerufen hat; oben arbeitet der neueste Aufruf |

    !! print zeigt an, return gibt zurück.
    !! Die Definition allein tut nichts: Erst der Aufruf führt den Code aus.
    """)
