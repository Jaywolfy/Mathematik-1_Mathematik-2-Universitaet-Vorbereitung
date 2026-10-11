// Schritt-für-Schritt-Visualisierer (ähnlich Python Tutor).
import { h, inline, esc, lade, reduziert } from "./util.js";
import { api } from "./api.js";
import { highlightZeilen } from "./highlight.js";
import { varKiste, wertElement, legende, ALIAS_FARBEN } from "./werte.js";

const TEMPO = { langsam: 1400, normal: 800, schnell: 350 };

/** Fehler-Info aus Trace- oder Ausführungs-Ergebnis vereinheitlichen. */
export function fehlerInfo(d) {
  if (!d) return null;
  const f = d.fehler;
  if (!f && !d.timeout) return null;
  if (f && typeof f === "object") {
    return {
      text: f.text || f.fehler || f.meldung || f.typ || JSON.stringify(f),
      zeile: f.zeile ?? f.fehler_zeile ?? d.fehler_zeile ?? null,
      erklaert: f.erklaert || f.fehler_erklaert || d.fehler_erklaert || null,
    };
  }
  return { text: f ? String(f) : "Zeitlimit überschritten", zeile: d.fehler_zeile ?? null, erklaert: d.fehler_erklaert || null, timeout: !!d.timeout };
}

export function fehlerKarte(info) {
  if (!info) return null;
  return h("div", { class: "fehler-erklaert", role: "alert" },
    h("span", { class: "fe-icon", text: info.timeout ? "⏱️" : "🐞" }),
    h("div", { class: "fe-text" },
      h("b", { text: info.timeout ? "Das Programm wurde abgebrochen" : "Was bedeutet dieser Fehler?" }),
      info.erklaert ? h("div", { html: inline(info.erklaert) }) : h("div", { text: "Python ist auf ein Problem gestoßen und hat das Programm angehalten." }),
      h("code", { class: "fe-roh", text: info.text + (info.zeile ? `  (Zeile ${info.zeile})` : "") })));
}

/** Tracer laden und anzeigen. */
export function tracerPanel(code, eingaben = [], { onSchliessen = null, titel = "Schritt für Schritt" } = {}) {
  const box = h("section", { class: "tracer", "aria-label": "Schritt-für-Schritt-Ansicht" }, lade("Programm wird Schritt für Schritt ausgeführt …"));
  api.post("/api/trace", { code, eingaben }).then(daten => {
    box.replaceChildren();
    aufbauen(box, code, daten, { onSchliessen, titel });
  }).catch(e => {
    box.replaceChildren(h("div", { class: "fehler-karte", style: { margin: "12px" }, text: "Schritt-für-Schritt-Ansicht nicht möglich: " + e.message }));
  });
  return box;
}

export function tracerAusDaten(code, daten, opts = {}) {
  const box = h("section", { class: "tracer", "aria-label": "Schritt-für-Schritt-Ansicht" });
  aufbauen(box, code, daten, opts);
  return box;
}

function rahmenName(f) {
  const n = f.funktion || "<modul>";
  return n === "<module>" || n === "<modul>" ? "Hauptprogramm" : n + "()";
}

