"""Formulare ohne WordPress: Versand über /anfrage.php an info@erdel-metallbau.de, Spamschutz reCAPTCHA v3.

Aufruf:  python3 werkzeuge/formulare.py
  - jedes Formular bekommt data-nxm-form (kontakt, tore, tueren, bewerbung), Honeypot und Zeitstempel
  - Forminator-Restfelder (Nonce, form_id …) fliegen raus
  - Hinweis zu Google reCAPTCHA unter dem Absende-Knopf (Badge ist per CSS ausgeblendet, Text ersetzt ihn)
  - Datenschutzerklärung: Versand per E-Mail, Abschnitt Google reCAPTCHA
reCAPTCHA wird erst geladen, wenn jemand das Datenschutz-Kästchen anhakt oder absendet (nxm.js).
Idempotent. Nach kundenrunde_3010.py laufen lassen."""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITEKEY = "6LcFYwguAAAAAGK_DEib7C3vsCw5pd0PJV_a94Z1"   # öffentlicher Websiteschlüssel, der geheime liegt nur in anfrage-config.php

FORMS = {
    "kontakt/index.html": ("forminator-module-691", "kontakt"),
    "konfiguration-tore/index.html": ("forminator-module-1224", "tore"),
    "konfiguration-tueren/index.html": ("forminator-module-1605", "tueren"),
    "jobs/index.html": ("nxm-bewerbung", "bewerbung"),
}

EXTRA = ('<input type="hidden" name="nxm_form" value="{form}"><input type="hidden" name="nxm_t" value="">'
         '<div class="nxm-hp" aria-hidden="true"><label for="f-website-{form}">Website</label>'
         '<input type="text" id="f-website-{form}" name="website" tabindex="-1" autocomplete="off"></div>')
HINWEIS = ('<p class="nxm-captcha">Spamschutz durch Google reCAPTCHA: Es gelten die '
           '<a href="https://policies.google.com/privacy?hl=de" target="_blank" rel="noopener">Datenschutzerklärung</a> und '
           '<a href="https://policies.google.com/terms?hl=de" target="_blank" rel="noopener">Nutzungs&shy;bedingungen</a> '
           'von&nbsp;Google.</p>')

DS_FORM_ALT = "Diese Daten geben wir nicht ohne Ihre Einwilligung&nbsp;weiter.</p>"
DS_FORM_NEU = ("Diese Daten geben wir nicht ohne Ihre Einwilligung&nbsp;weiter.</p>\n"
               "<p>Die Formulare dieser Website (Kontakt, Anfragen zu Toren und Türen, Kurzbewerbung) werden von unserem "
               "Webserver bei IONOS als E-Mail an info@erdel-metallbau.de übermittelt. Hochgeladene Dateien werden dabei als "
               "Anhang versendet und nicht auf dem Webserver&nbsp;gespeichert.</p>")
DS_RECAPTCHA = """<!-- nxm:recaptcha -->
<h3>Google reCAPTCHA</h3>
<p>Zum Schutz unserer Formulare vor Spam nutzen wir „Google reCAPTCHA“ (Version 3). Anbieter ist die Google Ireland Limited, Gordon House, Barrow Street, Dublin 4,&nbsp;Irland.</p>
<p>reCAPTCHA prüft, ob eine Eingabe von einem Menschen oder von einem automatisierten Programm stammt. Dazu wertet reCAPTCHA Informationen wie IP-Adresse, Verweildauer und Mausbewegungen aus und übermittelt sie an Google. Das Skript wird erst geladen, wenn Sie in einem Formular die Datenschutz-Einwilligung anhaken oder das Formular absenden; beim bloßen Besuch der Website wird keine Verbindung zu Google&nbsp;aufgebaut.</p>
<p>Die Verarbeitung erfolgt auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO. Wir haben ein berechtigtes Interesse daran, unsere Formulare vor missbräuchlicher automatisierter Nutzung und Spam zu schützen. Die Datenübertragung in die USA wird auf das EU-US Data Privacy Framework (DPF) gestützt. Weitere Informationen finden Sie in der <a href="https://policies.google.com/privacy?hl=de" target="_blank" rel="noopener">Datenschutzerklärung von Google</a> und in den <a href="https://policies.google.com/terms?hl=de" target="_blank" rel="noopener">Nutzungsbedingungen</a>.</p>
<!-- /nxm:recaptcha -->
"""

RESTE = re.compile(r'<input type="hidden" (?:id="forminator_nonce" )?name="(?:forminator_nonce|_wp_http_referer|form_id|page_id|'
                   r'form_type|current_url|render_id|action)"[^>]*>')


def edit(rel, fn):
    p = os.path.join(ROOT, rel)
    s = open(p, encoding="utf-8").read()
    n = fn(s)
    if n != s:
        open(p, "w", encoding="utf-8").write(n)
        print("geändert:", rel)


def formular(form_id, form):
    def fn(s):
        m = re.search(r'<form\b[^>]*\bid="%s"[^>]*>' % re.escape(form_id), s)
        if not m:
            raise SystemExit(f"Formular {form_id} nicht gefunden")
        tag = m.group(0)
        if "data-nxm-form" not in tag:
            neu = tag[:-1] + f' data-nxm-form="{form}" data-sitekey="{SITEKEY}" action="/anfrage.php">'
            neu = re.sub(r'\saction="(?!/anfrage)[^"]*"', "", neu)
            s = s[:m.start()] + neu + s[m.end():]
        ende = s.index("</form>", m.start())
        teil = s[m.start():ende]
        teil = RESTE.sub("", teil)
        if 'name="nxm_form"' not in teil:
            teil += EXTRA.format(form=form)
        if "nxm-captcha" not in teil:
            teil = re.sub(r'(<button class="forminator-button forminator-button-submit"[^>]*>.*?</button>)', r"\1" + HINWEIS, teil, count=1, flags=re.S)
        return s[:m.start()] + teil + s[ende:]
    return fn


for rel, (fid, form) in FORMS.items():
    edit(rel, formular(fid, form))


def datenschutz(s):
    if "Webserver bei IONOS als E-Mail" not in s:
        s = s.replace(DS_FORM_ALT, DS_FORM_NEU, 1)
    if "nxm:recaptcha" not in s:
        i = s.index("<h3>Schriftarten (lokal&nbsp;eingebunden)</h3>")
        s = s[:i] + DS_RECAPTCHA + s[i:]
    return s


edit("datenschutzerklaerung/index.html", datenschutz)
