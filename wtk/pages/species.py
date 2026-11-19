# -*- coding: utf-8 -*-
"""Artseiten (/arten/<art>/) und die Übersicht aller Arten (/arten/)."""
from data import SPECIES, GROUPS, ACTS
from ..config import SITE, DOMAIN, CONTENT_ISO, MONTHS, MSLUG
from ..helpers import (CREDITS, PAIRBY, esc, write, slug, in_group, name_of, gender_of, photo_key, other_of, pair_title,
                       ein, mit_art, pronoun, join_and, mlist, mrange)
from ..components import card, actlegend, months_bar, trackbox, track_text
from ..icons import act_svg
from ..layout import page
from ..media import img, credit, lic_url, new_tab
from ..products import product, gear_for, ADNOTE


def build_index():
    R = "../"
    sec, n = [], 0
    for g in GROUPS:
        ss = in_group(g)
        sec.append(f'<h2 class="h3 grp-h" id="g-{slug(g)}">{g}</h2><ul class="grid">{"".join(card(R, s, i, eager=n + i < 4) for i, s in enumerate(ss))}</ul>')
        n += len(ss)
    body = (f'<section class="block page"> <div class="wrap"> <h1>Alle Waldtiere</h1> {actlegend()} <p class="intro">{len(SPECIES)} Arten, nach Gruppen geordnet. '
            f'Zum Suchen und Filtern geht es zur <a href="../index.html#arten">Startseite</a>.</p> {"".join(sec)} </div> </section>')
    write("arten/index.html", page("arten/index.html", "Alle Waldtiere", "Alle Waldtiere im Überblick: Huftiere, Raubtiere, Kleinsäuger, Amphibien, Reptilien und Insekten.",
                                   body, active="index", crumbs=[("Arten", "")]))


def species_desc(s):
    """Meta-Beschreibung, höchstens 160 Zeichen."""
    for d in (f"{s['n']} ({s['lat']}): {s['short']} Merkmale, Spuren und wann du {pronoun(s['g'])} siehst.",
              f"{s['n']} ({s['lat']}): {s['short']} Merkmale und Spuren.",
              f"{s['n']}: {s['short']} Merkmale und Spuren."):
        if len(d) <= 160:
            return d
    return d[:157].rsplit(" ", 1)[0] + " …"


def species_title(s):
    """Seitentitel nach dem, was Leute suchen (wie beim Vogelkompass); mit Zusatz höchstens 65 Zeichen."""
    n = s["n"]
    opts = ([f"{n}: Spuren, Merkmale und Lebensweise", f"{n}: Spuren und Merkmale"] if track_text(s) else []) + \
           [f"{n} erkennen: Merkmale und Lebensweise", f"{n}: Merkmale und Lebensweise", f"{n} erkennen"]
    return next(t for t in opts if len(t) + len(f" · {SITE}") <= 65)


