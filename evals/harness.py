"""
harness.py — run a golden set against any string->string target.

    python -m evals.harness --cases <file.jsonl> --target <module>:<callable>

`--target evals.golden_set_example:answer` imports `answer` from that module and calls it
with each case's `input`. Exit code 0 = all green.

Importable:
    from evals.harness import run
    passed, failed, report = run("path/to/golden_set.jsonl", my_run_fn)
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

from .checks import apply


def load_cases(path: str) -> list[dict]:
    out = []
    for i, line in enumerate(Path(path).read_text().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise SystemExit(f"{path}:{i}: bad JSON — {e}")
    return out


def run(cases_path: str, run_fn) -> tuple[int, int, str]:
    cases = load_cases(cases_path)
    lines, passed, failed = [], 0, 0
    for c in cases:
        cid = c.get("id", "?")
        try:
            output = run_fn(c["input"])
        except Exception as e:  # a target that raised is a failed case
            failed += 1
            lines.append(f"  FAIL {cid}: target raised {e.__class__.__name__}: {e}")
            continue
        fails = [(chk, d) for chk in c.get("checks", []) for ok, d in [apply(chk, output)] if not ok]
        if fails:
            failed += 1
            lines.append(f"  FAIL {cid}")
            for chk, d in fails:
                lines.append(f"       - {chk.get('type')}: {d}")
        else:
            passed += 1
            lines.append(f"  ok   {cid}")
    total = passed + failed
    report = "\n".join(lines) + f"\n\n{passed}/{total} passed" + (f"  ({failed} FAILED)" if failed else "")
    return passed, failed, report


def _resolve(target: str):
    mod_name, _, fn_name = target.partition(":")
    if not fn_name:
        raise SystemExit("--target must be <module>:<callable>")
    return getattr(importlib.import_module(mod_name), fn_name)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", required=True)
    ap.add_argument("--target", required=True, help="<module>:<callable>")
    a = ap.parse_args()
    _, failed, report = run(a.cases, _resolve(a.target))
    print(report)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
