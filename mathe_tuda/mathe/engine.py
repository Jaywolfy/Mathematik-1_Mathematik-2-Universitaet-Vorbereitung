# -*- coding: utf-8 -*-
"""Engine: Datenmodell, Fragetypen und Prüflogik – unabhängig von der Oberfläche.

Inhalte (mathe/inhalte/*) benutzen neues_kapitel(...) und die Methoden des
Kapitels (k.zahl, k.term, k.generator, ...). Die Oberfläche benutzt KAPITEL,
TEILE, kapitel_nach_slug(), frage_nach_id() und für jede Frage:

    konkret = frage.instanz(seed)     # Generatoren: neue Zahlen; sonst die Frage selbst
    konkret.to_dict()                 # ohne Lösung
    konkret.pruefen(antwort)          # -> Ergebnis
"""

import hashlib
import math
import random
import re
import textwrap
import threading
from dataclasses import asdict, dataclass, field
from fractions import Fraction

from . import markup, mathlib, pruefer

F = Fraction

TEILE = [
    {"id": "fundament", "titel": "Fundament – Schulmathe von vorn",
     "untertitel": "Zahlen, Brüche, Terme, Gleichungen, Funktionen, Mathe lesen"},
    {"id": "vorkurs", "titel": "Vorkurs – Mathematik-Vorkurs der TU Darmstadt",
     "untertitel": "Mengen, Logik, Beweise, Funktionen, Folgen, Ableiten, Integrieren, Vektoren, Matrizen, komplexe Zahlen"},
    {"id": "mathe1", "titel": "Mathe 1 – Mathematik I für Informatik",
     "untertitel": "Relationen, Modulo und RSA, Gruppen, Ringe, Körper, Lineare Algebra bis Eigenwerte, Folgen und Reihen"},
    {"id": "mathe2", "titel": "Mathe 2 – Mathematik II für Informatik",
     "untertitel": "Stetigkeit, Potenzreihen, Ableiten, Integrieren, mehrere Variablen, Taylor, Fourier, Differentialgleichungen"},
    {"id": "bonus", "titel": "Bonus – Vertiefung", "untertitel": "Mathe mit Python und Ausblicke"},
    {"id": "klausur", "titel": "Klausur – Aufgaben im Uni-Stil", "untertitel": "Probeklausuren Mathe 1 und Mathe 2 (90 Minuten)"},
]
TEIL_IDS = [t["id"] for t in TEILE]

KAPITEL = []
_KAPITEL_NACH_SLUG = {}
_IDS = set()
_FRAGEN = {}
_LOCK = threading.RLock()

LOB = ["Richtig!", "Super!", "Genau so!", "Klasse!", "Stark!", "Perfekt!", "Sehr gut!", "Sauber gerechnet!"]

# Fragetypen, deren Antwort gerechnet wird (brauchen einen Rechenweg)
RECHEN_TYPEN = {"zahl", "term", "loesungsmenge", "menge", "vektor", "matrix", "lgs", "luecke", "graph_punkt"}


# ──────────────────────────────────────────────────────────────────────────
#  Ergebnis
# ──────────────────────────────────────────────────────────────────────────

@dataclass
class Ergebnis:
    ok: bool
    meldung: str = ""                  # Kurzfeedback (Markup)
    loesung: str | None = None         # Lösung als Markup (meist $…$)
    erklaerung: str = ""               # Markup
    rechenweg: str = ""                # Markup (vollständiger Rechenweg)
    details: list = field(default_factory=list)
    hinweis: str | None = None         # erkannte Ursache / Tipp (Markup)
    fehler_erkannt: bool = False       # typischer Fehler erkannt
    fast: bool = False                 # Rechnung stimmt, Form passt nicht (z. B. nicht gekürzt)
    lesefehler: bool = False           # Eingabe nicht lesbar: zählt nicht als Versuch
    teilpunkte: float | None = None    # 0..1 (mehrfach, rechenweg, papier)

    def to_dict(self, mit_loesung=True):
        d = asdict(self)
        if not mit_loesung:
            d["loesung"] = None
            d["rechenweg"] = ""
        return d


def _dedent(text):
    return textwrap.dedent(text or "").strip("\n")


def _als_text(x):
    """Lösungswert (Fraction/int/float/str) -> Term-Text für den Prüfer."""
    if isinstance(x, (int, Fraction)):
        return mathlib.text(x)
    if isinstance(x, float):
        return repr(x)
    return str(x)


# ──────────────────────────────────────────────────────────────────────────
#  Elemente
# ──────────────────────────────────────────────────────────────────────────

class Element:
    typ = "element"
    phase = "verstehen"
    kapitel = None


class Erklaerung(Element):
    typ = "erklaerung"

    def __init__(self, titel, text):
        self.titel = titel
        self.text = text

    def seiten(self):
        return markup.parse(self.text)

    def to_dict(self):
        return {"typ": "erklaerung", "titel": self.titel, "seiten": self.seiten()}


class Zusammenfassung(Element):
    typ = "zusammenfassung"
    phase = "merkzettel"

    def __init__(self, text):
        self.text = text

    def seiten(self):
        return markup.parse(self.text)

    def to_dict(self):
        return {"typ": "zusammenfassung", "seiten": self.seiten()}


class Frage(Element):
    """Basisklasse aller Fragetypen."""
    art = "Frage"
    typ = "frage"
    phase = "ueben"
    eingabe = None          # Modus des Eingabe-Pads

    def __init__(self, frage="", erklaerung="", tipps=None, rechenweg="", typische_fehler=(),
                 uebungsblatt=False, punkte=1, tipp=None):
        self.frage = _dedent(frage) if "\n" in str(frage) else str(frage)
        self.erklaerung = _dedent(erklaerung)
        self.tipps = [str(t) for t in (tipps or ([tipp] if tipp else []))]
        self.rechenweg = _dedent(rechenweg)
        self.typische_fehler = [(w, str(m)) for w, m in (typische_fehler or ())]
        self.uebungsblatt = bool(uebungsblatt)
        self.punkte = punkte
        self.id = None
        self.kapitel = None
        self.seed = None

    # --- Identität ---
    def haupttext(self):
        return self.frage

    def instanz(self, seed=None):
        return self

    def hat_fehlererkennung(self):
        return bool(self.typische_fehler)

    # --- Ausgabe ---
    def to_dict(self):
        d = {"id": self.id, "typ": self.typ, "art": self.art, "phase": self.phase,
             "kapitel": self.kapitel.slug if self.kapitel else None, "frage": self.frage,
             "tipps": list(self.tipps), "uebungsblatt": self.uebungsblatt, "punkte": self.punkte,
             "hat_rechenweg": bool(self.rechenweg), "eingabe": self.eingabe, "seed": self.seed}
        d.update(self._dict())
        return d

    def _dict(self):
        return {}

    def loesung_anzeigen(self):
        raise NotImplementedError

    # --- Prüfen ---
    def pruefen(self, antwort):
        raise NotImplementedError

    def _ergebnis(self, ok, meldung=None, **kw):
        if meldung is None:
            meldung = random.choice(LOB) if ok else "Noch nicht ganz."
        kw.setdefault("loesung", self.loesung_anzeigen())
        kw.setdefault("rechenweg", self.rechenweg)
        return Ergebnis(ok=ok, meldung=meldung, erklaerung=self.erklaerung, **kw)

    def _lesefehler(self, e):
        text = e.meldung if isinstance(e, pruefer.TermFehler) else str(e)
        return Ergebnis(ok=False, meldung=f"Das kann ich nicht lesen: {text}", lesefehler=True)

    def _typischer_fehler(self, vergleich):
        """vergleich(wert) -> bool. Liefert die Meldung des ersten passenden Fehlwerts."""
        for wert, meldung in self.typische_fehler:
            try:
                if vergleich(wert):
                    return meldung
            except (pruefer.TermFehler, ArithmeticError, ValueError, TypeError):
                continue
        return None

    def _falsch(self, vergleich, auto_hinweis=None, **kw):
        meldung = self._typischer_fehler(vergleich)
        if meldung:
            return self._ergebnis(False, "Fast! Da steckt ein typischer Fehler drin.", hinweis=meldung,
                                  fehler_erkannt=True, **kw)
        return self._ergebnis(False, hinweis=auto_hinweis, **kw)


# ──────────────────────────────────────────────────────────────────────────
#  Auswahl-Fragen
# ──────────────────────────────────────────────────────────────────────────

