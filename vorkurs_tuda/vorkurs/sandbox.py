# -*- coding: utf-8 -*-
"""Führt Code in einem eigenen Python-Prozess aus: Programme, Tests, Tracer.

Alles läuft in einem leeren Temp-Ordner mit Zeitlimit. Die Datei des
Benutzercodes heißt dort immer DATEINAME (für Fehlerzeilen und den Tracer).
"""

import itertools
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import threading

DATEINAME = "dein_code.py"
ZEITLIMIT = 6                    # Sekunden pro Programmlauf
AUSGABE_LIMIT = 200_000          # Zeichen; danach wird das Programm gestoppt
_MAX_PROZESSE = threading.BoundedSemaphore(max(4, min(12, (os.cpu_count() or 4) * 2)))
_CREATIONFLAGS = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0


# ──────────────────────────────────────────────────────────────────────────
#  Startcode im Kindprozess
# ──────────────────────────────────────────────────────────────────────────

_START = r'''
import builtins as _b, os as _os, sys as _sys, traceback as _tb
_modus = _sys.argv[1]          # "1" = Eingabe anzeigen, "0" = wie python, "2" = ohne Aufforderung
_echo = _modus == "1"
_limit = int(_sys.argv[2])
class _Begrenzt:
    def __init__(self, ziel):
        self._ziel = ziel
        self._anzahl = 0
    def write(self, s):
        self._anzahl += len(s)
        if self._anzahl > _limit:
            self._ziel.write(s[:max(0, _limit - (self._anzahl - len(s)))] + "\n")
            self._ziel.flush()
            _sys.__stderr__.write("AusgabeZuLang: Dein Programm hat sehr viel ausgegeben "
                                  "(vermutlich eine Endlosschleife) und wurde gestoppt.\n")
            _sys.__stderr__.flush()
            _os._exit(3)
        return self._ziel.write(s)
    def __getattr__(self, name):
        return getattr(self._ziel, name)
_sys.stdout = _Begrenzt(_sys.stdout)
if _echo:
    def _input(prompt=""):
        _sys.stdout.write(str(prompt))
        _sys.stdout.flush()
        zeile = _sys.stdin.readline()
        if not zeile:
            raise EOFError("EOF when reading a line")
        zeile = zeile.rstrip("\r\n")
        _sys.stdout.write(zeile + "\n")
        return zeile
    _b.input = _input
elif _modus == "2":
    # Tests: Der Aufforderungstext von input("Zahl: ") landet NICHT in der geprüften Ausgabe
    def _input(prompt=""):
        _sys.stdout.flush()
        zeile = _sys.stdin.readline()
        if not zeile:
            raise EOFError("EOF when reading a line")
        return zeile.rstrip("\r\n")
    _b.input = _input
_sys.argv = ["''' + DATEINAME + r'''"]
with open("''' + DATEINAME + r'''", encoding="utf-8") as _f:
    _quelltext = _f.read()
_ns = {"__name__": "__main__", "__file__": "''' + DATEINAME + r'''", "__builtins__": _b}
try:
    _code = compile(_quelltext, "''' + DATEINAME + r'''", "exec")
except SyntaxError as _e:
    _tb.print_exception(type(_e), _e, None)
    _sys.exit(1)
try:
    exec(_code, _ns)
except SystemExit:
    raise
except BaseException as _e:
    _sys.stdout.flush()
    _tb.print_exception(type(_e), _e, _e.__traceback__.tb_next)
    _sys.exit(1)
'''


def programm_starten(quelltext, eingabe_text="", timeout=ZEITLIMIT, echo=False, aufforderung=True):
    """Startet Code in einem eigenen Python-Prozess (in einem leeren Ordner).

    Rückgabe: (returncode | None bei Zeitüberschreitung, stdout, stderr).
    echo=True: input() zeigt die Eingabe in der Ausgabe an (wie im Terminal).
    aufforderung=False (ohne echo): der Aufforderungstext von input("...") wird nicht
    ausgegeben – so laufen die Tests der Programmieraufgaben.
    """
    modus = "1" if echo else ("0" if aufforderung else "2")
    with _MAX_PROZESSE:
        tmp = tempfile.mkdtemp(prefix="vorkurs_quiz_")
        try:
            with open(os.path.join(tmp, DATEINAME), "w", encoding="utf-8") as f:
                f.write(quelltext)
            umgebung = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
            befehl = [sys.executable, "-X", "utf8", "-B", "-c", _START,
                      modus, str(AUSGABE_LIMIT)]
            try:
                r = subprocess.run(befehl, input=eingabe_text, capture_output=True, text=True,
                                   encoding="utf-8", errors="replace", timeout=timeout,
                                   cwd=tmp, env=umgebung, creationflags=_CREATIONFLAGS)
            except subprocess.TimeoutExpired:
                return None, "", "TIMEOUT"
            return r.returncode, r.stdout, r.stderr
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


def _skript_starten(skript, eingabe_text="", timeout=ZEITLIMIT, argumente=()):
    """Startet ein internes Hilfsskript (nicht den Benutzercode-Rahmen)."""
    with _MAX_PROZESSE:
        tmp = tempfile.mkdtemp(prefix="vorkurs_quiz_")
        try:
            umgebung = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
            try:
                r = subprocess.run([sys.executable, "-X", "utf8", "-B", "-c", skript, *argumente],
                                   input=eingabe_text, capture_output=True, text=True,
                                   encoding="utf-8", errors="replace", timeout=timeout,
                                   cwd=tmp, env=umgebung, creationflags=_CREATIONFLAGS)
            except subprocess.TimeoutExpired:
                return None, "", "TIMEOUT"
            return r.returncode, r.stdout, r.stderr
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


def _marker_lesen(ausgabe, marker):
    for zeile in reversed(ausgabe.splitlines()):
        if zeile.startswith(marker):
            return json.loads(zeile[len(marker):])
    return None


# ──────────────────────────────────────────────────────────────────────────
#  Fehlermeldungen auswerten und erklären
# ──────────────────────────────────────────────────────────────────────────

def fehler_zeile_finden(stderr, offset=0, anzahl_zeilen=None):
    """Letzte Zeilennummer im Benutzercode laut Traceback (relativ, ab 1)."""
    nummer = None
    for z in stderr.splitlines():
        m = re.search(re.escape(DATEINAME) + r'", line (\d+)', z)
        if m:
            nummer = int(m.group(1)) - offset
    if nummer is None or nummer < 1 or (anzahl_zeilen is not None and nummer > anzahl_zeilen):
        return None
    return nummer


def fehler_letzte_zeile(stderr):
    zeilen = [z for z in stderr.strip().splitlines() if z.strip()]
    return zeilen[-1].strip() if zeilen else ""


