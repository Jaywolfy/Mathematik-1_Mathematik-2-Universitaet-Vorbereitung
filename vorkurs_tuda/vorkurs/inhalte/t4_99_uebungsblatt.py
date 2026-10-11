# -*- coding: utf-8 -*-
"""Kapitel: Übungsblatt 4 – Rekursion (alle Aufgaben von Übung 4)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="uebung4",
    titel="Übungsblatt 4 – Rekursion",
    beschreibung="Alle Aufgaben von Übung 4: Pfannkuchen, Fakultät, Fibonacci, Pascal, ggT und RSA",
    quelle="Übung 4",
    teil="tag4",
    icon="📝")


# ── Aufgabe 2.3: even ODER odd ────────────────────────────────────────────
# Das Blatt erlaubt eine der beiden Funktionen. Der Vorspann definiert eine
# Prüf-Funktion, die zur Laufzeit nachsieht, welche der beiden es gibt.
# (Die Regeln wie max_funktionen prüfen nur den Code der Lernenden, nicht den Vorspann.)
_GERADE_VORSPANN = """
def _quiz_gerade(n):
    if 'even' in globals():
        return even(n)
    if 'odd' in globals():
        w = odd(n)
        return (not w) if isinstance(w, bool) else w
    raise NameError("Es gibt weder eine Funktion even noch eine Funktion odd")
