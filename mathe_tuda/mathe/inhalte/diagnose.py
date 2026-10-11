# -*- coding: utf-8 -*-
"""Diagnosetest: 25 gemischte Fragen aus dem Fundament, danach eine Empfehlung.

Je Fundament-Kapitel werden Generatoren (bevorzugt) oder Übungsfragen gezogen.
auswerten() bekommt {slug: [richtig, gesamt]} und empfiehlt das erste Kapitel mit
weniger als 70 % richtig.
"""

import random

from .. import engine

ANZAHL = 25
SCHWELLE = 0.7


def fragen_ziehen(anzahl=ANZAHL):
    kap = engine.kapitel_von_teil("fundament")
    if not kap:
        return []
    erg, i = [], 0
    while len(erg) < anzahl and i < anzahl * 4:
        k = kap[i % len(kap)]
        i += 1
        pool = k.generatoren() or [f for f in k.fragen() if f.phase == "ueben" and f.typ not in ("papier",)]
        if pool:
            f = random.choice(pool)
            erg.append(f.instanz() if isinstance(f, engine.Generator) else f)
    return erg


def auswerten(ergebnisse):
    kapitel, empfehlung = {}, None
    for k in engine.kapitel_von_teil("fundament"):
        r, g = ergebnisse.get(k.slug, [0, 0])
        quote = r / g if g else None
        kapitel[k.slug] = {"titel": k.titel, "richtig": r, "gesamt": g, "quote": quote,
                           "luecke": quote is not None and quote < SCHWELLE}
        if empfehlung is None and quote is not None and quote < SCHWELLE:
            empfehlung = k.slug
    alle = engine.kapitel_von_teil("fundament")
    if empfehlung is None:
        empfehlung = alle[-1].slug if alle else None
    k = engine.kapitel_nach_slug(empfehlung) if empfehlung else None
    return {"kapitel": kapitel, "empfehlung": empfehlung, "empfehlung_titel": k.titel if k else None,
            "luecken": [s for s, e in kapitel.items() if e["luecke"]]}
