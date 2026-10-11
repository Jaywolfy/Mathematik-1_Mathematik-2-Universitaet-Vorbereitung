// Alle Visualisierungen aus dem Vertrag (Abschnitt 4) als HTML/SVG-Komponenten.
import { h, svg, esc, inline, reduziert } from "./util.js";
import { highlight } from "./highlight.js";
import { api } from "./api.js";
import { varKiste, wertElement, pyRepr, jsonZuWert, typKlasse, legende, literalTyp, ALIAS_FARBEN } from "./werte.js";

export const VISUAL_TYPEN = ["variablen", "liste", "string", "dict", "referenz", "ablauf", "entscheidung",
  "schleife", "zahlenstrahl", "wahrheitstabelle", "stapel", "baum", "funktion", "typen"];

const TITEL = {
  variablen: "📦 Variablen", liste: "🗂️ Liste", string: "🔤 String", dict: "📒 Wörterbuch (dict)",
  referenz: "🏷️ Namen & Objekte", ablauf: "➡️ Ablauf", entscheidung: "🔀 Entscheidung (if/elif/else)",
  schleife: "🔁 Schleife", zahlenstrahl: "📏 range() auf dem Zahlenstrahl", wahrheitstabelle: "✅ Wahrheitstabelle",
  stapel: "🥞 Aufrufstapel", baum: "🌳 Aufrufbaum", funktion: "⚙️ Funktion als Maschine", typen: "🧺 Datentypen",
};

export function visual(art, daten, fehler = null) {
  const box = h("figure", { class: `visual vis-${art}`, style: { margin: 0 } });
  if (fehler) {
    box.append(h("div", { class: "vis-fehler", text: `Visualisierung „${art}“ konnte nicht gelesen werden: ${fehler}` }));
    return box;
  }
  const bauer = BAUER[art];
  const d = daten || {};
  box.append(h("figcaption", { class: "vis-titel", text: d.titel || TITEL[art] || art }));
  if (!bauer) {
    box.append(h("div", { class: "vis-fehler", text: `Unbekannter Visualisierungstyp „${art}“.` }));
    return box;
  }
  try { bauer(box, d); } catch (e) {
    console.error(e);
    box.append(h("div", { class: "vis-fehler", text: `Fehler beim Zeichnen: ${e.message}` }));
  }
  const unterschrift = d.unterschrift || d.beschriftung || (art !== "string" && typeof d.text === "string" ? d.text : null);
  if (unterschrift) box.append(h("p", { class: "vis-unterschrift", html: inline(unterschrift) }));
  return box;
}

const BAUER = {
  variablen: visVariablen, liste: (b, d) => visFaecher(b, d, false), string: (b, d) => visFaecher(b, d, true),
  dict: visDict, referenz: visReferenz, ablauf: visAblauf, entscheidung: visEntscheidung, schleife: visSchleife,
  zahlenstrahl: visZahlenstrahl, wahrheitstabelle: visWahrheitstabelle, stapel: visStapel, baum: visBaum,
  funktion: visFunktion, typen: visTypen,
};

function knopf(text, onclick, extra = {}) {
  return h("button", { class: "btn btn-sm", type: "button", text, onclick, ...extra });
}

/* ------------------------------------------------------------------ variablen */
// markup.py liefert "anzeige" (Python-Darstellung, z. B. 2.0 statt 2); Fallback: wert
function varAnzeige(v) {
  if (v && typeof v.anzeige === "string") return v.anzeige;
  const w = v ? v.wert : undefined;
  return typeof w === "string" ? w : pyRepr(w);
}

function visVariablen(box, d) {
  const zustaende = Array.isArray(d.schritte) && d.schritte.length ? d.schritte : [d.vars || []];
  const texte = d.texte || [];
  const buehne = h("div", { class: "vis-reihe vk-gross", "aria-live": "polite" });
  const text = h("div", { class: "vk-text" });
  box.append(buehne);
  let i = 0, timer = null;
  const zaehler = h("span", { class: "zaehler" });
  const zurueck = knopf("◀ Zurück", () => zeigen(i - 1));
  const vor = knopf("Weiter ▶", () => zeigen(i + 1));
  const spiel = knopf("▶ Abspielen", () => abspielen());

  function zeigen(n, animieren = true) {
    n = Math.max(0, Math.min(zustaende.length - 1, n));
    const vorher = new Map((zustaende[i] || []).map(v => [v.name, v]));
    const vorwaerts = n === i + 1;
    i = n;
    buehne.replaceChildren();
    for (const v of zustaende[i] || []) {
      const anzeige = varAnzeige(v);
      const typ = v.typ === "None" ? "NoneType" : (v.typ || literalTyp(anzeige));
      let klasse = "";
      if (animieren && vorwaerts) {
        const alt = vorher.get(v.name);
        if (!alt) klasse = "neu"; else if (varAnzeige(alt) !== anzeige || alt.typ !== v.typ) klasse = "geaendert";
      }
      buehne.append(varKiste(v.name, h("span", { class: "w-prim", text: anzeige }), typ, { klasse }));
    }
    if (!(zustaende[i] || []).length) buehne.append(h("span", { class: "tr-leer", text: "(noch keine Variablen)" }));
    text.innerHTML = inline(texte[i] || "");
    text.hidden = !texte[i];
    zaehler.textContent = `Schritt ${i + 1} / ${zustaende.length}`;
    zurueck.disabled = i === 0; vor.disabled = i === zustaende.length - 1;
  }
  function abspielen() {
    if (timer) { clearInterval(timer); timer = null; spiel.textContent = "▶ Abspielen"; return; }
    if (i >= zustaende.length - 1) zeigen(0, false);
    spiel.textContent = "⏸ Pause";
    timer = setInterval(() => {
      if (i >= zustaende.length - 1 || !box.isConnected) { clearInterval(timer); timer = null; spiel.textContent = "▶ Abspielen"; return; }
      zeigen(i + 1);
    }, 1500);
  }
  box.append(text);
  if (zustaende.length > 1) box.append(h("div", { class: "vis-steuer" }, zurueck, zaehler, vor, spiel));
  box.append(h("div", { style: { marginTop: "12px" } }, legende()));
  zeigen(0, false);
}

