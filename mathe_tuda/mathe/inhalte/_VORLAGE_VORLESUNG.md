# Anleitung: Vorlesungs-Lektion `vl_NN_<thema>.py` (Teil "vorlesung")

Auslöser: Jason liefert nach einer Vorlesung die Folien (PDF) und ggf. Notizen. Skript siehe
`Unterlagen/Mathe1_Disser_2026/Skript_MatheI_Disser_WS2627.pdf` (Text: Scratchpad `disser/skript.txt`).
Folien/Notizen ablegen unter `Unterlagen/Mathe1_Disser_2026/Vorlesungen/VLNN/`.

Technisch wie jedes Kapitel (siehe `_VORLAGE_KAPITEL.md`), aber `teil="vorlesung"`,
`slug="vlNN"`, Datei `vl_NN_<thema>.py`, `quelle="Vorlesung NN (Datum), Folien VL NN, Skript Abschn. x"`.

## Aufbau (Pflicht)
1. **Rückblick** (nur ab VL 2): die Rückblickfragen der Folien als erste Üben-Fragen.
2. **Seiten in Folienreihenfolge**, mit denselben Begriffen, Reihenfolge und Beispielen wie Folien/Skript,
   Skript-Nummern nennen („Definition 1.21“). Jede Folienidee wird von Null erklärt: Alltagsbeispiel, dann
   Fachsprache, dann Folienbeispiel. Ton und Tiefe wie `v02_aussagen.py`. Nichts voraussetzen, nichts auslassen.
   Ein `:::alt` mit der „Alltagsversion“ je Seite. Fachbegriffe als `[[Glossar]]`.
3. **Beweise der Vorlesung** Schritt für Schritt (ordnen- und luecke-Aufgaben), Muster der Beweisform benennen.
4. **Üben**: (a) Folienquizze/Pingo-Fragen sinngemäß, (b) Verständnisfragen mit Fehlererkennung,
   (c) mindestens ein Generator (Rechenaufgaben im Stil der Vorlesung).
5. **Praxis**: Leseaufgaben der Vorlesung als `papier`-Aufgabe mit Musterlösung und Checkliste;
   mindestens eine Aufgabe im Stil der Übungsquizze/Hausübung (`uebungsblatt=True`).
6. **Zusammenfassung** („Das musst du nach dieser Vorlesung können“) + Querbezüge zur Informatik laut Folien.
7. Verweise auf die vertiefenden Mathe-1-Kapitel (`m1_*`) und Vorkurs-Kapitel per Glossar/Text, aber
   **keine Inhalte kopieren**: die Lektion ist die Brücke „Vorlesung verstehen“, `m1_*` die Vertiefung.

## Regeln
- Notation exakt wie Disser (ℕ = {0,1,…}, `:=`, ⊕, □).
- Termine/Organisatorisches gehören nicht in die Lektion.
- Mathematik rechnet Python (assert beim Laden), Selbsttest muss 0 Fehler melden.
- Jasons Fortschritt (`~/.mathe_quiz`) nie anfassen; Tests mit `MATHE_QUIZ_DATEN=<scratchpad>/...`.
