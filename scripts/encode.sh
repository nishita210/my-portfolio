#!/bin/sh
# Everything the site serves, from the prepared frames and cut-outs.
set -e
cd "$(dirname "$0")/.."

# The film: one frame per frame of the take, 1200px wide.
mkdir -p site/story
n=0
for f in scripts/v5clean/f*.png; do
  n=$((n + 1))
  cwebp -quiet -q 70 -resize 1200 0 "$f" -o "$(printf 'site/story/s%03d.webp' "$n")"
done
echo "film frames: $n"

# Project thumbnails and the personal photos.
for f in site/assets/p-*.png; do
  cwebp -quiet -q 78 -resize 1200 0 "$f" -o "${f%.png}.webp" && rm "$f"
done
for f in site/assets/photo-*.png; do
  cwebp -quiet -q 80 -resize 700 0 "$f" -o "${f%.png}.webp" && rm "$f"
done
# Cut-outs keep their alpha.
for f in site/assets/pose-*.png site/assets/squiggle.png site/assets/hero-figure.png; do
  [ -f "$f" ] || continue
  cwebp -quiet -q 90 -alpha_q 100 "$f" -o "${f%.png}.webp" && rm "$f"
done

echo "film: $(du -sh site/story | cut -f1)   assets: $(du -sh site/assets | cut -f1)"
