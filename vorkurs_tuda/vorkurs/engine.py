# -*- coding: utf-8 -*-
"""Engine: Datenmodell, Fragetypen und Prüflogik – unabhängig von der Oberfläche.

Inhalte (vorkurs/inhalte/*) benutzen neues_kapitel(...) und die Methoden des
Kapitels (k.mc, k.code, ...). Die Oberflächen benutzen KAPITEL, TEILE,
kapitel_nach_slug(), alle_fragen(), frage.to_dict() und frage.pruefen().
"""

import ast
import copy
import hashlib
import io
import json
import random
import re
import textwrap
import threading
import tokenize
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field

from . import markup, sandbox
from .sandbox import F, P, Test  # noqa: F401  (für die Kapitelmodule)

TEILE = [
    {"id": "tag1", "titel": "Tag 1 – Variablen & Ein-/Ausgabe",
     "untertitel": "Wie Computer denken, Datentypen, Rechnen, Variablen, Strings, print & input"},
    {"id": "tag2", "titel": "Tag 2 – Verzweigungen & Schleifen",
     "untertitel": "Logik, if/elif/else, while, Listen und Slicing"},
    {"id": "tag3", "titel": "Tag 3 – Schleifen & Funktionen",
     "untertitel": "Tupel, Dictionaries, for, import, Dateien und eigene Funktionen"},
    {"id": "tag4", "titel": "Tag 4 – Rekursion & Ausblick",
     "untertitel": "Rekursion, ein Blick auf Java und guter Code"},
    {"id": "challenge", "titel": "Programmierchallenge",
     "untertitel": "Größere Aufgaben zum Knobeln"},
    {"id": "bonus", "titel": "Bonus – Vertiefung",
     "untertitel": "Für Neugierige: mehr Mathe, mehr Code"},
]
TEIL_IDS = [t["id"] for t in TEILE]

KAPITEL = []
_KAPITEL_NACH_SLUG = {}
_IDS = set()
_LOCK = threading.RLock()

LOB = ["Richtig!", "Super!", "Genau so!", "Klasse!", "Volltreffer!", "Stark!",
       "Perfekt!", "Sehr gut!", "Läuft bei dir!", "Exzellent!"]


# ──────────────────────────────────────────────────────────────────────────
#  Ergebnis einer Prüfung
# ──────────────────────────────────────────────────────────────────────────

@dataclass
class Ergebnis:
    ok: bool
    meldung: str = ""                 # Kurzfeedback
    loesung: str | None = None        # Lösung als Text (Oberfläche entscheidet, wann sie sie zeigt)
    erklaerung: str = ""              # Markup
    details: list = field(default_factory=list)
    hinweis: str | None = None        # z. B. "Komma statt Punkt?"

    def to_dict(self, mit_loesung=True):
        d = asdict(self)
        if not mit_loesung:
            d["loesung"] = None
        return d


# ──────────────────────────────────────────────────────────────────────────
#  Normalisierungen (aus v1)
# ──────────────────────────────────────────────────────────────────────────

def norm_text(s, gross_klein=False):
    """Vereinheitlicht eine Textantwort (Groß/klein, Leerzeichen, Anführungszeichen egal).
       gross_klein=True: Groß-/Kleinschreibung zählt (z. B. `python3 -V` ≠ `python3 -v`)."""
    s = str(s).strip()
    if not gross_klein:
        s = s.lower()
    s = s.strip("'\"` ").rstrip(".!")
    return re.sub(r"\s+", "", s)


def norm_ausgabe(s):
    """Vereinheitlicht eine Konsolenausgabe: Zeilenumbrüche/Leerzeichen/Kommas
       zählen gleich, " und ' sind egal."""
    s = str(s).strip().replace('"', "'")
    s = re.sub(r"[\s,]+", " ", s).strip()
    s = re.sub(r"\b(true|false|none)\b", lambda m: m.group(1).capitalize(), s, flags=re.IGNORECASE)
    return s


def ohne_anfuehrungszeichen(s):
    s = str(s).strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "'\"":
        return s[1:-1]
    return s


def norm_code(s):
    """Vereinheitlicht ein Code-Stück: Leerzeichen zwischen Tokens egal,
       Groß/klein zählt, ' und " bei Strings egal."""
    s = str(s).strip()
    try:
        teile = []
        for tok in tokenize.generate_tokens(io.StringIO(s).readline):
            if tok.type in (tokenize.NEWLINE, tokenize.NL, tokenize.ENDMARKER,
                            tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT):
                continue
            text = tok.string
            if tok.type == tokenize.STRING:
                try:
                    text = repr(ast.literal_eval(text))
                except (ValueError, SyntaxError):
                    pass
            teile.append(text)
        return " ".join(teile)
    except (tokenize.TokenError, SyntaxError, IndentationError):
        return re.sub(r"\s+", " ", s)


def _code_tokens(quelltext):
    """Code ohne Kommentare und Strings als Token-Text (mit Leerzeichen getrennt)."""
    weg = {tokenize.COMMENT, tokenize.STRING, tokenize.NL, tokenize.NEWLINE,
           tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER}
    for name in ("FSTRING_START", "FSTRING_MIDDLE", "FSTRING_END"):
        if hasattr(tokenize, name):
            weg.add(getattr(tokenize, name))
    teile = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(quelltext).readline):
            if tok.type not in weg:
                teile.append(tok.string)
    except (tokenize.TokenError, SyntaxError, IndentationError):
        if not teile:
            ohne_kommentare = re.sub(r"#.*", "", quelltext)
            return re.sub(r"\s+", " ", ohne_kommentare).strip()
    return " ".join(teile)


