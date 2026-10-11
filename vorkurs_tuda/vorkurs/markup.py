# -*- coding: utf-8 -*-
"""Parser für Erklärungstexte (Markup, siehe ARCHITEKTUR.md Abschnitt 3).

markup.parse(text) -> Liste von Seiten, jede Seite ist eine Liste von Blöcken.
markup.pruefen(text) -> Liste von Problemen (für den Selbsttest).
"""

import ast
import itertools
import json
import re
import textwrap

VISUAL_TYPEN = (
    "variablen", "liste", "string", "dict", "referenz", "ablauf", "entscheidung",
    "schleife", "zahlenstrahl", "wahrheitstabelle", "stapel", "baum", "funktion",
    "typen",
)
BOX_ARTEN = ("analogie", "achtung", "info")
DIREKTIVEN = BOX_ARTEN + ("code", "trace", "visual", "vergleich")

_LISTE_RE = re.compile(r"^( {0,3})([•\-*])\s+(\S.*)$")
_NUMMER_RE = re.compile(r"^( {0,3})(\d{1,3})\.\s+(\S.*)$")
_TABELLE_TRENN_RE = re.compile(r"^\|[\s:\-|]+\|$")
# Zeilen, die als "vorformatiert" gelten (ASCII-Tabellen, ausgerichtete Spalten)
_SPALTEN_RE = re.compile(r"\S {2,}\S")
_RAHMEN_RE = re.compile(r"[─│┌┐└┘├┤┬┴┼═║╔╗╚╝]")


# ──────────────────────────────────────────────────────────────────────────
#  Öffentliche Funktionen
# ──────────────────────────────────────────────────────────────────────────

def parse(text):
    """Zerlegt Markup in Seiten (Listen von Block-Dicts)."""
    seiten, _ = _parse_mit_problemen(text)
    return seiten


def pruefen(text):
    """Liefert eine Liste von Problemen (leere Liste = alles in Ordnung)."""
    _, probleme = _parse_mit_problemen(text)
    return probleme


def alle_bloecke(seiten):
    """Alle Blöcke (auch die in Boxen und Vergleichen) nacheinander."""
    for seite in seiten:
        yield from _bloecke_flach(seite)


def code_beispiele(seiten):
    """Alle ausführbaren Beispiele (:::code und :::trace) einer Seitenliste."""
    return [b for b in alle_bloecke(seiten) if b["typ"] == "code"]


def ohne_inline(text):
    """Entfernt Inline-Markup (`code`, **fett**, *kursiv*) – z. B. für Terminal ohne Farben."""
    teile = re.split(r"(`[^`]*`)", text)
    for i in range(0, len(teile), 2):          # *kursiv* nur außerhalb von `code`
        teile[i] = INLINE_KURSIV_RE.sub(r"\1", teile[i])
    return "".join(teile).replace("**", "").replace("`", "")


# Empfohlene Muster für Oberflächen (fett nur, wenn ** nicht an Wortzeichen klebt):
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
INLINE_FETT_RE = re.compile(r"(?<![\w*])\*\*(?=\S)(.+?)(?<=\S)\*\*(?![\w*])")
# *kursiv*: einzelne Sternchen, direkt innen kein Leerzeichen, außen kein Wortzeichen/Stern.
# So bleiben `a * b`, `*args`, `2*3*4` und `**` (Potenz) unberührt. Kein `code` im Kursivtext.
INLINE_KURSIV_RE = re.compile(r"(?<![\w*])\*(?=[^\s*`])([^*`\n]*?[^\s*`])\*(?![\w*])")


def inline_saeubern(text):
    """Macht einzelne '**' (z. B. Potenz-Operator 2 ** 10) zu `**`, damit sie
       nicht als Fettdruck missverstanden werden. Echte **fett**-Paare bleiben."""
    if "**" not in text:
        return text
    teile = re.split(r"(`[^`]*`)", text)
    for i in range(0, len(teile), 2):          # gerade Indizes = außerhalb von `code`
        stueck = teile[i]
        ergebnis, pos = [], 0
        for m in INLINE_FETT_RE.finditer(stueck):
            ergebnis.append(stueck[pos:m.start()].replace("**", "`**`"))
            ergebnis.append(m.group(0))
            pos = m.end()
        ergebnis.append(stueck[pos:].replace("**", "`**`"))
        teile[i] = "".join(ergebnis)
    return "".join(teile)


# ──────────────────────────────────────────────────────────────────────────
#  Seiten und Direktiven
# ──────────────────────────────────────────────────────────────────────────

