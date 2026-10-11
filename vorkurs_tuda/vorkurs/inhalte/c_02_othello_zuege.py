# -*- coding: utf-8 -*-
"""Challenge, Etappe 2: Othello – Richtungen, Züge prüfen, Steine umdrehen."""
from ..engine import neues_kapitel, P, F  # noqa: F401
from .c_01_othello_spielfeld import CODE_ETAPPE1, TESTHILFE

CODE_RICHTUNGEN = """\
RICHTUNGEN = [(-1, -1), (0, -1), (1, -1),
              (-1, 0),           (1, 0),
              (-1, 1),  (0, 1),  (1, 1)]
"""

CODE_UMDREHEN_IN_RICHTUNG = """\
def umdrehen_in_richtung(brett, x, y, dx, dy, spieler):
    kandidaten = []
    x = x + dx
    y = y + dy
    while im_feld(x, y) and brett[y][x] == gegner(spieler):
        kandidaten.append((x, y))
        x = x + dx
        y = y + dy
    if im_feld(x, y) and brett[y][x] == spieler:
        return kandidaten
    return []
"""

CODE_UMZUDREHENDE = """\
def umzudrehende(brett, x, y, spieler):
    if not im_feld(x, y) or brett[y][x] != LEER:
        return []
    alle = []
    for dx, dy in RICHTUNGEN:
        alle += umdrehen_in_richtung(brett, x, y, dx, dy, spieler)
    return alle
"""

CODE_GUELTIGER_ZUG = """\
def gueltiger_zug(brett, x, y, spieler):
    return len(umzudrehende(brett, x, y, spieler)) > 0
"""

CODE_ZUG_AUSFUEHREN = """\
def zug_ausfuehren(brett, x, y, spieler):
    steine = umzudrehende(brett, x, y, spieler)
    brett[y][x] = spieler
    for sx, sy in steine:
        brett[sy][sx] = spieler
    return len(steine)
"""

CODE_ETAPPE2 = "\n\n".join([CODE_RICHTUNGEN, CODE_UMDREHEN_IN_RICHTUNG, CODE_UMZUDREHENDE,
                            CODE_GUELTIGER_ZUG, CODE_ZUG_AUSFUEHREN])

# Testbretter (stehen im Vorspann der Tests und werden in den Aufgaben gezeigt)
TESTBRETTER = TESTHILFE + """
RAND = brett_aus('W......S',
                 '......WW',
                 'S.W.....',
                 'SWWW....',
                 '........',
                 '........',
                 '........',
                 '........')

MEHRFACH = brett_aus('.SWW.WWW',
                     '...WW...',
                     '..S.W...',
                     '....W...',
                     '....S...',
                     '........',
                     '........',
                     '........')

DIAGONAL = brett_aus('S......S',
                     '.W....W.',
                     '........',
                     '........',
                     '........',
                     '........',
                     '........',
                     '........')

BESETZT = brett_aus('SWS.....',
                    '........',
                    '........',
                    '........',
                    '........',
                    '........',
                    '........',
                    '........')


def nach_zug(brett, x, y, spieler):
    # Nur für die Tests: Zug ausführen und das Brett danach zurückgeben.
    zug_ausfuehren(brett, x, y, spieler)
    return brett
"""

def _vorspann(*bausteine):
    """Etappe 1 + RICHTUNGEN + bereits geschriebene Funktionen + Testbretter."""
    return "\n\n".join([CODE_ETAPPE1, CODE_RICHTUNGEN, *bausteine, TESTBRETTER])


k = neues_kapitel(
    slug="othello_zuege",
    titel="Challenge 2 – Othello: Züge prüfen & Steine umdrehen",
    beschreibung="Richtungen als Tupel, Schritt für Schritt übers Brett laufen, Sandwiches finden",
    quelle="Challenge-Handout, Vorlesung 4 (vier_in_folge)",
    teil="challenge",
    icon="🧭")

k.lernziele([
    "Ich kann die 8 Richtungen als Tupel (dx, dy) aufschreiben und mit einer for-Schleife durchlaufen",
    "Ich kann von einem Feld aus Schritt für Schritt in eine Richtung laufen, ohne das Brett zu verlassen",
    "Ich kann bestimmen, welche gegnerischen Steine ein Zug umdreht",
    "Ich kann einen Zug auf dem Brett ausführen",
])

