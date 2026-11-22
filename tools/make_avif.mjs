// AVIF-Fassungen der Fotos: gleiche Bildwirkung, im Schnitt rund ein Viertel kleiner als WebP.
// Browser mit AVIF laden die .avif-Datei (<picture>-Quelle in wtk/media.py), alle anderen weiter die .webp-Datei.
// Aufruf nach neuen oder geänderten Fotos: node tools/make_avif.mjs   (erzeugt nur fehlende oder veraltete Dateien)
// Qualität 60 ist im Vergleich mit doppelter Vergrößerung nicht von der WebP-Vorlage zu unterscheiden. Wird die Datei
// dabei nicht mindestens 5 % kleiner (einfache Motive wie Möwen vor glattem Himmel), geht es in Fünferschritten bis 50 herunter.
import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';

const dir = path.resolve(import.meta.dirname, '..', 'photos');
const force = process.argv.includes('--alle');
let made = 0, kept = 0, sumW = 0, sumA = 0;
for (const f of fs.readdirSync(dir).filter((f) => f.endsWith('.webp')).sort()) {
  const src = path.join(dir, f), out = src.replace(/\.webp$/, '.avif');
  const w = fs.statSync(src).size;
  if (!force && fs.existsSync(out) && fs.statSync(out).mtimeMs >= fs.statSync(src).mtimeMs) {
    kept++; sumW += w; sumA += fs.statSync(out).size; continue;
  }
  let buf;
  for (let q = 60; q >= 50; q -= 5) {
    buf = await sharp(src).avif({ quality: q, effort: 6, chromaSubsampling: '4:2:0' }).toBuffer();
    if (buf.length <= w * 0.95) break;
  }
  fs.writeFileSync(out, buf);
  made++; sumW += w; sumA += buf.length;
}
console.log(`AVIF: ${made} neu, ${kept} aktuell · zusammen ${Math.round(sumA / 1024)} KB statt ${Math.round(sumW / 1024)} KB WebP (${Math.round(100 * sumA / sumW)} %)`);
