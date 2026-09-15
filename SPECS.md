# Fields Salad Bowl — Artwork Spec

Two packaging concepts, both in one viewer (`index.html`), switched with the
**Concept** toggle at the top of the panel:

1. **All-over print** — flood-printed bowl in Fields yellow. Overseas
   production, 10+ week lead time. Sections 1–5 below.
2. **Printed tape** — natural kraft bowl, clear lid, printed band over the top.
   Domestic, short lead time. Section 6 below.

For concept 1 the **bowl size is not yet locked** — the client is choosing
within the 44–52 oz range — so this document covers every candidate. The viewer
recalculates all of it live when you switch sizes.

---

## 1. Candidate sizes (44–52 oz)

Stock sizes actually produced in this range, from published manufacturer spec
sheets, narrowed to the **wide/shallow** profile — the bowls the client has on
hand match that shape. A narrower, taller 44 oz variant exists (165 × 144 ×
75 mm, HMDO) but has been dropped from consideration.

| Size | Nominal | Top × Base × Height | Form | Source |
|---|---|---|---|---|
| 44 oz | 1300 ml | 184 × 161 × 70 mm | wide / shallow | Bioleader PE-SSK44 |
| 48 oz | 1420 ml | 184.9 × 162.1 × 82 mm | wide / deep | Green Paper Products 185-Series |
| 49 oz | 1450 ml | 180 × 160 × 65 mm | wide / shallow | HMDO |
| 51 oz | 1500 ml | 180 × 160 × 70 mm | wide / shallow | HMDO |
| 52 oz | 1500 ml | 185 × 160 × 65 mm | wide / shallow | SoOPAK |

**Nominal capacity is a working fill volume, not the brim.** Suppliers rate
these inconsistently — the 1300 ml Bioleader bowl actually holds ~1638 ml to the
brim, while the 1500 ml SoOPAK holds ~1522 ml. The viewer shows both figures.
Do not use nominal capacity to compare shapes; use the dimensions.

The **185-Series** naming from Green Paper Products is a useful concept: it's a
family sharing a ~185 mm top diameter where only the height changes. Several
suppliers organise their range this way, which means **a size change within a
series keeps the wrap width and only alters its height.**

---

## 2. Design strip per size — *this is what you hand me*

Author artwork as a **plain rectangle**: width = rim circumference, height =
slant height. The viewer wraps it and converts it to the printer's die-line.

| Size (T×B×H) | Strip, mm | Strip @ 300 dpi | Aspect |
|---|---|---|---|
| 184 × 161 × 70 | 578.05 × 70.94 | 6827 × 838 px | 8.15 : 1 |
| 184.9 × 162.1 × 82 | 580.88 × 82.79 | 6861 × 978 px | 7.02 : 1 |
| 180 × 160 × 65 | 565.49 × 65.76 | 6679 × 777 px | 8.60 : 1 |
| 180 × 160 × 70 | 565.49 × 70.71 | 6679 × 835 px | 8.00 : 1 |
| 185 × 160 × 65 | 581.19 × 66.19 | 6865 × 782 px | 8.78 : 1 |

**Artwork is not portable between sizes.** Aspect ratios span 7.02:1 to 8.78:1 —
a strip built for one size stretches noticeably on another. Build final art only
once the size is signed off. Until then, work in vector so rescaling is free,
and use the viewer to sanity-check each candidate.

### Zones within the strip

| Zone | Size | Measured from |
|---|---|---|
| **Print stop — no ink at all** | 5 mm | top edge |
| Base crimp — keep *critical* content clear | 6 mm | bottom edge |
| Bleed | 3 mm | base and both side edges |
| Glue lap | 6 mm | right edge, overlaps the left |

Seam sits at the strip's left/right edges; strip centre is the front of the bowl.
Artwork crossing the seam must be continuous at both edges.

### The print stop

Ink stops 5 mm below the rim edge, and **the flood colour stops with it.** That
band and the rolled bead above it are bare board, so they show the liner —
white or natural kraft — not the Fields yellow. This is the standard look for
printed paper bowls; the Cold Co reference packaging does exactly this.

Two consequences for the artwork file:

- The top 5 mm of the strip must be **completely empty** — no type, no flood, no
  bleed. It is not a "keep type clear" margin, it is the edge of the printed
  area.
- **There is no top bleed.** Bleed still applies at the base and at both seam
  edges, where ink does run off the blank.

**The bottom behaves nothing like the top.** Ink runs all the way to the bottom
edge of the bowl — flood and artwork both — and that is the normal look. The
6 mm base-crimp figure is advisory only: the viewer does not clip there, and
graphics are expected to bleed straight through it. It marks where the sidewall
folds into the base seal, so keep *type and logos* out of it, but run patterns,
flood and illustration off the edge.

The viewer enforces this: the top band is clipped out of the composite, so it
reads as bare board on the model and exports as genuine transparency in the
die-line PNG. With the liner set to *Matches body* the bowl still reads as
continuous yellow, because the liner is then printed to the rim — that is the
alternative, more expensive spec, and it is worth confirming which one the
converter is quoting.