class MC(Frage):
    """Multiple Choice. Die ERSTE Option ist immer die richtige (wird gemischt)."""
    art = "Multiple Choice"
    typ = "mc"

    def __init__(self, frage, optionen, erklaerung="", fehler=None, **kw):
        super().__init__(frage, erklaerung, **kw)
        self.optionen = [str(o) for o in optionen]
        self.fehler = {str(k): str(v) for k, v in (fehler or {}).items()}

    def hat_fehlererkennung(self):
        return bool(self.fehler)

    def _dict(self):
        o = self.optionen[:]
        random.shuffle(o)
        return {"optionen": o}

    def loesung_anzeigen(self):
        return self.optionen[0]

    def pruefen(self, antwort):
        a = str(antwort if antwort is not None else "").strip()
        passend = [o for o in self.optionen if o.strip() == a]
        a = passend[0] if passend else a
        if a == self.optionen[0]:
            return self._ergebnis(True)
        if a in self.fehler:
            return self._ergebnis(False, "Fast! Da steckt ein typischer Fehler drin.", hinweis=self.fehler[a],
                                  fehler_erkannt=True)
        return self._ergebnis(False)


class WahrFalsch(Frage):
    art = "Wahr oder falsch?"
    typ = "wf"

    def __init__(self, aussage, wahr, erklaerung="", **kw):
        super().__init__(aussage, erklaerung, **kw)
        self.wahr = bool(wahr)

    def loesung_anzeigen(self):
        return "Wahr" if self.wahr else "Falsch"

    def pruefen(self, antwort):
        if isinstance(antwort, str):
            antwort = antwort.strip().lower() in ("w", "wahr", "true", "1", "ja", "richtig")
        return self._ergebnis(bool(antwort) == self.wahr)


def _norm_text(s):
    s = str(s).strip().lower().strip("'\"` ").rstrip(".!")
    return re.sub(r"\s+", "", s)


class Textfrage(Frage):
    art = "Antwort eintippen"
    typ = "text"
    eingabe = "text"

    def __init__(self, frage, antworten, erklaerung="", **kw):
        super().__init__(frage, erklaerung, **kw)
        self.antworten = [str(a) for a in antworten]

    def loesung_anzeigen(self):
        return self.antworten[0]

    def pruefen(self, antwort):
        a = _norm_text(antwort or "")
        if a in {_norm_text(x) for x in self.antworten}:
            return self._ergebnis(True)
        return self._falsch(lambda w: _norm_text(w) == a)


class Mehrfach(Frage):
    """Mehrfachauswahl: mehrere richtige Antworten."""
    art = "Mehrfachauswahl"
    typ = "mehrfach"

    def __init__(self, frage, richtig, falsch, erklaerung="", fehler=None, **kw):
        super().__init__(frage, erklaerung, **kw)
        self.richtig = [str(x) for x in richtig]
        self.falsch = [str(x) for x in falsch]
        self.fehler = {str(k): str(v) for k, v in (fehler or {}).items()}

    def hat_fehlererkennung(self):
        return bool(self.fehler)

    def _dict(self):
        o = self.richtig + self.falsch
        random.shuffle(o)
        return {"optionen": o}

    def loesung_anzeigen(self):
        return "Richtig sind: " + "; ".join(self.richtig) if self.richtig else "Keine der Aussagen ist richtig."

    def pruefen(self, antwort):
        gewaehlt = {str(a).strip() for a in (antwort or [])}
        details, treffer = [], 0
        for o in self.richtig + self.falsch:
            soll = o in self.richtig
            ok = (o in gewaehlt) == soll
            treffer += ok
            details.append({"name": o, "ok": ok, "soll": soll})
        n = len(details)
        if treffer == n:
            return self._ergebnis(True, details=details, teilpunkte=1.0)
        falsch_gewaehlt = [o for o in self.falsch if o in gewaehlt and o in self.fehler]
        if falsch_gewaehlt:
            return self._ergebnis(False, "Fast! Da steckt ein typischer Fehler drin.",
                                  hinweis=self.fehler[falsch_gewaehlt[0]], fehler_erkannt=True,
                                  details=details, teilpunkte=treffer / n)
        return self._ergebnis(False, f"{treffer} von {n} Entscheidungen stimmen.", details=details,
                              teilpunkte=treffer / n)


class Zuordnen(Frage):
    art = "Zuordnen"
    typ = "zuordnen"

    def __init__(self, frage, paare, erklaerung="", ablenker=(), **kw):
        super().__init__(frage, erklaerung, **kw)
        self.paare = [(str(a), str(b)) for a, b in paare]
        self.ablenker = [str(x) for x in ablenker]

    def _dict(self):
        rechts = [b for _, b in self.paare] + self.ablenker
        random.shuffle(rechts)
        return {"links": [a for a, _ in self.paare], "rechts": rechts}

    def loesung_anzeigen(self):
        return "  \n".join(f"{a} → {b}" for a, b in self.paare)

    def pruefen(self, antwort):
        if isinstance(antwort, dict):
            zuordnung = {str(k): str(v) for k, v in antwort.items()}
        else:
            zuordnung = {str(a): str(b) for a, b in (antwort or [])}
        details = [{"name": a, "ok": zuordnung.get(a) == b, "ausgabe": zuordnung.get(a, "")} for a, b in self.paare]
        richtig = sum(d["ok"] for d in details)
        if richtig == len(details):
            return self._ergebnis(True, details=details, teilpunkte=1.0)
        return self._ergebnis(False, f"{richtig} von {len(details)} Paaren stimmen.", details=details,
                              teilpunkte=richtig / len(details))


class Ordnen(Frage):
    """Rechen- oder Beweisschritte ordnen (Parsons-Prinzip), mit Ablenkern."""
    art = "Schritte ordnen"
    typ = "ordnen"

    def __init__(self, frage, schritte, erklaerung="", ablenker=(), alternativen=(), **kw):
        super().__init__(frage, erklaerung, **kw)
        self.schritte = [str(s) for s in schritte]
        self.ablenker = [str(a) for a in ablenker]
        self.alternativen = [[str(s) for s in alt] for alt in alternativen]
        self._ids = None

    def zeilen_ids(self):
        if self._ids is None:
            self._ids = {}
            for i, s in enumerate(self.schritte + self.ablenker):
                zid = hashlib.sha1(f"{self.id}|{i}|{s}".encode("utf-8")).hexdigest()[:8]
                self._ids[zid] = (s, i >= len(self.schritte))
        return self._ids

    def loesungs_ids(self):
        return list(self.zeilen_ids())[:len(self.schritte)]

    def _dict(self):
        z = [{"zeilen_id": k, "text": t} for k, (t, _) in self.zeilen_ids().items()]
        random.shuffle(z)
        return {"zeilen": z, "anzahl": len(self.schritte)}

    def loesung_anzeigen(self):
        return "\n".join(f"{i}. {s}" for i, s in enumerate(self.schritte, 1))

    def pruefen(self, antwort):
        ids = self.zeilen_ids()
        antwort = [str(a) for a in (antwort or [])]
        if any(a not in ids for a in antwort):
            return Ergebnis(False, "Unbekannter Schritt in der Antwort.", lesefehler=True)
        gewaehlt = [ids[a][0] for a in antwort]
        details = []
        for i, a in enumerate(antwort):
            text, ablenker = ids[a]
            soll = self.schritte[i] if i < len(self.schritte) else None
            details.append({"name": f"Schritt {i + 1}", "ok": not ablenker and text == soll, "ausgabe": text,
                            "meldung": "gehört nicht in die Lösung" if ablenker else ""})
        if gewaehlt == self.schritte or gewaehlt in self.alternativen:
            for d in details:
                d["ok"] = True
            return self._ergebnis(True, details=details)
        abl = [ids[a][0] for a in antwort if ids[a][1]]
        if abl:
            return self._ergebnis(False, f"Der Schritt „{abl[0]}“ gehört nicht in die Lösung.", details=details)
        if len(gewaehlt) != len(self.schritte):
            return self._ergebnis(False, f"Es gehören genau {len(self.schritte)} Schritte in die Lösung.",
                                  details=details)
        richtig = sum(d["ok"] for d in details)
        return self._ergebnis(False, f"{richtig} von {len(self.schritte)} Schritten stehen an der richtigen Stelle.",
                              details=details)


# ──────────────────────────────────────────────────────────────────────────
#  Rechen-Fragen
# ──────────────────────────────────────────────────────────────────────────

