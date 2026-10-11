# -*- coding: utf-8 -*-
"""Prüft beim Start, ob alles da ist (Python-Version, Schreibrechte, Dateien, Konsole).

Hinweis: Diese Datei muss auch unter alten Python-Versionen fehlerfrei
importierbar sein (keine neue Syntax), damit die Meldung ankommt.
"""

import os
import subprocess
import sys

MINDEST_VERSION = (3, 10)

# Optionale Zusatzpakete (pip-Name). MUSS LEER BLEIBEN – nur Standardbibliothek!
OPTIONALE_PAKETE = []

_HIER = os.path.dirname(os.path.abspath(__file__))
STATIC_ORDNER = os.path.join(_HIER, "web", "static")


def version_ok():
    return sys.version_info[:2] >= MINDEST_VERSION


def versions_meldung():
    return ("Dieses Programm braucht Python {}.{} oder neuer – du hast Python {}.\n"
            "Lade die aktuelle Version von https://www.python.org/downloads/ herunter."
            .format(MINDEST_VERSION[0], MINDEST_VERSION[1], sys.version.split()[0]))


def konsole_vorbereiten():
    """Stellt die Konsole auf UTF-8 und schaltet unter Windows die Farben frei."""
    for strom in (sys.stdout, sys.stderr):
        try:
            strom.reconfigure(encoding="utf-8")
        except Exception:
            pass
    if os.name == "nt":
        try:
            os.system("")  # aktiviert ANSI-Farbcodes in der Windows-Konsole
        except Exception:
            pass


def gui_dateien_vorhanden():
    return os.path.isfile(os.path.join(STATIC_ORDNER, "index.html"))


def fehlende_pakete():
    import importlib.util
    return [p for p in OPTIONALE_PAKETE if importlib.util.find_spec(p) is None]


def pakete_installieren(pakete):
    """Installiert Pakete mit pip (--user). Nur nach Rückfrage aufrufen!"""
    if not pakete:
        return True
    befehl = [sys.executable, "-m", "pip", "install", "--user"] + list(pakete)
    return subprocess.call(befehl) == 0


def pruefen(gui=True):
    """Liefert eine Liste von Problemen (deutsche Texte). Leere Liste = alles gut."""
    probleme = []
    if not version_ok():
        probleme.append(versions_meldung())
        return probleme
    try:
        from . import fortschritt
        if not fortschritt.ordner_beschreibbar():
            probleme.append(
                "Der Ordner für deinen Fortschritt ({}) ist nicht beschreibbar. "
                "Der Fortschritt wird stattdessen im Programmordner gespeichert."
                .format(fortschritt.daten_ordner()))
    except Exception as e:  # pragma: no cover - nur zur Sicherheit
        probleme.append("Der Fortschritt kann nicht gespeichert werden: {}".format(e))
    if gui and not gui_dateien_vorhanden():
        probleme.append(
            "Die Dateien der grafischen Oberfläche fehlen (vorkurs/web/static). "
            "Die Terminal-Version funktioniert trotzdem. Lade den Programmordner "
            "am besten noch einmal vollständig herunter.")
    kodierung = (getattr(sys.stdout, "encoding", None) or "").lower().replace("-", "")
    if kodierung and kodierung not in ("utf8", "utf_8"):
        probleme.append(
            "Deine Konsole benutzt die Zeichenkodierung '{}'. Umlaute und Symbole "
            "könnten falsch aussehen. Unter Windows hilft 'chcp 65001' (Start.bat "
            "macht das automatisch).".format(sys.stdout.encoding))
    fehlend = fehlende_pakete()
    if fehlend:
        probleme.append("Es fehlen Zusatzpakete: {}".format(", ".join(fehlend)))
    return probleme
