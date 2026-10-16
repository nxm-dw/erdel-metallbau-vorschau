"""Rechtliche Aktualisierungen (Stand Oktober 2026). Idempotent.
Offene Angaben, die nur der Kunde liefern kann, werden gelb markiert (.nxm-todo)."""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def edit(rel, fn):
    p = os.path.join(ROOT, rel)
    t = open(p, encoding="utf-8").read()
    n = fn(t)
    if n != t:
        open(p, "w", encoding="utf-8").write(n)
        print("geändert:", rel)


def todo(s):
    return f'<mark class="nxm-todo">{s}</mark>'


IMPRESSUM = f"""<h1>Impressum</h1>
<h2>Angaben gemäß § 5 DDG</h2>
<p>erdel metallbau GmbH<br />
Auf der Herrnmauer 12<br />
65779 Kelkheim im Taunus</p>
<h3>Vertreten durch</h3>
<p>Marc Erdel {todo("(Funktion bitte bestätigen, z. B. Geschäftsführer)")}</p>
<h3>Registereintrag</h3>
<p>Eintragung im Handelsregister<br />
Registergericht: {todo("Amtsgericht bitte ergänzen")}<br />
Registernummer: HRB 5572 {todo("bitte bestätigen")}</p>
<h3>Umsatzsteuer-ID</h3>
<p>Umsatzsteuer-Identifikationsnummer gemäß § 27a Umsatzsteuergesetz:<br />
{todo("DE … bitte ergänzen, falls vorhanden")}</p>
<h3>Kontakt</h3>
<p>Telefon: <a href="tel:+49619563192">06195 63192</a><br />
E-Mail: <a href="mailto:info@erdel-metallbau.de">info@erdel-metallbau.de</a></p>
<h3>Berufsbezeichnung und berufsrechtliche Regelungen</h3>
<p>Berufsbezeichnung: Metallbauer (Handwerk), verliehen in Deutschland<br />
Zuständige Kammer: {todo("Handwerkskammer Wiesbaden, bitte bestätigen")}<br />
Es gilt die Handwerksordnung (HwO), abrufbar unter <a href="https://www.gesetze-im-internet.de/hwo/" target="_blank" rel="noopener">gesetze-im-internet.de/hwo</a>.</p>
<h3>Verbraucherstreitbeilegung</h3>
<p>Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
"""

FONTS = """<h3>Schriftarten (lokal eingebunden)</h3>
<p>Für eine einheitliche Darstellung nutzt diese Website die Schriftart „Oxygen“. Die Schriftdateien liegen auf unserem eigenen Server. Beim Aufruf der Seite wird keine Verbindung zu Servern Dritter, etwa von Google, aufgebaut, und es werden dabei keine personenbezogenen Daten an Dritte übermittelt.</p>"""

