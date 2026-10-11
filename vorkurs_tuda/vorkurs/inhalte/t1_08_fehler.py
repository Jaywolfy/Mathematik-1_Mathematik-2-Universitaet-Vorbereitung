# -*- coding: utf-8 -*-
"""Kapitel: Kommentare, Fehlermeldungen & Fehlersuche (Vorlesung 1, Folien 44–48, Livecoding 1).

Nur Konzepte von Tag 1 (keine Listen, kein if). Die Aufgaben von Übung 2
(2.1, 2.2) stehen im Kapitel uebung2.
"""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="fehler",
    titel="Kommentare, Fehlermeldungen & Fehlersuche",
    beschreibung="# und \"\"\"-Kommentare, Fehlermeldungen lesen, Fehlerarten, Fehler finden und beheben",
    quelle="Vorlesung 1, Vorlesung 2, Livecoding 1",
    teil="tag1",
    icon="🐞")

k.lernziele([
    "Ich kann Kommentare mit # schreiben und weiß, wofür mehrzeilige Strings (\"\"\"…\"\"\") benutzt werden",
    "Ich kann gute von überflüssigen Kommentaren unterscheiden",
    "Ich kann eine Fehlermeldung lesen: Zeile, Markierung ^ und Fehlertyp",
    "Ich kann die häufigsten Fehlertypen von Tag 1 erkennen und beheben",
    "Ich kann ein fehlerhaftes Programm Schritt für Schritt reparieren",
])

# ── Erklärung 1: Kommentare ──────────────────────────────────────────────
k.erklaerung("Kommentare", r"""
    ## Kommentare – Notizzettel im Code

    Bei viel Code wird es schnell unübersichtlich. Mit **Kommentaren**
    schreibst du Erklärungen in den Code. Python IGNORIERT sie beim
    Ausführen komplett.

    Ein Kommentar beginnt mit `#` und geht bis zum Ende der Zeile:

    :::code
    # Begrüßung ausgeben
    print("Hallo")
    x = 5   # auch hinter Code möglich
    # print("Diese Zeile wird nicht ausgeführt")
    print(x)
    :::

    :::achtung // ist kein Kommentar
    In Java oder C beginnt ein Kommentar mit `//`. In Python ist `//` die
    Ganzzahl-Division! Kommentare beginnen in Python immer mit `#`.
    :::
    ---
    ## Mehrzeilige „Kommentare“

    Mehrzeilige Kommentare gibt es in Python genau genommen nicht. Häufig
    werden dafür mehrzeilige Strings mit drei Anführungszeichen (`'''` oder
    `<DQ3>`) „missbraucht“. Ohne Zuweisung erzeugt Python den String und wirft
    ihn sofort wieder weg:

        '''
        "Floor" in die
        Konsole ausgeben
        '''
        print('Floor')

    Steht so ein String ganz oben in einer Datei (oder später in einer
    Funktion), nennt man ihn **Docstring** – eine Beschreibung, die
    `help()` anzeigen kann:

        <DQ3>Rechnet Temperaturen von Celsius in Fahrenheit um.<DQ3>
    ---
    ## Gute und schlechte Kommentare

    :::analogie 🗒️ Post-its im Kochbuch
    Ein Post-it „Hier Eier aufschlagen“ neben „Eier aufschlagen“ bringt
    nichts. Hilfreich ist: „Unser Ofen heizt stärker – 10 Minuten kürzer
    backen!“ Das steht nicht im Rezept und erklärt das WARUM.
    :::

    :::vergleich ✘ Sagt nur das Offensichtliche | ✔ Hat einen Mehrwert
        # x um 1 erhöhen
        x = x + 1

        # "Floor" ausgeben
        print('Floor')
    |||
        # Schaltjahre lassen wir bewusst weg
        tage = jahre * 365

        # 1 Zoll = 2,54 cm
        zentimeter = zoll * 2.54
    :::

    !! Kommentiere Stellen, deren Bedeutung (vor allem für andere) nicht sofort klar ist.
    """.replace("<DQ3>", '"' * 3))

k.wf("Python führt Zeilen, die mit # beginnen, ganz normal aus.", False,
     "Mit # beginnt ein Kommentar – Python ignoriert alles dahinter in dieser Zeile.")

