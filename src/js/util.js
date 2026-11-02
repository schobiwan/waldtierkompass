// Gemeinsame Hilfsfunktionen für den Waldtierkompass
export const MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
export const MSLUG = ["januar", "februar", "maerz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember"];
export const NOW = new Date().getMonth() + 1;
export const NOW_NAME = MONTHS[NOW - 1];

export const $ = (id) => document.getElementById(id);
export const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
export const nums = (s) => (s || "").split(",").filter(Boolean).map(Number);
export const norm = (s) => String(s).toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss");
export const escapeHtml = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
export const reduced = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
export const setPressed = (el, on) => el.setAttribute("aria-pressed", String(!!on));
const root = document.documentElement.dataset.root || "./";
export const href = (p) => root + p + "index.html";
export function focusEl(el) {
  if (!(el instanceof HTMLElement)) return;
  if (!el.hasAttribute("tabindex") && !/^(A|BUTTON|INPUT|SELECT|TEXTAREA)$/.test(el.tagName)) el.setAttribute("tabindex", "-1");
  el.focus();
}
