// Fragekarten für alle Fragetypen (Vertrag Abschnitt 5).
// Ablauf: zwei Versuche, gestufte Tipps, ruhiges Feedback ("Fast!" statt "Falsch!"), Rechenweg.
import { h, inline, debounce, bestaetigen, toast, reduziert } from "./util.js";
import { api } from "./api.js";
import { setStatistik } from "./store.js";
import { texHtml } from "./formel.js";
import { renderBloecke, rechenwegElement, erklaerungElement } from "./markup.js";
import { eingabeFeld, zellenGitter } from "./eingabe.js";
import { visual } from "./visuals.js";
import { koordinaten, zahlText, auswerten } from "./plot.js";

export const TYP_INFO = {
  mc: { icon: "🔘", name: "Auswahl" }, wf: { icon: "⚖️", name: "Wahr oder falsch?" }, text: { icon: "✍️", name: "Kurze Antwort" },
  zahl: { icon: "🔢", name: "Zahl eingeben" }, term: { icon: "🧮", name: "Term eingeben" }, loesungsmenge: { icon: "🎯", name: "Lösungsmenge" },
  menge: { icon: "🫧", name: "Menge angeben" }, vektor: { icon: "➡️", name: "Vektor" }, matrix: { icon: "▦", name: "Matrix" },
  lgs: { icon: "🧩", name: "Gleichungssystem" }, mehrfach: { icon: "☑️", name: "Mehrfachauswahl" }, zuordnen: { icon: "🔗", name: "Zuordnen" },
  ordnen: { icon: "🪜", name: "Schritte ordnen" }, luecke: { icon: "⬚", name: "Lücken füllen" }, graph_punkt: { icon: "📍", name: "Am Graphen" },
  rechenweg: { icon: "👣", name: "Schritt für Schritt" }, papier: { icon: "📝", name: "Auf Papier" }, generator: { icon: "⚙️", name: "Übungsmaschine" },
};
const LOB = ["Richtig!", "Super!", "Genau so!", "Stark!", "Sehr gut!", "Sauber gerechnet!"];

let aktiveKarte = null;
document.addEventListener("keydown", (e) => {
  if (!aktiveKarte || !aktiveKarte.el.isConnected) return;
  if (e.target.closest && e.target.closest("input, textarea, select, [contenteditable]")) return;
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  if (document.querySelector(".dialog-hg")) return;
  aktiveKarte.taste && aktiveKarte.taste(e);
});

const tippsVon = (f) => (Array.isArray(f.tipps) ? f.tipps : []);

export function xpFlug(xp) {
  if (!xp || xp <= 0) return;
  const ziel = document.getElementById("xp-pill");
  const r = ziel ? ziel.getBoundingClientRect() : { left: window.innerWidth / 2, bottom: 60 };
  const el = h("div", { class: "xp-flug", text: `+${xp} XP`, "aria-hidden": "true" });
  el.style.left = r.left + "px";
  el.style.top = (r.bottom + 8) + "px";
  document.body.append(el);
  setTimeout(() => el.remove(), 1500);
}

function frageText(f) {
  if (Array.isArray(f.frage_bloecke) && f.frage_bloecke.length) return h("div", { class: "frage-text frage-md" }, renderBloecke(f.frage_bloecke));
  return h("div", { class: "frage-text", html: inline(f.frage || "") });
}

/** Feedback-Box. art: ok | nochmal | loesung | lesen */
function feedbackBox(art, { titel, r = null, xp = 0, extra = null }) {
  const icon = { ok: "✓", nochmal: "↻", loesung: "💡", lesen: "?" }[art];
  const box = h("div", { class: `feedback ${art}`, role: "status", "aria-live": "polite" },
    h("div", { class: "feedback-kopf" }, h("span", { class: "f-icon", "aria-hidden": "true", text: icon }), h("span", { text: titel }),
      xp > 0 ? h("span", { class: "chip primary xp-chip", text: `+${xp} XP` }) : null));
  if (r) {
    const meldung = r.meldung && !/^(noch nicht ganz\.?|richtig!?|fast!.*)$/i.test(r.meldung.trim()) && !LOB.includes(r.meldung) ? r.meldung : null;
    if (meldung) box.append(h("div", { class: "f-meldung", html: inline(meldung) }));
    if (r.hinweis) box.append(h("div", { class: "f-hinweis" }, h("span", { class: "f-hinweis-icon", "aria-hidden": "true", text: r.fehler_erkannt ? "🔍" : "💬" }), h("span", { html: inline(r.hinweis) })));
    if (r.loesung) box.append(h("div", { class: "f-loesung" }, h("span", { class: "lbl", text: "Lösung" }), h("div", { class: "loesung-text", html: inline(String(r.loesung).replace(/\$(?!\$)([^$]+)\$/g, (_, t) => "$\\displaystyle " + t + "$")) })));
    const rw = rechenwegElement(r.rechenweg_bloecke);
    if (rw) {
      if (art === "ok") {
        const knopf = h("button", { class: "btn btn-sm btn-ghost", type: "button", text: "👣 Rechenweg ansehen" });
        const slot = h("div", { class: "f-rechenweg", hidden: true }, h("span", { class: "lbl", text: "Rechenweg" }), rw);
        knopf.onclick = () => { slot.hidden = !slot.hidden; };
        box.append(h("div", { style: { marginTop: "8px" } }, knopf), slot);
      } else box.append(h("div", { class: "f-rechenweg" }, h("span", { class: "lbl", text: "So geht's: der komplette Rechenweg" }), rw));
    }
    const erk = erklaerungElement(r.erklaerung_bloecke, r.erklaerung);
    if (erk && (art !== "nochmal")) box.append(h("div", { class: "f-erklaerung" }, erk));
  }
  if (extra) box.append(extra);
  return box;
}

