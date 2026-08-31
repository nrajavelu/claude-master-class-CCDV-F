# Training portal

Static, Aizentify-branded landing pages that wrap the bootcamp materials. No build step, no
server code — plain HTML/CSS/JS. Works opened from disk **or** hosted.

| File | For | What it does |
|---|---|---|
| `index.html` | everyone | Program landing page — schedule, the method, three doors |
| `candidate.html` | candidates | Personal hub. `?c=Name` greets them and namespaces their progress (localStorage). Pre-work checklist + a card per day with per-lab tick-boxes + a progress bar. Internal links carry `?c=` forward. |
| `trainer.html` | trainers | Links to every guide / deck / logistics doc / question file, **and a candidate-link generator** (paste a roster → get one personal link per candidate, copy or CSV). |
| `practice.html` | everyone | Interactive exam-style questions from `questions.js` — pick, check, read the per-distractor rationale. Running score + per-domain tally, saved per candidate. Deep-links: `?day=1`, `?domain=D2`. |
| `view.html` | everyone | **Markdown reader.** `view.html?f=../path/to/file.md` fetches the `.md` and renders it themed (headings, tables, code, task-lists). All `.md` links in the portal route through it. In-doc `.md` links open in the reader too. **Requires the portal to be served over http(s)** — see Hosting; on `file://` it shows the raw file instead. Uses `marked` from cdnjs. |
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
