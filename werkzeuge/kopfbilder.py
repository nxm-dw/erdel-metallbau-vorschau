"""Kopfbilder (Hero) je Seite festlegen, als letzter Schritt nach seiten.py.
Jedes Kopfbild darf nur einmal vorkommen; das Skript bricht sonst ab."""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KOPF = {
    "": "nxm/img/fassade-bronze.jpg",
    "referenzen/": "nxm/img/hero-treppe.jpg",
    "jobs/": "nxm/img/hero-treppenauge.jpg",
    "leistungen/": "nxm/img/haus-terrasse.jpg",
    "historie/": "nxm/img/balkon-altbau.jpg",
    "hoermann/": "nxm/img/eingang-anthrazit.jpg",
    "konfiguration-tore/": "nxm/img/garagentor-verkleidet-2.jpg",
    "konfiguration-tueren/": "nxm/img/eingang-holztuer.jpg",
    "kontakt/": "nxm/img/tor-villa.jpg",
}
# weitere Bildtausch-Stellen: Seite -> [(alt, neu)]
TAUSCH = {"": [("nxm/img/zaun-transporter.jpg", "nxm/img/treppe-licht.jpg")]}

doppelt = [b for b in set(KOPF.values()) if list(KOPF.values()).count(b) > 1]
assert not doppelt, f"Kopfbild doppelt: {doppelt}"
HEAD = re.compile(r"(<header class=\"main-header featured-full-width-img[^\"]*\" style=\"background-image: url\(')[^']*('\))")
for seite, bild in KOPF.items():
    p = os.path.join(ROOT, seite, "index.html")
    t = open(p, encoding="utf-8").read()
    pre = "../" * seite.count("/")
    n, k = HEAD.subn(lambda m: m.group(1) + pre + bild + m.group(2), t)
    assert k == 1, f"kein Kopfbild in {seite or '/'}"
    for a, b in TAUSCH.get(seite, []):
        n = n.replace(a, b)
    if n != t:
        open(p, "w", encoding="utf-8").write(n)
        print("kopfbild:", seite or "/", bild)
