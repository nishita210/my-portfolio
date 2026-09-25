"""Prepare the end-to-end film that drives the whole scroll.

One take: stand on the left cliff, dive, land on the board, surf right,
reach the far cliff, climb it, stand on top. The paper it was rendered on
is a shade cooler than the site's, so it is warmed to match.
"""
import glob
import os
import numpy as np
from PIL import Image

SRC = sorted(glob.glob("scripts/v5/f*.png"))
OUT = "scripts/v5clean"
PAGE_PAPER = np.array([250.0, 242.0, 226.0])

os.makedirs(OUT, exist_ok=True)

first = np.asarray(Image.open(SRC[0]).convert("RGB")).astype(np.float64)
flat = first[::3, ::3].reshape(-1, 3)
colours, counts = np.unique(flat.astype(np.uint8), axis=0, return_counts=True)
paper = colours[counts.argmax()].astype(np.float64)
shift = PAGE_PAPER - paper
print("paper", paper, "->", PAGE_PAPER, "shift", shift)

for f in SRC:
    im = np.asarray(Image.open(f).convert("RGB")).astype(np.float64)
    # Warm the paper without dragging the ink or the water with it.
    weight = np.clip((im.mean(2) - 200.0) / 40.0, 0, 1)[:, :, None]
    im = np.clip(im + shift * weight, 0, 255)
    Image.fromarray(im.astype(np.uint8)).save(f"{OUT}/{os.path.basename(f)}")
print("prepared", len(SRC), "frames")
