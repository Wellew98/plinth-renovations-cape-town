"""Builds the site's image set from Plinth's own project photographs.

No stock, no remote URLs: every image is a real Plinth job, resized for web and
written under its search-facing filename from photos.py.
"""
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from photos import HERO, PHOTOS

SRC = Path(r"C:\Users\DELL\OneDrive\Desktop\PLINTH\images")
BRAND = Path(r"C:\Users\DELL\OneDrive\Desktop\PLINTH")
LOGO = BRAND / "logo.jpg"
OUT = Path(__file__).resolve().parent / "_images"
OUT.mkdir(parents=True, exist_ok=True)

# drop the old img-N names so nothing stale ships
for stale in OUT.glob("img-*.jpg"):
    stale.unlink()


def save(im: Image.Image, path: Path, quality=82):
    im.save(path, "JPEG", quality=quality, optimize=True, progressive=True)


def resized(path: Path, max_w: int) -> Image.Image:
    im = Image.open(path).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    return im


# brand media carried over from the original site
shutil.copyfile(BRAND / "logo.jpg", OUT / "logo.jpg")
shutil.copyfile(BRAND / "hero-video.mp4", OUT.parent / "hero-video.mp4")

# hero: wide, because it is the video poster and the social crop source
save(resized(SRC / HERO["src"], 1920), OUT / HERO["file"])

# project photography at 1600 wide, which is all a 2x phone or a retina tile needs
for p in PHOTOS:
    save(resized(SRC / p["src"], 1600), OUT / p["file"])

# header logo: the square gold-on-black lockup, small
logo = Image.open(LOGO).convert("RGB")
logo.thumbnail((320, 320), Image.LANCZOS)
logo.save(OUT / "logo.png", "PNG", optimize=True)

# favicon
fav = Image.open(LOGO).convert("RGB").resize((64, 64), Image.LANCZOS)
fav.save(OUT / "favicon.png", "PNG", optimize=True)

# social cover 1200x630: hero cropped, darkened at the base, brand line over it
cover = Image.new("RGB", (1200, 630), (13, 13, 12))
base = Image.open(OUT / HERO["file"]).convert("RGB")
scale = max(1200 / base.width, 630 / base.height)
base = base.resize((round(base.width * scale), round(base.height * scale)), Image.LANCZOS)
left = (base.width - 1200) // 2
top = (base.height - 630) // 2
cover.paste(base.crop((left, top, left + 1200, top + 630)), (0, 0))

overlay = Image.new("RGBA", cover.size, (0, 0, 0, 0))
d = ImageDraw.Draw(overlay)
for y in range(380, 630):
    a = int(200 * (y - 380) / 250)
    d.line([(0, y), (1200, y)], fill=(13, 13, 12, a))
cover = Image.alpha_composite(cover.convert("RGBA"), overlay).convert("RGB")

d = ImageDraw.Draw(cover)


def font(name, size):
    for candidate in [rf"C:\Windows\Fonts\{name}", r"C:\Windows\Fonts\arialbd.ttf"]:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


d.text((64, 452), "PLINTH RENOVATIONS", font=font("georgiab.ttf", 54), fill=(201, 168, 106))
d.text((66, 522), "Renovations, waterproofing and damp repair, Cape Town",
       font=font("arial.ttf", 26), fill=(240, 238, 232))
d.text((66, 560), "plinthrenovations.co.za  ·  066 150 5770",
       font=font("arial.ttf", 22), fill=(190, 186, 178))
cover.save(OUT.parent / "og-cover.jpg", "JPEG", quality=86, optimize=True)

total = sum(p.stat().st_size for p in OUT.glob("*")) // 1024
print("images written to", OUT)
for p in sorted(OUT.glob("*")):
    print(f"  {p.name:52} {p.stat().st_size // 1024:>4} KB")
print("total", total, "KB")