### Colour and transparency

The viewer composites **body colour first, then artwork on top**, so:

- **Logo-only PNG with alpha** is the right deliverable. The Fields yellow shows
  through, and the same file survives a change of flood colour.
- **Full-bleed opaque art** overrides the body entirely.

Body colour is locked to the Fields yellow **`#FCE300`** in the viewer (one
constant, `BODY_COLOUR`, at the top of `tools/index.template.html`).

That hex is the screen reference only. The viewer is deliberately tuned to
render it at full chroma — filmic tone mapping was dropped because it pushed
`#FCE300` to `#E6DC68` on screen, lifting the blue channel to 104 and reading as
cream. The lit face of the bowl now measures `#FEE726`. **Get a Pantone
specified and a printed draw-down before signing off** — a saturated yellow this
close to the edge of gamut is exactly the kind of colour that shifts most
between screen, CMYK and coated stock.

---

### Artwork in the viewer

The all-over artwork is **baked in** from the **`AOP Bowl`** folder beside
`bowl-viewer` — there is no uploader. Drop a PNG in and rerun
`python3 tools/build.py`; it becomes a button in the viewer.

**A leading numeric prefix sets the order and is stripped from the label**, so
`01-poppy-flowers.png` shows as "Poppy flowers". That is how the options are
sequenced — rename to reorder, no code change.

Four options, all **6827 × 838 px** with a transparent ground so the Fields
yellow shows through. The wordmark is poppy `#FD2E02` throughout; only the
dandelion changes. Option 1 loads by default:

| # | File | Dandelion |
|---|---|---|
| 1 | `01-all-red.png` | poppy `#FD2E02` — single ink, everything one colour |
| 2 | `02-poppy-flowers.png` | poppy `#FD2E02` |
| 3 | `03-burgundy-flowers.png` | burgundy `#691934` |
| 4 | `04-green-flowers.png` | forest `#1E3522` |

Option 1 is a **single-ink design** — worth flagging to the converter, since a
one-colour wrap on a flood-yellow bowl may price differently from the two-colour
options.

All three check out against the geometry:

| Check | Result |
|---|---|
| Repeats around the bowl | 2, evenly spaced |
| Seam | clear on both edges — nothing crosses the glue lap |
| Top edge | clears the print stop by **11.2 mm** (1, 4) / **5.9 mm** (2) / **8.9 mm** (3) |
| Bottom edge | ink reaches the base edge, so the stem prints to the bottom of the bowl |

Only type sits inside the crimp zone's 6 mm, and nothing critical does, so the
artwork bleeds off the bottom exactly as intended.

**It is built to the 44 oz strip (8.15:1).** On the other candidate sizes the
aspect runs 7.02:1 to 8.78:1, so the viewer will flag it and stretch. Re-export
once the size is signed off.

## 3. Distortion — the part that bites

A cone does not unroll to a rectangle. Two consequences:

**Horizontal squeeze.** Artwork compresses horizontally toward the base — 11–14 %
depending on size (base circumference vs. rim). A rectangle in the strip becomes
a trapezoid on the bowl, narrowing downward.

**Horizontals become arcs.** A straight horizontal rule in the strip prints as a
curve on the flat die-line. Vertical lines stay straight — they run along the
cone's generatrices.

Practical guidance:

- Keep type and logos **near the vertical centre** of the live area, where the
  squeeze is about half its full value.
- **Short, wide lockups work; tall near-square lockups fight the format.** The
  live area is only 51–72 mm tall against a ~520–580 mm circumference. The square
  `FIELDS / grains & greens` lockup has to shrink a long way to fit the height.
  The horizontal script logo from the yellow render suits this far better.
- Repeating a mark 3× around (every 120°) reads well from any angle.
- Flood colour and full-bleed pattern are unaffected — only recognisable shapes
  and type show the distortion.

---

## 4. Flat die-line (annular sector)

What the printer cuts. The viewer exports it as PNG (300 dpi, 3 mm bleed) and
SVG (cut / bleed / safe paths in millimetres), for whichever size is selected.

| Size (T×B×H) | Inner R | Outer R | Sweep |
|---|---|---|---|
| 184 × 161 × 70 | 496.6 mm | 567.5 mm | 58.36° |
| 184.9 × 162.1 × 82 | 588.6 mm | 671.4 mm | 49.57° |
| 180 × 160 × 65 | 526.1 mm | 591.9 mm | 54.74° |
| 180 × 160 × 70 | 565.7 mm | 636.4 mm | 50.91° |
| 185 × 160 × 65 | 423.6 mm | 489.8 mm | 67.99° |

Derivation — `R` = rim radius, `r` = base radius, `L` = slant height:

```
inner radius = r · L / (R − r)
outer radius = R · L / (R − r)
sweep angle  = 2π (R − r) / L
```

The die-line is drawn apex-down: the **outer arc is the rim**, the inner arc is
the base, and artwork reads upright.

---

## 5. Handoff checklist

