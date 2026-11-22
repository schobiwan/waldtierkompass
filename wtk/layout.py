# -*- coding: utf-8 -*-
"""Seitengerüst: Kopf mit Metadaten, Navigation, Schnellsuche, Brotkrumen, Fußzeile."""
import json
import re

from data import SPECIES, PAIRS
from .config import SITE, DOMAIN, PREVIEW, AWIN_META, CONTENT_UPDATED, MONTHS, SISTER_URL, AUTHOR
from .helpers import esc, count_group
from .icons import ICON, LOGO, LOGO_USE


def ld_script(obj, safe=False):
    """Strukturdaten als <script type="application/ld+json">; safe maskiert </ im Text."""
    s = json.dumps(obj, ensure_ascii=False)
    return '<script type="application/ld+json">' + (s.replace("</", "<\\/") if safe else s) + '</script>'


LDJSON = ld_script({"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": DOMAIN + "/",
                    "inLanguage": "de-DE", "description": "Waldtiere in Deutschland bestimmen: Fotos, Trittsiegel, Doppelgänger und Waldjahr.",
                    "publisher": AUTHOR})

# ------------------------------------------------------------------ Navigation
# Hauptnavigation nach den Fragen der Besucher (wie beim Vogelkompass):
# Bestimmen ▾ (Wer ist das?) · Spuren (Wer war das?) · Waldjahr (Was ist jetzt los?) · Ausrüstung
# Ohne JavaScript führt „Bestimmen“ zur Startseite mit der Suche.
NAV = [
    dict(key="bestimmen", label="Bestimmen", icon="find", href="index.html", intro="Wer ist das?", items=[
        ("index.html#arten", "Nach Name oder Merkmal", "Suchen und filtern, z. B. „Pinselohren“"),
        ("arten/index.html#g-huftiere", "Huftiere", f"{count_group('Huftiere')} Arten, vom Reh bis zum Wildschwein"),
        ("arten/index.html#g-raubtiere", "Raubtiere", f"{count_group('Raubtiere')} Arten, vom Fuchs bis zum Luchs"),
        ("arten/index.html#g-kleinsaeuger", "Kleinsäuger", f"{count_group('Kleinsäuger')} Arten, vom Eichhörnchen bis zur Fledermaus"),
        ("arten/index.html#g-amphibien", "Amphibien, Reptilien und Insekten", f"{count_group('Amphibien', 'Reptilien', 'Insekten')} Arten, vom Feuersalamander bis zum Hirschkäfer"),
        ("unterscheiden/index.html", "Doppelgänger unterscheiden", f"{len(PAIRS)} ähnliche Arten im direkten Vergleich"),
        ("arten/index.html", "Alle Arten im Überblick", f"{len(SPECIES)} Steckbriefe nach Gruppen"),
    ]),
    dict(key="spuren", label="Spuren", icon="track", href="spuren/index.html"),
    dict(key="waldjahr", label="Waldjahr", icon="year", href="waldjahr/index.html"),
    dict(key="ausruestung", label="Ausrüstung", icon="pack", href="ausruestung/index.html"),
]
# Seiten-Schlüssel (active) → Bereich der Navigation
AREA = {"index": "bestimmen", "unterscheiden": "bestimmen", "spuren": "spuren", "waldjahr": "waldjahr", "ausruestung": "ausruestung"}
# Trennstellen für die schmale untere Leiste (unsichtbar, solange das Wort passt)
SHY = {"Bestimmen": "Bestim&shy;men", "Ausrüstung": "Aus&shy;rüstung", "Waldjahr": "Wald&shy;jahr"}


def nav_tabs(R, path, active):
    area = AREA.get(active or "")
    out = []
    for m in NAV:
        inner = f'{ICON[m["icon"]]}<span>{SHY.get(m["label"], m["label"])}</span>'
        if "items" not in m:
            cur = ' aria-current="page"' if area == m["key"] else ""
            out.append(f'<li><a class="tab" href="{R}{m["href"]}"{cur}>{inner}</a></li>')
            continue
        cur = ' aria-current="true"' if area == m["key"] else ""
        lis = "".join(f'<li><a href="{R}{h}"{" aria-current=\"page\"" if h == path else ""}><b>{t}</b><span>{d}</span></a></li>' for h, t, d in m["items"])
        out.append(f'<li class="has-menu"><a class="tab" href="{R}{m["href"]}" data-menu="{m["key"]}"{cur}>{inner}{ICON["chev"]}</a>'
                   f'<div class="mpanel" id="menu-{m["key"]}" hidden><p class="mintro">{m["intro"]}</p><ul>{lis}</ul></div></li>')
    return "".join(out)