def fehlername(stderr):
    """'NameError' aus der letzten Traceback-Zeile (oder None)."""
    m = re.match(r"^([A-Za-z_][\w.]*)\s*(?::|$)", fehler_letzte_zeile(stderr))
    return m.group(1).split(".")[-1] if m else None


def fehler_kurz(stderr, offset, anzahl_zeilen):
    """Kurze Fehlermeldung wie in v1 (mit Zeilenangabe im Benutzercode)."""
    meldung = fehler_letzte_zeile(stderr) or "Unbekannter Fehler"
    nummer = fehler_zeile_finden(stderr, offset, anzahl_zeilen)
    if nummer:
        meldung += f"   (in deiner Zeile {nummer})"
    if "EOFError" in meldung:
        meldung += "\n      → Dein Programm wollte öfter input() aufrufen, als es Eingaben gab."
    return meldung


def _name_aus(meldung):
    m = re.search(r"'([^']*)'", meldung)
    return m.group(1) if m else "…"


def fehler_erklaeren(fehler):
    """Anfängerfreundliche Erklärung zu einer Fehlermeldung wie 'NameError: name 'x' ...'.

    Auch 'Timeout' und 'AusgabeZuLang' werden erklärt. Unbekanntes -> None.
    """
    if not fehler:
        return None
    typ, _, text = fehler.partition(":")
    typ = typ.strip().split(".")[-1]
    text = text.strip()
    if typ == "Timeout" or fehler.startswith("TIMEOUT"):
        return ("Dein Programm wurde nach einigen Sekunden gestoppt. Meistens ist das eine "
                "**Endlosschleife**: Die Bedingung einer `while`-Schleife wird nie falsch, z. B. "
                "weil du vergessen hast, die Zählvariable zu verändern (`i += 1`). Oder das "
                "Programm wartet auf mehr Eingaben, als es bekommt.")
    if typ == "AusgabeZuLang":
        return ("Dein Programm hat riesig viel ausgegeben und wurde gestoppt – vermutlich eine "
                "**Endlosschleife** mit `print()`. Prüfe, ob sich die Bedingung der Schleife "
                "irgendwann ändert.")
    if typ == "NameError":
        name = _name_aus(text)
        if name in ("true", "false", "none", "TRUE", "FALSE"):
            return (f"Python kennt `{name}` nicht. Die Werte heißen `True`, `False` und `None` – "
                    "mit großem Anfangsbuchstaben!")
        return (f"Python kennt den Namen `{name}` nicht. Häufige Ursachen: ein **Tippfehler** oder "
                "falsche Groß-/Kleinschreibung (`Alter` ist nicht `alter`), die Variable wird erst "
                "**später** angelegt als benutzt, oder bei einem Text fehlen die "
                f"**Anführungszeichen** (`print({name})` statt `print(\"{name}\")`).")
    if typ == "UnboundLocalError":
        name = _name_aus(text)
        return (f"In einer Funktion wird `{name}` benutzt, bevor es dort einen Wert bekommt. "
                f"Weil du `{name}` in der Funktion **zuweist**, hält Python es für eine lokale "
                "Variable. Übergib den Wert lieber als Parameter und gib das Ergebnis mit "
                f"`return` zurück (oder – selten sinnvoll – `global {name}`).")
    if typ == "TypeError":
        if "can only concatenate str" in text or ("unsupported operand" in text and "'str'" in text):
            return ("Du versuchst, **Text und Zahl** mit einem Rechenzeichen zu verbinden – das geht "
                    "nicht. Zum Zusammensetzen: Zahl mit `str(zahl)` umwandeln oder einen f-String "
                    "nutzen: `f\"Alter: {alter}\"`. Zum Rechnen: Text mit `int(...)` oder "
                    "`float(...)` in eine Zahl umwandeln (Achtung: `input()` liefert immer Text!).")
        if "unsupported operand" in text and "NoneType" in text:
            return ("Ein Wert ist `None` – oft, weil eine Funktion kein `return` hat und deshalb "
                    "`None` zurückgibt.")
        if "not supported between instances" in text:
            return ("Du vergleichst zwei Werte, die man nicht vergleichen kann, z. B. Text mit Zahl "
                    "(`\"5\" < 3`). Wandle die Eingabe zuerst mit `int(...)` um.")
        if "object is not callable" in text:
            return ("Hinter einem Wert stehen runde Klammern `( )`, als wäre er eine Funktion. "
                    "Fehlt ein `*` (z. B. `2(3+4)` statt `2*(3+4)`)? Oder hast du einen "
                    "Funktionsnamen als Variable benutzt (z. B. `print = 5` oder `sum = 0`)?")
        if "not subscriptable" in text:
            return ("Du benutzt eckige Klammern `[ ]` bei einem Wert, der keine Elemente hat "
                    "(z. B. bei einer Zahl oder bei `None`). Prüfe, welchen Typ der Wert hat.")
        if "does not support item assignment" in text:
            return ("Dieser Wert ist **unveränderlich** (Strings und Tupel). Du kannst nicht einzelne "
                    "Zeichen/Elemente ersetzen – baue stattdessen einen neuen Wert, z. B. mit "
                    "`s.replace(...)` oder Slicing.")
        if "missing" in text and "required positional argument" in text:
            return ("Du hast eine Funktion mit **zu wenigen Argumenten** aufgerufen. Zähle die "
                    "Parameter in der `def`-Zeile und die Werte im Aufruf.")
        if "positional argument" in text and "were given" in text:
            return ("Du hast eine Funktion mit **zu vielen Argumenten** aufgerufen. Zähle die "
                    "Parameter in der `def`-Zeile und die Werte im Aufruf.")
        if "has no len()" in text:
            return "`len()` funktioniert nur bei Strings, Listen, Tupeln, Dictionaries – nicht bei Zahlen."
        if "NoneType" in text:
            return ("Ein Wert ist `None`. Häufige Ursache: Eine Funktion ohne `return`, oder "
                    "`lst = lst.sort()` (sort() ändert die Liste und gibt `None` zurück).")
        if "object is not iterable" in text:
            return ("Du willst mit `for` über einen Wert laufen, der keine Elemente hat (z. B. eine "
                    "Zahl). Für Zahlenbereiche: `for i in range(n):`.")
        if "indices must be integers" in text:
            return ("Ein Index muss eine **ganze Zahl** sein. Kommt der Index aus `input()`, wandle "
                    "ihn mit `int(...)` um; bei `/` entsteht ein float – nimm `//`.")
        return ("Ein Wert hat den **falschen Typ** für diese Operation. Prüfe mit `type(x)`, was "
                "in deinen Variablen steckt.")
    if typ == "ValueError":
        if "invalid literal for int()" in text:
            return (f"`int()` kann nur Text umwandeln, der eine **ganze Zahl** ist. {text.split(':')[-1].strip()} "
                    "ist keine. Für Kommazahlen nimm `float(...)` (mit Punkt: `3.5`).")
        if "could not convert string to float" in text:
            return ("`float()` kann diesen Text nicht in eine Zahl umwandeln. Achtung: Python "
                    "schreibt Kommazahlen mit **Punkt** (`3.5`, nicht `3,5`).")
        if "too many values to unpack" in text or "not enough values to unpack" in text:
            return ("Beim Auspacken (z. B. `a, b = ...`) passt die Anzahl der Variablen links nicht "
                    "zur Anzahl der Werte rechts.")
        if "not in list" in text:
            return "Den gesuchten Wert gibt es nicht in der Liste. Prüfe vorher mit `if x in liste:`."
        return "Der Typ stimmt, aber der **Wert** passt nicht zu dieser Operation."
    if typ == "IndexError":
        if "pop from empty" in text:
            return "Du willst etwas aus einer **leeren** Liste entfernen. Prüfe vorher mit `if liste:`."
        return ("Der **Index ist zu groß** (oder zu klein). Bei einer Liste mit `n` Elementen sind "
                "nur die Indizes `0` bis `n - 1` erlaubt (bzw. `-1` bis `-n`). Häufig: "
                "`range(len(lst) + 1)` oder `lst[len(lst)]`.")
    if typ == "KeyError":
        return (f"Den Schlüssel {text or '…'} gibt es im Dictionary nicht. Prüfe vorher mit "
                "`if schluessel in d:` oder nutze `d.get(schluessel, standardwert)`.")
    if typ == "ZeroDivisionError":
        return ("Du teilst durch **0** – das geht auch in Python nicht. Prüfe vorher, ob der "
                "Teiler 0 ist (auch bei `//` und `%`).")
    if typ in ("IndentationError", "TabError"):
        if "expected an indented block" in text:
            return ("Nach einer Zeile mit Doppelpunkt (`if`, `else`, `for`, `while`, `def`, …) "
                    "muss mindestens eine **eingerückte** Zeile folgen (4 Leerzeichen).")
        if "unexpected indent" in text:
            return ("Diese Zeile ist **eingerückt, obwohl sie es nicht sein darf**. Nur nach einer "
                    "Zeile mit Doppelpunkt wird eingerückt.")
        if "unindent does not match" in text:
            return ("Die Einrückung passt zu keiner Ebene darüber. Nutze immer genau **4 Leerzeichen** "
                    "pro Ebene.")
        if typ == "TabError" or "tabs" in text:
            return "Du hast Tabs und Leerzeichen gemischt. Nutze nur Leerzeichen (4 pro Ebene)."
        return "Die **Einrückung** stimmt nicht. Python nutzt Einrückung (4 Leerzeichen), um Blöcke zu bilden."
    if typ == "SyntaxError":
        if "expected ':'" in text:
            return ("Am Ende der Zeile fehlt ein **Doppelpunkt** `:`. Nach `if`, `elif`, `else`, "
                    "`while`, `for` und `def` steht immer ein Doppelpunkt.")
        if "Maybe you meant '==' " in text or "Maybe you meant '=='" in text:
            return ("`=` ist eine **Zuweisung**. Zum Vergleichen brauchst du `==` "
                    "(z. B. `if x == 5:`).")
        if "unterminated string" in text or "EOL while scanning" in text or "unterminated triple" in text:
            return "Ein Text ist nicht abgeschlossen – es fehlt ein **Anführungszeichen** am Ende."
        if "was never closed" in text or "unexpected EOF" in text:
            return "Eine **Klammer** wurde geöffnet, aber nie geschlossen. Zähle `(` und `)`."
        if "unmatched" in text or "does not match opening parenthesis" in text:
            return "Hier steht eine **schließende Klammer zu viel** (oder die falsche Art von Klammer)."
        if "invalid character" in text:
            return ("Im Code steht ein Zeichen, das Python nicht kennt – oft typografische "
                    "Anführungszeichen „ “ oder ein langer Gedankenstrich –. Nutze \" und -.")
        if "Missing parentheses in call to 'print'" in text:
            return "In Python 3 braucht `print` runde Klammern: `print(\"Hallo\")`."
        if "invalid decimal literal" in text:
            return ("Eine Zahl und Buchstaben kleben zusammen. Variablennamen dürfen nicht mit einer "
                    "Ziffer beginnen, und zwischen Zahl und Variable fehlt evtl. ein `*`.")
        if "cannot assign to" in text:
            return ("Links vom `=` muss ein **Variablenname** stehen. Vergleichen geht mit `==`.")
        if "'return' outside function" in text:
            return "`return` darf nur innerhalb einer Funktion (`def`) stehen."
        if "'break' outside loop" in text or "'continue' not properly in loop" in text:
            return "`break` und `continue` dürfen nur innerhalb einer Schleife stehen."
        return ("Python versteht die **Grammatik** dieser Zeile nicht. Prüfe Doppelpunkte, Klammern, "
                "Anführungszeichen und Kommas – oft liegt der Fehler auch in der Zeile davor.")
    if typ == "RecursionError":
        return ("Die Funktion ruft sich **endlos selbst auf**. Fehlt der **Rekursionsanker** (der Fall, "
                "in dem die Funktion ohne Selbstaufruf zurückkehrt)? Oder wird das Problem beim "
                "Selbstaufruf nicht kleiner (z. B. `n - 1`)?")
    if typ == "EOFError":
        return ("Dein Programm ruft `input()` öfter auf, als es Eingaben gibt. Prüfe die Anzahl der "
                "`input()`-Aufrufe (und trage beim Ausführen genug Eingaben ein).")
    if typ == "AttributeError":
        if "'NoneType'" in text:
            return ("Ein Wert ist `None`. Häufig: `lst = lst.sort()` oder `lst = lst.append(x)` – "
                    "diese Methoden ändern die Liste direkt und geben `None` zurück.")
        m = re.search(r"'(\w+)' object has no attribute '(\w+)'", text)
        if m:
            return (f"Ein Wert vom Typ `{m.group(1)}` hat keine Methode `{m.group(2)}`. Tippfehler? "
                    "Oder hat die Variable einen anderen Typ als gedacht (z. B. `str` statt `list`)?")
        return "Diese Methode/dieses Attribut gibt es für den Wert nicht. Tippfehler oder falscher Typ?"
    if typ == "FileNotFoundError":
        return ("Die Datei gibt es nicht. Stimmen Name und Endung (`.txt`)? Liegt sie im selben Ordner "
                "wie das Programm? Zum Neu-Anlegen öffnet man mit Modus `'w'`.")
    if typ in ("ModuleNotFoundError", "ImportError"):
        return ("Dieses Modul gibt es nicht (Tippfehler?). Im Vorkurs brauchst du nur Module der "
                "Standardbibliothek wie `math` oder `random`.")
    if typ == "KeyboardInterrupt":
        return "Das Programm wurde abgebrochen."
    return None


