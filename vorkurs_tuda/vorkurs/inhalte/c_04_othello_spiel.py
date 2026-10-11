# -*- coding: utf-8 -*-
"""Challenge, Etappe 4: Othello – alles zusammensetzen zum spielbaren Programm."""
from ..engine import neues_kapitel, P, F
from .c_01_othello_spielfeld import CODE_ETAPPE1
from .c_02_othello_zuege import CODE_ETAPPE2, TESTBRETTER
from .c_03_othello_spielende import CODE_ETAPPE3

CODE_ALLES = "\n\n".join([CODE_ETAPPE1, CODE_ETAPPE2, CODE_ETAPPE3])

CODE_MOEGLICHE_ZUEGE = """\
def moegliche_zuege(brett, spieler):
    zuege = []
    for y in range(8):
        for x in range(8):
            if gueltiger_zug(brett, x, y, spieler):
                zuege.append((x + 1, y + 1))
    return zuege
"""

CODE_COMPUTER_ZUG = """\
def computer_zug(brett, spieler):
    bester = None
    beste_anzahl = 0
    for y in range(8):
        for x in range(8):
            anzahl = len(umzudrehende(brett, x, y, spieler))
            if anzahl > beste_anzahl:
                bester = (x, y)
                beste_anzahl = anzahl
    return bester
"""

CODE_SPIELEN = """\
NAMEN = {SCHWARZ: 'Schwarz', WEISS: 'Weiß'}


def spielen():
    brett = neues_brett()
    spieler = SCHWARZ
    while hat_zug(brett, SCHWARZ) or hat_zug(brett, WEISS):
        if not hat_zug(brett, spieler):
            print(NAMEN[spieler], 'kann nicht ziehen und muss passen.')
            spieler = gegner(spieler)
            continue
        brett_zeigen(brett)
        print(NAMEN[spieler], 'ist am Zug.')
        x = zahl_einlesen('Spalte (1-8): ')
        y = zahl_einlesen('Zeile (1-8): ')
        if not gueltiger_zug(brett, x, y, spieler):
            print('Ungültiger Zug!')
            continue
        zug_ausfuehren(brett, x, y, spieler)
        spieler = gegner(spieler)
    brett_zeigen(brett)
    schwarz, weiss = zaehlen(brett)
    print(f'Endstand: Schwarz {schwarz} : {weiss} Weiß')
    ergebnis = gewinner(brett)
    if ergebnis == 'Unentschieden':
        print('Unentschieden! Keiner hat gewonnen.')
    else:
        print(ergebnis, 'hat gewonnen!')


spielen()
"""

TESTBRETTER4 = TESTBRETTER + """
GIER = brett_aus('SW......',
                 '........',
                 '........',
                 '........',
                 '........',
                 '.WWWS...',
                 '........',
                 '........')

LEERES = brett_aus(*['........'] * 8)
"""

# Komplette Testpartien (Spalte, Zeile im Wechsel; 1-basiert).
# Partie 1: zuerst ungültige Eingaben (abc, 9, 0) und drei ungültige Züge (besetztes Feld 4/4,
# Felder ohne Wirkung 1/1 und 8/8), danach immer der erste gültige Zug in Lesereihenfolge.
# Ergebnis: Schwarz 19 : 45 Weiß, Schwarz muss viermal passen.
PARTIE_LANG = ("abc 9 0 4 4 1 1 8 8 "
               "4 3 3 3 2 3 2 2 2 1 1 1 3 4 3 1 3 2 4 2 4 1 5 1 1 2 1 3 6 5 5 2 6 1 7 1 6 2 5 3 "
               "2 5 2 4 1 5 1 4 3 5 1 6 6 4 6 3 7 3 7 2 8 2 8 1 8 3 8 4 7 4 3 6 7 5 8 5 2 6 3 7 "
               "4 6 5 6 6 6 7 6 8 6 8 7 1 7 2 7 1 8 4 7 5 7 6 7 7 7 7 8 2 8 3 8 4 8 5 8 6 8 8 8").split()
