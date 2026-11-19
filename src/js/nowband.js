// Startseite: Karussell „Jetzt unterwegs“ und Tier des Monats im Kopfbereich.
// Der Build kennt nur den Monat, in dem er lief; hier wird nach dem echten aktuellen Monat sortiert.
import { $, $$, nums, NOW, reduced, IDX } from "./util.js";

const list = $("nowcards");
const items = $$("#nowcards > li");
// Arten in Hauptzeit zuerst, dann alle übrigen aktiven Arten
const peak = items.filter((li) => nums(li.dataset.peak).includes(NOW));
const rest = items.filter((li) => !peak.includes(li) && nums(li.dataset.present).includes(NOW));
items.forEach((li) => { li.hidden = true; li.classList.toggle("pk", peak.includes(li)); });
[...peak, ...rest].forEach((li) => { li.hidden = false; list.appendChild(li); });

// Tier des Monats: erste Art in Hauptzeit
const top = peak[0] || rest[0];
function showSpot(li) {
  const k = li.dataset.k, im = $("spot-img");
  $("spot-link").href = `arten/${k}/${IDX}`;
  im.src = `photos/${k}.webp`;
  im.srcset = `photos/${k}-400.webp 400w, photos/${k}.webp 720w`;
  $("spot-name").textContent = li.dataset.name;
  $("spot-hl").textContent = li.dataset.hl;
  const c = li.querySelector(".cred"), sc = $("spot-cred");
  if (c && sc) { sc.innerHTML = c.innerHTML; sc.href = c.getAttribute("href"); }
}
if (top && top.dataset.k !== $("spot-link")?.getAttribute("href")?.split("/")[1]) showSpot(top);
if (top) top.hidden = true; // steht schon groß im Kopfbereich
$$(".h5-events").forEach((ul) => { ul.hidden = Number(ul.dataset.m) !== NOW; });

// Vor- und Zurück-Knöpfe blättern um so viele Karten, wie gerade sichtbar sind
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
