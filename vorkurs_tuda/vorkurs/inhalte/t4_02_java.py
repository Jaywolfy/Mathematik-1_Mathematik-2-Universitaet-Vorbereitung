# -*- coding: utf-8 -*-
"""Kapitel: Ausblick: Java – die nächste Sprache (Vorlesung 4, Folien 24–32)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="java",
    titel="Ausblick: Java – die nächste Sprache",
    beschreibung="Statische Typen, geschweifte Klammern, Compiler – Python vs. Java",
    quelle="Vorlesung 4",
    teil="tag4",
    icon="☕")

k.lernziele([
    "Ich kann die vier großen Unterschiede zwischen Python und Java nennen",
    "Ich kann einfache Java-Schnipsel (Variablen, if, Schleifen, Funktionen) lesen und in Python übersetzen",
    "Ich finde typische Java-Fehler wie ein fehlendes Semikolon oder 'Text' statt \"Text\"",
    "Ich weiß, dass Java-/ und Python-// bei negativen Zahlen verschieden rechnen",
])

k.erklaerung("Java im Vergleich zu Python", r"""
    ## Java – die nächste Sprache im Studium

    Java ist die nächste Programmiersprache, die du im Studium lernst. Wie
    unterscheidet sie sich von Python? Vier große Punkte (Folien 25 und 26):

    1. **Statische Typisierung**: Die Typen von Variablen, Rückgabewerten
       und Funktionsparametern müssen im Quelltext stehen. Dadurch kann zur
       Laufzeit weniger schiefgehen, die Programme sind robuster.
    2. **Objektorientierung**: Funktionen auf Objekten heißen **Methoden**.
       Die kennst du schon, z. B. `"Hallo".upper()`.
    3. **Einrückung ist egal**: Stattdessen trennen geschweifte Klammern
       `{ }` die Blöcke und Semikola `;` die Anweisungen.
    4. **Java wird kompiliert**: Man führt nicht direkt den Quelltext aus,
       sondern **Bytecode**. Vorher muss der **Compiler** `javac` laufen.

    :::analogie 📋 Formular statt Notizzettel
    Python ist wie ein Notizzettel: Du schreibst einfach `alter = 19` hin,
    und Python merkt sich selbst, dass das eine Zahl ist. Java ist wie ein
    Amtsformular mit festen Feldern: Im Feld „Alter (ganze Zahl)“ steht
    schon vorher, was hinein darf. Schreibt Ben dort „neunzehn“ hinein,
    lehnt das Amt (der Compiler) das Formular ab, **bevor** es bearbeitet
    wird. Das ist mehr Schreibarbeit, aber Fehler fallen früher auf.
    :::
    ---
    ## Vom Quelltext zum laufenden Programm

    :::visual ablauf
    {"schritte": [{"icon": "👩‍💻", "text": "Du schreibst Hallo.java"},
                  {"icon": "⚙️", "text": "javac übersetzt in Bytecode (Hallo.class)"},
                  {"icon": "☕", "text": "Java führt den Bytecode aus"}]}
    :::

    Findet `javac` einen Fehler (z. B. ein fehlendes Semikolon oder einen
    falschen Typ), entsteht gar kein Bytecode. Das Programm startet dann
    überhaupt nicht. In Python fällt so ein Fehler oft erst auf, wenn die
    Zeile ausgeführt wird.

    :::info Hintergrund (Zusatz, nicht auf der Folie)
    Den Bytecode führt die **Java Virtual Machine** (JVM) aus. Weil es die
    JVM für Windows, macOS und Linux gibt, läuft derselbe Bytecode überall.
    :::
    """)

k.mc("Was bedeutet statische Typisierung?",
     ["Typen von Variablen, Parametern und Rückgabewerten stehen im Quelltext",
      "Variablen dürfen sich nie ändern",
      "Das Programm läuft ohne Typen",
      "Typen werden erst beim Ausführen geraten"],
     "In Java steht z. B. `int x = 5;`. Der Wert von x darf sich ändern, nur der Typ steht "
     "fest. Dadurch kann zur Laufzeit weniger schiefgehen.")

k.mc("Wie heißt der Java-Compiler?",
     ["javac", "python3", "jvm-run", "gcc"],
     "javac übersetzt den Quelltext in Bytecode, der dann ausgeführt wird.")

k.mc("Was ersetzt in Java die Einrückung als Kennzeichen für Blöcke?",
     ["Geschweifte Klammern { } (und Semikola ; zum Trennen von Anweisungen)",
      "Doppelpunkte",
      "Eckige Klammern",
      "Nichts, Java hat keine Blöcke"],
     "Einrückung ist in Java irrelevant – Blöcke stehen in { }.")

k.wf("In Java ist die Einrückung genauso Pflicht wie in Python.", False,
     "In Java ist Einrückung für den Compiler egal (aber für Menschen trotzdem wichtig!).")

k.wf("Wer in Java ein Semikolon vergisst, merkt das erst, wenn das Programm an dieser Stelle läuft.",
     False,
     "Java wird vor dem Start kompiliert. javac findet den Fehler sofort, und es entsteht gar "
     "kein Bytecode. Das Programm startet also überhaupt nicht.")

k.erklaerung("Variablen, Verzweigungen und Funktionen", r"""
    ## Variablen

    :::vergleich 🐍 Python | ☕ Java
    Kein Typ, kein Semikolon:
        x = 5
        s = 'Lorem'
    |||
    Typ vorne, Semikolon hinten:
        int x = 5;
        String s = "Lorem";
    :::

    !! In Java werden Strings NUR mit "..." geschrieben, nicht mit '...'.

    :::achtung Typischer Fehler: einfache Anführungszeichen
    `String s = 'Lorem';` kompiliert nicht. In Java bedeutet `'L'` ein
    **einzelnes Zeichen** (Typ `char`), keinen String. Mehrere Zeichen
    zwischen `'...'` sind ein Fehler.
    :::
    ---
    ## Verzweigungen (Folie 28)

    :::vergleich 🐍 Python | ☕ Java
    Doppelpunkt und Einrückung:
        if x < 0:
            print("Negativ")
        elif x > 0:
            print("Positiv")
        else:
            print("Null")
    |||
    Klammern um die Bedingung, Blöcke in { }:
        if (x < 0) {
            System.out.println("Negativ");
        } else if (x > 0) {
            System.out.println("Positiv");
        } else {
            System.out.println("Null");
        }
    :::

    Aus `elif` wird `else if`. Aus `print` wird `System.out.println`.
    ---
    ## Funktionen (Folie 32)

    :::vergleich 🐍 Python | ☕ Java
    def, Doppelpunkt:
        def say_hello(name):
            print("Hello " + name + "!")
            print("How are you?")
    |||
    Rückgabetyp und Parametertyp:
        void sayHello(String name) {
            System.out.println("Hello " + name + "!");
            System.out.println("How are you?");
        }
    :::

      • `void` bedeutet: Diese Funktion gibt NICHTS zurück. Eine Funktion,
        die eine ganze Zahl liefert, beginnt mit `int`.
      • Der Parameter hat einen Typ: `String name`.
      • Zusatz (nicht auf der Folie): In Java schreibt man Namen in
        camelCase (`sayHello`), in Python in snake_case (`say_hello`).
    """)

k.mc("Wie schreibt man   x = 5   in Java?",
     ["int x = 5;", "x = 5", "var x := 5", "int x = 5"],
     "Typ angeben (statische Typisierung) und Semikolon am Ende. `int x = 5` ohne Semikolon "
     "kompiliert nicht.")

k.mc("Welcher String ist in Java gültig?",
     ['"Lorem"', "'Lorem'", "Beide", "Keiner"],
     "In Java können Strings nur mit doppelten Anführungszeichen definiert werden. "
     "`'L'` wäre ein einzelnes Zeichen (char), `'Lorem'` ist ein Fehler.")

k.mc("Wie schreibt man Pythons   elif   in Java?",
     ["else if", "elsif", "elif", "otherwise"],
     "} else if (x > 0) { ...")

k.mc("Was bedeutet   void   in   void sayHello(String name)  ?",
     ["Die Funktion gibt keinen Wert zurück",
      "Die Funktion ist leer",
      "Die Funktion ist verboten",
      "Der Parameter ist optional"],
     "void = 'nichts'. Es gibt keinen Rückgabewert.")

k.mc("Wie gibt man in Java etwas in der Konsole aus?",
     ["System.out.println(...)", "print(...)", "console.log(...)", "echo ..."],
     "System.out.println gibt eine Zeile aus.")

k.mc("Finde den Fehler: Welche Java-Zeile kompiliert NICHT?",
     ["String name = 'Kim';",
      "String name = \"Kim\";",
      "int alter = 19;",
      "System.out.println(\"Hallo \" + name);"],
     "In Java stehen Strings immer in doppelten Anführungszeichen. 'Kim' mit einfachen "
     "Anführungszeichen ist ein Fehler.")

k.erklaerung("Schleifen und zwei Stolperfallen", r"""
    ## while-Schleife (Folie 29)

    :::vergleich 🐍 Python | ☕ Java
    Ganzzahl-Division mit //:
        while n > 0:
            n = n // 2 - 1
    |||
    Bei zwei int-Zahlen teilt / ganzzahlig:
        while (n > 0) {
            n = n / 2 - 1;
        }
    :::

    Zusätzlich gibt es in Java eine **do-while-Schleife**. Die lernst du im
    ersten Semester.

    :::achtung Java-/ und Python-// sind NICHT immer gleich
    Für positive Zahlen liefern beide dasselbe: 7 / 2 ist in Java 3, und
    7 // 2 ist in Python 3. Bei **negativen** Zahlen unterscheiden sie sich:
      • Java **schneidet ab** (Richtung 0): -7 / 2 ergibt -3.
      • Python **rundet ab** (Richtung minus unendlich): -7 // 2 ergibt -4.
    In der Schleife oben ist n immer positiv, deshalb ist es dort egal.
    :::

    :::code
    print(7 // 2, -7 // 2)        # Python rundet ab: 3 und -4
    print(int(7 / 2), int(-7 / 2))  # int() schneidet ab wie Java: 3 und -3
    :::
    ---
    ## for-each und for mit Zähler (Folien 30 und 31)

    :::vergleich 🐍 Python | ☕ Java
    for-each über eine Liste:
        fruits = ["apple", "orange", "banana"]
        for f in fruits:
            print(f + " tasted good")
    Zähler mit range:
        for i in range(1, 11):
            print(str(i) + " squared is " + str(i*i))
    |||
    for-each über ein Array:
        String[] fruits = {"apple", "orange", "banana"};
        for (String f : fruits) {
            System.out.println(f + " tasted good");
        }
    Start; Bedingung; Schritt:
        for (int i = 1; i < 11; ++i) {
            System.out.println(i + " squared is " + i*i);
        }
    :::

    `++i` erhöht i um 1 (wie `i += 1`). Und: Java wandelt beim `+` mit
    einem String Zahlen **automatisch** in Text um. In Python brauchst du
    dafür `str(...)`, sonst gibt es einen TypeError.

    :::info Auf den Folien steht …
    • Folie 30: In der Python-Liste steht `"orage"` (Tippfehler, gemeint
      ist `"orange"` wie in der Java-Version). Außerdem fehlt in
      `f + "tasted good"` das Leerzeichen. Die Ausgabe wäre
      `appletasted good`. Oben ist beides korrigiert.
    • Folie 31: In der Java-Zeile `System.out.println(...)` fehlt am Ende
      das **Semikolon**. So würde der Code nicht kompilieren.
    :::
    """)

k.mc("Java: int n = 7;  n = n / 2 - 1;   Welchem Python-Code entspricht das?",
     ["n = n // 2 - 1", "n = n / 2 - 1", "n = n % 2 - 1", "n = n ** 2 - 1"],
     "In Java ist / bei zwei int-Zahlen eine Ganzzahl-Division – in Python ist das //. "
     "Achtung: Das gilt so nur für nicht-negative Zahlen. Bei negativen Zahlen schneidet "
     "Java ab (-7 / 2 = -3), Python rundet ab (-7 // 2 = -4).")

k.mc("Java: int x = -7 / 2;   Welchen Wert hat x?",
     ["-3", "-4", "-3.5", "3"],
     "Java schneidet bei int-Division den Nachkommateil ab, also Richtung 0: -3.5 wird zu -3. "
     "Python würde mit -7 // 2 abrunden und -4 liefern.")

k.ausgabe("print(-7 // 2)",
          "Python rundet bei // immer ab (Richtung minus unendlich): -3.5 wird zu -4. "
          "In Java ergäbe -7 / 2 dagegen -3.",
          tipp="Abrunden bei negativen Zahlen geht weg von der 0.")

k.mc("Welche Java-Schleife entspricht   for i in range(1, 11):  ?",
     ["for (int i = 1; i < 11; ++i) { ... }",
      "for (int i = 1; i <= 11; ++i) { ... }",
      "for (i in 1..11) { ... }",
      "while (i < 11) for i"],
     "Start 1, Bedingung i < 11 (also bis 10), Schritt ++i (i um 1 erhöhen).")

k.mc("Finde den Fehler (Folie 31): Warum kompiliert diese Java-Zeile nicht?\n"
     "    System.out.println(i + \" squared is \" + i*i)",
     ["Am Ende fehlt das Semikolon ;",
      "i muss zuerst mit str(i) umgewandelt werden",
      "println muss print heißen",
      "Die Anführungszeichen müssen einfach sein"],
     "In Java endet jede Anweisung mit einem Semikolon. Die Umwandlung der Zahl in Text macht "
     "Java beim + mit einem String automatisch, str() gibt es in Java nicht.")

k.ausgabe('fruits = ["apple", "orage", "banana"]\nfor f in fruits:\n    print(f + "tasted good")',
          "Das ist der Python-Code von Folie 30, genau wie er dort steht. Zwei Fehler: "
          "\"orage\" statt \"orange\", und vor \"tasted\" fehlt das Leerzeichen. Python klebt "
          "die Strings mit + direkt aneinander.",
          tipp="+ fügt Strings ohne Leerzeichen zusammen.")

k.mc("Was passiert in Python bei   print(3 + \" squared\")  ?",
     ["TypeError – Python wandelt die Zahl nicht automatisch in Text um",
      "Es wird 3 squared ausgegeben",
      "Es wird 3squared ausgegeben",
      "Es wird 0 ausgegeben"],
     "Java wandelt beim + mit einem String automatisch um, Python nicht. In Python schreibst du "
     "str(3) + \" squared\" oder einen f-String.")

k.wf("Java hat eine do-while-Schleife, Python nicht.", True,
     "Stimmt. Die lernst du im ersten Semester kennen.")

# ── Praxisteil ───────────────────────────────────────────────────────────
k.luecke("Übersetze die Java-for-each-Schleife in Python:\n"
         "    for (String f : fruits) {\n"
         "        System.out.println(f + \" tasted good\");\n"
         "    }",
         """
         fruits = ["apple", "orange", "banana"]
         for f ___ fruits:
             ___(f + " tasted good")
         """,
         [["in"], ["print"]],
         "`for (String f : fruits)` heißt in Python `for f in fruits:`. Der Typ String fällt "
         "weg, der Doppelpunkt ersetzt die geschweifte Klammer. Aus System.out.println wird print.",
         tipp="Wie heißt das Wort zwischen Laufvariable und Liste in einer Python-for-Schleife?")

k.puzzle("Übersetze die Java-Verzweigung von Folie 28 nach Python. Achtung, zwei Zeilen sind "
         "Java-Reste und gehören nicht hinein.",
         """
         x = int(input("Zahl: "))
         if x < 0:
             print("Negativ")
         elif x > 0:
             print("Positiv")
         else:
             print("Null")
         """,
         "Aus `else if` wird `elif`, Klammern und `{ }` fallen weg, stattdessen Doppelpunkt und "
         "Einrückung.",
         tipp="Python kennt kein 'else if' und keine geschweiften Klammern.",
         ablenker=["else if x > 0:", "}"])

k.code(r"""
    ## Quadratzahlen (Folie 31 in Python)

    Übersetze den Java-Code von Folie 31 nach Python (mit korrigiertem
    Semikolon):

        for (int i = 1; i < 11; ++i) {
            System.out.println(i + " squared is " + i*i);
        }

    Erwartete Ausgabe:

        1 squared is 1
        2 squared is 4
        ...
        10 squared is 100
    """,
    [P([], exakt=[f"{i} squared is {i * i}" for i in range(1, 11)],
       beschreibung="genau die 10 Zeilen")],
    """
    for i in range(1, 11):
        print(str(i) + " squared is " + str(i * i))
    """,
    "`for (int i = 1; i < 11; ++i)` läuft von 1 bis 10, also `range(1, 11)`. In Python "
    "müssen die Zahlen mit `str(...)` in Text umgewandelt werden, bevor man sie mit + an "
    "einen String hängt. Ein f-String geht auch: `print(f\"{i} squared is {i * i}\")`.",
    tipps=["Welches range passt zu Start 1 und Bedingung i < 11?",
           "Zahlen und Strings kann man in Python nicht direkt mit + verbinden.",
           "print(str(i) + \" squared is \" + str(i * i))"])

k.code(r"""
    ## Halbieren (Folie 29 als Funktion)

    Auf Folie 29 wird n in einer while-Schleife immer wieder mit
    `n = n // 2 - 1` verkleinert, solange n > 0 ist.

    Schreibe eine Funktion `halbieren(n)`, die eine Liste mit **allen
    Werten** zurückgibt, die n dabei nacheinander annimmt (nicht den
    Startwert).

        halbieren(20)  →  [9, 3, 0]
        halbieren(7)   →  [2, 0]
        halbieren(0)   →  []
    """,
    [F("halbieren(20)", [9, 3, 0]), F("halbieren(7)", [2, 0]), F("halbieren(0)", []),
     F("halbieren(1)", [-1]), F("halbieren(100)", [49, 23, 10, 4, 1, -1])],
    """
    def halbieren(n):
        werte = []
        while n > 0:
            n = n // 2 - 1
            werte.append(n)
        return werte
    """,
    "Die Schleife ist genau die von der Folie. Nach jeder Änderung wird der neue Wert an die "
    "Liste gehängt. Bei n = 1 ergibt 1 // 2 - 1 = -1. Danach ist die Bedingung n > 0 falsch "
    "und die Schleife endet.",
    tipps=["Starte mit einer leeren Liste und übernimm die while-Schleife von der Folie.",
           "Nach  n = n // 2 - 1  den neuen Wert mit append an die Liste hängen.",
           "while n > 0:\n    n = n // 2 - 1\n    werte.append(n)\nreturn werte"],
    vorlage="def halbieren(n):\n    werte = []\n    ...\n    return werte\n")

k.code(r"""
    ## Teilen wie Java

    Schreibe eine Python-Funktion `java_teilen(a, b)`, die zwei ganze
    Zahlen so teilt, wie Java es bei int-Zahlen tut: Das Ergebnis wird
    **Richtung 0 abgeschnitten**.

        java_teilen(7, 2)    →  3
        java_teilen(-7, 2)   →  -3      (Python: -7 // 2 wäre -4!)
        java_teilen(7, -2)   →  -3
        java_teilen(-8, 2)   →  -4
    """,
    [F("java_teilen(7, 2)", 3), F("java_teilen(-7, 2)", -3), F("java_teilen(7, -2)", -3),
     F("java_teilen(-7, -2)", 3), F("java_teilen(-8, 2)", -4), F("java_teilen(0, 5)", 0),
     F("java_teilen(-1, 3)", 0)],
    """
    def java_teilen(a, b):
        ergebnis = abs(a) // abs(b)       # mit positiven Zahlen sind / und // gleich
        if (a < 0) != (b < 0):            # genau eine Zahl negativ?
            return -ergebnis
        return ergebnis
    """,
    "Mit Beträgen (`abs`) ist alles positiv, dann schneidet `//` richtig ab. Ist genau eine "
    "der beiden Zahlen negativ, ist das Ergebnis negativ. Kürzer geht es mit "
    "`int(a / b)`: `int()` schneidet ebenfalls Richtung 0 ab (bei sehr großen Zahlen kann "
    "die Kommazahl aber ungenau werden).",
    tipps=["Probier aus: Was liefert -7 // 2 und was int(-7 / 2)?",
           "Rechne mit abs(a) // abs(b) und überlege dann das Vorzeichen.",
           "Negativ ist das Ergebnis, wenn (a < 0) != (b < 0)."],
    vorlage="def java_teilen(a, b):\n    ...\n")

k.zusammenfassung(r"""
    ## Python und Java auf einen Blick

    | Python | Java |
    |---|---|
    | `x = 5` | `int x = 5;` |
    | `s = 'Lorem'` oder `"Lorem"` | `String s = "Lorem";` (nur doppelte!) |
    | `elif` | `else if` |
    | `print(...)` | `System.out.println(...);` |
    | `for f in fruits:` | `for (String f : fruits) { … }` |
    | `for i in range(1, 11):` | `for (int i = 1; i < 11; ++i) { … }` |
    | `def say_hello(name):` | `void sayHello(String name) { … }` |
    | `str(i) + " …"` | `i + " …"` (automatische Umwandlung) |

      • Statische Typisierung: Typen stehen im Quelltext.
      • Einrückung ist egal, Blöcke stehen in `{ }`, Anweisungen enden mit `;`.
      • Java wird mit `javac` in Bytecode kompiliert, Fehler fallen vor dem Start auf.
      • Java kennt zusätzlich die do-while-Schleife.

    !! Java-/ (int) schneidet ab: -7 / 2 = -3. Python-// rundet ab: -7 // 2 = -4.
    """)
