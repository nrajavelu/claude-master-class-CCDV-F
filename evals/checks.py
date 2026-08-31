"""
checks.py — the check functions for the golden-set harness.

Each check is {"type": ..., "value": ...}. apply(check, output) -> (ok: bool, detail: str).
"""
from __future__ import annotations

import json
import re

_client = None


def _judge_client():
    global _client
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic()
    return _client


def _structural(rule: str, output: str) -> tuple[bool, str]:
    lines = [ln for ln in output.splitlines() if ln.strip()]
    m = re.match(r"(len|cited)\s*(>=|<=|==|>|<)\s*(\d+)", rule.strip())
    if not m:
        return False, f"bad structural rule {rule!r}"
    metric, op, n = m.group(1), m.group(2), int(m.group(3))
    val = len(lines) if metric == "len" else len(re.findall(r"(?:doc:|\[\d+\]|\bA-\d+\b)", output))
    ok = {">=": val >= n, "<=": val <= n, "==": val == n, ">": val > n, "<": val < n}[op]
    return ok, f"{metric}={val} {op} {n}"


def apply(check: dict, output: str) -> tuple[bool, str]:
    t = check.get("type")
    v = check.get("value", "")
    low = output.lower()

    if t == "contains":
        return (str(v).lower() in low), f"contains {v!r}"
    if t == "not_contains":
        return (str(v).lower() not in low), f"not_contains {v!r}"
    if t == "regex":
        return (re.search(v, output) is not None), f"regex {v!r}"
    if t == "json_valid":
        try:
            obj = json.loads(output)
        except Exception as e:
            return False, f"not JSON: {e}"
        if v and (not isinstance(obj, dict) or v not in obj):
            return False, f"missing key {v!r}"
        return True, "json ok"
    if t == "structural":
        return _structural(v, output)
    if t == "llm_judge":
        r = _judge_client().messages.create(
            model="claude-haiku-4-5", max_tokens=8,
            system="Answer with exactly one word: yes or no.",
            messages=[{"role": "user",
                       "content": f"Criterion: {v}\n\n---\n{output}\n---\n\nDoes the text meet the criterion?"}],
        )
        ans = "".join(b.text for b in r.content if b.type == "text").strip().lower()
        return ans.startswith("y"), f"judge said {ans!r}"

    return False, f"unknown check type {t!r}"
