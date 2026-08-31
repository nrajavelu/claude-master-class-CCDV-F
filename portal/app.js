/* Aizentify CDF-F portal — shared helpers. No dependencies. */
(function () {
  const A = (window.AIZ = window.AIZ || {});

  // ---- query params ----
  A.qp = function (k, def) {
    const v = new URLSearchParams(location.search).get(k);
    return v == null ? (def ?? null) : v;
  };

  // ---- per-candidate namespaced storage ----
  A.who = function () {
    const c = (A.qp("c") || A.qp("candidate") || "").trim();
    return c || "guest";
  };
  A.key = function (suffix) {
    return "aiz-cdf::" + A.who().toLowerCase().replace(/\s+/g, "-") + "::" + suffix;
  };
  A.get = function (suffix, def) {
    try {
      const raw = localStorage.getItem(A.key(suffix));
      return raw == null ? def : JSON.parse(raw);
    } catch (e) { return def; }
  };
  A.set = function (suffix, val) {
    try { localStorage.setItem(A.key(suffix), JSON.stringify(val)); } catch (e) {}
  };

  // ---- nav active link ----
  A.markNav = function () {
    const here = location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll(".nav .links a").forEach((a) => {
      if ((a.getAttribute("href") || "").split("?")[0] === here) a.classList.add("active");
    });
  };

  // ---- checklist wiring: any <ul class="checklist" data-store="key"> ----
  A.wireChecklists = function () {
    document.querySelectorAll("ul.checklist[data-store]").forEach((ul) => {
      const store = ul.dataset.store;
      const saved = A.get(store, {});
      const items = [...ul.querySelectorAll("li")];
      items.forEach((li, i) => {
        const cb = li.querySelector('input[type=checkbox]');
        if (!cb) return;
        const id = cb.dataset.id || String(i);
        cb.checked = !!saved[id];
        li.classList.toggle("checked", cb.checked);
        cb.addEventListener("change", () => {
          const s = A.get(store, {});
          s[id] = cb.checked;
          A.set(store, s);
          li.classList.toggle("checked", cb.checked);
          A.refreshProgress();
        });
      });
    });
    A.refreshProgress();
  };

  // ---- aggregate progress bar: <div class="progress" data-scan="store1,store2"><i></i></div> ----
  A.refreshProgress = function () {
    document.querySelectorAll(".progress[data-scan]").forEach((p) => {
      const stores = p.dataset.scan.split(",").map((s) => s.trim());
      let total = 0, done = 0;
      stores.forEach((st) => {
        document.querySelectorAll('ul.checklist[data-store="' + st + '"]').forEach((ul) => {
          const cbs = ul.querySelectorAll('input[type=checkbox]');
          total += cbs.length;
          cbs.forEach((cb) => { if (cb.checked) done++; });
        });
      });
      const pct = total ? Math.round((done / total) * 100) : 0;
      const bar = p.querySelector("i");
      if (bar) bar.style.width = pct + "%";
      const lbl = document.querySelector('[data-progress-label="' + (p.dataset.label || "") + '"]');
      if (lbl) lbl.textContent = done + " / " + total + "  (" + pct + "%)";
    });
  };

  // ---- greet the candidate ----
  A.greet = function () {
    const c = A.who();
    document.querySelectorAll("[data-who]").forEach((el) => {
      el.textContent = c === "guest" ? "there" : c;
    });
    // link every internal portal link back to this candidate
    if (c !== "guest") {
      document.querySelectorAll("a[data-keepc]").forEach((a) => {
        const u = new URL(a.getAttribute("href"), location.href);
        u.searchParams.set("c", c);
        a.setAttribute("href", u.pathname.split("/").pop() + u.search + u.hash);
      });
    }
  };

  document.addEventListener("DOMContentLoaded", function () {
    A.markNav();
    A.greet();
    A.wireChecklists();
  });
})();
