import os
from pathlib import Path

import fitz

folder = r"c:\Users\victo\Downloads"
v22 = None
for f in os.listdir(folder):
    if "v2.2" in f and f.endswith(".pdf") and "Implementation" in f:
        v22 = os.path.join(folder, f)
print("v22", v22)

doc = fitz.open(v22)
out = Path(r"c:\Users\victo\Documents\Projetos Random\Ultimate_Collector_Limpo\_ansa_preview")
out.mkdir(exist_ok=True)

for i, page in enumerate(doc):
    pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
    p = out / f"v22_page_{i+1}.png"
    pix.save(str(p))
    print("saved", p.name, pix.width, pix.height)

page = doc[0]
print("--- page1 blocks ---")
for b in page.get_text("dict")["blocks"]:
    if b.get("type") == 0:
        for l in b.get("lines", [])[:1]:
            for s in l.get("spans", [])[:1]:
                print(
                    f"y={b['bbox'][1]:.0f} size={s['size']:.1f} "
                    f"font={s['font'][:25]} text={s['text'][:70]!r}"
                )

for i, page in enumerate(doc):
    print(
        f"page{i+1} drawings={len(page.get_drawings())} "
        f"images={len(page.get_images())} textlen={len(page.get_text() or '')}"
    )
