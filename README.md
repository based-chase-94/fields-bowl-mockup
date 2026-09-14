# Fields 44 oz Bowl — 3D wrap viewer

Rotate the bowl, swap flood colours, drop in wrap artwork, and export both a
hero render and a printer-ready die-line. No build step, no dependencies to
install — `lib/three.min.js` is vendored.

See **[SPECS.md](SPECS.md)** for the artwork dimensions and die-line maths.

## Run it

Open `index.html` in a browser. That's it — the default wraps are inlined as
data URIs specifically so the page works straight off disk.

To serve it over HTTP instead (same as GitHub Pages will):

```bash
python3 tools/serve.py
```

Then open <http://localhost:8123/>.

## Using it

| Control | Notes |
|---|---|
| Drag / scroll / double-click | Orbit, zoom, reset |
| **Concept** | *All-over print* (flood-printed bowl) or *Printed tape* (kraft bowl, clear lid, band over the top). Switching rebuilds the whole model |
| **Tape artwork** *(tape mode)* | Colourways baked in from the `Bowl Tape` folder — click to switch. *Guide* shows the zone template, *Blank* is unprinted tape. No uploader: add artwork to that folder and rebuild |
| **Bowl size** | Five stock sizes across 44–52 oz, from real manufacturer spec sheets. Switching rebuilds the model and recalculates every die-line figure |
| **Rim & interior** | The liner — printed to the rim, white board, or natural kraft. Ink stops 5 mm below the rim edge, so on *White* and *Natural kraft* that band and the bead show bare board |
| **Wrap artwork** *(all-over mode)* | Artwork baked in from the `AOP Bowl` folder — click to switch. *Guide* is the calibration grid, *None* is flood colour only |
| **Save view as PNG** | 1×/2×/4×, transparent background unless you tick the backdrop |
| **Die-line PNG** | 300 dpi, 3 mm bleed, alpha outside the cut |
| **Die-line SVG** | Cut / bleed / safe-area paths, in millimetres |

Load **Guide** to see exactly how the cone distorts artwork — vertical lines
stay vertical, horizontals bow, and the bottom squeezes 11–14 %. The demo and
guide wraps are **drawn to fit whichever size is selected**, so they never
misrepresent the aspect ratio.

Artwork supplies colour via alpha: a transparent PNG lets the Fields yellow
(`#FCE300`) show through, which is how the current all-over wrap is built. The renderer uses no tone curve — filmic tone mapping
desaturated that yellow to `#E6DC68` — so the lighting is balanced to land the
lit face on the brand value without clipping away the form. If you change
`BODY_COLOUR` to something much brighter, re-check for clipping. The body colour is deliberately fixed — this is a client-facing tool,
and letting the bowl dimensions or flood colour be dragged around invites
artwork that looks wrong for reasons nobody can trace. To change either, edit
`BODY_COLOUR` or `PRESETS` at the top of `tools/index.template.html` and rebuild.

**Artwork is size-specific.** Strip aspect ratios run from 7.02:1 to 8.78:1
across the candidates, so a strip built for one size stretches on another. See
[SPECS.md](SPECS.md) for the per-size table.

## Source artwork lives outside this repo

`index.html` has every artwork inlined, so the published page is complete. But
the **source folders are not in this repo** — `AOP Bowl` and `Bowl Tape` sit
next to it in the client's working directory and are deliberately not published.

That means **a fresh clone cannot rebuild faithfully**: `tools/build.py` would
find no artwork folders and emit a viewer with empty artwork lists. Rebuild only
from the working directory that has those folders alongside.

## Publishing to GitHub Pages

The folder is already a static site rooted at `index.html`.

Published at **https://based-chase-94.github.io/fields-bowl-mockup/**

To push an update after rebuilding:

```bash
cd bowl-viewer
git add -A && git commit -m "Update artwork" && git push
```

`index.html` and `lib/three.min.js` are all the page needs at runtime; `assets/`,
`tools/` and the markdown ride along as source.

The page carries `<meta name="robots" content="noindex, nofollow">`. The repo is
public because GitHub Pages requires it on the free plan, but the page stays out
of search results. Note that a project-page `robots.txt` would have no effect —
robots.txt is only honoured at a domain root — so the meta tag is doing the work.

## Files

```
index.html                  the viewer — generated, do not hand-edit
lib/three.min.js            three.js r159 (UMD build, works from file://)
assets/
  fields-lockup-white.png   lockup on transparency, extracted from the signage PDF
tools/
  index.template.html       the real source — edit this
  build.py                  inlines the lockup into index.html
  make_assets.py            re-extracts the lockup from the signage PDF
  serve.py                  local static server
SPECS.md                    artwork + die-line specification
```

## Editing

`index.html` is generated. Edit `tools/index.template.html`, then:

```bash
python3 tools/build.py
```

The build inlines the default wraps as data URIs. That is deliberate: a
`file://` page that loads images by relative path taints the canvas, which
breaks both the WebGL texture upload and the die-line export.

The demo and guide wraps are generated in the browser (`drawDemo`, `drawGuide`)
rather than shipped as PNGs, because the strip aspect ratio changes with every
bowl size. Safe-area sizes live in `RIM_SAFE` / `BASE_SAFE` / `BLEED`; the size
list is `PRESETS`.

All artwork is baked in from the client folders next to `bowl-viewer` —
**`AOP Bowl`** for the all-over wrap, **`Bowl Tape`** for the band. Drop a PNG
in and rerun the build: it becomes a button. Neither viewer has an uploader, by
design.

A leading numeric prefix orders the buttons and is stripped from the label, so
`01-poppy-flowers.png` shows as "Poppy flowers". Rename to reorder.

`make_assets.py` only re-extracts the lockup from the signage PDF — you need it
just if that artwork changes:

```bash
python3 tools/make_assets.py && python3 tools/build.py
```

## Console API

`window.FieldsBowl` exposes `spec()`, `strip()`, `dielineCanvas()`,
`dielineSVG()`, `materials`, and `view(azimuth°, elevation°, distance)` for
scripted exports and repeatable camera angles.
