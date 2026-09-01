# Vendored third-party study course

This directory is a **verbatim copy** of the `study/` web app from:

- **Project:** Claude Certified Developer – Foundations (CCDV-F) study repo
- **Author:** pjmgomez
- **Source:** https://github.com/pjmgomez/claude-certified-developer-foundations
- **Commit:** `796012540e396e0cccf612bf7cd94b4e48c36c59` (2026-08-08)
- **License:** Apache License 2.0 — see [`LICENSE`](./LICENSE)

It is redistributed here, unmodified in substance, so the Aizentify CCDV-F cohort has the
material available offline alongside the rest of the bootcamp portal.

## Changes made (as required by Apache-2.0 §4)

1. **`index.html`** — a single hosting banner `<div>` added at the top of `<body>` that
   credits the original author, links the source, and links back to the Aizentify portal.
   No original markup was removed or altered.
2. **`capstone/`** — the runnable `capstone.py` (which makes live Claude API calls) was
   **removed** from this copy. The bootcamp ships its own capstone at
   `../../capstone-support-assistant/`. The original capstone remains available at the
   source repo above.
3. Nothing else is changed. All 37 lessons, 14 reference sheets, the spaced-review drill,
   the progress tracker, the shared CSS/JS, and the author's own theme are as published.

## Not vendored (linked at source instead)

- The **official Anthropic exam PDFs** in the source repo (Exam Guide, Certification Terms,
  Exam Policy) — Anthropic's copyright; linked from `../resources.html`.
- The `compass_artifact_*.md` study guide — linked from `../study.html`.

## Attribution

Portions of this portal © pjmgomez, licensed under Apache-2.0. The Aizentify bootcamp
materials (everything outside this `study/` directory) are separate and are **not** covered
by that license.
