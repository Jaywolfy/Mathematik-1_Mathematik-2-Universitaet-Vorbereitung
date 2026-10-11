# Vorlage für ein Kapitelmodul

Diese Datei wird nicht geladen (Name beginnt mit `_`). Vollständige, geprüfte Musterkapitel sind
`f01_zahlen.py`, `f02_rechnen.py` und `f03_brueche.py`: **Lies mindestens eins davon ganz**, bevor du ein
neues Kapitel schreibst. Der Vertrag steht in `mathe/ARCHITEKTUR.md` (Abschnitte 2, 3, 4, 6).

## So legst du ein Kapitel an

1. Datei anlegen: `f<NN>_<slug>.py` (Fundament), `m1_<NN>_<slug>.py`, `m2_<NN>_<slug>.py`, `b_…`, `k_…`.
2. Gerüst unten kopieren und füllen.
3. Neue Fachbegriffe in einer **eigenen Datei je Kapitel** eintragen: `inhalte/_glossar_<dateiname>.py`, z. B.
   `_glossar_v01.py` mit `from .glossar import eintrag` und `eintrag(begriff, erklaerung, beispiel, kapitel_slug, synonyme)`.
   Vorher prüfen, ob der Begriff schon existiert (`grep -rn 'eintrag("Begriff' inhalte/`). Doppelte Begriffe sind Fehler.
   `quelle=` bei `neues_kapitel` ist Pflicht (Fundstelle aus `mathe/LEHRPLAN.md`).
4. `python3 mathe_quiz.py --selbsttest --kapitel <slug>` → **0 Fehler**. Danach den ganzen Selbsttest.
5. Im Browser ansehen: `python3 mathe_quiz.py --gui`.

## Regeln in Kürze

- **Alle Zahlen rechnet Python.** Lösungen mit `Fraction`/`mathlib` berechnen oder `k.berechne`,
  `k.vereinfache`, `k.gleichung`, `k.lgs` benutzen. Keine Ergebnisse von Hand eintippen, wo es anders geht.
- Jeder Text mit LaTeX ist ein **Raw-String**: `r"…"`, `r"""…"""`. In normalen und f-Strings Backslash
  verdoppeln (`"$\\frac{1}{2}$"`), in f-Strings geschweifte Klammern verdoppeln: `f"\\frac{{{a}}}{{{b}}}"`.
  In JSON (Visuals) ebenfalls `\\`. Kommazahlen in LaTeX: `2{,}5`.
- Keine Backslashes und keine gleichen Anführungszeichen **innerhalb** von `{…}` in f-Strings (Python 3.10!).
- Bei `mc` ist die **erste** Option richtig. `zuordnen`: rechte Seite als Klartext (ℕ, ½ als Unicode).
- Jede Frage: `tipps=[vage, konkreter, fast die Lösung]`, `erklaerung`, bei Rechenfragen `rechenweg` mit
  `:::rechnung`, mindestens 3 Fragen im Üben-Teil mit `typische_fehler` bzw. `fehler=`.
- Seiten: höchstens ~120 Wörter, genau eine neue Idee, jede mit `:::rechnung` oder `:::visual` **und** `:::alt`.
- `:::rechnung`: jede Zeile `LaTeX || Begründung`. Der Selbsttest rechnet jede Zeile nach: Ketten müssen
  stimmen, Gleichungsumformungen müssen von der Lösung in den letzten Zeilen (`x = 5`) erfüllt werden.
  Absichtlich falsche Zeile: `!` am Anfang. Notizen wie `\quad | -5` am Zeilenende sind erlaubt.
- Sprache: Du-Form, kurze Sätze, kleine Zahlen, keine Floskeln, keine Gedankenstriche als Stilmittel.

## Gerüst

```python
# -*- coding: utf-8 -*-
"""Fundament N: Thema – Untertitel."""
from fractions import Fraction as F

from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

tk = mathlib.tex_klammer        # (-3) in Klammern

k = neues_kapitel(slug="thema", titel="Titel", beschreibung="Ein Satz, was drin ist",
                  teil="fundament", icon="🧮")
k.lernziele(["Ich kann …", "Ich kann …", "Ich kann …"])
k.warum(r"""Konkreter Informatik-Bezug (Datentypen, Algorithmen, Laufzeit, Grafik, Kryptografie, ML …).""")

k.erklaerung("Erste Idee", r"""
    ## Überschrift

    :::analogie 🍕 Alltagsbild
    Kurzes Bild aus dem Alltag.
    :::

    Erklärung mit [[Fachbegriff]] und Formel $a + b$.

    :::rechnung Beispiel vorgerechnet
    2 + 3 \cdot 4 || Aufgabe
    = 2 + 12 || Punkt vor Strich
    = 14 || addieren
    :::

    :::alt Mit einem anderen Bild erklärt
    Wirklich anders erklärt, nicht nur umformuliert.
    :::
    ---
    ## Nächste Seite …
    """)

# Frage direkt zur Idee
k.berechne("2 + 3*4", tipps=["…", "…", "…"], erklaerung="…",
           rechenweg=r""":::rechnung
           2 + 3 \cdot 4 = 2 + 12 || Punkt vor Strich
           = 14 || addieren
           :::""",
           typische_fehler=[(20, "Du hast von links nach rechts gerechnet …")])

k.praxis()
k.generator(meine_generatorfunktion, typ="zahl", titel="Kurzer Name", glatt=True)
k.zahl("…", F(3, 4), "…", uebungsblatt=True, tipps=[…], rechenweg=r"""…""")
k.zusammenfassung(r"""## Merkzettel …""")
```

