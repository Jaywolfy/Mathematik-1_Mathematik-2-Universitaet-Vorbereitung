# -*- coding: utf-8 -*-
"""Kapitel: while-Schleifen, break & continue (Vorlesung 2, Folien 24–37; Livecoding 2.3/2.4)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="while_schleifen",
    titel="while-Schleifen, break & continue",
    beschreibung="Dinge wiederholen, solange eine Bedingung gilt",
    quelle="Vorlesung 2, Livecoding 2",
    teil="tag2",
    icon="🔁")

k.lernziele([
    "Ich kann eine while-Schleife mit Zählvariable schreiben und vorhersagen, wann sie endet",
    "Ich erkenne Endlosschleifen, vermeide sie und kann ein Programm mit Strg+C abbrechen",
    "Ich kann mit break und continue Schleifen abbrechen oder Runden überspringen",
    "Ich kann Schleifen mit while True + break oder mit einer Abbruch-Variable bauen",
    "Ich kann den Ablauf einer Schleife Runde für Runde nachvollziehen",
])

# ── Erklärung 1: while ──────────────────────────────────────────────────────
k.erklaerung("Die while-Schleife", r"""
    ## Warum Schleifen?

    Oft soll ein Code-Block MEHRFACH ausgeführt werden. Man könnte ihn
    kopieren und einfügen, aber das ist fehleranfällig und unübersichtlich.
    **Schleifen** führen einen Block mehrfach aus, ohne dass man ihn
    mehrfach schreiben muss. Wie oft, steuert eine **Bedingung**.

        while <Bedingung>:
            <Körper>

    Ausformuliert: **„Solange <Bedingung>, dann führe <X> aus.“**

    Die Zeile mit `while` heißt **Schleifenkopf**, der eingerückte Block
    darunter **Schleifenkörper**. Ein Durchlauf des Körpers ist eine
    **Iteration** (Runde).

    :::analogie 🍽️ Der volle Teller
    „SOLANGE noch etwas auf dem Teller ist: einen Bissen essen.“
      • Vor JEDEM Bissen schaust du auf den Teller. Das ist die Bedingung
        im Schleifenkopf.
      • Der Bissen ist der Schleifenkörper.
      • Jeder Bissen macht den Teller leerer. Ohne diese Veränderung
        würdest du ewig weiteressen: eine Endlosschleife.
      • Ist der Teller schon am Anfang leer, isst du gar nichts. Der
        Körper läuft dann kein einziges Mal.
    :::
    ---
    ## So läuft eine while-Schleife ab

    :::visual schleife
    {"bedingung": "i < 3", "koerper": ["print(i)", "i += 1"], "danach": "print('fertig')", "art": "while"}
    :::

      1. Bedingung prüfen. Ist sie `False`: weiter hinter der Schleife.
      2. Ist sie `True`: den ganzen Körper ausführen.
      3. Zurück zu Schritt 1.

    :::visual variablen
    {"vars": [{"name": "i", "wert": "0", "typ": "int"}],
     "schritte": [[{"name": "i", "wert": "0", "typ": "int"}],
                  [{"name": "i", "wert": "1", "typ": "int"}],
                  [{"name": "i", "wert": "2", "typ": "int"}],
                  [{"name": "i", "wert": "3", "typ": "int"}]],
     "texte": ["Start: i = 0. 0 < 3 ist True → print(0), dann i += 1",
               "1 < 3 ist True → print(1), dann i += 1",
               "2 < 3 ist True → print(2), dann i += 1",
               "3 < 3 ist False → die Schleife endet, print('fertig')"]}
    :::
    ---
    ## Beispiel aus der Vorlesung

    Diese Schleife zählt von 0 bis 4 und gibt die Buchstaben eines
    Strings aus. Klicke dich Schritt für Schritt hindurch:

    :::trace
    i = 0
    s = 'Lorem'
    while i < len(s):
        print(f'Buchstabe an Stelle {i}: {s[i]}')
        i += 1
    :::

    Am Ende ist i = 5, und `5 < 5` ist False. Die Schleife endet.

    !! Die Schleife hört NICHT von selbst auf. Im Körper muss sich etwas
    !! ändern (hier `i += 1`), sonst läuft sie unendlich weiter.
    ---
    ## Endlosschleifen

    :::achtung Die Zählvariable vergessen
        i = 0
        while i < 5:
            print(i)        # i wird nie größer!
    Die Bedingung bleibt für immer True: eine **Endlosschleife**. Das
    Programm gibt ohne Ende 0 aus.
    :::

      • Manchmal ist das gewollt, zum Beispiel bei periodischen Aufgaben
        wie einer Ampelsteuerung, die immer laufen soll.
      • Meistens ist es ein Fehler.
      • Mit **Strg + C** brichst du ein Programm im Terminal ab.

    Übrigens: Eine „if-Schleife“ gibt es NICHT. `if` prüft nur EINMAL.
    (In C könnte man mit `goto` so etwas basteln. Bitte nicht!)
    ---
    ## Kontrollfluss am Beispiel Teig

    Schleifen und Verzweigungen lassen sich kombinieren, wie in einem Rezept:

        while falsche_konsistenz(teig):
            if zu_flüssig(teig):
                add(teig, mehl)
            else:
                add(teig, flüssigkeit)

    „Solange der Teig nicht passt: Ist er zu flüssig, Mehl dazu, sonst
    Flüssigkeit dazu.“ Danach wird die Konsistenz neu geprüft.

    :::info Zwei oder vier Leerzeichen?
    Auf der Folie ist der Teig-Code mit 2 Leerzeichen eingerückt. Python
    akzeptiert jede Einrückung, solange sie **einheitlich** ist. Üblich
    sind 4 Leerzeichen, so wie überall in diesem Quiz.
    :::
    """)

k.ausgabe("i = 0\nwhile i < 3:\n    print(i)\n    i += 1",
          "i = 0, 1, 2 werden ausgegeben. Bei i = 3 ist 3 < 3 False → Ende.")
k.ausgabe("i = 0\ns = 'abc'\nwhile i < len(s):\n    print(s[i])\n    i += 1",
          "len('abc') ist 3. Die Schleife läuft mit i = 0, 1, 2 und gibt a, b, c aus.")
k.ausgabe("n = 3\nwhile n > 0:\n    print(n)\n    n -= 1\nprint('Start!')",
          "Countdown: 3, 2, 1, dann ist n = 0 und 0 > 0 ist False → 'Start!'.")
k.ausgabe("summe = 0\ni = 1\nwhile i <= 4:\n    summe += i\n    i += 1\nprint(summe)",
          "summe = 1 + 2 + 3 + 4 = 10. Das print steht NACH der Schleife (nicht eingerückt), "
          "deshalb erscheint nur das Endergebnis.")
k.ausgabe("i = 10\nwhile i < 5:\n    print(i)\n    i += 1\nprint('fertig')",
          "Die Bedingung 10 < 5 ist schon beim ersten Mal False → der Körper wird "
          "GAR NICHT ausgeführt. Nur 'fertig' erscheint.")
k.ausgabe("x = 100\nschritte = 0\nwhile x > 1:\n    x = x // 2\n    schritte += 1\nprint(schritte)",
          "100 → 50 → 25 → 12 → 6 → 3 → 1. Das sind 6 Halbierungen.",
          tipp="Schreibe dir die Werte von x Runde für Runde auf.")
k.mc("Was passiert hier?",
     ["Eine Endlosschleife: Es wird immer wieder 0 ausgegeben",
      "Es werden 0 1 2 3 4 ausgegeben",
      "Ein SyntaxError",
      "Gar nichts"],
     "i wird nie verändert, also bleibt i < 5 für immer True. Abbrechen mit Strg + C.",
     code="i = 0\nwhile i < 5:\n    print(i)")
k.mc("Wie oft wird print('Hallo') ausgeführt?",
     ["3-mal", "2-mal", "4-mal", "Unendlich oft"],
     "i nimmt die Werte 1, 2, 3 an (bei 4 ist 4 <= 3 False). Also 3-mal.",
     code="i = 1\nwhile i <= 3:\n    print('Hallo')\n    i += 1")
k.wf("In Python gibt es eine if-Schleife.", False,
     "Eine if-Schleife gibt es nicht. if prüft nur ein einziges Mal. Zum Wiederholen "
     "braucht man while (oder morgen auch for).")
k.text("Welche Tastenkombination bricht ein laufendes Programm (zum Beispiel eine Endlosschleife) "
       "im Terminal ab?",
       ["Strg+C", "Strg + C", "Ctrl+C", "Ctrl + C", "Strg C", "Ctrl C", "Strg-C", "Ctrl-C"],
       "Mit Strg + C (englisch Ctrl + C) brichst du die Ausführung im Terminal ab.")

# ── Erklärung 2: break / continue ───────────────────────────────────────────
k.erklaerung("break und continue", r"""
    ## Iterationen überspringen oder abbrechen

    Manchmal soll der Körper nicht in JEDER Iteration komplett laufen,
    oder die Schleife soll früher enden. Dafür gibt es zwei Anweisungen:

    | Anweisung | Wirkung | Alltag |
    |---|---|---|
    | `continue` | beendet die AKTUELLE Runde, zurück zum Schleifenkopf | Lied in der Playlist überspringen |
    | `break` | beendet die GANZE Schleife, weiter hinter ihr | Notbremse ziehen |

    !! Beide gelten nur für die INNERSTE Schleife, in der sie stehen.
    ---
    ## continue im Beispiel

    :::trace
    i = 0
    while i < 10:
        if i == 5:
            i += 1
            continue
        print(i)
        i += 1
    print('Ende')
    :::

    Ausgabe: 0 1 2 3 4 6 7 8 9 Ende. Die 5 wird übersprungen.

    :::achtung Die continue-Falle
    Das `i += 1` VOR `continue` ist lebenswichtig. Fehlt es, springt die
    Schleife bei i = 5 zurück zum Kopf, ohne i zu erhöhen. i bleibt für
    immer 5: eine Endlosschleife. Sicherer Trick: die Zählvariable gleich
    am **Anfang** des Körpers erhöhen.
    :::
    ---
    ## break im Beispiel

    :::code
    i = 0
    while i < 10:
        if i == 5:
            break
        print(i)
        i += 1
    print('Ende')
    :::

    Ausgabe: 0 1 2 3 4 Ende. Bei 5 wird die Schleife abgebrochen.
    ---
    ## Nur die innerste Schleife

    Steht eine Schleife in einer anderen, beendet `break` nur die innere.
    Die äußere läuft weiter:

    :::trace
    zeile = 1
    while zeile <= 3:
        spalte = 1
        while spalte <= 3:
            if spalte == 2:
                break
            print(zeile, spalte)
            spalte += 1
        zeile += 1
    print('fertig')
    :::

    Jede innere Schleife bricht bei `spalte == 2` ab. Die äußere Schleife
    macht aber alle drei Runden.
    """)

k.ausgabe("i = 0\nwhile i < 10:\n    if i == 5:\n        i += 1\n        continue\n    print(i)\n    i += 1\nprint('Ende')",
          "continue überspringt bei i == 5 den Rest der Runde (also das print). "
          "Alle anderen Zahlen werden ausgegeben. (Vorlesung 2)",
          tipp="Bei welcher Zahl wird print übersprungen?")
k.ausgabe("i = 0\nwhile i < 10:\n    if i == 5:\n        break\n    print(i)\n    i += 1\nprint('Ende')",
          "break beendet die Schleife bei i == 5 komplett. Danach kommt print('Ende'). (Vorlesung 2)")
k.mc("Was ist der Unterschied zwischen break und continue?",
     ["break beendet die ganze Schleife, continue nur die aktuelle Runde",
      "continue beendet die ganze Schleife, break nur die aktuelle Runde",
      "Beide beenden das ganze Programm",
      "Es gibt keinen Unterschied"],
     "break = Notbremse (Schleife vorbei). continue = „Lied überspringen“ (nächste Runde).")
k.mc("Was passiert, wenn du diesen Code ausführst?",
     ["0 1 2 werden ausgegeben, danach hängt das Programm in einer Endlosschleife",
      "0 1 2 4 werden ausgegeben",
      "0 1 2 3 4 werden ausgegeben",
      "Es gibt einen SyntaxError, weil nach continue noch Code steht"],
     "Bei i == 3 springt continue zurück zum Kopf, OHNE i zu erhöhen (das `i += 1` steht "
     "dahinter und wird übersprungen). i bleibt 3, die Bedingung bleibt True: Endlosschleife. "
     "Lösung: i vor dem continue erhöhen oder gleich am Anfang des Körpers.",
     code="i = 0\nwhile i < 5:\n    if i == 3:\n        continue\n    print(i)\n    i += 1",
     tipp="Was passiert mit i, wenn continue ausgeführt wird?")
k.wf("break beendet bei verschachtelten Schleifen alle Schleifen auf einmal.", False,
     "break und continue wirken nur auf die INNERSTE Schleife.")
k.ausgabe("a = 0\nwhile a < 2:\n    b = 0\n    while b < 5:\n        if b == 2:\n            break\n        b += 1\n"
          "    print(a, b)\n    a += 1",
          "Das break beendet jedes Mal nur die innere Schleife (bei b == 2). Die äußere "
          "Schleife läuft trotzdem zweimal: '0 2' und '1 2'.",
          tipp="break wirkt nur auf die innerste Schleife.")

# ── Erklärung 3: Muster ─────────────────────────────────────────────────────
k.erklaerung("Typische Schleifenmuster", r"""
    ## Muster 1: while True mit break

    Manchmal weiß man erst MITTEN im Körper, ob Schluss ist, zum Beispiel
    beim Einlesen. Dann schreibt man eine absichtliche Endlosschleife und
    steigt mit `break` aus:

    :::code eingaben=3|4|5|0
    summe = 0
    while True:
        zahl = int(input("Zahl (0 = Ende): "))
        if zahl == 0:
            break
        summe += zahl
    print("Summe:", summe)
    :::

    `while True` allein wäre eine Endlosschleife. Erst das `break` macht
    daraus eine sinnvolle Schleife.
    ---
    ## Muster 2: eine Abbruch-Variable

    Aus dem Livecoding: Eine Variable vom Typ `bool` merkt sich, ob Schluss
    ist. Die Schleife läuft, solange sie `False` ist:

    :::trace
    x = 0
    abort = False
    while not abort:
        print(x)
        x = x + 1
        if x % 3 == 2:
            abort = True
    :::

    Bei x = 2 gilt `2 % 3 == 2`, also wird `abort` True. Der Körper läuft
    aber noch zu Ende. Erst beim nächsten Prüfen der Bedingung endet die
    Schleife. Ausgabe: 0 und 1.

    :::info Unterschied zu break
    `break` springt SOFORT aus der Schleife. Eine Abbruch-Variable wirkt
    erst, wenn die Bedingung das nächste Mal geprüft wird.
    :::
    ---
    ## Muster 3: Fragen, bis es passt

    :::code eingaben=hallo|1234|sesam
    passwort = input("Passwort: ")
    while passwort != "sesam":
        print("Falsch!")
        passwort = input("Passwort: ")
    print("Willkommen!")
    :::

    :::achtung input() in der Schleife nicht vergessen
    Fehlt das zweite `input()` im Körper, ändert sich `passwort` nie.
    Bei einer falschen Eingabe gibt das Programm dann endlos „Falsch!“ aus.
    :::
    """)

k.ausgabe("x = 0\nabort = False\nwhile not abort:\n    print(x)\n    x = x + 1\n    if x % 3 == 2:\n        abort = True",
          "Runde 1: print(0), x = 1, 1 % 3 = 1. Runde 2: print(1), x = 2, 2 % 3 = 2 → abort = True. "
          "Danach ist `not abort` False → Ende. Ausgabe: 0 und 1. (Livecoding 2)",
          tipp="Die Abbruch-Variable wird erst beim nächsten Prüfen der Bedingung wirksam.")
k.ausgabe("n = 0\nwhile True:\n    n += 1\n    if n * n > 20:\n        break\nprint(n)",
          "n = 1, 2, 3, 4: 16 ist noch nicht > 20. Bei n = 5 ist 25 > 20 → break. Ausgabe: 5.")
k.mc("Welches Muster passt, wenn ein Programm Zahlen einlesen soll, bis jemand 0 eingibt?",
     ["while True mit einem break, wenn die Eingabe 0 ist",
      "Eine einzige if-Anweisung",
      "while False:",
      "Eine Schleife ganz ohne Bedingung und ohne break"],
     "Erst nach dem Einlesen weiß man, ob Schluss ist. `while True:` und ein `break` bei 0 "
     "sind dafür das typische Muster. (Eine Abbruch-Variable ginge auch.)")
k.wf("Wird in einer while-Schleife die Abbruch-Variable auf True gesetzt, endet die Schleife "
     "sofort, auch mitten im Körper.", False,
     "Nein: Der Körper läuft zu Ende. Erst beim nächsten Prüfen der Bedingung endet die "
     "Schleife. Sofort aussteigen kann man nur mit break.")

# ── Praxisteil ──────────────────────────────────────────────────────────────
k.luecke("Ergänze den Countdown: Er soll 5, 4, 3, 2, 1 ausgeben und danach „Start!“.",
         """
         n = 5
         ___ n > 0:
             print(n)
             n ___ 1
         print("Start!")
         """,
         [["while"], ["-=", "= n -"]],
         "Der Kopf heißt `while n > 0:`. Im Körper muss n kleiner werden (`n -= 1`), sonst "
         "läuft die Schleife ewig.",
         tipp="Welche Kurzschreibweise zieht 1 von n ab?")

k.puzzle("Bringe die Zeilen in die richtige Reihenfolge: Zahlen einlesen, bis 0 kommt, "
         "dann die Summe ausgeben.",
         """
         summe = 0
         while True:
             zahl = int(input())
             if zahl == 0:
                 break
             summe += zahl
         print(summe)
         """,
         "Die Summe startet vor der Schleife bei 0. In der Schleife: einlesen, bei 0 "
         "aussteigen, sonst addieren. Ausgegeben wird erst nach der Schleife.",
         tipp="Erst prüfen, ob die Eingabe 0 ist, dann addieren.",
         ablenker=["    summe = 0", "    continue"])

# Die Tests prüfen mit `exakt` die genaue Reihenfolge der Zeilen. Damit ein Text in
# input("...") die Prüfung nicht stört, ersetzt dieser Vorspann input() durch eine
# Version, die den Aufforderungstext nicht ausgibt (nur für die Tests).
_OHNE_PROMPT = ("import builtins as _quiz_builtins\n"
                "def input(_text=''):\n"
                "    return _quiz_builtins.input()\n")

k.code(r"""
    ## Countdown

    Lies eine ganze Zahl n ein, zum Beispiel mit `n = int(input())`. Gib
    dann mit einer while-Schleife die Zahlen von n abwärts bis 1 aus, jede
    in einer eigenen Zeile, und zum Schluss `Start!`.

        Eingabe: 3        Ausgabe:
                          3
                          2
                          1
                          Start!
    """,
    [P(["3"], exakt=["3", "2", "1", "Start!"], vorspann=_OHNE_PROMPT),
     P(["5"], exakt=["5", "4", "3", "2", "1", "Start!"], vorspann=_OHNE_PROMPT),
     P(["1"], exakt=["1", "Start!"], vorspann=_OHNE_PROMPT),
     P(["0"], exakt=["Start!"], vorspann=_OHNE_PROMPT, beschreibung="Randfall 0: gar nicht zählen")],
    """
    n = int(input())
    while n > 0:
        print(n)
        n -= 1
    print("Start!")
    """,
    "Die Schleife läuft, solange n > 0 ist, und verkleinert n in jeder Runde. Bei n = 0 "
    "läuft sie gar nicht, und es kommt sofort „Start!“.",
    pflicht=["while"],
    tipps=["Die Schleife soll laufen, solange n größer als 0 ist.",
           "while n > 0: … und im Körper n verkleinern (n -= 1).",
           "Das print(\"Start!\") steht NACH der Schleife, also nicht eingerückt."],
    vorlage="n = int(input())\nwhile ...:\n    ...\n")

k.code(r"""
    ## Ohne Dreierzahlen

    Lies eine ganze Zahl n ein. Gib die Zahlen von 1 bis n aus, je eine
    pro Zeile, **überspringe** aber alle Vielfachen von 3. Benutze dafür
    `continue`.

        Eingabe: 7      Ausgabe: 1 2 4 5 7 (je eine Zeile)
    """,
    [P(["7"], exakt=["1", "2", "4", "5", "7"], vorspann=_OHNE_PROMPT),
     P(["2"], exakt=["1", "2"], vorspann=_OHNE_PROMPT),
     P(["3"], exakt=["1", "2"], vorspann=_OHNE_PROMPT, beschreibung="n selbst ist ein Vielfaches von 3"),
     P(["10"], exakt=["1", "2", "4", "5", "7", "8", "10"], vorspann=_OHNE_PROMPT),
     P(["0"], exakt=[], vorspann=_OHNE_PROMPT, beschreibung="Randfall 0: keine Ausgabe")],
    """
    n = int(input())
    i = 0
    while i < n:
        i += 1
        if i % 3 == 0:
            continue
        print(i)
    """,
    "Der Trick: `i += 1` steht am ANFANG des Körpers. So wird i auch dann erhöht, wenn "
    "continue den Rest der Runde überspringt. Stünde es am Ende, gäbe es bei i = 3 eine "
    "Endlosschleife.",
    pflicht=["while", "continue"],
    tipps=["Ein Vielfaches von 3 erkennst du an `i % 3 == 0`.",
           "Erhöhe i gleich am Anfang des Körpers, dann kann continue keine Endlosschleife erzeugen.",
           "i = 0; while i < n: i += 1; if i % 3 == 0: continue; print(i)"])

k.code(r"""
    ## Passwort-Abfrage

    Schreibe ein Programm, das so lange nach einem Passwort fragt, bis
    `sesam` eingegeben wird.
      • Bei jedem falschen Passwort soll `Falsch!` ausgegeben werden.
      • Bei richtigem Passwort soll `Willkommen!` ausgegeben werden.
    """,
    [P(["hallo", "1234", "sesam"], ["Falsch!", "Willkommen!"]),
     P(["hallo", "1234", "sesam"], anzahl={"Falsch!": 2},
       beschreibung="zwei falsche Versuche → genau zweimal Falsch!"),
     P(["sesam"], ["Willkommen!"], nicht=["falsch"], beschreibung="gleich beim ersten Mal richtig"),
     P(["Sesam", "geheim", "x", "sesam"], ["Willkommen!"], anzahl={"Falsch!": 3},
       beschreibung="Groß/klein zählt: Sesam ist falsch")],
    """
    passwort = input("Passwort: ")
    while passwort != "sesam":
        print("Falsch!")
        passwort = input("Passwort: ")
    print("Willkommen!")
    """,
    "Die Schleife läuft, SOLANGE das Passwort falsch ist. Wichtig: In der Schleife "
    "muss neu gefragt werden, sonst Endlosschleife! (Mit `while True` und `break` geht "
    "es auch.)",
    tipps=["Wiederhole, solange das Passwort NICHT \"sesam\" ist.",
           "Einmal vor der Schleife fragen, dann: while passwort != \"sesam\": …",
           "Im Körper: print(\"Falsch!\") und erneut passwort = input(…)."],
    streng=True)

k.code(r"""
    ## Collatz-Schritte (Knobelaufgabe)

    Lies eine positive ganze Zahl n ein. Wiederhole, solange n nicht 1 ist:
      • ist n gerade, wird n halbiert (`n // 2`),
      • ist n ungerade, wird n zu `3 * n + 1`.

    Zähle die Schritte, bis n bei 1 ankommt, und gib die Anzahl aus.

        6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1    Ausgabe: 8
    """,
    [P(["6"], ["8"]),
     P(["1"], ["0"], beschreibung="Randfall: schon bei 1"),
     P(["16"], ["4"]),
     P(["7"], ["16"]),
     P(["3"], ["7"])],
    """
    n = int(input())
    schritte = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        schritte += 1
    print(schritte)
    """,
    "Eine while-Schleife mit if/else im Körper. Der Zähler `schritte` startet bei 0 und "
    "wächst in jeder Runde um 1. Bei n = 1 läuft die Schleife gar nicht. Ob das für jede "
    "Startzahl irgendwann bei 1 endet, ist übrigens ein ungelöstes Problem der Mathematik!",
    tipps=["Du brauchst einen Zähler, der vor der Schleife bei 0 startet.",
           "while n != 1: und darin mit `n % 2 == 0` entscheiden, was passiert.",
           "Nach dem if/else im Körper: schritte += 1. Nach der Schleife print(schritte)."])

k.zusammenfassung(r"""
    ## while auf einen Blick

        i = 0                 # 1. Startwert
        while i < 5:          # 2. Bedingung, vor JEDER Runde geprüft
            print(i)
            i += 1            # 3. Veränderung, sonst Endlosschleife!

    | Anweisung | Wirkung |
    |---|---|
    | `continue` | Rest der Runde überspringen, zurück zum Kopf |
    | `break` | Schleife sofort verlassen |
    | `while True:` + `break` | Ausstieg mitten im Körper |
    | `while not abort:` | Abbruch-Variable, wirkt beim nächsten Prüfen |

    !! break und continue gelten nur für die innerste Schleife.
    !! Vor continue die Zählvariable erhöhen. Endlosschleife abbrechen: Strg + C.
    """)
