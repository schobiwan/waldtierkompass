// Hauptnavigation mit Aufklappmenüs (wie beim Vogelkompass):
// Am Computer klappt „Bestimmen“ unter der Leiste auf,
// auf dem Handy als Fenster über der unteren Leiste. Ohne JavaScript sind die Reiter normale Links.
import { $, $$ } from "./util.js";

const backdrop = $("mbackdrop");
const triggers = $$("[data-menu]");
const panelOf = (t) => $(`menu-${t.dataset.menu}`);
const mobile = () => matchMedia("(max-width: 960px)").matches;
const canHover = () => matchMedia("(hover: hover) and (pointer: fine)").matches;

triggers.forEach((t) => {
  t.setAttribute("role", "button");
  t.setAttribute("aria-expanded", "false");
  t.setAttribute("aria-controls", `menu-${t.dataset.menu}`);
});

function closeAll(except) {
  triggers.forEach((t) => {
    if (t === except) return;
    t.setAttribute("aria-expanded", "false");
    panelOf(t).hidden = true;
  });
  if (!except && backdrop) backdrop.hidden = true;
}
let openedAt = 0; // Zeitpunkt, zu dem ein Menü per Maus aufging
function open(t, focusFirst = false) {
  closeAll(t);
  t.setAttribute("aria-expanded", "true");
  panelOf(t).hidden = false;
  if (backdrop) backdrop.hidden = !mobile();
  if (focusFirst) panelOf(t).querySelector("a")?.focus();
}
const isOpen = (t) => t.getAttribute("aria-expanded") === "true";

let hoverTimer = 0;
triggers.forEach((t) => {
  const li = t.parentElement;
  t.addEventListener("click", (e) => {
    e.preventDefault();
    // Wer mit der Maus hinzeigt und gleich klickt, will das Menü offen halten, nicht schließen
    if (isOpen(t) && Date.now() - openedAt > 600) closeAll(); else open(t);
  });
  t.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown" || ((e.key === "Enter" || e.key === " ") && !isOpen(t))) { e.preventDefault(); open(t, true); }
    else if (e.key === " ") { e.preventDefault(); closeAll(); } // Leertaste schließt, statt die Seite zu scrollen
  });
  li.addEventListener("mouseenter", () => {
    if (!canHover() || mobile()) return;
    clearTimeout(hoverTimer); hoverTimer = window.setTimeout(() => { if (!isOpen(t)) { open(t); openedAt = Date.now(); } }, 80);
  });
  li.addEventListener("mouseleave", () => {
    if (!canHover() || mobile()) return;
    clearTimeout(hoverTimer); hoverTimer = window.setTimeout(() => { if (!li.matches(":focus-within")) closeAll(); }, 220);
  });
  li.addEventListener("focusout", (e) => {
    if (li.contains(e.relatedTarget)) return;
    t.setAttribute("aria-expanded", "false"); panelOf(t).hidden = true;
    if (backdrop) backdrop.hidden = true;
  });
});
document.addEventListener("keydown", (e) => {
  if (e.key !== "Escape") return;
  const t = triggers.find(isOpen);
  if (!t) return;
  closeAll(); t.focus();
});
document.addEventListener("click", (e) => { if (!e.target.closest(".has-menu")) closeAll(); });
backdrop?.addEventListener("click", () => closeAll());
// Ein Klick auf einen Eintrag mit Sprungmarke auf derselben Seite schließt das Menü
$$(".mpanel a").forEach((a) => a.addEventListener("click", () => closeAll()));

export { closeAll };
