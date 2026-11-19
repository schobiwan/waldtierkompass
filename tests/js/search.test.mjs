// Unit-Tests für Suche, Textfunktionen und Schwesterseiten (ohne Browser): node --test tests/js/
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { norm, fold, escapeHtml, nums, debounce } from "../../src/js/text.js";
import { prepare, rank, distance, suggest } from "../../src/js/search.js";
import { sisterFor } from "../../src/js/sisters.js";

const rows = JSON.parse(readFileSync(new URL("../../dist/search.json", import.meta.url), "utf8"));
const entries = rows.map(([name, key, names, alt, marks, href, kind]) => ({ name, key, href, kind, e: prepare(names, alt, marks.split("|")) }));
/** Beste Treffer wie in der Schnellsuche: Tiere vor Seiten, dann nach Rang und Name */
const search = (q) => entries.map((x) => ({ ...x, r: rank(x.e, q) })).filter((x) => x.r >= 0)
  .sort((a, b) => (a.kind ? 1 : 0) - (b.kind ? 1 : 0) || a.r - b.r || a.name.localeCompare(b.name, "de"));

test("Umlaute und Groß-/Kleinschreibung", () => {
  assert.equal(norm("Eichhörnchen"), "eichhoernchen");
  assert.equal(norm("Fuß"), "fuss");
  assert.equal(fold("Eichhörnchen"), fold("Eichhoernchen"));
  assert.equal(fold("Eichhornchen"), fold("Eichhörnchen"));
  assert.equal(fold(""), "");
  assert.equal(fold(null), "");
});

test("escapeHtml und nums", () => {
  assert.equal(escapeHtml('<a href="x">&</a>'), "&lt;a href=&quot;x&quot;&gt;&amp;&lt;/a&gt;");
  assert.deepEqual(nums("3,4,12"), [3, 4, 12]);
  assert.deepEqual(nums(""), []);
  assert.deepEqual(nums(undefined), []);
});

test("debounce führt nur den letzten Aufruf aus und lässt sich abbrechen", async () => {
  const calls = [];
  const d = debounce((v) => calls.push(v), 10);
  d(1); d(2); d(3);
  await new Promise((r) => setTimeout(r, 30));
  assert.deepEqual(calls, [3]);
  d(4); d.cancel();
  await new Promise((r) => setTimeout(r, 30));
  assert.deepEqual(calls, [3]);
});

test("Levenshtein-Abstand", () => {
  assert.equal(distance("dachs", "dachs"), 0);
  assert.equal(distance("dachs", "dachz"), 1);
  assert.equal(distance("", "abc"), 3);
  assert.equal(distance("wildscwein", "wildschwein"), 1);
});

test("Rangfolge: Name vor Doppelgänger vor Merkmal", () => {
  const e = prepare("Baummarder Martes martes Marder Edelmarder", "Steinmarder", ["Raubtiere", "Kehlfleck gelblich", "nachtaktiv"]);
  assert.equal(rank(e, "Baum"), 0);
  assert.equal(rank(e, "edelmarder"), 0);
  assert.equal(rank(e, "martes"), 0);
  assert.equal(rank(e, "Steinmarder"), 3);
  assert.equal(rank(e, "Kehlfleck"), 4);
  assert.equal(rank(e, "nachtaktiver Marder"), 5);
  assert.equal(rank(e, "Pinselohren"), -1);
  assert.equal(rank(e, ""), 0);
});

test("Schnellsuche findet typische Anfragen", () => {
  assert.equal(search("Dachs")[0].key, "dachs");
  assert.equal(search("Eichhoernchen")[0].key, "eichhoernchen");
  assert.equal(search("Pinselohren")[0].key, "luchs");
  assert.equal(search("Fuchs")[0].key, "rotfuchs");
  assert.equal(search("Keiler")[0].key, "wildschwein");
  assert.deepEqual(search("Marder").slice(0, 3).map((x) => x.key), ["baummarder", "marderhund", "steinmarder"]);
  assert.equal(search("Trittsiegel")[0].href, "spuren/");
  assert.equal(search("Brunft").find((x) => x.kind)?.href, "waldjahr/");
  assert.equal(search("November").find((x) => x.kind)?.href, "waldjahr/november/");
});

test("Tippfehler werden korrigiert", () => {
  const names = entries.map((x) => x.name);
  assert.equal(suggest("Wildscwein", names), "Wildschwein");
  assert.equal(suggest("Feuersala", names), "Feuersalamander");
  assert.equal(suggest("Eichhörnschen", names), "Eichhörnchen");
  assert.equal(suggest("xy", names), null);
  assert.equal(suggest("Giraffe", names), null);
});

test("Schwesterseiten", () => {
  assert.equal(sisterFor(fold("Buntspecht"))?.name, "Vogelkompass");
  assert.equal(sisterFor(fold("Möwe"))?.name, "Meereskompass");
  assert.equal(sisterFor(fold("Mowe"))?.name, "Meereskompass");
  assert.equal(sisterFor(fold("Buckelwal"))?.name, "Meereskompass");
  assert.equal(sisterFor(fold("Marienkäfer"))?.name, "Gartentierkompass");
  assert.equal(sisterFor(fold("Waldmaus")), null, "Waldmaus ist kein Wal");
  assert.equal(sisterFor(fold("Dachs")), null);
});
