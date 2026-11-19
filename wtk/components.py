# -*- coding: utf-8 -*-
"""Wiederkehrende Bausteine: Artkarte, Jahresband, Vergleichskarte, Filterknöpfe, Trittsiegel-Kasten."""
import art
from data import ACTS
from .config import MONTHS, MSHORT
from .helpers import esc, month_state, month_list, name_of, photo_key, fact, ucfirst, pair_title
from .icons import act_svg
from .media import img, cred, credit

# Zusätzliche Suchwörter je Gruppe und Art (Startseiten-Filter und Schnellsuche)
GRP_SYN = {"Huftiere": "Huftier Paarhufer Hirsch Wild", "Raubtiere": "Raubtier Räuber Beutegreifer", "Kleinsäuger": "Säugetier Nager Maus",
           "Amphibien": "Amphibie Lurch Frosch Kröte Molch", "Reptilien": "Reptil Echse Eidechse Schlange", "Insekten": "Insekt Käfer Krabbeltier"}
SYN = {"rotfuchs": "Fuchs", "wolf": "Isegrim Rudel", "wildschwein": "Sau Schwein Keiler Bache Frischling Schwarzwild", "reh": "Bock Ricke Kitz Rehwild",
       "rothirsch": "Hirsch Rotwild", "damhirsch": "Hirsch Damwild", "braunes-langohr": "Fledermaus Flattertier", "eichhoernchen": "Eichhorn Hörnchen",
       "siebenschlaefer": "Bilch Schläfer", "haselmaus": "Bilch Maus", "roetelmaus": "Maus Wühlmaus", "igel": "Stacheln", "maulwurf": "Erdhügel Maulwurfshügel",
       "feldhase": "Hase Meister Lampe", "wildkaninchen": "Kaninchen Karnickel", "wildkatze": "Katze", "luchs": "Katze Pinselohren", "hermelin": "Wiesel",
       "waschbaer": "Bär", "marderhund": "Hund Enok", "kreuzotter": "Schlange Otter Viper giftig", "ringelnatter": "Schlange Natter", "blindschleiche": "Schlange",
       "waldeidechse": "Bergeidechse", "erdkroete": "Kröte", "grasfrosch": "Frosch", "feuersalamander": "Salamander Molch", "bergmolch": "Molch",
       "hirschkaefer": "Käfer", "rote-waldameise": "Ameise Ameisenhaufen", "dachs": "Grimbart", "baummarder": "Marder Edelmarder", "steinmarder": "Marder Hausmarder Automarder"}


def acts_text(s):
    return [ACTS[a] for a in s["act"]]


def actlegend():
    return (f'<p class="actlegend" aria-hidden="true"><span>{act_svg("tag")} tagaktiv</span><span>{act_svg("daemmerung")} dämmerungsaktiv</span>'
            f'<span>{act_svg("nacht")} nachtaktiv</span></p>')


def card(R, s, i=0, hidden=False, eager=False):
    """Artkarte im Raster; die data-Attribute nutzt home.js zum Suchen, Filtern und Sortieren."""
    acts = "".join(f'<span class="act" title="{ACTS[a]}">{act_svg(a)}<span class="sr-only">{ACTS[a]}</span></span>' for a in s["act"])
    search = " ".join([s["n"], s["lat"], s["grp"], GRP_SYN[s["grp"]], SYN.get(s["k"], ""), s["short"]] + acts_text(s))
    return (f'<li class="bird" id="{s["k"]}" style="--i:{i}" data-key="{s["k"]}" data-name="{esc(s["n"])}" data-search="{esc(search)}" '
            f'data-grp="{esc(s["grp"])}" data-act="{"|".join(s["act"])}" data-hab="{esc("|".join(s["hab"]))}" data-size="{s["size"]}" data-mid="{s["mid"]}" '
            f'data-present="{month_list(s["p"])}" data-peak="{month_list(s["h"])}"{" hidden" if hidden else ""}> '
            f'{img(R, s["k"], "", eager=eager)}{cred(s["k"], R)} <div class="txt"> <h3><a class="open" href="{R}arten/{s["k"]}/index.html">{esc(s["n"])}</a></h3> '
            f'<span class="meta"><span class="latin" lang="la">{esc(s["lat"])}</span><span class="size">{esc(s["sz"])}</span></span> '
            f'<span class="row"><span class="tag status">{esc(s["grp"])}</span></span> <p class="short">{esc(s["short"])}</p> </div> '
            f'<span class="acts">{acts}</span> </li>')


def months_bar(s):
    """Jahresband wie bei Vogel-, Meeres- und Gartentierkompass: schlanke Balken, Monatsnamen darunter, „jetzt“ per app.js."""
    out = []
    for m in range(1, 13):
        cls, t = month_state(s, m)
        c = f' class="{cls}"' if cls else ""
        out.append(f'<span data-month="{m}"{c} title="{MONTHS[m-1]}: {t}"><i class="ml">{MSHORT[m-1]}</i><i class="ms">{MSHORT[m-1][0]}</i></span>')
    return (f'<div class="months" aria-hidden="true">{"".join(out)}</div>'
            '<p class="mlegend" aria-hidden="true"><span class="lh">Hauptzeit</span><span class="lp">aktiv</span><span class="ln">jetzt</span></p>')


def pair_card(R, p, h="h2"):
    figs = "".join(f'<figure>{img(R, photo_key(k), sizes="(max-width: 600px) 46vw, 240px")}<figcaption>{esc(name_of(k))}<small>{credit(photo_key(k), True)}</small></figcaption></figure>'
                   for k in (p["a"], p["b"]))
    return (f'<li class="pair"> <div class="ph"> {figs} </div> <div class="pb"> <{h}><a class="pair-link" href="{R}unterscheiden/{p["k"]}/index.html">'
            f'{esc(pair_title(p))}?</a></{h}> <p>{esc(p["short"])}</p> <span class="to" aria-hidden="true">Alle Unterschiede</span> </div> </li>')


def chipset(legend, g, items):
    """Gruppe von Filterknöpfen; g = Filtername in home.js, items = [(Wert, Beschriftung)]."""
    return f'<fieldset><legend>{legend}</legend><div class="fchips">' + "".join(
        f'<button class="chip" type="button" data-g="{g}" data-v="{esc(v)}" aria-pressed="false">{esc(t)}</button>' for v, t in items) + '</div></fieldset>'


def track_text(s):
    """Beschreibung des Trittsiegels, wenn es eine Zeichnung dazu gibt."""
    tr = fact(s, "Trittsiegel")
    return ucfirst(tr) if tr and art.is_track(s["art"]) else None


def trackbox(s):
    tr = track_text(s)
    if not tr:
        return ""
    return f'<div class="trackbox"><span class="trk-img">{art.small_track(s["art"])}</span><p><b>Trittsiegel</b>{esc(tr)}</p></div>'
