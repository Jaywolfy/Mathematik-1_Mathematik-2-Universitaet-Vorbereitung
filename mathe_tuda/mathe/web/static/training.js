// Training: Wiederholen (Leitner), Fehlerkiste, Thema endlos üben, Probeklausur, Diagnosetest.
import { h, inline, nurText, lade, ring, konfetti, toast, plural, lokal } from "./util.js";
import { api } from "./api.js";
import { setStatistik, store } from "./store.js";
import { frageKarte } from "./fragen.js";
import { uebersichtLaden, alleKapitel } from "./app.js";

const MODI = {
  wiederholen: { icon: "🔁", titel: "Wiederholen", text: "Karteikasten-Prinzip: Aufgaben, die dir schwerfallen, kommen öfter dran – sichere seltener." },
  fehlerkiste: { icon: "🧰", titel: "Fehlerkiste", text: "Hier sammeln sich Aufgaben, die noch nicht geklappt haben. Löst du sie richtig, sind sie raus." },
  thema: { icon: "⚙️", titel: "Endlos üben", text: "Immer neue Aufgaben mit neuen Zahlen – so oft du willst." },
  klausur: { icon: "🎓", titel: "Probeklausur", text: "Aufgaben wie in der echten Klausur: Rechnen, Mehrfachauswahl und Beweise auf Papier. Mit Zeitlimit, Punkten und Note. Feedback gibt es erst am Ende." },
};
const MODULE = [["mathe1", "Mathe 1"], ["mathe2", "Mathe 2"], ["vorkurs", "Vorkurs"], ["fundament", "Fundament (Schulstoff)"]];