def _auto_hinweis_zahl(ist, soll):
    """Allgemeine Fehlerdiagnose, wenn kein typischer Fehler hinterlegt ist."""
    try:
        if soll != 0 and pruefer.gleich(ist, -soll):
            return "Der Betrag stimmt, aber das **Vorzeichen** nicht. Prüfe Plus und Minus."
        if ist != 0 and soll != 0 and pruefer.gleich(F(1) / F(ist) if not isinstance(ist, float) else 1 / ist, soll):
            return "Dein Ergebnis ist genau der **Kehrwert**. Hast du Zähler und Nenner vertauscht?"
        for f in (10, 100, 1000):
            if soll != 0 and (pruefer.gleich(ist, soll * f) or pruefer.gleich(ist * f, soll)):
                return "Die Ziffern stimmen, aber das **Komma** sitzt an der falschen Stelle (Faktor 10, 100 oder 1000)."
        if soll != 0 and abs(float(ist) - float(soll)) <= 0.01 * abs(float(soll)):
            return "Sehr nah dran! Vermutlich hast du zu früh **gerundet**. Rechne mit Brüchen bis zum Schluss."
    except (ZeroDivisionError, TypeError, ValueError, OverflowError):
        pass
    return None


class Zahlfrage(Frage):
    """Ergebnis ist eine Zahl (ganz, Bruch, Dezimalzahl, auch √2 oder π)."""
    art = "Zahl eingeben"
    typ = "zahl"
    eingabe = "zahl"

    def __init__(self, frage, loesung, erklaerung="", toleranz=None, gekuerzt=False, einheit=None, form=None, **kw):
        super().__init__(frage, erklaerung, **kw)
        self.form = form            # "bruch": Antwort muss als Bruch (oder ganze Zahl) dastehen
        self.loesung_roh = loesung
        t = pruefer.parse(_als_text(loesung))
        if t.variablen:
            raise ValueError(f"Lösung {loesung!r} enthält Variablen")
        self.soll_ast = t.ast
        self.soll = pruefer.wert(t.ast)
        self.toleranz = toleranz
        self.gekuerzt = gekuerzt
        self.einheit = einheit

    def _dict(self):
        return {"einheit": self.einheit, "gekuerzt": self.gekuerzt, "form": self.form,
                "toleranz": self.toleranz}

    def loesung_anzeigen(self):
        if isinstance(self.soll, Fraction) and self.form == "dezimal":
            s = mathlib.dezimal(self.soll, 6)
        elif isinstance(self.soll, Fraction):
            s = mathlib.tex(self.soll)
        else:
            s = pruefer.zu_latex(self.soll_ast)
            if isinstance(self.soll, float):
                s += f" \\approx {mathlib.dezimal(self.soll, 4)}"
        return f"${s}$" + (f" {self.einheit}" if self.einheit else "")

    def _gleich(self, ist, soll):
        if self.toleranz is not None:
            return abs(float(ist) - float(soll)) <= float(self.toleranz) + 1e-12
        return pruefer.gleich(ist, soll)

    def pruefen(self, antwort):
        text = str(antwort or "").strip()
        if self.einheit:
            text = re.sub(re.escape(self.einheit) + r"\s*$", "", text).strip()
        if not text:
            return Ergebnis(False, "Bitte gib zuerst eine Zahl ein.", lesefehler=True)
        try:
            _, ist = pruefer.zahl_parsen(text)
        except (pruefer.TermFehler, pruefer.Undefiniert) as e:
            return self._lesefehler(e)
        if self._gleich(ist, self.soll):
            if self.form == "dezimal" and not re.fullmatch(r"\s*-?\s*\d*[.,]?\d+\s*", text):
                return self._ergebnis(False, "Fast!", hinweis="Der Wert stimmt. Gesucht ist aber die **Kommazahl**, "
                                                              "z. B. 0,75.", fast=True)
            if self.form == "bruch" and not _ist_bruch_eingabe(text):
                return self._ergebnis(False, "Fast!", hinweis="Der Wert stimmt. Gesucht ist aber ein **Bruch**, "
                                                              "also Zähler / Nenner, z. B. 3/4.", fast=True)
            if self.gekuerzt:
                m = pruefer.bruch_gekuerzt(text)
                if m:
                    return self._ergebnis(False, "Fast!", hinweis=m, fast=True)
            return self._ergebnis(True)

        gerundet = bool(re.search(r"\d[.,]\d{2,}", text))

        def vergleich(w):
            fw = pruefer.zahl_parsen(_als_text(w))[1]
            if self._gleich(ist, fw):
                return True
            # gerundet eingegeben (z. B. 1,333 für 4/3): auf 3 Nachkommastellen genau zählt als derselbe Fehler
            return gerundet and abs(float(ist) - float(fw)) <= 5e-4 * max(1.0, abs(float(fw)))
        return self._falsch(vergleich, _auto_hinweis_zahl(ist, self.soll))


def _ist_bruch_eingabe(text):
    """True für '3/4', '-3/4', '(-3)/4', '7' – nicht für '0,75'."""
    try:
        a = pruefer.parse(text).ast
    except pruefer.TermFehler:
        return False
    while a[0] == "neg":
        a = a[1]
    def ganz(k):
        while k[0] == "neg":
            k = k[1]
        return k[0] == "zahl" and k[1].denominator == 1 and "," not in k[2] and "." not in k[2]
    return ganz(a) or (a[0] == "div" and ganz(a[1]) and ganz(a[2]))


def _ist_zahl_text(x):
    try:
        pruefer.zahl_parsen(_als_text(x))
        return True
    except (pruefer.TermFehler, ArithmeticError, ValueError):
        return False


def _gleich_als_term(a, b):
    try:
        ta, tb = pruefer.parse(_als_text(a)), pruefer.parse(_als_text(b))
        if not ta.variablen and not tb.variablen:
            return pruefer.gleich(pruefer.wert(ta.ast), pruefer.wert(tb.ast))
        return pruefer.aequivalent(ta.ast, tb.ast).ok
    except (pruefer.TermFehler, pruefer.Undefiniert, ArithmeticError):
        return _norm_text(_als_text(a)) == _norm_text(_als_text(b))


def ohne_gleiche(loesung, fehler):
    """Für Generatoren: entfernt Fehlwerte, die zufällig gleich der Lösung sind (oder doppelt).
    Funktioniert für Zahlen, Terme und für Lückentexte (Lösung und Fehlwerte als Listen je Lücke)."""
    if isinstance(loesung, (list, tuple)) or not _ist_zahl_text(loesung):
        def gleich(x, y):
            if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
                return len(x) == len(y) and all(_gleich_als_term(p, q) for p, q in zip(x, y))
            return _gleich_als_term(x, y)
        erg = []
        for w, m in fehler:
            if gleich(w, loesung) or any(gleich(w, g) for g, _ in erg):
                continue
            erg.append((w, m))
        return erg
    soll = pruefer.zahl_parsen(_als_text(loesung))[1]
    erg, gesehen = [], []
    for w, m in fehler:
        try:
            v = pruefer.zahl_parsen(_als_text(w))[1]
        except (pruefer.TermFehler, ArithmeticError):
            continue
        if pruefer.gleich(v, soll) or any(pruefer.gleich(v, g) for g in gesehen):
            continue
        gesehen.append(v)
        erg.append((w, m))
    return erg


class Termfrage(Frage):
    """Term eingeben; Prüfung auf Äquivalenz (+ optionaler Formcheck)."""
    art = "Term eingeben"
    typ = "term"
    eingabe = "term"

    def __init__(self, frage, loesung, erklaerung="", variablen=None, form=None, **kw):
        super().__init__(frage, erklaerung, **kw)
        self.variablen = [v.strip() for v in variablen.split(",")] if isinstance(variablen, str) else list(variablen or [])
        self.soll_term = pruefer.parse(_als_text(loesung), self.variablen or None)
        if not self.variablen:
            self.variablen = sorted(self.soll_term.variablen)
        self.form = form

    def _dict(self):
        return {"variablen": self.variablen, "form": self.form}

    def loesung_anzeigen(self):
        return f"${self.soll_term.latex()}$"

    def pruefen(self, antwort):
        text = str(antwort or "").strip()
        if not text:
            return Ergebnis(False, "Bitte gib zuerst einen Term ein.", lesefehler=True)
        try:
            t = pruefer.parse(text, self.variablen)
        except pruefer.TermFehler as e:
            return self._lesefehler(e)
        fremd = t.variablen - set(self.variablen)
        if fremd:
            v = ", ".join(sorted(fremd))
            return Ergebnis(False, f"In deinem Term steht {v}, aber hier kommen nur {', '.join(self.variablen)} vor. "
                                   "Tippfehler?", lesefehler=True)
        v = pruefer.aequivalent(t.ast, self.soll_term.ast, self.variablen)
        if v.ok:
            m = pruefer.form_pruefen(t, self.form, self.soll_term.ast)
            if m:
                return self._ergebnis(False, "Fast!", hinweis=m, fast=True)
            return self._ergebnis(True)

        def vergleich(w):
            return pruefer.aequivalent(t.ast, pruefer.parse(_als_text(w), self.variablen).ast, self.variablen).ok
        auto = None
        if v.grund == "definitionsbereich":
            auto = "Dein Term passt an vielen Stellen nicht, an denen die Lösung definiert ist."
        elif v.stelle:
            stelle = ", ".join(f"{k} = {mathlib.text(w) if not isinstance(w, float) else round(w, 3)}"
                               for k, w in v.stelle.items())
            try:
                neg = pruefer.aequivalent(("neg", t.ast), self.soll_term.ast, self.variablen).ok
            except Exception:  # noqa: BLE001
                neg = False
            if neg:
                auto = "Fast alles stimmt, nur das **Vorzeichen** des ganzen Terms ist umgedreht."
            else:
                auto = (f"Probe: Setze {stelle} ein. Dein Term ergibt "
                        f"{_wert_text(v.ist)}, richtig wäre {_wert_text(v.soll)}.")
        return self._falsch(vergleich, auto)