def _enthaelt(code_tokens, stueck):
    """Kommt stueck (Text wie '[::-1]' oder 'while') im Token-Text vor?"""
    muster = _code_tokens(stueck) or stueck.strip()
    if not muster:
        return False
    text = " " + code_tokens + " "
    start = 0
    while True:
        pos = text.find(muster, start)
        if pos < 0:
            return False
        vorher, nachher = text[pos - 1], text[pos + len(muster)] if pos + len(muster) < len(text) else " "
        links_ok = not (muster[0].isalnum() or muster[0] == "_") or not (vorher.isalnum() or vorher == "_")
        rechts_ok = not (muster[-1].isalnum() or muster[-1] == "_") or not (nachher.isalnum() or nachher == "_")
        if links_ok and rechts_ok:
            return True
        start = pos + 1


def _ruft_sich_selbst_auf(quelltext, name):
    """None = Funktion fehlt, False = nicht rekursiv, True = rekursiv.

    name darf Alternativen mit | enthalten ("even|odd"): dann reicht EINE davon."""
    try:
        baum = ast.parse(quelltext)
    except SyntaxError:
        return None
    namen = [n.strip() for n in str(name).split("|") if n.strip()]
    gefunden = None
    for knoten in ast.walk(baum):
        if isinstance(knoten, (ast.FunctionDef, ast.AsyncFunctionDef)) and knoten.name in namen:
            gefunden = False
            for innen in ast.walk(knoten):
                if (isinstance(innen, ast.Call) and isinstance(innen.func, ast.Name)
                        and innen.func.id == knoten.name):
                    return True
    return gefunden


def _namen_text(name, wort="oder"):
    """'even|odd' -> '`even` oder `odd`'."""
    namen = [n.strip() for n in str(name).split("|") if n.strip()]
    return f" {wort} ".join(f"`{n}`" for n in namen)


# ──────────────────────────────────────────────────────────────────────────
#  Eingebaute Code-Regeln (AST) für k.code(..., regeln=[...])
# ──────────────────────────────────────────────────────────────────────────
#  "keine_slices"               kein Slice (lst[1:], lst[::-1], ...)
#  "keine_schleifen"            kein for/while (auch keine Comprehension)
#  "max_funktionen:N"           höchstens N Funktionen (def und lambda)
#  "schleife_in:name"           die Funktion name enthält eine Schleife
#  "funktion:name|name2"        mindestens eine dieser Funktionen ist definiert
#  "nur_konstanten:<json>"      alle Zahlen-/String-Literale stammen aus der Liste
#  "pflicht_konstanten:<json>"  jede Konstante der Liste kommt mindestens einmal vor
#  "keine_methode:name"         keine Methode .name (z. B. reverse, sort)
#  "keine_funktion:name"        keine Funktion name (z. B. reversed, max, factorial)
#  "nur_funktionen:a|b|c"       nur diese Funktionen aufrufen (Methoden wie .upper() erlaubt)
#  Mehrere Namen werden immer mit | getrennt, z. B. "keine_funktion:max|min|sorted".

_REGEL_ARGUMENT = {"keine_slices": None, "keine_schleifen": None, "max_funktionen": "zahl",
                   "schleife_in": "namen", "funktion": "namen", "nur_konstanten": "json",
                   "pflicht_konstanten": "json", "keine_methode": "namen", "keine_funktion": "namen",
                   "nur_funktionen": "namen"}
REGEL_NAMEN = tuple(_REGEL_ARGUMENT)
_SCHLEIFEN = (ast.For, ast.AsyncFor, ast.While, ast.ListComp, ast.SetComp, ast.DictComp,
              ast.GeneratorExp)
_FUNKTIONEN = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)


def _regel_zerlegen(regel):
    """'max_funktionen:1' -> ('max_funktionen', 1). Ungültig -> ValueError."""
    if not isinstance(regel, str):
        raise ValueError(f"Regel muss ein Text sein, nicht {type(regel).__name__}")
    name, _, arg = regel.partition(":")
    name, arg = name.strip(), arg.strip()
    if name not in _REGEL_ARGUMENT:
        raise ValueError(f"Unbekannte Regel {name!r}. Erlaubt: {', '.join(REGEL_NAMEN)}")
    art = _REGEL_ARGUMENT[name]
    if art is None:
        if arg:
            raise ValueError(f"Regel {name!r} hat kein Argument")
        return name, None
    if not arg:
        raise ValueError(f"Regel {name!r} braucht ein Argument ({name}:...)")
    if art == "zahl":
        if not arg.isdigit():
            raise ValueError(f"Regel {name!r} braucht eine ganze Zahl, nicht {arg!r}")
        return name, int(arg)
    if art == "namen":
        namen = [n.strip() for n in arg.split("|")]
        if not all(n.isidentifier() for n in namen):
            raise ValueError(f"Regel {name!r}: {arg!r} ist kein gültiger Name")
        return name, namen
    try:
        werte = json.loads(arg)
    except ValueError as e:
        raise ValueError(f"Regel {name!r}: ungültiges JSON {arg!r} ({e})") from None
    if not isinstance(werte, list) or not werte or not all(
            isinstance(w, (int, float, str)) and not isinstance(w, bool) for w in werte):
        raise ValueError(f"Regel {name!r} braucht eine JSON-Liste aus Zahlen und Texten")
    return name, werte


def regel_fehler(regel):
    """None, wenn die Regel gültig ist – sonst eine Fehlerbeschreibung (für den Selbsttest)."""
    try:
        _regel_zerlegen(regel)
        return None
    except ValueError as e:
        return str(e)


def _konstanten_text(werte):
    return ", ".join(repr(w) for w in werte)


def regel_beschreibung(regel):
    """Kurze, verständliche Beschreibung einer Regel (für Oberflächen)."""
    try:
        name, arg = _regel_zerlegen(regel)
    except ValueError:
        return str(regel)
    if name == "keine_slices":
        return "keine Slices (auch nicht lst[1:] oder lst[::-1])"
    if name == "keine_schleifen":
        return "keine Schleifen (kein for, kein while)"
    if name == "max_funktionen":
        return "nur eine einzige Funktion" if arg == 1 else f"höchstens {arg} Funktionen"
    if name == "schleife_in":
        return " oder ".join(f"{n}()" for n in arg) + " benutzt eine Schleife"
    if name == "funktion":
        return "Funktion " + " oder ".join(f"{n}()" for n in arg) + " definieren"
    if name == "nur_konstanten":
        return f"als Konstanten nur {_konstanten_text(arg)}"
    if name == "pflicht_konstanten":
        return f"die Konstanten {_konstanten_text(arg)} kommen vor"
    if name == "keine_methode":
        return "nicht erlaubt: " + ", ".join(f".{n}()" for n in arg)
    if name == "nur_funktionen":
        return "nur die Funktionen " + ", ".join(f"{n}()" for n in arg)
    return "nicht erlaubt: " + ", ".join(f"{n}()" for n in arg)


