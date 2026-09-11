#!/usr/bin/env python3
"""
Extracts the Fields lockup from the coming-soon signage PDF into a
white-on-transparent PNG, which is the only static artwork the viewer needs.

The wrap strips themselves (demo and safe-area guide) are NOT generated here —
they are drawn in the browser at the selected bowl size, because the strip
aspect ratio changes with every size preset.

    python3 tools/make_assets.py
"""
from PIL import Image, ImageChops
import os, subprocess, tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(HERE, "assets")
SRC_PDF = os.path.abspath(os.path.join(
    HERE, "..", "Coming Soon Print  Signage", "Fields-Window-Lettuce-Green.pdf"))

# The lockup is white on a mid-green ground with a faint lighter watermark.
# Keying on the minimum channel separates white ink from both cleanly.
INK_FLOOR = 160     # below this is background
INK_CEIL = 255
BAND = (600, 1650)  # y-range holding mark + FIELDS + "grains & greens",
                    # excluding the tagline block underneath


def main():
    with tempfile.TemporaryDirectory() as tmp:
        png = os.path.join(tmp, "page.png")
        subprocess.run(["sips", "-s", "format", "png", "--out", png, SRC_PDF],
                       check=True, capture_output=True)
        im = Image.open(png).convert("RGB")

        r, g, b = im.split()
        mn = ImageChops.darker(ImageChops.darker(r, g), b)
        span = INK_CEIL - INK_FLOOR
        alpha = mn.point(lambda v: 0 if v < INK_FLOOR
                         else min(255, int((v - INK_FLOOR) * 255 / span)))

        band = alpha.crop((0, BAND[0], im.width, BAND[1]))
        bx = band.point(lambda v: 255 if v > 20 else 0).getbbox()
        x0, y0, x1, y1 = bx[0], bx[1] + BAND[0], bx[2], bx[3] + BAND[0]

        pad = 12
        crop = alpha.crop((max(0, x0 - pad), max(0, y0 - pad), x1 + pad, y1 + pad))
        out = Image.new("RGB", crop.size, (255, 255, 255)).convert("RGBA")
        out.putalpha(crop)

        path = os.path.join(ASSETS, "fields-lockup-white.png")
        out.save(path)
        print(f"wrote {path}  {out.size}")


if __name__ == "__main__":
    main()
