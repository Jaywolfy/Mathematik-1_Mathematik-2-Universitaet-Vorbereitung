// Automatischer Oberflächentest (End-to-End). Wird NUR mit ?e2e=… geladen und braucht den
// Server im Testmodus (mathe_quiz.py --gui --e2e). Ohne diesen Modus gibt es /api/e2e/* nicht.
// Ergebnis als JSON in <pre id="e2e-ergebnis"> (auslesbar mit chrome-headless-shell --dump-dom).
//
//   ?e2e=kapitel&slugs=a,b   Kapitel komplett durchspielen (ohne slugs: alle); jede 3. Frage erst falsch
//   ?e2e=training            Wiederholen, Fehlerkiste, Klausur, Endlos-Üben, Diagnose
//   ?e2e=werkzeuge           Formelsammlung, Glossar, Spielwiese, Vorschau, Robustheit
//   ?e2e=formeln             alle Formeln aller Inhalte streng mit KaTeX rendern
import { h } from "./util.js";
import { api } from "./api.js";
import { store } from "./store.js";
import { texFehler } from "./formel.js";

const pause = (ms) => new Promise(r => setTimeout(r, ms));
const norm = (s) => String(s ?? "").replace(/\s+/g, " ").trim();
const bericht = { modus: "", start: new Date().toISOString(), fenster: `${innerWidth}x${innerHeight}`, kapitel: [], checks: [], jsFehler: [], fertig: false };
window.addEventListener("error", (e) => bericht.jsFehler.push(`${e.message} @ ${e.filename}:${e.lineno}`));
window.addEventListener("unhandledrejection", (e) => bericht.jsFehler.push("Promise: " + (e.reason && (e.reason.message || e.reason))));
const altError = console.error;
console.error = (...a) => { bericht.jsFehler.push("console.error: " + a.map(x => (x && x.message) || String(x)).join(" ")); altError.apply(console, a); };

let pre, statusEl;
const anzeigen = () => { if (pre) pre.textContent = JSON.stringify(bericht, null, 1); };
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
const taste = (el, key, extra = {}) => el.dispatchEvent(new KeyboardEvent("keydown", { key, bubbles: true, cancelable: true, ...extra }));
function eingeben(el, wert) { el.focus(); el.value = wert; el.dispatchEvent(new Event("input", { bubbles: true })); }

/* ---------------- Layout ---------------- */
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
  wurzel.querySelectorAll(".vis-fehler").forEach(x => probleme.push("Visual-Fehler: " + norm(x.textContent).slice(0, 160)));
  wurzel.querySelectorAll(".katex-error, .formel-ersatz").forEach(x => probleme.push("Formel nicht gesetzt: " + norm(x.textContent).slice(0, 80)));
  const karten = wurzel.matches(".karte") ? [wurzel] : [...wurzel.querySelectorAll(".karte")];
  for (const k of karten) {
    const kr = k.getBoundingClientRect();
    let n = 0;
    for (const el of k.querySelectorAll("*")) {
      const r = el.getBoundingClientRect();
      if (!r.width || r.right <= kr.right + 2 || scrollbarerVorfahr(el, k) || getComputedStyle(el).position === "fixed") continue;
      if (el.closest(".plot-etiketten")) continue;
      probleme.push(`Überlauf (${Math.round(r.right - kr.right)} px): <${el.tagName.toLowerCase()} class="${el.className?.baseVal ?? el.className}"> ${norm(el.textContent).slice(0, 60)}`);
      if (++n >= 3) break;
    }
  }
  return probleme.map(p => `${ort}: ${p}`);
}

/* ---------------- Antworten ---------------- */
async function loesungHolen(karte, schritt = 0) {
  const seed = karte.dataset.seed ? `&seed=${karte.dataset.seed}` : "";
  return (await api.get(`/api/e2e/antwort?id=${encodeURIComponent(karte.dataset.id)}${seed}&schritt=${schritt}`)).antwort;
}
const FALSCH = "1234567";