# Partie 2: kürzestmögliches Spiel (e6 f4 e3 f6 g5 d6 e7 f5 c5): Weiß hat danach keinen Stein mehr.
PARTIE_KURZ = "5 6 6 4 5 3 6 6 7 5 4 6 5 7 6 5 3 5".split()
# Partie 3: endet 32 : 32, Weiß muss einmal passen.
PARTIE_REMIS = ("5 6 6 6 4 3 5 3 6 3 3 3 3 4 3 5 2 6 4 6 2 2 3 6 7 6 1 1 2 3 5 7 4 8 1 6 2 1 3 2 "
                "1 7 5 2 6 2 1 4 5 1 7 7 1 3 2 5 3 1 7 2 7 8 8 6 6 4 8 8 2 4 7 3 8 3 4 7 7 4 6 8 "
                "1 5 8 2 8 1 4 2 7 5 5 8 3 7 3 8 8 4 6 1 6 7 7 1 4 1 1 2 8 5 1 8 6 5 2 7 8 7 2 8").split()


def _vorspann(*bausteine):
    return "\n\n".join([CODE_ALLES, *bausteine, TESTBRETTER4])


k = neues_kapitel(
    slug="othello_spiel",
    titel="Challenge 4 – Othello: Das komplette Spiel",
    beschreibung="Spielschleife mit Spielerwechsel, Passen, ungültigen Zügen und Gewinnermeldung",
    quelle="Challenge-Handout",
    teil="challenge",
    icon="🏆")

k.lernziele([
    "Ich kann aus vielen kleinen Funktionen ein ganzes Programm zusammensetzen",
    "Ich kann eine Spielschleife mit Spielerwechsel, Passen und ungültigen Zügen schreiben",
    "Ich kann am Spielende den Endstand und den Gewinner ausgeben",
    "Ich kann mein Programm mit kompletten Testpartien prüfen",
])

# ── Erklärung 1: Der Bauplan ───────────────────────────────────────────────
k.erklaerung("Der Bauplan", r"""
    ## Was du schon hast

    In drei Etappen sind alle Bausteine entstanden. Jetzt fehlt nur noch
    die **Spielschleife**, die sie in der richtigen Reihenfolge aufruft.

    | Funktion | Aufgabe | Etappe |
    |---|---|---|
    | `neues_brett()` | Startbrett anlegen | 1 |
    | `brett_zeigen(brett)` | Brett mit Nummern ausgeben | 1 |
    | `gegner(spieler)` | die andere Farbe | 1 |
    | `im_feld(x, y)` | liegt (x, y) auf dem Brett? | 1 |
    | `umzudrehende(...)` | welche Steine dreht ein Zug um? | 2 |
    | `gueltiger_zug(...)` | dreht der Zug mindestens einen Stein um? | 2 |
    | `zug_ausfuehren(...)` | Stein setzen und umdrehen | 2 |
    | `zahl_einlesen(text)` | 1–8 sicher einlesen, Index zurück | 3 |
    | `hat_zug(brett, spieler)` | gibt es irgendeinen Zug? | 3 |
    | `zaehlen(brett)`, `gewinner(brett)` | Endstand, Gewinner | 3 |

    :::analogie 🎲 Die Spielleitung am Brettspielabend
    Stell dir eine Spielleiterin vor, die selbst nicht mitspielt. In jeder
    Runde macht sie immer dasselbe: Sie schaut, ob überhaupt noch jemand
    ziehen kann. Wenn nicht, verkündet sie das Ergebnis. Sonst prüft sie,
    ob die Person am Zug einen Zug hat – wenn nicht, sagt sie "Du musst
    aussetzen" und gibt weiter. Dann fragt sie nach dem Zug. Ist er nicht
    erlaubt, sagt sie "Nochmal!" und **dieselbe** Person ist wieder dran.
    Ist er erlaubt, wird er ausgeführt und die andere Person ist dran.
    Genau diese Spielleiterin programmierst du jetzt: die Funktion
    `spielen()`. Die Handgriffe (prüfen, umdrehen, zählen) erledigen die
    Hilfsfunktionen.
    :::
    ---
    ## Eine Runde im Überblick

    :::visual ablauf
    {"schritte": [{"icon": "❓", "text": "Kann noch irgendwer ziehen? Sonst: Spielende"},
                  {"icon": "⏭️", "text": "Hat der Spieler am Zug keinen Zug? Dann passen"},
                  {"icon": "🖥️", "text": "Brett zeigen, Spalte und Zeile einlesen"},
                  {"icon": "🚫", "text": "Ungültiger Zug? Meldung, derselbe Spieler nochmal"},
                  {"icon": "🔄", "text": "Zug ausführen, Spieler wechseln"}]}
    :::

    :::visual entscheidung
    {"bedingung": "hat_zug(brett, spieler)",
     "ja": "Brett zeigen, Zug einlesen und prüfen",
     "nein": "Meldung 'muss passen', spieler = gegner(spieler), continue"}
    :::

    `continue` springt sofort zum nächsten Schleifendurchlauf, also wieder
    zur Bedingung oben. Alles, was danach im Schleifenkörper steht, wird in
    dieser Runde übersprungen.
    """)

