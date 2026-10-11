# -*- coding: utf-8 -*-
"""Challenge, Etappe 1: Othello – Spielregeln und Spielfeld (Liste von Listen)."""
from ..engine import neues_kapitel, P, F

# ──────────────────────────────────────────────────────────────────────────
#  Bausteine der Musterlösung (werden in späteren Etappen als Vorlage und
#  im Test-Vorspann mitgegeben, damit niemand von vorn anfangen muss)
# ──────────────────────────────────────────────────────────────────────────

CODE_KONSTANTEN = """\
LEER, SCHWARZ, WEISS = '.', 'S', 'W'
"""

CODE_GEGNER = """\
def gegner(spieler):
    if spieler == SCHWARZ:
        return WEISS
    return SCHWARZ
"""

CODE_IM_FELD = """\
def im_feld(x, y):
    return 0 <= x < 8 and 0 <= y < 8
"""

CODE_NEUES_BRETT = """\
def neues_brett():
    brett = []
    for y in range(8):
        brett.append([LEER] * 8)
    brett[3][3] = WEISS
    brett[3][4] = SCHWARZ
    brett[4][3] = SCHWARZ
    brett[4][4] = WEISS
    return brett
"""

CODE_BRETT_ZEIGEN = """\
def brett_zeigen(brett):
    print('  1 2 3 4 5 6 7 8')
    for y in range(8):
        print(y + 1, ' '.join(brett[y]))
"""

# Alles aus Etappe 1 zusammen (Vorlage/Vorspann für Etappe 2–4)
CODE_ETAPPE1 = "\n\n".join([CODE_KONSTANTEN, CODE_GEGNER, CODE_IM_FELD,
                            CODE_NEUES_BRETT, CODE_BRETT_ZEIGEN])

TESTHILFE = """\
def brett_aus(*zeilen):
    # Baut ein Brett aus 8 Texten mit je 8 Zeichen ('.', 'S' oder 'W').
    return [list(zeile) for zeile in zeilen]
"""


k = neues_kapitel(
    slug="othello_spielfeld",
    titel="Challenge 1 – Othello: Regeln & Spielfeld",
    beschreibung="Die Spielregeln, das Brett als Liste von Listen, Koordinaten und die Ausgabe",
    quelle="Challenge-Handout",
    teil="challenge",
    icon="⚫")

k.lernziele([
    "Ich kann die Regeln von Othello erklären: Zug, Umdrehen, Passen, Spielende",
    "Ich kann ein 8×8-Spielfeld als Liste von Listen anlegen und mit brett[y][x] auf ein Feld zugreifen",
    "Ich kann erklären, warum [[LEER] * 8] * 8 kein brauchbares Brett ist",
    "Ich kann prüfen, ob eine Koordinate auf dem Brett liegt",
    "Ich kann das Brett mit Zeilen- und Spaltennummern auf der Konsole ausgeben",
])

