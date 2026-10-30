"""Einmaliger HTML-Umbau der gespiegelten Erdel-Seiten: neuer Kopf, Vollbild-Menü,
mobile Aktionsleiste, neuer Fuß, Textkorrekturen. Idempotent über Marker."""
import os, re, glob, html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEL, TEL_TXT = "+49619563192", "06195 63192"
MAIL = "info@erdel-metallbau.de"
WA = "https://wa.me/49619563192"
U = "wp-content/uploads/"

MENU = [
    ("Start", "", U + "2022/07/header.jpg"),
    ("Referenzen", "referenzen/", "nxm/img/zaun-lamellen.jpg"),
    ("Leistungen", "leistungen/", "nxm/img/tor-anthrazit.jpg"),
    ("Hörmann", "hoermann/", U + "2022/10/garagentor-garage-metallbau-erdel-hoermann.jpg"),
    ("Historie", "historie/", "nxm/img/balkon-altbau.jpg"),
    ("Jobs", "jobs/", U + "2022/09/erdel-metallbau-background-mitarbeiter.jpg"),
    ("Kontakt", "kontakt/", "nxm/img/haus-terrasse.jpg"),
]

ICON = {
    "tel": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2c0 1.3.9 2.5 1 2.7.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18c.6 0 1 .4 1 1v12c0 .6-.4 1-1 1H3a1 1 0 0 1-1-1V6c0-.6.4-1 1-1zm9 7.3L4 7.2V17h16V7.2l-8 5.1zM5.2 7l6.8 4.3L18.8 7H5.2z"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.2 5.3 19.9 12l-6.7 6.7-1.4-1.4 4.3-4.3H4v-2h12.1l-4.3-4.3z"/></svg>',
}


def header(p, current):
    """Kopf und Menü im Stil des freigegebenen Entwurfs: Logo rechts, zwei Striche,
    Menü als abgedunkeltes Vollbildfoto mit schlichter Liste links."""
    cur_i = next((i for i, (_, h, _) in enumerate(MENU) if h == current), 0)
    items = []
    for i, (label, href, img) in enumerate(MENU):
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li style="--i:{i}"><a href="{p}{href}index.html" data-nxm-img="{i}"{cur}>{label}</a></li>')
    bgs = "".join(
        f'<img src="{p}{img}" alt="" decoding="async" data-nxm-img="{i}"{" class=is-active" if i == cur_i else ""}>'
        for i, (_, _, img) in enumerate(MENU)
    )
    return f"""<!-- nxm:header -->
<a class="nxm-skip" href="#content">Zum Inhalt springen</a>
<header class="nxm-head" id="nxm-head">
  <div class="nxm-head__right">
    <a class="nxm-head__tel" href="tel:{TEL}">{ICON["tel"]}<span>{TEL_TXT}</span></a>
    <button class="nxm-burger" type="button" aria-expanded="false" aria-controls="nxm-menu" aria-label="Menü öffnen">
      <span class="nxm-burger__icon" aria-hidden="true"><i></i><i></i></span>
    </button>
    <a class="nxm-head__logo" href="{p}index.html" aria-label="erdel metallbau – zur Startseite">
      <img src="{p}wp-content/themes/erdel/assets/images/logo.svg" alt="erdel metallbau" width="170" height="52">
    </a>
  </div>
</header>
<div class="nxm-menu" id="nxm-menu" role="dialog" aria-modal="true" aria-label="Hauptmenü" aria-hidden="true">
  <div class="nxm-menu__bg" aria-hidden="true">{bgs}</div>
  <div class="nxm-menu__inner">
    <nav class="nxm-menu__nav" aria-label="Hauptnavigation"><ul>{"".join(items)}</ul></nav>
    <a class="nxm-menu__cta" href="{p}kontakt/index.html"><span aria-hidden="true">&gt;</span> Kontaktformular</a>
  </div>
  <div class="nxm-menu__foot">
    <p>Auf der Herrnmauer 12, 65779 Kelkheim im Taunus<br>
      <a href="tel:{TEL}">+49 (0) 6195-63192</a> · <a href="mailto:{MAIL}">{MAIL}</a> · <a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></p>
    <p class="nxm-menu__legal"><a href="{p}impressum/index.html">Impressum</a><a href="{p}datenschutzerklaerung/index.html">Datenschutz</a></p>
  </div>
  <p class="nxm-menu__claim" aria-hidden="true">geradlinig<br>modern<br>individuell</p>
</div>
<!-- /nxm:header -->
"""


