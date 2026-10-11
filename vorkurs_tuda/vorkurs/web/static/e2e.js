// Automatischer Oberflächentest (End-to-End). Wird NUR mit ?e2e=… geladen und braucht den
// Server im Testmodus (vorkurs_quiz.py --gui --e2e). Ohne diesen Modus gibt es /api/e2e/* nicht.
// Der Test bedient die echte Oberfläche (Klicks, Tasten, Eingaben) und schreibt das Ergebnis
// als JSON in <pre id="e2e-ergebnis"> (auslesbar mit msedge --headless --dump-dom) und an den Server.
//
//   ?e2e=kapitel&slugs=a,b   Kapitel komplett durchspielen (ohne slugs: alle)
//   ?e2e=training            Probeprüfung mit Note, Fehlerkiste, Wiederholen
//   ?e2e=werkzeuge           Spickzettel-Suche, Spielwiese (Ausführen, Trace, Editor), Entwurf, Robustheit
//   ?e2e=neustart            wartet auf einen Server-Neustart und prüft die Fehlermeldung
import { h, inline } from "./util.js";
import { api } from "./api.js";
import { store } from "./store.js";

const pause = (ms) => new Promise(r => setTimeout(r, ms));
const norm = (s) => String(s ?? "").replace(/\s+/g, " ").trim();
const textVon = (markup) => { const d = document.createElement("div"); d.innerHTML = inline(String(markup)); return norm(d.textContent); };

const bericht = { modus: "", start: new Date().toISOString(), fenster: `${innerWidth}x${innerHeight}`, kapitel: [], checks: [], jsFehler: [], fertig: false };
window.addEventListener("error", (e) => bericht.jsFehler.push(`${e.message} @ ${e.filename}:${e.lineno}`));
window.addEventListener("unhandledrejection", (e) => bericht.jsFehler.push("Promise: " + (e.reason && (e.reason.message || e.reason))));
const altError = console.error;
console.error = (...a) => { bericht.jsFehler.push("console.error: " + a.map(x => (x && x.message) || String(x)).join(" ")); altError.apply(console, a); };

let box, pre, statusEl;
function anzeigen() { if (pre) pre.textContent = JSON.stringify(bericht, null, 1); }
function check(name, ok, detail = "") { bericht.checks.push({ name, ok: !!ok, detail: String(detail).slice(0, 400) }); anzeigen(); }

async function warten(fn, ms = 20000, was = "Bedingung") {
  const t0 = performance.now();
  for (;;) {
    let v = null;
    try { v = fn(); } catch { v = null; }
    if (v) return v;
    if (performance.now() - t0 > ms) throw new Error("Zeitüberschreitung beim Warten auf: " + was);
    await pause(40);
  }
}

function taste(el, key, extra = {}) {
  el.dispatchEvent(new KeyboardEvent("keydown", { key, bubbles: true, cancelable: true, ...extra }));
}
function eingeben(el, wert) {
  el.focus();
  el.value = wert;
  el.dispatchEvent(new Event("input", { bubbles: true }));
}

/* ---------------- Layout-Prüfung ---------------- */
function scrollbarerVorfahr(el, bis) {
  for (let p = el.parentElement; p && p !== bis; p = p.parentElement) {
    const o = getComputedStyle(p).overflowX;
    if (o === "auto" || o === "scroll" || o === "hidden") return true;
  }
  return false;
}
function layoutPruefen(wurzel, ort) {
  const probleme = [];
  if (document.documentElement.scrollWidth > innerWidth + 1) probleme.push(`Seite scrollt waagerecht (${document.documentElement.scrollWidth} > ${innerWidth})`);
  if (!wurzel) return probleme;
  wurzel.querySelectorAll(".vis-fehler").forEach(x => probleme.push("Visual-Fehler: " + norm(x.textContent).slice(0, 120)));
  wurzel.querySelectorAll(".visual").forEach(v => { const r = v.getBoundingClientRect(); if (r.height < 12 || !v.textContent.trim() && !v.querySelector("svg, canvas")) probleme.push("leeres Visual: " + (v.className || "")); });
  const karten = wurzel.matches(".karte") ? [wurzel] : [...wurzel.querySelectorAll(".karte")];
  for (const k of karten) {
    const kr = k.getBoundingClientRect();
    let n = 0;
    for (const el of k.querySelectorAll("*")) {
      const r = el.getBoundingClientRect();
      if (!r.width || r.right <= kr.right + 2) continue;
      if (scrollbarerVorfahr(el, k)) continue;
      if (getComputedStyle(el).position === "fixed") continue;
      probleme.push(`Überlauf (${Math.round(r.right - kr.right)} px): <${el.tagName.toLowerCase()} class="${el.className}"> ${norm(el.textContent).slice(0, 60)}`);
      if (++n >= 3) break;
    }
  }
  return probleme.map(p => `${ort}: ${p}`);
}