function feedbackEndgueltig(bereich) {
  const f = [...bereich.querySelectorAll(":scope > .feedback, :scope > div > .feedback")].pop();
  if (!f) return null;
  return f.classList.contains("ok") || f.classList.contains("loesung") ? f : null;
}

/** Füllt die Eingabe einer (Teil-)Karte und löst Prüfen aus. */
async function versuch(karte, typ, antwort, richtig, variante, prueferKnopf) {
  const klickOderEnter = (feld) => { if (variante % 2 && feld) taste(feld, "Enter"); else prueferKnopf.click(); };
  if (typ === "mc") {
    const opts = [...karte.querySelectorAll(".optionen .option")];
    const soll = norm(antwort.replace(/\$/g, ""));
    // Optionstext vergleichen: annotation (LaTeX) oder Textinhalt
    const text = (o) => norm(([...o.querySelectorAll("annotation")].map(a => a.textContent).join("") || o.textContent));
    let i = opts.findIndex(o => !o.disabled && (norm(o.querySelector(".opt-text").innerHTML) === norm(window.__inline(antwort))) === richtig);
    if (i < 0) i = opts.findIndex(o => !o.disabled && (text(o).includes(soll)) === richtig);
    if (i < 0) throw new Error("MC: Option nicht gefunden: " + antwort);
    if (variante % 2) { taste(document.body, String(i + 1)); taste(document.body, "Enter"); }
    else { opts[i].click(); prueferKnopf.click(); }
  } else if (typ === "wf") {
    const wahr = richtig ? !!antwort : !antwort;
    if (variante % 2) taste(document.body, wahr ? "w" : "f");
    else karte.querySelector(wahr ? ".wf-btn.wahr" : ".wf-btn.falsch-btn").click();
  } else if (["text", "zahl", "term", "loesungsmenge", "menge"].includes(typ) || (typ === "graph_punkt" && !Array.isArray(antwort))) {
    const inp = karte.querySelector("input.feld");
    eingeben(inp, richtig ? String(antwort) : FALSCH);
    klickOderEnter(inp);
  } else if (typ === "vektor" || typ === "matrix") {
    const felder = [...karte.querySelectorAll("input.zelle")];
    const werte = Array.isArray(antwort[0]) ? antwort.flat() : antwort;
    felder.forEach((f, i) => eingeben(f, richtig ? werte[i] : FALSCH));
    prueferKnopf.click();
  } else if (typ === "lgs") {
    const felder = [...karte.querySelectorAll("input.zelle")];
    const cb = karte.querySelector(".lgs-eingabe input[type=checkbox]");
    if (richtig && antwort.keine) { cb.checked = true; cb.dispatchEvent(new Event("change")); }
    else { if (cb.checked) { cb.checked = false; cb.dispatchEvent(new Event("change")); } felder.forEach((f, i) => eingeben(f, richtig ? antwort.werte[i] : FALSCH)); }
    prueferKnopf.click();
  } else if (typ === "mehrfach") {
    const opts = [...karte.querySelectorAll(".option.mehrfach")];
    const html = antwort.map(a => norm(window.__inline(a)));
    opts.forEach(o => { const soll = html.includes(norm(o.querySelector(".opt-text").innerHTML)); if (soll === richtig && !o.classList.contains("gewaehlt")) o.click(); if (soll !== richtig && o.classList.contains("gewaehlt")) o.click(); });
    prueferKnopf.click();
  } else if (typ === "zuordnen") {
    const sel = [...karte.querySelectorAll("select.zuordnen-wahl")];
    sel.forEach((s, i) => { s.value = richtig ? antwort[i][1] : s.options[s.options.length - 1 - (i % 2)].value; s.dispatchEvent(new Event("change")); });
    if (!richtig && sel.every((s, i) => s.value === antwort[i][1])) sel[0].value = sel[1].value;
    prueferKnopf.click();
  } else if (typ === "ordnen") {
    karte.querySelectorAll(".ziel .baustein").forEach(b => b.click());
    const ids = richtig ? antwort : [...antwort].reverse();
    ids.forEach((id, i) => { const b = karte.querySelector(`.quelle .baustein[data-id="${id}"]`); if ((variante + i) % 2) taste(b, "Enter"); else b.click(); });
    prueferKnopf.click();
  } else if (typ === "luecke") {
    const felder = [...karte.querySelectorAll(".luecken-liste input.feld")];
    felder.forEach((f, i) => eingeben(f, richtig ? antwort[i] : FALSCH));
    prueferKnopf.click();
  } else if (typ === "graph_punkt") {
    const zahl = (t) => { const [p, q] = String(t).split("/"); return q === undefined ? Number(p) : Number(p) / Number(q); };
    karte._punktSetzen(richtig ? antwort.map(zahl) : [zahl(antwort[1]) + 3, zahl(antwort[0]) - 3]);
    prueferKnopf.click();
  } else throw new Error("unbekannter Fragetyp " + typ);
}

