import re
from pathlib import Path

OUT = Path("../site-output")
pages = sorted(OUT.glob("*.html"))
credit = [p.name for p in pages if "Illustrative photograph" in p.read_text(encoding="utf-8")]
stale = [n for n in ("roof-waterproofing-membrane-installation.jpg",
                     "water-damaged-ceiling-damp.jpg")
         if (OUT / "images" / n).exists()]
noimg = [p.name for p in pages if "<img" not in p.read_text(encoding="utf-8")]
print("pages:", len(pages))
print("credits left:", credit)
print("stock files still deployed:", stale)
print("pages with no img:", noimg)
print("images in output:", len(list((OUT / "images").glob("*.jpg"))))
