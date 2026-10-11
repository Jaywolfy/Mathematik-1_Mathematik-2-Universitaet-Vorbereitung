// Diskrete Visuals: venn, wahrheitstabelle, relation_graph, pascal, euklid, modulo_uhr, induktion_domino, folge.
// Exakte Daten (Regionen, Tabellen, Eigenschaften, n0 …) kommen aus visuals.py; hier wird nur gezeichnet.
import { h, svg, inline, reduziert } from "./util.js";
import { texHtml } from "./formel.js";
import { koordinaten, auswerten, regler, zahlText } from "./plot.js";
import { knopf } from "./visuals.js";

if (!document.getElementById("vis-diskret-css")) {
  document.head.append(h("link", { id: "vis-diskret-css", rel: "stylesheet", href: new URL("./vis_diskret.css", import.meta.url).href }));
}

let uid = 0;
const neueId = (p) => `${p}${++uid}`;

/** Schritt-Steuerung: Zurück / Zähler / Weiter / Alles. zeigen(i) zeichnet Zustand i (0 … anzahl). */
function schrittSteuerung(anzahl, zeigen, { start = 0, alle = true, weiterText = "Weiter ▶" } = {}) {
  let i = start;
  const zaehler = h("span", { class: "zaehler", "aria-live": "polite" });
  const zur = knopf("◀ Zurück", () => setzen(i - 1));
  const vor = knopf(weiterText, () => setzen(i + 1), { class: "btn btn-sm btn-primary" });
  const ganz = alle ? knopf("Alles zeigen", () => setzen(anzahl)) : null;
  function setzen(k) {
    i = Math.max(0, Math.min(anzahl, k));
    zur.disabled = i === 0; vor.disabled = i === anzahl;
    if (ganz) ganz.disabled = i === anzahl;
    zaehler.textContent = `${i} / ${anzahl}`;
    zeigen(i);
  }
  return { el: h("div", { class: "vis-steuer" }, zur, zaehler, vor, ganz), setzen, get i() { return i; } };
}

/** Pfeilspitze für SVG-Pfeile. */
function pfeilMarker(id, klasse = "pfeilspitze") {
  return svg("marker", { id, viewBox: "0 0 10 10", refX: 8, refY: 5, markerWidth: 7, markerHeight: 7, orient: "auto-start-reverse" },
    svg("path", { d: "M0,0 L10,5 L0,10 z", class: klasse }));
}

/** SVG-Koordinaten eines Zeiger-Ereignisses (viewBox W×H, Seitenverhältnis bleibt). */
function svgPunkt(s, e, W, H) {
  const r = s.getBoundingClientRect();
  return [(e.clientX - r.left) / r.width * W, (e.clientY - r.top) / r.height * H];
}

