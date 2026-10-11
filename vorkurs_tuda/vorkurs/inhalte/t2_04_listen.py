# -*- coding: utf-8 -*-
"""Kapitel: Listen – Die Einkaufsliste (Vorlesung 2, Folien 38–46; Livecoding 2.5)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="listen",
    titel="Listen – Die Einkaufsliste",
    beschreibung="Viele Werte in einer Variable: Index, append, pop, sort, in, ...",
    quelle="Vorlesung 2, Livecoding 2",
    teil="tag2",
    icon="📝")

k.lernziele([
    "Ich kann Listen anlegen und Elemente über ihren Index (auch negativ) lesen und überschreiben",
    "Ich kann Listen mit append, pop, del, sort, reverse und clear verändern und mit in und index durchsuchen",
    "Ich kann mit einer while-Schleife alle Elemente einer Liste durchgehen und dabei verändern",
    "Ich kenne den Unterschied zwischen lst2 = lst1 und lst2 = lst1.copy()",
])

# ── Erklärung 1: Anlegen und Index ──────────────────────────────────────────
k.erklaerung("Listen anlegen und lesen", r"""
    ## Das Problem

    Bisher hättest du eine Reihe von Werten vielleicht so gespeichert:

        a1 = 3
        a2 = 4
        a3 = 1
        a4 = 2

    Wie geht das kürzer? Und wie kann eine Schleife alle Werte
    durchgehen? Mit **Listen**!

    Eine **Liste** speichert mehrere Werte in fester Reihenfolge in EINER
    Variable. Man schreibt sie mit **eckigen Klammern**, die Werte
    (**Elemente**) durch Kommas getrennt:

        lst1 = list()          # leere Liste
        lst1 = []              # auch eine leere Liste
        lst1 = [3, 4, 1, 2]    # Liste mit Werten
        einkauf = ["Milch", "Brot", "Eier"]

    `len(lst)` liefert die Anzahl der Elemente, die **Länge** der Liste.
    ---
    ## Schließfächer mit Nummern

    :::analogie 🔐 Die Schließfächer im Schwimmbad
    Eine Liste ist eine Reihe von Schließfächern. Jedes Fach hat eine
    Nummer, den **Index**, und das erste Fach hat die Nummer **0**.
      • `lst[2]` heißt: „Öffne Fach Nummer 2 und schau hinein.“
      • `lst[2] = 9` heißt: „Leg in Fach 2 etwas Neues.“ Der alte Inhalt
        fliegt raus.
      • Negative Nummern zählen von hinten: Fach -1 ist das letzte, wie
        „der Letzte in der Schlange“.
      • Ein Fach mit der Nummer `len(lst)` gibt es nicht: Bei 4 Fächern
        ist das letzte Fach Nummer 3.
    :::

    :::visual liste
    {"name": "lst", "werte": [3, 4, 1, 2], "markiert": [0], "negativ": true}
    :::

    Eine Liste speichert Werte an den **Indizes** 0 bis `len(lst) - 1`.
    ---
    ## Lesen und überschreiben

    :::code
    lst = [3, 4, 1, 2]
    print(lst[0])     # erstes Element: 3
    print(lst[2])     # drittes Element: 1
    print(lst[-1])    # letztes Element: 2
    print(lst[-3])    # 4
    lst[0] = 7
    lst[-1] = 5
    print(lst)        # [7, 4, 1, 5]
    :::

    Allgemein: `lst[-k]` ist dasselbe wie `lst[len(lst) - k]`.

    :::achtung lst[len(lst)] gibt IMMER einen Fehler
    Bei 4 Elementen ist der höchste Index 3. `lst[4]` gibt es nicht:
    `IndexError: list index out of range`. Das letzte Element bekommst du
    mit `lst[-1]` oder `lst[len(lst) - 1]`.
    :::
    """)

k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst[0])", "Index 0 ist das erste Element: 3.")
k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst[2])", "Index 2 ist das DRITTE Element: 1.")
k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst[-1])", "-1 ist immer das letzte Element: 2.")
k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst[-3])",
          "Von hinten gezählt: -1 → 2, -2 → 1, -3 → 4. (Oder: len(lst) - 3 = 1 → lst[1] = 4)")
k.ausgabe("lst = [3, 4, 1, 2]\nlst[0] = 7\nlst[1] = 1\nlst[-1] = 5\nprint(lst)",
          "[3,4,1,2] → [7,4,1,2] → [7,1,1,2] → [7,1,1,5].")
k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst[len(lst)])",
          "len(lst) ist 4, der höchste Index ist aber 3. lst[4] gibt es nicht → IndexError. "
          "Das passiert bei JEDER Liste.")
k.ausgabe("a = 0\ns = []\na /= len(s)\nprint(a)",
          "Die leere Liste hat die Länge 0. `a /= len(s)` bedeutet `a = a / 0`, und durch 0 "
          "kann man nicht teilen → ZeroDivisionError. (Quizfrage aus Vorlesung 2)",
          frage="Was passiert bei diesem Code? (Bei einem Fehler: den Namen des Fehlers)",
          tipp="Wie lang ist die leere Liste?")
k.mc("Welchen Index hat das ERSTE Element einer Liste?",
     ["0", "1", "-1", "Das kommt auf die Liste an"],
     "In Python (und den meisten Sprachen) beginnt die Zählung bei 0.")
k.mc("Wie kommst du immer an das LETZTE Element einer Liste lst?",
     ["lst[-1]", "lst[len(lst)]", "lst[last]", "lst[0]"],
     "lst[-1] (oder lst[len(lst) - 1]). lst[len(lst)] gibt immer einen IndexError.")
k.ausgabe("gemischt = [1, 'zwei', 3.0, True]\nprint(len(gemischt))",
          "Eine Liste darf Werte unterschiedlicher Typen enthalten. Sie hat 4 Elemente.")

# ── Erklärung 2: Listen verändern ───────────────────────────────────────────
k.erklaerung("Listen verändern und durchsuchen", r"""
    ## Enthalten? Wo?  (lst = [3, 4, 1, 2])

        4 in lst          # True
        5 in lst          # False
        5 not in lst      # True  (das Gegenteil von in)
        lst.index(1)      # 2  (die POSITION des Werts 1)
        lst.index(0)      # ValueError: 0 gibt es nicht

    :::achtung index(1) ist nicht lst[1]
    `lst.index(1)` sucht den WERT 1 und liefert seine Position (2).
    `lst[1]` holt den Wert an POSITION 1 (4). Die Fehlermeldung bei einem
    fehlenden Wert lautet je nach Python-Version etwas anders, der
    Fehlertyp ist immer `ValueError`.
    :::
    ---
    ## Hinzufügen, entfernen, umsortieren

    In Python haben Listen keine feste Länge. Jede Zeile der Tabelle
    startet mit `lst = [3, 4, 1, 2]`:

    | Befehl | Wirkung | Ergebnis |
    |---|---|---|
    | `lst.append(5)` | hinten anhängen | `[3, 4, 1, 2, 5]` |
    | `lst.pop()` | letztes entfernen (und zurückgeben) | `[3, 4, 1]` |
    | `del lst[1]` | Element an Index 1 löschen | `[3, 1, 2]` |
    | `lst.clear()` | alles löschen | `[]` |
    | `lst.reverse()` | Reihenfolge umdrehen | `[2, 1, 4, 3]` |
    | `lst.sort()` | aufsteigend sortieren | `[1, 2, 3, 4]` |

    Listen **zusammenfügen** (konkatenieren) geht mit `+`:
    `[3, 1, 2] + [5, 6, 1]` ergibt `[3, 1, 2, 5, 6, 1]`.

    :::info Folie 45: jede Zeile startet neu
    Auf der Folie stehen diese Befehle untereinander. Die Ergebnisse dort
    beziehen sich aber jeweils auf die AUSGANGSLISTE `[3, 4, 1, 2]`, nicht
    auf das Ergebnis der Zeile davor. Führst du sie wirklich nacheinander
    aus, kommt etwas anderes heraus (siehe nächste Seite).
    :::
    ---
    ## Nacheinander ausgeführt

    :::trace
    lst = [3, 4, 1, 2]
    lst.append(5)
    lst.pop()
    del lst[1]
    print(lst)
    lst.clear()
    lst.reverse()
    print(lst)
    :::

    Nach `append(5)` und `pop()` ist die Liste wieder `[3, 4, 1, 2]`.
    `del lst[1]` macht daraus `[3, 1, 2]`. Nach `clear()` ist sie leer, und
    eine leere Liste umzudrehen ergibt wieder `[]`.
    """)

k.ausgabe("lst = [3, 4, 1, 2]\nprint(4 in lst)\nprint(5 in lst)",
          "4 ist in der Liste (True), 5 nicht (False).")
k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst.index(1))",
          "Der Wert 1 steht an Index 2.",
          tipp="Gefragt ist die POSITION des Werts 1, nicht der Wert an Position 1.")
k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst.index(0))",
          "Den Wert 0 gibt es nicht in der Liste → ValueError.")
k.ausgabe("lst = [3, 4, 1, 2]\nlst.append(5)\nprint(lst)", "append hängt hinten an.")
k.ausgabe("lst = [3, 4, 1, 2]\ndel lst[1]\nprint(lst)", "del lst[1] löscht das Element an Index 1 (die 4).")
k.ausgabe("lst = [3, 4, 1, 2]\nlst.sort()\nprint(lst)", "sort() sortiert aufsteigend.")
k.ausgabe("lst = [3, 4, 1, 2]\nlst.append(5)\nlst.pop()\ndel lst[1]\nprint(lst)",
          "NACHEINANDER: [3,4,1,2] → append(5) → [3,4,1,2,5] → pop() → [3,4,1,2] → "
          "del lst[1] → [3,1,2]. Auf Folie 45 stehen die Ergebnisse dagegen jeweils für die "
          "Ausgangsliste.",
          tipp="Jede Zeile arbeitet mit dem Ergebnis der Zeile davor.")
k.ausgabe('einkauf = ["Milch", "Brot", "Eier"]\nletzter = einkauf.pop()\nprint(letzter)\nprint(einkauf)',
          "pop() entfernt das letzte Element UND gibt es zurück. Deshalb steht in letzter "
          "der Wert 'Eier'.")
k.ausgabe("lst1 = [3, 1, 2]\nlst2 = [5, 6, 1]\nprint(lst1 + lst2)",
          "+ hängt die zweite Liste an die erste an (Konkatenation).")
k.mc("Mit welcher Methode hängst du ein Element hinten an eine Liste an?",
     ["append()", "add()", "push()", "insert_last()"],
     "lst.append(5) hängt die 5 hinten an.")
k.wf("Listen haben in Python eine feste Länge, die man nicht ändern kann.", False,
     "Python-Listen können wachsen (append) und schrumpfen (pop, del, clear).")

# ── Erklärung 3: Schleifen über Listen ──────────────────────────────────────
k.erklaerung("Listen und while-Schleifen", r"""
    ## Alle Elemente durchgehen

    Mit einer Zählvariable i, die von 0 bis `len(lst) - 1` läuft, erreichst
    du jedes Fach genau einmal:

    :::code
    einkauf = ["Milch", "Brot", "Eier"]
    i = 0
    while i < len(einkauf):
        print(i, einkauf[i])
        i += 1
    :::

    Die Bedingung `i < len(einkauf)` sorgt dafür, dass i nie den
    ungültigen Index `len(einkauf)` erreicht. Bei einer leeren Liste läuft
    die Schleife kein einziges Mal.
    ---
    ## Elemente in der Schleife überschreiben

    Aus dem Livecoding: Die Schleife gibt jedes Element aus und
    überschreibt es danach mit 0.

    :::trace
    a = [1, 2, 3, 4, 5]
    i = 0
    while i < len(a):
        print(a[i])
        a[i] = 0
        i = i + 1
    print(a)
    :::

    `a[i] = 0` legt in Fach i einen neuen Wert. So kannst du eine Liste
    Element für Element verändern, zum Beispiel alle Preise erhöhen oder
    falsche Messwerte korrigieren.
    """)

k.ausgabe("a = [1, 2, 3, 4, 5]\ni = 0\nwhile i < len(a):\n    a[i] = 0\n    i = i + 1\nprint(a)",
          "Die Schleife besucht jeden Index von 0 bis 4 und legt jedes Mal 0 hinein → "
          "[0, 0, 0, 0, 0]. (Livecoding 2)")
k.ausgabe("preise = [2, 5, 10]\ni = 0\nwhile i < len(preise):\n    preise[i] = preise[i] * 2\n    i += 1\nprint(preise)",
          "Jeder Preis wird an seinem Platz verdoppelt: [4, 10, 20].")
k.ausgabe("lst = [3, 4, 1, 2]\nsumme = 0\ni = 0\nwhile i < len(lst):\n    summe += lst[i]\n    i += 1\nprint(summe)",
          "3 + 4 + 1 + 2 = 10. Die Variable summe sammelt alle Werte ein.")
k.mc("Warum schreibt man   while i < len(lst):   und nicht   while i <= len(lst):  ?",
     ["Weil der höchste Index len(lst) - 1 ist, lst[len(lst)] gäbe einen IndexError",
      "Weil <= in while-Schleifen verboten ist",
      "Weil die Schleife sonst ein Element zu wenig besucht",
      "Es gibt keinen Unterschied"],
     "Mit `<=` würde i am Ende den Wert len(lst) erreichen, und lst[len(lst)] gibt es nicht.")

# ── Erklärung 4: Referenzen ─────────────────────────────────────────────────
k.erklaerung("Zwei Namen, eine Liste", r"""
    ## Achtung: lst2 = lst1 kopiert nicht!

    :::trace
    lst1 = [3, 1, 2]
    lst2 = lst1
    lst1.sort()
    print(lst2)
    :::

    `lst2 = lst1` erstellt KEINE neue Liste. Beide Namen sind nur
    **Referenzen** (Verweise) auf DIESELBE Liste. Ändert man sie über den
    einen Namen, sieht man die Änderung auch über den anderen.

    :::visual referenz
    {"namen": {"lst1": 0, "lst2": 0}, "objekte": [[1, 2, 3]]}
    :::

    :::analogie 🔐 Zurück zu den Schließfächern
    `lst2 = lst1` ist, als würdest du ein zweites Namensschild an
    DENSELBEN Schließfachschrank kleben. Egal, über welches Schild du ein
    Fach umräumst: Es ist derselbe Schrank. `lst1.copy()` dagegen stellt
    einen zweiten Schrank mit demselben Inhalt daneben.
    :::
    ---
    ## Eine echte Kopie mit .copy()

    :::code
    lst1 = [3, 1, 2]
    lst2 = lst1.copy()
    lst1.sort()
    print(lst1)
    print(lst2)
    :::

    :::visual referenz
    {"namen": {"lst1": 0, "lst2": 1}, "objekte": [[1, 2, 3], [3, 1, 2]]}
    :::

    !! `lst2 = lst1` → zwei Namen, EINE Liste. `lst2 = lst1.copy()` → zwei Listen.
    """)

k.ausgabe("lst1 = [3, 1, 2]\nlst2 = lst1\nlst1.sort()\nprint(lst2)",
          "lst2 ist nur ein zweiter Name für DIESELBE Liste. Wird sie sortiert, sieht man "
          "das auch über lst2: [1, 2, 3].",
          tipp="Ist lst2 eine Kopie oder dieselbe Liste?")
k.ausgabe("lst1 = [3, 1, 2]\nlst2 = lst1.copy()\nlst1.sort()\nprint(lst2)",
          "Mit .copy() ist lst2 eine echte, eigene Kopie. Das Sortieren von lst1 ändert "
          "lst2 nicht: [3, 1, 2].")
k.ausgabe("a = [1, 2]\nb = a\nb.append(3)\nprint(a)",
          "b und a zeigen auf dieselbe Liste. append über b verändert also auch das, was man "
          "über a sieht: [1, 2, 3].")
k.wf("Nach   lst2 = lst1   sind lst1 und lst2 zwei unabhängige Listen.", False,
     "Nein: Beide Namen verweisen auf dieselbe Liste. Eine unabhängige Kopie bekommst du "
     "mit lst1.copy().")

# ── Praxisteil ──────────────────────────────────────────────────────────────
k.luecke("Ergänze den Code, der alle Zahlen der Liste zusammenzählt und die Summe ausgibt.",
         """
         lst = [3, 4, 1, 2]
         summe = 0
         i = ___
         while i < ___(lst):
             summe += lst[___]
             i += 1
         print(summe)
         """,
         [["0"], ["len"], ["i"]],
         "i startet beim ersten Index 0 und läuft bis len(lst) - 1. In jeder Runde wird "
         "lst[i] zur Summe addiert.",
         tipp="Mit welchem Index beginnt eine Liste?")

k.code(r"""
    ## Erstes, Letztes, Länge

    Es gibt bereits eine Variable `liste` (vom Quiz vorgegeben, mindestens
    ein Element). Gib in drei Zeilen aus:
      1. das erste Element
      2. das letzte Element
      3. die Länge der Liste

        liste = [3, 4, 1, 2]   →   3
                                   2
                                   4
    """,
    [P(vorspann="liste = [3, 4, 1, 2]", exakt=["3", "2", "4"]),
     P(vorspann="liste = ['x']", exakt=["x", "x", "1"], beschreibung="nur ein Element"),
     P(vorspann="liste = [8, 1, 3, -4, 5, 0, 2, 11]", exakt=["8", "11", "8"])],
    """
    print(liste[0])
    print(liste[-1])
    print(len(liste))
    """,
    "Das erste Element hat Index 0, das letzte Index -1 – egal, wie lang die Liste ist. "
    "`len()` liefert die Länge.",
    tipps=["Das erste Element hat den Index 0.",
           "Für das letzte Element hilft ein negativer Index.",
           "print(liste[0]), print(liste[-1]), print(len(liste))"])

k.code(r"""
    ## Wetterstation: Messfehler korrigieren

    Die Variable `messwerte` (vom Quiz vorgegeben) enthält Temperaturen.
    Negative Werte sind hier Messfehler. Ersetze mit einer while-Schleife
    jeden negativen Wert **in der Liste** durch 0 und gib danach die
    ganze Liste mit `print(messwerte)` aus.

        messwerte = [12, -3, 15, -1, 9]   →   [12, 0, 15, 0, 9]
    """,
    [P(vorspann="messwerte = [12, -3, 15, -1, 9]", exakt=["[12, 0, 15, 0, 9]"]),
     P(vorspann="messwerte = [5, 6, 7]", exakt=["[5, 6, 7]"], beschreibung="nichts zu korrigieren"),
     P(vorspann="messwerte = [-2, -8]", exakt=["[0, 0]"], beschreibung="alles negativ"),
     P(vorspann="messwerte = []", exakt=["[]"], beschreibung="leere Liste"),
     P(vorspann="messwerte = [0, -1, 3]", exakt=["[0, 0, 3]"])],
    """
    i = 0
    while i < len(messwerte):
        if messwerte[i] < 0:
            messwerte[i] = 0
        i += 1
    print(messwerte)
    """,
    "Mit `messwerte[i] = 0` wird das Fach i überschrieben. Die Schleife besucht jeden "
    "Index genau einmal. Die 0 selbst ist kein Messfehler, deshalb passt `< 0` am besten. "
    "(`<= 0` liefert hier dasselbe Ergebnis, weil eine 0 nur durch 0 ersetzt würde.)",
    pflicht=["while"],
    tipps=["Gehe mit i = 0, 1, 2, … durch alle Indizes.",
           "In der Schleife: if messwerte[i] < 0: messwerte[i] = 0",
           "Das print(messwerte) steht NACH der Schleife."])

k.code(r"""
    ## Maximum ohne max()

    Die Variable `liste` (vom Quiz vorgegeben, mindestens ein Element)
    enthält Zahlen. Finde mit einer while-Schleife die größte Zahl und gib
    sie aus. Die Funktionen `max()` und `sort()` sind verboten.

        liste = [3, 4, 1, 2]   →   4
    """,
    # erwartet + anzahl: Die Zahl darf beschriftet sein ("Maximum: 4"), muss aber genau
    # einmal vorkommen (fängt Lösungen ab, die in der Schleife Zwischenstände ausgeben).
    [P(vorspann="liste = [3, 4, 1, 2]", erwartet=["4"], anzahl={"4": 1}),
     P(vorspann="liste = [-5, -2, -9]", erwartet=["-2"], anzahl={"-2": 1},
       beschreibung="nur negative Zahlen"),
     P(vorspann="liste = [7]", erwartet=["7"], anzahl={"7": 1}, beschreibung="nur ein Element"),
     P(vorspann="liste = [1, 9, 9, 2]", erwartet=["9"], anzahl={"9": 1}),
     P(vorspann="liste = [10, 3, 5]", erwartet=["10"], anzahl={"10": 1},
       beschreibung="Maximum ganz vorne")],
    """
    groesstes = liste[0]
    i = 1
    while i < len(liste):
        if liste[i] > groesstes:
            groesstes = liste[i]
        i += 1
    print(groesstes)
    """,
    "Starte mit dem ersten Element als „bisher Größtes“ und vergleiche jedes weitere damit. "
    "Würdest du mit `groesstes = 0` starten, käme bei lauter negativen Zahlen fälschlich 0 heraus.",
    verboten=["max(", "sort(", "sorted("],
    pflicht=["while"],
    tipps=["Merke dir in einer Variable den bisher größten Wert.",
           "Starte mit groesstes = liste[0], nicht mit 0 (denk an negative Zahlen!).",
           "In der Schleife: if liste[i] > groesstes: groesstes = liste[i]"])

# Die Tests prüfen mit `exakt` die genaue Reihenfolge der Zeilen. Damit ein Text in
# input("...") die Prüfung nicht stört, ersetzt dieser Vorspann input() durch eine
# Version, die den Aufforderungstext nicht ausgibt (nur für die Tests).
_OHNE_PROMPT = ("import builtins as _quiz_builtins\n"
                "def input(_text=''):\n"
                "    return _quiz_builtins.input()\n")

k.code(r"""
    ## Einkaufsliste ohne Doppelte

    Lies Artikel ein (je ein `input()`), bis `fertig` eingegeben wird. Ein Artikel, der schon auf der Liste steht, wird nicht noch
    einmal aufgenommen. Gib danach zuerst die Anzahl der Artikel aus und
    dann alle Artikel alphabetisch sortiert, je einen pro Zeile.

        Eingaben: Milch, Brot, Eier, Brot, fertig
        Ausgabe:  3
                  Brot
                  Eier
                  Milch
    """,
    [P(["Milch", "Brot", "Eier", "Brot", "fertig"], exakt=["3", "Brot", "Eier", "Milch"],
       vorspann=_OHNE_PROMPT),
     P(["fertig"], exakt=["0"], vorspann=_OHNE_PROMPT, beschreibung="gleich fertig: leere Liste"),
     P(["Brot", "Brot", "Apfel", "fertig"], exakt=["2", "Apfel", "Brot"], vorspann=_OHNE_PROMPT),
     P(["Tee", "fertig"], exakt=["1", "Tee"], vorspann=_OHNE_PROMPT)],
    """
    einkauf = []
    eingabe = input()
    while eingabe != "fertig":
        if eingabe not in einkauf:
            einkauf.append(eingabe)
        eingabe = input()
    einkauf.sort()
    print(len(einkauf))
    i = 0
    while i < len(einkauf):
        print(einkauf[i])
        i += 1
    """,
    "`not in` prüft, ob der Artikel noch fehlt. Erst nach dem Einlesen wird sortiert und "
    "ausgegeben. Strings werden von `sort()` alphabetisch sortiert.",
    tipps=["Starte mit einer leeren Liste und lies in einer Schleife ein, bis \"fertig\" kommt.",
           "Vor dem append prüfen: if eingabe not in einkauf: …",
           "Nach der Schleife: einkauf.sort(), print(len(einkauf)), dann mit einer zweiten "
           "while-Schleife alle Elemente ausgeben."])

k.zusammenfassung(r"""
    ## Listen auf einen Blick

        lst = [3, 4, 1, 2]
        lst[0]       # 3  (erstes)       lst[-1]   # 2  (letztes)
        len(lst)     # 4                 lst[4]    # IndexError!
        lst[0] = 7   # überschreiben

    | Befehl | Wirkung |
    |---|---|
    | `x in lst` | True, wenn x enthalten ist |
    | `lst.index(x)` | Position von x (sonst ValueError) |
    | `lst.append(x)` | hinten anhängen |
    | `lst.pop()` | letztes entfernen und zurückgeben |
    | `del lst[i]` | Element an Index i löschen |
    | `lst.sort()` / `lst.reverse()` | sortieren / umdrehen |
    | `lst1 + lst2` | zusammenfügen (neue Liste) |
    | `lst.copy()` | echte Kopie |

        i = 0
        while i < len(lst):      # alle Indizes 0 … len(lst) - 1
            lst[i] = lst[i] * 2  # Element überschreiben
            i += 1

    !! Indizes beginnen bei 0. `lst2 = lst1` ist KEINE Kopie, nur ein zweiter Name.
    """)
