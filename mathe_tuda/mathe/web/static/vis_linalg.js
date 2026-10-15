// Lineare Algebra und komplexe Zahlen: vektoren2d, matrix_mult, gauss, komplexe_ebene.
// Exakte Werte (Felder mit _) kommen aus visuals.py; hier wird gezeichnet und bei Änderungen numerisch gerechnet.
import { h, svg, inline } from "./util.js";
import { texHtml } from "./formel.js";
import { koordinaten, regler, zahlText } from "./plot.js";
import { knopf } from "./visuals.js";

const FARBE = (n) => `var(--plot-${((n - 1) % 4) + 1})`;
const zTex = (x, s = 3) => zahlText(x, s).replace("−", "-").replace(",", "{,}");
const wertZeile = (tex) => h("div", { class: "vf-wert", html: texHtml("\\displaystyle " + tex) });

/* ---------- exakte Darstellung für Werte auf einem Raster (z. B. 0,5-Schritte beim Ziehen) ---------- */
const ggt = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; };
function nenner(...xs) {
  for (const n of [1, 2, 4, 8, 3, 6, 12]) if (xs.every(x => Math.abs(x * n - Math.round(x * n)) < 1e-9)) return n;
  return null;
}
/** Zahl als TeX-Bruch, falls Nenner klein, sonst Dezimal. */
function bruchTex(x) {
  const n = nenner(x);
  if (!n) return zTex(x);
  let p = Math.round(x * n), q = n;
  const g = ggt(p, q) || 1; p /= g; q /= g;
  if (q === 1) return String(p);
  return `${p < 0 ? "-" : ""}\\frac{${Math.abs(p)}}{${q}}`;
}
/** Wurzel-TeX für √(x²+y²), exakt bei kleinen Nennern. Rückgabe [tex, exakt]. */
function normTex(x, y) {
  const n = nenner(x, y);
  if (!n) return [zTex(Math.hypot(x, y)), false];
  const P = Math.round(x * n), Q = Math.round(y * n);
  let s = P * P + Q * Q, k = 1;
  for (let p = 2; p * p <= s; p++) while (s % (p * p) === 0) { s /= p * p; k *= p; }
  const g = ggt(k, n) || 1, kk = k / g, nn = n / g;
  const z = s === 1 ? String(kk) : (kk === 1 ? "" : kk) + `\\sqrt{${s}}`;
  return [nn === 1 ? z : `\\frac{${z}}{${nn}}`, true];
}
const vekTex = (x, y) => `\\begin{pmatrix} ${bruchTex(x)} \\\\ ${bruchTex(y)} \\end{pmatrix}`;

/* ---------- Pfeile mit eigener Spitze (Farbe wie der Schaft, hell/dunkel) ---------- */
function pfeil(k, x1, y1, x2, y2, farbe, klasse = "vl-pfeil") {
  const ax = k.px(x1), ay = k.py(y1), bx = k.px(x2), by = k.py(y2);
  const len = Math.hypot(bx - ax, by - ay);
  const g = svg("g", { class: klasse });
  if (len < 1) { k.inhalt.append(g); return g; }
  const ux = (bx - ax) / len, uy = (by - ay) / len, sp = Math.min(14, len * 0.45);
  const sx = bx - ux * sp, sy = by - uy * sp;
  g.append(svg("line", { x1: ax, y1: ay, x2: sx + ux * 1.5, y2: sy + uy * 1.5, style: `stroke:${farbe}` }),
    svg("path", { d: `M${bx},${by} L${sx - uy * sp * 0.45},${sy + ux * sp * 0.45} L${sx + uy * sp * 0.45},${sy - ux * sp * 0.45} Z`, style: `fill:${farbe}` }));
  k.inhalt.append(g);
  return g;
}

