// Ausführbare Beispiele (:::code / :::trace), Konsole, Eingaben-Feld.
import { h, inline, lade, toast } from "./util.js";
import { api } from "./api.js";
import { codeAnzeige } from "./highlight.js";
import { tracerPanel, fehlerInfo, fehlerKarte } from "./tracer.js";

export const brauchtEingabe = (code) => /\binput\s*\(/.test(code || "");

/** Eingaben-Feld für input(): eine Zeile pro Eingabe. */
export function eingabenFeld(vorgabe = [], { sichtbar = true } = {}) {
  const ta = h("textarea", { rows: Math.max(1, Math.min(4, vorgabe.length || 1)), spellcheck: "false", "aria-label": "Eingaben für input(), eine pro Zeile" });
  ta.value = (vorgabe || []).join("\n");
  const el = h("div", { class: "eingaben-feld", hidden: !sichtbar },
    h("label", null, "⌨️ Eingaben für ", h("code", { class: "ic", text: "input()" })),
    ta, h("small", { text: "Jede Zeile wird einer input()-Abfrage übergeben – der Reihe nach." }));
  return { el, werte: () => (ta.value === "" ? [] : ta.value.replace(/\r/g, "").split("\n")), ta };
}

/** Ergebnis von /api/ausfuehren als Konsole + Fehlererklärung. */
export function ausgabeElement(erg) {
  const wrap = h("div", { style: { display: "grid", gap: "10px" } });
  const pre = h("pre");
  const fehler = fehlerInfo(erg);
  if (erg.stdout) pre.append(document.createTextNode(erg.stdout));
  else if (!fehler) pre.append(h("span", { class: "leer", text: "(Das Programm hat nichts ausgegeben.)" }));
  if (fehler) {
    if (erg.stdout && !erg.stdout.endsWith("\n")) pre.append("\n");
    pre.append(h("span", { class: "k-fehler", text: erg.timeout ? "⏱ Abgebrochen: Das Programm lief zu lange (Endlosschleife oder wartet auf Eingaben?)" : `✖ ${fehler.text}${fehler.zeile ? `  (Zeile ${fehler.zeile})` : ""}` }));
  }
  const status = fehler ? "mit Fehler beendet" : "erfolgreich beendet";
  wrap.append(h("div", { class: "konsole", role: "log", "aria-label": "Programmausgabe" },
    h("div", { class: "konsole-kopf" }, h("i"), h("i"), h("i"), "Ausgabe", h("span", { class: "rechts", text: status })), pre));
  if (fehler) {
    wrap.append(fehlerKarte(fehler));
    if (erg.stderr && erg.stderr.trim()) {
      wrap.append(h("details", { style: { fontSize: "13px", color: "var(--text-2)" } },
        h("summary", { text: "Technische Details (Traceback)", style: { cursor: "pointer" } }),
        h("pre", { class: "mono", style: { whiteSpace: "pre-wrap", fontSize: "12.5px", margin: "6px 0 0" }, text: erg.stderr })));
    }
  }
  return wrap;
}

export async function ausfuehren(code, eingaben, ziel) {
  ziel.replaceChildren(lade("Programm läuft …"));
  try {
    const erg = await api.post("/api/ausfuehren", { code, eingaben });
    ziel.replaceChildren(ausgabeElement(erg));
    return erg;
  } catch (e) {
    ziel.replaceChildren(h("div", { class: "fehler-karte", text: e.message }));
    return null;
  }
}

export function oeffneInSpielwiese(code, eingaben = []) {
  try { sessionStorage.setItem("spielwiese_import", JSON.stringify({ code, eingaben })); } catch { /* egal */ }
  location.hash = "#/spielwiese";
}

/** :::code und :::trace */
export function codeBeispiel(block) {
  const code = String(block.code || "").replace(/\s+$/, "");
  const eingabe = eingabenFeld(block.eingaben || [], { sichtbar: brauchtEingabe(code) || (block.eingaben || []).length > 0 });
  const ausgabeSlot = h("div");
  const traceSlot = h("div");
  const fuss = h("div", { class: "beispiel-fuss" }, ausgabeSlot, traceSlot);
  const bAus = h("button", { class: "btn btn-sm btn-primary", type: "button" }, h("span", { class: "ico", text: "▶" }), "Ausführen");
  const bTrace = h("button", { class: "btn btn-sm", type: "button", "aria-expanded": "false" }, h("span", { class: "ico", text: "👣" }), "Schritt für Schritt");
  const bEditor = h("button", { class: "btn btn-sm btn-ghost", type: "button", title: "In der Spielwiese bearbeiten" }, "✎ Im Editor öffnen");
  const box = h("div", { class: "beispiel" },
    h("div", { class: "beispiel-kopf" }, h("span", { class: "titel", text: "🧪 Zum Ausprobieren" }), h("span", { class: "spacer" }), bAus, bTrace, bEditor),
    codeAnzeige(code, { nummern: code.split("\n").length > 3 }), eingabe.el, fuss);

  bAus.onclick = () => ausfuehren(code, eingabe.werte(), ausgabeSlot);
  const traceOeffnen = () => {
    traceSlot.replaceChildren(tracerPanel(code, eingabe.werte(), { onSchliessen: () => { traceSlot.replaceChildren(); bTrace.setAttribute("aria-expanded", "false"); } }));
    bTrace.setAttribute("aria-expanded", "true");
  };
  bTrace.onclick = () => {
    if (traceSlot.firstChild) { traceSlot.replaceChildren(); bTrace.setAttribute("aria-expanded", "false"); }
    else traceOeffnen();
  };
  bEditor.onclick = () => oeffneInSpielwiese(code, eingabe.werte());
  if (block.trace) {
    // Erst laden, wenn sichtbar (spart Prozesse beim Blättern)
    if ("IntersectionObserver" in window) {
      const io = new IntersectionObserver((eintraege) => {
        if (eintraege.some(e => e.isIntersecting)) { io.disconnect(); if (!traceSlot.firstChild) traceOeffnen(); }
      });
      requestAnimationFrame(() => io.observe(box));
    } else traceOeffnen();
  }
  return box;
}

export { toast, inline };
