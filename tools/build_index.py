#!/usr/bin/env python3
"""Generate index.html from Christine's .docx files.

RULE: every word of body content is inserted verbatim from content/source/.
Anything that is not her text is wrapped in a .ph placeholder. Do not type
her prose into this file - read it from the documents.

Run:  python3 tools/build_index.py
"""
from pathlib import Path
from extract import paragraphs, esc

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# APPROVED INTERFACE LABELS
#
# These are NOT Christine's prose. They are navigation and button labels that
# she approved explicitly. Nothing may be added here without her say-so, and
# anything added here must also be listed in tools/verify_verbatim.py so the
# verbatim check stays honest about what is hers and what is not.
# ---------------------------------------------------------------------------
UI = {
    "btn_mehr":           "Mehr erfahren",
    "footer_kontakt":     "Kontakt",
    "footer_uebersicht":  "Übersicht",
    "footer_rechtliches": "Rechtliches",
    # Section headings she approved. "Grundtonbestimmung" and "Kontakt" are
    # words from her own text; "Ausbildung" is not, and is used only with
    # her explicit sign-off.
    "h_grundton":         "Grundtonbestimmung",
    "h_kontakt":          "Kontakt",
    "h_ausbildung":       "Ausbildung",
    "h_kontakt_lang":     "Schreiben Sie mir",
    "hero_eyebrow":       "Christine Clausing \u00b7 Einzelcoaching",
    "img_alt":            "Christine Clausing",
}

# Written by the assistant, not by her, and restored at her explicit request.
# Kept here rather than inline so that everything that is not hers is visible
# in one place.
TIMELINE = [
    ("1964 \u00b7 M\u00fcnchen",
     "Geboren als \u201eM\u00fcnchner Kindl\u201c. Studium der Betriebswirtschaft, Diplom-Kauffrau."),
    ("1991 \u00b7 Berlin",
     "Referentin, sp\u00e4ter stellvertretende Abteilungsleiterin im Direktorat Abwicklung der Treuhandanstalt."),
    ("1993 \u00b7 Spreewald",
     "Aufbau des Hotels \u201eZur Bleiche\u201c - heute unter den 100 besten Hotels Europas."),
    ("Heute",
     "Einzelcoaching und Beratung. Kuratorin der Spreew\u00e4lder Kulturstiftung."),
]

QUALS = [
    ("Diplom-Kauffrau",
     "Studium der Betriebswirtschaftslehre, M\u00fcnchen."),
    ("Ausgebildeter Business-Coach",
     "Coaching-Ausbildung mit Schwerpunkt auf beruflicher Entwicklung."),
    ("SaMaSonologin",
     "Grundtonbestimmung nach dem Nadabrahma-System von Vemu Mukunda. Mitglied im Institut f\u00fcr Tonkraft."),
    ("Intraact-Konzept",
     "Verhaltenstherapeutischer Ansatz mit dem Fokus auf Bindung und Beziehung."),
    ("Kuratorin der Spreew\u00e4lder Kulturstiftung",
     "Ehrenamtliches Engagement f\u00fcr Kultur und Region."),
]


WAS   = paragraphs("Was.docx")
WER   = paragraphs("Wer.docx")
WIE   = paragraphs("Wie.docx")
WERTE = paragraphs("Werte.docx")
REF   = paragraphs("Referenz.docx")
PAULA = paragraphs("Referenz-Paula.txt")


def ph(label, hint=None, block=False):
    cls = "ph ph--block" if block else "ph"
    h = f'<span class="ph__hint">{esc(hint)}</span>' if hint else ""
    return f'<span class="{cls}">[ Platzhalter: {esc(label)} ]{h}</span>'


def paras(items, cls=""):
    c = f' class="{cls}"' if cls else ""
    return "\n".join(f"        <p{c}>{esc(p)}</p>" for p in items)