def appnav(R, path, active):
    return (f'<nav class="appnav" aria-label="Hauptnavigation"> <div class="wrap"> <a class="brand" href="{R}index.html">{LOGO_USE}<span>{SITE}</span><span class="sr-only">, zur Startseite</span></a> '
            f'<ul class="tabs" id="tabs"> {nav_tabs(R, path, active)} </ul> '
            f'<button class="navsearch" type="button" id="navsearch" aria-haspopup="dialog" aria-controls="sdlg">{ICON["find"]}<span class="sr-only">Tier suchen</span><span class="nsl" aria-hidden="true">Suchen</span></button> </div> '
            '<div class="mbackdrop" id="mbackdrop" hidden></div> </nav>')


def search_dialog(R):
    """Fenster der Schnellsuche (quicksearch.js)."""
    return (f'<dialog class="sdlg" id="sdlg" aria-labelledby="sdlg-title"> <form method="get" action="{R}index.html" class="sform" id="sform">'
            f'<h2 class="sr-only" id="sdlg-title">Tier suchen</h2><label class="search" for="sq">{ICON["find"]}<span class="sr-only">Name oder Merkmal</span>'
            '<input type="search" id="sq" name="q" placeholder="Name oder Merkmal, z. B. Pinselohren" autocomplete="off" enterkeyhint="search"></label>'
            '<button type="button" class="sclose" id="sclose">Schließen</button></form> <p class="sr-only" id="sstatus" role="status" aria-live="polite"></p><ul class="sresults" id="sresults" aria-label="Treffer"></ul>'
            f'<p class="smore" id="smore" hidden><a id="smore-link" href="{R}index.html#arten">Alle Treffer mit Filtern anzeigen</a></p> </dialog>')


# ------------------------------------------------------------------ Fußzeile
FOOT_DISCOVER = [("arten/index.html", "Alle Waldtiere"), ("spuren/index.html", "Spuren lesen"), ("unterscheiden/index.html", "Doppelgänger unterscheiden"),
                 ("waldjahr/index.html", "Waldjahr und Kalender"), ("ausruestung/index.html", "Ausrüstung")]
FOOT_LEGAL = [("ueber/index.html", "Über den Waldtierkompass"), ("impressum/index.html", "Impressum"), ("datenschutz/index.html", "Datenschutz"),
              ("bildnachweis/index.html", "Bildnachweis und Lizenzen")]
FOOT_SISTERS = [("Vogelkompass", "Vögel bestimmen"), ("Meereskompass", "Tiere an der Küste"), ("Gartentierkompass", "Tiere im Garten")]


def footer(R):
    li = lambda xs: "".join(f'<li><a href="{R}{h}">{t}</a></li>' for h, t in xs)
    sis = "".join(f'<li><a href="{SISTER_URL[n]}" rel="noopener">{n}: {t}</a></li>' for n, t in FOOT_SISTERS)
    return (f'<footer> <div class="wrap"> <a class="flogo" href="{R}index.html">{LOGO_USE}<span>{SITE}</span></a> <div class="fcols"> '
            f'<nav aria-label="Entdecken"><p class="fhead">Entdecken</p><ul>{li(FOOT_DISCOVER)}</ul></nav> '
            f'<nav aria-label="Rechtliches"><p class="fhead">Rechtliches</p><ul>{li(FOOT_LEGAL)}</ul></nav> '
            f'<nav aria-label="Schwesterseiten"><p class="fhead">Schwesterseiten</p><ul>{sis}</ul></nav> </div> '
            f'<p class="fby">Ein privates Projekt von <a href="{R}ueber/index.html">Nico Schober</a></p> '
            '<p class="footnote">Fotos: Wikimedia Commons, unter freien Lizenzen. Trittsiegel sind eigene Zeichnungen. Mit * markierte Links sind Werbelinks. Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p> </div> </footer>')


# ------------------------------------------------------------------ Autorenzeile und Brotkrumen
# Inhaltsseiten mit Autorenzeile: Artseiten, Doppelgänger, Waldjahr, Spuren, Ausrüstung
BYLINE_PAGES = re.compile(r"^(arten/[^/]+/|unterscheiden/|waldjahr/|spuren/|ausruestung/)")


def byline(R):
    """Sichtbare Autorenzeile wie beim Vogelkompass; passt zu author in den Strukturdaten."""
    y, m, d = CONTENT_UPDATED
    return f'<p class="byline">Von <a href="{R}ueber/index.html" rel="author">Nico Schober</a> · Stand: {d}. {MONTHS[m-1]} {y}</p>'


def add_byline(body, R):
    """Autorenzeile direkt unter die Überschrift setzen (auf Artseiten unter den lateinischen Namen)."""
    m = re.search(r'</h1>\s*(<p class="latin"[^>]*>.*?</p>)?', body, flags=re.S)
    return body[:m.end()] + " " + byline(R) + body[m.end():] if m else body


