import "./cursor.js";

/* Scroll drives one thing: which frame of the film is on screen. Everything
   that animates is a caption laid over it — the scene itself only scrubs. */

const FRAMES = 192;
const FRAME_URL = (n) => `story/s${String(n).padStart(3, "0")}.webp`;
const REDUCED = matchMedia("(prefers-reduced-motion: reduce)").matches;
const BLEND_STEPS = 12;   // dissolve levels between two frames
const SETTLE_MS = 140;    // once scrolling stops, land on a whole frame
/* Frame 1 has her painted out — the hover cut-out stands in for her there —
   so the reduced-motion still uses the next frame, where she is drawn. */
const STILL_FRAME = 2;

const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
const ease = (t) => t * t * (3 - 2 * t);

/* Scroll does not run the film at a constant rate. The take has its own
   rhythm (measured): she waves until 20, both cliffs are gone by 55, the
   water is open until 88, the far cliff is solid by 112 and the near one
   back by 136, and she stands on top from 160. Each act is held over the
   stretch of film that leaves it room, and the rest plays through briskly. */
const CUES = [
  [0.000,   1],   // waving from the left cliff
  [0.020,   1],   // held, so she can be said hello to
  [0.075,  20],
  [0.215,  55],   // dived, landed, both cliffs gone
  [0.560,  80],   // the open-water ride, six projects long
  [0.635,  96],   // the far cliff closing in
  [0.800, 111],   // ...held while the years arrive, before the near cliff returns
  [0.890, 160],   // the climb
  [1.000, 192],   // standing on top, both cliffs in shot
];

/** Where each act sits along the scroll. */
const ACTS = {
  hero:     [0.000, 0.075],
  projects: [0.225, 0.555],
  skills:   [0.640, 0.800],
  services: [0.895, 1.000],
};

/** Scroll position -> frame, through the cue points above. */
function frameAt(p) {
  for (let i = 1; i < CUES.length; i++) {
    const [p0, f0] = CUES[i - 1];
    const [p1, f1] = CUES[i];
    if (p <= p1 || i === CUES.length - 1) {
      const t = clamp01((p - p0) / (p1 - p0));
      return f0 + (f1 - f0) * t;
    }
  }
  return FRAMES;
}

/** How far the viewport has travelled through `el`, 0 before, 1 after. */
function progressThrough(el) {
  const r = el.getBoundingClientRect();
  const travel = r.height - innerHeight;
  if (travel <= 0) return clamp01((innerHeight - r.top) / (innerHeight + r.height));
  return clamp01(-r.top / travel);
}

/** 0 where `p` enters [a,b], 1 where it leaves. */
const within = (p, [a, b]) => clamp01((p - a) / (b - a));

// --- the film --------------------------------------------------------------

function filmstrip(canvas, count, url, onReady) {
  const ctx = canvas.getContext("2d", { alpha: false });
  ctx.fillStyle = "#faf2e2";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  const paint = (img) => ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

  if (REDUCED) {
    const still = new Image();
    still.src = url(STILL_FRAME);
    still.onload = () => paint(still);
    onReady?.();
    return { seek() {} };
  }

  const frames = new Array(count);
  const ready = new Array(count).fill(false);
  let loaded = 0;
  let drawn = "";

  /* A fractional frame is drawn as a dissolve between its two neighbours,
     so a slow stretch of scroll glides instead of stepping. */
  function draw(frame) {
    let i = Math.min(count - 1, Math.max(0, Math.floor(frame)));
    while (i >= 0 && !ready[i]) i--;
    if (i < 0) return;
    const next = i + 1 < count && ready[i + 1] ? i + 1 : i;
    const mix = next === i ? 0 : Math.round(clamp01(frame - i) * BLEND_STEPS) / BLEND_STEPS;
    const key = `${i}:${mix}`;
    if (key === drawn) return;
    drawn = key;
    ctx.globalAlpha = 1;
    paint(frames[i]);
    if (mix > 0) {
      ctx.globalAlpha = mix;
      paint(frames[next]);
      ctx.globalAlpha = 1;
    }
  }

  for (let i = 0; i < count; i++) {
    const img = new Image();
    img.decoding = "async";
    img.src = url(i + 1);
    img.onload = () => {
      ready[i] = true;
      if (drawn === "") draw(0);
      if (++loaded > 10) onReady?.();
    };
    img.onerror = () => { loaded++; };
    frames[i] = img;
  }

  return { seek: (frame) => draw(frame - 1) };
}

/** Where a point in a media element's own frame lands on screen. */
function mediaToScreen(el, nw, nh) {
  const box = el.getBoundingClientRect();
  const cs = getComputedStyle(el);
  const pick = cs.objectFit === "contain" ? Math.min : Math.max;
  const s = pick(box.width / nw, box.height / nh);
  const spare = { x: box.width - nw * s, y: box.height - nh * s };
  // object-position: keywords and percentages both, x then y.
  const WORDS = { left: 0, top: 0, center: 0.5, right: 1, bottom: 1 };
  const parts = cs.objectPosition.split(/\s+/);
  const frac = (v, dflt) => {
    if (v in WORDS) return WORDS[v];
    const n = parseFloat(v);
    return Number.isFinite(n) ? n / 100 : dflt;
  };
  return {
    left: box.left + spare.x * frac(parts[0], 0.5),
    top: box.top + spare.y * frac(parts[1] ?? "center", 0.5),
    s,
  };
}

// --- the story -------------------------------------------------------------

