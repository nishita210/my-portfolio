/* The circle cursor, shared by every page. */

function startCursor() {
  const dot = document.getElementById("cursor");
  if (!dot || !matchMedia("(hover: hover) and (pointer: fine)").matches) return;

  document.documentElement.classList.add("has-cursor");
  let x = 0;
  let y = 0;
  let queued = false;

  addEventListener("pointermove", (e) => {
    if (e.pointerType !== "mouse") return;
    x = e.clientX;
    y = e.clientY;
    dot.classList.add("live");
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      dot.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    });
  }, { passive: true });

  addEventListener("pointerout", (e) => {
    if (!e.relatedTarget) dot.classList.remove("live");
  });

  // Swell over anything worth clicking.
  addEventListener("pointerover", (e) => {
    dot.classList.toggle("big", !!e.target.closest?.("a, button, [role=button]"));
  }, { passive: true });
}

startCursor();
