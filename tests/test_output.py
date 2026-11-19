# -*- coding: utf-8 -*-
"""Prüft die fertig gebaute Seite in dist/ (vorher bauen: npm run build).
Interne Links, Sprungmarken, h1, Titel und Beschreibung prüft zusätzlich tools/check.py."""
import html
import json
import os
import re
import unittest

from data import SPECIES
from wtk.config import HERE, DOMAIN

DIST = os.path.join(HERE, "dist")

# Größenbudgets in Bytes (unkomprimiert). Wer sie reißen muss, prüft vorher PageSpeed.
BUDGET = {"assets/site.css": 70_000, "assets/home.js": 20_000, "assets/app.js": 12_000, "search.json": 20_000, "index.html": 110_000}
BUDGET_PAGE = 80_000      # jede andere HTML-Seite
BUDGET_PHOTO = 200_000    # einzelnes Foto (720 px; aktuell höchstens ~165 KB, auf dem Handy lädt die 400-px-Fassung)


def pages():
    for d, _, fs in os.walk(DIST):
        for f in fs:
            if f.endswith(".html"):
                p = os.path.join(d, f)
                with open(p, encoding="utf-8") as fh:
                    yield os.path.relpath(p, DIST), fh.read()


def visible(t):
    """HTML ohne Skripte, Stile und Tags."""
    t = re.sub(r"<(script|style)\b.*?</\1>", " ", t, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


@unittest.skipUnless(os.path.isdir(DIST), "dist/ fehlt – erst bauen")
class Pages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = dict(pages())

    def test_page_count(self):
        # Start, Arten-Übersicht, Artseiten, Doppelgänger, Waldjahr + 12 Monate, Spuren, Ausrüstung, 4 Rechtsseiten, 404
        self.assertGreaterEqual(len(self.pages), 1 + 1 + len(SPECIES) + 1 + 13 + 2 + 4 + 1)

    def test_basic_structure(self):
        for rel, t in self.pages.items():
            with self.subTest(rel):
                self.assertTrue(t.startswith('<!DOCTYPE html><html lang="de"'))
                self.assertEqual(t.count("<main"), 1)
                self.assertIn('<a class="skip" href="#main">', t)
                self.assertRegex(t, r'<link rel="stylesheet" href="[^"]*assets/site\.css\?v=[0-9a-f]{8}">')
                self.assertRegex(t, r'<script type="module" src="[^"]*assets/(app|home)\.js\?v=[0-9a-f]{8}">')

    def test_no_template_leftovers(self):
        """Vergessene f-Strings oder leere Werte („{now_name}“, „None“) im sichtbaren Text oder in Attributen."""
        for rel, t in self.pages.items():
            with self.subTest(rel):
                body = re.sub(r"<script\b.*?</script>", "", t, flags=re.S)
                self.assertIsNone(re.search(r"\{[a-zA-Z_][\w\[\]\"'.]*\}", body), "Platzhalter im HTML")
                self.assertIsNone(re.search(r"\b(None|undefined|NaN)\b", visible(t)))
                self.assertNotIn('=""None', body)

    def test_images_have_alt_and_size(self):
        for rel, t in self.pages.items():
            for tag in re.findall(r"<img\b[^>]*>", t):
                with self.subTest(rel, img=tag[:80]):
                    self.assertRegex(tag, r'\salt="')
                    self.assertRegex(tag, r'\swidth="\d+"')
                    self.assertRegex(tag, r'\sheight="\d+"')

    def test_ids_unique(self):
        for rel, t in self.pages.items():
            ids = re.findall(r'\sid="([^"]+)"', t)
            dup = {i for i in ids if ids.count(i) > 1}
            self.assertEqual(dup, set(), rel)

    def test_new_windows_are_announced(self):
        for rel, t in self.pages.items():
            for a in re.findall(r'<a\b[^>]*target="_blank"[^>]*>.*?</a>', t, flags=re.S):
                with self.subTest(rel, link=a[:80]):
                    self.assertIn("neuem Fenster", a)
                    self.assertIn("noopener", a)

    def test_affiliate_links_marked(self):
        for rel, t in self.pages.items():
            for a in re.findall(r'<a\b[^>]*href="https://www\.amazon\.de/[^"]*"[^>]*>', t):
                if "nodeId=" in a:  # Datenschutzerklärung von Amazon
                    continue
                with self.subTest(rel):
                    self.assertIn('rel="sponsored nofollow noopener"', a)

    def test_json_ld_valid(self):
        for rel, t in self.pages.items():
            for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, flags=re.S):
                with self.subTest(rel):
                    data = json.loads(block)
                    self.assertEqual(data["@context"], "https://schema.org")

    def test_canonical_and_noindex(self):
        for rel, t in self.pages.items():
            with self.subTest(rel):
                canon = re.search(r'<link rel="canonical" href="([^"]+)">', t).group(1)
                self.assertTrue(canon.startswith(DOMAIN + "/"))
                self.assertEqual('<meta name="robots" content="noindex">' in t, rel == "404.html")

    def test_clean_links_on_live_site(self):
        """Live-Seite ohne index.html in internen Links (außer auf der 404-Seite mit festen Pfaden)."""
        for rel, t in self.pages.items():
            if rel == "404.html":
                continue
            with self.subTest(rel):
                self.assertIsNone(re.search(r'href="(?!https?:)[^"]*index\.html', t))


