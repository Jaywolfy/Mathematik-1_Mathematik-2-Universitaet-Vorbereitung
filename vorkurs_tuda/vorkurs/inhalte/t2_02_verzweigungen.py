# -*- coding: utf-8 -*-
"""Kapitel: Verzweigungen – if, elif, else, match (Vorlesung 2, Folien 10–23)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="verzweigungen",
    titel="Verzweigungen – if, elif, else, match",
    beschreibung="Das Programm Entscheidungen treffen lassen",
    quelle="Vorlesung 2, Livecoding 2",
    teil="tag2",
    icon="🚦")

k.lernziele([
    "Ich kann mit if und else Code nur unter einer Bedingung ausführen",
    "Ich kann mit elif mehrere Fälle in der richtigen Reihenfolge prüfen",
    "Ich kann mit match und case einen Wert mit festen Möglichkeiten vergleichen",
    "Ich kann mit % prüfen, ob eine Zahl durch eine andere teilbar ist",
    "Ich rücke Blöcke richtig ein und halte die Verschachtelung flach",
])

# ── Erklärung 1: if / else ──────────────────────────────────────────────────
k.erklaerung("if und else", r"""
    ## Kontrollfluss: welchen Weg nimmt das Programm?

    Bisher lief jedes Programm stur von oben nach unten. Oft sollen
    Anweisungen aber nur unter einer **Bedingung** ausgeführt werden. Dafür
    gibt es **Verzweigungen**: Der **Kontrollfluss** (der Weg durch das
    Programm) teilt sich in mehrere **Zweige**.

    :::analogie 🧭 Das Navi
    Ein Navi entscheidet ständig: „WENN Stau auf der Autobahn, DANN fahr
    über die Landstraße, SONST bleib auf der Autobahn.“
      • Die **Bedingung** ist die Frage „Stau?“. Die Antwort ist Ja oder
        Nein, also `True` oder `False`.
      • Der **if-Zweig** ist die Landstraße, der **else-Zweig** die Autobahn.
      • Egal welcher Weg: Danach kommen beide wieder am selben Ziel an.
        Im Programm geht es nach der Verzweigung mit der nächsten nicht
        eingerückten Zeile weiter.
    :::

    Ausformuliert: **„Wenn <Bedingung>, dann führe <X> aus, sonst <Y>.“**

    :::visual entscheidung
    {"bedingung": "stau", "ja": "print(\"Landstraße\")", "nein": "print(\"Autobahn\")"}
    :::
    ---
    ## Die if-Anweisung

    :::code
    x = 5
    if x > 3:  # if benötigt einen bool als Bedingung
        print("x ist größer als 3")
    else:
        print("x ist nicht größer als 3")
    print("fertig")
    :::

    So funktioniert es:
      • Nach `if` kommt eine Bedingung, die `True` oder `False` ergibt.
      • Am Ende der Zeile steht ein **Doppelpunkt** `:`.
      • Der **Block** darunter ist **eingerückt** (meist 4 Leerzeichen).
      • Ist die Bedingung `True`, läuft der if-Block, sonst der else-Block.
      • `else` hat keine eigene Bedingung und ist optional.

    :::achtung Einrückung gehört zur Syntax
    Python erkennt nur an der Einrückung, welche Zeilen zum Block gehören.

        if x > 3:
        print("x ist größer als 3")

    ergibt `IndentationError: expected an indented block after 'if'
    statement on line 1`. Mische außerdem nie Tabs und Leerzeichen.
    :::
    ---
    ## Beispiel: Teilbarkeit mit %

    Der Rest-Operator `%` liefert den Rest einer Division. Ist der Rest 0,
    geht die Division glatt auf: Die Zahl ist **teilbar**.

    :::code eingaben=12
    num = int(input('Gib eine Zahl an: '))
    if num % 3 == 0:
        print('Die eingegebene Zahl ist durch 3 teilbar')
    else:
        print('Die eingegebene Zahl ist nicht durch 3 teilbar')
    :::

    Auch Verneinungen sind möglich: `if num % 3 != 0:` (dann die Zweige
    tauschen).

    !! Teilbarkeit prüfen: `a % b == 0` bedeutet „a ist durch b teilbar“.
    ---
    ## Schönheitsfehler: if a == True

    Am Anfang sieht man oft:

        if a == True:
        if a == False:

    Der Vergleich liefert selbst nur wieder `True` oder `False`. Genauso
    gut könnte man `((a == True) == True) == True` schreiben. Kürzer und
    besser:

        if a:
        if not a:
    """)

k.ausgabe('x = 5\nif x > 3:\n    print("x ist größer als 3")\nelse:\n    print("x ist nicht größer als 3")',
          "5 > 3 ist True → der if-Block wird ausgeführt, der else-Block nicht.")
k.ausgabe('x = 2\nif x > 3:\n    print("groß")\nelse:\n    print("klein")\nprint("fertig")',
          "2 > 3 ist False → else-Block: 'klein'. Die letzte Zeile ist nicht eingerückt, "
          "gehört also zu keinem Block und wird immer ausgeführt.")
k.ausgabe('x = 5\nif x > 3:\nprint("x ist größer als 3")',
          "Der Block nach if ist nicht eingerückt → IndentationError.")
k.mc("Was fehlt in dieser Zeile?   if x > 3",
     ["Ein Doppelpunkt am Ende", "Ein Semikolon am Ende", "Klammern um x > 3", "Nichts"],
     "Nach if-, elif- und else-Zeilen kommt in Python immer ein Doppelpunkt. "
     "(Bei den Schleifen im nächsten Kapitel ist es genauso.)")
k.mc("Wie überprüft man, ob die Zahl a durch die Zahl b teilbar ist?",
     ["a % b == 0", "a / b == 0", "a // b == 0", "a % b == 1"],
     "`%` liefert den Rest der Division. Rest 0 heißt: Die Division geht auf. `a / b == 0` "
     "wäre nur bei a = 0 wahr, und `a // b == 0` heißt nur „a ist kleiner als b“ (bei "
     "positiven Zahlen). (Quizfrage aus Vorlesung 2)")
k.ausgabe('num = 9\nif num % 3 == 0:\n    print("durch 3 teilbar")\nelse:\n    print("nicht durch 3 teilbar")',
          "9 % 3 = 0 → die Bedingung ist True.")
k.mc("Wie schreibt man   if a == True:   kürzer und besser?",
     ["if a:", "if True:", "if a = True:", "if not a:"],
     "a ist selbst schon True oder False. `if a:` reicht völlig. "
     "Und statt `if a == False:` schreibt man `if not a:`.")
k.wf("Die Einrückung gehört in Python zur Syntax.", True,
     "Ja! Sie zeigt Python, welche Anweisungen zu einem Block gehören. (In Java nimmt "
     "man dafür geschweifte Klammern.)")

# ── Erklärung 2: elif ───────────────────────────────────────────────────────
k.erklaerung("Mehrere Fälle: elif", r"""
    ## Die naheliegende (unschöne) Lösung

    Man kann if-Anweisungen ineinander **verschachteln**:

        if my_obj == "cube":
            print('the square hole')
        else:
            if my_obj == "circular":
                print('into the circle?')
            else:
                if my_obj == "rectangular":
                    print('please the rectangle')
                else:
                    print('INTO THE SQUARE HOLE')

    Das rutscht immer weiter nach rechts und wird unübersichtlich.
    ---
    ## Die elegantere Lösung: elif

    `elif` ist kurz für „else if“: „sonst, wenn …“.

        if my_obj == "cube":
            print('the square hole')
        elif my_obj == "circular":
            print('into the circle?')
        elif my_obj == "rectangular":
            print('please the rectangle')
        else:
            print('INTO THE SQUARE HOLE')

    :::analogie 📦 Die Sortieranlage bei der Post
    Ein Paket rollt über ein Band mit mehreren Klappen. An jeder Klappe
    wird gefragt: „Passt du hier?“ Das Paket fällt durch die **erste**
    passende Klappe und ist dann weg. Spätere Klappen sieht es nie.
    Kommt es am Ende an, landet es im Sammelkorb: das ist `else`.
    :::

    !! Die Bedingungen werden von OBEN nach UNTEN geprüft.
    !! Nur der ERSTE zutreffende Zweig wird ausgeführt, danach ist Schluss.
    ---
    ## Reihenfolge ist wichtig

    :::visual entscheidung
    {"bedingung": "temp > 25", "ja": "print(\"Badewetter\")",
     "elif": [{"bedingung": "temp > 10", "text": "print(\"Jacke\")"}],
     "nein": "print(\"Winterjacke\")"}
    :::

    :::code
    temp = 15
    if temp > 25:
        print("Badewetter")
    elif temp > 10:
        print("Jacke")
    else:
        print("Winterjacke")
    :::

    :::achtung Strenge Bedingungen nach oben
    Prüfst du zuerst `punkte >= 50` und danach `punkte >= 90`, landet
    jede 95 schon im ersten Zweig. Der zweite kommt nie dran. Ordne von
    der strengsten zur lockersten Bedingung.
    :::
    ---
    ## Wie tief darf man schachteln?

    Die Vorlesung fragt im Quiz: „Wie tief darf man in Python schachteln?“

    :::info Die Antwort
    Technisch erlaubt Python (CPython) knapp 100 Einrückungsebenen.
    Getestet: 99 verschachtelte `if`-Blöcke laufen, beim hundertsten
    meldet Python `IndentationError: too many levels of indentation`.

    Sinnvoll sind aber höchstens 3 bis 4 Ebenen. Alles darüber versteht
    niemand mehr. Statt tiefer zu schachteln: `elif` verwenden oder
    Bedingungen mit `and` zusammenfassen.
    :::
    """)

k.ausgabe('temp = 15\nif temp > 25:\n    print("Badewetter")\nelif temp > 10:\n    print("Jacke")\nelse:\n    print("Winterjacke")',
          "15 > 25? Nein. 15 > 10? Ja → 'Jacke'. Danach wird nichts mehr geprüft.")
k.ausgabe('punkte = 95\nif punkte >= 50:\n    print("bestanden")\nelif punkte >= 90:\n    print("super")',
          "Falle! 95 >= 50 ist schon True → 'bestanden'. Der elif-Zweig wird gar nicht "
          "mehr geprüft. Die strengere Bedingung (>= 90) hätte nach OBEN gehört!",
          tipp="Es wird nur der ERSTE zutreffende Zweig ausgeführt.")
k.ausgabe('x = 10\nif x > 5:\n    print("A")\nif x > 8:\n    print("B")',
          "Das sind zwei GETRENNTE if-Anweisungen. Beide werden geprüft und beide sind True → A und B.")
k.ausgabe('x = 10\nif x > 5:\n    print("A")\nelif x > 8:\n    print("B")',
          "Mit elif gehören sie zusammen: Der erste zutreffende Zweig (A) gewinnt, B wird übersprungen.")
k.wf("Bei if/elif/else können mehrere Zweige nacheinander ausgeführt werden.", False,
     "Nein, nur der erste Zweig, dessen Bedingung True ist. Danach wird der Rest übersprungen.")
k.mc("Wie tief darf man in Python schachteln?",
     ["Technisch knapp 100 Ebenen, sinnvoll sind aber höchstens 3–4",
      "Beliebig tief, es gibt keine Grenze",
      "Höchstens 2 Ebenen, sonst gibt es einen SyntaxError",
      "Gar nicht: if darf nie in einem anderen if stehen"],
     "CPython erlaubt knapp 100 Einrückungsebenen (danach: IndentationError: too many levels "
     "of indentation). Lesbar bleibt Code aber nur mit wenigen Ebenen. Lieber elif oder and "
     "verwenden. (Quizfrage aus Vorlesung 2)")

# ── Erklärung 3: match ──────────────────────────────────────────────────────
k.erklaerung("match und case", r"""
    ## Die (teilweise) noch elegantere Lösung: match

    Vergleichst du EINEN Wert mit vielen festen Möglichkeiten (`x == 1`,
    `x == 2`, `x == 3`, …), gibt es seit Python 3.10 die
    **match-Anweisung**:

    :::code
    my_obj = "circular"
    match my_obj:
        case "cube":
            print('the square hole')
        case "circular":
            print('into the circle?')
        case "rectangular":
            print('please the rectangle')
        case _:
            print('INTO THE SQUARE HOLE')
    :::

      • Jedes `case` entspricht einem if/elif-Fall mit `==`.
      • `case _:` ist der **Standardfall**: Er passt immer, wie `else`.
      • match kann nicht alle Bedingungen eines if umsetzen (kein `and`,
        kein `<` direkt im case).
      • Es ist ähnlich zu `switch` in Java, kann aber noch mehr.
    ---
    ## Der Getränkeautomat

    :::analogie 🥤 Tasten am Getränkeautomaten
    Du drückst eine Taste, der Automat schaut nach, welche es war:
    Taste 1 → Cola, Taste 2 → Wasser, Taste 3 → Saft. Jede andere Taste
    → „Ungültige Auswahl“. Genau so arbeitet `match`: ein Wert (die
    Taste), eine Liste fester Fälle (`case 1:`, `case 2:` …) und ein
    Auffangfall für alles andere (`case _:`).
    :::

    :::code eingaben=2
    taste = int(input("Taste: "))
    match taste:
        case 1:
            print("Cola")
        case 2:
            print("Wasser")
        case 3:
            print("Saft")
        case _:
            print("Ungültige Auswahl")
    :::

    :::info Auf Folie 21 steht „default“
    Dort heißt es: „`default` ist äquivalent zu `else`“. In Python gibt es
    aber kein Schlüsselwort `default`. So heißt der Standardfall in Java
    (`switch`). In Python schreibst du dafür **`case _:`** (wie auf Folie 20).
    :::
    """)

k.ausgabe('my_obj = "circular"\nmatch my_obj:\n    case "cube":\n        print("the square hole")\n'
          '    case "circular":\n        print("into the circle?")\n    case _:\n        print("INTO THE SQUARE HOLE")',
          "Der Fall 'circular' passt → 'into the circle?'.")
k.ausgabe('my_obj = "triangle"\nmatch my_obj:\n    case "cube":\n        print("the square hole")\n'
          '    case "circular":\n        print("into the circle?")\n    case _:\n        print("INTO THE SQUARE HOLE")',
          "Kein Fall passt → case _ (der Standardfall) wird ausgeführt.")
k.mc("Was bedeutet   case _:   in einer match-Anweisung?",
     ["Der Standardfall, wenn kein anderer case passt (wie else)",
      "Der Fall, dass der Wert ein Unterstrich ist",
      "Ein Fehler",
      "Der erste Fall"],
     "case _ fängt alles auf, was vorher nicht gepasst hat, wie else.")
k.wf("In Python schreibt man den Standardfall einer match-Anweisung als   default:", False,
     "Nein. `default` gibt es in Java bei `switch`. In Python heißt der Standardfall "
     "`case _:`. (Folie 21 ist hier ungenau.)")
k.mc("Wann ist match besonders praktisch?",
     ["Wenn man einen Wert mit vielen festen Möglichkeiten vergleicht",
      "Wenn man zwei Bedingungen mit and verknüpfen will",
      "Wenn man etwas wiederholen möchte",
      "Wenn man prüfen will, ob x größer als 5 ist"],
     "match eignet sich für ähnliche Fälle wie x == 1, x == 2, x == 3. Bedingungen mit "
     "and, < und Co. bildet man besser mit if/elif ab.")
k.ausgabe('alter = 16\nbegleitet = True\nif alter >= 18 or begleitet:\n    print("Einlass")\nelse:\n    print("Kein Einlass")',
          "16 >= 18 ist False, aber begleitet ist True. False or True = True → Einlass.")

# ── Praxisteil ──────────────────────────────────────────────────────────────
k.luecke("Ergänze den Code: Er soll „gerade“ ausgeben, wenn n durch 2 teilbar ist, sonst „ungerade“.",
         """
         n = int(input())
         if n ___ 2 == 0___
             print("gerade")
         ___
             print("ungerade")
         """,
         [["%"], [":"], ["else:"]],
         "Teilbarkeit prüft man mit dem Rest `%`. Nach der Bedingung kommt ein Doppelpunkt, "
         "der Gegenfall beginnt mit `else:`.",
         tipp="Welcher Operator liefert den Rest einer Division?")

k.puzzle("Notenrechner: Bringe die Zeilen in die richtige Reihenfolge. Ab 90 Punkten „sehr gut“, "
         "ab 75 „gut“, ab 50 „bestanden“, sonst „nicht bestanden“.",
         """
         punkte = int(input())
         if punkte >= 90:
             print("sehr gut")
         elif punkte >= 75:
             print("gut")
         elif punkte >= 50:
             print("bestanden")
         else:
             print("nicht bestanden")
         """,
         "Die strengste Bedingung (>= 90) muss ganz oben stehen. Sonst landet eine 95 schon "
         "bei „bestanden“.",
         tipp="Von der strengsten zur lockersten Bedingung.",
         ablenker=["if punkte >= 50:", "else punkte < 50:"])

k.code(r"""
    ## Eintrittspreise im Zoo

    Lies das Alter einer Person ein (ganze Zahl) und gib den Eintrittspreis aus:
      • unter 6 Jahren: `Eintritt: 0 Euro`
      • 6 bis 17 Jahre: `Eintritt: 5 Euro`
      • 18 bis 64 Jahre: `Eintritt: 12 Euro`
      • ab 65 Jahren: `Eintritt: 8 Euro`
    """,
    [P(["3"], ["Eintritt: 0 Euro"]), P(["6"], ["Eintritt: 5 Euro"]),
     P(["17"], ["Eintritt: 5 Euro"]), P(["18"], ["Eintritt: 12 Euro"]),
     P(["64"], ["Eintritt: 12 Euro"]), P(["65"], ["Eintritt: 8 Euro"]),
     P(["0"], ["Eintritt: 0 Euro"], beschreibung="Randfall: Baby mit 0 Jahren")],
    """
    alter = int(input("Wie alt bist du? "))
    if alter < 6:
        print("Eintritt: 0 Euro")
    elif alter < 18:
        print("Eintritt: 5 Euro")
    elif alter < 65:
        print("Eintritt: 12 Euro")
    else:
        print("Eintritt: 8 Euro")
    """,
    "Weil elif nur geprüft wird, wenn die Bedingungen davor False waren, muss man "
    "bei `elif alter < 18` nicht mehr `alter >= 6` dazuschreiben. Die Randfälle 6, 18 und "
    "65 zeigen, ob `<` und `<=` richtig gewählt sind.",
    tipps=["Prüfe die Altersgrenzen der Reihe nach von klein nach groß.",
           "if alter < 6: … elif alter < 18: … – wie geht es weiter?",
           "Zum Schluss: elif alter < 65: … und else: für alle ab 65."],
    streng=True)

k.code(r"""
    ## Größte von drei Zahlen

    Lies drei ganze Zahlen ein (je eine Eingabe) und gib die größte aus.
    Benutze dafür `if`/`elif`/`else` und **nicht** die Funktion `max()`.

        Eingaben: 1, 8, 3     Ausgabe: 8
    """,
    [P(["1", "2", "3"], ["3"]),
     P(["9", "2", "3"], ["9"]),
     P(["1", "8", "3"], ["8"]),
     P(["5", "5", "5"], ["5"], beschreibung="alle gleich"),
     P(["-1", "-7", "-3"], ["-1"], beschreibung="negative Zahlen"),
     P(["4", "9", "9"], ["9"], beschreibung="zwei gleiche Größte"),
     P(["3", "1", "9"], ["9"], beschreibung="Größte ganz hinten, erste größer als zweite")],
    """
    a = int(input())
    b = int(input())
    c = int(input())
    if a >= b and a >= c:
        print(a)
    elif b >= c:
        print(b)
    else:
        print(c)
    """,
    "Ist a mindestens so groß wie b UND c, ist a die größte. Sonst ist es b oder c, und "
    "dann reicht ein Vergleich der beiden. Mit `>=` statt `>` klappen auch gleiche Zahlen.",
    verboten=["max("],
    tipps=["Wann ist a die größte Zahl? Sie muss mit beiden anderen verglichen werden.",
           "if a >= b and a >= c: … – was bleibt im elif übrig?",
           "elif b >= c: print(b), sonst print(c)."])

k.code(r"""
    ## Wochentage mit match

    Lies eine Zahl von 1 bis 7 ein und gib mit einer **match**-Anweisung aus:
      • 1 → `Montag`, 2 → `Dienstag`, 3 → `Mittwoch`, 4 → `Donnerstag`,
        5 → `Freitag`
      • 6 und 7 → `Wochenende`
      • jede andere Zahl → `Ungültig`
    """,
    [P(["1"], ["Montag"]), P(["3"], ["Mittwoch"]), P(["5"], ["Freitag"]),
     P(["7"], ["Wochenende"]), P(["6"], ["Wochenende"]),
     P(["0"], ["Ungültig"], beschreibung="Randfall 0"),
     P(["8"], ["Ungültig"], beschreibung="Randfall 8")],
    """
    tag = int(input())
    match tag:
        case 1:
            print("Montag")
        case 2:
            print("Dienstag")
        case 3:
            print("Mittwoch")
        case 4:
            print("Donnerstag")
        case 5:
            print("Freitag")
        case 6:
            print("Wochenende")
        case 7:
            print("Wochenende")
        case _:
            print("Ungültig")
    """,
    "Jeder Tag bekommt ein eigenes `case`. Alles, was nicht passt, fängt `case _:` auf. "
    "Wichtig: Die Eingabe mit `int()` umwandeln, sonst vergleicht match den Text \"1\" mit "
    "der Zahl 1, und nichts passt. (Für Neugierige: `case 6 | 7:` fasst zwei Fälle zusammen.)",
    pflicht=["match", "case"],
    tipps=["Wandle die Eingabe mit int() um und schreibe dann `match tag:`.",
           "Für jeden Tag ein `case 1:`, `case 2:` … mit eingerücktem print darunter.",
           "Der letzte Fall heißt `case _:` und gibt Ungültig aus."],
    streng=True)

k.zusammenfassung(r"""
    ## Verzweigungen auf einen Blick

        if punkte >= 90:          # Doppelpunkt!
            print("sehr gut")     # eingerückt = gehört zum Block
        elif punkte >= 50:        # nur geprüft, wenn oben False war
            print("bestanden")
        else:                     # keine Bedingung
            print("nicht bestanden")

        match taste:
            case 1:
                print("Cola")
            case _:               # Standardfall (NICHT default)
                print("Ungültig")

    | Werkzeug | wofür |
    |---|---|
    | `if` / `else` | zwei Wege |
    | `elif` | mehrere Fälle, der erste passende gewinnt |
    | `match` / `case` | ein Wert gegen feste Möglichkeiten |
    | `a % b == 0` | a ist durch b teilbar |

    !! Strengste Bedingung zuerst. `if a:` statt `if a == True:`.
    !! Flach bleiben: technisch gehen knapp 100 Ebenen, lesbar sind 3–4.
    """)