# ──────────────────────────────────────────────────────────────────────────
#  Code einfach ausführen (Button "Ausführen")
# ──────────────────────────────────────────────────────────────────────────

def _stderr_saeubern(stderr):
    return stderr.replace("AusgabeZuLang: ", "").rstrip()


def ausfuehren(code, eingaben=(), timeout=ZEITLIMIT):
    """Führt Benutzercode aus. input() bekommt die Eingaben und zeigt sie an.

    Rückgabe: {"stdout", "stderr", "fehler", "fehler_zeile", "timeout", "fehler_erklaert"}
    """
    code = (code or "").expandtabs(4)
    eingabe_text = "".join(str(e) + "\n" for e in (eingaben or []))
    rc, out, err = programm_starten(code, eingabe_text, timeout=timeout, echo=True)
    if rc is None:
        return {"stdout": out, "stderr": "", "fehler": "Timeout: Zeitlimit überschritten",
                "fehler_zeile": None, "timeout": True,
                "fehler_erklaert": fehler_erklaeren("Timeout")}
    fehler = None
    zeile = None
    if rc != 0:
        letzte = fehler_letzte_zeile(err)
        fehler = letzte or f"Programm endete mit Code {rc}"
        zeile = fehler_zeile_finden(err, 0, len(code.splitlines()) or None)
    return {"stdout": out, "stderr": _stderr_saeubern(err), "fehler": fehler,
            "fehler_zeile": zeile, "timeout": False,
            "fehler_erklaert": fehler_erklaeren(fehler) if fehler else None}


