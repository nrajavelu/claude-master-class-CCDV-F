# Aizentify deck theme — tokens, rebranding, and authoring notes

All decks in this bootcamp share `assets/aizentify-theme.css` and `assets/deck.js`.
The palette and type mirror **aizentify.com** (`/assets/css/style.css`).

---

## 1. Brand tokens

| Group | CSS var | Value |
|---|---|---|
| Navy (deck ground) | `--navy-950 / 900 / 800 / 700` | `#0a0b0d` `#1a1c20` `#2b2e33` `#3f4348` |
| Blue | `--blue-600 / 500 / 400` | `#1450e8` `#1a7ee8` `#1ea7e8` |
| Cyan (accents) | `--cyan-400 / 300` | `#3dd1f2` `#7fe3f7` |
| Ink (muted text) | `--ink-900 / 700 / 500 / 300` | `#17181b` `#3d4045` `#6c7077` `#9ea3a9` |
| Paper (light surfaces) | `--paper-0 / 50 / 100 / 200`, `--line` | `#ffffff` `#f6f9fc` `#eef3f9` `#e2e9f2` `#dfe6f0` |
| Brand gradient | `--gradient-brand` | `linear-gradient(120deg, #3dd1f2 0%, #1a7ee8 55%, #1450e8 100%)` |
| Head font | `--font-head` | **Sora** → `"Segoe UI", system-ui, sans-serif` |
| Body font | `--font-body` | **Inter** → same fallback |
| Mono font | `--font-mono` | **JetBrains Mono** → `"SF Mono", Consolas, monospace` |

Fonts load from `fonts.googleapis.com`. With no network they fall back to the system stack
and decks still present correctly — only the exact letterforms change.

**Tagline:** *Identify what matters. Intelligently transform how you work.*
**Footer (auto-rendered on every slide):** `Aizentify · Claude Certified Developer – Foundation`
**Copyright line for title/closing slides:** `© 2026 Aizentify LLP`

---

## 2. Logo assets

The **official Aizentify header lockup** is used, downloaded from
`aizentify.com/assets/img/brand-logo-header.png`. It ships in two forms in `assets/`:

| File | What it is | Use |
|---|---|---|
| `brand-logo-header.png` | the official lockup, transparent background, edge-trimmed. Full colour (dark wordmark + blue accent). | light-background surfaces, print, docs |
| `brand-logo-light.png` | the **same lockup** — identical shapes, identical alpha channel — with the foreground knocked out to white (`--paper-50`) so it reads on the dark deck ground. Not a redraw; a monochrome derivative for contrast. | **the decks** (default) |

Trimmed aspect ratio is **6.096 : 1**, exposed as `--brand-logo-aspect` so the slide slot
sizes itself; `--brand-logo` selects which file. To use the full-colour version on a
light-themed deck, set in `aizentify-theme.css`:

```css
--brand-logo: url('./brand-logo-header.png');
```

If Aizentify later supplies an updated or higher-res lockup, replace `brand-logo-header.png`,
regenerate the white version (crop to alpha bbox, keep alpha, set RGB to `#f6f9fc`), and
update `--brand-logo-aspect` to the new `width / height`.

---

## 3. Authoring a slide

Each deck is one HTML file: `dayN-.../slides/dayN.html`. Skeleton:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Day N — Aizentify CDF</title>
  <link rel="stylesheet" href="../../assets/aizentify-theme.css">
</head>
<body>
  <div class="deck">

    <section class="slide title">
      <div class="kicker">Aizentify · Day N</div>
      <h1>Deck title</h1>
      <div class="rule"></div>
      <p class="tag">One-line promise of the day.</p>
    </section>

    <section class="slide section">
      <div class="num">Module 1</div>
      <h1>Section name</h1>
    </section>

    <section class="slide">
      <span class="pill">Concept</span>
      <h2>Slide <span class="accent">headline</span></h2>
      <ul class="clean">
        <li>Point one.</li>
        <li>Point two.</li>
      </ul>
    </section>

    <section class="slide">
      <span class="pill lab">Do this now</span>
      <h2>Lab 1 · <span class="accent">code explainer</span></h2>
      <pre><code>python -m labs.lab1_explainer.solution.explainer sample.py</code></pre>
    </section>

  </div>
  <script src="../../assets/deck.js"></script>
</body>
</html>
```

### Slide-class cheat sheet

| Class on `<section class="slide ...">` | Use |
|---|---|
| *(none)* | standard content slide |
| `title` | opening slide (kicker + h1 + rule + tag) |
| `section` | module divider (num + h1) |

### Component cheat sheet

| Markup | Renders as |
|---|---|
| `<span class="pill">Concept</span>` | small cyan tag |
| `<span class="pill lab">Do this now</span>` | blue "lab" tag |
| `<span class="pill exam">Exam watch</span>` | amber "exam" tag |
| `<h2>Text <span class="accent">word</span></h2>` | headline with gradient word |
| `<ul class="clean">` | ▸-bulleted list |
| `<div class="cols"> … </div>` | 2–3 equal columns |
| `<div class="card"><h3>…</h3>…</div>` | bordered panel |
| `<table class="k">` | compact key/value table |
| `<pre><code> … </code></pre>` | code block (left blue rule) |
| syntax spans | `tok-kw` `tok-str` `tok-num` `tok-com` `tok-fn` |

### Navigation (from `deck.js`)

`→ / Space / PageDown` next · `← / PageUp` prev · `Home` / `End` jump · `F` fullscreen ·
click right half = next, left half = prev. Slide number is in the URL hash (deep-linkable).
`Ctrl/Cmd-P` → "Save as PDF" prints one slide per page.

---

## 4. House style

- **One idea per slide.** If it needs two, it's two slides.
- Headlines are claims, not labels: "Streaming stops the 10-minute timeout", not "Streaming".
- Code slides: ≤ 16 lines visible, highlight the 1–2 lines that matter, cut imports if implied.
- Every lab has a **"Do this now"** cue slide immediately before candidates open the editor.
- Every module ends on a **one-slide recap** (3 bullets) before the next section divider.
- `pill exam` marks anything that is a known certification-question target.
