# -*- coding: utf-8 -*-
"""Challenge, Etappe 3: Othello – Eingaben prüfen, Passen, Spielende, Gewinner."""
from ..engine import neues_kapitel, P, F
from .c_01_othello_spielfeld import CODE_ETAPPE1
from .c_02_othello_zuege import CODE_ETAPPE2, TESTBRETTER

CODE_ZAHL_EINLESEN = """\
def zahl_einlesen(text):
    while True:
        eingabe = input(text)
        if eingabe.isnumeric() and 1 <= int(eingabe) <= 8:
            return int(eingabe) - 1
        print('Bitte eine Zahl von 1 bis 8 eingeben.')
"""

CODE_HAT_ZUG = """\
def hat_zug(brett, spieler):
    for y in range(8):
        for x in range(8):
            if gueltiger_zug(brett, x, y, spieler):
                return True
    return False
"""

CODE_ZAEHLEN = """\
def zaehlen(brett):
    schwarz = 0
    weiss = 0
    for zeile in brett:
        schwarz += zeile.count(SCHWARZ)
        weiss += zeile.count(WEISS)
    return (schwarz, weiss)
"""

CODE_GEWINNER = """\
def gewinner(brett):
    schwarz, weiss = zaehlen(brett)
    if schwarz > weiss:
        return 'Schwarz'
    elif weiss > schwarz:
        return 'Weiß'
    return 'Unentschieden'
"""

CODE_ETAPPE3 = "\n\n".join([CODE_ZAHL_EINLESEN, CODE_HAT_ZUG, CODE_ZAEHLEN, CODE_GEWINNER])

TESTBRETTER3 = TESTBRETTER + """
ECKE = brett_aus('S.......',
                 '........',
                 '........',
                 '........',
                 '........',
                 '........',
                 '.......S',
                 '.......W')

LEERES = brett_aus(*['........'] * 8)
"""


def _vorspann(*bausteine):
    return "\n\n".join([CODE_ETAPPE1, CODE_ETAPPE2, *bausteine, TESTBRETTER3])


k = neues_kapitel(
    slug="othello_spielende",
    titel="Challenge 3 – Othello: Eingaben, Passen & Spielende",
    beschreibung="Eingaben mit isnumeric() prüfen, Passen erkennen, Steine zählen, Gewinner bestimmen",
    quelle="Challenge-Handout",
    teil="challenge",
    icon="🏁")

k.lernziele([
    "Ich kann Eingaben mit isnumeric() prüfen und so lange nachfragen, bis sie stimmen",
    "Ich kann prüfen, ob die Farbe am Zug überhaupt einen gültigen Zug hat (sonst wird gepasst)",
    "Ich kann erklären, wann das Spiel zu Ende ist",
    "Ich kann die Steine zählen und den Gewinner oder ein Unentschieden bestimmen",
])

