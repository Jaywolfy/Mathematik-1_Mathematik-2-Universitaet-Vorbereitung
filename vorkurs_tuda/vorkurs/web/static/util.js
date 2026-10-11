// Kleine Helfer für DOM, Escaping, Inline-Markup, Dialoge, Toasts, Konfetti.

export const reduziert = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/** Element erzeugen: h("div", {class: "x", onclick: fn, text: "..."}, kind1, kind2) */
export function h(tag, attrs = null, ...kinder) {
  const el = tag.includes(":")
    ? document.createElementNS("http://www.w3.org/2000/svg", tag.split(":")[1])
    : document.createElement(tag);
  if (attrs) {
    for (const [k, v] of Object.entries(attrs)) {
      if (v === undefined || v === null || v === false) continue;
      if (k === "class") el.setAttribute("class", v);
      else if (k === "text") el.textContent = v;
      else if (k === "html") el.innerHTML = v;
      else if (k === "style" && typeof v === "object") Object.assign(el.style, v);
      else if (k.startsWith("on") && typeof v === "function") el.addEventListener(k.slice(2), v);
      else if (v === true) el.setAttribute(k, "");
      else el.setAttribute(k, v);
    }
  }
  anhaengen(el, kinder);
  return el;
}

function anhaengen(el, kinder) {
  for (const k of kinder) {
    if (k === null || k === undefined || k === false) continue;
    if (Array.isArray(k)) anhaengen(el, k);
    else if (k instanceof Node) el.append(k);
    else el.append(document.createTextNode(String(k)));
  }
}

export const svg = (tag, attrs, ...kinder) => h("svg:" + tag, attrs, ...kinder);

export function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

