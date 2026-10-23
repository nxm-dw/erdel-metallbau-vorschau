"""Neuer Inhaltsbereich für Kontakt, Jobs, Historie und die Stellenseite.
Ersetzt jeweils den Bereich zwischen <div class="main-body"> und <footer class="main-footer">.
Texte stammen von den bestehenden Seiten des Kunden; das Kontaktformular (Forminator) wird übernommen.
Idempotent über den Marker nxm:seite."""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEL, TEL_TXT, MAIL = "+49619563192", "06195 63192", "info@erdel-metallbau.de"
WA = "https://wa.me/49619563192"
MAPS = "https://www.google.com/maps/search/?api=1&query=Auf+der+Herrnmauer+12,+65779+Kelkheim+im+Taunus"
P = "../"
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.2 5.3 19.9 12l-6.7 6.7-1.4-1.4 4.3-4.3H4v-2h12.1l-4.3-4.3z"/></svg>'
I_TEL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>'
I_MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18c.6 0 1 .4 1 1v12c0 .6-.4 1-1 1H3a1 1 0 0 1-1-1V6c0-.6.4-1 1-1zm9 7.3L4 7.2V17h16V7.2l-8 5.1zM5.2 7l6.8 4.3L18.8 7H5.2z"/></svg>'
I_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2c0 1.3.9 2.5 1 2.7.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'
I_PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 1 7 7c0 5.2-7 13-7 13S5 14.2 5 9a7 7 0 0 1 7-7zm0 4.5A2.5 2.5 0 1 0 12 11.5 2.5 2.5 0 0 0 12 6.5z"/></svg>'

HOURS = """<div class="x-hours" data-nxm-open>
  <p class="x-status"><span class="x-dot"></span><span class="x-status__text">Geschäftszeiten</span></p>
  <dl>
    <div data-days="1,2,3,4"><dt>Montag bis Donnerstag</dt><dd>8:00 – 16:30 Uhr</dd></div>
    <div data-days="5"><dt>Freitag</dt><dd>8:00 – 13:00 Uhr</dd></div>
    <div data-days="0,6"><dt>Samstag und Sonntag</dt><dd>geschlossen</dd></div>
  </dl>
</div>"""


# --- Schlanke Formulare -------------------------------------------------------------------------
# Wunsch Okt. 2026: Kontakt- und Hörmann-Formulare deutlich kürzer. Die Formulare werden hier
# neu aufgebaut (Forminator-Klassen für das Aussehen, Form-Kopf und versteckte Felder bleiben).
# Zum Livegang die Felder in Forminator genauso anlegen (siehe README).

def _f(fid, label, inp, req=False, full=False, hint=""):
    star = ' <span class="forminator-required">*</span>' if req else ' <span class="x-opt">(optional)</span>'
    cls = "forminator-col forminator-col-12 x-full" if full else "forminator-col forminator-col-6"
    h = f'<span class="forminator-description x-hint">{hint}</span>' if hint else ""
    return (f'<div id="{fid}" class="{cls}"><div class="forminator-field">'
            f'<label for="f-{fid}" class="forminator-label">{label}{star}</label>{inp}{h}</div></div>')


def _in(fid, typ="text", req=False, ac=""):
    r = ' required aria-required="true"' if req else ""
    a = f' autocomplete="{ac}"' if ac else ""
    return f'<input type="{typ}" name="{fid}" id="f-{fid}" class="forminator-input"{a}{r} />'


def _upload(fid, label, hint):
    return (f'<div id="{fid}" class="forminator-col forminator-col-12 x-full"><div class="forminator-field">'
            f'<span class="forminator-label" id="l-{fid}">{label} <span class="x-opt">(optional)</span></span>'
            f'<div class="x-upload"><input type="file" name="{fid}[]" id="f-{fid}" class="x-upload__input" multiple '
            f'accept=".jpg,.jpeg,.png,.heic,.webp,.pdf" aria-labelledby="l-{fid}">'
            f'<label for="f-{fid}" class="x-upload__btn">Dateien auswählen</label>'
            f'<span class="x-upload__name" aria-live="polite">{hint}</span></div></div></div>')


CONSENT = ('<div class="forminator-row nxm-consent-row"><div id="nxm-consent" class="forminator-col forminator-col-12 x-full"><div class="forminator-field">'
           '<label class="forminator-checkbox nxm-consent"><input type="checkbox" name="datenschutz" value="Ja" required data-nxm-consent>'
           '<span class="forminator-checkbox-box" aria-hidden="true"></span><span class="forminator-checkbox-label">Ich habe die '
           f'<a href="{P}datenschutzerklaerung/" target="_blank" rel="noopener">Datenschutzerklärung</a> gelesen und bin einverstanden, '
           '{zweck} Widerruf jederzeit per E-Mail an <span class="nxm-nowrap">info@erdel-metallbau.de</span> möglich.&nbsp;<span class="forminator-required">*</span></span></label>'
           '<p class="nxm-consent__error" role="alert" hidden>Bitte bestätigen Sie die Datenschutzerklärung, damit wir Ihre Anfrage bearbeiten&nbsp;dürfen.</p></div></div></div>')


