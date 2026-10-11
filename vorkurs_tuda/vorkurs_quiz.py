#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DAS GROSSE PYTHON-VORKURS-LERNQUIZ (v2)
Programmiervorkurs TU Darmstadt 2026

Starten:
    Windows:     Doppelklick auf Start.bat   (oder: py vorkurs_quiz.py)
    macOS:       Doppelklick auf Start.command
    Linux:       ./start.sh                  (oder: python3 vorkurs_quiz.py)

Optionen:
    --gui            grafische Oberfläche im Browser starten
    --terminal       Terminal-Version starten
    --selbsttest     alle Inhalte automatisch prüfen
    --keine-farben   keine Farben im Terminal
    --port N         Port für die grafische Oberfläche (Standard 8765)
    --kein-browser   Browser nicht automatisch öffnen

Benötigt Python 3.10 oder neuer. Keine Zusatzpakete nötig.
"""

# ACHTUNG: Diese Datei muss auch von sehr alten Python-Versionen gelesen werden
# können, damit die Versionsmeldung ankommt. Deshalb hier keine f-Strings o. Ä.
import sys

if sys.version_info < (3, 10):
    print("")
    print("  Dieses Lernquiz braucht Python 3.10 oder neuer.")
    print("  Du hast Python " + sys.version.split()[0] + ".")
    print("  Lade die aktuelle Version von https://www.python.org/downloads/ herunter")
    print("  (unter Windows einfach Start.bat doppelklicken - das hilft beim Installieren).")
    print("")
    sys.exit(1)

import argparse  # noqa: E402
import os  # noqa: E402

HIER = os.path.dirname(os.path.abspath(__file__))
if HIER not in sys.path:
    sys.path.insert(0, HIER)

STANDARD_PORT = 8765


def optionen_lesen(argv=None):
    p = argparse.ArgumentParser(
        prog="vorkurs_quiz.py",
        description="Python-Lernquiz zum Programmiervorkurs der TU Darmstadt")
    modus = p.add_mutually_exclusive_group()
    modus.add_argument("--gui", action="store_true", help="grafische Oberfläche im Browser")
    modus.add_argument("--terminal", action="store_true", help="Terminal-Version")
    modus.add_argument("--selbsttest", action="store_true", help="alle Inhalte prüfen")
    p.add_argument("--keine-farben", action="store_true", help="keine Farben im Terminal")
    p.add_argument("--port", type=int, default=None, metavar="N",
                   help="Port der grafischen Oberfläche (Standard %d)" % STANDARD_PORT)
    p.add_argument("--kein-browser", action="store_true", help="Browser nicht automatisch öffnen")
    # nur für automatische Oberflächentests (verrät Musterlösungen), daher nicht in der Hilfe
    p.add_argument("--e2e", action="store_true", help=argparse.SUPPRESS)
    return p.parse_args(argv)


def farbig(text, code, an):
    return "\033[%sm%s\033[0m" % (code, text) if an else text


def modus_fragen(farben):
    """Fragt im Terminal: grafisch oder Terminal? Rückgabe 'gui' oder 'terminal'."""
    rahmen = "═" * 62
    print("")
    print(farbig("  ╔" + rahmen + "╗", "95", farben))
    print(farbig("  ║", "95", farben) + farbig("  DAS GROSSE PYTHON-VORKURS-LERNQUIZ".ljust(62), "1", farben)
          + farbig("║", "95", farben))
    print(farbig("  ║", "95", farben) + "  Programmiervorkurs TU Darmstadt".ljust(62)
          + farbig("║", "95", farben))
    print(farbig("  ╚" + rahmen + "╝", "95", farben))
    print("")
    print("  Wie möchtest du lernen?")
    print("")
    print("    " + farbig("[1]", "1;92", farben) + " Grafische Oberfläche im Browser " + farbig("(empfohlen)", "92", farben))
    print("    " + farbig("[2]", "1;96", farben) + " Terminal")
    print("")
    while True:
        try:
            wahl = input("  Deine Wahl [1/2, Enter = 1]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("")
            return None
        if wahl in ("", "1", "g", "gui", "grafisch"):
            return "gui"
        if wahl in ("2", "t", "terminal"):
            return "terminal"
        if wahl in ("q", "x", "exit", "quit", "ende"):
            return None
        print("  Bitte 1 oder 2 eingeben.")


def fehlendes_modul(name, fehler):
    """True, wenn genau das Modul 'name' (oder ein Elternpaket davon) fehlt."""
    fehlt = getattr(fehler, "name", None) or ""
    return isinstance(fehler, ModuleNotFoundError) and (name == fehlt or name.startswith(fehlt + "."))


def gui_starten(optionen, farben):
    try:
        from vorkurs.web import server
    except ImportError as e:
        if fehlendes_modul("vorkurs.web.server", e):
            print("")
            print(farbig("  Die grafische Oberfläche ist in diesem Programmordner (noch) nicht", "93", farben))
            print(farbig("  enthalten (vorkurs/web/server.py fehlt).", "93", farben))
            print("  Starte stattdessen die Terminal-Version:  python vorkurs_quiz.py --terminal")
            return 1
        raise
    port = optionen.port if optionen.port else STANDARD_PORT
    if optionen.e2e:
        return server.main(port=port, browser=not optionen.kein_browser, e2e=True)
    return server.main(port=port, browser=not optionen.kein_browser)


def terminal_starten(farben):
    try:
        from vorkurs.terminal import app
    except ImportError as e:
        if fehlendes_modul("vorkurs.terminal.app", e):
            print("")
            print(farbig("  Die Terminal-Version ist in diesem Programmordner (noch) nicht", "93", farben))
            print(farbig("  enthalten (vorkurs/terminal/app.py fehlt).", "93", farben))
            print("  Starte stattdessen die grafische Oberfläche:  python vorkurs_quiz.py --gui")
            return 1
        raise
    return app.main(farben=farben)


def main(argv=None):
    optionen = optionen_lesen(argv)
    from vorkurs import umgebung
    umgebung.konsole_vorbereiten()
    farben = not optionen.keine_farben and sys.stdout.isatty()

    if optionen.selbsttest:
        from vorkurs import selbsttest
        return selbsttest.main(farben=farben)

    if optionen.gui:
        modus = "gui"
    elif optionen.terminal:
        modus = "terminal"
    else:
        modus = modus_fragen(farben)
        if modus is None:
            return 0

    probleme = umgebung.pruefen(gui=(modus == "gui"))
    for problem in probleme:
        print("")
        print(farbig("  Hinweis: ", "93", farben) + problem)
    if modus == "gui" and not umgebung.gui_dateien_vorhanden():
        print("")
        print("  Die grafische Oberfläche kann nicht starten – ich starte die Terminal-Version.")
        modus = "terminal"

    try:
        if modus == "gui":
            ergebnis = gui_starten(optionen, farben)
        else:
            ergebnis = terminal_starten(farben)
    except KeyboardInterrupt:
        print("")
        print("  Bis bald – und viel Erfolg im Studium!")
        return 0
    return ergebnis if isinstance(ergebnis, int) else 0


if __name__ == "__main__":
    sys.exit(main())
