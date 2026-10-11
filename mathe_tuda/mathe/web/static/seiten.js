// Formelsammlung, Glossar, Spielwiese (Formel-Spielplatz) und Demo-Seiten.
import { h, inline, nurText, lade, lokal, debounce, $$ } from "./util.js";
import { api } from "./api.js";
import { texHtml, texFehler } from "./formel.js";
import { renderBloecke, renderSeiten, rechenwegElement } from "./markup.js";
import { eingabeFeld } from "./eingabe.js";
import { koordinaten, auswerten, regler } from "./plot.js";

/* ------------------------------------------------------------ Suche (gemeinsam) */
function markieren(wurzel, q) {
  const walker = document.createTreeWalker(wurzel, NodeFilter.SHOW_TEXT);
  const knoten = [];
  while (walker.nextNode()) knoten.push(walker.currentNode);
  for (const t of knoten) {
    const text = t.nodeValue, i = text.toLowerCase().indexOf(q);
    if (i < 0 || t.parentElement.closest("button, .katex, summary .pfeil")) continue;
    const frag = document.createDocumentFragment();
    frag.append(text.slice(0, i), h("mark", { class: "treffer", text: text.slice(i, i + q.length) }), text.slice(i + q.length));
    t.replaceWith(frag);
  }
}
function suchtext(el) {
  // Text + lesbare Formel (KaTeX legt eine MathML-Annotation mit dem LaTeX-Quelltext ab)
  return (el.textContent + " " + [...el.querySelectorAll("annotation")].map(a => a.textContent).join(" ")).toLowerCase();
}

/* ------------------------------------------------------------ Formelsammlung */
export async function formelsammlung(main) {
  document.title = "Formelsammlung · Mathe für Informatik";
  main.replaceChildren(lade());
  const d = await api.get("/api/formelsammlung");
  const suche = h("input", { class: "feld", type: "search", placeholder: "Suchen, z. B. „Bruch“, „binomisch“, „frac“ …", "aria-label": "Formelsammlung durchsuchen" });
  let teil = lokal.get("fs_teil", "alle");
  const tabBar = h("div", { class: "spick-tabs", role: "tablist" });
  const allgemein = h("section", { class: "karte spick-seite", "aria-label": "Allgemein" }, renderSeiten(d.seiten));
  const kapitel = h("section", { "aria-label": "Merkzettel je Kapitel" },
    (d.kapitel || []).map(k => h("details", { class: "karte spick-kapitel", "data-teil": k.teil, open: true },
      h("summary", null, h("span", { class: "k-ico", "aria-hidden": "true", text: k.icon }), h("span", { html: `${k.nummer}. ${inline(k.titel)}` }), h("span", { class: "pfeil", "aria-hidden": "true", text: "▶" })),
      h("div", { class: "spick-inhalt" }, renderSeiten(k.seiten), h("a", { class: "btn btn-sm btn-soft nicht-drucken", style: { marginTop: "14px" }, href: `#/kapitel/${k.slug}`, text: "Zum Kapitel →" })))));
  const leer = h("div", { class: "leer-hinweis", hidden: true }, h("span", { class: "gross", text: "🔍" }), "Nichts gefunden. Versuch einen anderen Begriff.");
  const tabs = [["alle", "Alles"], ...d.teile.filter(t => d.kapitel.some(k => k.teil === t.id)).map(t => [t.id, t.titel.split(" – ")[0]])];
  const malenTabs = () => tabBar.replaceChildren(...tabs.map(([id, name]) => h("button", { class: "tab", role: "tab", type: "button", "aria-selected": String(id === teil), text: name,
    onclick: () => { teil = id; lokal.set("fs_teil", id); malenTabs(); filtern(); } })));
  const filtern = () => {
    const q = suche.value.trim().toLowerCase();
    $$("mark.treffer", main).forEach(m => m.replaceWith(document.createTextNode(m.textContent)));
    main.normalize();
    let treffer = 0;
    allgemein.hidden = teil !== "alle" || (q && !suchtext(allgemein).includes(q));
    if (!allgemein.hidden && q) { treffer++; markieren(allgemein, q); }
    for (const det of kapitel.querySelectorAll(".spick-kapitel")) {
      const passt = (teil === "alle" || det.dataset.teil === teil) && (!q || suchtext(det).includes(q));
      det.classList.toggle("versteckt-suche", !passt);
      if (passt && q) { treffer++; markieren(det, q); det.open = true; }
    }
    leer.hidden = !q || treffer > 0;
  };
  suche.addEventListener("input", debounce(filtern, 150));
  malenTabs();
  main.replaceChildren(h("div", { class: "container" },
    h("div", { class: "seitenkopf" }, h("div", null, h("h1", { text: "📋 Formelsammlung" }), h("p", { text: "Alle Merkzettel an einem Ort – zum Nachschlagen und Ausdrucken." })),
      h("button", { class: "btn nicht-drucken", type: "button", text: "🖨 Drucken", onclick: () => window.print() })),
    h("div", { class: "such-feld nicht-drucken" }, suche), h("div", { class: "nicht-drucken" }, tabBar), leer, allgemein, kapitel));
  filtern();
  suche.focus();
  return null;
}