def _zeile(knoten):
    return f" (Zeile {knoten.lineno})" if getattr(knoten, "lineno", None) else ""


def _ist_konstante(knoten):
    """Zahlen- und String-Literale (True/False/None zählen nicht)."""
    return (isinstance(knoten, ast.Constant) and not isinstance(knoten.value, bool)
            and isinstance(knoten.value, (int, float, complex, str, bytes)))


def _gleiche_konstante(a, b):
    return type(a) is type(b) and a == b


def regel_anwenden(baum, regel):
    """Prüft eine Regel am AST. Rückgabe: Fehlermeldung (str) oder '' (eingehalten)."""
    name, arg = _regel_zerlegen(regel)
    knoten = list(ast.walk(baum))
    if name == "keine_slices":
        treffer = [k for k in knoten if isinstance(k, ast.Slice)]
        if treffer:
            return ("Slices wie `lst[1:]` oder `lst[::-1]` sind in dieser Aufgabe nicht erlaubt"
                    f"{_zeile(treffer[0])}.")
    elif name == "keine_schleifen":
        treffer = [k for k in knoten if isinstance(k, _SCHLEIFEN)]
        if treffer:
            art = ("eine for-Schleife" if isinstance(treffer[0], (ast.For, ast.AsyncFor))
                   else "eine while-Schleife" if isinstance(treffer[0], ast.While)
                   else "eine Schleife in eckigen/runden Klammern ([... for ... in ...])")
            return (f"In dieser Aufgabe sind keine Schleifen erlaubt – dein Code enthält {art}"
                    f"{_zeile(treffer[0])}.")
    elif name == "max_funktionen":
        funktionen = [k for k in knoten if isinstance(k, _FUNKTIONEN)]
        if len(funktionen) > arg:
            namen = ", ".join(f"`{k.name}`" if hasattr(k, "name") else "`lambda`" for k in funktionen)
            erlaubt = "genau eine Funktion" if arg == 1 else f"höchstens {arg} Funktionen"
            return f"Du hast {len(funktionen)} Funktionen definiert ({namen}), erlaubt ist {erlaubt}."
    elif name in ("schleife_in", "funktion"):
        defs = [k for k in knoten if isinstance(k, (ast.FunctionDef, ast.AsyncFunctionDef))
                and k.name in arg]
        if not defs:
            return f"Es gibt keine Funktion {_namen_text('|'.join(arg))} – prüfe den Namen."
        if name == "schleife_in" and not any(isinstance(k, _SCHLEIFEN) for d in defs
                                             for k in ast.walk(d)):
            return (f"In {_namen_text('|'.join(arg))} steckt keine Schleife. Benutze dort eine "
                    "`for`- oder `while`-Schleife.")
    elif name == "nur_konstanten":
        fremd = []
        for k in knoten:
            if _ist_konstante(k) and not any(_gleiche_konstante(k.value, w) for w in arg):
                text = repr(k.value) + _zeile(k)
                if text not in fremd:
                    fremd.append(text)
        if fremd:
            return (f"Nicht erlaubte Konstante(n): {', '.join(fremd[:5])}"
                    f"{' …' if len(fremd) > 5 else ''}. Erlaubt sind nur {_konstanten_text(arg)} "
                    "(Kommentare mit # sind ok).")
    elif name == "pflicht_konstanten":
        werte = [k.value for k in knoten if _ist_konstante(k)]
        fehlend = [w for w in arg if not any(_gleiche_konstante(v, w) for v in werte)]
        if fehlend:
            return (f"Diese Konstante(n) müssen mindestens einmal vorkommen: "
                    f"{_konstanten_text(fehlend)}.")
    elif name == "keine_methode":
        treffer = [k for k in knoten if isinstance(k, ast.Attribute) and k.attr in arg]
        if treffer:
            return (f"Die Methode `.{treffer[0].attr}()` darfst du in dieser Aufgabe nicht "
                    f"benutzen{_zeile(treffer[0])}.")
    elif name == "keine_funktion":
        treffer = [k for k in knoten
                   if (isinstance(k, ast.Name) and k.id in arg and not isinstance(k.ctx, ast.Store))
                   or (isinstance(k, ast.Attribute) and k.attr in arg)
                   or (isinstance(k, ast.alias) and k.name in arg)]
        if treffer:
            t = treffer[0]
            n = t.id if isinstance(t, ast.Name) else t.attr if isinstance(t, ast.Attribute) else t.name
            return f"Die Funktion `{n}()` darfst du in dieser Aufgabe nicht benutzen{_zeile(t)}."
    elif name == "nur_funktionen":
        treffer = [k for k in knoten if isinstance(k, ast.Call) and isinstance(k.func, ast.Name)
                   and k.func.id not in arg]
        if treffer:
            erlaubt = ", ".join(f"`{n}()`" for n in arg)
            return (f"Erlaubt sind nur die Funktionen {erlaubt} – du benutzt "
                    f"`{treffer[0].func.id}()`{_zeile(treffer[0])}.")
    return ""


def _dedent(text):
    return textwrap.dedent(text or "").strip("\n")


def _komma_hinweis():
    return "Fast! Achtung: Python schreibt Kommazahlen mit PUNKT, nicht mit Komma."


# ──────────────────────────────────────────────────────────────────────────
#  Elemente eines Kapitels
# ──────────────────────────────────────────────────────────────────────────

class Element:
    typ = "element"
    phase = "verstehen"
    kapitel = None