# ── Erklärung 1: Richtungen ────────────────────────────────────────────────
k.erklaerung("Acht Richtungen als Tupel", r"""
    ## Eine Richtung ist ein Paar (dx, dy)

    Ein Sandwich kann in 8 Richtungen liegen. Eine Richtung beschreibst du
    mit zwei Zahlen: Wie weit gehst du pro Schritt nach rechts (**dx**) und
    wie weit nach unten (**dy**)? Das "d" steht für "Differenz", also die
    Änderung pro Schritt. Beide Zahlen zusammen speicherst du als **Tupel**
    `(dx, dy)`.

    | | dx = -1 | dx = 0 | dx = 1 |
    |---|---|---|---|
    | dy = -1 | ↖ `(-1, -1)` | ↑ `(0, -1)` | ↗ `(1, -1)` |
    | dy = 0 | ← `(-1, 0)` | Start | → `(1, 0)` |
    | dy = 1 | ↙ `(-1, 1)` | ↓ `(0, 1)` | ↘ `(1, 1)` |

    !! Zeile 1 ist oben. Deshalb heißt dy = -1 "nach oben" und dy = 1 "nach unten".

    Alle 8 Richtungen kommen in eine Liste von Tupeln:

        RICHTUNGEN = [(-1, -1), (0, -1), (1, -1),
                      (-1, 0),           (1, 0),
                      (-1, 1),  (0, 1),  (1, 1)]

    Mit einer for-Schleife gehst du alle durch. Dabei entpackst du jedes
    Tupel direkt in zwei Variablen:

    :::code
    RICHTUNGEN = [(-1, -1), (0, -1), (1, -1), (-1, 0),
                  (1, 0), (-1, 1), (0, 1), (1, 1)]
    for dx, dy in RICHTUNGEN:
        print('dx =', dx, ' dy =', dy)
    :::
    ---
    ## Schritt für Schritt laufen

    :::analogie 🧭 Wandern mit Kompass
    Du stehst auf einem Feld und wählst eine Kompassrichtung, zum Beispiel
    Nordost. Bei jedem Schritt gehst du dx Felder nach rechts und dy Felder
    nach unten: `x = x + dx`, `y = y + dy`. Du läufst so lange weiter,
    wie der Weg es erlaubt. Am Brettrand ist **Wasser**: Dort musst du
    stehen bleiben, sonst gehst du baden (`IndexError`) oder landest wie
    durch Zauberei auf der anderen Seite (negative Indizes!). Für die
    nächste Richtung fängst du wieder beim Startfeld an.
    :::

    :::trace
    x, y = 2, 5
    dx, dy = 1, -1
    for schritt in range(3):
        x = x + dx
        y = y + dy
        print('Schritt', schritt + 1, '-> Feld', x, y)
    :::

    :::info Dieselbe Idee wie in Vorlesung 4
    In Vorlesung 4 (Guter Code) gibt es die Funktion
    `vier_in_folge(x, y, xo, yo)`. Statt einer Funktion für "waagerecht"
    und einer für "senkrecht" gibt es **eine** Funktion mit der Richtung
    als Parameter. Genau so machst du es hier: eine Funktion, die mit
    jeder der 8 Richtungen funktioniert, statt 8 fast gleicher Kopien.
    :::
    """)

k.mc("In welche Richtung zeigt `(0, -1)` auf dem Othello-Brett?",
     ["Nach oben", "Nach unten", "Nach links", "Nach rechts"],
     "dx = 0: keine Bewegung nach links/rechts. dy = -1: die Zeilennummer wird kleiner. "
     "Da Zeile 1 oben ist, geht es nach oben.")

k.wf("Die Richtung `(1, 1)` zeigt nach rechts oben.", False,
     "dx = 1 heißt nach rechts, dy = 1 heißt eine Zeile nach unten (die Zeilen zählen von oben). "
     "`(1, 1)` zeigt also nach rechts **unten**. Nach rechts oben wäre `(1, -1)`.")

