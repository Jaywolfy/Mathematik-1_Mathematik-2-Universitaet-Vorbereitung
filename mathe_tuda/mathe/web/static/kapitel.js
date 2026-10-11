// Kapitelansicht: geführter Lernpfad mit Phasen-Stepper und Ergebnis-Bildschirm.
import { h, inline, nurText, lade, ring, konfetti, zaehleHoch, toast, reduziert } from "./util.js";
import { api } from "./api.js";
import { setStatistik } from "./store.js";
import { renderBloecke, renderSeiten } from "./markup.js";
import { frageKarte, TYP_INFO, xpFlug } from "./fragen.js";
import { uebersichtLaden, meisterChip } from "./app.js";

const PHASEN = [
  { id: "verstehen", nr: "1", name: "Verstehen", icon: "📖", text: "Erklärungen mit Bildern und vorgerechneten Beispielen" },
  { id: "ueben", nr: "2", name: "Üben", icon: "🎯", text: "Kurze Fragen direkt zu jeder Idee" },
  { id: "praxis", nr: "3", name: "Praxis", icon: "✏️", text: "Rechnen – vom Leichten bis zum Übungsblatt" },
  { id: "merkzettel", nr: "4", name: "Merkzettel", icon: "📌", text: "Das Wichtigste auf einen Blick" },
];