class Erklaerung(Element):
    """Ein Lernabschnitt (Markup); '---' trennt Seiten."""
    typ = "erklaerung"

    def __init__(self, titel, text):
        self.titel = titel
        self.text = text

    def seiten(self):
        return markup.parse(self.text)

    def to_dict(self):
        return {"typ": "erklaerung", "titel": self.titel, "seiten": self.seiten()}


class Zusammenfassung(Element):
    """Merkzettel am Ende eines Kapitels (Markup)."""
    typ = "zusammenfassung"

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
    ist_code_aufgabe = False

    def __init__(self, erklaerung="", tipp=None, code=None, tipps=None):
        self.erklaerung = erklaerung or ""
        if tipps:
            self.tipps = [str(t) for t in tipps]
        else:
            self.tipps = [tipp] if tipp else []
        self.code = _dedent(code) if code else None
        self.id = None
        self.kapitel = None

    @property
    def tipp(self):
        return self.tipps[0] if self.tipps else None

    def haupttext(self):
        raise NotImplementedError

    def to_dict(self, mischen=True):
        d = {"id": self.id, "typ": self.typ, "art": self.art, "phase": self.phase,
             "kapitel": self.kapitel.slug if self.kapitel else None,
             "tipps": list(self.tipps), "code": self.code}
        d.update(self._dict(mischen))
        return d

    def _dict(self, mischen):
        return {}

    def pruefen(self, antwort):
        raise NotImplementedError

    def loesung_anzeigen(self):
        raise NotImplementedError

    def _ergebnis(self, ok, meldung=None, **kw):
        if meldung is None:
            meldung = random.choice(LOB) if ok else "Leider nicht richtig."
        kw.setdefault("loesung", self.loesung_anzeigen())
        return Ergebnis(ok=ok, meldung=meldung, erklaerung=self.erklaerung, **kw)


class MC(Frage):
    """Multiple Choice. Die ERSTE Option ist immer die richtige."""
    art = "Multiple Choice"
    typ = "mc"

    def __init__(self, frage, optionen, erklaerung="", code=None, tipp=None):
        super().__init__(erklaerung, tipp, code)
        self.frage = frage
        self.optionen = [str(o) for o in optionen]

    def haupttext(self):
        return self.frage

    def _dict(self, mischen):
        optionen = self.optionen[:]
        if mischen:
            random.shuffle(optionen)
        return {"frage": self.frage, "optionen": optionen}

    def loesung_anzeigen(self):
        return self.optionen[0]

    def pruefen(self, antwort):
        antwort = str(antwort if antwort is not None else "")
        if antwort not in self.optionen:
            passend = [o for o in self.optionen if o.strip() == antwort.strip()]
            antwort = passend[0] if passend else antwort
        return self._ergebnis(antwort == self.optionen[0])


class WahrFalsch(Frage):
    art = "Wahr oder falsch?"
    typ = "wf"

    def __init__(self, aussage, wahr, erklaerung="", code=None, tipp=None):
        super().__init__(erklaerung, tipp, code)
        self.aussage = aussage
        self.wahr = bool(wahr)

    def haupttext(self):
        return self.aussage

    def _dict(self, mischen):
        return {"aussage": self.aussage}

    def loesung_anzeigen(self):
        return "Wahr" if self.wahr else "Falsch"

    def pruefen(self, antwort):
        if isinstance(antwort, str):
            a = antwort.strip().lower()
            if a in ("w", "wahr", "j", "ja", "true", "t", "1", "richtig", "stimmt"):
                antwort = True
            elif a in ("f", "falsch", "n", "nein", "false", "0", "stimmt nicht"):
                antwort = False
            else:
                return self._ergebnis(False, "Bitte mit wahr oder falsch antworten.")
        return self._ergebnis(bool(antwort) == self.wahr)


class Textfrage(Frage):
    """Freie Antwort; 'antworten' ist eine Liste akzeptierter Antworten."""
    art = "Antwort eintippen"
    typ = "text"

    def __init__(self, frage, antworten, erklaerung="", tipp=None, code=None, gross_klein=False):
        super().__init__(erklaerung, tipp, code)
        self.frage = frage
        self.antworten = [str(a) for a in antworten]
        self.gross_klein = bool(gross_klein)

    def haupttext(self):
        return self.frage

    def _dict(self, mischen):
        return {"frage": self.frage, "gross_klein": self.gross_klein}

    def loesung_anzeigen(self):
        return self.antworten[0]

    def pruefen(self, antwort):
        antwort = str(antwort or "")
        gk = self.gross_klein
        gueltig = {norm_text(x, gk) for x in self.antworten}
        if norm_text(antwort, gk) in gueltig:
            return self._ergebnis(True)
        hinweis = None
        if "," in antwort and norm_text(antwort.replace(",", "."), gk) in gueltig:
            hinweis = _komma_hinweis()
        elif gk and norm_text(antwort) in {norm_text(x) for x in self.antworten}:
            hinweis = "Fast! Hier zählt die Groß-/Kleinschreibung – schau sie dir noch einmal genau an."
        return self._ergebnis(False, hinweis=hinweis)


