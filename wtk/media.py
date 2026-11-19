# -*- coding: utf-8 -*-
"""Fotos, Lizenzangaben und Links, die in einem neuen Fenster öffnen."""
import re

from .helpers import CREDITS, esc

SIZES_CARD = "(max-width: 760px) 46vw, 320px"


def new_tab(url, text, note="öffnet in neuem Fenster", rel="noopener"):
    """Link in neuem Fenster, mit Hinweis für Screenreader (WCAG 3.2.5)."""
    return f'<a href="{url}" target="_blank" rel="{rel}">{text}<span class="sr-only"> ({note})</span></a>'


def img(R, key, alt="", eager=False, cls="", sizes=SIZES_CARD):
    lz = "eager" if eager else "lazy"
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{R}photos/{key}.webp" srcset="{R}photos/{key}-400.webp 400w, {R}photos/{key}.webp 720w" sizes="{sizes}" '
            f'alt="{esc(alt)}" width="720" height="576" loading="{lz}" decoding="async">')


def lic_url(lic):
    """Link auf den Lizenztext (Creative Commons verlangt ihn bei jeder Nutzung)."""
    m = re.match(r"CC (BY(?:-SA)?) (\d\.\d)(?: (\w\w))?$", lic)
    if m:
        return f"https://creativecommons.org/licenses/{m.group(1).lower()}/{m.group(2)}/" + (f"{m.group(3)}/" if m.group(3) else "")
    if lic == "CC0":
        return "https://creativecommons.org/publicdomain/zero/1.0/deed.de"
    return ""


def lic_link(lic):
    u = lic_url(lic)
    return new_tab(u, esc(lic), "Lizenztext, öffnet in neuem Fenster", "noopener license") if u else esc(lic)


def credit(key, short=False):
    """Vollständige Bildangabe mit verlinkter Quelle und Lizenz."""
    a, lic, url = CREDITS[key]
    return (f'Foto: {new_tab(esc(url), esc(a), "Quelle, öffnet in neuem Fenster")}, {lic_link(lic)}'
            + ("" if short else ", Wikimedia Commons, zugeschnitten"))


def cred(key, R="", cls="", id_=""):
    """Bildangabe unter dem Foto: ein gut tippbarer Link zur Bildnachweis-Seite mit allen verlinkten Lizenzangaben."""
    a, lic, _ = CREDITS[key]
    c = f" {cls}" if cls else ""
    i = f' id="{id_}"' if id_ else ""
    return f'<a class="cred{c}"{i} href="{R}bildnachweis/index.html#f-{key}">Foto: {esc(a)}, {esc(lic)}<span class="sr-only"> – Lizenzangaben im Bildnachweis</span></a>'


def credit_row(anchor, label, a, lic, url):
    """Tabellenzeile im Bildnachweis."""
    return (f'<tr id="{anchor}"><th scope="row">{esc(label)}</th><td>{esc(a)}</td><td>{lic_link(lic)}</td>'
            f'<td>{new_tab(esc(url), "Quelle")}</td></tr>')
