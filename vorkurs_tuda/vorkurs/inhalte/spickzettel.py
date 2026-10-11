# -*- coding: utf-8 -*-
"""Spickzettel: alles Wichtige auf einen Blick (Markup, eine Seite pro Tag + Challenge)."""

SPICKZETTEL = r"""
## Tag 1 – Python starten, Datentypen, Rechnen

| Was | Wie |
|---|---|
| Programm ausführen | `python datei.py` (Poolrechner: `python3 datei.py`) |
| Interaktiver Modus | `python` starten, Eingabe nach `>>>` |
| Interaktiv beenden | `exit()` oder Strg+D (Windows: Strg+Z, dann Enter) |
| Programm abbrechen | Strg+C (z. B. bei einer Endlosschleife) |
| Hilfe | `help(print)` – oder `help()`: Seiten mit `q` verlassen, `quit` beendet |

Kommentare werden von Python ignoriert:

    # Kommentar bis zum Zeilenende
    '''Mehrzeiliger Text (auch mit drei "),
    wird oft als mehrzeiliger Kommentar benutzt.'''

| Typ | Beispiele | Hinweis |
|---|---|---|
| `int` | `42`, `-2` | beliebig groß |
| `float` | `2.5`, `1.6e6` | begrenzt und ungenau: `0.1 + 0.2 == 0.3` ist False |
| `str` | `"Text"`, `'Text'` | unveränderlich |
| `bool` | `True`, `False` | |
| `NoneType` | `None` | "kein Wert" |

`type(x)` zeigt den Typ. `int` mit `float` gemischt ergibt `float`.

| Operator | Bedeutung | Beispiel |
|---|---|---|
| `/` | Division, immer float | `7 / 2` → `3.5` |
| `//` | ganzzahlig, rundet AB | `7 // 2` → `3`, `-7 // 2` → `-4` |
| `%` | Rest | `7 % 2` → `1`; teilbar: `a % b == 0` |
| `**` | Potenz | `2 ** 10` → `1024` |
| `== != < > <= >=` | Vergleich | Ergebnis True/False |

Division durch 0 (`/`, `//`, `%`) → `ZeroDivisionError`.

!! Rangfolge: Klammern → ** → * / // % → + - → Vergleiche → not → and → or

## Variablen und Typumwandlung

    alter = 18          # rechte Seite zuerst, dann speichern
    alter += 1          # wie alter = alter + 1  (auch -=, *=)
    ist_gross = alter >= 18   # Vergleichsergebnis speichern

Namen: Buchstaben, Ziffern, `_`; nicht mit Ziffer beginnen; snake_case; Groß/klein zählt.

| Aufruf | Ergebnis |
|---|---|
| `int('5')` / `int('a')` | `5` / `ValueError` |
| `int(3.9)`, `int(-3.9)` | `3`, `-3` (schneidet ab, rundet nicht) |
| `int(float('4.5'))` | `4` (zweistufig umwandeln) |
| `float(5)`, `str(3)` | `5.0`, `'3'` |
| `bool(0)`, `bool('')` | `False` |
| `bool('False')` | `True` (nicht leer!) |

## Ein- und Ausgabe, Strings

    name = input('Name: ')            # input liefert IMMER str
    zahl = int(input('Zahl: '))
    print(name, zahl)                 # Leerzeichen dazwischen
    print('a', end='')                # kein Zeilenumbruch am Ende
    print(f'Hallo {name}, {zahl + 1}')

| String-Werkzeug | Wirkung |
|---|---|
| `'a' + 'b'` | `'ab'` – nur str + str (`'Alter: ' + str(18)`) |
| `'ab' * 3` | `'ababab'` |
| `len(s)`, `s[0]`, `s[-1]` | Länge, erstes, letztes Zeichen |
| `s.lower()`, `s.upper()`, `s.strip()` | klein, groß, Leerraum außen weg |
| `s.split(',')`, `s.replace('a', 'b')` | Liste der Teile, ersetzen |
| `\n`, `\t`, `\"`, `\'`, `\\` | Zeilenumbruch, Tab, Anführungszeichen, Backslash |

| Fehler | Typisches Beispiel |
|---|---|
| `SyntaxError` | Klammer oder Anführungszeichen fehlt |
| `IndentationError` | falsche Einrückung |
| `NameError` | `print(Alter)` – Name unbekannt (Groß/klein!) |
| `TypeError` | `'a' + 1` |
| `ValueError` | `int('abc')` |
---
## Tag 2 – Logik und Verzweigungen

| a | b | `a and b` | `a or b` | `not a` |
|---|---|---|---|---|
| True | True | True | True | False |
| True | False | False | True | False |
| False | True | False | True | True |
| False | False | False | False | True |

`and` und `or` werten von links aus und hören auf, sobald das Ergebnis feststeht.

    if alter >= 18:                  match tag:
        print('Eintritt')                case 'Sa' | 'So':
    elif alter >= 16:                        print('Wochenende')
        print('Mit Begleitung')          case _:          # Standardfall
    else:                                    print('Werktag')
        print('Kein Eintritt')

  • `if gefunden:` statt `if gefunden == True:`
  • Der Standardfall bei match heißt `case _:` (ein `default` gibt es in Python nicht).
  • `=` speichert, `==` vergleicht.

## while-Schleifen

    i = 0                            while True:
    while i < 5:                         eingabe = input('Zahl: ')
        print(i)                         if eingabe.isnumeric():
        i += 1   # sonst endlos!             break

  • Im Schleifenkörper muss sich etwas ändern, sonst Endlosschleife.
  • `break` beendet die Schleife, `continue` springt zur nächsten Runde –
    beide nur für die innerste Schleife. Vor `continue` das Hochzählen nicht vergessen!

## Listen

    lst = [3, 4, 1, 2]
    lst[0]        # 3          lst[-1]      # 2 (= lst[len(lst) - 1])
    len(lst)      # 4          4 in lst     # True
    lst[len(lst)] # IndexError lst.index(9) # ValueError

| Methode | Wirkung (verändert die Liste) |
|---|---|
| `lst.append(x)` / `lst.insert(0, x)` | hinten / vorne einfügen |
| `lst.pop()` / `del lst[i]` | letztes entfernen (und zurückgeben) / Index i löschen |
| `lst.sort()`, `lst.reverse()`, `lst.clear()` | sortieren, umdrehen, leeren |
| `lst2 = lst.copy()` | echte Kopie – `lst2 = lst` ist KEINE Kopie (Aliasing)! |

## Slicing `lst[start:end:step]`

| Teil | Standardwert (step positiv) | Standardwert (step negativ) |
|---|---|---|
| `start` | 0 (Anfang) | letztes Element |
| `end` | bis zum Ende (exklusiv!) | bis vor den Anfang |
| `step` | 1 | – |

| Ausdruck (`s = 'Python'`) | Ergebnis |
|---|---|
| `s[1:4]` | `'yth'` (Index 4 nicht mehr dabei) |
| `s[:2]`, `s[2:]` | `'Py'`, `'thon'` |
| `s[-3:]` | `'hon'` (die letzten drei) |
| `s[::2]` | `'Pto'` (jedes zweite) |
| `s[::-1]` | `'nohtyP'` (rückwärts) |
| `s[4:1:-1]` | `'oht'` |

Strings sind unveränderlich: `s[0] = 'X'` → `TypeError`.

| Fehlerart | Bedeutung | Beispiel |
|---|---|---|
| lexikalisch | falsches "Wort" | `Print(1)`, `einezahl` statt `eineZahl` |
| syntaktisch | falsche Grammatik | `if x > 3 print(x)` (Doppelpunkt fehlt) |
| semantisch | läuft, rechnet aber Falsches | `durchschnitt = a + b / 2` |
---
## Tag 3 – Tupel und Dictionaries

    t = (1, 2, 3)        # unveränderlich
    einzeln = (5,)       # Tupel mit einem Element: Komma! (5) ist nur 5
    a, b = b, a          # Werte tauschen (Tupel entpacken)

    d = {'Anna': 17, 'Ben': 19}
    d['Kim'] = 18                    # neu oder überschreiben
    d['Max']                         # KeyError
    d.get('Max', 0)                  # 0 statt Fehler
    'Anna' in d                      # True (prüft Schlüssel)
    del d['Ben']
    for name, alter in d.items():    # Schlüssel UND Wert
        print(name, alter)
    zaehler[w] = zaehler.get(w, 0) + 1   # Zählen-Muster

`d.keys()` und `d.values()` liefern nur Schlüssel bzw. Werte. Schlüssel müssen
unveränderlich sein: Tupel ja, Listen nein.

## for-Schleifen

| Aufruf | Zahlen |
|---|---|
| `range(5)` | 0 1 2 3 4 (Ende exklusiv) |
| `range(2, 10, 3)` | 2 5 8 |
| `range(10, 0, -3)` | 10 7 4 1 |

    for x in liste:                       for i, x in enumerate(liste):
        print(x)                              print(i, x)      # Index + Wert

    for a, b in zip([1, 2, 3], ['x', 'y']):    # (1, 'x'), (2, 'y')
        print(a, b)                            # zip hört bei der kürzeren Liste auf

    for i in range(len(liste)):           for key in d:            # Schlüssel
        print(i, liste[i])                    print(key, d[key])

Akkumulator: Startwert VOR der Schleife (Summe `0`, Produkt `1`, Liste `[]`, Zählen `{}`),
in der Schleife verändern, Ergebnis NACH der Schleife ausgeben.

## import

    import math                 # dann: math.sqrt(16), math.pi, math.floor(3.7)
    math.sin(90 * math.pi / 180)   # Winkel im Bogenmaß!  math.floor(-3.5) → -4
    from math import sqrt       # Zusatz (nicht in der VL): dann direkt sqrt(16)

## Dateien

    with open('daten.txt', 'r') as f:     # wird am Ende automatisch geschlossen
        inhalt = f.read()                 # alles als ein String
        # oder: f.readline() / f.readlines() – jede Zeile behält ihr '\n'!
    with open('daten.txt', 'w') as f:
        f.write('Text\n')                 # kein automatischer Zeilenumbruch

| Modus | Wirkung |
|---|---|
| `'r'` | lesen; Datei fehlt → `FileNotFoundError` |
| `'w'` | schreiben; vorhandene Datei wird geleert |
| `'a'` | anhängen ans Ende |
| `'x'` | neu anlegen; Datei existiert schon → Fehler |
| Zusatz `t` / `b` / `+` | Text (Standard) / Binär / Lesen+Schreiben, z. B. `'rb'`, `'r+'` |

!! Genau EIN Grundmodus (r, w, a oder x), optional mit Zusatz. `'+'` allein ist ungültig.

## Funktionen

    def flaeche(breite, hoehe):      # Parameter
        ergebnis = breite * hoehe    # lokale Variable – außen unsichtbar
        return ergebnis              # ohne return → None

    print(flaeche(3, 4))             # Argumente 3 und 4 → 12

  • `print` zeigt nur an, `return` gibt einen Wert zurück (und beendet die Funktion).
  • Die Definition allein tut nichts – erst der Aufruf `flaeche(3, 4)` führt sie aus.
  • `global x` in der Funktion, um eine globale Variable zu ändern.
  • Globale Variable lesen UND in der Funktion zuweisen (ohne `global`) → `UnboundLocalError`.
  • Funktionen dürfen andere Funktionen aufrufen.
---
## Tag 4 – Rekursion

Eine Funktion, die sich selbst aufruft. Sie braucht immer:
  1. einen **Rekursionsanker** (einfachster Fall, Antwort ohne Selbstaufruf),
  2. einen **Rekursionsschritt**, der das Problem **kleiner** macht.

    def fakultaet(n):
        if n == 0:                      # Rekursionsanker
            return 1
        return n * fakultaet(n - 1)     # Rekursionsschritt

    def fib(n):                         # mehrfache Rekursion: fib(0)=0, fib(1)=1
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)

    def summe(lst):                     # Rekursion über eine Liste
        if lst == []:
            return 0
        return lst[0] + summe(lst[1:])

  • Wechselseitige Rekursion: `is_even(n)` ruft `is_odd(n - 1)` auf und umgekehrt.
  • Aufrufstapel: Jeder Aufruf ist ein Teller mit eigenen Variablen. Erst bis zum Anker
    aufbauen, dann beim Zurückkehren rechnen.
  • Anker vergessen oder Problem wird nicht kleiner → `RecursionError` (maximale Tiefe ca. 1000).
  • Jede Schleife lässt sich auch rekursiv schreiben – was besser ist, hängt vom Problem ab.
  • Übung 4, 2.5: Auch `lst[1:]` ist ein Slice (verboten) → Kopie mit `list(lst)` und `pop(0)`.

    def ggT(a, b):                      # Übung 4, 3.1 (euklidischer Algorithmus)
        if a == 0:
            return b
        if b == 0:
            return a
        return ggT(b, a % b)

RSA: n = p · q, N = φ(n) = (p − 1)(q − 1); e mit ggT(e, N) = 1, d mit e · d % N == 1;
öffentlich (e, n), privat (d, n); `c = pow(m, e, n)`, `m = pow(c, d, n)`.

## Ausblick Java

| Python | Java |
|---|---|
| `x = 5` | `int x = 5;` – Typ angeben, Semikolon |
| `'Text'` oder `"Text"` | nur `"Text"` (`'a'` ist ein einzelnes Zeichen) |
| Einrückung bildet Blöcke | geschweifte Klammern, Einrückung egal |
| `elif` | `else if` |
| `for i in range(1, 11):` | `for (int i = 1; i < 11; ++i) { ... }` |
| `for f in fruits:` | `for (String f : fruits) { ... }` |
| `print(...)` | `System.out.println(...);` |
| `def say_hello(name):` | `void sayHello(String name) { ... }` |
| `str(i) + ' squared'` | `i + " squared"` (wandelt automatisch um) |
| `-7 // 2` → `-4` (rundet ab) | `-7 / 2` → `-3` (schneidet bei int ab) |
| direkt ausführen | erst kompilieren: `javac`, dann Bytecode ausführen |
| keine do-while-Schleife | zusätzlich `do { … } while (…);` |

## Guter Code

  • Allgemein statt Sonderfälle: eine Funktion mit Richtung als Parameter
    (`vier_in_folge(x, y, xo, yo)`) statt vieler fast gleicher Kopien.
  • Beim Laufen über ein Gitter immer zuerst den Rand prüfen
    (`0 <= x < breite`) – sonst `IndexError` oder heimliche Treffer über negative Indizes.
  • Was sich in einer Schleife nicht ändert, vor die Schleife ziehen;
    eine Datei einmal öffnen, nicht für jede Zeile neu.
  • Sprachensalat: funktional (Haskell), stack-basiert (Forth), Arrays (APL), 2D (AsciiDots),
    Bilder (Piet) – Paradigmen schließen sich nicht aus.
---
## Challenge – Othello

| Baustein | Code |
|---|---|
| Spielfeld | Liste von Listen, Zugriff `brett[y][x]` (erst Zeile, dann Spalte) |
| Brett bauen | `for y in range(8): brett.append([LEER] * 8)` |
| NICHT so | `[[LEER] * 8] * 8` – 8 Verweise auf dieselbe Zeile |
| Auf dem Brett? | `0 <= x < 8 and 0 <= y < 8` |
| 8 Richtungen | `for dx, dy in RICHTUNGEN:` mit Tupeln wie `(1, 0)`, `(1, -1)` |
| Ausgabe | `print(y + 1, ' '.join(brett[y]))` |
| Steine zählen | `zeile.count('S')` für jede Zeile addieren |

    def zahl_einlesen(text):              # sichere Eingabe 1–8
        while True:
            eingabe = input(text)
            if eingabe.isnumeric() and 1 <= int(eingabe) <= 8:
                return int(eingabe) - 1   # Spieler zählen ab 1, Listen ab 0
            print('Bitte eine Zahl von 1 bis 8 eingeben.')

  • Gültiger Zug: in mindestens einer Richtung gegnerische Steine zwischen
    neuem und eigenem Stein ("Sandwich") – diese werden umgedreht.
  • Kein gültiger Zug → passen. Keiner kann ziehen → Spielende.
  • Spielschleife: `while hat_zug(brett, SCHWARZ) or hat_zug(brett, WEISS):` – passen =
    Farbe wechseln + `continue`; ungültiger Zug = `continue` OHNE Wechsel.
  • Mehr Steine gewinnt, Gleichstand → unentschieden ausgeben.
  • Abgabe über Moodle, Abschnitt "Programmierchallenge".
"""
