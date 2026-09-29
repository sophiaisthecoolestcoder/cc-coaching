#!/usr/bin/env python3
"""Generate impressum.html and datenschutz.html from content/source/legal.html.

The legal text was supplied by the client and is reproduced verbatim. The only
change applied is the dash normalisation she instructed (see OVERRIDES in
extract.py), which here turns the generator's &ndash; into a plain hyphen.

Her document contains four blocks, each opened by an <h1>:
    Datenschutzerklaerung (de) | Privacy Policy (en)
    Impressum (de)             | Site Notice (en)
The German block leads each page, the English one follows it.

Run:  python3 tools/build_legal.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content/source/legal.html"

raw = SRC.read_text(encoding="utf-8")

# Dash normalisation, per her explicit instruction. Applied to the entity form
# the generator emits as well as to literal characters.
for old in ("&ndash;", "&mdash;", "–", "—", "‒", "―", "−"):
    raw = raw.replace(old, "-")

# Split into the four blocks on their <h1>.
parts = re.split(r"(?=<h1>)", raw)
blocks = {}
for part in parts:
    m = re.match(r"<h1>(.*?)</h1>", part, re.S)
    if not m:
        continue
    key = re.sub(r"<[^>]+>|&shy;", "", m.group(1)).strip()
    blocks[key] = part.strip()

# The English versions stay in content/source/legal.html but are NOT rendered.
# They are held for the day the site itself gets an English version; publishing
# them now would show every visitor the same text twice. Flip this to True at
# that point - no other change is needed.
INCLUDE_ENGLISH = False

expected = ["Datenschutzerkl&auml;rung", "Privacy Policy", "Impressum", "Site Notice"]
for k in expected:
    assert k in blocks, f"block missing from legal.html: {k}"


def english_block(en_key):
    if not INCLUDE_ENGLISH:
        return ""
    return ('\n      <hr class="rule rule--wide">\n'
            '      <div class="prose legal" lang="en">\n'
            + blocks[en_key] + "\n      </div>")


def page(title, de_key, en_key, filename, flat=False):
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - Christine Clausing</title>
<meta name="robots" content="noindex">
<script>document.documentElement.classList.add('js');</script>
<link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="assets/img/favicon-256.png" sizes="256x256" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/cormorant-garamond-300-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/inter-400-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles/fonts.css">
<link rel="stylesheet" href="styles/tokens.css">
<link rel="stylesheet" href="styles/base.css">
<link rel="stylesheet" href="styles/layout.css">
<link rel="stylesheet" href="styles/components.css">
<link rel="stylesheet" href="styles/sections.css">
</head>
<body>

<a class="skip-link" href="#main">Zum Inhalt springen</a>

<header class="site-header" data-header>
  <div class="container container--wide site-header__inner">
    <a class="logo" href="index.html" aria-label="CC Coaching &amp; Consulting">
      <picture>
        <source srcset="assets/img/logo.webp" type="image/webp">
        <img src="assets/img/logo.png" alt="CC Coaching &amp; Consulting" width="308" height="51">
      </picture>
    </a>
    <nav class="nav" aria-label="Hauptnavigation">
      <ul class="nav__list">
        <li><a class="nav__link" href="index.html">Startseite</a></li>
      </ul>
    </nav>
  </div>
</header>

<main id="main">
  <section class="section">
    <div class="container container--prose">
      <div class="prose legal{' legal--flat' if flat else ''}" lang="de">
{blocks[de_key]}
      </div>{english_block(en_key)}
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="container container--wide">
    <div class="grid grid--3">
      <div>
        <span class="site-footer__title">Kontakt</span>
        <ul class="site-footer__list stack stack--sm">
          <li>Christine Clausing</li>
          <li><a href="mailto:christine@cc-coaching.net">christine@cc-coaching.net</a></li>
        </ul>
      </div>
      <div>
        <span class="site-footer__title">&Uuml;bersicht</span>
        <ul class="site-footer__list stack stack--sm">
          <li><a href="index.html#was">Was</a></li>
          <li><a href="index.html#wer">Wer</a></li>
          <li><a href="index.html#wie">Wie</a></li>
          <li><a href="index.html#werte">Werte</a></li>
          <li><a href="index.html#referenzen">Referenzen</a></li>
        </ul>
      </div>
      <div>
        <span class="site-footer__title">Rechtliches</span>
        <ul class="site-footer__list stack stack--sm">
          <li><a href="impressum.html">Impressum</a></li>
          <li><a href="datenschutz.html">Datenschutzerkl&auml;rung</a></li>
        </ul>
      </div>
    </div>
    <div class="site-footer__bottom">
      <span>&copy; 2026 Christine Clausing</span>
    </div>
  </div>
</footer>

<script src="scripts/main.js" defer></script>
</body>
</html>
"""


if __name__ == "__main__":
    out = {
        "datenschutz.html": page("Datenschutzerklärung",
                                 "Datenschutzerkl&auml;rung", "Privacy Policy",
                                 "datenschutz.html"),
        "impressum.html":   page("Impressum", "Impressum", "Site Notice",
                                 "impressum.html", flat=True),
    }
    for name, html in out.items():
        (ROOT / name).write_text(html, encoding="utf-8")
        print(f"  {name}: {len(html.splitlines())} lines")