# ── Erklärung 1: Die Challenge und die Spielregeln ────────────────────────
k.erklaerung("Die Programmierchallenge: Othello", r"""
    ## Was ist die Challenge?

    Jedes Jahr gibt es im Vorkurs eine kleine **Programmierchallenge**. Du
    wendest das Gelernte endlich in etwas Größerem als 10 Zeilen an. Laut
    Handout habt ihr in den ersten drei Tagen genug gelernt, um so ein Spiel
    zu programmieren. Früher waren es Tic-Tac-Toe, 2048 oder Vier gewinnt.
    Dieses Jahr ist es **Reversi / Othello**.

    Die Aufgabe laut Handout:
      • Programmiert das Spiel "Othello" als **Konsolenprogramm**.
      • Das Spielfeld hat die Größe 8 × 8 (Breite × Höhe).
      • Die Interaktion läuft über die Konsole mit `input()` und `print()`.
      • Hinweis: Mit `.isnumeric()` könnt ihr prüfen, ob ein String zu einer
        Zahl umgewandelt werden kann.
      • Am Ende soll ausgegeben werden, welcher Spieler gewonnen hat bzw. ob
        keiner gewonnen hat.

    Die Challenge richtet sich vor allem an alle, die am Montag kaum oder
    keine Vorerfahrung hatten. Alle anderen dürfen natürlich auch mitmachen.
    Abgegeben wird über **Moodle**, Abschnitt "Programmierchallenge". Laut
    Folie bis Sonntagabend – den genauen Termin findest du im Moodle.

    !! Traut euch und gebt etwas ab, es lohnt sich! ("Unser Code war damals
    !! auch mehr Spaghetti als korrekt.")
    ---
    ## So arbeitest du hier

    In vier Etappen baust du das Spiel Schritt für Schritt selbst:

    | Etappe | Inhalt |
    |---|---|
    | 1 | Regeln, Spielfeld anlegen und anzeigen |
    | 2 | Züge prüfen und Steine umdrehen |
    | 3 | Eingaben prüfen, Passen, Spielende, Gewinner |
    | 4 | Alles zusammensetzen: das spielbare Spiel |

    Jede Etappe besteht aus kleinen **Hilfsfunktionen**. Eine Hilfsfunktion
    erledigt genau eine kleine Teilaufgabe, zum Beispiel "Liegt dieses Feld
    auf dem Brett?". Jede Funktion wird automatisch getestet. In späteren
    Aufgaben bekommst du deine bisherigen Funktionen fertig mitgeliefert.

    :::info Die Funktionsnamen sind ein Vorschlag
    Das Handout schreibt keine Funktionsnamen und keinen Aufbau vor. Hier
    gibt es Namen wie `neues_brett` oder `im_feld`, damit die Tests
    funktionieren. In deiner eigenen Abgabe darfst du alles anders machen.
    :::

    :::achtung Deine Abgabe soll DEIN Code sein
    Die Musterlösungen hier helfen dir beim Lernen. Das Vorkurs-Team möchte
    aber sehen, wie Leute ohne Vorerfahrung programmieren. Reiche deshalb deinen
    eigenen Code ein, auch wenn er nicht perfekt ist.
    :::
    ---
    ## Die Spielregeln

    Die Regeln stehen nicht auf den Folien, sondern nur hinter einem Link
    zu Wikipedia. Hier sind sie kurz zusammengefasst:

    1. Gespielt wird auf einem Brett mit 8 × 8 Feldern. Die Steine sind auf
       einer Seite schwarz und auf der anderen weiß.
    2. Am Anfang liegen vier Steine in der Mitte, über Kreuz.
    3. **Schwarz beginnt**, danach wird abgewechselt.
    4. Ein Zug ist nur **gültig**, wenn der neue Stein in mindestens einer
       der **8 Richtungen** eine lückenlose Reihe gegnerischer Steine
       zwischen sich und einem eigenen Stein einschließt.
    5. Alle eingeschlossenen Steine werden **umgedreht** und gehören jetzt dir.
    6. Wer keinen gültigen Zug hat, muss **passen** (aussetzen).
    7. Kann **keiner** mehr ziehen, ist das Spiel zu Ende. Wer mehr Steine
       hat, gewinnt. Bei Gleichstand ist es **unentschieden**.

    :::analogie 🥪 Das Sandwich
    Ein Zug ist wie ein Sandwich. Deine Steine sind die **Brotscheiben**,
    die gegnerischen Steine sind der **Belag**.
      • Nur ein komplettes Sandwich zählt: Brot, Belag, Brot. Dann wird
        der Belag "dein" Belag (umgedreht).
      • Ist zwischen den Belägen ein Loch (ein leeres Feld), hält das
        Sandwich nicht. Dann wird nichts umgedreht.
      • Liegt nur auf einer Seite Brot (die andere Seite ist der
        Brettrand), ist es kein Sandwich.
      • Mit einem Stein kannst du gleichzeitig mehrere Sandwiches bauen,
        in verschiedene Richtungen. Dann wird in allen umgedreht.
    :::
    ---
    ## Ein Beispielzug

    So sieht das Brett am Anfang aus (S = Schwarz, W = Weiß, . = leer).
    Die Spalten zählen von links nach rechts, die Zeilen von oben nach unten:

    |   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
    |---|---|---|---|---|---|---|---|---|
    | 1 | . | . | . | . | . | . | . | . |
    | 2 | . | . | . | . | . | . | . | . |
    | 3 | . | . | . | . | . | . | . | . |
    | 4 | . | . | . | W | S | . | . | . |
    | 5 | . | . | . | S | W | . | . | . |
    | 6 | . | . | . | . | . | . | . | . |
    | 7 | . | . | . | . | . | . | . | . |
    | 8 | . | . | . | . | . | . | . | . |

    Schwarz setzt in **Spalte 4, Zeile 3**. Darunter liegt Weiß (Spalte 4,
    Zeile 4), und darunter wieder Schwarz (Spalte 4, Zeile 5). Das ist ein
    Sandwich! Der weiße Stein wird schwarz:

    :::vergleich Vorher (Ausschnitt Zeile 3–5) | Nachher
    |   | 3 | 4 | 5 |
    |---|---|---|---|
    | 3 | . | . | . |
    | 4 | . | W | S |
    | 5 | . | S | W |
    |||
    |   | 3 | 4 | 5 |
    |---|---|---|---|
    | 3 | . | S | . |
    | 4 | . | S | S |
    | 5 | . | S | W |
    :::

    Jetzt steht es 4 : 1 für Schwarz. Schwarz hat am Anfang genau vier
    gültige Züge: Spalte/Zeile 4/3, 3/4, 6/5 und 5/6.
    """)