k.mc("Wie markiert man in Python einen (einzeiligen) Kommentar?",
     ["Mit # am Anfang", "Mit // am Anfang", "Mit <!-- -->", "Mit % am Anfang"],
     "# leitet in Python einen Kommentar ein. (// ist in Python die Ganzzahl-Division!)")

k.ausgabe('# print("A")\nprint("B")  # print("C")',
          "Zeile 1 ist komplett ein Kommentar. In Zeile 2 wird print(\"B\") ausgeführt, "
          "alles ab # ist Kommentar. Ausgabe: nur B.",
          tipp="Alles ab # bis zum Zeilenende wird ignoriert.")

k.mc("Was macht Python mit einem mehrzeiligen String in ''' ... ''', der keiner Variable "
     "zugewiesen wird?",
     ["Python erzeugt den String und verwirft ihn sofort wieder – er wirkt wie ein Kommentar",
      "Python gibt ihn automatisch aus",
      "Python meldet einen SyntaxError",
      "Python speichert ihn in einer Variable namens comment"],
     "Ein String ohne Zuweisung hat keine Wirkung. Deshalb wird ''' oder \"\"\" oft "
     "für mehrzeilige Erklärungen benutzt – echte mehrzeilige Kommentare gibt es "
     "in Python nicht.")

k.mc("Welcher Kommentar ist am sinnvollsten?",
     ["# Rabatt gilt nur für Studierende unter 30 (Vorgabe der Mensa)",
      "# x um 1 erhöhen",
      "# print aufrufen",
      "# Das ist eine Zeile Code"],
     "Gute Kommentare erklären Dinge, die man NICHT direkt im Code sieht – z.B. "
     "das Warum.")

# ── Erklärung 2: Fehlermeldungen lesen ───────────────────────────────────
k.erklaerung("Fehlermeldungen verstehen", r"""
    ## Keine Panik vor roten Fehlermeldungen!

    Fehler sind beim Programmieren völlig normal – auch für Profis. Python
    sagt dir fast immer, WO und WAS das Problem ist:

        x = 3 * 5)
          File "hallo.py", line 1
            x = 3 * 5)
                     ^
        SyntaxError: unmatched ')'

    :::analogie 🧭 Das Navi
    Eine Fehlermeldung ist wie ein Navi, das sagt: „Hier bist du falsch
    abgebogen.“ Die **Zeilennummer** ist die Straße, das **^** zeigt auf die
    Kreuzung, und die letzte Zeile nennt den **Fehlertyp** – also WAS schief
    ging. Lies die Meldung von unten nach oben: erst den Fehlertyp, dann die
    Stelle.
    :::

    :::visual ablauf
    {"schritte": [{"icon": "🔴", "text": "Letzte Zeile: Fehlertyp und Beschreibung lesen"},
                  {"icon": "📍", "text": "line …: die Zeile im Code finden"},
                  {"icon": "👉", "text": "^ zeigt die Stelle in der Zeile"},
                  {"icon": "🔧", "text": "Ursache beheben und neu ausführen"}]}
    :::

    :::achtung Der Fehler kann in der Zeile DAVOR liegen
    Fehlt in einer Zeile eine schließende Klammer, bemerkt Python das oft
    erst in der nächsten Zeile. Schau deshalb auch eine Zeile weiter oben.
    :::
    """)

k.mc("Was zeigt das Zeichen ^ in einer Python-Fehlermeldung an?",
     ["Die Stelle in der Zeile, an der Python den Fehler bemerkt hat",
      "Eine Potenz",
      "Dass der Fehler unwichtig ist",
      "Den Anfang des Programms"],
     "Python markiert mit ^ (und ~) die Stelle des Fehlers in der angezeigten Zeile.")

k.ausgabe("x = 3 * 5)",
          "Eine schließende Klammer ohne öffnende → SyntaxError: unmatched ')'.")

k.mc("Wo in einer Python-Fehlermeldung steht der Fehlertyp (z. B. NameError)?",
     ["In der letzten Zeile",
      "In der ersten Zeile",
      "Er steht gar nicht da",
      "Nur in der Python-Dokumentation"],
     "Die letzte Zeile nennt Fehlertyp und Beschreibung, z. B. "
     "\"NameError: name 'x' is not defined\". Darüber stehen Datei, Zeile und die Stelle.")