def beispiel_ausfuehren(code, timeout=ZEITLIMIT):
    """Für 'Was gibt der Code aus?': (ausgabe ohne letztes \\n, fehlername|None).

    Bei Zeitüberschreitung ist der Fehlername 'Timeout'.
    """
    rc, out, err = programm_starten(code, "", timeout=timeout)
    if rc is None:
        return "", "Timeout"
    fehler = None
    if rc != 0:
        fehler = fehlername(err) or "Fehler"
    return out.rstrip("\n"), fehler


# ──────────────────────────────────────────────────────────────────────────
#  Tests für Programmieraufgaben (Logik aus v1)
# ──────────────────────────────────────────────────────────────────────────

_AUS_LOESUNG = object()


class Test:
    """Ein Testfall für eine Programmieraufgabe.
       eingaben       : Liste von Texten, die das Programm per input() bekommt
       erwartet       : Texte, mit denen eine Ausgabezeile ENDEN muss. Ein Element darf
                        ein Tupel sein: dann reicht EINE der Alternativen.
       nicht          : Texte, die in keiner Ausgabezeile vorkommen dürfen (Groß/klein egal)
       exakt          : Liste der Zeilen, die genau so ausgegeben werden müssen (streng)
       anzahl         : {text: n} – text muss genau n-mal in der Ausgabe vorkommen
       streng         : None = Vorgabe der Aufgabe; True = auch `erwartet`/`anzahl`
                        beachten Groß/klein und Satzzeichen; False = auch `exakt` tolerant
       leerzeichen    : True = führende Leerzeichen (Einrückung) zählen bei `exakt`
       mit_aufforderung: True = der Aufforderungstext von input("...") steht in der geprüften
                        Ausgabe (Standard False: er wird weggelassen)
       vorspann       : Code, der VOR dem Benutzercode ausgeführt wird
       nachspann      : Code, der NACH dem Benutzercode ausgeführt wird (Prüfung)
       aufruf / soll  : Funktionstest – aufruf muss soll liefern"""

    def __init__(self, eingaben=(), erwartet=(), nicht=(), exakt=None, vorspann="",
                 nachspann="", aufruf=None, soll=_AUS_LOESUNG, beschreibung=None,
                 streng=None, anzahl=None, leerzeichen=False, mit_aufforderung=False):
        if isinstance(eingaben, str):
            eingaben = [eingaben]
        if isinstance(erwartet, str):
            erwartet = [erwartet]
        if isinstance(nicht, str):
            nicht = [nicht]
        self.eingaben = [str(e) for e in eingaben]
        self.erwartet = [tuple(str(a) for a in e) if isinstance(e, (tuple, list)) else str(e)
                         for e in erwartet]
        self.nicht = [str(n) for n in nicht]
        self.exakt = None if exakt is None else [str(z) for z in exakt]
        self.anzahl = {str(k): int(v) for k, v in (anzahl or {}).items()}
        self.streng = streng
        self.leerzeichen = bool(leerzeichen)
        self.mit_aufforderung = bool(mit_aufforderung)
        self.vorspann = textwrap.dedent(vorspann).strip("\n")
        self.nachspann = textwrap.dedent(nachspann).strip("\n")
        self.aufruf = aufruf
        self.soll = soll
        self.beschreibung = beschreibung

    def name(self):
        if self.beschreibung:
            return self.beschreibung
        if self.aufruf:
            return self.aufruf
        if self.eingaben:
            return "Eingaben: " + ", ".join(self.eingaben)
        return None


def P(eingaben=(), erwartet=(), nicht=(), exakt=None, vorspann="", nachspann="", beschreibung=None,
      streng=None, anzahl=None, leerzeichen=False, mit_aufforderung=False):
    """Test für ein ganzes Programm (mit Eingaben und erwarteter Ausgabe).

    erwartet: Texte, mit denen eine Zeile endet (Tupel-Element = Alternativen).
    exakt:    genaue Zeilenliste – STRENG (Groß/klein, Satzzeichen, Leerzeichen im Text).
    streng:   True macht auch `erwartet`/`anzahl` streng; False macht `exakt` tolerant.
    anzahl:   {"Falsch!": 3} – Text muss genau so oft vorkommen.
    leerzeichen: True – bei `exakt` zählen auch führende Leerzeichen (Einrückung).
    mit_aufforderung: True – der Aufforderungstext von input("Zahl: ") bleibt in der geprüften
                 Ausgabe. Standard: Er wird weggelassen (er klebt sonst an der nächsten Zeile).
    """
    return Test(eingaben, erwartet, nicht, exakt, vorspann, nachspann, beschreibung=beschreibung,
                streng=streng, anzahl=anzahl, leerzeichen=leerzeichen,
                mit_aufforderung=mit_aufforderung)


