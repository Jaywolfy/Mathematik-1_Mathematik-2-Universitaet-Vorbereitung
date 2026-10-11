// Gemeinsamer Zustand (Übersicht, Statistik) + Normalisierung der Statistik.

export const store = { uebersicht: null, statistik: null, einstellungen: {}, glossar: null };
const hoerer = new Set();

export function setStatistik(roh) {
  if (!roh) return;
  store.statistik = normStatistik(roh);
  hoerer.forEach(f => { try { f(store.statistik); } catch (e) { console.error(e); } });
}
export function onStatistik(f) { hoerer.add(f); return () => hoerer.delete(f); }

export const LEVEL_STUFEN = [0, 100, 250, 500, 900, 1400, 2000, 2800, 3800, 5000];
export const LEVEL_NAMEN = ["Zahlenneugier", "Bruchsicher", "Termgewandt", "Gleichungsklar", "Funktionsblick",
  "Beweislust", "Matrixkraft", "Grenzwertgespür", "Integralgefühl", "Mathe-Profi"];

const zahl = (...werte) => { for (const w of werte) if (typeof w === "number" && isFinite(w)) return w; return null; };

/** Bringt die Statistik aus fortschritt.statistik() in eine feste Form fürs Frontend. */
export function normStatistik(s) {
  const xp = zahl(s.xp, s.punkte) ?? 0;
  let lv = s.level;
  let level, name, von, bis;
  if (lv && typeof lv === "object") {
    level = zahl(lv.nummer, lv.stufe, lv.level);
    name = lv.titel || lv.name || null;
    von = zahl(lv.xp_start, lv.von, lv.xp_von, lv.min);
    bis = zahl(lv.xp_naechstes, lv.bis, lv.xp_bis, lv.naechstes, lv.max);
  } else {
    level = zahl(lv, s.stufe);
    name = s.level_name || s.level_titel || s.levelname || null;
    von = zahl(s.level_von, s.level_xp_von, s.level_start);
    bis = zahl(s.level_bis, s.level_xp_bis, s.naechstes_level, s.naechstes_level_xp);
  }
  if (level === null || von === null) {
    let i = 0;
    while (i + 1 < LEVEL_STUFEN.length && xp >= LEVEL_STUFEN[i + 1]) i++;
    if (level === null) level = i + 1;
    if (von === null) von = LEVEL_STUFEN[i];
    if (bis === null) bis = LEVEL_STUFEN[i + 1] ?? null;
  }
  if (!name) name = `Level ${level} · ${LEVEL_NAMEN[Math.min(level, 10) - 1] || ""}`;
  else if (!/level/i.test(name)) name = `Level ${level} · ${name}`;
  const anteil = (lv && typeof lv === "object" && typeof lv.fortschritt === "number") ? lv.fortschritt
    : (bis ? Math.max(0, Math.min(1, (xp - von) / (bis - von))) : 1);

  let serie = s.serie;
  if (serie && typeof serie === "object") serie = zahl(serie.tage, serie.anzahl) ?? 0;
  serie = zahl(serie, s.serie_tage) ?? 0;

  const abzeichen = (Array.isArray(s.abzeichen_alle) ? s.abzeichen_alle : Array.isArray(s.abzeichen) ? s.abzeichen : []).map(a => {
    if (typeof a === "string") return { id: a, name: a, icon: "🏅", beschreibung: "", erreicht: true };
    return {
      id: a.id, name: a.name || a.titel || a.id, icon: a.icon || a.emoji || "🏅",
      beschreibung: a.beschreibung || a.text || "", erreicht: a.erreicht ?? a.freigeschaltet ?? a.hat ?? true,
    };
  });

  return {
    roh: s, xp, level, levelName: name, levelVon: von, levelBis: bis, levelAnteil: anteil, serie, abzeichen,
    generatorGeloest: zahl(s.generator_geloest) ?? 0,
    diagnose: s.diagnose || null,
    fragenRichtig: zahl(s.fragen_richtig, s.richtig, s.fragen_geloest) ?? 0,
    fragenGesamt: zahl(s.fragen_gesamt, s.fragen_anzahl) ?? null,
    kapitelFertig: zahl(s.kapitel_abgeschlossen, s.kapitel_fertig) ?? null,
    kapitelGesamt: zahl(s.kapitel_gesamt, s.kapitel_anzahl) ?? null,
    fehlerkiste: zahl(s.fehlerkiste, s.fehlerkiste_anzahl) ?? (Array.isArray(s.fehlerkiste) ? s.fehlerkiste.length : 0),
    faellig: zahl(s.faellig, s.wiederholen_faellig, s.faellige) ?? null,
    besteNote: s.beste_note || null,
    klausuren: s.klausuren || 0,
    teile: Object.fromEntries((Array.isArray(s.teile) ? s.teile : []).map(t => [t.id, t])),
  };
}