def _wert_text(w):
    if isinstance(w, Fraction):
        return f"${mathlib.tex(w)}$"
    return f"$\\approx {mathlib.dezimal(w, 4)}$"


class Loesungsmengefrage(Frage):
    """Lösungsmenge: Punkte, Intervalle, Vereinigungen, leer, ℝ."""
    art = "Lösungsmenge"
    typ = "loesungsmenge"
    eingabe = "bereich"

    def __init__(self, frage, loesung, erklaerung="", variable="x", **kw):
        super().__init__(frage, erklaerung, **kw)
        self.variable = variable
        self.soll = loesung if isinstance(loesung, list) else pruefer.bereich_parsen(_als_text(loesung), variable)

    def _dict(self):
        return {"variable": self.variable}

    def loesung_anzeigen(self):
        return f"$\\mathbb{{L}} = {pruefer.bereich_latex(self.soll)}$"

    def pruefen(self, antwort):
        text = str(antwort or "").strip()
        if not text:
            return Ergebnis(False, "Bitte gib eine Lösungsmenge ein (z. B. {2; -3}, [0; 4) oder keine).",
                            lesefehler=True)
        try:
            ist = pruefer.bereich_parsen(text, self.variable)
        except (pruefer.TermFehler, pruefer.Undefiniert) as e:
            return self._lesefehler(e)
        if pruefer.bereiche_gleich(ist, self.soll):
            return self._ergebnis(True)

        def vergleich(w):
            return pruefer.bereiche_gleich(ist, pruefer.bereich_parsen(_als_text(w), self.variable))
        return self._falsch(vergleich, self._diagnose(ist, text))

    def _diagnose(self, ist, text):
        soll = self.soll
        if all(i.punkt() for i in ist + soll) and soll:
            sp = [i.lo for i in soll]
            ip = [i.lo for i in ist]
            fehlt = [p for p in sp if not any(pruefer.gleich_grenze(p, q) for q in ip)]
            zuviel = [p for p in ip if not any(pruefer.gleich_grenze(p, q) for q in sp)]
            if fehlt and not zuviel:
                return f"Deine Werte stimmen, aber es {'fehlt eine Lösung' if len(fehlt) == 1 else 'fehlen Lösungen'}."
            if zuviel and not fehlt:
                return "Eine deiner Zahlen ist keine Lösung. Mach die Probe durch Einsetzen."
        if len(ist) == len(soll) and all(pruefer.gleich_grenze(a.lo, b.lo) and pruefer.gleich_grenze(a.hi, b.hi)
                                         for a, b in zip(ist, soll)):
            return "Die Grenzen stimmen. Prüfe, ob sie **dazugehören** (eckige Klammer) oder nicht (runde Klammer)."
        if not soll and ist:
            return "Prüfe, ob es überhaupt eine Lösung gibt. Setze deine Zahl zur Probe ein."
        if "," in text and ";" not in text and re.search(r"\d,\d", text):
            return "Kommazahlen und Trennzeichen: Trenne Elemente mit ; wenn du ein Dezimalkomma benutzt."
        return None


class Mengefrage(Frage):
    art = "Menge angeben"
    typ = "menge"
    eingabe = "menge"

    def __init__(self, frage, loesung, erklaerung="", **kw):
        super().__init__(frage, erklaerung, **kw)
        self.soll = pruefer.menge_parsen(loesung) if isinstance(loesung, str) else \
            [("zahl", F(x)) if isinstance(x, (int, Fraction)) else pruefer._element_wert(str(x), True) for x in loesung]

    def loesung_anzeigen(self):
        return f"${pruefer.menge_latex(self.soll)}$"

    def pruefen(self, antwort):
        text = str(antwort or "").strip()
        if not text:
            return Ergebnis(False, "Bitte gib eine Menge ein, z. B. {1; 2; 3}.", lesefehler=True)
        try:
            ist = pruefer.menge_parsen(text)
        except (pruefer.TermFehler, pruefer.Undefiniert) as e:
            return self._lesefehler(e)
        a, b = pruefer.menge_schluessel(ist), pruefer.menge_schluessel(self.soll)
        if a == b:
            hinweis = None
            if len(ist) != len(a):
                hinweis = "Kleiner Hinweis: In einer Menge zählt jedes Element nur einmal. Doppelte kannst du weglassen."
            return self._ergebnis(True, hinweis=hinweis)

        def vergleich(w):
            return pruefer.menge_schluessel(pruefer.menge_parsen(_als_text(w))) == a
        auto = None
        if a < b:
            auto = f"Alle deine Elemente gehören dazu, aber es fehlen noch {len(b - a)}."
        elif a > b:
            auto = f"{len(a - b)} deiner Elemente gehören nicht in die Menge."
        if "," in text and ";" not in text and re.search(r"\d,\d", text):
            auto = ((auto + " ") if auto else "") + ("Achtung: Ohne ; liest das System jedes Komma als "
                                                     "Trennzeichen. Für Kommazahlen trenne Elemente mit ;.")
        return self._falsch(vergleich, auto)


def _zelle(text, variablen=None):
    t = pruefer.parse(str(text), variablen)
    return t


class Vektorfrage(Frage):
    art = "Vektor angeben"
    typ = "vektor"
    eingabe = "vektor"

    def __init__(self, frage, loesung, erklaerung="", vielfaches=False, **kw):
        super().__init__(frage, erklaerung, **kw)
        self.soll = [pruefer.zahl_parsen(_als_text(x))[1] for x in loesung]
        self.vielfaches = vielfaches

    def _dict(self):
        return {"zeilen": len(self.soll), "spalten": 1, "vielfaches": self.vielfaches}

    def loesung_anzeigen(self):
        return f"${mathlib.tex_vektor(self.soll)}$" + (" (oder ein Vielfaches ≠ 0)" if self.vielfaches else "")

    def _werte(self, antwort):
        zellen = list(antwort or [])
        if len(zellen) != len(self.soll) or any(not str(z).strip() for z in zellen):
            raise pruefer.TermFehler("Bitte fülle alle Felder aus.")
        return [pruefer.zahl_parsen(str(z))[1] for z in zellen]

    def pruefen(self, antwort):
        try:
            ist = self._werte(antwort)
        except (pruefer.TermFehler, pruefer.Undefiniert) as e:
            return self._lesefehler(e)
        if self.vielfaches:
            ok = _proportional(ist, self.soll)
            details = []
        else:
            details = [{"name": f"Eintrag {i + 1}", "ok": pruefer.gleich(a, b)} for i, (a, b) in enumerate(zip(ist, self.soll))]
            ok = all(d["ok"] for d in details)
        if ok:
            return self._ergebnis(True, details=details)

        def vergleich(w):
            ww = [pruefer.zahl_parsen(_als_text(x))[1] for x in w]
            return all(pruefer.gleich(a, b) for a, b in zip(ist, ww))
        auto = None
        if not self.vielfaches and _proportional(ist, self.soll):
            auto = "Dein Vektor zeigt in die richtige Richtung, hat aber die falsche Länge."
        elif all(not pruefer.gleich(a, 0) for a in ist) and all(pruefer.gleich(a, -b) for a, b in zip(ist, self.soll)):
            auto = "Alle Vorzeichen sind umgedreht."
        return self._falsch(vergleich, auto, details=details)