# ── Erklärung 1: Eingaben prüfen ──────────────────────────────────────────
k.erklaerung("Eingaben prüfen mit isnumeric()", r"""
    ## Spieler tippen alles Mögliche

    Die Spieler geben Spalte und Zeile mit `input()` ein. `input()` liefert
    **immer einen String**. Tippt jemand `abc`, stürzt `int('abc')` mit
    einem `ValueError` ab, und das ganze Spiel ist vorbei. Das Handout gibt
    dafür einen Hinweis: Mit `.isnumeric()` prüfst du vorher, ob ein String
    nur aus Ziffern besteht.

    :::code
    print('4'.isnumeric())
    print('12'.isnumeric())
    print('abc'.isnumeric())
    print('-3'.isnumeric())
    print(''.isnumeric())
    :::

    :::analogie 🚪 Der Türsteher
    Vor dem Club steht ein Türsteher und prüft zwei Dinge **nacheinander**:
    Erst "Hast du überhaupt einen Ausweis?" (Ist es eine Zahl?), dann
    "Bist du alt genug?" (Liegt die Zahl zwischen 1 und 8?). Ohne Ausweis
    fragt er gar nicht erst nach dem Alter. Wer durchfällt, wird nicht
    rausgeworfen, sondern stellt sich **wieder hinten an**: Das Programm
    fragt einfach noch einmal. Erst wer beide Prüfungen besteht, kommt rein.
    :::
    ---
    ## So lange fragen, bis es passt

    :::visual schleife
    {"bedingung": "True", "art": "while",
     "koerper": ["eingabe = input(text)",
                 "if eingabe.isnumeric() and 1 <= int(eingabe) <= 8: return int(eingabe) - 1",
                 "print('Bitte eine Zahl von 1 bis 8 eingeben.')"],
     "danach": "(wird nur über return verlassen)"}
    :::

    `while True:` ist eine Endlosschleife mit Ausgang: Das `return` beendet
    die Funktion – und damit auch die Schleife – sobald die Eingabe gültig
    ist. Die Spieler zählen ab 1, die Liste ab 0, deshalb `- 1`.

    :::code eingaben=abc|9|4
    def zahl_einlesen(text):
        while True:
            eingabe = input(text)
            if eingabe.isnumeric() and 1 <= int(eingabe) <= 8:
                return int(eingabe) - 1
            print('Bitte eine Zahl von 1 bis 8 eingeben.')

    spalte = zahl_einlesen('Spalte (1-8): ')
    print('Index:', spalte)
    :::

    :::achtung Erst prüfen, dann umwandeln
    `int(eingabe) <= 8 and eingabe.isnumeric()` stürzt bei `abc` ab, weil
    `int('abc')` zuerst ausgewertet wird. In der richtigen Reihenfolge
    sorgt `and` dafür, dass `int(...)` nur bei echten Ziffern aufgerufen
    wird (Kurzschlussauswertung, wie beim Türsteher).
    :::

    :::info Kleingedrucktes zu isnumeric()
    Auf der Folie steht `string.isnumeric()`. Gemeint ist die Methode, die
    jeder String hat, also z. B. `eingabe.isnumeric()`. Für die Challenge
    reicht sie völlig. Ganz genau genommen erkennt sie auch Zeichen wie
    `'½'` als "numerisch", obwohl `int('½')` scheitert. Wer ganz sicher
    gehen will, nimmt `eingabe.isdecimal()`. Negative Zahlen (`'-3'`) und
    Leerzeichen (`' 3'`) ergeben bei beiden `False`.
    :::
    """)

k.ausgabe(r"""
    for text in ['7', '07', 'sieben', '7.5', '']:
        print(text.isnumeric())
    """,
    "`'7'` und `'07'` bestehen nur aus Ziffern → True. `'sieben'` sind Buchstaben, `'7.5'` "
    "enthält einen Punkt und der leere String enthält gar keine Ziffer → jeweils False.",
    tipp="isnumeric() ist nur True, wenn der String nicht leer ist und NUR aus Ziffern besteht.")

k.mc("Welche Eingabe akzeptiert `eingabe.isnumeric() and 1 <= int(eingabe) <= 8`?",
     ["'8'", "'9'", "'0'", "'-1'"],
     "`'9'` und `'0'` sind zwar Ziffern, liegen aber außerhalb von 1 bis 8. `'-1'` ist für "
     "isnumeric() keine Zahl (das Minus ist keine Ziffer). Nur `'8'` besteht beide Prüfungen.")

k.wf("`'-3'.isnumeric()` ergibt True.", False,
     "Das Minuszeichen ist keine Ziffer, also ergibt es `False`. Für die Challenge ist das "
     "praktisch: Negative Eingaben werden automatisch abgelehnt.")

k.mc("Warum gibt `zahl_einlesen` `int(eingabe) - 1` zurück?",
     ["Die Spieler zählen ab 1, die Listen-Indizes beginnen bei 0",
      "Damit die Zahl nie größer als 8 wird",
      "Weil input() immer eins zu viel liefert",
      "Damit isnumeric() funktioniert"],
     "Auf dem angezeigten Brett heißen die Spalten 1 bis 8. Im Programm sind es die Indizes "
     "0 bis 7. Die Umrechnung passiert an genau einer Stelle: beim Einlesen.")

