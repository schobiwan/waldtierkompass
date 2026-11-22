# -*- coding: utf-8 -*-
"""Prüft die Inhalte in data.py, credits.json und die Fotos: Tippfehler in Schlüsseln fallen so vor dem Build auf."""
import os
import unittest

import art
from data import SPECIES, PAIRS, PAIR_DEEP, EXT, GROUPS, HABS, ACTS, SIZES, MONTH_EVENTS
from wtk.config import HERE
from wtk.helpers import BY, CREDITS, photo_key
from wtk.products import PRODUCTS, PHOTO, GEAR_FOR, GEAR_GRP, gear_for_month
from wtk.pages.tracks import GROUPS as TRACK_GROUPS, TRACK_CM

REQUIRED = {"k", "n", "g", "lat", "grp", "act", "hab", "size", "sz", "mid", "p", "h", "hl", "short", "marks", "facts", "life", "help", "tip", "alike", "art"}


class SpeciesData(unittest.TestCase):
    def test_keys_unique(self):
        self.assertEqual(len(BY), len(SPECIES))

    def test_required_fields(self):
        for s in SPECIES:
            with self.subTest(s["k"]):
                self.assertEqual(REQUIRED - set(s), set())

    def test_values_are_known(self):
        for s in SPECIES:
            with self.subTest(s["k"]):
                self.assertIn(s["grp"], GROUPS)
                self.assertIn(s["g"], "mfn")
                self.assertIn(s["size"], SIZES)
                self.assertTrue(set(s["act"]) <= set(ACTS))
                self.assertTrue(set(s["hab"]) <= set(HABS))
                self.assertIsInstance(s["mid"], (int, float))

    def test_months(self):
        for s in SPECIES:
            with self.subTest(s["k"]):
                self.assertTrue(s["p"] and s["h"], "aktiv und Hauptzeit dürfen nicht leer sein")
                self.assertTrue(set(s["p"]) <= set(range(1, 13)))
                self.assertTrue(set(s["h"]) <= set(s["p"]), "Hauptzeit muss in der aktiven Zeit liegen")
                # Reihenfolge ist frei: Winterarten wie das Hermelin zählen über den Jahreswechsel (11, 12, 1, 2)

    # Arten, deren Doppelgänger-Verweis bewusst auf ein Paar ohne sie selbst zeigt
    ALIKE_ELSEWHERE = set()

    def test_alike_points_to_pair_with_this_species(self):
        pairs = {p["k"]: p for p in PAIRS}
        for s in SPECIES:
            if s["alike"] and s["k"] not in self.ALIKE_ELSEWHERE:
                with self.subTest(s["k"]):
                    self.assertIn(s["alike"], pairs)
                    self.assertIn(s["k"], (pairs[s["alike"]]["a"], pairs[s["alike"]]["b"]))

    def test_every_group_has_species(self):
        for g in GROUPS:
            self.assertTrue(any(s["grp"] == g for s in SPECIES), g)

    def test_track_drawings_exist(self):
        """Arten mit Trittsiegel-Angabe und Zeichnung liefern gültiges SVG."""
        for s in SPECIES:
            if art.is_track(s["art"]):
                svg = art.small_track(s["art"])
                self.assertTrue(svg.startswith("<svg") and svg.endswith("</svg>"), s["k"])


class PairData(unittest.TestCase):
    def test_pair_members_exist(self):
        for p in PAIRS:
            for k in (p["a"], p["b"]):
                with self.subTest(p["k"], art=k):
                    self.assertTrue(k in BY or k in EXT)

    def test_pair_rows_have_three_columns(self):
        for p in PAIRS:
            for row in p["rows"]:
                self.assertEqual(len(row), 3, p["k"])

    def test_deep_pairs(self):
        for k, d in PAIR_DEEP.items():
            with self.subTest(k):
                self.assertIn(k, {p["k"] for p in PAIRS})
                self.assertLessEqual(len(d["desc"]), 160)
                self.assertRegex(d["updated"], r"^\d{4}-\d\d-\d\d$")
                for _, url in d["sources"]:
                    self.assertTrue(url.startswith("https://"), url)

    def test_month_events(self):
        self.assertEqual(sorted(MONTH_EVENTS), list(range(1, 13)))
        for m, ev in MONTH_EVENTS.items():
            self.assertTrue(ev, m)


class PhotosAndCredits(unittest.TestCase):
    def needed_photos(self):
        keys = {s["k"] for s in SPECIES} | {photo_key(k) for p in PAIRS for k in (p["a"], p["b"])}
        return keys

    def test_credit_for_every_photo(self):
        for k in self.needed_photos():
            with self.subTest(k):
                self.assertIn(k, CREDITS)
                a, lic, url = CREDITS[k]
                self.assertTrue(a and lic)
                self.assertTrue(url.startswith("https://commons.wikimedia.org/"), url)

    def test_photo_files_exist(self):
        for k in self.needed_photos():
            for suffix in (".webp", "-400.webp", ".avif", "-400.avif"):
                with self.subTest(k + suffix):
                    self.assertTrue(os.path.exists(os.path.join(HERE, "photos", k + suffix)))
        for k in PHOTO:
            for suffix in (".webp", "-400.webp", ".avif", "-400.avif"):
                with self.subTest("p-" + k + suffix):
                    self.assertTrue(os.path.exists(os.path.join(HERE, "photos", f"p-{k}{suffix}")))

    def test_no_unused_credits(self):
        self.assertEqual(set(CREDITS) - self.needed_photos(), set())


class Products(unittest.TestCase):
    def test_all_picks_exist(self):
        picks = [k for ks in GEAR_FOR.values() for k in ks] + [k for ks in GEAR_GRP.values() for k in ks]
        picks += [k for m in range(1, 13) for k in gear_for_month(m)]
        self.assertTrue(set(picks) <= set(PRODUCTS), set(picks) - set(PRODUCTS))
        self.assertTrue(set(PHOTO) <= set(PRODUCTS))
        self.assertTrue(set(GEAR_FOR) <= set(BY))
        self.assertEqual(set(GEAR_GRP), set(GROUPS))

    def test_affiliate_links_carry_partner_id(self):
        for k, p in PRODUCTS.items():
            with self.subTest(k):
                self.assertTrue(p["url"].startswith("https://www.amazon.de/"))
                self.assertIn("tag=schobiwan-21", p["url"])


class Tracks(unittest.TestCase):
    def test_track_page_species(self):
        for _, _, ks in TRACK_GROUPS:
            for k in ks:
                with self.subTest(k):
                    self.assertIn(k, BY)
                    self.assertIn(k, TRACK_CM)
                    self.assertTrue(any(a in ("Trittsiegel", "Spuren") for a, _ in BY[k]["facts"]))


if __name__ == "__main__":
    unittest.main()