"""


def _gerade_test(n):
    gerade = n % 2 == 0
    return F(f"_quiz_gerade({n})", gerade, vorspann=_GERADE_VORSPANN,
             beschreibung=f"even({n}) → {gerade}  bzw.  odd({n}) → {not gerade}")


k.lernziele([
    "Ich kann alle Aufgaben von Übungsblatt 4 selbstständig programmieren",
    "Ich kann Mengen mit einem Dictionary und einem Faktor umrechnen (Pfannkuchen)",
    "Ich kann Fakultät, Fibonacci, gerade/ungerade, Pascal-Einträge und den ggT rekursiv berechnen",
    "Ich kann dieselbe Aufgabe einmal mit Schleife und einmal rekursiv lösen",
    "Ich kann RSA-Schlüssel erzeugen und Zahlen damit ver- und entschlüsseln (Bonus)",
])

k.erklaerung("Worum geht es auf Übungsblatt 4?", r"""
    ## Übung 4 – Rekursion

    Das letzte Übungsblatt des Vorkurses hat drei Teile:

    | Aufgabe | Thema | Was du übst |
    |---|---|---|
    | 1 | Pfannkuchenrezept | Dictionary, Tupel, input, Dreisatz |
    | 2.1 – 2.5 | Rekursion | Fakultät, Fibonacci, gerade/ungerade, Pascalsches Dreieck, Liste umdrehen |
    | 3.1 – 3.2 | ggT und RSA (optional) | ggT rekursiv, Schlüssel erzeugen, ver- und entschlüsseln |

    Bei manchen Aufgaben macht das Blatt **Einschränkungen**, z. B. „ohne
    Schleifen“ oder „ohne `%` und `/`“. Das Quiz prüft diese Regeln
    automatisch. Achte auf die Zeilen „Regel …“ in den Testergebnissen.

    !! Lies die Aufgaben genau: Nur was auf dem Blatt steht, wird verlangt.

    Wenn du eine Aufgabe nicht schaffst: Erst die Tipps ansehen, dann im
    Kapitel „Rekursion – Die Matroschka“ nachlesen. Die Musterlösung
    kommt ganz zum Schluss.
    ---
    ## Kleine Ungenauigkeiten auf dem Blatt

    :::info Was auf dem Blatt steht – und was gemeint ist
    • 2.5: „Bereits in der ersten Aufgabe dieses Übungsblattes … Fakultät“.
      Die Fakultät steht aber in **Aufgabe 2.1** (Aufgabe 1 ist das
      Pfannkuchenrezept).
    • 3.1: „ggT … einer Funktion“. Gemeint ist der ggT **zweier Zahlen**.
    • 3.2.1: „φ(N) = (p − 1)(q − 1)“. Gemeint ist **φ(n)**, das in Übung 1
      **N** heißt: N = φ(n) = (p − 1)(q − 1). Mit dieser Bedeutung von N
      stimmen „ggT(e, N) = 1“ und „e · d mod N = 1“. Klein-n = p · q ist
      eine andere Zahl! (Mehr dazu bei Aufgabe 3.2.)
    • 2.4.2: Wie viele Zeilen „Tiefe“ bedeutet, steht nicht da. Hier gilt:
      **Tiefe = Anzahl der Zeilen**.
    :::
    """)

k.mc("Welche Einschränkung macht Übungsblatt 4 bei Aufgabe 2.3 (gerade oder ungerade)?",
     ["Kein % und kein /, und alles in einer einzigen Funktion",
      "Keine if-Anweisung",
      "Nur mit einer while-Schleife",
      "Zwei Funktionen even und odd, die sich gegenseitig aufrufen"],
     "Das Blatt verbietet den Modulo-Operator (%) und den Divisions-Operator (/) und verlangt "
     "ausdrücklich: „Ebenso soll dies mit einer einzigen Funktion umgesetzt werden.“ Das "
     "wechselseitige is_even/is_odd aus der Vorlesung zählt deshalb nicht.")

# ── Aufgabe 1 ─────────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 1: Pfannkuchenrezept", r"""
    ## Ein Rechner für Pfannkuchenzutaten

    Die Zutaten für 2 Personen sind laut Blatt:

    | Zutat | Menge | Einheit |
    |---|---|---|
    | Mehl | 350 | g |
    | Milch | 500 | ml |
    | Eier | 4 | Stück |
    | Zucker | 4 | TL |
    | Öl | 4 | EL |
    | Backpulver | 1 | TL |
    | Salz | 1 | Prise |

    Du gibst eine Zutat und ihre vorhandene Menge ein. Das Programm
    rechnet aus, wie viel du von **allen** Zutaten brauchst.

    :::analogie 🥞 Dreisatz in der Küche
    Kim hat noch 700 g Mehl. Das Rezept braucht 350 g, also hat Kim das
    **Doppelte**. Der Faktor ist 700 / 350 = 2. Mit genau diesem Faktor
    multipliziert Kim jede andere Zutat: 500 ml Milch · 2 = 1000 ml,
    4 Eier · 2 = 8 Eier …
    :::

    :::code eingaben=Mehl|700
    zutaten = {'Mehl': (350, 'g'), 'Milch': (500, 'ml'), 'Eier': (4, 'Stück')}
    zutat = input('Welche Zutat hast du? ')
    menge = float(input('Wie viel davon? '))
    faktor = menge / zutaten[zutat][0]          # Tupel: [0] = Menge, [1] = Einheit
    print('Faktor:', faktor)
    for name in zutaten:
        grundmenge, einheit = zutaten[name]
        print(f'- {name}: {grundmenge * faktor:.1f} {einheit}')
    :::

    `{menge:.1f}` gibt eine Kommazahl mit genau einer Nachkommastelle aus.
    """)

k.code(r"""
    ## Übung 4, Aufgabe 1 – Pfannkuchenrezept

    Schreibe ein Programm, dem man **die Zutat und die Menge dieser als
    Eingabe** gibt und das dann die Menge **aller** Zutaten ausgibt.

    Ablauf:
      1. `input()`: Name der Zutat, genau wie im Dictionary (z. B. `Mehl`)
      2. `input()`: vorhandene Menge als Zahl (z. B. `700` oder `2.5`)
      3. Ausgabe wie im Code-Schnipsel des Blatts: eine Kopfzeile und dann
         für jede Zutat eine Zeile `- Name: Menge Einheit` mit einer
         Nachkommastelle.

    Beispiel mit den Eingaben `Mehl` und `700`:

        Für die angegebene Menge werden folgende Zutaten benötigt:
        - Mehl: 700.0 g
        - Milch: 1000.0 ml
        - Eier: 8.0 Stück
        - Zucker: 8.0 TL
        - Öl: 8.0 EL
        - Backpulver: 2.0 TL
        - Salz: 2.0 Prise

    Der Code-Schnipsel vom Blatt steht schon im Editor.
    """,
    [P(["Mehl", "700"], ["Milch: 1000.0 ml", "Eier: 8.0 Stück", "Salz: 2.0 Prise"]),
     P(["Eier", "2"], ["Mehl: 175.0 g", "Milch: 250.0 ml", "Backpulver: 0.5 TL"]),
     P(["Milch", "250"], ["Zucker: 2.0 TL", "Öl: 2.0 EL", "Mehl: 175.0 g"]),
     P(["Backpulver", "3"], ["Mehl: 1050.0 g", "Eier: 12.0 Stück", "Salz: 3.0 Prise"]),
     P(["Backpulver", "1.5"], ["Mehl: 525.0 g", "Eier: 6.0 Stück", "Salz: 1.5 Prise"],
       beschreibung="Eingaben: Backpulver, 1.5 (Kommazahl)")],
    """
    zutaten = {
        'Mehl': (350, 'g'),
        'Milch': (500, 'ml'),
        'Eier': (4, 'Stück'),
        'Zucker': (4, 'TL'),
        'Öl': (4, 'EL'),
        'Backpulver': (1, 'TL'),
        'Salz': (1, 'Prise')
    }

    zutat = input('Welche Zutat hast du? ')
    menge = float(input('Wie viel davon? '))

    faktor = menge / zutaten[zutat][0]
    for name in zutaten:
        grundmenge, einheit = zutaten[name]
        zutaten[name] = (grundmenge * faktor, einheit)

    print(f'Für die angegebene Menge werden folgende Zutaten benötigt:')
    for name in zutaten:
        menge, einheit = zutaten[name]
        print(f'- {name}: {menge:.1f} {einheit}')
    """,
    "Der Schlüssel ist der **Faktor**: vorhandene Menge geteilt durch die Rezeptmenge "
    "dieser Zutat. `zutaten[zutat][0]` holt aus dem Tupel die Rezeptmenge. Danach wird jede "
    "Zutat mit dem Faktor multipliziert. Hier wird das Dictionary mit den neuen Mengen "
    "überschrieben, damit die Ausgabe-Schleife vom Blatt unverändert bleiben kann. Wichtig: "
    "`float(...)` statt `int(...)`, damit auch 2.5 funktioniert.",
    tipps=["Wie oft passt die Rezeptmenge in die vorhandene Menge? Das ist dein Faktor.",
           "faktor = menge / zutaten[zutat][0]  – danach jede Grundmenge mal faktor.",
           "In einer for-Schleife: grundmenge, einheit = zutaten[name]; "
           "zutaten[name] = (grundmenge * faktor, einheit)"],
    vorlage="zutaten = {\n    'Mehl': (350, 'g'),\n    'Milch': (500, 'ml'),\n    'Eier': (4, 'Stück'),\n"
            "    'Zucker': (4, 'TL'),\n    'Öl': (4, 'EL'),\n    'Backpulver': (1, 'TL'),\n"
            "    'Salz': (1, 'Prise')\n}\n\n# TODO Hier Code einfügen\n\n"
            "# Die Ausgabe kann zum Beispiel so aussehen\n"
            "print(f'Für die angegebene Menge werden folgende Zutaten benötigt:')\n"
            "for name in zutaten:\n    menge, einheit = zutaten[name]\n"
            "    print(f'- {name}: {menge:.1f} {einheit}')\n",
    streng=True)

# ── Aufgabe 2.1 / 2.2 ────────────────────────────────────────────────────
k.erklaerung("Aufgaben 2.1 und 2.2: Fakultät und Fibonacci", r"""
    ## Ohne Schleifen? Mit Rekursion!

    In Aufgabe 2.1 sollst du 1 · 2 · 3 · … · 15 = 15! **ohne Schleifen**
    berechnen. Das geht mit einer rekursiven Funktion:

      • Rekursionsanker: 0! = 1
      • Rekursionsschritt: n! = n · (n − 1)!

    In Aufgabe 2.2 berechnest du die Fibonacci-Zahlen rekursiv. Laut Blatt
    sind die ersten beiden Zahlen **0 und 1**:

        fib(0) = 0, fib(1) = 1, fib(n) = fib(n - 1) + fib(n - 2)
        Folge: 0, 1, 1, 2, 3, 5, 8, 13, ...

    :::achtung Die „ersten 20“ Fibonacci-Zahlen
    Die erste Zahl ist fib(0) = 0. Die ersten 20 sind also fib(0) bis
    fib(19), und die letzte davon ist **4181**. Wer `range(1, 21)` nimmt,
    lässt die 0 weg und gibt eine Zahl zu viel aus (6765).
    :::

    :::code
    def fib(n):
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)

    for i in range(5):        # die ersten 5: fib(0) bis fib(4)
        print(fib(i))
    :::

    Die Schleife außerhalb der Funktion ist hier erlaubt. Nur `fib` selbst
    muss rekursiv sein.
    """)

k.wf("Für die Ausgabe der ersten 20 Fibonacci-Zahlen ist `for i in range(1, 21): print(fib(i))` richtig.",
     False,
     "range(1, 21) liefert fib(1) bis fib(20). Damit fehlt die erste Zahl fib(0) = 0, und am "
     "Ende steht fib(20) = 6765. Richtig ist range(20), also fib(0) bis fib(19).")

k.code(r"""
    ## Übung 4, Aufgabe 2.1 (Teil 1) – Fakultät von 15

    Schreibe ein Programm, das den Wert des Ausdrucks
    1 · 2 · 3 · … · 15 = 15! (Fakultät von 15) **ohne Nutzung von
    Schleifen** berechnet und das Ergebnis auf der Konsole ausgibt.

    Schreibe dafür eine rekursive Funktion `fakultaet(n)` und gib
    `fakultaet(15)` aus.

    Erwartete Ausgabe:

        1307674368000
    """,
    [P([], ["1307674368000"]),
     F("fakultaet(15)", 1307674368000), F("fakultaet(0)", 1), F("fakultaet(1)", 1),
     F("fakultaet(6)", 720)],
    """
    def fakultaet(n):
        if n == 0:                       # Rekursionsanker: 0! = 1
            return 1
        return n * fakultaet(n - 1)      # Rekursionsschritt

    print(fakultaet(15))
    """,
    "Statt einer Schleife ruft sich `fakultaet` selbst auf, jedes Mal mit einer kleineren "
    "Zahl, bis der Anker n == 0 erreicht ist. Dann wird zurückgerechnet: "
    "1 · 1 · 2 · 3 · … · 15.",
    verboten=["for", "while", "math.factorial"],
    rekursiv="fakultaet",
    tipps=["Ohne Schleife bleibt nur: Die Funktion ruft sich selbst auf.",
           "Anker: fakultaet(0) ist 1. Schritt: fakultaet(n) = n * fakultaet(n - 1).",
           "def fakultaet(n):\n    if n == 0:\n        return 1\n    return n * fakultaet(n - 1)"])

k.code(r"""
    ## Übung 4, Aufgabe 2.1 (Teil 2) – Fakultät einer Eingabe

    Erweitere dein Programm so, dass es von **beliebigen Eingaben in der
    Konsole** die Fakultät berechnet. Weiterhin **ohne Schleifen**.

    Das Programm liest eine ganze Zahl n ≥ 0 mit `input()` ein und gibt
    n! aus, zum Beispiel so:

        Eingabe:  5
        Ausgabe:  5! = 120
    """,
    [P(["5"], ["120"]), P(["0"], ["1"]), P(["10"], ["3628800"]),
     P(["20"], ["2432902008176640000"]), P(["1"], ["1"])],
    """
    def fakultaet(n):
        if n == 0:
            return 1
        return n * fakultaet(n - 1)

    n = int(input('n = '))
    print(f'{n}! = {fakultaet(n)}')
    """,
    "Die Funktion bleibt gleich. Neu ist nur: Die Zahl kommt von `input()` und muss mit "
    "`int(...)` in eine ganze Zahl umgewandelt werden. Hinweis: Für sehr große n (über "
    "etwa 990) scheitert die Rekursion am Tiefenlimit von Python.",
    verboten=["for", "while", "math.factorial"],
    rekursiv="fakultaet",
    tipps=["Nimm deine Funktion aus Teil 1 und ändere nur den Aufruf.",
           "input() liefert Text – wandle ihn mit int(...) um.",
           "n = int(input())\nprint(fakultaet(n))"])

k.code(r"""
    ## Übung 4, Aufgabe 2.2 – Fibonacci

    Die ersten beiden Fibonacci-Zahlen sind 0 und 1. Jede weitere ist die
    Summe der beiden Vorgänger: 0, 1, 1, 2, 3, 5, 8, 13, …

    Schreibe eine Funktion `fib(n)`, die die n-te Fibonacci-Zahl
    **mittels Rekursion** berechnet (fib(0) = 0, fib(1) = 1). Gib
    anschließend die **ersten 20** Fibonacci-Zahlen aus, **eine Zahl pro
    Zeile** (also fib(0) bis fib(19)).

    Erwartete Ausgabe (gekürzt):

        0
        1
        1
        2
        ...
        4181
    """,
    [F("fib(0)", 0), F("fib(1)", 1), F("fib(2)", 1), F("fib(10)", 55), F("fib(19)", 4181),
     P([], exakt=["0", "1", "1", "2", "3", "5", "8", "13", "21", "34", "55", "89", "144", "233",
                  "377", "610", "987", "1597", "2584", "4181"],
       beschreibung="die ersten 20 Fibonacci-Zahlen, eine pro Zeile")],
    """
    def fib(n):
        if n <= 1:              # Rekursionsanker: fib(0) = 0, fib(1) = 1
            return n
        return fib(n - 1) + fib(n - 2)

    for i in range(20):
        print(fib(i))
    """,
    "`fib` ruft sich zweimal selbst auf (mehrfache Rekursion). Der Anker `n <= 1` mit "
    "`return n` deckt beide Startwerte ab. Die Schleife `range(20)` läuft von 0 bis 19, "
    "das sind genau die ersten 20 Zahlen.",
    rekursiv="fib",
    tipps=["Welche zwei Fälle kennst du sofort? Das sind deine Anker.",
           "if n <= 1: return n – sonst return fib(n - 1) + fib(n - 2).",
           "Für die Ausgabe: for i in range(20): print(fib(i))"])

# ── Aufgabe 2.3 ───────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 2.3: Gerade oder ungerade", r"""
    ## Eine einzige Funktion, ohne % und /

    Aus der Vorlesung kennst du `is_even` und `is_odd`, die sich
    gegenseitig aufrufen. Das Blatt verlangt aber **eine einzige
    Funktion**, die sich **selbst** aufruft, ohne `%` und ohne `/`.

    Die Idee: Zieh **2** ab! Eine Zahl ist genau dann gerade, wenn die Zahl
    2 kleiner gerade ist:

        even(6) = even(4) = even(2) = even(0) = True
        even(7) = even(5) = even(3) = even(1) = False

    Dafür brauchst du **zwei** Rekursionsanker: 0 (gerade) und 1
    (ungerade).

    :::achtung Negative Zahlen
    Das Blatt sagt „eine Ganzzahl“. Dazu gehört auch -3. Wer bei -3 immer
    weiter 2 abzieht, landet bei -5, -7 … und nie beim Anker →
    RecursionError. Trick: -3 ist genauso (un)gerade wie 3. Für negative
    Zahlen rufst du die Funktion also mit `-n` auf.
    :::

    :::info Und odd?
    Das Blatt lässt dir die Wahl: „eine der beiden Funktionen even und
    odd“. Auch im Quiz darfst du wählen: Die Tests erkennen, ob du `even`
    oder `odd` geschrieben hast. Für `odd` tauschst du einfach die beiden
    Anker: odd(0) = False, odd(1) = True. Nur beide zusammen gehen nicht –
    es soll ja eine einzige Funktion sein.
    :::
    """)

k.ausgabe("def even(n):\n    if n == 0:\n        return True\n    if n == 1:\n        return False\n"
          "    return even(n - 2)\n\nprint(even(8), even(5))",
          "even(8) → even(6) → even(4) → even(2) → even(0) = True. "
          "even(5) → even(3) → even(1) = False.",
          tipp="Ziehe jeweils 2 ab, bis du bei 0 oder 1 landest.")

k.code(r"""
    ## Übung 4, Aufgabe 2.3 – Gerade oder ungerade

    Schreibe die Funktion `even(n)` **mithilfe von Rekursion**. Sie bekommt
    eine Ganzzahl und gibt `True` zurück, wenn die Zahl gerade ist, sonst
    `False`. Das Blatt lässt dir die Wahl: Du darfst stattdessen auch
    `odd(n)` schreiben (`True` bei ungeraden Zahlen) – die Tests erkennen,
    welche der beiden Funktionen du definiert hast.

    Regeln vom Blatt:
      • weder den Modulo-Operator `%` noch den Divisions-Operator `/`
        (hier auch nicht `//`)
      • alles mit **einer einzigen Funktion** (keine zweite Funktion wie
        is_odd)

    Auch negative Ganzzahlen sollen funktionieren:

        even(10)  →  True
        even(7)   →  False
        even(-3)  →  False
    """,
    [_gerade_test(0), _gerade_test(7), _gerade_test(10), _gerade_test(1),
     _gerade_test(-3), _gerade_test(-4), _gerade_test(501)],
    """
    def even(n):
        if n < 0:              # negative Zahl: gleiche Antwort wie für -n
            return even(-n)
        if n == 0:             # Rekursionsanker 1: 0 ist gerade
            return True
        if n == 1:             # Rekursionsanker 2: 1 ist ungerade
            return False
        return even(n - 2)     # Rekursionsschritt: 2 abziehen
    """,
    "Bei jedem Schritt wird 2 abgezogen. Das ändert nichts daran, ob eine Zahl gerade ist. "
    "Irgendwann landet man bei 0 (gerade) oder 1 (ungerade). Negative Zahlen werden vorher "
    "mit `even(-n)` positiv gemacht, sonst entfernen sie sich immer weiter von den Ankern. "
    "Weil sich `even` nur selbst aufruft, reicht eine einzige Funktion.",
    verboten=["%", "/"],
    rekursiv="even|odd",
    regeln=["funktion:even|odd", "max_funktionen:1"],
    tipps=["Was ändert sich an „gerade/ungerade“, wenn du 2 abziehst?",
           "Zwei Anker: n == 0 → True, n == 1 → False. Schritt: return even(n - 2).",
           "Für negative Zahlen ganz am Anfang: if n < 0: return even(-n)"],
    vorlage="def even(n):\n    ...\n")

# ── Aufgabe 2.4 ───────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 2.4: Pascalsches Dreieck", r"""
    ## Jede Zahl ist die Summe der zwei Zahlen darüber

    Im **Pascalschen Dreieck** steht an beiden Rändern immer eine 1. Jede
    andere Zahl ist die Summe der beiden Zahlen schräg darüber:

        Zeile 0:           1
        Zeile 1:         1   1
        Zeile 2:       1   2   1
        Zeile 3:     1   3   3   1
        Zeile 4:   1   4   6   4   1

    Zeile 0 ist die oberste Zeile. In Zeile n gibt es die Positionen 0
    bis n. Beispiel: pascal(4, 2) = pascal(3, 1) + pascal(3, 2) = 3 + 3 = 6.

    :::analogie 🧱 Bauklötze-Pyramide
    Stell dir eine Pyramide aus Bauklötzen vor. Auf jedem Klotz steht, auf
    wie vielen Wegen man von der Spitze zu ihm kommt, wenn man nur nach
    unten geht. Zu einem Klotz führen zwei Wege: über den linken oder den
    rechten Klotz darüber. Deshalb ist seine Zahl die Summe der beiden. Zu
    den Randklötzen gibt es nur einen einzigen Weg: Sie tragen immer eine 1.
    :::

    Die Ränder sind die **Rekursionsanker** (pos == 0 oder pos == zeile).
    ---
    ## Das ganze Dreieck ausgeben

    Für 2.4.2 gibst du Zeile für Zeile aus. Zwei Hinweise vom Blatt:

      • **Padding** (Einrückung) per String-Multiplikation:
        `'a' * 4` ergibt `'aaaa'`, also ergibt `' ' * 6` sechs Leerzeichen.
      • `print(s, end='')` verhindert den Zeilenumbruch. So kannst du
        mehrere Zahlen in dieselbe Zeile schreiben. Ein leeres `print()`
        beendet die Zeile.

    :::code
    tiefe = 3
    for z in range(tiefe):
        print(' ' * (tiefe - 1 - z), end='')   # Einrückung: oben mehr, unten weniger
        for p in range(z + 1):
            print('* ', end='')                # alles in dieselbe Zeile
        print()                                # Zeilenende
    :::
    """)

k.mc("Was ergibt pascal(5, 1) im Pascalschen Dreieck (Zeile 5, Position 1)?",
     ["5", "1", "10", "6"],
     "Zeile 5 lautet 1, 5, 10, 10, 5, 1. Position 1 ist die zweite Zahl: 5. "
     "Rechnung: pascal(4, 0) + pascal(4, 1) = 1 + 4 = 5.",
     tipp="Schreibe Zeile 5 auf: Jede Zahl ist die Summe der beiden darüber.")

k.mc("Was macht `print('x', end='')`?",
     ["Es gibt x aus, ohne danach in eine neue Zeile zu wechseln",
      "Es gibt gar nichts aus",
      "Es beendet das Programm",
      "Es gibt x und dann eine Leerzeile aus"],
     "Normalerweise hängt print am Ende einen Zeilenumbruch an. Mit end='' wird stattdessen "
     "nichts angehängt, die nächste Ausgabe landet in derselben Zeile.")

k.code(r"""
    ## Übung 4, Aufgabe 2.4.1 – Ein Eintrag im Pascalschen Dreieck

    Schreibe eine Funktion `pascal(zeile, pos)`, die eine Zahl im
    Pascalschen Dreieck berechnet. Der erste Parameter ist die Zeile, der
    zweite die Position in der Zeile. Zeile 0 ist die oberste Zeile. Für
    die n-te Zeile kann `pos` die Werte 0 bis n annehmen.

    Zur Berechnung soll die **Summe zweier Zellen in der darüberliegenden
    Zeile** gebildet werden (also rekursiv).

        pascal(0, 0)  →  1
        pascal(4, 2)  →  6
        pascal(6, 3)  →  20
    """,
    [F("pascal(0, 0)", 1), F("pascal(4, 2)", 6), F("pascal(5, 5)", 1), F("pascal(5, 0)", 1),
     F("pascal(6, 3)", 20), F("pascal(10, 5)", 252)],
    """
    def pascal(zeile, pos):
        if pos == 0 or pos == zeile:      # Rand des Dreiecks: immer 1
            return 1
        return pascal(zeile - 1, pos - 1) + pascal(zeile - 1, pos)
    """,
    "Zwei Anker: der linke Rand (pos == 0) und der rechte Rand (pos == zeile). Sonst "
    "liegen die beiden Zellen darüber in Zeile `zeile - 1` an den Positionen `pos - 1` "
    "und `pos`. Ihre Summe ist das Ergebnis.",
    verboten=["comb", "factorial"],
    rekursiv="pascal",
    tipps=["Wo im Dreieck kennst du die Zahl sofort?",
           "Anker: pos == 0 or pos == zeile → 1.",
           "return pascal(zeile - 1, pos - 1) + pascal(zeile - 1, pos)"],
    vorlage="def pascal(zeile, pos):\n    ...\n")

_DREIECK_VORSPANN = """
import sys as _sys, io as _io, builtins as _bi
_echt = _sys.stdout
_sys.stdout = _io.StringIO()
_bi.input = lambda _p='': _sys.stdin.readline().rstrip('\\n')
"""

_DREIECK_NACHSPANN = """
_text = _sys.stdout.getvalue()
_sys.stdout = _echt
print(_text)
_zahlen = [_z for _z in _text.split('\\n') if _z.strip() and _z.replace(' ', '').isdigit()]
_einzug = [len(_z) - len(_z.lstrip()) for _z in _zahlen]
_ok = len(_zahlen) == 5 and all(_a > _b for _a, _b in zip(_einzug, _einzug[1:]))
print('Dreiecksform: ok' if _ok else 'Dreiecksform fehlt: obere Zeilen brauchen mehr Leerzeichen davor')
"""

k.code(r"""
    ## Übung 4, Aufgabe 2.4.2 – Das ganze Dreieck

    Nun soll ein gesamtes Dreieck generiert werden, dessen **Tiefe als
    Eingabe über die Konsole** angegeben wird. Tiefe = Anzahl der Zeilen.

    Nutze deine Funktion `pascal` aus 2.4.1. Rücke die Zeilen mit
    Leerzeichen ein (Padding per String-Multiplikation), sodass ein
    Dreieck entsteht: **Jede Zeile muss weniger eingerückt sein als die
    Zeile darüber.** Zwischen den Zahlen einer Zeile steht mindestens ein
    Leerzeichen. Tipp vom Blatt: `print(s, end='')`.

    Beispiel mit Eingabe `5`:

                   1
                 1   1
               1   2   1
             1   3   3   1
           1   4   6   4   1
    """,
    [P(["5"], ["1 1", "1 2 1", "1 3 3 1", "1 4 6 4 1"], nicht=["1 5 10"],
       beschreibung="Tiefe 5: fünf Zeilen"),
     P(["1"], ["1"], nicht=["1 1"], beschreibung="Tiefe 1: nur die Spitze"),
     P(["8"], ["1 7 21 35 35 21 7 1"], nicht=["1 8 28"], beschreibung="Tiefe 8"),
     P(["5"], ["Dreiecksform: ok"], vorspann=_DREIECK_VORSPANN, nachspann=_DREIECK_NACHSPANN,
       beschreibung="Zeilen sind als Dreieck eingerückt")],
    """
    def pascal(zeile, pos):
        if pos == 0 or pos == zeile:
            return 1
        return pascal(zeile - 1, pos - 1) + pascal(zeile - 1, pos)

    tiefe = int(input('Tiefe: '))
    for z in range(tiefe):
        print(' ' * (tiefe - 1 - z) * 2, end='')       # Padding per String-Multiplikation
        for p in range(z + 1):
            print(f'{pascal(z, p):4d}', end='')         # end='' verhindert den Zeilenumbruch
        print()
    """,
    "Die äußere Schleife geht die Zeilen 0 bis tiefe - 1 durch. Vor jeder Zeile kommen "
    "`(tiefe - 1 - z) * 2` Leerzeichen: oben viele, unten keine. Die innere Schleife "
    "schreibt mit `end=''` alle Zahlen der Zeile nebeneinander. `{...:4d}` gibt jeder Zahl "
    "4 Zeichen Platz, damit die Spalten gleich breit sind. `print()` beendet die Zeile.",
    rekursiv="pascal",
    tipps=["Zwei Schleifen: außen über die Zeilen, innen über die Positionen der Zeile.",
           "Einrückung vor Zeile z: ' ' * (tiefe - 1 - z). Zahlen mit print(..., end='').",
           "for z in range(tiefe):\n    print(' ' * (tiefe - 1 - z), end='')\n"
           "    for p in range(z + 1):\n        print(pascal(z, p), end=' ')\n    print()"])

# ── Aufgabe 2.5 ───────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 2.5: Liste umdrehen – Schleife gegen Rekursion", r"""
    ## Eine Liste umdrehen, ohne Abkürzung

    Die bequemen Wege sind verboten: kein Slice (`lst[::-1]`) und keine
    `reverse`-Funktion. Du baust die umgedrehte Liste selbst.

    :::analogie 🃏 Spielkarten umdrehen
    Ben hat einen Stapel Karten 1, 2, 3 und will ihn umdrehen.
    **Mit Schleife:** Ben nimmt eine Karte nach der anderen und legt jede
    auf einen neuen Stapel. Die erste Karte landet ganz unten, die letzte
    oben. **Rekursiv:** Ben legt die oberste Karte beiseite, lässt den
    Rest (ein kleineres Problem!) umdrehen und legt die Karte dann unter
    den umgedrehten Rest.
    :::

    :::code
    karten = [1, 2, 3]
    neu = []
    for k in karten:
        neu.insert(0, k)        # vorne einfügen
        print(neu)
    :::

    `liste.insert(0, x)` fügt x ganz vorne ein. `liste.pop(0)` nimmt das
    erste Element heraus und gibt es zurück.
    ---
    ## Rekursiv – und was ein Slice ist

    :::achtung Auch lst[1:] ist ein Slice!
    Die naheliegende Lösung `umdrehen(lst[1:]) + [lst[0]]` benutzt
    einen Slice. Den verbietet das Blatt. Nimm stattdessen eine Kopie
    und `pop(0)`:

        rest = list(lst)        # Kopie, das Original bleibt unverändert
        erstes = rest.pop(0)    # erstes Element herausnehmen
    :::

    So verändert sich das Ergebnis beim Zurückkehren aus der Rekursion für
    [1, 2, 3]:

    | Aufruf | gibt zurück |
    |---|---|
    | umdrehen([]) | [] (Anker) |
    | umdrehen([3]) | [] + [3] = [3] |
    | umdrehen([2, 3]) | [3] + [2] = [3, 2] |
    | umdrehen([1, 2, 3]) | [3, 2] + [1] = [3, 2, 1] |
    """)

k.mc("Welche dieser Zeilen ist in Aufgabe 2.5 NICHT erlaubt?",
     ["rest = lst[1:]", "rest = list(lst)", "erstes = rest.pop(0)", "neu.insert(0, x)"],
     "lst[1:] ist ein Slice (Doppelpunkt in eckigen Klammern) – und Slices verbietet das "
     "Blatt. list(lst) kopiert ohne Slice, pop und insert sind normale Listen-Methoden.")

k.code(r"""
    ## Übung 4, Aufgabe 2.5 (Teil 1) – Liste umdrehen mit Schleife

    Schreibe eine Funktion `umdrehen_schleife(lst)`, die eine **neue**
    Liste mit den Elementen in umgekehrter Reihenfolge zurückgibt. Benutze
    eine **Schleife**. Nicht erlaubt: Slices (z. B. `lst[::-1]`) und
    `reverse` bzw. `reversed`.

        umdrehen_schleife([1, 2, 3])          →  [3, 2, 1]
        umdrehen_schleife(['a', 'b', 'c'])    →  ['c', 'b', 'a']
        umdrehen_schleife([])                 →  []
    """,
    [F("umdrehen_schleife([1, 2, 3])", [3, 2, 1]), F("umdrehen_schleife([])", []),
     F("umdrehen_schleife([7])", [7]),
     F("umdrehen_schleife(list('abcd'))", ["d", "c", "b", "a"]),
     F("umdrehen_schleife([5, [1, 2], 'x'])", ["x", [1, 2], 5])],
    """
    def umdrehen_schleife(lst):
        ergebnis = []
        for element in lst:
            ergebnis.insert(0, element)     # jedes Element vorne einfügen
        return ergebnis
    """,
    "Jedes Element wird vorne in die neue Liste eingefügt. Das erste Element rutscht dadurch "
    "immer weiter nach hinten. Eine andere Lösung läuft mit einem Index von hinten nach "
    "vorne: `for i in range(len(lst) - 1, -1, -1): ergebnis.append(lst[i])`.",
    regeln=["keine_slices", "schleife_in:umdrehen_schleife", "keine_methode:reverse",
            "keine_funktion:reversed"],
    tipps=["Leg eine leere Ergebnisliste an und gehe die Elemente der Reihe nach durch.",
           "Wenn du jedes Element VORNE einfügst, steht das letzte am Ende vorne.",
           "ergebnis.insert(0, element) in der Schleife, am Ende return ergebnis"],
    vorlage="def umdrehen_schleife(lst):\n    ergebnis = []\n    ...\n    return ergebnis\n")

k.code(r"""
    ## Übung 4, Aufgabe 2.5 (Teil 2) – Liste umdrehen mit Rekursion

    Schreibe eine Funktion `umdrehen_rekursiv(lst)`, die dasselbe macht,
    aber **mithilfe von Rekursion**: Die Funktion ruft sich selbst auf und
    benutzt keine Schleife. Nicht erlaubt: Slices (auch nicht `lst[1:]`)
    und `reverse` bzw. `reversed`.

        umdrehen_rekursiv([1, 2, 3])    →  [3, 2, 1]
        umdrehen_rekursiv([])           →  []
    """,
    [F("umdrehen_rekursiv([1, 2, 3])", [3, 2, 1]), F("umdrehen_rekursiv([])", []),
     F("umdrehen_rekursiv([7])", [7]),
     F("umdrehen_rekursiv(list('abcd'))", ["d", "c", "b", "a"]),
     F("umdrehen_rekursiv([5, [1, 2], 'x'])", ["x", [1, 2], 5])],
    """
    def umdrehen_rekursiv(lst):
        if len(lst) == 0:                       # Rekursionsanker: leere Liste
            return []
        rest = list(lst)                        # Kopie, damit das Original bleibt
        erstes = rest.pop(0)                    # erstes Element herausnehmen
        return umdrehen_rekursiv(rest) + [erstes]
    """,
    "Anker: Eine leere Liste ist schon umgedreht. Schritt: Das erste Element wird "
    "herausgenommen, der Rest (eine kürzere Liste) wird rekursiv umgedreht, und das erste "
    "Element kommt ans Ende. Die Kopie mit `list(lst)` sorgt dafür, dass die übergebene "
    "Liste nicht verändert wird. Vergleich mit Teil 1: Die Schleife braucht keinen "
    "Aufrufstapel und klappt auch für sehr lange Listen. Die Rekursion scheitert ab etwa "
    "1000 Elementen am Tiefenlimit.",
    regeln=["keine_slices", "keine_schleifen", "keine_methode:reverse", "keine_funktion:reversed"],
    rekursiv="umdrehen_rekursiv",
    tipps=["Welche Liste ist ganz einfach umzudrehen?",
           "Anker: leere Liste → []. Schritt: erstes Element herausnehmen, Rest rekursiv umdrehen.",
           "rest = list(lst); erstes = rest.pop(0); return umdrehen_rekursiv(rest) + [erstes]"],
    vorlage="def umdrehen_rekursiv(lst):\n    if len(lst) == 0:\n        return []\n    ...\n")

# ── Aufgabe 3 ─────────────────────────────────────────────────────────────
k.erklaerung("Aufgabe 3: ggT und RSA (optional)", r"""
    ## 3.1 Der größte gemeinsame Teiler

    Der **größte gemeinsame Teiler** (ggT) zweier Zahlen ist die größte
    Zahl, durch die beide ohne Rest teilbar sind. Beispiel: ggT(12, 18) = 6.
    Das Blatt gibt eine rekursive Definition vor (euklidischer Algorithmus):

    | Fall | ggT(a, b) |
    |---|---|
    | a = 0 | b |
    | b = 0 | a |
    | sonst | ggT(b, a mod b) |

    `mod` ist in Python der Operator `%`. Hier ist er also erlaubt!

    So läuft die Rekursion für ggT(48, 180):

        ggT(48, 180) → ggT(180, 48) → ggT(48, 36) → ggT(36, 12) → ggT(12, 0) = 12

    :::analogie 🟫 Fliesen legen
    Deniz will einen Raum von 48 × 180 cm mit gleich großen quadratischen
    Fliesen auslegen, ohne eine Fliese zu schneiden. Die größte passende
    Fliese ist 12 × 12 cm, also der ggT. Der Algorithmus schneidet immer
    wieder das größte Quadrat ab, bis nichts übrig bleibt.
    :::
    ---
    ## 3.2 RSA (Bonus)

    Bei RSA (siehe auch Übung 1 und das Bonus-Kapitel „RSA“) braucht man:

    | Zeichen | Bedeutung | Beispiel p = 3, q = 11 |
    |---|---|---|
    | n | Modul: n = p · q | 33 |
    | N | N = φ(n) = (p − 1) · (q − 1) | 20 |
    | e | 1 < e < N mit ggT(e, N) = 1 | 3 |
    | d | 0 < d < N mit e · d mod N = 1 | 7 |

    Öffentlicher Schlüssel: **(e, n)**. Privater Schlüssel: **(d, n)**.
    Verschlüsseln: c = m^e mod n. Entschlüsseln: m = c^d mod n.

    :::info Achtung: n und N sind zwei verschiedene Zahlen!
    Auf Blatt 4 steht „φ(N) = (p − 1)(q − 1)“. Gemeint ist **φ(n)**, also
    die Zahl, die in Übung 1 **N** heißt. Für e und d rechnest du mit
    **N = (p − 1)(q − 1)**, zum Ver- und Entschlüsseln mit **n = p · q**.
    Wer beides verwechselt, bekommt Schlüssel, mit denen die meisten
    Nachrichten falsch entschlüsselt werden.
    :::
    """)

k.ausgabe("def ggT(a, b):\n    if a == 0:\n        return b\n    if b == 0:\n        return a\n"
          "    return ggT(b, a % b)\n\nprint(ggT(12, 18))",
          "ggT(12, 18) → ggT(18, 12) → ggT(12, 6) → ggT(6, 0) = 6.",
          tipp="12 % 18 ist 12, 18 % 12 ist 6, 12 % 6 ist 0.")

k.code(r"""
    ## Übung 4, Aufgabe 3.1 – Größter gemeinsamer Teiler

    Schreibe eine Funktion `ggT(a, b)`, die den größten gemeinsamen Teiler
    zweier Zahlen nach dieser Definition **rekursiv** berechnet:

        ggT(a, b) = b                  falls a = 0
        ggT(a, b) = a                  falls b = 0
        ggT(a, b) = ggT(b, a mod b)    sonst

    Teste dein Programm mit verschiedenen Eingaben, zum Beispiel:

        ggT(12, 18)  →  6
        ggT(17, 5)   →  1
        ggT(0, 5)    →  5

    `math.gcd` ist natürlich nicht erlaubt.
    """,
    [F("ggT(12, 18)", 6), F("ggT(0, 5)", 5), F("ggT(7, 0)", 7), F("ggT(17, 5)", 1),
     F("ggT(48, 180)", 12), F("ggT(0, 0)", 0)],
    """
    def ggT(a, b):
        if a == 0:
            return b
        if b == 0:
            return a
        return ggT(b, a % b)
    """,
    "Die Definition lässt sich eins zu eins übersetzen: zwei Anker (a == 0 und b == 0) und "
    "ein Rekursionsschritt mit `a % b` für „a mod b“. Weil `a % b` immer kleiner als b ist, "
    "werden die Zahlen bei jedem Schritt kleiner, bis eine davon 0 ist.",
    verboten=["gcd"],
    rekursiv="ggT",
    tipps=["Übersetze die drei Zeilen der Definition einzeln in Python.",
           "if a == 0: return b – if b == 0: return a – sonst rekursiver Aufruf.",
           "return ggT(b, a % b)"],
    vorlage="def ggT(a, b):\n    ...\n")

_RSA_EIGENSCHAFTEN = """
import math as _m
_fehler = []
for _p, _q in [(3, 11), (5, 11), (61, 53), (7, 13)]:
    _oeff, _priv = generate_key(_p, _q)
    _e, _n1 = _oeff
    _d, _n2 = _priv
    _N = (_p - 1) * (_q - 1)
    if _n1 != _p * _q or _n2 != _p * _q:
        _fehler.append(f'p={_p}, q={_q}: n muss p * q = {_p * _q} sein')
    elif not (1 < _e < _N and _m.gcd(_e, _N) == 1):
        _fehler.append(f'p={_p}, q={_q}: e={_e} passt nicht (1 < e < N und ggT(e, N) = 1 mit N = {_N})')
    elif not (0 < _d < _N and _e * _d % _N == 1):
        _fehler.append(f'p={_p}, q={_q}: d={_d} passt nicht (0 < d < N und e * d mod N = 1 mit N = {_N})')
