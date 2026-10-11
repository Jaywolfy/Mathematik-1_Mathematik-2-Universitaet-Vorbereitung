# -*- coding: utf-8 -*-
"""Kapitel: Übungsblatt 1 – Einstieg (alle sichtbaren Aufgaben aus Übung 1).

Hinweis für Autorinnen und Autoren: Das PDF enthält unsichtbaren Text
(KI-Fallen). Umgesetzt wird ausschließlich die SICHTBARE Aufgabenstellung.
Insbesondere gilt in Aufgabe 4.2: Erlaubt sind nur die Konstanten "1" und 0.
"""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="uebung1",
    titel="Übungsblatt 1 – Einstieg",
    beschreibung="Alle Aufgaben der Übung 1 zum Selbstlösen mit automatischer Prüfung",
    quelle="Übung 1",
    teil="tag1",
    icon="📄")

k.lernziele([
    "Ich kann alle Aufgaben von Übungsblatt 1 selbstständig lösen",
    "Ich kann Ausdrücke auswerten und den Datentyp des Ergebnisses bestimmen",
    "Ich kann vorhersagen, welche Konvertierungen gelingen und welche scheitern",
    "Ich kann eine Zahl nur aus vorgegebenen Bausteinen zusammensetzen",
    "Ich kann Fehler in einem Listing finden und Variablennamen beurteilen",
])

# ── Einleitung ───────────────────────────────────────────────────────────
k.erklaerung("Worum geht es auf Übungsblatt 1?", r"""
    ## Das Übungsblatt im Überblick

    Hier findest du alle Aufgaben von **Übung 1 – Einstieg**. Jede Aufgabe
    nennt ihre Nummer vom Blatt. Programmieraufgaben werden automatisch getestet.

    | Aufgabe | Thema | Passendes Kapitel |
    |---|---|---|
    | 1 | Python installieren | Wie Computer denken |
    | 2 | Theoriefragen (wahr/falsch) | mehrere |
    | 3.1, 3.2 | Code-Verständnis, Rechnen mit Typen | Datentypen, Operatoren |
    | 4.1, 4.2 | Konvertierung | Typumwandlung |
    | 5.1, 5.2 | Fehlersuche, Variablennamen | Variablen |
    | 6 | RSA (Bonus-Exkurs) | Operatoren (%, **) |

    :::analogie 🏋️ Der Trainingsplan
    Die Vorlesung zeigt dir die Übungen, wie eine Trainerin im Fitnessstudio.
    Kräftiger wirst du aber erst, wenn du selbst trainierst.
      • Das Übungsblatt ist dein Trainingsplan: erst leichte Gewichte
        (Aufgabe 1 bis 3), dann schwerere (Aufgabe 4 bis 6).
      • Die gestuften Tipps sind die Trainerin, die erst einen kleinen
        Hinweis gibt und später die ganze Bewegung vormacht.
      • Nur die Musterlösung anschauen ist wie beim Training zuschauen.
    :::
    ---
    ## Vor dem Start

    :::achtung Anführungszeichen nicht aus dem PDF kopieren
    Im PDF stehen typografische Anführungszeichen wie ’Lorem’ oder ”ipsum”.
    Kopierst du sie in Python, meldet es `SyntaxError: invalid character '’'`.
    Tippe Anführungszeichen immer selbst: `'Lorem'`, `"ipsum"`.
    :::

    :::info Aufgabe 1 – Python installieren
    Du brauchst eine (halbwegs) aktuelle Python-Installation. Eine Anleitung
    („Python Installieren für Dummies“) liegt im Moodle. Zum Schreiben reicht
    ein üblicher Texteditor – von einer IDE rät der Vorkurs eher ab. Auf den
    Poolrechnern ist Python schon installiert, der Befehl heißt `python3`.
    Mit `python3 --version` siehst du die installierte Version.
    :::
    """)

k.mc("Übung 1, Aufgabe 1: Womit sollst du im Vorkurs deine Programme schreiben?",
     ["Mit einem üblichen Texteditor – eine IDE ist nicht nötig",
      "Nur mit einer großen Entwicklungsumgebung (IDE)",
      "Mit einem Textverarbeitungsprogramm wie Word",
      "Direkt im Browser, eine Installation ist verboten"],
     "Ein üblicher Texteditor genügt. Von einer IDE rät der Vorkurs eher ab, damit "
     "du mehr lernst. Word ist ungeeignet: Es speichert Formatierungen und ersetzt "
     "Anführungszeichen durch typografische.")

