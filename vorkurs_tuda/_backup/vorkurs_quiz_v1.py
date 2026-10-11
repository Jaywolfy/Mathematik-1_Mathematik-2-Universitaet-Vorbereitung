#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
   DAS GROSSE PYTHON-VORKURS-LERNQUIZ
   (Programmiervorkurs TU Darmstadt 2026 – alle Vorlesungen + alle Übungen)
==============================================================================

Dieses Programm bringt dir ALLES bei, was im Vorkurs vorkam – Schritt für
Schritt, für komplette Anfänger, mit Alltagsbeispielen:

   Vorlesung 1: Variablen & Ein-/Ausgabe (Datentypen, Operatoren, Strings, ...)
   Vorlesung 2: Verzweigungen & Schleifen (Logik, if/elif/else, match, while,
                Listen, Slicing, Fehlermeldungen)
   Vorlesung 3: Schleifen & Funktionen (Tupel, Dictionaries, for, range,
                enumerate, zip, import, Dateien, Funktionen)
   Vorlesung 4: Rekursion, Ausblick auf Java, guter Code, Sprachensalat
   Übung 1-3:   alle Aufgaben als Quizfragen und Programmieraufgaben

SO STARTEST DU DAS QUIZ:
   Windows:              python vorkurs_quiz.py
   Mac/Linux/Poolrechner: python3 vorkurs_quiz.py

Optionen:
   --keine-farben   falls im Terminal komische Zeichen wie [92m auftauchen
   --selbsttest     prüft alle Musterlösungen (nur für Neugierige)

Benötigt Python 3.10 oder neuer (wegen 'match'). Keine Zusatzpakete nötig.

ACHTUNG: Weiter unten in dieser Datei stehen alle Lösungen.
Nicht spicken – erst spielen! ;-)
"""

import contextlib
import io
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap

# ════════════════════════════════════════════════════════════════════════════
#  TEIL 1: DIE QUIZ-MASCHINE
#  (Das ist der "Motor" des Quiz. Du musst ihn nicht verstehen – aber am Ende
#   des Vorkurses kannst du fast alles hier drin lesen!)
# ════════════════════════════════════════════════════════════════════════════

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

if os.name == "nt":
    os.system("")  # schaltet die Farben in der Windows-Konsole frei

FARBE_AN = "--keine-farben" not in sys.argv and sys.stdout.isatty()
BREITE = 78


def _farbe(code):
    def faerben(text):
        return f"\033[{code}m{text}\033[0m" if FARBE_AN else str(text)
    return faerben


fett = _farbe("1")
gruen = _farbe("92")
rot = _farbe("91")
gelb = _farbe("93")
blau = _farbe("94")
cyan = _farbe("96")
grau = _farbe("90")
magenta = _farbe("95")


class ZurueckZumMenue(Exception):
    """Wird ausgelöst, wenn man 'menü' tippt oder Strg+C drückt."""


MENUE_WOERTER = {"menü", "menue", "q", "quit", "exit"}


def eingabe(prompt=""):
    """Wie input(), aber 'menü' oder Strg+C bringen dich zurück ins Hauptmenü."""
    try:
        antwort = input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        raise ZurueckZumMenue()
    if antwort.strip().lower() in MENUE_WOERTER:
        raise ZurueckZumMenue()
    return antwort


def weiter(text="[Enter] = weiter"):
    eingabe(grau(f"\n  {text} "))


def text_ausgeben(text, einzug="  ", stil=None):
    """Gibt einen Text formatiert aus.
       '## '  am Zeilenanfang  -> Überschrift
       '!! '  am Zeilenanfang  -> Merksatz (gelb)
       4 Leerzeichen am Anfang -> Code (farbig)"""
    for zeile in textwrap.dedent(text).strip("\n").splitlines():
        if zeile.startswith("## "):
            print(einzug + fett(blau(zeile[3:])))
        elif zeile.startswith("!! "):
            print(einzug + gelb(fett("★ ") + zeile[3:]))
        elif zeile.startswith("    "):
            print(einzug + cyan(zeile))
        else:
            print(einzug + (stil(zeile) if stil and zeile.strip() else zeile))


def code_zeigen(code, einzug="  "):
    code = textwrap.dedent(code).strip("\n")
    print(einzug + grau("┌" + "─" * 58))
    for zeile in code.splitlines():
        print(einzug + grau("│ ") + cyan(zeile))
    print(einzug + grau("└" + "─" * 58))


def norm_text(s):
    """Vereinheitlicht eine Textantwort (Groß/klein, Leerzeichen, Anführungszeichen egal)."""
    s = s.strip().lower().strip("'\"` ").rstrip(".!")
    return re.sub(r"\s+", "", s)


def norm_ausgabe(s):
    """Vereinheitlicht eine Konsolenausgabe für den Vergleich:
       Zeilenumbrüche/Leerzeichen/Kommas zählen gleich, " und ' sind egal."""
    s = s.strip().replace('"', "'")
    s = re.sub(r"[\s,]+", " ", s).strip()
    s = re.sub(r"\b(true|false|none)\b", lambda m: m.group(1).capitalize(),
               s, flags=re.IGNORECASE)
    return s


def ohne_anfuehrungszeichen(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "'\"":
        return s[1:-1]
    return s


_AUSGABE_CACHE = {}


def fuehre_aus(code):
    """Führt einen Beispielcode aus und merkt sich, was er ausgibt
       (und ob ein Fehler auftritt). So sind die Lösungen immer korrekt."""
    code = textwrap.dedent(code).strip("\n")
    if code in _AUSGABE_CACHE:
        return _AUSGABE_CACHE[code]
    puffer = io.StringIO()
    fehler = None
    alter_ordner = os.getcwd()
    tmp = tempfile.mkdtemp(prefix="vorkurs_quiz_")
    try:
        os.chdir(tmp)
        with contextlib.redirect_stdout(puffer):
            exec(compile(code, "<beispiel>", "exec"), {"__name__": "__main__"})
    except Exception as e:  # z.B. SyntaxError, TypeError, RecursionError ...
        fehler = type(e).__name__
    finally:
        os.chdir(alter_ordner)
        shutil.rmtree(tmp, ignore_errors=True)
    ergebnis = (puffer.getvalue().rstrip("\n"), fehler)
    _AUSGABE_CACHE[code] = ergebnis
    return ergebnis


LOB = ["Richtig!", "Super!", "Genau so!", "Klasse!", "Volltreffer!", "Stark!",
       "Perfekt!", "Sehr gut!", "Läuft bei dir!", "Exzellent!"]


def rueckmeldung(ok, erklaerung="", loesung=None):
    print()
    if ok:
        print("  " + gruen(fett("✔ " + random.choice(LOB))))
    else:
        print("  " + rot(fett("✘ Leider nicht richtig.")))
        if loesung is not None:
            print("  " + fett("Richtige Antwort: ") + gruen(loesung))
    if erklaerung:
        print()
        print("  " + gelb(fett("Erklärung:")))
        text_ausgeben(erklaerung, einzug="    ")


# ──────────────────────────────────────────────────────────────────────────
#  Die verschiedenen Arten von Kapitel-Elementen
# ──────────────────────────────────────────────────────────────────────────

class Erklaerung:
    """Ein Lernabschnitt, der VOR den Fragen zu einem neuen Thema kommt.
       '---' in einer eigenen Zeile trennt Seiten."""

    def __init__(self, titel, text):
        self.titel = titel
        self.text = text

    def zeigen(self):
        seiten = re.split(r"\n[ \t]*---[ \t]*\n", textwrap.dedent(self.text).strip("\n"))
        for nr, seite in enumerate(seiten, 1):
            print()
            print(magenta("═" * BREITE))
            kopf = f"  NEUES THEMA: {self.titel}"
            if len(seiten) > 1:
                kopf += f"   (Seite {nr}/{len(seiten)})"
            print(fett(magenta(kopf)))
            print(magenta("═" * BREITE))
            print()
            text_ausgeben(seite)
            weiter()


class Frage:
    art = "Frage"
    ist_code_aufgabe = False

    def __init__(self, erklaerung="", tipp=None, code=None):
        self.erklaerung = erklaerung
        self.tipp = tipp
        self.code = code
        self.id = None
        self.kapitel = None

    def kopf(self, nr, gesamt):
        print()
        print(blau("─" * BREITE))
        print("  " + fett(blau(f"Frage {nr}/{gesamt}")) + grau(f"   ·   {self.art}"))
        print(blau("─" * BREITE))

    def tipp_zeigen(self):
        if self.tipp:
            print("  " + gelb("Tipp: ") + self.tipp)
        else:
            print("  " + grau("Für diese Frage gibt es leider keinen Tipp."))

    def stellen(self, nr, gesamt):
        raise NotImplementedError


class MC(Frage):
    """Multiple Choice. Die ERSTE Option in der Liste ist immer die richtige –
       beim Anzeigen werden die Optionen gemischt."""
    art = "Multiple Choice"

    def __init__(self, frage, optionen, erklaerung="", code=None, tipp=None):
        super().__init__(erklaerung, tipp, code)
        self.frage = frage
        self.optionen = list(optionen)

    def stellen(self, nr, gesamt):
        self.kopf(nr, gesamt)
        reihenfolge = self.optionen[:]
        random.shuffle(reihenfolge)
        richtig = reihenfolge.index(self.optionen[0])
        buchstaben = "abcdefgh"[:len(reihenfolge)]
        print()
        text_ausgeben(self.frage, stil=fett)
        if self.code:
            print()
            code_zeigen(self.code)
        print()
        for b, option in zip(buchstaben, reihenfolge):
            print(f"    {fett(b + ')')} {option}")
        print()
        while True:
            a = eingabe(f"  Deine Wahl ({'/'.join(buchstaben)}, ? = Tipp): ").strip().lower()
            if a == "?":
                self.tipp_zeigen()
                continue
            if a in ("x", "weiß nicht", "weiss nicht"):
                wahl = -1
                break
            if len(a) == 1 and a in buchstaben:
                wahl = buchstaben.index(a)
                break
            if a.isdigit() and 1 <= int(a) <= len(reihenfolge):
                wahl = int(a) - 1
                break
            print("  " + grau(f"Bitte tippe einen der Buchstaben {', '.join(buchstaben)} ein."))
        ok = wahl == richtig
        rueckmeldung(ok, self.erklaerung, None if ok else f"{buchstaben[richtig]}) {reihenfolge[richtig]}")
        return ok


class WahrFalsch(Frage):
    art = "Wahr oder falsch?"

    def __init__(self, aussage, wahr, erklaerung="", code=None, tipp=None):
        super().__init__(erklaerung, tipp, code)
        self.aussage = aussage
        self.wahr = wahr

    def stellen(self, nr, gesamt):
        self.kopf(nr, gesamt)
        print()
        print("  " + grau("Stimmt diese Aussage?"))
        text_ausgeben(self.aussage, stil=fett)
        if self.code:
            print()
            code_zeigen(self.code)
        print()
        while True:
            a = eingabe("  w = wahr, f = falsch (? = Tipp): ").strip().lower()
            if a == "?":
                self.tipp_zeigen()
                continue
            if a in ("w", "wahr", "j", "ja", "true", "t", "1", "richtig", "stimmt"):
                antwort = True
                break
            if a in ("f", "falsch", "n", "nein", "false", "0", "stimmt nicht"):
                antwort = False
                break
            print("  " + grau("Bitte w oder f eingeben."))
        ok = antwort == self.wahr
        rueckmeldung(ok, self.erklaerung, None if ok else ("WAHR" if self.wahr else "FALSCH"))
        return ok


class Textfrage(Frage):
    """Freie Antwort. 'antworten' ist eine Liste von akzeptierten Antworten."""
    art = "Antwort eintippen"

    def __init__(self, frage, antworten, erklaerung="", tipp=None, code=None):
        super().__init__(erklaerung, tipp, code)
        self.frage = frage
        self.antworten = list(antworten)

    def stellen(self, nr, gesamt):
        self.kopf(nr, gesamt)
        print()
        text_ausgeben(self.frage, stil=fett)
        if self.code:
            print()
            code_zeigen(self.code)
        print()
        gueltig = {norm_text(x) for x in self.antworten}
        for versuch in (1, 2):
            while True:
                a = eingabe("  Deine Antwort (? = Tipp, x = weiß nicht): ")
                if a.strip() == "?":
                    self.tipp_zeigen()
                    continue
                if a.strip():
                    break
            if a.strip().lower() in ("x", "weiß nicht", "weiss nicht"):
                break
            if norm_text(a) in gueltig:
                rueckmeldung(True, self.erklaerung)
                return versuch == 1
            if versuch == 1:
                print("  " + gelb("Nicht ganz – du hast noch einen Versuch!"))
                if self.tipp:
                    self.tipp_zeigen()
        rueckmeldung(False, self.erklaerung, self.antworten[0])
        return False


class Ausgabe(Frage):
    """'Was gibt dieser Code aus?' – die richtige Lösung wird durch echtes
       Ausführen des Codes ermittelt."""
    art = "Was gibt der Code aus?"
    _hinweis_gezeigt = False

    def __init__(self, code, erklaerung="", frage=None, tipp=None, akzeptiert=()):
        super().__init__(erklaerung, tipp, code)
        self.frage = frage or "Was gibt dieser Code in der Konsole aus?"
        self.akzeptiert = list(akzeptiert)

    def soll(self):
        return fuehre_aus(self.code)

    def loesungstext(self):
        ausgabe, fehler = self.soll()
        if fehler:
            return (ausgabe.replace("\n", " | ") + "  →  " if ausgabe else "") + f"Fehler: {fehler}"
        return ausgabe.replace("\n", "  ⏎  ") if ausgabe else "(gar nichts)"

    def pruefen(self, a):
        ausgabe, fehler = self.soll()
        if fehler:
            klein = a.lower()
            return fehler.lower() in klein or norm_text(a) in ("fehler", "error", "exception")
        kandidaten = {norm_ausgabe(a), norm_ausgabe(ohne_anfuehrungszeichen(a))}
        richtig = {norm_ausgabe(ausgabe)} | {norm_ausgabe(x) for x in self.akzeptiert}
        if not ausgabe and norm_text(a) in ("", "nichts", "garnichts", "leer", "keineausgabe"):
            return True
        return bool(kandidaten & richtig)

    def stellen(self, nr, gesamt):
        self.kopf(nr, gesamt)
        print()
        text_ausgeben(self.frage, stil=fett)
        print()
        code_zeigen(self.code)
        if not Ausgabe._hinweis_gezeigt:
            print(grau("  So antwortest du:"))
            print(grau("   • Mehrere Ausgabezeilen? Einfach mit Leerzeichen getrennt eintippen."))
            print(grau("   • Gibt es einen Fehler? Dann tippe den Namen des Fehlers (z.B. TypeError)."))
            print(grau("   • ? = Tipp   ·   x = weiß nicht"))
            Ausgabe._hinweis_gezeigt = True
        else:
            print(grau("  (mehrere Zeilen → mit Leerzeichen trennen · Fehler → Fehlername · ? = Tipp)"))
        print()
        for versuch in (1, 2):
            while True:
                a = eingabe("  Ausgabe: ")
                if a.strip() == "?":
                    self.tipp_zeigen()
                    continue
                if a.strip():
                    break
            if a.strip().lower() in ("x", "weiß nicht", "weiss nicht"):
                break
            if self.pruefen(a):
                ausgabe, fehler = self.soll()
                if fehler and fehler.lower() not in a.lower():
                    print("  " + gelb(f"Richtig, es gibt einen Fehler! Sein Name ist: {fehler} – merk ihn dir."))
                rueckmeldung(True, self.erklaerung)
                return versuch == 1
            if versuch == 1:
                if "," in a and self.pruefen(a.replace(",", ".")):
                    print("  " + gelb("Fast! Achtung: Python schreibt Kommazahlen mit PUNKT, nicht mit Komma."))
                else:
                    print("  " + gelb("Nicht ganz – du hast noch einen Versuch!"))
                if self.tipp:
                    self.tipp_zeigen()
        rueckmeldung(False, self.erklaerung, self.loesungstext())
        return False


class Ausdruck(Frage):
    """Der Nutzer tippt einen Python-Ausdruck ein, der dann ausgewertet wird.
       'tests' ist eine Liste von Variablenbelegungen (Dictionaries)."""
    art = "Python-Ausdruck schreiben"

    def __init__(self, frage, tests, loesung, erklaerung="", tipp=None, muss_enthalten=None):
        super().__init__(erklaerung, tipp)
        self.frage = frage
        self.tests = tests
        self.loesung = loesung
        self.muss_enthalten = muss_enthalten

    @staticmethod
    def auswerten(ausdruck, variablen):
        import copy
        return eval(ausdruck, {"__builtins__": __builtins__}, copy.deepcopy(variablen))

    def pruefen(self, a):
        if self.muss_enthalten and self.muss_enthalten not in a:
            return False, f"Dein Ausdruck soll '{self.muss_enthalten}' verwenden."
        for variablen in self.tests:
            soll = self.auswerten(self.loesung, variablen)
            try:
                ist = self.auswerten(a, variablen)
            except Exception as e:
                return False, f"Dein Ausdruck erzeugt einen Fehler: {type(e).__name__}: {e}"
            if ist != soll or type(ist) != type(soll):
                belegung = ", ".join(f"{k} = {v!r}" for k, v in variablen.items())
                return False, f"Bei {belegung} liefert dein Ausdruck {ist!r}, erwartet war {soll!r}."
        return True, ""

    def stellen(self, nr, gesamt):
        self.kopf(nr, gesamt)
        print()
        text_ausgeben(self.frage, stil=fett)
        belegung = self.tests[0]
        print()
        print(grau("  Gegeben ist:"))
        code_zeigen("\n".join(f"{k} = {v!r}" for k, v in belegung.items()))
        print(grau("  Tippe einen Python-Ausdruck ein (z.B. lst[0] + 1). ? = Tipp, x = weiß nicht"))
        print()
        for versuch in (1, 2):
            while True:
                a = eingabe("  Ausdruck: ").strip()
                if a == "?":
                    self.tipp_zeigen()
                    continue
                if a:
                    break
            if a.lower() in ("x", "weiß nicht", "weiss nicht"):
                break
            ok, meldung = self.pruefen(a)
            if ok:
                ergebnis = self.auswerten(a, belegung)
                print("  " + grau(f"Dein Ausdruck ergibt: {ergebnis!r}"))
                rueckmeldung(True, self.erklaerung)
                if norm_text(a) != norm_text(self.loesung):
                    print("    " + grau(f"(Eine mögliche Musterlösung wäre: {self.loesung})"))
                return versuch == 1
            print("  " + gelb(meldung))
            if versuch == 1:
                print("  " + gelb("Du hast noch einen Versuch!"))
                if self.tipp:
                    self.tipp_zeigen()
        soll = self.auswerten(self.loesung, belegung)
        rueckmeldung(False, self.erklaerung, f"{self.loesung}     (ergibt {soll!r})")
        return False


# ──────────────────────────────────────────────────────────────────────────
#  Programmieraufgaben: Dein Code wird in einem eigenen Python-Prozess
#  ausgeführt und mit Testfällen geprüft.
# ──────────────────────────────────────────────────────────────────────────

_AUS_LOESUNG = object()


class Test:
    """Ein Testfall für eine Programmieraufgabe.
       eingaben       : Liste von Texten, die dein Programm per input() bekommt
       erwartet       : Texte, die am Ende einer Ausgabezeile stehen müssen
       nicht          : Texte, die NICHT in der Ausgabe vorkommen dürfen
       exakt          : Liste der Zeilen, die genau so ausgegeben werden müssen
       vorspann       : Code, der VOR deinem Code ausgeführt wird (z.B. eine Liste)
       nachspann      : Code, der NACH deinem Code ausgeführt wird (Prüfung)
       aufruf / soll  : Funktionstest – aufruf muss soll liefern"""

    def __init__(self, eingaben=(), erwartet=(), nicht=(), exakt=None, vorspann="",
                 nachspann="", aufruf=None, soll=_AUS_LOESUNG, beschreibung=None):
        self.eingaben = [str(e) for e in eingaben]
        self.erwartet = list(erwartet)
        self.nicht = list(nicht)
        self.exakt = exakt
        self.vorspann = textwrap.dedent(vorspann).strip("\n")
        self.nachspann = textwrap.dedent(nachspann).strip("\n")
        self.aufruf = aufruf
        self.soll = soll
        self.beschreibung = beschreibung


def P(eingaben=(), erwartet=(), nicht=(), exakt=None, vorspann="", nachspann="", beschreibung=None):
    """Test für ein ganzes Programm (mit Eingaben und erwarteter Ausgabe)."""
    return Test(eingaben, erwartet, nicht, exakt, vorspann, nachspann, beschreibung=beschreibung)


def F(aufruf, soll=_AUS_LOESUNG, vorspann=""):
    """Test für eine Funktion: aufruf (z.B. 'fakultaet(5)') muss soll ergeben.
       Ohne soll wird der richtige Wert aus der Musterlösung berechnet."""
    return Test(vorspann=vorspann, aufruf=aufruf, soll=soll)


_HARNESS = '''
import math as _quiz_math
def _quiz_gleich(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return _quiz_math.isclose(a, b, rel_tol=1e-4, abs_tol=1e-6)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_quiz_gleich(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_quiz_gleich(a[k], b[k]) for k in b)
    return a == b
print()
try:
    _quiz_erg = __AUFRUF__
except Exception as _quiz_e:
    print("@@FEHLER@@" + type(_quiz_e).__name__ + ": " + str(_quiz_e))
else:
    print(("@@OK@@" if _quiz_gleich(_quiz_erg, __SOLL__) else "@@FALSCH@@") + repr(_quiz_erg))
'''


def programm_starten(quelltext, eingabe_text="", timeout=6):
    """Startet Code in einem eigenen Python-Prozess (in einem leeren Ordner)."""
    tmp = tempfile.mkdtemp(prefix="vorkurs_quiz_")
    try:
        pfad = os.path.join(tmp, "dein_code.py")
        with open(pfad, "w", encoding="utf-8") as f:
            f.write(quelltext)
        umgebung = dict(os.environ, PYTHONIOENCODING="utf-8")
        try:
            r = subprocess.run([sys.executable, "-X", "utf8", pfad], input=eingabe_text,
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=timeout, cwd=tmp, env=umgebung)
        except subprocess.TimeoutExpired:
            return None, "", "TIMEOUT"
        return r.returncode, r.stdout, r.stderr
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def fehler_kurz(stderr, offset, anzahl_zeilen):
    zeilen = [z for z in stderr.strip().splitlines() if z.strip()]
    if not zeilen:
        return "Unbekannter Fehler"
    meldung = zeilen[-1].strip()
    nummer = None
    for z in zeilen:
        m = re.search(r'dein_code\.py", line (\d+)', z)
        if m:
            nummer = int(m.group(1)) - offset
    if nummer and 1 <= nummer <= anzahl_zeilen:
        meldung += f"   (in deiner Zeile {nummer})"
    if "EOFError" in meldung:
        meldung += "\n      → Dein Programm wollte öfter input() aufrufen, als es Eingaben gab."
    return meldung


def _norm_zeile(z):
    z = re.sub(r"\s+", " ", z.strip().lower())
    return z.rstrip(" .!?:")


def _endet_mit(zeile, erwartet):
    if zeile == erwartet:
        return True
    if zeile.endswith(erwartet):
        vorher = zeile[-len(erwartet) - 1]
        return not (vorher.isalnum() or vorher in ".-_")
    return False


def test_ausfuehren(nutzercode, t, loesung):
    """Führt einen Test aus. Rückgabe: (bestanden, Meldung)."""
    nachspann = t.nachspann
    if t.aufruf:
        soll = t.soll
        if soll is _AUS_LOESUNG:
            soll = loesungswert(loesung, t)
        nachspann = _HARNESS.replace("__AUFRUF__", t.aufruf).replace("__SOLL__", repr(soll))
    teile = [x for x in (t.vorspann, nutzercode, nachspann) if x]
    offset = len(t.vorspann.splitlines()) if t.vorspann else 0
    eingabe_text = "\n".join(t.eingaben) + "\n" if t.eingaben else ""
    code, out, err = programm_starten("\n".join(teile) + "\n", eingabe_text)
    if code is None:
        return False, "Dein Programm lief länger als 6 Sekunden – vermutlich eine Endlosschleife!"
    fehler = fehler_kurz(err, offset, len(nutzercode.splitlines())) if code != 0 else ""

    if t.aufruf:
        if "@@OK@@" in out:
            return True, ""
        if "@@FALSCH@@" in out:
            ist = out.split("@@FALSCH@@")[-1].strip().splitlines()[0]
            return False, f"{t.aufruf} sollte {soll!r} liefern – dein Ergebnis: {ist}"
        if "@@FEHLER@@" in out:
            meldung = out.split("@@FEHLER@@")[-1].strip().splitlines()[0]
            return False, f"Beim Aufruf {t.aufruf} gab es einen Fehler: {meldung}"
        return False, f"Dein Code ist abgestürzt, bevor getestet werden konnte:\n      {fehler}"

    if code != 0:
        return False, f"Dein Programm ist mit einem Fehler abgestürzt:\n      {fehler}"
    zeilen = [_norm_zeile(z) for z in out.splitlines() if z.strip()]
    ausgabe_kurz = "\n".join("      │ " + z for z in out.strip().splitlines()[:15]) or "      │ (nichts)"
    info = ""
    if t.eingaben:
        info = f"   Eingaben: {', '.join(t.eingaben)}\n"
    if t.beschreibung:
        info = f"   Test: {t.beschreibung}\n" + info
    if t.exakt is not None:
        soll_zeilen = [_norm_zeile(z) for z in t.exakt]
        if zeilen != soll_zeilen:
            return False, (info + "   Erwartet wurden genau diese Zeilen:\n" +
                           "\n".join("      │ " + z for z in t.exakt) +
                           "\n   Deine Ausgabe war:\n" + ausgabe_kurz)
    for e in t.erwartet:
        if not any(_endet_mit(z, _norm_zeile(e)) for z in zeilen):
            return False, (info + f"   Erwartet wurde eine Zeile, die mit \"{e}\" endet.\n"
                           "   Deine Ausgabe war:\n" + ausgabe_kurz)
    for n in t.nicht:
        if any(n.lower() in z for z in zeilen):
            return False, (info + f"   \"{n}\" hätte hier NICHT ausgegeben werden dürfen.\n"
                           "   Deine Ausgabe war:\n" + ausgabe_kurz)
    return True, ""


_LOESUNGSWERTE = {}


def loesungswert(loesung, t):
    """Berechnet den erwarteten Rückgabewert eines Funktionsaufrufs mit der Musterlösung."""
    schluessel = (loesung, t.vorspann, t.aufruf)
    if schluessel not in _LOESUNGSWERTE:
        alter_ordner = os.getcwd()
        tmp = tempfile.mkdtemp(prefix="vorkurs_quiz_")
        try:
            os.chdir(tmp)
            ns = {"__name__": "__loesung__"}
            with contextlib.redirect_stdout(io.StringIO()):
                if t.vorspann:
                    exec(t.vorspann, ns)
                exec(textwrap.dedent(loesung), ns)
                _LOESUNGSWERTE[schluessel] = eval(t.aufruf, ns)
        finally:
            os.chdir(alter_ordner)
            shutil.rmtree(tmp, ignore_errors=True)
    return _LOESUNGSWERTE[schluessel]


class CodeAufgabe(Frage):
    art = "Programmieraufgabe"
    ist_code_aufgabe = True

    def __init__(self, aufgabe, tests, loesung, erklaerung="", tipp=None, vorlage=None):
        super().__init__(erklaerung, tipp)
        self.aufgabe = aufgabe
        self.tests = tests
        self.loesung = textwrap.dedent(loesung).strip("\n")
        self.vorlage = vorlage

    def alle_tests(self, nutzercode):
        for t in self.tests:
            ok, meldung = test_ausfuehren(nutzercode, t, self.loesung)
            if not ok:
                return False, meldung
        return True, ""

    @staticmethod
    def code_einlesen():
        print(grau("  Tippe deinen Code Zeile für Zeile ein (Einrückung = 4 Leerzeichen)."))
        print(grau("  Fertig? Dann schreibe in eine neue Zeile nur:  ") + fett("ENDE"))
        print(grau("  Längerer Code? Schreib ihn in einem Editor, speichere ihn und tippe:  ")
              + fett("DATEI meinpfad.py"))
        print(grau("  Statt Code geht auch:  ? = Tipp   ·   LÖSUNG = Musterlösung   ·   SKIP = überspringen"))
        zeilen = []
        while True:
            z = eingabe(cyan(">>> " if not zeilen else "... "))
            befehl = z.strip()
            if not zeilen and befehl.upper() in ("?", "LÖSUNG", "LOESUNG", "SKIP"):
                return befehl.upper().replace("OE", "Ö")
            if not zeilen and befehl.upper().startswith("DATEI "):
                pfad = befehl[6:].strip().strip('"').strip("'")
                try:
                    with open(pfad, encoding="utf-8") as f:
                        inhalt = f.read().expandtabs(4)
                    print(grau(f"  ({len(inhalt.splitlines())} Zeilen aus {pfad} geladen)"))
                    return inhalt
                except OSError as e:
                    print(rot(f"  Datei konnte nicht gelesen werden: {e}"))
                    continue
            if befehl.upper() == "ENDE":
                break
            zeilen.append(z.expandtabs(4))
        return "\n".join(zeilen)

    def stellen(self, nr, gesamt):
        self.kopf(nr, gesamt)
        print()
        text_ausgeben(self.aufgabe)
        if self.vorlage:
            print()
            print(grau("  So kannst du anfangen:"))
            code_zeigen(self.vorlage)
        print()
        loesung_gesehen = False
        while True:
            code = self.code_einlesen()
            if code == "?":
                self.tipp_zeigen()
                continue
            if code == "SKIP":
                print("  " + grau("Übersprungen. Hier die Musterlösung zum Anschauen:"))
                code_zeigen(self.loesung)
                if self.erklaerung:
                    text_ausgeben(self.erklaerung, einzug="    ")
                return False
            if code == "LÖSUNG":
                loesung_gesehen = True
                print()
                print("  " + gelb(fett("Musterlösung:")))
                code_zeigen(self.loesung)
                if self.erklaerung:
                    text_ausgeben(self.erklaerung, einzug="    ")
                print("  " + grau("Tipp es jetzt gern selbst ab – Abtippen trainiert auch!"))
                continue
            if not code.strip():
                print("  " + grau("Du hast keinen Code eingegeben."))
                continue
            print("  " + grau("Teste deinen Code ..."))
            ok, meldung = self.alle_tests(code)
            if ok:
                print("  " + gruen(fett(f"✔ Alle {len(self.tests)} Tests bestanden! " + random.choice(LOB))))
                print()
                print("  " + grau("Zum Vergleich die Musterlösung:"))
                code_zeigen(self.loesung)
                if self.erklaerung:
                    text_ausgeben(self.erklaerung, einzug="    ")
                return not loesung_gesehen
            print("  " + rot(fett("✘ Ein Test ist fehlgeschlagen:")))
            print(rot(meldung) if "\n" not in meldung else meldung)
            print()
            print("  " + grau("Kein Problem – Fehler sind normal! Versuch es nochmal."))


# ──────────────────────────────────────────────────────────────────────────
#  Kapitel
# ──────────────────────────────────────────────────────────────────────────

class Kapitel:
    def __init__(self, nummer, titel, beschreibung, quelle):
        self.nummer = nummer
        self.titel = titel
        self.beschreibung = beschreibung
        self.quelle = quelle
        self.elemente = []

    def _neu(self, element):
        if isinstance(element, Frage):
            element.id = f"K{self.nummer:02d}-{len(self.elemente):03d}"
            element.kapitel = self
        self.elemente.append(element)
        return element

    def fragen(self):
        return [e for e in self.elemente if isinstance(e, Frage)]

    # Abkürzungen, damit die Inhalte unten gut lesbar bleiben:
    def erklaerung(self, titel, text):
        return self._neu(Erklaerung(titel, text))

    def mc(self, frage, optionen, erklaerung="", code=None, tipp=None):
        return self._neu(MC(frage, optionen, erklaerung, code, tipp))

    def wf(self, aussage, wahr, erklaerung="", code=None, tipp=None):
        return self._neu(WahrFalsch(aussage, wahr, erklaerung, code, tipp))

    def text(self, frage, antworten, erklaerung="", tipp=None, code=None):
        return self._neu(Textfrage(frage, antworten, erklaerung, tipp, code))

    def ausgabe(self, code, erklaerung="", tipp=None, akzeptiert=(), frage=None):
        return self._neu(Ausgabe(code, erklaerung, frage, tipp, akzeptiert))

    def ausdruck(self, frage, tests, loesung, erklaerung="", tipp=None, muss_enthalten=None):
        return self._neu(Ausdruck(frage, tests, loesung, erklaerung, tipp, muss_enthalten))

    def code(self, aufgabe, tests, loesung, erklaerung="", tipp=None, vorlage=None):
        return self._neu(CodeAufgabe(aufgabe, tests, loesung, erklaerung, tipp, vorlage))


KAPITEL = []


def neues_kapitel(titel, beschreibung, quelle):
    k = Kapitel(len(KAPITEL) + 1, titel, beschreibung, quelle)
    KAPITEL.append(k)
    return k


# ════════════════════════════════════════════════════════════════════════════
#  TEIL 2: DIE LERNINHALTE
# ════════════════════════════════════════════════════════════════════════════

# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 1: Wie Computer "denken"
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Wie Computer 'denken' – Programme & Python",
    "Was ist ein Programm? Was ist Python? Ein bisschen Geschichte.",
    "Vorlesung 1")