k.mc("Wann ist ein Othello-Zug gültig?",
     ["Wenn der neue Stein in mindestens einer Richtung gegnerische Steine zwischen sich und einem eigenen Stein einschließt",
      "Wenn der neue Stein direkt neben irgendeinem Stein liegt",
      "Wenn das Feld leer ist – egal wo",
      "Wenn der neue Stein neben einem eigenen Stein liegt"],
     "Nur ein komplettes \"Sandwich\" zählt: eigener Stein, eine lückenlose Reihe gegnerischer "
     "Steine, eigener Stein. Ein Stein, der nur irgendwo daneben liegt, dreht nichts um und ist "
     "deshalb kein gültiger Zug.",
     tipp="Denk an das Sandwich: Brot – Belag – Brot.")

k.wf("Wer keinen gültigen Zug hat, hat das Spiel verloren.", False,
     "Wer nicht ziehen kann, muss nur **passen**, und der andere ist wieder dran. Das Spiel "
     "endet erst, wenn KEINER mehr ziehen kann. Dann gewinnt, wer mehr Steine hat.")

k.wf("Steine können auch schräg (diagonal) eingeschlossen und umgedreht werden.", True,
     "Es gibt 8 Richtungen: waagerecht (2), senkrecht (2) und diagonal (4). In jeder davon "
     "kann ein Sandwich entstehen.")

k.mc("Wer macht bei Othello den ersten Zug?",
     ["Schwarz", "Weiß", "Wer zuletzt gewonnen hat", "Das wird ausgelost"],
     "Nach den Regeln beginnt Schwarz. Danach wird abgewechselt (außer jemand muss passen).")

k.text("Wie nennt man es, wenn ein Spieler keinen gültigen Zug hat und deshalb aussetzen muss? "
       "(ein Verb)",
       ["passen", "aussetzen"],
       "Man muss **passen**. Danach ist der andere Spieler sofort wieder am Zug.")

k.mc("Wie soll dein Programm laut Handout mit den Spielern kommunizieren?",
     ["Über die Konsole mit input() und print()",
      "Über ein grafisches Fenster mit Maus",
      "Über eine Datei, in die man die Züge schreibt",
      "Gar nicht – der Computer spielt gegen sich selbst"],
     "Othello soll ein **Konsolenprogramm** sein: Eingaben mit `input()`, Ausgaben mit `print()`. "
     "Das kannst du alles seit Tag 1.")

