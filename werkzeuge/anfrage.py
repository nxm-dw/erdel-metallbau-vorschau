#!/usr/bin/env python3
"""Konfigurator-Anfrage (Tore, Türen): das lange Forminator-Formular wird durch einen kurzen
Assistenten in drei Schritten ersetzt (Projekt, Wünsche und Fotos, Kontakt). Links zum
Hörmann-Konfigurator werden entfernt, die Seitenleiste spiegelt die drei Schritte.
Idempotent, nach einwilligung.py laufen lassen. Stil: nxm.css (.x-wiz), Logik: nxm.js."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATEN = {
    "konfiguration-tore/index.html": dict(
        art="Tore", frage="Welches Tor planen Sie?",
        wahl=[("Sektionaltor", "Öffnet senkrecht nach oben, platzsparend"),
              ("Schwingtor", "Die klassische, robuste Lösung"),
              ("Industrietor", "Für Gewerbe, Hallen und Tiefgaragen"),
              ("Noch unsicher", "Wir beraten Sie zur passenden Lösung")],
        situation=("Neubau", "Austausch des bestehenden Tors"),
        platz="z. B. Breite und Höhe, Wunschfarbe, Oberfläche, Antrieb gewünscht",
        fotos="Außen- und Innenansicht der Garage, Aufmaßblatt oder Bauplan"),
    "konfiguration-tueren/index.html": dict(
        art="Türen", frage="Welche Tür planen Sie?",
        wahl=[("Haustür", "Aluminium oder Stahl, mit Wärmedämmung"),
              ("Nebeneingangstür", "Für Garage, Keller oder Garten"),
              ("Innentür", "Stahl- und Funktionstüren im Haus"),
              ("Noch unsicher", "Wir beraten Sie zur passenden Lösung")],
        situation=("Neubau", "Austausch der bestehenden Tür"),
        platz="z. B. Höhe und Breite, Türvariante, Motiv, Sicherheitsausstattung",
        fotos="Außen- und Innenansicht der bestehenden Tür, Maße oder Pläne"),
}

I_UP = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 7 8h3v6h4V8h3l-5-5zM5 14v5a2 2 0 0 0 2 2h10'
        'a2 2 0 0 0 2-2v-5h-2v5H7v-5H5z"/></svg>')

SEITE_SCHRITTE = """<ol class="x-steps">
          <li><strong>Ihr Projekt</strong><span>Art und Situation, zwei&nbsp;Klicks.</span></li>
          <li><strong>Wünsche und Fotos</strong><span>Maße, Farbe, Unterlagen. Alles&nbsp;optional.</span></li>
          <li><strong>Kontakt</strong><span>Name, Telefon und&nbsp;E&#8209;Mail.</span></li>
        </ol>"""


def wizard(d):
    karten = "".join(
        f'<label class="x-card"><input type="radio" name="produkt" value="{n}" required>'
        f'<span class="x-card__body"><strong>{n}</strong><span>{s}</span></span></label>'
        for n, s in d["wahl"])
    neu, tausch = d["situation"]
    return f"""<form class="x-wiz" id="anfrage-form" method="post" enctype="multipart/form-data" novalidate data-nxm-wizard>
