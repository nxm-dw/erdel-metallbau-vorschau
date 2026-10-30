# erdel metallbau – Vorschau Relaunch

Statische Kopie der WordPress-Relaunch-Seite (relaunch.erdel-metallbau.de) mit Feinschliff von NEXAS Media.
Vorschau: https://nxm-dw.github.io/erdel-metallbau-vorschau/

## Aufbau
- `nxm/nxm.css`, `nxm/nxm.js` – neues Design (Kopf, Vollbild-Menü, mobile Aktionsleiste, Fuß, Formulare, Karten)
- `nxm/fonts/` – Oxygen (Schrift aus dem freigegebenen Entwurf 2022), lokal eingebunden
- `nxm/img/` – echte Projektfotos aus dem Kundenarchiv (NAS: _Archiviert/_Kunden/Erdel Metallbau GmbH/03_Bildarchiv) und neue Kundenfotos (OneDrive „erdel Metallbau“, Okt. 2026), auf 2000 px verkleinert, ohne Metadaten; `nxm/img/galerie/` = Ausschnitte 700×800 für die Referenzen-Galerie
- `werkzeuge/` – Umbau-Skripte in dieser Reihenfolge (alle idempotent):
  1. `optimieren.py` – Kopf, Menü, Fuß, Aktionsleiste, Teaser, Alt-Texte
  2. `rechtliches.py` – Impressum (§ 5 DDG), Datenschutz-Ergänzungen
  3. `feinschliff_text.py` – Textkorrekturen, Trennhilfen
  4. `umbrueche.py` – letzte zwei Wörter zusammenhalten
  5. `saubere_links.py` – Links ohne `index.html`
  6. `bilder.py` – Stockfotos durch Archivfotos ersetzen, Teaser „+ mehr“
  6a. `fotos.py "<Ordner mit Originalfotos>"` – neue Kundenfotos übernehmen; Hausnummern, Namens-/Klingelschilder, Kennzeichen und Personen weichzeichnen (auch in Galerie und Archivfotos)
  6b. `bilder_neu.py` – restliche Stockfotos seitenweit ersetzen, Referenzen-Galerie um 20 neue Projekte erweitern
  7. `seiten.py` – neuer Inhalt für Kontakt, Jobs (Karriere mit Beispielstellen + Kurzbewerbung), Historie, Hörmann-Konfiguratoren; schlanke Formulare; Stellenseite und Bewerbungsformular leiten auf `jobs/` weiter
  8. `abschluss.py` – Abschlussband auf Referenzen, Leistungen, Hörmann
  9. `einwilligung.py` – Datenschutz-Pflichtfeld in allen Formularen (nach `seiten.py`)
  10. `paare_loesen.py` – zu lange Wortpaare lösen (nach `umbrueche.py` laufen lassen)
  10a. `kundenrunde_3010.py` – Kundenrunde 30.10.2026: weniger „Unikat“/„keine Grenzen“, Geschäftszeiten ab 7:00, Qualitätsleiste Startseite (seit 1925, Meisterbetrieb, TÜV, DIN EN 1090, 3D-Werkplanung), Kontakt-Leiste rechts (Desktop), alle Formulare im Vorschau-Modus ohne Aufruf an relaunch.erdel-metallbau.de
  11. `kopfbilder.py` – Kopfbild je Seite festlegen, bricht bei Doppelungen ab (immer als letzter Schritt)

Prüfskripte (Playwright, lokaler Server z. B. `python3 -m http.server 8010`):
- `werkzeuge/pruefen.py [URL] [Seite …]` – Überlauf, angeschnittene Texte, einzelne Wörter in der letzten Zeile, JS-Fehler, 404 (6 Breiten)
- `werkzeuge/kontrast.py [URL]` – Lesbarkeit weißer Schrift auf Fotos (WCAG)
Bekannte Ausnahme: drei lange Fachwort-Überschriften in der Datenschutzerklärung bei 360 px.

Kundenwunsch Hero: Bild vollflächig, Rufnummer + Menü + Logo rechts, Claim linksbündig im rechten Drittel unten (wie alte Seite).

Nach Änderungen CSS/JS-Version (`?v=`) in allen Seiten hochzählen.

## Offen (vom Kunden zu liefern)
- Karriere: vier Beispielstellen (Metallbauer:in, Kalkulation/Projektleitung, Monteur:in Tore/Türen, Ausbildung) – Texte, Konditionen und welche Stellen wirklich offen sind, bestätigen lassen (gelb markiert)
- Fotos von Team, Werkstatt und Fahrzeugen fehlen noch; Partnerbild Ferschke stammt vom Partner
Gelb markierte Stellen im Impressum: Funktion von Marc Erdel, Registergericht, HRB-Nummer, USt-IdNr., zuständige Handwerkskammer.

## Hinweis
Formulare senden in der Vorschau nicht ab (statische Seite, Abfang-Skript zeigt Hinweis; es geht auch nichts an das alte WordPress).
Balkonfoto Altbauvilla (`balkon-altbau.jpg`) ist oberhalb der Vorhänge zugeschnitten (`CROP` in `fotos.py`); eine echte Retusche mit Vorhängen weg steht aus.

## Hinweis Livegang (WordPress/Forminator)
Empfänger aller Formular-Benachrichtigungen (Kontakt, Hörmann Tore/Türen, Kurzbewerbung): **info@erdel-metallbau.de** (Kundenwunsch 30.10.2026).
Die Formulare sind in der Vorschau schlank neu aufgebaut. Beim Livegang in Forminator genauso anlegen
(Datenschutz-Kästchen `name="datenschutz"` jeweils als echtes GDPR-/Checkbox-Pflichtfeld):
- Kontakt (Formular 691): Name*, E-Mail*, Telefon, Anliegen (Themen-Chips setzen nur eine Zeile ins Textfeld), Datenschutz*
- Hörmann Tore/Türen: Name*, Telefon*, E-Mail*, PLZ und Ort*, Wünsche (Textfeld), Datei-Upload mehrfach (JPG/PNG/HEIC/PDF), Datenschutz*
  (entfallen: Produktauswahl, Firma/Privat, Vor-/Nachname getrennt, Straße, Hausnummer, Pflichtfelder Farbe/Sektionen/Oberfläche, drei Einzel-Uploads)
- Kurzbewerbung auf `jobs/` (ersetzt Formular 700): Name*, Telefon*, E-Mail, Stelle (Auswahl), Lebenslauf-Upload mehrfach, Datenschutz*
Danach `/kalkulator-job1/` und `/bewerbungsformular/` in WordPress per 301 auf `/jobs/#stelle-metallbauer` bzw. `/jobs/#bewerben` umleiten.