# ── Erklärung 2: Liste von Listen ─────────────────────────────────────────
k.erklaerung("Das Spielfeld als Liste von Listen", r"""
    ## Eine Zeile ist eine Liste

    Wie speichert man ein Spielfeld? Fang mit **einer Zeile** an. Eine Zeile
    hat 8 Felder, also nimmst du eine Liste mit 8 Einträgen. Jeder Eintrag
    ist ein kurzer String:

        LEER, SCHWARZ, WEISS = '.', 'S', 'W'

    Diese drei Namen sind **Konstanten**: Werte, die sich im Programm nie
    ändern. In Python schreibt man sie nach Konvention in GROSSBUCHSTABEN.
    `SCHWARZ` liest sich besser als ein rätselhaftes `'S'`. Die Zeile oben
    weist drei Variablen auf einmal Werte zu (wie beim Entpacken von Tupeln).

    Die vierte Zeile des Startbretts sieht so aus:

    :::visual liste
    {"name": "zeile4", "werte": [".", ".", ".", "W", "S", ".", ".", "."],
     "markiert": [3, 4], "negativ": false}
    :::

    !! Der Index beginnt bei 0. Spalte 4 auf dem Brett ist also Index 3.
    ---
    ## Das Brett ist eine Liste von Zeilen

    Das ganze Brett ist eine Liste, deren 8 Einträge selbst wieder Listen
    sind: eine **Liste von Listen** (auch **2D-Liste**, "zweidimensional").

        brett = [zeile1, zeile2, zeile3, ..., zeile8]

    Ein Feld holst du mit **zwei** Indizes: `brett[y][x]`.
      • `brett[y]` holt zuerst die Zeile (y = Zeilennummer, von oben).
      • `[x]` holt aus dieser Zeile das Feld (x = Spaltennummer, von links).

    :::analogie 🎬 Die Kinokarte
    Auf einer Kinokarte steht "Reihe 4, Platz 5". Du suchst zuerst die
    **Reihe** und gehst dann in der Reihe zum **Platz**. Genauso
    `brett[reihe][platz]`, also `brett[y][x]`: erst die Zeile, dann das
    Feld darin. Wer "Platz 5, Reihe 4" vertauscht, sitzt falsch, und
    genau das passiert bei `brett[x][y]`.
    :::

    | Ausdruck | Bedeutung |
    |---|---|
    | `brett[3]` | die ganze 4. Zeile (eine Liste) |
    | `brett[3][4]` | Zeile 4, Spalte 5 → `'S'` |
    | `brett[3][4] = WEISS` | dieses Feld wird weiß |
    | `len(brett)` | 8 Zeilen |
    | `len(brett[0])` | 8 Felder pro Zeile |

    :::trace
    brett = [['.', '.', '.'],
             ['.', 'S', '.'],
             ['.', '.', 'W']]
    print(brett[1][1])
    print(brett[2][0])
    brett[0][2] = 'S'
    print(brett[0])
    :::

    :::achtung x und y vertauscht
    Der häufigste Fehler bei 2D-Listen: `brett[x][y]` statt `brett[y][x]`.
    Python meldet keinen Fehler, du landest nur auf dem falschen Feld.
    Merke: **erst y (Zeile), dann x (Spalte)**.
    :::
    ---
    ## Ein leeres Brett bauen

    Ein Brett baust du mit einer Schleife. Jede Runde hängt eine **neue**
    Zeile an:

    :::code
    brett = []
    for y in range(3):
        brett.append(['.'] * 3)
    brett[0][0] = 'S'
    print(brett)
    :::

    Kürzer sieht `[['.'] * 3] * 3` aus. Das ist aber eine **Falle**: Die
    äußere Multiplikation kopiert nicht die Zeile, sondern nur den
    **Verweis** auf dieselbe Zeile. Alle drei "Zeilen" sind ein und
    dieselbe Liste (Aliasing, wie bei `lst2 = lst1`):

    :::visual referenz
    {"namen": {"brett[0]": 0, "brett[1]": 0, "brett[2]": 0},
     "objekte": [[".", ".", "."]]}
    :::

    :::code
    falsch = [['.'] * 3] * 3
    falsch[0][0] = 'S'
    print(falsch)
    :::

    !! Ein Stein in Zeile 1 taucht plötzlich in ALLEN Zeilen auf. Baue das
    !! Brett deshalb mit einer Schleife und append.
    """)

k.ausdruck("Gegeben sind ein Brett `brett` sowie eine Spalte `x` und eine Zeile `y` "
           "(alle ab 0 gezählt). Schreibe einen Ausdruck, der das Feld in Spalte x, Zeile y liefert.",
           tests=[{"brett": [['.', 'S', '.'], ['W', '.', '.'], ['.', '.', 'S']], "x": 1, "y": 0},
                  {"brett": [['.', 'S', '.'], ['W', '.', '.'], ['.', '.', 'S']], "x": 0, "y": 1},
                  {"brett": [['.', 'S', '.'], ['W', '.', '.'], ['.', '.', 'S']], "x": 2, "y": 2},
                  {"brett": [['S', 'W', 'W'], ['.', '.', '.'], ['.', '.', '.']], "x": 2, "y": 0}],
           loesung="brett[y][x]",
           erklaerung="Erst die Zeile holen (`brett[y]`), dann darin das Feld (`[x]`). "
                      "`brett[x][y]` würde Zeile und Spalte vertauschen.",
           tipp="Wie bei der Kinokarte: erst die Reihe, dann der Platz.",
           muss_enthalten="[")

