"""Alle Fragetypen im Terminal stellen (mc, wf, text, ausgabe, ausdruck,
luecke, puzzle, code). Geprüft wird ausschließlich über frage.pruefen()."""

from __future__ import annotations

import os
import random
import re
import textwrap
from dataclasses import dataclass

from . import render as r
from .konsole import WEISS_NICHT, ausgeben, eingabe

PHASEN_NAME = {"verstehen": "Verstehen", "ueben": "Üben", "programmieren": "Programmieren"}
PHASEN_FARBE = {"verstehen": r.magenta, "ueben": r.blau, "programmieren": r.gruen}
TYP_SYMBOL = {"mc": "🔘", "wf": "⚖", "text": "✏", "ausgabe": "🖥", "ausdruck": "🧮",
              "luecke": "🧩", "puzzle": "🔀", "code": "⌨"}


@dataclass
class Antwort:
    """Ergebnis einer gestellten Frage."""
    ok: bool = False
    versuch: int = 1
    xp: int = 0
    uebersprungen: bool = False
    loesung_gesehen: bool = False


class Kontext:
    """Was die Fragen von außen brauchen."""

    def __init__(self, markup, verbuchen=None, entwurf_laden=None, entwurf_speichern=None,
                 loesung_angesehen=None, pruefungsmodus=False):
        self.markup = markup
        self.loesung_angesehen = loesung_angesehen or (lambda frage: None)
        self.verbuchen = verbuchen or (lambda frage, ok, versuch: 0)
        self.entwurf_laden = entwurf_laden or (lambda fid: None)
        self.entwurf_speichern = entwurf_speichern or (lambda fid, code: None)
        self.pruefungsmodus = pruefungsmodus
        self.ausgabe_hinweis_gezeigt = False
        self.code_hilfe_gezeigt = False


# ════════════════════════════════════════════════════════════════════════════
#  Bausteine
# ════════════════════════════════════════════════════════════════════════════

def _w():
    return r.breite()


def markup_zeilen(ctx, text, einzug="  ", w=None):
    """Markup-Text (mehrere Seiten werden einfach aneinandergehängt)."""
    if not text:
        return []
    try:
        seiten = ctx.markup.parse(str(text))
    except Exception:
        return [einzug + z for z in r.umbrechen(str(text), (w or _w()) - len(einzug))]
    bloecke = [b for s in seiten for b in s]
    return r.seite_zeilen(bloecke, w or _w(), einzug=einzug)


def code_zeigen(code, titel=None, luecken=False, nummern=True):
    w = _w() - 2
    ausgeben(["  " + z for z in r.code_kasten(code, w, titel=titel, nummern=nummern, luecken=luecken)])


def kopf(frage, nr, gesamt, zusatz=None):
    w = _w()
    phase = getattr(frage, "phase", "ueben")
    f = PHASEN_FARBE.get(phase, r.blau)
    links = f"━━ {'Aufgabe' if phase == 'programmieren' else 'Frage'} {nr}/{gesamt} "
    mitte = f"{TYP_SYMBOL.get(frage.typ, '•')} {frage.art} "
    rechts = f" {PHASEN_NAME.get(phase, '')} ━━"
    fuell = max(3, w - r.sichtbreite(links) - r.sichtbreite(mitte) - r.sichtbreite(rechts))
    ausgeben("")
    ausgeben(f(r.fett(links)) + r.fett(mitte) + f("━" * fuell) + f(r.fett(rechts)))
    if zusatz:
        ausgeben("  " + r.grau(zusatz))


def tipp_zeigen(frage, ctx, stufe):
    """Zeigt Tipp Nummer 'stufe' (0-basiert). Rückgabe: nächste Stufe."""
    if ctx.pruefungsmodus:
        ausgeben("  " + r.grau("In der Prüfung gibt es keine Tipps – du schaffst das!"))
        return stufe
    tipps = list(getattr(frage, "tipps", None) or [])
    if not tipps:
        ausgeben("  " + r.grau("Für diese Frage gibt es leider keinen Tipp."))
        return stufe
    i = min(stufe, len(tipps) - 1)
    titel = f"Tipp {i + 1}/{len(tipps)}" if len(tipps) > 1 else "Tipp"
    zeilen = markup_zeilen(ctx, tipps[i], einzug="", w=_w() - 6)
    ausgeben(["  " + z for z in r.kasten(zeilen, _w() - 2, titel="💡 " + titel, farbe=r.gelb)])
    if stufe >= len(tipps) - 1 and len(tipps) > 1:
        ausgeben("  " + r.grau("(Das war der letzte Tipp.)"))
    return stufe + 1


def erklaerung_zeigen(ctx, text):
    if not text or not str(text).strip():
        return
    zeilen = markup_zeilen(ctx, text, einzug="", w=_w() - 6)
    ausgeben("")
    ausgeben(["  " + z for z in r.kasten(zeilen, _w() - 2, titel="💬 Erklärung", farbe=r.blau)])


