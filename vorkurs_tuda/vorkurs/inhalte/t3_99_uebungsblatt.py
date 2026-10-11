# -*- coding: utf-8 -*-
"""Kapitel: Übungsblatt 3 – Schleifen und Funktionen (alle Aufgaben aus Übung 3)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="uebung3",
    titel="Übungsblatt 3 – Schleifen und Funktionen",
    beschreibung="Alle Aufgaben der Übung 3 zum Selbstlösen mit automatischer Prüfung",
    quelle="Übung 3",
    teil="tag3",
    icon="📄")

k.lernziele([
    "Ich kann Summen, Produkte und Listen mit while- und for-Schleifen berechnen",
    "Ich kann prüfen, ob eine Zahl eine Primzahl ist, und dabei Sonderfälle beachten",
    "Ich kann Daten als CSV in eine Datei schreiben und wieder einlesen und auswerten",
    "Ich kann Funktionen schreiben, die andere Funktionen und das Paket math benutzen",
])

# ── Einleitung ──────────────────────────────────────────────────────────
k.erklaerung("Worum geht es auf Übungsblatt 3?", r"""
    ## Das Übungsblatt im Überblick

    Hier findest du alle Aufgaben von **Übung 3 – Schleifen und Funktionen**.
    Jede Aufgabe nennt ihre Nummer vom Blatt, so findest du sie schnell
    wieder. Programmieraufgaben werden automatisch getestet.

    | Aufgabe | Thema | Passendes Kapitel |
    |---|---|---|
    | 1.1.1–1.1.3 | Summe 1 bis 20: Formel, while, for | for-Schleifen |
    | 1.2 | Fakultät | for-Schleifen |
    | 1.3 | Listenverarbeitung (Summe, Produkt, Durchschnitt, Quadrate) | for-Schleifen |
    | 1.4 | Primzahl | for-Schleifen |
    | 2.1, 2.2 | Daten als CSV schreiben und lesen | Dateien, Dictionaries |
    | 3.1 | Zoll → cm, größtes Element | Funktionen |
    | 3.2 | Bildschirmdiagonale | Funktionen, Import |
    | 3.3 (Bonus) | Farben von HSV nach RGB | Bonus: HSV → RGB |

    :::analogie 🏋️ Der Trainingsplan
    Die Vorlesung zeigt dir die Übungen, wie eine Trainerin im
    Fitnessstudio. Kräftiger wirst du aber erst, wenn du selbst trainierst.
      • Das Übungsblatt ist dein Trainingsplan: erst Schleifen (Teil 1), dann
        Dateien (Teil 2), dann Funktionen (Teil 3).
      • Die gestuften Tipps sind die Trainerin: erst ein kleiner Hinweis,
        später die ganze Bewegung.
      • Die Musterlösung nur anzuschauen ist wie Zuschauen beim Training:
        Es sieht leicht aus, bringt aber wenig Muskeln.
    :::

    :::achtung Erst selbst probieren
    Schreib zuerst deinen eigenen Code und lass ihn testen. Fehler sind hier
    ausdrücklich erwünscht: Aus den Testergebnissen lernst du am meisten.
    :::

    :::info Was das Quiz festlegt
    Manche Aufgaben lassen auf dem Blatt offen, **wie** die Ausgabe aussehen
    soll oder wie die Datei heißt. Damit automatisch getestet werden kann,
    legt das Quiz das in der Aufgabe genau fest. Bei den Dateiaufgaben legt
    das Quiz die nötigen Dateien vorher in einem leeren Ordner an.
    :::
    """)

# ── 1.1 Summe ───────────────────────────────────────────────────────────
k.code(r"""
    ## Übung 3, Aufgabe 1.1.1 – Gaußsche Summenformel

    Berechne die Summe der Zahlen 1 bis 20 (eingeschlossen) mit der
    **Gaußschen Summenformel** und gib sie aus:

        1 + 2 + 3 + … + n = n · (n + 1) / 2

    Benutze **keine Schleife** und schreib das Ergebnis nicht direkt hin.
    Ausgabe: `210`. Mit `/` erscheint `210.0`, das ist auch richtig. Als
    ganze Zahl bekommst du es mit `//` oder `int(...)`.
    """,
    [P(erwartet=[("210", "210.0")])],
    """
    n = 20
    print(n * (n + 1) // 2)
    """,
    "Die Formel liefert das Ergebnis ohne Schleife. `//` teilt ganzzahlig, das Ergebnis ist "
    "hier immer ganz, weil n · (n + 1) immer gerade ist.",
    verboten=["for", "while", "210"],
    tipps=["Lege n = 20 in einer Variable ab.",
           "Setze n in die Formel n * (n + 1) / 2 ein.",
           "print(n * (n + 1) // 2)"])

k.ausgabe("n = 20\nprint(n * (n + 1) // 2)",
          "Gaußsche Summenformel: 20 · 21 // 2 = 210. (Übung 3, 1.1.1)")

k.mc("Warum soll die Summe in Übung 3, Aufgabe 1.1.2 zusätzlich mit einer Schleife berechnet werden, "
     "obwohl die Formel so schnell ist?",
     ["Weil nicht alle Zahlenreihen einfach aufsteigend sind – dann gibt es keine so einfache Formel",
      "Weil die Gaußsche Formel manchmal falsch rechnet",
      "Weil Python keine Multiplikation kann",
      "Weil Schleifen immer schneller sind als Formeln"],
     "So steht es auf dem Blatt: Die Formel klappt nur für 1 + 2 + … + n. Für beliebige "
     "Zahlenreihen braucht man eine Schleife.")

k.code(r"""
    ## Übung 3, Aufgabe 1.1.2 – Summe mit while

    Berechne die Summe der Zahlen 1 bis 20 (eingeschlossen) diesmal mit einer
    **while-Schleife** und gib sie aus. Ausgabe: `210`
    """,
    [P(erwartet=["210"])],
    """
    summe = 0
    i = 1
    while i <= 20:
        summe += i
        i += 1
    print(summe)
    """,
    "Summen-Akkumulator mit Startwert 0, Zähler i von 1 bis 20. Wichtig: `i <= 20`, damit die "
    "20 dabei ist, und `i += 1`, sonst entsteht eine Endlosschleife.",
    pflicht=["while"],
    verboten=["for", "210"],
    tipps=["Du brauchst zwei Variablen: eine für die Summe, eine zum Zählen.",
           "summe = 0, i = 1, dann while i <= 20:",
           "Im Körper: summe += i und i += 1. Nach der Schleife print(summe)."])

k.code(r"""
    ## Übung 3, Aufgabe 1.1.3 – Summe mit for

    Setze die Summe der Zahlen 1 bis 20 (eingeschlossen) abschließend mit einer
    **for-Schleife** um und gib sie aus. Ausgabe: `210`
    """,
    [P(erwartet=["210"])],
    """
    summe = 0
    for i in range(1, 21):
        summe += i
    print(summe)
    """,
    "range(1, 21) – das Ende ist exklusiv, deshalb 21 und nicht 20!",
    pflicht=["for"],
    verboten=["while", "210"],
    tipps=["Welche Zahlen soll range liefern? Denk an das exklusive Ende.",
           "for i in range(1, 21):",
           "summe = 0 vor der Schleife, summe += i darin, print(summe) danach."])

# ── 1.2 Fakultät ────────────────────────────────────────────────────────
k.code(r"""
    ## Übung 3, Aufgabe 1.2 (1) – Fakultät von 15

    Schreibe ein Programm, das den Wert des Ausdrucks
    1 · 2 · 3 · … · 15 = 15! (Fakultät von 15) berechnet und das Ergebnis auf
    der Konsole ausgibt. Benutze eine Schleife.
    """,
    [P(erwartet=["1307674368000"])],
    """
    ergebnis = 1
    for i in range(1, 16):
        ergebnis *= i
    print(ergebnis)
    """,
    "Produkt-Akkumulator: Startwert 1 (nicht 0!), range(1, 16), damit die 15 dabei ist.",
    verboten=["1307674368000", "factorial"],
    tipps=["Ein Produkt wird in einer Schleife aufgebaut. Mit welchem Wert startet es?",
           "ergebnis = 1, dann for i in range(1, 16):",
           "Im Körper: ergebnis *= i. Danach print(ergebnis)."])

k.code(r"""
    ## Übung 3, Aufgabe 1.2 (2) – Fakultät beliebiger Eingaben

    Erweitere dein Programm: Lies eine ganze Zahl n mit `input()` ein und gib
    n! aus. Es gilt `0! = 1`.

    Für negative Zahlen gibt es keine Fakultät. Gib dann genau diesen Hinweis
    aus: `Keine Fakultät für negative Zahlen`

        Eingabe: 5     Ausgabe: 120
        Eingabe: 0     Ausgabe: 1
        Eingabe: -3    Ausgabe: Keine Fakultät für negative Zahlen
    """,
    [P(["15"], ["1307674368000"]), P(["5"], ["120"]), P(["0"], ["1"]), P(["1"], ["1"]),
     P(["20"], ["2432902008176640000"]),
     P(["-3"], ["Keine Fakultät für negative Zahlen"], beschreibung="negative Zahl")],
    """
    n = int(input("n = "))
    if n < 0:
        print("Keine Fakultät für negative Zahlen")
    else:
        ergebnis = 1
        for i in range(1, n + 1):
            ergebnis *= i
        print(ergebnis)
    """,
    "Startwert 1 (Produkt!). range(1, n + 1), damit n selbst dabei ist. Bei n = 0 läuft "
    "die Schleife gar nicht, und es bleibt korrekt bei 1. Negative Zahlen fängt das if ab.",
    tipps=["Was ändert sich gegenüber Teil 1? Woher kommt jetzt die obere Grenze?",
           "Erst mit if n < 0 den Sonderfall behandeln, sonst wie in Teil 1.",
           "ergebnis = 1, dann for i in range(1, n + 1): ergebnis *= i"],
    streng=True)

# ── 1.3 Listenverarbeitung ──────────────────────────────────────────────
k.mc("Was musst du bei der Berechnung des Durchschnitts beachten? (Übung 3, 1.3)",
     ["Bei einer leeren Liste würde durch 0 geteilt werden",
      "Der Durchschnitt muss immer eine Ganzzahl sein",
      "Man darf nur // benutzen",
      "Der Durchschnitt ist immer das mittlere Element"],
     "summe / len(liste) – bei len(liste) = 0 gibt es einen ZeroDivisionError. Außerdem "
     "ist das Ergebnis mit / immer ein float.")

k.code(r"""
    ## Übung 3, Aufgabe 1.3 – Listenverarbeitung

    Häufig gibt es eine Variable, in der das Ergebnis langsam aufgebaut wird
    (für eine Summe startet sie bei 0). Die Variable `liste` ist schon
    vorgegeben, z. B. `[10, 2, 7, 4, 3, 5, 8]`. Berechne und gib aus, jedes in
    einer eigenen Zeile und in dieser Reihenfolge:
      1. die Summe aller Elemente
      2. das Produkt aller Elemente
      3. den Durchschnitt aller Elemente (nicht runden!)
      4. eine Liste der Quadrate der Elemente (z. B. `[100, 4, 49, ...]`)

    Ist die Liste leer, gib statt des Durchschnitts die Zeile `Kein Durchschnitt`
    aus. Schaffst du es mit nur EINER Schleife?
    """,
    [P(vorspann="liste = [10, 2, 7, 4, 3, 5, 8]",
       erwartet=["39", "67200", "5.571428571428571", "[100, 4, 49, 16, 9, 25, 64]"]),
     P(vorspann="liste = [1, 2, 3]", erwartet=["6", "2.0", "[1, 4, 9]"]),
     P(vorspann="liste = [-2, 2]", erwartet=["0", "-4", "0.0", "[4, 4]"]),
     P(vorspann="liste = [5]", erwartet=["5", "5.0", "[25]"]),
     P(vorspann="liste = []", erwartet=["0", "1", "Kein Durchschnitt", "[]"],
       beschreibung="leere Liste")],
    """
    summe = 0
    produkt = 1
    quadrate = []
    for x in liste:
        summe += x
        produkt *= x
        quadrate.append(x ** 2)
    print(summe)
    print(produkt)
    if len(liste) > 0:
        print(summe / len(liste))
    else:
        print("Kein Durchschnitt")
    print(quadrate)
    """,
    "Ein Durchlauf reicht für alle Werte: drei Akkumulatoren mit den Startwerten 0, 1 und []. "
    "Vor dem Teilen wird geprüft, ob die Liste leer ist, sonst gäbe es einen ZeroDivisionError.",
    tipps=["Drei Startwerte vor der Schleife: summe, produkt, quadrate.",
           "summe = 0, produkt = 1, quadrate = [] – in der Schleife +=, *= und append.",
           "Für den Durchschnitt: if len(liste) > 0: print(summe / len(liste)) else: print('Kein Durchschnitt')"],
    vorlage="# liste ist schon vorgegeben\n",
    streng=True)

# ── 1.4 Primzahl ────────────────────────────────────────────────────────
k.code(r"""
    ## Übung 3, Aufgabe 1.4 – Primzahl

    Lies eine ganze Zahl mit `input()` ein und prüfe, ob sie eine Primzahl
    ist. Gib genau eine dieser Zeilen aus:

        <n> ist eine Primzahl
        <n> ist keine Primzahl

    Primzahlen sind größer als 1 und nur durch 1 und sich selbst teilbar.
    0, 1 und negative Zahlen sind KEINE Primzahlen, 2 ist eine. Teste dein
    Programm mit verschiedenen Werten.
    """,
    [P(["7"], ["7 ist eine Primzahl"], nicht=["keine primzahl"]),
     P(["2"], ["2 ist eine Primzahl"], nicht=["keine primzahl"]),
     P(["97"], ["97 ist eine Primzahl"], nicht=["keine primzahl"]),
     P(["7919"], ["7919 ist eine Primzahl"], nicht=["keine primzahl"]),
     P(["9"], ["9 ist keine Primzahl"], nicht=["ist eine primzahl"]),
     P(["25"], ["25 ist keine Primzahl"], nicht=["ist eine primzahl"]),
     P(["1"], ["1 ist keine Primzahl"], nicht=["ist eine primzahl"]),
     P(["0"], ["0 ist keine Primzahl"], nicht=["ist eine primzahl"]),
     P(["-7"], ["-7 ist keine Primzahl"], nicht=["ist eine primzahl"])],
    """
    n = int(input("Zahl: "))
    ist_prim = n > 1
    for teiler in range(2, n):
        if n % teiler == 0:
            ist_prim = False
            break
    if ist_prim:
        print(f"{n} ist eine Primzahl")
    else:
        print(f"{n} ist keine Primzahl")
    """,
    "`ist_prim = n > 1` erledigt die Sonderfälle 0, 1 und negative Zahlen. Mit break hört man "
    "beim ersten gefundenen Teiler auf. Profi-Tipp: Es reicht, Teiler bis zur Wurzel von n "
    "zu prüfen (`while teiler * teiler <= n`).",
    tipps=["Was macht eine Zahl zur Primzahl? Welche Zahlen sind auf jeden Fall keine?",
           "Probiere alle Teiler von 2 bis n-1. Findest du einen mit n % teiler == 0, ist es keine.",
           "ist_prim = n > 1, dann for teiler in range(2, n): if n % teiler == 0: ist_prim = False"],
    streng=True)

# ── 2.1 CSV schreiben ───────────────────────────────────────────────────
_BESTELLUNGEN = """
bestellungen = [
    ('joern.siegmund@gmail.com', 'Jörn Siegmund', 'Informatik'),
    ('alena_joerg@aol.com', 'Alena Jörg', 'Elektrotechnik'),
    ('gema76@yahoo.com', 'Gerta Volkmar', 'Informatik'),
    ('lia.wendeltreppe@proton.me', 'Lia Wendel', 'Cognitive Science'),
    ('leon.heinrich@gmail.com', 'Leon Heinrich', 'Wirtschaftsinformatik'),
    ('harter-mut1996@gmx.de', 'Christoph Hartmut', 'Maschinenbau')
]
"""

_ALTE_DATEI = """
with open("anmeldungen.csv", "w", encoding="utf-8") as _f:
    _f.write("ALT\\n" * 9)
"""

_CSV_PRUEFUNG = """
import os as _os
if not _os.path.exists("anmeldungen.csv"):
    print("PRÜFUNG: Die Datei anmeldungen.csv wurde nicht gefunden!")
else:
    with open("anmeldungen.csv", encoding="utf-8", errors="replace") as _f:
        _ist = [_z.strip() for _z in _f.read().strip().splitlines()]
    _soll = ["Mail,Name,Studiengang"] + [",".join(_t) for _t in bestellungen]
    if _ist == _soll:
        print("PRÜFUNG: Datei korrekt")
    else:
        print("PRÜFUNG: Inhalt stimmt nicht. Erwartet wurde:")
        for _z in _soll:
            print("   ", _z)
        print("PRÜFUNG: Gefunden wurde:")
        for _z in _ist:
            print("   ", _z)
"""

k.code(r"""
    ## Übung 3, Aufgabe 2.1 – Daten als CSV schreiben

    Die Liste `bestellungen` ist schon vorgegeben (Daten einer fiktiven
    Programmiervorkurs-Anmeldung). Jeder Eintrag ist ein Tupel
    `(Mail, Name, Studiengang)`, z. B.

        ('joern.siegmund@gmail.com', 'Jörn Siegmund', 'Informatik')

    Erstelle mit Python die Datei `anmeldungen.csv` und schreibe die Werte im
    Format CSV hinein:
      • Die erste Zeile enthält die Spaltenüberschriften `Mail,Name,Studiengang`.
      • Jedes Tupel kommt in eine eigene Zeile, die Einträge mit Kommas getrennt
        (ohne Leerzeichen).
      • Existiert die Datei bereits, sollen die Daten überschrieben werden bzw.
        am Dateianfang begonnen werden.

    Das Quiz legt vorher eine alte `anmeldungen.csv` an und prüft danach den Inhalt.
    """,
    [P(vorspann=_BESTELLUNGEN + _ALTE_DATEI, nachspann=_CSV_PRUEFUNG,
       erwartet=["PRÜFUNG: Datei korrekt"], beschreibung="alte Datei wird überschrieben"),
     P(vorspann="bestellungen = [('a@b.de', 'Ada', 'Mathe'), ('c@d.de', 'Carl', 'Physik')]"
                + _ALTE_DATEI,
       nachspann=_CSV_PRUEFUNG, erwartet=["PRÜFUNG: Datei korrekt"], beschreibung="andere Daten"),
     P(vorspann="bestellungen = []", nachspann=_CSV_PRUEFUNG,
       erwartet=["PRÜFUNG: Datei korrekt"], beschreibung="leere Liste: nur die Überschrift")],
    r"""
    with open("anmeldungen.csv", "w", encoding="utf-8") as f:
        f.write("Mail,Name,Studiengang\n")
        for mail, name, studiengang in bestellungen:
            f.write(f"{mail},{name},{studiengang}\n")
    """,
    "Modus 'w' überschreibt die Datei bzw. beginnt am Dateianfang (mit 'a' bliebe der alte "
    "Inhalt stehen). Das Tupel wird in der for-Schleife direkt in drei Variablen ausgepackt. "
    "Das \\n am Ende jeder Zeile nicht vergessen! (Alternative: f.write(','.join(eintrag) + '\\n'))",
    tipps=["Welcher Modus beginnt am Dateianfang und wirft den alten Inhalt weg?",
           "with open('anmeldungen.csv', 'w', encoding='utf-8') as f: und zuerst die Überschrift schreiben.",
           r'for mail, name, studiengang in bestellungen: f.write(f"{mail},{name},{studiengang}\n")'],
    vorlage="# bestellungen ist schon vorgegeben\n")

k.mc("Bei welcher Nutzereingabe gibt es Probleme mit dem CSV-Format? (Übung 3, 2.1)",
     ["Wenn ein Name ein Komma enthält, z.B. 'Muster, Anna'",
      "Wenn ein Name Umlaute enthält",
      "Wenn eine Mail-Adresse ein @ enthält",
      "Wenn ein Name sehr kurz ist"],
     "Das Komma ist das Trennzeichen. Ein Komma IM Wert lässt die Spalten verrutschen. "
     "(Auch Zeilenumbrüche in der Eingabe wären ein Problem.)")

k.wf("Auf dem Blatt warnt der Hinweis davor, existierende Dateien zu überschreiben, die Aufgabe "
     "verlangt aber das Überschreiben. Das ist ein echter Widerspruch.", False,
     "Kein Widerspruch: Die eigene CSV-Datei darf (und soll) überschrieben werden. Der Hinweis "
     "meint fremde, wichtige Dateien. Darum: Pfad genau prüfen, bevor man im Modus 'w' öffnet.")

# ── 2.2 CSV lesen ───────────────────────────────────────────────────────
_CSV_DATEI = """
with open("anmeldungen.csv", "w", encoding="utf-8") as _f:
    _f.write("Mail,Name,Studiengang\\n")
    _f.write("joern.siegmund@gmail.com,Jörn Siegmund,Informatik\\n")
    _f.write("alena_joerg@aol.com,Alena Jörg,Elektrotechnik\\n")
    _f.write("gema76@yahoo.com,Gerta Volkmar,Informatik\\n")
    _f.write("lia.wendeltreppe@proton.me,Lia Wendel,Cognitive Science\\n")
    _f.write("leon.heinrich@gmail.com,Leon Heinrich,Wirtschaftsinformatik\\n")
    _f.write("harter-mut1996@gmx.de,Christoph Hartmut,Maschinenbau\\n")
"""
_CSV_DATEI_2 = """
with open("anmeldungen.csv", "w", encoding="utf-8") as _f:
    _f.write("Mail,Name,Studiengang\\n")
    _f.write("a@b.de,Ada,Mathe\\n")
    _f.write("c@d.de,Carl,Physik\\n")
    _f.write("e@f.de,Emmy,Mathe\\n")
"""
_CSV_LEERZEILE = """
with open("anmeldungen.csv", "w", encoding="utf-8") as _f:
    _f.write("Mail,Name,Studiengang\\n")
    _f.write("a@b.de,Ada,Mathe\\n")
    _f.write("c@d.de,Carl,Physik\\n")
    _f.write("\\n")
"""
_CSV_NUR_KOPF = """
with open("anmeldungen.csv", "w", encoding="utf-8") as _f:
    _f.write("Mail,Name,Studiengang\\n")
"""

k.code(r"""
    ## Übung 3, Aufgabe 2.2 – Daten lesen

    Die Datei `anmeldungen.csv` aus Aufgabe 2.1 existiert bereits (das Quiz
    legt sie an):

        Mail,Name,Studiengang
        joern.siegmund@gmail.com,Jörn Siegmund,Informatik
        alena_joerg@aol.com,Alena Jörg,Elektrotechnik
        ...

    Öffne die Datei in Python und lies alle Zeilen als Liste von Strings ein.
    Zähle, wie häufig die einzelnen Studiengänge angegeben wurden, und gib für
    jeden Studiengang eine Zeile aus:

        Informatik: 2
        Elektrotechnik: 1
        ...

    Die Überschriftenzeile darf NICHT mitgezählt werden, leere Zeilen werden
    ignoriert. Die Reihenfolge der Ausgabezeilen ist egal.
    """,
    [P(vorspann=_CSV_DATEI, erwartet=["Informatik: 2", "Elektrotechnik: 1",
                                       "Cognitive Science: 1", "Wirtschaftsinformatik: 1",
                                       "Maschinenbau: 1"], nicht=["studiengang: 1"]),
     P(vorspann=_CSV_DATEI_2, erwartet=["Mathe: 2", "Physik: 1"], nicht=["studiengang: 1"]),
     P(vorspann=_CSV_LEERZEILE, erwartet=["Mathe: 1", "Physik: 1"], beschreibung="Leerzeile am Ende"),
     P(vorspann=_CSV_NUR_KOPF, nicht=["studiengang:"], beschreibung="nur die Überschrift")],
    """
    with open("anmeldungen.csv", encoding="utf-8") as f:
        zeilen = f.readlines()

    anzahl = {}
    for zeile in zeilen[1:]:
        teile = zeile.strip().split(",")
        if len(teile) < 3:
            continue
        studiengang = teile[2]
        anzahl[studiengang] = anzahl.get(studiengang, 0) + 1

    for studiengang, n in anzahl.items():
        print(f"{studiengang}: {n}")
    """,
    "zeilen[1:] überspringt die Überschrift. strip() entfernt das \\n, split(',') zerlegt die "
    "Zeile, [2] ist die dritte Spalte. Zeilen mit weniger als drei Teilen (Leerzeilen) werden "
    "übersprungen. Gezählt wird mit dem Muster anzahl.get(schluessel, 0) + 1.",
    tipps=["Erst lesen (readlines), dann zählen (Dictionary), dann ausgeben.",
           "for zeile in zeilen[1:]: teile = zeile.strip().split(',') – Leerzeilen mit continue überspringen.",
           "anzahl[teile[2]] = anzahl.get(teile[2], 0) + 1 und am Ende for s, n in anzahl.items(): print(f'{s}: {n}')"],
    streng=True)

# ── 3.1 Funktionen ──────────────────────────────────────────────────────
k.code(r"""
    ## Übung 3, Aufgabe 3.1 (1) – Zoll in Zentimeter

    Definiere als Einstieg eine Hilfsfunktion zum Umrechnen von Einheiten,
    genauer Zoll → cm. Die Funktion heißt `zoll_zu_cm(zoll)` und gibt die Länge
    in Zentimetern ZURÜCK (return, nicht print!). 1 Zoll = 2.54 cm.

        zoll_zu_cm(1)  → 2.54
        zoll_zu_cm(27) → 68.58
    """,
    [F("zoll_zu_cm(1)", 2.54), F("zoll_zu_cm(0)", 0), F("zoll_zu_cm(27)", 68.58),
     F("zoll_zu_cm(2.5)", 6.35), F("zoll_zu_cm(10)")],
    """
    def zoll_zu_cm(zoll):
        return zoll * 2.54
    """,
    "Eine Zeile im Körper reicht. Wichtig ist return: Nur dann kann man das Ergebnis später "
    "weiterverwenden, z. B. in Aufgabe 3.2.",
    tipps=["Wie rechnest du von Zoll in cm um?",
           "Die Funktion bekommt zoll als Parameter und soll das Ergebnis zurückgeben.",
           "return zoll * 2.54"],
    vorlage="def zoll_zu_cm(zoll):\n    ...")

k.code(r"""
    ## Übung 3, Aufgabe 3.1 (2) – Größtes Element ausgeben

    Schreibe eine Funktion `groesstes_ausgeben(liste)`, die eine Liste von
    Zahlen als Parameter nimmt, das größte Element bestimmt und es zusammen mit
    seinem Index **auf der Konsole ausgibt**. Achte dabei auf Sonderfälle:
      • Kommt das Maximum mehrfach vor, nimm den ERSTEN Index.
      • Ist die Liste leer, gib `Die Liste ist leer` aus.

    Format der Ausgabe:

        groesstes_ausgeben([3, 9, 2])    gibt aus:  Größtes Element: 9 an Index 1

    Das Quiz ruft deine Funktion mit verschiedenen Listen auf.
    """,
    [P(nachspann="groesstes_ausgeben([3, 9, 2])", erwartet=["Größtes Element: 9 an Index 1"],
       beschreibung="groesstes_ausgeben([3, 9, 2])"),
     P(nachspann="groesstes_ausgeben([-3, -1, -7])", erwartet=["Größtes Element: -1 an Index 1"],
       beschreibung="nur negative Zahlen"),
     P(nachspann="groesstes_ausgeben([4, 4, 1])", erwartet=["Größtes Element: 4 an Index 0"],
       nicht=["an index 1"], beschreibung="Maximum doppelt"),
     P(nachspann="groesstes_ausgeben([5])", erwartet=["Größtes Element: 5 an Index 0"],
       beschreibung="ein Element"),
     P(nachspann="groesstes_ausgeben([])", erwartet=["Die Liste ist leer"],
       beschreibung="leere Liste"),
     P(nachspann="groesstes_ausgeben([1.5, 2.25, 0])", erwartet=["Größtes Element: 2.25 an Index 1"],
       beschreibung="Kommazahlen")],
    """
    def groesstes_ausgeben(liste):
        if len(liste) == 0:
            print("Die Liste ist leer")
            return
        max_index = 0
        for i in range(1, len(liste)):
            if liste[i] > liste[max_index]:
                max_index = i
        print(f"Größtes Element: {liste[max_index]} an Index {max_index}")
    """,
    "Sonderfälle: Die leere Liste wird zuerst abgefangen (ein leeres `return` beendet die "
    "Funktion). Man startet mit dem ersten Element, nicht mit 0, sonst wäre bei lauter "
    "negativen Zahlen 0 das „Maximum“. Mit `>` statt `>=` bleibt bei Gleichstand der erste Index.",
    tipps=["Welche Sonderfälle gibt es? Denk an [], an [-3, -1, -7] und an [4, 4, 1].",
           "Merke dir den Index des bisher größten Elements, Startwert 0, und vergleiche alle weiteren.",
           'Am Ende: print(f"Größtes Element: {liste[max_index]} an Index {max_index}")'],
    vorlage="def groesstes_ausgeben(liste):\n    ...\n",
    streng=True)

# ── 3.2 Bildschirmdiagonale ─────────────────────────────────────────────
k.erklaerung("Mathe zur Bildschirmdiagonale (Aufgabe 3.2)", r"""
    ## Breite, Höhe und Diagonale

    Bildschirme werden mit ihrer Diagonale in Zoll und dem Seitenverhältnis
    Breite:Höhe (z. B. 16:9) verkauft. Breite, Höhe und Diagonale bilden ein
    rechtwinkliges Dreieck. In Abbildung 1 des Blatts liegt der Winkel **α
    unten links, zwischen der Höhe und der Diagonale**:

        +--------- Breite ---------+
        |                      /   |
        |                 /        |
      Höhe           /             |
        |       /   Diagonale      |
        | α /                      |
        +--------------------------+

    Von α aus gesehen ist die Breite die **Gegenkathete** und die Höhe die
    **Ankathete**. Deshalb:

        tan(α) = Breite / Höhe     →   α = math.atan(breite_verh / hoehe_verh)
        Breite = Diagonale · sin(α)
        Höhe   = Diagonale · cos(α)

    :::code
    import math
    diagonale_cm = 27 * 2.54
    alpha = math.atan(16 / 9)
    print(round(diagonale_cm * math.sin(alpha), 2))
    print(round(diagonale_cm * math.cos(alpha), 2))
    :::

    :::info Andere Wege führen auch ans Ziel
    Nimmt man den Winkel zwischen **Breite** und Diagonale, vertauschen sich
    sin und cos. Ganz ohne Winkel geht es mit Pythagoras:
    `faktor = diagonale_cm / math.sqrt(b**2 + h**2)`, dann `breite = b * faktor`
    und `hoehe = h * faktor`. Alle Wege liefern dieselben Zahlen.

    Das Blatt lässt offen, wie das Seitenverhältnis übergeben wird. Im Quiz
    bekommt die Funktion zwei Zahlen, z. B. `16` und `9`.
    :::
    """)

k.mc("In Abbildung 1 liegt α zwischen Höhe und Diagonale. Wie berechnet man α aus dem "
     "Seitenverhältnis?",
     ["alpha = math.atan(breite_verh / hoehe_verh)",
      "alpha = math.atan(hoehe_verh / breite_verh)",
      "alpha = math.tan(breite_verh / hoehe_verh)",
      "alpha = breite_verh / hoehe_verh"],
     "Von α aus ist die Breite gegenüber (Gegenkathete) und die Höhe anliegend (Ankathete). "
     "tan(α) = Gegenkathete / Ankathete = Breite / Höhe, also α = atan(Breite / Höhe). Die "
     "Umkehrfunktion von tan ist atan, nicht tan.")

k.code(r"""
    ## Übung 3, Aufgabe 3.2 – Bildschirmdiagonale

    Berechne die Größe eines Bildschirms im metrischen System. Schreibe eine
    Funktion

        bildschirm_groesse(diagonale_zoll, breite_verh, hoehe_verh)

    die die Bildschirmdiagonale in Zoll und das Seitenverhältnis (Breite:Höhe,
    als zwei Zahlen) entgegennimmt und die Breite und Höhe in Zentimetern als
    Tupel `(breite_cm, hoehe_cm)` ZURÜCKGIBT.

    Du kannst `zoll_zu_cm` aus Aufgabe 3.1 wiederverwenden (dann musst du sie
    hier noch einmal mit hineinschreiben). Vergiss `import math` nicht.

        bildschirm_groesse(27, 16, 9)  → ungefähr (59.77, 33.62)
        bildschirm_groesse(15, 4, 3)   → (30.48, 22.86)
    """,
    [F("bildschirm_groesse(27, 16, 9)"), F("bildschirm_groesse(24, 16, 10)"),
     F("bildschirm_groesse(15, 4, 3)", (30.48, 22.86)), F("bildschirm_groesse(10, 1, 1)"),
     F("bildschirm_groesse(34, 21, 9)")],
    """
    import math

    def zoll_zu_cm(zoll):
        return zoll * 2.54

    def bildschirm_groesse(diagonale_zoll, breite_verh, hoehe_verh):
        diagonale_cm = zoll_zu_cm(diagonale_zoll)
        alpha = math.atan(breite_verh / hoehe_verh)   # Winkel zwischen Höhe und Diagonale
        breite = diagonale_cm * math.sin(alpha)
        hoehe = diagonale_cm * math.cos(alpha)
        return (breite, hoehe)
    """,
    "Funktionen können andere Funktionen benutzen – hier wird zoll_zu_cm wiederverwendet. "
    "Der Winkel α aus Abbildung 1 liegt zwischen Höhe und Diagonale: tan α = Breite / Höhe. "
    "Alternative mit Pythagoras: `faktor = diagonale_cm / math.sqrt(b**2 + h**2)`, dann "
    "`breite = b * faktor` und `hoehe = h * faktor`.",
    tipps=["Erst die Diagonale in cm umrechnen, dann mit dem Winkel weiterrechnen.",
           "alpha = math.atan(breite_verh / hoehe_verh)",
           "breite = diagonale_cm * math.sin(alpha), hoehe = diagonale_cm * math.cos(alpha), return (breite, hoehe)"],
    vorlage="import math\n\n\ndef bildschirm_groesse(diagonale_zoll, breite_verh, hoehe_verh):\n    ...\n")

# ── 3.3 HSV → RGB (Bonus) ───────────────────────────────────────────────
k.code(r"""
    ## Übung 3, Aufgabe 3.3 (Bonus) – Farbkonvertierung HSV → RGB

    Farben im HSV-Format (Hue, Saturation, Value) haben die Wertebereiche
    H ∈ [0, 360], S ∈ [0, 1] und V ∈ [0, 1]. Schreibe eine Funktion
    `hsv_zu_rgb(h, s, v)`, die ein Dreier-Tupel `(r, g, b)` für die RGB-Farben
    zurückgibt. Die Formeln vom Blatt:

        hi = ⌊H / 60⌋        (abrunden mit math.floor)
        f  = H / 60 − hi
        p  = V · (1 − S)
        q  = V · (1 − S · f)
        t  = V · (1 − S · (1 − f))

        (r, g, b) = (q, V, p)   wenn hi = 1
                    (p, V, t)   wenn hi = 2
                    (p, q, V)   wenn hi = 3
                    (t, p, V)   wenn hi = 4
                    (V, p, q)   wenn hi = 5
                    (V, t, p)   sonst

    Die resultierenden RGB-Werte liegen im Bereich [0, 1].

        hsv_zu_rgb(0, 1, 1)   → (1, 0, 0)     (Rot)
        hsv_zu_rgb(120, 1, 1) → (0, 1, 0)     (Grün)

    Mehr Hintergrund und Übungen in kleinen Schritten findest du im Kapitel
    „Bonus: Farben von HSV nach RGB umrechnen“.
    """,
    [F("hsv_zu_rgb(0, 1, 1)"), F("hsv_zu_rgb(120, 1, 1)"), F("hsv_zu_rgb(240, 1, 1)"),
     F("hsv_zu_rgb(60, 1, 1)"), F("hsv_zu_rgb(30, 1, 1)"), F("hsv_zu_rgb(300, 0.5, 0.8)"),
     F("hsv_zu_rgb(200, 0, 0.5)"), F("hsv_zu_rgb(360, 1, 1)"), F("hsv_zu_rgb(180, 0.25, 0.4)")],
    """
    import math

    def hsv_zu_rgb(h, s, v):
        hi = math.floor(h / 60)
        f = h / 60 - hi
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))
        if hi == 1:
            return (q, v, p)
        elif hi == 2:
            return (p, v, t)
        elif hi == 3:
            return (p, q, v)
        elif hi == 4:
            return (t, p, v)
        elif hi == 5:
            return (v, p, q)
        else:
            return (v, t, p)
    """,
    "Erst alle Hilfswerte berechnen, dann mit if/elif/else den passenden Fall auswählen. "
    "Für H = 360 ist hi = 6, das fällt in „sonst“ und liefert wieder Rot – richtig so, denn "
    "360° ist auf dem Farbkreis dasselbe wie 0°.",
    tipps=["import math nicht vergessen. Berechne zuerst hi, f, p, q und t.",
           "hi = math.floor(h / 60), f = h / 60 - hi, …",
           "Dann: if hi == 1: return (q, v, p) elif hi == 2: … else: return (v, t, p)"],
    vorlage="import math\n\n\ndef hsv_zu_rgb(h, s, v):\n    hi = math.floor(h / 60)\n    ...\n")

k.zusammenfassung(r"""
    ## Die Muster aus Übungsblatt 3

    | Aufgabe | Kern der Lösung |
    |---|---|
    | 1.1 Summe | Formel `n * (n + 1) // 2`, oder `summe = 0` und `summe += i` in while/for |
    | 1.2 Fakultät | `ergebnis = 1`, `for i in range(1, n + 1): ergebnis *= i`, 0! = 1 |
    | 1.3 Liste | mehrere Akkumulatoren in EINER Schleife, leere Liste vor dem Teilen prüfen |
    | 1.4 Primzahl | `ist_prim = n > 1`, Teiler suchen, `break` |
    | 2.1 CSV schreiben | Modus `'w'`, Überschrift, `f.write(f"{a},{b},{c}\n")` |
    | 2.2 CSV lesen | `readlines()`, `zeilen[1:]`, `strip().split(',')`, Zähl-Dictionary |
    | 3.1 Funktionen | `return` für Werte, `print` für Ausgaben, Sonderfälle zuerst |
    | 3.2 Bildschirm | `alpha = math.atan(b / h)`, `d·sin α`, `d·cos α` |
    | 3.3 HSV → RGB | `math.floor`, Hilfswerte, if/elif/else |

    !! Sonderfälle zuerst bedenken: leere Liste, 0, 1, negative Zahlen.
    !! Ein Produkt startet bei 1, eine Summe bei 0.
    """)
