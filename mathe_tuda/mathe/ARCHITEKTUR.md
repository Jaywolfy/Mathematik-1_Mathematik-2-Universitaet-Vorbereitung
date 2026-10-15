# Mathe-Lernsystem – Architektur & Vertrag

Diese Datei ist der verbindliche Vertrag zwischen allen Teilen des Programms.
Wer etwas baut (auch Subagenten, die Kapitel schreiben), hält sich an diese
Schnittstellen. Vorbild ist der Python-Vorkurs (`vorkurs_tuda/vorkurs/ARCHITEKTUR.md`);
Aufbau und Prinzipien sind übernommen, alles Python-Spezifische ist durch Mathe ersetzt.

Ziel: Lernsystem für komplette Anfänger, die Mathe 1 und Mathe 2 im B.Sc. Informatik
an der TU Darmstadt bestehen wollen – vom Bruchrechnen bis zu Eigenwerten und Integralen.

## 0. Grundregeln

- **Nur Python-Standardbibliothek (>= 3.10)**. Keine pip-Pakete. `umgebung.OPTIONALE_PAKETE` bleibt leer.
- **Komplett offline.** Einzige Fremdbibliothek: **KaTeX 0.19.0**, einmalig mit
  `python3 tools/katex_holen.py` aus dem npm-Registry geladen (sha512 geprüft) und unter
  `mathe/web/static/vendor/katex/` mitgeliefert (CSS, JS, Auto-Render, `.woff2`-Schriften, MIT-Lizenz).
  Es gibt **keine** externe URL im Programm. Fehlt KaTeX, zeigt `formel.js` lesbaren Unicode-Ersatz.
- Frontend ohne Framework und ohne Build-Schritt (ES-Module).
- Dateinamen im Paket nur ASCII. Pfade immer relativ zu `Path(__file__)`.
- Fortschritt liegt **nicht** im Programmordner (Abschnitt 8): Weitergabe des Ordners schickt keinen Stand mit.
- Start: `Start.bat` (Windows, CRLF, nur ASCII), `Start.command` (macOS, LF), `start.sh` (Linux, LF).
  Sie suchen Python >= 3.10, geben sonst Installationshinweise und starten `mathe_quiz.py`.

## 1. Ordnerstruktur

```
Start.bat / Start.command / start.sh / LIESMICH.md
mathe_quiz.py            Starter: --gui (Standard), --selbsttest [--kapitel SLUG] [--leise],
                         --port N (Standard 8766), --kein-browser, --keine-farben, --e2e (nur Tests)
tools/katex_holen.py     KaTeX einmalig holen (Entwickler)
tools/katex_check.js     alle Formeln mit echtem KaTeX prüfen (nur wenn Node vorhanden)
mathe/
  ARCHITEKTUR.md         diese Datei
  engine.py              Kapitel, Fragetypen, Generatoren, Prüfablauf, Musterantworten
  pruefer.py             sicherer Term-Parser, exakte Auswertung, Äquivalenz, Formchecks,
                         Zahl/Menge/Lösungsmenge, LaTeX->Term (für :::rechnung), LaTeX-Validator
  mathlib.py             exakte Helfer: tex(), Polynom, Matrix, gauss(), det(), inverse(), kern(),
                         lgs_loesen(), euklid_schritte(), primfaktoren(), in_basis(), loese()
  markup.py              Markup -> Blöcke (Abschnitt 3), latex_zu_text()
  visuals.py             Visual-Schemata + exakte Zusatzdaten (Abschnitt 4)
  fortschritt.py         Laden/Speichern, XP, Level, Serie, Abzeichen, Leitner, Meisterschaft
  selbsttest.py          prüft ALLE Inhalte (Abschnitt 10)
  spielwiese.py          Werkzeuge der Spielwiese mit Rechenweg
  demo.py                Beispieldaten für #/demo/visuals
  umgebung.py            Startprüfungen
  inhalte/
    __init__.py          lädt Kapitel: f*, v*, m1_*, m2_*, b_*, k_* (je alphabetisch)
    _VORLAGE_KAPITEL.md  Vorlage für neue Kapitel (LESEN!)
    _glossar_eintraege.py  Glossar-Einträge der Kapitel f01–f03
    _glossar_<datei>.py  Glossar-Einträge eines Kapitels, z. B. _glossar_v01.py (eine Datei je Kapitel)
    glossar.py, formelsammlung.py, diagnose.py
    f01_zahlen.py …      ein Modul pro Kapitel
  web/
    server.py            http.server + JSON-API (Abschnitt 9)
    static/              index.html, app.css, app.js, kapitel.js, fragen.js, eingabe.js, formel.js,
                         markup.js, plot.js, visuals.js, vis_*.js, training.js, seiten.js, e2e.js, …
    static/vendor/katex/ KaTeX (lokal)
```

Die Terminal-Oberfläche des Vorkurses gibt es hier (noch) nicht: Formeln gehören in den Browser.

## 2. Kapitel-API (für Inhalte)

```python
from fractions import Fraction as F
from .. import mathlib
from ..engine import neues_kapitel, ohne_gleiche

k = neues_kapitel(slug="brueche", titel="Brüche", beschreibung="…", teil="fundament", icon="🥧",
                  quelle="Schulstoff (Voraussetzung für den TU-Vorkurs)", rechenthema=True)
k.lernziele(["Ich kann …", …])          # 3–5
k.warum(r"""Wozu brauche ich das als Informatiker? (Markup)""")
k.erklaerung("Titel", r"""Markup, Seiten mit ---""")
k.<frage>(…)                             # Verständnis-/Rechenfragen direkt nach der Idee
…
k.praxis()                               # ab hier Praxisaufgaben (leicht -> schwer)
k.generator(fn, typ="zahl", titel="…")   # mindestens ein Generator pro Rechenthema
k.<frage>(…, uebungsblatt=True)          # mindestens eine im Übungsblatt-Stil
k.zusammenfassung(r"""Merkzettel (Markup) -> landet in der Formelsammlung""")
```