k.erklaerung("Was ist ein Computer eigentlich?", r"""
    ## Der Computer – ein superschneller, aber völlig phantasieloser Koch

    Stell dir einen Koch vor, der ...
      • kein Deutsch und kein Englisch versteht – nur ganz exakte Anweisungen,
      • eigentlich nur rechnen kann (für ihn ist ALLES Mathematik),
      • immer genau einen Arbeitsschritt nach dem anderen erledigt,
      • dafür aber unfassbar schnell ist (Milliarden Schritte pro Sekunde!).

    Genau so ist ein Computer. Aus der Vorlesung:
      • Computer sprechen keine natürlichen Sprachen.
      • Computer sind rein-mathematische Maschinen.
      • Computer rechnen Arbeitsschritt für Arbeitsschritt.
      • Computer sind extrem schnell ... also wirklich schnell.

    !! Ein Computer macht IMMER genau das, was du schreibst – nicht das, was du meinst.
    ---
    ## Was ist ein Programm?

    Ein Programm ist eine Abfolge von Arbeitsschritten in einer fest
    definierten Schreibweise. Das ist wie ein KOCHREZEPT:

      Rezept "Spiegelei"            Programm
      1. Pfanne erhitzen            Schritt 1
      2. Öl hineingeben             Schritt 2
      3. Ei aufschlagen             Schritt 3
      4. 4 Minuten warten           Schritt 4

    Die genaue Schreibweise (also die "Grammatik" des Rezepts) wird von der
    PROGRAMMIERSPRACHE festgelegt. Es gibt unzählige Programmiersprachen
    (Python, Java, C, Haskell, ...) – es gibt nicht DIE eine Sprache.

    In diesem Vorkurs benutzen wir PYTHON.
    ---
    ## Python – unsere Sprache

    Ein Python-Programm ist einfach nur TEXT. Diesen Text nennt man
    QUELLTEXT (englisch: Source Code).

    Ein Programm namens "Python-Interpreter" liest diesen Text und
    übersetzt ihn in Anweisungen, die der Computer ausführen kann.
    (Wie ein Dolmetscher zwischen dir und dem Computer.)

    Der Ablauf ist also immer:
      1. Der Mensch schreibt ein Programm als Python-Quelltext.
      2. Python übersetzt den Quelltext in Anweisungen für den Computer.
      3. Der Computer führt die Anweisungen aus.
    ---
    ## Zwei Wege, Python zu benutzen

    WEG 1: Direkt in der Python-Konsole (zum Ausprobieren).
    Du startest sie im Terminal mit "python" (Windows) bzw. "python3"
    (Mac/Linux und auf den Poolrechnern der Uni). Du erkennst sie an >>>
        > python3
        Python 3.13.7 ...
        >>> print("Hello, World!")
        Hello, World!
        >>> 1 + 2 * 3
        7

    WEG 2: Code in eine Datei schreiben (z.B. hallo.py) und ausführen:
        python3 hallo.py

    Zum Schreiben reicht ein ganz normaler Texteditor – eine große
    Entwicklungsumgebung (IDE) braucht man im Vorkurs nicht.
    ---
    ## Ein bisschen Geschichte

      • Früher wurden Programme auf LOCHKARTEN gestanzt und von einem
        Lochkartenleser eingelesen – jedes Loch war eine Information.
      • Konrad Zuse baute 1941 die Z3 – den ersten funktionsfähigen,
        frei programmierbaren Digitalrechner der Welt.
      • 1957 füllten Computer noch ganze Räume ("Rechenzentren").
      • Margaret Hamilton leitete die Entwicklung der Software für die
        Apollo-11-Mission (erste Mondlandung 1969). Berühmt ist das Foto,
        auf dem sie neben einem Stapel Programmcode steht, der so groß
        ist wie sie selbst.
    ---
    ## Wenn du nicht weiterkommst

    Die Empfehlung aus dem Vorkurs, in dieser Reihenfolge:
      1. Die Fehlermeldung nochmal GENAU lesen.
      2. In der Vorlesung nach einer Lösung suchen.
      3. Mit einer Suchmaschine nach dem Problem suchen (nicht mit KI!).
      4. Einen Tutor fragen.

    Nützlich:
      • help() – im Python-Interpreter eingebaut. Z.B. help(print) zeigt
        die Dokumentation zu print.
      • Strg + C – bricht ein laufendes Programm im Terminal ab
        (z.B. wenn es "hängt").

    !! Zur KI: Im Vorkurs und an der Uni im Normalfall nicht erlaubt.
    !! Du bist hier, um es SELBST zu lernen – und KI macht oft Fehler.
    """)

k.mc("Womit vergleicht die Vorlesung ein Programm?",
     ["Mit einem Kochrezept",
      "Mit einem Bauplan für ein Haus aus Lego",
      "Mit einer Landkarte",
      "Mit einem Wörterbuch"],
     "Ein Programm ist eine Abfolge von Arbeitsschritten in fest definierter "
     "Schreibweise – genau wie ein Kochrezept.")

k.wf("Ein Computer versteht direkt natürliche Sprachen wie Deutsch oder Englisch.", False,
     "Computer sprechen keine natürlichen Sprachen. Sie sind rein-mathematische "
     "Maschinen. Deshalb brauchen wir Programmiersprachen mit fester Schreibweise.")

k.wf("Es gibt genau eine richtige Programmiersprache, die alle benutzen.", False,
     "Es gibt unzählige Programmiersprachen (Python, Java, C, Haskell, ...). "
     "Es gibt nicht DIE eine Programmiersprache.")

k.wf("Ein Computer arbeitet Arbeitsschritt für Arbeitsschritt.", True,
     "Richtig – ein Schritt nach dem anderen, aber extrem schnell.")

k.mc("Wie nennt man den Text, den du als Programmierer schreibst?",
     ["Quelltext (Source Code)",
      "Maschinentext",
      "Binärbrief",
      "Lochkartentext"],
     "Python-Programme bestehen aus Text, der interpretiert wird. Diesen Text "
     "nennt man Quelltext oder auf Englisch Source Code.")

k.mc("Was macht der Python-Interpreter?",
     ["Er liest deinen Quelltext und übersetzt ihn in Anweisungen für den Computer",
      "Er übersetzt deinen Code ins Englische",
      "Er speichert deinen Code im Internet",
      "Er malt deinen Code bunt an"],
     "Mensch schreibt Quelltext → Python übersetzt ihn → Computer führt aus. "
     "Der Interpreter ist wie ein Dolmetscher.")

k.mc("Woran erkennst du, dass du in der interaktiven Python-Konsole bist?",
     [">>>", "C:\\>", "$", "###"],
     "Die Python-Konsole zeigt >>> als Eingabeaufforderung. Dort kannst du "
     "einzelne Befehle direkt ausprobieren.")

k.text("Welchen Befehl tippst du auf den Poolrechnern der Uni ins Terminal, um Python zu starten?",
       ["python3"],
       "Auf den Poolrechnern (und meist auf Mac/Linux) heißt der Befehl python3. "
       "Unter Windows heißt er meistens einfach python.",
       tipp="Es ist 'python' plus die Hauptversionsnummer.")

k.mc("Welche zwei Arten gibt es, Python-Code auszuführen?",
     ["Direkt in der Python-Konsole oder als Datei, die an Python übergeben wird",
      "Nur über das Internet oder per E-Mail",
      "Nur mit einer teuren Entwicklungsumgebung (IDE)",
      "Nur auf Lochkarten"],
     "Zum Ausprobieren: Konsole (>>>). Für richtige Programme: eine .py-Datei, "
     "z.B. 'python3 hallo.py'.")

k.mc("Wer leitete die Entwicklung der Software für die Apollo-11-Mondlandung?",
     ["Margaret Hamilton", "Konrad Zuse", "Ada Lovelace", "Alan Turing"],
     "Margaret Hamilton – das Foto mit dem riesigen Stapel Programmcode ist berühmt.")

k.mc("Welchen Rechner baute Konrad Zuse?",
     ["Die Z3", "Den Apple I", "Den ENIAC", "Die Lochkarte"],
     "Die Z3 (1941) gilt als erster funktionsfähiger, frei programmierbarer "
     "Digitalrechner der Welt.")

k.mc("Dein Programm 'hängt' im Terminal und hört nicht auf. Was drückst du?",
     ["Strg + C", "Strg + S", "Alt + Tab", "Strg + Z + Enter + Neustart"],
     "Mit Strg + C bricht man die Ausführung eines Programms im Terminal ab.")

k.text("Welche eingebaute Funktion zeigt dir im Python-Interpreter die Dokumentation an?",
       ["help", "help()"],
       "help() – z.B. help(print) erklärt dir die print-Funktion.",
       tipp="Englisch für 'Hilfe'.")

k.mc("Du bekommst eine Fehlermeldung. Was ist laut Vorkurs der ERSTE Schritt?",
     ["Die Fehlermeldung nochmal genau lesen",
      "Sofort einen Tutor fragen",
      "Die KI fragen",
      "Den Computer neu starten"],
     "Reihenfolge: 1. Fehlermeldung genau lesen, 2. in der Vorlesung suchen, "
     "3. Suchmaschine, 4. Tutor fragen.")

k.ausgabe('print("Hello, World!")',
          "print() gibt den Text zwischen den Anführungszeichen aus – "
          "die Anführungszeichen selbst werden nicht mit ausgegeben.")

k.ausgabe("print(1 + 2 * 3)",
          "Punkt vor Strich gilt auch in Python: erst 2 * 3 = 6, dann 1 + 6 = 7.")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 2: Datentypen
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Datentypen – Welche Art von Daten?",
    "bool, int, float, str, None und die Funktion type()",
    "Vorlesung 1, Übung 1")

k.erklaerung("Was sind Daten – und wer sind diese 'Typen'?", r"""
    ## Alles ist 0 und 1

    Im Computer wird alles als Binärzahl (nur 0 und 1) gespeichert.
    Das Problem: Der Computer weiß selbst nicht, was diese Bits BEDEUTEN.

    Beispiel aus der Vorlesung: Die Bits 01000001 können bedeuten:
      • die Zahl 65
      • oder den Buchstaben 'A'

    Alltagsbeispiel: Die Ziffern "0612" auf einem Zettel. Ist das ...
      • eine Uhrzeit (06:12 Uhr)?
      • ein Datum (6. Dezember)?
      • eine Zahl (612)?
      • eine Telefon-Vorwahl?
    Ohne zu wissen, WAS es ist, kannst du nichts damit anfangen.

    !! Der DATENTYP legt fest, wie die Daten interpretiert werden.
    ---
    ## Die 5 wichtigsten Datentypen im Vorkurs

      Typ       Bedeutung          Beispiele          Alltag
      ───────── ────────────────── ────────────────── ─────────────────────
      bool      Wahrheitswert      True, False        Lichtschalter an/aus
      int       Ganzzahl           177013, -2, 0      Anzahl Äpfel im Korb
      float     Fließkommazahl     21.5, -0.135       Preis 2.49, Temperatur
      str       Zeichenkette       "lorem", 'ipsum'   Name, Adresse, Text
      NoneType  Nulltyp            None               leeres Formularfeld

    Wichtige Stolperfallen:
      • True und False schreibt man mit GROSSEM Anfangsbuchstaben.
        true (klein) kennt Python nicht!
      • Kommazahlen schreibt man mit PUNKT: 2.5 – nicht 2,5
      • 10.0 ist ein float (wegen des Punkts), 10 ist ein int.
      • "5" in Anführungszeichen ist ein str (Text), keine Zahl!
      • None bedeutet "hier ist (noch) nichts".
    ---
    ## Den Typ herausfinden: type()

    Mit der Funktion type() kannst du Python fragen, welchen Typ ein Wert hat:
        >>> type(5)
        <class 'int'>
        >>> type(2.5)
        <class 'float'>
        >>> type("Hallo")
        <class 'str'>
        >>> type(True)
        <class 'bool'>
        >>> type(None)
        <class 'NoneType'>

    Alltagstipp: Eine Telefonnummer wie "0151 1234567" speichert man als
    Text (str). Man rechnet nicht damit, und die führende 0 würde bei
    einer Zahl verloren gehen.
    """)

k.mc("Welchen Datentyp hat der Wert 177013?",
     ["int", "float", "str", "bool"],
     "Eine ganze Zahl ohne Punkt und ohne Anführungszeichen ist ein int (integer = Ganzzahl).")

k.mc("Welchen Datentyp hat der Wert -0.135?",
     ["float", "int", "str", "NoneType"],
     "Der Punkt macht es zur Fließkommazahl: float.")

k.mc("Welchen Datentyp hat der Wert \"lorem\"?",
     ["str", "bool", "float", "int"],
     "Alles in Anführungszeichen (egal ob ' oder \") ist eine Zeichenkette: str.")

k.mc("Welchen Datentyp hat der Wert None?",
     ["NoneType", "bool", "str", "int"],
     "None ist der einzige Wert vom Typ NoneType – er bedeutet 'kein Wert'.")

k.mc("Du willst speichern, ob ein Laden gerade geöffnet hat. Welcher Typ passt?",
     ["bool", "int", "float", "str"],
     "Offen oder zu – also ja oder nein → Wahrheitswert: True oder False (bool).")

k.mc("Du willst die Anzahl der Personen in deiner WG speichern. Welcher Typ passt?",
     ["int", "float", "bool", "NoneType"],
     "Personen zählt man in ganzen Zahlen – es gibt keine 2,5 Mitbewohner. → int")

k.mc("Du willst den Preis einer Pizza speichern (8,50 €). Welcher Typ passt?",
     ["float", "int", "bool", "NoneType"],
     "Preise haben Nachkommastellen → float, geschrieben als 8.5 (mit Punkt!).")

k.mc("Du willst eine Handynummer wie 0151 2345678 speichern. Welcher Typ ist am sinnvollsten?",
     ["str", "int", "float", "bool"],
     "Mit Telefonnummern rechnet man nicht. Außerdem würde bei einer Zahl die "
     "führende 0 verschwinden. → als Text (str) speichern.")

k.mc("Wie schreibt man den Wahrheitswert 'wahr' in Python?",
     ["True", "true", "TRUE", "\"wahr\""],
     "Nur True mit großem T. 'true' (klein) kennt Python nicht → NameError.")

k.mc("Was bedeutet None?",
     ["Kein Wert / nichts vorhanden",
      "Die Zahl 0",
      "Falsch (False)",
      "Ein leerer Text"],
     "None ist ein eigener Wert für 'nichts'. Es ist NICHT dasselbe wie 0, "
     "False oder \"\" – auch wenn es sich manchmal ähnlich anfühlt.")

k.wf("Die Bits 01000001 können sowohl die Zahl 65 als auch den Buchstaben 'A' bedeuten.", True,
     "Genau deshalb gibt es Datentypen: Der Typ legt fest, wie die Bits interpretiert werden.")

k.wf("Der Computer weiß von selbst, wie er eine Folge von Bits verstehen soll.", False,
     "Nein – der Computer sieht nur 0 und 1. Erst der Datentyp gibt den Bits eine Bedeutung.")

k.wf("In Python schreibt man Kommazahlen mit einem Komma, also 3,5.", False,
     "Python schreibt Kommazahlen mit PUNKT: 3.5. Ein Komma trennt in Python "
     "verschiedene Werte voneinander.")

k.ausgabe("print(type(10.0))",
          "10.0 hat einen Punkt → float. Auch wenn der Wert 'eigentlich' ganz ist!",
          akzeptiert=["float"])

k.ausgabe("print(type(2))",
          "2 ist eine Ganzzahl → int.", akzeptiert=["int"])

k.ausgabe("print(type('Lorem'))",
          "Einfache Anführungszeichen erzeugen genauso einen str wie doppelte.",
          akzeptiert=["str"])

k.ausgabe('print(type("5"))',
          "\"5\" steht in Anführungszeichen → das ist TEXT, keine Zahl! Typ: str.",
          akzeptiert=["str"])

k.ausgabe("print(type(True))",
          "True ist ein Wahrheitswert → bool.", akzeptiert=["bool"])

k.ausgabe("print(type(true))",
          "true (klein geschrieben) ist KEIN gültiger Wert. Python denkt, das sei "
          "ein Variablenname, den es nicht gibt → NameError. Richtig wäre True.",
          tipp="Achte genau auf die Groß- und Kleinschreibung.")

k.ausgabe("print(type(None))",
          "None hat seinen ganz eigenen Typ: NoneType.", akzeptiert=["NoneType"])


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 3: Operatoren
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Rechnen mit Python – Operatoren",
    "+ - * / // % **, Reihenfolge der Auswertung und Vergleiche",
    "Vorlesung 1, Übung 1")

k.erklaerung("Mathematische Operatoren", r"""
    ## Python als Taschenrechner

      Operator  Bedeutung                     Beispiel
      ────────  ────────────────────────────  ──────────────
         +      Addition                      5 + 2   → 7
         -      Subtraktion                   5 - 2   → 3
         *      Multiplikation                5 * 2   → 10
         /      Division (IMMER float!)       5 / 2   → 2.5
         //     Ganzzahl-Division (abrunden)  5 // 2  → 2
         %      Modulo (der REST)             5 % 2   → 1
         **     Potenz                        5 ** 2  → 25
    ---
    ## Die drei Divisionen – mit Alltagsbeispielen

    /  NORMALE DIVISION – liefert IMMER eine Kommazahl (float):
       5 Pizzen für 2 Personen: 5 / 2 = 2.5 Pizzen pro Person.
       Achtung: Auch 4 / 2 ergibt 2.0 (nicht 2)!

    // GANZZAHL-DIVISION – "Wie oft passt es ganz rein?"
       Du hast 17 €, eine Kinokarte kostet 5 €:
       17 // 5 = 3  → du kannst 3 Karten kaufen.

    %  MODULO – "Was bleibt übrig?"
       17 % 5 = 2  → es bleiben 2 € übrig.

    !! In C, C++ oder Java ergibt 5 / 2 einfach 2. In Python ist es 2.5!
    !! Den Operator // gibt es so meist nur in Python.
    ---
    ## Wofür braucht man Modulo (%)?

    Super nützlich, um TEILBARKEIT zu prüfen:
    Ist der Rest 0, dann ist die Zahl teilbar.
        10 % 5 == 0     → True   (10 ist durch 5 teilbar)
        7 % 2 == 0      → False  (7 ist ungerade)
        8 % 2 == 0      → True   (8 ist gerade)

    Uhrzeit-Beispiel: Es ist 22 Uhr. Wie spät ist es in 5 Stunden?
        (22 + 5) % 24   → 3   (also 3 Uhr nachts)

    Potenz (**): 2 ** 10 = 1024. In anderen Sprachen schreibt man das
    meist als Funktion, z.B. pow(2, 10).
    ---
    ## Grenzen von Zahlen

      • Kurzschreibweise für große Zahlen: 1.6e6 bedeutet 1.6 · 10^6,
        also 1600000.0 (das Ergebnis ist ein float!).
      • Fließkommazahlen sind nicht unendlich genau. Berühmtes Beispiel:
            0.1 + 0.2   → 0.30000000000000004
        Das ist wie 1/3 = 0.3333... auf Papier: Irgendwann musst du
        aufhören zu schreiben, und es wird ungenau.
    ---
    ## Reihenfolge der Auswertung (Operatorpräzedenz)

    Wie in Mathe gilt "Punkt vor Strich". Die Reihenfolge, grob von
    "zuerst" nach "zuletzt":
      1. ( )                 Klammern
      2. **                  Potenz
      3. *  /  //  %         Punktrechnung
      4. +  -                Strichrechnung
      5. == != < > <= >=     Vergleiche
      6. not, dann and, dann or   (kommt im Logik-Kapitel)

    Beispiele aus der Vorlesung:
        3 + 5 * 2        → 13     (erst 5 * 2)
        (3 + 5) * 2      → 16     (Klammern zuerst)
        5 * 3 > 2 - 1    → True   (erst rechnen: 15 > 1, dann vergleichen)

    Tipp: Schau dir die Tabelle "Operator Precedence" in der Python-
    Dokumentation mindestens einmal an. Und im Zweifel: Klammern setzen!
    ---
    ## Vergleichsoperatoren

    Vergleiche liefern IMMER einen Wahrheitswert (True oder False).

      Schreibweise  Bedeutung         Beispiel   Ergebnis
      ────────────  ────────────────  ─────────  ────────
          ==        gleich            3 == 3     True
          !=        ungleich          5 != 5     False
          >         größer als        7 > 7      False
          >=        größer gleich     5 >= 5     True
          <         kleiner als       2 < 5      True
          <=        kleiner gleich    4 <= 4     True

    !! = ist eine ZUWEISUNG ("leg den Wert in die Kiste").
    !! == ist eine FRAGE ("Sind die beiden gleich?").
    """)

k.ausgabe("print(5 / 2)", "Die normale Division / ergibt eine Kommazahl: 2.5.")
k.ausgabe("print(4 / 2)",
          "Achtung Falle! / liefert IMMER einen float – also 2.0 und nicht 2.",
          tipp="Welchen Typ liefert der Operator / immer?")
k.ausgabe("print(5 // 2)", "// teilt und rundet ab: 5 // 2 = 2 (2.5 abgerundet).")
k.ausgabe("print(5 % 2)", "5 geteilt durch 2 ist 2 Rest 1. Modulo gibt den Rest: 1.")
k.ausgabe("print(5 ** 2)", "** ist die Potenz: 5 hoch 2 = 5 · 5 = 25.")
k.ausgabe("print(17 // 5)",
          "Kino-Beispiel: Mit 17 € kannst du 3 Karten zu je 5 € kaufen. 17 // 5 = 3.")
k.ausgabe("print(17 % 5)",
          "Und es bleiben 17 - 3·5 = 2 € übrig. 17 % 5 = 2.")
k.ausgabe("print(20 // 6)\nprint(20 % 6)",
          "20 Eier, Kartons für je 6 Eier: 3 volle Kartons (20 // 6 = 3), "
          "2 Eier bleiben übrig (20 % 6 = 2).",
          tipp="Wie viele volle 6er-Kartons, wie viele Eier übrig?")
k.ausgabe("print(16 + 26)", "Ganz normale Addition: 42. (Übung 1)")
k.ausgabe("print(12 * 123 // 28 - 15)",
          "Von links nach rechts bei gleichem Rang: 12 * 123 = 1476, dann "
          "1476 // 28 = 52 (52 · 28 = 1456, Rest 20), dann 52 - 15 = 37. (Übung 1)",
          tipp="* und // haben den gleichen Rang → von links nach rechts.")
k.ausgabe("print(5 * 3 + 6 * 6)", "Punkt vor Strich: 15 + 36 = 51. (Übung 1)")
k.ausgabe("print(2**6 + 2**3 + 2**1)",
          "Potenzen zuerst: 64 + 8 + 2 = 74. (Übung 1)")
k.ausgabe("print(13.75 + 28.67)",
          "Zwei floats addiert ergibt einen float. (Übung 1) "
          "Wundere dich nicht, wenn bei Kommazahlen manchmal winzige "
          "Rundungsfehler entstehen – das liegt an der begrenzten Genauigkeit.",
          akzeptiert=["42.42"])
k.ausgabe("print(5.4 * 7.7)",
          "Mathematisch wäre das 41.58. Python zeigt aber 41.580000000000005 – "
          "Fließkommazahlen haben eine begrenzte Genauigkeit! (Übung 1) "
          "Wenn du 41.58 getippt hast, lassen wir das gelten.",
          akzeptiert=["41.58"])
k.ausgabe("print(0.1 + 0.2)",
          "Das klassische Beispiel für die begrenzte Genauigkeit von "
          "Fließkommazahlen: 0.30000000000000004.",
          tipp="Es ist NICHT einfach 0.3 ...")
k.ausgabe("print(1.6e6)",
          "1.6e6 bedeutet 1.6 · 10^6 = 1600000. Weil es eine Kommazahl-"
          "Schreibweise ist, kommt ein float heraus: 1600000.0")
k.ausgabe("print(3 + 5 * 2)", "Punkt vor Strich: 5 * 2 = 10, dann 3 + 10 = 13.")
k.ausgabe("print((3 + 5) * 2)", "Klammern zuerst: 3 + 5 = 8, dann 8 * 2 = 16.")
k.ausgabe("print(5 * 3 > 2 - 1)",
          "Erst wird gerechnet (15 und 1), dann verglichen: 15 > 1 ist True.")
k.ausgabe("print((22 + 5) % 24)",
          "Uhrzeit-Rechnung: 27 % 24 = 3. Fünf Stunden nach 22 Uhr ist es 3 Uhr.")
k.ausgabe("print(10 % 5 == 0)",
          "10 % 5 ist 0 (kein Rest), und 0 == 0 ist True → 10 ist durch 5 teilbar.")
k.ausgabe("print(3 == 3)\nprint(5 != 5)",
          "3 == 3 ist True. 5 != 5 fragt 'Ist 5 ungleich 5?' → False.")
k.ausgabe("print(7 > 7)\nprint(5 >= 5)",
          "7 ist nicht GRÖSSER als 7 → False. Aber 5 ist größer ODER GLEICH 5 → True.")

k.mc("Mit welchem Ausdruck prüfst du, ob eine Zahl x gerade ist?",
     ["x % 2 == 0", "x / 2 == 0", "x // 2 == 1", "x ** 2 == 0"],
     "Gerade Zahlen lassen beim Teilen durch 2 keinen Rest: x % 2 == 0.")

k.text("20 Eier sollen in 6er-Kartons. Welchen Operator benutzt du, um die Anzahl "
       "VOLLER Kartons zu berechnen? (Nur den Operator eintippen)",
       ["//"],
       "20 // 6 = 3 volle Kartons. Für die übrigen Eier nähme man % (20 % 6 = 2).",
       tipp="Ganzzahl-Division.")

k.text("Und welchen Operator benutzt du, um zu berechnen, wie viele Eier ÜBRIG bleiben?",
       ["%"],
       "Modulo % liefert den Rest: 20 % 6 = 2.")

k.mc("Was ergibt 5 / 2 in den Sprachen C oder Java (mit Ganzzahlen)?",
     ["2", "2.5", "3", "Einen Fehler"],
     "In C, C++ und Java ist die Division zweier Ganzzahlen wieder eine Ganzzahl: 2. "
     "In Python ergibt 5 / 2 dagegen 2.5.")

k.wf("In Python ergibt der Ausdruck 5 / 2 den Wert 2.5.", True,
     "Richtig (Übung 1). Die Division mit / liefert in Python immer einen float.")

k.mc("Was ist der Unterschied zwischen = und == ?",
     ["= weist einen Wert zu, == vergleicht zwei Werte",
      "Es gibt keinen Unterschied",
      "= vergleicht, == weist zu",
      "== ist nur in Java erlaubt"],
     "x = 5 legt 5 in die Variable x. x == 5 fragt: 'Ist x gleich 5?' und ergibt True/False.")

k.mc("Was liefert ein Vergleich wie 3 < 7 immer?",
     ["Einen Wahrheitswert (True oder False)", "Eine Zahl", "Einen Text", "None"],
     "Vergleichsoperatoren liefern immer einen bool.")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 4: Variablen
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Variablen – Beschriftete Kisten",
    "Werte speichern, Namensregeln, snake_case, +=",
    "Vorlesung 1, Übung 1, Übung 2")

k.erklaerung("Was sind Variablen?", r"""
    ## Variablen = beschriftete Kisten

    Stell dir den Arbeitsspeicher als riesiges Lager mit Millionen Kisten
    vor. Jede Kiste hat eine Nummer wie 0x7ffeefbff5c8 – unmöglich zu merken.

    Eine VARIABLE ist ein NAMENSSCHILD, das du auf eine Kiste klebst.
    Dann musst du dir nur noch den Namen merken, nicht die Nummer.
    (Wie im Handy: Du speicherst "Mama" statt dir die Nummer zu merken.)

    So erstellst du eine Variable – mit einem einfachen =
        alter = 19
        name = "Lea"
        preis = 2.49

    Links steht der NAME, rechts der WERT. Python bestimmt den Typ
    automatisch anhand des Wertes (alter → int, name → str, ...).
    ---
    ## Rechte Seite zuerst!

    Bei einer Zuweisung wird IMMER zuerst die rechte Seite ausgerechnet,
    und dann wird das Ergebnis in die Kiste links gelegt.

        x = 5
        y = x * 3 + 3      # rechts: 5 * 3 + 3 = 18  → y ist 18
        y = y * 2          # rechts: 18 * 2 = 36    → y ist jetzt 36
        print(y)           # gibt 36 aus

    "y = y * 2" ist in Mathe Unsinn – beim Programmieren heißt es aber:
    "Nimm den alten Inhalt von y, verdopple ihn, leg ihn zurück in y."

    !! Eine Variable merkt sich einen WERT, keine Rechnung.
        preis = 3
        gesamt = preis * 4     # gesamt ist 12
        preis = 10             # gesamt bleibt trotzdem 12!
    ---
    ## Abkürzungen

    Weil man so oft "x = x + etwas" schreibt, gibt es Kurzformen:
        punkte += 10      # dasselbe wie: punkte = punkte + 10
        leben -= 1        # dasselbe wie: leben = leben - 1
        geld *= 2         # dasselbe wie: geld = geld * 2
        anteil /= 4       # dasselbe wie: anteil = anteil / 4
        kartons //= 6     # dasselbe wie: kartons = kartons // 6

    Alltag: Wie ein Punktestand im Spiel – bei jedem Treffer: punkte += 10
    ---
    ## Namensregeln (in Python)

      • Groß-/Kleinschreibung zählt (case-sensitive):
        meinAlter und meinalter sind ZWEI VERSCHIEDENE Variablen!
      • Der Name muss mit einem Buchstaben oder Unterstrich _ beginnen,
        NIE mit einer Ziffer.  (alter2 ok, 2alter verboten)
      • Erlaubt sind nur Buchstaben, Ziffern und Unterstriche.
        Keine Punkte, Bindestriche, Sterne, &, #, Leerzeichen, ...
      • Wörter, die Python selbst benutzt (if, while, for, True, ...),
        sind als Namen verboten.
      • Namen sollten AUSSAGEKRÄFTIG sein. "a" und "b" sind es meistens nicht.
            anzahl_teilnehmer = 25     # gut
            a = 25                     # schlecht – was ist a?
    ---
    ## snake_case – die Python-Schreibweise

    In Python schreibt man Variablennamen in snake_case:
      • alles klein
      • Wörter mit Unterstrich getrennt  (sieht aus wie eine Schlange _ _ _)

        matrikel_nummer      ✔ snake_case
        anzahl_kekse         ✔ snake_case
        anzahlKekse          ✘ camelCase (benutzt man z.B. in Java)
        AnzahlKekse          ✘ PascalCase

    !! Achtung: Ein Name kann GÜLTIG sein (Python akzeptiert ihn),
    !! aber trotzdem NICHT der Konvention snake_case entsprechen.
    !! Z.B. ist _meinAlter gültig, aber kein snake_case (großes A).
    """)

k.ausgabe("x = 5\ny = x * 3 + 3\ny = y * 2\nprint(y)",
          "x = 5. Dann y = 5 * 3 + 3 = 18. Dann y = 18 * 2 = 36. (Beispiel aus der Vorlesung)")

k.ausgabe("a = 10\na = a + 5\nprint(a)",
          "Rechte Seite zuerst: 10 + 5 = 15, das kommt zurück in a.")

k.ausgabe("punkte = 0\npunkte += 10\npunkte += 5\npunkte -= 3\nprint(punkte)",
          "0 + 10 = 10, + 5 = 15, - 3 = 12.")

k.ausgabe("konto = 100\nkonto *= 2\nkonto //= 3\nprint(konto)",
          "100 * 2 = 200. Dann 200 // 3 = 66 (66 · 3 = 198, Rest 2).")

k.ausgabe("preis = 3\nmenge = 4\ngesamt = preis * menge\npreis = 10\nprint(gesamt)",
          "gesamt wurde EINMAL ausgerechnet (3 * 4 = 12) und gespeichert. Dass "
          "preis später geändert wird, ändert gesamt nicht mehr. Eine Variable "
          "merkt sich den Wert, nicht die Rechnung!",
          tipp="Wird gesamt automatisch neu berechnet, wenn sich preis ändert?")

k.ausgabe("a = 1\nb = 2\na = b\nb = a\nprint(a, b)",
          "Klassischer Anfängerfehler beim 'Tauschen': Nach a = b ist a = 2. "
          "Der alte Wert 1 ist damit weg! Dann b = a → b = 2. Ergebnis: 2 2. "
          "(print mit zwei Werten gibt sie mit Leerzeichen getrennt aus.)",
          tipp="Was steht in a, nachdem 'a = b' ausgeführt wurde?")

k.ausgabe("meinAlter = 21\nmeinalter = meinalter + 1\nprint(meinAlter)",
          "Das ist Übung 1, Aufgabe 5.1: In Zeile 2 steht meinalter (kleines a). "
          "Diese Variable gibt es noch nicht – Python unterscheidet Groß- und "
          "Kleinschreibung! → NameError. Verbesserung: meinAlter = meinAlter + 1",
          tipp="Schau ganz genau auf die Schreibweise der Namen in Zeile 1 und 2.")

k.wf("Python unterscheidet bei Variablennamen zwischen Groß- und Kleinschreibung.", True,
     "Ja, Python ist case-sensitive: alter, Alter und ALTER sind drei verschiedene Variablen.")

k.wf("5y ist ein gültiger Variablenname.", False,
     "Variablennamen dürfen nicht mit einer Ziffer beginnen. (Übung 1)")

for _name, _antwort, _grund in [
    ("matrikel_nummer", "gültig UND snake_case",
     "Nur Kleinbuchstaben und Unterstrich – perfekt."),
    ("ÄhmKeineAhnung", "gültig, aber KEIN snake_case",
     "Python 3 erlaubt Umlaute in Namen – also gültig. Aber Großbuchstaben "
     "und keine Unterstriche → kein snake_case (unüblich sind Umlaute auch)."),
    ("2fancy4python", "UNGÜLTIG",
     "Beginnt mit einer Ziffer → verboten."),
    ("_meinAlter", "gültig, aber KEIN snake_case",
     "Unterstrich am Anfang ist erlaubt, aber das große A passt nicht zu snake_case "
     "(snake_case wäre: _mein_alter)."),
    ("richtig&gut", "UNGÜLTIG",
     "Das Zeichen & ist in Namen nicht erlaubt (es ist ein Operator)."),
    ("_2Euro", "gültig, aber KEIN snake_case",
     "Beginnt mit _ (erlaubt), danach Ziffer ist ok. Aber das große E → kein snake_case."),
    ("Variable2", "gültig, aber KEIN snake_case",
     "Gültig, aber das große V passt nicht zu snake_case (richtig wäre variable2)."),
    ("noch_besser", "gültig UND snake_case",
     "Alles klein, Wörter mit _ getrennt – genau so soll es sein."),
    ("#Falsch", "UNGÜLTIG",
     "Mit # beginnt in Python ein Kommentar – das kann kein Name sein."),
]:
    k.mc(f"Übung 1, Aufgabe 5.2: Was gilt für den Variablennamen   {_name}   ?",
         [_antwort] + [x for x in ("gültig UND snake_case", "gültig, aber KEIN snake_case",
                                   "UNGÜLTIG") if x != _antwort],
         _grund,
         tipp="Regeln: Beginn mit Buchstabe oder _, danach nur Buchstaben/Ziffern/_. "
              "snake_case = alles klein mit _.")

