# Mathe für Informatik – Lernsystem (TU Darmstadt 2026)

Ein Lernprogramm für Mathe 1 und Mathe 2 im Informatikstudium, das bei null anfängt:
Brüche, Klammern, Gleichungen – und dann Schritt für Schritt bis zu Eigenwerten und Integralen.
Mit Erklärungen, vorgerechneten Beispielen, Bildern zum Ausprobieren und vielen Übungen.
Alles läuft **offline** auf deinem Computer.

## Voraussetzungen

- **Python 3.10 oder neuer.** Sonst nichts: keine Zusatzpakete, kein Internet.
- Ein Browser (Firefox, Chrome, Edge, Safari).
- Windows, macOS oder Linux.

## Starten

| System | So geht's |
|---|---|
| Windows | Doppelklick auf **`Start.bat`**. Fehlt Python, bietet das Skript an, es mit `winget` zu installieren. |
| macOS | Doppelklick auf **`Start.command`**. Beim ersten Mal ggf. im Terminal: `chmod +x Start.command`. Bei einer Sicherheitswarnung: Rechtsklick → „Öffnen“. |
| Linux | Im Terminal im Programmordner: `chmod +x start.sh` (einmalig), dann `./start.sh` |
| Überall | `python mathe_quiz.py` (Windows) bzw. `python3 mathe_quiz.py` |

Der Browser öffnet sich von selbst. Beenden: Button „Beenden“ oben rechts oder **Strg + C** im Terminalfenster.

### Optionen

```
python3 mathe_quiz.py --port 9000      anderer Port (Standard 8766, belegt -> nächster freier)
python3 mathe_quiz.py --kein-browser   Browser nicht automatisch öffnen
python3 mathe_quiz.py --selbsttest     alle Inhalte automatisch prüfen (für Neugierige)
```

Der Python-Vorkurs benutzt Port 8765. Beide Programme können also gleichzeitig laufen.

## Bedienung in Kürze

- Die Kapitel sind in **Fundament** (Schulstoff von vorn), **Vorkurs** (wie der Mathematik-Vorkurs der
  TU Darmstadt), **Mathe 1** und **Mathe 2** (wie „Mathematik I/II für Informatik“ laut Modulhandbuch
  PO 2023), **Bonus** und **Klausur** sortiert. Welche Quelle hinter welchem Kapitel steht, zeigt das
  Kapitel oben an und steht in `mathe/LEHRPLAN.md`.
- Beim ersten Start kannst du einen freiwilligen **Diagnosetest** machen. Er empfiehlt dir, wo du einsteigst.
- Jedes Kapitel: **Verstehen** (Erklärseiten mit vorgerechneten Beispielen), **Üben** (kurze Fragen
  direkt zu jeder Idee), **Praxis** (vom Leichten bis zum Übungsblatt), **Merkzettel**.
- Unter jeder Erklärung gibt es den Knopf **„Ich verstehe das nicht“** mit einer zweiten, anderen Erklärung.
- Unterstrichene Fachwörter erklären sich beim Darüberfahren oder Antippen (Glossar).
- Bei Aufgaben hast du **zwei Versuche** und bis zu drei **Tipps**. Typische Fehler werden erkannt und
  erklärt. Danach siehst du den kompletten **Rechenweg**.
- Unter dem Eingabefeld zeigt die **Vorschau**, wie das Programm deine Eingabe versteht. Die
  **Mathe-Tasten** helfen bei Brüchen, Wurzeln, Hochzahlen und Mengenklammern.
- **Endlos üben**: Übungsmaschinen erzeugen immer neue Aufgaben mit neuen Zahlen.
- **Wiederholen** (Karteikasten), **Fehlerkiste**, **Probeklausur** mit Zeitlimit und Note,
  **Formelsammlung** (druckbar), **Glossar**, **Spielwiese** (Funktionsplotter, Bruch-, Matrix- und
  LGS-Rechner mit Rechenweg, Primfaktoren, Basiswandler).
- Tasten: **Enter** prüft, **Strg + Enter** geht zur nächsten Aufgabe, **← / →** blättern.
- Einstellungen (⚙️): Farbschema, Schrift- und Formelgröße, Animationen, Pausenhinweis.

### So gibst du Antworten ein

| Was | Beispiele |
|---|---|
| Zahlen | `3/4`, `-2,5`, `0.75`, `sqrt(2)`, `√2`, `pi` |
| Terme | `2x + 3`, `(x+1)^2`, `x²`, `3(x - 1)`, `|x|` |
| Lösungsmengen | `{2; -3}`, `keine`, `[0; 4)`, `x < 2`, `(-inf; 1] ∪ [3; inf)` |
| Mengen | `{1; 2; 3}`, `{}` |

Kommazahlen in Mengen: Elemente mit **Semikolon** trennen, z. B. `{1,5; 2}`.

## Wo wird mein Fortschritt gespeichert?

Nicht im Programmordner, sondern in deinem Benutzerordner:

- Windows: `C:\Users\<Name>\.mathe_quiz\fortschritt.json`
- macOS/Linux: `~/.mathe_quiz/fortschritt.json`

Ist dieser Ordner nicht beschreibbar, wird ersatzweise `mathe_quiz_fortschritt.json` im Programmordner
benutzt. Den Speicherort kannst du mit der Umgebungsvariable `MATHE_QUIZ_DATEN` (Ordnerpfad) selbst festlegen.

## Weitergeben

Du kannst den **ganzen Ordner `mathe_tuda`** kopieren oder als ZIP weitergeben. Dein persönlicher
Fortschritt wird dabei nicht mitgeschickt. Wer das Programm bekommt, braucht nur Python 3.10+.

## Probleme?

- *„Python wurde nicht gefunden“*: Python von https://www.python.org/downloads/ installieren. Unter
  Windows beim Installieren **„Add python.exe to PATH“** ankreuzen.
- *Der Browser öffnet sich nicht*: Die Adresse (z. B. `http://127.0.0.1:8766`) steht im Terminalfenster.
  Kopiere sie in den Browser.
- *Formeln sehen aus wie einfacher Text*: Die Formelschrift KaTeX fehlt im Ordner
  `mathe/web/static/vendor/katex`. Lade den Programmordner vollständig neu herunter.
- *Port belegt*: Das Programm nimmt automatisch den nächsten freien Port, oder du wählst einen mit `--port 9000`.

## Für Entwickler

- Aufbau, Schnittstellen und Datenformate: `mathe/ARCHITEKTUR.md`.
- Vorlage für neue Kapitel: `mathe/inhalte/_VORLAGE_KAPITEL.md`.
- Nach jeder Inhaltsänderung: `python3 mathe_quiz.py --selbsttest` (muss mit 0 Fehlern enden).
- Oberflächentest im Browser: `python3 mathe_quiz.py --gui --e2e`, dann `http://127.0.0.1:8766/?e2e=kapitel`
  (weitere Modi: `training`, `werkzeuge`, `formeln`). Der Bericht erscheint im Terminal.
- **KaTeX** (MIT-Lizenz, `mathe/web/static/vendor/katex/LICENSE`) wurde einmalig mit
  `python3 tools/katex_holen.py` aus dem npm-Registry geladen (Version 0.19.0, sha512 geprüft). Zur
  Laufzeit wird nichts aus dem Internet geladen.
