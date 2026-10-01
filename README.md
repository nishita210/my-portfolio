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

`site/story/s001–s192.webp` is `Firefly Create one continuous 2D hand-drawn
animation….mp4`, one take that follows the storyboard: wave from the left cliff,
dive, ride the open water, reach the far cliff, climb it, stand on top. It opens
and closes on the storyboard's own framing — both cliffs whole — so the page
starts straight on the film.

Scroll does not run it at a constant rate. Measured, both cliffs are gone by
frame 55, the water is open until 88, the far cliff is solid by 112 and the near
one back by 136. `CUES` in `main.js` holds each act over the stretch of film that
leaves it room, and plays the rest through briskly:

| Act | Scroll | Frames | What the words do |
|---|---|---|---|
| hero | 0.000–0.075 | 1–20 | one line, "scroll to explore" |
| projects | 0.225–0.555 | 56–80 | six cards, one on screen at a time |
| skills | 0.640–0.800 | 96–111 | heading holds, years arrive one by one |
| services | 0.895–1.000 | 162–192 | the four offers arrive one by one |

Between whole frames the canvas dissolves from one to the next, so a slow
stretch of scroll glides rather than steps; once scrolling stops it lands on the
nearest whole frame, so nothing rests double-exposed.

The film is fitted to the width and stood on the foot of the screen, like the
storyboard frames, with paper above for the words. Only a screen wider than 16:9
crops it (top and bottom). Margins follow the storyboard: 112px either side of a
1440 frame (`--gutter`), headings 146px down, the project image spanning
569–1328px.

Hovering the surfer makes her react. `prep_story.py` lifts her out of frame 1 as
`assets/hero-figure.webp` and paints her out of `s001`, so the cut-out can move
without a second copy underneath; from frame 2 the film draws her again.

Hovering either cliff on the opening frame rewrites its chalk label as a list,
as storyboard frames 1a and 1b do — "What I am" becomes designer, traveller,
painter, adventurer; "What I offer" becomes service, UI UX and product design.
`prep_story.py` paints the old label out of frame 1 in the cliff's own colour
and chalks the storyboard's list on (`assets/cliff-am.webp`, `cliff-offer.webp`),
so only the lettering changes. A tap toggles it on touch screens.

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
ffmpeg -i Firefly*.mp4 -vsync 0 scripts/v6/f%03d.png
python3 scripts/prep_story.py     # warms the paper, cuts her out of frame 1 -> scripts/v6clean/
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
- **Skills sit over the approach, not the climb.** The near cliff comes back
  while she climbs, right where the list belongs, so the years arrive while she
  rides toward the far cliff and the climb itself plays without words.
