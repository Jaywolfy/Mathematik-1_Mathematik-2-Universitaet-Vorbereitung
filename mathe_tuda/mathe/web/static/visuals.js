// Visualisierungen (Vertrag Abschnitt 4): Rahmen + Register. Die Typen liegen nach Themen
// in eigenen Modulen und werden erst geladen, wenn sie gebraucht werden.
import { h, inline } from "./util.js";

const MODUL = {
  zahlenstrahl: "vis_basis", bruch: "vis_basis", rechnung: "vis_basis", funktionsgraph: "vis_basis", parabel: "vis_basis",
  // vis_diskret.js
  venn: "vis_diskret", wahrheitstabelle: "vis_diskret", relation_graph: "vis_diskret", pascal: "vis_diskret",
  euklid: "vis_diskret", modulo_uhr: "vis_diskret", induktion_domino: "vis_diskret", folge: "vis_diskret",
  // vis_funktionen.js, vis_linalg.js
  einheitskreis: "vis_funktionen", exp_log: "vis_funktionen", tangente: "vis_funktionen", riemann: "vis_funktionen",
  vektoren2d: "vis_linalg", matrix_mult: "vis_linalg", gauss: "vis_linalg", komplexe_ebene: "vis_linalg",
  // vis_ordnung.js
  graph_gerichtet: "vis_ordnung", hasse: "vis_ordnung", aequivalenz_klassen: "vis_ordnung",
};
export const VISUAL_TYPEN = Object.keys(MODUL);

const TITEL = {
  zahlenstrahl: "📏 Zahlenstrahl", bruch: "🥧 Bruch", rechnung: "⚖️ Die Waage", funktionsgraph: "📈 Funktionsgraph",
  parabel: "⌒ Parabel",
  // vis_diskret.js
  venn: "🔵 Mengendiagramm", wahrheitstabelle: "🔢 Wahrheitstabelle", relation_graph: "➡️ Zuordnung",
  pascal: "🔺 Pascalsches Dreieck", euklid: "➗ Euklidischer Algorithmus", modulo_uhr: "🕒 Modulo-Uhr",
  induktion_domino: "⛓️ Induktion als Dominokette", folge: "📉 Folge",
  // vis_funktionen.js, vis_linalg.js
  einheitskreis: "⭕ Einheitskreis", exp_log: "📈 Exponential & Logarithmus", tangente: "📐 Sekante & Tangente",
  riemann: "▥ Riemann-Summe", vektoren2d: "↗️ Vektoren", matrix_mult: "✖️ Matrixmultiplikation",
  gauss: "🧮 Gauß-Verfahren", komplexe_ebene: "🌀 Komplexe Zahlenebene",
  // vis_ordnung.js
  graph_gerichtet: "🔁 Relation als Graph", hasse: "🧱 Hasse-Diagramm", aequivalenz_klassen: "🎨 Äquivalenzklassen",
};

const geladen = new Map();
function laden(modul) {
  if (!geladen.has(modul)) geladen.set(modul, import(`./${modul}.js`));
  return geladen.get(modul);
}

export function visual(art, daten, fehler = null) {
  const box = h("figure", { class: `visual vis-${art}` });
  if (fehler) {
    box.append(h("div", { class: "vis-fehler", text: `Visualisierung „${art}“ konnte nicht gelesen werden: ${fehler}` }));
    return box;
  }
  const d = daten || {};
  box.append(h("figcaption", { class: "vis-titel", html: d.titel ? inline(d.titel) : (TITEL[art] || art) }));
  const koerper = h("div", { class: "vis-koerper" });
  box.append(koerper);
  if (d.unterschrift) box.append(h("p", { class: "vis-unterschrift", html: inline(d.unterschrift) }));
  if (!MODUL[art]) {
    koerper.append(h("div", { class: "vis-fehler", text: `Unbekannter Visualisierungstyp „${art}“.` }));
    return box;
  }
  box.dataset.laedt = "1";
  laden(MODUL[art]).then(m => {
    try { m.BAUER[art](koerper, d); } catch (e) {
      console.error(e);
      koerper.append(h("div", { class: "vis-fehler", text: `Fehler beim Zeichnen: ${e.message}` }));
    }
  }).catch(e => koerper.append(h("div", { class: "vis-fehler", text: `Modul fehlt: ${e.message}` })))
    .finally(() => { delete box.dataset.laedt; });
  return box;
}

export function knopf(text, onclick, extra = {}) {
  return h("button", { class: "btn btn-sm", type: "button", text, onclick, ...extra });
}
