"""Terminal-Oberfläche des Vorkurs-Lernquiz.

Einstieg: main(farben=True)

Bedienung überall:  ? = Tipp · x = weiß nicht · menü oder Strg+C = Hauptmenü
Code-Eingabe:       Zeile für Zeile, ENDE = prüfen, DATEI pfad.py, LÖSUNG, SKIP
"""

from __future__ import annotations

import random
import sys
import textwrap

from . import fragen as fr
from . import konsole as k
from . import render as r
from .konsole import ProgrammEnde, ZurueckZumMenue, ausgeben, eingabe, ja_nein, weiter

PHASEN = [("verstehen", "Verstehen"), ("ueben", "Üben"), ("programmieren", "Programmieren"),
          ("merkzettel", "Merkzettel")]

BEISPIELE = [
    ("Begrüßung mit input()", 'name = input("Wie heißt du? ")\nalter = int(input("Wie alt bist du? "))\n'
     'print("Hallo", name)\nprint("In 10 Jahren bist du", alter + 10)', ["Anna", "19"]),
    ("Summe mit while", "summe = 0\nzahl = 1\nwhile zahl <= 4:\n    summe += zahl\n    zahl += 1\n"
     "print(summe)", []),
    ("Liste und for", 'einkauf = ["Brot", "Milch", "Käse"]\nfor i, ding in enumerate(einkauf):\n'
     '    print(i, ding)\neinkauf.append("Äpfel")\nprint(len(einkauf))', []),
    ("Rekursion: Fakultät", "def fak(n):\n    if n <= 1:\n        return 1\n    return n * fak(n - 1)\n\n"
     "print(fak(4))", []),
]


def _w():
    return r.breite()


def _eingerueckt(zeilen, einzug="  "):
    return [einzug + z if z else "" for z in zeilen]


