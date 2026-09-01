"""Extract the parent-repo episode decks (epNN/*.pptx) into browsable slide images for the
portal. Read-only on epNN/ — writes only under portal/decks/.

Most episode decks are one full-bleed PNG per slide, so extraction is lossless: we copy the
media bytes out in true slide order. ep09 is a vector deck (PptxGenJS) with almost no
images — we copy its source .pptx instead and mark it non-renderable.

    cd aizentify-cdf-bootcamp
    python tools/extract_decks.py            # all episodes
    python tools/extract_decks.py ep03 ep10  # just these

Needs nothing but the stdlib.
"""
from __future__ import annotations

import json
import pathlib
import re
import shutil
import sys
import zipfile

REPO = pathlib.Path(__file__).resolve().parents[2]          # claude-api-masterclass/
OUT = pathlib.Path(__file__).resolve().parents[1] / "portal" / "decks"

# ep -> (pptx filename, title, bootcamp mapping, blueprint sub-skills, youtube watch link)
EPISODES: dict[str, tuple] = {
    "ep01": ("Coding_Claude_Agents.pptx", "Your First Agent on the Raw Messages API",
             "Day 1 · Lab 4 (agent loop by hand)", "2.3 · 5.1 · 1.1",
             "https://www.youtube.com/watch?v=RheXq2HKJmY"),
    "ep02": ("ppt.pptx", "Same Job on the Claude Agent SDK",
             "Day 3 · M3 (Agent SDK tour)", "1.2 · 1.1", None),
    "ep03": ("ppt.pptx", "Custom Tool: Docstring Coverage Checker",
             "Day 2 · Lab 2 · Day 3 · M7", "8.1 · 8.3", None),
    "ep04": ("episode_4.pptx", "Hooks & Guardrails",
             "Day 3 · M4 · Lab 2 (blocking hook)", "7.3 · 7.2", None),
    "ep05": (None, "Subagents & the Coordinator",
             "Day 3 · M5 · Lab 1 (2-subagent auditor)", "1.1 · 1.3", None),
    "ep06": ("ppt.pptx", "Memory, Sessions & Context That Survives",
             "Day 4 · M6 (context engineering)", "6.1", None),
    "ep07": ("ppt.pptx", "Structured Output You Can Trust",
             "Day 2 · Lab 3 (strict schema + validation)", "6.3", None),
    "ep08": ("ppt.pptx", "Skills: Reusable Agent Capabilities",
             "Day 3 · M6 · Day 4", "3.1 · 8.3", None),
    "ep09": ("ppt.pptx", "MCP in the Real World",
             "Day 3 · M7 · Lab 4 (FastMCP server)", "8.2 · 8.3", None),
    "ep10": ("ppt.pptx", "Choosing Your Model",
             "Day 5 · M1 (trade-off triangle)", "5.3", None),
    "ep11": ("ppt.pptx", "Cost, Tokens & Reliability in Production",
             "Day 5 · M2–5 (caching, batch, fallbacks)", "5.4 · 5.2 · 4.1", None),
    "ep12": ("ppt.pptx", "Managed Agents",
             "Day 5 (hand the runtime to Anthropic)", "1.2", None),
}

_REL = re.compile(r'Id="([^"]+)"[^>]*Target="([^"]+)"')
_SLD = re.compile(r'<p:sldId[^>]*r:id="([^"]+)"')


def _slide_order(z: zipfile.ZipFile) -> list[str]:
    """Return slide part names (ppt/slides/slideN.xml) in presentation order."""
    pres = z.read("ppt/presentation.xml").decode("utf-8", "ignore")
    rels = z.read("ppt/_rels/presentation.xml.rels").decode("utf-8", "ignore")
    rid_to_target = {i: t for i, t in _REL.findall(rels)}
    parts = []
    for rid in _SLD.findall(pres):
        tgt = rid_to_target.get(rid, "")
        if tgt:
            parts.append("ppt/" + tgt.lstrip("/").replace("../", ""))
    return parts


def _slide_image(z: zipfile.ZipFile, slide_part: str) -> str | None:
    """The media part backing a slide, if the slide is a single image."""
    base = slide_part.rsplit("/", 1)[-1]
    rel_part = f"ppt/slides/_rels/{base}.rels"
    try:
        rels = z.read(rel_part).decode("utf-8", "ignore")
    except KeyError:
        return None
    imgs = [t for i, t in _REL.findall(rels) if "/media/" in t]
    if not imgs:
        return None
    return "ppt/" + imgs[0].lstrip("/").replace("../", "")


def extract(ep: str) -> dict:
    fname, title, mapping, blueprint, yt = EPISODES[ep]
    dst = OUT / ep
    dst.mkdir(parents=True, exist_ok=True)
    man = {"ep": ep, "title": title, "mapping": mapping, "blueprint": blueprint,
           "youtube": yt, "renderable": False, "slides": [], "source_pptx": None}

    if fname is None:
        man["note"] = "No deck in the source repo for this episode."
        (dst / "manifest.json").write_text(json.dumps(man, indent=2))
        print(f"{ep}: no pptx — manifest only")
        return man

    src = REPO / ep / fname
    z = zipfile.ZipFile(src)
    parts = _slide_order(z)
    imaged = [(p, _slide_image(z, p)) for p in parts]
    have = sum(1 for _, m in imaged if m)

    if have < len(parts) * 0.6:  # vector deck — ship the source instead
        shutil.copyfile(src, dst / "source.pptx")
        man["source_pptx"] = "source.pptx"
        man["note"] = ("Vector slides (not image-based). Open source.pptx in "
                       "PowerPoint / Keynote / Google Slides.")
        (dst / "manifest.json").write_text(json.dumps(man, indent=2))
        print(f"{ep}: vector deck ({have}/{len(parts)} imaged) — copied source.pptx")
        return man

    for i, (part, media) in enumerate(imaged, 1):
        if not media:
            continue
        ext = media.rsplit(".", 1)[-1].lower()
        name = f"{ep}-{i:02d}.{ext}"
        (dst / name).write_bytes(z.read(media))
        man["slides"].append({"n": i, "img": name})
    man["renderable"] = True
    man["count"] = len(man["slides"])
    man["cover"] = man["slides"][0]["img"] if man["slides"] else None
    (dst / "manifest.json").write_text(json.dumps(man, indent=2))
    print(f"{ep}: {len(man['slides'])} slides -> {dst.relative_to(OUT.parent.parent)}")
    return man


def main(argv: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    eps = argv or list(EPISODES)
    catalog = []
    for ep in eps:
        if ep not in EPISODES:
            print(f"skip {ep}: unknown", file=sys.stderr)
            continue
        m = extract(ep)
        catalog.append({k: m.get(k) for k in
                        ("ep", "title", "mapping", "blueprint", "youtube",
                         "renderable", "count", "cover", "source_pptx", "note")})
    if not argv:  # full run — (re)write the catalog
        (OUT / "catalog.json").write_text(json.dumps(catalog, indent=2))
        print(f"\ncatalog.json: {len(catalog)} episodes")


if __name__ == "__main__":
    main(sys.argv[1:])
