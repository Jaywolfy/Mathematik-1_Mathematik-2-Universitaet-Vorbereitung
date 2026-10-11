# -*- coding: utf-8 -*-
"""Kapitel: Wie Computer 'denken' – Programme & Python (Vorlesung 0 + Vorlesung 1, Teil 1)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="computer",
    titel="Wie Computer 'denken' – Programme & Python",
    beschreibung="Was ist ein Programm? Was ist Python? Konsole, Dateien und Hilfe.",
    quelle="Vorlesung 0, Vorlesung 1",
    teil="tag1",
    icon="💻")

k.lernziele([
    "Ich kann erklären, was ein Programm ist und warum ein Computer eine Programmiersprache braucht",
    "Ich kann beschreiben, wie Quelltext über den Python-Interpreter zum Computer gelangt",
    "Ich kann die Python-Konsole starten, darin rechnen und sie wieder beenden",
    "Ich kann ein kleines Programm mit print() schreiben und als Datei ausführen",
    "Ich weiß, was ich tue, wenn ich nicht weiterkomme",
])

# ── Erklärung 1: Vorkurs, Computer, Programme ─────────────────────────────
k.erklaerung("Was ist ein Computer – und was ist ein Programm?", r"""
    ## Willkommen im Programmiervorkurs!

    Vorwissen brauchst du keins – außer, dass du schon mal einen PC bedient
    hast. Im Vorkurs lernst du die wichtigsten Grundkonzepte von Programmen:

    | Tag | Themen in der Vorlesung | Hier im Quiz |
    |---|---|---|
    | Montag | Einführung, Ein-/Ausgabe, Variablen, Operatoren | Tag 1 |
    | Dienstag | Logik, Verzweigungen, Listen, Slices, Schleifen (Teil 1) | Tag 2 |
    | Mittwoch | Schleifen (Teil 2), Tupel, Dictionaries, Dateien, Funktionen | Tag 3 |
    | Donnerstag | Rekursion, Ausblick | Tag 4 |
    | Freitag | Programmierchallenge | Challenge |

    Jeden Tag gibt es vormittags die **Vorlesung** und nachmittags die
    **Übung**, in der Tutorinnen und Tutoren dir helfen.

    Warum **Python** und nicht Java? Die Gründe aus der Vorlesung:
      1. Python ist sehr einfach zu lernen.
      2. Die Installation ist ebenfalls relativ einfach.
      3. Du brauchst Python sehr wahrscheinlich irgendwann im Studium.

    !! Frag gern! Im Moodle-Forum sehen auch andere deine Frage und die Antwort.
    ---
    ## Der Computer – ein superschneller, aber phantasieloser Koch

    :::analogie 👨‍🍳 Der Computer in der Küche
    Stell dir einen Koch vor, der kein Deutsch und kein Englisch versteht.
    Er kann nur ganz exakte Anweisungen ausführen, **eine nach der anderen**,
    dafür aber Milliarden pro Sekunde.

      • Das **Rezept** ist dein **Programm**.
      • Die feste Schreibweise des Rezepts ist die **Programmiersprache**.
      • Ein **Dolmetscher** übersetzt dein Rezept Zeile für Zeile für den
        Koch. Das ist der **Python-Interpreter**.
      • Steht im Rezept „Salz“, obwohl du Zucker meintest, nimmt der Koch Salz.
    :::

    Genau so beschreibt die Vorlesung Computer:
      • Computer sprechen keine natürlichen Sprachen.
      • Computer sind rein-mathematische Maschinen.
      • Computer rechnen Arbeitsschritt für Arbeitsschritt.
      • Computer sind extrem schnell ... also wirklich schnell.

    !! Ein Computer macht IMMER genau das, was du schreibst – nicht das, was du meinst.
    ---
    ## Was ist ein Programm?

    Ein **Programm** ist eine Abfolge von Arbeitsschritten in einer fest
    definierten Schreibweise – wie ein Kochrezept:

    | Rezept „Spiegelei“ | im Programm |
    |---|---|
    | 1. Pfanne erhitzen | Schritt 1 |
    | 2. Öl hineingeben | Schritt 2 |
    | 3. Ei aufschlagen | Schritt 3 |
    | 4. 4 Minuten warten | Schritt 4 |

    Die genaue Schreibweise legt die **Programmiersprache** fest. Es gibt
    unzählige davon (Python, Java, C, Haskell, ...) – es gibt nicht DIE
    eine Programmiersprache. Im Vorkurs benutzen wir **Python**.
    ---
    ## Vom Quelltext zum Computer

    Ein Python-Programm ist einfach nur Text. Diesen Text nennt man
    **Quelltext** (englisch: Source Code). Der **Python-Interpreter** ist
    ein Programm, das deinen Quelltext liest und in Anweisungen übersetzt,
    die der Computer ausführen kann.

    :::visual ablauf
    {"schritte": [{"icon": "👩‍💻", "text": "Der Mensch schreibt Python-Quelltext"},
                  {"icon": "🐍", "text": "Python übersetzt ihn in Anweisungen"},
                  {"icon": "💻", "text": "Der Computer führt die Anweisungen aus"}]}
    :::

    Probier es aus – drück auf „Ausführen“:

    :::code
    print("Hallo, Welt!")
    print(1 + 2 * 3)
    :::
    """)

k.mc("Womit vergleicht die Vorlesung ein Programm?",
     ["Mit einem Kochrezept",
      "Mit einem Bauplan für ein Haus aus Lego",
      "Mit einer Landkarte",
      "Mit einem Wörterbuch"],
     "Ein Programm ist eine Abfolge von Arbeitsschritten in fest definierter "
     "Schreibweise – genau wie ein Kochrezept.")

k.wf("Ein Computer versteht direkt natürliche Sprachen wie Deutsch oder Englisch.", False,
     "Computer sprechen keine natürlichen Sprachen. Sie sind rein-mathematische "
     "Maschinen. Deshalb brauchen wir Programmiersprachen mit fester Schreibweise.")

k.wf("Es gibt genau eine richtige Programmiersprache, die alle benutzen.", False,
     "Es gibt unzählige Programmiersprachen (Python, Java, C, Haskell, ...). "
     "Es gibt nicht DIE eine Programmiersprache.")

k.wf("Ein Computer arbeitet Arbeitsschritt für Arbeitsschritt.", True,
     "Richtig – ein Schritt nach dem anderen, aber extrem schnell.")

k.mc("Wie nennt man den Text, den du beim Programmieren schreibst?",
     ["Quelltext (Source Code)",
      "Maschinentext",
      "Binärbrief",
      "Lochkartentext"],
     "Python-Programme bestehen aus Text, der interpretiert wird. Diesen Text "
     "nennt man Quelltext oder auf Englisch Source Code.")

k.mc("Was macht der Python-Interpreter?",
     ["Er liest deinen Quelltext und übersetzt ihn in Anweisungen für den Computer",
      "Er übersetzt deinen Code ins Englische",
      "Er speichert deinen Code im Internet",
      "Er malt deinen Code bunt an"],
     "Mensch schreibt Quelltext → Python übersetzt ihn → Computer führt aus. "
     "Der Interpreter ist wie ein Dolmetscher.")

# ── Erklärung 2: Konsole und Dateien ─────────────────────────────────────
k.erklaerung("Python benutzen: Konsole und Datei", r"""
    ## Weg 1: Die Python-Konsole (zum Ausprobieren)

    Du startest Python im Terminal. Auf den Poolrechnern der Uni (und meist
    auf macOS/Linux) heißt der Befehl `python3`, unter Windows meist
    `python` oder `py`. Die Konsole erkennst du an `>>>`:

        > python3
        Python 3.13.7 ...
        Type "help" for more information.
        >>> print("Hello, World!")
        Hello, World!
        >>> 1 + 2 * 3
        7
        >>> 1e6
        1000000.0

    In der Konsole zeigt Python den Wert jedes Ausdrucks sofort an – wie ein
    Taschenrechner, der direkt antwortet.

    ## Die Konsole wieder verlassen

    | Wie? | Wo? |
    |---|---|
    | `exit()` eintippen | überall |
    | Strg + D | Linux und macOS |
    | Strg + Z, danach Enter | Windows |

    Nicht verwechseln: **Strg + C** bricht ein laufendes Programm ab, das
    „hängt“ – die Konsole selbst bleibt dabei offen.
    ---
    ## Weg 2: Ein Programm als Datei

    Für richtige Programme schreibst du den Quelltext in eine Datei, z. B.
    `hallo.py`, und startest sie im Terminal (nicht in der `>>>`-Konsole!):

        python3 hallo.py

    Zum Schreiben reicht ein ganz normaler Texteditor. Von einer großen
    Entwicklungsumgebung (IDE) rät der Vorkurs eher ab – ohne Helfer lernst
    du mehr.

    :::vergleich Konsole >>> | Datei hallo.py
    Ein Ausdruck wird sofort angezeigt:
        >>> 5 + 3
        8
    |||
    Ein Ausdruck allein zeigt NICHTS an:
        5 + 3
        print(5 + 3)
    Nur die zweite Zeile gibt 8 aus.
    :::

    :::achtung Konsole und Terminal verwechselt
    `python3 hallo.py` gehört ins normale Terminal. Tippst du es hinter
    `>>>`, meldet Python einen SyntaxError. Umgekehrt versteht das normale
    Terminal kein `print(...)` – dafür musst du erst Python starten.
    :::
    """)

k.mc("Woran erkennst du, dass du in der interaktiven Python-Konsole bist?",
     [">>>", "C:\\>", "$", "###"],
     "Die Python-Konsole zeigt >>> als Eingabeaufforderung. Dort kannst du "
     "einzelne Befehle direkt ausprobieren.")

k.text("Welchen Befehl tippst du auf den Poolrechnern der Uni ins Terminal, um Python zu starten?",
       ["python3"],
       "Auf den Poolrechnern (und meist auf Mac/Linux) heißt der Befehl python3. "
       "Unter Windows heißt er meistens einfach python (oder py).",
       tipp="Es ist 'python' plus die Hauptversionsnummer.")

k.mc("Welche zwei Arten gibt es, Python-Code auszuführen?",
     ["Direkt in der Python-Konsole oder als Datei, die an Python übergeben wird",
      "Nur über das Internet oder per E-Mail",
      "Nur mit einer teuren Entwicklungsumgebung (IDE)",
      "Nur auf Lochkarten"],
     "Zum Ausprobieren: Konsole (>>>). Für richtige Programme: eine .py-Datei, "
     "z.B. 'python3 hallo.py'.")

k.mc("Du bist in der Python-Konsole (>>>) und willst sie verlassen. Was funktioniert auf JEDEM Betriebssystem?",
     ["exit() eintippen und Enter drücken",
      "Strg + S drücken",
      "close eintippen",
      "Das Fenster mit Alt + Tab wechseln"],
     "exit() beendet die Konsole überall. Zusätzlich gibt es Tastenkürzel: "
     "Strg + D unter Linux/macOS, Strg + Z und Enter unter Windows.")

k.wf("Steht in einer Datei hallo.py nur die Zeile   5 + 3   , dann zeigt Python beim Ausführen 8 an.",
     False,
     "Nur die Konsole (>>>) zeigt Werte von Ausdrücken automatisch an. In einer "
     "Datei rechnet Python zwar 5 + 3 aus, zeigt aber nichts an. Dafür brauchst "
     "du print(5 + 3).")

k.mc("Dein Programm 'hängt' im Terminal und hört nicht auf. Was drückst du?",
     ["Strg + C", "Strg + S", "Alt + Tab", "Strg + V"],
     "Mit Strg + C bricht man die Ausführung eines Programms im Terminal ab.")

k.ausgabe('print("Hello, World!")',
          "print() gibt den Text zwischen den Anführungszeichen aus – "
          "die Anführungszeichen selbst werden nicht mit ausgegeben.")

k.ausgabe("print(1 + 2 * 3)",
          "Punkt vor Strich gilt auch in Python: erst 2 * 3 = 6, dann 1 + 6 = 7.")

# ── Erklärung 3: Geschichte und Hilfe ────────────────────────────────────
k.erklaerung("Ein bisschen Geschichte – und Hilfe, wenn es hakt", r"""
    ## Ein bisschen Geschichte

    Die Folien zeigen ein paar Stationen der Computergeschichte:
      • Früher wurden Programme auf **Lochkarten** gestanzt und von einem
        Lochkartenleser eingelesen – jedes Loch war eine Information.
      • Konrad Zuse baute die **Z3** (1941) – den ersten funktionsfähigen,
        frei programmierbaren Digitalrechner der Welt.
      • 1957 füllten Computer noch ganze Räume („Rechenzentren“).
      • **Margaret Hamilton** leitete die Entwicklung der Software für die
        Apollo-11-Mission (Mondlandung 1969). Berühmt ist das Foto, auf dem
        sie neben einem Stapel Programmcode steht, der so groß ist wie sie.
    ---
    ## Wenn du nicht weiterkommst

    Die Empfehlung aus dem Vorkurs, in dieser Reihenfolge:

    :::visual ablauf
    {"schritte": [{"icon": "🔍", "text": "Fehlermeldung nochmal genau lesen"},
                  {"icon": "📚", "text": "In der Vorlesung nach einer Lösung suchen"},
                  {"icon": "🌐", "text": "Mit einer Suchmaschine suchen (nicht mit KI!)"},
                  {"icon": "🙋", "text": "Eine Tutorin oder einen Tutor fragen"}]}
    :::

    Python hat außerdem eine eingebaute Hilfe:
      • `help(print)` zeigt die Dokumentation zu `print`.
      • `help()` startet die interaktive Hilfe mit dem Prompt `help>`. Dort
        tippst du einen Begriff ein, z. B. `print`.
      • Eine lange Hilfeseite schließt du mit **q**. Die interaktive Hilfe
        verlässt du mit `quit` (oder Enter in einer leeren Zeile).

    :::info Warum nicht einfach KI fragen?
    Im Vorkurs (und an der Uni im Normalfall) ist KI nicht erlaubt. Du bist
    hier, um es SELBST zu lernen – und KI macht immer noch häufig Fehler.
    :::
    """)

k.mc("Wer leitete die Entwicklung der Software für die Apollo-11-Mondlandung?",
     ["Margaret Hamilton", "Konrad Zuse", "Ada Lovelace", "Alan Turing"],
     "Margaret Hamilton – das Foto mit dem riesigen Stapel Programmcode ist berühmt.")

k.mc("Welchen Rechner baute Konrad Zuse?",
     ["Die Z3", "Den Apple I", "Den ENIAC", "Die Lochkarte"],
     "Die Z3 (1941) gilt als erster funktionsfähiger, frei programmierbarer "
     "Digitalrechner der Welt.")

k.text("Welche eingebaute Funktion zeigt dir im Python-Interpreter die Dokumentation an?",
       ["help", "help()"],
       "help() – z.B. help(print) erklärt dir die print-Funktion. Ohne Argument "
       "startet help() die interaktive Hilfe mit dem Prompt help>.",
       tipp="Englisch für 'Hilfe'.")

k.mc("Du liest mit help(print) die Hilfeseite. Mit welcher Taste schließt du sie wieder?",
     ["q", "x", "Esc", "Entf"],
     "Die Hilfeseite wird in einem Anzeigeprogramm geöffnet. Unten steht "
     "'(press h for help or q to quit)': mit q kommst du zurück.")

k.mc("Du bekommst eine Fehlermeldung. Was ist laut Vorkurs der ERSTE Schritt?",
     ["Die Fehlermeldung nochmal genau lesen",
      "Sofort einen Tutor fragen",
      "Die KI fragen",
      "Den Computer neu starten"],
     "Reihenfolge: 1. Fehlermeldung genau lesen, 2. in der Vorlesung suchen, "
     "3. Suchmaschine, 4. Tutor fragen.")

# ── Praxisteil ───────────────────────────────────────────────────────────
k.puzzle("Bringe das Spiegelei-Rezept in die richtige Reihenfolge. Das Programm "
         "soll die vier Schritte nummeriert von 1 bis 4 ausgeben.",
         """
         print("1. Pfanne erhitzen")
         print("2. Öl hineingeben")
         print("3. Ei aufschlagen")
         print("4. Vier Minuten warten")
         """,
         "Der Computer führt die Zeilen genau in der Reihenfolge aus, in der sie "
         "dastehen – wie ein Koch, der das Rezept von oben nach unten abarbeitet.",
         tipp="Python liest von oben nach unten. Die Nummern im Text helfen dir.",
         ablenker=['print("Ei essen")'])

k.code(r"""
    ## Dein erstes Programm

    Schreibe ein Programm, das genau diese zwei Zeilen ausgibt:

        Hallo, Welt!
        Ich lerne Python.

    Achte auf Komma, Leerzeichen und Punkt.
    """,
    [P(exakt=["Hallo, Welt!", "Ich lerne Python."], beschreibung="genau diese zwei Zeilen"),
     P(erwartet=["Hallo, Welt!"], beschreibung="erste Zeile"),
     P(nicht=['"', "print"], beschreibung="keine Anführungszeichen und kein 'print' in der Ausgabe")],
    """
    print("Hallo, Welt!")
    print("Ich lerne Python.")
    """,
    "Jedes print() gibt eine eigene Zeile aus. Der Text steht in Anführungszeichen, "
    "damit Python weiß: Das ist Text und kein Befehl. Die Anführungszeichen selbst "
    "werden nicht ausgegeben.",
    tipps=["Du brauchst zwei Aufrufe von print().",
           "Text gehört in Anführungszeichen: print(\"...\")",
           "print(\"Hallo, Welt!\") und darunter print(\"Ich lerne Python.\")"],
    streng=True)

k.code(r"""
    ## Python als Taschenrechner

    Lass Python die beiden Rechnungen ausrechnen und gib die Ergebnisse
    untereinander aus:

        1 + 2 * 3
        (1 + 2) * 3

    Erwartete Ausgabe:

        7
        9

    Wichtig: Python soll rechnen – die Ergebnisse 7 und 9 darfst du nicht
    selbst eintippen.
    """,
    [P(exakt=["7", "9"], beschreibung="beide Ergebnisse untereinander"),
     P(erwartet=["9"], beschreibung="mit Klammern kommt 9 heraus")],
    """
    print(1 + 2 * 3)
    print((1 + 2) * 3)
    """,
    "In print() darf eine Rechnung stehen. Python rechnet sie aus und gibt das "
    "Ergebnis aus. Ohne Klammern gilt Punkt vor Strich (7), mit Klammern wird "
    "zuerst addiert (9).",
    verboten=["7", "9"],
    tipps=["Schreib die Rechnung direkt in die Klammern von print().",
           "Für die zweite Rechnung brauchst du Klammern um 1 + 2.",
           "print(1 + 2 * 3) und print((1 + 2) * 3)"])

k.zusammenfassung(r"""
    ## Das Wichtigste aus Kapitel 1

      • Ein **Programm** ist eine Abfolge von Arbeitsschritten in fester
        Schreibweise – wie ein Kochrezept.
      • Der Computer macht genau das, was dasteht, Schritt für Schritt.
      • **Quelltext** = der Text, den du schreibst. Der **Interpreter**
        übersetzt ihn für den Computer.

    | Was? | Wie? |
    |---|---|
    | Python starten (Pool, macOS, Linux) | `python3` |
    | Python starten (Windows) | `python` oder `py` |
    | Datei ausführen | `python3 hallo.py` (im Terminal) |
    | Konsole beenden | `exit()`, Strg + D (Linux/macOS), Strg + Z + Enter (Windows) |
    | Laufendes Programm abbrechen | Strg + C |
    | Hilfe | `help(print)`, Hilfeseite mit q schließen |

    !! In der Konsole erscheinen Werte automatisch, in einer Datei nur mit print().

        print("Hallo, Welt!")
        print(1 + 2 * 3)      # 7

    Wenn du nicht weiterkommst: Fehlermeldung lesen → Vorlesung → Suchmaschine
    → Tutorin oder Tutor fragen.
    """)
