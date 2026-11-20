# -*- coding: utf-8 -*-
"""Feste Einstellungen: Name, Domain, Ausgabeordner, Stand der Inhalte, Partner-IDs."""
import datetime as _dt
import os
import sys

SITE = "Waldtierkompass"
DOMAIN = "https://waldtierkompass.de"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Live-Seite (dist/) mit kurzen Adressen wie /arten/dachs/.
# Mit --preview entsteht preview/ mit Links auf index.html für die Vorschau im Chat, die keine Ordner-Adressen kennt.
PREVIEW = "--preview" in sys.argv
OUT = os.path.join(HERE, "preview" if PREVIEW else "dist")
TOOLS = os.path.join(HERE, "node_modules", ".bin")

# Stand der Inhalte für die Autorenzeile und die Sitemap (bei inhaltlichen Änderungen anpassen)
CONTENT_UPDATED = (2026, 11, 19)
CONTENT_ISO = "%04d-%02d-%02d" % CONTENT_UPDATED

# IndexNow-Schlüssel (Datei <schlüssel>.txt im Wurzelverzeichnis; nie ändern oder löschen)
INDEXNOW_KEY = "5e1f0c9a7b3d4e8f9a2c6b1d0e7f3a48"

# Amazon-Partner-ID
TAG = "schobiwan-21"

# Awin-Bestätigung der Werbefläche (nur Startseite)
AWIN_META = '<meta name="verification" content="a0ca5410287e16bad10570b80f3630af">'

# Klassen, die nur per JavaScript gesetzt werden und purgecss deshalb nicht im HTML findet
CSS_SAFELIST = ["now", "open", "calm", "scrolled", "clear", "fcount", "pk", "sico"]

MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
MSHORT = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
MSLUG = ["januar", "februar", "maerz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember"]

# Aktueller Monat (deutsche Zeit) zum Zeitpunkt des Builds; die Seite korrigiert ihn im Browser, falls der Build älter ist
try:
    from zoneinfo import ZoneInfo
    NOWM = _dt.datetime.now(ZoneInfo("Europe/Berlin")).month
except Exception:
    NOWM = _dt.datetime.now().month

# Gemeinsame Kennung für Nico Schober auf allen Kompassseiten (Vogel-, Wald-, Meeres-, Gartentierkompass).
# Muss nicht erreichbar sein; so erkennt Google, dass dieselbe Person hinter allen Seiten steht.
PERSON_ID = "https://nicoschober.com/#person"
AUTHOR = {"@type": "Person", "@id": PERSON_ID, "name": "Nico Schober", "url": DOMAIN + "/ueber/"}

# Schwesterseiten (Fußzeile, Startseite, Über-Seite, llms.txt). Die Beschreibungen stehen jeweils dort, wo sie gebraucht werden.
SISTER_URL = {
    "Vogelkompass": "https://vogelkompass.de/",
    "Meereskompass": "https://meereskompass.de/",
    "Gartentierkompass": "https://gartentierkompass.de/",
}
