// Grund-Visuals: zahlenstrahl, bruch, rechnung (Waage), funktionsgraph, parabel.
import { h, svg, inline, reduziert } from "./util.js";
import { texHtml } from "./formel.js";
import { koordinaten, auswerten, regler, zahlText, nullstellenNumerisch } from "./plot.js";
import { knopf } from "./visuals.js";

/* =========================================================== Zahlenstrahl */
function zahlenstrahl(box, d) {
  const W = 680, H = 130, pad = 34, yA = 80;
  const von = d._von, bis = d._bis, schritt = Number(d.schritt) > 0 ? Number(d.schritt) : 1;
  const x = (v) => pad + (Math.max(von - 1e9, Math.min(bis + 1e9, v)) - von) / (bis - von) * (W - 2 * pad);
  const s = svg("svg", { class: "zs-svg", viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Zahlenstrahl" });
  const etiketten = h("div", { class: "plot-etiketten" });
  const buehne = h("div", { class: "plot-buehne" }, s, etiketten);
  const etikett = (px, py, html, kl = "") => {
    const e = h("div", { class: "plot-etikett " + kl, html });
    e.style.left = (px / W * 100) + "%"; e.style.top = (py / H * 100) + "%";
    etiketten.append(e);
  };
  s.append(svg("line", { class: "achse", x1: pad - 14, y1: yA, x2: W - pad + 16, y2: yA }));
  s.append(svg("path", { class: "achsen-spitze", d: `M${W - pad + 18},${yA} l-10,-6 v12 z` }));
  const anzahl = Math.round((bis - von) / schritt);
  const jedeN = anzahl > 24 ? Math.ceil(anzahl / 12) : 1;
  for (let i = 0; i <= anzahl; i++) {
    const v = von + i * schritt;
    const gross = i % jedeN === 0;
    s.append(svg("line", { class: Math.abs(v) < 1e-9 ? "tick null" : "tick", x1: x(v), y1: yA - (gross ? 7 : 4), x2: x(v), y2: yA + (gross ? 7 : 4) }));
    if (gross) s.append(svg("text", { class: "tick-lbl", x: x(v), y: yA + 24 }, zahlText(v)));
  }
  (d.intervalle || []).forEach((iv, n) => {
    const zahl = (v) => (v === "inf" ? Infinity : v === "-inf" ? -Infinity : v);
    const a = zahl(iv._von), b = zahl(iv._bis), y = yA - 2 - n * 8;
    const xa = Number.isFinite(a) ? x(a) : pad - 12, xb = Number.isFinite(b) ? x(b) : W - pad + 12;
    s.append(svg("line", { class: "intervall", x1: xa, y1: y, x2: xb, y2: y }));
    if (Number.isFinite(a)) s.append(svg("circle", { class: "rand" + (iv.von_zu ? " zu" : ""), cx: xa, cy: y, r: 6.5 }));
    if (Number.isFinite(b)) s.append(svg("circle", { class: "rand" + (iv.bis_zu ? " zu" : ""), cx: xb, cy: y, r: 6.5 }));
    etikett((xa + xb) / 2, y - 18, texHtml(iv.label || iv._tex), "intervall-lbl");
  });
  (d.pfeile || []).forEach((p, i) => {
    const a = x(p._von), b = x(p._bis), m = (a + b) / 2, hoehe = Math.min(46, 16 + Math.abs(b - a) * 0.25);
    const pfad = svg("path", { class: "sprung", d: `M${a},${yA - 6} Q${m},${yA - 6 - hoehe * 1.7} ${b},${yA - 6}`, "marker-end": "url(#zs-spitze)" });
    if (!reduziert()) { pfad.style.strokeDasharray = "400"; pfad.style.strokeDashoffset = "400"; pfad.style.animation = `zsZeichnen .6s ${i * 0.5}s forwards`; }
    s.append(pfad);
    etikett(m, yA - 8 - hoehe * 0.95, texHtml(p.label), "sprung-lbl");
  });
  s.prepend(svg("defs", null, svg("marker", { id: "zs-spitze", viewBox: "0 0 10 10", refX: 8, refY: 5, markerWidth: 7, markerHeight: 7, orient: "auto" }, svg("path", { d: "M0,0 L10,5 L0,10 z", class: "pfeilspitze" }))));
  (d.punkte || []).forEach((p) => {
    s.append(svg("circle", { class: "zs-punkt" + (p.farbe ? " " + p.farbe : ""), cx: x(p._x), cy: yA, r: 7 }));
    const aufStrich = Math.abs((p._x - von) / schritt - Math.round((p._x - von) / schritt)) < 1e-9;
    if (p.label || !aufStrich) etikett(x(p._x), yA - 22, texHtml(p.label || p._tex), "punkt-lbl");
  });
  box.append(h("div", { class: "vis-scroll" }, buehne));
  if (d.interaktiv) {
    const anzeige = h("div", { class: "ausdruck-zeile", "aria-live": "polite" });
    const marke = svg("g", { class: "zs-marke" }, svg("circle", { r: 9 }), svg("line", { x1: 0, y1: -14, x2: 0, y2: 14 }));
    s.append(marke);
    const setzen = (v) => {
      v = Math.max(von, Math.min(bis, Math.round(v / (schritt / 2)) * (schritt / 2)));
      marke.setAttribute("transform", `translate(${x(v)},${yA})`);
      const lage = v < 0 ? "links von 0: negativ" : v > 0 ? "rechts von 0: positiv" : "genau die Null";
      anzeige.innerHTML = `<span>Du zeigst auf</span> <b class="erg">${zahlText(v)}</b> <span class="chip">${lage}</span>`;
    };
    const ausEvent = (e) => { const r = s.getBoundingClientRect(); setzen(von + ((e.clientX - r.left) / r.width * W - pad) / (W - 2 * pad) * (bis - von)); };
    let zieht = false;
    s.addEventListener("pointerdown", (e) => { zieht = true; s.setPointerCapture(e.pointerId); ausEvent(e); });
    s.addEventListener("pointermove", (e) => { if (zieht) ausEvent(e); });
    s.addEventListener("pointerup", () => { zieht = false; });
    s.style.cursor = "pointer";
    s.tabIndex = 0;
    let aktuell = 0;
    s.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight" || e.key === "ArrowLeft") { e.preventDefault(); e.stopPropagation(); aktuell += (e.key === "ArrowRight" ? 1 : -1) * schritt / 2; setzen(aktuell); }
    });
    setzen(0);
    box.append(anzeige, h("p", { class: "antwort-hinweis", text: "Tippe oder klicke auf den Strahl (oder nutze die Pfeiltasten). Rechts werden die Zahlen größer." }));
  }
  if (!document.getElementById("zs-keyframes")) document.head.append(h("style", { id: "zs-keyframes", text: "@keyframes zsZeichnen { to { stroke-dashoffset: 0; } }" }));
}

