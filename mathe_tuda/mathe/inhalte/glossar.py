# -*- coding: utf-8 -*-
"""Glossar: alle Fachbegriffe mit kurzer Erklärung und Beispiel.

Im Markup verweist [[Begriff]] oder [[angezeigter Text|Begriff]] auf einen Eintrag.
Die Oberfläche zeigt dann beim Darüberfahren (oder Antippen) die Erklärung.
Felder: begriff, erklaerung (Markup), beispiel (Markup), kapitel (slug, wo der Begriff
eingeführt wird), synonyme (weitere Schreibweisen, die auf denselben Eintrag zeigen).
"""

GLOSSAR = []
LADEFEHLER = []


def eintrag(begriff, erklaerung, beispiel="", kapitel=None, synonyme=()):
    GLOSSAR.append({"begriff": begriff, "erklaerung": erklaerung, "beispiel": beispiel,
                    "kapitel": kapitel, "synonyme": list(synonyme)})


def finden(name):
    n = str(name).strip().lower()
    for e in GLOSSAR:
        if e["begriff"].lower() == n or n in (s.lower() for s in e["synonyme"]):
            return e
    return None


def _alle_laden():
    """Lädt _glossar_eintraege.py und jede Datei _glossar_<kapitel>.py (eine pro Kapitel,
    damit Autoren parallel arbeiten können)."""
    import importlib
    import pkgutil
    from . import __path__ as pfad
    for m in sorted(m.name for m in pkgutil.iter_modules(pfad) if m.name.startswith("_glossar_")):
        try:
            importlib.import_module(f"{__package__}.{m}")
        except Exception as e:
            LADEFEHLER.append((m, f"{type(e).__name__}: {e}"))


_alle_laden()