/* =========================================================== Venn-Diagramm */
function venn(box, d) {
  const n = d._n, namen = d._namen, id = neueId("venn");
  const W = 480, H = n === 3 ? 380 : 290;
  const r = n === 3 ? 100 : 100;
  const kreise = n === 2
    ? [{ x: W / 2 - 62, y: H / 2 + 10 }, { x: W / 2 + 62, y: H / 2 + 10 }]
    : [{ x: W / 2 - 58, y: 148 }, { x: W / 2 + 58, y: 148 }, { x: W / 2, y: 246 }];
  const rand = { x: 8, y: 8, w: W - 16, h: H - 16 };
  const maskeBei = (x, y) => kreise.reduce((m, k, i) => m + ((x - k.x) ** 2 + (y - k.y) ** 2 < r * r ? 1 << i : 0), 0);
  const regionen = d._regionen || [];
  const markiert = new Set(d._markiert || []);
  const s = svg("svg", { class: "venn-svg", viewBox: `0 0 ${W} ${H}`, role: "img",
    "aria-label": `Mengendiagramm mit den Mengen ${namen.join(", ")}` });
  const defs = svg("defs");
  s.append(defs);
  kreise.forEach((k, i) => defs.append(svg("clipPath", { id: `${id}c${i}` }, svg("circle", { cx: k.x, cy: k.y, r }))));
  const flaechen = new Map();
  for (const reg of regionen) {
    const m = reg.maske;
    let el = svg("rect", { class: "venn-flaeche", x: rand.x, y: rand.y, width: rand.w, height: rand.h });
    kreise.forEach((k, i) => { if (m >> i & 1) el = svg("g", { "clip-path": `url(#${id}c${i})` }, el); });
    const aussen = kreise.filter((k, i) => !(m >> i & 1));
    if (aussen.length) {
      defs.append(svg("mask", { id: `${id}m${m}`, maskUnits: "userSpaceOnUse", x: 0, y: 0, width: W, height: H },
        svg("rect", { x: 0, y: 0, width: W, height: H, fill: "#fff" }),
        ...aussen.map(k => svg("circle", { cx: k.x, cy: k.y, r, fill: "#000" }))));
      el = svg("g", { mask: `url(#${id}m${m})` }, el);
    }
    const g = svg("g", { class: "venn-region" + (markiert.has(m) ? " markiert" : "") }, el);
    flaechen.set(m, g);
    s.append(g);
  }
  s.append(svg("rect", { class: "venn-rand", x: rand.x, y: rand.y, width: rand.w, height: rand.h, rx: 10 }));
  if (d.universum) s.append(svg("text", { class: "venn-name", x: rand.x + 12, y: rand.y + 24 }, d.universum_name || "G"));
  kreise.forEach((k, i) => s.append(svg("circle", { class: `venn-kreis k${i + 1}`, cx: k.x, cy: k.y, r })));
  // Mengennamen außen an den Kreisen
  const winkel = n === 2 ? [-140, -40] : [-150, -30, 90];
  kreise.forEach((k, i) => {
    const w = winkel[i] * Math.PI / 180, a = r + 16;
    s.append(svg("text", { class: `venn-name k${i + 1}`, x: k.x + a * Math.cos(w), y: k.y + a * Math.sin(w) + 6, "text-anchor": "middle" }, namen[i]));
  });
  // Elemente in ihre Regionen setzen (Kandidatenpunkte mit größtem Abstand zu allen Rändern)
  const kandidaten = new Map();
  for (let y = rand.y + 14; y < rand.y + rand.h - 8; y += 4) {
    for (let x = rand.x + 14; x < rand.x + rand.w - 14; x += 4) {
      if (y < rand.y + 36 && x < rand.x + 40) continue;   // Platz für den Namen der Grundmenge
      const abst = Math.min(...kreise.map(k => Math.abs(Math.hypot(x - k.x, y - k.y) - r)), x - rand.x, rand.x + rand.w - x, y - rand.y, rand.y + rand.h - y);
      if (abst < 12) continue;
      const m = maskeBei(x, y);
      if (!kandidaten.has(m)) kandidaten.set(m, []);
      kandidaten.get(m).push({ x, y, abst });
    }
  }
  for (const reg of regionen) {
    const kand = (kandidaten.get(reg.maske) || []).sort((a, b) => b.abst - a.abst);
    if (!reg.elemente.length || !kand.length) continue;
    let gewaehlt = [];
    for (const abstand of [30, 25, 20, 16, 12]) {
      gewaehlt = [];
      for (const p of kand) {
        if (gewaehlt.every(q => Math.hypot(p.x - q.x, (p.y - q.y) * 1.4) >= abstand)) gewaehlt.push(p);
        if (gewaehlt.length === reg.elemente.length) break;
      }
      if (gewaehlt.length === reg.elemente.length) break;
    }
    reg.elemente.forEach((e, j) => {
      const p = gewaehlt[j] || kand[j % kand.length];
      s.append(svg("text", { class: "venn-el", x: p.x, y: p.y + 5, "text-anchor": "middle" }, e));
    });
  }
  const info = h("div", { class: "venn-info", "aria-live": "polite" });
  const stdInfo = () => {
    if (!d._markiert) return `${inline("Tippe auf eine Fläche.")}`;
    const zusatz = d._markiert_unvollstaendig ? " <span class='chip gelb'>ohne Grundmenge: nur die gezeigten Elemente</span>" : "";
    return `<span class="chip primary">markiert</span> ${texHtml(`${d._markiert_tex} = ${d._markiert_elemente}`)}${zusatz}`;
  };
  let aktiv = null;
  function waehlen(m) {
    aktiv = m;
    flaechen.forEach((g, mm) => g.classList.toggle("aktiv", mm === m));
    const reg = regionen.find(x => x.maske === m);
    info.innerHTML = reg ? `<span class="chip">Fläche</span> ${texHtml(`${reg.tex} = ${reg.elemente_tex}`)}` : stdInfo();
  }
  box.append(h("div", { class: "venn-buehne" }, s), info);
  waehlen(null);
  if (d.interaktiv !== false) {
    const reihenfolge = regionen.map(x => x.maske);
    s.tabIndex = 0;
    s.style.cursor = "pointer";
    s.addEventListener("click", (e) => {
      const [x, y] = svgPunkt(s, e, W, H);
      if (x < rand.x || x > rand.x + rand.w || y < rand.y || y > rand.y + rand.h) return;
      const m = maskeBei(x, y);
      waehlen(aktiv === m ? null : m);
    });
    s.addEventListener("keydown", (e) => {
      const i = reihenfolge.indexOf(aktiv);
      if (["ArrowRight", "ArrowDown"].includes(e.key)) waehlen(reihenfolge[(i + 1) % reihenfolge.length]);
      else if (["ArrowLeft", "ArrowUp"].includes(e.key)) waehlen(reihenfolge[(i - 1 + reihenfolge.length) % reihenfolge.length]);
      else if (e.key === "Escape") waehlen(null);
      else return;
      e.preventDefault(); e.stopPropagation();
    });
    box.append(h("p", { class: "antwort-hinweis", text: "Tippe auf eine Fläche (oder Tab und Pfeiltasten). Noch einmal tippen zeigt wieder die Markierung." }));
  }
}

