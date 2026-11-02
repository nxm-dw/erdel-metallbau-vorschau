"""Live-Fassung für den IONOS-Webspace bauen (Ordner NXM_2026, Domain erdel-metallbau.de).

Aufruf:  python3 werkzeuge/live_build.py <Zielordner>
  - kopiert die Seite ohne .git, werkzeuge/, README, Vorlagen
  - entfernt noindex (außer auf den Weiterleitungsseiten), robots.txt erlaubt alles, sitemap.xml
  - .htaccess: 301 für alte Stellen-URLs, anfrage-config.php gesperrt
  - anfrage-config.php muss im Repo-Ordner liegen (nicht im Git), sonst Abbruch
Upload danach per lftp, siehe README „Livegang“."""
import os, re, shutil, subprocess, sys, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOMAIN = "https://www.erdel-metallbau.de"
WEITERLEITUNG = ("kalkulator-job1", "bewerbungsformular")

if len(sys.argv) < 2:
    raise SystemExit(__doc__)
ZIEL = os.path.abspath(sys.argv[1])
if not os.path.isfile(os.path.join(ROOT, "anfrage-config.php")):
    raise SystemExit("anfrage-config.php fehlt (Vorlage: anfrage-config.example.php)")

if os.path.isdir(ZIEL):
    shutil.rmtree(ZIEL)
subprocess.run(["rsync", "-a", "--exclude", ".git", "--exclude", "werkzeuge", "--exclude", "README.md",
                "--exclude", ".gitignore", "--exclude", "anfrage-config.example.php", "--exclude", ".DS_Store",
                "--exclude", "wp-admin", "--exclude", ".nojekyll", ROOT + "/", ZIEL + "/"], check=True)

seiten = []
for d, _, files in os.walk(ZIEL):
    if "index.html" not in files:
        continue
    rel = os.path.relpath(d, ZIEL)
    p = os.path.join(d, "index.html")
    if rel.split(os.sep)[0] in WEITERLEITUNG:
        continue
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"<meta name=['\"]robots['\"] content=['\"]noindex[^'\"]*['\"]\s*/?>\n?", "", s)
    open(p, "w", encoding="utf-8").write(s)
    seiten.append("" if rel == "." else rel.replace(os.sep, "/") + "/")

heute = datetime.date.today().isoformat()
with open(os.path.join(ZIEL, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for s in sorted(seiten, key=lambda x: (x != "", x)):
        f.write(f"  <url><loc>{DOMAIN}/{s}</loc><lastmod>{heute}</lastmod></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(ZIEL, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
with open(os.path.join(ZIEL, ".htaccess"), "w") as f:
    f.write("""# erdel metallbau – statische Website (NEXAS Media)
Options -Indexes
DirectoryIndex index.html index.php

<Files "anfrage-config.php">
  Require all denied
</Files>

RewriteEngine On
RewriteRule ^kalkulator-job1/?$ /jobs/#stelle-metallbauer [R=301,NE,L]
RewriteRule ^bewerbungsformular/?$ /jobs/#bewerben [R=301,NE,L]

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpeg "access plus 30 days"
  ExpiresByType image/png "access plus 30 days"
  ExpiresByType image/svg+xml "access plus 30 days"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType text/css "access plus 30 days"
  ExpiresByType application/javascript "access plus 30 days"
</IfModule>
""")
print(f"Live-Fassung: {ZIEL} ({len(seiten)} Seiten in der Sitemap)")
