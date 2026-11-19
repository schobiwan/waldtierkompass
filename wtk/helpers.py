# -*- coding: utf-8 -*-
"""Kleine Hilfen: Datei schreiben, Arten nachschlagen, deutsche Grammatik, Monatsangaben."""
import html
import json
import os
import re

from data import SPECIES, PAIRS, EXT
from .config import OUT, HERE, MONTHS

BY = {s["k"]: s for s in SPECIES}
PAIRBY = {p["k"]: p for p in PAIRS}

# Bildnachweis je Foto: Schlüssel → (Urheber, Lizenz, Quelle)
with open(os.path.join(HERE, "credits.json"), encoding="utf-8") as _f:
    CREDITS = json.load(_f)


def esc(s):
    return html.escape(str(s), quote=True)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, content):
    """Datei relativ zum Ausgabeordner schreiben, Ordner bei Bedarf anlegen."""
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")).strip("-")


def ucfirst(t):
    return t[0].upper() + t[1:]


def first_sentence(t):
    return t.split(". ")[0].rstrip(".") + "."


def by_name(items):
    return sorted(items, key=lambda x: x["n"])


def in_group(*groups):
    """Arten der genannten Gruppen, nach Namen sortiert."""
    return by_name(s for s in SPECIES if s["grp"] in groups)


def count_group(*groups):
    return sum(1 for s in SPECIES if s["grp"] in groups)


def month_list(ms):
    """Monate als Daten-Attribut: 1,2,3"""
    return ",".join(map(str, ms))


# ------------------------------------------------------------------ Arten und Doppelgänger
# Doppelgänger ohne eigene Artseite stehen in EXT und haben keine Gruppe; sie bekommen die ihres Zeichentyps.
EXT_GROUP = {"felid": "Raubtiere", "canid_large": "Raubtiere", "mustelid_small": "Raubtiere", "newt": "Amphibien",
             "lizard": "Reptilien", "rodent": "Kleinsäuger"}


def animal(key):
    """Art mit eigener Seite oder externer Doppelgänger."""
    return BY[key] if key in BY else EXT[key]


def name_of(key):
    return animal(key)["n"]


def lat_of(key):
    return animal(key)["lat"]


def gender_of(key):
    return animal(key)["g"]


def art_of(key):
    """(Zeichentyp, Gruppe) einer Art oder eines Doppelgängers."""
    if key in BY:
        return BY[key]["art"], BY[key]["grp"]
    e = EXT[key]
    return e["art"], EXT_GROUP[e["art"]]


def photo_key(k):
    """Doppelgänger ohne eigene Artseite haben Fotos mit Präfix x-."""
    return k if k in BY else "x-" + k


def key_of_photo(k):
    """Umkehrung von photo_key: x-hund → hund."""
    return k[2:] if k.startswith("x-") else k


def other_of(pair, key):
    """Die andere Art eines Doppelgänger-Paars."""
    return pair["b"] if pair["a"] == key else pair["a"]


def pair_title(p):
    return f"{name_of(p['a'])} oder {name_of(p['b'])}"


def fact(s, *labels):
    """Erster Steckbrief-Eintrag mit einer der Bezeichnungen, sonst None."""
    return next((v for a, v in s["facts"] if a in labels), None)


# ------------------------------------------------------------------ Grammatik
WEAK = {"feldhase": "Feldhasen", "waschbaer": "Waschbären"}  # schwache Beugung: den Feldhasen, dem Waschbären
ARTICLE = {"nom": {"m": "der", "f": "die", "n": "das"}, "akk": {"m": "den", "f": "die", "n": "das"}, "dat": {"m": "dem", "f": "der", "n": "dem"}}


def ein(g, case="nom"):
    if case == "dat":
        return "der" if g == "f" else "dem"
    return "eine" if g == "f" else "ein"


def _adj(n, case):
    """Namen mit Adjektiv beugen: Braunes Langohr → das Braune / dem Braunen Langohr."""
    w = n.split(" ")
    if len(w) == 2 and w[0][0].isupper() and w[0].endswith(("es", "e")):
        stem = w[0][:-2] if w[0].endswith("es") else w[0][:-1]
        return f"{stem}{'en' if case == 'dat' else 'e'} {w[1]}"
    return n


def mit_art(s, case="nom"):
    """Name mit bestimmtem Artikel: der Dachs, den Dachs, dem Dachs."""
    art = ARTICLE[case][s["g"]]
    if case != "nom" and s["k"] in WEAK:
        return f"{art} {WEAK[s['k']]}"
    return f"{art} {_adj(s['n'], case)}"


def pronoun(g):
    return "sie" if g == "f" else ("es" if g == "n" else "ihn")


def join_and(items):
    """a, b und c"""
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " und " + items[-1]


# ------------------------------------------------------------------ Monate
def mlist(ms):
    ms = list(ms)
    if len(ms) == 12:
        return "ganzjährig"
    return join_and(MONTHS[m - 1] for m in ms)


def mrange(ms):
    ms = sorted(ms)
    if len(ms) == 12:
        return "ganzjährig"
    return f"{MONTHS[ms[0]-1]} bis {MONTHS[ms[-1]-1]}"


def month_state(s, m):
    """CSS-Klasse und Bezeichnung für Art s im Monat m."""
    if m in s["h"]:
        return "h", "Hauptzeit"
    return ("p", "aktiv") if m in s["p"] else ("", "kaum zu sehen")
