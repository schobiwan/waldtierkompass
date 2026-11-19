# -*- coding: utf-8 -*-
"""Fehlerseite, Cache-Header für statichost und llms.txt (übernommen vom Vogelkompass)."""
from data import SPECIES, PAIRS, GROUPS
from ..config import SITE, DOMAIN, SISTER_URL
from ..helpers import write, in_group
from ..layout import page

HEADERS = """# Waldtierkompass – Header für statichost.eu (Format wie beim Vogelkompass)
*
    X-Content-Type-Options: nosniff
    Referrer-Policy: strict-origin-when-cross-origin
/assets/*
    Cache-Control: public, max-age=31536000, immutable
/fonts/*
    Cache-Control: public, max-age=31536000, immutable
/photos/*
    Cache-Control: public, max-age=2592000
"""

LLMS_SISTERS = [("Vogelkompass", "Vögel bestimmen"), ("Meereskompass", "Tiere an Nord- und Ostsee"), ("Gartentierkompass", "Tiere im Garten bestimmen")]


def not_found():
    links = [("/index.html", "Zur Startseite", "Tier suchen und nach Gruppe filtern"),
             ("/arten/index.html", f"Alle {len(SPECIES)} Arten", "Steckbriefe nach Gruppen"),
             ("/spuren/index.html", "Spuren lesen", "Trittsiegel und andere Hinweise"),
             ("/waldjahr/index.html", "Waldjahr", "Was im Wald gerade los ist")]
    body = ('<section class="block page"><div class="wrap prose"><h1>Hier ist kein Tier</h1>'
            '<p>Die Seite, die du suchst, gibt es nicht oder nicht mehr. Vielleicht hilft dir einer dieser Wege weiter:</p>'
            '<ul class="explore">' + "".join(f'<li><a href="{h}"><b>{t}</b><span>{d}</span></a></li>' for h, t, d in links) + '</ul></div></section>')
    write("404.html", page("404.html", "Seite nicht gefunden", "Diese Seite gibt es nicht.", body, root="/", noindex=True))


def llms_txt():
    lines = [f"# {SITE}", "",
             f"> Waldtiere in Deutschland erkennen: {len(SPECIES)} Arten mit Foto, Merkmalen, Spuren und Aktivität im Jahresverlauf, dazu {len(PAIRS)} Vergleiche ähnlicher Arten. "
             "Privates, unabhängiges Angebot von Nico Schober aus Bremen. Fotos von Wikimedia Commons.", "",
             "Sprache: Deutsch. Angaben zu Aktivität und Jahreszeiten sind grobe Richtwerte für Deutschland.", "",
             "## Bestimmen",
             f"- [Tier suchen]({DOMAIN}/): Suche nach Name oder Merkmal, Filter nach Gruppe und Aktivität",
             f"- [Alle Arten]({DOMAIN}/arten/): Steckbriefe nach Gruppen",
             f"- [Doppelgänger unterscheiden]({DOMAIN}/unterscheiden/): ähnliche Arten im direkten Vergleich",
             f"- [Spuren lesen]({DOMAIN}/spuren/): Trittsiegel und andere Hinweise",
             f"- [Waldjahr]({DOMAIN}/waldjahr/): welche Tiere in welchem Monat aktiv sind",
             f"- [Ausrüstung]({DOMAIN}/ausruestung/): Fernglas, Wildkamera, Bestimmungsbücher",
             f"- [Über den Waldtierkompass]({DOMAIN}/ueber/): wer die Seite macht, Quellen und Finanzierung", ""]
    for g in GROUPS:
        xs = in_group(g)
        if not xs:
            continue
        lines.append(f"## {g}")
        lines += [f"- [{x['n']}]({DOMAIN}/arten/{x['k']}/): {x['short']}" for x in xs]
        lines.append("")
    lines += ["## Schwesterseiten"] + [f"- [{n}]({SISTER_URL[n]}): {d}" for n, d in LLMS_SISTERS] + [""]
    write("llms.txt", "\n".join(lines))


def build():
    not_found()
    write("_headers", HEADERS)
    llms_txt()
