// Kleiner Python-Tokenizer + Syntax-Highlighting (ohne externe Bibliotheken).
import { esc, h, kopieren, toast } from "./util.js";

const KEYWORDS = new Set(("and as assert async await break class continue def del elif else except finally for " +
  "from global if import in is lambda nonlocal not or pass raise return try while with yield match case").split(" "));
const KONSTANTEN = new Set(["True", "False", "None"]);
const BUILTINS = new Set(("print input len range int float str bool list dict tuple set type abs min max sum sorted " +
  "reversed enumerate zip round isinstance map filter open any all chr ord help id repr divmod pow format iter next " +
  "super object Exception ValueError TypeError IndexError KeyError ZeroDivisionError NameError RecursionError " +
  "AttributeError StopIteration hash hex bin oct frozenset").split(" "));

const RE_NUM = /^(?:0[xX][\da-fA-F_]+|0[bB][01_]+|0[oO][0-7_]+|(?:\d[\d_]*\.?[\d_]*|\.\d[\d_]*)(?:[eE][+-]?\d+)?[jJ]?)/;
const RE_NAME = /^[A-Za-z_À-￿][\wÀ-￿]*/;
const RE_OP = /^(?:\*\*=?|\/\/=?|==|!=|<=|>=|->|:=|<<=?|>>=?|[+\-*/%<>=!&|^~@]=?)/;
const RE_STR_START = /^([rRbBuUfF]{0,2})('''|"""|'|")/;

/** Zerlegt Python-Quelltext in Tokens {t, v}. Verliert kein Zeichen. */
export function tokenize(src) {
  const out = [];
  const n = src.length;
  let i = 0;
  let vorher = null; // letztes bedeutsames Token
  const push = (t, v) => { out.push({ t, v }); if (t !== "ws" && t !== "nl") vorher = { t, v }; };
  while (i < n) {
    const c = src[i];
    if (c === "\n") { push("nl", c); i++; continue; }
    if (c === " " || c === "\t" || c === "\r") {
      let j = i; while (j < n && (src[j] === " " || src[j] === "\t" || src[j] === "\r")) j++;
      push("ws", src.slice(i, j)); i = j; continue;
    }
    if (c === "#") {
      let j = src.indexOf("\n", i); if (j < 0) j = n;
      push("com", src.slice(i, j)); i = j; continue;
    }
    const rest = src.slice(i, i + 6);
    const ms = RE_STR_START.exec(rest);
    if (ms && /^(|r|b|u|f|rb|br|fr|rf)$/i.test(ms[1])) {
      const praefix = ms[1], q = ms[2];
      let j = i + praefix.length + q.length;
      let ende = -1;
      while (j < n) {
        if (src[j] === "\\") { j += 2; continue; }
        if (src.startsWith(q, j)) { ende = j + q.length; break; }
        if (q.length === 1 && src[j] === "\n") { ende = j; break; }
        j++;
      }
      if (ende < 0) ende = n;
      const ganz = src.slice(i, ende);
      if (/f/i.test(praefix)) fString(ganz, praefix.length + q.length, q.length, push);
      else push("str", ganz);
      i = ende; continue;
    }
    if (/[0-9]/.test(c) || (c === "." && /[0-9]/.test(src[i + 1] || ""))) {
      const m = RE_NUM.exec(src.slice(i));
      if (m) { push("num", m[0]); i += m[0].length; continue; }
    }
    const mn = RE_NAME.exec(src.slice(i, i + 80));
    if (mn) {
      const w = mn[0];
      let typ = "name";
      if (KONSTANTEN.has(w)) typ = "const";
      else if (KEYWORDS.has(w)) typ = "kw";
      else if (vorher && vorher.t === "kw" && (vorher.v === "def" || vorher.v === "class")) typ = "fn";
      else if (w === "self") typ = "self";
      else if (vorher && vorher.v === ".") typ = naechstesZeichen(src, i + w.length) === "(" ? "call" : "name";
      else if (BUILTINS.has(w)) typ = "bi";
      else if (naechstesZeichen(src, i + w.length) === "(") typ = "call";
      push(typ, w); i += w.length; continue;
    }
    const mo = RE_OP.exec(src.slice(i, i + 3));
    if (mo) { push("op", mo[0]); i += mo[0].length; continue; }
    push("punc", c); i++;
  }
  return out;
}

function naechstesZeichen(src, i) {
  while (i < src.length && (src[i] === " " || src[i] === "\t")) i++;
  return src[i];
}

function fString(ganz, kopfLaenge, qLaenge, push) {
  const ende = ganz.length - (ganz.length >= kopfLaenge + qLaenge ? qLaenge : 0);
  let puffer = ganz.slice(0, kopfLaenge);
  let i = kopfLaenge;
  while (i < ende) {
    const c = ganz[i];
    if (c === "{" && ganz[i + 1] === "{") { puffer += "{{"; i += 2; continue; }
    if (c === "}" && ganz[i + 1] === "}") { puffer += "}}"; i += 2; continue; }
    if (c === "{") {
      let tiefe = 1, j = i + 1;
      while (j < ende && tiefe > 0) { if (ganz[j] === "{") tiefe++; else if (ganz[j] === "}") tiefe--; if (tiefe > 0) j++; }
      if (puffer) { push("str", puffer); puffer = ""; }
      push("fbr", "{");
      const innen = ganz.slice(i + 1, j);
      // Formatangabe nach ":" (z. B. {x:.2f}) als String zeigen
      const doppel = innen.search(/:(?![=])/);
      const ausdruck = doppel >= 0 && !innen.slice(0, doppel).includes("[") ? innen.slice(0, doppel) : innen;
      for (const t of tokenize(ausdruck)) push(t.t, t.v);
      if (ausdruck.length < innen.length) push("str", innen.slice(ausdruck.length));
      if (j < ende) push("fbr", "}");
      i = j + 1;
      continue;
    }
    puffer += c; i++;
  }
  puffer += ganz.slice(ende);
  if (puffer) push("str", puffer);
}

function tokenHtml(t) {
  if (t.t === "ws" || t.t === "nl" || t.t === "punc" || t.t === "name") return esc(t.v);
  return `<span class="sx-${t.t}">${esc(t.v)}</span>`;
}

/** Ganzer Code -> HTML-String mit Highlighting. */
export function highlight(code) {
  return tokenize(String(code ?? "")).map(tokenHtml).join("");
}

/** Code -> Liste von HTML-Strings, eine pro Zeile (Strings über mehrere Zeilen korrekt). */
export function highlightZeilen(code) {
  const zeilen = [""];
  for (const t of tokenize(String(code ?? ""))) {
    if (t.t === "nl") { zeilen.push(""); continue; }
    const stuecke = t.v.split("\n");
    stuecke.forEach((s, k) => {
      if (k > 0) zeilen.push("");
      if (s) zeilen[zeilen.length - 1] += tokenHtml({ t: t.t, v: s });
    });
  }
  return zeilen;
}

/** Fertiger Codeblock (nur anzeigen) mit Kopier-Button. */
export function codeAnzeige(code, { nummern = false, kopierbar = true, klasse = "" } = {}) {
  const text = String(code ?? "").replace(/\s+$/, "");
  const pre = h("pre", { tabindex: "0", "aria-label": "Python-Code" });
  const c = h("code");
  highlightZeilen(text).forEach((z, i) => {
    c.append(h("span", { class: "code-zeile", "data-nr": i + 1, html: z || " " }));
  });
  pre.append(c);
  const box = h("div", { class: "code-block " + (nummern ? "mit-nr " : "") + klasse }, pre);
  if (kopierbar) {
    box.append(h("button", {
      class: "kopier-btn", type: "button", text: "Kopieren", "aria-label": "Code kopieren",
      onclick: async (e) => {
        await kopieren(text).catch(() => {});
        e.target.textContent = "✓ Kopiert";
        setTimeout(() => { e.target.textContent = "Kopieren"; }, 1400);
      },
    }));
  }
  return box;
}

export { toast };
