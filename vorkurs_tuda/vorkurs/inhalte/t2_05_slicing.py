# -*- coding: utf-8 -*-
"""Kapitel: Slicing & mehr über Strings (Vorlesung 2, Folien 47–48; Livecoding 2.6)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="slicing",
    titel="Slicing & mehr über Strings",
    beschreibung="Teile von Listen und Texten ausschneiden, split(), replace(), Palindrome",
    quelle="Vorlesung 2, Livecoding 2",
    teil="tag2",
    icon="✂️")

k.lernziele([
    "Ich kann mit [start:end:step] Teile von Listen und Strings ausschneiden",
    "Ich kenne die Standardwerte für weggelassene Teile, auch bei negativer Schrittweite",
    "Ich kann Strings mit Index, Slicing, split() und replace() bearbeiten",
    "Ich weiß, dass Strings unveränderlich sind, und baue stattdessen neue Strings",
])

# ── Erklärung 1: Grundlagen ─────────────────────────────────────────────────
k.erklaerung("Slicing – Scheiben abschneiden", r"""
    ## Slices sind Teile einer Liste (oder eines Strings)

    Ein **Slice** (englisch „Scheibe“) ist ein Ausschnitt einer Liste.
    Die allgemeine Schreibweise:

        lst[start:end:step]

    | Teil | Bedeutung | Verhalten |
    |---|---|---|
    | `start` | erster Index des Ausschnitts | wird MITGENOMMEN (inklusiv) |
    | `end` | Index NACH dem Ende | wird NICHT mitgenommen (exklusiv) |
    | `step` | Schrittweite und Richtung | 2 = jedes zweite, -1 = rückwärts |

    :::analogie 🍞 Brot schneiden
    Die Liste ist ein Brot, jede Scheibe hat eine Nummer (den Index).
      • `start` ist die erste Scheibe, die du nimmst.
      • `end` ist ein **Zaun**: Du schneidest bis VOR den Zaun. Die
        Scheibe am Zaun bleibt liegen.
      • `step` sagt, ob du jede Scheibe nimmst (1), jede zweite (2) oder
        vom anderen Ende her schneidest (negativ).
      • Das Brot selbst bleibt ganz: Ein Slice ist eine NEUE Liste, die
        alte Liste ändert sich nicht.
    :::
    ---
    ## Ausprobieren

    Verschiebe die Regler für start, end und step und beobachte, welche
    Fächer ausgewählt werden:

    :::visual liste
    {"name": "lst", "werte": [8, 1, 3, -4, 5, 0, 2, 11], "slice": "1:3",
     "interaktiv": true, "negativ": true}
    :::

    :::code
    lst = [3, 4, 1, 2]
    print(lst[1:3])     # Index 1 und 2, NICHT 3 → [4, 1]
    print(lst[1:3:2])   # Index 1, dann wäre 3 schon am Zaun → [4]
    print(lst)          # unverändert
    :::

    :::achtung end ist exklusiv
    `lst[1:3]` liefert nur ZWEI Elemente (Index 1 und 2). Die Anzahl ist
    `end - start` (bei step 1). Wer Index 3 dabeihaben will, schreibt `lst[1:4]`.
    :::
    """)

k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst[1:3])",
          "Von Index 1 (inklusive) bis 3 (exklusive): Index 1 und 2 → [4, 1].",
          tipp="Der end-Index wird NICHT mitgenommen.")
k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst[1:3:2])",
          "Start bei 1 (Wert 4), nächster wäre 1 + 2 = 3, aber 3 ist schon das Ende → [4].")
k.mc("Was bedeuten die drei Teile in lst[a:b:c]?",
     ["a = Start (inklusiv), b = Ende (exklusiv), c = Schrittweite",
      "a = Start (exklusiv), b = Ende (inklusiv), c = Anzahl",
      "a = Länge, b = Start, c = Ende",
      "a = Schrittweite, b = Start, c = Ende"],
     "start ist dabei, end nicht, step ist die Schrittweite (und Richtung).")
k.wf("Nach   teil = lst[1:3]   ist die Liste lst kürzer geworden.", False,
     "Slicing erzeugt eine NEUE Liste. Die ursprüngliche Liste bleibt unverändert.")

# ── Erklärung 2: Standardwerte ──────────────────────────────────────────────
k.erklaerung("Was gilt, wenn man etwas weglässt?", r"""
    ## Standardwerte

    Jeder der drei Teile darf leer bleiben. Dann setzt Python einen
    **Standardwert** ein. Der hängt von der Richtung ab:

    | weggelassen | bei positivem step | bei negativem step |
    |---|---|---|
    | `step` | 1 | (gibt es nicht, step ist ja angegeben) |
    | `start` | 0 (ganz vorne) | letztes Element (ganz hinten) |
    | `end` | `len(lst)` (bis ganz zum Ende) | „vor den Anfang“ (Index 0 ist noch dabei) |

    Für „vor den Anfang“ gibt es keine Zahl, die du hinschreiben könntest:
    `-1` wäre das LETZTE Element. Deshalb lässt man end einfach leer.

    :::code
    lst = [8, 1, 3, -4, 5, 0, 2, 11]
    print(lst[:])       # ganze Liste
    print(lst[:3])      # die ersten 3
    print(lst[5:])      # ab Index 5
    print(lst[::2])     # jedes zweite
    print(lst[::-1])    # rückwärts
    print(lst[-3:])     # die letzten 3
    print(lst[6:2:-1])  # Index 6, 5, 4, 3
    print(lst[3::-1])   # von Index 3 rückwärts bis zum Anfang
    :::
    ---
    ## Rückwärts schneiden

    Bei negativem step läuft der Slice von rechts nach links. Dann muss
    start RECHTS von end liegen. Beispiel aus dem Livecoding:

    :::code
    a = [1, 2, 3, 4, 5]
    print(a[3:1:-1])        # Index 3, 2 → [4, 3]
    print("12345"[3:1:-1])  # dasselbe bei Strings → '43'
    print(a[1:3:-1])        # start links von end → []
    :::

    :::achtung Leere Liste statt Fehler
    `a[1:3:-1]` gibt keinen Fehler, sondern einfach `[]`: Von Index 1
    kommt man rückwärts nie zu Index 3. Prüfe bei negativem step immer,
    ob start größer als end ist.
    :::

    :::info step darf nicht 0 sein
    `lst[::0]` ergibt `ValueError: slice step cannot be zero`. Mit
    Schrittweite 0 käme man nie voran.
    :::
    """)

k.mc("Welche Werte gelten, wenn man bei lst[::] alles leer lässt (positive Schrittweite)?",
     ["start = 0, end = len(lst), step = 1",
      "start = 1, end = len(lst), step = 0",
      "start = 0, end = -1, step = 1",
      "Es gibt einen SyntaxError"],
     "Leer heißt: ganz vom Anfang (0) bis ganz zum Ende (len(lst)) in Einerschritten.")
k.mc("Was setzt Python für start und end ein, wenn du   lst[::-1]   schreibst?",
     ["start = letztes Element, end = vor dem Anfang (Index 0 ist noch dabei)",
      "start = 0, end = len(lst)",
      "start = -1, end = 0 (Index 0 ist nicht dabei)",
      "start = 0, end = -1"],
     "Bei negativer Schrittweite beginnt der Slice hinten und läuft bis VOR den Anfang. "
     "Darum ist auch das Element an Index 0 dabei. `lst[-1:0:-1]` würde Index 0 dagegen "
     "auslassen.")
k.ausgabe("a = [1, 2, 3, 4, 5]\nprint(a[3:1:-1])",
          "Start bei Index 3 (Wert 4), rückwärts: Index 2 (Wert 3). Index 1 ist der Zaun "
          "und nicht mehr dabei → [4, 3]. (Livecoding 2)",
          tipp="Bei step -1 läuft man nach links. end bleibt exklusiv.")
k.ausgabe('print("12345"[3:1:-1])',
          "Strings funktionieren genauso: Index 3 ('4') und Index 2 ('3') → 43.")
k.ausgabe("lst = [8, 1, 3, -4, 5, 0, 2, 11]\nprint(lst[-3:])",
          "Start bei -3 (Wert 0), end leer = bis zum Ende → [0, 2, 11].")
k.ausgabe("a = [1, 2, 3, 4, 5]\nprint(a[1:3:-1])",
          "Rückwärts von Index 1 kommt man nie zu Index 3 → leere Liste [], kein Fehler.")
k.ausgabe("s = [1, 3, 6, 8, 1, 2]\nprint(s[3:0:-2])",
          "Start bei Index 3 (Wert 8), rückwärts in 2er-Schritten: Index 1 (Wert 3). "
          "Index -1 läge schon hinter dem Zaun 0 → [8, 3].",
          tipp="Start bei Index 3, Schrittweite -2, Index 0 ist exklusiv.")
k.ausdruck("Gegeben ist lst. Schreibe einen Slicing-Ausdruck für die LETZTEN DREI Elemente.",
           [{"lst": [3, 4, 1, 2, 9, 7]}, {"lst": [10, 20, 30, 40]}, {"lst": [5, 6, 7]}],
           "lst[-3:]",
           "Negativer Start zählt von hinten: -3 ist das drittletzte Element. end leer = bis "
           "zum Ende. So klappt es für jede Länge.",
           tipp="Ein negativer start zählt von hinten.", muss_enthalten=":")
k.ausdruck("Schreibe einen Slicing-Ausdruck für alle Elemente von lst AUSSER dem ersten und dem letzten.",
           [{"lst": [3, 4, 1, 2, 9, 7]}, {"lst": [10, 20, 30, 40]}, {"lst": [1, 2]}],
           "lst[1:-1]",
           "start 1 lässt das erste Element weg, end -1 ist exklusiv und lässt das letzte weg.",
           tipp="end darf auch negativ sein.", muss_enthalten=":")
k.ausdruck("Schreibe einen Slicing-Ausdruck, der die Elemente an Index 3, 2 und 1 von lst liefert "
           "(genau in dieser Reihenfolge).",
           [{"lst": [3, 4, 1, 2, 9, 7]}, {"lst": [10, 20, 30, 40, 50]}],
           "lst[3:0:-1]",
           "Rückwärts heißt step -1. Start bei 3, und end 0 ist exklusiv, also hört der Slice "
           "bei Index 1 auf.",
           tipp="Rückwärts: step = -1. Wo steht der Zaun, damit Index 1 noch dabei ist?",
           muss_enthalten=":")

# ── Erklärung 3: Strings ────────────────────────────────────────────────────
k.erklaerung("Strings wie Listen", r"""
    ## Strings verhalten sich (fast) wie Listen

    Eine **Zeichenkette** (String) ist eine Folge einzelner Zeichen. Vieles
    funktioniert deshalb genau wie bei Listen:

    | Was | String | Liste |
    |---|---|---|
    | Zugriff | `s[1]` | `lst[1]` |
    | Länge | `len(s)` | `len(lst)` |
    | Verketten | `s1 + s2` | `lst1 + lst2` |
    | Slices | `s[1:3]` | `lst[1:3]` |

    :::visual string
    {"text": "Lorem ipsum!", "slice": "0:5", "interaktiv": true}
    :::

        "Lorem ipsum!"[:5]     # 'Lorem'
        "Hallo"[::-1]          # 'ollaH'
        "Hallo"[-1]            # 'o'
    ---
    ## Strings sind unveränderlich

    :::achtung s[0] = "B" geht nicht
    Anders als Listen sind Strings **unveränderlich**. `s[0] = "B"` gibt
    einen `TypeError`. Auch `.pop()`, `.sort()` oder `.append()` gibt es
    für Strings nicht. Stattdessen baust du einen NEUEN String:

        s = "Hallo"
        s = "B" + s[1:]     # 'Ballo'
    :::
    ---
    ## Nützliche String-Funktionen

    `.split('trenner')` teilt einen String an einem **Trennstring** in eine
    LISTE von Strings auf:

    :::code
    print("Anna,19,Informatik".split(","))
    print("Hallo schöne Welt".split(" "))
    woerter = "Ich lerne Python".split(" ")
    print(len(woerter), woerter[0], woerter[-1])
    :::

    `.replace(alt, neu)` ersetzt Teile eines Strings. Mit `''` als neu
    werden sie gelöscht:

    :::code
    print('lorem'.replace('ore', 'i'))
    print('H-a-l-l-o'.replace('-', ''))
    :::
    ---
    ## Palindrome erkennen

    Ein **Palindrom** ist ein Wort, das vorwärts und rückwärts gleich ist:
    Otto, Anna, Rentner, Lagerregal. Mit Slicing ist der Test ein Einzeiler:

        wort == wort[::-1]

    :::achtung Lagerregal ist mit großem L KEIN Palindrom für Python
    `"Lagerregal"[::-1]` ergibt `"lagerregaL"`. Das große L steht jetzt
    am Ende, und für Python sind `L` und `l` verschiedene Zeichen. Der
    Vergleich liefert `False`. Erst wenn du vorher mit `.lower()` alles
    klein machst, klappt es:

        wort.lower() == wort.lower()[::-1]    # True für "Lagerregal"
    :::
    """)

k.ausgabe('print("Lorem ipsum!"[:5])', "Die ersten 5 Zeichen (Index 0 bis 4): Lorem")
k.ausgabe('print("Hallo"[::-1])', "Schrittweite -1 dreht den String um.")
k.ausgabe('print("Hallo Welt"[6:])', "Ab Index 6 bis zum Ende: Welt")
k.ausgabe('print("Anna,19,Informatik".split(","))',
          "split(',') teilt am Komma und liefert eine Liste von Strings.")
k.ausgabe("print('lorem'.replace('ore', 'i'))",
          "Der Teil 'ore' wird durch 'i' ersetzt: l + i + m = lim. (Vorlesung 2)")
k.ausgabe('wort = "Lagerregal"\nprint(wort == wort[::-1])',
          "Rückwärts ist es 'lagerregaL': Das große L steht jetzt am Ende. Groß und klein "
          "sind verschieden → False!",
          tipp="Achte auf den ersten Buchstaben.")
k.ausgabe('wort = "Lagerregal"\nprint(wort.lower() == wort.lower()[::-1])',
          "Erst alles klein machen ('lagerregal'), dann vergleichen → True.")
k.ausgabe('s = "Hallo"\ns[0] = "B"',
          "Strings kann man nicht verändern → TypeError. Stattdessen einen neuen String "
          "bauen: s = 'B' + s[1:]")
k.ausgabe('s = "Hallo"\ns = "B" + s[1:]\nprint(s)',
          "s[1:] ist 'allo'. Zusammen mit 'B' ergibt sich ein NEUER String: Ballo.")
k.wf("Strings haben die Funktionen .sort() und .pop() genau wie Listen.", False,
     "Strings sind unveränderlich, solche Funktionen gibt es für sie nicht. Dafür gibt es "
     ".split() und .replace().")
k.ausdruck("Eine Zeile aus einer CSV-Datei liegt in der Variable zeile. Schreibe einen Ausdruck, "
           "der nur den Studiengang (das letzte Feld) liefert.",
           [{"zeile": "Anna,19,Informatik"}, {"zeile": "Ben,21,Maschinenbau"}],
           "zeile.split(',')[-1]",
           "split(',') macht daraus eine Liste, [-1] nimmt das letzte Element. "
           "zeile.split(',')[2] geht auch.",
           tipp="Erst mit split(',') zerlegen, dann das letzte Element nehmen.")

# ── Praxisteil ──────────────────────────────────────────────────────────────
k.luecke("Ergänze die Slices: erst die ersten drei Buchstaben, dann das Wort rückwärts.",
         """
         wort = "Python"
         print(wort[___])     # Pyt
         print(wort[___])     # nohtyP
         """,
         [[":3", "0:3"], ["::-1", "-1::-1"]],
         "`[:3]` nimmt Index 0, 1, 2. `[::-1]` läuft mit Schrittweite -1 vom Ende zum Anfang.",
         tipp="end ist exklusiv, und rückwärts heißt step -1.")

k.code(r"""
    ## Wort rückwärts

    Lies ein Wort ein und gib es rückwärts aus. Benutze Slicing.

        Eingabe: Hallo      Ausgabe: ollaH
    """,
    [P(["Hallo"], ["ollaH"]),
     P(["Lagerregal"], ["lagerregaL"], beschreibung="Groß/klein bleibt erhalten"),
     P(["a"], ["a"], beschreibung="nur ein Zeichen"),
     P(["ab cd"], ["dc ba"], beschreibung="mit Leerzeichen")],
    """
    wort = input("Wort: ")
    print(wort[::-1])
    """,
    "`[::-1]` liefert alle Zeichen mit Schrittweite -1, also von hinten nach vorne.",
    pflicht=[":"],
    tipps=["Ein Slice kann auch rückwärts laufen.",
           "Die Schrittweite -1 dreht die Richtung um.",
           "print(wort[::-1])"],
    streng=True)

# Die Aufgabe ist streng (streng=True): Groß/klein und Punkte der Initialen zählen.
def _initialen_test(vor, nach, soll):
    return P([vor, nach], [soll], beschreibung=f"Ausgabe {soll} (groß geschrieben)")


k.code(r"""
    ## Initialen

    Lies zuerst einen Vornamen und dann einen Nachnamen ein. Gib die
    Initialen als Großbuchstaben mit Punkt aus.

        Eingaben: ada, lovelace      Ausgabe: A.L.
    """,
    [_initialen_test("ada", "lovelace", "A.L."),
     _initialen_test("Alan", "Turing", "A.T."),
     _initialen_test("grace", "Hopper", "G.H."),
     _initialen_test("Kim", "lee", "K.L.")],
    """
    vorname = input("Vorname: ")
    nachname = input("Nachname: ")
    print(vorname[0].upper() + "." + nachname[0].upper() + ".")
    """,
    "`vorname[0]` (oder `vorname[:1]`) ist der erste Buchstabe, `.upper()` macht ihn groß. "
    "Mit `+` werden die Teile zu einem neuen String verbunden.",
    tipps=["Den ersten Buchstaben bekommst du mit Index 0.",
           "Großbuchstaben macht .upper().",
           "print(vorname[0].upper() + \".\" + nachname[0].upper() + \".\")"],
    streng=True)

k.code(r"""
    ## Wörter zählen

    Lies einen Satz ein (Wörter durch je ein Leerzeichen getrennt). Gib in
    drei Zeilen aus: die Anzahl der Wörter, das erste Wort und das letzte Wort.

        Eingabe: Ich lerne Python
        Ausgabe: 3
                 Ich
                 Python
    """,
    [P(["Ich lerne Python"], ["3", "Ich", "Python"]),
     P(["Hallo"], ["1", "Hallo"], beschreibung="nur ein Wort"),
     P(["a b c d e"], ["5", "a", "e"]),
     P(["Heute ist ein guter Tag"], ["5", "Heute", "Tag"])],
    """
    satz = input("Satz: ")
    woerter = satz.split(" ")
    print(len(woerter))
    print(woerter[0])
    print(woerter[-1])
    """,
    "`split(\" \")` zerlegt den Satz in eine Liste von Wörtern. Danach ist alles wie bei "
    "Listen: len(), Index 0 und Index -1.",
    tipps=["Mit .split(\" \") wird aus dem Satz eine Liste.",
           "Die Anzahl ist die Länge dieser Liste.",
           "woerter[0] ist das erste, woerter[-1] das letzte Wort."],
    streng=True)

k.code(r"""
    ## Satz-Palindrom (Knobelaufgabe)

    Lies einen Satz ein. Gib `Palindrom` aus, wenn er vorwärts und
    rückwärts gleich ist, sonst `Kein Palindrom`. Dabei sollen
    **Leerzeichen** und **Groß-/Kleinschreibung** keine Rolle spielen.

        Ein Esel lese nie   →   Palindrom
        Hallo Welt          →   Kein Palindrom
    """,
    [P(["Ein Esel lese nie"], ["Palindrom"], nicht=["kein"]),
     P(["Otto"], ["Palindrom"], nicht=["kein"]),
     P(["Hallo Welt"], ["Kein Palindrom"]),
     P(["Die Liebe ist Sieger rege ist sie bei Leid"], ["Palindrom"], nicht=["kein"]),
     P(["Rentner ab"], ["Kein Palindrom"])],
    """
    satz = input("Satz: ")
    s = satz.lower().replace(" ", "")
    if s == s[::-1]:
        print("Palindrom")
    else:
        print("Kein Palindrom")
    """,
    "Zuerst alles klein machen (`.lower()`) und die Leerzeichen löschen "
    "(`.replace(\" \", \"\")`). Dann der bekannte Vergleich mit `[::-1]`.",
    tipps=["Bereite den Satz erst auf: alles klein und ohne Leerzeichen.",
           "s = satz.lower().replace(\" \", \"\")",
           "if s == s[::-1]: print(\"Palindrom\") else: print(\"Kein Palindrom\")"],
    streng=True)

k.zusammenfassung(r"""
    ## Slicing auf einen Blick

        lst = [8, 1, 3, -4, 5, 0, 2, 11]
        lst[1:3]     # [1, 3]       start inklusiv, end exklusiv
        lst[:3]      # [8, 1, 3]    die ersten 3
        lst[-3:]     # [0, 2, 11]   die letzten 3
        lst[::2]     # [8, 3, 5, 2] jedes zweite
        lst[::-1]    # rückwärts
        lst[6:2:-1]  # [2, 0, 5, -4]

    | weggelassen | step > 0 | step < 0 |
    |---|---|---|
    | start | 0 | letztes Element |
    | end | bis zum Ende (`len`) | bis vor den Anfang |
    | step | 1 | – |

    Strings: `s[i]`, `s[a:b]`, `len(s)`, `s.split(",")` (→ Liste),
    `s.replace("a", "b")`, `s.lower()`.

    !! Strings sind unveränderlich. Palindrom-Test: `w.lower() == w.lower()[::-1]`.
    """)