k.mc("Wie lautet die richtige Bedingung der Spielschleife?",
     ["while hat_zug(brett, SCHWARZ) or hat_zug(brett, WEISS):",
      "while hat_zug(brett, spieler):",
      "while hat_zug(brett, SCHWARZ) and hat_zug(brett, WEISS):",
      "while True:"],
     "Das Spiel läuft weiter, solange **mindestens einer** ziehen kann – also `or`. "
     "Mit `hat_zug(brett, spieler)` wäre das Spiel schon zu Ende, wenn nur der aktuelle "
     "Spieler passen muss. Mit `and` endet es ebenfalls zu früh. `while True` ohne Ausstieg "
     "liefe ewig.")

k.mc("Was soll passieren, wenn jemand einen ungültigen Zug eingibt?",
     ["Meldung ausgeben, und DERSELBE Spieler gibt einen neuen Zug ein",
      "Der andere Spieler ist dran",
      "Das Programm beendet sich",
      "Der Stein wird trotzdem gesetzt"],
     "Ein ungültiger Zug zählt nicht. Darum `continue` **ohne** Spielerwechsel: Die Schleife "
     "beginnt von vorn, und derselbe Spieler wird wieder gefragt.")

k.wf("Nach dem Passen ist derselbe Spieler noch einmal am Zug.", False,
     "Passen heißt aussetzen: `spieler = gegner(spieler)`, dann ist der andere dran. Ohne den "
     "Wechsel würde das Programm endlos \"muss passen\" ausgeben.")

k.ausgabe(r"""
    spieler = 'S'
    for runde in range(5):
        if runde == 2:
            print(spieler, 'passt')
        else:
            print(spieler, 'zieht')
        if spieler == 'S':
            spieler = 'W'
        else:
            spieler = 'S'
    """,
    "Der Spieler wechselt nach JEDER Runde, auch nach dem Passen: S, W, S (passt), W, S.",
    tipp="Gehe die fünf Runden einzeln durch und notiere, wer gerade dran ist.")

k.ausgabe(r"""
    for zahl in [1, 2, 3, 4]:
        if zahl == 2:
            continue
        print(zahl)
    """,
    "Bei `zahl == 2` springt `continue` sofort zum nächsten Durchlauf, `print` wird "
    "übersprungen. Ausgegeben werden 1, 3 und 4.")