def _proportional(a, b):
    if all(pruefer.gleich(x, 0) for x in a):
        return False
    faktor = None
    for x, y in zip(a, b):
        if pruefer.gleich(y, 0):
            if not pruefer.gleich(x, 0):
                return False
            continue
        f = x / y if not isinstance(x, float) and not isinstance(y, float) else float(x) / float(y)
        if faktor is None:
            faktor = f
        elif not pruefer.gleich(f, faktor):
            return False
    return faktor is not None


class Matrixfrage(Frage):
    art = "Matrix angeben"
    typ = "matrix"
    eingabe = "matrix"

    def __init__(self, frage, loesung, erklaerung="", **kw):
        super().__init__(frage, erklaerung, **kw)
        self.soll = [[pruefer.zahl_parsen(_als_text(x))[1] for x in z] for z in loesung]

    def _dict(self):
        return {"zeilen": len(self.soll), "spalten": len(self.soll[0])}

    def loesung_anzeigen(self):
        return f"${mathlib.tex_matrix(self.soll)}$"

    def pruefen(self, antwort):
        try:
            zeilen = list(antwort or [])
            if len(zeilen) != len(self.soll) or any(len(z) != len(self.soll[0]) for z in zeilen):
                raise pruefer.TermFehler("Die Matrix hat nicht die richtige Größe.")
            if any(not str(c).strip() for z in zeilen for c in z):
                raise pruefer.TermFehler("Bitte fülle alle Felder aus.")
            ist = [[pruefer.zahl_parsen(str(c))[1] for c in z] for z in zeilen]
        except (pruefer.TermFehler, pruefer.Undefiniert) as e:
            return self._lesefehler(e)
        details = [{"name": f"Zeile {i + 1}, Spalte {j + 1}", "ok": pruefer.gleich(a, b), "pos": [i, j]}
                   for i, (za, zb) in enumerate(zip(ist, self.soll)) for j, (a, b) in enumerate(zip(za, zb))]
        if all(d["ok"] for d in details):
            return self._ergebnis(True, details=details)

        def vergleich(w):
            return all(pruefer.gleich(a, pruefer.zahl_parsen(_als_text(b))[1])
                       for za, zb in zip(ist, w) for a, b in zip(za, zb))
        auto = None
        if len(self.soll) == len(self.soll[0]) and all(pruefer.gleich(ist[i][j], self.soll[j][i])
                                                       for i in range(len(ist)) for j in range(len(ist))):
            auto = "Deine Matrix ist genau die **transponierte** Lösung: Zeilen und Spalten sind vertauscht."
        richtig = sum(d["ok"] for d in details)
        return self._falsch_mit_zaehler(vergleich, auto, details, richtig)

    def _falsch_mit_zaehler(self, vergleich, auto, details, richtig):
        e = self._falsch(vergleich, auto, details=details)
        if not e.fehler_erkannt:
            e.meldung = f"{richtig} von {len(details)} Einträgen stimmen."
        return e


PARAMETER = ("s", "t", "r", "u")


class LGSFrage(Frage):
    """Lineares Gleichungssystem A·x = b. Lösung wird von mathlib.gauss berechnet.

    Antwort: {"keine": bool, "werte": [str, ...]} – Einträge dürfen Parameter s, t, r, u enthalten."""
    art = "Gleichungssystem lösen"
    typ = "lgs"
    eingabe = "lgs"

    def __init__(self, frage, a, b, erklaerung="", variablen=None, **kw):
        super().__init__(frage, erklaerung, **kw)
        self.a, self.b = mathlib.matrix(a), [F(x) for x in b]
        self.n = len(self.a[0])
        self.variablen = variablen or (["x", "y", "z"][:self.n] if self.n <= 3 else [f"x_{i + 1}" for i in range(self.n)])
        self.loesung = mathlib.lgs_loesen(self.a, self.b)

    def _dict(self):
        return {"zeilen": self.n, "variablen": self.variablen, "parameter": list(PARAMETER)}

    def loesung_anzeigen(self):
        l = self.loesung
        if l["art"] == "keine":
            return "Das System hat **keine Lösung**: $\\mathbb{L} = \\emptyset$."
        if l["art"] == "eindeutig":
            return f"Genau eine Lösung: ${mathlib.tex_vektor(l['x'])}$"
        teile = mathlib.tex_vektor(l["x"])
        for p, r in zip(PARAMETER, l["richtungen"]):
            teile += f" + {p} \\cdot {mathlib.tex_vektor(r)}"
        params = ", ".join(PARAMETER[:len(l["richtungen"])])
        return f"Unendlich viele Lösungen: $\\vec x = {teile}$ mit ${params} \\in \\mathbb{{R}}$"

    def pruefen(self, antwort):
        antwort = antwort or {}
        if antwort.get("keine"):
            if self.loesung["art"] == "keine":
                return self._ergebnis(True)
            return self._ergebnis(False, hinweis="Das System **hat** Lösungen. Prüfe deine Zeilenumformungen noch einmal.")
        if self.loesung["art"] == "keine":
            return self._ergebnis(False, hinweis="Mach die Probe: Erfüllt dein Vektor wirklich **alle** Gleichungen? "
                                                 "Im Gauß-Verfahren entsteht hier eine Zeile 0 = (Zahl ≠ 0).")
        zellen = list(antwort.get("werte") or [])
        if len(zellen) != self.n or any(not str(z).strip() for z in zellen):
            return Ergebnis(False, "Bitte fülle alle Felder aus.", lesefehler=True)
        try:
            terme = [pruefer.parse(str(z), list(PARAMETER)).ast for z in zellen]
        except pruefer.TermFehler as e:
            return self._lesefehler(e)
        params = sorted(set().union(*[pruefer.variablen_von(t) for t in terme]))
        fremd = set(params) - set(PARAMETER)
        if fremd:
            return Ergebnis(False, f"Als Parameter sind nur {', '.join(PARAMETER)} erlaubt, nicht {', '.join(fremd)}.",
                            lesefehler=True)
        try:
            ok, grund = self._parametrisch_pruefen(terme, params)
        except (pruefer.Undefiniert, ArithmeticError) as e:
            return self._lesefehler(str(e))
        if ok:
            return self._ergebnis(True)

        def vergleich(w):
            return all(pruefer.gleich(pruefer.wert(t, {p: F(0) for p in params}), pruefer.zahl_parsen(_als_text(x))[1])
                       for t, x in zip(terme, w))
        return self._falsch(vergleich, grund)

    def _parametrisch_pruefen(self, terme, params):
        def auswerten(bel):
            return [pruefer.wert(t, bel) for t in terme]
        null = {p: F(0) for p in params}
        p0 = auswerten(null)
        if any(isinstance(x, float) for x in p0):
            return False, "Die Lösung besteht hier aus Brüchen. Rechne exakt, ohne zu runden."
        richtungen = []
        for p in params:
            e = dict(null, **{p: F(1)})
            richtungen.append([a - b for a, b in zip(auswerten(e), p0)])
        # affin? Test an Zufallsstellen
        rng = random.Random(7)
        for _ in range(4):
            bel = {p: F(rng.randint(-5, 5), rng.randint(1, 4)) for p in params}
            erwartet = [x + sum(bel[p] * r[i] for p, r in zip(params, richtungen)) for i, x in enumerate(p0)]
            if auswerten(bel) != erwartet:
                return False, "Deine Einträge müssen lineare Ausdrücke in den Parametern sein, z. B. 2 + 3t."
        if mathlib.mat_vec(self.a, p0) != self.b:
            return False, "Mach die Probe: Setze deine Lösung (mit Parameter = 0) in die Gleichungen ein, mindestens eine geht nicht auf."
        for r in richtungen:
            if any(x != 0 for x in mathlib.mat_vec(self.a, r)):
                return False, "Dein Lösungsvektor erfüllt die Gleichungen nicht für jeden Parameterwert."
        anzahl_frei = len(self.loesung["richtungen"])
        if richtungen and mathlib.rang(richtungen) < len(richtungen):
            return False, "Zwei deiner Parameter-Richtungen sind voneinander abhängig."
        if len(richtungen) < anzahl_frei:
            if not richtungen:
                return False, ("Dein Vektor ist **eine** Lösung, aber es gibt unendlich viele. "
                               "Gib die allgemeine Lösung mit Parameter an (z. B. t).")
            return False, "Es gibt mehr freie Variablen. Du brauchst noch einen weiteren Parameter."
        return True, None


