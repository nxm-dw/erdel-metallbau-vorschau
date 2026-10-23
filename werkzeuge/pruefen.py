"""Qualitätsprüfung vor jedem Push (braucht Playwright):
  python3 werkzeuge/pruefen.py [Basis-URL] [Seite …]
Prüft je Seite und Breite: horizontaler Überlauf, angeschnittene/überstehende Texte (ÜBERSTAND),
einzelne Wörter in der letzten Zeile (WAISE), JS-Fehler, nicht ladende Bilder/Dateien.
Animationen werden abgeschaltet, Einblend-Effekte sofort sichtbar."""
import os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].startswith("http") else "http://localhost:8010/"
PAGES = [a for a in sys.argv[1:] if not a.startswith("http")] or [""] + sorted(
    d + "/" for d in os.listdir(ROOT)
    if os.path.isfile(os.path.join(ROOT, d, "index.html")) and d not in ("kalkulator-job1", "bewerbungsformular"))
WIDTHS = [360, 390, 768, 1024, 1280, 1440]
STATIC = """*,*::before,*::after{transition:none!important;animation:none!important}
html.nxm-js .nxm-reveal{opacity:1!important;transform:none!important;clip-path:none!important}"""

JS = r"""() => {
const vw = document.documentElement.clientWidth, out = [];
const vis = el => { const s = getComputedStyle(el); const r = el.getBoundingClientRect();
  return s.visibility !== 'hidden' && s.display !== 'none' && r.width > 0 && r.height > 0 && !el.closest('.nxm-menu,[aria-hidden="true"],.visually-hidden,.modal,script,style,noscript'); };
const txt = el => (el.innerText || '').replace(/\s+/g, ' ').trim();
if (document.scrollingElement.scrollWidth > vw + 1) out.push(['SEITE', 'scrollWidth ' + document.scrollingElement.scrollWidth + ' > ' + vw]);
const sel = 'h1,h2,h3,h4,p,li,a,button,label,dt,dd,figcaption,summary span,.x-tile__value,.x-stelle__title,.x-upload__name,option';
document.querySelectorAll(sel).forEach(el => {
  if (!vis(el) || !txt(el)) return;
  const r = el.getBoundingClientRect();
  if (r.right > vw + 1 || r.left < -1) out.push(['RAND', el.tagName + ' ' + txt(el).slice(0, 50) + ' [' + Math.round(r.left) + '..' + Math.round(r.right) + ' / ' + vw + ']']);
  const rg = document.createRange(); rg.selectNodeContents(el); const t = rg.getBoundingClientRect();
  if (t.width && (t.right > r.right + 2 || t.left < r.left - 2) && getComputedStyle(el).overflowX !== 'visible')
    out.push(['ÜBERSTAND', el.tagName + ' ' + txt(el).slice(0, 50)]);
  // von einem Vorfahren abgeschnitten?
  let p = el.parentElement;
  while (p && p !== document.body) {
    const s = getComputedStyle(p);
    if (s.overflowX !== 'visible' && !p.matches('.x-upload,.modal,.x-strip__item,.x-tl__media,figure')) {
      const pr = p.getBoundingClientRect();
      if (t.width && (t.right > pr.right + 2 || t.left < pr.left - 2)) { out.push(['ANGESCHNITTEN', el.tagName + ' ' + txt(el).slice(0, 50) + ' in ' + p.className.toString().slice(0, 30)]); break; }
    }
    p = p.parentElement;
  }
});
// einzelnes Wort in der letzten Zeile
document.querySelectorAll('h1,h2,h3,h4,p,li,figcaption,dd,.x-stelle__title,.x-stelle__teaser,.x-benefits strong,.x-tile__value').forEach(el => {
  if (!vis(el)) return;
  const t = txt(el); if (!t || t.split(' ').length < 3 || el.querySelector('br,p,li,h2,h3')) return;
  const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); const words = []; let n;
  while ((n = walker.nextNode())) { const re = /\S+/g; let m; while ((m = re.exec(n.data))) {
    const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length);
    const rs = rg.getClientRects(); if (rs.length) words.push([rs[rs.length - 1].top, m[0]]); } }
  if (words.length < 3) return;
  const lines = []; words.forEach(([top, w]) => { const L = lines.find(l => Math.abs(l.top - top) < 6); if (L) L.w.push(w); else lines.push({ top, w: [w] }); });
  if (lines.length < 2) return;
  lines.sort((a, b) => a.top - b.top); const last = lines[lines.length - 1].w;
  if (last.length === 1 && last[0].replace(/[^\p{L}\p{N}]/gu, '').length > 0 && last[0].length > 1 && !/[ ]/.test(last[0]))
    out.push(['WAISE', el.tagName + ': …' + lines[lines.length - 2].w.slice(-3).join(' ') + ' | ' + last[0]]);
});
document.querySelectorAll('img').forEach(i => { if (i.complete && i.naturalWidth === 0 && i.getAttribute('src')) out.push(['BILD', i.getAttribute('src')]); });
return out; }"""

total = 0
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for w in WIDTHS:
        ctx = b.new_context(viewport={"width": w, "height": 900})
        pg = ctx.new_page()
        errs, bad = [], []
        pg.on("pageerror", lambda e: errs.append(str(e)[:120]))
        pg.on("response", lambda r: bad.append(f"{r.status} {r.url}") if r.status >= 400 and BASE in r.url else None)
        for u in PAGES:
            errs.clear(); bad.clear()
            pg.goto(BASE + u, wait_until="networkidle")
            pg.add_style_tag(content=STATIC)
            pg.evaluate("""async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); }
                          document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'); scrollTo(0, 0); }""")
            pg.wait_for_timeout(300)
            res = pg.evaluate(JS) + [["JS", e] for e in errs] + [["404", x] for x in bad]
            for kind, msg in res:
                print(w, u or "/", kind, msg)
            total += len(res)
        ctx.close()
    b.close()
print("Befunde:", total)
