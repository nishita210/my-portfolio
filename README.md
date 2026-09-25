# Nishita Gupta — scroll portfolio

A one-page site built from the Figma storyboard and a single hand-drawn
animation. Scroll is the timeline: it scrubs one continuous take, and every
caption is laid over it. The scene itself never animates — only the words do.

```bash
python3 -m http.server 4173 --directory site
```

No build step, no framework, no dependencies. `site/` is the whole deliverable —
drop it on Netlify, Vercel, GitHub Pages or any static host as-is.

## The film

`site/story/s001–s192.webp` is `Create_animated_surfing_characte….mp4`, one take:
stand on the left cliff, dive, land on the board, ride right, reach the far
cliff, climb it, stand on top. The paper it was rendered on is cooler than the
site's, so the frames are warmed to match.

Scroll does not run it at a constant rate. The cliffs enter and leave on the
footage's own schedule — measured, the left one is clear of frame by 91 and the
far one closes in from 121 — so `CUES` in `main.js` stretches the ride over the
open water between them and plays the rest through briskly. The four acts hang
off that same scroll position:

| Act | Scroll | What the words do |
|---|---|---|
| hero | 0.00–0.075 | one line, "scroll to explore" |
| projects | 0.335–0.578 | six cards, one on screen at a time |
| skills | 0.745–0.885 | heading holds, years arrive one by one |
| services | 0.915–1.00 | the four offers arrive one by one |

Personal and contact follow in ordinary flow once the film is done.

The page opens on `assets/opening.webp` — storyboard frame 2, the only framing
with both cliffs and her standing — and dissolves into the film on the first
stretch of scroll, walking the still onto the film's framing as it goes.

Hovering the surfer makes her react: she is drawn twice, once in the opening
frame and once as a cut-out (`assets/hero-figure.webp`) sitting exactly on top
of it, so she can move without the scene moving with her.

## Case studies

`gas-station`, `aviation`, `healthcare`, `agri-tech`, `retrofit`, `tourism.html`,
in storyboard order. Each is the project's own Figma page exported as one tall
render, with a back link and a link on to the next — except the last, which only
goes back. `scripts/build_projects.py` regenerates them.

## CV

`cv.html` embeds `cv/nishita-gupta-cv.pdf` full height, so it stays sharp at any
zoom and prints properly, with a download button beside the back link.

## Regenerating

```bash
ffmpeg -i Create_animated_*.mp4 -vsync 0 scripts/v5/f%03d.png
python3 scripts/prep_story.py     # warms the paper -> scripts/v5clean/
python3 scripts/extract.py        # storyboard PNGs -> site/assets/*.png
./scripts/encode.sh               # everything -> webp
python3 scripts/build_projects.py # case-study pages
```

`FRAMES` in `site/main.js` must match what `prep_story.py` encodes.

## Deploying

`.github/workflows/deploy.yml` publishes `site/` on every push to `main`.

Pages has to be switched on once by hand — **Settings → Pages → Source →
"GitHub Actions"**. The Actions token is not permitted to create the Pages site
itself, so `configure-pages` fails until that is done.

Every path in the site is relative, so it serves correctly from the
`/my-portfolio/` subpath without any base-path configuration.

## Known limits

- **Fonts are approximations.** Figma outlined all the text on export, so the
  real typefaces were not recoverable. The site uses Alfa Slab One (display),
  Poppins (body) and Caveat (handwriting). Swap the `<link>` and the
  `--display` / `--body` / `--hand` variables in `style.css`.
- **The far cliff is visible during the last projects.** The footage has no
  stretch with neither cliff in frame — the camera hands off directly from one
  to the other — so the ride is timed to keep it to a sliver at the right rather
  than out of shot entirely.
- **The opening is a still, not the film.** The take starts tight on the left
  cliff — the right one only enters at frame 37, by which point she has already
  jumped — so the page opens on storyboard frame 2, which holds both cliffs
  together, and dissolves into the film over the first 360px of scroll. The two
  are different drawings of the same scene, so the crossover is registered on
  shared landmarks (the left cliff's top corner and the waterline below it) but
  cannot overlap exactly.