`teil` ∈ `fundament`, `vorkurs`, `mathe1`, `mathe2`, `bonus`, `klausur`. **Nur dieser Wert** entscheidet,
wo ein Kapitel erscheint. Welche Kapitel es gibt und woher ihr Stoff stammt, legt `mathe/LEHRPLAN.md`
fest (Modulhandbuch PO 2023, Vorkurs-Folien 2026, Skript Mathe I/II). `quelle` ist Pflicht und nennt
die Fundstelle, z. B. `"MVK 2026, VL 3"` oder `"Mathe I (PO 2023); Skript Kap. 2.1"`.

### Gemeinsame Parameter aller Fragen

`erklaerung` (Markup, nach der Antwort), `tipps=[vage, konkreter, fast die Lösung]`,
`rechenweg` (Markup, meist mit `:::rechnung`; Pflicht bei Rechenfragen),
`typische_fehler=[(wert, meldung), …]` (Fehlwert im Lösungsformat + kurze Erklärung, was man
vermutlich gemacht hat und warum es nicht geht), `uebungsblatt=False`, `punkte=1` (Klausur).

### Fragetypen

| Methode | Antwort der Oberfläche | Prüfung |
|---|---|---|
| `k.mc(frage, optionen, erkl, fehler={option: meldung})` | Optionstext | erste Option ist richtig (wird gemischt) |
| `k.wf(aussage, wahr, erkl)` | bool | |
| `k.text(frage, [akzeptiert], erkl)` | str | Groß/klein und Leerzeichen egal |
| `k.zahl(frage, loesung, erkl, toleranz=None, gekuerzt=False, form=None, einheit=None)` | str | exakt mit `Fraction`, irrational mit rel. Toleranz 1e-9 oder `toleranz`; `gekuerzt` meldet ungekürzte Brüche („Fast!“); `form="bruch"` verlangt Bruch statt Kommazahl |
| `k.term(frage, loesung, erkl, variablen="x", form=None)` | str | Äquivalenz an ≥ 8 Zufallsstellen (exakt an rationalen Stellen); `form`: `ausmultipliziert`, `faktorisiert`, `gekuerzt`, `ohne_klammern`, `vereinfacht` (mit `\|` kombinierbar) |
| `k.loesungsmenge(frage, loesung, erkl, variable="x")` | str | Punkte, Intervalle, Vereinigungen, leer, ℝ, `ℝ \ {2}`, `x < 2` … |
| `k.menge(frage, loesung, erkl)` | str | als Menge (Reihenfolge, Doppelte egal); Elemente: Zahlen, Symbole, Tupel, Mengen, `∅`/`\emptyset`; ein einzelnes `e` ist ein Buchstabe, wenn die Musterlösung daneben weitere Symbole enthält (`{a, b, e}`), sonst die Euler-Zahl; ein einzelnes `E` ist immer ein Symbol |
| `k.vektor(frage, loesung, erkl, vielfaches=False)` | [str] | elementweise exakt; `vielfaches`: jedes Vielfache ≠ 0 |
| `k.matrix(frage, loesung, erkl)` | [[str]] | elementweise; erkennt die Transponierte |
| `k.lgs(frage, A, b, erkl, variablen=None)` | {keine, werte} | Lösung von `mathlib.lgs_loesen`; Parameter `t, s, r, u` werden durch Einsetzen + Kern-Dimension geprüft |
| `k.mehrfach(frage, richtig, falsch, erkl, fehler={})` | [Optionstexte] | Teilpunkte |
| `k.zuordnen(frage, [(links, rechts)], erkl, ablenker=())` | [[l, r]] | rechte Seite als **Klartext** (Select-Feld, kein LaTeX) |
| `k.ordnen(frage, schritte, erkl, ablenker=(), alternativen=())` | [zeilen_id] | Parsons-Prinzip für Rechen-/Beweisschritte |
| `k.luecke(frage, formel_mit_\luecke, [[akzeptiert], …], erkl)` | [str] | je Lücke Zahl/Term-Äquivalenz |
| `k.graph_punkt(frage, visual, modus="setzen", ziel=(x, y) / modus="ablesen", loesung=…, toleranz=0.25, raster=0.5)` | [x, y] / str | Funktionsgraph aus `visual` (Schema wie `funktionsgraph`) |
| `k.rechenweg_aufgabe(frage, [{"typ": "zahl", "frage": …, "loesung": …, "tipps": …, …}, …])` | {schritt, antwort} | 2–5 Teilschritte (Typen: zahl, term, loesungsmenge, menge, text, vektor, matrix, mc, luecke, wf), jeder einzeln, Teilpunkte; nach jedem Schritt wird der richtige Wert gezeigt |
| `k.papier(aufgabe, musterloesung, [checkliste], erkl)` | [bool] | Selbstbewertung pro Punkt, XP 5 je Punkt |
| `k.generator(fn, typ, titel, glatt=False, probe=None)` | wie `typ` | siehe unten |

Bequeme Varianten (Python rechnet die Lösung selbst aus):
`k.berechne("1/2+1/3", frage=None)` → Zahl-Frage mit exaktem Wert; `{term}` im Fragetext wird gesetzt.
`k.vereinfache(term, loesung, form=…)` → der Selbsttest prüft `term ≡ loesung` und die Form der Lösung.
`k.gleichung("3x+5=20", loesung=None)` → `mathlib.loese` berechnet die Lösungsmenge (Polynome bis Grad 2
vollständig, höher über rationale Nullstellen, auch Ungleichungen); eine angegebene `loesung` wird gegengeprüft.

### Generator

