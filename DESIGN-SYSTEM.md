# Design System - CC Coaching & Consulting

The binding rules for this website. `styles/tokens.css` is the machine-readable
version of this document; where the two disagree, `tokens.css` wins and this file
is out of date.

Render `styleguide.html` to see every rule below applied.

---

## The one rule

**`styles/tokens.css` is the only file permitted to contain a literal colour,
font size, spacing value, duration or easing curve.** Every other stylesheet
consumes `var(--…)`.

Need a value that isn't there? Add a token. That friction is deliberate - it
stops the system drifting one hard-coded `margin: 37px` at a time.

---

## 1. Colour - "Warm Sand & Ink"

| Token | Hex | Use |
|---|---|---|
| `--c-sand` | `#FAF7F2` | Page background |
| `--c-shell` | `#F1EBE2` | Alternating section bands |
| `--c-ink` | `#1C1B19` | Headings, display type, footer background |
| `--c-ink-soft` | `#3A3630` | Running body copy (Inter) |
| `--c-stone` | `#6B6660` | Secondary text, captions, meta |
| `--c-clay` | `#A9674B` | Decorative accent - rules, washes, control borders |
| `--c-clay-deep` | `#8F5239` | Text-safe accent, button fills, focus ring |
| `--c-clay-light` | `#C98A6B` | Accent **on dark grounds only** |
| `--c-line` | `#E4D9CB` | Decorative hairlines |

Prefer the semantic aliases in component CSS: `--bg`, `--bg-alt`, `--text`,
`--text-strong`, `--text-muted`, `--accent`, `--accent-soft`, `--accent-on-dark`,
`--border`, `--border-strong`.

### Contrast - measured, not estimated

On `--c-sand`:

| Pair | Ratio | |
|---|---|---|
| `--c-ink` | 16.1:1 | AAA |
| `--c-ink-soft` | 11.2:1 | AAA |
| `--c-stone` | 5.3:1 | AA |
| `--c-clay` | **4.2:1** | **fails AA for body text** |
| `--c-clay-deep` | 5.7:1 | AA |
| white on `--c-clay` | **4.4:1** | **fails AA for body text** |
| white on `--c-clay-deep` | 6.1:1 | AA |

On `--c-shell`: ink 14.5:1, ink-soft 10.1:1, stone 4.8:1, clay-deep 5.2:1 - all AA
or better.

On `--c-ink` (footer, mobile nav overlay):

| Pair | Ratio | |
|---|---|---|
| `--c-clay` | **3.9:1** | **fails AA for body text** |
| `--c-clay-light` | 6.0:1 | AA |
| `--c-sand` | 16.1:1 | AAA |

### The four colour rules

1. **Two levels of ink.** Headings and display type carry `--c-ink`; running
   body copy carries `--c-ink-soft`. Inter has a large x-height and, set in full
   ink beside Cormorant Light, out-weighs the heading and flattens the
   hierarchy. Both are AAA - the split exists purely to let Cormorant lead.

2. **Text at reading size never uses `--c-clay`.** It uses `--c-clay-deep` on
   light grounds and `--c-clay-light` on dark ones. `--c-clay` is for rules,
   washes, dots, and display-size type only.
3. **Filled buttons use `--c-clay-deep`.** White on `--c-clay` fails AA.
4. **Interactive control boundaries use `--border-strong`, not `--border`.**
   `--c-line` is 1.3:1 on sand. WCAG 1.4.11 exempts decorative dividers and card
   edges but requires 3:1 for the visible edge of a control. This is why
   `.btn--ghost` has a clay border rather than a hairline.

Re-run the contrast check whenever a colour changes.

---

## 2. Typography

Three families, three roles. **No family leaves its role.**

| Role | Family | Weights shipped |
|---|---|---|
| Display - h1, h2, h3, pull-quotes, values | Cormorant Garamond | 300, 400 |
| Body, h4 | Inter | 400, 600, 400 italic |
| Lead | Inter | 300 |
| Eyebrows, nav, buttons, labels, step numerals | Jost | 400 |

**The Jost rule.** Jost appears only as uppercase at `--tr-micro` (0.15em)
tracking. That wide-tracked capital setting is the typographic echo of the
`COACHING & CONSULTING` wordmark in the logo, which makes it a brand rule rather
than a stylistic one. Never use it for more than a few words - long strings at
0.15em stop being readable.

**Italics.** Inter ships a real italic for body emphasis. Cormorant does not, and
must never be set in italic. `font-synthesis: none` on `h1`-`h4` stops the
browser inventing faux weights and slants in display type.

**The lead is Inter Light (300).** `--c-stone` is already 4.80:1 on `--c-shell`,
so lightening the lead's colour any further would break AA on the alternating
bands. Weight is the only lever left, and it removes the perceived heaviness at
no contrast cost. Below 26rem it steps back to 400, where Light gets fragile.

**Inter runs with negative tracking.** `--tr-body` (-0.011em) and `--tr-lead`
(-0.016em). Inter is drawn to be optically tracked; set at 0 it reads like a
default interface font rather than typeset text. Cormorant gets `--tr-display`
at h1/h2 and no tracking at h3 - never Inter's negative values.

**`h4` is Inter semibold, not Cormorant.** At body size Cormorant reads lighter
than the Inter paragraph beneath it and inverts the hierarchy. Components that
genuinely want display type at that level set it explicitly - see `.card__title`.