@unittest.skipUnless(os.path.isdir(DIST), "dist/ fehlt – erst bauen")
class Files(unittest.TestCase):
    def read(self, p):
        with open(os.path.join(DIST, p), encoding="utf-8") as f:
            return f.read()

    def test_search_json(self):
        rows = json.loads(self.read("search.json"))
        animals = [r for r in rows if len(r) == 5]
        topics = [r for r in rows if len(r) == 8]
        self.assertEqual(len(animals), len(SPECIES))
        self.assertEqual(len(animals) + len(topics), len(rows))
        for r in topics:
            self.assertTrue(os.path.exists(os.path.join(DIST, r[5], "index.html")), r[5])

    def test_sitemap_lists_every_page(self):
        sm = self.read("sitemap.xml")
        locs = re.findall(r"<loc>([^<]+)</loc>", sm)
        expected = {DOMAIN + "/" + (os.path.dirname(rel) + "/" if os.path.dirname(rel) else "") for rel, _ in pages() if rel.endswith("index.html")}
        self.assertEqual(set(locs), expected)
        self.assertEqual(len(locs), len(set(locs)))
        self.assertNotIn("404", sm)

    def test_robots_indexnow_manifest(self):
        self.assertIn(f"Sitemap: {DOMAIN}/sitemap.xml", self.read("robots.txt"))
        key = "5e1f0c9a7b3d4e8f9a2c6b1d0e7f3a48"
        self.assertEqual(self.read(f"{key}.txt"), key)
        m = json.loads(self.read("site.webmanifest"))
        for icon in m["icons"]:
            self.assertTrue(os.path.exists(os.path.join(DIST, icon["src"].lstrip("/"))))

    def test_social_images(self):
        self.assertTrue(os.path.exists(os.path.join(DIST, "photos", "og.jpg")))
        for s in SPECIES:
            self.assertTrue(os.path.exists(os.path.join(DIST, "photos", f"og-{s['k']}.jpg")), s["k"])

    def test_size_budgets(self):
        for p, limit in BUDGET.items():
            with self.subTest(p):
                self.assertLessEqual(os.path.getsize(os.path.join(DIST, p)), limit)
        for rel, t in pages():
            if rel != "index.html":
                with self.subTest(rel):
                    self.assertLessEqual(len(t.encode()), BUDGET_PAGE)
        for f in os.listdir(os.path.join(DIST, "photos")):
            with self.subTest(f):
                self.assertLessEqual(os.path.getsize(os.path.join(DIST, "photos", f)), BUDGET_PHOTO)


if __name__ == "__main__":
    unittest.main()