k.ausgabe(r"""
    x, y = 4, 4
    dx, dy = -1, 1
    for i in range(2):
        x = x + dx
        y = y + dy
    print(x, y)
    """,
    "Zwei Schritte mit (-1, 1): x wird zweimal um 1 kleiner (4 → 2), y zweimal um 1 größer "
    "(4 → 6). Ergebnis: `2 6`.",
    tipp="Pro Schritt: x + dx, y + dy.")

k.text("Wie viele Tupel stehen in der Liste RICHTUNGEN (ohne (0, 0))?",
       ["8", "acht"],
       "Drei Richtungen nach oben, drei nach unten, links und rechts: 3 + 3 + 2 = 8. "
       "`(0, 0)` wäre keine Richtung, man käme nie vom Fleck.")

k.ausdruck("Schreibe einen Ausdruck für die Spalte, auf der du nach `n` Schritten in Richtung "
           "`dx` stehst, wenn du in Spalte `x` startest.",
           tests=[{"x": 2, "dx": 1, "n": 3}, {"x": 5, "dx": -1, "n": 2},
                  {"x": 4, "dx": 0, "n": 7}, {"x": 0, "dx": 1, "n": 0}],
           loesung="x + n * dx",
           erklaerung="Jeder Schritt addiert dx. Nach n Schritten also `x + n * dx`. "
                      "Genau so rechnet auch `vier_in_folge` aus Vorlesung 4: `x + i * xo`.",
           tipp="Ein Schritt: x + dx. Zwei Schritte: x + 2 * dx. n Schritte: …")

# ── Erklärung 2: Eine Richtung prüfen ─────────────────────────────────────
k.erklaerung("In eine Richtung prüfen", r"""
    ## Erst einmal nur eine Zeile

    Bevor es um das ganze Brett geht, schau dir **eine Zeile** an. Schwarz
    will auf Index 0 setzen und schaut nach rechts:

    :::visual liste
    {"name": "zeile", "werte": [".", "W", "W", "S", "."], "markiert": [1, 2]}
    :::

    Das Vorgehen:
    1. Einen Schritt weitergehen.
    2. **Solange** das Feld auf dem Brett liegt und dort ein gegnerischer
       Stein liegt: den Stein als Kandidat merken und weitergehen.
    3. Danach prüfen: Liegt hier (noch auf dem Brett) ein **eigener**
       Stein? Dann ist das Sandwich komplett, und alle Kandidaten werden
       umgedreht. Sonst wird nichts umgedreht.

    :::trace
    zeile = ['.', 'W', 'W', 'S', '.']
    x = 0
    kandidaten = []
    x = x + 1
    while x < len(zeile) and zeile[x] == 'W':
        kandidaten.append(x)
        x = x + 1
    if x < len(zeile) and zeile[x] == 'S':
        print('Umdrehen:', kandidaten)
    else:
        print('Nichts umdrehen')
    :::
    ---
    ## Die Entscheidung am Ende

    Nach der Schleife stehst du auf dem ersten Feld, das **kein**
    gegnerischer Stein ist. Jetzt entscheidet sich alles:

    :::visual entscheidung
    {"bedingung": "im_feld(x, y) and brett[y][x] == spieler",
     "ja": "Sandwich komplett: return kandidaten",
     "nein": "Kein Sandwich: return []"}
    :::

    | Situation (Zug ganz links, Blick nach rechts) | Ergebnis |
    |---|---|
    | `[neu] W W S` | W, W werden umgedreht |
    | `[neu] W W .` | nichts – Lücke, kein Brot am Ende |
    | `[neu] W W` und dann Brettrand | nichts – kein Brot am Ende |
    | `[neu] S` | nichts – kein Belag dazwischen (Kandidaten leer) |

    :::achtung Erst den Rand prüfen, dann aufs Brett schauen
    In `im_feld(x, y) and brett[y][x] == gegner(spieler)` ist die
    Reihenfolge wichtig. `and` wertet die rechte Seite **nur** aus, wenn
    die linke `True` ist. Liegt (x, y) außerhalb, wird `brett[y][x]` gar
    nicht erst gelesen. Andersherum gäbe es am rechten oder unteren Rand
    einen `IndexError` und am linken oder oberen Rand heimlich falsche
    Treffer über negative Indizes.
    :::

    Die fertige Funktion für das ganze Brett und eine beliebige Richtung
    (dx, dy) schreibst du gleich selbst. Sie gibt die **Liste der
    Koordinaten-Tupel** `(x, y)` zurück, die umgedreht würden.
    """)