export async function kapitelAnsicht(main, slug, startSchritt) {
  main.replaceChildren(lade("Kapitel wird geladen …"));
  const daten = await api.get(`/api/kapitel/${encodeURIComponent(slug)}`);
  const k = daten.kapitel;
  document.title = `${nurText(k.titel)} · Mathe für Informatik`;

  // ---- Schritte: Lernziele, Seiten, Fragen, Merkzettel, Ergebnis ----
  const schritte = [{ art: "ziele", phase: "verstehen" }];
  for (const el of daten.elemente) {
    if (el.typ === "erklaerung") {
      (el.seiten || []).forEach((seite, i) => schritte.push({ art: "seite", phase: "verstehen", titel: el.titel, seite, nr: i + 1, von: el.seiten.length }));
    } else if (el.typ === "frage") {
      schritte.push({ art: "frage", phase: el.frage.phase === "praxis" ? "praxis" : "ueben", frage: el.frage });
    } else if (el.typ === "zusammenfassung") {
      schritte.push({ art: "merkzettel", phase: "merkzettel", seiten: el.seiten });
    }
  }
  schritte.push({ art: "ergebnis", phase: "merkzettel" });
  const ERG = schritte.length - 1;
  const status = schritte.map(() => "offen");
  const karten = new Map();
  let idx = -1, xpSumme = 0, wiederholung = null;
  const fragenIdx = schritte.map((s, i) => (s.art === "frage" ? i : -1)).filter(i => i >= 0);

  const f = k.fortschritt || {};
  const kopf = h("header", { class: "kap-kopf" },
    h("span", { class: "gross-icon", "aria-hidden": "true", text: k.icon }),
    h("div", { style: { minWidth: 0 } },
      h("div", { class: "kap-ueber", text: `Kapitel ${k.nummer}` }),
      h("h1", { html: inline(k.titel) }), h("p", { html: inline(k.beschreibung) }),
      h("div", { class: "meta" },
        k.quelle ? h("span", { class: "chip", text: `📚 ${k.quelle}` }) : null,
        h("span", { class: "chip", text: `${k.anzahl?.fragen ?? fragenIdx.length} Aufgaben` }),
        meisterChip(f),
        f.abgeschlossen ? h("span", { class: "chip gruen", text: `✓ abgeschlossen · Bestwert ${f.best}/${f.max}` }) : null,
        k.anzahl?.generatoren ? h("a", { class: "chip primary", href: `#/training/thema/${k.slug}`, text: "⚙️ Endlos üben" }) : null)));
  const stepper = h("nav", { class: "stepper", "aria-label": "Phasen des Kapitels" });
  const stepBtns = PHASEN.map((p, i) => {
    const b = h("button", { class: "step", type: "button" }, h("span", { class: "nr", text: p.nr }), h("span", { class: "lbl", text: p.name }));
    b.onclick = () => {
      const ziel = schritte.findIndex((s, j) => s.phase === p.id && s.art !== "ergebnis" && (status[j] === "offen" || status[j] === "gesehen"));
      const erstes = schritte.findIndex(s => s.phase === p.id && s.art !== "ergebnis");
      zeigen(ziel >= 0 ? ziel : erstes);
    };
    if (i > 0) stepper.append(h("span", { class: "step-trenner", "aria-hidden": "true" }));
    stepper.append(b);
    return b;
  });
  const segmente = h("div", { class: "segmente", role: "group", "aria-label": "Fortschritt im Kapitel" });
  const segs = schritte.map((s, i) => {
    if (s.art === "ergebnis") return null;
    const b = h("button", { class: "segment", type: "button", "aria-label": `Schritt ${i + 1}: ${schrittName(s)}`, title: schrittName(s) });
    b.onclick = () => zeigen(i);
    segmente.append(b);
    return b;
  });
  const buehne = h("div", { "aria-live": "polite" });
  const bZurueck = h("button", { class: "btn", type: "button", text: "← Zurück" });
  const bSkip = h("button", { class: "btn btn-ghost", type: "button", text: "Überspringen" });
  const bWeiter = h("button", { class: "btn btn-primary btn-lg", type: "button", text: "Weiter →" });
  const mitte = h("span", { class: "mitte" });
  main.replaceChildren(h("div", { class: "container" }, kopf, stepper, segmente, buehne, h("div", { class: "kap-nav" }, bZurueck, mitte, bSkip, bWeiter)));

  function schrittName(s) {
    if (s.art === "ziele") return "Lernziele";
    if (s.art === "seite") return nurText(`${s.titel}${s.von > 1 ? ` (${s.nr}/${s.von})` : ""}`);
    if (s.art === "frage") return (TYP_INFO[s.frage.typ] || {}).name || "Frage";
    if (s.art === "merkzettel") return "Merkzettel";
    return "Ergebnis";
  }

  function frageEl(i) {
    const s = schritte[i];
    const karte = frageKarte(s.frage, {
      onFertig: (info) => {
        if (info.ergebnis && info.ergebnis.xp_neu) xpSumme += info.ergebnis.xp_neu;
        if (status[i] === "offen" || status[i] === "uebersprungen") status[i] = info.ok ? "richtig" : "falsch";
        navAktualisieren();
        if (info.ok) setTimeout(() => bWeiter.focus({ preventScroll: true }), 50);
      },
      neueAufgabe: async () => {
        try {
          const r = await api.get(`/api/generator/neu?id=${encodeURIComponent(s.frage.id)}`);
          s.frage = r.frage;
          karten.delete(i);
          zeigen(i, "vor");
        } catch (e) { toast(e.message, "rot"); }
      },
    });
    karte.el._karte = karte;
    return karte.el;
  }

  function schrittElement(i) {
    if (karten.has(i) && schritte[i].art !== "ergebnis") return karten.get(i);
    const s = schritte[i];
    let el;
    if (s.art === "ziele") el = zieleKarte();
    else if (s.art === "seite") {
      el = h("article", { class: "karte erkl-karte" },
        h("div", { class: "erkl-kopf" }, h("span", { class: "chip primary", text: "📖 Verstehen" }), h("h2", { html: inline(s.titel) }),
          s.von > 1 ? h("span", { class: "seiten-punkte", "aria-label": `Seite ${s.nr} von ${s.von}` }, Array.from({ length: s.von }, (_, j) => h("i", { class: j === s.nr - 1 ? "an" : "" }))) : null),
        renderBloecke(s.seite));
    } else if (s.art === "frage") el = frageEl(i);
    else if (s.art === "merkzettel") {
      el = h("article", { class: "karte erkl-karte" },
        h("div", { class: "erkl-kopf" }, h("span", { class: "chip gelb", text: "📌 Merkzettel" }), h("h2", { text: "Das Wichtigste auf einen Blick" })),
        renderSeiten(s.seiten),
        h("p", { class: "antwort-hinweis", style: { marginTop: "18px" }, text: "Diesen Merkzettel findest du jederzeit in der Formelsammlung wieder." }));
    } else el = h("div");
    karten.set(i, el);
    return el;
  }

  function zieleKarte() {
    const anz = k.anzahl || {};
    return h("article", { class: "karte ziele-karte" },
      h("span", { class: "chip primary", text: "🎯 Lernziele" }),
      h("h2", { style: { marginTop: "12px" }, text: "Das lernst du in diesem Kapitel" }),
      h("ul", { class: "ziele-liste" }, (k.lernziele || []).map(z => h("li", { class: f.abgeschlossen ? "erreicht" : "" }, h("span", { class: "haken", "aria-hidden": "true", text: "✓" }), h("span", { html: inline(z) })))),
      (k.warum_bloecke || []).length ? h("aside", { class: "box box-warum" },
        h("div", { class: "box-kopf" }, h("span", { class: "box-icon", "aria-hidden": "true", text: "💻" }), h("div", null, h("span", { class: "box-label", text: "Wozu brauche ich das als Informatiker?" }))),
        renderBloecke(k.warum_bloecke)) : null,
      h("div", { class: "phasen-vorschau" }, PHASEN.map(p => h("div", { class: "phase-kachel" },
        h("span", { class: "p-ico", "aria-hidden": "true", text: p.icon }), h("b", { text: `${p.nr}. ${p.name}` }),
        h("span", { text: p.id === "verstehen" ? `${anz.seiten ?? "?"} Seiten` : p.id === "ueben" ? `${anz.ueben ?? "?"} Fragen` : p.id === "praxis" ? `${anz.praxis ?? "?"} Aufgaben` : "Zusammenfassung" })))));
  }

  function zeigen(i, richtung = null) {
    i = Math.max(0, Math.min(ERG, i));
    if (richtung === null) richtung = i >= idx ? "vor" : "zurueck";
    idx = i;
    const s = schritte[i];
    if (s.art !== "frage" && s.art !== "ergebnis" && status[i] === "offen") status[i] = "gesehen";
    const el = schrittElement(i);
    buehne.replaceChildren(h("div", { class: "schritt-buehne" + (richtung === "zurueck" ? " zurueck" : "") }, el));
    if (s.art === "ergebnis") ergebnisZeigen(el);
    history.replaceState(null, "", `#/kapitel/${k.slug}/${i}`);
    navAktualisieren();
    const oben = buehne.getBoundingClientRect().top + window.scrollY - 80;
    if (window.scrollY > oben) window.scrollTo({ top: Math.max(0, oben), behavior: reduziert() ? "auto" : "smooth" });
    if (s.art === "frage" && el._karte && !beantwortet(i)) setTimeout(() => { try { el._karte.fokus && el._karte.fokus(); } catch { /* egal */ } }, 380);
  }
  const beantwortet = (i) => status[i] === "richtig" || status[i] === "falsch";
  const naechsterIndex = () => {
    if (wiederholung) { const rest = wiederholung.filter(j => j > idx); return rest.length ? rest[0] : ERG; }
    return idx + 1;
  };

  function navAktualisieren() {
    const s = schritte[idx];
    PHASEN.forEach((p, j) => {
      const b = stepBtns[j];
      const vorhanden = schritte.some(x => x.phase === p.id && x.art !== "ergebnis");
      const alleFertig = vorhanden && schritte.every((x, n) => x.phase !== p.id || x.art === "ergebnis" || status[n] !== "offen");
      const aktiv = s.phase === p.id && s.art !== "ergebnis";
      b.classList.toggle("aktiv", aktiv);
      b.classList.toggle("fertig", alleFertig && !aktiv);
      b.disabled = !vorhanden;
      b.querySelector(".nr").textContent = alleFertig && !aktiv ? "✓" : p.nr;
      if (aktiv) b.setAttribute("aria-current", "step"); else b.removeAttribute("aria-current");
    });
    segs.forEach((b, j) => { if (b) b.className = "segment " + (status[j] !== "offen" ? status[j] : "") + (j === idx ? " aktuell" : ""); });
    const frageOffen = s.art === "frage" && !beantwortet(idx);
    bZurueck.disabled = idx === 0;
    bZurueck.hidden = bWeiter.hidden = s.art === "ergebnis";
    bSkip.hidden = !frageOffen;
    bWeiter.disabled = frageOffen;
    const n = naechsterIndex();
    bWeiter.textContent = s.art === "ziele" ? "Los geht's →" : n === ERG ? "Kapitel abschließen ✓" : "Weiter →";
    bWeiter.title = frageOffen ? "Beantworte zuerst die Frage – oder überspringe sie." : "Strg + Enter";
    const nrFrage = fragenIdx.indexOf(idx);
    mitte.textContent = s.art === "ergebnis" ? "" : nrFrage >= 0 ? `Aufgabe ${nrFrage + 1} von ${fragenIdx.length}` : `Schritt ${idx + 1} von ${ERG}`;
  }

  bZurueck.onclick = () => zeigen(idx - 1, "zurueck");
  bWeiter.onclick = () => { if (!bWeiter.disabled) zeigen(naechsterIndex(), "vor"); };
  bSkip.onclick = () => { if (status[idx] === "offen") status[idx] = "uebersprungen"; zeigen(naechsterIndex(), "vor"); };

  const taste = (e) => {
    if (e.defaultPrevented || document.querySelector(".dialog-hg")) return;
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {          // Strg+Enter: nächste Frage / weiter
      if (!bWeiter.hidden && !bWeiter.disabled) { e.preventDefault(); bWeiter.click(); }
      return;
    }
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.target.closest && e.target.closest("input, textarea, select, .puzzle, .plot, .zs-svg, [contenteditable]")) return;
    if (e.key === "ArrowRight" && !bWeiter.hidden && !bWeiter.disabled) { e.preventDefault(); bWeiter.click(); }
    else if (e.key === "ArrowLeft" && !bZurueck.hidden && !bZurueck.disabled) { e.preventDefault(); bZurueck.click(); }
    else if (e.key === "Enter" && e.target === document.body && !bWeiter.hidden && !bWeiter.disabled && schritte[idx].art !== "frage") { e.preventDefault(); bWeiter.click(); }
  };
  document.addEventListener("keydown", taste);

  // ---- Ergebnis ----
  let abschlussLaeuft = false;
  async function ergebnisZeigen(el) {
    const max = fragenIdx.length;
    const punkte = fragenIdx.filter(i => status[i] === "richtig").length;
    const offen = fragenIdx.filter(i => status[i] !== "richtig");
    const pct = max ? punkte / max : 1;
    const titel = pct >= 0.9 ? "Hervorragend! 🏆" : pct >= 0.7 ? "Stark gemacht! 💪" : pct >= 0.5 ? "Gut gemacht! 👍" : "Geschafft – bleib dran! 🌱";
    const xpEl = h("span", { text: "0" });
    const abzeichenSlot = h("div");
    const karte = h("article", { class: "karte ergebnis-karte" },
      h("div", { class: "ergebnis-ring" }, ring(pct, { groesse: 132, dicke: 11, text: `${Math.round(pct * 100)}%`, label: `${punkte} von ${max} richtig` })),
      h("h2", { text: titel }),
      h("p", { class: "unter", html: `Du hast Kapitel ${k.nummer} „${inline(k.titel)}“ abgeschlossen.` }),
      h("div", { class: "ergebnis-zahlen" },
        h("div", { class: "ez" }, h("b", { text: `${punkte} / ${max}` }), h("span", { text: "Aufgaben richtig" })),
        h("div", { class: "ez xp" }, h("b", null, "+", xpEl), h("span", { text: "XP in diesem Kapitel" })),
        h("div", { class: "ez" }, h("b", { text: String(offen.length) }), h("span", { text: "zum Wiederholen" }))),
      abzeichenSlot);
    if ((k.lernziele || []).length) {
      karte.append(h("div", { style: { textAlign: "left", marginTop: "22px" } },
        h("div", { class: "abschnitt-titel", style: { margin: "0 0 8px" }, text: "Das kannst du jetzt" }),
        h("ul", { class: "ziele-liste", style: { margin: 0 } }, k.lernziele.map(z => h("li", { class: "erreicht" }, h("span", { class: "haken", text: "✓" }), h("span", { html: inline(z) }))))));
    }
    if (offen.length) {
      karte.append(h("div", { class: "ergebnis-liste" },
        h("div", { class: "abschnitt-titel", style: { margin: "18px 0 4px" }, text: "Noch nicht richtig" }),
        offen.map(i => {
          const fr = schritte[i].frage;
          const t = nurText(String(fr.frage || "").split("\n")[0]);
          return h("button", { class: "el", type: "button", onclick: () => { karten.delete(i); status[i] = "offen"; wiederholung = [i]; zeigen(i); } },
            h("span", { class: "st", text: status[i] === "falsch" ? "↻" : "⏭" }), h("span", { text: (TYP_INFO[fr.typ] || {}).icon || "❓" }),
            h("span", { class: "el-text", text: t.length > 90 ? t.slice(0, 88) + "…" : t }));
        })));
    }
    const aktionen = h("div", { class: "ergebnis-aktionen" });
    if (offen.length) aktionen.append(h("button", { class: "btn btn-lg", type: "button", text: `↻ Offene wiederholen (${offen.length})`, onclick: () => {
      offen.forEach(i => { karten.delete(i); status[i] = "offen"; });
      wiederholung = offen.slice();
      zeigen(offen[0], "vor");
    } }));
    if (k.anzahl?.generatoren) aktionen.append(h("a", { class: "btn btn-lg", href: `#/training/thema/${k.slug}`, text: "⚙️ Endlos weiterüben" }));
    if (k.naechstes) aktionen.append(h("a", { class: "btn btn-primary btn-lg", href: `#/kapitel/${k.naechstes}`, text: "Nächstes Kapitel →", title: nurText(k.naechstes_titel || "") }));
    aktionen.append(h("a", { class: "btn btn-ghost btn-lg", href: "#/", text: "Zur Übersicht" }));
    karte.append(aktionen);
    el.replaceChildren(karte);
    wiederholung = null;

    if (abschlussLaeuft) return;
    abschlussLaeuft = true;
    try {
      const r = await api.post(`/api/kapitel/${encodeURIComponent(k.slug)}/abschluss`, { punkte, max });
      setStatistik(r.statistik);
      xpSumme += r.xp_neu || 0;
      if (r.xp_neu) xpFlug(r.xp_neu);
      zaehleHoch(xpEl, 0, xpSumme, 1100);
      if (r.neuer_rekord) abzeichenSlot.append(h("p", { class: "chip gruen", style: { marginTop: "14px" }, text: "🎉 Neuer Bestwert!" }));
      if (r.neue_abzeichen && r.neue_abzeichen.length) {
        abzeichenSlot.append(h("div", { class: "abschnitt-titel", style: { justifyContent: "center", margin: "22px 0 4px" }, text: "Neue Abzeichen" }),
          h("div", { class: "neue-abzeichen" }, r.neue_abzeichen.map((a, i) => h("div", { class: "abzeichen", style: { animationDelay: `${0.3 + i * 0.15}s` } },
            h("span", { class: "az-icon", text: a.icon }), h("b", { text: a.titel }), h("span", { text: a.beschreibung || "" })))));
      }
      if ((r.neue_abzeichen && r.neue_abzeichen.length) || pct >= 0.8) konfetti();
      uebersichtLaden().catch(() => {});
    } catch (e) {
      toast("Ergebnis konnte nicht gespeichert werden: " + e.message, "rot");
    } finally { abschlussLaeuft = false; }
  }

  const debug = /[?&](debug|demo|e2e)=/.test(location.search);
  if (Number.isInteger(startSchritt) && startSchritt > ERG && debug) startSchritt = ERG;
  const start = Number.isInteger(startSchritt) && startSchritt >= 0 && startSchritt <= ERG ? startSchritt : 0;
  if (start === ERG && !debug) zeigen(0); else zeigen(start, "vor");
  return () => document.removeEventListener("keydown", taste);
}
