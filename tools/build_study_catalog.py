"""Regenerate portal/study/catalog.json — the sidebar data for portal/study.html.

Run after updating the vendored pjmgomez study web (portal/study/). Reads the <h1> and
lesson-kicker out of each lesson / reference page; maps their phases to our bootcamp week.

    cd aizentify-cdf-bootcamp
    python tools/build_study_catalog.py

Stdlib only.
"""
import glob
import html
import json
import os
import re

STUDY = os.path.join(os.path.dirname(__file__), "..", "portal", "study")

# their phase -> our bootcamp day(s)
PHASE_DAY = {
    "Phase 0": "Day 0", "Phase 1": "Day 1", "Phase 2": "Day 2–3",
    "Phase 3": "Day 5", "Phase 4": "Day 2", "Phase 5": "Day 3",
    "Phase 6": "Day 3–4", "Phase 7": "Day 5", "Phase 8": "Day 5",
}

# provenance — bump when you re-vendor
SOURCE = "https://github.com/pjmgomez/claude-certified-developer-foundations"
COMMIT = "796012540e396e0cccf612bf7cd94b4e48c36c59"


def _text(pattern, blob):
    m = re.search(pattern, blob, re.S)
    return html.unescape(re.sub("<.*?>", "", m.group(1)).strip()) if m else ""


def main():
    lessons = []
    for p in sorted(glob.glob(os.path.join(STUDY, "lessons", "*.html"))):
        blob = open(p, encoding="utf-8").read()
        rel = "lessons/" + os.path.basename(p)
        kicker = _text(r'<div class="lesson-kicker">(.*?)</div>', blob)
        phase = kicker.split("·")[0].strip() if "·" in kicker else kicker
        lessons.append({
            "file": rel,
            "n": int(re.match(r"(\d+)", os.path.basename(p)).group(1)),
            "title": _text(r"<h1>(.*?)</h1>", blob),
            "phase": kicker,
            "day": PHASE_DAY.get(phase, ""),
        })

    references = []
    for p in sorted(glob.glob(os.path.join(STUDY, "reference", "*.html"))):
        blob = open(p, encoding="utf-8").read()
        references.append({
            "file": "reference/" + os.path.basename(p),
            "title": _text(r"<h1>(.*?)</h1>", blob).rstrip(": ").strip(),
        })

    cat = {"source": SOURCE, "commit": COMMIT, "license": "Apache-2.0",
           "lessons": lessons, "references": references}
    out = os.path.join(STUDY, "catalog.json")
    json.dump(cat, open(out, "w"), indent=2)
    print(f"{out}: {len(lessons)} lessons, {len(references)} references")


if __name__ == "__main__":
    main()