k.mc("Schwarz setzt ganz links, rechts daneben liegen: `W W .` – was wird in diese Richtung umgedreht?",
     ["Nichts, weil am Ende kein schwarzer Stein liegt",
      "Beide weißen Steine",
      "Nur der erste weiße Stein",
      "Das leere Feld wird schwarz"],
     "Nach den weißen Steinen kommt ein leeres Feld statt eines eigenen Steins. Das Sandwich "
     "hat nur eine Brotscheibe, also wird in dieser Richtung nichts umgedreht.")

k.ausgabe(r"""
    zeile = ['.', 'W', 'W', 'W']
    x = 1
    kandidaten = []
    while x < len(zeile) and zeile[x] == 'W':
        kandidaten.append(x)
        x = x + 1
    if x < len(zeile) and zeile[x] == 'S':
        print(kandidaten)
    else:
        print([])
    """,
    "Die Schleife sammelt die Indizes 1, 2, 3 und endet bei x = 4, also am Rand. Dort liegt "
    "kein schwarzer Stein (es gibt gar kein Feld mehr), deshalb wird `[]` ausgegeben.",
    tipp="Was steht in x, wenn die Schleife endet?")

k.wf("Bei `a and b` wird b nicht mehr ausgewertet, wenn a schon False ist.", True,
     "Das nennt man Kurzschlussauswertung. Darum schreibt man die Randprüfung `im_feld(x, y)` "
     "zuerst: Ist sie False, wird `brett[y][x]` gar nicht erst gelesen.")

k.mc("Warum ist `brett[y][x]` ohne Randprüfung am LINKEN Rand gefährlich, obwohl kein Fehler kommt?",
     ["x = -1 liefert über den negativen Index das Feld am rechten Rand – ein falscher Treffer",
      "Weil Python bei negativen Zahlen abstürzt",
      "Weil x = -1 automatisch zu 0 wird",
      "Es ist nicht gefährlich, Python prüft den Rand selbst"],
     "Negative Indizes zählen von hinten. `brett[y][-1]` ist das letzte Feld der Zeile. "
     "Das Programm \"sieht\" so einen Stein, der in Wirklichkeit auf der anderen Seite liegt.")

# ── Erklärung 3: Alle Richtungen, gültiger Zug, Zug ausführen ─────────────
k.erklaerung("Alle Richtungen, gültige Züge, Zug ausführen", r"""
    ## Alle 8 Richtungen zusammen

    Ein Zug kann in mehrere Richtungen gleichzeitig Steine umdrehen. Also
    fragst du jede Richtung einzeln und sammelst alle Ergebnisse in einer
    Liste. Zwei Listen verbindest du mit `+` bzw. `+=`:

    :::code
    alle = []
    alle += [(3, 3)]
    alle += []
    alle += [(4, 1), (4, 2)]
    print(alle)
    print(len(alle))
    :::

    Vorher prüfst du noch zwei Dinge: Das Feld muss auf dem Brett liegen
    und **leer** sein. Auf ein besetztes Feld darf man nicht setzen.

        def umzudrehende(brett, x, y, spieler):
            if not im_feld(x, y) or brett[y][x] != LEER:
                return []
            alle = []
            for dx, dy in RICHTUNGEN:
                alle += umdrehen_in_richtung(brett, x, y, dx, dy, spieler)
            return alle
    ---
    ## Gültiger Zug und Zug ausführen

    Ein Zug ist genau dann gültig, wenn er mindestens einen Stein umdreht:

    :::visual funktion
    {"name": "gueltiger_zug", "eingaben": ["brett", "x = 3", "y = 2", "spieler = 'S'"],
     "ausgabe": "True", "innen": "return len(umzudrehende(brett, x, y, spieler)) > 0"}
    :::

    Einen Zug ausführen heißt:

    :::visual ablauf
    {"schritte": [{"icon": "🔍", "text": "Umzudrehende Steine bestimmen (VOR dem Setzen!)"},
                  {"icon": "⚫", "text": "Eigenen Stein auf (x, y) setzen"},
                  {"icon": "🔄", "text": "Jeden Stein aus der Liste umfärben"},
                  {"icon": "🔢", "text": "Anzahl umgedrehter Steine zurückgeben"}]}
    :::

    :::achtung Erst rechnen, dann setzen
    Bestimme die umzudrehenden Steine, **bevor** du den neuen Stein setzt.
    `umzudrehende` verlangt ein leeres Feld. Setzt du zuerst, liefert es
    nur noch `[]`, und es wird nichts umgedreht.
    :::

    Am Anfang hat Schwarz genau vier gültige Züge (x, y ab 0 gezählt):
    `(3, 2)`, `(2, 3)`, `(5, 4)` und `(4, 5)`. Jeder dreht genau einen
    weißen Stein um.
    """)