- [ ] **Bowl size signed off** — everything below depends on it
- [ ] Supplier's own spec sheet obtained and cross-checked against the viewer
- [ ] Art supplied at the strip size for that specific bowl, 300 dpi
- [ ] Top 5 mm of the strip is completely empty — flood included
- [ ] Nothing critical within 6 mm of the bottom
- [ ] Art bleeds 3 mm past the base and both seam edges (no top bleed)
- [ ] Converter has confirmed whether print stops below the rim or runs over it
- [ ] Seam-crossing art is continuous at the left/right edges
- [ ] Type checked on the bowl in the viewer, not just flat
- [ ] Flood yellow `#FCE300` matched to a Pantone, with a printed draw-down approved
- [ ] CMYK conversion done against that Pantone, not against the screen hex
- [ ] Liner decision made — printed to rim / white / natural kraft
- [ ] Die-line SVG sent alongside the art

---

## 6. Concept two — printed tape

A natural kraft bowl with a clear lid and a printed band running over the top
and down both sides. No printing on the bowl itself, so the only artwork is the
tape. Domestic production.

### Tape

| | |
|---|---|
| Size | **18 × 2.25 in** (457.2 × 57.1 mm) |
| Artwork @ 300 dpi | **5400 × 675 px**, long axis horizontal |
| Adhesive each end | 1.00 in — **not printed** |
| Printed length | 16.00 in |

Supply artwork at the **full 18 in**, not just the printed 16. The viewer paints
the outer inch at each end as adhesive over whatever is there, so the ends can
be left empty or allowed to run off — but the file is the full tape.

### Where the tape actually lands

Measured along the tape from the centre outward, on the 44 oz bowl
(184 × 161 × 70 mm) with a clear lid:

| Zone | Length | Notes |
|---|---|---|
| Bowl top (over the lid) | **7.37 in**, centred | **put the words here** |
| Bowl side | 2.87 in down each wall | |
| Underside | 2.45 in onto the base at each end | includes the 1 in adhesive |

This is the client's brief checked against the geometry, and it holds: they
specified "the top of bowl is approx 6–7 inches so that is where the words
should center", and the lid spans **7.36 in** (187 mm). An 18 in tape is very
close to the right length — the full path over the bowl is 19.4 in, so the tape
stops **0.72 in short of the centre of the underside at each end.** The two ends
do not meet, which is what you want.

Two things worth confirming with the converter:

- **The adhesive inch ends up on the underside**, not on the side wall. If the
  intent was for the tape to stop at the bottom of the wall, the tape wants to
  be about 13.5 in, not 18.
- **Anything wider than 7.37 in of artwork spills off the lid** and onto the
  curved side walls, where it reads at an angle. Load the **Guide** in the
  viewer to see the zone boundaries on the actual bowl.

### Artwork versions

Three colourways are baked into the viewer and switch instantly on the bowl:

| Button | File | Ground | Ink |
|---|---|---|---|
| Lilac on poppy | `lilac-on-poppy.png` | poppy `#FD2E02` | lilac `#C4A9D9` |
| Poppy on lilac | `poppy-on-lilac.png` | lilac `#C4A9D9` | poppy `#FD2E02` |
| Poppy on yellow | `poppy-on-yellow.png` | yellow `#FCE300` | poppy `#FD2E02` |

All three are **5400 × 675 px** — exactly the tape spec, no rescaling.

**The `Bowl Tape` folder beside `bowl-viewer` is the source of truth.** The
viewer has no uploader by design. To add or replace a concept, drop a PNG in
that folder and rerun `python3 tools/build.py`; the button label comes from the
filename, and a numeric prefix (`01-`, `02-`) controls the order.

### Fit check against the lid

All three share one layout. Its ink spans **−83.8 to +84.2 mm** from the tape
centre, against a lid zone of **±93.6 mm** — so the whole mark, dandelion
included, sits on the flat top with **9.4 mm (0.37 in) of clearance at each
end**. Only flat colour runs down the bowl sides.

That clearance is the number to watch if the bowl size changes, since the lid
zone follows the bowl's top diameter:

| Bowl | Lid zone | Clearance |
|---|---|---|
| 44 oz (184 mm) | ±93.6 mm | +9.4 mm |
| 48 oz (184.9 mm) | ±94.1 mm | +9.9 mm |
| 49 / 51 oz (180 mm) | ±91.6 mm | +7.4 mm |
| 52 oz (185 mm) | ±94.1 mm | +9.9 mm |

The layout clears every candidate size, tightest on the 180 mm bowls. Re-run the
check if the artwork grows.

---

## Sources

- [Bioleader — kraft paper compostable salad bowls](https://www.bioleaderpack.com/product/compostable-salad-bowls-kraft-paper/)
- [Green Paper Products — 48 oz 185-Series paper food bowl](https://greenpaperproducts.com/products/48-oz-pla-lined-paper-food-bowl-185-series-bon-appetit-bowls)
- [HMDO Packaging — kraft paper round salad bowl size chart](https://www.hmdopackaging.com/products/1300ml-kraft-paper-round-salad-bowl/)
- [SoOPAK — kraft paper bowl](https://shop.soopak.com/products/kraft-paper-bowl)