class Luecke(Frage):
    """Formel mit Lücken (\\luecke im LaTeX). Jede Lücke: Liste akzeptierter Werte."""
    art = "Lücken füllen"
    typ = "luecke"
    eingabe = "term"

    def __init__(self, frage, formel, antworten, erklaerung="", formen=None, **kw):
        super().__init__(frage, erklaerung, **kw)
        self.formel = formel
        self.antworten = [[_als_text(a) for a in (x if isinstance(x, (list, tuple)) else [x])] for x in antworten]
        # formen: je Lücke None oder ein Formcheck wie bei Termfragen ("gekuerzt", "wurzel_vereinfacht", …)
        self.formen = list(formen) if formen else [None] * len(self.antworten)

    def haupttext(self):
        return self.frage + "\n" + self.formel

    def anzahl(self):
        return self.formel.count("\\luecke")

    def _dict(self):
        return {"formel": self.formel, "anzahl_luecken": self.anzahl()}

    def loesung_anzeigen(self):
        teile = self.formel.split("\\luecke")
        s = teile[0]
        for i, rest in enumerate(teile[1:]):
            wert = self.antworten[i][0]
            try:
                wert = pruefer.zu_latex(pruefer.parse(wert).ast)
            except pruefer.TermFehler:
                pass
            s += "\\boxed{" + wert + "}" + rest
        return f"${s}$"

    @staticmethod
    def _passt(eingabe, akzeptiert):
        for a in akzeptiert:
            try:
                ta, te = pruefer.parse(a), pruefer.parse(eingabe)
                if not ta.variablen and not te.variablen:
                    if pruefer.gleich(pruefer.wert(te.ast), pruefer.wert(ta.ast)):
                        return True
                elif pruefer.aequivalent(te.ast, ta.ast).ok:
                    return True
            except (pruefer.TermFehler, pruefer.Undefiniert):
                if _norm_text(a) == _norm_text(eingabe):
                    return True
        return False

    def pruefen(self, antwort):
        eingaben = [str(x) for x in (antwort or [])]
        if len(eingaben) != self.anzahl() or any(not e.strip() for e in eingaben):
            return Ergebnis(False, f"Bitte fülle alle {self.anzahl()} Lücken aus.", lesefehler=True)
        details = [{"name": f"Lücke {i + 1}", "ok": self._passt(e, a)} for i, (e, a) in enumerate(zip(eingaben, self.antworten))]
        richtig = sum(d["ok"] for d in details)
        if richtig == len(details):
            for i, (e, form) in enumerate(zip(eingaben, self.formen)):
                if not form:
                    continue
                try:
                    t = pruefer.parse(e)
                except pruefer.TermFehler:
                    continue
                m = (pruefer.bruch_gekuerzt(e) if form == "gekuerzt" and not t.variablen
                     else pruefer.form_pruefen(t, form, pruefer.parse(self.antworten[i][0]).ast))
                if m:
                    return self._ergebnis(False, "Fast!", hinweis=f"Lücke {i + 1}: {m}", fast=True, details=details)
            return self._ergebnis(True, details=details)

        def vergleich(w):
            return all(self._passt(e, [_als_text(x)]) for e, x in zip(eingaben, w))
        e = self._falsch(vergleich, None, details=details)
        if not e.fehler_erkannt:
            e.meldung = f"{richtig} von {len(details)} Lücken stimmen."
        return e


class GraphPunkt(Frage):
    """Punkt im Koordinatensystem setzen (modus='setzen') oder Wert ablesen (modus='ablesen')."""
    art = "Am Graphen arbeiten"
    typ = "graph_punkt"
    eingabe = "punkt"

    def __init__(self, frage, visual, ziel=None, loesung=None, modus="setzen", toleranz=0.25,
                 erklaerung="", raster=0.5, **kw):
        super().__init__(frage, erklaerung, **kw)
        from . import visuals
        self.visual = visuals.ergaenzen("funktionsgraph", dict(visual)) if visual.get("funktionen") else dict(visual)
        self.modus = modus
        self.toleranz = toleranz
        self.raster = raster
        if modus == "setzen":
            self.ziel = (F(ziel[0]), F(ziel[1]))
        else:
            self.soll = pruefer.zahl_parsen(_als_text(loesung))[1]

    def haupttext(self):
        return self.frage + self.modus

    def _dict(self):
        return {"visual": self.visual, "modus": self.modus, "raster": self.raster,
                "eingabe": "punkt" if self.modus == "setzen" else "zahl"}

    def loesung_anzeigen(self):
        if self.modus == "setzen":
            return f"$P({mathlib.tex(self.ziel[0])} \\mid {mathlib.tex(self.ziel[1])})$"
        return f"${mathlib.tex(self.soll)}$"

    def pruefen(self, antwort):
        try:
            if self.modus == "setzen":
                x, y = (float(pruefer.zahl_parsen(str(v))[1]) for v in antwort)
                ok = abs(x - float(self.ziel[0])) <= self.toleranz and abs(y - float(self.ziel[1])) <= self.toleranz
                if ok:
                    return self._ergebnis(True)
                auto = None
                if abs(x - float(self.ziel[1])) <= self.toleranz and abs(y - float(self.ziel[0])) <= self.toleranz:
                    auto = "Du hast x und y **vertauscht**. Erst nach rechts (x), dann nach oben (y)."
                return self._falsch(lambda w: abs(x - float(F(w[0]))) <= self.toleranz
                                    and abs(y - float(F(w[1]))) <= self.toleranz, auto)
            _, ist = pruefer.zahl_parsen(str(antwort))
        except (pruefer.TermFehler, pruefer.Undefiniert, TypeError, ValueError) as e:
            return self._lesefehler(e)
        if abs(float(ist) - float(self.soll)) <= self.toleranz:
            return self._ergebnis(True)
        return self._falsch(lambda w: abs(float(ist) - float(pruefer.zahl_parsen(_als_text(w))[1])) <= self.toleranz,
                            _auto_hinweis_zahl(ist, self.soll))


class Papier(Frage):
    """Auf Papier lösen, dann Musterlösung + Checkliste zur Selbstbewertung."""
    art = "Auf Papier lösen"
    typ = "papier"

    def __init__(self, aufgabe, musterloesung, checkliste, erklaerung="", **kw):
        kw.setdefault("punkte", len(checkliste))
        super().__init__(aufgabe, erklaerung, **kw)
        self.musterloesung = _dedent(musterloesung)
        self.checkliste = [str(c) for c in checkliste]
        self.rechenweg = self.rechenweg or self.musterloesung

    def _dict(self):
        return {"anzahl_punkte": len(self.checkliste)}

    def loesung_anzeigen(self):
        return self.musterloesung

    def bewertung_dict(self):
        """Musterlösung + Checkliste (erst nach 'Ich bin fertig')."""
        return {"musterloesung": self.musterloesung, "checkliste": self.checkliste}

    def pruefen(self, antwort):
        haken = [bool(x) for x in (antwort or [])]
        if len(haken) != len(self.checkliste):
            return Ergebnis(False, "Bitte bewerte jeden Punkt der Checkliste.", lesefehler=True)
        n = sum(haken)
        details = [{"name": c, "ok": h} for c, h in zip(self.checkliste, haken)]
        if n == len(haken):
            return self._ergebnis(True, "Alles abgehakt – stark!", details=details, teilpunkte=1.0)
        return self._ergebnis(False, f"{n} von {len(haken)} Punkten geschafft. Schau dir die offenen Punkte "
                                     "in der Musterlösung noch einmal an.", details=details, teilpunkte=n / len(haken))


# ──────────────────────────────────────────────────────────────────────────
#  Rechenweg (mehrere Teilschritte) und Generator
# ──────────────────────────────────────────────────────────────────────────

def frage_aus_dict(typ, d):
    """Baut eine konkrete Frage aus einem Dict (für Generatoren und Rechenweg-Schritte)."""
    d = dict(d)
    frage = d.pop("frage", "")
    if typ == "zahl":
        return Zahlfrage(frage, d.pop("loesung"), **d)
    if typ == "term":
        return Termfrage(frage, d.pop("loesung"), **d)
    if typ == "loesungsmenge":
        return Loesungsmengefrage(frage, d.pop("loesung"), **d)
    if typ == "menge":
        return Mengefrage(frage, d.pop("loesung"), **d)
    if typ == "vektor":
        return Vektorfrage(frage, d.pop("loesung"), **d)
    if typ == "matrix":
        return Matrixfrage(frage, d.pop("loesung"), **d)
    if typ == "lgs":
        return LGSFrage(frage, d.pop("a"), d.pop("b"), **d)
    if typ == "mc":
        return MC(frage, d.pop("optionen"), **d)
    if typ == "wf":
        return WahrFalsch(frage, d.pop("wahr"), **d)
    if typ == "text":
        return Textfrage(frage, d.pop("antworten"), **d)
    if typ == "mehrfach":
        return Mehrfach(frage, d.pop("richtig"), d.pop("falsch"), **d)
    if typ == "luecke":
        return Luecke(frage, d.pop("formel"), d.pop("antworten"), **d)
    if typ == "ordnen":
        return Ordnen(frage, d.pop("schritte"), **d)
    raise ValueError(f"Unbekannter Fragetyp {typ!r}")