def _rebuild(t, rows, button, zweck="dass meine Angaben zur Bearbeitung meiner Anfrage verarbeitet werden."):
    """Formular der Seite neu aufbauen: Kopf und versteckte Forminator-Felder bleiben, Felder werden ersetzt."""
    s = t.find("<form"); e = t.find("</form>") + len("</form>")
    form = t[s:e]
    head = form[:form.find(">", form.find("data-uid")) + 1]
    if "x-slim" not in head:
        head = head.replace('class="forminator-ui ', 'class="forminator-ui x-slim ', 1)
    if 'enctype' not in head:
        head = head.replace('method="post"', 'method="post"\n\t\t\t\tenctype="multipart/form-data"', 1)
    hidden = "".join(m for m in re.findall(r'<input type="hidden"[^>]*>', form) if 'referer_url' not in m)
    body = ('<div class="forminator-response-message forminator-error" aria-hidden="true"></div>'
            + "".join(f'<div class="forminator-row">{r}</div>' for r in rows)
            + CONSENT.replace("{zweck}", zweck)
            + f'<div class="forminator-row forminator-row-last"><div class="forminator-col x-full"><div class="forminator-field">'
              f'<button class="forminator-button forminator-button-submit">{button}</button></div></div></div>')
    return head + body + hidden + "</form>"


def kontakt_form(t):
    return _rebuild(t, [
        _f("name-1", "Name", _in("name-1", req=True, ac="name"), req=True) + _f("email-1", "E-Mail", _in("email-1", "email", True, "email"), req=True),
        _f("phone-1", "Telefon", _in("phone-1", "tel", ac="tel"), full=True, hint="Für einen kurzen Rückruf, wenn Sie das&nbsp;möchten."),
        _f("textarea-1", "Ihr Anliegen", '<textarea name="textarea-1" id="f-textarea-1" class="forminator-textarea" rows="5" maxlength="1500"></textarea>', full=True),
    ], "Nachricht senden")


def konfig_form(t, art):
    was = "Tor" if art == "Tore" else "Tür"
    return _rebuild(t, [
        _f("name-1", "Name", _in("name-1", req=True, ac="name"), req=True) + _f("phone-1", "Telefon", _in("phone-1", "tel", True, "tel"), req=True),
        _f("email-1", "E-Mail", _in("email-1", "email", True, "email"), req=True) + _f("name-5", "PLZ und Ort", _in("name-5", req=True, ac="postal-code"), req=True),
        _f("textarea-1", f"Ihre Wünsche zum {was}",
           f'<textarea name="textarea-1" id="f-textarea-1" class="forminator-textarea" rows="4" maxlength="1500" placeholder="z.&nbsp;B. Maße, Farbe, Oberfläche oder&nbsp;Antrieb"></textarea>', full=True),
        _upload("upload-1", "Fotos, Aufmaßblatt oder Konfiguration", "Mehrere Dateien möglich: JPG, PNG oder&nbsp;PDF"),
    ], "Anfrage senden")


def kontakt(t):
    form = kontakt_form(t)
    return f"""
<section class="x-section x-intro">
  <div class="x-wrap x-split">
    <div>
      <p class="x-eyebrow">Kontakt</p>
      <h2 class="x-display">Haben Sie Fragen oder möchten Sie über individuelle Konstruktionen&nbsp;sprechen?</h2>
      <p class="x-lead">Wir sind gerne für Sie da. Rufen Sie an, schreiben Sie uns oder schicken Sie Ihre Anfrage direkt über das&nbsp;Formular.</p>
    </div>
    {HOURS}
  </div>
</section>

<section class="x-section x-section--tight">
  <div class="x-wrap">
    <div class="x-tiles">
      <a class="x-tile x-tile--dark" href="tel:{TEL}">{I_TEL}<span class="x-tile__label">Telefon</span><span class="x-tile__value">{TEL_TXT}</span><span class="x-tile__cta">Jetzt anrufen {ARROW}</span></a>
      <a class="x-tile" href="mailto:{MAIL}">{I_MAIL}<span class="x-tile__label">E-Mail</span><span class="x-tile__value x-tile__value--sm">{MAIL}</span><span class="x-tile__cta">E-Mail schreiben {ARROW}</span></a>
      <a class="x-tile" href="{WA}" target="_blank" rel="noopener">{I_WA}<span class="x-tile__label">WhatsApp</span><span class="x-tile__value">Kurz&nbsp;schreiben</span><span class="x-tile__cta">Chat öffnen {ARROW}</span></a>
      <a class="x-tile" href="{MAPS}" target="_blank" rel="noopener">{I_PIN}<span class="x-tile__label">Werkstatt</span><span class="x-tile__value x-tile__value--sm">Auf der Herrnmauer 12<br>65779 Kelkheim im&nbsp;Taunus</span><span class="x-tile__cta">Route planen {ARROW}</span></a>
    </div>
  </div>
</section>

<section class="x-section x-formsec" id="anfrage">
  <div class="x-wrap x-formgrid">
    <aside class="x-formside">
      <img src="{P}nxm/img/haus-giebel.jpg" alt="Wohnhaus mit Metallarbeiten von erdel metallbau" loading="lazy">
      <div class="x-formside__body">
        <p class="x-eyebrow x-eyebrow--light">Projekt anfragen</p>
        <h2>So einfach&nbsp;geht's</h2>
        <ol class="x-steps">
          <li><strong>Anfrage senden</strong><span>Beschreiben Sie kurz Ihr Vorhaben, gerne mit Fotos oder&nbsp;Maßen.</span></li>
          <li><strong>Termin vor Ort</strong><span>Wir nehmen die genauen Aufmaße und beraten Sie&nbsp;persönlich.</span></li>
          <li><strong>Ihr Angebot</strong><span>Sie erhalten ein individuelles Angebot für Ihr&nbsp;Unikat.</span></li>
        </ol>
        <p class="x-formside__hint">Hörmann-Tor oder -Tür geplant? Nutzen Sie direkt unsere Konfiguratoren für <a href="{P}konfiguration-tore/">Tore</a> und <a href="{P}konfiguration-tueren/">Türen</a>.</p>
      </div>
    </aside>
    <div class="x-formcard">
      <div class="x-formcard__head"><h2>Ihre Nachricht an&nbsp;uns</h2><p class="x-formcard__req"><span aria-hidden="true">*</span> Pflichtfeld</p></div>
      {form}
    </div>
  </div>
</section>

<section class="x-section">
  <div class="x-wrap">
    <p class="x-eyebrow">Netzwerk</p>
    <h2 class="x-h2">Unsere zuverlässigen&nbsp;Partner</h2>
    <div class="x-partners">
      <a class="x-partner" href="{P}hoermann/">
        <img src="{P}nxm/img/garagentor-verkleidet-2.jpg" alt="Hörmann-Garagentor" loading="lazy">
        <span class="x-partner__body"><span class="x-partner__name">HÖRMANN Tore &amp;&nbsp;Türen</span><span class="x-partner__cta">Mehr erfahren {ARROW}</span></span>
      </a>
      <a class="x-partner" href="https://www.galabau-ferschke.de/" target="_blank" rel="noopener">
        <img src="{P}wp-content/uploads/2022/10/PartnerFerschke.jpg" alt="Gartengestaltung J. &amp; W. Ferschke" loading="lazy">
        <span class="x-partner__body"><span class="x-partner__name">Gartengestaltung J. &amp; W.&nbsp;Ferschke</span><span class="x-partner__cta">Zur Website {ARROW}</span></span>
      </a>
    </div>
  </div>
</section>
"""


