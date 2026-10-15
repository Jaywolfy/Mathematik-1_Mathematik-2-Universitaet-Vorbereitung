# -*- coding: utf-8 -*-
"""Parser für Erklärungstexte (Markup, siehe ARCHITEKTUR.md Abschnitt 3).

markup.parse(text) -> Liste von Seiten, jede Seite ist eine Liste von Blöcken.
markup.pruefen(text) -> Liste von Problemen (für den Selbsttest).

Gegenüber dem Vorkurs neu: $…$ / $$…$$ (Formeln), :::rechnung (vorgerechnetes
Beispiel), :::alt (zweite Erklärung), :::warum (Informatik-Bezug), [[Glossar]].
"""

import json
import re
import textwrap

from . import visuals

VISUAL_TYPEN = visuals.VISUAL_TYPEN
BOX_ARTEN = ("analogie", "achtung", "info", "warum", "beispiel")
DIREKTIVEN = BOX_ARTEN + ("visual", "vergleich", "rechnung", "alt")

_LISTE_RE = re.compile(r"^( {0,3})([•\-*])\s+(\S.*)$")
_NUMMER_RE = re.compile(r"^( {0,3})(\d{1,3})\.\s+(\S.*)$")
_TABELLE_TRENN_RE = re.compile(r"^\|[\s:\-|]+\|$")
_SPALTEN_RE = re.compile(r"\S {2,}\S")
_RAHMEN_RE = re.compile(r"[─│┌┐└┘├┤┬┴┼═║╔╗╚╝]")

# Inline-Bausteine: `code` zuerst, dann $Formel$, im Rest **fett**, *kursiv*, [[Glossar]]
INLINE_TEIL_RE = re.compile(r"(`[^`]*`|(?<!\\)\$(?!\$)(?:\\.|[^$\\])+?(?<!\\)\$)")
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
INLINE_FORMEL_RE = re.compile(r"(?<!\\)\$(?!\$)((?:\\.|[^$\\])+?)(?<!\\)\$")
INLINE_FETT_RE = re.compile(r"(?<![\w*])\*\*(?=\S)(.+?)(?<=\S)\*\*(?![\w*])")
INLINE_KURSIV_RE = re.compile(r"(?<![\w*])\*(?=[^\s*`])([^*`\n]*?[^\s*`])\*(?![\w*])")
# Begriff beginnt mit Buchstabe: JSON wie [[5, 2]] in :::visual ist kein Glossar-Link
GLOSSAR_RE = re.compile(r"\[\[([^\W\d_][^\]|]*)(?:\|([^\]]+))?\]\]")


# ──────────────────────────────────────────────────────────────────────────
#  Öffentliche Funktionen
# ──────────────────────────────────────────────────────────────────────────

def parse(text):
    seiten, _ = _parse_mit_problemen(text)
    return seiten


def pruefen(text):
    _, probleme = _parse_mit_problemen(text)
    return probleme


def alle_bloecke(seiten):
    for seite in seiten:
        yield from _bloecke_flach(seite)


def inline_teile(text):
    """Zerlegt Text in [(art, inhalt)] mit art = 'text' | 'code' | 'formel'."""
    erg = []
    for i, teil in enumerate(INLINE_TEIL_RE.split(str(text or ""))):
        if not teil:
            continue
        if i % 2 == 1:
            erg.append(("code", teil[1:-1]) if teil.startswith("`") else ("formel", teil[1:-1]))
        else:
            erg.append(("text", teil))
    return erg


def formeln_im_text(text):
    return [inhalt for art, inhalt in inline_teile(text) if art == "formel"]


def formeln(seiten):
    """Alle LaTeX-Formeln einer Seitenliste (inline, abgesetzt, Rechnungen, Visual-Texte)."""
    erg = []
    for b in alle_bloecke(seiten):
        typ = b["typ"]
        if typ in ("absatz", "merke", "ueberschrift"):
            erg += formeln_im_text(b["text"])
        elif typ == "liste":
            for p in b["punkte"]:
                erg += formeln_im_text(p)
        elif typ == "tabelle":
            for z in [b["kopf"]] + b["zeilen"]:
                for c in z:
                    erg += formeln_im_text(c)
        elif typ == "formel":
            erg.append(b["tex"])
        elif typ == "rechnung":
            for s in b["schritte"]:
                erg.append(s["tex"])
                erg += formeln_im_text(s["grund"])
        elif typ == "box" or typ == "alt":
            erg += formeln_im_text(b.get("titel", ""))
        elif typ == "visual" and not b.get("fehler"):
            erg += formeln_im_text(b["daten"].get("unterschrift", ""))
    return erg