/* ---------------- Fragen beantworten ---------------- */
async function loesungHolen(id) {
  return (await api.get(`/api/e2e/antwort?id=${encodeURIComponent(id)}`)).antwort;
}

function feedbackEndgueltig(karte, typ) {
  const f = karte.querySelector(".feedback");
  if (!f) return null;
  if (f.classList.contains("ok") || f.classList.contains("nok")) return f;
  if (typ === "code" && f.classList.contains("nochmal")) return f;
  return null;
}

/** Ein Versuch. richtig=false erzeugt eine falsche Antwort. variante steuert Maus/Tastatur. */
async function versuch(karte, antwort, richtig, variante) {
  const typ = karte.dataset.typ;
  const pruefBtn = karte.querySelector(".frage-aktionen .btn-primary");
  const klickOderTaste = (feld, tasteName = "Enter", extra = {}) => { if (variante % 2) taste(feld, tasteName, extra); else pruefBtn.click(); };
  if (typ === "mc") {
    const opts = [...karte.querySelectorAll(".option")];
    const soll = textVon(antwort);
    const i = opts.findIndex(o => !o.disabled && (norm(o.querySelector(".opt-text").textContent) === soll) === richtig);
    if (i < 0) throw new Error("MC: passende Option nicht gefunden: " + soll);
    if (variante % 2) { taste(document.activeElement && document.activeElement !== document.body ? document.activeElement : document.body, String(i + 1)); taste(document.activeElement || document.body, "Enter"); }
    else { opts[i].click(); pruefBtn.click(); }
  } else if (typ === "wf") {
    const wahr = richtig ? !!antwort : !antwort;
    if (variante % 2) taste(document.body, wahr ? "w" : "f");
    else karte.querySelector(wahr ? ".wf-btn.wahr" : ".wf-btn.falsch-btn").click();
  } else if (typ === "text" || typ === "ausdruck") {
    const inp = karte.querySelector("input.feld");
    eingeben(inp, richtig ? String(antwort) : "falsch_xyz_123");
    klickOderTaste(inp);
  } else if (typ === "ausgabe") {
    const ta = karte.querySelector("textarea.feld");
    eingeben(ta, richtig ? String(antwort) : "falsch_xyz_123");
    klickOderTaste(ta, "Enter", { ctrlKey: true });
  } else if (typ === "luecke") {
    const felder = [...karte.querySelectorAll(".luecke-feld")];
    felder.forEach((f, i) => { if (!f.readOnly) eingeben(f, richtig ? antwort[i] : "falsch_xyz"); });
    if (variante % 2) taste(felder[felder.length - 1], "Enter"); else pruefBtn.click();
  } else if (typ === "puzzle") {
    // zurücklegen, was schon im Programm liegt
    karte.querySelectorAll(".ziel .baustein").forEach(b => b.click());
    const ids = richtig ? antwort : antwort.slice(0, 1);
    ids.forEach((id, i) => {
      const b = karte.querySelector(`.quelle .baustein[data-id="${id}"]`);
      if (!b) throw new Error("Puzzle-Baustein fehlt: " + id);
      if ((variante + i) % 2) taste(b, "Enter"); else b.click();
    });
    const imZiel = [...karte.querySelectorAll(".ziel .baustein")];
    if (richtig && imZiel.length >= 2) {      // Sortierknöpfe testen: runter und wieder hoch
      imZiel[0].querySelector('.bs-aktionen button[aria-label="nach unten"]').click();
      const jetzt = [...karte.querySelectorAll(".ziel .baustein")];
      if (jetzt[1] !== imZiel[0]) check("Puzzle: Knopf ↓ verschiebt", false, karte.dataset.id);
      taste(jetzt[1], "ArrowUp", { altKey: true });
      const zurueck = [...karte.querySelectorAll(".ziel .baustein")];
      if (zurueck[0] !== imZiel[0]) check("Puzzle: Alt+↑ verschiebt", false, karte.dataset.id);
    }
    pruefBtn.click();
  } else if (typ === "code") {
    const ta = karte.querySelector(".ed-flaeche textarea");
    eingeben(ta, richtig ? String(antwort) : "print('falsch')\n");
    if (variante % 2) taste(ta, "Enter", { ctrlKey: true });
    else [...karte.querySelectorAll(".code-aufgabe-werkzeuge .btn-primary")][0].click();
  } else throw new Error("unbekannter Fragetyp " + typ);
}