`fn(rng)` (rng = `random.Random`) liefert ein Dict: `frage`, `loesung` (bzw. typspezifische Felder wie
`optionen`, `schritte`, `a`/`b`), `tipps`, `rechenweg`, `erklaerung`, `typische_fehler`, optional `typ`.
**Alle Zahlen berechnet Python** (`Fraction`, `mathlib`). Fehlwerte mit `ohne_gleiche(loesung, fehler)`
filtern, damit kein Fehlwert zufällig gleich der Lösung ist. Die ID hängt nur am Funktionsnamen
(`fn.__name__` niemals ändern). Jede Instanz hat einen `seed`; der Server erzeugt beim Prüfen
die Aufgabe aus dem seed neu (zustandslos, Lösung bleibt auf dem Server). `glatt=True`: Lösung
muss ein Bruch mit Nenner ≤ 100 sein. `probe(daten) -> bool`: eigene Gegenprobe.

### IDs

`f"{slug}:{sha1(art + haupttext)[:8]}"`; haupttext = Fragetext (Lücke: + Formel, Generator:
`generator:<fn.__name__>`). Textänderung = neue ID = Fortschritt der Frage weg. Tippfehler darf man trotzdem korrigieren.

## 3. Markup (markup.py)

Zeilenregeln wie im Vorkurs: `---` neue Seite, `## ` Überschrift, `!! ` Merksatz, 4+ Leerzeichen
Einrückung = vorformatierter Text, `- `/`• `/`* ` Liste, `1. ` nummerierte Liste, `| a | b |` Tabelle.

Inline: `` `code` ``, `$Formel$`, `**fett**`, `*kursiv*`, `[[Begriff]]`, `[[angezeigt|Begriff]]` (Glossar).
Reihenfolge der Erkennung: erst Code, dann Formeln, dann der Rest. In Code gibt es keine Formeln,
in Formeln kein Fett/Kursiv. `\$` ist ein echtes Dollarzeichen. `|` in Formeln trennt keine Tabellenzellen.

Abgesetzte Formel: Zeile beginnt mit `$$`, endet (ggf. Zeilen später) mit `$$` → `{"typ": "formel", "tex"}`.

Direktiven (`:::name Kopf` … `:::`, nicht verschachtelbar):

```
:::analogie 🍕 Titel     Alltagsbild (Markup)
:::achtung Titel         Warnbox mit typischen Fehlern (Markup)
:::info Titel            Hintergrund
:::warum Titel           „Wozu brauche ich das als Informatiker?“ (zusätzlich zu k.warum)
:::beispiel Titel        neutrale Beispielbox
:::alt Titel             zweite Erklärung für „Ich verstehe das nicht“ (wirklich anders erklärt!)
:::rechnung Titel        vorgerechnetes Beispiel, Zeilen:  LaTeX || Begründung
                         - Zeile mit "=" am Anfang setzt eine Kette fort
                         - "!" am Zeilenanfang: absichtlich falscher Schritt („So nicht!“, wird nicht nachgerechnet)
                         - \hl{…} hebt einen Teil farbig hervor
                         - "?? " am Zeilenanfang: wird nicht nachgerechnet, ohne Warnung (z. B. Mengenlehre, Text);
                           ebenso Zeilen mit \text{…} (zählen nur als „nicht automatisch prüfbar“)
                         - Umformungsnotiz am Rand per "\quad | -5" wird beim Nachrechnen ignoriert
:::visual TYP            JSON (Abschnitt 4)
:::vergleich L | R       zwei Spalten, getrennt durch eine Zeile |||
```

`markup.parse(text)` → Liste von Seiten; Blöcke: `ueberschrift, absatz, merke, codeblock, formel,
liste, tabelle, box{art,titel,bloecke}, alt{titel,bloecke}, rechnung{titel,schritte[{tex,grund,falsch}]},
visual{art,daten,fehler}, vergleich{titel,spalten}`.

**Escape-Regeln für Inhalte:** Jeder Text mit LaTeX ist ein `r"…"`- oder `r"""…"""`-String (sonst
wird `\frac` zu Seitenvorschub + `rac`; der Selbsttest meldet das). In normalen Strings (z. B. in
f-Strings von Generatoren) Backslashes verdoppeln: `"$\\frac{1}{2}$"`, geschweifte Klammern in
f-Strings verdoppeln: `f"\\frac{{{a}}}{{{b}}}"`. In JSON (Visuals) Backslashes verdoppeln: `"\\sqrt{2}"`.

Dezimalzahlen in LaTeX mit `{,}`: `2{,}5`. Mengen: `\mathbb{N}`. Lösungsmenge: `\mathbb{L}`.

## 4. Visualisierungen (`:::visual TYP` + JSON)

Python (`visuals.py`) prüft das Schema und rechnet exakte Zusatzfelder (beginnen mit `_`).
Das Frontend zeichnet nur (SVG, ohne Bibliothek), rechnet bei Reglern numerisch und passt sich
Hell/Dunkel an. Terme in JSON nutzen die Term-Syntax des Prüfers (`a*x^2 + c`, `sqrt(2)`, `pi`).
Zahlen dürfen Strings wie `"1/2"`, `"sqrt(2)"`, `"pi"`, `"inf"` sein. Unbekannte Felder sind Fehler.
Ein Typ darf erst benutzt werden, wenn er in `visuals.VISUAL_FERTIG` steht (Frontend gebaut).

