# -*- coding: utf-8 -*-
"""Kapitel: Bonus: Farben von HSV nach RGB umrechnen (Übung 3, Aufgabe 3.3 in kleinen Schritten)."""
from ..engine import neues_kapitel, P, F  # noqa: F401

k = neues_kapitel(
    slug="hsv_rgb",
    titel="Bonus: Farben von HSV nach RGB umrechnen",
    beschreibung="Eine größere Funktion mit math.floor und vielen Fällen (Übung 3, 3.3)",
    quelle="Übung 3",
    teil="bonus",
    icon="🎨")

k.lernziele([
    "Ich kann erklären, was H, S und V bei einer Farbe bedeuten und wie RGB funktioniert",
    "Ich kann die Hilfswerte hi, f, p, q und t aus den Formeln von Übung 3 berechnen",
    "Ich kann mit if/elif/else den passenden Fall auswählen und ein Tupel zurückgeben",
    "Ich kann mit HSV Farben mit gleichem Farbtonabstand erzeugen",
])

_HSV = """
import math

def hsv_zu_rgb(h, s, v):
    hi = math.floor(h / 60)
    f = h / 60 - hi
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))
    if hi == 1:
        return (q, v, p)
    elif hi == 2:
        return (p, v, t)
    elif hi == 3:
        return (p, q, v)
    elif hi == 4:
        return (t, p, v)
    elif hi == 5:
        return (v, p, q)
    else:
        return (v, t, p)
"""

# ── Erklärung 1: HSV und RGB ─────────────────────────────────────────────
k.erklaerung("HSV und RGB", r"""
    ## Zwei Arten, Farben zu beschreiben

    **RGB**: Wie viel Rot, Grün und Blau steckt in der Farbe? Jeder Anteil
    liegt hier zwischen 0 und 1.

    | Farbe | RGB |
    |---|---|
    | Rot | `(1, 0, 0)` |
    | Gelb | `(1, 1, 0)` |
    | Grau | `(0.5, 0.5, 0.5)` |
    | Schwarz | `(0, 0, 0)` |

    **HSV** beschreibt eine Farbe so wie der Farbwähler eines Malprogramms:
      • **H** (Hue) = Farbton auf dem Farbkreis, 0 bis 360 Grad
        (0 = Rot, 60 = Gelb, 120 = Grün, 240 = Blau, 360 = wieder Rot)
      • **S** (Saturation) = Sättigung von 0 (grau) bis 1 (knallig)
      • **V** (Value) = Helligkeit von 0 (schwarz) bis 1 (hell)

    :::analogie 🎨 Der Farbkasten
    Stell dir einen runden Farbkasten vor.
      • **H** sagt, in welches Näpfchen du den Pinsel tauchst: Du drehst
        dich auf dem Kreis um H Grad weiter.
      • **S** sagt, wie viel Wasser du dazugibst: Viel Wasser (S nahe 0)
        macht die Farbe blass und grau, wenig Wasser macht sie kräftig.
      • **V** sagt, wie hell das Licht im Raum ist: Bei V = 0 ist alles schwarz.
    Gleich weit auseinanderliegende Näpfchen ergeben gleichmäßig verteilte
    Farben. Darum nutzt man HSV z. B. für Farben mit gleichem Farbtonabstand.
    :::
    ---
    ## Die Formeln aus der Übung

        hi = floor(H / 60)          (mit math.floor)
        f  = H / 60 - hi
        p  = V · (1 - S)
        q  = V · (1 - S · f)
        t  = V · (1 - S · (1 - f))

        (r, g, b) = (q, V, p)    wenn hi = 1
                    (p, V, t)    wenn hi = 2
                    (p, q, V)    wenn hi = 3
                    (t, p, V)    wenn hi = 4
                    (V, p, q)    wenn hi = 5
                    (V, t, p)    sonst   (also hi = 0 oder hi = 6)

    `hi` sagt, in welchem 60°-Abschnitt des Farbkreises die Farbe liegt (0 bis
    5). `f` sagt, wie weit sie in diesem Abschnitt schon ist (0 bis knapp 1).
    Das Ergebnis liegt im Bereich [0, 1].

    :::achtung H = 360 ergibt hi = 6
    `math.floor(360 / 60)` ist 6. Diesen Fall gibt es in der Liste nicht
    extra, er landet in „sonst“ und liefert wieder Rot. Das passt: 360° ist
    auf dem Farbkreis dieselbe Stelle wie 0°.
    :::
    ---
    ## Ein Beispiel Schritt für Schritt: Orange

    Orange hat H = 30, S = 1, V = 1.

    :::trace
    import math
    h, s, v = 30, 1, 1
    hi = math.floor(h / 60)
    f = h / 60 - hi
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))
    print(hi, f, p, q, t)
    print((v, t, p))
    :::

    hi ist 0, also gilt „sonst“: `(V, t, p) = (1, 0.5, 0)`. Volles Rot, halbes
    Grün, kein Blau: Orange.
    """)

