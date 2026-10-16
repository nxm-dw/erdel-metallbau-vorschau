# erdel metallbau – Vorschau Relaunch

Statische Kopie der WordPress-Relaunch-Seite (relaunch.erdel-metallbau.de) mit Feinschliff von NEXAS Media.
Vorschau: https://nxm-dw.github.io/erdel-metallbau-vorschau/

## Aufbau
- `nxm/nxm.css`, `nxm/nxm.js` – neues Design (Kopf, Vollbild-Menü, mobile Aktionsleiste, Fuß, Formulare, Karten)
- `nxm/fonts/` – Oxygen (Schrift aus dem freigegebenen Entwurf 2022), lokal eingebunden
- `nxm/img/` – echte Projektfotos aus dem Kundenarchiv (NAS: _Archiviert/_Kunden/Erdel Metallbau GmbH/03_Bildarchiv), auf 2000 px verkleinert
- `werkzeuge/` – Umbau-Skripte in dieser Reihenfolge (alle idempotent):
  1. `optimieren.py` – Kopf, Menü, Fuß, Aktionsleiste, Teaser, Alt-Texte
  2. `rechtliches.py` – Impressum (§ 5 DDG), Datenschutz-Ergänzungen
  3. `feinschliff_text.py` – Textkorrekturen, Trennhilfen
  4. `umbrueche.py` – letzte zwei Wörter zusammenhalten
  5. `saubere_links.py` – Links ohne `index.html`
  6. `bilder.py` – Stockfotos durch Archivfotos ersetzen, Teaser „+ mehr“

Kundenwunsch Hero: Bild vollflächig, Rufnummer + Menü + Logo rechts, Claim linksbündig im rechten Drittel unten (wie alte Seite).

Nach Änderungen CSS/JS-Version (`?v=`) in allen Seiten hochzählen.

## Offen (vom Kunden zu liefern)
Gelb markierte Stellen im Impressum: Funktion von Marc Erdel, Registergericht, HRB-Nummer, USt-IdNr., zuständige Handwerkskammer.

## Hinweis
Formulare senden in der Vorschau nicht ab (statische Seite, Abfang-Skript zeigt Hinweis).