def glossar_verweise(text):
    """Begriffe aus [[Begriff]] / [[Text|Begriff]]."""
    return [(m.group(2) or m.group(1)).strip() for m in GLOSSAR_RE.finditer(str(text or ""))]


def ohne_inline(text):
    """Text ohne Inline-Markup (Formeln als lesbarer Text)."""
    erg = []
    for art, inhalt in inline_teile(text):
        if art == "formel":
            erg.append(latex_zu_text(inhalt))
        elif art == "code":
            erg.append(inhalt)
        else:
            t = GLOSSAR_RE.sub(lambda m: m.group(1), inhalt)
            t = INLINE_KURSIV_RE.sub(r"\1", t).replace("**", "")
            erg.append(t.replace("\\$", "$"))
    return "".join(erg)


def woerter(seite):
    """Wörter auf einer Seite (ohne Formeln, Rechnungen, Visuals, Alternative)."""
    n = 0
    for b in seite:
        if b["typ"] in ("visual", "rechnung", "formel", "alt"):
            continue
        for x in _bloecke_flach([b]):
            if x["typ"] in ("absatz", "merke", "ueberschrift"):
                n += _wortzahl(x["text"])
            elif x["typ"] == "liste":
                n += sum(_wortzahl(p) for p in x["punkte"])
            elif x["typ"] == "tabelle":
                n += sum(_wortzahl(c) for z in [x["kopf"]] + x["zeilen"] for c in z)
    return n


def _wortzahl(text):
    nur_text = " ".join(inhalt for art, inhalt in inline_teile(text) if art == "text")
    return len(re.findall(r"[A-Za-zÄÖÜäöüß]{2,}", nur_text))


def inline_saeubern(text):
    """Einzelnes '**' (kein Fett-Paar) wird zu `**`. Formeln und Code bleiben unberührt."""
    if "**" not in text:
        return text
    teile = INLINE_TEIL_RE.split(text)
    for i in range(0, len(teile), 2):
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
#  LaTeX -> lesbarer Text (Fallback für Titel, Tooltips, ohne KaTeX)
# ──────────────────────────────────────────────────────────────────────────

