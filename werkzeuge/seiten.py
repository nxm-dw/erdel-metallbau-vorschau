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


def kontakt(t):
    s = t.find("<form"); e = t.find("</form>") + len("</form>")
    form = t[s:e]
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
        <img src="{P}wp-content/uploads/2022/10/garagentor-erdel-metallbau-hoermann-schwarz.jpg" alt="Hörmann-Garagentor" loading="lazy">
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


BEWERBEN = f"""
<section class="x-cta">
  <img src="{P}nxm/img/gelaender-edelstahl.jpg" alt="" loading="lazy">
  <div class="x-wrap x-cta__inner">
    <div>
      <p class="x-eyebrow x-eyebrow--light">Initiativbewerbung</p>
      <h2>Nichts Passendes dabei? Wir freuen uns trotzdem auf&nbsp;dich.</h2>
      <p>Sende uns deine digitale Bewerbung mit deinem Portfolio an <a href="mailto:{MAIL}">{MAIL}</a> oder per Post an erdel metallbau, Auf der Herrnmauer 12, 65779 Kelkheim im&nbsp;Taunus.</p>
    </div>
    <div class="x-cta__actions">
      <a class="nxm-btn nxm-btn--light" href="{P}bewerbungsformular/">Jetzt bewerben {ARROW}</a>
      <a class="nxm-btn nxm-btn--ghost" href="tel:{TEL}">{I_TEL} {TEL_TXT}</a>
    </div>
  </div>
</section>
"""

BENEFITS = """
    <ul class="x-benefits">
      <li><span class="x-benefits__no">01</span><strong>Ein starkes Team</strong><span>Ein tolles, bunt gemischtes Team, in dem man sich aufeinander verlassen&nbsp;kann.</span></li>
      <li><span class="x-benefits__no">02</span><strong>Verantwortung</strong><span>Eine interessante, eigenverantwortliche Position mit Raum für eigene&nbsp;Ideen.</span></li>
      <li><span class="x-benefits__no">03</span><strong>Abwechslung</strong><span>Abwechslungsreiche Projekte, bei denen du dich kreativ ausleben&nbsp;kannst.</span></li>
    </ul>"""


def bewerbung_block(form, stellen_link):
    """Formularblock der Bewerbung (Seitenleiste + Forminator-Formular), auf Jobs- und Bewerbungsseite gleich."""
    return f"""
<section class="x-section x-formsec x-section--flush" id="bewerbung">
  <div class="x-wrap x-formgrid">
    <aside class="x-formside">
      <img src="{P}nxm/img/gelaender-edelstahl.jpg" alt="" loading="lazy">
      <div class="x-formside__body">
        <p class="x-eyebrow x-eyebrow--light">So geht's</p>
        <h2>In drei&nbsp;Schritten</h2>
        <ol class="x-steps">
          <li><strong>Angaben eintragen</strong><span>Name, Telefon und&nbsp;E&#8209;Mail.</span></li>
          <li><strong>Unterlagen hochladen</strong><span>Lebenslauf, gerne auch Zeugnisse oder&nbsp;Portfolio.</span></li>
          <li><strong>Absenden</strong><span>Gerne mit ein paar Worten zu&nbsp;dir.</span></li>
        </ol>
        <p class="x-formside__hint">Lieber per E-Mail oder Post? Sende deine Bewerbung an <a href="mailto:{MAIL}">{MAIL}</a> oder an erdel metallbau, Auf der Herrnmauer 12, 65779 Kelkheim im Taunus. <a href="{stellen_link}">Zu den offenen&nbsp;Stellen</a></p>
      </div>
    </aside>
    <div class="x-formcard">
      <div class="x-formcard__head"><h2>Deine&nbsp;Bewerbung</h2><p class="x-formcard__req"><span aria-hidden="true">*</span> Pflichtfeld</p></div>
      {form}
    </div>
  </div>
</section>
"""


def bewerbungsformular_markup():
    """Das Forminator-Bewerbungsformular aus der Bewerbungsseite (inkl. Datenschutz-Pflichtfeld)."""
    t = open(os.path.join(ROOT, "bewerbungsformular/index.html"), encoding="utf-8").read()
    s = t.find("<form"); e = t.find("</form>") + len("</form>")
    return t[s:e]


