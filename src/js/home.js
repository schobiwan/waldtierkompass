// Startseite: Suche, Filter und Sortierung
import "./app.js";
import { $, $$, nums, norm, escapeHtml, NOW, reduced, setPressed, focusEl } from "./util.js";

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
  q: "", grp: new Set(), act: new Set(), hab: new Set(), size: new Set(), now: false, sort: "now",
  count() { return SETS.reduce((n, k) => n + this[k].size, 0) + (this.now ? 1 : 0); },
  reset(keepQuery = false) {
    if (!keepQuery) { this.q = ""; q.value = ""; }
    SETS.forEach((k) => this[k].clear());
    this.now = false;
  },
  matches(a) {
    const term = norm(this.q.trim());
    return (!term || a.search.includes(term))
      && (!this.grp.size || this.grp.has(a.grp))
      && (!this.act.size || a.act.some((x) => this.act.has(x)))
      && (!this.hab.size || a.hab.some((x) => this.hab.has(x)))
      && (!this.size.size || this.size.has(a.size))
      && (!this.now || a.present.includes(NOW));
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
  else if (r === "now") state.now = false;
  else state[r].delete(b.dataset.v);
  render();
  focusEl($("active").querySelector("button") || q);
});
render();
grid.classList.add("calm");

// Karussell "Jetzt unterwegs": Arten in Hauptzeit zuerst, dann alle übrigen aktiven Arten
{
  const list = $("nowcards");
  const items = $$("#nowcards > li");
  const peak = items.filter((li) => nums(li.dataset.peak).includes(NOW));
  const rest = items.filter((li) => !peak.includes(li) && nums(li.dataset.present).includes(NOW));
  items.forEach((li) => { li.hidden = true; li.classList.toggle("pk", peak.includes(li)); });
  [...peak, ...rest].forEach((li) => { li.hidden = false; list.appendChild(li); });
  // Tier des Monats: erste Art in Hauptzeit
  const top = peak[0] || rest[0];
  if (top && top.dataset.k !== $("spot-link")?.getAttribute("href")?.split("/")[1]) {
    const k = top.dataset.k, im = $("spot-img");
    $("spot-link").href = `arten/${k}/index.html`;
    im.src = `photos/${k}.webp`;
    im.srcset = `photos/${k}-400.webp 400w, photos/${k}.webp 720w`;
    $("spot-name").textContent = top.dataset.name;
    $("spot-hl").textContent = top.dataset.hl;
    $("spot-cred").textContent = `Foto: ${top.dataset.credit}`;
  }
  if (top) top.hidden = true; // steht schon groß im Kopfbereich
  $$(".h5-events").forEach((ul) => { ul.hidden = Number(ul.dataset.m) !== NOW; });
  const prev = $("now-prev"), next = $("now-next");
  const step = () => { const li = list.querySelector("li:not([hidden])"); return li ? li.offsetWidth + 12 : list.clientWidth; };
  const sync = () => {
    const max = list.scrollWidth - list.clientWidth - 2;
    prev.disabled = list.scrollLeft <= 2;
    next.disabled = list.scrollLeft >= max;
  };
  const go = (dir) => {
    const per = Math.max(1, Math.round(list.clientWidth / step()));
    list.scrollBy({ left: dir * per * step(), behavior: reduced() ? "auto" : "smooth" });
  };
  prev?.addEventListener("click", () => go(-1));
  next?.addEventListener("click", () => go(1));
  list.addEventListener("scroll", sync, { passive: true });
  addEventListener("resize", sync);
  sync();
}

// Tiergruppen im Kopfbereich setzen den Gruppenfilter
$$(".hchip").forEach((b) => b.addEventListener("click", () => {
  state.grp.clear(); state.grp.add(b.dataset.hgrp); render();
  $("arten").scrollIntoView({ behavior: reduced() ? "auto" : "smooth" });
}));

// Suche im Kopfbereich steuert das Raster
const hq = $("hq");
$("hsearch")?.addEventListener("submit", (e) => {
  e.preventDefault();
  q.value = hq.value; state.q = hq.value; render();
  $("arten").scrollIntoView({ behavior: reduced() ? "auto" : "smooth" });
});
hq?.addEventListener("input", () => { q.value = hq.value; state.q = hq.value; render(); });

