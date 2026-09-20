import "./cursor.js";

/* Scroll drives everything: the hero is a scrubbed frame sequence, the
   sections below read their own progress and hand it to CSS as a variable. */

const FRAME_COUNT = 120;
const FRAME_URL = (n) => `frames/f${String(n).padStart(3, "0")}.webp`;
const SURF_COUNT = 110;
const SURF_URL = (n) => `surf/s${String(n).padStart(3, "0")}.webp`;
const REDUCED = matchMedia("(prefers-reduced-motion: reduce)").matches;

const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);

/** How far the viewport has travelled through `el`, 0 before, 1 after. */
function progressThrough(el) {
  const r = el.getBoundingClientRect();
  const travel = r.height - innerHeight;
  if (travel <= 0) return clamp01((innerHeight - r.top) / (innerHeight + r.height));
  return clamp01(-r.top / travel);
}

/** 0 as the element enters the viewport, 1 as it leaves. */
function progressAcross(el) {
  const r = el.getBoundingClientRect();
  return clamp01((innerHeight - r.top) / (innerHeight + r.height));
}

// --- the hero film --------------------------------------------------------

/**
 * A canvas that plays a frame sequence under scroll control.
 * Returns { seek(t) } where t is 0..1, or a still under reduced motion.
 */
function filmstrip(canvas, count, url, onFirstFrames) {
  const ctx = canvas.getContext("2d", { alpha: false });
  ctx.fillStyle = "#faf2e2";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  const paint = (img) => ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

  // Nobody who asked for less motion needs a hundred frames of it.
  if (REDUCED) {
    const still = new Image();
    still.src = url(count);
    still.onload = () => paint(still);
    onFirstFrames?.();
    return { seek() {} };
  }

  const frames = new Array(count);
  const ready = new Array(count).fill(false);
  let loaded = 0;
  let drawn = -1;

  /** Draw the wanted frame, or the nearest earlier one that has arrived. */
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
      if (++loaded > 8) onFirstFrames?.();
    };
    img.onerror = () => { loaded++; };
    frames[i] = img;
  }

  return { seek: (t) => draw(Math.round(clamp01(t) * (count - 1))) };
}

function startFilm() {
  const canvas = document.getElementById("film");
  const hero = document.getElementById("hero");
  const loading = document.getElementById("filmLoading");
  if (!canvas || !hero) return () => {};

  const film = filmstrip(canvas, FRAME_COUNT, FRAME_URL, () => {
    if (loading) loading.hidden = true;
  });

  // Three lines of copy, each holding station over part of the leap.
  const beats = [...document.querySelectorAll(".beat")];
  const WINDOWS = [[0.00, 0.10], [0.13, 0.21], [0.23, 0.31]];
  const LAST_FRAME_AT = 0.86;   // the leap ends here; the rest holds and fades
  const FADE_FROM = 0.9;

  if (REDUCED) {
    beats.forEach((b) => b.classList.add("on"));
    return () => {};
  }

  return function onScroll() {
    const p = progressThrough(hero);
    film.seek(p / LAST_FRAME_AT);
    // Dissolve the sea into the paper before the next act wipes up over it.
    canvas.style.opacity = p < FADE_FROM ? "1" : clamp01((1 - p) / (1 - FADE_FROM)).toFixed(3);
    beats.forEach((beat, i) => {
      const [from, to] = WINDOWS[i];
      beat.classList.toggle("on", p >= from && p < to);
    });
  };
}

// --- the cliffs answer back ------------------------------------------------

/** Where a point in the film's own 1200x675 frame lands on screen. */
function filmToScreen(canvas) {
  const box = canvas.getBoundingClientRect();
  const fit = getComputedStyle(canvas).objectFit;
  const pick = fit === "contain" ? Math.min : Math.max;
  const s = pick(box.width / canvas.width, box.height / canvas.height);
  return {
    left: box.left + (box.width - canvas.width * s) / 2,
    top: box.top + (box.height - canvas.height * s) / 2,
    s,
  };
}

function startCliffs() {
  const wrap = document.getElementById("cliffs");
  const canvas = document.getElementById("film");
  const hero = document.getElementById("hero");
  if (!wrap || !canvas || !hero) return () => {};

  // Boxes measured off the film, as fractions of its frame.
  const AREA = {
    am:    { zone: [0.000, 0.410, 0.250, 1.000], panel: [0.030, 0.495, 0.215, 0.680] },
    offer: { zone: [0.715, 0.410, 1.000, 1.000], panel: [0.795, 0.485, 0.980, 0.670] },
  };
  const STILL_UNTIL = 0.11;   // past this the cliffs start sliding apart

  const place = (el, [a, b, c, d], m) => {
    el.style.left = `${m.left + a * canvas.width * m.s}px`;
    el.style.top = `${m.top + b * canvas.height * m.s}px`;
    el.style.width = `${(c - a) * canvas.width * m.s}px`;
    el.style.height = `${(d - b) * canvas.height * m.s}px`;
  };

  function layout() {
    const m = filmToScreen(canvas);
    for (const [key, area] of Object.entries(AREA)) {
      place(wrap.querySelector(`[data-cliff="${key}"]`), area.zone, m);
      place(wrap.querySelector(`[data-reveal="${key}"]`), area.panel, m);
    }
  }

  for (const zone of wrap.querySelectorAll(".cliff-zone")) {
    const panel = wrap.querySelector(`[data-reveal="${zone.dataset.cliff}"]`);
    const show = () => panel.classList.add("show");
    const hide = () => panel.classList.remove("show");
    zone.addEventListener("pointerenter", show);
    zone.addEventListener("pointerleave", hide);
    zone.addEventListener("focus", show);
    zone.addEventListener("blur", hide);
  }

  layout();
  addEventListener("resize", layout);

  return function onScroll() {
    // They are only there to touch while the cliffs are still standing still.
    const reachable = progressThrough(hero) < STILL_UNTIL;
    wrap.classList.toggle("reachable", reachable);
    if (reachable) layout();
    else wrap.querySelectorAll(".show").forEach((p) => p.classList.remove("show"));
  };
}

