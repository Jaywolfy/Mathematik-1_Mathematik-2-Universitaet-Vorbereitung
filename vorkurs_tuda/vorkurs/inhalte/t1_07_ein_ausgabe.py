# -*- coding: utf-8 -*-
"""Kapitel: Ein- und Ausgabe – print() und input() (Vorlesung 1, Folien 39–43, Livecoding 1)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="ein_ausgabe",
    titel="Ein- und Ausgabe – print() und input()",
    beschreibung="Mit dem Nutzer reden: Ausgeben, f-Strings, Eingaben einlesen",
    quelle="Vorlesung 1, Livecoding 1",
    teil="tag1",
    icon="💬")

k.lernziele([
    "Ich kann mit print() mehrere Werte ausgeben und mit end='' den Zeilenumbruch steuern",
    "Ich kann f-Strings schreiben und darin auch rechnen",
    "Ich kann Eingaben mit input() lesen und für Rechnungen umwandeln",
    "Ich kann ein kleines Programm nach dem Muster Eingabe → Verarbeitung → Ausgabe schreiben",
])

# ── Erklärung 1: print() ─────────────────────────────────────────────────
k.erklaerung("Ausgabe mit print()", r"""
    ## print() – die Anzeigetafel deines Programms

    Mit `print()` zeigt dein Programm etwas in der Konsole an – wie die
    Anzeigetafel am Bahnhof.

        print()                 # gibt eine leere Zeile aus
        print(5)                # 5
        print('Lorem ipsum')    # Lorem ipsum

    Der Wert wird bei Bedarf automatisch in Text umgewandelt.
    Gibst du **mehrere Werte** mit Komma an, trennt `print` sie mit einem
    Leerzeichen:

    :::code
    print("Alter:", 19)
    print(5, '-', 2, '=', 3)
    :::

    :::info Auf Folie 40 steht „ein einzelner Parameter“
    Gemeint ist: Man KANN `print()` einen Wert übergeben. Tatsächlich nimmt
    `print()` aber beliebig viele Werte – auch gar keinen (dann gibt es eine
    leere Zeile).
    :::
    ---
    ## Kein Zeilenumbruch: end=''

    Normalerweise beginnt nach jedem `print()` eine neue Zeile. Mit
    `end=''` bestimmst du selbst, was am Ende kommt – hier: nichts.

    :::code
    print('Hallo', end='')
    print(' Welt')
    print('Lade', end='...')
    print('fertig')
    :::

    `end` ist ein **benannter Parameter**: Du schreibst seinen Namen, ein `=`
    und den Wert. In der Hilfe (`help(print)`) siehst du, dass `end`
    normalerweise `'\n'` ist – genau der Zeilenumbruch.
    """)

k.mc("Was gibt print() ohne Parameter aus?",
     ["Eine leere Zeile", "Einen Fehler", "None", "Das Wort 'print'"],
     "print() ohne Parameter gibt einfach eine leere Zeile aus.")
k.ausgabe('print("Alter:", 19)',
          "Mehrere Werte mit Komma → print trennt sie mit einem Leerzeichen.")
k.ausgabe("print(5, '-', 2, '=', 3)",
          "Fünf Werte, jeweils durch ein Leerzeichen getrennt: 5 - 2 = 3. "
          "(Python rechnet hier nichts – das '-' ist nur Text.)")
k.ausgabe('print("Hallo", end="")\nprint("Welt")',
          "end=\"\" verhindert den Zeilenumbruch nach dem ersten print. Das zweite "
          "print schreibt direkt dahinter: HalloWelt – ohne Leerzeichen!",
          tipp="Was steht nach 'Hallo' – ein Zeilenumbruch oder nichts?")
k.ausgabe('print("Summe: " + str(10 + 5))',
          "Erst 10 + 5 = 15, dann str(15) = '15', dann verketten: 'Summe: 15'.")
k.wf("print() kann immer nur genau einen Wert ausgeben.", False,
     "print() nimmt beliebig viele Werte (durch Kommas getrennt) und setzt "
     "Leerzeichen dazwischen – oder gar keinen Wert (leere Zeile).")

# ── Erklärung 2: f-Strings ───────────────────────────────────────────────
k.erklaerung("Text und Werte mischen: f-Strings", r"""
    ## Zwei Wege, Text und Werte zu mischen

    :::vergleich Weg 1: umwandeln und verketten | Weg 2: f-String (besser!)
        n = 5
        print('Info: ' + str(n) + ' Dateien heruntergeladen')
    Umständlich: str() nicht vergessen, Leerzeichen selbst setzen.
    |||
        n = 5
        print(f'Info: {n} Dateien heruntergeladen')
    Übersichtlich: Der Wert steht direkt an seinem Platz.
    :::

    So funktioniert ein **Formatierungsstring** (kurz **f-String**):
      • Vor das Anführungszeichen kommt ein `f`.
      • In geschweifte Klammern `{ }` schreibst du Variablen oder Rechnungen.
      • Python setzt dort den Wert ein (und wandelt ihn selbst in Text um).

    :::analogie ✉️ Der Serienbrief
    Ein f-String ist wie ein Serienbrief: „Liebe Person {name}, du hast
    {punkte} Punkte!“ Der Text bleibt gleich, nur die Lücken in `{ }` werden
    für jede Person mit den passenden Werten gefüllt. Fehlt das `f`, wird der
    Brief mit den leeren Platzhaltern verschickt.
    :::

    :::achtung Das f vergessen
    `print("Info: {n}")` gibt wörtlich `Info: {n}` aus. Ohne `f` sind die
    geschweiften Klammern ganz normale Zeichen.
    :::
    """)

k.ausgabe("n = 5\nprint(f'Info: {n} Dateien heruntergeladen')",
          "Im f-String wird {n} durch den Wert von n ersetzt.")
k.ausgabe('name = "Lea"\nalter = 19\nprint(f"{name} ist {alter} Jahre alt.")',
          "Beide Platzhalter werden ersetzt.")
k.ausgabe('print("3 + 4 = {3 + 4}")',
          "Hier fehlt das f vor dem String! Dann sind die { } ganz normale Zeichen "
          "und es wird nichts eingesetzt.",
          tipp="Schau genau hin: Steht vor dem String ein f?")
k.text("Welcher Buchstabe muss vor dem Anführungszeichen eines Formatierungsstrings stehen?",
       ["f"],
       "f wie 'formatiert': f'Hallo {name}'")
k.mc("Welche Klammern benutzt man in f-Strings für die Platzhalter?",
     ["Geschweifte Klammern { }", "Runde Klammern ( )", "Eckige Klammern [ ]", "Spitze Klammern < >"],
     "f'Info: {n} Dateien' – die Variable kommt in geschweifte Klammern.")

# ── Erklärung 3: Rechnen im f-String ─────────────────────────────────────
k.erklaerung("Rechnen im f-String", r"""
    ## In den Klammern darf gerechnet werden

    In `{ }` darf jeder Ausdruck stehen – also auch eine Rechnung. Außerhalb
    der Klammern ist alles normaler Text:

    :::code
    y = 4.5
    print(f'Y hat den Wert {y}!')
    print(f'Y+5 hat den Wert {y + 5}!')
    print(f"3 + 4 = {3 + 4}")
    :::

    !! Rechnungen in { } werden ausgerechnet, alles außerhalb bleibt Text.
    """)

k.ausgabe('print(f"3 + 4 = {3 + 4}")',
          "Außerhalb der { } ist alles normaler Text ('3 + 4 = '). In den { } wird "
          "gerechnet: 7.")
k.ausgabe('preis = 2.5\nmenge = 4\nprint(f"Gesamt: {preis * menge} Euro")',
          "In { } darf gerechnet werden: 2.5 * 4 = 10.0 (float mal int ergibt float).")
k.ausgabe('a = 7\nb = 2\nprint(f"{a} // {b} = {a // b}")',
          "Nur der dritte Platzhalter enthält eine Rechnung. Die ersten beiden setzen "
          "einfach die Werte ein, das // dazwischen ist Text: 7 // 2 = 3")

# ── Erklärung 4: input() ─────────────────────────────────────────────────
k.erklaerung("Eingabe mit input()", r"""
    ## input() – das Programm fragt nach

    `input()` ist das Gegenstück zu `print()`: Das Programm hält an und
    WARTET, bis jemand etwas tippt und Enter drückt.

    :::analogie 🧑‍🍳 Die Bedienung im Restaurant
    Die Bedienung fragt: „Was darf’s sein?“ (das ist der Text in den
    Klammern) und wartet, bis du antwortest. Deine Antwort schreibt sie
    IMMER als Text auf ihren Block – auch wenn du „2“ sagst. Rechnen kann
    die Küche damit erst, wenn jemand aus dem Text eine Zahl macht.
    :::

    :::visual ablauf
    {"schritte": [{"icon": "⏸️", "text": "Programm zeigt den Text und hält an"},
                  {"icon": "⌨️", "text": "Du tippst etwas und drückst Enter"},
                  {"icon": "📝", "text": "input() liefert das Getippte als str"},
                  {"icon": "🔄", "text": "Bei Bedarf umwandeln: int() oder float()"}]}
    :::

        x = input()                            # wartet ohne Text
        n = input('Bitte gib eine Zahl an: ')  # zeigt erst den Text an

    !! input() gibt IMMER einen String (str) zurück – auch bei Ziffern!
    ---
    ## Mit Eingaben rechnen

    :::code eingaben=Anna|17
    name = input("Wie heißt du? ")
    alter = int(input("Wie alt bist du? "))
    print(f"Hallo {name}, in 3 Jahren bist du {alter + 3}.")
    :::

    :::achtung Umwandeln nicht vergessen
    Ohne `int()` wäre `alter + 3` ein TypeError (str + int). Und wer
    Kommazahlen wie `2.5` erwartet, braucht `float()` – `int("2.5")` gibt
    einen ValueError.
    :::
    """)

k.mc("Welchen Datentyp liefert input() zurück?",
     ["Immer str", "int, wenn man eine Zahl eintippt", "Immer int", "bool"],
     "input() liefert IMMER einen String – auch bei der Eingabe '42'.")
k.mc("Der Nutzer tippt 5 ein. Was passiert?",
     ["Ein TypeError, weil x ein String ist",
      "Es wird 6 ausgegeben",
      "Es wird 51 ausgegeben",
      "Es wird 5 ausgegeben"],
     "x ist der String '5'. '5' + 1 (str + int) → TypeError. Lösung: x = int(input('Zahl: '))",
     code="x = input('Zahl: ')\nprint(x + 1)")
k.mc("Wie liest du eine ganze Zahl vom Nutzer ein?",
     ["zahl = int(input('Zahl: '))",
      "zahl = input(int('Zahl: '))",
      "zahl = input('Zahl: ').int",
      "zahl = number(input('Zahl: '))"],
     "Erst input() (liefert str), dann das Ergebnis mit int() umwandeln. Von innen nach außen!")
k.mc("Das Programm fragt nach einem Preis. Jemand tippt 2.5 ein. Was passiert?",
     ["ValueError – '2.5' ist keine Ganzzahl",
      "preis wird 2",
      "preis wird 2.5",
      "preis wird 3"],
     "int('2.5') scheitert, weil der Text einen Punkt enthält. Für Preise nimmt man "
     "float(input(...)).",
     code="preis = int(input('Preis: '))")

# ── Praxisteil ───────────────────────────────────────────────────────────
k.luecke("Ergänze den Code: Das Programm liest ein Alter als Zahl ein und gibt mit "
         "einem f-String aus, wie alt man in 5 Jahren ist.",
         """
         alter = ___(input("Wie alt bist du? "))
         print(___"In 5 Jahren bist du {___}.")
         """,
         [["int"], ["f", "F"], ["alter + 5", "5 + alter", "(alter + 5)", "(5 + alter)"]],
         "input() liefert Text, int() macht eine Zahl daraus. Das f vor dem String "
         "macht ihn zum f-String, und in { } darf gerechnet werden.",
         tipp="Umwandeln, f-String, Rechnung in den Klammern.")

k.code(r"""
    ## Info-Zeile

    Lies ein, wie viele Dateien heruntergeladen wurden, und gib diese Zeile aus
    (wie auf Folie 41):

        Eingabe:  5
        Ausgabe:  Info: 5 Dateien heruntergeladen

    Benutze einen f-String.
    """,
    [P(["5"], ["Info: 5 Dateien heruntergeladen"]),
     P(["0"], ["Info: 0 Dateien heruntergeladen"]),
     P(["12"], ["Info: 12 Dateien heruntergeladen"]),
     P(["7"], nicht=["{"], beschreibung="Platzhalter wurde ersetzt")],
    """
    n = input("Wie viele Dateien? ")
    print(f"Info: {n} Dateien heruntergeladen")
    """,
    "Hier musst du nicht einmal umwandeln: Du rechnest nicht, du setzt den Text "
    "nur ein. Der f-String erledigt den Rest.",
    tipps=["Speichere die Eingabe in einer Variable n.",
           "Ein f-String beginnt mit f vor dem Anführungszeichen, der Platzhalter ist {n}.",
           "print(f\"Info: {n} Dateien heruntergeladen\")"],
    streng=True)

k.code(r"""
    ## Celsius in Fahrenheit

    Lies eine Temperatur in Grad Celsius ein (sie kann Nachkommastellen haben)
    und rechne sie in Fahrenheit um: `F = C * 9 / 5 + 32`.

        Eingabe:  20
        Ausgabe:  20.0 °C sind 68.0 °F
    """,
    [P(["20"], ["20.0 °C sind 68.0 °F"]),
     P(["0"], ["0.0 °C sind 32.0 °F"]),
     P(["-40"], ["-40.0 °C sind -40.0 °F"], beschreibung="negative Temperatur"),
     P(["37.5"], ["37.5 °C sind 99.5 °F"], beschreibung="Kommazahl"),
     P(["100"], ["100.0 °C sind 212.0 °F"])],
    """
    celsius = float(input("Temperatur in °C: "))
    fahrenheit = celsius * 9 / 5 + 32
    print(f"{celsius} °C sind {fahrenheit} °F")
    """,
    "float() macht aus der Eingabe eine Kommazahl – deshalb steht auch bei 20 "
    "die Ausgabe 20.0. Punkt vor Strich sorgt dafür, dass erst multipliziert und "
    "geteilt, dann 32 addiert wird.",
    tipps=["Die Eingabe kann ein Komma-Wert sein – welche Umwandlung brauchst du?",
           "fahrenheit = celsius * 9 / 5 + 32",
           "print(f\"{celsius} °C sind {fahrenheit} °F\")"],
    streng=True)

k.code(r"""
    ## Pizza-Rechner

    Ihr bestellt Pizza und teilt die Rechnung. Schreibe ein Programm, das
      1. den Gesamtpreis einliest (eine Kommazahl, z.B. 25.5)
      2. die Anzahl der Personen einliest (eine ganze Zahl)
      3. ausgibt:   Jede Person zahlt <betrag> Euro

    Beispiel: 30 und 4  →  Jede Person zahlt 7.5 Euro
    (Runde nicht – gib das Ergebnis einfach so aus, wie Python es berechnet.)
    """,
    [P(["30", "4"], ["Jede Person zahlt 7.5 Euro"]),
     P(["25.5", "3"], ["Jede Person zahlt 8.5 Euro"]),
     P(["12", "1"], ["Jede Person zahlt 12.0 Euro"], beschreibung="nur eine Person"),
     P(["0", "5"], ["Jede Person zahlt 0.0 Euro"], beschreibung="Pizza geschenkt")],
    """
    preis = float(input("Gesamtpreis: "))
    personen = int(input("Anzahl Personen: "))
    print(f"Jede Person zahlt {preis / personen} Euro")
    """,
    "Der Preis braucht float() (er kann Nachkommastellen haben). "
    "int('25.5') würde einen ValueError erzeugen! Die Division mit / liefert "
    "immer einen float, deshalb steht auch bei 12 / 1 die Ausgabe 12.0.",
    tipps=["Zwei Eingaben: eine Kommazahl und eine ganze Zahl.",
           "Preis mit float(input(...)), Personen mit int(input(...)), dann teilen mit /.",
           "print(f\"Jede Person zahlt {preis / personen} Euro\")"],
    streng=True)

k.code(r"""
    ## Kassenbon mit end=

    Lies den Namen eines Artikels, den Preis (Kommazahl) und die Menge (ganze
    Zahl) ein. Gib dann EINE Zeile aus – aber mit ZWEI print-Aufrufen:

      1. `print(artikel, end=": ")` schreibt den Artikel und einen Doppelpunkt,
         ohne die Zeile zu beenden.
      2. Das zweite print schreibt Menge, Preis und Gesamtpreis dahinter.

    Beispiel:

        Eingaben:  Brezel, 0.5, 4
        Ausgabe:   Brezel: 4 x 0.5 = 2.0
    """,
    [P(["Brezel", "0.5", "4"], ["Brezel: 4 x 0.5 = 2.0"]),
     P(["Kaffee", "2.0", "3"], ["Kaffee: 3 x 2.0 = 6.0"]),
     P(["Wasser", "1.25", "2"], ["Wasser: 2 x 1.25 = 2.5"]),
     P(["Kekse", "1.5", "0"], ["Kekse: 0 x 1.5 = 0.0"], beschreibung="Menge 0")],
    """
    artikel = input("Artikel: ")
    preis = float(input("Preis: "))
    menge = int(input("Menge: "))
    print(artikel, end=": ")
    print(menge, "x", preis, "=", menge * preis)
    """,
    "Nach dem ersten print steht dank end=\": \" kein Zeilenumbruch, sondern ein "
    "Doppelpunkt mit Leerzeichen. Das zweite print schreibt direkt dahinter. Mehrere "
    "Werte mit Komma werden durch Leerzeichen getrennt.",
    pflicht=["end"],
    tipps=["Erst die drei Eingaben lesen und umwandeln (str, float, int).",
           "print(artikel, end=\": \") beendet die Zeile nicht.",
           "print(menge, \"x\", preis, \"=\", menge * preis)"],
    streng=True)

k.zusammenfassung(r"""
    ## Das Wichtigste aus Kapitel 7

        print()                         # leere Zeile
        print("Alter:", 19)             # Alter: 19   (Leerzeichen dazwischen)
        print("Hallo", end="")          # kein Zeilenumbruch danach
        print(f"{name} ist {alter}")    # f-String: Werte einsetzen
        print(f"Summe: {a + b}")        # in { } darf gerechnet werden

    !! input() liefert IMMER einen str – zum Rechnen umwandeln!

    | Eingabe soll sein ... | so liest du sie ein |
    |---|---|
    | Text | `name = input("Name: ")` |
    | ganze Zahl | `anzahl = int(input("Anzahl: "))` |
    | Kommazahl | `preis = float(input("Preis: "))` |

      • f vergessen → `{n}` wird wörtlich ausgegeben.
      • `int("2.5")` → ValueError, dafür `float()` nehmen.
      • Muster für kleine Programme: Eingabe → Verarbeitung → Ausgabe.
    """)