k.mc("Welcher Name ist am besten für 'Anzahl der Teilnehmer'?",
     ["anzahl_teilnehmer", "AnzahlTeilnehmer", "a", "anzahl-teilnehmer"],
     "anzahl_teilnehmer ist aussagekräftig und in snake_case. 'anzahl-teilnehmer' "
     "wäre sogar ungültig (Bindestrich = Minus!).")

k.text("Wie heißt die Schreibweise für Variablennamen, die man in Python verwendet?",
       ["snake_case", "snakecase", "snake case", "snake-case"],
       "snake_case: alles klein, Wörter mit Unterstrich getrennt.",
       tipp="Ein Tier, das lang und dünn ist ...")

k.mc("Was passiert bei   x = 2 + 3   zuerst?",
     ["Die rechte Seite 2 + 3 wird ausgerechnet",
      "x wird gelöscht",
      "x wird mit 2 verglichen",
      "Python prüft, ob x gleich 5 ist"],
     "Erst wird die rechte Seite berechnet (5), dann wird das Ergebnis in x gespeichert.")

k.mc("Wofür sind Variablen laut Vorlesung gut?",
     ["Sie geben Speicherplätzen Namen, damit wir Daten speichern und wiederverwenden können",
      "Sie machen das Programm automatisch schneller",
      "Sie verbinden den Computer mit dem Internet",
      "Sie sind nur zur Dekoration da"],
     "Variablen sind Namen für Speicherplätze. Ohne sie wären Programme sehr "
     "unpraktisch und schwer lesbar.")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 5: Zeichenketten (Strings)
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Zeichenketten (Strings) – Text in Python",
    "Anführungszeichen, \\n, len(), upper(), lower(), Index, Verketten mit +",
    "Vorlesung 1, Übung 2")

k.erklaerung("Was ist eine Zeichenkette?", r"""
    ## Eine Kette aus Zeichen

    Eine Zeichenkette (englisch: String, Typ str) ist eine Abfolge von
    Zeichen – Buchstaben, Ziffern, Leerzeichen, Sonderzeichen.
    Stell sie dir vor wie Buchstaben-Perlen auf einer Schnur.

    Man schreibt sie in einfache ODER doppelte Anführungszeichen –
    in Python gibt es dabei KEINEN Unterschied:
        'Hallo'      "Hallo"      "12345"      '!@#$%'

    !! "12345" ist TEXT, keine Zahl. Wie die Hausnummer auf einem Schild:
    !! Man kann sie lesen, aber nicht mit ihr rechnen.

    Praktisch: Enthält dein Text ein Apostroph ', nimm außen "...":
        "Dillgurkensuppe gibt's heut' Mittag!"
    ---
    ## Sonderzeichen: Zeilenumbruch und Tabulator

    Zeilenumbrüche und Einrückungen muss man extra markieren:
        "Zeile 1\nZeile 2"     \n = neue Zeile (n wie "new line")
        "\tEingerückt"         \t = Tabulator (t wie "tab")

    Der Backslash \ sagt: "Das nächste Zeichen ist etwas Besonderes."
    ---
    ## Nützliche Werkzeuge für Strings

        s1 = 'Lorem'
        s2 = "Ipsum"
        s1 == s2         # False – verschiedener Text
        len(s1)          # 5     – Länge (Anzahl Zeichen)
        s1.lower()       # 'lorem' – alles klein
        s1.upper()       # 'LOREM' – alles GROSS
        s1[2]            # 'r'   – das Zeichen an Position 2

    !! Gezählt wird ab 0! Wie bei einem Aufzug, bei dem "0" das
    !! Erdgeschoss ist:  L=0  o=1  r=2  e=3  m=4

    Auch Leerzeichen zählen bei len() mit: len("Hallo Welt") ist 10.
    ---
    ## Strings verketten (Konkatenation)

    Mit + klebt man Strings aneinander:
        'Hello, ' + 'World!'      →  'Hello, World!'
        "Eis" + "bär"             →  'Eisbär'

    !! Wichtig: + funktioniert nur zwischen str und str!
    !! Python wandelt NICHT automatisch um:
        'a' + 'b'       # ok → 'ab'
        '1' + '1'       # ok → '11'  (Text, nicht 2!)
        1 + '1'         # FEHLER: TypeError

    Alltag: Du kannst ein Wort an ein Wort hängen, aber nicht ein Wort an
    eine Zahl. Erst musst du die Zahl "aufschreiben" (umwandeln) – dazu
    mehr im nächsten Kapitel.
    ---
    ## Kurzer Einschub: Funktionen

    Du hast eben len(...), s.lower(), print(...) gesehen. Das sind FUNKTIONEN:
      • eine benannte Folge von Anweisungen, die eine Aufgabe erledigt
      • sie bekommen Parameter (in den Klammern) ...
      • ... und können einen Rückgabewert liefern
    Form:  funktionsname(parameter1, parameter2, ...)

    Funktionen wie .lower() stehen mit einem Punkt hinter einem Wert –
    sie gehören zu diesem Wert ("Methode"). Mehr dazu später!
    """)

k.ausgabe("s1 = 'Lorem'\nprint(len(s1))", "'Lorem' hat 5 Zeichen.")
k.ausgabe("print('Lorem'.lower())", ".lower() macht alles klein: lorem")
k.ausgabe("print('Lorem'.upper())", ".upper() macht alles groß: LOREM")
k.ausgabe("print('Lorem'[2])",
          "Index 2 ist das DRITTE Zeichen, weil ab 0 gezählt wird: L(0) o(1) r(2).",
          tipp="Zähle ab 0!")
k.ausgabe("print('Lorem'[0])", "Index 0 ist das erste Zeichen: L")
k.ausgabe("print(len('Hallo Welt'))",
          "Das Leerzeichen zählt mit: 5 + 1 + 4 = 10.")
k.ausgabe("print(len(''))", "Ein leerer String hat die Länge 0.")
k.ausgabe("print('Lorem' == 'lorem')",
          "Groß- und Kleinschreibung macht einen Unterschied → False.")
k.ausgabe("print('Hello, ' + 'World!')",
          "Konkatenation: Die beiden Strings werden zusammengeklebt.")
k.ausgabe("print('1' + '1')",
          "Zwei Strings werden zusammengeklebt, nicht addiert: '11'.",
          tipp="Achte auf die Anführungszeichen!")
k.ausgabe("print(1 + '1')",
          "Eine Zahl und ein String können nicht mit + verbunden werden → TypeError.")
k.ausgabe('name = "Anna"\nprint("Hallo " + name + "!")',
          "Die drei Strings werden zu 'Hallo Anna!' verkettet.")
k.ausgabe('wort = "Python"\nprint(wort[0] + wort[5])',
          "wort[0] ist 'P', wort[5] ist 'n' (P=0 y=1 t=2 h=3 o=4 n=5). Zusammen: Pn")
k.ausgabe(r'print("Zeile1\nZeile2")',
          r"\n erzeugt einen Zeilenumbruch: Es werden zwei Zeilen ausgegeben.",
          tipp=r"Was bedeutet \n?")

k.mc("Welche Schreibweise erzeugt in Python einen gültigen String?",
     ["Sowohl 'Hallo' als auch \"Hallo\"",
      "Nur \"Hallo\"",
      "Nur 'Hallo'",
      "Nur «Hallo»"],
     "In Python sind einfache und doppelte Anführungszeichen gleichwertig. "
     "(In Java übrigens nicht – dort nur \"...\".)")

k.wf("'12345' ist eine Zahl, mit der man direkt rechnen kann.", False,
     "In Anführungszeichen ist es ein Text (str). Zum Rechnen muss man ihn erst "
     "umwandeln, z.B. mit int('12345').")

k.text("Was schreibst du in einen String, um eine neue Zeile zu beginnen?",
       ["\\n"],
       r"\n steht für 'new line' (neue Zeile).",
       tipp="Backslash plus ein Buchstabe ...")

k.text("Welche Funktion liefert die Länge eines Strings?",
       ["len", "len()"],
       "len() wie 'length' (Länge): len('Lorem') ist 5.")

k.mc("Was heißt 'Konkatenation'?",
     ["Strings mit + aneinanderhängen",
      "Einen String in Großbuchstaben umwandeln",
      "Die Länge eines Strings bestimmen",
      "Einen String löschen"],
     "Konkatenation = Verkettung: 'Hello, ' + 'World!' → 'Hello, World!'")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 6: Typumwandlung
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Typumwandlung – int(), float(), str(), bool()",
    "Werte von einem Typ in einen anderen umwandeln",
    "Vorlesung 1, Übung 1")

k.erklaerung("Typen umwandeln (Konvertierung)", r"""
    ## Warum umwandeln?

    Manchmal hast du einen Wert im "falschen" Typ. Beispiel: Jemand tippt
    sein Alter ein – Python bekommt aber den TEXT "19", nicht die Zahl 19.
    Um damit zu rechnen, musst du den Typ umwandeln.

    Alltag: Wie Geld wechseln. Du hast Euro, brauchst aber Dollar.
    Der Wert bleibt "gleich", nur die Form ändert sich.

      Funktion   wandelt um in ...      Beispiel        Ergebnis
      ────────   ─────────────────────  ──────────────  ────────
      int()      Ganzzahl               int('3')        3
      float()    Fließkommazahl         float('3.0')    3.0
      str()      Zeichenkette           str(3)          '3'
      bool()     Wahrheitswert          bool(5)         True

    !! Der Datentyp int und die Funktion int() sind zwei verschiedene Dinge,
    !! auch wenn sie gleich heißen!
    ---
    ## Die wichtigsten Regeln

    int() von einer Kommazahl SCHNEIDET AB (rundet NICHT):
        int(3.17)    → 3
        int(3.99)    → 3        (nicht 4!)

    int() von einem Text klappt nur, wenn der Text eine Ganzzahl ist:
        int('5')     → 5
        int('a')     → ValueError  (was soll 'a' als Zahl sein?)
        int('3.5')   → ValueError  (Text mit Punkt → erst float(), dann int())

    float() hängt bei Ganzzahlen ".0" an:
        float(5)     → 5.0

    str() macht aus allem Text:
        str(3.1415)  → '3.1415'
    ---
    ## bool() – die Überraschungen

    Bei bool() gilt: "Leer" oder "Null" ist False, ALLES ANDERE ist True.
        bool(0)       → False
        bool(5)       → True
        bool(-2)      → True
        bool('')      → False    (leerer Text)
        bool('Hallo') → True
        bool('false') → True   !!!
        bool('False') → True   !!!

    !! bool('false') ist True, weil der Text nicht leer ist!
    !! bool() liest den Text nicht – es prüft nur: leer oder nicht?
    ---
    ## type() hilft beim Verstehen

        >>> x = 5
        >>> type(x)
        <class 'int'>
        >>> type(str(x))
        <class 'str'>

    Ausdrücke kann man auch verschachteln. Sie werden von INNEN nach
    AUSSEN ausgewertet (wie Zwiebelschalen):
        float(int(str(int("3"))))
          int("3")    → 3
          str(3)      → '3'
          int('3')    → 3
          float(3)    → 3.0
    """)

k.ausgabe("print(int(3.17))",
          "int() schneidet die Nachkommastellen ab: 3. (Übung 1, 4.1)")
k.ausgabe("print(int(3.99))",
          "int() RUNDET NICHT, es schneidet ab. Deshalb 3 und nicht 4!",
          tipp="Runden oder abschneiden?")
k.ausgabe("print(int('a'))",
          "'a' ist keine Zahl → int() kann es nicht umwandeln → ValueError. (Übung 1, 4.1)")
k.ausgabe("print(float(5))", "Aus der Ganzzahl 5 wird die Kommazahl 5.0. (Übung 1, 4.1)")
k.ausgabe("print(int('5') + 1)",
          "int('5') macht aus dem Text die Zahl 5, und 5 + 1 = 6. (Übung 1, 4.1)")
k.ausgabe("print(type(str(3.1415)))",
          "str() macht aus der Zahl den Text '3.1415' → Typ str. (Übung 1, 4.1)",
          akzeptiert=["str"])
k.ausgabe("print(bool(5))",
          "Alles, was nicht 0 ist, wird zu True. (Übung 1, 4.1)")
k.ausgabe("print(bool('false'))",
          "Überraschung! 'false' ist ein NICHT-LEERER Text, also True. bool() "
          "liest den Inhalt nicht. (Übung 1, 4.1)",
          tipp="Ist der Text leer oder nicht?")
k.ausgabe("print(bool(0))", "0 wird zu False.")
k.ausgabe("print(bool(''))", "Ein leerer String wird zu False.")
k.ausgabe("print(int('3.5'))",
          "Der Text '3.5' ist keine GANZZAHL → ValueError. Richtig wäre: int(float('3.5')) → 3.")
k.ausgabe('print(float(int(str(int("3")))))',
          "Von innen nach außen: int('3') → 3, str(3) → '3', int('3') → 3, "
          "float(3) → 3.0. Ein gültiger Ausdruck! (Übung 1, Theoriefrage)")
k.ausgabe('print("2" + 5)',
          "Ein String plus eine Zahl → TypeError. Python wandelt nicht automatisch um. "
          "(Übung 1, Theoriefrage)")
k.ausgabe('print("2" + str(5))',
          "Erst wird 5 zu '5', dann werden die Strings verkettet: '25'.")
k.ausgabe('print(int("2") + 5)',
          "Erst wird '2' zu 2, dann wird gerechnet: 2 + 5 = 7.")

k.wf('float(int(str(int("3")))) ist ein gültiger Python-Ausdruck.', True,
     "Ja: int('3') → 3 → '3' → 3 → 3.0. Jede Umwandlung funktioniert. (Übung 1)")

k.wf('"2" + 5 wird ohne Fehler ausgeführt.', False,
     "str + int geht nicht → TypeError. (Übung 1)")

k.mc("Was macht int(7.9)?",
     ["Es ergibt 7 (Nachkommastellen werden abgeschnitten)",
      "Es ergibt 8 (es wird gerundet)",
      "Es ergibt einen ValueError",
      "Es ergibt 7.9"],
     "int() von einem float schneidet immer ab, es rundet nie.")

k.mc("Welcher dieser Werte ergibt mit bool() den Wert False?",
     ["0", "'False'", "-1", "'0'"],
     "Nur die Zahl 0 ist 'leer'. '0' und 'False' sind nicht-leere TEXTE → True. "
     "-1 ist nicht 0 → True.")

k.ausgabe('eins = int("1")\n'
          'zwei = eins + eins\n'
          'zehn = int("1" + str(0))\n'
          'neun = zehn - eins\n'
          'ergebnis = int(str(zwei) + "1" + str(neun))\n'
          'print(ergebnis)',
          "Übung 1, Aufgabe 4.2 ('Überkomplizierte Eingabe'): Nur mit \"1\", 0, "
          "int() und str() soll 219 entstehen. Trick: Die Ziffern '2', '1' und '9' "
          "einzeln bauen und als TEXT aneinanderkleben: '2' + '1' + '9' = '219', "
          "dann mit int() in eine Zahl umwandeln.",
          tipp="Welche Zahlen stecken in zwei, zehn und neun? Dann als Text zusammenkleben.")

# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 7: Ein- und Ausgabe
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Ein- und Ausgabe – print() und input()",
    "Mit dem Nutzer reden: Ausgeben, f-Strings, Eingaben einlesen",
    "Vorlesung 1, Übung 2")

k.erklaerung("Ausgabe mit print()", r"""
    ## print() – der Lautsprecher deines Programms

    Mit print() zeigt dein Programm etwas in der Konsole an – wie die
    Anzeigetafel am Bahnhof.
        print()                 # gibt eine leere Zeile aus
        print(5)                # 5
        print('Lorem ipsum')    # Lorem ipsum

    Der übergebene Wert wird bei Bedarf automatisch in Text umgewandelt.
    Gibst du mehrere Werte mit Komma an, trennt print sie mit Leerzeichen:
        print("Alter:", 19)     # Alter: 19
    ---
    ## Text und Werte mischen: f-Strings

    Oft willst du Text UND Werte ausgeben. Zwei Wege:

    WEG 1 – alles in Strings umwandeln und mit + verketten (umständlich):
        n = 5
        print('Info: ' + str(n) + ' Dateien heruntergeladen')

    WEG 2 – FORMATIERUNGSSTRINGS (f-Strings) – viel besser:
        print(f'Info: {n} Dateien heruntergeladen')

    So funktioniert ein f-String:
      • Vor das Anführungszeichen kommt ein f
      • In geschweifte Klammern { } schreibst du Variablen oder Rechnungen
      • Python setzt dort den Wert ein

    Alltag: Wie ein Serienbrief: "Liebe/r {name}, du hast {punkte} Punkte!"
    Für jede Person wird automatisch der richtige Name eingesetzt.
        name = "Lea"
        alter = 19
        print(f"{name} ist {alter} Jahre alt.")   # Lea ist 19 Jahre alt.
        print(f"3 + 4 = {3 + 4}")                 # 3 + 4 = 7
    ---
    ## Eingabe mit input()

    input() ist das Gegenstück zu print(): Das Programm hält an und
    WARTET, bis der Nutzer etwas tippt und Enter drückt.
    (Wie eine Bedienung, die fragt "Was darf's sein?" und auf deine
    Antwort wartet.)

        x = input()                          # wartet ohne Text
        n = input('Bitte gib eine Zahl an: ') # zeigt erst den Text an

    !! input() gibt IMMER einen String (str) zurück –
    !! auch wenn nur Ziffern eingetippt wurden!

    Willst du mit der Eingabe rechnen, musst du sie umwandeln:
        alter = int(input('Wie alt bist du? '))
        print(f'Nächstes Jahr bist du {alter + 1}.')

    Ohne int() gäbe alter + 1 einen TypeError (str + int).
    """)

k.ausgabe("n = 5\nprint(f'Info: {n} Dateien heruntergeladen')",
          "Im f-String wird {n} durch den Wert von n ersetzt.")
k.ausgabe('name = "Lea"\nalter = 19\nprint(f"{name} ist {alter} Jahre alt.")',
          "Beide Platzhalter werden ersetzt.")
k.ausgabe('print(f"3 + 4 = {3 + 4}")',
          "Außerhalb der { } ist alles normaler Text ('3 + 4 = '). In den { } wird "
          "gerechnet: 7.")
k.ausgabe('print("3 + 4 = {3 + 4}")',
          "Hier fehlt das f vor dem String! Dann sind die { } ganz normale Zeichen "
          "und es wird nichts eingesetzt.",
          tipp="Schau genau hin: Steht vor dem String ein f?")
k.ausgabe('print("Summe: " + str(10 + 5))',
          "Erst 10 + 5 = 15, dann str(15) = '15', dann verketten: 'Summe: 15'.")
k.ausgabe('print("Alter:", 19)',
          "Mehrere Werte mit Komma → print trennt sie mit einem Leerzeichen.")
k.ausgabe('preis = 2.5\nmenge = 4\nprint(f"Gesamt: {preis * menge} Euro")',
          "In { } darf gerechnet werden: 2.5 * 4 = 10.0 (float mal int ergibt float).")

k.mc("Welchen Datentyp liefert input() zurück?",
     ["Immer str", "int, wenn man eine Zahl eintippt", "Immer int", "bool"],
     "input() liefert IMMER einen String – auch bei der Eingabe '42'.")

k.mc("Der Nutzer tippt 5 ein. Was passiert?",
     ["Ein TypeError, weil x ein String ist",
      "Es wird 6 ausgegeben",
      "Es wird 51 ausgegeben",
      "Es wird 5 ausgegeben"],
     "x ist der String '5'. '5' + 1 (str + int) → TypeError. Lösung: x = int(input('Zahl: '))",
     code="x = input('Zahl: ')\nprint(x + 1)")

k.mc("Wie liest du eine ganze Zahl vom Nutzer ein?",
     ["zahl = int(input('Zahl: '))",
      "zahl = input(int('Zahl: '))",
      "zahl = input('Zahl: ').int",
      "zahl = number(input('Zahl: '))"],
     "Erst input() (liefert str), dann das Ergebnis mit int() umwandeln. Von innen nach außen!")

k.text("Welcher Buchstabe muss vor dem Anführungszeichen eines Formatierungsstrings stehen?",
       ["f"],
       "f wie 'formatiert': f'Hallo {name}'")

k.mc("Welche Klammern benutzt man in f-Strings für die Platzhalter?",
     ["Geschweifte Klammern { }", "Runde Klammern ( )", "Eckige Klammern [ ]", "Spitze Klammern < >"],
     "f'Info: {n} Dateien' – die Variable kommt in geschweifte Klammern.")

k.mc("Was gibt print() ohne Parameter aus?",
     ["Eine leere Zeile", "Einen Fehler", "None", "Das Wort 'print'"],
     "print() ohne Parameter gibt einfach eine leere Zeile aus.")

k.code(r"""
    ## Übung 2, Aufgabe 4.1 – Variablen einlesen

    Schreibe ein Programm, das nacheinander einliest:
      • den Namen (als Text)
      • das Geburtsdatum als DREI ganze Zahlen: Tag, Monat, Jahr

    Danach soll es ausgeben:
        <Name> hat am <tag>.<monat>.<jahr> Geburtstag.

    Beispiel: Anna, 15, 11, 2006  →  Anna hat am 15.11.2006 Geburtstag.

    Benutze einen f-String (nicht +). Die Fragen im input() darfst du
    frei formulieren – mach sie schön verständlich (Bedienerfreundlichkeit)!
    """,
    [P(["Anna", "15", "11", "2006"], ["Anna hat am 15.11.2006 Geburtstag"]),
     P(["Ben", "24", "12", "2005"], ["Ben hat am 24.12.2005 Geburtstag"])],
    """
    name = input("Wie heißt du? ")
    tag = int(input("An welchem Tag bist du geboren? "))
    monat = int(input("In welchem Monat (als Zahl)? "))
    jahr = int(input("In welchem Jahr? "))
    print(f"{name} hat am {tag}.{monat}.{jahr} Geburtstag.")
    """,
    "Bonus-Wissen: Mit {tag:02d} würde ein Tag wie 5 als '05' ausgegeben.",
    tipp="Vier input()-Aufrufe, drei davon mit int(...) drumherum. "
         "Am Ende: print(f\"{name} hat am {tag}.{monat}.{jahr} Geburtstag.\")",
    vorlage='name = input("Wie heißt du? ")\n...')

k.code(r"""
    ## Pizza-Rechner

    Ihr bestellt Pizza und teilt die Rechnung. Schreibe ein Programm, das
      1. den Gesamtpreis einliest (eine Kommazahl, z.B. 25.5)
      2. die Anzahl der Personen einliest (eine ganze Zahl)
      3. ausgibt:   Jeder zahlt <betrag> Euro

    Beispiel: 30 und 4  →  Jeder zahlt 7.5 Euro
    (Runde nicht – gib das Ergebnis einfach so aus, wie Python es berechnet.)
    """,
    [P(["30", "4"], ["Jeder zahlt 7.5 Euro"]),
     P(["25.5", "3"], ["Jeder zahlt 8.5 Euro"])],
    """
    preis = float(input("Gesamtpreis: "))
    personen = int(input("Anzahl Personen: "))
    print(f"Jeder zahlt {preis / personen} Euro")
    """,
    "Der Preis braucht float() (er kann Nachkommastellen haben). "
    "int('25.5') würde einen ValueError erzeugen!",
    tipp="Preis mit float(input(...)), Personen mit int(input(...)), dann teilen mit /.")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 8: Kommentare, Fehler & Fehlersuche
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Kommentare, Fehlermeldungen & Fehlersuche",
    "# Kommentare, Fehlerarten (lexikalisch, syntaktisch, semantisch), Debugging",
    "Vorlesung 1, Vorlesung 2, Übung 2")

k.erklaerung("Kommentare", r"""
    ## Kommentare – Notizzettel im Code

    Bei viel Code wird es schnell unübersichtlich. Mit Kommentaren kannst
    du Erklärungen in den Code schreiben – wie Post-its in einem Buch.
    Python IGNORIERT Kommentare beim Ausführen komplett.

    Ein Kommentar beginnt mit #:
        # "Floor" in die Konsole ausgeben
        print('Floor')
        x = 5   # auch hinter Code möglich

    Mehrzeilige Kommentare gibt es in Python genau genommen nicht.
    Häufig werden dafür mehrzeilige Strings mit ''' (drei Anführungszeichen) "missbraucht" –
    ohne Zuweisung wirft der Interpreter sie einfach weg:
        '''
        "Floor" in die
        Konsole ausgeben
        '''
        print('Floor')
    ---
    ## Gute und schlechte Kommentare

    Kommentare sollen einen MEHRWERT haben und nicht das Offensichtliche
    beschreiben.

    SCHLECHT (das sieht man doch eh):
        x = x + 1   # erhöht x um 1

    GUT (erklärt, WARUM / WAS gemeint ist):
        # Prüfen, ob die Datei mit der JPEG-Kennung beginnt
        if fdata[0:3] == bytes([0xff, 0xd8, 0xff]):

    Kommentiere Stellen, deren Bedeutung (vor allem für andere) nicht
    sofort klar ist.
    """)

k.erklaerung("Fehlermeldungen verstehen", r"""
    ## Keine Panik vor roten Fehlermeldungen!

    Fehler sind beim Programmieren völlig normal – auch für Profis.
    Python nennt dir fast immer die STELLE, an der der Fehler liegt:
        x = 3 * 5)
          File "<python-input-25>", line 1
            x = 3 * 5)
                     ^
        SyntaxError: unmatched ')'

    Das ^ zeigt auf die Stelle, die letzte Zeile nennt den FEHLERTYP.
    ---
    ## Drei Arten von Fehlern – wie bei einer Sprache

    1. LEXIKALISCHER FEHLER – ein "Wort" gibt es nicht / falsch geschrieben
       Alltag: "Ich gehe in den Supermakrt."  (Tippfehler)
           prinnt("Hallo")          → NameError
           eineZahl = 3
           print(einezahl)          → NameError (Groß/klein!)
           x = true                 → NameError (richtig: True)

    2. SYNTAKTISCHER FEHLER – die "Grammatik" ist falsch
       Alltag: "Ich Supermarkt gehe den in."
           x = 2 + 5) * 3           → SyntaxError: unmatched ')'
           if x < 10                → SyntaxError: expected ':'
           4 +* 5                   → SyntaxError

    3. SEMANTISCHER FEHLER – Grammatik ok, aber die LOGIK/der SINN ist falsch
       Alltag: "Ich trinke ein Brot."  (grammatisch korrekt, aber Unsinn)
           2 // 0                   → ZeroDivisionError (Teilen durch 0)
           x = []
           y = x[1]                 → IndexError (Liste ist leer)
       Auch ein FALSCHES ERGEBNIS ohne Absturz ist ein semantischer Fehler.
       Der ist am gemeinsten, denn dann steht NICHTS in der Konsole!
    ---
    ## Einrückungsfehler

    Python reagiert sehr empfindlich auf falsche Einrückung:
        x = 5
          y = 3          ← unerwartet eingerückt!
        z = 2
    → IndentationError: unexpected indent

    Und wenn nach if/while/def die Einrückung FEHLT:
    → IndentationError: expected an indented block

    !! In einer Datei dürfen Tabs und Leerzeichen NICHT gemischt werden.
    !! Konvention: 4 Leerzeichen pro Einrückungsebene.
    ---
    ## Die häufigsten Fehlertypen auf einen Blick

      NameError          Name unbekannt (Tippfehler, Groß/klein, nicht definiert)
      SyntaxError        Grammatik falsch (Klammer, Doppelpunkt, Anführungszeichen)
      IndentationError   Einrückung falsch
      TypeError          falsche Typen kombiniert, z.B. "Alter: " + 18
      ValueError         richtiger Typ, aber unmöglicher Wert, z.B. int('a')
      ZeroDivisionError  Teilen durch 0
      IndexError         Index gibt es nicht, z.B. [][1]
      KeyError           Schlüssel fehlt im Dictionary (kommt später)
      RecursionError     zu tiefe Rekursion (kommt später)
    ---
    ## So gehst du bei der Fehlersuche vor

      1. Konsolenausgabe lesen
      2. Fehlertyp identifizieren
      3. Stelle im Code finden (Zeilennummer!)
      4. Bei Bedarf Werte mit print() und type() ausgeben
      5. Fehler beheben

    Wenn das Programm nicht abstürzt, sondern nur FALSCHE Ergebnisse
    liefert, steht der Fehler meistens nicht in der Konsole. Dann helfen
    print()-Ausgaben an verschiedenen Stellen ("Wo stimmt der Wert noch?").
    """)

k.wf("Python führt Zeilen, die mit # beginnen, ganz normal aus.", False,
     "Mit # beginnt ein Kommentar – Python ignoriert alles dahinter in dieser Zeile.")

k.mc("Welcher Kommentar ist am sinnvollsten?",
     ["# Rabatt gilt nur für Studierende unter 27 (Vorgabe der Mensa)",
      "# x um 1 erhöhen",
      "# print aufrufen",
      "# Das ist eine Zeile Code"],
     "Gute Kommentare erklären Dinge, die man NICHT direkt im Code sieht – z.B. "
     "das Warum.")

k.mc("Wie markiert man in Python einen (einzeiligen) Kommentar?",
     ["Mit # am Anfang", "Mit // am Anfang", "Mit <!-- -->", "Mit % am Anfang"],
     "# leitet in Python einen Kommentar ein. (// ist in Python die Ganzzahl-Division!)")

k.mc("Übung 2, Aufgabe 2.1: Was passiert bei   true   und welche Fehlerart ist das?",
     ["NameError – lexikalischer Fehler",
      "SyntaxError – syntaktischer Fehler",
      "ZeroDivisionError – semantischer Fehler",
      "Kein Fehler"],
     "true (klein) ist ein unbekanntes 'Wort' für Python → NameError. Das ist ein "
     "lexikalischer Fehler (wie ein Tippfehler). Richtig wäre True.")

k.mc("Übung 2, Aufgabe 2.1: Was passiert bei   4 +* 5   und welche Fehlerart ist das?",
     ["SyntaxError – syntaktischer Fehler",
      "NameError – lexikalischer Fehler",
      "ZeroDivisionError – semantischer Fehler",
      "Es ergibt 20"],
     "Zwei Operatoren direkt hintereinander ergeben keinen Sinn in der 'Grammatik' "
     "von Python → SyntaxError, ein syntaktischer Fehler.")

k.mc("Übung 2, Aufgabe 2.1: Was passiert bei   2 // 0   und welche Fehlerart ist das?",
     ["ZeroDivisionError – semantischer Fehler",
      "SyntaxError – syntaktischer Fehler",
      "NameError – lexikalischer Fehler",
      "Es ergibt 0"],
     "Die Grammatik stimmt, aber Teilen durch 0 ist mathematisch unmöglich → "
     "ZeroDivisionError, ein semantischer Fehler (Logikfehler).")

k.ausgabe('''prinnt("Dillgurkensuppe gibt's heut' Mittag!")''',
          "Übung 2, Aufgabe 2.2: Tippfehler! 'prinnt' gibt es nicht → NameError. "
          "Richtig: print(...)")
k.ausgabe('print(Lorem ipsum !)',
          "Übung 2, Aufgabe 2.2: Die Anführungszeichen fehlen. Python versucht, "
          "'Lorem ipsum !' als Code zu verstehen → SyntaxError. Richtig: print('Lorem ipsum !')")
k.ausgabe('print("Alter: " + 18)',
          "Übung 2, Aufgabe 2.2: String + Zahl → TypeError. Richtig: "
          "print('Alter: ' + str(18)) oder print(f'Alter: {18}')")
k.ausgabe('print("Hey guys, did you know that ...?)',
          "Übung 2, Aufgabe 2.2: Das schließende Anführungszeichen fehlt → SyntaxError "
          "(unterminated string literal).")
k.ausgabe("x = 3 * 5)",
          "Eine schließende Klammer ohne öffnende → SyntaxError: unmatched ')'.")
k.ausgabe("x = 5\nif x < 10\n    print('Die Zahl ist klein')",
          "Nach der if-Bedingung fehlt der Doppelpunkt → SyntaxError: expected ':'.")
k.ausgabe("x = 5\n  y = 3\nz = 2",
          "Zeile 2 ist ohne Grund eingerückt → IndentationError: unexpected indent.")
k.ausgabe("eineZahl = 3\nprint(einezahl)",
          "einezahl ≠ eineZahl → NameError. Python schlägt sogar vor: "
          "Did you mean: 'eineZahl'?")
k.ausgabe("x = []\ny = x[1]",
          "Die Liste ist leer, es gibt kein Element an Position 1 → IndexError: "
          "list index out of range. (Semantischer Fehler)")
k.ausgabe("a = 0\ns = []\na /= len(s)",
          "Quiz aus Vorlesung 2: len([]) ist 0, also wird durch 0 geteilt → ZeroDivisionError.",
          tipp="Wie lang ist eine leere Liste?")

k.wf("In einer Python-Datei darf man Tabs und Leerzeichen zur Einrückung beliebig mischen.", False,
     "Nein – das Mischen führt zu Fehlern. Benutze konsequent 4 Leerzeichen. "
     "(Zur Übung-1-Frage: Ja, es macht einen Unterschied, ob man Tabs oder Spaces "
     "verwendet – für Python sind es verschiedene Zeichen.)")

