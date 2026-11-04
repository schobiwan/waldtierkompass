// Läuft auf jeder Seite: Navigation, Monatsangaben, Falt-Abschnitte
import { $$, nums, NOW, NOW_NAME, MSLUG, href } from "./util.js";

// Abschnitte auf dem Handy eingeklappt, am Desktop offen
const mq = matchMedia("(max-width: 760px)");
const folds = $$("details[data-fold]");
const syncFolds = () => folds.forEach((d) => { d.open = !mq.matches; });
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

// "Jetzt unterwegs"-Liste im Kopf der Startseite
$$("[data-now-list]").forEach((list) => {
  const items = $$("li[data-peak]", list);
  const peak = items.filter((li) => nums(li.dataset.peak).includes(NOW));
  const shown = peak.length >= 3 ? peak : items.filter((li) => nums(li.dataset.present).includes(NOW));
  items.forEach((li) => { li.hidden = !shown.includes(li); });
  list.hidden = false;
  fit(list, shown);
});

function fit(list, shown) {
  const btn = list.querySelector(".now-more");
  const li = btn?.parentElement;
  if (!btn || !li) return;
  let open = false;
  btn.hidden = false;
  const label = (n) => { btn.innerHTML = `+${n}<span class="sr-only"> weitere Arten anzeigen</span><span aria-hidden="true">&nbsp;weitere</span>`; };
  const layout = () => {
    shown.forEach((x) => { x.hidden = false; });
    li.hidden = false;
    if (open) { btn.textContent = "Weniger anzeigen"; return; }
    li.hidden = true;
    const top = shown[0]?.offsetTop ?? 0;
    if (shown.length < 2 || shown[shown.length - 1].offsetTop === top) return;
    li.hidden = false;
    let n = shown.length;
    while (n > 1) {
      label(shown.length - n);
      if (li.offsetTop === top) break;
      n--;
      shown[n].hidden = true;
    }
  };
  btn.addEventListener("click", () => {
    open = !open;
    btn.setAttribute("aria-expanded", String(open));
    list.classList.toggle("open", open);
    layout();
    if (!open) btn.focus();
  });
  let raf = 0;
  addEventListener("resize", () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(layout); });
  layout();
  document.fonts?.ready.then(layout);
}
