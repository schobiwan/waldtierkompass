# -*- coding: utf-8 -*-
"""Symbole, Logo und Favicon als SVG."""

ICON = {
 "pack": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6V4.5A1.5 1.5 0 0 1 10.5 3h3A1.5 1.5 0 0 1 15 4.5V6"/><rect x="5" y="6" width="14" height="15" rx="4"/><path d="M9 13h6M9 13v3h6v-3"/></svg>',
 "chev": '<svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="m7 10 5 5 5-5"/></svg>',
 "find": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/></svg>',
 "track": '<svg viewBox="0 0 24 24" aria-hidden="true"><ellipse cx="12" cy="15.5" rx="4" ry="3.5"/><circle cx="6.5" cy="10" r="1.7"/><circle cx="10" cy="6.5" r="1.7"/><circle cx="14" cy="6.5" r="1.7"/><circle cx="17.5" cy="10" r="1.7"/></svg>',
 "pair": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="6" width="8" height="12" rx="2"/><rect x="13" y="6" width="8" height="12" rx="2"/></svg>',
 "year": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>',
 "arrow": '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"></path></svg>',
 "moon": '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10.5 2.5a5.5 5.5 0 1 0 3 9.6A6 6 0 0 1 10.5 2.5z" fill="currentColor" stroke="none"/></svg>',
 "sun": '<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="3"/><path d="M8 1.5v2M8 12.5v2M1.5 8h2M12.5 8h2M3.4 3.4l1.4 1.4M11.2 11.2l1.4 1.4M3.4 12.6l1.4-1.4M11.2 4.8l1.4-1.4"/></svg>',
 "dusk": '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 11.5h12M4 11.5a4 4 0 0 1 8 0M8 3.5v2M3.2 6.2l1.3 1.1M12.8 6.2l-1.3 1.1"/></svg>',
}
# Aktivität → Symbol (einmal pro Seite als <symbol>, dann per <use>)
ACT_ICON = {"tag": "sun", "daemmerung": "dusk", "nacht": "moon"}

# Symbole der Produktempfehlungen ohne Foto
PICON = {
 "binoc": '<circle cx="8" cy="15" r="4.5"/><circle cx="16" cy="15" r="4.5"/><path d="M8 10.5V6h3v6M16 10.5V6h-3v6"/>',
 "cam": '<rect x="4" y="5" width="16" height="15" rx="3"/><circle cx="12" cy="12" r="3.5"/><circle cx="12" cy="12" r="1"/><path d="M8 17h8"/>',
 "lamp": '<path d="M4 12c0-2 2-3 8-3s8 1 8 3"/><rect x="9" y="9" width="6" height="5" rx="1.5"/><path d="M12 14v2M7 19l2-3M17 19l-2-3"/>',
 "book": '<path d="M4 5h6a2 2 0 0 1 2 2v12a2 2 0 0 0-2-2H4zM20 5h-6a2 2 0 0 0-2 2v12a2 2 0 0 1 2-2h6z"/>',
 "wave": '<path d="M3 12h2l2-5 3 10 3-12 3 10 2-3h3"/>',
 "lens": '<circle cx="10" cy="10" r="5.5"/><path d="m14 14 6 6"/>',
}


def icon_symbols():
    out = []
    for k in ACT_ICON.values():
        inner = ICON[k].split(">", 1)[1].rsplit("</svg>", 1)[0]
        out.append(f'<symbol id="i-{k}" viewBox="0 0 16 16">{inner}</symbol>')
    return "".join(out)


def act_svg(a):
    return f'<svg aria-hidden="true"><use href="#i-{ACT_ICON[a]}"></use></svg>'


def focusless(k):
    """Symbol für die Suchdaten (ohne Fokus in alten Browsern)."""
    return ICON[k].replace('aria-hidden="true"', 'aria-hidden="true" focusable="false"')


PAW = ('<path d="M24 25c4 0 6.5 3 6.5 5.6 0 2.6-2.4 3.6-6.5 2.8-4.1.8-6.5-.2-6.5-2.8 0-2.6 2.5-5.6 6.5-5.6z"/>'
       '<ellipse cx="20.6" cy="17.6" rx="2.3" ry="3"/><ellipse cx="27.4" cy="17.6" rx="2.3" ry="3"/>'
       '<ellipse cx="15.8" cy="22.6" rx="2.1" ry="2.7" transform="rotate(-25 15.8 22.6)"/>'
       '<ellipse cx="32.2" cy="22.6" rx="2.1" ry="2.7" transform="rotate(25 32.2 22.6)"/>')

LOGO = ('<svg class="logo-defs" aria-hidden="true" focusable="false"><symbol id="logo-mark" viewBox="0 0 48 48">'
        '<circle cx="24" cy="24" r="21" fill="none" stroke="currentColor" stroke-width="2.2"></circle>'
        '<circle cx="24" cy="24" r="17" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 2.5" stroke-opacity=".6"></circle>'
        '<g fill="currentColor">' + PAW + '</g><path d="M24 1.8 26.6 7.4H21.4z" fill="var(--logo-accent)"></path>'
        '</symbol>' + icon_symbols() + '</svg>')

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="11" fill="#3b2a20"/>'
           '<circle cx="24" cy="25" r="17.5" fill="none" stroke="#f6efe4" stroke-width="2.4"/>'
           '<g fill="#f6efe4" transform="translate(0 1)">' + PAW + '</g><path d="M24 4.5 27 10.5H21z" fill="#e8a24a"/></svg>')

LOGO_USE = '<svg class="logo" aria-hidden="true"><use href="#logo-mark"></use></svg>'
