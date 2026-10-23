"""Neue Kundenfotos (OneDrive „erdel Metallbau“, Okt. 2026) übernehmen und Kontaktdaten unkenntlich machen.

Aufruf:  python3 werkzeuge/fotos.py "<Ordner mit den Originalfotos>"
  - dreht nach EXIF, verkleinert auf max. 2000 px, speichert OHNE Metadaten (keine GPS-Daten) nach nxm/img/
  - zeichnet Hausnummern, Namens-/Klingelschilder, Kennzeichen und Personen weich (BLUR, relative Koordinaten)
  - wendet dieselbe Weichzeichnung auf bereits vorhandene Bilder an (Galerie, Archivfotos)
Idempotent: bearbeitete Bilder tragen den JPEG-Kommentar „nxm-unkenntlich“ und werden nicht doppelt bearbeitet.
Braucht Pillow."""
import os, sys
from PIL import Image, ImageOps, ImageFilter, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG = os.path.join(ROOT, "nxm", "img")
GAL = "wp-content/uploads/2022/10/erdel-metallbau-kelkheim-rhein-main-metallbauer-unternehmen-galerie-referenzen-{}.jpg"
MARK = b"nxm-unkenntlich"

NEU = {
    "ULI_2178tm.jpg": "tor-villa", "IMG_9326.jpg": "fassade-bronze", "IMG_6800.jpg": "balkon-altbau",
    "PHOTO-2026-08-19-11-28-26.jpg": "garagentor-verkleidet", "PHOTO-2026-08-19-11-28-25.jpg": "garagentor-verkleidet-2",
    "IMG_2604.jpeg": "pforte-anthrazit", "IMG_2609.jpeg": "muellbox-anthrazit",
    "9e48d284-8db3-472e-8c38-a5de69a9d377.JPG": "briefkasten-gold", "d8fd7cac-9882-4948-942f-f660202374dc.JPG": "muellbox-gold",
    "ULIP0355.jpg": "treppe-holz-glas", "Innengeländer 4.jpg": "treppe-licht", "Innengeländer 5.jpg": "treppenauge",
    "IMG_8425.jpg": "gelaender-glas", "IMG_7755.JPG": "balkone", "IMG_1345.jpg": "zaun-stab",
    "214f381e-d71c-4b6a-a3fb-f44192b72d69.JPG": "zaun-transporter", "3049464a-6d9b-400f-912c-31153ec850c3.JPG": "montage-transporter",
    "23183fcc-1a82-4c02-8264-e8e0cdf57292.JPG": "pergola", "ULIP0368.jpg": "sichtschutz-schraenke",
    "a622bdc0-708a-4c31-8639-4db072bd1b46.JPG": "regal-showroom", "_MG_0092.jpg": "schreibtisch",
    "1c43842d-2760-47a1-9512-2c06735450b3.JPG": "spinde-gitter", "38357dc1-c318-4730-95c6-c4a36555b927.JPG": "regal-wand",
    "IMG_1081.jpeg": "treppe-glas-2",
}

# Kopfbilder im Querformat aus den Originalen (volle Schärfe): Original -> (Datei, Fokus y von 0 bis 1)
HERO = {"ULIP0355.jpg": ("hero-treppe", 0.62), "Innengeländer 5.jpg": ("hero-treppenauge", 0.5)}

