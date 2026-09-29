# Christine Clausing - CC Coaching & Consulting

Static website for the coach and consultant Christine Clausing.

## Stack

Plain HTML, CSS and vanilla JavaScript. No build step, no dependencies, no
framework. Deployed as static files to IONOS Webhosting.

The site makes **zero third-party requests** - fonts are self-hosted, and there
is no analytics, no embed and no contact form. That is a deliberate constraint:
it keeps the site out of DSGVO trouble and means no cookie banner is required.

## Development

```bash
python3 -m http.server 8001
```

Then open <http://localhost:8001>.

- `index.html` - the site (one-pager with anchor sections)
- `styleguide.html` - every design token and component, rendered. Not linked
  from the site and marked `noindex`.

## Design system

**[`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) is binding.** `styles/tokens.css` is its
machine-readable form and is the only file allowed to contain literal colours,
font sizes, spacing values or durations.

Palette: Warm Sand & Ink. Type: Cormorant Garamond (display), Inter (body),
Jost (uppercase micro-type, echoing the logo wordmark).

## Structure

```
index.html                site
impressum.html            § 5 DDG, § 18 Abs. 2 MStV
datenschutz.html          Art. 13 DSGVO
styleguide.html           design system reference (noindex)
robots.txt · sitemap.xml
styles/                   fonts · tokens · base · layout · components · sections
scripts/main.js           sticky header, mobile nav, scroll reveal, nav spy
assets/fonts/             self-hosted woff2 (latin + latin-ext)
assets/img/               logo and imagery
content/source/           client source documents - git-ignored, contains
                          personal data
```

## Deployment

IONOS Webhosting (Apache) via `tools/deploy.sh`, which uploads only the public
files over SFTP/SSH. `.htaccess` handles the HTTPS redirect and security headers.

## License

All rights reserved © Christine Clausing.