NEU = """<!-- nxm:datenschutz-ergaenzung -->
<h3>Anfragen über die Konfiguratoren für Tore und Türen</h3>
<p>Wenn Sie uns über die Konfiguratoren eine Anfrage senden, verarbeiten wir die eingegebenen Angaben (z. B. Name, Anschrift, Telefonnummer, E-Mail-Adresse, Maße, Farb- und Oberflächenwünsche) sowie hochgeladene Dateien wie Fotos oder Aufmaßblätter. Die Verarbeitung dient der Erstellung eines Angebots und erfolgt auf Grundlage von Art. 6 Abs. 1 lit. b DSGVO (vorvertragliche Maßnahmen). Wir löschen die Daten, sobald sie für diesen Zweck nicht mehr erforderlich sind, sofern keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p>
<h3>Bewerbungen</h3>
<p>Bewerben Sie sich bei uns, über das Bewerbungsformular, per E-Mail oder per Post, verarbeiten wir Ihre Angaben und Unterlagen ausschließlich zur Durchführung des Bewerbungsverfahrens. Rechtsgrundlage ist § 26 BDSG in Verbindung mit Art. 6 Abs. 1 lit. b DSGVO. Kommt kein Arbeitsverhältnis zustande, löschen wir Ihre Unterlagen spätestens sechs Monate nach Abschluss des Verfahrens, es sei denn, Sie haben in eine längere Speicherung eingewilligt (Art. 6 Abs. 1 lit. a DSGVO). Kommt ein Arbeitsverhältnis zustande, werden Ihre Daten zur Durchführung des Beschäftigungsverhältnisses weiterverarbeitet.</p>
<h3>Kontakt über WhatsApp</h3>
<p>Auf unserer Website verlinken wir auf WhatsApp. Erst wenn Sie den Link anklicken, wird die WhatsApp-Anwendung bzw. -Website des Anbieters WhatsApp Ireland Limited, Merrion Road, Dublin 4, D04 X2K5, Irland, geöffnet. Beim bloßen Besuch unserer Website werden keine Daten an WhatsApp übertragen. Schreiben Sie uns über WhatsApp, verarbeitet der Anbieter Ihre Daten nach seinen eigenen Datenschutzbestimmungen (<a href="https://www.whatsapp.com/legal/privacy-policy-eea" target="_blank" rel="noopener">whatsapp.com/legal/privacy-policy-eea</a>); eine Übermittlung in Drittländer wie die USA kann dabei nicht ausgeschlossen werden. Wir nutzen Ihre Nachricht nur zur Beantwortung Ihres Anliegens (Art. 6 Abs. 1 lit. b bzw. f DSGVO). Alternativ erreichen Sie uns jederzeit per Telefon oder E-Mail.</p>
<h3>Cookies</h3>
<p>Diese Website setzt keine Cookies zu Analyse- oder Marketingzwecken und verwendet keine Tracking- oder Analysedienste. Eine Einwilligungsabfrage („Cookie-Banner“) ist daher nicht erforderlich.</p>
<p><em>Stand: Oktober 2026</em></p>
<!-- /nxm:datenschutz-ergaenzung -->"""


def impressum(t):
    if "nxm:impressum" in t:
        return t
    s = t.find("<h1><strong>Impressum</strong></h1>")
    e = t.find("teilzunehmen.</p>", s) + len("teilzunehmen.</p>")
    assert s > 0 and e > s
    return t[:s] + "<!-- nxm:impressum -->\n" + IMPRESSUM + "<!-- /nxm:impressum -->" + t[e:]


def datenschutz(t):
    t = t.replace("TTDSG", "TDDDG")
    t = t.replace(" Andere Daten können zur Analyse Ihres Nutzerverhaltens verwendet werden.", "")
    # Google-Fonts-Abschnitt ersetzen (Seite lädt keine Google Fonts)
    t = re.sub(r"<h3>Google Web Fonts \(lokales Hosting\)</h3>.*?(?=<h[23]|\s*</div>)", FONTS + "\n", t, count=1, flags=re.S)
    if "nxm:datenschutz-ergaenzung" not in t:
        i = t.find("<h3><strong>5. Plugins und Tools</strong></h3>")
        assert i > 0
        t = t[:i] + NEU + "\n" + t[i:]
    return t


def doppelte_h1(t):
    # Seiten mit eigener H1 im Inhalt: Kopf-H1 wieder leeren
    body = t[t.find('<div class="main-body">'):]
    if "<h1" in body:
        t = re.sub(r'(<header class="main-header">\s*<div[^>]*>\s*)<h1>[^<]*</h1>', r"\1<h1></h1>", t, count=1)
    return t


edit("impressum/index.html", lambda t: doppelte_h1(impressum(t)))
edit("datenschutzerklaerung/index.html", lambda t: doppelte_h1(datenschutz(t)))
for rel in ["konfiguration-tore/index.html", "konfiguration-tueren/index.html", "bewerbungsformular/index.html"]:
    edit(rel, doppelte_h1)

# Überschriften und kleine Textfehler
FIX = [
    ("seit1925", "seit 1925"),
    ("<h1>werde Teil unseres Teams</h1>", "<h1>Werde Teil unseres Teams</h1>"),
    ("<h1>HÖRMANN - Starke Partner</h1>", "<h1>HÖRMANN – starker Partner</h1>"),
    ('href="https://www.galabau-ferschke.de/" _blank>', 'href="https://www.galabau-ferschke.de/" target="_blank" rel="noopener">'),
    ("Strasse *", "Straße *"),
]
for rel in ["index.html"] + [d + "/index.html" for d in os.listdir(ROOT) if os.path.isfile(os.path.join(ROOT, d, "index.html")) and not d.startswith(("wp-", "nxm", "werkzeuge"))]:
    def f(t):
        for a, b in FIX:
            t = t.replace(a, b)
        return t
    edit(rel, f)