/** Fokussierbarer, ziehbarer Griff in der Ebene über dem Inhalt. */
function griff(k, { label, holen, setzen, raster = 0.5 }) {
  const c = svg("circle", { class: "vl-griff", r: 13, tabindex: 0, role: "slider", "aria-label": label });
  k.oben.append(c);
  const snap = (v) => Math.round(v / raster) * raster;
  c.addEventListener("pointerdown", (e) => {
    e.stopPropagation(); e.preventDefault();
    c.setPointerCapture(e.pointerId); c.classList.add("zieht");
    const bewegen = (ev) => { const [x, y] = k.ausEvent(ev); setzen(snap(x), snap(y)); };
    const ende = () => { c.classList.remove("zieht"); c.removeEventListener("pointermove", bewegen); c.removeEventListener("pointerup", ende); c.removeEventListener("pointercancel", ende); };
    c.addEventListener("pointermove", bewegen); c.addEventListener("pointerup", ende); c.addEventListener("pointercancel", ende);
  });
  c.addEventListener("keydown", (e) => {
    const d = { ArrowRight: [1, 0], ArrowLeft: [-1, 0], ArrowUp: [0, 1], ArrowDown: [0, -1] }[e.key];
    if (!d) return;
    e.preventDefault(); e.stopPropagation();
    const [x, y] = holen();
    setzen(x + d[0] * raster, y + d[1] * raster);
  });
  return {
    el: c,
    lage: () => { const [x, y] = holen(); c.setAttribute("cx", k.px(x)); c.setAttribute("cy", k.py(y)); c.setAttribute("aria-valuetext", `(${zahlText(x)} | ${zahlText(y)})`); },
  };
}

function bereich(punkte, rand = 1) {
  let xmin = -1, xmax = 1, ymin = -1, ymax = 1;
  for (const [x, y] of punkte) { xmin = Math.min(xmin, x); xmax = Math.max(xmax, x); ymin = Math.min(ymin, y); ymax = Math.max(ymax, y); }
  return passend({ x: [Math.floor(xmin - rand), Math.ceil(xmax + rand)], y: [Math.floor(ymin - rand), Math.ceil(ymax + rand)] });
}
/** Bei gleichen Achsen (640 × 400) die x-Spanne so weit vergrößern, dass der ganze y-Bereich sichtbar bleibt. */
function passend(b, verh = 640 / 400) {
  const noetig = (b.y[1] - b.y[0]) * verh, hat = b.x[1] - b.x[0];
  if (hat < noetig) { const m = (b.x[0] + b.x[1]) / 2; b.x = [m - noetig / 2, m + noetig / 2]; }
  return b;
}

