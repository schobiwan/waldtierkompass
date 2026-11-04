// Läuft auf jeder Seite: Navigation, Monatsangaben, Falt-Abschnitte
import { $$, NOW, NOW_NAME, MSLUG, href } from "./util.js";

// Falt-Abschnitte: Am Desktop immer offen und nicht bedienbar, auf dem Handy aufklappbar.
// Abschnitte mit data-fold starten auf dem Handy zugeklappt.
const mq = matchMedia("(max-width: 760px)");
const folds = $$("details.fold");
const syncFolds = () => folds.forEach((d) => {
  if (!mq.matches || d.hasAttribute("data-fold")) d.open = !mq.matches;
  d.querySelector("summary")?.setAttribute("tabindex", mq.matches ? "0" : "-1");
});
syncFolds();
mq.addEventListener("change", syncFolds);
folds.forEach((d) => d.querySelector("summary")?.addEventListener("click", (e) => { if (!mq.matches) e.preventDefault(); }));

// Schatten unter der Navigation beim Scrollen
const nav = document.querySelector(".appnav");
const onScroll = () => nav?.classList.toggle("scrolled", window.scrollY > 4);
addEventListener("scroll", onScroll, { passive: true });
onScroll();

// Aktueller Monat
$$("[data-now-name]").forEach((el) => { el.textContent = NOW_NAME; });
$$("a[data-now-link]").forEach((a) => { a.href = href(`waldjahr/${MSLUG[NOW - 1]}/`); });
$$("[data-month]").forEach((el) => { if (Number(el.dataset.month) === NOW) el.classList.add("now"); });

// Kalender auf dem Handy zum aktuellen Monat scrollen
$$(".cal-wrap").forEach((wrap) => {
  const th = wrap.querySelector(`thead th[data-month="${NOW}"]`), n = wrap.querySelector(".n");
  if (th && wrap.scrollWidth > wrap.clientWidth) wrap.scrollLeft = Math.max(0, th.offsetLeft - (n ? n.offsetWidth : 0) - th.offsetWidth * 2);
});