k.mc("Warum prüft `umzudrehende` zuerst, ob das Feld leer ist?",
     ["Auf ein besetztes Feld darf kein Stein gesetzt werden",
      "Damit Python schneller rechnet",
      "Weil leere Felder nicht auf dem Brett liegen",
      "Das ist nicht nötig, man könnte auch Steine überschreiben"],
     "Nach den Regeln kommt ein neuer Stein immer auf ein **leeres** Feld. Ohne die Prüfung "
     "könnte man einen Stein überschreiben, der irgendwo ein Sandwich schließen würde.")

k.ausgabe(r"""
    alle = []
    for teil in [[(1, 2)], [], [(5, 5), (6, 6)]]:
        alle += teil
    print(alle, len(alle) > 0)
    """,
    "`+=` hängt die Elemente jeder Teilliste an. Die leere Liste ändert nichts. "
    "Am Ende enthält `alle` drei Tupel, `len(alle) > 0` ist `True`.")

k.wf("Ein Zug ist auch gültig, wenn er keinen einzigen Stein umdreht – Hauptsache, das Feld ist leer.",
     False,
     "Ein gültiger Zug muss mindestens ein Sandwich bilden, also mindestens einen Stein "
     "umdrehen. Deshalb gilt: `gueltiger_zug` ⇔ `len(umzudrehende(...)) > 0`.")

k.mc("Was passiert, wenn `zug_ausfuehren` ZUERST den Stein setzt und DANN `umzudrehende` aufruft?",
     ["Es wird nichts umgedreht, weil das Feld schon besetzt ist",
      "Es werden doppelt so viele Steine umgedreht",
      "Python meldet einen SyntaxError",
      "Es funktioniert genauso"],
     "`umzudrehende` gibt für ein besetztes Feld `[]` zurück. Erst rechnen, dann setzen.")

# ── Praxisteil ─────────────────────────────────────────────────────────────
_BRETTER_TEXT = r"""
    Das Testbrett `RAND` steht schon bereit (`brett_aus` macht aus den
    Texten eine Liste von Listen, Zeilen 5 bis 8 sind leer):

        RAND = brett_aus('W......S',     # (1, 0) nach links: Rand! nichts
                         '......WW',     # (5, 1) nach rechts: W W Rand, nichts
                         'S.W.....',     # (3, 2) nach links: W, dann Lücke, nichts
                         'SWWW....',     # (4, 3) nach links: W W W S, umdrehen!
                         '........', ...)
    """

