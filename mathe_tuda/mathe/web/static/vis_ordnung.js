// Relationen und Ordnungen: graph_gerichtet, hasse, aequivalenz_klassen.
// Knotentexte, Positionen (Einheiten, y nach unten), Kanten und Eigenschaften kommen aus visuals.py;
// hier wird nur gezeichnet (SVG, Farben über Theme-Variablen in vis_ordnung.css).
import { h, svg, inline } from "./util.js";
import { texHtml } from "./formel.js";

if (!document.getElementById("vis-ordnung-css")) {
  document.head.append(h("link", { id: "vis-ordnung-css", rel: "stylesheet", href: new URL("./vis_ordnung.css", import.meta.url).href }));
}

let uid = 0;

/* ---------- gemeinsame Bausteine ---------- */

/** Anzeigetext im Knoten: lange Mengen ohne Leerzeichen nach dem Komma, damit sie in den Kreis passen. */
const kurz = (t) => (t.length > 6 ? t.replace(/, /g, ",") : t);
const schriftGroesse = (t) => (kurz(t).length > 7 ? 13.5 : kurz(t).length > 4 ? 15.5 : 18);
const radiusVon = (t) => Math.max(19, Math.ceil(kurz(t).length * schriftGroesse(t) * 0.52 / 2) + 10);

/** Einheiten -> Pixel. extent: {x0, x1, y0, y1} in Einheiten, rand: Platz um den Inhalt (Pixel). */
function geometrie(knoten, extent, { rand, maxSkala = 100, wMax = 620, hMax = 440 }) {
  const rmax = Math.max(...knoten.map(k => radiusVon(k.text)));
  let minAbst = Infinity;
  for (let i = 0; i < knoten.length; i++) for (let j = i + 1; j < knoten.length; j++) {
    const a = Math.hypot(knoten[i].x - knoten[j].x, knoten[i].y - knoten[j].y);
    if (a > 1e-6) minAbst = Math.min(minAbst, a);
  }
  const sx = extent.x1 - extent.x0, sy = extent.y1 - extent.y0;
  let skala = Math.min(maxSkala, sx > 1e-6 ? (wMax - 2 * rand) / sx : Infinity, sy > 1e-6 ? (hMax - 2 * rand) / sy : Infinity);
  if (!Number.isFinite(skala)) skala = maxSkala;
  if (Number.isFinite(minAbst)) skala = Math.max(skala, (2 * rmax + 16) / minAbst);
  const W = Math.max(Math.ceil(sx * skala + 2 * rand), 2 * rand + 2 * rmax, 240), H = Math.max(Math.ceil(sy * skala + 2 * rand), 2 * rand + 2 * rmax);
  const mx = (W - sx * skala) / 2 - extent.x0 * skala, my = (H - sy * skala) / 2 - extent.y0 * skala;
  return { W, H, skala, rmax, px: (k) => [mx + k.x * skala, my + k.y * skala] };
}

const umfang = (knoten) => ({
  x0: Math.min(...knoten.map(k => k.x)), x1: Math.max(...knoten.map(k => k.x)),
  y0: Math.min(...knoten.map(k => k.y)), y1: Math.max(...knoten.map(k => k.y)),
});

/** Pfeilspitze mit fester Größe (unabhängig von der Linienbreite). */
function marker(id, klasse) {
  return svg("marker", { id, viewBox: "0 0 10 10", refX: 9, refY: 5, markerUnits: "userSpaceOnUse", markerWidth: 12, markerHeight: 12, orient: "auto" },
    svg("path", { d: "M0,0 L10,5 L0,10 z", class: klasse }));
}

