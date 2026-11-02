# Waldtierkompass

Statische Website zum Bestimmen von Waldtieren in Deutschland. Schwesterseite zum [Vogelkompass](https://vogelkompass.de/).

33 Arten mit Fotos, Trittsiegeln, Doppelgängern, Waldjahr, Quiz und einem Tagebuch, das nur im Browser gespeichert wird.

## Ordner

| Pfad | Inhalt |
|---|---|
| `data.py` | Alle Texte: Arten, Doppelgänger, Ereignisse im Waldjahr |
| `credits.json` | Urheber, Lizenz und Quelle jedes Fotos (Wikimedia Commons) |
| `build.py` | Erzeugt alle HTML-Seiten in `dist/` |
| `art.py` | Zeichnet die Trittsiegel als SVG |
| `src/css/` | Stylesheet (`base.css` = Grundgerüst, `extra.css` = Ergänzungen) |
| `src/js/` | Skripte für Suche und Filter, Tagebuch, Quiz |
| `photos/` | Tierfotos als WebP (720 px und 400 px breit) |
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

## Veröffentlichen

`dist/` ist mit eingecheckt. statichost.eu liest die Datei `statichost.yml` und liefert `dist/` direkt aus, ohne selbst zu bauen.

Nach Änderungen an Texten oder Code lokal `npm run build` ausführen und `dist/` mit committen.

Vor dem Livegang anpassen:

- `DOMAIN` in `build.py` (derzeit `https://waldtierkompass.de`)
- Hosting-Anbieter in der Datenschutzerklärung (in `build.py`, Funktion `build_legal`, als Platzhalter markiert)
