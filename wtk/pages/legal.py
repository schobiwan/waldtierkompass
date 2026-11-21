# -*- coding: utf-8 -*-
"""Impressum, Datenschutz, Bildnachweis und „Über den Waldtierkompass“."""
from data import SPECIES, PAIRS
from ..config import SITE, DOMAIN, SISTER_URL, AUTHOR
from ..helpers import CREDITS, write, name_of, key_of_photo
from ..layout import page
from ..media import credit_row
from ..products import PRODUCTS, PHOTO

IMPRESSUM = '''<section class="block page"> <div class="wrap prose"> <h1>Impressum</h1> <h2>Angaben gemäß § 5 DDG und § 18 Abs. 1 MStV</h2> <p>Nico Schober<br>Herzogin-Cecilie-Allee 10<br>28217 Bremen<br>Deutschland</p> <h2>Kontakt</h2> <p>E-Mail: <a href="mailto:info@nicoschober.com">info@nicoschober.com</a><br>Website: <a href="https://nicoschober.com/" target="_blank" rel="noopener">nicoschober.com<span class="sr-only"> (öffnet in neuem Fenster)</span></a></p> <h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2> <p>Nico Schober, Anschrift wie oben.</p> <h2>Art des Angebots</h2> <p>Der Waldtierkompass ist ein privates Informationsangebot. Er verkauft selbst keine Waren oder Dienstleistungen. Einige Seiten enthalten gekennzeichnete Werbelinks zum Amazon-Partnerprogramm; kaufst du über einen solchen Link ein, erhält der Betreiber eine Provision. Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p> <h2>Haftung für Inhalte</h2> <p>Die Inhalte wurden mit Sorgfalt erstellt. Für Richtigkeit, Vollständigkeit und Aktualität kann jedoch keine Gewähr übernommen werden. Angaben zu Aktivitätszeiten und Verbreitung sind grobe Richtwerte und können regional abweichen. Die Seite ersetzt keine fachliche Beratung, etwa bei Schlangenbissen oder verletzten Wildtieren.</p> <h2>Haftung für Links</h2> <p>Diese Seite enthält Links zu externen Websites, auf deren Inhalte kein Einfluss besteht. Für diese Inhalte ist der jeweilige Anbieter verantwortlich. Zum Zeitpunkt der Verlinkung waren keine Rechtsverstöße erkennbar. Werden Rechtsverletzungen bekannt, wird der betreffende Link umgehend entfernt.</p> <h2>Urheberrecht</h2> <p>Texte, Zeichnungen und Gestaltung dieser Seite stammen vom Betreiber. Die Fotos stammen von Dritten und stehen unter freien Lizenzen; Urheber und Lizenzen sind aufgeführt unter <a href="../bildnachweis/index.html">Bildnachweis und Lizenzen</a>.</p> </div> </section>'''

