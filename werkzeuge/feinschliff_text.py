"""Textkorrekturen und Trennhilfen gegen Einzelwort-Umbrüche (idempotent)."""
import os, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIX = [
    ('class="forminator-label">Strasse <span', 'class="forminator-label">Straße <span'),
    ("Bewirb dich jetzt über unser&nbsp;Bewerbungsformular", "Jetzt online&nbsp;bewerben"),
    (">Strasse<", ">Straße<"),
    ("entgegen&shy;stehen", "entgegenstehen"),
    ("weiter&shy;verarbeitet", "weiterverarbeitet"),
    ("Edelstahl- und&nbsp;Aluminium&shy;konstruktionen", "Konstruktionen aus Edelstahl und&nbsp;Aluminium"),
    ("Berück&shy;sichtigung&nbsp;bau&shy;technischer<", "Berück&shy;sichtigung bau&shy;technischer&nbsp;Anforderungen<"),
    ('href="tel:49619563192"', 'href="tel:+49619563192"'),
    ("Verbraucherschlichtungsstelle", "Verbraucher&shy;schlichtungs&shy;stelle"),
    ("Aufbewahrungspflichten&nbsp;entgegenstehen", "Aufbewahrungs&shy;pflichten&nbsp;entgegen&shy;stehen"),
    ("Beschäftigungsverhältnisses&nbsp;weiterverarbeitet", "Beschäftigungs&shy;verhältnisses&nbsp;weiter&shy;verarbeitet"),
    ("Edelstahl- und&nbsp;Aluminiumkonstruktionen", "Edelstahl- und&nbsp;Aluminium&shy;konstruktionen"),
    ("Edelstahl- und Aluminium&shy;konstruktionen", "Edelstahl- und&nbsp;Aluminium&shy;konstruktionen"),
    ("Berück&shy;sichtigung bau&shy;technischer", "Berück&shy;sichtigung&nbsp;bau&shy;technischer"),
    ("Hörmann-Türanlagen", "Hörmann&#8209;Türanlagen"),
    ("an Hörmann&#8209;Türanlagen?", "an&nbsp;Hörmann&#8209;Türanlagen?"),
    ("Berücksichtigung&nbsp;bautechnischer", "Berück&shy;sichtigung bau&shy;technischer"),
    ("Maschinelle und…", "Maschinelle&nbsp;und…"),
    ("und&nbsp; beste Wärmedämmwerte", "und beste&nbsp;Wärmedämmwerte"),
    (">Einbruchschutz die KfW fördert<", ">Einbruchschutz, den die KfW&nbsp;fördert<"),
    ("WIR SUCHEN EINE/N Metallbauer – Fachrichtung Konstruktionstechnik in Vollzeit, Teilzeit oder geringfügiger&nbsp;Beschäftigung",
     "Wir suchen: Metallbauer (m/w/d), Fachrichtung Konstruktions&shy;technik, in Vollzeit, Teilzeit oder gering&shy;fügiger&nbsp;Beschäftigung"),
]
for f in glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True):
    if "/wp-" in f: continue
    t = open(f, encoding="utf-8").read(); o = t
    for a, b in FIX: t = t.replace(a, b)
    if t != o: open(f, "w", encoding="utf-8").write(t); print("text:", os.path.relpath(f, ROOT))
