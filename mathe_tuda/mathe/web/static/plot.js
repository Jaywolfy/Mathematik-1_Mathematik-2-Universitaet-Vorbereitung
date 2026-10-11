// Gemeinsames Koordinatensystem für alle Funktions-Visuals (SVG, ohne Bibliothek).
// Exakte Werte kommen aus Python; hier wird nur numerisch gezeichnet.
import { h, svg, reduziert } from "./util.js";
import { texHtml } from "./formel.js";

/* ---------- AST-Auswerter (AST kommt fertig vom Server, kein Parser im Browser) ---------- */
const FAK = (n) => { let r = 1; for (let i = 2; i <= n; i++) r *= i; return r; };
export function auswerten(ast, env) {
  const [art, a, b] = ast;
  switch (art) {
    case "zahl": return a;
    case "var": return env[a];
    case "konst": return a === "pi" ? Math.PI : Math.E;
    case "neg": return -auswerten(a, env);
    case "add": return auswerten(a, env) + auswerten(b, env);
    case "sub": return auswerten(a, env) - auswerten(b, env);
    case "mul": return auswerten(a, env) * auswerten(b, env);
    case "div": { const n = auswerten(b, env); return n === 0 ? NaN : auswerten(a, env) / n; }
    case "pow": {
      const x = auswerten(a, env), y = auswerten(b, env);
      if (x < 0 && !Number.isInteger(y)) { // ungerade Wurzeln negativer Zahlen
        const q = 1 / y;
        if (Number.isInteger(Math.round(q)) && Math.abs(q - Math.round(q)) < 1e-9 && Math.round(q) % 2) return -Math.pow(-x, y);
        return NaN;
      }
      return Math.pow(x, y);
    }
    case "fak": { const n = auswerten(a, env); return n >= 0 && Number.isInteger(n) ? FAK(n) : NaN; }
    case "abs": return Math.abs(auswerten(a, env));
    case "fun": {
      const x = auswerten(b, env);
      switch (a) {
        case "sqrt": return x < 0 ? NaN : Math.sqrt(x);
        case "sin": return Math.sin(x);
        case "cos": return Math.cos(x);
        case "tan": return Math.abs(Math.cos(x)) < 1e-12 ? NaN : Math.tan(x);
        case "ln": return x <= 0 ? NaN : Math.log(x);
        case "log2": return x <= 0 ? NaN : Math.log2(x);
        case "log10": return x <= 0 ? NaN : Math.log10(x);
        case "exp": return Math.exp(x);
      }
    }
  }
  return NaN;
}

export function zahlText(x, stellen = 3) {
  if (!Number.isFinite(x)) return x > 0 ? "∞" : x < 0 ? "−∞" : "–";
  const r = Math.round(x * 10 ** stellen) / 10 ** stellen;
  return String(Object.is(r, -0) ? 0 : r).replace("-", "−").replace(".", ",");
}

function schoenerSchritt(spanne, ziel = 10) {
  const roh = spanne / ziel;
  const p = Math.pow(10, Math.floor(Math.log10(roh)));
  for (const m of [1, 2, 5, 10]) if (roh <= m * p) return m * p;
  return 10 * p;
}

let uid = 0;

/**
 * Koordinatensystem. opts: {x: [min, max], y: [min, max], breite, hoehe, gleicheAchsen, zoom, beschriftung}
 * malen(k) wird bei jedem Neuzeichnen (Zoom/Verschieben) aufgerufen und zeichnet in k.inhalt.
 */
