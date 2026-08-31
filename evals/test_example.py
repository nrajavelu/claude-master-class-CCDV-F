"""pytest wrapper: one test per golden case. `pytest evals/test_example.py -q`"""
import pytest
from evals.harness import load_cases
from evals.checks import apply
from evals.golden_set_example import answer

CASES = load_cases("evals/golden_set.example.jsonl")


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_golden(case):
    out = answer(case["input"])
    fails = [f"{c['type']}: {d}" for c in case["checks"] for ok, d in [apply(c, out)] if not ok]
    assert not fails, "; ".join(fails)
