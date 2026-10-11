// Eingabe-Pad: Textfeld + Mathe-Tasten + Live-Vorschau ("So verstehe ich deine Eingabe").
// Die Vorschau kommt vom Server (derselbe Parser wie beim Prüfen) -> keine Überraschungen.
import { h, debounce, lokal } from "./util.js";
import { api } from "./api.js";
import { texHtml } from "./formel.js";

// [Beschriftung (LaTeX oder Text), einzufügender Text, Cursor-Versatz vom Ende (für Klammern)]
const T = {
  bruch: ["\\frac{□}{□}", "()/()", 4, "Bruch"], hoch2: ["x^2", "^2", 0, "hoch 2"], hoch: ["x^{□}", "^", 0, "hoch"],
  wurzel: ["\\sqrt{□}", "sqrt()", 1, "Wurzel"], pi: ["\\pi", "π", 0, "pi"], mal: ["\\cdot", "·", 0, "mal"],
  geteilt: [":", ":", 0, "geteilt"], minus: ["-", "-", 0, "minus"], klammer: ["(\\,)", "()", 1, "Klammer"],
  betrag: ["|\\,|", "||", 1, "Betrag"], e: ["\\mathrm{e}", "e", 0, "Eulersche Zahl"], komma: [",", ",", 0, "Komma"],
  le: ["\\le", "≤", 0, "kleiner gleich"], ge: ["\\ge", "≥", 0, "größer gleich"], lt: ["<", "<", 0, "kleiner"],
  gt: [">", ">", 0, "größer"], ne: ["\\neq", "≠", 0, "ungleich"], menge: ["\\{\\,\\}", "{}", 1, "Mengenklammer"],
  semi: [";", "; ", 0, "Trenner"], leer: ["\\emptyset", "{}", 0, "leere Menge"], inf: ["\\infty", "∞", 0, "unendlich"],
  minf: ["-\\infty", "-∞", 0, "minus unendlich"], vereinigt: ["\\cup", " ∪ ", 0, "vereinigt"], geschnitten: ["\\cap", " ∩ ", 0, "geschnitten"],
  r: ["\\mathbb{R}", "ℝ", 0, "alle reellen Zahlen"], eckauf: ["[", "[", 0, "eckige Klammer auf"], eckzu: ["]", "]", 0, "eckige Klammer zu"],
  rundauf: ["(", "(", 0, "runde Klammer auf"], rundzu: [")", ")", 0, "runde Klammer zu"], fak: ["n!", "!", 0, "Fakultät"],
  ln: ["\\ln", "ln()", 1, "ln"], log2: ["\\log_2", "log2()", 1, "log zur Basis 2"], sin: ["\\sin", "sin()", 1, "Sinus"],
  cos: ["\\cos", "cos()", 1, "Kosinus"], keine: ["\\text{keine}", "keine", 0, "keine Lösung"],
};

const LAYOUT = {
  zahl: ["bruch", "minus", "klammer", "hoch2", "hoch", "wurzel", "pi", "mal", "komma"],
  term: ["bruch", "klammer", "hoch2", "hoch", "wurzel", "mal", "minus", "betrag", "pi", "e"],
  bereich: ["menge", "semi", "eckauf", "eckzu", "rundauf", "rundzu", "inf", "minf", "vereinigt", "lt", "le", "gt", "ge", "r", "keine", "bruch", "wurzel"],
  menge: ["menge", "semi", "leer", "vereinigt", "geschnitten", "rundauf", "rundzu", "bruch", "minus"],
  zelle: ["bruch", "minus", "wurzel", "hoch"],
};

/** Fügt text an der Cursorposition ein. zurueck = wie viele Zeichen der Cursor vom Ende zurückspringt. */
export function einfuegen(inp, text, zurueck = 0) {
  const a = inp.selectionStart ?? inp.value.length, b = inp.selectionEnd ?? inp.value.length;
  const markiert = inp.value.slice(a, b);
  let neu = text;
  if (markiert && zurueck > 0) {           // Markierung in die Klammer/den Bruch übernehmen
    const pos = text.length - zurueck;
    neu = text.slice(0, pos) + markiert + text.slice(pos);
  }
  inp.value = inp.value.slice(0, a) + neu + inp.value.slice(b);
  const cursor = a + neu.length - (markiert ? 0 : zurueck);
  inp.focus();
  inp.setSelectionRange(cursor, cursor);
  inp.dispatchEvent(new Event("input", { bubbles: true }));
}