k.ausgabe(r"""
    brett = [['.', '.', '.'],
             ['S', 'W', '.'],
             ['.', '.', 'W']]
    print(brett[1][0], brett[2][2], len(brett[0]))
    """,
    "`brett[1]` ist die mittlere Zeile `['S', 'W', '.']`, davon Index 0 → `S`. "
    "`brett[2][2]` ist das Feld unten rechts → `W`. Jede Zeile hat 3 Felder.",
    tipp="Erst die Zeile auswählen, dann das Feld darin.")

k.mc("Welches Feld meint `brett[2][5]` auf dem Othello-Brett (Zählung ab 1 wie im Spiel)?",
     ["Zeile 3, Spalte 6", "Zeile 6, Spalte 3", "Zeile 2, Spalte 5", "Zeile 5, Spalte 2"],
     "Der erste Index ist die Zeile, der zweite die Spalte. Beide zählen ab 0, "
     "also Zeile 2 + 1 = 3 und Spalte 5 + 1 = 6.")

k.ausgabe(r"""
    brett = [['.'] * 3] * 3
    brett[1][1] = 'S'
    print(brett[0])
    """,
    "Alle drei Einträge von `brett` zeigen auf **dieselbe** Zeilenliste. Ändert man "
    "`brett[1][1]`, ändert man diese eine Liste, also sieht man das `'S'` auch über `brett[0]`. "
    "Deshalb baut man ein Brett mit einer Schleife und `append`.",
    tipp="Wie viele verschiedene Zeilenlisten gibt es hier wirklich?")

k.wf("`brett[y][x]` und `brett[x][y]` meinen immer dasselbe Feld.", False,
     "Nur wenn x und y zufällig gleich sind. Sonst vertauscht `brett[x][y]` Zeile und Spalte. "
     "Python meldet dabei keinen Fehler, das Programm rechnet einfach mit dem falschen Feld.")

# ── Erklärung 3: Rand prüfen und Brett anzeigen ───────────────────────────
k.erklaerung("Rand prüfen und Brett anzeigen", r"""
    ## Liegt ein Feld auf dem Brett?

    Später läufst du vom gesetzten Stein aus Schritt für Schritt über das
    Brett. Irgendwann kommst du an den Rand. Deshalb brauchst du eine
    Hilfsfunktion, die prüft, ob eine Koordinate noch auf dem Brett liegt:

        def im_feld(x, y):
            return 0 <= x < 8 and 0 <= y < 8

    `0 <= x < 8` ist ein **verketteter Vergleich**. Er bedeutet dasselbe wie
    `0 <= x and x < 8`. Gültig sind also die Indizes 0 bis 7.

    :::achtung Negative Indizes sind KEIN Fehler
    `brett[0][-1]` stürzt nicht ab. Python liefert einfach das **letzte**
    Feld der Zeile (negative Indizes zählen von hinten). Ein Programm, das
    den Rand nicht prüft, schaut so heimlich "um die Ecke" auf die andere
    Seite des Bretts. Bei Indizes über 7 gibt es dagegen einen `IndexError`.
    Prüfe deshalb immer erst `im_feld(x, y)`, bevor du `brett[y][x]` liest.
    :::

    :::visual liste
    {"name": "zeile", "werte": ["W", ".", ".", ".", ".", ".", ".", "S"],
     "markiert": [7], "negativ": true}
    :::

    `zeile[-1]` ist hier `'S'`, obwohl "links von Index 0" eigentlich gar
    kein Feld mehr ist.
    ---
    ## Das Brett anzeigen

    Die Spieler sollen das Brett sehen, und zwar mit Nummern, damit sie
    Spalte und Zeile eintippen können. Für die Spieler zählen wir **ab 1**:

          1 2 3 4 5 6 7 8
        1 . . . . . . . .
        2 . . . . . . . .
        3 . . . . . . . .
        4 . . . W S . . .
        5 . . . S W . . .
        6 . . . . . . . .
        7 . . . . . . . .
        8 . . . . . . . .

    Das Werkzeug dafür ist `' '.join(liste)`. Es klebt alle Strings einer
    Liste zusammen und setzt jeweils ein Leerzeichen dazwischen:

    :::code
    zeile = ['.', 'S', 'W', '.']
    print(' '.join(zeile))
    print(1, ' '.join(zeile))
    print('-'.join(zeile))
    :::

    `print` mit mehreren Werten trennt sie automatisch durch ein
    Leerzeichen. Die Kopfzeile beginnt mit zwei Leerzeichen, damit die
    Spaltennummern über den Feldern stehen.

    :::info Ohne join geht es auch
    Du kannst jedes Feld einzeln mit `print(feld, end=' ')` ausgeben.
    `end=' '` ersetzt den Zeilenumbruch am Ende durch ein Leerzeichen.
    Nach jeder Zeile brauchst du dann ein leeres `print()`.
    :::
    """)