# ── Erklärung 3: Drei Fehlerarten ────────────────────────────────────────
k.erklaerung("Drei Arten von Fehlern", r"""
    ## Fehler – wie bei einer Sprache

    | Fehlerart | Was ist falsch? | Alltag | Beispiel in Python |
    |---|---|---|---|
    | lexikalisch | ein „Wort“ gibt es nicht | „Supermakrt“ | `prnt("Hallo")` → NameError |
    | syntaktisch | die „Grammatik“ | „Ich Supermarkt gehe den in.“ | `print("Hallo"` → SyntaxError |
    | semantisch | der Sinn / die Logik | „Ich trinke ein Brot.“ | `7 / 0` → ZeroDivisionError |

    Weitere Beispiele von Tag 1:
      • lexikalisch: `true` statt `True`, `eineZahl` vs. `einezahl` → NameError
      • syntaktisch: `3 + * 4`, `print("Hallo)` (Anführungszeichen fehlt) → SyntaxError
      • semantisch: `int("abc")` → ValueError, `"Punkte: " + 10` → TypeError
    ---
    ## Der gemeinste Fehler: falsches Ergebnis

    Auch ein FALSCHES ERGEBNIS ohne Absturz ist ein **semantischer Fehler**.
    Dann steht NICHTS in der Konsole – das Programm tut nur nicht, was es
    soll:

    :::code
    a = 2
    b = 4
    durchschnitt = a + b / 2
    print(durchschnitt)
    :::

    Erwartet war 3.0, heraus kommt 4.0. Grund: Punkt vor Strich, also
    `a + (b / 2)`. Richtig wäre `(a + b) / 2`.

    !! Gegen falsche Ergebnisse helfen print()-Ausgaben: „Wo stimmt der Wert noch?“
    """)

k.mc("Was passiert bei   Print(\"Hallo\")   (mit großem P) und welche Fehlerart ist das?",
     ["NameError – lexikalischer Fehler",
      "SyntaxError – syntaktischer Fehler",
      "TypeError – semantischer Fehler",
      "Kein Fehler, Python ignoriert Groß/klein"],
     "Python ist case-sensitive: Print gibt es nicht, nur print. Ein unbekanntes 'Wort' "
     "→ NameError, also ein lexikalischer Fehler (wie ein Tippfehler).")

k.mc("Was ist ein semantischer Fehler?",
     ["Ein Fehler in der Programmlogik (z.B. Teilen durch 0)",
      "Ein Tippfehler in einem Namen",
      "Eine fehlende Klammer",
      "Ein falsch eingerückter Block"],
     "Semantisch = die Bedeutung/Logik ist falsch, obwohl die Grammatik stimmt.")

k.ausgabe("eineZahl = 3\nprint(einezahl)",
          "einezahl ≠ eineZahl → NameError. Python schlägt sogar vor: "
          "Did you mean: 'eineZahl'?")

k.ausgabe('print("Hallo)',
          "Das schließende Anführungszeichen fehlt. Python findet das Ende des Strings "
          "nicht → SyntaxError (unterminated string literal).",
          tipp="Zähle die Anführungszeichen.")

k.ausgabe("a = 6\nb = 2\nprint(a + b / 2)",
          "Kein Absturz, aber vielleicht nicht das Gewünschte: b / 2 = 1.0 wird zuerst "
          "gerechnet, dann 6 + 1.0 = 7.0. Wer den Durchschnitt (4.0) wollte, braucht "
          "Klammern: (a + b) / 2.",
          tipp="Punkt vor Strich!")

k.mc("Dein Programm stürzt NICHT ab, liefert aber ein falsches Ergebnis. Was hilft am ehesten?",
     ["Werte an verschiedenen Stellen mit print() ausgeben und nachverfolgen",
      "Auf die Fehlermeldung warten",
      "Den Computer neu starten",
      "Alle Variablen umbenennen"],
     "Bei falschen Ergebnissen gibt es keine Fehlermeldung. Mit print() (und type()) "
     "findest du heraus, ab wo die Werte nicht mehr stimmen.")

