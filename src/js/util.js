// Gemeinsame Hilfsfunktionen für den Waldtierkompass (mit Zugriff auf die Seite)
export { norm, fold, escapeHtml, nums, debounce } from "./text.js";

const MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
export const MSLUG = ["januar", "februar", "maerz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember"];
export const NOW = new Date().getMonth() + 1;
export const NOW_NAME = MONTHS[NOW - 1];

export const $ = (id) => document.getElementById(id);
export const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
export const reduced = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
export const setPressed = (el, on) => el.setAttribute("aria-pressed", String(!!on));

// Weg zur Wurzel der Seite (data-root im <html>), z. B. "../../"
export const ROOT = document.documentElement.dataset.root || "./";
// Live-Seite nutzt kurze Adressen (/arten/dachs/), die Vorschau verlinkt index.html
export const IDX = document.documentElement.hasAttribute("data-clean") ? "" : "index.html";
export const href = (p) => ROOT + p + IDX;

export function focusEl(el) {
  if (!(el instanceof HTMLElement)) return;
  if (!el.hasAttribute("tabindex") && !/^(A|BUTTON|INPUT|SELECT|TEXTAREA)$/.test(el.tagName)) el.setAttribute("tabindex", "-1");
  el.focus();
}