def F(aufruf, soll=_AUS_LOESUNG, vorspann="", beschreibung=None):
    """Test für eine Funktion: aufruf (z.B. 'fakultaet(5)') muss soll ergeben.
       Ohne soll wird der richtige Wert aus der Musterlösung berechnet.
       beschreibung wird (statt des Aufrufs) als Testname angezeigt."""
    return Test(vorspann=vorspann, aufruf=aufruf, soll=soll, beschreibung=beschreibung)


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

_WERTE_SKRIPT = r'''
import contextlib, io, json, sys
_daten = json.loads(sys.stdin.read())
_erg = []
for _a in _daten["aufgaben"]:
    _ns = {"__name__": "__loesung__"}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            if _a["vorspann"]:
                exec(_a["vorspann"], _ns)
            exec(_daten["loesung"], _ns)
            _wert = eval(_a["aufruf"], _ns)
        _erg.append({"ok": True, "repr": repr(_wert)})
    except BaseException as _e:
        _erg.append({"ok": False, "fehler": type(_e).__name__ + ": " + str(_e)})
print("@@WERTE@@" + json.dumps(_erg))
'''

_LOESUNGSWERTE = {}
_LOESUNGSWERTE_LOCK = threading.Lock()


class LoesungsFehler(Exception):
    """Die Musterlösung selbst liefert für einen Funktionstest keinen Wert."""


def loesungswerte_berechnen(loesung, tests):
    """Berechnet (in EINEM Kindprozess) die Sollwerte aller F-Tests ohne soll."""
    loesung = textwrap.dedent(loesung)
    offen = []
    for t in tests:
        if t.aufruf and t.soll is _AUS_LOESUNG:
            schluessel = (loesung, t.vorspann, t.aufruf)
            with _LOESUNGSWERTE_LOCK:
                if schluessel not in _LOESUNGSWERTE and schluessel not in offen:
                    offen.append(schluessel)
    if not offen:
        return
    daten = {"loesung": loesung,
             "aufgaben": [{"vorspann": v, "aufruf": a} for (_, v, a) in offen]}
    rc, out, err = _skript_starten(_WERTE_SKRIPT, json.dumps(daten), timeout=20)
    werte = _marker_lesen(out, "@@WERTE@@") if rc is not None else None
    if werte is None:
        raise LoesungsFehler("Die Musterlösung konnte nicht ausgeführt werden: "
                             + (fehler_letzte_zeile(err) or "Zeitüberschreitung"))
    with _LOESUNGSWERTE_LOCK:
        for schluessel, wert in zip(offen, werte):
            _LOESUNGSWERTE[schluessel] = wert


def loesungswert_repr(loesung, t):
    """repr() des erwarteten Rückgabewerts eines Funktionstests."""
    if t.soll is not _AUS_LOESUNG:
        return repr(t.soll)
    schluessel = (textwrap.dedent(loesung), t.vorspann, t.aufruf)
    with _LOESUNGSWERTE_LOCK:
        wert = _LOESUNGSWERTE.get(schluessel)
    if wert is None:
        loesungswerte_berechnen(loesung, [t])
        with _LOESUNGSWERTE_LOCK:
            wert = _LOESUNGSWERTE[schluessel]
    if not wert["ok"]:
        raise LoesungsFehler(f"Musterlösung scheitert bei {t.aufruf}: {wert['fehler']}")
    return wert["repr"]


def _norm_zeile(z):
    """Tolerante Form einer Zeile: Groß/klein, Leerzeichen und Satzzeichen am Ende egal."""
    z = re.sub(r"\s+", " ", z.strip().lower())
    return z.rstrip(" .!?:")


def _norm_streng(z):
    """Strenge Form für `erwartet`: nur Leerzeichen außen und mehrfache Leerzeichen egal."""
    return re.sub(r"\s+", " ", z.strip())


def _norm_nicht(z):
    """Form für `nicht`: Groß/klein und mehrfache Leerzeichen egal, Satzzeichen zählen."""
    return re.sub(r"\s+", " ", z.strip().lower())


def _endet_mit(zeile, erwartet):
    if zeile == erwartet:
        return True
    if erwartet and zeile.endswith(erwartet):
        vorher = zeile[-len(erwartet) - 1]
        return not (vorher.isalnum() or vorher in ".-_")
    return False


# Satzzeichen für den "Fast!"-Vergleich (Punkt/Komma zwischen Ziffern zählen nicht dazu)
_SATZZEICHEN_RE = re.compile(r"(?<!\d)[.,]|[.,](?!\d)|[;:!?'\"„“”‚‘’«»…]")


def _lose(s):
    """Sehr grobe Form: ohne Groß/klein, Leerzeichen und Satzzeichen."""
    return re.sub(r"\s+", "", _SATZZEICHEN_RE.sub("", s.lower()))


def _unterschied_art(soll, ist):
    """Worin unterscheiden sich zwei fast gleiche Texte? z. B. 'Satzzeichen'."""
    arten = [("Groß-/Kleinschreibung", str.lower),
             ("Satzzeichen", lambda s: _SATZZEICHEN_RE.sub("", s)),
             ("Leerzeichen", lambda s: re.sub(r"\s+", "", s))]
    for n in (1, 2, 3):
        for auswahl in itertools.combinations(arten, n):
            a, b = soll, ist
            for _, f in auswahl:
                a, b = f(a), f(b)
            if a == b:
                namen = [name for name, _ in auswahl]
                return namen[0] if n == 1 else ", ".join(namen[:-1]) + " und " + namen[-1]
    return "Groß-/Kleinschreibung, Satzzeichen oder Leerzeichen"


def _fast_meldung(soll, ist):
    return (f"Fast! Deine Ausgabe unterscheidet sich nur in {_unterschied_art(soll, ist)}: "
            f"erwartet „{soll}“ – deine Ausgabe „{ist}“.")


def _ohne_leere_raender(zeilen):
    zeilen = list(zeilen)
    while zeilen and not zeilen[0].strip():
        zeilen.pop(0)
    while zeilen and not zeilen[-1].strip():
        zeilen.pop()
    return zeilen


