"""Remove the generator's star watermark from the surfer video frames.

The star is a fixed-position white alpha blend: out = base*(1-a) + 255*a.
Frames 1..~120 have it sitting on flat cliff black, so the per-pixel alpha
can be solved there exactly and then un-blended from every frame.
"""
import glob
import os
import numpy as np
from PIL import Image

BOX = (1125, 550, 1215, 645)          # x0, y0, x1, y1 around the star
SRC = sorted(glob.glob("scripts/vidframes/f*.png"))
OUT = "scripts/clean"
os.makedirs(OUT, exist_ok=True)

x0, y0, x1, y1 = BOX
ref = np.asarray(Image.open(SRC[0]).convert("RGB")).astype(np.float64)[y0:y1, x0:x1]
# the cliff behind the star is flat: its colour is the region's dark mode
base = np.median(ref[ref.mean(2) < ref.mean() ], axis=0)
alpha = ((ref - base) / (255.0 - base)).mean(2)
alpha = np.clip(alpha, 0, 1)
alpha[alpha < 0.05] = 0                # keep paper grain out of the mask
print("alpha peak", alpha.max().round(3), "covered px", int((alpha > 0).sum()))

a3 = alpha[:, :, None]
for f in SRC:
    im = np.asarray(Image.open(f).convert("RGB")).astype(np.float64)
    patch = im[y0:y1, x0:x1]
    im[y0:y1, x0:x1] = np.clip((patch - 255.0 * a3) / (1.0 - a3 + 1e-6), 0, 255)
    Image.fromarray(im.astype(np.uint8)).save(os.path.join(OUT, os.path.basename(f)))
print("cleaned", len(SRC), "frames")
