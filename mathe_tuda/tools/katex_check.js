// Entwickler-Werkzeug: prüft alle Formeln (JSON-Liste über stdin) mit dem lokalen KaTeX (throwOnError).
// Wird vom Selbsttest automatisch benutzt, wenn Node installiert ist. Ausgabe: "FEHLER <formel>: <meldung>".
const path = require("path");
const katex = require(path.join(__dirname, "..", "mathe", "web", "static", "vendor", "katex", "katex.min.js"));
const makros = { "\\hl": "\\htmlClass{hl}{#1}", "\\N": "\\mathbb{N}", "\\Z": "\\mathbb{Z}", "\\Q": "\\mathbb{Q}", "\\R": "\\mathbb{R}", "\\C": "\\mathbb{C}" };
let daten = "";
process.stdin.on("data", (c) => { daten += c; });
process.stdin.on("end", () => {
  const formeln = JSON.parse(daten);
  let fehler = 0;
  for (const f of formeln) {
    try {
      katex.renderToString(f.replace(/\\luecke/g, "\\boxed{\\phantom{00}}"), { throwOnError: true, strict: "ignore", macros: { ...makros }, trust: (k) => k.command === "\\htmlClass" });
    } catch (e) { fehler++; console.log(`FEHLER ${f.slice(0, 80)}: ${e.message}`); }
  }
  console.log(`OK ${formeln.length - fehler} von ${formeln.length}`);
});