def _parse_mit_problemen(text):
    probleme = []
    zeilen = textwrap.dedent((text or "").expandtabs(4)).strip("\n").splitlines()
    seiten = [[]]
    puffer = []

    def puffer_leeren():
        if puffer:
            seiten[-1].extend(_bloecke(puffer))
            puffer.clear()

    i = 0
    while i < len(zeilen):
        zeile = zeilen[i]
        s = zeile.strip()
        if s == "---":
            puffer_leeren()
            seiten.append([])
            i += 1
            continue
        if s.startswith(":::") and s != ":::":
            puffer_leeren()
            kopf = s[3:].strip()
            inhalt = []
            i += 1
            while i < len(zeilen) and zeilen[i].strip() != ":::":
                inhalt.append(zeilen[i])
                i += 1
            if i >= len(zeilen):
                probleme.append(f"Direktive ':::{kopf}' wurde nicht mit ':::' geschlossen.")
            i += 1
            block = _direktive(kopf, inhalt, probleme)
            if block is not None:
                seiten[-1].append(block)
            continue
        puffer.append(zeile)
        i += 1
    puffer_leeren()
    seiten = [s for s in seiten if s] or [[]]
    return seiten, probleme


def _direktive(kopf, inhalt, probleme):
    name, _, rest = kopf.partition(" ")
    name = name.strip().lower()
    rest = rest.strip()
    roh = textwrap.dedent("\n".join(inhalt)).strip("\n")

    if name in BOX_ARTEN:
        return {"typ": "box", "art": name, "titel": rest, "bloecke": _bloecke(roh.splitlines())}

    if name in ("code", "trace"):
        eingaben = []
        m = re.search(r"eingaben\s*=\s*(.*)$", rest)
        if m:
            eingaben = [e.strip() for e in m.group(1).split("|")]
        if not roh.strip():
            probleme.append(f"':::{name}' enthält keinen Code.")
        return {"typ": "code", "code": roh, "eingaben": eingaben, "trace": name == "trace"}

    if name == "visual":
        art = rest.split()[0].lower() if rest else ""
        fehler = None
        daten = {}
        try:
            daten = json.loads(roh) if roh.strip() else {}
            if not isinstance(daten, dict):
                fehler = "Das JSON muss ein Objekt {...} sein."
                daten = {}
        except ValueError as e:
            fehler = f"Ungültiges JSON: {e}"
        if not fehler and art not in VISUAL_TYPEN:
            fehler = f"Unbekannter Visual-Typ '{art}'. Erlaubt: {', '.join(VISUAL_TYPEN)}"
        if not fehler:
            try:
                _visual_ergaenzen(art, daten)
            except Exception as e:  # Ergänzungen sind nur ein Bonus
                fehler = f"Visual '{art}' konnte nicht ausgewertet werden: {e}"
        if fehler:
            probleme.append(f":::visual {art}: {fehler}")
        elif art == "wahrheitstabelle":
            for nr, a in enumerate(daten.get("ausdruecke", [])):
                if any(z["ergebnisse"][nr] is None for z in daten.get("zeilen", [])):
                    probleme.append(f":::visual wahrheitstabelle: Ausdruck {a!r} kann nicht "
                                    "ausgewertet werden (erlaubt: Variablen, True/False, and, or, "
                                    "not, ^, &, |, ==, !=, Klammern).")
        return {"typ": "visual", "art": art, "daten": daten, "fehler": fehler}

    if name == "vergleich":
        titel = [t.strip() for t in rest.split("|", 1)] if rest else ["", ""]
        while len(titel) < 2:
            titel.append("")
        links, rechts, gefunden = [], [], False
        for z in inhalt:
            if z.strip() == "|||" and not gefunden:
                gefunden = True
                continue
            (rechts if gefunden else links).append(z)
        if not gefunden:
            probleme.append("':::vergleich' braucht eine Zeile '|||' zwischen linker und rechter Seite.")
        spalten = [_bloecke(textwrap.dedent("\n".join(seite)).strip("\n").splitlines())
                   for seite in (links, rechts)]
        return {"typ": "vergleich", "titel": titel[:2], "spalten": spalten}

    probleme.append(f"Unbekannte Direktive ':::{name}'. Erlaubt: {', '.join(DIREKTIVEN)}")
    return {"typ": "box", "art": "info", "titel": rest, "bloecke": _bloecke(roh.splitlines())}


def py_anzeige(w):
    """JSON-Wert so, wie Python ihn anzeigen würde (2.0 bleibt "2.0", 'a' mit Quotes)."""
    if isinstance(w, list):
        return "[" + ", ".join(py_anzeige(x) for x in w) + "]"
    if isinstance(w, dict):
        return "{" + ", ".join(f"{py_anzeige(k)}: {py_anzeige(v)}" for k, v in w.items()) + "}"
    return repr(w)