### Scale

All display sizes are fluid via `clamp()`; body sizes are fixed.

| Token | Min → Max | Line height |
|---|---|---|
| `--fs-display` | 44 → 88px | 1.08 |
| `--fs-h1` | 36 → 60px | 1.12 |
| `--fs-h2` | 28 → 40px | 1.20 |
| `--fs-h3` | 20 → 24px | 1.35 |
| `--fs-lead` | 17 → 20px | 1.55 |
| `--fs-body` | 16px | 1.65 |
| `--fs-small` | 15px | - |
| `--fs-micro` | 13px | - |

Measure: body caps at `--w-prose` (68ch), lead at `--w-lead` (60ch), pull quotes
at `--w-display` (44rem).

**`--w-display` is deliberately in `rem`, not `ch`.** `ch` is relative to
font-size, so a `ch` measure applied to display type balloons to an accidental
width - 60ch on 40px Cormorant resolves to over 1000px. Any measure on display
type uses `rem`.

### German typesetting

- Quotes are always typographic: `„so"`. Never `"so"`.
- `hyphens: auto` on prose. Christine's compounds - *Grundtonbestimmung*,
  *Einfühlungsvermögen* - break narrow columns without it. Requires `lang="de"`.
- Never hyphenate headings, leads, pull quotes or values.
- **Specificity trap:** the hyphenation defaults are written as `:lang(de) p`
  and `:lang(de) blockquote` (specificity 0,1,1). A bare class selector like
  `.lead { hyphens: manual }` is 0,1,0 and *loses silently* - the declaration
  appears in the file and does nothing. Every no-hyphenation selector therefore
  keeps its `:lang(de)` prefix, and they all live together in `base.css`. Verify
  with computed style, not by eye.
- Fonts are subset to `latin` + `latin-ext`. German umlauts live in `latin`, so
  `latin-ext` effectively never downloads.

---

## 3. Space

4px base. Every gap comes from this scale; there is nothing in between.

`--sp-1` 4 · `--sp-2` 8 · `--sp-3` 12 · `--sp-4` 16 · `--sp-5` 24 · `--sp-6` 32
· `--sp-7` 48 · `--sp-8` 64 · `--sp-9` 96 · `--sp-10` 128 · `--sp-11` 160

**Sections never set their own vertical padding.** Rhythm comes only from
`--section-y` on `.section`. Horizontal padding comes only from `--gutter`.

---

## 4. Shape and elevation

- `--radius` is 2px. This design is sharp and editorial, not rounded.
- **Elevation is hairlines, not shadows.** The only shadow in the system is
  `--shadow-header`, on the sticky header once scrolled.

---

## 5. Motion

One primitive: **fade in and rise 12px**, staggered 60ms within a group. Applied
with `data-reveal`.

**In-page scrolling** uses the same curve. `scroll-behavior: smooth` in the
stylesheet is the no-JS fallback; when JavaScript runs it switches that off and
animates anchor jumps itself with `cubic-bezier(0.22, 1, 0.36, 1)` - the same
control points as `--ease` - over 420-1100ms depending on distance. The scroll
offset is read from `scroll-padding-top`, so it stays tied to `--header-h`
rather than duplicating it. On arrival the URL hash updates and focus moves to
the section, so keyboard and screen-reader users travel with the page.

A `setTimeout` guard force-completes the scroll if `requestAnimationFrame` is
throttled - browsers pause it in background tabs, and a paused animation would
otherwise strand the reader mid-page with the hash and focus never updated.

Banned: parallax, carousels, autoplay, anything that moves without user intent.

- `prefers-reduced-motion: reduce` drops every transform and shows all content
  immediately.
- The hidden starting state is scoped to `.js [data-reveal]`. Without JavaScript
  nothing is ever hidden. **Never write a hidden state without that guard.**

---

## 6. Accessibility floor

Non-negotiable, and checked before any deploy:

- Focus is never removed. `2px solid --c-clay-deep`, `3px` offset.
- Every page has a skip link and correct landmarks.
- Contrast meets the tables above.
- Full keyboard operation, including the mobile nav overlay (Escape closes it).
- Text at reading size never falls below AA.

---

## 7. Privacy and third parties

**The site makes zero third-party requests.** This is a design constraint, not a
preference.

- Fonts are self-hosted in `assets/fonts/`. Remote Google Fonts sends the
  visitor's IP to a US server without consent - treated as a DSGVO violation by
  LG München I (20.01.2022, 3 O 17493/20) and an active abuse-letter target.
- No analytics, no embeds, no maps, no CDN, no contact form.
- Consequence: **no cookie banner is required.** Keep it that way. Anything that
  adds a third party has to be weighed against losing that.

---

## 8. Files

```
styles/
  fonts.css        @font-face only - generated, self-hosted
  tokens.css       the single source of truth
  base.css         reset, element defaults, a11y, German typesetting
  layout.css       containers, section rhythm, grids
  components.css   buttons, nav, cards, quote, timeline, steps, values, footer
  sections.css     hero, portrait, qualifications, testimonials, pull quote
scripts/
  main.js          sticky header, mobile nav, scroll reveal, active nav link
```

Stylesheets load in that order and the order matters - `components.css` relies on
overriding `base.css`.