class Ausgabe(Frage):
    """'Was gibt dieser Code aus?' – die Lösung wird durch echtes Ausführen ermittelt."""
    art = "Was gibt der Code aus?"
    typ = "ausgabe"
    _CACHE = {}
    _CACHE_LOCK = threading.Lock()

    def __init__(self, code, erklaerung="", frage=None, tipp=None, akzeptiert=()):
        super().__init__(erklaerung, tipp, code)
        self.frage = frage or "Was gibt dieser Code in der Konsole aus?"
        self.akzeptiert = [str(a) for a in akzeptiert]

    def haupttext(self):
        return self.code

    def _dict(self, mischen):
        return {"frage": self.frage}

    def soll(self):
        """(ausgabe, fehlername|None) – wird einmal ausgeführt und gemerkt."""
        with Ausgabe._CACHE_LOCK:
            if self.code in Ausgabe._CACHE:
                return Ausgabe._CACHE[self.code]
        erg = sandbox.beispiel_ausfuehren(self.code)
        if erg[1] != "Timeout":
            with Ausgabe._CACHE_LOCK:
                Ausgabe._CACHE[self.code] = erg
        return erg

    def loesung_anzeigen(self):
        ausgabe, fehler = self.soll()
        if fehler:
            return (ausgabe + "\n" if ausgabe else "") + f"Fehler: {fehler}"
        return ausgabe if ausgabe else "(gar nichts)"

    def _passt(self, a):
        ausgabe, fehler = self.soll()
        if fehler:
            return fehler.lower() in a.lower() or norm_text(a) in ("fehler", "error", "exception")
        kandidaten = {norm_ausgabe(a), norm_ausgabe(ohne_anfuehrungszeichen(a))}
        richtig = {norm_ausgabe(ausgabe)} | {norm_ausgabe(x) for x in self.akzeptiert}
        if not ausgabe and norm_text(a) in ("", "nichts", "garnichts", "leer", "keineausgabe"):
            return True
        return bool(kandidaten & richtig)

    def pruefen(self, antwort):
        a = str(antwort or "")
        if self._passt(a):
            _, fehler = self.soll()
            hinweis = None
            if fehler and fehler.lower() not in a.lower():
                hinweis = f"Richtig, es gibt einen Fehler! Sein Name ist: {fehler} – merk ihn dir."
            return self._ergebnis(True, hinweis=hinweis)
        hinweis = None
        if "," in a and self._passt(a.replace(",", ".")):
            hinweis = _komma_hinweis()
        return self._ergebnis(False, hinweis=hinweis)


class Ausdruck(Frage):
    """Der Nutzer tippt einen Python-Ausdruck; 'tests' sind Variablenbelegungen."""
    art = "Python-Ausdruck schreiben"
    typ = "ausdruck"

    def __init__(self, frage, tests, loesung, erklaerung="", tipp=None, muss_enthalten=None):
        super().__init__(erklaerung, tipp)
        self.frage = frage
        self.tests = list(tests)
        self.loesung = loesung
        self.muss_enthalten = muss_enthalten

    def haupttext(self):
        return self.frage

    def gegeben(self):
        belegung = self.tests[0] if self.tests else {}
        return "\n".join(f"{k} = {v!r}" for k, v in belegung.items())

    def _dict(self, mischen):
        return {"frage": self.frage, "gegeben": self.gegeben(),
                "muss_enthalten": self.muss_enthalten}

    def _soll(self, belegung):
        return eval(self.loesung, {"__builtins__": __builtins__}, copy.deepcopy(belegung))

    def loesung_anzeigen(self):
        if self.tests:
            return f"{self.loesung}     (ergibt {self._soll(self.tests[0])!r})"
        return self.loesung

    def pruefen(self, antwort):
        a = str(antwort or "").strip()
        if not a:
            return self._ergebnis(False, "Du hast keinen Ausdruck eingegeben.")
        if self.muss_enthalten and self.muss_enthalten not in a:
            return self._ergebnis(False, f"Dein Ausdruck soll '{self.muss_enthalten}' verwenden.")
        erg = sandbox.ausdruck_auswerten(a, self.loesung, self.tests)
        if erg is None:
            return self._ergebnis(False, "Dein Ausdruck braucht viel zu lange zum Rechnen.")
        details = []
        for belegung, e in zip(self.tests, erg):
            name = ", ".join(f"{k} = {v!r}" for k, v in belegung.items())
            details.append({"name": name, "ok": e.get("ok", False),
                            "meldung": e.get("fehler", ""), "eingaben": [],
                            "erwartet": e.get("soll", ""), "ausgabe": e.get("ist", "")})
        fehlschlag = next((d for d, e in zip(details, erg) if not e.get("ok")), None)
        if fehlschlag is None:
            hinweis = f"Dein Ausdruck ergibt: {erg[0]['ist']}" if erg else None
            if norm_text(a) != norm_text(self.loesung):
                hinweis = (hinweis + "   " if hinweis else "") + \
                    f"(Eine mögliche Musterlösung wäre: {self.loesung})"
            return self._ergebnis(True, details=details, hinweis=hinweis)
        if fehlschlag["meldung"]:
            meldung = f"Dein Ausdruck erzeugt einen Fehler: {fehlschlag['meldung']}"
            hinweis = sandbox.fehler_erklaeren(fehlschlag["meldung"])
        else:
            meldung = (f"Bei {fehlschlag['name']} liefert dein Ausdruck {fehlschlag['ausgabe']}, "
                       f"erwartet war {fehlschlag['erwartet']}.")
            hinweis = None
        return self._ergebnis(False, meldung, details=details, hinweis=hinweis)


class Luecke(Frage):
    """Lückencode: ___ im Code, pro Lücke eine Liste akzeptierter Antworten."""
    art = "Lückencode"
    typ = "luecke"
    phase = "programmieren"
    LUECKE = "___"

    def __init__(self, frage, code, antworten, erklaerung="", tipp=None):
        super().__init__(erklaerung, tipp, code)
        self.frage = frage
        self.antworten = [[str(a) for a in (x if isinstance(x, (list, tuple)) else [x])]
                          for x in antworten]

    def haupttext(self):
        return self.frage + "\n" + (self.code or "")

    def anzahl_luecken(self):
        return (self.code or "").count(self.LUECKE)

    def _dict(self, mischen):
        return {"frage": self.frage, "anzahl_luecken": self.anzahl_luecken()}

    def loesung_anzeigen(self):
        teile = (self.code or "").split(self.LUECKE)
        text = teile[0]
        for i, rest in enumerate(teile[1:]):
            text += (self.antworten[i][0] if i < len(self.antworten) else "???") + rest
        return text

    def pruefen(self, antwort):
        if isinstance(antwort, str):
            antwort = [antwort]
        antwort = [str(a) for a in (antwort or [])]
        n = self.anzahl_luecken()
        if len(antwort) != n:
            return self._ergebnis(False, f"Bitte fülle alle {n} Lücken aus.")
        details = []
        for i, (a, gueltig) in enumerate(zip(antwort, self.antworten), 1):
            ok = norm_code(a) in {norm_code(g) for g in gueltig}
            details.append({"name": f"Lücke {i}", "ok": ok, "meldung": "" if ok else "stimmt nicht",
                            "eingaben": [], "erwartet": "", "ausgabe": a})
        richtig = sum(d["ok"] for d in details)
        if richtig == n:
            return self._ergebnis(True, details=details)
        return self._ergebnis(False, f"{richtig} von {n} Lücken richtig.", details=details)


