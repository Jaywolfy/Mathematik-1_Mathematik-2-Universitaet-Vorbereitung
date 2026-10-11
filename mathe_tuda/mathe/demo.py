# -*- coding: utf-8 -*-
"""Beispieldaten für die Demo-Seite #/demo/visuals (ein Beispiel je Visual-Typ).

Der Selbsttest prüft alle Beispiele; die Seite zeigt jeden Typ, der im Frontend fertig ist.
"""

import copy

from . import visuals

DEMO = {
    "zahlenstrahl": {"von": -5, "bis": 5, "punkte": [{"x": -3}, {"x": "1/2"}, {"x": 4}],
                     "pfeile": [{"von": -3, "bis": 1}], "intervalle": [{"von": 2, "bis": "inf", "von_zu": True}],
                     "interaktiv": True, "unterschrift": "Punkte, ein Pfeil für $-3 + 4 = 1$ und das Intervall $[2, \\infty)$."},
    "bruch": {"zaehler": 3, "nenner": 4, "erweitern": 2, "modell": "kuchen", "unterschrift": "Drei Viertel eines Kuchens."},
    "rechnung": {"links": "3x + 5", "rechts": "20", "schritte": [{"op": "-5", "text": "Auf beiden Seiten 5 wegnehmen."},
                                                               {"op": ":3", "text": "Beide Seiten durch 3 teilen."}]},
    "funktionsgraph": {"funktionen": [{"term": "a*x^2 + c", "label": "f(x)"}],
                       "parameter": [{"name": "a", "wert": 1, "von": -2, "bis": 2}, {"name": "c", "wert": -4, "von": -5, "bis": 5}],
                       "nullstellen": True, "scheitel": True, "wertetabelle": [-2, -1, 0, 1, 2], "x": [-5, 5], "y": [-6, 6]},
    "parabel": {"a": 1, "b": -2, "c": -3, "form": "scheitel"},
}

# Funktionen/Analysis (vis_funktionen.js) und Lineare Algebra/komplexe Zahlen (vis_linalg.js)
DEMO.update({
    "einheitskreis": {"winkel": 60, "zeige": ["sin", "cos", "tan", "kurve"],
                      "unterschrift": "Ziehe den Punkt oder nutze den Regler. Bei Vielfachen von $15^\\circ$ stehen exakte Werte da."},
    "exp_log": {"basis": 2, "unterschrift": "$2^x$ und $\\log_2(x)$ liegen spiegelbildlich zur Geraden $y = x$."},
    "tangente": {"term": "x^2/2", "x0": 1, "h": 2, "ableitung": "x", "x": [-3, 4], "y": [-2, 5],
                 "unterschrift": "Schiebe $h$ gegen $0$: Die Sekante wird zur Tangente."},
    "riemann": {"term": "x^2", "von": 0, "bis": 2, "n": 4, "art": "links", "stammfunktion": "x^3/3",
                "x": [-0.5, 2.5], "y": [-0.5, 4.5], "unterschrift": "Mehr Rechtecke: Die Summe nähert sich dem Integral."},
    "vektoren2d": {"vektoren": [{"x": 3, "y": 1}, {"x": 1, "y": 2}], "zeige": ["summe", "norm", "vielfaches", "skalarprodukt"],
                   "faktor": "-1/2", "interaktiv": True, "unterschrift": "Ziehe die Pfeilspitzen (oder Tab + Pfeiltasten)."},
    "matrix_mult": {"a": [[1, 2, 0], [-1, 3, 1]], "b": [[2, 1], [0, -1], [4, "1/2"]],
                    "unterschrift": "Eintrag $c_{ij}$ = Zeile $i$ von $A$ mal Spalte $j$ von $B$."},
    "gauss": {"matrix": [[1, 1, 1], [2, -1, 1], [1, 2, -1]], "rechts": [6, 3, 2]},
    "komplexe_ebene": {"z": [1, 1], "w": ["sqrt(3)", 1], "op": "mal", "interaktiv": True,
                       "unterschrift": "Beim Multiplizieren werden die Beträge multipliziert und die Winkel addiert."},
})


def demo_daten():
    erg = []
    for art in visuals.VISUAL_TYPEN:
        if art not in DEMO or art not in visuals.VISUAL_FERTIG:
            continue
        d = copy.deepcopy(DEMO[art])
        fehler = "; ".join(visuals.pruefen(art, d)) or None
        if not fehler:
            try:
                visuals.ergaenzen(art, d)
            except Exception as e:  # noqa: BLE001
                fehler = f"{type(e).__name__}: {e}"
        erg.append({"art": art, "daten": d, "fehler": fehler})
    return erg
