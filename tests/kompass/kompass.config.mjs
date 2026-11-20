// Einstellungen für den gemeinsamen Test der Kompassseiten (serve.mjs, seiten.mjs und perf.mjs sind in allen Repositories gleich).
// Leistungsbudget: Ziel sind die Grenzen des Vogelkompass (95 Punkte, LCP 2,5 s, Speed Index 2 s, Blockierzeit 250 ms, CLS 0,01).
// kb = Datenmenge höchstens, rund 10 % über dem Stand vom 20.11.2026 (Median, gzip wie bei statichost).
// Startseite und Vergleich liegen noch unter dem Ziel: dort gilt vorerst der heutige Stand (score, lcp), er darf nicht schlechter werden.
export default {
  dist: '../../dist',
  perf: [
    // Startseite: Chrome lädt manchmal die Fotos weiter unten schon vor (gemessen 641 oder rund 960 KB), das Budget deckt beide Fälle ab
    { path: '', name: 'Startseite', kb: 1060, score: 89, lcp: 3300 },
    { path: 'arten/dachs/', name: 'Artseite', kb: 320 },
    { path: 'unterscheiden/baummarder-oder-steinmarder/', name: 'Vergleich', kb: 440, score: 91, lcp: 3300 },
    { path: 'waldjahr/november/', name: 'Waldjahr', kb: 650 },
    { path: 'spuren/', name: 'Spuren', kb: 100 },
  ],
};
