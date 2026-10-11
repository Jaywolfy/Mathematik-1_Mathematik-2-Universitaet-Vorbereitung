# -*- coding: utf-8 -*-
"""Kapitel: Guter Code & Sprachensalat (Vorlesung 4, Folien 33–44)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="guter_code",
    titel="Guter Code & Sprachensalat",
    beschreibung="Allgemeiner programmieren, Effizienz und andere Programmier-Paradigmen",
    quelle="Vorlesung 4",
    teil="tag4",
    icon="✨")

k.lernziele([
    "Ich kann doppelten Code durch eine allgemeinere Funktion mit Parametern ersetzen",
    "Ich kann vier_in_folge erklären und mit Randprüfung sicher machen",
    "Ich kann zwei einfache Effizienz-Regeln aus der Vorlesung anwenden",
    "Ich kann funktionale, stack-basierte und andere Sprachen grob einordnen",
])

k.erklaerung("Guter Code", r"""
    ## Allgemein statt tausend Sonderfälle

    Probleme kann man oft **abstrakter** betrachten, um sie allgemeiner
    (und einfacher) zu lösen und weniger Code zu duplizieren. Wer gerade
    erst programmieren lernt, schreibt leider oft tausende Bedingungen statt
    einer allgemeinen Lösung (Folie 34).

    :::analogie 🍰 Ein Rezept für alle Obstkuchen
    Anna backt Apfelkuchen, Kirschkuchen und Pflaumenkuchen. Sie könnte
    drei Rezepte aufschreiben, die zu 95 % gleich sind. Findet sie einen
    Fehler in der Backzeit, muss sie ihn dreimal verbessern und vergisst
    bestimmt eins. Klüger: **ein** Rezept „Obstkuchen“, bei dem das Obst
    eine Zutat ist, die man einsetzt. In Python ist das Rezept eine
    Funktion und das Obst ein **Parameter**.
    :::

    :::vergleich ✘ Kopierter Code | ✔ Eine Funktion
    Dreimal fast dasselbe:
        print("Kaffee:", round(2.00 * 1.19, 2))
        print("Kuchen:", round(3.00 * 1.19, 2))
        print("Saft:", round(1.80 * 1.19, 2))
    |||
    Die Rechnung steht nur einmal da:
        def brutto(netto):
            return round(netto * 1.19, 2)

        print("Kaffee:", brutto(2.00))
        print("Kuchen:", brutto(3.00))
        print("Saft:", brutto(1.80))
    :::

    !! Aber: Nicht ZU „klug“ designen – sonst verstehst du es später
    !! selbst nicht mehr!
    ---
    ## Beispiel: Vier gewinnt (Folien 35 und 36)

    Das Spielfeld `grid` ist eine Liste von Zeilen: `grid[y][x]` ist das
    Feld in Zeile y und Spalte x.

    :::vergleich Verbose: zwei fast gleiche Funktionen | Kompakt: eine Funktion mit Richtung
    Nur die Indizes unterscheiden sich:
        def vier_waagerecht(x, y):
            entry = grid[y][x]
            for i in range(1, 4):
                if grid[y][x+i] != entry:
                    return False
            return True

        def vier_senkrecht(x, y):
            entry = grid[y][x]
            for i in range(1, 4):
                if grid[y+i][x] != entry:
                    return False
            return True
    |||
    xo = Schritt nach rechts, yo = Schritt nach unten:
        def vier_in_folge(x, y, xo, yo):
            entry = grid[y][x]
            for i in range(1, 4):
                if grid[y+i*yo][x+i*xo] != entry:
                    return False
            return True
    :::

    | Richtung | Aufruf |
    |---|---|
    | waagerecht | `vier_in_folge(x, y, 1, 0)` |
    | senkrecht | `vier_in_folge(x, y, 0, 1)` |
    | Diagonale nach rechts unten | `vier_in_folge(x, y, 1, 1)` |
    | Diagonale nach rechts oben | `vier_in_folge(x, y, 1, -1)` |

    Mit zwei zusätzlichen Parametern braucht man nur noch eine Funktion,
    und die Diagonalen kann man auch prüfen.
    """)

k.ausgabe('''grid = [
    [1, 1, 1, 1],
    [2, 0, 0, 0],
    [2, 0, 0, 0],
    [2, 0, 0, 0],
]

def vier_in_folge(x, y, xo, yo):
    entry = grid[y][x]
    for i in range(1, 4):
        if grid[y + i * yo][x + i * xo] != entry:
            return False
    return True

print(vier_in_folge(0, 0, 1, 0))
print(vier_in_folge(0, 0, 0, 1))''',
          "(0, 0, 1, 0) prüft waagerecht in Zeile 0: 1, 1, 1, 1 → True. (0, 0, 0, 1) prüft "
          "senkrecht in Spalte 0: 1, 2, ... → schon das zweite passt nicht → False.",
          tipp="xo = Schritt nach rechts, yo = Schritt nach unten.")

k.mc("Welche Richtung (xo, yo) prüft bei vier_in_folge eine DIAGONALE?",
     ["(1, 1)", "(1, 0)", "(0, 1)", "(0, 0)"],
     "Bei jedem Schritt eins nach rechts UND eins nach unten → diagonal. Die andere Diagonale "
     "(nach rechts oben) ist (1, -1).")

k.mc("Warum ist vier_in_folge(x, y, xo, yo) besser als zwei getrennte Funktionen?",
     ["Kein doppelter Code, und Diagonalen gibt's gratis dazu",
      "Weil Funktionen mit 4 Parametern immer schneller sind",
      "Weil Python nur eine Funktion pro Datei erlaubt",
      "Ist es nicht – zwei Funktionen sind immer besser"],
     "Die Logik ist bis auf die Richtung identisch. Mit Parametern für die Richtung "
     "braucht man nur eine Funktion. Einen Fehler muss man dann auch nur an einer Stelle "
     "verbessern.")

k.erklaerung("Achtung am Spielfeldrand", r"""
    ## Was passiert am Rand?

    Die Version von der Folie prüft **nicht**, ob die Felder überhaupt im
    Spielfeld liegen. Das führt zu zwei Problemen:

    1. **Rechts oder unten über den Rand**: `grid[y][x + i]` gibt es nicht
       → `IndexError: list index out of range`.
    2. **Links oder oben über den Rand** (z. B. Richtung `(-1, 0)` oder
       `(1, -1)`): Der Index wird negativ. Python wirft dann **keinen**
       Fehler, denn `grid[0][-1]` ist einfach das **letzte** Element! Die
       Funktion schaut „um die Ecke“ auf die andere Seite des Spielfelds und
       liefert still ein falsches Ergebnis.

    :::code
    grid = [[1, 1, 0, 1, 1]]

    def vier_in_folge(x, y, xo, yo):
        entry = grid[y][x]
        for i in range(1, 4):
            if grid[y + i * yo][x + i * xo] != entry:
                return False
        return True

    # Von Spalte 1 nach links: Es gibt nur EIN Feld links davon ...
    print(vier_in_folge(1, 0, -1, 0))   # ... trotzdem True!
    :::

    :::achtung Typischer Fehler: negative Indizes am Rand
    Ein `IndexError` ist ärgerlich, aber man bemerkt ihn wenigstens. Ein
    still falsches Ergebnis durch einen negativen Index ist schlimmer. Prüfe
    vor jedem Zugriff, ob die Position im Feld liegt:

        if not (0 <= ny < len(grid) and 0 <= nx < len(grid[ny])):
            return False
    :::
    """)

k.ausgabe("grid = [[1, 1, 0, 1, 1]]\nprint(grid[0][-1], grid[0][-2])",
          "Negative Indizes zählen von hinten: grid[0][-1] ist das letzte Feld (1), grid[0][-2] "
          "das vorletzte (1). Genau deshalb „sieht“ vier_in_folge ohne Randprüfung links neben "
          "Spalte 0 noch Steine.",
          tipp="Index -1 ist das letzte Element einer Liste.")

k.mc("grid hat 5 Spalten (Index 0 bis 4). Was passiert bei vier_in_folge(2, 0, 1, 0) mit der "
     "Version von der Folie, wenn die ersten Felder gleich sind?",
     ["IndexError, weil Spalte 5 nicht existiert",
      "False, weil Python den Rand automatisch erkennt",
      "Python springt zurück auf Spalte 0",
      "True, weil fehlende Felder als gleich zählen"],
     "Geprüft werden x = 3, 4 und 5. Spalte 5 gibt es nicht, also IndexError. Ohne Randprüfung "
     "erkennt Python den Rand nicht von selbst.")

k.wf("Bei vier_in_folge(1, 0, -1, 0) ohne Randprüfung gibt Python einen IndexError aus.", False,
     "Nein! x wird 0, dann -1, dann -2. Negative Indizes sind in Python erlaubt und zählen von "
     "hinten. Es gibt also keinen Fehler, sondern ein womöglich falsches Ergebnis.")

k.erklaerung("(Mangelnde) Effizienz", r"""
    ## Nicht unnötig doppelt arbeiten

    Im Vorkurs und im ersten Semester ist Geschwindigkeit noch nicht so
    wichtig. Trotzdem sollte man sich beim Grund-Design Gedanken machen.
    (Windows, Discord, … sind laut Folie 37 nicht sonderlich effizient –
    Rechner könnten heute eigentlich viel schneller sein.)

    :::analogie 📚 Das Buch im Regal
    Deniz will aus einem Buch jede Zeile abschreiben. Deniz holt das Buch
    aus dem Regal, sucht Zeile 1, schreibt sie ab, stellt das Buch zurück.
    Dann holt Deniz es wieder, sucht Zeile 2, … So dauert es ewig. Klüger:
    Buch **einmal** holen, alle Zeilen der Reihe nach abschreiben, Buch
    zurückstellen. Genauso solltest du eine Datei einmal öffnen und
    zeilenweise durchgehen, statt sie für jede Zeile neu zu öffnen.
    :::

    Zweite Regel: Ein Funktionsaufruf, der in einer Schleife **immer
    dasselbe** Ergebnis liefert, gehört **vor** die Schleife.

    :::code
    aufrufe = 0
    def mwst_satz():          # stell dir vor, das dauert lange
        global aufrufe
        aufrufe += 1
        return 0.19

    preise = [2.0, 3.0, 1.8, 4.5]
    satz = mwst_satz()        # EINMAL vor der Schleife
    for p in preise:
        print(round(p * (1 + satz), 2))
    print("mwst_satz wurde", aufrufe, "Mal aufgerufen")
    :::

    Stünde `mwst_satz()` in der Schleife, würde es viermal aufgerufen,
    obwohl jedes Mal 0.19 herauskommt.
    """)

k.mc("Welcher Tipp zur Effizienz stammt aus der Vorlesung?",
     ["Funktionsaufrufe, die in einer Schleife immer dasselbe liefern, vor die Schleife ziehen",
      "Für jede Zeile einer Datei die Datei neu öffnen",
      "Möglichst viele globale Variablen verwenden",
      "Alle Schleifen durch Rekursion ersetzen"],
     "Was sich nicht ändert, muss man nicht 1000-mal neu berechnen.")

k.mc("Du willst eine Datei mit 1000 Zeilen zeilenweise bearbeiten. Was ist laut Vorlesung "
     "ungeschickt?",
     ["Für jede Zeile die Datei öffnen, die n-te Zeile lesen und wieder schließen",
      "Die Datei einmal öffnen und mit einer Schleife alle Zeilen durchgehen",
      "Die Datei mit with open(...) öffnen",
      "Die Zeilen mit .strip() säubern"],
     "1000-mal öffnen und bis zur n-ten Zeile suchen ist viel Arbeit. Einmal öffnen und der "
     "Reihe nach lesen reicht.")

k.erklaerung("Sprachensalat – andere Programmier-Paradigmen", r"""
    ## Nicht jede Sprache tickt wie Python

    Ein **Paradigma** ist eine grundsätzliche Art, Programme zu denken und
    aufzuschreiben. Vorlesung 4 zeigt ein paar ungewöhnliche Beispiele.

    **Funktionale Sprachen** (z. B. Haskell – benannt nach Haskell Brooks
    Curry)
      • Verkettung von Funktionen ist die Grundlage für komplexe Programme.
      • Es gibt keine Variablen, nur Konstanten.
      • Funktionen sind wie Werte: Sie können Parameter und Rückgabewerte sein.
      • Kombinatoren verketten Funktionen weiter.
      • Funktionen kann man oft nur teilweise („partiell“) anwenden:
        **Currying**.
    ---
    ## Stack-basierte Sprachen: Forth

    „Forth was discovered, not invented“ (Charles H. Moore).
      • Grundprinzip: Es gibt **einen oder mehrere Stacks** (Stapel) für
        Daten, wie ein Tellerstapel: oben drauflegen, oben wegnehmen.
      • Operatoren arbeiten nur auf den Stacks: Sie nehmen ihre Parameter
        vom Stapel und legen das Ergebnis wieder darauf.
      • Funktionen sind Adressen (also Zahlen), die man auch auf den Stack
        legen kann.

    So rechnet Forth `2 3 + 4 *` (also (2 + 3) · 4):

    :::visual ablauf
    {"schritte": [{"icon": "2️⃣", "text": "2 → Stapel: 2"},
                  {"icon": "3️⃣", "text": "3 → Stapel: 2 3"},
                  {"icon": "➕", "text": "+ nimmt 2 und 3, legt 5 → Stapel: 5"},
                  {"icon": "4️⃣", "text": "4 → Stapel: 5 4"},
                  {"icon": "✖️", "text": "* nimmt 5 und 4, legt 20 → Stapel: 20"}]}
    :::

    :::info Augenzwinkern auf der Folie
    Auf Folie 40 steht auch: „so gut wie jede CPU ist/beinhaltet eine
    Stack-Maschine“ und „Es gibt keine Arrays, Schleifen, Listen …, nur den
    STACK STACK STACK“. Das ist bewusst überspitzt (Forth kennt durchaus
    Schleifen). Merke dir das Grundprinzip: Daten liegen auf Stapeln.
    :::
    ---
    ## Noch verrückter

    **APL** (A Programming Language)
      • Alles basiert auf N-dimensionalen Arrays – auch eine Zahl ist nur
        ein 0D-Array.
      • Operatoren kombinieren Arrays zu anderen Arrays.
      • Besteht im Wesentlichen aus einzelnen Symbolen. Conways „Game of
        Life“ passt in eine einzige Zeile.

    **AsciiDots** – 2D-Programmierung
      • Code muss nicht zeilenbasiert sein: „Punkte“ wandern über Linien
        aus ASCII-Zeichen.
      • Schleifen sind Kreise, es gibt keine expliziten Variablen.

    **Piet** – Programme sind Bilder
      • Besteht aus 20 Farben (18 Farben + Schwarz und Weiß).
      • Schon einfache Probleme sind wie ein Puzzle.
      • Am Ende hat man ein schönes Bild.

    !! Key Take-Away: Es gibt verschiedene Paradigmen, die Probleme
    !! unterschiedlich gut lösen. Sie schließen sich nicht aus, sondern
    !! leben friedlich zusammen (Python kann z. B. auch „funktional“).
    """)

k.mc("Was ist typisch für funktionale Sprachen wie Haskell?",
     ["Es gibt keine Variablen, nur Konstanten – und Funktionen sind wie Werte",
      "Alles ist ein Bild aus 20 Farben",
      "Alle Daten liegen auf Stapeln",
      "Alles ist ein N-dimensionales Array"],
     "Funktional: Verkettung von Funktionen, Konstanten, Funktionen als Parameter/Rückgabewerte, Currying.")

k.mc("Welche Sprache ist stack-basiert?",
     ["Forth", "Piet", "APL", "Haskell"],
     "Forth legt Daten auf einen oder mehrere Stapel (Stacks). Operatoren nehmen ihre Werte "
     "vom Stapel und legen das Ergebnis wieder darauf.")

k.text("Forth rechnet   2 3 + 4 *  . Welche Zahl liegt am Ende auf dem Stapel?",
       ["20"],
       "2 und 3 kommen auf den Stapel, + macht daraus 5. Dann kommt 4 dazu, * macht aus 5 und 4 "
       "die 20.",
       tipp="Jeder Operator nimmt die zwei obersten Zahlen vom Stapel.")

k.mc("In welcher Sprache sind Programme Bilder aus Farben?",
     ["Piet", "AsciiDots", "Forth", "Java"],
     "Piet besteht aus 20 Farben – am Ende hat man ein schönes Bild.")

k.mc("Was bedeutet 'Currying'?",
     ["Eine Funktion nur teilweise (partiell) anwenden",
      "Eine Funktion besonders scharf würzen",
      "Eine Schleife abbrechen",
      "Code in Farben darstellen"],
     "Benannt nach Haskell Brooks Curry: Man gibt einer Funktion erst einen Teil ihrer "
     "Parameter und bekommt eine neue Funktion für den Rest.")

k.wf("Programmier-Paradigmen schließen sich gegenseitig aus.", False,
     "Sie leben friedlich zusammen – viele Sprachen (auch Python) vereinen mehrere Paradigmen.")

# ── Praxisteil ───────────────────────────────────────────────────────────
k.luecke("Ergänze die Liste aller vier Richtungen, die man bei Vier gewinnt prüfen muss: "
         "waagerecht, senkrecht, Diagonale nach rechts unten und Diagonale nach rechts oben "
         "(x wächst nach rechts, y wächst nach unten).",
         """
         richtungen = [(1, 0), (0, 1), (1, 1), ___]
         for xo, yo in richtungen:
             print(xo, yo)
         """,
         [["(1, -1)", "(1,-1)", "(-1, 1)", "(-1,1)"]],
         "Rechts oben heißt: x eins mehr, y eins weniger, also (1, -1). (-1, 1) prüft dieselbe "
         "Linie in Gegenrichtung und ist auch richtig.",
         tipp="Nach oben bedeutet: y wird kleiner.")

_KASSE_VORLAGE = ('print("Kaffee:", round(2.00 * 1.19, 2), "Euro")\n'
                  'print("Kuchen:", round(3.00 * 1.19, 2), "Euro")\n'
                  'print("Saft:", round(1.80 * 1.19, 2), "Euro")\n')

k.code(r"""
    ## Refactoring: Kassenbon

    Der Code im Editor rechnet für drei Netto-Preise den Preis mit 19 %
    Mehrwertsteuer aus. Die Rechnung steht dreimal da. Mach ihn lesbarer:

      1. Schreibe eine Funktion `brutto(netto)`, die
         `round(netto * 1.19, 2)` zurückgibt.
      2. Benutze sie in den drei print-Zeilen.

    Die Ausgabe muss **genau gleich** bleiben:

        Kaffee: 2.38 Euro
        Kuchen: 3.57 Euro
        Saft: 2.14 Euro
    """,
    [P([], exakt=["Kaffee: 2.38 Euro", "Kuchen: 3.57 Euro", "Saft: 2.14 Euro"],
       beschreibung="gleiche Ausgabe wie vorher"),
     F("brutto(10)", 11.9), F("brutto(0)", 0), F("brutto(2.00)", 2.38)],
    """
    def brutto(netto):
        return round(netto * 1.19, 2)

    print("Kaffee:", brutto(2.00), "Euro")
    print("Kuchen:", brutto(3.00), "Euro")
    print("Saft:", brutto(1.80), "Euro")
    """,
    "Die Rechnung steht jetzt an genau einer Stelle. Ändert sich der Steuersatz, musst du nur "
    "die Funktion anpassen. Das Verhalten (die Ausgabe) ist gleich geblieben. Genau das "
    "bedeutet Refactoring: Code verbessern, ohne zu ändern, was er tut.",
    pflicht=["def brutto", "return"],
    tipps=["Welcher Teil wiederholt sich in allen drei Zeilen?",
           "def brutto(netto):\n    return round(netto * 1.19, 2)",
           "print(\"Kaffee:\", brutto(2.00), \"Euro\")  – und die anderen beiden genauso"],
    vorlage=_KASSE_VORLAGE)

_WOCHENTAG_VORLAGE = '''def wochentag(nr):
    if nr == 1:
        return "Montag"
    elif nr == 2:
        return "Dienstag"
    elif nr == 3:
        return "Mittwoch"
    elif nr == 4:
        return "Donnerstag"
    elif nr == 5:
        return "Freitag"
    elif nr == 6:
        return "Samstag"
    elif nr == 7:
        return "Sonntag"
'''

k.code(r"""
    ## Refactoring: Allgemein statt tausend Bedingungen

    Die Funktion im Editor hat sieben fast gleiche Bedingungen. Schreibe
    `wochentag(nr)` so um, dass sie **ohne if/elif** auskommt: Lege die
    Namen in eine Liste und hole den richtigen Eintrag über den Index.
    Das Verhalten für 1 bis 7 bleibt gleich:

        wochentag(1)  →  "Montag"
        wochentag(7)  →  "Sonntag"
    """,
    [F("wochentag(1)", "Montag"), F("wochentag(3)", "Mittwoch"), F("wochentag(7)", "Sonntag"),
     F("[wochentag(i) for i in range(1, 8)]",
       ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"])],
    """
    def wochentag(nr):
        tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag",
                "Freitag", "Samstag", "Sonntag"]
        return tage[nr - 1]          # Liste beginnt bei Index 0
    """,
    "Statt sieben Bedingungen steckt das Wissen jetzt in einer Liste. Weil Listen bei 0 "
    "anfangen zu zählen, gehört Tag 1 zu Index 0, also `tage[nr - 1]`. Das ist genau die "
    "Idee von Folie 34: allgemeiner formuliert statt tausender Bedingungen.",
    verboten=["if", "elif"],
    tipps=["Was haben alle sieben Bedingungen gemeinsam? Nur der Name ändert sich.",
           "Lege eine Liste mit den sieben Namen an.",
           "return tage[nr - 1] – denn Montag steht bei Index 0."],
    vorlage=_WOCHENTAG_VORLAGE)

_GRID = """
G = [
    [1, 1, 0, 1, 1],
    [0, 2, 2, 2, 2],
    [0, 0, 2, 0, 0],
    [0, 2, 0, 2, 0],
    [2, 0, 0, 0, 2],
]
"""

k.code(r"""
    ## vier_in_folge mit Randprüfung

    Schreibe `vier_in_folge(grid, x, y, xo, yo)` wie auf Folie 36, aber
    **sicher am Rand**: Liegt eines der drei weiteren Felder außerhalb des
    Spielfelds, gibt die Funktion `False` zurück (kein IndexError und kein
    „Um-die-Ecke-Schauen“ mit negativen Indizes).

    Getestet wird mit diesem Spielfeld `G`:

        [1, 1, 0, 1, 1],
        [0, 2, 2, 2, 2],
        [0, 0, 2, 0, 0],
        [0, 2, 0, 2, 0],
        [2, 0, 0, 0, 2],

        vier_in_folge(G, 1, 1, 1, 0)    →  True    (Zeile 1 waagerecht)
        vier_in_folge(G, 0, 4, 1, -1)   →  True    (Diagonale nach rechts oben)
        vier_in_folge(G, 2, 1, 1, 0)    →  False   (rechter Rand!)
        vier_in_folge(G, 1, 0, -1, 0)   →  False   (linker Rand!)
    """,
    [F("vier_in_folge(G, 1, 1, 1, 0)", True, vorspann=_GRID),
     F("vier_in_folge(G, 1, 1, 1, 1)", True, vorspann=_GRID),
     F("vier_in_folge(G, 0, 4, 1, -1)", True, vorspann=_GRID),
     F("vier_in_folge(G, 0, 1, 0, 1)", False, vorspann=_GRID),
     F("vier_in_folge(G, 2, 1, 1, 0)", False, vorspann=_GRID),
     F("vier_in_folge(G, 3, 3, 1, 1)", False, vorspann=_GRID),
     F("vier_in_folge(G, 1, 0, -1, 0)", False, vorspann=_GRID)],
    """
    def vier_in_folge(grid, x, y, xo, yo):
        entry = grid[y][x]
        for i in range(1, 4):
            nx = x + i * xo
            ny = y + i * yo
            if not (0 <= ny < len(grid) and 0 <= nx < len(grid[ny])):
                return False                 # außerhalb des Spielfelds
            if grid[ny][nx] != entry:
                return False
        return True
    """,
    "Vor jedem Zugriff wird die neue Position (nx, ny) geprüft. Liegt sie außerhalb, kann es "
    "keine vier in Folge geben, also `False`. Wichtig ist auch die Prüfung `0 <= ...`: Ohne "
    "sie wären negative Indizes erlaubt und Python würde auf der anderen Seite des Felds "
    "weiterzählen.",
    tipps=["Berechne für jedes i die neue Position nx, ny, bevor du auf grid zugreifst.",
           "Gültig ist eine Position, wenn 0 <= ny < len(grid) und 0 <= nx < len(grid[ny]).",
           "if not (0 <= ny < len(grid) and 0 <= nx < len(grid[ny])):\n    return False"],
    vorlage="def vier_in_folge(grid, x, y, xo, yo):\n    entry = grid[y][x]\n"
            "    for i in range(1, 4):\n        if grid[y + i * yo][x + i * xo] != entry:\n"
            "            return False\n    return True\n")

k.zusammenfassung(r"""
    ## Guter Code auf einen Blick

      • **Allgemein statt Sonderfälle**: Wiederholten Code in eine Funktion
        mit Parametern packen (Obstkuchen-Rezept, `vier_in_folge`).
      • Aber nicht zu „klug“: Code muss verständlich bleiben.
      • **Randprüfung** bei Spielfeldern: `0 <= ny < len(grid)` und
        `0 <= nx < len(grid[ny])` – negative Indizes zählen sonst von hinten!
      • **Effizienz**: Gleichbleibende Aufrufe vor die Schleife ziehen; Dateien
        einmal öffnen und zeilenweise durchgehen.
      • **Refactoring** = Code verbessern, ohne das Verhalten zu ändern.

    | Paradigma / Sprache | Grundidee |
    |---|---|
    | funktional (Haskell) | Funktionen verketten, nur Konstanten, Currying |
    | stack-basiert (Forth) | Daten auf einem oder mehreren Stapeln |
    | APL | alles sind N-dimensionale Arrays |
    | AsciiDots | 2D-Programme, Punkte wandern über Linien |
    | Piet | Programme sind Bilder aus 20 Farben |

    !! Paradigmen schließen sich nicht aus – sie leben friedlich zusammen.
    """)
