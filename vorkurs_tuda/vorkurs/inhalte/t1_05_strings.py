# -*- coding: utf-8 -*-
"""Kapitel: Zeichenketten (Strings) – Text in Python (Vorlesung 1, Folien 30–35, Livecoding 1)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="strings",
    titel="Zeichenketten (Strings) – Text in Python",
    beschreibung="Anführungszeichen, Escape-Zeichen, len(), upper(), lower(), Index, Verketten mit +",
    quelle="Vorlesung 1, Livecoding 1",
    teil="tag1",
    icon="🔤")

k.lernziele([
    "Ich kann Strings mit ' und \" schreiben und Anführungszeichen im Text richtig einbauen",
    "Ich kann die Escape-Zeichen \\n, \\t, \\\" und \\\\ benutzen",
    "Ich kann len(), .upper(), .lower() und den Index [i] verwenden",
    "Ich kann Strings mit + verketten und weiß, warum str + int einen TypeError gibt",
])

# ── Erklärung 1: Was ist ein String? ─────────────────────────────────────
k.erklaerung("Was ist eine Zeichenkette?", r"""
    ## Eine Kette aus Zeichen

    Eine **Zeichenkette** (englisch: String, Typ `str`) ist eine Abfolge
    von Zeichen – Buchstaben, Ziffern, Leerzeichen, Sonderzeichen.

    :::analogie 📿 Die Perlenkette
    Ein String ist wie eine Kette aus Buchstaben-Perlen. Jede Perle hat eine
    Nummer – und gezählt wird ab **0**. Die Länge ist die Anzahl der Perlen.
    Zwei Ketten kannst du zu einer langen Kette zusammenknoten (das ist `+`).
    Aber du kannst keine Zahl an eine Perlenkette knoten – erst musst du die
    Zahl in eine Perle verwandeln (aus `5` wird `"5"`).
    :::

    :::visual string
    {"text": "Lorem", "markiert": [], "slice": null, "interaktiv": false}
    :::

    Man schreibt Strings in einfache ODER doppelte Anführungszeichen – in
    Python gibt es dabei KEINEN Unterschied:

        'Hallo'      "Hallo"      "12345"      '!@#$%'

    !! "12345" ist TEXT, keine Zahl – wie eine Hausnummer auf einem Schild:
    !! Man kann sie lesen, aber nicht mit ihr rechnen.
    """)

k.mc("Welche Schreibweise erzeugt in Python einen gültigen String?",
     ["Sowohl 'Hallo' als auch \"Hallo\"",
      "Nur \"Hallo\"",
      "Nur 'Hallo'",
      "Nur «Hallo»"],
     "In Python sind einfache und doppelte Anführungszeichen gleichwertig. "
     "(In Java übrigens nicht – dort nur \"...\".)")

k.wf("'12345' ist eine Zahl, mit der man direkt rechnen kann.", False,
     "In Anführungszeichen ist es ein Text (str). Zum Rechnen muss man ihn erst "
     "umwandeln, z.B. mit int('12345').")

k.ausgabe("print('Lorem' == 'lorem')",
          "Groß- und Kleinschreibung macht einen Unterschied → False.")

# ── Erklärung 2: Anführungszeichen und Escape ────────────────────────────
k.erklaerung("Anführungszeichen im Text und Escape-Zeichen", r"""
    ## Anführungszeichen IM Text

    Was passiert hier?

        print("Name: "Thomas"")

    Python liest `"Name: "` als fertigen String – danach steht `Thomas` ohne
    Anführungszeichen. Das ergibt einen **SyntaxError**. Zwei Lösungen:

      1. Außen die andere Sorte nehmen: `'Name: "Thomas"'`
         (genauso: `"Dillgurkensuppe gibt's heut' Mittag!"`)
      2. Das Zeichen **escapen**, also mit `\` markieren: `"Name: \"Thomas\""`

    :::code
    print('Name: "Thomas"')
    print("Name: \"Thomas\"")
    :::
    ---
    ## Escape-Zeichen

    Der Backslash `\` sagt: „Achtung, das nächste Zeichen ist besonders!“

    | Im Code | Bedeutung |
    |---|---|
    | `\n` | neue Zeile (englisch: new line) |
    | `\t` | Tabulator (Einrückung) |
    | `\"` bzw. `\'` | ein Anführungszeichen, das den String NICHT beendet |
    | `\\` | ein echter Backslash |

    :::code
    print("Zeile 1\nZeile 2")
    print("\tEingerückt")
    print("Zeilenumbrüche werden mit \\n markiert")
    :::

    :::achtung \n ist EIN Zeichen
    Im Code tippst du zwei Zeichen (`\` und `n`), im String steht aber nur
    EIN Zeichen: der Zeilenumbruch. `len("a\nb")` ist deshalb 3, nicht 4.
    Willst du wirklich `\n` sehen, schreib `\\n`.
    :::
    """)

k.ausgabe(r'print("Zeile1\nZeile2")',
          r"\n erzeugt einen Zeilenumbruch: Es werden zwei Zeilen ausgegeben.",
          tipp=r"Was bedeutet \n?")

k.ausgabe('print("Name: "Thomas"")',
          "Nach \"Name: \" ist der String zu Ende. Thomas steht dann ohne "
          "Anführungszeichen da, und Python versteht die Zeile nicht → SyntaxError.",
          tipp="Wo endet der erste String?")

k.ausgabe("print('Name: \"Thomas\"')",
          "Außen stehen einfache Anführungszeichen, also dürfen innen doppelte "
          "stehen. Sie werden ganz normal ausgegeben: Name: \"Thomas\"")

k.ausgabe(r'print("Ordner: C:\\neu")',
          r"\\ steht für EINEN echten Backslash. Deshalb wird hier kein Zeilenumbruch "
          r"erzeugt, sondern Ordner: C:\neu ausgegeben.",
          tipp="Zwei Backslashes hintereinander ...")

k.text("Was schreibst du in einen String, um eine neue Zeile zu beginnen?",
       ["\\n"],
       r"\n steht für 'new line' (neue Zeile).",
       tipp="Backslash plus ein Buchstabe ...")

# ── Erklärung 3: Länge und Index ─────────────────────────────────────────
k.erklaerung("Länge und Index", r"""
    ## len() und der Index

    `len(s)` liefert die **Länge** eines Strings, also die Anzahl der Zeichen.
    Leerzeichen zählen mit: `len("Hallo Welt")` ist 10.

    Mit eckigen Klammern holst du ein einzelnes Zeichen. Die Nummer heißt
    **Index** – und gezählt wird ab 0:

    :::visual string
    {"text": "Lorem", "markiert": [2], "slice": null, "interaktiv": false}
    :::

        s1 = 'Lorem'
        len(s1)       # 5
        s1[0]         # 'L'
        s1[2]         # 'r'
        s1[4]         # 'm'  – das letzte Zeichen hat Index len(s1) - 1

    :::achtung Der Index len(s) existiert nicht
    'Lorem' hat 5 Zeichen mit den Indizes 0 bis 4. `s1[5]` gibt es nicht →
    **IndexError: string index out of range**. Das letzte Zeichen bekommst du
    mit `s1[len(s1) - 1]`.
    :::

    :::code
    wort = "Python"
    print(len(wort))
    print(wort[0])
    print(wort[len(wort) - 1])
    :::
    """)

k.ausgabe("s1 = 'Lorem'\nprint(len(s1))", "'Lorem' hat 5 Zeichen.")
k.ausgabe("print('Lorem'[2])",
          "Index 2 ist das DRITTE Zeichen, weil ab 0 gezählt wird: L(0) o(1) r(2).",
          tipp="Zähle ab 0!")
k.ausgabe("print('Lorem'[0])", "Index 0 ist das erste Zeichen: L")
k.ausgabe("print(len('Hallo Welt'))",
          "Das Leerzeichen zählt mit: 5 + 1 + 4 = 10.")
k.ausgabe("print(len(''))", "Ein leerer String hat die Länge 0.")
k.ausgabe('wort = "Python"\nprint(wort[0] + wort[5])',
          "wort[0] ist 'P', wort[5] ist 'n' (P=0 y=1 t=2 h=3 o=4 n=5). Zusammen: Pn")

# ── Erklärung 4: Methoden und Funktionen ─────────────────────────────────
k.erklaerung("upper(), lower() – und ein Einschub zu Funktionen", r"""
    ## Großbuchstaben, Kleinbuchstaben

        s1 = 'Lorem'
        s1.upper()       # 'LOREM' – alles GROSS
        s1.lower()       # 'lorem' – alles klein

    :::achtung upper() ändert s1 nicht
    `s1.upper()` liefert einen NEUEN String. `s1` selbst bleibt 'Lorem'. Willst
    du das Ergebnis behalten, speichere es: `s1 = s1.upper()`.
    :::
    ---
    ## Kurzer Einschub: Funktionen

    `print(...)`, `len(...)`, `type(...)`, `s1.upper()` – das sind
    **Funktionen**:
      • eine benannte Folge von Anweisungen, die eine Aufgabe erledigt,
      • sie bekommen **Parameter** (in den Klammern) ...
      • ... und können einen **Rückgabewert** liefern.

    Form: `funktionsname(parameter1, parameter2, ...)`

    Funktionen wie `.upper()` stehen mit einem Punkt hinter einem Wert – sie
    gehören zu diesem Wert. Man nennt sie **Methoden**. Eigene Funktionen
    schreibst du an Tag 3.
    """)

k.ausgabe("print('Lorem'.lower())", ".lower() macht alles klein: lorem")
k.ausgabe("print('Lorem'.upper())", ".upper() macht alles groß: LOREM")
k.ausgabe('s = "Hallo"\ns.upper()\nprint(s)',
          "s.upper() erzeugt zwar 'HALLO', aber das Ergebnis wird nirgends gespeichert. "
          "s selbst bleibt unverändert: Hallo.",
          tipp="Wurde das Ergebnis von s.upper() irgendwo gespeichert?")
k.text("Welche Funktion liefert die Länge eines Strings?",
       ["len", "len()"],
       "len() wie 'length' (Länge): len('Lorem') ist 5.")

# ── Erklärung 5: Konkatenation ───────────────────────────────────────────
k.erklaerung("Strings verketten (Konkatenation)", r"""
    ## Strings aneinanderkleben

    Mit `+` klebt man Strings aneinander. Das heißt **Konkatenation**:

        'Hello, ' + 'World!'      →  'Hello, World!'
        "Eis" + "bär"             →  'Eisbär'

    :::vergleich ✘ Leerzeichen vergessen | ✔ Leerzeichen eingebaut
        name = "Anna"
        print("Hallo" + name)
    Ausgabe: HalloAnna
    |||
        name = "Anna"
        print("Hallo " + name)
    Ausgabe: Hallo Anna
    :::

    !! + funktioniert nur zwischen str und str! Python wandelt NICHT automatisch um.

        'a' + 'b'       # ok → 'ab'
        '1' + '1'       # ok → '11'  (Text, nicht 2!)
        1 + '1'         # FEHLER: TypeError

    Wie man aus der Zahl 1 den Text '1' macht, lernst du im nächsten Kapitel.
    ---
    ## Vorschau: Text einlesen mit input()

    In den Programmieraufgaben liest dein Programm schon Text ein:

        name = input()

    `input()` wartet, bis jemand etwas eintippt und Enter drückt, und liefert
    das Getippte als **String**. Mehr dazu im Kapitel „Ein- und Ausgabe“.

    :::code eingaben=Kim
    name = input()
    print("Hallo, " + name + "!")
    :::
    """)

k.ausgabe("print('Hello, ' + 'World!')",
          "Konkatenation: Die beiden Strings werden zusammengeklebt.")
k.ausgabe("print('1' + '1')",
          "Zwei Strings werden zusammengeklebt, nicht addiert: '11'.",
          tipp="Achte auf die Anführungszeichen!")
k.ausgabe("print(1 + '1')",
          "Eine Zahl und ein String können nicht mit + verbunden werden → TypeError.")
k.ausgabe('name = "Anna"\nprint("Hallo " + name + "!")',
          "Die drei Strings werden zu 'Hallo Anna!' verkettet.")
k.ausgabe('vorname = "Ada"\nnachname = "Lovelace"\nprint(vorname + nachname)',
          "+ fügt KEIN Leerzeichen ein. Die Strings kleben direkt aneinander: "
          "AdaLovelace. Richtig wäre vorname + \" \" + nachname.")
k.mc("Was heißt 'Konkatenation'?",
     ["Strings mit + aneinanderhängen",
      "Einen String in Großbuchstaben umwandeln",
      "Die Länge eines Strings bestimmen",
      "Einen String löschen"],
     "Konkatenation = Verkettung: 'Hello, ' + 'World!' → 'Hello, World!'")

# ── Praxisteil ───────────────────────────────────────────────────────────
k.luecke("Ergänze den Code, sodass er 6, PYTHON und P ausgibt.",
         """
         wort = "Python"
         print(___(wort))
         print(wort.___())
         print(wort[___])
         """,
         [["len"], ["upper"], ["0", "-6"]],
         "len(wort) ist 6, wort.upper() ist 'PYTHON', und das erste Zeichen hat "
         "den Index 0.",
         tipp="Länge, alles groß, erstes Zeichen.")

k.code(r"""
    ## Begrüßung

    Lies mit `input()` einen Namen ein und gib eine Begrüßung aus. Verkette
    die Teile mit `+`.

        Eingabe:  Anna
        Ausgabe:  Hallo, Anna!

    Achte auf das Komma, das Leerzeichen und das Ausrufezeichen.
    """,
    [P(["Anna"], ["Hallo, Anna!"]),
     P(["Ben"], ["Hallo, Ben!"]),
     P(["Lea Marie"], ["Hallo, Lea Marie!"], beschreibung="Name mit Leerzeichen"),
     P(["Kim"], nicht=["HalloKim", "Hallo,Kim"], beschreibung="Leerzeichen nach dem Komma")],
    """
    name = input()
    print("Hallo, " + name + "!")
    """,
    "input() liefert den Namen als String. Mit + werden \"Hallo, \", der Name und "
    "\"!\" zu einem String verkettet. Das Leerzeichen gehört in den ersten Teil.",
    tipps=["Speichere die Eingabe in einer Variable, z. B. name = input().",
           "Du brauchst drei Teile: \"Hallo, \", name und \"!\".",
           "print(\"Hallo, \" + name + \"!\")"],
    vorlage="name = input()\n",
    streng=True)

k.code(r"""
    ## Anführungszeichen-Profi

    Gib genau diese drei Zeilen aus:

        Name: "Thomas"
        Er sagte: 'Hallo!'
        Zeilenumbrüche werden mit \n markiert

    In der dritten Zeile soll wirklich ein Backslash und ein n zu sehen sein –
    kein Zeilenumbruch.
    """,
    [P(exakt=['Name: "Thomas"', "Er sagte: 'Hallo!'", r"Zeilenumbrüche werden mit \n markiert"],
       beschreibung="genau drei Zeilen")],
    r"""
    print('Name: "Thomas"')
    print("Er sagte: 'Hallo!'")
    print("Zeilenumbrüche werden mit \\n markiert")
    """,
    "Steht im Text ein doppeltes Anführungszeichen, nimm außen einfache – und "
    "umgekehrt. Alternativ escapest du mit \\\". Für einen echten Backslash "
    "schreibst du \\\\, sonst wird aus \\n ein Zeilenumbruch.",
    tipps=["Wechsle die Sorte der äußeren Anführungszeichen.",
           "Ein echter Backslash im String wird als \\\\ geschrieben.",
           "print('Name: \"Thomas\"') – und für Zeile 3: \"... mit \\\\n markiert\""])

k.code(r"""
    ## Initialen

    Lies einen Vornamen und einen Nachnamen ein (zwei Eingaben). Speichere die
    Initialen in der Variable `initialen` – als GROSSBUCHSTABEN mit Punkt –
    und gib sie aus.

        Eingaben:  anna, schmidt
        Ausgabe:   A.S.

    Auch wenn jemand die Namen klein tippt, sollen die Initialen groß sein.
    """,
    [P(["anna", "schmidt"], ["A.S."],
       nachspann='print("Großbuchstaben-Prüfung:", initialen == initialen.upper())'),
     P(["Ben", "Meier"], ["B.M."]),
     P(["ada", "lovelace"], ["A.L.", "Großbuchstaben-Prüfung: True"],
       nachspann='print("Großbuchstaben-Prüfung:", initialen == initialen.upper())',
       beschreibung="kleine Eingabe → große Initialen"),
     P(["deniz", "yilmaz"], ["Großbuchstaben-Prüfung: True"],
       nachspann='print("Großbuchstaben-Prüfung:", initialen == initialen.upper())',
       beschreibung="Initialen in Großbuchstaben")],
    """
    vorname = input()
    nachname = input()
    initialen = vorname[0].upper() + "." + nachname[0].upper() + "."
    print(initialen)
    """,
    "vorname[0] ist der erste Buchstabe. .upper() macht ihn groß. Mit + werden "
    "die Buchstaben und Punkte verkettet. Du kannst auch erst verketten und dann "
    "einmal .upper() auf alles anwenden.",
    tipps=["Den ersten Buchstaben bekommst du mit dem Index 0.",
           "vorname[0].upper() liefert den ersten Buchstaben groß.",
           "initialen = vorname[0].upper() + \".\" + nachname[0].upper() + \".\""],
    vorlage="vorname = input()\nnachname = input()\n",
    streng=True)

k.code(r"""
    ## Wort-Analyse

    Lies ein Wort ein und gib drei Zeilen aus:

        Eingabe:  Lorem
        Ausgabe:  Länge: 5
                  Erster Buchstabe: L
                  Letzter Buchstabe: m

    Das Programm muss für JEDES Wort funktionieren, auch für ein Wort mit nur
    einem Buchstaben. (Tipp: Der letzte Index ist `len(wort) - 1`.)
    """,
    [P(["Lorem"], ["Länge: 5", "Erster Buchstabe: L", "Letzter Buchstabe: m"]),
     P(["Python"], ["Länge: 6", "Erster Buchstabe: P", "Letzter Buchstabe: n"]),
     P(["a"], ["Länge: 1", "Erster Buchstabe: a", "Letzter Buchstabe: a"],
       beschreibung="Wort mit einem Buchstaben"),
     P(["Darmstadt"], ["Länge: 9", "Letzter Buchstabe: t"])],
    """
    wort = input()
    print("Länge: " + str(len(wort)))
    print("Erster Buchstabe: " + wort[0])
    print("Letzter Buchstabe: " + wort[len(wort) - 1])
    """,
    "len(wort) liefert eine Zahl. Damit du sie mit + an einen Text hängen kannst, "
    "machst du mit str() einen Text daraus (mehr dazu im nächsten Kapitel). "
    "Alternativ: print(\"Länge:\", len(wort)). Der letzte Buchstabe hat den Index "
    "len(wort) - 1, weil ab 0 gezählt wird.",
    tipps=["Für die Länge gibt es len(), für einzelne Zeichen den Index in [ ].",
           "Mit print(\"Länge:\", len(wort)) musst du nichts umwandeln.",
           "Letzter Buchstabe: wort[len(wort) - 1]"],
    vorlage="wort = input()\n",
    streng=True)

k.zusammenfassung(r"""
    ## Das Wichtigste aus Kapitel 5

      • Strings schreibt man in `'...'` oder `"..."` – kein Unterschied.
      • Anführungszeichen im Text: außen die andere Sorte oder `\"` bzw. `\'`.
      • Escape: `\n` neue Zeile, `\t` Tabulator, `\\` echter Backslash.

    | Werkzeug | Beispiel | Ergebnis |
    |---|---|---|
    | Länge | `len("Lorem")` | `5` |
    | Index (ab 0) | `"Lorem"[0]` | `'L'` |
    | letztes Zeichen | `s[len(s) - 1]` | `'m'` |
    | groß / klein | `"Lorem".upper()` | `'LOREM'` |
    | verketten | `"Eis" + "bär"` | `'Eisbär'` |

    !! + verbindet nur str mit str. 1 + '1' → TypeError.

        name = input()                    # liefert immer einen str
        print("Hallo, " + name + "!")     # Leerzeichen selbst einbauen
    """)