function wuerfel(box, W, H, label, klasse) {
  const s = svg("svg", { class: "og-svg " + klasse, viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": label });
  const buehne = h("div", { class: "og-buehne" }, s);
  buehne.style.maxWidth = W + "px";
  box.append(buehne);
  return s;
}

function knotenZeichnen(g, k, pos, klasse, extra = {}) {
  const [x, y] = pos;
  const r = radiusVon(k.text);
  const knoten = svg("g", { class: "og-knoten " + klasse });
  knoten.append(svg("circle", { class: "og-kreis", cx: x, cy: y, r }),
    svg("text", { class: "og-text", x, y: y + schriftGroesse(k.text) * 0.36, "text-anchor": "middle", style: `font-size:${schriftGroesse(k.text)}px` }, kurz(k.text)));
  for (const [a, v] of Object.entries(extra)) knoten.setAttribute(a, v);
  g.append(knoten);
  return knoten;
}

/** Pfeile (gerichtet) zwischen Knoten: gerade, gegenläufige Paare versetzt, Schleifen nach außen. */
function pfeileZeichnen(g, knoten, pos, kanten, { markerId, mittenVon = null, klasseVon = () => "" }) {
  const paarSet = new Set(kanten.map(([a, b]) => `${a}>${b}`));
  const mitte = [pos.reduce((s, p) => s + p[0], 0) / pos.length, pos.reduce((s, p) => s + p[1], 0) / pos.length];
  const r = knoten.map(k => radiusVon(k.text));
  const elemente = [];
  kanten.forEach(([a, b], i) => {
    const kl = klasseVon(a, b, i);
    const m = `url(#${markerId}${kl.includes("markiert") ? "m" : kl.includes("grau") ? "g" : ""})`;
    let d;
    if (a === b) {
      const [x, y] = pos[a];
      const m0 = mittenVon ? mittenVon(a) : mitte;
      let vx = x - m0[0], vy = y - m0[1];
      if (Math.hypot(vx, vy) < 1e-6) { vx = 0; vy = -1; }
      const th = Math.atan2(vy, vx), ra = r[a], L = ra + 44, da = 0.5, dc = 0.62;
      const P = (rad, w) => `${(x + rad * Math.cos(th + w)).toFixed(1)},${(y + rad * Math.sin(th + w)).toFixed(1)}`;
      d = `M${P(ra, -da)} C${P(L, -dc)} ${P(L, dc)} ${P(ra + 1.5, da)}`;
    } else {
      const [x1, y1] = pos[a], [x2, y2] = pos[b];
      const len = Math.hypot(x2 - x1, y2 - y1), dx = (x2 - x1) / len, dy = (y2 - y1) / len;
      if (paarSet.has(`${b}>${a}`)) {
        const off = Math.max(14, Math.min(26, len * 0.17));
        const cx = (x1 + x2) / 2 - dy * off * 2, cy = (y1 + y2) / 2 + dx * off * 2;   // Kontrollpunkt; Kurve liegt halb so weit weg
        const u1 = [cx - x1, cy - y1], l1 = Math.hypot(...u1), u2 = [cx - x2, cy - y2], l2 = Math.hypot(...u2);
        d = `M${(x1 + u1[0] / l1 * r[a]).toFixed(1)},${(y1 + u1[1] / l1 * r[a]).toFixed(1)} Q${cx.toFixed(1)},${cy.toFixed(1)} ${(x2 + u2[0] / l2 * (r[b] + 1.5)).toFixed(1)},${(y2 + u2[1] / l2 * (r[b] + 1.5)).toFixed(1)}`;
      } else {
        d = `M${(x1 + dx * r[a]).toFixed(1)},${(y1 + dy * r[a]).toFixed(1)} L${(x2 - dx * (r[b] + 1.5)).toFixed(1)},${(y2 - dy * (r[b] + 1.5)).toFixed(1)}`;
      }
    }
    const p = svg("path", { class: "og-pfeil " + kl, d, "marker-end": m });
    g.append(p);
    elemente.push(p);
  });
  return elemente;
}

function markerSatz(id) {
  return svg("defs", null, marker(id, "og-spitze"), marker(id + "m", "og-spitze markiert"), marker(id + "g", "og-spitze grau"));
}

/* =========================================================== gerichteter Graph */
function graphGerichtet(box, d) {
  const id = "gg" + (++uid);
  const K = d._knoten, E = d._kanten;
  const schleifen = E.some(([a, b]) => a === b);
  const geo = geometrie(K, umfang(K), { rand: Math.max(...K.map(k => radiusVon(k.text))) + (schleifen ? 58 : 22), maxSkala: 150, wMax: 700, hMax: 640 });
  const s = wuerfel(box, geo.W, geo.H, d._alt, "og-graph");
  s.append(markerSatz(id));
  const pos = K.map(geo.px);
  const markK = new Set(d._markiert_knoten), markE = new Set(d._markiert_kanten.map(([a, b]) => `${a}>${b}`));
  const g = svg("g");
  s.append(g);
  pfeileZeichnen(g, K, pos, E, { markerId: id, klasseVon: (a, b) => (markE.has(`${a}>${b}`) ? "markiert" : "") });
  K.forEach((k, i) => knotenZeichnen(g, k, pos[i], markK.has(i) ? "markiert" : ""));
}

/* =========================================================== Hasse-Diagramm */
function hasse(box, d) {
  const K = d._knoten, E = d._kanten, T = d._teilmenge ? new Set(d._teilmenge) : null;
  const geo = geometrie(K, umfang(K), { rand: Math.max(...K.map(k => radiusVon(k.text))) + 30, maxSkala: 96 });
  const s = wuerfel(box, geo.W, geo.H, d._alt, "og-hasse");
  const pos = K.map(geo.px);
  const g = svg("g");
  s.append(g);
  const sup = d.sup ? d._sup : null, inf = d.inf ? d._inf : null;
  const obere = new Set(d.schranken ? d._obere : []), untere = new Set(d.schranken ? d._untere : []);
  for (const [a, b] of E) {
    const [x1, y1] = pos[a], [x2, y2] = pos[b];
    const len = Math.hypot(x2 - x1, y2 - y1), dx = (x2 - x1) / len, dy = (y2 - y1) / len;
    const aktiv = !T || (T.has(a) && T.has(b));
    g.append(svg("line", { class: "og-linie" + (aktiv ? "" : " grau"), x1: x1 + dx * radiusVon(K[a].text), y1: y1 + dy * radiusVon(K[a].text), x2: x2 - dx * radiusVon(K[b].text), y2: y2 - dy * radiusVon(K[b].text) }));
  }
  K.forEach((k, i) => {
    const kl = [T ? (T.has(i) ? "schwarz" : "grau") : "schwarz"];
    if (i === sup) kl.push("sup");
    if (i === inf) kl.push("inf");
    if (obere.has(i) && i !== sup) kl.push("obere");
    if (untere.has(i) && i !== inf) kl.push("untere");
    knotenZeichnen(g, k, pos[i], kl.join(" "));
    const tags = [i === sup ? "sup" : null, i === inf ? "inf" : null].filter(Boolean);
    if (tags.length) {
      const [x, y] = pos[i], r = radiusVon(k.text);
      g.append(svg("text", { class: "og-tag " + tags[0], x, y: y + r + 15, "text-anchor": "middle" }, tags.join(" = ")));
    }
  });
  if (T || d._info.length) {
    const legende = h("div", { class: "og-legende" });
    if (T) legende.append(chip("schwarz", "Teilmenge T"), chip("grau", "übrige Elemente"));
    if (sup !== null) legende.append(chip("sup", "Supremum"));
    if (inf !== null) legende.append(chip("inf", "Infimum"));
    if (obere.size) legende.append(chip("obere", "obere Schranke"));
    if (untere.size) legende.append(chip("untere", "untere Schranke"));
    box.append(legende);
  }
  if (d._info.length) box.append(h("div", { class: "og-info", "aria-live": "polite" }, d._info.map(t => h("p", { html: inline(t) }))));
}

const chip = (klasse, text) => h("span", { class: "og-chip" }, h("i", { class: "og-farbe " + klasse }), h("span", { text }));

/* =========================================================== Äquivalenzklassen */
function aequivalenzKlassen(box, d) {
  const id = "aq" + (++uid);
  const K = d._knoten, C = d._klassen, E = d._kanten;
  const ext = { x0: Math.min(...C.map(c => c.x - c.r)), x1: Math.max(...C.map(c => c.x + c.r)), y0: Math.min(...C.map(c => c.y - c.r)), y1: Math.max(...C.map(c => c.y + c.r)) };
  const rmax = Math.max(...K.map(k => radiusVon(k.text)));
  const geo = geometrie(K, ext, { rand: 30, maxSkala: 100 });
  const oben = 22;                       // Platz für die Klassennamen über den Bereichen
  const s = wuerfel(box, geo.W, geo.H + oben, d._alt, "og-aequiv");
  s.append(markerSatz(id));
  const pos = K.map(geo.px).map(([x, y]) => [x, y + oben]);
  const farbe = (ki) => `k${(ki % 4) + 1}${ki >= 4 ? " alt" : ""}`;
  const g = svg("g");
  s.append(g);
  C.forEach((c, ki) => {
    const [cx, cy] = geo.px({ x: c.x, y: c.y });
    const rad = Math.max(c.r * geo.skala, 0);
    g.append(svg("circle", { class: "og-region " + farbe(ki), cx, cy: cy + oben, r: Math.max(rad, rmax + 10) }));
    g.append(svg("text", { class: "og-klassenname " + farbe(ki), x: cx, y: cy + oben - Math.max(rad, rmax + 10) - 7, "text-anchor": "middle" }, c.name));
  });
  if (E.length) pfeileZeichnen(g, K, pos, E, { markerId: id, mittenVon: (i) => { const c = C[K[i].klasse]; return geo.px({ x: c.x, y: c.y }).map((v, j) => v + (j ? oben : 0)); } });
  K.forEach((k, i) => knotenZeichnen(g, k, pos[i], farbe(k.klasse) + (k.vertreter ? " vertreter" : "")));
  box.append(h("div", { class: "og-klassenliste" }, C.map((c, i) => h("div", { class: "og-zeile " + farbe(i).split(" ")[0] }, h("span", { class: "og-punkt" }), h("span", { html: texHtml(c.tex) })))));
  box.append(h("p", { class: "antwort-hinweis", text: "Jedes Element liegt in genau einer Klasse. Ausgefüllt: der Vertreter der Klasse." + (E.length ? " Pfeile: Die Relation gilt zwischen allen Elementen derselben Klasse." : "") }));
}

export const BAUER = { graph_gerichtet: graphGerichtet, hasse, aequivalenz_klassen: aequivalenzKlassen };
