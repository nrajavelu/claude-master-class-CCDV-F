# Chaining · parallelisation · routing

> Worked example · **Day 3** · exam domain **D1** · source `code-snippets/workflow_patterns.py`
> Run it yourself: `python code-snippets/workflow_patterns.py`

## Scenario

The three 'your code owns the path' workflow patterns, back to back: a fixed transform chain, the same prompt over many inputs concurrently, and classify-then-specialise routing.

**Input / dataset.** A metrics paragraph (chain), three stakeholder groups (parallel), one billing complaint (routing).

## The code

<!-- CODE:START -->
```python
"""
workflow_patterns.py — the three "your code owns the path" workflow patterns, minimal.

Adapted from the Anthropic Claude Cookbooks (MIT):
  patterns/agents/basic_workflows.ipynb  ·  https://github.com/anthropics/claude-cookbooks

Exam angles (D1 · Agents & Workflows):
  * WORKFLOW = your code decides the sequence; AGENT = the model decides. This file is
    all workflow.
  * prompt chaining  — fixed steps, each stage's output feeds the next
  * parallelisation  — same prompt over many inputs, concurrently (speed) or N times (vote)
  * routing          — classify first, then a specialised prompt per class
  * "one mega-prompt doing five jobs" that mislabels edge cases -> the fix is ROUTING,
    not a bigger model / more few-shot.

    cd aizentify-cdf-bootcamp && python code-snippets/workflow_patterns.py
"""
from concurrent.futures import ThreadPoolExecutor
import re

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"  # pinned for classroom cost — Day 5 covers model selection


def call(prompt: str, system: str = "") -> str:
    r = client.messages.create(model=MODEL, max_tokens=1024, system=system,
                               messages=[{"role": "user", "content": prompt}])
    return "".join(b.text for b in r.content if b.type == "text")


def xml(text: str, tag: str) -> str:
    m = re.search(rf"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return m.group(1).strip() if m else ""


# ---- 1. prompt chaining --------------------------------------------------------
def chain(text: str, steps: list[str]) -> str:
    out = text
    for i, step in enumerate(steps, 1):
        out = call(f"{step}\n\nInput:\n{out}")
        print(f"-- step {i} --\n{out}\n")
    return out


# ---- 2. parallelisation ------------------------------------------------------
def parallel(prompt: str, inputs: list[str], workers: int = 3) -> list[str]:
    with ThreadPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(lambda x: call(f"{prompt}\n\nInput:\n{x}"), inputs))


# ---- 3. routing -------------------------------------------------------------
def route(text: str, routes: dict[str, str]) -> str:
    pick = call(
        f"Classify the input into exactly one of {list(routes)}. "
        f"Reply as <selection>name</selection>.\n\nInput: {text}"
    )
    name = xml(pick, "selection") or next(iter(routes))
    print(f"-- routed to: {name} --")
    return call(f"{routes[name]}\n\nInput: {text}")


if __name__ == "__main__":
    print("### chaining ###")
    chain(
        "Q3: satisfaction rose to 92 points. Revenue grew 45%. Churn fell to 5%.",
        ["Extract each 'value: metric' on its own line.",
         "Normalise every value to a percentage.",
         "Sort descending by value, keep 'value: metric'."],
    )
    print("### parallelisation ###")
    for r in parallel("One-sentence risk for this group:",
                      ["price-sensitive customers", "employees fearing layoffs", "growth investors"]):
        print(" -", r)
    print("\n### routing ###")
    print(route(
        "I was charged twice for my subscription this month.",
        {"billing": "You are billing support. Start with 'Billing:'. Be concrete.",
         "technical": "You are tech support. Start with 'Technical:'. Numbered steps.",
         "account": "You are account security. Start with 'Account:'. Verify identity first."},
    ))
```
<!-- CODE:END -->

## Output

<!-- OUTPUT:START -->
_captured · mock run — numbers illustrative_

```text
### chaining ###
-- step 1 --
| Metric | Value |
|:--|--:|
| Customer satisfaction | 92% |

-- step 2 --
[mock reply] The support desk should acknowledge the issue, state the next step, and give a timeline.

-- step 3 --
| Metric | Value |
|:--|--:|
| Customer satisfaction | 92% |

### parallelisation ###
 - [mock reply] The support desk should acknowledge the issue, state the next step, and give a timeline.
 - [mock reply] The support desk should acknowledge the issue, state the next step, and give a timeline.
 - [mock reply] The support desk should acknowledge the issue, state the next step, and give a timeline.

### routing ###
-- routed to: billing --
[mock reply] The support desk should acknowledge the issue, state the next step, and give a timeline.
```
<!-- OUTPUT:END -->

## Read the output

- **Workflow**, not agent — the sequence is in your code, the model never picks the path.
- Routing = classify first, then a specialised prompt per class — the fix for one mega-prompt mislabelling edge cases.
- Orchestrator-workers (next page) is different: there the *model* invents the subtasks.

## Exam hook

SCN 'five ticket categories, one prompt mislabels' → routing (not a bigger model / more few-shot).

## Your turn

Give `route()` a ticket that fits two categories — see which one the classifier picks and why.
