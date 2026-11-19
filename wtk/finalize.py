# -*- coding: utf-8 -*-
"""Nach dem Erzeugen der Seiten: CSS und JavaScript bündeln, Links kürzen, Sitemap und robots.txt schreiben."""
import datetime as _dt
import hashlib
import os
import re
import subprocess

from data import PAIR_DEEP
from .config import HERE, OUT, TOOLS, PREVIEW, DOMAIN, CONTENT_ISO, INDEXNOW_KEY, CSS_SAFELIST
from .helpers import read, write

ASSETS = os.path.join(OUT, "assets")
CSS_PARTS = ("base.css", "extra.css")
JS_ENTRIES = ("app.js", "home.js")  # app.js läuft auf allen Seiten, home.js (enthält app.js) auf der Startseite


def tool(name):
    return os.path.join(TOOLS, name)


def bundle_css():
    """base.css + extra.css zusammenfügen, ungenutzte Regeln entfernen (purgecss), minifizieren (lightningcss)."""
    os.makedirs(ASSETS, exist_ok=True)
    full, purged = os.path.join(ASSETS, "_full.css"), os.path.join(ASSETS, "_purged.css")
    with open(full, "w", encoding="utf-8") as f:
        for part in CSS_PARTS:
            f.write(read(os.path.join(HERE, "src", "css", part)) + "\n")
    subprocess.run([tool("purgecss"), "--css", full, "--content", f"{OUT}/**/*.html", f"{HERE}/src/js/*.js",
                    "--safelist", *CSS_SAFELIST, "--output", purged], check=True)
    subprocess.run([tool("lightningcss"), "--minify", "--targets", ">= 0.5%", purged, "-o", os.path.join(ASSETS, "site.css")], check=True)
    os.remove(full)
    os.remove(purged)


def bundle_js():
    for f in os.listdir(ASSETS):
        if f.endswith(".js"):
            os.remove(os.path.join(ASSETS, f))
    entries = [os.path.join(HERE, "src", "js", f) for f in JS_ENTRIES]
    subprocess.run([tool("esbuild"), *entries, "--bundle", "--format=esm", "--minify", "--target=es2020",
                    "--legal-comments=none", f"--outdir={ASSETS}", "--log-level=warning"], check=True)


CLEAN_LINK = re.compile(r'href="(?![a-z]+:|#|//)([^"]*?)index\.html(#[^"]*)?"')


def clean_links(t):
    """Interne Links ohne index.html: arten/dachs/index.html → arten/dachs/, index.html#arten → ./#arten"""
    return CLEAN_LINK.sub(lambda m: f'href="{m.group(1) or "./"}{m.group(2) or ""}"', t)


def html_files():
    for d, _, fs in os.walk(OUT):
        for f in fs:
            if f.endswith(".html"):
                yield os.path.join(d, f)


def rewrite_html():
    """Ein Durchgang über alle Seiten: kurze Adressen ohne index.html (nur Live-Seite)
    und Dateiversion an CSS und JS, damit Browser nach einer Änderung nicht die alte Fassung aus dem Cache nehmen."""
    ver = {}
    for f in ("site.css",) + JS_ENTRIES:
        with open(os.path.join(ASSETS, f), "rb") as fh:
            ver[f] = hashlib.sha1(fh.read()).hexdigest()[:8]
    for fp in html_files():
        t = read(fp)
        if not PREVIEW:
            t = clean_links(t)
        for a, v in ver.items():
            t = t.replace(f'assets/{a}"', f'assets/{a}?v={v}"')
        with open(fp, "w", encoding="utf-8") as f:
            f.write(t)


def lastmod(u):
    """Änderungsdatum für Seiten, deren Inhalt ein eigenes Stand-Datum trägt."""
    m = re.search(r"/unterscheiden/([^/]+)/$", u)
    d = PAIR_DEEP.get(m.group(1)) if m else None
    return f"<lastmod>{max(d['updated'], CONTENT_ISO) if d else CONTENT_ISO}</lastmod>"


def sitemap_urls():
    urls = []
    for d, _, fs in os.walk(OUT):
        if "index.html" in fs:
            rel = os.path.relpath(d, OUT).replace(os.sep, "/")
            urls.append(DOMAIN + "/" + ("" if rel == "." else rel + "/"))
    return sorted(urls, key=lambda u: (u.count("/"), u))


def write_meta_files():
    """Sitemap (alle index.html), robots.txt, IndexNow-Schlüssel und Build-Zeitpunkt (zum Prüfen, ob die Live-Seite aktuell ist)."""
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{u}</loc>{lastmod(u)}</url>\n" for u in sitemap_urls()) + "</urlset>\n")
    write(f"{INDEXNOW_KEY}.txt", INDEXNOW_KEY)
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    write("version.txt", _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + "\n")


def run():
    bundle_css()
    bundle_js()
    rewrite_html()
    write_meta_files()