def breadcrumbs(R, crumbs, canon):
    """Sichtbare Brotkrumen und dieselbe Spur als BreadcrumbList. crumbs = [(Bezeichnung, Adresse), …, (aktuelle Seite, "")]"""
    items = [f'<li><a href="{R}index.html">Start</a></li>']
    items += [f'<li><a href="{R}{href}">{esc(lab)}</a></li>' for lab, href in crumbs[:-1]]
    items.append(f'<li><span aria-current="page">{esc(crumbs[-1][0])}</span></li>')
    trail = [("Start", DOMAIN + "/")] + [(lab, DOMAIN + "/" + href.replace("index.html", "")) for lab, href in crumbs[:-1]] + [(crumbs[-1][0], canon)]
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
          {"@type": "ListItem", "position": i + 1, "name": lab, "item": u} for i, (lab, u) in enumerate(trail)]}
    return f'<nav class="crumbs wrap" aria-label="Brotkrumen"><ol> {" ".join(items)} </ol></nav>' + ld_script(ld)


# ------------------------------------------------------------------ Kopf
# Speculation Rules: Seiten der eigenen Website werden beim Hovern/Antippen vorab geladen (nur prefetch, keine Cookies, keine Fremdlinks)
SPEC_RULES = '<script type="speculationrules">{"prefetch":[{"where":{"href_matches":"/*"},"eagerness":"moderate"}]}</script>'
FONTS = ("fraunces-latin-600-normal", "figtree-latin-400-normal", "figtree-latin-700-normal")
OG_DEFAULT = "og.jpg"


def head(R, title, desc, canon, og, og_alt, og_type, is_home, noindex):
    og_w, og_h = (960, 503) if og == OG_DEFAULT else (720, 377)
    fonts = "".join(f'<link rel="preload" href="{R}fonts/{f}.woff2" as="font" type="font/woff2" crossorigin>' for f in FONTS)
    return ('<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            f'<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canon}">'
            '<meta name="theme-color" content="#dfe6cc" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#0f2418" media="(prefers-color-scheme: dark)"><meta name="color-scheme" content="light dark">'
            + ('<meta name="robots" content="noindex">' if noindex else "") +
            f'<link rel="icon" href="{R}favicon.ico" sizes="48x48"><link rel="icon" href="{R}favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="{R}apple-touch-icon.png"><link rel="manifest" href="{R}site.webmanifest">'
            + fonts +
            f'<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{SITE}"><meta property="og:locale" content="de_DE">'
            f'<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}">'
            f'<meta property="og:image" content="{DOMAIN}/photos/{og}"><meta property="og:image:width" content="{og_w}"><meta property="og:image:height" content="{og_h}">'
            f'<meta property="og:image:alt" content="{esc(og_alt or "Reh am Waldrand")}"><meta name="twitter:card" content="summary_large_image">'
            + (LDJSON + AWIN_META if is_home else "") +
            f'<link rel="stylesheet" href="{R}assets/site.css">' + SPEC_RULES + '</head>')


def canonical(path):
    return DOMAIN + "/" + (path[:-len("index.html")] if path.endswith("index.html") else path)


def page(path, title, desc, body, active=None, script="app.js", crumbs=None, is_home=False, og=OG_DEFAULT, og_alt=None, og_type="website",
         ld=None, root=None, noindex=False):
    """Ganze HTML-Seite. path relativ zur Wurzel (z. B. arten/dachs/index.html), root überschreibt den Weg zur Wurzel (404-Seite: "/")."""
    R = root if root is not None else "../" * path.count("/")
    if BYLINE_PAGES.match(path):
        body = add_byline(body, R)
    canon = canonical(path)
    cr = breadcrumbs(R, crumbs, canon) if crumbs else ""
    lds = ld_script(ld, safe=True) if ld else ""
    full_title = title if is_home or SITE in title else f"{title} · {SITE}"   # Titel mit Seitennamen (z. B. Über-Seite) ohne Zusatz
    return (f'<!DOCTYPE html><html lang="de" data-root="{R or "./"}"{"" if PREVIEW else " data-clean"}> '
            f'{head(R, full_title, desc, canon, og, og_alt, og_type, is_home, noindex)} '
            f'<body> {LOGO} <a class="skip" href="#main">Zum Inhalt springen</a> {appnav(R, path, active)} {search_dialog(R)} '
            f'<main id="main" tabindex="-1"> {cr} {body} </main> {footer(R)} '
            f'{lds}<script type="module" src="{R}assets/{script}"></script> </body> </html>')
