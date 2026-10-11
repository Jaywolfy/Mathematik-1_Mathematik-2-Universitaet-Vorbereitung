// Selbst gebauter Code-Editor: Textarea über Highlight-Layer, Zeilennummern,
// Einrückungshilfe, Kommentar umschalten, Klammern schließen.
import { h } from "./util.js";
import { highlight } from "./highlight.js";

const EINZUG = "    ";
const PAARE = { "(": ")", "[": "]", "{": "}" };
const ZU = new Set([")", "]", "}"]);

export class Editor {
  constructor({ wert = "", onChange = null, onStrgEnter = null, label = "Python-Code-Editor", minZeilen = 8, statuszeile = true, platzhalter = "# Schreibe hier deinen Python-Code …" } = {}) {
    this.onChange = onChange;
    this.onStrgEnter = onStrgEnter;
    this.minZeilen = minZeilen;
    this.tabFrei = false; // nach Escape darf Tab den Fokus verlassen
    this.gutter = h("div", { class: "ed-gutter", "aria-hidden": "true" });
    this.code = h("code");
    this.pre = h("pre", { "aria-hidden": "true" }, this.code);
    this.ta = h("textarea", {
      spellcheck: "false", autocapitalize: "off", autocomplete: "off", autocorrect: "off", wrap: "off",
      "aria-label": label + " (Tab rückt ein; Escape und dann Tab verlässt den Editor)", "aria-multiline": "true", placeholder: platzhalter,
    });
    this.innen = h("div", { class: "ed-innen" }, this.pre, this.ta);
    this.flaeche = h("div", { class: "ed-flaeche" }, this.innen);
    this.status = h("span", { class: "ed-pos", text: "Zeile 1, Spalte 1" });
    this.gespeichert = h("span", { class: "gespeichert" });
    this.el = h("div", { class: "editor" }, this.gutter, this.flaeche,
      statuszeile ? h("div", { class: "ed-statuszeile" }, this.status, this.gespeichert,
        h("span", { class: "ed-hilfe", html: "<kbd>Tab</kbd> einrücken · <kbd>Strg</kbd>+<kbd>/</kbd> Kommentar · <kbd>Strg</kbd>+<kbd>Enter</kbd> prüfen" })) : null);
    this.ta.value = wert;
    this.ta.addEventListener("input", () => this._geaendert());
    this.ta.addEventListener("keydown", (e) => this._taste(e));
    this.ta.addEventListener("keyup", () => this._position());
    this.ta.addEventListener("click", () => this._position());
    this.ta.addEventListener("focus", () => { this.tabFrei = false; });
    this.flaeche.addEventListener("click", (e) => { if (e.target === this.flaeche) this.ta.focus(); });
    this._zeichnen();
  }

  get wert() { return this.ta.value; }
  set wert(v) { this.ta.value = v; this._zeichnen(); }
  fokus() { this.ta.focus(); }
  setzeGespeichert(text) { this.gespeichert.textContent = text; }

  _geaendert() {
    this._zeichnen();
    if (this.onChange) this.onChange(this.ta.value);
  }

  _zeichnen() {
    const text = this.ta.value;
    const zeilen = text.split("\n");
    this.code.innerHTML = highlight(text) + "\n ";
    const n = Math.max(zeilen.length, this.minZeilen);
    if (this.gutter.childElementCount !== n) {
      this.gutter.replaceChildren(...Array.from({ length: n }, (_, i) => h("div", { text: i + 1 })));
    }
    const laengste = zeilen.reduce((m, z) => Math.max(m, z.length), 0);
    const hoehe = `calc(${n} * 1.6em + 24px)`;
    this.pre.style.minHeight = hoehe;
    this.pre.style.width = `calc(${laengste + 2}ch + 32px)`;
    this._position();
  }

  _position() {
    const pos = this.ta.selectionStart;
    const vor = this.ta.value.slice(0, pos);
    const zeile = vor.split("\n").length;
    const spalte = pos - vor.lastIndexOf("\n");
    this.status.textContent = `Zeile ${zeile}, Spalte ${spalte}`;
    [...this.gutter.children].forEach((d, i) => d.classList.toggle("aktiv", i === zeile - 1));
  }

  /** Text an der Auswahl einfügen – über execCommand, damit Strg+Z funktioniert. */
  _einfuegen(text, selStart = null, selEnd = null) {
    const ta = this.ta;
    if (selStart !== null) ta.setSelectionRange(selStart, selEnd ?? selStart);
    let ok = false;
    try { ok = document.execCommand("insertText", false, text); } catch { ok = false; }
    if (!ok) {
      ta.setRangeText(text, ta.selectionStart, ta.selectionEnd, "end");
      this._geaendert();
    }
  }

  _zeilenBereich() {
    const ta = this.ta, v = ta.value;
    const a = v.lastIndexOf("\n", ta.selectionStart - 1) + 1;
    let e = ta.selectionEnd;
    if (e > ta.selectionStart && v[e - 1] === "\n") e--;
    let ende = v.indexOf("\n", e);
    if (ende < 0) ende = v.length;
    return [a, ende];
  }

  _zeilenErsetzen(fn) {
    const ta = this.ta;
    const [a, e] = this._zeilenBereich();
    const alt = ta.value.slice(a, e);
    const neu = alt.split("\n").map(fn).join("\n");
    if (neu === alt) return;
    this._einfuegen(neu, a, e);
    ta.setSelectionRange(a, a + neu.length);
  }