# --- Karriere (Neugestaltung Okt. 2026) -------------------------------------------------------
# Beispielstellen (vom Kunden noch abzustimmen), alles auf einer Seite: Stelle aufklappen,
# „Auf diese Stelle bewerben“ springt direkt zur Kurzbewerbung unten. Kein Seitenwechsel.

STELLEN = [
    dict(id="metallbauer", kurz="Metallbauer:in", titel="Metallbauer:in Konstruktions&shy;technik&nbsp;(m/w/d)", tags=["Vollzeit", "ab sofort", "Werkstatt &amp; Montage"],
         teaser="Du fertigst Treppen, Geländer und Tore in unserer Werkstatt und baust sie beim Kunden&nbsp;ein.",
         aufgaben=["Fertigung von Treppen, Geländern, Toren und Zäunen nach&nbsp;Zeichnung", "Schweißen und Bearbeiten von Stahl, Edelstahl und&nbsp;Aluminium", "Montage bei unseren Kunden im Rhein-Main-Gebiet", "Pflege von Werkzeug und&nbsp;Maschinen"],
         profil=["Ausbildung als Metallbauer:in oder&nbsp;Schlosser:in", "Erfahrung im Schweißen (MAG/WIG)", "Führerschein Klasse&nbsp;B", "Sorgfalt und Freude an schönen&nbsp;Details"]),
    dict(id="kalkulator", kurz="Kalkulation und Projektleitung", titel="Kalkulator:in und Projekt&shy;leitung Metallbau&nbsp;(m/w/d)", tags=["Vollzeit", "ab sofort", "Büro &amp; Baustelle"],
         teaser="Du berätst Bauherren, nimmst Maß und begleitest Projekte vom Angebot bis zur&nbsp;Montage.",
         aufgaben=["Technische Beratung unter Berücksichtigung bautechnischer&nbsp;Anforderungen", "Aufmaß vor Ort und Abstimmung mit&nbsp;Architekten", "Kalkulation und Erstellung von&nbsp;Angeboten", "Planung und Begleitung bis zur&nbsp;Abnahme"],
         profil=["Meister:in oder Techniker:in im Metallbau, alternativ&nbsp;Berufserfahrung", "Sicherer Umgang mit Zeichnungen, CAD von&nbsp;Vorteil", "Freude am Kontakt mit&nbsp;Kunden", "Strukturierte, selbstständige&nbsp;Arbeitsweise"]),
    dict(id="monteur", kurz="Monteur:in Tore und Türen", titel="Monteur:in für Tore und Türen&nbsp;(m/w/d)", tags=["Vollzeit", "ab sofort", "Montage"],
         teaser="Du montierst Hörmann-Garagentore, Haustüren und Antriebe und bist beim Kunden das Gesicht von&nbsp;erdel.",
         aufgaben=["Montage von Garagentoren, Haustüren und&nbsp;Antrieben", "Wartung und Reparatur bei unseren&nbsp;Kunden", "Inbetriebnahme und Einweisung vor&nbsp;Ort", "Aufmaß für Folgeaufträge"],
         profil=["Handwerkliche Ausbildung, z.&nbsp;B. Metallbau, Tischlerei oder&nbsp;Elektro", "Führerschein Klasse&nbsp;B", "Zuverlässigkeit und freundliches&nbsp;Auftreten", "Lust, Neues zu&nbsp;lernen"]),
    dict(id="ausbildung", kurz="Ausbildung Metallbauer:in", titel="Ausbildung Metallbauer:in&nbsp;(m/w/d)", tags=["Ausbildung", "Start 1.&nbsp;August 2027", "3,5&nbsp;Jahre"],
         teaser="Du lernst das Handwerk von Grund auf: vom ersten Schweißpunkt bis zur fertigen&nbsp;Treppe.",
         aufgaben=["Schweißen, Biegen, Bohren und&nbsp;Montieren", "Technische Zeichnungen lesen und&nbsp;umsetzen", "Mitarbeit an echten Kundenprojekten", "Mit auf Montage im Team"],
         profil=["Haupt- oder Realschulabschluss", "Spaß an Technik und&nbsp;Handwerk", "Teamgeist und&nbsp;Pünktlichkeit", "Gern vorher ein Praktikum bei&nbsp;uns"]),
]

