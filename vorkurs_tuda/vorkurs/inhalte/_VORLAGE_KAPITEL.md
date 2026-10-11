# Vorlage für ein Kapitelmodul

Diese Datei wird **nicht** geladen, weil ihr Name mit `_` beginnt. Sie zeigt ein
vollständiges Beispielkapitel, das **alle Elementtypen**, **alle
Markup-Direktiven** und **alle Visual-Typen** richtig verwendet (Vertrag:
`vorkurs/ARCHITEKTUR.md`, Abschnitte 2–6).

So legst du ein neues Kapitel an:

1. Datei `vorkurs/inhalte/t<tag>_<nr>_<slug>.py` anlegen, z. B. `t2_06_mengen.py`
   (Bonus: `b_<nr>_<slug>.py`, Challenge: `c_<nr>_<slug>.py`). Die Reihenfolge
   ergibt sich aus dem Dateinamen: t1…t4, dann c_, dann b_.
2. Den Python-Block unten hineinkopieren und anpassen.
3. `python vorkurs_quiz.py --selbsttest` ausführen. Es darf **0 Fehler** geben.

## Regeln in Kürze

- `slug`: eindeutig und stabil, nur `a-z0-9_`. **Nie mehr ändern**, denn der Fortschritt hängt daran.
- Frage-IDs entstehen aus slug + Fragetext. Wird der Text einer Frage geändert,
  ist ihr Fortschritt weg. Kleine Tippfehler darf man trotzdem korrigieren.
- `teil`: `tag1`, `tag2`, `tag3`, `tag4`, `challenge` oder `bonus`.
- Bei `mc` ist die **erste** Option immer die richtige (sie wird gemischt angezeigt).
- Lernpfad: `lernziele` → (`erklaerung` → 2–6 Verständnisfragen) × n →
  2–4 Programmieraufgaben (`luecke`, `puzzle`, `code`, leicht → schwer) → `zusammenfassung`.
- Markup-Texte immer als `r"""..."""` schreiben (wegen `\n` in Beispielen).
- In `:::code`-Beispielen keine dreifachen Anführungszeichen verwenden.
- Inline: `` `code` `` und `**fett**`. Fett wird nur erkannt, wenn die `**` nicht
  direkt an Buchstaben oder Ziffern kleben. Ein einzelnes `**`, z. B. der
  Potenz-Operator in `2 ** 10`, bleibt deshalb normaler Text.

## Markup-Spickzettel

| Syntax | Wirkung |
|---|---|
| `---` (eigene Zeile) | neue Seite |
| `## Titel` | Überschrift |
| `!! Text` | Merksatz (direkt folgende `!!`-Zeilen werden verbunden) |
| 4+ Leerzeichen Einrückung | Codeblock (nur anzeigen) |
| `• Text`, `- Text`, `* Text` | Aufzählung (Fortsetzungszeilen auf Höhe des Textes einrücken) |
| `1. Text` | nummerierte Liste |
| `\| a \| b \|` | Tabelle (erste Zeile = Kopf, `\|---\|` optional) |
| `:::analogie 🏠 Titel` … `:::` | Alltagsbeispiel-Box |
| `:::achtung Titel` … `:::` | Warnbox (typischer Fehler) |
| `:::info Titel` … `:::` | Infobox |
| `:::code` / `:::code eingaben=Anna\|17` … `:::` | ausführbares Beispiel |
| `:::trace` … `:::` | Beispiel mit sofort geöffneter Schritt-für-Schritt-Ansicht |
| `:::visual TYP` + JSON … `:::` | Visualisierung |
| `:::vergleich Links \| Rechts` … `\|\|\|` … `:::` | zwei Spalten |

## Beispielkapitel

