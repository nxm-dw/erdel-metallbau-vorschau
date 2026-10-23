"""Lesbarkeit weißer Schrift auf Fotos messen (braucht Playwright + Pillow):
  python3 werkzeuge/kontrast.py [Basis-URL]
Blendet den Text aus, fotografiert den Hintergrund hinter jeder Zeile und rechnet den WCAG-Kontrast
gegen die Schriftfarbe: „hell95“ = hellste 5 % der Pixel (schlechtester Fall), „mittel“ = Durchschnitt.
Grenze: große Schrift 3:1, normale Schrift 4,5:1 (gemessen am Mittel, hell95 als Warnhinweis)."""
import io, sys
from playwright.sync_api import sync_playwright
from PIL import Image

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8010/"
PAGES = ["", "referenzen/", "leistungen/", "hoermann/", "jobs/", "historie/", "kontakt/", "konfiguration-tore/", "konfiguration-tueren/"]
SEL = ".main-header h1, .teaser-block h2, .teaser-block .teaser-sub, .teaser-block p, .x-cta h2, .x-cta p, .x-strip__item figcaption, .x-partner__name, .x-konf-media figcaption strong, .x-konf-media figcaption span, .x-formside h2, .x-formside li strong, .x-formside li span, .x-formside__hint"
STATIC = "*,*::before,*::after{transition:none!important;animation:none!important} html.nxm-js .nxm-reveal{opacity:1!important;transform:none!important;clip-path:none!important}"


def lum(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])


def ratio(a, b):
    a, b = max(a, b), min(a, b)
    return (a + 0.05) / (b + 0.05)


bad = 0
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for w in (1440, 390):
        pg = br.new_page(viewport={"width": w, "height": 900})
        for u in PAGES:
            pg.goto(BASE + u, wait_until="networkidle")
            pg.add_style_tag(content=STATIC)
            n = pg.evaluate(f"document.querySelectorAll({SEL!r}).length")
            for i in range(n):
                info = pg.evaluate(f"""(i) => {{ const el = document.querySelectorAll({SEL!r})[i];
                    const r = el.getBoundingClientRect(); if (!r.width || getComputedStyle(el).visibility === 'hidden') return null;
                    el.scrollIntoView({{block: 'center'}}); const q = el.getBoundingClientRect();
                    const c = getComputedStyle(el).color.match(/\\d+/g).map(Number);
                    const big = parseFloat(getComputedStyle(el).fontSize) >= 24 || (parseFloat(getComputedStyle(el).fontSize) >= 18.66 && +getComputedStyle(el).fontWeight >= 700);
                    el.dataset.k = '1'; return {{x: q.x, y: q.y, w: q.width, h: q.height, c, big, t: el.innerText.trim().slice(0, 40)}}; }}""", i)
                if not info or info["w"] < 4:
                    continue
                pg.add_style_tag(content="[data-k='1']{color:transparent!important;text-shadow:none!important} [data-k='1'] *{color:transparent!important}")
                clip = {"x": max(0, info["x"]), "y": max(0, info["y"]), "width": min(info["w"], w - max(0, info["x"])), "height": info["h"]}
                im = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")
                pg.evaluate(f"(i) => {{ const el = document.querySelectorAll({SEL!r})[i]; delete el.dataset.k; }}", i)
                L = sorted(lum(p) for p in im.get_flattened_data())
                fg = lum(info["c"])
                hi = L[int(len(L) * 0.95)] if fg > 0.5 else L[int(len(L) * 0.05)]
                mean = sum(L) / len(L)
                r_mean, r_hi = ratio(fg, mean), ratio(fg, hi)
                need = 3 if info["big"] else 4.5
                flag = "ZU HELL" if r_mean < need else ("knapp" if r_hi < need else "")
                if flag:
                    bad += flag == "ZU HELL"
                    print(f"{w} {u or '/'} {flag}: mittel {r_mean:.1f} hell95 {r_hi:.1f} (≥{need}) „{info['t']}“")
        pg.close()
    br.close()
print("zu hell:", bad)