def actionbar(p):
    return f"""<!-- nxm:actions -->
<nav class="nxm-actions" aria-label="Schnellkontakt">
  <a href="tel:{TEL}">{ICON["tel"]}<span>Anrufen</span></a>
  <a href="{WA}" target="_blank" rel="noopener">{ICON["wa"]}<span>WhatsApp</span></a>
  <a href="{p}kontakt/index.html" class="is-primary">{ICON["mail"]}<span>Anfrage</span></a>
</nav>
<!-- /nxm:actions -->"""


def footer(p):
    nav = "".join(f'<li><a href="{p}{h}index.html">{l}</a></li>' for l, h, _ in MENU)
    return f"""<!-- nxm:footer -->
<footer class="nxm-foot">
  <div class="nxm-foot__inner">
    <div class="nxm-foot__brand">
      <img src="{p}wp-content/themes/erdel/assets/images/logo.svg" alt="erdel metallbau" width="190" height="58" loading="lazy">
      <p>Tore, Geländer, Treppen und Unikate aus Metall. Gefertigt in Kelkheim im Taunus, seit 1925.</p>
      <a class="nxm-btn nxm-btn--light" href="{p}kontakt/index.html">Projekt anfragen {ICON["arrow"]}</a>
    </div>
    <div class="nxm-foot__col">
      <p class="nxm-eyebrow">Kontakt</p>
      <address>erdel metallbau GmbH<br>Auf der Herrnmauer 12<br>65779 Kelkheim im Taunus</address>
      <a href="tel:{TEL}">{TEL_TXT}</a><br>
      <a href="mailto:{MAIL}">{MAIL}</a><br>
      <a href="{WA}" target="_blank" rel="noopener">WhatsApp schreiben</a>
    </div>
    <div class="nxm-foot__col">
      <p class="nxm-eyebrow">Geschäftszeiten</p>
      <p>Montag bis Donnerstag<br>8:00 bis 16:30 Uhr</p>
      <p>Freitag<br>8:00 bis 13:00 Uhr</p>
    </div>
    <div class="nxm-foot__col">
      <p class="nxm-eyebrow">Seiten</p>
      <ul>{nav}</ul>
    </div>
  </div>
  <div class="nxm-foot__bar">
    <span>© 2026 erdel metallbau GmbH</span>
    <span><a href="{p}impressum/index.html">Impressum</a><a href="{p}datenschutzerklaerung/index.html">Datenschutz</a></span>
  </div>
</footer>
<!-- /nxm:footer -->"""


FORM_HINT = ('<p class="nxm-form-hint">Ihre Angaben verwenden wir nur, um Ihre Anfrage zu bearbeiten. '
             'Details finden Sie in unserer <a href="{p}datenschutzerklaerung/index.html">Datenschutzerklärung</a>.</p>')

TEXTFIXES = [
    ("Refernzen", "Referenzen"),
    ("geradlining modern individuell", "geradlinig modern individuell"),
    ("Ein Paar Worte", "Ein paar Worte"),
    ("tel:tel:", "tel:"),
]


