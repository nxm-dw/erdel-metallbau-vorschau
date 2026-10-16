"""Interne Links ohne index.html: kontakt/index.html -> kontakt/, index.html -> ./"""
import os, re, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
pat = re.compile(r'''(href=["'])((?:\.\./)*)((?:[a-z0-9-]+/)*)index\.html(#[^"']*)?(["'])''')
def fix(m):
    pre, up, path, frag, q = m.group(1), m.group(2), m.group(3), m.group(4) or "", m.group(5)
    url = up + path
    return f"{pre}{url or './'}{frag}{q}"
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    if "/wp-" in f: continue
    t = open(f, encoding="utf-8").read()
    n = pat.sub(fix, t)
    if n != t:
        open(f, "w", encoding="utf-8").write(n); print("links:", os.path.relpath(f, ROOT))