async function beantworten(karte, richtig = true, variante = 0) {
  const typ = karte.dataset.typ, id = karte.dataset.id;
  const antwort = await loesungHolen(id);
  const t0 = performance.now();
  const realStart = Date.now();
  await versuch(karte, antwort, richtig, variante);
  let fb = await warten(() => feedbackEndgueltig(karte, typ) || karte.querySelector(".feedback.nochmal"), 30000, `Rückmeldung ${id}`);
  if (!richtig && fb.classList.contains("nochmal") && typ !== "code") {
    await pause(50);
    await versuch(karte, antwort, false, variante + 1);
    fb = await warten(() => feedbackEndgueltig(karte, typ), 30000, `Rückmeldung 2 ${id}`);
  }
  if (typ === "code" && !fb.classList.contains("ok")) await warten(() => feedbackEndgueltig(karte, typ), 30000, "Code-Rückmeldung");
  const ok = fb.classList.contains("ok");
  return { id, typ, ok, ms: Math.round(performance.now() - t0), real_ms: Date.now() - realStart, meldung: ok ? "" : norm(fb.textContent).slice(0, 300) };
}

/* ---------------- Kapitel ---------------- */
const buehne = () => { const nav = document.querySelector("#main .kap-nav"); return nav ? nav.previousElementSibling : null; };

