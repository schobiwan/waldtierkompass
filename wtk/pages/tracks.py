# -*- coding: utf-8 -*-
"""Spuren lesen (/spuren/): Trittsiegel nach Gruppen, maßstäblich gezeichnet, dazu Fraßspuren."""
import art
from ..helpers import BY, esc, write, slug, fact, ucfirst
from ..layout import page
from ..products import gearband

# ungefähre Länge eines Trittsiegels in cm, für die maßstäbliche Darstellung
TRACK_CM = {"reh": 4.5, "damhirsch": 6, "rothirsch": 8.5, "wildschwein": 6.5, "rotfuchs": 5, "wolf": 10, "marderhund": 4.5,
            "wildkatze": 4, "luchs": 8, "dachs": 6, "baummarder": 4, "steinmarder": 4, "hermelin": 2, "feldhase": 6,
            "wildkaninchen": 4, "eichhoernchen": 4.5, "roetelmaus": 1.5, "waschbaer": 6.5, "igel": 2.5, "maulwurf": 3}

GROUPS = [
 ("Paarhufer", "Hirsche und Wildschweine laufen auf zwei Zehenspitzen, den Schalen. Beim Wildschwein drücken sich dahinter fast immer die Afterklauen ab.", ["reh", "damhirsch", "rothirsch", "wildschwein"]),
 ("Hundeartige", "Vier Zehen, Krallen sichtbar, das Trittsiegel ist länger als breit. Fuchs und Wolf setzen die Pfoten wie an einer Schnur hintereinander.", ["rotfuchs", "wolf", "marderhund"]),
 ("Katzen", "Vier Zehen ohne Krallenabdruck, denn die Krallen sind eingezogen. Das Siegel wirkt rund.", ["wildkatze", "luchs"]),
 ("Marder und Dachs", "Fünf Zehen, oft springen Marder und hinterlassen Abdrücke in Zweiergruppen. Der Dachs zeigt lange Krallen.", ["dachs", "baummarder", "steinmarder", "hermelin"]),
 ("Hasen und Nager", "Sprungspuren: Die großen Hinterpfoten landen vor den kleinen Vorderpfoten.", ["feldhase", "wildkaninchen", "eichhoernchen", "roetelmaus"]),
 ("Weitere", "Hand-ähnliche Abdrücke und Grabspuren.", ["waschbaer", "igel", "maulwurf"]),
]

INTRO = ('<p class="intro">Die meisten Waldtiere sind scheu und nachts unterwegs. Ihre Spuren verraten sie trotzdem: im Schnee, im Matsch am Wegrand oder als angenagte Nuss. '
         'Einen einzelnen Fußabdruck nennt man Trittsiegel, eine Reihe davon Fährte oder Spur.</p> '
         '<ol class="steps"><li><b>Zehen zählen</b> Zwei Schalen, vier oder fünf Zehen? Damit ist die Tiergruppe meist schon klar.</li>'
         '<li><b>Krallen suchen</b> Hunde und Marder zeigen Krallen, Katzen nicht.</li>'
         '<li><b>Größe messen</b> Ein Lineal oder ein Stift daneben hilft, Fuchs und Hund oder Reh und Hirsch zu trennen.</li>'
         '<li><b>Muster ansehen</b> Gerade Linie, Paare oder Vierergruppen verraten die Gangart.</li></ol>')

TIPS = [
    ("Nach Neuschnee", "Am Morgen nach einer Schneenacht sind die Spuren frisch und scharf. Wenige Stunden später verlaufen sie schon."),
    ("Wegränder und Pfützen", "Feuchter Lehm am Rand von Forstwegen und ausgetrocknete Pfützen halten Trittsiegel tagelang."),
    ("Fotografieren mit Maßstab", "Lege ein Lineal oder einen Schlüssel neben das Siegel. Ohne Größenangabe ist eine Spur kaum zu bestimmen."),
    ("Hunde im Kopf behalten", "Die meisten Pfotenabdrücke auf Spazierwegen stammen von Hunden. Ihre Spur läuft im Zickzack."),
]