/** Gestaffelte Tipps: Tipp 1 vage → Tipp 3 fast die Lösung → danach Rechenweg. */
function tippBereich(tipps, onLetzter) {
  const liste = h("div", { class: "tipps-liste" });
  let n = 0;
  const btn = h("button", { class: "btn btn-ghost", type: "button" });
  const text = () => {
    if (n >= tipps.length) { btn.textContent = "💡 Alle Tipps gezeigt"; btn.disabled = true; }
    else btn.textContent = tipps.length > 1 ? `💡 Tipp ${n + 1} von ${tipps.length}` : "💡 Tipp";
  };
  btn.onclick = () => {
    if (n >= tipps.length) return;
    liste.append(h("div", { class: "tipp" }, h("span", { class: "t-nr", text: tipps.length > 1 ? `Tipp ${n + 1}` : "Tipp" }), h("div", { html: inline(tipps[n]) })));
    n++; text();
    if (n >= tipps.length && onLetzter) onLetzter();
  };
  text();
  if (!tipps.length) btn.hidden = true;
  return { btn, liste, naechster: () => btn.onclick() };
}

/**
 * Erzeugt eine Fragekarte.
 * opts.onFertig({ok, versuch, ergebnis, loesungAngesehen, teilpunkte}) – Status ist endgültig.
 * opts.kontext – Text-Chip (z. B. Kapitelname). opts.klausur – Klausurmodus: keine Tipps/Rechenweg vor der Abgabe.
 */