k.ausgabe(r"""
    eingabe = 'abc'
    if eingabe.isnumeric() and int(eingabe) <= 8:
        print('ok')
    else:
        print('nochmal')
    """,
    "`'abc'.isnumeric()` ist False. Wegen der Kurzschlussauswertung wird `int('abc')` gar "
    "nicht erst aufgerufen, es gibt also keinen Fehler, sondern `nochmal`.")

# ── Erklärung 2: Passen und Spielende ─────────────────────────────────────
k.erklaerung("Passen und Spielende", r"""
    ## Kann der Spieler überhaupt ziehen?

    Bevor jemand nach einem Zug gefragt wird, muss das Programm wissen, ob
    es für diese Farbe **irgendeinen** gültigen Zug gibt. Dafür probiert es alle 64 Felder
    durch: zwei verschachtelte Schleifen, eine für die Zeilen, eine für die
    Spalten. Sobald ein gültiger Zug gefunden ist, ist die Antwort klar:
    sofort `return True`. Erst wenn **alle** Felder durchprobiert sind und
    keins gepasst hat, ist die Antwort `False`.

    :::trace
    brett = [['S', 'W'],
             ['.', 'S']]
    def erstes_leeres(brett):
        for y in range(2):
            for x in range(2):
                if brett[y][x] == '.':
                    return (x, y)
        return None
    print(erstes_leeres(brett))
    :::

    :::achtung return False nicht in die Schleife!
    Ein `else: return False` innerhalb der Schleife beendet die Funktion
    schon beim **ersten** Feld, das nicht passt. Dann werden 63 Felder nie
    geprüft. `return False` gehört **hinter** beide Schleifen.
    :::
    ---
    ## Wann ist das Spiel vorbei?

    | Situation | Was passiert? |
    |---|---|
    | Spieler am Zug hat einen gültigen Zug | es muss gezogen werden |
    | Spieler am Zug hat keinen Zug, der andere schon | **passen**, der andere ist dran |
    | **Keiner** hat einen gültigen Zug | Spielende |

    Das Spiel endet also nicht nur, wenn alle 64 Felder voll sind. Auch
    wenn noch Felder frei sind, kann es vorbei sein, z. B. wenn ein Spieler
    gar keine Steine mehr hat.

    !! Spielende ⇔ not hat_zug(brett, SCHWARZ) and not hat_zug(brett, WEISS)
    """)

k.mc("Schwarz ist am Zug, hat aber keinen gültigen Zug. Weiß hat noch Züge. Was passiert?",
     ["Schwarz passt, Weiß ist sofort wieder am Zug",
      "Das Spiel ist zu Ende",
      "Schwarz hat verloren",
      "Schwarz darf einen Stein auf ein beliebiges Feld setzen"],
     "Wer nicht ziehen kann, setzt nur aus. Das Spiel endet erst, wenn KEINER mehr ziehen kann.")

k.wf("Das Spiel endet erst, wenn alle 64 Felder belegt sind.", False,
     "Es endet, sobald keiner mehr einen gültigen Zug hat. Das kann auch mit freien Feldern "
     "passieren, z. B. wenn alle Steine dieselbe Farbe haben.")

k.mc("Was ist falsch an dieser Version von hat_zug?",
     ["Sie gibt schon nach dem ersten Feld (0, 0) eine Antwort",
      "Sie prüft die Felder doppelt",
      "Sie gibt nie True zurück",
      "Nichts, sie ist richtig"],
     "Beim ersten Feld wird entweder True oder False zurückgegeben – die Funktion ist danach "
     "beendet. `return False` darf erst nach beiden Schleifen stehen.",
     code="""
     def hat_zug(brett, spieler):
         for y in range(8):
             for x in range(8):
                 if gueltiger_zug(brett, x, y, spieler):
                     return True
                 else:
                     return False
     """)