def track_scale(k):
    return max(0.3, min(1.0, TRACK_CM.get(k, 6) / 10))


def track_item(R, k):
    s = BY[k]
    tr = ucfirst(fact(s, "Trittsiegel", "Spuren"))
    return (f'<li class="trk"><a href="{R}arten/{k}/index.html"><span class="trk-img" style="--s:{track_scale(k):.2f}">{art.small_track(s["art"])}</span>'
            f'<span class="trk-t"><b>{esc(s["n"])}</b><span>{esc(tr)}</span></span></a></li>')


def nut_table(R):
    return ('<section class="block" aria-labelledby="h-nut"><div class="wrap"><h2 id="h-nut">Wer hat die Haselnuss geknackt?</h2><p class="intro">Fraßspuren halten sich lange '
            'und sind oft leichter zu finden als Trittsiegel. Mit einer Lupe sind sie eindeutig.</p><div class="cmp-wrap"><table class="cmp"><thead><tr><td></td>'
            '<th scope="col">So sieht die Nuss aus</th></tr></thead><tbody>\n'
            f'<tr><th scope="row"><a href="{R}arten/eichhoernchen/index.html">Eichhörnchen</a></th><td>Schale in zwei Hälften gesprengt oder mit grobem, gezacktem Rand</td></tr>\n'
            f'<tr><th scope="row"><a href="{R}arten/haselmaus/index.html">Haselmaus</a></th><td>rundes, glattes Loch, die Zahnspuren laufen parallel zum Lochrand</td></tr>\n'
            '<tr><th scope="row">Waldmaus und Rötelmaus</th><td>rundes Loch, Zahnspuren quer zum Rand und oft auch auf der Schale daneben</td></tr>\n'
            '<tr><th scope="row">Buntspecht</th><td>grob zerhackt, oft in eine Rindenspalte geklemmt</td></tr>\n'
            '</tbody></table></div></div></section>')


def build():
    R = "../"
    secs = ""
    for title, intro, ks in GROUPS:
        sid = slug(title)
        secs += (f'<section class="block" aria-labelledby="h-{sid}" id="g-{sid}"><div class="wrap"><h2 id="h-{sid}">{title}</h2><p class="intro">{intro}</p>'
                 f'<ul class="trkgrid">{"".join(track_item(R, k) for k in ks)}</ul></div></section>')
    jump = "".join(f'<li><a href="#g-{slug(t)}">{t}</a></li>' for t, _, _ in GROUPS)
    tips = "".join(f'<li><div><b>{t}</b><span>{d}</span></div></li>' for t, d in TIPS)
    body = (f'<section class="block page"> <div class="wrap"> <h1>Tierspuren lesen und bestimmen</h1> {INTRO} '
            f'<nav class="jump" aria-label="Zu den Gruppen springen"><ul class="pills">{jump}<li><a href="#h-nut">Fraßspuren</a></li></ul></nav> '
            '<p class="intro small">Die Zeichnungen sind im Verhältnis zueinander skaliert: Ein großes Siegel ist auch in Wirklichkeit größer.</p> </div> </section> '
            f'{secs}\n{nut_table(R)}\n'
            f'<section class="block" aria-labelledby="h-tip"><div class="wrap"><h2 id="h-tip">Tipps für die Spurensuche</h2><ul class="explore tips">{tips}</ul></div></section>')
    body += gearband(R, "Für die Spurensuche", ("buch", "gips", "lupe", "wildkamera"))
    write("spuren/index.html", page("spuren/index.html", "Tierspuren bestimmen: Trittsiegel im Wald lesen",
                                    "Tierspuren bestimmen: Trittsiegel von Reh, Fuchs, Marder, Wildschwein und Co. mit Zeichnungen, dazu Fraßspuren an Haselnüssen.",
                                    body, active="spuren", crumbs=[("Spuren", "")]))
