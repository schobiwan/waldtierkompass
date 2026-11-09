#!/usr/bin/env python3
"""Prüft die gebaute Seite ohne Server: alle internen Links und Sprungmarken (#…) müssen existieren,
jede Seite braucht genau eine h1, einen Titel und eine Beschreibung bis 160 Zeichen.

Aufruf:  python3 tools/check.py          (prüft dist/ und, falls vorhanden, preview/)
Ende mit Fehlercode 1, wenn etwas kaputt ist.
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HREF = re.compile(r'href="([^"]+)"')
ID = re.compile(r'\sid="([^"]+)"')


def target_file(root, page_dir, href):
    """Datei, auf die ein interner Link zeigt (Ordner-Adressen → index.html)."""
    path = href.split("#")[0].split("?")[0]
    if not path:
        return None
    base = root if path.startswith("/") else page_dir
    full = os.path.normpath(os.path.join(base, path.lstrip("/")))
    if path.endswith("/") or os.path.isdir(full):
        full = os.path.join(full, "index.html")
    return full


def check(root):
    problems, pages, ids = [], {}, {}
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(".html"):
                fp = os.path.join(d, f)
                pages[fp] = open(fp, encoding="utf-8").read()
                ids[fp] = set(ID.findall(pages[fp]))
    links = 0
    for fp, t in pages.items():
        rel = os.path.relpath(fp, root)
        if t.count("<h1") != 1:
            problems.append(f"{rel}: {t.count('<h1')} h1-Überschriften")
        desc = re.search(r'<meta name="description" content="([^"]*)"', t)
        if not re.search(r"<title>[^<]+</title>", t) or not desc:
            problems.append(f"{rel}: Titel oder Beschreibung fehlt")
        elif len(html.unescape(desc.group(1))) > 160:
            problems.append(f"{rel}: Beschreibung länger als 160 Zeichen")
        for href in set(HREF.findall(t)):
            if re.match(r"[a-z]+:|//", href):
                continue  # extern, mailto:
            links += 1
            frag = href.split("#")[1] if "#" in href else ""
            tgt = fp if href.startswith("#") else target_file(root, os.path.dirname(fp), href)
            if tgt is None:
                tgt = fp
            if not os.path.exists(tgt):
                problems.append(f"{rel}: Link ins Leere → {href}")
            elif frag and tgt.endswith(".html") and frag not in ids.get(tgt, set()):
                problems.append(f"{rel}: Sprungmarke fehlt → {href}")
    return links, len(pages), problems


if __name__ == "__main__":
    failed = False
    for name in ("dist", "preview"):
        root = os.path.join(HERE, name)
        if not os.path.isdir(root):
            continue
        links, n, problems = check(root)
        print(f"{name}: {n} Seiten, {links} interne Links, {len(problems)} Probleme")
        for p in problems[:50]:
            print("  ", p)
        failed |= bool(problems)
    sys.exit(1 if failed else 0)