| TYP | Pflicht | optional | Bedeutung |
|---|---|---|---|
| `zahlenstrahl` | `von`, `bis` | `schritt`, `punkte[{x, label?, farbe?: orange\|gruen}]`, `intervalle[{von, bis, von_zu, bis_zu, label?}]`, `pfeile[{von, bis, label?}]`, `interaktiv` | Zahlen, Intervalle (offen/geschlossen), Addition als Pfeile, antippbar |
| `bruch` | `zaehler`, `nenner` | `modell: kuchen\|balken`, `erweitern: k`, `kuerzen`, `plus: [[z,n],[z,n]]`, `interaktiv` | Kuchen/Balken, Erweitern, Kürzen, Addition mit Hauptnenner Schritt für Schritt |
| `rechnung` | `links`, `rechts`, `schritte[{op: "-5"\|"+2x"\|":3"\|"*2", text}]` | `variable` | Gleichung als Waage (lineare Terme), Python rechnet jeden Zustand |
| `funktionsgraph` | `funktionen[{term, label?, farbe?: 1-4}]` | `parameter[{name, wert, von, bis, schritt, tex?}]`, `x`, `y`, `wertetabelle[x…]`, `nullstellen`, `scheitel`, `punkte[{x, y, label?}]`, `gleiche_achsen` | Graphen mit Reglern, Zoom/Verschieben; Nullstellen/Scheitel/Wertetabelle exakt für die Startwerte |
| `parabel` | – | `a`, `b`, `c`, `form: allgemein\|scheitel`, `regler`, `x`, `y` | Parabel mit Reglern, Scheitel, Symmetrieachse |
| `einheitskreis` | – | `winkel` (Grad, Standard 30), `regler`, `zeige: [sin, cos, tan, kurve]`, `bogenmass` (Standard true) | Punkt (cos α, sin α) ziehbar/Regler/Tasten, Projektionen, tan an x = 1, sin-/cos-Kurve daneben; `_tabelle`: exakte Werte für alle Vielfachen von 15° |
| `exp_log` | – | `basis` (Standard 2, auch `"e"`, `"1/2"`), `umkehr` (Standard true), `regler`, `x`, `y` | $a^x$ und $\log_a x$ mit Spiegelachse $y = x$, Punkte (0\|1), (1\|a), (1\|0), (a\|1), gespiegeltes Punktpaar P/P'; Regler für die Basis |
| `tangente` | `term`, `x0` | `h` (Standard 1), `ableitung` (Term, empfohlen), `sekante` (Standard true), `x`, `y` | Sekante durch x0 und x0 + h, Steigungsdreieck, Tangente, Regler x0/h, Knopf „h → 0“; `ableitung` wird per Differenzenquotient-Stichprobe gegengeprüft (Abweichung = Schemafehler); exakt: `_y0_tex`, `_m_tex`, `_m_sek_tex`, `_tangente_tex` |
| `riemann` | `term`, `von`, `bis` | `n` (Standard 4), `n_max` (Standard 50), `art: links\|rechts\|mitte\|unter\|ober`, `stammfunktion` (Term), `x`, `y` | Rechtecke, Regler n, Umschalter für die Art; `_summe` exakt für Startwerte; mit `stammfunktion` (gegengeprüft: F' = f) exakter Integralwert `_integral` |
| `vektoren2d` | `vektoren[{x, y, label?, farbe?: 1-4}]` (1–4) | `zeige: [summe, differenz, kette, vielfaches, norm, skalarprodukt]`, `faktor` (λ, Standard 2), `interaktiv` (Spitzen ziehbar, Tab + Pfeiltasten), `x`, `y` | Pfeile, Parallelogramm/Pfeilkette, λ·a mit Regler, Normen und Skalarprodukt exakt (auch nach dem Ziehen, Raster 0,5) |
| `matrix_mult` | `a`, `b` (Listen von Zeilen) | – | Falk-Schema, Zeile·Spalte Schritt für Schritt hervorgehoben, Einträge von C anklickbar; `_summanden`, `_rechnungen`, `_c` exakt |
| `gauss` | `matrix` | `rechts` (Vektor → erweiterte Matrix), `reduziert` (Standard true) | Zeilenumformungen Schritt für Schritt (Vor/Zurück), Pivot markiert, geänderte Zeilen hervorgehoben; am Ende Rang und `_loesung_tex` |
| `komplexe_ebene` | `z: [Re, Im]` **oder** `punkte` | `w: [Re, Im]`, `op: keine\|konjugiert\|plus\|minus\|mal\|geteilt` (Standard mal mit w, sonst keine), `interaktiv`, `x`, `y` | Zeiger, Betrag/Argument mit Winkelbögen, Spiegelung, Parallelogramm, Drehstreckung; zusätzlich `punkte[{z: [Re, Im], label?, farbe?: 1-4}]` (auch einfach `[Re, Im]`; 1–8 Zahlen als Pfeile von 0, mit `pfeile: false` nur als Punkte; `label` ist LaTeX, Standard `z_{i}`), `konjugiert` (gestrichelte Spiegelpunkte \(\bar z\)), `betragskreis` (Kreis mit Radius \|z\| je Zahl); ohne `z` zeigt der Typ nur die `punkte` (`_punkte[{re, im, tex, betrag_tex, konj_tex, …}]`, `_alt`); exakte Polarform (`_z`, `_w`, `_ergebnis`: `tex`, `betrag_tex`, `arg_tex`, `polar_tex`), Einträge wie `"sqrt(3)"` erlaubt |
| `venn` | `mengen[{name, elemente}]` (2–3 Mengen, Elemente Zahlen/kurze Texte) | `universum` (Liste, enthält alle Elemente), `universum_name` (Standard „G“), `markiert` (Mengenausdruck: `∩ ∪ \ ` bzw. `\cap \cup \setminus`, Komplement als `Komplement A`, `A'`, `A^c`, `\overline{A}`, Klammern), `interaktiv` (Standard true) | Elemente in ihren Regionen; markierte Fläche farbig; Fläche antippen/Tab + Pfeiltasten zeigt Formel und Elemente. Python: `_regionen[{maske, elemente, tex, elemente_tex}]`, `_markiert` (Masken), `_markiert_tex`, `_markiert_elemente` |
| `relation_graph` | `links`, `rechts` (je 1–10 Elemente), `pfeile[[l, r], …]` | `namen` (Standard `["A", "B"]`), `zeige` (Teilmenge von `abbildung, injektiv, surjektiv, bijektiv`), `aufdecken` (Ergebnisse erst nach „Auflösen“) | Pfeildiagramm; Eigenschaft antippen markiert Verstöße rot mit kurzer Erklärung. Python: `_abbildung` (jedes Element links genau ein Pfeil), `_injektiv`/`_surjektiv`/`_bijektiv` (`null`, wenn keine Abbildung), `_verstoesse[{eigenschaft, seite, element, pfeile, text}]` |
| `wahrheitstabelle` | `variablen` (1–4), `ausdruecke` (¬ ∧ ∨ ⇒ ⇔ ⊕, Rangfolge ¬ vor ∧ vor ⊕ vor ∨ vor ⇒ vor ⇔, ⇒ rechtsassoziativ; auch `! & \| -> <-> and or not xor`) | `darstellung: wf` (Standard, w/f wie im Vorkurs) `\| 01`, `markiert` (Ausdrücke als Text oder Index ab 0), `schrittweise` (Standard true: Spalten einzeln aufdecken) | Python: `_kopf`, `_zeilen[{werte, ergebnisse}]`, `_art` (tautologie/kontradiktion/erfuellbar je Spalte), `_gleich` (Paare gleicher Spalten = äquivalent), `_markiert` |
| `induktion_domino` | – | `anzahl` (3–12, Standard 8), `anfang` (n₀, Standard 1), `aussage` (Markup), `text_anfang`, `text_schritt` (Markup) | Dominokette: Knöpfe Induktionsanfang (erster Stein fällt, IA), Induktionsschritt (k stößt k+1 um, IS), alle fallen; ohne Animation bei reduzierter Bewegung |
| `beweisbaum` | `wurzel` | | geplant |
| `modulo_uhr` | `n` (2–36) | `start` (a), genau eins von `plus` (b: Sprung a → a+b), `mal` (b Sprünge der Weite a ab 0), `potenz` (k: a, a², …, aᵏ mod n); `interaktiv` (Regler für n, a, b) | Uhr mit n Positionen, Sprünge als Bögen/Sehnen (animiert), Ergebnis grün. Python: `_ergebnis`, `_spruenge[[von, bis, x]]`, `_tex` (z. B. `7 + 8 = 15 \equiv 3 \pmod{12}`), `_rechnung` (Division mit Rest), `_potenzen[{exp, wert, tex}]` |
| `euklid` | `a`, `b` (positive ganze Zahlen) | `erweitert` (Rückwärtseinsetzen) | Tabelle der Divisionen mit Rest Schritt für Schritt (Vor/Zurück/Alles), dann ggT, dann Rückwärtseinsetzen mit Probe. Python: `_schritte[[a, b, q, r]]`, `_ggt`, `_rueckwaerts[{tex, text}]`, `_bezout{s, t, tex}` |
| `pascal` | – | `zeilen` (1–16, Standard 7), `markiert[[n, k], …]` (Zeile und Stelle ab 0), `interaktiv` (Standard true) | Dreieck; gewählte Zelle zeigt die beiden Zahlen darüber und $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$. Python: `_zeilen`, `_markiert[{n, k, wert, tex}]` |
| `folge` | `term` (in `n`) **oder** `start` + `rekursion` (in `a` = Vorgänger aₙ und `n`; ergibt aₙ₊₁) | `n_von` (Standard 1; bei Rekursion Index von `start`), `n_bis` (Standard n_von+19, höchstens 200 Glieder), `grenzwert`, `epsilon` (braucht `grenzwert`), `interaktiv` (ε-Regler, Standard true), `monotonie`, `schranken`, `y` | Punkte (n, aₙ), Grenzwert-Linie, ε-Schlauch, senkrechte Linie bei n₀. Python: `_werte`, `_tex`, `_n0` (kleinstes n₀, ab dem alle Glieder im Schlauch liegen; exakt mit Brüchen, nachgeprüft bis `_n0_bis` = 10 000; `null`, wenn es keins gibt), `_monotonie`/`_schranken` (nur für den gezeigten Bereich) |
| `graph_gerichtet` | `elemente` (1–16; Zahlen, Texte, Listen = Mengen, `[]`/`"∅"` = leere Menge), `paare[[a, b], …]` | `layout` (`"kreis"` Standard, `"zeilen"` oder `{Element: [x, y]}` mit y nach oben), `markiert` (Elemente und/oder Pfeile `[a, b]`) | Relation auf **einer** Menge als gerichteter Graph: Kreise, Pfeile mit Spitze, Schleifen nach außen, gegenläufige Paare als zwei Bögen. Python prüft, dass alle Paarglieder Elemente sind (keine doppelten Elemente/Paare). `_knoten[{text, tex, x, y}]`, `_kanten[[von, nach]]` (Indizes), `_markiert_knoten`, `_markiert_kanten`, `_alt` |
| `hasse` | `elemente` (1–20), `paare[[a, b], …]` (a ≼ b; auch volle Relation mit Reflexiv- und Abkürzungspaaren erlaubt) | `teilmenge` (schwarz, Rest ausgegraut), `sup`, `inf` (Markierung orange/grün, braucht `teilmenge`), `schranken` (obere/untere Schranken gestrichelt) | Hasse-Diagramm: Python bildet den reflexiv-transitiven Abschluss (Antisymmetrie verletzt = Fehler), die transitive Reduktion und Schichten nach Höhe (kleinste unten, Schwerpunktverfahren gegen Kreuzungen). `_knoten` (mit `ebene`), `_kanten` (Überdeckungen [klein, groß]), `_ebenen`, `_ordnung`, `_teilmenge`, `_obere`, `_untere`, `_sup`, `_inf` (Index oder `null`), `_info` (Markup-Zeilen, z. B. `$\\sup T = \\{1, 2\\}$`), `_alt` |
| `aequivalenz_klassen` | `klassen[[…], …]` (1–8 disjunkte, nichtleere Listen, höchstens 24 Elemente) | `elemente` (muss genau die Elemente der Klassen sein), `repraesentanten` (höchstens einer je Klasse, Standard: erstes Element; ausgefüllt), `namen` (LaTeX je Klasse, Standard `[Vertreter]`), `graph` (Pfeile zwischen allen Elementen einer Klasse: Schleifen und Doppelpfeile, höchstens 4 Elemente je Klasse) | Elemente in farbigen Bereichen je Klasse, darunter `[a] = {…}` als Formelliste. `_knoten[{text, tex, x, y, klasse, vertreter}]`, `_klassen[{name, name_tex, x, y, r, knoten, tex}]`, `_kanten`, `_alt` |
| `binaer`, `kombi_baum`, `urne` | siehe `visuals.SCHEMA` | | geplant |
| `vektoren3d`, `gerade_ebene`, `lgs_geometrie`, `transformation2d` | siehe `visuals.SCHEMA` | | geplant |
| `reihe`, `stetigkeit`, `ableitung_graph`, `kurvendiskussion`, `flaeche_integral`, `landau`, `graph`, `baum` | siehe `visuals.SCHEMA` | | geplant |

Layout-Koordinaten der Relations-Visuals (`graph_gerichtet`, `hasse`, `aequivalenz_klassen`) liefert Python (Einheiten, y nach unten); das Frontend (`vis_ordnung.js`) skaliert und zeichnet. In `demo.py` darf ein Typ eine Liste von Beispielen haben.

Die Felder aller Typen stehen maschinenlesbar in `visuals.SCHEMA`. Die Demo-Seite `#/demo/visuals`
zeigt jeden fertigen Typ mit den Beispieldaten aus `mathe/demo.py`. Mit jeder Welle wandern Typen
von „geplant“ nach `VISUAL_FERTIG`, und diese Tabelle wird ergänzt.

## 5. Engine und Prüflogik

- `frage.instanz(seed)` → konkrete Frage (Generatoren: neue Zahlen; sonst die Frage selbst).
- `konkret.to_dict()` → JSON ohne Lösung: `id, typ, art, phase (ueben|praxis), kapitel, frage, tipps,
  uebungsblatt, punkte, hat_rechenweg, eingabe, seed` + typspezifisch.
- `konkret.pruefen(antwort)` → `Ergebnis{ok, meldung, loesung (Markup), erklaerung, rechenweg, details,
  hinweis, fehler_erkannt, fast, lesefehler, teilpunkte}`.
  - `lesefehler`: Eingabe nicht lesbar → **zählt nicht als Versuch**.
  - `fehler_erkannt`: ein typischer Fehler passt; `hinweis` sagt, was vermutlich passiert ist.
  - `fast`: Wert stimmt, Form nicht (nicht gekürzt, nicht ausmultipliziert, kein Bruch …).
  - Ohne passenden typischen Fehler gibt es automatische Hinweise (Vorzeichen, Kehrwert, Komma
    verschoben, zu früh gerundet, Probe mit konkretem Wert, fehlende Lösung, offene/geschlossene Grenze).
- `engine.musterantwort(konkret)` → richtige Antwort im Oberflächenformat (Selbsttest, E2E).

**Term-Grammatik (pruefer.py):** Zahlen mit `,` oder `.`; `+ - − * × · / ÷ : ^ ² ³ !`; `( ) [ ]`;
`|x|`; `sqrt √ abs sin cos tan ln log2 log10 exp`; `pi π e` (Konstante e!); implizites Mal (`2x`,
`3(x+1)`, `2pi r`); `-x^2 = -(x^2)`; `^` rechtsassoziativ; `log` ohne Basis ist ein Lesefehler mit Hinweis.
Kein `eval`: Tokenizer + rekursiver Abstieg → AST aus Tupeln; Grenzen für Länge, Tiefe, Exponent.

**Formchecks** (`form=` bei `term`/`vereinfache`, `formen=[…]` je Lücke bei `luecke`, mehrere mit `|`):
`ausmultipliziert`, `faktorisiert`, `ohne_klammern`, `gekuerzt` (Zahlbruch bzw. Polynombruch),
`wurzel_vereinfacht` (kein Quadratfaktor unter √, keine ganz ausrechenbare Wurzel, keine Wurzel im Nenner),
`potenz` (jede Basis einmal pro Produkt, keine Potenz einer Potenz), `ggt_ausgeklammert` (Zahl·Klammer, Klammer
ganzzahlig mit ggT 1 und ohne gemeinsames x), `linearfaktoren` (zerfällt über ℚ nicht weiter), `vereinfacht` (alles davor außer
ausmultipliziert/faktorisiert, Zahlen zusammengerechnet, nicht deutlich länger als die Lösung).
`ohne_gleiche(loesung, fehler)` filtert auch Terme und Lücken-Listen. Zahlfragen und Lücken mit rationaler
Lösung verlangen automatisch einen ausgerechneten Wert (`3,45*100` → „Fast!“). Einheiten-Synonyme: € = Euro,
% = Prozent, ° = Grad, GB/MB/kB ausgeschrieben. In Mengen und Lösungsmengen versteht der Prüfer `±`
(`±5`, `x = ±5`, `2 ± sqrt(3)`, `{±1; ±2}`). Angezeigte Mengen trennen mit Komma (TU-Stil), mit `;` nur bei Dezimalzahlen.

**`:::rechnung`-Zeilen:** `!` = absichtlich falscher Schritt („So nicht!“); `#` = Widerspruch ohne
Variable (z. B. `1 = 5`), daraus folgt $\mathbb{L} = \emptyset$; davor stehende Gleichungen werden dann
auf „keine Lösung“ geprüft. Endet eine Rechnung mit `v = Term` (Term mit anderen Variablen), gilt sie
als Formelumstellung: jede Zeile wird nach Einsetzen von `v` auf Äquivalenz geprüft.

**Komma-Regel** (Mengen, Lösungsmengen, Intervalle): Enthält die Eingabe `;`, trennt `;` und `,` ist
Dezimalkomma. Sonst trennt `,` und Dezimalzahlen brauchen `.`. Die Vorschau zeigt die Deutung.

## 6. Kapitelmodule und Mindestanforderungen (vom Selbsttest geprüft, Fehler!)

Dateiname: `f<NN>_<slug>.py` (Fundament), `v<NN>_<slug>.py` (Vorkurs), `m1_<NN>_…`, `m2_<NN>_…`, `b_<NN>_…`, `k_<NN>_…`.

Lernpfad je Kapitel: Lernziele (+ Warum) → (Erklärseite → 1–3 Fragen dazu) × n → `k.praxis()` →
Praxisaufgaben leicht → schwer, zuletzt Übungsblatt-Stil → Merkzettel.

| Regel | |
|---|---|
| 3–5 Lernziele, Warum-Text, mind. eine `:::achtung`-Box | |
| 4–10 Erklärseiten, **jede** mit `:::rechnung` oder `:::visual` **und** `:::alt` | |
| höchstens 120 Wörter Fließtext pro Seite (Warnung), ab 170 Fehler | Formeln, Rechnungen, Visuals und `:::alt` zählen nicht |
| 6–14 Üben-Fragen, davon mind. 3 mit Fehlererkennung (`typische_fehler` oder `fehler=`) | |
| mind. 1 Generator (außer `rechenthema=False`) | |
| mind. 2 Praxisaufgaben, davon mind. 1 mit `uebungsblatt=True` | |
| Merkzettel | |
| jede Frage: Erklärung oder Rechenweg; mind. 2 Tipps (wf/zuordnen/papier: 1); Rechenfragen: Rechenweg | |
| Glossar: jeder `[[Begriff]]` existiert im Glossar; neue Begriffe in `inhalte/_glossar_<datei>.py`; kein Begriff doppelt | |
| `quelle` gesetzt | |

Kapitel mit `teil="klausur"` sind Aufgabenpools: dort gelten nur die Regeln für Fragen.

**Didaktik (für alle Autoren verbindlich):** ein Gedanke pro Seite; Reihenfolge Alltagsbild →
vorgerechnetes Beispiel (jeder Zwischenschritt mit Begründung) → „Jetzt du“ mit fast derselben
Aufgabe → leicht verändert → schwerer. Nie einen Schritt überspringen. Jeder Fachbegriff beim ersten
Auftreten erklärt und als `[[…]]` verlinkt. `:::alt` erklärt mit einem **anderen** Bild, nicht umformuliert.
Deutsch, Du-Form, kurze Sätze, kleine Zahlen. Keine Floskeln, keine Gedankenstriche als Stilmittel.
Vereinfachungen müssen stimmen und werden später präzisiert. Beweise: jeder Schritt begründet,
Induktionsanfang, -voraussetzung und -schritt ausdrücklich benannt.

**Mathe 1 folgt dem Skript von Prof. Disser (WS 26/27):** Notation, Begriffe und Satznummern siehe LEHRPLAN.md, Abschnitt Mathe 1. Bei Widerspruch zu den Regeln unten gilt dort das Skript.

**Notation (wie an der TU Darmstadt):** Dezimalkomma; Intervalle mit runden Klammern $(a, b]$
(die Schreibweise $]a, b]$ wird erwähnt); Malpunkt `\cdot`; Abbildungen $f\colon D \to W,\ x \mapsto \ldots$;
Folgen $(a_n)_{n \in \mathbb{N}}$; Mengen mit Doppelpunkt $\{x \in \mathbb{R} : x > 0\}$.
**$\mathbb{N}$ hängt vom Teil ab, weil die TU-Unterlagen sich hier unterscheiden:**
- Fundament und Vorkurs (Vorkurs-Folien 2026): $\mathbb{N} = \{1, 2, 3, \ldots\}$, $\mathbb{N}_0 = \{0, 1, 2, \ldots\}$.
- Mathe 1 und 2 (Skript Mathe I/II): $\mathbb{N} = \{0, 1, 2, \ldots\}$, $\mathbb{N}^* = \{1, 2, 3, \ldots\}$.
- Aufgaben dürfen von dieser Wahl nie abhängen. Schreibe im Zweifel $\mathbb{N}_0$, $\mathbb{N}^*$ oder „$n \ge 1$“.
  Das Kapitel „Mathematik lesen“ und das erste Mathe-1-Kapitel erklären den Unterschied in einer `:::achtung`-Box.

