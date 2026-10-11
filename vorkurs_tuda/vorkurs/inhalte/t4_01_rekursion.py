# -*- coding: utf-8 -*-
"""Kapitel: Rekursion – Die Matroschka (Vorlesung 4, Livecoding 4)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="rekursion",
    titel="Rekursion – Die Matroschka",
    beschreibung="Funktionen, die sich selbst aufrufen: Anker, Schritt und Aufrufstapel",
    quelle="Vorlesung 4, Livecoding 4",
    teil="tag4",
    icon="🪆")

k.lernziele([
    "Ich kann erklären, was Rekursionsanker und Rekursionsschritt sind",
    "Ich kann verfolgen, wie der Aufrufstapel bei einer rekursiven Funktion wächst und wieder abgebaut wird",
    "Ich kann einfache rekursive Funktionen selbst schreiben",
    "Ich kann rekursiv durch verschachtelte Listen und Ordner laufen",
    "Ich erkenne, warum ein RecursionError entsteht, und kann ihn beheben",
])

# ── Erklärung 1: Was ist Rekursion? ──────────────────────────────────────
k.erklaerung("Was ist Rekursion?", r"""
    ## Funktionen können sich selbst aufrufen!

    Mit Funktionen und Schleifen kannst du im Prinzip schon alles
    programmieren. Manchmal wird der Code damit aber nicht schön.
    Eine sehr wichtige Eigenschaft von Funktionen fehlt noch:

    !! Eine Funktion darf sich in ihrem eigenen Körper selbst aufrufen.

    Das nennt man **Rekursion** (von lateinisch *recurrere*, zurücklaufen).
    Eine Funktion, die das tut, heißt **rekursive Funktion**.

    Rekursion im Alltag (Bilder aus Vorlesung 4):
      • Videokonferenz: Du teilst deinen Bildschirm, auf dem die Konferenz
        läuft. Darin siehst du den Bildschirm, darin wieder den Bildschirm …
      • Die Droste-Kakaodose: Auf der Dose ist eine Frau mit derselben Dose,
        auf der wieder die Frau mit der Dose ist …
      • In der Natur: Romanesco. Jedes Röschen sieht aus wie der ganze Kopf.
      • In der Informatik: Binärbäume. Jeder Ast ist selbst wieder ein Baum.
    ---
    ## Die Matroschka

    :::analogie 🪆 Matroschka-Puppen
    Anna bekommt eine Matroschka geschenkt und will wissen, wie viele Puppen
    darin stecken. Ihr Plan ist immer derselbe:

    1. Puppe ansehen. Lässt sie sich **nicht** öffnen? Dann ist es die
       kleinste. Antwort: „1 Puppe“. Hier hört das Öffnen auf.
    2. Lässt sie sich öffnen? Dann holt Anna die nächste Puppe heraus und
       macht mit ihr **genau dasselbe** (zurück zu Schritt 1).
    3. Kommt die Antwort aus der kleineren Puppe zurück, zählt Anna eins
       dazu: „In der kleineren stecken 3, also sind es mit dieser 4.“

    Die kleinste Puppe ist der **Rekursionsanker**. „Öffnen und mit der
    kleineren Puppe dasselbe tun“ ist der **Rekursionsschritt**. Wichtig:
    Jede Puppe ist kleiner als die vorige. Deshalb kommt Anna sicher an.
    :::

    So sieht Annas Plan als Python-Funktion aus (die Puppen sind hier nur
    eine Zahl, die bei jedem Öffnen kleiner wird):

    :::code
    def puppen_zaehlen(groesse):
        if groesse == 1:                  # kleinste Puppe: Rekursionsanker
            return 1
        return 1 + puppen_zaehlen(groesse - 1)   # Rekursionsschritt

    print(puppen_zaehlen(4))
    :::
    ---
    ## Anker und Schritt

    Viele Dinge (besonders in Mathe und Informatik) sind in Bezug auf sich
    selbst definiert. Das nennt man eine **rekursive Definition**.
    Beispiele aus der Vorlesung:
      • die Fibonacci-Folge
      • die Fakultät
      • der Programmcode, den wir schreiben (Blöcke in Blöcken)
      • Dateisysteme: Ordner können Unterordner haben, die wieder
        Unterordner haben …

    Jede Rekursion besteht aus zwei Teilen:

    | Teil | Bedeutung | Matroschka |
    |---|---|---|
    | **Rekursionsanker** | Anfangs- bzw. Ausgangszustand: Hier ruft sich die Funktion NICHT mehr auf. | die kleinste Puppe |
    | **Rekursionsschritt** | Anweisungen, um von einem Zustand zum nächsten zu kommen: Problem verkleinern und sich selbst aufrufen. | öffnen und mit der kleineren Puppe weitermachen |

    !! Ohne Anker hört die Rekursion nie auf. Ohne Verkleinern erreicht
    !! sie den Anker nie.
    ---
    ## Beispiel: Eine Datei im Ordner suchen

    Szenario aus der Vorlesung: Du willst vom obersten Ordner (dem
    **Wurzelknoten**) aus eine Datei finden.

      • Gehe die Liste der Unterelemente des Ordners durch und prüfe, ob die
        gesuchte Datei dabei ist.
      • Für jeden Unterordner: Mach dort **genau dasselbe**. Das ist der
        Rekursionsschritt.
      • Wurde die Datei gefunden ODER gibt es keinen Unterordner mehr (man
        kann nicht weiter „absteigen“), kehrt die Suche zur Ebene darüber
        zurück. Das ist der Rekursionsanker.

    :::visual baum
    {"wurzel": {"text": "Tom", "kinder": [
        {"text": "Data", "kinder": [{"text": "One.txt"}, {"text": "Two.txt"}]},
        {"text": "Thesis"},
        {"text": "Notes.txt"},
        {"text": "Tools", "kinder": [{"text": "Format"}, {"text": "Stats"}, {"text": "Old"}]}]}}
    :::

    Jeder Ordner ist selbst wieder ein kleiner Ordnerbaum. Deshalb passt
    Rekursion hier so gut.
    """)

k.mc("Was ist ein Rekursionsanker?",
     ["Der Fall, bei dem die Funktion sich NICHT mehr selbst aufruft und die Rekursion endet",
      "Der erste Aufruf der Funktion",
      "Eine besonders schwere Variable",
      "Der Fehler, der bei zu tiefer Rekursion kommt"],
     "Der Anker ist der Ausgangszustand, wie die kleinste Matroschka. Dort wird die Antwort "
     "direkt geliefert, ohne einen weiteren Aufruf. Der erste Aufruf ist dagegen der Start, "
     "nicht das Ende.")

k.mc("Bei den Matroschka-Puppen: Was ist der Rekursionsanker?",
     ["Die kleinste Puppe, die sich nicht mehr öffnen lässt",
      "Die größte Puppe",
      "Das Öffnen einer Puppe",
      "Der Laden, in dem man sie kauft"],
     "Bei der kleinsten Puppe hört das „Öffnen und weiter suchen“ auf. Das Öffnen selbst ist "
     "der Rekursionsschritt.")

k.mc("Wie macht man eine Funktion in Python rekursiv?",
     ["Indem sie sich in ihrem eigenen Körper selbst aufruft",
      "Indem man 'recursive' vor def schreibt",
      "Mit import recursion",
      "Indem man sie in eine while-Schleife packt"],
     "Eine rekursive Funktion ruft sich selbst auf, z. B. `return n * factorial(n - 1)`. "
     "Ein besonderes Schlüsselwort gibt es dafür nicht.")

k.mc("Was ist bei der Dateisuche im Ordnerbaum der Rekursionsschritt?",
     ["In jedem Unterordner wieder genau dieselbe Suche starten",
      "Die Datei gefunden haben",
      "Den Computer ausschalten",
      "Alle Dateien löschen"],
     "Der Schritt ist: „Mach in jedem Unterordner dasselbe“. Der Anker: Datei gefunden oder "
     "keine Unterordner mehr.")

k.ausgabe("def puppen_zaehlen(groesse):\n    if groesse == 1:\n        return 1\n"
          "    return 1 + puppen_zaehlen(groesse - 1)\n\nprint(puppen_zaehlen(6))",
          "puppen_zaehlen(6) = 1 + puppen_zaehlen(5) = 1 + 1 + puppen_zaehlen(4) … bis zum "
          "Anker puppen_zaehlen(1) = 1. Zusammen: 6.",
          tipp="Bei jedem Schritt kommt 1 dazu, bis die Größe 1 erreicht ist.")

# ── Erklärung 2: Fakultät und Aufrufstapel ───────────────────────────────
k.erklaerung("Die Fakultät und der Aufrufstapel", r"""
    ## Die Fakultät rekursiv

    Die **Fakultät** n! ist das Produkt 1 · 2 · 3 · … · n. Rekursiv
    definiert (Vorlesung 4, Folie 15):

        n! = 1               wenn n = 0      (Rekursionsanker)
        n! = n · (n - 1)!    wenn n > 0      (Rekursionsschritt)

    In Python steht das fast wörtlich so da:

    :::code
    def factorial(n):
        if n == 0:                      # Rekursionsanker
            return 1
        return n * factorial(n - 1)     # rekursiver Funktionsaufruf

    print(factorial(3))
    :::

    Was passiert bei factorial(3)? Python rechnet erst „nach unten“ und
    dann „zurück nach oben“:

        factorial(3) = 3 * factorial(2)
                     = 3 * (2 * factorial(1))
                     = 3 * (2 * (1 * factorial(0)))
                     = 3 * (2 * (1 * 1))
                     = 6
    ---
    ## Der Aufrufstapel – ein Tellerstapel

    :::analogie 🍽️ Tellerstapel in der Mensa
    Jeder Funktionsaufruf ist ein **Teller** mit einem Notizzettel darauf:
    „Ich bin fakultaet(3) und warte auf das Ergebnis von fakultaet(2).“

    • Ruft eine Funktion eine andere auf, kommt ein neuer Teller **oben**
      auf den Stapel. Der Teller darunter wartet.
    • Nur der oberste Teller wird gerade bearbeitet.
    • Ist eine Funktion fertig (`return`), wird ihr Teller abgeräumt. Ihr
      Ergebnis wandert zum Teller darunter, der jetzt weiterrechnen kann.

    Dieser Stapel heißt **Aufrufstapel** (englisch *call stack*). Python
    merkt sich darauf für jeden Aufruf die eigenen Variablen (hier `n`).
    Deshalb stören sich die vielen `n` nicht gegenseitig.
    :::

    So wächst und schrumpft der Stapel bei fakultaet(4):

    :::visual stapel
    {"titel": "Aufrufstapel bei fakultaet(4)",
     "rahmen": ["fakultaet(4)", "fakultaet(3)", "fakultaet(2)", "fakultaet(1)", "fakultaet(0)"],
     "rueckgaben": ["24", "6", "2", "1", "1"]}
    :::

    !! Erst wird der Stapel bis zum Anker aufgebaut, dann wird er von oben
    !! nach unten wieder abgebaut, und dabei wird gerechnet.
    ---
    ## Schritt für Schritt ansehen

    Klick auf „Schritt für Schritt“ und beobachte rechts den Aufrufstapel:
    Bei jedem Aufruf kommt ein neuer Rahmen mit einem eigenen `n` dazu.
    Beim Zurückkehren verschwinden sie wieder.

    :::trace
    def fakultaet(n):
        if n == 0:
            return 1
        ergebnis = n * fakultaet(n - 1)
        return ergebnis

    print(fakultaet(4))
    :::

    Beim tiefsten Punkt liegen **fünf** Teller auf dem Stapel:
    fakultaet(4), fakultaet(3), fakultaet(2), fakultaet(1) und
    fakultaet(0). Erst fakultaet(0) kann sofort antworten (Anker).

    :::achtung Typischer Fehler: return vergessen
    Wer im Rekursionsschritt das `return` weglässt, rechnet zwar, gibt das
    Ergebnis aber nicht nach unten weiter. Die Funktion liefert dann `None`:

        def fakultaet(n):
            if n == 0:
                return 1
            n * fakultaet(n - 1)      # FEHLT: return

    Danach scheitert `n * None` mit einem TypeError.
    :::
    """)

k.ausgabe("def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(5))",
          "5! = 5 · 4 · 3 · 2 · 1 · 1 = 120.")
k.ausgabe("def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(0))",
          "Direkt der Rekursionsanker: 0! = 1. Es kommt kein weiterer Aufruf dazu.")

k.text("Wie viele Aufrufe von fakultaet liegen bei fakultaet(4) im tiefsten Moment GLEICHZEITIG "
       "auf dem Aufrufstapel? (Zahl eingeben)",
       ["5", "fünf"],
       "fakultaet(4), (3), (2), (1) und (0): Das sind fünf Teller. Alle warten auf den nächsten, "
       "nur fakultaet(0) antwortet sofort mit 1.",
       tipp="Zähle von 4 bis 0 – die 0 nicht vergessen!")

k.mc("Der Aufrufstapel bei fakultaet(3) ist gerade am höchsten. Welcher Aufruf liegt GANZ OBEN "
     "und wird als Erstes fertig?",
     ["fakultaet(0)", "fakultaet(3)", "fakultaet(1)", "Alle werden gleichzeitig fertig"],
     "Der zuletzt gestartete Aufruf liegt oben: fakultaet(0). Er ist der Anker und gibt sofort "
     "1 zurück. Danach wird fakultaet(1) fertig, dann (2), zuletzt (3). Wie beim Tellerstapel: "
     "Was zuletzt draufkam, kommt zuerst weg.")

k.ausgabe("def countdown(n):\n    if n == 0:\n        print('Start!')\n        return\n    print(n)\n    countdown(n - 1)\n\ncountdown(3)",
          "Ein Countdown als Rekursion: 3, 2, 1, dann der Anker bei 0: Start!")

k.ausgabe("def zeige(n):\n    if n == 0:\n        return\n    zeige(n - 1)\n    print(n)\n\nzeige(3)",
          "Knifflig: Das print kommt NACH dem rekursiven Aufruf. Es wird also erst ganz nach "
          "unten abgestiegen (Stapel aufbauen). Beim Zurückkehren (Stapel abbauen) wird "
          "ausgegeben: zuerst zeige(1), dann zeige(2), dann zeige(3). Also 1, 2, 3.",
          tipp="Wann wird print ausgeführt – vor oder nach dem tieferen Aufruf?")

k.ausgabe("def summe(n):\n    if n == 0:\n        return 0\n    return n + summe(n - 1)\n\nprint(summe(4))",
          "4 + 3 + 2 + 1 + 0 = 10.")

# ── Erklärung 3: Mehrfache und wechselseitige Rekursion ──────────────────
k.erklaerung("Mehrfache und wechselseitige Rekursion", r"""
    ## Fibonacci: zwei Aufrufe auf einmal

    Die **Fibonacci-Folge** beginnt mit 0 und 1. Jede weitere Zahl ist die
    Summe der beiden Zahlen davor: 0, 1, 1, 2, 3, 5, 8, 13, 21, …

        fib(0) = 0
        fib(1) = 1
        fib(n) = fib(n - 1) + fib(n - 2)    für n > 1

    :::code
    def fibonacci(n):
        if n <= 1:                                  # Rekursionsanker (n = 0 und n = 1)
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)  # ZWEI rekursive Aufrufe

    print(fibonacci(7))
    :::

    !! Funktionen können sich auch MEHRMALS rekursiv aufrufen.

    Hier gibt es zwei Ankerfälle: n = 0 und n = 1. Der Vergleich `n <= 1`
    fasst beide zusammen. `return n` liefert dann genau 0 bzw. 1.
    ---
    ## Der Aufrufbaum

    Weil sich fibonacci zweimal aufruft, entsteht kein Stapel in einer
    Reihe, sondern ein **Aufrufbaum**. So sieht er bei fib(4) aus:

    :::visual baum
    {"wurzel": {"text": "fib(4)", "kinder": [
        {"text": "fib(3)", "kinder": [
            {"text": "fib(2)", "kinder": [{"text": "fib(1)"}, {"text": "fib(0)"}]},
            {"text": "fib(1)"}]},
        {"text": "fib(2)", "kinder": [{"text": "fib(1)"}, {"text": "fib(0)"}]}]}}
    :::

    Zähl mal nach: 9 Aufrufe für fib(4). Und fib(2) wird **zweimal**
    komplett neu berechnet! Bei fib(20) sind es schon 21 891 Aufrufe.
    Deshalb wird diese einfache Version für große n sehr langsam.

    :::info Andere Zählweise im Livecoding
    Im Livecoding 4 steht `if n <= 1: return 1`. Damit ist fib(0) = 1 und
    fib(1) = 1, die Folge lautet also 1, 1, 2, 3, 5, … Sie ist um eine
    Stelle verschoben. In der Vorlesung (Folie 17) und auf Übungsblatt 4
    gilt **fib(0) = 0** und fib(1) = 1. Das lernst du hier, und das prüfen
    auch die Aufgaben.
    :::
    ---
    ## Hin und her: wechselseitige Rekursion

    Zwei Funktionen dürfen sich auch gegenseitig aufrufen (Folie 16):

    :::code
    def is_even(n):
        if n == 0:              # Rekursionsanker
            return True
        return is_odd(n - 1)    # ruft die ANDERE Funktion auf

    def is_odd(n):
        if n == 0:              # Rekursionsanker
            return False
        return is_even(n - 1)

    print(is_even(4), is_odd(4))
    :::

    !! Rekursion kann auch hin und her springen.

    Die Idee: 4 ist gerade, wenn 3 ungerade ist. 3 ist ungerade, wenn 2
    gerade ist … bis zur 0, die gerade ist.

    :::achtung Der Anker muss für ALLE Eingaben erreichbar sein
    `is_even(-1)` ruft `is_odd(-2)` auf, dann `is_even(-3)` … Die Zahl
    entfernt sich immer weiter von 0. Der Anker wird nie erreicht und es
    kommt zum RecursionError. Prüfe immer: Wird das Problem bei JEDER
    erlaubten Eingabe kleiner und landet beim Anker?
    :::
    """)

k.ausgabe("def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n - 1) + fibonacci(n - 2)\n\nprint(fibonacci(7))",
          "Die Folge: 0, 1, 1, 2, 3, 5, 8, 13 → fib(7) = 13.",
          tipp="fib(0) = 0, fib(1) = 1, jede weitere ist die Summe der beiden vorherigen.")

k.ausgabe("def is_even(n):\n    if n == 0:\n        return True\n    return is_odd(n - 1)\n\n"
          "def is_odd(n):\n    if n == 0:\n        return False\n    return is_even(n - 1)\n\nprint(is_even(7))",
          "is_even(7) → is_odd(6) → is_even(5) → ... → is_odd(0) → False. 7 ist ungerade.")

k.ausgabe("def fib(n):\n    if n <= 1:\n        return 1\n    return fib(n - 1) + fib(n - 2)\n\nprint(fib(5))",
          "Das ist die Livecoding-Variante mit `return 1`: 1, 1, 2, 3, 5, 8 → fib(5) = 8. "
          "Mit der Vorlesungs-Definition (fib(0) = 0) wäre fibonacci(5) = 5. "
          "Der Anker entscheidet, wo die Folge beginnt.",
          tipp="Hier ist fib(0) = 1 und fib(1) = 1.")

k.mc("Wie viele Aufrufe von fib gibt es insgesamt bei fib(4) (den ersten Aufruf mitgezählt)?",
     ["9", "4", "5", "16"],
     "Zähle die Knoten im Aufrufbaum: fib(4) 1 ×, fib(3) 1 ×, fib(2) 2 ×, fib(1) 3 ×, "
     "fib(0) 2 ×. Zusammen 9. Weil fib(2) doppelt berechnet wird, wächst die Zahl der "
     "Aufrufe sehr schnell.",
     tipp="Schau dir den Aufrufbaum für fib(4) an und zähle alle Knoten.")

k.mc("Wie viele Rekursionsanker braucht eine rekursive Funktion?",
     ["Mindestens einen", "Genau keinen", "Immer genau zwei", "So viele wie Parameter"],
     "Ohne Anker gibt es eine endlose Rekursion. Manchmal braucht man auch mehrere "
     "Ankerfälle (Fibonacci: n = 0 und n = 1, hier zusammengefasst als n <= 1).")

k.wf("is_even(-2) aus der Vorlesung liefert True.", False,
     "is_even(-2) → is_odd(-3) → is_even(-4) → … Die Zahl wird nie 0, der Anker wird nie "
     "erreicht. Nach etwa 1000 Aufrufen bricht Python mit RecursionError ab.")

# ── Erklärung 4: Grenzen ─────────────────────────────────────────────────
k.erklaerung("Grenzen der Rekursion: RecursionError", r"""
    ## Was passiert ohne Anker?

    Ohne Rekursionsanker ruft sich die Funktion endlos selbst auf. Jeder
    Aufruf legt einen neuen Teller auf den Stapel, keiner wird abgeräumt:

    :::visual stapel
    {"titel": "Unendliche Rekursion: fun(0)",
     "rahmen": ["fun(0)", "fun(1)", "fun(2)", "fun(3)", "…", "fun(996)", "💥 Stapel zu hoch!"]}
    :::

    Python hat eine **maximale Tiefe** von ungefähr **1000**
    Funktionsaufrufen. Ist der Stapel so hoch, bricht Python ab. Probier es aus:

    :::code
    def fun(num):
        fun(num + 1)      # kein Anker!

    fun(0)
    :::

    So liest du die Fehlermeldung (von oben nach unten):
      • `Traceback (most recent call last)`: Der jüngste Aufruf steht unten.
      • `fun(num + 1)` und darunter `[Previous line repeated 996 more times]`:
        Dieselbe Zeile wurde hunderte Male aufgerufen. (Die genaue Zahl hängt
        von der Python-Version ab, auf Folie 21 steht 988.)
      • Die letzte Zeile nennt die Fehlerart:
        `RecursionError: maximum recursion depth exceeded`.
    ---
    ## Weitere Fallen aus dem Livecoding

    1. **Das Problem wird nicht kleiner.** `f(n)` statt `f(n - 1)` ruft
       immer wieder dasselbe auf. Auch mit Anker gibt es dann einen
       RecursionError.
    2. **Zu viele Aufrufe trotz Anker.** Der Code unten ist richtig. Bei
       `f(10000)` bräuchte er aber 10 000 Teller und scheitert ebenfalls.
    3. **Anker mit größer-gleich.** Bei `if n >= 0: f(n - 1)` wird auch noch
       `f(-1)` aufgerufen. Deshalb erscheint am Ende noch `-1`.

    :::code
    def f(n):
        print(n)
        if (n >= 0):     # Klammern sind Java-Stil, in Python erlaubt, aber unnötig
            f(n - 1)

    f(3)
    :::

    :::achtung Finde den Fehler (Livecoding 4)
    Eigentlich sollte im Livecoding eine Endlos-Rekursion gezeigt werden:

        def f():
            print(n)
            f(n)

        f(20)

    Es kommt aber kein RecursionError, sondern sofort ein **TypeError**:
    `f() takes 0 positional arguments but 1 was given`. Der Parameter `n`
    fehlt in der ersten Zeile. Richtig wäre `def f(n):`.
    :::
    ---
    ## Rekursion oder Schleife?

    „Grundsätzlich lässt sich jede Schleife in Python auch mit Rekursion
    umsetzen.“ Ausnahme: Endlosschleifen bzw. Schleifen mit zu vielen
    Durchläufen (Folie 19). Eine Schleife wiederholt etwas, ohne den Stapel
    wachsen zu lassen. Das nennt man **Iteration**.

    :::vergleich 🪆 Rekursiv | 🔁 Mit Schleife (iterativ)
    Elegant, wenn das Problem rekursiv definiert ist:
        def fak(n):
            if n == 0:
                return 1
            return n * fak(n - 1)
    Braucht für fak(2000) mehr als 1000 Teller → RecursionError.
    |||
    Etwas mehr Code, dafür ohne Tiefenlimit:
        def fak(n):
            ergebnis = 1
            for i in range(1, n + 1):
                ergebnis *= i
            return ergebnis
    fak(2000) ist kein Problem.
    :::

    Was ist besser? **Kommt auf das Problem an.** Für verschachtelte
    Strukturen (Ordner, Bäume, Listen in Listen) ist Rekursion oft
    einfacher. Für einfaches Zählen und Wiederholen sind Schleifen in
    Python meist effizienter.
    """)

k.ausgabe("def fun(num):\n    fun(num + 1)\n\nfun(0)",
          "Kein Rekursionsanker → die Funktion ruft sich endlos auf, bis Python bei ca. 1000 "
          "Aufrufen abbricht: RecursionError. (Vorlesung 4)")

k.ausgabe("def f(n):\n    print(n)\n    if (n >= 0):\n        f(n - 1)\n\nf(3)",
          "Ausgegeben wird VOR der Prüfung. Bei n = 0 ist `0 >= 0` noch wahr, also wird f(-1) "
          "aufgerufen und gibt -1 aus. Erst dort ist `-1 >= 0` falsch. Ausgabe: 3, 2, 1, 0, -1.",
          tipp="Wird bei n = 0 noch einmal f aufgerufen? Prüfe 0 >= 0.")

k.ausgabe("def f():\n    print(n)\n    f(n)\n\nf(20)",
          "Der Aufruf f(20) übergibt ein Argument, aber `def f():` hat keinen Parameter. "
          "Python meldet sofort einen TypeError, noch bevor irgendetwas ausgegeben wird. "
          "Das ist der Tippfehler aus dem Livecoding 4.",
          tipp="Schau dir die Klammern bei def f(): genau an.")

k.wf("Python kann beliebig tief rekursiv aufrufen.", False,
     "Die maximale Aufruftiefe liegt bei ungefähr 1000. Danach: RecursionError.")

k.mc("Die Funktion f(n) aus dem Livecoding hat einen korrekten Anker. Was passiert trotzdem bei "
     "f(10000)?",
     ["Nach etwa 1000 Ausgaben bricht Python mit RecursionError ab",
      "Es werden alle Zahlen von 10000 bis -1 ausgegeben",
      "Python wartet, bis genug Speicher frei ist",
      "Es gibt sofort einen TypeError"],
     "Auch richtige Rekursion braucht für jeden Aufruf einen Teller auf dem Stapel. Mehr als "
     "etwa 1000 gleichzeitig erlaubt Python nicht. Für so viele Wiederholungen nimmt man eine "
     "Schleife.")

k.mc("Ist im Allgemeinen Rekursion oder Iteration (Schleifen) sinnvoller?",
     ["Kommt auf das Problem an – Rekursion ist oft eleganter, Schleifen oft effizienter",
      "Immer Rekursion",
      "Immer Iteration",
      "Beides ist verboten"],
     "Quiz aus Vorlesung 4: Für verschachtelte Strukturen ist Rekursion toll. In Python "
     "sind Schleifen meist effizienter und haben kein Tiefenlimit.")

k.wf("Grundsätzlich lässt sich jede Schleife auch mit Rekursion umsetzen (außer bei zu vielen Durchläufen).", True,
     "Genau so steht es in Vorlesung 4. Die Grenze ist die maximale Rekursionstiefe.")

# ── Erklärung 5: Verschachtelte Listen und Ordner ───────────────────────
k.erklaerung("Rekursion über Listen in Listen und Ordner", r"""
    ## Listen in Listen ausgeben (Livecoding 4)

    Eine Liste kann wieder Listen enthalten, und die wieder Listen …
    Mit einer Schleife allein weißt du nicht, wie tief du graben musst.
    Mit Rekursion ist es einfach:

    :::code
    def print_list(lst):
        for e in lst:
            if type(e) == list:     # e ist selbst eine Liste?
                print_list(e)       # dann dasselbe mit der inneren Liste
            else:
                print(e)            # sonst: einfach ausgeben

    print_list([5, [3, 6, 2, [1, 4], 3], 7, 8, [10]])
    :::

    Wo ist hier der Anker? Es gibt kein `if … return`. Der Anker ist eine
    Liste **ohne** innere Listen: Dann ruft sich print_list nicht mehr auf,
    die Schleife endet und die Funktion kehrt zurück.

    :::analogie 📦 Kisten in Kisten
    Kim räumt den Keller auf. In einer Kiste liegen Bücher und weitere
    Kisten. Kims Regel: „Nimm jedes Ding aus der Kiste. Ist es ein Buch,
    stell es ins Regal. Ist es eine Kiste, mach mit ihr genau dasselbe.“
    Egal wie tief die Kisten ineinander stecken: Die Regel funktioniert.
    :::
    ---
    ## Ordnerbaum ausgeben (Livecoding 4)

    Ordner sind rekursiv aufgebaut. Mit dem Modul `os` kannst du sie
    durchlaufen:
      • `os.listdir(ordner)` liefert die Namen aller Einträge im Ordner.
      • `os.path.isdir(pfad)` prüft, ob ein Pfad ein Ordner ist.

    Das Beispiel legt zuerst ein paar Ordner an (os.makedirs) und gibt
    dann den Baum aus. `depth` ist die Tiefe, sie steuert die Einrückung:

    :::code
    import os
    os.makedirs("schule/mathe", exist_ok=True)
    os.makedirs("schule/info/python", exist_ok=True)
    open("schule/info/python/hallo.py", "w").close()

    def tree(folder, depth):
        children = sorted(os.listdir(folder))
        for child in children:
            print(("| " * depth) + "+-", child)
            path = folder + "/" + child
            if os.path.isdir(path):
                tree(path, depth + 1)

    tree("schule", 0)
    :::

    (Im Livecoding steht `os.listdir` ohne `sorted`. `sorted` sorgt hier
    nur für eine feste Reihenfolge.)
    """)

k.ausgabe("def print_list(lst):\n    for e in lst:\n        if type(e) == list:\n            print_list(e)\n"
          "        else:\n            print(e)\n\nprint_list([1, [2, [3]], 4])",
          "print_list steigt in jede innere Liste ab und gibt die Zahlen der Reihe nach aus: "
          "1, 2, 3, 4. Die Klammern der Listen erscheinen nicht.",
          tipp="Jede Zahl landet in einer eigenen Zeile – egal wie tief sie steckt.")

k.mc("Was würde print_list([5, [3, 6]]) ausgeben, wenn man die Prüfung `if type(e) == list` "
     "weglässt und immer nur `print(e)` macht?",
     ["5 und dann [3, 6] als Ganzes",
      "5, 3 und 6 einzeln",
      "Einen RecursionError",
      "Gar nichts"],
     "Ohne die Prüfung gibt es keinen rekursiven Aufruf. Die innere Liste ist dann einfach ein "
     "Element und wird komplett mit Klammern ausgegeben.")

k.mc("Warum braucht tree(folder, depth) den Parameter depth?",
     ["Damit tiefere Ordner weiter eingerückt ausgegeben werden",
      "Damit Python weiß, wann der Speicher voll ist",
      "Weil os.listdir sonst nicht funktioniert",
      "depth zählt die Dateien im Ordner"],
     "Jeder rekursive Aufruf bekommt depth + 1. So wird `\"| \" * depth` mit jeder Ebene länger "
     "und man sieht die Verschachtelung.")

# ── Praxisteil ───────────────────────────────────────────────────────────
k.luecke("Ergänze den Countdown: Er soll n, n-1, …, 1 und dann 'Start!' ausgeben. "
         "Fülle den Rekursionsanker und den Rekursionsschritt aus.",
         """
         def countdown(n):
             if n == ___:
                 print('Start!')
                 return
             print(n)
             countdown(___)
         """,
         [["0"], ["n - 1", "n-1"]],
         "Der Anker ist n == 0 (dort wird 'Start!' ausgegeben). Im Schritt wird das Problem "
         "kleiner: countdown(n - 1).",
         tipp="Bei welcher Zahl soll 'Start!' kommen? Und wie wird n bei jedem Schritt kleiner?")

k.puzzle("Bringe die Zeilen in die richtige Reihenfolge: print_list soll alle Zahlen einer "
         "verschachtelten Liste einzeln ausgeben.",
         """
         def print_list(lst):
             for e in lst:
                 if type(e) == list:
                     print_list(e)
                 else:
                     print(e)

         print_list([1, [2, 3], [[4]]])
         """,
         "Für jedes Element: Ist es eine Liste, ruft sich die Funktion selbst auf. Sonst wird "
         "das Element ausgegeben.",
         tipp="Erst die Schleife über die Elemente, darin die Unterscheidung Liste / keine Liste.",
         ablenker=["        print_list(lst)", "    return lst[0]"])

k.code(r"""
    ## Kekspyramide

    Ben stapelt Kekse zu einer Pyramide: In der obersten Reihe liegt 1 Keks,
    in der zweiten 2, in der dritten 3 … in der Reihe n liegen n Kekse.

    Schreibe eine **rekursive** Funktion `pyramide(n)`, die zurückgibt, wie
    viele Kekse eine Pyramide mit n Reihen insgesamt braucht. Schleifen sind
    nicht erlaubt.

        pyramide(0)  →  0
        pyramide(1)  →  1
        pyramide(4)  →  10     (1 + 2 + 3 + 4)
    """,
    [F("pyramide(0)", 0), F("pyramide(1)", 1), F("pyramide(4)", 10), F("pyramide(100)", 5050)],
    """
    def pyramide(n):
        if n == 0:                      # Rekursionsanker: keine Reihe, keine Kekse
            return 0
        return n + pyramide(n - 1)      # unterste Reihe + kleinere Pyramide
    """,
    "Anker: Eine Pyramide mit 0 Reihen hat 0 Kekse. Schritt: Eine Pyramide mit n Reihen ist "
    "die unterste Reihe (n Kekse) plus eine Pyramide mit n - 1 Reihen.",
    verboten=["for", "while"],
    rekursiv="pyramide",
    tipps=["Was ist die kleinste Pyramide, deren Antwort du sofort kennst?",
           "Eine Pyramide mit n Reihen = n Kekse unten + Pyramide mit n - 1 Reihen.",
           "if n == 0: return 0   und sonst   return n + pyramide(n - 1)"],
    vorlage="def pyramide(n):\n    if n == 0:\n        ...\n    return ...\n")

k.code(r"""
    ## Quersumme rekursiv

    Die Quersumme ist die Summe aller Ziffern: quersumme(1234) = 1+2+3+4 = 10.
    Schreibe eine rekursive Funktion   quersumme(n)   für n >= 0.

    Trick (Modulo und Ganzzahl-Division!):
        1234 % 10   → 4      (die letzte Ziffer)
        1234 // 10  → 123    (die Zahl ohne letzte Ziffer)
    """,
    [F("quersumme(0)", 0), F("quersumme(7)", 7), F("quersumme(1234)", 10),
     F("quersumme(99999)", 45), F("quersumme(1000)", 1)],
    """
    def quersumme(n):
        if n < 10:
            return n
        return n % 10 + quersumme(n // 10)
    """,
    "Anker: Eine einstellige Zahl ist ihre eigene Quersumme. Schritt: letzte Ziffer + "
    "Quersumme vom Rest. (Anker n == 0 → return 0 funktioniert auch.)",
    tipp="Letzte Ziffer: n % 10. Rest: n // 10. Anker: n < 10.",
    rekursiv="quersumme",
    tipps=["Welche Zahlen haben eine Quersumme, die du sofort kennst?",
           "Anker: n < 10. Schritt: letzte Ziffer (n % 10) plus Quersumme vom Rest (n // 10).",
           "return n % 10 + quersumme(n // 10)"])

_ORDNER = """
import os as _os
_os.makedirs("projekt/hilfe", exist_ok=True)
_os.makedirs("projekt/daten/tief", exist_ok=True)
for _name in ["projekt/main.py", "projekt/bild.png", "projekt/hilfe/werkzeug.py",
              "projekt/hilfe/notizen.txt", "projekt/daten/tief/skript.py"]:
    open(_name, "w").close()
"""

k.code(r"""
    ## Finde den Fehler: Dateien mit bestimmter Endung (Livecoding 4)

    Im Livecoding sollte `tree(folder, ext)` alle Dateien mit der Endung
    `ext` in einem Ordner **und allen Unterordnern** ausgeben. Der Code im
    Editor stürzt aber beim ersten Unterordner ab.

    Finde und behebe den Fehler. Der Ordner `projekt` wird beim Testen
    automatisch angelegt:

        projekt/main.py
        projekt/bild.png
        projekt/hilfe/werkzeug.py
        projekt/hilfe/notizen.txt
        projekt/daten/tief/skript.py

    Erwartete Ausgabe (Reihenfolge egal):

        projekt/main.py
        projekt/hilfe/werkzeug.py
        projekt/daten/tief/skript.py
    """,
    [P(vorspann=_ORDNER,
       # Windows-Pfade (os.path.join) mit \ sind auch richtig
       erwartet=[("projekt/main.py", "projekt\\main.py"),
                 ("projekt/hilfe/werkzeug.py", "projekt\\hilfe\\werkzeug.py"),
                 ("projekt/daten/tief/skript.py", "projekt\\daten\\tief\\skript.py")],
       nicht=["notizen.txt", "bild.png"],
       beschreibung="alle .py-Dateien, auch in Unterordnern"),
     P(vorspann=_ORDNER, nachspann='print("---")\ntree("projekt", "txt")',
       erwartet=[("projekt/hilfe/notizen.txt", "projekt\\hilfe\\notizen.txt")],
       beschreibung="danach tree(\"projekt\", \"txt\")")],
    """
    import os

    def tree(folder, ext):
        children = os.listdir(folder)
        for child in children:
            path = folder + "/" + child
            if path.endswith("." + ext):
                print(path)
            if os.path.isdir(path):
                tree(path, ext)

    tree("projekt", "py")
    """,
    "Der rekursive Aufruf `tree(path)` hat das zweite Argument vergessen. Die Funktion "
    "verlangt aber zwei Parameter, also gibt es einen TypeError (`missing 1 required "
    "positional argument: 'ext'`). Richtig ist `tree(path, ext)`: Die Endung muss an jede "
    "tiefere Ebene weitergereicht werden.",
    rekursiv="tree",
    tipps=["Lies die Fehlermeldung: Welches Argument fehlt?",
           "Schau dir den rekursiven Aufruf in der letzten Zeile der Funktion an.",
           "Ändere tree(path) zu tree(path, ext)."],
    vorlage="import os\n\ndef tree(folder, ext):\n    children = os.listdir(folder)\n"
            "    for child in children:\n        path = folder + \"/\" + child\n"
            "        if path.endswith(\".\" + ext):\n            print(path)\n"
            "        if os.path.isdir(path):\n            tree(path)\n\ntree(\"projekt\", \"py\")\n")

k.code(r"""
    ## Einkaufsliste glatt bügeln

    Deniz hat eine Einkaufsliste mit Unterlisten pro Laden, und manche
    Unterlisten haben wieder Unterlisten. Schreibe eine **rekursive**
    Funktion `flach(lst)`, die eine neue Liste mit allen Elementen ohne
    Verschachtelung zurückgibt (Reihenfolge bleibt gleich).

        flach(["Milch", ["Eier", "Mehl"], [["Zucker"]]])
            →  ["Milch", "Eier", "Mehl", "Zucker"]
        flach([5, [3, 6, 2, [1, 4], 3], 7, 8, [10]])
            →  [5, 3, 6, 2, 1, 4, 3, 7, 8, 10]
        flach([])  →  []

    Tipp: Das ist print_list aus dem Livecoding, nur dass die Elemente
    gesammelt statt ausgegeben werden.
    """,
    [F('flach(["Milch", ["Eier", "Mehl"], [["Zucker"]]])', ["Milch", "Eier", "Mehl", "Zucker"]),
     F("flach([5, [3, 6, 2, [1, 4], 3], 7, 8, [10]])", [5, 3, 6, 2, 1, 4, 3, 7, 8, 10]),
     F("flach([])", []),
     F("flach([[[]]])", []),
     F("flach([1, [2, [3, [4]]]])", [1, 2, 3, 4])],
    """
    def flach(lst):
        ergebnis = []
        for e in lst:
            if type(e) == list:
                ergebnis += flach(e)     # Ergebnis der inneren Liste anhängen
            else:
                ergebnis.append(e)
        return ergebnis
    """,
    "Wie print_list: Für jedes Element wird geprüft, ob es eine Liste ist. Wenn ja, liefert "
    "der rekursive Aufruf die flache Version der inneren Liste, und die wird mit `+=` "
    "angehängt. Sonst wird das Element mit `append` angehängt. Häufiger Fehler: das Ergebnis "
    "von `flach(e)` nicht verwenden. Dann gehen die inneren Elemente verloren.",
    rekursiv="flach",
    tipps=["Starte mit einer leeren Ergebnisliste und gehe alle Elemente durch.",
           "Ist ein Element eine Liste (type(e) == list), hole dir mit flach(e) ihre flache Version.",
           "ergebnis += flach(e)  für Listen, sonst  ergebnis.append(e); am Ende return ergebnis"],
    vorlage="def flach(lst):\n    ergebnis = []\n    for e in lst:\n        ...\n    return ergebnis\n")

k.zusammenfassung(r"""
    ## Rekursion auf einen Blick

    Eine **rekursive Funktion** ruft sich selbst auf. Sie braucht:

    | Teil | Aufgabe | Beispiel Fakultät |
    |---|---|---|
    | Rekursionsanker | einfachster Fall, Antwort ohne neuen Aufruf | `if n == 0: return 1` |
    | Rekursionsschritt | Problem verkleinern und sich selbst aufrufen | `return n * fak(n - 1)` |

        def fak(n):
            if n == 0:
                return 1
            return n * fak(n - 1)

    !! Ohne Anker oder ohne Verkleinern: RecursionError (Grenze ca. 1000 Aufrufe).

      • **Aufrufstapel**: Jeder Aufruf ist ein Teller mit eigenen Variablen.
        Erst wird bis zum Anker aufgebaut, dann wird zurückgerechnet.
      • **Mehrfache Rekursion**: fib ruft sich zweimal auf → Aufrufbaum,
        viele doppelte Berechnungen. fib(0) = 0, fib(1) = 1.
      • **Wechselseitige Rekursion**: is_even ruft is_odd auf und umgekehrt.
      • **Verschachtelte Listen / Ordner**: `if type(e) == list:` bzw.
        `os.path.isdir(pfad)` → rekursiv weitermachen.
      • Rekursiver Aufruf braucht ALLE Argumente (`tree(path, ext)`) und
        meist ein `return` davor.
      • Rekursion oder Schleife? Kommt aufs Problem an.
    """)