def py_wert(w, tiefe=0):
    """JSON-Wert -> WERT-Struktur wie beim Tracer ({"typ", "repr", "elemente"/"paare"})."""
    typen = {bool: "bool", int: "int", float: "float", str: "str", type(None): "NoneType",
             list: "list", dict: "dict"}
    erg = {"typ": typen.get(type(w), "andere"), "repr": py_anzeige(w)}
    if isinstance(w, list) and tiefe < 3:
        erg["elemente"] = [py_wert(x, tiefe + 1) for x in w]
    elif isinstance(w, dict) and tiefe < 3:
        erg["paare"] = [[py_wert(k, tiefe + 1), py_wert(v, tiefe + 1)] for k, v in w.items()]
    return erg


def _variable_ergaenzen(v):
    if isinstance(v, dict) and "wert" in v:
        w = v["wert"]
        v["anzeige"] = w if isinstance(w, str) else py_anzeige(w)


def _visual_ergaenzen(art, daten):
    """Berechnet Zusatzfelder, die beide Oberflächen nutzen können.

    Python-Darstellung der Werte (JSON/JavaScript verlieren z. B. bei 2.0 die
    Nachkommastelle): liste -> "werte_anzeige", dict -> "paare_anzeige",
    variablen -> je Variable "anzeige", referenz -> "objekte_anzeige" + "objekte_werte".
    """
    if art == "liste" and isinstance(daten.get("werte"), list):
        daten["werte_anzeige"] = [py_anzeige(w) for w in daten["werte"]]
    elif art == "dict" and isinstance(daten.get("paare"), list):
        daten["paare_anzeige"] = [[py_anzeige(p[0]), py_anzeige(p[1])]
                                  if isinstance(p, (list, tuple)) and len(p) >= 2 else ["?", "?"]
                                  for p in daten["paare"]]
    elif art == "variablen":
        for v in daten.get("vars") or []:
            _variable_ergaenzen(v)
        for schritt in daten.get("schritte") or []:
            for v in schritt if isinstance(schritt, list) else []:
                _variable_ergaenzen(v)
    elif art == "referenz" and isinstance(daten.get("objekte"), list):
        daten["objekte_anzeige"] = [py_anzeige(o) for o in daten["objekte"]]
        daten["objekte_werte"] = [py_wert(o) for o in daten["objekte"]]
    if art == "typen":
        typen = []
        for w in daten.get("werte", []):
            try:
                typ = type(ast.literal_eval(str(w))).__name__
            except (ValueError, SyntaxError):
                typ = "unbekannt"
            typen.append({"wert": str(w), "typ": typ})
        daten["typen"] = typen
    elif art == "wahrheitstabelle":
        variablen = [str(v) for v in daten.get("variablen", [])]
        ausdruecke = [str(a) for a in daten.get("ausdruecke", [])]
        zeilen = []
        for werte in itertools.product([True, False], repeat=len(variablen)):
            belegung = dict(zip(variablen, werte))
            zeilen.append({"werte": list(werte),
                           "ergebnisse": [_logik_auswerten(a, belegung) for a in ausdruecke]})
        daten["zeilen"] = zeilen


_ERLAUBTE_KNOTEN = (ast.Expression, ast.BoolOp, ast.UnaryOp, ast.Not, ast.And, ast.Or,
                    ast.Name, ast.Load, ast.Constant, ast.Compare, ast.Eq, ast.NotEq,
                    ast.BinOp, ast.BitXor, ast.BitAnd, ast.BitOr)


def _logik_auswerten(ausdruck, belegung):
    """Wertet einen and/or/not-Ausdruck sicher aus (auch ^, &, |, ==, !=; sonst None)."""
    try:
        baum = ast.parse(ausdruck, mode="eval")
    except SyntaxError:
        return None
    if not all(isinstance(k, _ERLAUBTE_KNOTEN) for k in ast.walk(baum)):
        return None
    try:
        erg = eval(compile(baum, "<logik>", "eval"), {"__builtins__": {}}, dict(belegung))
        return erg if isinstance(erg, bool) else bool(erg)
    except Exception:
        return None


# ──────────────────────────────────────────────────────────────────────────
#  Normale Zeilen -> Blöcke
# ──────────────────────────────────────────────────────────────────────────

def _einzug(zeile):
    return len(zeile) - len(zeile.lstrip(" "))


def _vorformatiert(s):
    return bool(_SPALTEN_RE.search(s) or _RAHMEN_RE.search(s))