def rueckmeldung(ctx, frage, erg, antwort, loesung_text=None, loesung_als_code=False):
    """Zeigt ✔/✘, Lösung, Hinweis, Erklärung und XP."""
    ausgeben("")
    if erg.ok:
        meldung = erg.meldung or "Richtig!"
        if not meldung.startswith("✔"):
            meldung = "✔ " + meldung
        zeile = "  " + r.gruen(r.fett(meldung))
        if antwort.xp:
            zeile += "   " + r.gelb(r.fett(f"+{antwort.xp} XP"))
        if antwort.versuch == 2:
            zeile += r.grau("  (im 2. Versuch)")
        ausgeben(zeile)
    else:
        meldung = erg.meldung or "Leider nicht richtig."
        if meldung.startswith("✔"):
            meldung = "Leider nicht richtig."
        ausgeben("  " + r.rot(r.fett("✘ " + meldung)))
        loesung = loesung_text if loesung_text is not None else erg.loesung
        if loesung is not None and loesung != "":
            if loesung_als_code or "\n" in str(loesung):
                ausgeben("  " + r.fett("Richtige Lösung:"))
                code_zeigen(str(loesung), nummern=False)
            else:
                ausgeben("  " + r.fett("Richtige Antwort: ") + r.gruen(r.inline(str(loesung))))
    if erg.hinweis:
        ausgeben(["  " + z for z in r.haengend("ℹ ", str(erg.hinweis), _w() - 4, basis=r.gelb,
                                               praefix_stil=r.gelb)])
    erklaerung_zeigen(ctx, erg.erklaerung)


def _ist_weiss_nicht(a):
    return a.strip().lower() in WEISS_NICHT


def _verbuchen(ctx, frage, ok, versuch, antwort):
    try:
        xp = ctx.verbuchen(frage, ok, versuch)
        antwort.xp = int(xp or 0) if ok else 0
    except Exception:
        antwort.xp = 0


def _fehlversuch_hinweis(frage, ctx, erg, tippstufe):
    """Nach dem 1. falschen Versuch: Hinweis + automatisch Tipp 1."""
    if erg.hinweis:
        ausgeben("  " + r.gelb("ℹ " + r.inline(str(erg.hinweis))))
    meldung = erg.meldung if (erg.meldung and not erg.meldung.startswith("Leider")) else None
    if meldung:
        ausgeben("  " + r.gelb(r.inline(meldung)))
    ausgeben("  " + r.gelb(r.fett("Nicht ganz – du hast noch einen Versuch!")))
    if getattr(frage, "tipps", None) and not ctx.pruefungsmodus and tippstufe == 0:
        return tipp_zeigen(frage, ctx, 0)
    return tippstufe


def _hilfezeile(ctx, extra=""):
    teile = []
    if extra:
        teile.append(extra)
    if not ctx.pruefungsmodus:
        teile.append("? = Tipp")
    teile.append("x = weiß nicht")
    teile.append("menü = Hauptmenü")
    return "\n".join(r.teile_umbrechen([r.grau(t) for t in teile], _w(), r.grau("  ·  ")))


# ════════════════════════════════════════════════════════════════════════════
#  Einfache Fragetypen
# ════════════════════════════════════════════════════════════════════════════

def _mc(frage, ctx, antwort):
    d = frage.to_dict(mischen=True)
    optionen = d.get("optionen") or []
    ausgeben(markup_zeilen(ctx, d.get("frage", "")))
    if d.get("code"):
        code_zeigen(d["code"])
    buchstaben = "abcdefghij"[:len(optionen)]
    ausgeben("")
    for b, o in zip(buchstaben, optionen):
        ausgeben(["    " + z for z in r.haengend(f"{b}) ", o, _w() - 6,
                                                 praefix_stil=lambda s: r.blau(r.fett(s)))])
    ausgeben("")
    ausgeben(_hilfezeile(ctx, f"Antwort: {'/'.join(buchstaben)} oder 1–{len(optionen)}"))
    tippstufe = 0
    while True:
        a = eingabe("  Deine Wahl: ").strip().lower()
        if a == "?":
            tippstufe = tipp_zeigen(frage, ctx, tippstufe)
            continue
        if _ist_weiss_nicht(a):
            wahl = None
            break
        a = a.rstrip(")").strip()
        if len(a) == 1 and a in buchstaben:
            wahl = buchstaben.index(a)
            break
        if a.isdigit() and 1 <= int(a) <= len(optionen):
            wahl = int(a) - 1
            break
        ausgeben("  " + r.grau(f"Bitte einen der Buchstaben {', '.join(buchstaben)} eintippen."))
    erg = frage.pruefen(optionen[wahl] if wahl is not None else "")
    _verbuchen(ctx, frage, erg.ok, 1, antwort)
    antwort.ok = erg.ok
    richtig_txt = erg.loesung
    if not erg.ok and erg.loesung in optionen:
        richtig_txt = f"{buchstaben[optionen.index(erg.loesung)]}) {erg.loesung}"
    rueckmeldung(ctx, frage, erg, antwort, loesung_text=richtig_txt)