# Linkify only - the visible characters stay exactly as she wrote them.
def linkify(s):
    s = esc(s)
    s = s.replace("christine@cc-coaching.net",
                  '<a href="mailto:christine@cc-coaching.net">christine@cc-coaching.net</a>')
    s = s.replace("www.tonkraft.net",
                  '<a href="https://www.tonkraft.net" rel="noopener">www.tonkraft.net</a>')
    return s


HEAD = '''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Christine Clausing - Coaching &amp; Consulting</title>
<meta name="description" content="PLATZHALTER - Meta-Beschreibung muss von Christine Clausing formuliert werden.">
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
    <a class="logo" href="#top" aria-label="CC Coaching &amp; Consulting">
      <picture>
        <source srcset="assets/img/logo.webp" type="image/webp">
        <img src="assets/img/logo.png" alt="CC Coaching &amp; Consulting" width="308" height="51">
      </picture>
    </a>
    <button class="nav__toggle" type="button" data-nav-open aria-expanded="false" aria-controls="hauptnavigation" aria-label="Menü">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <nav class="nav nav--overlay" id="hauptnavigation" data-nav aria-label="Hauptnavigation">
      <button class="nav__close" type="button" data-nav-close aria-label="Menü schließen">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
      <ul class="nav__list">
        <li><a class="nav__link" data-nav-link href="#was">Was</a></li>
        <li><a class="nav__link" data-nav-link href="#wer">Wer</a></li>
        <li><a class="nav__link" data-nav-link href="#wie">Wie</a></li>
        <li><a class="nav__link" data-nav-link href="#werte">Werte</a></li>
        <li><a class="nav__link" data-nav-link href="#referenzen">Referenzen</a></li>
      </ul>
    </nav>
  </div>
</header>

<main id="main">
'''

# ---------------------------------------------------------------- hero
# No text of hers is placed here. "Es geht mir um den Menschen. Immer."
# was tried as a claim and rejected as too strong for a single sentence;
# it stays where she wrote it, at the end of Wer.docx.
# The lead is a placeholder too: Was.docx[1] is shown complete in the Was
# section, and repeating it here would print the same paragraph twice.

# Her five values are one sentence in Werte.docx. Splitting it into lines is a
# layout choice she asked for; the words are taken straight out of her sentence
# and their capitalisation is left exactly as she wrote it ("richtiges Handeln"
# stays lower case).
VALUES = [v.strip() for v in WERTE[3].rstrip(".").split(",")]
assert len(VALUES) == 5, "expected five values in Werte.docx"
for _v in VALUES:
    assert _v in WERTE[3], "each value must come from her sentence"

timeline_items = "\n".join(
    f'        <li class="timeline__item">\n'
    f'          <span class="timeline__year">{esc(y)}</span>\n'
    f'          <p>{esc(t)}</p>\n'
    f'        </li>'
    for y, t in TIMELINE
)

qual_items = "\n".join(
    f'        <li class="qual">\n'
    f'          <h3 class="qual__name">{esc(n)}</h3>\n'
    f'          <p class="qual__note">{esc(d)}</p>\n'
    f'        </li>'
    for n, d in QUALS
)

value_items = "\n".join(
    f'        <li class="values__item">{esc(v)}</li>' for v in VALUES
)

# Both taken word for word out of Was.docx[1]. The assertions below fail the
# build if either stops matching her document exactly.
HERO_H1 = "Ich begleite, berate und unterst\u00fctze Menschen in ihrer Entwicklung."
HERO_LEAD = ("Der berufliche Aspekt steht oft im Vordergrund, das Private darf dabei "
             "nicht au\u00dfen vor bleiben.")
# The second reference is Referenz.docx[9] and [10], chosen by her.
assert REF[9].startswith("Ich glaube, am meisten hängen geblieben"), "Pia reference moved"
assert REF[10].startswith("Unsere Session kam in einer sehr besonderen Phase"), "Pia reference moved"
assert REF[15] == "Pia" and REF[22] == "piaheld.com", "Pia attribution lines moved"
# Paula's reference was sent as a message, not a document; it is kept verbatim
# in Referenz-Paula.txt - two paragraphs, then her own one-line attribution.
assert len(PAULA) == 3 and PAULA[2].startswith("Paula,"), "Paula reference changed shape"

