# -*- coding: utf-8 -*-
"""Kapitel: Typumwandlung – int(), float(), str(), bool() (Vorlesung 1, Folien 36–38, Livecoding 1)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="typumwandlung",
    titel="Typumwandlung – int(), float(), str(), bool()",
    beschreibung="Werte von einem Typ in einen anderen umwandeln",
    quelle="Vorlesung 1, Livecoding 1",
    teil="tag1",
    icon="🔄")

k.lernziele([
    "Ich kann Werte mit int(), float(), str() und bool() umwandeln",
    "Ich weiß, dass int() Nachkommastellen abschneidet und wann ein ValueError entsteht",
    "Ich kann vorhersagen, was bool() liefert – auch bei bool('False')",
    "Ich kann verschachtelte Umwandlungen von innen nach außen auswerten",
])

# ── Erklärung 1: Warum umwandeln? ────────────────────────────────────────
k.erklaerung("Typen umwandeln (Konvertierung)", r"""
    ## Warum umwandeln?

    Manchmal hat ein Wert den „falschen“ Typ. Beispiel: Jemand tippt sein
    Alter ein – Python bekommt aber den TEXT `"19"`, nicht die Zahl `19`.
    Um damit zu rechnen, musst du den Typ ändern. Das heißt
    **Typumwandlung** oder **Typkonvertierung**.

    :::analogie 💱 Geld wechseln
    In der Wechselstube tauschst du Euro gegen Dollar. Der Wert bleibt
    (ungefähr) gleich, nur die Form ändert sich. Aber: Nicht alles lässt sich
    tauschen. Mit Spielgeld bekommst du keine Dollar – und aus dem Text `'a'`
    bekommst du keine Zahl. Dann meldet Python einen **ValueError**.
    :::

    | Funktion | wandelt um in ... | Beispiel | Ergebnis |
    |---|---|---|---|
    | `int()` | Ganzzahl | `int('3')` | `3` |
    | `float()` | Fließkommazahl | `float('3.0')` | `3.0` |
    | `str()` | Zeichenkette | `str(3)` | `'3'` |
    | `bool()` | Wahrheitswert | `bool(5)` | `True` |
    ---
    ## Derselbe Wert, verschiedene Typen

    :::visual variablen
    {"vars": [{"name": "x", "wert": "'19.0'", "typ": "str"}],
     "schritte": [[{"name": "x", "wert": "'19'", "typ": "str"}],
                  [{"name": "x", "wert": "19", "typ": "int"}],
                  [{"name": "x", "wert": "19.0", "typ": "float"}],
                  [{"name": "x", "wert": "'19.0'", "typ": "str"}]],
     "texte": ["x = '19'", "x = int(x)", "x = float(x)", "x = str(x)"]}
    :::

    Ohne Umwandlung geht es schief:

    :::code
    x = "3"
    print(int(x) + 2)
    print(x + 2)
    :::

    :::achtung Datentyp int ≠ Funktion int()
    Der **Datentyp** `int` (die Art des Werts) und die **Funktion** `int()`
    (die etwas umwandelt) heißen gleich, sind aber zwei verschiedene Dinge.
    `type(5)` zeigt den Datentyp, `int("5")` ruft die Funktion auf.
    :::
    """)

k.ausgabe('print("2" + str(5))',
          "Erst wird 5 zu '5', dann werden die Strings verkettet: '25'.")
k.ausgabe('print(int("2") + 5)',
          "Erst wird '2' zu 2, dann wird gerechnet: 2 + 5 = 7.")
k.ausgabe('x = "3"\nprint(x + 2)',
          "x ist ein String. String + Zahl geht nicht → TypeError. Richtig wäre "
          "int(x) + 2 (ergibt 5) oder x + str(2) (ergibt '32').",
          tipp="Welchen Typ hat x?")
k.wf("Der Datentyp int und die Funktion int() sind ein und dasselbe.", False,
     "Sie heißen gleich, sind aber verschiedene Dinge: int ist die Art eines Werts "
     "(z. B. type(5)), int() ist eine Funktion, die einen Wert in eine Ganzzahl "
     "umwandelt.")

# ── Erklärung 2: Die wichtigsten Regeln ──────────────────────────────────
k.erklaerung("Die wichtigsten Regeln", r"""
    ## int() schneidet ab

    :::analogie ✂️ Die Schere
    `int()` auf eine Kommazahl ist wie eine Schere: Alles nach dem Punkt
    wird abgeschnitten. Gerundet wird NICHT – auch nicht bei .99. Bei
    negativen Zahlen schneidet die Schere Richtung 0: `int(-3.9)` → `-3`.
    :::

        int(3.17)    → 3
        int(3.99)    → 3        (nicht 4!)
        int(-3.9)    → -3
    ---
    ## Text in Zahlen umwandeln

    `int()` von einem Text klappt nur, wenn der Text eine **Ganzzahl** ist:

        int('5')       → 5
        int('a')       → ValueError  (was soll 'a' als Zahl sein?)
        int('4.5')     → ValueError  (Text mit Punkt ist keine Ganzzahl)
        float('4.5')   → 4.5

    :::achtung Text mit Punkt in eine Ganzzahl verwandeln
    `int('4.5')` scheitert. Der Trick geht in zwei Stufen: erst `float()`,
    dann `int()`: `int(float('4.5'))` → `4`.
    :::

    Weitere Regeln:
      • `float(5)` → `5.0` (hängt `.0` an)
      • `str(3.1415)` → `'3.1415'` (aus allem wird Text)
      • Die Funktion heißt `str()`, nicht `string()`. `string(3.1415)` kennt
        Python nicht → NameError.
    """)

k.ausgabe("print(int(3.99))",
          "int() RUNDET NICHT, es schneidet ab. Deshalb 3 und nicht 4!",
          tipp="Runden oder abschneiden?")
k.mc("Was macht int(7.9)?",
     ["Es ergibt 7 (Nachkommastellen werden abgeschnitten)",
      "Es ergibt 8 (es wird gerundet)",
      "Es ergibt einen ValueError",
      "Es ergibt 7.9"],
     "int() von einem float schneidet immer ab, es rundet nie.")
k.ausgabe("print(int(-3.9))",
          "int() schneidet Richtung 0 ab: Aus -3.9 wird -3 (nicht -4).",
          tipp="Nachkommastellen einfach weglassen.")
k.ausgabe("print(int('3.5'))",
          "Der Text '3.5' ist keine GANZZAHL → ValueError. Richtig wäre: int(float('3.5')) → 3.")
k.ausgabe('print(int(float("4.5")))',
          "Von innen nach außen: float('4.5') → 4.5, dann int(4.5) → 4 (abgeschnitten).")
k.mc("Was passiert bei   string(3.1415)   ?",
     ["NameError – die Funktion heißt str(), nicht string()",
      "Es ergibt '3.1415'",
      "Es ergibt 3",
      "ValueError – 3.1415 lässt sich nicht umwandeln"],
     "Python kennt keine Funktion string. Der Typ und die Funktion heißen str: "
     "str(3.1415) ergibt '3.1415'.")

# ── Erklärung 3: bool() ──────────────────────────────────────────────────
k.erklaerung("bool() – die Überraschungen", r"""
    ## Leer oder nicht leer?

    :::analogie 📦 Die Schachtel
    `bool()` öffnet eine Schachtel und schaut nur: Ist sie leer? Was drin
    liegt, liest es NICHT. Leer (0, `0.0`, `''`, `None`) → `False`.
    Alles andere → `True`. Auch ein Zettel mit der Aufschrift „False“ ist
    ein Inhalt – also `True`.
    :::

    | Ausdruck | Ergebnis | Warum? |
    |---|---|---|
    | `bool(0)` | `False` | Null |
    | `bool(5)`, `bool(-2)` | `True` | nicht Null |
    | `bool('')` | `False` | leerer Text |
    | `bool('Hallo')` | `True` | nicht leer |
    | `bool('False')` | `True` | nicht leer! |

    :::info Auf Folie 36 steht `bool('True')` als Beispiel
    Das Ergebnis ist zwar `True` – aber nicht, weil im Text „True“ steht,
    sondern nur, weil der Text nicht leer ist. `bool('False')` ist genauso `True`.
    :::

    Umgekehrt wird ein Wahrheitswert mit `str()` zum Text: `str(3 == 3)` → `'True'`.
    """)

k.ausgabe("print(bool(0))", "0 wird zu False.")
k.ausgabe("print(bool(''))", "Ein leerer String wird zu False.")
k.ausgabe("print(bool('False'))",
          "Überraschung! 'False' ist ein NICHT-LEERER Text, also True. bool() liest "
          "den Inhalt nicht, es prüft nur: leer oder nicht?",
          tipp="Ist der Text leer?")
k.mc("Welcher dieser Werte ergibt mit bool() den Wert False?",
     ["0", "'False'", "-1", "'0'"],
     "Nur die Zahl 0 ist 'leer'. '0' und 'False' sind nicht-leere TEXTE → True. "
     "-1 ist nicht 0 → True.")
k.ausgabe("print(str(3 == 3) + '!')",
          "3 == 3 ergibt True. str(True) ist der Text 'True', und daran wird '!' "
          "gehängt: True!")

# ── Erklärung 4: Verschachteln ───────────────────────────────────────────
k.erklaerung("Verschachtelte Umwandlungen", r"""
    ## Von innen nach außen – wie eine Zwiebel

    Umwandlungen kann man ineinander schachteln. Python wertet sie von INNEN
    nach AUSSEN aus – Schale für Schale:

    :::visual ablauf
    {"schritte": [{"icon": "🧅", "text": "float(int(str(int(\"3\"))))"},
                  {"icon": "1️⃣", "text": "int(\"3\") → 3"},
                  {"icon": "2️⃣", "text": "str(3) → '3'"},
                  {"icon": "3️⃣", "text": "int('3') → 3"},
                  {"icon": "✅", "text": "float(3) → 3.0"}]}
    :::

    `type()` hilft dir, jeden Zwischenschritt zu überprüfen:

    :::trace
    x = 5
    print(type(x))
    print(type(str(x)))
    y = float(str(x))
    print(y, type(y))
    :::
    """)

k.ausgabe('print(type(float("7")))',
          "float('7') ergibt 7.0, und dessen Typ ist float.", akzeptiert=["float"])
k.ausgabe('print(int(str(4) + str(2)) + 1)',
          "Innen: str(4) + str(2) = '42' (Text verkettet). int('42') = 42. Plus 1 → 43.",
          tipp="Erst die Texte verketten, dann umwandeln, dann rechnen.")
k.ausgabe('print(float(str(2) + "5") / 10)',
          "Innen: str(2) + \"5\" = '25' (Text verkettet). float('25') = 25.0. "
          "Geteilt durch 10 → 2.5.",
          tipp="Erst verketten, dann umwandeln, dann teilen.")

# ── Praxisteil ───────────────────────────────────────────────────────────
k.puzzle("Bringe die Zeilen in die richtige Reihenfolge: Das Programm liest ein Alter ein "
         "und gibt aus, wie alt man nächstes Jahr ist.",
         """
         text = input("Wie alt bist du? ")
         alter = int(text)
         alter = alter + 1
         print("Nächstes Jahr bist du " + str(alter))
         """,
         "Erst einlesen (str), dann in int umwandeln, dann rechnen und zum Ausgeben "
         "wieder in str umwandeln.",
         tipp="input() liefert Text – damit kann man noch nicht rechnen.",
         ablenker=['print("Nächstes Jahr bist du " + alter)'])

k.code(r"""
    ## Text oder Zahl?

    Lies zwei Eingaben ein. Gib danach zwei Zeilen aus:

      1. die beiden Eingaben als TEXT aneinandergehängt
      2. die SUMME der beiden Zahlen

        Eingaben:  12, 30
        Ausgabe:   1230
                   42

    Benutze `input()` ohne Text in den Klammern.
    """,
    [P(["12", "30"], ["1230", "42"]),
     P(["1", "1"], ["11", "2"]),
     P(["0", "7"], ["07", "7"], beschreibung="führende Null bleibt im Text erhalten"),
     P(["-5", "5"], ["-55", "0"], beschreibung="negative Zahl")],
    """
    a = input()
    b = input()
    print(a + b)
    print(int(a) + int(b))
    """,
    "input() liefert Strings – a + b klebt sie aneinander. Für die Summe wandelst "
    "du beide mit int() in Zahlen um.",
    tipps=["Was macht + mit zwei Strings, was mit zwei Zahlen?",
           "Für die zweite Zeile brauchst du int() um beide Eingaben.",
           "print(a + b) und print(int(a) + int(b))"],
    vorlage="a = input()\nb = input()\n")

k.code(r"""
    ## Nur der ganze Teil

    Lies eine Kommazahl ein und gib ihren ganzzahligen Teil aus – ohne zu runden:

        Eingabe:  3.99
        Ausgabe:  Ganzer Teil: 3

    Das Programm soll auch mit negativen Zahlen und mit ganzen Zahlen wie `7`
    funktionieren.
    """,
    [P(["3.17"], ["Ganzer Teil: 3"]),
     P(["3.99"], ["Ganzer Teil: 3"], beschreibung="nicht runden"),
     P(["-2.5"], ["Ganzer Teil: -2"], beschreibung="negative Zahl"),
     P(["7"], ["Ganzer Teil: 7"], beschreibung="ganze Zahl als Eingabe"),
     P(["0.5"], ["Ganzer Teil: 0"])],
    """
    zahl = float(input())
    print("Ganzer Teil:", int(zahl))
    """,
    "Der Text '3.99' muss erst mit float() zur Zahl werden – int('3.99') gäbe einen "
    "ValueError. Danach schneidet int() die Nachkommastellen ab: aus 3.99 wird 3, "
    "aus -2.5 wird -2.",
    tipps=["int(input()) scheitert bei '3.99'. Welche Umwandlung klappt mit Punkt?",
           "Zwei Stufen: erst float(), dann int().",
           "zahl = float(input()) und print(\"Ganzer Teil:\", int(zahl))"],
    streng=True)

k.code(r"""
    ## Einkauf an der Kasse

    Lies nacheinander ein: den Namen eines Artikels, den Stückpreis (Kommazahl)
    und die Menge (ganze Zahl). Gib dann aus:

        Eingaben:  Brezel, 0.5, 4
        Ausgabe:   4 x Brezel kosten 2.0 Euro

    Verwende `+` zum Verketten. Dafür musst du Zahlen mit `str()` in Text
    umwandeln.
    """,
    [P(["Brezel", "0.5", "4"], ["4 x Brezel kosten 2.0 Euro"]),
     P(["Kaffee", "2.5", "2"], ["2 x Kaffee kosten 5.0 Euro"]),
     P(["Apfel", "0.25", "8"], ["8 x Apfel kosten 2.0 Euro"]),
     P(["Wasser", "1", "0"], ["0 x Wasser kosten 0.0 Euro"], beschreibung="Menge 0, Preis ohne Punkt")],
    """
    artikel = input("Artikel: ")
    preis = float(input("Preis: "))
    menge = int(input("Menge: "))
    gesamt = preis * menge
    print(str(menge) + " x " + artikel + " kosten " + str(gesamt) + " Euro")
    """,
    "Der Preis braucht float(), die Menge int(). preis * menge ist ein float (z. B. "
    "2.0). Zum Verketten mit + müssen menge und gesamt mit str() zu Text werden – "
    "sonst gibt es einen TypeError.",
    pflicht=["float(", "int(", "str("],
    tipps=["Drei input()-Aufrufe – zwei davon brauchen eine Umwandlung.",
           "preis = float(input()), menge = int(input()), gesamt = preis * menge",
           "print(str(menge) + \" x \" + artikel + \" kosten \" + str(gesamt) + \" Euro\")"],
    streng=True)

k.zusammenfassung(r"""
    ## Das Wichtigste aus Kapitel 6

    | Aufruf | Ergebnis | Merke |
    |---|---|---|
    | `int(3.99)` | `3` | schneidet ab, rundet nie |
    | `int('5')` | `5` | Text mit Ganzzahl klappt |
    | `int('4.5')` | ValueError | erst `float()`, dann `int()` |
    | `int('a')` | ValueError | kein Zahltext |
    | `float(5)` | `5.0` | |
    | `str(3.1415)` | `'3.1415'` | Funktion heißt `str`, nicht `string` |
    | `bool(0)`, `bool('')` | `False` | leer/Null |
    | `bool('False')` | `True` | nicht leer! |

    !! Verschachtelt wird von innen nach außen ausgewertet.

        zahl = int(input("Zahl: "))       # Text → Zahl
        print("Doppelt: " + str(zahl * 2))  # Zahl → Text

    Datentyp `int` ≠ Funktion `int()`.
    """)
