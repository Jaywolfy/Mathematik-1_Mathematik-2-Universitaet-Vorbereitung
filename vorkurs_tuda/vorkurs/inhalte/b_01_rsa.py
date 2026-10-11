# -*- coding: utf-8 -*-
"""Kapitel: Bonus: RSA-Verschlüsselung (Übung 1, Aufgabe 6 und Übung 4, Aufgabe 3)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="rsa",
    titel="Bonus: RSA-Verschlüsselung",
    beschreibung="Geheime Nachrichten mit Modulo und Potenzen (Übung 1, Aufgabe 6 und Übung 4, Aufgabe 3)",
    quelle="Übung 1, Übung 4",
    teil="bonus",
    icon="🔐")

k.lernziele([
    "Ich kann erklären, was öffentlicher und privater Schlüssel bei RSA sind",
    "Ich kann n = p · q und N = (p − 1)(q − 1) sicher auseinanderhalten",
    "Ich kann Zahlen mit m ** e % n bzw. pow(m, e, n) ver- und entschlüsseln",
    "Ich kann zu e ein passendes d mit e · d mod N = 1 suchen",
])

k.erklaerung("RSA – Verschlüsseln mit Mathe", r"""
    ## Die Idee (keine Panik – das ist ein Exkurs!)

    RSA ist ein echtes Verschlüsselungsverfahren, das z. B. im Internet
    benutzt wird. Übung 1 sagt selbst: Etwas Verwirrung ist hier völlig in
    Ordnung.

    :::analogie 📬 Der Briefkasten
    Kim hat einen Briefkasten mit Schlitz. **Jeder** kann einen Brief
    einwerfen, dafür braucht man keinen Schlüssel. Das ist der
    **öffentliche Schlüssel** (e, n): Kim darf ihn allen verraten.
    Herausholen kann die Briefe aber nur, wer den Briefkastenschlüssel hat.
    Das ist der **private Schlüssel** (d, n), den nur Kim kennt. Ben wirft
    eine verschlüsselte Nachricht ein, und selbst Ben kann sie danach nicht
    mehr lesen – nur Kim.
    :::

    :::visual ablauf
    {"schritte": [{"icon": "✉️", "text": "Nachricht m (eine Zahl, 0 ≤ m < n)"},
                  {"icon": "🔒", "text": "Verschlüsseln mit (e, n): c = m^e mod n"},
                  {"icon": "📨", "text": "Geheimtext c wird verschickt"},
                  {"icon": "🔑", "text": "Entschlüsseln mit (d, n): m = c^d mod n"}]}
    :::

    Man braucht zwei Primzahlen p und q. Ihr Produkt n = p · q legt fest:
    Nach jeder Rechnung wird das Ergebnis mit „mod n“ in den Bereich
    0 bis n − 1 gebracht (in Python: `% n`).
    ---
    ## Die Zahlen aus Übung 1

    | Zeichen | Bedeutung | Wert |
    |---|---|---|
    | p, q | zwei Primzahlen | 3 und 11 |
    | n | Modul: n = p · q | 33 |
    | N | N = φ(n) = (p − 1) · (q − 1) | 2 · 10 = 20 |
    | e | 0 < e < N, ggT(e, N) = 1 | 3 |
    | d | 0 < d < N, e · d mod N = 1 | 7, denn 3 · 7 = 21 und 21 mod 20 = 1 |

    (Übung 4 verlangt für e genauer 1 < e < N. Mit e = 1 bliebe jede
    Nachricht unverändert, das wäre keine Verschlüsselung.)

    Verschlüsseln einer Nachricht m (eine Zahl mit 0 ≤ m < n):

        c = m ** e % n          →   c = m ** 3 % 33

    Entschlüsseln eines Geheimtextes c:

        m = c ** d % n          →   m = c ** 7 % 33

    :::code
    n, e, d = 33, 3, 7
    m = 4
    c = m ** e % n
    print("verschlüsselt:", c)
    print("entschlüsselt:", c ** d % n)
    :::

    Python-Tipp: `pow(m, e, n)` rechnet `m ** e % n` besonders effizient.
    """)

k.ausgabe("print((3 - 1) * (11 - 1))", "N = (p-1)·(q-1) = 2 · 10 = 20.")
k.ausgabe("print(3 * 7 % 20)", "e · d mod N = 21 mod 20 = 1 – genau das muss für d gelten.")
k.ausgabe("print(4 ** 3 % 33)", "Verschlüsseln: 4³ = 64, 64 % 33 = 31.")
k.ausgabe("print(31 ** 7 % 33)", "Entschlüsseln: 31⁷ mod 33 ergibt wieder die ursprüngliche Nachricht 4!")
k.ausgabe("print(pow(4, 3, 33))", "`pow(m, e, n)` ist dasselbe wie `m ** e % n`: 31.")

k.mc("Warum muss die Nachricht m die Bedingung 0 <= m < n erfüllen?",
     ["Weil alle Ergebnisse mod n im Bereich 0 bis n-1 liegen – größere Zahlen gingen verloren",
      "Weil Python keine großen Zahlen kann",
      "Weil m eine Primzahl sein muss",
      "Das muss sie gar nicht"],
     "Nach dem Entschlüsseln kommt immer eine Zahl zwischen 0 und n-1 heraus. Eine "
     "größere Nachricht könnte man also nie zurückbekommen.")

k.mc("Welcher Schlüssel darf veröffentlicht werden?",
     ["(e, n) – der öffentliche Schlüssel zum Verschlüsseln",
      "(d, n) – der private Schlüssel",
      "p und q",
      "N = (p − 1)(q − 1)"],
     "Mit (e, n) kann jeder verschlüsseln, aber nicht entschlüsseln. d, p, q und N müssen "
     "geheim bleiben: Wer p und q kennt, kann N und damit d ausrechnen.")

k.erklaerung("n und N nicht verwechseln – Schlüssel selbst berechnen", r"""
    ## Zwei Zahlen, fast gleicher Name

    :::info Groß-N und klein-n (Übung 1 und Übung 4)
    In Übung 1 heißt **n = p · q** der Modul und **N = φ(n) = (p − 1)(q − 1)**.
    φ (gesprochen „fi“) ist die eulersche Phi-Funktion. Auf Übungsblatt 4,
    Aufgabe 3.2.1, steht „φ(N) = (p − 1)(q − 1)“. Gemeint ist **φ(n)**, also
    genau das N aus Übung 1. Mit dieser Bedeutung sind „ggT(e, N) = 1“ und
    „e · d mod N = 1“ auf dem Blatt richtig.

    • **N** = (p − 1)(q − 1) brauchst du, um **e und d zu finden**.
    • **n** = p · q brauchst du zum **Ver- und Entschlüsseln** und es steht
      in beiden Schlüsseln: (e, n) und (d, n).
    :::

    Was passiert, wenn man beides verwechselt und e und d mit n = 33 statt
    mit N = 20 sucht? Dann käme e = 2 und d = 17 heraus:

    :::code
    n = 33
    e, d = 2, 17          # passt zu 33, aber NICHT zu N = 20
    falsch = 0
    for m in range(n):
        if pow(pow(m, e, n), d, n) != m:
            falsch += 1
    print(falsch, "von", n, "Nachrichten kommen falsch zurück")
    :::
    ---
    ## e und d finden

    So findest du die Schlüssel (das ist Übung 4, Aufgabe 3.2.1):

    1. **e**: Probiere e = 2, 3, 4, … bis ggT(e, N) = 1 ist. Den ggT
       berechnest du rekursiv (Übung 4, Aufgabe 3.1).
    2. **d**: Probiere d = 1, 2, 3, … bis e · d % N == 1 ist.

    :::trace
    N = 20
    e = 3
    d = 1
    while e * d % N != 1:
        d += 1
    print("d =", d)
    :::

    :::achtung Typischer Fehler: zu große Zahlen mit **
    `c ** d % n` rechnet erst die riesige Zahl c ** d aus und teilt dann.
    Bei echten Schlüsseln mit hunderten Stellen dauert das ewig.
    `pow(c, d, n)` rechnet nach jedem Schritt mod n und bleibt schnell.
    :::
    """)

k.mc("Mit welcher Zahl sucht man e und d?",
     ["Mit N = (p − 1)(q − 1)",
      "Mit n = p · q",
      "Mit p + q",
      "Mit der Nachricht m"],
     "e muss teilerfremd zu N sein und e · d mod N = 1 erfüllen. n = p · q braucht man erst "
     "beim Ver- und Entschlüsseln.")

k.wf("Für p = 3 und q = 11 ist N = 33.", False,
     "33 ist n = p · q. N ist (3 − 1) · (11 − 1) = 20. Die beiden zu verwechseln führt zu "
     "falschen Schlüsseln.")

k.ausgabe("N = 20\ne = 3\nd = 1\nwhile e * d % N != 1:\n    d += 1\nprint(d)",
          "3 · 1 = 3, 3 · 2 = 6, … 3 · 7 = 21, und 21 % 20 = 1. Also d = 7 – genau der Wert aus "
          "Übung 1.",
          tipp="Gesucht ist das erste d, bei dem 3 · d geteilt durch 20 den Rest 1 lässt.")

# ── Praxisteil ───────────────────────────────────────────────────────────
k.luecke("Ergänze die effiziente Verschlüsselung c = m^e mod n mit der eingebauten Funktion "
         "pow.",
         """
         m, e, n = 4, 3, 33
         c = ___(m, e, ___)
         print(c)
         """,
         [["pow"], ["n"]],
         "`pow(m, e, n)` rechnet `m ** e % n`, nimmt aber nach jedem Zwischenschritt mod n und "
         "bleibt dadurch auch bei riesigen Zahlen schnell.",
         tipp="Das dritte Argument von pow ist der Modul.")

k.code(r"""
    ## RSA programmieren

    Schreibe zwei Funktionen mit n = 33, e = 3, d = 7:
        verschluesseln(m)    →  liefert  m ** e % n
        entschluesseln(c)    →  liefert  c ** d % n

    Test: entschluesseln(verschluesseln(m)) muss wieder m ergeben!
    """,
    [F("verschluesseln(4)", 31), F("entschluesseln(31)", 4),
     F("[entschluesseln(verschluesseln(m)) for m in range(33)]", list(range(33)))],
    """
    n = 33
    e = 3
    d = 7

    def verschluesseln(m):
        return m ** e % n

    def entschluesseln(c):
        return c ** d % n
    """,
    "Spiel ruhig damit: Verschlüssele eine Zahl und lass sie von deinem Sitznachbarn "
    "entschlüsseln!",
    tipp="Zwei kurze Funktionen mit return ... ** ... % n",
    tipps=["Lege n, e und d als Variablen an.",
           "verschluesseln gibt m ** e % n zurück.",
           "def entschluesseln(c):\n    return c ** d % n"])

k.code(r"""
    ## Das passende d finden

    Schreibe eine Funktion `inverses(e, N)`, die das **kleinste** d mit
    0 < d < N zurückgibt, für das `e * d % N == 1` gilt. Gibt es kein
    solches d, soll sie `None` zurückgeben.

        inverses(3, 20)     →  7
        inverses(7, 3120)   →  1783
        inverses(2, 20)     →  None     (2 und 20 sind beide gerade)
    """,
    [F("inverses(3, 20)", 7), F("inverses(7, 3120)", 1783), F("inverses(2, 20)", None),
     F("inverses(3, 40)", 27), F("inverses(1, 5)", 1)],
    """
    def inverses(e, N):
        for d in range(1, N):
            if e * d % N == 1:
                return d
        return None
    """,
    "Die Schleife probiert alle d von 1 bis N − 1 der Reihe nach. Das erste passende d wird "
    "sofort mit `return` zurückgegeben, also ist es das kleinste. Findet die Schleife keins, "
    "kommt man unten bei `return None` an. Das passiert genau dann, wenn ggT(e, N) nicht 1 ist.",
    tipps=["Probiere alle d von 1 bis N − 1 durch.",
           "for d in range(1, N): und darin prüfen, ob e * d % N == 1 ist.",
           "Das erste passende d sofort zurückgeben; nach der Schleife return None."],
    vorlage="def inverses(e, N):\n    ...\n")

k.code(r"""
    ## Zusatz: Text verschlüsseln

    Dies steht nicht auf den Übungsblättern, ist aber eine schöne
    Erweiterung. RSA verschlüsselt Zahlen. Mit `ord(zeichen)` wird aus
    jedem Zeichen eine Zahl, mit `chr(zahl)` wieder ein Zeichen.

    Schreibe zwei Funktionen:
      • `text_verschluesseln(text, oeffentlich)`: verschlüsselt jedes
        Zeichen einzeln mit dem Schlüssel `(e, n)` und gibt eine **Liste
        von Zahlen** zurück.
      • `text_entschluesseln(zahlen, privat)`: macht daraus mit `(d, n)`
        wieder den Text.

    Getestet wird mit den Schlüsseln (7, 3233) und (1783, 3233):

        text_verschluesseln("A", (7, 3233))   →  [1317]
    """,
    [F('text_verschluesseln("A", (7, 3233))', [1317]),
     F('text_verschluesseln("", (7, 3233))', []),
     F('text_entschluesseln([1317], (1783, 3233))', "A"),
     F('text_entschluesseln(text_verschluesseln("Hallo TU!", (7, 3233)), (1783, 3233))',
       "Hallo TU!"),
     F('text_entschluesseln(text_verschluesseln("Grüße", (7, 3233)), (1783, 3233))', "Grüße")],
    """
    def text_verschluesseln(text, oeffentlich):
        e, n = oeffentlich
        zahlen = []
        for zeichen in text:
            zahlen.append(pow(ord(zeichen), e, n))
        return zahlen

    def text_entschluesseln(zahlen, privat):
        d, n = privat
        text = ""
        for c in zahlen:
            text += chr(pow(c, d, n))
        return text
    """,
    "Jedes Zeichen wird mit `ord` zu einer Zahl (z. B. 'A' → 65) und dann wie in Übung 1 "
    "verschlüsselt. Beim Entschlüsseln kommt die Zahl zurück, und `chr` macht wieder ein "
    "Zeichen daraus. Das klappt, solange jede Zeichennummer kleiner als n ist. Echtes RSA "
    "verschlüsselt übrigens nicht Zeichen für Zeichen, das wäre zu leicht zu knacken.",
    tipps=["Pack den Schlüssel zuerst aus: e, n = oeffentlich.",
           "In einer Schleife über den Text: pow(ord(zeichen), e, n) an eine Liste hängen.",
           "Beim Entschlüsseln: text += chr(pow(c, d, n))"],
    vorlage="def text_verschluesseln(text, oeffentlich):\n    ...\n\n"
            "def text_entschluesseln(zahlen, privat):\n    ...\n")

k.zusammenfassung(r"""
    ## RSA auf einen Blick

    | Schritt | Formel | Beispiel p = 3, q = 11 |
    |---|---|---|
    | Modul | n = p · q | 33 |
    | N = φ(n) | (p − 1)(q − 1) | 20 |
    | e | ggT(e, N) = 1 | 3 |
    | d | e · d mod N = 1 | 7 |
    | verschlüsseln | c = m^e mod n | 4 → 31 |
    | entschlüsseln | m = c^d mod n | 31 → 4 |

    !! e und d sucht man mit N, gerechnet wird mit n.

      • Öffentlicher Schlüssel (e, n), privater Schlüssel (d, n).
      • Die Nachricht muss 0 ≤ m < n erfüllen.
      • `pow(m, e, n)` ist dasselbe wie `m ** e % n`, aber viel schneller.

        def encrypt(m, oeffentlich):
            e, n = oeffentlich
            return pow(m, e, n)
    """)