<div class="x-wiz__top"><p class="x-wiz__count" aria-live="polite" data-wiz-count>Schritt 1 von 3</p><div class="x-wiz__progress" aria-hidden="true"><span></span></div></div>
<fieldset class="x-wiz__step" data-step="1">
<legend class="x-wiz__title">{d['frage']}</legend>
<div class="x-cards" role="radiogroup" aria-label="{d['frage']}" data-group="produkt">{karten}</div>
<p class="x-wiz__label">Ihre Situation</p>
<div class="x-seg" role="radiogroup" aria-label="Ihre Situation" data-group="situation">
<label><input type="radio" name="situation" value="{neu}" required><span>{neu}</span></label>
<label><input type="radio" name="situation" value="Austausch"><span>{tausch}</span></label>
</div>
<p class="x-wiz__error" hidden>Bitte treffen Sie eine Auswahl, dann geht es weiter.</p>
<div class="x-wiz__nav"><button type="button" class="x-wiz__next" data-wiz-next>Weiter</button></div>
</fieldset>
<fieldset class="x-wiz__step" data-step="2" hidden>
<legend class="x-wiz__title">Was sollen wir wissen?</legend>
<label class="x-field x-field--area"><span class="x-field__label">Maße, Farbe, Wünsche <em>optional</em></span><textarea name="textarea-1" rows="5" placeholder="{d['platz']}"></textarea></label>
<label class="x-upload"><input type="file" name="upload-1[]" multiple accept="image/*,.pdf">{I_UP}<span class="x-upload__text"><strong>Fotos oder Unterlagen hinzufügen</strong><span>{d['fotos']}. Optional, hilft uns aber sehr.</span></span><span class="x-upload__list" data-upload-list></span></label>
<div class="x-wiz__nav"><button type="button" class="x-wiz__prev" data-wiz-prev>Zurück</button><button type="button" class="x-wiz__next" data-wiz-next>Weiter</button></div>
</fieldset>
<fieldset class="x-wiz__step" data-step="3" hidden>
<legend class="x-wiz__title">Wie erreichen wir Sie?</legend>
<p class="x-wiz__summary" data-wiz-summary hidden></p>
<div class="x-wiz__grid">
<label class="x-field"><span class="x-field__label">Name <b aria-hidden="true">*</b></span><input type="text" name="name-2" required autocomplete="name"></label>
<label class="x-field"><span class="x-field__label">Telefon <b aria-hidden="true">*</b></span><input type="tel" name="phone-1" required autocomplete="tel"></label>
<label class="x-field"><span class="x-field__label">E&#8209;Mail <b aria-hidden="true">*</b></span><input type="email" name="email-1" required autocomplete="email"></label>
<label class="x-field"><span class="x-field__label">PLZ und Ort <b aria-hidden="true">*</b></span><input type="text" name="name-6" required autocomplete="postal-code"></label>
</div>
<p class="x-wiz__error" hidden>Bitte füllen Sie die markierten Felder aus.</p>
<div class="forminator-field x-wiz__consent">
<label class="x-consent"><input type="checkbox" name="checkbox-2[]" value="Ja" required data-nxm-consent><span class="x-consent__box"></span><span class="x-consent__text">Ich habe die <a href="../datenschutzerklaerung/" target="_blank" rel="noopener">Datenschutzerklärung</a> gelesen und bin einverstanden, dass meine Angaben zur Bearbeitung meiner Anfrage und Erstellung eines Angebots verarbeitet werden. Widerruf jederzeit per E&#8209;Mail an info@erdel-metallbau.de möglich. <b aria-hidden="true">*</b></span></label>
<p class="nxm-consent__error" hidden>Bitte bestätigen Sie die Datenschutzerklärung.</p>
</div>
<div class="x-wiz__nav"><button type="button" class="x-wiz__prev" data-wiz-prev>Zurück</button><button type="submit" class="x-wiz__next">Anfrage senden</button></div>
</fieldset>
<div class="x-wiz__done" tabindex="-1" hidden><strong>Vielen Dank für Ihre&nbsp;Anfrage.</strong><p>Wir sehen uns Ihre Angaben an und melden uns bei Ihnen. Bei Fragen erreichen Sie uns unter <a href="tel:+49619563192">06195&nbsp;63192</a>.</p></div>
</form>"""


def umbauen(rel, d):
    p = os.path.join(ROOT, rel)
    t = open(p, encoding="utf-8").read()
    # Links zum Hörmann-Konfigurator raus (Kopfbereich und Karte bei den Downloads)
    t = re.sub(r'\s*<a class="nxm-btn nxm-btn--outline" href="https://www\.hoermann\.de/[^"]*"[^>]*>.*?</a>', '', t, count=1, flags=re.S)
    t = re.sub(r'\s*<a class="x-konfig" href="https://www\.hoermann\.de/[^"]*"[^>]*>.*?</a>', '', t, count=1, flags=re.S)
    t = re.sub(r'Alles direkt im Formular hochladen, auch Ihre&nbsp;Hörmann&#8209;Konfiguration\.',
               'Drei kurze Schritte: Projekt, Wünsche, Kontakt. Fotos laden Sie direkt mit&nbsp;hoch.', t)
    # Seitenleiste: die drei Schritte des Assistenten
    t = re.sub(r'<ol class="x-steps">.*?</ol>', SEITE_SCHRITTE, t, count=1, flags=re.S)
    # Formular ersetzen (Forminator oder ein früherer Assistent)
    s = t.find("<form")
    e = t.find("</form>", s) + len("</form>")
    assert s > 0 and e > s, rel
    t = t[:s] + wizard(d) + t[e:]
    assert "hoermann.de" not in t, rel
    open(p, "w", encoding="utf-8").write(t)
    print("Anfrage neu:", rel)


def kontakt_kuerzen():
    """Kontaktformular: Straße/Hausnummer und Stadt/Ort raus, Textfeld heißt „Ihre Nachricht“ (Anliegen-Chips entfernt in nxm.js)."""
    p = os.path.join(ROOT, "kontakt/index.html")
    t = open(p, encoding="utf-8").read()
    for col in ("name-2", "name-4"):
        t, n = re.subn(r'<div id="%s" class="forminator-col[^"]*"><div class="forminator-field">.*?</div></div>' % col, '', t, count=1, flags=re.S)
        assert n <= 1
    t = re.sub(r'(<label for="forminator-field-textarea-1_[^"]+" class="forminator-label">)Ihr Anliegen', r'\1Ihre Nachricht', t, count=1)
    assert 'id="name-2"' not in t and 'id="name-4"' not in t and 'id="name-3"' in t
    open(p, "w", encoding="utf-8").write(t)
    print("Kontaktformular gekürzt")


if __name__ == "__main__":
    for rel, d in DATEN.items():
        umbauen(rel, d)
    kontakt_kuerzen()
