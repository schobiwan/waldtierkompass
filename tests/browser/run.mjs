// Browsertests in Chrome: Bedienung (Suche, Filter, Menü, Tastatur), Fehler in der Konsole und Barrierefreiheit (axe, WCAG 2.2 AA).
// Aufruf: npm run build && npm run test:browser      Chrome-Pfad bei Bedarf über CHROME=/pfad/zu/chrome
import { createServer } from "node:http";
import { readFileSync, existsSync, statSync, readdirSync } from "node:fs";
import { join, extname, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
import { chromium } from "playwright-core";

const require = createRequire(import.meta.url);
const ROOT = process.env.DIST ? join(process.env.DIST, "/") : fileURLToPath(new URL("../../dist/", import.meta.url));
const AXE = readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");
const MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
const NOW = new Date().getMonth() + 1;

// ---------------------------------------------------------------- kleiner Server wie statichost (Ordner → index.html, sonst 404.html)
const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".json": "application/json", ".svg": "image/svg+xml",
  ".webp": "image/webp", ".jpg": "image/jpeg", ".png": "image/png", ".ico": "image/x-icon", ".woff2": "font/woff2", ".webmanifest": "application/manifest+json", ".txt": "text/plain" };
const server = createServer((req, res) => {
  let p = join(ROOT, decodeURIComponent(new URL(req.url, "http://x").pathname));
  if (existsSync(p) && statSync(p).isDirectory()) p = join(p, "index.html");
  const ok = existsSync(p);
  res.writeHead(ok ? 200 : 404, { "Content-Type": (ok ? TYPES[extname(p)] : TYPES[".html"]) || "application/octet-stream" });
  res.end(readFileSync(ok ? p : join(ROOT, "404.html")));
});
await new Promise((r) => server.listen(0, "127.0.0.1", r));
const BASE = `http://127.0.0.1:${server.address().port}`;

const chromePath = process.env.CHROME || ["/usr/bin/google-chrome", "/usr/bin/chromium", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"].find(existsSync);
const browser = await chromium.launch({ executablePath: chromePath });

// ---------------------------------------------------------------- Mini-Testrahmen
let failed = 0, passed = 0;
async function test(name, fn) {
  try { await fn(); passed++; console.log(`  ✓ ${name}`); }
  catch (e) { failed++; console.log(`  ✗ ${name}\n      ${String(e.message || e).split("\n").join("\n      ")}`); }
}
function expect(cond, msg) { if (!cond) throw new Error(msg); }
async function open(path, opts = {}) {
  const ctx = await browser.newContext({ viewport: opts.mobile ? { width: 390, height: 844 } : { width: 1280, height: 900 },
    isMobile: !!opts.mobile, hasTouch: !!opts.mobile, colorScheme: opts.dark ? "dark" : "light", javaScriptEnabled: opts.js !== false,
    reducedMotion: "reduce" });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(`JS-Fehler: ${e.message}`));
  page.on("console", (m) => { if (m.type() === "error") errors.push(`Konsole: ${m.text()}`); });
  page.on("response", (r) => { if (r.url().startsWith(BASE) && r.status() >= 400 && !r.url().endsWith("/gibt-es-nicht/")) errors.push(`${r.status()}: ${r.url()}`); });
  await page.goto(BASE + path, { waitUntil: "load" });
  return { page, errors, close: () => ctx.close() };
}
const visibleCards = (page) => page.$$eval("#grid > li.bird", (lis) => lis.filter((l) => !l.hidden).map((l) => l.dataset.key));
const pause = (page, ms = 250) => page.waitForTimeout(ms);

const allPages = [];
(function walk(d) {
  for (const f of readdirSync(d, { withFileTypes: true })) {
    if (f.isDirectory()) walk(join(d, f.name));
    else if (f.name === "index.html") allPages.push("/" + relative(ROOT, d).replaceAll("\\", "/") + (d === ROOT.replace(/\/$/, "") || relative(ROOT, d) === "" ? "" : "/"));
  }
})(ROOT);
allPages.sort();

// ---------------------------------------------------------------- Tests
console.log(`\nAlle ${allPages.length} Seiten laden ohne Fehler`);
await test("keine JS-Fehler, keine fehlenden Dateien", async () => {
  const problems = [];
  for (const p of allPages) {
    const { page, errors, close } = await open(p);
    await pause(page, 50);
    if (errors.length) problems.push(`${p}: ${errors.join(" | ")}`);
    await close();
  }
  expect(!problems.length, problems.join("\n"));
});

