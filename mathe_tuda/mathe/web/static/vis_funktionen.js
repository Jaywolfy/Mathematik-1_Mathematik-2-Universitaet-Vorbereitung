// Funktionen/Analysis: einheitskreis, exp_log, tangente, riemann.
// Exakte Werte (Felder mit _) kommen aus visuals.py; hier wird nur numerisch gezeichnet.
import { h, inline, reduziert } from "./util.js";
import { texHtml } from "./formel.js";
import { koordinaten, auswerten, regler, zahlText } from "./plot.js";
import { knopf } from "./visuals.js";

const zt = (x, s = 3) => zahlText(x, s);
/** Dezimalzahl für TeX (Komma als {,}). */
const zTex = (x, s = 3) => zt(x, s).replace("−", "-").replace(",", "{,}");
/** Zeile "Name = Wert" als KaTeX-Zeile in einer Werteliste. */
const wertZeile = (tex) => h("div", { class: "vf-wert", html: texHtml("\\displaystyle " + tex) });

/** Tastatur für ein fokussierbares SVG: Pfeile ±klein, Bild auf/ab ±gross. */
function tasten(el, { klein, gross, aendern, label }) {
  el.setAttribute("tabindex", "0");
  el.setAttribute("aria-label", label);
  el.addEventListener("keydown", (e) => {
    const d = { ArrowRight: klein, ArrowUp: klein, ArrowLeft: -klein, ArrowDown: -klein, PageUp: gross, PageDown: -gross }[e.key];
    if (d === undefined) return;
    e.preventDefault(); e.stopPropagation();
    aendern(d);
  });
}

/** Ziehen per Maus/Finger: onzug(datenX, datenY) */
function ziehbar(k, onzug, { start = null } = {}) {
  let aktiv = false;
  k.svg.addEventListener("pointerdown", (e) => {
    const p = k.ausEvent(e);
    if (start && !start(p[0], p[1])) return;
    aktiv = true; k.svg.setPointerCapture(e.pointerId); onzug(p[0], p[1]); e.preventDefault();
  });
  k.svg.addEventListener("pointermove", (e) => { if (aktiv) { const p = k.ausEvent(e); onzug(p[0], p[1]); } });
  const ende = () => { aktiv = false; };
  k.svg.addEventListener("pointerup", ende);
  k.svg.addEventListener("pointercancel", ende);
}

/* =========================================================== Einheitskreis */
const PI_TICKS = [[0.5, "π/2"], [1, "π"], [1.5, "3π/2"], [2, "2π"]].map(([f, text]) => ({ x: f * Math.PI, text }));