k.ausdruck("Schreibe einen Ausdruck, der `True` liefert, wenn die Koordinate (x, y) auf dem "
           "8×8-Brett liegt (Indizes 0 bis 7), sonst `False`.",
           tests=[{"x": 0, "y": 0}, {"x": 7, "y": 7}, {"x": 8, "y": 3}, {"x": 3, "y": -1},
                  {"x": -1, "y": 5}, {"x": 4, "y": 8}, {"x": 5, "y": 2}],
           loesung="0 <= x < 8 and 0 <= y < 8",
           erklaerung="Beide Koordinaten müssen zwischen 0 (einschließlich) und 8 (ausschließlich) "
                      "liegen. Mit verketteten Vergleichen: `0 <= x < 8 and 0 <= y < 8`.",
           tipp="Du brauchst zwei Bedingungen, verbunden mit and.")

k.ausgabe(r"""
    zeile = ['W', '.', '.', '.', '.', '.', '.', 'S']
    print(zeile[-1])
    """,
    "Negative Indizes zählen von hinten: `zeile[-1]` ist das letzte Feld, also `S`. "
    "Kein Fehler! Deshalb muss ein Programm den Rand selbst prüfen.",
    tipp="Was bedeutet ein negativer Index?")

k.ausgabe(r"""
    zeile = ['S', '.', 'W']
    print(3, ' '.join(zeile))
    """,
    "`' '.join(zeile)` ergibt `S . W`. `print` setzt zwischen die 3 und diesen Text ein "
    "Leerzeichen: `3 S . W`.")

k.mc("Was passiert bei `brett[2][8]` auf einem 8×8-Brett?",
     ["Es gibt einen IndexError", "Man bekommt das erste Feld der Zeile",
      "Man bekommt None", "Python erweitert die Liste automatisch"],
     "Gültig sind die Indizes 0 bis 7 (und -1 bis -8). Index 8 gibt es nicht, also "
     "`IndexError: list index out of range`.")

# ── Praxisteil ─────────────────────────────────────────────────────────────
k.luecke("Ergänze die Funktion `gegner(spieler)`. Sie bekommt `SCHWARZ` oder `WEISS` und gibt "
         "die jeweils andere Farbe zurück.",
         r"""
         LEER, SCHWARZ, WEISS = '.', 'S', 'W'

         def gegner(spieler):
             if spieler == ___:
                 return WEISS
             ___ SCHWARZ
         """,
         [["SCHWARZ", "'S'"], ["return"]],
         "Ist der Spieler Schwarz, ist der Gegner Weiß. In allen anderen Fällen (also bei Weiß) "
         "ist der Gegner Schwarz. Ein `else` ist nicht nötig, weil `return` die Funktion sofort "
         "beendet.",
         tipp="Welche Farbe muss der Spieler haben, damit der Gegner WEISS ist?")

