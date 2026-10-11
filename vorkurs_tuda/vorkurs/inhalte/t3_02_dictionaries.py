# -*- coding: utf-8 -*-
"""Kapitel: Dictionaries – Das Telefonbuch (Vorlesung 3, Folien 8–11; Livecoding 3.1)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="dictionaries",
    titel="Dictionaries – Das Telefonbuch",
    beschreibung="Werte über Schlüssel finden: d['name'], get(), in, del, items()",
    quelle="Vorlesung 3, Livecoding 3",
    teil="tag3",
    icon="📖")

k.lernziele([
    "Ich kann ein Dictionary anlegen und über einen Schlüssel auf den Wert zugreifen",
    "Ich kann mit get() oder in verhindern, dass ein KeyError entsteht",
    "Ich kann Einträge hinzufügen, überschreiben und mit del entfernen",
    "Ich kann Tupel als Schlüssel verwenden und mit d.items() alle Paare durchlaufen",
])

# ── Erklärung 1: Anlegen ────────────────────────────────────────────────
k.erklaerung("Dictionaries (dict)", r"""
    ## Zugriff mit Namen statt Nummern

    Bei einer Liste findest du Werte über ihre Position (0, 1, 2, …). Ein
    **Dictionary** (englisch für Wörterbuch, Typ `dict`) erlaubt den Zugriff
    über beliebige **Schlüssel** (englisch *key*). Zu jedem Schlüssel gehört
    ein **Wert** (*value*).

    :::analogie 📞 Das Telefonbuch
    Im Telefonbuch suchst du nicht „den 347. Eintrag“, sondern den Namen
    „Oma“, und bekommst die Nummer.
      • Der Name ist der **Schlüssel**, die Nummer ist der **Wert**.
      • Nachschlagen: `telefon['Oma']`.
      • Jeder Name steht nur **einmal** drin. Trägst du „Oma“ neu ein, wird die
        alte Nummer überschrieben.
      • Steht ein Name nicht drin, gibt es Alarm (`KeyError`), außer du sagst
        vorher: „Sonst nimm ‚unbekannt‘.“ Das macht `get()`.
      • Einen Eintrag durchstreichen: `del telefon['Pizza']`.
    :::

    :::visual dict
    {"titel": "Ein Dictionary als Telefonbuch", "name": "telefon",
     "paare": [["Oma", "06151 123456"], ["Pizza", "06151 999999"], ["Kim", "0170 5555"]],
     "markiert": ["Oma"]}
    :::
    ---
    ## Ein Dictionary erstellen

        d = dict()          # leeres Dictionary
        d = {}              # auch leer
        d = {
            'a': 5,
            'x': 'lorem'
        }

      • Schlüssel und Wert werden mit `:` verbunden, die Paare mit `,` getrennt.
      • Schlüssel dürfen **unterschiedliche Typen** haben (z. B. `1` und `'zwei'`).
      • Werte ebenfalls.

    Die Folie zeigt dazu ein Meme: „Es ist Mittwoch, meine Duden.“ Ein
    Duden ist ein Wörterbuch: Wort → Erklärung. Genau so funktioniert `dict`.

    :::code
    telefon = {"Oma": "06151 123456", "Pizza": "06151 999999"}
    print(telefon["Oma"])
    print(len(telefon))
    print(telefon)
    :::
    """)

k.ausgabe("d = {'a': 5, 'x': 'lorem'}\nprint(d['a'])", "Der Wert zum Schlüssel 'a' ist 5.")
k.mc("Mit welchen Klammern erstellt man ein Dictionary mit Inhalt?",
     ["Geschweifte Klammern { }", "Eckige Klammern [ ]", "Runde Klammern ( )", "Spitze Klammern < >"],
     "{'a': 5} – geschweifte Klammern, Schlüssel: Wert.")
k.wf("Alle Schlüssel eines Dictionaries müssen denselben Typ haben.", False,
     "Schlüssel dürfen unterschiedliche Typen haben (z.B. 1 und 'zwei').")
k.ausgabe("d = {1: 'eins', 'zwei': 2, 3.0: [3]}\nprint(d['zwei'])",
          "Schlüssel und Werte dürfen unterschiedliche Typen haben.")

# ── Erklärung 2: Zugriff ohne Absturz ────────────────────────────────────
k.erklaerung("Zugreifen ohne Absturz", r"""
    ## Zugriffe

        d = {'a': 5, 'x': 'lorem'}
        d['a']            # → 5
        d['b']            # → FEHLER: KeyError (den Schlüssel gibt es nicht)
        d.get('b', 0)     # → 0  ('b' fehlt, also der Standardwert 0)
        d.get('a', 0)     # → 5
        d.get('b')        # → None (ohne Standardwert)

    Prüfen, ob ein Schlüssel existiert:

        'a' in d          # → True
        'b' in d          # → False

    !! Zwei Wege ohne Fehler: d.get(schluessel, standardwert) oder vorher
    !! mit schluessel in d prüfen.

    :::code eingaben=Opa
    telefon = {"Oma": "06151 123456", "Pizza": "06151 999999"}
    name = input("Wen willst du anrufen? ")
    if name in telefon:
        print(telefon[name])
    else:
        print("Nicht im Telefonbuch")
    print(telefon.get(name, "unbekannt"))
    :::

    :::achtung KeyError und None
    `d['fehlt']` bricht das Programm mit `KeyError` ab. `d.get('fehlt')`
    liefert **None**, nicht 0. Willst du 0, schreib `d.get('fehlt', 0)`.
    :::
    """)

k.ausgabe("d = {'a': 5, 'x': 'lorem'}\nprint(d['b'])",
          "Den Schlüssel 'b' gibt es nicht → KeyError.")
k.ausgabe("d = {'a': 5, 'x': 'lorem'}\nprint(d.get('b', 0))",
          "get() mit Standardwert: 'b' fehlt → 0, und es gibt keinen Fehler.")
k.ausgabe("d = {'a': 5, 'x': 'lorem'}\nprint(d.get('a', 0))",
          "'a' existiert → der echte Wert 5 wird geliefert.")
k.ausgabe("d = {'x': 1}\nprint(d.get('y'))",
          "Ohne Standardwert liefert get() bei fehlendem Schlüssel None.")
k.mc("Wie kommst du an einen Wert, OHNE dass ein Fehler entsteht, falls der Schlüssel fehlt?",
     ["d.get(schluessel, standardwert) – oder vorher mit 'schluessel in d' prüfen",
      "d[schluessel] – das gibt nie einen Fehler",
      "d.find(schluessel)",
      "d(schluessel)"],
     "Quiz aus Vorlesung 3: get() mit Standardwert, oder erst mit in prüfen.")
k.mc("Welcher Fehler tritt auf, wenn man mit d['xyz'] auf einen fehlenden Schlüssel zugreift?",
     ["KeyError", "IndexError", "NameError", "ValueError"],
     "Key = Schlüssel → KeyError. (IndexError gibt es bei Listen.)")

# ── Erklärung 3: Ändern ──────────────────────────────────────────────────
k.erklaerung("Hinzufügen, ändern, löschen", r"""
    ## Einträge hinzufügen und ändern

    Ein Dictionary kann wachsen. Man weist einfach einem Schlüssel einen Wert zu:

        d['neu'] = 42     # neuer Eintrag, weil es 'neu' noch nicht gibt
        d['a'] = 6        # 'a' gibt es schon: der Wert wird überschrieben

    Entfernen:

        del d['a']

    Schau dir Schritt für Schritt an, wie sich das Dictionary verändert:

    :::trace
    preise = {"Brot": 2.5}
    preise["Milch"] = 1.2
    preise["Brot"] = 2.8
    del preise["Milch"]
    print(preise)
    :::

    :::info Skript oder Konsole?
    Im Livecoding steht nach `d[2] = 5` einfach `d` in einer eigenen Zeile.
    Das zeigt den Inhalt nur in der **interaktiven Python-Konsole** (`>>>`) an.
    In einem Programm (Skript) passiert bei so einer Zeile gar nichts. Dort
    brauchst du `print(d)`.
    :::
    """)

k.ausgabe("d = {'a': 5, 'x': 'lorem'}\nprint('a' in d)\ndel d['a']\nprint('a' in d)",
          "Erst ist 'a' drin (True), nach del nicht mehr (False).")
k.ausgabe('preise = {"Brot": 2.5, "Milch": 1.2}\npreise["Butter"] = 2\nprint(len(preise))',
          "Durch die Zuweisung kommt 'Butter' neu hinzu → 3 Einträge.")
k.ausgabe('preise = {"Brot": 2.5, "Milch": 1.2}\npreise["Milch"] = 1.5\nprint(preise["Milch"])',
          "Gibt es den Schlüssel schon, wird der Wert überschrieben.")
k.mc("Wie entfernst du den Eintrag 'a' aus dem Dictionary d?",
     ["del d['a']", "d.remove['a']", "d['a'] = None", "d - 'a'"],
     "del d['a'] löscht den Eintrag. d['a'] = None würde ihn behalten (nur mit Wert None).")

# ── Erklärung 4: Tupel als Schlüssel, items() ───────────────────────────
k.erklaerung("Tupel als Schlüssel und alle Paare durchgehen", r"""
    ## Welche Schlüssel sind erlaubt?

    Im Livecoding werden ganz verschiedene Schlüssel benutzt:

        d = {2: 5}
        d['name'] = 'Tim'
        d['age'] = 28
        d[(2, 3)] = 'no'      # ein TUPEL als Schlüssel
        print(d[(2, 3)])      # → no

    Tupel als Schlüssel sind praktisch für alles mit zwei Koordinaten, z. B.
    einen Sitzplan `{(reihe, platz): name}` oder ein Spielfeld.

    :::achtung Listen sind als Schlüssel verboten
    Ein Schlüssel darf sich nie ändern, sonst fände Python ihn nicht wieder.
    Darum sind unveränderliche Werte (Zahlen, Strings, **Tupel**) erlaubt,
    Listen aber nicht:
        d = {[1, 2]: 'x'}     # TypeError: unhashable type: 'list'
    Hier zahlt sich die „versiegelte Box“ aus dem Tupel-Kapitel aus.
    :::
    ---
    ## Alle Paare durchgehen: d.items()

    Mit einer for-Schleife und `d.items()` bekommst du jedes Paar als Tupel
    `(schluessel, wert)`, das direkt ausgepackt wird. (Die for-Schleife lernst
    du im nächsten Kapitel genau kennen. Hier reicht: Sie geht alle Paare
    nacheinander durch.)

    :::code
    d = {2: 5, 'name': 'Tim', (2, 3): 'no'}
    for key, value in d.items():
        print(f'Für Schlüssel "{key}" ist der Wert "{value}" gespeichert')
    :::

    Die Paare kommen in der Reihenfolge, in der sie eingefügt wurden.
    Nur die Schlüssel: `d.keys()`, nur die Werte: `d.values()`.
    ---
    ## Typisches Muster: Zählen wie mit einer Strichliste

        woerter = ["Apfel", "Birne", "Apfel"]
        zaehler = {}
        for w in woerter:
            zaehler[w] = zaehler.get(w, 0) + 1
        # zaehler ist jetzt {'Apfel': 2, 'Birne': 1}

    `for w in woerter:` heißt: Nimm nacheinander jedes Wort der Liste.
    `zaehler.get(w, 0)` liefert den bisherigen Zählerstand, oder 0, wenn das
    Wort noch nie vorkam. Dann kommt 1 dazu.
    """)

k.ausgabe("sitzplan = {(1, 1): 'Anna', (1, 2): 'Ben'}\nprint(sitzplan[(1, 2)])",
          "Der Schlüssel ist das Tupel (1, 2) – Reihe 1, Platz 2. Dort sitzt Ben.")
k.ausgabe("d = {[1, 2]: 'x'}",
          "Listen sind veränderlich und darum als Schlüssel verboten → TypeError: unhashable "
          "type: 'list'. Ein Tupel (1, 2) wäre erlaubt.",
          tipp="Darf sich ein Schlüssel nachträglich ändern?")
k.wf("Ein Tupel wie (2, 3) darf als Schlüssel in einem Dictionary benutzt werden.", True,
     "Ja, Tupel sind unveränderlich und deshalb als Schlüssel erlaubt (Livecoding: d[(2, 3)] = 'no').")
k.ausgabe("d = {'a': 1, 'b': 2}\nfor k, v in d.items():\n    print(k, v)",
          "items() liefert die Paare ('a', 1) und ('b', 2). Sie werden in k und v ausgepackt.")
k.ausgabe('woerter = ["Apfel", "Birne", "Apfel"]\nzaehler = {}\nfor w in woerter:\n'
          '    zaehler[w] = zaehler.get(w, 0) + 1\nprint(zaehler["Apfel"])',
          "Apfel kommt zweimal vor. Beim ersten Mal: get → 0, + 1 = 1. Beim zweiten Mal: 1 + 1 = 2.")

# ── Praxis ───────────────────────────────────────────────────────────────
k.luecke("Ergänze den Code: Für 'Kim' soll 'unbekannt' erscheinen (ohne Fehler), danach sollen "
         "alle Namen mit Nummer ausgegeben werden.",
         """
         telefon = {"Anna": "0151 111", "Ben": "0170 222"}
         print(telefon.___("Kim", "unbekannt"))
         for name, nummer in telefon.___():
             print(name, nummer)
         """,
         [["get"], ["items"]],
         "get(schluessel, standardwert) liefert den Standardwert, wenn der Schlüssel fehlt. "
         "items() liefert alle Paare (Schlüssel, Wert).",
         tipp="Die erste Methode „holt“ einen Wert, die zweite liefert alle „Elemente“ als Paare.")

_TELEFON = 'telefonbuch = {"Oma": "06151 123456", "Pizza": "06151 999999", "Mia": "0170 5555"}'

k.code(r"""
    ## Telefonbuch

    Das Dictionary `telefonbuch` ist schon vorgegeben:

        telefonbuch = {"Oma": "06151 123456", "Pizza": "06151 999999", "Mia": "0170 5555"}

    Lies einen Namen mit `input()` ein und gib die passende Nummer aus. Steht
    der Name nicht im Telefonbuch, gib `Unbekannt` aus. Das Programm darf
    dabei nicht abstürzen.

        Eingabe: Oma     Ausgabe: 06151 123456
        Eingabe: Opa     Ausgabe: Unbekannt
    """,
    [P(["Oma"], ["06151 123456"], vorspann=_TELEFON),
     P(["Mia"], ["0170 5555"], vorspann=_TELEFON),
     P(["Opa"], ["Unbekannt"], nicht=["06151"], vorspann=_TELEFON),
     P(["oma"], ["Unbekannt"], vorspann=_TELEFON, beschreibung="Groß-/Kleinschreibung zählt"),
     P(["Kim"], ["0160 42"], vorspann='telefonbuch = {"Kim": "0160 42"}',
       beschreibung="anderes Telefonbuch")],
    """
    name = input("Name: ")
    print(telefonbuch.get(name, "Unbekannt"))
    """,
    "get() mit Standardwert erledigt beides in einer Zeile. Genauso richtig ist "
    "`if name in telefonbuch: ... else: print('Unbekannt')`.",
    tipps=["Was passiert bei telefonbuch['Opa']? Wie vermeidest du das?",
           "Es gibt eine Methode, der man einen Standardwert mitgeben kann.",
           'print(telefonbuch.get(name, "Unbekannt"))'],
    vorlage="# telefonbuch ist schon vorgegeben\nname = input(\"Name: \")\n",
    streng=True)

_LAGER = 'lager = {"Äpfel": 3, "Birnen": 0}'

k.code(r"""
    ## Lager auffüllen

    Das Dictionary `lager` ist schon vorgegeben, z. B.

        lager = {"Äpfel": 3, "Birnen": 0}

    Lies nacheinander einen **Artikel** und eine **Anzahl** (ganze Zahl) ein.
    Erhöhe den Bestand des Artikels um diese Anzahl. Gibt es den Artikel noch
    nicht, wird er mit dieser Anzahl neu angelegt. Gib am Ende das ganze
    Dictionary mit `print(lager)` aus.

        Eingaben: Äpfel, 2    Ausgabe: {'Äpfel': 5, 'Birnen': 0}
        Eingaben: Kiwis, 4    Ausgabe: {'Äpfel': 3, 'Birnen': 0, 'Kiwis': 4}
    """,
    [P(["Äpfel", "2"], ["{'Äpfel': 5, 'Birnen': 0}"], vorspann=_LAGER),
     P(["Kiwis", "4"], ["{'Äpfel': 3, 'Birnen': 0, 'Kiwis': 4}"], vorspann=_LAGER),
     P(["Birnen", "10"], ["{'Äpfel': 3, 'Birnen': 10}"], vorspann=_LAGER),
     P(["Brot", "1"], ["{'Brot': 1}"], vorspann="lager = {}", beschreibung="leeres Lager")],
    """
    artikel = input("Artikel: ")
    anzahl = int(input("Anzahl: "))
    lager[artikel] = lager.get(artikel, 0) + anzahl
    print(lager)
    """,
    "`lager.get(artikel, 0)` liefert den alten Bestand oder 0 für neue Artikel. Darauf kommt "
    "die Anzahl. Mit `lager[artikel] = anzahl` würde der alte Bestand verloren gehen, mit "
    "`lager[artikel] += anzahl` gäbe es bei neuen Artikeln einen KeyError.",
    tipps=["Unterscheide zwei Fälle: Artikel schon da oder neu.",
           "Mit `if artikel in lager:` oder mit `lager.get(artikel, 0)`.",
           "lager[artikel] = lager.get(artikel, 0) + anzahl"],
    streng=True)

_SITZPLAN = 'sitzplan = {(1, 1): "Anna", (1, 2): "Ben", (2, 1): "Deniz"}'

k.code(r"""
    ## Sitzplan im Hörsaal (Tupel als Schlüssel)

    Das Dictionary `sitzplan` ist schon vorgegeben. Jeder Schlüssel ist ein
    Tupel `(reihe, platz)`:

        sitzplan = {(1, 1): "Anna", (1, 2): "Ben", (2, 1): "Deniz"}

    Lies nacheinander Reihe und Platz ein (zwei ganze Zahlen). Gib aus, wer
    dort sitzt. Ist der Platz nicht im Sitzplan, gib `frei` aus.

        Eingaben: 1, 2    Ausgabe: Ben
        Eingaben: 2, 2    Ausgabe: frei
    """,
    [P(["1", "2"], ["Ben"], vorspann=_SITZPLAN),
     P(["2", "1"], ["Deniz"], vorspann=_SITZPLAN),
     P(["1", "1"], ["Anna"], vorspann=_SITZPLAN),
     P(["2", "2"], ["frei"], vorspann=_SITZPLAN),
     P(["7", "3"], ["frei"], vorspann=_SITZPLAN)],
    """
    reihe = int(input("Reihe: "))
    platz = int(input("Platz: "))
    print(sitzplan.get((reihe, platz), "frei"))
    """,
    "Aus den beiden Zahlen wird das Tupel (reihe, platz) gebaut, und genau das ist der "
    "Schlüssel. Wichtig ist int(): Der Schlüssel (1, 2) ist nicht dasselbe wie ('1', '2').",
    tipps=["Wie sieht ein Schlüssel im Sitzplan aus?",
           "Lies beide Zahlen mit int(input()) ein und baue daraus das Tupel (reihe, platz).",
           'print(sitzplan.get((reihe, platz), "frei"))'],
    streng=True)

k.zusammenfassung(r"""
    ## Dictionaries auf einen Blick

        d = {'a': 5, 'x': 'lorem'}     # Schlüssel: Wert
        d['a']                         # → 5
        d['b']                         # KeyError!
        d.get('b', 0)                  # → 0 (Standardwert statt Fehler)
        'a' in d                       # → True
        d['neu'] = 42                  # hinzufügen oder überschreiben
        del d['a']                     # entfernen
        d[(2, 3)] = 'no'               # Tupel als Schlüssel ist erlaubt
        for key, value in d.items():   # alle Paare durchgehen
            print(key, value)

    | Ich will … | Code |
    |---|---|
    | sicher nachschlagen | `d.get(k, standard)` oder `if k in d:` |
    | zählen | `z[w] = z.get(w, 0) + 1` |
    | alle Schlüssel | `for k in d:` oder `d.keys()` |
    | alle Werte | `d.values()` |

    !! Schlüssel sind eindeutig und unveränderlich (Zahl, String, Tupel, aber keine Liste).
    """)