function einheitskreis(box, d) {
  const zeige = new Set(d.zeige || ["sin", "cos", "kurve"]);
  const tab = new Map((d._tabelle || []).map(z => [z.grad, z]));
  const bogen = d.bogenmass !== false;
  let grad = Number(d._winkel ?? 30);
  const rad = () => grad * Math.PI / 180;

  const kreis = koordinaten({ x: [-1.45, 1.45], y: [-1.45, 1.45], breite: 380, hoehe: 380, zoom: false, klickbar: true, schritt: 0.5,
    label: "Einheitskreis" }, (k) => {
    const a = rad(), c = Math.cos(a), s = Math.sin(a);
    k.kreis(0, 0, 1, "ek-kreis");
    k.bogen(0, 0, 30, 0, a, "winkelbogen");
    if (zeige.has("tan") && Math.abs(c) > 1e-6) {
      const t = s / c;
      k.linie(1, -3, 1, 3, "ek-tangentenlinie");
      k.linie(0, 0, 1, t, "hilfslinie");
      k.linie(1, 0, 1, t, "ek-tan");
      if (Math.abs(t) < 1.4) k.etikett(1, t / 2, texHtml("\\tan\\alpha"), "ek-lbl rechts");
    }
    k.linie(0, 0, c, s, "ek-radius");
    if (zeige.has("cos")) {
      k.linie(c, s, c, 0, "hilfslinie");
      k.linie(0, 0, c, 0, "ek-cos");
      k.etikett(c / 2, 0, texHtml("\\cos\\alpha"), s >= 0 ? "ek-lbl unten" : "ek-lbl oben");
    }
    if (zeige.has("sin")) {
      k.linie(c, 0, c, s, "ek-sin");
      k.linie(0, s, c, s, "hilfslinie");
      k.etikett(c, s / 2, texHtml("\\sin\\alpha"), c >= 0 ? "ek-lbl rechts" : "ek-lbl links");
    }
    k.punkt(c, s, { klasse: "punkt ek-p" });
    const ma = a / 2;
    if (grad > 8) k.etikett(0.42 * Math.cos(ma), 0.42 * Math.sin(ma), texHtml("\\alpha"), "ek-alpha");
    k.etikett(c * 1.17, s * 1.17, texHtml("P"), "ek-alpha");
  });

  let kurve = null;
  if (zeige.has("kurve")) {
    kurve = koordinaten({ x: [-0.4, 2 * Math.PI + 0.4], y: [-1.45, 1.45], breite: 560, hoehe: 380, zoom: false, xTicks: PI_TICKS,
      xName: "α", label: "Sinus- und Kosinuskurve" }, (k) => {
      const a = rad();
      if (zeige.has("cos")) k.kurve(Math.cos, "kurve", "var(--plot-1)");
      if (zeige.has("sin")) k.kurve(Math.sin, "kurve", "var(--plot-2)");
      k.linie(a, -1.45, a, 1.45, "hilfslinie");
      if (zeige.has("cos")) k.punkt(a, Math.cos(a), { klasse: "punkt ek-cos-p" });
      if (zeige.has("sin")) k.punkt(a, Math.sin(a), { klasse: "punkt ek-sin-p" });
    });
  }

  const werte = h("div", { class: "vf-werte", "aria-live": "polite" });
  function anzeigen() {
    const ganz = Math.abs(grad - Math.round(grad)) < 1e-9 ? Math.round(grad) : null;
    const z = ganz !== null ? tab.get(ganz) : null;
    const a = rad();
    const w = (tex, num) => (z && tex !== undefined ? (tex === null ? "\\text{nicht definiert}" : tex) : `\\approx ${zTex(num)}`);
    const zeilen = [`\\alpha = ${zt(grad, 1).replace(",", "{,}")}^\\circ` + (bogen ? (z ? ` = ${z.rad}` : ` \\approx ${zTex(a)}`) : "")];
    if (zeige.has("sin")) zeilen.push(`\\sin\\alpha ${z ? "= " : ""}${w(z && z.sin, Math.sin(a))}`);
    if (zeige.has("cos")) zeilen.push(`\\cos\\alpha ${z ? "= " : ""}${w(z && z.cos, Math.cos(a))}`);
    if (zeige.has("tan")) {
      const c = Math.cos(a);
      zeilen.push(Math.abs(c) < 1e-9 ? "\\tan\\alpha\\ \\text{ist nicht definiert}" : `\\tan\\alpha ${z ? "= " : ""}${w(z ? z.tan : undefined, Math.tan(a))}`);
    }
    werte.replaceChildren(...zeilen.map(wertZeile));
    if (!z) werte.append(h("div", { class: "vf-hinweis", text: "Exakte Werte gibt es hier für Vielfache von 15°." }));
  }

  let r = null;
  function setzen(g, vonRegler = false) {
    grad = Math.max(0, Math.min(360, g));
    kreis.neu(); kurve && kurve.neu(); anzeigen();
    if (r && !vonRegler) r.setzen(grad);
  }
  ziehbar(kreis, (x, y) => {
    let g = Math.atan2(y, x) * 180 / Math.PI;
    if (g < 0) g += 360;
    g = Math.round(g);
    const naechst = Math.round(g / 15) * 15;
    if (Math.abs(g - naechst) <= 3) g = naechst;   // an Standardwinkel einrasten
    setzen(g);
  });
  tasten(kreis.svg, { klein: 1, gross: 15, aendern: (dg) => setzen(grad + dg), label: "Einheitskreis: Winkel mit Pfeiltasten ändern (Bild auf/ab: 15°)" });

  const stufe = h("div", { class: "vf-reihe" }, h("div", { class: "vf-buehne vf-quadrat" }, kreis.el));
  if (kurve) stufe.append(h("div", { class: "vf-buehne vf-breit" }, kurve.el));
  box.append(stufe);
  if (kurve) box.append(h("div", { class: "plot-legende" },
    zeige.has("sin") ? h("span", { class: "leg" }, h("i", { style: { background: "var(--plot-2)" } }), h("span", { html: texHtml("\\sin\\alpha") })) : null,
    zeige.has("cos") ? h("span", { class: "leg" }, h("i", { style: { background: "var(--plot-1)" } }), h("span", { html: texHtml("\\cos\\alpha") })) : null));
  box.append(werte);
  if (d.regler !== false) {
    r = regler({ name: "Winkel α in Grad", tex: "\\alpha", von: 0, bis: 360, schritt: 1, wert: grad, format: (v) => zt(v, 1) + "°",
      oninput: (v) => setzen(v, true) });
    box.append(h("div", { class: "regler-reihe" }, r.el),
      h("div", { class: "vis-steuer" }, knopf("− 15°", () => setzen(Math.ceil(grad / 15) * 15 - 15)),
        knopf("+ 15°", () => setzen(Math.floor(grad / 15) * 15 + 15))));
  }
  anzeigen();
}