function aufbauen(box, code, daten, { onSchliessen, titel }) {
  const schritte = Array.isArray(daten.schritte) ? daten.schritte : [];
  const fehler = fehlerInfo(daten);
  const zeilenHtml = highlightZeilen(code.replace(/\s+$/, ""));

  // Kopf
  const info = h("span", { class: "schritt-info", "aria-live": "polite" });
  const vollBtn = h("button", { class: "btn btn-sm btn-ghost", type: "button", title: "Vollbild", "aria-label": "Vollbild umschalten", text: "⛶ Groß" });
  const kopf = h("div", { class: "tr-kopf" },
    h("span", { class: "titel" }, "👣 ", titel), info, h("span", { class: "spacer" }), vollBtn,
    onSchliessen ? h("button", { class: "btn btn-sm btn-ghost", type: "button", "aria-label": "Schritt-für-Schritt-Ansicht schließen", text: "✕ Schließen", onclick: () => { stop(); onSchliessen(); } }) : null);
  box.append(kopf);

  if (!schritte.length) {
    box.append(h("div", { style: { padding: "14px" } },
      fehler ? fehlerKarte(fehler) : h("p", { class: "tr-leer", text: "Keine Schritte – das Programm ist leer oder konnte nicht starten." })));
    if (daten.ausgabe || daten.stdout) box.append(h("div", { class: "tr-unten" }, konsoleMini(daten.ausgabe || daten.stdout, "")));
    return;
  }

  // Code-Spalte
  const codeSpalte = h("div", { class: "tr-code", tabindex: "0", "aria-label": "Programmcode mit Markierung der aktuellen Zeile" });
  const zeilenEls = zeilenHtml.map((z, i) => {
    const el = h("div", { class: "tr-zeile", "data-zeile": i + 1 },
      h("span", { class: "tr-pfeil", "aria-hidden": "true" }), h("span", { class: "tr-nr", text: i + 1 }), h("code", { html: z || " " }));
    codeSpalte.append(el);
    return el;
  });
  const pfeilLegende = h("div", { class: "tr-pfeil-legende" },
    h("span", null, h("b", { class: "gruen", text: "➜ " }), "gerade ausgeführt"),
    h("span", null, h("b", { class: "hell", text: "➜ " }), "kommt als Nächstes"));
  const zustand = h("div", { class: "tr-zustand" });
  const links = h("div", { style: { display: "flex", flexDirection: "column", minWidth: 0 } }, codeSpalte);
  codeSpalte.prepend(pfeilLegende);
  box.append(h("div", { class: "tr-haupt" }, links, zustand));

  // Steuerung
  const regler = h("input", { type: "range", min: 0, max: schritte.length - 1, value: 0, "aria-label": "Schritt wählen" });
  const bAnfang = h("button", { class: "btn btn-sm", type: "button", text: "⏮", title: "Zum Anfang", "aria-label": "Zum Anfang" });
  const bZurueck = h("button", { class: "btn btn-sm", type: "button", text: "◀", title: "Schritt zurück (←)", "aria-label": "Schritt zurück" });
  const bVor = h("button", { class: "btn btn-sm btn-primary", type: "button", text: "▶", title: "Nächster Schritt (→)", "aria-label": "Nächster Schritt" });
  const bEnde = h("button", { class: "btn btn-sm", type: "button", text: "⏭", title: "Zum Ende", "aria-label": "Zum Ende" });
  const bSpiel = h("button", { class: "btn btn-sm btn-soft", type: "button", text: "▶ Abspielen" });
  const tempo = h("select", { "aria-label": "Geschwindigkeit" },
    h("option", { value: "langsam", text: "🐢 langsam" }), h("option", { value: "normal", text: "Normal", selected: true }), h("option", { value: "schnell", text: "🐇 schnell" }));
  box.append(h("div", { class: "tr-steuerung" }, bAnfang, bZurueck, regler, bVor, bEnde, bSpiel, tempo));

  const erkl = h("div", { class: "tr-erklaerung", "aria-live": "polite" });
  box.append(erkl);
  const unten = h("div", { class: "tr-unten" });
  box.append(unten);
  if (daten.abgebrochen) unten.append(h("div", { class: "tr-hinweis", text: `⚠️ Nach ${schritte.length} Schritten angehalten – das Programm ist zu lang für die Schritt-Ansicht (oder eine Endlosschleife).` }));
  const konsoleSlot = h("div");
  const fehlerSlot = h("div");
  unten.append(konsoleSlot, fehlerSlot, h("div", { style: { display: "flex", justifyContent: "space-between", gap: "10px", flexWrap: "wrap" } }, legende(),
    h("span", { class: "tr-leer", style: { fontStyle: "normal" }, html: "Tasten: <kbd>←</kbd> <kbd>→</kbd> Schritt, <kbd>Leertaste</kbd> Abspielen" })));

  // Parameter jedes Aufrufs merken (beim "call"-Ereignis enthalten die lokalen Variablen genau die Parameter)
  const aufrufParams = [];
  { const stack = [];
    schritte.forEach((st, j) => {
      const tiefe = (st.stapel || []).length;
      stack.length = Math.max(0, tiefe);
      if (st.ereignis === "call" && tiefe) {
        const vars = (st.stapel[tiefe - 1] || {}).variablen || {};
        stack[tiefe - 1] = Object.entries(vars).filter(([, w]) => !w || w.typ !== "function").map(([n, w]) => `${n}=${kuerzen(w ? w.repr : "None")}`).join(", ");
      }
      aufrufParams[j] = stack.slice();
    }); }
  let idx = -1, timer = null;

  function stop() { if (timer) { clearInterval(timer); timer = null; } bSpiel.textContent = "▶ Abspielen"; }
  function abspielen() {
    if (timer) { stop(); return; }
    if (idx >= schritte.length - 1) zeigen(0);
    bSpiel.textContent = "⏸ Pause";
    timer = setInterval(() => {
      if (!box.isConnected || idx >= schritte.length - 1) { stop(); return; }
      zeigen(idx + 1);
    }, TEMPO[tempo.value] || 800);
  }
  tempo.addEventListener("change", () => { if (timer) { stop(); abspielen(); } });

  function zeigen(n) {
    n = Math.max(0, Math.min(schritte.length - 1, n));
    const vorwaerts = n === idx + 1;
    idx = n;
    const s = schritte[n], vorher = n > 0 ? schritte[n - 1] : null;
    const istLetzter = n === schritte.length - 1;
    regler.value = n;
    info.textContent = `Schritt ${n + 1} von ${schritte.length}`;
    bAnfang.disabled = bZurueck.disabled = n === 0;
    bVor.disabled = bEnde.disabled = istLetzter;

    // Zeilenmarkierung
    zeilenEls.forEach(z => z.classList.remove("aktuell", "naechste", "fehler"));
    let aktuell = null, naechste = null;
    if (s.ereignis === "line" || s.ereignis === "call") { naechste = s.zeile; aktuell = vorher ? vorher.zeile : null; }
    else { aktuell = s.zeile; }
    const fehlerHier = istLetzter && fehler && (s.ereignis === "exception" || fehler.zeile);
    if (fehlerHier) { aktuell = null; naechste = null; }
    if (aktuell && zeilenEls[aktuell - 1]) zeilenEls[aktuell - 1].classList.add("aktuell");
    if (naechste && zeilenEls[naechste - 1] && naechste !== aktuell) zeilenEls[naechste - 1].classList.add("naechste");
    else if (naechste && zeilenEls[naechste - 1]) zeilenEls[naechste - 1].classList.add("aktuell");
    if (fehlerHier) {
      const fz = fehler.zeile || s.zeile;
      if (zeilenEls[fz - 1]) zeilenEls[fz - 1].classList.add("fehler");
    }
    const ziel = codeSpalte.querySelector(".tr-zeile.fehler, .tr-zeile.naechste, .tr-zeile.aktuell");
    if (ziel) {
      const top = ziel.offsetTop - codeSpalte.clientHeight / 2 + ziel.offsetHeight / 2;
      codeSpalte.scrollTo({ top: Math.max(0, top), behavior: reduziert() ? "auto" : "smooth" });
    }

    // Variablen & Stapel
    zustandZeichnen(s, vorher, vorwaerts);

    // Konsole
    const ausgabe = s.ausgabe || "";
    const alt = vorher && vorwaerts ? (vorher.ausgabe || "") : ausgabe;
    konsoleSlot.replaceChildren(konsoleMini(ausgabe, ausgabe.startsWith(alt) ? alt : ausgabe));

    // Erklärung
    erkl.replaceChildren(...erklaerung(s, vorher, istLetzter));
    fehlerSlot.replaceChildren();
    if (istLetzter && fehler) fehlerSlot.append(fehlerKarte(fehler));
  }

  function zustandZeichnen(s, vorher, vorwaerts) {
    const stapel = Array.isArray(s.stapel) ? s.stapel : [];
    const alteWerte = new Map();
    if (vorher && vorwaerts) {
      (vorher.stapel || []).forEach((f, ebene) => Object.entries(f.variablen || {}).forEach(([n, w]) =>
        alteWerte.set(`${ebene}|${f.funktion}|${n}`, JSON.stringify([w.typ, w.repr]))));
    }
    // Aliasing: gleiche id bei veränderlichen Objekten
    const idNamen = new Map();
    stapel.forEach((f, ebene) => Object.entries(f.variablen || {}).forEach(([n, w]) => {
      if (!w || w.id === undefined || !["list", "dict", "set", "andere"].includes(w.typ)) return;
      if (!idNamen.has(w.id)) idNamen.set(w.id, []);
      idNamen.get(w.id).push({ n, ebene, f: rahmenName(f) });
    }));
    const aliasInfo = new Map();
    let fi = 0;
    for (const [id, liste] of idNamen) {
      if (liste.length < 2) continue;
      const farbe = ALIAS_FARBEN[fi % ALIAS_FARBEN.length];
      const marke = String.fromCharCode(65 + fi);
      fi++;
      aliasInfo.set(id, { farbe, marke, liste });
    }

    const kinder = [h("div", { class: "tr-zustand-titel" }, "🧠 Speicher", h("span", { class: "chip", text: stapel.length > 1 ? `Aufrufstapel: ${stapel.length} Rahmen` : "Variablen" }))];
    const neuerRahmen = vorher && vorwaerts && (vorher.stapel || []).length < stapel.length;
    [...stapel].map((f, ebene) => ({ f, ebene })).reverse().forEach(({ f, ebene }, k) => {
      const oben = k === 0;
      const vars = Object.entries(f.variablen || {});
      const rahmen = h("div", { class: "tr-rahmen" + (oben ? " aktiv" : " inaktiv") + (oben && neuerRahmen ? " neu-rein" : "") },
        h("div", { class: "tr-rahmen-kopf" },
          h("span", { text: ebene === 0 ? "🏠" : "📞" }),
          h("span", { class: "fname", text: ebene > 0 && aufrufParams[idx] && aufrufParams[idx][ebene] !== undefined ? `${f.funktion}(${aufrufParams[idx][ebene]})` : rahmenName(f) }),
          oben && stapel.length > 1 ? h("span", { class: "chip primary", text: "aktiv" }) : null,
          h("span", { class: "ebene", text: ebene === 0 ? "global" : `Ebene ${ebene}` + (f.zeile ? ` · Zeile ${f.zeile}` : "") })));
      const grid = h("div", { class: "tr-vars" });
      if (!vars.length) grid.append(h("span", { class: "tr-leer", text: ebene === 0 ? "Noch keine Variablen." : "Keine lokalen Variablen." }));
      vars.forEach(([n, w]) => {
        const schluessel = `${ebene}|${f.funktion}|${n}`;
        let klasse = "";
        if (vorher && vorwaerts) {
          const alt = alteWerte.get(schluessel);
          if (alt === undefined) klasse = "neu";
          else if (alt !== JSON.stringify([w.typ, w.repr])) klasse = "geaendert";
        }
        let alias = null;
        const ai = w && aliasInfo.get(w.id);
        if (ai) {
          const andere = ai.liste.filter(x => !(x.n === n && x.ebene === ebene)).map(x => x.ebene === ebene ? x.n : `${x.n} (in ${x.f})`);
          alias = { farbe: ai.farbe, marke: ai.marke, text: `zeigt auf dasselbe Objekt wie ${andere.join(", ")}` };
        }
        if (w && w.typ === "function") klasse += " vk-funktion";
        grid.append(varKiste(n, wertElement(w), w ? w.typ : "NoneType", { klasse, alias }));
      });
      rahmen.append(grid);
      if (oben && s.ereignis === "return") {
        rahmen.append(h("div", { class: "tr-rueckgabe" }, "↩ Rückgabewert: ", wertElement(s.rueckgabe)));
      }
      kinder.push(rahmen);
    });
    zustand.replaceChildren(...kinder);
  }

  function erklaerung(s, vorher, istLetzter) {
    const tiefe = s.stapel ? s.stapel.length : 0;
    let name = tiefe ? rahmenName(s.stapel[tiefe - 1]) : "";
    if (tiefe > 1 && aufrufParams[idx] && aufrufParams[idx][tiefe - 1] !== undefined) name = `${s.stapel[tiefe - 1].funktion}(${aufrufParams[idx][tiefe - 1]})`;
    let icon = "👉", html = "";
    if (s.ereignis === "call") {
      icon = "📞"; html = `Die Funktion <code>${esc(name)}</code> wird aufgerufen – ein neuer Rahmen kommt <b>oben</b> auf den Stapel. Die Parameter bekommen ihre Werte.`;
    } else if (s.ereignis === "return") {
      icon = "↩️";
      const r = s.rueckgabe ? s.rueckgabe.repr : "None";
      html = name === "Hauptprogramm"
        ? "Das Programm ist am Ende angekommen."
        : `<code>${esc(name)}</code> ist fertig und gibt <code>${esc(r)}</code> zurück. Der Rahmen wird vom Stapel genommen.`;
    } else if (s.ereignis === "exception") {
      icon = "🐞"; html = `In Zeile ${s.zeile} ist ein <b>Fehler</b> aufgetreten.`;
    } else {
      html = (vorher ? `Zeile ${vorher.zeile} wurde ausgeführt. ` : "Das Programm startet. ") + `Als Nächstes ist <b>Zeile ${s.zeile}</b> dran.`;
    }
    if (vorher && (s.ausgabe || "").length > (vorher.ausgabe || "").length) html += " 🖨️ Es wurde etwas ausgegeben.";
    if (istLetzter) {
      if (fehler) { icon = "🐞"; html = `Das Programm wurde wegen eines Fehlers <b>abgebrochen</b>${fehler.zeile ? ` (Zeile ${fehler.zeile})` : ""}.`; }
      else if (!daten.abgebrochen) { icon = "🏁"; html = "<b>Fertig!</b> Das Programm ist komplett durchgelaufen."; }
    }
    return [h("span", { class: "tr-e-icon", text: icon }), h("span", { html })];
  }

  bAnfang.onclick = () => { stop(); zeigen(0); };
  bZurueck.onclick = () => { stop(); zeigen(idx - 1); };
  bVor.onclick = () => { stop(); zeigen(idx + 1); };
  bEnde.onclick = () => { stop(); zeigen(schritte.length - 1); };
  bSpiel.onclick = abspielen;
  regler.addEventListener("input", () => { stop(); zeigen(parseInt(regler.value, 10)); });
  box.tabIndex = -1;
  box.addEventListener("keydown", (e) => {
    if (e.target.matches("input[type=text], textarea, select")) return;
    if (e.key === "ArrowRight" && e.target !== regler) { e.preventDefault(); stop(); zeigen(idx + 1); }
    else if (e.key === "ArrowLeft" && e.target !== regler) { e.preventDefault(); stop(); zeigen(idx - 1); }
    else if (e.key === " " && e.target.tagName !== "BUTTON") { e.preventDefault(); abspielen(); }
    else if (e.key === "Escape" && box.classList.contains("vollbild")) { box.classList.remove("vollbild"); }
  });
  vollBtn.onclick = () => { box.classList.toggle("vollbild"); vollBtn.textContent = box.classList.contains("vollbild") ? "⤡ Klein" : "⛶ Groß"; };
  zeigen(0);
}

function kuerzen(s, n = 18) { s = String(s); return s.length > n ? s.slice(0, n - 1) + "…" : s; }

function konsoleMini(text, alt) {
  const pre = h("pre");
  if (!text) pre.append(h("span", { class: "leer", text: "(noch keine Ausgabe)" }));
  else {
    pre.append(document.createTextNode(alt));
    const neu = text.slice(alt.length);
    if (neu) pre.append(h("span", { class: "neu", text: neu }));
  }
  return h("div", { class: "konsole" }, h("div", { class: "konsole-kopf" }, h("i"), h("i"), h("i"), "Ausgabe"), pre);
}
