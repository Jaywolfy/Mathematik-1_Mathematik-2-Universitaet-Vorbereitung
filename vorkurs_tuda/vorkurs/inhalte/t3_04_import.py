# -*- coding: utf-8 -*-
"""Kapitel: Pakete importieren – Der Werkzeugkasten (Vorlesung 3, Folien 24–26; Übung 3)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="module_import",
    titel="Pakete importieren – Der Werkzeugkasten",
    beschreibung="import math, math.sin, math.pi, math.floor, ...",
    quelle="Vorlesung 3, Übung 3",
    teil="tag3",
    icon="🧰")

k.lernziele([
    "Ich kann ein Paket mit import einbinden und seine Funktionen mit paket.funktion(...) aufrufen",
    "Ich kann math.pi, math.sqrt, math.floor und die Winkelfunktionen benutzen",
    "Ich kann Grad ins Bogenmaß umrechnen, bevor ich math.sin oder math.cos aufrufe",
    "Ich kann den Unterschied zwischen math.floor() und int() bei negativen Zahlen erklären",
])

# ── Erklärung 1: import ──────────────────────────────────────────────────
k.erklaerung("Pakete importieren", r"""
    ## Das Rad nicht neu erfinden

    Häufig möchte man Funktionalitäten nicht mehrfach erfinden müssen.
    Deshalb bindet man **Funktionsbibliotheken** ein. In Python (und Java)
    **importiert** man sie aus anderen **Paketen**. Die Syntax dafür:

        import <paket-name>

    :::analogie 🧰 Der Werkzeugkasten
    Du baust ein Regal auf. Du schmiedest dir keinen eigenen Schraubenzieher,
    du holst den Werkzeugkasten aus dem Keller.
      • `import math` heißt: „Hol den Werkzeugkasten math.“ Das macht man
        **einmal**, am besten ganz oben im Programm.
      • `math.sqrt(16)` heißt: „Aus dem Kasten math nimm die Wurzel-Zange.“
        Der Punkt bedeutet „aus dem Kasten“.
      • Ohne den Kasten zu holen, kennt Python das Werkzeug nicht: `NameError`.
      • Im Kasten liegen nicht nur Werkzeuge, sondern auch fertige Werte, zum
        Beispiel `math.pi`.
    :::

    :::visual ablauf
    {"titel": "Vom Import zum Ergebnis",
     "schritte": [{"icon": "🧰", "text": "import math – den Werkzeugkasten holen"},
                  {"icon": "🔧", "text": "math.sqrt(16) – ein Werkzeug aus dem Kasten benutzen"},
                  {"icon": "✅", "text": "Ergebnis: 4.0"}]}
    :::
    ---
    ## Beispiel: das math-Paket

    Für mathematische Funktionen gibt es im Python-Standard das Paket `math`
    (Folie 26):

        >>> import math
        >>> math.sin(math.pi * 0.5)
        1.0

    Nach `import math` schreibt man `math.<name>`, also z. B. `math.pi` oder
    `math.sqrt(2)`.

    | Name | Bedeutung | Beispiel |
    |---|---|---|
    | `math.pi` | die Kreiszahl π | `3.141592653589793` |
    | `math.sqrt(x)` | Wurzel | `math.sqrt(16)` → `4.0` |
    | `math.floor(x)` | abrunden | `math.floor(3.7)` → `3` |
    | `math.sin(x)`, `math.cos(x)`, `math.tan(x)` | Winkelfunktionen | `math.cos(0)` → `1.0` |
    | `math.asin(x)`, `math.acos(x)`, `math.atan(x)` | Arcus-Funktionen (Winkel aus Verhältnis) | `math.atan(1)` → `0.785…` |

    :::code
    import math
    print(math.pi)
    print(math.sqrt(16))
    print(math.floor(3.7))
    print(math.sin(math.pi * 0.5))
    :::

    :::achtung Typische Fehler beim Import
      • `import math` vergessen → `NameError: name 'math' is not defined`.
      • `sqrt(16)` statt `math.sqrt(16)` → `NameError`, denn das Werkzeug
        liegt im Kasten.
      • Die eigene Datei `math.py` nennen: Dann findet Python deine Datei
        statt des echten Pakets.
    :::

    :::info Bonus-Wissen: from … import
    Es gibt auch `from math import sqrt`. Danach darf man direkt `sqrt(16)`
    schreiben. Das kommt in der Vorlesung nicht vor. Im Vorkurs reicht
    `import math`.
    :::
    """)

k.ausgabe("import math\nprint(math.sin(math.pi * 0.5))",
          "pi · 0.5 sind 90° im Bogenmaß, und sin(90°) = 1 → 1.0 (Beispiel aus Vorlesung 3).")
k.ausgabe("import math\nprint(math.sqrt(16))",
          "Die Wurzel aus 16 ist 4. math.sqrt liefert einen float: 4.0.")
k.ausgabe("print(math.pi)",
          "Das Paket math wurde nicht importiert → NameError: name 'math' is not defined.")
k.mc("Wie bindest du das Paket math ein?",
     ["import math", "include math", "using math", "#import math"],
     "In Python: import <paket-name>.")
k.mc("Warum importiert man Pakete?",
     ["Um fertige Funktionen zu benutzen, statt sie selbst neu zu programmieren",
      "Damit das Programm eine Internetverbindung bekommt",
      "Weil Python ohne import nicht starten kann",
      "Um Variablen zu löschen"],
     "Man möchte Funktionalitäten nicht mehrfach erfinden müssen → Bibliotheken einbinden.")
k.mc("Du hast   import math   geschrieben. Wie ziehst du die Wurzel aus 2?",
     ["math.sqrt(2)", "sqrt(2)", "math(sqrt, 2)", "import sqrt(2)"],
     "Nach `import math` holt man jedes Werkzeug mit dem Punkt aus dem Kasten: `math.sqrt(2)`. "
     "Nur `sqrt(2)` gibt einen NameError.")

# ── Erklärung 2: Winkel und Runden ───────────────────────────────────────
k.erklaerung("Winkel und Abrunden", r"""
    ## Bogenmaß statt Grad

    !! Die Winkelfunktionen von math rechnen im BOGENMASS (englisch radians), nicht in Grad!

    Ein ganzer Kreis hat 360° oder 2π im Bogenmaß. Umrechnen:

        bogen = grad * math.pi / 180

    | Grad | Bogenmaß | `math.sin(...)` |
    |---|---|---|
    | 0° | `0` | `0.0` |
    | 30° | `math.pi / 6` | `0.5` (ungefähr) |
    | 90° | `math.pi * 0.5` | `1.0` |
    | 180° | `math.pi` | fast `0` |
    | 360° | `2 * math.pi` | fast `0` |

    :::visual ablauf
    {"titel": "Sinus von 90 Grad berechnen",
     "schritte": [{"icon": "📐", "text": "grad = 90"},
                  {"icon": "🔁", "text": "bogen = grad * math.pi / 180 → 1.5707…"},
                  {"icon": "📈", "text": "math.sin(bogen) → 1.0"}]}
    :::

    Die **Arcus-Funktionen** gehen den umgekehrten Weg: Aus einem Verhältnis
    wird ein Winkel (im Bogenmaß). `math.atan(1)` ist 45° = π/4. Das brauchst
    du in Übung 3 bei der Bildschirmdiagonale.

    :::code
    import math
    grad = 30
    bogen = grad * math.pi / 180
    print(math.sin(bogen))
    print(math.sin(30))
    print(math.atan(1) * 180 / math.pi)
    :::
    Die zweite Ausgabezeile zeigt den typischen Fehler: `math.sin(30)` rechnet mit
    30 im **Bogenmaß** und liefert etwas völlig anderes als 0.5.

    Kleine Rechenungenauigkeiten wie `0.49999999999999994` sind normal bei
    Kommazahlen. Mit `round(wert, 2)` oder `f"{wert:.2f}"` wird es hübsch.
    ---
    ## floor() vs. int()

    Beide machen aus einer Kommazahl eine Ganzzahl, aber unterschiedlich:
      • `math.floor()` rundet immer AB (Richtung minus unendlich).
      • `int()` SCHNEIDET die Nachkommastellen ab (Richtung 0).

    Bei positiven Zahlen ist das gleich, bei negativen nicht:

        math.floor(-3.5)    # → -4
        int(-3.5)           # → -3
    """)

k.wf("math.sin() erwartet den Winkel in Grad.", False,
     "Die Winkelfunktionen von math arbeiten im Bogenmaß. 90° = math.pi / 2.")
k.ausgabe("import math\nprint(math.floor(3.7))", "floor rundet ab: 3.")
k.ausgabe("import math\nprint(math.floor(-3.5))\nprint(int(-3.5))",
          "floor rundet nach UNTEN (Richtung minus unendlich): -4. int schneidet ab: -3.",
          tipp="Was ist bei negativen Zahlen 'abrunden'?")
k.ausgabe("import math\nprint(round(math.atan(1) * 180 / math.pi))",
          "atan(1) ist der Winkel, dessen Tangens 1 ist: π/4 im Bogenmaß. Umgerechnet in "
          "Grad (· 180 / π) sind das 45.",
          tipp="Bei welchem Winkel sind beide Seiten eines rechtwinkligen Dreiecks gleich lang?")
k.mc("Wie berechnest du den Sinus von 60 Grad richtig?",
     ["math.sin(60 * math.pi / 180)", "math.sin(60)", "math.sin(60 / 180)", "math.sin(60 * 180 / math.pi)"],
     "Erst Grad ins Bogenmaß umrechnen: · π / 180. `math.sin(60)` würde 60 als Bogenmaß deuten.")

# ── Praxis ───────────────────────────────────────────────────────────────
k.luecke("Ergänze den Code: Die Kreisfläche für r = 2 soll ausgegeben werden.",
         """
         ___ math
         r = 2
         print(math.___ * r ** 2)
         """,
         [["import"], ["pi"]],
         "Erst das Paket einbinden, dann die Kreiszahl mit `math.pi` holen. Fläche = π · r².",
         tipp="Wie holt man den Werkzeugkasten? Und wie heißt die Kreiszahl?")

k.puzzle("Bringe die Zeilen in die richtige Reihenfolge: Der Sinus von 30 Grad soll auf zwei "
         "Stellen gerundet ausgegeben werden.",
         """
         import math
         grad = 30
         bogen = grad * math.pi / 180
         print(round(math.sin(bogen), 2))
         """,
         "Zuerst importieren, dann den Winkel festlegen, ins Bogenmaß umrechnen und erst dann "
         "den Sinus berechnen.",
         tipp="Ohne import kennt Python math nicht. Und sin braucht das Bogenmaß.",
         ablenker=["print(round(math.sin(grad), 2))"])

k.code(r"""
    ## Pizza-Rechner: Kreisfläche

    Lies den Radius einer Pizza in cm ein (Kommazahl, `float(input())`).
    Berechne die Fläche A = π · r² mit `math.pi` und gib sie mit zwei
    Nachkommastellen aus:

        Eingabe: 10      Ausgabe: Fläche: 314.16
        Eingabe: 0       Ausgabe: Fläche: 0.00
    """,
    [P(["10"], ["Fläche: 314.16"]),
     P(["0"], ["Fläche: 0.00"]),
     P(["1"], ["Fläche: 3.14"]),
     P(["2.5"], ["Fläche: 19.63"])],
    """
    import math
    r = float(input("Radius: "))
    flaeche = math.pi * r ** 2
    print(f"Fläche: {flaeche:.2f}")
    """,
    "math.pi ist viel genauer als 3.14. Bei r = 10 macht das schon einen Unterschied: "
    "314.16 statt 314.00. `{flaeche:.2f}` zeigt genau zwei Nachkommastellen.",
    pflicht=["math.pi"],
    tipps=["Welche Zahl aus math brauchst du für Kreise?",
           "import math, dann r mit float(input()) einlesen, flaeche = math.pi * r ** 2.",
           'print(f"Fläche: {flaeche:.2f}")'],
    streng=True)

k.code(r"""
    ## Wie lang ist die Leiter?

    Eine Leiter lehnt an der Wand. Ihr Fuß steht `a` Meter von der Wand
    entfernt und sie reicht `b` Meter hoch. Nach Pythagoras ist ihre Länge
    c = √(a² + b²).

    Lies a und b ein (Kommazahlen) und gib die Länge mit `math.sqrt` und zwei
    Nachkommastellen aus:

        Eingaben: 3, 4     Ausgabe: Länge: 5.00
        Eingaben: 1, 1     Ausgabe: Länge: 1.41
    """,
    [P(["3", "4"], ["Länge: 5.00"]),
     P(["5", "12"], ["Länge: 13.00"]),
     P(["1", "1"], ["Länge: 1.41"]),
     P(["0", "0"], ["Länge: 0.00"]),
     P(["0.5", "2"], ["Länge: 2.06"])],
    """
    import math
    a = float(input("Abstand zur Wand: "))
    b = float(input("Höhe: "))
    c = math.sqrt(a ** 2 + b ** 2)
    print(f"Länge: {c:.2f}")
    """,
    "Erst die Quadrate addieren, dann die Wurzel ziehen. Ein häufiger Fehler ist "
    "`math.sqrt(a) + math.sqrt(b)`, das ist etwas ganz anderes.",
    pflicht=["import math"],
    tipps=["Welche Funktion aus math zieht die Wurzel?",
           "c = math.sqrt(a ** 2 + b ** 2)",
           'print(f"Länge: {c:.2f}")'],
    streng=True)

k.code(r"""
    ## Sinus in Grad

    Lies einen Winkel in **Grad** ein (ganze Zahl). Gib den Sinus dieses
    Winkels mit vier Nachkommastellen aus. Denk daran: `math.sin` erwartet das
    Bogenmaß!

        Eingabe: 90     Ausgabe: 1.0000
        Eingabe: 30     Ausgabe: 0.5000
        Eingabe: -90    Ausgabe: -1.0000
    """,
    [P(["90"], ["1.0000"], nicht=["0.8940"]),
     P(["30"], ["0.5000"]),
     P(["0"], ["0.0000"]),
     P(["-90"], ["-1.0000"]),
     P(["180"], ["0.0000"])],
    """
    import math
    grad = int(input("Winkel in Grad: "))
    bogen = grad * math.pi / 180
    print(f"{math.sin(bogen):.4f}")
    """,
    "Grad · π / 180 ergibt das Bogenmaß. Wer `math.sin(90)` rechnet, bekommt 0.8940, weil "
    "90 als Bogenmaß gedeutet wird. sin(180°) ist wegen Rundung nicht genau 0, mit vier "
    "Nachkommastellen steht aber 0.0000 da.",
    tipps=["Was erwartet math.sin: Grad oder Bogenmaß?",
           "bogen = grad * math.pi / 180",
           'print(f"{math.sin(bogen):.4f}")'])

k.zusammenfassung(r"""
    ## Import auf einen Blick

        import math                   # Paket einbinden (einmal, oben)
        math.pi                       # 3.141592653589793
        math.sqrt(16)                 # 4.0
        math.floor(-3.5)              # -4   (int(-3.5) wäre -3)
        math.sin(90 * math.pi / 180)  # 1.0  (Bogenmaß!)
        math.atan(1)                  # 0.785… = 45° im Bogenmaß

    | Fehler | Ursache |
    |---|---|
    | `NameError: name 'math' is not defined` | `import math` fehlt |
    | `NameError: name 'sqrt' is not defined` | `math.` vergessen |
    | falscher Sinus-Wert | Grad statt Bogenmaß übergeben |

    !! Erst importieren, dann mit paket.name benutzen. Winkel immer ins Bogenmaß umrechnen.
    """)