k.code(r"""
    ## Liegt das Feld auf dem Brett?

    Schreibe eine Funktion `im_feld(x, y)`. Sie gibt `True` zurück, wenn die
    Spalte `x` und die Zeile `y` auf dem 8×8-Brett liegen (beide ab 0
    gezählt, also 0 bis 7). Sonst gibt sie `False` zurück.

        im_feld(0, 0)   →  True
        im_feld(7, 3)   →  True
        im_feld(8, 3)   →  False
        im_feld(2, -1)  →  False
    """,
    [F("im_feld(0, 0)", True), F("im_feld(7, 7)", True), F("im_feld(8, 3)", False),
     F("im_feld(3, 8)", False), F("im_feld(-1, 4)", False), F("im_feld(5, -1)", False)],
    CODE_IM_FELD,
    "Beide Koordinaten müssen im Bereich 0 bis 7 liegen. Der verkettete Vergleich "
    "`0 <= x < 8` prüft beide Grenzen auf einmal. Typische Fehler sind `<= 8` (dann zählt "
    "Index 8 mit, den es nicht gibt) und das Vergessen der negativen Werte.",
    tipps=["Welche Indizes gibt es bei 8 Feldern?",
           "Prüfe x und y getrennt und verbinde beide Bedingungen mit and.",
           "return 0 <= x < 8 and 0 <= ___"],
    vorlage="def im_feld(x, y):\n    ...\n")

k.code(r"""
    ## Das Startbrett

    Schreibe eine Funktion `neues_brett()`, die das Othello-Startbrett als
    **Liste von 8 Zeilenlisten** mit je 8 Feldern zurückgibt. Alle Felder
    sind `LEER`, nur in der Mitte liegen vier Steine:

    | Feld | Inhalt |
    |---|---|
    | `brett[3][3]` | `WEISS` |
    | `brett[3][4]` | `SCHWARZ` |
    | `brett[4][3]` | `SCHWARZ` |
    | `brett[4][4]` | `WEISS` |

    Wichtig: Jede Zeile muss eine **eigene** Liste sein. Ein Test setzt
    einen Stein in die erste Zeile und schaut, ob er in den anderen Zeilen
    auftaucht (die `[[LEER] * 8] * 8`-Falle).
    """,
    [F("neues_brett()"),
     F("len(neues_brett())", 8),
     F("[len(zeile) for zeile in neues_brett()]", [8] * 8),
     F("erste_spalte_nach_aenderung()",
       vorspann="""
       def erste_spalte_nach_aenderung():
           # Setzt einen Stein in die Ecke oben links und liest dann Spalte 1 aller Zeilen.
           brett = neues_brett()
           brett[0][0] = 'S'
           return [zeile[0] for zeile in brett]
       """),
     F("zaehle_steine(neues_brett())", (2, 2),
       vorspann="""
       def zaehle_steine(brett):
           # Hilfsfunktion des Tests: (Anzahl S, Anzahl W)
           return (sum(z.count('S') for z in brett), sum(z.count('W') for z in brett))
       """)],
    CODE_KONSTANTEN + "\n" + CODE_NEUES_BRETT,
    "Die Schleife hängt 8-mal eine **neue** Liste `[LEER] * 8` an. Jede Zeile ist damit ein "
    "eigenes Objekt. Danach werden die vier Startsteine gesetzt – immer `brett[y][x]`, "
    "also erst die Zeile. Mit `[[LEER] * 8] * 8` wären alle Zeilen dieselbe Liste, und der "
    "Test mit der Ecke würde 8 schwarze Steine finden.",
    tipps=["Starte mit einer leeren Liste und hänge in einer for-Schleife Zeilen an.",
           "Eine Zeile ist [LEER] * 8. Danach setzt du brett[3][3] = WEISS usw.",
           "for y in range(8):\n    brett.append([LEER] * 8)"],
    vorlage="LEER, SCHWARZ, WEISS = '.', 'S', 'W'\n\n\ndef neues_brett():\n    brett = []\n"
            "    # 8 Zeilen anhängen, dann die 4 Startsteine setzen\n    return brett\n")

_ANZEIGE_START = ["  1 2 3 4 5 6 7 8", "1 . . . . . . . .", "2 . . . . . . . .",
                  "3 . . . . . . . .", "4 . . . W S . . .", "5 . . . S W . . .",
                  "6 . . . . . . . .", "7 . . . . . . . .", "8 . . . . . . . ."]

