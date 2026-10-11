// Fragekarten für alle Fragetypen: mc, wf, text, ausgabe, ausdruck, luecke, puzzle, code.
import { h, inline, inlineAbsaetze, esc, debounce, bestaetigen, toast, balken, reduziert } from "./util.js";
import { api } from "./api.js";
import { setStatistik } from "./store.js";
import { codeAnzeige, highlight } from "./highlight.js";
import { erklaerungElement, renderBloecke } from "./markup.js";
import { Editor } from "./editor.js";
import { eingabenFeld, ausfuehren, brauchtEingabe } from "./runner.js";
import { tracerPanel, fehlerKarte } from "./tracer.js";
import { pyRepr } from "./werte.js";

export const TYP_INFO = {
  mc: { icon: "🔘", name: "Multiple Choice" },
  wf: { icon: "⚖️", name: "Wahr oder falsch?" },
  text: { icon: "✍️", name: "Kurze Antwort" },
  ausgabe: { icon: "🖨️", name: "Was gibt der Code aus?" },
  ausdruck: { icon: "🧮", name: "Ausdruck schreiben" },
  luecke: { icon: "🧩", name: "Lückentext" },
  puzzle: { icon: "🧱", name: "Code-Puzzle" },
  code: { icon: "💻", name: "Programmieraufgabe" },
};

const LOB = ["Richtig!", "Super!", "Genau so!", "Stark!", "Sehr gut!", "Perfekt!"];

let aktiveKarte = null;
document.addEventListener("keydown", (e) => {
  if (!aktiveKarte || !aktiveKarte.el.isConnected) return;
  if (e.target.closest && e.target.closest("input, textarea, select, [contenteditable]")) return;
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  if (document.querySelector(".dialog-hg")) return;
  aktiveKarte.taste && aktiveKarte.taste(e);
});

const frageText = (f) => f.frage ?? f.aussage ?? f.aufgabe ?? f.text ?? "";

/** Fragetext: mehrteiliges Markup (vom Server geparst) oder einfacher Text mit Inline-Markup. */
function frageTextElement(f, extra = null) {
  const b = f.text_bloecke;
  if (Array.isArray(b) && b.length && !(b.length === 1 && b[0].typ === "absatz")) {
    return h("div", { class: "frage-text frage-md" }, extra, renderBloecke(b));
  }
  return h("div", { class: "frage-text" }, extra, h("div", { html: inlineAbsaetze(frageText(f)) }));
}
const tippsVon = (f) => (Array.isArray(f.tipps) && f.tipps.length ? f.tipps : (f.tipp ? [f.tipp] : []));

export function xpFlug(xp) {
  if (!xp || xp <= 0) return;
  const ziel = document.getElementById("xp-pill");
  const r = ziel ? ziel.getBoundingClientRect() : { left: window.innerWidth / 2, bottom: 60 };
  const el = h("div", { class: "xp-flug", text: `+${xp} XP`, "aria-hidden": "true" });
  el.style.left = r.left + "px";
  el.style.top = (r.bottom + 8) + "px";
  document.body.append(el);
  setTimeout(() => el.remove(), 1500);
  if (ziel && !reduziert()) ziel.animate([{ transform: "scale(1)" }, { transform: "scale(1.15)" }, { transform: "scale(1)" }], { duration: 500, delay: 300 });
}

/** Feedback-Box */
function feedbackBox(art, { titel, meldung, hinweis, loesung, loesungCode = false, ergebnis = null, xp = 0 }) {
  const icon = art === "ok" ? "✓" : art === "nochmal" ? "↻" : "✗";
  const box = h("div", { class: `feedback ${art}`, role: "status", "aria-live": "polite" },
    h("div", { class: "feedback-kopf" }, h("span", { class: "f-icon", "aria-hidden": "true", text: icon }), h("span", { text: titel }),
      xp > 0 ? h("span", { class: "chip primary xp-chip", text: `+${xp} XP` }) : null));
  if (meldung && !/^\s*(leider\s+)?(nicht\s+)?(ganz\s+)?(richtig|falsch)[.!]?\s*$/i.test(meldung)) box.append(h("div", { class: "f-meldung", html: inline(meldung) }));
  if (hinweis) box.append(h("div", { class: "f-hinweis", html: "💬 " + inline(hinweis) }));
  if (loesung !== null && loesung !== undefined && loesung !== "") {
    box.append(h("div", { class: "f-loesung" }, h("span", { class: "lbl", text: "Richtige Lösung" }),
      loesungCode && String(loesung).includes("\n") ? codeAnzeige(loesung) : h("div", { class: "loesung-text", html: loesungCode ? highlight(loesung) : inline(loesung) })));
  }
  if (ergebnis) {
    const e = erklaerungElement(ergebnis);
    if (e) box.append(h("div", { class: "f-erklaerung" }, e));
  }
  return box;
}