## 7. Fortschritt (fortschritt.py)

Speicherort `~/.mathe_quiz/fortschritt.json`; Umgebungsvariable `MATHE_QUIZ_DATEN` (Ordner) überschreibt
(**Tests müssen sie setzen**); ist der Ordner nicht beschreibbar: `<Programmordner>/mathe_quiz_fortschritt.json`.
Atomares Speichern (`.tmp` + `os.replace`), Thread-Lock, defekte Datei wird als `.defekt.json` gesichert.

```json
{"version": 1, "kapitel": {"<slug>": {"best", "max", "abgeschlossen", "zuletzt"}},
 "fragen": {"<id>": {"richtig", "falsch", "zuletzt", "kasten", "loesung_angesehen"?}},
 "fehlerkiste": ["<id>"], "klausuren": [{"modul", "datum", "punkte", "max", "note", "dauer"}],
 "entwuerfe": {"<id>": "Text"}, "xp": 0, "serie": {"tage", "zuletzt"}, "abzeichen": ["<id>"],
 "diagnose": {"datum", "ergebnis", "empfehlung"} | null, "papier": {"<id>": {"punkte", "max", "datum"}},
 "generatoren": {"<id>": anzahl_geloest},
 "einstellungen": {"theme", "schrift": s|m|l|xl, "animationen", "pause_hinweis", "pause_minuten", "begruessung_gesehen"},
 "meta": {}}
```

