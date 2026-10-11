// Renderer für alle Markup-Blöcke aus markup.parse() (Vertrag Abschnitt 3).
import { h, inline, EMOJI_ANFANG } from "./util.js";
import { codeAnzeige } from "./highlight.js";
import { codeBeispiel } from "./runner.js";
import { visual } from "./visuals.js";

const BOX = {
  analogie: { icon: "💡", label: "Alltagsbeispiel" },
  achtung: { icon: "⚠️", label: "Typischer Fehler" },
  info: { icon: "ℹ️", label: "Gut zu wissen" },
};

export function renderBloecke(bloecke, { klasse = "" } = {}) {
  const wrap = h("div", { class: "md " + klasse });
  for (const b of bloecke || []) {
    try { wrap.append(renderBlock(b)); } catch (e) {
      console.error(e, b);
      wrap.append(h("div", { class: "vis-fehler", text: `Block „${b && b.typ}“ konnte nicht angezeigt werden: ${e.message}` }));
    }
  }
  return wrap;
}

/** Mehrere Seiten -> ein Element (z. B. Merkzettel, Spickzettel). */
export function renderSeiten(seiten, opts) {
  const wrap = h("div", { class: "md-seiten" });
  (seiten || []).forEach((s, i) => {
    if (i > 0) wrap.append(h("hr", { style: { border: 0, borderTop: "1px dashed var(--border-strong)", margin: "22px 0" } }));
    wrap.append(renderBloecke(s, opts));
  });
  return wrap;
}

export function renderBlock(b) {
  switch (b.typ) {
    case "ueberschrift": return h("h3", { class: "md-h", html: inline(b.text) });
    case "absatz": return h("p", { html: inline(b.text) });
    case "merke": return h("div", { class: "md-merke" }, h("span", { class: "stern", "aria-hidden": "true", text: "★" }),
      h("div", null, h("span", { class: "merke-label", text: "Merke" }), h("span", { html: inline(b.text) })));
    case "codeblock": return codeAnzeige(b.code, { nummern: String(b.code || "").split("\n").length > 4 });
    case "liste": return h(b.nummeriert ? "ol" : "ul", { class: "md-liste" }, (b.punkte || []).map(p => h("li", { html: inline(p) })));
    case "tabelle": {
      const t = h("table", { class: "md-tabelle" });
      if (b.kopf && b.kopf.length) t.append(h("thead", null, h("tr", null, b.kopf.map(k => h("th", { html: inline(k) })))));
      t.append(h("tbody", null, (b.zeilen || []).map(z => h("tr", null, z.map(c => h("td", { html: inline(c) }))))));
      return h("div", { class: "md-tabelle-wrap" }, t);
    }
    case "box": {
      const art = BOX[b.art] ? b.art : "info";
      let icon = BOX[art].icon, titel = b.titel || "";
      const m = EMOJI_ANFANG.exec(titel);
      if (m) { icon = m[1]; titel = titel.slice(m[0].length); }
      return h("aside", { class: `box box-${art}`, "aria-label": BOX[art].label },
        h("div", { class: "box-kopf" }, h("span", { class: "box-icon", "aria-hidden": "true", text: icon }),
          h("div", null, h("span", { class: "box-label", text: (art === "analogie" ? "💡 " : "") + BOX[art].label }), titel ? h("span", { class: "box-titel", html: inline(titel) }) : null)),
        renderBloecke(b.bloecke || []));
    }
    case "code": return codeBeispiel(b);
    case "visual": return visual(b.art, b.daten, b.fehler);
    case "vergleich": {
      const [t1, t2] = b.titel || ["", ""];
      const [s1, s2] = b.spalten || [[], []];
      return h("div", { class: "vergleich" },
        h("div", null, h("h4", { html: inline(t1 || "") }), renderBloecke(s1)),
        h("div", null, h("h4", { html: inline(t2 || "") }), renderBloecke(s2)));
    }
    default:
      return h("p", { html: inline(b.text || "") });
  }
}

/** Erklärungstext einer Antwort: Blöcke (vom Server geparst) oder einfacher Text. */
export function erklaerungElement(ergebnis) {
  if (Array.isArray(ergebnis.erklaerung_bloecke) && ergebnis.erklaerung_bloecke.length) return renderBloecke(ergebnis.erklaerung_bloecke);
  if (!ergebnis.erklaerung) return null;
  const wrap = h("div", { class: "md" });
  String(ergebnis.erklaerung).trim().split(/\n\s*\n/).forEach(a => wrap.append(h("p", { html: inline(a).replace(/\n/g, "<br>") })));
  return wrap;
}
