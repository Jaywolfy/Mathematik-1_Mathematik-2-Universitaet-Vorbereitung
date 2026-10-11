// Training: Probeprüfung, Fehlerkiste, Wiederholen (Leitner) – alle mit denselben Fragekarten.
import { h, lade, ring, balken, konfetti, toast, plural, lokal } from "./util.js";
import { api } from "./api.js";
import { setStatistik, store } from "./store.js";
import { frageKarte } from "./fragen.js";
import { uebersichtLaden } from "./app.js";

const MODI = {
  pruefung: { icon: "🎓", titel: "Probeprüfung", text: "Gemischte Fragen aus Tag 1 bis 4 – wie in einer echten Klausur. Am Ende bekommst du eine Note (1,0 bis 5,0). Code-Aufgaben sind nicht dabei." },
  fehlerkiste: { icon: "🧰", titel: "Fehlerkiste", text: "Hier landen alle Fragen, die du falsch beantwortet hast. Beantwortest du sie richtig, fliegen sie raus." },
  wiederholen: { icon: "🔁", titel: "Wiederholen", text: "Karteikasten-Prinzip (Leitner): Fragen, die dir schwerfallen, kommen öfter dran – sichere seltener." },
};

export async function trainingAnsicht(main, modus) {
  const m = MODI[modus];
  if (!m) { main.replaceChildren(h("div", { class: "container fehler-karte", text: "Unbekannter Trainingsmodus." })); return null; }
  document.title = `${m.titel} · Python-Vorkurs`;
  let timer = null;
  const aufraeumen = () => { if (timer) clearInterval(timer); timer = null; };

  if (modus === "pruefung") {
    const anzahlSel = h("select", { class: "feld", style: { width: "auto", padding: "6px 10px" }, "aria-label": "Anzahl der Fragen" },
      [10, 20, 30].map(n => h("option", { value: n, text: `${n} Fragen`, selected: n === 30 })));
    const timerCb = h("input", { type: "checkbox", checked: lokal.get("pruefung_timer", false) || undefined });
    const start = h("button", { class: "btn btn-primary btn-lg", type: "button", text: "Prüfung starten →" });
    const s = store.statistik || {};
    main.replaceChildren(h("div", { class: "container schmal" }, h("div", { class: "karte training-intro" },
      h("span", { class: "gross", "aria-hidden": "true", text: m.icon }), h("h1", { text: m.titel }), h("p", { text: m.text }),
      h("div", { class: "training-optionen" }, anzahlSel,
        h("label", { class: "schalter" }, timerCb, h("span", { text: "⏱ Mit Zeitlimit (1,5 Min. pro Frage)" }))),
      s.besteNote ? h("p", { style: { marginTop: "10px" }, html: `Deine beste Note bisher: <b>${s.besteNote}</b>` }) : null,
      h("div", { style: { marginTop: "18px" } }, start))));
    start.onclick = async () => {
      lokal.set("pruefung_timer", timerCb.checked);
      const n = parseInt(anzahlSel.value, 10);
      main.replaceChildren(lade("Fragen werden zusammengestellt …"));
      const r = await api.get(`/api/training?modus=pruefung&anzahl=${n}`);
      runde(r.fragen, timerCb.checked ? Math.round(n * 90) : null);
    };
    start.focus();
    return aufraeumen;
  }

  main.replaceChildren(lade());
  const r = await api.get(`/api/training?modus=${modus}`);
  if (!r.fragen.length) {
    main.replaceChildren(h("div", { class: "container schmal" }, h("div", { class: "karte training-intro" },
      h("span", { class: "gross", "aria-hidden": "true", text: modus === "fehlerkiste" ? "🧹" : "🌱" }),
      h("h1", { text: modus === "fehlerkiste" ? "Deine Fehlerkiste ist leer!" : "Noch nichts zu wiederholen" }),
      h("p", { text: modus === "fehlerkiste" ? "Super – es gibt gerade keine falsch beantworteten Fragen. Weiter so!" : "Beantworte zuerst ein paar Fragen in den Kapiteln. Dann tauchen sie hier zum Auffrischen auf." }),
      h("div", { style: { marginTop: "18px" } }, h("a", { class: "btn btn-primary", href: "#/", text: "Zur Übersicht" })))));
    return aufraeumen;
  }
  runde(r.fragen, null);
  return aufraeumen;

  /* ---------- Fragerunde ---------- */
  function runde(fragen, sekunden) {
    const status = fragen.map(() => null); // true / false / "skip"
    let i = 0;
    const fortschritt = h("div", { class: "balken" }, h("i"));
    const zaehler = h("span", { class: "chip" });
    const uhr = h("span", { class: "timer", hidden: !sekunden, role: "timer", "aria-label": "Verbleibende Zeit" });
    const buehne = h("div");
    const bSkip = h("button", { class: "btn btn-ghost", type: "button", text: "Überspringen" });
    const bWeiter = h("button", { class: "btn btn-primary btn-lg", type: "button", text: "Weiter →", disabled: true });
    const bAbbruch = h("button", { class: "btn btn-sm btn-ghost", type: "button", text: "Beenden" });
    main.replaceChildren(h("div", { class: "container" },
      h("div", { class: "runde-kopf" }, h("span", { style: { fontSize: "28px" }, "aria-hidden": "true", text: m.icon }), h("h1", { text: m.titel }), zaehler, fortschritt, uhr, bAbbruch),
      buehne, h("div", { class: "kap-nav" }, h("span", { class: "mitte" }), bSkip, bWeiter)));

    if (sekunden) {
      let rest = sekunden;
      const malen = () => { uhr.textContent = `⏱ ${Math.floor(rest / 60)}:${String(rest % 60).padStart(2, "0")}`; uhr.classList.toggle("knapp", rest <= 60); };
      malen();
      timer = setInterval(() => {
        rest--; malen();
        if (rest <= 0) { clearInterval(timer); timer = null; toast("⏱ Die Zeit ist um!"); fertig(); }
        if (!uhr.isConnected) { clearInterval(timer); timer = null; }
      }, 1000);
    }

    function zeigen() {
      const f = fragen[i];
      zaehler.textContent = `Frage ${i + 1} / ${fragen.length}`;
      fortschritt.querySelector("i").style.width = `${(i / fragen.length) * 100}%`;
      const karte = frageKarte(f, {
        kontext: f.kapitel_titel ? `${f.kapitel_icon || ""} ${f.kapitel_titel}`.trim() : null,
        onFertig: (info) => {
          status[i] = !!info.ok;
          bWeiter.disabled = false; bSkip.hidden = true;
          if (info.ok) setTimeout(() => bWeiter.focus({ preventScroll: true }), 50);
        },
      });
      buehne.replaceChildren(h("div", { class: "schritt-buehne" }, karte.el));
      bWeiter.disabled = true; bSkip.hidden = false;
      bWeiter.textContent = i === fragen.length - 1 ? "Auswerten ✓" : "Weiter →";
      window.scrollTo({ top: 0 });
      setTimeout(() => { if (f.typ !== "code") karte.fokus && karte.fokus(); }, 300);
    }
    bWeiter.onclick = () => { if (i < fragen.length - 1) { i++; zeigen(); } else fertig(); };
    bSkip.onclick = () => { status[i] = "skip"; if (i < fragen.length - 1) { i++; zeigen(); } else fertig(); };
    bAbbruch.onclick = () => fertig();
    zeigen();

    async function fertig() {
      if (timer) { clearInterval(timer); timer = null; }
      const max = fragen.length;
      const punkte = status.filter(x => x === true).length;
      const pct = max ? punkte / max : 0;
      let note = null, neueAbzeichen = [];
      if (modus === "pruefung") {
        try {
          const r = await api.post("/api/pruefung/ergebnis", { punkte, max });
          note = r.note; neueAbzeichen = r.neue_abzeichen || [];
          setStatistik(r.statistik);
        } catch (e) { toast(e.message, "rot"); }
      }
      const karte = h("div", { class: "karte ergebnis-karte" },
        note ? h("div", null, h("div", { class: "note-gross", text: note }), h("p", { class: "unter", text: "Deine Note" }))
          : h("div", { class: "ergebnis-ring" }, ring(pct, { groesse: 120, dicke: 10, text: `${Math.round(pct * 100)}%` })),
        h("h2", { text: pct >= 0.8 ? "Sehr stark! 🎉" : pct >= 0.5 ? "Gut gemacht! 👍" : "Dranbleiben – Übung macht den Meister! 🌱" }),
        h("div", { class: "ergebnis-zahlen" },
          h("div", { class: "ez" }, h("b", { text: `${punkte} / ${max}` }), h("span", { text: "richtig" })),
          h("div", { class: "ez" }, h("b", { text: String(status.filter(x => x === false).length) }), h("span", { text: "falsch" })),
          h("div", { class: "ez" }, h("b", { text: String(status.filter(x => x === null || x === "skip").length) }), h("span", { text: "übersprungen" }))),
        neueAbzeichen.length ? h("div", { class: "neue-abzeichen" }, neueAbzeichen.map(a => h("div", { class: "abzeichen" }, h("span", { class: "az-icon", text: a.icon }), h("b", { text: a.titel || a.name }), h("span", { text: a.beschreibung || "" })))) : null,
        modus === "pruefung" ? h("p", { class: "antwort-hinweis", style: { justifyContent: "center", marginTop: "14px" }, text: "Falsch beantwortete Fragen liegen jetzt in deiner Fehlerkiste." }) : null,
        h("div", { class: "ergebnis-aktionen" },
          h("button", { class: "btn btn-primary btn-lg", type: "button", text: modus === "pruefung" ? "Neue Prüfung" : "Nochmal", onclick: () => trainingAnsicht(main, modus) }),
          modus !== "fehlerkiste" && (store.statistik?.fehlerkiste || 0) > 0 ? h("a", { class: "btn btn-lg", href: "#/training/fehlerkiste", text: `🧰 Fehlerkiste (${store.statistik.fehlerkiste})` }) : null,
          h("a", { class: "btn btn-ghost btn-lg", href: "#/", text: "Zur Übersicht" })));
      main.replaceChildren(h("div", { class: "container schmal" }, karte));
      if (pct >= 0.8 || neueAbzeichen.length) konfetti();
      uebersichtLaden().catch(() => {});
    }
  }
}

export { plural, balken };