# ── Erklärung 4: Einrückung, Tabs und Spaces ─────────────────────────────
k.erklaerung("Einrückung: Tabs und Leerzeichen", r"""
    ## Python achtet auf Einrückung

    Am Zeilenanfang stehende Leerzeichen (die **Einrückung**) haben in Python
    eine Bedeutung. An Tag 2 rückst du damit Blöcke ein (bei `if` und
    Schleifen). Bis dahin gilt: Jede Zeile beginnt ganz links.

        x = 5
          y = 3          ← unerwartet eingerückt!
        z = 2

    → **IndentationError: unexpected indent**

    Ein IndentationError ist ein **syntaktischer** Fehler: Die Form des
    Programms stimmt nicht, deshalb startet Python es gar nicht erst.
    ---
    ## Tabs oder Leerzeichen?

    Für Python sind ein **Tab** und **Leerzeichen** verschiedene Zeichen.

      • Nur Tabs ODER nur Leerzeichen: beides funktioniert.
      • Beides innerhalb eines Blocks **gemischt**: Python meldet
        **TabError: inconsistent use of tabs and spaces in indentation**
        (eine Unterart des IndentationError).
      • Konvention in Python: **4 Leerzeichen** pro Einrückungsebene.

    :::info Übung 1 fragt: „Macht es einen Unterschied?“
    Ja: Python unterscheidet die beiden Zeichen, und wer mischt, bekommt einen
    Fehler. Wer konsequent bei EINER Art bleibt (am besten 4 Leerzeichen), hat
    keine Probleme. Viele Editoren wandeln die Tab-Taste automatisch in 4
    Leerzeichen um.
    :::
    """)

k.ausgabe("x = 5\n  y = 3\nz = 2",
          "Zeile 2 ist ohne Grund eingerückt → IndentationError: unexpected indent.")

k.wf("In einer Python-Datei darf man Tabs und Leerzeichen zur Einrückung beliebig mischen.", False,
     "Nein. Für Python sind Tab und Leerzeichen verschiedene Zeichen. Wer innerhalb "
     "eines Blocks mischt, bekommt einen TabError (eine Art IndentationError). Nur Tabs "
     "oder nur Leerzeichen funktioniert – Konvention sind 4 Leerzeichen.")

k.mc("Welche Einrückung ist in Python üblich?",
     ["4 Leerzeichen pro Ebene",
      "1 Leerzeichen pro Ebene",
      "Abwechselnd Tab und Leerzeichen",
      "Gar keine – Einrückung ist in Python egal"],
     "Die Konvention sind 4 Leerzeichen. Wichtig ist vor allem: nicht mischen.")

k.mc("Zu welcher Fehlerart gehört ein IndentationError (falsche Einrückung)?",
     ["Syntaktischer Fehler – die „Grammatik“ (Form) des Codes stimmt nicht",
      "Lexikalischer Fehler – ein Wort ist Python unbekannt",
      "Semantischer Fehler – die Logik ist falsch, die Form stimmt",
      "Gar kein Fehler, nur eine Warnung"],
     "Die Einrückung gehört in Python zur Syntax. Stimmt sie nicht, ist die Form des "
     "Programms falsch, so wie ein Satz mit falscher Grammatik. Python startet das "
     "Programm dann gar nicht erst.")

# ── Erklärung 5: Fehlertypen und Vorgehen ────────────────────────────────
k.erklaerung("Fehlertypen auf einen Blick – und das Vorgehen", r"""
    ## Die häufigsten Fehlertypen von Tag 1

    | Fehlertyp | Bedeutung | Beispiel |
    |---|---|---|
    | `NameError` | Name unbekannt | `prnt(1)`, `true` |
    | `SyntaxError` | Grammatik falsch | `print("x)`, `3 + * 4` |
    | `IndentationError` | Einrückung falsch | Zeile grundlos eingerückt |
    | `TypeError` | Typen passen nicht | `"Punkte: " + 10` |
    | `ValueError` | Typ ok, Wert unmöglich | `int("abc")` |
    | `ZeroDivisionError` | Teilen durch 0 | `7 / 0`, `7 % 0` |

    Später kommen noch `IndexError`, `KeyError` und `RecursionError` dazu.
    ---
    ## So gehst du bei der Fehlersuche vor

      1. Konsolenausgabe lesen.
      2. Fehlertyp bestimmen (letzte Zeile).
      3. Stelle im Code finden (Zeilennummer, ^).
      4. Bei Bedarf Werte mit `print()` und `type()` ausgeben.
      5. Fehler beheben und neu ausführen.

    Probier es: Diese Zeilen haben einen Fehler. Führe sie aus, lies die
    Meldung und überlege, wie die Reparatur aussieht.

    :::code
    anzahl = "3"
    preis = 2.5
    print(anzahl * preis)
    :::
    """)