class Rechenweg(Frage):
    """Aufgabe in 2 bis 5 Teilschritten; jeder Schritt wird einzeln geprüft (Teilpunkte).

    Antwort: {"schritt": i, "antwort": ...}. Nach jedem Schritt zeigt die Oberfläche den
    richtigen Wert, damit Folgefehler nicht weiterwandern."""
    art = "Schritt für Schritt rechnen"
    typ = "rechenweg"

    def __init__(self, frage, schritte, erklaerung="", **kw):
        kw.setdefault("punkte", len(schritte))
        super().__init__(frage, erklaerung, **kw)
        self.schritte = []
        for s in schritte:
            s = dict(s)
            typ = s.pop("typ", "zahl")
            q = frage_aus_dict(typ, s)
            self.schritte.append(q)

    def hat_fehlererkennung(self):
        return any(s.hat_fehlererkennung() for s in self.schritte)

    def _dict(self):
        return {"schritte": [dict(s.to_dict(), id=None, kapitel=None) for s in self.schritte]}

    def loesung_anzeigen(self):
        return "\n".join(f"{i}. {s.frage} {s.loesung_anzeigen()}" for i, s in enumerate(self.schritte, 1))

    def pruefen(self, antwort):
        antwort = antwort or {}
        try:
            i = int(antwort.get("schritt", 0))
        except (TypeError, ValueError):
            i = -1
        if not 0 <= i < len(self.schritte):
            return Ergebnis(False, "Unbekannter Schritt.", lesefehler=True)
        s = self.schritte[i]
        e = s.pruefen(antwort.get("antwort"))
        e.details = [{"schritt": i, "von": len(self.schritte)}] + list(e.details)
        e.loesung = s.loesung_anzeigen()
        if i == len(self.schritte) - 1:
            e.rechenweg = self.rechenweg
        else:
            e.rechenweg = s.rechenweg
        return e


class Generator(Frage):
    """Parametrisierte Aufgabe: fn(rng) -> dict mit frage, loesung, rechenweg, tipps, typische_fehler, ...

    Die ID hängt nur am Funktionsnamen. Jede Instanz hat einen seed; der Server baut die
    Aufgabe zum Prüfen aus dem seed neu (zustandslos, Lösung bleibt auf dem Server)."""
    art = "Übungsmaschine"
    typ = "generator"

    def __init__(self, fn, typ="zahl", titel="", glatt=False, probe=None, **kw):
        super().__init__(titel or fn.__name__, kw.pop("erklaerung", ""), **kw)
        self.fn = fn
        self.ziel_typ = typ
        self.titel = titel
        self.glatt = glatt
        self.probe = probe
        self._cache = {}

    def haupttext(self):
        return "generator:" + self.fn.__name__

    def hat_fehlererkennung(self):
        try:
            return bool(self.daten(1).get("typische_fehler"))
        except Exception:  # noqa: BLE001
            return False

    def daten(self, seed):
        rng = random.Random(f"{self.fn.__name__}:{seed}")
        return self.fn(rng)

    def instanz(self, seed=None):
        if seed is None:
            seed = random.randrange(1, 10 ** 9)
        seed = int(seed)
        if seed in self._cache:
            return self._cache[seed]
        d = dict(self.daten(seed))
        typ = d.pop("typ", self.ziel_typ)
        d.setdefault("uebungsblatt", self.uebungsblatt)
        q = frage_aus_dict(typ, d)
        q.id, q.kapitel, q.seed, q.phase = self.id, self.kapitel, seed, self.phase
        q.generator_titel = self.titel
        if len(self._cache) > 500:
            self._cache.clear()
        self._cache[seed] = q
        return q

    def to_dict(self):
        return self.instanz().to_dict()

    def loesung_anzeigen(self):
        return ""

    def pruefen(self, antwort):
        raise RuntimeError("Generator: erst instanz(seed) bilden")


# ──────────────────────────────────────────────────────────────────────────
#  Kapitel
# ──────────────────────────────────────────────────────────────────────────

class _Lernziele(list):
    def __call__(self, ziele):
        self[:] = [str(z) for z in ziele]
        return self


def _frage_id(slug, frage):
    text = (frage.art + (frage.haupttext() or "").strip()).encode("utf-8")
    basis = f"{slug}:{hashlib.sha1(text).hexdigest()[:8]}"
    fid, n = basis, 1
    while fid in _IDS:
        n += 1
        fid = f"{basis}-{n}"
    _IDS.add(fid)
    return fid


class Kapitel:
    def __init__(self, slug, nummer, titel, beschreibung="", quelle="", teil="fundament", icon="📘",
                 rechenthema=True):
        self.slug = slug
        self.nummer = nummer
        self.titel = titel
        self.beschreibung = beschreibung
        self.quelle = quelle
        self.teil = teil
        self.icon = icon
        self.rechenthema = rechenthema
        self.lernziele = _Lernziele()
        self.warum_text = None
        self.elemente = []
        self.zusammenfassung_text = None
        self._praxis = False

    def __repr__(self):
        return f"<Kapitel {self.nummer} {self.slug}>"

    def _neu(self, element):
        element.kapitel = self
        if isinstance(element, Frage):
            element.phase = "praxis" if self._praxis else "ueben"
            with _LOCK:
                element.id = _frage_id(self.slug, element)
                _FRAGEN[element.id] = element
        self.elemente.append(element)
        return element

    def fragen(self):
        return [e for e in self.elemente if isinstance(e, Frage)]

    def erklaerungen(self):
        return [e for e in self.elemente if isinstance(e, Erklaerung)]

    def generatoren(self):
        return [f for f in self.fragen() if isinstance(f, Generator)]

    def to_dict(self):
        fragen = self.fragen()
        return {"slug": self.slug, "nummer": self.nummer, "titel": self.titel,
                "beschreibung": self.beschreibung, "quelle": self.quelle, "teil": self.teil,
                "icon": self.icon, "lernziele": list(self.lernziele), "warum": self.warum_text,
                "anzahl": {"seiten": sum(len(e.seiten()) for e in self.erklaerungen()),
                           "ueben": sum(f.phase == "ueben" for f in fragen),
                           "praxis": sum(f.phase == "praxis" for f in fragen),
                           "fragen": len(fragen), "generatoren": len(self.generatoren())},
                "hat_zusammenfassung": self.zusammenfassung_text is not None}

    def elemente_dicts(self):
        liste = []
        for e in self.elemente:
            if isinstance(e, Frage):
                liste.append({"typ": "frage", "frage": e.to_dict()})
            else:
                liste.append(e.to_dict())
        return liste

    # ---- API für Inhalte ----
    def warum(self, text):
        self.warum_text = _dedent(text)

    def erklaerung(self, titel, text):
        return self._neu(Erklaerung(titel, text))

    def praxis(self):
        """Ab hier: Praxisaufgaben (leicht -> schwer, zuletzt Übungsblatt-Stil)."""
        self._praxis = True

    def zusammenfassung(self, text):
        self.zusammenfassung_text = text
        e = Zusammenfassung(text)
        e.kapitel = self
        self.elemente.append(e)
        return e

    def mc(self, frage, optionen, erklaerung="", **kw):
        return self._neu(MC(frage, optionen, erklaerung, **kw))

    def wf(self, aussage, wahr, erklaerung="", **kw):
        return self._neu(WahrFalsch(aussage, wahr, erklaerung, **kw))

    def text(self, frage, antworten, erklaerung="", **kw):
        return self._neu(Textfrage(frage, antworten, erklaerung, **kw))

    def mehrfach(self, frage, richtig, falsch, erklaerung="", **kw):
        return self._neu(Mehrfach(frage, richtig, falsch, erklaerung, **kw))

    def zuordnen(self, frage, paare, erklaerung="", **kw):
        return self._neu(Zuordnen(frage, paare, erklaerung, **kw))

    def ordnen(self, frage, schritte, erklaerung="", **kw):
        return self._neu(Ordnen(frage, schritte, erklaerung, **kw))

    def zahl(self, frage, loesung, erklaerung="", **kw):
        return self._neu(Zahlfrage(frage, loesung, erklaerung, **kw))

    def term(self, frage, loesung, erklaerung="", **kw):
        return self._neu(Termfrage(frage, loesung, erklaerung, **kw))

    def loesungsmenge(self, frage, loesung, erklaerung="", **kw):
        return self._neu(Loesungsmengefrage(frage, loesung, erklaerung, **kw))

    def menge(self, frage, loesung, erklaerung="", **kw):
        return self._neu(Mengefrage(frage, loesung, erklaerung, **kw))

    def vektor(self, frage, loesung, erklaerung="", **kw):
        return self._neu(Vektorfrage(frage, loesung, erklaerung, **kw))

    def matrix(self, frage, loesung, erklaerung="", **kw):
        return self._neu(Matrixfrage(frage, loesung, erklaerung, **kw))

    def lgs(self, frage, a, b, erklaerung="", **kw):
        return self._neu(LGSFrage(frage, a, b, erklaerung, **kw))

    def luecke(self, frage, formel, antworten, erklaerung="", **kw):
        return self._neu(Luecke(frage, formel, antworten, erklaerung, **kw))

    def graph_punkt(self, frage, visual, erklaerung="", **kw):
        return self._neu(GraphPunkt(frage, visual, erklaerung=erklaerung, **kw))

    def rechenweg_aufgabe(self, frage, schritte, erklaerung="", **kw):
        return self._neu(Rechenweg(frage, schritte, erklaerung, **kw))

    def papier(self, aufgabe, musterloesung, checkliste, erklaerung="", **kw):
        return self._neu(Papier(aufgabe, musterloesung, checkliste, erklaerung, **kw))

    def generator(self, fn, typ="zahl", titel="", **kw):
        return self._neu(Generator(fn, typ, titel, **kw))

    # ---- Bequeme Varianten: Python rechnet die Lösung selbst aus ----
    def berechne(self, term, frage=None, erklaerung="", **kw):
        """Zahl-Aufgabe; Lösung = exakter Wert von term. frage: Text, '{term}' wird ersetzt."""
        t = pruefer.parse(term)
        w = pruefer.wert(t.ast)
        frage = (frage or "Berechne $\\displaystyle {term}$.").replace("{term}", pruefer.aufgabe_latex(t.ast))
        q = self._neu(Zahlfrage(frage, w, erklaerung, **kw))
        q.aufgabe_term = term
        return q

    def vereinfache(self, term, loesung, frage=None, form="vereinfacht", erklaerung="", **kw):
        """Term-Aufgabe: term soll umgeformt werden; der Selbsttest prüft term ≡ loesung."""
        t = pruefer.parse(term, kw.get("variablen"))
        frage = (frage or "Vereinfache $\\displaystyle {term}$.").replace("{term}", t.latex())
        q = self._neu(Termfrage(frage, loesung, erklaerung, form=form, **kw))
        q.aufgabe_term = term
        return q

    def gleichung(self, gleichung, frage=None, loesung=None, variable="x", erklaerung="", **kw):
        """Löse eine (Un-)Gleichung; mathlib.loese rechnet die Lösungsmenge. Eine angegebene
        loesung wird vom Selbsttest gegengeprüft."""
        berechnet = mathlib.loese(gleichung, variable)
        tex = _gleichung_tex(gleichung, variable)
        frage = (frage or "Löse $\\displaystyle {gleichung}$. Gib die Lösungsmenge an.").replace("{gleichung}", tex)
        q = self._neu(Loesungsmengefrage(frage, berechnet, erklaerung, variable=variable, **kw))
        q.gleichung_text = gleichung
        q.autor_loesung = loesung
        return q


