# assets/img/ — hand-made slide illustrations (build pass B)

Build pass **A** shipped the visual system with **inline-SVG schematic diagrams** (authored
directly in each deck, styled by `.d-*` classes in `aizentify-theme.css`). That is the
default and covers every mental model.

Build pass **B** is optional: drop richer, hand-made illustrations here and wire them onto a
few "hero" slides for extra warmth — the way `ep01/Coding_Claude_Agents.pptx` uses rendered
art for the stateless / tool-anatomy / loop slides.

---

## How to add one

1. Produce the image (NotebookLM, an image model, or a designer) to the brief below.
2. Save it here, named `dayN-<slug>.png` (or `.svg`). Transparent background.
3. In the slide, replace the `<div class="diagram">…</div>` with:
   ```html
   <div class="illo"><img src="../../assets/img/day1-stateless.png" alt="…"></div>
   ```
4. Add to `aizentify-theme.css` (once):
   ```css
   .illo{max-width:900px;margin:.4rem 0}
   .illo img{width:100%;height:auto;border-radius:12px}
   ```
   Keep the SVG version in git history so it can be swapped back.

The `.chip`, `.watch-chip`, and `pre.dim / mark.focus` systems from pass A stay exactly as
they are — illustrations only replace the diagram body.

---

## Illustration brief (house style)

| Spec | Value |
|---|---|
| Canvas | 1600 × ~900 px, **transparent** PNG (or SVG) |
| Ground | designed for the **dark deck** (`#0a0b0d`) — light strokes / fills |
| Palette | brand only: cyan `#3dd1f2`, blue `#1a7ee8` / `#1450e8`, gradient `120deg` cyan→blue; muted `#9ea3a9`; a single warm `#f2b877` allowed for "danger / production" |
| Accent | **one** glowing accent per image (a soft blue/cyan glow), like ep01's orange — used on the element that matters |
| Type in image | avoid baking in body text; short labels only, in a geometric sans; code labels in mono |
| Style | clean technical schematic or light isometric — **not** cartoon mascots (that's a different asset set); think Stripe / Linear docs |
| Consistency | same stroke weight, corner radius, and glow across the whole set |

## Candidate "hero" slides for pass B (Day 1)

| Slide | Illustration idea |
|---|---|
| The API has amnesia | laptop holding a growing stack of message cards ⇄ a server marked "no memory", dashed arrows both ways |
| Anatomy of a request | isometric stacked slabs `model · max_tokens · system · messages` with a big `{` and leader lines |
| The agentic loop | a ring of arrows `Send → Check → Act → Append`, `while True:` glowing in the centre |
| One endpoint | one bright door labelled `/v1/messages`, many small parameter tags feeding into it (tools, vision, PDF, thinking) |

Do the same for Days 2–5 as their decks are built.
