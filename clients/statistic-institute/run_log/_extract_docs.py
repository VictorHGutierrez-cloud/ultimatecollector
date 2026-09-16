import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

OUT = Path(__file__).resolve().parent


def extract(path: str) -> str:
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    paras = []
    for p in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
        texts = [
            t.text or ""
            for t in p.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t")
        ]
        line = "".join(texts).strip()
        if line:
            paras.append(line)
    return "\n".join(paras)


def clean(text: str) -> str:
    reps = {
        "\u25a1": "[ ]",
        "\uf0b7": "-",
        "\u2019": "'",
        "\u2018": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\xa0": " ",
    }
    for a, b in reps.items():
        text = text.replace(a, b)
    return text


FILES = [
    (
        r"c:\Users\victo\Downloads\PMS TEMPLATES & GUIDELINES_STATIN 2026.docx",
        "_extract_PMS_TEMPLATES_and_GUIDELINES_STATIN_2026.txt",
    ),
    (
        r"c:\Users\victo\Downloads\Statistical Institute of Jamaica Factorial Buisness case socuement.docx",
        "_extract_SIJ_Factorial_Business_Case.txt",
    ),
]


def main() -> None:
    for src, name in FILES:
        text = clean(extract(src))
        out = OUT / name
        out.write_text(text, encoding="utf-8")
        print(f"WROTE {out.name} chars={len(text)} lines={text.count(chr(10))+1}")


if __name__ == "__main__":
    main()