def _fast_erwartet(roh_zeilen, alternativen):
    """Sucht eine Zeile, die bis auf Groß/klein, Satzzeichen und Leerzeichen passt.
       Rückgabe: Fast-Meldung oder None."""
    for alt in alternativen:
        ziel = _lose(alt)
        if not ziel:
            continue
        for z in roh_zeilen:
            z = z.strip()
            if not _lose(z).endswith(ziel):
                continue
            # kürzestes Ende der Zeile, das grob passt (von hinten; _lose wächst monoton)
            for i in range(len(z) - 1, -1, -1):
                ende = _lose(z[i:])
                if len(ende) > len(ziel):
                    break
                if ende == ziel:
                    vorher_ok = i == 0 or not (z[i - 1].isalnum() or z[i - 1] in ".-_")
                    if vorher_ok and z[i:].strip() != alt.strip():
                        return _fast_meldung(alt.strip(), z[i:].strip())
                    break
    return None


def _als_text(e):
    """Erwarteter Text; bei Alternativen 'A (oder: B) (oder: C)'."""
    if isinstance(e, tuple):
        return e[0] + "".join(f" (oder: {x})" for x in e[1:])
    return e


def _erwartet_text(t, soll_repr=None):
    if t.aufruf:
        return f"{t.aufruf} → {soll_repr}"
    teile = []
    if t.exakt is not None:
        teile.append("Genau diese Zeilen:\n" + ("\n".join(t.exakt) if t.exakt else "(keine Ausgabe)"))
    for e in t.erwartet:
        teile.append(f"Eine Zeile endet mit: {_als_text(e)}")
    for text, n in t.anzahl.items():
        teile.append(f"Genau {n}-mal in der Ausgabe: {text}")
    for n in t.nicht:
        teile.append(f"Nicht in der Ausgabe: {n}")
    return "\n".join(teile)


def _ausgabe_pruefen(t, out, streng_vorgabe=False):
    """Vergleicht die Ausgabe mit exakt/erwartet/anzahl/nicht.

    Rückgabe: None (alles passt) oder (lange Meldung ohne Ausgabe, kurze Meldung, fast: bool).
    """
    streng = t.streng if t.streng is not None else bool(streng_vorgabe)
    roh = out.splitlines()
    if t.exakt is not None:
        if t.streng is False:                           # ausdrücklich tolerant (wie v1)
            ist = [_norm_zeile(z) for z in roh if z.strip()]
            soll = [_norm_zeile(z) for z in t.exakt if z.strip()]
        else:
            form = (lambda z: z.rstrip()) if t.leerzeichen else (lambda z: z.strip())
            ist = [form(z) for z in _ohne_leere_raender(roh)]
            soll = [form(z) for z in _ohne_leere_raender(t.exakt)]
        if ist != soll:
            lang = ("   Erwartet wurden genau diese Zeilen:\n" +
                    "\n".join("      │ " + z for z in t.exakt))
            kurz = "Die Ausgabe stimmt nicht genau mit den erwarteten Zeilen überein."
            ist_v = [z for z in ist if z.strip()]
            soll_v = [z for z in soll if z.strip()]
            if len(ist_v) == len(soll_v) and all(_lose(a) == _lose(b) for a, b in zip(ist_v, soll_v)):
                paare = [(s, i) for s, i in zip(soll_v, ist_v) if s != i]
                if paare:
                    s, i = paare[0]
                    if s.strip() == i.strip():
                        fast = (f"Fast! Nur die Einrückung stimmt nicht: erwartet „{s}“ – deine "
                                f"Ausgabe „{i}“ (achte auf die Leerzeichen am Zeilenanfang).")
                    else:
                        fast = _fast_meldung(s.strip(), i.strip())
                else:
                    fast = ("Fast! Der Text stimmt, aber deine Ausgabe hat zusätzliche oder "
                            "fehlende Leerzeilen.")
                return f"   {fast}\n" + lang, fast, True
            return lang, kurz, False
    if streng:
        zeilen = [_norm_streng(z) for z in roh if z.strip()]
        form = _norm_streng
    else:
        zeilen = [_norm_zeile(z) for z in roh if z.strip()]
        form = _norm_zeile
    if streng and t.leerzeichen:
        zeilen = [z.rstrip() for z in roh if z.strip()]
        form = str.rstrip
    for e in t.erwartet:
        alternativen = e if isinstance(e, tuple) else (e,)
        if not any(_endet_mit(z, form(a)) for a in alternativen for z in zeilen):
            text = _als_text(e)
            lang = f"   Erwartet wurde eine Zeile, die mit \"{text}\" endet."
            fast = _fast_erwartet(roh, alternativen)
            if fast:
                return f"   {fast}\n" + lang, fast, True
            return lang, f"Erwartet wurde eine Zeile, die mit \"{text}\" endet.", False
    for text, soll_n in t.anzahl.items():
        if streng:
            muster, liste = _norm_streng(text), [_norm_streng(z) for z in roh]
        else:
            muster = _norm_zeile(text) or _norm_nicht(text)
            liste = [_norm_nicht(z) for z in roh]
        ist_n = sum(z.count(muster) for z in liste) if muster else 0
        if ist_n != soll_n:
            kurz = f"\"{text}\" sollte genau {soll_n}-mal ausgegeben werden, bei dir {ist_n}-mal."
            if streng:
                lose_n = sum(_lose(z).count(_lose(text)) for z in roh) if _lose(text) else 0
                if lose_n == soll_n:
                    kurz = (f"Fast! \"{text}\" kommt richtig oft vor, unterscheidet sich aber in "
                            f"Groß-/Kleinschreibung, Satzzeichen oder Leerzeichen.")
                    return "   " + kurz, kurz, True
            return "   " + kurz, kurz, False
    zeilen_nicht = [_norm_nicht(z) for z in roh if z.strip()]
    for n in t.nicht:
        muster = _norm_nicht(n)
        if muster and any(muster in z for z in zeilen_nicht):
            kurz = f"\"{n}\" hätte hier NICHT ausgegeben werden dürfen."
            return "   " + kurz, kurz, False
    return None