export async function trainingAnsicht(main, modus, extra) {
  const m = MODI[modus];
  if (!m) { main.replaceChildren(h("div", { class: "container fehler-karte", text: "Unbekannter Trainingsmodus." })); return null; }
  document.title = `${m.titel} · Mathe für Informatik`;
  let timer = null;
  const aufraeumen = () => { if (timer) clearInterval(timer); timer = null; };

  if (modus === "klausur") {
    const vorhanden = new Set((store.uebersicht?.teile || []).map(t => t.id));
    const modulSel = h("select", { class: "feld schmal-feld", "aria-label": "Modul" }, MODULE.filter(([id]) => vorhanden.has(id)).map(([id, name]) => h("option", { value: id, text: name })));
    const anzahlSel = h("select", { class: "feld schmal-feld", "aria-label": "Anzahl der Aufgaben" }, [6, 10, 15].map(n => h("option", { value: n, text: `${n} Aufgaben`, selected: n === 10 })));
    const timerCb = h("input", { type: "checkbox", checked: lokal.get("klausur_timer", true) || undefined });
    const start = h("button", { class: "btn btn-primary btn-lg", type: "button", text: "Klausur starten →" });
    const s = store.statistik || {};
    main.replaceChildren(h("div", { class: "container schmal" }, h("div", { class: "karte training-intro" },
      h("span", { class: "gross", "aria-hidden": "true", text: m.icon }), h("h1", { text: m.titel }), h("p", { text: m.text }),
      h("div", { class: "training-optionen" }, modulSel, anzahlSel, h("label", { class: "schalter" }, timerCb, h("span", { text: "⏱ Mit Zeitlimit (3 Min. pro Punkt)" }))),
      s.besteNote ? h("p", { style: { marginTop: "10px" }, html: `Deine beste Note bisher: <b>${s.besteNote}</b>` }) : null,
      h("div", { style: { marginTop: "18px" } }, start))));
    start.onclick = async () => {
      lokal.set("klausur_timer", timerCb.checked);
      main.replaceChildren(lade("Aufgaben werden zusammengestellt …"));
      const r = await api.get(`/api/training?modus=klausur&modul=${modulSel.value}&anzahl=${anzahlSel.value}`);
      if (!r.fragen.length) { main.replaceChildren(h("div", { class: "container leer-hinweis", text: "Für dieses Modul gibt es noch keine Aufgaben." })); return; }
      const punkte = r.fragen.reduce((a, f) => a + (f.punkte || 1), 0);
      runde(r.fragen, { sekunden: timerCb.checked ? punkte * 180 : null, klausur: true, modul: modulSel.value });
    };
    return aufraeumen;
  }

  main.replaceChildren(lade());
  const url = modus === "thema" ? `/api/training?modus=thema&kapitel=${encodeURIComponent(extra || "")}&anzahl=10` : `/api/training?modus=${modus}`;
  const r = await api.get(url);
  if (!r.fragen.length) {
    main.replaceChildren(h("div", { class: "container schmal" }, h("div", { class: "karte training-intro" },
      h("span", { class: "gross", "aria-hidden": "true", text: modus === "fehlerkiste" ? "🧹" : "🌱" }),
      h("h1", { text: modus === "fehlerkiste" ? "Deine Fehlerkiste ist leer!" : "Noch nichts zu wiederholen" }),
      h("p", { text: modus === "fehlerkiste" ? "Super – gerade gibt es keine offenen Aufgaben. Weiter so!" : "Bearbeite zuerst ein paar Aufgaben in den Kapiteln. Dann tauchen sie hier zum Auffrischen auf." }),
      h("div", { style: { marginTop: "18px" } }, h("a", { class: "btn btn-primary", href: "#/", text: "Zur Übersicht" })))));
    return aufraeumen;
  }
  const kap = modus === "thema" ? alleKapitel().find(k => k.slug === extra) : null;
  runde(r.fragen, { endlos: modus === "thema", titel: kap ? `Endlos üben: ${nurText(kap.titel)}` : m.titel });
  return aufraeumen;

  /* ---------- Fragerunde ---------- */
  function runde(fragen, { sekunden = null, klausur = false, modul = null, endlos = false, titel = m.titel } = {}) {
    const ergebnisse = [];       // {ok, teilpunkte, punkte, karte}
    let i = 0;
    const t0 = Date.now();
    const fortschritt = h("div", { class: "balken" }, h("i"));
    const zaehler = h("span", { class: "chip" });
    const uhr = h("span", { class: "timer", hidden: !sekunden, role: "timer", "aria-label": "Verbleibende Zeit" });
    const buehne = h("div", { class: klausur ? "klausur-modus" : "" });
    const bSkip = h("button", { class: "btn btn-ghost", type: "button", text: klausur ? "Auslassen" : "Überspringen" });
    const bWeiter = h("button", { class: "btn btn-primary btn-lg", type: "button", text: "Weiter →", disabled: true });
    const bAbbruch = h("button", { class: "btn btn-sm btn-ghost", type: "button", text: endlos ? "Fertig" : "Beenden" });
    main.replaceChildren(h("div", { class: "container" },
      h("div", { class: "runde-kopf" }, h("span", { class: "runde-icon", "aria-hidden": "true", text: m.icon }), h("h1", { text: titel }), zaehler, endlos ? null : fortschritt, uhr, bAbbruch),
      buehne, h("div", { class: "kap-nav" }, h("span", { class: "mitte" }), bSkip, bWeiter)));
    if (sekunden) {
      let rest = sekunden;
      const malen = () => { uhr.textContent = `⏱ ${Math.floor(rest / 60)}:${String(rest % 60).padStart(2, "0")}`; uhr.classList.toggle("knapp", rest <= 120); };
      malen();
      timer = setInterval(() => {
        rest--; malen();
        if (rest <= 0) { clearInterval(timer); timer = null; toast("⏱ Die Zeit ist um!"); fertig(); }
        if (!uhr.isConnected) { clearInterval(timer); timer = null; }
      }, 1000);
    }
    const tasten = (e) => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey) && !bWeiter.disabled) { e.preventDefault(); bWeiter.click(); } };
    document.addEventListener("keydown", tasten);

    async function zeigen() {
      if (endlos && i >= fragen.length - 2) {
        try { const mehr = await api.get(`/api/training?modus=thema&kapitel=${encodeURIComponent(extra)}&anzahl=10`); fragen.push(...mehr.fragen); } catch { /* egal */ }
      }
      const f = fragen[i];
      const richtig = ergebnisse.filter(e => e.ok).length;
      zaehler.textContent = endlos ? `${richtig} von ${ergebnisse.length} richtig` : `Aufgabe ${i + 1} / ${fragen.length}`;
      fortschritt.querySelector("i").style.width = `${(i / fragen.length) * 100}%`;
      const karte = frageKarte(f, {
        klausur,
        kontext: f.kapitel_titel ? `${f.kapitel_icon || ""} ${nurText(f.kapitel_titel)}`.trim() : null,
        onFertig: (info) => {
          ergebnisse[i] = { ok: !!info.ok, teilpunkte: info.ok ? 1 : (info.teilpunkte || 0), punkte: f.punkte || 1, karte };
          bWeiter.disabled = false; bSkip.hidden = true;
          if (klausur) setTimeout(() => bWeiter.click(), 250);
          else if (info.ok) setTimeout(() => bWeiter.focus({ preventScroll: true }), 50);
        },
      });
      buehne.replaceChildren(h("div", { class: "schritt-buehne" }, karte.el));
      bWeiter.disabled = true; bSkip.hidden = false;
      bWeiter.textContent = !endlos && i === fragen.length - 1 ? "Auswerten ✓" : "Weiter →";
      window.scrollTo({ top: 0 });
      setTimeout(() => karte.fokus && karte.fokus(), 300);
    }
    bWeiter.onclick = () => { if (endlos || i < fragen.length - 1) { i++; zeigen(); } else fertig(); };
    bSkip.onclick = () => { ergebnisse[i] = { ok: false, teilpunkte: 0, punkte: fragen[i].punkte || 1, uebersprungen: true }; bWeiter.disabled = false; bWeiter.click(); };
    bAbbruch.onclick = () => fertig();
    zeigen();

    async function fertig() {
      document.removeEventListener("keydown", tasten);
      if (timer) { clearInterval(timer); timer = null; }
      const gezaehlt = endlos ? ergebnisse.filter(Boolean) : fragen.map((f, k) => ergebnisse[k] || { ok: false, teilpunkte: 0, punkte: f.punkte || 1, uebersprungen: true });
      const max = gezaehlt.reduce((a, e) => a + e.punkte, 0);
      const punkte = Math.round(gezaehlt.reduce((a, e) => a + e.punkte * e.teilpunkte, 0) * 2) / 2;
      const pct = max ? punkte / max : 0;
      let note = null, neueAbzeichen = [];
      if (klausur) {
        try {
          const r = await api.post("/api/klausur/ergebnis", { modul, punkte, max, dauer: Math.round((Date.now() - t0) / 1000) });
          note = r.note; neueAbzeichen = r.neue_abzeichen || []; setStatistik(r.statistik);
        } catch (e) { toast(e.message, "rot"); }
      }
      const karte = h("div", { class: "karte ergebnis-karte" },
        note ? h("div", null, h("div", { class: "note-gross", text: note }), h("p", { class: "unter", text: "Deine Note" }))
          : h("div", { class: "ergebnis-ring" }, ring(pct, { groesse: 120, dicke: 10, text: `${Math.round(pct * 100)}%` })),
        h("h2", { text: pct >= 0.8 ? "Sehr stark! 🎉" : pct >= 0.5 ? "Gut gemacht! 👍" : "Dranbleiben – jede Aufgabe macht dich sicherer! 🌱" }),
        h("div", { class: "ergebnis-zahlen" },
          h("div", { class: "ez" }, h("b", { text: klausur ? `${String(punkte).replace(".", ",")} / ${max}` : `${gezaehlt.filter(e => e.ok).length} / ${gezaehlt.length}` }), h("span", { text: klausur ? "Punkte" : "richtig" })),
          h("div", { class: "ez" }, h("b", { text: String(gezaehlt.filter(e => !e.ok && !e.uebersprungen).length) }), h("span", { text: "noch nicht richtig" })),
          h("div", { class: "ez" }, h("b", { text: String(gezaehlt.filter(e => e.uebersprungen).length) }), h("span", { text: "ausgelassen" }))),
        neueAbzeichen.length ? h("div", { class: "neue-abzeichen" }, neueAbzeichen.map(a => h("div", { class: "abzeichen" }, h("span", { class: "az-icon", text: a.icon }), h("b", { text: a.titel }), h("span", { text: a.beschreibung || "" })))) : null,
        h("div", { class: "ergebnis-aktionen" },
          h("button", { class: "btn btn-primary btn-lg", type: "button", text: klausur ? "Neue Klausur" : endlos ? "Weiter üben" : "Nochmal", onclick: () => trainingAnsicht(main, modus, extra) }),
          (store.statistik?.fehlerkiste || 0) > 0 && modus !== "fehlerkiste" ? h("a", { class: "btn btn-lg", href: "#/training/fehlerkiste", text: `🧰 Fehlerkiste (${store.statistik.fehlerkiste})` }) : null,
          h("a", { class: "btn btn-ghost btn-lg", href: "#/", text: "Zur Übersicht" })));
      const inhalt = h("div", { class: "container schmal" }, karte);
      if (klausur) {
        const review = h("div", { class: "klausur-review" }, h("h2", { class: "abschnitt-titel", text: "Deine Aufgaben mit Lösungen" }),
          gezaehlt.map((e, k) => e.karte ? h("div", { class: "review-eintrag" }, h("div", { class: "review-kopf" }, h("b", { text: `Aufgabe ${k + 1}` }), h("span", { class: "chip " + (e.ok ? "gruen" : "gelb"), text: `${String(Math.round(e.punkte * e.teilpunkte * 2) / 2).replace(".", ",")} / ${e.punkte} P.` })), e.karte.el) : null));
        inhalt.append(review);
      }
      main.replaceChildren(inhalt);
      if (pct >= 0.8 || neueAbzeichen.length) konfetti();
      uebersichtLaden().catch(() => {});
    }
  }
}

