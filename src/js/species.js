// Artseite: Tagebuch-Kasten
import "./app.js";
import { $, Diary, today, fmtDate, escapeHtml } from "./util.js";

const box = $("sp-diary");
if (box) {
  const key = box.dataset.key;
  const name = box.dataset.name;
  const render = () => {
    const list = Diary.forKey(key);
    $("d-seenline").textContent = list.length
      ? `Schon ${list.length === 1 ? "einmal" : list.length + "-mal"} gesehen, zuletzt am ${fmtDate(list[0].d)}.`
      : "";
    $("d-list").innerHTML = list.slice(0, 5).map((e) =>
      `<li><time datetime="${e.d}">${fmtDate(e.d)}</time>${e.o ? " · " + escapeHtml(e.o) : ""}${e.n ? `<br><span class="dnote2">${escapeHtml(e.n)}</span>` : ""}</li>`).join("");
  };
  $("d-date").value = today();
  $("d-seen").addEventListener("click", () => {
    Diary.add({ k: key, d: today(), o: "", n: "" });
    render();
    $("d-seen").textContent = "Eingetragen";
    setTimeout(() => { $("d-seen").textContent = "Heute gesehen"; }, 2500);
  });
  $("d-form").addEventListener("submit", (e) => {
    e.preventDefault();
    Diary.add({ k: key, d: $("d-date").value || today(), o: $("d-ort").value.trim(), n: $("d-note").value.trim() });
    $("d-ort").value = ""; $("d-note").value = "";
    const s = $("d-saved"); s.hidden = false; setTimeout(() => { s.hidden = true; }, 2500);
    render();
  });
  document.addEventListener("wk:diary", render);
  render();
  void name;
}