def teaser_mobile(t):
    """Teaser der Startseite: Überschrift auch mobil zeigen (sonst nur Pille mit Linktext)."""
    marker = '<div class="container-fluid gx-0 malu-1 position-relative">'
    parts = t.split(marker)
    for k in range(1, len(parts)):
        block = parts[k]
        h2 = re.search(r"<h2[^>]*>(.*?)</h2>", block, re.S)
        if not h2 or "nxm-teaser" in block:
            continue
        title = h2.group(1).strip()
        parts[k] = re.sub(
            r'<div class="bg-item[^"]*">\s*<a class="mt-4" href="([^"]+)">\s*<i class="icon-arrow-right2"></i>\s*([^<]+?)\s*</a>',
            lambda n: (f'<div class="bg-item nxm-teaser"><a href="{n.group(1)}">'
                       f'<span class="nxm-teaser__title">{title}</span>'
                       f'<span class="nxm-teaser__link">{ICON["arrow"]}{n.group(2).strip()}</span></a>'),
            block, count=1)
    return marker.join(parts)


for f in sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith(("wp-", "nxm", "werkzeuge")):
        continue
    depth = rel.count(os.sep)
    p = "../" * depth
    current = "" if depth == 0 else os.path.dirname(rel) + "/"
    t = open(f, encoding="utf-8").read()
    o = t

    if "nxm:header" in t:
        a = t.index("<!-- nxm:header -->"); b = t.index("<!-- /nxm:header -->") + len("<!-- /nxm:header -->\n")
        t = t[:a] + header(p, current) + t[b:]
    if "nxm:header" not in t:
        s = t.find('<div class="container sticky">')
        e = t.find('<div id="content"')
        assert s > 0 and e > s, rel
        t = t[:s] + header(p, current) + t[e:]
        # Alter Fuß samt Social-Leiste -> neuer Fuß + Aktionsleiste
        s = t.find('<footer id="page-footer"')
        e = t.find("</footer>", s) + len("</footer>")
        assert s > 0 and e > s, rel
        t = t[:s] + footer(p) + "\n" + actionbar(p) + t[e:]
        t = t.replace("</head>",
                      f'<link rel="preload" href="{p}nxm/fonts/oxygen-300-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
                      f'<link rel="stylesheet" href="{p}nxm/nxm.css?v=1">\n<meta name="theme-color" content="#141414">\n</head>', 1)
        t = t.replace("</body>", f'<script src="{p}nxm/nxm.js?v=1" defer></script>\n</body>', 1)
        has_hero = "featured-full-width-img" in t
        t = re.sub(r'<body class="', f'<body class="{"nxm-hero" if has_hero else "nxm-nohero"} ', t, count=1)
        # Leere Kommentar-Container und tote Rückgabe-Knöpfe entfernen
        t = t.replace('<div id="comments" class="comment-content">\n    \n    \n    </div>', "")

    t = re.sub(r'<h1></h1>(\s*<!--<h1 class="main-title text-right">(.*?)</h1>-->)',
               lambda m: f'<h1>{m.group(2)}</h1>{m.group(1)}', t)
    for a, b in TEXTFIXES:
        t = t.replace(a, b)
    if depth == 0:
        t = teaser_mobile(t)
    if current == "kontakt/" and "nxm-form-hint" not in t:
        t = re.sub(r"(</form>)", r"\1" + FORM_HINT.format(p=p), t, count=1)
    # Bildbeschreibungen: generische Alt-Texte aus dem Titel ableiten
    t = re.sub(r'alt="erdel-metallbau" title="([^"]+)"',
               lambda m: f'alt="{html.escape(m.group(1).strip())}" title="{m.group(1)}"', t)
    t = re.sub(r'alt="" title="([a-z0-9-]+)"',
               lambda m: 'alt="{}" title="{}"'.format(
                   m.group(1).replace("-erdel-metallbau", "").replace("-leistungen", "").replace("erdel-metallbau-", "")
                   .replace("-", " ").strip().capitalize(), m.group(1)), t)

    if t != o:
        open(f, "w", encoding="utf-8").write(t)
        print("umgebaut:", rel)
