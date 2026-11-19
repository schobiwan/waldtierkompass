# -*- coding: utf-8 -*-
"""Einzelne Bausteine: Grammatik, Monatsangaben, Lizenzen, Titel und Beschreibungen."""
import unittest

from data import SPECIES
from wtk.helpers import BY, mit_art, ein, pronoun, mlist, mrange, join_and, slug, first_sentence, month_state, art_of, photo_key, key_of_photo
from wtk.media import lic_url, new_tab
from wtk.finalize import clean_links
from wtk.layout import canonical, add_byline
from wtk.pages.species import species_desc, species_title
from wtk.pages.tracks import track_scale


class Grammar(unittest.TestCase):
    def test_articles(self):
        self.assertEqual(mit_art(BY["dachs"]), "der Dachs")
        self.assertEqual(mit_art(BY["dachs"], "akk"), "den Dachs")
        self.assertEqual(mit_art(BY["reh"], "dat"), "dem Reh")
        self.assertEqual(mit_art(BY["wildkatze"], "dat"), "der Wildkatze")

    def test_weak_nouns(self):
        self.assertEqual(mit_art(BY["feldhase"], "akk"), "den Feldhasen")
        self.assertEqual(mit_art(BY["waschbaer"], "dat"), "dem Waschbären")
        self.assertEqual(mit_art(BY["feldhase"]), "der Feldhase")

    def test_adjective_names(self):
        self.assertEqual(mit_art(BY["braunes-langohr"]), "das Braune Langohr")
        self.assertEqual(mit_art(BY["braunes-langohr"], "dat"), "dem Braunen Langohr")

    def test_ein_pronoun(self):
        self.assertEqual(ein("f", "dat"), "der")
        self.assertEqual(ein("m", "dat"), "dem")
        self.assertEqual(ein("f"), "eine")
        self.assertEqual([pronoun(g) for g in "mfn"], ["ihn", "sie", "es"])


class Months(unittest.TestCase):
    def test_lists(self):
        self.assertEqual(mlist([3]), "März")
        self.assertEqual(mlist([3, 4, 5]), "März, April und Mai")
        self.assertEqual(mlist(range(1, 13)), "ganzjährig")
        self.assertEqual(mrange([5, 3, 9]), "März bis September")
        self.assertEqual(join_and(["a", "b"]), "a und b")

    def test_month_state(self):
        s = {"p": [3, 4, 5], "h": [4]}
        self.assertEqual(month_state(s, 4), ("h", "Hauptzeit"))
        self.assertEqual(month_state(s, 3), ("p", "aktiv"))
        self.assertEqual(month_state(s, 1), ("", "kaum zu sehen"))


class Text(unittest.TestCase):
    def test_slug(self):
        self.assertEqual(slug("Kleinsäuger"), "kleinsaeuger")
        self.assertEqual(slug("Marder und Dachs"), "marder-und-dachs")

    def test_first_sentence(self):
        self.assertEqual(first_sentence("Eins. Zwei."), "Eins.")
        self.assertEqual(first_sentence("Nur einer"), "Nur einer.")

    def test_photo_keys(self):
        self.assertEqual(photo_key("dachs"), "dachs")
        self.assertEqual(photo_key("hund"), "x-hund")
        self.assertEqual(key_of_photo("x-hund"), "hund")
        self.assertEqual(art_of("hund"), ("canid_large", "Raubtiere"))


class Licenses(unittest.TestCase):
    def test_cc_urls(self):
        self.assertEqual(lic_url("CC BY-SA 4.0"), "https://creativecommons.org/licenses/by-sa/4.0/")
        self.assertEqual(lic_url("CC BY 2.0 de"), "https://creativecommons.org/licenses/by/2.0/de/")
        self.assertEqual(lic_url("CC0"), "https://creativecommons.org/publicdomain/zero/1.0/deed.de")
        self.assertEqual(lic_url("Public Domain"), "")

    def test_new_tab_has_screenreader_note(self):
        self.assertIn('target="_blank"', new_tab("https://x.de", "X"))
        self.assertIn("öffnet in neuem Fenster", new_tab("https://x.de", "X"))


class Links(unittest.TestCase):
    def test_clean_links(self):
        self.assertEqual(clean_links('href="../arten/dachs/index.html"'), 'href="../arten/dachs/"')
        self.assertEqual(clean_links('href="index.html#arten"'), 'href="./#arten"')
        self.assertEqual(clean_links('href="https://x.de/index.html"'), 'href="https://x.de/index.html"')
        self.assertEqual(clean_links('href="#main"'), 'href="#main"')

    def test_canonical(self):
        self.assertEqual(canonical("index.html"), "https://waldtierkompass.de/")
        self.assertEqual(canonical("arten/dachs/index.html"), "https://waldtierkompass.de/arten/dachs/")
        self.assertEqual(canonical("404.html"), "https://waldtierkompass.de/404.html")

    def test_byline_after_latin_name(self):
        out = add_byline('<h1>Dachs</h1> <p class="latin" lang="la">Meles meles</p> <p>Text</p>', "../../")
        self.assertRegex(out, r'Meles meles</p> <p class="byline">.*</p> <p>Text')


class SpeciesMeta(unittest.TestCase):
    def test_description_and_title_lengths(self):
        for s in SPECIES:
            with self.subTest(s["k"]):
                self.assertLessEqual(len(species_desc(s)), 160)
                self.assertLessEqual(len(species_title(s) + " · Waldtierkompass"), 65)
                self.assertTrue(species_title(s).startswith(s["n"]))

    def test_track_scale_bounds(self):
        self.assertEqual(track_scale("wolf"), 1.0)
        self.assertEqual(track_scale("roetelmaus"), 0.3)
        self.assertEqual(track_scale("unbekannt"), 0.6)


if __name__ == "__main__":
    unittest.main()