/* --------------------------------------------------------- liste & string */
function parseSlice(s) {
  if (s === null || s === undefined || s === "") return null;
  const teile = String(s).replace(/^\[|\]$/g, "").split(":");
  const z = (t) => (t === undefined || t.trim() === "" ? null : parseInt(t, 10));
  return { start: z(teile[0]), stop: z(teile[1]), step: teile.length > 2 ? z(teile[2]) : null };
}

export function sliceIndizes(len, start, stop, step) {
  step = step ?? 1;
  if (step === 0) return [];
  const [lower, upper] = step > 0 ? [0, len] : [-1, len - 1];
  const norm = (v, std) => {
    if (v === null || v === undefined) return std;
    if (v < 0) return Math.max(v + len, lower);
    return Math.min(v, upper);
  };
  const s = norm(start, step > 0 ? lower : upper);
  const e = norm(stop, step > 0 ? upper : lower);
  const r = [];
  if (step > 0) for (let i = s; i < e; i += step) r.push(i);
  else for (let i = s; i > e; i += step) r.push(i);
  return r;
}

function sliceText(sl) {
  const f = (v) => (v === null || v === undefined ? "" : String(v));
  return `${f(sl.start)}:${f(sl.stop)}${sl.step !== null && sl.step !== undefined ? ":" + sl.step : ""}`;
}

function visFaecher(box, d, istString) {
  const werte = istString ? [...String(d.text ?? "")] : (Array.isArray(d.werte) ? d.werte : []);
  // Python-Darstellung aus markup.py ("werte_anzeige"), sonst eigene Umwandlung
  const anz = (i) => (!istString && Array.isArray(d.werte_anzeige) && typeof d.werte_anzeige[i] === "string")
    ? d.werte_anzeige[i] : pyRepr(werte[i]);
  const name = d.name || (istString ? "text" : "lst");
  const len = werte.length;
  const markiert = new Set((d.markiert || []).map(m => (m < 0 ? m + len : m)));
  const negativ = d.negativ ?? !!d.interaktiv;
  let sl = parseSlice(d.slice);
  if (d.interaktiv && !sl) sl = { start: null, stop: null, step: null };

  const reihe = h("div", { class: "faecher-reihe" });
  const zeile = h("div", { class: "listen-zeile" }, h("span", { class: "listen-name", text: name + " =" }), h("div", { class: "faecher" }, reihe));
  box.append(h("div", { class: "vis-scroll" }, zeile));
  const faecher = werte.map((w, i) => {
    const anzeige = istString ? (w === " " ? "␣" : w) : anz(i);
    const f = h("div", { class: "fach" + (markiert.has(i) ? " markiert" : "") + (istString ? "" : "") },
      h("span", { class: "slice-nr" }),
      h("span", { class: "idx", text: i, title: `Index ${i}` }),
      h("div", { class: "zelle", title: istString ? `Zeichen ${JSON.stringify(w)}` : anzeige }, h("span", { text: anzeige, class: istString && w === " " ? "zeichen-leer" : "" })),
      negativ ? h("span", { class: "idx neg", text: i - len, title: `Index ${i - len}` }) : null);
    reihe.append(f);
    return f;
  });
  if (istString) zeile.querySelector(".faecher").classList.add("string-faecher");
  if (!len) reihe.append(h("span", { class: "w-leer", text: istString ? "'' (leerer String)" : "[] (leere Liste)" }));

  const ausdruck = h("div", { class: "ausdruck-zeile", "aria-live": "polite" });
  function aktualisieren() {
    faecher.forEach(f => { f.classList.remove("im-slice"); f.querySelector(".slice-nr").textContent = ""; });
    if (!sl) { ausdruck.hidden = true; return; }
    const idx = sliceIndizes(len, sl.start, sl.stop, sl.step);
    idx.forEach((i, k) => { faecher[i].classList.add("im-slice"); faecher[i].querySelector(".slice-nr").textContent = idx.length > 1 && (sl.step ?? 1) !== 1 ? `${k + 1}.` : ""; });
    const erg = idx.map(i => werte[i]);
    const ergText = istString ? pyRepr(erg.join("")) : "[" + idx.map(anz).join(", ") + "]";
    ausdruck.hidden = false;
    ausdruck.innerHTML = `<span>${highlight(`${name}[${sliceText(sl)}]`)}</span><span class="gleich">→</span><span class="erg">${esc(ergText)}</span>`
      + (idx.length === 0 ? `<span class="chip gelb">leer – kein Element passt</span>` : "");
  }
  box.append(ausdruck);

  if (d.interaktiv) {
    const regler = h("div", { class: "slice-regler" });
    const mk = (feld, label, min, max, std) => {
      const out = h("output");
      const r = h("input", { type: "range", min, max, step: 1, value: sl[feld] ?? std, "aria-label": label });
      const leer = h("input", { type: "checkbox", checked: sl[feld] === null ? true : undefined, "aria-label": `${label} weglassen` });
      const sync = () => {
        let v = parseInt(r.value, 10);
        if (feld === "step" && v === 0) { v = 1; r.value = 1; }
        sl[feld] = leer.checked ? null : v;
        r.disabled = leer.checked;
        out.textContent = leer.checked ? "leer" : v;
        aktualisieren();
      };
      r.addEventListener("input", sync); leer.addEventListener("change", sync);
      sync();
      return h("div", { class: "regler" },
        h("label", null, h("span", { text: label }), out),
        r, h("label", { class: "leer-schalter" }, leer, "weglassen (Standardwert)"));
    };
    regler.append(mk("start", "start", -len, len, 0), mk("stop", "stop", -len, len, len), mk("step", "step", -3, 3, 1));
    box.append(regler);
    box.append(h("p", { class: "vis-unterschrift", html: "Schiebe die Regler: <code>start</code> ist dabei, <code>stop</code> ist <b>nicht</b> mehr dabei, <code>step</code> ist die Schrittweite (negativ = rückwärts)." }));
  } else {
    aktualisieren();
    if (!sl && markiert.size) {
      const m = [...markiert][0];
      box.append(h("p", { class: "vis-unterschrift", html: `<code>${esc(name)}[${m}]</code> → <code>${esc(istString ? pyRepr(werte[m]) : anz(m))}</code>` }));
    }
  }
  aktualisieren();
}

