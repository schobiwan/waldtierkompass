# -*- coding: utf-8 -*-
"""Statischer Build des Waldtierkompass nach dem Muster von Vogelkompass."""
import os, json, shutil, html, random, subprocess
from data import SPECIES, PAIRS, EXT, GROUPS, HABS, ACTS, SIZES, MONTH_EVENTS
import art
CREDITS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "credits.json"), encoding="utf-8"))

SITE = "Waldtierkompass"
DOMAIN = "https://waldtierkompass.de"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
MSHORT = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
MSLUG = ["januar", "februar", "maerz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember"]
BY = {s["k"]: s for s in SPECIES}
PAIRBY = {p["k"]: p for p in PAIRS}
TAG = "schobiwan-21"

esc = lambda s: html.escape(str(s), quote=True)

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def art_of(key):
    if key in BY:
        return BY[key]["art"], BY[key]["grp"]
    e = EXT[key]
    grp = {"felid": "Raubtiere", "canid_large": "Raubtiere", "mustelid_small": "Raubtiere", "newt": "Amphibien",
           "lizard": "Reptilien", "rodent": "Kleinsäuger"}[e["art"]]
    return e["art"], grp

def name_of(key):
    return BY[key]["n"] if key in BY else EXT[key]["n"]

def lat_of(key):
    return BY[key]["lat"] if key in BY else EXT[key]["lat"]

def ein(g, case="nom"):
    if case == "dat":
        return "der" if g == "f" else "dem"
    return "eine" if g == "f" else "ein"

def mlist(ms):
    ms = list(ms)
    if len(ms) == 12:
        return "ganzjährig"
    names = [MONTHS[m - 1] for m in ms]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " und " + names[-1]

def mrange(ms):
    ms = sorted(ms)
    if len(ms) == 12:
        return "ganzjährig"
    return f"{MONTHS[ms[0]-1]} bis {MONTHS[ms[-1]-1]}"

# ------------------------------------------------------------------ Icons
ICON = {
 "find": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/></svg>',
 "track": '<svg viewBox="0 0 24 24" aria-hidden="true"><ellipse cx="12" cy="15.5" rx="4" ry="3.5"/><circle cx="6.5" cy="10" r="1.7"/><circle cx="10" cy="6.5" r="1.7"/><circle cx="14" cy="6.5" r="1.7"/><circle cx="17.5" cy="10" r="1.7"/></svg>',
 "pair": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="6" width="8" height="12" rx="2"/><rect x="13" y="6" width="8" height="12" rx="2"/></svg>',
 "year": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>',
 "arrow": '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"></path></svg>',
 "moon": '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10.5 2.5a5.5 5.5 0 1 0 3 9.6A6 6 0 0 1 10.5 2.5z" fill="currentColor" stroke="none"/></svg>',
 "sun": '<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="3"/><path d="M8 1.5v2M8 12.5v2M1.5 8h2M12.5 8h2M3.4 3.4l1.4 1.4M11.2 11.2l1.4 1.4M3.4 12.6l1.4-1.4M11.2 4.8l1.4-1.4"/></svg>',
 "dusk": '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 11.5h12M4 11.5a4 4 0 0 1 8 0M8 3.5v2M3.2 6.2l1.3 1.1M12.8 6.2l-1.3 1.1"/></svg>',
}
ACT_ICON = {"tag": "sun", "daemmerung": "dusk", "nacht": "moon"}

def icon_symbols():
    out = []
    for k in ("sun", "dusk", "moon"):
        inner = ICON[k].split(">", 1)[1].rsplit("</svg>", 1)[0]
        out.append(f'<symbol id="i-{k}" viewBox="0 0 16 16">{inner}</symbol>')
    return "".join(out)

def act_svg(a):
    return f'<svg aria-hidden="true"><use href="#i-{ACT_ICON[a]}"></use></svg>'

PAW = ('<path d="M24 25c4 0 6.5 3 6.5 5.6 0 2.6-2.4 3.6-6.5 2.8-4.1.8-6.5-.2-6.5-2.8 0-2.6 2.5-5.6 6.5-5.6z"/>'
       '<ellipse cx="20.6" cy="17.6" rx="2.3" ry="3"/><ellipse cx="27.4" cy="17.6" rx="2.3" ry="3"/>'
       '<ellipse cx="15.8" cy="22.6" rx="2.1" ry="2.7" transform="rotate(-25 15.8 22.6)"/>'
       '<ellipse cx="32.2" cy="22.6" rx="2.1" ry="2.7" transform="rotate(25 32.2 22.6)"/>')
LOGO = ('<svg class="logo-defs" aria-hidden="true" focusable="false"><symbol id="logo-mark" viewBox="0 0 48 48">'
        '<circle cx="24" cy="24" r="21" fill="none" stroke="currentColor" stroke-width="2.2"></circle>'
        '<circle cx="24" cy="24" r="17" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 2.5" stroke-opacity=".6"></circle>'
        '<g fill="currentColor">' + PAW + '</g><path d="M24 1.8 26.6 7.4H21.4z" fill="var(--logo-accent)"></path>'
        '</symbol>' + icon_symbols() + '</svg>')

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="11" fill="#3b2a20"/>'
           '<circle cx="24" cy="25" r="17.5" fill="none" stroke="#f6efe4" stroke-width="2.4"/>'
           '<g fill="#f6efe4" transform="translate(0 1)">' + PAW + '</g><path d="M24 4.5 27 10.5H21z" fill="#e8a24a"/></svg>')

LDJSON = ('<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": DOMAIN + "/",
          "inLanguage": "de-DE", "description": "Waldtiere in Deutschland bestimmen: Fotos, Trittsiegel, Doppelgänger und Waldjahr."}, ensure_ascii=False) + '</script>')

TABS = [("index", "Bestimmen", "Arten", "find"), ("spuren", "Spuren", "Spuren", "track"),
        ("unterscheiden", "Doppelgänger", "Vergleich", "pair"), ("waldjahr", "Waldjahr", "Jahr", "year")]

# ------------------------------------------------------------------ Layout
def page(path, title, desc, body, active=None, scripts=(), crumbs=None, data=None, is_home=False, og="og.jpg"):
    depth = path.count("/")
    R = "../" * depth
    canon = DOMAIN + "/" + (path[:-len("index.html")] if path.endswith("index.html") else path)
    tabs = []
    for key, label, short, ic in TABS:
        href = R + ("index.html" if key == "index" else f"{key}/index.html")
        cur = ' aria-current="page"' if active == key else ""
        tabs.append(f'<li><a class="tab" href="{href}"{cur}> {ICON[ic]}<span class="tl">{label}</span><span class="ts">{short}</span> </a></li>')
    cr = ""
    if crumbs:
        items = [f'<li><a href="{R}index.html">Start</a></li>']
        for (lab, href) in crumbs[:-1]:
            items.append(f'<li><a href="{R}{href}">{esc(lab)}</a></li>')
        items.append(f'<li><span aria-current="page">{esc(crumbs[-1][0])}</span></li>')
        cr = f'<nav class="crumbs wrap" aria-label="Brotkrumen"><ol> {" ".join(items)} </ol></nav>'
    dj = f'<script type="application/json" id="wk-data">{json.dumps(data, ensure_ascii=False)}</script>' if data is not None else ""
    sc = f'<script type="module" src="{R}assets/{(scripts[0] if scripts else "app.js")}"></script>'
    full_title = title if is_home else f"{title} · {SITE}"
    return f'''<!DOCTYPE html><html lang="de" data-root="{R or './'}" data-index> <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>{esc(full_title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canon}"><meta name="theme-color" content="#eadbc4" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#1f1612" media="(prefers-color-scheme: dark)"><meta name="color-scheme" content="light dark"><link rel="icon" href="{R}favicon.svg" type="image/svg+xml"><link rel="preload" href="{R}fonts/fraunces-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="{R}fonts/figtree-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin><meta property="og:type" content="website"><meta property="og:site_name" content="{SITE}"><meta property="og:locale" content="de_DE"><meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{DOMAIN}/photos/{og}"><meta name="twitter:card" content="summary_large_image">{LDJSON if is_home else ""}<link rel="stylesheet" href="{R}assets/site.css"></head> <body> {LOGO} <a class="skip" href="#main">Zum Inhalt springen</a> <nav class="appnav" aria-label="Hauptnavigation"> <div class="wrap"> <a class="brand" href="{R}index.html"><svg class="logo" aria-hidden="true"><use href="#logo-mark"></use></svg><span>{SITE}</span><span class="sr-only">, zur Startseite</span></a> <ul class="tabs"> {"".join(tabs)} </ul> </div> </nav> <main id="main" tabindex="-1"> {cr} {body} </main> {footer(R)} {dj}{sc} </body> </html>'''