async function kapitelDurchlauf(slug) {
  const r = { slug, seiten: 0, fragen: 0, richtig: 0, falsch: [], probleme: [], beispiel: null, ergebnis: null, ms: 0 };
  const t0 = Date.now();
  location.hash = `#/kapitel/${slug}`;
  await warten(() => document.querySelector(".kap-kopf h1") && buehne() && buehne().querySelector(".ziele-karte"), 30000, "Kapitel " + slug);
  let beispielGetestet = false;
  for (let schritt = 0; schritt < 500; schritt++) {
    const b = buehne();
    if (b.querySelector(".ergebnis-karte")) break;
    const karte = b.querySelector(".frage-karte");
    if (karte) {
      r.fragen++;
      try {
        const a = await beantworten(karte, true, r.fragen);
        if (a.ok) r.richtig++; else r.falsch.push(a);
        if (a.typ === "code") (r.code_ms = r.code_ms || []).push(a.real_ms);
      } catch (e) { r.falsch.push({ id: karte.dataset.id, typ: karte.dataset.typ, fehler: e.message }); }
      r.probleme.push(...layoutPruefen(karte, `${slug}#${schritt} ${karte.dataset.typ}`));
    } else {
      const k = b.querySelector(".karte");
      if (k && k.matches(".erkl-karte")) r.seiten++;
      await pause(30);
      r.probleme.push(...layoutPruefen(k, `${slug}#${schritt}`));
      if (!beispielGetestet && k) {
        const aus = [...k.querySelectorAll(".beispiel .beispiel-kopf .btn-primary")][0];
        if (aus) {
          beispielGetestet = true;
          const box = aus.closest(".beispiel");
          aus.click();
          try {
            const kons = await warten(() => box.querySelector(".beispiel-fuss .konsole, .beispiel-fuss .fehler-karte"), 20000, "Beispielausgabe");
            r.beispiel = kons.matches(".konsole") ? "ok" : "Fehler: " + norm(kons.textContent);
          } catch (e) { r.beispiel = e.message; }
        }
      }
    }
    const weiter = document.querySelector(".kap-nav .btn-primary");
    if (!weiter || weiter.hidden) break;
    try { await warten(() => !weiter.disabled, 5000, "Weiter-Knopf"); }
    catch { r.probleme.push(`${slug}#${schritt}: Weiter bleibt gesperrt`); document.querySelector(".kap-nav .btn-ghost")?.click(); continue; }
    const vorher = location.hash;
    weiter.click();
    await warten(() => location.hash !== vorher || buehne().querySelector(".ergebnis-karte"), 10000, "nächster Schritt");
  }
  try {
    const erg = await warten(() => buehne().querySelector(".ergebnis-karte"), 10000, "Ergebnis");
    await pause(1500);
    r.ergebnis = { prozent: norm(erg.querySelector(".ergebnis-ring text")?.textContent), zahlen: [...erg.querySelectorAll(".ez b")].map(x => norm(x.textContent)), titel: norm(erg.querySelector("h2")?.textContent) };
    r.probleme.push(...layoutPruefen(erg, `${slug} Ergebnis`));
  } catch (e) { r.probleme.push(e.message); }
  r.ms = Date.now() - t0;
  bericht.kapitel.push(r);
  anzeigen();
}

/* ---------------- Training ---------------- */
async function rundeSpielen(richtigBis, maxFragen = 100) {
  const ergebnisse = [];
  for (let i = 0; i < maxFragen; i++) {
    const karte = await warten(() => document.querySelector("#main .schritt-buehne .frage-karte"), 20000, "Trainingsfrage");
    const a = await beantworten(karte, i < richtigBis, i);
    ergebnisse.push(a);
    const weiter = document.querySelector("#main .kap-nav .btn-primary");
    await warten(() => !weiter.disabled, 5000, "Weiter im Training");
    const letzte = /Auswerten/.test(weiter.textContent);
    weiter.click();
    if (letzte) break;
    await warten(() => document.querySelector("#main .schritt-buehne .frage-karte") !== karte, 10000, "nächste Trainingsfrage");
  }
  await warten(() => document.querySelector("#main .ergebnis-karte"), 15000, "Trainingsergebnis");
  await pause(800);
  return ergebnisse;
}

