# -*- coding: utf-8 -*-
"""Statischer Build des Waldtierkompass nach dem Muster von Vogelkompass.

Aufruf:  python3 build.py            → dist/ (Live-Seite, kurze Adressen wie /arten/dachs/)
         python3 build.py --preview  → preview/ (Links auf index.html, für die Vorschau im Chat)

Die Bausteine liegen in wtk/: config (Einstellungen), helpers, layout (Seitengerüst), components,
products (Werbelinks), media (Fotos und Lizenzen), pages/ (je Seitentyp ein Modul), finalize (CSS, JS, Sitemap).
"""
import os
import shutil

from wtk.config import OUT
from wtk import finalize
from wtk.pages import assets, home, species, pairs, year, tracks, gear, legal, extras


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    assets.build()
    home.build()
    species.build_all()
    pairs.build_all()
    year.build_all()
    tracks.build()
    gear.build()
    legal.build()
    extras.build()
    finalize.run()
    print("Dateien:", sum(len(fs) for _, _, fs in os.walk(OUT)))


if __name__ == "__main__":
    main()