def footer(R):
    ent = [("arten/index.html", "Alle Waldtiere"), ("spuren/index.html", "Spuren lesen"), ("unterscheiden/index.html", "Doppelgänger unterscheiden"),
           ("waldjahr/index.html", "Waldjahr und Kalender"), ("ausruestung/index.html", "Ausrüstung")]
    leg = [("impressum/index.html", "Impressum"), ("datenschutz/index.html", "Datenschutz"), ("bildnachweis/index.html", "Bildnachweis und Lizenzen")]
    li = lambda xs: "".join(f'<li><a href="{R}{h}">{t}</a></li>' for h, t in xs)
    return f'''<footer> <div class="wrap"> <a class="flogo" href="{R}index.html"><svg class="logo" aria-hidden="true"><use href="#logo-mark"></use></svg><span>{SITE}</span></a> <div class="fcols"> <nav aria-label="Entdecken"><p class="fhead">Entdecken</p><ul>{li(ent)}</ul></nav> <nav aria-label="Rechtliches"><p class="fhead">Rechtliches</p><ul>{li(leg)}</ul></nav> <nav aria-label="Schwesterseite"><p class="fhead">Schwesterseite</p><ul><li><a href="https://vogelkompass.de/" rel="noopener">Vogelkompass: Vögel bestimmen</a></li></ul></nav> </div> <p class="footnote">Fotos: Wikimedia Commons, unter freien Lizenzen. Trittsiegel sind eigene Zeichnungen. Mit * markierte Links sind Werbelinks. Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p> </div> </footer>'''

# ------------------------------------------------------------------ Bausteine
def img(R, key, alt="", eager=False, cls="", sizes="(max-width: 600px) 92vw, 400px"):
    lz = "eager" if eager else "lazy"
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{R}photos/{key}.webp" srcset="{R}photos/{key}-400.webp 400w, {R}photos/{key}.webp 720w" sizes="{sizes}" '
            f'alt="{esc(alt)}" width="720" height="576" loading="{lz}" decoding="async">')

def lic_url(lic):
    """Link auf den Lizenztext (Creative Commons verlangt ihn bei jeder Nutzung)."""
    import re as _re
    m = _re.match(r"CC (BY(?:-SA)?) (\d\.\d)(?: (\w\w))?$", lic)
    if m:
        return f"https://creativecommons.org/licenses/{m.group(1).lower()}/{m.group(2)}/" + (f"{m.group(3)}/" if m.group(3) else "")
    if lic == "CC0":
        return "https://creativecommons.org/publicdomain/zero/1.0/deed.de"
    return ""

def lic_link(lic):
    u = lic_url(lic)
    return f'<a href="{u}" target="_blank" rel="noopener license">{esc(lic)}</a>' if u else esc(lic)

def credit_parts(a, lic, url):
    return (f'Foto: <a href="{esc(url)}" target="_blank" rel="noopener">{esc(a)}</a>, {lic_link(lic)}')

def credit(key, short=False):
    a, lic, url = CREDITS[key]
    return credit_parts(a, lic, url) + ("" if short else ", Wikimedia Commons, zugeschnitten")

def cred(key):
    """Kleine Bildangabe direkt auf dem Foto, liegt über dem Kartenlink."""
    return f'<small class="cred">{credit(key, True)}</small>'

def card(R, s, i=0, hidden=False):
    acts = "".join(f'<span class="act" title="{ACTS[a]}">{act_svg(a)}<span class="sr-only">{ACTS[a]}</span></span>' for a in s["act"])
    search = " ".join([s["n"], s["lat"], s["grp"]] + [ACTS[a] for a in s["act"]])
    return (f'<li class="bird" id="{s["k"]}" style="--i:{i}" data-key="{s["k"]}" data-name="{esc(s["n"])}" data-search="{esc(search)}" '
            f'data-grp="{esc(s["grp"])}" data-act="{"|".join(s["act"])}" data-hab="{esc("|".join(s["hab"]))}" data-size="{s["size"]}" data-mid="{s["mid"]}" '
            f'data-present="{",".join(map(str, s["p"]))}" data-peak="{",".join(map(str, s["h"]))}"{" hidden" if hidden else ""}> '
            f'{img(R, s["k"], "", eager=i < 6)}{cred(s["k"])} <div class="txt"> <h3><a class="open" href="{R}arten/{s["k"]}/index.html">{esc(s["n"])}</a></h3> '
            f'<span class="meta"><span class="latin" lang="la">{esc(s["lat"])}</span><span class="size">{esc(s["sz"])}</span></span> '
            f'<span class="row"><span class="tag status">{esc(s["grp"])}</span></span> <p class="short">{esc(s["short"])}</p> </div> '
            f'<span class="acts">{acts}</span> </li>')

def months_bar(s):
    out = []
    for m in range(1, 13):
        cls = "h" if m in s["h"] else ("p" if m in s["p"] else "")
        t = "Hauptzeit" if cls == "h" else ("aktiv" if cls == "p" else "kaum zu sehen")
        out.append(f'<span data-month="{m}" class="{cls}" title="{MONTHS[m-1]}: {t}">{MSHORT[m-1]}</span>')
    return f'<div class="months" aria-hidden="true"> {"".join(out)} </div>'