/* =========================================================== Bruch */
const BRUCH_FARBEN = ["var(--plot-1)", "var(--plot-2)", "var(--plot-3)"];

function balken(g, x0, y0, breite, hoehe, z, n, teilung = 1, farbe = BRUCH_FARBEN[0]) {
  // ein Ganzes (Balken) mit n Teilen, z davon gefärbt; jede Teilfläche zusätzlich in "teilung" Streifen
  const teile = n * teilung, w = breite / teile;
  for (let i = 0; i < teile; i++) {
    const voll = i < z * teilung;
    g.append(svg("rect", { class: "bruch-teil" + (voll ? " voll" : ""), x: x0 + i * w, y: y0, width: w, height: hoehe, style: voll ? `fill:${farbe}` : "" }));
  }
  for (let i = 1; i < n; i++) g.append(svg("line", { class: "bruch-grenze", x1: x0 + i * breite / n, y1: y0, x2: x0 + i * breite / n, y2: y0 + hoehe }));
  g.append(svg("rect", { class: "bruch-rahmen", x: x0, y: y0, width: breite, height: hoehe }));
}

function kuchen(g, cx, cy, r, z, n, teilung = 1, farbe = BRUCH_FARBEN[0]) {
  const teile = n * teilung;
  for (let i = 0; i < teile; i++) {
    const a1 = -Math.PI / 2 + i * 2 * Math.PI / teile, a2 = a1 + 2 * Math.PI / teile;
    const voll = i < z * teilung;
    const p = teile === 1
      ? svg("circle", { cx, cy, r })
      : svg("path", { d: `M${cx},${cy} L${cx + r * Math.cos(a1)},${cy + r * Math.sin(a1)} A${r},${r} 0 ${a2 - a1 > Math.PI ? 1 : 0} 1 ${cx + r * Math.cos(a2)},${cy + r * Math.sin(a2)} Z` });
    p.setAttribute("class", "bruch-teil" + (voll ? " voll" : "") + (teilung > 1 && i % teilung ? " fein" : ""));
    if (voll) p.style.fill = farbe;
    g.append(p);
  }
  g.append(svg("circle", { class: "bruch-rahmen", cx, cy, r }));
}

