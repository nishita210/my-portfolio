#!/bin/sh
# Hero scrub sequence: every 2nd video frame, 1200px wide.
set -e
cd "$(dirname "$0")/.."
mkdir -p site/frames
n=0; i=0
for f in scripts/clean/f*.png; do
  i=$((i + 1))
  [ $((i % 2)) -eq 1 ] || continue
  n=$((n + 1))
  cwebp -quiet -q 70 -resize 1200 0 "$f" -o "$(printf 'site/frames/f%03d.webp' "$n")"
done
echo "hero frames: $n"

# Project photos: wide crops, no alpha needed.
for f in site/assets/p-*.png; do
  cwebp -quiet -q 78 -resize 1200 0 "$f" -o "${f%.png}.webp" && rm "$f"
done
# Personal photos.
for f in site/assets/photo-*.png; do
  cwebp -quiet -q 80 -resize 700 0 "$f" -o "${f%.png}.webp" && rm "$f"
done
# Cut-outs keep alpha; lossless stays small on flat line art.
for f in site/assets/cliff.png site/assets/pose-*.png site/assets/wave-tile.png \
         site/assets/squiggle.png site/assets/label-*.png; do
  cwebp -quiet -q 88 -alpha_q 100 "$f" -o "${f%.png}.webp" && rm "$f"
done
echo "frames: $(du -sh site/frames | cut -f1)   assets: $(du -sh site/assets | cut -f1)"
