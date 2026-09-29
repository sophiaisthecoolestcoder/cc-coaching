#!/usr/bin/env python3
"""Extract Christine's text verbatim from content/source/*.docx.

The website content is GENERATED from these documents, never retyped, so no
paraphrase or 'improvement' can creep in. Typos in the source are preserved
deliberately - correcting them is her call, not ours.
"""
import zipfile, re, html as _html
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "content/source"


def paragraphs(docname):
    """Return the non-empty paragraphs of a .docx or .txt, exactly as written.

    Plain .txt sources hold text that reached us as a message rather than a
    document (a client's reference, pasted verbatim), one paragraph per line.
    """
    if docname.endswith(".txt"):
        text = (SRC / docname).read_text(encoding="utf-8")
        return [apply_overrides(p.rstrip()) for p in text.split("\n") if p.strip()]
    with zipfile.ZipFile(SRC / docname) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<w:br[^>]*/>", "\n", xml)
    text = _html.unescape(re.sub(r"<[^>]+>", "", xml))
    return [apply_overrides(p.rstrip()) for p in text.split("\n") if p.strip()]


# ---------------------------------------------------------------------------
# CLIENT OVERRIDES
#
# Rule zero says her text is reproduced verbatim. These two substitutions are
# the documented exceptions, instructed explicitly by the client, who stated
# that her instruction takes precedence over rule zero in these cases.
#
# Everything here is applied to BOTH the generated page and the corpus that
# verify_verbatim.py checks against, so the verbatim check stays meaningful.
# Nothing may be added here without an explicit instruction from her.
# ---------------------------------------------------------------------------
OVERRIDES = [
    # 1. E-mail domain: .de -> .net
    ("cc-coaching.de", "cc-coaching.net"),
    # 2. Long dashes -> the regular hyphen. Her documents currently contain
    #    none, so this is a no-op today; it exists so that a dash typed into
    #    a future version of a document is normalised automatically.
    ("\u2013", "-"),   # en dash
    ("\u2014", "-"),   # em dash
    ("\u2012", "-"),   # figure dash
    ("\u2015", "-"),   # horizontal bar
    ("\u2212", "-"),   # minus sign
]


def apply_overrides(s):
    for old, new in OVERRIDES:
        s = s.replace(old, new)
    return s


def esc(s):
    """HTML-escape without touching her punctuation."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


if __name__ == "__main__":
    for doc in sorted(p.name for p in SRC.glob("*.docx")):
        print("=" * 60, "\n", doc, "\n", "=" * 60)
        for i, p in enumerate(paragraphs(doc)):
            print(f"[{i}] {p[:90]}{'…' if len(p) > 90 else ''}")
        print()