def test_ausfuehren(nutzercode, t, loesung, timeout=ZEITLIMIT, streng=False):
    """Führt einen Test aus. Rückgabe: (bestanden, meldung, details_dict).

    meldung ist ausführlich (wie v1, für das Terminal); details_dict enthält
    {"name", "ok", "meldung" (kurz), "eingaben", "erwartet", "ausgabe", "fehler", "fast"}.
    streng: Vorgabe der Aufgabe für `erwartet`/`anzahl` (siehe Test.streng).
    """
    details = {"name": t.name(), "ok": False, "meldung": "", "eingaben": list(t.eingaben),
               "erwartet": "", "ausgabe": "", "fehler": None, "fast": False}
    nachspann = t.nachspann
    soll_repr = None
    if t.aufruf:
        soll_repr = loesungswert_repr(loesung, t)
        nachspann = _HARNESS.replace("__AUFRUF__", t.aufruf).replace("__SOLL__", soll_repr)
    details["erwartet"] = _erwartet_text(t, soll_repr)
    teile = [x for x in (t.vorspann, nutzercode, nachspann) if x]
    offset = len(t.vorspann.splitlines()) if t.vorspann else 0
    eingabe_text = "\n".join(t.eingaben) + "\n" if t.eingaben else ""
    code, out, err = programm_starten("\n".join(teile) + "\n", eingabe_text, timeout=timeout,
                                      aufforderung=t.mit_aufforderung)

    def fertig(ok, meldung, kurz=None):
        details["ok"] = ok
        details["meldung"] = kurz if kurz is not None else meldung.strip()
        return ok, meldung, details

    if code is None:
        details["fehler"] = "Timeout"
        return fertig(False, f"Dein Programm lief länger als {timeout} Sekunden – "
                             "vermutlich eine Endlosschleife!")
    # Ausgabe des Benutzers (ohne die Zeilen der Testmaschine)
    sichtbar = out.split("@@")[0] if t.aufruf else out
    if t.aufruf and sichtbar.endswith("\n\n"):
        sichtbar = sichtbar[:-1]
    details["ausgabe"] = sichtbar.rstrip("\n")
    fehler = fehler_kurz(err, offset, len(nutzercode.splitlines())) if code != 0 else ""
    if code != 0:
        details["fehler"] = fehler_letzte_zeile(err)

    if t.aufruf:
        if "@@OK@@" in out:
            ist = out.split("@@OK@@")[-1].strip().splitlines()[0]
            details["ausgabe"] = ist
            return fertig(True, "")
        if "@@FALSCH@@" in out:
            ist = out.split("@@FALSCH@@")[-1].strip().splitlines()[0]
            details["ausgabe"] = ist
            return fertig(False, f"{t.aufruf} sollte {soll_repr} liefern – dein Ergebnis: {ist}")
        if "@@FEHLER@@" in out:
            meldung = out.split("@@FEHLER@@")[-1].strip().splitlines()[0]
            details["fehler"] = meldung
            details["ausgabe"] = meldung
            return fertig(False, f"Beim Aufruf {t.aufruf} gab es einen Fehler: {meldung}")
        return fertig(False, f"Dein Code ist abgestürzt, bevor getestet werden konnte:\n      {fehler}",
                      f"Dein Code ist abgestürzt, bevor getestet werden konnte: {fehler}")

    if code != 0:
        return fertig(False, f"Dein Programm ist mit einem Fehler abgestürzt:\n      {fehler}",
                      f"Dein Programm ist mit einem Fehler abgestürzt: {fehler}")
    ausgabe_kurz = "\n".join("      │ " + z for z in out.strip("\n").splitlines()[:15]) or "      │ (nichts)"
    info = ""
    if t.eingaben:
        info = f"   Eingaben: {', '.join(t.eingaben)}\n"
    if t.beschreibung:
        info = f"   Test: {t.beschreibung}\n" + info
    problem = _ausgabe_pruefen(t, out, streng)
    if problem is None:
        return fertig(True, "")
    lang, kurz, fast = problem
    details["fast"] = fast
    return fertig(False, info + lang + "\n   Deine Ausgabe war:\n" + ausgabe_kurz, kurz)


# ──────────────────────────────────────────────────────────────────────────
#  Ausdrücke prüfen (Fragetyp "ausdruck")
# ──────────────────────────────────────────────────────────────────────────

_AUSDRUCK_SKRIPT = r'''
import copy, json, sys
_d = json.loads(sys.stdin.read())
_tests = eval(_d["tests"])
_erg = []
for _v in _tests:
    _soll = eval(_d["loesung"], {"__builtins__": __builtins__}, copy.deepcopy(_v))
    try:
        _ist = eval(_d["antwort"], {"__builtins__": __builtins__}, copy.deepcopy(_v))
    except BaseException as _e:
        _erg.append({"ok": False, "fehler": type(_e).__name__ + ": " + str(_e)})
        continue
    _erg.append({"ok": _ist == _soll and type(_ist) == type(_soll),
                 "ist": repr(_ist), "soll": repr(_soll)})
print("@@AUSDRUCK@@" + json.dumps(_erg))
'''


def ausdruck_auswerten(antwort, loesung, tests, timeout=4):
    """Wertet einen Benutzer-Ausdruck für alle Variablenbelegungen aus.

    Rückgabe: Liste von {"ok", "ist", "soll"} oder {"ok": False, "fehler"};
    None bei Zeitüberschreitung.
    """
    daten = {"tests": repr(list(tests)), "loesung": loesung, "antwort": antwort}
    rc, out, err = _skript_starten(_AUSDRUCK_SKRIPT, json.dumps(daten), timeout=timeout)
    if rc is None:
        return None
    erg = _marker_lesen(out, "@@AUSDRUCK@@")
    if erg is None:
        return [{"ok": False, "fehler": fehler_letzte_zeile(err) or "Unbekannter Fehler"}]
    return erg


# ──────────────────────────────────────────────────────────────────────────
#  Tracer: Schritt-für-Schritt-Ausführung
# ──────────────────────────────────────────────────────────────────────────

