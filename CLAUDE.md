# CC Coaching & Consulting - working rules

Static marketing site for Christine Clausing, a German coach and consultant.
No build step, no dependencies, no framework. Plain HTML, CSS and vanilla JS.

## Rule zero - her words, or a marked placeholder

**Never write, rewrite, shorten, correct or invent any user-facing text.**
Christine's documents in `content/source/` are the only source of copy. This
includes headings, button labels, card titles, image captions and meta
descriptions - not just body prose.

- Typos in her documents stay. `wer sie sind`, `Lösungensmöglichkeiten`,
  `das sich ausbreiten will`, `nicht nur Höhe` are hers to change, not ours.
- Do not split one of her sentences into several elements, do not merge two of
  her lines into one string, and do not excerpt a longer passage.
- Anything the design needs but she has not written becomes a visible
  `.ph` placeholder. If in doubt, ask her - never fill the gap yourself.

### The two sanctioned exceptions

She instructed explicitly that these override rule zero. Both live in
`OVERRIDES` in `tools/extract.py` and are applied to the generated page **and**
to the corpus the verifier checks, so the check stays meaningful:

1. E-mail domain `cc-coaching.de` -> `cc-coaching.net`.
2. Long dashes (en, em, figure, minus) -> the regular hyphen `-`. Her documents
   contain none today; this keeps it that way if one is typed later.

Nothing else may be added there without an explicit instruction from her.

### Text on the page that is not hers

`UI`, `TIMELINE` and `QUALS` in `tools/build_index.py` hold every word on the
page she did not write - interface labels, the timeline entries and the
qualification descriptions, all restored at her request. `verify_verbatim.py`
imports them, so the two files cannot drift apart. Adding an entry there is how
invented text would slip past the check: get her approval first.

`index.html` is **generated**, not hand-edited:

```bash
cd tools && python3 build_index.py      # regenerate from the .docx files
cd tools && python3 verify_verbatim.py  # must print PASS
```

`verify_verbatim.py` strips markup and placeholders and checks every remaining
line against the source documents. Run it after any content change; a FAIL means
text was invented somewhere.

All four pages currently carry `noindex` because they contain placeholders.
Remove it only when the page is genuinely finished.

## Read first

**`DESIGN-SYSTEM.md` is binding.** Read it before touching any CSS or adding any
section. `styles/tokens.css` is its machine-readable form.

## Hard rules

1. **Only `styles/tokens.css` may contain literal values** - colours, font sizes,
   spacing, durations, easings. Everything else uses `var(--…)`. Need a new
   value? Add a token first.

2. **Zero third-party requests.** No CDN, no Google Fonts, no analytics, no
   embeds, no web fonts loaded remotely. Fonts are self-hosted in
   `assets/fonts/`. This keeps the site free of a cookie banner and out of
   DSGVO trouble - do not trade that away without asking.

3. **Text at reading size never uses `--c-clay`** (4.2:1, fails AA). Use
   `--c-clay-deep` on light grounds, `--c-clay-light` on dark. Filled buttons use
   `--c-clay-deep`. Interactive control borders use `--border-strong`, never
   `--border`.

4. **Never remove a focus style.** Never write a hidden reveal state without the
   `.js` guard.

5. **Sections never set their own vertical padding.** Use `.section` and
   `--section-y`.

6. **Hyphenation is set by `:lang(de) p` / `:lang(de) blockquote` in `base.css`
   (specificity 0,1,1).** A bare class cannot override it - `.lead { hyphens:
   manual }` silently does nothing. Add new exceptions to the `:lang(de) …`
   group in `base.css` and check with computed style.

7. **German content**: `lang="de"`, typographic quotes `„…"`, `hyphens: auto` on
   prose, no hyphenation in headings. Christine addresses clients with *Sie*.

## Content

Her source documents live in `content/source/` (Wer, Was, Wie, Werte, Referenz).
They are the authoritative copy - use her own words rather than rewriting them
into marketing language. Her voice is essayistic and warm; keep it.

**`content/source/Referenz.docx` contains a client's private phone number and
home address.** Consent covers name, age and website only. Those two fields must
never enter the repo or the site.

## Structure

One-pager (`index.html`) with anchor sections, plus `impressum.html` and
`datenschutz.html`. `styleguide.html` is the design-system reference and is
`noindex` + disallowed in robots.txt. German now; the markup should stay clean enough that an
`/en/` copy is a translation, not a rebuild.

## Checks before calling anything done

```bash
python3 -m http.server 8001     # then check index, styleguide, legal pages
```

- Responsive at 320 / 768 / 1024 / 1440
- Keyboard-only pass, focus always visible
- `prefers-reduced-motion: reduce` - nothing hidden, nothing moving
- Network panel shows **no third-party requests**
- German proofread: umlauts, `„…"` quotes, hyphenation in narrow columns

## Deployment

IONOS Webhosting Plus (Apache), domain `cc-coaching.net` on the same IONOS
account. Mail for `christine@cc-coaching.net` runs on a separate IONOS Mail Basic
contract - never touch the domain's MX or TXT records.

```bash
IONOS_USER=… IONOS_HOST=… tools/deploy.sh        # dry run
IONOS_USER=… IONOS_HOST=… tools/deploy.sh --go   # upload
```

`deploy.sh` uploads only the public files and refuses to run unless
`verify_verbatim.py` passes. `.htaccess` forces `https://cc-coaching.net/` and sets
a CSP that blocks third-party requests; if the inline `js` script in the page
heads changes, its hash in `.htaccess` must be recomputed.

The Datenschutzerklärung must name IONOS SE as hosting processor.
