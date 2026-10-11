// Renderer für alle Markup-Blöcke aus markup.parse() (Vertrag Abschnitt 3).
import { h, inline, EMOJI_ANFANG, reduziert } from "./util.js";
import { texHtml } from "./formel.js";
import { visual } from "./visuals.js";

const BOX = {
  analogie: { icon: "💡", label: "Alltagsbild" },
  achtung: { icon: "⚠️", label: "Typischer Fehler" },
  info: { icon: "ℹ️", label: "Gut zu wissen" },
  warum: { icon: "💻", label: "Wozu brauche ich das als Informatiker?" },
  beispiel: { icon: "✏️", label: "Beispiel" },
};

export function renderBloecke(bloecke, { klasse = "" } = {}) {
  const wrap = h("div", { class: "md " + klasse });
  const alt = [];
  for (const b of bloecke || []) {
    if (b && b.typ === "alt") { alt.push(b); continue; }
    try { wrap.append(renderBlock(b)); } catch (e) {
      console.error(e, b);
      wrap.append(h("div", { class: "vis-fehler", text: `Block „${b && b.typ}“ konnte nicht angezeigt werden: ${e.message}` }));
    }
  }
  for (const a of alt) wrap.append(altBereich(a));
  return wrap;
}

export function renderSeiten(seiten, opts) {
  const wrap = h("div", { class: "md-seiten" });
  (seiten || []).forEach((s, i) => {
    if (i > 0) wrap.append(h("hr", { class: "seiten-trenner" }));
    wrap.append(renderBloecke(s, opts));
  });
  return wrap;
}

/** "Ich verstehe das nicht": zweite Erklärung mit anderem Bild. */
function altBereich(b) {
  const inhalt = h("div", { class: "alt-inhalt", hidden: true },
    h("div", { class: "alt-kopf" }, h("span", { class: "alt-icon", "aria-hidden": "true", text: "🔄" }),
      h("div", null, h("span", { class: "box-label", text: "Noch einmal anders erklärt" }), b.titel && b.titel !== "Noch einmal anders erklärt" ? h("span", { class: "box-titel", html: inline(b.titel) }) : null)),
    renderBloecke(b.bloecke || []));
  const knopf = h("button", { class: "btn btn-soft alt-knopf", type: "button", "aria-expanded": "false" },
    h("span", { "aria-hidden": "true", text: "🤔" }), "Ich verstehe das nicht");
  knopf.onclick = () => {
    const offen = inhalt.hidden;
    inhalt.hidden = !offen;
    knopf.setAttribute("aria-expanded", offen ? "true" : "false");
    knopf.lastChild.textContent = offen ? "Andere Erklärung ausblenden" : "Ich verstehe das nicht";
    if (offen) inhalt.scrollIntoView({ behavior: reduziert() ? "auto" : "smooth", block: "nearest" });
  };
  return h("div", { class: "alt-bereich" }, knopf, inhalt);
}

export function renderBlock(b) {
  switch (b.typ) {
    case "ueberschrift": return h("h3", { class: "md-h", html: inline(b.text) });
    case "absatz": return h("p", { html: inline(b.text) });
    case "merke": return h("div", { class: "md-merke" }, h("span", { class: "stern", "aria-hidden": "true", text: "★" }),
      h("div", null, h("span", { class: "merke-label", text: "Merke" }), h("span", { html: inline(b.text) })));
    case "codeblock": return h("pre", { class: "md-pre", text: b.code });
    case "formel": return h("div", { class: "formel-block", html: texHtml(b.tex, true) });
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
          h("div", null, h("span", { class: "box-label", text: BOX[art].label }), titel ? h("span", { class: "box-titel", html: inline(titel) }) : null)),
        renderBloecke(b.bloecke || []));
    }
    case "rechnung": return rechnung(b);
    case "visual": return visual(b.art, b.daten, b.fehler);
    case "vergleich": {
      const [t1, t2] = b.titel || ["", ""];
      const [s1, s2] = b.spalten || [[], []];
      return h("div", { class: "vergleich" },
        h("div", null, h("h4", { html: inline(t1 || "") }), renderBloecke(s1)),
        h("div", null, h("h4", { html: inline(t2 || "") }), renderBloecke(s2)));
    }
    case "alt": return altBereich(b);
    default:
      return h("p", { html: inline(b.text || "") });
  }
}

/** Vorgerechnetes Beispiel: Schritt für Schritt aufbauen, Begründung am Rand. */
export function rechnung(b, { alleZeigen = false } = {}) {
  const schritte = b.schritte || [];
  const liste = h("ol", { class: "rechnung-liste" });
  const zeilen = schritte.map((s, i) => {
    const z = h("li", { class: "rechnung-zeile" + (s.falsch ? " falsch" : ""), hidden: !alleZeigen && i > 0 },
      h("div", { class: "rz-formel", html: texHtml("\\displaystyle " + s.tex, false) }),
      h("div", { class: "rz-grund" }, s.falsch ? h("span", { class: "chip rot", text: "✗ So nicht!" }) : null, h("span", { html: inline(s.grund || "") })));
    liste.append(z);
    return z;
  });
  let n = alleZeigen ? schritte.length : 1;
  const zaehler = h("span", { class: "zaehler" });
  const weiter = h("button", { class: "btn btn-primary btn-sm", type: "button", text: "Nächster Schritt ▶" });
  const alle = h("button", { class: "btn btn-sm btn-ghost", type: "button", text: "Alles zeigen" });
  const neu = h("button", { class: "btn btn-sm btn-ghost", type: "button", text: "↺ Von vorn" });
  const aktualisieren = (animiert = true) => {
    zeilen.forEach((z, i) => {
      const war = !z.hidden;
      z.hidden = i >= n;
      z.classList.toggle("neu", animiert && !war && !z.hidden && !reduziert());
    });
    zaehler.textContent = `Schritt ${n} von ${schritte.length}`;
    weiter.disabled = alle.disabled = n >= schritte.length;
    neu.hidden = n <= 1;
  };
  weiter.onclick = () => { n = Math.min(schritte.length, n + 1); aktualisieren(); };
  alle.onclick = () => { n = schritte.length; aktualisieren(); };
  neu.onclick = () => { n = 1; aktualisieren(false); };
  const box = h("figure", { class: "rechnung" },
    h("figcaption", { class: "rechnung-titel" }, h("span", { "aria-hidden": "true", text: "✏️" }), b.titel ? h("span", { html: inline(b.titel) }) : "Beispiel vorgerechnet"),
    liste);
  if (schritte.length > 1 && !alleZeigen) {
    box.append(h("div", { class: "rechnung-steuer" }, weiter, alle, neu, zaehler));
    box.tabIndex = -1;
  }
  aktualisieren(false);
  return box;
}

/** Erklärungstext einer Antwort: Blöcke (vom Server geparst) oder einfacher Text. */
export function erklaerungElement(bloecke, text) {
  if (Array.isArray(bloecke) && bloecke.length) return renderBloecke(bloecke);
  if (!text) return null;
  return h("div", { class: "md" }, h("p", { html: inline(text) }));
}

/** Rechenweg komplett (alle Schritte direkt sichtbar). */
export function rechenwegElement(bloecke) {
  if (!Array.isArray(bloecke) || !bloecke.length) return null;
  const wrap = h("div", { class: "md" });
  for (const b of bloecke) wrap.append(b.typ === "rechnung" ? rechnung(b, { alleZeigen: true }) : renderBlock(b));
  return wrap;
}
