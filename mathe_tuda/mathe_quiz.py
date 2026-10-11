#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MATHE FÜR INFORMATIK – LERNSYSTEM
TU Darmstadt 2026 · Mathe 1 und Mathe 2 von null an

Starten:
    Windows:     Doppelklick auf Start.bat   (oder: py mathe_quiz.py)
    macOS:       Doppelklick auf Start.command
    Linux:       ./start.sh                  (oder: python3 mathe_quiz.py)

Optionen:
    --gui            grafische Oberfläche im Browser (Standard)
    --selbsttest     alle Inhalte automatisch prüfen
    --kapitel SLUG   beim Selbsttest nur dieses Kapitel (mehrfach möglich)
    --port N         Port der Oberfläche (Standard 8766)
    --kein-browser   Browser nicht automatisch öffnen

Benötigt Python 3.10 oder neuer. Keine Zusatzpakete, kein Internet.
"""

# ACHTUNG: Diese Datei muss auch von sehr alten Python-Versionen gelesen werden
# können, damit die Versionsmeldung ankommt. Deshalb hier keine f-Strings o. Ä.
import sys

if sys.version_info < (3, 10):
    print("")
    print("  Dieses Lernsystem braucht Python 3.10 oder neuer.")
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

STANDARD_PORT = 8766


def optionen_lesen(argv=None):
    p = argparse.ArgumentParser(prog="mathe_quiz.py",
                                description="Mathe-Lernsystem für Informatik (TU Darmstadt)")
    modus = p.add_mutually_exclusive_group()
    modus.add_argument("--gui", action="store_true", help="grafische Oberfläche im Browser (Standard)")
    modus.add_argument("--selbsttest", action="store_true", help="alle Inhalte prüfen")
    p.add_argument("--kapitel", action="append", metavar="SLUG", help="Selbsttest nur für dieses Kapitel")
    p.add_argument("--leise", action="store_true", help="Selbsttest: Warnungen nicht einzeln zeigen")
    p.add_argument("--keine-farben", action="store_true", help="keine Farben im Terminal")
    p.add_argument("--port", type=int, default=None, metavar="N",
                   help="Port der Oberfläche (Standard %d)" % STANDARD_PORT)
    p.add_argument("--kein-browser", action="store_true", help="Browser nicht automatisch öffnen")
    p.add_argument("--e2e", action="store_true", help=argparse.SUPPRESS)
    return p.parse_args(argv)


def main(argv=None):
    optionen = optionen_lesen(argv)
    from mathe import umgebung
    umgebung.konsole_vorbereiten()
    farben = not optionen.keine_farben and sys.stdout.isatty()

    if optionen.selbsttest:
        from mathe import selbsttest
        return selbsttest.main(farben=farben, kapitel=optionen.kapitel, leise=optionen.leise)

    for problem in umgebung.pruefen(gui=True):
        print("")
        print("  Hinweis: " + problem)
    if not umgebung.version_ok() or not umgebung.gui_dateien_vorhanden():
        return 1
    from mathe.web import server
    port = optionen.port if optionen.port else STANDARD_PORT
    try:
        return server.main(port=port, browser=not optionen.kein_browser, e2e=optionen.e2e)
    except KeyboardInterrupt:
        print("")
        print("  Bis bald – und viel Erfolg im Studium!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