k.ausgabe("import math\nprint(math.floor(200 / 60))",
          "200 / 60 = 3.33…, abgerundet 3. Ein Farbton von 200° liegt also im Abschnitt hi = 3 "
          "(180° bis 240°).",
          tipp="Wie oft passt 60 ganz in 200?")
k.mc("Welcher Fall gilt für H = 120 (Grün)?",
     ["hi = 2, also (p, V, t)", "hi = 1, also (q, V, p)", "hi = 0, also (V, t, p)", "hi = 3, also (p, q, V)"],
     "120 / 60 = 2, abgerundet 2. Für S = 1, V = 1 ist p = 0 und t = 0 (f = 0), das Ergebnis "
     "ist (0, 1, 0): reines Grün.")
k.wf("Für H = 360 gibt es keinen passenden Fall in den Formeln, deshalb ist das Ergebnis falsch.", False,
     "hi = 6 fällt in „sonst“ und liefert (V, t, p). Mit f = 0 ist das bei S = 1, V = 1 genau "
     "(1, 0, 0), also Rot – wie bei H = 0.")
k.ausgabe("s, v = 0, 0.5\np = v * (1 - s)\nprint(p)",
          "Bei S = 0 (keine Sättigung) ist p = V · 1 = V. Auch q und t werden zu V: Die Farbe ist "
          "ein Grauton (0.5, 0.5, 0.5).")

# ── Praxis ───────────────────────────────────────────────────────────────
k.luecke("Ergänze die ersten beiden Formeln: hi ist der abgerundete Abschnitt, f der Rest darin.",
         """
         import math
         h = 200
         hi = math.___(h / 60)
         f = h / 60 - ___
         print(hi, f)
         """,
         [["floor"], ["hi"]],
         "math.floor rundet ab: floor(3.33) = 3. Zieht man hi von h / 60 ab, bleibt der Anteil "
         "f = 0.33… übrig.",
         tipp="Der Hinweis auf dem Blatt nennt die Funktion zum Abrunden.")

k.puzzle("Bringe die Zeilen in die richtige Reihenfolge: Für hi = 2 soll (p, V, t) ausgegeben "
         "werden, sonst (V, t, p).",
         """
         hi, v, p, t = 2, 1, 0, 0.5
         if hi == 2:
             print((p, v, t))
         else:
             print((v, t, p))
         """,
         "Erst die Werte festlegen, dann mit if/else den passenden Fall wählen.",
         tipp="Was muss feststehen, bevor man vergleicht?",
         ablenker=["elif hi = 2:"])