class App:
    def __init__(self, engine, markup, sandbox, fortschritt, inhalte):
        self.engine = engine
        self.markup = markup
        self.sandbox = sandbox
        self.fs = fortschritt
        self.inhalte = inhalte
        self.daten = fortschritt.laden()
        self.neue_abzeichen = []
        self._ausfuehr_cache = {}
        self._speicher_warnung = False

    # ────────────────────────────────────────────────────────────────────
    #  Fortschritt
    # ────────────────────────────────────────────────────────────────────

    def speichern(self):
        try:
            ok = self.fs.speichern(self.daten)
        except Exception:
            ok = False
        if not ok and not self._speicher_warnung:
            self._speicher_warnung = True
            ausgeben("  " + r.gelb("⚠ Der Fortschritt konnte nicht gespeichert werden "
                                   "(keine Schreibrechte?)."))

    def kontext(self, pruefungsmodus=False):
        def verbuchen(frage, ok, versuch):
            res = self.fs.antwort_verbuchen(self.daten, frage, ok, versuch, endgueltig=True)
            self.neue_abzeichen.extend(res.get("neue_abzeichen") or [])
            self.speichern()
            return res.get("xp_neu", 0)

        def entwurf_laden(fid):
            return (self.daten.get("entwuerfe") or {}).get(fid)

        def entwurf_speichern(fid, code):
            self.fs.entwurf_speichern(self.daten, fid, code)
            self.speichern()

        def loesung_angesehen(frage):
            self.fs.loesung_angesehen(self.daten, frage)
            self.speichern()

        return fr.Kontext(self.markup, verbuchen, entwurf_laden, entwurf_speichern,
                          loesung_angesehen, pruefungsmodus)

    def abzeichen_feiern(self, liste=None):
        liste = self.neue_abzeichen if liste is None else liste
        if not liste:
            return
        inhalt = []
        for a in liste:
            inhalt.append(f"{a.get('icon', '🏅')}  " + r.fett(a.get("titel", "")) + r.grau(" – ")
                          + a.get("beschreibung", ""))
        titel = "🏅 Neues Abzeichen!" if len(liste) == 1 else f"🏅 {len(liste)} neue Abzeichen!"
        ausgeben("")
        ausgeben(_eingerueckt(r.kasten(inhalt, _w() - 2, titel=titel, farbe=r.gelb, stil="doppelt")))
        if liste is self.neue_abzeichen:
            self.neue_abzeichen = []
        else:
            for a in liste:
                if a in self.neue_abzeichen:
                    self.neue_abzeichen.remove(a)

    def statistik(self):
        try:
            return self.fs.statistik(self.daten)
        except Exception:
            return {}

    # ────────────────────────────────────────────────────────────────────
    #  Code ausführen / Schritt für Schritt
    # ────────────────────────────────────────────────────────────────────

    def ausfuehren(self, code, eingaben=()):
        schluessel = (code, tuple(eingaben or ()))
        if schluessel not in self._ausfuehr_cache:
            self._ausfuehr_cache[schluessel] = self.sandbox.ausfuehren(code, list(eingaben or ()))
        return self._ausfuehr_cache[schluessel]

    def trace_ansehen(self, code, eingaben=()):
        ausgeben("  " + r.grau("⏳ Das Programm wird Schritt für Schritt ausgeführt …"))
        try:
            erg = self.sandbox.trace(code, list(eingaben or ()))
        except Exception as e:
            ausgeben("  " + r.rot(f"Die Schritt-für-Schritt-Ansicht ist fehlgeschlagen: {e}"))
            return
        schritte = erg.get("schritte") or []
        if not schritte:
            ausgeben("")
            ausgeben(_eingerueckt(r.code_kasten(code, _w() - 2, titel="Code",
                                                aktuell=erg.get("fehler_zeile"))))
            ausgeben(_eingerueckt(r.ausgabe_kasten(erg, _w() - 2, titel="Ergebnis")))
            ausgeben("  " + r.gelb("Das Programm startet gar nicht erst – deshalb gibt es keine Schritte."))
            weiter()
            return
        i = 0
        n = len(schritte)
        while True:
            k.bildschirm_leeren()
            ausgeben("")
            ausgeben(r.trace_seite(code, erg, i, _w()))
            ausgeben("")
            if i < n - 1:
                hilfe = "[Enter] weiter · z zurück · a bis zum Ende · q beenden · Zahl = zu Schritt"
            else:
                hilfe = "[Enter] beenden · z zurück · 1 = von vorn"
            a = eingabe(r.grau(f"  {hilfe} ")).strip().lower()
            if a in ("q", "quit", "beenden", "ende"):
                return
            if a in ("z", "zurück", "zurueck", "-"):
                i = max(0, i - 1)
            elif a in ("a", "alles"):
                i = n - 1
            elif a.isdigit():
                i = max(0, min(n - 1, int(a) - 1))
            elif a in ("", "w", "weiter", "+"):
                if i >= n - 1:
                    return
                i += 1
            else:
                ausgeben("  " + r.grau("Enter = weiter, z = zurück, a = bis zum Ende, q = beenden"))
                weiter()

    def visual_ausprobieren(self, block):
        art = block.get("art")
        daten = dict(block.get("daten") or {})
        if art in ("liste", "string"):
            beispiel = "1:3  ::-1  -1  0:5:2"
            frage = "Slice oder Index (z. B. 1:3, ::-1, -1)"
        else:
            beispiel = "2 10 2"
            frage = "range: start stop step (z. B. 2 10 2 oder nur 5)"
        ausgeben("  " + r.cyan(r.fett("✎ Ausprobieren: ")) + r.grau(f"Tippe z. B. {beispiel} – Enter = fertig"))
        while True:
            a = eingabe(f"  {frage}: ").strip()
            if not a:
                return
            neu = dict(daten)
            if art in ("liste", "string"):
                neu["slice"] = a
                neu["markiert"] = []
            else:
                zahlen = a.replace(",", " ").replace("range", " ").replace("(", " ").replace(")", " ").split()
                try:
                    werte = [int(z) for z in zahlen]
                except ValueError:
                    ausgeben("  " + r.rot("Bitte nur ganze Zahlen eingeben, z. B. 0 10 2."))
                    continue
                if not 1 <= len(werte) <= 3:
                    ausgeben("  " + r.rot("Ein bis drei Zahlen: stop  ODER  start stop  ODER  start stop step"))
                    continue
                if len(werte) == 1:
                    werte = [0, werte[0], 1]
                elif len(werte) == 2:
                    werte = [werte[0], werte[1], 1]
                neu.update({"start": werte[0], "stop": werte[1], "step": werte[2]})
            ausgeben("")
            ausgeben(_eingerueckt(r.visual_zeilen(art, neu, _w() - 2)))
            ausgeben("")

    # ────────────────────────────────────────────────────────────────────
    #  Seiten (Erklärungen, Merkzettel, Spickzettel)
    # ────────────────────────────────────────────────────────────────────

    def seiten_zeigen(self, titel, seiten, icon="📖", farbe=r.magenta, phasen=None, rueckfrage=True):
        """Blättert durch Markup-Seiten. Bietet Schritt-für-Schritt und Ausprobieren an."""
        seiten = [s for s in (seiten or []) if s] or [[]]
        i = 0
        gesehen_trace = set()
        while 0 <= i < len(seiten):
            seite = seiten[i]
            ausgeben("")
            if phasen:
                ausgeben(phasen)
            rechts = f"Seite {i + 1}/{len(seiten)}" if len(seiten) > 1 else ""
            links = f"{icon} {titel}"
            ende = (" " + r.grau(rechts) + farbe(" ━━")) if rechts else ""
            fuell = max(3, _w() - r.sichtbreite(links) - 4 - r.sichtbreite(ende))
            ausgeben(farbe(r.fett("━━ " + links + " ")) + farbe("━" * fuell) + ende)
            ausgeben("")
            ausgeben(r.seite_zeilen(seite, _w(), ausfuehren=self.ausfuehren))
            codes = [b for b in seite if b.get("typ") == "code"]
            interaktiv = [b for b in seite if b.get("typ") == "visual" and b.get("art") in r.INTERAKTIV
                          and not b.get("fehler")]
            traces = [b for b in codes if b.get("trace")]
            for b in traces:
                schluessel = (i, codes.index(b))
                if schluessel in gesehen_trace:
                    continue
                gesehen_trace.add(schluessel)
                nr = f" {codes.index(b) + 1}" if len(codes) > 1 else ""
                if ja_nein(f"👣 Beispiel{nr} jetzt Schritt für Schritt ansehen?", standard=True):
                    self.trace_ansehen(b.get("code", ""), b.get("eingaben") or [])
            if not rueckfrage:
                return
            optionen = ["[Enter] weiter"]
            if i > 0:
                optionen.append("z zurück")
            if codes:
                optionen.append("s Schritt für Schritt" if len(codes) == 1
                                else f"s1–s{len(codes)} Schritt für Schritt")
            if interaktiv:
                optionen.append("p ausprobieren" if len(interaktiv) == 1
                                else f"p1–p{len(interaktiv)} ausprobieren")
            optionen.append("menü")
            while True:
                a = eingabe(r.grau("\n  " + " · ".join(optionen) + " ")).strip().lower()
                if a == "":
                    i += 1
                    break
                if a in ("z", "zurück", "zurueck") and i > 0:
                    i -= 1
                    break
                if a.startswith("s") and codes and (a == "s" or a[1:].strip().isdigit()):
                    nr = int(a[1:]) if a[1:].strip().isdigit() else 1
                    if 1 <= nr <= len(codes):
                        b = codes[nr - 1]
                        self.trace_ansehen(b.get("code", ""), b.get("eingaben") or [])
                        break
                if a.startswith("p") and interaktiv and (a == "p" or a[1:].strip().isdigit()):
                    nr = int(a[1:]) if a[1:].strip().isdigit() else 1
                    if 1 <= nr <= len(interaktiv):
                        self.visual_ausprobieren(interaktiv[nr - 1])
                        continue
                ausgeben("  " + r.grau("Das habe ich nicht verstanden."))

    def phasen_leiste(self, aktuell, besucht):
        teile = []
        for pid, name in PHASEN:
            if pid == aktuell:
                teile.append(r.gelb(r.fett("● " + name)))
            elif pid in besucht:
                teile.append(r.gruen("✔ " + name))
            else:
                teile.append(r.grau("○ " + name))
        return "  " + r.grau("[") + r.grau(" ▸ ").join(teile) + r.grau("]")

    # ────────────────────────────────────────────────────────────────────
    #  Start, Hauptmenü
    # ────────────────────────────────────────────────────────────────────

    def starten(self):
        self.begruessung()
        st = self.statistik()
        if not st.get("xp") and not self.daten.get("kapitel"):
            self.hilfe(erster_start=True)
        while True:
            try:
                if not self.hauptmenue():
                    break
            except ZurueckZumMenue:
                ausgeben("\n  " + r.grau("Zurück im Hauptmenü. (Dein Fortschritt ist gespeichert.)"))
            except KeyboardInterrupt:
                ausgeben("\n  " + r.grau("Abgebrochen – zurück im Hauptmenü."))
            self.speichern()
        self.abschied()

    def begruessung(self):
        ausgeben("")
        ausgeben(_eingerueckt(r.banner("🐍 DAS GROSSE PYTHON-VORKURS-LERNQUIZ",
                                       ["Programmiervorkurs TU Darmstadt 2026 · Version 2",
                                        "Erklären → Üben → Programmieren – für komplette Anfänger"],
                                       _w() - 2)))

    def abschied(self):
        self.speichern()
        st = self.statistik()
        ausgeben("")
        zeile = "  " + r.fett("Bis bald – und viel Erfolg im Studium! 👋")
        if st.get("xp"):
            zeile += r.grau(f"   ({st['xp']} XP gesammelt)")
        ausgeben(zeile)
        ausgeben("")

    def kopfzeile(self, st):
        lv = st.get("level") or {}
        xp = st.get("xp", 0)
        teile = [r.gelb(r.fett("⭐ " + lv.get("titel", "Level 1")))]
        if lv.get("xp_naechstes"):
            teile.append(r.balken(xp - lv.get("xp_start", 0), lv["xp_naechstes"] - lv.get("xp_start", 0), 12,
                                  farbig=False) + r.grau(f" {xp}/{lv['xp_naechstes']} XP"))
        else:
            teile.append(r.gelb(f"{xp} XP"))
        serie = (st.get("serie") or {}).get("tage", 0)
        teile.append(("🔥 " + r.fett(f"{serie} Tag{'e' if serie != 1 else ''}")) if serie else r.grau("🔥 0 Tage"))
        teile.append(f"🏅 {len(st.get('abzeichen') or [])}")
        return "  " + "   ".join(teile)

    def kapitel_zeile(self, kap, nummer_breite=2):
        status = self.fs.kapitel_status(self.daten, kap)
        if status["abgeschlossen"]:
            sym = r.gruen("✔")
        elif status["fragen_richtig"]:
            sym = r.gelb("◐")
        else:
            sym = r.grau("·")
        perfekt = status["abgeschlossen"] and status.get("best") is not None and status.get("max") \
            and status["best"] >= status["max"]
        rechts = (r.balken(status["fragen_richtig"], status["fragen_gesamt"], 10)
                  + r.grau(f" {status['fragen_richtig']:>2}/{status['fragen_gesamt']:<2}")
                  + (r.gelb(" ★") if perfekt else "  "))
        links = f"  {r.fett(str(kap.nummer).rjust(nummer_breite))} {sym} "
        icon = (kap.icon or "📘")
        titel_platz = _w() - r.sichtbreite(links) - r.sichtbreite(rechts) - r.sichtbreite(icon) - 3
        titel = r.abschneiden(kap.titel, titel_platz)
        return links + icon + " " + r.pad(titel, titel_platz) + " " + rechts

    def naechstes_kapitel(self):
        for kap in self.engine.KAPITEL:
            if not (self.daten["kapitel"].get(kap.slug) or {}).get("abgeschlossen"):
                return kap
        return None

    @staticmethod
    def teil_kuerzel(teil):
        """tag1 -> 't1', challenge -> 'c', bonus -> 'b'."""
        tid = teil["id"]
        if tid.startswith("tag") and tid[3:].isdigit():
            return "t" + tid[3:]
        return tid[:1]

    def teile_mit_kapiteln(self):
        return [(t, self.engine.kapitel_von_teil(t["id"])) for t in self.engine.TEILE
                if self.engine.kapitel_von_teil(t["id"])]

    def teil_zeile(self, teil, kapitel, st_teil):
        """Eine Zeile der Ebene 1: Kürzel, Titel, Kapitelbereich, Balken, x/y Kapitel."""
        fertig = sum(1 for kap in kapitel if (self.daten["kapitel"].get(kap.slug) or {}).get("abgeschlossen"))
        richtig = (st_teil or {}).get("fragen_richtig", 0)
        gesamt = (st_teil or {}).get("fragen_gesamt", 0) or sum(len(k.fragen()) for k in kapitel)
        if fertig == len(kapitel):
            sym = r.gruen("✔")
        elif fertig or richtig:
            sym = r.gelb("◐")
        else:
            sym = r.grau("·")
        kuerzel = r.magenta(r.fett(f" {self.teil_kuerzel(teil).upper():<2} "))
        bereich = (f"{kapitel[0].nummer}–{kapitel[-1].nummer}" if len(kapitel) > 1 else str(kapitel[0].nummer))
        rechts = (r.balken(richtig, gesamt, 12) + " " + r.pad(f"{fertig}/{len(kapitel)}", 5, "r")
                  + r.grau(" Kapitel"))
        links = "  " + kuerzel + " " + sym + " "
        platz = _w() - r.sichtbreite(links) - r.sichtbreite(rechts) - 2
        titel = r.fett(teil["titel"]) + r.grau(f"  (Kap. {bereich})")
        return links + r.pad(r.abschneiden(titel, platz), platz) + "  " + rechts

    def hauptmenue(self):
        """Ebene 1: Weiterlernen, Teile mit Gesamtfortschritt, übrige Menüpunkte (< 30 Zeilen)."""
        st = self.statistik()
        w = _w()
        ausgeben("")
        ausgeben(r.blau("━" * w))
        ausgeben("  " + r.blau(r.fett("HAUPTMENÜ")) + r.grau("  ·  Buchstabe, Teil (z. B. T1) oder Kapitelnummer"))
        ausgeben(self.kopfzeile(st))
        ausgeben(r.blau("━" * w))
        naechstes = self.naechstes_kapitel()
        if naechstes:
            weiter_txt = f"Weiterlernen  →  Kapitel {naechstes.nummer}: {naechstes.icon} {naechstes.titel}"
        else:
            weiter_txt = "Weiterlernen  →  alles geschafft! 🎉"
        ausgeben("  " + r.gelb(r.fett(" W ")) + " " + r.fett(r.abschneiden(weiter_txt, w - 8)))
        ausgeben("")
        st_teile = {t["id"]: t for t in (st.get("teile") or [])}
        for teil, kapitel in self.teile_mit_kapiteln():
            ausgeben(self.teil_zeile(teil, kapitel, st_teile.get(teil["id"])))
        fk = st.get("fehlerkiste", 0)
        faellig = st.get("faellig", 0)
        punkte = [
            ("K", "Alle Kapitel (Liste)"), ("P", "Prüfung (30 Fragen)"),
            ("F", f"Fehlerkiste ({fk})"), ("R", f"Wiederholen ({faellig} fällig)"),
            ("S", "Spickzettel"), ("L", "Spielwiese (Code ausprobieren)"),
            ("A", "Abzeichen & Statistik"), ("H", "Hilfe"),
            ("Z", "Fortschritt zurücksetzen"), ("X", "Beenden"),
        ]
        ausgeben(r.blau("─" * w))
        spalte = (w - 4) // 2
        for j in range(0, len(punkte), 2):
            zeile = ""
            for b, t in punkte[j:j + 2]:
                eintrag = r.blau(r.fett(f" {b} ")) + " " + r.abschneiden(t, spalte - 5)
                zeile += r.pad(eintrag, spalte)
            ausgeben("  " + zeile.rstrip())
        try:
            wahl = eingabe("\n  " + r.fett("Deine Wahl: "), menue=False).strip().lower()
        except ZurueckZumMenue:   # Strg+C im Hauptmenü = beenden
            wahl = "x"
        return self.menue_ausfuehren(wahl)

    def teil_menue(self, teil, kapitel):
        """Ebene 2: die Kapitel eines Teils."""
        while True:
            ausgeben("")
            fertig = sum(1 for kap in kapitel if (self.daten["kapitel"].get(kap.slug) or {}).get("abgeschlossen"))
            info = [teil["untertitel"]] if teil.get("untertitel") else []
            info.append(f"{fertig} von {len(kapitel)} Kapiteln abgeschlossen")
            ausgeben(_eingerueckt(r.banner(f"{self.teil_kuerzel(teil).upper()} · {teil['titel']}", info,
                                           _w() - 2, farbe=r.magenta)))
            nb = len(str(kapitel[-1].nummer))
            for kap in kapitel:
                ausgeben(self.kapitel_zeile(kap, nb))
            offen = next((kap for kap in kapitel
                          if not (self.daten["kapitel"].get(kap.slug) or {}).get("abgeschlossen")), None)
            hilfe = "Kapitelnummer eingeben"
            if offen:
                hilfe += f" · W = nächstes offenes Kapitel ({offen.nummer})"
            hilfe += " · Enter = zurück zum Hauptmenü"
            ausgeben(r.teile_umbrechen([r.grau(hilfe)], _w()))
            a = eingabe("  Deine Wahl: ").strip().lower()
            if not a:
                return
            if a == "w" and offen:
                self.kapitel_spielen(offen)
                continue
            if a.isdigit() and 1 <= int(a) <= len(self.engine.KAPITEL):
                kap = self.engine.KAPITEL[int(a) - 1]
                self.kapitel_spielen(kap)
                if kap not in kapitel:
                    return
                continue
            ausgeben("  " + r.grau(f"Bitte eine Kapitelnummer ({kapitel[0].nummer}–{kapitel[-1].nummer}) "
                                   "oder Enter eingeben."))

    def menue_ausfuehren(self, wahl):
        wahl = wahl.strip().lower()
        if wahl.isdigit():
            nr = int(wahl)
            if 1 <= nr <= len(self.engine.KAPITEL):
                self.kapitel_spielen(self.engine.KAPITEL[nr - 1])
            else:
                ausgeben("  " + r.grau(f"Kapitel {nr} gibt es nicht (1 bis {len(self.engine.KAPITEL)})."))
            return True
        for teil, kapitel in self.teile_mit_kapiteln():
            kuerzel = self.teil_kuerzel(teil)
            if wahl in (kuerzel, kuerzel.replace("t", "tag"), teil["id"]):
                self.teil_menue(teil, kapitel)
                return True
        aktionen = {
            "w": self.weiterlernen, "k": self.kapitel_waehlen, "p": self.pruefung, "f": self.fehlerkiste,
            "r": self.wiederholen, "s": self.spickzettel, "l": self.spielwiese, "a": self.abzeichen_statistik,
            "h": self.hilfe, "z": self.zuruecksetzen,
        }
        if wahl in ("x", "q", "exit", "quit", "beenden", "ende"):
            return False
        if wahl in ("", "menü", "menue"):
            return True
        f = aktionen.get(wahl) if len(wahl) == 1 else None
        if f is None:
            ausgeben("  " + r.grau("Bitte einen Buchstaben, einen Teil (z. B. T1) oder eine Kapitelnummer "
                                   "eingeben."))
            return True
        f()
        return True

    # ────────────────────────────────────────────────────────────────────
    #  Kapitel
    # ────────────────────────────────────────────────────────────────────

    def weiterlernen(self):
        kap = self.naechstes_kapitel()
        if kap is None:
            ausgeben("")
            ausgeben("  " + r.gruen(r.fett("🎉 Du hast alle Kapitel abgeschlossen!")))
            ausgeben("  " + r.grau("Ideal jetzt: Wiederholen (R), Fehlerkiste (F) oder die Prüfung (P)."))
            weiter()
            return
        while kap is not None:
            self.kapitel_spielen(kap)
            idx = self.engine.KAPITEL.index(kap)
            if idx + 1 >= len(self.engine.KAPITEL):
                break
            naechstes = self.engine.KAPITEL[idx + 1]
            ausgeben("")
            if not ja_nein(f"Weiter mit Kapitel {naechstes.nummer}: {naechstes.titel}?", standard=True):
                break
            kap = naechstes

    def kapitel_waehlen(self):
        ausgeben("")
        ausgeben(_eingerueckt(r.banner("📚 KAPITEL WÄHLEN", None, _w() - 2, farbe=r.blau)))
        for teil in self.engine.TEILE:
            kapitel = self.engine.kapitel_von_teil(teil["id"])
            if not kapitel:
                continue
            ausgeben("")
            ausgeben("  " + r.magenta(r.fett(teil["titel"])))
            if teil.get("untertitel"):
                ausgeben("  " + r.grau(teil["untertitel"]))
            for kap in kapitel:
                ausgeben(self.kapitel_zeile(kap))
                if kap.beschreibung:
                    ausgeben("         " + r.grau(r.abschneiden(kap.beschreibung, _w() - 10)))
        while True:
            a = eingabe("\n  Kapitelnummer (Enter = zurück): ").strip()
            if not a:
                return
            if a.isdigit() and 1 <= int(a) <= len(self.engine.KAPITEL):
                self.kapitel_spielen(self.engine.KAPITEL[int(a) - 1])
                return
            ausgeben("  " + r.grau(f"Bitte eine Zahl von 1 bis {len(self.engine.KAPITEL)} eingeben."))

    def kapitel_spielen(self, kap):
        status = self.fs.kapitel_status(self.daten, kap)
        d = kap.to_dict()
        anz = d.get("anzahl") or {}
        ausgeben("")
        info = [kap.beschreibung] if kap.beschreibung else []
        info.append(f"Quelle: {kap.quelle}   ·   {anz.get('erklaerungen', 0)} Erklärungen · "
                    f"{anz.get('ueben', 0)} Übungsfragen · {anz.get('programmieren', 0)} Programmieraufgaben")
        ausgeben(_eingerueckt(r.banner(f"KAPITEL {kap.nummer} · {kap.icon} {kap.titel}", info, _w() - 2)))
        if kap.lernziele:
            ziele = [r.grau("☐ ") + r.inline(z) for z in kap.lernziele]
            ausgeben("")
            ausgeben(_eingerueckt(r.kasten(ziele, _w() - 2, titel="🎯 Lernziele – am Ende kannst du …",
                                           farbe=r.cyan)))
        elemente = list(kap.elemente)
        if status["abgeschlossen"] or status["fragen_richtig"]:
            if status["abgeschlossen"]:
                ausgeben("  " + r.gruen(f"Du hast dieses Kapitel schon abgeschlossen (bestes Ergebnis "
                                        f"{status.get('best')}/{status.get('max')})."))
            else:
                ausgeben("  " + r.gelb(f"Du hast hier schon {status['fragen_richtig']} von "
                                       f"{status['fragen_gesamt']} Fragen richtig."))
            ausgeben("  " + r.fett("[Enter]") + r.grau(" komplett durcharbeiten   ") + r.fett("f")
                     + r.grau(" nur Fragen & Aufgaben   ") + r.fett("p") + r.grau(" nur Programmieren   ")
                     + r.fett("m") + r.grau(" nur Merkzettel"))
            while True:
                a = eingabe("  Deine Wahl: ").strip().lower()
                if a in ("", "f", "p", "m"):
                    break
                ausgeben("  " + r.grau("Bitte Enter, f, p oder m."))
            Frage = self.engine.Frage
            if a == "f":
                elemente = [e for e in elemente if isinstance(e, Frage)]
            elif a == "p":
                elemente = [e for e in elemente if isinstance(e, Frage) and e.phase == "programmieren"]
            elif a == "m":
                elemente = [e for e in elemente if e.typ == "zusammenfassung"]
                if not elemente:
                    ausgeben("  " + r.grau("Für dieses Kapitel gibt es (noch) keinen Merkzettel."))
                    return
                self.merkzettel_zeigen(kap)
                return
        else:
            weiter("[Enter] = los geht's   ·   'menü' = zurück zum Hauptmenü")

        fragen = [e for e in elemente if isinstance(e, self.engine.Frage)]
        gesamt = len(fragen)
        punkte, nr, xp_summe, falsche = 0, 0, 0, []
        besucht, aktuell = set(), None
        ctx = self.kontext()
        for e in elemente:
            phase = "merkzettel" if e.typ == "zusammenfassung" else e.phase
            leiste = None
            if phase != aktuell:
                if aktuell:
                    besucht.add(aktuell)
                aktuell = phase
                leiste = self.phasen_leiste(aktuell, besucht)
            if e.typ == "erklaerung":
                self.seiten_zeigen(e.titel, e.seiten(), icon="📖", phasen=leiste)
            elif e.typ == "zusammenfassung":
                if leiste:
                    ausgeben("")
                    ausgeben(leiste)
                self.merkzettel_zeigen(kap, e)
            elif isinstance(e, self.engine.Frage):
                if leiste:
                    ausgeben("")
                    ausgeben(leiste)
                nr += 1
                antwort = fr.stellen(e, nr, gesamt, ctx)
                xp_summe += antwort.xp
                if antwort.ok:
                    punkte += 1
                else:
                    falsche.append(e)
                self.abzeichen_feiern()
                ausgeben("")
                stand = r.grau(f"  Punkte: {punkte}/{nr}") + (r.gelb(f"   ·   +{xp_summe} XP in diesem Kapitel")
                                                               if xp_summe else "")
                ausgeben(stand)
                weiter("[Enter] = weiter   ·   'menü' = zurück zum Hauptmenü")
        if gesamt == 0:
            return
        self.kapitel_ergebnis(kap, punkte, gesamt, xp_summe, falsche)

    def merkzettel_zeigen(self, kap, element=None):
        text = element.text if element is not None else kap.zusammenfassung_text
        if not text:
            return
        self.seiten_zeigen(f"Merkzettel: {kap.titel}", self.markup.parse(text), icon="📝", farbe=r.gelb)

    def kapitel_ergebnis(self, kap, punkte, gesamt, xp_summe, falsche):
        res = self.fs.kapitel_abschliessen(self.daten, kap, punkte, gesamt)
        self.neue_abzeichen.extend(res.get("neue_abzeichen") or [])
        self.speichern()
        xp_summe += res.get("xp_neu", 0)
        quote = punkte / gesamt if gesamt else 0
        if quote >= 0.9:
            urteil = r.gruen("Hervorragend! Das Thema sitzt. 🎓")
        elif quote >= 0.7:
            urteil = r.gruen("Sehr ordentlich! Schau dir die falschen Fragen nochmal an.")
        elif quote >= 0.5:
            urteil = r.gelb("Gut auf dem Weg! Wiederhole das Kapitel ruhig noch einmal.")
        else:
            urteil = r.gelb("Nicht aufgeben – lies die Erklärungen nochmal in Ruhe und probier es erneut!")
        inhalt = [r.fett(f"{punkte} von {gesamt} Punkten ({quote:.0%})") + "   " + r.balken(punkte, gesamt, 24),
                  "", urteil, ""]
        inhalt.append(r.gelb(r.fett(f"+{xp_summe} XP")) + r.grau(" in diesem Kapitel")
                      + (r.grau(f" (davon {res.get('xp_neu')} für den Abschluss)") if res.get("xp_neu") else ""))
        if res.get("neuer_rekord"):
            inhalt.append(r.gruen("🏆 Neuer persönlicher Rekord für dieses Kapitel!"))
        lv = (self.statistik().get("level") or {})
        if lv:
            inhalt.append(r.grau("Dein Stand: ") + lv.get("titel", "") + r.grau(f" · {lv.get('xp', 0)} XP"))
        ausgeben("")
        ausgeben(_eingerueckt(r.kasten(inhalt, _w() - 2, titel=f"🏁 ERGEBNIS · Kapitel {kap.nummer}",
                                       farbe=r.magenta, stil="doppelt", innen_abstand=2)))
        self.abzeichen_feiern()
        if falsche:
            ausgeben("")
            if ja_nein(f"{len(falsche)} Frage(n) waren nicht richtig. Jetzt direkt wiederholen?", standard=True):
                p2, a2, _ = self.runde(falsche, "Wiederholung", zeige_kapitel=False)
                self.runden_ergebnis(p2, a2, "Wiederholung")
        weiter()

    # ────────────────────────────────────────────────────────────────────
    #  Training: Runde, Prüfung, Fehlerkiste, Wiederholen
    # ────────────────────────────────────────────────────────────────────

    def runde(self, fragen, titel, zeige_kapitel=True, ctx=None):
        ctx = ctx or self.kontext()
        punkte, falsche = 0, []
        xp = 0
        for nr, f in enumerate(fragen, 1):
            zusatz = None
            if zeige_kapitel and f.kapitel is not None:
                zusatz = f"{titel} · aus Kapitel {f.kapitel.nummer}: {f.kapitel.titel}"
            antwort = fr.stellen(f, nr, len(fragen), ctx, zusatz=zusatz)
            xp += antwort.xp
            if antwort.ok:
                punkte += 1
            else:
                falsche.append(f)
            self.abzeichen_feiern()
            ausgeben("")
            ausgeben(r.grau(f"  Punkte: {punkte}/{nr}") + (r.gelb(f"   ·   +{xp} XP") if xp else ""))
            weiter("[Enter] = weiter   ·   'menü' = abbrechen")
        return punkte, len(fragen), falsche

    def runden_ergebnis(self, punkte, anzahl, titel, zusatz=None):
        quote = punkte / anzahl if anzahl else 0
        inhalt = [r.fett(f"{punkte} von {anzahl} richtig ({quote:.0%})") + "   " + r.balken(punkte, anzahl, 24)]
        if zusatz:
            inhalt.extend(zusatz)
        ausgeben("")
        ausgeben(_eingerueckt(r.kasten(inhalt, _w() - 2, titel=f"🏁 {titel}", farbe=r.magenta, stil="doppelt",
                                       innen_abstand=2)))

    def pruefung(self):
        # wie in der grafischen Oberfläche: Fragen aus Tag 1 bis 4 (ohne Challenge/Bonus)
        alle = [f for f in self.engine.alle_fragen().values() if f.typ != "code"]
        pool = [f for f in alle if f.kapitel is not None and f.kapitel.teil in ("tag1", "tag2", "tag3", "tag4")]
        if len(pool) < 30:
            pool = alle
        anzahl = min(30, len(pool))
        ausgeben("")
        ausgeben(_eingerueckt(r.banner("🎓 PROBEPRÜFUNG", [
            f"{anzahl} zufällige Fragen aus Tag 1 bis 4 – ohne Erklärungen vorher.",
            "Wie in einer echten Prüfung: nur EIN Versuch pro Frage und keine Tipps.",
            "Abbrechen mit 'menü' oder Strg+C (dann gibt es keine Note)."], _w() - 2)))
        if not pool:
            ausgeben("  " + r.grau("Es gibt noch keine Fragen."))
            return
        weiter("[Enter] = Prüfung starten   ·   'menü' = zurück")
        auswahl = random.sample(pool, anzahl)
        punkte, anzahl, falsche = self.runde(auswahl, "Prüfung", ctx=self.kontext(pruefungsmodus=True))
        res = self.fs.pruefung_verbuchen(self.daten, punkte, anzahl)
        self.neue_abzeichen.extend(res.get("neue_abzeichen") or [])
        self.speichern()
        note = res.get("note", "?")
        zusatz = ["", r.fett("Deine (inoffizielle) Note: ") + (r.gruen if note <= "4,0" else r.rot)(r.fett(note))]
        if falsche:
            kap_fehler = {}
            for f in falsche:
                if f.kapitel is not None:
                    kap_fehler.setdefault(f.kapitel, 0)
                    kap_fehler[f.kapitel] += 1
            if kap_fehler:
                zusatz.append("")
                zusatz.append(r.grau("Schau dir diese Kapitel nochmal an:"))
                for kap, n in sorted(kap_fehler.items(), key=lambda x: -x[1])[:6]:
                    zusatz.append(f"  {kap.nummer:>2} {kap.icon} {kap.titel}" + r.grau(f"  ({n} Fehler)"))
            zusatz.append(r.grau("Die falschen Fragen liegen jetzt in deiner Fehlerkiste (F)."))
        self.runden_ergebnis(punkte, anzahl, "PRÜFUNGSERGEBNIS", zusatz)
        self.abzeichen_feiern()
        weiter()

    def fehlerkiste(self):
        alle = self.engine.alle_fragen()
        ids = [i for i in self.daten.get("fehlerkiste", []) if i in alle]
        ausgeben("")
        if not ids:
            ausgeben("  " + r.gruen("📦 Deine Fehlerkiste ist leer – super!"))
            ausgeben("  " + r.grau("Falsch beantwortete Fragen landen automatisch hier."))
            weiter()
            return
        ausgeben(_eingerueckt(r.banner(f"📦 FEHLERKISTE · {len(ids)} Frage(n)", [
            "Hier liegen Fragen, die du noch nicht richtig hattest.",
            "Richtig beantwortet? Dann fliegen sie raus – wie bei Karteikarten."], _w() - 2, farbe=r.gelb)))
        anzahl = len(ids)
        if anzahl > 15:
            a = eingabe(f"  Wie viele Fragen jetzt? (Enter = 15, max. {anzahl}): ").strip()
            anzahl = int(a) if a.isdigit() and 0 < int(a) <= len(ids) else 15
        else:
            weiter("[Enter] = los")
        auswahl = [alle[i] for i in ids]
        random.shuffle(auswahl)
        punkte, n, _ = self.runde(auswahl[:anzahl], "Fehlerkiste")
        rest = len([i for i in self.daten.get("fehlerkiste", []) if i in alle])
        self.runden_ergebnis(punkte, n, "FEHLERKISTE", ["", r.grau(f"Noch {rest} Frage(n) in der Kiste.")])
        self.abzeichen_feiern()
        weiter()

    def wiederholen(self):
        alle = self.engine.alle_fragen()
        ids = [i for i in self.fs.faellige_fragen(self.daten, 10) if i in alle]
        ausgeben("")
        if not ids:
            ausgeben("  " + r.grau("🔁 Noch nichts zu wiederholen – bearbeite zuerst ein paar Kapitel."))
            weiter()
            return
        ausgeben(_eingerueckt(r.banner("🔁 WIEDERHOLEN (Lernkartei)", [
            f"{len(ids)} Fragen aus deiner Lernkartei – fällige und schwierige zuerst.",
            "Jede richtige Antwort wandert ein Fach weiter und kommt später wieder dran."], _w() - 2,
            farbe=r.cyan)))
        weiter("[Enter] = los")
        punkte, n, _ = self.runde([alle[i] for i in ids], "Wiederholen")
        self.runden_ergebnis(punkte, n, "WIEDERHOLEN")
        self.abzeichen_feiern()
        weiter()

    # ────────────────────────────────────────────────────────────────────
    #  Spickzettel, Spielwiese, Statistik, Hilfe, Zurücksetzen
    # ────────────────────────────────────────────────────────────────────

    def spickzettel(self):
        while True:
            ausgeben("")
            ausgeben(_eingerueckt(r.banner("📋 SPICKZETTEL", [
                "G = gesamter Spickzettel (alles Wichtige auf einen Blick)",
                "Kapitelnummer = Merkzettel dieses Kapitels"], _w() - 2, farbe=r.gelb)))
            mit = [kap for kap in self.engine.KAPITEL if kap.zusammenfassung_text]
            if mit:
                zeilen = [f"{kap.nummer:>2} {kap.icon} {kap.titel}" for kap in mit]
                ausgeben(_eingerueckt([r.grau("Merkzettel gibt es für:")] + zeilen))
            else:
                ausgeben("  " + r.grau("(Merkzettel pro Kapitel gibt es noch keine.)"))
            a = eingabe("\n  Deine Wahl (Enter = zurück): ").strip().lower()
            if not a:
                return
            if a == "g":
                text = getattr(self.inhalte, "SPICKZETTEL", "") or ""
                self.seiten_zeigen("Spickzettel", self.markup.parse(text), icon="📋", farbe=r.gelb)
            elif a.isdigit() and 1 <= int(a) <= len(self.engine.KAPITEL):
                kap = self.engine.KAPITEL[int(a) - 1]
                if kap.zusammenfassung_text:
                    self.merkzettel_zeigen(kap)
                else:
                    ausgeben("  " + r.grau("Für dieses Kapitel gibt es (noch) keinen Merkzettel."))
            else:
                ausgeben("  " + r.grau("Bitte G oder eine Kapitelnummer eingeben."))

    def spielwiese(self):
        ausgeben("")
        ausgeben(_eingerueckt(r.banner("🛝 SPIELWIESE – probier Python aus!", [
            "Schreib eigenen Code, führe ihn aus oder schau zu, wie Python ihn Schritt für Schritt abarbeitet.",
            "Tipp: Mit b1–b4 lädst du ein fertiges Beispiel."], _w() - 2, farbe=r.cyan)))
        code_zeilen, eingaben = [], []
        while True:
            if code_zeilen:
                ausgeben("")
                ausgeben(_eingerueckt(r.code_kasten("\n".join(code_zeilen), _w() - 2, titel="Dein Code")))
                if eingaben:
                    ausgeben("  " + r.grau("Eingaben für input(): ") + ", ".join(r.cyan(e) for e in eingaben))
            ausgeben("")
            optionen = []
            if code_zeilen:
                optionen += [("a", "ausführen"), ("s", "Schritt für Schritt"), ("b", "bearbeiten"),
                             ("n", "neuer Code"), ("e", "Eingaben für input()")]
            else:
                optionen += [("c", "Code schreiben")]
            optionen += [("b1–b4", "Beispiel laden"), ("Enter", "zurück zum Hauptmenü")]
            ausgeben(r.teile_umbrechen([r.fett(b) + r.grau(" " + t) for b, t in optionen], _w(), "   "))
            ausgeben(r.teile_umbrechen([r.grau(f"b{i}: {titel}") for i, (titel, _, _) in enumerate(BEISPIELE, 1)],
                                       _w(), r.grau(" · "), einzug="     "))
            a = eingabe("  Deine Wahl: ").strip().lower()
            if a == "":
                return
            if a in ("c", "n") or (a == "b" and not code_zeilen):
                aktion, neu = fr.code_editor([])
                if aktion in ("pruefen", "datei"):
                    code_zeilen = neu
                    eingaben = []
                    if aktion == "datei" or code_zeilen:
                        self._spielwiese_laufen(code_zeilen, eingaben)
                elif aktion == "tipp":
                    ausgeben("  " + r.grau("In der Spielwiese gibt es keine Tipps – probier einfach aus!"))
                continue
            if a == "b" and code_zeilen:
                aktion, neu = fr.code_editor(code_zeilen)
                if aktion in ("pruefen", "datei"):
                    code_zeilen = neu
                    self._spielwiese_laufen(code_zeilen, eingaben)
                continue
            if a.startswith("b") and a[1:].isdigit():
                i = int(a[1:])
                if 1 <= i <= len(BEISPIELE):
                    _, code, eing = BEISPIELE[i - 1]
                    code_zeilen = code.split("\n")
                    eingaben = list(eing)
                    continue
            if a == "a" and code_zeilen:
                self._spielwiese_laufen(code_zeilen, eingaben)
                continue
            if a == "s" and code_zeilen:
                self.trace_ansehen("\n".join(code_zeilen), eingaben)
                continue
            if a == "e" and code_zeilen:
                ausgeben("  " + r.grau("Gib die Eingaben für input() mit | getrennt ein, z. B.: Anna|19"))
                t = eingabe("  Eingaben: ")
                eingaben = [x.strip() for x in t.split("|")] if t.strip() else []
                continue
            ausgeben("  " + r.grau("Das habe ich nicht verstanden."))

    def _spielwiese_laufen(self, code_zeilen, eingaben):
        code = "\n".join(code_zeilen)
        if "input(" in code and not eingaben:
            ausgeben(["  " + z for z in r.umbrechen("Dein Code benutzt input(). Gib die Eingaben mit | "
                                                    "getrennt ein (z. B. Anna|19), Enter = keine:",
                                                    _w() - 4, basis=r.gelb)])
            t = eingabe("  Eingaben: ")
            eingaben[:] = [x.strip() for x in t.split("|")] if t.strip() else []
        ausgeben("  " + r.grau("▶ Programm läuft …"))
        erg = self.sandbox.ausfuehren(code, list(eingaben))
        ausgeben(_eingerueckt(r.ausgabe_kasten(erg, _w() - 2, titel="Ausgabe", eingaben=eingaben)))

    def abzeichen_statistik(self):
        st = self.statistik()
        lv = st.get("level") or {}
        ausgeben("")
        ausgeben(_eingerueckt(r.banner("🏅 ABZEICHEN & STATISTIK", None, _w() - 2, farbe=r.gelb)))
        xp = st.get("xp", 0)
        inhalt = [r.gelb(r.fett("⭐ " + lv.get("titel", "")))]
        if lv.get("xp_naechstes"):
            fehlt = lv["xp_naechstes"] - xp
            inhalt.append(r.balken(xp - lv["xp_start"], lv["xp_naechstes"] - lv["xp_start"], 30, farbig=False)
                          + f"  {xp} / {lv['xp_naechstes']} XP" + r.grau(f"  (noch {fehlt} XP bis Level "
                                                                      f"{lv['nummer'] + 1})"))
        else:
            inhalt.append(r.gelb(f"{xp} XP – höchstes Level erreicht!"))
        serie = st.get("serie") or {}
        inhalt.append(f"🔥 Serie: {r.fett(str(serie.get('tage', 0)))} Tag(e) in Folge"
                      + (r.grau(f" (zuletzt geübt: {serie.get('zuletzt')})") if serie.get("zuletzt") else ""))
        ausgeben(_eingerueckt(r.kasten(inhalt, _w() - 2, titel="Dein Level", farbe=r.gelb)))
        zahlen = [
            ["Kapitel abgeschlossen", f"{st.get('kapitel_abgeschlossen', 0)} / {st.get('kapitel_gesamt', 0)}"],
            ["Fragen richtig beantwortet", f"{st.get('fragen_richtig', 0)} / {st.get('fragen_gesamt', 0)}"],
            ["Programmieraufgaben gelöst", f"{st.get('code_geloest', 0)} / {st.get('code_gesamt', 0)}"],
            ["Fragen in der Fehlerkiste", str(st.get("fehlerkiste", 0))],
            ["Fragen zum Wiederholen fällig", str(st.get("faellig", 0))],
            ["Probeprüfungen", str(st.get("pruefungen", 0))
             + (f" (beste Note {st['beste_note']})" if st.get("beste_note") else "")],
        ]
        ausgeben("")
        ausgeben(_eingerueckt(r.tabelle(["Statistik", "Stand"], zahlen, _w() - 2)))
        teile = st.get("teile") or []
        if teile:
            ausgeben("")
            ausgeben("  " + r.fett("Fortschritt je Teil"))
            breite_titel = max(r.sichtbreite(t["titel"]) for t in teile)
            breite_titel = min(breite_titel, _w() - 40)
            for t in teile:
                ausgeben("  " + r.pad(r.abschneiden(t["titel"], breite_titel), breite_titel) + "  "
                         + r.balken(t["fragen_richtig"], t["fragen_gesamt"], 16)
                         + r.grau(f" {t['fragen_richtig']}/{t['fragen_gesamt']} Fragen · "
                                  f"{t['kapitel_abgeschlossen']}/{t['kapitel_gesamt']} Kapitel"))
        pruefungen = self.daten.get("pruefungen") or []
        if pruefungen:
            ausgeben("")
            ausgeben("  " + r.fett("Letzte Probeprüfungen"))
            for p in pruefungen[-5:]:
                ausgeben("  " + r.grau(str(p.get("datum") or "früher")) + f"  {p.get('punkte')}/{p.get('max')}"
                         + "  Note " + r.fett(str(p.get("note"))))
        alle = st.get("abzeichen_alle") or []
        if alle:
            erreicht = [a for a in alle if a.get("erreicht")]
            ausgeben("")
            ausgeben("  " + r.fett(f"Abzeichen ({len(erreicht)}/{len(alle)})"))
            for a in alle:
                if a.get("erreicht"):
                    ausgeben("  " + f"{a.get('icon', '🏅')} " + r.gelb(r.fett(a["titel"])) + r.grau(" – ")
                             + a.get("beschreibung", ""))
                else:
                    ausgeben("  " + r.grau(f"🔒 {a['titel']} – {a.get('beschreibung', '')}"))
        weiter()

    def hilfe(self, erster_start=False):
        text = r"""
        ## So funktioniert das Lernquiz

        Jedes Kapitel folgt dem Lernpfad **Verstehen ▸ Üben ▸ Programmieren ▸ Merkzettel**:
        erst eine Erklärung (lies sie in Ruhe!), dann Verständnisfragen, dann echte
        Programmieraufgaben, die automatisch getestet werden.

        | Eingabe | Bedeutung |
        |---|---|
        | `?` | Tipp anzeigen (bei Programmieraufgaben: der nächste, genauere Tipp) |
        | `x` | „weiß ich nicht“ – zeigt die Lösung |
        | `menü` oder Strg+C | zurück zum Hauptmenü (dein Fortschritt bleibt gespeichert) |
        | `z` | auf Erklärungsseiten: eine Seite zurück |
        | `s` | Beispielcode Schritt für Schritt ansehen |

        ## Programmieraufgaben

        • Tippe deinen Code Zeile für Zeile, einrücken mit 4 Leerzeichen. Mit **ENDE** wird geprüft.
        • Längerer Code? Speichere ihn in einer Datei und tippe `DATEI meinpfad.py`.
        • `V` übernimmt die Vorlage, `ÄNDERN 3` schreibt Zeile 3 neu, `ZEIGEN` zeigt deinen Code.
        • `LÖSUNG` zeigt die Musterlösung, `SKIP` überspringt die Aufgabe.
        • Dein letzter Stand wird als Entwurf gespeichert (`E` lädt ihn wieder).

        ## Punkte & Wiederholung

        • Richtige Antworten bringen **XP** (1. Versuch +10, 2. Versuch +5, Code +30, Kapitel +50).
        • Falsche Fragen landen in der **Fehlerkiste**; **Wiederholen** fragt nach der Lernkartei-Methode ab.
        • Die **Spielwiese** ist dein Python-Sandkasten mit Schritt-für-Schritt-Ansicht.

        !! Empfehlung: Kapitel der Reihe nach mit „Weiterlernen“ (W) – und jeden Code auch selbst ausprobieren!
        """
        if erster_start:
            ausgeben("")
            ausgeben("  " + r.gelb(r.fett("Willkommen! Kurz erklärt, wie alles funktioniert:")))
        seiten = self.markup.parse(textwrap.dedent(text))
        self.seiten_zeigen("Hilfe", seiten, icon="❓", farbe=r.blau)

    def zuruecksetzen(self):
        ausgeben("")
        ausgeben("  " + r.rot(r.fett("⚠ Damit werden ALLE Punkte, XP, Abzeichen, Entwürfe und die Fehlerkiste gelöscht.")))
        a = eingabe("  Wirklich alles zurücksetzen? Tippe 'ja' zum Bestätigen: ").strip().lower()
        if a == "ja":
            self.fs.zuruecksetzen(self.daten)
            self.speichern()
            ausgeben("  " + r.gruen("Fortschritt zurückgesetzt. Viel Spaß beim Neustart!"))
        else:
            ausgeben("  " + r.grau("Nichts gelöscht."))


def main(farben=True):
    """Startet die Terminal-Oberfläche. Rückgabe: Exit-Code."""
    k.vorbereiten(farben)
    try:
        from .. import engine, fortschritt, markup, sandbox
        from .. import inhalte
    except Exception as e:  # pragma: no cover - nur wenn Dateien fehlen
        ausgeben(r.rot(f"Das Programm konnte nicht geladen werden: {type(e).__name__}: {e}"))
        return 1
    app = App(engine, markup, sandbox, fortschritt, inhalte)
    try:
        app.starten()
    except (ProgrammEnde, KeyboardInterrupt):
        app.abschied()
    except ZurueckZumMenue:  # pragma: no cover
        app.abschied()
    return 0


if __name__ == "__main__":
    sys.exit(main("--keine-farben" not in sys.argv))