k.text("Übung 1, Aufgabe 1: Mit welchem Befehl prüfst du auf einem Poolrechner, welche "
       "Python-Version installiert ist?",
       ["python3 --version", "python3 -V", "python3 –version"],
       "python3 --version (oder kurz python3 -V) zeigt z. B. 'Python 3.12.10'. Unter "
       "Windows heißt der Befehl meist python --version oder py --version.",
       tipp="Der Startbefehl auf dem Pool plus die Option für die Version.",
       gross_klein=True)  # python3 -v (klein) ist der "verbose"-Modus, nicht die Version

# ── Aufgabe 2 ────────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 2 – Theoriefragen", r"""
    ## Wahr oder falsch?

    Entscheide bei den fünf Aussagen vom Blatt, ob sie stimmen. Überlege
    jeweils, WARUM – die Erklärung nach der Antwort hilft dir dabei.

    Was du dafür brauchst:
      • `/` liefert immer einen float.
      • Variablennamen beginnen mit Buchstabe oder `_`.
      • `+` verbindet nur str mit str oder Zahl mit Zahl.
      • Verschachtelte Umwandlungen werden von innen nach außen ausgewertet.
      • Tab und Leerzeichen sind für Python verschiedene Zeichen.
    """)

k.wf("In Python ergibt der Ausdruck 5 / 2 den Wert 2.5.", True,
     "Richtig (Übung 1, Aufgabe 2). Die Division mit / liefert in Python immer einen "
     "float – auch bei zwei Ganzzahlen.")

k.wf("5y ist ein valider Variablenname.", False,
     "Falsch (Übung 1, Aufgabe 2). Variablennamen dürfen nicht mit einer Ziffer "
     "beginnen. y5 oder _5y wären gültig.")

k.wf('"2" + 5 wird ohne Fehler ausgeführt.', False,
     "Falsch (Übung 1, Aufgabe 2). str + int geht nicht → TypeError: can only "
     "concatenate str (not \"int\") to str. Python wandelt nicht automatisch um.")

k.wf('float(int(str(int("3")))) ist ein valider Ausdruck.', True,
     "Wahr (Übung 1, Aufgabe 2). Von innen nach außen: int('3') → 3, str(3) → '3', "
     "int('3') → 3, float(3) → 3.0. Jede Umwandlung funktioniert.")

k.wf("Es macht einen Unterschied, ob ich Tabs oder Spaces für die Einrückung verwende.", True,
     "Wahr (Übung 1, Aufgabe 2). Für Python sind Tab und Leerzeichen verschiedene "
     "Zeichen. Wer innerhalb eines Blocks mischt, bekommt einen TabError (eine Art "
     "IndentationError). Konsequent nur eine Sorte funktioniert – Konvention sind "
     "4 Leerzeichen.")

# ── Aufgabe 3.1 ──────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 3.1 – Code-Verständnis", r"""
    ## Korrekter Code? Welcher Typ?

    Überlege für jeden Ausdruck vom Blatt, ob er korrekten Python-Code
    darstellt und von welchem Datentyp er ist:

        2      10.0      true      'Lorem'      True      "ipsum"

    Zum Nachprüfen hilft `print(type(...))`. In den Fragen unten sagst du
    vorher, was herauskommt.

    :::info true ist ein Sonderfall
    `true` ist für Python kein Wert, sondern ein **Name**. Weil es keine
    Variable namens `true` gibt, meldet Python beim Ausführen einen
    **NameError**. Den Wahrheitswert schreibt man `True`.
    :::
    """)

for _code, _erkl, _akz in [
    ("print(type(2))", "2 ist eine Ganzzahl → int.", ["int"]),
    ("print(type(10.0))", "10.0 hat einen Punkt → float, auch wenn der Wert 'eigentlich' ganz ist.",
     ["float"]),
    ("print(type(true))", "true (klein) ist kein gültiger Wert. Python hält es für einen "
     "Variablennamen, den es nicht gibt → NameError. Richtig wäre True.", []),
    ("print(type('Lorem'))", "Einfache Anführungszeichen erzeugen einen str.", ["str"]),
    ("print(type(True))", "True (groß) ist ein Wahrheitswert → bool.", ["bool"]),
    ('print(type("ipsum"))', "Doppelte Anführungszeichen erzeugen genauso einen str wie einfache.",
     ["str"]),
]:
    k.ausgabe(_code, "Übung 1, Aufgabe 3.1: " + _erkl, akzeptiert=_akz,
              frage="Übung 1, Aufgabe 3.1: Was gibt dieser Code aus? (Bei einem Fehler: "
                    "den Namen des Fehlers)")

# ── Aufgabe 3.2 ──────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 3.2 – Mathe 0 für Informatiker", r"""
    ## Ergebnis UND Typ

    Überlege, was die Ausdrücke ergeben und für welche Rechenoperation die
    Symbole stehen. Beachte die **Präzedenz** und lass dir **immer auch den
    Datentyp** des Ergebnisses ausgeben:

        16 + 26
        12 * 123 // 28 - 15
        5 * 3 + 6 * 6
        13.75 + 28.67
        2**6 + 2**3 + 2**1
        5.4 * 7.7

    Tipp: `print(wert, type(wert))` gibt beides in einer Zeile aus.

    :::code
    print(16 + 26, type(16 + 26))
    :::
    """)

k.ausgabe("print(12 * 123 // 28 - 15)",
          "Übung 1, Aufgabe 3.2: Bei gleichem Rang von links nach rechts: 12 * 123 = 1476, "
          "dann 1476 // 28 = 52 (52 · 28 = 1456, Rest 20), dann 52 - 15 = 37.",
          tipp="* und // haben den gleichen Rang → von links nach rechts.")
k.ausgabe("print(5 * 3 + 6 * 6)",
          "Übung 1, Aufgabe 3.2: Punkt vor Strich: 15 + 36 = 51.")
k.ausgabe("print(2**6 + 2**3 + 2**1)",
          "Übung 1, Aufgabe 3.2: Potenzen zuerst: 64 + 8 + 2 = 74.")
k.ausgabe("print(5.4 * 7.7)",
          "Übung 1, Aufgabe 3.2: Mathematisch wäre das 41.58. Python zeigt aber "
          "41.580000000000005 – Fließkommazahlen haben eine begrenzte Genauigkeit! "
          "Wenn du 41.58 getippt hast, lassen wir das gelten.",
          akzeptiert=["41.58"])
k.mc("Übung 1, Aufgabe 3.2: Welchen Typ hat das Ergebnis von   12 * 123 // 28 - 15  ?",
     ["int", "float", "str", "bool"],
     "Alle Operanden sind Ganzzahlen, und // liefert bei Ganzzahlen eine Ganzzahl. "
     "Nur / würde einen float erzeugen.")
k.mc("Übung 1, Aufgabe 3.2: Welchen Typ hat das Ergebnis von   13.75 + 28.67  ?",
     ["float", "int", "str", "bool"],
     "Zwei Fließkommazahlen ergeben eine Fließkommazahl: 42.42 (float).")

k.code(r"""
    ## Übung 1, Aufgabe 3.2 – Ergebnis und Typ ausgeben

    Schreibe ein Programm, das für jeden der sechs Ausdrücke das Ergebnis UND
    seinen Datentyp in einer Zeile ausgibt – in der Reihenfolge vom Blatt:

        16 + 26
        12 * 123 // 28 - 15
        5 * 3 + 6 * 6
        13.75 + 28.67
        2**6 + 2**3 + 2**1
        5.4 * 7.7

    Die erste Zeile der Ausgabe lautet also `42 <class 'int'>`. Python soll
    rechnen – die Ergebnisse darfst du nicht selbst eintippen.
    """,
    [P(exakt=["42 <class 'int'>", "37 <class 'int'>", "51 <class 'int'>",
              "42.42 <class 'float'>", "74 <class 'int'>",
              "41.580000000000005 <class 'float'>"], beschreibung="sechs Zeilen: Wert und Typ"),
     P(erwartet=["41.580000000000005 <class 'float'>"], beschreibung="letzte Zeile (float!)")],
    """
    print(16 + 26, type(16 + 26))
    print(12 * 123 // 28 - 15, type(12 * 123 // 28 - 15))
    print(5 * 3 + 6 * 6, type(5 * 3 + 6 * 6))
    print(13.75 + 28.67, type(13.75 + 28.67))
    print(2**6 + 2**3 + 2**1, type(2**6 + 2**3 + 2**1))
    print(5.4 * 7.7, type(5.4 * 7.7))
    """,
    "print() mit zwei Werten setzt ein Leerzeichen dazwischen. Ganzzahlen mit +, *, "
    "// und ** bleiben int, sobald ein float beteiligt ist, wird das Ergebnis float. "
    "Wer mag, speichert jeden Ausdruck erst in einer Variable: x = 16 + 26, dann "
    "print(x, type(x)).",
    verboten=["42", "37", "51", "74", "41.58", "41.580000000000005"],
    tipps=["print(wert, type(wert)) gibt Wert und Typ in einer Zeile aus.",
           "Schreib den Ausdruck zweimal: einmal als Wert, einmal in type().",
           "print(16 + 26, type(16 + 26)) – und genauso für die anderen fünf."])

# ── Aufgabe 4.1 ──────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 4.1 – Konvertierung: Grundlagen", r"""
    ## Was kommt heraus – und was klappt nicht?

    Führe diese Konvertierungen durch und notiere die Ergebnisse. Welche
    funktionieren nicht?

    | Nr. | Konvertierung | in Python |
    |---|---|---|
    | 1 | 3.17 → int | `int(3.17)` |
    | 2 | 'a' → int | `int('a')` |
    | 3 | 5 → float | `float(5)` |
    | 4 | '5' → int | `int('5')` |
    | 5 | 3.1415 → string | `str(3.1415)` |
    | 6 | 5 → bool | `bool(5)` |
    | 7 | 'false' → bool | `bool('false')` |

    :::info Auf dem Blatt steht „string“
    Gemeint ist der Python-Typ `str`. Die Funktion heißt deshalb `str()` –
    `string(3.1415)` kennt Python nicht und meldet einen NameError.
    :::

    Wenn eine Konvertierung nicht möglich ist, nennst du einfach den
    Fehlertyp und den Grund.
    """)

for _code, _erkl, _akz in [
    ("print(int(3.17))", "int() schneidet die Nachkommastellen ab: 3.", []),
    ("print(int('a'))", "'a' ist kein Zahltext → int() kann es nicht umwandeln → ValueError. "
     "Das ist die Konvertierung, die nicht funktioniert.", []),
    ("print(float(5))", "Aus der Ganzzahl 5 wird die Kommazahl 5.0.", []),
    ("print(int('5'))", "Der Text '5' stellt eine Ganzzahl dar → 5.", []),
    ("print(type(str(3.1415)))", "str() macht aus der Zahl den Text '3.1415' → Typ str.", ["str"]),
    ("print(bool(5))", "Alles, was nicht 0 ist, wird zu True.", []),
    ("print(bool('false'))", "Überraschung! 'false' ist ein NICHT-LEERER Text, also True. "
     "bool() liest den Inhalt nicht, es prüft nur: leer oder nicht?", []),
]:
    k.ausgabe(_code, "Übung 1, Aufgabe 4.1: " + _erkl, akzeptiert=_akz,
              frage="Übung 1, Aufgabe 4.1: Was gibt dieser Code aus? (Bei einem Fehler: "
                    "den Namen des Fehlers)")

k.mc("Übung 1, Aufgabe 4.1: Welche der sieben Konvertierungen funktioniert NICHT?",
     ["'a' → int", "3.17 → int", "'false' → bool", "3.1415 → string (mit str())"],
     "Nur int('a') scheitert mit einem ValueError: 'a' stellt keine Zahl dar. "
     "int(3.17) schneidet ab (3), bool('false') ist True (nicht leer), str(3.1415) "
     "ergibt '3.1415'.")

k.code(r"""
    ## Übung 1, Aufgabe 4.1 – alle funktionierenden Konvertierungen

    Schreibe ein Programm, das die Ergebnisse der SECHS funktionierenden
    Konvertierungen aus Aufgabe 4.1 untereinander ausgibt (in der Reihenfolge
    vom Blatt, die nicht funktionierende `int('a')` lässt du weg):

        3.17 → int,  5 → float,  '5' → int,
        3.1415 → str,  5 → bool,  'false' → bool
    """,
    [P(exakt=["3", "5.0", "5", "3.1415", "True", "True"], beschreibung="sechs Ergebnisse")],
    """
    print(int(3.17))
    print(float(5))
    print(int('5'))
    print(str(3.1415))
    print(bool(5))
    print(bool('false'))
    """,
    "int() schneidet ab, float() hängt .0 an, int('5') liest den Zahltext, str() "
    "macht Text daraus, und bool() liefert für alles außer 0 bzw. leerem Text True – "
    "auch für 'false'.",
    pflicht=["int(", "float(", "str(", "bool("],
    verboten=["True"],
    tipps=["Für jede Konvertierung ein print() mit der passenden Funktion.",
           "Die Funktionen heißen int(), float(), str() und bool().",
           "print(int(3.17)), print(float(5)), print(int('5')), print(str(3.1415)), "
           "print(bool(5)), print(bool('false'))"])

# ── Aufgabe 4.2 ──────────────────────────────────────────────────────────
# Die SICHTBAREN Regeln von Aufgabe 4.2 prüft die Engine am Syntaxbaum (regeln=...):
# nur die Konstanten "1" (str) und 0 (int), beide mindestens einmal, nur int()/str()/print().
_REGELN_219 = ['nur_konstanten:["1", 0]', 'pflicht_konstanten:["1", 0]',
               "nur_funktionen:int|str|print"]

k.erklaerung("Aufgabe 4.2 – Überkomplizierte Eingabe", r"""
    ## 219 aus "1" und 0 bauen

    Die Regeln vom Blatt:
      • Erlaubt sind nur die Stringkonstante `"1"` und die Zahlenkonstante `0`.
      • Dazu die Konvertierungsfunktionen `int()` und `str()`.
      • Arithmetische und String-Operationen (`+`, `-`, `*`, ...) sind erlaubt.
      • **Keine weiteren Konstanten** wie z. B. `2` oder `"19"`.
      • Beide Konstanten sollen mindestens einmal (sinnvoll) vorkommen.

    Das Beispiel vom Blatt: Mit `"1" + str(0)` bekommt man `"10"`. Das kann
    man wieder in einen Integer umwandeln und damit weiterrechnen:

    :::visual ablauf
    {"schritte": [{"icon": "🔤", "text": "\"1\" + str(0)  →  \"10\""},
                  {"icon": "🔢", "text": "int(\"10\")  →  10"},
                  {"icon": "🧮", "text": "damit weiterrechnen …"},
                  {"icon": "🎯", "text": "… bis die Ganzzahl 219 entsteht"}]}
    :::

    :::analogie 🧱 Bauen mit nur zwei Steinsorten
    Du hast nur zwei Sorten Bausteine: die Ziffer „1“ als Text und die Zahl 0.
    Durch Rechnen (+, -) machst du aus ihnen neue Zahlen, durch Aneinanderkleben
    von Text neue Ziffernfolgen. Mit `str()` und `int()` wechselst du zwischen
    den beiden Welten hin und her.
    :::
    """)

k.code(r"""
    ## Übung 1, Aufgabe 4.2 – Überkomplizierte Eingabe

    Kombiniere die Konstanten so, dass sich am Ende die **Ganzzahl 219** ergibt.
    Speichere sie in der Variable `ergebnis` und gib sie mit `print(ergebnis)` aus.

    Regeln (vom Blatt):
      • Als Konstanten sind NUR `"1"` und `0` erlaubt – beide mindestens einmal.
      • Funktionen: `int()` und `str()` (und `print()` für die Ausgabe).
      • Arithmetische und String-Operationen sind erlaubt.
      • Keine weiteren Konstanten wie `2` oder `"19"` – auch nicht im
        `print()` oder als Text in Anführungszeichen. Kommentare mit `#` sind ok.

    Die Tests prüfen die Regeln automatisch.
    """,
    [P(exakt=["219"], beschreibung="Ausgabe 219"),
     F("ergebnis", 219, beschreibung="ergebnis ist 219"),
     F("type(ergebnis).__name__", "int", beschreibung="ergebnis ist eine Ganzzahl (int), kein Text")],
    """
    eins = int("1")
    zwei = eins + eins
    zehn = int("1" + str(0))
    neun = zehn - eins
    ergebnis = int(str(zwei) + "1" + str(neun))
    print(ergebnis)
    """,
    "Idee: Die Ziffern 2, 1 und 9 einzeln bauen und als TEXT aneinanderkleben. "
    "int(\"1\") ist 1, 1 + 1 ist 2, int(\"1\" + str(0)) ist 10, 10 - 1 ist 9. "
    "Dann str(2) + \"1\" + str(9) = \"219\", und int() macht daraus die Ganzzahl 219. "
    "Andere Wege sind genauso richtig, solange nur \"1\" und 0 als Konstanten vorkommen.",
    regeln=_REGELN_219,
    pflicht=["int(", "str("],
    tipps=["Welche einzelnen Ziffern stecken in 219? Wie bekommst du sie aus \"1\" und 0?",
           "int(\"1\") ist 1, und mit \"1\" + str(0) bekommst du \"10\". 1 + 1 = 2, 10 - 1 = 9.",
           "Baue die Ziffern einzeln, wandle sie mit str() in Text, klebe \"2\" + \"1\" + \"9\" "
           "zusammen und mach am Ende mit int() eine Zahl daraus."],
    vorlage="# Erlaubte Konstanten: \"1\" und 0\n\nergebnis = ...\nprint(ergebnis)\n")

# ── Aufgabe 5.1 ──────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 5.1 – Fehlersuche", r"""
    ## Warum stürzt dieses Listing ab?

        meinAlter = 21
        meinalter = meinalter + 1
        print(meinAlter)

    Beim Ausführen der zweiten Zeile wirft Python einen Fehler. Warum?
    Verbessere das Listing.

    :::achtung Ganz genau hinschauen
    Vergleiche die Namen Buchstabe für Buchstabe. Python ist **case-sensitive**.
    :::
    """)

k.ausgabe("meinAlter = 21\nmeinalter = meinalter + 1\nprint(meinAlter)",
          "Übung 1, Aufgabe 5.1: In Zeile 2 steht rechts meinalter (kleines a). Diese "
          "Variable gibt es noch nicht – Python unterscheidet Groß- und Kleinschreibung! "
          "→ NameError: name 'meinalter' is not defined. Did you mean: 'meinAlter'?",
          tipp="Schau ganz genau auf die Schreibweise der Namen in Zeile 1 und 2.")

k.mc("Übung 1, Aufgabe 5.1: Warum gibt es in Zeile 2 einen Fehler?",
     ["meinalter wurde nie ein Wert zugewiesen – meinAlter ist wegen des großen A ein anderer Name",
      "Man darf eine Variable nicht mit sich selbst addieren",
      "Variablennamen dürfen keine Großbuchstaben enthalten",
      "21 + 1 ist zu groß für eine Variable"],
     "Python ist case-sensitive. meinalter und meinAlter sind zwei verschiedene Namen. "
     "Rechts vom = soll meinalter gelesen werden, das gibt es aber nicht → NameError.")

k.code(r"""
    ## Übung 1, Aufgabe 5.1 – Listing verbessern

    Die Vorlage enthält das fehlerhafte Listing vom Blatt. Verbessere es so,
    dass das Alter um 1 erhöht und `22` ausgegeben wird. Behalte dabei den
    Variablennamen `meinAlter` bei (die Tests prüfen ihn).
    """,
    [P(exakt=["22"], beschreibung="Ausgabe 22"),
     F("meinAlter", 22)],
    """
    meinAlter = 21
    meinAlter = meinAlter + 1
    print(meinAlter)
    """,
    "In Zeile 2 muss es auf beiden Seiten meinAlter heißen (oder kurz: meinAlter += 1). "
    "Hinweis: Nach der Python-Konvention snake_case hieße die Variable eigentlich "
    "mein_alter.",
    verboten=["meinalter", "22"],
    tipps=["Führe den Code aus und lies die letzte Zeile der Fehlermeldung.",
           "Python schlägt dir sogar den richtigen Namen vor (Did you mean ...?).",
           "Zeile 2: meinAlter = meinAlter + 1"],
    vorlage="meinAlter = 21\nmeinalter = meinalter + 1\nprint(meinAlter)\n")

# ── Aufgabe 5.2 ──────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 5.2 – Gültigkeit & Konvention", r"""
    ## Gültig? snake_case?

    Zwei Fragen zu jedem Namen vom Blatt:
      1. Ist er ein **gültiger** Variablenname (akzeptiert Python ihn)?
      2. Entspricht er der Namenskonvention **snake_case**?

    | Regel | Bedeutung |
    |---|---|
    | gültig | beginnt mit Buchstabe oder `_`, danach nur Buchstaben, Ziffern, `_` |
    | snake_case | gültig UND nur Kleinbuchstaben (Wörter mit `_` getrennt) |

    :::info Umlaute
    Folie 27 sagt „keine … Sonderzeichen“. Umlaute wie Ä zählen für Python 3
    aber als Buchstaben – `ÄhmKeineAhnung` ist also gültig. In der Praxis
    vermeidet man sie trotzdem.
    :::
    """)

for _name, _antwort, _grund in [
    ("matrikel_nummer", "gültig UND snake_case",
     "Nur Kleinbuchstaben und Unterstrich – perfekt."),
    ("ÄhmKeineAhnung", "gültig, aber KEIN snake_case",
     "Python 3 erlaubt Umlaute in Namen – also gültig (auch wenn die Folie 'keine "
     "Sonderzeichen' sagt; Umlaute vermeidet man in der Praxis). Großbuchstaben und "
     "keine Unterstriche → kein snake_case."),
    ("2fancy4python", "UNGÜLTIG",
     "Beginnt mit einer Ziffer → verboten."),
    ("_meinAlter", "gültig, aber KEIN snake_case",
     "Unterstrich am Anfang ist erlaubt, aber das große A passt nicht zu snake_case "
     "(snake_case wäre: _mein_alter)."),
    ("richtig&gut", "UNGÜLTIG",
     "Das Zeichen & ist in Namen nicht erlaubt (es ist ein Operator)."),
    ("_2Euro", "gültig, aber KEIN snake_case",
     "Beginnt mit _ (erlaubt), danach Ziffer ist ok. Aber das große E → kein snake_case."),
    ("Variable2", "gültig, aber KEIN snake_case",
     "Gültig, aber das große V passt nicht zu snake_case (richtig wäre variable2)."),
    ("noch_besser", "gültig UND snake_case",
     "Alles klein, Wörter mit _ getrennt – genau so soll es sein."),
    ("#Falsch", "UNGÜLTIG",
     "Mit # beginnt in Python ein Kommentar – das kann kein Name sein."),
]:
    k.mc(f"Übung 1, Aufgabe 5.2: Was gilt für den Variablennamen   {_name}   ?",
         [_antwort] + [x for x in ("gültig UND snake_case", "gültig, aber KEIN snake_case",
                                   "UNGÜLTIG") if x != _antwort],
         _grund,
         tipp="Regeln: Beginn mit Buchstabe oder _, danach nur Buchstaben/Ziffern/_. "
              "snake_case = alles klein mit _.")

# ── Aufgabe 6 ────────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 6 – RSA (Exkurs)", r"""
    ## Verschlüsseln mit Modulo

    Diese Aufgabe ist ein Exkurs – etwas Verwirrung ist völlig in Ordnung.
    Bei Fragen zur Mathematik: Frag die Tutorinnen und Tutoren!

      • Zwei Primzahlen `p = 3` und `q = 11`. Ihr Produkt ist `n = p · q = 33`.
        Nach jeder Rechnung bringt man das Ergebnis mit Modulo in den
        Bereich 0 bis n - 1.
      • `N = (p - 1) · (q - 1) = 20`.
      • `e = 3`: zwischen 0 und N, größter gemeinsamer Teiler von e und N ist 1.
      • `d = 7`: zwischen 0 und N, und `e · d mod N = 1` (3 · 7 = 21, 21 mod 20 = 1).

    | Schritt | Formel | in Python |
    |---|---|---|
    | Verschlüsseln | c = mᵉ mod n | `c = m ** e % n` |
    | Entschlüsseln | m = cᵈ mod n | `m = c ** d % n` |

    Die Nachricht `m` muss eine Zahl mit 0 ≤ m < n sein.

    :::analogie 📮 Der Briefkasten
    `n` und `e` sind wie ein öffentlicher Briefkasten: Jede Person kann etwas
    einwerfen (verschlüsseln). Nur wer den Schlüssel `d` hat, kann den
    Kasten öffnen und die Nachricht lesen (entschlüsseln).
    :::

    :::code
    m = 4
    c = m ** 3 % 33
    print(c)
    print(c ** 7 % 33)
    :::
    """)

k.code(r"""
    ## Übung 1, Aufgabe 6 – Verschlüsseln und entschlüsseln

    Benutze die Werte vom Blatt: `n = 33`, `e = 3`, `d = 7`. Lies eine Nachricht
    `m` (ganze Zahl von 0 bis 32) ein, verschlüssele sie und entschlüssele das
    Ergebnis wieder:

        Eingabe:  4
        Ausgabe:  verschlüsselt: 31
                  entschlüsselt: 4
    """,
    [P(["4"], ["verschlüsselt: 31", "entschlüsselt: 4"]),
     P(["2"], ["verschlüsselt: 8", "entschlüsselt: 2"]),
     P(["5"], ["verschlüsselt: 26", "entschlüsselt: 5"]),
     P(["10"], ["verschlüsselt: 10", "entschlüsselt: 10"], beschreibung="10 bleibt 10"),
     P(["0"], ["verschlüsselt: 0", "entschlüsselt: 0"], beschreibung="Randfall 0"),
     P(["32"], ["verschlüsselt: 32", "entschlüsselt: 32"], beschreibung="Randfall n - 1")],
    """
    n = 33
    e = 3
    d = 7
    m = int(input("Nachricht (0 bis 32): "))
    c = m ** e % n
    print(f"verschlüsselt: {c}")
    print(f"entschlüsselt: {c ** d % n}")
    """,
    "** hat Vorrang vor %, also rechnet m ** e % n erst die Potenz und dann den Rest. "
    "Beim Entschlüsseln kommt wieder die ursprüngliche Nachricht heraus – das gilt "
    "für alle m von 0 bis 32.",
    tipps=["Lies m mit int(input()) ein und lege n, e und d als Variablen an.",
           "Verschlüsseln: c = m ** e % n",
           "Entschlüsseln: c ** d % n – beides mit einem f-String ausgeben."],
    vorlage="n = 33\ne = 3\nd = 7\nm = int(input(\"Nachricht (0 bis 32): \"))\n",
    streng=True)

k.zusammenfassung(r"""
    ## Das Wichtigste aus Übungsblatt 1

      • Aufgabe 1: Auf dem Pool heißt der Befehl `python3`; ein Texteditor genügt.
      • Aufgabe 2: `5 / 2` → 2.5 · `5y` ungültig · `"2" + 5` → TypeError ·
        `float(int(str(int("3"))))` → 3.0 · Tabs und Spaces nicht mischen.
      • Aufgabe 3: `true` → NameError. `//` mit Ganzzahlen bleibt int,
        `5.4 * 7.7` → 41.580000000000005.

    | Aufgabe 4.1 | Ergebnis |
    |---|---|
    | `int(3.17)` | `3` |
    | `int('a')` | ValueError – funktioniert nicht |
    | `float(5)` | `5.0` |
    | `int('5')` | `5` |
    | `str(3.1415)` | `'3.1415'` |
    | `bool(5)` / `bool('false')` | `True` / `True` |

    Aufgabe 4.2 – nur `"1"` und `0`: Zahlen durch Rechnen bauen
    (`int("1")`, `int("1" + str(0))`), Ziffern mit `str()` als Text
    aneinanderkleben, am Ende mit `int()` zur Ganzzahl machen.

    Aufgabe 5: `meinalter` ≠ `meinAlter` (NameError). snake_case = gültig und klein.

    !! Anführungszeichen selbst tippen – nie aus dem PDF kopieren.
    """)
