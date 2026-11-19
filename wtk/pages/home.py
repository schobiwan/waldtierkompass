# -*- coding: utf-8 -*-
"""Startseite: Kopfbereich mit Tier des Monats, Karussell „Jetzt unterwegs“, Suche und Filter, Empfehlungen."""
from data import SPECIES, PAIRS, GROUPS, HABS, ACTS, SIZES, MONTH_EVENTS
from ..config import NOWM, MONTHS, SISTER_URL
from ..helpers import esc, write, by_name, count_group, first_sentence, month_list
from ..components import card, chipset, actlegend
from ..icons import ICON
from ..layout import page
from ..media import cred
from ..products import gearband

NOW_NAME = '<span data-now-name>{}</span>'  # home.js/app.js setzen den Monat im Browser neu

EXPLORE = [
    ("spuren/index.html", "Spuren lesen", "Trittsiegel von Huftieren, Hunden, Katzen und Mardern, dazu Fraßspuren an Nüssen und Zapfen."),
    ("unterscheiden/index.html", "Doppelgänger unterscheiden", f"Reh oder Rothirsch, Baum- oder Steinmarder: {len(PAIRS)} Vergleiche mit den entscheidenden Merkmalen."),
    ("waldjahr/index.html", "Das Waldjahr", "Brunft, Krötenwanderung, Winterschlaf: was im Wald wann passiert, Monat für Monat."),
    ("ausruestung/index.html", "Ausrüstung", "Fernglas, Wildkamera, Rotlicht-Lampe und Spurenbuch für Beobachtungen in der Dämmerung."),
]
EXPLORE_SISTERS = [
    ("Vogelkompass", "Vögel im Wald?", "Specht, Eichelhäher und Co. findest du auf der Schwesterseite Vogelkompass."),
    ("Meereskompass", "Robbe, Wal und Qualle?", "Seehunde, Schweinswale und Strandfunde an Nord- und Ostsee findest du auf der Schwesterseite Meereskompass."),
    ("Gartentierkompass", "Käfer, Schnecke, Schmetterling?", "Igel, Marienkäfer, Schnecken und andere Gartentiere findest du auf der Schwesterseite Gartentierkompass."),
]
GEAR = ("fernglas", "wildkamera", "waermebild", "lampe", "buch", "gips", "lupe", "igelhaus")


def ranked_now():
    """Arten in Hauptzeit zuerst, dann nach Name; die erste ist das Tier des Monats."""
    return sorted(SPECIES, key=lambda x: (0 if NOWM in x["h"] else 1, x["n"]))


def now_card(x, i, spot):
    hidden = "" if (NOWM in x["p"] and x is not spot) else " hidden"
    return (f'<li data-peak="{month_list(x["h"])}" data-present="{month_list(x["p"])}" data-k="{x["k"]}" data-name="{esc(x["n"])}" '
            f'data-hl="{esc(first_sentence(x["hl"]))}"{hidden}>'
            f'<a href="arten/{x["k"]}/index.html"><img src="photos/{x["k"]}-400.webp" alt="" width="400" height="300" loading="{"eager" if 0 < i < 4 else "lazy"}" decoding="async">'
            f'<span class="nc-ov"><b>{esc(x["n"])}</b><i>Hauptzeit</i></span></a>{cred(x["k"])}</li>')


def filters(now_name):
    return (chipset("Gruppe", "grp", [(g, g) for g in GROUPS]) +
            chipset("Aktiv", "act", list(ACTS.items())) +
            chipset("Lebensraum", "hab", [(h, h) for h in HABS]) +
            chipset("Größe", "size", list(SIZES.items())) +
            '<fieldset><legend>Außerdem</legend><div class="fchips"><button class="chip" type="button" data-g="flag" data-v="now" aria-pressed="false">'
            f'Jetzt im {now_name} aktiv</button></div></fieldset>')


def hero(now_name, spot):
    gchips = "".join(f'<button type="button" class="hchip" data-hgrp="{g}">{g}<span>{count_group(g)}</span></button>' for g in GROUPS)
    events = "".join(f'<ul class="h5-events" data-m="{m}"{"" if m == NOWM else " hidden"}>' + "".join(f"<li>{esc(e)}</li>" for e in MONTH_EVENTS[m]) + "</ul>"
                     for m in range(1, 13))
    k = spot["k"]
    return (f'<header class="hero5"> <div class="wrap hero5-in"> <div class="h5-text"> <h1><span class="h1-kick">Waldtiere bestimmen</span> Wer war hier?</h1> '
            f'<p class="lede">{len(SPECIES)} Tiere aus deutschen Wäldern, erkannt am Foto, an der Spur und an dem, was sie hinterlassen.</p> '
            f'<form class="hsearch" id="hsearch" role="search" aria-label="Tier suchen"> <label for="hq"><span class="sr-only">Tier suchen</span>{ICON["find"]}'
            '<input type="search" id="hq" placeholder="Tier suchen, zum Beispiel Dachs" autocomplete="off" enterkeyhint="search"></label> '
            '<button class="hsearch-btn" type="submit">Suchen</button> </form> '
            f'<div class="hchips" role="group" aria-label="Nach Tiergruppe zeigen">{gchips}</div> '
            f'<div class="h5-month"><h2 class="h5-mh">Im Wald im {now_name}</h2>{events}</div> </div>\n'
            f'<figure class="spot" id="spot"> <a href="arten/{k}/index.html" id="spot-link"><img id="spot-img" src="photos/{k}.webp" '
            f'srcset="photos/{k}-400.webp 400w, photos/{k}.webp 720w" sizes="(max-width: 900px) 92vw, 600px" alt="" width="720" height="540" fetchpriority="high"> '
            f'<figcaption><span class="spot-tag">Hauptzeit im {now_name}</span><b id="spot-name">{esc(spot["n"])}</b><span id="spot-hl">{esc(first_sentence(spot["hl"]))}</span></figcaption></a> '
            f'{cred(k, cls="spot-cred", id_="spot-cred")} </figure> </div> </header>')


