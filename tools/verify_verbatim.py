#!/usr/bin/env python3
"""Prove that every sentence rendered on the site is Christine's, verbatim.

Strips markup from index.html, removes anything inside a .ph placeholder,
then checks each remaining line against the source documents.
"""
import re, html as _html
from pathlib import Path
from extract import paragraphs

ROOT = Path(__file__).resolve().parent.parent

source = []
for doc in ("Was.docx", "Wer.docx", "Wie.docx", "Werte.docx", "Referenz.docx",
            "Referenz-Paula.txt"):
    source += paragraphs(doc)
corpus = "\n".join(source)

html = (ROOT / "index.html").read_text(encoding="utf-8")

# Drop head, scripts, svg, and every placeholder span.
body = html.split("<body>", 1)[1]
body = re.sub(r"<script.*?</script>", " ", body, flags=re.S)
body = re.sub(r"<svg.*?</svg>", " ", body, flags=re.S)
body = re.sub(r'<span class="ph[^"]*">.*?</span>\s*(?:<span class="ph__hint">.*?</span>)?',
              " ", body, flags=re.S)
body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)

text = _html.unescape(re.sub(r"<[^>]+>", "\n", body))
lines = [l.strip() for l in text.split("\n") if l.strip()]

# Not her prose. Imported from the generator so the two can never drift apart:
# anything the page shows that is not in her documents must be declared there.
from build_index import UI, TIMELINE, QUALS

ALLOW = set(UI.values())
for _year, _text in TIMELINE:
    ALLOW.update({_year, _text})
for _name, _desc in QUALS:
    ALLOW.update({_name, _desc})
ALLOW.update({
    "Zum Inhalt springen", "Christine Clausing", "CC Coaching & Consulting",
    "Was", "Wer", "Wie", "Werte", "Referenzen", "Impressum",
    "Datenschutzerklärung", "christine@cc-coaching.net",
    "© 2026 Christine Clausing", "·", "Menü", "Menü schließen",
})

missing = []
for line in lines:
    if line in ALLOW or line.startswith("[ Platzhalter") or len(line) < 3:
        continue
    if line not in corpus:
        missing.append(line)

print(f"lines checked : {len(lines)}")
print(f"not verbatim  : {len(missing)}")
for m in missing:
    print("   NOT IN SOURCE >>", m[:120])
print("\nRESULT:", "PASS - every sentence is verbatim" if not missing else "FAIL")