- XP: 1. Versuch +10, 2. Versuch +5, erneut gelöst +2, weitere Generator-Instanz +3, Papier +5 je
  neu abgehaktem Punkt, Kapitel +50 (erstes Mal), Diagnose +30 (erstes Mal).
- Level (0, 100, 250, 500, 900, 1400, 2000, 2800, 3800, 5000): Zahlenneugier, Bruchsicher,
  Termgewandt, Gleichungsklar, Funktionsblick, Beweislust, Matrixkraft, Grenzwertgespür,
  Integralgefühl, Mathe-Profi (geschlechtsneutral).
- Leitner-Kasten 1–5 (fällig nach 0/1/2/4/8 Tagen). Falsch (endgültig) → Kasten 1 + Fehlerkiste.
- **Meisterschaft je Kapitel** = Abdeckung × (0,6 · Trefferquote + 0,4 · mittlere Kasten-Stufe);
  Stufen neu < angefangen (>0) < sicher (≥ 0,6) < gemeistert (≥ 0,85).

## 8. Weitergabe

Der ganze Ordner `mathe_tuda/` kann kopiert oder gezippt werden (ohne `__pycache__`). Wer ihn bekommt,
braucht nur Python ≥ 3.10. Der persönliche Fortschritt bleibt im Benutzerordner.

