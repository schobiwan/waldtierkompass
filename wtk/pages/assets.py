# -*- coding: utf-8 -*-
"""Dateien neben den HTML-Seiten: Suchdaten, Symbole, Manifest, Schriften, Fotos und Vorschaubilder."""
import json
import os
import shutil

from data import SPECIES, PAIRS, ACTS
from ..config import SITE, HERE, OUT, MONTHS, MSLUG
from ..helpers import write, name_of, photo_key, pair_title
from ..components import GRP_SYN, SYN
from ..icons import FAVICON, focusless

OG_RATIO = 1.91  # Vorschaubilder für soziale Netzwerke


def search_rows():
    """Suchdaten für die Schnellsuche.
    Tiere:  [Name, Schlüssel, Namen, Doppelgänger, Merkmale getrennt mit |]
    Seiten: zusätzlich [Adresse, Art der Seite, Symbol]; Symbol leer = Foto des Tiers im Schlüssel."""
    rows = []
    for sp in SPECIES:
        k = sp["k"]
        alt = " ".join(name_of(p["b"] if p["a"] == k else p["a"]) for p in PAIRS if k in (p["a"], p["b"]))
        rows.append([sp["n"], k, " ".join([sp["n"], sp["lat"], SYN.get(k, "")]), alt,
                     "|".join([sp["grp"] + " " + GRP_SYN[sp["grp"]], sp["short"], " ".join(ACTS[a] for a in sp["act"])])])

    def pg(title, href, names, marks, kind="Seite", icon="find", key=""):
        rows.append([title, key, names, "", marks, href, kind, focusless(icon) if icon else ""])

    pg("Tierspuren lesen und bestimmen", "spuren/", "Spuren Tierspuren Spurensuche Trittsiegel Fährte Fährten Fußabdruck Pfotenabdruck Abdruck Spur",
       "Fraßspuren Nuss Haselnuss Zapfen angenagt|Schnee Matsch Pfote Krallen Zehen", icon="track")
    pg("Das Waldjahr", "waldjahr/", "Waldjahr Waldkalender Kalender Jahreslauf Monat Monate",
       "Brunft Rauschzeit Ranzzeit Krötenwanderung Winterschlaf Winterruhe Laichzeit Setzzeit", icon="year")
    for m in range(1, 13):
        pg(f"Der Wald im {MONTHS[m-1]}", f"waldjahr/{MSLUG[m-1]}/", f"{MONTHS[m-1]} Wald im {MONTHS[m-1]}", "", kind="Waldjahr", icon="year")
    pg("Doppelgänger unterscheiden", "unterscheiden/", "Doppelgänger Unterschied Unterschiede unterscheiden Verwechslung verwechseln Vergleich ähnlich",
       "Reh Hirsch Marder Natter Otter", icon="pair")
    for p in PAIRS:
        pg(f"{pair_title(p)}?", f"unterscheiden/{p['k']}/", f"{name_of(p['a'])} {name_of(p['b'])} Unterschied",
           p["short"], kind="Vergleich", icon="", key=photo_key(p["a"]))
    pg("Ausrüstung für Waldbeobachter", "ausruestung/", "Ausrüstung Ausruestung Zubehör Fernglas Wildkamera Wärmebildkamera Stirnlampe Rotlicht Lupe Gips",
       "Igelhaus Fledermauskasten Futterkasten Fledermaus-Detektor Bestimmungsbuch Buch", icon="pack")
    pg("Alle Waldtiere", "arten/", "Alle Waldtiere Arten Tiere Liste Übersicht Steckbriefe", "Huftiere Raubtiere Kleinsäuger Amphibien Reptilien Insekten")
    return rows


def manifest():
    return json.dumps({
        "name": SITE, "short_name": SITE, "lang": "de", "start_url": "/", "display": "standalone",
        "background_color": "#f6efe4", "theme_color": "#dfe6cc",
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
                  {"src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}, ensure_ascii=False, indent=1)


def og_crop(src, dst, quality, top_third=False):
    """Bild auf 1.91:1 zuschneiden (mittig oder im oberen Drittel, wo meist der Kopf ist) und als JPG speichern,
    weil nicht jeder Dienst WebP anzeigt."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    w, h = im.size
    th = round(w / OG_RATIO)
    y = max(0, (h - th) // 3) if top_third else (h - th) // 2
    im.crop((0, y, w, y + th)).save(dst, quality=quality, optimize=True, progressive=True)


def copy_files(src_dir, dst_dir, suffix=""):
    os.makedirs(dst_dir, exist_ok=True)
    for f in os.listdir(src_dir):
        if f.endswith(suffix):
            shutil.copy(os.path.join(src_dir, f), os.path.join(dst_dir, f))


def build():
    write("favicon.svg", FAVICON)
    write("search.json", json.dumps(search_rows(), ensure_ascii=False, separators=(",", ":")))
    # Symbole für Browser ohne SVG-Favicon, Google-Suchergebnisse und den Startbildschirm (aus icons/, erzeugt aus favicon.svg)
    copy_files(os.path.join(HERE, "icons"), OUT)
    write("site.webmanifest", manifest())
    shutil.copytree(os.path.join(HERE, "fonts"), os.path.join(OUT, "fonts"), dirs_exist_ok=True)
    photos = os.path.join(OUT, "photos")
    copy_files(os.path.join(HERE, "photos"), photos, ".webp")
    og_crop(os.path.join(HERE, "photos_src", "wk-reh.jpg"), os.path.join(photos, "og.jpg"), quality=80)
    for sp in SPECIES:
        og_crop(os.path.join(HERE, "photos", sp["k"] + ".webp"), os.path.join(photos, f"og-{sp['k']}.jpg"), quality=78, top_third=True)
