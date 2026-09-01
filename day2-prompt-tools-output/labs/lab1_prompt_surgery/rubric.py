"""Heuristic rubric for lab1_prompt_surgery. Offline, deliberately crude — it rewards the
*structural* properties a good summary of a bug report should have. Five checks, 1 point
each. Not a substitute for an LLM judge (Day 4), but enough to see a prompt improve.
"""
import re

REQUIRED_TERMS = ("health", "wait", "race", "readiness", "poll", "retry", "startup")


def score(summary: str) -> tuple[int, list[str]]:
    s = summary.strip()
    low = s.lower()
    checks = {
        "<= 4 bullet/line items": _bullets(s) <= 4 and _bullets(s) >= 1,
        "names the root cause (missing wait / race / health-check)":
            any(t in low for t in ("no wait", "without wait", "race", "health check",
                                   "health-check", "readiness", "before it is ready",
                                   "not ready")),
        "mentions CI vs local timing difference":
            ("ci" in low or "pipeline" in low) and ("local" in low),
        "no invented specifics (ports, tools, numbers not in the input)":
            not re.search(r"\b(kubernetes|docker|postgres|port \d{2,5}|localhost:\d+)\b", low),
        "ends actionable (suggests a fix direction)":
            any(t in low for t in ("add a", "wait for", "poll", "health", "readiness",
                                   "retry", "should")),
    }
    got = [name for name, ok in checks.items() if ok]
    missed = [name for name, ok in checks.items() if not ok]
    return len(got), missed


def _bullets(s: str) -> int:
    lines = [ln for ln in s.splitlines() if ln.strip()]
    b = [ln for ln in lines if re.match(r"\s*[-*•\d]", ln)]
    return len(b) if b else len(lines)


if __name__ == "__main__":
    import sys
    text = sys.stdin.read()
    n, missed = score(text)
    print(f"score: {n}/5")
    for m in missed:
        print("  missed:", m)