DATENSCHUTZ = '''<section class="block page"> <div class="wrap prose"> <h1>Datenschutzerklärung</h1> <p class="stand">Stand: November 2026</p> <h2>1. Verantwortlicher</h2> <p>Verantwortlich für die Datenverarbeitung auf dieser Website ist der im <a href="../impressum/index.html">Impressum</a> genannte Betreiber.</p> <h2>2. Das Wichtigste in Kürze</h2> <ul> <li>Es gibt keine Registrierung, keine Cookies, kein Tracking und keine Reichweitenmessung. Werbung gibt es nur in Form gekennzeichneter Links zu Amazon, die erst beim Anklicken eine Verbindung aufbauen.</li> <li>Die Seite speichert nichts in deinem Browser.</li> <li>Schriftarten, Fotos und Zeichnungen werden vom selben Server geladen wie die Seite selbst. Es findet keine Verbindung zu Google Fonts oder anderen Drittanbietern statt.</li> </ul> <h2>3. Hosting und Server-Protokolle</h2> <p>Diese Website wird bei statichost.eu gehostet, einem Dienst von Variable Object Assignment, c/o Knackeriet, Svartmangatan 9, 111 29 Stockholm, Schweden. Die Server stehen nach Angaben des Anbieters in der Europäischen Union; eine Übermittlung in Drittländer findet nicht statt.</p> <p>Beim Aufruf der Seite verarbeitet der Anbieter deine IP-Adresse sowie technisch notwendige Angaben zur Anfrage (abgerufene Datei, Zeitpunkt, Browser), um dir die Seite ausliefern zu können. Nach Angaben des Anbieters wird die IP-Adresse dabei nur für die Dauer der Anfrage im Arbeitsspeicher verarbeitet und nicht protokolliert. Für die Abrechnung werden technische Protokolle ohne personenbezogene Daten (vor allem die übertragene Datenmenge) höchstens sieben Tage aufbewahrt. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO; das berechtigte Interesse liegt in der zuverlässigen und sicheren Bereitstellung der Website. statichost.eu ist Auftragsverarbeiter im Sinne von Art. 28 DSGVO; der Anbieter stellt dafür einen eigenen Vertrag zur Auftragsverarbeitung bereit. Weitere Informationen: <a href="https://www.statichost.eu/privacy/" rel="noopener">Datenschutzerklärung von statichost.eu</a>.</p> <h2>4. Werbelinks zum Amazon-Partnerprogramm</h2> <p>Einige Seiten enthalten mit einem Sternchen gekennzeichnete Links zu Produkten bei Amazon.de. Der Betreiber nimmt am Partnerprogramm von Amazon Europe Core S.à r.l. teil und erhält eine Provision, wenn du über einen solchen Link einkaufst. Auf dieser Website werden dafür keine Skripte, Bilder oder Cookies von Amazon geladen. Erst wenn du einen Werbelink anklickst, wirst du zu Amazon weitergeleitet; Amazon kann dann Cookies setzen, um die Herkunft der Bestellung zuzuordnen. Einzelheiten findest du in der <a href="https://www.amazon.de/gp/help/customer/display.html?nodeId=201909010" target="_blank" rel="noopener">Datenschutzerklärung von Amazon<span class="sr-only"> (öffnet in neuem Fenster)</span></a>.</p> <h2>5. Externe Links</h2> <p>Die Seite verlinkt auf externe Angebote wie Wikipedia oder den Vogelkompass. Erst wenn du einen solchen Link anklickst, wird eine Verbindung zum jeweiligen Anbieter aufgebaut.</p> <h2>6. Kontakt per E-Mail</h2> <p>Wenn du mir eine E-Mail schreibst, verarbeite ich deine Adresse und den Inhalt der Nachricht, um dir zu antworten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Die Nachricht wird gelöscht, sobald dein Anliegen erledigt ist und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p> <h2>7. Deine Rechte</h2> <p>Du hast das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch (Art. 21). Wende dich dafür an die im Impressum genannte Adresse. Außerdem kannst du dich bei einer Datenschutz-Aufsichtsbehörde beschweren (Art. 77 DSGVO). Für den Betreiber zuständig ist die Landesbeauftragte für Datenschutz und Informationsfreiheit der Freien Hansestadt Bremen.</p> </div> </section>'''


def credit_table(label, head, rows):
    return (f'<div class="wrap"><div class="cmp-wrap" tabindex="0" role="region" aria-label="{label}"><table class="cmp"><thead><tr><th scope="col">{head}</th>'
            f'<th scope="col">Urheber</th><th scope="col">Lizenz</th><th scope="col">Quelle</th></tr></thead><tbody>{rows}</tbody></table></div></div>')


