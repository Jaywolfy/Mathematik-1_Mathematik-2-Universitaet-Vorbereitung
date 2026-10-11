# -*- coding: utf-8 -*-
"""Kapitel: Übungsblatt 2 – Verzweigungen und Listen (alle Aufgaben aus Übung 2)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="uebung2",
    titel="Übungsblatt 2 – Verzweigungen und Listen",
    beschreibung="Alle Aufgaben der Übung 2 zum Selbstlösen mit automatischer Prüfung",
    quelle="Übung 2",
    teil="tag2",
    icon="📄")

k.lernziele([
    "Ich kann alle Aufgaben von Übungsblatt 2 selbstständig lösen",
    "Ich kann Fehlermeldungen einer Fehlerart zuordnen und die Ursache beheben",
    "Ich kann Programme mit input(), f-Strings und if/elif/else schreiben",
    "Ich kann Listen über Indizes, while-Schleifen und Slicing auswerten",
])

# ── Einleitung ──────────────────────────────────────────────────────────────
k.erklaerung("Worum geht es auf Übungsblatt 2?", r"""
    ## Das Übungsblatt im Überblick

    Hier findest du alle Aufgaben von **Übung 2 – Verzweigungen und
    Listen**. Jede Aufgabe nennt ihre Nummer vom Blatt, so findest du sie
    schnell wieder. Programmieraufgaben werden automatisch getestet.

    | Aufgabe | Thema | Passendes Kapitel |
    |---|---|---|
    | 1 | Variablen-Zuweisungen ergänzen | Variablen, Verzweigungen |
    | 2.1, 2.2 | Fehlertypen und Fehlersuche | Fehlermeldungen |
    | 3 | Logische Operatoren, Präzedenz | Logische Operatoren |
    | 4.1–4.3 | Eingabe und Verzweigungen | Ein-/Ausgabe, Verzweigungen |
    | 5.1, 5.2 | Listen, Indizes, Länge | Listen |
    | 5.3.1–5.3.3 | Slicing bei Listen und Text | Slicing |

    :::analogie 🏋️ Der Trainingsplan
    Die Vorlesung zeigt dir die Übungen, wie eine Trainerin im
    Fitnessstudio. Kräftiger wirst du aber erst, wenn du selbst trainierst.
      • Das Übungsblatt ist dein Trainingsplan: erst leichte Gewichte
        (Aufgabe 1 bis 3), dann schwerere (Aufgabe 4 und 5).
      • Die gestuften Tipps sind die Trainerin, die erst einen kleinen
        Hinweis gibt und erst später die ganze Bewegung vormacht.
      • Die Musterlösung nur anzuschauen ist wie Zuschauen beim
        Training: Es sieht leicht aus, bringt aber wenig Muskeln.
    :::

    :::achtung Erst selbst probieren
    Schreib zuerst deinen eigenen Code und lass ihn testen. Fehler sind
    hier ausdrücklich erwünscht: Aus den Testergebnissen lernst du am
    meisten. Hol dir Tipps Stufe für Stufe, bevor du die Lösung ansiehst.
    :::
    """)

# ── Aufgabe 1 ───────────────────────────────────────────────────────────────
_A1_VORLAGE = """variable1 = ...  # hier Zuweisung 1 einsetzen
variable2 = 3
variable3 = ...  # hier Zuweisung 2 einsetzen
variable2 = variable2 + variable1
if variable3 > 5:
    variable2 = 0
else:
    variable2 *= variable3
