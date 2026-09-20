# Nishita Gupta — scroll portfolio

A one-page site built from the Figma storyboard (`1a, 1b, 1–21.png`) plus two
hand-drawn animations. Scroll is the timeline: two acts are scrubbed frame
sequences, the rest is real HTML with the storyboard's artwork cut out as
transparent layers.

```bash
python3 -m http.server 4173 --directory site
```

No build step, no framework, no dependencies. `site/` is the whole deliverable —
drop it on Netlify, Vercel, GitHub Pages or any static host as-is. 6.7 MB.

## The six acts

| Section | Storyboard | How it moves |
|---|---|---|
| `#hero` | 1a–7 | 120-frame scrub of the leap: stand, dive, cliffs part, splash, surface |
| `#projects` | 8–13 | pinned frame: 110-frame scrub of the surf ride, with the work travelling right-to-left past her, resting on each card |
| `#skills` | 14–17 | rock pinned to the right; ropes draw from each milestone to her hand |
| `#services` | 18–19 | both cliffs ease in from off-frame |
| `#personal` | 20 | photos and closing line reveal on entry |
| `#contact` | 21 | — |

The ride ends exactly as she reaches the rock, which is where the climb act
picks her up.

## Where things come from

- `site/frames/f001–f120.webp` — every 2nd frame of the **dive** video
  (`Surfing_character_hand_drawn_ani…_20260920135918.mp4`).
- `site/surf/s001–s110.webp` — the surfing half of the **ride** video
  (`Woman_surfing_and_climbing_cliff_20260920150256.mp4`); she grabs the rock at
  frame 112, so the climb is cut. Its paper was a cool white, so the frames are
  warmed to the site's cream.
- Both videos carried the generator's star watermark in the same spot. It is a
  white alpha blend, so rather than smudging it out, the alpha is solved against
  a frame where flat rock backs it and then un-blended from every frame.
- `site/assets/*.webp` — cut out of the storyboard PNGs by keying the paper.
  Each frame was rendered on a slightly different cream, so the key detects each
  frame's own paper rather than assuming one colour.

### Regenerating

```bash
python3 scripts/unwatermark.py   # dive video frames  -> scripts/clean/
python3 scripts/prep_surf.py     # ride video frames  -> scripts/v3clean/
python3 scripts/extract.py       # storyboard PNGs    -> site/assets/*.png
./scripts/encode.sh              # everything         -> webp
```

Frame counts live at the top of `site/main.js` as `FRAME_COUNT` and
`SURF_COUNT` — keep them in step with what you encode.

## Things you'll probably want to change

- **Fonts.** Figma outlined all the text on export, so the real typefaces
  weren't recoverable. The site approximates them with Alfa Slab One (display),
  Poppins (body) and Caveat (handwriting). Swap the `<link>` and the
  `--display` / `--body` / `--hand` variables in `style.css`.
- **"View project" buttons** all point at `#contact` — there are no case-study
  pages yet. The Figma export does contain the full tourism and gas-station
  research imagery if you want to build them.
- **Card dwell.** `HOLD` in `startSurf()` is the share of each leg a card rests
  in frame (0.42). Raise it to linger, drop it for a continuous drift.