async function beantworten(karte, richtig = true, variante = 0) {
  const typ = karte.dataset.typ, id = karte.dataset.id;
  const t0 = performance.now();
  if (typ === "papier") {
    karte.querySelector(".frage-aktionen .btn-primary").click();
    await warten(() => karte.querySelector(".check-zeile"), 10000, "Musterlösung");
    karte.querySelectorAll(".check-zeile").forEach((z, i) => z.querySelectorAll("button")[richtig || i ? 0 : 1].click());
    [...karte.querySelectorAll(".frage-aktionen .btn-primary")].pop().click();
    const fb = await warten(() => karte.querySelector(".checkliste ~ div .feedback, .feedback"), 10000, "Papier-Feedback");
    return { id, typ, ok: fb.classList.contains("ok"), ms: Math.round(performance.now() - t0) };
  }
  if (typ === "rechenweg") {
    let n = 0;
    for (;;) {
      const schritt = [...karte.querySelectorAll(".teilschritt.aktiv")].pop();
      if (!schritt) break;
      const stTyp = schritt.querySelector(".optionen") ? "mc" : schritt.querySelector("input.zelle") ? "vektor" : schritt.querySelector(".luecken-liste") ? "luecke" : "zahl";
      const antwort = await loesungHolen(karte, n);
      const knopf = schritt.querySelector(".frage-aktionen .btn-primary");
      await versuch(schritt, stTyp, antwort, richtig || n > 0, variante, knopf);
      await warten(() => !schritt.classList.contains("aktiv") || schritt.querySelector(".feedback.nochmal"), 15000, "Schritt " + n);
      if (schritt.classList.contains("aktiv")) { await versuch(schritt, stTyp, antwort, true, variante, knopf); await warten(() => !schritt.classList.contains("aktiv"), 15000, "Schritt 2"); }
      n++;
      if (n > 6) break;
    }
    const fb = await warten(() => karte.querySelector(":scope > div > .feedback"), 15000, "Rechenweg-Ende");
    return { id, typ, ok: fb.classList.contains("ok"), ms: Math.round(performance.now() - t0) };
  }
  const antwort = await loesungHolen(karte);
  const knopf = karte.querySelector(".frage-aktionen .btn-primary");
  const fbOrt = karte;
  await versuch(karte, typ, antwort, richtig, variante, knopf);
  let fb = await warten(() => feedbackEndgueltig(fbOrt) || fbOrt.querySelector(".feedback.nochmal, .feedback.lesen"), 20000, `Rückmeldung ${id}`);
  if (fb.classList.contains("lesen")) return { id, typ, ok: false, meldung: "Lesefehler: " + norm(fb.textContent).slice(0, 200) };
  if (fb.classList.contains("nochmal")) {
    const hinweis = norm(fb.textContent);
    await pause(30);
    await versuch(karte, typ, antwort, true, variante + 1, knopf);
    fb = await warten(() => feedbackEndgueltig(fbOrt), 20000, `Rückmeldung 2 ${id}`);
    if (fb.classList.contains("ok") && !richtig) return { id, typ, ok: true, zweiter: true, hinweis };
  }
  return { id, typ, ok: fb.classList.contains("ok"), ms: Math.round(performance.now() - t0), meldung: fb.classList.contains("ok") ? "" : norm(fb.textContent).slice(0, 300) };
}

