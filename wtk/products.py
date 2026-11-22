# -*- coding: utf-8 -*-
"""Ausrüstungsempfehlungen mit Amazon-Werbelinks: Produkte, Beispielfotos, Auswahl je Art und Gruppe."""
from .config import TAG
from .helpers import esc
from .icons import ICON, PICON


def amazon(path):
    return f"https://www.amazon.de/{path}tag={TAG}"


PRODUCTS = {
 "fernglas": dict(cat="Fernglas", name="Celestron Nature DX 8x42", by="Celestron", tip=True, icon="binoc",
   why="Helles Einsteigerglas für die Dämmerung: 8-fache Vergrößerung, wasserdicht und leicht genug für lange Ansitze.",
   url=amazon("dp/B00B73JONS?")),
 "wildkamera": dict(cat="Wildkamera", name="Wildkamera mit Nachtsicht", by="Auswahl bei Amazon", tip=True, icon="cam",
   why="Zeigt dir, wer nachts am Bau oder an der Futterstelle vorbeikommt. Achte auf unsichtbares Infrarot (No-Glow), damit die Tiere nicht gestört werden.",
   url=amazon("s?k=wildkamera+no+glow&")),
 "lampe": dict(cat="Stirnlampe", name="Stirnlampe mit Rotlicht", by="Auswahl bei Amazon", tip=False, icon="lamp",
   why="Rotes Licht blendet Tiere kaum und schont deine Nachtsicht, ideal für Kröten- und Salamanderabende.",
   url=amazon("s?k=stirnlampe+rotlicht&")),
 "buch": dict(cat="Buch", name="Bestimmungsbuch Tierspuren", by="Auswahl bei Amazon", tip=True, icon="book",
   why="Ein Spurenführer mit Zeichnungen der Trittsiegel in Originalgröße hilft draußen beim Vergleichen.",
   url=amazon("s?k=tierspuren+bestimmen+buch&")),
 "detektor": dict(cat="Zubehör", name="Fledermaus-Detektor", by="Auswahl bei Amazon", tip=False, icon="wave",
   why="Macht die Ultraschallrufe der Fledermäuse hörbar. Schon einfache Geräte zeigen, wer über dem Weg jagt.",
   url=amazon("s?k=fledermaus+detektor&")),
 "lupe": dict(cat="Zubehör", name="Einschlaglupe 10-fach", by="Auswahl bei Amazon", tip=False, icon="lens",
   why="Für Fraßspuren an Nüssen und Zapfen: Zahnspuren werden mit der Lupe eindeutig.",
   url=amazon("s?k=einschlaglupe+10x&")),
 "waermebild": dict(cat="Wärmebild", name="Wärmebildkamera für Naturbeobachtung", by="Auswahl bei Amazon", tip=False, icon="binoc",
   why="Zeigt warme Tierkörper auch in völliger Dunkelheit und hinter dünnem Gebüsch. So entdeckst du Reh, Fuchs oder Dachs, ohne Licht zu machen.",
   url=amazon("s?k=w%C3%A4rmebildkamera+monokular&")),
 "gips": dict(cat="Spuren", name="Modellgips für Spurenabdrücke", by="Auswahl bei Amazon", tip=False, icon="book",
   why="Mit etwas Gips hältst du ein Trittsiegel aus dem Matsch dauerhaft fest. Ein schönes Projekt für Kinder und Spurensammler.",
   url=amazon("s?k=modellgips&")),
 "igelhaus": dict(cat="Garten", name="Igelhaus für den Garten", by="Auswahl bei Amazon", tip=False, icon="book",
   why="Ein geschützter Platz für den Winterschlaf. Stelle es an eine ruhige, schattige Stelle unter Hecken oder Laub.",
   url=amazon("s?k=igelhaus+winterfest&")),
 "fledermauskasten": dict(cat="Garten", name="Fledermauskasten aus Holzbeton", by="Auswahl bei Amazon", tip=False, icon="wave",
   why="Ersatzquartier für Fledermäuse wie das Braune Langohr. In drei bis fünf Metern Höhe aufhängen, möglichst ohne Lampe in der Nähe.",
   url=amazon("s?k=fledermauskasten+holzbeton&")),
 "futterkasten": dict(cat="Garten", name="Futterkasten für Eichhörnchen", by="Auswahl bei Amazon", tip=False, icon="book",
   why="Mit Klappdeckel, damit Vögel nicht mitfressen. Am Baumstamm aufgehängt, siehst du die Kletterer aus nächster Nähe.",
   url=amazon("s?k=eichh%C3%B6rnchen+futterkasten&")),
}

