"""Zu lange &nbsp;-Paare wieder lösen (sonst Überlauf auf schmalen Handys).
Überschriften bleiben gebunden (nxm.js verkleinert bei Bedarf die Schrift), Absätze max. 34 Zeichen, Links max. 14."""
import os, re, glob, html
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LIM = {"h1": 99, "h2": 99, "h3": 99, "h4": 99, "p": 34, "li": 30, "span": 20, "strong": 30, "a": 14, "em": 30, "b": 30}
pat = re.compile(r"([^\s<>]{1,60})&nbsp;([^\s<>]{1,60})(\s*)</(h1|h2|h3|h4|p|li|span|strong|a|em|b)>")
def vis(s): return len(html.unescape(re.sub(r"&shy;", "", s)))
for f in glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True):
    if "/wp-" in f: continue
    t = open(f, encoding="utf-8").read(); o = t
    def fix(m):
        w1, w2, sp, tag = m.groups()
        if "&shy;" in w1 + w2: return m.group(0)            # mit Trennstellen darf es bleiben
        return m.group(0) if vis(w1) + vis(w2) + 1 <= LIM[tag] else f"{w1} {w2}{sp}</{tag}>"
    t = pat.sub(fix, t)
    if t != o: open(f, "w", encoding="utf-8").write(t); print("gelöst:", os.path.relpath(f, ROOT))
