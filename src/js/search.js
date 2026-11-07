// Artsuche für die Schnellsuche, übernommen vom Vogelkompass: Namen zuerst, dann Doppelgänger, dann Merkmale.
// Mehrere Wörter in beliebiger Reihenfolge, Wortendungen und Umlaute egal („Eichhoernchen“, „nachtaktive Marder“).

export const fold = (t) => String(t || "").toLowerCase()
  .replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss");

const STOP = new Set(["mit", "und", "oder", "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "einem", "einer",
  "am", "im", "an", "in", "auf", "von", "vom", "zum", "zur"]);

/** Wortstamm: eine typische Endung abschneiden, mindestens drei Buchstaben bleiben */
const stem = (w) => { const s = w.replace(/(en|er|es|em|e|s|n)$/, ""); return s.length >= 3 ? s : w; };

export const searchWords = (q) => (fold(q).match(/[a-z0-9]+/g) || []).filter((w) => !STOP.has(w)).map(stem);

export const prepare = (names, alt, marks) => ({ names: fold(names), alt: fold(alt), marks: marks.filter(Boolean).map(fold) });

/**
 * Rang eines Treffers, kleiner ist besser; -1 = kein Treffer.
 * 0 Name beginnt mit der Suche · 1 Name enthält sie · 2 alle Wörter im Namen
 * 3 Doppelgänger · 4 alle Wörter in einem Merkmal (Aussehen, Gruppe, Lebensraum)
 * 5 alle Wörter irgendwo in Name und Merkmalen zusammen
 */
export function rank(e, query) {
  const q = fold(String(query || "").trim());
  if (!q) return 0;
  if (e.names.split(" ").some((n) => n.startsWith(q))) return 0;
  if (e.names.includes(q)) return 1;
  const words = searchWords(q);
  if (!words.length) return -1;
  const all = (t) => words.every((w) => t.includes(w));
  if (all(e.names)) return 2;
  if (e.alt && (e.alt.includes(q) || all(e.alt))) return 3;
  if (e.marks.some(all)) return 4;
  // Wörter über Name und Merkmale verteilt, z. B. „Marder nachtaktiv“
  if (all([e.names, e.alt, ...e.marks].join(" "))) return 5;
  return -1;
}

export function distance(a, b) {
  const row = Array.from({ length: b.length + 1 }, (_, i) => i);
  for (let i = 1; i <= a.length; i++) {
    let prev = row[0]; row[0] = i;
    for (let j = 1; j <= b.length; j++) {
      const tmp = row[j];
      row[j] = Math.min(row[j] + 1, row[j - 1] + 1, prev + (a[i - 1] === b[j - 1] ? 0 : 1));
      prev = tmp;
    }
  }
  return row[b.length];
}

/** Ähnlichster Name bei Tippfehlern („Eichhörnschen“ → „Eichhörnchen“), sonst null */
export function suggest(query, names) {
  const q = fold(String(query || "").trim());
  if (q.length < 3) return null;
  let best = null, bestD = Infinity;
  for (const n of names) {
    const f = fold(n);
    // ganzer Name oder gleich langer Anfang („Feuersala“ → „Feuersalamander“)
    const d = Math.min(distance(q, f), distance(q, f.slice(0, q.length + 1)) + (f.length > q.length + 1 ? 1 : 0));
    if (d < bestD) { bestD = d; best = n; }
  }
  return bestD <= Math.max(1, Math.floor(q.length / 4)) ? best : null;
}
