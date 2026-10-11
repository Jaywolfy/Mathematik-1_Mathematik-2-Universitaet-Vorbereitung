"""Darstellung für das Terminal.

Alles, was hier steht, ERZEUGT nur Textzeilen (list[str]) – es wird nichts
eingelesen. Die Bedienung (Eingaben, Menüs) liegt in app.py / fragen.py.

Inhalt:
  * Farben (ANSI, abschaltbar) und Anzeigebreite (Emojis zählen doppelt)
  * Inline-Markup (`code`, **fett**) mit Zeilenumbruch
  * Syntax-Highlighting für Python (tokenize, robust bei kaputtem Code)
  * Rahmen, Tabellen, Code- und Ausgabekästen
  * alle Markup-Blöcke (ARCHITEKTUR.md Abschnitt 3)
  * alle Visualisierungen (Abschnitt 4) als Unicode-Grafik
  * eine Seite der Schritt-für-Schritt-Ansicht (sandbox.trace)
"""

from __future__ import annotations

import ast
import builtins
import io
import itertools
import keyword
import re
import shutil
import tokenize
import unicodedata

# ════════════════════════════════════════════════════════════════════════════
#  Farben
# ════════════════════════════════════════════════════════════════════════════

_FARBEN = True
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
RESET = "\x1b[0m"


def farben_setzen(an):
    global _FARBEN
    _FARBEN = bool(an)


def farben_an():
    return _FARBEN


def _stil(*codes):
    seq = "\x1b[" + ";".join(codes) + "m"

    def faerben(text):
        text = str(text)
        if not _FARBEN or not text:
            return text
        # Verschachtelung: nach jedem inneren Reset den äußeren Stil erneuern
        return seq + text.replace(RESET, RESET + seq) + RESET
    return faerben


fett = _stil("1")
duenn = _stil("2")
kursiv = _stil("3")
rot = _stil("91")
gruen = _stil("92")
gelb = _stil("93")
blau = _stil("94")
magenta = _stil("95")
cyan = _stil("96")
grau = _stil("90")
weiss = _stil("97")
hl_gruen = _stil("30", "102")    # schwarz auf hellgrün (Slice-Auswahl)
hl_gelb = _stil("30", "103")     # schwarz auf gelb (markiert)
hl_zeile = _stil("1", "97", "44")  # aktuelle Zeile im Tracer


def ohne_ansi(s):
    return ANSI_RE.sub("", str(s))


# ════════════════════════════════════════════════════════════════════════════
#  Breiten
# ════════════════════════════════════════════════════════════════════════════

EINZUG = "  "


def breite():
    """Nutzbare Zeilenbreite: Terminalbreite, aber mindestens 70, höchstens 100."""
    try:
        spalten = shutil.get_terminal_size((90, 24)).columns
    except Exception:  # pragma: no cover
        spalten = 90
    return max(70, min(100, spalten - 1))


def _zeichenbreite(ch):
    o = ord(ch)
    if o in (0x200D, 0xFE0E, 0xFE0F, 0x200B):
        return 0
    if unicodedata.combining(ch):
        return 0
    kat = unicodedata.category(ch)
    if kat in ("Mn", "Me", "Cf", "Cc"):
        return 0
    if unicodedata.east_asian_width(ch) in ("W", "F"):
        return 2
    return 1


def sichtbreite(s):
    """Anzeigebreite eines Textes im Terminal (ANSI-Codes zählen nicht,
    breite Zeichen/Emojis zählen doppelt, Zeichen nach ZWJ gar nicht)."""
    s = ANSI_RE.sub("", str(s))
    w = 0
    nach_zwj = False
    letzte = 0
    for ch in s:
        if nach_zwj:
            nach_zwj = False
            continue
        if ch == "‍":
            nach_zwj = True
            continue
        if ch == "️":
            if letzte == 1:     # Emoji-Darstellung macht schmale Symbole breit
                w += 1
                letzte = 2
            continue
        b = _zeichenbreite(ch)
        w += b
        if b:
            letzte = b
    return w


def pad(s, w, ausr="l"):
    """Füllt s mit Leerzeichen auf Anzeigebreite w auf (l, r oder c)."""
    s = str(s)
    d = w - sichtbreite(s)
    if d <= 0:
        return s
    if ausr == "r":
        return " " * d + s
    if ausr == "c":
        links = d // 2
        return " " * links + s + " " * (d - links)
    return s + " " * d


def _ansi_teile(s):
    """Zerlegt s in (text, ist_ansi)-Stücke."""
    pos = 0
    for m in ANSI_RE.finditer(s):
        if m.start() > pos:
            yield s[pos:m.start()], False
        yield m.group(), True
        pos = m.end()
    if pos < len(s):
        yield s[pos:], False


def _cluster(text):
    """Zerlegt Text in Graphem-ähnliche Einheiten (Emoji+ZWJ+Emoji bleibt zusammen)."""
    einheiten = []
    for ch in text:
        if einheiten and (ch in "‍️︎" or unicodedata.combining(ch)
                          or einheiten[-1].endswith("‍")):
            einheiten[-1] += ch
        else:
            einheiten.append(ch)
    return einheiten


def hart_umbrechen(s, w):
    """Bricht einen (evtl. farbigen) Text nach genau w Spalten um.
    Farben werden über den Umbruch hinweg fortgesetzt."""
    if w <= 0:
        return [s]
    zeilen, akt, akt_w, aktiv = [], "", 0, ""
    for stueck, ist_ansi in _ansi_teile(s):
        if ist_ansi:
            akt += stueck
            aktiv = "" if stueck == RESET else aktiv + stueck
            continue
        for e in _cluster(stueck):
            eb = sichtbreite(e)
            if akt_w + eb > w and akt_w > 0:
                zeilen.append(akt + (RESET if aktiv else ""))
                akt, akt_w = aktiv, 0
            akt += e
            akt_w += eb
    zeilen.append(akt)
    return zeilen


def abschneiden(s, w, ende="…"):
    """Kürzt einen (evtl. farbigen) Text auf Anzeigebreite w."""
    if sichtbreite(s) <= w:
        return s
    teile = hart_umbrechen(s, max(1, w - sichtbreite(ende)))
    return teile[0] + (RESET if _FARBEN and "\x1b[" in teile[0] else "") + ende


# ════════════════════════════════════════════════════════════════════════════
#  Inline-Markup und Zeilenumbruch
# ════════════════════════════════════════════════════════════════════════════

_INLINE_RE = re.compile(r"`([^`]+)`|\*\*(.+?)\*\*"
                        r"|(?<![\w*])\*(?=[^\s*`])([^*`\n]*?[^\s*`])\*(?![\w*])")   # *kursiv*


def inline_segmente(text):
    """'Das ist `x` und **wichtig**' -> [(txt, art)], art in '', 'code', 'fett', 'kursiv'."""
    segs, pos = [], 0
    for m in _INLINE_RE.finditer(text):
        if m.start() > pos:
            segs.append((text[pos:m.start()], ""))
        if m.group(1) is not None:
            segs.append((m.group(1), "code"))
        elif m.group(2) is not None:
            segs.append((m.group(2), "fett"))
        else:
            segs.append((m.group(3), "kursiv"))
        pos = m.end()
    if pos < len(text):
        segs.append((text[pos:], ""))
    return segs


def _seg_stil(txt, art, basis=None):
    if art == "code":
        if not _FARBEN:
            return "`" + txt + "`"
        return cyan(txt)
    if art == "fett":
        return fett(basis(txt) if basis else txt)
    if art == "kursiv":                 # ohne Farben: Text ohne Sternchen
        return kursiv(basis(txt) if basis else txt)
    return basis(txt) if basis else txt


def inline(text, basis=None):
    """Inline-Markup in farbigen Text umwandeln (ohne Umbruch)."""
    return "".join(_seg_stil(t, a, basis) for t, a in inline_segmente(str(text)))


def inline_plain(text):
    """Inline-Markup entfernen (für Breitenberechnung ohne Farben)."""
    return ohne_ansi(inline(text))


def umbrechen(text, w, basis=None):
    """Bricht Text mit Inline-Markup auf Breite w um. Code-Stücke werden
    möglichst nicht getrennt. Rückgabe: Liste farbiger Zeilen."""
    text = str(text)
    if not text.strip():
        return [""]
    woerter = []   # None = Leerraum, sonst Liste von (txt, art)
    akt = []
    for txt, art in inline_segmente(text):
        if art == "code":
            akt.append((txt, art))
            continue
        for teil in re.split(r"(\s+)", txt):
            if not teil:
                continue
            if teil.isspace():
                if akt:
                    woerter.append(akt)
                    akt = []
                woerter.append(None)
            else:
                akt.append((teil, art))
    if akt:
        woerter.append(akt)

    def wortbreite(wort):
        return sum(sichtbreite(_seg_stil(t, a)) for t, a in wort)

    zeilen, zeile, zw, leer = [], [], 0, False
    for wort in woerter:
        if wort is None:
            leer = bool(zeile)
            continue
        wb = wortbreite(wort)
        bedarf = wb + (1 if leer and zeile else 0)
        if zeile and zw + bedarf > w:
            zeilen.append(zeile)
            zeile, zw = [], 0
            bedarf = wb
        if zeile and leer:
            zeile.append((" ", ""))
        zeile.extend(wort)
        zw += bedarf
        leer = False
    if zeile:
        zeilen.append(zeile)

    ergebnis = []
    for z in zeilen:
        s = "".join(_seg_stil(t, a, basis) for t, a in z)
        ergebnis.extend(hart_umbrechen(s, w) if sichtbreite(s) > w else [s])
    return ergebnis or [""]