/* ---------- Diagnosetest ---------- */
export async function diagnoseAnsicht(main) {
  document.title = "Diagnosetest · Mathe für Informatik";
  const letzte = store.statistik?.diagnose;
  const start = h("button", { class: "btn btn-primary btn-lg", type: "button", text: letzte ? "Diagnosetest wiederholen →" : "Diagnosetest starten →" });
  main.replaceChildren(h("div", { class: "container schmal" }, h("div", { class: "karte training-intro" },
    h("span", { class: "gross", "aria-hidden": "true", text: "🧭" }), h("h1", { text: "Diagnosetest" }),
    h("p", { text: "25 gemischte Aufgaben aus dem Schulstoff. Keine Note, kein Druck: Wenn du etwas nicht weißt, überspring es einfach. Am Ende siehst du, welche Themen schon sitzen und wo du am besten einsteigst." }),
    letzte ? h("p", { class: "antwort-hinweis", style: { justifyContent: "center" }, html: `Letzter Test am ${letzte.datum}: Empfehlung <b>${letzte.empfehlung || "–"}</b>` }) : null,
    h("div", { style: { marginTop: "18px" } }, start))));
  start.onclick = async () => {
    main.replaceChildren(lade("Aufgaben werden zusammengestellt …"));
    const r = await api.get("/api/diagnose");
    if (!r.fragen.length) { main.replaceChildren(h("div", { class: "container leer-hinweis", text: "Noch keine Fundament-Kapitel vorhanden." })); return; }
    const stand = {};
    let i = 0;
    const zaehler = h("span", { class: "chip" });
    const balkenEl = h("div", { class: "balken" }, h("i"));
    const buehne = h("div");
    const bSkip = h("button", { class: "btn btn-ghost", type: "button", text: "Weiß ich nicht – überspringen" });
    const bWeiter = h("button", { class: "btn btn-primary btn-lg", type: "button", text: "Weiter →", disabled: true });
    main.replaceChildren(h("div", { class: "container" },
      h("div", { class: "runde-kopf" }, h("span", { class: "runde-icon", text: "🧭" }), h("h1", { text: "Diagnosetest" }), zaehler, balkenEl),
      buehne, h("div", { class: "kap-nav" }, h("span", { class: "mitte" }), bSkip, bWeiter)));
    const zaehlen = (f, ok) => { const s = f.kapitel; stand[s] = stand[s] || [0, 0]; stand[s][1]++; if (ok) stand[s][0]++; };
    const zeigen = () => {
      const f = r.fragen[i];
      zaehler.textContent = `Aufgabe ${i + 1} / ${r.fragen.length}`;
      balkenEl.querySelector("i").style.width = `${i / r.fragen.length * 100}%`;
      const karte = frageKarte(f, { klausur: true, kontext: f.kapitel_titel ? nurText(f.kapitel_titel) : null, onFertig: (info) => { zaehlen(f, info.ok); setTimeout(weiter, 200); } });
      buehne.replaceChildren(h("div", { class: "schritt-buehne klausur-modus" }, karte.el));
      setTimeout(() => karte.fokus && karte.fokus(), 300);
    };
    const weiter = () => { i++; if (i < r.fragen.length) zeigen(); else auswerten(); };
    bSkip.onclick = () => { zaehlen(r.fragen[i], false); weiter(); };
    zeigen();
    async function auswerten() {
      const a = await api.post("/api/diagnose/ergebnis", { ergebnisse: stand });
      setStatistik(a.statistik);
      const zeilen = Object.entries(a.kapitel).filter(([, e]) => e.gesamt).map(([slug, e]) => h("a", { class: "diag-zeile" + (e.luecke ? " luecke" : ""), href: `#/kapitel/${slug}` },
        h("span", { class: "diag-titel", html: inline(e.titel) }), h("span", { class: "diag-wert", text: `${e.richtig} / ${e.gesamt}` }),
        h("span", { class: "chip " + (e.luecke ? "gelb" : "gruen"), text: e.luecke ? "üben" : "sitzt" })));
      main.replaceChildren(h("div", { class: "container schmal" }, h("div", { class: "karte ergebnis-karte" },
        h("span", { class: "gross", style: { fontSize: "54px" }, text: "🧭" }), h("h2", { text: "Deine Auswertung" }),
        a.empfehlung ? h("p", { class: "unter", html: `Empfehlung: Starte mit <b>${inline(a.empfehlung_titel)}</b>.` }) : null,
        h("div", { class: "diag-liste" }, zeilen),
        h("div", { class: "ergebnis-aktionen" },
          a.empfehlung ? h("a", { class: "btn btn-primary btn-lg", href: `#/kapitel/${a.empfehlung}`, text: "Zum empfohlenen Kapitel →" }) : null,
          h("a", { class: "btn btn-ghost btn-lg", href: "#/", text: "Zur Übersicht" })))));
      if (a.xp_neu) toast(`+${a.xp_neu} XP für den Diagnosetest`);
      uebersichtLaden().catch(() => {});
    }
  };
  return null;
}

export { plural };