```python
# -*- coding: utf-8 -*-
"""Kapitel: Vorlage – zeigt alle Möglichkeiten."""
from ..engine import neues_kapitel, P, F

k = neues_kapitel(
    slug="vorlage_demo",
    titel="Vorlage – Alles auf einen Blick",
    beschreibung="Ein Beispielkapitel mit allen Elementen",
    quelle="Vorlesung 1, Übung 1",
    teil="tag1",
    icon="🧪")

k.lernziele([
    "Ich kann einer Variable einen Wert zuweisen",
    "Ich kann mit einer Schleife etwas wiederholen",
    "Ich kann eine kleine Funktion mit return schreiben",
])

# ── Erklärung 1: normales Markup, Boxen, Code, Vergleich ─────────────────
k.erklaerung("Variablen und Ausgaben", r"""
    ## Variablen sind beschriftete Kisten

    Eine **Variable** speichert einen Wert unter einem Namen. Mit `=` legst
    du den Wert hinein.

        alter = 19
        name = "Lea"

    !! Rechts vom = wird zuerst gerechnet, dann wird das Ergebnis gespeichert.

    Wichtige Regeln:
      • Namen beginnen mit einem Buchstaben oder `_`,
        aber nie mit einer Ziffer.
      • Groß-/Kleinschreibung zählt.
      - Bindestriche sind verboten.

    Reihenfolge beim Ausführen:
      1. rechte Seite ausrechnen
      2. Ergebnis in die Kiste legen

    | Wert | Typ | Beispiel |
    |---|---|---|
    | ganze Zahl | `int` | `42` |
    | Kommazahl | `float` | `2.5` |
    | Text | `str` | `"Hallo"` |
    ---
    ## Analogie, Warnung, Info

    :::analogie 🏠 Wie ein Umzugskarton
    Du klebst ein **Etikett** auf einen Karton. Der Name ist das Etikett,
    der Inhalt ist der Wert.
    :::

    :::achtung Typischer Fehler: = und ==
    `=` speichert einen Wert, `==` vergleicht zwei Werte.
        if alter == 18:
            print("Volljährig")
    :::

    :::info Hintergrund
    Python merkt sich den Typ automatisch. Man nennt das *dynamische Typisierung*.
    :::
    ---
    ## Selbst ausprobieren

    :::code
    alter = 19
    alter = alter + 1
    print("Nächstes Jahr bist du", alter)
    :::

    Mit Eingaben (sie gehen der Reihe nach an `input()`):

    :::code eingaben=Anna|17
    name = input("Wie heißt du? ")
    alter = int(input("Wie alt bist du? "))
    print(f"Hallo {name}, in 3 Jahren bist du {alter + 3}.")
    :::

    :::trace
    a = [1, 2, 3]
    b = a
    b.append(4)
    print(a)
    :::

    :::vergleich ✘ Ohne Variable | ✔ Mit Variable
    Der Wert steht mehrfach im Code:
        print(19 * 12)
        print(19 + 1)
    |||
    Der Wert steht nur einmal im Code:
        alter = 19
        print(alter * 12)
        print(alter + 1)
    :::
    """)

k.mc("Was passiert bei   x = 2 + 3   zuerst?",
     ["Die rechte Seite 2 + 3 wird ausgerechnet",     # erste Option = richtig
      "x wird gelöscht",
      "x wird mit 5 verglichen"],
     "Erst wird rechts gerechnet (5), dann wird das Ergebnis in x gelegt.",
     tipp="Lies die Zeile von rechts nach links.")

k.wf("Variablennamen dürfen mit einer Ziffer beginnen.", False,
     "Namen beginnen mit einem Buchstaben oder `_` – `2alter` ist ungültig.")

k.text("Wie heißt die Python-Schreibweise für Variablennamen wie anzahl_kekse?",
       ["snake_case", "snake case"],
       "snake_case: alles klein, Wörter mit Unterstrich getrennt.",
       tipp="Ein Tier, das lang und dünn ist ...")

k.ausgabe("x = 5\nx = x * 2\nprint(x)",
          "Rechte Seite zuerst: 5 * 2 = 10, das kommt zurück in x.",
          tipp="Was steht nach Zeile 2 in x?")

k.ausgabe("print(7 / 2)",
          "/ liefert immer eine Kommazahl: 3.5.",
          akzeptiert=["3.5"],
          frage="Was gibt Python hier aus? (Kommazahlen mit Punkt!)")

k.ausdruck("Schreibe einen Ausdruck, der das letzte Element von lst liefert.",
           tests=[{"lst": [3, 1, 4]}, {"lst": [9]}, {"lst": ["a", "b"]}],
           loesung="lst[-1]",
           erklaerung="Der Index -1 zählt von hinten.",
           tipp="Negative Indizes zählen von hinten.",
           muss_enthalten="[")

# ── Erklärung 2: alle Visual-Typen ──────────────────────────────────────
k.erklaerung("Bilder sagen mehr als Worte", r"""
    ## Variablen und Typen

    :::visual variablen
    {"vars": [{"name": "alter", "wert": "19", "typ": "int"}],
     "schritte": [[{"name": "alter", "wert": "19", "typ": "int"}],
                  [{"name": "alter", "wert": "20", "typ": "int"}]],
     "texte": ["alter = 19", "alter = alter + 1"]}
    :::

    :::visual typen
    {"werte": ["42", "3.14", "'Hallo'", "True", "None"]}
    :::

    :::visual referenz
    {"namen": {"a": 0, "b": 0, "c": 1}, "objekte": [[1, 2, 3], [1, 2, 3]]}
    :::
    ---
    ## Listen, Strings, Dictionaries

    :::visual liste
    {"name": "lst", "werte": [3, 4, 1, 2], "markiert": [0], "slice": "1:3",
     "interaktiv": false, "negativ": true}
    :::

    :::visual string
    {"text": "Hallo", "markiert": [1], "slice": null, "interaktiv": true}
    :::

    :::visual dict
    {"name": "telefon", "paare": [["Anna", "0151 123"], ["Ben", "0170 456"]],
     "markiert": ["Anna"]}
    :::
    ---
    ## Abläufe, Entscheidungen, Schleifen

    :::visual ablauf
    {"schritte": [{"icon": "👩‍💻", "text": "Du schreibst Quelltext"},
                  {"icon": "🐍", "text": "Python übersetzt"},
                  {"icon": "💻", "text": "Der Computer führt aus"}]}
    :::

    :::visual entscheidung
    {"bedingung": "alter >= 18", "ja": "Eintritt", "nein": "Kein Eintritt",
     "elif": [{"bedingung": "alter >= 16", "text": "Eintritt mit Begleitung"}]}
    :::

    :::visual schleife
    {"bedingung": "zahl < 5", "koerper": ["print(zahl)", "zahl += 1"],
     "danach": "print('fertig')", "art": "while"}
    :::

    :::visual zahlenstrahl
    {"start": 0, "stop": 10, "step": 2, "interaktiv": true}
    :::

    :::visual wahrheitstabelle
    {"variablen": ["a", "b"], "ausdruecke": ["a and b", "a or b", "not a"]}
    :::
    ---
    ## Funktionen und Rekursion

    :::visual funktion
    {"name": "verdoppeln", "eingaben": ["x = 4"], "ausgabe": "8", "innen": "return x * 2"}
    :::

    :::visual stapel
    {"titel": "Aufrufstapel", "rahmen": ["fak(3)", "fak(2)", "fak(1)"],
     "rueckgaben": ["6", "2", "1"]}
    :::

    :::visual baum
    {"wurzel": {"text": "fib(3)", "kinder": [
        {"text": "fib(2)", "kinder": [{"text": "fib(1)"}, {"text": "fib(0)"}]},
        {"text": "fib(1)"}]}}
    :::
    """)

k.mc("Wie oft läuft   for i in range(0, 10, 2):   ?",
     ["5-mal", "10-mal", "4-mal", "6-mal"],
     "0, 2, 4, 6, 8 – die 10 selbst ist nicht dabei (Stop ist exklusiv).")

# ── Praxisteil: Lücke → Puzzle → Code (leicht → schwer) ──────────────────
k.luecke("Ergänze den Code, sodass die Zahlen 1 bis 3 ausgegeben werden.",
         """
         for i in ___(1, ___):
             print(i)
         """,
         [["range"], ["4"]],                     # pro ___ eine Liste akzeptierter Antworten
         "range(1, 4) liefert 1, 2, 3 – das Ende ist exklusiv.",
         tipp="Das Ende von range ist nicht mehr dabei.")

k.puzzle("Bringe die Zeilen in die richtige Reihenfolge: Summe von 1 bis 4 ausgeben.",
         """
         summe = 0
         for i in range(1, 5):
             summe += i
         print(summe)
         """,
         "Erst die Summe auf 0 setzen, dann in der Schleife addieren, am Ende ausgeben.",
         tipp="Was muss vor der Schleife passieren?",
         ablenker=["    summe = 0", "print(i)"])

k.code(r"""
    ## Begrüßung

    Lies einen Namen mit `input()` ein und gib `Hallo <Name>!` aus.
        Eingabe:  Anna
        Ausgabe:  Hallo Anna!
    """,
    [P(["Anna"], ["Hallo Anna!"]),
     P(["Bob"], exakt=["Hallo Bob!"], beschreibung="genau eine Zeile")],
    """
    name = input()
    print(f"Hallo {name}!")
    """,
    "input() liefert den Text, ein f-String setzt ihn ein.",
    tipps=["Du brauchst input() und print().",
           "Speichere die Eingabe in einer Variable name.",
           'print(f"Hallo {name}!")'],
    vorlage="name = ...\n")

k.code(r"""
    ## Fakultät rekursiv

    Schreibe eine Funktion `fakultaet(n)`, die n! **rekursiv** berechnet
    (ohne Schleife). Es gilt `0! = 1`.
    """,
    [F("fakultaet(0)", 1), F("fakultaet(5)"), F("fakultaet(10)")],   # ohne soll: aus der Musterlösung
    """
    def fakultaet(n):
        if n == 0:
            return 1
        return n * fakultaet(n - 1)
    """,
    "Rekursionsanker n == 0, sonst n * fakultaet(n - 1).",
    verboten=["for", "while"],
    pflicht=["def ", "return"],
    rekursiv="fakultaet",
    tipps=["Was ist der einfachste Fall?", "fakultaet(n) = n * fakultaet(n - 1)"])

k.zusammenfassung(r"""
    ## Das Wichtigste

      • `name = wert` speichert einen Wert – rechts wird zuerst gerechnet.
      • `range(start, stop, step)` – stop ist exklusiv.
      • Funktionen: `def`, Parameter, `return`.

    !! Eine Variable merkt sich einen WERT, keine Rechnung.

        def verdoppeln(x):
            return x * 2
    """)
```

## Visual-Typen (Kurzreferenz)

`variablen`, `liste`, `string`, `dict`, `referenz`, `ablauf`, `entscheidung`,
`schleife`, `zahlenstrahl`, `wahrheitstabelle`, `stapel`, `baum`, `funktion`,
`typen`. Die Felder stehen in ARCHITEKTUR.md, Abschnitt 4. `markup.parse`
ergänzt bei `typen` das Feld `daten["typen"]` (per Python ermittelt) und bei
`wahrheitstabelle` das Feld `daten["zeilen"]` (berechnete Werte).