k.ausgabe('punkte = 10\nprint("Punkte: " + punkte)',
          "String + Zahl → TypeError. Richtig: print('Punkte: ' + str(punkte)) oder "
          "print(f'Punkte: {punkte}')")

k.ausgabe('print(int("abc"))',
          "'abc' ist kein Zahltext. Der Typ (str) passt zu int(), aber der Wert nicht "
          "→ ValueError.")

k.mc("Welcher Fehlertyp entsteht bei   int(\"12a\")  ?",
     ["ValueError", "TypeError", "NameError", "SyntaxError"],
     "int() akzeptiert Text, aber nur Text, der eine Ganzzahl darstellt. '12a' ist "
     "keiner → ValueError.")

k.mc("Welcher Fehlertyp entsteht bei   7 % 0  ?",
     ["ZeroDivisionError", "ValueError", "SyntaxError", "Kein Fehler, das Ergebnis ist 0"],
     "Modulo braucht eine Division, und durch 0 darf man nicht teilen → ZeroDivisionError.")

# ── Praxisteil ───────────────────────────────────────────────────────────
k.luecke("Repariere den Code durch Ausfüllen der Lücken: Er soll eine ganze Zahl einlesen "
         "und ihr Doppeltes ausgeben, z. B. „Das Doppelte ist 14“.",
         """
         zahl = ___(input("Zahl: "))
         print("Das Doppelte ist " + ___(zahl * 2))
         """,
         [["int"], ["str"]],
         "Ohne int() wäre zahl ein Text, und zahl * 2 würde den Text nur verdoppeln "
         "('77'). Ohne str() gäbe es beim Verketten einen TypeError.",
         tipp="Erst Text → Zahl, dann Zahl → Text.")

k.code(r"""
    ## Fehler finden: Tage-Rechner

    Das Programm in der Vorlage soll ausrechnen, wie viele Tage man ungefähr
    alt ist (Alter mal 365). Führe es aus: Es stürzt nicht ab, gibt aber
    statt einer Zahl einen riesigen Zahlensalat aus. Repariere es. Achtung:
    Nach der ersten Reparatur meldet Python einen neuen Fehler – lies ihn
    genau.

        Eingabe:  20
        Ausgabe:  Du bist ungefähr 7300 Tage alt.

    Tipp: Schreib dir einen Kommentar mit `#` dazu, was du geändert hast.
    """,
    [P(["20"], ["Du bist ungefähr 7300 Tage alt."]),
     P(["1"], ["Du bist ungefähr 365 Tage alt."]),
     P(["0"], ["Du bist ungefähr 0 Tage alt."], beschreibung="Alter 0"),
     P(["100"], ["Du bist ungefähr 36500 Tage alt."])],
    """
    alter = int(input("Wie alt bist du? "))   # input() liefert Text → umwandeln
    tage = alter * 365
    print("Du bist ungefähr " + str(tage) + " Tage alt.")   # Zahl → Text zum Verketten
    """,
    "Fehler 1 (semantisch, ohne Absturz): input() liefert einen String. \"20\" * 365 "
    "rechnet nicht, sondern wiederholt den Text 365-mal – also int() drumherum. "
    "Fehler 2: Jetzt ist tage eine Zahl, und beim Verketten mit + gibt es einen "
    "TypeError – tage muss mit str() zu Text werden. Alternative für die Ausgabe: "
    "ein f-String.",
    tipps=["Schau dir die Ausgabe an: Welcher Typ hat alter eigentlich?",
           "input() liefert Text. Zum Rechnen brauchst du int(), zum Verketten str().",
           "alter = int(input(...)) und print(\"Du bist ungefähr \" + str(tage) + \" Tage alt.\")"],
    vorlage='alter = input("Wie alt bist du? ")\n'
            'tage = alter * 365\n'
            'print("Du bist ungefähr " + tage + " Tage alt.")\n',
    streng=True)