# Pfad (relativ zum Repo) -> Rechtecke (x0, y0, x1, y1) als Anteil von Breite/Höhe
BLUR = {
    "nxm/img/pforte-anthrazit.jpg": [(0.455, 0.425, 0.535, 0.555), (0.895, 0.405, 0.935, 0.535)],   # Klingel + „40“, Sprechanlage
    "nxm/img/briefkasten-gold.jpg": [(0.395, 0.30, 0.455, 0.41), (0.125, 0.25, 0.165, 0.375)],      # „5“, Klingel
    "nxm/img/zaun-transporter.jpg": [(0.855, 0.55, 0.935, 0.595), (0.215, 0.335, 0.25, 0.385), (0.695, 0.37, 0.725, 0.41)],  # Kennzeichen, Hausnr., Passant
    "nxm/img/montage-transporter.jpg": [(0.955, 0.50, 1.0, 0.70)],                                 # Klingel + Hausnr.
    "nxm/img/briefkasten.jpg": [(0.315, 0.465, 0.595, 0.635), (0.42, 0.70, 0.475, 0.74)],              # „43 b“, Namensschild
    "nxm/img/eingang-anthrazit.jpg": [(0.158, 0.488, 0.238, 0.59), (0.45, 0.34, 0.475, 0.393)],     # Briefkasten-Schilder, „4“
    "nxm/img/eingang-holztuer.jpg": [(0.845, 0.52, 0.96, 0.615), (0.405, 0.283, 0.465, 0.307)],    # „19“ + Schild, Türschild
    GAL.format(3): [(0.33, 0.47, 0.535, 0.565)],                                                  # „19“ + Namensschild
    GAL.format(14): [(0.76, 0.08, 0.98, 0.17), (0.865, 0.58, 0.935, 0.615), (0.53, 0.395, 0.605, 0.435)],  # „86 Nossa Casa“, Namensfenster, Klingel
    GAL.format(17): [(0.155, 0.215, 0.26, 0.33)],                                                 # „17“
    GAL.format(27): [(0.06, 0.31, 0.49, 0.435)],                                                  # „43 a“ + Klingel
}


def blur(im, boxes):
    w, h = im.size
    for x0, y0, x1, y1 in boxes:
        b = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        pad = max(4, int(min(b[2] - b[0], b[3] - b[1]) * 0.25))
        o = (max(0, b[0] - pad), max(0, b[1] - pad), min(w, b[2] + pad), min(h, b[3] + pad))
        part = im.crop(o)
        # erst grob vergröbern (Ziffern verlieren ihre Form), dann weich glätten
        small = part.resize((max(1, part.size[0] // 14), max(1, part.size[1] // 14)), Image.BILINEAR)
        r = max(6, int(max(part.size) / 8))
        soft = small.resize(part.size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(r))
        # weiche Kante, damit kein harter Kasten sichtbar ist
        mask = Image.new("L", part.size, 0)
        ImageDraw.Draw(mask).rectangle((b[0] - o[0], b[1] - o[1], b[2] - o[0], b[3] - o[1]), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(pad / 2))
        im.paste(Image.composite(soft, part, mask), o[:2])
    return im


def save(im, path, mark):
    kw = dict(quality=82, optimize=True, progressive=True)
    if mark:
        kw["comment"] = MARK
    im.save(path, **kw)


if len(sys.argv) > 1:
    src = sys.argv[1]
    for name, slug in NEU.items():
        im = ImageOps.exif_transpose(Image.open(os.path.join(src, name))).convert("RGB")
        im.thumbnail((2000, 2000), Image.LANCZOS)
        rel = f"nxm/img/{slug}.jpg"
        if rel in BLUR:
            im = blur(im, BLUR[rel])
        save(im, os.path.join(ROOT, rel), rel in BLUR)
        print("foto:", rel, im.size)
    for name, (slug, fy) in HERO.items():
        im = ImageOps.exif_transpose(Image.open(os.path.join(src, name))).convert("RGB")
        w, h = im.size
        ch = round(w * 9 / 16)
        y = round((h - ch) * fy)
        im = im.crop((0, y, w, y + ch)).resize((2400, 1350), Image.LANCZOS)
        save(im, os.path.join(IMG, slug + ".jpg"), False)
        print("kopfbild:", slug)

for rel, boxes in BLUR.items():
    p = os.path.join(ROOT, rel)
    im = Image.open(p)
    if MARK in (im.info.get("comment") or b""):
        continue
    im = blur(ImageOps.exif_transpose(im).convert("RGB"), boxes)
    save(im, p, True)
    print("unkenntlich:", rel)