_SYMBOLE = {
    "cdot": "·", "times": "×", "div": "÷", "pm": "±", "le": "≤", "leq": "≤", "ge": "≥", "geq": "≥",
    "neq": "≠", "ne": "≠", "approx": "≈", "infty": "∞", "pi": "π", "alpha": "α", "beta": "β",
    "gamma": "γ", "delta": "δ", "Delta": "Δ", "epsilon": "ε", "varepsilon": "ε", "lambda": "λ", "mu": "μ",
    "sigma": "σ", "Sigma": "Σ", "phi": "φ", "varphi": "φ", "omega": "ω", "Omega": "Ω", "theta": "θ",
    "rho": "ρ", "tau": "τ", "Gamma": "Γ", "Pi": "Π", "Lambda": "Λ", "chi": "χ", "psi": "ψ", "eta": "η",
    "in": "∈", "notin": "∉", "subset": "⊂", "subseteq": "⊆", "supseteq": "⊇", "cup": "∪", "cap": "∩",
    "setminus": "∖", "emptyset": "∅", "varnothing": "∅", "forall": "∀", "exists": "∃", "neg": "¬",
    "lnot": "¬", "land": "∧", "wedge": "∧", "lor": "∨", "vee": "∨", "Rightarrow": "⇒", "Leftarrow": "⇐",
    "Leftrightarrow": "⇔", "rightarrow": "→", "to": "→", "mapsto": "↦", "implies": "⇒", "iff": "⇔",
    "sum": "Σ", "prod": "Π", "int": "∫", "partial": "∂", "nabla": "∇", "ldots": "…", "cdots": "⋯",
    "dots": "…", "mid": "|", "circ": "∘", "equiv": "≡", "oplus": "⊕", "perp": "⊥", "parallel": "∥",
    "langle": "⟨", "rangle": "⟩", "lfloor": "⌊", "rfloor": "⌋", "lceil": "⌈", "rceil": "⌉",
    "quad": " ", "qquad": "  ", "lvert": "|", "rvert": "|", "vert": "|", "ast": "*", "aleph": "ℵ",
}
_MENGEN = {"N": "ℕ", "Z": "ℤ", "Q": "ℚ", "R": "ℝ", "C": "ℂ"}
_HOCH = str.maketrans("0123456789+-=()niknx", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱᵏⁿˣ")
_TIEF = str.maketrans("0123456789+-=()aeijknx", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑᵢⱼₖₙₓ")


def latex_zu_text(tex):
    s = str(tex)
    s = re.sub(r"\\mathbb\{(\w)\}", lambda m: _MENGEN.get(m.group(1), m.group(1)), s)
    s = re.sub(r"\\(?:text|mathrm|operatorname|mathbf|textbf|mathit|hl|boxed)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\(?:textcolor|color)\{[^{}]*\}", "", s)
    s = re.sub(r"\\htmlClass\{[^{}]*\}", "", s)
    for _ in range(4):
        s = re.sub(r"\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}", lambda m: f"{_kl(m.group(1))}/{_kl(m.group(2))}", s)
        s = re.sub(r"\\sqrt\{([^{}]*)\}", lambda m: f"√{_kl(m.group(1))}", s)
        s = re.sub(r"\\binom\{([^{}]*)\}\{([^{}]*)\}", r"(\1 über \2)", s)
        s = re.sub(r"\^\{([^{}]*)\}", lambda m: _hoch(m.group(1)), s)
        s = re.sub(r"_\{([^{}]*)\}", lambda m: _tief(m.group(1)), s)
    s = re.sub(r"\^(\w)", lambda m: _hoch(m.group(1)), s)
    s = re.sub(r"_(\w)", lambda m: _tief(m.group(1)), s)
    s = re.sub(r"\\(left|right|big|Big|bigl|bigr|displaystyle)", "", s)
    s = re.sub(r"\\([A-Za-z]+)", lambda m: _SYMBOLE.get(m.group(1), m.group(1)), s)
    s = s.replace("\\{", "{").replace("\\}", "}").replace("\\,", " ").replace("\\;", " ").replace("\\ ", " ")
    s = s.replace("{,}", ",").replace("{", "").replace("}", "").replace("\\\\", "; ").replace("&", " ")
    return re.sub(r"\s+", " ", s).strip()


def _kl(s):
    return s if re.fullmatch(r"[\w.,]+", s) else f"({s})"


def _hoch(s):
    t = s.translate(_HOCH)
    return t if all(c in "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱᵏˣ" for c in t) else f"^({s})"


def _tief(s):
    t = s.translate(_TIEF)
    return t if all(c in "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑᵢⱼₖₙₓ" for c in t) else f"_{s}"


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
            seiten[-1].extend(_bloecke(puffer, probleme))
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
        if s.startswith("$$"):
            puffer_leeren()
            inhalt = s[2:]
            if inhalt.rstrip().endswith("$$") and len(inhalt.rstrip()) >= 2:
                tex = inhalt.rstrip()[:-2]
                i += 1
            else:
                teile = [inhalt]
                i += 1
                while i < len(zeilen) and not zeilen[i].rstrip().endswith("$$"):
                    teile.append(zeilen[i].strip())
                    i += 1
                if i >= len(zeilen):
                    probleme.append("Abgesetzte Formel $$ … wird nicht mit $$ geschlossen.")
                else:
                    teile.append(zeilen[i].rstrip()[:-2].strip())
                    i += 1
                tex = "\n".join(teile)
            seiten[-1].append({"typ": "formel", "tex": tex.strip()})
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
    eigene = []
    for seite in seiten:
        for b in alle_bloecke([seite]):
            for tex in _formeln_eines_blocks(b):
                from . import pruefer
                for p in pruefer.latex_pruefen(tex):
                    eigene.append(f"Formel ${tex[:50]}$: {p}")
            for text in _texte_eines_blocks(b):
                if re.search(r"(?<!\\)\$", INLINE_TEIL_RE.sub("", text)):
                    eigene.append(f"Einzelnes $ ohne Gegenstück in: {text[:60]!r} (für ein Dollarzeichen \\$ schreiben)")
                for ctrl in "\f\b\a\v":
                    if ctrl in text:
                        eigene.append(f"Steuerzeichen im Text {text[:40]!r} – r-String vergessen?")
    return seiten, list(dict.fromkeys(probleme + eigene))


def _texte_eines_blocks(b):
    typ = b["typ"]
    if typ in ("absatz", "merke", "ueberschrift"):
        return [b["text"]]
    if typ == "liste":
        return list(b["punkte"])
    if typ == "tabelle":
        return [c for z in [b["kopf"]] + b["zeilen"] for c in z]
    if typ == "rechnung":
        return [s["grund"] for s in b["schritte"]]
    return []


def _formeln_eines_blocks(b):
    typ = b["typ"]
    if typ == "formel":
        return [b["tex"]]
    if typ == "rechnung":
        return [s["tex"] for s in b["schritte"]] + [f for s in b["schritte"] for f in formeln_im_text(s["grund"])]
    erg = []
    for t in _texte_eines_blocks(b):
        erg += formeln_im_text(t)
    if typ == "box":
        erg += formeln_im_text(b.get("titel", ""))
    return erg


def _unter(roh, probleme):
    """Inhalt einer Box/Alternative: volles Markup (auch $$ und :::visual), Seiten flach."""
    unter, p2 = _parse_mit_problemen(roh)
    probleme.extend(p2)
    return [b for s in unter for b in s]


def _direktive(kopf, inhalt, probleme):
    name, _, rest = kopf.partition(" ")
    name = name.strip().lower()
    rest = rest.strip()
    roh = textwrap.dedent("\n".join(inhalt)).strip("\n")

    if name in BOX_ARTEN:
        return {"typ": "box", "art": name, "titel": rest, "bloecke": _unter(roh, probleme)}

    if name == "alt":
        if not roh.strip():
            probleme.append("':::alt' ist leer.")
        return {"typ": "alt", "titel": rest or "Noch einmal anders erklärt", "bloecke": _unter(roh, probleme)}

    if name == "rechnung":
        schritte = []
        for z in roh.splitlines():
            if not z.strip():
                continue
            falsch = z.lstrip().startswith("!")
            widerspruch = z.lstrip().startswith("#")
            frei = z.lstrip().startswith("??")      # "?? ": vom Nachrechnen ausgenommen (ohne Warnung)
            z = z.lstrip()[1:] if falsch or widerspruch else (z.lstrip()[2:] if frei else z)
            tex, _, grund = z.partition("||")
            if not tex.strip():
                probleme.append(f"':::rechnung': Zeile ohne Formel: {z!r}")
                continue
            schritt = {"tex": tex.strip(), "grund": grund.strip(), "falsch": falsch}
            if widerspruch:
                schritt["widerspruch"] = True
            if frei:
                schritt["ungeprueft"] = True
            schritte.append(schritt)
        if not schritte:
            probleme.append("':::rechnung' enthält keine Schritte.")
        return {"typ": "rechnung", "titel": rest, "schritte": schritte}

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
        if not fehler:
            schema = visuals.pruefen(art, daten)
            if schema:
                fehler = "; ".join(schema)
        if not fehler:
            try:
                visuals.ergaenzen(art, daten)
            except Exception as e:  # noqa: BLE001 – jede Ausnahme ist ein Inhaltsfehler
                fehler = f"Visual '{art}' konnte nicht berechnet werden: {type(e).__name__}: {e}"
        if fehler:
            probleme.append(f":::visual {art}: {fehler}")
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
        spalten = [_bloecke(textwrap.dedent("\n".join(seite)).strip("\n").splitlines(), probleme)
                   for seite in (links, rechts)]
        return {"typ": "vergleich", "titel": titel[:2], "spalten": spalten}

    probleme.append(f"Unbekannte Direktive ':::{name}'. Erlaubt: {', '.join(DIREKTIVEN)}")
    return {"typ": "box", "art": "info", "titel": rest, "bloecke": _bloecke(roh.splitlines(), probleme)}


# ──────────────────────────────────────────────────────────────────────────
#  Normale Zeilen -> Blöcke
# ──────────────────────────────────────────────────────────────────────────

def _einzug(zeile):
    return len(zeile) - len(zeile.lstrip(" "))


def _vorformatiert(s):
    return bool(_SPALTEN_RE.search(s) or _RAHMEN_RE.search(s))


def _tabellen_zellen(s):
    """'| a | $|x|$ |' -> ['a', '$|x|$'] (| in Formeln und Code trennt nicht)."""
    innen = s[1:-1]
    zellen, aktuell, i = [], "", 0
    teile = INLINE_TEIL_RE.split(innen)
    for k, teil in enumerate(teile):
        if k % 2 == 1:
            aktuell += teil
            continue
        for c in teil:
            if c == "|":
                zellen.append(aktuell.strip())
                aktuell = ""
            else:
                aktuell += c
    zellen.append(aktuell.strip())
    return zellen


def _bloecke(zeilen, probleme=None):
    bloecke = []
    offen = None
    daten = {}
    leer_davor = False

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
                daten["zeilen"].append(_tabellen_zellen(s))
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
            daten["punkte"][-1] += " " + s
        elif (offen == "absatz" and daten.get("spalte") is not None and not leer_davor
              and abs(e - daten["spalte"]) <= 1):
            daten["zeilen"].append(s)
        elif e >= 4 or (e >= 1 and _vorformatiert(s)):
            listenspalte = (daten.get("spalte") if offen in ("liste", "absatz") and not leer_davor else None)
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
        if b["typ"] in ("box", "alt"):
            yield from _bloecke_flach(b["bloecke"])
        elif b["typ"] == "vergleich":
            for spalte in b["spalten"]:
                yield from _bloecke_flach(spalte)