/* =========================================================== Vektoren in der Ebene */
function vektoren2d(box, d) {
  const zeige = new Set(d.zeige || []);
  const vs = d.vektoren.map((v, i) => ({ x: v._x, y: v._y, label: v.label, farbe: v.farbe ? FARBE(v.farbe) : FARBE(i === 2 ? 4 : i + 1) }));
  const start = vs.map(v => [v.x, v.y]);
  let lam = d._faktor ?? 2;
  const lamStart = lam;
  const unveraendert = () => vs.every((v, i) => v.x === start[i][0] && v.y === start[i][1]);
  const zwei = vs.length >= 2;
  const pkte = vs.map(v => [v.x, v.y]);
  if (zwei) pkte.push([vs[0].x + vs[1].x, vs[0].y + vs[1].y], [vs[0].x - vs[1].x, vs[0].y - vs[1].y]);
  if (zeige.has("vielfaches")) pkte.push([lam * vs[0].x, lam * vs[0].y]);
  const b = bereich(pkte, 1.5);
  const werte = h("div", { class: "vf-werte", "aria-live": "polite" });
  const griffe = [];
  const k = koordinaten({ x: (d.x || b.x).map(Number), y: (d.y || b.y).map(Number), gleicheAchsen: true, klickbar: !!d.interaktiv, label: "Vektoren in der Ebene" }, (k) => {
    const [a, c] = vs;
    if (zeige.has("vielfaches")) {
      pfeil(k, 0, 0, lam * a.x, lam * a.y, "var(--plot-4)", "vl-pfeil breit");
      k.etikett(lam * a.x, lam * a.y, texHtml(`${bruchTex(lam)}\\,${a.label}`), "ueber klein");
    }
    if (zwei && (zeige.has("summe") || zeige.has("kette"))) {
      const sx = a.x + c.x, sy = a.y + c.y;
      if (zeige.has("summe")) { k.linie(a.x, a.y, sx, sy, "hilfslinie"); k.linie(c.x, c.y, sx, sy, "hilfslinie"); }
      if (zeige.has("kette")) pfeil(k, a.x, a.y, sx, sy, c.farbe, "vl-pfeil kette");
      pfeil(k, 0, 0, sx, sy, "var(--plot-3)", "vl-pfeil summe");
      k.etikett(sx, sy, texHtml(`${a.label} + ${c.label}`), "ueber klein");
    }
    if (zwei && zeige.has("differenz")) {
      pfeil(k, c.x, c.y, a.x, a.y, "var(--plot-4)", "vl-pfeil kette");
      k.etikett((a.x + c.x) / 2, (a.y + c.y) / 2, texHtml(`${a.label} - ${c.label}`), "klein");
    }
    vs.forEach((v) => {
      pfeil(k, 0, 0, v.x, v.y, v.farbe);
      k.etikett(v.x / 2, v.y / 2, texHtml(v.label), "vl-label");
    });
    griffe.forEach(g => g.lage());
  });
  if (d.interaktiv) {
    vs.forEach((v, i) => griffe.push(griff(k, { label: `Spitze von Vektor ${i + 1} (Pfeiltasten verschieben)`, holen: () => [v.x, v.y],
      setzen: (x, y) => { v.x = x; v.y = y; neu(); } })));
  }
  function anzeigen() {
    const ex = unveraendert();
    const z = [];
    vs.forEach((v, i) => {
      const t = ex ? d.vektoren[i]._tex : vekTex(v.x, v.y);
      let zeile = `${v.label} = ${t}`;
      if (zeige.has("norm")) {
        const [nt, ok] = normTex(v.x, v.y);
        zeile += `,\\quad |${v.label}| ${ex ? d.vektoren[i]._norm_tex : (ok ? "= " : "\\approx ") + nt}`;   // kurz genug für eine Zeile
      }
      z.push(zeile);
    });
    const [a, c] = vs;
    if (zwei && (zeige.has("summe") || zeige.has("kette"))) {
      const [nt, ok] = normTex(a.x + c.x, a.y + c.y);
      z.push(`${a.label} + ${c.label} = ${ex ? d._summe.tex : vekTex(a.x + c.x, a.y + c.y)}` + (zeige.has("norm") ? `,\\quad |${a.label} + ${c.label}| ${ex ? d._summe.norm_tex : (ok ? "= " : "\\approx ") + nt}` : ""));
    }
    if (zwei && zeige.has("differenz")) z.push(`${a.label} - ${c.label} = ${ex ? d._differenz.tex : vekTex(a.x - c.x, a.y - c.y)}`);
    if (zeige.has("vielfaches")) z.push(`${bruchTex(lam)} \\cdot ${a.label} = ${ex && lam === lamStart ? d._vielfaches.tex : vekTex(lam * a.x, lam * a.y)}`);
    if (zwei && zeige.has("skalarprodukt")) {
      const sp = a.x * c.x + a.y * c.y;
      z.push(`${a.label} \\cdot ${c.label} = ${bruchTex(a.x)} \\cdot ${bruchTex(c.x)} + ${bruchTex(a.y)} \\cdot ${bruchTex(c.y)} ${ex ? d._skalarprodukt.tex : "= " + bruchTex(sp)}`.replace(/\+ -/g, "- ")
        + (Math.abs(sp) < 1e-12 ? "\\quad(\\text{orthogonal})" : ""));
    }
    werte.replaceChildren(...z.map(wertZeile));
  }
  const neu = () => { k.neu(); anzeigen(); };
  box.append(h("div", { class: "vis-scroll" }, k.el), werte);
  if (zeige.has("vielfaches")) {
    box.append(h("div", { class: "regler-reihe" }, regler({ name: "Faktor λ", tex: "\\lambda", von: -3, bis: 3, schritt: 0.25, wert: lam,
      oninput: (v) => { lam = v; neu(); } }).el));
  }
  if (d.interaktiv) box.append(h("p", { class: "antwort-hinweis", text: "Ziehe die Kreise an den Pfeilspitzen – oder Tab und Pfeiltasten." }));
  griffe.forEach(g => g.lage());
  anzeigen();
}

/* =========================================================== Matrixmultiplikation (Falk-Schema) */
function matrixEl(eintraege, name, klasse) {
  const m = eintraege.length, n = eintraege[0].length;
  const gitter = h("div", { class: "mm-matrix " + klasse, style: { gridTemplateColumns: `repeat(${n}, auto)` }, role: "table", "aria-label": `Matrix ${name}` });
  const zellen = eintraege.map((zeile, i) => zeile.map((t, j) => {
    const z = h("div", { class: "mm-zelle", role: "cell", "data-i": i, "data-j": j, html: t === null ? "" : texHtml(t) });
    gitter.append(z);
    return z;
  }));
  return { el: h("div", { class: "mm-block" }, h("div", { class: "mm-name", html: texHtml(name) }), gitter), zellen, m, n };
}