k.ausgabe(r"""
    def suche(liste, ziel):
        for i in range(len(liste)):
            if liste[i] == ziel:
                return i
        return -1

    print(suche(['.', 'W', 'S', 'S'], 'S'), suche(['.', '.'], 'S'))
    """,
    "Das erste `'S'` steht bei Index 2. `return` beendet die Funktion sofort, das zweite "
    "`'S'` wird nicht mehr angeschaut. In der zweiten Liste gibt es kein `'S'`, also läuft "
    "die Schleife ganz durch und es kommt `-1`.")

# ── Erklärung 3: Zählen und Gewinner ──────────────────────────────────────
k.erklaerung("Steine zählen und Gewinner bestimmen", r"""
    ## Zählen mit count()

    `liste.count(wert)` zählt, wie oft ein Wert in einer Liste vorkommt.
    Für das ganze Brett zählst du Zeile für Zeile und addierst:

    :::code
    brett = [['S', 'W', '.'],
             ['S', 'S', 'W'],
             ['.', '.', 'S']]
    schwarz = 0
    for zeile in brett:
        schwarz += zeile.count('S')
    print(schwarz)
    :::

    Zwei Ergebnisse auf einmal gibt eine Funktion als **Tupel** zurück:
    `return (schwarz, weiss)`. Beim Aufruf entpackst du es wieder:
    `schwarz, weiss = zaehlen(brett)`.

    :::visual variablen
    {"vars": [{"name": "schwarz", "wert": "19", "typ": "int"},
              {"name": "weiss", "wert": "45", "typ": "int"}]}
    :::
    ---
    ## Wer hat gewonnen?

    :::visual entscheidung
    {"bedingung": "schwarz > weiss", "ja": "'Schwarz'",
     "elif": [{"bedingung": "weiss > schwarz", "text": "'Weiß'"}],
     "nein": "'Unentschieden'"}
    :::

    Das Handout verlangt ausdrücklich beide Fälle: Es soll ausgegeben
    werden, **welcher Spieler gewonnen hat bzw. ob keiner gewonnen hat**.
    Vergiss also das Unentschieden nicht!
    """)

k.ausgabe(r"""
    zeile = ['S', 'W', 'S', '.', 'S']
    print(zeile.count('S'), zeile.count('.'), zeile.count('X'))
    """,
    "`'S'` kommt dreimal vor, `'.'` einmal, `'X'` gar nicht → `3 1 0`.")

k.ausgabe(r"""
    def zaehle(a, b):
        return (a + b, a - b)

    summe, differenz = zaehle(19, 45)
    print(differenz)
    """,
    "Die Funktion gibt ein Tupel `(64, -26)` zurück. Beim Entpacken bekommt `summe` den "
    "ersten und `differenz` den zweiten Wert: `-26`.")

k.wf("Bei 32 : 32 Steinen soll das Programm \"Unentschieden\" bzw. \"keiner hat gewonnen\" melden.",
     True,
     "Laut Handout soll am Ende ausgegeben werden, welcher Spieler gewonnen hat **bzw. ob "
     "keiner gewonnen hat**. Gleichstand ist bei Othello möglich.")

# ── Praxisteil ─────────────────────────────────────────────────────────────
_NACH = "print('Ergebnis:', zahl_einlesen('Spalte (1-8): '))"