console.log("\nBarrierefreiheit (axe, WCAG 2.2 A und AA)");
const AXE_PAGES = allPages.concat(["/gibt-es-nicht/"]);
for (const mode of [{ name: "hell, Computer" }, { name: "dunkel, Computer", dark: true }, { name: "hell, Handy", mobile: true }, { name: "dunkel, Handy", dark: true, mobile: true }]) {
  await test(`alle Seiten ${mode.name}`, async () => {
    const problems = [];
    for (const p of AXE_PAGES) {
      const { page, close } = await open(p, mode);
      await page.addScriptTag({ content: AXE });
      const res = await page.evaluate(async () => (await axe.run(document, { runOnly: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"] })).violations
        .map((v) => `${v.id} (${v.impact}): ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(", ")}`));
      res.forEach((r) => problems.push(`${p}: ${r}`));
      await close();
    }
    expect(!problems.length, problems.slice(0, 30).join("\n"));
  });
}

console.log("\nStartseite: Suche und Filter");
{
  const { page, errors, close } = await open("/");
  await test("aktueller Monat überall eingesetzt", async () => {
    const names = await page.$$eval("[data-now-name]", (els) => els.map((e) => e.textContent));
    expect(names.length >= 5 && names.every((n) => n === MONTHS[NOW - 1]), `Monatsnamen: ${names.join(", ")}`);
    expect(!(await page.content()).includes("{now_name}"), "Platzhalter {now_name} im HTML");
  });
  await test("Tier des Monats ist eine Art in Hauptzeit und fehlt im Karussell", async () => {
    const spot = (await page.getAttribute("#spot-link", "href")).split("/")[1];
    const peak = await page.$eval(`#nowcards > li[data-k="${spot}"]`, (li) => ({ hidden: li.hidden, peak: li.dataset.peak.split(",").map(Number) }));
    expect(peak.hidden, "Tier des Monats steht zusätzlich im Karussell");
    expect(peak.peak.includes(new Date().getMonth() + 1), "Tier des Monats nicht in Hauptzeit");
  });
  await test("Karussell blättert", async () => {
    expect(await page.isDisabled("#now-prev"), "Zurück-Knopf am Anfang nicht gesperrt");
    await page.click("#now-next"); await pause(page, 400);
    expect(await page.$eval("#nowcards", (l) => l.scrollLeft) > 0, "Karussell hat nicht geblättert");
    expect(!(await page.isDisabled("#now-prev")), "Zurück-Knopf bleibt gesperrt");
  });
  await test("alle 33 Arten ohne Suche", async () => {
    expect((await visibleCards(page)).length === 33, "nicht alle Arten sichtbar");
    expect((await page.textContent("#rcount")) === "33 Arten", await page.textContent("#rcount"));
  });
  await test("Suche nach Name", async () => {
    await page.fill("#q", "Luchs"); await pause(page);
    // die unscharfe Suche findet auch ähnliche Wörter (Luchs ~ Fuchs), der genaue Treffer steht vorn
    const found = await visibleCards(page);
    expect(found[0] === "luchs", String(found));
    expect((await page.textContent("#rcount")) === `${found.length} von 33 Arten`, await page.textContent("#rcount"));
    expect((await page.inputValue("#hq")) === "Luchs", "Suchfeld im Kopfbereich nicht mitgezogen");
  });
  await test("Suche nach Merkmal und Synonym", async () => {
    await page.fill("#q", "Pinselohren"); await pause(page);
    expect((await visibleCards(page))[0] === "luchs", String(await visibleCards(page)));
    await page.fill("#q", "Keiler"); await pause(page);
    expect((await visibleCards(page))[0] === "wildschwein", String(await visibleCards(page)));
  });
  await test("Tippfehler: Vorschlag „Meintest du …?“", async () => {
    await page.fill("#q", "Wildschwien"); await pause(page);
    const found = await visibleCards(page);
    if (found.length) { expect(found[0] === "wildschwein", String(found)); return; } // unscharfe Suche hat es schon gefunden
    await page.click("#empty-suggest [data-try]"); await pause(page);
    expect((await visibleCards(page))[0] === "wildschwein", "Vorschlag führt nicht zum Wildschwein");
  });
  await test("Vogel gesucht: Hinweis auf den Vogelkompass", async () => {
    await page.fill("#q", "Buntspecht"); await pause(page);
    expect(await page.isVisible("#empty"), "Leer-Hinweis fehlt");
    expect((await page.getAttribute("#empty-suggest a", "href")) === "https://vogelkompass.de/", "Link zum Vogelkompass fehlt");
  });
  await test("Thema gesucht: passende Seite", async () => {
    await page.fill("#q", "Trittsiegel");
    await page.waitForFunction(() => document.querySelector("#empty-suggest a.linkbtn")?.getAttribute("href").startsWith("spuren/"), null, { timeout: 3000 });
  });
  await test("Escape leert die Suche, auch direkt nach dem Tippen", async () => {
    await page.fill("#q", "Igel"); await page.keyboard.press("Escape"); await pause(page);
    expect((await page.inputValue("#q")) === "" && (await visibleCards(page)).length === 33, "Suche nicht geleert");
  });
  await test("Filter: Panel, Fokus, Gruppe, Zähler, Zurücksetzen", async () => {
    await page.click("#f-toggle");
    expect((await page.getAttribute("#f-toggle", "aria-expanded")) === "true", "aria-expanded nicht gesetzt");
    expect(await page.evaluate(() => document.activeElement.classList.contains("chip")), "Fokus nicht auf erster Filteroption");
    await page.click('.fchips .chip[data-g="grp"][data-v="Huftiere"]'); await pause(page);
    expect((await visibleCards(page)).length === 4, `Huftiere: ${await visibleCards(page)}`);
    expect((await page.getAttribute('.fchips .chip[data-v="Huftiere"]', "aria-pressed")) === "true", "aria-pressed fehlt");
    await page.click('.fchips .chip[data-g="act"][data-v="tag"]'); await pause(page);
    expect((await page.textContent("#fcount")).startsWith("2"), "Filterzähler falsch");
    await page.click("#f-done");
    expect(await page.isHidden("#fpanel") && await page.evaluate(() => document.activeElement.id === "f-toggle"), "Panel zu / Fokus zurück");
    expect((await page.$$("#active [data-rm]")).length === 3, "aktive Filter samt „Alles zurücksetzen“ fehlen");
    await page.click('#active [data-rm="all"]'); await pause(page);
    expect((await visibleCards(page)).length === 33 && await page.isHidden("#active"), "Zurücksetzen hat nicht gewirkt");
  });
  await test("„Jetzt aktiv“-Filter", async () => {
    await page.click("#f-toggle");
    await page.click('.fchips .chip[data-g="flag"][data-v="now"]'); await pause(page);
    const keys = await visibleCards(page);
    const ok = await page.$$eval("#grid > li.bird:not([hidden])", (lis, now) => lis.every((l) => l.dataset.present.split(",").map(Number).includes(now)), NOW);
    expect(keys.length > 0 && ok, "Filter zeigt Arten, die jetzt nicht aktiv sind");
    await page.click("#f-reset"); await page.click("#f-done"); await pause(page);
  });
  await test("Sortierung A–Z und nach Größe", async () => {
    await page.selectOption("#sort", "az"); await pause(page);
    const names = await page.$$eval("#grid > li.bird:not([hidden])", (l) => l.map((x) => x.dataset.name));
    expect(JSON.stringify(names) === JSON.stringify([...names].sort((a, b) => a.localeCompare(b, "de"))), "nicht alphabetisch");
    await page.selectOption("#sort", "size"); await pause(page);
    const mids = await page.$$eval("#grid > li.bird:not([hidden])", (l) => l.map((x) => Number(x.dataset.mid)));
    expect(mids.every((m, i) => !i || mids[i - 1] <= m), "nicht nach Größe");
  });
  await test("Gruppe im Kopfbereich filtert, zweiter Klick hebt auf", async () => {
    await page.click('.hchip[data-hgrp="Amphibien"]'); await pause(page, 500);
    const n = (await visibleCards(page)).length;
    expect(n > 0 && n < 33 && (await page.getAttribute('.hchip[data-hgrp="Amphibien"]', "aria-pressed")) === "true", `Amphibien: ${n}`);
    await page.click('.hchip[data-hgrp="Amphibien"]'); await pause(page);
    expect((await visibleCards(page)).length === 33, "zweiter Klick hebt nicht auf");
  });
  await test("Suche im Kopfbereich", async () => {
    await page.fill("#hq", "Igel"); await page.click(".hsearch-btn"); await pause(page, 400);
    expect((await visibleCards(page))[0] === "igel", String(await visibleCards(page)));
  });
  await test("Schnellsuche-Knopf springt auf der Startseite zum Suchfeld", async () => {
    await page.click("#navsearch");
    expect(await page.evaluate(() => ["hq", "q"].includes(document.activeElement.id)), "Fokus nicht im Suchfeld");
  });
  await test("keine Fehler auf der Startseite", async () => expect(!errors.length, errors.join("\n")));
  await close();
}
await test("Suchbegriff aus der Adresse (?q=)", async () => {
  const { page, close } = await open("/?q=luchs#arten");
  await pause(page);
  expect((await visibleCards(page))[0] === "luchs", String(await visibleCards(page)));
  await close();
});

console.log("\nSchnellsuche und Navigation auf Unterseiten");
{
  const { page, errors, close } = await open("/arten/dachs/");
  await test("Suchfenster per Knopf: Treffer und Ansage", async () => {
    await page.click("#navsearch");
    expect(await page.isVisible("#sdlg"), "Fenster nicht offen");
    await page.fill("#sq", "luchs"); await page.waitForSelector("#sresults a");
    expect((await page.getAttribute("#sresults a", "href")).endsWith("arten/luchs/"), await page.getAttribute("#sresults a", "href"));
    expect((await page.textContent("#sstatus")).includes("Treffer"), "Ansage für Screenreader fehlt");
  });
  await test("Tippfehler zeigt ähnliche Schreibweise", async () => {
    await page.fill("#sq", "Feuersalamder"); await page.waitForFunction(() => document.querySelector("#sresults")?.textContent.includes("Feuersalamander"));
  });
  await test("Escape schließt, „/“ öffnet", async () => {
    await page.keyboard.press("Escape");
    expect(!(await page.isVisible("#sdlg")), "Fenster bleibt offen");
    await page.keyboard.press("/");
    expect(await page.isVisible("#sdlg") && await page.evaluate(() => document.activeElement.id === "sq"), "„/“ öffnet die Suche nicht");
  });
  await test("Enter mit einem Treffer öffnet die Artseite", async () => {
    await page.fill("#sq", "Hirschkäfer"); await page.waitForSelector("#sresults a");
    await Promise.all([page.waitForURL("**/arten/hirschkaefer/"), page.keyboard.press("Enter")]);
  });
  await test("Menü „Bestimmen“ per Tastatur", async () => {
    await page.focus('[data-menu="bestimmen"]'); await page.keyboard.press("ArrowDown");
    expect((await page.getAttribute('[data-menu="bestimmen"]', "aria-expanded")) === "true", "Menü nicht offen");
    expect(await page.evaluate(() => document.activeElement.closest("#menu-bestimmen") !== null), "Fokus nicht im Menü");
    await page.keyboard.press("Escape");
    expect(await page.isHidden("#menu-bestimmen") && await page.evaluate(() => document.activeElement.dataset.menu === "bestimmen"), "Escape schließt nicht / Fokus nicht zurück");
  });
  await test("Menü per Klick, Klick daneben schließt", async () => {
    await page.click('[data-menu="bestimmen"]');
    expect(await page.isVisible("#menu-bestimmen"), "Menü nicht offen");
    await page.mouse.click(5, 600);
    expect(await page.isHidden("#menu-bestimmen"), "Menü bleibt offen");
  });
  await test("keine Fehler", async () => expect(!errors.length, errors.join("\n")));
  await close();
}

console.log("\nHandy");
{
  const { page, close } = await open("/arten/igel/", { mobile: true });
  await test("Lebensweise-Abschnitte starten zugeklappt und sind bedienbar", async () => {
    const st = await page.$$eval("details[data-fold]", (ds) => ds.map((d) => [d.open, d.querySelector("summary").tabIndex]));
    expect(st.length && st.every(([o, t]) => !o && t === 0), JSON.stringify(st));
    await page.click("details[data-fold] summary");
    expect(await page.$eval("details[data-fold]", (d) => d.open), "lässt sich nicht aufklappen");
  });
  await test("kein waagerechtes Scrollen", async () => {
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), "Seite breiter als der Bildschirm");
  });
  await close();
  const home = await open("/", { mobile: true });
  await test("Startseite ohne waagerechtes Scrollen", async () => {
    expect(await home.page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), "Startseite breiter als der Bildschirm");
  });
  await home.close();
}
await test("Computer: Abschnitte offen, nicht zuklappbar", async () => {
  const { page, close } = await open("/arten/igel/");
  await page.click("details[data-fold] summary");
  expect(await page.$eval("details[data-fold]", (d) => d.open), "am Computer zugeklappt");
  await close();
});

console.log("\nWaldjahr und ohne JavaScript");
await test("Kalender markiert den aktuellen Monat", async () => {
  const { page, close } = await open("/waldjahr/");
  expect(await page.$(`thead th[data-month="${NOW}"].now`), "aktueller Monat nicht markiert");
  await close();
});
await test("ohne JavaScript: alle Arten sichtbar, Links funktionieren", async () => {
  const { page, close } = await open("/", { js: false });
  expect((await visibleCards(page)).length === 33, "Arten fehlen ohne JavaScript");
  expect((await page.getAttribute('a.tab[data-menu="bestimmen"]', "href")) === "./", "„Bestimmen“ ist ohne JS kein Link");
  await close();
});
await test("404-Seite", async () => {
  const { page, close } = await open("/gibt-es-nicht/");
  expect((await page.textContent("h1")) === "Hier ist kein Tier", "falsche Fehlerseite");
  await close();
});

await browser.close();
server.close();
console.log(`\n${passed} bestanden, ${failed} fehlgeschlagen`);
process.exit(failed ? 1 : 0);