/* ---------------- Kapitel ---------------- */
const buehne = () => { const nav = document.querySelector("#main .kap-nav"); return nav ? nav.previousElementSibling : null; };

async function kapitelDurchlauf(slug) {
  const r = { slug, seiten: 0, fragen: 0, richtig: 0, falsch: [], probleme: [], alt: 0, rechnungen: 0, ergebnis: null, ms: 0 };
  const t0 = Date.now();
  location.hash = `#/kapitel/${slug}`;
  await warten(() => document.querySelector(".kap-kopf h1") && buehne() && buehne().querySelector(".ziele-karte"), 30000, "Kapitel " + slug);
  for (let schritt = 0; schritt < 500; schritt++) {
    const b = buehne();
    if (b.querySelector(".ergebnis-karte")) break;
    const karte = b.querySelector(".frage-karte");
    if (karte) {
      r.fragen++;
      try {
        const erstFalsch = r.fragen % 3 === 0 && !["wf", "papier", "rechenweg", "ordnen"].includes(karte.dataset.typ);
        const a = await beantworten(karte, !erstFalsch, r.fragen);
        if (a.ok) r.richtig++; else r.falsch.push(a);
      } catch (e) { r.falsch.push({ id: karte.dataset.id, typ: karte.dataset.typ, fehler: e.message }); }
      r.probleme.push(...layoutPruefen(karte, `${slug}#${schritt} ${karte.dataset.typ}`));
    } else {
      const k = b.querySelector(".karte");
      if (k && k.matches(".erkl-karte")) r.seiten++;
      await warten(() => !b.querySelector("[data-laedt]"), 8000, "Visuals");
      r.probleme.push(...layoutPruefen(k, `${slug}#${schritt}`));
      // Interaktion: "Ich verstehe das nicht" und "Nächster Schritt"
      const alt = k && k.querySelector(".alt-knopf");
      if (alt) { alt.click(); r.alt++; if (k.querySelector(".alt-inhalt").hidden) r.probleme.push(`${slug}#${schritt}: Alternative öffnet nicht`); }
      for (const rech of k ? k.querySelectorAll(".rechnung") : []) {
        r.rechnungen++;
        const weiter = rech.querySelector(".rechnung-steuer .btn-primary");
        let n = 0;
        while (weiter && !weiter.disabled && n++ < 30) weiter.click();
        if (rech.querySelector(".rechnung-zeile[hidden]")) r.probleme.push(`${slug}#${schritt}: Rechnung nicht vollständig aufgedeckt`);
      }
    }
    const weiter = document.querySelector(".kap-nav .btn-primary");
    if (!weiter || weiter.hidden) break;
    try { await warten(() => !weiter.disabled, 5000, "Weiter-Knopf"); }
    catch { r.probleme.push(`${slug}#${schritt}: Weiter bleibt gesperrt`); document.querySelector(".kap-nav .btn-ghost")?.click(); continue; }
    const vorher = location.hash;
    if (schritt % 4 === 1) taste(document.body, "Enter", { ctrlKey: true }); else weiter.click();
    await warten(() => location.hash !== vorher || buehne().querySelector(".ergebnis-karte"), 10000, "nächster Schritt");
  }
  try {
    const erg = await warten(() => buehne().querySelector(".ergebnis-karte"), 10000, "Ergebnis");
    await pause(1200);
    r.ergebnis = { zahlen: [...erg.querySelectorAll(".ez b")].map(x => norm(x.textContent)), titel: norm(erg.querySelector("h2")?.textContent) };
    r.probleme.push(...layoutPruefen(erg, `${slug} Ergebnis`));
  } catch (e) { r.probleme.push(e.message); }
  r.ms = Date.now() - t0;
  bericht.kapitel.push(r);
  anzeigen();
}

