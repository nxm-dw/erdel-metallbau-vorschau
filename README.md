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
  10b. `formulare.py` – Formulare auf `anfrage.php` umstellen, Honeypot, reCAPTCHA-Hinweis, Datenschutz-Abschnitt
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

## Formulare (ohne WordPress)
Live-Betrieb als statische Seite auf dem IONOS-Webspace (PHP 8). Alle Formulare (Kontakt, Hörmann Tore/Türen, Kurzbewerbung)
gehen über `anfrage.php` per E-Mail an **info@erdel-metallbau.de**, Anhänge (JPG/PNG/HEIC/WEBP/PDF, max. 10 Dateien / 15 MB) hängen an der Mail.
- Spamschutz: Google reCAPTCHA v3 (serverseitig geprüft, Mindestwert 0,5), Honeypot-Feld, Mindest-Ausfüllzeit 3 s, max. 5 Anfragen je IP in 10 Minuten.
- reCAPTCHA wird erst geladen, wenn die Datenschutz-Einwilligung angehakt oder abgesendet wird; Badge ausgeblendet, Pflichthinweis unter dem Knopf, Abschnitt in der Datenschutzerklärung.
- Zugangsdaten: `anfrage-config.php` (Vorlage `anfrage-config.example.php`) neben `anfrage.php` hochladen. **Nie ins Repo** (steht in `.gitignore`, Repo ist öffentlich). Websiteschlüssel steht in `werkzeuge/formulare.py`.
- Vor dem Livegang: reCAPTCHA-Admin → Domains `erdel-metallbau.de` und `www.erdel-metallbau.de` eintragen.
- **SPF:** Mails verschickt der IONOS-Server mit Absender `website@erdel-metallbau.de`. Der SPF-Eintrag erlaubt bisher nur Microsoft 365 (`-all`), sonst landen die Mails im Spam oder werden abgewiesen. TXT-Eintrag bei IONOS ändern auf:
  `v=spf1 include:spf.protection.outlook.com include:_spf-eu.ionos.com -all`
- In der Vorschau (github.io, localhost) wird nichts versendet, die Formulare zeigen nur einen Hinweis.
- Test lokal: Kopie mit `'test' => true` in der Config, `php -S 127.0.0.1:8011`, Mail landet als `nxm-anfrage-test.eml` im Temp-Ordner.

## Hinweis
Balkonfoto Altbauvilla (`balkon-altbau.jpg`) ist oberhalb der Vorhänge zugeschnitten (`CROP` in `fotos.py`); eine echte Retusche mit Vorhängen weg steht aus.

## Hinweis Livegang
Kein WordPress (Entscheidung 30.10.2026). Die Seite geht statisch auf den IONOS-Webspace, Formulare siehe oben.
`/kalkulator-job1/` und `/bewerbungsformular/` per `.htaccess` 301 auf `/jobs/#stelle-metallbauer` bzw. `/jobs/#bewerben` umleiten.