async function training() {
  // Probeprüfung: 10 Fragen, 7 richtig, 3 falsch -> Note prüfen
  location.hash = "#/training/pruefung";
  const sel = await warten(() => document.querySelector("#main .training-optionen select"), 10000, "Prüfungsstart");
  sel.value = "10";
  document.querySelector("#main .training-intro .btn-primary").click();
  const pr = await rundeSpielen(7, 10);
  const note = norm(document.querySelector("#main .note-gross")?.textContent);
  check("Prüfung: 10 Fragen gespielt", pr.length === 10, pr.length);
  check("Prüfung: 7 richtig / 3 falsch wie geplant", pr.filter(x => x.ok).length === 7, JSON.stringify(pr.map(x => [x.typ, x.ok, x.meldung])));
  check("Prüfung: Note angezeigt", !!note, note);
  bericht.pruefung = { note, zahlen: [...document.querySelectorAll("#main .ez b")].map(x => norm(x.textContent)), fehlerkiste_danach: store.statistik?.fehlerkiste };
  // Fehlerkiste: alle richtig -> leer
  const vorher = store.statistik?.fehlerkiste || 0;
  location.hash = "#/training/fehlerkiste";
  await warten(() => document.querySelector("#main .frage-karte, #main .training-intro"), 15000, "Fehlerkiste");
  if (document.querySelector("#main .frage-karte")) {
    const fk = await rundeSpielen(1000);
    check("Fehlerkiste: Fragen richtig beantwortet", fk.every(x => x.ok), JSON.stringify(fk.map(x => x.meldung)));
    bericht.fehlerkiste = { vorher, gespielt: fk.length, nachher: store.statistik?.fehlerkiste };
    check("Fehlerkiste: nach dem Üben leer", (store.statistik?.fehlerkiste || 0) === 0, `vorher ${vorher}, nachher ${store.statistik?.fehlerkiste}`);
  } else check("Fehlerkiste hatte Fragen", vorher === 0, "leer angezeigt, Statistik " + vorher);
  location.hash = "#/";
  await pause(300);
  location.hash = "#/training/fehlerkiste";
  await warten(() => document.querySelector("#main .training-intro"), 15000, "leere Fehlerkiste");
  check("Fehlerkiste: Leer-Hinweis", /leer/i.test(document.querySelector("#main .training-intro h1")?.textContent || ""), document.querySelector("#main h1")?.textContent);
  // Wiederholen (erst auf die neue Seite warten, sonst sieht man noch die alte Fehlerkisten-Karte)
  document.querySelector("#main").replaceChildren();
  location.hash = "#/training/wiederholen";
  await warten(() => document.title.startsWith("Wiederholen"), 10000, "Wiederholen-Seite");
  await warten(() => document.querySelector("#main .frage-karte, #main .training-intro"), 15000, "Wiederholen");
  if (document.querySelector("#main .frage-karte")) {
    const wd = await rundeSpielen(1000, 15);
    check("Wiederholen: Runde gespielt", wd.length > 0 && wd.every(x => x.ok), `${wd.length} Fragen`);
  } else check("Wiederholen: Fragen vorhanden", false, "nichts zu wiederholen");
}

/* ---------------- Werkzeuge ---------------- */
async function spickzettelTest() {
  location.hash = "#/spickzettel";
  const suche = await warten(() => document.querySelector("#main .such-feld input"), 15000, "Spickzettel");
  check("Spickzettel: Merkzettel je Kapitel", document.querySelectorAll("#main .spick-kapitel").length >= 30, document.querySelectorAll("#main .spick-kapitel").length);
  for (const [q, soll] of [["range", true], ["Slicing", true], ["def", true], ["xyzquatsch", false]]) {
    eingeben(suche, q);
    await pause(400);
    const treffer = document.querySelectorAll("#main mark.treffer").length;
    const leer = !document.querySelector("#main .leer-hinweis").hidden;
    check(`Spickzettel-Suche „${q}“`, soll ? treffer > 0 && !leer : treffer === 0 && leer, `${treffer} Treffer, Leer-Hinweis ${leer}`);
  }
  eingeben(suche, "");
  await pause(300);
  bericht.layout_spick = layoutPruefen(document.querySelector("#main .container"), "Spickzettel");
}

async function spielwieseLauf(code, eingaben = "") {
  const ed = document.querySelector("#main .editor textarea");
  eingeben(ed, code);
  const eg = document.querySelector("#main .eingaben-feld textarea");
  if (eg) eingeben(eg, eingaben);
  const slot = document.querySelector("#main .spielwiese-grid").children[2];
  slot.replaceChildren();
  const t0 = Date.now();
  [...document.querySelectorAll("#main .werkzeugleiste .btn-primary")][0].click();
  const kons = await warten(() => slot.querySelector(".konsole, .fehler-karte"), 30000, "Ausgabe Spielwiese");
  return { text: norm(slot.textContent), ms: Date.now() - t0, kons };
}

