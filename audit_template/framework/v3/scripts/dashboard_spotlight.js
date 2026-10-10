// Soft decorative cursor light. No tracking storage, network calls or audit edits.
(() => {
  const fine = matchMedia('(hover:hover) and (pointer:fine)');
  const reduced = matchMedia('(prefers-reduced-motion:reduce)');
  const light = document.createElement('div');
  light.className = 'cursorSpotlight';
  light.setAttribute('aria-hidden', 'true');
  document.body.append(light);
  let frame = 0, x = 0, y = 0;
  const allowed = () => fine.matches && !reduced.matches;
  function hide() {
    light.classList.remove('visible');
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
  }
  document.addEventListener('pointermove', event => {
    if (!allowed() || event.pointerType !== 'mouse') return hide();
    x = event.clientX; y = event.clientY;
    if (!frame) frame = requestAnimationFrame(() => {
      frame = 0;
      light.style.transform = `translate3d(${x - 300}px,${y - 300}px,0)`;
      light.classList.add('visible');
    });
  }, {passive:true});
  document.documentElement.addEventListener('pointerleave', hide);
  window.addEventListener('blur', hide);
  document.addEventListener('visibilitychange', () => { if (document.hidden) hide(); });
  fine.addEventListener('change', hide);
  reduced.addEventListener('change', hide);
})();
