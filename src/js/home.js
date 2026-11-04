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
  words: [...new Set(norm(li.dataset.search).split(/[^a-z0-9]+/).filter((w) => w.length > 2))],
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
    return (!term || fuzzy(a, term))
      && (!this.grp.size || this.grp.has(a.grp))
      && (!this.act.size || a.act.some((x) => this.act.has(x)))
      && (!this.hab.size || a.hab.some((x) => this.hab.has(x)))
      && (!this.size.size || this.size.has(a.size))
      && (!this.now || a.present.includes(NOW));
  },
};

// Tippfehler verzeihen: Levenshtein-Abstand, auch gegen den Wortanfang
function dist(a, b) {
  const m = a.length, n = b.length;
  let prev = Array.from({ length: n + 1 }, (_, j) => j);
  for (let i = 1; i <= m; i++) {
    const cur = [i];
    for (let j = 1; j <= n; j++) cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    prev = cur;
  }
  return prev[n];
}
const tolerance = (t) => (t.length >= 7 ? 2 : t.length >= 3 ? 1 : 0);
function fuzzy(a, term) {
  if (a.search.includes(term)) return true;
  const k = tolerance(term);
  if (!k || term.includes(" ")) return false;
  return a.words.some((w) => dist(term, w) <= k || (w.length > term.length && dist(term, w.slice(0, term.length)) <= k));
}
function suggest(term) {
  let best = null, bd = 99;
  animals.forEach((a) => a.words.forEach((w) => {
    const d = Math.min(dist(term, w), w.length > term.length ? dist(term, w.slice(0, term.length)) + 1 : 99);
    if (d < bd) { bd = d; best = a; }
  }));
  return bd <= tolerance(term) + (term.length >= 5 ? 1 : 0) ? best : null;
}

const BIRDS = ["vogel", "voegel", "eule", "kauz", "uhu", "specht", "meise", "amsel", "drossel", "fink", "bussard", "falke", "habicht", "sperber", "kraehe", "rabe", "elster", "haeher", "taube", "kuckuck", "zaunkoenig", "rotkehlchen", "kleiber", "schnepfe", "storch", "reiher", "ente", "gans", "schwan", "milan", "adler"];
const byName = (a, b) => a.name.localeCompare(b.name, "de");
const nowRank = (a) => (a.peak.includes(NOW) ? 0 : a.present.includes(NOW) ? 1 : 2);
let lastOrder = "";
const sep = document.createElement("li");
sep.className = "grid-sep";
sep.setAttribute("role", "presentation");
sep.innerHTML = "<span>Gerade kaum zu sehen</span>";

function render() {
  const list = animals.filter((a) => state.matches(a));
  if (state.sort === "az") list.sort(byName);
  else if (state.sort === "size") list.sort((a, b) => a.mid - b.mid || byName(a, b));
  else list.sort((a, b) => nowRank(a) - nowRank(b) || byName(a, b));
  const order = state.sort + ":" + list.map((a) => a.key).join();
  grid.classList.toggle("calm", order === lastOrder);
  if (order !== lastOrder) {
    animals.forEach((a) => { a.li.hidden = true; });
    sep.remove();
    list.forEach((a, i) => {
      a.li.hidden = false;
      a.li.style.setProperty("--i", String(Math.min(i, 14)));
      if (state.sort === "now" && i > 0 && nowRank(a) === 2 && nowRank(list[i - 1]) < 2) grid.appendChild(sep);
      grid.appendChild(a.li);
    });
    if (!reduced()) list.forEach((a) => { a.li.style.animation = "none"; void a.li.offsetWidth; a.li.style.animation = ""; });
  }
  lastOrder = order;
  $("empty").hidden = list.length > 0;
  const sg = $("empty-suggest"), term = norm(state.q.trim());
  const hit = !list.length && term ? suggest(term) : null;
  const bird = !list.length && term && BIRDS.some((w) => term.includes(w) || (term.length >= 4 && w.startsWith(term)));
  sg.hidden = !hit && !bird;
  if (bird) sg.innerHTML = `Vögel findest du auf unserer Schwesterseite <a class="linkbtn" href="https://vogelkompass.de/" rel="noopener">Vogelkompass</a>.`;
  else if (hit) sg.innerHTML = `Meintest du <button type="button" class="linkbtn" data-try="${escapeHtml(hit.name)}">${escapeHtml(hit.name)}</button>?`;

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
q.addEventListener("input", () => { const hqf = $("hq"); if (hqf) hqf.value = q.value; clearTimeout(t); t = setTimeout(() => { state.q = q.value; render(); }, 120); });
q.addEventListener("keydown", (e) => { if (e.key === "Escape" && q.value) { e.preventDefault(); q.value = ""; state.q = ""; render(); } });
sortSel.addEventListener("change", () => { state.sort = sortSel.value; render(); });

const panel = $("fpanel"), toggle = $("f-toggle");
const showPanel = (on = panel.hidden) => { panel.hidden = !on; toggle.setAttribute("aria-expanded", String(on)); };
toggle.addEventListener("click", () => showPanel());
$("f-done").addEventListener("click", () => { showPanel(false); toggle.focus(); });
$("f-reset").addEventListener("click", () => { state.reset(true); render(); });
$("empty-reset").addEventListener("click", () => { state.reset(); const hqf = $("hq"); if (hqf) hqf.value = ""; render(); focusEl(q); });
$("empty").addEventListener("click", (e) => {
  const tryB = e.target.closest("[data-try]"), g = e.target.closest("[data-sgrp]");
  if (tryB) { q.value = tryB.dataset.try; state.q = q.value; const hqf = $("hq"); if (hqf) hqf.value = q.value; render(); focusEl(q); }
  if (g) { state.reset(); const hqf = $("hq"); if (hqf) hqf.value = ""; state.grp.add(g.dataset.sgrp); render(); focusEl($("rcount")); }
});
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
  else if (r === "q") { state.q = ""; q.value = ""; const hqf = $("hq"); if (hqf) hqf.value = ""; }
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
    $("spot-cred").innerHTML = top.querySelector(".cred")?.innerHTML || "";
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

