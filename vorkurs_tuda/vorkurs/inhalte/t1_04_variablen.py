# -*- coding: utf-8 -*-
"""Kapitel: Variablen – Beschriftete Kisten (Vorlesung 1, Folien 23–29, Livecoding 1)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="variablen",
    titel="Variablen – Beschriftete Kisten",
    beschreibung="Werte speichern, überschreiben, Namensregeln, snake_case, +=",
    quelle="Vorlesung 1, Livecoding 1",
    teil="tag1",
    icon="📦")

k.lernziele([
    "Ich kann Variablen anlegen, auslesen und überschreiben",
    "Ich kann vorhersagen, welchen Wert eine Variable nach mehreren Zuweisungen hat",
    "Ich kann Kurzformen wie += und -= benutzen",
    "Ich kann gültige von ungültigen Variablennamen unterscheiden und schreibe snake_case",
    "Ich kann die Werte zweier Variablen mit einer Hilfsvariable tauschen",
])

# ── Erklärung 1: Was sind Variablen? ─────────────────────────────────────
k.erklaerung("Was sind Variablen?", r"""
    ## Variablen = beschriftete Kisten

    Der Computer speichert Daten im **Arbeitsspeicher**. Jeder Speicherplatz
    hat eine Adresse wie `0x7ffeefbff5c8` – unmöglich zu merken.

    !! Variablen sind Namen für Speicherplätze im Arbeitsspeicher.

    :::analogie 📦 Das Lager mit den Kisten
    Stell dir den Arbeitsspeicher als riesiges Lager vor. Die Regalnummern
    (Adressen) will sich niemand merken. Also klebst du ein **Etikett** auf
    eine Kiste, z. B. `alter`. Das Etikett ist der **Name** der Variable,
    der Inhalt der Kiste ist ihr **Wert**.

      • `alter = 19` – lege 19 in die Kiste mit dem Etikett „alter“.
      • `print(alter)` – schau in die Kiste und zeig den Inhalt.
      • `alter = 20` – nimm den alten Inhalt heraus, leg 20 hinein.
        In einer Kiste liegt immer nur EIN Wert.

    Im Handy ist es genauso: Du speicherst „Mama“ statt der Nummer.
    :::
    ---
    ## Eine Variable anlegen

    Eine Variable entsteht mit einem einfachen `=` (der **Zuweisung**):

        alter = 19
        name = "Lea"
        preis = 2.49

    Links steht der NAME, rechts der WERT. Python bestimmt den Typ
    automatisch anhand des Werts (`alter` → int, `name` → str, ...).

    Der Wert darf ein beliebiger **Ausdruck** sein, also auch eine Rechnung
    oder ein Funktionsaufruf: `laenge = len("Hallo")` speichert das
    Ergebnis des Aufrufs, also 5 (`len()` zählt die Zeichen, mehr dazu im
    nächsten Kapitel).

    :::code
    x = 5
    print(x)
    x = "Hallo"
    print(x)
    print(type(x))
    :::

    Der Typ hängt am **Wert**, nicht am Namen. Dieselbe Variable kann erst
    eine Zahl und später einen Text enthalten.

    :::achtung Erst zuweisen, dann benutzen
    Benutzt du einen Namen, dem noch nie ein Wert zugewiesen wurde, meldet
    Python einen **NameError**: `name 'y' is not defined`. Und die Richtung
    ist fest: `5 = x` ist ein SyntaxError – der Name steht immer links.
    :::
    """)

k.mc("Wofür sind Variablen laut Vorlesung gut?",
     ["Sie geben Speicherplätzen Namen, damit wir Daten speichern und wiederverwenden können",
      "Sie machen das Programm automatisch schneller",
      "Sie verbinden den Computer mit dem Internet",
      "Sie sind nur zur Dekoration da"],
     "Variablen sind Namen für Speicherplätze. Ohne sie wären Programme sehr "
     "unpraktisch und schwer lesbar.")

k.ausgabe('x = 5\nx = "Hallo"\nprint(type(x))',
          "Die Variable x bekommt einen neuen Wert – und damit auch einen neuen Typ. "
          "Der Typ gehört zum Wert, nicht zum Namen.",
          akzeptiert=["str"])

k.ausgabe("x = 5\nprint(y)",
          "y wurde nie ein Wert zugewiesen. Python kennt den Namen nicht → NameError.",
          tipp="Welche Variablen gibt es nach Zeile 1?")

k.wf("Die Zeile   5 = x   speichert die Zahl 5 in der Variable x.", False,
     "Bei einer Zuweisung steht der Name immer LINKS und der Wert rechts. "
     "5 = x ist ein SyntaxError. Richtig: x = 5")

# ── Erklärung 2: Rechte Seite zuerst ─────────────────────────────────────
k.erklaerung("Rechte Seite zuerst – und Kurzformen", r"""
    ## Rechte Seite zuerst!

    Bei einer Zuweisung wird IMMER zuerst die rechte Seite ausgerechnet.
    Dann wird das Ergebnis in die Kiste links gelegt. Das Beispiel aus der
    Vorlesung, Schritt für Schritt:

    :::visual variablen
    {"vars": [{"name": "x", "wert": "5", "typ": "int"}, {"name": "y", "wert": "36", "typ": "int"}],
     "schritte": [[{"name": "x", "wert": "5", "typ": "int"}],
                  [{"name": "x", "wert": "5", "typ": "int"}, {"name": "y", "wert": "18", "typ": "int"}],
                  [{"name": "x", "wert": "5", "typ": "int"}, {"name": "y", "wert": "36", "typ": "int"}]],
     "texte": ["x = 5", "y = x * 3 + 3   (rechts: 5 * 3 + 3 = 18)", "y = y * 2   (rechts: 18 * 2 = 36)"]}
    :::

    `y = y * 2` ist in Mathe Unsinn. Beim Programmieren heißt es: „Nimm
    den alten Inhalt von y, verdopple ihn, leg ihn zurück in y.“

    !! Eine Variable merkt sich einen WERT, keine Rechnung.

        preis = 3
        gesamt = preis * 4     # gesamt ist 12
        preis = 10             # gesamt bleibt trotzdem 12!
    ---
    ## Kurzformen

    Weil man so oft `x = x + etwas` schreibt, gibt es Kurzformen:

    | Kurzform | bedeutet |
    |---|---|
    | `punkte += 10` | `punkte = punkte + 10` |
    | `leben -= 1` | `leben = leben - 1` |
    | `geld *= 2` | `geld = geld * 2` |
    | `anteil /= 4` | `anteil = anteil / 4` |
    | `kartons //= 6` | `kartons = kartons // 6` |

    :::trace
    punkte = 0
    punkte += 10
    punkte += 10
    punkte -= 3
    print(punkte)
    :::
    """)

k.mc("Was passiert bei   x = 2 + 3   zuerst?",
     ["Die rechte Seite 2 + 3 wird ausgerechnet",
      "x wird gelöscht",
      "x wird mit 2 verglichen",
      "Python prüft, ob x gleich 5 ist"],
     "Erst wird die rechte Seite berechnet (5), dann wird das Ergebnis in x gespeichert.")

k.ausgabe("x = 5\ny = x * 3 + 3\ny = y * 2\nprint(y)",
          "x = 5. Dann y = 5 * 3 + 3 = 18. Dann y = 18 * 2 = 36. (Beispiel aus der Vorlesung)")

k.ausgabe("a = 10\na = a + 5\nprint(a)",
          "Rechte Seite zuerst: 10 + 5 = 15, das kommt zurück in a.")

k.ausgabe("punkte = 0\npunkte += 10\npunkte += 5\npunkte -= 3\nprint(punkte)",
          "0 + 10 = 10, + 5 = 15, - 3 = 12.")

k.ausgabe("konto = 100\nkonto *= 2\nkonto //= 3\nprint(konto)",
          "100 * 2 = 200. Dann 200 // 3 = 66 (66 · 3 = 198, Rest 2).")

k.ausgabe("preis = 3\nmenge = 4\ngesamt = preis * menge\npreis = 10\nprint(gesamt)",
          "gesamt wurde EINMAL ausgerechnet (3 * 4 = 12) und gespeichert. Dass "
          "preis später geändert wird, ändert gesamt nicht mehr. Eine Variable "
          "merkt sich den Wert, nicht die Rechnung!",
          tipp="Wird gesamt automatisch neu berechnet, wenn sich preis ändert?")

# ── Erklärung 3: Tauschen ────────────────────────────────────────────────
k.erklaerung("Zwei Variablen tauschen", r"""
    ## Der Tausch-Trick mit dem leeren Glas

    :::analogie 🥤 Zwei volle Gläser
    In Glas A ist Saft, in Glas B ist Wasser. Du willst die Inhalte tauschen.
    Kippst du einfach B in A, ist der Saft weg. Du brauchst ein drittes,
    leeres Glas: erst Saft ins Hilfsglas, dann Wasser nach A, dann den Saft
    aus dem Hilfsglas nach B.
    :::

    :::vergleich ✘ Ohne Hilfsvariable | ✔ Mit Hilfsvariable
    Der alte Wert von a geht verloren:
        a = 1
        b = 2
        a = b      # a ist 2, die 1 ist weg
        b = a      # b ist 2
    Ergebnis: 2 2
    |||
    Die Hilfsvariable rettet den Wert:
        a = 1
        b = 2
        hilf = a   # hilf ist 1
        a = b      # a ist 2
        b = hilf   # b ist 1
    Ergebnis: 2 1
    :::

    Probier es Schritt für Schritt aus und beobachte die Kisten:

    :::trace
    a = 1
    b = 2
    hilf = a
    a = b
    b = hilf
    print(a, b)
    :::

    :::info Für später: der Python-Kurztrick
    Python kennt zusätzlich die Schreibweise `a, b = b, a`, die beide Werte
    auf einmal tauscht. Warum das funktioniert, lernst du an Tag 3 bei den
    Tupeln. Der Weg über die Hilfsvariable klappt in jeder Sprache.
    :::
    """)

k.ausgabe("a = 1\nb = 2\na = b\nb = a\nprint(a, b)",
          "Klassischer Anfängerfehler beim 'Tauschen': Nach a = b ist a = 2. "
          "Der alte Wert 1 ist damit weg! Dann b = a → b = 2. Ergebnis: 2 2. "
          "(print mit zwei Werten gibt sie mit Leerzeichen getrennt aus.)",
          tipp="Was steht in a, nachdem 'a = b' ausgeführt wurde?")

k.ausgabe('a = "Saft"\nb = "Wasser"\nhilf = a\na = b\nb = hilf\nprint(a, b)',
          "Mit der Hilfsvariable klappt der Tausch: hilf rettet 'Saft', bevor a "
          "überschrieben wird. Am Ende: a = 'Wasser', b = 'Saft'.")

k.mc("Warum braucht man beim Tauschen mit einzelnen Zuweisungen wie a = b eine Hilfsvariable?",
     ["Weil beim Überschreiben einer Variable ihr alter Wert verloren geht",
      "Weil Python nur drei Variablen gleichzeitig erlaubt",
      "Weil a = b einen Fehler auslöst",
      "Weil Variablen sonst ihren Typ verlieren"],
     "In einer Kiste liegt immer nur ein Wert. a = b wirft den alten Inhalt von a "
     "weg. Die Hilfsvariable merkt ihn sich vorher.")

# ── Erklärung 4: Namensregeln ────────────────────────────────────────────
k.erklaerung("Namensregeln und snake_case", r"""
    ## Namensregeln (in Python)

      • **Case-sensitive**: Groß-/Kleinschreibung zählt. `punktestand` und
        `punkteStand` sind ZWEI VERSCHIEDENE Variablen!
      • Der Name beginnt mit einem **Buchstaben oder Unterstrich** `_`,
        NIE mit einer Ziffer (`alter2` ok, `2alter` verboten).
      • Danach nur Buchstaben, Ziffern und `_` – keine Punkte, Bindestriche,
        Sterne, `&`, `#`, Leerzeichen ...
      • Wörter, die Python selbst benutzt (`if`, `while`, `for`, `True`, ...),
        sind als Namen verboten.
      • Namen sollen **aussagekräftig** sein: `anzahl_teilnehmer = 25` statt `a = 25`.

    :::achtung Bindestrich = Minus
    `anzahl-kekse = 5` liest Python als „anzahl MINUS kekse = 5“ und meldet
    einen SyntaxError. Nimm den Unterstrich: `anzahl_kekse`.
    :::

    :::info Und Umlaute?
    Die Folie sagt „keine Sonderzeichen“. Umlaute wie ä, ö, ü zählen für
    Python 3 aber als Buchstaben – `größe = 1.8` ist gültig. Trotzdem vermeidet
    man sie in der Praxis (andere Tastaturen, andere Sprachen): `groesse`.
    :::
    ---
    ## snake_case – die Python-Schreibweise

    In Python schreibt man Variablennamen in **snake_case**: alles klein,
    Wörter mit Unterstrich getrennt (sieht aus wie eine Schlange `_ _ _`).

    | Name | Schreibweise | in Python üblich? |
    |---|---|---|
    | `matrikel_nummer` | snake_case | ✔ |
    | `anzahl_kekse` | snake_case | ✔ |
    | `anzahlKekse` | camelCase (z. B. in Java) | ✘ |
    | `AnzahlKekse` | PascalCase | ✘ |

    !! Ein Name kann GÜLTIG sein (Python akzeptiert ihn) und trotzdem
    !! NICHT der Konvention snake_case entsprechen, z. B. punkteStand.
    """)

k.wf("Python unterscheidet bei Variablennamen zwischen Groß- und Kleinschreibung.", True,
     "Ja, Python ist case-sensitive: alter, Alter und ALTER sind drei verschiedene Variablen.")

k.ausgabe("punkteStand = 10\nprint(punktestand)",
          "punktestand (kleines s) ist ein anderer Name als punkteStand. Diesen "
          "Namen gibt es nicht → NameError. Python schlägt sogar vor: "
          "Did you mean: 'punkteStand'?",
          tipp="Vergleiche die Schreibweise Buchstabe für Buchstabe.")

k.mc("Welcher dieser Variablennamen ist UNGÜLTIG?",
     ["anzahl-kekse", "anzahl_kekse", "_anzahl", "kekse2"],
     "Der Bindestrich ist für Python ein Minus. anzahl-kekse wäre 'anzahl minus "
     "kekse'. Die anderen drei sind gültig.")

k.mc("Welcher Name ist am besten für 'Anzahl der Teilnehmer'?",
     ["anzahl_teilnehmer", "AnzahlTeilnehmer", "a", "anzahl-teilnehmer"],
     "anzahl_teilnehmer ist aussagekräftig und in snake_case. 'anzahl-teilnehmer' "
     "wäre sogar ungültig (Bindestrich = Minus!).")

k.text("Wie heißt die Schreibweise für Variablennamen, die man in Python verwendet?",
       ["snake_case", "snakecase", "snake case", "snake-case"],
       "snake_case: alles klein, Wörter mit Unterstrich getrennt.",
       tipp="Ein Tier, das lang und dünn ist ...")

k.wf("mein alter   (mit Leerzeichen) ist ein gültiger Variablenname.", False,
     "Leerzeichen sind in Namen nicht erlaubt. Python würde zwei Namen 'mein' und "
     "'alter' sehen → SyntaxError. Richtig: mein_alter")

# ── Praxisteil ───────────────────────────────────────────────────────────
k.puzzle("Tausche die Getränke: Am Ende soll   Tee Kaffee   ausgegeben werden. "
         "Benutze die Hilfsvariable hilf.",
         """
         a = "Kaffee"
         b = "Tee"
         hilf = a
         a = b
         b = hilf
         print(a, b)
         """,
         "Erst den Wert von a in hilf retten, dann a mit b überschreiben, dann den "
         "geretteten Wert nach b legen.",
         tipp="Was muss gesichert werden, bevor a überschrieben wird?",
         ablenker=["b = a"])

k.code(r"""
    ## Punktestand im Spiel

    Schreibe ein Programm mit der Variable `punkte`:

      1. Am Anfang hat man 0 Punkte.
      2. Zwei Treffer: je 10 Punkte dazu.
      3. Eine Strafe: 3 Punkte weg.
      4. Bonusrunde: Die Punkte werden verdoppelt.
      5. Gib den Punktestand aus.

    Benutze für die Schritte 2 bis 4 die Kurzformen `+=`, `-=` und `*=`.
    Die erwartete Ausgabe ist `34`.
    """,
    [P(erwartet=["34"], beschreibung="Ausgabe 34"),
     F("punkte", 34)],
    """
    punkte = 0
    punkte += 10
    punkte += 10
    punkte -= 3
    punkte *= 2
    print(punkte)
    """,
    "0 → 10 → 20 → 17 → 34. Jede Kurzform nimmt den alten Wert, rechnet und legt "
    "das Ergebnis zurück in punkte.",
    verboten=["34"],
    pflicht=["+=", "-=", "*="],
    tipps=["Leg die Variable mit punkte = 0 an.",
           "punkte += 10 bedeutet: punkte = punkte + 10.",
           "punkte = 0, zweimal punkte += 10, dann punkte -= 3, punkte *= 2, print(punkte)"],
    vorlage="punkte = 0\n")

k.code(r"""
    ## Kassenbon im Café

    Die Preise und Mengen stehen schon in der Vorlage. Berechne damit:

      • `summe`: Gesamtpreis aller Kaffees und Brezeln
      • `rabatt`: 10 % der Summe (also `summe * 0.1`)
      • `zu_zahlen`: Summe minus Rabatt

    Gib am Ende `zu_zahlen` aus. Python soll alles aus den Variablen
    ausrechnen – keine Ergebnisse selbst eintippen.
    """,
    [F("summe", 9.1),
     F("rabatt", 0.91),
     F("zu_zahlen", 8.19),
     P(erwartet=["8.19"], beschreibung="Ausgabe von zu_zahlen")],
    """
    preis_kaffee = 2.5
    preis_brezel = 0.8
    anzahl_kaffee = 3
    anzahl_brezel = 2
    summe = preis_kaffee * anzahl_kaffee + preis_brezel * anzahl_brezel
    rabatt = summe * 0.1
    zu_zahlen = summe - rabatt
    print(zu_zahlen)
    """,
    "Erst die Summe (2.5 · 3 + 0.8 · 2 = 9.1), dann der Rabatt (0.91), dann die "
    "Differenz (8.19). Weil jede Zeile mit den Variablen rechnet, stimmt der Bon "
    "auch, wenn sich ein Preis ändert – man muss das Programm nur neu ausführen.",
    verboten=["9.1", "0.91", "8.19"],
    tipps=["Die Summe ist Preis mal Anzahl für den Kaffee plus Preis mal Anzahl für die Brezeln.",
           "rabatt = summe * 0.1 und zu_zahlen = summe - rabatt",
           "summe = preis_kaffee * anzahl_kaffee + preis_brezel * anzahl_brezel"],
    vorlage="preis_kaffee = 2.5\npreis_brezel = 0.8\nanzahl_kaffee = 3\nanzahl_brezel = 2\n")

k.code(r"""
    ## Minuten umrechnen

    Ein Film dauert `minuten_gesamt = 135` Minuten. Berechne daraus

      • `stunden`: die vollen Stunden
      • `minuten`: die restlichen Minuten

    und gib beides in dieser Form aus:

        2 h 15 min

    Tipp: `print(stunden, "h", minuten, "min")` setzt automatisch Leerzeichen
    zwischen die Werte. Die Ergebnisse 2 und 15 darfst du nicht eintippen.
    """,
    [F("stunden", 2),
     F("minuten", 15),
     P(erwartet=["2 h 15 min"], beschreibung="Ausgabe")],
    """
    minuten_gesamt = 135
    stunden = minuten_gesamt // 60
    minuten = minuten_gesamt % 60
    print(stunden, "h", minuten, "min")
    """,
    "// 60 zählt die vollen Stunden (135 // 60 = 2), % 60 liefert die übrigen "
    "Minuten (135 % 60 = 15).",
    verboten=["2", "15"],
    tipps=["Eine Stunde hat 60 Minuten. Welche zwei Operatoren kennst du für „voll“ und „Rest“?",
           "stunden = minuten_gesamt // 60",
           "minuten = minuten_gesamt % 60, danach print(stunden, \"h\", minuten, \"min\")"],
    vorlage="minuten_gesamt = 135\n",
    streng=True)

k.zusammenfassung(r"""
    ## Das Wichtigste aus Kapitel 4

    !! Variablen sind Namen für Speicherplätze – beschriftete Kisten.

        alter = 19          # anlegen (Zuweisung)
        alter = alter + 1   # rechte Seite zuerst → 20
        alter += 1          # Kurzform → 21

      • Rechts vom `=` wird zuerst gerechnet, dann gespeichert.
      • Eine Variable merkt sich einen WERT, keine Rechnung.
      • Der Typ gehört zum Wert und kann sich ändern.
      • Unbekannter Name → NameError.
      • Tauschen mit Hilfsvariable: `hilf = a`, `a = b`, `b = hilf`.

    | Regel | gültig | ungültig |
    |---|---|---|
    | Beginn mit Buchstabe oder `_` | `alter2`, `_x` | `2alter` |
    | nur Buchstaben, Ziffern, `_` | `anzahl_kekse` | `anzahl-kekse`, `mein alter` |
    | Groß/klein zählt | `punkteStand` ≠ `punktestand` | |

    Konvention: **snake_case** (`matrikel_nummer`), nicht camelCase.
    """)