k.code(r"""
    ## Eine Richtung prüfen

    Schreibe `umdrehen_in_richtung(brett, x, y, dx, dy, spieler)`. Die
    Funktion bekommt das Feld (x, y), auf das `spieler` setzen will, und
    eine Richtung (dx, dy). Sie gibt die **Liste der Tupel (x, y)** der
    gegnerischen Steine zurück, die in **dieser einen Richtung** umgedreht
    würden. Ohne komplettes Sandwich gibt sie `[]` zurück.

      • Gehe vom Feld aus Schritt für Schritt in Richtung (dx, dy).
      • Sammle die gegnerischen Steine, solange du auf dem Brett bist.
      • Danach muss (noch auf dem Brett) ein eigener Stein liegen.

    Beispiel mit dem Startbrett: Schwarz setzt auf (3, 2) und schaut nach
    unten (0, 1):

        umdrehen_in_richtung(neues_brett(), 3, 2, 0, 1, 'S')   →  [(3, 3)]

    `gegner`, `im_feld`, `neues_brett` usw. aus Etappe 1 stehen in der
    Vorlage. Die Tests prüfen auch den Brettrand (`RAND`): kein
    `IndexError` und kein "Um-die-Ecke-Schauen" über negative Indizes.
    """ + _BRETTER_TEXT,
    [F("umdrehen_in_richtung(neues_brett(), 3, 2, 0, 1, 'S')", [(3, 3)],
       vorspann=_vorspann()),
     F("umdrehen_in_richtung(neues_brett(), 3, 2, 1, 0, 'S')", [], vorspann=_vorspann()),
     F("sorted(umdrehen_in_richtung(RAND, 4, 3, -1, 0, 'S'))", [(1, 3), (2, 3), (3, 3)],
       vorspann=_vorspann()),
     F("umdrehen_in_richtung(RAND, 3, 2, -1, 0, 'S')", [], vorspann=_vorspann()),
     F("umdrehen_in_richtung(RAND, 5, 1, 1, 0, 'S')", [], vorspann=_vorspann()),
     F("umdrehen_in_richtung(RAND, 1, 0, -1, 0, 'S')", [], vorspann=_vorspann())],
    CODE_UMDREHEN_IN_RICHTUNG,
    "Zuerst einen Schritt gehen. Die while-Schleife sammelt gegnerische Steine, solange das "
    "Feld auf dem Brett liegt. `im_feld` steht vorne, damit `brett[y][x]` nie außerhalb "
    "gelesen wird. Nach der Schleife zählt nur ein eigener Stein auf dem Brett als zweite "
    "Brotscheibe. Typische Fehler: den Rand nicht prüfen (IndexError bzw. falscher Treffer "
    "über `brett[0][-1]`) oder die Kandidaten zurückgeben, ohne den eigenen Stein am Ende "
    "zu prüfen.",
    tipps=["Starte mit einer leeren Liste kandidaten und gehe erst einmal einen Schritt: "
           "x = x + dx, y = y + dy.",
           "while im_feld(x, y) and brett[y][x] == gegner(spieler): … Danach entscheidet "
           "ein if, ob kandidaten oder [] zurückgegeben wird.",
           "if im_feld(x, y) and brett[y][x] == spieler:\n    return kandidaten\nreturn []"],
    vorlage=CODE_ETAPPE1 + "\n\n" + "def umdrehen_in_richtung(brett, x, y, dx, dy, spieler):\n"
            "    kandidaten = []\n    # Schritt für Schritt in Richtung (dx, dy) gehen …\n"
            "    return kandidaten\n")