def _wf(frage, ctx, antwort):
    d = frage.to_dict(mischen=False)
    ausgeben("  " + r.grau("Stimmt diese Aussage?"))
    ausgeben(markup_zeilen(ctx, d.get("aussage", "")))
    if d.get("code"):
        code_zeigen(d["code"])
    ausgeben("")
    ausgeben(_hilfezeile(ctx, "w = wahr, f = falsch"))
    tippstufe = 0
    while True:
        a = eingabe("  Wahr oder falsch? ").strip().lower()
        if a == "?":
            tippstufe = tipp_zeigen(frage, ctx, tippstufe)
            continue
        if _ist_weiss_nicht(a):
            wert = None
            break
        if a in ("w", "wahr", "j", "ja", "true", "t", "1", "richtig", "stimmt"):
            wert = True
            break
        if a in ("f", "falsch", "n", "nein", "false", "0", "stimmt nicht"):
            wert = False
            break
        ausgeben("  " + r.grau("Bitte w (wahr) oder f (falsch) eingeben."))
    if wert is None:
        erg = frage.pruefen(not frage.wahr) if hasattr(frage, "wahr") else frage.pruefen("?")
        erg.ok = False
    else:
        erg = frage.pruefen(wert)
    _verbuchen(ctx, frage, erg.ok, 1, antwort)
    antwort.ok = erg.ok
    rueckmeldung(ctx, frage, erg, antwort, loesung_text=(erg.loesung or "").upper())


def _freitext(frage, ctx, antwort, prompt, vorbereiten):
    """Gemeinsamer Ablauf für text/ausgabe/ausdruck: 2 Versuche (Prüfung: 1)."""
    vorbereiten()
    versuche = 1 if ctx.pruefungsmodus else 2
    tippstufe = 0
    erg = None
    for versuch in range(1, versuche + 1):
        while True:
            a = eingabe(prompt)
            if a.strip() == "?":
                tippstufe = tipp_zeigen(frage, ctx, tippstufe)
                continue
            if a.strip():
                break
            ausgeben("  " + r.grau("Bitte gib eine Antwort ein (x = weiß nicht)."))
        if _ist_weiss_nicht(a):
            erg = frage.pruefen("")
            erg.ok = False
            antwort.versuch = versuch
            break
        erg = frage.pruefen(a)
        antwort.versuch = versuch
        if erg.ok:
            break
        if versuch < versuche:
            tippstufe = _fehlversuch_hinweis(frage, ctx, erg, tippstufe)
            erg = None
    antwort.ok = bool(erg and erg.ok)
    _verbuchen(ctx, frage, antwort.ok, antwort.versuch, antwort)
    return erg


def _text(frage, ctx, antwort):
    d = frage.to_dict(mischen=False)

    def vorbereiten():
        ausgeben(markup_zeilen(ctx, d.get("frage", "")))
        if d.get("code"):
            code_zeigen(d["code"])
        ausgeben("")
        if d.get("gross_klein"):
            ausgeben("  " + r.gelb("Achtung: Hier zählt die Groß-/Kleinschreibung."))
        ausgeben(_hilfezeile(ctx))
    erg = _freitext(frage, ctx, antwort, "  Deine Antwort: ", vorbereiten)
    rueckmeldung(ctx, frage, erg, antwort)


def _ausgabe(frage, ctx, antwort):
    d = frage.to_dict(mischen=False)

    def vorbereiten():
        ausgeben(markup_zeilen(ctx, d.get("frage", "")))
        code_zeigen(d.get("code") or "")
        if not ctx.ausgabe_hinweis_gezeigt:
            ausgeben(r.grau("  So antwortest du:"))
            ausgeben(r.grau("   • Mehrere Ausgabezeilen? Einfach mit Leerzeichen getrennt eintippen."))
            ausgeben(r.grau("   • Gibt es einen Fehler? Dann tippe den Namen des Fehlers (z. B. TypeError)."))
            ausgeben(r.grau("   • Gibt der Code nichts aus? Dann tippe: nichts"))
            ctx.ausgabe_hinweis_gezeigt = True
        ausgeben(_hilfezeile(ctx, "mehrere Zeilen → Leerzeichen · Fehler → Fehlername"))
    erg = _freitext(frage, ctx, antwort, "  Ausgabe: ", vorbereiten)
    loesung = erg.loesung if erg else None
    if erg and not erg.ok and loesung is not None:
        ausgeben("")
        ausgeben("  " + r.rot(r.fett("✘ " + (erg.meldung or "Leider nicht richtig."))))
        ausgeben("  " + r.fett("So sieht die echte Ausgabe aus:"))
        zeilen = str(loesung).split("\n")
        ausgeben(["  " + z for z in r.kasten([r.rot(z) if z.startswith("Fehler:") else z for z in zeilen],
                                              _w() - 2, titel="Ausgabe", farbe=r.grau)])
        if erg.hinweis:
            ausgeben("  " + r.gelb("ℹ " + r.inline(str(erg.hinweis))))
        erklaerung_zeigen(ctx, erg.erklaerung)
        return
    rueckmeldung(ctx, frage, erg, antwort)


