# erdel metallbau – Vorschau Relaunch

Statische Kopie der WordPress-Relaunch-Seite (relaunch.erdel-metallbau.de) mit Feinschliff von NEXAS Media.
Vorschau: https://nxm-dw.github.io/erdel-metallbau-vorschau/

## Aufbau
- `nxm/nxm.css`, `nxm/nxm.js` – neues Design (Kopf, Vollbild-Menü, mobile Aktionsleiste, Fuß, Formulare, Karten)
- `nxm/fonts/` – Manrope, lokal eingebunden (keine Verbindung zu Google)
- `werkzeuge/` – Umbau-Skripte in dieser Reihenfolge (alle idempotent):
  1. `optimieren.py` – Kopf, Menü, Fuß, Aktionsleiste, Teaser, Alt-Texte
  2. `rechtliches.py` – Impressum (§ 5 DDG), Datenschutz-Ergänzungen
  3. `feinschliff_text.py` – Textkorrekturen, Trennhilfen
  4. `umbrueche.py` – letzte zwei Wörter zusammenhalten
  5. `saubere_links.py` – Links ohne `index.html`

Nach Änderungen CSS/JS-Version (`?v=`) in allen Seiten hochzählen.

## Offen (vom Kunden zu liefern)
Gelb markierte Stellen im Impressum: Funktion von Marc Erdel, Registergericht, HRB-Nummer, USt-IdNr., zuständige Handwerkskammer.

## Hinweis
Formulare senden in der Vorschau nicht ab (statische Seite, Abfang-Skript zeigt Hinweis).