function startStory() {
  const story = document.getElementById("story");
  const canvas = document.getElementById("film");
  const loading = document.getElementById("filmLoading");
  if (!story || !canvas) return () => {};

  const film = filmstrip(canvas, FRAMES, FRAME_URL, () => {
    if (loading) loading.hidden = true;
  });

  const acts = [...document.querySelectorAll(".act")];
  const cards = [...document.querySelectorAll(".card")];
  const steps = [...document.querySelectorAll(".timeline li")];
  const offers = [...document.querySelectorAll(".services li")];
  const figure = document.getElementById("heroFigure");
  const poke = document.getElementById("heroPoke");

  const cliffs = [
    // Each relettered label is a patch of frame 1; these are where (from prep_story.py).
    [document.getElementById("cliffAm"),    { x: 0.0422, y: 0.4472, w: 0.1547, h: 0.2972 }],
    [document.getElementById("cliffOffer"), { x: 0.8016, y: 0.4694, w: 0.1734, h: 0.2167 }],
  ].filter(([el]) => el);

  // The cut-out sits exactly where she was painted out of frame 1.
  const FIG = { x: 0.1602, y: 0.0611, w: 0.1953, h: 0.3056 };

  /** Lay `el` over the film at a box given as fractions of the frame. */
  function pin(el, box, withHeight = true) {
    const m = mediaToScreen(canvas, canvas.width, canvas.height);
    el.style.left = `${m.left + box.x * canvas.width * m.s}px`;
    el.style.top = `${m.top + box.y * canvas.height * m.s}px`;
    el.style.width = `${box.w * canvas.width * m.s}px`;
    if (withHeight) el.style.height = `${box.h * canvas.height * m.s}px`;
  }

  function placeFigure() {
    if (figure) pin(figure, FIG, false);
    if (poke) pin(poke, FIG);
    for (const [el, box] of cliffs) pin(el, box);
  }

  // A tap on a touch screen has no hover to end it, so it toggles instead.
  for (const [el] of cliffs) {
    el.addEventListener("click", () => el.classList.toggle("on"));
    el.addEventListener("pointerleave", (e) => {
      if (e.pointerType === "mouse") el.classList.remove("on");
    });
  }

  if (poke && figure) {
    const react = () => {
      figure.classList.remove("poked");
      void figure.offsetWidth;          // restart the keyframes
      figure.classList.add("poked");
    };
    poke.addEventListener("pointerenter", react);
    poke.addEventListener("focus", react);
    poke.addEventListener("click", react);
    figure.addEventListener("animationend", () => figure.classList.remove("poked"));
  }

  placeFigure();
  addEventListener("resize", placeFigure);

  if (REDUCED) {
    acts.forEach((a) => a.classList.add("on"));
    cards.forEach((c) => c.classList.add("on"));
    steps.forEach((s) => s.classList.add("in"));
    offers.forEach((o) => o.classList.add("in"));
    return () => {};
  }

  let settle = 0;
  function showFrame(frame) {
    film.seek(frame);
    // Frame 1 has her painted out and the cut-out standing in. As frame 1
    // dissolves into frame 2 — where the film draws her in the same pose —
    // the cut-out fades by the same amount, so she never thins out.
    const handover = Math.round(clamp01(frame - 1) * BLEND_STEPS) / BLEND_STEPS;
    if (figure) figure.style.opacity = String(1 - handover);
    if (poke) poke.hidden = handover > 0;
    // The lists are lettered onto frame 1, so they only belong there too.
    for (const [el] of cliffs) {
      el.hidden = handover > 0;
      if (el.hidden) el.classList.remove("on");
    }
  }

  /** Reveal a list one item at a time across its act. */
  function cascade(items, t, from, span) {
    items.forEach((el, i) => {
      const at = from + (i / items.length) * span;
      el.classList.toggle("in", t >= at);
    });
  }

  return function onScroll() {
    const p = progressThrough(story);
    showFrame(frameAt(p));
    // A dissolve reads as motion while scrolling, but as a double exposure
    // once it stops — so at rest, land on the nearest whole frame.
    clearTimeout(settle);
    settle = setTimeout(() => showFrame(Math.round(frameAt(progressThrough(story)))), SETTLE_MS);

    for (const act of acts) {
      const [a, b] = ACTS[act.dataset.act];
      act.classList.toggle("on", p >= a && p <= b);
    }

    // One project on screen at a time, handed over as she rides along.
    const tp = within(p, ACTS.projects);
    const slot = Math.min(cards.length - 1, Math.floor(tp * cards.length));
    cards.forEach((c, i) => c.classList.toggle("on", i === slot && tp > 0 && tp < 1));

    // The rock is already there; the years arrive one after another.
    cascade(steps, within(p, ACTS.skills), 0.12, 0.7);
    cascade(offers, within(p, ACTS.services), 0.05, 0.62);

  };
}

// --- wiring ----------------------------------------------------------------

const handlers = [startStory()].filter(Boolean);

function run() { for (const h of handlers) h(); }

let queued = false;
function onScroll() {
  if (queued) return;
  queued = true;
  requestAnimationFrame(() => { queued = false; run(); });
}

addEventListener("scroll", onScroll, { passive: true });
addEventListener("resize", run, { passive: true });
addEventListener("visibilitychange", () => { if (!document.hidden) run(); });
addEventListener("pageshow", run);
run();
document.fonts?.ready.then(run);

const seen = new IntersectionObserver(
  (entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      e.target.classList.add("in");
      seen.unobserve(e.target);
    }
  },
  { rootMargin: "0px 0px -12% 0px" }
);
document.querySelectorAll(".reveal").forEach((el) => seen.observe(el));