def _ausdruck(frage, ctx, antwort):
    d = frage.to_dict(mischen=False)

    def vorbereiten():
        ausgeben(markup_zeilen(ctx, d.get("frage", "")))
        if d.get("gegeben"):
            ausgeben("  " + r.grau("Gegeben ist:"))
            code_zeigen(d["gegeben"], nummern=False)
        if d.get("muss_enthalten"):
            ausgeben("  " + r.grau("Dein Ausdruck muss ") + r.cyan(str(d["muss_enthalten"]))
                     + r.grau(" enthalten."))
        ausgeben(_hilfezeile(ctx, "Tippe einen Python-Ausdruck, z. B. lst[0] + 1"))
    erg = _freitext(frage, ctx, antwort, "  Ausdruck: ", vorbereiten)
    rueckmeldung(ctx, frage, erg, antwort)


# ════════════════════════════════════════════════════════════════════════════
#  Lückencode
# ════════════════════════════════════════════════════════════════════════════

def _luecke(frage, ctx, antwort):
    d = frage.to_dict(mischen=False)
    n = int(d.get("anzahl_luecken") or str(d.get("code") or "").count("___"))
    ausgeben(markup_zeilen(ctx, d.get("frage", "")))
    code_zeigen(d.get("code") or "", titel="Lückencode", luecken=True)
    ausgeben(_hilfezeile(ctx, f"Fülle die {n} Lücke{'n' if n != 1 else ''} nacheinander aus"))
    versuche = 1 if ctx.pruefungsmodus else 2
    werte = [""] * n
    richtig = [False] * n
    tippstufe = 0
    erg = None
    for versuch in range(1, versuche + 1):
        antwort.versuch = versuch
        abbruch = False
        for i in range(n):
            if richtig[i]:
                ausgeben("  " + r.gruen(f"  [{i + 1}] ✓ ") + r.cyan(werte[i]))
                continue
            while True:
                zusatz = ""
                if versuch > 1 and werte[i]:
                    zusatz = r.grau(f" (vorher: {werte[i]})")
                a = eingabe(f"  Lücke {r.hl_gelb(f'[{i + 1}]') if r.farben_an() else f'[{i + 1}]'}{zusatz}: ")
                if a.strip() == "?":
                    tippstufe = tipp_zeigen(frage, ctx, tippstufe)
                    continue
                if _ist_weiss_nicht(a):
                    abbruch = True
                    break
                if a.strip():
                    werte[i] = a.strip()
                    break
                ausgeben("  " + r.grau("Bitte etwas eintragen (x = weiß nicht)."))
            if abbruch:
                break
        if abbruch:
            erg = frage.pruefen(["\u0000"] * n)
            erg.ok = False
            break
        erg = frage.pruefen(werte)
        if erg.ok:
            break
        for i, det in enumerate((erg.details or [])[:n]):
            richtig[i] = bool(det.get("ok"))
        if versuch < versuche:
            ausgeben("")
            for i in range(n):
                sym = r.gruen("✓") if richtig[i] else r.rot("✗")
                ausgeben(f"    {sym} Lücke [{i + 1}]: " + r.cyan(werte[i]))
            tippstufe = _fehlversuch_hinweis(frage, ctx, erg, tippstufe)
            ausgeben("  " + r.grau("Die richtigen Lücken bleiben stehen – fülle nur die falschen neu aus."))
    antwort.ok = bool(erg and erg.ok)
    _verbuchen(ctx, frage, antwort.ok, antwort.versuch, antwort)
    if antwort.ok:
        rueckmeldung(ctx, frage, erg, antwort)
        return
    ausgeben("")
    ausgeben("  " + r.rot(r.fett("✘ " + (erg.meldung if erg and erg.meldung else "Leider nicht richtig."))))
    ausgeben("  " + r.fett("Der vollständige Code:"))
    code_zeigen(frage.loesung_anzeigen())
    erklaerung_zeigen(ctx, erg.erklaerung if erg else frage.erklaerung)


# ════════════════════════════════════════════════════════════════════════════
#  Code-Puzzle
# ════════════════════════════════════════════════════════════════════════════

def _einrueckung_zeigen(text, einrueckung):
    stufen = einrueckung // 4
    rest = einrueckung % 4
    return r.grau("┊   " * stufen) + " " * rest + text


def puzzle_zeilen_zeigen(zeilen):
    w = _w() - 2
    inhalt = []
    nb = len(str(len(zeilen)))
    for i, z in enumerate(zeilen, 1):
        code = r.py_farben(z["text"])[0]
        inhalt.append(r.blau(r.fett(str(i).rjust(nb))) + r.grau(" │ ") + _einrueckung_zeigen(code, z["einrueckung"]))
    ausgeben(["  " + z for z in r.kasten(inhalt, w, titel="🔀 Zeilen (gemischt)", farbe=r.grau, stil="eckig")])


