"""Kundenrunde 30.10.2026: Texte, Öffnungszeiten, Qualitätsleiste, Kontakt-Leiste rechts.

Aufruf:  python3 werkzeuge/kundenrunde_3010.py
  - weniger „Unikat“ / „keine Grenzen“ (ein „Unikat für die Ewigkeit“ bleibt auf Leistungen)
  - Geschäftszeiten ab 7:00 Uhr (Fuß, Kontaktseite; Live-Status in nxm.js)
  - „seit 1925 / über 100 Jahre“, Meisterbetrieb, TÜV-zertifiziert, DIN EN 1090, 3D-Werkplanung (CAD)
    als Leiste auf der Startseite, im Fuß und auf Historie
  - alle Formulare zeigen in der Vorschau nur einen Hinweis (Empfänger beim Livegang: info@erdel-metallbau.de)
  - feste Kontakt-Leiste (Telefon, E-Mail) am rechten Bildrand, erscheint nach dem Scrollen (Desktop)
Idempotent. Nach seiten.py/abschluss.py/paare_loesen.py laufen lassen, vor kopfbilder.py."""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEL, TEL_TXT, MAIL = "+49619563192", "06195&nbsp;63192", "info@erdel-metallbau.de"
I_TEL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>'
I_MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18c.6 0 1 .4 1 1v12c0 .6-.4 1-1 1H3a1 1 0 0 1-1-1V6c0-.6.4-1 1-1zm9 7.3L4 7.2V17h16V7.2l-8 5.1zM5.2 7l6.8 4.3L18.8 7H5.2z"/></svg>'

# Für alle Seiten: (alt, neu)
TEXT = [
    # Fuß
    ("Tore, Geländer, Treppen und Unikate aus Metall. Gefertigt in Kelkheim im Taunus, seit&nbsp;1925.",
     "Tore, Geländer, Treppen und Sonderanfertigungen aus Metall. Meisterbetrieb in Kelkheim im Taunus, seit&nbsp;1925."),
    # Geschäftszeiten
    ("8:00 bis 16:30", "7:00 bis 16:30"), ("8:00 bis 13:00", "7:00 bis 13:00"),
    ("8:00 – 16:30", "7:00 – 16:30"), ("8:00 – 13:00", "7:00 – 13:00"),
    # Startseite
    ("Unser Fokus liegt in der Freude am Gestalten. Wir fertigen hochwertige Unikate. Dabei sind den Wünschen unserer Kunden keine Grenzen&nbsp;gesetzt.",
     "Unser Fokus liegt in der Freude am Gestalten. Seit über 100&nbsp;Jahren fertigen wir in Kelkheim hochwertige Metallarbeiten nach Maß, ganz nach den Wünschen unserer&nbsp;Kunden."),
    # Leistungen
    ("hochwertige Veredelungen die Ihre Treppe zu einem Unikat machen.",
     "hochwertige Veredelungen, die Ihrer Treppe eine eigene Handschrift geben."),
    ("Dabei sind Ihnen keine Grenzen&nbsp;gesetzt!", "Gemeinsam finden wir die Lösung, die zu Ihrem Haus&nbsp;passt."),
    ("Wir schaffen einzigartige Unikate für unsere Kunden. Dabei sind Ihren Vorstellungen keine Grenzen gesetzt. Dabei sind wir",
     "Wir veredeln Metall ganz nach Ihren Vorstellungen. Dabei sind wir"),
    ("Wir machen aus Serienmöbeln Unikate.", "Wir machen aus Serienmöbeln Einzelstücke."),
    # Historie
    ("Fast 100 Jahre Erfahrung für Ihr&nbsp;Unikat.", "Über 100 Jahre Erfahrung für Ihr&nbsp;Projekt."),
    ("Seit 1925 steht unser Metallbaubetrieb für handwerkliche Qualität und Zuverlässigkeit.",
     "Seit 1925, also seit über 100 Jahren, steht unser Metallbaubetrieb für handwerkliche Qualität und Zuverlässigkeit. "
     "Als TÜV-zertifizierter Meisterbetrieb fertigen wir nach DIN EN 1090 und planen jedes Projekt vorab in 3D im&nbsp;CAD."),
    # Kontakt
    ("individuelles Angebot für Ihr&nbsp;Unikat.", "individuelles Angebot für Ihr&nbsp;Vorhaben."),
    # Referenzen
    ("Unsere Kompetenz und Leidenschaft liegt in der Gestaltung von Unikaten.",
     "Unsere Kompetenz und Leidenschaft liegt in der Gestaltung individueller Metallarbeiten."),
    ("Ihr Unikat ist das nächste&nbsp;Projekt.", "Ihr Vorhaben ist unser nächstes&nbsp;Projekt."),
    # Jobs
    ("<dt>Fertigung</dt><dd>Unikate</dd>", "<dt>Fertigung</dt><dd>Maßarbeit</dd>"),
    ("Unikate statt&nbsp;Serie", "Maßarbeit statt&nbsp;Serie"),
]