/* ------------------------------------------------------------ Glossar */
export async function glossar(main, _b, query) {
  document.title = "Glossar · Mathe für Informatik";
  main.replaceChildren(lade());
  const d = await api.get("/api/glossar");
  const suche = h("input", { class: "feld", type: "search", placeholder: "Begriff suchen, z. B. „injektiv“ …", "aria-label": "Glossar durchsuchen", value: query?.get("q") || "" });
  const liste = h("div", { class: "glossar-liste" }, d.eintraege.map(e => h("article", { class: "karte glossar-eintrag", id: "g-" + encodeURIComponent(e.begriff) },
    h("h3", { html: inline(e.begriff) }), e.synonyme.length ? h("p", { class: "synonyme", text: "auch: " + e.synonyme.join(", ") }) : null,
    h("p", { html: inline(e.erklaerung) }), e.beispiel ? h("p", { class: "tip-beispiel", html: "Beispiel: " + inline(e.beispiel) }) : null,
    e.kapitel ? h("a", { class: "chip primary", href: `#/kapitel/${e.kapitel}`, html: "📘 " + inline(e.kapitel_titel || e.kapitel) }) : null)));
  const leer = h("div", { class: "leer-hinweis", hidden: true, text: d.eintraege.length ? "Kein passender Begriff." : "Das Glossar füllt sich mit jedem Kapitel." });
  const filtern = () => {
    const q = suche.value.trim().toLowerCase();
    let n = 0;
    for (const el of liste.children) { const p = !q || suchtext(el).includes(q); el.hidden = !p; n += p; }
    leer.hidden = n > 0;
  };
  suche.addEventListener("input", debounce(filtern, 120));
  main.replaceChildren(h("div", { class: "container" },
    h("div", { class: "seitenkopf" }, h("div", null, h("h1", { text: "📖 Glossar" }), h("p", { text: "Jeder Fachbegriff mit einer kurzen Erklärung und einem Beispiel. Unterstrichene Wörter in den Kapiteln führen hierher." }))),
    h("div", { class: "such-feld" }, suche), leer, liste));
  filtern();
  suche.focus();
  return null;
}

/* ------------------------------------------------------------ Spielwiese */
const WERKZEUGE = [
  { id: "plotter", icon: "📈", name: "Funktionsplotter" },
  { id: "bruch", icon: "🥧", name: "Bruchrechner" },
  { id: "matrix", icon: "▦", name: "Matrixrechner" },
  { id: "lgs", icon: "🧩", name: "LGS-Löser (Gauß)" },
  { id: "primfaktoren", icon: "🔢", name: "Primfaktoren" },
  { id: "basis", icon: "💾", name: "Basiswandler" },
];

export function spielwiese(main, werkzeug) {
  document.title = "Spielwiese · Mathe für Informatik";
  const aktiv = WERKZEUGE.find(w => w.id === werkzeug) || WERKZEUGE[0];
  const tabs = h("div", { class: "spick-tabs", role: "tablist" }, WERKZEUGE.map(w => h("a", { class: "tab", role: "tab", href: `#/spielwiese/${w.id}`, "aria-selected": String(w.id === aktiv.id), text: `${w.icon} ${w.name}` })));
  const flaeche = h("div", { class: "karte spielwiese-karte" });
  main.replaceChildren(h("div", { class: "container" },
    h("div", { class: "seitenkopf" }, h("div", null, h("h1", { text: "🧪 Spielwiese" }), h("p", { text: "Probier alles aus – mit vollständigem Rechenweg. Nichts wird bewertet." }))),
    tabs, flaeche));
  ({ plotter, bruch: bruchRechner, matrix: matrixRechner, lgs: lgsLoeser, primfaktoren: primRechner, basis: basisWandler })[aktiv.id](flaeche);
  return null;
}

