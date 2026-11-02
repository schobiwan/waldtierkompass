# -*- coding: utf-8 -*-
"""Trittsiegel als SVG (eigene Zeichnungen)."""
import math

def E(cx, cy, rx, ry, rot=0, extra=""):
    t = f' transform="rotate({rot:.1f} {cx:.1f} {cy:.1f})"' if rot else ""
    return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}"{t}{extra}/>'

# ---------- Trittsiegel, gezeichnet in einer Box ca. 0..100 ----------
def hoof(w=1.0, l=1.0, round_=0.0, dew=False):
    # zwei Schalen um x=50, Spitze oben
    hw = 15 * w; L = 70 * l; top = 50 - L / 2; bot = 50 + L / 2
    gap = 2.5
    def half(sgn):
        x0 = 50 + sgn * gap
        xo = 50 + sgn * (gap + hw)
        tipx = 50 + sgn * (gap + hw * (0.15 + round_ * 0.5))
        return (f'<path d="M{x0:.1f} {top+6:.1f} '
                f'C{tipx:.1f} {top-2:.1f} {xo:.1f} {top+L*0.25:.1f} {xo:.1f} {top+L*0.6:.1f} '
                f'C{xo:.1f} {bot-4:.1f} {50+sgn*(gap+hw*0.55):.1f} {bot+2:.1f} {x0:.1f} {bot-3:.1f} Z"/>')
    s = half(-1) + half(1)
    if dew:
        s += E(50 - hw - 10, bot + 16, 4.5, 7, -15) + E(50 + hw + 10, bot + 16, 4.5, 7, 15)
    return s

def canid(scale=1.0, narrow=1.0):
    s = ""
    s += '<path d="M50 60 C62 60 70 70 70 79 C70 88 62 92 50 88 C38 92 30 88 30 79 C30 70 38 60 50 60 Z"/>'
    for (x, y, rx, ry, r) in [(41*1, 38, 7.5, 10, -8), (59, 38, 7.5, 10, 8), (27 + (1-narrow)*6, 56, 7, 9, -25), (73 - (1-narrow)*6, 56, 7, 9, 25)]:
        s += E(x, y, rx, ry, r)
    for (x, y, r) in [(42, 23, -8), (58, 23, 8), (24, 43, -25), (76, 43, 25)]:
        s += E(x, y, 2, 3.4, r)
    return s

def felid():
    s = '<path d="M50 56 C60 56 66 60 70 66 C76 70 76 82 68 86 C62 90 56 86 50 88 C44 86 38 90 32 86 C24 82 24 70 30 66 C34 60 40 56 50 56 Z"/>'
    for (x, y, rx, ry) in [(37, 37, 8, 9.5), (55, 33, 8, 9.5), (24, 52, 7.5, 8.5), (73, 48, 7.5, 8.5)]:
        s += E(x, y, rx, ry)
    return s

def mustelid(claws=True, wide=False):
    s = '<path d="M30 70 C30 60 40 56 50 60 C60 56 70 60 70 70 C70 80 60 82 50 79 C40 82 30 80 30 70 Z"/>'
    pts = [(22, 48), (35, 38), (50, 34), (65, 38), (78, 48)] if not wide else [(20, 44), (35, 40), (50, 38), (65, 40), (80, 44)]
    for i, (x, y) in enumerate(pts):
        s += E(x, y, 5.5, 7)
        if claws:
            L = 14 if wide else 5
            s += f'<path d="M{x:.1f} {y-8:.1f} L{x+(x-50)*0.12:.1f} {y-8-L:.1f}" stroke-width="3.2" stroke-linecap="round" fill="none"/>'
    return s

def raccoon():
    s = '<path d="M34 62 C34 54 44 52 50 54 C56 52 66 54 66 62 C68 74 60 84 50 84 C40 84 32 74 34 62 Z"/>'
    for ang in (-62, -30, 0, 30, 62):
        a = math.radians(ang - 90)
        x1, y1 = 50 + 16 * math.cos(a), 56 + 16 * math.sin(a)
        x2, y2 = 50 + 38 * math.cos(a), 56 + 38 * math.sin(a)
        s += f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke-width="9" stroke-linecap="round" fill="none"/>'
    return s

