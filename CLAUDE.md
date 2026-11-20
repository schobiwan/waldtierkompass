# Waldtierkompass – Arbeitsregeln für Claude

Website waldtierkompass.de (statisch, Python-Generator `build.py` + Paket `wtk/`). Schwesterseite von vogelkompass.de; Neuerungen dort werden auf Wunsch übernommen, wenn sie hier sinnvoll sind.

## Gemeinsame Regeln aller Kompassseiten
Gilt gleich für Vogel-, Waldtier-, Meeres- und Gartentierkompass. Dieser Abschnitt ist in allen vier Repositories identisch; Änderungen in alle vier übernehmen.

- Betreiber: Nico Schober. Antworten auf Deutsch, Anrede „Nico“.
- Kein Entwurf: Änderungen direkt umsetzen, testen und auf `main` pushen. Erst dann „live“ melden, wenn die Änderung wirklich online ist (z. B. `/version.txt` oder die geänderte Seite abrufen), nicht schon nach dem Push.
- Bei jeder Änderung Barrierefreiheit (WCAG AA, axe hell und dunkel) und PageSpeed prüfen – das muss immer sein. **PageSpeed darf sich nie verschlechtern.**
- Design nur auf ausdrücklichen Wunsch ändern. Keine neuen Einblende-Animationen beim Laden (PageSpeed wertet ausgeblendeten Inhalt als nicht sichtbar); Vogel- und Meereskompass haben keine, Wald- und Gartentierkompass blenden ihre Tierkarten noch ein.
- Nie Dateien von Nico löschen. Dateien für Nico gehen in Google Drive.
- Tonalität: Tiere beobachten und ihnen helfen, nie „anlocken“.
- Werbung: Amazon-Partner-Tag `schobiwan-21`, Werbelinks mit * gekennzeichnet. Feedback nur per E-Mail-Link an info@nicoschober.com, kein Kontaktformular. Keine Cookies, kein Tracking.
- Commit als Nico: `git -c user.name="Nico Schober" -c user.email="info@nicoschober.com" commit …`
- Veröffentlicht wird nur `dist/` (`statichost.yml`: `public: dist`), Quellcode bleibt privat.
- Strukturdaten: Nico Schober überall mit derselben Kennung `https://nicoschober.com/#person`. Über-Seite nach dem Muster „Über den …: Macher, Quellen, Finanzierung“.
- Monatlicher Neubau am 1. jedes Monats per GitHub Actions (`.github/workflows/monatlich.yml`).

### Tests (gleicher Umfang auf allen vier Seiten)
- `npm test`: Seitentest mit echtem Browser über alle Seiten, hell und dunkel: Statuscode, Titel höchstens 70 Zeichen und keiner doppelt, Beschreibung 50–160 Zeichen, genau eine h1, Bilder, JSON-LD, interne Links, Skriptfehler, axe; außerdem kein seitliches Scrollen bei 320–1280 px. Dazu die eigenen Prüfungen der Seite.
- `npm run perf`: Leistungsbudget mit Lighthouse (Handy, wie PageSpeed Insights), 5 Seitentypen, Median aus 3 Läufen. Ziel wie beim Vogelkompass: 95 Punkte, LCP 2,5 s, Speed Index 2 s, Blockierzeit 250 ms, CLS 0,01. Wo eine Seite heute darunter liegt, steht ihr aktueller Stand als Untergrenze in der Konfiguration.
- Wald-, Meeres- und Gartentierkompass nutzen dafür dieselben Dateien `tests/kompass/serve.mjs`, `seiten.mjs` und `perf.mjs` (nur `kompass.config.mjs` ist je Seite verschieden). Der Vogelkompass prüft dasselbe mit `tests/e2e.mjs` und `tests/perf.mjs`.

## Ablauf je Änderung
1. `npm ci` (einmalig), dann `npm run build`
2. `npm test` (baut, prüft Daten, Bausteine, Links, Bedienung im Browser und den gemeinsamen Seitentest; Chrome-Pfad bei Bedarf über `CHROME=…`)
3. `npm run perf` (Leistungsbudget, Seiten und Grenzen in `tests/kompass/kompass.config.mjs`). Zum Vergleich auch den Stand vor der Änderung messen, die Punkte schwanken um etwa ±3.
4. Commit als Nico, dann `git push origin main`; `dist/` wird mit eingecheckt
5. Prüfen, dass die Änderung live ist (`https://waldtierkompass.de/version.txt`)

## Nützliches
- Aufbau, Ordner und Tests: siehe `README.md`.
- Bei inhaltlichen Änderungen `CONTENT_UPDATED` in `wtk/config.py` anpassen (Autorenzeile, Sitemap).
- IndexNow meldet geänderte Seiten nach jedem Push automatisch (`.github/workflows/indexnow.yml`); den Schlüssel `INDEXNOW_KEY` nie ändern.
- Waldtierkompass deckt auch Tierspuren ab (Trittsiegel als SVG aus `art.py`).