/** Gestaffelte Tipps */
function tippBereich(tipps) {
  const liste = h("div", { class: "tipps-liste" });
  let n = 0;
  const btn = h("button", { class: "btn btn-ghost", type: "button" });
  const text = () => {
    if (n >= tipps.length) { btn.textContent = tipps.length > 1 ? "💡 Alle Tipps gezeigt" : "💡 Tipp gezeigt"; btn.disabled = true; }
    else btn.textContent = tipps.length > 1 ? `💡 Tipp ${n + 1} von ${tipps.length}` : "💡 Tipp anzeigen";
  };
  btn.onclick = () => {
    if (n >= tipps.length) return;
    liste.append(h("div", { class: "tipp" }, h("span", { class: "t-nr", text: tipps.length > 1 ? `Tipp ${n + 1}` : "Tipp" }), h("div", { html: inline(tipps[n]) })));
    n++; text();
  };
  text();
  if (!tipps.length) btn.hidden = true;
  return { btn, liste, alleZeigen: () => { while (n < tipps.length) btn.onclick(); } };
}

/**
 * Erzeugt eine Fragekarte.
 * opts.onFertig({ok, versuch, uebersprungen, loesungAngesehen}) – Status hat sich (endgültig) geändert.
 * opts.kontext – z. B. Kapitelname im Training.
 */