# ── Erklärung 2: Die Spielschleife ─────────────────────────────────────────
k.erklaerung("Die Spielschleife schreiben", r"""
    ## Der Ablauf als Code

    Hier ein vereinfachtes Modell der Schleife zum Ausprobieren. Statt
    eines echten Bretts gibt es eine Liste, wer wie oft noch ziehen kann:

    :::trace
    zuege_uebrig = {'S': 1, 'W': 2}
    spieler = 'S'
    while zuege_uebrig['S'] > 0 or zuege_uebrig['W'] > 0:
        if zuege_uebrig[spieler] == 0:
            print(spieler, 'muss passen')
        else:
            print(spieler, 'zieht')
            zuege_uebrig[spieler] -= 1
        spieler = 'W' if spieler == 'S' else 'S'
    print('Spielende')
    :::

    (`'W' if spieler == 'S' else 'S'` ist eine Kurzform von if/else in
    einer Zeile – du kannst genauso gut `gegner(spieler)` schreiben.)

    :::achtung Die drei häufigsten Fehler
      • Passen vergessen: Kann der Spieler am Zug nicht, wartet das
        Programm trotzdem auf seine Eingabe, und jeder Zug ist ungültig.
      • Spielerwechsel beim Passen vergessen: endlose "muss passen"-Meldungen.
      • Schleife nur mit `hat_zug(brett, spieler)`: Das Spiel endet schon,
        wenn der aktuelle Spieler passen müsste.
    :::
    ---
    ## Damit die Tests dein Spiel verstehen

    Die Tests spielen **drei komplette Partien** und geben die Züge über
    `input()` ein. Dafür müssen Eingaben und Meldungen genau festgelegt
    sein:

    | Wann? | Was genau? |
    |---|---|
    | Eingabe | erst Spalte, dann Zeile (je 1–8) mit `zahl_einlesen` |
    | Passen | `Schwarz kann nicht ziehen und muss passen.` (bzw. `Weiß`) |
    | Ungültiger Zug | `Ungültiger Zug!` |
    | Ende | `Endstand: Schwarz 19 : 45 Weiß` |
    | Gewinner | `Weiß hat gewonnen!` bzw. `Schwarz hat gewonnen!` |
    | Gleichstand | `Unentschieden! Keiner hat gewonnen.` |

    Zusätzliche Ausgaben (Brett, "ist am Zug") stören die Tests nicht.

    :::info Selbst spielen
    Speichere dein fertiges Programm als `othello.py` und starte es im
    Terminal mit `python othello.py` (auf den Poolrechnern `python3`).
    Dann kannst du gegen jemanden am selben Rechner spielen.
    :::
    """)

k.mc("Warum steht `zahl_einlesen` VOR der Prüfung mit `gueltiger_zug`?",
     ["Erst muss feststehen, dass Spalte und Zeile Zahlen von 1 bis 8 sind – dann kann man den Zug prüfen",
      "Weil gueltiger_zug sonst zu langsam ist",
      "Die Reihenfolge ist egal",
      "Weil input() nur am Anfang einer Funktion stehen darf"],
     "`zahl_einlesen` sorgt dafür, dass x und y gültige Indizes sind. Erst dann ergibt die "
     "Frage \"Ist dieser Zug erlaubt?\" einen Sinn. Zwei Prüfungen, zwei Ebenen: Eingabe "
     "(Format) und Spielregel (Sandwich).")

k.ausgabe(r"""
    schwarz, weiss = 19, 45
    print(f'Endstand: Schwarz {schwarz} : {weiss} Weiß')
    """,
    "Der f-String setzt die Werte in die geschweiften Klammern ein.")

