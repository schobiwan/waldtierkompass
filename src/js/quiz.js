// Quiz: nach Trittsiegel oder nach Merkmal
import "./app.js";
import { $, $$, pageData, shuffle, focusEl, href, reduced, NOW, NOW_NAME, Diary, root } from "./util.js";

const all = pageData() || [];
const box = $("quizbox");
const art = (g) => (g === "f" ? "eine" : "ein");

const quiz = {
  mode: "foto", scope: "all", i: 0, score: 0, streak: 0, order: [], done: false, misses: [], note: "",
  base() { return this.mode === "spur" ? all.filter((a) => a.t) : all; },
  pool() {
    const b = this.base();
    if (this.scope === "now") return b.filter((a) => a.p.includes(NOW));
    if (this.scope === "seen") return b.filter((a) => Diary.isSeen(a.k));
    if (this.scope === "open") return b.filter((a) => !Diary.isSeen(a.k));
    return b;
  },
  start(mode) {
    if (mode) this.mode = mode;
    Object.assign(this, { i: 0, score: 0, streak: 0, misses: [], note: "" });
    let p = this.pool();
    if (p.length < 4) { this.note = "Für diese Auswahl gibt es weniger als vier Arten, deshalb werden alle Arten abgefragt."; p = this.base(); }
    this.order = shuffle(p).slice(0, 10);
    this.question();
  },
  top() {
    const opt = (v, t) => `<option value="${v}"${this.scope === v ? " selected" : ""}>${t}</option>`;
    const n = this.order.length;
    return `<div class="qtop">
      <div class="seg" role="group" aria-label="Quiz-Art">
        <button type="button" data-mode="foto" aria-pressed="${this.mode === "foto"}">Nach Foto</button>
        <button type="button" data-mode="spur" aria-pressed="${this.mode === "spur"}">Nach Spur</button>
        <button type="button" data-mode="merkmal" aria-pressed="${this.mode === "merkmal"}">Nach Merkmal</button>
      </div>
      <label class="qscope" for="qscope">Arten <select id="qscope">${opt("all", "Alle Arten")}${opt("now", `Im ${NOW_NAME} aktiv`)}${opt("seen", "Schon gesehen")}${opt("open", "Noch nicht gesehen")}</select></label>
      <span class="count">${this.i < n ? `Frage ${this.i + 1} von ${n}` : "Fertig"} · ${this.score} richtig</span>
    </div>${this.note ? `<p class="qnote">${this.note}</p>` : ""}`;
  },
  question() {
    const a = this.order[this.i];
    this.done = false;
    // Ablenker mit anderem Bild wählen, damit die Spur eindeutig bleibt
    const others = shuffle(this.base().filter((x) => x !== a && (this.mode !== "spur" || x.a !== a.a))).slice(0, 3);
    const opts = shuffle([a, ...others]);
    const stage = this.mode === "foto"
      ? `<img src="${root}photos/${a.k}.webp" alt="Gesuchtes Tier" width="720" height="576">`
      : this.mode === "spur"
      ? `<div class="qtrack">${a.svg}</div><span class="hint">Trittsiegel, nicht maßstabsgetreu</span>`
      : `<div class="qclue"><p>${a.m}.</p><p>${a.m2}.</p></div>`;
    box.innerHTML = this.top() + `
      <div class="qstage">${stage}</div>
      <div class="qside">
        <h2 class="h3" id="q-question" tabindex="-1">${this.mode === "spur" ? "Wer hat diese Spur hinterlassen?" : this.mode === "foto" ? "Welches Tier ist das?" : "Welches Tier passt zu diesen Merkmalen?"}</h2>
        <div class="opts">${opts.map((o) => `<button type="button" class="opt" data-a="${o.k}">${o.n}</button>`).join("")}</div>
        <p class="qfb" id="qfb" aria-live="polite"></p>
        <button type="button" class="btn qnext" id="qnext" hidden>${this.i < this.order.length - 1 ? "Nächste Frage" : "Ergebnis ansehen"}</button>
      </div>`;
  },
  answer(k) {
    if (this.done) return;
    this.done = true;
    const a = this.order[this.i];
    const ok = k === a.k;
    if (ok) { this.score++; this.streak++; } else { this.misses.push(a); this.streak = 0; }
    $$("#quizbox .opt").forEach((b) => {
      b.disabled = true;
      if (b.dataset.a === a.k) b.classList.add("right");
      else if (b.dataset.a === k) b.classList.add("wrong");
    });
    $("qfb").innerHTML = ok ? `<b>Richtig.</b> ${a.m}.` : `<b>Das war ${art(a.g)} ${a.n}.</b> ${a.m}.`;
    const nx = $("qnext"); nx.hidden = false; nx.focus();
    box.querySelector(".count").innerHTML = `Frage ${this.i + 1} von ${this.order.length} · ${this.score} richtig${this.streak >= 3 ? ` · <span class="streak">${this.streak} in Folge</span>` : ""}`;
  },
  next() {
    this.i++;
    if (this.i < this.order.length) { this.question(); focusEl($("q-question")); }
    else { this.end(); focusEl(box.querySelector(".big")); }
  },
  end() {
    const r = this.score / this.order.length;
    const msg = r >= 0.9 ? "Ausgezeichnet, du liest den Wald wie ein Förster." : r >= 0.6 ? "Gut gemacht. Ein paar Tiere lohnt es sich noch einmal anzusehen." : "Ein guter Anfang. Schau dir die Merkmale noch einmal an und versuch es erneut.";
    const miss = [...new Set(this.misses)];
    box.innerHTML = this.top() + `<div class="qend">
      <div class="big">${this.score} von ${this.order.length}</div>
      <p>${msg}</p>
      ${miss.length ? `<p class="qmiss">Noch einmal ansehen:</p><ul>${miss.map((m) => `<li><a href="${href(`arten/${m.k}/`)}">${m.n}</a></li>`).join("")}</ul>` : ""}
      <div class="actions"><button type="button" class="btn" data-restart="foto">Neues Quiz nach Foto</button><button type="button" class="btn ghost" data-restart="spur">Nach Spur</button><button type="button" class="btn ghost" data-restart="merkmal">Nach Merkmal</button></div>
    </div>`;
    const big = box.querySelector(".big"), s = this.score, n = this.order.length;
    if (big && !reduced() && s > 0) {
      const t0 = performance.now();
      const step = (t) => { const f = Math.min(1, (t - t0) / 700); big.textContent = `${Math.round(s * (1 - Math.pow(1 - f, 3)))} von ${n}`; if (f < 1) requestAnimationFrame(step); };
      big.textContent = `0 von ${n}`; requestAnimationFrame(step);
    }
  },
};

box.addEventListener("change", (e) => { if (e.target.id === "qscope") { quiz.scope = e.target.value; quiz.start(); focusEl($("qscope")); } });
box.addEventListener("click", (e) => {
  const t = e.target;
  const m = t.closest("[data-mode]");
  if (m) { quiz.start(m.dataset.mode); focusEl(box.querySelector(`[data-mode="${m.dataset.mode}"]`)); return; }
  const a = t.closest("[data-a]");
  if (a) { quiz.answer(a.dataset.a); return; }
  if (t.closest("#qnext")) { quiz.next(); return; }
  const r = t.closest("[data-restart]");
  if (r) { quiz.start(r.dataset.restart); focusEl($("q-question")); }
});
if (all.length) quiz.start(["#spur", "#merkmal"].includes(location.hash) ? location.hash.slice(1) : "foto");
