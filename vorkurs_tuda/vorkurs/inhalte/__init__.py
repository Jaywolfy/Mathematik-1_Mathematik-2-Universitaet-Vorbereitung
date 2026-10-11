# -*- coding: utf-8 -*-
"""Lädt alle Kapitelmodule in fester Reihenfolge.

Reihenfolge: t1_*, t2_*, ... (nach Tag), dann c_* (Challenge), dann b_* (Bonus);
innerhalb einer Gruppe alphabetisch nach Dateiname. Dateien, die mit "_"
beginnen, und spickzettel.py werden nicht als Kapitel geladen.
"""

import importlib
import pkgutil
import re

from .spickzettel import SPICKZETTEL  # noqa: F401


def _sortierschluessel(name):
    m = re.match(r"^t(\d+)_", name)
    if m:
        return (0, int(m.group(1)), name)
    if name.startswith("c_"):
        return (1, 0, name)
    if name.startswith("b_"):
        return (2, 0, name)
    return (3, 0, name)


def modulnamen():
    """Namen aller Kapitelmodule in Ladereihenfolge."""
    namen = [m.name for m in pkgutil.iter_modules(__path__)
             if not m.name.startswith("_") and m.name != "spickzettel"]
    return sorted(namen, key=_sortierschluessel)


for _name in modulnamen():
    importlib.import_module(f"{__name__}.{_name}")
