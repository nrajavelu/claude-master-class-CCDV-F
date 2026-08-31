"""
run_golden.py — run this assistant's golden set. Do it after ANY change to
system_prompt.txt, config.toml (model id / budget), or tools.py descriptions.

    cd aizentify-cdf-bootcamp
    python capstone-support-assistant/run_golden.py

Makes real API calls (~a few cents for 8 cases). That's the point.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # so `evals` imports
from evals.harness import run          # noqa: E402
from assistant import run as _run      # noqa: E402  (capstone-support-assistant/assistant.py)


def target(inp: str) -> str:
    if inp.startswith("--only-lookup "):
        return _run(inp[len("--only-lookup "):], only_lookup=True)
    return _run(inp)


if __name__ == "__main__":
    passed, failed, report = run(str(Path(__file__).parent / "golden_set.jsonl"), target)
    print(report)
    sys.exit(1 if failed else 0)