## 9. Web-API (web/server.py)

`ThreadingHTTPServer` auf 127.0.0.1, Port 8766 (belegt → nächster freier). Host- und Origin-Prüfung,
keine CORS-Freigaben. Statische Dateien unter `/static/`. Antworten JSON, Fehler `{"fehler": text}`.
Lösungen gehen erst nach dem letzten Versuch oder über `/api/loesung` an den Client.

| Methode & Pfad | Body / Query | Antwort |
|---|---|---|
| GET `/api/uebersicht` | | `{teile[{…, kapitel[to_dict + fortschritt]}], statistik, einstellungen}` |
| GET `/api/kapitel/<slug>` | | `{kapitel, elemente[erklaerung\|frage\|zusammenfassung]}` |
| GET `/api/generator/neu?id=` | | `{frage}` neue Instanz |
| GET `/api/training?modus=wiederholen\|fehlerkiste\|thema\|klausur&kapitel=&modul=&anzahl=` | | `{fragen}` |
| GET `/api/diagnose` | | `{fragen, letzte}` |
| GET `/api/formelsammlung`, `/api/glossar`, `/api/status`, `/api/demo/visuals` | | |
| POST `/api/antwort` | `{id, seed?, antwort, versuch, schritt?, bisher?}` | Ergebnis + `xp_neu, neue_abzeichen, statistik, zweiter_versuch, final` |
| POST `/api/loesung` | `{id, seed?}` | `{loesung, rechenweg, erklaerung (+ _bloecke)}`; zählt als angesehen |
| POST `/api/papier/loesung` | `{id}` | `{musterloesung, checkliste}` (kein Abzug) |
| POST `/api/term/vorschau` | `{text, typ: zahl\|term\|bereich\|menge, variablen?, ast?}` | `{latex, fehler, pos, ast?}` – derselbe Parser wie beim Prüfen |
| POST `/api/kapitel/<slug>/abschluss` | `{punkte, max}` | |
| POST `/api/klausur/ergebnis` | `{modul, punkte, max, dauer}` | `{note}` |
| POST `/api/diagnose/ergebnis` | `{ergebnisse: {slug: [richtig, gesamt]}}` | Auswertung + Empfehlung |
| POST `/api/spielwiese/<bruch\|matrix\|lgs\|primfaktoren\|basis>` | Werkzeug-Daten | `{ergebnis (LaTeX), rechenweg}` |
| POST `/api/entwurf`, `/api/einstellungen`, `/api/fortschritt/zuruecksetzen`, `/api/beenden` | | |
| GET `/api/e2e/antwort`, `/api/e2e/formeln`; POST `/api/e2e/bericht` | nur mit `--e2e` | |