k.mc("Dein Programm stürzt NICHT ab, liefert aber ein falsches Ergebnis. Was hilft am ehesten?",
     ["Werte an verschiedenen Stellen mit print() ausgeben und nachverfolgen",
      "Auf die Fehlermeldung warten",
      "Den Computer neu starten",
      "Alle Variablen umbenennen"],
     "Bei falschen Ergebnissen gibt es keine Fehlermeldung. Mit print() (und type()) "
     "findest du heraus, ab wo die Werte nicht mehr stimmen.")

k.mc("Was ist ein semantischer Fehler?",
     ["Ein Fehler in der Programmlogik (z.B. Teilen durch 0)",
      "Ein Tippfehler in einem Namen",
      "Eine fehlende Klammer",
      "Ein falsch eingerückter Block"],
     "Semantisch = die Bedeutung/Logik ist falsch, obwohl die Grammatik stimmt.")

k.mc("Was zeigt das Zeichen ^ in einer Python-Fehlermeldung an?",
     ["Die Stelle in der Zeile, an der Python den Fehler bemerkt hat",
      "Eine Potenz",
      "Dass der Fehler unwichtig ist",
      "Den Anfang des Programms"],
     "Python markiert mit ^ (und ~) die Stelle des Fehlers in der angezeigten Zeile.")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 9: Logische Operatoren
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Logische Operatoren – and, or, not",
    "Bedingungen kombinieren und umdrehen",
    "Vorlesung 2, Übung 2")

k.erklaerung("and, or, not", r"""
    ## Bedingungen kombinieren

    Wie prüft man, ob x zwischen 3 und 7 liegt? Man braucht ZWEI
    Bedingungen: 3 < x und x < 7. Kombiniert wird mit LOGISCHEN OPERATOREN.
    Sie arbeiten mit Wahrheitswerten (bool).

      Operator  Bedeutung                     Beispiel
      ────────  ────────────────────────────  ──────────────────
      and       BEIDE sind wahr               is_car and is_boat
      or        MINDESTENS EINER ist wahr     is_car or is_boat
      not       dreht den Wert um             not is_car
    ---
    ## Alltagsbeispiele

    and – "Ich gehe joggen, wenn es warm UND trocken ist."
          Nur wenn beides stimmt, gehe ich.

    or  – "Du kommst ins Kino, wenn du 18 bist ODER ein Erwachsener
          dabei ist." Eins von beiden reicht – beides geht auch!
          (Das Python-or ist kein "entweder-oder".)

    not – "Ich gehe raus, wenn es NICHT regnet."

    Beispiel aus der Vorlesung: Ein regnerischer Tag hat Wolken und Regen:
        raining = False
        cloudy = True
        rainyday = raining and cloudy     # False
    ---
    ## Wahrheitstabellen

        A      B      A and B   A or B
        True   True   True      True
        True   False  False     True
        False  True   False     True
        False  False  False     False

        not True  → False
        not False → True
    ---
    ## Reihenfolge (Präzedenz)

    Was passiert zuerst? Von "zuerst" nach "zuletzt":
      1. Rechnen (* / + - ...)
      2. Vergleiche (== != < > <= >=)
      3. not
      4. and
      5. or

    Merkhilfe: and ist wie "mal", or ist wie "plus" → and bindet stärker.
        True or False and False
        = True or (False and False)
        = True or False
        = True

    !! Im Zweifel: Klammern setzen! Das macht den Code auch lesbarer.
    ---
    ## Anfänger-Schönheitsfehler

    Oft sieht man:
        if a == True:
        if a == False:
    Der Vergleich ergibt ja selbst wieder True oder False – genauso gut
    könnte man ((a == True) == True) == True schreiben. Kürzer und besser:
        if a:
        if not a:
    """)

k.ausgabe("print(True and False)", "and braucht BEIDE als True → False.")
k.ausgabe("print(True or False)", "or braucht nur EINEN als True → True.")
k.ausgabe("print(not True)", "not dreht um → False.")
k.ausgabe("print(False or False)", "Keiner ist True → False.")
k.ausgabe("raining = False\ncloudy = True\nrainyday = raining and cloudy\nprint(rainyday)",
          "Es regnet nicht (False). False and irgendwas ist immer False.")
k.ausgabe("x = 10\na = (x == 60)\nb = 5 > 3\nprint(not (a or b))",
          "a = (10 == 60) = False, b = (5 > 3) = True. a or b = True. not True = False. "
          "(Beispiel aus Vorlesung 2)")
k.ausgabe("x = 10\na = (x == 60)\nb = 5 > 3\nprint(b or (x > 50) and a)",
          "and zuerst: (x > 50) and a = False and False = False. Dann b or False = "
          "True or False = True.")
k.ausgabe("print(True or False and False)",
          "and bindet stärker: True or (False and False) = True or False = True.")
k.ausgabe("print(not False and False)",
          "not zuerst: (not False) = True. Dann True and False = False.")

_aufgaben_3 = [
    "b = x > 5 or y < 7 and z != 0",
    "b = x * y != y * x and x + z == 0",
    "b = not (x == y) and z <= 0",
    "b = x >= 11 or x < 9 and not(y == 2) and x + y * z > 0 or a",
    "b = z != z or not a and x - y * z <= 0",
    "b = not a and z < y - x",
]
_erklaerungen_3 = [
    "x > 5 → 6 > 5 → True. y < 7 → False, z != 0 → False, also 'False and False' = False. "
    "Dann: True or False = True.",
    "x * y = 42 und y * x = 42 → 42 != 42 ist False. False and ... ist immer False → False.",
    "x == y → 6 == 7 → False, not False → True. z <= 0 → 0 <= 0 → True. True and True = True.",
    "x >= 11 → False. Dann der and-Teil: x < 9 (True) and not(y == 2) (True) and "
    "x + y*z > 0 (6 + 0 = 6 > 0 → True) → True. False or True or a → True.",
    "z != z → False. not a → True. x - y*z = 6 - 0 = 6, 6 <= 0 → False. "
    "True and False = False. False or False = False.",
    "not a → True. y - x = 1, z < 1 → 0 < 1 → True. True and True = True.",
]
for _i, (_ausdruck, _erkl) in enumerate(zip(_aufgaben_3, _erklaerungen_3), 1):
    k.ausgabe(f"x = 6\ny = 7\nz = 0\na = False\n{_ausdruck}\nprint(b)",
              f"Übung 2, Aufgabe 3.{_i}: {_erkl}",
              tipp="Erst rechnen, dann vergleichen, dann not, dann and, zuletzt or.")

k.mc("Mit welcher Bedingung prüfst du, ob x zwischen 3 und 7 liegt (3 und 7 nicht eingeschlossen)?",
     ["3 < x and x < 7", "3 < x or x < 7", "not 3 < x", "3 > x and x > 7"],
     "Beide Bedingungen müssen gelten → and. (Mit or wäre z.B. auch x = 100 'drin', "
     "weil 3 < 100 gilt.) Python erlaubt übrigens auch die Kurzform 3 < x < 7.")

k.mc("Kino: Einlass ab 18 ODER in Begleitung eines Erwachsenen. Welche Bedingung passt?",
     ["alter >= 18 or begleitet", "alter >= 18 and begleitet",
      "not alter >= 18", "alter > 18 and not begleitet"],
     "Eins von beiden reicht → or. Mit and müssten 18-Jährige trotzdem jemanden mitbringen.")

k.mc("Wie schreibt man   if a == True:   kürzer und besser?",
     ["if a:", "if True:", "if a = True:", "if not a:"],
     "a ist selbst schon True oder False. if a: reicht völlig. "
     "Und statt if a == False: schreibt man if not a:")

k.wf("x or y ist nur dann True, wenn GENAU EINER von beiden True ist.", False,
     "or ist True, wenn MINDESTENS einer True ist – also auch, wenn beide True sind.")

k.mc("Was wird in   a or b and c   zuerst ausgewertet?",
     ["b and c", "a or b", "Alles gleichzeitig", "Von rechts nach links: c zuerst allein"],
     "and bindet stärker als or (wie mal vor plus): a or (b and c).")

k.wf("Logische Operatoren arbeiten auf dem Datentyp bool.", True,
     "Ja – sie kombinieren oder verändern Wahrheitswerte. Das unterscheidet sie von "
     "den mathematischen Operatoren.")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 10: Verzweigungen
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Verzweigungen – if, elif, else, match",
    "Das Programm Entscheidungen treffen lassen",
    "Vorlesung 2, Übung 2")

k.erklaerung("if und else", r"""
    ## Kontrollfluss – welchen Weg nimmt das Programm?

    Bisher lief jedes Programm stur von oben nach unten. Oft sollen
    Anweisungen aber nur unter bestimmten BEDINGUNGEN ausgeführt werden.
    Dafür braucht man Verzweigungen im Kontrollfluss.

    Alltag: Das Navi. "WENN Stau auf der Autobahn, DANN fahre über die
    Landstraße, SONST bleib auf der Autobahn."

    Ausformuliert: "Wenn <Bedingung>, dann führe <X> aus, sonst <Y>."
    ---
    ## Die if-Anweisung

        x = 5
        if x > 3:
            print("x ist größer als 3")
        else:
            print("x ist nicht größer als 3")

    So funktioniert es:
      • Nach if kommt eine Bedingung (ergibt True oder False).
      • Am Ende der Zeile steht ein DOPPELPUNKT :
      • Der Block darunter ist EINGERÜCKT (meist 4 Leerzeichen).
        Die Einrückung gehört zur Syntax – sie zeigt Python, was zum
        Block gehört!
      • Ist die Bedingung True, wird der if-Block ausgeführt.
      • Sonst wird (falls vorhanden) der else-Block ausgeführt.

    Ohne Einrückung:
        if x > 3:
        print("x ist größer als 3")
    → IndentationError: expected an indented block after 'if' statement
    ---
    ## Beispiel: Teilbarkeit

        num = int(input('Gib eine Zahl an: '))
        if num % 3 == 0:
            print('Die eingegebene Zahl ist durch 3 teilbar')
        else:
            print('Die eingegebene Zahl ist nicht durch 3 teilbar')

    Auch Verneinungen sind möglich: if num % 3 != 0: ...
    """)

k.erklaerung("Mehrere Fälle: elif und match", r"""
    ## Viele Fälle – die naheliegende (unschöne) Lösung

    Man kann if-Anweisungen ineinander verschachteln:
        if my_obj == "cube":
            print('the square hole')
        else:
            if my_obj == "circular":
                print('into the circle?')
            else:
                if my_obj == "rectangular":
                    print('please the rectangle')
                else:
                    print('INTO THE SQUARE HOLE')
    Das rutscht immer weiter nach rechts und wird unübersichtlich.
    ---
    ## Die elegantere Lösung: elif

    elif bedeutet "else if" – "sonst, wenn ...":
        if my_obj == "cube":
            print('the square hole')
        elif my_obj == "circular":
            print('into the circle?')
        elif my_obj == "rectangular":
            print('please the rectangle')
        else:
            print('INTO THE SQUARE HOLE')

    !! Die Bedingungen werden von OBEN nach UNTEN geprüft.
    !! Nur der ERSTE zutreffende Zweig wird ausgeführt – danach ist Schluss!

    Deshalb ist die Reihenfolge wichtig. Beispiel Wetter:
        if temp > 25:
            print("Badewetter")
        elif temp > 10:
            print("Jacke")
        else:
            print("Winterjacke")
    ---
    ## Die (teilweise) noch elegantere Lösung: match

    Wenn man EINEN Wert mit vielen festen Möglichkeiten vergleicht
    (x == 1, x == 2, x == 3, ...), gibt es match (ab Python 3.10):
        match my_obj:
            case "cube":
                print('the square hole')
            case "circular":
                print('into the circle?')
            case "rectangular":
                print('please the rectangle')
            case _:
                print('INTO THE SQUARE HOLE')

    Alltag: Wie ein Getränkeautomat: Taste A → Cola, Taste B → Wasser,
    jede andere Taste → "Ungültige Auswahl".

      • Jedes case entspricht einem if/elif-Fall.
      • case _ ist der "Standardfall" (default) – wie else.
      • match kann nicht alle Bedingungen eines if umsetzen (z.B. "and").
      • Ähnlich zu switch in Java (kann aber noch mehr).
    """)

k.ausgabe('x = 5\nif x > 3:\n    print("x ist größer als 3")\nelse:\n    print("x ist nicht größer als 3")',
          "5 > 3 ist True → der if-Block wird ausgeführt, der else-Block nicht.")
k.ausgabe('x = 2\nif x > 3:\n    print("groß")\nelse:\n    print("klein")\nprint("fertig")',
          "2 > 3 ist False → else-Block: 'klein'. Die letzte Zeile ist nicht eingerückt, "
          "gehört also zu keinem Block und wird immer ausgeführt.")
k.ausgabe('temp = 15\nif temp > 25:\n    print("Badewetter")\nelif temp > 10:\n    print("Jacke")\nelse:\n    print("Winterjacke")',
          "15 > 25? Nein. 15 > 10? Ja → 'Jacke'. Danach wird nichts mehr geprüft.")
k.ausgabe('punkte = 95\nif punkte >= 50:\n    print("bestanden")\nelif punkte >= 90:\n    print("super")',
          "Falle! 95 >= 50 ist schon True → 'bestanden'. Der elif-Zweig wird gar nicht "
          "mehr geprüft. Die strengere Bedingung (>= 90) hätte nach OBEN gehört!",
          tipp="Es wird nur der ERSTE zutreffende Zweig ausgeführt.")
k.ausgabe('x = 10\nif x > 5:\n    print("A")\nif x > 8:\n    print("B")',
          "Das sind zwei GETRENNTE if-Anweisungen. Beide werden geprüft und beide sind True → A und B.")
k.ausgabe('x = 10\nif x > 5:\n    print("A")\nelif x > 8:\n    print("B")',
          "Mit elif gehören sie zusammen: Der erste zutreffende Zweig (A) gewinnt, B wird übersprungen.")
k.ausgabe('num = 9\nif num % 3 == 0:\n    print("durch 3 teilbar")\nelse:\n    print("nicht durch 3 teilbar")',
          "9 % 3 = 0 → die Bedingung ist True.")
k.ausgabe('my_obj = "circular"\nmatch my_obj:\n    case "cube":\n        print("the square hole")\n'
          '    case "circular":\n        print("into the circle?")\n    case _:\n        print("INTO THE SQUARE HOLE")',
          "Der Fall 'circular' passt → 'into the circle?'.")
k.ausgabe('my_obj = "triangle"\nmatch my_obj:\n    case "cube":\n        print("the square hole")\n'
          '    case "circular":\n        print("into the circle?")\n    case _:\n        print("INTO THE SQUARE HOLE")',
          "Kein Fall passt → case _ (der Standardfall) wird ausgeführt.")
k.ausgabe('x = 5\nif x > 3:\nprint("x ist größer als 3")',
          "Der Block nach if ist nicht eingerückt → IndentationError.")
k.ausgabe('alter = 16\nbegleitet = True\nif alter >= 18 or begleitet:\n    print("Einlass")\nelse:\n    print("Kein Einlass")',
          "16 >= 18 ist False, aber begleitet ist True. False or True = True → Einlass.")
k.ausgabe('''variable1 = True + True
variable2 = 3
variable3 = True
variable2 = variable2 + variable1
if variable3 > 5:
    variable2 = 0
else:
    variable2 *= variable3
variable4 = "b"
variable5 = "a"
variable5 = variable5 + variable4
variable6 = 18
variable7 = variable6 > variable2 * 2
variable5 = variable5 + "c"
print(variable7)
print(variable2)
print(variable5)''',
          "Übung 2, Aufgabe 1 (fertig ausgefüllt): True verhält sich beim Rechnen wie 1! "
          "variable1 = True + True = 2. variable2 = 3 + 2 = 5. True > 5? Nein → else: "
          "5 * True = 5 * 1 = 5. variable5 = 'a' + 'b' = 'ab'. variable7 = 18 > 10 = True. "
          "Zuletzt 'ab' + 'c' = 'abc'. Ausgabe: True, 5, abc – genau wie gefordert.",
          tipp="Beim Rechnen zählt True als 1 und False als 0.")

k.mc("Was fehlt in dieser Zeile?   if x > 3",
     ["Ein Doppelpunkt am Ende", "Ein Semikolon am Ende", "Klammern um x > 3", "Nichts"],
     "Nach if-, elif-, else-, while-, for- und def-Zeilen kommt in Python immer ein Doppelpunkt.")

k.mc("Was bedeutet   case _:   in einer match-Anweisung?",
     ["Der Standardfall, wenn kein anderer case passt (wie else)",
      "Der Fall, dass der Wert ein Unterstrich ist",
      "Ein Fehler",
      "Der erste Fall"],
     "case _ fängt alles auf, was vorher nicht gepasst hat – wie else.")

k.wf("Bei if/elif/else können mehrere Zweige nacheinander ausgeführt werden.", False,
     "Nein – nur der erste Zweig, dessen Bedingung True ist. Danach wird der Rest übersprungen.")

k.wf("Die Einrückung gehört in Python zur Syntax.", True,
     "Ja! Sie zeigt Python, welche Anweisungen zu einem Block gehören. (In Java nimmt "
     "man dafür geschweifte Klammern.)")

k.mc("Wann ist match besonders praktisch?",
     ["Wenn man einen Wert mit vielen festen Möglichkeiten vergleicht",
      "Wenn man zwei Bedingungen mit and verknüpfen will",
      "Wenn man etwas wiederholen möchte",
      "Wenn man eine Datei öffnen will"],
     "match eignet sich für ähnliche Fälle wie x == 1, x == 2, x == 3. Bedingungen mit "
     "and & Co. kann es nicht direkt abbilden.")

k.code(r"""
    ## Übung 2, Aufgabe 4.2 – Teilbarkeit

    1. Frage den Nutzer nach zwei ganzen Zahlen a und b (mit input()).
    2. Ist eine Zahl ein Vielfaches der anderen, gib aus, welche ein
       Vielfaches von welcher ist – genau in dieser Form:
           15 ist ein Vielfaches von 5
    3. Andernfalls gib aus:
           Kein Vielfaches

    Beispiele:   a=5,  b=15  →  15 ist ein Vielfaches von 5
                 a=15, b=5   →  15 ist ein Vielfaches von 5
                 a=5,  b=17  →  Kein Vielfaches
    (Die Eingabe 0 musst du nicht beachten.)
    """,
    [P(["5", "15"], ["15 ist ein Vielfaches von 5"]),
     P(["15", "5"], ["15 ist ein Vielfaches von 5"]),
     P(["5", "17"], ["Kein Vielfaches"], nicht=["ist ein Vielfaches"]),
     P(["7", "21"], ["21 ist ein Vielfaches von 7"])],
    """
    a = int(input("Erste Zahl: "))
    b = int(input("Zweite Zahl: "))
    if b % a == 0:
        print(f"{b} ist ein Vielfaches von {a}")
    elif a % b == 0:
        print(f"{a} ist ein Vielfaches von {b}")
    else:
        print("Kein Vielfaches")
    """,
    "Überlege dir vorher alle Fälle: b Vielfaches von a, a Vielfaches von b, keins von "
    "beiden. Teilbarkeit prüft man mit %. Sonderfall 0: b % 0 würde einen "
    "ZeroDivisionError auslösen!",
    tipp="b ist ein Vielfaches von a, wenn b % a == 0 gilt.")

k.code(r"""
    ## Übung 2, Aufgabe 4.3 – Vergleiche

    1. Frage den Nutzer nach drei ganzen Zahlen.
    2. Gib aus, wie viele Werte gleich sind – genau so:
           Drei gleiche Werte
           Zwei gleiche Werte
           Alle verschieden

    Beispiele:  1, 1, 1  →  Drei gleiche Werte
                1, 2, 1  →  Zwei gleiche Werte
                1, 2, 3  →  Alle verschieden
    """,
    [P(["1", "1", "1"], ["Drei gleiche Werte"], nicht=["zwei gleiche", "alle verschieden"]),
     P(["1", "2", "1"], ["Zwei gleiche Werte"], nicht=["drei gleiche", "alle verschieden"]),
     P(["2", "2", "1"], ["Zwei gleiche Werte"], nicht=["drei gleiche", "alle verschieden"]),
     P(["4", "7", "7"], ["Zwei gleiche Werte"], nicht=["drei gleiche", "alle verschieden"]),
     P(["1", "2", "3"], ["Alle verschieden"], nicht=["gleiche werte"])],
    """
    a = int(input("Erste Zahl: "))
    b = int(input("Zweite Zahl: "))
    c = int(input("Dritte Zahl: "))
    if a == b and b == c:
        print("Drei gleiche Werte")
    elif a == b or b == c or a == c:
        print("Zwei gleiche Werte")
    else:
        print("Alle verschieden")
    """,
    "Reihenfolge ist wichtig: Erst auf 'alle drei gleich' prüfen! Sonst würde bei "
    "1, 1, 1 schon die Bedingung für 'zwei gleiche' zutreffen.",
    tipp="Erst prüfen, ob a == b and b == c. Dann mit or prüfen, ob irgendein Paar gleich ist.")

k.code(r"""
    ## Eintrittspreise im Zoo

    Lies das Alter einer Person ein (ganze Zahl) und gib den Eintrittspreis aus:
      • unter 6 Jahren:       Eintritt: 0 Euro
      • 6 bis 17 Jahre:       Eintritt: 5 Euro
      • 18 bis 64 Jahre:      Eintritt: 12 Euro
      • ab 65 Jahren:         Eintritt: 8 Euro
    """,
    [P(["3"], ["Eintritt: 0 Euro"]), P(["6"], ["Eintritt: 5 Euro"]),
     P(["17"], ["Eintritt: 5 Euro"]), P(["18"], ["Eintritt: 12 Euro"]),
     P(["64"], ["Eintritt: 12 Euro"]), P(["65"], ["Eintritt: 8 Euro"]),
     P(["90"], ["Eintritt: 8 Euro"])],
    """
    alter = int(input("Wie alt bist du? "))
    if alter < 6:
        print("Eintritt: 0 Euro")
    elif alter < 18:
        print("Eintritt: 5 Euro")
    elif alter < 65:
        print("Eintritt: 12 Euro")
    else:
        print("Eintritt: 8 Euro")
    """,
    "Weil elif nur geprüft wird, wenn die Bedingungen davor False waren, muss man "
    "bei 'elif alter < 18' nicht mehr 'alter >= 6' dazuschreiben.",
    tipp="Prüfe die Altersgrenzen der Reihe nach von klein nach groß mit if/elif/else.")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 11: while-Schleifen
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "while-Schleifen, break & continue",
    "Dinge wiederholen, solange eine Bedingung gilt",
    "Vorlesung 2, Vorlesung 3, Übung 2, Übung 3")

k.erklaerung("Die while-Schleife", r"""
    ## Warum Schleifen?

    Oft soll ein Code-Block MEHRFACH ausgeführt werden. Man könnte ihn
    kopieren und einfügen – aber das ist fehleranfällig und unübersichtlich.
    (Stell dir vor, du müsstest "Zähne putzen" 1000-mal untereinander
    aufschreiben ...)

    SCHLEIFEN führen einen Block mehrfach aus, ohne dass man ihn mehrfach
    schreiben muss. Die Ausführung kann über eine Bedingung gesteuert werden.
    ---
    ## while = "solange"

        while <Bedingung>:
            <Körper>

    Ausformuliert: "SOLANGE <Bedingung> gilt, führe <X> aus."
    Alltag: "SOLANGE der Teller nicht leer ist: einen Bissen essen."

      • Der eingerückte Körper wird immer wieder ausgeführt, solange die
        Bedingung True ist.
      • Vor JEDER Runde wird die Bedingung neu geprüft.
      • Ist sie False, geht es hinter der Schleife weiter.
    ---
    ## Beispiel aus der Vorlesung

        i = 0
        s = 'Lorem'
        while i < len(s):
            print(f'Buchstabe an Stelle {i}: {s[i]}')
            i += 1

    Ausgabe:
        Buchstabe an Stelle 0: L
        Buchstabe an Stelle 1: o
        Buchstabe an Stelle 2: r
        Buchstabe an Stelle 3: e
        Buchstabe an Stelle 4: m

    Danach ist i = 5, und 5 < 5 ist False → Schleife endet.

    !! Die Schleife hört NICHT von selbst auf! Im Körper muss sich etwas
    !! ändern (hier: i += 1), sonst läuft sie unendlich weiter.
    ---
    ## Endlosschleifen

    Vergisst man i += 1, ist die Bedingung immer True → ENDLOSSCHLEIFE.
      • Manchmal ist das gewollt (z.B. bei periodischen Aufgaben wie einer
        Ampelsteuerung, die ewig laufen soll).
      • Meistens ist es ein Fehler.
      • Mit Strg + C brichst du ein Programm im Terminal ab.

    Übrigens: Eine "if-Schleife" gibt es NICHT. if prüft nur EINMAL.
    (In der Sprache C könnte man mit "goto" so etwas basteln – bitte nicht!)
    ---
    ## Kontrollfluss am Beispiel Teig

    Schleifen und Verzweigungen lassen sich kombinieren – wie in einem Rezept:
        while falsche_konsistenz(teig):
            if zu_flüssig(teig):
                add(teig, mehl)
            else:
                add(teig, flüssigkeit)

    "Solange der Teig nicht passt: Ist er zu flüssig, Mehl dazu,
     sonst Flüssigkeit dazu."
    """)

k.erklaerung("break und continue", r"""
    ## Iterationen überspringen oder abbrechen

    Manchmal möchte man nicht für ALLE Durchläufe (Iterationen) den
    Körper ausführen – oder die Schleife sogar früher beenden.

    continue – beendet die AKTUELLE Runde sofort und springt zurück zur
               Bedingung (Schleifenkopf).
               Alltag: In der Playlist "dieses Lied überspringen".

    break    – beendet die GANZE Schleife sofort. Es geht hinter der
               Schleife weiter.
               Alltag: Die Notbremse – "Ich hab genug, ich geh nach Hause."

    !! Beide gelten nur für die INNERSTE Schleife, in der sie stehen!
    ---
    ## continue im Beispiel

        i = 0
        while i < 10:
            if i == 5:
                i += 1        # wichtig! sonst Endlosschleife
                continue
            print(i)
            i += 1
        print('Ende')

    Gibt 0 1 2 3 4 6 7 8 9 Ende aus – die 5 wird übersprungen.
    Achtung: Ohne das i += 1 vor continue bliebe i für immer 5!
    ---
    ## break im Beispiel

        i = 0
        while i < 10:
            if i == 5:
                break
            print(i)
            i += 1
        print('Ende')

    Gibt 0 1 2 3 4 Ende aus – bei 5 wird die Schleife abgebrochen.
    """)

k.ausgabe("i = 0\nwhile i < 3:\n    print(i)\n    i += 1",
          "i = 0, 1, 2 werden ausgegeben. Bei i = 3 ist 3 < 3 False → Ende.")
k.ausgabe("i = 0\ns = 'abc'\nwhile i < len(s):\n    print(s[i])\n    i += 1",
          "len('abc') ist 3. Die Schleife läuft mit i = 0, 1, 2 und gibt a, b, c aus.")
k.ausgabe("i = 0\nwhile i < 10:\n    if i == 5:\n        i += 1\n        continue\n    print(i)\n    i += 1\nprint('Ende')",
          "continue überspringt bei i == 5 den Rest der Runde (also das print). "
          "Alle anderen Zahlen werden ausgegeben. (Vorlesung 2)",
          tipp="Bei welcher Zahl wird print übersprungen?")
k.ausgabe("i = 0\nwhile i < 10:\n    if i == 5:\n        break\n    print(i)\n    i += 1\nprint('Ende')",
          "break beendet die Schleife bei i == 5 komplett. Danach kommt print('Ende'). (Vorlesung 2)")
k.ausgabe("n = 3\nwhile n > 0:\n    print(n)\n    n -= 1\nprint('Start!')",
          "Countdown: 3, 2, 1, dann ist n = 0 und 0 > 0 ist False → 'Start!'.")
k.ausgabe("summe = 0\ni = 1\nwhile i <= 4:\n    summe += i\n    i += 1\nprint(summe)",
          "summe = 1 + 2 + 3 + 4 = 10.")
k.ausgabe("x = 100\nschritte = 0\nwhile x > 1:\n    x = x // 2\n    schritte += 1\nprint(schritte)",
          "100 → 50 → 25 → 12 → 6 → 3 → 1. Das sind 6 Halbierungen.",
          tipp="Schreibe dir die Werte von x Runde für Runde auf.")
k.ausgabe("i = 10\nwhile i < 5:\n    print(i)\n    i += 1\nprint('fertig')",
          "Die Bedingung 10 < 5 ist schon beim ersten Mal False → der Körper wird "
          "GAR NICHT ausgeführt. Nur 'fertig' erscheint.")

k.mc("Was passiert hier?",
     ["Eine Endlosschleife – es wird immer wieder 0 ausgegeben",
      "Es werden 0 1 2 3 4 ausgegeben",
      "Ein SyntaxError",
      "Gar nichts"],
     "i wird nie verändert, also bleibt i < 5 für immer True. Abbrechen mit Strg + C.",
     code="i = 0\nwhile i < 5:\n    print(i)")

k.mc("Was ist der Unterschied zwischen break und continue?",
     ["break beendet die ganze Schleife, continue nur die aktuelle Runde",
      "continue beendet die ganze Schleife, break nur die aktuelle Runde",
      "Beide beenden das ganze Programm",
      "Es gibt keinen Unterschied"],
     "break = Notbremse (Schleife vorbei). continue = 'Lied überspringen' (nächste Runde).")

k.wf("break beendet bei verschachtelten Schleifen alle Schleifen auf einmal.", False,
     "break und continue wirken nur auf die INNERSTE Schleife.")

k.wf("In Python gibt es eine if-Schleife.", False,
     "Eine if-Schleife gibt es nicht. if prüft nur ein einziges Mal. Zum Wiederholen "
     "braucht man while (oder for).")

k.mc("Wie oft wird print('Hallo') ausgeführt?",
     ["3-mal", "2-mal", "4-mal", "Unendlich oft"],
     "i nimmt die Werte 1, 2, 3 an (bei 4 ist 4 <= 3 False). Also 3-mal.",
     code="i = 1\nwhile i <= 3:\n    print('Hallo')\n    i += 1")

k.code(r"""
    ## Countdown

    Lies mit   n = int(input())   eine Zahl ein (bitte input() OHNE Text
    in den Klammern benutzen). Gib dann mit einer while-Schleife die Zahlen
    von n abwärts bis 1 aus – jede in einer eigenen Zeile – und zum Schluss:
        Start!

    Beispiel für n = 3:
        3
        2
        1
        Start!
    """,
    [P(["3"], exakt=["3", "2", "1", "Start!"]),
     P(["5"], exakt=["5", "4", "3", "2", "1", "Start!"]),
     P(["1"], exakt=["1", "Start!"])],
    """
    n = int(input())
    while n > 0:
        print(n)
        n -= 1
    print("Start!")
    """,
    tipp="while n > 0: ... und im Körper n verkleinern (n -= 1).",
    vorlage="n = int(input())\nwhile ...:\n    ...")

k.code(r"""
    ## Übung 3, Aufgabe 1.1 – Summe mit while

    Berechne die Summe der Zahlen 1 bis 20 (einschließlich) mit einer
    while-Schleife und gib das Ergebnis aus.
    """,
    [P(erwartet=["210"])],
    """
    summe = 0
    i = 1
    while i <= 20:
        summe += i
        i += 1
    print(summe)
    """,
    "Das Muster 'Ergebnisvariable vor der Schleife anlegen, in der Schleife "
    "verändern' wirst du ständig brauchen. Für die Summe startet man bei 0.",
    tipp="summe = 0 und i = 1 vor der Schleife. In der Schleife: summe += i und i += 1.")

k.code(r"""
    ## Übung 3, Aufgabe 1.1.1 – Gaußsche Summenformel

    Der kleine Carl Friedrich Gauß sollte in der Schule die Zahlen von 1
    bis 100 addieren – und war in Sekunden fertig. Sein Trick:
        1 + 2 + 3 + ... + n  =  n · (n + 1) / 2

    Berechne damit die Summe von 1 bis 20 (ohne Schleife!) und gib sie aus.
    """,
    [P(erwartet=["210"])],
    """
    n = 20
    print(n * (n + 1) // 2)
    """,
    "Mit / käme 210.0 heraus (float). Mit // bleibt es eine Ganzzahl. Beides ist "
    "hier richtig, weil n · (n + 1) immer gerade ist.",
    tipp="n = 20, dann n * (n + 1) // 2 ausgeben.")

k.code(r"""
    ## Passwort-Abfrage

    Schreibe ein Programm, das so lange nach einem Passwort fragt, bis
    "sesam" eingegeben wird.
      • Bei jedem falschen Passwort soll   Falsch!   ausgegeben werden.
      • Bei richtigem Passwort soll   Willkommen!   ausgegeben werden.
    """,
    [P(["hallo", "1234", "sesam"], ["Falsch", "Willkommen"]),
     P(["sesam"], ["Willkommen"], nicht=["falsch"])],
    """
    passwort = input("Passwort: ")
    while passwort != "sesam":
        print("Falsch!")
        passwort = input("Passwort: ")
    print("Willkommen!")
    """,
    "Die Schleife läuft, SOLANGE das Passwort falsch ist. Wichtig: In der Schleife "
    "muss neu gefragt werden – sonst Endlosschleife!",
    tipp="Einmal vor der Schleife fragen, dann: while passwort != 'sesam': ...")

# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 12: Listen
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Listen – Die Einkaufsliste",
    "Viele Werte in einer Variable: Index, append, pop, sort, in, ...",
    "Vorlesung 2, Übung 2")

