// Tagebuch-Seite: Fortschritt, offene Arten, Einträge nach Monat
import "./app.js";
import { $, pageData, Diary, fmtDate, escapeHtml, href, MONTHS } from "./util.js";

const species = pageData() || [];
const names = Object.fromEntries(species.map((s) => [s.k, s.n]));

function render() {
  const list = Diary.all().filter((e) => names[e.k]).sort((a, b) => b.d.localeCompare(a.d));
  const seen = new Set(list.map((e) => e.k));
  const n = seen.size, total = species.length;
  $("ring-num").textContent = String(n);
  $("ring").setAttribute("stroke-dasharray", `${Math.round((n / total) * 100)} 100`);
  $("tally").textContent = n ? `${n} von ${total} Arten gesehen, ${list.length} ${list.length === 1 ? "Eintrag" : "Einträge"}` : "Noch keine Art gesehen";
  const open = species.filter((s) => !seen.has(s.k));
  $("open-title").textContent = open.length ? `Noch nicht gesehen (${open.length})` : "Alle Arten gesehen!";
  $("open-list").innerHTML = open.map((s) => `<a href="${href(`arten/${s.k}/`)}">${escapeHtml(s.n)}</a>`).join("");

  if (!list.length) { $("log").innerHTML = '<p class="none">Noch keine Sichtungen.</p>'; return; }
  const groups = new Map();
  list.forEach((e) => {
    const [y, m] = e.d.split("-");
    const k = `${MONTHS[Number(m) - 1]} ${y}`;
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(e);
  });
  $("log").innerHTML = [...groups].map(([k, es]) => `<section class="logm"><h2 class="h5">${k}</h2><ul class="dlist">${es.map((e) => `
    <li><time datetime="${e.d}">${fmtDate(e.d)}</time> · <a href="${href(`arten/${e.k}/`)}">${escapeHtml(names[e.k])}</a>${e.o ? " · " + escapeHtml(e.o) : ""}${e.n ? `<br><span class="dnote2">${escapeHtml(e.n)}</span>` : ""}
    <button type="button" class="del" data-del="${e.id}" aria-label="Eintrag vom ${fmtDate(e.d)} löschen">Löschen</button></li>`).join("")}</ul></section>`).join("");
}

$("log").addEventListener("click", (e) => {
  const b = e.target.closest("[data-del]");
  if (!b) return;
  if (!b.classList.contains("confirm")) {
    b.classList.add("confirm"); b.textContent = "Wirklich löschen?";
    setTimeout(() => { if (b.isConnected) { b.classList.remove("confirm"); b.textContent = "Löschen"; } }, 4000);
    return;
  }
  Diary.remove(b.dataset.del);
});

$("copy").addEventListener("click", async () => {
  const list = Diary.all().filter((e) => names[e.k]).sort((a, b) => a.d.localeCompare(b.d));
  const text = list.map((e) => `${fmtDate(e.d)}\t${names[e.k]}${e.o ? "\t" + e.o : ""}${e.n ? "\t" + e.n : ""}`).join("\n") || "Noch keine Sichtungen.";
  try { await navigator.clipboard.writeText(text); $("copied").textContent = "Kopiert."; }
  catch { $("copied").textContent = "Kopieren ist hier nicht möglich."; }
  setTimeout(() => { $("copied").textContent = ""; }, 3000);
});

document.addEventListener("wk:diary", render);
render();
