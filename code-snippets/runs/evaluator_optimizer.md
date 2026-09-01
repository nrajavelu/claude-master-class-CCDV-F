# Generate → critique → loop

> Worked example · **Day 3** · exam domain **D1/D4** · source `code-snippets/evaluator_optimizer.py`
> Run it yourself: `python code-snippets/evaluator_optimizer.py`

## Scenario

One model generates a solution; a second evaluates it against explicit criteria; loop until PASS or a max-rounds cap.

**Input / dataset.** A coding task with a clear bar (all operations O(1)).

## The code

<!-- CODE:START -->
```python
"""
evaluator_optimizer.py — one model generates, another critiques, loop until it passes.

Adapted from the Anthropic Claude Cookbooks (MIT):
  patterns/agents/evaluator_optimizer.ipynb · https://github.com/anthropics/claude-cookbooks

Exam angles (D1 · Agent Patterns · D4 evals):
  * fits when there is a CLEAR quality bar and iteration helps (code, translation,
    structured drafts).
  * the evaluator only judges — it never tries to solve the task.
  * bound the loop: a max-rounds cap is the guardrail (Rule 1 — mechanism, not vibes).

    cd aizentify-cdf-bootcamp && python code-snippets/evaluator_optimizer.py
"""
import re

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"  # pinned for classroom cost

GEN = """Complete the task. If <feedback> is present, revise to address it.
{feedback}
Task: {task}

Reply as:
<thoughts>how you're approaching it / responding to feedback</thoughts>
<response>your answer</response>"""

EVAL = """Evaluate the response against the task on correctness, complexity, and style.
Judge only — do not solve it. Reply as:
<verdict>PASS or NEEDS_WORK</verdict>
<feedback>what to fix, or "none"</feedback>

Task: {task}
Response: {response}"""


def call(p: str) -> str:
    r = client.messages.create(model=MODEL, max_tokens=1400,
                               messages=[{"role": "user", "content": p}])
    return "".join(b.text for b in r.content if b.type == "text")


def xml(t, tag):
    m = re.search(rf"<{tag}>(.*?)</{tag}>", t, re.DOTALL)
    return m.group(1).strip() if m else ""


def run(task: str, max_rounds: int = 3) -> str:
    feedback, answer = "", ""
    for i in range(1, max_rounds + 1):
        fb = f"<feedback>{feedback}</feedback>" if feedback else ""
        answer = xml(call(GEN.format(task=task, feedback=fb)), "response")
        verdict = call(EVAL.format(task=task, response=answer))
        print(f"-- round {i}: {xml(verdict, 'verdict')} --")
        if xml(verdict, "verdict") == "PASS":
            return answer
        feedback = xml(verdict, "feedback")
    print("-- hit max_rounds; returning best effort --")
    return answer


if __name__ == "__main__":
    print(run("Implement a Stack with push, pop and get_min, all O(1). Python."))
```
<!-- CODE:END -->

## Output

<!-- OUTPUT:START -->
_captured · mock run — numbers illustrative_

```text
-- round 1: PASS --
class MinStack: ...
```
<!-- OUTPUT:END -->

## Read the output

- Fits when there's a **clear quality bar** and iteration helps.
- The evaluator only judges — it never tries to solve the task.
- Bound the loop with `max_rounds` — the guardrail is a mechanism, not a vibe.

## Exam hook

Pattern id; 'the evaluator should…' judgement items; ties to D4 evals.

## Your turn

Lower `max_rounds` to 1 and give it a hard task — see it return a NEEDS_WORK draft.
