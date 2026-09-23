"""Inspect text positions in ANSA v2.2 PDF for surgical edits."""
import os
from pathlib import Path

import fitz

folder = r"c:\Users\victo\Downloads"
src = None
for f in os.listdir(folder):
    if "v2.2" in f and f.endswith(".pdf") and "Implementation" in f:
        src = os.path.join(folder, f)
doc = fitz.open(src)

needles = [
    "Companion workbook",
    "POC requirement",
    "Android remote lock",
    "Named resale partners",
    "SOLUTION OUTLINE",
    "GAP ANALYSIS",
    "TWELVE LIFECYCLE",
    "TARGET OPERATING MODEL",
    "11. SECURITY",
    "12. DELIVERABLES",
    "13. Investment",
    "2 × USD 2,500",
    "2 × USD 2,500",
    "PS instalment",
    "PS instalments",
    "companion workbook",
    "R-01",
    "R-09",
    "Included in platform",
    "Payment plan",
    "see workbook",
]

out = Path(r"c:\Users\victo\Documents\Projetos Random\Ultimate_Collector_Limpo\_ansa_preview\hits.txt")
lines = []
for i, page in enumerate(doc):
    for n in needles:
        for rect in page.search_for(n):
            lines.append(f"p{i+1} y={rect.y0:.1f}-{rect.y1:.1f} x={rect.x0:.1f} | {n!r}")
    # also find exact money strings with variants
    for n in ["USD 2,500", "2 ×", "2 x", "instalment 1/2", "instalment 2/2"]:
        for rect in page.search_for(n):
            lines.append(f"p{i+1} y={rect.y0:.1f}-{rect.y1:.1f} | money:{n!r}")

out.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {len(lines)} hits to {out}")
for L in lines[:80]:
    print(L)