async function spielwieseTest() {
  location.hash = "#/spielwiese";
  const ed = await warten(() => document.querySelector("#main .editor textarea"), 10000, "Spielwiese");
  let r = await spielwieseLauf('print("Grüße 🐍✨ – äöüß")\nprint(2 ** 10)');
  check("Spielwiese: Sonderzeichen & Emoji", r.text.includes("Grüße 🐍✨ – äöüß") && r.text.includes("1024"), r.text);
  bericht.zeiten = { ausfuehren_ms: r.ms };
  r = await spielwieseLauf('name = input("Name? ")\nprint("Hallo", name)', "Anna");
  check("Spielwiese: input() mit Eingabe", r.text.includes("Hallo Anna"), r.text);
  r = await spielwieseLauf('name = input("Name? ")\nprint("Hallo", name)', "");
  check("Spielwiese: input() ohne Eingabe -> verständliche Meldung", /EOFError/.test(r.text) && /input/.test(r.text), r.text);
  r = await spielwieseLauf("while True:\n    pass");
  check("Spielwiese: Endlosschleife -> Timeout-Meldung", /zu lange|Endlosschleife|abgebrochen/i.test(r.text), r.text.slice(0, 300));
  bericht.zeiten.endlosschleife_ms = r.ms;
  r = await spielwieseLauf("for i in range(10**7):\n    print('Zeile', i)");
  check("Spielwiese: sehr lange Ausgabe wird gestoppt", /sehr viel ausgegeben|gestoppt|zu lange/i.test(r.text), r.text.slice(-300));
  bericht.zeiten.lange_ausgabe_ms = r.ms;
  check("Spielwiese: lange Ausgabe sprengt das Layout nicht", document.documentElement.scrollWidth <= innerWidth + 1, document.documentElement.scrollWidth);
  r = await spielwieseLauf("x = 1/0");
  check("Spielwiese: Fehler wird erklärt", /ZeroDivisionError/.test(r.text) && r.kons.parentElement.querySelector(".fehler-erklaert"), r.text.slice(0, 200));
  // Trace
  eingeben(ed, "summe = 0\nfor i in range(3):\n    summe += i\nprint(summe)");
  document.querySelector("#main .werkzeugleiste .btn:not(.btn-primary):not(.btn-ghost)").click();
  let tr = await warten(() => document.querySelector("#main .tracer .tr-steuerung, #main .tracer .fehler-karte"), 20000, "Trace");
  const regler = document.querySelector("#main .tracer input[type=range]");
  check("Trace: Schritte vorhanden", regler && +regler.max > 5, regler && regler.max);
  document.querySelector('#main .tracer [aria-label="Zum Ende"]').click();
  await pause(100);
  check("Trace: Endzustand zeigt Ausgabe 3", /3/.test(document.querySelector("#main .tracer .tr-unten .konsole")?.textContent || "") && /Fertig/.test(document.querySelector("#main .tr-erklaerung")?.textContent || ""), document.querySelector("#main .tr-erklaerung")?.textContent);
  eingeben(ed, "x = 0\nfor i in range(100000):\n    x += i\nprint(x)");
  const t0 = Date.now();
  document.querySelector("#main .werkzeugleiste .btn:not(.btn-primary):not(.btn-ghost)").click();
  await warten(() => document.querySelector("#main .tracer .tr-steuerung, #main .tracer .fehler-karte"), 30000, "Trace groß");
  const hinweis = document.querySelector("#main .tracer .tr-hinweis");
  check("Trace: große Schleife -> max_schritte-Hinweis", hinweis && /angehalten/.test(hinweis.textContent), hinweis ? hinweis.textContent : "kein Hinweis");
  bericht.zeiten.trace_gross_ms = Date.now() - t0;
  // Editor-Tasten
  eingeben(ed, "if x > 1:");
  ed.setSelectionRange(ed.value.length, ed.value.length);
  taste(ed, "Enter");
  check("Editor: Enter nach ':' rückt ein", ed.value === "if x > 1:\n    ", JSON.stringify(ed.value));
  ed.value = "print(x)"; ed.dispatchEvent(new Event("input")); ed.setSelectionRange(0, 0);
  taste(ed, "Tab");
  check("Editor: Tab rückt 4 Leerzeichen ein", ed.value === "    print(x)", JSON.stringify(ed.value));
  taste(ed, "Tab", { shiftKey: true });
  check("Editor: Umschalt+Tab rückt aus", ed.value === "print(x)", JSON.stringify(ed.value));
  taste(ed, "/", { ctrlKey: true });
  check("Editor: Strg+/ kommentiert", ed.value === "# print(x)", JSON.stringify(ed.value));
  taste(ed, "/", { ctrlKey: true });
  check("Editor: Strg+/ entkommentiert", ed.value === "print(x)", JSON.stringify(ed.value));
  ed.value = 'print("Strg+Enter")'; ed.dispatchEvent(new Event("input"));
  const slot = document.querySelector("#main .spielwiese-grid").children[2];
  slot.replaceChildren();
  taste(ed, "Enter", { ctrlKey: true });
  const k2 = await warten(() => slot.querySelector(".konsole"), 20000, "Strg+Enter");
  check("Editor: Strg+Enter führt aus", /Strg\+Enter/.test(k2.textContent), k2.textContent);
  bericht.layout_spielwiese = layoutPruefen(document.querySelector("#main .container"), "Spielwiese");
}

