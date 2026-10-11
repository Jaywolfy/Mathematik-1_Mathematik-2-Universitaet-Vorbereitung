// App-Shell: Router, Kopfzeile, Seitenleiste, Dashboard, Theme, Einstellungen, Begrüßung, Pausenhinweis.
import { h, $, inline, nurText, lade, ring, balken, lokal, dialog, bestaetigen, toast, plural, zaehleHoch } from "./util.js";
import { api } from "./api.js";
import { store, setStatistik, onStatistik } from "./store.js";
import { katexDa, texHtml } from "./formel.js";

const params = new URLSearchParams(location.search);
const DEBUG = params.has("debug") || params.has("demo") || params.has("e2e");

if (DEBUG) {
  const melden = (text) => {
    let box = document.querySelector(".debug-fehler");
    if (!box) { box = h("div", { class: "debug-fehler", id: "debug-fehler", role: "alert" }, h("b", { text: "JS-Fehler (Debug-Modus):" })); document.body.append(box); }
    box.append("\n" + text);
  };
  window.addEventListener("error", (e) => melden(`${e.message} @ ${e.filename}:${e.lineno}:${e.colno}`));
  window.addEventListener("unhandledrejection", (e) => melden("Promise: " + (e.reason && (e.reason.stack || e.reason.message) || e.reason)));
}

/* ---------- Theme, Schriftgröße, Animationen ---------- */
const THEMES = ["auto", "hell", "dunkel"];
const THEME_ICON = { auto: "🖥️", hell: "☀️", dunkel: "🌙" };
const THEME_NAME = { auto: "wie das System", hell: "hell", dunkel: "dunkel" };
const SCHRIFTEN = { s: "Klein", m: "Normal", l: "Groß", xl: "Sehr groß" };
let theme = lokal.get("theme", "auto");
const urlTheme = params.get("theme");
if (urlTheme) theme = { dark: "dunkel", light: "hell" }[urlTheme] || urlTheme;
const mq = window.matchMedia("(prefers-color-scheme: dark)");

function themeAnwenden() {
  const dunkel = theme === "dunkel" || (theme === "auto" && mq.matches);
  document.documentElement.setAttribute("data-theme", dunkel ? "dark" : "light");
  const b = $("#theme-btn");
  b.textContent = THEME_ICON[theme] || "🖥️";
  b.title = `Farbschema: ${THEME_NAME[theme]} (klicken zum Wechseln)`;
}
mq.addEventListener("change", themeAnwenden);
function themeSetzen(t, speichern = true) {
  theme = THEMES.includes(t) ? t : "auto";
  lokal.set("theme", theme);
  themeAnwenden();
  if (speichern) api.post("/api/einstellungen", { theme }).catch(() => {});
}
function darstellungAnwenden() {
  const e = store.einstellungen || {};
  document.documentElement.dataset.schrift = e.schrift || lokal.get("schrift", "m");
  document.documentElement.dataset.animation = e.animationen === false ? "aus" : "an";
}
function einstellungSetzen(werte) {
  Object.assign(store.einstellungen, werte);
  if (werte.schrift) lokal.set("schrift", werte.schrift);
  darstellungAnwenden();
  api.post("/api/einstellungen", werte).catch(() => {});
}
$("#theme-btn").addEventListener("click", () => { themeSetzen(THEMES[(THEMES.indexOf(theme) + 1) % THEMES.length]); toast(`Farbschema: ${THEME_NAME[theme]}`); });
themeAnwenden();
document.documentElement.dataset.schrift = lokal.get("schrift", "m");