export function frageKarte(f, opts = {}) {
  const info = TYP_INFO[f.typ] || { icon: "❓", name: f.art || "Frage" };
  const karte = { el: null, taste: null, fertig: false, f };
  const el = h("article", { class: "karte frage-karte", "aria-label": info.name, "data-id": f.id, "data-typ": f.typ, "data-seed": f.seed ?? "" });
  karte.el = el;
  aktiveKarte = karte;
  el.addEventListener("pointerdown", () => { aktiveKarte = karte; });
  el.addEventListener("focusin", () => { aktiveKarte = karte; });

  el.append(h("div", { class: "frage-kopf" },
    h("span", { class: "frage-typ" }, h("span", { text: info.icon }), info.name),
    f.generator_titel ? h("span", { class: "chip", title: "Diese Aufgabe wird jedes Mal mit neuen Zahlen erzeugt", text: `⚙️ ${f.generator_titel}` }) : null,
    f.uebungsblatt ? h("span", { class: "chip gelb", text: "🎓 Übungsblatt-Stil" }) : null,
    h("span", { class: "rechts" }, opts.kontext ? h("span", { class: "chip", text: opts.kontext }) : null)));
  el.append(frageText(f));

  if (f.typ === "rechenweg") return rechenwegKarte(f, opts, karte);
  if (f.typ === "papier") return papierKarte(f, opts, karte);

  const bereich = h("div", { class: "antwort-bereich" });
  const rwBtn = h("button", { class: "btn btn-ghost", type: "button", text: "👣 Rechenweg zeigen", hidden: !f.hat_rechenweg || opts.klausur });
  const tipps = tippBereich(opts.klausur ? [] : tippsVon(f), () => rwBtn.classList.add("btn-soft"));
  const pruefenBtn = h("button", { class: "btn btn-primary btn-lg", type: "button", text: "Prüfen" });
  const aktionen = h("div", { class: "frage-aktionen" }, tipps.btn, rwBtn, h("span", { class: "spacer" }), pruefenBtn);
  const fbSlot = h("div");
  el.append(bereich, tipps.liste, aktionen, fbSlot);

  let versuch = opts.klausur ? 2 : 1;     // Klausur/Diagnose: nur ein Versuch
  let antwortHolen = () => null;
  let nachErgebnis = () => {};
  let sperren = () => {};

  async function senden() {
    if (karte.fertig) return;
    const antwort = antwortHolen();
    if (antwort === undefined) return;
    if (antwort === null || (typeof antwort === "string" && !antwort.trim())) { toast("Bitte gib zuerst eine Antwort ein."); return; }
    pruefenBtn.disabled = true;
    let r;
    try { r = await api.post("/api/antwort", { id: f.id, seed: f.seed, antwort, versuch }); }
    catch (e) { toast(e.message, "rot"); pruefenBtn.disabled = false; return; }
    pruefenBtn.disabled = false;
    if (r.statistik) setStatistik(r.statistik);
    if (r.lesefehler) {
      fbSlot.replaceChildren(feedbackBox("lesen", { titel: "Das kann ich noch nicht lesen", r: { meldung: r.meldung, hinweis: "Dieser Versuch zählt nicht. Schau in die Vorschau unter dem Eingabefeld." } }));
      return;
    }
    if (r.ok) {
      xpFlug(r.xp_neu);
      fbSlot.replaceChildren(feedbackBox("ok", { titel: versuch === 1 ? LOB[Math.floor(Math.random() * LOB.length)] : "Richtig – im zweiten Versuch!", r, xp: r.xp_neu, extra: neuKnopf() }));
      abschliessen(true, r);
    } else if (r.zweiter_versuch) {
      const titel = r.fehler_erkannt ? "Fast! Da steckt ein typischer Fehler drin." : r.fast ? "Fast! Nur noch eine Kleinigkeit." : "Noch nicht ganz. Du hast noch einen Versuch.";
      fbSlot.replaceChildren(feedbackBox("nochmal", { titel, r }));
      if (!reduziert()) { el.classList.remove("stupsen"); void el.offsetWidth; el.classList.add("stupsen"); }
      versuch = 2;
      nachErgebnis(r, false);
      pruefenBtn.textContent = "Nochmal prüfen";
      if (tippsVon(f).length && !tipps.btn.disabled && !opts.klausur) tipps.naechster();
    } else {
      fbSlot.replaceChildren(feedbackBox("loesung", { titel: r.fehler_erkannt ? "Typischer Fehler – so geht es richtig:" : "Schau dir an, wie es geht:", r, extra: neuKnopf() }));
      abschliessen(false, r);
    }
  }

  function neuKnopf() {
    if (!f.generator_titel || opts.klausur || !opts.neueAufgabe) return null;
    return h("div", { class: "neu-zeile" }, h("button", { class: "btn btn-soft", type: "button", text: "🔁 Neue Aufgabe dieser Art", onclick: () => opts.neueAufgabe() }));
  }

  function abschliessen(ok, r) {
    karte.fertig = true;
    sperren(ok, r);
    nachErgebnis(r, true);
    aktionen.hidden = true;
    if (opts.onFertig) opts.onFertig({ ok, versuch, ergebnis: r, teilpunkte: r.teilpunkte });
  }
  pruefenBtn.onclick = senden;

  rwBtn.onclick = async () => {
    if (!(await bestaetigen("Rechenweg ansehen?", "Probier es ruhig noch ein bisschen, Fehler gehören zum Lernen. Wenn du jetzt den Rechenweg ansiehst, zählt die Aufgabe **nicht** als selbst gelöst. Sie kommt später in die Fehlerkiste.", "Rechenweg zeigen", "Weiter probieren", "👣"))) return;
    try {
      const r = await api.post("/api/loesung", { id: f.id, seed: f.seed });
      if (r.statistik) setStatistik(r.statistik);
      fbSlot.replaceChildren(feedbackBox("loesung", { titel: "So geht's:", r: { loesung: r.loesung, rechenweg_bloecke: r.rechenweg_bloecke, erklaerung_bloecke: r.erklaerung_bloecke }, extra: neuKnopf() }));
      karte.fertig = true; aktionen.hidden = true; sperren(false, {});
      if (opts.onFertig) opts.onFertig({ ok: false, loesungAngesehen: true });
    } catch (e) { toast(e.message, "rot"); }
  };

  // ---------- Typ-spezifisch ----------
  const t = f.typ;
  if (t === "mc") {
    const optionen = f.optionen || [];
    let gewaehlt = null;
    const buttons = optionen.map((o, i) => {
      const b = h("button", { class: "option", type: "button", "aria-pressed": "false" }, h("span", { class: "taste", text: i + 1 }), h("span", { class: "opt-text", html: inline(o) }));
      b.onclick = () => {
        if (karte.fertig || b.classList.contains("falsch")) return;
        gewaehlt = i;
        buttons.forEach((x, k) => { x.classList.toggle("gewaehlt", k === i); x.setAttribute("aria-pressed", String(k === i)); });
      };
      return b;
    });
    bereich.append(h("div", { class: "optionen", role: "group", "aria-label": "Antwortmöglichkeiten" }, buttons),
      h("p", { class: "antwort-hinweis", html: `Tasten <kbd>1</kbd>–<kbd>${Math.min(9, optionen.length)}</kbd> wählen, <kbd>Enter</kbd> prüft.` }));
    antwortHolen = () => (gewaehlt === null ? null : optionen[gewaehlt]);
    nachErgebnis = (r, endgueltig) => {
      if (gewaehlt !== null && !r.ok) { buttons[gewaehlt].classList.replace("gewaehlt", "falsch"); buttons[gewaehlt].disabled = true; gewaehlt = null; }
      if (r.ok && gewaehlt !== null) buttons[gewaehlt].classList.replace("gewaehlt", "richtig");
      if (endgueltig) {
        buttons.forEach(b => { b.disabled = true; });
        if (r.loesung) buttons.forEach((b, i) => { if (optionen[i].trim() === String(r.loesung).trim()) b.classList.add("richtig"); });
      }
    };
    karte.taste = (e) => {
      if (karte.fertig) return;
      const n = parseInt(e.key, 10);
      if (n >= 1 && n <= buttons.length) { e.preventDefault(); buttons[n - 1].click(); buttons[n - 1].focus(); }
      else if (e.key === "Enter" && gewaehlt !== null && !e.target.closest("button:not(.option)")) { e.preventDefault(); senden(); }
    };
  } else if (t === "wf") {
    pruefenBtn.hidden = true;
    let wahl = null;
    const bw = h("button", { class: "wf-btn wahr", type: "button" }, h("span", { class: "gross", text: "👍" }), "Wahr", h("small", { text: "Taste W" }));
    const bf = h("button", { class: "wf-btn falsch-btn", type: "button" }, h("span", { class: "gross", text: "👎" }), "Falsch", h("small", { text: "Taste F" }));
    bw.onclick = () => { if (!karte.fertig) { wahl = true; senden(); } };
    bf.onclick = () => { if (!karte.fertig) { wahl = false; senden(); } };
    bereich.append(h("div", { class: "wf-buttons" }, bw, bf));
    antwortHolen = () => wahl;
    sperren = (ok) => {
      bw.disabled = bf.disabled = true;
      if (wahl === null) return;
      (wahl ? bw : bf).classList.add(ok ? "richtig" : "falsch");
      if (!ok) (wahl ? bf : bw).classList.add("richtig");
    };
    karte.taste = (e) => {
      if (karte.fertig) return;
      if (e.key === "w" || e.key === "W") { e.preventDefault(); bw.click(); }
      if (e.key === "f" || e.key === "F") { e.preventDefault(); bf.click(); }
    };
  } else if (["text", "zahl", "term", "loesungsmenge", "menge"].includes(t)) {
    const modus = { text: "text", zahl: "zahl", term: "term", loesungsmenge: "bereich", menge: "menge" }[t];
    const ein = eingabeFeld({ modus, variablen: f.variablen || [], einheit: f.einheit, onEnter: senden, wert: f.entwurf || "" });
    bereich.append(ein.el);
    const hinweise = [];
    if (t === "zahl" && f.gekuerzt) hinweise.push("Gib das Ergebnis <b>vollständig gekürzt</b> an.");
    if (t === "zahl" && f.toleranz) hinweise.push(`Gerundete Ergebnisse sind ok (Abweichung bis ${zahlText(f.toleranz, 4)}).`);
    if (t === "term" && f.form) hinweise.push({ ausmultipliziert: "Gesucht: <b>ausmultipliziert</b> (ohne Klammern um Summen).", faktorisiert: "Gesucht: als <b>Produkt</b> (faktorisiert).", gekuerzt: "Gesucht: <b>vollständig gekürzt</b>.", vereinfacht: "Gesucht: so <b>einfach</b> wie möglich.", ohne_klammern: "Gesucht: <b>ohne Klammern</b>." }[f.form] || "");
    if (t === "loesungsmenge") hinweise.push("Mehrere Lösungen mit <b>;</b> trennen, z. B. <code class=\"ic\">{2; -3}</code>. Keine Lösung: <code class=\"ic\">keine</code>. Intervalle wie <code class=\"ic\">[0; 4)</code> oder <code class=\"ic\">x &lt; 2</code>.");
    if (t === "menge") hinweise.push("Elemente mit <b>;</b> trennen, z. B. <code class=\"ic\">{1; 2; 3}</code>. Leere Menge: <code class=\"ic\">{}</code>.");
    hinweise.push("<kbd>Enter</kbd> prüft.");
    bereich.append(h("p", { class: "antwort-hinweis", html: hinweise.filter(Boolean).join(" ") }));
    antwortHolen = () => ein.wert();
    nachErgebnis = (r, endgueltig) => { ein.markieren(!!r.ok); if (!endgueltig) ein.inp.select(); };
    sperren = (ok) => ein.sperren(ok);
    karte.fokus = () => ein.fokus();
    entwurfMerken(f, ein.inp);
  } else if (t === "vektor" || t === "matrix") {
    const g = zellenGitter({ zeilen: f.zeilen, spalten: f.spalten || 1, onEnter: senden });
    bereich.append(g.el, h("p", { class: "antwort-hinweis", html: (f.vielfaches ? "Jedes Vielfache (≠ 0) der Lösung ist auch richtig. " : "") + "Brüche wie <code class=\"ic\">3/4</code> sind erlaubt. <kbd>Enter</kbd> springt weiter." }));
    antwortHolen = () => { const w = g.werte(); return (Array.isArray(w[0]) ? w.flat() : w).some(x => !String(x).trim()) ? (toast("Bitte fülle alle Felder aus."), undefined) : w; };
    nachErgebnis = (r) => g.markieren(r.details);
    sperren = () => g.sperren();
    karte.fokus = () => g.fokus();
  } else if (t === "lgs") {
    const g = zellenGitter({ zeilen: f.zeilen, namen: f.variablen, onEnter: senden, parameter: true });
    const keine = h("input", { type: "checkbox" });
    const schalter = h("label", { class: "schalter" }, keine, h("span", { text: "Das System hat keine Lösung" }));
    keine.onchange = () => g.felder.flat().forEach(x => { x.disabled = keine.checked; });
    bereich.append(h("div", { class: "lgs-eingabe" }, g.el, h("div", null, schalter,
      h("p", { class: "antwort-hinweis", html: "Gibt es unendlich viele Lösungen, schreibe sie mit einem Parameter, z. B. <code class=\"ic\">2 + 3t</code>. Erlaubt sind <code class=\"ic\">t, s, r, u</code>." }))));
    antwortHolen = () => {
      if (keine.checked) return { keine: true, werte: [] };
      const w = g.werte();
      return w.some(x => !String(x).trim()) ? (toast("Bitte fülle alle Felder aus."), undefined) : { keine: false, werte: w };
    };
    sperren = () => { g.sperren(); keine.disabled = true; };
    karte.fokus = () => g.fokus();
  } else if (t === "mehrfach") {
    const gewaehlt = new Set();
    const buttons = (f.optionen || []).map((o) => {
      const b = h("button", { class: "option mehrfach", type: "button", "aria-pressed": "false" }, h("span", { class: "kaestchen", "aria-hidden": "true" }), h("span", { class: "opt-text", html: inline(o) }));
      b.onclick = () => {
        if (karte.fertig) return;
        if (gewaehlt.has(o)) gewaehlt.delete(o); else gewaehlt.add(o);
        b.classList.toggle("gewaehlt", gewaehlt.has(o)); b.setAttribute("aria-pressed", String(gewaehlt.has(o)));
      };
      return b;
    });
    bereich.append(h("div", { class: "optionen" }, buttons), h("p", { class: "antwort-hinweis", text: "Es können mehrere Antworten richtig sein – oder auch keine." }));
    antwortHolen = () => [...gewaehlt];
    nachErgebnis = (r, endgueltig) => {
      if (!endgueltig) return;
      (r.details || []).forEach((d) => {
        const i = (f.optionen || []).indexOf(d.name);
        if (i >= 0) { buttons[i].classList.add(d.soll ? "richtig" : (gewaehlt.has(d.name) ? "falsch" : "neutral")); buttons[i].disabled = true; }
      });
    };
  } else if (t === "zuordnen") {
    const selects = (f.links || []).map((l) => {
      const s = h("select", { class: "feld zuordnen-wahl", "aria-label": `Zuordnung für ${l}` }, h("option", { value: "", text: "– bitte wählen –" }),
        (f.rechts || []).map(r => h("option", { value: r, text: r.replace(/\$/g, "") })));
      return s;
    });
    bereich.append(h("div", { class: "zuordnen" }, (f.links || []).map((l, i) => h("div", { class: "zuordnen-zeile" },
      h("div", { class: "zuordnen-links", html: inline(l) }), h("span", { class: "zuordnen-pfeil", text: "→" }), selects[i]))));
    antwortHolen = () => (selects.some(s => !s.value) ? (toast("Bitte ordne jedem Eintrag etwas zu."), undefined) : (f.links || []).map((l, i) => [l, selects[i].value]));
    nachErgebnis = (r) => (r.details || []).forEach((d, i) => { selects[i].classList.toggle("ok", d.ok); selects[i].classList.toggle("nok", !d.ok); });
    sperren = () => selects.forEach(s => { s.disabled = true; });
  } else if (t === "ordnen") {
    const pz = ordnenBereich(f);
    bereich.append(pz.el);
    antwortHolen = () => (pz.ids().length ? pz.ids() : (toast("Lege zuerst Schritte in „Deine Reihenfolge“."), undefined));
    sperren = (ok) => pz.sperren(ok);
  } else if (t === "luecke") {
    let k = 0;
    const tex = String(f.formel || "").replace(/\\luecke/g, () => `\\boxed{\\,\\textsf{${++k}}\\,}`);
    const felder = [];
    const liste = h("div", { class: "luecken-liste" });
    for (let i = 0; i < k; i++) {
      const ein = eingabeFeld({ modus: "term", label: `Lücke ${i + 1}`, onEnter: () => (i < k - 1 ? felder[i + 1].fokus() : senden()) });
      ein.el.querySelector(".pad-kopf")?.remove(); ein.el.querySelector(".pad")?.remove();
      felder.push(ein);
      liste.append(h("div", { class: "luecke-zeile" }, h("span", { class: "luecke-nr", text: i + 1 }), ein.el));
    }
    bereich.append(h("div", { class: "formel-block gross", html: texHtml(tex, true) }), liste);
    antwortHolen = () => (felder.some(x => !x.wert().trim()) ? (toast("Bitte fülle alle Lücken aus."), undefined) : felder.map(x => x.wert()));
    nachErgebnis = (r) => (r.details || []).forEach((d, i) => felder[i] && felder[i].markieren(d.ok));
    sperren = () => felder.forEach(x => x.sperren());
    karte.fokus = () => felder[0] && felder[0].fokus();
  } else if (t === "graph_punkt") {
    if (f.modus === "setzen") {
      let gesetzt = null;
      const anzeige = h("div", { class: "ausdruck-zeile", text: "Tippe ins Koordinatensystem, um den Punkt zu setzen." });
      const d = f.visual || {};
      const fns = (d.funktionen || []).map(fn => (x) => auswerten(fn._ast, { x }));
      const k = koordinaten({ x: (d.x || [-5, 5]).map(Number), y: (d.y || [-5, 5]).map(Number), klickbar: true, zoom: false }, (k) => {
        fns.forEach((fn, i) => k.kurve(fn, "kurve", `var(--plot-${i + 1})`));
        if (gesetzt) k.punkt(gesetzt[0], gesetzt[1], { klasse: "punkt gesetzt", label: `P(${zahlText(gesetzt[0])} | ${zahlText(gesetzt[1])})` });
      });
      k.svg.style.cursor = "crosshair";
      k.svg.addEventListener("click", (e) => {
        if (karte.fertig) return;
        const r = k.svg.getBoundingClientRect();
        const [x, y] = k.inv((e.clientX - r.left) / r.width * k.W, (e.clientY - r.top) / r.height * k.H);
        const ras = f.raster || 0.5;
        gesetzt = [Math.round(x / ras) * ras, Math.round(y / ras) * ras];
        anzeige.textContent = `Dein Punkt: P(${zahlText(gesetzt[0])} | ${zahlText(gesetzt[1])})`;
        k.neu();
      });
      bereich.append(h("div", { class: "vis-scroll" }, k.el), anzeige);
      el._punktSetzen = ([x, y]) => { gesetzt = [x, y]; anzeige.textContent = `Dein Punkt: P(${zahlText(x)} | ${zahlText(y)})`; k.neu(); };
      antwortHolen = () => (gesetzt ? gesetzt.map(String) : (toast("Setze zuerst einen Punkt."), undefined));
    } else {
      bereich.append(visual("funktionsgraph", f.visual));
      const ein = eingabeFeld({ modus: "zahl", onEnter: senden });
      bereich.append(ein.el);
      antwortHolen = () => ein.wert();
      sperren = (ok) => ein.sperren(ok);
      karte.fokus = () => ein.fokus();
    }
  } else {
    bereich.append(h("p", { class: "vis-fehler", text: `Unbekannter Fragetyp „${t}“.` }));
  }
  karte.fokus = karte.fokus || (() => el.querySelector("button.option, input, textarea")?.focus({ preventScroll: true }));
  karte.pruefen = senden;
  return karte;
}

