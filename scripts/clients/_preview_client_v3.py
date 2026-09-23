import os
from pathlib import Path

import fitz

folder = r"c:\Users\victo\Downloads"
src = os.path.join(folder, "ANSA_McAL_Factorial_IT_Implementation_Package_Client_v3.pdf")
doc = fitz.open(src)
out = Path(r"c:\Users\victo\Documents\Projetos Random\Ultimate_Collector_Limpo\_ansa_preview")
out.mkdir(exist_ok=True)

extract = out / "client_v3_extract.txt"
with extract.open("w", encoding="utf-8") as f:
    f.write(f"pages={doc.page_count} size={os.path.getsize(src)}\n")
    for i, page in enumerate(doc):
        f.write(f"\n===== PAGE {i+1} =====\n")
        f.write(page.get_text() or "")
        pix = page.get_pixmap(matrix=fitz.Matrix(1.6, 1.6))
        pix.save(str(out / f"client_v3_page_{i+1}.png"))
        print(
            f"page{i+1} drawings={len(page.get_drawings())} "
            f"images={len(page.get_images())} text={len(page.get_text() or '')}"
        )

print("extract", extract)
print("fonts page1", doc[0].get_fonts()[:8])
