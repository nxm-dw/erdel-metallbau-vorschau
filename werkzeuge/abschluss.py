"""Einheitliches Abschlussband (CTA) für Referenzen, Leistungen und Hörmann; ersetzt auf
Referenzen den alten „Jetzt anfragen“-Teaser samt leerer Blöcke. Idempotent über nxm:abschluss."""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.2 5.3 19.9 12l-6.7 6.7-1.4-1.4 4.3-4.3H4v-2h12.1l-4.3-4.3z"/></svg>'
I_TEL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>'


def band(img, eyebrow, title, links):
    btns = "".join(links)
    return f"""<!-- nxm:abschluss -->
<section class="x-cta x-cta--end">
  <img src="../{img}" alt="" loading="lazy">
  <div class="x-wrap x-cta__inner">
    <div>
      <p class="x-eyebrow x-eyebrow--light">{eyebrow}</p>
      <h2>{title}</h2>
    </div>
    <div class="x-cta__actions">{btns}</div>
  </div>
</section>
<!-- /nxm:abschluss -->
"""


ANFRAGE = f'<a class="nxm-btn nxm-btn--light" href="../kontakt/">Projekt anfragen {ARROW}</a>'
TEL = f'<a class="nxm-btn nxm-btn--ghost" href="tel:+49619563192">{I_TEL} 06195 63192</a>'

PAGES = {
    "referenzen/index.html": band("nxm/img/haus-terrasse.jpg", "Ihr Projekt", "Ihr Unikat ist das nächste&nbsp;Projekt.", [ANFRAGE, TEL]),
    "leistungen/index.html": band("nxm/img/zaun-lamellen.jpg", "Beratung", "Sprechen wir über Ihre&nbsp;Idee.",
                                  [ANFRAGE, '<a class="nxm-btn nxm-btn--ghost" href="../referenzen/">Referenzen ansehen</a>']),
    "hoermann/index.html": band("wp-content/uploads/2022/10/hoermann-tore-erdel-metallbau-garage.jpg", "Hörmann bei erdel",
                                "Ihr Wunschtor, fachgerecht&nbsp;montiert.",
                                [f'<a class="nxm-btn nxm-btn--light" href="../konfiguration-tore/">Tor konfigurieren {ARROW}</a>',
                                 '<a class="nxm-btn nxm-btn--ghost" href="../konfiguration-tueren/">Tür konfigurieren</a>']),
}

for rel, html in PAGES.items():
    p = os.path.join(ROOT, rel)
    t = open(p, encoding="utf-8").read()
    if "nxm:abschluss" in t:
        continue
    if rel.startswith("referenzen"):
        # alten Anfrage-Teaser und die beiden leeren Inhaltsblöcke entfernen
        t, n = re.subn(r'<div class="container-fluid gx-0 malu-1 position-relative">(?:(?!malu-1).)*?Jetzt&nbsp;anfragen!.*?'
                       r'<div class="content-width-100 content-align-left">\s*<p></p>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>',
                       "", t, count=1, flags=re.S)
        assert n == 1, "Referenzen-Teaser nicht gefunden"
    i = t.find('<footer class="main-footer">')
    assert i > 0, rel
    t = t[:i] + html + t[i:]
    open(p, "w", encoding="utf-8").write(t)
    print("abschluss:", rel)