I_PLUS = '<svg class="x-stelle__icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M11 5h2v14h-2z"/><path class="x-stelle__h" d="M5 11h14v2H5z"/></svg>'


def _stelle(s):
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    tags = "".join(f"<span>{x}</span>" for x in s["tags"])
    return f"""
      <details class="x-stelle" id="stelle-{s['id']}">
        <summary>
          <span class="x-stelle__head">
            <span class="x-stelle__tags">{tags}</span>
            <span class="x-stelle__title">{s['titel']}</span>
            <span class="x-stelle__teaser">{s['teaser']}</span>
          </span>
          <span class="x-stelle__more"><span class="x-stelle__open">Details</span><span class="x-stelle__close">Schließen</span>{I_PLUS}</span>
        </summary>
        <div class="x-stelle__body">
          <div><h3 class="x-h4">Deine Aufgaben</h3><ul class="x-check">{li(s['aufgaben'])}</ul></div>
          <div><h3 class="x-h4">Das bringst du&nbsp;mit</h3><ul class="x-check">{li(s['profil'])}</ul></div>
          <div class="x-stelle__go">
            <p>Kein Anschreiben nötig. Name und Telefonnummer reichen, wir melden uns&nbsp;persönlich.</p>
            <a class="nxm-btn nxm-btn--dark" href="#bewerben" data-stelle="{s['id']}">Auf diese Stelle bewerben {ARROW}</a>
          </div>
        </div>
      </details>"""


BENEFITS = """
    <ul class="x-benefits x-benefits--6">
      <li><span class="x-benefits__no">01</span><strong>Familienbetrieb seit&nbsp;1925</strong><span>Vierte Generation, kurze Wege und ein offenes Ohr für deine&nbsp;Ideen.</span></li>
      <li><span class="x-benefits__no">02</span><strong>Unikate statt&nbsp;Serie</strong><span>Treppen, Tore, Geländer und Möbel: Jedes Projekt ist&nbsp;anders.</span></li>
      <li><span class="x-benefits__no">03</span><strong>Ein starkes&nbsp;Team</strong><span>Ein tolles, bunt gemischtes Team, in dem man sich aufeinander verlassen&nbsp;kann.</span></li>
      <li><span class="x-benefits__no">04</span><strong>Verantwortung</strong><span>Eine eigenverantwortliche Position mit Raum für eigene&nbsp;Ideen.</span></li>
      <li><span class="x-benefits__no">05</span><strong>Projekte in der&nbsp;Region</strong><span>Werkstatt in Kelkheim, Baustellen im Rhein-Main-Gebiet statt&nbsp;Fernmontage.</span></li>
      <li><span class="x-benefits__no">06</span><strong>Hörmann-Fachbetrieb</strong><span>Tore, Türen und Antriebe vom Marktführer, fachgerecht&nbsp;montiert.</span></li>
    </ul>"""

ARBEIT = [("treppe-holz-glas", "Freitragende Holztreppe mit&nbsp;Glasgeländer"), ("briefkasten-gold", "Briefkastenanlage in&nbsp;Messingoptik"),
          ("tor-villa", "Einfahrtstor mit&nbsp;Pforte"), ("treppe-licht", "Treppenauge mit&nbsp;Glasbrüstung")]


def bewerbung_form():
    opts = "".join(f'<option value="{s["id"]}">{s["kurz"]}</option>' for s in STELLEN)
    rows = [
        _f("name-1", "Name", _in("name-1", req=True, ac="name"), req=True) + _f("phone-1", "Telefon", _in("phone-1", "tel", True, "tel"), req=True),
        _f("email-1", "E-Mail", _in("email-1", "email", ac="email"))
        + _f("select-1", "Stelle", f'<select name="select-1" id="f-select-1" class="forminator-select x-select">{opts}<option value="initiativ">Initiativbewerbung</option><option value="praktikum">Praktikum</option></select>'),
        _upload("upload-1", "Lebenslauf oder Zeugnisse", "PDF oder Foto vom Handy, mehrere Dateien&nbsp;möglich"),
    ]
    body = ('<div class="forminator-response-message" aria-live="polite" hidden></div>'
            + "".join(f'<div class="forminator-row">{r}</div>' for r in rows)
            + CONSENT.replace("{zweck}", "dass meine Angaben zur Bearbeitung meiner Bewerbung verarbeitet werden.")
            + '<div class="forminator-row forminator-row-last"><div class="forminator-col x-full"><div class="forminator-field">'
              '<button class="forminator-button forminator-button-submit">Bewerbung absenden</button></div></div></div>')
    return f'<form id="nxm-bewerbung" class="forminator-ui forminator-custom-form x-slim" method="post" enctype="multipart/form-data" data-nxm-preview>{body}</form>'