k.code(r"""
    ## Alle Richtungen

    Schreibe `umzudrehende(brett, x, y, spieler)`. Die Funktion gibt die
    Liste **aller** Steine zurück, die ein Stein von `spieler` auf (x, y)
    umdrehen würde – in allen 8 Richtungen zusammen.

      • Liegt (x, y) nicht auf dem Brett oder ist das Feld nicht `LEER`,
        gibt sie `[]` zurück.
      • Sonst ruft sie `umdrehen_in_richtung` für jede Richtung aus
        `RICHTUNGEN` auf und sammelt alle Ergebnisse in einer Liste.

    Die Reihenfolge der Tupel ist egal (die Tests sortieren).

        umzudrehende(neues_brett(), 3, 2, 'S')   →  [(3, 3)]
        umzudrehende(neues_brett(), 3, 3, 'S')   →  []   (Feld besetzt)

    Die Tests verwenden diese Bretter (Zeilen 6 bis 8 sind leer):

        MEHRFACH = brett_aus(       DIAGONAL = brett_aus(      BESETZT = brett_aus(
            '.SWW.WWW',                 'S......S',                'SWS.....',
            '...WW...',                 '.W....W.',                '........',
            '..S.W...',                 '........',                '........',
            '....W...',                 '........',                '........',
            '....S...', ...)            '........', ...)           '........', ...)

    Bei `MEHRFACH` setzt Schwarz auf (4, 0) und baut gleich drei Sandwiches
    (links, unten, schräg links unten). Rechts liegt nur Weiß bis zum Rand,
    dort wird nichts umgedreht. Bei `BESETZT` ist das Feld (2, 0) schon
    belegt, also gibt es dort keinen Zug.
    """,
    [F("sorted(umzudrehende(neues_brett(), 3, 2, 'S'))", [(3, 3)],
       vorspann=_vorspann(CODE_UMDREHEN_IN_RICHTUNG)),
     F("umzudrehende(neues_brett(), 0, 0, 'S')", [], vorspann=_vorspann(CODE_UMDREHEN_IN_RICHTUNG)),
     F("sorted(umzudrehende(MEHRFACH, 4, 0, 'S'))", vorspann=_vorspann(CODE_UMDREHEN_IN_RICHTUNG)),
     F("sorted(umzudrehende(DIAGONAL, 2, 2, 'S'))", [(1, 1)],
       vorspann=_vorspann(CODE_UMDREHEN_IN_RICHTUNG)),
     F("sorted(umzudrehende(DIAGONAL, 5, 2, 'S'))", [(6, 1)],
       vorspann=_vorspann(CODE_UMDREHEN_IN_RICHTUNG)),
     F("umzudrehende(BESETZT, 2, 0, 'S')", [], vorspann=_vorspann(CODE_UMDREHEN_IN_RICHTUNG)),
     F("umzudrehende(neues_brett(), 9, 2, 'S')", [], vorspann=_vorspann(CODE_UMDREHEN_IN_RICHTUNG))],
    CODE_UMZUDREHENDE,
    "Erst die Sonderfälle: außerhalb oder besetzt → `[]`. Dann für jede der 8 Richtungen "
    "die Teilliste holen und mit `+=` an `alle` anhängen. Wer Richtungen vergisst (z. B. die "
    "Diagonalen), scheitert am Brett `DIAGONAL`. Wer die Leer-Prüfung vergisst, scheitert "
    "an `BESETZT`.",
    tipps=["Zwei Teile: zuerst ein if für die Sonderfälle, dann eine for-Schleife über RICHTUNGEN.",
           "for dx, dy in RICHTUNGEN: … alle += umdrehen_in_richtung(…)",
           "if not im_feld(x, y) or brett[y][x] != LEER:\n    return []"],
    vorlage=CODE_ETAPPE1 + "\n\n" + CODE_RICHTUNGEN + "\n\n" + CODE_UMDREHEN_IN_RICHTUNG +
            "\n\ndef umzudrehende(brett, x, y, spieler):\n    alle = []\n    # …\n    return alle\n")

k.luecke("Ergänze `gueltiger_zug`: Ein Zug ist gültig, wenn er mindestens einen Stein umdreht.",
         r"""
         def gueltiger_zug(brett, x, y, spieler):
             return ___(umzudrehende(brett, x, y, spieler)) ___ 0
         """,
         [["len"], [">", "!="]],
         "`umzudrehende` liefert eine Liste. Ist sie nicht leer (Länge > 0), dreht der Zug "
         "etwas um und ist gültig. Der Vergleich liefert direkt `True` oder `False`, ein "
         "if ist nicht nötig.",
         tipp="Wie bekommst du die Anzahl der Elemente einer Liste?")

