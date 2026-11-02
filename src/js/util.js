// Gemeinsame Hilfsfunktionen für den Waldtierkompass
export const MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
export const MSLUG = ["januar", "februar", "maerz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember"];
export const NOW = new Date().getMonth() + 1;
export const NOW_NAME = MONTHS[NOW - 1];
export const KEYS = { diary: "waldtierkompass-tagebuch", animation: "waldtierkompass-animation" };

export const $ = (id) => document.getElementById(id);
export const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
export const nums = (s) => (s || "").split(",").filter(Boolean).map(Number);
export const norm = (s) => String(s).toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss");
export const escapeHtml = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
export const reduced = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
export const setPressed = (el, on) => el.setAttribute("aria-pressed", String(!!on));
export const root = document.documentElement.dataset.root || "./";
export const href = (p) => root + p + "index.html";
export function focusEl(el) {
  if (!(el instanceof HTMLElement)) return;
  if (!el.hasAttribute("tabindex") && !/^(A|BUTTON|INPUT|SELECT|TEXTAREA)$/.test(el.tagName)) el.setAttribute("tabindex", "-1");
  el.focus();
}
export function today() {
  const d = new Date();
  return new Date(d.getTime() - d.getTimezoneOffset() * 6e4).toISOString().slice(0, 10);
}
export function fmtDate(iso) {
  const [y, m, d] = iso.split("-").map(Number);
  return `${d}. ${MONTHS[m - 1]} ${y}`;
}
export function shuffle(a) {
  const r = [...a];
  for (let i = r.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; }
  return r;
}
export function pageData() {
  const el = document.getElementById("wk-data");
  try { return el ? JSON.parse(el.textContent || "null") : null; } catch { return null; }
}

// Tagebuch im localStorage
export const Diary = {
  all() {
    try { return JSON.parse(localStorage.getItem(KEYS.diary) || "[]"); } catch { return []; }
  },
  save(list) {
    try { localStorage.setItem(KEYS.diary, JSON.stringify(list)); } catch {}
    document.dispatchEvent(new CustomEvent("wk:diary"));
  },
  add(entry) {
    const list = this.all();
    list.push({ id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6), ...entry });
    this.save(list);
  },
  remove(id) { this.save(this.all().filter((e) => e.id !== id)); },
  forKey(k) { return this.all().filter((e) => e.k === k).sort((a, b) => b.d.localeCompare(a.d)); },
  seenKeys() { return new Set(this.all().map((e) => e.k)); },
  isSeen(k) { return this.all().some((e) => e.k === k); },
  count() { return this.all().length; },
};