def bildnachweis():
    animals = sorted(CREDITS, key=lambda k: name_of(key_of_photo(k)))
    rows = "".join(credit_row(f"f-{k}", name_of(key_of_photo(k)), *CREDITS[k]) for k in animals)
    prows = "".join(credit_row(f"p-{k}", PRODUCTS[k]["name"], a, lic, url) for k, (a, lic, url) in PHOTO.items())
    return ('<section class="block page"> <div class="wrap prose"> <h1>Bildnachweis und Lizenzen</h1> <h2>Fotos</h2> <p>Alle Fotos stammen von Wikimedia Commons und stehen '
            'unter den genannten freien Lizenzen. Für die Seite wurden sie verkleinert und zugeschnitten. Die Lizenz ist jeweils mit ihrem Lizenztext verlinkt, die Quelle mit '
            'der Originaldatei. Bearbeitete Fotos unter einer Share-alike-Lizenz (BY-SA) stehen unter derselben Lizenz wie das Original.</p> </div> '
            f'{credit_table("Bildnachweis der Tierfotos", "Art", rows)} '
            '<div class="wrap prose"> <h2>Fotos zu den Produktempfehlungen</h2> <p>Die Fotos sind als Beispielfoto gekennzeichnet. Sie zeigen typische Geräte und Beispiele, '
            'nicht das verlinkte Produkt. Sichtbare Markenlogos wurden unkenntlich gemacht.</p> </div> '
            f'{credit_table("Bildnachweis der Produktfotos", "Empfehlung", prows)} '
            '<div class="wrap prose"> <h2>Zeichnungen</h2> <p>Die Trittsiegel sind eigene Zeichnungen für den Waldtierkompass. Sie zeigen typische Formen und sind nicht '
            'maßstabsgetreu.</p> <h2>Schriften</h2> <p>Fraunces (Undercase Type) und Figtree (Erik Kennedy), beide unter der SIL Open Font License 1.1, lokal eingebunden '
            'über das Projekt Fontsource.</p> </div> </section>')


ABOUT_SISTERS = [
    ("Vogelkompass", "Vögel in Deutschland erkennen, mit Rufen zum Anhören"),
    ("Meereskompass", "Seevögel, Robben, Wale und Strandfunde an Nord- und Ostsee"),
    ("Gartentierkompass", "Igel, Käfer, Schnecken und Schmetterlinge im Garten erkennen"),
]