/* ---------- Kopfzeile ---------- */
let letzteXp = null;
onStatistik((s) => {
  const xpEl = $("#xp-zahl");
  if (letzteXp === null) xpEl.textContent = s.xp; else zaehleHoch(xpEl, letzteXp, s.xp, 700);
  letzteXp = s.xp;
  $("#level-name").textContent = s.levelName;
  $("#level-xp").textContent = s.levelBis ? `${s.xp - s.levelVon} / ${s.levelBis - s.levelVon}` : "max";
  const lb = $("#level-balken");
  lb.querySelector("i").style.width = `${Math.round(s.levelAnteil * 100)}%`;
  lb.setAttribute("aria-valuenow", Math.round(s.levelAnteil * 100));
  $("#serie-zahl").textContent = s.serie;
  $("#serie").classList.toggle("aus", !s.serie);
  $("#serie").title = s.serie ? `Tagesserie: ${plural(s.serie, "Tag", "Tage")} in Folge geübt` : "Noch keine Tagesserie – übe heute, um sie zu starten!";
  const fk = document.querySelector('[data-zahl="fehlerkiste"]');
  if (fk) { fk.textContent = s.fehlerkiste || ""; fk.hidden = !s.fehlerkiste; }
  const wd = document.querySelector('[data-zahl="faellig"]');
  if (wd) { wd.textContent = s.faellig || ""; wd.hidden = !s.faellig; }
});

$("#beenden-btn").addEventListener("click", async () => {
  if (!(await bestaetigen("Lernsystem beenden?", "Dein Fortschritt ist bereits gespeichert. Der Server im Terminal wird beendet.", "Beenden", "Abbrechen", "⏻"))) return;
  try { await api.post("/api/beenden", {}); } catch { /* Server ist evtl. schon weg */ }
  document.body.append(h("div", { class: "beendet" }, h("div", null,
    h("div", { style: { fontSize: "56px" }, text: "👋" }), h("h1", { text: "Bis bald!" }),
    h("p", { text: "Das Lernsystem wurde beendet und dein Fortschritt ist gespeichert." }),
    h("p", { text: "Du kannst dieses Fenster jetzt schließen." }))));
});
$("#einst-btn").addEventListener("click", einstellungenDialog);

function wahlGruppe(werte, aktuell, onwahl, label) {
  const g = h("div", { class: "btn-gruppe", role: "radiogroup", "aria-label": label });
  for (const [wert, text] of werte) {
    g.append(h("button", { class: "btn btn-sm" + (wert === aktuell ? " btn-primary" : ""), type: "button", role: "radio", "aria-checked": String(wert === aktuell),
      text, onclick: (e) => {
        g.querySelectorAll("button").forEach(b => { b.classList.remove("btn-primary"); b.setAttribute("aria-checked", "false"); });
        e.currentTarget.classList.add("btn-primary"); e.currentTarget.setAttribute("aria-checked", "true");
        onwahl(wert);
      } }));
  }
  return g;
}