function padTasten(inp, modus, variablen = []) {
  const namen = [...(LAYOUT[modus] || LAYOUT.term)];
  const tasten = namen.map(n => {
    const [tex, text, zurueck, label] = T[n];
    return h("button", { class: "pad-taste", type: "button", "aria-label": label, title: label, html: texHtml(tex),
      onmousedown: (e) => e.preventDefault(), onclick: () => einfuegen(inp, text, zurueck) });
  });
  for (const v of variablen.slice(0, 4)) {
    tasten.unshift(h("button", { class: "pad-taste var", type: "button", "aria-label": `Variable ${v}`, html: texHtml(v),
      onmousedown: (e) => e.preventDefault(), onclick: () => einfuegen(inp, v) }));
  }
  tasten.push(h("button", { class: "pad-taste weg", type: "button", "aria-label": "Zeichen löschen", text: "⌫",
    onmousedown: (e) => e.preventDefault(), onclick: () => {
      const a = inp.selectionStart, b = inp.selectionEnd;
      if (a === b && a > 0) { inp.value = inp.value.slice(0, a - 1) + inp.value.slice(b); inp.setSelectionRange(a - 1, a - 1); }
      else { inp.value = inp.value.slice(0, a) + inp.value.slice(b); inp.setSelectionRange(a, a); }
      inp.focus(); inp.dispatchEvent(new Event("input", { bubbles: true }));
    } }));
  return h("div", { class: "pad", role: "group", "aria-label": "Mathe-Tasten" }, tasten);
}

const PLATZHALTER = {
  zahl: "z. B. 3/4 oder -2,5", term: "z. B. 2x + 3 oder (x+1)^2", bereich: "z. B. {2; -3}  oder  [0; 4)  oder  x < 2",
  menge: "z. B. {1; 2; 3}", text: "Deine Antwort …",
};
const VORSCHAU_TYP = { zahl: "zahl", term: "term", bereich: "bereich", menge: "menge", zelle: "zahl" };

/**
 * Eingabefeld mit Pad und Vorschau.
 * opts: {modus: "zahl"|"term"|"bereich"|"menge"|"text", variablen, einheit, onEnter, wert, label}
 */
export function eingabeFeld(opts = {}) {
  const modus = opts.modus || "term";
  const inp = h("input", { class: "feld formel-eingabe", type: "text", spellcheck: "false", autocomplete: "off", autocapitalize: "off",
    inputmode: "text", placeholder: PLATZHALTER[modus] || "", "aria-label": opts.label || "Deine Antwort" });
  if (opts.wert) inp.value = opts.wert;
  const vorschau = h("div", { class: "vorschau", "aria-live": "polite" });
  const zeile = h("div", { class: "eingabe-zeile" }, inp, opts.einheit ? h("span", { class: "einheit", text: opts.einheit }) : null);
  const el = h("div", { class: "eingabe" }, zeile);
  let pad = null;
  if (modus !== "text") {
    pad = padTasten(inp, modus, opts.variablen || []);
    const offen = lokal.get("pad_offen", true);
    pad.hidden = !offen;
    const schalter = h("button", { class: "btn btn-sm btn-ghost pad-schalter", type: "button", "aria-expanded": String(offen), text: offen ? "▾ Mathe-Tasten ausblenden" : "▸ Mathe-Tasten zeigen" });
    schalter.onclick = () => {
      pad.hidden = !pad.hidden;
      lokal.set("pad_offen", !pad.hidden);
      schalter.textContent = pad.hidden ? "▸ Mathe-Tasten zeigen" : "▾ Mathe-Tasten ausblenden";
      schalter.setAttribute("aria-expanded", String(!pad.hidden));
    };
    el.append(vorschau, h("div", { class: "pad-kopf" }, schalter), pad);
  }
  let zaehler = 0;
  const aktualisieren = debounce(async () => {
    if (modus === "text") return;
    const text = inp.value;
    const nr = ++zaehler;
    if (!text.trim()) { vorschau.replaceChildren(); vorschau.className = "vorschau"; return; }
    try {
      const r = await api.post("/api/term/vorschau", { text, typ: VORSCHAU_TYP[modus] || "term", variablen: opts.variablen || null });
      if (nr !== zaehler) return;
      if (r.fehler) {
        vorschau.className = "vorschau fehler";
        vorschau.replaceChildren(h("span", { class: "v-lbl", text: "Noch nicht lesbar:" }), h("span", { text: r.fehler }));
      } else {
        vorschau.className = "vorschau ok";
        vorschau.replaceChildren(h("span", { class: "v-lbl", text: "So verstehe ich das:" }), h("span", { class: "v-formel", html: texHtml("\\displaystyle " + (r.latex || "")) }));
      }
    } catch { /* Vorschau ist nur eine Hilfe */ }
  }, 220);
  inp.addEventListener("input", () => { aktualisieren(); opts.onInput && opts.onInput(inp.value); });
  inp.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.ctrlKey && !e.metaKey) { e.preventDefault(); opts.onEnter && opts.onEnter(); }
  });
  if (inp.value) aktualisieren();
  return {
    el, inp,
    wert: () => inp.value,
    fokus: () => inp.focus({ preventScroll: true }),
    sperren: (ok) => { inp.readOnly = true; inp.classList.add(ok ? "ok" : "nok"); if (pad) pad.hidden = true; el.querySelector(".pad-kopf")?.remove(); },
    markieren: (ok) => { inp.classList.toggle("ok", ok); inp.classList.toggle("nok", !ok); },
  };
}