def _puzzle(frage, ctx, antwort):
    d = frage.to_dict(mischen=True)
    zeilen = d.get("zeilen") or []
    anzahl = int(d.get("anzahl") or len(zeilen))
    ausgeben(markup_zeilen(ctx, d.get("aufgabe", "")))
    puzzle_zeilen_zeigen(zeilen)
    if anzahl < len(zeilen):
        ausgeben("  " + r.gelb(f"Achtung: Nur {anzahl} der {len(zeilen)} Zeilen gehören in die Lösung "
                               "– lass die falschen einfach weg!"))
    ausgeben("  " + r.grau("Die Einrückung (┊) ist schon richtig vorgegeben."))
    ausgeben(_hilfezeile(ctx, f"Reihenfolge eingeben, z. B. {' '.join(str(i) for i in range(1, min(anzahl, 4) + 1))}"))
    versuche = 1 if ctx.pruefungsmodus else 2
    tippstufe = 0
    erg = None
    for versuch in range(1, versuche + 1):
        antwort.versuch = versuch
        while True:
            a = eingabe("  Reihenfolge: ").strip()
            if a == "?":
                tippstufe = tipp_zeigen(frage, ctx, tippstufe)
                continue
            if _ist_weiss_nicht(a):
                reihenfolge = None
                break
            if a.lower() == "z":
                puzzle_zeilen_zeigen(zeilen)
                continue
            nummern = re.findall(r"-?\d+", a)
            if not nummern:
                ausgeben("  " + r.grau("Bitte Zeilennummern mit Leerzeichen getrennt eingeben, z. B. 3 1 2. "
                                       "(z = Zeilen nochmal zeigen)"))
                continue
            nummern = [int(x) for x in nummern]
            falsch = [x for x in nummern if not 1 <= x <= len(zeilen)]
            if falsch:
                ausgeben("  " + r.rot(f"Die Zeile {falsch[0]} gibt es nicht (1 bis {len(zeilen)})."))
                continue
            if len(set(nummern)) != len(nummern):
                ausgeben("  " + r.rot("Jede Zeile darf nur einmal vorkommen."))
                continue
            if len(nummern) != anzahl:
                ausgeben("  " + r.gelb(f"Du hast {len(nummern)} Zeilen gewählt – die Lösung braucht genau "
                                       f"{anzahl}."))
                continue
            reihenfolge = nummern
            break
        if reihenfolge is None:
            erg = frage.pruefen([])
            erg.ok = False
            break
        gewaehlt = [zeilen[i - 1] for i in reihenfolge]
        code = "\n".join(" " * z["einrueckung"] + z["text"] for z in gewaehlt)
        code_zeigen(code, titel="Deine Reihenfolge")
        erg = frage.pruefen([z["zeilen_id"] for z in gewaehlt])
        if erg.ok:
            break
        if versuch < versuche:
            tippstufe = _fehlversuch_hinweis(frage, ctx, erg, tippstufe)
            puzzle_zeilen_zeigen(zeilen)
    antwort.ok = bool(erg and erg.ok)
    _verbuchen(ctx, frage, antwort.ok, antwort.versuch, antwort)
    if antwort.ok:
        rueckmeldung(ctx, frage, erg, antwort)
        return
    ausgeben("")
    ausgeben("  " + r.rot(r.fett("✘ " + (r.inline(erg.meldung) if erg and erg.meldung else "Leider nicht richtig."))))
    ausgeben("  " + r.fett("Die richtige Reihenfolge:"))
    code_zeigen(frage.loesung_anzeigen())
    erklaerung_zeigen(ctx, erg.erklaerung if erg else frage.erklaerung)


# ════════════════════════════════════════════════════════════════════════════
#  Programmieraufgaben
# ════════════════════════════════════════════════════════════════════════════

CODE_HILFE = [
    "Tippe deinen Code Zeile für Zeile (einrücken mit 4 Leerzeichen oder Tab).",
    "Fertig? Dann schreibe in eine neue Zeile nur:  **ENDE**",
    "Weitere Befehle (jeweils allein in einer Zeile):",
]
BEFEHLE = [
    ("ENDE", "Code prüfen"),
    ("ZEIGEN", "bisherigen Code anzeigen"),
    ("ZURÜCK", "letzte Zeile löschen"),
    ("ÄNDERN n", "Zeile n neu schreiben"),
    ("EINFÜGEN n", "vor Zeile n eine Zeile einfügen"),
    ("LÖSCHEN n", "Zeile n löschen"),
    ("NEU", "alles löschen und neu anfangen"),
    ("DATEI pfad.py", "Code aus einer Datei laden und prüfen"),
    ("V", "Vorlage übernehmen"),
    ("E", "gespeicherten Entwurf laden"),
    ("?", "nächster Tipp"),
    ("LÖSUNG", "Musterlösung ansehen"),
    ("SKIP", "Aufgabe überspringen"),
]


def _befehl(z):
    t = z.strip()
    oben = t.upper().replace("OE", "Ö").replace("UE", "Ü").replace("AE", "Ä")
    return t, oben


