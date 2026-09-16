#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the STATIN Factorial scope guide PDF from its Markdown source.

Factorial Documents does not preview .md files, so the client-facing artefact
must be a PDF.

Usage:
  python scripts/clients/statistic-institute/build_scope_guide_pdf.py
  python scripts/clients/statistic-institute/build_scope_guide_pdf.py --source path.md --out path.pdf
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import markdown
from xhtml2pdf import pisa

ROOT = Path(__file__).resolve().parents[3]
ASSET_DIR = ROOT / "clients" / "statistic-institute" / "statistic-instituteasset"
DEFAULT_SOURCE = ASSET_DIR / "FACTORIAL_SCOPE_GUIDE_STATIN.md"
DEFAULT_OUT = ASSET_DIR / "STATIN Factorial Scope Guide.pdf"

CSS = """
@page {
  size: a4 portrait;
  margin: 1.8cm 1.6cm 2cm 1.6cm;
  @frame footer {
    -pdf-frame-content: footerContent;
    bottom: 1cm;
    margin-left: 1.6cm;
    margin-right: 1.6cm;
    height: 1cm;
  }
}
body { font-family: Helvetica, Arial, sans-serif; font-size: 9.5pt; color: #1c1c1c; line-height: 1.45; }
h1 { font-size: 20pt; color: #0a0a0a; margin: 0 0 4pt 0; border-bottom: 2pt solid #1f6feb; padding-bottom: 4pt; }
h2 { font-size: 13pt; color: #14315c; margin: 16pt 0 4pt 0; border-bottom: 0.6pt solid #c8d4e3; padding-bottom: 2pt; }
h3 { font-size: 11pt; color: #14315c; margin: 12pt 0 3pt 0; }
h4 { font-size: 10pt; color: #333333; margin: 10pt 0 3pt 0; }
p { margin: 3pt 0 5pt 0; }
ul, ol { margin: 3pt 0 6pt 14pt; }
li { margin: 1.5pt 0; }
strong { color: #0a0a0a; }
hr { border: none; border-top: 0.6pt solid #d5dde7; margin: 10pt 0; }
table { width: 100%; border-collapse: collapse; margin: 5pt 0 9pt 0; }
th { background-color: #eef3fa; border: 0.5pt solid #b9c7d9; padding: 4pt 5pt; font-size: 8.8pt; text-align: left; color: #14315c; }
td { border: 0.5pt solid #cdd8e5; padding: 4pt 5pt; font-size: 8.8pt; vertical-align: top; }
code { font-family: Courier, monospace; font-size: 8.5pt; background-color: #f2f4f7; }
pre { font-family: Courier, monospace; font-size: 8.5pt; background-color: #f5f7fa; border: 0.5pt solid #d5dde7;
      padding: 5pt; margin: 4pt 0 8pt 0; }
a { color: #1f6feb; text-decoration: none; }
.footer { font-size: 7.5pt; color: #6b7684; text-align: center; }
"""


def markdown_to_html(md_text: str) -> str:
    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list"],
    )
    # xhtml2pdf renders raw checkbox syntax poorly; use a visual box instead.
    body = body.replace("[ ]", "&#9744;").replace("[x]", "&#9745;")
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>{CSS}</style></head>
<body>
<div id="footerContent" class="footer">
  Statistical Institute of Jamaica &middot; Factorial scope guide &middot; page <pdf:pagenumber> of <pdf:pagecount>
</div>
{body}
</body>
</html>
"""


def build_pdf(source: Path, out: Path) -> Path:
    md_text = source.read_text(encoding="utf-8")
    # Drop the trailing italic sign-off marker rendering oddly in PDF footers.
    md_text = re.sub(r"\n\*End of guide[^\n]*\*\s*$", "\n", md_text)
    html = markdown_to_html(md_text)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as handle:
        result = pisa.CreatePDF(html, dest=handle, encoding="utf-8")
    if result.err:
        raise RuntimeError(f"PDF generation failed with {result.err} error(s)")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Build STATIN scope guide PDF")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="Markdown source path")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output PDF path")
    args = parser.parse_args()

    out = build_pdf(Path(args.source), Path(args.out))
    size_kb = out.stat().st_size / 1024
    print(f"PDF written: {out} ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
