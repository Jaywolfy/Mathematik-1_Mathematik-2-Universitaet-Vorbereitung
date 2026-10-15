# -*- coding: utf-8 -*-
"""Lädt alle Kapitelmodule in fester Reihenfolge.

Reihenfolge: f* (Fundament), v* (Vorkurs), m1_* (Mathe 1), m2_* (Mathe 2), b_* (Bonus), k_* (Klausur);
innerhalb einer Gruppe alphabetisch nach Dateiname. Welcher TEIL ein Kapitel ist,
entscheidet allein der Wert `teil` im Modul – die Dateinamen regeln nur die Reihenfolge.
Module, die mit "_" beginnen, sowie glossar, formelsammlung und diagnose sind keine Kapitel.
"""

import importlib
import pkgutil

from .formelsammlung import FORMELSAMMLUNG  # noqa: F401
from .glossar import GLOSSAR  # noqa: F401

KEINE_KAPITEL = {"glossar", "formelsammlung", "diagnose"}
_GRUPPEN = ("vl_", "f", "v", "m1_", "m2_", "b_", "k_")


def _sortierschluessel(name):
    for i, praefix in enumerate(_GRUPPEN):
        if name.startswith(praefix) and (praefix not in ("f", "v") or name[1:3].isdigit()):
            return (i, name)
    return (len(_GRUPPEN), name)


def modulnamen():
    namen = [m.name for m in pkgutil.iter_modules(__path__)
             if not m.name.startswith("_") and m.name not in KEINE_KAPITEL]
    return sorted(namen, key=_sortierschluessel)


LADEFEHLER = []   # [(modulname, fehlertext)]; der Selbsttest meldet jeden als Fehler


def _laden(name):
    try:
        importlib.import_module(f"{__name__}.{name}")
    except Exception as e:  # ein kaputtes Kapitel darf die anderen nicht blockieren
        import traceback
        LADEFEHLER.append((name, "".join(traceback.format_exception_only(type(e), e)).strip()))


for _name in modulnamen():
    _laden(_name)