## 10. Selbsttest (`python3 mathe_quiz.py --selbsttest`)

Exit-Code 0 nur ohne Fehler. Geprüft wird:
- Prüfer-Batterie: äquivalente und nicht äquivalente Termpaare werden richtig erkannt.
- Jede Musterlösung besteht ihren eigenen Prüfer (auch jeder Rechenweg-Schritt).
- Jeder typische Fehlwert ist **nicht** richtig, ist lesbar und löst seine Meldung aus.
- Jeder Generator läuft mit 200 Seeds ohne Ausnahme; `glatt`; eigene `probe`; Vielfalt der Aufgaben.
- **Jede `:::rechnung` wird nachgerechnet** (in Erklärungen, Rechenwegen, Generator-Ausgaben):
  Ketten ohne Variablen exakt; Termumformungen per Äquivalenz; Gleichungsketten durch Einsetzen der
  Lösung aus den letzten Zeilen; Ungleichungsketten durch Vergleich der Wahrheitswerte an vielen Stellen.
  Nicht übersetzbare Zeilen werden als „nicht automatisch prüfbar“ gezählt.
- `vereinfache()`/`gleichung()`: Ausgangsterm ≡ Lösung, Form erfüllt, Autor-Lösung = berechnete.
- Alle Formeln gültig (Python-Validator; mit Node zusätzlich echtes KaTeX; sonst `?e2e=formeln`).
- Visual-Schemata, Steuerzeichen (vergessener r-String), Glossar-Verweise, eindeutige IDs,
  Mindestanforderungen je Kapitel (Abschnitt 6), Demo-Visuals.

Zusätzlich gibt es den E2E-Test im Browser (`mathe_quiz.py --gui --e2e`, dann `?e2e=kapitel|training|werkzeuge|formeln`),
der jedes Kapitel über die echte Oberfläche durchspielt.

## 11. Inhaltsprüfung durch Subagenten

Nach jeder Kapitelgruppe rechnet ein **separater Prüf-Subagent** jede Aussage, jede Rechnung und jede
Lösung unabhängig nach und meldet Fehler, Ungenauigkeiten und Lücken im Aufbau. Alles wird behoben,
bevor es weitergeht. Der Autor-Agent prüft sich nicht selbst ab.
