# -*- coding: utf-8 -*-
"""Kapitel: Datentypen – Welche Art von Daten? (Vorlesung 1, Folien 12–14)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="datentypen",
    titel="Datentypen – Welche Art von Daten?",
    beschreibung="bool, int, float, str, None und die Funktion type()",
    quelle="Vorlesung 1",
    teil="tag1",
    icon="🏷️")

k.lernziele([
    "Ich kann erklären, warum Daten im Computer einen Typ brauchen",
    "Ich kann die Typen bool, int, float, str und NoneType an Beispielen erkennen",
    "Ich kann mit type() den Typ eines Werts herausfinden",
    "Ich kann für eine Information aus dem Alltag den passenden Typ wählen",
])

# ── Erklärung 1: Bits brauchen eine Deutung ──────────────────────────────
k.erklaerung("Was sind Daten – und wer sind diese 'Typen'?", r"""
    ## Alles ist 0 und 1

    Im Computer wird alles als **Binärzahl** gespeichert, also nur mit 0 und 1.
    Der Computer selbst weiß aber nicht, was diese Bits BEDEUTEN.

    Beispiel aus der Vorlesung: Die Bits `01000001` können bedeuten:
      • die Zahl 65
      • oder den Buchstaben 'A'

    :::analogie 📝 Der Zettel mit „0612“
    Auf einem Zettel steht nur „0612“. Ist das eine Uhrzeit (06:12 Uhr), ein
    Datum (6. Dezember), die Zahl 612 oder eine Vorwahl? Ohne Hinweis kannst
    du nichts damit anfangen. Schreibt jemand „Uhrzeit:“ davor, ist alles klar.

    Genau diesen Hinweis gibt der **Datentyp**: Er steht unsichtbar an jedem
    Wert und sagt dem Computer, wie er die Bits lesen soll.
    :::

    !! Der DATENTYP legt fest, wie die Daten interpretiert werden.

    :::info Exkurs: Zeichen und Zahlen
    Mit `ord()` siehst du die Zahl hinter einem Zeichen, mit `chr()` das
    Zeichen hinter einer Zahl. Gleiche Bits, zwei Deutungen:
    :::

    :::code
    print(ord("A"))
    print(chr(65))
    :::
    """)

k.wf("Die Bits 01000001 können sowohl die Zahl 65 als auch den Buchstaben 'A' bedeuten.", True,
     "Genau deshalb gibt es Datentypen: Der Typ legt fest, wie die Bits interpretiert werden.")

k.wf("Der Computer weiß von selbst, wie er eine Folge von Bits verstehen soll.", False,
     "Nein – der Computer sieht nur 0 und 1. Erst der Datentyp gibt den Bits eine Bedeutung.")

k.mc("Was legt der Datentyp eines Werts fest?",
     ["Wie die gespeicherten Bits interpretiert werden",
      "Wie viele Variablen das Programm haben darf",
      "In welcher Farbe der Wert angezeigt wird",
      "Wie schnell der Computer rechnet"],
     "Bits allein haben keine Bedeutung. Der Typ sagt, ob z. B. 01000001 als "
     "Zahl 65 oder als Zeichen 'A' gelesen wird.")

# ── Erklärung 2: Die fünf Typen ──────────────────────────────────────────
k.erklaerung("Die 5 wichtigsten Datentypen", r"""
    ## Die 5 wichtigsten Datentypen im Vorkurs

    | Typ | Bedeutung | Beispiele | Alltag |
    |---|---|---|---|
    | `bool` | Wahrheitswert | `True`, `False` | Lichtschalter an/aus |
    | `int` | Ganzzahl | `177013`, `-2`, `0` | Anzahl Äpfel im Korb |
    | `float` | Fließkommazahl | `21.5`, `-0.135` | Preis, Temperatur |
    | `str` | Zeichenkette (Text) | `"lorem"`, `'ipsum'` | Name, Adresse |
    | `NoneType` | Nulltyp | `None` | leeres Formularfeld |

    :::visual typen
    {"werte": ["True", "177013", "-2", "21.5", "-0.135", "'lorem'", "\"ipsum\"", "None"]}
    :::
    ---
    ## Woran erkennst du den Typ?

      • `True` und `False` schreibt man mit GROSSEM Anfangsbuchstaben.
      • Kommazahlen schreibt man mit PUNKT: `2.5`, nicht `2,5`.
      • `10.0` ist ein float (wegen des Punkts), `10` ist ein int.
      • `"5"` in Anführungszeichen ist ein str – also Text, keine Zahl!
      • `None` bedeutet „hier ist (noch) nichts“. Das ist nicht dasselbe wie
        `0`, `False` oder `""`.

    :::visual typen
    {"werte": ["10", "10.0", "'10'", "True", "'True'", "None"]}
    :::

    :::achtung Kleingeschrieben und kopiert
    `true` (klein) kennt Python nicht. Python hält es für einen unbekannten
    Namen und meldet einen **NameError**. Richtig ist `True`.

    Kopierst du Code aus einer PDF, landen dort oft **typografische**
    Anführungszeichen wie ’Lorem’ oder ”ipsum” statt `'Lorem'` und `"ipsum"`.
    Dann meldet Python `SyntaxError: invalid character`. Tippe
    Anführungszeichen deshalb immer selbst ein.
    :::
    """)

k.mc("Welchen Datentyp hat der Wert 177013?",
     ["int", "float", "str", "bool"],
     "Eine ganze Zahl ohne Punkt und ohne Anführungszeichen ist ein int (integer = Ganzzahl).")

k.mc("Welchen Datentyp hat der Wert -0.135?",
     ["float", "int", "str", "NoneType"],
     "Der Punkt macht es zur Fließkommazahl: float.")

k.mc("Welchen Datentyp hat der Wert \"lorem\"?",
     ["str", "bool", "float", "int"],
     "Alles in Anführungszeichen (egal ob ' oder \") ist eine Zeichenkette: str.")

k.mc("Welchen Datentyp hat der Wert None?",
     ["NoneType", "bool", "str", "int"],
     "None ist der einzige Wert vom Typ NoneType – er bedeutet 'kein Wert'.")

k.mc("Wie schreibt man den Wahrheitswert 'wahr' in Python?",
     ["True", "true", "TRUE", "\"wahr\""],
     "Nur True mit großem T. 'true' (klein) kennt Python nicht → NameError.")

k.wf("In Python schreibt man Kommazahlen mit einem Komma, also 3,5.", False,
     "Python schreibt Kommazahlen mit PUNKT: 3.5. Ein Komma trennt in Python "
     "verschiedene Werte voneinander.")

# ── Erklärung 3: type() ──────────────────────────────────────────────────
k.erklaerung("Den Typ herausfinden: type()", r"""
    ## Python fragen: Welcher Typ ist das?

    Mit der Funktion `type()` fragst du Python nach dem Typ eines Werts.
    Mit `print()` drumherum siehst du die Antwort auch in einer Datei:

    :::code
    print(type(5))
    print(type(2.5))
    print(type("Hallo"))
    print(type(True))
    print(type(None))
    :::

    Die Ausgabe `<class 'int'>` heißt einfach: „Das ist ein int.“

    `print()` kann auch mehrere Werte auf einmal ausgeben, getrennt durch
    Kommas. Python setzt dann ein Leerzeichen dazwischen:

    :::code
    print(42, type(42))
    print("42", type("42"))
    :::

    !! Anführungszeichen machen aus allem Text: "42" ist ein str, 42 ein int.
    """)

k.ausgabe('print(type("5"))',
          "\"5\" steht in Anführungszeichen → das ist TEXT, keine Zahl! Typ: str.",
          akzeptiert=["str"])

k.ausgabe("print(type(-7))",
          "Auch negative ganze Zahlen sind Ganzzahlen → int.", akzeptiert=["int"])

k.ausgabe("print(type(3.0))",
          "3.0 hat einen Punkt → float. Auch wenn nach dem Punkt nur eine 0 steht!",
          akzeptiert=["float"])

k.ausgabe('print(type("True"))',
          "Vorsicht, Anführungszeichen! \"True\" ist ein Text aus vier Buchstaben, "
          "kein Wahrheitswert → str.",
          akzeptiert=["str"],
          tipp="Schau, ob Anführungszeichen um den Wert stehen.")

k.ausgabe("print(type(False))",
          "False ist (wie True) ein Wahrheitswert → bool.", akzeptiert=["bool"])

k.ausgabe("print(type(None))",
          "None hat seinen ganz eigenen Typ: NoneType.", akzeptiert=["NoneType"])

# ── Erklärung 4: Welcher Typ passt? ──────────────────────────────────────
k.erklaerung("Welcher Typ passt zu meinen Daten?", r"""
    ## Die richtige Schublade wählen

    Beim Programmieren überlegst du dir für jede Information: Was will ich
    damit tun? Daraus folgt der Typ.

    | Information | Typ | Warum? |
    |---|---|---|
    | Anzahl Personen in der WG | `int` | man zählt in ganzen Zahlen |
    | Preis einer Pizza | `float` | hat Nachkommastellen: `8.5` |
    | Hat der Laden geöffnet? | `bool` | nur ja oder nein |
    | Name einer Stadt | `str` | Text |
    | Telefonnummer `0151 2345678` | `str` | man rechnet nicht damit |
    | Zweitname (wenn es keinen gibt) | `NoneType` | „nichts vorhanden“ |

    :::achtung Zahlen, mit denen man nicht rechnet
    Telefonnummern oder Postleitzahlen wie `"01067"` (Dresden) speichert man
    als Text. Als Zahl würde die führende 0 verschwinden: aus `01067` würde
    `1067` – und rechnen will damit sowieso niemand.
    :::
    """)

k.mc("Du willst speichern, ob ein Laden gerade geöffnet hat. Welcher Typ passt?",
     ["bool", "int", "float", "str"],
     "Offen oder zu – also ja oder nein → Wahrheitswert: True oder False (bool).")

k.mc("Du willst die Anzahl der Personen in deiner WG speichern. Welcher Typ passt?",
     ["int", "float", "bool", "NoneType"],
     "Personen zählt man in ganzen Zahlen – es gibt keine 2,5 Mitbewohner. → int")

k.mc("Du willst den Preis einer Pizza speichern (8,50 €). Welcher Typ passt?",
     ["float", "int", "bool", "NoneType"],
     "Preise haben Nachkommastellen → float, geschrieben als 8.5 (mit Punkt!).")

k.mc("Du willst eine Handynummer wie 0151 2345678 speichern. Welcher Typ ist am sinnvollsten?",
     ["str", "int", "float", "bool"],
     "Mit Telefonnummern rechnet man nicht. Außerdem würde bei einer Zahl die "
     "führende 0 verschwinden. → als Text (str) speichern.")

k.mc("Was bedeutet None?",
     ["Kein Wert / nichts vorhanden",
      "Die Zahl 0",
      "Falsch (False)",
      "Ein leerer Text"],
     "None ist ein eigener Wert für 'nichts'. Es ist NICHT dasselbe wie 0, "
     "False oder \"\" – auch wenn es sich manchmal ähnlich anfühlt.")

# ── Praxisteil ───────────────────────────────────────────────────────────
k.luecke("Ergänze in den Kommentaren, welchen Typ Python jeweils ausgibt "
         "(nur den Namen, z. B. int).",
         """
         print(type(42))       # <class '___'>
         print(type(4.2))      # <class '___'>
         print(type("42"))     # <class '___'>
         print(type(False))    # <class '___'>
         """,
         [["int"], ["float"], ["str"], ["bool"]],
         "42 ist eine Ganzzahl (int), 4.2 hat einen Punkt (float), \"42\" steht in "
         "Anführungszeichen (str), False ist ein Wahrheitswert (bool).",
         tipp="Achte auf Punkt, Anführungszeichen und Großbuchstaben.")

k.code(r"""
    ## Typ-Steckbrief für den Pizzaabend

    Lege diese fünf Variablen an. Die Werte darfst du dir aussuchen, aber der
    Typ muss stimmen. (Variablen lernst du in Kapitel 4 genauer kennen. Hier
    reicht: `name = wert` speichert einen Wert unter einem Namen, z. B.
    `anzahl_personen = 4`.)

    | Variable | Typ |
    |---|---|
    | `anzahl_personen` | int |
    | `pizza_preis` | float |
    | `lieblingsessen` | str |
    | `hat_hunger` | bool |
    | `nachtisch` | None (es gibt keinen) |

    Gib danach mit `print(type(...))` den Typ jeder Variable aus – jeden in
    einer eigenen Zeile und in der Reihenfolge der Tabelle. Die Ausgabe
    beginnt also mit `<class 'int'>`.
    """,
    [F("type(anzahl_personen).__name__", "int"),
     F("type(pizza_preis).__name__", "float"),
     F("type(lieblingsessen).__name__", "str"),
     F("type(hat_hunger).__name__", "bool"),
     F("nachtisch is None", True),
     P(exakt=["<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'bool'>",
              "<class 'NoneType'>"], beschreibung="fünf Zeilen mit den Typen")],
    """
    anzahl_personen = 4
    pizza_preis = 8.5
    lieblingsessen = "Pizza Margherita"
    hat_hunger = True
    nachtisch = None
    print(type(anzahl_personen))
    print(type(pizza_preis))
    print(type(lieblingsessen))
    print(type(hat_hunger))
    print(type(nachtisch))
    """,
    "Der Typ ergibt sich aus der Schreibweise des Werts: ohne Punkt → int, mit "
    "Punkt → float, in Anführungszeichen → str, True/False → bool, None → NoneType. "
    "Häufige Fehler: pizza_preis = 8 (das wäre int) oder hat_hunger = \"True\" "
    "(das wäre str).",
    tipps=["Eine Variable legst du mit name = wert an.",
           "Ein float braucht einen Punkt (z. B. 8.5), ein bool heißt True oder False.",
           "anzahl_personen = 4 und darunter print(type(anzahl_personen)) – "
           "genauso für die anderen vier."],
    vorlage="anzahl_personen = ...\n")

k.code(r"""
    ## Die richtige Schublade

    Speichere die folgenden Informationen aus einem Café in Variablen
    (`name = wert`). Wähle selbst den passenden Typ – genau wie in der
    Tabelle der Erklärung.

      • `telefon`: die Telefonnummer `06151 123456`
      • `temperatur`: draußen sind es 21,5 Grad
      • `anzahl_tische`: im Café stehen 12 Tische
      • `ist_geoeffnet`: das Café hat gerade geöffnet (ja)
      • `wlan_passwort`: es gibt kein WLAN-Passwort (nichts vorhanden)

    Eine Ausgabe ist nicht nötig. Die Tests prüfen Typ und Wert.
    """,
    [F("type(telefon).__name__", "str"),
     F("telefon", "06151 123456"),
     F("type(temperatur).__name__", "float"),
     F("temperatur", 21.5),
     F("type(anzahl_tische).__name__", "int"),
     F("anzahl_tische == 12 and ist_geoeffnet is True and wlan_passwort is None", True)],
    """
    telefon = "06151 123456"
    temperatur = 21.5
    anzahl_tische = 12
    ist_geoeffnet = True
    wlan_passwort = None
    """,
    "Die Telefonnummer ist Text (führende 0, Leerzeichen, man rechnet nicht damit). "
    "21,5 schreibt Python als 21.5 (float). Tische zählt man (int). Ja/nein ist ein "
    "bool. Und für „nichts vorhanden“ gibt es None.",
    tipps=["Frag dich bei jeder Information: Text, ganze Zahl, Kommazahl, ja/nein oder nichts?",
           "Kommazahlen mit Punkt schreiben. Die Telefonnummer in Anführungszeichen.",
           "telefon = \"06151 123456\", temperatur = 21.5, anzahl_tische = 12, "
           "ist_geoeffnet = True, wlan_passwort = None"])

k.zusammenfassung(r"""
    ## Das Wichtigste aus Kapitel 2

    !! Der Datentyp legt fest, wie Daten interpretiert werden.

    | Typ | Bedeutung | Beispiele |
    |---|---|---|
    | `bool` | Wahrheitswert | `True`, `False` |
    | `int` | Ganzzahl | `42`, `-2`, `0` |
    | `float` | Fließkommazahl | `2.5`, `10.0` |
    | `str` | Zeichenkette | `"Hallo"`, `'42'` |
    | `NoneType` | Nulltyp | `None` |

        print(type(42))      # <class 'int'>
        print(type("42"))    # <class 'str'>

      • Punkt statt Komma: `3.5`.
      • `True`/`False` groß schreiben – `true` gibt einen NameError.
      • Anführungszeichen machen alles zu Text.
      • Anführungszeichen selbst tippen, nicht aus PDFs kopieren.
    """)