async function einstellungenDialog() {
  const e = store.einstellungen || {};
  const reset = h("button", { class: "btn btn-sm btn-danger", type: "button", text: "Fortschritt zurücksetzen …" });
  const pause = h("input", { type: "checkbox", checked: e.pause_hinweis !== false ? true : undefined });
  pause.onchange = () => einstellungSetzen({ pause_hinweis: pause.checked });
  const anim = h("input", { type: "checkbox", checked: e.animationen !== false ? true : undefined });
  anim.onchange = () => einstellungSetzen({ animationen: anim.checked });
  const inhalt = h("div", { class: "einst-grid" },
    h("div", null, h("b", { text: "Farbschema" }), wahlGruppe(THEMES.map(t => [t, `${THEME_ICON[t]} ${THEME_NAME[t][0].toUpperCase() + THEME_NAME[t].slice(1)}`]), theme, (t) => themeSetzen(t), "Farbschema")),
    h("div", null, h("b", { text: "Schrift- und Formelgröße" }), wahlGruppe(Object.entries(SCHRIFTEN), e.schrift || lokal.get("schrift", "m"), (s) => einstellungSetzen({ schrift: s }), "Schriftgröße"),
      h("div", { class: "einst-probe", html: "Probe: " + texHtml("\\frac{3}{4} + \\frac{1}{6} = \\frac{11}{12}") })),
    h("label", { class: "schalter" }, anim, h("span", { text: "Animationen (Übergänge, Konfetti)" })),
    h("label", { class: "schalter" }, pause, h("span", { text: `Pausenhinweis nach ${e.pause_minuten || 25} Minuten` })),
    h("div", null, h("b", { text: "Tastenkürzel" }), h("ul", { class: "md-liste klein", html:
      "<li><kbd>Enter</kbd> prüft die Antwort</li><li><kbd>Strg</kbd>+<kbd>Enter</kbd> nächste Frage / weiter</li><li><kbd>←</kbd>/<kbd>→</kbd> Seiten blättern</li><li><kbd>1</kbd>–<kbd>9</kbd> Antwort wählen, <kbd>W</kbd>/<kbd>F</kbd> wahr/falsch</li>" })),
    h("div", null, h("b", { text: "Fortschritt" }), h("p", { class: "d-text", text: "Setzt XP, Abzeichen, Fehlerkiste, Diagnose und alle Ergebnisse zurück." }), h("div", { style: { marginTop: "8px" } }, reset)));
  reset.onclick = async () => {
    if (!(await bestaetigen("Wirklich alles zurücksetzen?", "Alle XP, Abzeichen, Kapitel-Ergebnisse und die Fehlerkiste werden **unwiderruflich** gelöscht.", "Ja, alles löschen", "Abbrechen", "⚠️"))) return;
    try {
      const r = await api.post("/api/fortschritt/zuruecksetzen", { bestaetigt: true });
      setStatistik(r.statistik); toast("Fortschritt zurückgesetzt.");
      await uebersichtLaden(); route();
    } catch (err) { toast(err.message, "rot"); }
  };
  await dialog({ titel: "Einstellungen", icon: "⚙️", inhalt, knoepfe: [{ text: "Schließen", wert: true, klasse: "btn-primary" }] });
}

/* ---------- Pausenhinweis (Pomodoro) ---------- */
let aktiveSekunden = 0;
setInterval(() => {
  if (document.hidden) return;
  aktiveSekunden++;
  const e = store.einstellungen || {};
  const grenze = (e.pause_minuten || 25) * 60;
  if (e.pause_hinweis !== false && aktiveSekunden >= grenze && !document.querySelector(".dialog-hg")) {
    aktiveSekunden = 0;
    dialog({ titel: "Zeit für eine kurze Pause?", icon: "☕", text: `Du lernst seit ${e.pause_minuten || 25} Minuten. Steh kurz auf, trink etwas, schau aus dem Fenster. Fünf Minuten Pause helfen dem Gehirn, das Gelernte zu speichern.`,
      knoepfe: [{ text: "Hinweis abschalten", wert: "aus", klasse: "btn-ghost" }, { text: "Weiterlernen", wert: true, klasse: "btn-primary" }] })
      .then(w => { if (w === "aus") einstellungSetzen({ pause_hinweis: false }); });
  }
}, 1000);

