/* IndexNow: meldet geänderte Seiten sofort an Bing, Yandex, Seznam, Naver u. a.
   (Bing speist auch die Websuche von ChatGPT und Copilot – wichtig für die Sichtbarkeit in KI-Antworten).
   Aufruf: node tools/indexnow.mjs <alter-dist-ordner> <neuer-dist-ordner>
   Ohne alten Ordner werden alle Seiten der Sitemap gemeldet. Läuft in .github/workflows/indexnow.yml.
   WAIT=1: vorher warten, bis statichost die neue Fassung ausliefert (höchstens 20 Min.). DRY=1: nur anzeigen, nichts senden. */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, relative } from 'node:path';

const HOST = 'waldtierkompass.de';
const [oldDir, newDir = 'dist'] = process.argv.slice(2);
const key = readdirSync(newDir).map(f => f.match(/^([0-9a-f]{32})\.txt$/)?.[1]).find(Boolean);
if (!key) throw new Error('IndexNow-Schlüsseldatei in dist/ fehlt');

/* Alle Seiten aus der Sitemap (nur diese sollen in den Index) */
const sitemap = readFileSync(join(newDir, 'sitemap.xml'), 'utf8');
const pages = [...sitemap.matchAll(/<loc>https:\/\/waldtierkompass\.de(\/[^<]*)<\/loc>/g)].map(m => m[1]);

const htmlOf = (dir, p) => { const f = join(dir, p, 'index.html'); return existsSync(f) ? readFileSync(f, 'utf8') : null; };
/* Erstmeldung: Hatte die alte Fassung den Schlüssel noch nicht, werden alle Seiten gemeldet */
const firstRun = !oldDir || !existsSync(join(oldDir, `${key}.txt`));
const changed = !firstRun ? pages.filter(p => htmlOf(oldDir, p) !== htmlOf(newDir, p)) : pages;

if (!changed.length) { console.log('IndexNow: keine Seite geändert, nichts zu melden.'); process.exit(0); }
const urlList = changed.map(p => `https://${HOST}${p}`);
console.log(`IndexNow: ${urlList.length} Seite(n) melden:\n${urlList.slice(0, 40).join('\n')}${urlList.length > 40 ? '\n…' : ''}`);

/* statichost baut ohne Git-Infos: daran erkennen, dass die erste geänderte Seite live genauso aussieht wie im neuen Build */
if (process.env.WAIT) {
  const probe = changed[0], want = htmlOf(newDir, probe);
  for (let i = 0; ; i++) {
    const live = await fetch(`https://${HOST}${probe}`, { cache: 'no-store' }).then(r => r.text()).catch(() => '');
    if (live === want) { console.log(`Neue Fassung ist live (${probe}).`); break; }
    if (i >= 40) { console.log('Neue Fassung nach 20 Minuten nicht erkennbar live – melde trotzdem.'); break; }
    await new Promise(r => setTimeout(r, 30_000));
  }
}

const res = process.env.DRY ? {status:200,statusText:"dry"} : await fetch('https://api.indexnow.org/indexnow', {
  method: 'POST', headers: { 'Content-Type': 'application/json; charset=utf-8' },
  body: JSON.stringify({ host: HOST, key, keyLocation: `https://${HOST}/${key}.txt`, urlList }),
});
console.log(`Antwort: ${res.status} ${res.statusText}`);
/* 200/202 = angenommen; 422 = Schlüssel noch nicht online (erster Lauf vor dem Bauen) */
if (![200, 202].includes(res.status)) process.exitCode = 1;