class Puzzle(Frage):
    """Code-Puzzle (Parsons-Problem): Zeilen in die richtige Reihenfolge bringen."""
    art = "Code-Puzzle"
    typ = "puzzle"
    phase = "programmieren"

    def __init__(self, aufgabe, loesungscode, erklaerung="", tipp=None, ablenker=()):
        super().__init__(erklaerung, tipp)
        self.aufgabe = aufgabe
        self.loesung = _dedent(loesungscode)
        self.zeilen = [z.rstrip() for z in self.loesung.splitlines() if z.strip()]
        self.ablenker = [str(a).rstrip() for a in ablenker]
        self._ids = None

    def haupttext(self):
        return self.aufgabe

    def _zeilen_ids(self):
        """{zeilen_id: (text, ist_ablenker)} – IDs verraten die Reihenfolge nicht."""
        if self._ids is None:
            ids = {}
            for i, z in enumerate(self.zeilen + self.ablenker):
                zid = hashlib.sha1(f"{self.id}|{i}|{z}".encode("utf-8")).hexdigest()[:8]
                ids[zid] = (z, i >= len(self.zeilen))
            self._ids = ids
        return self._ids

    def _loesungs_ids(self):
        return list(self._zeilen_ids())[:len(self.zeilen)]

    def _dict(self, mischen):
        eintraege = [{"zeilen_id": zid, "text": text.strip(),
                      "einrueckung": len(text) - len(text.lstrip(" "))}
                     for zid, (text, _) in self._zeilen_ids().items()]
        if mischen:
            random.shuffle(eintraege)
        return {"aufgabe": self.aufgabe, "zeilen": eintraege, "anzahl": len(self.zeilen)}

    def loesung_anzeigen(self):
        return self.loesung

    def pruefen(self, antwort):
        ids = self._zeilen_ids()
        antwort = list(antwort or [])
        if any(a not in ids for a in antwort):
            return self._ergebnis(False, "Unbekannte Zeile in der Antwort.")
        gewaehlt = [ids[a][0] for a in antwort]
        details = []
        for i, zid in enumerate(antwort):
            text, ablenker = ids[zid]
            soll = self.zeilen[i] if i < len(self.zeilen) else None
            ok = not ablenker and text == soll
            details.append({"name": f"Zeile {i + 1}", "ok": ok,
                            "meldung": "gehört nicht in die Lösung" if ablenker else "",
                            "eingaben": [], "erwartet": "", "ausgabe": text})
        if gewaehlt == self.zeilen:
            return self._ergebnis(True, details=details)
        benutzte_ablenker = [ids[a][0].strip() for a in antwort if ids[a][1]]
        if benutzte_ablenker:
            return self._ergebnis(False, f"Die Zeile `{benutzte_ablenker[0]}` gehört nicht in die "
                                         "Lösung.", details=details)
        if sorted(gewaehlt) != sorted(self.zeilen):
            return self._ergebnis(False, f"Es müssen genau {len(self.zeilen)} Zeilen verwendet "
                                         "werden.", details=details)
        # Andere Reihenfolge mit gleicher Ausgabe ist auch richtig (nur ohne input()).
        if "input(" not in self.loesung:
            soll_aus, soll_fehler = sandbox.beispiel_ausfuehren(self.loesung)
            if soll_aus and not soll_fehler:
                ist_aus, ist_fehler = sandbox.beispiel_ausfuehren("\n".join(gewaehlt))
                if not ist_fehler and ist_aus == soll_aus:
                    for d in details:
                        d["ok"] = True
                    return self._ergebnis(True, "Richtig! Deine Reihenfolge erzeugt dieselbe "
                                                "Ausgabe wie die Musterlösung.", details=details)
        richtig = sum(d["ok"] for d in details)
        return self._ergebnis(False, f"{richtig} von {len(self.zeilen)} Zeilen stehen an der "
                                     "richtigen Stelle.", details=details)


