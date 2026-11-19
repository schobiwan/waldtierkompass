// Reine Textfunktionen ohne Zugriff auf die Seite (auch in Node testbar)

/** Kleinbuchstaben, Umlaute ausgeschrieben: „Eichhörnchen“ → „eichhoernchen“ */
export const norm = (s) => String(s).toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss");

/** Für die Suche: Umlaute auf den Grundvokal falten, getipptes „ae“ ebenso („Eichhornchen“ = „Eichhoernchen“ = „Eichhörnchen“) */
export const fold = (s) => norm(s || "").replace(/ae/g, "a").replace(/oe/g, "o").replace(/ue/g, "u");

export const escapeHtml = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

/** Zahlenliste aus einem Daten-Attribut: "3,4,5" → [3, 4, 5] */
export const nums = (s) => (s || "").split(",").filter(Boolean).map(Number);

/** Funktion erst ausführen, wenn ms Millisekunden lang kein neuer Aufruf kam; cancel() bricht ab */
export function debounce(fn, ms) {
  let t = 0;
  const run = (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
  run.cancel = () => clearTimeout(t);
  return run;
}
