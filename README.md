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
  9. `einwilligung.py` – Datenschutz-Pflichtfeld in allen Formularen (nach `seiten.py`)
  10. `paare_loesen.py` – zu lange Wortpaare lösen (nach `umbrueche.py` laufen lassen)
  11. `anfrage.py` – Konfigurator-Anfrage Tore/Türen als kurzer Assistent in drei Schritten (Projekt, Wünsche und Fotos, Kontakt), Hörmann-Konfigurator-Links raus, Kontaktformular ohne Straße/Ort und ohne Anliegen-Chips (nach `einwilligung.py`)

Prüfskripte (Playwright, im Scratchpad entwickelt): Anschnitt, zerrissene Wörter, Einzelwort-Umbrüche, Kontrast.

Kundenwunsch Hero: Bild vollflächig, Rufnummer + Menü + Logo rechts, Claim linksbündig im rechten Drittel unten (wie alte Seite).

Nach Änderungen CSS/JS-Version (`?v=`) in allen Seiten hochzählen.

## Offen (vom Kunden zu liefern)
- Kundenfotos vom 21.10.2026 (18 Stück aus dem OneDrive-Ordner „erdel Metallbau“) sind in `nxm/img/` importiert (max. 1800 px, `bilder.py` Abschnitt SWAP2/GALERIE_NEU): Leistungen-Karten Briefkästen (`briefkasten-gold.jpg`, ersetzt Stele 43 b), Treppen & Geländer (`treppe-eiche-glas.jpg`), Weitere Metallbauarbeiten (`villa-balkon.jpg`), Möbelbau (`moebel-schreibtisch.jpg`); alle 18 zusätzlich vorn in der Referenzen-Galerie (jetzt 36 Kacheln, einheitlich 7:8 per CSS). Weitere 22 Fotos liegen noch unverwendet im OneDrive-Ordner.
- Hörmann: alle Bilder der Seite tauschen (Kopfbild Garage mit Sektionaltor und die weiteren Fotos), neue Bilder folgen vom Kunden (Stand 21.10.2026)
- Jobs: Stellenliste mit Direktbewerbung, Bewerbungsformular liegt jetzt auch auf der Jobs-Seite (`#bewerbung`), „Jetzt bewerben“ an einer Stelle trägt die Stelle oben ins Formular und in die Nachricht ein (`?stelle=` funktioniert auch auf der Bewerbungsseite). Echte Teamfotos und Stellentexte weiterhin vom Kunden
- Stellenbeschreibung Kalkulator/Metallbauer (bisher Lorem ipsum), echte Teamfotos für Jobs
- Beide Stellen verlinken auf dieselbe Detailseite
Gelb markierte Stellen im Impressum: Funktion von Marc Erdel, Registergericht, HRB-Nummer, USt-IdNr., zuständige Handwerkskammer.

## Hinweis
Formulare senden in der Vorschau nicht ab (statische Seite, Abfang-Skript zeigt Hinweis).

## Hinweis Livegang (WordPress/Forminator)
Konfigurator-Anfrage (Tore, Türen) ist in der Vorschau ein eigener dreistufiger Assistent (`.x-wiz`, Logik in `nxm.js`). Beim Livegang in Forminator mit Seitenumbrüchen nachbauen: Schritt 1 Produkt (Radio: Sektionaltor/Schwingtor/Industrietor/Noch unsicher bzw. Haustür/Nebeneingangstür/Innentür/Noch unsicher) + Situation (Neubau/Austausch), Schritt 2 Nachricht `textarea-1` + Upload `upload-1` (mehrere Dateien), Schritt 3 Name `name-2`, Telefon `phone-1`, E-Mail `email-1`, PLZ und Ort `name-6`, Datenschutz `checkbox-2`. Kontaktformular 691: Felder Straße/Hausnummer (`name-2`) und Stadt/Ort (`name-4`) auch in Forminator entfernen. Bewerbungsformular wird auf Jobs-Seite und Bewerbungsseite eingebunden (gleicher Forminator-Shortcode).
Das Datenschutz-Kästchen im Kontaktformular ist ein eigenes Feld (`name="datenschutz"`). Beim Livegang in Forminator als echtes GDPR-/Checkbox-Pflichtfeld anlegen, damit es auch serverseitig geprüft wird.