async function entwurfTest() {
  // erste Programmieraufgabe des ersten Kapitels: Entwurf schreiben, weg navigieren, zurück
  const kap = (store.uebersicht?.teile || [])[0]?.kapitel?.[0];
  const d = await api.get(`/api/kapitel/${kap.slug}`);
  let idx = 1, ziel = -1;
  for (const el of d.elemente) {
    if (el.typ === "erklaerung") idx += el.seiten.length;
    else if (el.typ === "frage") { if (el.frage.typ === "code" && ziel < 0) ziel = idx; idx++; }
  }
  location.hash = `#/kapitel/${kap.slug}/${ziel}`;
  const ta = await warten(() => document.querySelector("#main .aufgabe-karte .ed-flaeche textarea"), 15000, "Code-Aufgabe");
  const code = "# Entwurf vom E2E-Test 🐍\nprint('Entwurf')\n";
  eingeben(ta, code);
  await warten(() => /gespeichert/.test(document.querySelector("#main .aufgabe-karte .gespeichert")?.textContent || ""), 10000, "Autosave");
  location.hash = "#/";
  await warten(() => document.querySelector("#main .hero"), 10000, "Übersicht");
  location.hash = `#/kapitel/${kap.slug}/${ziel}`;
  const ta2 = await warten(() => document.querySelector("#main .aufgabe-karte .ed-flaeche textarea"), 15000, "Code-Aufgabe 2");
  check("Entwurf bleibt nach Neuladen erhalten", ta2.value === code, JSON.stringify(ta2.value));
  check("Entwurf: Hinweis-Chip", /Entwurf geladen/.test(document.querySelector("#main .aufgabe-karte .frage-kopf").textContent), document.querySelector("#main .aufgabe-karte .frage-kopf").textContent);
}

async function robustTest() {
  try { await api.post("/api/antwort", { id: "gibtsnicht:00000000", antwort: "x" }); check("Unbekannte Frage -> 404", false, "keine Fehlermeldung"); }
  catch (e) { check("Unbekannte Frage -> verständliche Meldung", e.status === 404 && /neu/.test(e.message), e.message); }
  location.hash = "#/kapitel/gibtsnicht";
  const fk = await warten(() => document.querySelector("#main .fehler-karte"), 10000, "Fehlerseite");
  check("Unbekanntes Kapitel -> Fehlerseite statt Absturz", /nicht gefunden/.test(fk.textContent), fk.textContent);
  location.hash = "#/gibtsnicht";
  await warten(() => document.querySelector("#main .leer-hinweis"), 10000, "404-Seite");
  check("Unbekannte Seite -> Hinweis", true);
}