/* ---------- Glossar-Tooltips ---------- */
let tip = null;
async function glossarLaden() {
  if (!store.glossar) {
    const r = await api.get("/api/glossar");
    store.glossar = new Map();
    for (const e of r.eintraege) { store.glossar.set(e.begriff.toLowerCase(), e); for (const s of e.synonyme || []) store.glossar.set(s.toLowerCase(), e); }
  }
  return store.glossar;
}
async function tooltipZeigen(ziel) {
  const g = await glossarLaden();
  const e = g.get(String(ziel.dataset.begriff || "").toLowerCase());
  if (!tip) { tip = h("div", { class: "glossar-tip", role: "tooltip", id: "glossar-tip" }); document.body.append(tip); }
  tip.replaceChildren(e
    ? h("div", null, h("b", { html: inline(e.begriff) }), h("p", { html: inline(e.erklaerung) }), e.beispiel ? h("p", { class: "tip-beispiel", html: "Beispiel: " + inline(e.beispiel) }) : null,
      h("a", { href: `#/glossar?q=${encodeURIComponent(e.begriff)}`, text: "Im Glossar ansehen →" }))
    : h("div", { text: "Diesen Begriff gibt es (noch) nicht im Glossar." }));
  const r = ziel.getBoundingClientRect();
  tip.hidden = false;
  const breite = Math.min(340, window.innerWidth - 24);
  tip.style.width = breite + "px";
  tip.style.left = Math.max(12, Math.min(window.innerWidth - breite - 12, r.left + r.width / 2 - breite / 2)) + "px";
  const unten = r.bottom + 8 + tip.offsetHeight < window.innerHeight;
  tip.style.top = (unten ? r.bottom + 8 : r.top - tip.offsetHeight - 8) + window.scrollY + "px";
  ziel.setAttribute("aria-describedby", "glossar-tip");
}
const tooltipWeg = () => { if (tip) tip.hidden = true; };
document.addEventListener("mouseover", (e) => { const g = e.target.closest && e.target.closest(".glossar"); if (g) tooltipZeigen(g); });
document.addEventListener("mouseout", (e) => { if (e.target.closest && e.target.closest(".glossar") && !(e.relatedTarget && e.relatedTarget.closest && e.relatedTarget.closest(".glossar-tip"))) setTimeout(() => { if (!document.querySelector(".glossar-tip:hover")) tooltipWeg(); }, 250); });
document.addEventListener("focusin", (e) => { if (e.target.classList && e.target.classList.contains("glossar")) tooltipZeigen(e.target); });
document.addEventListener("click", (e) => {
  const g = e.target.closest && e.target.closest(".glossar");
  if (g) { e.preventDefault(); tooltipZeigen(g); } else if (!(e.target.closest && e.target.closest(".glossar-tip"))) tooltipWeg();
});
document.addEventListener("keydown", (e) => { if (e.key === "Escape") tooltipWeg(); });

/* ---------- Seitenleiste ---------- */
const leiste = $("#seitenleiste");
$("#menue-btn").addEventListener("click", () => {
  const offen = document.body.classList.toggle("leiste-offen");
  $("#menue-btn").setAttribute("aria-expanded", String(offen));
});
document.addEventListener("click", (e) => {
  if (document.body.classList.contains("leiste-offen") && !leiste.contains(e.target) && !e.target.closest("#menue-btn")) document.body.classList.remove("leiste-offen");
});

export async function uebersichtLaden() {
  const u = await api.get("/api/uebersicht");
  store.uebersicht = u;
  store.einstellungen = u.einstellungen || {};
  if (!urlTheme && store.einstellungen.theme && store.einstellungen.theme !== theme && lokal.get("theme", null) === null) themeSetzen(store.einstellungen.theme, false);
  darstellungAnwenden();
  setStatistik(u.statistik);
  seitenleisteZeichnen();
  return u;
}

export function alleKapitel() {
  return (store.uebersicht?.teile || []).flatMap(t => t.kapitel.map(k => ({ ...k, teilTitel: t.titel, teilId: t.id })));
}

const MEISTER = { neu: ["", "neu"], angefangen: ["🌱", "angefangen"], sicher: ["🌿", "sicher"], gemeistert: ["🌳", "gemeistert"] };
export function meisterChip(f) {
  const [icon, name] = MEISTER[f?.meister_stufe || "neu"];
  if (!icon) return null;
  return h("span", { class: `chip meister ${f.meister_stufe}`, title: `Meisterschaft ${Math.round((f.meisterschaft || 0) * 100)} %: aus Trefferquote und Karteikasten-Stufe`, text: `${icon} ${name}` });
}

