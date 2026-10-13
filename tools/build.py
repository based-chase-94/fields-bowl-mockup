#!/usr/bin/env python3
"""
Builds index.html from tools/index.template.html, inlining every artwork as a
data URI.

Inlining matters twice over. Opened straight off disk (file://), an
<img src="assets/..."> taints the canvas, which breaks both the WebGL texture
upload and the die-line export — data URIs are same-origin. And it keeps the
published page self-contained: index.html plus lib/three.min.js is the whole
site.

Artwork lives in the client folders beside bowl-viewer, which stay the source
of truth. Drop a PNG in, rerun this, and it becomes a button. The viewer has no
uploader by design.

    python3 tools/build.py
"""
import base64, json, os, re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(HERE, "tools", "index.template.html")
OUT = os.path.join(HERE, "index.html")
EXT = (".png", ".jpg", ".jpeg")

def artwork_root():
    """Where the client's artwork folders live.

    This repo is public, so the path is not committed: set FIELDS_ARTWORK, or
    put the path in artwork-path.local (git-ignored) next to this repo.
    """
    env = os.environ.get("FIELDS_ARTWORK")
    if env:
        return env
    cfg = os.path.join(HERE, "artwork-path.local")
    if os.path.exists(cfg):
        return open(cfg, encoding="utf-8").read().strip()
    raise SystemExit(
        "Artwork folder not configured.\n"
        "  echo '/path/to/Fields' > artwork-path.local\n"
        "  (or export FIELDS_ARTWORK=/path/to/Fields)"
    )


ROOT = artwork_root()

# token -> (source folder, label to use when the folder holds a single file)
ART = {
    "__WRAP_ART__":    (os.path.join(ROOT, "AOP Bowl"), "All-over wrap"),
    "__TAPE_ART__":    (os.path.join(ROOT, "Bowl Tape"), None),
    "__STICKER_ART__": (os.path.join(ROOT, "Bowl Sticker"), "Fields logo"),
}

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


def data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    with open(path, "rb") as f:
        return f"data:{MIME[ext]};base64," + base64.b64encode(f.read()).decode("ascii")


def parse_name(filename):
    """Button label plus any variant the filename pins.

    A leading numeric prefix orders the buttons and is stripped. Optional
    trailing tokens, each introduced by '--', describe the colourway so that one
    click sets the whole bowl:

        05-lavender-flowers--on-FD2E02--32oz.png
        -> label "Lavender flowers", ground #FD2E02, size "32 oz"

    Artwork with no tokens keeps the default body colour and whatever size is
    selected.
    """
    stem = os.path.splitext(filename)[0]
    stem = re.sub(r"^\d+[-_ ]+", "", stem)
    parts = stem.split("--")
    label, ground, size = parts[0], None, None
    for tok in parts[1:]:
        tok = tok.strip()
        m = re.fullmatch(r"on-([0-9A-Fa-f]{6})", tok)
        if m:
            ground = "#" + m.group(1).upper()
            continue
        m = re.fullmatch(r"(\d+)\s*oz", tok, re.I)
        if m:
            size = m.group(1) + " oz"
            continue
        print(f"    warning: unrecognised token {tok!r} in {filename}")
    label = label.replace("-", " ").replace("_", " ").strip()
    return label[:1].upper() + label[1:], ground, size


def scan(folder, single_label):
    """Artwork in a folder, alphabetical. A numeric filename prefix orders them."""
    if not os.path.isdir(folder):
        print(f"  note: {os.path.basename(folder)!r} not found — nothing baked in")
        return []
    files = sorted(f for f in os.listdir(folder) if f.lower().endswith(EXT))
    out = []
    for f in files:
        label, ground, size = parse_name(f)
        if single_label and len(files) == 1:
            label = single_label
        entry = {"name": label, "uri": data_uri(os.path.join(folder, f))}
        if ground:
            entry["ground"] = ground
        if size:
            entry["size"] = size
        extra = "".join(f"  {k}={entry[k]}" for k in ("ground", "size") if k in entry)
        out.append(entry)
        print(f"  {os.path.basename(folder)}/{f}  ->  {label!r}{extra}")
    return out


html = open(TPL, encoding="utf-8").read()
for token, (folder, single) in ART.items():
    if token not in html:
        raise SystemExit(f"token {token} missing from template")
    html = html.replace(token, json.dumps(scan(folder, single), separators=(",", ":")))

open(OUT, "w", encoding="utf-8").write(html)
print(f"wrote {OUT}  ({len(html)/1024:.0f} KB)")
