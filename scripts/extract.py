"""Cut transparent layers out of the flat storyboard frames.

The frames are flattened renders on near-uniform cream paper (std ~0.5), so a
tight chroma-key against that cream separates the ink. White foam inside the
waves keys out too, which is correct: the page background is the same cream,
so the wave reads exactly as it does in the frame.

The opening act (cliff -> dive -> splash -> surf) comes from the video frame
sequence instead, so only the scenes below it are cut here.
"""
import base64
import io
import os
import re
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = "/Users/kartikey.gupta/Downloads/Portfolio 2026 (2)"
OUT = os.path.join(ROOT, "site", "assets")
KEY_FLOOR, KEY_CEIL = 4, 12      # channel distance: fully clear .. fully opaque

os.makedirs(OUT, exist_ok=True)


def frame(name):
    return np.asarray(Image.open(f"{ROOT}/{name}.png").convert("RGB")).astype(np.int16)


def paper_of(rgb):
    """The frames were rendered on a few different papers; find this one's."""
    flat = rgb[::3, ::3].reshape(-1, 3)
    colours, counts = np.unique(flat, axis=0, return_counts=True)
    return colours[counts.argmax()]


def key_cream(rgb, paper=None):
    if paper is None:
        paper = paper_of(rgb)
    dist = np.abs(rgb - paper).max(axis=2)
    alpha = np.clip((dist - KEY_FLOOR) / (KEY_CEIL - KEY_FLOOR), 0, 1) * 255
    return np.dstack([rgb, alpha]).astype(np.uint8)


def key_white(rgb):
    """Keep only the white chalk lettering, drop the cliff behind it."""
    lum = rgb.mean(axis=2)
    alpha = np.clip((lum - 120) / 90, 0, 1) * 255
    return np.dstack([np.full_like(rgb, 255), alpha]).astype(np.uint8)


def trim(rgba, pad=2, thresh=8):
    a = rgba[:, :, 3]
    ys, xs = np.where(a > thresh)
    if not len(ys):
        return rgba
    return rgba[max(0, ys.min() - pad):ys.max() + 1 + pad,
                max(0, xs.min() - pad):xs.max() + 1 + pad]


def cut(name, src, box, keyer=key_cream, do_trim=True):
    x0, y0, x1, y1 = box
    full = frame(src)
    patch = full[y0:y1, x0:x1]
    rgba = keyer(patch, paper_of(full)) if keyer is key_cream else keyer(patch)
    if do_trim:
        rgba = trim(rgba)
    Image.fromarray(rgba).save(f"{OUT}/{name}.png")
    print(f"{name:14} {rgba.shape[1]}x{rgba.shape[0]}")


# --- the cliff and its chalk labels ---------------------------------------
# Frame 14 holds the only bare cliff (15 has the climber on it); the left one is just its mirror.
cut("cliff", 14, (1176, 386, 1440, 828), do_trim=False)
cut("label-am", 4, (40, 520, 250, 660), keyer=key_white)
cut("label-offer", 4, (1180, 520, 1420, 660), keyer=key_white)

# --- the surfer ------------------------------------------------------------
cut("pose-stand", 19, (1150, 225, 1275, 401))     # on the cliff, board in hand
cut("pose-surf", 8, (120, 715, 340, 900))
cut("pose-climb", 15, (1118, 548, 1262, 785))
cut("pose-point", 21, (1272, 720, 1410, 958))

# --- closing scene ---------------------------------------------------------
cut("pose-hips", 20, (1262, 738, 1418, 962))
cut("squiggle", 21, (0, 946, 1440, 1000), do_trim=False)


# --- a seamless wave tile --------------------------------------------------
# One clean span of the intro wave, mirrored, so it repeats across any width.
f2 = frame(2)
half = trim(key_cream(f2[812:1024, 320:1040], paper_of(f2)), pad=0, thresh=4)
tile = np.concatenate([half, half[:, ::-1]], axis=1)
Image.fromarray(tile).save(f"{OUT}/wave-tile.png")
print(f"{'wave-tile':14} {tile.shape[1]}x{tile.shape[0]}")


# --- assets Figma already stores with alpha --------------------------------
def from_svg(svg, index, name):
    s = open(f"{FIG}/{svg}", encoding="utf-8", errors="replace").read()
    data = re.findall(r'xlink:href="data:image/png;base64,([A-Za-z0-9+/=]+)"', s)
    im = Image.open(io.BytesIO(base64.b64decode(data[index])))
    im.save(f"{OUT}/{name}.png")
    print(f"{name:14} {im.width}x{im.height}  ({svg} #{index})")


from_svg("20.svg", 1, "photo-surf")
from_svg("20.svg", 2, "photo-hike")
for i, (svg, name) in enumerate([("8.svg", "p-agritech"), ("9.svg", "p-retrofit"),
                                 ("10.svg", "p-healthcare"), ("11.svg", "p-gas"),
                                 ("12.svg", "p-aviation"), ("13.svg", "p-tourism")]):
    from_svg(svg, 1, name)