function entwurfMerken(f, inp) {
  if (f.seed) return;    // Generator-Instanzen sind flüchtig
  const merken = debounce(() => api.post("/api/entwurf", { id: f.id, text: inp.value }).catch(() => {}), 1500);
  inp.addEventListener("input", merken);
}

/* ---------------------------------------------------------------- Ordnen */
function ordnenBereich(f) {
  const quelle = h("div", { class: "puzzle-zone quelle", role: "list", "aria-label": "Schritte" }, h("h4", { text: "🧱 Schritte" }));
  const ziel = h("div", { class: "puzzle-zone ziel", role: "list", "aria-label": "Deine Reihenfolge" }, h("h4", { text: "🪜 Deine Reihenfolge" }));
  let gesperrt = false;
  const umsetzen = (b) => { if (!gesperrt) { (b.parentElement === quelle ? ziel : quelle).append(b); aktualisieren(); } };
  const verschieben = (b, r) => {
    if (gesperrt) return;
    const n = r < 0 ? b.previousElementSibling : b.nextElementSibling;
    if (n && n.classList.contains("baustein")) (r < 0 ? n.before(b) : n.after(b));
    aktualisieren();
  };
  for (const z of f.zeilen || []) {
    const hoch = h("button", { type: "button", "aria-label": "nach oben", text: "↑" });
    const runter = h("button", { type: "button", "aria-label": "nach unten", text: "↓" });
    const b = h("div", { class: "baustein", tabindex: "0", role: "listitem", "data-id": z.zeilen_id },
      h("span", { class: "bs-text", html: inline(z.text) }), h("span", { class: "bs-aktionen" }, hoch, runter));
    hoch.onclick = (e) => { e.stopPropagation(); verschieben(b, -1); };
    runter.onclick = (e) => { e.stopPropagation(); verschieben(b, 1); };
    b.onclick = () => umsetzen(b);
    b.onkeydown = (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); umsetzen(b); b.focus(); }
      else if (e.altKey && e.key === "ArrowUp") { e.preventDefault(); verschieben(b, -1); b.focus(); }
      else if (e.altKey && e.key === "ArrowDown") { e.preventDefault(); verschieben(b, 1); b.focus(); }
    };
    quelle.append(b);
  }
  function aktualisieren() {
    ziel.querySelectorAll(".bs-aktionen").forEach(a => { a.hidden = false; });
    quelle.querySelectorAll(".bs-aktionen").forEach(a => { a.hidden = true; });
    ziel.classList.toggle("leer", !ziel.querySelector(".baustein"));
  }
  aktualisieren();
  return {
    el: h("div", null, h("div", { class: "puzzle" }, quelle, ziel),
      h("p", { class: "antwort-hinweis", html: `Klicke die Schritte in der richtigen Reihenfolge an (${f.anzahl} gehören hinein). Vorsicht: Manche Schritte sind falsch! Mit ↑ ↓ sortierst du um.` })),
    ids: () => [...ziel.querySelectorAll(".baustein")].map(b => b.dataset.id),
    sperren: (ok) => { gesperrt = true; ziel.querySelectorAll(".baustein").forEach(b => b.classList.add(ok ? "ok" : "nok")); ziel.querySelectorAll(".bs-aktionen").forEach(a => { a.hidden = true; }); },
  };
}