/* =========================================================== Exponential & Logarithmus */
function expLog(box, d) {
  const start = Number(d._basis ?? 2);
  let a = start, t = -1;
  const umkehr = d.umkehr !== false;
  const exakt = () => Math.abs(a - start) < 1e-12;
  const legende = h("div", { class: "plot-legende" });
  const info = h("div", { class: "plot-info", "aria-live": "polite" });
  const k = koordinaten({ x: (d.x || [-4, 6]).map(Number), y: (d.y || [-3, 6]).map(Number), gleicheAchsen: true, label: "Exponential- und Logarithmusfunktion" }, (k) => {
    const bt = exakt() ? d._basis_tex : zTex(a, 2);
    const fe = (x) => Math.pow(a, x), fl = (x) => (x > 0 ? Math.log(x) / Math.log(a) : NaN);
    const eins = Math.abs(a - 1) < 1e-9;
    if (umkehr) k.gerade(0, 0, 1, "symmetrieachse");
    k.kurve(fe, "kurve", "var(--plot-1)");
    if (umkehr && !eins) k.kurve(fl, "kurve", "var(--plot-2)", [Math.max(1e-6, k.xmin), k.xmax]);
    k.punkt(0, 1, { label: texHtml("(0 \\mid 1)"), labelKlasse: "links-oben" });
    k.punkt(1, a, { label: texHtml(`(1 \\mid ${bt})`) });
    if (umkehr && !eins) {
      k.punkt(1, 0, { klasse: "punkt null", label: texHtml("(1 \\mid 0)"), labelKlasse: "unten" });
      k.punkt(a, 1, { klasse: "punkt null", label: texHtml(`(${bt} \\mid 1)`), labelKlasse: "unten" });
      // gespiegeltes Punktpaar P(t | a^t) und P'(a^t | t)
      const y = fe(t);
      if (Number.isFinite(y)) {
        k.linie(t, y, y, t, "hilfslinie");
        k.punkt(t, y, { klasse: "punkt scheitel", label: texHtml("P"), labelKlasse: "klein" });
        k.punkt(y, t, { klasse: "punkt scheitel", label: texHtml("P'"), labelKlasse: "klein" });
      }
    }
    const expTex = exakt() ? d._exp_tex : `${bt}^{x}`, logTex = exakt() ? d._log_tex : `\\log_{${bt}}(x)`;
    legende.replaceChildren(
      h("span", { class: "leg" }, h("i", { style: { background: "var(--plot-1)" } }), h("span", { html: texHtml(`f(x) = ${expTex}`) })),
      umkehr && !eins ? h("span", { class: "leg" }, h("i", { style: { background: "var(--plot-2)" } }), h("span", { html: texHtml(`f^{-1}(x) = ${logTex}`) })) : null,
      umkehr ? h("span", { class: "leg" }, h("i", { class: "gestrichelt" }), h("span", { html: texHtml("y = x") })) : null);
    info.innerHTML = inline(eins ? "Basis $1$: $1^x = 1$ ist konstant und hat keine Umkehrfunktion."
      : a > 1 ? "$a > 1$: $a^x$ und $\\log_a(x)$ wachsen." : "$0 < a < 1$: $a^x$ und $\\log_a(x)$ fallen.");
  });
  box.append(h("div", { class: "vis-scroll" }, k.el), legende, info);
  const reihe = h("div", { class: "regler-reihe" });
  if (d.regler !== false) {
    reihe.append(regler({ name: "Basis a", tex: "a", von: 0.1, bis: 5, schritt: 0.05, wert: Math.min(5, Math.max(0.1, start)),
      format: (v) => zt(v, 2), oninput: (v) => { a = v; k.neu(); } }).el);
  }
  if (umkehr) reihe.append(regler({ name: "Punkt P auf der Exponentialkurve", tex: "P\\text{: } x", von: -2, bis: 2, schritt: 0.1, wert: t,
    oninput: (v) => { t = v; k.neu(); } }).el);
  if (reihe.children.length) box.append(reihe);
}

