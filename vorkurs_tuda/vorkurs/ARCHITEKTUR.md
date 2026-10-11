# Vorkurs-Lernquiz v2 – Architektur & Vertrag

Diese Datei ist der verbindliche Vertrag zwischen allen Teilen des Programms.
Wer etwas baut, hält sich an diese Schnittstellen. Änderungen am Vertrag nur
mit Absprache (Teamleiter).

Ziel: Lernprogramm für komplette Anfänger zum Python-Vorkurs der TU Darmstadt.
Zwei Oberflächen (Terminal + Browser-GUI) teilen sich EINE Engine und EINEN
Inhaltsbestand. Nur Python-Standardbibliothek (Python >= 3.10), keine
Zusatzpakete, keine CDNs – alles läuft offline.

## 0. Weitergabe an andere (Portabilität)

Der Programmordner wird als Ganzes an andere Personen weitergegeben. Deshalb:
- NUR Standardbibliothek. Es gibt keine pip-Pakete und nichts aus dem Internet,
  auch keine Schriftarten oder CDNs. Python >= 3.10 ist die einzige Voraussetzung.
- `vorkurs/umgebung.py`: `pruefen() -> list[str]` (Probleme) prüft beim Start
  Python-Version (>= 3.10), Schreibrechte für den Fortschrittsordner,
  Vorhandensein von web/static/*, Konsolen-Encoding. Der Starter zeigt klare
  deutsche Anleitungen bei Problemen. Falls später jemand optionale Pakete
  einführt: Liste `OPTIONALE_PAKETE` dort pflegen; fehlende werden beim Start
  mit `python -m pip install --user <paket>` nach Rückfrage installiert. Aktuell ist
  die Liste LEER und muss leer bleiben.
- Start-Skripte im Hauptordner (Doppelklick):
  - `Start.bat` (Windows): sucht `py -3`, dann `python`, dann `python3`, und prüft
    die Version >= 3.10. Fehlt Python, bietet es nach Rückfrage
    `winget install -e --id Python.Python.3.12` an (sonst Link python.org)
    und startet danach `vorkurs_quiz.py`. Die Datei braucht Zeilenenden CRLF,
    nur ASCII-Zeichen in Befehlen und `chcp 65001`.
  - `Start.command` (macOS) und `start.sh` (Linux): nutzen python3, prüfen die
    Version und geben sonst Installationshinweise (python.org / brew /
    apt). Zeilenenden LF. Ausführbarkeit wird in der LIESMICH erklärt.
- `LIESMICH.md` im Hauptordner: Start, Bedienung, Voraussetzungen, Weitergabe.
- Pfade nie hart kodieren; alles relativ zu `Path(__file__)`. Dateinamen im
  Paket nur ASCII (keine Umlaute).
- Fortschritt liegt NICHT im Programmordner (siehe Abschnitt 8), damit eine
  Weitergabe keinen persönlichen Stand mitschickt.

## 1. Ordnerstruktur

```
Start.bat / Start.command / start.sh / LIESMICH.md
vorkurs_quiz.py                 Starter: fragt "Terminal oder Grafisch?"
                                Optionen: --terminal, --gui, --selbsttest,
                                --keine-farben, --port N, --kein-browser
vorkurs/
  __init__.py
  ARCHITEKTUR.md                diese Datei
  engine.py                     Datenmodell, Fragetypen, Prüflogik, Kapitel
  markup.py                     Parser für Erklärungstexte -> Blöcke
  sandbox.py                    Code in eigenem Prozess ausführen, Tests, Tracer
  fortschritt.py                Laden/Speichern/Migration, XP, Serie, Abzeichen
  selbsttest.py                 prüft ALLE Inhalte automatisch
  inhalte/
    __init__.py                 lädt alle Kapitelmodule in fester Reihenfolge
    t1_01_computer.py ...       ein Modul pro Kapitel (siehe Abschnitt 6)
    spickzettel.py              SPICKZETTEL (Markup-Text)
  terminal/
    __init__.py
    app.py                      Terminal-Oberfläche (main())
    render.py                   Markup-Blöcke & Visuals als Text/ASCII
  web/
    __init__.py
    server.py                   http.server + JSON-API (main())
    static/index.html, app.css, app.js, editor.js, visuals.js, ...
```

## 2. Inhalte schreiben (API für Kapitelmodule)

Jedes Kapitelmodul sieht so aus:

```python
from ..engine import neues_kapitel, P, F

k = neues_kapitel(
    slug="variablen",                      # eindeutig, stabil, a-z0-9_
    titel="Variablen – Beschriftete Kisten",
    beschreibung="Werte speichern, überschreiben, benennen",
    quelle="Vorlesung 1, Übung 1",
    teil="tag1",                           # siehe TEILE in engine.py
    icon="📦")                             # ein Emoji für die GUI

k.lernziele(["Ich kann einer Variable einen Wert zuweisen", ...])

k.erklaerung("Titel", r"""  ...Markup (Abschnitt 3)...  """)
k.mc(frage, [richtig, falsch1, falsch2, ...], erklaerung, code=None, tipp=None)
k.wf(aussage, wahr: bool, erklaerung, code=None, tipp=None)
k.text(frage, [akzeptierte Antworten], erklaerung, tipp=None, code=None, gross_klein=False)
k.ausgabe(code, erklaerung, tipp=None, akzeptiert=(), frage=None)
k.ausdruck(frage, tests=[{var: wert}, ...], loesung="ausdruck", erklaerung, tipp=None, muss_enthalten=None)
k.luecke(frage, code_mit_luecken, [[akzeptiert für Lücke 1], [für Lücke 2], ...], erklaerung, tipp=None)
k.puzzle(aufgabe, loesungscode, erklaerung, tipp=None, ablenker=())
k.code(aufgabe, tests=[P(...), F(...)], loesung, erklaerung, tipp=None, vorlage=None,
       verboten=(), pflicht=(), rekursiv=None, tipps=None, regeln=(), streng=False)
k.zusammenfassung(r"""Markup: das Wichtigste der Lektion auf einen Blick""")
```

Bedeutung der neuen Elemente:
- `lernziele`: 2–5 "Ich kann ..."-Sätze, werden am Kapitelanfang gezeigt.
- `text(..., gross_klein=True)`: Groß-/Kleinschreibung zählt beim Vergleich (z. B.
  `python3 -V` vs. `python3 -v`). Standard: egal. Die Oberflächen weisen darauf hin;
  eine nur in Groß/klein abweichende Antwort bekommt einen „Fast!“-Hinweis.
- `luecke`: Lückencode. Im Code steht `___` (drei Unterstriche) für jede Lücke.
  Pro Lücke eine Liste akzeptierter Antworten (Vergleich mit norm_text:
  Groß/klein egal? NEIN – bei Code zählt Groß/klein; nur Leerzeichen außen
  egal und Leerzeichen innen normalisiert). Antworten-Liste hat genau so
  viele Einträge wie es `___` gibt.
- `puzzle`: Code-Puzzle (Parsons-Problem). `loesungscode` ist korrekt
  eingerückter Code; die Zeilen werden gemischt angezeigt (mit Einrückung).
  `ablenker` = zusätzliche falsche Zeilen, die NICHT verwendet werden dürfen.
  Richtig ist eine Reihenfolge, wenn die zusammengesetzten Zeilen exakt dem
  Lösungscode entsprechen ODER (falls ohne input()) dieselbe Ausgabe erzeugen.
- `code`: Programmieraufgabe mit automatischen Tests.
  - `verboten`: Liste von Textstücken, die im Code NICHT vorkommen dürfen
    (z. B. ["%", "/", "[::-1]", ".reverse("]). Kommentare/Strings werden
    dabei ignoriert (Prüfung über tokenize).
  - `pflicht`: Textstücke, die vorkommen MÜSSEN (z. B. ["def ", "while"]).
  - `rekursiv`: Funktionsname, der sich selbst aufrufen muss (AST-Prüfung).
    Alternativen mit `|`: `rekursiv="even|odd"` – eine der Funktionen muss
    existieren und sich selbst aufrufen.
  - `regeln`: eingebaute AST-Regeln mit deutschen Meldungen (statt Nachspann-
    Tricks, siehe unten). Die Musterlösung muss sie erfüllen (Selbsttest).
  - `streng`: Vorgabe für ALLE P-Tests der Aufgabe: `erwartet` und `anzahl`
    beachten dann Groß/klein und Satzzeichen (einzelne Tests: `P(..., streng=...)`).
  - `tipps`: Liste gestufter Tipps (Tipp 1 vage … Tipp 3 fast Lösung).
    `tipp` (einzeln) bleibt erlaubt; intern wird daraus tipps=[tipp].
  - `vorlage`: Startcode, der im Editor vorausgefüllt ist (auch für
    "Finde den Fehler"-Aufgaben: fehlerhafter Code als Vorlage).
- `zusammenfassung`: wird als "Merkzettel" am Ende des Kapitels gezeigt
  und ist im Spickzettel-Bereich pro Kapitel abrufbar.

Didaktische Reihenfolge pro Kapitel (Lernpfad "Erklären → Quiz → Coden"):
  lernziele → (erklaerung → 2–6 Verständnisfragen) × n → Praxisteil mit
  2–4 Programmieraufgaben (`code`, `puzzle`, `luecke`), vom leichten zum
  schweren → zusammenfassung.
Die GUI erkennt die Phase am Elementtyp: Erklärung = "Verstehen",
mc/wf/text/ausgabe/ausdruck = "Üben", code/puzzle/luecke = "Programmieren".

Test-Helfer:
- `P(eingaben=(), erwartet=(), nicht=(), exakt=None, vorspann="", nachspann="",
  beschreibung=None, streng=None, anzahl=None, leerzeichen=False, mit_aufforderung=False)`
  Programmtest: Eingaben gehen an input() (ohne Echo). Der Aufforderungstext von
  `input("Zahl: ")` wird in Tests standardmäßig NICHT ausgegeben, er klebt also nicht
  an der nächsten Ausgabezeile und stört `exakt` nicht. `erwartet` prüft trotzdem das
  ZEILENENDE (die Ausgabe kann ja mit `print(..., end="")` zusammengesetzt sein).
  - `mit_aufforderung=True`: der Aufforderungstext bleibt in der geprüften Ausgabe
    (wie in v1), für Tests, die ihn bewusst prüfen (`erwartet=["Wie heißt du?"]` o. Ä.).
    Alte Vorspann-Tricks, die `input` ohne Aufforderung ersetzen, funktionieren weiter.
  - `erwartet`: Texte, mit denen je eine Ausgabezeile ENDEN muss (davor steht der
    Zeilenanfang oder ein Nicht-Wortzeichen). Ein Element darf ein **Tupel von
    Alternativen** sein: `erwartet=[("210", "210.0")]`.
  - `exakt`: genaue Zeilenliste, IMMER STRENG.
  - `nicht`: Texte, die in keiner Zeile vorkommen dürfen.
  - `anzahl`: `{"Falsch!": 3}` – der Text kommt insgesamt genau so oft vor
    (alle Vorkommen in allen Zeilen, auch als Teil einer Zeile).
  - `streng`: None = Vorgabe der Aufgabe (`k.code(..., streng=...)`, Standard
    False); True = auch `erwartet`/`anzahl` streng; False = auch `exakt`
    tolerant (altes v1-Verhalten, nur für Sonderfälle).
  - `leerzeichen=True`: führende Leerzeichen (Einrückung) zählen bei `exakt`
    (und bei strengem `erwartet`), z. B. für eine Kopfzeile `"  1 2 3"`.

  Vergleichsregeln:

  | Prüfung | Groß/klein | Satzzeichen | Leerzeichen |
  |---|---|---|---|
  | `erwartet` tolerant (Standard) | egal | `.!?:` am Zeilenende egal | außen egal, mehrfache = eins |
  | `erwartet` streng | zählt | zählen | außen egal, mehrfache = eins |
  | `exakt` (immer streng) | zählt | zählen | im Text exakt; am Zeilenende egal, am Zeilenanfang egal außer mit `leerzeichen=True`; Leerzeilen nur am Anfang/Ende egal |
  | `nicht` | egal | zählen | außen egal, mehrfache = eins |
  | `anzahl` | wie `erwartet` (tolerant/streng) | wie `erwartet` | wie `erwartet` |

  Scheitert ein Vergleich NUR an Groß/klein, Satzzeichen, Leerzeichen,
  Leerzeilen oder Einrückung, meldet der Test „Fast! Deine Ausgabe
  unterscheidet sich nur in …: erwartet „…“ – deine Ausgabe „…“.“ (Detail
  `fast: true`; die Meldung steht auch in `Ergebnis.hinweis`).
  Faustregel für Inhalte: Gibt die Aufgabe den Wortlaut vor (Text in der
  Aufgabe, „genau“, Beispielausgabe), `streng=True` bzw. `exakt` benutzen.
  Ist der Wortlaut frei, tolerantes `erwartet`.
- `F(aufruf, soll=<aus Musterlösung>, vorspann="", beschreibung=None)` Funktionstest;
  `beschreibung` wird statt des Aufrufs als Testname angezeigt.

Eingebaute Regeln für `k.code(..., regeln=[...])` (Prüfung am Syntaxbaum des
Nutzercodes; Kommentare egal; Vorspann/Nachspann zählen nicht mit). Mehrere
Namen werden mit `|` getrennt. Unbekannte/ungültige Regeln meldet der Selbsttest
als Fehler (zur Laufzeit werden sie übersprungen).

| Regel | Bedeutung |
|---|---|
| `keine_slices` | kein Slice (`lst[1:]`, `lst[::-1]`, …) |
| `keine_schleifen` | kein `for`/`while`, auch keine Comprehension `[… for …]` |
| `max_funktionen:N` | höchstens N Funktionen (`def` und `lambda`) |
| `schleife_in:name` | die Funktion `name` existiert und enthält eine Schleife (auch Comprehension) |
| `funktion:a\|b` | mindestens eine der Funktionen ist definiert |
| `nur_konstanten:<JSON-Liste>` | alle Zahlen- und String-Literale stammen aus der Liste (Typ zählt: `"1"` ≠ `1`; True/False/None zählen nicht), z. B. `'nur_konstanten:["1", 0]'` |
| `pflicht_konstanten:<JSON-Liste>` | jede dieser Konstanten kommt mindestens einmal vor |
| `keine_methode:a\|b` | keine Methode `.a(...)` (z. B. `reverse`, `sort`) |
| `keine_funktion:a\|b` | keine Funktion `a` (als Name, `modul.a` oder Import), z. B. `reversed`, `max` |
| `nur_funktionen:a\|b` | nur diese Funktionen aufrufen (Methoden wie `.upper()` sind frei) |

Helfer: `engine.REGEL_NAMEN`, `engine.regel_fehler(regel) -> str|None`,
`engine.regel_beschreibung(regel) -> str`, `engine.regel_anwenden(ast_baum, regel) -> str`
(Fehlermeldung oder "").

## 3. Markup für Erklärungen (markup.py)

Text wird mit textwrap.dedent bereinigt. Zeilenweise Regeln:

| Syntax | Block |
|---|---|
| Zeile nur `---` | neue Seite |
| `## Text` | Überschrift |
| `!! Text` | Merksatz (hervorgehoben, Stern) |
| 4+ Leerzeichen Einrückung (zusammenhängend) | Codeblock (nur anzeigen) |
| `• Text` oder `- Text` oder `* Text` (auch eingerückt bis 3 Leerz.) | Aufzählung |
| `1. Text` | nummerierte Aufzählung |
| `\| a \| b \|` Zeilen | Tabelle (erste Zeile = Kopf; Trennzeile `\|---\|` optional) |
| sonst | Absatz (aufeinanderfolgende Zeilen werden verbunden) |

Inline in Absätzen/Listen/Tabellen: `` `code` ``, `**fett**` und `*kursiv*`.
`*kursiv*` gilt nur, wenn direkt innerhalb der Sternchen kein Leerzeichen steht und außen
kein Wortzeichen/Stern klebt (`markup.INLINE_KURSIV_RE`): `a * b`, `2*3`, `*args`, `**` bleiben
unverändert, in `` `code` `` wird nie umgesetzt. GUI: `<em>`, Terminal: ANSI kursiv bzw. ohne
Farben der Text ohne Sternchen.

Direktiven-Blöcke (Zeile beginnt mit `:::`, Ende mit einer Zeile nur `:::`;
Inhalt wird roh übernommen, nicht verschachtelbar):

```
:::analogie 🏠 Titel der Analogie       Alltagsbeispiel-Box (Inhalt = Markup)
:::achtung Titel                        Warnbox: typischer Fehler (Inhalt = Markup)
:::info Titel                           Infobox/Hintergrund (Inhalt = Markup)
:::code                                 ausführbares Beispiel: GUI zeigt Buttons
                                        "▶ Ausführen" und "👣 Schritt für Schritt";
                                        Terminal zeigt Code + echte Ausgabe
:::code eingaben=Anna|17                optional: Eingaben für input(), mit | getrennt
:::trace                                wie :::code, aber Schritt-für-Schritt-
                                        Ansicht wird direkt geöffnet
:::visual TYP                           Visualisierung, Inhalt = JSON (Abschnitt 4)
:::vergleich Links-Titel | Rechts-Titel zwei Spalten, Inhalt mit einer Zeile
                                        `|||` getrennt (beide Seiten = Markup)
```

markup.parse(text) liefert:
```python
[  # Seiten
  [ {"typ": "ueberschrift", "text": str},
    {"typ": "absatz", "text": str},              # mit Inline-Markup
    {"typ": "merke", "text": str},
    {"typ": "codeblock", "code": str},
    {"typ": "liste", "nummeriert": bool, "punkte": [str]},
    {"typ": "tabelle", "kopf": [str], "zeilen": [[str]]},
    {"typ": "box", "art": "analogie"|"achtung"|"info", "titel": str, "bloecke": [...]},
    {"typ": "code", "code": str, "eingaben": [str], "trace": bool},
    {"typ": "visual", "art": str, "daten": dict, "fehler": str|None},
    {"typ": "vergleich", "titel": [str, str], "spalten": [[...], [...]]},
  ], ...
]
```
Inline-Markup bleibt im Text erhalten (`` ` `` und `**`); jede Oberfläche
rendert es selbst (GUI: HTML-escapen, dann ersetzen!). Ungültiges JSON bei
visual -> "fehler" gesetzt; der Selbsttest meldet das.

## 4. Visualisierungen (`:::visual TYP` + JSON)

Beide Oberflächen implementieren ALLE Typen (GUI als animiertes SVG/HTML,
Terminal als ASCII). Unbekannte Felder werden ignoriert.

| TYP | JSON-Felder | Bedeutung |
|---|---|---|
| `variablen` | `{"vars": [{"name": "alter", "wert": "18", "typ": "int"}], "schritte": [[...], ...]?}` | Variablen als beschriftete Kisten mit Typ-Farbe. Optional `schritte`: Liste von Zuständen (je eine vars-Liste) + Untertitel `"texte": [str]` -> GUI blättert/animiert. |
| `liste` | `{"name": "lst", "werte": [3,4,1,2], "markiert": [0], "slice": "1:3", "interaktiv": false, "negativ": true}` | Nummerierte Fächer mit Index oben (und negativem Index unten). `slice` hebt Bereich hervor; `interaktiv` = Regler für start/stop/step. Werte als JSON (Strings werden mit Anführungszeichen gezeigt). |
| `string` | `{"text": "Hallo", "markiert": [], "slice": null, "interaktiv": false}` | wie liste, aber Zeichen |
| `dict` | `{"name": "telefon", "paare": [["Anna", "0151…"], ...], "markiert": ["Anna"]}` | Schlüssel → Wert als Schließfächer/Tabelle |
| `referenz` | `{"namen": {"a": 0, "b": 0, "c": 1}, "objekte": [[1,2,3], [1,2,3]]}` | Namensschilder (Variablen) mit Pfeilen auf Objekte; zeigt Aliasing vs. Kopie |
| `ablauf` | `{"schritte": [{"icon": "👩‍💻", "text": "Du schreibst Quelltext"}, ...]}` | Pfeilkette (Prozess) |
| `entscheidung` | `{"bedingung": "alter >= 18", "ja": "Eintritt", "nein": "Kein Eintritt", "elif": [{"bedingung": "...", "text": "..."}]}` | Flussdiagramm if/elif/else |
| `schleife` | `{"bedingung": "zahl < 5", "koerper": ["print(zahl)", "zahl += 1"], "danach": "print('fertig')", "art": "while"\|"for"}` | Flussdiagramm Schleife mit Rückpfeil |
| `zahlenstrahl` | `{"start": 0, "stop": 10, "step": 2, "interaktiv": true}` | range() auf dem Zahlenstrahl, Stop exklusiv markiert |
| `wahrheitstabelle` | `{"variablen": ["a", "b"], "ausdruecke": ["a and b", "a or b", "a ^ b", "a != b"]}` | wird in markup.py berechnet (`daten["zeilen"]`, siehe Abschnitt 11); die GUI-Ersatzauswertung und das Terminal können ebenfalls and/or/not/^/&/==/!= |
| `stapel` | `{"titel": "Aufrufstapel", "rahmen": ["fak(3)", "fak(2)", "fak(1)"], "rueckgaben": ["6", "2", "1"]}` | Stapel (Teller), unten zuerst; animiertes Auf- und Abbauen |
| `baum` | `{"wurzel": {"text": "fib(4)", "kinder": [{"text": "fib(3)", "kinder": [...]}, ...]}}` | Aufrufbaum (z. B. Fibonacci) |
| `funktion` | `{"name": "verdoppeln", "eingaben": ["x = 4"], "ausgabe": "8", "innen": "return x * 2"}` | Funktion als Maschine: Eingang → Maschine → Ausgang |
| `typen` | `{"werte": ["42", "3.14", "'Hallo'", "True", "None"]}` | Werte nach Datentyp einsortiert (Typ wird per Python ermittelt) |

## 5. Engine (engine.py) – UI-unabhängig

Alle Fragetypen haben:
- `id` (stabil): `f"{kapitel.slug}:{sha1(art + haupttext)[:8]}"` – bei
  Kollision `-2`, `-3` angehängt. haupttext = frage/aussage/code/aufgabe.
- `art` (Klartext), `typ` (Kurzname: mc, wf, text, ausgabe, ausdruck,
  luecke, puzzle, code), `phase` ("ueben" | "programmieren"),
  `kapitel` (Kapitel-Objekt), `tipps` (Liste, ggf. leer).
- `to_dict(mischen=True)` -> JSON-fähiges Dict OHNE Lösung (für GUI).
  MC: Optionen gemischt, Index der richtigen Antwort NICHT enthalten.
  Puzzle: Zeilen gemischt (inkl. Ablenker), je Zeile eine `zeilen_id`.
- `pruefen(antwort) -> Ergebnis` (Dataclass):
  `ok: bool, meldung: str (Kurzfeedback), loesung: str|None (Lösung als Text),
   erklaerung: str (Markup), details: list[dict] (z. B. Testergebnisse),
   hinweis: str|None (z. B. "Komma statt Punkt?")`
  Antwortformate:
  - mc: Optionstext (str) – NICHT der Index (Index hängt vom Mischen ab)
  - wf: bool
  - text/ausgabe/ausdruck: str
  - luecke: list[str]
  - puzzle: list[zeilen_id] in gewählter Reihenfolge (Einrückung ist fest)
  - code: str (Quellcode) -> details = [{"name", "ok", "meldung", "eingaben", "erwartet", "ausgabe"}]
    für JEDEN Test (nicht nur bis zum ersten Fehler), außerdem Prüfung von
    verboten/pflicht/rekursiv mit verständlicher Meldung.
- `loesung_anzeigen() -> str` (Musterlösung als Text/Code).

Kapitel: `slug, nummer, titel, beschreibung, quelle, teil, icon, lernziele,
elemente, fragen()`, `to_dict()` (Metadaten + Anzahl je Phase).
`TEILE` = geordnete Liste von Dicts:
`{"id": "tag1", "titel": "Tag 1 – Variablen & Ein-/Ausgabe", "untertitel": ...}`,
dann `tag2` (Verzweigungen & Schleifen), `tag3` (Schleifen & Funktionen),
`tag4` (Rekursion & Ausblick), `challenge` (Programmierchallenge),
`bonus` (Vertiefung).

`KAPITEL` (Liste in Reihenfolge), `kapitel_nach_slug(slug)`,
`alle_fragen() -> dict[id, Frage]`.

## 6. Kapitelmodule (vorkurs/inhalte/)

Dateiname `t<tag>_<nr>_<slug>.py`, z. B. `t1_04_variablen.py`; Bonus `b_<nr>_...`,
Challenge `c_<nr>_...`. `inhalte/__init__.py` importiert alle Module in
sortierter Dateinamen-Reihenfolge (pkgutil), damit die Kapitelnummern stimmen.

## 7. Sandbox (sandbox.py)

- `programm_starten(quelltext, eingabe_text="", timeout=6)` -> (returncode|None, stdout, stderr)
  eigener Prozess, leerer Temp-Ordner, UTF-8.
- `test_ausfuehren(nutzercode, test, loesung, timeout=6, streng=False)` liefert
  `(ok, meldung, details_dict)`; `streng` = Vorgabe der Aufgabe (siehe Abschnitt 2).
  details_dict: `name, ok, meldung, eingaben, erwartet, ausgabe, fehler, fast`.
- **Garantierte Interna** (Inhalte dürfen sich darauf verlassen, sie bleiben stabil):
  - Jeder Test läuft in einem eigenen Prozess in einem LEEREN Temp-Ordner (= aktueller
    Ordner). Dort liegt nur `dein_code.py` (`sandbox.DATEINAME`) plus Dateien, die der
    Vorspann anlegt.
  - `dein_code.py` = Vorspann + Zeilenumbruch + Nutzercode + Zeilenumbruch + Nachspann (bei
    F-Tests statt Nachspann der Prüfrahmen). Alles läuft in EINEM Namensraum mit
    `__name__ == "__main__"` und `__file__ == "dein_code.py"`; Funktionen und Variablen des
    Nutzers sind im Nachspann sichtbar, Funktionen des Vorspanns im Nutzercode.
  - Zeilennummern in Fehlermeldungen werden um die Länge des Vorspanns korrigiert.
  - `input()` liest in Tests aus stdin OHNE Echo und (außer bei `P(..., mit_aufforderung=True)`)
    OHNE Aufforderungstext. `sys.stdout` darf im Vorspann ersetzt und im Nachspann wiederhergestellt
    werden (so prüft Übung 4, Aufgabe 2.4.2 die Dreiecksform).
  - F-Tests: Nach dem Nutzercode wird ein Prüfrahmen angehängt, der genau eine Zeile mit
    `@@OK@@`, `@@FALSCH@@` oder `@@FEHLER@@` ausgibt; die Nutzerausgabe ist alles davor.
  - Zeitlimit 6 s pro Test, Ausgabelimit 200 000 Zeichen.
  - Prüfungen, die `dein_code.py` selbst lesen und an einem Marker abschneiden (früher
    `# @@REGELPRUEFUNG@@`), werden nicht mehr gebraucht: Dafür gibt es `regeln`
    (Abschnitt 2). Falls doch nötig: `open(__file__)` liefert Vorspann + Code + Nachspann.
- `ausfuehren(code, eingaben=[]) -> {"stdout", "stderr", "fehler": str|None, "fehler_zeile": int|None, "timeout": bool, "fehler_erklaert": str|None}`
  `fehler_erklaert`: anfängerfreundliche deutsche Erklärung für die
  häufigsten Fehler (NameError, TypeError, ValueError, IndexError, KeyError,
  ZeroDivisionError, SyntaxError, IndentationError, RecursionError,
  EOFError, AttributeError, UnboundLocalError, FileNotFoundError, Timeout).
- `trace(code, eingaben=[], max_schritte=400) -> {"schritte": [...], "abgebrochen": bool, "fehler": ...}`
  Läuft in eigenem Prozess (sys.settrace im Kindprozess, Ergebnis als JSON
  auf eine Marker-Zeile in stdout). Jeder Schritt:
  `{"zeile": int, "ereignis": "line"|"call"|"return"|"exception",
    "stapel": [{"funktion": "<modul>"|name, "zeile": int, "variablen": {name: WERT}}],
    "ausgabe": str (gesamte bisherige Ausgabe), "rueckgabe": WERT|None}`
  WERT = `{"typ": "int"|"float"|"str"|"bool"|"NoneType"|"list"|"tuple"|"dict"|"set"|"function"|"module"|"andere", "repr": str, "elemente": [WERT]?, "paare": [[WERT, WERT]]?, "id": int}`
  (verschachtelt bis Tiefe 3, max. 30 Elemente; `id` ermöglicht Aliasing-
  Pfeile). Nur Benutzer-Variablen (keine __dunder__, keine Module, keine
  importierten Funktionen). input() funktioniert mit den Eingaben.

## 8. Fortschritt (fortschritt.py)

Speicherort: `Path.home() / ".vorkurs_quiz" / "fortschritt.json"` (Ordner
bei Bedarf anlegen). Umgebungsvariable `VORKURS_QUIZ_DATEN` überschreibt den
Ordner (für Tests). Falls der Ordner nicht beschreibbar ist, wird
`<Programmordner>/vorkurs_quiz_fortschritt.json` als Ausweichpfad genutzt.
Beim ersten Start: Existiert `vorkurs_quiz_fortschritt.json` (v1) neben
`vorkurs_quiz.py` und noch keine neue Datei, wird es migriert. Danach wird die alte
Datei in `vorkurs_quiz_fortschritt.v1.json` umbenannt. Format v2:
```json
{
 "version": 2,
 "kapitel": {"<slug>": {"best": 12, "max": 15, "abgeschlossen": true, "zuletzt": "2026-10-03"}},
 "fragen": {"<frage_id>": {"richtig": 2, "falsch": 1, "zuletzt": "2026-10-03", "kasten": 3}},
 "fehlerkiste": ["<frage_id>", ...],
 "pruefungen": [{"datum": "...", "punkte": 25, "max": 30, "note": "1,7"}],
 "entwuerfe": {"<frage_id>": "code..."},
 "xp": 340,
 "serie": {"tage": 3, "zuletzt": "2026-10-03"},
 "abzeichen": ["erstes_kapitel", ...],
 "einstellungen": {"theme": "auto"}
}
```
- Migration v1 -> v2: v1 hat `kapitel` mit Nummern "1".."24" in der Reihenfolge
  der alten Kapitel. Mapping alte Nummer -> neuer slug liegt in
  `fortschritt.V1_KAPITEL_SLUGS` (Liste von 24 slugs). Alte Fehlerkiste-IDs
  (Format "K02-012") können nicht zugeordnet werden und werden verworfen.
  Vorher Sicherung `vorkurs_quiz_fortschritt.v1.json` anlegen.
- XP: richtige Frage im ersten Versuch +10, im zweiten +5, Code-Aufgabe +30,
  Kapitel abgeschlossen +50. Level = Stufen (0, 100, 250, 500, 900, 1400,
  2000, 2800, 3800, 5000) mit geschlechtsneutralen Namen, z. B.
  "Level 1 · Neugierig", "Level 2 · Entdecken", "Level 3 · Ausprobieren" …
  "Level 10 · Python-Profi".
- Leitner-Kasten (1–5) pro Frage für "Wiederholen": falsch -> Kasten 1,
  richtig -> +1. `faellige_fragen(n)` liefert bevorzugt niedrige Kästen.
- Funktionen: `laden()`, `speichern(daten)` (atomar: erst .tmp, dann replace),
  `antwort_verbuchen(daten, frage, ok, versuch)`, `kapitel_abschliessen(daten, kapitel, punkte, max)`,
  `statistik(daten) -> dict` (für Dashboard: XP, Level, Fortschritt je Teil,
  Serie, Abzeichen, Anzahl gelöster Code-Aufgaben).
- Thread-sicher (threading.Lock), da der Webserver mehrere Threads hat.

## 9. Web-API (web/server.py)

`ThreadingHTTPServer` auf 127.0.0.1, Port 8765 (falls belegt: nächster freier).
Öffnet den Browser (webbrowser.open), außer `--kein-browser`. Beenden mit
Strg+C im Terminal oder Button "Beenden" (POST /api/beenden).
Alle Antworten JSON (UTF-8). Statische Dateien aus web/static.

| Methode & Pfad | Body | Antwort |
|---|---|---|
| GET /api/uebersicht | – | `{"teile": [{..., "kapitel": [kapitel.to_dict() + fortschritt]}], "statistik": {...}}` |
| GET /api/kapitel/<slug> | – | `{"kapitel": {...}, "elemente": [ {"typ": "erklaerung", "titel", "seiten": markup.parse(...)} | {"typ": "frage", "frage": frage.to_dict()} | {"typ": "zusammenfassung", "seiten": ...} ]}` |
| POST /api/antwort | `{"id", "antwort", "versuch": 1|2}` | `Ergebnis` als Dict + `{"xp_neu", "statistik"}` |
| POST /api/code/pruefen | `{"id", "code"}` | wie /api/antwort (details = Testergebnisse); speichert Entwurf |
| POST /api/entwurf | `{"id", "code"}` | `{}` (Autosave) |
| POST /api/loesung | `{"id"}` | `{"loesung": str, "erklaerung": str}` (zählt als "Lösung angesehen") |
| POST /api/ausfuehren | `{"code", "eingaben": [str]}` | sandbox.ausfuehren |
| POST /api/trace | `{"code", "eingaben": [str]}` | sandbox.trace |
| POST /api/kapitel/<slug>/abschluss | `{"punkte", "max"}` | `{"statistik", "neue_abzeichen": [...]}` |
| GET /api/training?modus=pruefung|fehlerkiste|wiederholen&anzahl=N | – | `{"fragen": [frage.to_dict()]}` |
| POST /api/pruefung/ergebnis | `{"punkte", "max"}` | `{"note"}` |
| GET /api/spickzettel | – | `{"seiten": markup.parse(SPICKZETTEL), "kapitel": [{"slug","titel","seiten"}]}` |
| GET /api/visual/typen | – | `{"typ": "...", ...}` Helfer für Visual `typen` (Python bestimmt Typen) |
| POST /api/fortschritt/zuruecksetzen | `{"bestaetigt": true}` | `{}` |
| POST /api/einstellungen | `{...}` | `{}` |
| POST /api/beenden | – | `{}` und Server fährt herunter |

Fehler: HTTP 400/404/500 mit `{"fehler": "Text"}`. Keine Lösungen im
Klartext an den Client, bevor geantwortet oder /api/loesung aufgerufen wurde.

## 10. Selbsttest (`python vorkurs_quiz.py --selbsttest`)

Prüft: jede Musterlösung besteht ihre Tests; verboten/pflicht/rekursiv werden
von der Musterlösung erfüllt; MC ohne doppelte Optionen und >= 2 Optionen;
Ausgabe-Fragen laufen ohne Hänger; bei Code-Aufgaben: Regeln gültig (`regel_fehler`),
keine leeren Alternativen oder Anzahl-Texte, keine negativen Anzahlen, `streng` ist bool,
F-Tests ohne Ausgabe-Angaben, `leerzeichen` nur mit exakt/streng; Lückenanzahl == Antwortenanzahl; Puzzle-
Lösung ist korrekt; alle Markup-Blöcke parsebar, alle visual-JSONs gültig und
mit bekanntem TYP; alle :::code-Beispiele laufen (Fehler sind erlaubt,
Timeouts nicht); IDs eindeutig; jedes Kapitel hat lernziele, mindestens eine
Erklärung, mindestens 2 Programmieraufgaben (code/puzzle/luecke) und eine
zusammenfassung (Warnung statt Fehler, solange Inhalte noch wachsen).
Exit-Code 0 nur ohne Fehler.

## 11. Entscheidungen des Core-Agents

Ergänzungen und Klarstellungen. Bestehende Schnittstellen bleiben gültig;
alles hier ist zusätzlich oder präzisiert eine Lücke.

**Laden der Inhalte**
- `engine.py` importiert am Dateiende `vorkurs.inhalte`. `engine.KAPITEL` ist also
  nach `from vorkurs import engine` gefüllt (`engine.inhalte_laden()` kann gefahrlos
  erneut aufgerufen werden).
- Reihenfolge der Kapitelmodule: zuerst `t<tag>_*` nach Tagnummer, dann `c_*`, dann
  `b_*`, jeweils alphabetisch. Rein alphabetisch stünde `b_` vor `t1_`. Module mit
  `_` am Anfang und `spickzettel.py` sind keine Kapitel.
- `vorkurs.inhalte.SPICKZETTEL` wird aus `spickzettel.py` re-exportiert.

**IDs**: `sha1(art + haupttext.strip())`, `art` = Klartext (z. B. "Multiple Choice").
haupttext: mc/text/ausdruck = frage, wf = aussage, ausgabe = code, code/puzzle =
aufgabe, **luecke = frage + "\n" + code** (sonst kollidieren gleiche Fragetexte).

**Kapitel**: `k.lernziele` ist eine Liste, die man aufrufen kann (`k.lernziele([...])`
setzt sie). Dazu kommen `k.zusammenfassung_text` (str|None), `k.erklaerungen()`,
`k.elemente_dicts(mischen=True)` (fertige Elementliste im Format von
GET /api/kapitel), `engine.kapitel_von_teil(teil)`, `engine.frage_nach_id(id)`,
`engine.vorberechnen()` (rechnet Ausgabe-Lösungen und Sollwerte vorab, z. B. im
Hintergrund beim Serverstart). `Kapitel.to_dict()["anzahl"]` =
`{"erklaerungen", "ueben", "programmieren", "fragen"}` plus `hat_zusammenfassung`.

**Frage.to_dict()** – gemeinsame Felder: `id, typ, art, phase, kapitel (slug), tipps,
code`. Zusätzlich je nach Typ:
mc `frage, optionen` · wf `aussage` · text `frage` · ausgabe `frage` (+ `code`) ·
ausdruck `frage, gegeben` (Variablenbelegung als Code-Text), `muss_enthalten` ·
luecke `frage, anzahl_luecken` (`code` enthält `___`) ·
puzzle `aufgabe, anzahl` (benötigte Zeilen), `zeilen: [{"zeilen_id", "text" (ohne
Einrückung), "einrueckung" (Anzahl Leerzeichen)}]` (zeilen_ids verraten die
Reihenfolge nicht) ·
code `aufgabe, vorlage, tests: [{"name", "eingaben"}], anzahl_tests, verboten,
pflicht, rekursiv` (ggf. mit `|`-Alternativen), `regeln` (Liste lesbarer Beschreibungen),
`genaue_ausgabe` (bool: mindestens ein Test prüft Groß/klein und Satzzeichen). Markup-Felder: frage, aussage, aufgabe, erklaerung (mit
markup.parse rendern).

**Ergebnis**: `loesung` ist immer gefüllt. Die Oberfläche entscheidet, wann sie die
Lösung zeigt (vor dem letzten Versuch nicht), z. B. mit
`ergebnis.to_dict(mit_loesung=False)`. Bei MC wird nur der Optionstext akzeptiert.
`details` bei code: zuerst die Regel-Einträge (`"regel": true`, Namen "Verboten: …",
"Pflicht: …", "Rekursion: …", "Regel: <Beschreibung>"), dann ein Eintrag pro Test, mit den
Zusatzfeldern `fehler` (letzte Fehlerzeile oder None) und `fast` (nur Groß/klein,
Satzzeichen oder Leerzeichen falsch). Bei luecke/puzzle gibt es einen Eintrag
pro Lücke bzw. Zeile, bei ausdruck einen pro Belegung (`erwartet`/`ausgabe` = repr).
Ein Syntaxfehler im Code wird vorab erkannt; dann laufen keine Tests. `hinweis`
enthält bei Laufzeitfehlern die Erklärung aus `sandbox.fehler_erklaeren`, sonst
die „Fast!“-Meldung des ersten fehlgeschlagenen Tests. Ausgabevergleich: siehe Abschnitt 2
(`erwartet` standardmäßig tolerant wie in v1, `exakt` streng, `streng=True` für den Wortlaut).

**Markup-Heuristiken** (damit die v1-Texte sinnvoll zerfallen):
- Eine Zeile, die auf der Texthöhe eines Listenpunkts eingerückt ist (±1), setzt
  diesen Punkt fort.
- Zeilen mit 1–3 Leerzeichen Einrückung und Spaltenausrichtung (2+ Leerzeichen im
  Text) oder mit Rahmenzeichen (─│…) gelten als vorformatiert, also Codeblock
  (ASCII-Tabellen). Folgen sie direkt auf einen Codeblock, gehören sie dazu.
- Direkt aufeinanderfolgende `!!`-Zeilen werden zu EINEM Merksatz verbunden.
- Ein einzelnes `**`, das kein Fett-Paar ist (z. B. `2 ** 10`), wird beim Parsen zu
  `` `**` ``. Empfohlene Regexe für die Oberflächen: `markup.INLINE_CODE_RE` und
  `markup.INLINE_FETT_RE` = `(?<![\w*])\*\*(?=\S)(.+?)(?<=\S)\*\*(?![\w*])`.
- `markup.parse` ergänzt Visuals: `typen` bekommt `daten["typen"] = [{"wert","typ"}]`,
  `wahrheitstabelle` bekommt `daten["zeilen"] = [{"werte": [bool], "ergebnisse": [bool|None]}]`
  (erlaubt: Variablen, True/False, `and`, `or`, `not`, `^` (XOR), `&`, `|`, `==`, `!=`,
  Klammern; nicht auswertbare Ausdrücke meldet `markup.pruefen`, also der Selbsttest).
- Python-Darstellung der Werte (JSON/JavaScript verlieren bei `2.0` die Nachkommastelle):
  `liste` bekommt `daten["werte_anzeige"] = [str]`, `dict` `daten["paare_anzeige"] =
  [[str, str]]`, `variablen` je Variable (auch in `schritte`) `"anzeige"` (Text-Werte bleiben,
  wie sie geschrieben sind), `referenz` `daten["objekte_anzeige"] = [str]` und
  `daten["objekte_werte"] = [WERT]` (Format wie beim Tracer). Berechnet wird mit Python
  (`repr`), also `2.0` → `"2.0"`, `"a"` → `"'a'"`. GUI (visuals.js) und Terminal (render.py)
  nutzen diese Felder und fallen auf die alten Felder zurück. Helfer: `markup.py_anzeige(w)`,
  `markup.py_wert(w)`.
- Weitere Helfer: `markup.pruefen(text) -> [Probleme]`, `markup.alle_bloecke(seiten)`,
  `markup.code_beispiele(seiten)`, `markup.VISUAL_TYPEN`.

**Sandbox**
- Der Benutzercode läuft als `dein_code.py` in einem Startrahmen. Tracebacks zeigen
  nur Benutzerzeilen. Bei mehr als 200 000 Zeichen Ausgabe wird das Programm
  gestoppt (Endlosschleife mit print). Höchstens 4–12 Kindprozesse gleichzeitig.
- `ausfuehren` und `trace` zeigen Eingaben im Ausgabetext an, wie in einem echten
  Terminal (`Name? Anna`). Die Tests (P/F) tun das NICHT (wie in v1) und lassen
  zusätzlich den Aufforderungstext weg (`programm_starten(..., aufforderung=False)`;
  Ausnahme `P(..., mit_aufforderung=True)`). Ausgabe-Fragen und Puzzle laufen unverändert.
- `ausfuehren`: `stderr` ist bereinigt. `trace` hat zusätzlich `fehler_zeile`,
  `fehler_erklaert`, `ausgabe` (gesamt) und `timeout`. `fehler` ist bei beiden ein
  Text wie "ZeroDivisionError: division by zero" oder None.
- Trace-Semantik: Ein `line`-Schritt zeigt die Zeile, die als NÄCHSTE ausgeführt wird,
  und die Variablen VOR dieser Zeile. `call` erscheint beim Funktionseintritt, aber
  nicht für das Modul. `exception`-Schritte haben das Zusatzfeld `fehler`. Der letzte
  Schritt ist meist `return` von `<modul>` (Endzustand). `stapel[0]` ist das Modul,
  der letzte Eintrag die aktuelle Funktion. Bei Überschreiten von `max_schritte` gilt
  `abgebrochen = true`. WERT hat bei mehr als 30 Elementen zusätzlich `"gekuerzt": true`.
- "Was gibt der Code aus?" und die Ausdrücke der Nutzer laufen im Kindprozess
  (v1: exec im selben Prozess). Das ist sicher für den Webserver mit Threads.
  Ergebnisse werden gecacht. `sandbox.fehler_erklaeren(text)` gibt es auch einzeln.

**Fortschritt**
- Der Ausweichpfad im Programmordner hat denselben Namen wie die v1-Datei. Liegt
  dort eine v1-Datei, wird sie an Ort und Stelle migriert (vorher Sicherung `.v1.json`).
- Ist `VORKURS_QUIZ_DATEN` gesetzt, wird auch die v1-Datei NUR in diesem Ordner
  gesucht. **Tests aller Agents müssen diese Variable setzen.** Sonst wird der
  echte Fortschritt des Nutzers migriert.
- Zusatzschlüssel `"meta"` (z. B. `migriert_von`, `fehlerkiste_geleert`).
  Fragen-Einträge können zusätzlich `"loesung_angesehen": true` haben.
- Migration: Jedes alte Kapitel gilt als abgeschlossen und bringt
  XP = 50 + 10 × best (der Stand war ja verdient). Prüfungen werden mit Note übernommen.
- XP: Die Werte aus Abschnitt 8 gibt es beim ERSTEN Lösen einer Frage. Wer eine schon
  gelöste Frage erneut löst, bekommt +2. Code nach angesehener Lösung bringt +5, ein
  Kapitel +50 nur beim ersten Abschluss.
- `antwort_verbuchen(daten, frage, ok, versuch=1, endgueltig=None)` →
  `{"xp_neu", "neue_abzeichen"}`. `frage` darf ein Objekt oder eine ID sein. Ein
  falscher Versuch zählt nur als "falsch". In Fehlerkiste und Kasten 1 kommt die
  Frage erst, wenn der Versuch endgültig ist (Standard: `versuch >= 2` oder Typ
  mc/wf). Für "weiß nicht" bitte `endgueltig=True` übergeben.
- Weitere Funktionen: `loesung_angesehen(daten, frage)` (→ Fehlerkiste),
  `kapitel_abschliessen(...)` → `{"xp_neu", "neue_abzeichen", "neuer_rekord"}` (setzt
  immer `abgeschlossen = true`), `pruefung_verbuchen(daten, punkte, max)` →
  `{"note", "neue_abzeichen"}`, `note_berechnen`, `entwurf_speichern`,
  `einstellungen_setzen`, `zuruecksetzen(daten)` (behält einstellungen),
  `kapitel_status(daten, kapitel)`, `level(xp)`, `anzahl_faellig`, `ABZEICHEN`
  (Liste von `{id, titel, beschreibung, icon}`). Alle Funktionen ändern nur `daten`;
  `speichern(daten)` ruft der Aufrufer auf.
- `faellige_fragen(daten, n=10)` (auch `faellige_fragen(n)`): Leitner-Intervalle
  Kasten 1–5 = 0/1/2/4/8 Tage. Fällige Fragen kommen zuerst, sortiert nach Kasten und
  Datum. Danach wird mit den übrigen beantworteten Fragen aufgefüllt.
- `statistik(daten)`: `xp, level{nummer,name,titel,xp_start,xp_naechstes,fortschritt},
  serie, abzeichen, abzeichen_alle[+erreicht], teile[{id,titel,kapitel_gesamt,
  kapitel_abgeschlossen,fragen_gesamt,fragen_richtig,fortschritt}], kapitel_gesamt,
  kapitel_abgeschlossen, fragen_gesamt, fragen_richtig, code_gesamt, code_geloest,
  fehlerkiste, faellig, pruefungen, beste_note`.

**Umgebung & Starter**: `umgebung.pruefen(gui=True)` prüft web/static nur bei
`gui=True`. Dazu gibt es `umgebung.konsole_vorbereiten()` und
`umgebung.gui_dateien_vorhanden()`. Fehlen die GUI-Dateien, startet der Starter die
Terminal-Version. Ohne `--port` übergibt er `port=8765`.
