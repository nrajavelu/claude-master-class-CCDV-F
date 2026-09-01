# Training portal

Static, Aizentify-branded landing pages that wrap the bootcamp materials. No build step, no
server code — plain HTML/CSS/JS. Works opened from disk **or** hosted.

| File | For | What it does |
|---|---|---|
| `index.html` | everyone | Program landing page — schedule, the method, three doors |
| `candidate.html` | candidates | Personal hub. `?c=Name` greets them and namespaces their progress (localStorage). Pre-work checklist + a card per day with per-lab tick-boxes + a progress bar. Internal links carry `?c=` forward. |
| `trainer.html` | trainers | Links to every guide / deck / logistics doc / question file, **and a candidate-link generator** (paste a roster → get one personal link per candidate, copy or CSV). |
| `practice.html` | everyone | Interactive exam-style questions from `questions.js` — pick, check, read the per-distractor rationale. Running score + per-domain tally, saved per candidate. Deep-links: `?day=1`, `?domain=D2`. |
| `view.html` | everyone | **Markdown reader.** `view.html?f=../path/to/file.md` fetches the `.md` and renders it themed (headings, tables, code, task-lists). All `.md` links in the portal route through it; every rendered link opens in a new tab; YouTube deep-links inside a doc are rewritten to the in-portal player. **Requires the portal to be served over http(s)** — see Hosting; on `file://` it shows the raw file instead. Uses `marked` from cdnjs. |
| `watch.html` | everyone | **In-page video player** (YouTube IFrame API, privacy-enhanced embed) — no trip to youtube.com. Three tabs: **Exam walkthrough** (`Lan-CbQ2IKM`, 17 chapters), **Exam guide** (`zEH83eIU5-0`, blueprint), **Build-along course** (one video per episode). Deep links: `watch.html?t=597` (seconds), `watch.html?l=2` (lesson #), `watch.html?s=build&e=3` (build-along episode #). **Paste the remaining build-along episode video IDs into `watch.html` + `../video-companion.md` when you have the playlist.** |
| `decks.html` | everyone | Grid of all 12 build-along **episode decks**, each card showing the cover slide, its bootcamp day/module, exam sub-skills, and a ▶ link into `watch.html`. Data from `decks/catalog.json`. |
| `deck.html` | everyone | **Episode slide viewer** — `deck.html?ep=03&s=7`. Large slide, ◀ ▶ / arrow keys / space, `F` fullscreen, a thumbnail filmstrip, slide counter, and the episode's video deep-link. ep09 (vector) offers its `source.pptx`; ep05 has no deck. Data from `decks/<ep>/manifest.json`. |
| `resources.html` | everyone | Curated **external references** — official Anthropic docs + the CCDV-F exam guide, the three video series, the public study repos the course was cross-checked against, and the Udemy prep course. |
| `cookbooks.html` + `cookbooks/catalog.json` | everyone | **~56 [Claude Cookbooks](https://github.com/anthropics/claude-cookbooks) (Anthropic, MIT)** curated and grouped by CCDV-F domain / bootcamp day. Each card opens the notebook **rendered on GitHub** (reliable, read-only), with **Colab** (run it) and **nbviewer** as alternates. Six recipes are distilled into runnable `../code-snippets/` (`workflow_patterns.py`, `orchestrator_workers.py`, `evaluator_optimizer.py`, `cookbook_building_evals.py`, `usage_cost_api.py`, `extended_thinking.py`). Slugs (`CB:<slug>`) are reference-chip targets in the decks (`data-refs`) and the exam runner (`refs:`). |
| `examples.html` + `../code-snippets/runs/*.md` | everyone | **Worked example per code-snippet** — scenario + real input, the actual code, its **captured output** (predict-then-reveal toggle), "read the output", the exam hook it defends, a tweak to try. No `?f=` → the index grouped by day; `?f=<slug>` → one page. Regenerate output with `python tools/capture_runs.py` (`--mock` offline / `--live` real). The exam runner's `cs:` chips link here. |
| `study.html` + `study/` | everyone | **Hosted study library.** `study/` is the [pjmgomez CCDV-F study web](https://github.com/pjmgomez/claude-certified-developer-foundations) (37 lessons, 14 reference sheets, spaced-review drill), **Apache-2.0**, vendored intact — see `study/VENDORED.md`. `study.html` is an Aizentify shell around it: our nav + a domain/topic sidebar (lessons grouped by their phase → our week), each lesson opening in an `<iframe>`. Deep-link `study.html?p=lessons/0014-prompt-caching.html`. Rebuild the sidebar data with `python tools/build_study_catalog.py` if the vendored copy changes. |
| `portal.css` | — | Shared theme (Aizentify tokens, Sora/Inter, light with a dark hero). Uses the real logo in `../assets/`. |
| `app.js` | — | Shared helpers: query params, per-candidate storage, checklist wiring, progress bars, `?c=` propagation. |
| `questions.js` | — | The practice question bank as data. **Day 1 set (20 items) is in;** append Day 2–5 items in the same shape as those days are built. |

---

## Candidate-specific links

Each candidate gets:

```
<portal-base>/candidate.html?c=Priya%20Sharma
<portal-base>/practice.html?c=Priya%20Sharma
```

`?c=` is only an identifier for **local** progress storage — it is not auth and carries no
secrets. Progress lives in that person's browser (`localStorage`), never leaves the device,
and is per-browser. Generate the links in bulk on `trainer.html`.

---

## Hosting (optional)

### GitHub Pages
1. Repo → **Settings → Pages** → Source: *Deploy from a branch* → `main` / `/ (root)`.
2. Portal base becomes:
   `https://nrajavelu.github.io/claude-master-class-CCDV-F/portal/`
3. Put that into the "Portal base URL" box on `trainer.html` before generating links.

The `.md` files (quizzes, guides) will render as raw text in a browser — that's fine, they're
meant to be read in an editor during the session. The **decks** (`day1-foundations/slides/day1.html`)
and all portal pages render fully.

### Episode decks

`decks.html` / `deck.html` read `portal/decks/`, which is generated from the read-only
`epNN/*.pptx` in the parent repo:

```
python tools/extract_decks.py          # rebuild all 12
python tools/extract_decks.py ep10     # just one
```

Stdlib only. Most episode decks are one full-bleed image per slide, so extraction is
lossless (the PNGs are copied out in true slide order). `deck.html` needs http (`./start.sh`)
so it can `fetch` the manifest.

### Local (no hosting)
Open `portal/index.html` directly and the landing / candidate / trainer / practice pages all
work. **The Markdown reader (`view.html`) needs http**, though — Chrome blocks a `file://`
page from reading sibling files. So for the full experience (rendered guides/quizzes) use the
launcher in the bootcamp root:

```
./start.sh            # serve locally + open the portal in your browser
./start.sh --lan      # also bind 0.0.0.0 and print a shareable http://<your-ip>:PORT/portal/ URL
./start.sh 9000       # pick a port
./stop.sh             # stop it (or just Ctrl+C the start.sh terminal)
```

`start.sh` picks a free port if the default (8000) is taken, waits for the server, prints the
URLs, and opens your browser. Generate candidate links on `trainer.html` using the base URL
it prints.

---

## Extending the practice bank

Add objects to `window.AIZ_QUESTIONS` in `questions.js`:

```js
{ id:"d2-01", day:2, domain:"D6", sub:"Prompt Engineering", style:"SBA",
  stem:"…", options:[{k:"A",t:"…"},{k:"B",t:"…"},{k:"C",t:"…"},{k:"D",t:"…"}],
  answer:["B"],                                  // 2+ keys => multiple-response
  rationale:"why B, and why each distractor is wrong" }
```

`style` is one of SBA · MR · SCN · OUT · BUG · JDG. The domain filter and per-domain scoring
pick up new domains automatically.