class CodeAufgabe(Frage):
    """Programmieraufgabe mit automatischen Tests."""
    art = "Programmieraufgabe"
    typ = "code"
    phase = "programmieren"
    ist_code_aufgabe = True

    def __init__(self, aufgabe, tests, loesung, erklaerung="", tipp=None, vorlage=None,
                 verboten=(), pflicht=(), rekursiv=None, tipps=None, regeln=(), streng=False):
        super().__init__(erklaerung, tipp, tipps=tipps)
        self.aufgabe = aufgabe
        self.tests = list(tests)
        self.loesung = _dedent(loesung)
        self.vorlage = vorlage
        self.verboten = list(verboten or ())
        self.pflicht = list(pflicht or ())
        self.rekursiv = rekursiv
        self.regeln = [regeln] if isinstance(regeln, str) else list(regeln or ())
        self.streng = bool(streng)

    def haupttext(self):
        return self.aufgabe

    def genaue_ausgabe(self):
        """True, wenn mindestens ein Test Groß/klein und Satzzeichen der Ausgabe prüft."""
        for t in self.tests:
            if t.aufruf:
                continue
            if t.exakt is not None and t.streng is not False:
                return True
            if (t.erwartet or t.anzahl) and (t.streng if t.streng is not None else self.streng):
                return True
        return False

    def _dict(self, mischen):
        return {"aufgabe": self.aufgabe, "vorlage": self.vorlage,
                "tests": [{"name": t.name() or f"Test {i}", "eingaben": list(t.eingaben)}
                          for i, t in enumerate(self.tests, 1)],
                "anzahl_tests": len(self.tests), "verboten": list(self.verboten),
                "pflicht": list(self.pflicht), "rekursiv": self.rekursiv,
                "regeln": [regel_beschreibung(r) for r in self.regeln],
                "genaue_ausgabe": self.genaue_ausgabe()}

    def loesung_anzeigen(self):
        return self.loesung

    def regeln_pruefen(self, code):
        """Prüft verboten/pflicht/rekursiv. Rückgabe: Liste von Detail-Dicts."""
        ergebnisse = []
        tokens = _code_tokens(code)
        for stueck in self.verboten:
            ok = not _enthaelt(tokens, stueck)
            ergebnisse.append({"name": f"Verboten: {stueck.strip()}", "ok": ok, "regel": True,
                               "meldung": "" if ok else f"In dieser Aufgabe darfst du `{stueck.strip()}` "
                                                         "nicht benutzen.",
                               "eingaben": [], "erwartet": "", "ausgabe": ""})
        for stueck in self.pflicht:
            ok = _enthaelt(tokens, stueck)
            ergebnisse.append({"name": f"Pflicht: {stueck.strip()}", "ok": ok, "regel": True,
                               "meldung": "" if ok else f"Dein Code soll `{stueck.strip()}` verwenden.",
                               "eingaben": [], "erwartet": "", "ausgabe": ""})
        if self.rekursiv:
            status = _ruft_sich_selbst_auf(code, self.rekursiv)
            ok = status is True
            namen = _namen_text(self.rekursiv)
            mehrere = "|" in str(self.rekursiv)
            if status is None:
                meldung = (f"Es gibt keine Funktion {namen} – oder der Code enthält Syntaxfehler.")
            elif status is False:
                meldung = (f"Die Funktion {namen} soll sich selbst aufrufen (Rekursion)." if not mehrere
                           else f"Eine der Funktionen {namen} soll sich selbst aufrufen (Rekursion).")
            else:
                meldung = ""
            ergebnisse.append({"name": f"Rekursion: {self.rekursiv.replace('|', ' oder ')}", "ok": ok,
                               "regel": True, "meldung": meldung, "eingaben": [], "erwartet": "",
                               "ausgabe": ""})
        if self.regeln:
            try:
                baum = ast.parse(code)
            except SyntaxError:
                baum = None
            for regel in self.regeln:
                if regel_fehler(regel):
                    continue            # ungültige Regel: meldet der Selbsttest
                meldung = regel_anwenden(baum, regel) if baum is not None else                     "Die Regel kann wegen eines Syntaxfehlers nicht geprüft werden."
                ergebnisse.append({"name": f"Regel: {regel_beschreibung(regel)}", "ok": not meldung,
                                   "regel": True, "meldung": meldung, "eingaben": [],
                                   "erwartet": "", "ausgabe": ""})
        return ergebnisse

    def tests_ausfuehren(self, code):
        """Führt ALLE Tests (parallel) aus. Rückgabe: Liste (ok, meldung, details)."""
        sandbox.loesungswerte_berechnen(self.loesung, self.tests)
        if not self.tests:
            return []
        with ThreadPoolExecutor(max_workers=min(8, len(self.tests))) as pool:
            ergebnisse = list(pool.map(lambda t: sandbox.test_ausfuehren(code, t, self.loesung,
                                                                         streng=self.streng),
                                       self.tests))
        for i, (_, _, d) in enumerate(ergebnisse, 1):
            d["name"] = f"Test {i}" + (f": {d['name']}" if d["name"] else "")
        return ergebnisse

    def alle_tests(self, code):
        """Wie v1: (ok, meldung des ersten fehlgeschlagenen Tests)."""
        for ok, meldung, _ in self.tests_ausfuehren(code):
            if not ok:
                return False, meldung
        return True, ""

    def pruefen(self, antwort):
        code = str(antwort or "").expandtabs(4)
        if not code.strip():
            return self._ergebnis(False, "Du hast noch keinen Code geschrieben.")
        try:
            compile(code, sandbox.DATEINAME, "exec")
        except SyntaxError as e:
            fehler = f"{type(e).__name__}: {e.msg}"
            meldung = f"Dein Code enthält einen Syntaxfehler in Zeile {e.lineno}: {e.msg}"
            details = [{"name": f"Test {i}" + (f": {t.name()}" if t.name() else ""), "ok": False,
                        "meldung": "nicht ausgeführt (Syntaxfehler)", "eingaben": list(t.eingaben),
                        "erwartet": "", "ausgabe": "", "fehler": fehler}
                       for i, t in enumerate(self.tests, 1)]
            return self._ergebnis(False, meldung, details=details,
                                  hinweis=sandbox.fehler_erklaeren(fehler))
        regeln = self.regeln_pruefen(code)
        ergebnisse = self.tests_ausfuehren(code)
        details = regeln + [d for _, _, d in ergebnisse]
        bestanden = sum(1 for ok, _, _ in ergebnisse if ok)
        regel_fehler = [r["meldung"] for r in regeln if not r["ok"]]
        alle_ok = bestanden == len(ergebnisse) and not regel_fehler
        if alle_ok:
            return self._ergebnis(True, f"✔ Alle {len(ergebnisse)} Tests bestanden! " + random.choice(LOB),
                                  details=details)
        teile = [f"{bestanden} von {len(ergebnisse)} Tests bestanden."]
        teile += regel_fehler
        hinweis = None
        erster = next((d for _, _, d in ergebnisse if not d["ok"]), None)
        if erster and erster.get("fehler"):
            hinweis = sandbox.fehler_erklaeren(erster["fehler"])
        elif erster and erster.get("fast"):
            hinweis = erster["meldung"]
        return self._ergebnis(False, " ".join(teile), details=details, hinweis=hinweis)


# ──────────────────────────────────────────────────────────────────────────
#  Kapitel
# ──────────────────────────────────────────────────────────────────────────