def jobs(t):
    stellen = "".join(_stelle(s) for s in STELLEN)
    fotos = "".join(f'<figure class="x-strip__item"><img src="{P}nxm/img/galerie/{f}.jpg" alt="{a.replace("&nbsp;", " ")}" loading="lazy"><figcaption>{a}</figcaption></figure>' for f, a in ARBEIT)
    return f"""
<section class="x-section x-intro">
  <div class="x-wrap x-split x-split--wide">
    <div>
      <p class="x-eyebrow">Karriere bei erdel</p>
      <h2 class="x-display">Handwerk mit Anspruch. Seit&nbsp;1925.</h2>
      <p class="x-lead">Wir suchen Menschen, die gern mit Metall arbeiten und stolz auf das Ergebnis sind. Bewerben dauert bei uns zwei Minuten, ein Anschreiben brauchen wir&nbsp;nicht.</p>
      <div class="x-cta__actions x-konf-actions">
        <a class="nxm-btn nxm-btn--dark" href="#bewerben">Jetzt bewerben {ARROW}</a>
        <a class="nxm-btn nxm-btn--outline" href="#stellen">Offene Stellen</a>
      </div>
    </div>
    <dl class="x-facts">
      <div><dt>Gegründet</dt><dd>1925</dd></div>
      <div><dt>Familienbetrieb</dt><dd>4.&nbsp;Generation</dd></div>
      <div><dt>Fertigung</dt><dd>Unikate</dd></div>
    </dl>
  </div>
</section>

<section class="x-section x-section--tight" id="stellen">
  <div class="x-wrap">
    <div class="x-stellen__head">
      <div>
        <p class="x-eyebrow">Offene Stellen</p>
        <h2 class="x-h2">Finde deinen Platz im&nbsp;Team</h2>
      </div>
      <p class="x-stellen__note"><mark class="nxm-todo">Beispielstellen: Texte und Konditionen stimmt erdel noch&nbsp;ab.</mark></p>
    </div>
    <div class="x-stellen">{stellen}
    </div>
  </div>
</section>

<section class="x-section x-section--tight">
  <div class="x-wrap">
    <p class="x-eyebrow">So einfach geht's</p>
    <ol class="x-steps3">
      <li><span class="x-steps3__no">01</span><strong>Kurz bewerben</strong><span>Name und Telefonnummer reichen. Lebenslauf gern, Anschreiben&nbsp;nicht.</span></li>
      <li><span class="x-steps3__no">02</span><strong>Wir rufen dich an</strong><span>Persönlich und unkompliziert, damit wir uns kennenlernen&nbsp;können.</span></li>
      <li><span class="x-steps3__no">03</span><strong>Werkstatt erleben</strong><span>Komm vorbei, lern das Team kennen und schau dir unsere Projekte&nbsp;an.</span></li>
    </ol>
  </div>
</section>

<section class="x-section x-section--stone">
  <div class="x-wrap">
    <p class="x-eyebrow">Das bieten wir dir</p>
    <h2 class="x-h2">Warum erdel&nbsp;metallbau?</h2>
    {BENEFITS}
  </div>
</section>

<section class="x-section">
  <div class="x-wrap">
    <p class="x-eyebrow">Daran arbeitest du</p>
    <h2 class="x-h2">Projekte aus unserer&nbsp;Werkstatt</h2>
    <div class="x-strip">{fotos}</div>
    <p class="x-strip__more"><a href="{P}referenzen/">Alle Referenzen ansehen</a></p>
  </div>
</section>

<section class="x-section x-formsec" id="bewerben">
  <div class="x-wrap x-formgrid">
    <aside class="x-formside">
      <img src="{P}nxm/img/montage-transporter.jpg" alt="" loading="lazy">
      <div class="x-formside__body">
        <p class="x-eyebrow x-eyebrow--light">Kurzbewerbung</p>
        <h2>In zwei Minuten&nbsp;beworben</h2>
        <ol class="x-steps">
          <li><strong>Name und Telefon</strong><span>Mehr brauchen wir für den ersten Schritt&nbsp;nicht.</span></li>
          <li><strong>Lebenslauf anhängen</strong><span>Optional, ein Foto vom Handy&nbsp;genügt.</span></li>
          <li><strong>Wir melden uns</strong><span>Persönlich, per Telefon oder&nbsp;E&#8209;Mail.</span></li>
        </ol>
        <div class="x-formside__alt">
          <a class="nxm-btn nxm-btn--light" href="tel:{TEL}">{I_TEL} {TEL_TXT}</a>
          <a class="nxm-btn nxm-btn--ghost" href="{WA}" target="_blank" rel="noopener">{I_WA} WhatsApp</a>
        </div>
        <p class="x-formside__hint">Lieber per E-Mail oder Post? Sende deine Bewerbung an <a href="mailto:{MAIL}">{MAIL}</a> oder an erdel metallbau, Auf der Herrnmauer 12, 65779 Kelkheim im&nbsp;Taunus.</p>
      </div>
    </aside>
    <div class="x-formcard">
      <div class="x-formcard__head"><h2>Deine Kurz&shy;bewerbung</h2><p class="x-formcard__req"><span aria-hidden="true">*</span> Pflichtfeld</p></div>
      {bewerbung_form()}
    </div>
  </div>
</section>
"""


