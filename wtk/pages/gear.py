# -*- coding: utf-8 -*-
"""Ausrüstung (/ausruestung/): alle Empfehlungen nach Einsatzzweck."""
from ..helpers import write
from ..layout import page
from ..products import product, ADNOTE

SECTIONS = [
    ("Beobachten", ("fernglas", "waermebild", "wildkamera", "lampe")),
    ("Spuren und Fraßspuren", ("buch", "gips", "lupe", "detektor")),
    ("Für Garten und Waldrand", ("igelhaus", "fledermauskasten", "futterkasten")),
]

ADVICE = ('<section class="block"><div class="wrap prose"><h2>Worauf es beim Fernglas ankommt</h2><p>Für die Dämmerung ist ein 8x42 oder 10x42 ideal: Die zweite Zahl ist der '
          'Durchmesser der Objektive in Millimetern. Je größer, desto heller das Bild, wenn Reh und Fuchs am Waldrand auftauchen. Achte auf Wasserdichtigkeit und darauf, '
          'dass das Glas dir nach einer Stunde noch nicht zu schwer ist.</p><h2>Wildkameras rücksichtsvoll nutzen</h2><p>Stelle Kameras nur mit Erlaubnis des Eigentümers '
          'oder Jagdpächters auf und richte sie nicht auf Wege, auf denen Menschen unterwegs sind. Fotos von Personen dürfen ohne deren Einwilligung nicht entstehen.</p></div></section>')


def build():
    R = "../"
    secs = "".join(f'<h2 class="h3 gear-h">{t}</h2><ul class="products">{"".join(product(R, k, sizes="(max-width: 600px) 92vw, 360px") for k in ks)}</ul>'
                   for t, ks in SECTIONS)
    body = (f'<section class="block page"> <div class="wrap"> <h1>Ausrüstung für Waldbeobachter</h1> <p class="intro">Für die meisten Begegnungen brauchst du nur Geduld, '
            f'gute Ohren und Wind von vorn. Diese Dinge machen es leichter, vor allem in der Dämmerung.</p> {secs}{ADNOTE} </div> </section>\n{ADVICE}')
    write("ausruestung/index.html", page("ausruestung/index.html", "Ausrüstung für die Tierbeobachtung im Wald",
                                         "Fernglas, Wildkamera, Rotlicht-Lampe und Spurenbuch: Ausrüstung für Waldbeobachtungen.",
                                         body, active="ausruestung", crumbs=[("Ausrüstung", "")]))