QUALI = """<!-- nxm:qualitaet -->
    <div class="row px-3">
        <div class="col-md-2 d-sm-none d-md-block"></div>
        <div class="col-lg-9 col-sm-12">
            <ul class="nxm-quali" aria-label="Das zeichnet uns aus">
                <li><strong>Seit&nbsp;1925</strong><span>Über 100 Jahre Familienbetrieb in&nbsp;Kelkheim</span></li>
                <li><strong>Meisterbetrieb</strong><span>Handwerk mit&nbsp;Meisterbrief</span></li>
                <li><strong>TÜV-zertifiziert</strong><span>Unabhängig geprüfte&nbsp;Qualität</span></li>
                <li><strong>DIN&nbsp;EN&nbsp;1090</strong><span>Tragende Bauteile nach Norm&nbsp;gefertigt</span></li>
                <li><strong>3D-Werkplanung</strong><span>Jedes Projekt vorab im CAD&nbsp;konstruiert</span></li>
            </ul>
        </div>
    </div>
<!-- /nxm:qualitaet -->"""

# leere Textzeile unter dem Einleitungssatz der Startseite
LEER = re.compile(r'<div class="row px-3">\s*<div class="col-lg-4 d-sm-none d-md-block">\s*</div>\s*'
                  r'<div class="col-lg-8 col-sm-12 px-5 mb-5"[^>]*>\s*<p>\s*</p>\s*</div>\s*</div>')

DOCK = f"""<!-- nxm:dock -->
<nav class="nxm-dock" aria-label="Direktkontakt">
  <a href="tel:{TEL}">{I_TEL}<span>{TEL_TXT}</span></a>
  <a href="mailto:{MAIL}">{I_MAIL}<span>{MAIL}</span></a>
</nav>
<!-- /nxm:dock -->"""


def pages():
    for d, _, files in os.walk(ROOT):
        rel = os.path.relpath(d, ROOT)
        if rel.split(os.sep)[0] in ("wp-content", "wp-includes", "wp-admin", "nxm", "werkzeuge", ".git"):
            continue
        if "index.html" in files:
            yield os.path.join(d, "index.html")


for p in pages():
    s = open(p, encoding="utf-8").read()
    n = s
    for a, b in TEXT:
        n = n.replace(a, b)
    if os.path.relpath(p, ROOT) == "index.html" and "nxm:qualitaet" not in n:
        n, k = LEER.subn(QUALI, n, count=1)
        if not k:
            raise SystemExit("Startseite: Platz für die Qualitätsleiste nicht gefunden")
    # alle Formulare im Vorschau-Modus (kein Absenden an relaunch.erdel-metallbau.de)
    n = re.sub(r'<form(?![^>]*data-nxm-preview)(\s[^>]*forminator-ui[^>]*)>', r'<form\1 data-nxm-preview>', n)
    # keine Aufrufe an das alte WordPress: Nonce-Abfrage raus, Ajax-Adresse lokal (wird nie angefragt)
    n = re.sub(r'<script type="text/javascript">jQuery\(function\(\) \{jQuery\.ajax\(\{url: \'https://relaunch\.erdel-metallbau\.de/'
               r'wp-admin/admin-ajax\.php\',type: "POST",data: \{action: "forminator_get_nonce".*?</script>', "", n, flags=re.S)
    n = n.replace('"ajaxUrl":"https://relaunch.erdel-metallbau.de/wp-admin/admin-ajax.php"', '"ajaxUrl":"#"')
    if "nxm:dock" not in n and "<!-- /nxm:actions -->" in n:
        n = n.replace("<!-- /nxm:actions -->", "<!-- /nxm:actions -->\n" + DOCK, 1)
    if n != s:
        open(p, "w", encoding="utf-8").write(n)
        print("geändert:", os.path.relpath(p, ROOT))