_REL_TEX = {"<=": "\\le", ">=": "\\ge", "<": "<", ">": ">", "=": "="}


def _gleichung_tex(text, var):
    s = str(text).replace("≤", "<=").replace("≥", ">=")
    m = re.match(r"^(.*?)(<=|>=|<|>|=)(.*)$", s)
    links = pruefer.parse(m.group(1), [var]).latex()
    rechts = pruefer.parse(m.group(3), [var]).latex()
    return f"{links} {_REL_TEX[m.group(2)]} {rechts}"


_SLUG_RE = re.compile(r"^[a-z0-9_]+$")


def neues_kapitel(slug, titel, beschreibung="", quelle="", teil="fundament",
                  icon="📘", rechenthema=True):
    if not _SLUG_RE.match(slug or ""):
        raise ValueError(f"Ungültiger slug {slug!r} (nur a-z, 0-9 und _)")
    if teil not in TEIL_IDS:
        raise ValueError(f"Unbekannter teil {teil!r} – erlaubt: {', '.join(TEIL_IDS)}")
    with _LOCK:
        if slug in _KAPITEL_NACH_SLUG:
            raise ValueError(f"Den slug {slug!r} gibt es schon")
        k = Kapitel(slug, len(KAPITEL) + 1, titel, beschreibung, quelle, teil, icon, rechenthema)
        KAPITEL.append(k)
        _KAPITEL_NACH_SLUG[slug] = k
    return k


def kapitel_nach_slug(slug):
    return _KAPITEL_NACH_SLUG.get(slug)


def kapitel_von_teil(teil):
    return [k for k in KAPITEL if k.teil == teil]


def alle_fragen():
    return dict(_FRAGEN)


def frage_nach_id(fid):
    return _FRAGEN.get(fid)


def inhalte_laden():
    from . import inhalte  # noqa: F401


inhalte_laden()


# ──────────────────────────────────────────────────────────────────────────
#  Musterantwort (Antwortformat der Oberfläche) – für Selbsttest und E2E
# ──────────────────────────────────────────────────────────────────────────

def _zahl_eingabe(w):
    if isinstance(w, Fraction):
        return mathlib.text(w)
    return repr(float(w))


def musterantwort(q, schritt=None):
    """Richtige Antwort im Format von POST /api/antwort für eine KONKRETE Frage."""
    t = q.typ
    if t == "mc":
        return q.optionen[0]
    if t == "wf":
        return q.wahr
    if t == "text":
        return q.antworten[0]
    if t == "zahl":
        if isinstance(q.soll, Fraction) and getattr(q, "form", None) == "dezimal":
            return mathlib.dezimal(q.soll, 9).replace("{,}", ",")
        return pruefer.zu_text(q.soll_ast) if not isinstance(q.soll, Fraction) else mathlib.text(q.soll)
    if t == "term":
        return pruefer.zu_text(q.soll_term.ast)
    if t == "loesungsmenge":
        return pruefer.bereich_text(q.soll)
    if t == "menge":
        return "{" + "; ".join(_element_text(e) for e in q.soll) + "}"
    if t == "vektor":
        return [_zahl_eingabe(x) for x in q.soll]
    if t == "matrix":
        return [[_zahl_eingabe(x) for x in z] for z in q.soll]
    if t == "lgs":
        l = q.loesung
        if l["art"] == "keine":
            return {"keine": True, "werte": []}
        werte = []
        for i, x in enumerate(l["x"]):
            teile = [mathlib.text(x)]
            for p, r in zip(PARAMETER, l["richtungen"]):
                if r[i] != 0:
                    teile.append(f"({mathlib.text(r[i])})*{p}")
            werte.append(" + ".join(teile))
        return {"keine": False, "werte": werte}
    if t == "mehrfach":
        return list(q.richtig)
    if t == "zuordnen":
        return [[a, b] for a, b in q.paare]
    if t == "ordnen":
        return q.loesungs_ids()
    if t == "luecke":
        return [a[0] for a in q.antworten]
    if t == "graph_punkt":
        return [mathlib.text(q.ziel[0]), mathlib.text(q.ziel[1])] if q.modus == "setzen" else _zahl_eingabe(q.soll)
    if t == "papier":
        return [True] * len(q.checkliste)
    if t == "rechenweg":
        i = schritt or 0
        return {"schritt": i, "antwort": musterantwort(q.schritte[i])}
    raise ValueError(f"Keine Musterantwort für {t}")


def _element_text(e):
    art, w = e
    if art == "zahl":
        return _zahl_eingabe(w)
    if art == "tupel":
        return "(" + "; ".join(_element_text(x) for x in w) + ")"
    if art == "menge":
        return "{" + "; ".join(_element_text(x) for x in w) + "}"
    return str(w)


def fehler_als_antwort(q, wert):
    """Ein typischer Fehlwert im Antwortformat (für den Selbsttest)."""
    t = q.typ
    if t in ("vektor",):
        return [_als_text(x) for x in wert]
    if t == "matrix":
        return [[_als_text(x) for x in z] for z in wert]
    if t == "luecke":
        return [_als_text(x) for x in wert]
    if t == "graph_punkt" and q.modus == "setzen":
        return [_als_text(wert[0]), _als_text(wert[1])]
    if t == "lgs":
        return {"keine": False, "werte": [_als_text(x) for x in wert]}
    return _als_text(wert)
