// Formeln: KaTeX (lokal unter /static/vendor/katex) mit Unicode-Ersatz, falls KaTeX fehlt.
import { esc } from "./util.js";

const MAKROS = {
  "\\hl": "\\htmlClass{hl}{#1}",
  "\\N": "\\mathbb{N}", "\\Z": "\\mathbb{Z}", "\\Q": "\\mathbb{Q}", "\\R": "\\mathbb{R}", "\\C": "\\mathbb{C}",
};
const cache = new Map();

export const katexDa = () => typeof window.katex !== "undefined";

/** LaTeX -> HTML-String (gesetzt mit KaTeX, sonst lesbarer Ersatztext). */
export function texHtml(tex, display = false) {
  const schluessel = (display ? "D" : "I") + tex;
  if (cache.has(schluessel)) return cache.get(schluessel);
  let html;
  if (katexDa()) {
    try {
      html = window.katex.renderToString(String(tex), {
        displayMode: display, throwOnError: false, strict: "ignore", output: "htmlAndMathml",
        macros: { ...MAKROS }, trust: (k) => k.command === "\\htmlClass",
      });
    } catch (e) { html = null; }
  }
  if (!html) html = `<span class="formel-ersatz">${esc(texText(tex))}</span>`;
  if (cache.size > 3000) cache.clear();
  cache.set(schluessel, html);
  return html;
}

/** Formel als Element. */
export function formelEl(tex, display = false) {
  const el = document.createElement(display ? "div" : "span");
  el.className = display ? "formel-block" : "formel";
  el.innerHTML = texHtml(tex, display);
  return el;
}

/** Prüft eine Formel streng (für den E2E-Formeltest). Rückgabe: Fehlertext oder null. */
export function texFehler(tex) {
  if (!katexDa()) return "KaTeX nicht geladen";
  try {
    window.katex.renderToString(String(tex).replace(/\\luecke/g, "\\boxed{\\phantom{00}}"),
      { throwOnError: true, strict: "ignore", macros: { ...MAKROS }, trust: (k) => k.command === "\\htmlClass" });
    return null;
  } catch (e) { return e.message; }
}

/* ---------- LaTeX -> lesbarer Text (Tab-Titel, Tooltips, Ersatz ohne KaTeX) ---------- */
const SYMBOLE = {
  cdot: "·", times: "×", div: "÷", pm: "±", le: "≤", leq: "≤", ge: "≥", geq: "≥", neq: "≠", ne: "≠", approx: "≈",
  infty: "∞", pi: "π", alpha: "α", beta: "β", gamma: "γ", delta: "δ", Delta: "Δ", epsilon: "ε", varepsilon: "ε",
  lambda: "λ", mu: "μ", sigma: "σ", Sigma: "Σ", phi: "φ", varphi: "φ", omega: "ω", theta: "θ", rho: "ρ", tau: "τ",
  in: "∈", notin: "∉", subset: "⊂", subseteq: "⊆", supseteq: "⊇", cup: "∪", cap: "∩", setminus: "∖", emptyset: "∅",
  varnothing: "∅", forall: "∀", exists: "∃", neg: "¬", lnot: "¬", land: "∧", wedge: "∧", lor: "∨", vee: "∨",
  Rightarrow: "⇒", Leftarrow: "⇐", Leftrightarrow: "⇔", rightarrow: "→", to: "→", mapsto: "↦", implies: "⇒",
  iff: "⇔", sum: "Σ", prod: "Π", int: "∫", partial: "∂", ldots: "…", cdots: "⋯", dots: "…", mid: "|", circ: "∘",
  equiv: "≡", oplus: "⊕", perp: "⊥", quad: " ", qquad: "  ", lvert: "|", rvert: "|", vert: "|",
};
const MENGEN = { N: "ℕ", Z: "ℤ", Q: "ℚ", R: "ℝ", C: "ℂ" };
const HOCH = { 0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹", "+": "⁺", "-": "⁻", n: "ⁿ" };
const TIEF = { 0: "₀", 1: "₁", 2: "₂", 3: "₃", 4: "₄", 5: "₅", 6: "₆", 7: "₇", 8: "₈", 9: "₉", n: "ₙ", k: "ₖ", i: "ᵢ" };
const ueber = (s, tab, pre) => ([...s].every(c => tab[c]) ? [...s].map(c => tab[c]).join("") : `${pre}(${s})`);
const kl = (s) => (/^[\w.,]+$/.test(s) ? s : `(${s})`);

export function texText(tex) {
  let s = String(tex);
  s = s.replace(/\\mathbb\{(\w)\}/g, (_, b) => MENGEN[b] || b);
  s = s.replace(/\\(?:text|mathrm|operatorname|mathbf|textbf|hl|boxed)\{([^{}]*)\}/g, "$1");
  for (let i = 0; i < 4; i++) {
    s = s.replace(/\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}/g, (_, a, b) => `${kl(a)}/${kl(b)}`);
    s = s.replace(/\\sqrt\{([^{}]*)\}/g, (_, a) => `√${kl(a)}`);
    s = s.replace(/\^\{([^{}]*)\}/g, (_, a) => ueber(a, HOCH, "^"));
    s = s.replace(/_\{([^{}]*)\}/g, (_, a) => ueber(a, TIEF, "_"));
  }
  s = s.replace(/\^(\w)/g, (_, a) => ueber(a, HOCH, "^")).replace(/_(\w)/g, (_, a) => ueber(a, TIEF, "_"));
  s = s.replace(/\\(left|right|big|Big|displaystyle)/g, "");
  s = s.replace(/\\([A-Za-z]+)/g, (_, n) => SYMBOLE[n] ?? n);
  s = s.replace(/\\\{/g, "{").replace(/\\\}/g, "}").replace(/\\[,; ]/g, " ").replace(/\{,\}/g, ",");
  return s.replace(/[{}]/g, "").replace(/\\\\/g, "; ").replace(/&/g, " ").replace(/\s+/g, " ").trim();
}
