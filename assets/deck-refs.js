/* Aizentify deck — per-slide study references.
   A slide opts in with  data-refs="L14|Prompt caching ; E11#8|Ep 11 · caching ; V:l11|walkthrough"
     Lxx        -> pjmgomez study lesson number xx      (portal/study/lessons/00xx-*.html)
     R:slug     -> study reference sheet                 (portal/study/reference/<slug>.html)
     ENN#S      -> our episode deck NN, slide S          (portal/deck.html?ep=NN&s=S)
     V:lNN      -> exam-walkthrough video, lesson NN     (portal/watch.html?l=NN)
     V:g#SEC    -> exam-guide video at SEC seconds       (portal/watch.html?s=guide&t=SEC)
     V:eNN      -> build-along video, episode NN         (portal/watch.html?s=build&e=NN)
   Each token may be followed by "|label". Tokens are separated by ";".
   Renders a chip row on the slide; a chip opens a right-side drawer with the target in an
   <iframe> (cmd/middle-click still opens the standalone page in a new tab).
   Loaded AFTER deck.js. No dependencies. */
(function () {
  var slides = document.querySelectorAll('.slide[data-refs]');
  if (!slides.length) return;

  var PORTAL = '../../portal/';
  var lessonByNum = {};   // "14" -> "lessons/0014-prompt-caching.html"
  var titleByFile = {};   // file -> human title

  // ---- drawer ---------------------------------------------------------------
  var dr = document.createElement('div');
  dr.id = 'refdrawer';
  dr.innerHTML =
    '<div class="rd-back"></div>' +
    '<aside class="rd-panel" role="dialog" aria-label="Study reference">' +
      '<header><span class="rd-title"></span>' +
        '<a class="rd-ext" target="_blank" rel="noopener">open in new tab ↗</a>' +
        '<button class="rd-x" aria-label="Close">✕</button></header>' +
      '<iframe title="Study reference" referrerpolicy="no-referrer"></iframe>' +
    '</aside>';
  document.body.appendChild(dr);
  var rdPanel = dr.querySelector('.rd-panel'),
      rdTitle = dr.querySelector('.rd-title'),
      rdExt = dr.querySelector('.rd-ext'),
      rdFrame = dr.querySelector('iframe');

  function openDrawer(src, ext, title) {
    rdFrame.src = src; rdExt.href = ext; rdTitle.textContent = title || 'Study reference';
    dr.classList.add('on');
    document.addEventListener('keydown', keyGuard, true);
  }
  function closeDrawer() {
    dr.classList.remove('on'); rdFrame.src = 'about:blank';
    document.removeEventListener('keydown', keyGuard, true);
  }
  function keyGuard(e) {
    if (e.key === 'Escape') { closeDrawer(); e.stopPropagation(); return; }
    // keep deck.js arrow/space/f nav from firing behind the drawer
    if ([' ', 'ArrowLeft', 'ArrowRight', 'PageUp', 'PageDown', 'Home', 'End'].indexOf(e.key) > -1
        || e.key.toLowerCase() === 'f') { e.stopPropagation(); }
  }
  dr.querySelector('.rd-back').addEventListener('click', function (e) { e.stopPropagation(); closeDrawer(); });
  dr.querySelector('.rd-x').addEventListener('click', function (e) { e.stopPropagation(); closeDrawer(); });
  dr.addEventListener('click', function (e) { e.stopPropagation(); });   // don't trigger deck click-nav

  // ---- resolve a token to {drawerSrc, extHref, label} ---------------------
  function resolve(token, label) {
    token = token.trim();
    var m;
    if ((m = token.match(/^L0*(\d{1,3})$/i))) {
      var file = lessonByNum[String(+m[1])];
      if (!file) return null;
      return { src: PORTAL + 'study/' + file,
               ext: PORTAL + 'study.html?p=' + encodeURIComponent(file),
               label: label || titleByFile[file] || ('Lesson ' + m[1]) };
    }
    if ((m = token.match(/^R:([a-z0-9-]+)$/i))) {
      var rf = 'reference/' + m[1] + '.html';
      return { src: PORTAL + 'study/' + rf,
               ext: PORTAL + 'study.html?p=' + encodeURIComponent(rf),
               label: label || titleByFile[rf] || m[1] };
    }
    if ((m = token.match(/^E(\d{1,2})(?:#(\d{1,3}))?$/i))) {
      var q = 'ep=' + (+m[1]) + (m[2] ? '&s=' + (+m[2]) : '');
      return { src: PORTAL + 'deck.html?' + q, ext: PORTAL + 'deck.html?' + q,
               label: label || ('Episode ' + (+m[1]) + (m[2] ? ' · slide ' + m[2] : '')) };
    }
    if ((m = token.match(/^V:l0*(\d{1,2})$/i))) {
      var w = 'watch.html?l=' + (+m[1]);
      return { src: PORTAL + w, ext: PORTAL + w, video: true,
               label: label || ('Walkthrough · L' + (+m[1])) };
    }
    if ((m = token.match(/^V:g#(\d{1,6})$/i))) {
      var wg = 'watch.html?s=guide&t=' + (+m[1]);
      return { src: PORTAL + wg, ext: PORTAL + wg, video: true, label: label || 'Exam guide' };
    }
    if ((m = token.match(/^V:e0*(\d{1,2})$/i))) {
      var we = 'watch.html?s=build&e=' + (+m[1]);
      return { src: PORTAL + we, ext: PORTAL + we, video: true,
               label: label || ('Build-along · Ep ' + (+m[1])) };
    }
    return null;
  }

  function build() {
    slides.forEach(function (slide) {
      var row = document.createElement('div');
      row.className = 'slide-refs';
      slide.getAttribute('data-refs').split(';').forEach(function (part) {
        if (!part.trim()) return;
        var bits = part.split('|'),
            r = resolve(bits[0], bits.slice(1).join('|').trim());
        if (!r) return;
        var a = document.createElement('a');
        a.className = 'ref-chip' + (r.video ? ' vid' : ''); a.href = r.ext; a.textContent = r.label;
        a.title = r.video ? 'Play in the portal video player' : 'Open study reference';
        a.addEventListener('click', function (e) {
          if (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1) return; // let the browser open a tab
          e.preventDefault(); e.stopPropagation();
          openDrawer(r.src, r.ext, r.label);
        });
        row.appendChild(a);
      });
      if (row.children.length) slide.appendChild(row);
    });
  }

  // catalog is optional — Lxx / R:slug labels get nicer text when it loads
  fetch(PORTAL + 'study/catalog.json')
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (c) {
      if (c) {
        c.lessons.forEach(function (l) { lessonByNum[String(l.n)] = l.file; titleByFile[l.file] = l.title; });
        c.references.forEach(function (r) { titleByFile[r.file] = r.title; });
      }
    })
    .catch(function () {})
    .then(build);
})();
