/* Aizentify deck navigation — arrow keys / space / click, + counter + progress bar.
   No dependencies. Every dayN/slides/dayN.html includes this at the end of <body>. */
(function () {
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  if (!slides.length) return;
  var i = 0;

  // chrome
  var counter = document.createElement('div'); counter.id = 'counter';
  var progress = document.createElement('div'); progress.id = 'progress';
  var hint = document.createElement('div'); hint.id = 'hint';
  hint.textContent = '← → to navigate · F for fullscreen';
  document.body.appendChild(counter);
  document.body.appendChild(progress);
  document.body.appendChild(hint);

  function clamp(n) { return Math.max(0, Math.min(slides.length - 1, n)); }

  function show(n) {
    i = clamp(n);
    slides.forEach(function (s, idx) { s.classList.toggle('active', idx === i); });
    counter.textContent = (i + 1) + ' / ' + slides.length;
    progress.style.width = ((i + 1) / slides.length * 100) + '%';
    location.hash = i + 1;
  }

  function next() { hideHint(); show(i + 1); }
  function prev() { hideHint(); show(i - 1); }
  function hideHint() { hint.style.opacity = '0'; }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') { e.preventDefault(); next(); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); prev(); }
    else if (e.key === 'Home') { show(0); }
    else if (e.key === 'End') { show(slides.length - 1); }
    else if (e.key.toLowerCase() === 'f') {
      if (!document.fullscreenElement) document.documentElement.requestFullscreen();
      else document.exitFullscreen();
    }
  });

  // click right half = next, left half = prev
  document.addEventListener('click', function (e) {
    if (e.target.closest('a')) return;
    if (e.clientX > window.innerWidth * 0.5) next(); else prev();
  });

  var start = parseInt(location.hash.replace('#', ''), 10);
  show(isNaN(start) ? 0 : start - 1);
})();