def about(R):
    """Über den Waldtierkompass: wer die Seite macht, woher die Inhalte stammen, wie sie sich finanziert (wie beim Vogelkompass).
    Wichtig für Vertrauen bei Besuchern und für Google (Erfahrung, Fachwissen, Vertrauenswürdigkeit)."""
    sis = "\n".join(f'<li><a href="{SISTER_URL[n]}" rel="noopener">{n}</a>: {d}</li>' for n, d in ABOUT_SISTERS)
    return f'''<section class="block page"> <div class="wrap prose"> <h1>Über den Waldtierkompass</h1>
<p>Der Waldtierkompass hilft dir, die Tiere zu erkennen, die dir in Deutschland im Wald und am Waldrand begegnen, und die Spuren, die sie hinterlassen. Er zeigt {len(SPECIES)} typische Arten, von Reh und Fuchs über Igel und Fledermaus bis zu Feuersalamander und Hirschkäfer, mit Foto, Merkmalen und Aktivität im Jahresverlauf. In {len(PAIRS)} Vergleichen erklärt er, wie du sie von ihren Doppelgängern unterscheidest.</p>
<h2>Wer den Waldtierkompass macht</h2>
<p>Den Waldtierkompass betreibt Nico Schober aus Bremen als privates, unabhängiges Angebot. Texte, Auswahl der Arten und Gestaltung stammen von ihm. Die Seite gehört zu keinem Verband, keiner Jägerschaft und keinem Hersteller. Die Kontaktdaten stehen im <a href="{R}impressum/index.html">Impressum</a>. Mehr über ihn erfährst du auf seiner Website <a href="https://nicoschober.com/" target="_blank" rel="noopener">nicoschober.com<span class="sr-only"> (öffnet in neuem Fenster)</span></a>.</p>
<h2>Woher die Inhalte stammen</h2>
<ul>
<li><b>Steckbriefe:</b> Merkmale, Größe und Lebensweise sind kurz und alltagstauglich zusammengefasst. Jede Artseite verlinkt unter „Mehr erfahren“ den passenden Wikipedia-Artikel zum Nachlesen.</li>
<li><b>Jahreszeiten und Aktivität:</b> Die Angaben, wann eine Art aktiv und gut zu sehen ist, sind grobe Richtwerte für Deutschland. Je nach Region, Höhenlage und Wetter weichen sie ab.</li>
<li><b>Fotos:</b> von Wikimedia Commons, unter freien Lizenzen, mit Namen der Fotografinnen und Fotografen an jedem Bild.</li>
<li><b>Trittsiegel:</b> eigene, vereinfachte Zeichnungen. Die Größenangaben sind typische Werte, einzelne Abdrücke können je nach Boden und Tier abweichen.</li>
</ul>
<p>Alle Urheber und Lizenzen stehen gesammelt unter <a href="{R}bildnachweis/index.html">Bildnachweis und Lizenzen</a>.</p>
<h2>Wie sich die Seite finanziert</h2>
<p>Der Waldtierkompass ist kostenlos und ohne Anmeldung nutzbar. Einige Seiten empfehlen Ferngläser, Wildkameras oder Bücher mit Werbelinks zu Amazon, die mit * gekennzeichnet sind. Kaufst du über einen solchen Link, erhält der Betreiber eine kleine Provision, für dich ändert sich am Preis nichts. Die Empfehlungen sind nicht selbst getestet, und Hersteller haben keinen Einfluss auf die Auswahl.</p>
<h2>Deine Daten</h2>
<p>Der Waldtierkompass setzt keine Cookies, misst keine Reichweite und speichert nichts in deinem Browser. Mehr dazu in der <a href="{R}datenschutz/index.html">Datenschutzerklärung</a>.</p>
<h2>Fehler gefunden?</h2>
<p>Wenn dir eine falsche Angabe, ein falsch zugeordnetes Foto oder eine ungenaue Spur auffällt, schreib gern an <a href="mailto:info@nicoschober.com">info@nicoschober.com</a>. Hinweise werden geprüft und eingearbeitet.</p>
<h2>Schwesterseiten</h2>
<ul>
{sis}
</ul> </div> </section>'''


def build():
    R = "../"
    write("impressum/index.html", page("impressum/index.html", "Impressum", "Impressum des Waldtierkompass: Anbieter Nico Schober aus Bremen, Kontakt per E-Mail, Hinweise zu Haftung, Links und Urheberrecht.", IMPRESSUM, crumbs=[("Impressum", "")]))
    write("datenschutz/index.html", page("datenschutz/index.html", "Datenschutz", "Datenschutz beim Waldtierkompass: keine Cookies, kein Tracking, Hosting in der EU bei statichost.eu und deine Rechte nach der DSGVO.", DATENSCHUTZ, crumbs=[("Datenschutz", "")]))
    write("bildnachweis/index.html", page("bildnachweis/index.html", "Bildnachweis und Lizenzen", "Bildnachweis des Waldtierkompass: Fotografinnen, Fotografen und freie Lizenzen aller Tierfotos von Wikimedia Commons auf einen Blick.", bildnachweis(),
                                          crumbs=[("Bildnachweis", "")]))
    ld = {"@context": "https://schema.org", "@type": "AboutPage", "name": f"Über den {SITE}", "url": f"{DOMAIN}/ueber/", "inLanguage": "de-DE",
          "mainEntity": {**AUTHOR, "address": {"@type": "PostalAddress", "addressLocality": "Bremen", "addressCountry": "DE"}},
          "about": {"@type": "WebSite", "name": SITE, "url": DOMAIN + "/"}}
    write("ueber/index.html", page("ueber/index.html", "Über den Waldtierkompass: Macher, Quellen, Finanzierung",
                                   "Wer den Waldtierkompass macht, woher Fotos, Steckbriefe und Trittsiegel stammen, wie die Seite sich finanziert und wie du Fehler meldest.",
                                   about(R), crumbs=[("Über den Waldtierkompass", "")], ld=ld))