function matrixMult(box, d) {
  const m = d._a.length, p = d._b[0].length;
  const A = matrixEl(d._a, "A", "a"), B = matrixEl(d._b, "B", "b");
  const C = matrixEl(d._c.map(z => z.map(() => null)), "C = A \\cdot B", "c");
  const falk = h("div", { class: "mm-falk" }, h("div", { class: "mm-leer" }), B.el, A.el, C.el);
  const rechnung = h("div", { class: "mm-rechnung", "aria-live": "polite" });
  const zaehler = h("span", { class: "zaehler" });
  const gesamt = m * p;
  let s = 0;
  const zur = knopf("◀ Zurück", () => zeigen(s - 1)), vor = knopf("Weiter ▶", () => zeigen(s + 1));
  const alle = knopf("Alle Einträge", () => zeigen(gesamt));
  C.zellen.flat().forEach((z) => {
    z.setAttribute("tabindex", "0");
    z.classList.add("klickbar");
    const ziel = Number(z.dataset.i) * p + Number(z.dataset.j) + 1;
    z.addEventListener("click", () => zeigen(ziel));
    z.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); zeigen(ziel); } });
  });
  function zeigen(n) {
    s = Math.max(1, Math.min(gesamt, n));
    const i = Math.floor((s - 1) / p), j = (s - 1) % p;
    A.zellen.forEach((z, r) => z.forEach(c => c.classList.toggle("hl-zeile", r === i)));
    B.zellen.forEach(z => z.forEach((c, sp) => c.classList.toggle("hl-spalte", sp === j)));
    C.zellen.forEach((z, r) => z.forEach((c, sp) => {
      const nr = r * p + sp + 1;
      c.innerHTML = nr <= s ? texHtml(d._c[r][sp]) : "";
      c.classList.toggle("hl-ziel", nr === s);
      c.classList.toggle("offen", nr > s);
      c.setAttribute("aria-label", nr <= s ? `c${r + 1}${sp + 1}` : `c${r + 1}${sp + 1} noch offen`);
    }));
    const summanden = (d._summanden || [])[i]?.[j];
    const mitte = summanden ? summanden.map((t, kk) => `\\htmlClass{mm-paar mm-paar-${kk % 4}}{${t}}`).join(" + ") : d._rechnungen[i][j];
    rechnung.innerHTML = texHtml(`c_{${i + 1}${j + 1}} = ${mitte} = ${d._c[i][j]}`, true);
    rechnung.append(h("div", { class: "vf-hinweis", html: inline(`Zeile ${i + 1} von $A$ mal Spalte ${j + 1} von $B$: Eintrag für Eintrag multiplizieren, dann addieren.`) }));
    zaehler.textContent = `Eintrag ${s} / ${gesamt}`;
    zur.disabled = s <= 1; vor.disabled = s >= gesamt;
  }
  box.append(h("div", { class: "vis-scroll" }, falk), rechnung, h("div", { class: "vis-steuer" }, zur, zaehler, vor, alle));
  zeigen(1);
}

/* =========================================================== Gauß-Verfahren */
function gauss(box, d) {
  const schritte = d._schritte || [];
  const sp = d._spalten ?? (schritte[0]?.matrix[0].length || 0);
  const tabelle = h("div", { class: "vis-scroll" });
  const op = h("div", { class: "gs-op", "aria-live": "polite" });
  const ende = h("div", { class: "vf-werte" });
  const zaehler = h("span", { class: "zaehler" });
  let i = 0;
  const zur = knopf("◀ Zurück", () => zeigen(i - 1)), vor = knopf("Weiter ▶", () => zeigen(i + 1));
  function zeigen(n) {
    i = Math.max(0, Math.min(schritte.length - 1, n));
    const st = schritte[i];
    const t = h("table", { class: "gs-matrix", "aria-label": "Erweiterte Koeffizientenmatrix" });
    st.matrix.forEach((zeile, r) => {
      const tr = h("tr", { class: st.zeilen.includes(r) ? "geaendert" : "" }, h("th", { scope: "row", html: texHtml(`Z_{${r + 1}}`) }));
      zeile.forEach((w, c) => {
        const piv = st.pivot && st.pivot[0] === r && st.pivot[1] === c;
        tr.append(h("td", { class: (c === sp && sp < zeile.length ? "rechts " : "") + (piv ? "pivot" : ""), html: texHtml(w), title: piv ? "Pivotelement" : null }));
      });
      t.append(tr);
    });
    tabelle.replaceChildren(t);
    op.innerHTML = i === 0 ? "Ausgangsmatrix" + (sp < st.matrix[0].length ? " (links A, rechts vom Strich die rechte Seite)" : "")
      : texHtml(st.op) + `<span class="vf-hinweis"> – ${st.zeilen.length > 1 ? "Zeilen tauschen" : "Zeilenumformung"}${st.pivot ? `, Pivot in Spalte ${st.pivot[1] + 1}` : ""}</span>`;
    ende.replaceChildren();
    if (i === schritte.length - 1) {
      ende.append(wertZeile(`\\operatorname{Rang} = ${d._rang}`));
      if (d._loesung_tex) ende.append(wertZeile(d._loesung_tex));
    }
    zaehler.textContent = `Schritt ${i + 1} / ${schritte.length}`;
    zur.disabled = i === 0; vor.disabled = i === schritte.length - 1;
  }
  box.append(op, tabelle, ende, h("div", { class: "vis-steuer" }, zur, zaehler, vor));
  zeigen(0);
}

