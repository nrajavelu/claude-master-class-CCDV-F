# Training portal

Static, Aizentify-branded landing pages that wrap the bootcamp materials. No build step, no
server code — plain HTML/CSS/JS. Works opened from disk **or** hosted.

| File | For | What it does |
|---|---|---|
| `index.html` | everyone | Program landing page — schedule, the method, three doors |
| `candidate.html` | candidates | Personal hub. `?c=Name` greets them and namespaces their progress (localStorage). Pre-work checklist + a card per day with per-lab tick-boxes + a progress bar. Internal links carry `?c=` forward. |
| `trainer.html` | trainers | Links to every guide / deck / logistics doc / question file, **and a candidate-link generator** (paste a roster → get one personal link per candidate, copy or CSV). |
| `practice.html` | everyone | Interactive exam-style questions from `questions.js` — pick, check, read the per-distractor rationale. Running score + per-domain tally, saved per candidate. Deep-links: `?day=1`, `?domain=D2`. |
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
Just open `portal/index.html` in a browser. Everything works; the trainer generator will
produce `file://` links which also work on the same machine. For a shared local network,
`python -m http.server` from the `aizentify-cdf-bootcamp/` folder and browse to
`http://<your-ip>:8000/portal/`.

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