function seitenleisteZeichnen() {
  const u = store.uebersicht;
  const s = store.statistik || {};
  const zu = lokal.get("teile_zu", []);
  const navLink = (href, icon, text, zahlName = null) => h("a", { class: "nav-link", href, "data-route": href },
    h("span", { class: "ico", "aria-hidden": "true", text: icon }), h("span", { text }),
    zahlName ? h("span", { class: "zahl", "data-zahl": zahlName, hidden: !s[zahlName], text: s[zahlName] || "" }) : null);
  const kinder = [h("div", { class: "nav-haupt" },
    navLink("#/", "🏠", "Übersicht"),
    navLink("#/diagnose", "🧭", "Diagnosetest"),
    navLink("#/training/wiederholen", "🔁", "Wiederholen", "faellig"),
    navLink("#/training/fehlerkiste", "🧰", "Fehlerkiste", "fehlerkiste"),
    navLink("#/training/klausur", "🎓", "Probeklausur"),
    navLink("#/formelsammlung", "📋", "Formelsammlung"),
    navLink("#/glossar", "📖", "Glossar"),
    navLink("#/spielwiese", "🧪", "Spielwiese"))];
  for (const t of u?.teile || []) {
    const fertig = t.kapitel.filter(k => k.fortschritt?.abgeschlossen).length;
    const kurz = t.titel.split(" – ")[0];
    const gruppe = h("div", { class: "nav-teil" + (zu.includes(t.id) ? " zu" : "") });
    const knopf = h("button", { type: "button", "aria-expanded": String(!zu.includes(t.id)), title: t.titel },
      h("span", { text: kurz }), h("span", { class: "teil-zaehler", text: `${fertig}/${t.kapitel.length}` }), h("span", { class: "pfeil", "aria-hidden": "true", text: "▼" }));
    knopf.onclick = () => {
      gruppe.classList.toggle("zu");
      const liste = lokal.get("teile_zu", []).filter(x => x !== t.id);
      if (gruppe.classList.contains("zu")) liste.push(t.id);
      lokal.set("teile_zu", liste);
      knopf.setAttribute("aria-expanded", String(!gruppe.classList.contains("zu")));
    };
    gruppe.append(knopf, h("div", { class: "nav-kapitel" }, t.kapitel.map(k => {
      const f = k.fortschritt || {};
      return h("a", { class: "kap-link", href: `#/kapitel/${k.slug}`, "data-route": `#/kapitel/${k.slug}`, title: nurText(k.titel) },
        h("span", { class: "kap-icon", "aria-hidden": "true", text: k.icon }),
        h("span", { class: "kap-titel" }, h("span", { class: "kap-nr", text: `${k.nummer}.` }), " ", h("span", { html: inline(k.titel) })),
        ring(f.meisterschaft || f.fortschritt || 0, { groesse: 22, dicke: 3, fertig: f.meister_stufe === "gemeistert", label: `Meisterschaft ${Math.round((f.meisterschaft || 0) * 100)} Prozent` }));
    })));
    kinder.push(gruppe);
  }
  leiste.replaceChildren(...kinder);
  aktivMarkieren();
}

function aktivMarkieren() {
  const hash = (location.hash || "#/").split("?")[0];
  leiste.querySelectorAll("[data-route]").forEach(a => {
    const r = a.dataset.route;
    const aktiv = r === "#/" ? (hash === "#/" || hash === "#" || hash === "") : (hash === r || hash.startsWith(r + "/"));
    a.classList.toggle("aktiv", aktiv);
    if (aktiv) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
  });
}

/* ---------- Dashboard ---------- */
function gruss() {
  const std = new Date().getHours();
  return std < 11 ? "Guten Morgen" : std < 18 ? "Hallo" : "Guten Abend";
}

export function naechstesKapitel() {
  const alle = alleKapitel();
  const empf = store.statistik?.diagnose?.empfehlung;
  return alle.find(k => !k.fortschritt?.abgeschlossen && (k.fortschritt?.fragen_richtig || 0) > 0)
    || (empf && alle.find(k => k.slug === empf && !k.fortschritt?.abgeschlossen))
    || alle.find(k => !k.fortschritt?.abgeschlossen) || alle[0];
}