/* =========================================================== Komplexe Zahlenebene */
function komplexInfo(re, im) {
  const r = Math.hypot(re, im), phi = Math.atan2(im, re);
  return { re, im, r, phi };
}
function komplexTex(re, im) {
  const rt = bruchTex(re), it = bruchTex(Math.abs(im));
  if (Math.abs(im) < 1e-12) return rt;
  const ip = it === "1" ? "i" : `${it}\\,i`;
  if (Math.abs(re) < 1e-12) return (im < 0 ? "-" : "") + ip;
  return `${rt} ${im < 0 ? "-" : "+"} ${ip}`;
}
function polarZeile(name, info, exakt) {
  // exakt: Python-Info (_z/_w/_ergebnis) für die Startwerte, sonst numerisch
  if (exakt) {
    const e = exakt;
    if (e.arg_tex === null) return `${name} = 0`;
    const grad = Math.round(e.arg_grad * 100) / 100;
    return [`${name} = ${e.tex} ${e.polar_exakt ? "=" : "\\approx"} ${e.polar_tex}`,
      `|${name}| ${e.betrag_exakt ? "=" : "\\approx"} ${e.betrag_tex},\\quad \\varphi_{${name}} ${e.arg_exakt ? "=" : "\\approx"} ${e.arg_tex} \\mathrel{\\widehat=} ${zTex(grad, 2)}^\\circ`];
  }
  const [bt, ok] = normTex(info.re, info.im);
  if (info.r < 1e-12) return `${name} = 0`;
  return [`${name} ${nenner(info.re, info.im) ? "=" : "\\approx"} ${komplexTex(info.re, info.im)}`, `|${name}| ${ok ? "=" : "\\approx"} ${bt},\\quad \\varphi_{${name}} \\approx ${zTex(info.phi * 180 / Math.PI, 1)}^\\circ`];
}

const OP_TEX = { plus: "z + w", minus: "z - w", mal: "z \\cdot w", geteilt: "\\frac{z}{w}", konjugiert: "\\bar{z}" };