/* ---------------------------------------------------------------- Rechenweg (Teilschritte) */
function rechenwegKarte(f, opts, karte) {
  const el = karte.el;
  const schritte = f.schritte || [];
  const ergebnisse = [];
  const liste = h("ol", { class: "schritt-liste" });
  el.append(liste);
  const fbSlot = h("div");
  el.append(fbSlot);
  let aktiv = 0;

  function schrittBauen(i) {
    const s = schritte[i];
    const li = h("li", { class: "teilschritt aktiv" });
    li.append(h("div", { class: "ts-kopf" }, h("span", { class: "ts-nr", text: `Schritt ${i + 1} von ${schritte.length}` })), h("div", { class: "ts-frage", html: inline(s.frage) }));
    const modus = { zahl: "zahl", term: "term", loesungsmenge: "bereich", menge: "menge", text: "text" }[s.typ];
    let holen, ein = null, g = null;
    let versuch = opts.klausur ? 2 : 1;
    const tipps = tippBereich(opts.klausur ? [] : s.tipps || []);
    const pruefen = h("button", { class: "btn btn-primary", type: "button", text: "Schritt prüfen" });
    const fb = h("div");
    if (modus) {
      ein = eingabeFeld({ modus, variablen: s.variablen || [], onEnter: () => pruefen.click() });
      li.append(ein.el);
      holen = () => ein.wert();
    } else if (s.typ === "vektor" || s.typ === "matrix") {
      g = zellenGitter({ zeilen: s.zeilen, spalten: s.spalten || 1, onEnter: () => pruefen.click() });
      li.append(g.el);
      holen = () => g.werte();
    } else if (s.typ === "mc") {
      let wahl = null;
      const bs = (s.optionen || []).map(o => { const b = h("button", { class: "option", type: "button", html: inline(o) }); b.onclick = () => { wahl = o; bs.forEach(x => x.classList.toggle("gewaehlt", x === b)); }; return b; });
      li.append(h("div", { class: "optionen" }, bs));
      holen = () => wahl;
    }
    li.append(tipps.liste, h("div", { class: "frage-aktionen" }, tipps.btn, h("span", { class: "spacer" }), pruefen), fb);
    pruefen.onclick = async () => {
      const antwort = holen();
      if (antwort === null || antwort === "" || antwort === undefined) { toast("Bitte gib zuerst etwas ein."); return; }
      pruefen.disabled = true;
      let r;
      try { r = await api.post("/api/antwort", { id: f.id, seed: f.seed, schritt: i, antwort, versuch, bisher: ergebnisse }); }
      catch (e) { toast(e.message, "rot"); pruefen.disabled = false; return; }
      pruefen.disabled = false;
      if (r.statistik) setStatistik(r.statistik);
      if (r.lesefehler) { fb.replaceChildren(feedbackBox("lesen", { titel: "Das kann ich noch nicht lesen", r: { meldung: r.meldung } })); return; }
      if (r.ok || !r.zweiter_versuch) {
        ergebnisse.push(!!r.ok);
        fb.replaceChildren(feedbackBox(r.ok ? "ok" : "loesung", { titel: r.ok ? "Richtig!" : "Hier der richtige Wert – damit geht es weiter:", r: { ...r, erklaerung_bloecke: [], erklaerung: "" }, xp: r.xp_neu }));
        pruefen.hidden = true; tipps.btn.hidden = true;
        if (ein) ein.sperren(r.ok); if (g) g.sperren();
        li.classList.replace("aktiv", r.ok ? "ok" : "nok");
        if (i + 1 < schritte.length) { aktiv = i + 1; schrittBauen(aktiv); }
        else fertig(r);
      } else {
        versuch = 2;
        fb.replaceChildren(feedbackBox("nochmal", { titel: r.fehler_erkannt ? "Fast! Typischer Fehler erkannt." : "Noch nicht ganz – noch ein Versuch.", r }));
        if ((s.tipps || []).length && !opts.klausur) tipps.naechster();
      }
    };
    liste.append(li);
    setTimeout(() => { ein ? ein.fokus() : g && g.fokus(); }, 80);
  }

  function fertig(r) {
    const richtig = ergebnisse.filter(Boolean).length;
    const ok = richtig === schritte.length;
    karte.fertig = true;
    if (ok) xpFlug(r.xp_neu);
    fbSlot.replaceChildren(feedbackBox(ok ? "ok" : "loesung", { titel: ok ? "Alle Schritte richtig! 🎉" : `${richtig} von ${schritte.length} Schritten richtig`, r: { rechenweg_bloecke: r.rechenweg_bloecke, erklaerung_bloecke: r.erklaerung_bloecke } }));
    if (opts.onFertig) opts.onFertig({ ok, ergebnis: r, teilpunkte: richtig / schritte.length });
  }
  schrittBauen(0);
  karte.fokus = () => liste.querySelector("input")?.focus({ preventScroll: true });
  return karte;
}

