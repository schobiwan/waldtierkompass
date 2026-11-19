# -*- coding: utf-8 -*-
"""Waldjahr: Übersicht mit Kalender (/waldjahr/) und je Monat eine Seite."""
from data import SPECIES, GROUPS, MONTH_EVENTS
from ..config import MONTHS, MSHORT, MSLUG
from ..helpers import esc, write, by_name, in_group, month_state
from ..components import card
from ..layout import page
from ..products import gearband, gear_for_month


def month_href(R, m):
    return f"{R}waldjahr/{MSLUG[m-1]}/index.html"


def cal_table(R):
    head = "".join(f'<th scope="col" data-month="{m}"><a href="{month_href(R, m)}"><abbr title="{MONTHS[m-1]}">{MSHORT[m-1]}</abbr></a></th>' for m in range(1, 13))
    rows = []
    for g in GROUPS:
        rows.append(f'<tr class="grow"><th scope="rowgroup" colspan="13"><span>{g}</span></th></tr>')
        for s in in_group(g):
            tds = ""
            for m in range(1, 13):
                c, t = month_state(s, m)
                tds += f'<td data-month="{m}" class="m {c}" title="{esc(s["n"])}, {MONTHS[m-1]}: {t}"><span class="sr-only">{MONTHS[m-1]}: {t}</span></td>'
            rows.append(f'<tr><th scope="row" class="n"><a href="{R}arten/{s["k"]}/index.html">{esc(s["n"])}</a></th> {tds} </tr>')
    return (f'<div class="cal-wrap" tabindex="0" role="region" aria-label="Kalender: wann welche Art aktiv ist"><table class="cal"> '
            f'<caption class="sr-only">Aktivität aller Arten nach Monaten</caption> <thead><tr><th scope="col"><span class="sr-only">Art</span></th> {head}</tr></thead> '
            f'<tbody> {"".join(rows)} </tbody> </table></div>')


def build_index():
    R = "../"
    links = ""
    for m in range(1, 13):
        n_p = sum(1 for s in SPECIES if m in s["p"])
        n_h = sum(1 for s in SPECIES if m in s["h"])
        links += f'<li data-month="{m}"><a href="{month_href(R, m)}"><b>{MONTHS[m-1]}</b><span>{n_p} aktiv, {n_h} in Hauptzeit</span></a></li>'
    events = "".join(f'<li data-month="{m}"><b>{MONTHS[m-1]}</b><span>{esc(MONTH_EVENTS[m][0])}</span></li>' for m in range(1, 13))
    body = (f'<section class="block page"> <div class="wrap"> <h1>Das Waldjahr</h1> <p class="intro">Was im Wald wann passiert: Brunft, Krötenwanderung, Winterschlaf. '
            f'Wähle einen Monat, um zu sehen, wer dann unterwegs ist und was es zu entdecken gibt.</p> <ul class="monthlinks">{links}</ul> </div> </section>\n'
            f'<section class="block" aria-labelledby="h-ev"> <div class="wrap"> <h2 id="h-ev">Das Wichtigste im Jahreslauf</h2> <ul class="yearline">{events}</ul> </div> </section>\n'
            f'<section class="block" aria-labelledby="h-cal"> <div class="wrap"> <h2 id="h-cal">Wann siehst du wen?</h2> <p class="intro">Monate, in denen die Art aktiv ist, '
            f'und wann sie besonders gut zu beobachten ist.</p> <p class="mlegend callegend" aria-hidden="true"><span class="lh">Hauptzeit</span><span class="lp">aktiv</span>'
            f'<span class="ln">aktueller Monat</span></p> <p class="swipe">Seitlich wischen, um alle Monate zu sehen.</p> {cal_table(R)} </div> </section>')
    write("waldjahr/index.html", page("waldjahr/index.html", "Das Waldjahr",
                                      "Waldkalender: welche Waldtiere wann aktiv sind, mit Brunft, Krötenwanderung und Winterschlaf Monat für Monat.",
                                      body, active="waldjahr", crumbs=[("Waldjahr", "")]))


def build(m):
    R = "../../"
    name = MONTHS[m - 1]
    peak = by_name(s for s in SPECIES if m in s["h"])
    act = by_name(s for s in SPECIES if m in s["p"] and m not in s["h"])
    sleep = by_name(s for s in SPECIES if m not in s["p"])
    ev = "".join(f"<li>{esc(e)}</li>" for e in MONTH_EVENTS[m])
    prev_m, next_m = (m - 2) % 12 + 1, m % 12 + 1
    sl = ('<section class="block" aria-labelledby="h-sl"><div class="wrap"><h2 id="h-sl">In Winterruhe oder kaum zu sehen</h2><div class="pills">'
          + "".join(f'<a href="{R}arten/{s["k"]}/index.html">{esc(s["n"])}</a>' for s in sleep) + '</div></div></section>') if sleep else ""
    body = (f'<section class="block page"> <div class="wrap"> <h1>Der Wald im {name}</h1> <p class="intro">{len(peak) + len(act)} der {len(SPECIES)} Arten sind im {name} aktiv, '
            f'{len(peak)} davon in ihrer Hauptzeit.</p> <ul class="evlist">{ev}</ul> <p class="actions"><a class="btn ghost" href="{month_href(R, prev_m)}">← {MONTHS[prev_m-1]}</a> '
            f'<a class="btn ghost" href="{month_href(R, next_m)}">{MONTHS[next_m-1]} →</a></p> </div> </section>\n'
            f'<section class="block" aria-labelledby="h-pk"><div class="wrap"><h2 id="h-pk">Jetzt besonders gut zu beobachten</h2><ul class="grid">{"".join(card(R, s, i, eager=i < 2) for i, s in enumerate(peak))}</ul></div></section>\n'
            f'<section class="block" aria-labelledby="h-ac"><div class="wrap"><h2 id="h-ac">Außerdem unterwegs</h2><ul class="grid">{"".join(card(R, s, i) for i, s in enumerate(act))}</ul></div></section> '
            f'{sl} {gearband(R, f"Passend zum {name}", gear_for_month(m))}')
    path = f"waldjahr/{MSLUG[m-1]}/index.html"
    write(path, page(path, f"Waldtiere im {name}", f"Welche Waldtiere im {name} aktiv sind und was im Wald passiert: {MONTH_EVENTS[m][0]}", body,
                     active="waldjahr", crumbs=[("Waldjahr", "waldjahr/index.html"), (name, "")]))


def build_all():
    build_index()
    for m in range(1, 13):
        build(m)
