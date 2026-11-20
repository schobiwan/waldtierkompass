// Gemeinsamer Test der Kompassseiten (Vogel-, Waldtier-, Meeres-, Gartentierkompass) – in allen Repositories gleich.
// Kleiner statischer Server wie statichost: Ordner -> index.html, sonst 404.html, Text gzip-komprimiert.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';

const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.avif': 'image/avif', '.ico': 'image/x-icon',
  '.woff2': 'font/woff2', '.mp3': 'audio/mpeg', '.pdf': 'application/pdf', '.xml': 'application/xml', '.txt': 'text/plain',
  '.webmanifest': 'application/manifest+json' };

export function serve(root, port = 0) {
  root = path.resolve(root);
  const server = http.createServer((req, res) => {
    let file = path.join(root, decodeURIComponent(new URL(req.url, 'http://x').pathname));
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    if (!file.startsWith(root) || !fs.existsSync(file)) {
      res.writeHead(404, { 'content-type': TYPES['.html'] });
      const nf = path.join(root, '404.html');
      return res.end(fs.existsSync(nf) ? fs.readFileSync(nf) : 'Nicht gefunden');
    }
    const type = TYPES[path.extname(file)] || 'application/octet-stream';
    // Textdateien komprimiert ausliefern wie der echte Hoster, damit die Messungen in perf.mjs realistisch sind
    if (/text|javascript|json|xml|svg|manifest/.test(type) && /gzip/.test(req.headers['accept-encoding'] || '')) {
      res.writeHead(200, { 'content-type': type, 'content-encoding': 'gzip' });
      return fs.createReadStream(file).pipe(zlib.createGzip()).pipe(res);
    }
    res.writeHead(200, { 'content-type': type });
    fs.createReadStream(file).pipe(res);
  });
  return new Promise(resolve => server.listen(port, '127.0.0.1', () =>
    resolve({ url: `http://127.0.0.1:${server.address().port}`, close: () => server.close() })));
}

// Chrome für Playwright und Lighthouse: CHROME oder CHROME_PATH, sonst die üblichen Orte
export function chromePath() {
  const c = [process.env.CHROME, process.env.CHROME_PATH, process.env.CHROMIUM_PATH, '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'];
  const p = c.find(x => x && fs.existsSync(x));
  if (!p) throw new Error('Chrome nicht gefunden – Pfad mit CHROME=/pfad/zu/chrome angeben');
  return p;
}