def hedgehog():
    s = '<path d="M36 64 C36 56 44 54 50 56 C56 54 64 56 64 64 C64 74 56 78 50 76 C44 78 36 74 36 64 Z"/>'
    for (x, y) in [(27, 50), (36, 40), (50, 36), (64, 40), (73, 50)]:
        s += E(x, y, 5, 6)
    return s

def leaping(big=True):
    # Hase/Kaninchen: Hinterläufe vorne nebeneinander, Vorderläufe hintereinander
    k = 1 if big else 0.8
    s = E(34, 26, 8 * k, 20 * k, -6) + E(66, 26, 8 * k, 20 * k, 6)
    s += E(50, 62, 6 * k, 9 * k) + E(48, 86, 6 * k, 9 * k)
    return s

def squirrel():
    s = ""
    for x0 in (30, 70):
        s += E(x0, 34, 7, 11)
        for (dx, dy) in [(-10, -12), (-4, -18), (4, -18), (10, -12), (13, -2)]:
            s += E(x0 + dx * (1 if x0 > 50 else -1) * -1, 34 + dy, 2.6, 4)
    for x0 in (38, 62):
        s += E(x0, 76, 5.5, 7)
        for (dx, dy) in [(-7, -9), (-2, -12), (3, -12), (8, -9)]:
            s += E(x0 + dx, 76 + dy, 2.2, 3.2)
    return s

def rodent():
    s = ""
    for (x0, y0, k) in [(34, 30, 1), (66, 30, 1), (40, 72, .8), (60, 72, .8)]:
        s += E(x0, y0, 5 * k, 6 * k)
        for ang in (-70, -30, 10, 50):
            a = math.radians(ang - 90)
            s += E(x0 + 11 * k * math.cos(a), y0 + 11 * k * math.sin(a), 1.8 * k, 3 * k, ang)
    return s

def mole():
    s = ""
    for x0, flip in ((32, -1), (68, 1)):
        s += E(x0, 58, 11, 13, flip * 15)
        for i, ang in enumerate((-40, -20, 0, 20, 40)):
            a = math.radians(ang - 90 + flip * 15)
            s += f'<path d="M{x0+10*math.cos(a):.1f} {58+12*math.sin(a):.1f} L{x0+24*math.cos(a):.1f} {58+26*math.sin(a):.1f}" stroke-width="3.4" stroke-linecap="round" fill="none"/>'
    return s

TRACKS = {
 "hoof_small": lambda: hoof(0.75, 0.9, 0.0),
 "hoof_mid": lambda: hoof(0.9, 0.95, 0.3),
 "hoof_large": lambda: hoof(1.1, 1.0, 0.6),
 "hoof_boar": lambda: hoof(1.0, 0.72, 0.7, dew=True),
 "canid": lambda: canid(),
 "canid_large": lambda: canid(narrow=1.2),
 "felid": felid, "felid_large": felid,
 "mustelid": lambda: mustelid(), "mustelid_small": lambda: mustelid(),
 "badger": lambda: mustelid(True, True),
 "raccoon": raccoon, "hedgehog": hedgehog,
 "hare": lambda: leaping(True), "hare_small": lambda: leaping(False),
 "squirrel": squirrel, "rodent": rodent, "mole": mole,
}

def is_track(art):
    return art in TRACKS

def glyph(art):
    return TRACKS[art]()

def small_track(art, ink="currentColor"):
    """Nur das Motiv, für Spuren-Seite und Quiz (viewBox 0 0 100 100)."""
    return f'<svg viewBox="0 0 100 100" aria-hidden="true" fill="{ink}" stroke="{ink}">{glyph(art)}</svg>'