function dashboard(main) {
  const u = store.uebersicht, s = store.statistik;
  const alle = alleKapitel();
  const naechstes = naechstesKapitel();
  const angefangen = (s.xp || 0) > 0;
  const c = h("div", { class: "container" });
  c.append(h("div", { class: "gruss", style: { marginBottom: "22px" } },
    h("h1", { text: `${gruss()}! 👋` }),
    h("p", { text: angefangen ? "Schön, dass du wieder da bist. Kleine Schritte jeden Tag bringen dich am weitesten." : "Willkommen! Hier lernst du die Mathe für dein Informatikstudium – von den Brüchen bis zu Eigenwerten und Integralen. Schritt für Schritt, ohne dass etwas vorausgesetzt wird." })));

  if (!alle.length) { c.append(h("div", { class: "leer-hinweis", text: "Noch keine Kapitel vorhanden." })); main.replaceChildren(c); return; }
  const nf = naechstes?.fortschritt || {};
  const weiter = h("a", { class: "weiter-karte", href: `#/kapitel/${naechstes.slug}` },
    h("span", { class: "deko", "aria-hidden": "true", text: naechstes.icon }),
    h("span", { class: "wk-label", text: angefangen ? "Weiterlernen" : "Hier geht's los" }),
    h("span", { class: "wk-titel" }, h("span", { class: "wk-icon", "aria-hidden": "true", text: naechstes.icon }),
      h("span", null, h("span", { class: "wk-teil", text: `Kapitel ${naechstes.nummer} · ${naechstes.teilTitel.split(" – ")[0]}` }), h("span", { html: inline(naechstes.titel) }))),
    h("span", { class: "wk-text", html: inline(naechstes.beschreibung) }),
    h("span", { class: "wk-fuss" }, balken(nf.fortschritt || 0), h("span", { class: "wk-btn", text: (nf.fragen_richtig || 0) > 0 ? "Fortsetzen →" : "Starten →" })));
  const gk = h("div", { class: "karte gruss-karte" },
    h("div", { style: { display: "flex", gap: "16px", alignItems: "center" } },
      ring(s.levelAnteil, { groesse: 72, dicke: 7, text: String(s.level), label: `Level ${s.level}` }),
      h("div", null, h("div", { class: "lv-name", text: s.levelName }),
        h("div", { class: "lv-rest", text: s.levelBis ? `Noch ${s.levelBis - s.xp} XP bis Level ${s.level + 1}` : "Höchstes Level erreicht – stark!" }))),
    h("div", { class: "mini-stats" },
      h("div", { class: "mini-stat" }, h("b", { text: s.xp }), h("span", { text: "XP gesamt" })),
      h("div", { class: "mini-stat" }, h("b", { text: `🔥 ${s.serie}` }), h("span", { text: s.serie === 1 ? "Tag in Folge" : "Tage in Folge" })),
      h("div", { class: "mini-stat" }, h("b", { text: `${s.kapitelFertig ?? 0}/${s.kapitelGesamt ?? alle.length}` }), h("span", { text: "Kapitel fertig" }))));
  c.append(h("div", { class: "hero" }, weiter, gk));

  if (!s.diagnose) {
    c.append(h("div", { class: "karte diagnose-band" }, h("span", { class: "gross", "aria-hidden": "true", text: "🧭" }),
      h("div", null, h("b", { text: "Wo stehst du gerade?" }), h("p", { text: "Der Diagnosetest (25 kurze Aufgaben, etwa 20 Minuten) zeigt dir, wo du am besten einsteigst. Freiwillig – du kannst auch direkt mit Kapitel 1 anfangen." })),
      h("a", { class: "btn btn-primary", href: "#/diagnose", text: "Diagnosetest starten" })));
  }

  c.append(h("h2", { class: "abschnitt-titel", text: "Dein Weg" }));
  c.append(h("div", { class: "tage-grid" }, (u.teile || []).map(t => {
    const st = s.teile[t.id] || {};
    const fertig = t.kapitel.filter(k => k.fortschritt?.abgeschlossen).length;
    const ziel = t.kapitel.find(k => !k.fortschritt?.abgeschlossen) || t.kapitel[0];
    const anteil = st.fortschritt ?? 0;
    const [kurz, rest] = t.titel.split(" – ");
    return h("a", { class: "karte tag-karte", href: `#/kapitel/${ziel.slug}` },
      ring(anteil, { groesse: 58, dicke: 6, text: `${Math.round(anteil * 100)}%`, fertig: fertig === t.kapitel.length && fertig > 0 }),
      h("div", { style: { minWidth: 0 } }, h("h3", { text: kurz }), h("p", { text: rest || t.untertitel || "" }),
        h("div", { class: "tag-zahl", text: `${fertig} von ${t.kapitel.length} Kapiteln · Meisterschaft ${Math.round((st.meisterschaft || 0) * 100)} %` }),
        h("div", { class: "meister-balken", title: "Meisterschaft: Trefferquote und Karteikasten-Stufe" }, balken(st.meisterschaft || 0, "gruen"))));
  })));

  c.append(h("h2", { class: "abschnitt-titel", text: "Trainieren & Nachschlagen" }));
  const kachel = (href, icon, farbe, titel, text, zahl = null) => h("a", { class: "karte schnell", href },
    h("span", { class: "s-icon", style: { background: farbe }, "aria-hidden": "true", text: icon }), h("b", { text: titel }), h("span", { text }),
    zahl ? h("span", { class: "chip primary badge-zahl", text: zahl }) : null);
  c.append(h("div", { class: "schnell-grid" },
    kachel("#/training/wiederholen", "🔁", "var(--success-soft)", "Wiederholen", "Karteikasten: fällige Aufgaben auffrischen", s.faellig || null),
    kachel("#/training/fehlerkiste", "🧰", "var(--warn-soft)", "Fehlerkiste", s.fehlerkiste ? "Noch offene Aufgaben in Ruhe nachholen" : "Noch leer – sehr gut!", s.fehlerkiste || null),
    kachel("#/training/klausur", "🎓", "var(--primary-soft)", "Probeklausur", "Mit Zeitlimit, Punkten und Note"),
    kachel("#/formelsammlung", "📋", "var(--info-soft)", "Formelsammlung", "Alle Merkzettel – durchsuchbar, druckbar"),
    kachel("#/glossar", "📖", "var(--warm-soft)", "Glossar", "Alle Fachbegriffe mit Beispiel"),
    kachel("#/spielwiese", "🧪", "var(--surface-3)", "Spielwiese", "Plotter, Matrix-, Bruch- und LGS-Rechner")));

  c.append(h("h2", { class: "abschnitt-titel", text: "Statistik" }));
  const stat = (icon, wert, text) => h("div", { class: "karte stat" }, h("span", { class: "st-icon", "aria-hidden": "true", text: icon }), h("div", null, h("b", { text: wert }), h("span", { text })));
  c.append(h("div", { class: "statistik-grid" },
    stat("✅", `${s.fragenRichtig}${s.fragenGesamt ? " / " + s.fragenGesamt : ""}`, "Aufgaben richtig gelöst"),
    stat("⚙️", String(s.generatorGeloest), "Übungsmaschinen-Aufgaben gelöst"),
    stat("🎓", s.besteNote || "–", s.klausuren ? `Beste Note (${plural(s.klausuren, "Klausur", "Klausuren")})` : "Noch keine Probeklausur"),
    stat("🏅", `${s.abzeichen.filter(a => a.erreicht).length} / ${s.abzeichen.length}`, "Abzeichen gesammelt")));

  c.append(h("h2", { class: "abschnitt-titel", text: "Abzeichen" }));
  c.append(h("div", { class: "abzeichen-grid" }, s.abzeichen.map(a =>
    h("div", { class: "karte abzeichen" + (a.erreicht ? "" : " gesperrt"), title: a.erreicht ? "Erreicht!" : "Noch gesperrt" },
      h("span", { class: "az-icon", "aria-hidden": "true", text: a.icon }), h("b", { text: a.name }), h("span", { text: a.beschreibung }),
      h("span", { class: "sr-only", text: a.erreicht ? "erreicht" : "noch gesperrt" })))));
  c.append(h("div", { class: "einstellungen-zeile" },
    h("button", { class: "btn btn-sm btn-ghost", type: "button", text: "⚙️ Einstellungen", onclick: einstellungenDialog }),
    h("span", { text: katexDa() ? "Alles läuft lokal auf deinem Computer – ohne Internet." : "Hinweis: Die Formelschrift (KaTeX) fehlt, Formeln erscheinen als einfacher Text." })));
  main.replaceChildren(c);
}