k.code(r"""
    ## Einen Zug ausführen

    Schreibe `zug_ausfuehren(brett, x, y, spieler)`. Die Funktion
      1. bestimmt mit `umzudrehende` die Steine, die umgedreht werden,
      2. setzt den Stein von `spieler` auf (x, y),
      3. färbt alle Steine aus der Liste in die Farbe von `spieler` um,
      4. gibt die **Anzahl** der umgedrehten Steine zurück.

    Die Funktion verändert das übergebene Brett direkt (Listen sind
    veränderbar), sie muss kein neues Brett zurückgeben. Du darfst davon
    ausgehen, dass der Zug gültig ist.

        b = neues_brett()
        zug_ausfuehren(b, 3, 2, 'S')    →  1
        b[2][3], b[3][3]                →  'S', 'S'

    Der Test-Helfer `nach_zug(brett, x, y, spieler)` ruft deine Funktion
    auf und gibt danach das ganze Brett zum Vergleichen zurück.
    """,
    [F("zug_ausfuehren(neues_brett(), 3, 2, 'S')", 1,
       vorspann=_vorspann(CODE_UMDREHEN_IN_RICHTUNG, CODE_UMZUDREHENDE, CODE_GUELTIGER_ZUG)),
     F("nach_zug(neues_brett(), 3, 2, 'S')",
       vorspann=_vorspann(CODE_UMDREHEN_IN_RICHTUNG, CODE_UMZUDREHENDE, CODE_GUELTIGER_ZUG)),
     F("nach_zug(neues_brett(), 2, 4, 'W')",
       vorspann=_vorspann(CODE_UMDREHEN_IN_RICHTUNG, CODE_UMZUDREHENDE, CODE_GUELTIGER_ZUG)),
     F("zug_ausfuehren(MEHRFACH, 4, 0, 'S')",
       vorspann=_vorspann(CODE_UMDREHEN_IN_RICHTUNG, CODE_UMZUDREHENDE, CODE_GUELTIGER_ZUG)),
     F("nach_zug(MEHRFACH, 4, 0, 'S')",
       vorspann=_vorspann(CODE_UMDREHEN_IN_RICHTUNG, CODE_UMZUDREHENDE, CODE_GUELTIGER_ZUG))],
    CODE_ZUG_AUSFUEHREN,
    "Die Reihenfolge ist entscheidend: Erst die Liste bestimmen (das Feld ist noch leer), "
    "dann setzen, dann umfärben. In der Schleife entpackt `for sx, sy in steine` jedes "
    "Tupel. Beim Schreiben gilt wieder `brett[sy][sx]` – erst die Zeile!",
    tipps=["Speichere zuerst steine = umzudrehende(brett, x, y, spieler).",
           "Danach brett[y][x] = spieler und eine for-Schleife über steine.",
           "for sx, sy in steine:\n    brett[sy][sx] = spieler\nreturn len(steine)"],
    vorlage=CODE_ETAPPE1 + "\n\n" + CODE_RICHTUNGEN + "\n\n" + CODE_UMDREHEN_IN_RICHTUNG +
            "\n\n" + CODE_UMZUDREHENDE + "\n\n" + CODE_GUELTIGER_ZUG +
            "\n\ndef zug_ausfuehren(brett, x, y, spieler):\n    # 1. bestimmen, 2. setzen, "
            "3. umfärben, 4. Anzahl zurückgeben\n    ...\n")

k.zusammenfassung(r"""
    ## Züge prüfen & Steine umdrehen

    | Richtung | Tupel (dx, dy) |
    |---|---|
    | rechts / links | `(1, 0)` / `(-1, 0)` |
    | unten / oben | `(0, 1)` / `(0, -1)` |
    | diagonal | `(1, 1)`, `(-1, -1)`, `(1, -1)`, `(-1, 1)` |

    Eine Richtung prüfen (Sandwich suchen):

        def umdrehen_in_richtung(brett, x, y, dx, dy, spieler):
            kandidaten = []
            x = x + dx
            y = y + dy
            while im_feld(x, y) and brett[y][x] == gegner(spieler):
                kandidaten.append((x, y))
                x = x + dx
                y = y + dy
            if im_feld(x, y) and brett[y][x] == spieler:
                return kandidaten
            return []

      • `umzudrehende`: Feld leer? Dann alle 8 Richtungen mit `+=` sammeln.
      • `gueltiger_zug`: `len(umzudrehende(...)) > 0`.
      • `zug_ausfuehren`: erst bestimmen, dann setzen, dann umfärben.

    !! Randprüfung immer zuerst: `im_feld(x, y) and brett[y][x] ...`
    """)
