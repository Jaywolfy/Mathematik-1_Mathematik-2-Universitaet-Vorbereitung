// Spielwiese, Spickzettel und Demo-Galerie (für Screenshots: ?demo=visuals).
import { h, lade, lokal, debounce, $$ } from "./util.js";
import { api } from "./api.js";
import { store } from "./store.js";
import { Editor } from "./editor.js";
import { eingabenFeld, ausfuehren, brauchtEingabe } from "./runner.js";
import { tracerPanel } from "./tracer.js";
import { renderBloecke, renderSeiten, renderBlock } from "./markup.js";
import { visual, VISUAL_TYPEN } from "./visuals.js";
import { frageKarte } from "./fragen.js";

/* ------------------------------------------------------------------ Spielwiese */
export const BEISPIELE = [
  { name: "👋 Hallo mit Eingabe", eingaben: ["Anna"], code: 'name = input("Wie heißt du? ")\nprint("Hallo", name + "!")\nprint("Dein Name hat", len(name), "Buchstaben.")' },
  { name: "🔁 while-Schleife", code: "zahl = 1\nwhile zahl <= 5:\n    print(zahl, \"zum Quadrat ist\", zahl ** 2)\n    zahl += 1\nprint(\"fertig\")" },
  { name: "🛒 Liste & for", code: "einkauf = [\"Milch\", \"Brot\", \"Äpfel\"]\neinkauf.append(\"Käse\")\nfor ding in einkauf:\n    print(\"-\", ding)\nprint(len(einkauf), \"Dinge auf der Liste\")" },
  { name: "⚙️ Funktion", code: "def brutto(netto, steuer=0.19):\n    return round(netto * (1 + steuer), 2)\n\npreis = brutto(10)\nprint(\"Preis mit MwSt:\", preis)\nprint(brutto(100, 0.07))" },
  { name: "🥞 Rekursion (Fakultät)", code: "def fak(n):\n    if n <= 1:\n        return 1\n    return n * fak(n - 1)\n\nergebnis = fak(4)\nprint(ergebnis)" },
  { name: "📒 Dictionary", code: "telefon = {\"Anna\": \"0151 234\", \"Ben\": \"0176 987\"}\ntelefon[\"Cem\"] = \"0160 555\"\nfor name, nummer in telefon.items():\n    print(name, \"→\", nummer)" },
  { name: "🏷️ Zwei Namen, eine Liste", code: "a = [1, 2, 3]\nb = a          # kein Kopieren!\nc = a.copy()   # echte Kopie\nb.append(4)\nprint(a)\nprint(c)" },
];

