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
from PIL import Image, ImageDraw

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

l, t, r, b = FIGURE_BOX
fw, fh = first.shape[1], first.shape[0]
print("prepared", len(SRC), "frames")
print(f"FIG = {{ x: {l / fw:.4f}, y: {t / fh:.4f}, w: {(r - l) / fw:.4f}, h: {(b - t) / fh:.4f} }}")
