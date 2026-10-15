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
                   "faktor": "-1/2", "interaktiv": True, "unterschrift": "Summe als Parallelogramm, Vielfaches mit Faktor $\\lambda$."},
    "matrix_mult": {"a": [[1, 2, 0], [-1, 3, 1]], "b": [[2, 1], [0, -1], [4, "1/2"]],
                    "unterschrift": "Eintrag $c_{ij}$ = Zeile $i$ von $A$ mal Spalte $j$ von $B$."},
    "gauss": {"matrix": [[1, 1, 1], [2, -1, 1], [1, 2, -1]], "rechts": [6, 3, 2]},
    "komplexe_ebene": {"z": [1, 1], "w": ["sqrt(3)", 1], "op": "mal", "interaktiv": True,
                       "unterschrift": "Beim Multiplizieren werden die Beträge multipliziert und die Winkel addiert."},
})

# Diskrete Mathematik, Logik, Folgen (vis_diskret.js)
DEMO.update({
    "venn": {"mengen": [{"name": "A", "elemente": [1, 2, 3, 4]}, {"name": "B", "elemente": [3, 4, 5, 6]},
                        {"name": "C", "elemente": [4, 6, 7]}],
             "universum": [1, 2, 3, 4, 5, 6, 7, 8, 9], "markiert": "(A ∩ B) \\ C",
             "unterschrift": "Markiert ist $(A \\cap B) \\setminus C$. Tippe auf eine Fläche: Du siehst ihre Formel und ihre Elemente."},
    "wahrheitstabelle": {"variablen": ["A", "B"], "ausdruecke": ["A => B", "!B => !A", "A or !A"],
                         "markiert": ["A => B"],
                         "unterschrift": "Gleiche Spalten heißen: Die Aussagen sind äquivalent (Kontraposition)."},
    "relation_graph": {"links": [1, 2, 3, 4], "rechts": ["a", "b", "c"], "pfeile": [[1, "a"], [2, "b"], [3, "b"], [4, "c"]],
                       "namen": ["A", "B"], "unterschrift": "Tippe auf eine Eigenschaft: Verstöße werden im Bild markiert."},
    "pascal": {"zeilen": 8, "markiert": [[5, 2]], "interaktiv": True,
               "unterschrift": "Jede Zahl ist die Summe der beiden darüber. Tippe auf eine Zahl (oder Pfeiltasten)."},
    "euklid": {"a": 252, "b": 105, "erweitert": True},
    "modulo_uhr": {"n": 12, "start": 7, "plus": 8, "interaktiv": True,
                   "unterschrift": "$7 + 8 = 15$, auf der Uhr landet man bei $3$: $15 \\equiv 3 \\pmod{12}$."},
    "induktion_domino": {"anzahl": 8, "anfang": 1, "aussage": "$1 + 2 + \\ldots + n = \\frac{n(n+1)}{2}$"},
    "folge": {"term": "(n+1)/n", "n_bis": 30, "grenzwert": "1", "epsilon": "1/10", "interaktiv": True,
              "monotonie": True, "schranken": True,
              "unterschrift": "Schiebe $\\varepsilon$: Je schmaler der Schlauch, desto später liegen alle Glieder darin."},
})


# Relationen und Ordnungen (vis_ordnung.js); eine Liste = mehrere Beispiele desselben Typs
_POTENZ = [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
DEMO.update({
    "graph_gerichtet": [
        {"elemente": [1, 2, 3, 4], "paare": [[1, 1], [2, 2], [3, 3], [4, 4], [1, 2], [2, 1], [2, 3], [3, 4]],
         "markiert": [[2, 3]], "layout": "kreis",
         "unterschrift": "Schleifen an 1 bis 4 (reflexiv), $1 \\leftrightarrow 2$ als gegenläufiges Paar. Der Pfeil $2 \\to 3$ ist markiert."},
        {"elemente": [[], [1], [1, 2]], "paare": [[[], []], [[], [1]], [[], [1, 2]], [[1], [1]], [[1], [1, 2]], [[1, 2], [1, 2]]],
         "layout": {"∅": [0, 0], "{1}": [1, 0], "{1, 2}": [2, 0]},
         "unterschrift": "Mengen als Knoten: die Relation $\\subseteq$ auf $\\{\\emptyset, \\{1\\}, \\{1, 2\\}\\}$."}],
    "hasse": [
        {"elemente": _POTENZ, "paare": [[a, b] for a in _POTENZ for b in _POTENZ if set(a) <= set(b)],
         "teilmenge": [[1], [2]], "sup": True, "inf": True, "schranken": True,
         "unterschrift": "Potenzmenge von $\\{1, 2, 3\\}$ mit $\\subseteq$. Schwarz: $T = \\{\\{1\\}, \\{2\\}\\}$, orange: Supremum, grün: Infimum."},
        {"elemente": [1, 2, 3, 4, 6, 12], "paare": [[a, b] for a in (1, 2, 3, 4, 6, 12) for b in (1, 2, 3, 4, 6, 12) if b % a == 0],
         "unterschrift": "Teilbarkeit auf den Teilern von $12$: $a \\preceq b$ genau dann, wenn $a \\mid b$."}],
    "aequivalenz_klassen": [
        {"klassen": [[0, 3, 6], [1, 4, 7], [2, 5, 8]], "repraesentanten": [0, 1, 2],
         "unterschrift": "Rest beim Teilen durch $3$: Jede Zahl liegt in genau einer Klasse."},
        {"klassen": [[1, 2], [3], [4, 5, 6]], "graph": True,
         "unterschrift": "Dieselbe Idee als Graph: Reflexiv (Schleifen), symmetrisch (Doppelpfeile), transitiv."}],
})
DEMO["komplexe_ebene"] = [DEMO["komplexe_ebene"],
                          {"punkte": [{"z": [3, 4], "label": "z_1"}, {"z": [-2, 1], "label": "z_2"}],
                           "konjugiert": True, "betragskreis": True,
                           "unterschrift": "Gestrichelt: die Konjugierten (Spiegelung an der reellen Achse) und die Kreise mit dem Betrag als Radius."}]


def demo_daten():
    erg = []
    for art in visuals.VISUAL_TYPEN:
        if art not in DEMO or art not in visuals.VISUAL_FERTIG:
            continue
        for beispiel in (DEMO[art] if isinstance(DEMO[art], list) else [DEMO[art]]):
            d = copy.deepcopy(beispiel)
            fehler = "; ".join(visuals.pruefen(art, d)) or None
            if not fehler:
                try:
                    visuals.ergaenzen(art, d)
                except Exception as e:  # noqa: BLE001
                    fehler = f"{type(e).__name__}: {e}"
            erg.append({"art": art, "daten": d, "fehler": fehler})
    return erg