def haengend(praefix, text, w, basis=None, praefix_stil=None):
    """Text mit Präfix (z. B. '• ') und hängendem Einzug umbrechen."""
    pb = sichtbreite(praefix)
    zeilen = umbrechen(text, max(10, w - pb), basis)
    p = praefix_stil(praefix) if praefix_stil else praefix
    return [(p if i == 0 else " " * pb) + z for i, z in enumerate(zeilen)]


# ════════════════════════════════════════════════════════════════════════════
#  Syntax-Highlighting
# ════════════════════════════════════════════════════════════════════════════

_BUILTINS = {n for n in dir(builtins) if not n.startswith("_")}
_KONSTANTEN = {"True", "False", "None"}
_FALLBACK_RE = re.compile(
    r"(?P<kommentar>#.*)"
    r"|(?P<string>[rRbBfF]{0,2}('''|\"\"\"|'|\")(?:\\.|(?!\3).)*(?:\3)?)"
    r"|(?P<zahl>\b\d+(?:\.\d*)?(?:[eE][+-]?\d+)?\b)"
    r"|(?P<name>[A-Za-z_À-￿][\w]*)")


def _stil_fuer_name(name, folgt_klammer, nach_def):
    if name in _KONSTANTEN:
        return magenta
    if keyword.iskeyword(name) or name in ("match", "case"):
        return lambda t: fett(magenta(t))
    if nach_def:
        return lambda t: fett(blau(t))
    if name in _BUILTINS and folgt_klammer:
        return cyan
    if folgt_klammer:
        return blau
    return None


def _fallback_spans(zeile):
    spans = []
    for m in _FALLBACK_RE.finditer(zeile):
        art = m.lastgroup
        if art == "kommentar":
            spans.append((m.start(), m.end(), grau))
        elif art == "string":
            spans.append((m.start(), m.end(), gruen))
        elif art == "zahl":
            spans.append((m.start(), m.end(), gelb))
        elif art == "name":
            rest = zeile[m.end():].lstrip()
            st = _stil_fuer_name(m.group(), rest.startswith("("), False)
            if st:
                spans.append((m.start(), m.end(), st))
    return spans


def py_farben(code):
    """Python-Code -> Liste farbiger Zeilen. Funktioniert auch mit
    unvollständigem/fehlerhaftem Code (dann ab der Fehlerstelle per Regex)."""
    zeilen = str(code).split("\n")
    if not _FARBEN:
        return zeilen
    spans = [[] for _ in zeilen]
    bis_zeile = 0    # alle Zeilen < bis_zeile wurden von tokenize vollständig erfasst
    try:
        toks = []
        for tok in tokenize.generate_tokens(io.StringIO(str(code) + "\n").readline):
            toks.append(tok)
            bis_zeile = tok.start[0] - 1
        bis_zeile = len(zeilen)
    except (tokenize.TokenError, IndentationError, SyntaxError, ValueError):
        pass
    except Exception:
        toks = []
        bis_zeile = 0
    signifikant = [t for t in toks if t.type not in (
        tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT)]
    naechster = {}
    for a, b in zip(signifikant, signifikant[1:]):
        naechster[id(a)] = b
    vorheriger = {}
    for a, b in zip(signifikant, signifikant[1:]):
        vorheriger[id(b)] = a
    fstring_typen = {getattr(tokenize, n) for n in ("FSTRING_START", "FSTRING_MIDDLE", "FSTRING_END")
                     if hasattr(tokenize, n)}
    for tok in toks:
        st = None
        if tok.type == tokenize.COMMENT:
            st = grau
        elif tok.type == tokenize.STRING or tok.type in fstring_typen:
            st = gruen
        elif tok.type == tokenize.NUMBER:
            st = gelb
        elif tok.type == tokenize.NAME:
            nach = naechster.get(id(tok))
            vor = vorheriger.get(id(tok))
            st = _stil_fuer_name(tok.string, bool(nach and nach.string == "("),
                                 bool(vor and vor.string in ("def", "class")))
        if not st:
            continue
        (z1, s1), (z2, s2) = tok.start, tok.end
        for z in range(z1, z2 + 1):
            if 1 <= z <= len(zeilen):
                a = s1 if z == z1 else 0
                e = s2 if z == z2 else len(zeilen[z - 1])
                spans[z - 1].append((a, e, st))
    for i in range(max(0, bis_zeile), len(zeilen)):
        spans[i] = _fallback_spans(zeilen[i])
    ergebnis = []
    for zeile, sp in zip(zeilen, spans):
        out, pos = [], 0
        for a, e, st in sorted(sp, key=lambda x: x[0]):
            a, e = max(a, pos), min(e, len(zeile))
            if a >= e:
                continue
            out.append(zeile[pos:a])
            out.append(st(zeile[a:e]))
            pos = e
        out.append(zeile[pos:])
        ergebnis.append("".join(out))
    return ergebnis


# ════════════════════════════════════════════════════════════════════════════
#  Rahmen, Kästen, Tabellen
# ════════════════════════════════════════════════════════════════════════════

RAHMEN = {
    "eckig": "┌┐└┘─│",
    "rund": "╭╮╰╯─│",
    "doppelt": "╔╗╚╝═║",
    "dick": "┏┓┗┛━┃",
}


def kasten(inhalt, w, titel=None, farbe=None, stil="rund", innen_abstand=1, rechts=None):
    """Zeichnet einen Rahmen der Gesamtbreite w um die Zeilen 'inhalt'.
    Zu lange Zeilen werden hart umgebrochen. 'rechts' = Text unten rechts."""
    f = farbe or (lambda t: t)
    lo, ro, lu, ru, h, v = RAHMEN[stil]
    innen = w - 2 - 2 * innen_abstand
    if titel:
        t = " " + titel + " "
        if sichtbreite(t) > w - 4:
            t = abschneiden(t, w - 4)
        rest = w - 3 - sichtbreite(t)
        oben = f(lo + h) + f(fett(t)) + f(h * rest + ro)
    else:
        oben = f(lo + h * (w - 2) + ro)
    zeilen = [oben]
    sp = " " * innen_abstand
    for z in inhalt:
        for teil in (hart_umbrechen(z, innen) if sichtbreite(z) > innen else [z]):
            zeilen.append(f(v) + sp + pad(teil, innen) + sp + f(v))
    if rechts:
        r = " " + rechts + " "
        zeilen.append(f(lu + h * (w - 3 - sichtbreite(r))) + grau(r) + f(h + ru))
    else:
        zeilen.append(f(lu + h * (w - 2) + ru))
    return zeilen


def mini_kasten(zeilen, farbe=None, stil="eckig", minbreite=0, ausr="l"):
    """Kleiner Kasten, so breit wie sein Inhalt."""
    f = farbe or (lambda t: t)
    lo, ro, lu, ru, h, v = RAHMEN[stil]
    w = max([minbreite] + [sichtbreite(z) for z in zeilen])
    out = [f(lo + h * (w + 2) + ro)]
    for z in zeilen:
        out.append(f(v) + " " + pad(z, w, ausr) + " " + f(v))
    out.append(f(lu + h * (w + 2) + ru))
    return out


def nebeneinander(bloecke, abstand=2):
    """Setzt mehrere Zeilenblöcke nebeneinander (oben bündig)."""
    bloecke = [b for b in bloecke if b is not None]
    if not bloecke:
        return []
    hoehe = max(len(b) for b in bloecke)
    breiten = [max([0] + [sichtbreite(z) for z in b]) for b in bloecke]
    out = []
    for i in range(hoehe):
        teile = [pad(b[i] if i < len(b) else "", bw) for b, bw in zip(bloecke, breiten)]
        out.append((" " * abstand).join(teile).rstrip())
    return out


def fliessend(bloecke, w, abstand=2, zeilenabstand=0):
    """Blöcke nebeneinander; passt es nicht mehr, beginnt eine neue Reihe."""
    reihen, akt, aw = [], [], 0
    for b in bloecke:
        bw = max([0] + [sichtbreite(z) for z in b])
        if akt and aw + abstand + bw > w:
            reihen.append(akt)
            akt, aw = [], 0
        aw += (abstand if akt else 0) + bw
        akt.append(b)
    if akt:
        reihen.append(akt)
    out = []
    for i, r in enumerate(reihen):
        if i:
            out.extend([""] * zeilenabstand)
        out.extend(nebeneinander(r, abstand))
    return out