k.erklaerung("Listen – viele Werte in einer Variable", r"""
    ## Das Problem

    Bisher hättest du eine Reihe von Werten vielleicht so gespeichert:
        a1 = 3
        a2 = 4
        a3 = 1
        a4 = 2
    Wie geht das kürzer? Und wie kann man mit einer Schleife alle
    Werte durchgehen?  → Mit LISTEN!
    ---
    ## Listen erstellen

    Eine Liste ist wie ein EINKAUFSZETTEL: mehrere Einträge in fester
    Reihenfolge, und man kann jederzeit etwas dazuschreiben oder streichen.

    Man schreibt sie mit ECKIGEN Klammern, die Werte durch Kommas getrennt:
        lst1 = list()          # leere Liste
        lst1 = []              # auch eine leere Liste
        lst1 = [3, 4, 1, 2]    # Liste mit Werten
        lst2 = lst1.copy()     # eine echte Kopie der Liste
        einkauf = ["Milch", "Brot", "Eier"]

    len(lst) liefert die Anzahl der Elemente (die Länge).
    ---
    ## Zugriff über den Index

    Stell dir einen Zug vor: Jeder Waggon hat eine Nummer – und der
    erste Waggon hat die Nummer 0!

        lst = [3, 4, 1, 2]
        Index:  0  1  2  3

        lst[0]    # → 3   (erstes Element)
        lst[2]    # → 1

    Eine Liste speichert Werte an den Indizes 0 bis len(lst) - 1.

    !! Deshalb führt lst[len(lst)] IMMER zu einem Fehler (IndexError):
    !! Bei 4 Elementen ist der letzte Index 3 – den Index 4 gibt es nicht.
    ---
    ## Negative Indizes (Python-Besonderheit)

    Negative Indizes zählen von HINTEN. lst[-1] ist das letzte Element –
    wie "der Letzte in der Warteschlange".
        lst = [3, 4, 1, 2]
        lst[-1]   # → 2   (letztes)
        lst[-3]   # → 4
    Genauer: lst[-i] entspricht lst[len(lst) - i].

    Werte überschreiben funktioniert genauso:
        lst[0] = 7     # → [7, 4, 1, 2]
        lst[1] = 1     # → [7, 1, 1, 2]
        lst[-1] = 5    # → [7, 1, 1, 5]
    ---
    ## Nützliche Funktionen  (lst = [3, 4, 1, 2])

    Ist etwas enthalten?
        4 in lst          # → True
        5 in lst          # → False
    An welcher Position steht ein Wert?
        lst.index(1)      # → 2
        lst.index(0)      # → ValueError: 0 is not in list

    Listen haben keine feste Länge – man kann Einträge hinzufügen/entfernen:
        lst.append(5)     # hinten anhängen   → [3, 4, 1, 2, 5]
        lst.pop()         # letztes entfernen → [3, 4, 1]   (und zurückgeben)
        del lst[1]        # Index 1 löschen   → [3, 1, 2]
        lst.clear()       # alles löschen     → []
    (Jede Zeile hier bezieht sich auf die ursprüngliche Liste [3, 4, 1, 2].)

    Reihenfolge ändern:
        lst.reverse()     # umdrehen  → [2, 1, 4, 3]
        lst.sort()        # sortieren → [1, 2, 3, 4]

    Zusammenfügen (Konkatenation):
        [3, 1, 2] + [5, 6, 1]     # → [3, 1, 2, 5, 6, 1]
    ---
    ## ACHTUNG: Zwei Namen – EINE Liste!

        lst1 = [3, 1, 2]
        lst2 = lst1          # KEINE Kopie!
        lst1.sort()
        print(lst2)          # → [1, 2, 3]   (!!!)

    lst2 = lst1 erstellt keine neue Liste. Es klebt nur ein ZWEITES
    Namensschild auf DIESELBE Liste. Ändert man sie über den einen Namen,
    sieht man die Änderung auch über den anderen.

    Alltag: Ein geteilter Link zu EINEM Online-Dokument. Wenn deine
    Freundin etwas ändert, siehst du es auch.  Mit lst1.copy() bekommst
    du dagegen eine eigene Kopie – wie ein heruntergeladenes Dokument.
    """)

k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst[0])", "Index 0 ist das erste Element: 3.")
k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst[2])", "Index 2 ist das DRITTE Element: 1.")
k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst[-1])", "-1 ist immer das letzte Element: 2.")
k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst[-3])",
          "Von hinten gezählt: -1 → 2, -2 → 1, -3 → 4. (Oder: len(lst) - 3 = 1 → lst[1] = 4)")
k.ausgabe("lst = [3, 4, 1, 2]\nlst[0] = 7\nlst[1] = 1\nlst[-1] = 5\nprint(lst)",
          "[3,4,1,2] → [7,4,1,2] → [7,1,1,2] → [7,1,1,5].")
k.ausgabe("lst = [3, 4, 1, 2]\nprint(4 in lst)\nprint(5 in lst)",
          "4 ist in der Liste (True), 5 nicht (False).")
k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst.index(1))",
          "Der Wert 1 steht an Index 2.",
          tipp="Gefragt ist die POSITION des Werts 1, nicht der Wert an Position 1.")
k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst.index(0))",
          "Den Wert 0 gibt es nicht in der Liste → ValueError.")
k.ausgabe("lst = [3, 4, 1, 2]\nlst.append(5)\nprint(lst)", "append hängt hinten an.")
k.ausgabe("lst = [3, 4, 1, 2]\nlst.pop()\nprint(lst)", "pop() entfernt das letzte Element.")
k.ausgabe("lst = [3, 4, 1, 2]\ndel lst[1]\nprint(lst)", "del lst[1] löscht das Element an Index 1 (die 4).")
k.ausgabe("lst = [3, 4, 1, 2]\nlst.reverse()\nprint(lst)", "reverse() dreht die Reihenfolge um.")
k.ausgabe("lst = [3, 4, 1, 2]\nlst.sort()\nprint(lst)", "sort() sortiert aufsteigend.")
k.ausgabe("lst = [3, 4, 1, 2]\nlst.clear()\nprint(lst)", "clear() leert die Liste komplett.")
k.ausgabe("lst1 = [3, 1, 2]\nlst2 = [5, 6, 1]\nprint(lst1 + lst2)",
          "+ hängt die zweite Liste an die erste an.")
k.ausgabe("lst1 = [3, 1, 2]\nlst2 = lst1\nlst1.sort()\nprint(lst2)",
          "lst2 ist nur ein zweiter Name für DIESELBE Liste. Wird sie sortiert, sieht man "
          "das auch über lst2: [1, 2, 3].",
          tipp="Ist lst2 eine Kopie oder dieselbe Liste?")
k.ausgabe("lst1 = [3, 1, 2]\nlst2 = lst1.copy()\nlst1.sort()\nprint(lst2)",
          "Mit .copy() ist lst2 eine echte, eigene Kopie. Das Sortieren von lst1 ändert "
          "lst2 nicht: [3, 1, 2].")
k.ausgabe('einkauf = ["Milch", "Brot"]\neinkauf.append("Eier")\nprint(len(einkauf))',
          "Nach dem Anhängen stehen 3 Dinge auf der Einkaufsliste.")
k.ausgabe('einkauf = ["Milch", "Brot", "Eier"]\nletzter = einkauf.pop()\nprint(letzter)\nprint(einkauf)',
          "pop() entfernt das letzte Element UND gibt es zurück. Deshalb steht in letzter "
          "der Wert 'Eier'.")
k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst[len(lst)])",
          "Übung 2, Aufgabe 5.2: len(lst) ist 4, der höchste Index ist aber 3. lst[4] gibt "
          "es nicht → IndexError. Das passiert bei JEDER Liste.")
k.ausgabe("gemischt = [1, 'zwei', 3.0, True]\nprint(len(gemischt))",
          "Eine Liste darf Werte unterschiedlicher Typen enthalten. Sie hat 4 Elemente.")

k.mc("Welchen Index hat das ERSTE Element einer Liste?",
     ["0", "1", "-1", "Das kommt auf die Liste an"],
     "In Python (und den meisten Sprachen) beginnt die Zählung bei 0.")

k.mc("Wie kommst du immer an das LETZTE Element einer Liste lst?",
     ["lst[-1]", "lst[len(lst)]", "lst[last]", "lst[0]"],
     "lst[-1] (oder lst[len(lst) - 1]). lst[len(lst)] gibt immer einen IndexError.")

k.mc("Warum führt liste[len(liste)] immer zu einem Fehler?",
     ["Weil der höchste Index len(liste) - 1 ist",
      "Weil len() nur bei Strings funktioniert",
      "Weil man Listen nicht mit Zahlen indizieren darf",
      "Tut es gar nicht"],
     "Die Indizes gehen von 0 bis len(liste) - 1. (Übung 2, Aufgabe 5.2)")

k.mc("Mit welcher Funktion hängst du ein Element hinten an eine Liste an?",
     ["append()", "add()", "push()", "insert_last()"],
     "lst.append(5) hängt die 5 hinten an.")

k.wf("Listen haben in Python eine feste Länge, die man nicht ändern kann.", False,
     "Python-Listen können wachsen (append) und schrumpfen (pop, del, clear).")

k.code(r"""
    ## Übung 2, Aufgabe 5.1 – Definition & Indizes

    Es gibt bereits eine Variable   liste   mit genau 8 Zahlen.
    (Sie wird vom Quiz vorgegeben – lege sie NICHT selbst an!)

    Gib nacheinander aus (jeweils in einer eigenen Zeile):
      1. die Summe der Zahlen an den Indizes 1, 2 und 7
      2. das Produkt jeder zweiten Zahl, beginnend mit der zweiten
         (also Indizes 1, 3, 5 und 7)
      3. die erste Zahl mal 300

    Ohne Schleifen und ohne Slicing!
    Kontrolle: Für liste = [1,1,2,3,5,8,13,21] ist das 24, 504 und 300.
    """,
    [P(vorspann="liste = [1, 1, 2, 3, 5, 8, 13, 21]", erwartet=["24", "504", "300"]),
     P(vorspann="liste = [-1, 1, -1, 1, -1, 1, -1, 1]", erwartet=["1", "-300"]),
     P(vorspann="liste = [2, 3, 4, 5, 6, 7, 8, 9]", erwartet=["16", "945", "600"])],
    """
    print(liste[1] + liste[2] + liste[7])
    print(liste[1] * liste[3] * liste[5] * liste[7])
    print(liste[0] * 300)
    """,
    "Die 'zweite Zahl' hat den Index 1 – wegen der Zählung ab 0!",
    tipp="Die zweite Zahl hat Index 1. Jede zweite ab da: 1, 3, 5, 7.")

k.code(r"""
    ## Übung 2, Aufgabe 5.2 – Alle Elemente ausgeben

    Es gibt bereits eine Variable   liste   (vom Quiz vorgegeben, beliebig lang).
    Gib mit einer while-Schleife alle Elemente der Reihe nach aus –
    jedes in einer eigenen Zeile.

    Nicht erlaubt: print(liste) oder str(liste).
    """,
    [P(vorspann='liste = ["Milch", "Brot", "Eier"]', exakt=["Milch", "Brot", "Eier"]),
     P(vorspann="liste = [3, 1, 4, 1, 5]", exakt=["3", "1", "4", "1", "5"]),
     P(vorspann="liste = []", exakt=[])],
    """
    i = 0
    while i < len(liste):
        print(liste[i])
        i += 1
    """,
    "Die Bedingung i < len(liste) sorgt dafür, dass der letzte Index len(liste) - 1 ist. "
    "Bei einer leeren Liste läuft die Schleife kein einziges Mal – auch das passt.",
    tipp="i = 0 und dann while i < len(liste): ...",
    vorlage="i = 0\nwhile ...:\n    ...")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 13: Slicing & String-Funktionen
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Slicing & mehr über Strings",
    "Teile von Listen und Texten ausschneiden, split(), replace(), Palindrome",
    "Vorlesung 2, Vorlesung 3, Übung 2")

k.erklaerung("Slicing – Scheiben abschneiden", r"""
    ## Slices = Teile einer Liste (oder eines Strings)

    Wie beim Brot: Du schneidest dir nur die Scheiben ab, die du willst.

    Allgemeine Syntax:   lst[start:end:step]

      start  erster Index des Ausschnitts   → wird MITGENOMMEN (inklusiv)
      end    Index NACH dem Ende            → wird NICHT mitgenommen (exklusiv)
      step   Schrittweite und Richtung      → z.B. 2 = jedes zweite,
                                              -1 = rückwärts

    Beispiele:
        lst = [3, 4, 1, 2]
        lst[1:3]      # → [4, 1]   (Index 1 und 2, NICHT 3)
        lst[1:3:2]    # → [4]      (Index 1, dann 1+2=3 ist schon zu weit)

    Merke: "end" ist wie ein Zaun – bis VOR den Zaun wird geschnitten.
    ---
    ## Was gilt, wenn man etwas weglässt?

    Jeder der drei Teile darf leer bleiben. Dann gilt:
      • step leer   → 1
      • start leer  → ganz vom Anfang  (bei negativem step: vom Ende)
      • end leer    → bis ganz zum Ende (bei negativem step: bis zum Anfang)

        lst = [8, 1, 3, -4, 5, 0, 2, 11]
        lst[:]        # ganze Liste           → [8, 1, 3, -4, 5, 0, 2, 11]
        lst[:3]       # die ersten 3          → [8, 1, 3]
        lst[5:]       # ab Index 5            → [0, 2, 11]
        lst[::2]      # jedes zweite          → [8, 3, 5, 2]
        lst[::-1]     # RÜCKWÄRTS             → [11, 2, 0, 5, -4, 3, 1, 8]
        lst[6:2:-1]   # Index 6, 5, 4, 3      → [2, 0, 5, -4]
    ---
    ## Slicing bei Strings

    Strings verhalten sich in vielen Fällen wie Listen, denn sie sind
    effektiv eine Liste einzelner Zeichen:
      • Zugriff:        s[1]       wie lst[1]
      • Verketten:      s1 + s2    wie lst1 + lst2
      • Slices:         s[1:3]     wie lst[1:3]

        "Lorem ipsum!"[:5]     # → 'Lorem'
        "Hallo"[::-1]          # → 'ollaH'

    !! Funktionen wie .pop(), .sort(), .append() gibt es für Strings NICHT.
    !! Strings kann man auch nicht verändern: s[0] = 'X' → TypeError.
    ---
    ## Nützliche String-Funktionen

    .split('trenner') – teilt einen String an einem Trennzeichen in eine
    LISTE von Strings auf. Super für Daten wie CSV-Zeilen!
        "Anna,19,Informatik".split(",")   # → ['Anna', '19', 'Informatik']
        "Hallo schöne Welt".split(" ")    # → ['Hallo', 'schöne', 'Welt']

    .replace(alt, neu) – ersetzt Teile eines Strings (oder löscht sie,
    wenn man '' als neu nimmt):
        'lorem'.replace('ore', 'i')       # → 'lim'
        'H-a-l-l-o'.replace('-', '')      # → 'Hallo'
    ---
    ## Palindrome erkennen

    Ein Palindrom ist ein Wort, das vorwärts und rückwärts gleich ist:
    Otto, Anna, Rentner, Lagerregal.

    Mit Slicing ist das ein Einzeiler:
        wort == wort[::-1]

    Aber Achtung bei Großbuchstaben: "Lagerregal"[::-1] ist "lagerregaL"
    – das ist nicht gleich! Deshalb vorher alles klein machen:
        wort.lower() == wort.lower()[::-1]
    """)

k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst[1:3])",
          "Von Index 1 (inklusive) bis 3 (exklusive): Index 1 und 2 → [4, 1].",
          tipp="Der end-Index wird NICHT mitgenommen.")
k.ausgabe("lst = [3, 4, 1, 2]\nprint(lst[1:3:2])",
          "Start bei 1 (Wert 4), nächster wäre 1 + 2 = 3, aber 3 ist schon das Ende → [4].")
k.ausgabe("s = [1, 3, 6, 8, 1, 2]\nprint(s[3:0:-2])",
          "Quiz aus Vorlesung 3: Start bei Index 3 (Wert 8), rückwärts in 2er-Schritten: "
          "Index 1 (Wert 3). Index -1 wäre schon hinter dem Ende 0 → [8, 3].",
          tipp="Start bei Index 3, Schrittweite -2, Index 0 ist exklusiv.")
k.ausgabe('print("Lorem ipsum!"[:5])', "Die ersten 5 Zeichen (Index 0 bis 4): Lorem")
k.ausgabe('print("Hallo"[::-1])', "Schrittweite -1 dreht den String um.")
k.ausgabe('print("Hallo Welt"[6:])', "Ab Index 6 bis zum Ende: Welt")
k.ausgabe('print("Anna,19,Informatik".split(","))',
          "split(',') teilt am Komma und liefert eine Liste von Strings.")
k.ausgabe('print("Hallo schöne Welt".split(" "))',
          "split(' ') teilt an den Leerzeichen.")
k.ausgabe("print('lorem'.replace('ore', 'i'))",
          "Der Teil 'ore' wird durch 'i' ersetzt: l + i + m = lim. (Vorlesung 2)")
k.ausgabe("print('H-a-l-l-o'.replace('-', ''))",
          "Durch Ersetzen mit einem leeren String werden alle Bindestriche gelöscht.")
k.ausgabe('wort = "Lagerregal"\nprint(wort == wort[::-1])',
          "Rückwärts ist es 'lagerregaL' – das große L steht jetzt am Ende. Groß und klein "
          "sind verschieden → False!",
          tipp="Achte auf den ersten Buchstaben.")
k.ausgabe('wort = "Lagerregal"\nprint(wort.lower() == wort.lower()[::-1])',
          "Erst alles klein machen ('lagerregal'), dann vergleichen → True.")
k.ausgabe('s = "Hallo"\ns[0] = "B"',
          "Strings kann man nicht verändern → TypeError. Stattdessen einen neuen String "
          "bauen: s = 'B' + s[1:]")
k.ausgabe('s = "Hallo"\ns = "B" + s[1:]\nprint(s)',
          "s[1:] ist 'allo'. Zusammen mit 'B' ergibt sich ein NEUER String: Ballo.")

_lst = {"lst": [8, 1, 3, -4, 5, 0, 2, 11]}
k.ausdruck("Übung 2, Aufgabe 5.3.2 (1): Schreibe einen Slicing-Ausdruck für die GESAMTE Liste.",
           [_lst], "lst[:]",
           "lst[:] – Start und Ende weggelassen → alles. (lst[0:8] oder lst[::] gehen auch.)",
           tipp="Lass start, end und step einfach leer.", muss_enthalten=":")
k.ausdruck("Übung 2, Aufgabe 5.3.2 (2): Die gesamte Liste RÜCKWÄRTS.",
           [_lst], "lst[::-1]",
           "Schrittweite -1 läuft rückwärts. Start/Ende leer → automatisch die ganze Liste.",
           tipp="Die Schrittweite (das dritte Feld) bestimmt die Richtung.", muss_enthalten=":")
k.ausdruck("Übung 2, Aufgabe 5.3.2 (3): Jedes zweite Element, beginnend mit dem ZWEITEN Element.",
           [_lst], "lst[1::2]",
           "Das zweite Element hat Index 1. Dann Schrittweite 2 → Indizes 1, 3, 5, 7.",
           tipp="Das zweite Element hat Index 1.", muss_enthalten=":")
k.ausdruck("Übung 2, Aufgabe 5.3.2 (4): Nur das erste Element (als Liste!).",
           [_lst], "lst[:1]",
           "lst[:1] liefert die Liste [8]. (lst[0] wäre nur die Zahl 8, keine Liste!)",
           tipp="Von Anfang bis VOR Index 1.", muss_enthalten=":")
k.ausdruck("Übung 2, Aufgabe 5.3.2 (5): Das erste Element und jedes dritte danach – "
           "aber nur mit Indizes kleiner 7.",
           [_lst], "lst[0:7:3]",
           "Indizes 0, 3, 6 (9 wäre zu groß). end = 7 sorgt dafür, dass nur Indizes < 7 "
           "vorkommen. Ergebnis: [8, -4, 2].",
           tipp="start = 0, end = 7 (exklusiv!), step = 3.", muss_enthalten=":")
k.ausdruck("Übung 2, Aufgabe 5.3.2 (6): Die Elemente an Index 6, 5, 4 und 3 (in dieser Reihenfolge).",
           [_lst], "lst[6:2:-1]",
           "Start bei 6, rückwärts (step = -1), und end = 2, weil end exklusiv ist "
           "(Index 3 soll noch dabei sein).",
           tipp="Rückwärts heißt step = -1. Das Ende ist exklusiv – wo musst du also aufhören?",
           muss_enthalten=":")
k.ausdruck("Übung 2, Aufgabe 5.3.3: Schreibe einen Ausdruck, der True ergibt, wenn wort ein "
           "Palindrom ist (Groß-/Kleinschreibung soll egal sein), sonst False.",
           [{"wort": "Lagerregal"}, {"wort": "Python"}, {"wort": "Otto"}, {"wort": "Reittier"}],
           "wort.lower() == wort.lower()[::-1]",
           "Erst mit .lower() alles klein machen, dann mit [::-1] umdrehen und vergleichen.",
           tipp="Umdrehen geht mit [::-1]. Und denk an .lower()!")
k.ausdruck("Eine Zeile aus einer CSV-Datei liegt in der Variable zeile. Schreibe einen Ausdruck, "
           "der nur den Studiengang (das letzte Feld) liefert.",
           [{"zeile": "Anna,19,Informatik"}, {"zeile": "Ben,21,Maschinenbau"}],
           "zeile.split(',')[-1]",
           "split(',') macht daraus eine Liste, [-1] nimmt das letzte Element. "
           "zeile.split(',')[2] geht auch.",
           tipp="Erst mit split(',') zerlegen, dann das letzte Element nehmen.")

k.mc("Was bedeuten die drei Teile in lst[a:b:c]?",
     ["a = Start (inklusiv), b = Ende (exklusiv), c = Schrittweite",
      "a = Start (exklusiv), b = Ende (inklusiv), c = Anzahl",
      "a = Länge, b = Start, c = Ende",
      "a = Schrittweite, b = Start, c = Ende"],
     "Übung 2, Aufgabe 5.3.1: start ist dabei, end nicht, step ist die Schrittweite.")

k.mc("Welche Werte gelten, wenn man bei lst[::] alles leer lässt (positive Schrittweite)?",
     ["start = 0, end = len(lst), step = 1",
      "start = 1, end = len(lst), step = 0",
      "start = 0, end = -1, step = 1",
      "Es gibt einen SyntaxError"],
     "Leer = ganz vom Anfang (0) bis ganz zum Ende (len(lst)) in Einerschritten.")

k.wf("Strings haben die Funktionen .sort() und .pop() genau wie Listen.", False,
     "Strings sind unveränderlich, solche Funktionen gibt es für sie nicht. Dafür gibt es "
     ".split() und .replace().")

k.code(r"""
    ## Übung 2, Aufgabe 5.3.3 – Palindrom-Erkennung

    Lies ein Wort mit input() ein. Gib dann aus:
        Palindrom          wenn es vorwärts und rückwärts gleich ist
        Kein Palindrom     sonst

    Groß-/Kleinschreibung soll egal sein ("Lagerregal" ist ein Palindrom).
    """,
    [P(["Lagerregal"], ["Palindrom"], nicht=["kein"]),
     P(["Otto"], ["Palindrom"], nicht=["kein"]),
     P(["Python"], ["Kein Palindrom"]),
     P(["Rentner"], ["Palindrom"], nicht=["kein"])],
    """
    wort = input("Wort: ")
    if wort.lower() == wort.lower()[::-1]:
        print("Palindrom")
    else:
        print("Kein Palindrom")
    """,
    tipp="wort.lower() == wort.lower()[::-1] als Bedingung im if.")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 14: Tupel
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Tupel – Die versiegelte Box",
    "Feste, unveränderliche Wertegruppen",
    "Vorlesung 3")

k.erklaerung("Tupel", r"""
    ## Wenn sich nichts ändern soll

    Listen sind praktisch – aber nicht immer braucht man eine
    Datenstruktur, deren Größe sich ändern kann. Für eine FESTE Anzahl
    von Werten gibt es TUPEL.

    Alltag: Ein Tupel ist wie ein gedrucktes Ticket oder ein versiegeltes
    Paket. Was drauf steht, bleibt so.
      • Ein Geburtsdatum:   (15, 11, 2006)
      • GPS-Koordinaten:    (49.877, 8.654)
      • Eine Anmeldung:     ('anna@mail.de', 'Anna', 'Informatik')

    Man schreibt Tupel mit RUNDEN Klammern:
        t1 = (wert1, wert2, ..., wertN)
        geburtstag = (15, 11, 2006)
    ---
    ## Was geht mit Tupeln?

    Zugriff und Slices – genau wie bei Listen:
        geburtstag[0]       # → 15
        geburtstag[1:]      # → (11, 2006)
        len(geburtstag)     # → 3

    Umwandeln:
        list((1, 2, 3))     # → [1, 2, 3]
        tuple([1, 2, 3])    # → (1, 2, 3)

    !! Der wichtige Unterschied: Tupel können NICHT verändert werden.
    !! geburtstag[0] = 16  → TypeError
    Man kann nur die ganze Variable mit einem neuen Tupel überschreiben:
        geburtstag = (16, 11, 2006)    # ok

    Vorteil: Tupel haben eine bessere Performance (sind schneller).
    ---
    ## Auspacken (sehr praktisch!)

    Man kann ein Tupel direkt in mehrere Variablen "auspacken":
        tag, monat, jahr = (15, 11, 2006)
        print(monat)        # → 11

    Das wirst du gleich bei for-Schleifen mit enumerate() und zip()
    wiedersehen.
    """)

k.ausgabe("t = (4, 5, 6)\nprint(t[1])", "Zugriff wie bei Listen: Index 1 → 5.")
k.ausgabe("t = (4, 5, 6)\nprint(t[1:])", "Ein Slice eines Tupels ist wieder ein Tupel: (5, 6).")
k.ausgabe("t = (4, 5, 6)\nt[0] = 1",
          "Tupel sind unveränderlich → TypeError: 'tuple' object does not support item assignment.")
k.ausgabe("t = (4, 5, 6)\nt = (1, 5, 6)\nprint(t)",
          "Die VARIABLE darf ein neues Tupel bekommen (überschreiben). Nur das Tupel "
          "selbst kann man nicht verändern.")
k.ausgabe("t = (4, 5, 6)\nprint(list(t))", "list() macht aus dem Tupel eine Liste: [4, 5, 6].")
k.ausgabe("print(tuple([1, 2]))", "tuple() macht aus der Liste ein Tupel: (1, 2).")
k.ausgabe("punkt = (3, 7)\nx, y = punkt\nprint(y)",
          "Auspacken: x bekommt 3, y bekommt 7.")
k.ausgabe("geburtstag = (15, 11, 2006)\ntag, monat, jahr = geburtstag\nprint(f'{tag}.{monat}.{jahr}')",
          "Das Tupel wird in drei Variablen ausgepackt und dann im f-String benutzt.")

k.mc("Wann nimmt man eher ein Tupel statt einer Liste?",
     ["Wenn es eine feste Anzahl von Werten ist, die sich nicht ändern soll",
      "Wenn man ständig Elemente hinzufügen will",
      "Wenn man die Werte sortieren möchte",
      "Nie, Tupel sind veraltet"],
     "Feste, unveränderliche Daten (z.B. Koordinaten, Datum) → Tupel. "
     "Wachsende/schrumpfende Sammlungen → Liste.")

k.mc("Mit welchen Klammern schreibt man ein Tupel?",
     ["Runde Klammern ( )", "Eckige Klammern [ ]", "Geschweifte Klammern { }", "Gar keine"],
     "Tupel: ( ), Listen: [ ], Dictionaries: { }")

k.wf("Tupel haben eine bessere Performance als Listen.", True,
     "Ja, weil sie unveränderlich sind, kann Python sie effizienter behandeln.")

k.wf("Man kann ein Element eines Tupels mit t[0] = 5 ändern.", False,
     "Tupel können nicht modifiziert werden, nur komplett überschrieben.")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 15: Dictionaries
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Dictionaries – Das Telefonbuch",
    "Werte über Schlüssel finden: d['name'], get(), in, del",
    "Vorlesung 3, Übung 3")

k.erklaerung("Dictionaries (dict)", r"""
    ## Zugriff mit Namen statt Nummern

    Bei einer Liste findest du Werte über ihre Position (0, 1, 2, ...).
    Ein DICTIONARY (Wörterbuch, Typ dict) erlaubt Zugriff über beliebige
    SCHLÜSSEL.

    Alltag: Ein TELEFONBUCH. Du suchst nicht "den 347. Eintrag", sondern
    den Namen "Oma" – und bekommst die Nummer.
       Schlüssel (key)   →   Wert (value)
       "Oma"             →   "06151 123456"
       "Pizza-Service"   →   "06151 999999"

    Erstellen:
        d = dict()          # leeres Dictionary
        d = {}              # auch leer
        d = {
            'a': 5,
            'x': 'lorem'
        }

      • Schlüssel und Wert werden mit : verbunden, Paare mit , getrennt.
      • Schlüssel dürfen unterschiedliche Typen haben.
      • Werte ebenfalls.
    ---
    ## Zugriffe

        d['a']            # → 5
        d['b']            # → FEHLER: KeyError (Schlüssel gibt es nicht)
        d.get('b', 0)     # → 0  (gibt es 'b' nicht, nimm den Standardwert 0)
        d.get('a', 0)     # → 5
        d.get('b')        # → None (ohne Standardwert)

    Hinzufügen oder ändern – einfach zuweisen:
        d['neu'] = 42     # neuer Eintrag
        d['a'] = 6        # vorhandener Wert wird überschrieben

    Prüfen, ob ein Schlüssel existiert:
        'a' in d          # → True

    Entfernen:
        del d['a']
    ---
    ## Typisches Muster: Zählen (wie eine Strichliste)

        woerter = ["Apfel", "Birne", "Apfel"]
        zaehler = {}
        for w in woerter:
            zaehler[w] = zaehler.get(w, 0) + 1
        # zaehler ist jetzt {'Apfel': 2, 'Birne': 1}

    get(w, 0) liefert den bisherigen Zählerstand – oder 0, wenn das Wort
    noch nie vorkam. (Die for-Schleife lernst du im nächsten Kapitel.)
    """)

k.ausgabe("d = {'a': 5, 'x': 'lorem'}\nprint(d['a'])", "Der Wert zum Schlüssel 'a' ist 5.")
k.ausgabe("d = {'a': 5, 'x': 'lorem'}\nprint(d['b'])",
          "Den Schlüssel 'b' gibt es nicht → KeyError.")
k.ausgabe("d = {'a': 5, 'x': 'lorem'}\nprint(d.get('b', 0))",
          "get() mit Standardwert: 'b' fehlt → 0, und es gibt keinen Fehler.")
k.ausgabe("d = {'a': 5, 'x': 'lorem'}\nprint(d.get('a', 0))",
          "'a' existiert → der echte Wert 5 wird geliefert.")
k.ausgabe("d = {'x': 1}\nprint(d.get('y'))",
          "Ohne Standardwert liefert get() bei fehlendem Schlüssel None.")
k.ausgabe("d = {'a': 5, 'x': 'lorem'}\nprint('a' in d)\ndel d['a']\nprint('a' in d)",
          "Erst ist 'a' drin (True), nach del nicht mehr (False).")
k.ausgabe('preise = {"Brot": 2.5, "Milch": 1.2}\npreise["Butter"] = 2\nprint(len(preise))',
          "Durch die Zuweisung kommt 'Butter' neu hinzu → 3 Einträge.")
k.ausgabe('preise = {"Brot": 2.5, "Milch": 1.2}\npreise["Milch"] = 1.5\nprint(preise["Milch"])',
          "Gibt es den Schlüssel schon, wird der Wert überschrieben.")
k.ausgabe('woerter = ["Apfel", "Birne", "Apfel"]\nzaehler = {}\nfor w in woerter:\n'
          '    zaehler[w] = zaehler.get(w, 0) + 1\nprint(zaehler["Apfel"])',
          "Apfel kommt zweimal vor. Beim ersten Mal: get → 0, + 1 = 1. Beim zweiten Mal: 1 + 1 = 2.")
k.ausgabe("d = {1: 'eins', 'zwei': 2, 3.0: [3]}\nprint(d['zwei'])",
          "Schlüssel und Werte dürfen unterschiedliche Typen haben.")

k.mc("Wie kommst du an einen Wert, OHNE dass ein Fehler entsteht, falls der Schlüssel fehlt?",
     ["d.get(schluessel, standardwert) – oder vorher mit 'schluessel in d' prüfen",
      "d[schluessel] – das gibt nie einen Fehler",
      "d.find(schluessel)",
      "d(schluessel)"],
     "Quiz aus Vorlesung 3: get() mit Standardwert, oder erst mit in prüfen.")

k.mc("Mit welchen Klammern erstellt man ein Dictionary mit Inhalt?",
     ["Geschweifte Klammern { }", "Eckige Klammern [ ]", "Runde Klammern ( )", "Spitze Klammern < >"],
     "{'a': 5} – geschweifte Klammern, Schlüssel: Wert.")

k.mc("Welcher Fehler tritt auf, wenn man mit d['xyz'] auf einen fehlenden Schlüssel zugreift?",
     ["KeyError", "IndexError", "NameError", "ValueError"],
     "Key = Schlüssel → KeyError. (IndexError gibt es bei Listen.)")

k.wf("Alle Schlüssel eines Dictionaries müssen denselben Typ haben.", False,
     "Schlüssel dürfen unterschiedliche Typen haben (z.B. 1 und 'zwei').")

k.mc("Wie entfernst du den Eintrag 'a' aus dem Dictionary d?",
     ["del d['a']", "d.remove['a']", "d['a'] = None", "d - 'a'"],
     "del d['a'] löscht den Eintrag. d['a'] = None würde ihn behalten (nur mit Wert None).")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 16: for-Schleifen
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "for-Schleifen, range, enumerate, zip",
    "Bequem über Listen, Strings und Zahlenbereiche laufen",
    "Vorlesung 3, Übung 3")