export function frageKarte(f, opts = {}) {
  if (f.typ === "code") return codeAufgabe(f, opts);
  const info = TYP_INFO[f.typ] || { icon: "❓", name: f.art || "Frage" };
  const karte = { el: null, taste: null, fertig: false };
  const el = h("article", { class: "karte frage-karte", "aria-label": info.name, "data-id": f.id, "data-typ": f.typ });
  karte.el = el;
  aktiveKarte = karte;
  el.addEventListener("pointerdown", () => { aktiveKarte = karte; });
  el.addEventListener("focusin", () => { aktiveKarte = karte; });

  el.append(h("div", { class: "frage-kopf" },
    h("span", { class: "frage-typ" }, h("span", { text: info.icon }), info.name),
    h("span", { class: "rechts" }, opts.kontext ? h("span", { class: "chip", text: opts.kontext }) : null)));
  const text = frageText(f);
  if (f.typ === "wf") el.append(frageTextElement(f, h("p", { style: { fontSize: "13px", fontWeight: 700, color: "var(--text-2)", textTransform: "uppercase", letterSpacing: ".05em", marginBottom: "6px" }, text: "Stimmt diese Aussage?" })));
  else if (text) el.append(frageTextElement(f));
  if (f.code && f.typ !== "luecke") el.append(h("div", { class: "frage-code" }, codeAnzeige(f.code, { nummern: String(f.code).split("\n").length > 4, kopierbar: false })));

  const bereich = h("div", { class: "antwort-bereich" });
  const tipps = tippBereich(tippsVon(f));
  const pruefenBtn = h("button", { class: "btn btn-primary btn-lg", type: "button", text: "Prüfen" });
  const aktionen = h("div", { class: "frage-aktionen" }, tipps.btn, h("span", { class: "spacer" }), pruefenBtn);
  const fbSlot = h("div");
  el.append(bereich, tipps.liste, aktionen, fbSlot);

  let versuch = 1;
  let antwortHolen = () => null;
  let nachErgebnis = () => {};
  let sperren = () => {};

  async function senden() {
    const antwort = antwortHolen();
    if (antwort === undefined) return;
    if (antwort === null || (typeof antwort === "string" && !antwort.trim()) || (Array.isArray(antwort) && !antwort.length && f.typ === "puzzle")) {
      toast(f.typ === "puzzle" ? "Ziehe zuerst Bausteine in „Dein Programm“." : "Bitte gib zuerst eine Antwort ein.");
      return;
    }
    pruefenBtn.disabled = true;
    let r;
    try { r = await api.post("/api/antwort", { id: f.id, antwort, versuch }); }
    catch (e) { toast(e.message, "rot"); pruefenBtn.disabled = false; return; }
    setStatistik(r.statistik);
    const zweiter = r.zweiter_versuch ?? (versuch === 1 && !r.ok && f.typ !== "wf" && !(f.typ === "mc" && (f.optionen || []).length <= 2));
    if (r.ok) {
      xpFlug(r.xp_neu);
      fbSlot.replaceChildren(feedbackBox("ok", { titel: versuch === 1 ? LOB[Math.floor(Math.random() * LOB.length)] : "Richtig – im zweiten Versuch!", meldung: r.meldung, hinweis: r.hinweis, ergebnis: r, xp: r.xp_neu }));
      abschliessen(true, r);
    } else if (zweiter) {
      fbSlot.replaceChildren(feedbackBox("nochmal", { titel: "Noch nicht ganz – du hast noch einen Versuch!", meldung: r.meldung, hinweis: r.hinweis }));
      el.classList.remove("wackeln"); void el.offsetWidth; if (!reduziert()) el.classList.add("wackeln");
      versuch = 2;
      nachErgebnis(r, false);
      pruefenBtn.disabled = false;
      pruefenBtn.textContent = "Nochmal prüfen";
      if (tippsVon(f).length && !tipps.btn.disabled) tipps.btn.onclick();
    } else {
      fbSlot.replaceChildren(feedbackBox("nok", { titel: "Leider falsch", meldung: r.meldung, hinweis: r.hinweis, loesung: r.loesung,
        loesungCode: ["ausgabe", "ausdruck", "luecke", "puzzle"].includes(f.typ), ergebnis: r }));
      el.classList.remove("wackeln"); void el.offsetWidth; if (!reduziert()) el.classList.add("wackeln");
      abschliessen(false, r);
    }
  }

  function abschliessen(ok, r) {
    karte.fertig = true;
    sperren(ok, r);
    nachErgebnis(r, true);
    aktionen.hidden = true;
    if (opts.onFertig) opts.onFertig({ ok, versuch, ergebnis: r });
  }
  pruefenBtn.onclick = senden;

  // ---------- Typ-spezifisch ----------
  if (f.typ === "mc") {
    const optionen = f.optionen || f.antworten || [];
    let gewaehlt = null;
    const buttons = optionen.map((o, i) => {
      const b = h("button", { class: "option", type: "button", "aria-pressed": "false" },
        h("span", { class: "taste", text: i + 1 }), h("span", { class: "opt-text", html: inline(o) }));
      b.onclick = () => {
        if (karte.fertig || b.classList.contains("falsch")) return;
        gewaehlt = i;
        buttons.forEach((x, k) => { x.classList.toggle("gewaehlt", k === i); x.setAttribute("aria-pressed", k === i ? "true" : "false"); });
      };
      return b;
    });
    bereich.append(h("div", { class: "optionen", role: "group", "aria-label": "Antwortmöglichkeiten" }, buttons));
    bereich.append(h("p", { class: "antwort-hinweis", html: `Tasten <kbd>1</kbd>–<kbd>${Math.min(9, optionen.length)}</kbd> wählen, <kbd>Enter</kbd> prüft.` }));
    antwortHolen = () => (gewaehlt === null ? null : optionen[gewaehlt]);
    nachErgebnis = (r, endgueltig) => {
      if (gewaehlt !== null && !r.ok) { buttons[gewaehlt].classList.remove("gewaehlt"); buttons[gewaehlt].classList.add("falsch"); buttons[gewaehlt].disabled = true; gewaehlt = null; }
      if (r.ok && gewaehlt !== null) { buttons[gewaehlt].classList.remove("gewaehlt"); buttons[gewaehlt].classList.add("richtig"); }
      if (endgueltig) {
        buttons.forEach(b => { b.disabled = true; });
        if (r.loesung) {
          const norm = (s) => String(s).replace(/\s+/g, " ").trim();
          buttons.forEach((b, i) => { if (norm(optionen[i]) === norm(r.loesung)) b.classList.add("richtig"); });
        }
      }
    };
    karte.taste = (e) => {
      if (karte.fertig) return;
      const n = parseInt(e.key, 10);
      if (n >= 1 && n <= buttons.length) { e.preventDefault(); buttons[n - 1].click(); buttons[n - 1].focus(); }
      else if (e.key === "Enter" && gewaehlt !== null && !e.target.closest("button:not(.option)")) { e.preventDefault(); senden(); }
    };
  } else if (f.typ === "wf") {
    aktionen.querySelector(".btn-primary").hidden = true;
    let wahl = null;
    const bw = h("button", { class: "wf-btn wahr", type: "button" }, h("span", { class: "gross", text: "👍" }), "Wahr", h("small", { text: "Taste W" }));
    const bf = h("button", { class: "wf-btn falsch-btn", type: "button" }, h("span", { class: "gross", text: "👎" }), "Falsch", h("small", { text: "Taste F" }));
    bw.onclick = () => { if (karte.fertig) return; wahl = true; senden(); };
    bf.onclick = () => { if (karte.fertig) return; wahl = false; senden(); };
    bereich.append(h("div", { class: "wf-buttons" }, bw, bf));
    antwortHolen = () => wahl;
    sperren = (ok) => {
      bw.disabled = bf.disabled = true;
      const gewaehlt = wahl ? bw : bf, anders = wahl ? bf : bw;
      gewaehlt.classList.add(ok ? "richtig" : "falsch");
      if (!ok) anders.classList.add("richtig");
    };
    karte.taste = (e) => {
      if (karte.fertig) return;
      if (e.key === "w" || e.key === "W" || e.key === "1") { e.preventDefault(); bw.click(); }
      if (e.key === "f" || e.key === "F" || e.key === "2") { e.preventDefault(); bf.click(); }
    };
  } else if (f.typ === "text" || f.typ === "ausdruck") {
    const inp = h("input", { class: "feld" + (f.typ === "ausdruck" ? " mono" : ""), type: "text", spellcheck: "false", autocomplete: "off",
      placeholder: f.typ === "ausdruck" ? "z. B. len(lst) - 1" : "Deine Antwort …", "aria-label": "Deine Antwort" });
    inp.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); if (!karte.fertig) senden(); } });
    if (f.typ === "ausdruck") {
      const gegeben = ausdruckBelegung(f);
      if (gegeben.length) {
        bereich.append(h("div", { class: "gegeben", style: { marginTop: 0, marginBottom: "14px" } }, h("span", { class: "lbl", text: "Gegeben:" }),
          gegeben.map(([k, v]) => h("code", { class: "ic", style: { fontSize: "15px" }, html: highlight(`${k} = ${v}`) }))));
      }
      bereich.append(h("div", { class: "ausdruck-eingabe" }, h("span", { class: "prompt", text: ">>>" }), inp));
      bereich.append(h("p", { class: "antwort-hinweis", text: "Schreibe einen einzigen Python-Ausdruck – er wird mit den gegebenen Variablen ausgewertet." + (f.muss_enthalten ? ` Er soll „${f.muss_enthalten}“ verwenden.` : "") }));
    } else {
      bereich.append(inp);
      bereich.append(h("p", { class: "antwort-hinweis", html: (f.gross_klein ? "<b>Groß-/Kleinschreibung zählt.</b>" : "Groß-/Kleinschreibung ist egal.") + " <kbd>Enter</kbd> prüft." }));
    }
    antwortHolen = () => inp.value;
    nachErgebnis = (r, endgueltig) => { inp.classList.toggle("nok", !r.ok); inp.classList.toggle("ok", !!r.ok); if (!endgueltig) inp.select(); };
    sperren = () => { inp.readOnly = true; };
    karte.fokus = () => inp.focus();
  } else if (f.typ === "ausgabe") {
    const ta = h("textarea", { class: "feld mono", rows: 3, spellcheck: "false", placeholder: "Was erscheint auf dem Bildschirm?", "aria-label": "Erwartete Ausgabe" });
    ta.addEventListener("keydown", (e) => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); if (!karte.fertig) senden(); } });
    bereich.append(ta, h("div", { class: "antwort-hinweis" },
      h("ul", null,
        h("li", { html: "Mehrere Ausgabezeilen? Schreibe jede in eine eigene Zeile (oder mit Leerzeichen getrennt)." }),
        h("li", { html: "Anführungszeichen von Strings erscheinen <b>nicht</b> in der Ausgabe." }),
        h("li", { html: "Gibt es einen Fehler? Schreibe seinen Namen, z. B. <code class=\"ic\">TypeError</code>. Gar keine Ausgabe? Schreibe <code class=\"ic\">nichts</code>." }),
        h("li", { html: "<kbd>Strg</kbd>+<kbd>Enter</kbd> prüft." }))));
    antwortHolen = () => ta.value;
    nachErgebnis = (r) => { ta.classList.toggle("nok", !r.ok); ta.classList.toggle("ok", !!r.ok); };
    sperren = () => { ta.readOnly = true; };
    karte.fokus = () => ta.focus();
  } else if (f.typ === "luecke") {
    const code = String(f.code || "");
    let k = 0;
    // Platzhalter aus Zeichen des privaten Unicode-Bereichs: Sie verschmelzen beim Hervorheben nicht
    // mit Nachbarn (früher wurde aus "0___" die Zahl "0__" und die Lücke verschwand).
    const PH = (i) => String.fromCharCode(0xE000 + i);
    const platzhalter = code.replace(/___/g, () => PH(k++));
    let html = highlight(platzhalter);
    const felder = [];
    for (let i = 0; i < k; i++) {
      html = html.replace(PH(i), `<input class="luecke-feld" data-i="${i}" type="text" spellcheck="false" autocomplete="off" aria-label="Lücke ${i + 1}" size="5">`);
    }
    const box = h("div", { class: "luecken-code", html });
    box.querySelectorAll("input").forEach((inp, i) => {
      felder[i] = inp;
      const breite = () => { inp.style.width = `${Math.max(5, inp.value.length + 2)}ch`; };
      inp.addEventListener("input", breite); breite();
      inp.addEventListener("keydown", (e) => {
        if (e.key === "Enter") { e.preventDefault(); if (i < felder.length - 1 && !felder[i + 1].value) felder[i + 1].focus(); else if (!karte.fertig) senden(); }
      });
    });
    bereich.append(box, h("p", { class: "antwort-hinweis", html: `Fülle ${k === 1 ? "die Lücke" : `alle ${k} Lücken`} aus. Groß-/Kleinschreibung zählt. <kbd>Enter</kbd> springt weiter bzw. prüft.` }));
    antwortHolen = () => (felder.some(x => !x.value.trim()) ? (toast("Bitte fülle alle Lücken aus."), undefined) : felder.map(x => x.value));
    nachErgebnis = (r) => {
      const det = Array.isArray(r.details) ? r.details : [];
      felder.forEach((x, i) => {
        const d = det[i];
        const ok = d && typeof d === "object" && "ok" in d ? d.ok : r.ok;
        x.classList.toggle("ok", !!ok); x.classList.toggle("nok", !ok);
      });
    };
    sperren = () => felder.forEach(x => { x.readOnly = true; });
    karte.fokus = () => felder[0] && felder[0].focus();
  } else if (f.typ === "puzzle") {
    const pz = puzzle(f);
    bereich.append(pz.el);
    antwortHolen = () => pz.ids();
    sperren = (ok) => pz.sperren(ok);
  } else {
    bereich.append(h("p", { class: "vis-fehler", text: `Unbekannter Fragetyp „${f.typ}“.` }));
  }

  karte.fokus = karte.fokus || (() => el.querySelector("button, input, textarea")?.focus());
  return karte;
}