export function koordinaten(opts, malen) {
  const W = opts.breite || 640, H = opts.hoehe || 400;
  let [xmin, xmax] = opts.x || [-5, 5];
  let [ymin, ymax] = opts.y || [-5, 5];
  const start = { xmin, xmax, ymin, ymax };
  if (opts.gleicheAchsen) {
    const mitte = (ymin + ymax) / 2, halb = (xmax - xmin) * H / W / 2;
    ymin = mitte - halb; ymax = mitte + halb;
  }
  const id = "k" + (++uid);
  const s = svg("svg", { class: "plot", viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": opts.label || "Koordinatensystem" });
  const defs = svg("defs", null,
    svg("clipPath", { id: id + "c" }, svg("rect", { x: 0, y: 0, width: W, height: H })),
    svg("marker", { id: id + "p", viewBox: "0 0 10 10", refX: 8, refY: 5, markerWidth: 7, markerHeight: 7, orient: "auto-start-reverse" },
      svg("path", { d: "M0,0 L10,5 L0,10 z", class: "pfeilspitze" })));
  const gitter = svg("g", { class: "gitter" });
  const inhalt = svg("g", { class: "inhalt", "clip-path": `url(#${id}c)` });
  const oben = svg("g", { class: "oben" });   // bleibt beim Neuzeichnen erhalten (z. B. fokussierbare Griffe)
  s.append(defs, gitter, inhalt, oben);
  const etiketten = h("div", { class: "plot-etiketten", "aria-hidden": "true" });
  const buehne = h("div", { class: "plot-buehne" }, s, etiketten);
  const k = {
    svg: s, inhalt, oben, el: buehne, id, W, H,
    get xmin() { return xmin; }, get xmax() { return xmax; }, get ymin() { return ymin; }, get ymax() { return ymax; },
    px: (x) => (x - xmin) / (xmax - xmin) * W,
    py: (y) => H - (y - ymin) / (ymax - ymin) * H,
    inv: (px, py) => [xmin + px / W * (xmax - xmin), ymin + (H - py) / H * (ymax - ymin)],
    neu, etikett, kurve, punkt, linie, pfeil, flaeche, kreis, bogen, gerade, ausEvent,
  };

  function etikett(x, y, html, klasse = "") {
    const e = h("div", { class: "plot-etikett " + klasse, html });
    e.style.left = (k.px(x) / W * 100) + "%";
    e.style.top = (k.py(y) / H * 100) + "%";
    etiketten.append(e);
    return e;
  }
  function kurve(f, klasse = "kurve", farbe = null, bereich = null) {
    const n = 700;
    const [a, b] = bereich || [xmin, xmax];
    const spanneY = ymax - ymin;
    let d = "", offen = false, letztY = null;
    for (let i = 0; i <= n; i++) {
      const x = a + (b - a) * i / n;
      let y;
      try { y = f(x); } catch { y = NaN; }
      if (!Number.isFinite(y) || Math.abs(y - (ymin + ymax) / 2) > spanneY * 20) { offen = false; letztY = null; continue; }
      if (letztY !== null && Math.abs(y - letztY) > spanneY * 1.5) offen = false;
      const yp = Math.max(-H, Math.min(2 * H, k.py(y)));
      d += (offen ? "L" : "M") + k.px(x).toFixed(2) + "," + yp.toFixed(2);
      offen = true; letztY = y;
    }
    const p = svg("path", { class: klasse, d });
    if (farbe) p.style.stroke = farbe;
    inhalt.append(p);
    return p;
  }
  function punkt(x, y, { klasse = "punkt", r = 5.5, label = null, labelKlasse = "", offen = false } = {}) {
    const c = svg("circle", { class: klasse + (offen ? " offen" : ""), cx: k.px(x), cy: k.py(y), r });
    inhalt.append(c);
    if (label) etikett(x, y, label, "ueber " + labelKlasse);
    return c;
  }
  function linie(x1, y1, x2, y2, klasse = "hilfslinie") {
    const l = svg("line", { class: klasse, x1: k.px(x1), y1: k.py(y1), x2: k.px(x2), y2: k.py(y2) });
    inhalt.append(l);
    return l;
  }
  function pfeil(x1, y1, x2, y2, klasse = "vektor") {
    const l = svg("line", { class: klasse, x1: k.px(x1), y1: k.py(y1), x2: k.px(x2), y2: k.py(y2), "marker-end": `url(#${id}p)` });
    inhalt.append(l);
    return l;
  }
  function flaeche(punkte, klasse = "flaeche") {
    const p = svg("polygon", { class: klasse, points: punkte.map(([x, y]) => `${k.px(x)},${k.py(y)}`).join(" ") });
    inhalt.append(p);
    return p;
  }
  function kreis(cx, cy, r, klasse = "hilfskreis") {
    const c = svg("ellipse", { class: klasse, cx: k.px(cx), cy: k.py(cy), rx: Math.abs(k.px(r) - k.px(0)), ry: Math.abs(k.py(r) - k.py(0)) });
    inhalt.append(c);
    return c;
  }
  /** Kreisbogen um (cx, cy) mit Radius rPx (Pixel) von Winkel a1 bis a2 (Bogenmaß, mathematisch positiv). */
  function bogen(cx, cy, rPx, a1, a2, klasse = "winkelbogen") {
    const x0 = k.px(cx), y0 = k.py(cy);
    const p = (a) => `${(x0 + rPx * Math.cos(a)).toFixed(2)},${(y0 - rPx * Math.sin(a)).toFixed(2)}`;
    const gross = Math.abs(a2 - a1) > Math.PI ? 1 : 0, sweep = a2 > a1 ? 0 : 1;
    const b = svg("path", { class: klasse, d: Math.abs(a2 - a1) < 1e-9 ? "" : `M${p(a1)} A${rPx},${rPx} 0 ${gross} ${sweep} ${p(a2)}` });
    inhalt.append(b);
    return b;
  }
  /** Gerade durch (x1, y1) mit Steigung m über die ganze Breite (m = Infinity: senkrecht). */
  function gerade(x1, y1, m, klasse = "gerade") {
    if (!Number.isFinite(m)) return linie(x1, ymin - (ymax - ymin), x1, ymax + (ymax - ymin), klasse);
    const a = xmin - (xmax - xmin), b = xmax + (xmax - xmin);
    return linie(a, y1 + m * (a - x1), b, y1 + m * (b - x1), klasse);
  }
  /** Zeiger-Ereignis -> Datenkoordinaten (berücksichtigt die CSS-Skalierung). */
  function ausEvent(e) {
    const r = s.getBoundingClientRect();
    return k.inv((e.clientX - r.left) / r.width * W, (e.clientY - r.top) / r.height * H);
  }
  function achsen() {
    gitter.replaceChildren();
    const sx = opts.schritt || schoenerSchritt(xmax - xmin), sy = opts.schritt || schoenerSchritt(ymax - ymin, 8);
    const xTicks = opts.xTicks || null;   // [{x, text}] statt gleichmäßiger Zahlen (z. B. π/2, π, …)
    const xWerte = xTicks ? xTicks.map(t => t.x) : [];
    if (!xTicks) for (let x = Math.ceil(xmin / sx) * sx; x <= xmax + 1e-9; x += sx) xWerte.push(x);
    if (xTicks && !xWerte.some(x => Math.abs(x) < 1e-9) && xmin < 0 && xmax > 0) xWerte.push(0);
    for (const x of xWerte) {
      gitter.append(svg("line", { class: Math.abs(x) < 1e-9 ? "achse" : "gitterlinie", x1: k.px(x), y1: 0, x2: k.px(x), y2: H }));
    }
    for (let y = Math.ceil(ymin / sy) * sy; y <= ymax + 1e-9; y += sy) {
      gitter.append(svg("line", { class: Math.abs(y) < 1e-9 ? "achse" : "gitterlinie", x1: 0, y1: k.py(y), x2: W, y2: k.py(y) }));
    }
    const y0 = Math.min(H - 4, Math.max(14, k.py(0))), x0 = Math.min(W - 6, Math.max(6, k.px(0)));
    for (const x of xWerte) {
      if (Math.abs(x) < 1e-9 || k.px(x) < 14 || k.px(x) > W - 14) continue;
      const text = xTicks ? (xTicks.find(t => t.x === x) || {}).text : zahlText(x);
      if (text) gitter.append(svg("text", { class: "achsen-zahl", x: k.px(x), y: y0 + 15, "text-anchor": "middle" }, text));
    }
    for (let y = Math.ceil(ymin / sy) * sy; y <= ymax + 1e-9; y += sy) {
      if (Math.abs(y) < 1e-9 || k.py(y) < 14 || k.py(y) > H - 8) continue;
      gitter.append(svg("text", { class: "achsen-zahl", x: x0 - 6, y: k.py(y) + 4, "text-anchor": "end" }, zahlText(y)));
    }
    gitter.append(svg("text", { class: "achsen-name", x: W - 8, y: y0 - 8, "text-anchor": "end" }, opts.xName || "x"));
    gitter.append(svg("text", { class: "achsen-name", x: x0 + 8, y: 14 }, opts.yName || "y"));
  }
  function neu() {
    inhalt.replaceChildren();
    etiketten.replaceChildren();
    achsen();
    malen && malen(k);
  }

  if (opts.zoom !== false) {
    const zoomen = (f) => {
      const mx = (xmin + xmax) / 2, my = (ymin + ymax) / 2;
      xmin = mx - (mx - xmin) * f; xmax = mx + (xmax - mx) * f;
      ymin = my - (my - ymin) * f; ymax = my + (ymax - my) * f;
      neu();
    };
    const leiste = h("div", { class: "plot-zoom" },
      h("button", { class: "btn btn-sm", type: "button", "aria-label": "hineinzoomen", text: "+", onclick: () => zoomen(0.7) }),
      h("button", { class: "btn btn-sm", type: "button", "aria-label": "herauszoomen", text: "−", onclick: () => zoomen(1 / 0.7) }),
      h("button", { class: "btn btn-sm", type: "button", "aria-label": "Ansicht zurücksetzen", text: "⟲", onclick: () => { ({ xmin, xmax, ymin, ymax } = start); neu(); } }));
    buehne.append(leiste);
    // Verschieben mit Maus/Finger (nicht, wenn ein Visual selbst Klicks braucht)
    if (!opts.klickbar) {
      let ziehen = null;
      s.addEventListener("pointerdown", (e) => { ziehen = { x: e.clientX, y: e.clientY, xmin, xmax, ymin, ymax }; s.setPointerCapture(e.pointerId); });
      s.addEventListener("pointermove", (e) => {
        if (!ziehen) return;
        const r = s.getBoundingClientRect();
        const dx = (e.clientX - ziehen.x) / r.width * (ziehen.xmax - ziehen.xmin);
        const dy = (e.clientY - ziehen.y) / r.height * (ziehen.ymax - ziehen.ymin);
        xmin = ziehen.xmin - dx; xmax = ziehen.xmax - dx; ymin = ziehen.ymin + dy; ymax = ziehen.ymax + dy;
        neu();
      });
      s.addEventListener("pointerup", () => { ziehen = null; });
      s.addEventListener("pointercancel", () => { ziehen = null; });
    }
  }
  neu();
  return k;
}

/** Schieberegler mit Beschriftung (KaTeX-Name) und Wertanzeige. */
export function regler({ name, tex = null, von = -5, bis = 5, schritt = 0.5, wert = 0, oninput, format = zahlText }) {
  const out = h("output", { text: format(wert) });
  const r = h("input", { type: "range", min: von, max: bis, step: schritt, value: wert, "aria-label": name, "aria-valuetext": format(wert) });
  const anzeigen = (v) => { out.textContent = format(v); r.setAttribute("aria-valuetext", format(v)); };
  r.addEventListener("input", () => { const v = parseFloat(r.value); anzeigen(v); oninput(v); });
  return {
    el: h("div", { class: "regler" }, h("label", null, h("span", { html: texHtml(tex || name) }), out), r),
    input: r,
    setzen: (v) => { r.value = v; anzeigen(v); },
  };
}

/** Nullstellen numerisch (Vorzeichenwechsel + Bisektion) im Intervall. */
export function nullstellenNumerisch(f, a, b, n = 800) {
  const erg = [];
  let xa = a, ya = f(a);
  for (let i = 1; i <= n; i++) {
    const xb = a + (b - a) * i / n, yb = f(xb);
    if (Number.isFinite(ya) && Number.isFinite(yb)) {
      if (ya === 0) erg.push(xa);
      else if (ya * yb < 0 && Math.abs(ya - yb) < 1e3) {
        let lo = xa, hi = xb;
        for (let k = 0; k < 60; k++) { const m = (lo + hi) / 2; (f(lo) * f(m) <= 0) ? (hi = m) : (lo = m); }
        erg.push((lo + hi) / 2);
      }
    }
    xa = xb; ya = yb;
  }
  return erg.filter((x, i) => i === 0 || Math.abs(x - erg[i - 1]) > 1e-6);
}

export const animationErlaubt = () => !reduziert();
