// Dünne Schicht über fetch: JSON rein, JSON raus, deutsche Fehlermeldungen.

async function anfrage(pfad, optionen = {}) {
  let antwort;
  try {
    antwort = await fetch(pfad, { cache: "no-store", ...optionen });
  } catch (e) {
    throw new Error("Keine Verbindung zum Lernquiz-Server. Läuft das Programm noch im Terminal?");
  }
  let daten = null;
  try { daten = await antwort.json(); } catch { daten = null; }
  if (!antwort.ok) {
    const meldung = (daten && daten.fehler) || `Serverfehler (${antwort.status})`;
    const err = new Error(meldung);
    err.status = antwort.status;
    throw err;
  }
  return daten ?? {};
}

export const api = {
  get: (pfad) => anfrage(pfad),
  post: (pfad, body = {}) => anfrage(pfad, {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify(body),
  }),
};