def code_hilfe_zeigen(hat_vorlage, hat_entwurf):
    ausgeben(["  " + r.grau("│ ") + z for z in r.umbrechen(" ".join(CODE_HILFE[:2]), _w() - 6, basis=r.grau)])
    teile = []
    for b, t in BEFEHLE:
        if b == "V" and not hat_vorlage:
            continue
        if b == "E" and not hat_entwurf:
            continue
        teile.append(r.fett(b) + r.grau(f" = {t}"))
    zeilen, akt = [], ""
    for t in teile:
        if akt and r.sichtbreite(akt) + 3 + r.sichtbreite(t) > _w() - 6:
            zeilen.append(akt)
            akt = ""
        akt = (akt + r.grau(" · ") if akt else "") + t
    if akt:
        zeilen.append(akt)
    ausgeben(["  " + r.grau("│ ") + z for z in zeilen])


def code_editor(zeilen, vorlage=None, entwurf=None, start_text=None, kompakt=False):
    """Zeilenweiser Mini-Editor. Rückgabe: (aktion, zeilen)
    aktion: 'pruefen', 'tipp', 'loesung', 'skip', 'datei' (dann zeilen = geladener Code)."""
    zeilen = list(zeilen or [])
    if zeilen:
        ausgeben("  " + r.grau("Dein bisheriger Code (du schreibst unten weiter):"))
        code_zeigen("\n".join(zeilen))
    while True:
        nr = len(zeilen) + 1
        prompt = "  " + r.cyan(f"{nr:>3} │ ")
        z = eingabe(prompt)
        t, oben = _befehl(z)
        if oben == "ENDE":
            return "pruefen", zeilen
        if t == "?":
            return "tipp", zeilen
        if oben in ("LÖSUNG", "LOSUNG"):
            return "loesung", zeilen
        if oben == "SKIP":
            return "skip", zeilen
        if oben in ("ZEIGEN", "ANZEIGEN"):
            if zeilen:
                code_zeigen("\n".join(zeilen), titel="Dein Code bisher")
            else:
                ausgeben("  " + r.grau("(noch leer)"))
            continue
        if oben in ("ZURÜCK", "ZURUCK"):
            if zeilen:
                weg = zeilen.pop()
                ausgeben("  " + r.grau(f"Zeile {len(zeilen) + 1} gelöscht: ") + r.cyan(weg))
            continue
        if oben == "NEU":
            zeilen = []
            ausgeben("  " + r.grau("Alles gelöscht – fang neu an."))
            continue
        if oben == "HILFE":
            code_hilfe_zeigen(vorlage is not None, entwurf is not None)
            continue
        if oben == "V" and vorlage is not None:
            zeilen = str(vorlage).expandtabs(4).rstrip("\n").split("\n")
            ausgeben("  " + r.grau("Vorlage übernommen. Schreib weiter – oder ändere Zeilen mit ÄNDERN n:"))
            code_zeigen("\n".join(zeilen))
            continue
        if oben == "E" and entwurf:
            zeilen = str(entwurf).expandtabs(4).rstrip("\n").split("\n")
            ausgeben("  " + r.grau("Entwurf geladen:"))
            code_zeigen("\n".join(zeilen))
            continue
        m = re.match(r"^(ÄNDERN|ANDERN|EINFÜGEN|EINFUGEN|LÖSCHEN|LOSCHEN)\s+(\d+)$", oben)
        if m:
            befehl, n = m.group(1), int(m.group(2))
            if befehl.startswith(("ÄN", "AN")):
                if not 1 <= n <= len(zeilen):
                    ausgeben("  " + r.rot(f"Zeile {n} gibt es nicht."))
                    continue
                ausgeben("  " + r.grau(f"Bisher: ") + r.py_farben(zeilen[n - 1])[0])
                neu = eingabe("  " + r.gelb(f"{n:>3} │ ")).expandtabs(4)
                zeilen[n - 1] = neu
            elif befehl.startswith(("EIN",)):
                if not 1 <= n <= len(zeilen) + 1:
                    ausgeben("  " + r.rot(f"Zeile {n} gibt es nicht."))
                    continue
                neu = eingabe("  " + r.gelb(f"{n:>3} │ ")).expandtabs(4)
                zeilen.insert(n - 1, neu)
            else:
                if not 1 <= n <= len(zeilen):
                    ausgeben("  " + r.rot(f"Zeile {n} gibt es nicht."))
                    continue
                weg = zeilen.pop(n - 1)
                ausgeben("  " + r.grau(f"Zeile {n} gelöscht: ") + r.cyan(weg))
            code_zeigen("\n".join(zeilen), titel="Dein Code jetzt")
            continue
        if oben.startswith("DATEI ") or oben == "DATEI":
            pfad = t[5:].strip().strip('"').strip("'")
            if not pfad:
                ausgeben("  " + r.grau("Bitte so: DATEI C:\\Pfad\\zu\\meinem_code.py"))
                continue
            pfad = os.path.expanduser(pfad)
            try:
                with open(pfad, encoding="utf-8-sig") as f:
                    inhalt = f.read().expandtabs(4)
            except OSError as e:
                ausgeben("  " + r.rot(f"Datei konnte nicht gelesen werden: {e.strerror or e}"))
                continue
            except UnicodeDecodeError:
                ausgeben("  " + r.rot("Die Datei ist nicht in UTF-8 gespeichert."))
                continue
            ausgeben("  " + r.grau(f"({len(inhalt.splitlines())} Zeilen aus {pfad} geladen)"))
            return "datei", inhalt.rstrip("\n").split("\n")
        zeilen.append(z.expandtabs(4).rstrip("\r"))