/** Inline-Markup: erst HTML-escapen, dann `code` und **fett**. */
export function inline(text) {
  const teile = String(text ?? "").split("`");
  let html = "";
  teile.forEach((teil, i) => {
    if (i % 2 === 1 && i < teile.length - 1) {
      html += `<code class="ic">${esc(teil)}</code>`;
    } else {
      let t = esc(i % 2 === 1 ? "`" + teil : teil);
      t = t.replace(/(?<![\w*])\*\*(?=\S)(.+?)(?<=\S)\*\*(?![\w*])/g, "<strong>$1</strong>");  // wie markup.INLINE_FETT_RE
      t = t.replace(/(?<![\w*])\*(?=[^\s*`])([^*`\n]*?[^\s*`])\*(?![\w*])/g, "<em>$1</em>");   // wie markup.INLINE_KURSIV_RE
      html += t;
    }
  });
  return html;
}

/** Mehrzeiliger Text mit Inline-Markup -> Absätze (Leerzeile trennt). */
export function inlineAbsaetze(text) {
  const absaetze = String(text ?? "").trim().split(/\n\s*\n/);
  return absaetze.map(a => `<p>${inline(a).replace(/\n/g, "<br>")}</p>`).join("");
}

export const $ = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

export function debounce(fn, ms) {
  let t;
  const f = (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
  f.sofort = (...a) => { clearTimeout(t); fn(...a); };
  return f;
}

export function leeren(el) { while (el.firstChild) el.removeChild(el.firstChild); return el; }

export function lade(text = "Wird geladen …") {
  return h("div", { class: "lade", role: "status" }, h("span", { class: "spinner" }), text);
}

/* ---------- Fortschrittsring ---------- */
export function ring(anteil, { groesse = 26, dicke = 3.5, text = null, fertig = false, label = null } = {}) {
  const r = (groesse - dicke) / 2;
  const u = 2 * Math.PI * r;
  const a = Math.max(0, Math.min(1, anteil || 0));
  const s = svg("svg", {
    class: "ring" + (fertig ? " fertig" : ""), width: groesse, height: groesse, viewBox: `0 0 ${groesse} ${groesse}`,
    role: "img", "aria-label": label || `${Math.round(a * 100)} Prozent`,
  });
  s.append(svg("circle", { class: "ring-bg", cx: groesse / 2, cy: groesse / 2, r, "stroke-width": dicke }));
  const fg = svg("circle", {
    class: "ring-fg", cx: groesse / 2, cy: groesse / 2, r, "stroke-width": dicke,
    "stroke-dasharray": u, "stroke-dashoffset": u, transform: `rotate(-90 ${groesse / 2} ${groesse / 2})`,
  });
  s.append(fg);
  requestAnimationFrame(() => requestAnimationFrame(() => fg.setAttribute("stroke-dashoffset", u * (1 - a))));
  if (fertig && !text) {
    const c = groesse / 2;
    s.append(svg("path", {
      d: `M${c - groesse * 0.17} ${c + groesse * 0.01} l${groesse * 0.11} ${groesse * 0.11} l${groesse * 0.22} -${groesse * 0.22}`,
      fill: "none", style: "stroke:var(--success-strong)", "stroke-width": Math.max(2, dicke * 0.8), "stroke-linecap": "round", "stroke-linejoin": "round",
    }));
  } else if (text !== null) {
    s.append(svg("text", { x: groesse / 2, y: groesse / 2 + 0.5, "font-size": groesse * 0.26 }, text));
  }
  return s;
}

export function balken(anteil, extraKlasse = "") {
  const i = h("i");
  const b = h("div", { class: "balken " + extraKlasse, role: "progressbar", "aria-valuemin": 0, "aria-valuemax": 100, "aria-valuenow": Math.round((anteil || 0) * 100) }, i);
  requestAnimationFrame(() => requestAnimationFrame(() => { i.style.width = `${Math.max(0, Math.min(1, anteil || 0)) * 100}%`; }));
  return b;
}

/* ---------- Toasts ---------- */
let toastBox = null;
export function toast(text, art = "") {
  if (!toastBox) { toastBox = h("div", { class: "toasts", role: "status", "aria-live": "polite" }); document.body.append(toastBox); }
  const t = h("div", { class: "toast " + art, text });
  toastBox.append(t);
  setTimeout(() => t.remove(), 3200);
}

/* ---------- Dialog ---------- */
export function dialog({ titel, text = "", inhalt = null, knoepfe = [{ text: "OK", wert: true, klasse: "btn-primary" }], icon = "" }) {
  return new Promise(resolve => {
    const vorher = document.activeElement;
    const hg = h("div", { class: "dialog-hg" });
    const box = h("div", { class: "dialog", role: "dialog", "aria-modal": "true", "aria-labelledby": "dlg-titel" },
      h("h2", { id: "dlg-titel" }, icon ? h("span", { text: icon }) : null, titel),
      text ? h("p", { class: "d-text", html: inline(text) }) : null,
      inhalt ? h("div", { class: "d-inhalt" }, inhalt) : null,
      h("div", { class: "d-aktionen" }, knoepfe.map(k => h("button", {
        class: "btn " + (k.klasse || ""), text: k.text, onclick: () => schliessen(k.wert),
      }))));
    hg.append(box);
    const schliessen = (wert) => {
      hg.remove();
      document.removeEventListener("keydown", taste, true);
      if (vorher && vorher.focus) vorher.focus();
      resolve(wert);
    };
    const taste = (e) => {
      if (e.key === "Escape") { e.preventDefault(); schliessen(null); }
      if (e.key === "Tab") {
        const f = [...box.querySelectorAll("button, input, select, textarea, [tabindex]")].filter(x => !x.disabled);
        if (!f.length) return;
        const i = f.indexOf(document.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
      }
    };
    hg.addEventListener("click", e => { if (e.target === hg) schliessen(null); });
    document.addEventListener("keydown", taste, true);
    document.body.append(hg);
    const btns = box.querySelectorAll(".d-aktionen button");
    (btns[btns.length - 1] || box).focus();
  });
}

export function bestaetigen(titel, text, ja = "Ja", nein = "Abbrechen", icon = "") {
  return dialog({ titel, text, icon, knoepfe: [
    { text: nein, wert: false, klasse: "btn-ghost" },
    { text: ja, wert: true, klasse: "btn-primary" },
  ] }).then(Boolean);
}

/* ---------- Konfetti (dezent) ---------- */
export function konfetti(anzahl = 70) {
  if (reduziert()) return;
  const farben = ["#4f46e5", "#8b5cf6", "#db2777", "#f59e0b", "#10b981", "#0ea5e9"];
  const box = h("div", { class: "konfetti", "aria-hidden": "true" });
  for (let i = 0; i < anzahl; i++) {
    const s = h("i");
    s.style.left = Math.random() * 100 + "vw";
    s.style.background = farben[i % farben.length];
    s.style.setProperty("--x", (Math.random() * 30 - 15) + "vw");
    s.style.setProperty("--r", (Math.random() * 900 - 450) + "deg");
    s.style.setProperty("--d", (2 + Math.random() * 1.8) + "s");
    s.style.animationDelay = (Math.random() * 0.5) + "s";
    if (i % 3 === 0) { s.style.width = "7px"; s.style.height = "7px"; s.style.borderRadius = "50%"; }
    box.append(s);
  }
  document.body.append(box);
  setTimeout(() => box.remove(), 4500);
}

/* ---------- Zahl hochzählen ---------- */
export function zaehleHoch(el, von, bis, ms = 900) {
  if (reduziert() || von === bis) { el.textContent = bis; return; }
  const t0 = performance.now();
  const schritt = (t) => {
    const p = Math.min(1, (t - t0) / ms);
    const e = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(von + (bis - von) * e);
    if (p < 1) requestAnimationFrame(schritt);
  };
  requestAnimationFrame(schritt);
}

export function kopieren(text) {
  if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
  const t = h("textarea", { style: { position: "fixed", opacity: "0" } });
  t.value = text; document.body.append(t); t.select();
  try { document.execCommand("copy"); } finally { t.remove(); }
  return Promise.resolve();
}

/** localStorage sicher lesen/schreiben (kann in privaten Fenstern scheitern). */
export const lokal = {
  get(k, std = null) { try { const v = localStorage.getItem(k); return v === null ? std : JSON.parse(v); } catch { return std; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* egal */ } },
};

export function plural(n, ein, mehr) { return `${n} ${n === 1 ? ein : mehr}`; }

export const EMOJI_ANFANG = /^(\p{Extended_Pictographic}(?:️|‍\p{Extended_Pictographic}|\p{Emoji_Modifier})*)\s*/u;