/* -------------------------------------------------------------------- dict */
function visDict(box, d) {
  const paare = Array.isArray(d.paare) ? d.paare : Object.entries(d.daten || {});
  const markiert = new Set((d.markiert || []).map(String));
  const name = d.name || "d";
  const anz = (i, k) => (Array.isArray(d.paare_anzeige) && Array.isArray(d.paare_anzeige[i]) && typeof d.paare_anzeige[i][k] === "string")
    ? d.paare_anzeige[i][k] : pyRepr(paare[i][k]);
  const liste = h("div", { class: "dict-vis" },
    h("div", { class: "dict-kopf" }, h("span", { text: "Schlüssel" }), h("span"), h("span", { text: "Wert" })));
  paare.forEach(([k, v], i) => {
    const z = h("div", { class: "dict-zeile" + (markiert.has(String(k)) ? " markiert" : ""), style: { animation: `hochkommen .4s ${i * 0.07}s both` } },
      h("div", { class: "dict-key", text: anz(i, 0) }), h("div", { class: "dict-pfeil", text: "→" }), h("div", { class: "dict-val", text: anz(i, 1) }));
    liste.append(z);
  });
  if (!paare.length) liste.append(h("div", { class: "w-leer", text: "{} – leeres Wörterbuch" }));
  box.append(h("div", { class: "listen-name", style: { marginBottom: "10px" }, text: `${name} = { … }` }), liste);
  const mi = paare.findIndex(([k]) => markiert.has(String(k)));
  if (mi >= 0) box.append(h("p", { class: "vis-unterschrift", html: `Nachschlagen per Schlüssel: <code>${esc(name)}[${esc(anz(mi, 0))}]</code> → <code>${esc(anz(mi, 1))}</code>` }));
}

/* ---------------------------------------------------------------- referenz */
function visReferenz(box, d) {
  const namen = Object.entries(d.namen || {});
  const objekte = d.objekte || [];
  const grid = h("div", { class: "ref-vis" });
  const spalteN = h("div", { class: "ref-namen" });
  const spalteO = h("div", { class: "ref-objekte" });
  const pfeile = svg("svg", { class: "ref-pfeile", "aria-hidden": "true" });
  grid.append(spalteN, spalteO, pfeile);
  const nameEls = namen.map(([n, idx]) => { const e = h("div", { class: "ref-name", text: n, "data-ziel": idx }); spalteN.append(e); return e; });
  const objEls = objekte.map((o, i) => {
    const w = (Array.isArray(d.objekte_werte) && d.objekte_werte[i]) ? d.objekte_werte[i] : jsonZuWert(o);
    const e = h("div", { class: "ref-objekt" }, h("span", { class: "ref-id", text: `Objekt #${i + 1}` }),
      h("div", { class: `var-kiste ${typKlasse(w.typ)}`, style: { borderColor: ALIAS_FARBEN[i % ALIAS_FARBEN.length] } }, h("div", { class: "vk-wert" }, wertElement(w))));
    spalteO.append(e); return e;
  });
  box.append(h("div", { class: "vis-scroll" }, grid));

  const zeichnen = () => {
    if (!grid.isConnected) return;
    const g = grid.getBoundingClientRect();
    pfeile.setAttribute("width", g.width); pfeile.setAttribute("height", g.height);
    pfeile.replaceChildren();
    const defs = svg("defs");
    ALIAS_FARBEN.forEach((f, i) => defs.append(svg("marker", { id: `refspitze${i}-${box.dataset.uid}`, viewBox: "0 0 10 10", refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: "auto-start-reverse" },
      svg("path", { d: "M0,0 L10,5 L0,10 z", fill: f }))));
    pfeile.append(defs);
    nameEls.forEach(ne => {
      const idx = parseInt(ne.dataset.ziel, 10);
      const oe = objEls[idx]; if (!oe) return;
      const a = ne.getBoundingClientRect(), b = oe.querySelector(".var-kiste").getBoundingClientRect();
      const x1 = a.right - g.left, y1 = a.top + a.height / 2 - g.top;
      const x2 = b.left - g.left - 2, y2 = b.top + b.height / 2 - g.top;
      const mx = (x1 + x2) / 2;
      const fi = idx % ALIAS_FARBEN.length;
      pfeile.append(svg("path", { d: `M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}`, stroke: ALIAS_FARBEN[fi], "marker-end": `url(#refspitze${fi}-${box.dataset.uid})` }));
    });
  };
  box.dataset.uid = Math.random().toString(36).slice(2, 8);
  new ResizeObserver(() => requestAnimationFrame(zeichnen)).observe(grid);
  requestAnimationFrame(() => requestAnimationFrame(zeichnen));

  // Erklärung: wer teilt sich ein Objekt, wo gibt es gleiche Inhalte?
  const gruppen = new Map();
  namen.forEach(([n, i]) => { if (!gruppen.has(i)) gruppen.set(i, []); gruppen.get(i).push(n); });
  const saetze = [];
  for (const [, ns] of gruppen) if (ns.length > 1) saetze.push(`<code>${ns.map(esc).join("</code> und <code>")}</code> zeigen auf <b>dasselbe</b> Objekt (Aliasing): Eine Änderung über den einen Namen sieht man auch über den anderen. <code>${esc(ns[0])} is ${esc(ns[1])}</code> → <code>True</code>`);
  const reprs = objekte.map((o, i) => (Array.isArray(d.objekte_anzeige) && typeof d.objekte_anzeige[i] === "string") ? d.objekte_anzeige[i] : JSON.stringify(o));
  for (let i = 0; i < objekte.length; i++) for (let j = i + 1; j < objekte.length; j++) {
    if (reprs[i] === reprs[j] && gruppen.get(i) && gruppen.get(j)) {
      const a = gruppen.get(i)[0], b = gruppen.get(j)[0];
      saetze.push(`<code>${esc(a)}</code> und <code>${esc(b)}</code> haben den gleichen Inhalt, sind aber <b>verschiedene</b> Objekte (Kopie): <code>${esc(a)} == ${esc(b)}</code> → <code>True</code>, aber <code>${esc(a)} is ${esc(b)}</code> → <code>False</code>`);
    }
  }
  if (saetze.length) box.append(h("div", { class: "ref-legende" }, saetze.map(s => h("p", { html: "• " + s }))));
}