def tldr(s):
    """„Kurz gesagt“: Kurzantwort oben auf der Artseite (für Eilige und KI-Übersichten)."""
    rows = [("Erkennen", s["short"]), ("Lebensraum", ", ".join(s["hab"])),
            ("Aktiv", f'{", ".join(ACTS[a] for a in s["act"])}, {mrange(s["p"])}'),
            ("Am besten zu sehen", mlist(s["h"]))]
    tr = track_text(s)
    if tr:
        rows.append(("Spur", tr))
    if s["alike"]:
        rows.append(("Verwechslung", name_of(other_of(PAIRBY[s["alike"]], s["k"]))))
    return ('<section class="tldr" aria-labelledby="h-tldr"><h2 id="h-tldr">Kurz gesagt</h2><dl>'
            + "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in rows) + '</dl></section>')


def species_ld(s):
    """WebPage mit Art (Taxon) und Hauptfoto samt Fotograf und Lizenz, wie beim Vogelkompass."""
    k = s["k"]
    a, lic, url = CREDITS[k]
    return {"@context": "https://schema.org", "@type": "WebPage", "name": f"{s['n']} ({s['lat']})", "description": species_desc(s),
            "inLanguage": "de-DE", "url": f"{DOMAIN}/arten/{k}/", "dateModified": CONTENT_ISO,
            "author": {"@type": "Person", "name": "Nico Schober", "url": f"{DOMAIN}/ueber/"},
            "about": {"@type": "Taxon", "name": s["lat"], "alternateName": s["n"], "taxonRank": "species"},
            "image": f"{DOMAIN}/photos/{k}.webp",
            "primaryImageOfPage": {"@type": "ImageObject", "contentUrl": f"{DOMAIN}/photos/{k}.webp", "creator": {"@type": "Person", "name": a},
                                   "license": lic_url(lic) or url, "acquireLicensePage": url, "creditText": f"{a}, Wikimedia Commons",
                                   "copyrightNotice": f"© {a}, {lic}"}}


def year_text(s, R):
    article = {"n": "Das", "f": "Die"}.get(s["g"], "Der")
    active = "das ganze Jahr über aktiv" if len(s["p"]) == 12 else "von " + mrange(s["p"]) + " aktiv"
    peaks = join_and(f'<a href="{R}waldjahr/{MSLUG[m-1]}/index.html">{MONTHS[m-1]}</a>' for m in s["h"])
    return f'{article} {esc(s["n"])} ist {active}. Besonders gut zu beobachten im {peaks}. {esc(s["hl"])}'


def alike_box(s, R):
    """Hinweis auf den Doppelgänger mit Foto und Link zum Vergleich."""
    if not s["alike"]:
        return ""
    p = PAIRBY[s["alike"]]
    other = other_of(p, s["k"])
    return (f'<section class="alike" aria-labelledby="h-alike"> {img(R, photo_key(other), name_of(other), sizes="(max-width: 900px) 96px, 140px")} <div> '
            f'<h2 id="h-alike">Nicht verwechseln mit {ein(gender_of(other), "dat")} {esc(name_of(other))}</h2> '
            f'<p>{esc(p["short"])}</p> <p><a href="{R}unterscheiden/{p["k"]}/index.html">{esc(pair_title(p))}? Alle Unterschiede</a></p> </div> </section>')


def build(s):
    R = "../../"
    k = s["k"]
    acts = ", ".join(ACTS[a] for a in s["act"])
    habs = "".join(f"<span>{esc(h)}</span>" for h in s["hab"])
    act_tags = "".join(f'<span class="tag act-tag">{act_svg(a)}{ACTS[a]}</span>' for a in s["act"])
    facts = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in s["facts"] + [("Aktiv", acts)])
    marks = "".join(f"<li>{esc(m)}</li>" for m in s["marks"])
    life = "".join(f'<details class="fold" open data-fold><summary><h3>{esc(a)}</h3></summary><p>{esc(b)}</p></details>' for a, b in s["life"])
    wiki = "https://de.wikipedia.org/w/index.php?search=" + s["lat"].replace(" ", "+")
    gear = "".join(product(R, g, True) for g in gear_for(s))
    top = (f'<div class="sp-top"> <figure class="sp-photo"> {img(R, k, s["n"], eager=True, sizes="(max-width: 760px) 92vw, 560px")} <figcaption>{credit(k)}</figcaption> </figure> '
           f'<div class="sp-intro"> <h1>{esc(s["n"])}</h1> <p class="latin" lang="la">{esc(s["lat"])}</p> '
           f'<p class="row"><span class="tag status">{esc(s["grp"])}</span><span class="tag">{esc(s["sz"])}</span>{act_tags}</p> '
           f'<p class="habs">{habs}</p> <p class="text">{esc(s["short"])} {esc(s["hl"])}</p> {trackbox(s)} </div> </div>')
    main = (f'<div class="sp-main"> {tldr(s)} '
            f'<section aria-labelledby="h-marks"> <h2 id="h-marks">So erkennst du {esc(mit_art(s, "akk"))}</h2> <ul class="marks">{marks}</ul> <dl class="facts">{facts}</dl> </section> '
            f'<section aria-labelledby="h-year"> <h2 id="h-year">Wann ist {esc(mit_art(s))} zu sehen?</h2> {months_bar(s)} '
            f'<p class="sr-only">Aktiv: {mlist(s["p"])}. Hauptzeit: {mlist(s["h"])}.</p> <p class="yeartext">{year_text(s, R)}</p> </section> '
            f'<section class="life" aria-labelledby="h-life"> <h2 id="h-life">Lebensweise</h2> {life} </section> '
            f'<section class="helpbox" aria-label="Hilfe und Beobachtung"> '
            f'<details class="fold" open><summary><h2>So hilfst du {esc(mit_art(s, "dat"))}</h2></summary><p>{esc(s["help"])}</p></details> '
            f'<details class="fold" open><summary><h2>Wo und wie du {pronoun(s["g"])} beobachtest</h2></summary><p>{esc(s["tip"])}</p></details> </section> '
            f'{alike_box(s, R)} <section class="more" aria-labelledby="h-more"> <h2 id="h-more">Mehr erfahren</h2> <ul class="morelinks"> <li>{new_tab(wiki, "Wikipedia")}</li> </ul> </section> </div>')
    side = (f'<aside class="sp-side" aria-label="Empfehlungen"> <section class="gearbox" aria-labelledby="h-gear"><h2 id="h-gear">Passend dazu</h2>'
            f'<ul class="products compact"> {gear} </ul>{ADNOTE}<p class="gearall"><a href="{R}ausruestung/index.html">Alle Ausrüstungstipps ansehen</a></p></section> </aside>')
    body = f'<article class="sp wrap"> {top}\n<div class="sp-cols"> {main}\n{side} </div> </article>'
    write(f"arten/{k}/index.html", page(f"arten/{k}/index.html", species_title(s), species_desc(s), body, active="index",
                                        crumbs=[("Arten", "arten/index.html"), (s["n"], "")], og=f"og-{k}.jpg", og_alt=s["n"], og_type="article", ld=species_ld(s)))


def build_all():
    build_index()
    for s in SPECIES:
        build(s)