def test_details_zeilen(details, w):
    """Testergebnisse ✓/✗ als Zeilen."""
    out = []
    for d in details or []:
        ok = d.get("ok")
        sym = r.gruen(r.fett("✓")) if ok else r.rot(r.fett("✗"))
        name = str(d.get("name") or "Test")
        out.append(sym + " " + (r.inline(name) if ok else r.fett(r.inline(name))))
        if ok:
            continue
        einr = "    "
        if d.get("meldung"):
            out.extend(einr + z for z in r.umbrechen(str(d["meldung"]), w - 4, basis=r.rot))
        if d.get("regel"):
            continue
        if d.get("eingaben") and "Eingaben:" not in name:
            out.append(einr + r.grau("Eingaben: ") + ", ".join(r.cyan(str(e)) for e in d["eingaben"]))
        if d.get("erwartet") and not str(d.get("meldung", "")).startswith("Erwartet wurde eine Zeile"):
            ew = str(d["erwartet"]).split("\n")
            out.append(einr + r.grau("Erwartet: ") + ew[0])
            out.extend(einr + "          " + z for z in ew[1:8])
        aus = d.get("ausgabe")
        if aus is not None and d.get("meldung", "") != "nicht ausgeführt (Syntaxfehler)":
            az = str(aus).split("\n") if str(aus) else []
            if len(az) > 8:
                az = az[:8] + [r.grau(f"… ({len(az) - 8} weitere Zeilen)")]
            out.append(einr + r.grau("Deine Ausgabe:") + (r.grau(" (nichts)") if not az else ""))
            out.extend(einr + r.grau("│ ") + z for z in az)
        if d.get("fehler") and d.get("fehler") not in str(d.get("meldung")):
            out.append(einr + r.rot("Fehler: " + str(d["fehler"])))
    return out