/* ------------------------------------------------------------------ ablauf */
function visAblauf(box, d) {
  const schritte = d.schritte || [];
  const reihe = h("div", { class: "ablauf" });
  schritte.forEach((s, i) => {
    const verz = reduziert() ? 0 : i * 0.18;
    const teil = h("div", { class: "ablauf-schritt" });
    if (i > 0) teil.append(h("div", { class: "ablauf-pfeil", style: { animationDelay: `${verz - 0.05}s` }, "aria-hidden": "true", text: "➜" }));
    teil.append(h("div", { class: "ablauf-karte", style: { animationDelay: `${verz}s` } },
      h("span", { class: "a-icon", text: s.icon || "•" }), h("span", { class: "a-nr", text: `SCHRITT ${i + 1}` }), h("span", { html: inline(s.text || "") })));
    reihe.append(teil);
  });
  box.append(reihe);
}

/* ------------------------------------------------------------ entscheidung */
function visEntscheidung(box, d) {
  const fluss = h("div", { class: "fluss vis-scroll" });
  const zweige = [{ art: "if", bedingung: d.bedingung, text: d.ja }, ...(d.elif || []).map(e => ({ art: "elif", bedingung: e.bedingung, text: e.text ?? e.ja }))];
  let t = 0;
  const delay = () => (reduziert() ? "0s" : `${(t++) * 0.22}s`);
  zweige.forEach((z, i) => {
    if (i > 0) fluss.append(h("div", { class: "fluss-nein", style: { animationDelay: delay() } }, h("span", { text: "Nein" })));
    fluss.append(h("div", { class: "fluss-zeile", style: { animationDelay: delay() } },
      h("div", { class: "fluss-bed" }, h("small", { text: z.art + " – trifft zu?" }), z.bedingung ?? ""),
      h("div", { class: "fluss-ja" }, h("span", { text: "Ja" }), h("span", { class: "linie" })),
      h("div", { class: "fluss-aktion" }, h("small", { text: "dann" }), h("span", { html: inline(z.text ?? "") }))));
  });
  if (d.nein !== undefined && d.nein !== null) {
    fluss.append(h("div", { class: "fluss-nein", style: { animationDelay: delay() } }, h("span", { text: "Nein" })));
    fluss.append(h("div", { class: "fluss-sonst", style: { animationDelay: delay() } }, h("small", { text: "else – sonst" }), h("span", { html: inline(d.nein) })));
  }
  box.append(fluss);
  box.append(h("p", { class: "vis-unterschrift", html: "Python prüft die Bedingungen <b>von oben nach unten</b>. Die <b>erste</b>, die zutrifft, gewinnt – alle weiteren werden übersprungen." }));
}

