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
    # Historie-Teaser: Altbauvilla mit Stahlbalkon (Kundenwunsch 30.10.2026, vorher Weltkugel)
    t = re.sub(r'(<a href="historie/">\s*<img[^>]*src=")[^"]+(")', r"\1nxm/img/balkon-altbau.jpg\2", t, count=1)
    # Linktext rechts neben dem Bild wie im Entwurf: „+ mehr“
    t = re.sub(r'(<a class="mt-4 more-item" href="[^"]+">)\s*<i class="icon-arrow-right2"></i>\s*([^<]+?)(\s*</a>)',
               r'\1<span aria-hidden="true">+</span> mehr<span class="visually-hidden"> zu \2</span>\3', t)
    return t


edit("index.html", startseite)
