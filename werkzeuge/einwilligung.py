"""Datenschutz-Einwilligung in allen Formularen: einheitlicher Text mit Link, Pflichtfeld,
nicht vorausgewählt. Kontakt bekommt das Feld neu, Bewerbung/Konfiguratoren erhalten neuen Text. Idempotent."""
import os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MAIL = "info@erdel-metallbau.de"

def text(zweck):
    return (f'Ich habe die <a href="../datenschutzerklaerung/" target="_blank" rel="noopener">Datenschutzerklärung</a> gelesen und bin '
            f'einverstanden, dass meine Angaben {zweck} verarbeitet werden. Widerruf jederzeit per E-Mail an '
            f'<span class="nxm-nowrap">{MAIL}</span> möglich.&nbsp;<span class="forminator-required">*</span>')

FEHLER = '<p class="nxm-consent__error" role="alert" hidden>Bitte bestätigen Sie die Datenschutzerklärung, damit wir Ihre Anfrage bearbeiten dürfen.</p>'

def kontakt(t):
    if 'data-nxm-consent' in t: return t
    row = ('<div class="forminator-row nxm-consent-row"><div id="nxm-consent" class="forminator-col forminator-col-12">'
           '<div class="forminator-field"><label class="forminator-checkbox nxm-consent">'
           '<input type="checkbox" name="datenschutz" value="Ja" required data-nxm-consent>'
           '<span class="forminator-checkbox-box" aria-hidden="true"></span>'
           f'<span class="forminator-checkbox-label">{text("zur Bearbeitung meiner Anfrage")}</span></label>{FEHLER}</div></div></div>')
    m = re.search(r'<form\s+id="forminator-module-691"', t); s = m.start() if m else -1
    e = t.find('<div class="forminator-row forminator-row-last">', s)
    assert s > 0 and e > s
    t = t[:e] + row + t[e:]
    # bisherigen Hinweis unter dem Formular entfernen (steht jetzt in der Einwilligung)
    t = re.sub(r'\s*<p class="nxm-form-hint">.*?</p>', '', t, count=1, flags=re.S)
    return t

def vorhanden(t, zweck):
    """Bestehendes Forminator-Kästchen (Bewerbung: „Ja“, Konfigurator: langer Text) umbeschriften und als Pflicht markieren."""
    s = t.find('<form'); e = t.find('</form>', s)
    fm = t[s:e]
    if 'data-nxm-consent' in fm: return t
    m = re.search(r'(<div role="group" class="forminator-field required"[^>]*>)(.*?)(</div>\s*</div>\s*</div>)', fm, re.S)
    assert m, "Einwilligungsfeld nicht gefunden"
    grp = m.group(2)
    grp = re.sub(r'(<input type="checkbox"[^>]*?)(/?>)', r'\1 required data-nxm-consent\2', grp, count=1)
    grp = re.sub(r'<span class="forminator-checkbox-label">.*?</span>', f'<span class="forminator-checkbox-label">{text(zweck)}</span>', grp, count=1, flags=re.S)
    grp = re.sub(r'(<label[^>]*class="forminator-checkbox")\s+title="[^"]*"', r'\1', grp, count=1)
    grp = re.sub(r'<span id="[^"]*-description" class="forminator-description">.*?</span>', '', grp, count=1, flags=re.S)
    if 'forminator-label">Datenschutz' not in grp:
        grp = '<p class="forminator-label">Datenschutz <span class="forminator-required">*</span></p>' + grp
    grp += FEHLER
    fm = fm[:m.start(2)] + grp + fm[m.end(2):]
    return t[:s] + fm + t[e:]

JOBS = {
    "kontakt/index.html": kontakt,
    "bewerbungsformular/index.html": lambda t: vorhanden(t, "zur Durchführung des Bewerbungsverfahrens"),
    "konfiguration-tueren/index.html": lambda t: vorhanden(t, "zur Bearbeitung meiner Anfrage und Erstellung eines Angebots"),
    "konfiguration-tore/index.html": lambda t: vorhanden(t, "zur Bearbeitung meiner Anfrage und Erstellung eines Angebots"),
}
for rel, fn in JOBS.items():
    p = os.path.join(ROOT, rel); t = open(p, encoding="utf-8").read(); n = fn(t)
    if n != t: open(p, "w", encoding="utf-8").write(n); print("einwilligung:", rel)