function ausdruckBelegung(f) {
  // Server liefert "gegeben" als [[name, repr], ...] (repr von Python berechnet)
  if (typeof f.gegeben === "string") {
    return f.gegeben.split("\n").filter(z => z.trim()).map(z => { const i = z.indexOf("="); return i > 0 ? [z.slice(0, i).trim(), z.slice(i + 1).trim()] : [z, ""]; });
  }
  if (Array.isArray(f.gegeben)) return f.gegeben.map(x => (Array.isArray(x) ? [x[0], String(x[1])] : [x.name, String(x.repr ?? x.wert)]));
  const quelle = f.variablen || (Array.isArray(f.tests) && f.tests[0]) || null;
  if (!quelle || typeof quelle !== "object") return [];
  return Object.entries(quelle).map(([k, v]) => [k, pyRepr(v)]);
}

/* ------------------------------------------------------------------ Puzzle */
function puzzle(f) {
  const zeilen = (f.zeilen || f.bausteine || []).map((z, i) => {
    if (typeof z === "string") z = { text: z };
    const roh = String(z.text ?? z.code ?? "");
    const fuehrend = (roh.match(/^ */) || [""])[0].length;
    // engine liefert "einrueckung" in Leerzeichen
    const einzug = z.einzug ?? Math.round((z.einrueckung ?? fuehrend) / 4);
    return { id: z.zeilen_id ?? z.id ?? i, text: roh.trimStart(), einzug };
  });
  const quelle = h("div", { class: "puzzle-zone quelle", "aria-label": "Bausteine" });
  const ziel = h("div", { class: "puzzle-zone ziel", "aria-label": "Dein Programm" });
  const kopfQ = h("h4", null, h("span", { text: "🧱 Bausteine" }), h("span", { class: "zaehl" }));
  const kopfZ = h("h4", null, h("span", { text: "📝 Dein Programm" }), h("span", { class: "zaehl" }));
  quelle.append(kopfQ); ziel.append(kopfZ);
  let gesperrt = false;
  const el = h("div", null, h("div", { class: "puzzle" }, quelle, ziel),
    h("p", { class: "antwort-hinweis", html: "Ziehe die Bausteine in die richtige Reihenfolge – oder klicke sie an. Die Einrückung ist schon vorgegeben. Vorsicht: Manche Bausteine gehören nicht dazu! Tastatur: <kbd>Enter</kbd> verschiebt, <kbd>Alt</kbd>+<kbd>↑</kbd>/<kbd>↓</kbd> sortiert." }));

  const bausteine = new Map();
  let gezogen = null;
  const marke = h("div", { class: "drop-markierung" });

  function bauen(z) {
    const code = h("code");
    for (let i = 0; i < z.einzug; i++) code.append(h("span", { class: "einzug", "aria-hidden": "true" }));
    code.append(h("span", { html: highlight(z.text) }));
    const hoch = h("button", { type: "button", title: "nach oben", "aria-label": "nach oben", text: "↑" });
    const runter = h("button", { type: "button", title: "nach unten", "aria-label": "nach unten", text: "↓" });
    const wechsel = h("button", { type: "button" });
    const b = h("div", { class: "baustein", tabindex: "0", draggable: "true", role: "listitem", "data-id": z.id },
      h("span", { class: "griff", "aria-hidden": "true", text: "⋮⋮" }), code, h("span", { class: "bs-aktionen" }, hoch, runter, wechsel));
    b.setAttribute("aria-label", `${"    ".repeat(z.einzug)}${z.text}`.trim());
    hoch.onclick = (e) => { e.stopPropagation(); verschieben(b, -1); };
    runter.onclick = (e) => { e.stopPropagation(); verschieben(b, 1); };
    wechsel.onclick = (e) => { e.stopPropagation(); umsetzen(b); };
    b.addEventListener("click", () => umsetzen(b));
    b.addEventListener("keydown", (e) => {
      if (gesperrt) return;
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); umsetzen(b); b.focus(); }
      else if (e.altKey && e.key === "ArrowUp") { e.preventDefault(); verschieben(b, -1); b.focus(); }
      else if (e.altKey && e.key === "ArrowDown") { e.preventDefault(); verschieben(b, 1); b.focus(); }
      else if (e.key === "ArrowDown") { e.preventDefault(); (b.nextElementSibling?.classList.contains("baustein") ? b.nextElementSibling : null)?.focus(); }
      else if (e.key === "ArrowUp") { e.preventDefault(); (b.previousElementSibling?.classList.contains("baustein") ? b.previousElementSibling : null)?.focus(); }
    });
    b.addEventListener("dragstart", (e) => { if (gesperrt) { e.preventDefault(); return; } gezogen = b; b.classList.add("zieht"); e.dataTransfer.effectAllowed = "move"; e.dataTransfer.setData("text/plain", String(z.id)); });
    b.addEventListener("dragend", () => { b.classList.remove("zieht"); gezogen = null; marke.remove(); [quelle, ziel].forEach(x => x.classList.remove("drag-ueber")); aktualisieren(); });
    bausteine.set(String(z.id), b);
    return b;
  }

  function umsetzen(b) {
    if (gesperrt) return;
    (b.parentElement === quelle ? ziel : quelle).append(b);
    aktualisieren();
  }
  function verschieben(b, richtung) {
    if (gesperrt) return;
    if (richtung < 0) { const v = b.previousElementSibling; if (v && v.classList.contains("baustein")) v.before(b); }
    else { const n = b.nextElementSibling; if (n && n.classList.contains("baustein")) n.after(b); }
    aktualisieren();
  }
  function aktualisieren() {
    for (const [zone, kopf, leerText] of [[quelle, kopfQ, "Alle Bausteine verwendet."], [ziel, kopfZ, "Ziehe Bausteine hierher oder klicke sie an."]]) {
      const anzahl = zone.querySelectorAll(".baustein").length;
      kopf.querySelector(".zaehl").textContent = anzahl ? String(anzahl) : "";
      let leer = zone.querySelector(".zone-leer");
      if (!anzahl && !leer) zone.append(h("div", { class: "zone-leer", text: leerText }));
      if (anzahl && leer) leer.remove();
    }
    quelle.querySelectorAll(".baustein").forEach(b => { const w = b.querySelector(".bs-aktionen button:last-child"); w.textContent = "＋"; w.title = "ins Programm"; w.setAttribute("aria-label", "ins Programm übernehmen"); b.querySelectorAll(".bs-aktionen button:not(:last-child)").forEach(x => x.hidden = true); });
    ziel.querySelectorAll(".baustein").forEach(b => { const w = b.querySelector(".bs-aktionen button:last-child"); w.textContent = "✕"; w.title = "zurücklegen"; w.setAttribute("aria-label", "zurück zu den Bausteinen"); b.querySelectorAll(".bs-aktionen button:not(:last-child)").forEach(x => x.hidden = false); });
  }
  for (const zone of [quelle, ziel]) {
    zone.setAttribute("role", "list");
    zone.addEventListener("dragover", (e) => {
      if (!gezogen) return;
      e.preventDefault();
      zone.classList.add("drag-ueber");
      const nach = [...zone.querySelectorAll(".baustein:not(.zieht)")].find(b => { const r = b.getBoundingClientRect(); return e.clientY < r.top + r.height / 2; });
      if (nach) nach.before(marke); else zone.append(marke);
    });
    zone.addEventListener("dragleave", (e) => { if (!zone.contains(e.relatedTarget)) { zone.classList.remove("drag-ueber"); } });
    zone.addEventListener("drop", (e) => {
      e.preventDefault();
      if (!gezogen) return;
      if (marke.parentElement === zone) marke.replaceWith(gezogen); else zone.append(gezogen);
      zone.classList.remove("drag-ueber");
      aktualisieren();
    });
  }
  zeilen.forEach(z => quelle.append(bauen(z)));
  aktualisieren();
  return {
    el,
    ids: () => [...ziel.querySelectorAll(".baustein")].map(b => { const id = b.dataset.id; return /^\d+$/.test(id) && typeof zeilen[0]?.id === "number" ? Number(id) : id; }),
    sperren: (ok) => { gesperrt = true; el.querySelectorAll(".baustein").forEach(b => { b.draggable = false; b.classList.add(ok ? "ok" : "nok"); b.querySelector(".bs-aktionen").hidden = true; }); },
  };
}