/* Zusätzliche Zahlen (punkte), Konjugierte und Betragskreise; z (falls vorhanden) zählt mit. */
function extraBereich(d, z) {
  const pk = [];
  for (const p of [...(z ? [{ re: z.re, im: z.im }] : []), ...(d._punkte || [])]) {
    pk.push([p.re, p.im], [p.re, -p.im]);
    if (d.betragskreis) { const r = Math.hypot(p.re, p.im); pk.push([r, r], [-r, -r]); }
  }
  return pk;
}
function extraZeichnen(k, d, z) {
  const P = d._punkte || [];
  const alle = [...(z ? [{ re: z.re, im: z.im, label: "z", farbe: 1, haupt: true }] : []), ...P];
  const farbe = (p) => FARBE(p.farbe);
  if (d.betragskreis) {
    const gesehen = new Set();
    for (const p of alle) {
      const r = Math.hypot(p.re, p.im), schluessel = r.toFixed(6);
      if (r < 1e-9 || gesehen.has(schluessel)) continue;
      gesehen.add(schluessel);
      const c = k.kreis(0, 0, r, "betragskreis");
      c.style.stroke = farbe(p);
    }
  }
  if (d.konjugiert) {
    for (const p of alle) {
      if (Math.abs(p.im) < 1e-12) continue;
      k.linie(p.re, p.im, p.re, -p.im, "hilfslinie");
      if (d.pfeile === false && !p.haupt) k.punkt(p.re, -p.im, { klasse: "punkt konj", r: 5 }).style.fill = farbe(p);
      else pfeil(k, 0, 0, p.re, -p.im, farbe(p), "vl-pfeil konj");
      k.etikett(p.re, -p.im, texHtml(`\\overline{${p.label}}`), (p.im > 0 ? "unten" : "ueber") + " klein");
    }
  }
  for (const p of P) {
    if (d.pfeile === false) k.punkt(p.re, p.im, { r: 6 }).style.fill = farbe(p);
    else pfeil(k, 0, 0, p.re, p.im, farbe(p));
    k.etikett(p.re, p.im, texHtml(p.label), "ueber klein");
  }
}
function extraZeilen(d) {
  return (d._punkte || []).map(p => {
    const bt = `|${p.label}| ${p.betrag_exakt ? "=" : "\\approx"} ${p.betrag_tex}`;
    return `${p.label} = ${p.tex},\\quad ${bt}` + (d.konjugiert ? `,\\quad \\overline{${p.label}} = ${p.konj_tex}` : "");
  });
}

/** Nur Punkte: Zahlen als Pfeile oder Punkte in der Gaußschen Zahlenebene. */
function komplexePunkte(box, d) {
  const auto = bereich(extraBereich(d, null), 1);
  const k = koordinaten({ x: (d.x || auto.x).map(Number), y: (d.y || auto.y).map(Number), gleicheAchsen: true,
    xName: "Re", yName: "Im", label: d._alt }, (k) => extraZeichnen(k, d, null));
  const werte = h("div", { class: "vf-werte", "aria-live": "polite" }, extraZeilen(d).map(wertZeile));
  werte.append(h("div", { class: "vf-hinweis", text: "Betrag = Länge des Pfeils." + (d.konjugiert ? " Konjugieren = Spiegeln an der reellen Achse." : "") }));
  box.append(h("div", { class: "vis-scroll" }, k.el), werte);
}