/* =========================================================== Tangente & Sekante */
function yBereich(f, a, b) {
  let lo = Infinity, hi = -Infinity;
  for (let i = 0; i <= 200; i++) { const y = f(a + (b - a) * i / 200); if (Number.isFinite(y)) { lo = Math.min(lo, y); hi = Math.max(hi, y); } }
  if (!Number.isFinite(lo)) return [-5, 5];
  lo = Math.max(lo, -50); hi = Math.min(hi, 50);
  const rand = Math.max(0.5, (hi - lo) * 0.15);
  return [Math.min(lo - rand, -0.5), Math.max(hi + rand, 0.5)];
}

function tangente(box, d) {
  const f = (x) => auswerten(d._ast, { x });
  const fs = d._abl_ast ? (x) => auswerten(d._abl_ast, { x }) : (x) => { const e = 1e-5 * Math.max(1, Math.abs(x)); return (f(x + e) - f(x - e)) / (2 * e); };
  const start = { x0: d._x0, h: d._h };
  let x0 = d._x0, hh = d._h;
  const mitSekante = d.sekante !== false;
  const xb = (d.x || [x0 - 4, x0 + 4]).map(Number);
  const yb = d.y ? d.y.map(Number) : yBereich(f, xb[0], xb[1]);
  const werte = h("div", { class: "vf-werte", "aria-live": "polite" });
  const k = koordinaten({ x: xb, y: yb, label: "Funktion mit Sekante und Tangente" }, (k) => {
    k.kurve(f, "kurve", "var(--plot-1)");
    const y0 = f(x0), m = fs(x0);
    if (!Number.isFinite(y0)) return;
    if (Number.isFinite(m)) k.gerade(x0, y0, m, "tangente");
    const sek = mitSekante && Math.abs(hh) > 1e-9;
    if (sek) {
      const y1 = f(x0 + hh);
      if (Number.isFinite(y1)) {
        const ms = (y1 - y0) / hh;
        k.gerade(x0, y0, ms, "sekante");
        k.linie(x0, y0, x0 + hh, y0, "steigungsdreieck");
        k.linie(x0 + hh, y0, x0 + hh, y1, "steigungsdreieck");
        k.etikett(x0 + hh / 2, y0, texHtml("h"), y1 >= y0 ? "unten klein" : "oben klein");
        k.punkt(x0 + hh, y1, { klasse: "punkt null", label: texHtml("Q"), labelKlasse: "klein" });
      }
    }
    k.punkt(x0, y0, { label: texHtml("P"), labelKlasse: "klein" });
  });
  function anzeigen() {
    const amStart = Math.abs(x0 - start.x0) < 1e-12, hStart = amStart && Math.abs(hh - start.h) < 1e-12;
    const y0 = f(x0), m = fs(x0);
    const z = [`f(x) = ${d._tex}`, `x_0 ${amStart ? "= " + d._x0_tex : "\\approx " + zTex(x0, 2)}`];
    if (mitSekante) {
      if (Math.abs(hh) < 1e-9) z.push("h = 0\\text{: keine Sekante mehr – nur noch der Grenzwert}");
      else {
        const ms = (f(x0 + hh) - y0) / hh;
        z.push(`m_{\\text{Sek}} = \\frac{f(x_0 + h) - f(x_0)}{h} ${hStart && d._m_sek_tex ? d._m_sek_tex : Number.isFinite(ms) ? "\\approx " + zTex(ms) : "\\text{ n. d.}"}`);
      }
    }
    const mTex = amStart && d._m_tex ? d._m_tex : Number.isFinite(m) ? "\\approx " + zTex(m) : "\\text{ n. d.}";
    z.push(`m_{\\text{Tan}} = f'(x_0) ${mTex}`);
    if (amStart && d._tangente_tex) z.push(`t\\colon\\ ${d._tangente_tex}`);
    werte.replaceChildren(...z.map(wertZeile));
    if (d._abl_tex) werte.append(wertZeile(`f'(x) = ${d._abl_tex}`));
  }
  box.append(h("div", { class: "vis-scroll" }, k.el),
    h("div", { class: "plot-legende" },
      h("span", { class: "leg" }, h("i", { style: { background: "var(--plot-1)" } }), h("span", { html: texHtml("f") })),
      mitSekante ? h("span", { class: "leg" }, h("i", { style: { background: "var(--plot-2)" } }), "Sekante") : null,
      h("span", { class: "leg" }, h("i", { style: { background: "var(--plot-3)" } }), "Tangente")),
    werte);
  const neu = () => { k.neu(); anzeigen(); };
  const rx = regler({ name: "Stelle x0", tex: "x_0", von: xb[0], bis: xb[1], schritt: 0.05, wert: x0, oninput: (v) => { x0 = v; neu(); } });
  const reihe = h("div", { class: "regler-reihe" }, rx.el);
  let rh = null, lauf = null;
  if (mitSekante) {
    rh = regler({ name: "Abstand h", tex: "h", von: -3, bis: 3, schritt: 0.01, wert: hh, format: (v) => zt(v, 2), oninput: (v) => { stopp(); hh = v; neu(); } });
    reihe.append(rh.el);
  }
  box.append(reihe);
  function stopp() { if (lauf) { cancelAnimationFrame(lauf); lauf = null; } }
  if (mitSekante) {
    const gegenNull = knopf("h → 0", () => {
      stopp();
      if (reduziert()) { hh = 0.01 * Math.sign(hh || 1); rh.setzen(hh); neu(); return; }
      const schritt = () => {
        hh *= 0.94;
        if (Math.abs(hh) < 0.01) { hh = 0.01 * Math.sign(hh); lauf = null; } else lauf = requestAnimationFrame(schritt);
        rh.setzen(hh); neu();
      };
      lauf = requestAnimationFrame(schritt);
    });
    const zurueck = knopf("Zurücksetzen", () => { stopp(); x0 = start.x0; hh = start.h; rx.setzen(x0); rh.setzen(hh); neu(); });
    box.append(h("div", { class: "vis-steuer" }, gegenNull, zurueck));
  }
  anzeigen();
}