k.code(r"""
    ## Das Brett anzeigen

    Schreibe eine Funktion `brett_zeigen(brett)`, die das Brett so ausgibt
    (Beispiel: Startbrett):

          1 2 3 4 5 6 7 8
        1 . . . . . . . .
        2 . . . . . . . .
        3 . . . . . . . .
        4 . . . W S . . .
        5 . . . S W . . .
        6 . . . . . . . .
        7 . . . . . . . .
        8 . . . . . . . .

      • Kopfzeile: zwei Leerzeichen, dann die Spaltennummern 1 bis 8.
      • Danach 8 Zeilen: Zeilennummer **ab 1**, dann die Felder, jeweils mit
        einem Leerzeichen getrennt.

    Die Funktion gibt nur aus, sie braucht kein `return`. Die Konstanten
    und `neues_brett()` stehen schon in der Vorlage. Die Tests rufen deine
    Funktion mit verschiedenen Brettern auf.
    """,
    [P(nachspann="brett_zeigen(neues_brett())", exakt=_ANZEIGE_START,
       vorspann=CODE_ETAPPE1.replace(CODE_BRETT_ZEIGEN, ""), beschreibung="Startbrett",
       leerzeichen=True),
     P(nachspann="b = neues_brett()\nb[0][0] = 'S'\nb[7][7] = 'W'\nb[2][5] = 'S'\nbrett_zeigen(b)",
       exakt=["  1 2 3 4 5 6 7 8", "1 S . . . . . . .", "2 . . . . . . . .",
              "3 . . . . . S . .", "4 . . . W S . . .", "5 . . . S W . . .",
              "6 . . . . . . . .", "7 . . . . . . . .", "8 . . . . . . . W"],
       vorspann=CODE_ETAPPE1.replace(CODE_BRETT_ZEIGEN, ""),
       beschreibung="Brett mit Steinen in den Ecken", leerzeichen=True)],
    CODE_BRETT_ZEIGEN,
    "Die Kopfzeile ist ein fester Text. Dann läuft `y` von 0 bis 7: `y + 1` ist die Nummer "
    "für die Spieler, `' '.join(brett[y])` macht aus der Zeilenliste einen Text mit "
    "Leerzeichen. `print` setzt zwischen Nummer und Text noch ein Leerzeichen.",
    tipps=["Erst die Kopfzeile ausgeben, dann eine Schleife über die 8 Zeilen.",
           "' '.join(liste) verbindet die Felder einer Zeile mit Leerzeichen.",
           "for y in range(8):\n    print(y + 1, ' '.join(brett[y]))"],
    vorlage=CODE_KONSTANTEN + "\n\n" + CODE_NEUES_BRETT + "\n\ndef brett_zeigen(brett):\n"
            "    print('  1 2 3 4 5 6 7 8')\n    # jetzt die 8 Zeilen\n")

k.zusammenfassung(r"""
    ## Othello: Regeln & Spielfeld

      • 8 × 8 Felder, Start mit 4 Steinen über Kreuz in der Mitte, **Schwarz beginnt**.
      • Gültiger Zug = Sandwich: eigener Stein, lückenlose Reihe gegnerischer Steine,
        neuer eigener Stein. Die eingeschlossenen Steine werden umgedreht.
      • Kein gültiger Zug → passen. Keiner kann ziehen → Spielende, mehr Steine gewinnt.

    | Ausdruck | Bedeutung |
    |---|---|
    | `brett[y]` | ganze Zeile y (Liste) |
    | `brett[y][x]` | Feld in Zeile y, Spalte x (erst Zeile!) |
    | `0 <= x < 8` | x liegt auf dem Brett |
    | `' '.join(zeile)` | Felder mit Leerzeichen verbinden |

        LEER, SCHWARZ, WEISS = '.', 'S', 'W'

        def neues_brett():
            brett = []
            for y in range(8):
                brett.append([LEER] * 8)   # jede Zeile eine EIGENE Liste
            brett[3][3] = WEISS
            brett[3][4] = SCHWARZ
            brett[4][3] = SCHWARZ
            brett[4][4] = WEISS
            return brett

    !! Nie `[[LEER] * 8] * 8` – das sind 8 Verweise auf DIESELBE Zeile.

    !! Negative Indizes sind kein Fehler – deshalb immer zuerst im_feld prüfen.
    """)