function ergebnisAnzeige() {
  const el = h("div", { class: "spiel-ergebnis", "aria-live": "polite" });
  return {
    el,
    zeigen(r) {
      if (r.fehler) { el.replaceChildren(h("div", { class: "vis-fehler", text: r.fehler })); return; }
      el.replaceChildren(h("div", { class: "formel-block gross", html: texHtml(r.ergebnis, true) }),
        h("div", { class: "f-rechenweg" }, h("span", { class: "lbl", text: "Rechenweg" }), rechenwegElement(r.rechenweg_bloecke) || ""));
    },
  };
}
async function rechnen(werkzeug, body, anzeige) {
  try { anzeige.zeigen(await api.post(`/api/spielwiese/${werkzeug}`, body)); } catch (e) { anzeige.zeigen({ fehler: e.message }); }
}

function plotter(box) {
  const funktionen = [{ ast: null, tex: "" }];
  const ein = eingabeFeld({ modus: "term", variablen: ["x", "a"], wert: lokal.get("plot_term", "x^2 - 2x - 3"), label: "f(x)" });
  let a = 1;
  const k = koordinaten({ x: [-6, 6], y: [-6, 6] }, (k) => { if (funktionen[0].ast) k.kurve((x) => auswerten(funktionen[0].ast, { x, a }), "kurve", "var(--plot-1)"); });
  const laden = debounce(async () => {
    lokal.set("plot_term", ein.wert());
    try {
      const r = await api.post("/api/term/vorschau", { text: ein.wert(), typ: "term", variablen: ["x", "a"], ast: true });
      if (r.ast) { funktionen[0].ast = r.ast; k.neu(); }
    } catch { /* egal */ }
  }, 300);
  ein.inp.addEventListener("input", laden);
  const rA = regler({ name: "a", von: -5, bis: 5, schritt: 0.25, wert: 1, oninput: (v) => { a = v; k.neu(); } });
  box.append(h("h2", { text: "📈 Funktionsplotter" }), h("p", { class: "antwort-hinweis", html: "Tippe einen Term mit <code class=\"ic\">x</code> ein. Mit dem Parameter <code class=\"ic\">a</code> und dem Regler kannst du die Funktion verändern." }),
    h("div", { class: "plot-eingabe" }, h("span", { html: texHtml("f(x) =") }), ein.el), h("div", { class: "vis-scroll" }, k.el), h("div", { class: "regler-reihe" }, rA.el));
  laden();
}

function bruchRechner(box) {
  const a = eingabeFeld({ modus: "zahl", wert: "1/2", label: "erster Bruch" }), b = eingabeFeld({ modus: "zahl", wert: "1/3", label: "zweiter Bruch" });
  const op = h("select", { class: "feld schmal-feld", "aria-label": "Rechenart" }, ["+", "-", "·", ":"].map(o => h("option", { value: o === "·" ? "*" : o === ":" ? "/" : o, text: o })));
  const anzeige = ergebnisAnzeige();
  const los = h("button", { class: "btn btn-primary", type: "button", text: "Rechnen", onclick: () => rechnen("bruch", { a: a.wert(), b: b.wert(), op: op.value }, anzeige) });
  box.append(h("h2", { text: "🥧 Bruchrechner" }), h("div", { class: "spiel-zeile" }, a.el, op, b.el, los), anzeige.el);
  los.click();
}