# ── Praxisteil ─────────────────────────────────────────────────────────────
k.code(r"""
    ## Zugvorschläge

    Für die Spieler wäre eine Hilfe praktisch: "Wo darf ich überhaupt
    setzen?" Schreibe `moegliche_zuege(brett, spieler)`. Die Funktion gibt
    eine Liste aller gültigen Züge als Tupel `(spalte, zeile)` zurück –
    **ab 1 gezählt**, so wie die Spieler sie eintippen. Die Reihenfolge ist
    die Lesereihenfolge: Zeile für Zeile von oben, in jeder Zeile von links.

        moegliche_zuege(neues_brett(), 'S')   →  [(4, 3), (3, 4), (6, 5), (5, 6)]

    Alle bisherigen Funktionen stehen in der Vorlage.
    """,
    [F("moegliche_zuege(neues_brett(), 'S')", [(4, 3), (3, 4), (6, 5), (5, 6)], vorspann=_vorspann()),
     F("moegliche_zuege(neues_brett(), 'W')", vorspann=_vorspann()),
     F("moegliche_zuege(GIER, 'S')", vorspann=_vorspann()),
     F("moegliche_zuege(LEERES, 'S')", [], vorspann=_vorspann())],
    CODE_MOEGLICHE_ZUEGE,
    "Wie `hat_zug`, nur dass die Funktion nicht beim ersten Treffer aufhört, sondern alle "
    "Treffer sammelt. Die äußere Schleife läuft über die Zeilen (y), die innere über die "
    "Spalten (x) – das ergibt die Lesereihenfolge. `+ 1` rechnet die Indizes in die "
    "Spieler-Zählung um.",
    tipps=["Wie hat_zug – aber mit einer Liste statt return True.",
           "Bei jedem gültigen Feld: zuege.append((x + 1, y + 1)).",
           "for y in range(8):\n    for x in range(8):\n        if gueltiger_zug(brett, x, y, spieler):"],
    vorlage=CODE_ALLES + "\n\ndef moegliche_zuege(brett, spieler):\n    zuege = []\n    # …\n"
            "    return zuege\n")

k.puzzle("Bringe den Kern der Spielschleife in die richtige Reihenfolge. Zwei Zeilen gehören "
         "nicht dazu.",
         r"""
         while hat_zug(brett, SCHWARZ) or hat_zug(brett, WEISS):
             if not hat_zug(brett, spieler):
                 print(NAMEN[spieler], 'kann nicht ziehen und muss passen.')
                 spieler = gegner(spieler)
                 continue
             x = zahl_einlesen('Spalte (1-8): ')
             y = zahl_einlesen('Zeile (1-8): ')
             if not gueltiger_zug(brett, x, y, spieler):
                 print('Ungültiger Zug!')
                 continue
             zug_ausfuehren(brett, x, y, spieler)
             spieler = gegner(spieler)
         """,
         "Zuerst wird das Passen behandelt (mit Spielerwechsel und `continue`). Dann wird der "
         "Zug eingelesen und geprüft. Ein ungültiger Zug führt mit `continue` zurück an den "
         "Anfang – OHNE Wechsel. Nur ein ausgeführter Zug wechselt den Spieler.",
         tipp="Was muss passieren, bevor man überhaupt nach einem Zug fragt?",
         ablenker=["while hat_zug(brett, spieler):", "    spieler = SCHWARZ"])