variable4 = ...  # hier Zuweisung 3 einsetzen
variable5 = ...  # hier Zuweisung 4 einsetzen
variable5 = variable5 + variable4
variable6 = ...  # hier Zuweisung 5 einsetzen
variable7 = variable6 > variable2 * 2
variable5 = variable5 + "c"
print(variable7)
print(variable2)
print(variable5)
"""

k.code(r"""
    ## Übung 2, Aufgabe 1 – Variablen-Zuweisungen

    Ergänze im Listing (im Editor) die fehlenden Variablenzuweisungen, so
    dass keine Fehler auftreten und am Ende die drei Zeilen `True`, `5`
    und `"abc"` in der Konsole ausgegeben werden.

    Ersetze nur die fünf `...` durch passende Werte. Alle anderen Zeilen
    bleiben, wie sie sind. Hinweis: `print` zeigt einen String ohne
    Anführungszeichen, in der Konsole steht also `abc`.

        True
        5
        abc
    """,
    [P(exakt=["True", "5", "abc"], beschreibung="genau die drei Zeilen True, 5, abc"),
     P(nachspann='print("Typ von variable2:", type(variable2).__name__)',
       erwartet=["Typ von variable2: int"],
       beschreibung="variable2 ist eine ganze Zahl (5, nicht 5.0)")],
    """
    variable1 = 2
    variable2 = 3
    variable3 = 1
    variable2 = variable2 + variable1
    if variable3 > 5:
        variable2 = 0
    else:
        variable2 *= variable3
    variable4 = "b"
    variable5 = "a"
    variable5 = variable5 + variable4
    variable6 = 11
    variable7 = variable6 > variable2 * 2
    variable5 = variable5 + "c"
    print(variable7)
    print(variable2)
    print(variable5)
    """,
    "Rückwärts denken hilft:\n\n"
    "  • **variable2 soll 5 sein.** Ist `variable3 > 5`, würde variable2 auf 0 gesetzt. "
    "Also muss `variable3 <= 5` sein, und dann gilt `variable2 = (3 + variable1) * variable3`. "
    "Damit das 5 ergibt, passt zum Beispiel `variable1 = 2` und `variable3 = 1` "
    "(auch `variable1 = -2` und `variable3 = 5` geht).\n"
    "  • **variable5 soll \"abc\" sein.** Am Ende wird \"c\" angehängt, davor wird "
    "`variable5 + variable4` gerechnet. Also `variable5 = \"a\"` und `variable4 = \"b\"`.\n"
    "  • **variable7 soll True sein.** `variable6 > variable2 * 2` heißt `variable6 > 10`, "
    "zum Beispiel `variable6 = 11`.\n\n"
    "Vorsicht mit Kommazahlen: `variable1 = 7` und `variable3 = 0.5` ergeben 5.0 statt 5.",
    pflicht=["variable2 = 3", "variable2 = variable2 + variable1", "if variable3 > 5:",
             "variable2 *= variable3", "variable5 = variable5 + variable4",
             "variable7 = variable6 > variable2 * 2",
             "print(variable7)", "print(variable2)", "print(variable5)"],
    tipps=["Arbeite rückwärts: Welche Werte müssen variable2, variable5 und variable7 am Ende haben?",
           "Für variable2 = 5 darf der if-Zweig nicht laufen (variable3 <= 5). Dann gilt "
           "(3 + variable1) * variable3 == 5.",
           "Eine Möglichkeit: variable1 = 2, variable3 = 1, variable4 = \"b\", variable5 = \"a\", "
           "variable6 = 11."],
    vorlage=_A1_VORLAGE)

# ── Aufgabe 2 ───────────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 2 – Fehler einordnen", r"""
    ## Drei Arten von Fehlern

    Die Vorlesung unterscheidet drei Fehlerarten. Man kann sie mit Fehlern
    in einem deutschen Satz vergleichen:

    | Fehlerart | Was ist falsch? | Satz-Vergleich | Typische Meldung |
    |---|---|---|---|
    | lexikalisch | ein „Wort“, das Python nicht kennt | „Ich gehe in den Supermakrt.“ | `NameError` |
    | syntaktisch | die „Grammatik“ | „Ich Supermarkt gehe den in.“ | `SyntaxError`, `IndentationError` |
    | semantisch | die Bedeutung, die Logik | „Ich trinke ein Brot.“ | `ZeroDivisionError`, `IndexError` |

    :::code
    zahl = 7
    print(zahl // 0)
    :::

    Die Zeile ist grammatisch einwandfrei, aber durch 0 teilen ist
    unmöglich: ein semantischer Fehler. Lies bei Fehlermeldungen immer die
    LETZTE Zeile: Dort stehen Fehlertyp und Beschreibung.
    """)

k.mc("Übung 2, Aufgabe 2.1: Welcher Fehlertyp und welche Fehlerart gehören zu   true  ?",
     ["NameError – lexikalischer Fehler",
      "SyntaxError – syntaktischer Fehler",
      "ZeroDivisionError – semantischer Fehler",
      "Kein Fehler, true ist ein Wahrheitswert"],
     "Python kennt das „Wort“ `true` (klein) nicht → `NameError: name 'true' is not defined`. "
     "Das ist ein lexikalischer Fehler. Richtig wäre `True`.")
k.mc("Übung 2, Aufgabe 2.1: Welcher Fehlertyp und welche Fehlerart gehören zu   4 +* 5  ?",
     ["SyntaxError – syntaktischer Fehler",
      "NameError – lexikalischer Fehler",
      "ZeroDivisionError – semantischer Fehler",
      "Kein Fehler, es ergibt 20"],
     "Zwei Rechenzeichen direkt hintereinander verletzen die „Grammatik“ von Python → "
     "`SyntaxError: invalid syntax`, ein syntaktischer Fehler.")
k.mc("Übung 2, Aufgabe 2.1: Welcher Fehlertyp und welche Fehlerart gehören zu   2 // 0  ?",
     ["ZeroDivisionError – semantischer Fehler",
      "SyntaxError – syntaktischer Fehler",
      "NameError – lexikalischer Fehler",
      "Kein Fehler, es ergibt 0"],
     "Die Schreibweise stimmt, aber durch 0 kann man nicht teilen → `ZeroDivisionError`. "
     "Die Bedeutung ist falsch: ein semantischer Fehler.")

_FRAGE_22 = "Übung 2, Aufgabe 2.2: Welcher Fehler tritt beim Ausführen auf? (Name des Fehlers genügt)"
k.ausgabe('''prinnt("Dillgurkensuppe gibt's heut' Mittag!")''',
          "Tippfehler im Funktionsnamen: `prinnt` gibt es nicht → `NameError`. Die Apostrophe "
          "im Text sind dagegen kein Problem, weil der String in doppelten Anführungszeichen "
          "steht. Korrektur: `print(...)`.",
          frage=_FRAGE_22)
k.ausgabe('print(Lorem ipsum !)',
          "Die Anführungszeichen fehlen. Python versucht, `Lorem ipsum !` als Code zu lesen, "
          "und versteht die Grammatik nicht → `SyntaxError`. Korrektur: `print(\"Lorem ipsum !\")`.",
          frage=_FRAGE_22)
k.ausgabe('print("Alter: " + 18)',
          "Text + Zahl geht nicht, Python wandelt nicht automatisch um → `TypeError: can only "
          "concatenate str (not \"int\") to str`. Korrektur: `str(18)` oder ein f-String.",
          frage=_FRAGE_22)
k.ausgabe('print("Hey guys, did you know that ...?)',
          "Das schließende Anführungszeichen fehlt. Der Text endet nie → `SyntaxError: "
          "unterminated string literal`.",
          frage=_FRAGE_22)

k.code(r"""
    ## Übung 2, Aufgabe 2.2 – Fehler beheben

    Im Editor stehen die vier Zeilen aus Aufgabe 2.2. Jede erzeugt einen
    Fehler. Korrigiere sie so, dass das Programm fehlerfrei läuft und die
    vier Texte genau so ausgibt (der Text selbst bleibt unverändert):

        Dillgurkensuppe gibt's heut' Mittag!
        Lorem ipsum !
        Alter: 18
        Hey guys, did you know that ...?
    """,
    [P(exakt=["Dillgurkensuppe gibt's heut' Mittag!", "Lorem ipsum !", "Alter: 18",
              "Hey guys, did you know that ...?"],
       beschreibung="alle vier Zeilen, Texte unverändert")],
    """
    print("Dillgurkensuppe gibt's heut' Mittag!")
    print("Lorem ipsum !")
    print("Alter: " + str(18))
    print("Hey guys, did you know that ...?")
    """,
    "1. `prinnt` → `print` (lexikalisch). 2. Anführungszeichen um den Text ergänzen "
    "(syntaktisch). 3. Die Zahl mit `str(18)` in Text umwandeln, oder `f\"Alter: {18}\"` "
    "(Typfehler). 4. Das schließende `\"` ergänzen (syntaktisch).",
    verboten=["prinnt"],
    tipps=["Führe das Programm aus und lies die letzte Zeile der Fehlermeldung.",
           "Zeile 1: Tippfehler. Zeile 2 und 4: Anführungszeichen. Zeile 3: Text und Zahl.",
           "Zeile 3: print(\"Alter: \" + str(18))"],
    vorlage='prinnt("Dillgurkensuppe gibt\'s heut\' Mittag!")\nprint(Lorem ipsum !)\n'
            'print("Alter: " + 18)\nprint("Hey guys, did you know that ...?)\n')

# ── Aufgabe 3 ───────────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 3 – Logische Operatoren", r"""
    ## Präzedenz Schritt für Schritt

    In Aufgabe 3 gilt immer `x = 6`, `y = 7`, `z = 0`, `a = False`. Gesucht
    ist jeweils der Wert von `b`. Werte in dieser Reihenfolge aus:

      1. Klammern
      2. Rechnen (`*` vor `+` und `-`)
      3. Vergleiche (`==`, `!=`, `<`, `<=`, `>`, `>=`)
      4. `not`
      5. `and`
      6. `or`

    So sieht das für einen ähnlichen Ausdruck aus (nicht aus der Aufgabe):

    :::trace
    x = 6
    y = 7
    rechnung = x + y * 2
    vergleich = rechnung > 15
    b = not x == y and vergleich
    print(rechnung, vergleich, b)
    :::

    `not x == y` bedeutet `not (x == y)`, weil Vergleiche vor `not`
    kommen. Auf dem Blatt fehlen bei `not (x == y)and` Leerzeichen. Das ist
    erlaubt, aber schwer lesbar. Hier stehen sie mit Leerzeichen.
    """)

_AUFGABEN_3 = [
    ("b = x > 5 or y < 7 and z != 0",
     "and zuerst: y < 7 ist False, z != 0 ist False → False and False = False. "
     "Dann x > 5 (True) or False = True."),
    ("b = x * y != y * x and x + z == 0",
     "Rechnen: x * y = 42, y * x = 42 → 42 != 42 ist False. `False and …` ist immer False."),
    ("b = not (x == y) and z <= 0",
     "x == y ist False, not False = True. z <= 0 ist 0 <= 0 = True. True and True = True."),
    ("b = x >= 11 or x < 9 and not (y == 2) and x + y * z > 0 or a",
     "x >= 11 ist False. Der and-Teil: x < 9 (True) and not (y == 2) (True) and "
     "6 + 7 * 0 = 6 > 0 (True) → True. False or True or a → True."),
    ("b = z != z or not a and x - y * z <= 0",
     "z != z ist False. not a ist True. x - y * z = 6 - 0 = 6, 6 <= 0 ist False. "
     "True and False = False. False or False = False."),
    ("b = not a and z < y - x",
     "not a ist True. y - x = 1, z < 1 → 0 < 1 ist True. True and True = True."),
]
for _nr, (_ausdruck, _erkl) in enumerate(_AUFGABEN_3, 1):
    k.ausgabe(f"x = 6\ny = 7\nz = 0\na = False\n{_ausdruck}\nprint(b)",
              _erkl,
              frage=f"Übung 2, Aufgabe 3.{_nr}: Welchen Wert hat b? (Ausgabe von print(b))",
              tipp="Erst rechnen, dann vergleichen, dann not, dann and, zuletzt or.")

# ── Aufgabe 4 ───────────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 4 – Eingabe und Verzweigungen", r"""
    ## f-Strings statt +

    In Aufgabe 4.1 sollst du für die Ausgabe **format-Strings** (f-Strings)
    benutzen und keine Verkettung mit `+`. In einem f-String schreibst du
    Variablen in geschweifte Klammern:

    :::code eingaben=Anna|5|3|2007
    name = input("Wie heißt du? ")
    tag = int(input("Tag: "))
    monat = int(input("Monat: "))
    jahr = int(input("Jahr: "))
    print(f"{name}: {tag}.{monat}.{jahr}")
    print(f"{name}: {tag:02d}.{monat:02d}.{jahr}")
    :::

    :::info Bonus: führende Nullen
    Das Format `tt.mm.jjjj` auf dem Blatt meint zweistellige Tage und
    Monate, also `05.03.2007`. Mit `{tag:02d}` füllt Python mit einer 0 auf
    zwei Stellen auf. `5.3.2007` wird hier ebenfalls als richtig gewertet.
    :::
    ---
    ## Alle Fälle bedenken

    Bei Aufgabe 4.2 und 4.3 hilft es, vorher alle Fälle aufzuschreiben.
    Für die Teilbarkeit von a und b gibt es drei:
      • b ist ein Vielfaches von a (`b % a == 0`),
      • a ist ein Vielfaches von b (`a % b == 0`),
      • keins von beiden.

    :::achtung Die 0
    `b % 0` löst einen `ZeroDivisionError` aus. Die Eingabe 0 musst du in
    dieser Aufgabe nicht beachten. Wer möchte, fängt sie mit einem eigenen
    `if` ab.
    :::
    """)

def _datum(name, tag, monat, jahr):
    """Alle erlaubten Schreibweisen: mit oder ohne führende Null (05.03. oder 5.3.)."""
    tage = sorted({f"{tag:02d}", str(tag)})
    monate = sorted({f"{monat:02d}", str(monat)})
    return tuple(f"{name} hat am {t}.{m}.{jahr} Geburtstag." for t in tage for m in monate)


k.code(r"""
    ## Übung 2, Aufgabe 4.1 – Variablen einlesen

    Schreibe ein Programm, das mit `input()` nacheinander einliest und in
    Variablen speichert:
      • deinen Namen als Zeichenkette,
      • dein Geburtsdatum als drei separate, ganze Zahlen: Tag, Monat, Jahr.

    Insgesamt sind das vier Eingaben. Die Eingabeaufforderungen sollen
    klar sagen, was erwartet wird (Bedienerfreundlichkeit). Danach gibst
    du aus:

        <Name> hat am <tt.mm.jjjj> Geburtstag.

    Benutze für die Ausgabe einen f-String, keine Verkettung mit `+`.

        Eingaben: Anna, 15, 11, 2006
        Ausgabe:  Anna hat am 15.11.2006 Geburtstag.
    """,
    [P(["Anna", "15", "11", "2006"], ["Anna hat am 15.11.2006 Geburtstag."]),
     P(["Lea Marie", "31", "12", "1999"], ["Lea Marie hat am 31.12.1999 Geburtstag."],
       beschreibung="Name mit Leerzeichen"),
     P(["Ben", "5", "3", "2007"], [_datum("Ben", 5, 3, 2007)],
       beschreibung="einstelliger Tag und Monat: Ben hat am 05.03.2007 (oder 5.3.2007) Geburtstag."),
     P(["Deniz", "1", "10", "2000"], [_datum("Deniz", 1, 10, 2000)],
       beschreibung="Deniz hat am 01.10.2000 (oder 1.10.2000) Geburtstag.")],
    """
    name = input("Wie heißt du? ")
    tag = int(input("Geburtstag – Tag (z. B. 15): "))
    monat = int(input("Geburtstag – Monat als Zahl (z. B. 11): "))
    jahr = int(input("Geburtstag – Jahr (z. B. 2006): "))
    print(f"{name} hat am {tag:02d}.{monat:02d}.{jahr} Geburtstag.")
    """,
    "Tag, Monat und Jahr werden mit `int()` zu ganzen Zahlen. Der f-String setzt alles "
    "ohne `+` zusammen. `{tag:02d}` sorgt für die führende Null (05 statt 5). Ohne `:02d` "
    "ist die Lösung hier auch richtig.",
    verboten=["+"],
    pflicht=["int("],
    tipps=["Du brauchst vier input()-Aufrufe. Die drei Zahlen wandelst du mit int() um.",
           "Die Ausgabe: print(f\"{name} hat am …\") – die Variablen kommen in geschweifte Klammern.",
           "print(f\"{name} hat am {tag}.{monat}.{jahr} Geburtstag.\")"],
    streng=True)

k.code(r"""
    ## Übung 2, Aufgabe 4.2 – Teilbarkeit

    1. Frage den Nutzer nach zwei ganzen Zahlen a und b.
    2. Ist eine Zahl ein Vielfaches der anderen, gib aus, welche ein
       Vielfaches von welcher ist, in dieser Form: `15 ist ein Vielfaches von 5`
    3. Andernfalls gib aus: `Kein Vielfaches`

        a=5,  b=15   →   15 ist ein Vielfaches von 5
        a=15, b=5    →   15 ist ein Vielfaches von 5
        a=5,  b=17   →   Kein Vielfaches

    Die Eingabe 0 musst du nicht beachten. Sind a und b gleich, ist jede
    Zahl ein Vielfaches der anderen (`7 ist ein Vielfaches von 7`).
    """,
    [P(["5", "15"], ["15 ist ein Vielfaches von 5"]),
     P(["15", "5"], ["15 ist ein Vielfaches von 5"], beschreibung="größere Zahl zuerst"),
     P(["5", "17"], ["Kein Vielfaches"], nicht=["ist ein Vielfaches"]),
     P(["7", "7"], ["7 ist ein Vielfaches von 7"], beschreibung="beide gleich"),
     P(["-3", "9"], ["9 ist ein Vielfaches von -3"], beschreibung="negative Zahl"),
     P(["6", "4"], ["Kein Vielfaches"], nicht=["ist ein Vielfaches"],
       beschreibung="gemeinsamer Teiler, aber kein Vielfaches")],
    """
    a = int(input("Erste ganze Zahl a: "))
    b = int(input("Zweite ganze Zahl b: "))
    if b % a == 0:
        print(f"{b} ist ein Vielfaches von {a}")
    elif a % b == 0:
        print(f"{a} ist ein Vielfaches von {b}")
    else:
        print("Kein Vielfaches")
    """,
    "Drei Fälle: b Vielfaches von a, a Vielfaches von b, keins von beiden. Teilbarkeit "
    "prüft man mit `%`: Rest 0 heißt teilbar. Wer nur `b % a == 0` prüft, verpasst den "
    "Fall a=15, b=5. Sonderfall 0: `b % 0` würde einen ZeroDivisionError auslösen.",
    pflicht=["%"],
    tipps=["Überlege dir vorab alle Fälle, die eintreten können. Es sind drei.",
           "b ist ein Vielfaches von a, wenn b % a == 0 gilt. Und umgekehrt?",
           "if b % a == 0: … elif a % b == 0: … else: print(\"Kein Vielfaches\")"],
    streng=True)

k.code(r"""
    ## Übung 2, Aufgabe 4.3 – Vergleiche

    1. Frage den Nutzer nach drei Ganzzahlen.
    2. Gib aus, wie viele Werte gleich sind, genau so:

        a=1, b=1, c=1   →   Drei gleiche Werte
        a=1, b=2, c=1   →   Zwei gleiche Werte
        a=1, b=2, c=3   →   Alle verschieden
    """,
    [P(["1", "1", "1"], ["Drei gleiche Werte"], nicht=["zwei gleiche", "alle verschieden"]),
     P(["1", "2", "1"], ["Zwei gleiche Werte"], nicht=["drei gleiche", "alle verschieden"],
       beschreibung="erste und dritte gleich"),
     P(["2", "2", "1"], ["Zwei gleiche Werte"], nicht=["drei gleiche", "alle verschieden"]),
     P(["4", "7", "7"], ["Zwei gleiche Werte"], nicht=["drei gleiche", "alle verschieden"]),
     P(["1", "2", "3"], ["Alle verschieden"], nicht=["gleiche werte"])],
    """
    a = int(input("Erste Zahl: "))
    b = int(input("Zweite Zahl: "))
    c = int(input("Dritte Zahl: "))
    if a == b and b == c:
        print("Drei gleiche Werte")
    elif a == b or b == c or a == c:
        print("Zwei gleiche Werte")
    else:
        print("Alle verschieden")
    """,
    "Reihenfolge ist wichtig: Erst auf „alle drei gleich“ prüfen! Sonst würde bei "
    "1, 1, 1 schon die Bedingung für „zwei gleiche“ zutreffen. Und das Paar a/c nicht "
    "vergessen.",
    tipps=["Welcher Fall muss zuerst geprüft werden, damit er nicht von einem anderen verdeckt wird?",
           "Erst: a == b and b == c. Dann mit or prüfen, ob irgendein Paar gleich ist.",
           "elif a == b or b == c or a == c: print(\"Zwei gleiche Werte\")"],
    streng=True)

# ── Aufgabe 5 ───────────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 5 – Listen und Slicing", r"""
    ## Zählen ab 0

    In Aufgabe 5.1 ist „jede zweite Zahl, beginnend mit der zweiten“
    gefragt. Die zweite Zahl hat den Index **1**, also geht es um die
    Indizes 1, 3, 5 und 7:

    :::visual liste
    {"name": "liste", "werte": [1, 1, 2, 3, 5, 8, 13, 21], "markiert": [1, 3, 5, 7], "negativ": false}
    :::

    `1 * 3 * 8 * 21 = 504`. Genau das steht als Kontrollwert auf dem Blatt.
    ---
    ## Die Variable liste wird vorgegeben

    In 5.1 und 5.2 legt das Quiz die Variable `liste` vor deinem Code an
    und testet mit verschiedenen Listen. Lege sie deshalb NICHT selbst an.
    Zum Ausprobieren im Editor kannst du kurz eine eigene Zeile wie
    `liste = [1, 1, 2, 3, 5, 8, 13, 21]` an den Anfang schreiben und sie vor
    dem Prüfen wieder löschen.

    :::achtung liste[len(liste)]
    Die Indizes laufen von 0 bis `len(liste) - 1`. Der Index `len(liste)`
    liegt immer eins hinter dem Ende → `IndexError`.
    :::
    """)

k.code(r"""
    ## Übung 2, Aufgabe 5.1 – Definition & Indizes

    Es gibt bereits eine Variable `liste` mit genau 8 Zahlen (vom Quiz
    vorgegeben, lege sie NICHT selbst an). Gib nacheinander aus, jeweils in
    einer eigenen Zeile:
      1. die Summe der Zahlen an den Indizes 1, 2 und 7,
      2. das Produkt jeder zweiten Zahl, beginnend mit der zweiten,
      3. die erste Zahl mal 300.

    Für diese Aufgabe brauchst du weder Schleifen noch Slicing.
    Kontrolle: Für `liste = [1,1,2,3,5,8,13,21]` ist das 24, 504 und 300.
    Für `liste = [-1,1,-1,1,-1,1,-1,1]` ist das 1, 1 und -300.
    """,
    [P(vorspann="liste = [1, 1, 2, 3, 5, 8, 13, 21]", exakt=["24", "504", "300"]),
     P(vorspann="liste = [-1, 1, -1, 1, -1, 1, -1, 1]", exakt=["1", "1", "-300"]),
     P(vorspann="liste = [2, 3, 4, 5, 6, 7, 8, 9]", exakt=["16", "945", "600"]),
     P(vorspann="liste = [0, 0, 0, 0, 0, 0, 0, 0]", exakt=["0", "0", "0"], beschreibung="nur Nullen")],
    """
    print(liste[1] + liste[2] + liste[7])
    print(liste[1] * liste[3] * liste[5] * liste[7])
    print(liste[0] * 300)
    """,
    "Die „zweite Zahl“ hat den Index 1, wegen der Zählung ab 0. Jede zweite ab da: "
    "Indizes 1, 3, 5, 7.",
    tipps=["Die erste Zahl hat Index 0, die zweite Index 1.",
           "Jede zweite ab der zweiten: Indizes 1, 3, 5, 7.",
           "print(liste[1] * liste[3] * liste[5] * liste[7])"])

k.mc("Übung 2, Aufgabe 5.2: Warum führt der Ausdruck   liste[len(liste)]   immer zu einem Fehler?",
     ["Weil die Indizes von 0 bis len(liste) - 1 laufen, len(liste) ist eins zu groß",
      "Weil len() nur bei Strings funktioniert",
      "Weil man Listen nicht mit Zahlen indizieren darf",
      "Tut es nicht, es liefert das letzte Element"],
     "Bei 4 Elementen sind die Indizes 0, 1, 2, 3. Der Index 4 = len(liste) existiert nicht → "
     "IndexError. Bei der leeren Liste ist schon liste[0] zu viel.")

k.code(r"""
    ## Übung 2, Aufgabe 5.2 – Alle Elemente ausgeben

    Es gibt bereits eine Variable `liste` (vom Quiz vorgegeben, beliebig
    lang, auch leer). Schreibe ein Programm, das alle Elemente der Reihe
    nach ausgibt, jedes in einer eigenen Zeile. Du kannst dafür eine
    while-Schleife verwenden.

    Nicht erlaubt: `print(liste)` und `str(liste)`.
    """,
    [P(vorspann='liste = ["Milch", "Brot", "Eier"]', exakt=["Milch", "Brot", "Eier"]),
     P(vorspann="liste = [3, 1, 4, 1, 5]", exakt=["3", "1", "4", "1", "5"]),
     P(vorspann="liste = []", exakt=[], beschreibung="leere Liste: keine Ausgabe"),
     P(vorspann="liste = [42]", exakt=["42"], beschreibung="nur ein Element")],
    """
    i = 0
    while i < len(liste):
        print(liste[i])
        i += 1
    """,
    "Die Bedingung `i < len(liste)` sorgt dafür, dass der letzte Index len(liste) - 1 ist. "
    "Bei einer leeren Liste läuft die Schleife kein einziges Mal, auch das passt.",
    verboten=["print(liste)", "str(liste)"],
    tipps=["Eine Zählvariable i läuft über alle Indizes.",
           "i = 0 und dann while i < len(liste): …",
           "Im Körper: print(liste[i]) und i += 1"],
    vorlage="i = 0\nwhile ...:\n    ...\n")

k.mc("Übung 2, Aufgabe 5.3.1: Wofür stehen a, b und c im Slicing-Ausdruck   [a:b:c]  ?",
     ["a = Start (inklusiv), b = Ende (exklusiv), c = Schrittweite und Richtung",
      "a = Start (exklusiv), b = Ende (inklusiv), c = Anzahl der Elemente",
      "a = Länge, b = Start, c = Ende",
      "a = Schrittweite, b = Start, c = Ende"],
     "start ist dabei, end nicht. Deshalb gilt `[1,2,3,4][1:3] == [2,3]`: Index 1 und 2.")
k.mc("Übung 2, Aufgabe 5.3.1: Welche Werte gelten, wenn a, b und c leer bleiben (also lst[::])?",
     ["start = 0, end = len(lst), step = 1",
      "start = 1, end = len(lst), step = 0",
      "start = 0, end = -1, step = 1",
      "Es gibt einen SyntaxError"],
     "Leer heißt: vom Anfang (0) bis ganz zum Ende (len(lst)) in Einerschritten (1). "
     "step = 0 wäre sogar verboten (ValueError).")
k.mc("Übung 2, Aufgabe 5.3.1: Und wenn nur c angegeben und negativ ist (zum Beispiel lst[::-1])?",
     ["start = letztes Element, end = vor dem Anfang, also ist Index 0 noch dabei",
      "start = 0, end = len(lst)",
      "start = -1, end = 0, also ist Index 0 nicht dabei",
      "Ein leerer Slice, weil start kleiner als end ist"],
     "Bei negativer Schrittweite drehen sich die Standardwerte um: Es geht hinten los und "
     "läuft bis VOR den Anfang. Eine Zahl dafür gibt es nicht (-1 wäre das letzte Element).")

_LST = {"lst": [8, 1, 3, -4, 5, 0, 2, 11]}
_LST2 = {"lst": [10, 20, 30, 40, 50, 60, 70, 80]}
_A532 = [
    ("Die gesamte Liste.", "lst[:]",
     "start und end weggelassen → alles. (`lst[0:8]` oder `lst[::]` gehen auch.)",
     "Lass start, end und step einfach leer."),
    ("Die gesamte Liste rückwärts.", "lst[::-1]",
     "Schrittweite -1 läuft rückwärts. start/end leer → automatisch die ganze Liste.",
     "Die Schrittweite (das dritte Feld) bestimmt die Richtung."),
    ("Jedes zweite Element, beginnend mit dem zweiten Element.", "lst[1::2]",
     "Das zweite Element hat Index 1. Mit Schrittweite 2 → Indizes 1, 3, 5, 7.",
     "Das zweite Element hat Index 1."),
    ("Nur das erste Element (mit Slicing, also als Liste).", "lst[:1]",
     "`lst[:1]` liefert die Liste `[8]`. (`lst[0]` wäre nur die Zahl 8, keine Liste.)",
     "Von Anfang bis VOR Index 1."),
    ("Das erste Element und jedes dritte danach, mit Indizes kleiner 7.", "lst[:7:3]",
     "Indizes 0, 3, 6 (9 wäre zu groß). end = 7 sorgt dafür, dass nur Indizes < 7 "
     "vorkommen. Ergebnis: `[8, -4, 2]`.",
     "start = 0 (oder leer), end = 7 (exklusiv!), step = 3."),
    ("Die Elemente an Index 6, 5, 4 und 3 (in dieser Reihenfolge).", "lst[6:2:-1]",
     "Start bei 6, rückwärts (step -1). end = 2, weil end exklusiv ist und Index 3 noch "
     "dabei sein soll.",
     "Rückwärts heißt step -1. Das Ende ist exklusiv: Wo musst du also aufhören?"),
]
for _nr, (_text, _loesung, _erkl, _tipp) in enumerate(_A532, 1):
    k.ausdruck(f"Übung 2, Aufgabe 5.3.2 ({_nr}): Finde einen Slicing-Ausdruck für lst. {_text}",
               [_LST, _LST2], _loesung, _erkl, tipp=_tipp, muss_enthalten=":")

k.ausdruck("Übung 2, Aufgabe 5.3.3: Finde einen Ausdruck mit Slicing, der True ergibt, wenn wort ein "
           "Palindrom ist, sonst False. Das Beispiel „Lagerregal“ soll als Palindrom erkannt werden.",
           [{"wort": "Lagerregal"}, {"wort": "Python"}, {"wort": "Otto"}, {"wort": "anna"},
            {"wort": "Reittier"}],
           "wort.lower() == wort.lower()[::-1]",
           "`wort == wort[::-1]` ist der Kern. Für „Lagerregal“ reicht das aber nicht: Rückwärts "
           "steht das große L am Ende, und `L` ist nicht `l`. Deshalb vorher mit `.lower()` "
           "alles klein machen.",
           tipp="Umdrehen geht mit [::-1]. Und denk an Groß- und Kleinschreibung!",
           muss_enthalten="[::-1]")

k.code(r"""
    ## Übung 2, Aufgabe 5.3.3 – Palindrom als Programm

    Lies ein Wort mit `input()` ein. Gib dann aus:
      • `Palindrom`, wenn es vorwärts und rückwärts gleich ist,
      • `Kein Palindrom` sonst.

    Benutze Slicing. Groß-/Kleinschreibung soll egal sein: „Lagerregal“
    ist ein Palindrom.
    """,
    [P(["Lagerregal"], ["Palindrom"], nicht=["kein"]),
     P(["Otto"], ["Palindrom"], nicht=["kein"]),
     P(["Python"], ["Kein Palindrom"]),
     P(["Reittier"], ["Palindrom"], nicht=["kein"]),
     P(["a"], ["Palindrom"], nicht=["kein"], beschreibung="ein einzelner Buchstabe")],
    """
    wort = input("Wort: ")
    if wort.lower() == wort.lower()[::-1]:
        print("Palindrom")
    else:
        print("Kein Palindrom")
    """,
    "Erst mit `.lower()` alles klein machen, dann mit `[::-1]` umdrehen und vergleichen. "
    "Ohne `.lower()` scheitert „Lagerregal“ (und „Otto“) am großen Anfangsbuchstaben.",
    pflicht=["[::-1]"],
    tipps=["Wie drehst du einen String mit Slicing um?",
           "Vergleiche das Wort mit seiner Umkehrung, aber vorher .lower() anwenden.",
           "if wort.lower() == wort.lower()[::-1]: …"],
    streng=True)

k.zusammenfassung(r"""
    ## Übungsblatt 2 auf einen Blick

    | Aufgabe | Kernidee |
    |---|---|
    | 1 | rückwärts rechnen: (3 + v1) · v3 = 5, v5 + v4 = "ab", v6 > 10 |
    | 2.1 | `true` → NameError (lexikalisch), `4 +* 5` → SyntaxError (syntaktisch), `2 // 0` → ZeroDivisionError (semantisch) |
    | 2.2 | NameError, SyntaxError, TypeError, SyntaxError |
    | 3 | Klammern → Rechnen → Vergleiche → not → and → or |
    | 4.1 | `int(input(...))` und f-String, `{tag:02d}` für 05 |
    | 4.2 | `b % a == 0` und `a % b == 0`, sonst „Kein Vielfaches“ |
    | 4.3 | erst „drei gleich“, dann „zwei gleich“ mit or |
    | 5.1 | Index ab 0: zweite Zahl = `liste[1]` |
    | 5.2 | `while i < len(liste):` |
    | 5.3 | `[start:end:step]`, Standard 0 / len / 1, rückwärts `[::-1]` |

        wort.lower() == wort.lower()[::-1]    # Palindrom-Test
        lst[6:2:-1]                           # Index 6, 5, 4, 3

    !! Lies Fehlermeldungen von unten: Fehlertyp und Grund stehen in der letzten Zeile.
    """)