export function spielwiese(main) {
  document.title = "Spielwiese · Python-Vorkurs";
  let start = { code: lokal.get("spielwiese_code", BEISPIELE[1].code), eingaben: lokal.get("spielwiese_eingaben", []) };
  try {
    const imp = sessionStorage.getItem("spielwiese_import");
    if (imp) { start = JSON.parse(imp); sessionStorage.removeItem("spielwiese_import"); }
  } catch { /* egal */ }
  const eingabe = eingabenFeld(start.eingaben || [], { sichtbar: brauchtEingabe(start.code) });
  eingabe.el.style.borderRadius = "0 0 12px 12px";
  const merken = debounce(() => { lokal.set("spielwiese_code", editor.wert); lokal.set("spielwiese_eingaben", eingabe.werte()); }, 500);
  eingabe.ta.addEventListener("input", merken);
  const ausgabeSlot = h("div");
  const traceSlot = h("div");
  const editor = new Editor({
    wert: start.code, minZeilen: 14, label: "Spielwiese",
    onChange: (c) => { merken(); eingabe.el.hidden = !brauchtEingabe(c); editor.setzeGespeichert(""); },
    onStrgEnter: () => bAus.click(),
  });
  editor.el.querySelector(".ed-hilfe").innerHTML = "<kbd>Tab</kbd> einrücken · <kbd>Strg</kbd>+<kbd>/</kbd> Kommentar · <kbd>Strg</kbd>+<kbd>Enter</kbd> ausführen";
  const auswahl = h("select", { "aria-label": "Beispiel laden" }, h("option", { value: "", text: "📚 Beispiel laden …" }), BEISPIELE.map((b, i) => h("option", { value: i, text: b.name })));
  auswahl.onchange = () => {
    const b = BEISPIELE[auswahl.value];
    if (!b) return;
    editor.wert = b.code; eingabe.ta.value = (b.eingaben || []).join("\n"); eingabe.el.hidden = !brauchtEingabe(b.code);
    merken(); auswahl.value = ""; ausgabeSlot.replaceChildren(); traceSlot.replaceChildren(); editor.fokus();
  };
  const bAus = h("button", { class: "btn btn-primary", type: "button" }, h("span", { class: "ico", text: "▶" }), "Ausführen");
  const bTrace = h("button", { class: "btn", type: "button" }, h("span", { class: "ico", text: "👣" }), "Schritt für Schritt");
  const bLeer = h("button", { class: "btn btn-ghost", type: "button", text: "🗑 Leeren" });
  bAus.onclick = () => { traceSlot.replaceChildren(); ausfuehren(editor.wert, eingabe.werte(), ausgabeSlot); };
  bTrace.onclick = () => { ausgabeSlot.replaceChildren(); traceSlot.replaceChildren(tracerPanel(editor.wert, eingabe.werte(), { onSchliessen: () => traceSlot.replaceChildren() })); };
  bLeer.onclick = () => { editor.wert = ""; merken(); ausgabeSlot.replaceChildren(); traceSlot.replaceChildren(); editor.fokus(); };
  main.replaceChildren(h("div", { class: "container breit" },
    h("div", { class: "seitenkopf" }, h("div", null, h("h1", { text: "🧪 Spielwiese" }), h("p", { text: "Probier hier alles aus, was du gelernt hast. Nichts kann kaputtgehen – dein Code läuft sicher in einem eigenen Prozess." }))),
    h("div", { class: "spielwiese-grid" },
      h("div", { class: "werkzeugleiste" }, auswahl, h("span", { class: "spacer" }), bLeer, bTrace, bAus),
      h("div", null, editor.el, eingabe.el), ausgabeSlot, traceSlot)));
  setTimeout(() => editor.fokus(), 50);
  return () => merken.sofort();
}

/* ------------------------------------------------------------------ Spickzettel */
export async function spickzettel(main) {
  document.title = "Spickzettel · Python-Vorkurs";
  main.replaceChildren(lade());
  const d = await api.get("/api/spickzettel");
  const suche = h("input", { class: "feld", type: "search", placeholder: "Suchen, z. B. „range“, „Slicing“, „def“ …", "aria-label": "Spickzettel durchsuchen" });
  const tabs = [["alles", "Alles"], ["spick", "📋 Spickzettel"], ["merk", "📌 Merkzettel je Kapitel"]];
  let tab = lokal.get("spick_tab", "alles");
  const tabBar = h("div", { class: "spick-tabs", role: "tablist" });
  const allgemein = h("section", { "aria-label": "Spickzettel" }, (d.seiten || []).map(s => h("div", { class: "karte spick-seite" }, renderBloecke(s))));
  const kapitel = h("section", { "aria-label": "Merkzettel je Kapitel" },
    h("h2", { class: "abschnitt-titel", text: "Merkzettel der Kapitel" }),
    (d.kapitel || []).map(k => h("details", { class: "karte spick-kapitel", "data-slug": k.slug },
      h("summary", null, h("span", { class: "k-ico", "aria-hidden": "true", text: k.icon }), h("span", { text: `${k.nummer}. ${k.titel}` }), h("span", { class: "pfeil", "aria-hidden": "true", text: "▶" })),
      h("div", { class: "spick-inhalt" }, renderSeiten(k.seiten), h("a", { class: "btn btn-sm btn-soft", style: { marginTop: "14px" }, href: `#/kapitel/${k.slug}`, text: "Zum Kapitel →" })))));
  const leer = h("div", { class: "leer-hinweis", hidden: true }, h("span", { class: "gross", text: "🔍" }), "Nichts gefunden. Versuch einen anderen Begriff.");
  const malenTabs = () => {
    tabBar.replaceChildren(...tabs.map(([id, name]) => h("button", { class: "tab", role: "tab", type: "button", "aria-selected": id === tab ? "true" : "false", text: name,
      onclick: () => { tab = id; lokal.set("spick_tab", id); malenTabs(); filtern(); } })));
  };
  const filtern = () => {
    const q = suche.value.trim().toLowerCase();
    allgemein.hidden = tab === "merk";
    kapitel.hidden = tab === "spick";
    $$("mark.treffer", main).forEach(m => m.replaceWith(document.createTextNode(m.textContent)));
    main.normalize();
    let treffer = 0;
    const bloecke = [...allgemein.querySelectorAll(".md > *"), ...kapitel.querySelectorAll(".spick-kapitel")];
    for (const b of bloecke) {
      const passt = !q || b.textContent.toLowerCase().includes(q);
      b.classList.toggle("versteckt-suche", !passt);
      if (passt && q) { treffer++; markieren(b, q); if (b.tagName === "DETAILS") b.open = true; }
    }
    $$(".spick-seite", allgemein).forEach(s => s.classList.toggle("versteckt-suche", !!q && !s.querySelector(".md > *:not(.versteckt-suche)")));
    leer.hidden = !q || treffer > 0;
  };
  suche.addEventListener("input", debounce(filtern, 120));
  malenTabs();
  main.replaceChildren(h("div", { class: "container" },
    h("div", { class: "seitenkopf" }, h("div", null, h("h1", { text: "📋 Spickzettel" }), h("p", { text: "Alles Wichtige zum Nachschlagen – auch prima zum Ausdrucken (Strg+P)." }))),
    h("div", { class: "such-feld" }, suche), tabBar, leer, allgemein, kapitel));
  filtern();
  suche.focus();
  return null;
}