/* =========================================================== Wahrheitstabelle */
function wahrheitstabelle(box, d) {
  const vars = d.variablen.map(String), kopf = d._kopf, zeilen = d._zeilen;
  const nullEins = d.darstellung === "01";
  const zeichen = (b) => (nullEins ? (b ? "1" : "0") : (b ? "w" : "f"));
  const markiert = new Set(d._markiert || []);
  const schrittweise = d.schrittweise !== false && kopf.length > 0;
  const zellen = kopf.map(() => []);
  const kopfZellen = [];
  const thead = h("tr", null,
    vars.map(v => h("th", { scope: "col", html: texHtml(v) })),
    kopf.map((k, j) => { const th = h("th", { scope: "col", class: (j === 0 ? "trenner " : "") + (markiert.has(j) ? "ergebnis-spalte" : ""), html: texHtml(k) }); kopfZellen.push(th); return th; }));
  const tbody = h("tbody", null, zeilen.map((z, zi) => h("tr", { style: { animationDelay: `${reduziert() ? 0 : zi * 0.04}s` } },
    z.werte.map(b => h("td", null, h("span", { class: "wb " + (b ? "wahr" : "falsch"), text: zeichen(b) }))),
    z.ergebnisse.map((b, j) => {
      const td = h("td", { class: (j === 0 ? "trenner " : "") + (markiert.has(j) ? "markiert" : "") }, h("span", { class: "wb " + (b ? "wahr" : "falsch"), text: zeichen(b) }));
      zellen[j].push(td);
      return td;
    }))));
  const tabelle = h("table", { class: "wt wt-diskret" }, h("thead", null, thead), tbody);
  const hinweise = h("div", { class: "wt-hinweise", "aria-live": "polite" });
  const text = h("div", { class: "vk-text" });
  box.append(h("div", { class: "vis-scroll dk-scroll wt-rahmen" }, tabelle), text, hinweise);

  function hinweiseZeigen(sichtbar) {
    const teile = [];
    kopf.forEach((k, j) => {
      if (j >= sichtbar) return;
      if (d._art[j] === "tautologie") teile.push(`<span class="chip gruen">Tautologie</span> ${texHtml(k)} ist in jeder Zeile ${zeichen(true)}.`);
      if (d._art[j] === "kontradiktion") teile.push(`<span class="chip rot">Widerspruch</span> ${texHtml(k)} ist in jeder Zeile ${zeichen(false)}.`);
    });
    for (const [i, j] of d._gleich || []) {
      if (j < sichtbar) teile.push(`<span class="chip primary">äquivalent</span> ${texHtml(`${kopf[i]} \\;\\Leftrightarrow\\; ${kopf[j]}`)}: gleiche Spalten.`);
    }
    hinweise.replaceChildren(...teile.map(t => h("p", { html: t })));
  }
  function zeigen(i) {
    zellen.forEach((spalte, j) => {
      const an = j < i;
      spalte.forEach(td => td.classList.toggle("verdeckt", !an));
      kopfZellen[j].classList.toggle("verdeckt-kopf", !an);
    });
    if (i === 0) text.innerHTML = inline(`Links stehen alle ${zeilen.length} Kombinationen von ${nullEins ? "1 und 0" : "w (wahr) und f (falsch)"}. Überlege die nächste Spalte selbst, dann decke sie auf.`);
    else text.innerHTML = `Spalte ${texHtml(kopf[i - 1])}: ${inline(spaltenText(i - 1))}`;
    hinweiseZeigen(i);
  }
  function spaltenText(j) {
    const anz = zeilen.filter(z => z.ergebnisse[j]).length;
    return `in ${anz} von ${zeilen.length} Zeilen ${zeichen(true)}.`;
  }
  if (schrittweise) {
    const st = schrittSteuerung(kopf.length, zeigen, { weiterText: "Nächste Spalte ▶" });
    box.append(st.el);
    st.setzen(0);
  } else {
    zeigen(kopf.length);
    text.remove();
  }
}

/* =========================================================== Relation / Abbildung */
const EIGENSCHAFT = {
  abbildung: { name: "Abbildung", regel: "Jedes Element links hat **genau einen** Pfeil." },
  injektiv: { name: "injektiv", regel: "Kein Element rechts wird **mehr als einmal** getroffen." },
  surjektiv: { name: "surjektiv", regel: "Jedes Element rechts wird **mindestens einmal** getroffen." },
  bijektiv: { name: "bijektiv", regel: "injektiv **und** surjektiv: Jedes Element rechts wird **genau einmal** getroffen." },
};

function relationGraph(box, d) {
  const L = d._links, R = d._rechts, P = d._pfeile, id = neueId("rel");
  const zeilen = Math.max(L.length, R.length);
  const W = 370, dy = 46, oben = 48, H = oben + zeilen * dy + 20;
  const xl = 92, xr = 278;
  const y = (i, anz) => oben + 10 + (zeilen - anz) * dy / 2 + i * dy + dy / 2;
  const s = svg("svg", { class: "rel-svg", viewBox: `0 0 ${W} ${H}`, role: "img",
    "aria-label": `Pfeildiagramm von ${d._namen[0]} nach ${d._namen[1]} mit ${P.length} Pfeilen` });
  s.append(svg("defs", null, pfeilMarker(`${id}p`), pfeilMarker(`${id}pr`, "pfeilspitze rel-spitze-fehler")));
  for (const [x, name] of [[xl, d._namen[0]], [xr, d._namen[1]]]) {
    s.append(svg("rect", { class: "rel-menge", x: x - 56, y: oben, width: 112, height: zeilen * dy + 20, rx: 42 }));
    s.append(svg("text", { class: "rel-name", x, y: oben - 14, "text-anchor": "middle" }, name));
  }
  const punkte = { links: [], rechts: [] };
  const elemente = (liste, seite, x, dotX, anker) => liste.forEach((e, i) => {
    const yy = y(i, liste.length);
    const ring = svg("circle", { class: "rel-ring", cx: dotX, cy: yy, r: 11 });
    s.append(ring, svg("circle", { class: "rel-punkt", cx: dotX, cy: yy, r: 5 }),
      svg("text", { class: "rel-el", x, y: yy + 5, "text-anchor": anker }, e.text));
    punkte[seite].push({ y: yy, ring });
  });
  elemente(L, "links", xl - 10, xl + 30, "middle");
  elemente(R, "rechts", xr + 10, xr - 30, "middle");
  const pfeile = P.map(([a, b]) => {
    const y1 = punkte.links[a].y, y2 = punkte.rechts[b].y;
    const x1 = xl + 36, x2 = xr - 38, len = Math.hypot(x2 - x1, y2 - y1);
    const l = svg("line", { class: "rel-pfeil", x1, y1, x2: x2 - (x2 - x1) / len * 2, y2: y2 - (y2 - y1) / len * 2, "marker-end": `url(#${id}p)` });
    s.append(l);
    return l;
  });
  box.append(h("div", { class: "rel-buehne" }, s));

  const symbol = (v) => (v === true ? "✓" : v === false ? "✗" : "–");
  const wert = { abbildung: d._abbildung, injektiv: d._injektiv, surjektiv: d._surjektiv, bijektiv: d._bijektiv };
  let aufgedeckt = !d.aufdecken, gewaehlt = null;
  const knoepfe = {};
  const leiste = h("div", { class: "rel-eigenschaften", role: "group", "aria-label": "Eigenschaften" });
  const erklaerung = h("div", { class: "vk-text rel-erklaerung", "aria-live": "polite" });
  for (const e of d._zeige) {
    const b = h("button", { type: "button", class: "btn btn-sm rel-chip", "aria-pressed": "false", onclick: () => waehlen(e) });
    knoepfe[e] = b;
    leiste.append(b);
  }
  function beschriften() {
    for (const [e, b] of Object.entries(knoepfe)) {
      const v = wert[e];
      b.textContent = `${EIGENSCHAFT[e].name} ${aufgedeckt ? symbol(v) : "?"}`;
      b.classList.toggle("ja", aufgedeckt && v === true);
      b.classList.toggle("nein", aufgedeckt && v === false);
    }
  }
  function waehlen(e) {
    gewaehlt = e;
    Object.entries(knoepfe).forEach(([k, b]) => b.setAttribute("aria-pressed", String(k === e)));
    pfeile.forEach(p => { p.classList.remove("fehler"); p.setAttribute("marker-end", `url(#${id}p)`); });
    [...punkte.links, ...punkte.rechts].forEach(p => p.ring.classList.remove("fehler"));
    const betroffen = (e === "bijektiv" ? ["injektiv", "surjektiv"] : [e]);
    const verst = d._verstoesse.filter(v => betroffen.includes(v.eigenschaft));
    let html = `<b>${EIGENSCHAFT[e].name}:</b> ${inline(EIGENSCHAFT[e].regel)}`;
    if (!aufgedeckt) { erklaerung.innerHTML = html + " " + inline("Prüfe selbst, dann tippe auf **Auflösen**."); return; }
    if (e !== "abbildung" && !d._abbildung) {
      html += "<br>" + inline("Das ist **keine Abbildung**. Injektiv, surjektiv und bijektiv fragt man nur bei Abbildungen.");
    } else if (!verst.length) {
      html += "<br>✓ " + inline("Erfüllt.");
    } else {
      html += "<br>✗ " + verst.map(v => inline(v.text)).join(" ");
      for (const v of verst) {
        punkte[v.seite][v.element].ring.classList.add("fehler");
        v.pfeile.forEach(i => { pfeile[i].classList.add("fehler"); pfeile[i].setAttribute("marker-end", `url(#${id}pr)`); });
      }
    }
    erklaerung.innerHTML = html;
  }
  box.append(leiste, erklaerung);
  if (d.aufdecken) {
    const b = knopf("Auflösen", () => { aufgedeckt = true; b.remove(); beschriften(); waehlen(gewaehlt); }, { class: "btn btn-sm btn-primary" });
    leiste.append(b);
  }
  beschriften();
  const erster = d._zeige.find(e => wert[e] === false) || d._zeige[0];
  waehlen(d.aufdecken ? d._zeige[0] : erster);
}