/** Gitter aus Zellen (Vektor / Matrix / LGS). */
export function zellenGitter({ zeilen, spalten = 1, namen = null, onEnter, parameter = false }) {
  const felder = [];
  const tabelle = h("div", { class: "gitter-feld" + (spalten === 1 ? " vektor" : ""), style: { gridTemplateColumns: `repeat(${spalten}, minmax(64px, 110px))` } });
  for (let i = 0; i < zeilen; i++) {
    felder.push([]);
    for (let j = 0; j < spalten; j++) {
      const inp = h("input", { class: "feld zelle", type: "text", spellcheck: "false", autocomplete: "off",
        "aria-label": namen ? namen[i] : `Zeile ${i + 1}, Spalte ${j + 1}`, placeholder: namen ? namen[i] : "" });
      inp.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
          e.preventDefault();
          const naechste = felder.flat()[felder.flat().indexOf(inp) + 1];
          if (naechste && !naechste.value) naechste.focus(); else onEnter && onEnter();
        }
      });
      felder[i].push(inp);
      tabelle.append(inp);
    }
  }
  const klammer = h("div", { class: "gitter-klammer" }, tabelle);
  const pad = h("div", { class: "pad klein" }, [...(parameter ? ["t", "s"] : []), "bruch", "minus", "wurzel"].map(n => {
    const [tex, text, zurueck, label] = T[n] || [n, n, 0, `Parameter ${n}`];
    return h("button", { class: "pad-taste", type: "button", "aria-label": label, html: texHtml(tex), onmousedown: (e) => e.preventDefault(),
      onclick: () => { const ziel = felder.flat().find(f => f === document.activeElement) || felder.flat().find(f => !f.value) || felder[0][0]; einfuegen(ziel, text, zurueck); } });
  }));
  return {
    el: h("div", { class: "gitter-eingabe" }, klammer, pad),
    felder,
    werte: () => (spalten === 1 ? felder.map(z => z[0].value) : felder.map(z => z.map(f => f.value))),
    fokus: () => felder[0][0].focus({ preventScroll: true }),
    markieren: (details) => {
      (details || []).forEach((d, k) => {
        const f = d.pos ? felder[d.pos[0]][d.pos[1]] : felder.flat()[k];
        if (f && "ok" in d) { f.classList.toggle("ok", d.ok); f.classList.toggle("nok", !d.ok); }
      });
    },
    sperren: () => { felder.flat().forEach(f => { f.readOnly = true; }); pad.hidden = true; },
  };
}