function markieren(wurzel, q) {
  const walker = document.createTreeWalker(wurzel, NodeFilter.SHOW_TEXT);
  const knoten = [];
  while (walker.nextNode()) knoten.push(walker.currentNode);
  for (const t of knoten) {
    const text = t.nodeValue, i = text.toLowerCase().indexOf(q);
    if (i < 0 || t.parentElement.closest("button, summary .pfeil")) continue;
    const frag = document.createDocumentFragment();
    frag.append(text.slice(0, i), h("mark", { class: "treffer", text: text.slice(i, i + q.length) }), text.slice(i + q.length));
    t.replaceWith(frag);
  }
}

/* ------------------------------------------------------------------ Demo */
export const DEMO_VISUALS = {
  variablen: { vars: [{ name: "alter", wert: "18", typ: "int" }], schritte: [
    [{ name: "alter", wert: "18", typ: "int" }],
    [{ name: "alter", wert: "18", typ: "int" }, { name: "name", wert: "'Anna'", typ: "str" }],
    [{ name: "alter", wert: "19", typ: "int" }, { name: "name", wert: "'Anna'", typ: "str" }, { name: "volljaehrig", wert: "True", typ: "bool" }]],
    texte: ["`alter = 18` legt eine Kiste mit der Aufschrift „alter“ an.", "`name = 'Anna'` – eine zweite Kiste, diesmal mit Text.", "`alter = alter + 1` überschreibt den alten Inhalt."] },
  liste: { name: "noten", werte: [1.3, 2.0, 1.7, 3.0, 2.3], markiert: [0], slice: "1:4", interaktiv: true, negativ: true },
  string: { text: "Python", markiert: [0], slice: "::-1" },
  dict: { name: "telefon", paare: [["Anna", "0151 234"], ["Ben", "0176 987"], ["Cem", "0160 555"]], markiert: ["Ben"] },
  referenz: { namen: { a: 0, b: 0, c: 1 }, objekte: [[1, 2, 3], [1, 2, 3]] },
  ablauf: { schritte: [{ icon: "👩‍💻", text: "Du schreibst **Quelltext**" }, { icon: "🐍", text: "Python liest Zeile für Zeile" }, { icon: "⚙️", text: "Der Computer führt aus" }, { icon: "🖥️", text: "Ausgabe erscheint" }] },
  entscheidung: { bedingung: "alter >= 18", ja: "Eintritt frei 🎉", nein: "Kein Eintritt", elif: [{ bedingung: "alter >= 16", text: "Nur mit Begleitung" }] },
  schleife: { bedingung: "zahl < 5", koerper: ["print(zahl)", "zahl += 1"], danach: "print('fertig')", art: "while" },
  zahlenstrahl: { start: 2, stop: 11, step: 3, interaktiv: true },
  wahrheitstabelle: { variablen: ["a", "b"], ausdruecke: ["a and b", "a or b", "not a"] },
  stapel: { rahmen: ["fak(3)", "fak(2)", "fak(1)"], rueckgaben: ["6", "2", "1"] },
  baum: { wurzel: { text: "fib(4)", kinder: [{ text: "fib(3)", kinder: [{ text: "fib(2)", kinder: [{ text: "fib(1)" }, { text: "fib(0)" }] }, { text: "fib(1)" }] }, { text: "fib(2)", kinder: [{ text: "fib(1)" }, { text: "fib(0)" }] }] } },
  funktion: { name: "verdoppeln", eingaben: ["x = 4"], ausgabe: "8", innen: "return x * 2" },
  typen: { werte: ["42", "3.14", "'Hallo'", "True", "None", "[1, 2]", "(1, 2)", "{'a': 1}", "-7", "\"Python\""] },
};