def tabelle(kopf, zeilen, w, ausr=None, kopf_stil=None, zell_stil=None):
    """Tabelle mit Unicode-Rahmen. Zellen dürfen Inline-Markup enthalten und
    werden bei Platzmangel umgebrochen. zell_stil(spalte, text) -> farbiger Text."""
    n = max([len(kopf or [])] + [len(z) for z in zeilen])
    if n == 0:
        return []
    kopf = list(kopf or [])
    if kopf:
        kopf += [""] * (n - len(kopf))
    zeilen = [list(z) + [""] * (n - len(z)) for z in zeilen]
    alle = ([kopf] if kopf else []) + zeilen
    natuerlich = [max(sichtbreite(inline_plain(str(z[i]))) for z in alle) for i in range(n)]
    natuerlich = [max(1, x) for x in natuerlich]
    verfuegbar = w - (3 * n + 1)
    breiten = natuerlich[:]
    while sum(breiten) > verfuegbar and max(breiten) > 6:
        i = breiten.index(max(breiten))
        breiten[i] -= 1
    ausr = ausr or ["l"] * n

    def zelle_zeilen(text, i, ist_kopf):
        text = str(text)
        if ist_kopf:
            return umbrechen(text, breiten[i], basis=(kopf_stil or fett))
        if zell_stil:
            res = zell_stil(i, text)
            if res is not None:
                return hart_umbrechen(res, breiten[i]) if sichtbreite(res) > breiten[i] else [res]
        return umbrechen(text, breiten[i])

    def linie(l, m, r):
        return grau(l + m.join("─" * (b + 2) for b in breiten) + r)

    out = [linie("┌", "┬", "┐")]
    for zi, z in enumerate(alle):
        ist_kopf = bool(kopf) and zi == 0
        zellen = [zelle_zeilen(t, i, ist_kopf) for i, t in enumerate(z)]
        hoehe = max(len(c) for c in zellen)
        for k in range(hoehe):
            teile = [pad(c[k] if k < len(c) else "", breiten[i], ausr[i] if i < len(ausr) else "l")
                     for i, c in enumerate(zellen)]
            out.append(grau("│") + grau("│").join(" " + t + " " for t in teile) + grau("│"))
        if ist_kopf:
            out.append(linie("├", "┼", "┤"))
    out.append(linie("└", "┴", "┘"))
    return out


def balken(wert, maximum, laenge=12, farbig=True):
    """Fortschrittsbalken ███░░░ (rot < 50 % ≤ gelb < 80 % ≤ grün)."""
    if not maximum:
        return grau("░" * laenge)
    anteil = max(0.0, min(1.0, wert / maximum))
    voll = round(laenge * anteil)
    if not farbig:
        f = blau
    else:
        f = gruen if anteil >= 0.8 else (gelb if anteil >= 0.5 else rot)
    return f("█" * voll) + grau("░" * (laenge - voll))


def teile_umbrechen(teile, w, trenner=" · ", einzug="  "):
    """Setzt kurze (farbige) Textstücke mit Trenner zu Zeilen <= w zusammen."""
    zeilen, akt = [], ""
    for t in teile:
        if akt and sichtbreite(akt) + sichtbreite(trenner) + sichtbreite(t) > w - len(einzug):
            zeilen.append(einzug + akt)
            akt = ""
        akt = (akt + trenner if akt else "") + t
    if akt:
        zeilen.append(einzug + akt)
    return zeilen


def linie(w, zeichen="─", farbe=grau):
    return farbe(zeichen * w)


def banner(titel, untertitel=None, w=None, farbe=magenta):
    """Großer doppelter Rahmen für Kapitel-/Bereichsanfänge."""
    w = w or breite()
    inhalt = [fett(titel)]
    if untertitel:
        for u in ([untertitel] if isinstance(untertitel, str) else untertitel):
            inhalt.extend(umbrechen(u, w - 6))
    return kasten(inhalt, w, farbe=farbe, stil="doppelt", innen_abstand=2)


def ueberschrift(text, w=None, farbe=blau, zeichen="─"):
    w = w or breite()
    t = f"{zeichen * 2} {text} "
    return [farbe(fett(t)) + farbe(zeichen * max(0, w - sichtbreite(t)))]


# ════════════════════════════════════════════════════════════════════════════
#  Code- und Ausgabekästen
# ════════════════════════════════════════════════════════════════════════════

