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
  7. `seiten.py` – neuer Inhalt für Kontakt, Jobs, Historie, Stellenseite (Texte vom Kunden)
  8. `abschluss.py` – Abschlussband auf Referenzen, Leistungen, Hörmann
  9. `paare_loesen.py` – zu lange Wortpaare lösen (nach `umbrueche.py` laufen lassen)

Prüfskripte (Playwright, im Scratchpad entwickelt): Anschnitt, zerrissene Wörter, Einzelwort-Umbrüche, Kontrast.

Kundenwunsch Hero: Bild vollflächig, Rufnummer + Menü + Logo rechts, Claim linksbündig im rechten Drittel unten (wie alte Seite).

Nach Änderungen CSS/JS-Version (`?v=`) in allen Seiten hochzählen.

## Offen (vom Kunden zu liefern)
- Stellenbeschreibung Kalkulator/Metallbauer (bisher Lorem ipsum), echte Teamfotos für Jobs
- Beide Stellen verlinken auf dieselbe Detailseite
Gelb markierte Stellen im Impressum: Funktion von Marc Erdel, Registergericht, HRB-Nummer, USt-IdNr., zuständige Handwerkskammer.

## Hinweis
Formulare senden in der Vorschau nicht ab (statische Seite, Abfang-Skript zeigt Hinweis).