k.code(r"""
    ## Das komplette Spiel

    Jetzt kommt alles zusammen! Schreibe die Funktion `spielen()` und rufe
    sie am Ende des Programms auf. Alle Hilfsfunktionen stehen schon in der
    Vorlage.

    Ablauf: Startbrett anlegen, Schwarz beginnt. Dann wiederholen, solange
    **mindestens einer** ziehen kann:

    | Situation | Was dein Programm tut |
    |---|---|
    | Spieler am Zug kann nicht ziehen | `<Name> kann nicht ziehen und muss passen.` ausgeben, Spieler wechseln, nächste Runde |
    | sonst | Brett zeigen, `<Name> ist am Zug.` ausgeben, `zahl_einlesen('Spalte (1-8): ')`, dann `zahl_einlesen('Zeile (1-8): ')` |
    | Zug ungültig | `Ungültiger Zug!` ausgeben, derselbe Spieler ist nochmal dran |
    | Zug gültig | Zug ausführen, Spieler wechseln |

    Am Ende: Brett zeigen, dann `Endstand: Schwarz <s> : <w> Weiß` und
    `<Gewinner> hat gewonnen!` bzw. `Unentschieden! Keiner hat gewonnen.`
    ausgeben.

    Die Namen sind `Schwarz` und `Weiß` (z. B. über das Dictionary
    `NAMEN = {SCHWARZ: 'Schwarz', WEISS: 'Weiß'}`).

    Die Tests spielen drei komplette Partien: eine lange (mit Tippfehlern,
    ungültigen Zügen und viermal Passen), die kürzestmögliche Partie
    (9 Züge, danach hat Weiß keinen Stein mehr) und eine, die
    unentschieden 32 : 32 endet.
    """,
    [P(PARTIE_LANG,
       erwartet=["Bitte eine Zahl von 1 bis 8 eingeben.", "Ungültiger Zug!",
                 "Schwarz kann nicht ziehen und muss passen.",
                 "Endstand: Schwarz 19 : 45 Weiß", "Weiß hat gewonnen!"],
       nicht=["Unentschieden"], vorspann=CODE_ALLES,
       beschreibung="lange Partie mit Fehleingaben und Passen"),
     P(PARTIE_KURZ, erwartet=["Endstand: Schwarz 13 : 0 Weiß", "Schwarz hat gewonnen!"],
       nicht=["Weiß hat gewonnen", "Unentschieden", "passen"], vorspann=CODE_ALLES,
       beschreibung="kürzeste Partie (9 Züge)"),
     P(PARTIE_REMIS, erwartet=["Weiß kann nicht ziehen und muss passen.",
                               "Endstand: Schwarz 32 : 32 Weiß",
                               "Unentschieden! Keiner hat gewonnen."],
       nicht=["Schwarz hat gewonnen", "Weiß hat gewonnen"], vorspann=CODE_ALLES,
       beschreibung="Partie mit Gleichstand")],
    CODE_SPIELEN,
    "Die Schleifenbedingung mit `or` hält das Spiel am Laufen, solange irgendwer ziehen kann. "
    "Im Körper wird zuerst das Passen erledigt (Wechsel + `continue`), dann der Zug "
    "eingelesen. Ein ungültiger Zug springt mit `continue` zurück, **ohne** den Spieler zu "
    "wechseln. Nach der Schleife stehen Endstand und Gewinner fest. Jede Hilfsfunktion "
    "erledigt eine Kleinigkeit, deshalb bleibt `spielen()` kurz und lesbar.",
    tipps=["Starte mit brett = neues_brett() und spieler = SCHWARZ, dann eine while-Schleife.",
           "while hat_zug(brett, SCHWARZ) or hat_zug(brett, WEISS): … Zuerst: "
           "if not hat_zug(brett, spieler): passen, wechseln, continue.",
           "Nach der Schleife: schwarz, weiss = zaehlen(brett) und "
           "print(f'Endstand: Schwarz {schwarz} : {weiss} Weiß'), dann gewinner(brett) auswerten."],
    vorlage=CODE_ALLES + "\n\nNAMEN = {SCHWARZ: 'Schwarz', WEISS: 'Weiß'}\n\n\ndef spielen():\n"
            "    brett = neues_brett()\n    spieler = SCHWARZ\n"
            "    # Spielschleife, danach Endstand und Gewinner\n\n\nspielen()\n",
    streng=True)

