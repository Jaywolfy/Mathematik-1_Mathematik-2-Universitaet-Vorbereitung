"""Ein- und Ausgabe im Terminal: Eingaben mit 'menü'/Strg+C/EOF-Behandlung,
Windows-Farbunterstützung, Ausgabe von Zeilenlisten."""

from __future__ import annotations

import os
import sys

from . import render as r


class ZurueckZumMenue(Exception):
    """'menü' getippt oder Strg+C gedrückt -> zurück ins Hauptmenü."""


class ProgrammEnde(Exception):
    """Eingabe ist zu Ende (EOF, z. B. Strg+Z/Strg+D) -> sauber beenden."""


MENUE_WOERTER = {"menü", "menue", "menu", "hauptmenü", "hauptmenue"}
WEISS_NICHT = {"x", "weiß nicht", "weiss nicht", "keine ahnung", "?!"}

_ECHO = False   # Eingaben mit ausgeben, wenn stdin keine Tastatur ist (Tests, Pipes)


def vorbereiten(farben=True):
    """UTF-8 einstellen, unter Windows ANSI-Farben einschalten.
    Rückgabe: ob Farben tatsächlich benutzt werden."""
    global _ECHO
    for strom in (sys.stdout, sys.stderr):
        try:
            strom.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    try:
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        _ECHO = not sys.stdin.isatty()
    except Exception:
        _ECHO = False

    erzwungen = os.environ.get("VORKURS_FARBEN", "").strip() == "1"
    if os.environ.get("NO_COLOR") and not erzwungen:
        farben = False
    try:
        ist_tty = sys.stdout.isatty()
    except Exception:
        ist_tty = False
    if farben and not ist_tty and not erzwungen:
        farben = False
    if farben and os.name == "nt" and ist_tty:
        farben = _windows_vt_einschalten()
    r.farben_setzen(farben)
    return farben


def _windows_vt_einschalten():
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)          # STD_OUTPUT_HANDLE
        modus = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(modus)):
            return False
        if modus.value & 0x0004:
            return True
        return bool(kernel32.SetConsoleMode(handle, modus.value | 0x0004))  # VIRTUAL_TERMINAL
    except Exception:
        try:
            os.system("")   # alter Trick: schaltet VT in vielen Konsolen frei
            return True
        except Exception:
            return False


def ausgeben(zeilen=()):
    """Gibt Zeilen (Liste oder einzelner Text) aus."""
    if isinstance(zeilen, str):
        zeilen = [zeilen]
    text = "\n".join(zeilen)
    try:
        print(text, flush=True)
    except UnicodeEncodeError:  # pragma: no cover - sehr alte Konsolen
        print(text.encode("ascii", "replace").decode("ascii"), flush=True)


def leer(n=1):
    print("\n" * (n - 1), flush=True)


def eingabe(prompt="", menue=True):
    """Wie input(), aber:
       'menü' / Strg+C  -> ZurueckZumMenue
       Ende der Eingabe -> ProgrammEnde"""
    try:
        antwort = input(prompt)
    except EOFError:
        print()
        raise ProgrammEnde()
    except KeyboardInterrupt:
        print()
        raise ZurueckZumMenue()
    if _ECHO:
        print(r.grau(antwort) if antwort else "")
    if menue and antwort.strip().lower() in MENUE_WOERTER:
        raise ZurueckZumMenue()
    return antwort


def weiter(text="[Enter] = weiter", menue=True):
    """Wartet auf Enter. Gibt die (kleingeschriebene) Eingabe zurück."""
    return eingabe(r.grau(f"\n  {text} "), menue=menue).strip().lower()


def ja_nein(frage, standard=None):
    """j/n-Abfrage. Enter = standard (falls gesetzt)."""
    while True:
        auswahl = "(J/n)" if standard is True else ("(j/N)" if standard is False else "(j/n)")
        a = eingabe(f"  {frage} " + r.grau(auswahl + " ")).strip().lower()
        if a in ("j", "ja", "y", "yes"):
            return True
        if a in ("n", "nein", "no"):
            return False
        if a == "" and standard is not None:
            return standard
        ausgeben("  " + r.grau("Bitte j (ja) oder n (nein) eingeben."))


def bildschirm_leeren():
    """Leert den Bildschirm nur in echten Terminals mit Farben."""
    if r.farben_an() and not _ECHO:
        print("\x1b[2J\x1b[H", end="", flush=True)