/* ------------------------------------------------------------ Code-Aufgabe */
function anforderungsChips(f) {
  const chips = [];
  for (const v of f.verboten || []) chips.push(h("span", { class: "chip rot", title: "Darf im Code nicht vorkommen" }, "🚫 nicht erlaubt: ", h("code", { text: v })));
  for (const p of f.pflicht || []) chips.push(h("span", { class: "chip gruen", title: "Muss im Code vorkommen" }, "✅ muss vorkommen: ", h("code", { text: p.trim() })));
  if (f.rekursiv) chips.push(h("span", { class: "chip primary", title: "Die Funktion muss sich selbst aufrufen" }, "🔁 rekursiv: ", h("code", { text: String(f.rekursiv).split("|").map(n => n.trim() + "()").join(" oder ") })));
  for (const r of f.regeln || []) chips.push(h("span", { class: "chip", title: "Regel – wird automatisch geprüft" }, "📏 " + r));
  if (f.genaue_ausgabe) chips.push(h("span", { class: "chip", title: "Die Ausgabe wird genau verglichen" }, "🔤 Ausgabe genau: Groß-/Kleinschreibung und Satzzeichen zählen"));
  const n = f.anzahl_tests ?? (Array.isArray(f.tests) ? f.tests.length : null);
  if (n) chips.push(h("span", { class: "chip", text: `🧪 ${n} automatische Test${n === 1 ? "" : "s"}` }));
  return chips.length ? h("div", { class: "anforderungen" }, chips) : null;
}

