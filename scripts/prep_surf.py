"""Prepare the surf ride that drives the projects act.

Takes the surfing half of the climb video (she reaches the rock at ~f112),
lifts the generator's star watermark, and warms the cool paper it was
rendered on to match the rest of the site.
"""
import glob
import os
import numpy as np
from PIL import Image

SRC = sorted(glob.glob("scripts/v3/f*.png"))[:110]   # surf only, no climb
OUT = "scripts/v3clean"
BOX = (1125, 550, 1215, 645)        # the star sits here in every frame
WM_REF = "scripts/v3/f200.png"      # a frame where flat rock backs the star
PAGE_PAPER = np.array([250.0, 242.0, 226.0])

os.makedirs(OUT, exist_ok=True)
x0, y0, x1, y1 = BOX

# The star is a white alpha blend; solve its alpha where the backing is flat.
ref = np.asarray(Image.open(WM_REF).convert("RGB")).astype(np.float64)[y0:y1, x0:x1]
base = np.median(ref[ref.mean(2) < ref.mean()], axis=0)
alpha = np.clip(((ref - base) / (255.0 - base)).mean(2), 0, 1)
alpha[alpha < 0.05] = 0
a3 = alpha[:, :, None]
print("star alpha peak", round(float(alpha.max()), 3), "px", int((alpha > 0).sum()))

first = np.asarray(Image.open(SRC[0]).convert("RGB")).astype(np.float64)
flat = first[::3, ::3].reshape(-1, 3)
colours, counts = np.unique(flat.astype(np.uint8), axis=0, return_counts=True)
paper = colours[counts.argmax()].astype(np.float64)
shift = PAGE_PAPER - paper
print("paper", paper, "->", PAGE_PAPER)

for f in SRC:
    im = np.asarray(Image.open(f).convert("RGB")).astype(np.float64)
    patch = im[y0:y1, x0:x1]
    im[y0:y1, x0:x1] = np.clip((patch - 255.0 * a3) / (1.0 - a3 + 1e-6), 0, 255)
    # Warm the paper without dragging the ink or the water with it.
    weight = np.clip((im.mean(2) - 200.0) / 40.0, 0, 1)[:, :, None]
    im = np.clip(im + shift * weight, 0, 255)
    Image.fromarray(im.astype(np.uint8)).save(f"{OUT}/{os.path.basename(f)}")
print("prepared", len(SRC), "frames")