k.erklaerung("Die for-Schleife", r"""
    ## Warum noch eine Schleife?

    Mit while über eine Liste zu laufen ist umständlich: Man muss selbst
    hochzählen – und VERGISST man das i += 1, gibt es eine Endlosschleife.
        i = 0
        s = 'Lorem'
        while i < len(s):
            print(f'Buchstabe an Stelle {i}: {s[i]}')
            i += 1

    Die for-Schleife nimmt einem das ab:
        for var in <etwas Durchlaufbares>:
            mach_etwas(var)

    Alltag: "FÜR JEDEN Teller im Stapel: abwaschen."
    Man muss nicht mitzählen – es geht automatisch Teller für Teller.
    ---
    ## for-each: jedes Element durchgehen

    Bei Listen oder Strings will man oft etwas mit JEDEM Element machen:
        s = 'Lorem Ipsum'
        for c in s:
            print(c)          # gibt jeden Buchstaben einzeln aus

        einkauf = ["Milch", "Brot", "Eier"]
        for artikel in einkauf:
            print(f"Nicht vergessen: {artikel}")

    Der Name nach for (c, artikel) ist frei wählbar. In jeder Runde
    steckt darin das nächste Element.
    ---
    ## range(): Zahlenbereiche

    Kurzform der while-Zählschleife:
        for i in range(len(s)):
            print(s[i])
    Hier kann man das Hochzählen gar nicht vergessen!

    range(start, end, step) funktioniert im Prinzip wie Slices:
        range(5)          → 0, 1, 2, 3, 4          (end exklusiv!)
        range(2, 6)       → 2, 3, 4, 5
        range(1, 7, 2)    → 1, 3, 5
        range(10, 0, -3)  → 10, 7, 4, 1

    Vergleich mit Slices:
        lst = [9, 1, 8, 6, 7, 2, 1, 8]
        lst[1:7:2]               # → [1, 6, 2]  (Werte an den Indizes 1, 3, 5)
        list(range(1, 7, 2))     # → [1, 3, 5]  (genau diese Indizes)
    ---
    ## enumerate(): Element UND Index

    Manchmal braucht man zum Element auch seinen Index – will aber keine
    range-Schleife schreiben:
        for i, c in enumerate("Hi!"):
            print(i, c)
    Ausgabe:
        0 H
        1 i
        2 !

    Alltag: Startnummern beim Marathon – jeder Läufer bekommt der Reihe
    nach eine Nummer.
    ---
    ## zip(): zwei Listen gleichzeitig

    Für zwei gleich lange Listen gibt es zip() – wie ein Reißverschluss,
    der immer ein Element von links und eins von rechts zusammenfügt:
        namen = ["Ali", "Bea", "Cem"]
        noten = [2, 1, 3]
        for name, note in zip(namen, noten):
            print(name, note)
    Ausgabe:
        Ali 2
        Bea 1
        Cem 3
    ---
    ## Dictionaries durchlaufen

    Auch über Dictionaries kann man laufen – man bekommt die SCHLÜSSEL:
        lager = {"Äpfel": 3, "Birnen": 0}
        for key in lager:
            value = lager[key]
            print(key, value)
    """)

k.erklaerung("Ergebnisse in Schleifen aufbauen", r"""
    ## Das Akkumulator-Muster (Übung 3, Aufgabe 1.3)

    Oft gibt es eine Variable, in der das Ergebnis langsam aufgebaut wird.
    Alltag: Ein Einkaufswagen an der Kasse – die Summe startet bei 0 und
    jeder Artikel kommt dazu.

        liste = [10, 2, 7, 4, 3, 5, 8]
        summe = 0                 # Startwert für Summen: 0
        produkt = 1               # Startwert für Produkte: 1 (!)
        quadrate = []             # Startwert für Listen: leere Liste
        for x in liste:
            summe += x
            produkt *= x
            quadrate.append(x ** 2)
        durchschnitt = summe / len(liste)

    !! Ein Produkt muss bei 1 starten – mit 0 wäre alles 0!
    !! Beim Durchschnitt: Ist die Liste leer, wird durch 0 geteilt
    !! (ZeroDivisionError) – vorher prüfen! Und / liefert immer float.

    Alles geht in EINER Schleife – man muss nicht für jeden Wert eine
    eigene Schleife schreiben.
    ---
    ## Fakultät und Primzahl

    FAKULTÄT: n! = 1 · 2 · 3 · ... · n      z.B. 5! = 120
        ergebnis = 1
        for i in range(1, n + 1):
            ergebnis *= i
    (Achtung: range(1, n + 1), sonst fehlt n selbst. 0! ist 1.)

    PRIMZAHL: Eine Zahl größer als 1, die nur durch 1 und sich selbst
    teilbar ist (2, 3, 5, 7, 11, 13, ...).
    Idee: Probiere alle möglichen Teiler von 2 bis n - 1 durch. Ist einer
    davon ein Teiler (n % t == 0), ist n keine Primzahl.
        ist_prim = n > 1
        for t in range(2, n):
            if n % t == 0:
                ist_prim = False
                break             # ein Teiler reicht – Rest sparen!
    """)

k.ausgabe("for c in 'abc':\n    print(c)", "for-each über einen String: jedes Zeichen einzeln.")
k.ausgabe("print(list(range(5)))", "range(5) liefert 0 bis 4 – die 5 ist exklusiv.")
k.ausgabe("print(list(range(2, 6)))", "Von 2 bis VOR 6: [2, 3, 4, 5].")
k.ausgabe("print(list(range(1, 7, 2)))", "Von 1 bis vor 7 in 2er-Schritten: [1, 3, 5].")
k.ausgabe("for i in range(1, 8, 3):\n    print(i)",
          "Quiz aus Vorlesung 3: 1, dann 1 + 3 = 4, dann 4 + 3 = 7. Die 10 wäre zu groß.",
          tipp="Start 1, Schrittweite 3, Ende 8 (exklusiv).")
k.ausgabe("print(list(range(10, 0, -3)))",
          "Rückwärts in 3er-Schritten: 10, 7, 4, 1. (-2 wäre schon hinter der 0.)")
k.ausgabe("for i, c in enumerate('hi'):\n    print(i, c)",
          "enumerate liefert Paare aus Index und Element: (0, 'h') und (1, 'i').")
k.ausgabe('namen = ["Ali", "Bea"]\nnoten = [2, 1]\nfor n, x in zip(namen, noten):\n    print(n, x)',
          "zip fügt die Listen paarweise zusammen: (Ali, 2) und (Bea, 1).")
k.ausgabe('lager = {"Äpfel": 3, "Birnen": 0, "Kiwis": 5}\nfor k in lager:\n'
          '    if lager[k] == 0:\n        print(k, "nachbestellen")',
          "Die Schleife geht alle Schlüssel durch. Nur bei Birnen ist der Bestand 0.")
k.ausgabe("summe = 0\nfor x in [10, 2, 7, 4, 3, 5, 8]:\n    summe += x\nprint(summe)",
          "10 + 2 + 7 + 4 + 3 + 5 + 8 = 39.")
k.ausgabe("produkt = 0\nfor x in [10, 2, 7]:\n    produkt *= x\nprint(produkt)",
          "Klassischer Fehler: Startwert 0! 0 · irgendwas = 0. Ein Produkt muss bei 1 starten.",
          tipp="Was ist 0 mal irgendwas?")
k.ausgabe("quadrate = []\nfor x in [1, 2, 3]:\n    quadrate.append(x ** 2)\nprint(quadrate)",
          "Für jedes Element wird das Quadrat hinten angehängt.")
k.ausgabe("n = 20\nprint(n * (n + 1) // 2)",
          "Gaußsche Summenformel: 20 · 21 // 2 = 210. (Übung 3, 1.1.1)")
k.ausgabe("ergebnis = 1\nfor i in range(1, 6):\n    ergebnis *= i\nprint(ergebnis)",
          "5! = 1 · 2 · 3 · 4 · 5 = 120.")
k.ausgabe("for i in range(3):\n    for j in range(3):\n        if j == 1:\n            break\n"
          "        print(i, j)",
          "break beendet nur die INNERE Schleife. Die äußere läuft weiter. Bei jedem i wird "
          "nur j = 0 ausgegeben, bei j = 1 bricht die innere Schleife ab.",
          tipp="Welche Schleife beendet break?")
k.ausgabe("for i in range(5):\n    if i % 2 == 0:\n        continue\n    print(i)",
          "continue überspringt die geraden Zahlen. Es bleiben 1 und 3.")
k.ausgabe("s = 'Lorem'\nfor i in range(len(s)):\n    print(s[i])",
          "range(len(s)) ist range(5) → i = 0, 1, 2, 3, 4. So bekommt man jeden Buchstaben.")

k.mc("Was ist der Hauptvorteil von for gegenüber while beim Durchlaufen einer Liste?",
     ["Man kann das Hochzählen des Index nicht vergessen",
      "for ist immer schneller",
      "while kann keine Listen durchlaufen",
      "for braucht keine Einrückung"],
     "Bei for kümmert sich Python ums Weiterzählen – keine vergessenen i += 1 und keine "
     "Endlosschleifen dadurch.")

k.mc("Du brauchst in der Schleife Index UND Element einer Liste. Was ist am elegantesten?",
     ["for i, x in enumerate(liste):",
      "for i, x in zip(liste):",
      "for i in liste.index():",
      "while liste:"],
     "enumerate liefert Paare aus Index und Element.")

k.mc("Welche Zahlen durchläuft   for i in range(3, 10, 3):  ?",
     ["3, 6, 9", "3, 6, 9, 12", "3, 4, 5, 6, 7, 8, 9", "0, 3, 6, 9"],
     "Start 3, dann +3 → 6, +3 → 9. 12 ist nicht mehr kleiner als 10.")

k.mc("Was musst du bei der Berechnung des Durchschnitts beachten? (Übung 3, 1.3)",
     ["Bei einer leeren Liste würde durch 0 geteilt werden",
      "Der Durchschnitt muss immer eine Ganzzahl sein",
      "Man darf nur // benutzen",
      "Der Durchschnitt ist immer das mittlere Element"],
     "summe / len(liste) – bei len(liste) = 0 gibt es einen ZeroDivisionError. Außerdem "
     "ist das Ergebnis mit / immer ein float.")

k.mc("Welchen Startwert braucht eine Variable, in der ein PRODUKT aufgebaut wird?",
     ["1", "0", "None", "Eine leere Liste"],
     "Mit 0 wäre jedes Produkt 0. Die 1 verändert beim Multiplizieren nichts.")

k.code(r"""
    ## Übung 3, Aufgabe 1.1.3 – Summe mit for

    Berechne die Summe der Zahlen 1 bis 20 (einschließlich) – diesmal mit
    einer for-Schleife und range() – und gib sie aus.
    """,
    [P(erwartet=["210"])],
    """
    summe = 0
    for i in range(1, 21):
        summe += i
    print(summe)
    """,
    "range(1, 21) – das Ende ist exklusiv, deshalb 21 und nicht 20!",
    tipp="for i in range(1, 21): summe += i")

k.code(r"""
    ## Übung 3, Aufgabe 1.2 – Fakultät

    Lies eine ganze Zahl n mit input() ein und gib n! aus.
      n! = 1 · 2 · 3 · ... · n          und  0! = 1

    Beispiel: 15! = 1307674368000
    """,
    [P(["15"], ["1307674368000"]), P(["5"], ["120"]), P(["0"], ["1"]), P(["1"], ["1"])],
    """
    n = int(input("n = "))
    ergebnis = 1
    for i in range(1, n + 1):
        ergebnis *= i
    print(ergebnis)
    """,
    "Startwert 1 (Produkt!). range(1, n + 1), damit n selbst dabei ist. Bei n = 0 läuft "
    "die Schleife gar nicht, und es bleibt korrekt bei 1.",
    tipp="ergebnis = 1, dann for i in range(1, n + 1): ergebnis *= i")

k.code(r"""
    ## Übung 3, Aufgabe 1.3 – Listenverarbeitung

    Es gibt bereits eine Variable   liste   (vom Quiz vorgegeben, z.B.
    [10, 2, 7, 4, 3, 5, 8]). Berechne und gib aus – jedes in einer eigenen Zeile:
      1. die Summe aller Elemente
      2. das Produkt aller Elemente
      3. den Durchschnitt (nicht runden!)
      4. eine Liste der Quadrate der Elemente  (z.B. [100, 4, 49, ...])

    Schaffst du es mit nur EINER Schleife?
    """,
    [P(vorspann="liste = [10, 2, 7, 4, 3, 5, 8]",
       erwartet=["39", "67200", "5.571428571428571", "[100, 4, 49, 16, 9, 25, 64]"]),
     P(vorspann="liste = [1, 2, 3]", erwartet=["6", "2.0", "[1, 4, 9]"])],
    """
    summe = 0
    produkt = 1
    quadrate = []
    for x in liste:
        summe += x
        produkt *= x
        quadrate.append(x ** 2)
    print(summe)
    print(produkt)
    print(summe / len(liste))
    print(quadrate)
    """,
    "Ein Durchlauf reicht für alle Werte. Achtung beim Durchschnitt: Bei einer leeren "
    "Liste müsste man vorher prüfen, ob len(liste) > 0 ist.",
    tipp="Drei Startwerte vor der Schleife: summe = 0, produkt = 1, quadrate = [].")

k.code(r"""
    ## Übung 3, Aufgabe 1.4 – Primzahl

    Lies eine ganze Zahl n mit input() ein und prüfe, ob sie eine
    Primzahl ist. Gib genau eine dieser Zeilen aus:
        <n> ist eine Primzahl
        <n> ist keine Primzahl

    Zur Erinnerung: Primzahlen sind größer als 1 und nur durch 1 und sich
    selbst teilbar. 0 und 1 sind KEINE Primzahlen, 2 ist eine.
    """,
    [P(["7"], ["7 ist eine Primzahl"], nicht=["keine primzahl"]),
     P(["2"], ["2 ist eine Primzahl"], nicht=["keine primzahl"]),
     P(["97"], ["97 ist eine Primzahl"], nicht=["keine primzahl"]),
     P(["9"], ["9 ist keine Primzahl"], nicht=["ist eine primzahl"]),
     P(["15"], ["15 ist keine Primzahl"], nicht=["ist eine primzahl"]),
     P(["1"], ["1 ist keine Primzahl"], nicht=["ist eine primzahl"])],
    """
    n = int(input("Zahl: "))
    ist_prim = n > 1
    for teiler in range(2, n):
        if n % teiler == 0:
            ist_prim = False
            break
    if ist_prim:
        print(f"{n} ist eine Primzahl")
    else:
        print(f"{n} ist keine Primzahl")
    """,
    "Mit break hört man beim ersten gefundenen Teiler auf – das spart Zeit. "
    "Profi-Tipp: Es reicht, Teiler bis zur Wurzel von n zu prüfen.",
    tipp="Probiere alle Teiler von 2 bis n-1. Findest du einen mit n % teiler == 0, "
         "ist es keine Primzahl. Denk an n <= 1!")

k.code(r"""
    ## Übung 3, Aufgabe 2.2 (Teil 2) – Studiengänge zählen

    Es gibt bereits eine Liste   studiengaenge   (vom Quiz vorgegeben), z.B.
        ['Informatik', 'Elektrotechnik', 'Informatik', ...]

    Zähle mit einem Dictionary, wie oft jeder Studiengang vorkommt, und
    gib für jeden Studiengang eine Zeile aus:
        Informatik: 2
        Elektrotechnik: 1
        ...
    (Die Reihenfolge der Zeilen ist egal.)
    """,
    [P(vorspann="studiengaenge = ['Informatik', 'Elektrotechnik', 'Informatik', "
                "'Cognitive Science', 'Wirtschaftsinformatik', 'Maschinenbau']",
       erwartet=["Informatik: 2", "Elektrotechnik: 1", "Cognitive Science: 1",
                 "Wirtschaftsinformatik: 1", "Maschinenbau: 1"]),
     P(vorspann="studiengaenge = ['Mathe', 'Physik', 'Mathe', 'Mathe']",
       erwartet=["Mathe: 3", "Physik: 1"])],
    """
    anzahl = {}
    for fach in studiengaenge:
        anzahl[fach] = anzahl.get(fach, 0) + 1
    for fach in anzahl:
        print(f"{fach}: {anzahl[fach]}")
    """,
    "Das Zähl-Muster mit get(schluessel, 0) + 1 ist ein echter Klassiker.",
    tipp="anzahl = {} und dann für jedes fach: anzahl[fach] = anzahl.get(fach, 0) + 1")

# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 17: Pakete importieren
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Pakete importieren – Der Werkzeugkasten",
    "import math, math.sin, math.pi, math.floor, ...",
    "Vorlesung 3, Übung 3")

k.erklaerung("Pakete importieren", r"""
    ## Das Rad nicht neu erfinden

    Viele Funktionen hat schon jemand anderes programmiert. Statt alles
    selbst zu schreiben, bindet man FUNKTIONSBIBLIOTHEKEN (Pakete) ein.

    Alltag: Du baust ein Regal auf. Du schmiedest dir keinen eigenen
    Schraubenzieher – du holst ihn aus dem Werkzeugkasten.

    In Python (und Java) IMPORTIERT man Pakete:
        import <paket-name>
    ---
    ## Beispiel: das math-Paket

    Für mathematische Funktionen gibt es im Python-Standard das Paket math:
        >>> import math
        >>> math.sin(math.pi * 0.5)
        1.0

    Man schreibt immer   paketname.funktion(...)   – der Punkt heißt
    "aus dem Paket math nimm ...".

    Nützliches aus math:
        math.pi             # 3.141592653589793
        math.sqrt(16)       # 4.0     (Wurzel)
        math.floor(3.7)     # 3       (abrunden)
        math.sin(x), math.cos(x), math.tan(x)
        math.asin(x), math.acos(x), math.atan(x)   (Arcus-Funktionen)

    !! Die Winkelfunktionen rechnen im BOGENMASS (Radiant), nicht in Grad!
    !! 90° entsprechen math.pi * 0.5. (Umrechnen: math.radians(90))

    !! Ohne import math kennt Python "math" nicht → NameError.
    ---
    ## floor() vs. int()

    Beide machen aus einer Kommazahl eine Ganzzahl – aber unterschiedlich:
      • math.floor() rundet immer AB (Richtung minus unendlich)
      • int() SCHNEIDET die Nachkommastellen ab (Richtung 0)
    Bei positiven Zahlen ist das gleich. Bei negativen nicht:
        math.floor(-3.5)    # → -4
        int(-3.5)           # → -3
    """)

k.ausgabe("import math\nprint(math.sin(math.pi * 0.5))",
          "pi · 0.5 sind 90° im Bogenmaß, und sin(90°) = 1 → 1.0 (Beispiel aus Vorlesung 3).")
k.ausgabe("import math\nprint(math.sqrt(16))",
          "Die Wurzel aus 16 ist 4. math.sqrt liefert einen float: 4.0.")
k.ausgabe("import math\nprint(math.floor(3.7))", "floor rundet ab: 3.")
k.ausgabe("import math\nprint(math.floor(-3.5))\nprint(int(-3.5))",
          "floor rundet nach UNTEN (Richtung minus unendlich): -4. int schneidet ab: -3.",
          tipp="Was ist bei negativen Zahlen 'abrunden'?")
k.ausgabe("print(math.pi)",
          "Das Paket math wurde nicht importiert → NameError: name 'math' is not defined.")

k.mc("Wie bindest du das Paket math ein?",
     ["import math", "include math", "using math", "#import math"],
     "In Python: import <paket-name>.")

k.wf("math.sin() erwartet den Winkel in Grad.", False,
     "Die Winkelfunktionen von math arbeiten im Bogenmaß. 90° = math.pi / 2.")

k.mc("Warum importiert man Pakete?",
     ["Um fertige Funktionen zu benutzen, statt sie selbst neu zu programmieren",
      "Damit das Programm eine Internetverbindung bekommt",
      "Weil Python ohne import nicht starten kann",
      "Um Variablen zu löschen"],
     "Man möchte Funktionalitäten nicht mehrfach erfinden müssen → Bibliotheken einbinden.")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 18: Dateien
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Dateien lesen & schreiben",
    "open(), Modi r/w/a/x, read(), readlines(), write(), close(), with, CSV",
    "Vorlesung 3, Übung 3")

k.erklaerung("Dateien öffnen", r"""
    ## Warum Dateien?

    Variablen leben nur, solange das Programm läuft. Danach ist alles weg –
    wie eine Tafel, die nach dem Unterricht gewischt wird.

    Mit print() und input() reden wir mit der Konsole. Um Daten DAUERHAFT
    zu speichern oder aus Dateien zu lesen, braucht man DATEIEN – wie ein
    Notizbuch, das man später wieder aufschlagen kann.
    ---
    ## Eine Datei öffnen

        f = open('<pfad>', '<modus>')
        f = open('main.py', 'r')       # Beispiel: main.py zum Lesen öffnen

      • Der Pfad kann relativ ('daten.txt') oder absolut
        ('C:/Users/.../daten.txt') angegeben werden.
      • Achtung: Ein relativer Pfad bezieht sich auf den Ordner, in dem
        dein Programm AUSGEFÜHRT wird!
    ---
    ## Die Modi

      Kürzel  Bedeutung          Alltag
      ──────  ─────────────────  ───────────────────────────────────────
      r       Lesen (Standard)   Buch aufschlagen und lesen
      w       Schreiben          Neues, LEERES Blatt – Altes wird gelöscht!
      a       Anhängen           Tagebuch: neuer Eintrag hinten dran
      x       Datei erstellen    Nur, wenn es die Datei noch NICHT gibt
      +       Lesen + Schreiben

    Zusätzlich:   t = Text (Standard)    b = Binärdaten (z.B. Bilder)
    z.B. 'rb' = Binärdaten lesen

      • Es ist immer nur EIN Modus möglich. Zum Wechseln muss man die
        Datei neu öffnen.
      • Bis auf 'x' prüft keine Operation, ob die Datei schon existiert.
        'w' überschreibt sie im Zweifelsfall!
      • 'x' gibt einen FileExistsError, wenn die Datei schon da ist.
      • 'r' gibt einen FileNotFoundError, wenn die Datei fehlt.
    ---
    ## Lesen

        content = f.read()        # ganze Datei als EIN großer String
        section = f.read(5)       # die nächsten 5 Zeichen
        line = f.readline()       # eine einzelne Zeile
        lines = f.readlines()     # ganze Datei als LISTE von Zeilen

    Die Liste kann man wie gewohnt durchlaufen:
        for line in lines:
            print(line.strip())

    !! Jede Zeile endet mit '\n' (Zeilenumbruch). Mit .strip() entfernt man
    !! Leerzeichen und Zeilenumbrüche am Anfang und Ende.
    ---
    ## Schreiben

        f.write('Lorem ipsum')

      • Zu schreibende Daten (String oder Bytes) übergibt man an f.write().
      • Die Daten werden an der aktuellen Schreibposition angefügt.
      • write() macht KEINEN automatischen Zeilenumbruch – den musst du
        selbst mit '\n' schreiben!
    ---
    ## Schließen – und warum with so toll ist

    Offene Dateien "vermüllen" das System. Und: Schreiboperationen sind
    erst GARANTIERT abgeschlossen, wenn die Datei geschlossen wurde.
    Sonst können Daten verloren gehen! (Wie ein Dokument, das man nicht
    gespeichert hat.)
        f.close()

    Offizielle Empfehlung von Python – die with-Anweisung:
        with open(pfad) as f:
            content = f.read()

        with open(pfad, 'w') as f:
            f.write('Inhaltsloser Inhalt\n')

    f.close() wird nach dem eingerückten Block AUTOMATISCH ausgeführt und
    kann nicht vergessen werden. (Wie eine Kühlschranktür, die von selbst
    zufällt.)

    Tipp für Umlaute: open(pfad, 'w', encoding='utf-8')
    ---
    ## CSV – Tabellen als Textdatei

    CSV = "comma-separated values". Jede Zeile ist ein Datensatz, die Werte
    sind durch Kommas getrennt. Die erste Zeile enthält oft Überschriften:
        Mail,Name,Studiengang
        anna@mail.de,Anna Muster,Informatik
        ben@mail.de,Ben Beispiel,Maschinenbau

    Schreiben:   f.write(mail + ',' + name + ',' + fach + '\n')
    Lesen:       teile = zeile.strip().split(',')

    !! Problem: Was, wenn jemand ein Komma in seinen Namen schreibt –
    !! z.B. "Muster, Anna"? Dann verrutschen die Spalten!
    !! Auch Zeilenumbrüche in der Eingabe machen das Format kaputt.
    """)

k.ausgabe('with open("test.txt", "w") as f:\n    f.write("Hallo\\n")\n    f.write("Welt\\n")\n\n'
          'with open("test.txt") as f:\n    print(f.readlines())',
          r"readlines() liefert eine Liste der Zeilen – jeweils MIT dem '\n' am Ende.",
          tipp=r"Jede Zeile behält ihr \n.")
k.ausgabe('with open("test.txt", "w") as f:\n    f.write("abc")\n    f.write("def")\n\n'
          'with open("test.txt") as f:\n    print(f.read())',
          r"write() fügt keinen Zeilenumbruch ein – die Texte kleben direkt aneinander: abcdef.")
k.ausgabe('with open("test.txt", "w") as f:\n    f.write("Eins")\n\n'
          'with open("test.txt", "w") as f:\n    f.write("Zwei")\n\n'
          'with open("test.txt") as f:\n    print(f.read())',
          "Modus 'w' überschreibt die Datei jedes Mal komplett. 'Eins' ist weg!",
          tipp="Was macht der Modus 'w' mit dem alten Inhalt?")
k.ausgabe('with open("test.txt", "w") as f:\n    f.write("Eins")\n\n'
          'with open("test.txt", "a") as f:\n    f.write("Zwei")\n\n'
          'with open("test.txt") as f:\n    print(f.read())',
          "Modus 'a' hängt hinten an. Der alte Inhalt bleibt erhalten: EinsZwei.")
k.ausgabe('with open("test.txt", "w") as f:\n    f.write("Lorem ipsum")\n\n'
          'with open("test.txt") as f:\n    print(f.read(5))',
          "read(5) liest nur die nächsten 5 Zeichen: Lorem.")
k.ausgabe('with open("test.txt", "w") as f:\n    f.write("Zeile 1\\nZeile 2\\n")\n\n'
          'with open("test.txt") as f:\n    print(f.readline().strip())',
          "readline() liest nur die erste Zeile, strip() entfernt das \\n am Ende.")
k.ausgabe('f = open("gibt_es_nicht.txt", "r")',
          "Zum Lesen muss die Datei existieren → FileNotFoundError.")
k.ausgabe('with open("neu.txt", "w") as f:\n    f.write("x")\n\nf = open("neu.txt", "x")',
          "Modus 'x' (erstellen) verweigert, wenn die Datei schon existiert → FileExistsError.")
k.ausgabe('zeile = "anna@mail.de,Anna Muster,Informatik\\n"\nteile = zeile.strip().split(",")\nprint(teile[1])',
          "strip() entfernt das \\n, split(',') zerlegt in ['anna@mail.de', 'Anna Muster', "
          "'Informatik']. Index 1 ist der Name.")

k.mc("Du willst in deinem Tagebuch-Programm einen NEUEN Eintrag hinten anfügen, ohne die alten zu löschen. Welcher Modus?",
     ["'a'", "'w'", "'r'", "'x'"],
     "'a' wie 'append' (anhängen). 'w' würde alles Bisherige löschen!")

k.mc("Welcher Modus wirft einen Fehler, wenn die Datei bereits existiert?",
     ["'x'", "'w'", "'a'", "'r'"],
     "'x' (exklusiv erstellen) ist der einzige Modus, der prüft, ob die Datei schon da ist.")

k.mc("Warum sollte man   with open(...) as f:   benutzen?",
     ["Die Datei wird nach dem Block automatisch geschlossen",
      "Die Datei wird dadurch schneller gelesen",
      "Ohne with kann man nicht schreiben",
      "with verschlüsselt die Datei"],
     "with ruft f.close() automatisch auf – man kann es nicht vergessen.")

k.mc("Was passiert, wenn man eine Datei nach dem Schreiben NICHT schließt?",
     ["Es kann zu Datenverlust kommen, weil das Schreiben erst beim Schließen garantiert ist",
      "Nichts, das ist völlig egal",
      "Die Datei wird automatisch gelöscht",
      "Python stürzt sofort ab"],
     "Schreiboperationen sind erst garantiert abgeschlossen, wenn die Datei geschlossen wurde.")

k.wf("f.write('Hallo') fügt am Ende automatisch einen Zeilenumbruch ein.", False,
     r"Nein – den Zeilenumbruch musst du selbst schreiben: f.write('Hallo\n').")

k.mc("Was liefert f.readlines()?",
     ["Eine Liste von Strings – eine pro Zeile",
      "Einen einzigen großen String",
      "Nur die erste Zeile",
      "Die Anzahl der Zeilen"],
     "readlines() → Liste der Zeilen. read() → ein großer String. readline() → eine Zeile.")

k.mc("Bei welcher Nutzereingabe gibt es Probleme mit dem CSV-Format? (Übung 3, 2.1)",
     ["Wenn ein Name ein Komma enthält, z.B. 'Muster, Anna'",
      "Wenn ein Name Umlaute enthält",
      "Wenn eine Mail-Adresse ein @ enthält",
      "Wenn ein Name sehr kurz ist"],
     "Das Komma ist das Trennzeichen. Ein Komma IM Wert lässt die Spalten verrutschen. "
     "(Auch Zeilenumbrüche in der Eingabe wären ein Problem.)")

_BESTELLUNGEN = """
bestellungen = [
    ('joern.siegmund@gmail.com', 'Jörn Siegmund', 'Informatik'),
    ('alena_joerg@aol.com', 'Alena Jörg', 'Elektrotechnik'),
    ('gema76@yahoo.com', 'Gerta Volkmar', 'Informatik'),
    ('lia.wendeltreppe@proton.me', 'Lia Wendel', 'Cognitive Science'),
    ('leon.heinrich@gmail.com', 'Leon Heinrich', 'Wirtschaftsinformatik'),
    ('harter-mut1996@gmx.de', 'Christoph Hartmut', 'Maschinenbau')
]
"""

_CSV_PRUEFUNG = """
import os as _os
if not _os.path.exists("anmeldungen.csv"):
    print("PRÜFUNG: Die Datei anmeldungen.csv wurde nicht gefunden!")
else:
    with open("anmeldungen.csv", encoding="utf-8", errors="replace") as _f:
        _ist = [_z.strip() for _z in _f.read().strip().splitlines()]
    _soll = ["Mail,Name,Studiengang"] + [",".join(_t) for _t in bestellungen]
    if _ist == _soll:
        print("PRÜFUNG: Datei korrekt")
    else:
        print("PRÜFUNG: Inhalt stimmt nicht. Erwartet wurde:")
        for _z in _soll:
            print("   ", _z)
        print("PRÜFUNG: Gefunden wurde:")
        for _z in _ist:
            print("   ", _z)
"""

k.code(r"""
    ## Übung 3, Aufgabe 2.1 – Daten als CSV schreiben

    Es gibt bereits eine Liste   bestellungen   (vom Quiz vorgegeben).
    Jeder Eintrag ist ein Tupel (Mail, Name, Studiengang), z.B.
        ('joern.siegmund@gmail.com', 'Jörn Siegmund', 'Informatik')

    Schreibe alle Daten in die Datei   anmeldungen.csv :
      • erste Zeile: die Überschriften   Mail,Name,Studiengang
      • danach jedes Tupel in einer eigenen Zeile, Werte mit Komma getrennt
      • existiert die Datei schon, soll sie überschrieben werden
      • keine Leerzeichen nach den Kommas
    """,
    [P(vorspann=_BESTELLUNGEN, nachspann=_CSV_PRUEFUNG, erwartet=["PRÜFUNG: Datei korrekt"],
       beschreibung="Inhalt von anmeldungen.csv prüfen")],
    r"""
    with open("anmeldungen.csv", "w", encoding="utf-8") as f:
        f.write("Mail,Name,Studiengang\n")
        for mail, name, fach in bestellungen:
            f.write(f"{mail},{name},{fach}\n")
    """,
    "Modus 'w' überschreibt die Datei bzw. beginnt am Dateianfang. Das Tupel wird in der "
    "for-Schleife direkt in drei Variablen ausgepackt. Das \\n am Ende jeder Zeile nicht "
    "vergessen! (Alternative: f.write(','.join(eintrag) + '\\n'))",
    tipp="with open('anmeldungen.csv', 'w') as f: ... und in einer for-Schleife jede Zeile "
         "mit f.write(...) schreiben. Denk an das \\n!")

_CSV_DATEI = """
with open("anmeldungen.csv", "w", encoding="utf-8") as _f:
    _f.write("Mail,Name,Studiengang\\n")
    _f.write("joern.siegmund@gmail.com,Jörn Siegmund,Informatik\\n")
    _f.write("alena_joerg@aol.com,Alena Jörg,Elektrotechnik\\n")
    _f.write("gema76@yahoo.com,Gerta Volkmar,Informatik\\n")
    _f.write("lia.wendeltreppe@proton.me,Lia Wendel,Cognitive Science\\n")
    _f.write("leon.heinrich@gmail.com,Leon Heinrich,Wirtschaftsinformatik\\n")
    _f.write("harter-mut1996@gmx.de,Christoph Hartmut,Maschinenbau\\n")
"""
_CSV_DATEI_2 = """
with open("anmeldungen.csv", "w", encoding="utf-8") as _f:
    _f.write("Mail,Name,Studiengang\\n")
    _f.write("a@b.de,Ada,Mathe\\n")
    _f.write("c@d.de,Carl,Physik\\n")
    _f.write("e@f.de,Emmy,Mathe\\n")
"""