def _bloecke(zeilen):
    """Wandelt Textzeilen (ohne Direktiven/Seitenumbrüche) in Blöcke um."""
    bloecke = []
    offen = None          # "absatz" | "liste" | "code" | "tabelle" | "merke" | None
    daten = {}            # Zustand des offenen Blocks
    leer_davor = False    # gab es seit der letzten Textzeile eine Leerzeile?

    def schliessen():
        nonlocal offen
        if offen == "absatz":
            bloecke.append({"typ": "absatz", "text": inline_saeubern(" ".join(daten["zeilen"]))})
        elif offen == "merke":
            bloecke.append({"typ": "merke", "text": inline_saeubern(" ".join(daten["zeilen"]))})
        elif offen == "liste":
            bloecke.append({"typ": "liste", "nummeriert": daten["nummeriert"],
                            "punkte": [inline_saeubern(p) for p in daten["punkte"]]})
        elif offen == "code":
            code = textwrap.dedent("\n".join(daten["zeilen"])).strip("\n")
            bloecke.append({"typ": "codeblock", "code": code})
        elif offen == "tabelle":
            kopf, *rest = [[inline_saeubern(c) for c in z] for z in daten["zeilen"]] or [[]]
            bloecke.append({"typ": "tabelle", "kopf": kopf, "zeilen": rest})
        offen = None
        daten.clear()

    for roh in zeilen:
        zeile = roh.rstrip()
        s = zeile.strip()
        if not s:
            leer_davor = True
            if offen in ("absatz", "merke", "tabelle"):
                schliessen()
            elif offen == "code":
                daten["leer"] += 1
            continue
        e = _einzug(zeile)

        # Codeblock fortsetzen?
        if offen == "code":
            ende_wegen_liste = daten.get("listenspalte") is not None and e <= daten["listenspalte"] + 1
            if not ende_wegen_liste and (e >= 4 or (e >= 1 and _vorformatiert(s))):
                daten["zeilen"].extend([""] * daten["leer"])
                daten["leer"] = 0
                daten["zeilen"].append(zeile)
                leer_davor = False
                continue
            listenspalte = daten.get("listenspalte")
            schliessen()
            if ende_wegen_liste:
                # Text, der nach einem Codebeispiel zu einem Listenpunkt gehört
                offen = "absatz"
                daten["zeilen"] = [s]
                daten["spalte"] = listenspalte
                leer_davor = False
                continue

        if e <= 3 and (s.startswith("## ") or s.startswith("### ")):
            schliessen()
            bloecke.append({"typ": "ueberschrift", "text": inline_saeubern(s.lstrip("#").strip())})
        elif e <= 3 and s.startswith("!!"):
            text = s[2:].strip()
            if offen == "merke" and not leer_davor:
                daten["zeilen"].append(text)
            else:
                schliessen()
                offen = "merke"
                daten["zeilen"] = [text]
        elif e <= 3 and len(s) >= 2 and s.startswith("|") and s.endswith("|"):
            if offen != "tabelle":
                schliessen()
                offen = "tabelle"
                daten["zeilen"] = []
            if not _TABELLE_TRENN_RE.match(s):
                daten["zeilen"].append([z.strip() for z in s[1:-1].split("|")])
        elif _LISTE_RE.match(zeile) or _NUMMER_RE.match(zeile):
            m = _LISTE_RE.match(zeile) or _NUMMER_RE.match(zeile)
            nummeriert = m.re is _NUMMER_RE
            if not (offen == "liste" and daten["nummeriert"] == nummeriert):
                schliessen()
                offen = "liste"
                daten["nummeriert"] = nummeriert
                daten["punkte"] = []
            daten["punkte"].append(m.group(3).strip())
            daten["spalte"] = m.start(3)
        elif offen == "liste" and not leer_davor and abs(e - daten["spalte"]) <= 1:
            daten["punkte"][-1] += " " + s          # Fortsetzungszeile eines Punktes
        elif (offen == "absatz" and daten.get("spalte") is not None and not leer_davor
              and abs(e - daten["spalte"]) <= 1):
            daten["zeilen"].append(s)
        elif e >= 4 or (e >= 1 and _vorformatiert(s)):
            listenspalte = (daten.get("spalte") if offen in ("liste", "absatz") and not leer_davor
                            else None)
            schliessen()
            offen = "code"
            daten["zeilen"] = [zeile]
            daten["leer"] = 0
            daten["listenspalte"] = listenspalte
        else:
            if offen == "absatz" and not leer_davor:
                daten["zeilen"].append(s)
            else:
                schliessen()
                offen = "absatz"
                daten["zeilen"] = [s]
        leer_davor = False
    schliessen()
    return bloecke


def _bloecke_flach(bloecke):
    for b in bloecke:
        yield b
        if b["typ"] == "box":
            yield from _bloecke_flach(b["bloecke"])
        elif b["typ"] == "vergleich":
            for spalte in b["spalten"]:
                yield from _bloecke_flach(spalte)
