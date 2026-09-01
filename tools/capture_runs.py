"""Run each code-snippet and splice its SOURCE + real STDOUT into the matching
worked-example page under code-snippets/runs/<name>.md.

    cd aizentify-cdf-bootcamp
    python tools/capture_runs.py            # --mock (offline fake anthropic SDK), all snippets
    python tools/capture_runs.py --live     # real API key + spend, all snippets
    python tools/capture_runs.py workflow_patterns prompt_caching   # just these

Each runs/<name>.md must contain these marker pairs (they are replaced in place):
    <!-- CODE:START -->  ... <!-- CODE:END -->
    <!-- OUTPUT:START --> ... <!-- OUTPUT:END -->

Stdlib only. --mock installs code-snippets/_mockanthropic (canned, deterministic; numbers
are illustrative, not real). --live runs the snippet unchanged.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import subprocess
import sys
import textwrap

ROOT = pathlib.Path(__file__).resolve().parents[1]
SNIPPETS = ROOT / "code-snippets"
RUNS = SNIPPETS / "runs"

# snippets that cannot run under --mock (extra deps / admin key / network)
LIVE_ONLY = {
    "blocking_hook": "needs `claude-agent-sdk` — run with --live",
    "mcp_server": "JSON-RPC over stdin; captured separately",
    "usage_cost_api": "needs an `sk-ant-admin-…` key + network — run with --live",
}

MOCK_SHIM = (
    "import sys\n"
    f"sys.path.insert(0, {str(SNIPPETS)!r})\n"
    "import _mockanthropic; _mockanthropic.install()\n"
)


def run_snippet(name: str, live: bool) -> str:
    src = SNIPPETS / f"{name}.py"
    if not src.exists():
        return f"(no such snippet: {name}.py)"
    env = dict(os.environ)
    if not live:
        if name in LIVE_ONLY:
            return f"[not run under --mock] {LIVE_ONLY[name]}"
        # prepend the mock shim, run the combined program
        prog = MOCK_SHIM + "\n\n" + src.read_text(encoding="utf-8")
        cmd = [sys.executable, "-c", prog]
        env["ANTHROPIC_API_KEY"] = env.get("ANTHROPIC_API_KEY", "sk-ant-mock")
    else:
        cmd = [sys.executable, str(src)]
    try:
        p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return "(timed out after 120s)"
    out = (p.stdout or "") + (p.stderr or "")
    out = out.strip() or "(no output)"
    # trim absurdly long traces
    lines = out.splitlines()
    if len(lines) > 60:
        out = "\n".join(lines[:58] + ["…", f"({len(lines) - 58} more lines)"])
    return out


def splice(md_path: pathlib.Path, code: str, output: str, mock: bool) -> bool:
    if not md_path.exists():
        return False
    txt = md_path.read_text(encoding="utf-8")
    tag = " · mock run — numbers illustrative" if mock else " · live run"

    code_block = ("<!-- CODE:START -->\n```python\n" + code.rstrip() + "\n```\n<!-- CODE:END -->")
    out_block = ("<!-- OUTPUT:START -->\n_captured" + tag + "_\n\n```text\n"
                 + output.rstrip() + "\n```\n<!-- OUTPUT:END -->")
    txt2 = re.sub(r"<!-- CODE:START -->.*?<!-- CODE:END -->", lambda _m: code_block, txt, count=1, flags=re.S)
    txt2 = re.sub(r"<!-- OUTPUT:START -->.*?<!-- OUTPUT:END -->", lambda _m: out_block, txt2, count=1, flags=re.S)
    if txt2 != txt:
        md_path.write_text(txt2, encoding="utf-8")
        return True
    return False


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*", help="snippet base names; default: all with a runs/ page")
    ap.add_argument("--live", action="store_true", help="run for real (API key + spend)")
    args = ap.parse_args(argv)

    pages = sorted(RUNS.glob("*.md"))
    names = args.names or [p.stem for p in pages]
    for name in names:
        md = RUNS / f"{name}.md"
        if not md.exists():
            print(f"skip {name}: no runs/{name}.md"); continue
        code = (SNIPPETS / f"{name}.py").read_text(encoding="utf-8") if (SNIPPETS / f"{name}.py").exists() else "(source missing)"
        out = run_snippet(name, args.live)
        changed = splice(md, code, out, mock=not args.live)
        print(f"{'updated' if changed else 'no-change'}  runs/{name}.md   ({len(out.splitlines())} output lines)")


if __name__ == "__main__":
    main(sys.argv[1:])