k.code(r"""
    ## Fehler-Kette: Zimmerfläche

    Das Programm in der Vorlage soll die Fläche eines Zimmers berechnen. Es
    enthält aber mehrere Fehler: Python wird nacheinander einen SyntaxError,
    einen NameError und TypeErrors melden. Repariere sie der Reihe nach – nach
    jeder Reparatur neu ausführen!

        Eingaben:  3, 4
        Ausgabe:   Fläche: 12.0 m²

    Breite und Höhe können Kommazahlen sein.
    """,
    [P(["3", "4"], ["Fläche: 12.0 m²"]),
     P(["2.5", "2"], ["Fläche: 5.0 m²"], beschreibung="Kommazahl"),
     P(["1.5", "1.5"], ["Fläche: 2.25 m²"]),
     P(["0", "7"], ["Fläche: 0.0 m²"], beschreibung="Breite 0")],
    """
    breite = float(input("Breite in m: "))
    hoehe = float(input("Höhe in m: "))
    flaeche = breite * hoehe
    print("Fläche: " + str(flaeche) + " m²")
    """,
    "1. In der letzten Zeile fehlt die schließende Klammer (SyntaxError). "
    "2. Breite ≠ breite: Groß/klein zählt (NameError). "
    "3. Die Eingaben sind Text, und Text mal Text geht nicht (TypeError) – mit "
    "float() werden sie zu Zahlen. 4. Für das Verketten braucht flaeche ein str() "
    "(sonst wieder TypeError).",
    tipps=["Python zeigt immer nur den ersten Fehler. Repariere ihn und führe den Code erneut aus.",
           "Achte auf Klammern, Groß-/Kleinschreibung und die Typen der Eingaben.",
           "breite = float(input(...)), flaeche = breite * hoehe, "
           "print(\"Fläche: \" + str(flaeche) + \" m²\")"],
    vorlage='breite = input("Breite in m: ")\n'
            'hoehe = input("Höhe in m: ")\n'
            'flaeche = Breite * hoehe\n'
            'print("Fläche: " + flaeche + " m²"\n',
    streng=True)

k.code(r"""
    ## Der stille Fehler: Durchschnitt

    Dieses Programm stürzt nicht ab – es rechnet nur falsch. Es soll den
    Durchschnitt zweier Zahlen ausgeben:

        Eingaben:  2, 4
        Ausgabe:   Durchschnitt: 3.0

    Finde und behebe den semantischen Fehler.
    """,
    [P(["2", "4"], ["Durchschnitt: 3.0"]),
     P(["1", "2"], ["Durchschnitt: 1.5"]),
     P(["10", "10"], ["Durchschnitt: 10.0"]),
     P(["-4", "4"], ["Durchschnitt: 0.0"], beschreibung="negative Zahl"),
     P(["0", "0"], ["Durchschnitt: 0.0"])],
    """
    a = float(input())
    b = float(input())
    durchschnitt = (a + b) / 2
    print("Durchschnitt:", durchschnitt)
    """,
    "Ohne Klammern rechnet Python a + (b / 2), weil / Vorrang vor + hat. Mit "
    "(a + b) / 2 wird erst addiert und dann halbiert.",
    tipps=["Rechne das Beispiel 2 und 4 von Hand nach, so wie Python es tut.",
           "Punkt vor Strich: Was wird in a + b / 2 zuerst gerechnet?",
           "durchschnitt = (a + b) / 2"],
    vorlage='a = float(input())\n'
            'b = float(input())\n'
            'durchschnitt = a + b / 2\n'
            'print("Durchschnitt:", durchschnitt)\n',
    streng=True)

k.zusammenfassung(r"""
    ## Das Wichtigste aus Kapitel 8

        # Kommentar bis zum Zeilenende
        x = 5   # auch hinter Code
        '''
        mehrzeiliger String ohne Zuweisung –
        wird oft als Kommentar benutzt (Docstring ganz oben)
        '''

      • Gute Kommentare erklären das WARUM, nicht das Offensichtliche.
      • Fehlermeldung von unten lesen: Fehlertyp → Zeile → ^.
      • Fehlerarten: lexikalisch (NameError), syntaktisch (SyntaxError),
        semantisch (z. B. ZeroDivisionError oder ein falsches Ergebnis).

    | Fehlertyp | typische Ursache |
    |---|---|
    | NameError | Tippfehler, Groß/klein, `true` |
    | SyntaxError | Klammer oder Anführungszeichen fehlt |
    | IndentationError / TabError | grundlos eingerückt, Tabs und Leerzeichen gemischt |
    | TypeError | `"Text" + 5` |
    | ValueError | `int("abc")`, `int("4.5")` |
    | ZeroDivisionError | `/ 0`, `// 0`, `% 0` |

    !! Einrückung: konsequent 4 Leerzeichen, nie mit Tabs mischen.
    """)