k.code(r"""
    ## Spalte oder Zeile einlesen

    Schreibe eine Funktion `zahl_einlesen(text)`. Sie
      • fragt mit `input(text)` nach einer Eingabe,
      • prüft mit `.isnumeric()`, ob es eine Zahl ist, und ob sie zwischen
        1 und 8 liegt,
      • gibt bei einer ungültigen Eingabe genau diesen Satz aus und fragt
        dann erneut: `Bitte eine Zahl von 1 bis 8 eingeben.`
      • gibt bei einer gültigen Eingabe die Zahl **minus 1** zurück
        (Index ab 0).

    Beispiel (der Test ruft
    `print('Ergebnis:', zahl_einlesen('Spalte (1-8): '))` auf):

        Spalte (1-8): abc
        Bitte eine Zahl von 1 bis 8 eingeben.
        Spalte (1-8): 9
        Bitte eine Zahl von 1 bis 8 eingeben.
        Spalte (1-8): 4
        Ergebnis: 3
    """,
    [P(["abc", "9", "0", "4"], erwartet=["Bitte eine Zahl von 1 bis 8 eingeben.", "Ergebnis: 3"],
       nachspann=_NACH),
     P(["8"], erwartet=["Ergebnis: 7"], nicht=["Bitte eine Zahl"], nachspann=_NACH),
     P(["1"], erwartet=["Ergebnis: 0"], nicht=["Bitte eine Zahl"], nachspann=_NACH),
     P(["-3", "", "2.5", "2"], erwartet=["Bitte eine Zahl von 1 bis 8 eingeben.", "Ergebnis: 1"],
       nachspann=_NACH)],
    CODE_ZAHL_EINLESEN,
    "`while True` wiederholt die Frage, bis das `return` die Funktion verlässt. Die Bedingung "
    "prüft zuerst `isnumeric()`, damit `int()` nie bei Buchstaben aufgerufen wird. `- 1` "
    "rechnet die Spieler-Zählung (1–8) in Listen-Indizes (0–7) um.",
    tipps=["Du brauchst eine Schleife, die erst endet, wenn die Eingabe gültig ist.",
           "while True: … und darin ein if mit isnumeric() und dem Bereich 1 bis 8.",
           "if eingabe.isnumeric() and 1 <= int(eingabe) <= 8:\n    return int(eingabe) - 1"],
    vorlage="def zahl_einlesen(text):\n    while True:\n        eingabe = input(text)\n        # prüfen …\n",
    streng=True)

k.code(r"""
    ## Kann der Spieler ziehen?

    Schreibe `hat_zug(brett, spieler)`. Die Funktion gibt `True` zurück,
    wenn `spieler` auf **irgendeinem** der 64 Felder einen gültigen Zug hat
    (`gueltiger_zug` aus Etappe 2), sonst `False`.

        hat_zug(neues_brett(), 'S')   →  True

    Testbrett `ECKE`: Schwarz in der Ecke oben links und bei (7, 6),
    Weiß in der Ecke unten rechts (7, 7). Weiß kann auf (7, 5) setzen,
    Schwarz hat keinen Zug. Außerdem gibt es ein leeres Brett `LEERES`.

    Alle Funktionen aus Etappe 1 und 2 stehen in der Vorlage.
    """,
    [F("hat_zug(neues_brett(), 'S')", True, vorspann=_vorspann()),
     F("hat_zug(neues_brett(), 'W')", True, vorspann=_vorspann()),
     F("hat_zug(ECKE, 'W')", True, vorspann=_vorspann()),
     F("hat_zug(ECKE, 'S')", False, vorspann=_vorspann()),
     F("hat_zug(LEERES, 'S')", False, vorspann=_vorspann())],
    CODE_HAT_ZUG,
    "Zwei verschachtelte Schleifen gehen alle Felder durch. Beim ersten gültigen Zug ist die "
    "Antwort sicher `True`. `return False` steht hinter den Schleifen, denn erst wenn alle 64 "
    "Felder geprüft sind, steht fest, dass es keinen Zug gibt. Das Brett `ECKE` erwischt "
    "Lösungen, die nach dem ersten Feld aufgeben: Der einzige Zug liegt fast ganz unten.",
    tipps=["Probiere jedes Feld mit gueltiger_zug aus.",
           "for y in range(8):\n    for x in range(8):\n        …",
           "Innen: if gueltiger_zug(brett, x, y, spieler): return True. Nach den Schleifen: return False."],
    vorlage=CODE_ETAPPE1 + "\n\n" + CODE_ETAPPE2 + "\n\ndef hat_zug(brett, spieler):\n    ...\n")