print('Schlüssel ok' if not _fehler else 'Fehler: ' + _fehler[0])
"""

k.code(r"""
    ## Übung 4, Aufgabe 3.2.1 – Schlüsselberechnung (Bonus)

    Schreibe eine Funktion `generate_key(p, q)`, die zwei Primzahlen p und
    q entgegennimmt und den öffentlichen und privaten Schlüssel berechnet:

      1. n = p · q und N = φ(n) = (p − 1)(q − 1) bestimmen
      2. ein e mit 1 < e < N finden, für das ggT(e, N) = 1 gilt
      3. ein d mit 0 < d < N finden, für das e · d mod N = 1 gilt
      4. `return ((e, n), (d, n))` (öffentlicher, privater Schlüssel)

    Du darfst deine Funktion `ggT` aus 3.1 mit in den Code schreiben und
    benutzen. Beispiel (mit dem kleinsten passenden e):

        generate_key(3, 11)  →  ((3, 33), (7, 33))

    Getestet werden die Eigenschaften, nicht ein bestimmtes e.
    """,
    [P(nachspann=_RSA_EIGENSCHAFTEN, erwartet=["Schlüssel ok"],
       beschreibung="e und d erfüllen die Bedingungen für mehrere Primzahlpaare"),
     F("generate_key(3, 11)[0][1]", 33), F("generate_key(61, 53)[1][1]", 3233),
     F("type(generate_key(5, 11)) == tuple and len(generate_key(5, 11)) == 2", True)],
    """
    def ggT(a, b):
        if a == 0:
            return b
        if b == 0:
            return a
        return ggT(b, a % b)

    def generate_key(p, q):
        n = p * q                    # Modul
        N = (p - 1) * (q - 1)        # N = phi(n)
        e = 2
        while ggT(e, N) != 1:        # kleinstes e > 1 mit ggT(e, N) = 1
            e += 1
        d = 1
        while e * d % N != 1:        # passendes d mit e * d mod N = 1
            d += 1
        return ((e, n), (d, n))      # (öffentlicher Schlüssel, privater Schlüssel)
    """,
    "Zwei while-Schleifen probieren der Reihe nach: Erst wird e hochgezählt, bis ggT(e, N) = 1 "
    "ist, dann d, bis e · d mod N = 1 ist. Wichtig ist der Unterschied zwischen n = p · q "
    "(für den Schlüssel) und N = (p − 1)(q − 1) (für die Suche nach e und d). Für p = 3, "
    "q = 11 kommen genau die Werte aus Übung 1 heraus: n = 33, N = 20, e = 3, d = 7.",
    verboten=["gcd"],
    tipps=["Berechne zuerst n = p * q und N = (p - 1) * (q - 1).",
           "Für e: bei 2 anfangen und hochzählen, solange ggT(e, N) != 1. Für d genauso mit "
           "e * d % N != 1.",
           "e = 2\nwhile ggT(e, N) != 1:\n    e += 1\nd = 1\nwhile e * d % N != 1:\n    d += 1\n"
           "return ((e, n), (d, n))"])

k.code(r"""
    ## Übung 4, Aufgabe 3.2.2 – Ver- und Entschlüsselung (Bonus)

    Schreibe zwei Funktionen (die Formeln stehen in Übung 1):

      1. `encrypt(m, oeffentlich)`: bekommt die Nachricht m (eine Zahl mit
         0 ≤ m < n) und den öffentlichen Schlüssel `(e, n)` und gibt die
         verschlüsselte Nachricht c = m^e mod n zurück.
      2. `decrypt(c, privat)`: bekommt die verschlüsselte Nachricht und den
         privaten Schlüssel `(d, n)` und gibt m = c^d mod n zurück.

    Beispiel mit den Schlüsseln aus Übung 1:

        encrypt(4, (3, 33))   →  31
        decrypt(31, (7, 33))  →  4
    """,
    [F("encrypt(4, (3, 33))", 31), F("decrypt(31, (7, 33))", 4), F("encrypt(0, (3, 33))", 0),
     F("[decrypt(encrypt(m, (3, 33)), (7, 33)) for m in range(33)]", list(range(33))),
     F("[decrypt(encrypt(m, (7, 3233)), (1783, 3233)) for m in range(0, 3233, 97)]",
       list(range(0, 3233, 97)))],
    """
    def encrypt(m, oeffentlich):
        e, n = oeffentlich           # Tupel entpacken
        return pow(m, e, n)          # dasselbe wie m ** e % n, nur schneller

    def decrypt(c, privat):
        d, n = privat
        return pow(c, d, n)
    """,
    "Die Schlüssel sind Tupel. Mit `e, n = oeffentlich` packst du sie aus. `pow(m, e, n)` "
    "rechnet `m ** e % n`, ist aber bei großen Zahlen viel schneller. Der letzte Test prüft "
    "die „Rundreise“: Jede verschlüsselte Zahl kommt beim Entschlüsseln wieder heraus.",
    tipps=["Ein Schlüssel ist ein Tupel aus zwei Zahlen. Pack es zuerst aus.",
           "Verschlüsseln: m ** e % n. Entschlüsseln: c ** d % n.",
           "e, n = oeffentlich\nreturn pow(m, e, n)"],
    vorlage="def encrypt(m, oeffentlich):\n    ...\n\ndef decrypt(c, privat):\n    ...\n")

k.zusammenfassung(r"""
    ## Übungsblatt 4 auf einen Blick

    | Aufgabe | Kern der Lösung |
    |---|---|
    | 1 Pfannkuchen | `faktor = menge / zutaten[zutat][0]`, dann jede Menge mal Faktor |
    | 2.1 Fakultät | Anker `n == 0 → 1`, Schritt `n * fakultaet(n - 1)`, keine Schleife |
    | 2.2 Fibonacci | Anker `n <= 1 → n`, Schritt `fib(n - 1) + fib(n - 2)`, `range(20)` |
    | 2.3 gerade | eine Funktion, Anker 0 und 1, Schritt `even(n - 2)`, negativ: `even(-n)` |
    | 2.4 Pascal | Rand → 1, sonst Summe der zwei Zellen darüber; Padding mit `' ' * k` |
    | 2.5 umdrehen | Schleife mit `insert(0, x)`; rekursiv mit Kopie und `pop(0)`, kein Slice |
    | 3.1 ggT | `ggT(b, a % b)` bis eine Zahl 0 ist |
    | 3.2 RSA | n = p · q, N = (p − 1)(q − 1), e und d über N, rechnen mod n |

    !! „Ohne Schleifen“ heißt: Die Wiederholung entsteht durch den
    !! Selbstaufruf der Funktion.

        def ggT(a, b):
            if a == 0:
                return b
            if b == 0:
                return a
            return ggT(b, a % b)
    """)
