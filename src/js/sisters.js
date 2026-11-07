// Schwesterseiten: Sucht jemand nach Vögeln oder Meerestieren, verweisen Startseite und Schnellsuche dorthin
const SITES = {
  meer: { url: "https://meereskompass.de/", name: "Meereskompass", what: "Tiere an Nord- und Ostsee",
    words: ["kueste", "strand", "nordsee", "ostsee", "wattenmeer", "robbe", "seehund", "kegelrobbe", "wal", "schweinswal", "delfin", "delphin", "qualle", "krabbe", "garnele", "muschel", "seestern", "bernstein", "seeigel", "moewe", "seeschwalbe", "austernfischer", "basstoelpel", "kormoran", "eiderente", "papageitaucher", "trottellumme"] },
  vogel: { url: "https://vogelkompass.de/", name: "Vogelkompass", what: "Vögel",
    words: ["vogel", "voegel", "eule", "kauz", "uhu", "specht", "meise", "amsel", "drossel", "fink", "bussard", "falke", "habicht", "sperber", "kraehe", "rabe", "elster", "haeher", "taube", "kuckuck", "zaunkoenig", "rotkehlchen", "kleiber", "schnepfe", "storch", "reiher", "ente", "gans", "schwan", "milan", "adler"] },
};

// Wort trifft genau, als Ende eines zusammengesetzten Worts („Buckelwal“) oder als Anfang ab 5 Buchstaben („Robben“).
// So zählt „Waldmaus“ nicht als „Wal“.
const hits = (t, w) => t === w || t.endsWith(w) || (w.length >= 5 && t.startsWith(w)) || (t.length >= 4 && w.startsWith(t));

/** Schwesterseite zum (normalisierten) Suchbegriff oder null */
export function sisterFor(term) {
  const words = term.split(/\s+/).filter(Boolean);
  for (const s of Object.values(SITES)) if (words.some((t) => s.words.some((w) => hits(t, w)))) return s;
  return null;
}

export const sisterHint = (s) =>
  `${s.what} findest du auf unserer Schwesterseite <a class="linkbtn" href="${s.url}" rel="noopener">${s.name}</a>.`;
