import "./cursor.js";

/* Scroll drives one thing: which frame of the film is on screen. Everything
   that animates is a caption laid over it — the scene itself only scrubs. */

const FRAMES = 192;
const FRAME_URL = (n) => `story/s${String(n).padStart(3, "0")}.webp`;
const REDUCED = matchMedia("(prefers-reduced-motion: reduce)").matches;

const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
const ease = (t) => t * t * (3 - 2 * t);

/* Scroll does not run the film at a constant rate. The cliffs enter and
   leave on the footage's own schedule (measured: the left one is gone by
   frame 91, the right one closes in from frame 121), so the ride is
   stretched over the stretch of open water between them and the rest is
   played through briskly. */
const CUES = [
  [0.00,   1],   // standing on the left cliff
  [0.08,  20],
  [0.26,  62],   // dived, landed on the board
  [0.33,  91],   // left cliff clear of frame
  [0.59, 118],   // the whole ride, held long enough for six projects
  [0.71, 140],   // the far cliff, and a hand on it
  [0.90, 178],   // climbing
  [1.00, 192],   // standing on top
];

/** Where each act sits along the scroll. */
const ACTS = {
  hero:     [0.000, 0.075],
  projects: [0.335, 0.578],
  skills:   [0.745, 0.885],
  services: [0.915, 1.000],
};
const FIGURE_UNTIL = 0.05;    // past this she has moved and the cut-out lies

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
    still.src = url(1);
    still.onload = () => paint(still);
    onReady?.();
    return { seek() {} };
  }

  const frames = new Array(count);
  const ready = new Array(count).fill(false);
  let loaded = 0;
  let drawn = -1;

  function draw(index) {
    let i = Math.min(count - 1, Math.max(0, index));
    while (i >= 0 && !ready[i]) i--;
    if (i < 0 || i === drawn) return;
    drawn = i;
    paint(frames[i]);
  }

  for (let i = 0; i < count; i++) {
    const img = new Image();
    img.decoding = "async";
    img.src = url(i + 1);
    img.onload = () => {
      ready[i] = true;
      if (drawn < 0) draw(0);
      if (++loaded > 10) onReady?.();
    };
    img.onerror = () => { loaded++; };
    frames[i] = img;
  }

  return { seek: (frame) => draw(Math.round(frame) - 1) };
}

/** Where a point in the film's own frame lands on screen, under object-fit. */
function filmToScreen(canvas) {
  const box = canvas.getBoundingClientRect();
  const cs = getComputedStyle(canvas);
  const pick = cs.objectFit === "contain" ? Math.min : Math.max;
  const s = pick(box.width / canvas.width, box.height / canvas.height);
  const spare = { x: box.width - canvas.width * s, y: box.height - canvas.height * s };
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

  // The cut-out sits exactly where she is drawn in frame one.
  const FIG = { x: 0.1375, y: 0.1556, w: 0.1445, h: 0.2194 };

  function placeFigure() {
    if (!figure) return;
    const m = filmToScreen(canvas);
    figure.style.left = `${m.left + FIG.x * canvas.width * m.s}px`;
    figure.style.top = `${m.top + FIG.y * canvas.height * m.s}px`;
    figure.style.width = `${FIG.w * canvas.width * m.s}px`;
    if (poke) {
      const pad = 14;
      poke.style.left = `${m.left + FIG.x * canvas.width * m.s - pad}px`;
      poke.style.top = `${m.top + FIG.y * canvas.height * m.s - pad}px`;
      poke.style.width = `${FIG.w * canvas.width * m.s + pad * 2}px`;
      poke.style.height = `${FIG.h * canvas.height * m.s + pad * 2}px`;
    }
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

  /** Reveal a list one item at a time across its act. */
  function cascade(items, t, from, span) {
    items.forEach((el, i) => {
      const at = from + (i / items.length) * span;
      el.classList.toggle("in", t >= at);
    });
  }

  return function onScroll() {
    const p = progressThrough(story);
    film.seek(frameAt(p));

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

    // The cut-out only tells the truth while she is standing still.
    if (figure) {
      const still = p < FIGURE_UNTIL;
      figure.classList.toggle("gone", !still);
      if (poke) poke.hidden = !still;
      if (still) placeFigure();
    }
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
