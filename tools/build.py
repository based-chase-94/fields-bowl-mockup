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

# token -> (source folder, label to use when the folder holds a single file)
ART = {
    "__WRAP_ART__": (os.path.join(HERE, "..", "AOP Bowl"), "All-over wrap"),
    "__TAPE_ART__": (os.path.join(HERE, "..", "Bowl Tape"), None),
}

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


def data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    with open(path, "rb") as f:
        return f"data:{MIME[ext]};base64," + base64.b64encode(f.read()).decode("ascii")


def label_from(filename):
    """Button label from the filename. A leading numeric prefix orders the
    buttons and is stripped from the label, so 01-poppy-flowers.png shows as
    "Poppy flowers"."""
    stem = os.path.splitext(filename)[0]
    stem = re.sub(r"^\d+[-_ ]+", "", stem)
    stem = stem.replace("-", " ").replace("_", " ").strip()
    return stem[:1].upper() + stem[1:]


def scan(folder, single_label):
    """Artwork in a folder, alphabetical. A numeric filename prefix orders them."""
    if not os.path.isdir(folder):
        print(f"  note: {os.path.basename(folder)!r} not found — nothing baked in")
        return []
    files = sorted(f for f in os.listdir(folder) if f.lower().endswith(EXT))
    out = []
    for f in files:
        name = single_label if (single_label and len(files) == 1) else label_from(f)
        out.append({"name": name, "uri": data_uri(os.path.join(folder, f))})
        print(f"  {os.path.basename(folder)}/{f}  ->  {name!r}")
    return out


html = open(TPL, encoding="utf-8").read()
for token, (folder, single) in ART.items():
    if token not in html:
        raise SystemExit(f"token {token} missing from template")
    html = html.replace(token, json.dumps(scan(folder, single), separators=(",", ":")))

open(OUT, "w", encoding="utf-8").write(html)
print(f"wrote {OUT}  ({len(html)/1024:.0f} KB)")
