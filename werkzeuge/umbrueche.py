"""Letzte zwei Wörter in Überschriften, Absätzen und Listenpunkten zusammenhalten (&nbsp;)."""
import os, re, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TAGS = "h1|h2|h3|h4|p|li|span|strong|b|em|a"
pat = re.compile(r"([^\s<>]{1,40})[ \t\n]+([^\s<>&]{1,24})(\s*)</(" + TAGS + r")>")
for f in glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True):
    if "/wp-" in f: continue
    t = open(f, encoding="utf-8").read()
    o = t
    t = t.replace("<h1>geradlinig modern individuell </h1>", "<h1>geradlinig<br>modern<br>individuell</h1>")
    # nur im sichtbaren Body arbeiten, Skripte/Styles auslassen
    head, body = t.split("<body", 1)
    parts = re.split(r"(<script.*?</script>|<style.*?</style>|<textarea.*?</textarea>)", body, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = pat.sub(lambda m: f"{m.group(1)}&nbsp;{m.group(2)}{m.group(3)}</{m.group(4)}>", parts[i])
    t = head + "<body" + "".join(parts)
    if t != o:
        open(f, "w", encoding="utf-8").write(t); print("umbrüche:", os.path.relpath(f, ROOT))