k.code(r"""
    ## Von 0 bis 1 nach 0 bis 255

    Viele Programme erwarten RGB-Werte als ganze Zahlen von 0 bis 255 statt
    von 0 bis 1. Schreibe eine Funktion `zu_255(farbe)`, die ein Tupel
    `(r, g, b)` mit Werten von 0 bis 1 bekommt und ein Tupel mit **gerundeten
    ganzen Zahlen** von 0 bis 255 zurückgibt (mit `round()`).

        zu_255((1, 0.5, 0))     → (255, 128, 0)
        zu_255((0.2, 0.4, 0.6)) → (51, 102, 153)
    """,
    [F("zu_255((1, 0.5, 0))", (255, 128, 0)),
     F("zu_255((0, 0, 0))", (0, 0, 0)),
     F("zu_255((1, 1, 1))", (255, 255, 255)),
     F("zu_255((0.2, 0.4, 0.6))", (51, 102, 153)),
     F("type(zu_255((1, 1, 1))[0]).__name__", "int")],
    """
    def zu_255(farbe):
        r, g, b = farbe
        return (round(r * 255), round(g * 255), round(b * 255))
    """,
    "Tupel auspacken, jeden Anteil mal 255 nehmen und runden, wieder als Tupel zurückgeben. "
    "0.5 · 255 = 127.5 wird zu 128 gerundet.",
    tipps=["Pack das Tupel in drei Variablen aus.",
           "Jeder Wert wird mit 255 multipliziert und mit round() gerundet.",
           "return (round(r * 255), round(g * 255), round(b * 255))"],
    vorlage="def zu_255(farbe):\n    ...\n")

k.code(r"""
    ## Farbpalette mit gleichem Farbtonabstand

    Die Funktion `hsv_zu_rgb(h, s, v)` aus Übung 3, Aufgabe 3.3 ist hier
    **schon vorgegeben** (du musst sie nicht schreiben).

    Schreibe eine Funktion `farbpalette(n)`, die eine Liste mit `n` RGB-Tupeln
    zurückgibt. Die Farbtöne sollen gleichmäßig über den Farbkreis verteilt
    sein: H = 0, 360/n, 2·360/n, … (immer S = 1 und V = 1). Für `n = 0` ist
    die Liste leer.

        farbpalette(3) → [(1, 0, 0), (0, 1, 0), (0, 0, 1)]   (Rot, Grün, Blau)
    """,
    [F("farbpalette(3)", vorspann=_HSV), F("farbpalette(1)", vorspann=_HSV),
     F("farbpalette(6)", vorspann=_HSV), F("farbpalette(0)", vorspann=_HSV),
     F("len(farbpalette(12))", vorspann=_HSV)],
    """
    def farbpalette(n):
        farben = []
        for i in range(n):
            h = i * 360 / n
            farben.append(hsv_zu_rgb(h, 1, 1))
        return farben
    """,
    "Der Abstand zwischen zwei Farbtönen ist 360 / n Grad. i läuft von 0 bis n - 1, also "
    "kommt man nie bei 360 an (das wäre wieder Rot). Die Liste wird als Akkumulator aufgebaut.",
    tipps=["Wie groß ist der Abstand zwischen zwei Farbtönen bei n Farben?",
           "for i in range(n): h = i * 360 / n",
           "farben.append(hsv_zu_rgb(h, 1, 1)) und am Ende return farben"],
    vorlage="# hsv_zu_rgb(h, s, v) ist schon vorgegeben\n\ndef farbpalette(n):\n    ...\n")

k.zusammenfassung(r"""
    ## HSV → RGB auf einen Blick

    | Wert | Bedeutung | Bereich |
    |---|---|---|
    | H | Farbton auf dem Farbkreis | 0 bis 360 |
    | S | Sättigung (grau ↔ kräftig) | 0 bis 1 |
    | V | Helligkeit (schwarz ↔ hell) | 0 bis 1 |

        hi = math.floor(h / 60)     # Abschnitt 0 … 5 (6 bei h = 360 → „sonst“)
        f = h / 60 - hi             # Anteil im Abschnitt
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))
        # dann mit if/elif/else das passende Tupel zurückgeben

    !! Gleich große Schritte im Farbton (360 / n) ergeben gleichmäßig verteilte Farben.
    """)