/* =========================================================== Pascalsches Dreieck */
function binomTex(i, k, Z) {
  if (k > 0 && k < i) {
    const a = Z[i - 1][k - 1], b = Z[i - 1][k];
    return `\\binom{${i}}{${k}} = \\binom{${i - 1}}{${k - 1}} + \\binom{${i - 1}}{${k}} = ${a} + ${b} = ${a + b}`;
  }
  return `\\binom{${i}}{${k}} = 1`;
}

function pascal(box, d) {
  const Z = d._zeilen, n = Z.length;
  const cw = 50, ch = 40, W = n * cw + 90, H = n * ch + 16;
  const pos = (i, k) => ({ x: W / 2 + (k - i / 2) * cw, y: 8 + i * ch + ch / 2 });
  const s = svg("svg", { class: "pascal-svg", viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": `Pascalsches Dreieck mit ${n} Zeilen` });
  s.style.minWidth = n > 9 ? `${Math.round(W * 0.62)}px` : "";
  s.style.maxWidth = `${W * 1.1}px`;
  const linien = svg("g");
  s.append(linien);
  const zellen = Z.map((zeile, i) => {
    s.append(svg("text", { class: "pascal-zeile", x: 6, y: pos(i, 0).y + 4 }, `n=${i}`));
    return zeile.map((w, k) => {
      const p = pos(i, k);
      const g = svg("g", { class: "pascal-zelle", "data-i": i, "data-k": k },
        svg("rect", { x: p.x - (cw - 6) / 2, y: p.y - (ch - 8) / 2, width: cw - 6, height: ch - 8, rx: 9 }),
        svg("text", { x: p.x, y: p.y + 5, "text-anchor": "middle", style: String(w).length > 3 ? "font-size:12.5px" : "" }, String(w)));
      s.append(g);
      return g;
    });
  });
  (d._markiert || []).forEach(m => zellen[m.n][m.k].classList.add("markiert"));
  const info = h("div", { class: "pascal-info", "aria-live": "polite" });
  let sel = null;
  function waehlen(i, k) {
    zellen.flat().forEach(z => z.classList.remove("aktiv", "eltern"));
    linien.replaceChildren();
    if (i === null) { info.innerHTML = inline("Jede Zahl ist die Summe der beiden Zahlen schräg darüber. Am Rand steht immer $1$."); sel = null; return; }
    sel = { i, k };
    zellen[i][k].classList.add("aktiv");
    if (k > 0 && k < i) {
      for (const kk of [k - 1, k]) {
        zellen[i - 1][kk].classList.add("eltern");
        const a = pos(i - 1, kk), b = pos(i, k);
        linien.append(svg("line", { class: "pascal-linie", x1: a.x, y1: a.y, x2: b.x, y2: b.y }));
      }
    }
    const m = (d._markiert || []).find(x => x.n === i && x.k === k);
    info.innerHTML = texHtml(m ? m.tex : binomTex(i, k, Z), true) +
      (k === 0 || k === i ? `<p>${inline("Randzahl: Darüber steht nur eine Zahl, darum ist sie $1$.")}</p>` : "");
  }
  box.append(h("div", { class: "vis-scroll dk-scroll" }, h("div", { class: "pascal-buehne" }, s)), info);
  const m0 = (d._markiert || [])[0];
  if (m0) waehlen(m0.n, m0.k); else waehlen(null);
  if (d.interaktiv !== false) {
    s.tabIndex = 0;
    s.classList.add("klickbar");
    s.addEventListener("click", (e) => {
      const z = e.target.closest(".pascal-zelle");
      if (z) waehlen(+z.dataset.i, +z.dataset.k);
    });
    s.addEventListener("keydown", (e) => {
      let { i, k } = sel || { i: Math.min(2, n - 1), k: Math.min(1, n - 1) };
      if (!sel) { /* erster Tastendruck: Startzelle */ }
      else if (e.key === "ArrowLeft") k--;
      else if (e.key === "ArrowRight") k++;
      else if (e.key === "ArrowUp") i--;
      else if (e.key === "ArrowDown") i++;
      else if (e.key === "Escape") { waehlen(null); return; }
      else return;
      e.preventDefault(); e.stopPropagation();
      i = Math.max(0, Math.min(n - 1, i)); k = Math.max(0, Math.min(i, k));
      waehlen(i, k);
    });
  }
}

/* =========================================================== Euklidischer Algorithmus */
function euklid(box, d) {
  const S = d._schritte, rueck = d._rueckwaerts || [], g = d._ggt;
  const a0 = Number(d.a), b0 = Number(d.b);
  const zeilen = S.map(([a, b, q, r], i) => h("tr", null,
    h("td", { class: "eu-nr", text: String(i + 1) }),
    h("td", { html: texHtml(`${a} = ${q} \\cdot \\htmlClass{eu-b}{${b}} + \\htmlClass{eu-r}{${r}}`) }),
    h("td", { class: r === 0 ? "eu-null" : "", html: texHtml(String(r)) })));
  const tabelle = h("table", { class: "md-tabelle eu-tabelle" },
    h("thead", null, h("tr", null, h("th", { text: "Zeile" }), h("th", { text: "Division mit Rest" }), h("th", { text: "Rest" }))),
    h("tbody", null, zeilen));
  const ggtZeile = h("div", { class: "eu-ggt dk-scroll", html: texHtml(`\\operatorname{ggT}(${a0}, ${b0}) = ${g}`, true) });
  const rueckEls = rueck.map(z => h("div", { class: "eu-rueck-zeile" }, h("div", { html: texHtml(z.tex, true) })));
  const rueckBox = rueck.length ? h("div", { class: "eu-rueck" }, h("div", { class: "eu-rueck-titel", text: "Rückwärts einsetzen (erweiterter Euklid)" }), rueckEls) : null;
  const text = h("div", { class: "vk-text", "aria-live": "polite" });
  box.append(h("div", { class: "dk-scroll" }, h("div", { class: "md-tabelle-wrap" }, tabelle)), ggtZeile, rueckBox, text);
  const anzahl = S.length + 1 + rueck.length;
  function zeigen(i) {
    zeilen.forEach((z, j) => { z.hidden = j >= i; z.classList.toggle("neu", j === i - 1); });
    ggtZeile.hidden = i <= S.length;
    if (rueckBox) rueckBox.hidden = i <= S.length + 1;
    rueckEls.forEach((z, j) => { z.hidden = j >= i - S.length - 1; z.classList.toggle("neu", j === i - S.length - 2); });
    if (i === 0) text.innerHTML = inline(`Gesucht ist $\\operatorname{ggT}(${a0}, ${b0})$. Teile immer die größere Zahl mit Rest. Dann rückt alles eine Stelle weiter: Der Teiler wird zur neuen Zahl, der Rest zum neuen Teiler.`);
    else if (i <= S.length) {
      const [a, b, q, r] = S[i - 1];
      text.innerHTML = r === 0
        ? inline(`$${b}$ passt genau $${q}$-mal in $${a}$, Rest $0$. Fertig: Der letzte Rest ungleich $0$ ist der ggT.`)
        : inline(`$${b}$ passt $${q}$-mal in $${a}$, es bleibt der Rest $${r}$. Weiter mit $${b}$ und $${r}$.`);
    } else if (i === S.length + 1) text.innerHTML = inline(`Der ggT ist $${g}$.` + (rueck.length ? " Jetzt rückwärts: Wir schreiben ihn als Kombination von $" + a0 + "$ und $" + b0 + "$." : ""));
    else text.innerHTML = inline(rueck[i - S.length - 2].text);
  }
  const st = schrittSteuerung(anzahl, zeigen);
  box.append(st.el);
  st.setzen(0);
}

/* =========================================================== Modulo-Uhr */
function moduloRechnen(n, a, w, art) {
  const mod = (x) => ((x % n) + n) % n;
  const pmod = `\\pmod{${n}}`;
  if (art === "plus") {
    const roh = a + w;
    return { erg: mod(roh), spruenge: [[mod(a), mod(roh), w]], tex: `${a} ${w >= 0 ? "+" : "-"} ${Math.abs(w)} = ${roh} \\equiv ${mod(roh)} ${pmod}`, roh };
  }
  if (art === "mal") {
    const spruenge = [];
    let p = 0;
    for (let i = 0; i < w; i++) { spruenge.push([p, mod(p + a), a]); p = mod(p + a); }
    return { erg: mod(a * w), spruenge, tex: `${a} \\cdot ${w} = ${a * w} \\equiv ${mod(a * w)} ${pmod}`, roh: a * w };
  }
  if (art === "potenz") {
    let x = mod(a);
    const spruenge = [], potenzen = [{ exp: 1, wert: x, tex: `${a}^{1} \\equiv ${x} ${pmod}` }];
    for (let e = 2; e <= w; e++) {
      const neu = mod(x * a);
      spruenge.push([x, neu, e]);
      potenzen.push({ exp: e, wert: neu, tex: `${a}^{${e}} \\equiv ${x} \\cdot ${a} = ${x * a} \\equiv ${neu} ${pmod}` });
      x = neu;
    }
    return { erg: x, spruenge, potenzen, tex: `${a}^{${w}} \\equiv ${x} ${pmod}`, roh: null };
  }
  return { erg: mod(a), spruenge: [], tex: `${a} \\equiv ${mod(a)} ${pmod}`, roh: a };
}

function moduloUhr(box, d) {
  const art = d._art, id = neueId("mod");
  const st = { n: d._n, a: d._start, w: d._wert };
  const W = 360, H = 360, c = 180, R = 128;
  const buehne = h("div", { class: "mod-buehne" });
  const formel = h("div", { class: "mod-formel", "aria-live": "polite" });
  const liste = h("div", { class: "mod-liste" });
  box.append(buehne, formel, liste);
  const winkel = (k, n) => -Math.PI / 2 + 2 * Math.PI * k / n;
  const punkt = (k, n, rad = R) => [c + rad * Math.cos(winkel(k, n)), c + rad * Math.sin(winkel(k, n))];

  function malen(animiert) {
    const { n, a, w } = st;
    const python = n === d._n && a === d._start && w === d._wert;
    const r = moduloRechnen(n, a, w, art);
    const s = svg("svg", { class: "mod-svg", viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": `Uhr mit ${n} Positionen; Ergebnis ${r.erg}` });
    s.append(svg("defs", null, pfeilMarker(`${id}p`, "pfeilspitze mod-spitze")));
    s.append(svg("circle", { class: "mod-kreis", cx: c, cy: c, r: R }));
    const gross = n > 24 ? 11 : n > 16 ? 13 : 15;
    for (let k = 0; k < n; k++) {
      const [x, y] = punkt(k, n), [tx, ty] = punkt(k, n, R + 20);
      const klasse = k === r.erg ? "mod-pos ergebnis" : (art === "plus" && k === ((a % n) + n) % n) ? "mod-pos start" : "mod-pos";
      s.append(svg("circle", { class: klasse, cx: x, cy: y, r: k === r.erg ? 9 : 5 }));
      s.append(svg("text", { class: "mod-zahl" + (k === r.erg ? " ergebnis" : ""), x: tx, y: ty + gross / 3, "text-anchor": "middle", style: `font-size:${gross}px` }, String(k)));
    }
    const pfade = [];
    if (art === "plus" && r.spruenge.length) {
      const [von, , weite] = r.spruenge[0];
      const schritte = Math.max(1, Math.abs(weite) * 12);
      let pfad = "";
      for (let i = 0; i <= schritte; i++) {
        const t = i / schritte, k = von + weite * t;
        const rad = R - 18 - 12 * Math.abs(weite * t) / n;
        const [x, y] = punkt(k, n, rad);
        pfad += (i ? "L" : "M") + x.toFixed(1) + "," + y.toFixed(1);
      }
      pfade.push(svg("path", { class: "mod-sprung", d: pfad, "marker-end": `url(#${id}p)` }));
      const [lx, ly] = punkt(von + weite / 2, n, R - 46 - 12 * Math.abs(weite / 2) / n);
      s.append(svg("text", { class: "mod-sprung-lbl", x: lx, y: ly + 5, "text-anchor": "middle" }, `${weite >= 0 ? "+" : "−"}${Math.abs(weite)}`));
    } else {
      r.spruenge.forEach(([von, bis], i) => {
        const [x1, y1] = punkt(von, n, R - 10), [x2, y2] = punkt(bis, n, R - 10);
        const qx = c + ((x1 + x2) / 2 - c) * 0.35, qy = c + ((y1 + y2) / 2 - c) * 0.35;
        pfade.push(svg("path", { class: "mod-sprung", d: von === bis ? `M${x1},${y1} a10,10 0 1,0 1,0` : `M${x1.toFixed(1)},${y1.toFixed(1)} Q${qx.toFixed(1)},${qy.toFixed(1)} ${x2.toFixed(1)},${y2.toFixed(1)}`, "marker-end": `url(#${id}p)` }));
        if (r.spruenge.length <= 12) {
          const mx = (x1 + x2) / 4 + qx / 2, my = (y1 + y2) / 4 + qy / 2;
          s.append(svg("text", { class: "mod-sprung-nr", x: mx, y: my + 4, "text-anchor": "middle" }, String(i + 1)));
        }
      });
    }
    pfade.forEach((p, i) => {
      s.append(p);
      if (animiert && !reduziert()) {
        const len = 1600;
        p.style.strokeDasharray = len; p.style.strokeDashoffset = len;
        p.style.animation = `modZeichnen .7s ${i * 0.55}s forwards`;
      }
    });
    buehne.replaceChildren(s);
    const tex = python ? d._tex : r.tex;
    const rechnung = python ? d._rechnung : (r.roh !== null ? `${r.roh} = ${Math.floor(r.roh / n)} \\cdot ${n} + ${((r.roh % n) + n) % n}` : null);
    formel.innerHTML = texHtml(tex, true) + (rechnung ? `<div class="mod-rechnung">${inline("Division mit Rest: $" + rechnung + "$")}</div>` : "");
    const pot = python ? d._potenzen : r.potenzen;
    liste.replaceChildren(...(pot && pot.length > 1 ? pot.map(p => h("div", { html: texHtml(p.tex) })) : []));
    liste.hidden = !(pot && pot.length > 1);
  }
  malen(true);
  const steuer = h("div", { class: "vis-steuer" }, knopf("↻ Noch einmal", () => malen(true)));
  box.append(steuer);
  if (d.interaktiv) {
    const reihe = h("div", { class: "regler-reihe" });
    const rn = regler({ name: "n", tex: "n", von: 2, bis: 24, schritt: 1, wert: st.n, oninput: (v) => { st.n = v; malen(false); } });
    const ra = regler({ name: art === "potenz" ? "Basis" : "Start", tex: art === "potenz" ? "\\text{Basis } a" : art === "mal" ? "\\text{Sprungweite } a" : "\\text{Start } a",
      von: 0, bis: Math.max(23, st.a), schritt: 1, wert: st.a, oninput: (v) => { st.a = v; malen(false); } });
    reihe.append(rn.el, ra.el);
    if (art !== "rest") {
      const info = { plus: ["plus", "\\text{plus } b", 0, Math.max(30, st.w)], mal: ["mal", "\\text{Anzahl Sprünge } b", 0, Math.max(12, st.w)], potenz: ["Exponent", "\\text{Exponent } k", 1, Math.max(12, st.w)] }[art];
      reihe.append(regler({ name: info[0], tex: info[1], von: info[2], bis: info[3], schritt: 1, wert: st.w, oninput: (v) => { st.w = v; malen(false); } }).el);
    }
    box.append(reihe);
  }
  if (!document.getElementById("mod-keyframes")) document.head.append(h("style", { id: "mod-keyframes", text: "@keyframes modZeichnen { to { stroke-dashoffset: 0; } }" }));
}

/* =========================================================== Induktion als Dominokette */
function induktionDomino(box, d) {
  const N = d._anzahl, n0 = d._anfang;
  const abstand = 50, W = 30 + N * abstand + 40, H = 210, bw = 22, bh = 92, boden = 160;
  const xStein = (i) => 30 + i * abstand;
  const kippWinkel = Math.asin(Math.min(1, (abstand - bw) / bh)) * 180 / Math.PI;
  const s = svg("svg", { class: "domino-svg", viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": `Dominokette mit ${N} Steinen, beginnend bei n = ${n0}` });
  s.append(svg("line", { class: "domino-boden", x1: 10, y1: boden, x2: W - 10, y2: boden }));
  const steine = [], labels = [];
  for (let i = 0; i < N; i++) {
    const x = xStein(i);
    const g = svg("g", { class: "domino" },
      svg("rect", { x, y: boden - bh, width: bw, height: bh, rx: 3 }),
      svg("circle", { cx: x + bw / 2, cy: boden - bh * 0.72, r: 2.6 }), svg("circle", { cx: x + bw / 2, cy: boden - bh * 0.28, r: 2.6 }),
      svg("line", { x1: x + 3, y1: boden - bh / 2, x2: x + bw - 3, y2: boden - bh / 2 }));
    s.append(g);
    steine.push(g);
    const t = svg("text", { class: "domino-nr", x: x + bw / 2, y: boden + 22, "text-anchor": "middle" }, String(n0 + i));
    s.append(t);
    labels.push(t);
  }
  s.append(svg("text", { class: "domino-nr", x: xStein(N) + 6, y: boden - 30 }, "…"));
  const marke = svg("g", { class: "domino-marke" });
  s.append(marke);
  const text = h("div", { class: "vk-text", "aria-live": "polite" });
  const aussage = d.aussage ? h("div", { class: "domino-aussage", html: `<b>Aussage</b> ${texHtml("A(n)")}: ${inline(d.aussage)}` }) : null;
  box.append(aussage, h("div", { class: "domino-buehne" }, s), text);

  let timer = [];
  function zuruecksetzen() {
    timer.forEach(clearTimeout); timer = [];
    steine.forEach(g => { g.style.transition = "none"; g.style.transform = ""; g.classList.remove("an", "fokus"); });
    labels.forEach((t, i) => { t.textContent = String(n0 + i); t.classList.remove("fokus"); });
    marke.replaceChildren();
    void s.getBoundingClientRect();
  }
  function kippen(i, verzoegerung) {
    const g = steine[i];
    const los = () => {
      g.style.transition = reduziert() ? "none" : "transform .32s ease-in";
      g.style.transform = `rotate(${kippWinkel}deg)`;
      g.classList.add("an");
    };
    if (reduziert() || !verzoegerung) los(); else timer.push(setTimeout(los, verzoegerung));
  }
  function etikett(x, y, txt, klasse = "") {
    marke.append(svg("text", { class: "domino-lbl " + klasse, x, y, "text-anchor": "middle" }, txt));
  }
  const tAnfang = d.text_anfang || `**Induktionsanfang (IA):** Zeige, dass die Aussage für $n = ${n0}$ stimmt. Der erste Stein fällt.`;
  const tSchritt = d.text_schritt || "**Induktionsschritt (IS):** Nimm an, die Aussage stimmt für ein beliebiges $k$ (Induktionsvoraussetzung). Zeige, dass sie dann auch für $k + 1$ stimmt. Jeder fallende Stein stößt den nächsten um.";
  const aktionen = {
    anfang() {
      zuruecksetzen();
      steine[0].classList.add("fokus");
      kippen(0, 30);
      etikett(xStein(0) + bw / 2, 26, "IA", "ia");
      etikett(xStein(0) + bw / 2, 44, `A(${n0}) gilt`, "klein");
      text.innerHTML = inline(tAnfang);
    },
    schritt() {
      zuruecksetzen();
      const k = Math.min(3, N - 2);
      labels[k].textContent = "k"; labels[k + 1].textContent = "k+1";
      labels[k].classList.add("fokus"); labels[k + 1].classList.add("fokus");
      steine[k].classList.add("fokus"); steine[k + 1].classList.add("fokus");
      kippen(k, 300);
      kippen(k + 1, 300 + 320);
      const xm = (xStein(k) + xStein(k + 1)) / 2 + bw / 2;
      etikett(xm, 26, "IS", "is");
      etikett(xm, 44, "A(k) ⇒ A(k+1)", "klein");
      text.innerHTML = inline(tSchritt);
    },
    alle() {
      zuruecksetzen();
      for (let i = 0; i < N; i++) kippen(i, 60 + i * 260);
      etikett(W / 2, 30, `A(n) gilt für alle n ≥ ${n0}`, "ia");
      text.innerHTML = inline(`**Beides zusammen:** Der erste Stein fällt (IA), und jeder fallende Stein stößt den nächsten um (IS). Also fallen alle Steine: Die Aussage gilt für alle $n \\ge ${n0}$.`);
    },
  };
  box.append(h("div", { class: "vis-steuer" },
    knopf("1. Induktionsanfang", aktionen.anfang), knopf("2. Induktionsschritt", aktionen.schritt),
    knopf("3. Alle fallen", aktionen.alle, { class: "btn btn-sm btn-primary" }),
    knopf("Aufstellen", () => { zuruecksetzen(); text.innerHTML = inline("Alle Steine stehen. Damit **alle** fallen, brauchst du zwei Dinge: Der erste fällt, und jeder Stein reißt den nächsten mit."); })));
  text.innerHTML = inline("Alle Steine stehen. Damit **alle** fallen, brauchst du zwei Dinge: Der erste fällt, und jeder Stein reißt den nächsten mit.");
}

/* =========================================================== Folge mit ε-Schlauch */
function folge(box, d) {
  const NMAX = d._n0_bis || 10000;
  const nVon = d._werte[0][0], nBis = d._werte[d._werte.length - 1][0];
  const g = d._grenzwert, hatG = typeof g === "number";
  // Glieder numerisch bis NMAX (für n0 bei anderen ε); im Bild die Werte aus Python
  let abstaende = null;
  if (hatG && typeof d._epsilon === "number") {
    abstaende = [];
    let a = d._start;
    for (let n = nVon; n <= NMAX; n++) {
      let w;
      if (d._ast) w = auswerten(d._ast, { n });
      else { w = a; a = auswerten(d._ast_rek, { a, n }); }
      if (!Number.isFinite(w)) break;
      abstaende.push(Math.abs(w - g));
    }
  }
  let eps = d._epsilon;
  const n0Von = (e) => {
    if (e === d._epsilon && "_n0" in d) return d._n0;
    let letzt = null;
    for (let i = abstaende.length - 1; i >= 0; i--) if (!(abstaende[i] < e)) { letzt = nVon + i; break; }
    if (abstaende.length < NMAX - nVon + 1) return null;
    if (letzt === null) return nVon;
    return letzt === NMAX ? null : letzt + 1;
  };
  const ys = d._werte.map(w => w[1]);
  if (hatG) ys.push(g + (eps || 0), g - (eps || 0));
  let ymin = Math.min(...ys), ymax = Math.max(...ys);
  const pad = (ymax - ymin || 1) * 0.15;
  ymin -= pad; ymax += pad;
  if (d.y) [ymin, ymax] = d.y.map(Number);
  const legende = h("div", { class: "plot-legende" }, h("span", { html: texHtml(d._tex) }),
    hatG ? h("span", { html: texHtml(`g = ${d._grenzwert_tex}`) }) : null);
  const info = h("div", { class: "plot-info folge-info", "aria-live": "polite" });
  const k = koordinaten({ x: [nVon - 1, nBis + 1], y: [ymin, ymax], xName: "n", yName: "aₙ", label: "Folgenglieder als Punkte" }, (k) => {
    const n0 = eps ? n0Von(eps) : null;
    if (hatG && eps) {
      k.flaeche([[k.xmin, g - eps], [k.xmax, g - eps], [k.xmax, g + eps], [k.xmin, g + eps]], "folge-schlauch");
      k.linie(k.xmin, g + eps, k.xmax, g + eps, "folge-schlauch-rand");
      k.linie(k.xmin, g - eps, k.xmax, g - eps, "folge-schlauch-rand");
    }
    if (hatG) k.linie(k.xmin, g, k.xmax, g, "folge-grenze");
    if (d._schranken) {
      k.linie(k.xmin, d._schranken.max, k.xmax, d._schranken.max, "folge-schranke");
      k.linie(k.xmin, d._schranken.min, k.xmax, d._schranken.min, "folge-schranke");
    }
    if (n0 !== null && n0 !== undefined && n0 <= nBis) {
      k.linie(n0, k.ymin, n0, k.ymax, "folge-n0");
      k.etikett(n0, k.ymax - (k.ymax - k.ymin) * 0.06, texHtml(`n_0 = ${n0}`), "folge-n0-lbl");
    }
    for (const [n, w] of d._werte) {
      let kl = "punkt folge-pkt";
      if (hatG && eps) kl += Math.abs(w - g) < eps ? (n0 !== null && n >= n0 ? " drin" : " drin-frueh") : " draussen";
      k.punkt(n, w, { klasse: kl, r: 4.5 });
    }
    info.innerHTML = infoText(n0);
  });
  function infoText(n0) {
    const teile = [];
    if (hatG && eps) {
      const epsTex = eps === d._epsilon ? d._epsilon_tex : zahlText(eps, 4).replace(",", "{,}").replace("−", "-");
      const bed = `|a_n - ${d._grenzwert_tex}| < ${epsTex}`;
      if (n0 === null) teile.push(inline(`Für $\\varepsilon = ${epsTex}$ liegen bis $n = ${NMAX}$ **nicht** ab einer Stelle alle Glieder im Schlauch.`));
      else teile.push(inline(`Ab $n_0 = ${n0}$ liegen alle Glieder im $\\varepsilon$-Schlauch: $${bed}$.`) + (n0 > nBis ? " " + inline("(Das ist rechts außerhalb des Bildes.)") : ""));
    }
    if (d._monotonie) teile.push(`<span class="chip">im Bild ${d._monotonie}</span>`);
    if (d._schranken) teile.push(`<span class="chip">im Bild zwischen ${texHtml(d._schranken.min_tex)} und ${texHtml(d._schranken.max_tex)}</span>`);
    return teile.join(" ");
  }
  box.append(h("div", { class: "vis-scroll" }, k.el), legende, info);
  if (hatG && eps && d.interaktiv !== false && abstaende) {
    const e0 = d._epsilon;
    const r = regler({ name: "epsilon", tex: "\\varepsilon", von: e0 / 20, bis: e0 * 3, schritt: e0 / 20, wert: e0,
      format: (v) => zahlText(v, 4), oninput: (v) => { eps = Math.abs(v - e0) < e0 / 1000 ? e0 : v; k.neu(); } });
    box.append(h("div", { class: "regler-reihe" }, r.el));
  }
  if (hatG && eps) box.append(h("p", { class: "antwort-hinweis", text: `Grün: im Schlauch ab n₀. Orange: außerhalb. Nachgeprüft bis n = ${NMAX.toLocaleString("de-DE")}.` }));
}

export const BAUER = {
  venn, wahrheitstabelle, relation_graph: relationGraph, pascal, euklid, modulo_uhr: moduloUhr,
  induktion_domino: induktionDomino, folge,
};