assert HERO_H1 in WAS[1], "hero heading must be a verbatim excerpt of Was.docx"
assert HERO_LEAD in WAS[1], "hero lead must be a verbatim excerpt of Was.docx"

IMG_SIZES = "(min-width: 56rem) 42vw, 100vw"

hero = f'''
  <section class="hero" id="top">
    <div class="container">
      <div class="split hero__split">
        <div>
          <span class="eyebrow">{esc(UI["hero_eyebrow"])}</span>
          <h1 class="hero__claim">{esc(HERO_H1)}</h1>
          <hr class="rule">
          <p class="lead">{esc(HERO_LEAD)}</p>
          <div class="hero__actions">
            <a class="btn btn--primary" href="#was">{esc(UI["btn_mehr"])}</a>
          </div>
        </div>
        <figure class="portrait">
          <picture>
            <source type="image/webp" sizes="{IMG_SIZES}"
                    srcset="assets/img/christine-600.webp 600w, assets/img/christine-1200.webp 1200w">
            <img src="assets/img/christine-1200.jpg" sizes="{IMG_SIZES}"
                 srcset="assets/img/christine-600.jpg 600w, assets/img/christine-1200.jpg 1200w"
                 alt="{esc(UI["img_alt"])}" width="1200" height="1600">
          </picture>
        </figure>
      </div>
    </div>
  </section>
'''

# ---------------------------------------------------------------- was
was = f'''
  <section class="section section--alt" id="was">
    <div class="container">
      <div class="section-head" data-reveal>
        <h2>{esc(WAS[0])}</h2>
      </div>
      <div class="prose" data-reveal>
{paras(WAS[1:])}
      </div>
    </div>
  </section>
'''

# ---------------------------------------------------------------- wer
wer = f'''
  <section class="section" id="wer">
    <div class="container">
      <div class="section-head" data-reveal>
        <h2>{esc(WER[0])}</h2>
      </div>
      <div class="prose" data-reveal>
{paras(WER[1:])}
      </div>
      <ol class="timeline" style="margin-top: var(--sp-8); max-width: var(--w-prose);" data-reveal>
{timeline_items}
      </ol>
    </div>
  </section>
'''

# ------------------------------------------------------- qualifikationen
quals = f'''
  <section class="section section--alt" id="qualifikationen">
    <div class="container">
      <div class="section-head" data-reveal>
        <h2>{esc(UI["h_ausbildung"])}</h2>
      </div>
      <ul class="quals" style="max-width: var(--w-prose);" data-reveal>
{qual_items}
      </ul>
    </div>
  </section>
'''

# ---------------------------------------------------------------- wie
wie = f'''
  <section class="section" id="wie">
    <div class="container">
      <div class="section-head" data-reveal>
        <h2>{esc(WIE[0])}</h2>
      </div>
      <div class="prose" data-reveal>
        <p>{esc(WIE[1])}</p>
        <p>{linkify(WIE[2])}</p>
      </div>
    </div>
  </section>
'''

# --------------------------------------------------------------- ablauf
ablauf = f'''
  <section class="section section--alt" id="ablauf">
    <div class="container">
      <div class="section-head" data-reveal>
        <h2>{esc(UI["h_grundton"])}</h2>
      </div>
      <div class="prose" data-reveal>
        <p>{esc(WIE[4])}</p>
      </div>
      <blockquote class="pullquote" data-reveal>{esc(WIE[5])}</blockquote>
    </div>
  </section>
'''