  _taste(e) {
    const ta = this.ta;
    const v = ta.value, s = ta.selectionStart, en = ta.selectionEnd;
    if (e.key === "Escape") { this.tabFrei = true; return; }
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault(); if (this.onStrgEnter) this.onStrgEnter(); return;
    }
    if ((e.ctrlKey || e.metaKey) && (e.key === "/" || e.code === "Slash" || e.key === "#" || e.code === "Digit7" && e.shiftKey)) {
      e.preventDefault();
      const [a, b] = this._zeilenBereich();
      const zeilen = v.slice(a, b).split("\n");
      const alleKommentiert = zeilen.filter(z => z.trim()).every(z => /^\s*#/.test(z));
      this._zeilenErsetzen(z => {
        if (!z.trim()) return z;
        if (alleKommentiert) return z.replace(/^(\s*)# ?/, "$1");
        return z.replace(/^(\s*)/, "$1# ");
      });
      return;
    }
    if (e.key === "Tab" && !e.ctrlKey && !e.altKey) {
      if (this.tabFrei) return; // Fokus verlassen erlaubt
      e.preventDefault();
      if (e.shiftKey) {
        this._zeilenErsetzen(z => z.replace(/^( {1,4}|\t)/, ""));
      } else if (s !== en && v.slice(s, en).includes("\n")) {
        this._zeilenErsetzen(z => (z.length ? EINZUG + z : z));
      } else {
        const spalte = s - (v.lastIndexOf("\n", s - 1) + 1);
        this._einfuegen(" ".repeat(4 - (spalte % 4)));
      }
      return;
    }
    if (e.key === "Enter" && !e.shiftKey && !e.ctrlKey && !e.altKey && !e.isComposing) {
      e.preventDefault();
      const zeilenAnfang = v.lastIndexOf("\n", s - 1) + 1;
      const zeile = v.slice(zeilenAnfang, s);
      let einzug = (zeile.match(/^[ \t]*/) || [""])[0];
      const ohneKommentar = zeile.replace(/#.*$/, "").trimEnd();
      if (ohneKommentar.endsWith(":")) einzug += EINZUG;
      else if (/^\s*(return|break|continue|pass|raise)\b/.test(zeile) && einzug.length >= 4) einzug = einzug.slice(0, -4);
      // Zwischen Klammern: z. B. "(|)" -> neue Zeile eingerückt
      const naechstes = v[en];
      const vorher = v[s - 1];
      if (vorher && PAARE[vorher] && PAARE[vorher] === naechstes) {   // nur zwischen ( ) [ ] { }
        this._einfuegen("\n" + einzug + EINZUG + "\n" + einzug);
        const p = s + 1 + einzug.length + EINZUG.length;
        ta.setSelectionRange(p, p);
        return;
      }
      this._einfuegen("\n" + einzug);
      return;
    }
    if (e.key === "Backspace" && s === en && s > 0) {
      const zeilenAnfang = v.lastIndexOf("\n", s - 1) + 1;
      const vor = v.slice(zeilenAnfang, s);
      if (vor.length && /^ +$/.test(vor)) {
        e.preventDefault();
        const weg = vor.length % 4 === 0 ? 4 : vor.length % 4;
        this._einfuegen("", s - weg, s);
        return;
      }
      if (PAARE[v[s - 1]] && PAARE[v[s - 1]] === v[s]) {
        e.preventDefault();
        this._einfuegen("", s - 1, s + 1);
        return;
      }
    }
    if (PAARE[e.key] && !e.ctrlKey && !e.altKey) {
      const naechstes = v[en] || "";
      if (s !== en) {
        e.preventDefault();
        const inhalt = v.slice(s, en);
        this._einfuegen(e.key + inhalt + PAARE[e.key]);
        ta.setSelectionRange(s + 1, s + 1 + inhalt.length);
        return;
      }
      if (!naechstes || /[\s)\]},:]/.test(naechstes)) {
        e.preventDefault();
        this._einfuegen(e.key + PAARE[e.key]);
        ta.setSelectionRange(s + 1, s + 1);
        return;
      }
    }
    if (ZU.has(e.key) && s === en && v[s] === e.key) {
      e.preventDefault();
      ta.setSelectionRange(s + 1, s + 1);
      return;
    }
    if ((e.key === '"' || e.key === "'") && s === en && v[s] === e.key) {
      // über ein bereits automatisch gesetztes Anführungszeichen springen
      const zeile = v.slice(v.lastIndexOf("\n", s - 1) + 1, s);
      if ((zeile.split(e.key).length - 1) % 2 === 1) { e.preventDefault(); ta.setSelectionRange(s + 1, s + 1); return; }
    }
    if ((e.key === '"' || e.key === "'") && s === en && !e.ctrlKey) {
      const vorher = v[s - 1] || "", naechstes = v[s] || "";
      const zeile = v.slice(v.lastIndexOf("\n", s - 1) + 1, s);
      const imKommentar = zeile.includes("#");
      const ungerade = (zeile.split(e.key).length - 1) % 2 === 1;
      if (!imKommentar && !ungerade && !/\w/.test(vorher) && (!naechstes || /[\s)\]},:]/.test(naechstes))) {
        e.preventDefault();
        this._einfuegen(e.key + e.key);
        ta.setSelectionRange(s + 1, s + 1);
      }
    }
  }
}