/* ----------------------------------------------------------------- schleife */
function visSchleife(box, d) {
  const CW = 8.7, ZH = 24;
  const art = d.art || (String(d.bedingung || "").includes(" in ") ? "for" : "while");
  const bed = String(d.bedingung ?? "");
  const bedText = art === "for" ? `for ${bed.replace(/^for\s+/, "").replace(/:$/, "")}` : `${bed}`;
  const koerper = (d.koerper || []).map(String);
  const danach = d.danach ? String(d.danach) : "";
  const hw = Math.max(115, bedText.length * CW / 2 + 52), hh = 40;
  const bodyW = Math.max(190, Math.max(...koerper.map(z => z.length), 6) * CW + 36);
  const bodyH = Math.max(1, koerper.length) * ZH + 22;
  const links = 34;
  const cx = links + 26 + Math.max(hw, bodyW / 2);
  const cy = 30 + hh;
  const by = cy + hh + 56;
  const nx = cx + hw + 64;
  const danachW = danach ? Math.max(140, danach.length * CW + 36) : 0;
  const W = Math.max(danach ? nx + danachW : cx + hw + 40, cx + bodyW / 2 + 130) + 12;
  const H = by + bodyH + 62;
  const s = svg("svg", { class: "schleife-svg", viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": `Flussdiagramm einer ${art}-Schleife` });
  s.style.maxWidth = W + "px";
  const u = Math.random().toString(36).slice(2, 7);
  const defs = svg("defs");
  [["pS", "var(--text-3)"], ["pJ", "var(--success-strong)"], ["pN", "var(--danger-strong)"], ["pZ", "var(--primary)"]].forEach(([id, f]) =>
    defs.append(svg("marker", { id: id + u, viewBox: "0 0 10 10", refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: "auto" }, svg("path", { d: "M0,0 L10,5 L0,10 z", style: `fill:${f}` }))));
  s.append(defs);
  // Start-Pfeil
  s.append(svg("path", { class: "kante", d: `M${cx},4 L${cx},${cy - hh - 2}`, "marker-end": `url(#pS${u})` }));
  // Bedingung (Raute)
  s.append(svg("g", { class: "k-bed" },
    svg("polygon", { points: `${cx},${cy - hh} ${cx + hw},${cy} ${cx},${cy + hh} ${cx - hw},${cy}` }),
    svg("text", { x: cx, y: cy + 5, "text-anchor": "middle" }, bedText)));
  s.append(svg("text", { class: "lbl", x: cx - hw + 10, y: cy - hh + 2, style: "fill:var(--warn)" }, art === "for" ? "noch ein Element?" : "Bedingung wahr?"));
  // Ja nach unten
  s.append(svg("path", { class: "kante ja", d: `M${cx},${cy + hh} L${cx},${by - 2}`, "marker-end": `url(#pJ${u})` }));
  s.append(svg("text", { class: "lbl", x: cx + 8, y: cy + hh + 30, style: "fill:var(--success)" }, "Ja"));
  // Körper
  const g = svg("g", { class: "k-body" }, svg("rect", { x: cx - bodyW / 2, y: by, width: bodyW, height: bodyH, rx: 12 }));
  koerper.forEach((z, i) => g.append(svg("text", { x: cx - bodyW / 2 + 18, y: by + 26 + i * ZH }, z)));
  s.append(g);
  s.append(svg("text", { class: "lbl", x: cx + bodyW / 2 + 10, y: by + 18, style: "fill:var(--primary-text)" }, "Schleifenkörper"));
  s.append(svg("text", { class: "lbl", x: cx + bodyW / 2 + 10, y: by + 34, style: "fill:var(--text-3)" }, "(eingerückt)"));
  // Rücksprung
  const rueck = `M${cx},${by + bodyH} L${cx},${by + bodyH + 30} L${links},${by + bodyH + 30} L${links},${cy} L${cx - hw - 2},${cy}`;
  s.append(svg("path", { class: "kante zurueck", d: rueck, "marker-end": `url(#pZ${u})` }));
  s.append(svg("text", { class: "lbl", x: links + 8, y: by + bodyH + 50, style: "fill:var(--primary-text)" }, "↺ zurück zur Bedingung"));
  // Nein nach rechts
  if (danach) {
    s.append(svg("path", { class: "kante nein", d: `M${cx + hw},${cy} L${nx - 2},${cy}`, "marker-end": `url(#pN${u})` }));
    s.append(svg("text", { class: "lbl", x: cx + hw + 10, y: cy - 8, style: "fill:var(--danger)" }, art === "for" ? "fertig" : "Nein"));
    s.append(svg("g", { class: "k-danach" }, svg("rect", { x: nx, y: cy - 22, width: danachW, height: 44, rx: 12 }),
      svg("text", { x: nx + 16, y: cy + 5 }, danach)));
    s.append(svg("text", { class: "lbl", x: nx + 4, y: cy - 30, style: "fill:var(--text-2)" }, "danach (nicht eingerückt)"));
  }
  if (!reduziert()) {
    const pfad = `M${cx},${cy + hh} L${cx},${by + bodyH + 30} L${links},${by + bodyH + 30} L${links},${cy} L${cx - hw},${cy}`;
    const p = svg("circle", { class: "punkt", r: 6 });
    p.append(svg("animateMotion", { dur: "4s", repeatCount: "indefinite", path: pfad }));
    s.append(p);
  }
  box.append(h("div", { class: "vis-scroll" }, s));
  box.append(h("p", { class: "vis-unterschrift", html: art === "for"
    ? "Für <b>jedes</b> Element wird der eingerückte Körper einmal ausgeführt. Sind alle Elemente dran gewesen, geht es <b>danach</b> weiter."
    : "Solange die Bedingung <code>True</code> ist, läuft der Körper immer wieder. Ist sie <code>False</code>, geht es <b>danach</b> weiter. Ändert der Körper nichts an der Bedingung, entsteht eine Endlosschleife!" }));
}

/* ------------------------------------------------------------ zahlenstrahl */
function rangeWerte(start, stop, step) {
  const r = [];
  if (!step) return r;
  if (step > 0) for (let i = start; i < stop && r.length < 200; i += step) r.push(i);
  else for (let i = start; i > stop && r.length < 200; i += step) r.push(i);
  return r;
}

function visZahlenstrahl(box, d) {
  const z = { start: d.start ?? 0, stop: d.stop ?? 10, step: d.step ?? 1 };
  const buehne = h("div");
  const ausdruck = h("div", { class: "ausdruck-zeile", "aria-live": "polite" });
  box.append(buehne, ausdruck);
  const zeichnen = () => {
    const werte = rangeWerte(z.start, z.stop, z.step);
    const lo = Math.min(z.start, z.stop, 0) - 1, hi = Math.max(z.start, z.stop) + 1;
    const W = 680, pad = 26, yA = 92;
    const x = (v) => pad + (v - lo) * (W - 2 * pad) / Math.max(1, hi - lo);
    const span = hi - lo;
    const tickStep = span <= 24 ? 1 : span <= 60 ? 5 : 10;
    const s = svg("svg", { class: "zs-svg", viewBox: `0 0 ${W} 140`, role: "img", "aria-label": `range(${z.start}, ${z.stop}, ${z.step}) ergibt ${werte.join(", ") || "nichts"}` });
    s.append(svg("line", { class: "achse", x1: pad - 8, y1: yA, x2: W - pad + 8, y2: yA }));
    s.append(svg("path", { d: `M${W - pad + 8},${yA} l-8,-5 v10 z`, style: "fill:var(--text-3)" }));
    for (let v = Math.ceil(lo); v <= hi; v++) {
      if (v % tickStep !== 0) continue;
      s.append(svg("line", { class: "tick", x1: x(v), y1: yA - 5, x2: x(v), y2: yA + 5 }));
      s.append(svg("text", { class: "tick-lbl", x: x(v), y: yA + 22 }, String(v)));
    }
    // Sprünge
    werte.forEach((v, i) => {
      if (i === 0) return;
      const a = x(werte[i - 1]), b = x(v), m = (a + b) / 2, hoehe = Math.min(42, 14 + Math.abs(b - a) * 0.35);
      const p = svg("path", { class: "sprung", d: `M${a},${yA - 8} Q${m},${yA - 8 - hoehe * 1.6} ${b},${yA - 8}` });
      if (!reduziert()) { p.style.strokeDasharray = "200"; p.style.strokeDashoffset = "200"; p.style.animation = `zsZeichnen .5s ${i * 0.12}s forwards`; }
      s.append(p);
      if (werte.length <= 14) s.append(svg("text", { class: "sprung-lbl", x: m, y: yA - 12 - hoehe * 0.8 }, (z.step > 0 ? "+" : "") + z.step));
    });
    werte.forEach((v, i) => {
      const c = svg("circle", { class: "wert-kreis", cx: x(v), cy: yA, r: 7 });
      if (!reduziert()) { c.style.opacity = 0; c.style.animation = `einblenden .3s ${i * 0.12}s forwards`; }
      s.append(c);
    });
    // Stop (exklusiv)
    s.append(svg("circle", { class: "stop-kreis", cx: x(z.stop), cy: yA, r: 7 }));
    s.append(svg("text", { class: "stop-lbl", x: x(z.stop), y: yA + 40 }, `stop = ${z.stop} (nicht dabei)`));
    s.append(svg("text", { class: "start-lbl", x: x(z.start), y: 16 }, `start = ${z.start}`));
    buehne.replaceChildren(s);
    const aufruf = z.step === 1 ? (z.start === 0 ? `range(${z.stop})` : `range(${z.start}, ${z.stop})`) : `range(${z.start}, ${z.stop}, ${z.step})`;
    ausdruck.innerHTML = `<span>${highlight(`list(${aufruf})`)}</span><span class="gleich">→</span><span class="erg">[${werte.join(", ")}]</span>`
      + (werte.length ? `<span class="chip">${werte.length} Zahl${werte.length === 1 ? "" : "en"}</span>` : `<span class="chip gelb">leer – ${z.step > 0 ? "start ist nicht kleiner als stop" : "start ist nicht größer als stop"}</span>`);
  };
  if (!document.getElementById("zs-keyframes")) {
    document.head.append(h("style", { id: "zs-keyframes", text: "@keyframes zsZeichnen { to { stroke-dashoffset: 0; } }" }));
  }
  if (d.interaktiv) {
    const regler = h("div", { class: "slice-regler" });
    const mk = (feld, min, max) => {
      const out = h("output", { text: z[feld] });
      const r = h("input", { type: "range", min, max, value: z[feld], "aria-label": feld });
      r.addEventListener("input", () => {
        let v = parseInt(r.value, 10);
        if (feld === "step" && v === 0) { v = z.step > 0 ? -1 : 1; r.value = v; }
        z[feld] = v; out.textContent = v; zeichnen();
      });
      return h("div", { class: "regler" }, h("label", null, h("span", { text: feld }), out), r);
    };
    regler.append(mk("start", -10, 20), mk("stop", -10, 20), mk("step", -5, 5));
    box.append(regler);
  }
  zeichnen();
}

/* -------------------------------------------------------- wahrheitstabelle */
// Ersatz-Auswertung, falls markup.py keine "zeilen" geliefert hat. Rangfolge wie in Python:
// or < and < not < Vergleich (==, !=) < | < ^ < &
function boolParser(text) {
  const toks = String(text).match(/\(|\)|!=|==|[A-Za-z_][\w]*|\S/g) || [];
  let i = 0;
  const peek = () => toks[i];
  const naechst = () => toks[i++];
  function oder(env) { let v = und(env); while (peek() === "or") { naechst(); const r = und(env); v = v || r; } return v; }
  function und(env) { let v = nicht(env); while (peek() === "and") { naechst(); const r = nicht(env); v = v && r; } return v; }
  function nicht(env) { if (peek() === "not") { naechst(); return !nicht(env); } return vergleich(env); }
  function vergleich(env) {
    let links = bitOder(env), ok = true, kette = false;
    while (peek() === "==" || peek() === "!=") {
      const op = naechst(); const rechts = bitOder(env);
      ok = ok && (op === "==" ? links === rechts : links !== rechts);
      links = rechts; kette = true;
    }
    return kette ? ok : links;
  }
  function bitOder(env) { let v = bitXor(env); while (peek() === "|") { naechst(); v = Boolean(v | bitXor(env)); } return v; }
  function bitXor(env) { let v = bitUnd(env); while (peek() === "^") { naechst(); v = Boolean(v ^ bitUnd(env)); } return v; }
  function bitUnd(env) { let v = atom(env); while (peek() === "&") { naechst(); v = Boolean(v & atom(env)); } return v; }
  function atom(env) {
    const t = naechst();
    if (t === "(") { const v = oder(env); if (naechst() !== ")") throw new Error("Klammer fehlt"); return v; }
    if (t === "True") return true;
    if (t === "False") return false;
    if (t !== undefined && Object.prototype.hasOwnProperty.call(env, t)) return env[t];
    throw new Error(`Unbekannt: ${t}`);
  }
  return (env) => { i = 0; const v = oder(env); if (i < toks.length) throw new Error("Zu viel"); return v; };
}

function visWahrheitstabelle(box, d) {
  const vars = d.variablen || ["a", "b"];
  const ausdr = d.ausdruecke || [];
  const parser = ausdr.map(a => { try { return boolParser(a); } catch { return null; } });
  const t = h("table", { class: "wt" });
  t.append(h("thead", null, h("tr", null,
    vars.map(v => h("th", { text: v })),
    ausdr.map((a, i) => h("th", { class: "ergebnis-spalte" + (i === 0 ? " trenner" : ""), text: a })))));
  const body = h("tbody");
  const n = vars.length;
  const zelle = (val) => val === null || val === undefined ? h("span", { class: "wb", text: "?" })
    : h("span", { class: "wb " + (val ? "wahr" : "falsch") }, val ? "✓ True" : "✗ False");
  // Bevorzugt die von Python berechneten Zeilen (markup.py), sonst eigene Auswertung
  const zeilen = Array.isArray(d.zeilen) && d.zeilen.length ? d.zeilen : null;
  for (let z = 0; z < (zeilen ? zeilen.length : (1 << n)); z++) {
    const env = {};
    let ergebnisse;
    if (zeilen) {
      vars.forEach((v, k) => { env[v] = zeilen[z].werte[k]; });
      ergebnisse = zeilen[z].ergebnisse || [];
    } else {
      vars.forEach((v, k) => { env[v] = !((z >> (n - 1 - k)) & 1); });
      ergebnisse = parser.map(p => { try { return p ? p(env) : null; } catch { return null; } });
    }
    const tr = h("tr", { style: { animationDelay: reduziert() ? "0s" : `${z * 0.08}s` } },
      vars.map(v => h("td", null, zelle(env[v]))),
      ausdr.map((_, i) => h("td", { class: i === 0 ? "trenner" : "" }, zelle(ergebnisse[i]))));
    body.append(tr);
  }
  t.append(body);
  box.append(h("div", { class: "vis-scroll" }, t));
  const xor = ausdr.some(a => /\^|!=/.test(a));
  box.append(h("p", { class: "vis-unterschrift", html: "<code>and</code> ist nur <code>True</code>, wenn <b>beide</b> Seiten <code>True</code> sind. <code>or</code> ist <code>True</code>, sobald <b>mindestens eine</b> Seite <code>True</code> ist. <code>not</code> dreht um."
    + (xor ? " <code>^</code> (XOR, „entweder – oder“) und <code>!=</code> sind <code>True</code>, wenn <b>genau eine</b> Seite <code>True</code> ist." : "") }));
}

/* ------------------------------------------------------------------ stapel */
function visStapel(box, d) {
  const rahmen = d.rahmen || [];
  const rueck = d.rueckgaben || [];
  const n = rahmen.length;
  const turm = h("div", { class: "stapel-turm", "aria-live": "polite" });
  const log = h("div", { class: "stapel-log" });
  box.append(h("div", { class: "stapel-vis" }, turm, h("div", null, h("div", { class: "vis-titel", text: "Was passiert?" }), log)));
  const maxZ = n + (rueck.length ? n : 0);
  let z = n, timer = null;
  const zaehler = h("span", { class: "zaehler" });
  const zurueck = knopf("◀", () => zeigen(z - 1), { "aria-label": "Schritt zurück" });
  const vor = knopf("▶", () => zeigen(z + 1), { "aria-label": "Schritt vor" });
  const spiel = knopf("▶ Abspielen", () => abspielen());
  const logEintraege = [];
  for (let k = 0; k < n; k++) logEintraege.push({ text: `📥 ${rahmen[k]} wird aufgerufen – neuer Teller oben drauf`, ret: false });
  if (rueck.length) for (let k = n - 1; k >= 0; k--) logEintraege.push({ text: `📤 ${rahmen[k]} ist fertig und gibt ${rueck[k] ?? "?"} zurück`, ret: true });

  function zeigen(neu, animiert = true) {
    neu = Math.max(0, Math.min(maxZ, neu));
    const vorwaerts = neu === z + 1;
    z = neu;
    turm.replaceChildren();
    const sichtbar = z <= n ? z : n - (z - n);
    for (let k = 0; k < sichtbar; k++) {
      const oben = k === sichtbar - 1;
      const el = h("div", { class: "teller" + (oben ? " oben" : "") }, h("span", { text: rahmen[k] }));
      if (!animiert || !vorwaerts || !(oben && z <= n)) el.style.animation = "none";
      turm.append(el);
    }
    if (z > n) {
      const k = n - (z - n);
      const raus = h("div", { class: "teller raus" }, h("span", { text: rahmen[k] }), h("span", { class: "rueck", text: "↩ " + (rueck[k] ?? "") }));
      if (!animiert) raus.style.display = "none";
      turm.append(raus);
    }
    if (!sichtbar && z > n) turm.append(h("div", { class: "tr-leer", text: "Stapel leer – alles fertig ✓" }));
    log.replaceChildren(...logEintraege.slice(0, z).map((e, i) => h("div", { class: (e.ret ? "ret" : "") + (i === z - 1 ? " aktiv" : ""), text: e.text })));
    log.scrollTop = log.scrollHeight;
    zaehler.textContent = `${z} / ${maxZ}`;
    zurueck.disabled = z === 0; vor.disabled = z === maxZ;
  }
  function abspielen() {
    if (timer) { clearInterval(timer); timer = null; spiel.textContent = "▶ Abspielen"; return; }
    zeigen(0, false);
    spiel.textContent = "⏸ Pause";
    timer = setInterval(() => {
      if (z >= maxZ || !box.isConnected) { clearInterval(timer); timer = null; spiel.textContent = "▶ Abspielen"; return; }
      zeigen(z + 1);
    }, 1100);
  }
  box.append(h("div", { class: "vis-steuer" }, zurueck, zaehler, vor, spiel));
  box.append(h("p", { class: "vis-unterschrift", html: "Jeder Funktionsaufruf legt einen neuen <b>Teller</b> (Rahmen) oben auf den Stapel. Nur der <b>oberste</b> arbeitet. Ist er fertig, wird er mit seinem Rückgabewert abgeräumt." }));
  zeigen(n, false);
}

/* -------------------------------------------------------------------- baum */
function visBaum(box, d) {
  const wurzel = d.wurzel;
  if (!wurzel) { box.append(h("div", { class: "vis-fehler", text: "Kein Baum angegeben." })); return; }
  const CW = 8.2, NH = 34, DY = 74, GAP = 14;
  let blattX = 0, maxTiefe = 0;
  const knoten = [];
  const layout = (k, tiefe) => {
    const text = String(k.text ?? "");
    const w = Math.max(54, text.length * CW + 22);
    const node = { text, w, tiefe, kinder: [] };
    maxTiefe = Math.max(maxTiefe, tiefe);
    const kinder = k.kinder || [];
    if (!kinder.length) { node.x = blattX + w / 2; blattX += w + GAP; }
    else {
      node.kinder = kinder.map(c => layout(c, tiefe + 1));
      const a = node.kinder[0].x, b = node.kinder[node.kinder.length - 1].x;
      node.x = (a + b) / 2;
      // Platz für breite Elternknoten
      if (node.x - w / 2 < 0) { /* selten */ }
    }
    knoten.push(node);
    return node;
  };
  const r = layout(wurzel, 0);
  const W = Math.max(blattX - GAP, r.w) + 20, H = (maxTiefe + 1) * DY - DY + NH + 20;
  const s = svg("svg", { class: "baum-svg", viewBox: `-10 -10 ${W} ${H}`, width: W, role: "img", "aria-label": "Aufrufbaum" });
  const kanten = svg("g"), nodes = svg("g");
  s.append(kanten, nodes);
  const verz = (t) => (reduziert() ? "0s" : `${t * 0.35}s`);
  for (const k of knoten) {
    const y = k.tiefe * DY;
    for (const c of k.kinder) {
      const yc = c.tiefe * DY;
      kanten.append(svg("path", { class: "kante", d: `M${k.x},${y + NH} C${k.x},${y + NH + 22} ${c.x},${yc - 22} ${c.x},${yc}`, style: `animation-delay:${verz(c.tiefe)}` }));
    }
    nodes.append(svg("g", { class: "knoten" + (k.tiefe === 0 ? " wurzel" : "") + (!k.kinder.length ? " blatt" : ""), style: `animation-delay:${verz(k.tiefe)}` },
      svg("rect", { x: k.x - k.w / 2, y, width: k.w, height: NH, rx: 10 }),
      svg("text", { x: k.x, y: y + NH / 2 }, k.text)));
  }
  box.append(h("div", { class: "vis-scroll" }, s));
  box.append(h("p", { class: "vis-unterschrift", html: `Jeder Kasten ist ein Funktionsaufruf, die Linien zeigen, wer wen aufruft. Grün = <b>Basisfall</b> (ruft nichts mehr auf). Insgesamt <b>${knoten.length}</b> Aufrufe.` }));
}

/* ---------------------------------------------------------------- funktion */
function visFunktion(box, d) {
  const eingaben = d.eingaben || [];
  const name = d.name || "f";
  const werte = eingaben.map(e => String(e).split("=").slice(1).join("=").trim() || String(e));
  const m = h("div", { class: "maschine" },
    h("div", { class: "m-ein" }, h("span", { class: "m-lbl", text: "Eingabe (Parameter)" }), eingaben.map(e => h("span", { class: "m-chip", text: e }))),
    h("div", { class: "m-box" },
      h("div", null, h("span", { class: "m-zahnrad", "aria-hidden": "true", text: "⚙️" })),
      h("div", { class: "m-name", text: `def ${name}(${eingaben.map(e => String(e).split("=")[0].trim()).join(", ")}):` }),
      d.innen ? h("pre", { html: highlight(d.innen) }) : null),
    h("div", { class: "m-aus" }, h("span", { class: "m-lbl", text: "Ausgabe (return)" }), h("span", { class: "m-chip aus", text: d.ausgabe ?? "None" })));
  box.append(m);
  const start = knopf("▶ Maschine starten", () => { m.classList.remove("laeuft"); void m.offsetWidth; m.classList.add("laeuft"); });
  box.append(h("div", { class: "vis-steuer" }, start,
    h("span", { class: "vis-unterschrift", style: { margin: 0 }, html: `<code>${esc(name)}(${esc(werte.join(", "))})</code> → <code>${esc(d.ausgabe ?? "None")}</code>` })));
  box.append(h("p", { class: "vis-unterschrift", html: "Eine Funktion ist wie eine Maschine: Oben kommen Werte hinein (Parameter), innen wird gearbeitet, mit <code>return</code> kommt das Ergebnis heraus." }));
}

/* ------------------------------------------------------------------- typen */
const TYP_INFO = {
  int: "ganze Zahlen", float: "Kommazahlen", str: "Text", bool: "Wahrheitswerte", NoneType: "„nichts“",
  list: "Listen", tuple: "Tupel", dict: "Wörterbücher", set: "Mengen", andere: "Sonstiges",
};
function visTypen(box, d) {
  const werte = (d.werte || []).map(String);
  const grid = h("div", { class: "typen-vis" });
  box.append(grid);
  const fuellen = (typen) => {
    const faecher = new Map();
    werte.forEach((w, i) => {
      const t = typen[i] || literalTyp(w);
      if (!faecher.has(t)) faecher.set(t, []);
      faecher.get(t).push(w);
    });
    const ordnung = Object.keys(TYP_INFO);
    grid.replaceChildren(...[...faecher.entries()].sort((a, b) => ordnung.indexOf(a[0]) - ordnung.indexOf(b[0])).map(([t, ws]) =>
      h("div", { class: `typ-fach ${typKlasse(t)}` },
        h("h4", null, h("span", { text: t === "NoneType" ? "NoneType" : t }), h("small", { text: TYP_INFO[t] || "" })),
        h("div", { class: "werte" }, ws.map((w, i) => h("span", { class: "w", text: w, style: { animationDelay: reduziert() ? "0s" : `${i * 0.12}s` } }))))));
  };
  if (Array.isArray(d.typen) && d.typen.length === werte.length) {
    // markup.py hat die Typen bereits mit Python bestimmt
    fuellen(d.typen.map(t => (t.typ === "unbekannt" ? "andere" : t.typ)));
  } else {
    fuellen([]);
    const qs = werte.map(w => "w=" + encodeURIComponent(w)).join("&");
    api.get("/api/visual/typen?" + qs).then(r => {
      if (Array.isArray(r.typen)) fuellen(r.typen);
    }).catch(() => { /* lokale Bestimmung bleibt */ });
  }
  box.append(h("p", { class: "vis-unterschrift", html: "Jeder Wert hat einen <b>Datentyp</b>. Mit <code>type(wert)</code> fragst du Python danach." }));
}