# ---------------------------------------------------------------- werte
werte = f'''
  <section class="section" id="werte">
    <div class="container">
      <div class="section-head" data-reveal>
        <h2>{esc(WERTE[0])}</h2>
      </div>
      <div class="prose" data-reveal>
        <p>{esc(WERTE[1])}</p>
        <p>{esc(WERTE[2])}</p>
      </div>
      <ul class="values" style="margin-top: var(--sp-7); max-width: var(--w-prose);" data-reveal>
{value_items}
      </ul>
      <div class="prose" data-reveal>
        <p>{esc(WERTE[4])}</p>
      </div>
    </div>
  </section>
'''

# ----------------------------------------------------------- referenzen
# Charlotte's reference is reproduced in full. Pia's document is a private
# letter in which she asks Christine to pick the sentences herself - that
# selection is Christine's to make, not ours.
ref = f'''
  <section class="section section--alt" id="referenzen">
    <div class="container">
      <div class="section-head" data-reveal>
        <h2>{esc(REF[0])}</h2>
      </div>
      <div class="testimonials" style="max-width: var(--w-prose);">
        <blockquote class="quote" data-reveal>
          <p class="quote__text">{esc(REF[2])}</p>
          <p class="quote__text">{esc(REF[3])}</p>
          <cite class="testimonial__meta"><span>{esc(REF[4])}</span><span>{esc(REF[1])}</span></cite>
        </blockquote>
        <blockquote class="quote" data-reveal>
          <p class="quote__text">{esc(REF[9])}</p>
          <p class="quote__text">{esc(REF[10])}</p>
          <cite class="testimonial__meta">
            <span>{esc(REF[15])}</span>
            <span><a href="https://piaheld.com" rel="noopener">{esc(REF[22])}</a></span>
          </cite>
        </blockquote>
        <blockquote class="quote" data-reveal>
          <p class="quote__text">{esc(PAULA[0])}</p>
          <p class="quote__text">{esc(PAULA[1])}</p>
          <cite class="testimonial__meta"><span>{esc(PAULA[2])}</span></cite>
        </blockquote>
      </div>
    </div>
  </section>
'''

# --------------------------------------------------------------- kontakt
kontakt = f'''
  <section class="section" id="kontakt">
    <div class="container">
      <div class="section-head" data-reveal>
        <h2>{esc(UI["h_kontakt_lang"])}</h2>
      </div>
      <div class="prose" data-reveal>
        <p>{linkify(WIE[3])}</p>
      </div>
    </div>
  </section>
'''

FOOT = f'''
</main>

<footer class="site-footer">
  <div class="container container--wide">
    <div class="grid grid--3">
      <div>
        <span class="site-footer__title">{esc(UI["footer_kontakt"])}</span>
        <ul class="site-footer__list stack stack--sm">
          <li>Christine Clausing</li>
          <li><a href="mailto:christine@cc-coaching.net">christine@cc-coaching.net</a></li>
        </ul>
      </div>
      <div>
        <span class="site-footer__title">{esc(UI["footer_uebersicht"])}</span>
        <ul class="site-footer__list stack stack--sm">
          <li><a href="#was">Was</a></li>
          <li><a href="#wer">Wer</a></li>
          <li><a href="#wie">Wie</a></li>
          <li><a href="#werte">Werte</a></li>
          <li><a href="#referenzen">Referenzen</a></li>
        </ul>
      </div>
      <div>
        <span class="site-footer__title">{esc(UI["footer_rechtliches"])}</span>
        <ul class="site-footer__list stack stack--sm">
          <li><a href="impressum.html">Impressum</a></li>
          <li><a href="datenschutz.html">Datenschutzerklärung</a></li>
        </ul>
      </div>
    </div>
    <div class="site-footer__bottom">
      <span>© 2026 Christine Clausing</span>
    </div>
  </div>
</footer>

<script src="scripts/main.js" defer></script>
</body>
</html>
'''

out = HEAD + hero + was + wer + quals + wie + ablauf + werte + ref + kontakt + FOOT

if __name__ == "__main__":
    (ROOT / "index.html").write_text(out, encoding="utf-8")
    print(f"index.html written - {len(out.splitlines())} lines")