function zuText(x) {
  if (x === null || x === undefined) return "";
  if (Array.isArray(x)) return x.map(String).join("\n");
  return String(x);
}

function diffAnsicht(erwartet, ausgabe) {
  const eZ = zuText(erwartet).replace(/\n$/, "").split("\n");
  // Engine schreibt manchmal eine Überschrift wie "Genau diese Zeilen:" voran
  let erwLabel = null;
  if (eZ.length > 1 && /^[A-ZÄÖÜa-zäöü][^"'()=]*:$/.test(eZ[0].trim())) erwLabel = eZ.shift().trim().replace(/:$/, "");
  const aZ = zuText(ausgabe).replace(/\n$/, "").split("\n");
  const preE = h("pre"), preA = h("pre");
  const zeile = (text, anders, mark) => {
    const s = h("span", { class: "dz" + (anders ? " anders" : "") });
    if (!text) { s.append(h("span", { class: "leerzeile", text: "(leere Zeile)" })); return s; }
    if (mark) {
      const [a, b] = mark;
      s.append(text.slice(0, a)); if (b > a) s.append(h("mark", { text: text.slice(a, b) })); s.append(text.slice(b));
    } else s.append(text);
    return s;
  };
  const exakt = eZ.length === aZ.length;
  if (exakt) {
    eZ.forEach((e, i) => {
      const a = aZ[i];
      if (e === a) { preE.append(zeile(e, false)); preA.append(zeile(a, false)); return; }
      let p = 0; while (p < e.length && p < a.length && e[p] === a[p]) p++;
      let s = 0; while (s < e.length - p && s < a.length - p && e[e.length - 1 - s] === a[a.length - 1 - s]) s++;
      preE.append(zeile(e, true, [p, e.length - s])); preA.append(zeile(a, true, [p, a.length - s]));
    });
  } else {
    eZ.forEach(e => {
      const gefunden = aZ.some(a => a.trimEnd().endsWith(e.trim()));
      preE.append(zeile(e, !gefunden, null));
    });
    aZ.forEach(a => preA.append(zeile(a, false)));
  }
  if (!zuText(ausgabe)) preA.replaceChildren(h("span", { class: "leerzeile", text: "(keine Ausgabe)" }));
  return h("div", { class: "diff" },
    h("div", { class: "erw" }, h("div", { class: "lbl", text: erwLabel ? `Erwartet – ${erwLabel}` : exakt ? "Erwartet" : "Erwartet (Zeilen sollen so enden)" }), preE),
    h("div", null, h("div", { class: "lbl", text: "Deine Ausgabe" }), preA));
}

function testsListe(details) {
  const tests = (details || []).filter(d => d && typeof d === "object");
  const bestanden = tests.filter(t => t.ok).length;
  const wrap = h("div", { class: "tests-liste" });
  if (!tests.length) return wrap;
  wrap.append(h("div", { class: "tests-kopf" }, h("span", { text: `${bestanden} von ${tests.length} Tests bestanden` }), balken(bestanden / tests.length, "gruen")));
  let ersterFehler = true;
  tests.forEach((t, i) => {
    const offen = !t.ok && ersterFehler;
    if (!t.ok) ersterFehler = false;
    const det = h("div", { class: "test-details" });
    if (t.meldung) det.append(h("div", { class: "test-meldung", html: inline(t.meldung).replace(/\n/g, "<br>") }));
    const eing = t.eingaben;
    if (eing && (Array.isArray(eing) ? eing.length : String(eing).trim())) {
      det.append(h("div", { class: "test-eingaben" }, "⌨️ Eingaben:", (Array.isArray(eing) ? eing : String(eing).split("\n")).map(x => h("code", { class: "ic", text: String(x) }))));
    }
    if (!t.ok && (t.erwartet !== undefined && t.erwartet !== null) && t.ausgabe !== undefined) det.append(diffAnsicht(t.erwartet, t.ausgabe));
    else if (t.ausgabe) det.append(h("div", { class: "diff" }, h("div", null, h("div", { class: "lbl", text: "Deine Ausgabe" }), h("pre", { text: zuText(t.ausgabe) }))));
    if (t.fehler_erklaert) det.append(fehlerKarte({ text: t.fehler || "Fehler", erklaert: t.fehler_erklaert }));
    const kopf = h("button", { class: "test-kopf", type: "button", "aria-expanded": offen ? "true" : "false" },
      h("span", { class: "st", "aria-hidden": "true", text: t.ok ? "✓" : "✗" }),
      h("span", { text: t.name || `Test ${i + 1}` }), h("span", { class: "sr-only", text: t.ok ? "bestanden" : "nicht bestanden" }),
      h("span", { class: "pfeil", text: "▶" }));
    const item = h("div", { class: "test " + (t.ok ? "ok" : "nok") + (offen ? " offen" : ""), style: { animationDelay: `${i * 0.05}s` } }, kopf, det);
    kopf.onclick = () => { item.classList.toggle("offen"); kopf.setAttribute("aria-expanded", item.classList.contains("offen") ? "true" : "false"); };
    wrap.append(item);
  });
  return wrap;
}

export function codeAufgabe(f, opts = {}) {
  const karte = { el: null, fertig: false };
  const vorlage = f.vorlage ?? "";
  const startCode = f.entwurf ?? vorlage;
  const el = h("article", { class: "karte frage-karte aufgabe-karte", "aria-label": "Programmieraufgabe", "data-id": f.id, "data-typ": "code" });
  karte.el = el;
  aktiveKarte = karte;
  el.append(h("div", { class: "frage-kopf" },
    h("span", { class: "frage-typ" }, h("span", { text: "💻" }), f.art && /fehler/i.test(f.art) ? f.art : "Programmieraufgabe"),
    h("span", { class: "rechts" }, opts.kontext ? h("span", { class: "chip", text: opts.kontext }) : null, f.entwurf && f.entwurf !== vorlage ? h("span", { class: "chip", text: "📝 Entwurf geladen" }) : null)));
  el.append(frageTextElement(f));
  const chips = anforderungsChips(f);
  if (chips) el.append(chips);

  const speichern = debounce(async (code) => {
    try { await api.post("/api/entwurf", { id: f.id, code }); editor.setzeGespeichert("✓ Entwurf gespeichert"); }
    catch { editor.setzeGespeichert("Entwurf nicht gespeichert"); }
  }, 1200);
  const eingabe = eingabenFeld([], { sichtbar: brauchtEingabe(startCode) });
  const editor = new Editor({
    wert: startCode, minZeilen: Math.max(8, startCode.split("\n").length + 2), label: "Dein Code",
    onChange: (code) => { editor.setzeGespeichert("…"); speichern(code); eingabe.el.hidden = !brauchtEingabe(code); },
    onStrgEnter: () => pruefen(),
  });
  el.append(h("div", { style: { marginTop: "16px" } }, editor.el), eingabe.el);
  eingabe.el.style.borderRadius = "0 0 12px 12px";

  const bAus = h("button", { class: "btn", type: "button" }, h("span", { class: "ico", text: "▶" }), "Ausführen");
  const bPruef = h("button", { class: "btn btn-primary", type: "button", title: "Strg+Enter" }, h("span", { class: "ico", text: "✓" }), "Prüfen");
  const bTrace = h("button", { class: "btn", type: "button" }, h("span", { class: "ico", text: "👣" }), "Schritt für Schritt");
  const tipps = tippBereich(tippsVon(f));
  const bLoesung = h("button", { class: "btn btn-ghost", type: "button", text: "👀 Lösung zeigen" });
  const bReset = h("button", { class: "btn btn-ghost", type: "button", text: "↺ Zurücksetzen", title: "Vorlage wiederherstellen" });
  el.append(h("div", { class: "code-aufgabe-werkzeuge" }, bAus, bTrace, bPruef, h("span", { class: "spacer" }), tipps.btn, bLoesung, bReset));
  const ausgabeSlot = h("div", { style: { marginTop: "12px" } });
  const traceSlot = h("div", { style: { marginTop: "12px" } });
  const testSlot = h("div");
  const fbSlot = h("div");
  const loesungSlot = h("div");
  el.append(tipps.liste, ausgabeSlot, traceSlot, testSlot, fbSlot, loesungSlot);

  let loesungGesehen = false;
  let geloest = false;

  bAus.onclick = () => { traceSlot.replaceChildren(); ausfuehren(editor.wert, eingabe.werte(), ausgabeSlot); };
  bTrace.onclick = () => {
    ausgabeSlot.replaceChildren();
    traceSlot.replaceChildren(tracerPanel(editor.wert, eingabe.werte(), { onSchliessen: () => traceSlot.replaceChildren() }));
  };
  bReset.onclick = async () => {
    if (editor.wert !== vorlage && !(await bestaetigen("Code zurücksetzen?", "Dein bisheriger Code wird durch die Vorlage ersetzt.", "Zurücksetzen"))) return;
    editor.wert = vorlage; speichern(vorlage); editor.fokus();
  };
  bLoesung.onclick = async () => {
    if (!loesungGesehen && !geloest) {
      const ja = await bestaetigen("Lösung ansehen?", "Probier es ruhig noch ein bisschen – Fehler gehören zum Lernen! Wenn du die Lösung jetzt ansiehst, zählt die Aufgabe **nicht** als selbst gelöst. Du kannst sie später in der Fehlerkiste wiederholen.", "Lösung zeigen", "Weiter probieren", "👀");
      if (!ja) return;
    }
    try {
      const r = await api.post("/api/loesung", { id: f.id });
      loesungGesehen = true;
      if (r.statistik) setStatistik(r.statistik);
      const uebernehmen = h("button", { class: "btn btn-sm", type: "button", text: "In den Editor übernehmen" });
      uebernehmen.onclick = async () => {
        if (await bestaetigen("Lösung übernehmen?", "Dein Code im Editor wird ersetzt.", "Übernehmen")) { editor.wert = r.loesung; speichern(r.loesung); }
      };
      const erk = erklaerungElement(r);
      loesungSlot.replaceChildren(h("div", { class: "loesung-box" },
        h("div", { class: "lbl" }, "👀 Musterlösung", h("span", { class: "spacer" }), uebernehmen),
        codeAnzeige(r.loesung || "", { nummern: true }), erk ? h("div", { style: { marginTop: "10px" } }, erk) : null,
        h("p", { class: "antwort-hinweis", text: "Tipp: Schließe die Lösung, tippe sie selbst ab und lass sie prüfen – so bleibt mehr hängen." })));
      if (!geloest && opts.onFertig) opts.onFertig({ ok: false, loesungAngesehen: true });
    } catch (e) { toast(e.message, "rot"); }
  };

  async function pruefen() {
    bPruef.disabled = true;
    const altText = bPruef.lastChild.textContent;
    bPruef.lastChild.textContent = "Wird geprüft …";
    testSlot.replaceChildren();
    let r;
    try { r = await api.post("/api/code/pruefen", { id: f.id, code: editor.wert }); }
    catch (e) { toast(e.message, "rot"); return; }
    finally { bPruef.disabled = false; bPruef.lastChild.textContent = altText; }
    setStatistik(r.statistik);
    editor.setzeGespeichert("✓ Entwurf gespeichert");
    testSlot.append(testsListe(r.details));
    if (r.ok) {
      geloest = true;
      xpFlug(r.xp_neu);
      fbSlot.replaceChildren(feedbackBox("ok", { titel: loesungGesehen ? "Alle Tests bestanden (mit Lösung angesehen)" : "Alle Tests bestanden! 🎉", meldung: r.meldung, hinweis: r.hinweis, ergebnis: r, xp: r.xp_neu }));
      if (opts.onFertig) opts.onFertig({ ok: !loesungGesehen, loesungAngesehen: loesungGesehen, ergebnis: r });
    } else {
      fbSlot.replaceChildren(feedbackBox("nochmal", { titel: "Noch nicht ganz – schau dir die Tests an", meldung: r.meldung, hinweis: r.hinweis }));
      if (!reduziert()) { el.classList.remove("wackeln"); void el.offsetWidth; el.classList.add("wackeln"); }
    }
  }
  bPruef.onclick = pruefen;
  karte.fokus = () => editor.fokus();
  return karte;
}

export { esc };