/* ---------------- Training ---------------- */
async function rundeSpielen(richtigBis, maxFragen = 100) {
  const erg = [];
  for (let i = 0; i < maxFragen; i++) {
    const karte = await warten(() => document.querySelector("#main .schritt-buehne .frage-karte"), 20000, "Trainingsfrage");
    const a = await beantworten(karte, i < richtigBis, i);
    erg.push(a);
    const weiter = document.querySelector("#main .kap-nav .btn-primary");
    await warten(() => !weiter.disabled || document.querySelector("#main .ergebnis-karte"), 8000, "Weiter im Training");
    if (document.querySelector("#main .ergebnis-karte")) break;
    const letzte = /Auswerten/.test(weiter.textContent);
    weiter.click();
    if (letzte) break;
    await warten(() => document.querySelector("#main .ergebnis-karte") || document.querySelector("#main .schritt-buehne .frage-karte") !== karte, 10000, "nächste Trainingsfrage");
    if (document.querySelector("#main .ergebnis-karte")) break;
  }
  if (!document.querySelector("#main .ergebnis-karte")) document.querySelector("#main .runde-kopf .btn-ghost")?.click();
  await warten(() => document.querySelector("#main .ergebnis-karte"), 15000, "Trainingsergebnis");
  await pause(600);
  return erg;
}

async function training() {
  location.hash = "#/training/wiederholen";
  await warten(() => document.querySelector("#main .frage-karte, #main .training-intro"), 15000, "Wiederholen");
  if (document.querySelector("#main .frage-karte")) { const w = await rundeSpielen(1000, 8); check("Wiederholen: Runde gespielt", w.length > 0, w.length); }
  else check("Wiederholen: Fragen vorhanden", false, "nichts zu wiederholen");
  location.hash = "#/training/fehlerkiste";
  await warten(() => document.title.startsWith("Fehlerkiste") && document.querySelector("#main .frage-karte, #main .training-intro"), 15000, "Fehlerkiste");
  const vorher = store.statistik?.fehlerkiste || 0;
  if (document.querySelector("#main .frage-karte")) {
    const fk = await rundeSpielen(1000);
    check("Fehlerkiste: alle richtig beantwortet", fk.every(x => x.ok), JSON.stringify(fk.filter(x => !x.ok)));
    check("Fehlerkiste: danach leer", (store.statistik?.fehlerkiste || 0) === 0, `vorher ${vorher}, nachher ${store.statistik?.fehlerkiste}`);
  }
  const slug = store.uebersicht.teile[0].kapitel[0].slug;
  location.hash = `#/training/thema/${slug}`;
  await warten(() => document.querySelector("#main .frage-karte"), 15000, "Endlos üben");
  for (let i = 0; i < 4; i++) {
    const karte = document.querySelector("#main .schritt-buehne .frage-karte");
    const a = await beantworten(karte, true, i);
    check(`Endlos üben: Aufgabe ${i + 1} richtig`, a.ok, JSON.stringify(a));
    document.querySelector("#main .kap-nav .btn-primary").click();
    await warten(() => document.querySelector("#main .schritt-buehne .frage-karte") !== karte, 10000, "nächste Endlos-Aufgabe");
  }
  location.hash = "#/training/klausur";
  const start = await warten(() => document.querySelector("#main .training-intro .btn-primary"), 10000, "Klausurstart");
  const sel = document.querySelectorAll("#main .training-intro select")[1]; sel.value = "6";
  start.click();
  const kl = await rundeSpielen(4, 6);
  const note = norm(document.querySelector("#main .note-gross")?.textContent);
  check("Klausur: Note angezeigt", /^\d,\d$/.test(note), note);
  check("Klausur: Review mit Lösungen", document.querySelectorAll("#main .review-eintrag .feedback").length > 0, document.querySelectorAll("#main .review-eintrag").length);
  bericht.klausur = { note, fragen: kl.length };
  location.hash = "#/diagnose";
  (await warten(() => document.querySelector("#main .training-intro .btn-primary"), 10000, "Diagnose")).click();
  for (let i = 0; i < 40; i++) {
    const karte = await warten(() => document.querySelector("#main .frage-karte") || document.querySelector("#main .diag-liste"), 15000, "Diagnosefrage");
    if (karte.matches(".diag-liste")) break;
    if (i % 4 === 3) document.querySelector("#main .kap-nav .btn-ghost").click();
    else await beantworten(karte, i % 2 === 0, i);
    await warten(() => document.querySelector("#main .frage-karte") !== karte, 10000, "nächste Diagnosefrage");
  }
  check("Diagnose: Auswertung mit Empfehlung", !!document.querySelector("#main .diag-liste") && /Empfehlung/.test(document.querySelector("#main").textContent), norm(document.querySelector("#main .unter")?.textContent));
}

