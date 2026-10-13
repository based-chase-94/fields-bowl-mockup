#!/usr/bin/env python3
"""
Artwork template for a wrap strip: a transparent guide overlay (PNG, 300 dpi)
plus vector guides (SVG, millimetres).

    python3 tools/make_template.py "32 oz"
    python3 tools/make_template.py            # every size in PRESETS

The strip is the rectangular design space: width = rim circumference, height =
slant height. Place the PNG as a top layer over artwork at the same pixel size,
or open the SVG in Illustrator as a guide layer.
"""
from PIL import Image, ImageDraw, ImageFont
import math, os, sys

DPI = 300
MM = DPI / 25.4
RIM_SAFE, BASE_SAFE, BLEED = 5.0, 6.0, 3.0      # mm, matching the viewer

# label -> (top OD, base OD, height) in mm
PRESETS = {
    "32 oz": (185, 163, 63),
    "44 oz": (184, 161, 70),
    "48 oz": (184.9, 162.1, 82),
    "49 oz": (180, 160, 65),
    "51 oz": (180, 160, 70),
    "52 oz": (185, 160, 65),
}

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def out_dir():
    cfg = os.path.join(HERE, "artwork-path.local")
    root = os.environ.get("FIELDS_ARTWORK") or (
        open(cfg, encoding="utf-8").read().strip() if os.path.exists(cfg) else None)
    if not root:
        raise SystemExit("set FIELDS_ARTWORK or write artwork-path.local")
    d = os.path.join(root, "Templates")
    os.makedirs(d, exist_ok=True)
    return d


def geom(dT, dB, H):
    Rt, Rb = dT / 2, dB / 2
    slant = math.hypot(Rt - Rb, H)
    arc = math.pi * dT
    return arc, slant


def halo(g, xy, text, fnt, fill):
    """Guides sit over artwork of unknown colour, so every label carries a
    light outline — magenta on poppy is otherwise near-invisible."""
    g.text(xy, text, font=fnt, fill=fill,
           stroke_width=max(2, fnt.size // 8), stroke_fill=(255, 255, 255, 215))


def font(sz):
    try:
        return ImageFont.truetype(F_BOLD, max(10, int(sz)))
    except Exception:
        return ImageFont.load_default()


def make(label):
    dT, dB, H = PRESETS[label]
    arc, slant = geom(dT, dB, H)
    W, Hpx = round(arc * MM), round(slant * MM)
    live = slant - RIM_SAFE - BASE_SAFE

    im = Image.new("RGBA", (W, Hpx), (0, 0, 0, 0))
    g = ImageDraw.Draw(im)
    y_at = lambda mm_: (1 - mm_ / slant) * Hpx          # mm above base -> px
    sm, md = font(Hpx * 0.045), font(Hpx * 0.062)

    # excluded zones: rim roll (no ink) and base crimp (no critical content)
    for y0, y1, lab in ((0, y_at(slant - RIM_SAFE), f"PRINT STOPS — no ink above ({RIM_SAFE:g} mm)"),
                        (y_at(BASE_SAFE), Hpx, f"BASE CRIMP — bleed through, keep type out ({BASE_SAFE:g} mm)")):
        g.rectangle([0, y0, W, y1], fill=(255, 0, 128, 28))
        for x in range(-Hpx, W, int(Hpx * 0.05)):
            g.line([x, y1, x + (y1 - y0), y0], fill=(255, 0, 128, 70), width=3)
        halo(g, (W * 0.5 - Hpx * 2.2, y0 + Hpx * 0.02), lab, md, (192, 0, 106, 255))

    # safe-area boundaries
    for mm_ in (slant - RIM_SAFE, BASE_SAFE):
        y = y_at(mm_)
        for x in range(0, W, int(Hpx * 0.09)):
            g.line([x, y, x + Hpx * 0.05, y], fill=(255, 0, 128, 235), width=max(3, int(Hpx * 0.007)))

    # circumference grid every 30 degrees
    for deg in range(0, 360, 30):
        x = deg / 360 * W
        major = deg % 90 == 0
        g.line([x, 0, x, Hpx], fill=(0, 0, 0, 140 if major else 65),
               width=max(2, int(Hpx * (0.006 if major else 0.004))))
        halo(g, (x + Hpx * 0.018, y_at(slant - RIM_SAFE) + Hpx * 0.02), f"{deg}°",
             sm, (0, 0, 0, 190))

    # slant rules every 10 mm from the base
    for mm_ in range(10, int(slant), 10):
        y = y_at(mm_)
        g.line([0, y, W, y], fill=(0, 0, 0, 65), width=max(2, int(Hpx * 0.003)))
        halo(g, (Hpx * 0.02, y - Hpx * 0.055), f"{mm_} mm", sm, (0, 0, 0, 185))

    # seam and front centre
    lw = max(4, int(Hpx * 0.011))
    for x in (1, W - 2):
        g.line([x, 0, x, Hpx], fill=(212, 0, 0, 255), width=lw)
    halo(g, (Hpx * 0.20, Hpx * 0.42), "SEAM / GLUE LAP", md, (212, 0, 0, 255))
    g.line([W / 2, 0, W / 2, Hpx], fill=(10, 110, 209, 210), width=max(3, int(Hpx * 0.008)))
    halo(g, (W / 2 + Hpx * 0.03, Hpx * 0.42), "FRONT CENTRE", md, (10, 91, 176, 235))

    d = out_dir()
    png = os.path.join(d, f"fields-{label.replace(' ', '')}-wrap-template.png")
    im.save(png, dpi=(DPI, DPI))

    svg = os.path.join(d, f"fields-{label.replace(' ', '')}-wrap-template.svg")
    with open(svg, "w", encoding="utf-8") as f:
        f.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{arc:.2f}mm" height="{slant:.2f}mm" '
            f'viewBox="0 0 {arc:.3f} {slant:.3f}">\n'
            f'<title>Fields {label} wrap template</title>\n'
            f'<desc>Strip = rim circumference x slant height. Units: millimetres. '
            f'Ink stops {RIM_SAFE:g} mm below the rim; the bottom {BASE_SAFE:g} mm is '
            f'crimped into the base (bleed through it, keep type out).</desc>\n'
            '<g fill="none" stroke-width="0.25">\n'
            f'  <rect id="strip" x="0" y="0" width="{arc:.3f}" height="{slant:.3f}" stroke="#FF0000"/>\n'
            f'  <rect id="live-area" x="0" y="{RIM_SAFE:.3f}" width="{arc:.3f}" '
            f'height="{live:.3f}" stroke="#00B050" stroke-dasharray="2 2"/>\n'
            f'  <line id="front-centre" x1="{arc/2:.3f}" y1="0" x2="{arc/2:.3f}" '
            f'y2="{slant:.3f}" stroke="#0070C0"/>\n'
            '</g>\n</svg>\n')

    print(f"{label}: strip {arc:.2f} x {slant:.2f} mm  =  {W} x {Hpx} px @ {DPI} dpi")
    print(f"        live area {live:.2f} mm tall  (ink stops {RIM_SAFE:g} mm below rim, "
          f"{BASE_SAFE:g} mm crimp at base)")
    print(f"        -> {os.path.basename(png)}")
    print(f"        -> {os.path.basename(svg)}")
    return png, svg


if __name__ == "__main__":
    for lab in (sys.argv[1:] or PRESETS.keys()):
        make(lab)
