// Darstellung von Python-Werten als Kisten/Fächer (Tracer + Visualisierungen).
import { h } from "./util.js";

export const TYP_LEGENDE = [
  ["int", "int", "ganze Zahl"], ["float", "float", "Kommazahl"], ["str", "str", "Text"], ["bool", "bool", "Wahrheitswert"],
  ["NoneType", "None", "nichts"], ["list", "list", "Liste"], ["tuple", "tuple", "Tupel"], ["dict", "dict", "Wörterbuch"],
];

export function typKlasse(typ) {
  const t = String(typ || "andere");
  if (t === "None" || t === "none") return "t-NoneType";
  if (["int", "float", "str", "bool", "NoneType", "list", "tuple", "dict", "set", "function", "module"].includes(t)) return "t-" + t;
  return "t-andere";
}

export function typAnzeige(typ) {
  return typ === "NoneType" ? "None" : (typ || "?");
}

export function legende() {
  return h("div", { class: "typ-legende", "aria-label": "Farblegende der Datentypen" },
    TYP_LEGENDE.map(([k, n, d]) => h("span", { class: typKlasse(k), title: d }, h("i"), n)));
}

/** WERT aus der Trace-API -> Element */
export function wertElement(w, tiefe = 0) {
  if (w === null || w === undefined) return h("span", { class: "w-prim w-none", text: "None" });
  if (typeof w !== "object") return h("span", { class: "w-prim", text: String(w) });
  const typ = w.typ;
  const repr = w.repr ?? "";
  switch (typ) {
    case "int": return h("span", { class: "w-prim w-num", text: repr });
    case "float": return h("span", { class: "w-prim w-float", text: repr });
    case "str": return h("span", { class: "w-prim w-str", text: repr });
    case "bool": return h("span", { class: "w-prim w-bool", text: repr });
    case "NoneType": return h("span", { class: "w-prim w-none", text: "None" });
    case "function": return h("span", { class: "w-prim w-func", text: "⚙ " + repr.replace(/^<function (\w+).*$/, "$1()") });
    case "list": case "tuple": {
      if (!Array.isArray(w.elemente)) return h("span", { class: "w-prim", text: repr });
      if (!w.elemente.length) return h("span", { class: "w-leer", text: typ === "list" ? "[]  leere Liste" : "()  leeres Tupel" });
      const box = h("span", { class: "w-faecher " + typKlasse(typ) });
      w.elemente.forEach((el, i) => box.append(h("span", { class: "w-fach" },
        h("span", { class: "w-idx", text: i }), h("span", { class: "w-inhalt" }, wertElement(el, tiefe + 1)))));
      if (w.gekuerzt || (w.laenge && w.laenge > w.elemente.length)) box.append(h("span", { class: "w-fach" }, h("span", { class: "w-idx", text: "…" }), h("span", { class: "w-inhalt", text: "…" })));
      return h("span", { class: "w-verschachtelt" }, box);
    }
    case "dict": {
      if (!Array.isArray(w.paare)) return h("span", { class: "w-prim", text: repr });
      if (!w.paare.length) return h("span", { class: "w-leer", text: "{}  leeres Wörterbuch" });
      const t = h("table", { class: "w-dict t-dict" });
      w.paare.forEach(([k, v]) => t.append(h("tr", null,
        h("td", { class: "k" }, wertElement(k, tiefe + 1)), h("td", { class: "p", text: "→" }), h("td", null, wertElement(v, tiefe + 1)))));
      return h("span", { class: "w-verschachtelt" }, t);
    }
    case "set": {
      if (!Array.isArray(w.elemente)) return h("span", { class: "w-prim", text: repr });
      if (!w.elemente.length) return h("span", { class: "w-leer", text: "set()  leere Menge" });
      return h("span", { class: "w-set t-set" }, w.elemente.map(el => h("span", { class: "el" }, wertElement(el, tiefe + 1))));
    }
    default: return h("span", { class: "w-prim", text: repr });
  }
}

/** Beschriftete Kiste: Name oben, Wert innen, Typ klein. */
export function varKiste(name, wertEl, typ, { klasse = "", alias = null, titel = null } = {}) {
  const k = h("div", { class: `var-kiste ${typKlasse(typ)} ${klasse}`, title: titel || undefined },
    h("div", { class: "vk-name" }, h("span", { text: name }), h("span", { class: "vk-typ", text: typAnzeige(typ) })),
    h("div", { class: "vk-wert" }, wertEl));
  if (alias) {
    k.dataset.alias = alias.marke;
    k.style.setProperty("--ac", alias.farbe);
    k.querySelector(".vk-name").append(h("span", { class: "alias-marke", title: "zeigt auf dasselbe Objekt", text: "🔗 " + alias.marke }));
    if (alias.text) k.append(h("div", { class: "alias-hinweis", text: alias.text }));
  }
  return k;
}

/** JSON-Wert (aus Visual-Daten) im Python-Stil anzeigen. */
export function pyRepr(v) {
  if (v === null || v === undefined) return "None";
  if (v === true) return "True";
  if (v === false) return "False";
  if (typeof v === "string") return "'" + v.replace(/\\/g, "\\\\").replace(/'/g, "\\'") + "'";
  if (Array.isArray(v)) return "[" + v.map(pyRepr).join(", ") + "]";
  if (typeof v === "object") return "{" + Object.entries(v).map(([k, x]) => pyRepr(k) + ": " + pyRepr(x)).join(", ") + "}";
  return String(v);
}

export function jsTyp(v) {
  if (v === null || v === undefined) return "NoneType";
  if (typeof v === "boolean") return "bool";
  if (typeof v === "number") return Number.isInteger(v) ? "int" : "float";
  if (typeof v === "string") return "str";
  if (Array.isArray(v)) return "list";
  return "dict";
}

/** JSON-Wert -> WERT-Struktur wie aus der Trace-API. */
export function jsonZuWert(v) {
  const typ = jsTyp(v);
  const w = { typ, repr: pyRepr(v) };
  if (typ === "list") w.elemente = v.map(jsonZuWert);
  if (typ === "dict") w.paare = Object.entries(v).map(([k, x]) => [jsonZuWert(k), jsonZuWert(x)]);
  return w;
}

/** Typ eines Python-Literals (als Text) grob bestimmen – Ersatz, falls der Server nicht hilft. */
export function literalTyp(s) {
  const t = String(s).trim();
  if (/^(True|False)$/.test(t)) return "bool";
  if (t === "None") return "NoneType";
  if (/^[-+]?\d[\d_]*$/.test(t)) return "int";
  if (/^[-+]?(\d[\d_]*\.\d*|\.\d+|\d+(\.\d*)?[eE][-+]?\d+)$/.test(t)) return "float";
  if (/^[rbfu]*(['"]).*\1$/is.test(t)) return "str";
  if (/^\[.*\]$/s.test(t)) return "list";
  if (/^\(.*\)$/s.test(t)) return /,/.test(t) || t === "()" ? "tuple" : "andere";
  if (/^\{\s*\}$/.test(t) || /^\{.*:.*\}$/s.test(t)) return "dict";
  if (/^\{.*\}$/s.test(t)) return "set";
  return "andere";
}

export const ALIAS_FARBEN = ["#6366f1", "#db2777", "#0d9488", "#d97706", "#7c3aed", "#0284c7"];