/* ---------------- Visuals Funktionen/Lineare Algebra bedienen (Demo-Seite) ---------------- */
async function visualsBedienen() {
  await warten(() => !document.querySelector("#main .visual[data-laedt]"), 15000, "Visuals geladen");
  const fehler = [...document.querySelectorAll("#main .vis-fehler")].map(e => norm(e.textContent).slice(0, 120));
  check("Demo: keine Visual-Fehler", !fehler.length, fehler.join(" | "));
  const vis = (art) => document.querySelector(`#main .vis-${art}`);
  const text = (el) => norm([...el.querySelectorAll("annotation")].map(a => a.textContent).join(" ") + " " + el.textContent);
  const ek = vis("einheitskreis");
  if (ek) {
    taste(ek.querySelector("svg.plot[tabindex]"), "PageUp"); await pause(50);   // 60° -> 75°
    check("einheitskreis: Tastatur, exakter Wert bei 75°", /sqrt\{6\}\+\\sqrt\{2\}/.test(text(ek.querySelector(".vf-werte"))), text(ek.querySelector(".vf-werte")).slice(0, 200));
    eingeben(ek.querySelector("input[type=range]"), "100"); await pause(50);
    check("einheitskreis: Regler 100° -> Näherung", /approx/.test(text(ek.querySelector(".vf-werte"))));
  }
  const tg = vis("tangente");
  if (tg) {
    const [, rh] = tg.querySelectorAll("input[type=range]");
    eingeben(rh, "0.5"); await pause(50);
    check("tangente: h-Regler ändert Sekante", /m_\{\\text\{Sek\}\}.*approx 1,25|m_\{\\text\{Sek\}\}.*approx 1\{,\}25/.test(text(tg)), text(tg.querySelector(".vf-werte")).slice(0, 200));
  }
  const rm = vis("riemann");
  if (rm) {
    const vorher = rm.querySelectorAll("polygon.rechteck").length;
    eingeben(rm.querySelector("input[type=range]"), "20"); await pause(50);
    [...rm.querySelectorAll(".vf-segment .btn")].find(b => b.textContent === "Obersumme").click(); await pause(50);
    check("riemann: n und Obersumme", vorher === 4 && rm.querySelectorAll("polygon.rechteck").length === 20 && /Obersumme/.test(rm.querySelector(".vf-werte").textContent), `${vorher} -> ${rm.querySelectorAll("polygon.rechteck").length}`);
  }
  const vk = vis("vektoren2d");
  if (vk) {
    taste(vk.querySelector(".vl-griff"), "ArrowUp"); await pause(50);
    check("vektoren2d: Griff mit Pfeiltaste", /pmatrix\} 3 \\\\ \\frac\{3\}\{2\}/.test(text(vk.querySelector(".vf-werte"))), text(vk.querySelector(".vf-werte")).slice(0, 160));
  }
  const mm = vis("matrix_mult");
  if (mm) {
    [...mm.querySelectorAll(".vis-steuer .btn")].find(b => /Weiter/.test(b.textContent)).click(); await pause(50);
    check("matrix_mult: Schritt 2 hebt Zeile 1 / Spalte 2 hervor", mm.querySelectorAll(".mm-matrix.b .hl-spalte").length === 3 && /c_\{12\}/.test(text(mm.querySelector(".mm-rechnung"))));
  }
  const gs = vis("gauss");
  if (gs) {
    const weiter = [...gs.querySelectorAll(".vis-steuer .btn")].find(b => /Weiter/.test(b.textContent));
    for (let i = 0; i < 20 && !weiter.disabled; i++) { weiter.click(); await pause(10); }
    check("gauss: bis zum Ende, Lösung angezeigt", /x_\{1\} = 1/.test(text(gs)) && gs.querySelector("td.pivot"), text(gs.querySelector(".vf-werte")).slice(0, 160));
  }
  const ke = vis("komplexe_ebene");
  if (ke) {
    check("komplexe_ebene: exakte Polarform", /e\^\{i\\frac\{5\\pi\}\{12\}\}/.test(text(ke)), text(ke.querySelector(".vf-werte")).slice(0, 200));
    taste(ke.querySelector(".vl-griff"), "ArrowRight"); await pause(50);
    check("komplexe_ebene: z verschiebbar", /z = \\frac\{3\}\{2\} \+ i/.test(text(ke)), text(ke.querySelector(".vf-werte")).slice(0, 160));
  }
}