function matrixFeld(wert, label) {
  return h("textarea", { class: "feld mono matrix-text", rows: 3, "aria-label": label, text: wert, spellcheck: "false" });
}
function matrixRechner(box) {
  const ta = matrixFeld("2 1\n1 3", "Matrix A"), tb = matrixFeld("1 0\n4 2", "Matrix B");
  const op = h("select", { class: "feld schmal-feld", "aria-label": "Operation" }, [["det", "Determinante det(A)"], ["inverse", "Inverse A⁻¹"], ["transponiert", "Transponierte Aᵀ"], ["mult", "Produkt A · B"]].map(([v, t]) => h("option", { value: v, text: t })));
  const bWrap = h("label", { class: "matrix-wrap", hidden: true }, "B =", tb);
  op.onchange = () => { bWrap.hidden = op.value !== "mult"; };
  const anzeige = ergebnisAnzeige();
  const los = h("button", { class: "btn btn-primary", type: "button", text: "Rechnen", onclick: () => rechnen("matrix", { a: ta.value, b: tb.value, op: op.value }, anzeige) });
  box.append(h("h2", { text: "▦ Matrixrechner" }), h("p", { class: "antwort-hinweis", text: "Eine Zeile pro Matrixzeile, Einträge mit Leerzeichen trennen. Brüche wie 1/2 sind erlaubt." }),
    h("div", { class: "spiel-zeile" }, h("label", { class: "matrix-wrap" }, "A =", ta), bWrap, op, los), anzeige.el);
  los.click();
}
function lgsLoeser(box) {
  const ta = matrixFeld("1 1 1 6\n1 -1 2 5\n2 1 -1 1", "erweiterte Koeffizientenmatrix");
  const anzeige = ergebnisAnzeige();
  const los = h("button", { class: "btn btn-primary", type: "button", text: "Lösen", onclick: () => rechnen("lgs", { a: ta.value }, anzeige) });
  box.append(h("h2", { text: "🧩 LGS-Löser mit Gauß-Schritten" }), h("p", { class: "antwort-hinweis", html: "Eine Zeile pro Gleichung: erst die Koeffizienten, die <b>letzte Zahl ist die rechte Seite</b>. Beispiel: <code class=\"ic\">1 1 1 6</code> steht für x + y + z = 6." }),
    h("div", { class: "spiel-zeile" }, ta, los), anzeige.el);
  los.click();
}
function primRechner(box) {
  const ein = eingabeFeld({ modus: "zahl", wert: "360", label: "Zahl" });
  const anzeige = ergebnisAnzeige();
  const los = h("button", { class: "btn btn-primary", type: "button", text: "Zerlegen", onclick: () => rechnen("primfaktoren", { n: ein.wert() }, anzeige) });
  box.append(h("h2", { text: "🔢 Primfaktorzerlegung" }), h("div", { class: "spiel-zeile" }, ein.el, los), anzeige.el);
  los.click();
}
function basisWandler(box) {
  const zahl = h("input", { class: "feld mono schmal-feld", value: "45", "aria-label": "Zahl" });
  const von = h("input", { class: "feld schmal-feld", type: "number", min: 2, max: 36, value: 10, "aria-label": "von Basis" });
  const nach = h("input", { class: "feld schmal-feld", type: "number", min: 2, max: 36, value: 2, "aria-label": "nach Basis" });
  const anzeige = ergebnisAnzeige();
  const los = h("button", { class: "btn btn-primary", type: "button", text: "Umwandeln", onclick: () => rechnen("basis", { zahl: zahl.value, von: von.value, nach: nach.value }, anzeige) });
  box.append(h("h2", { text: "💾 Basiswandler" }), h("div", { class: "spiel-zeile" }, zahl, h("span", { text: "von Basis" }), von, h("span", { text: "nach Basis" }), nach, los), anzeige.el);
  los.click();
}

/* ------------------------------------------------------------ Demo */
export async function demo(main, art) {
  document.title = "Demo · Mathe für Informatik";
  const c = h("div", { class: "container" });
  main.replaceChildren(c);
  if (art === "formeln") {
    // Alle Formeln aller Inhalte streng mit KaTeX prüfen (nur mit --e2e verfügbar)
    const r = await api.get("/api/e2e/formeln");
    const fehler = r.formeln.map(f => [f, texFehler(f)]).filter(([, e]) => e);
    c.append(h("h1", { text: "Formel-Prüfung" }), h("pre", { id: "formel-ergebnis", text: JSON.stringify({ anzahl: r.formeln.length, fehler }, null, 1) }));
    return null;
  }
  c.append(h("div", { class: "seitenkopf" }, h("div", null, h("h1", { text: "Demo: Visualisierungen" }), h("p", { text: "Jeder fertige :::visual-Typ mit Beispieldaten aus mathe/demo.py." }))));
  const d = await api.get("/api/demo/visuals");
  const nur = (new URLSearchParams(location.search).get("typen") || "").split(",").filter(Boolean);
  const grid = h("div", { class: "demo-grid" });
  for (const b of d.bloecke) {
    if (nur.length && !nur.includes(b.art || b.typ)) continue;
    grid.append(h("section", { class: "demo-teil" }, h("h2", { text: b.typ === "visual" ? `:::visual ${b.art}` : `:::${b.typ}` }), renderBloecke([b])));
  }
  c.append(grid);
  return null;
}

export { nurText };