const DEMO_TRACE = "def fak(n):\n    if n <= 1:\n        return 1\n    return n * fak(n - 1)\n\nzahlen = [3, 1, 2]\nandere = zahlen\nandere.append(fak(3))\nprint(zahlen)";

export async function demo(main, art) {
  document.title = "Demo · Python-Vorkurs";
  const c = h("div", { class: "container" });
  main.replaceChildren(c);
  if (art === "trace") {
    c.append(h("h1", { style: { marginBottom: "16px" }, text: "Demo: Schritt für Schritt" }));
    const t = tracerPanel(DEMO_TRACE, []);
    c.append(t);
    // nach dem Laden zu einem interessanten Schritt springen (Rekursion + Aliasing)
    const ziel = parseInt(new URLSearchParams(location.search).get("schritt") || "14", 10);
    const warten = setInterval(() => {
      const r = t.querySelector("input[type=range]");
      if (!r) return;
      clearInterval(warten);
      r.value = Math.min(ziel, parseInt(r.max, 10)); r.dispatchEvent(new Event("input"));
    }, 100);
    return () => clearInterval(warten);
  }
  if (art === "inhalte") {
    // Rendert alle Erklärungen + Merkzettel aller Kapitel (Prüfung der echten Inhalte)
    c.append(h("h1", { style: { marginBottom: "16px" }, text: "Demo: alle Inhalte" }));
    const statistik = h("p", { id: "inhalte-statistik", class: "chip" });
    c.append(statistik);
    const kap = (store.uebersicht?.teile || []).flatMap(t => t.kapitel);
    let bloecke = 0, probleme = [];
    for (const k of kap) {
      const d = await api.get(`/api/kapitel/${k.slug}`);
      const sek = h("section", { class: "karte erkl-karte", style: { marginBottom: "18px" } }, h("h2", { text: `${k.nummer}. ${k.titel}` }));
      for (const e of d.elemente) {
        if (e.typ !== "erklaerung" && e.typ !== "zusammenfassung") continue;
        for (const s of e.seiten || []) { bloecke += s.length; sek.append(renderBloecke(s)); }
      }
      c.append(sek);
      sek.querySelectorAll(".vis-fehler").forEach(x => probleme.push(`${k.slug}: ${x.textContent}`));
    }
    statistik.textContent = `${kap.length} Kapitel, ${bloecke} Blöcke, ${c.querySelectorAll(".visual").length} Visuals, ${probleme.length} Probleme`;
    if (probleme.length) c.prepend(h("pre", { id: "inhalte-probleme", class: "fehler-karte", text: probleme.join("\n") }));
    return null;
  }
  if (art === "fragen") {
    c.append(h("h1", { style: { marginBottom: "16px" }, text: "Demo: alle Fragetypen" }));
    const gesucht = new Set(["mc", "wf", "text", "ausgabe", "ausdruck", "luecke", "puzzle", "code"]);
    const kap = (store.uebersicht?.teile || []).flatMap(t => t.kapitel);
    const gefunden = [];
    for (const k of kap) {
      if (!gesucht.size) break;
      const d = await api.get(`/api/kapitel/${k.slug}`);
      for (const e of d.elemente) if (e.typ === "frage" && gesucht.has(e.frage.typ)) { gesucht.delete(e.frage.typ); gefunden.push(e.frage); }
    }
    const q = new URLSearchParams(location.search);
    const nurTyp = q.get("typ");
    for (const f of gefunden) {
      if (nurTyp && f.typ !== nurTyp) continue;
      const el = frageKarte(f, { kontext: f.kapitel }).el;
      c.append(h("div", { style: { marginBottom: "22px" } }, el));
      // ?auto=1: Karte automatisch (meist falsch) beantworten – für Screenshots von Feedback & Tests
      if (q.get("auto")) setTimeout(() => {
        el.querySelectorAll(".option")[1]?.click();
        [...el.querySelectorAll(".quelle .baustein")].slice(0, 2).forEach(b => b.click());
        el.querySelectorAll(".luecke-feld").forEach(x => { x.value = "x"; });
        const t = el.querySelector("input.feld, textarea.feld"); if (t) t.value = "42";
        el.querySelector(".wf-btn")?.click();
        const ed = el.querySelector(".ed-flaeche textarea");
        if (ed) { ed.value = "print(\"Hallo Welt\")\nprint(\"Tschüss\")"; ed.dispatchEvent(new Event("input")); }
        [...el.querySelectorAll("button")].find(b => /Prüfen/.test(b.textContent))?.click();
      }, 400);
    }
    return null;
  }
  // Galerie aller Visual-Typen + Markup-Blöcke
  c.append(h("div", { class: "seitenkopf" }, h("div", null, h("h1", { text: "Demo: Visualisierungen & Blöcke" }), h("p", { text: "Alle :::visual-Typen aus dem Vertrag sowie die übrigen Markup-Blöcke." }))));
  const grid = h("div", { class: "demo-grid" });
  // ?typen=liste,dict  zeigt nur diese Typen; "bloecke" = Markup-Blöcke
  const nur = (new URLSearchParams(location.search).get("typen") || "").split(",").filter(Boolean);
  const zeigen = (t) => !nur.length || nur.includes(t);
  for (const t of VISUAL_TYPEN.filter(zeigen)) grid.append(h("section", { class: "demo-teil" }, h("h2", { text: `:::visual ${t}` }), visual(t, DEMO_VISUALS[t])));
  if (zeigen("bloecke")) grid.append(h("section", { class: "demo-teil" }, h("h2", { text: "Markup-Blöcke" }), renderBloecke([
    { typ: "ueberschrift", text: "Überschrift mit `code`" },
    { typ: "absatz", text: "Ein Absatz mit **fettem Text**, `inline_code()` und <b>HTML, das escaped wird</b>." },
    { typ: "merke", text: "Variablen sind **beschriftete Kisten** für Werte." },
    { typ: "liste", nummeriert: false, punkte: ["Erster Punkt", "Zweiter mit `len()`"] },
    { typ: "liste", nummeriert: true, punkte: ["Schritt eins", "Schritt zwei"] },
    { typ: "tabelle", kopf: ["Operator", "Bedeutung"], zeilen: [["`//`", "ganzzahlig teilen"], ["`%`", "Rest"]] },
    { typ: "box", art: "analogie", titel: "🏠 Eine Variable ist wie ein Briefkasten", bloecke: [{ typ: "absatz", text: "Auf dem Briefkasten steht ein **Name**, drinnen liegt der **Wert**." }] },
    { typ: "box", art: "achtung", titel: "`=` ist nicht `==`", bloecke: [{ typ: "absatz", text: "`=` weist zu, `==` vergleicht." }] },
    { typ: "box", art: "info", titel: "Hintergrund", bloecke: [{ typ: "absatz", text: "Python wurde 1991 veröffentlicht." }] },
    { typ: "codeblock", code: "for i in range(3):\n    print(f\"Runde {i + 1}\")  # f-String" },
    { typ: "vergleich", titel: ["❌ So nicht", "✅ So geht's"], spalten: [[{ typ: "codeblock", code: "if x = 5:\n    print(x)" }], [{ typ: "codeblock", code: "if x == 5:\n    print(x)" }]] },
    { typ: "code", code: "name = input(\"Name? \")\nprint(\"Hallo\", name)", eingaben: ["Anna"], trace: false },
    { typ: "code", code: DEMO_TRACE, eingaben: [], trace: true },
  ])));
  c.append(grid);
  return null;
}

export { renderBlock };
