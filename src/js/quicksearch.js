// Schnellsuche auf jeder Seite (wie beim Vogelkompass): Knopf „Suchen“ in der Leiste oder Taste „/“.
// Auf der Startseite springt sie stattdessen zum Suchfeld im Kopfbereich.
import { $, escapeHtml, focusEl, IDX } from "./util.js";
import { prepare, rank, suggest, fold } from "./search.js";
import { sisterFor, sisterHint } from "./sisters.js";

const ROOT = document.documentElement.dataset.root || "./";
const dlg = $("sdlg"), btn = $("navsearch"), sq = $("sq"), list = $("sresults"), more = $("smore"), moreLink = $("smore-link"), status = $("sstatus");
const home = $("hq") || $("q"); // Suchfeld der Startseite

let entries = null;
async function data() {
  if (entries) return entries;
  try {
    const rows = await (await fetch(`${ROOT}search.json`)).json();
    // Tiere: [Name, Schlüssel, Namen, Doppelgänger, Merkmale]; Seiten zusätzlich [Adresse, Art der Seite, Symbol]
    entries = rows.map(([name, key, names, alt, marks, href, kind, icon]) =>
      ({ name, key, href: href ?? `arten/${key}/`, kind, icon, e: prepare(names, alt, marks.split("|")) }));
  } catch { entries = null; return []; } // offline: beim nächsten Öffnen erneut versuchen
  return entries;
}

let seq = 0;
async function results() {
  const q = sq.value.trim(), my = ++seq;
  if (!q) { list.innerHTML = ""; more.hidden = true; status.textContent = ""; return; }
  const all = await data();
  if (my !== seq) return; // eine neuere Eingabe ist schon unterwegs
  if (!all.length) { list.innerHTML = '<li class="snone">Die Suche ist gerade nicht erreichbar.</li>'; status.textContent = "Die Suche ist gerade nicht erreichbar."; return; }
  // Tiere vor Seiten, dann nach Rang und Name
  let hits = all.map((x) => ({ ...x, r: rank(x.e, q) })).filter((x) => x.r >= 0)
    .sort((a, b) => (a.kind ? 1 : 0) - (b.kind ? 1 : 0) || a.r - b.r || a.name.localeCompare(b.name, "de"));
  let fuzzyHit = false;
  const sister = !hits.length && sisterFor(fold(q));
  if (!hits.length && !sister) {
    // Tippfehler („Wildscwein“): den ähnlichsten Namen gleich als Treffer zeigen
    const g = suggest(q, all.map((x) => x.name));
    const hit = g && all.find((x) => x.name === g);
    if (hit) { hits = [{ ...hit, r: 9 }]; fuzzyHit = true; }
  }
  const note = (x) => x.r === 9 ? "ähnliche Schreibweise" : x.kind ? x.kind : x.r === 3 ? "ähnelt der gesuchten Art" : x.r >= 4 ? "passt zu den Merkmalen" : "";
  const pic = (x) => x.icon ? `<span class="sico">${x.icon}</span>`
    : `<img src="${ROOT}photos/${x.key}-400.webp" alt="" width="48" height="38" loading="lazy">`;
  if (!hits.length) {
    list.innerHTML = `<li class="snone">Nichts gefunden.${sister ? " " + sisterHint(sister) : ""}</li>`;
  } else {
    list.innerHTML = hits.slice(0, 8).map((x) =>
      `<li><a href="${ROOT}${x.href}${IDX}">${pic(x)}${escapeHtml(x.name)}${note(x) ? `<span>${note(x)}</span>` : ""}</a></li>`).join("");
  }
  const animalHits = hits.filter((x) => !x.kind).length;
  more.hidden = animalHits <= 8 || fuzzyHit;
  // Kurze Ansage für Screenreader statt der ganzen Liste
  status.textContent = hits.length ? `${hits.length} Treffer${fuzzyHit ? " bei ähnlicher Schreibweise" : ""}${hits.length > 8 ? ", die ersten 8 werden gezeigt" : ""}` : "Nichts gefunden";
  moreLink.href = `${ROOT}${IDX}?q=${encodeURIComponent(q)}#arten`;
}

function openSearch() {
  if (home) { // Startseite: das vorhandene Suchfeld über der Liste nutzen
    home.scrollIntoView({ block: "center" }); focusEl(home); return;
  }
  if (!dlg) return;
  dlg.showModal(); sq.focus(); results();
}

btn?.addEventListener("click", openSearch);
$("sclose")?.addEventListener("click", () => dlg.close());
dlg?.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
let t = 0;
sq?.addEventListener("input", () => { clearTimeout(t); t = window.setTimeout(results, 100); });
// Escape schließt das Fenster sofort, statt erst das Feld zu leeren
sq?.addEventListener("keydown", (e) => { if (e.key === "Escape") { e.preventDefault(); dlg.close(); } });
$("sform")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  await results();
  const links = list.querySelectorAll("a");
  location.href = links.length === 1 ? links[0].href : moreLink.href;
});
// Tastenkürzel „/“ öffnet die Suche
document.addEventListener("keydown", (e) => {
  if (e.key !== "/" || e.ctrlKey || e.metaKey || e.altKey) return;
  if (e.target.closest?.("input, textarea, select, [contenteditable]")) return;
  e.preventDefault(); openSearch();
});