k.code(r"""
    ## Übung 3, Aufgabe 2.2 – Daten lesen

    Die Datei   anmeldungen.csv   existiert bereits (vom Quiz angelegt) und
    sieht so aus:
        Mail,Name,Studiengang
        joern.siegmund@gmail.com,Jörn Siegmund,Informatik
        alena_joerg@aol.com,Alena Jörg,Elektrotechnik
        ...

    Öffne die Datei, lies alle Zeilen als Liste von Strings ein und zähle,
    wie oft jeder Studiengang vorkommt. Gib für jeden Studiengang aus:
        Informatik: 2
    Die Überschriftenzeile darf NICHT mitgezählt werden!
    """,
    [P(vorspann=_CSV_DATEI, erwartet=["Informatik: 2", "Elektrotechnik: 1",
                                       "Cognitive Science: 1", "Wirtschaftsinformatik: 1",
                                       "Maschinenbau: 1"], nicht=["studiengang: 1"]),
     P(vorspann=_CSV_DATEI_2, erwartet=["Mathe: 2", "Physik: 1"], nicht=["studiengang: 1"])],
    """
    with open("anmeldungen.csv", encoding="utf-8") as f:
        zeilen = f.readlines()

    anzahl = {}
    for zeile in zeilen[1:]:
        fach = zeile.strip().split(",")[2]
        anzahl[fach] = anzahl.get(fach, 0) + 1

    for fach in anzahl:
        print(f"{fach}: {anzahl[fach]}")
    """,
    "zeilen[1:] überspringt die Überschrift. strip() entfernt das \\n, split(',') "
    "zerlegt die Zeile, [2] ist die dritte Spalte (Studiengang).",
    tipp="readlines(), dann for zeile in zeilen[1:]: ... zeile.strip().split(',')[2]")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 19: Funktionen
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Funktionen – Eigene Maschinen bauen",
    "def, Parameter, return, lokale & globale Variablen",
    "Vorlesung 3, Vorlesung 4, Übung 3")

k.erklaerung("Warum Funktionen?", r"""
    ## Funktionen kennst du schon!

    print(), input(), int(), len() ... das sind alles Funktionen.
    Jetzt lernst du, EIGENE Funktionen zu schreiben. Aber warum?

    Stell dir vor, du begrüßt Besucher:
        counter = 1

        name = input('Name: ')
        print(f'Hallo {name}, du bist der {counter}. Besucher')
        counter += 1

        name = input('Name: ')
        print(f'Hallo {name}, du bist der {counter}. Besucher')
        counter += 1
    Immer derselbe Code, kopiert. Das geht schöner!
    ---
    ## Funktionen = eigene kleine Maschinen

    Alltag: Eine KAFFEEMASCHINE.
      • Du gibst etwas hinein (Bohnen, Wasser)     → PARAMETER
      • Drinnen passiert etwas, das du nicht siehst → FUNKTIONSKÖRPER
      • Heraus kommt etwas (Kaffee)                 → RÜCKGABEWERT (return)
    Einmal gebaut, kannst du sie so oft benutzen, wie du willst.

    Vorteile von Funktionen:
      • Weniger doppelter Code (Redundanz) → spart Programmierzeit
      • Code wird lesbarer (bei sinnvollen Namen!)
      • Lokale Variablen und Logik werden "abgekapselt"
      • Unnötige Details werden nach außen versteckt
        (du musst nicht wissen, wie die Kaffeemaschine innen funktioniert)
    ---
    ## So definiert man eine Funktion

        def name(parameter1, parameter2):
            anweisungen
            return ergebnis

      • def ("define") leitet die Funktion ein, dann Name, Klammern, :
      • Der Körper ist eingerückt.
      • return gibt einen Wert zurück UND beendet die Funktion sofort.

    Keine Parameter, kein Rückgabewert:
        def fun1():
            print('Keine Parameter')

    Ein Parameter, kein Rückgabewert:
        def fun2(param1):
            print(f'Nur ein Parameter: {param1}')

    Mit Rückgabewert:
        def fun3(param1, param2):
            print(f'Zwei Parameter: {param1} und {param2}')
            return param1 + param2

    !! Die Definition allein tut noch NICHTS. Erst der AUFRUF fun1()
    !! führt den Code aus. (Eine Kaffeemaschine kocht erst, wenn du
    !! auf den Knopf drückst.)
    ---
    ## Funktionen aufrufen

        rückgabewert = funktionsname(parameter)

        def add1(a, b):
            return a + b + 1

        c = add1(5, 3)      # c ist 9

      • Je nach Definition braucht man Parameter oder nicht.
      • Den Rückgabewert MUSS man nicht nutzen, will es aber meistens.
      • Die NAMEN der übergebenen Variablen und der Parameter müssen
        NICHT gleich sein:  c = add1(x, 5)  passt zu  def add1(a, b):
        (Der Kaffeemaschine ist egal, wie deine Bohnentüte heißt.)
    ---
    ## print oder return? (Anfänger-Klassiker!)

      • print() ZEIGT etwas in der Konsole an – für den Menschen.
      • return GIBT einen Wert an den Aufrufer ZURÜCK – fürs Programm.

        def doppelt_print(x):
            print(x * 2)          # zeigt nur an

        def doppelt_return(x):
            return x * 2          # liefert den Wert

        a = doppelt_print(4)      # zeigt 8 an, aber a ist None!
        b = doppelt_return(4)     # zeigt nichts an, aber b ist 8

    !! Eine Funktion ohne return liefert automatisch None.
    """)

k.erklaerung("Lokale und globale Variablen", r"""
    ## Was in der Funktion passiert, bleibt in der Funktion

    Variablen, die IN einer Funktion erstellt werden, sind LOKAL.
    Außerhalb sind sie nicht sichtbar.
    Alltag: Die Notizzettel in der Restaurantküche – die Gäste im
    Speisesaal bekommen sie nie zu sehen. Sie sehen nur das fertige Essen.

        def greet():
            name = input()
            print(f'Hallo, {name}')

        greet()
        print(name)     # → NameError: name 'name' is not defined
    ---
    ## Lokale Variablen "verdecken" globale

    Eine einfache Zuweisung in einer Funktion erzeugt eine NEUE lokale
    Variable – auch wenn es draußen eine gleichnamige gibt:
        counter = 1
        def greet():
            counter = 1        # neue, LOKALE Variable
            counter += 1       # ändert nur die lokale
        greet()
        print(counter)         # → 1  (die globale ist unverändert!)
    ---
    ## global

    Will man die GLOBALE Variable in der Funktion ändern, muss man sie
    mit global ankündigen:
        counter = 1
        def greet():
            global counter
            counter += 1
        greet()
        print(counter)         # → 2

    Das Besucher-Beispiel wird damit schön kurz:
        counter = 1
        def greet():
            global counter
            name = input('Name: ')
            print(f'Hallo {name}, du bist der {counter}. Besucher')
            counter += 1
        greet()
        greet()

    Tipp: Meistens ist es sauberer, Werte als Parameter hinein- und mit
    return herauszugeben, statt global zu benutzen.
    """)

k.ausgabe("def add1(a, b):\n    return a + b + 1\n\nc = add1(5, 3)\nprint(c)",
          "5 + 3 + 1 = 9. Der Rückgabewert landet in c. (Vorlesung 3)")
k.ausgabe("def fun3(param1, param2):\n    print(f'Zwei Parameter: {param1} und {param2}')\n"
          "    return param1 + param2\n\nergebnis = fun3(2, 3)\nprint(ergebnis)",
          "Erst gibt die Funktion selbst eine Zeile aus. Dann wird der Rückgabewert 5 "
          "ausgegeben.")
k.ausgabe("def fun1():\n    print('Keine Parameter')\n\nprint('Start')",
          "Die Funktion wird nur DEFINIERT, aber nie AUFGERUFEN. Daher wird nur 'Start' ausgegeben.",
          tipp="Wird fun1 irgendwo aufgerufen?")
k.ausgabe("def f():\n    print('hi')\n\nx = f()\nprint(x)",
          "f() gibt 'hi' aus, hat aber kein return → liefert None. x ist also None.")
k.ausgabe("def doppelt(zahl):\n    return zahl * 2\n\nx = 7\nprint(doppelt(x))",
          "Der Parameter heißt zahl, die Variable x – das ist egal. 7 * 2 = 14.")
k.ausgabe("def test():\n    return 1\n    print('nie')\n\nprint(test())",
          "return beendet die Funktion sofort. Die Zeile danach wird nie erreicht.")
k.ausgabe("def greet():\n    name = 'Lea'\n\ngreet()\nprint(name)",
          "name ist eine LOKALE Variable der Funktion. Außerhalb gibt es sie nicht → NameError.")
k.ausgabe("counter = 1\ndef greet():\n    counter = 1\n    counter += 1\n\ngreet()\nprint(counter)",
          "In der Funktion wird eine neue LOKALE Variable counter erzeugt. Die globale "
          "bleibt 1. (Vorlesung 3)",
          tipp="Wird hier die globale oder eine lokale Variable verändert?")
k.ausgabe("counter = 1\ndef greet():\n    global counter\n    counter += 1\n\ngreet()\nprint(counter)",
          "Mit global counter wird die GLOBALE Variable verändert → 2. (Vorlesung 3)")
k.ausgabe("counter = 1\ndef greet():\n    global counter\n    counter += 1\n\ngreet()\ngreet()\ngreet()\nprint(counter)",
          "Drei Aufrufe, jedes Mal + 1: 1 → 2 → 3 → 4.")
k.ausgabe('def zaehlen(name, buchstabe):\n    zaehler = 0\n    for zeichen in name:\n'
          '        if zeichen.lower() == buchstabe:\n            zaehler += 1\n    return zaehler\n\n'
          'zahl = zaehlen("Anna", "a")\nprint(f"Du hast {zahl} A\'s im Namen")',
          "Beispiel aus Vorlesung 4: 'A' wird durch .lower() zu 'a' und zählt mit. Also 2.")
k.ausgabe("def quadrat(x):\n    return x * x\n\nprint(quadrat(3) + quadrat(4))",
          "quadrat(3) = 9, quadrat(4) = 16, zusammen 25.")
k.ausgabe("def begruessung(name, gruss='Hallo'):\n    return f'{gruss}, {name}!'\n\n"
          "print(begruessung('Tom'))\nprint(begruessung('Tom', 'Moin'))",
          "Bonus-Wissen: Parameter können Standardwerte haben. Ohne zweiten Wert wird "
          "'Hallo' benutzt, mit zweitem Wert 'Moin'.")

k.mc("Was ist der Unterschied zwischen print und return in einer Funktion?",
     ["print zeigt etwas in der Konsole an, return gibt einen Wert an den Aufrufer zurück",
      "Es gibt keinen Unterschied",
      "return zeigt etwas an, print gibt einen Wert zurück",
      "print beendet die Funktion, return nicht"],
     "print = Anzeige für den Menschen. return = Ergebnis für das Programm "
     "(und Funktion beenden).")

k.mc("Was liefert eine Funktion, die kein return enthält?",
     ["None", "0", "Einen Fehler", "Den letzten berechneten Wert"],
     "Ohne return liefert jede Funktion automatisch None.")

k.wf("Beim Aufruf müssen die Variablen genauso heißen wie die Parameter in der Definition.", False,
     "Nein! c = add1(x, 5) funktioniert mit def add1(a, b). Der Wert von x landet einfach in a.")

k.mc("Mit welchem Schlüsselwort definiert man eine Funktion?",
     ["def", "function", "func", "define"],
     "def name(parameter): ...")

k.mc("Wozu dient das Schlüsselwort global in einer Funktion?",
     ["Um eine globale Variable in der Funktion verändern zu können",
      "Um eine Funktion überall im Internet verfügbar zu machen",
      "Um eine Variable zu löschen",
      "Um eine Funktion schneller zu machen"],
     "Ohne global würde eine Zuweisung eine neue lokale Variable erzeugen.")

k.mc("Welcher Vorteil von Funktionen wird in der Vorlesung NICHT genannt?",
     ["Funktionen machen jedes Programm automatisch fehlerfrei",
      "Sie reduzieren Redundanz",
      "Code wird lesbarer",
      "Unnötige Details werden nach außen versteckt"],
     "Leider macht nichts Programme automatisch fehlerfrei. Die anderen drei sind "
     "echte Vorteile.")

k.code(r"""
    ## Übung 3, Aufgabe 3.1 (1) – Zoll in Zentimeter

    Schreibe eine Funktion   zoll_zu_cm(zoll)   , die eine Länge in Zoll
    in Zentimeter umrechnet und ZURÜCKGIBT (return, nicht print!).
    1 Zoll = 2.54 cm
    """,
    [F("zoll_zu_cm(1)", 2.54), F("zoll_zu_cm(10)"), F("zoll_zu_cm(27)"), F("zoll_zu_cm(0)")],
    """
    def zoll_zu_cm(zoll):
        return zoll * 2.54
    """,
    tipp="Eine Zeile im Körper: return zoll * 2.54",
    vorlage="def zoll_zu_cm(zoll):\n    ...")

k.code(r"""
    ## Teilbar?

    Schreibe eine Funktion   ist_teilbar(a, b)   , die True zurückgibt,
    wenn a durch b teilbar ist, und sonst False.

    Beispiele:  ist_teilbar(10, 5) → True     ist_teilbar(10, 3) → False
    """,
    [F("ist_teilbar(10, 5)", True), F("ist_teilbar(10, 3)", False),
     F("ist_teilbar(21, 7)", True), F("ist_teilbar(7, 21)", False)],
    """
    def ist_teilbar(a, b):
        return a % b == 0
    """,
    "Der Vergleich a % b == 0 ist selbst schon True oder False – man braucht kein if!",
    tipp="Modulo! Und ein Vergleich liefert schon True/False.",
    vorlage="def ist_teilbar(a, b):\n    ...")

k.code(r"""
    ## Buchstaben zählen (Vorlesung 4)

    Schreibe eine Funktion   zaehlen(name, buchstabe)   , die zurückgibt,
    wie oft der (kleine) buchstabe im name vorkommt – egal ob groß oder
    klein geschrieben.

    Beispiele:  zaehlen("Anna", "a") → 2      zaehlen("ANANAS", "a") → 3
    """,
    [F('zaehlen("Anna", "a")', 2), F('zaehlen("ANANAS", "a")', 3),
     F('zaehlen("Bob", "a")', 0), F('zaehlen("", "x")', 0)],
    """
    def zaehlen(name, buchstabe):
        zaehler = 0
        for zeichen in name:
            if zeichen.lower() == buchstabe:
                zaehler += 1
        return zaehler
    """,
    tipp="zaehler = 0, dann for zeichen in name: ... mit zeichen.lower() vergleichen.",
    vorlage="def zaehlen(name, buchstabe):\n    zaehler = 0\n    ...")

k.code(r"""
    ## Übung 3, Aufgabe 3.1 (2) – Größtes Element mit Index

    Schreibe eine Funktion   groesstes_element(liste)   , die das größte
    Element und seinen Index als Tupel (wert, index) ZURÜCKGIBT.
      • Kommt das Maximum mehrfach vor, nimm den ERSTEN Index.
      • Achte auf Sonderfälle: Ist die Liste leer, gib None zurück.

    Beispiel:  groesstes_element([3, 9, 2]) → (9, 1)
    """,
    [F("groesstes_element([3, 9, 2])", (9, 1)),
     F("groesstes_element([5])", (5, 0)),
     F("groesstes_element([-3, -1, -7])", (-1, 1)),
     F("groesstes_element([4, 4, 1])", (4, 0)),
     F("groesstes_element([])", None)],
    """
    def groesstes_element(liste):
        if len(liste) == 0:
            return None
        max_wert = liste[0]
        max_index = 0
        for i, wert in enumerate(liste):
            if wert > max_wert:
                max_wert = wert
                max_index = i
        return (max_wert, max_index)
    """,
    "Sonderfälle: Leere Liste (sonst IndexError bei liste[0]) und NEGATIVE Zahlen: "
    "Wer mit max_wert = 0 startet, findet bei [-3, -1, -7] fälschlich 0! Darum mit dem "
    "ersten Element starten. Mit > (nicht >=) bleibt bei Gleichstand der erste Index.",
    tipp="Starte mit max_wert = liste[0] (nicht 0!) und laufe mit enumerate durch die Liste.",
    vorlage="def groesstes_element(liste):\n    if len(liste) == 0:\n        return None\n    ...")

k.code(r"""
    ## Übung 3, Aufgabe 3.2 – Bildschirmdiagonale

    Monitore werden in Zoll (Diagonale) und mit Seitenverhältnis (z.B. 16:9)
    verkauft. Wie breit und hoch ist der Bildschirm in cm?

    Schreibe eine Funktion
        bildschirm_groesse(diagonale_zoll, breite_verh, hoehe_verh)
    die (breite_cm, hoehe_cm) als Tupel zurückgibt.

    Mathe dazu (Breite, Höhe und Diagonale bilden ein rechtwinkliges Dreieck):
        winkel = math.atan(hoehe_verh / breite_verh)
        breite = diagonale · cos(winkel)
        hoehe  = diagonale · sin(winkel)
    Vergiss nicht, Zoll in cm umzurechnen (1 Zoll = 2.54 cm) und
    import math zu schreiben!

    Beispiel: 27 Zoll, 16:9  →  ca. (59.77, 33.62)
    """,
    [F("bildschirm_groesse(27, 16, 9)"), F("bildschirm_groesse(24, 16, 10)"),
     F("bildschirm_groesse(15, 4, 3)"), F("bildschirm_groesse(10, 1, 1)")],
    """
    import math

    def zoll_zu_cm(zoll):
        return zoll * 2.54

    def bildschirm_groesse(diagonale_zoll, breite_verh, hoehe_verh):
        diagonale_cm = zoll_zu_cm(diagonale_zoll)
        winkel = math.atan(hoehe_verh / breite_verh)
        breite = diagonale_cm * math.cos(winkel)
        hoehe = diagonale_cm * math.sin(winkel)
        return (breite, hoehe)
    """,
    "Funktionen können andere Funktionen benutzen – hier wird zoll_zu_cm "
    "wiederverwendet. Alternative mit Pythagoras: faktor = diagonale / "
    "math.sqrt(b**2 + h**2), dann breite = b * faktor und hoehe = h * faktor.",
    tipp="Erst diagonale_cm = diagonale_zoll * 2.54, dann winkel mit math.atan, dann cos/sin.",
    vorlage="import math\n\ndef bildschirm_groesse(diagonale_zoll, breite_verh, hoehe_verh):\n    ...")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 20: Rekursion
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Rekursion – Die Matroschka",
    "Funktionen, die sich selbst aufrufen: Anker & Rekursionsschritt",
    "Vorlesung 4")

k.erklaerung("Was ist Rekursion?", r"""
    ## Funktionen können sich selbst aufrufen!

    Mit Funktionen und Schleifen kann man im Prinzip schon alles machen –
    aber manchmal wird es nicht schön. Eine sehr wichtige Eigenschaft
    von Funktionen fehlt noch: Sie können SICH SELBST aufrufen.
    Das nennt man REKURSION.

    Rekursion im Alltag:
      • MATROSCHKA-Puppen: Du öffnest eine Puppe – darin ist eine
        kleinere Puppe. Die öffnest du – wieder eine kleinere ... bis zur
        kleinsten, die sich nicht mehr öffnen lässt.
      • Zwei Spiegel gegenüber: ein Bild im Bild im Bild ...
      • In der Natur: Romanesco oder Farn – jedes Teilstück sieht aus
        wie das Ganze.
      • In der Informatik: Binärbäume.
    ---
    ## Das Warteschlangen-Beispiel

    Du stehst in einer langen Schlange und willst wissen, an welcher
    Stelle du stehst. Du kannst nicht nach vorne schauen. Also fragst du
    die Person vor dir: "An welcher Stelle stehst du?"
    Die fragt wieder ihre Vorderperson ... und so weiter.
    Die ERSTE Person sieht niemanden vor sich und sagt: "Ich bin Nummer 1!"
    Dann wird zurückgereicht: "Ich bin 2", "Ich bin 3", ...

      • Die erste Person ist der REKURSIONSANKER (hier hört es auf).
      • "Frag den Vordermann und rechne + 1" ist der REKURSIONSSCHRITT.
    ---
    ## Rekursive Definitionen

    Viele Dinge (besonders in Mathe und Informatik) sind in Bezug auf
    sich selbst definiert. Beispiele:
      • die Fibonacci-Folge
      • die Fakultät
      • der Programmcode, den wir schreiben (Blöcke in Blöcken)
      • Dateisysteme: Ordner können Unterordner haben, die wieder
        Unterordner haben ...

    Die wesentlichen Bestandteile jeder Rekursion:
      1. REKURSIONSANKER – der Anfangs- bzw. Ausgangszustand, bei dem
         die Rekursion aufhört (die kleinste Matroschka).
      2. REKURSIONSSCHRITT – die Anweisungen, um von einem Zustand zum
         nächsten zu kommen (Problem verkleinern, sich selbst aufrufen).
    ---
    ## Beispiel: Datei im Dateisystem suchen

      • Starte im obersten Ordner (Wurzel).
      • Gehe die Liste der Unterelemente durch und prüfe, ob die gesuchte
        Datei dabei ist.
      • Für jeden Unterordner: Mach dort GENAU DASSELBE (Rekursionsschritt).
      • Wurde die Datei gefunden ODER gibt es keine Unterordner mehr
        (man kann nicht weiter "absteigen"), kehrt die Suche zur Ebene
        darüber zurück (Rekursionsanker).
    ---
    ## Die Fakultät rekursiv

    Mathematisch:    n! = 1               wenn n = 0
                     n! = n · (n - 1)!    wenn n > 0

    In Python:
        def factorial(n):
            if n == 0:                      # Rekursionsanker
                return 1
            return n * factorial(n - 1)     # rekursiver Aufruf

    Was passiert bei factorial(3)?
        factorial(3) = 3 * factorial(2)
                     = 3 * 2 * factorial(1)
                     = 3 * 2 * 1 * factorial(0)
                     = 3 * 2 * 1 * 1
                     = 6
    ---
    ## Mehrfache und wechselseitige Rekursion

    Fibonacci:  fib(0) = 0,  fib(1) = 1,  fib(n) = fib(n-1) + fib(n-2)
    Folge: 0, 1, 1, 2, 3, 5, 8, 13, 21, ...
        def fibonacci(n):
            if n <= 1:                                  # Rekursionsanker
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)  # ZWEI Aufrufe
    Merke: Funktionen können sich auch MEHRMALS rekursiv aufrufen.

    Rekursion kann auch hin und her springen (wechselseitig):
        def is_even(n):
            if n == 0:
                return True
            return is_odd(n - 1)

        def is_odd(n):
            if n == 0:
                return False
            return is_even(n - 1)
    ---
    ## Probleme und Grenzen

      • Grundsätzlich lässt sich jede Schleife auch mit Rekursion umsetzen.
      • Ausnahme: Endlosschleifen bzw. Schleifen mit zu vielen Durchläufen.
      • Python hat eine maximale Tiefe von ungefähr 1000 Funktionsaufrufen.

    Ohne Rekursionsanker ruft sich die Funktion endlos auf:
        def fun(num):
            fun(num + 1)
        fun(0)
    → RecursionError: maximum recursion depth exceeded

    Rekursion oder Schleife (Iteration)? Kommt drauf an!
      • Rekursion ist oft eleganter bei verschachtelten Strukturen
        (Ordner, Bäume) und rekursiv definierten Problemen.
      • Schleifen sind in Python meist effizienter und haben kein
        Tiefenlimit.
      • Man braucht MINDESTENS EINEN Rekursionsanker (manchmal mehrere).
    """)

k.ausgabe("def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(5))",
          "5! = 5 · 4 · 3 · 2 · 1 · 1 = 120.")
k.ausgabe("def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(0))",
          "Direkt der Rekursionsanker: 0! = 1.")
k.ausgabe("def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n - 1) + fibonacci(n - 2)\n\nprint(fibonacci(7))",
          "Die Folge: 0, 1, 1, 2, 3, 5, 8, 13 → fib(7) = 13.",
          tipp="fib(0) = 0, fib(1) = 1, jede weitere ist die Summe der beiden vorherigen.")
k.ausgabe("def is_even(n):\n    if n == 0:\n        return True\n    return is_odd(n - 1)\n\n"
          "def is_odd(n):\n    if n == 0:\n        return False\n    return is_even(n - 1)\n\nprint(is_even(7))",
          "is_even(7) → is_odd(6) → is_even(5) → ... → is_odd(0) → False. 7 ist ungerade.")
k.ausgabe("def countdown(n):\n    if n == 0:\n        print('Start!')\n        return\n    print(n)\n    countdown(n - 1)\n\ncountdown(3)",
          "Ein Countdown als Rekursion: 3, 2, 1, dann der Anker bei 0: Start!")
k.ausgabe("def summe(n):\n    if n == 0:\n        return 0\n    return n + summe(n - 1)\n\nprint(summe(4))",
          "4 + 3 + 2 + 1 + 0 = 10.")
k.ausgabe("def fun(num):\n    fun(num + 1)\n\nfun(0)",
          "Kein Rekursionsanker → die Funktion ruft sich endlos auf, bis Python bei ca. 1000 "
          "Aufrufen abbricht: RecursionError. (Vorlesung 4)")
k.ausgabe("def zeige(n):\n    if n == 0:\n        return\n    zeige(n - 1)\n    print(n)\n\nzeige(3)",
          "Knifflig: Das print kommt NACH dem rekursiven Aufruf. Es wird also erst ganz nach "
          "unten abgestiegen, und beim Zurückkehren ausgegeben: 1, 2, 3.",
          tipp="Wann wird print ausgeführt – vor oder nach dem tieferen Aufruf?")

k.mc("Was ist ein Rekursionsanker?",
     ["Der Fall, bei dem die Funktion sich NICHT mehr selbst aufruft und die Rekursion endet",
      "Der erste Aufruf der Funktion",
      "Eine besonders schwere Variable",
      "Der Fehler, der bei zu tiefer Rekursion kommt"],
     "Der Anker ist der Ausgangszustand – wie die kleinste Matroschka.")

k.mc("Wie viele Rekursionsanker braucht eine rekursive Funktion?",
     ["Mindestens einen", "Genau keinen", "Immer genau zwei", "So viele wie Parameter"],
     "Ohne Anker gibt es eine endlose Rekursion. Manchmal braucht man auch mehrere "
     "Ankerfälle (Fibonacci: n = 0 und n = 1, hier zusammengefasst als n <= 1).")

k.mc("Wie macht man eine Funktion in Python rekursiv?",
     ["Indem sie sich in ihrem eigenen Körper selbst aufruft",
      "Indem man 'recursive' vor def schreibt",
      "Mit import recursion",
      "Indem man sie in eine while-Schleife packt"],
     "Eine rekursive Funktion ruft sich selbst auf – z.B. return n * factorial(n - 1).")

k.mc("Bei den Matroschka-Puppen: Was ist der Rekursionsanker?",
     ["Die kleinste Puppe, die sich nicht mehr öffnen lässt",
      "Die größte Puppe",
      "Das Öffnen einer Puppe",
      "Der Laden, in dem man sie kauft"],
     "Bei der kleinsten Puppe hört das 'Öffnen und weiter suchen' auf.")

k.mc("Was ist bei der Dateisuche im Ordnerbaum der Rekursionsschritt?",
     ["In jedem Unterordner wieder genau dieselbe Suche starten",
      "Die Datei gefunden haben",
      "Den Computer ausschalten",
      "Alle Dateien löschen"],
     "Der Schritt ist: 'Mach in jedem Unterordner dasselbe'. Der Anker: Datei gefunden "
     "oder keine Unterordner mehr.")

k.wf("Python kann beliebig tief rekursiv aufrufen.", False,
     "Die maximale Aufruftiefe liegt bei ungefähr 1000. Danach: RecursionError.")

k.mc("Ist im Allgemeinen Rekursion oder Iteration (Schleifen) sinnvoller?",
     ["Kommt auf das Problem an – Rekursion ist oft eleganter, Schleifen oft effizienter",
      "Immer Rekursion",
      "Immer Iteration",
      "Beides ist verboten"],
     "Quiz aus Vorlesung 4: Für verschachtelte Strukturen ist Rekursion toll. In Python "
     "sind Schleifen meist effizienter und haben kein Tiefenlimit.")

k.wf("Grundsätzlich lässt sich jede Schleife auch mit Rekursion umsetzen (außer bei zu vielen Durchläufen).", True,
     "Genau so steht es in Vorlesung 4. Die Grenze ist die maximale Rekursionstiefe.")

k.code(r"""
    ## Fakultät rekursiv

    Schreibe eine REKURSIVE Funktion   fakultaet(n)   (ohne Schleife!):
        fakultaet(0) = 1
        fakultaet(n) = n * fakultaet(n - 1)
    """,
    [F("fakultaet(0)", 1), F("fakultaet(1)", 1), F("fakultaet(5)", 120),
     F("fakultaet(15)", 1307674368000)],
    """
    def fakultaet(n):
        if n == 0:
            return 1
        return n * fakultaet(n - 1)
    """,
    tipp="Rekursionsanker: if n == 0: return 1. Schritt: return n * fakultaet(n - 1)",
    vorlage="def fakultaet(n):\n    if n == 0:\n        ...\n    return ...")

k.code(r"""
    ## Fibonacci rekursiv

    Schreibe eine rekursive Funktion   fibonacci(n)   :
        fibonacci(0) = 0
        fibonacci(1) = 1
        fibonacci(n) = fibonacci(n - 1) + fibonacci(n - 2)
    """,
    [F("fibonacci(0)", 0), F("fibonacci(1)", 1), F("fibonacci(2)", 1),
     F("fibonacci(7)", 13), F("fibonacci(15)", 610)],
    """
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    """,
    "Zwei rekursive Aufrufe pro Schritt – deshalb wird das bei großen n sehr langsam "
    "(es wird vieles doppelt berechnet). Probier mal fibonacci(35) aus!",
    tipp="Anker: if n <= 1: return n. Schritt: Summe der zwei vorherigen.")

k.code(r"""
    ## Quersumme rekursiv

    Die Quersumme ist die Summe aller Ziffern: quersumme(1234) = 1+2+3+4 = 10.
    Schreibe eine rekursive Funktion   quersumme(n)   für n >= 0.

    Trick (Modulo und Ganzzahl-Division!):
        1234 % 10   → 4      (die letzte Ziffer)
        1234 // 10  → 123    (die Zahl ohne letzte Ziffer)
    """,
    [F("quersumme(0)", 0), F("quersumme(7)", 7), F("quersumme(1234)", 10),
     F("quersumme(99999)", 45)],
    """
    def quersumme(n):
        if n < 10:
            return n
        return n % 10 + quersumme(n // 10)
    """,
    "Anker: Eine einstellige Zahl ist ihre eigene Quersumme. Schritt: letzte Ziffer + "
    "Quersumme vom Rest. (Anker n == 0 → return 0 funktioniert auch.)",
    tipp="Letzte Ziffer: n % 10. Rest: n // 10. Anker: n < 10.")

# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 21: Ausblick Java
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Ausblick: Java – die nächste Sprache",
    "Statische Typen, geschweifte Klammern, Compiler – Python vs. Java",
    "Vorlesung 4")

k.erklaerung("Java im Vergleich zu Python", r"""
    ## Java – die nächste Sprache im Studium

    Wie unterscheidet sich Java von Python?

    1. STATISCHE TYPISIERUNG
       Die Typen von Variablen, Rückgabewerten und Funktionsparametern
       müssen im Quelltext STEHEN.
       Alltag: Ein Formular mit festen Feldern – ins Feld "Alter (Zahl)"
       kannst du keinen Text schreiben.
       → Zur Laufzeit kann weniger schiefgehen, Programme sind robuster.

    2. OBJEKTORIENTIERUNG
       Funktionen auf Objekten heißen METHODEN. Die kennst du schon:
       "Hallo".upper()

    3. EINRÜCKUNG IST EGAL
       Stattdessen nutzt man geschweifte Klammern { } für Blöcke und
       Semikola ; am Ende von Anweisungen.

    4. JAVA WIRD KOMPILIERT
       Man führt nicht direkt den Quelltext aus, sondern BYTECODE.
       Vorher muss der Compiler aufgerufen werden: javac
    ---
    ## Variablen und Verzweigungen

      Python                     Java
      x = 5                      int x = 5;
      s = 'Lorem'                String s = "Lorem";

    !! In Java werden Strings NUR mit "..." geschrieben, nicht mit '...'.

      Python                     Java
      if x < 0:                  if (x < 0) {
          print("Negativ")           System.out.println("Negativ");
      elif x > 0:                } else if (x > 0) {
          print("Positiv")           System.out.println("Positiv");
      else:                      } else {
          print("Null")              System.out.println("Null");
                                 }
    ---
    ## Schleifen

      while:
      Python                     Java
      while n > 0:               while (n > 0) {
          n = n // 2 - 1             n = n / 2 - 1;
                                 }
    (In Java ist / bei int-Zahlen schon die Ganzzahl-Division!)
    Zusätzlich gibt es in Java eine do-while-Schleife (1. Semester).

      for-each:
      Python                     Java
      for f in fruits:           for (String f : fruits) {
          print(f + " tasted")       System.out.println(f + " tasted");
                                 }

      for mit Zähler:
      Python                     Java
      for i in range(1, 11):     for (int i = 1; i < 11; ++i) {
          print(i * i)               System.out.println(i * i);
                                 }
    ---
    ## Funktionen

      Python                         Java
      def say_hello(name):           void sayHello(String name) {
          print("Hello " + name)         System.out.println("Hello " + name);
                                     }

      • void bedeutet: Diese Funktion gibt NICHTS zurück.
      • Der Parameter hat einen Typ: String name.
      • In Java schreibt man Namen in camelCase (sayHello), nicht snake_case.
    """)

k.mc("Wie schreibt man   x = 5   in Java?",
     ["int x = 5;", "x = 5", "var x := 5", "int x = 5"],
     "Typ angeben (statische Typisierung) und Semikolon am Ende.")

k.mc("Welcher String ist in Java gültig?",
     ['"Lorem"', "'Lorem'", "Beide", "Keiner"],
     "In Java können Strings nur mit doppelten Anführungszeichen definiert werden.")

k.mc("Was ersetzt in Java die Einrückung als Kennzeichen für Blöcke?",
     ["Geschweifte Klammern { } (und Semikola ; zum Trennen von Anweisungen)",
      "Doppelpunkte",
      "Eckige Klammern",
      "Nichts, Java hat keine Blöcke"],
     "Einrückung ist in Java irrelevant – Blöcke stehen in { }.")