/* ---------------- Werkzeuge ---------------- */
async function werkzeuge() {
  location.hash = "#/formelsammlung";
  const suche = await warten(() => document.querySelector("#main .such-feld input"), 15000, "Formelsammlung");
  check("Formelsammlung: Merkzettel vorhanden", document.querySelectorAll("#main .spick-kapitel").length >= 1, document.querySelectorAll("#main .spick-kapitel").length);
  for (const [q, soll] of [["Zahlengerade", true], ["mathbb", true], ["xyzquatsch", false]]) {
    eingeben(suche, q); await pause(350);
    const leer = !document.querySelector("#main .leer-hinweis").hidden;
    check(`Formelsammlung-Suche „${q}“`, soll ? !leer : leer, `leer=${leer}`);
  }
  location.hash = "#/glossar?q=Gegenzahl";
  await warten(() => document.querySelector("#main .glossar-liste"), 15000, "Glossar");
  check("Glossar: Suche filtert", [...document.querySelectorAll("#main .glossar-eintrag")].filter(e => !e.hidden).length === 1, [...document.querySelectorAll("#main .glossar-eintrag")].filter(e => !e.hidden).length);
  for (const [w, erwartet] of [["bruch", "frac{5}{6}"], ["primfaktoren", "2^{3}"], ["basis", "101101"], ["matrix", "det"], ["lgs", "vec x"]]) {
    location.hash = `#/spielwiese/${w}`;
    let e = null;
    try { e = await warten(() => { const x = document.querySelector("#main .spiel-ergebnis .formel-block annotation"); return x && x.textContent.includes(erwartet) ? x : null; }, 15000, "Spielwiese " + w); } catch { /* unten gemeldet */ }
    check(`Spielwiese ${w}`, !!e, e ? "" : norm(document.querySelector("#main .spiel-ergebnis")?.textContent).slice(0, 200));
  }
  location.hash = "#/demo/visuals";
  await warten(() => document.querySelector("#main .demo-grid, #main .fehler-karte"), 15000, "Demo-Seite");
  await pause(800);
  const probleme = layoutPruefen(document.querySelector("#main .container"), "Demo");
  check("Demo-Seite: alle Visuals ohne Fehler", !document.querySelector("#main .fehler-karte") && !probleme.length
        && document.querySelectorAll("#main .demo-teil").length >= 5, probleme.join("; ") || document.querySelector("#main .fehler-karte")?.textContent);
  await visualsBedienen();
  location.hash = "#/spielwiese/plotter";
  await warten(() => document.querySelector("#main .plot path.kurve"), 15000, "Plotter-Kurve");
  check("Spielwiese: Plotter zeichnet", (document.querySelector("#main .plot path.kurve").getAttribute("d") || "").length > 100);
  // Vorschau des Eingabe-Pads
  const r = await api.post("/api/term/vorschau", { text: "2x(x+1)^2", typ: "term" });
  check("Vorschau: Term gesetzt", /left\(x \+ 1\\right\)\^\{2\}/.test(r.latex || ""), r.latex);
  const f = await api.post("/api/term/vorschau", { text: "(x+1", typ: "term" });
  check("Vorschau: Fehler verständlich", /Klammer/.test(f.fehler || ""), f.fehler);
  try { await api.post("/api/antwort", { id: "gibtsnicht:00000000", antwort: "x" }); check("Unbekannte Frage -> 404", false); }
  catch (e) { check("Unbekannte Frage -> verständliche Meldung", e.status === 404 && /neu/.test(e.message), e.message); }
  location.hash = "#/kapitel/gibtsnicht";
  const fk = await warten(() => document.querySelector("#main .fehler-karte"), 10000, "Fehlerseite");
  check("Unbekanntes Kapitel -> Fehlerseite", /nicht gefunden/.test(fk.textContent), fk.textContent);
}