/* ---------------------------------------------------------------- Papier */
function papierKarte(f, opts, karte) {
  const el = karte.el;
  const notizen = h("textarea", { class: "feld", rows: 4, placeholder: "Platz für Notizen (optional). Die eigentliche Lösung schreibst du auf Papier.", "aria-label": "Notizen" });
  if (f.entwurf) notizen.value = f.entwurf;
  const merken = debounce(() => api.post("/api/entwurf", { id: f.id, text: notizen.value }).catch(() => {}), 1500);
  notizen.addEventListener("input", merken);
  const fertigBtn = h("button", { class: "btn btn-primary btn-lg", type: "button", text: "Ich bin fertig – Musterlösung zeigen" });
  const slot = h("div");
  el.append(h("div", { class: "papier-hinweis" }, h("span", { "aria-hidden": "true", text: "📝" }),
    h("span", { html: "Nimm Stift und Papier. Schreib jeden Schritt auf und begründe ihn. Danach vergleichst du mit der Musterlösung und bewertest dich selbst – ehrlich ist am hilfreichsten." })),
    notizen, h("div", { class: "frage-aktionen" }, h("span", { class: "spacer" }), fertigBtn), slot);
  fertigBtn.onclick = async () => {
    let d;
    try { d = await api.post("/api/papier/loesung", { id: f.id, seed: f.seed }); } catch (e) { toast(e.message, "rot"); return; }
    fertigBtn.hidden = true;
    const haken = d.checkliste.map(() => null);
    const zeilen = d.checkliste.map((c, i) => {
      const ja = h("button", { class: "btn btn-sm", type: "button", text: "✅ geschafft" });
      const nein = h("button", { class: "btn btn-sm", type: "button", text: "❌ noch nicht" });
      const setzen = (v) => { haken[i] = v; ja.classList.toggle("btn-success", v === true); nein.classList.toggle("btn-soft", v === false); };
      ja.onclick = () => setzen(true); nein.onclick = () => setzen(false);
      return h("li", { class: "check-zeile" }, h("span", { html: inline(c) }), h("span", { class: "btn-gruppe" }, ja, nein));
    });
    const abschicken = h("button", { class: "btn btn-primary", type: "button", text: "Bewertung speichern" });
    const fb = h("div");
    slot.replaceChildren(h("div", { class: "f-rechenweg musterloesung" }, h("span", { class: "lbl", text: "Musterlösung" }), renderBloecke(d.musterloesung_bloecke)),
      h("div", { class: "checkliste" }, h("h4", { text: "Bewerte dich selbst – Punkt für Punkt:" }), h("ul", null, zeilen)),
      h("div", { class: "frage-aktionen" }, h("span", { class: "spacer" }), abschicken), fb);
    abschicken.onclick = async () => {
      if (haken.some(x => x === null)) { toast("Bitte bewerte jeden Punkt."); return; }
      let r;
      try { r = await api.post("/api/antwort", { id: f.id, seed: f.seed, antwort: haken, versuch: 1 }); } catch (e) { toast(e.message, "rot"); return; }
      if (r.statistik) setStatistik(r.statistik);
      xpFlug(r.xp_neu);
      abschicken.hidden = true;
      zeilen.forEach(z => z.querySelectorAll("button").forEach(b => { b.disabled = true; }));
      fb.replaceChildren(feedbackBox(r.ok ? "ok" : "loesung", { titel: r.ok ? "Alles geschafft – stark!" : r.meldung, xp: r.xp_neu }));
      karte.fertig = true;
      if (opts.onFertig) opts.onFertig({ ok: r.ok, ergebnis: r, teilpunkte: r.teilpunkte });
    };
  };
  karte.fokus = () => fertigBtn.focus({ preventScroll: true });
  return karte;
}
