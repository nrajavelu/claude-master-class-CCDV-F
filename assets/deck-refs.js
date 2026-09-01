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
  var PORTAL = '../../portal/';

  // ======================================================================
  //  Auto-link file paths mentioned in slide text (<code>…/foo.md</code> etc.)
  //  so "Stuck? labs/lab1_explainer/README.md" is a clickable new-tab link.
  // ======================================================================
  (function linkifyPaths() {
    var seg = location.pathname.split('/').filter(Boolean);          // …/dayN-x/slides/dayN.html
    var dayFolder = seg.length >= 3 ? seg[seg.length - 3] : '';       // "day1-foundations"
    var ROOT_FILES = ['topic-briefings.md', 'blueprint-mastery-map.md', 'curriculum-map.md',
      'reasoning-patterns.md', 'video-companion.md'];
    var ROOT_DIRS = ['question-bank/', 'code-snippets/', 'logistics/', 'evals/',
      'capstone-support-assistant/', 'day0-prework/', 'portal/', 'tools/'];
    var DAY_DIRS = ['labs/', 'mock-exam/', 'slides/'];               // live inside dayN-*/
    var DAY_FILES = ['quiz.md', 'exercises.md', 'exam-style-questions.md',
      'trainer-guide.md', 'recap.html'];
    var pathRe = /^(?:[\w.@-]+\/)*[\w.@-]+\.(md|py|html|jsonl|txt|toml|json|sh)$/;

    function toPortalRel(p) {                       // -> path relative to portal/ (null = can't link)
      if (/^[.~]/.test(p)) return null;                              // .claude/…, ~/…, .mcp.json
      if (/^ep\d\d\//.test(p)) return null;                          // parent repo — not served here
      if (/^day[0-9]/.test(p.split('/')[0])) return '../' + p;       // already day-prefixed
      var i;
      for (i = 0; i < DAY_DIRS.length; i++)
        if (p.indexOf(DAY_DIRS[i]) === 0) return dayFolder ? '../' + dayFolder + '/' + p : null;
      for (i = 0; i < ROOT_DIRS.length; i++)
        if (p.indexOf(ROOT_DIRS[i]) === 0) return '../' + p;
      if (/^domain-[0-9].*\.md$/.test(p)) return '../question-bank/' + p;   // bare domain-N-*.md
      if (p.indexOf('/') === -1) {
        if (ROOT_FILES.indexOf(p) > -1) return '../' + p;
        if (DAY_FILES.indexOf(p) > -1) return dayFolder ? '../' + dayFolder + '/' + p : null;
      }
      return null;                                                  // unknown shape — don't guess
    }

    document.querySelectorAll('.slide code').forEach(function (el) {
      if (el.children.length || el.closest('a') || el.closest('pre')) return;   // skip code blocks / already-linked
      var t = el.textContent.trim();
      if (!pathRe.test(t)) return;
      var rel = toPortalRel(t);
      if (!rel) return;
      var isMd = /\.md$/.test(t);
      var a = document.createElement('a');
      a.href = isMd ? (PORTAL + 'view.html?f=' + encodeURIComponent(rel)) : (PORTAL + rel);
      a.target = '_blank'; a.rel = 'noopener';
      a.className = 'code-link'; a.title = 'Open ' + t + ' in a new tab';
      el.replaceWith(a); a.appendChild(el);
    });
  })();

  var slides = document.querySelectorAll('.slide[data-refs]');
  if (!slides.length) return;

  var lessonByNum = {};   // "14" -> "lessons/0014-prompt-caching.html"
  var titleByFile = {};   // file -> human title
  var cbBySlug = {};      // "caching" -> {title, path}  (Claude Cookbooks)
  var COOKBOOK_BASE = 'https://github.com/anthropics/claude-cookbooks/blob/main/';

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
    if ((m = token.match(/^CB:([a-z0-9-]+)$/i))) {
      var cb = cbBySlug[m[1]];
      if (!cb) return null;
      var url = COOKBOOK_BASE + cb.path;
      return { src: url, ext: url, cookbook: true,
               label: label || ('Cookbook · ' + cb.title) };
    }
    if ((m = token.match(/^cs:([a-z0-9_]+)$/i))) {
      var ex = PORTAL + 'examples.html?f=' + m[1];
      return { src: ex, ext: ex, label: label || ('Worked example · ' + m[1]) };
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
        a.className = 'ref-chip' + (r.video ? ' vid' : '') + (r.cookbook ? ' cb' : '');
        a.href = r.ext; a.textContent = r.label;
        a.title = r.cookbook ? 'Open the cookbook (new tab)'
                : r.video ? 'Play in the portal video player' : 'Open study reference';
        if (r.cookbook) { a.target = '_blank'; a.rel = 'noopener'; }
        a.addEventListener('click', function (e) {
          if (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1) return; // let the browser open a tab
          if (r.cookbook) return;   // nbviewer is cross-origin — just open the tab
          e.preventDefault(); e.stopPropagation();
          openDrawer(r.src, r.ext, r.label);
        });
        row.appendChild(a);
      });
      if (row.children.length) slide.appendChild(row);
    });
  }

  // catalogs are optional — they give Lxx / R:slug / CB:slug nicer labels
  Promise.all([
    fetch(PORTAL + 'study/catalog.json').then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }),
    fetch(PORTAL + 'cookbooks/catalog.json').then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; })
  ]).then(function (res) {
    var c = res[0], cb = res[1];
    if (c) {
      c.lessons.forEach(function (l) { lessonByNum[String(l.n)] = l.file; titleByFile[l.file] = l.title; });
      c.references.forEach(function (r) { titleByFile[r.file] = r.title; });
    }
    if (cb) cb.groups.forEach(function (g) { g.items.forEach(function (it) { cbBySlug[it.slug] = it; }); });
  }).then(build);
})();