async function formeln() {
  const r = await api.get("/api/e2e/formeln");
  const fehler = r.formeln.map(f => [f, texFehler(f)]).filter(([, e]) => e);
  bericht.formeln = { anzahl: r.formeln.length, fehler: fehler.slice(0, 50) };
  check(`KaTeX: ${r.formeln.length} Formeln fehlerfrei`, fehler.length === 0, JSON.stringify(fehler.slice(0, 5)));
}

/* ---------------- Start ---------------- */
export async function e2eStarten(params) {
  const modus = params.get("e2e") || "kapitel";
  bericht.modus = modus;
  const { inline } = await import("./util.js");
  window.__inline = inline;
  statusEl = h("span", { id: "e2e-status", text: "läuft" });
  pre = h("pre", { id: "e2e-ergebnis", style: { maxHeight: "120px", overflow: "auto", margin: 0, fontSize: "10px" } });
  document.body.append(h("div", { id: "e2e-box", style: { position: "fixed", right: "6px", bottom: "6px", width: "260px", background: "#fffbe6", color: "#000", border: "1px solid #999", padding: "4px", zIndex: 9999, fontSize: "11px", opacity: .85 } }, h("b", { text: "E2E-Test: " }), statusEl, pre));
  try { await api.get("/api/e2e/antwort?id=x"); } catch (e) {
    if (e.status === 404 && /Unbekannte Adresse/.test(e.message)) { bericht.jsFehler.push("Server läuft nicht mit --e2e"); bericht.fertig = true; anzeigen(); return; }
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
    else if (modus === "werkzeuge") await werkzeuge();
    else if (modus === "formeln") await formeln();
    else if (modus === "zustand") {
      // Für Screenshots: Kapitelschritt öffnen und die Frage n-mal falsch beantworten, dann stehen bleiben
      location.hash = `#/kapitel/${params.get("slug")}/${params.get("schritt") || 0}`;
      const karte = await warten(() => document.querySelector("#main .frage-karte"), 15000, "Frage");
      const n = parseInt(params.get("falsch") || "1", 10);
      const antwort = await loesungHolen(karte);
      const knopf = karte.querySelector(".frage-aktionen .btn-primary");
      for (let i = 0; i < n; i++) {
        await versuch(karte, karte.dataset.typ, params.get("eingabe") || antwort, !!params.get("eingabe"), 0, knopf);
        await warten(() => karte.querySelectorAll(".feedback").length && !knopf.disabled, 10000, "Feedback");
        await pause(200);
      }
      if (params.get("tipp")) karte.querySelector(".frage-aktionen .btn-ghost")?.click();
      document.getElementById("e2e-box").remove();
      window.scrollTo(0, Math.max(0, karte.getBoundingClientRect().top + scrollY - 70));
    }
  } catch (e) { check("Abbruch", false, e.message + " " + (e.stack || "")); }
  bericht.statistik = store.statistik ? { xp: store.statistik.xp, level: store.statistik.levelName, fehlerkiste: store.statistik.fehlerkiste, abzeichen: store.statistik.abzeichen.filter(a => a.erreicht).map(a => a.id) } : null;
  bericht.fertig = true;
  bericht.ende = new Date().toISOString();
  statusEl.textContent = "fertig";
  anzeigen();
  try { await api.post("/api/e2e/bericht", bericht); } catch { /* egal */ }
}
