# The eval loop: code-graded vs judge

> Worked example · **Day 4** · exam domain **D4** · source `code-snippets/cookbook_building_evals.py`
> Run it yourself: `python code-snippets/cookbook_building_evals.py`

## Scenario

A tiny golden set ('how many legs does this animal have'), run through the task prompt, then graded two ways: pull-the-integer (code) and an LLM judge.

**Input / dataset.** Three golden cases including a tricky one (5 legs).

## The code

<!-- CODE:START -->
```python
"""
cookbook_building_evals.py — the eval loop: task prompt -> grade -> score.

Adapted from the Anthropic Claude Cookbooks (MIT):
  misc/building_evals.ipynb · https://github.com/anthropics/claude-cookbooks

Exam angles (D4 · Eval, Testing & Debugging):
  * grading method is a decision tree:
      one exact value        -> code / exact match   (cheap, brittle)
      structured output      -> code-graded check    (format, not quality)
      open-ended quality     -> LLM-as-judge         (calibrate vs humans first)
  * judge technique: ask for reasoning BEFORE the score, and use a single yes/no
    criterion where you can — a 1-10 scale drifts to ~6.
  * a golden set runs on EVERY prompt or model change; assert on structure + key
    content, not exact wording.

    cd aizentify-cdf-bootcamp && python code-snippets/cookbook_building_evals.py
"""
import re

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"  # pinned for classroom cost

GOLDEN = [
    {"statement": "The animal is a human.", "legs": "2"},
    {"statement": "The animal is a snake.", "legs": "0"},
    {"statement": "A fox lost a leg, then grew it back plus one extra.", "legs": "5"},
]


def task_prompt(statement: str) -> str:
    return (f"How many legs does this animal have? Reply with just the integer.\n"
            f"<animal_statement>{statement}</animal_statement>")


def run_task(statement: str) -> str:
    r = client.messages.create(model=MODEL, max_tokens=16,
                               messages=[{"role": "user", "content": task_prompt(statement)}])
    return "".join(b.text for b in r.content if b.type == "text").strip()


def grade_exact(output: str, golden: str) -> bool:
    """Code-graded: pull the first integer, compare."""
    m = re.search(r"-?\d+", output)
    return bool(m) and m.group() == golden


def grade_judge(question: str, output: str, golden: str) -> bool:
    """LLM-as-judge: reasoning first, then a yes/no. Use for open-ended tasks."""
    p = (f"Question: {question}\nExpected: {golden}\nModel answer: {output}\n\n"
         f"First give one sentence of reasoning, then on a new line reply exactly "
         f"CORRECT or INCORRECT.")
    r = client.messages.create(model=MODEL, max_tokens=120,
                               messages=[{"role": "user", "content": p}])
    text = "".join(b.text for b in r.content if b.type == "text")
    return "CORRECT" in text.split()[-3:]


if __name__ == "__main__":
    passed = 0
    for case in GOLDEN:
        out = run_task(case["statement"])
        ok = grade_exact(out, case["legs"])
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {case['statement'][:48]:48}  got {out!r:8} want {case['legs']}")
    print(f"\ncode-graded: {passed}/{len(GOLDEN)}")
    # For an open-ended task you'd swap grade_exact -> grade_judge on the same loop.
```
<!-- CODE:END -->

## Output

<!-- OUTPUT:START -->
_captured · mock run — numbers illustrative_

```text
[FAIL] The animal is a human.                            got '4'      want 2
[FAIL] The animal is a snake.                            got '4'      want 0
[FAIL] A fox lost a leg, then grew it back plus one ext  got '4'      want 5

code-graded: 0/3
```
<!-- OUTPUT:END -->

## Read the output

- Grading is a decision tree: one exact value → code match; structured → code-graded check; open-ended quality → LLM judge.
- Judge technique: ask for reasoning **before** the verdict; use a single yes/no criterion.
- A golden set runs on **every** prompt or model change; assert structure + key content, not exact wording.

## Exam hook

JDG 'an LLM-as-judge check is best written as…'; 'a regression test should…'.

## Your turn

Swap `grade_exact` for `grade_judge` on the same loop and compare pass counts.
