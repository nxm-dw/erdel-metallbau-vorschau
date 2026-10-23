"""Zweite Bildrunde (Okt. 2026): restliche Stockfotos seitenweit durch echte Projektfotos ersetzen
und die Referenzen-Galerie um die neuen Projekte erweitern. Nach fotos.py und vor seiten.py laufen lassen.
Idempotent (reine Pfadersetzung, Galerie über Marker nxm:galerie-neu)."""
import os, glob
from PIL import Image, ImageOps

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UP = "wp-content/uploads/"

# Stockfoto -> echtes Projektfoto, auf allen Seiten (auch Menü-Hintergründe)
SWAP = [
    (UP + "2022/07/header.jpg", "nxm/img/tor-villa.jpg"),
    (UP + "2022/10/garagentor-garage-metallbau-erdel-hoermann.jpg", "nxm/img/eingang-anthrazit.jpg"),
    (UP + "2022/09/erdel-metallbau-background-mitarbeiter.jpg", "nxm/img/montage-transporter.jpg"),
    (UP + "2022/11/erdel-metallbau-schlosser-arbeiten-jobs.jpg", "nxm/img/zaun-transporter.jpg"),
    (UP + "2022/09/erdel-metalbau-historie-banner.jpg", "nxm/img/balkon-altbau.jpg"),
    (UP + "2022/10/hoermann-garage-erdel-metallbau.jpg", "nxm/img/garagentor-verkleidet-2.jpg"),
    (UP + "2022/10/erdel-metallbau-hoermann-haustuere.jpg", "nxm/img/eingang-holztuer.jpg"),
    (UP + "2022/10/hoermann-tore-erdel-metallbau-garage.jpg", "nxm/img/tor-villa.jpg"),
    (UP + "2022/10/garagentor-erdel-metallbau-hoermann-schwarz.jpg", "nxm/img/garagentor-verkleidet-2.jpg"),
    (UP + "2022/09/erdel-metallbau-referenzen-banner.jpg", "nxm/img/fassade-bronze.jpg"),
    (UP + "2022/08/headerteam.jpg", "nxm/img/zaun-transporter.jpg"),
    ("nxm/img/briefkasten.jpg", "nxm/img/briefkasten-gold.jpg"),
]

# neue Galeriebilder: Datei, Alternativtext, Bildausschnitt (Fokus x, y von 0 bis 1)
GALERIE = [
    ("treppe-holz-glas", "Freitragende Holztreppe mit Glasgeländer", (0.5, 0.5)),
    ("briefkasten-gold", "Briefkasten- und Müllboxanlage in Messingoptik", (0.45, 0.5)),
    ("treppe-licht", "Treppenauge mit Glasbrüstung und Lichtakzent", (0.5, 0.5)),
    ("gelaender-glas", "Ganzglasbrüstung an einer Terrasse", (0.5, 0.5)),
    ("tor-villa", "Zweiflügeliges Einfahrtstor mit Pforte", (0.35, 0.5)),
    ("treppenauge", "Blick ins Treppenauge mit Glasgeländer", (0.5, 0.5)),
    ("pergola", "Lamellendach über der Terrasse", (0.5, 0.5)),
    ("balkone", "Balkonanlage mit Stahlgeländern", (0.6, 0.5)),
    ("muellbox-gold", "Müllboxen mit Messingfronten", (0.45, 0.5)),
    ("zaun-stab", "Stabzaun in Anthrazit entlang eines Weges", (0.35, 0.5)),
    ("garagentor-verkleidet", "Garagentor mit flächenbündiger Verkleidung", (0.45, 0.5)),
    ("fassade-bronze", "Fassadenverkleidung aus bronzefarbenen Lamellen", (0.75, 0.5)),
    ("balkon-altbau", "Stahlbalkon mit Außentreppe an einer Altbauvilla", (0.5, 0.5)),
    ("regal-showroom", "Regalsystem aus Stahl im Showroom", (0.5, 0.5)),
    ("pforte-anthrazit", "Pforte mit Sprechanlage, Anthrazit", (0.55, 0.5)),
    ("sichtschutz-schraenke", "Sichtschutzwand mit integrierten Schränken", (0.7, 0.5)),
    ("spinde-gitter", "Schrankfronten aus Streckmetall", (0.5, 0.5)),
    ("muellbox-anthrazit", "Müllboxen in Anthrazit mit Griffleisten", (0.5, 0.5)),
    ("schreibtisch", "Schreibtisch mit Stahlwange", (0.6, 0.5)),
    ("regal-wand", "Wandregal aus Stahl", (0.5, 0.5)),
]


def crop(slug, focus):
    out = os.path.join(ROOT, "nxm", "img", "galerie", slug + ".jpg")
    if os.path.exists(out):
        return
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im = ImageOps.exif_transpose(Image.open(os.path.join(ROOT, "nxm", "img", slug + ".jpg"))).convert("RGB")
    w, h = im.size
    tw, th = (w, round(w * 8 / 7)) if w * 8 / 7 <= h else (round(h * 7 / 8), h)
    x = min(max(0, round(focus[0] * w - tw / 2)), w - tw)
    y = min(max(0, round(focus[1] * h - th / 2)), h - th)
    im = im.crop((x, y, x + tw, y + th)).resize((700, 800), Image.LANCZOS)
    im.save(out, quality=80, optimize=True, progressive=True)


for slug, _, focus in GALERIE:
    crop(slug, focus)

for p in [os.path.join(ROOT, "index.html")] + sorted(glob.glob(os.path.join(ROOT, "*", "index.html"))):
    if "/wp-" in p or "/werkzeuge/" in p:
        continue
    t = open(p, encoding="utf-8").read()
    n = t
    for a, b in SWAP:
        n = n.replace(a, b)
    if p.endswith("referenzen/index.html") and "nxm:galerie-neu" not in n:
        items = "".join(f"""
                <div class="col-12 col-sm-4 portfolio-item">
                    <div class="gallery-image-container">
                            <a href="./#" class="fl-gallery">
                                <img decoding="async" loading="lazy" class="img-fluid" src="../nxm/img/galerie/{s}.jpg" title="{alt}" alt="{alt}" />
                            </a>
                    </div>
                </div>""" for s, alt, _ in GALERIE)
        anchor = '<div class="col-12 col-sm-4 portfolio-item">'
        i = n.find(anchor)
        assert i > 0, "Galerie nicht gefunden"
        n = n[:i] + "<!-- nxm:galerie-neu -->" + items + "\n<!-- /nxm:galerie-neu -->\n                " + n[i:]
    if n != t:
        open(p, "w", encoding="utf-8").write(n)
        print("bilder_neu:", os.path.relpath(p, ROOT))