// --- give CSS the real height of the pinned act headings ------------------

function measureHeads() {
  for (const head of document.querySelectorAll(".act-head")) {
    head.closest("section").style.setProperty("--head", `${Math.ceil(head.offsetHeight)}px`);
  }
}

// --- the ride: she travels right, so the work travels left ----------------

function startSurf() {
  const act = document.getElementById("projects");
  const canvas = document.getElementById("surf");
  const track = act?.querySelector(".track");
  if (!act || !canvas || !track) return () => {};

  const ride = filmstrip(canvas, SURF_COUNT, SURF_URL);
  if (REDUCED) {
    track.style.overflowX = "auto";   // no pinning, so let them swipe it
    return () => {};
  }

  const stations = track.children.length - 1;
  const HOLD = 0.42;            // share of each leg a card rests in frame

  /** Linear scroll in, card-by-card rhythm out: rest, slide, rest. */
  function stepped(p) {
    if (stations < 1) return 0;
    const leg = 1 / stations;
    const i = Math.min(stations - 1, Math.floor(p / leg));
    const t = (p - i * leg) / leg;
    const m = t < HOLD ? 0 : (t - HOLD) / (1 - HOLD);
    return (i + m * m * (3 - 2 * m)) * leg;
  }

  return function onScroll() {
    const p = progressThrough(act);
    ride.seek(p);                                  // she keeps surfing throughout
    const travel = Math.max(0, track.scrollWidth - innerWidth);
    track.style.transform = `translate3d(${(-stepped(p) * travel).toFixed(1)}px, 0, 0)`;
  };
}

// --- ropes from each milestone to the climber's hand ----------------------

function startClimb() {
  const act = document.getElementById("skills");
  const svg = act?.querySelector(".ropes");
  const rows = [...(act?.querySelectorAll(".timeline li") ?? [])];
  if (!act || !svg || !rows.length) return () => {};

  let paths = [];

  /** Redraw the fan against wherever the rows and the climber actually sit. */
  function layout() {
    const hand = act.querySelector(".climber");
    const box = svg.getBoundingClientRect();
    if (!hand || box.width < 10) return;

    const grip = hand.getBoundingClientRect();
    const hx = grip.left + grip.width * 0.72 - box.left;
    const hy = grip.top + grip.height * 0.12 - box.top;

    svg.setAttribute("viewBox", `0 0 ${box.width} ${box.height}`);
    svg.innerHTML = rows
      .map((row) => {
        const r = row.getBoundingClientRect();
        const y = r.top + Math.min(18, r.height / 2) - box.top;
        const x = r.right - box.left + 16;
        const bend = x + (hx - x) * 0.55;
        return `<path d="M${x.toFixed(1)} ${y.toFixed(1)} C${bend.toFixed(1)} ${y.toFixed(1)}, ` +
               `${bend.toFixed(1)} ${hy.toFixed(1)}, ${hx.toFixed(1)} ${hy.toFixed(1)}"/>` +
               `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="4.5"/>`;
      })
      .join("");

    paths = [...svg.querySelectorAll("path")];
    for (const p of paths) {
      const len = p.getTotalLength();
      p.dataset.len = len;
      p.style.strokeDasharray = len;
      p.style.strokeDashoffset = REDUCED ? 0 : len;
    }
  }

  layout();
  addEventListener("resize", layout);
  document.fonts?.ready.then(layout);
  // the rock and the climber are images; their boxes only exist once decoded
  for (const img of act.querySelectorAll(".rockface img")) {
    if (!img.complete) img.addEventListener("load", layout, { once: true });
  }

  if (REDUCED) return () => {};

  return function onScroll() {
    const p = progressAcross(act);
    paths.forEach((path, i) => {
      const start = 0.2 + (i / paths.length) * 0.4;
      const local = clamp01((p - start) / 0.16);
      path.style.strokeDashoffset = (1 - local) * path.dataset.len;
    });
  };
}

// --- the two cliffs easing back together ----------------------------------

function startGorge() {
  const gorge = document.querySelector(".gorge");
  if (!gorge || REDUCED) return () => {};
  return function onScroll() {
    const p = progressAcross(gorge);
    // They drift in from off-frame, then settle.
    gorge.style.setProperty("--part", `${(1 - clamp01(p * 2)) * -90}px`);
  };
}

// --- wiring ----------------------------------------------------------------

const handlers = [startFilm(), startSurf(), startClimb(), startGorge(), startCliffs()].filter(Boolean);

function run() {
  for (const h of handlers) h();
}

// Scrolling is throttled to a frame; everything else runs straight away,
// because a page loaded in a background tab gets no frames at all until it
// is looked at, and it still has to be laid out correctly when it is.
let queued = false;
function onScroll() {
  if (queued) return;
  queued = true;
  requestAnimationFrame(() => {
    queued = false;
    run();
  });
}

addEventListener("scroll", onScroll, { passive: true });
addEventListener("resize", () => { measureHeads(); run(); }, { passive: true });
addEventListener("visibilitychange", () => { if (!document.hidden) { measureHeads(); run(); } });
addEventListener("pageshow", run);
measureHeads();
run();
// Web fonts land after first paint and change the heading height.
document.fonts?.ready.then(() => { measureHeads(); run(); });

// Reveal blocks as they arrive.
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
