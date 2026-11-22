// Gemeinsamer Test der Kompassseiten (Vogel-, Waldtier-, Meeres-, Gartentierkompass) – in allen Repositories gleich.
// Leistungsbudget wie beim Vogelkompass: Lighthouse (Handy, gedrosselt wie PageSpeed Insights) auf fünf wichtigen Seitentypen.
// Jede Seite läuft dreimal, gewertet wird der Median. Schlägt fehl, sobald eine Seite unter das Budget fällt,
// damit keine Änderung die Ladezeit verschlechtert. Seiten und Budgets stehen in kompass.config.mjs.
// Aufruf: npm run perf (nach dem Build). Nur die Startseite: NUR_START=1 npm run perf. Braucht Chrome und Netz für npx.
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { serve, chromePath } from './serve.mjs';
import CONFIG from './kompass.config.mjs';

// Grenzen wie beim Vogelkompass; eine Seite darf in kompass.config.mjs eigene Werte haben (score, lcp, si), wenn sie heute noch darunter liegt
const DEFAULT = { score: 95, tbt: 250, lcp: 2500, si: 2000, cls: 0.01 }, RUNS = 3;
// Auf den GitHub-Rechnern (pruefung.yml setzt PERF_TOLERANZ=1) messen Chrome und Lighthouse etwas anders als lokal:
// dort gelten 3 Punkte, 10 % Zeit und 0,01 CLS Spielraum, damit nicht jeder Messausreißer Alarm schlägt. Lokal bleibt alles streng.
const TOL = process.env.PERF_TOLERANZ ? { score: 3, zeit: 1.1, cls: 0.01 } : { score: 0, zeit: 1, cls: 0 };
const pages = process.env.NUR_START ? CONFIG.perf.slice(0, 1) : CONFIG.perf;
const server = await serve(path.resolve(import.meta.dirname, CONFIG.dist));
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'kompass-perf-'));
const median = a => [...a].sort((x, y) => x - y)[Math.floor(a.length / 2)];
let failed = 0;
try {
  for (const pg of pages) {
    const roh = { ...DEFAULT, ...pg }, runs = [];
    const lim = { ...roh, score: roh.score - TOL.score, tbt: roh.tbt * TOL.zeit, lcp: roh.lcp * TOL.zeit, si: roh.si * TOL.zeit, cls: roh.cls + TOL.cls };
    for (let i = 0; i < RUNS; i++) {
      const out = path.join(tmp, `r${i}.json`);
      // asynchron, sonst blockiert der Aufruf den Server im selben Prozess
      await promisify(execFile)('npx', ['--yes', 'lighthouse@12.8.2', `${server.url}/${pg.path}`, '--only-categories=performance', '--form-factor=mobile',
        '--output=json', `--output-path=${out}`, '--chrome-flags=--headless=new --no-sandbox', '--quiet'],
        { timeout: 180000, env: { ...process.env, CHROME_PATH: chromePath() } });
      const r = JSON.parse(fs.readFileSync(out, 'utf8')), a = r.audits;
      runs.push({ score: Math.round(r.categories.performance.score * 100), tbt: a['total-blocking-time'].numericValue,
        lcp: a['largest-contentful-paint'].numericValue, si: a['speed-index'].numericValue, cls: a['cumulative-layout-shift'].numericValue, kb: a['total-byte-weight'].numericValue / 1024 });
    }
    const m = Object.fromEntries(['score', 'tbt', 'lcp', 'si', 'cls', 'kb'].map(k => [k, median(runs.map(r => r[k]))]));
    const errs = [];
    if (m.score < lim.score) errs.push(`Punkte ${m.score} < ${lim.score}`);
    if (m.tbt > lim.tbt) errs.push(`Blockierzeit ${Math.round(m.tbt)} ms > ${Math.round(lim.tbt)}`);
    if (m.lcp > lim.lcp) errs.push(`LCP ${Math.round(m.lcp)} ms > ${Math.round(lim.lcp)}`);
    // Speed Index: fängt Einblende-Animationen ab, die den sichtbaren Aufbau verzögern
    if (m.si > lim.si) errs.push(`Speed Index ${Math.round(m.si)} ms > ${Math.round(lim.si)}`);
    if (m.cls > lim.cls) errs.push(`CLS ${m.cls.toFixed(3)} > ${lim.cls}`);
    if (m.kb > pg.kb) errs.push(`${Math.round(m.kb)} KB > ${pg.kb} KB`);
    failed += errs.length ? 1 : 0;
    console.log(`${errs.length ? '✗' : '✓'} ${pg.name.padEnd(12)} ${m.score} Punkte · TBT ${Math.round(m.tbt)} ms · LCP ${(m.lcp / 1000).toFixed(1)} s · SI ${(m.si / 1000).toFixed(1)} s · CLS ${m.cls.toFixed(3)} · ${Math.round(m.kb)} KB${errs.length ? '  → ' + errs.join(', ') : ''}`);
  }
} finally { server.close(); fs.rmSync(tmp, { recursive: true, force: true }); }
console.log(failed ? `\n${failed} Seite(n) über dem Leistungsbudget` : '\nLeistungsbudget eingehalten');
process.exit(failed ? 1 : 0);