class _Lernziele(list):
    """Liste, die man auch aufrufen kann: k.lernziele([...]) setzt die Ziele."""

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
    def __init__(self, slug, nummer, titel, beschreibung="", quelle="", teil="bonus", icon="📘"):
        self.slug = slug
        self.nummer = nummer
        self.titel = titel
        self.beschreibung = beschreibung
        self.quelle = quelle
        self.teil = teil
        self.icon = icon
        self.lernziele = _Lernziele()
        self.elemente = []
        self.zusammenfassung_text = None

    def __repr__(self):
        return f"<Kapitel {self.nummer} {self.slug}>"

    def _neu(self, element):
        element.kapitel = self
        if isinstance(element, Frage):
            with _LOCK:
                element.id = _frage_id(self.slug, element)
        self.elemente.append(element)
        return element

    def fragen(self):
        return [e for e in self.elemente if isinstance(e, Frage)]

    def erklaerungen(self):
        return [e for e in self.elemente if isinstance(e, Erklaerung)]

    def to_dict(self):
        fragen = self.fragen()
        return {"slug": self.slug, "nummer": self.nummer, "titel": self.titel,
                "beschreibung": self.beschreibung, "quelle": self.quelle, "teil": self.teil,
                "icon": self.icon, "lernziele": list(self.lernziele),
                "anzahl": {"erklaerungen": len(self.erklaerungen()),
                           "ueben": sum(f.phase == "ueben" for f in fragen),
                           "programmieren": sum(f.phase == "programmieren" for f in fragen),
                           "fragen": len(fragen)},
                "hat_zusammenfassung": self.zusammenfassung_text is not None}

    def elemente_dicts(self, mischen=True):
        """Elemente im Format von GET /api/kapitel/<slug> (ohne Lösungen)."""
        liste = []
        for e in self.elemente:
            if isinstance(e, Frage):
                liste.append({"typ": "frage", "frage": e.to_dict(mischen)})
            else:
                liste.append(e.to_dict())
        return liste

    # Abkürzungen für die Inhalte:
    def erklaerung(self, titel, text):
        return self._neu(Erklaerung(titel, text))

    def zusammenfassung(self, text):
        self.zusammenfassung_text = text
        return self._neu(Zusammenfassung(text))

    def mc(self, frage, optionen, erklaerung="", code=None, tipp=None):
        return self._neu(MC(frage, optionen, erklaerung, code, tipp))

    def wf(self, aussage, wahr, erklaerung="", code=None, tipp=None):
        return self._neu(WahrFalsch(aussage, wahr, erklaerung, code, tipp))

    def text(self, frage, antworten, erklaerung="", tipp=None, code=None, gross_klein=False):
        return self._neu(Textfrage(frage, antworten, erklaerung, tipp, code, gross_klein))

    def ausgabe(self, code, erklaerung="", tipp=None, akzeptiert=(), frage=None):
        return self._neu(Ausgabe(code, erklaerung, frage, tipp, akzeptiert))

    def ausdruck(self, frage, tests, loesung, erklaerung="", tipp=None, muss_enthalten=None):
        return self._neu(Ausdruck(frage, tests, loesung, erklaerung, tipp, muss_enthalten))

    def luecke(self, frage, code, antworten, erklaerung="", tipp=None):
        return self._neu(Luecke(frage, code, antworten, erklaerung, tipp))

    def puzzle(self, aufgabe, loesungscode, erklaerung="", tipp=None, ablenker=()):
        return self._neu(Puzzle(aufgabe, loesungscode, erklaerung, tipp, ablenker))

    def code(self, aufgabe, tests, loesung, erklaerung="", tipp=None, vorlage=None,
             verboten=(), pflicht=(), rekursiv=None, tipps=None, regeln=(), streng=False):
        return self._neu(CodeAufgabe(aufgabe, tests, loesung, erklaerung, tipp, vorlage,
                                     verboten, pflicht, rekursiv, tipps, regeln, streng))


_SLUG_RE = re.compile(r"^[a-z0-9_]+$")


def neues_kapitel(slug, titel, beschreibung="", quelle="", teil="bonus", icon="📘"):
    """Legt ein neues Kapitel an und hängt es an KAPITEL an."""
    if not _SLUG_RE.match(slug or ""):
        raise ValueError(f"Ungültiger slug {slug!r} (nur a-z, 0-9 und _ erlaubt)")
    if teil not in TEIL_IDS:
        raise ValueError(f"Unbekannter teil {teil!r} – erlaubt: {', '.join(TEIL_IDS)}")
    with _LOCK:
        if slug in _KAPITEL_NACH_SLUG:
            raise ValueError(f"Den slug {slug!r} gibt es schon")
        k = Kapitel(slug, len(KAPITEL) + 1, titel, beschreibung, quelle, teil, icon)
        KAPITEL.append(k)
        _KAPITEL_NACH_SLUG[slug] = k
    return k


def kapitel_nach_slug(slug):
    return _KAPITEL_NACH_SLUG.get(slug)


def kapitel_von_teil(teil):
    return [k for k in KAPITEL if k.teil == teil]


def alle_fragen():
    """dict[id, Frage] über alle Kapitel."""
    return {f.id: f for k in KAPITEL for f in k.fragen()}


def frage_nach_id(fid):
    return alle_fragen().get(fid)


def vorberechnen(max_workers=8):
    """Berechnet die Lösungen aller Ausgabe-Fragen und Funktionstests vorab
       (z. B. im Hintergrund beim Serverstart), damit Antworten schneller kommen."""
    aufgaben = []
    for f in alle_fragen().values():
        if isinstance(f, Ausgabe):
            aufgaben.append(f.soll)
        elif isinstance(f, CodeAufgabe):
            aufgaben.append(lambda f=f: sandbox.loesungswerte_berechnen(f.loesung, f.tests))
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        for z in [pool.submit(a) for a in aufgaben]:
            try:
                z.result()
            except Exception:
                pass


def inhalte_laden():
    """Importiert vorkurs.inhalte (füllt KAPITEL). Mehrfacher Aufruf schadet nicht."""
    from . import inhalte  # noqa: F401


inhalte_laden()
