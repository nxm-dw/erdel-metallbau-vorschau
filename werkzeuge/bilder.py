"""Stockfotos durch echte Projektfotos aus dem Kundenarchiv ersetzen und die Startseiten-Teaser
an den freigegebenen Entwurf anlehnen (Titel auf dem Bild, „+ mehr“ daneben). Idempotent."""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UP = "wp-content/uploads/"

SWAP = {
    "index.html": [
        (UP + "2022/11/erdel-metallbau-schlosser-arbeiten-leistungen.jpg", "nxm/img/zaun-lamellen.jpg"),
        (UP + "2022/11/erdel-metallbau-schlosser-arbeitenreferenzen.jpg", "nxm/img/schiebetor.jpg"),
    ],
    "leistungen/index.html": [
        (UP + "2023/02/tore-erdel-metallbau-leistungen.jpg", "nxm/img/tor-anthrazit.jpg"),
        (UP + "2023/02/briefkasten-erdel-metallbau-leistungen.jpg", "nxm/img/briefkasten.jpg"),
        (UP + "2023/02/treppen-erdel-metallbau-leistungen.jpg", "nxm/img/treppe-glas.jpg"),
        (UP + "2022/09/erdel-metallbau-referenzen-banner.jpg", "nxm/img/veredelung-edelstahl.jpg"),
        (UP + "2023/02/metallbau-arbeiten-erdel-leistungen.jpg", "nxm/img/gelaender-edelstahl.jpg"),
        (UP + "2023/02/individueller-moebelbau-leistungen-erdel-metallbau.jpg", "nxm/img/moebel-tisch.jpg"),
        (UP + "2022/09/erdel-metallbau-leistungen-banner.jpg", "nxm/img/haus-terrasse.jpg"),
    ],
}


def edit(rel, fn):
    p = os.path.join(ROOT, rel)
    t = open(p, encoding="utf-8").read()
    n = fn(t)
    if n != t:
        open(p, "w", encoding="utf-8").write(n)
        print("bilder:", rel)


for rel, pairs in SWAP.items():
    pre = "../" * rel.count("/")
    def f(t, pairs=pairs, pre=pre):
        for a, b in pairs:
            t = t.replace(pre + a, pre + b)
        return t
    edit(rel, f)


def startseite(t):
    # Historie-Teaser: eigene Sonderkonstruktion (Weltkugel) statt Stockfoto
    t = re.sub(r'(<a href="historie/">\s*<img[^>]*src=")[^"]+(")', r"\1nxm/img/weltkugel.jpg\2", t, count=1)
    # Linktext rechts neben dem Bild wie im Entwurf: „+ mehr“
    t = re.sub(r'(<a class="mt-4 more-item" href="[^"]+">)\s*<i class="icon-arrow-right2"></i>\s*([^<]+?)(\s*</a>)',
               r'\1<span aria-hidden="true">+</span> mehr<span class="visually-hidden"> zu \2</span>\3', t)
    return t


edit("index.html", startseite)


# --- Kundenfotos vom 21.10.2026 (Ordner „erdel Metallbau“ in OneDrive, importiert nach nxm/img/) ---
# Leistungen-Karten: Briefkästen, Treppen & Geländer, Weitere Metallbauarbeiten, Möbelbau auf neue Fotos
SWAP2 = {
    "leistungen/index.html": [
        ("nxm/img/briefkasten.jpg", "nxm/img/briefkasten-gold.jpg"),
        ("nxm/img/treppe-glas.jpg", "nxm/img/treppe-eiche-glas.jpg"),
        ("nxm/img/gelaender-edelstahl.jpg", "nxm/img/villa-balkon.jpg"),
        ("nxm/img/moebel-tisch.jpg", "nxm/img/moebel-schreibtisch.jpg"),
    ],
}
for rel, pairs in SWAP2.items():
    pre = "../" * rel.count("/")
    def f(t, pairs=pairs, pre=pre):
        for a, b in pairs:
            t = t.replace(pre + a, pre + b)
        return t
    edit(rel, f)

# Referenzen-Galerie: neue Fotos vorn einfügen (Reihenfolge nach Themen), vorhandene bleiben dahinter
GALERIE_NEU = [
    ("tor-schwarz-villa.jpg", "Zweiflügeliges Einfahrtstor in Schwarz vor weißer Villa"),
    ("zaun-gold-lamellen.jpg", "Lamellenzaun mit Tor und Briefkastenanlage in Gold"),
    ("eingangstor-anthrazit.jpg", "Eingangstor in Anthrazit mit Sprechanlage und Briefschlitz"),
    ("briefkasten-gold.jpg", "Briefkastenanlage in Gold mit Hausnummer"),
    ("kubus-gold.jpg", "Kubus in Gold mit Briefkasten und Hausnummer, Seitenansicht"),
    ("treppe-eiche-glas.jpg", "Kragarmtreppe aus Eiche mit Ganzglasgeländer"),
    ("treppe-glasgelaender.jpg", "Treppenhaus mit rahmenlosem Glasgeländer"),
    ("treppenauge-spiegel.jpg", "Blick ins Treppenauge mit Edelstahlgeländer"),
    ("treppe-glas-beige.jpg", "Steintreppe mit Ganzglasgeländer"),
    ("villa-balkon.jpg", "Stahlbalkon mit Vordach und Außentreppe an einer Jugendstilvilla"),
    ("balkon-glas.jpg", "Balkongeländer aus Glas mit Stahlrahmen"),
    ("balkone-stahl.jpg", "Vorgestellte Stahlbalkone an einem Mehrfamilienhaus"),
    ("terrassendach-lamellen.jpg", "Terrassenüberdachung mit Lamellen"),
    ("fassade-lamellen.jpg", "Fassade mit vertikalen Metalllamellen"),
    ("muelltonnenbox-anthrazit.jpg", "Mülltonnenboxen in Anthrazit"),
    ("muelltonnenbox-grau.jpg", "Sichtschutz und Mülltonnenboxen in Grau"),
    ("moebel-schreibtisch.jpg", "Schreibtisch aus Stahl und Nussbaum"),
    ("regal-stahl.jpg", "Regal aus schwarzem Stahl"),
]


def galerie(t):
    item = ('            <div class="col-12 col-sm-4 portfolio-item">\n'
            '                    <div class="gallery-image-container">\n'
            '                            <a href="./#" class="fl-gallery">\n'
            '                                <img decoding="async" class="img-fluid" src="../nxm/img/%s" alt="%s" loading="lazy" />\n'
            '                            </a>\n'
            '                    </div>\n'
            '                </div>\n')
    neu = "".join(item % (f, alt) for f, alt in GALERIE_NEU if "nxm/img/" + f not in t)
    if not neu:
        return t
    anker = '</h2>\n                </div>\n'
    i = t.find(anker, t.find('gallery-heading'))
    assert i > 0, "Galerie-Überschrift nicht gefunden"
    i += len(anker)
    return t[:i] + neu + t[i:]


edit("referenzen/index.html", galerie)