STELLEN = [
    ("Kalkulator (m/w/d) im Metallbau", "Kalkulator (m/w/d) im&nbsp;Metallbau",
     "Technische Beratung unter Berücksichtigung bautechnischer&nbsp;Anforderungen.", "wp-content/uploads/2022/07/arbeit.jpg"),
    ("Fachkraft für Metallbau / Schlosser:in (m/w/d)", "Fachkraft für Metallbau / Schlosser:in&nbsp;(m/w/d)",
     "Anfertigung technischer Zeichnungen und maschinelle Fertigung in unserer&nbsp;Werkstatt.", "wp-content/uploads/2022/07/welder-ga36fb2b9b_640.jpg"),
]


def jobs(t):
    karten = "".join(f"""
      <article class="x-job">
        <a class="x-job__media" href="{P}kalkulator-job1/" tabindex="-1" aria-hidden="true"><img src="{P}{img}" alt="" loading="lazy"></a>
        <div class="x-job__body">
          <p class="x-job__tags"><span>m/w/d</span><span>Kelkheim im Taunus</span></p>
          <h3 class="x-job__title"><a href="{P}kalkulator-job1/">{titel}</a></h3>
          <p class="x-job__text">{text}</p>
        </div>
        <div class="x-job__actions">
          <a class="nxm-btn nxm-btn--dark" href="#bewerbung" data-stelle="{name}">Jetzt bewerben {ARROW}</a>
          <a class="x-job__go" href="{P}kalkulator-job1/">Details zur Stelle {ARROW}</a>
        </div>
      </article>""" for name, titel, text, img in STELLEN)
    cta = BEWERBEN.replace(f'href="{P}bewerbungsformular/"', 'href="#bewerbung"')
    return f"""
<section class="x-section x-intro">
  <div class="x-wrap x-split x-split--wide">
    <div>
      <p class="x-eyebrow">Karriere bei erdel</p>
      <h2 class="x-display">Handwerk mit Anspruch. Seit&nbsp;1925.</h2>
      <p class="x-lead">Du hast Interesse an einer Tätigkeit bei erdel metallbau? Hier findest du unsere offenen Stellen und kannst dich direkt&nbsp;bewerben.</p>
      <div class="x-cta__actions x-intro__actions">
        <a class="nxm-btn nxm-btn--dark" href="#bewerbung">Jetzt bewerben {ARROW}</a>
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
    <p class="x-eyebrow">Offene Stellen</p>
    <div class="x-jobs">{karten}
    </div>
  </div>
</section>

<section class="x-section x-section--stone">
  <div class="x-wrap">
    <p class="x-eyebrow">Das bieten wir dir</p>
    <h2 class="x-h2">Warum erdel&nbsp;metallbau?</h2>
    {BENEFITS}
  </div>
</section>
{cta}
{bewerbung_block(bewerbungsformular_markup(), "#stellen")}
"""