def code_kasten(code, w, titel=None, nummern=True, aktuell=None, nebenzeilen=(),
                farbe=grau, luecken=False, max_zeilen=None):
    """Code mit Rahmen, Zeilennummern und Syntax-Highlighting.
    aktuell     = Zeilennummer, die mit ➜ markiert wird (Tracer)
    nebenzeilen = Zeilennummern, die mit · markiert werden (Aufrufer)
    luecken     = '___' durch nummerierte Lücken [1], [2] … ersetzen"""
    code = str(code).expandtabs(4).rstrip("\n")
    roh = code.split("\n")
    farbig = py_farben(code)
    if luecken:
        zaehler = itertools.count(1)

        def ersetze(m):
            return hl_gelb(f"[{next(zaehler)}]") if _FARBEN else f"[{next(zaehler)}]"
        farbig = [re.sub(r"___", ersetze, z) for z in farbig]
    nb = len(str(len(roh)))
    gutter = (nb + 4) if nummern else 1
    innen = w - 2 - gutter - 1
    lo, ro, lu, ru, h, v = RAHMEN["eckig"]
    if titel:
        t = " " + titel + " "
        oben = farbe(lo + h) + fett(t) + farbe(h * max(0, w - 3 - sichtbreite(t)) + ro)
    else:
        oben = farbe(lo + h * (w - 2) + ro)
    out = [oben]
    sichtbar = list(enumerate(farbig, 1))
    ausgelassen = 0
    if max_zeilen and len(sichtbar) > max_zeilen:
        if aktuell:
            mitte = min(max(aktuell - max_zeilen // 2, 0), len(sichtbar) - max_zeilen)
            sichtbar = sichtbar[mitte:mitte + max_zeilen]
        else:
            ausgelassen = len(sichtbar) - max_zeilen
            sichtbar = sichtbar[:max_zeilen]
    for nr, zeile in sichtbar:
        if nummern:
            if nr == aktuell:
                g = gruen(fett("➜")) + " " + gruen(fett(str(nr).rjust(nb))) + " " + farbe("│")
            elif nr in nebenzeilen:
                g = gelb("·") + " " + gelb(str(nr).rjust(nb)) + " " + farbe("│")
            else:
                g = "  " + grau(str(nr).rjust(nb)) + " " + farbe("│")
        else:
            g = " "
        teile = hart_umbrechen(zeile, innen) if sichtbreite(zeile) > innen else [zeile]
        for k, teil in enumerate(teile):
            if nr == aktuell and _FARBEN:
                inhalt = hl_zeile(pad(ohne_ansi(teil), innen))
            else:
                inhalt = pad(teil, innen)
            if k == 0:
                out.append(farbe(v) + g + " " + inhalt + farbe(v))
            elif nummern:
                out.append(farbe(v) + " " * (gutter - 2) + grau("↪") + farbe("│")
                           + " " + inhalt + farbe(v))
            else:
                out.append(farbe(v) + grau("↪") + " " + inhalt + farbe(v))
    if ausgelassen:
        out.append(farbe(v) + pad(grau(f"   … ({ausgelassen} weitere Zeilen)"), w - 2) + farbe(v))
    out.append(farbe(lu + h * (w - 2) + ru))
    return out


def ausgabe_kasten(erg, w, titel="Ausgabe", eingaben=None, max_zeilen=25):
    """Ergebnis von sandbox.ausfuehren als Kasten."""
    erg = erg or {}
    inhalt = []
    if eingaben:
        inhalt.append(grau("Eingaben: ") + ", ".join(cyan(str(e)) for e in eingaben))
    stdout = str(erg.get("stdout") or "").rstrip("\n")
    zeilen = stdout.split("\n") if stdout else []
    if len(zeilen) > max_zeilen:
        zeilen = zeilen[:max_zeilen] + [grau(f"… ({len(stdout.splitlines()) - max_zeilen} weitere Zeilen)")]
    for z in zeilen:
        inhalt.append(z.expandtabs(4))
    if not zeilen and not erg.get("fehler") and not erg.get("timeout"):
        inhalt.append(grau("(keine Ausgabe)"))
    farbe = grau
    if erg.get("timeout"):
        farbe = rot
        inhalt.append(rot(fett("⏱ Zeitlimit überschritten")) + rot(" – läuft da eine Endlosschleife?"))
    elif erg.get("fehler"):
        farbe = rot
        f = str(erg["fehler"]).strip().splitlines()
        zeile = erg.get("fehler_zeile")
        kopf = rot(fett("✘ " + (f[-1] if f else "Fehler")))
        if zeile:
            kopf += grau(f"   (Zeile {zeile})")
        inhalt.append(kopf)
    erkl = erg.get("fehler_erklaert")
    if erkl and (erg.get("fehler") or erg.get("timeout")):
        for z in str(erkl).strip().split("\n"):
            inhalt.extend(haengend("", z, w - 6, basis=gelb) if z.strip() else [""])
    return kasten(inhalt, w, titel=titel, farbe=farbe, stil="rund")


# ════════════════════════════════════════════════════════════════════════════
#  Markup-Blöcke
# ════════════════════════════════════════════════════════════════════════════

BOX_ARTEN = {
    "analogie": ("💡", cyan, "Stell dir vor"),
    "achtung": ("⚠", rot, "Achtung"),
    "info": ("ℹ", blau, "Info"),
}


def block_zeilen(block, w, ausfuehren=None, code_nr=None):
    """Ein Markup-Block -> Zeilen (ohne Außeneinzug, Breite <= w).
    ausfuehren(code, eingaben) -> dict wie sandbox.ausfuehren; für :::code."""
    typ = block.get("typ")
    try:
        if typ == "ueberschrift":
            t = inline(block.get("text", ""), basis=lambda s: fett(blau(s)))
            return ["", blau("▌ ") + t, grau("─" * min(w, sichtbreite(t) + 2))]
        if typ == "absatz":
            return umbrechen(block.get("text", ""), w)
        if typ == "merke":
            innen = haengend("★ ", block.get("text", ""), w - 2, basis=lambda s: fett(gelb(s)),
                             praefix_stil=lambda s: gelb(fett(s)))
            return [gelb("┃ ") + z for z in innen]
        if typ == "codeblock":
            return code_kasten(block.get("code", ""), w, nummern=False)
        if typ == "liste":
            out = []
            for i, p in enumerate(block.get("punkte", []), 1):
                praefix = f"{i}. " if block.get("nummeriert") else "• "
                if block.get("nummeriert") and len(block.get("punkte", [])) >= 10:
                    praefix = f"{i:>2}. "
                out.extend(haengend(praefix, p, w, praefix_stil=lambda s: blau(fett(s))))
            return out
        if typ == "tabelle":
            return tabelle(block.get("kopf", []), block.get("zeilen", []), w)
        if typ == "box":
            art = block.get("art", "info")
            icon, farbe, standard = BOX_ARTEN.get(art, BOX_ARTEN["info"])
            titel = (block.get("titel") or standard).strip()
            innen = []
            for b in block.get("bloecke", []):
                if innen and b.get("typ") not in ("ueberschrift",):
                    innen.append("")
                innen.extend(block_zeilen(b, w - 4, ausfuehren))
            while innen and not innen[0].strip():
                innen.pop(0)
            return kasten(innen, w, titel=f"{icon} {titel}", farbe=farbe, stil="rund")
        if typ == "code":
            return code_beispiel_zeilen(block, w, ausfuehren, code_nr)
        if typ == "visual":
            if block.get("fehler"):
                return [rot(f"(Visualisierung '{block.get('art')}' fehlerhaft: {block['fehler']})")]
            return visual_zeilen(block.get("art", ""), block.get("daten") or {}, w)
        if typ == "vergleich":
            return vergleich_zeilen(block, w, ausfuehren)
    except Exception as e:  # Darstellung darf nie das Programm abstürzen lassen
        return [rot(f"(Darstellungsfehler bei Block '{typ}': {type(e).__name__}: {e})")]
    if "text" in block:
        return umbrechen(str(block["text"]), w)
    return [grau(f"(unbekannter Block: {typ})")]


def code_beispiel_zeilen(block, w, ausfuehren=None, code_nr=None):
    code = block.get("code", "")
    eingaben = block.get("eingaben") or []
    titel = "▶ Beispiel" + (f" {code_nr}" if code_nr else "")
    if block.get("trace"):
        titel = "👣 Beispiel" + (f" {code_nr}" if code_nr else "") + " – Schritt für Schritt"
    out = code_kasten(code, w, titel=titel)
    if ausfuehren:
        try:
            erg = ausfuehren(code, eingaben)
        except Exception as e:
            erg = {"stdout": "", "fehler": f"Konnte nicht ausgeführt werden: {e}"}
        out.extend(ausgabe_kasten(erg, w, titel="Ausgabe", eingaben=eingaben))
    elif eingaben:
        out.append(grau("Eingaben: ") + ", ".join(eingaben))
    return out


def vergleich_zeilen(block, w, ausfuehren=None):
    titel = list(block.get("titel") or ["", ""]) + ["", ""]
    spalten = list(block.get("spalten") or [[], []]) + [[], []]
    sw = (w - 3) // 2           # Breite linke Spalte (zwischen den Rahmen)
    rw_ges = w - sw - 3         # Breite rechte Spalte
    breiten = (sw - 2, rw_ges - 2)
    seiten = []
    for s, bw in zip(spalten[:2], breiten):
        z = []
        for b in s:
            if z:
                z.append("")
            z.extend(block_zeilen(b, bw, ausfuehren))
        seiten.append([t for x in z for t in (hart_umbrechen(x, bw) if sichtbreite(x) > bw else [x])])
    out = [grau("┌" + "─" * sw + "┬" + "─" * rw_ges + "┐")]
    out.append(grau("│ ") + pad(fett(inline(titel[0])), breiten[0]) + grau(" │ ")
               + pad(fett(inline(titel[1])), breiten[1]) + grau(" │"))
    out.append(grau("├" + "─" * sw + "┼" + "─" * rw_ges + "┤"))
    links, rechts = seiten
    for i in range(max(len(links), len(rechts))):
        l = links[i] if i < len(links) else ""
        r = rechts[i] if i < len(rechts) else ""
        out.append(grau("│ ") + pad(l, breiten[0]) + grau(" │ ") + pad(r, breiten[1]) + grau(" │"))
    out.append(grau("└" + "─" * sw + "┴" + "─" * rw_ges + "┘"))
    return out


def seite_zeilen(bloecke, w=None, ausfuehren=None, einzug=EINZUG):
    """Eine ganze Seite (Liste von Blöcken) -> eingerückte Zeilen."""
    w = (w or breite()) - len(einzug)
    out = []
    code_nr = 0
    anzahl_code = sum(1 for b in bloecke if b.get("typ") == "code")
    for b in bloecke:
        if out and b.get("typ") != "ueberschrift":
            out.append("")
        nr = None
        if b.get("typ") == "code":
            code_nr += 1
            nr = code_nr if anzahl_code > 1 else None
        out.extend(block_zeilen(b, w, ausfuehren, nr))
    while out and not out[0].strip():
        out.pop(0)
    return [einzug + z if z else "" for z in out]


# ════════════════════════════════════════════════════════════════════════════
#  Visualisierungen
# ════════════════════════════════════════════════════════════════════════════

TYP_FARBE = {
    "int": blau, "float": cyan, "str": gruen, "bool": magenta, "NoneType": grau,
    "list": gelb, "tuple": gelb, "dict": gelb, "set": gelb, "function": blau,
}
TYP_NAME = {
    "int": "Ganzzahl", "float": "Kommazahl", "str": "Text", "bool": "Wahrheitswert",
    "NoneType": "Nichts", "list": "Liste", "tuple": "Tupel", "dict": "Dictionary",
    "set": "Menge", "function": "Funktion", "range": "Bereich", "complex": "komplexe Zahl",
}


def _tf(typ):
    return TYP_FARBE.get(typ, lambda t: t)


def py_repr(v):
    """JSON-Wert so anzeigen, wie Python ihn schreiben würde."""
    try:
        return repr(v)
    except Exception:
        return str(v)


def _wert_text(v, typ=None):
    """'wert' aus variablen-Visual: Text wird roh gezeigt, bei Typ str mit Quotes."""
    if not isinstance(v, str):
        return py_repr(v)
    if typ == "str" and not (len(v) >= 2 and v[0] == v[-1] and v[0] in "'\""):
        return repr(v)
    return v


def kiste(name, wert, typ=None, markierung=None, maxbreite=40):
    """Variable als beschriftete Kiste:
         alter
        ┌──────┐
        │  18  │
        └──────┘
          int"""
    wert = abschneiden(str(wert), maxbreite)
    f = _tf(typ)
    innen = max(sichtbreite(wert), sichtbreite(str(name)), sichtbreite(str(typ or "")), 3)
    zeilen = [pad(fett(str(name)), innen + 4, "c")]
    zeilen.append(f("┌" + "─" * (innen + 2) + "┐"))
    zeilen.append(f("│") + " " + pad(f(fett(wert)) if typ else fett(wert), innen, "c") + " " + f("│"))
    zeilen.append(f("└" + "─" * (innen + 2) + "┘"))
    unter = grau(str(typ)) if typ else ""
    if markierung:
        unter = (unter + " " if unter else "") + markierung
    zeilen.append(pad(unter, innen + 4, "c"))
    return zeilen


def _v_variablen(d, w):
    def reihe(vars_):
        bl = []
        for v in vars_ or []:
            if not isinstance(v, dict):
                continue
            typ = v.get("typ")
            wert = v.get("wert", "")
            # markup.py liefert "anzeige" (Python-Darstellung); Text-Werte bleiben wie bisher
            text = (_wert_text(wert, typ) if isinstance(wert, str) or not isinstance(v.get("anzeige"), str)
                    else v["anzeige"])
            bl.append(kiste(v.get("name", "?"), text, typ))
        return fliessend(bl, w, abstand=3, zeilenabstand=1) if bl else [grau("(keine Variablen)")]

    schritte = d.get("schritte")
    if schritte:
        texte = d.get("texte") or []
        out = []
        for i, s in enumerate(schritte):
            if i:
                out.append(grau("        ▼"))
            t = texte[i] if i < len(texte) else ""
            out.append(blau(fett(f"Schritt {i + 1}")) + ("  " + inline(t) if t else ""))
            out.extend(reihe(s))
        return out
    return reihe(d.get("vars"))


def slice_parsen(text):
    """'1:3', '[::-1]', 'lst[2:]' -> slice; '2' / '-1' -> int. Fehler: ValueError."""
    t = str(text).strip()
    m = re.match(r"^[A-Za-z_]\w*\s*\[(.*)\]$", t)
    if m:
        t = m.group(1)
    t = t.strip().strip("[]").strip()
    if not t:
        raise ValueError("leer")
    teile = t.split(":")
    if len(teile) == 1:
        return int(t)
    if len(teile) > 3:
        raise ValueError("Höchstens zwei Doppelpunkte: start:stop:step")
    werte = [int(p) if p.strip() else None for p in teile] + [None] * (3 - len(teile))
    if werte[2] == 0:
        raise ValueError("Die Schrittweite darf nicht 0 sein (ValueError).")
    return slice(*werte)


def _slice_text(sl):
    if isinstance(sl, int):
        return f"[{sl}]"
    teile = ["" if x is None else str(x) for x in (sl.start, sl.stop, sl.step)]
    if sl.step is None:
        teile = teile[:2]
    return "[" + ":".join(teile) + "]"


def faecher_zeilen(texte, w, markiert=(), gewaehlt=(), negativ=True, start_index=0,
                   index_label=True):
    """Nummerierte Fächer: Index oben, Werte im Kasten, negativer Index unten."""
    n = len(texte)
    if n == 0:
        return [grau("┌───┐"), grau("│   │") + grau("  (leer)"), grau("└───┘")]
    zb = max([3] + [sichtbreite(t) + 2 for t in texte] + [len(str(-n)) + 2])
    pro_reihe = max(1, (w - 2) // (zb + 1))
    markiert, gewaehlt = set(markiert), list(gewaehlt)
    gw = set(gewaehlt)
    out = []
    for anfang in range(0, n, pro_reihe):
        idx = list(range(anfang, min(n, anfang + pro_reihe)))
        if anfang:
            out.append("")
        out.append(" " + "".join(pad(blau(str(i + start_index)) if i in gw or i in markiert
                                     else grau(str(i + start_index)), zb, "c") + " " for i in idx))
        out.append(grau("┌" + "┬".join("─" * zb for _ in idx) + "┐"))
        zellen = []
        for i in idx:
            t = pad(texte[i], zb, "c")
            if i in gw:
                t = hl_gruen(t)
            elif i in markiert:
                t = hl_gelb(t)
            zellen.append(t)
        out.append(grau("│") + grau("│").join(zellen) + grau("│"))
        out.append(grau("└" + "┴".join("─" * zb for _ in idx) + "┘"))
        if negativ:
            out.append(" " + "".join(pad(grau(str(i - n)), zb, "c") + " " for i in idx))
        if gw or markiert:
            marken = []
            for i in idx:
                if i in gw:
                    nr = gewaehlt.index(i) + 1
                    marken.append(pad(gruen("▲" + (str(nr) if len(gewaehlt) > 1 and
                                                     gewaehlt != sorted(gewaehlt) else "")), zb, "c"))
                elif i in markiert:
                    marken.append(pad(gelb("↑"), zb, "c"))
                else:
                    marken.append(" " * zb)
            out.append(" " + " ".join(marken))
    if index_label:
        legende = grau("oben: Index") + (grau(" · unten: negativer Index") if negativ else "")
        out.append(legende)
    return out


def _sequenz_visual(d, w, zeichen):
    if zeichen:
        text = str(d.get("text", ""))
        werte = list(text)
        texte = ["␣" if c == " " else c for c in werte]
        name = d.get("name") or "text"
        kopfzeile = f"{name} = {text!r}"
    else:
        werte = list(d.get("werte") or [])
        anzeige = d.get("werte_anzeige")
        if isinstance(anzeige, list) and len(anzeige) == len(werte):
            texte = [str(t) for t in anzeige]            # Python-Darstellung aus markup.py
        else:
            texte = [py_repr(v) for v in werte]
        name = d.get("name") or "lst"
        kopfzeile = f"{name} = {py_repr(werte)}"
    n = len(werte)
    out = [fett(abschneiden(kopfzeile, w - 14)) + grau(f"   (len = {n})")]
    markiert = set()
    for m in d.get("markiert") or []:
        try:
            m = int(m)
            if -n <= m < n:
                markiert.add(m % n)
        except (TypeError, ValueError):
            pass
    gewaehlt, info = [], []
    s = d.get("slice")
    if s not in (None, ""):
        try:
            sl = slice_parsen(s)
            if isinstance(sl, int):
                if -n <= sl < n:
                    markiert = {sl % n}
                    info.append(f"{name}[{sl}]" + grau("  →  ") + gelb(fett(py_repr(werte[sl]))))
                else:
                    info.extend(umbrechen(f"{name}[{sl}] gibt es nicht! Erlaubt sind die Indizes 0 bis "
                                          f"{n - 1} (oder -{n} bis -1) → IndexError", w, basis=rot))
            else:
                gewaehlt = list(range(n))[sl]
                ergebnis = [werte[i] for i in gewaehlt]
                erg_txt = repr("".join(ergebnis)) if zeichen else py_repr(ergebnis)
                info.append(f"{name}{_slice_text(sl)}" + grau("  →  ")
                            + gruen(fett(abschneiden(erg_txt, w - sichtbreite(name) - 20))))
                start, stop, step = sl.indices(n)
                if step > 0:
                    info.append(grau(f"Start {sl.start if sl.start is not None else 'weggelassen → 0'}"
                                     f" (ist dabei) · Stopp "
                                     f"{sl.stop if sl.stop is not None else 'weggelassen → bis zum Ende'}"
                                     f" (NICHT mehr dabei) · Schritt {step}"))
                else:
                    info.append(grau(f"Negativer Schritt {step}: es wird RÜCKWÄRTS gelaufen."))
                if not gewaehlt:
                    info.extend(umbrechen("Der Bereich ist leer – das Ergebnis ist leer (kein Fehler!).", w,
                                          basis=gelb))
        except ValueError as e:
            info.extend(umbrechen(f"'{s}' verstehe ich nicht: {e}", w, basis=rot))
    out.extend(faecher_zeilen(texte, w, markiert, gewaehlt, d.get("negativ", True) is not False))
    out.extend(info)
    return out


def _v_dict(d, w):
    name = d.get("name") or "d"
    paare = d.get("paare") or []
    markiert = {py_repr(m) for m in (d.get("markiert") or [])}
    out = [fett(f"{name} = {{ … }}") + grau(f"   ({len(paare)} Eintr{'ag' if len(paare) == 1 else 'äge'})")]
    if not paare:
        out.append(grau("{}  (leeres Dictionary)"))
        return out
    ks = [py_repr(p[0]) if isinstance(p, (list, tuple)) and p else "?" for p in paare]
    vs = [py_repr(p[1]) if isinstance(p, (list, tuple)) and len(p) > 1 else "?" for p in paare]
    anzeige = d.get("paare_anzeige")
    if isinstance(anzeige, list) and len(anzeige) == len(paare):     # Python-Darstellung aus markup.py
        ks = [str(a[0]) if isinstance(a, (list, tuple)) and a else k for a, k in zip(anzeige, ks)]
        vs = [str(a[1]) if isinstance(a, (list, tuple)) and len(a) > 1 else v for a, v in zip(anzeige, vs)]
    kw = min(max(sichtbreite(k) for k in ks + ["Schlüssel"]), w // 2 - 6)
    vw = min(max(sichtbreite(v) for v in vs + ["Wert"]), w - kw - 14)
    out.append(grau("┌" + "─" * (kw + 4) + "┐     ┌" + "─" * (vw + 2) + "┐"))
    out.append(grau("│ ") + fett(pad("🔑 Schlüssel", kw + 2)) + grau(" │     │ ") + fett(pad("Wert", vw))
               + grau(" │"))
    out.append(grau("├" + "─" * (kw + 4) + "┤     ├" + "─" * (vw + 2) + "┤"))
    for k, v in zip(ks, vs):
        mk = k in markiert
        kt = pad(abschneiden(k, kw + 2), kw + 2)
        vt = pad(abschneiden(v, vw), vw)
        if mk:
            kt, vt = hl_gelb(kt), hl_gelb(vt)
        pfeil = gelb(" ──▶ ") if mk else grau(" ──▶ ")
        out.append(grau("│ ") + kt + grau(" │") + pfeil + grau("│ ") + vt + grau(" │"))
    out.append(grau("└" + "─" * (kw + 4) + "┘     └" + "─" * (vw + 2) + "┘"))
    if markiert:
        for k, v in zip(ks, vs):
            if k in markiert:
                out.append(f"{name}[{k}]" + grau("  →  ") + gelb(fett(v)))
    return out


_VERBINDER = {
    # (links, rechts, oben, unten) -> Zeichen
    (True, True, False, False): "─", (False, False, True, True): "│",
    (True, False, False, True): "┐", (True, False, True, False): "┘",
    (True, False, True, True): "┤", (True, True, False, True): "┬",
    (True, True, True, False): "┴", (True, True, True, True): "┼",
    (False, True, False, True): "┌", (False, True, True, False): "└",
    (False, True, True, True): "├",
}


def _objekt_bild(obj):
    if isinstance(obj, (list, tuple)):
        texte = [py_repr(v) for v in obj] or [" "]
        zb = [max(3, sichtbreite(t) + 2) for t in texte]
        return [grau("┌" + "┬".join("─" * b for b in zb) + "┐"),
                grau("│") + grau("│").join(pad(t, b, "c") for t, b in zip(texte, zb)) + grau("│"),
                grau("└" + "┴".join("─" * b for b in zb) + "┘")]
    return mini_kasten([py_repr(obj)], farbe=grau)


def _v_referenz(d, w):
    namen = d.get("namen") or {}
    objekte = d.get("objekte") or []
    out = []
    nw = max([1] + [sichtbreite(n) for n in namen])
    for oi, obj in enumerate(objekte):
        zeiger = [n for n, i in namen.items() if i == oi]
        bild = _objekt_bild(obj)
        typname = type(obj).__name__ if not isinstance(obj, list) else "list"
        bild[1] = bild[1] + "  " + grau(f"Objekt {oi + 1} ({typname})")
        k = len(zeiger)
        hoehe = max(len(bild), k)
        if k == 1:
            namenszeilen = {1: zeiger[0]}
        else:
            namenszeilen = {r: n for r, n in enumerate(zeiger)}
        reihen_mit_name = set(namenszeilen)
        pfeil_reihe = 1
        rows = sorted(reihen_mit_name | {pfeil_reihe})
        lo_r, hi_r = rows[0], rows[-1]
        for r in range(hoehe):
            name = namenszeilen.get(r)
            links = (fett(gelb(pad(name, nw, "r"))) + gelb(" ──")) if name else " " * (nw + 3)
            if k == 0 or not (lo_r <= r <= hi_r):
                verb = " "
            else:
                schl = (name is not None, r == pfeil_reihe, r > lo_r, r < hi_r)
                verb = _VERBINDER.get(schl, "│" if (schl[2] or schl[3]) else "─") if k > 1 else "─"
            if k == 0 and r == pfeil_reihe:
                rechts = grau("    ")
                links = " " * (nw + 3)
            else:
                rechts = gelb("──▶ ") if r == pfeil_reihe and k else "    "
            objteil = bild[r] if r < len(bild) else ""
            out.append(links + gelb(verb) + rechts + objteil)
        if k == 0:
            out.append(grau(" " * (nw + 4) + "(auf dieses Objekt zeigt kein Name)"))
        out.append("")
    while out and not out[-1]:
        out.pop()
    geteilt = [[n for n, i in namen.items() if i == oi] for oi in range(len(objekte))]
    for g in geteilt:
        if len(g) > 1:
            namen_txt = ", ".join(f"**{n}**" for n in g[:-1]) + f" und **{g[-1]}**"
            out.extend(haengend("↳ ", namen_txt + " zeigen auf DASSELBE Objekt: Eine Änderung über "
                                "einen Namen sieht man bei allen!", w, praefix_stil=gelb))
    if len(objekte) > 1 and len({py_repr(o) for o in objekte}) < len(objekte):
        out.extend(haengend("↳ ", "Gleicher Inhalt heißt nicht gleiches Objekt: `==` ist True, "
                            "`is` ist False.", w, basis=grau, praefix_stil=grau))
    return out


def _v_ablauf(d, w):
    schritte = d.get("schritte") or []
    if not schritte:
        return [grau("(leerer Ablauf)")]
    texte = []
    for s in schritte:
        if isinstance(s, dict):
            icon = s.get("icon", "")
            texte.append(((icon + " ") if icon else "") + str(s.get("text", "")))
        else:
            texte.append(str(s))
    innen = min(max(sichtbreite(inline_plain(t)) for t in texte), w - 10)
    # waagerecht, falls es passt
    gesamt = sum(sichtbreite(inline_plain(t)) + 4 for t in texte) + 5 * (len(texte) - 1)
    if gesamt <= w and len(texte) <= 4:
        bl = []
        for i, t in enumerate(texte):
            if i:
                bl.append(["", gelb(" ──▶ "), ""])
            bl.append(mini_kasten([inline(t)], farbe=blau, stil="rund"))
        return nebeneinander(bl, abstand=0)
    out = []
    mitte = (innen + 4) // 2
    for i, t in enumerate(texte):
        if i:
            out.append(" " * mitte + gelb("│"))
            out.append(" " * mitte + gelb("▼"))
        zeilen = umbrechen(t, innen)
        nr = grau(f" {i + 1}")
        k = mini_kasten(zeilen, farbe=blau, stil="rund", minbreite=innen)
        k[1] += nr
        out.extend(k)
    return out


def _bedingungskasten(text, farbe=gelb):
    """Raute-ähnlicher Kasten für eine Bedingung, mit Ausgang rechts (Zeile 1)
    und unten (Spalte 4)."""
    zeilen = text if isinstance(text, list) else [text]
    iw = max(sichtbreite(z) for z in zeilen)
    iw = max(iw, 6)
    oben = farbe("┌" + "─" * (iw + 2) + "┐")
    mitte = []
    for i, z in enumerate(zeilen):
        rechts = "├" if i == 0 else "│"
        mitte.append(farbe("│") + " " + pad(z, iw) + " " + farbe(rechts))
    unten = farbe("└───┬" + "─" * (iw - 2) + "┘")
    return [oben] + mitte + [unten], iw + 4


def _v_entscheidung(d, w):
    zweige = [("if", str(d.get("bedingung", "?")), d.get("ja", ""))]
    for e in d.get("elif") or []:
        if isinstance(e, dict):
            zweige.append(("elif", str(e.get("bedingung", "?")), e.get("text", "")))
    sonst = d.get("nein")
    out = []
    for kw, bed, text in zweige:
        cond_txt = magenta(fett(kw)) + " " + (py_farben(bed)[0] if _FARBEN else bed) + " " + gelb("?")
        cbox, cw = _bedingungskasten(cond_txt)
        rest = max(10, w - cw - 12)
        rbox = mini_kasten(umbrechen(str(text or "…"), rest), farbe=gruen, stil="rund")
        pfeil = [" " * 10, gruen("── ja ──▶ "), " " * 10]
        while len(pfeil) < len(rbox):
            pfeil.append(" " * 10)
        links = cbox[:]
        while len(links) < len(rbox):
            links.append("    " + gelb("│"))
        out.extend(nebeneinander([links, pfeil, rbox], abstand=0))
        out.append("    " + gelb("│") + rot(" nein"))
        out.append("    " + gelb("▼"))
    if sonst:
        b = mini_kasten(umbrechen(str(sonst), w - 12), farbe=rot, stil="rund")
        b[1] += "  " + grau("(else)")
        out.extend(b)
    else:
        out.append(grau("  (kein else: es geht einfach normal weiter)"))
    return out


def _v_schleife(d, w):
    art = d.get("art", "while")
    bed = str(d.get("bedingung", "?"))
    koerper = d.get("koerper") or []
    if isinstance(koerper, str):
        koerper = koerper.split("\n")
    danach = d.get("danach")
    farbig = lambda s: py_farben(s)[0] if _FARBEN else s  # noqa: E731
    if art == "for":
        cond = [magenta(fett("for")) + " " + farbig(bed) + ":", gelb("noch ein Wert übrig?")]
    else:
        cond = [magenta(fett("while")) + " " + farbig(bed) + " " + gelb("?")]
    cbox, cw = _bedingungskasten(cond)
    body = [farbig(z) for z in koerper] or [grau("pass")]
    bw = max(cw - 4, max(sichtbreite(z) for z in body))
    bbox = [blau("┌" + "─" * (bw + 2) + "┐")]
    bbox += [blau("│") + " " + pad(z, bw) + " " + blau("│") for z in body]
    bbox.append(blau("└───┬" + "─" * (bw - 2) + "┘"))
    rest = max(10, w - cw - 18)
    dbox = mini_kasten(umbrechen(str(danach or "weiter im Programm"), rest), farbe=gruen, stil="rund")
    links = ["    ", gelb("┌──▶"), gelb("│   ")]
    oberer = []
    for i in range(max(len(cbox), len(dbox))):
        l = links[i] if i < len(links) else gelb("│   ")
        c = cbox[i] if i < len(cbox) else ("    " + gelb("│"))
        p = rot("── nein ──▶ ") if i == 1 else " " * 12
        dz = dbox[i] if i < len(dbox) else ""
        oberer.append(l + pad(c, cw) + p + dz)
    out = oberer
    out.append(gelb("│   ") + "    " + gelb("│") + gruen(" ja"))
    out.append(gelb("│   ") + "    " + gelb("▼"))
    for z in bbox:
        out.append(gelb("│   ") + z)
    out.append(gelb("└───────┘") + grau("   zurück zur Bedingung ↺"))
    return out


def _v_zahlenstrahl(d, w):
    try:
        start = int(d.get("start", 0))
        stop = int(d.get("stop", 10))
        step = int(d.get("step", 1) if d.get("step") is not None else 1)
    except (TypeError, ValueError):
        return [rot("Zahlenstrahl: start/stop/step müssen ganze Zahlen sein.")]
    aufruf = f"range({start}, {stop}" + (f", {step})" if step != 1 else ")")
    if step == 0:
        return [fett(aufruf), rot("ValueError: Die Schrittweite (step) darf nicht 0 sein.")]
    werte = list(range(start, stop, step))
    out = [fett(aufruf) + grau("  →  ") + gruen(fett(abschneiden(py_repr(werte), w - len(aufruf) - 22)))
           + grau(f"   ({len(werte)} Zahlen)")]
    lo, hi = min(start, stop), max(start, stop)
    zahlen = list(range(lo, hi + 1))
    zw = max(3, len(str(lo)) + 1, len(str(hi)) + 1)
    massstab = len(zahlen) * zw + 2 <= w
    if massstab:
        punkte = zahlen
    else:
        punkte = sorted(set(werte) | {start, stop})
        max_p = max(2, (w - 2) // zw)
        if len(punkte) > max_p:
            vorne = punkte[:max_p // 2]
            hinten = punkte[-(max_p - len(vorne) - 1):]
            punkte = vorne + [None] + hinten
    ws = set(werte)
    achse, zahlenreihe = [], []
    for p in punkte:
        if p is None:
            achse.append(grau(pad("┈┈", zw, "c").replace(" ", "┈")))
            zahlenreihe.append(pad(grau("…"), zw, "c"))
            continue
        links = (zw - 1) // 2
        rechts = zw - 1 - links
        if p in ws:
            m = gruen(fett("●"))
            nt = gruen(fett(str(p)))
        elif p == stop:
            m = rot(fett("○"))
            nt = rot(fett(str(p)))
        else:
            m = grau("┼")
            nt = grau(str(p))
        achse.append(grau("─" * links) + m + grau("─" * rechts))
        zahlenreihe.append(pad(nt, zw, "c"))
    out.append("")
    out.append(" " + "".join(achse) + grau("▶"))
    out.append(" " + "".join(zahlenreihe))
    out.append(gruen("● kommt vor") + "   " + rot("○ stop – NICHT mehr dabei")
               + ("" if massstab else grau("   (nicht maßstabsgetreu)")))
    if step < 0 and werte:
        out.append(grau("Reihenfolge (rückwärts): ") + " → ".join(str(x) for x in werte[:12])
                   + (" …" if len(werte) > 12 else ""))
    elif not werte:
        out.extend(umbrechen("Der Bereich ist leer: Mit diesem step kommt man von start nie in "
                             "Richtung stop.", w, basis=gelb))
    return out


def _v_wahrheitstabelle(d, w):
    variablen = [str(v) for v in (d.get("variablen") or [])]
    ausdruecke = [str(a) for a in (d.get("ausdruecke") or [])]
    zeilen = []
    for kombi in itertools.product([True, False], repeat=len(variablen)):
        belegung = dict(zip(variablen, kombi))
        z = [str(b) for b in kombi]
        for a in ausdruecke:
            try:
                z.append(py_repr(eval(a, {"__builtins__": {}}, dict(belegung))))  # noqa: S307
            except Exception as e:
                z.append(f"Fehler: {type(e).__name__}")
        zeilen.append(z)

    def stil(_i, t):
        if t == "True":
            return gruen(fett("True"))
        if t == "False":
            return rot("False")
        return None
    kopf = variablen + [f"`{a}`" for a in ausdruecke]
    return tabelle(kopf, zeilen, w, ausr=["c"] * (len(variablen) + len(ausdruecke)), zell_stil=stil)


def _v_stapel(d, w):
    titel = d.get("titel") or "Aufrufstapel"
    rahmen = [str(r) for r in (d.get("rahmen") or [])]
    rueck = [str(r) if r is not None else "" for r in (d.get("rueckgaben") or [])]
    out = [fett(titel) + grau("   (unten = zuerst aufgerufen, oben = gerade aktiv)")]
    if not rahmen:
        out.append(grau("(leerer Stapel)"))
        return out
    iw = max(12, max(sichtbreite(r) for r in rahmen) + 4)
    out.append("   " + blau("╭" + "─" * iw + "╮"))
    for k, i in enumerate(reversed(range(len(rahmen)))):
        r = rahmen[i]
        zus = ""
        if i < len(rueck) and rueck[i] != "":
            zus = gruen("  ↩ gibt ") + gruen(fett(rueck[i])) + gruen(" zurück")
        kennz = gelb("▶ ") if k == 0 else "  "
        out.append(kennz + " " + blau("│") + pad(fett(r) if k == 0 else r, iw, "c") + blau("│") + zus)
        if k < len(rahmen) - 1:
            out.append("   " + blau("├" + "─" * iw + "┤"))
    out.append("   " + blau("╰" + "─" * iw + "╯"))
    out.append("  " + grau("▀" * (iw + 4)))
    if len(rahmen) > 1:
        out.append(grau("Aufbau:  ") + " → ".join(rahmen))
        if any(rueck):
            abbau = [f"{rahmen[i]} = {rueck[i]}" for i in reversed(range(len(rahmen)))
                     if i < len(rueck) and rueck[i] != ""]
            out.append(grau("Abbau:   ") + " → ".join(abbau))
    return out


def _v_baum(d, w):
    wurzel = d.get("wurzel") or {}
    out = []

    def knoten_text(k):
        t = str(k.get("text", "?"))
        wert = k.get("wert", k.get("rueckgabe"))
        s = fett(t) if not k.get("kinder") else blau(fett(t))
        if wert is not None:
            s += grau("  → ") + gruen(str(wert))
        return s

    def gehe(k, praefix, letzter, tiefe):
        if tiefe == 0:
            out.append(knoten_text(k))
            neu = ""
        else:
            out.append(grau(praefix + ("└─ " if letzter else "├─ ")) + knoten_text(k))
            neu = praefix + ("   " if letzter else "│  ")
        if tiefe > 25:
            return
        kinder = [c for c in (k.get("kinder") or []) if isinstance(c, dict)]
        for i, c in enumerate(kinder):
            gehe(c, neu, i == len(kinder) - 1, tiefe + 1)
    if isinstance(wurzel, dict):
        gehe(wurzel, "", True, 0)
    texte = []

    def sammeln(k):
        texte.append(str(k.get("text", "")))
        for c in k.get("kinder") or []:
            if isinstance(c, dict):
                sammeln(c)
    if isinstance(wurzel, dict):
        sammeln(wurzel)
    doppelt = {t for t in texte if texte.count(t) > 1}
    if doppelt:
        out.append(grau(f"↳ {len(texte)} Aufrufe insgesamt; mehrfach berechnet: ")
                   + gelb(", ".join(sorted(doppelt))))
    return out


def _v_funktion(d, w):
    name = str(d.get("name", "f"))
    eingaben = [str(e) for e in (d.get("eingaben") or [])]
    ausgabe = d.get("ausgabe")
    innen = d.get("innen") or ""
    innen_z = py_farben(str(innen)) if innen else []
    kopf = "⚙ " + fett(name)
    maschine = mini_kasten([kopf] + innen_z, farbe=magenta, stil="doppelt", minbreite=12)
    ein = eingaben or [grau("(keine Eingabe)")]
    aus = [gruen(fett(str(ausgabe)))] if ausgabe not in (None, "") else [grau("None")]
    ein_block = [grau("Eingabe")] + [cyan(e) for e in ein]
    aus_block = [grau("Ausgabe")] + aus
    mitte = 1 + (len(maschine) - 2) // 2
    pfeil_ein = [""] * len(maschine)
    pfeil_ein[mitte] = gelb(" ──▶ ")
    pfeil_aus = [""] * len(maschine)
    pfeil_aus[mitte] = gelb(" ──▶ ")
    eb = [""] * max(0, mitte - 1) + ein_block
    ab = [""] * max(0, mitte - 1) + aus_block
    zeilen = nebeneinander([eb, pfeil_ein, maschine, pfeil_aus, ab], abstand=0)
    if max(sichtbreite(z) for z in zeilen) <= w:
        return zeilen
    out = [grau("Eingabe: ") + ", ".join(cyan(e) for e in ein), "   " + gelb("▼")]
    out += maschine
    out += ["   " + gelb("▼"), grau("Ausgabe: ") + aus[0]]
    return out


def typ_bestimmen(literal):
    """'42' -> 'int' usw. (sicher über ast.literal_eval; sonst eval ohne builtins)."""
    try:
        return type(ast.literal_eval(str(literal))).__name__
    except Exception:
        pass
    try:
        sichere = {"range": range, "len": len, "int": int, "float": float, "str": str,
                   "list": list, "tuple": tuple, "dict": dict, "set": set, "bool": bool}
        return type(eval(str(literal), {"__builtins__": sichere}, {})).__name__  # noqa: S307
    except Exception:
        return "?"


def _v_typen(d, w):
    werte = [str(v) for v in (d.get("werte") or [])]
    gruppen = {}
    for v in werte:
        gruppen.setdefault(typ_bestimmen(v), []).append(v)
    bl = []
    for typ, vs in gruppen.items():
        f = _tf(typ)
        titel = f(fett(typ)) + grau(" · " + TYP_NAME.get(typ, "?" if typ == "?" else typ))
        if typ == "?":
            titel = rot(fett("?")) + grau(" · unbekannt/Fehler")
        iw = max([sichtbreite(titel)] + [sichtbreite(v) for v in vs])
        b = [f("┌" + "─" * (iw + 2) + "┐"), f("│") + " " + pad(titel, iw) + " " + f("│"),
             f("├" + "─" * (iw + 2) + "┤")]
        for v in vs:
            b.append(f("│") + " " + pad(f(v), iw) + " " + f("│"))
        b.append(f("└" + "─" * (iw + 2) + "┘"))
        bl.append(b)
    if not bl:
        return [grau("(keine Werte)")]
    return fliessend(bl, w, abstand=2, zeilenabstand=1) + [grau("Python bestimmt den Typ selbst: "
                                                                 "type(42) → <class 'int'>")]


VISUALS = {
    "variablen": _v_variablen,
    "liste": lambda d, w: _sequenz_visual(d, w, False),
    "string": lambda d, w: _sequenz_visual(d, w, True),
    "dict": _v_dict,
    "referenz": _v_referenz,
    "ablauf": _v_ablauf,
    "entscheidung": _v_entscheidung,
    "schleife": _v_schleife,
    "zahlenstrahl": _v_zahlenstrahl,
    "wahrheitstabelle": _v_wahrheitstabelle,
    "stapel": _v_stapel,
    "baum": _v_baum,
    "funktion": _v_funktion,
    "typen": _v_typen,
}

# Visuals, die im Terminal eine kleine Eingabe zum Ausprobieren anbieten
INTERAKTIV = {"liste", "string", "zahlenstrahl"}


def visual_zeilen(art, daten, w):
    f = VISUALS.get(art)
    if not f:
        return [grau(f"(Visualisierung '{art}' wird im Terminal nicht unterstützt)")]
    try:
        zeilen = f(daten if isinstance(daten, dict) else {}, w)
        # Sicherheitsnetz: nie breiter als w
        return [t for z in zeilen for t in (hart_umbrechen(z, w) if sichtbreite(z) > w else [z])]
    except Exception as e:
        return [rot(f"(Visualisierung '{art}' konnte nicht gezeichnet werden: {type(e).__name__}: {e})")]


# ════════════════════════════════════════════════════════════════════════════
#  Werte aus dem Tracer (sandbox.trace) und Schritt-für-Schritt-Ansicht
# ════════════════════════════════════════════════════════════════════════════

def _wert_kurz(wert, maxb=40):
    if not isinstance(wert, dict):
        return abschneiden(str(wert), maxb)
    return abschneiden(str(wert.get("repr", "?")), maxb)


def wert_bloecke(name, wert, w, markierung=None, alias=None):
    """Ein Tracer-WERT als Zeilenblock: Kiste (Skalar), Fächer (Liste/Tupel),
    Tabelle (Dict). Rückgabe: (zeilen, ist_breit)."""
    if not isinstance(wert, dict):
        return kiste(name, str(wert)), False
    typ = wert.get("typ", "andere")
    zusatz = (" " + markierung) if markierung else ""
    if alias:
        zusatz += grau(f"  (dasselbe Objekt wie {alias})")
    if typ in ("list", "tuple") and wert.get("elemente") is not None:
        el = wert.get("elemente") or []
        texte = [_wert_kurz(e, 18) for e in el]
        kopf = fett(name) + grau(f" : {typ}, len {len(el)}") + zusatz
        z = [kopf] + faecher_zeilen(texte, w, negativ=False, index_label=False)
        if typ == "tuple":
            z[0] = kopf + grau("  (Tupel – unveränderlich)")
        return z, True
    if typ == "dict" and wert.get("paare") is not None:
        paare = wert.get("paare") or []
        kopf = fett(name) + grau(f" : dict, {len(paare)} Eintr{'ag' if len(paare) == 1 else 'äge'}") + zusatz
        if not paare:
            return [kopf, grau("{}")], True
        zeilen = [[_wert_kurz(k, 24), _wert_kurz(v, 30)] for k, v in paare]
        return [kopf] + tabelle(["Schlüssel", "Wert"], zeilen, min(w, 60)), True
    if typ == "set" and wert.get("elemente") is not None:
        return [fett(name) + grau(" : set") + zusatz, "{" + ", ".join(_wert_kurz(e, 18)
                                                                    for e in wert["elemente"]) + "}"], True
    if typ == "function":
        return kiste(name, "⚙ " + abschneiden(str(wert.get("repr", "Funktion")), 20), "function",
                     markierung), False
    return kiste(name, _wert_kurz(wert, 30), typ, markierung), False


def variablen_zeilen(variablen, w, vorher=None):
    """Alle Variablen eines Rahmens: kleine Werte als Kisten in einer Reihe,
    Listen/Dicts darunter. vorher = Variablen des vorigen Schritts (für ★)."""
    if not variablen:
        return [grau("(noch keine Variablen)")]
    kleine, grosse = [], []
    ids = {}
    for n, v in variablen.items():
        if isinstance(v, dict) and v.get("typ") in ("list", "dict", "set", "tuple") and v.get("id") is not None:
            ids.setdefault(v["id"], []).append(n)
    for n, v in variablen.items():
        mark = None
        if vorher is not None:
            if n not in vorher:
                mark = gelb("★ neu")
            elif _wert_kurz(vorher[n], 200) != _wert_kurz(v, 200):
                mark = gelb("✎ geändert")
        alias = None
        if isinstance(v, dict) and v.get("id") in ids and len(ids[v["id"]]) > 1:
            erster = ids[v["id"]][0]
            alias = erster if erster != n else None
        bl, breit = wert_bloecke(n, v, w, mark, alias)
        (grosse if breit else kleine).append(bl)
    out = fliessend(kleine, w, abstand=2, zeilenabstand=0) if kleine else []
    for g in grosse:
        if out:
            out.append("")
        out.extend(g)
    return out


EREIGNIS_TEXT = {
    "line": "Diese Zeile ist als Nächstes dran.",
    "call": "Eine Funktion wird aufgerufen – ein neuer Rahmen kommt auf den Stapel.",
    "return": "Die Funktion ist fertig und gibt ihren Wert zurück.",
    "exception": "Hier passiert ein Fehler!",
}


def trace_seite(code, ergebnis, i, w=None):
    """Zeilen für Schritt i (0-basiert) der Schritt-für-Schritt-Ansicht."""
    w = (w or breite()) - len(EINZUG)
    schritte = ergebnis.get("schritte") or []
    n = len(schritte)
    out = []
    if not schritte:
        out.append(rot("Es gibt keine Schritte anzuzeigen."))
        if ergebnis.get("fehler"):
            out.append(rot(str(ergebnis["fehler"])))
        return [EINZUG + z for z in out]
    i = max(0, min(i, n - 1))
    s = schritte[i]
    vor = schritte[i - 1] if i > 0 else None
    zeile = s.get("zeile")
    ereignis = s.get("ereignis", "line")
    stapel = s.get("stapel") or []
    aktiv = stapel[-1] if stapel else {"funktion": "<modul>", "variablen": {}}
    fn = aktiv.get("funktion", "<modul>")
    wo = "Hauptprogramm" if fn in ("<modul>", "<module>") else f"Funktion {fn}"

    kopf = (cyan(fett(f"👣 Schritt {i + 1} von {n}")) + grau("  ·  ") + f"Zeile {zeile}"
            + grau("  ·  ") + wo)
    out.append(kopf)
    out.append(balken(i + 1, n, min(40, w - 4), farbig=False))
    text = EREIGNIS_TEXT.get(ereignis, "")
    if ereignis == "return":
        rw = s.get("rueckgabe")
        if fn in ("<modul>", "<module>"):
            out.append(gruen("🏁 Das Hauptprogramm ist durchgelaufen."))
        else:
            text = f"{fn} ist fertig und gibt {_wert_kurz(rw) if rw is not None else 'None'} zurück."
            out.append(gruen("↩ " + text))
    elif ereignis == "call":
        out.append(blau("📞 " + f"{fn} wird aufgerufen – ein neuer Rahmen kommt auf den Stapel."))
    elif ereignis == "exception":
        out.append(rot("💥 " + text) + (rot(" " + str(s["fehler"])) if s.get("fehler") else ""))
    else:
        out.append(grau("➜ " + text))
    out.append("")
    nebenzeilen = [r.get("zeile") for r in stapel[:-1] if r.get("zeile")]
    out.extend(code_kasten(code, w, titel="Code", aktuell=zeile, nebenzeilen=nebenzeilen, max_zeilen=18))

    # Variablen
    vor_vars = None
    if vor:
        vst = vor.get("stapel") or []
        if vst and len(vst) == len(stapel) and vst[-1].get("funktion") == fn:
            vor_vars = vst[-1].get("variablen") or {}
        elif vst and len(vst) == len(stapel):
            vor_vars = None
    out.append("")
    titel = "Variablen im Hauptprogramm" if fn in ("<modul>", "<module>") else f"Variablen in {fn}()"
    out.extend(ueberschrift(titel, w, farbe=gelb))
    out.extend(variablen_zeilen(aktiv.get("variablen") or {}, w, vor_vars))
    if len(stapel) > 1:
        glob = stapel[0].get("variablen") or {}
        if glob:
            out.append("")
            out.extend(ueberschrift("Globale Variablen (Hauptprogramm)", w, farbe=grau))
            out.extend(variablen_zeilen(glob, w))
        out.append("")
        out.extend(ueberschrift("Aufrufstapel", w, farbe=blau))
        rahmen = []
        for r in stapel:
            f = r.get("funktion", "?")
            if f in ("<modul>", "<module>"):
                rahmen.append(f"Hauptprogramm (Zeile {r.get('zeile')})")
            else:
                args = ", ".join(f"{k}={_wert_kurz(v, 12)}" for k, v in list((r.get("variablen") or {}).items())[:3])
                rahmen.append(f"{f}({args})  Zeile {r.get('zeile')}")
        bild = _v_stapel({"titel": "", "rahmen": rahmen}, w)[1:]
        out.extend(z for z in bild if not ohne_ansi(z).startswith(("Aufbau", "Abbau")))

    # Ausgabe
    ausgabe = str(s.get("ausgabe") or "")
    out.append("")
    az = ausgabe.rstrip("\n").split("\n") if ausgabe else []
    neu = ausgabe != str((vor or {}).get("ausgabe") or "") and vor is not None
    if len(az) > 8:
        az = [grau(f"… ({len(az) - 8} Zeilen weiter oben)")] + az[-8:]
    if not az:
        az = [grau("(noch keine Ausgabe)")]
    elif neu:
        az[-1] = az[-1] + "  " + gelb("◀ neu")
    out.extend(kasten(az, w, titel="Ausgabe", farbe=grau))
    if i == n - 1:
        if ergebnis.get("fehler"):
            out.append(rot(fett("✘ " + str(ergebnis["fehler"]).strip().splitlines()[-1])))
            if ergebnis.get("fehler_erklaert"):
                out.extend(haengend("", str(ergebnis["fehler_erklaert"]), w, basis=gelb))
        elif ergebnis.get("abgebrochen"):
            out.append(gelb("⏹ Nach zu vielen Schritten abgebrochen (Endlosschleife?)."))
        else:
            out.append(gruen(fett("✔ Programm zu Ende.")))
    return [EINZUG + z if z else "" for z in out]