# Beispielfotos (nicht das verlinkte Produkt): Schlüssel → (Urheber, Lizenz, Quelle)
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

# Empfehlungen auf den Artseiten: erst nach Art, sonst nach Gruppe
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


def gear_for(s):
    return GEAR_FOR.get(s["k"]) or GEAR_GRP[s["grp"]]


def gear_for_month(m):
    """Empfehlungen je Jahreszeit auf den Monatsseiten."""
    if m in (10, 11, 12, 1, 2):
        return ("igelhaus", "futterkasten", "fernglas", "waermebild")
    if m in (3, 4, 5):
        return ("lampe", "buch", "fledermauskasten", "wildkamera")
    return ("fledermauskasten", "detektor", "wildkamera", "lupe")


ADNOTE = '<p class="adnote"><span aria-hidden="true">*</span> Werbelink: Wenn du über diesen Link etwas kaufst, erhält der Waldtierkompass eine kleine Provision von Amazon. Für dich ändert sich am Preis nichts. Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p>'


def pcred(R, key, cls):
    a, lic, _ = PHOTO[key]
    return f'<a class="cred {cls}" href="{R}bildnachweis/index.html#p-{key}">Beispielfoto · Foto: {esc(a)}, {esc(lic)}<span class="sr-only"> – Lizenzangaben im Bildnachweis</span></a>'


def product(R, key, compact=False, sizes="(max-width: 560px) 46vw, 280px"):
    """Produktkarte; compact = schmale Fassung für die Seitenleiste der Artseiten."""
    p = PRODUCTS[key]
    has_photo = key in PHOTO
    tip = '<span class="ptip">Unser Tipp</span>' if p["tip"] and not compact else ""
    why = f'<p class="pwhy">{esc(p["why"])}</p>' if not compact else ""
    meta = f'<span>{p["cat"]}{" · Unser Tipp" if (p["tip"] and compact) else ""}</span>'
    if has_photo:
        sz = "88px" if compact else sizes
        pic = (f'<picture><source type="image/avif" srcset="{R}photos/p-{key}-400.avif 400w, {R}photos/p-{key}.avif 720w" sizes="{sz}">'
               f'<img src="{R}photos/p-{key}-400.webp" srcset="{R}photos/p-{key}-400.webp 400w, {R}photos/p-{key}.webp 720w" '
               f'sizes="{sz}" alt="" width="400" height="300" loading="lazy" decoding="async"></picture>')
    else:
        pic = f'<span class="picon"><svg viewBox="0 0 24 24" aria-hidden="true">{PICON[p["icon"]]}</svg></span>'
    under = pcred(R, key, "pcred") if (has_photo and not compact) else ""
    inside = pcred(R, key, "pcred2") if (has_photo and compact) else ""
    return (f'<li class="product{" pick" if p["tip"] else ""}"> <div class="pimg">{pic}{tip}</div>{under} '
            f'<div class="pbody"> <p class="pmeta">{meta}<span class="pad">Anzeige</span></p> <h3 class="pname">{esc(p["name"])}</h3> <p class="pby">{esc(p["by"])}</p> {why} {inside} '
            f'<a class="plink" href="{p["url"]}" target="_blank" rel="sponsored nofollow noopener"><span>Bei Amazon ansehen<span aria-hidden="true">*</span></span>{ICON["arrow"]}'
            f'<span class="sr-only"> {esc(p["name"])} (Werbelink, öffnet in neuem Fenster)</span></a> </div> </li>')


def gearband(R, title, picks):
    """Band mit Empfehlungen über die ganze Breite (Startseite, Spuren, Monatsseiten)."""
    return (f'<section class="gearband" aria-labelledby="h-gear"><div class="wrap"><div class="head-row"><h2 id="h-gear">{title}</h2>'
            f'<a class="gearmore" href="{R}ausruestung/index.html">Alle Empfehlungen ansehen</a></div>'
            f'<ul class="products">{"".join(product(R, g) for g in picks)}</ul>{ADNOTE}</div></section>')