def now_band(now_name, ranked, spot):
    arrow = lambda d: f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{d}"/></svg>'
    cards = "".join(now_card(x, i, spot) for i, x in enumerate(ranked))
    return (f'<section class="nowband" aria-labelledby="now-h"> <div class="wrap"> <div class="now-head"><h2 id="now-h">Jetzt im {now_name} unterwegs</h2>'
            f'<div class="now-nav"><a href="waldjahr/index.html" data-now-link>Alle im {now_name}</a>'
            f'<button class="cbtn" type="button" id="now-prev" aria-controls="nowcards" aria-label="Vorherige Tiere" disabled>{arrow("m14.5 6-6 6 6 6")}</button>'
            f'<button class="cbtn" type="button" id="now-next" aria-controls="nowcards" aria-label="Weitere Tiere">{arrow("m9.5 6 6 6-6 6")}</button></div></div> '
            f'<ul class="nowcards" id="nowcards">{cards}</ul> </div> </section>')


def search_bar(now_name):
    return (f'<div class="bar" id="arten"> <div class="wrap barrow" role="search" aria-label="Arten suchen und filtern"> <label class="search" for="q">{ICON["find"]}'
            '<span class="sr-only">Art suchen</span> <input type="search" id="q" placeholder="Tier suchen, z. B. Marder" autocomplete="off" enterkeyhint="search"></label> '
            '<button class="chip ftoggle" id="f-toggle" type="button" aria-expanded="false" aria-controls="fpanel"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M7 12h10M10 18h4"></path></svg>'
            'Filter<b class="fcount" id="fcount" hidden></b></button> <label class="sortsel" for="sort"><span>Sortieren</span> <select id="sort">'
            '<option value="now">Jetzt aktiv zuerst</option><option value="az">Name A–Z</option><option value="size">Größe, klein zuerst</option></select></label> '
            f'<span class="rcount" id="rcount" aria-live="polite">{len(SPECIES)} Arten</span> </div> <div class="fpanel" id="fpanel" hidden> <div class="wrap fgrid"> '
            f'{filters(now_name)} <div class="factions"><button class="btn ghost" id="f-reset" type="button">Alle Filter zurücksetzen</button>'
            '<button class="btn" id="f-done" type="button">Ergebnisse anzeigen</button></div> </div> </div> <div class="wrap active" id="active" hidden></div> </div>')


def species_grid():
    cards = "".join(card("", s, i) for i, s in enumerate(by_name(SPECIES)))
    groups = "".join(f'<button type="button" class="chip" data-sgrp="{g}">{g}</button>' for g in GROUPS)
    return ('<section class="sub" aria-labelledby="arten-h"> <div class="wrap"> <h2 class="sr-only" id="arten-h">Arten</h2> '
            f'{actlegend()} <ul class="grid" id="grid"> {cards} </ul> <div class="empty" id="empty" hidden><p id="empty-msg">Kein Tier passt zu deiner Suche oder Auswahl.</p>'
            f'<p id="empty-suggest" hidden></p><div class="empty-groups" aria-label="Stattdessen eine Tiergruppe ansehen">{groups}</div>'
            '<button class="btn ghost" type="button" id="empty-reset">Suche und Filter zurücksetzen</button></div> </div> </section>')


def explore():
    own = " ".join(f'<li><a href="{h}"><b>{t}</b><span>{d}</span></a></li>' for h, t, d in EXPLORE)
    sis = "".join(f'<li><a href="{SISTER_URL[n]}" rel="noopener"><b>{t}</b><span>{d}</span></a></li>' for n, t, d in EXPLORE_SISTERS)
    return f'<section class="block"> <div class="wrap"> <h2>Weiter entdecken</h2> <ul class="explore"> {own} {sis} </ul> </div> </section>'


def build():
    now_name = NOW_NAME.format(MONTHS[NOWM - 1])
    ranked = ranked_now()
    spot = ranked[0]
    body = "\n".join([hero(now_name, spot), now_band(now_name, ranked, spot), search_bar(now_name), species_grid(),
                      gearband("", "Gut ausgerüstet in den Wald", GEAR), explore()])
    write("index.html", page("index.html", "Waldtierkompass – Waldtiere in Deutschland bestimmen",
                             f"Waldtiere bestimmen leicht gemacht: {len(SPECIES)} Tiere aus deutschen Wäldern mit Trittsiegeln, Doppelgängern und Waldkalender.",
                             body, active="index", script="home.js", is_home=True))