k.code(r"""
    ## Bonus: Ein Computergegner

    Für Neugierige: Lass den Computer einen Zug aussuchen! Schreibe
    `computer_zug(brett, spieler)`. Die Funktion gibt das Feld `(x, y)`
    (ab 0 gezählt) zurück, das **die meisten** Steine umdreht. Bei
    Gleichstand gewinnt das Feld, das in Lesereihenfolge zuerst kommt.
    Gibt es keinen gültigen Zug, gibt sie `None` zurück.

        computer_zug(neues_brett(), 'S')   →  (3, 2)

    Testbrett `GIER`: Oben links dreht ein Zug 1 Stein um, in Zeile 6
    dreht ein Zug 3 Steine um.

        GIER = brett_aus('SW......',
                         '........', '........', '........', '........',
                         '.WWWS...',
                         '........', '........')

    Auf dem leeren Brett `LEERES` gibt es keinen Zug.

    (Mit dieser Funktion kannst du `spielen()` so umbauen, dass Weiß vom
    Computer gespielt wird – das ist aber keine Pflicht.)
    """,
    [F("computer_zug(neues_brett(), 'S')", (3, 2), vorspann=_vorspann()),
     F("computer_zug(GIER, 'S')", (0, 5), vorspann=_vorspann()),
     F("computer_zug(MEHRFACH, 'S')", vorspann=_vorspann()),
     F("computer_zug(LEERES, 'S')", None, vorspann=_vorspann())],
    CODE_COMPUTER_ZUG,
    "Die Funktion merkt sich das bisher beste Feld und dessen Anzahl. Nur ein **echt "
    "besseres** Feld (`>`) ersetzt es, deshalb gewinnt bei Gleichstand das erste. Startet "
    "`beste_anzahl` bei 0, zählen nur Felder, die mindestens einen Stein umdrehen – also "
    "nur gültige Züge. Gibt es keinen, bleibt `bester` bei `None`. Diese \"gierige\" "
    "Strategie ist übrigens nicht besonders klug: Wer gut Othello spielt, nimmt am Anfang "
    "lieber wenige Steine und sichert sich die Ecken.",
    tipps=["Merke dir zwei Dinge: das beste Feld bisher und wie viele Steine es umdreht.",
           "anzahl = len(umzudrehende(brett, x, y, spieler)) für jedes Feld.",
           "if anzahl > beste_anzahl:\n    bester = (x, y)\n    beste_anzahl = anzahl"],
    vorlage=CODE_ALLES + "\n\ndef computer_zug(brett, spieler):\n    bester = None\n"
            "    beste_anzahl = 0\n    # …\n    return bester\n")

k.erklaerung("Wie geht es weiter?", r"""
    ## Geschafft – und jetzt?

    Du hast ein komplettes Spiel aus etwa 100 Zeilen gebaut, mit Listen von
    Listen, Tupeln, Schleifen, Verzweigungen, Funktionen und Eingabeprüfung.
    Das ist genau das, was die Challenge zeigen will: Mit dem Stoff der
    ersten drei Vorkurstage kann man echte Programme schreiben.

    Ideen zum Weiterbauen:
      • Zugvorschläge anzeigen (`moegliche_zuege`) oder auf dem Brett mit
        `*` markieren.
      • Koordinaten wie auf dem echten Brett eingeben: `d3` statt `4` und `3`.
      • Nach jedem Zug den Zwischenstand ausgeben.
      • Gegen den Computer spielen (`computer_zug`).

    :::info Abgabe der Challenge
    Abgegeben wird über **Moodle**, Abschnitt "Programmierchallenge".
    Den genauen Termin findest du dort. Laut Handout freut sich das Team
    über **jede** Abgabe und versucht, zeitnah Feedback zu geben. Bei
    Fragen ist es auch persönlich für euch da.
    :::

    !! Am meisten lernst du, wenn du das Spiel noch einmal ohne Vorlage
    !! selbst schreibst – mit deinen eigenen Namen und deinem eigenen Aufbau.
    """)

k.zusammenfassung(r"""
    ## Das komplette Spiel

        def spielen():
            brett = neues_brett()
            spieler = SCHWARZ
            while hat_zug(brett, SCHWARZ) or hat_zug(brett, WEISS):
                if not hat_zug(brett, spieler):
                    print(NAMEN[spieler], 'kann nicht ziehen und muss passen.')
                    spieler = gegner(spieler)
                    continue
                brett_zeigen(brett)
                x = zahl_einlesen('Spalte (1-8): ')
                y = zahl_einlesen('Zeile (1-8): ')
                if not gueltiger_zug(brett, x, y, spieler):
                    print('Ungültiger Zug!')
                    continue                     # KEIN Spielerwechsel
                zug_ausfuehren(brett, x, y, spieler)
                spieler = gegner(spieler)
            # danach: Endstand mit zaehlen, Gewinner mit gewinner

    | Situation | Reaktion |
    |---|---|
    | keiner kann ziehen | Schleife endet → Endstand, Gewinner |
    | Spieler am Zug kann nicht | passen: wechseln + `continue` |
    | ungültiger Zug | Meldung + `continue` (derselbe Spieler) |
    | gültiger Zug | ausführen, wechseln |

    !! Große Programme = viele kleine, getestete Funktionen + eine kurze Hauptschleife.
    """)