k.code(r"""
    ## Steine zählen

    Schreibe `zaehlen(brett)`. Die Funktion gibt ein **Tupel**
    `(schwarz, weiss)` mit der Anzahl der schwarzen und der weißen Steine
    zurück – Schwarz zuerst!

        zaehlen(neues_brett())   →  (2, 2)

    Der Test-Helfer `nach_zug` führt vorher einen Zug aus, damit die
    Zahlen verschieden sind.
    """,
    [F("zaehlen(neues_brett())", (2, 2), vorspann=_vorspann(CODE_HAT_ZUG)),
     F("zaehlen(nach_zug(neues_brett(), 3, 2, 'S'))", (4, 1), vorspann=_vorspann(CODE_HAT_ZUG)),
     F("zaehlen(ECKE)", (2, 1), vorspann=_vorspann(CODE_HAT_ZUG)),
     F("zaehlen(LEERES)", (0, 0), vorspann=_vorspann(CODE_HAT_ZUG)),
     F("zaehlen([['S'] * 8] * 5 + [['W'] * 8] * 3)", (40, 24), vorspann=_vorspann(CODE_HAT_ZUG))],
    CODE_ZAEHLEN,
    "`zeile.count(SCHWARZ)` zählt die schwarzen Steine einer Zeile, die Schleife addiert alle "
    "Zeilen. Die Reihenfolge im Tupel ist wichtig: `(schwarz, weiss)`. Wer sie vertauscht, "
    "scheitert am Test nach dem Zug (4 : 1).",
    tipps=["Zwei Zähler, beide starten bei 0.",
           "for zeile in brett: … zeile.count(SCHWARZ) …",
           "return (schwarz, weiss)"],
    vorlage="LEER, SCHWARZ, WEISS = '.', 'S', 'W'\n\n\ndef zaehlen(brett):\n    schwarz = 0\n"
            "    weiss = 0\n    # …\n    return (schwarz, weiss)\n")

k.luecke("Ergänze `gewinner(brett)`. Sie gibt `'Schwarz'`, `'Weiß'` oder `'Unentschieden'` zurück.",
         r"""
         def gewinner(brett):
             schwarz, weiss = ___(brett)
             if schwarz > weiss:
                 return 'Schwarz'
             ___ weiss > schwarz:
                 return 'Weiß'
             ___ 'Unentschieden'
         """,
         [["zaehlen"], ["elif", "if"], ["return"]],
         "`zaehlen` liefert das Tupel, das direkt entpackt wird. Danach drei Fälle: Schwarz vorn, "
         "Weiß vorn, sonst Gleichstand. Weil jedes `return` die Funktion beendet, braucht der "
         "letzte Fall kein `else`.",
         tipp="Welche Funktion liefert (schwarz, weiss)?")

k.zusammenfassung(r"""
    ## Eingaben, Passen & Spielende

        def zahl_einlesen(text):
            while True:
                eingabe = input(text)
                if eingabe.isnumeric() and 1 <= int(eingabe) <= 8:
                    return int(eingabe) - 1        # Spieler zählen ab 1
                print('Bitte eine Zahl von 1 bis 8 eingeben.')

    | Werkzeug | Wofür |
    |---|---|
    | `s.isnumeric()` | Besteht s nur aus Ziffern? (`'-3'`, `''` → False) |
    | `while True:` + `return` | so lange fragen, bis es passt |
    | `liste.count(x)` | wie oft kommt x vor? |
    | `return (a, b)` | zwei Werte als Tupel zurückgeben |

      • Kein gültiger Zug → **passen**, der andere ist dran.
      • **Keiner** kann ziehen → Spielende (auch mit freien Feldern).
      • Gewinner: mehr Steine; Gleichstand → unentschieden.

    !! Erst isnumeric(), dann int() – und return False erst NACH allen Schleifen.
    """)