def _code(frage, ctx, antwort):
    d = frage.to_dict(mischen=False)
    ausgeben(markup_zeilen(ctx, d.get("aufgabe", "")))
    regeln = []
    if d.get("verboten"):
        regeln.append("Verboten: " + ", ".join(f"`{v.strip()}`" for v in d["verboten"]))
    if d.get("pflicht"):
        regeln.append("Muss vorkommen: " + ", ".join(f"`{v.strip()}`" for v in d["pflicht"]))
    if d.get("rekursiv"):
        namen = [n.strip() for n in str(d["rekursiv"]).split("|") if n.strip()]
        if len(namen) > 1:
            regeln.append("Eine der Funktionen " + " oder ".join(f"`{n}`" for n in namen)
                          + " muss sich selbst aufrufen (Rekursion).")
        else:
            regeln.append(f"Die Funktion `{d['rekursiv']}` muss sich selbst aufrufen (Rekursion).")
    for regel in d.get("regeln") or []:
        regeln.append("Regel: " + str(regel))
    if d.get("genaue_ausgabe"):
        regeln.append("Die Ausgabe wird genau geprüft: Groß-/Kleinschreibung und Satzzeichen zählen.")
    for regel in regeln:
        ausgeben(["  " + z for z in r.haengend("📏 ", regel, _w() - 4, basis=r.gelb)])
    if d.get("tests"):
        ausgeben("  " + r.grau(f"Dein Code wird mit {len(d['tests'])} automatischen Test(s) geprüft."))
    vorlage = d.get("vorlage")
    if vorlage:
        vorlage = textwrap.dedent(str(vorlage)).strip("\n")
    if vorlage:
        ausgeben("")
        ausgeben("  " + r.grau("So kannst du anfangen (") + r.fett("V") + r.grau(" = Vorlage übernehmen):"))
        code_zeigen(vorlage, titel="Vorlage")
    entwurf = None
    try:
        entwurf = ctx.entwurf_laden(frage.id)
    except Exception:
        entwurf = None
    if entwurf and entwurf.strip():
        ausgeben("  " + r.gelb("📝 Du hast hier schon einen Entwurf gespeichert: ") + r.fett("E")
                 + r.gelb(" = Entwurf laden"))
    else:
        entwurf = None
    ausgeben("")
    if not ctx.code_hilfe_gezeigt:
        code_hilfe_zeigen(vorlage is not None, entwurf is not None)
        ctx.code_hilfe_gezeigt = True
    else:
        ausgeben(r.grau("  ENDE = prüfen · ? = Tipp · V = Vorlage · LÖSUNG · SKIP · HILFE = alle Befehle"))

    zeilen = []
    tippstufe = 0
    einsendungen = 0
    aktion = None
    while True:
        if aktion is None:
            aktion, zeilen = code_editor(zeilen, vorlage, entwurf)
        if aktion == "tipp":
            aktion = None
            tippstufe = tipp_zeigen(frage, ctx, tippstufe)
            continue
        if aktion in ("loesung", "skip"):
            ausgeben("")
            if aktion == "skip":
                ausgeben("  " + r.grau("Übersprungen. Hier die Musterlösung zum Anschauen:"))
            else:
                antwort.loesung_gesehen = True
                try:
                    ctx.loesung_angesehen(frage)
                except Exception:
                    pass
                ausgeben("  " + r.gelb(r.fett("Musterlösung:")))
            code_zeigen(frage.loesung_anzeigen(), titel="Musterlösung")
            erklaerung_zeigen(ctx, frage.erklaerung)
            if aktion == "skip":
                antwort.uebersprungen = True
                antwort.ok = False
                _verbuchen(ctx, frage, False, max(1, einsendungen), antwort)
                return
            ausgeben(["  " + z for z in r.umbrechen("Tipp sie jetzt gern selbst ab – Abtippen trainiert "
                                                    "auch! (Als selbst gelöst zählt die Aufgabe dann aber "
                                                    "nicht.)", _w() - 4, basis=r.grau)])
            aktion = None
            continue
        aktion = None
        code = "\n".join(zeilen)
        if not code.strip():
            ausgeben("  " + r.grau("Du hast noch keinen Code eingegeben."))
            continue
        try:
            ctx.entwurf_speichern(frage.id, code)
        except Exception:
            pass
        einsendungen += 1
        ausgeben("  " + r.grau("⏳ Teste deinen Code …"))
        erg = frage.pruefen(code)
        ausgeben("")
        ausgeben(["  " + z for z in test_details_zeilen(erg.details, _w() - 4)])
        if erg.ok:
            antwort.versuch = 1 if einsendungen == 1 else 2
            _verbuchen(ctx, frage, True, antwort.versuch, antwort)
            antwort.ok = not antwort.loesung_gesehen   # für die Kapitelpunkte
            ausgeben("")
            zeile = "  " + r.gruen(r.fett(erg.meldung or "✔ Alle Tests bestanden!"))
            if antwort.xp:
                zeile += "   " + r.gelb(r.fett(f"+{antwort.xp} XP"))
            ausgeben(zeile)
            if antwort.loesung_gesehen:
                ausgeben("  " + r.grau("(Da du die Lösung angesehen hast, zählt die Aufgabe nicht als "
                                       "selbst gelöst.)"))
            ausgeben("")
            ausgeben("  " + r.grau("Zum Vergleich die Musterlösung:"))
            code_zeigen(frage.loesung_anzeigen(), titel="Musterlösung")
            erklaerung_zeigen(ctx, frage.erklaerung)
            return
        ausgeben("")
        ausgeben("  " + r.rot(r.fett("✘ " + r.inline(erg.meldung or "Noch nicht ganz."))))
        if erg.hinweis:
            ausgeben(["  " + z for z in r.haengend("ℹ ", str(erg.hinweis), _w() - 4, basis=r.gelb,
                                                   praefix_stil=r.gelb)])
        ausgeben("  " + r.grau("Kein Problem – Fehler sind normal! Wie geht's weiter?"))
        ausgeben("  " + r.fett("[Enter]") + r.grau(" = Code weiter bearbeiten   ") + r.fett("n")
                 + r.grau(" = neu schreiben   ") + r.fett("?") + r.grau(" = Tipp   ") + r.fett("LÖSUNG")
                 + r.grau("   ") + r.fett("SKIP"))
        while True:
            _, oben = _befehl(eingabe("  Deine Wahl: "))
            if oben == "?":
                tippstufe = tipp_zeigen(frage, ctx, tippstufe)
                continue
            break
        if oben in ("N", "NEU"):
            zeilen = []
        elif oben in ("LÖSUNG", "LOSUNG"):
            aktion = "loesung"
        elif oben == "SKIP":
            aktion = "skip"


# ════════════════════════════════════════════════════════════════════════════
#  Einstieg
# ════════════════════════════════════════════════════════════════════════════

STELLER = {"mc": _mc, "wf": _wf, "text": _text, "ausgabe": _ausgabe, "ausdruck": _ausdruck,
           "luecke": _luecke, "puzzle": _puzzle, "code": _code}


def stellen(frage, nr, gesamt, ctx, zusatz=None):
    """Stellt eine Frage und gibt ein Antwort-Objekt zurück.
    ZurueckZumMenue/ProgrammEnde werden durchgereicht."""
    kopf(frage, nr, gesamt, zusatz)
    antwort = Antwort()
    f = STELLER.get(getattr(frage, "typ", ""))
    if f is None:
        ausgeben("  " + r.rot(f"(Unbekannter Fragetyp '{getattr(frage, 'typ', '?')}' – wird übersprungen.)"))
        antwort.uebersprungen = True
        return antwort
    f(frage, ctx, antwort)
    return antwort


def lob():
    return random.choice(["Richtig!", "Super!", "Klasse!", "Stark!", "Sehr gut!"])