def weiterleitung(ziel, titel):
    """Alte Unterseiten (Stellenseite, Bewerbungsformular) führen direkt in den neuen Karrierebereich."""
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, follow">
<title>{titel} &#8211; Erdel Metallbau</title>
<link rel="canonical" href="{ziel}">
<meta http-equiv="refresh" content="0; url={ziel}">
<script>location.replace({ziel!r});</script>
</head>
<body style="font-family:Arial,sans-serif;padding:24px">
<p>Weiter zu <a href="{ziel}">{titel}</a>.</p>
</body>
</html>
"""


GEN = [
    ("1925", "1. Generation", "Gründung durch Clemens&nbsp;Erdel",
     "Im Jahr 1925 machte sich Clemens Erdel, gelernter Dreher, in einer kleinen Werkstatt in Kelkheim selbstständig. Kelkheim wurde immer mehr für seine Möbelindustrie bekannt. Für Schreinereien wurden im eigenen Betrieb Leimöfen, Band- und Tellerschleifmaschinen sowie Furnierpressen gebaut. Besonders die Furnierpressen aus eigener Herstellung waren, nicht nur in Kelkheim, bekannt und&nbsp;begehrt.",
     None),   # kein historisches Foto vorhanden: Typo-Karte statt Stockfoto
    ("1960", "2. Generation", "Vom Maschinenbau zur&nbsp;Schlosserei",
     "Im Jahr 1960 übernahm Clemens Erdel Junior, gelernter Schlosser, die Firma Clemens Erdel &amp; Sohn. Durch die Industrialisierung im Maschinenbau wurde der Betrieb auf Schlosserarbeiten umgestellt. Im Jahr 1970 starb Clemens Erdel Junior an den Folgen einer Lungenentzündung, sein Vater folgte ihm drei Monate&nbsp;später.",
     "wp-content/uploads/2022/07/IMG_2525-scaled.jpg"),
    ("1970", "3. Generation", "Josefine und Helmuth&nbsp;Erdel",
     "Josefine Erdel, Frau von Clemens Erdel Junior, übernahm die Geschäftsführung der Schlosserei, um ihrem Sohn Helmuth den Gang zur Meisterschule zu ermöglichen. Die Regierung gestattete Josefine nur ein Jahr lang, den Metallbaubetrieb zu leiten. Im Jahr 1970 ging die Schlosserei Clemens Erdel &amp; Sohn traditionsgetreu in Helmuth Erdels Hände&nbsp;über.",
     "wp-content/uploads/2022/07/Weldkugel.jpg"),
    ("2001", "4. Generation", "Die erdel metallbau&nbsp;GmbH",
     "Im Jahr 2001 wurde aus der Firma Clemens Erdel &amp; Sohn die erdel metallbau GmbH. Seitdem übernahmen Helmuth Erdel und sein Sohn Marc Erdel, gelernter Schlosser, gemeinsam die&nbsp;Geschäftsführung.",
     "nxm/img/tor-anthrazit.jpg"),
    ("heute", "erdel metallbau GmbH", "Tradition, weitergedacht",
     "Heute wird die Schlosserei erdel metallbau GmbH von Marc Erdel in der 4. Generation weitergeführt und&nbsp;weiterentwickelt.",
     "nxm/img/zaun-lamellen.jpg"),
]


def historie(t):
    items = "".join(f"""
    <li class="x-tl__item">
      {f'<figure class="x-tl__media"><img src="{P}{img}" alt="{g}: {sub.replace(chr(38) + "nbsp;", " ")}" loading="lazy"></figure>' if img else '<figure class="x-tl__media x-tl__media--typo"><small>Aus eigener Herstellung</small><span>Leimöfen</span><span>Band- und Teller&shy;schleif&shy;maschinen</span><span>Furnier&shy;pressen</span></figure>'}
      <div class="x-tl__text">
        <p class="x-tl__year">{y}</p>
        <p class="x-eyebrow">{g}</p>
        <h3>{sub}</h3>
        <p>{txt}</p>
      </div>
    </li>""" for y, g, sub, txt, img in GEN)
    return f"""
<section class="x-section x-intro">
  <div class="x-wrap x-split x-split--wide">
    <div>
      <p class="x-eyebrow">Historie</p>
      <h2 class="x-display">Vier Generationen&nbsp;Metallbau.</h2>
    </div>
    <p class="x-lead">Seit 1925 steht unser Metallbaubetrieb für handwerkliche Qualität und Zuverlässigkeit. Durch persönliche, kompetente und individuelle Beratung erhalten Ihre Ideen und Konstruktionen&nbsp;Einzigartigkeit.</p>
  </div>
</section>

<section class="x-section x-section--tight">
  <div class="x-wrap">
    <ol class="x-tl">{items}
    </ol>
  </div>
</section>

<section class="x-cta">
  <img src="{P}nxm/img/haus-terrasse.jpg" alt="" loading="lazy">
  <div class="x-wrap x-cta__inner">
    <div>
      <p class="x-eyebrow x-eyebrow--light">Ihr Projekt</p>
      <h2>Fast 100 Jahre Erfahrung für Ihr&nbsp;Unikat.</h2>
    </div>
    <div class="x-cta__actions">
      <a class="nxm-btn nxm-btn--light" href="{P}kontakt/">Projekt anfragen {ARROW}</a>
      <a class="nxm-btn nxm-btn--ghost" href="{P}referenzen/">Referenzen ansehen</a>
    </div>
  </div>
