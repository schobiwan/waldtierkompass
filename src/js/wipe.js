// Datenschutz-Seite: alle lokalen Daten löschen
import "./app.js";
import { $, KEYS } from "./util.js";

$("wipe")?.addEventListener("click", () => {
  try { Object.values(KEYS).forEach((k) => localStorage.removeItem(k)); } catch {}
  document.dispatchEvent(new CustomEvent("wk:diary"));
  $("wipe-done").textContent = "Alle Daten auf diesem Gerät wurden gelöscht.";
});