k.mc("Wie heißt der Java-Compiler?",
     ["javac", "python3", "jvm-run", "gcc"],
     "javac übersetzt den Quelltext in Bytecode, der dann ausgeführt wird.")

k.mc("Was bedeutet statische Typisierung?",
     ["Typen von Variablen, Parametern und Rückgabewerten stehen im Quelltext",
      "Variablen dürfen sich nie ändern",
      "Das Programm läuft ohne Typen",
      "Typen werden erst beim Ausführen geraten"],
     "In Java steht z.B. int x = 5; – dadurch kann zur Laufzeit weniger schiefgehen.")

k.mc("Welche Java-Schleife entspricht   for i in range(1, 11):  ?",
     ["for (int i = 1; i < 11; ++i) { ... }",
      "for (int i = 1; i <= 11; ++i) { ... }",
      "for (i in 1..11) { ... }",
      "while (i < 11) for i"],
     "Start 1, Bedingung i < 11 (also bis 10), Schritt ++i (i um 1 erhöhen).")

k.mc("Wie gibt man in Java etwas in der Konsole aus?",
     ["System.out.println(...)", "print(...)", "console.log(...)", "echo ..."],
     "System.out.println gibt eine Zeile aus.")

k.mc("Wie schreibt man Pythons   elif   in Java?",
     ["else if", "elsif", "elif", "otherwise"],
     "} else if (x > 0) { ...")

k.mc("Was bedeutet   void   in   void sayHello(String name)  ?",
     ["Die Funktion gibt keinen Wert zurück",
      "Die Funktion ist leer",
      "Die Funktion ist verboten",
      "Der Parameter ist optional"],
     "void = 'nichts'. Es gibt keinen Rückgabewert.")

k.wf("In Java ist die Einrückung genauso Pflicht wie in Python.", False,
     "In Java ist Einrückung für den Compiler egal (aber für Menschen trotzdem wichtig!).")

k.wf("Java hat eine do-while-Schleife, Python nicht.", True,
     "Stimmt. Die lernst du im ersten Semester kennen.")

k.mc("Java: int n = 7;  n = n / 2 - 1;   Welchen Python-Code entspricht das?",
     ["n = n // 2 - 1", "n = n / 2 - 1", "n = n % 2 - 1", "n = n ** 2 - 1"],
     "In Java ist / bei zwei int-Zahlen eine Ganzzahl-Division – in Python ist das //.")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 22: Guter Code & Sprachensalat
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Guter Code & Sprachensalat",
    "Allgemeiner programmieren, Effizienz und andere Programmier-Paradigmen",
    "Vorlesung 4")

k.erklaerung("Guter Code", r"""
    ## Allgemein statt tausend Sonderfälle

    Probleme kann man oft ABSTRAKTER betrachten, um sie allgemeiner (und
    einfacher) zu lösen und weniger Code zu duplizieren.
    Anfänger schreiben leider oft tausende Bedingungen statt einer
    allgemeinen Lösung.

    Alltag: Statt 20 Rezepten "Apfelkuchen", "Kirschkuchen", ... schreibst
    du EIN Rezept "Obstkuchen" mit dem Obst als Zutat (Parameter).

    Aber: Nicht ZU "klug" designen – sonst verstehst du es später selbst
    nicht mehr!
    ---
    ## Beispiel: Vier gewinnt

    Verbose (umständliche) Version – zwei fast gleiche Funktionen:
        def vier_waagerecht(x, y):
            entry = grid[y][x]
            for i in range(1, 4):
                if grid[y][x+i] != entry:
                    return False
            return True

        def vier_senkrecht(x, y):
            entry = grid[y][x]
            for i in range(1, 4):
                if grid[y+i][x] != entry:
                    return False
            return True

    Kompakte Version – EINE Funktion mit Richtung (xo, yo):
        def vier_in_folge(x, y, xo, yo):
            entry = grid[y][x]
            for i in range(1, 4):
                if grid[y+i*yo][x+i*xo] != entry:
                    return False
            return True

      waagerecht:  vier_in_folge(x, y, 1, 0)
      senkrecht:   vier_in_folge(x, y, 0, 1)
      diagonal:    vier_in_folge(x, y, 1, 1)   ← gibt's gratis dazu!
    ---
    ## (Mangelnde) Effizienz

    Im Vorkurs und im 1. Semester ist Geschwindigkeit noch nicht so
    wichtig. Trotzdem sollte man sich beim Grund-Design Gedanken machen.
    (Windows, Discord, ... sind nicht sonderlich effizient – Rechner
    könnten heute eigentlich viel schneller sein.)

    Beispiele:
      • Funktionsaufrufe, die in einer Schleife IMMER das gleiche Ergebnis
        liefern, zieht man VOR die Schleife.
      • Eine Datei zeilenweise bearbeiten: NICHT für jede Zeile die Datei
        öffnen, schließen und die n-te Zeile lesen/ändern – sondern
        einmal öffnen und alles durchgehen.
    """)

k.erklaerung("Sprachensalat – andere Programmier-Paradigmen", r"""
    ## Nicht jede Sprache tickt wie Python

    FUNKTIONALE SPRACHEN (z.B. Haskell – benannt nach Haskell Brooks Curry)
      • Verkettung von Funktionen ist die Grundlage für komplexe Programme
      • Es gibt keine Variablen, nur Konstanten
      • Funktionen sind wie Werte: Sie können Parameter und Rückgabewerte sein
      • Kombinatoren verketten Funktionen weiter
      • Funktionen kann man teilweise ("partiell") anwenden: CURRYING

    STACK-BASIERTE SPRACHEN (z.B. Forth – "Forth was discovered, not
    invented", Charles H. Moore)
      • Es gibt einen oder mehrere STAPEL (Stacks) für Daten –
        wie ein Tellerstapel: Man legt oben drauf und nimmt oben weg
      • Operatoren arbeiten nur auf dem Stack
      • Sehr hardwarenah, da fast jede CPU eine Stack-Maschine enthält
      • Keine Arrays, Schleifen, Listen – nur den STACK
    ---
    ## Noch verrückter

    APL (A Programming Language)
      • Alles basiert auf N-dimensionalen Arrays – auch eine Zahl ist nur
        ein 0D-Array
      • Besteht im Wesentlichen aus einzelnen Symbolen
      • Conways "Game of Life" passt in eine einzige Zeile

    AsciiDots – 2D-Programmierung
      • Code muss nicht zeilenbasiert sein: "Punkte" wandern über Linien
        aus ASCII-Zeichen
      • Schleifen sind Kreise, es gibt keine expliziten Variablen

    Piet – Programme sind BILDER
      • Besteht aus 20 Farben (18 Farben + Schwarz und Weiß)
      • Schon einfache Probleme sind wie ein Puzzle
      • Am Ende hat man ein schönes Bild

    !! Key Take-Away: Es gibt verschiedene Paradigmen, die Probleme
    !! unterschiedlich gut lösen. Sie schließen sich nicht aus, sondern
    !! leben friedlich zusammen (Python kann z.B. auch "funktional").
    """)

k.ausgabe('''grid = [
    [1, 1, 1, 1],
    [2, 0, 0, 0],
    [2, 0, 0, 0],
    [2, 0, 0, 0],
]

def vier_in_folge(x, y, xo, yo):
    entry = grid[y][x]
    for i in range(1, 4):
        if grid[y + i * yo][x + i * xo] != entry:
            return False
    return True

print(vier_in_folge(0, 0, 1, 0))
print(vier_in_folge(0, 0, 0, 1))''',
          "(0, 0, 1, 0) prüft waagerecht in Zeile 0: 1, 1, 1, 1 → True. (0, 0, 0, 1) prüft "
          "senkrecht in Spalte 0: 1, 2, ... → schon das zweite passt nicht → False.",
          tipp="xo = Schritt nach rechts, yo = Schritt nach unten.")

k.mc("Welche Richtung (xo, yo) prüft bei vier_in_folge eine DIAGONALE?",
     ["(1, 1)", "(1, 0)", "(0, 1)", "(0, 0)"],
     "Bei jedem Schritt eins nach rechts UND eins nach unten → diagonal.")

k.mc("Warum ist vier_in_folge(x, y, xo, yo) besser als zwei getrennte Funktionen?",
     ["Kein doppelter Code, und Diagonalen gibt's gratis dazu",
      "Weil Funktionen mit 4 Parametern immer schneller sind",
      "Weil Python nur eine Funktion pro Datei erlaubt",
      "Ist es nicht – zwei Funktionen sind immer besser"],
     "Die Logik ist bis auf die Richtung identisch. Mit Parametern für die Richtung "
     "braucht man nur eine Funktion.")

k.mc("Welcher Tipp zur Effizienz stammt aus der Vorlesung?",
     ["Funktionsaufrufe, die in einer Schleife immer dasselbe liefern, vor die Schleife ziehen",
      "Für jede Zeile einer Datei die Datei neu öffnen",
      "Möglichst viele globale Variablen verwenden",
      "Alle Schleifen durch Rekursion ersetzen"],
     "Was sich nicht ändert, muss man nicht 1000-mal neu berechnen.")

k.mc("Was ist typisch für funktionale Sprachen wie Haskell?",
     ["Es gibt keine Variablen, nur Konstanten – und Funktionen sind wie Werte",
      "Alles ist ein Bild aus 20 Farben",
      "Es gibt nur einen Stack",
      "Alles ist ein N-dimensionales Array"],
     "Funktional: Verkettung von Funktionen, Konstanten, Funktionen als Parameter/Rückgabewerte, Currying.")

k.mc("Welche Sprache arbeitet nur mit einem Stapel (Stack)?",
     ["Forth", "Piet", "APL", "Haskell"],
     "Forth ist stack-basiert und sehr hardwarenah.")

k.mc("In welcher Sprache sind Programme Bilder aus Farben?",
     ["Piet", "AsciiDots", "Forth", "Java"],
     "Piet besteht aus 20 Farben – am Ende hat man ein schönes Bild.")

k.mc("Was bedeutet 'Currying'?",
     ["Eine Funktion nur teilweise (partiell) anwenden",
      "Eine Funktion besonders scharf würzen",
      "Eine Schleife abbrechen",
      "Code in Farben darstellen"],
     "Benannt nach Haskell Brooks Curry: Man gibt einer Funktion erst einen Teil ihrer "
     "Parameter und bekommt eine neue Funktion für den Rest.")

k.wf("Programmier-Paradigmen schließen sich gegenseitig aus.", False,
     "Sie leben friedlich zusammen – viele Sprachen (auch Python) vereinen mehrere Paradigmen.")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 23: Bonus – RSA
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Bonus: RSA-Verschlüsselung",
    "Geheime Nachrichten mit Modulo und Potenzen (Übung 1, Aufgabe 6)",
    "Übung 1")

k.erklaerung("RSA – Verschlüsseln mit Mathe", r"""
    ## Die Idee (keine Panik – das ist ein Exkurs!)

    RSA ist ein echtes Verschlüsselungsverfahren, das z.B. im Internet
    benutzt wird. Alltag: ein BRIEFKASTEN. Jeder kann etwas einwerfen
    (öffentlicher Schlüssel), aber nur der Besitzer hat den Schlüssel
    zum Herausholen (privater Schlüssel).

    Man braucht zwei Primzahlen p und q. Ihr Produkt n = p · q legt fest:
    Nach jeder Rechnung wird das Ergebnis mit "mod n" in den Bereich
    0 bis n-1 gebracht.
    ---
    ## Die Zahlen aus der Übung

        p = 3,  q = 11
        n = p · q = 33
        N = (p - 1) · (q - 1) = 2 · 10 = 20
        e = 3     (größter gemeinsamer Teiler von e und N ist 1)
        d = 7     (denn e · d mod N = 21 mod 20 = 1)

    VERSCHLÜSSELN einer Nachricht m (eine Zahl mit 0 <= m < n):
        c = m ** e % n          →   c = m ** 3 % 33

    ENTSCHLÜSSELN eines Geheimtextes c:
        m = c ** d % n          →   m = c ** 7 % 33

    Beispiel: m = 4
        verschlüsseln:  4 ** 3 = 64,  64 % 33 = 31   → c = 31
        entschlüsseln:  31 ** 7 % 33 = 4              → wieder m = 4 !

    Python-Tipp: pow(m, e, n) rechnet m ** e % n besonders effizient.
    """)

k.ausgabe("print((3 - 1) * (11 - 1))", "N = (p-1)·(q-1) = 2 · 10 = 20.")
k.ausgabe("print(3 * 7 % 20)", "e · d mod N = 21 mod 20 = 1 – genau das muss für d gelten.")
k.ausgabe("print(4 ** 3 % 33)", "Verschlüsseln: 4³ = 64, 64 % 33 = 31.")
k.ausgabe("print(31 ** 7 % 33)", "Entschlüsseln: 31⁷ mod 33 ergibt wieder die ursprüngliche Nachricht 4!")
k.ausgabe("print(pow(4, 3, 33))", "pow(m, e, n) ist dasselbe wie m ** e % n: 31.")

k.mc("Warum muss die Nachricht m die Bedingung 0 <= m < n erfüllen?",
     ["Weil alle Ergebnisse mod n im Bereich 0 bis n-1 liegen – größere Zahlen gingen verloren",
      "Weil Python keine großen Zahlen kann",
      "Weil m eine Primzahl sein muss",
      "Das muss sie gar nicht"],
     "Nach dem Entschlüsseln kommt immer eine Zahl zwischen 0 und n-1 heraus. Eine "
     "größere Nachricht könnte man also nie zurückbekommen.")

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
    tipp="Zwei kurze Funktionen mit return ... ** ... % n")


# ────────────────────────────────────────────────────────────────────────────
#  KAPITEL 24: Bonus – Farben umrechnen
# ────────────────────────────────────────────────────────────────────────────
k = neues_kapitel(
    "Bonus: Farben von HSV nach RGB umrechnen",
    "Eine größere Funktion mit math.floor und vielen Fällen (Übung 3, 3.3)",
    "Übung 3")

k.erklaerung("HSV und RGB", r"""
    ## Zwei Arten, Farben zu beschreiben

    RGB: Wie viel Rot, Grün, Blau? (Jeweils 0 bis 1.)
         (1, 0, 0) = Rot,  (1, 1, 0) = Gelb,  (0.5, 0.5, 0.5) = Grau

    HSV: So wie im Farbwähler eines Malprogramms:
      H (Hue)        = Farbton auf dem Farbkreis, 0 bis 360 Grad
                       (0 = Rot, 120 = Grün, 240 = Blau)
      S (Saturation) = Sättigung 0 bis 1 (grau ↔ knallig)
      V (Value)      = Helligkeit 0 bis 1 (schwarz ↔ hell)

    HSV ist praktisch, um z.B. Farben mit gleichem Farbtonabstand zu
    erzeugen.
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

    Das Ergebnis liegt im Bereich [0, 1].
    """)

k.code(r"""
    ## Übung 3, Aufgabe 3.3 – HSV nach RGB

    Schreibe eine Funktion   hsv_zu_rgb(h, s, v)   , die ein Tupel (r, g, b)
    zurückgibt. Benutze die Formeln von der vorherigen Seite.
    (Tipp: Das ist ein perfekter Fall für if/elif/else oder match!)

    Beispiele:  hsv_zu_rgb(0, 1, 1)   → (1, 0, 0)     (Rot)
                hsv_zu_rgb(120, 1, 1) → (0, 1, 0)     (Grün)
    """,
    [F("hsv_zu_rgb(0, 1, 1)"), F("hsv_zu_rgb(120, 1, 1)"), F("hsv_zu_rgb(240, 1, 1)"),
     F("hsv_zu_rgb(60, 1, 1)"), F("hsv_zu_rgb(30, 1, 1)"), F("hsv_zu_rgb(300, 0.5, 0.8)"),
     F("hsv_zu_rgb(200, 0, 0.5)"), F("hsv_zu_rgb(360, 1, 1)")],
    """
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
    """,
    "Erst alle Hilfswerte berechnen, dann mit if/elif/else den passenden Fall "
    "auswählen. Mit match hi: case 1: ... case _: ... geht es genauso.",
    tipp="import math nicht vergessen. hi = math.floor(h / 60). Die Fälle mit if/elif/else.",
    vorlage="import math\n\ndef hsv_zu_rgb(h, s, v):\n    hi = math.floor(h / 60)\n    ...")


# ════════════════════════════════════════════════════════════════════════════
#  TEIL 3: SPICKZETTEL
# ════════════════════════════════════════════════════════════════════════════

SPICKZETTEL = r"""
## DATENTYPEN
    bool  True / False      int  42, -2        float  2.5, 1.6e6
    str   "Text", 'Text'    None (NoneType)    type(x) → zeigt den Typ

## OPERATOREN
    + - *      /  (immer float)     // (ganzzahlig, abrunden)
    %  (Rest)  ** (Potenz)          Punkt vor Strich, Klammern zuerst
    == != < > <= >=  → True/False
    and (beide)   or (mind. einer)   not (umdrehen)   Reihenfolge: not, and, or

## VARIABLEN
    name = wert       (rechte Seite zuerst!)       x += 1  x -= 1  x *= 2
    snake_case, Beginn mit Buchstabe oder _, Groß/klein zählt

## UMWANDELN
    int('5') → 5   int(3.9) → 3   float(5) → 5.0   str(3) → '3'
    bool(0) → False   bool('') → False   bool('false') → True (!)

## EIN-/AUSGABE
    print(x)   print(a, b)   print(f'Hallo {name}, du bist {alter}')
    eingabe = input('Text: ')            → immer str!
    zahl = int(input('Zahl: '))

## STRINGS
    len(s)  s[0]  s[-1]  s.lower()  s.upper()  s1 + s2
    s.split(',')  → Liste      s.replace('alt', 'neu')     s.strip()
    \n Zeilenumbruch   \t Tab   Strings sind unveränderlich

## VERZWEIGUNGEN
    if bedingung:          match wert:
        ...                    case 1:
    elif andere:                   ...
        ...                    case _:      ← sonst
    else:                          ...
        ...

## SCHLEIFEN
    while bedingung:         for x in liste:          for i in range(start, end, step):
        ...                      ...                      ...
    for i, x in enumerate(liste):     for a, b in zip(liste1, liste2):
    break = Schleife beenden    continue = nächste Runde (nur innerste Schleife)
    Strg + C bricht Endlosschleifen ab

## LISTEN  [ ]
    lst = [3, 4, 1, 2]   lst[0]  lst[-1]  len(lst)   4 in lst   lst.index(4)
    lst.append(x)  lst.pop()  del lst[i]  lst.clear()  lst.sort()  lst.reverse()
    lst1 + lst2    lst.copy()   (lst2 = lst1 ist KEINE Kopie!)
    Slicing: lst[start:end:step]   end exklusiv   lst[::-1] = rückwärts

## TUPEL  ( )
    t = (1, 2, 3)   unveränderlich   a, b, c = t   list(t)   tuple(lst)

## DICTIONARIES  { }
    d = {'a': 5}   d['a']   d['neu'] = 1   d.get('x', 0)   'a' in d   del d['a']
    for key in d:   zaehler[k] = zaehler.get(k, 0) + 1

## DATEIEN
    with open('datei.txt', 'r') as f:     r lesen  w (über)schreiben
        inhalt = f.read()                 a anhängen  x neu erstellen
        zeilen = f.readlines()            f.read(5)   f.readline()
    with open('datei.txt', 'w') as f:
        f.write('Text\n')                 (kein automatischer Zeilenumbruch!)

## FUNKTIONEN
    def name(param1, param2):
        ...
        return ergebnis          ohne return → None
    Lokale Variablen sind außen unsichtbar.  global x  → globale ändern
    import math → math.sqrt(16), math.pi, math.floor(3.7), math.sin(...)

## REKURSION
    def fakultaet(n):
        if n == 0:                    ← Rekursionsanker
            return 1
        return n * fakultaet(n - 1)   ← Rekursionsschritt
    Max. Tiefe ca. 1000 → sonst RecursionError

## FEHLER
    NameError (Name unbekannt)   SyntaxError (Grammatik)   IndentationError
    TypeError ('a' + 1)   ValueError (int('a'))   ZeroDivisionError
    IndexError (Index zu groß)   KeyError (Schlüssel fehlt)
    lexikalisch = falsches "Wort" · syntaktisch = falsche Grammatik
    semantisch = falsche Logik

## JAVA
    int x = 5;   String s = "Text";   if (x < 0) { ... } else if (...) { ... }
    for (int i = 1; i < 11; ++i) { ... }   System.out.println(...);   javac
"""


# ════════════════════════════════════════════════════════════════════════════
#  TEIL 4: MENÜ, FORTSCHRITT, PRÜFUNG
# ════════════════════════════════════════════════════════════════════════════

FORTSCHRITT_DATEI = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "vorkurs_quiz_fortschritt.json")


def fortschritt_laden():
    try:
        with open(FORTSCHRITT_DATEI, encoding="utf-8") as f:
            daten = json.load(f)
    except (OSError, ValueError):
        daten = {}
    daten.setdefault("kapitel", {})
    daten.setdefault("fehlerkiste", [])
    daten.setdefault("pruefungen", [])
    return daten


def fortschritt_speichern(daten):
    try:
        with open(FORTSCHRITT_DATEI, "w", encoding="utf-8") as f:
            json.dump(daten, f, ensure_ascii=False, indent=1)
    except OSError:
        pass  # Speichern ist nett, aber nicht lebenswichtig


def alle_fragen():
    return {f.id: f for kap in KAPITEL for f in kap.fragen()}


def balken(wert, maximum, breite=12):
    if not maximum:
        return grau("░" * breite)
    voll = round(breite * wert / maximum)
    farbe = gruen if wert / maximum >= 0.8 else (gelb if wert / maximum >= 0.5 else rot)
    return farbe("█" * voll) + grau("░" * (breite - voll))


def fragen_runde(fragen, daten, zeige_kapitel=False, erklaerungen=None):
    """Stellt eine Folge von Fragen (Erklärungen dazwischen möglich).
       Rückgabe: (punkte, anzahl, liste_der_falschen)."""
    elemente = erklaerungen if erklaerungen is not None else fragen
    anzahl = sum(1 for e in elemente if isinstance(e, Frage))
    punkte, nr, falsche = 0, 0, []
    for e in elemente:
        if isinstance(e, Erklaerung):
            e.zeigen()
            continue
        nr += 1
        if zeige_kapitel:
            print()
            print(grau(f"  (aus Kapitel {e.kapitel.nummer}: {e.kapitel.titel})"))
        ok = e.stellen(nr, anzahl)
        if ok:
            punkte += 1
            if e.id in daten["fehlerkiste"]:
                daten["fehlerkiste"].remove(e.id)
        else:
            falsche.append(e)
            if e.id not in daten["fehlerkiste"]:
                daten["fehlerkiste"].append(e.id)
        fortschritt_speichern(daten)
        print()
        print("  " + grau(f"Punkte bisher: {punkte}/{nr}"))
        weiter("[Enter] = nächste Frage   ·   'menü' = zurück zum Hauptmenü")
    return punkte, anzahl, falsche


def zusammenfassung(punkte, anzahl):
    print()
    print(magenta("═" * BREITE))
    quote = punkte / anzahl if anzahl else 0
    print("  " + fett(f"ERGEBNIS: {punkte} von {anzahl} Punkten ({quote:.0%})  ") + balken(punkte, anzahl, 20))
    if quote >= 0.9:
        print("  " + gruen("Hervorragend! Das Thema sitzt. 🎓"))
    elif quote >= 0.7:
        print("  " + gruen("Sehr ordentlich! Schau dir die falschen Fragen nochmal an."))
    elif quote >= 0.5:
        print("  " + gelb("Gut auf dem Weg! Wiederhole das Kapitel ruhig noch einmal."))
    else:
        print("  " + gelb("Nicht aufgeben – lies die Erklärungen nochmal in Ruhe und probier es erneut!"))
    print(magenta("═" * BREITE))


def kapitel_spielen(kap, daten):
    eintrag = daten["kapitel"].get(str(kap.nummer))
    mit_erkl = True
    print()
    print(magenta("═" * BREITE))
    print("  " + fett(magenta(f"KAPITEL {kap.nummer}: {kap.titel}")))
    print("  " + kap.beschreibung)
    print("  " + grau(f"Quelle: {kap.quelle}   ·   {len(kap.fragen())} Fragen/Aufgaben"))
    print(magenta("═" * BREITE))
    if eintrag:
        a = eingabe("\n  Du kennst das Kapitel schon. Erklärungen nochmal anzeigen? (j/n): ")
        mit_erkl = a.strip().lower() not in ("n", "nein")
    else:
        weiter("[Enter] = los geht's")
    elemente = kap.elemente if mit_erkl else kap.fragen()
    punkte, anzahl, falsche = fragen_runde(None, daten, erklaerungen=elemente)
    zusammenfassung(punkte, anzahl)
    alt = daten["kapitel"].get(str(kap.nummer), {}).get("best", -1)
    if punkte > alt:
        daten["kapitel"][str(kap.nummer)] = {"best": punkte, "max": anzahl}
        if alt >= 0:
            print("  " + gruen("Neuer persönlicher Rekord für dieses Kapitel!"))
    fortschritt_speichern(daten)
    if falsche:
        a = eingabe(f"\n  {len(falsche)} Frage(n) waren falsch. Jetzt direkt wiederholen? (j/n): ")
        if a.strip().lower() in ("j", "ja", "y"):
            p2, a2, _ = fragen_runde(falsche, daten)
            zusammenfassung(p2, a2)
    weiter()


def pruefung(daten):
    pool = [f for f in alle_fragen().values() if not f.ist_code_aufgabe]
    anzahl = min(30, len(pool))
    print()
    print(magenta("═" * BREITE))
    print("  " + fett(magenta("ABSCHLUSSPRÜFUNG")))
    print(f"  {anzahl} zufällige Fragen aus ALLEN Kapiteln – ohne Erklärungen vorher.")
    print("  Wie in einer echten Prüfung: Erst denken, dann tippen!")
    print(magenta("═" * BREITE))
    weiter("[Enter] = Prüfung starten")
    auswahl = random.sample(pool, anzahl)
    punkte, anzahl, _ = fragen_runde(auswahl, daten, zeige_kapitel=True)
    zusammenfassung(punkte, anzahl)
    quote = punkte / anzahl
    for grenze, note in ((0.95, "1,0"), (0.9, "1,3"), (0.85, "1,7"), (0.8, "2,0"), (0.75, "2,3"),
                         (0.7, "2,7"), (0.65, "3,0"), (0.6, "3,3"), (0.55, "3,7"), (0.5, "4,0")):
        if quote >= grenze:
            break
    else:
        note = "5,0"
    print("  " + fett(f"Deine (inoffizielle) Note: {note}"))
    daten["pruefungen"].append({"punkte": punkte, "max": anzahl})
    fortschritt_speichern(daten)
    weiter()


def fehlerkiste(daten):
    alle = alle_fragen()
    ids = [i for i in daten["fehlerkiste"] if i in alle]
    if not ids:
        print("\n  " + gruen("Deine Fehlerkiste ist leer – super! Spiel erst ein paar Kapitel."))
        weiter()
        return
    print()
    print("  " + fett(f"FEHLERKISTE: {len(ids)} Frage(n), die du noch nicht richtig hattest."))
    print("  " + grau("Richtig beantwortete Fragen fliegen aus der Kiste raus (wie bei Karteikarten)."))
    weiter("[Enter] = los")
    fragen = [alle[i] for i in ids]
    random.shuffle(fragen)
    punkte, anzahl, _ = fragen_runde(fragen, daten, zeige_kapitel=True)
    zusammenfassung(punkte, anzahl)
    weiter()


def spickzettel_zeigen():
    print()
    print(magenta("═" * BREITE))
    print("  " + fett(magenta("SPICKZETTEL – alles Wichtige auf einen Blick")))
    print(magenta("═" * BREITE))
    text_ausgeben(SPICKZETTEL)
    weiter()


def begruessung():
    print()
    print(magenta("╔" + "═" * (BREITE - 2) + "╗"))
    print(magenta("║") + fett("  DAS GROSSE PYTHON-VORKURS-LERNQUIZ".ljust(BREITE - 2)) + magenta("║"))
    print(magenta("║") + "  Programmiervorkurs TU Darmstadt – alle Vorlesungen & Übungen".ljust(BREITE - 2) + magenta("║"))
    print(magenta("╚" + "═" * (BREITE - 2) + "╝"))


def anleitung():
    print()
    text_ausgeben(r"""
    ## So funktioniert das Quiz

      • Jedes Kapitel beginnt mit einer ERKLÄRUNG (lies sie in Ruhe!),
        danach kommen Fragen und Programmieraufgaben.
      • Fragearten: Multiple Choice, Wahr/Falsch, Antwort eintippen,
        "Was gibt der Code aus?", Python-Ausdrücke schreiben und echte
        Programmieraufgaben, die automatisch getestet werden.
      • ?      = Tipp anzeigen
      • x      = "weiß ich nicht" (zeigt die Lösung)
      • menü   = zurück zum Hauptmenü (auch Strg + C)
      • Dein Fortschritt wird automatisch gespeichert.
      • Falsche Fragen landen in der FEHLERKISTE zum Wiederholen.

    Empfehlung: Spiel die Kapitel der Reihe nach (Menüpunkt A),
    mach zum Schluss die Abschlussprüfung (P) – und probier jeden
    Code auch selbst in Python aus!
    """)
    weiter()


def hauptmenue():
    daten = fortschritt_laden()
    begruessung()
    if not daten["kapitel"]:
        anleitung()
    while True:
        print()
        print(blau("─" * BREITE))
        print("  " + fett("HAUPTMENÜ"))
        print(blau("─" * BREITE))
        for kap in KAPITEL:
            e = daten["kapitel"].get(str(kap.nummer))
            n = len(kap.fragen())
            if e:
                status = balken(e["best"], e["max"]) + f" {e['best']:>2}/{e['max']:<2}"
            else:
                status = grau("░" * 12 + f"  -/{n:<2}")
            print(f"  {kap.nummer:>2}) {status}  {kap.titel}")
        print()
        fk = len([i for i in daten["fehlerkiste"] if i in alle_fragen()])
        print(f"   {fett('A')}) Alle Kapitel der Reihe nach (ab dem ersten unbearbeiteten)")
        print(f"   {fett('P')}) Abschlussprüfung (30 Zufallsfragen aus allem)")
        print(f"   {fett('F')}) Fehlerkiste wiederholen ({fk} Fragen)")
        print(f"   {fett('S')}) Spickzettel anzeigen")
        print(f"   {fett('H')}) Hilfe / Anleitung")
        print(f"   {fett('R')}) Fortschritt zurücksetzen")
        print(f"   {fett('X')}) Beenden")
        try:
            wahl = input("\n  Deine Wahl: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            wahl = "x"
        try:
            if wahl.isdigit() and 1 <= int(wahl) <= len(KAPITEL):
                kapitel_spielen(KAPITEL[int(wahl) - 1], daten)
            elif wahl == "a":
                start = next((kap for kap in KAPITEL if str(kap.nummer) not in daten["kapitel"]),
                             KAPITEL[0])
                for kap in KAPITEL[start.nummer - 1:]:
                    kapitel_spielen(kap, daten)
                    if kap is not KAPITEL[-1]:
                        a = eingabe(f"\n  Weiter mit Kapitel {kap.nummer + 1}? (j/n): ")
                        if a.strip().lower() in ("n", "nein"):
                            break
            elif wahl == "p":
                pruefung(daten)
            elif wahl == "f":
                fehlerkiste(daten)
            elif wahl == "s":
                spickzettel_zeigen()
            elif wahl == "h":
                anleitung()
            elif wahl == "r":
                if eingabe("  Wirklich ALLES zurücksetzen? (ja/nein): ").strip().lower() == "ja":
                    daten = {"kapitel": {}, "fehlerkiste": [], "pruefungen": []}
                    fortschritt_speichern(daten)
                    print("  " + gruen("Fortschritt zurückgesetzt."))
            elif wahl in ("x", "q", "exit", "quit", "ende"):
                print("\n  " + fett("Bis bald – und viel Erfolg im Studium! 👋\n"))
                return
            else:
                print("  " + grau("Bitte eine Kapitelnummer oder einen der Buchstaben eingeben."))
        except ZurueckZumMenue:
            print("\n  " + grau("Zurück im Hauptmenü. (Dein Fortschritt ist gespeichert.)"))


# ════════════════════════════════════════════════════════════════════════════
#  TEIL 5: SELBSTTEST (prüft alle Musterlösungen)
# ════════════════════════════════════════════════════════════════════════════

def selbsttest():
    fehler = 0
    gesamt = 0
    for kap in KAPITEL:
        print(fett(f"\nKapitel {kap.nummer}: {kap.titel}"))
        for f in kap.fragen():
            gesamt += 1
            if isinstance(f, Ausgabe):
                ausgabe, fe = f.soll()
                print(f"  {f.id} Ausgabe  → {f.loesungstext()}")
            elif isinstance(f, MC):
                if len(set(f.optionen)) != len(f.optionen) or len(f.optionen) < 2:
                    print(rot(f"  {f.id} MC hat doppelte/zu wenige Optionen"))
                    fehler += 1
            elif isinstance(f, Ausdruck):
                ok, meldung = f.pruefen(f.loesung)
                print(f"  {f.id} Ausdruck {f.loesung} → {'ok' if ok else rot(meldung)}")
                fehler += not ok
            elif isinstance(f, CodeAufgabe):
                ok, meldung = f.alle_tests(f.loesung)
                print(f"  {f.id} Code     → {gruen('ok') if ok else rot(meldung)}")
                fehler += not ok
    print(fett(f"\n{gesamt} Fragen/Aufgaben in {len(KAPITEL)} Kapiteln, {fehler} Probleme."))
    return fehler


if __name__ == "__main__":
    if sys.version_info < (3, 10):
        print("Hinweis: Dieses Quiz braucht Python 3.10 oder neuer (wegen 'match').")
        print(f"Du hast Python {sys.version.split()[0]}. Bitte aktualisiere Python.")
        sys.exit(1)
    if "--selbsttest" in sys.argv:
        sys.exit(1 if selbsttest() else 0)
    hauptmenue()