</section>
"""


I_PDF = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 2h8l6 6v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm7 1.5V9h5.5L13 3.5zM8 13v5h1.4v-1.6h.8c1.1 0 1.8-.6 1.8-1.7S11.3 13 10.2 13H8zm1.4 1.1h.7c.4 0 .6.2.6.6s-.2.6-.6.6h-.7v-1.2zM12.4 13v5h1.7c1.5 0 2.4-.9 2.4-2.5S15.6 13 14.1 13h-1.7zm1.4 1.2h.2c.7 0 1.1.4 1.1 1.3s-.4 1.3-1.1 1.3h-.2v-2.6z"/></svg>'
I_EXT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 3h7v7h-2V6.4l-9.3 9.3-1.4-1.4L17.6 5H14V3zM5 5h6v2H5v12h12v-6h2v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z"/></svg>'
UP = "wp-content/uploads/2022/10/"

KONFIG = {
  "konfiguration-tueren/index.html": dict(
    art="Türen", title="Maßanfertigungen von&nbsp;Türen", img="nxm/img/eingang-holztuer.jpg", hero="nxm/img/eingang-anthrazit.jpg", claim="Türen nach&nbsp;Maß",
    lead="Die langjährige Partnerschaft des Systemhauses HÖRMANN und erdel metallbau zeichnet sich durch Qualität, Zuverlässigkeit und Vertrauen aus. Unsere Kunden profitieren von individuellen Lösungen und einer unschlagbaren&nbsp;Produktqualität.",
    sub="Türen für innen &amp;&nbsp;außen", sub2="Hohe Sicherheitsansprüche und beste&nbsp;Wärmedämmwerte",
    text="Wenn Sie Ihren Hauseingang mit einer qualitativ hochwertigen und optisch ansprechenden Tür abrunden möchten, treffen Sie mit einer Hörmann-Eingangstür genau die richtige Wahl. Wir unterstützen Sie bei Ihrem&nbsp;Vorhaben.",
    check=["Zwei Fotos der bestehenden Haustür (innen und außen)", "Höhe und Breite", "Türvariante", "Gewünschtes Motiv bzw. gewünschte Farbe", "Bei Neubauten: Bauplan mit Maßen&nbsp;(optional)"],
    downloads=[("Katalog Aluminium-Haustüren", UP + "Katalog_Aluminium_Haustueren.pdf"), ("Hörmann-Vorzugsfarben", UP + "HOeRMANN_Vorzugsfarben.pdf"), ("Aufmaßblatt", UP + "Aufmassblatt.pdf")],
    kfw=UP + "KFW-Zuschuss-bei-RC2-Sicherheitsausstattung-1.pdf",
    step3=("Ihr Angebot", "Sobald alle Informationen vorliegen, erstellen wir Ihr individuelles&nbsp;Angebot.")),
  "konfiguration-tore/index.html": dict(
    art="Tore", title="Qualitätsprodukte nach Ihren&nbsp;Vorstellungen", img="nxm/img/tor-anthrazit.jpg", hero="nxm/img/garagentor-verkleidet-2.jpg", claim="Tore nach&nbsp;Maß",
    lead="Die langjährige Partnerschaft des Systemhauses HÖRMANN und erdel metallbau zeichnet sich durch Qualität, Zuverlässigkeit und Vertrauen aus. Unsere Kunden profitieren von individuellen Lösungen und einer unschlagbaren&nbsp;Produktqualität.",
    sub="Industrietore und&nbsp;Antriebe", sub2="Hier schwingt Qualität in schöner&nbsp;Optik",
    text="Alles spricht für das Original: Qualität und Sicherheit, Optik und Komfort und die ausgereifte Technik. In jedem Hörmann-Tor steckt die Erfahrung von über 50 Jahren Know-how im Bau von&nbsp;Garagentoren.",
    check=["Zwei Fotos der bestehenden Garage (innen und außen)", "Maße laut Aufmaßblatt", "Wunschfarbe: Standard ist Verkehrsweiß RAL 9016, weitere Hörmann-Vorzugsfarben im&nbsp;Download", "Größe der Sektionen und Wunsch der Oberfläche", "Ist ein Antrieb gewünscht?", "Bei Neubauten: Bauplan mit&nbsp;Maßen"],
    downloads=[("Aufmaßblatt", UP + "Aufmassblatt.pdf"), ("Hörmann-Vorzugsfarben", UP + "HOeRMANN_Vorzugsfarben-1.pdf"), ("Größe der Sektionen", UP + "HOeRMANN-Sektionaltor-Sektionen.pdf"), ("Oberflächen", UP + "HOeRMANN-Oberflaechen.pdf")],
    kfw=UP + "KFW-Zuschuss-bei-RC2-Sicherheitsausstattung.pdf",
    step3=("Termin vor Ort &amp; Angebot", "Wir nehmen die genauen Aufmaße, beraten Sie persönlich und erstellen Ihr&nbsp;Angebot.")),
}


def konfig_for(rel):
    d = KONFIG[rel]
    def fn(t):
        form = konfig_form(t, d["art"])
        checks = "".join(f"<li>{c}</li>" for c in d["check"])
        dls = "".join(f'<a class="x-dl" href="{P}{h}" target="_blank" rel="noopener">{I_PDF}<span class="x-dl__name">{n}</span><span class="x-dl__meta">PDF öffnen</span></a>' for n, h in d["downloads"])
        return f"""
<section class="x-section x-konf-hero">
  <div class="x-wrap x-split x-split--konf">
    <div>
      <p class="x-eyebrow">Hörmann · Konfiguration {d['art']}</p>
      <h2 class="x-display">{d['title']}</h2>
      <p class="x-lead">{d['lead']}</p>
      <div class="x-cta__actions x-konf-actions">
        <a class="nxm-btn nxm-btn--dark" href="#anfrage">Anfrage starten {ARROW}</a>
        <a class="nxm-btn nxm-btn--outline" href="https://www.hoermann.de/konfigurator/" target="_blank" rel="noopener">Hörmann&#8209;Konfigurator {I_EXT}</a>
      </div>
    </div>
    <figure class="x-konf-media"><img src="{P}{d['img']}" alt="Hörmann {d['art']} von erdel metallbau"><figcaption><strong>{d['sub']}</strong><span>{d['sub2']}</span></figcaption></figure>
  </div>
</section>

<section class="x-section x-section--tight">
  <div class="x-wrap">
    <p class="x-lead x-lead--wide">{d['text']}</p>
    <ol class="x-steps3">
      <li><span class="x-steps3__no">01</span><strong>Unterlagen&nbsp;zusammenstellen</strong><span>Fotos, Maße und Wünsche, die Checkliste unten hilft&nbsp;dabei.</span></li>
      <li><span class="x-steps3__no">02</span><strong>Anfrage senden</strong><span>Alles direkt im Formular hochladen, auch Ihre&nbsp;Hörmann&#8209;Konfiguration.</span></li>
      <li><span class="x-steps3__no">03</span><strong>{d['step3'][0]}</strong><span>{d['step3'][1]}</span></li>
    </ol>
  </div>
