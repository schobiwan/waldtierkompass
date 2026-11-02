// Startseite: Suche, Filter und Sortierung
import "./app.js";
import { $, $$, nums, norm, escapeHtml, NOW, reduced, setPressed, focusEl, Diary } from "./util.js";

const grid = $("grid");
const q = $("q");
const sortSel = $("sort");
const animals = $$("#grid > li.bird").map((li) => ({
  li,
  key: li.dataset.key,
  name: li.dataset.name,
  search: norm(li.dataset.search),
  grp: li.dataset.grp,
  act: li.dataset.act.split("|"),
  hab: li.dataset.hab.split("|"),
  size: li.dataset.size,
  mid: Number(li.dataset.mid),
  present: nums(li.dataset.present),
  peak: nums(li.dataset.peak),
}));
const TOTAL = animals.length;
const SETS = ["grp", "act", "hab", "size"];
const LABEL = {
  act: { tag: "tagaktiv", daemmerung: "dämmerungsaktiv", nacht: "nachtaktiv" },
  size: { s: "bis Maus", m: "bis Eichhörnchen", l: "bis Fuchs", xl: "größer als ein Fuchs" },
};

const state = {
  q: "", grp: new Set(), act: new Set(), hab: new Set(), size: new Set(), now: false, open: false, sort: "now",
  count() { return SETS.reduce((n, k) => n + this[k].size, 0) + (this.now ? 1 : 0) + (this.open ? 1 : 0); },
  reset(keepQuery = false) {
    if (!keepQuery) { this.q = ""; q.value = ""; }
    SETS.forEach((k) => this[k].clear());
    this.now = false; this.open = false;
  },
  matches(a) {
    const term = norm(this.q.trim());
    return (!term || a.search.includes(term))
      && (!this.grp.size || this.grp.has(a.grp))
      && (!this.act.size || a.act.some((x) => this.act.has(x)))
      && (!this.hab.size || a.hab.some((x) => this.hab.has(x)))
      && (!this.size.size || this.size.has(a.size))
      && (!this.now || a.present.includes(NOW))
      && (!this.open || !Diary.isSeen(a.key));
  },
};

const byName = (a, b) => a.name.localeCompare(b.name, "de");
const nowRank = (a) => (a.peak.includes(NOW) ? 0 : a.present.includes(NOW) ? 1 : 2);
let lastOrder = "";

function render() {
  const list = animals.filter((a) => state.matches(a));
  if (state.sort === "az") list.sort(byName);
  else if (state.sort === "size") list.sort((a, b) => a.mid - b.mid || byName(a, b));
  else list.sort((a, b) => nowRank(a) - nowRank(b) || byName(a, b));
  const order = list.map((a) => a.key).join();
  grid.classList.toggle("calm", order === lastOrder);
  if (order !== lastOrder) {
    animals.forEach((a) => { a.li.hidden = true; });
    list.forEach((a, i) => {
      a.li.hidden = false;
      a.li.style.setProperty("--i", String(Math.min(i, 14)));
      grid.appendChild(a.li);
    });
    if (!reduced()) list.forEach((a) => { a.li.style.animation = "none"; void a.li.offsetWidth; a.li.style.animation = ""; });
  }
  lastOrder = order;
  $("empty").hidden = list.length > 0;

  const n = state.count();
  const fc = $("fcount");
  fc.hidden = !n;
  fc.innerHTML = `${n}<span class="sr-only"> aktiv</span>`;
  $("rcount").textContent = list.length === TOTAL ? `${TOTAL} Arten` : `${list.length} von ${TOTAL} Arten`;

  $$(".fchips .chip").forEach((c) => {
    const g = c.dataset.g, v = c.dataset.v;
    setPressed(c, g === "flag" ? state[v] : state[g].has(v));
  });

  const chips = [];
  const chip = (attrs, label) => `<button type="button" ${attrs} aria-label="Filter ${escapeHtml(label)} entfernen">${escapeHtml(label)}</button>`;
  if (state.q.trim()) chips.push(chip('data-rm="q"', `Suche: „${state.q.trim()}“`));
  SETS.forEach((g) => state[g].forEach((v) => chips.push(chip(`data-rm="${g}" data-v="${escapeHtml(v)}"`, LABEL[g]?.[v] || v))));
  if (state.now) chips.push(chip('data-rm="now"', "Jetzt aktiv"));
  if (state.open) chips.push(chip('data-rm="open"', "Noch nicht gesehen"));
  if (chips.length > 1) chips.push('<button type="button" class="clear" data-rm="all">Alles zurücksetzen</button>');
  const act = $("active");
  act.innerHTML = chips.join("");
  act.hidden = !chips.length;
}

let t = 0;
q.addEventListener("input", () => { clearTimeout(t); t = setTimeout(() => { state.q = q.value; render(); }, 120); });
q.addEventListener("keydown", (e) => { if (e.key === "Escape" && q.value) { e.preventDefault(); q.value = ""; state.q = ""; render(); } });
sortSel.addEventListener("change", () => { state.sort = sortSel.value; render(); });

const panel = $("fpanel"), toggle = $("f-toggle");
const showPanel = (on = panel.hidden) => { panel.hidden = !on; toggle.setAttribute("aria-expanded", String(on)); };
toggle.addEventListener("click", () => showPanel());
$("f-done").addEventListener("click", () => { showPanel(false); toggle.focus(); });
$("f-reset").addEventListener("click", () => { state.reset(true); render(); });
$("empty-reset").addEventListener("click", () => { state.reset(); render(); focusEl(q); });
panel.addEventListener("click", (e) => {
  const c = e.target.closest(".fchips .chip");
  if (!c) return;
  const g = c.dataset.g, v = c.dataset.v;
  if (g === "flag") state[v] = !state[v];
  else state[g].has(v) ? state[g].delete(v) : state[g].add(v);
  render();
});
$("active").addEventListener("click", (e) => {
  const b = e.target.closest("[data-rm]");
  if (!b) return;
  const r = b.dataset.rm;
  if (r === "all") state.reset();
  else if (r === "q") { state.q = ""; q.value = ""; }
  else if (r === "now" || r === "open") state[r] = false;
  else state[r].delete(b.dataset.v);
  render();
  focusEl($("active").querySelector("button") || q);
});
$("now-all")?.addEventListener("click", () => {
  state.reset(); state.now = true; state.sort = "now"; sortSel.value = "now"; render();
  $("arten").scrollIntoView({ behavior: reduced() ? "auto" : "smooth" });
  focusEl($("rcount"));
});
document.addEventListener("wk:diary", () => { if (state.open) render(); });
render();
grid.classList.add("calm");