PRODUCTS = {
 "fernglas": dict(cat="Fernglas", name="Celestron Nature DX 8x42", by="Celestron", tip=True, icon="binoc",
   why="Helles Einsteigerglas für die Dämmerung: 8-fache Vergrößerung, wasserdicht und leicht genug für lange Ansitze.",
   url="https://www.amazon.de/dp/B00B73JONS?tag=" + TAG),
 "wildkamera": dict(cat="Wildkamera", name="Wildkamera mit Nachtsicht", by="Auswahl bei Amazon", tip=True, icon="cam",
   why="Zeigt dir, wer nachts am Bau oder an der Futterstelle vorbeikommt. Achte auf unsichtbares Infrarot (No-Glow), damit die Tiere nicht gestört werden.",
   url="https://www.amazon.de/s?k=wildkamera+no+glow&tag=" + TAG),
 "lampe": dict(cat="Stirnlampe", name="Stirnlampe mit Rotlicht", by="Auswahl bei Amazon", tip=False, icon="lamp",
   why="Rotes Licht blendet Tiere kaum und schont deine Nachtsicht, ideal für Kröten- und Salamanderabende.",
   url="https://www.amazon.de/s?k=stirnlampe+rotlicht&tag=" + TAG),
 "buch": dict(cat="Buch", name="Bestimmungsbuch Tierspuren", by="Auswahl bei Amazon", tip=True, icon="book",
   why="Ein Spurenführer mit Zeichnungen der Trittsiegel in Originalgröße hilft draußen beim Vergleichen.",
   url="https://www.amazon.de/s?k=tierspuren+bestimmen+buch&tag=" + TAG),
 "detektor": dict(cat="Zubehör", name="Fledermaus-Detektor", by="Auswahl bei Amazon", tip=False, icon="wave",
   why="Macht die Ultraschallrufe der Fledermäuse hörbar. Schon einfache Geräte zeigen, wer über dem Weg jagt.",
   url="https://www.amazon.de/s?k=fledermaus+detektor&tag=" + TAG),
 "lupe": dict(cat="Zubehör", name="Einschlaglupe 10-fach", by="Auswahl bei Amazon", tip=False, icon="lens",
   why="Für Fraßspuren an Nüssen und Zapfen: Zahnspuren werden mit der Lupe eindeutig.",
   url="https://www.amazon.de/s?k=einschlaglupe+10x&tag=" + TAG),
 "waermebild": dict(cat="Wärmebild", name="Wärmebildkamera für Naturbeobachtung", by="Auswahl bei Amazon", tip=False, icon="binoc",
   why="Zeigt warme Tierkörper auch in völliger Dunkelheit und hinter dünnem Gebüsch. So entdeckst du Reh, Fuchs oder Dachs, ohne Licht zu machen.",
   url="https://www.amazon.de/s?k=w%C3%A4rmebildkamera+monokular&tag=" + TAG),
 "gips": dict(cat="Spuren", name="Modellgips für Spurenabdrücke", by="Auswahl bei Amazon", tip=False, icon="book",
   why="Mit etwas Gips hältst du ein Trittsiegel aus dem Matsch dauerhaft fest. Ein schönes Projekt für Kinder und Spurensammler.",
   url="https://www.amazon.de/s?k=modellgips&tag=" + TAG),
 "igelhaus": dict(cat="Garten", name="Igelhaus für den Garten", by="Auswahl bei Amazon", tip=False, icon="book",
   why="Ein geschützter Platz für den Winterschlaf. Stelle es an eine ruhige, schattige Stelle unter Hecken oder Laub.",
   url="https://www.amazon.de/s?k=igelhaus+winterfest&tag=" + TAG),
 "fledermauskasten": dict(cat="Garten", name="Fledermauskasten aus Holzbeton", by="Auswahl bei Amazon", tip=False, icon="wave",
   why="Ersatzquartier für Fledermäuse wie das Braune Langohr. In drei bis fünf Metern Höhe aufhängen, möglichst ohne Lampe in der Nähe.",
   url="https://www.amazon.de/s?k=fledermauskasten+holzbeton&tag=" + TAG),
 "futterkasten": dict(cat="Garten", name="Futterkasten für Eichhörnchen", by="Auswahl bei Amazon", tip=False, icon="book",
   why="Mit Klappdeckel, damit Vögel nicht mitfressen. Am Baumstamm aufgehängt, siehst du die Kletterer aus nächster Nähe.",
   url="https://www.amazon.de/s?k=eichh%C3%B6rnchen+futterkasten&tag=" + TAG),
}
PHOTO = {
 "wildkamera": ("DYVER", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Wildkamera_mit_Bewegungsmelder_%26_Nachtsicht_-_1.jpg"),
 "lampe": ("jd", "Public Domain", "https://commons.wikimedia.org/wiki/File:Petzl_Tikka.jpeg"),
 "buch": ("Dat doris", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Tierspuren_im_Sand.JPG"),
 "detektor": ("Gilles San Martin", "CC BY-SA 2.0", "https://commons.wikimedia.org/wiki/File:Bat_detector_(2861898848).jpg"),
 "lupe": ("KENPEI", "CC BY-SA 3.0", "https://commons.wikimedia.org/wiki/File:Loupe.jpg"),
 "gips": ("Gormo", "CC0", "https://commons.wikimedia.org/wiki/File:Procyon_lotor_tracks_in_mud.jpg"),
 "waermebild": ("Vitaly V. Kuzmin", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:PT-2_thermal_imaging_monocular.jpg"),
 "igelhaus": ("14GTR", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Insect_%26_hedgehog_hotel,_Manor_Corner,_Bristol.jpg"),
 "fledermauskasten": ("Marie-Lan Taÿ Pamart", "CC BY 4.0", "https://commons.wikimedia.org/wiki/File:Schwegler_Bat_Box_2FN_Chanteraines.jpg"),
 "futterkasten": ("Richard Webb", "CC BY-SA 2.0", "https://commons.wikimedia.org/wiki/File:Squirrel_feeder_in_use_-_geograph.org.uk_-_7138613.jpg"),
}
GEAR_GRP = {
 "Huftiere": ["fernglas", "wildkamera", "waermebild"],
 "Raubtiere": ["wildkamera", "waermebild", "gips"],
 "Kleinsäuger": ["wildkamera", "lupe", "buch"],
 "Amphibien": ["lampe", "buch", "lupe"],
 "Reptilien": ["fernglas", "buch", "lupe"],
 "Insekten": ["lupe", "buch", "fernglas"],
}
GEAR_FOR = {
 "igel": ["igelhaus", "wildkamera", "lampe"],
 "braunes-langohr": ["fledermauskasten", "detektor", "lampe"],
 "eichhoernchen": ["futterkasten", "fernglas", "lupe"],
 "siebenschlaefer": ["wildkamera", "lampe", "lupe"],
 "haselmaus": ["lupe", "wildkamera", "buch"],
 "rotfuchs": ["wildkamera", "waermebild", "gips"],
 "wolf": ["gips", "buch", "wildkamera"],
}
PICON = {
 "binoc": '<circle cx="8" cy="15" r="4.5"/><circle cx="16" cy="15" r="4.5"/><path d="M8 10.5V6h3v6M16 10.5V6h-3v6"/>',
 "cam": '<rect x="4" y="5" width="16" height="15" rx="3"/><circle cx="12" cy="12" r="3.5"/><circle cx="12" cy="12" r="1"/><path d="M8 17h8"/>',
 "lamp": '<path d="M4 12c0-2 2-3 8-3s8 1 8 3"/><rect x="9" y="9" width="6" height="5" rx="1.5"/><path d="M12 14v2M7 19l2-3M17 19l-2-3"/>',
 "book": '<path d="M4 5h6a2 2 0 0 1 2 2v12a2 2 0 0 0-2-2H4zM20 5h-6a2 2 0 0 0-2 2v12a2 2 0 0 1 2-2h6z"/>',
 "wave": '<path d="M3 12h2l2-5 3 10 3-12 3 10 2-3h3"/>',
 "lens": '<circle cx="10" cy="10" r="5.5"/><path d="m14 14 6 6"/>',
}

def product(R, key, compact=False):
    p = PRODUCTS[key]
    tip = '<span class="ptip">Unser Tipp</span>' if p["tip"] and not compact else ""
    why = f'<p class="pwhy">{esc(p["why"])}</p>' if not compact else ""
    meta = f'<span>{p["cat"]}{" · Unser Tipp" if (p["tip"] and compact) else ""}</span>'
    pic = (f'<img src="{R}photos/p-{key}-400.webp" srcset="{R}photos/p-{key}-400.webp 400w, {R}photos/p-{key}.webp 720w" '
           f'sizes="{"88px" if compact else "(max-width: 600px) 92vw, 360px"}" alt="" width="400" height="300" loading="lazy" decoding="async">'
) if key in PHOTO else f'<span class="picon"><svg viewBox="0 0 24 24" aria-hidden="true">{PICON[p["icon"]]}</svg></span>'
    under = f'<small class="pcred">Beispielfoto · {credit_parts(*PHOTO[key])}</small>' if (key in PHOTO and not compact) else ""
    return (f'<li class="product{" pick" if p["tip"] else ""}"> <div class="pimg">{pic}{tip}</div>{under} '
            f'<div class="pbody"> <p class="pmeta">{meta}<span class="pad">Anzeige</span></p> <h3 class="pname">{esc(p["name"])}</h3> <p class="pby">{esc(p["by"])}</p> {why} {f'<small class="pcred2">Beispielfoto · {credit_parts(*PHOTO[key])}</small>' if (compact and key in PHOTO) else ""} '
            f'<a class="plink" href="{p["url"]}" target="_blank" rel="sponsored nofollow noopener"><span>Bei Amazon ansehen<span aria-hidden="true">*</span></span>{ICON["arrow"]}'
            f'<span class="sr-only"> {esc(p["name"])} (Werbelink, öffnet in neuem Fenster)</span></a> </div> </li>')

ADNOTE = '<p class="adnote"><span aria-hidden="true">*</span> Werbelink: Wenn du über diesen Link etwas kaufst, erhält der Waldtierkompass eine kleine Provision von Amazon. Für dich ändert sich am Preis nichts. Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p>'

def pair_card(R, p, h="h2"):
    figs = "".join(f'<figure>{img(R, k if k in BY else "x-" + k)}<figcaption>{esc(name_of(k))}<small>{credit(k if k in BY else "x-" + k, True)}</small></figcaption></figure>' for k in (p["a"], p["b"]))
    return (f'<li class="pair"> <div class="ph" aria-hidden="true"> {figs} </div> <div class="pb"> <{h}><a class="pair-link" href="{R}unterscheiden/{p["k"]}/index.html">'
            f'{esc(name_of(p["a"]))} oder {esc(name_of(p["b"]))}?</a></{h}> <p>{esc(p["short"])}</p> <span class="to" aria-hidden="true">Alle Unterschiede</span> </div> </li>')

def chipset(legend, g, items):
    return f'<fieldset><legend>{legend}</legend><div class="fchips">' + "".join(
        f'<button class="chip" type="button" data-g="{g}" data-v="{esc(v)}" aria-pressed="false">{esc(t)}</button>' for v, t in items) + '</div></fieldset>'

# ------------------------------------------------------------------ Seiten
def build_home():
    R = ""
    filt = (chipset("Gruppe", "grp", [(g, g) for g in GROUPS]) +
            chipset("Aktiv", "act", [(k, v) for k, v in ACTS.items()]) +
            chipset("Lebensraum", "hab", [(h, h) for h in HABS]) +
            chipset("Größe", "size", list(SIZES.items())) +
            '<fieldset><legend>Außerdem</legend><div class="fchips"><button class="chip" type="button" data-g="flag" data-v="now" aria-pressed="false">Jetzt im <span data-now-name>November</span> aktiv</button>'
            '</div></fieldset>')
    cards = "".join(card(R, s, i) for i, s in enumerate(sorted(SPECIES, key=lambda x: x["n"])))
    NOWM_BUILD = 11
    ranked = sorted(SPECIES, key=lambda x: (0 if NOWM_BUILD in x["h"] else 1, x["n"]))
    def nowcard(x, i):
        first = x["hl"].split(". ")[0].rstrip(".") + "."
        return (f'<li data-peak="{",".join(map(str, x["h"]))}" data-present="{",".join(map(str, x["p"]))}" data-k="{x["k"]}" data-name="{esc(x["n"])}" '
                f'data-hl="{esc(first)}"{"" if NOWM_BUILD in x["p"] else " hidden"}>'
                f'<a href="arten/{x["k"]}/index.html"><img src="photos/{x["k"]}-400.webp" alt="" width="400" height="300" loading="{"eager" if i < 5 else "lazy"}" decoding="async">'
                f'<span class="nc-ov"><b>{esc(x["n"])}</b><i>Hauptzeit</i></span></a>{cred(x["k"])}</li>')
    nowc = "".join(nowcard(x, i) for i, x in enumerate(ranked))
    sp = ranked[0]
    sp_first = sp["hl"].split(". ")[0].rstrip(".") + "."
    gcount = {g: sum(1 for x in SPECIES if x["grp"] == g) for g in GROUPS}
    gchips = "".join(f'<button type="button" class="hchip" data-hgrp="{g}">{g}<span>{gcount[g]}</span></button>' for g in GROUPS)
    events = "".join(f'<ul class="h5-events" data-m="{m}"{"" if m == NOWM_BUILD else " hidden"}>' + "".join(f"<li>{esc(e)}</li>" for e in MONTH_EVENTS[m]) + "</ul>" for m in range(1, 13))
    body = f'''<header class="hero5"> <div class="wrap hero5-in"> <div class="h5-text"> <h1>Wer war hier?</h1> <p class="lede">{len(SPECIES)} Tiere aus deutschen Wäldern, erkannt am Foto, an der Spur und an dem, was sie hinterlassen.</p> <form class="hsearch" id="hsearch" role="search" aria-label="Tier suchen"> <label for="hq"><span class="sr-only">Tier suchen</span>{ICON["find"]}<input type="search" id="hq" placeholder="Tier suchen, zum Beispiel Dachs" autocomplete="off" enterkeyhint="search"></label> <button class="hsearch-btn" type="submit">Suchen</button> </form> <div class="hchips" role="group" aria-label="Nach Tiergruppe zeigen">{gchips}</div> <div class="h5-month"><h2 class="h5-mh">Im Wald im <span data-now-name>November</span></h2>{events}</div> </div>
<figure class="spot" id="spot"> <a href="arten/{sp["k"]}/index.html" id="spot-link"><img id="spot-img" src="photos/{sp["k"]}.webp" srcset="photos/{sp["k"]}-400.webp 400w, photos/{sp["k"]}.webp 720w" sizes="(max-width: 900px) 92vw, 600px" alt="" width="720" height="540" fetchpriority="high"> <figcaption><span class="spot-tag">Hauptzeit im <span data-now-name>November</span></span><b id="spot-name">{esc(sp["n"])}</b><span id="spot-hl">{esc(sp_first)}</span></figcaption></a> <small class="spot-cred" id="spot-cred">{credit(sp["k"], True)}</small> </figure> </div> </header>
<section class="nowband" aria-labelledby="now-h"> <div class="wrap"> <div class="now-head"><h2 id="now-h">Jetzt im <span data-now-name>November</span> unterwegs</h2><div class="now-nav"><a href="waldjahr/index.html" data-now-link>Alle im <span data-now-name>November</span></a><button class="cbtn" type="button" id="now-prev" aria-controls="nowcards" aria-label="Vorherige Tiere" disabled><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m14.5 6-6 6 6 6"/></svg></button><button class="cbtn" type="button" id="now-next" aria-controls="nowcards" aria-label="Weitere Tiere"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9.5 6 6 6-6 6"/></svg></button></div></div> <ul class="nowcards" id="nowcards">{nowc}</ul> </div> </section>
<div class="bar" id="arten"> <div class="wrap barrow" role="search" aria-label="Arten suchen und filtern"> <label class="search" for="q">{ICON["find"]}<span class="sr-only">Art suchen</span> <input type="search" id="q" placeholder="Tier suchen, z. B. Marder" autocomplete="off" enterkeyhint="search"></label> <button class="chip ftoggle" id="f-toggle" type="button" aria-expanded="false" aria-controls="fpanel"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M7 12h10M10 18h4"></path></svg>Filter<b class="fcount" id="fcount" hidden></b></button> <label class="sortsel" for="sort"><span>Sortieren</span> <select id="sort"><option value="now">Jetzt aktiv zuerst</option><option value="az">Name A–Z</option><option value="size">Größe, klein zuerst</option></select></label> <span class="rcount" id="rcount" aria-live="polite">{len(SPECIES)} Arten</span> </div> <div class="fpanel" id="fpanel" hidden> <div class="wrap fgrid"> {filt} <div class="factions"><button class="btn ghost" id="f-reset" type="button">Alle Filter zurücksetzen</button><button class="btn" id="f-done" type="button">Ergebnisse anzeigen</button></div> </div> </div> <div class="wrap active" id="active" hidden></div> </div>
<section class="sub" aria-labelledby="arten-h"> <div class="wrap"> <h2 class="sr-only" id="arten-h">Arten</h2> <ul class="grid" id="grid"> {cards} </ul> <div class="empty" id="empty" hidden><p>Kein Tier passt zu deiner Suche oder Auswahl.</p><button class="btn ghost" type="button" id="empty-reset">Suche und Filter zurücksetzen</button></div> </div> </section>
<section class="gearband" aria-labelledby="h-gear"><div class="wrap"><div class="head-row"><h2 id="h-gear">Gut ausgerüstet in den Wald</h2><a class="gearmore" href="ausruestung/index.html">Alle Empfehlungen ansehen</a></div><ul class="products"> {"".join(product(R, g) for g in ("fernglas", "wildkamera", "waermebild", "lampe", "buch", "gips", "lupe", "igelhaus"))} </ul>{ADNOTE}</div></section>
<section class="block"> <div class="wrap"> <h2>Weiter entdecken</h2> <ul class="explore"> <li><a href="spuren/index.html"><b>Spuren lesen</b><span>Trittsiegel von Huftieren, Hunden, Katzen und Mardern, dazu Fraßspuren an Nüssen und Zapfen.</span></a></li> <li><a href="unterscheiden/index.html"><b>Doppelgänger unterscheiden</b><span>Reh oder Rothirsch, Baum- oder Steinmarder: {len(PAIRS)} Vergleiche mit den entscheidenden Merkmalen.</span></a></li> <li><a href="waldjahr/index.html"><b>Das Waldjahr</b><span>Brunft, Krötenwanderung, Winterschlaf: was im Wald wann passiert, Monat für Monat.</span></a></li> <li><a href="ausruestung/index.html"><b>Ausrüstung</b><span>Fernglas, Wildkamera, Rotlicht-Lampe und Spurenbuch für Beobachtungen in der Dämmerung.</span></a></li> <li><a href="https://vogelkompass.de/" rel="noopener"><b>Vögel im Wald?</b><span>Specht, Eichelhäher und Co. findest du auf der Schwesterseite Vogelkompass.</span></a></li> </ul> </div> </section>'''
    write("index.html", page("index.html", "Waldtierkompass – Waldtiere in Deutschland bestimmen",
        f"Waldtiere bestimmen leicht gemacht: {len(SPECIES)} Tiere aus deutschen Wäldern mit Trittsiegeln, Doppelgängern und Waldkalender.",
        body, active="index", scripts=("home.js",), is_home=True))

def build_arten_index():
    R = "../"
    sec = []
    for g in GROUPS:
        ss = sorted([s for s in SPECIES if s["grp"] == g], key=lambda x: x["n"])
        sec.append(f'<h2 class="h3 grp-h">{g}</h2><ul class="grid">{"".join(card(R, s, i) for i, s in enumerate(ss))}</ul>')
    body = f'<section class="block page"> <div class="wrap"> <h1>Alle Waldtiere</h1> <p class="intro">{len(SPECIES)} Arten, nach Gruppen geordnet. Zum Suchen und Filtern geht es zur <a href="../index.html#arten">Startseite</a>.</p> {"".join(sec)} </div> </section>'
    write("arten/index.html", page("arten/index.html", "Alle Waldtiere", "Alle Waldtiere im Überblick: Huftiere, Raubtiere, Kleinsäuger, Amphibien, Reptilien und Insekten.", body, crumbs=[("Arten", "")]))

def trackbox(s):
    if not art.is_track(s["art"]):
        return ""
    tr = next((v for a, v in s["facts"] if a == "Trittsiegel"), None)
    if not tr:
        return ""
    return f'<div class="trackbox"><span class="trk-img">{art.small_track(s["art"])}</span><p><b>Trittsiegel</b>{esc(tr[0].upper() + tr[1:])}</p></div>'

def build_species(s):
    R = "../../"
    k = s["k"]
    acts = ", ".join(ACTS[a] for a in s["act"])
    habs = "".join(f"<span>{esc(h)}</span>" for h in s["hab"])
    facts = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in s["facts"] + [("Aktiv", acts)])
    life = "".join(f'<details class="fold" open data-fold><summary><h3>{esc(a)}</h3></summary><p>{esc(b)}</p></details>' for a, b in s["life"])
    peaklinks = [f'<a href="{R}waldjahr/{MSLUG[m-1]}/index.html">{MONTHS[m-1]}</a>' for m in s["h"]]
    pl = peaklinks[0] if len(peaklinks) == 1 else ", ".join(peaklinks[:-1]) + " und " + peaklinks[-1]
    yeartext = (f'{"Das" if s["g"]=="n" else ("Die" if s["g"]=="f" else "Der")} {esc(s["n"])} ist {"das ganze Jahr über aktiv" if len(s["p"])==12 else "von " + mrange(s["p"]) + " aktiv"}. '
                f'Besonders gut zu beobachten im {pl}. {esc(s["hl"])}')
    alike = ""
    if s["alike"]:
        p = PAIRBY[s["alike"]]
        other = p["b"] if p["a"] == k else p["a"]
        okey = other if other in BY else "x-" + other
        alike = (f'<section class="alike" aria-labelledby="h-alike"> {img(R, okey, name_of(other))} <div> <h2 id="h-alike">Nicht verwechseln mit {ein(BY[other]["g"] if other in BY else EXT[other]["g"], "dat")} {esc(name_of(other))}</h2> '
                 f'<p>{esc(p["short"])}</p> <p><a href="{R}unterscheiden/{p["k"]}/index.html">{esc(name_of(p["a"]))} oder {esc(name_of(p["b"]))}? Alle Unterschiede</a></p> </div> </section>')
    wiki = "https://de.wikipedia.org/w/index.php?search=" + s["lat"].replace(" ", "+")
    gear = GEAR_FOR.get(k) or GEAR_GRP[s["grp"]]
    body = f'''<article class="sp wrap"> <div class="sp-top"> <figure class="sp-photo"> {img(R, k, s["n"], eager=True, sizes="(max-width: 760px) 92vw, 560px")} <figcaption>{credit(k)}</figcaption> </figure> <div class="sp-intro"> <h1>{esc(s["n"])}</h1> <p class="latin" lang="la">{esc(s["lat"])}</p> <p class="row"><span class="tag status">{esc(s["grp"])}</span><span class="tag">{esc(s["sz"])}</span>{"".join(f'<span class="tag act-tag">{act_svg(a)}{ACTS[a]}</span>' for a in s["act"])}</p> <p class="habs">{habs}</p> <p class="text">{esc(s["short"])} {esc(s["hl"])}</p> {trackbox(s)} </div> </div>
<div class="sp-cols"> <div class="sp-main"> <section aria-labelledby="h-marks"> <h2 id="h-marks">So erkennst du {"sie" if s["g"]=="f" else ("es" if s["g"]=="n" else "ihn")}</h2> <ul class="marks">{"".join(f"<li>{esc(m)}</li>" for m in s["marks"])}</ul> <dl class="facts">{facts}</dl> </section> <section aria-labelledby="h-year"> <h2 id="h-year">Wann im Jahr</h2> {months_bar(s)} <p class="sr-only">Aktiv: {mlist(s["p"])}. Hauptzeit: {mlist(s["h"])}.</p> <p class="yeartext">{yeartext}</p> </section> <section class="life" aria-labelledby="h-life"> <h2 id="h-life">Lebensweise</h2> {life} </section> <section class="helpbox" aria-label="Hilfe und Beobachtung"> <details class="fold" open data-fold><summary><h2>Rücksicht und Schutz</h2></summary><p>{esc(s["help"])}</p></details> <details class="fold" open data-fold><summary><h2>Beobachtungstipp</h2></summary><p>{esc(s["tip"])}</p></details> </section> {alike} <section class="more" aria-labelledby="h-more"> <h2 id="h-more">Mehr erfahren</h2> <ul class="morelinks"> <li><a href="{wiki}" target="_blank" rel="noopener">Wikipedia<span class="sr-only"> (öffnet in neuem Fenster)</span></a></li> </ul> </section> </div>
<aside class="sp-side" aria-label="Empfehlungen"> <section class="gearbox" aria-labelledby="h-gear"><h2 id="h-gear">Passend dazu</h2><ul class="products compact"> {"".join(product(R, g, True) for g in gear)} </ul>{ADNOTE}</section> </aside> </div> </article>'''
    write(f"arten/{k}/index.html", page(f"arten/{k}/index.html", f"{s['n']} erkennen", f"{s['n']} ({s['lat']}): {s['short']} Merkmale, Spuren, Lebensweise und wann du {'sie' if s['g']=='f' else ('es' if s['g']=='n' else 'ihn')} im Wald siehst.",
                                        body, crumbs=[("Arten", "arten/index.html"), (s["n"], "")], og=f"{k}.webp"))

def build_pairs():
    R = "../"
    body = f'<section class="block page"> <div class="wrap"> <h1>Doppelgänger unterscheiden</h1> <p class="intro">Viele Waldtiere sehen sich auf den ersten Blick ähnlich oder hinterlassen fast gleiche Spuren. Diese Merkmale helfen beim Unterscheiden.</p> <ul class="pairs">{"".join(pair_card(R, p) for p in PAIRS)}</ul> </div> </section>'
    write("unterscheiden/index.html", page("unterscheiden/index.html", "Doppelgänger unterscheiden", "Reh oder Rothirsch, Baummarder oder Steinmarder, Ringelnatter oder Kreuzotter: Waldtiere sicher unterscheiden.", body, active="unterscheiden", crumbs=[("Doppelgänger", "")]))
    for p in PAIRS:
        R = "../../"
        figs = ""
        for k in (p["a"], p["b"]):
            ik = k if k in BY else "x-" + k
            figs += f'<figure>{img(R, ik, name_of(k), eager=True)}<figcaption>{esc(name_of(k))} <i lang="la">{esc(lat_of(k))}</i><small>{credit(ik)}</small></figcaption></figure>'
        rows = "".join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td></tr>' for a, b, c in p["rows"])
        btns = " ".join(f'<a class="btn{"" if i==0 else " ghost"}" href="{R}arten/{k}/index.html">{esc(name_of(k))} im Porträt</a>' for i, k in enumerate([x for x in (p["a"], p["b"]) if x in BY]))
        others = [q for q in PAIRS if q["k"] != p["k"]]
        rnd = random.Random(p["k"]); rel = rnd.sample(others, 3)
        body = f'''<article class="wrap pairpage"> <h1>{esc(name_of(p["a"]))} oder {esc(name_of(p["b"]))}?</h1> <p class="intro">{esc(p["short"])}</p> <div class="ph big"> {figs} </div> <section aria-labelledby="h-cmp"> <h2 id="h-cmp">Die Unterschiede</h2> <div class="cmp-wrap"><table class="cmp"> <thead><tr><td></td><th scope="col">{esc(name_of(p["a"]))}</th><th scope="col">{esc(name_of(p["b"]))}</th></tr></thead> <tbody>{rows}</tbody> </table></div> <p class="merksatz"><b>Merkhilfe:</b> {esc(p["tip"])}</p> <p class="actions"> {btns} </p> </section> <section class="related" aria-labelledby="h-more"> <h2 id="h-more">Weitere Doppelgänger</h2> <ul class="pairs three">{"".join(pair_card(R, q, "h3") for q in rel)}</ul> </section> </article>'''
        write(f"unterscheiden/{p['k']}/index.html", page(f"unterscheiden/{p['k']}/index.html", f"{name_of(p['a'])} oder {name_of(p['b'])}?", p["short"], body, active="unterscheiden",
              crumbs=[("Doppelgänger", "unterscheiden/index.html"), (f"{name_of(p['a'])} oder {name_of(p['b'])}", "")]))

def cal_table(R):
    head = "".join(f'<th scope="col" data-month="{m}"><a href="{R}waldjahr/{MSLUG[m-1]}/index.html"><abbr title="{MONTHS[m-1]}">{MSHORT[m-1]}</abbr></a></th>' for m in range(1, 13))
    rows = []
    for g in GROUPS:
        rows.append(f'<tr class="grow"><th scope="rowgroup" colspan="13">{g}</th></tr>')
        for s in sorted([x for x in SPECIES if x["grp"] == g], key=lambda x: x["n"]):
            tds = ""
            for m in range(1, 13):
                c = "h" if m in s["h"] else ("p" if m in s["p"] else "")
                t = "Hauptzeit" if c == "h" else ("aktiv" if c == "p" else "kaum zu sehen")
                tds += f'<td data-month="{m}" class="m {c}" title="{esc(s["n"])}, {MONTHS[m-1]}: {t}"><span class="sr-only">{MONTHS[m-1]}: {t}</span></td>'
            rows.append(f'<tr><th scope="row" class="n"><a href="{R}arten/{s["k"]}/index.html">{esc(s["n"])}</a></th> {tds} </tr>')
    return f'<div class="cal-wrap"><table class="cal"> <caption class="sr-only">Aktivität aller Arten nach Monaten</caption> <thead><tr><th scope="col"><span class="sr-only">Art</span></th> {head}</tr></thead> <tbody> {"".join(rows)} </tbody> </table></div>'

def build_year():
    R = "../"
    links = ""
    for m in range(1, 13):
        n_p = sum(1 for s in SPECIES if m in s["p"]); n_h = sum(1 for s in SPECIES if m in s["h"])
        links += f'<li data-month="{m}"><a href="{R}waldjahr/{MSLUG[m-1]}/index.html"><b>{MONTHS[m-1]}</b><span>{n_p} aktiv, {n_h} in Hauptzeit</span></a></li>'
    events = "".join(f'<li data-month="{m}"><b>{MONTHS[m-1]}</b><span>{esc(MONTH_EVENTS[m][0])}</span></li>' for m in range(1, 13))
    body = f'''<section class="block page"> <div class="wrap"> <h1>Das Waldjahr</h1> <p class="intro">Was im Wald wann passiert: Brunft, Krötenwanderung, Winterschlaf. Wähle einen Monat, um zu sehen, wer dann unterwegs ist und was es zu entdecken gibt.</p> <ul class="monthlinks">{links}</ul> </div> </section>
<section class="block" aria-labelledby="h-ev"> <div class="wrap"> <h2 id="h-ev">Das Wichtigste im Jahreslauf</h2> <ul class="yearline">{events}</ul> </div> </section>
<section class="block" aria-labelledby="h-cal"> <div class="wrap"> <h2 id="h-cal">Wann siehst du wen?</h2> <p class="intro">Monate, in denen die Art aktiv ist, und wann sie besonders gut zu beobachten ist. Der aktuelle Monat ist farbig umrandet.</p> <p class="swipe">Seitlich wischen, um alle Monate zu sehen.</p> {cal_table(R)} </div> </section>'''
    write("waldjahr/index.html", page("waldjahr/index.html", "Das Waldjahr", "Waldkalender: welche Waldtiere wann aktiv sind, mit Brunft, Krötenwanderung und Winterschlaf Monat für Monat.", body, active="waldjahr", crumbs=[("Waldjahr", "")]))
    for m in range(1, 13):
        R = "../../"
        peak = sorted([s for s in SPECIES if m in s["h"]], key=lambda x: x["n"])
        act = sorted([s for s in SPECIES if m in s["p"] and m not in s["h"]], key=lambda x: x["n"])
        sleep = sorted([s for s in SPECIES if m not in s["p"]], key=lambda x: x["n"])
        ev = "".join(f"<li>{esc(e)}</li>" for e in MONTH_EVENTS[m])
        prev_m, next_m = (m - 2) % 12 + 1, m % 12 + 1
        sl = (f'<section class="block" aria-labelledby="h-sl"><div class="wrap"><h2 id="h-sl">In Winterruhe oder kaum zu sehen</h2><div class="pills">'
              + "".join(f'<a href="{R}arten/{s["k"]}/index.html">{esc(s["n"])}</a>' for s in sleep) + '</div></div></section>') if sleep else ""
        body = f'''<section class="block page"> <div class="wrap"> <h1>Der Wald im {MONTHS[m-1]}</h1> <p class="intro">{len(peak) + len(act)} der {len(SPECIES)} Arten sind im {MONTHS[m-1]} aktiv, {len(peak)} davon in ihrer Hauptzeit.</p> <ul class="evlist">{ev}</ul> <p class="actions"><a class="btn ghost" href="{R}waldjahr/{MSLUG[prev_m-1]}/index.html">← {MONTHS[prev_m-1]}</a> <a class="btn ghost" href="{R}waldjahr/{MSLUG[next_m-1]}/index.html">{MONTHS[next_m-1]} →</a></p> </div> </section>
<section class="block" aria-labelledby="h-pk"><div class="wrap"><h2 id="h-pk">Jetzt besonders gut zu beobachten</h2><ul class="grid">{"".join(card(R, s, i) for i, s in enumerate(peak))}</ul></div></section>
<section class="block" aria-labelledby="h-ac"><div class="wrap"><h2 id="h-ac">Außerdem unterwegs</h2><ul class="grid">{"".join(card(R, s, i) for i, s in enumerate(act))}</ul></div></section> {sl} {month_gear(R, m)}'''
        write(f"waldjahr/{MSLUG[m-1]}/index.html", page(f"waldjahr/{MSLUG[m-1]}/index.html", f"Waldtiere im {MONTHS[m-1]}", f"Welche Waldtiere im {MONTHS[m-1]} aktiv sind und was im Wald passiert: {MONTH_EVENTS[m][0]}", body, active="waldjahr",
              crumbs=[("Waldjahr", "waldjahr/index.html"), (MONTHS[m-1], "")]))

def month_gear(R, m):
    picks = ("igelhaus", "futterkasten", "fernglas", "waermebild") if m in (10, 11, 12, 1, 2) else (("lampe", "buch", "fledermauskasten", "wildkamera") if m in (3, 4, 5) else ("fledermauskasten", "detektor", "wildkamera", "lupe"))
    return (f'<section class="gearband" aria-labelledby="h-gear"><div class="wrap"><div class="head-row"><h2 id="h-gear">Passend zum {MONTHS[m-1]}</h2><a class="gearmore" href="{R}ausruestung/index.html">Alle Empfehlungen ansehen</a></div>'
            f'<ul class="products">{"".join(product(R, g) for g in picks)}</ul>{ADNOTE}</div></section>')

def build_tracks():
    R = "../"
    groups = [
     ("Paarhufer", "Hirsche und Wildschweine laufen auf zwei Zehenspitzen, den Schalen. Beim Wildschwein drücken sich dahinter fast immer die Afterklauen ab.", ["reh", "damhirsch", "rothirsch", "wildschwein"]),
     ("Hundeartige", "Vier Zehen, Krallen sichtbar, das Trittsiegel ist länger als breit. Fuchs und Wolf setzen die Pfoten wie an einer Schnur hintereinander.", ["rotfuchs", "wolf", "marderhund"]),
     ("Katzen", "Vier Zehen ohne Krallenabdruck, denn die Krallen sind eingezogen. Das Siegel wirkt rund.", ["wildkatze", "luchs"]),
     ("Marder und Dachs", "Fünf Zehen, oft springen Marder und hinterlassen Abdrücke in Zweiergruppen. Der Dachs zeigt lange Krallen.", ["dachs", "baummarder", "steinmarder", "hermelin"]),
     ("Hasen und Nager", "Sprungspuren: Die großen Hinterpfoten landen vor den kleinen Vorderpfoten.", ["feldhase", "wildkaninchen", "eichhoernchen", "roetelmaus"]),
     ("Weitere", "Hand-ähnliche Abdrücke und Grabspuren.", ["waschbaer", "igel", "maulwurf"]),
    ]
    secs = ""
    for title, intro, ks in groups:
        items = ""
        for k in ks:
            s = BY[k]
            tr = next(v for a, v in s["facts"] if a in ("Trittsiegel", "Spuren"))
            items += (f'<li class="trk"><a href="{R}arten/{k}/index.html"><span class="trk-img">{art.small_track(s["art"])}</span>'
                      f'<b>{esc(s["n"])}</b><span>{esc(tr[0].upper() + tr[1:])}</span></a></li>')
        secs += f'<section class="block" aria-label="{title}"><div class="wrap"><h2>{title}</h2><p class="intro">{intro}</p><ul class="trkgrid">{items}</ul></div></section>'
    body = f'''<section class="block page"> <div class="wrap"> <h1>Spuren lesen</h1> <p class="intro">Die meisten Waldtiere sind scheu und nachts unterwegs. Ihre Spuren verraten sie trotzdem: im Schnee, im Matsch am Wegrand oder als angenagte Nuss. Einen einzelnen Fußabdruck nennt man Trittsiegel, eine Reihe davon Fährte oder Spur.</p> <ol class="steps"><li><b>Zehen zählen</b> Zwei Schalen, vier oder fünf Zehen? Damit ist die Tiergruppe meist schon klar.</li><li><b>Krallen suchen</b> Hunde und Marder zeigen Krallen, Katzen nicht.</li><li><b>Größe messen</b> Ein Lineal oder ein Stift daneben hilft, Fuchs und Hund oder Reh und Hirsch zu trennen.</li><li><b>Muster ansehen</b> Gerade Linie, Paare oder Vierergruppen verraten die Gangart.</li></ol> </div> </section> {secs}
<section class="block" aria-labelledby="h-nut"><div class="wrap"><h2 id="h-nut">Wer hat die Haselnuss geknackt?</h2><p class="intro">Fraßspuren halten sich lange und sind oft leichter zu finden als Trittsiegel. Mit einer Lupe sind sie eindeutig.</p><div class="cmp-wrap"><table class="cmp"><thead><tr><td></td><th scope="col">So sieht die Nuss aus</th></tr></thead><tbody>
<tr><th scope="row"><a href="{R}arten/eichhoernchen/index.html">Eichhörnchen</a></th><td>Schale in zwei Hälften gesprengt oder mit grobem, gezacktem Rand</td></tr>
<tr><th scope="row"><a href="{R}arten/haselmaus/index.html">Haselmaus</a></th><td>rundes, glattes Loch, die Zahnspuren laufen parallel zum Lochrand</td></tr>
<tr><th scope="row">Waldmaus und Rötelmaus</th><td>rundes Loch, Zahnspuren quer zum Rand und oft auch auf der Schale daneben</td></tr>
<tr><th scope="row">Buntspecht</th><td>grob zerhackt, oft in eine Rindenspalte geklemmt</td></tr>
</tbody></table></div></div></section>
<section class="block" aria-labelledby="h-tip"><div class="wrap"><h2 id="h-tip">Tipps für die Spurensuche</h2><ul class="explore tips"><li><div><b>Nach Neuschnee</b><span>Am Morgen nach einer Schneenacht sind die Spuren frisch und scharf. Wenige Stunden später verlaufen sie schon.</span></div></li><li><div><b>Wegränder und Pfützen</b><span>Feuchter Lehm am Rand von Forstwegen und ausgetrocknete Pfützen halten Trittsiegel tagelang.</span></div></li><li><div><b>Fotografieren mit Maßstab</b><span>Lege ein Lineal oder einen Schlüssel neben das Siegel. Ohne Größenangabe ist eine Spur kaum zu bestimmen.</span></div></li><li><div><b>Hunde im Kopf behalten</b><span>Die meisten Pfotenabdrücke auf Spazierwegen stammen von Hunden. Ihre Spur läuft im Zickzack.</span></div></li></ul></div></section>'''
    body += f'<section class="gearband" aria-labelledby="h-gear"><div class="wrap"><div class="head-row"><h2 id="h-gear">Für die Spurensuche</h2><a class="gearmore" href="{R}ausruestung/index.html">Alle Empfehlungen ansehen</a></div><ul class="products">{"".join(product(R, g) for g in ("buch", "gips", "lupe", "wildkamera"))}</ul>{ADNOTE}</div></section>'
    write("spuren/index.html", page("spuren/index.html", "Tierspuren im Wald lesen", "Tierspuren bestimmen: Trittsiegel von Reh, Fuchs, Marder, Wildschwein und Co. mit Zeichnungen, dazu Fraßspuren an Haselnüssen.", body, active="spuren", crumbs=[("Spuren", "")]))

def build_gear():
    R = "../"
    gsec = lambda t, ks: f'<h2 class="h3 gear-h">{t}</h2><ul class="products">{"".join(product(R, k) for k in ks)}</ul>'
    body = f'''<section class="block page"> <div class="wrap"> <h1>Ausrüstung für Waldbeobachter</h1> <p class="intro">Für die meisten Begegnungen brauchst du nur Geduld, gute Ohren und Wind von vorn. Diese Dinge machen es leichter, vor allem in der Dämmerung.</p> {gsec("Beobachten", ("fernglas", "waermebild", "wildkamera", "lampe"))}{gsec("Spuren und Fraßspuren", ("buch", "gips", "lupe", "detektor"))}{gsec("Für Garten und Waldrand", ("igelhaus", "fledermauskasten", "futterkasten"))}{ADNOTE} </div> </section>
<section class="block"><div class="wrap prose"><h2>Worauf es beim Fernglas ankommt</h2><p>Für die Dämmerung ist ein 8x42 oder 10x42 ideal: Die zweite Zahl ist der Durchmesser der Objektive in Millimetern. Je größer, desto heller das Bild, wenn Reh und Fuchs am Waldrand auftauchen. Achte auf Wasserdichtigkeit und darauf, dass das Glas dir nach einer Stunde noch nicht zu schwer ist.</p><h2>Wildkameras rücksichtsvoll nutzen</h2><p>Stelle Kameras nur mit Erlaubnis des Eigentümers oder Jagdpächters auf und richte sie nicht auf Wege, auf denen Menschen unterwegs sind. Fotos von Personen dürfen ohne deren Einwilligung nicht entstehen.</p></div></section>'''
    write("ausruestung/index.html", page("ausruestung/index.html", "Ausrüstung", "Fernglas, Wildkamera, Rotlicht-Lampe und Spurenbuch: Ausrüstung für Waldbeobachtungen.", body, crumbs=[("Ausrüstung", "")]))

def build_legal():
    R = "../"
    imp = f'''<section class="block page"> <div class="wrap prose"> <h1>Impressum</h1> <h2>Angaben gemäß § 5 DDG und § 18 Abs. 1 MStV</h2> <p>Nico Schober<br>Herzogin-Cecilie-Allee 10<br>28217 Bremen<br>Deutschland</p> <h2>Kontakt</h2> <p>E-Mail: <a href="mailto:info@nicoschober.com">info@nicoschober.com</a></p> <h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2> <p>Nico Schober, Anschrift wie oben.</p> <h2>Art des Angebots</h2> <p>Der Waldtierkompass ist ein privates Informationsangebot. Er verkauft selbst keine Waren oder Dienstleistungen. Einige Seiten enthalten gekennzeichnete Werbelinks zum Amazon-Partnerprogramm; kaufst du über einen solchen Link ein, erhält der Betreiber eine Provision. Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p> <h2>Haftung für Inhalte</h2> <p>Die Inhalte wurden mit Sorgfalt erstellt. Für Richtigkeit, Vollständigkeit und Aktualität kann jedoch keine Gewähr übernommen werden. Angaben zu Aktivitätszeiten und Verbreitung sind grobe Richtwerte und können regional abweichen. Die Seite ersetzt keine fachliche Beratung, etwa bei Schlangenbissen oder verletzten Wildtieren.</p> <h2>Haftung für Links</h2> <p>Diese Seite enthält Links zu externen Websites, auf deren Inhalte kein Einfluss besteht. Für diese Inhalte ist der jeweilige Anbieter verantwortlich. Zum Zeitpunkt der Verlinkung waren keine Rechtsverstöße erkennbar. Werden Rechtsverletzungen bekannt, wird der betreffende Link umgehend entfernt.</p> <h2>Urheberrecht</h2> <p>Texte, Zeichnungen und Gestaltung dieser Seite stammen vom Betreiber. Die Fotos stammen von Dritten und stehen unter freien Lizenzen; Urheber und Lizenzen sind aufgeführt unter <a href="../bildnachweis/index.html">Bildnachweis und Lizenzen</a>.</p> </div> </section>'''
    write("impressum/index.html", page("impressum/index.html", "Impressum", "Impressum des Waldtierkompass.", imp, crumbs=[("Impressum", "")]))
    ds = f'''<section class="block page"> <div class="wrap prose"> <h1>Datenschutzerklärung</h1> <p class="stand">Stand: November 2026</p> <h2>1. Verantwortlicher</h2> <p>Verantwortlich für die Datenverarbeitung auf dieser Website ist der im <a href="../impressum/index.html">Impressum</a> genannte Betreiber.</p> <h2>2. Das Wichtigste in Kürze</h2> <ul> <li>Es gibt keine Registrierung, keine Cookies, kein Tracking und keine Reichweitenmessung. Werbung gibt es nur in Form gekennzeichneter Links zu Amazon, die erst beim Anklicken eine Verbindung aufbauen.</li> <li>Die Seite speichert nichts in deinem Browser.</li> <li>Schriftarten, Fotos und Zeichnungen werden vom selben Server geladen wie die Seite selbst. Es findet keine Verbindung zu Google Fonts oder anderen Drittanbietern statt.</li> </ul> <h2>3. Hosting und Server-Protokolle</h2> <p>Diese Website wird bei statichost.eu gehostet, einem Dienst von Variable Object Assignment, c/o Knackeriet, Svartmangatan 9, 111 29 Stockholm, Schweden. Die Server stehen nach Angaben des Anbieters in der Europäischen Union; eine Übermittlung in Drittländer findet nicht statt.</p> <p>Beim Aufruf der Seite verarbeitet der Anbieter deine IP-Adresse sowie technisch notwendige Angaben zur Anfrage (abgerufene Datei, Zeitpunkt, Browser), um dir die Seite ausliefern zu können. Nach Angaben des Anbieters wird die IP-Adresse dabei nur für die Dauer der Anfrage im Arbeitsspeicher verarbeitet und nicht protokolliert. Für die Abrechnung werden technische Protokolle ohne personenbezogene Daten (vor allem die übertragene Datenmenge) höchstens sieben Tage aufbewahrt. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO; das berechtigte Interesse liegt in der zuverlässigen und sicheren Bereitstellung der Website. statichost.eu ist Auftragsverarbeiter im Sinne von Art. 28 DSGVO; der Anbieter stellt dafür einen eigenen Vertrag zur Auftragsverarbeitung bereit. Weitere Informationen: <a href="https://www.statichost.eu/privacy/" rel="noopener">Datenschutzerklärung von statichost.eu</a>.</p> <h2>4. Werbelinks zum Amazon-Partnerprogramm</h2> <p>Einige Seiten enthalten mit einem Sternchen gekennzeichnete Links zu Produkten bei Amazon.de. Der Betreiber nimmt am Partnerprogramm von Amazon Europe Core S.à r.l. teil und erhält eine Provision, wenn du über einen solchen Link einkaufst. Auf dieser Website werden dafür keine Skripte, Bilder oder Cookies von Amazon geladen. Erst wenn du einen Werbelink anklickst, wirst du zu Amazon weitergeleitet; Amazon kann dann Cookies setzen, um die Herkunft der Bestellung zuzuordnen. Einzelheiten findest du in der <a href="https://www.amazon.de/gp/help/customer/display.html?nodeId=201909010" target="_blank" rel="noopener">Datenschutzerklärung von Amazon<span class="sr-only"> (öffnet in neuem Fenster)</span></a>.</p> <h2>5. Externe Links</h2> <p>Die Seite verlinkt auf externe Angebote wie Wikipedia oder den Vogelkompass. Erst wenn du einen solchen Link anklickst, wird eine Verbindung zum jeweiligen Anbieter aufgebaut.</p> <h2>6. Kontakt per E-Mail</h2> <p>Wenn du mir eine E-Mail schreibst, verarbeite ich deine Adresse und den Inhalt der Nachricht, um dir zu antworten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Die Nachricht wird gelöscht, sobald dein Anliegen erledigt ist und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p> <h2>7. Deine Rechte</h2> <p>Du hast das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch (Art. 21). Wende dich dafür an die im Impressum genannte Adresse. Außerdem kannst du dich bei einer Datenschutz-Aufsichtsbehörde beschweren (Art. 77 DSGVO). Für den Betreiber zuständig ist die Landesbeauftragte für Datenschutz und Informationsfreiheit der Freien Hansestadt Bremen.</p> </div> </section>'''
    write("datenschutz/index.html", page("datenschutz/index.html", "Datenschutz", "Datenschutzerklärung des Waldtierkompass.", ds, crumbs=[("Datenschutz", "")]))
    rows = ""
    for k in sorted(CREDITS, key=lambda x: name_of(x[2:] if x.startswith("x-") else x)):
        a_, lic, url = CREDITS[k]
        n = name_of(k[2:] if k.startswith("x-") else k)
        rows += f'<tr><th scope="row">{esc(n)}</th><td>{esc(a_)}</td><td>{lic_link(lic)}</td><td><a href="{esc(url)}" target="_blank" rel="noopener">Quelle<span class="sr-only"> (öffnet in neuem Fenster)</span></a></td></tr>'
    prows = "".join(f'<tr><th scope="row">{esc(PRODUCTS[k]["name"])}</th><td>{esc(a_)}</td><td>{lic_link(lic)}</td><td><a href="{esc(url)}" target="_blank" rel="noopener">Quelle<span class="sr-only"> (öffnet in neuem Fenster)</span></a></td></tr>' for k, (a_, lic, url) in PHOTO.items())
    bn = f'''<section class="block page"> <div class="wrap prose"> <h1>Bildnachweis und Lizenzen</h1> <h2>Fotos</h2> <p>Alle Fotos stammen von Wikimedia Commons und stehen unter den genannten freien Lizenzen. Für die Seite wurden sie verkleinert und zugeschnitten. Die Lizenz ist jeweils mit ihrem Lizenztext verlinkt, die Quelle mit der Originaldatei. Bearbeitete Fotos unter einer Share-alike-Lizenz (BY-SA) stehen unter derselben Lizenz wie das Original.</p> </div> <div class="wrap"><div class="cmp-wrap"><table class="cmp"><thead><tr><td>Art</td><th scope="col">Urheber</th><th scope="col">Lizenz</th><th scope="col">Quelle</th></tr></thead><tbody>{rows}</tbody></table></div></div> <div class="wrap prose"> <h2>Fotos zu den Produktempfehlungen</h2> <p>Die Fotos sind als Beispielfoto gekennzeichnet. Sie zeigen typische Geräte und Beispiele, nicht das verlinkte Produkt. Sichtbare Markenlogos wurden unkenntlich gemacht.</p> </div> <div class="wrap"><div class="cmp-wrap"><table class="cmp"><thead><tr><td>Empfehlung</td><th scope="col">Urheber</th><th scope="col">Lizenz</th><th scope="col">Quelle</th></tr></thead><tbody>{prows}</tbody></table></div></div> <div class="wrap prose"> <h2>Zeichnungen</h2> <p>Die Trittsiegel sind eigene Zeichnungen für den Waldtierkompass. Sie zeigen typische Formen und sind nicht maßstabsgetreu.</p> <h2>Schriften</h2> <p>Fraunces (Undercase Type) und Figtree (Erik Kennedy), beide unter der SIL Open Font License 1.1, lokal eingebunden über das Projekt Fontsource.</p> </div> </section>'''
    write("bildnachweis/index.html", page("bildnachweis/index.html", "Bildnachweis und Lizenzen", "Bildnachweis und Lizenzen des Waldtierkompass.", bn, crumbs=[("Bildnachweis", "")]))

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(HERE, "node_modules", ".bin")
SAFELIST = ["now", "open", "calm", "scrolled", "clear", "fcount", "pk"]

def build_assets():
    from PIL import Image
    write("favicon.svg", FAVICON)
    shutil.copytree(os.path.join(HERE, "fonts"), os.path.join(OUT, "fonts"), dirs_exist_ok=True)
    os.makedirs(os.path.join(OUT, "photos"), exist_ok=True)
    for f in os.listdir(os.path.join(HERE, "photos")):
        if f.endswith(".webp"):
            shutil.copy(os.path.join(HERE, "photos", f), os.path.join(OUT, "photos", f))
    # Vorschaubild für soziale Netzwerke (1.91:1)
    im = Image.open(os.path.join(HERE, "photos_src", "wk-reh.jpg")).convert("RGB")
    w, h = im.size; th = round(w / 1.91); y = (h - th) // 2
    im.crop((0, y, w, y + th)).save(os.path.join(OUT, "photos", "og.jpg"), quality=80, optimize=True, progressive=True)

def finalize():
    """CSS entschlacken und minifizieren, JS bündeln, Sitemap schreiben."""
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    css_src = os.path.join(OUT, "assets", "_full.css")
    with open(css_src, "w", encoding="utf-8") as f:
        f.write(open(os.path.join(HERE, "src", "css", "base.css"), encoding="utf-8").read() + open(os.path.join(HERE, "src", "css", "extra.css"), encoding="utf-8").read())
    purged = os.path.join(OUT, "assets", "_purged.css")
    subprocess.run([os.path.join(TOOLS, "purgecss"), "--css", css_src, "--content", f"{OUT}/**/*.html", f"{HERE}/src/js/*.js",
                    "--safelist", *SAFELIST, "--output", purged], check=True)
    subprocess.run([os.path.join(TOOLS, "lightningcss"), "--minify", "--targets", ">= 0.5%", purged, "-o", os.path.join(OUT, "assets", "site.css")], check=True)
    os.remove(css_src); os.remove(purged)
    for f in os.listdir(os.path.join(OUT, "assets")):
        if f.endswith(".js"):
            os.remove(os.path.join(OUT, "assets", f))
    entries = [os.path.join(HERE, "src", "js", f) for f in ("app.js", "home.js")]
    subprocess.run([os.path.join(TOOLS, "esbuild"), *entries, "--bundle", "--format=esm", "--minify", "--target=es2020",
                    "--legal-comments=none", f"--outdir={os.path.join(OUT, 'assets')}", "--log-level=warning"], check=True)
    urls = []
    for d, _, fs in os.walk(OUT):
        for f in fs:
            if f == "index.html":
                rel = os.path.relpath(os.path.join(d, f), OUT).replace(os.sep, "/")
                urls.append(DOMAIN + "/" + rel[:-len("index.html")])
    urls.sort(key=lambda u: (u.count("/"), u))
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    # Zeitpunkt des Builds, um zu prüfen, ob die Live-Seite aktuell ist
    import datetime as _dt
    write("version.txt", _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + "\n")

if __name__ == "__main__":
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    build_assets(); build_home(); build_arten_index()
    for s in SPECIES:
        build_species(s)
    build_pairs(); build_year(); build_tracks(); build_gear(); build_legal()
    finalize()
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print("Dateien:", n)