</section>

<section class="x-section x-section--stone">
  <div class="x-wrap x-two x-two--konf">
    <div>
      <p class="x-eyebrow">Checkliste</p>
      <h2 class="x-h3">Das hilft uns beim&nbsp;Angebot</h2>
      <ul class="x-check">{checks}</ul>
      <p class="x-note">Nichts davon ist Pflicht. Was fehlt, klären wir beim Termin vor&nbsp;Ort.</p>
    </div>
    <div>
      <p class="x-eyebrow">Downloads</p>
      <h2 class="x-h3">Unterlagen &amp;&nbsp;Hilfen</h2>
      <div class="x-dls">{dls}</div>
      <a class="x-kfw" href="{P}{d['kfw']}" target="_blank" rel="noopener">
        <span class="x-kfw__tag">KfW-Förderung</span>
        <strong>Zuschuss für Einbruchschutz</strong>
        <span>Mit dem KfW-Programm können Sie sich Zuschüsse für verschiedene Maßnahmen sichern, zum Beispiel für Türen mit RC2-Sicherheitsausstattung.</span>
        <span class="x-kfw__go">Infos zum Zuschuss (PDF) {ARROW}</span>
      </a>
      <a class="x-konfig" href="https://www.hoermann.de/konfigurator/" target="_blank" rel="noopener">
        <span><strong>Online konfigurieren</strong><span>Stellen Sie Ihr Wunschmodell im Hörmann&#8209;Konfigurator zusammen und laden Sie die Konfiguration im Formular&nbsp;hoch.</span></span>
        {I_EXT}
      </a>
    </div>
  </div>
</section>

<section class="x-section x-formsec" id="anfrage">
  <div class="x-wrap x-formgrid x-formgrid--konf">
    <aside class="x-formside">
      <img src="{P}{d['img']}" alt="" loading="lazy">
      <div class="x-formside__body">
        <p class="x-eyebrow x-eyebrow--light">Anfrageformular</p>
        <h2>Ihre Anfrage für {d['art']}</h2>
        <ol class="x-steps">
          <li><strong>Kontakt angeben</strong><span>Name, Telefon, E&#8209;Mail und&nbsp;Ort.</span></li>
          <li><strong>Wünsche beschreiben</strong><span>Ein paar Stichworte&nbsp;genügen.</span></li>
          <li><strong>Fotos anhängen</strong><span>Wenn vorhanden, gern auch&nbsp;später.</span></li>
        </ol>
        <p class="x-formside__hint">Nicht alles zur Hand? Schicken Sie, was Sie haben. Den Rest klären wir beim Termin vor Ort oder unter <a href="tel:{TEL}">{TEL_TXT}</a>.</p>
      </div>
    </aside>
    <div class="x-formcard">
      <div class="x-formcard__head"><h2>Anfrage&nbsp;{d['art']}</h2><p class="x-formcard__req"><span aria-hidden="true">*</span> Pflichtfeld</p></div>
      {form}
    </div>
  </div>
</section>
"""
    return fn


REDIRECT = {"kalkulator-job1/index.html": ("../jobs/#stelle-metallbauer", "Stelle Metallbauer:in"),
            "bewerbungsformular/index.html": ("../jobs/#bewerben", "Bewerbung")}

PAGES = {"kontakt/index.html": kontakt, "jobs/index.html": jobs, "historie/index.html": historie,
         "konfiguration-tueren/index.html": konfig_for("konfiguration-tueren/index.html"),
         "konfiguration-tore/index.html": konfig_for("konfiguration-tore/index.html")}

for rel, (ziel, titel) in REDIRECT.items():
    open(os.path.join(ROOT, rel), "w", encoding="utf-8").write(weiterleitung(ziel, titel))
    print("weiterleitung:", rel)

for rel, fn in PAGES.items():
    p = os.path.join(ROOT, rel)
    t = open(p, encoding="utf-8").read()
    a = t.find('<div class="main-body">') + len('<div class="main-body">')
    b = t.find('<footer class="main-footer">')
    if b < 0:
        b = t.find('</main>', a)   # Bewerbungsseite hat keinen main-footer
    assert a > 30 and b > a, rel
    inner = t[a:b]
    if "nxm:seite" in inner:
        # erneuter Lauf: Formular aus der bereits umgebauten Seite holen
        pass
    new = "\n<!-- nxm:seite -->" + fn(t) + "<!-- /nxm:seite -->\n</div>\n"
    # Rest des alten main-body (schließendes div) entfernen: wir schließen selbst
    t = t[:a] + new + t[b:]
    if rel.startswith(("konfiguration-", "bewerbungsformular")):
        t = re.sub(r'<header class="main-header">.*?</header>', '', t, count=1, flags=re.S)
    if rel in KONFIG and "featured-full-width-img" not in t:
        d = KONFIG[rel]
        hero = (f'<header class="main-header featured-full-width-img bg-dark text-light mb-3" style="background-image: url(\'{P}{d["hero"]}\')">'
                f'<div class="container h-100 d-flex align-items-end pb-3 ms-auto p-2 bd-highlight"><h1>{d["claim"]}</h1></div></header>\n')
        t = t.replace('<main id="main" class="main-content">', '<main id="main" class="main-content">\n' + hero, 1)
        t = t.replace('<body class="nxm-nohero ', '<body class="nxm-hero ', 1)
    open(p, "w", encoding="utf-8").write(t)
    print("neu:", rel)
