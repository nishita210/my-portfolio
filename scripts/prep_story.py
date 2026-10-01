"""Prepare the end-to-end film that drives the whole scroll.

One take: wave from the left cliff, dive, land on the board, ride the open
water, reach the far cliff, climb it, stand on top. The paper it was rendered
on is a shade off the site's, so it is warmed to match.

The first frame is also split in two: she is lifted out as a cut-out
(site/assets/hero-figure.png) and painted out of the frame itself, so on
hover she can move without a second copy of her showing underneath.
"""
import glob
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = sorted(glob.glob("scripts/v6/f*.png"))
OUT = "scripts/v6clean"
FIGURE_OUT = "site/assets/hero-figure.png"
PAGE_PAPER = np.array([250.0, 242.0, 226.0])

# Her, the board and the "Hi!" bubble on frame 1, in source pixels. The
# bottom edge stops just above the cliff's outline, so the plate keeps it.
FIGURE_BOX = (205, 44, 455, 264)   # left, top, right, bottom (exclusive)
PAPER_TOLERANCE = 30

os.makedirs(OUT, exist_ok=True)

first = np.asarray(Image.open(SRC[0]).convert("RGB")).astype(np.float64)
flat = first[::3, ::3].reshape(-1, 3)
colours, counts = np.unique(flat.astype(np.uint8), axis=0, return_counts=True)
paper = colours[counts.argmax()].astype(np.float64)
shift = PAGE_PAPER - paper
print("paper", paper, "->", PAGE_PAPER, "shift", shift)


def warm(im):
    # Warm the paper without dragging the ink or the water with it.
    weight = np.clip((im.mean(2) - 200.0) / 40.0, 0, 1)[:, :, None]
    return np.clip(im + shift * weight, 0, 255)


def split_figure(im):
    """Return (cut-out RGBA, frame with her painted out)."""
    l, t, r, b = FIGURE_BOX
    box = im[t:b, l:r]
    is_paper = np.abs(box - PAGE_PAPER).sum(2) < PAPER_TOLERANCE
    # Paper reachable from the box edge is background; paper enclosed by
    # ink (inside the board, the bubble) stays part of her.
    mask = Image.fromarray(np.where(is_paper, 255, 0).astype(np.uint8)).copy()
    h, w = is_paper.shape
    for seed in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        if mask.getpixel(seed) == 255:
            ImageDraw.floodfill(mask, seed, 128)
    alpha = np.where(np.asarray(mask) == 128, 0, 255).astype(np.uint8)
    cutout = np.dstack([box.astype(np.uint8), alpha])

    plate = im.copy()
    plate[t:b, l:r] = PAGE_PAPER
    return Image.fromarray(cutout, "RGBA"), plate


for i, f in enumerate(SRC):
    im = warm(np.asarray(Image.open(f).convert("RGB")).astype(np.float64))
    if i == 0:
        cutout, im = split_figure(im)
        cutout.save(FIGURE_OUT)
    Image.fromarray(im.astype(np.uint8)).save(f"{OUT}/{os.path.basename(f)}")

# --- the cliffs' hover lists -------------------------------------------------
# Storyboard frames 1a and 1b rewrite each cliff's chalk label as a list. On
# frame 1 the old label is painted out with the cliff's own colour and the
# list from the storyboard is chalked on in its place; only that patch of
# the frame is saved, so on hover nothing but the lettering changes.
CLIFFS = {
    # name: (old label box, patch box, storyboard frame, list box there, list top-left on the film)
    "am":    ((60, 365, 205, 495), (54, 322, 252, 536), "1a.png", (60, 470, 290, 722), (62, 330)),
    "offer": ((1055, 362, 1236, 488), (1026, 338, 1248, 494), "1b.png", (1148, 478, 1412, 668), (1036, 344)),
}
LIST_SCALE = 0.8          # the film's cliffs are drawn smaller than the storyboard's
CHALK_FLOOR, CHALK_RAMP = 120, 90


def chalk_mask(rgb):
    return np.clip((rgb.mean(2) - CHALK_FLOOR) / CHALK_RAMP, 0, 1)


def cliff_patch(frame, name):
    old, (l, t, r, b), board, (bl, bt, br, bb), (lx, ly) = CLIFFS[name]
    patch = frame[t:b, l:r].copy()
    ink = patch.max(2) < 90
    cliff_colour = np.median(patch[ink], 0)
    chalk_colour = np.median(patch[patch.min(2) > 200], 0)

    # Paint the old label out, a couple of pixels wider than its strokes.
    ox0, oy0, ox1, oy1 = old[0] - l, old[1] - t, old[2] - l, old[3] - t
    region = chalk_mask(patch[oy0:oy1, ox0:ox1]) > 0.05
    grown = Image.fromarray((region * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))
    grown = np.asarray(grown) > 0
    patch[oy0:oy1, ox0:ox1][grown] = cliff_colour

    # Chalk the storyboard's list on, at the film's scale.
    src = chalk_mask(np.asarray(Image.open(board).convert("RGB")).astype(np.float64)[bt:bb, bl:br])
    ys, xs = np.nonzero(src > 0.05)
    src = src[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    a = Image.fromarray((src * 255).astype(np.uint8))
    a = a.resize((round(a.width * LIST_SCALE), round(a.height * LIST_SCALE)), Image.LANCZOS)
    a = np.asarray(a).astype(np.float64)[:, :, None] / 255
    x, y = lx - l, ly - t
    h, w = a.shape[:2]
    assert x + w <= patch.shape[1] and y + h <= patch.shape[0], f"{name}: list overruns its patch"
    patch[y:y + h, x:x + w] = patch[y:y + h, x:x + w] * (1 - a) + chalk_colour * a
    return Image.fromarray(patch.astype(np.uint8)), (l, t, r, b)


frame1 = np.asarray(Image.open(f"{OUT}/{os.path.basename(SRC[0])}").convert("RGB")).astype(np.float64)
for name in CLIFFS:
    img, (l, t, r, b) = cliff_patch(frame1, name)
    img.save(f"site/assets/cliff-{name}.png")
    print(f"cliff-{name}: {{ x: {l / 1280:.4f}, y: {t / 720:.4f}, w: {(r - l) / 1280:.4f}, h: {(b - t) / 720:.4f} }}")

l, t, r, b = FIGURE_BOX
fw, fh = first.shape[1], first.shape[0]
print("prepared", len(SRC), "frames")
print(f"FIG = {{ x: {l / fw:.4f}, y: {t / fh:.4f}, w: {(r - l) / fw:.4f}, h: {(b - t) / fh:.4f} }}")
