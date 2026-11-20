// Gemeinsamer Test der Kompassseiten (Vogel-, Waldtier-, Meeres-, Gartentierkompass) – in allen Repositories gleich.
// Prüft die gebaute Website mit einem echten Browser (wie tests/e2e.mjs beim Vogelkompass):
//  1. alle Seiten, hell und dunkel: Statuscode, Titel (höchstens 70 Zeichen, keiner doppelt), Beschreibung (50–160 Zeichen),
//     genau eine h1, Bilder, JSON-LD, interne Links, Skriptfehler, Barrierefreiheit mit axe (alle Regeln wie beim Vogelkompass)
//  2. Breiten 320 bis 1280 px: kein seitliches Scrollen
// Aufruf: npm test (nach dem Build). Chrome-Pfad bei Bedarf über CHROME=/pfad/zu/chrome. Nur einen Teil: NUR=light|dark|breiten
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { chromium } from 'playwright-core';
import { serve, chromePath } from './serve.mjs';
import CONFIG from './kompass.config.mjs';

const require = createRequire(import.meta.url);
const AXE = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const server = await serve(path.resolve(import.meta.dirname, CONFIG.dist));
const B = server.url;
const browser = await chromium.launch({ executablePath: chromePath() });
let failures = 0;
const ok = (cond, msg) => { if (!cond) failures++; console.log(`${cond ? '✓' : '✗'} ${msg}`); };

async function crawl(colorScheme) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, colorScheme });
  const seen = new Set(), queue = ['/'], titles = new Map(), problems = [], axe = {};
  while (queue.length) {
    const p = queue.shift(); if (seen.has(p)) continue; seen.add(p);
    const page = await ctx.newPage(), errs = [];
    page.on('pageerror', e => errs.push(e.message));
    page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    const r = await page.goto(B + p, { waitUntil: 'networkidle' });
    if (r?.status() !== 200) problems.push(`${p}: HTTP ${r?.status()}`);
    const info = await page.evaluate(() => ({
      title: document.title, desc: document.querySelector('meta[name=description]')?.content || '',
      h1: document.querySelectorAll('h1').length,
      links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')),
      broken: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.currentSrc || i.src),
      ld: [...document.querySelectorAll('script[type="application/ld+json"]')].every(s => { try { JSON.parse(s.textContent); return true; } catch { return false; } }),
    }));
    if (info.h1 !== 1) problems.push(`${p}: ${info.h1} h1`);
    if (info.desc.length < 50 || info.desc.length > 160) problems.push(`${p}: Beschreibung hat ${info.desc.length} Zeichen`);
    if (info.title.length > 70) problems.push(`${p}: Titel hat ${info.title.length} Zeichen`);
    if (titles.has(info.title)) problems.push(`${p}: gleicher Titel wie ${titles.get(info.title)}`); titles.set(info.title, p);
    if (info.broken.length) problems.push(`${p}: Bilder fehlen ${info.broken.join(', ')}`);
    if (!info.ld) problems.push(`${p}: JSON-LD ungültig`);
    errs.forEach(e => problems.push(`${p}: Skriptfehler ${e}`));
    for (const l of info.links) {
      if (/^(https?:|mailto:|tel:|#)/.test(l)) continue;
      const u = new URL(l, B + p); if (u.origin !== B) continue;
      if (/\.\w+$/.test(u.pathname)) continue;                 // Dateien (PDF, Bilder) werden nicht gecrawlt
      if (!u.pathname.endsWith('/')) { problems.push(`${p}: Link ohne Schrägstrich ${l}`); continue; }
      if (!seen.has(u.pathname) && !queue.includes(u.pathname)) queue.push(u.pathname);
    }
    // Einblende-Animationen abschließen, sonst misst axe halb durchsichtige Karten als zu kontrastarm
    await page.evaluate(() => document.getAnimations().forEach(a => { try { a.finish(); } catch {} }));
    await page.addScriptTag({ content: AXE });
    const v = await page.evaluate(async () => (await window.axe.run(document, { resultTypes: ['violations'] }))
      .violations.map(x => ({ id: x.id, node: x.nodes[0]?.html.slice(0, 120) })));
    v.forEach(x => { (axe[x.id] ||= { node: x.node, pages: [] }).pages.push(p); });
    await page.close();
  }
  await ctx.close();
  ok(problems.length === 0, `${seen.size} Seiten (${colorScheme}): ${problems.length ? '\n    ' + problems.join('\n    ') : 'Titel, Beschreibungen, Links, Bilder, Skripte in Ordnung'}`);
  const n = Object.keys(axe).length;
  ok(!n, `Barrierefreiheit (${colorScheme}): ${n ? Object.entries(axe).map(([id, x]) => `\n    ${id} auf ${x.pages.length} Seite(n), z. B. ${x.pages[0]}: ${x.node}`).join('') : 'keine Verstöße'}`);
}

async function breiten() {
  const bad = [];
  for (const width of [320, 390, 768, 1280]) {
    const ctx = await browser.newContext({ viewport: { width, height: 800 } });
    const page = await ctx.newPage();
    for (const pg of CONFIG.perf) {
      await page.goto(`${B}/${pg.path}`, { waitUntil: 'networkidle' });
      const over = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      if (over > 1) bad.push(`${pg.name} bei ${width} px: ${over} px zu breit`);
    }
    await ctx.close();
  }
  ok(!bad.length, `Breiten 320–1280 px: ${bad.length ? '\n    ' + bad.join('\n    ') : 'kein seitliches Scrollen'}`);
}

const parts = { light: () => crawl('light'), dark: () => crawl('dark'), breiten };
try {
  for (const [name, fn] of Object.entries(parts)) if (!process.env.NUR || process.env.NUR.split(',').includes(name)) await fn();
} finally { await browser.close(); server.close(); }
console.log(failures ? `\n${failures} Prüfung(en) fehlgeschlagen` : '\nAlle Seitenprüfungen bestanden');
process.exit(failures ? 1 : 0);