/* ---------------- Server-Neustart ---------------- */
async function neustartTest() {
  location.hash = "#/spielwiese";
  await warten(() => document.querySelector("#main .editor textarea"), 10000, "Spielwiese");
  let r = await spielwieseLauf('print("vorher")');
  check("Neustart: vor dem Neustart läuft alles", r.text.includes("vorher"), r.text);
  const status = async () => { try { await api.get("/api/status"); return true; } catch { return false; } };
  statusEl.textContent = "warte auf Serverende";
  for (let i = 0; i < 600 && (await status()); i++) await pause(100);
  r = await spielwieseLauf('print("waehrenddessen")');
  check("Neustart: Server weg -> verständliche Meldung", /Keine Verbindung/.test(r.text), r.text);
  statusEl.textContent = "warte auf Neustart";
  for (let i = 0; i < 600 && !(await status()); i++) await pause(100);
  r = await spielwieseLauf('print("nachher")');
  check("Neustart: danach geht es ohne Neuladen weiter", r.text.includes("nachher"), r.text);
}

/* ---------------- Start ---------------- */
export async function e2eStarten(params) {
  const modus = params.get("e2e") || "kapitel";
  bericht.modus = modus;
  bericht.lauf = params.get("lauf") || modus;
  statusEl = h("span", { id: "e2e-status", text: "läuft" });
  pre = h("pre", { id: "e2e-ergebnis", style: { maxHeight: "120px", overflow: "auto", margin: 0, fontSize: "10px" } });
  box = h("div", { id: "e2e-box", style: { position: "fixed", right: "6px", bottom: "6px", width: "260px", background: "#fffbe6", color: "#000", border: "1px solid #999", padding: "4px", zIndex: 9999, fontSize: "11px", opacity: .85 } }, h("b", { text: "E2E-Test: " }), statusEl, pre);
  document.body.append(box);
  try {
    await api.get("/api/e2e/antwort?id=x");
  } catch (e) {
    if (e.status === 404 && /Unbekannte Adresse/.test(e.message)) {
      bericht.jsFehler.push("Server läuft nicht mit --e2e");
      statusEl.textContent = "Server ohne --e2e"; bericht.fertig = true; anzeigen(); return;
    }
  }
  try {
    await warten(() => store.uebersicht, 20000, "Übersicht");
    if (modus === "kapitel") {
      const alle = store.uebersicht.teile.flatMap(t => t.kapitel.map(k => k.slug));
      const slugs = (params.get("slugs") || "").split(",").filter(Boolean);
      for (const s of slugs.length ? slugs : alle) {
        statusEl.textContent = "Kapitel " + s;
        try { await kapitelDurchlauf(s); } catch (e) { bericht.kapitel.push({ slug: s, abbruch: e.message }); }
      }
    } else if (modus === "training") await training();
    else if (modus === "werkzeuge") {
      for (const [n, f] of [["spick", spickzettelTest], ["spielwiese", spielwieseTest], ["entwurf", entwurfTest], ["robust", robustTest]]) {
        statusEl.textContent = n;
        try { await f(); } catch (e) { check(`${n}: Abbruch`, false, e.message); }
      }
    } else if (modus === "neustart") await neustartTest();
  } catch (e) {
    check("Abbruch", false, e.message + " " + (e.stack || ""));
  }
  bericht.statistik = store.statistik ? { xp: store.statistik.xp, level: store.statistik.levelName, serie: store.statistik.serie, fehlerkiste: store.statistik.fehlerkiste,
    kapitelFertig: store.statistik.kapitelFertig, abzeichen: store.statistik.abzeichen.filter(a => a.erreicht).map(a => a.id) } : null;
  bericht.kopfzeile = { xp: document.getElementById("xp-zahl")?.textContent, level: document.getElementById("level-name")?.textContent, serie: document.getElementById("serie-zahl")?.textContent };
  bericht.fertig = true;
  bericht.ende = new Date().toISOString();
  statusEl.textContent = "fertig";
  anzeigen();
  try { await api.post("/api/e2e/bericht", bericht); } catch { /* egal */ }
}