/* =========================================================== Riemann-Summen */
const ARTEN = [["links", "links"], ["rechts", "rechts"], ["mitte", "Mitte"], ["unter", "Untersumme"], ["ober", "Obersumme"]];

function riemann(box, d) {
  const f = (x) => auswerten(d._ast, { x });
  const a = d._von, b = d._bis;
  let n = d._n, art = d.art || "links";
  const xb = (d.x || [a - (b - a) * 0.15, b + (b - a) * 0.15]).map(Number);
  const yb = d.y ? d.y.map(Number) : yBereich(f, xb[0], xb[1]);
  const werte = h("div", { class: "vf-werte", "aria-live": "polite" });

  function hoehe(l, r) {
    if (art === "links") return f(l);
    if (art === "rechts") return f(r);
    if (art === "mitte") return f((l + r) / 2);
    let best = art === "ober" ? -Infinity : Infinity;
    for (let i = 0; i <= 60; i++) { const y = f(l + (r - l) * i / 60); if (Number.isFinite(y)) best = art === "ober" ? Math.max(best, y) : Math.min(best, y); }
    return best;
  }
  function summe() {
    const dx = (b - a) / n;
    let s = 0;
    for (let i = 0; i < n; i++) s += hoehe(a + i * dx, a + (i + 1) * dx) * dx;
    return s;
  }
  const k = koordinaten({ x: xb, y: yb, label: "Riemann-Summe" }, (k) => {
    // Fläche unter der Kurve (zart)
    const pts = [[a, 0]];
    for (let i = 0; i <= 160; i++) { const x = a + (b - a) * i / 160, y = f(x); if (Number.isFinite(y)) pts.push([x, y]); }
    pts.push([b, 0]);
    k.flaeche(pts, "flaeche zart");
    const dx = (b - a) / n;
    for (let i = 0; i < n; i++) {
      const l = a + i * dx, r = l + dx, y = hoehe(l, r);
      if (!Number.isFinite(y)) continue;
      k.flaeche([[l, 0], [r, 0], [r, y], [l, y]], "rechteck" + (y < 0 ? " negativ" : ""));
      if (n <= 40 && ["links", "rechts", "mitte"].includes(art)) {
        const xi = art === "links" ? l : art === "rechts" ? r : (l + r) / 2;
        k.punkt(xi, y, { r: n > 16 ? 2.5 : 4, klasse: "punkt stuetz" });
      }
    }
    k.kurve(f, "kurve", "var(--plot-1)");
    k.linie(a, k.ymin, a, k.ymax, "hilfslinie");
    k.linie(b, k.ymin, b, k.ymax, "hilfslinie");
  });
  function anzeigen() {
    const s = summe(), exakt = d._summe && d._summe.n === n && d._summe.art === art && d._summe.tex;
    const name = { links: "linke Summe", rechts: "rechte Summe", mitte: "Mittelsumme", ober: "Obersumme", unter: "Untersumme" }[art];
    const z = [`f(x) = ${d._tex}\\quad\\text{auf } [${d._von_tex},\\ ${d._bis_tex}]`,
      `n = ${n},\\quad \\Delta x = \\frac{${d._bis_tex} - (${d._von_tex})}{${n}} ${Math.abs(Math.round((b - a) / n * 1000) / 1000 - (b - a) / n) < 1e-12 ? "=" : "\\approx"} ${zTex((b - a) / n)}`.replace("- (0)", "- 0"),
      `S_{${n}}\\ (\\text{${name}}) ${exakt ? "= " + d._summe.tex : "\\approx " + zTex(s, 4)}`];
    if (d._integral) {
      const I = d._integral;
      z.push(`\\int_{${d._von_tex}}^{${d._bis_tex}} ${d._tex}\\,dx = \\left[${d._stamm_tex}\\right]_{${d._von_tex}}^{${d._bis_tex}} ${I.exakt ? "= " : "\\approx "}${I.tex}`);
      z.push(`|S_{${n}} - I| \\approx ${zTex(Math.abs(s - I.wert), 4)}`);
    }
    werte.replaceChildren(...z.map(wertZeile));
  }
  const neu = () => { k.neu(); anzeigen(); };
  const knoepfe = ARTEN.map(([id, text]) => knopf(text, () => { art = id; knoepfe.forEach((kn, i) => kn.setAttribute("aria-pressed", String(ARTEN[i][0] === art))); neu(); },
    { "aria-pressed": String(id === art) }));
  box.append(h("div", { class: "vis-scroll" }, k.el), werte,
    h("div", { class: "regler-reihe" }, regler({ name: "Anzahl der Rechtecke n", tex: "n", von: 1, bis: d._n_max || 50, schritt: 1, wert: n,
      format: (v) => String(v), oninput: (v) => { n = Math.round(v); neu(); } }).el),
    h("div", { class: "vis-steuer vf-segment", role: "group", "aria-label": "Art der Summe" }, knoepfe));
  anzeigen();
}

export const BAUER = { einheitskreis, exp_log: expLog, tangente, riemann };
export { tasten, ziehbar, wertZeile, zTex };