def stelle(t):
    return f"""
<section class="x-section x-intro">
  <div class="x-wrap">
    <p class="x-eyebrow">Stellenangebot</p>
    <h2 class="x-display x-display--md">Metallbauer, Fachrichtung Konstruktions&shy;technik&nbsp;(m/w/d)</h2>
    <p class="x-tags"><span>Vollzeit</span><span>Teilzeit</span><span>geringfügige Beschäftigung</span><span>Kelkheim im Taunus</span></p>
    <p class="x-lead"><mark class="nxm-todo">Stellenbeschreibung folgt: Auf der bisherigen Seite steht hier noch Blindtext. Bitte Aufgaben und Tätigkeiten vom Kunden&nbsp;liefern lassen.</mark></p>
    <p class="x-lead">Wenn du dir das vorstellen kannst, bewirb dich bei&nbsp;uns!</p>
    <div class="x-cta__actions x-intro__actions">
      <a class="nxm-btn nxm-btn--dark" href="{P}bewerbungsformular/?stelle=Metallbauer%20Konstruktionstechnik%20(m/w/d)">Jetzt bewerben {ARROW}</a>
      <a class="nxm-btn nxm-btn--outline" href="{P}jobs/#stellen">Alle Stellen</a>
    </div>
  </div>
</section>

<section class="x-section x-section--stone">
  <div class="x-wrap x-two">
    <div>
      <h2 class="x-h3">Das bringst du&nbsp;mit</h2>
      <ul class="x-check">
        <li>Abgeschlossene Berufsausbildung als Metallbauer/in</li>
        <li>Gute Fachkenntnis</li>
        <li>Freundliche Umgangsformen</li>
        <li>Selbstständiges Arbeiten</li>
      </ul>
    </div>
    <div>
      <h2 class="x-h3">Das bieten wir&nbsp;dir</h2>
      <ul class="x-check">
        <li>Ein tolles, bunt gemischtes Team</li>
        <li>Eine interessante, eigenverantwortliche Position</li>
        <li>Abwechslungsreiche Projekte, bei denen du dich kreativ ausleben&nbsp;kannst</li>
      </ul>
    </div>
  </div>
</section>
{BEWERBEN.replace("Nichts Passendes dabei? Wir freuen uns trotzdem auf&nbsp;dich.", "Wenn dein Herz gerade ein bisschen schneller schlägt, möchten wir von dir&nbsp;hören.").replace("Initiativbewerbung", "Bewerbung")}
"""


GEN = [
    ("1925", "1. Generation", "Gründung durch Clemens&nbsp;Erdel",
     "Im Jahr 1925 machte sich Clemens Erdel, gelernter Dreher, in einer kleinen Werkstatt in Kelkheim selbstständig. Kelkheim wurde immer mehr für seine Möbelindustrie bekannt. Für Schreinereien wurden im eigenen Betrieb Leimöfen, Band- und Tellerschleifmaschinen sowie Furnierpressen gebaut. Besonders die Furnierpressen aus eigener Herstellung waren, nicht nur in Kelkheim, bekannt und&nbsp;begehrt.",
     "wp-content/uploads/2022/07/historie_1.jpg"),
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
      <figure class="x-tl__media"><img src="{P}{img}" alt="{g}: {sub.replace('&nbsp;', ' ')}" loading="lazy"></figure>
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
      <h2>Über 100 Jahre Erfahrung für Ihr&nbsp;Unikat.</h2>
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
    check=["Anschrift inkl. Telefonnummer und&nbsp;E&#8209;Mail&#8209;Adresse", "Zwei Fotos der bestehenden Haustür (innen und außen)", "Höhe und Breite", "Türvariante", "Gewünschtes Motiv bzw. gewünschte Farbe", "Bei Neubauten: Bauplan mit Maßen&nbsp;(optional)"],
    downloads=[("Katalog Aluminium-Haustüren", UP + "Katalog_Aluminium_Haustueren.pdf"), ("Hörmann-Vorzugsfarben", UP + "HOeRMANN_Vorzugsfarben.pdf"), ("Aufmaßblatt", UP + "Aufmassblatt.pdf")],
    kfw=UP + "KFW-Zuschuss-bei-RC2-Sicherheitsausstattung-1.pdf",
    step3=("Ihr Angebot", "Sobald alle Informationen vorliegen, erstellen wir Ihr individuelles&nbsp;Angebot.")),
  "konfiguration-tore/index.html": dict(
    art="Tore", title="Qualitätsprodukte nach Ihren&nbsp;Vorstellungen", img="nxm/img/tor-anthrazit.jpg", hero=UP + "hoermann-tore-erdel-metallbau-garage.jpg", claim="Tore nach&nbsp;Maß",
    lead="Die langjährige Partnerschaft des Systemhauses HÖRMANN und erdel metallbau zeichnet sich durch Qualität, Zuverlässigkeit und Vertrauen aus. Unsere Kunden profitieren von individuellen Lösungen und einer unschlagbaren&nbsp;Produktqualität.",
    sub="Industrietore und&nbsp;Antriebe", sub2="Hier schwingt Qualität in schöner&nbsp;Optik",
    text="Alles spricht für das Original: Qualität und Sicherheit, Optik und Komfort und die ausgereifte Technik. In jedem Hörmann-Tor steckt die Erfahrung von über 50 Jahren Know-how im Bau von&nbsp;Garagentoren.",
    check=["Anschrift inkl. Telefonnummer und&nbsp;E&#8209;Mail&#8209;Adresse", "Zwei Fotos der bestehenden Garage (innen und außen)", "Maße laut Aufmaßblatt", "Wunschfarbe: Standard ist Verkehrsweiß RAL 9016, weitere Hörmann-Vorzugsfarben im&nbsp;Download", "Größe der Sektionen und Wunsch der Oberfläche", "Ist ein Antrieb gewünscht?", "Bei Neubauten: Bauplan mit&nbsp;Maßen"],
    downloads=[("Aufmaßblatt", UP + "Aufmassblatt.pdf"), ("Hörmann-Vorzugsfarben", UP + "HOeRMANN_Vorzugsfarben-1.pdf"), ("Größe der Sektionen", UP + "HOeRMANN-Sektionaltor-Sektionen.pdf"), ("Oberflächen", UP + "HOeRMANN-Oberflaechen.pdf")],
    kfw=UP + "KFW-Zuschuss-bei-RC2-Sicherheitsausstattung.pdf",
    step3=("Termin vor Ort &amp; Angebot", "Wir nehmen die genauen Aufmaße, beraten Sie persönlich und erstellen Ihr&nbsp;Angebot.")),
}