_TRACE_SKRIPT = r'''
import builtins as _b, io as _io, json as _json, os as _os, sys as _sys, types as _types
_DATEI = "''' + DATEINAME + r'''"
_MAX = int(_sys.argv[1])
_eingaben = _json.loads(_sys.stdin.read())
_echt = _sys.stdout
_puffer = []
_laenge = [0]
_AUSGABE_MAX = 20000

class _Aus:
    encoding = "utf-8"
    def write(self, s):
        s = str(s)
        if _laenge[0] < _AUSGABE_MAX:
            _puffer.append(s[:_AUSGABE_MAX - _laenge[0]])
            if _laenge[0] + len(s) >= _AUSGABE_MAX:
                _puffer.append("\n… (Ausgabe gekürzt)\n")
        _laenge[0] += len(s)
        return len(s)
    def flush(self):
        pass
    def isatty(self):
        return False

def _input(prompt=""):
    _sys.stdout.write(str(prompt))
    if not _eingaben:
        raise EOFError("EOF when reading a line")
    w = str(_eingaben.pop(0))
    _sys.stdout.write(w + "\n")
    return w

_ids = {}
_halten = []

def _id(o):
    k = id(o)
    if k not in _ids:
        _ids[k] = len(_ids) + 1
        _halten.append(o)
    return _ids[k]

_TYPEN = {int: "int", float: "float", str: "str", bool: "bool", type(None): "NoneType",
          list: "list", tuple: "tuple", dict: "dict", set: "set", frozenset: "set"}

def _kurz(text, n=200):
    return text if len(text) <= n else text[:n - 1] + "…"

def _wert(o, tiefe=0):
    typ = _TYPEN.get(type(o))
    if typ is None:
        if isinstance(o, (_types.FunctionType, _types.BuiltinFunctionType, _types.MethodType)):
            typ = "function"
        elif isinstance(o, _types.ModuleType):
            typ = "module"
        else:
            typ = "andere"
    if typ == "function":
        try:
            c = o.__code__
            r = "Funktion " + o.__name__ + "(" + ", ".join(c.co_varnames[:c.co_argcount]) + ")"
        except AttributeError:
            r = "Funktion " + getattr(o, "__name__", "?")
    else:
        try:
            r = _kurz(repr(o))
        except BaseException:
            r = "<?>"
    w = {"typ": typ, "repr": r, "id": _id(o)}
    if typ in ("list", "tuple", "set") and tiefe < 3:
        elemente = list(o)
        w["elemente"] = [_wert(x, tiefe + 1) for x in elemente[:30]]
        if len(elemente) > 30:
            w["gekuerzt"] = True
    elif typ == "dict" and tiefe < 3:
        paare = list(o.items())
        w["paare"] = [[_wert(k, tiefe + 1), _wert(v, tiefe + 1)] for k, v in paare[:30]]
        if len(paare) > 30:
            w["gekuerzt"] = True
    return w

def _sichtbar(name, o):
    if name.startswith("__") and name.endswith("__"):
        return False
    if isinstance(o, _types.ModuleType):
        return False
    if isinstance(o, (_types.BuiltinFunctionType, _types.BuiltinMethodType)):
        return False
    if isinstance(o, _types.FunctionType) and o.__code__.co_filename != _DATEI:
        return False
    if isinstance(o, type) and getattr(o, "__module__", "") != "__main__":
        return False
    return True

def _variablen(frame):
    ns = frame.f_globals if frame.f_code.co_name == "<module>" else dict(frame.f_locals)
    return {n: _wert(v) for n, v in list(ns.items()) if _sichtbar(n, v)}

def _stapel(frame):
    rahmen = []
    f = frame
    while f is not None and f.f_code.co_filename == _DATEI:
        name = f.f_code.co_name
        rahmen.append({"funktion": "<modul>" if name == "<module>" else name,
                       "zeile": f.f_lineno, "variablen": _variablen(f)})
        f = f.f_back
    rahmen.reverse()
    return rahmen

_schritte = []

def _ende(abgebrochen, fehler=None, zeile=None):
    _sys.settrace(None)
    erg = {"schritte": _schritte, "abgebrochen": abgebrochen, "fehler": fehler,
           "fehler_zeile": zeile, "ausgabe": "".join(_puffer)}
    _echt.write("\n@@TRACE@@" + _json.dumps(erg) + "\n")
    _echt.flush()
    _os._exit(0)

def _schritt(frame, ereignis, arg):
    if len(_schritte) >= _MAX:
        _ende(True)
    s = {"zeile": frame.f_lineno, "ereignis": ereignis, "stapel": _stapel(frame),
         "ausgabe": "".join(_puffer), "rueckgabe": None}
    if ereignis == "return":
        s["rueckgabe"] = _wert(arg)
    elif ereignis == "exception":
        s["fehler"] = arg[0].__name__ + ": " + str(arg[1])
    _schritte.append(s)

def _lokal(frame, ereignis, arg):
    if ereignis in ("line", "return", "exception"):
        _schritt(frame, ereignis, arg)
    return _lokal

def _global(frame, ereignis, arg):
    if frame.f_code.co_filename != _DATEI:
        return None
    if ereignis == "call" and frame.f_code.co_name != "<module>":
        _schritt(frame, "call", None)
    return _lokal

with open(_DATEI, encoding="utf-8") as _f:
    _quelltext = _f.read()
try:
    _code = compile(_quelltext, _DATEI, "exec")
except SyntaxError as _e:
    _ende(False, "SyntaxError: " + str(_e.msg), _e.lineno)
_sys.stdout = _Aus()
_b.input = _input
_ns = {"__name__": "__main__", "__builtins__": _b}
try:
    _sys.settrace(_global)
    exec(_code, _ns)
    _sys.settrace(None)
except SystemExit:
    _sys.settrace(None)
    _ende(False)
except BaseException as _e:
    _sys.settrace(None)
    _zeile = None
    _t = _e.__traceback__
    while _t is not None:
        if _t.tb_frame.f_code.co_filename == _DATEI:
            _zeile = _t.tb_lineno
        _t = _t.tb_next
    if isinstance(_e, SyntaxError) and _zeile is None:
        _zeile = _e.lineno
    _ende(False, type(_e).__name__ + ": " + str(_e), _zeile)
_ende(False)
'''


def trace(code, eingaben=(), max_schritte=400, timeout=10):
    """Führt Code Schritt für Schritt aus (Format siehe ARCHITEKTUR.md Abschnitt 7).

    Rückgabe: {"schritte", "abgebrochen", "fehler", "fehler_zeile", "fehler_erklaert",
               "ausgabe", "timeout"}
    """
    code = (code or "").expandtabs(4)
    with _MAX_PROZESSE:
        tmp = tempfile.mkdtemp(prefix="vorkurs_quiz_")
        try:
            with open(os.path.join(tmp, DATEINAME), "w", encoding="utf-8") as f:
                f.write(code)
            umgebung = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
            try:
                r = subprocess.run([sys.executable, "-X", "utf8", "-B", "-c", _TRACE_SKRIPT,
                                    str(int(max_schritte))],
                                   input=json.dumps([str(e) for e in (eingaben or [])]),
                                   capture_output=True, text=True, encoding="utf-8",
                                   errors="replace", timeout=timeout, cwd=tmp, env=umgebung,
                                   creationflags=_CREATIONFLAGS)
            except subprocess.TimeoutExpired:
                return {"schritte": [], "abgebrochen": True, "timeout": True,
                        "fehler": "Timeout: Zeitlimit überschritten", "fehler_zeile": None,
                        "fehler_erklaert": fehler_erklaeren("Timeout"), "ausgabe": ""}
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    erg = _marker_lesen(r.stdout, "@@TRACE@@")
    if erg is None:
        fehler = fehler_letzte_zeile(r.stderr) or "Der Tracer ist unerwartet abgebrochen."
        return {"schritte": [], "abgebrochen": True, "timeout": False, "fehler": fehler,
                "fehler_zeile": None, "fehler_erklaert": fehler_erklaeren(fehler), "ausgabe": ""}
    erg["timeout"] = False
    erg["fehler_erklaert"] = fehler_erklaeren(erg["fehler"]) if erg.get("fehler") else None
    return erg