function komplexeEbene(box, d) {
  if (!d._z) { komplexePunkte(box, d); return; }
  const op = d.op || "keine";
  const z = { re: d._z.re, im: d._z.im }, w = d._w ? { re: d._w.re, im: d._w.im } : null;
  const start = JSON.stringify([z, w]);
  const ergebnis = () => {
    if (op === "konjugiert") return { re: z.re, im: -z.im };
    if (!w) return null;
    if (op === "plus") return { re: z.re + w.re, im: z.im + w.im };
    if (op === "minus") return { re: z.re - w.re, im: z.im - w.im };
    if (op === "mal") return { re: z.re * w.re - z.im * w.im, im: z.re * w.im + z.im * w.re };
    if (op === "geteilt") { const n = w.re * w.re + w.im * w.im; return n ? { re: (z.re * w.re + z.im * w.im) / n, im: (z.im * w.re - z.re * w.im) / n } : null; }
    return null;
  };
  const pk = [[z.re, z.im]];
  if (w) pk.push([w.re, w.im]);
  const e0 = ergebnis();
  if (e0) pk.push([e0.re, e0.im]);
  pk.push(...extraBereich(d, null), ...(d.konjugiert || d.betragskreis ? extraBereich({ betragskreis: d.betragskreis }, z) : []));
  const auto = bereich(pk, 1);
  const werte = h("div", { class: "vf-werte", "aria-live": "polite" });
  const griffe = [];
  const k = koordinaten({ x: (d.x || auto.x).map(Number), y: (d.y || auto.y).map(Number), gleicheAchsen: true, klickbar: !!d.interaktiv,
    xName: "Re", yName: "Im", label: "Komplexe Zahlenebene" }, (k) => {
    const e = ergebnis();
    const winkel = (c, rPx, klasse) => { const phi = Math.atan2(c.im, c.re); if (Math.hypot(c.re, c.im) > 1e-9) k.bogen(0, 0, rPx, 0, phi, klasse); };
    if (op === "keine") {
      k.linie(z.re, z.im, z.re, 0, "hilfslinie"); k.linie(z.re, z.im, 0, z.im, "hilfslinie");
      k.etikett(z.re, 0, texHtml(`\\operatorname{Re} z`), z.im >= 0 ? "unten klein" : "oben klein");
      k.etikett(0, z.im, texHtml(`\\operatorname{Im} z`), z.re >= 0 ? "links klein" : "rechts klein");
    }
    if (op === "konjugiert" && e) k.linie(z.re, z.im, e.re, e.im, "hilfslinie");
    if (op === "plus" && w && e) { k.linie(z.re, z.im, e.re, e.im, "hilfslinie"); k.linie(w.re, w.im, e.re, e.im, "hilfslinie"); }
    if (op === "minus" && w) pfeil(k, w.re, w.im, z.re, z.im, "var(--plot-4)", "vl-pfeil kette");
    if (op === "keine" || op === "konjugiert") { winkel(z, 34, "winkelbogen"); }
    if (op === "mal" || op === "geteilt") {
      winkel(z, 30, "winkelbogen b1"); winkel(w, 42, "winkelbogen b3"); if (e) winkel(e, 56, "winkelbogen b2");
    }
    if (e) {
      pfeil(k, 0, 0, e.re, e.im, "var(--plot-2)", "vl-pfeil breit");
      k.etikett(e.re, e.im, texHtml(OP_TEX[op]), "ueber klein");
    }
    if (w) { pfeil(k, 0, 0, w.re, w.im, "var(--plot-3)"); k.etikett(w.re, w.im, texHtml("w"), "ueber klein"); }
    pfeil(k, 0, 0, z.re, z.im, "var(--plot-1)");
    k.etikett(z.re, z.im, texHtml("z"), "ueber klein");
    if (d._punkte || d.konjugiert || d.betragskreis) extraZeichnen(k, d, z);
    griffe.forEach(g => g.lage());
  });
  function anzeigen() {
    const ex = JSON.stringify([z, w]) === start;
    const e = ergebnis();
    const zeilen = [polarZeile("z", komplexInfo(z.re, z.im), ex && d._z)].flat();
    if (w) zeilen.push(...[polarZeile("w", komplexInfo(w.re, w.im), ex && d._w)].flat());
    if (e && op !== "keine") {
      const exE = ex && d._ergebnis;
      if (exE) zeilen.push(`${OP_TEX[op]} ${exE.exakt ? "=" : "\\approx"} ${exE.tex}`, ...(exE.arg_tex !== null ? [`${OP_TEX[op]} ${exE.polar_exakt ? "=" : "\\approx"} ${exE.polar_tex}`] : []));
      else zeilen.push(`${OP_TEX[op]} ${nenner(e.re, e.im) ? "=" : "\\approx"} ${komplexTex(e.re, e.im)}`);
    }
    zeilen.push(...extraZeilen(d));
    werte.replaceChildren(...zeilen.map(wertZeile));
    const regel = { mal: "Multiplizieren = Drehstreckung: Beträge multiplizieren, Winkel addieren.",
      geteilt: "Dividieren: Beträge teilen, Winkel subtrahieren.", plus: "Addieren wie Vektoren: Pfeile aneinanderhängen (Parallelogramm).",
      minus: "Subtrahieren: Pfeil von w nach z.", konjugiert: "Konjugieren = Spiegeln an der reellen Achse: Imaginärteil wechselt das Vorzeichen.",
      keine: "Betrag = Länge des Pfeils, Argument = Winkel zur positiven reellen Achse." }[op];
    werte.append(h("div", { class: "vf-hinweis", text: regel }));
  }
  if (d.interaktiv) {
    griffe.push(griff(k, { label: "Zahl z verschieben (Pfeiltasten)", holen: () => [z.re, z.im], setzen: (x, y) => { z.re = x; z.im = y; neu(); } }));
    if (w) griffe.push(griff(k, { label: "Zahl w verschieben (Pfeiltasten)", holen: () => [w.re, w.im], setzen: (x, y) => { w.re = x; w.im = y; neu(); } }));
  }
  const neu = () => { k.neu(); anzeigen(); };
  box.append(h("div", { class: "vis-scroll" }, k.el), werte);
  if (d.interaktiv) box.append(h("p", { class: "antwort-hinweis", text: "Ziehe z oder w – oder Tab und Pfeiltasten (Schritt 0,5)." }));
  griffe.forEach(g => g.lage());
  anzeigen();
}

export const BAUER = { vektoren2d, matrix_mult: matrixMult, gauss, komplexe_ebene: komplexeEbene };