const NENNER_NAME = { 2: "Halbe", 3: "Drittel", 4: "Viertel", 5: "Fünftel", 6: "Sechstel", 7: "Siebtel", 8: "Achtel", 9: "Neuntel", 10: "Zehntel", 12: "Zwölftel" };
const nennerName = (n) => NENNER_NAME[n] || `${n}tel`;

function bruch(box, d) {
  if (d._plus) { bruchPlus(box, d); return; }
  const modell = d.modell === "balken" ? "balken" : "kuchen";
  let z = Number(d.zaehler), n = Number(d.nenner), teilung = 1;
  const buehne = h("div", { class: "bruch-buehne" });
  const label = h("div", { class: "bruch-label", "aria-live": "polite" });
  box.append(buehne, label);

  function malen() {
    const ganze = Math.max(1, Math.ceil(z / n));
    const W = modell === "kuchen" ? Math.max(180, ganze * 160) : 520, H = modell === "kuchen" ? 170 : Math.max(80, ganze * 70);
    const s = svg("svg", { class: "bruch-svg", viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": `Bruch ${z}/${n}` });
    s.style.maxWidth = W + "px";
    const g = svg("g");
    s.append(g);
    for (let k = 0; k < ganze; k++) {
      const zk = Math.max(0, Math.min(n, z - k * n));
      if (modell === "kuchen") kuchen(g, 80 + k * 160, 85, 70, zk, n, teilung);
      else balken(g, 10, 10 + k * 70, W - 20, 50, zk, n, teilung);
    }
    buehne.replaceChildren(s);
    const tex = teilung > 1
      ? `\\frac{${z}}{${n}} = \\frac{${z} \\cdot ${teilung}}{${n} \\cdot ${teilung}} = \\frac{${z * teilung}}{${n * teilung}}`
      : `\\frac{${z}}{${n}}`;
    label.innerHTML = texHtml(tex, true);
  }
  malen();

  const steuer = h("div", { class: "vis-steuer" });
  if (d.erweitern) {
    const k = Number(d.erweitern);
    const b = knopf(`Mit ${k} erweitern`, () => { teilung = teilung === 1 ? k : 1; b.textContent = teilung === 1 ? `Mit ${k} erweitern` : "Zurück zum Ausgangsbruch"; malen(); });
    steuer.append(b, h("span", { class: "vis-unterschrift", style: { margin: 0 }, text: "Jedes Stück wird kleiner geschnitten. Die gefärbte Fläche bleibt gleich groß." }));
  }
  if (d.kuerzen) {
    const [kz, kn] = d._gekuerzt;
    const ausgang = [z, n];
    const b = knopf("Kürzen", () => {
      if (z === ausgang[0]) { z = kz; n = kn; b.textContent = "Zurück zum Ausgangsbruch"; }
      else { [z, n] = ausgang; b.textContent = "Kürzen"; }
      malen();
      if (z !== ausgang[0]) label.innerHTML = texHtml(`\\frac{${ausgang[0]}}{${ausgang[1]}} = \\frac{${kz}}{${kn}}`, true);
    });
    steuer.append(b);
  }
  if (d.interaktiv) {
    const rz = regler({ name: "Zähler", tex: "\\text{Zähler}", von: 0, bis: 24, schritt: 1, wert: z, oninput: (v) => { z = v; teilung = 1; malen(); } });
    const rn = regler({ name: "Nenner", tex: "\\text{Nenner}", von: 1, bis: 12, schritt: 1, wert: n, oninput: (v) => { n = v; teilung = 1; malen(); } });
    box.append(h("div", { class: "regler-reihe" }, rz.el, rn.el));
  }
  if (steuer.children.length) box.append(steuer);
}

function bruchPlus(box, d) {
  const p = d._plus, [a, b] = d.plus;
  const schritte = [
    { text: a[1] === b[1] ? `Beide Brüche haben den Nenner ${a[1]}: Die Stücke sind schon gleich groß.` : `Zwei Brüche mit verschiedenen Nennern: ${nennerName(a[1])} und ${nennerName(b[1])}. So kann man sie nicht zusammenzählen.`, tex: `\\frac{${a[0]}}{${a[1]}} + \\frac{${b[0]}}{${b[1]}}`, teil: [1, 1] },
    { text: `Beide in ${nennerName(p.hauptnenner)} schneiden (Hauptnenner ${p.hauptnenner}). Die Flächen bleiben gleich.`, tex: `\\frac{${p.a[0]}}{${p.hauptnenner}} + \\frac{${p.b[0]}}{${p.hauptnenner}}`, teil: [p.hauptnenner / a[1], p.hauptnenner / b[1]] },
    { text: "Jetzt sind alle Stücke gleich groß. Die Stücke werden einfach gezählt.", tex: `\\frac{${p.a[0]} + ${p.b[0]}}{${p.hauptnenner}} = \\frac{${p.summe[0]}}{${p.summe[1]}}`, teil: null },
  ];
  if (a[1] === b[1]) schritte.splice(1, 1);
  if (p.gekuerzt[1] !== p.summe[1]) schritte.push({ text: "Zum Schluss kürzen.", tex: `\\frac{${p.summe[0]}}{${p.summe[1]}} = \\frac{${p.gekuerzt[0]}}{${p.gekuerzt[1]}}`, teil: null });
  const buehne = h("div", { class: "bruch-buehne" });
  const text = h("div", { class: "vk-text" });
  const formel = h("div", { class: "bruch-label" });
  let i = 0;
  const zaehler = h("span", { class: "zaehler" });
  const zur = knopf("◀ Zurück", () => zeigen(i - 1)), vor = knopf("Weiter ▶", () => zeigen(i + 1));
  function zeigen(k) {
    i = Math.max(0, Math.min(schritte.length - 1, k));
    const s = schritte[i], W = 520;
    const g = svg("svg", { class: "bruch-svg", viewBox: `0 0 ${W} 140`, role: "img", "aria-label": "Brüche addieren" });
    g.style.maxWidth = W + "px";
    if (s.teil) {
      balken(g, 10, 10, W - 20, 50, a[0], a[1], s.teil[0], BRUCH_FARBEN[0]);
      balken(g, 10, 80, W - 20, 50, b[0], b[1], s.teil[1], BRUCH_FARBEN[1]);
    } else {
      const hn = p.hauptnenner, w = (W - 20) / hn;
      for (let t = 0; t < hn; t++) {
        const farbe = t < p.a[0] ? BRUCH_FARBEN[0] : t < p.a[0] + p.b[0] ? BRUCH_FARBEN[1] : null;
        g.append(svg("rect", { class: "bruch-teil" + (farbe ? " voll" : ""), x: 10 + t * w, y: 45, width: w, height: 50, style: farbe ? `fill:${farbe}` : "" }));
      }
      for (let t = 1; t < hn; t++) g.append(svg("line", { class: "bruch-grenze", x1: 10 + t * w, y1: 45, x2: 10 + t * w, y2: 95 }));
      g.append(svg("rect", { class: "bruch-rahmen", x: 10, y: 45, width: W - 20, height: 50 }));
    }
    buehne.replaceChildren(g);
    text.innerHTML = inline(s.text);
    formel.innerHTML = texHtml(s.tex, true);
    zaehler.textContent = `Schritt ${i + 1} / ${schritte.length}`;
    zur.disabled = i === 0; vor.disabled = i === schritte.length - 1;
  }
  box.append(buehne, formel, text, h("div", { class: "vis-steuer" }, zur, zaehler, vor));
  zeigen(0);
}

/* =========================================================== Waage (rechnung) */
function waageSvg(z) {
  const W = 560, H = 240;
  const s = svg("svg", { class: "waage-svg", viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Waage im Gleichgewicht" });
  s.append(svg("path", { class: "waage-fuss", d: `M${W / 2 - 40},${H - 10} L${W / 2},${H - 70} L${W / 2 + 40},${H - 10} Z` }));
  s.append(svg("line", { class: "waage-balken", x1: 60, y1: H - 70, x2: W - 60, y2: H - 70 }));
  for (const [cx, bild] of [[140, z.bild_links], [W - 140, z.bild_rechts]]) {
    s.append(svg("line", { class: "waage-seil", x1: cx, y1: H - 70, x2: cx - 70, y2: H - 100 }));
    s.append(svg("line", { class: "waage-seil", x1: cx, y1: H - 70, x2: cx + 70, y2: H - 100 }));
    s.append(svg("path", { class: "waage-schale", d: `M${cx - 95},${H - 100} Q${cx},${H - 82} ${cx + 95},${H - 100} Z` }));
    if (bild) {
      const dinge = [...Array(bild.x).fill("x"), ...Array(bild.eins).fill("1")];
      const proReihe = 8;
      dinge.forEach((art, i) => {
        const r = Math.floor(i / proReihe), c = i % proReihe;
        const anzahl = Math.min(proReihe, dinge.length - r * proReihe);
        const x = cx - (anzahl - 1) * 11 + c * 22, y = H - 112 - r * 24;
        if (art === "x") {
          s.append(svg("rect", { class: "waage-x", x: x - 10, y: y - 10, width: 20, height: 20, rx: 4 }));
          s.append(svg("text", { class: "waage-x-text", x, y: y + 5 }, "x"));
        } else s.append(svg("circle", { class: "waage-eins", cx: x, cy: y, r: 9 }));
      });
    }
  }
  return s;
}

function waage(box, d) {
  const zust = d._zustaende || [];
  const buehne = h("div", { class: "waage-buehne" });
  const gleichung = h("div", { class: "waage-gleichung", "aria-live": "polite" });
  const text = h("div", { class: "vk-text" });
  let i = 0;
  const zaehler = h("span", { class: "zaehler" });
  const zur = knopf("◀ Zurück", () => zeigen(i - 1)), vor = knopf("Nächster Schritt ▶", () => zeigen(i + 1));
  function zeigen(k) {
    i = Math.max(0, Math.min(zust.length - 1, k));
    const z = zust[i];
    const svgEl = waageSvg(z);
    const ohneBild = !z.bild_links || !z.bild_rechts;
    buehne.replaceChildren(svgEl);
    if (ohneBild) {
      buehne.append(h("div", { class: "waage-term links", html: texHtml(z.links) }), h("div", { class: "waage-term rechts", html: texHtml(z.rechts) }));
    }
    buehne.classList.toggle("neu", i > 0 && !reduziert());
    gleichung.innerHTML = texHtml(`${z.links} = ${z.rechts}`, true);
    text.innerHTML = i === 0 ? inline(z.text || "Die Waage ist im Gleichgewicht: links wiegt genauso viel wie rechts.")
      : `<b>${texHtml(`\\big| ${z.op}`)}</b> ${inline(z.text || "")}`;
    zaehler.textContent = `Schritt ${i + 1} / ${zust.length}`;
    zur.disabled = i === 0; vor.disabled = i === zust.length - 1;
  }
  box.append(buehne, gleichung, text, h("div", { class: "vis-steuer" }, zur, zaehler, vor),
    h("p", { class: "vis-unterschrift", html: "Ein Kästchen ist ein unbekanntes <b>x</b>, ein Kreis wiegt <b>1</b>. Was du links machst, musst du auch rechts machen. Dann bleibt die Waage im Gleichgewicht." }));
  zeigen(0);
}

/* =========================================================== Funktionsgraph */
const PLOT_FARBEN = ["var(--plot-1)", "var(--plot-2)", "var(--plot-3)", "var(--plot-4)"];

function funktionsgraph(box, d) {
  const params = Object.fromEntries((d.parameter || []).map(p => [p.name, p._wert]));
  const start = { ...params };
  const unveraendert = () => Object.keys(params).every(k => params[k] === start[k]);
  const fns = (d.funktionen || []).map((f, i) => ({ ...f, farbe: f.farbe ? `var(--plot-${f.farbe})` : PLOT_FARBEN[i % 4], fn: (x) => auswerten(f._ast, { ...params, x }) }));
  const legende = h("div", { class: "plot-legende" }, fns.map(f => h("span", { class: "leg" }, h("i", { style: { background: f.farbe } }), h("span", { html: texHtml((f.label || "f(x)") + " = " + f._tex) }))));
  const info = h("div", { class: "plot-info", "aria-live": "polite" });
  const k = koordinaten({ x: (d.x || [-5, 5]).map(Number), y: (d.y || [-5, 5]).map(Number), gleicheAchsen: d.gleiche_achsen }, (k) => {
    const infos = [];
    fns.forEach((f) => {
      k.kurve(f.fn, "kurve", f.farbe);
      if (d.nullstellen) {
        const exakt = unveraendert() && f._nullstellen;
        const xs = exakt ? f._nullstellen.map(n => n.x) : nullstellenNumerisch(f.fn, k.xmin, k.xmax);
        xs.forEach((x, j) => k.punkt(x, 0, { klasse: "punkt null", label: exakt ? texHtml(f._nullstellen[j].tex) : zahlText(x, 2) }));
        if (!xs.length) infos.push("keine Nullstelle im Bild");
      }
      if (d.scheitel) {
        const sch = unveraendert() && f._scheitel ? f._scheitel : scheitelNumerisch(f.fn, k.xmin, k.xmax);
        if (sch) k.punkt(sch.x, sch.y, { klasse: "punkt scheitel", label: sch.tex ? texHtml("S" + sch.tex) : `S(${zahlText(sch.x, 2)} | ${zahlText(sch.y, 2)})`, labelKlasse: "scheitel-lbl" });
      }
    });
    (d.punkte || []).forEach(p => k.punkt(p._x, p._y, { label: texHtml(p.label) }));
    info.textContent = infos.join(" · ");
  });
  box.append(h("div", { class: "vis-scroll" }, k.el), legende, info);
  const tabelleSlot = h("div");
  const tabelle = () => {
    if (!d.wertetabelle || !fns.length) return;
    const f = fns[0];
    const exakt = unveraendert() && f._tabelle;
    const t = h("table", { class: "wertetabelle" },
      h("tr", null, h("th", { html: texHtml("x") }), ...(exakt ? f._tabelle : d.wertetabelle).map(z => h("td", { html: exakt ? texHtml(z.x) : zahlText(Number(z)) }))),
      h("tr", null, h("th", { html: texHtml(f.label || "f(x)") }), ...(exakt ? f._tabelle.map(z => h("td", { html: texHtml(z.y) })) : d.wertetabelle.map(x => h("td", { text: zahlText(f.fn(Number(eval_zahl(x))), 2) })))));
    tabelleSlot.replaceChildren(h("div", { class: "md-tabelle-wrap" }, t));
  };
  if ((d.parameter || []).length) {
    const reihe = h("div", { class: "regler-reihe" });
    for (const p of d.parameter) {
      reihe.append(regler({ name: p.name, tex: p.tex || p.name, von: p._von, bis: p._bis, schritt: Number(p.schritt), wert: p._wert,
        oninput: (v) => { params[p.name] = v; k.neu(); tabelle(); } }).el);
    }
    box.append(reihe);
  }
  box.append(tabelleSlot);
  tabelle();
}

function eval_zahl(x) {
  if (typeof x === "number") return x;
  const m = String(x).match(/^(-?\d+(?:[.,]\d+)?)(?:\/(\d+))?$/);
  return m ? parseFloat(m[1].replace(",", ".")) / (m[2] ? parseFloat(m[2]) : 1) : NaN;
}

function scheitelNumerisch(f, a, b) {
  const n = 600;
  let best = null;
  for (let i = 1; i < n; i++) {
    const x0 = a + (b - a) * (i - 1) / n, x1 = a + (b - a) * i / n, x2 = a + (b - a) * (i + 1) / n;
    const y0 = f(x0), y1 = f(x1), y2 = f(x2);
    if ([y0, y1, y2].every(Number.isFinite) && ((y1 <= y0 && y1 <= y2) || (y1 >= y0 && y1 >= y2)) && !(y0 === y1 && y1 === y2)) {
      best = { x: x1, y: y1 };
      break;
    }
  }
  return best;
}

/* =========================================================== Parabel */
function parabel(box, d) {
  const w = { a: Number(d.a ?? 1), b: Number(d.b ?? 0), c: Number(d.c ?? 0) };
  const start = { ...w };
  const scheitelform = d.form === "scheitel";
  const f = (x) => w.a * x * x + w.b * x + w.c;
  const formel = h("div", { class: "plot-legende" });
  const info = h("div", { class: "plot-info", "aria-live": "polite" });
  const k = koordinaten({ x: (d.x || [-6, 6]).map(Number), y: (d.y || [-4, 8]).map(Number) }, (k) => {
    k.kurve(f, "kurve", "var(--plot-1)");
    const xs = -w.b / (2 * w.a), ys = f(xs);
    const exakt = w.a === start.a && w.b === start.b && w.c === start.c;
    k.linie(xs, k.ymin, xs, k.ymax, "symmetrieachse");
    k.punkt(xs, ys, { klasse: "punkt scheitel", label: exakt ? texHtml("S" + d._scheitel.tex) : `S(${zahlText(xs, 2)} | ${zahlText(ys, 2)})`, labelKlasse: "scheitel-lbl" });
    const nst = exakt ? d._nullstellen.map(n => n.x) : nullstellenNumerisch(f, k.xmin, k.xmax);
    nst.forEach((x, j) => k.punkt(x, 0, { klasse: "punkt null", label: exakt ? texHtml(d._nullstellen[j].tex) : zahlText(x, 2) }));
    const zahl = (v) => zahlText(v, 2).replace("−", "-");
    const faktor = (v) => (Math.abs(v - 1) < 1e-9 ? "" : Math.abs(v + 1) < 1e-9 ? "-" : zahl(v));
    const glied = (v, rest) => (Math.abs(v) < 1e-9 ? "" : ` ${v < 0 ? "-" : "+"} ${Math.abs(Math.abs(v) - 1) < 1e-9 && rest ? "" : zahl(Math.abs(v))}${rest}`);
    const klammer = Math.abs(xs) < 1e-9 ? "x" : `(x ${xs < 0 ? "+" : "-"} ${zahl(Math.abs(xs))})`;
    const tex = scheitelform
      ? `f(x) = ${faktor(w.a)}${klammer}^2${glied(ys, "")}`
      : `f(x) = ${faktor(w.a)}x^2${glied(w.b, "x")}${glied(w.c, "")}`;
    formel.innerHTML = texHtml(tex.replace(/\{,\}/g, ","));
    info.textContent = w.a > 0 ? "a > 0: Die Parabel ist nach oben geöffnet (lächelt)." : "a < 0: Die Parabel ist nach unten geöffnet.";
    if (Math.abs(w.a) < 1e-9) info.textContent = "a = 0: Das ist keine Parabel mehr, sondern eine Gerade!";
  });
  box.append(h("div", { class: "vis-scroll" }, k.el), formel, info);
  if (d.regler !== false) {
    const reihe = h("div", { class: "regler-reihe" });
    for (const name of ["a", "b", "c"]) {
      reihe.append(regler({ name, von: name === "a" ? -3 : -6, bis: name === "a" ? 3 : 6, schritt: name === "a" ? 0.25 : 0.5, wert: w[name],
        oninput: (v) => { w[name] = Math.abs(v) < 1e-9 && name === "a" ? 0.0001 : v; k.neu(); } }).el);
    }
    box.append(reihe);
  }
}

export const BAUER = { zahlenstrahl, bruch, rechnung: waage, funktionsgraph, parabel };