async function begruessung() {
  if (store.einstellungen?.begruessung_gesehen || params.has("e2e") || params.has("demo")) return;
  const w = await dialog({ titel: "Willkommen!", icon: "👋",
    text: "Schön, dass du da bist! Dieses Programm bringt dich Schritt für Schritt von den Grundlagen (Brüche, Klammern, Gleichungen) bis zu Mathe 1 und Mathe 2 an der Uni. Nichts wird vorausgesetzt.\n\nMagst du mit einem kurzen **Diagnosetest** herausfinden, wo du am besten einsteigst? Er ist freiwillig und dauert etwa 20 Minuten.",
    knoepfe: [{ text: "Direkt mit Kapitel 1 starten", wert: "start", klasse: "btn-ghost" }, { text: "Diagnosetest machen", wert: "diagnose", klasse: "btn-primary" }] });
  einstellungSetzen({ begruessung_gesehen: true });
  if (w === "diagnose") location.hash = "#/diagnose";
  else if (w === "start") { const k = alleKapitel()[0]; if (k) location.hash = `#/kapitel/${k.slug}`; }
}

/* ---------- Router ---------- */
let aufraeumen = null, routeZaehler = 0;

async function route() {
  const nr = ++routeZaehler;
  if (typeof aufraeumen === "function") { try { aufraeumen(); } catch { /* egal */ } }
  aufraeumen = null;
  document.body.classList.remove("leiste-offen");
  tooltipWeg();
  const [pfad, query] = (location.hash.replace(/^#/, "") || "/").split("?");
  const teile = pfad.split("/").filter(Boolean).map(decodeURIComponent);
  const q = new URLSearchParams(query || "");
  const main = $("#main");
  aktivMarkieren();
  try {
    if (!store.uebersicht) { main.replaceChildren(lade()); await uebersichtLaden(); }
    if (nr !== routeZaehler) return;
    const [a, b, c] = teile;
    window.scrollTo(0, 0);
    if (!a) { document.title = "Übersicht · Mathe für Informatik"; dashboard(main); begruessung(); }
    else if (a === "kapitel" && b) {
      const { kapitelAnsicht } = await import("./kapitel.js");
      aufraeumen = await kapitelAnsicht(main, b, c ? parseInt(c, 10) : null);
    } else if (a === "training") {
      const { trainingAnsicht } = await import("./training.js");
      aufraeumen = await trainingAnsicht(main, b || "wiederholen", c);
    } else if (a === "diagnose") {
      const { diagnoseAnsicht } = await import("./training.js");
      aufraeumen = await diagnoseAnsicht(main);
    } else if (a === "formelsammlung" || a === "glossar" || a === "spielwiese" || a === "demo") {
      const seiten = await import("./seiten.js");
      aufraeumen = await seiten[a](main, b, q);
    } else {
      main.replaceChildren(h("div", { class: "container leer-hinweis" }, h("span", { class: "gross", text: "🧭" }), h("p", { text: "Diese Seite gibt es nicht." }), h("a", { class: "btn btn-primary", href: "#/", text: "Zur Übersicht" })));
    }
    if (location.hash && !location.hash.startsWith("#/kapitel")) main.focus({ preventScroll: true });
  } catch (e) {
    if (!e.status) console.error(e);
    main.replaceChildren(h("div", { class: "container" }, h("div", { class: "fehler-karte", role: "alert" },
      h("b", { text: "Da ist etwas schiefgegangen. " }), e.message,
      h("div", { style: { marginTop: "10px" } }, h("button", { class: "btn btn-sm", type: "button", text: "Neu laden", onclick: () => location.reload() })))));
  }
}

export { route, einstellungenDialog };
window.addEventListener("hashchange", route);

if (params.get("demo") && !location.hash) location.replace(`#/demo/${params.get("demo")}`);
else route();
if (params.has("e2e")) import("./e2e.js").then(m => m.e2eStarten(params)).catch(e => console.error(e));