## Alle Fragetypen (Kurzbeispiele)

```python
k.mc("Frage?", ["richtig", "falsch 1", "falsch 2"], "Erklärung", tipps=[...],
     fehler={"falsch 1": "Was man vermutlich gedacht hat und warum es falsch ist."})
k.wf("Aussage", True, "Erklärung", tipps=["…"])
k.text("Wie heißt …?", ["Antwort", "Variante"], "Erklärung", tipps=[...])
k.zahl("Berechne $\\frac{3}{4} : \\frac{1}{2}$.", F(3, 4) / F(1, 2), "…", gekuerzt=True, form="bruch",
       tipps=[...], rechenweg=r"""…""", typische_fehler=[(F(3, 8), "…")])
k.berechne("1/2 + 1/3", gekuerzt=True, tipps=[...], rechenweg=r"""…""")      # Frage + Lösung automatisch
k.term("Multipliziere aus: $(x+1)^2$", "x^2 + 2x + 1", "…", variablen="x", form="ausmultipliziert", ...)
k.vereinfache("2(x+3) - x", "x + 6", form="ausmultipliziert", variablen="x", ...)   # prüft Äquivalenz
k.gleichung("3x + 5 = 20", tipps=[...], rechenweg=r"""…""")                    # Lösungsmenge per mathlib
k.loesungsmenge("Löse $x^2 < 4$.", "(-2; 2)", "…", ...)
k.menge("Gib $\\{x \\in \\mathbb{Z} \\mid -3 \\le x < 2\\}$ an.", "{-3; -2; -1; 0; 1}", "…", ...)
k.vektor("…", [1, F(1, 2), -3], "…", ...)                       # vielfaches=True für Richtungen
k.matrix("…", [[1, 2], [3, 4]], "…", ...)
k.lgs("Löse das System …", [[1, 1], [1, -1]], [3, 1], "…", ...)   # Lösung via Gauß
k.mehrfach("Welche …?", ["$\\mathbb{Z}$", "$\\mathbb{Q}$"], ["$\\mathbb{N}$"], "…", fehler={...}, ...)
k.zuordnen("Ordne zu …", [("$5$", "ℕ (natürliche Zahlen)"), ("$-2$", "ℤ (ganze Zahlen)")], "…", ...)
k.ordnen("Bringe die Schritte in Reihenfolge …", ["Schritt 1", "Schritt 2"], "…", ablenker=["falsch"], ...)
k.luecke("Erweitere:", "\\frac{2}{3} = \\frac{\\luecke}{12}", [[8]], "…", typische_fehler=[([2], "…")], ...)
k.graph_punkt("Setze den Scheitelpunkt.", {"funktionen": [{"term": "x^2 - 2"}], "x": [-4, 4], "y": [-3, 6]},
              modus="setzen", ziel=(0, -2), erklaerung="…", tipps=[...], rechenweg="…")
k.rechenweg_aufgabe("Längere Aufgabe …", [
    {"typ": "zahl", "frage": "Schritt 1: …", "loesung": F(2, 9), "tipps": [...], "rechenweg": "…",
     "typische_fehler": [(…, "…")]},
    {"typ": "zahl", "frage": "Schritt 2: …", "loesung": 9, "tipps": [...], "rechenweg": "…"}],
    "Erklärung", uebungsblatt=True, tipps=[...], rechenweg=r"""…""")
k.papier(r"""Beweise/erkläre auf Papier …""", r"""Musterlösung (Markup)""",
         ["Checkpunkt 1", "Checkpunkt 2"], "Erklärung", tipps=["…"])
```

## Generator

```python
def brueche_kuerzen(rng):                       # Name nie mehr ändern (ID hängt daran)
    p, q, g = …                                  # Zahlen zufällig, aber "schön"
    loesung = F(p, q)
    fehler = [(F(q, p), "Das ist der Kehrwert …")]
    return {
        "frage": f"Kürze $\\frac{{{p * g}}}{{{q * g}}}$ vollständig.",
        "loesung": loesung, "gekuerzt": True,        # weitere Felder des Fragetyps erlaubt
        "tipps": [...3 Stück, passend zu den Zahlen...],
        "rechenweg": ":::rechnung\n… || …\n:::",     # wird vom Selbsttest nachgerechnet
        "erklaerung": "…",
        "typische_fehler": ohne_gleiche(loesung, fehler),   # nie gleich der Lösung
    }

k.generator(brueche_kuerzen, typ="zahl", titel="Brüche kürzen", glatt=True)
```

Ein Generator läuft im Selbsttest mit 200 Seeds. Vermeide Sonderfälle, bei denen ein typischer Fehler
zufällig richtig wäre (z. B. Faktor 1, Summe 0) und Nenner, die für Anfänger zu groß sind.

## Visuals

Erlaubt sind nur Typen aus `visuals.VISUAL_FERTIG` (aktuell: `zahlenstrahl`, `bruch`, `rechnung` (Waage),
`funktionsgraph`, `parabel`). Felder: `ARCHITEKTUR.md` Abschnitt 4 bzw. `visuals.SCHEMA`.
Beispiele: `mathe/demo.py` und die Demo-Seite `#/demo/visuals`.
