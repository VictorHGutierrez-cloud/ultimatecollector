#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build LIAT Factorial AVD SOW PDF from Markdown."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import markdown
from xhtml2pdf import pisa

ROOT = Path(__file__).resolve().parents[3]
ASSET_DIR = ROOT / "clients" / "liat-air" / "liat-airasset"
DEFAULT_SOURCE = ASSET_DIR / "FACTORIAL_AVD_SOW_LIAT.md"
DEFAULT_OUT = ASSET_DIR / "LIAT Factorial AVD Operating Guide.pdf"

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
h1 { font-size: 18pt; color: #0a0a0a; margin: 0 0 4pt 0; border-bottom: 2pt solid #0b3d5c; padding-bottom: 4pt; }
h2 { font-size: 12.5pt; color: #0b3d5c; margin: 14pt 0 4pt 0; border-bottom: 0.6pt solid #c8d4e3; padding-bottom: 2pt; }
h3 { font-size: 11pt; color: #0b3d5c; margin: 11pt 0 3pt 0; }
h4 { font-size: 10pt; color: #333333; margin: 9pt 0 3pt 0; }
p { margin: 3pt 0 5pt 0; }
ul, ol { margin: 3pt 0 6pt 14pt; }
li { margin: 1.5pt 0; }
strong { color: #0a0a0a; }
hr { border: none; border-top: 0.6pt solid #d5dde7; margin: 10pt 0; }
table { width: 100%; border-collapse: collapse; margin: 5pt 0 9pt 0; table-layout: fixed; }
th { background-color: #eef3fa; border: 0.5pt solid #b9c7d9; padding: 4pt 5pt; font-size: 8.8pt; text-align: left; color: #0b3d5c; word-wrap: break-word; }
td { border: 0.5pt solid #cdd8e5; padding: 4pt 5pt; font-size: 8.8pt; vertical-align: top; word-wrap: break-word; }
code { font-family: Courier, monospace; font-size: 8.5pt; background-color: #f2f4f7; }
pre { font-family: Courier, monospace; font-size: 8pt; background-color: #f5f7fa; border: 0.5pt solid #d5dde7;
      padding: 5pt; margin: 4pt 0 8pt 0; }
a { color: #1f6feb; text-decoration: none; }
.footer { font-size: 7.5pt; color: #6b7684; text-align: center; }
"""


def _equal_colgroup(match: re.Match[str]) -> str:
    """Force equal column widths — xhtml2pdf otherwise crushes narrow headers."""
    table_open = match.group(1)
    inner = match.group(2)
    header_row = re.search(r"<tr>\s*((?:<th[^>]*>.*?</th>\s*)+)</tr>", inner, flags=re.I | re.S)
    if not header_row:
        return match.group(0)
    ncols = len(re.findall(r"<th\b", header_row.group(1), flags=re.I))
    if ncols < 2:
        return match.group(0)
    width = max(1, int(100 / ncols))
    cols = "".join(f'<col width="{width}%" />' for _ in range(ncols))
    return f"{table_open}<colgroup>{cols}</colgroup>{inner}</table>"


def balance_table_columns(html: str) -> str:
    return re.sub(
        r"(<table[^>]*>)(.*?)</table>",
        _equal_colgroup,
        html,
        flags=re.I | re.S,
    )


def markdown_to_html(md_text: str) -> str:
    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list"],
    )
    body = body.replace("[ ]", "&#9744;").replace("[x]", "&#9745;")
    body = balance_table_columns(body)
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>{CSS}</style></head>
<body>
<div id="footerContent" class="footer">
  Liat (2020) Limited &middot; Factorial AVD operating guide &middot; page <pdf:pagenumber> of <pdf:pagecount>
</div>
{body}
</body>
</html>
"""


def build_pdf(source: Path, out: Path) -> Path:
    md_text = source.read_text(encoding="utf-8")
    md_text = re.sub(r"\n\*End of guide[^\n]*\*\s*$", "\n", md_text)
    html = markdown_to_html(md_text)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as handle:
        result = pisa.CreatePDF(html, dest=handle, encoding="utf-8")
    if result.err:
        raise RuntimeError(f"PDF generation failed with {result.err} error(s)")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Build LIAT AVD SOW PDF")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args()
    out = build_pdf(Path(args.source), Path(args.out))
    print(f"PDF written: {out} ({out.stat().st_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
