# -*- coding: utf-8 -*-
"""Doppelgänger: Übersicht (/unterscheiden/) und je Paar eine Vergleichsseite."""
import random

from data import PAIRS, PAIR_DEEP
from ..config import MONTHS
from ..helpers import BY, esc, write, name_of, lat_of, photo_key, art_of, pair_title
from ..components import pair_card
from ..layout import page
from ..media import img, credit, new_tab


def build_index():
    R = "../"
    body = (f'<section class="block page"> <div class="wrap"> <h1>Doppelgänger unterscheiden</h1> <p class="intro">Viele Waldtiere sehen sich auf den ersten Blick ähnlich '
            f'oder hinterlassen fast gleiche Spuren. Diese Merkmale helfen beim Unterscheiden.</p> <ul class="pairs">{"".join(pair_card(R, p) for p in PAIRS)}</ul> </div> </section>')
    write("unterscheiden/index.html", page("unterscheiden/index.html", "Doppelgänger unterscheiden",
                                           "Reh oder Rothirsch, Baummarder oder Steinmarder, Ringelnatter oder Kreuzotter: Waldtiere sicher unterscheiden.",
                                           body, active="unterscheiden", crumbs=[("Doppelgänger", "")]))


def related(p):
    """Drei weitere Vergleiche, bevorzugt aus derselben Tiergruppe; feste Zufallsfolge je Paar, damit der Build gleich bleibt."""
    others = [q for q in PAIRS if q["k"] != p["k"]]
    rnd = random.Random(p["k"])
    g0 = art_of(p["a"])[1]
    same = [q for q in others if art_of(q["a"])[1] == g0]
    rest = [q for q in others if q not in same]
    rnd.shuffle(same)
    rnd.shuffle(rest)
    return (same + rest)[:3]


def deep_sections(d):
    """Vertiefte Inhalte (Fließtext, häufige Fragen, Quellen) und FAQPage-Strukturdaten."""
    if not d:
        return "", None
    out = "".join(f'<section class="deep" aria-labelledby="h-t{i}"> <h2 id="h-t{i}">{esc(h)}</h2> <p>{esc(t)}</p> </section> ' for i, (h, t) in enumerate(d["text"]))
    out += ('<section class="faq" aria-labelledby="h-faq"> <h2 id="h-faq">Häufige Fragen</h2> '
            + "".join(f'<div class="qa"> <h3>{esc(q)}</h3> <p>{esc(a)}</p> </div> ' for q, a in d["faq"]) + '</section> ')
    y, mo, _ = d["updated"].split("-")
    out += ('<section class="more" aria-labelledby="h-src"> <h2 id="h-src">Quellen</h2> <ul class="morelinks"> '
            + "".join(f'<li>{new_tab(esc(u), esc(n))}</li> ' for n, u in d["sources"])
            + f'</ul> <p class="stand">Stand: <time datetime="{d["updated"]}">{MONTHS[int(mo)-1]} {y}</time></p> </section> ')
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
          {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]}
    return out, ld


def build(p):
    R = "../../"
    a, b = p["a"], p["b"]
    na, nb = esc(name_of(a)), esc(name_of(b))
    figs = "".join(f'<figure>{img(R, photo_key(k), name_of(k), eager=True, high=(k == a), sizes="(max-width: 760px) 92vw, 560px")}'
                   f'<figcaption>{esc(name_of(k))} <i lang="la">{esc(lat_of(k))}</i><small>{credit(photo_key(k))}</small></figcaption></figure>' for k in (a, b))
    rows = "".join(f'<tr><th scope="row">{esc(x)}</th><td data-label="{na}">{esc(y)}</td><td data-label="{nb}">{esc(z)}</td></tr>' for x, y, z in p["rows"])
    btns = " ".join(f'<a class="btn{"" if i == 0 else " ghost"}" href="{R}arten/{k}/index.html">{esc(name_of(k))} im Porträt</a>'
                    for i, k in enumerate([x for x in (a, b) if x in BY]))
    d = PAIR_DEEP.get(p["k"])
    deep, ld = deep_sections(d)
    body = (f'<article class="wrap pairpage"> <h1>{na} oder {nb}?</h1> <p class="intro">{esc(p["short"])}</p> <div class="ph big"> {figs} </div> '
            f'<section aria-labelledby="h-cmp"> <h2 id="h-cmp">Die Unterschiede</h2> <div class="cmp-wrap"><table class="cmp cmp-pair"> '
            f'<thead><tr><td></td><th scope="col">{na}</th><th scope="col">{nb}</th></tr></thead> <tbody>{rows}</tbody> </table></div> '
            f'<p class="merksatz"><b>Merkhilfe:</b> {esc(p["tip"])}</p> <p class="actions"> {btns} </p> </section> '
            f'{deep}<section class="related" aria-labelledby="h-more"> <h2 id="h-more">Weitere Doppelgänger</h2> '
            f'<ul class="pairs three">{"".join(pair_card(R, q, "h3") for q in related(p))}</ul> </section> </article>')
    title = f"{pair_title(p)}?"
    write(f"unterscheiden/{p['k']}/index.html", page(f"unterscheiden/{p['k']}/index.html", d["title"] if d else title, d["desc"] if d else p["short"], body,
                                                     active="unterscheiden", ld=ld, crumbs=[("Doppelgänger", "unterscheiden/index.html"), (pair_title(p), "")]))


def build_all():
    build_index()
    for p in PAIRS:
        build(p)
