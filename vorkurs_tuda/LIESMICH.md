# Python-Vorkurs-Lernquiz (TU Darmstadt 2026)

Ein Lernprogramm für komplette Anfänger zum Programmiervorkurs: Erklärungen,
Quizfragen und echte Programmieraufgaben, die automatisch geprüft werden.
Alles läuft **offline** auf deinem Computer.

## Voraussetzungen

- **Python 3.10 oder neuer**. Sonst nichts: keine Zusatzpakete und kein Internet.
- Windows, macOS oder Linux.

## Starten

| System | So geht's |
|---|---|
| Windows | Doppelklick auf **`Start.bat`**. Fehlt Python, bietet das Skript an, es mit `winget` zu installieren. |
| macOS | Doppelklick auf **`Start.command`**. Beim ersten Mal ggf. im Terminal: `chmod +x Start.command`. Bei einer Sicherheitswarnung: Rechtsklick → „Öffnen“. |
| Linux | Im Terminal im Programmordner: `chmod +x start.sh` (einmalig), dann `./start.sh` |
| Überall | `python vorkurs_quiz.py` (Windows) bzw. `python3 vorkurs_quiz.py` |

Nach dem Start wählst du:

- **[1] Grafische Oberfläche** (empfohlen): Das Quiz öffnet sich im Browser.
  Beenden kannst du es mit dem Button „Beenden“ oder mit **Strg + C** im Terminalfenster.
- **[2] Terminal**: Alles läuft direkt im Konsolenfenster.

### Optionen

```
python vorkurs_quiz.py --gui            grafische Oberfläche direkt starten
python vorkurs_quiz.py --terminal       Terminal-Version direkt starten
python vorkurs_quiz.py --keine-farben   falls im Terminal komische Zeichen wie [92m erscheinen
python vorkurs_quiz.py --port 9000      anderer Port für die grafische Oberfläche
python vorkurs_quiz.py --kein-browser   Browser nicht automatisch öffnen
python vorkurs_quiz.py --selbsttest     alle Inhalte automatisch prüfen (für Neugierige)
```

Die Start-Skripte reichen diese Optionen durch, z. B. `Start.bat --terminal`.

## Bedienung in Kürze

- Die Kapitel sind nach den **Vorkurs-Tagen** sortiert (Tag 1–4, dazu Bonus).
- Jedes Kapitel folgt dem Lernpfad **Verstehen → Üben → Programmieren**.
- Bei Fragen hast du meist **zwei Versuche**, und es gibt Tipps.
- Programmieraufgaben werden mit automatischen Tests geprüft. Dein Code läuft
  dabei in einem eigenen, abgeschotteten Python-Prozess mit Zeitlimit.
- Falsch beantwortete Fragen landen in der **Fehlerkiste**. Unter
  **Wiederholen** kommen Fragen nach dem Karteikasten-Prinzip zurück.
- Für richtige Antworten gibt es XP, Level und Abzeichen.

## Wo wird mein Fortschritt gespeichert?

Nicht im Programmordner, sondern in deinem Benutzerordner:

- Windows: `C:\Users\<Name>\.vorkurs_quiz\fortschritt.json`
- macOS/Linux: `~/.vorkurs_quiz/fortschritt.json`

Ist dieser Ordner nicht beschreibbar, wird ersatzweise
`vorkurs_quiz_fortschritt.json` im Programmordner benutzt.
Ein Fortschritt aus der alten Version 1 (`vorkurs_quiz_fortschritt.json` neben
`vorkurs_quiz.py`) wird beim ersten Start automatisch übernommen. Die alte Datei
bleibt als `vorkurs_quiz_fortschritt.v1.json` erhalten.

Fortgeschrittene können den Speicherort mit der Umgebungsvariable
`VORKURS_QUIZ_DATEN` (Ordnerpfad) selbst festlegen.

## Weitergeben

Du kannst den **ganzen Programmordner** einfach kopieren oder als ZIP
weitergeben. Dein persönlicher Fortschritt wird dabei nicht mitgeschickt, weil
er im Benutzerordner liegt. Wer das Quiz bekommt, braucht nur Python 3.10+.

## Probleme?

- *„Python wurde nicht gefunden“*: Python von https://www.python.org/downloads/
  installieren. Unter Windows beim Installieren **„Add python.exe to PATH“** ankreuzen.
- *Komische Zeichen im Terminal*: `--keine-farben` benutzen oder die grafische Oberfläche nehmen.
- *Der Browser öffnet sich nicht*: Die Adresse (z. B. `http://127.0.0.1:8765`)
  steht im Terminalfenster. Kopiere sie in den Browser.
- *Port belegt*: Das Programm nimmt automatisch den nächsten freien Port, oder du
  wählst einen mit `--port 9000`.

## Für Entwickler

Aufbau, Schnittstellen und Datenformate stehen in `vorkurs/ARCHITEKTUR.md`.
Eine Vorlage für neue Kapitel liegt in `vorkurs/inhalte/_VORLAGE_KAPITEL.md`.
Nach jeder Inhaltsänderung bitte `python vorkurs_quiz.py --selbsttest` laufen lassen.
