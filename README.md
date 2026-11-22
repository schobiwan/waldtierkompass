# Waldtierkompass

Statische Website zum Bestimmen von Waldtieren in Deutschland. Schwesterseite zum [Vogelkompass](https://vogelkompass.de/).

33 Arten mit Fotos, Trittsiegeln, Doppelgängern und Waldjahr.

## Ordner

| Pfad | Inhalt |
|---|---|
| `data.py` | Alle Texte: Arten, Doppelgänger, Ereignisse im Waldjahr |
| `credits.json` | Urheber, Lizenz und Quelle jedes Fotos (Wikimedia Commons) |
| `build.py` | Startet den Build: erzeugt alle Seiten in `dist/` |
| `wtk/config.py` | Einstellungen: Domain, Stand der Inhalte (`CONTENT_UPDATED`), IndexNow-Schlüssel, Partner-ID |
| `wtk/layout.py` | Seitengerüst: Kopf, Navigation, Schnellsuche, Brotkrumen, Fußzeile |
| `wtk/components.py` | Bausteine: Artkarte, Jahresband, Vergleichskarte, Filterknöpfe, Suchwörter |
| `wtk/products.py` | Ausrüstungsempfehlungen mit Werbelinks und Beispielfotos |
| `wtk/media.py`, `wtk/icons.py`, `wtk/helpers.py` | Fotos und Lizenzen, Symbole, Grammatik und Monatsangaben |
| `wtk/pages/` | Je Seitentyp ein Modul (Startseite, Arten, Doppelgänger, Waldjahr, Spuren, Ausrüstung, Rechtliches) |
| `wtk/finalize.py` | CSS und JavaScript bündeln, kurze Links, Sitemap, robots.txt |
| `art.py` | Zeichnet die Trittsiegel als SVG |
| `src/css/` | Stylesheet (`base.css` = Grundgerüst, `extra.css` = Ergänzungen) |
| `src/js/` | Skripte für Suche, Filter, Navigation und Monatsangaben (`text.js` und `search.js` ohne Seitenzugriff, in Node testbar) |
| `tests/` | Tests (siehe unten) |
| `photos/` | Tierfotos als WebP und AVIF (720 px und 400 px breit); AVIF nach neuen Fotos mit `node tools/make_avif.mjs` erzeugen |
| `photos_src/` | Ausgangsbild für das Vorschaubild in sozialen Netzwerken |
| `fonts/` | Fraunces und Figtree, lokal eingebunden |
| `dist/` | **Fertige Website** – diesen Ordner veröffentlichen |

## Bauen

Voraussetzungen: Python 3 mit Pillow, Node.js.

```bash
npm install
pip install pillow
npm run build      # oder: python3 build.py
```

Der Build schreibt `dist/` komplett neu, entfernt ungenutztes CSS, minifiziert CSS und JavaScript und erzeugt `sitemap.xml` und `robots.txt`.

## Testen

```bash
npm test               # baut dist/ und prüft Daten, Bausteine, fertige Seiten, Suche und alle internen Links
npm run test:browser   # danach: Bedienung in Chrome und Barrierefreiheit (axe, WCAG 2.2 AA) auf allen Seiten
```

- `tests/test_data.py` – Inhalte: Pflichtfelder, Monate, Doppelgänger-Verweise, Fotos und Bildnachweise, Werbelinks
- `tests/test_helpers.py` – Grammatik („dem Braunen Langohr“), Monatsangaben, Lizenzlinks, Titel- und Beschreibungslängen
- `tests/test_output.py` – fertige Seiten: Aufbau, keine vergessenen Platzhalter, Alt-Texte, Strukturdaten, Sitemap, Größenbudgets
- `tests/js/` – Suche, Tippfehler-Korrektur und Schwesterseiten-Hinweise
- `tests/browser/run.mjs` – Suche, Filter, Menü und Tastatur im echten Browser; axe hell/dunkel auf Handy und Computer
- `tools/check.py` – interne Links und Sprungmarken, eine h1, Titel und Beschreibung je Seite

Für die Browsertests muss Chrome installiert sein (anderer Pfad: `CHROME=/pfad/zu/chrome npm run test:browser`).

## Veröffentlichen

`dist/` ist mit eingecheckt. statichost.eu liest die Datei `statichost.yml` und liefert `dist/` direkt aus, ohne selbst zu bauen.

Nach Änderungen an Texten oder Code lokal `npm test` ausführen (baut auch) und `dist/` mit committen.

Die Domain steht in `wtk/config.py` unter `DOMAIN` (`https://waldtierkompass.de`).

## Suchmaschinen

- Sitemap mit Änderungsdatum (`CONTENT_UPDATED` in `wtk/config.py`, bei inhaltlichen Änderungen anpassen).
- **IndexNow:** Nach jedem Push mit geändertem `dist/` meldet `.github/workflows/indexnow.yml` die geänderten Seiten an Bing, Yandex und Co. (`tools/indexnow.mjs`). Der Schlüssel steht als `INDEXNOW_KEY` in `wtk/config.py`, die Datei `dist/<schlüssel>.txt` entsteht beim Bauen. Schlüssel nie ändern.
