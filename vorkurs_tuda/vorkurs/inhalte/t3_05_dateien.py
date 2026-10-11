# -*- coding: utf-8 -*-
"""Kapitel: Dateien lesen & schreiben (Vorlesung 3, Folien 27–35; Livecoding 3.3)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="dateien",
    titel="Dateien lesen & schreiben",
    beschreibung="open(), Modi r/w/a/x, read(), readlines(), write(), close(), with, CSV",
    quelle="Vorlesung 3, Livecoding 3",
    teil="tag3",
    icon="📁")

k.lernziele([
    "Ich kann eine Datei mit open() und dem passenden Modus (r, w, a, x) öffnen",
    "Ich kann eine Datei mit read(), readline() und readlines() lesen und Zeilen mit strip() säubern",
    "Ich kann mit write() Text in eine Datei schreiben und weiß, dass ich '\\n' selbst setzen muss",
    "Ich kann mit with dafür sorgen, dass eine Datei automatisch geschlossen wird",
    "Ich kann einfache CSV-Zeilen schreiben und mit split(',') wieder zerlegen",
])


def _datei_pruefen(name, soll_zeilen):
    """Nachspann: liest die Datei und vergleicht sie zeilenweise mit soll_zeilen."""
    return f'''
import os as _os
if not _os.path.exists({name!r}):
    print("PRÜFUNG: Die Datei {name} wurde nicht gefunden!")
else:
    with open({name!r}, encoding="utf-8", errors="replace") as _f:
        _ist = [_z.rstrip() for _z in _f.read().splitlines()]
    while _ist and _ist[-1] == "":
        _ist.pop()
    _soll = {list(soll_zeilen)!r}
    if _ist == _soll:
        print("PRÜFUNG: Datei korrekt")
    else:
        print("PRÜFUNG: Inhalt stimmt nicht.")
        print("Erwartet:", _soll)
        print("Gefunden:", _ist)
'''


def _datei_anlegen(name, inhalt):
    """Vorspann: legt eine Datei mit dem gegebenen Inhalt an."""
    return f"with open({name!r}, 'w', encoding='utf-8') as _f:\n    _f.write({inhalt!r})\n"


# ── Erklärung 1: Öffnen und Modi ─────────────────────────────────────────
k.erklaerung("Dateien öffnen", r"""
    ## Warum Dateien?

    Mit `print()` und `input()` reden wir mit der Konsole. Variablen leben aber
    nur, solange das Programm läuft. Um Daten **permanent** zu speichern oder
    aus Dateien zu lesen, braucht man **Dateien**.

    :::analogie 📓 Tafel und Notizbuch
    Variablen sind wie eine **Tafel**: Nach dem Unterricht wird sie gewischt.
    Eine Datei ist ein **Notizbuch**: Es liegt morgen noch da.
      • `open(...)` heißt: das Notizbuch aufschlagen. Dabei sagst du, was du vorhast (der Modus).
      • `'r'` (read): nur lesen. Gibt es das Heft nicht, kannst du nichts lesen (`FileNotFoundError`).
      • `'w'` (write): ein **leeres** Blatt nehmen. Was vorher drinstand, wird herausgerissen!
      • `'a'` (append): hinten weiterschreiben, wie beim Tagebuch.
      • `'x'`: ein neues Heft anlegen, aber nur, wenn es noch keins gibt.
      • `close()`: das Heft zuklappen, damit die Tinte trocknet. Sonst können Einträge verloren gehen.
    :::
    ---
    ## Eine Datei öffnen

        f = open('<pfad>', '<modus>')
        f = open('main.py', 'r')       # Beispiel: main.py zum Lesen öffnen
        f = open('main.py')            # ohne Modus: Standard ist 'r'

      • Der Pfad kann **relativ** (`'daten.txt'`) oder **absolut**
        (`'C:/Users/anna/daten.txt'`) angegeben werden.
      • Ein relativer Pfad bezieht sich auf den Ordner, in dem dein Programm
        **ausgeführt** wird.

    :::achtung Beachtet, in welchem Ordner euer Programm ausgeführt wird!
    Liegt `daten.txt` in einem anderen Ordner als gedacht, gibt es beim Lesen
    einen `FileNotFoundError`. Das Livecoding sagt kurz: „Pfad muss richtig sein!“
    :::

    :::info So ist es hier im Quiz
    Jedes Programm im Quiz läuft in einem **leeren Ordner**. Deshalb legen die
    Beispiele ihre Dateien zuerst selbst an, bevor sie sie lesen. Bei den
    Aufgaben erzeugt das Quiz die nötigen Dateien vorher für dich.
    :::
    ---
    ## Die Modi

    Es gibt vier **Grundmodi**. Genau einer davon wird gewählt:

    | Modus | Bedeutung | Datei fehlt | Datei existiert schon |
    |---|---|---|---|
    | `'r'` | Lesen (Standard) | `FileNotFoundError` | wird gelesen |
    | `'w'` | Schreiben | wird neu angelegt | wird **geleert**, alter Inhalt weg! |
    | `'a'` | Anhängen | wird neu angelegt | Neues kommt **hinten** dran |
    | `'x'` | Datei erstellen | wird neu angelegt | `FileExistsError` |

    Dazu kann man **Zusätze** anhängen:
      • `t` = Text (Standard), `b` = Binärdaten (z. B. Bilder): `'rb'`, `'wb'`
      • `+` = zusätzlich lesen UND schreiben: `'r+'`, `'w+'`, `'a+'`

    !! Genau EIN Grundmodus (r, w, a oder x), optional mit Zusätzen.
    !! Wechseln geht nur, indem man die Datei neu öffnet.

    :::info Genauer als auf der Folie
    Auf Folie 30 steht „+ Lesen + Schreiben“ wie ein eigener Modus. `+` ist aber
    nur ein **Zusatz**: `open('daten.txt', '+')` gibt einen `ValueError`, richtig
    ist z. B. `'r+'`. Auch `'rw'` ist ungültig (zwei Grundmodi).

    Außerdem steht dort: „Bis auf 'x' überprüft die Operation nicht, ob eine
    Datei bereits existiert und überschreibt diese im Zweifelsfall.“ Gemeint
    ist: Nur `'x'` **schützt vor dem Überschreiben**. Genau genommen gilt:
    `'w'` leert eine vorhandene Datei, `'a'` hängt nur hinten an, und `'r'`
    braucht eine vorhandene Datei, sonst `FileNotFoundError`.

    „Es ist immer nur ein Modus möglich“ heißt: genau ein Grundmodus.
    Kombinationen mit Zusätzen wie `'rb'` sind erlaubt.
    :::
    """)

k.mc("Du willst in deinem Tagebuch-Programm einen NEUEN Eintrag hinten anfügen, ohne die alten zu löschen. Welcher Modus?",
     ["'a'", "'w'", "'r'", "'x'"],
     "'a' wie 'append' (anhängen). 'w' würde alles Bisherige löschen!")
k.mc("Welcher Modus wirft einen Fehler, wenn die Datei bereits existiert?",
     ["'x'", "'w'", "'a'", "'r'"],
     "'x' (exklusiv erstellen) ist der einzige Modus, der einen Fehler wirft, wenn die Datei "
     "SCHON existiert (FileExistsError). 'r' wirft umgekehrt einen Fehler, wenn sie FEHLT.")
k.ausgabe('f = open("gibt_es_nicht.txt", "r")',
          "Zum Lesen muss die Datei existieren → FileNotFoundError.")
k.ausgabe('with open("neu.txt", "w") as f:\n    f.write("x")\n\nf = open("neu.txt", "x")',
          "Modus 'x' (erstellen) verweigert, wenn die Datei schon existiert → FileExistsError.")
k.ausgabe('f = open("daten.txt", "+")',
          "'+' ist kein eigener Modus, sondern nur ein Zusatz (z. B. 'r+'). Ohne Grundmodus "
          "gibt es einen ValueError.",
          tipp="Ist + ein Grundmodus oder ein Zusatz?")
k.wf("open('bild.png', 'rb') ist erlaubt, obwohl dort zwei Buchstaben stehen.", True,
     "Ja: 'r' ist der eine Grundmodus, 'b' (Binärdaten) nur ein Zusatz. Verboten wären zwei "
     "Grundmodi wie 'rw'.")

# ── Erklärung 2: Lesen ───────────────────────────────────────────────────
k.erklaerung("Dateien lesen", r"""
    ## Vier Arten zu lesen

        content = f.read()        # ganze Datei als EIN großer String
        section = f.read(5)       # die nächsten 5 Zeichen
        line = f.readline()       # eine einzelne Zeile
        lines = f.readlines()     # ganze Datei als LISTE von Zeilen

    Die Liste von `readlines()` kann man wie gewohnt mit einer for-Schleife
    durchlaufen: `for line in lines:`.

    Wichtig: Jede Zeile behält ihren Zeilenumbruch `'\n'` am Ende. So sieht
    `readlines()` für eine Datei mit „Hallo“ und „Welt“ aus:

    :::visual liste
    {"titel": "Ergebnis von f.readlines()", "name": "lines", "werte": ["Hallo\n", "Welt\n"]}
    :::

    `zeile.strip()` entfernt Leerzeichen und Zeilenumbrüche am Anfang und Ende.

    :::code
    with open("hallo.txt", "w") as f:
        f.write("Hallo\nWelt\n")
    with open("hallo.txt") as f:
        lines = f.readlines()
    print(lines)
    for line in lines:
        print(line.strip())
    :::
    ---
    ## Die rätselhaften Leerzeilen

    Im Livecoding wurde jede Zeile einer Datei so ausgegeben:

    :::code
    with open("hallo.txt", "w") as f:
        f.write("Hallo\nWelt\n")
    f = open("hallo.txt")
    for k, line in enumerate(f.readlines()):
        print(f'Zeile {k}: {line}')
    f.close()
    :::

    :::achtung Doppelte Zeilenumbrüche
    `line` endet schon mit `'\n'`, und `print()` hängt noch einen an. So
    entsteht nach jeder Zeile eine Leerzeile. Abhilfe: `line.strip()`.
    :::
    """)

k.ausgabe('with open("test.txt", "w") as f:\n    f.write("Hallo\\n")\n    f.write("Welt\\n")\n\n'
          'with open("test.txt") as f:\n    print(f.readlines())',
          r"readlines() liefert eine Liste der Zeilen – jeweils MIT dem '\n' am Ende.",
          tipp=r"Jede Zeile behält ihr \n.")
k.ausgabe('with open("test.txt", "w") as f:\n    f.write("Lorem ipsum")\n\n'
          'with open("test.txt") as f:\n    print(f.read(5))',
          "read(5) liest nur die nächsten 5 Zeichen: Lorem.")
k.ausgabe('with open("test.txt", "w") as f:\n    f.write("Zeile 1\\nZeile 2\\n")\n\n'
          'with open("test.txt") as f:\n    print(f.readline().strip())',
          "readline() liest nur die erste Zeile, strip() entfernt das \\n am Ende.")
k.mc("Was liefert f.readlines()?",
     ["Eine Liste von Strings – eine pro Zeile",
      "Einen einzigen großen String",
      "Nur die erste Zeile",
      "Die Anzahl der Zeilen"],
     "readlines() → Liste der Zeilen. read() → ein großer String. readline() → eine Zeile.")
k.mc("Warum steht bei diesem Code nach jeder Zeile eine Leerzeile in der Ausgabe?",
     ["Weil line schon mit '\\n' endet und print() noch einen Zeilenumbruch anhängt",
      "Weil readlines() zwischen die Zeilen Leerzeilen einfügt",
      "Weil enumerate jede zweite Zeile überspringt",
      "Weil die Datei im Modus 'r' geöffnet wurde"],
     "Zwei Umbrüche hintereinander ergeben eine Leerzeile. Mit print(line.strip()) "
     "verschwindet sie.",
     code="f = open('hallo.txt')\nfor k, line in enumerate(f.readlines()):\n"
          "    print(f'Zeile {k}: {line}')\nf.close()")

# ── Erklärung 3: Schreiben und Schließen ─────────────────────────────────
k.erklaerung("Schreiben und schließen", r"""
    ## Schreiben

    Schreiben verhält sich ähnlich zum Lesen. Die Daten (ein String) übergibt
    man an `f.write(...)`. Sie werden an der **aktuellen Schreibposition**
    angefügt, also hinter das, was schon geschrieben wurde.

        f.write('Lorem ipsum')

    :::achtung write() macht keinen Zeilenumbruch
    Anders als `print()` hängt `write()` **kein** `'\n'` an. Den Zeilenumbruch
    musst du selbst schreiben: `f.write("Hallo\n")`.

    Außerdem nimmt `write()` nur Strings: `f.write(5)` gibt einen `TypeError`,
    richtig ist `f.write(str(5))` oder `f.write(f"{5}\n")`.
    :::
    ---
    ## Schließen – und warum with so praktisch ist

    Offene Dateien „vermüllen“ das System. Vor allem aber sind
    **Schreiboperationen erst garantiert abgeschlossen, wenn die Datei
    geschlossen wurde**. Sonst kann Text verloren gehen.

        f.close()

    Die offizielle Empfehlung von Python ist die **with-Anweisung**:

        with open(pfad) as f:
            content = f.read()

        with open(pfad, 'w') as f:
            f.write('Inhaltsloser Inhalt\n')

    `f.close()` wird nach dem eingerückten Block **automatisch** ausgeführt und
    kann nicht vergessen werden. Wie eine Tür mit Türschließer: Sie fällt von
    selbst zu, sobald du durch bist.

    :::code
    with open("welt.txt", "w") as f:
        f.write("Hallo\n")
        f.write("Welt\n")
    with open("welt.txt", "a") as f:
        f.write("Schnupsi\n")
    with open("welt.txt") as f:
        print(f.read())
    :::

    Im Livecoding steht zusätzlich `f.close()` innerhalb des with-Blocks. Das
    schadet nicht, ist aber überflüssig.

    Tipp für Umlaute: `open(pfad, 'w', encoding='utf-8')`. Dann sehen „ä, ö, ü“
    auf jedem Computer gleich aus.
    """)

k.ausgabe('with open("test.txt", "w") as f:\n    f.write("abc")\n    f.write("def")\n\n'
          'with open("test.txt") as f:\n    print(f.read())',
          r"write() fügt keinen Zeilenumbruch ein – die Texte kleben direkt aneinander: abcdef.")
k.wf("f.write('Hallo') fügt am Ende automatisch einen Zeilenumbruch ein.", False,
     r"Nein – den Zeilenumbruch musst du selbst schreiben: f.write('Hallo\n').")
k.ausgabe('with open("test.txt", "w") as f:\n    f.write("Eins")\n\n'
          'with open("test.txt", "w") as f:\n    f.write("Zwei")\n\n'
          'with open("test.txt") as f:\n    print(f.read())',
          "Modus 'w' überschreibt die Datei jedes Mal komplett. 'Eins' ist weg!",
          tipp="Was macht der Modus 'w' mit dem alten Inhalt?")
k.ausgabe('with open("test.txt", "w") as f:\n    f.write("Eins")\n\n'
          'with open("test.txt", "a") as f:\n    f.write("Zwei")\n\n'
          'with open("test.txt") as f:\n    print(f.read())',
          "Modus 'a' hängt hinten an. Der alte Inhalt bleibt erhalten: EinsZwei.")
k.mc("Warum sollte man   with open(...) as f:   benutzen?",
     ["Die Datei wird nach dem Block automatisch geschlossen",
      "Die Datei wird dadurch schneller gelesen",
      "Ohne with kann man nicht schreiben",
      "with verschlüsselt die Datei"],
     "with ruft f.close() automatisch auf – man kann es nicht vergessen.")
k.mc("Was passiert, wenn man eine Datei nach dem Schreiben NICHT schließt?",
     ["Es kann zu Datenverlust kommen, weil das Schreiben erst beim Schließen garantiert ist",
      "Nichts, das ist völlig egal",
      "Die Datei wird automatisch gelöscht",
      "Python stürzt sofort ab"],
     "Schreiboperationen sind erst garantiert abgeschlossen, wenn die Datei geschlossen wurde.")

# ── Erklärung 4: CSV ─────────────────────────────────────────────────────
k.erklaerung("CSV – Tabellen als Textdatei", r"""
    ## Comma-separated values

    CSV heißt „comma-separated values“: Jede Zeile ist ein Datensatz, die
    Werte sind durch Kommas getrennt. Die erste Zeile enthält oft die
    Spaltenüberschriften:

        Mail,Name,Studiengang
        anna@mail.de,Anna Muster,Informatik
        ben@mail.de,Ben Beispiel,Maschinenbau

    So eine Datei kann jedes Tabellenprogramm öffnen.

    Schreiben (eine Zeile pro Datensatz):

        f.write(f"{mail},{name},{fach}\n")

    Lesen (Zeile säubern und am Komma zerlegen):

        teile = zeile.strip().split(',')     # → ['anna@mail.de', 'Anna Muster', 'Informatik']

    :::code
    with open("noten.csv", "w", encoding="utf-8") as f:
        f.write("Name,Note\n")
        f.write("Anna,1.7\n")
        f.write("Ben,2.3\n")
    with open("noten.csv", encoding="utf-8") as f:
        zeilen = f.readlines()
    for zeile in zeilen[1:]:
        name, note = zeile.strip().split(",")
        print(name, "hat", float(note))
    :::

    `zeilen[1:]` überspringt die Überschriftenzeile. Die Werte sind nach dem
    Lesen immer **Strings**. Für Zahlen braucht man `int()` oder `float()`.

    :::achtung Wenn ein Wert selbst ein Komma enthält
    Schreibt jemand „Muster, Anna“ als Namen, verrutschen die Spalten. Auch
    ein Zeilenumbruch in einer Eingabe macht das Format kaputt. Darüber sollst
    du in Übung 3 (Aufgabe 2.1) nachdenken.
    :::
    """)

k.ausgabe('zeile = "anna@mail.de,Anna Muster,Informatik\\n"\nteile = zeile.strip().split(",")\nprint(teile[1])',
          "strip() entfernt das \\n, split(',') zerlegt in ['anna@mail.de', 'Anna Muster', "
          "'Informatik']. Index 1 ist der Name.")
k.ausgabe('zeile = "Ben,2.3\\n"\nname, note = zeile.strip().split(",")\nprint(note + note)',
          "Nach dem Zerlegen ist note der STRING '2.3'. Strings werden mit + aneinandergehängt: "
          "2.32.3. Zum Rechnen braucht man float(note).",
          tipp="Welchen Typ hat note nach split()?")
k.mc("Wozu schreibt man   encoding='utf-8'   in open(...)?",
     ["Damit Umlaute wie ä, ö, ü auf jedem Computer richtig gespeichert und gelesen werden",
      "Damit die Datei verschlüsselt wird",
      "Damit die Datei automatisch geschlossen wird",
      "Damit man Zahlen statt Text schreiben kann"],
     "Die Kodierung legt fest, wie Zeichen als Bytes gespeichert werden. Ohne Angabe nimmt "
     "Windows oft eine andere als macOS/Linux, dann werden Umlaute zu Zeichensalat.")

# ── Praxis ───────────────────────────────────────────────────────────────
k.luecke("Ergänze den Code: Die Datei gruss.txt soll neu geschrieben werden (alter Inhalt weg) "
         "und eine Zeile enthalten.",
         """
         with ___("gruss.txt", ___) as f:
             f.___("Hallo Welt\\n")
         """,
         [["open"], ["'w'", "'wt'", "'w+'"], ["write"]],
         "open() öffnet die Datei, Modus 'w' schreibt neu (alter Inhalt verschwindet), "
         "f.write() schreibt den Text.",
         tipp="Öffnen, Modus für „neues leeres Blatt“, und die Methode zum Schreiben.")

k.puzzle("Bringe die Zeilen in die richtige Reihenfolge: Erst zwei Namen in namen.txt schreiben, "
         "dann die Datei lesen und jeden Namen ohne Leerzeilen ausgeben.",
         """
         with open("namen.txt", "w") as f:
             f.write("Anna\\nBen\\n")
         with open("namen.txt") as f:
             zeilen = f.readlines()
         for zeile in zeilen:
             print(zeile.strip())
         """,
         "Erst schreiben (Modus 'w'), die Datei wird nach dem with-Block geschlossen. Dann lesen "
         "und in der Schleife jede Zeile mit strip() säubern.",
         tipp="Lesen kann man erst, wenn die Datei geschrieben ist.",
         ablenker=["    zeilen = f.read(5)"])

_ALT_ZAHLEN = _datei_anlegen("zahlen.txt", "ALT\nALT\n")

k.code(r"""
    ## Zahlen in eine Datei schreiben

    Lies eine ganze Zahl n mit `input()` ein. Schreibe die Zahlen 1 bis n in
    die Datei `zahlen.txt`, jede Zahl in eine eigene Zeile. Gibt es die Datei
    schon, soll ihr alter Inhalt **verschwinden**.

        Eingabe: 3      Inhalt von zahlen.txt:
                        1
                        2
                        3

    Das Quiz legt vorher eine alte `zahlen.txt` an und prüft danach den Inhalt.
    """,
    [P(["3"], ["PRÜFUNG: Datei korrekt"], vorspann=_ALT_ZAHLEN,
       nachspann=_datei_pruefen("zahlen.txt", ["1", "2", "3"])),
     P(["1"], ["PRÜFUNG: Datei korrekt"], vorspann=_ALT_ZAHLEN,
       nachspann=_datei_pruefen("zahlen.txt", ["1"])),
     P(["0"], ["PRÜFUNG: Datei korrekt"], vorspann=_ALT_ZAHLEN,
       nachspann=_datei_pruefen("zahlen.txt", []), beschreibung="n = 0: Datei ist danach leer"),
     P(["5"], ["PRÜFUNG: Datei korrekt"],
       nachspann=_datei_pruefen("zahlen.txt", ["1", "2", "3", "4", "5"]),
       beschreibung="Datei gibt es vorher noch nicht")],
    r"""
    n = int(input("n: "))
    with open("zahlen.txt", "w") as f:
        for i in range(1, n + 1):
            f.write(f"{i}\n")
    """,
    "Modus 'w' leert die alte Datei. write() braucht einen String und den Zeilenumbruch "
    "`\\n` von dir. Mit Modus 'a' bliebe das alte ALT stehen.",
    tipps=["Welcher Modus wirft den alten Inhalt weg?",
           "with open('zahlen.txt', 'w') as f: und darin eine for-Schleife über range(1, n + 1).",
           r'In der Schleife: f.write(f"{i}\n")'])

k.code(r"""
    ## Tagebuch: hinten anhängen

    Die Datei `tagebuch.txt` gibt es schon (das Quiz legt sie an), z. B. mit
    dem Inhalt

        Montag: Vorkurs gestartet

    Sie endet mit einem Zeilenumbruch. Lies mit `input()` einen neuen Eintrag
    ein und hänge ihn als **neue Zeile** hinten an die Datei an. Die alten
    Einträge müssen erhalten bleiben, und der nächste Eintrag muss wieder in
    einer neuen Zeile beginnen können!

        Eingabe: Dienstag: Funktionen gelernt
        tagebuch.txt danach:
            Montag: Vorkurs gestartet
            Dienstag: Funktionen gelernt
    """,
    [P(["Dienstag: Funktionen gelernt"], ["PRÜFUNG: Datei korrekt"],
       vorspann=_datei_anlegen("tagebuch.txt", "Montag: Vorkurs gestartet\n"),
       nachspann=_datei_pruefen("tagebuch.txt", ["Montag: Vorkurs gestartet",
                                                 "Dienstag: Funktionen gelernt"])),
     P(["Mittwoch: Dateien"], ["PRÜFUNG: Datei korrekt"],
       vorspann=_datei_anlegen("tagebuch.txt", "Montag: A\nDienstag: B\n"),
       nachspann=_datei_pruefen("tagebuch.txt", ["Montag: A", "Dienstag: B", "Mittwoch: Dateien"])),
     P(["Erster Eintrag"], ["PRÜFUNG: Datei korrekt"],
       vorspann=_datei_anlegen("tagebuch.txt", ""),
       nachspann=_datei_pruefen("tagebuch.txt", ["Erster Eintrag"]), beschreibung="leeres Tagebuch"),
     P(["Donnerstag: Pause"], ["PRÜFUNG: Datei korrekt"],
       vorspann=_datei_anlegen("tagebuch.txt", "Mittwoch: Dateien\n"),
       nachspann="with open('tagebuch.txt', 'a', encoding='utf-8') as _f:\n    _f.write('Freitag: Ende\\n')\n"
                 + _datei_pruefen("tagebuch.txt", ["Mittwoch: Dateien", "Donnerstag: Pause",
                                                   "Freitag: Ende"]),
       beschreibung="danach hängt das Quiz noch einen Eintrag an")],
    r"""
    eintrag = input("Neuer Eintrag: ")
    with open("tagebuch.txt", "a", encoding="utf-8") as f:
        f.write(eintrag + "\n")
    """,
    "Modus 'a' hängt hinten an, die alten Zeilen bleiben stehen. Mit 'w' wären sie weg. Das "
    "`\\n` sorgt dafür, dass der nächste Eintrag in einer neuen Zeile beginnt.",
    tipps=["Welcher Modus schreibt hinten weiter?",
           "with open('tagebuch.txt', 'a') as f:",
           r'f.write(eintrag + "\n")'])

k.code(r"""
    ## Notendurchschnitt aus einer Datei

    Die Datei `noten.txt` gibt es schon. Jede Zeile hat die Form `Name,Note`:

        Ali,1.0
        Bea,2.0
        Cem,3.3

    Lies die Datei, berechne den Durchschnitt aller Noten und gib ihn mit zwei
    Nachkommastellen aus: `Durchschnitt: 2.10`. Leere Zeilen werden ignoriert.
    Steht gar keine Note in der Datei, gib `Keine Noten` aus.
    """,
    [P(erwartet=["Durchschnitt: 2.10"], vorspann=_datei_anlegen("noten.txt", "Ali,1.0\nBea,2.0\nCem,3.3\n")),
     P(erwartet=["Durchschnitt: 1.70"], vorspann=_datei_anlegen("noten.txt", "Ali,1.7\n")),
     P(erwartet=["Keine Noten"], vorspann=_datei_anlegen("noten.txt", ""), beschreibung="leere Datei"),
     P(erwartet=["Durchschnitt: 1.50"], vorspann=_datei_anlegen("noten.txt", "Ali,1.0\n\nBea,2.0\n"),
       beschreibung="mit Leerzeile"),
     P(erwartet=["Durchschnitt: 2.65"], vorspann=_datei_anlegen("noten.txt", "Kim,2.3\nDeniz,3.0"),
       beschreibung="letzte Zeile ohne Zeilenumbruch")],
    """
    with open("noten.txt", encoding="utf-8") as f:
        zeilen = f.readlines()
    summe = 0
    anzahl = 0
    for zeile in zeilen:
        zeile = zeile.strip()
        if zeile == "":
            continue
        name, note = zeile.split(",")
        summe += float(note)
        anzahl += 1
    if anzahl == 0:
        print("Keine Noten")
    else:
        print(f"Durchschnitt: {summe / anzahl:.2f}")
    """,
    "Lesen, jede Zeile säubern, leere überspringen, zerlegen, die Note mit float() in eine "
    "Zahl umwandeln und aufsummieren. Vor dem Teilen prüfen, ob es überhaupt Noten gibt "
    "(sonst ZeroDivisionError).",
    tipps=["Du brauchst zwei Akkumulatoren: die Summe und die Anzahl der Noten.",
           "Für jede Zeile: strip(), leere Zeilen mit continue überspringen, dann split(',').",
           'Am Ende: if anzahl == 0: print("Keine Noten") else: print(f"Durchschnitt: {summe / anzahl:.2f}")'],
    streng=True)

k.zusammenfassung(r"""
    ## Dateien auf einen Blick

        with open("daten.txt", "w", encoding="utf-8") as f:   # schreiben (neu)
            f.write("Hallo\n")                               # \n selbst setzen!
        with open("daten.txt", "a", encoding="utf-8") as f:   # anhängen
            f.write("Welt\n")
        with open("daten.txt", encoding="utf-8") as f:        # lesen ('r')
            zeilen = f.readlines()                           # ['Hallo\n', 'Welt\n']
        for zeile in zeilen:
            print(zeile.strip())

    | Modus | Datei fehlt | Datei existiert |
    |---|---|---|
    | `'r'` | `FileNotFoundError` | lesen |
    | `'w'` | neu anlegen | leeren und neu schreiben |
    | `'a'` | neu anlegen | hinten anhängen |
    | `'x'` | neu anlegen | `FileExistsError` |
    | Zusätze | `b` binär, `t` Text, `+` lesen und schreiben (`'r+'`) | |

    !! with schließt die Datei automatisch. Erst nach dem Schließen ist alles sicher gespeichert.
    !! readlines() behält das '\n' am Zeilenende → strip() benutzen.
    """)