def konfig_for(rel):
    d = KONFIG[rel]
    def fn(t):
        s = t.find("<form"); e = t.find("</form>") + len("</form>")
        form = t[s:e]
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
      <li><span class="x-steps3__no">02</span><strong>Anfrage senden</strong><span>Drei kurze Schritte: Projekt, Wünsche, Kontakt. Fotos laden Sie direkt mit&nbsp;hoch.</span></li>
      <li><span class="x-steps3__no">03</span><strong>{d['step3'][0]}</strong><span>{d['step3'][1]}</span></li>
    </ol>
  </div>
</section>

<section class="x-section x-section--stone">
  <div class="x-wrap x-two x-two--konf">
    <div>
      <p class="x-eyebrow">Checkliste</p>
      <h2 class="x-h3">Das brauchen wir von&nbsp;Ihnen</h2>
      <ul class="x-check">{checks}</ul>
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
          <li><strong>Daten eintragen</strong><span>Name, Anschrift und&nbsp;Kontakt.</span></li>
          <li><strong>Wünsche angeben</strong><span>Farbe, Maße und gewünschte&nbsp;Ausführung.</span></li>
          <li><strong>Dateien hochladen</strong><span>Fotos, Aufmaßblatt oder&nbsp;Konfiguration.</span></li>
        </ol>
        <p class="x-formside__hint">Erst wenn alle Informationen vorliegen, können wir ein passendes Angebot erstellen. Bei Rückfragen erreichen Sie uns unter <a href="tel:{TEL}">{TEL_TXT}</a>.</p>
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


def bewerbung(t):
    s = t.find("<form"); e = t.find("</form>") + len("</form>")
    form = t[s:e]
    return f"""
<section class="x-section x-intro x-intro--compact">
  <div class="x-wrap">
    <p class="x-eyebrow">Bewerbung</p>
    <h1 class="x-display">Jetzt online&nbsp;bewerben</h1>
    <p class="x-lead">Schick uns deine Unterlagen direkt über das Formular. Lebenslauf, Zeugnisse oder Portfolio kannst du als Datei&nbsp;hochladen.</p>
  </div>
</section>
{bewerbung_block(form, P + "jobs/#stellen")}
"""


PAGES = {"kontakt/index.html": kontakt, "jobs/index.html": jobs, "historie/index.html": historie, "kalkulator-job1/index.html": stelle,
         "konfiguration-tueren/index.html": konfig_for("konfiguration-tueren/index.html"),
         "konfiguration-tore/index.html": konfig_for("konfiguration-tore/index.html"),
         "bewerbungsformular/index.html": bewerbung}

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
