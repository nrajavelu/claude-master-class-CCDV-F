# Orchestrator-workers

> Worked example · **Day 3** · exam domain **D1** · source `code-snippets/orchestrator_workers.py`
> Run it yourself: `python code-snippets/orchestrator_workers.py`

## Scenario

A lead LLM breaks a task into 2–3 approaches *at runtime*, then worker calls produce each one.

**Input / dataset.** A single task: 'write a product description', decomposed by the model.

## The code

<!-- CODE:START -->
```python
"""
orchestrator_workers.py — a lead LLM decomposes a task, workers do the pieces.

Adapted from the Anthropic Claude Cookbooks (MIT):
  patterns/agents/orchestrator_workers.ipynb · https://github.com/anthropics/claude-cookbooks

Exam angles (D1 · Agent Patterns):
  * ORCHESTRATOR-WORKERS != parallelisation. In parallelisation you already know the
    subtasks; here the LEAD LLM invents them at runtime, then delegates.
  * still a workflow shape — your code runs the loop, not the model.
  * use when the decomposition depends on the input (e.g. "write this N ways").

    cd aizentify-cdf-bootcamp && python code-snippets/orchestrator_workers.py
"""
import re

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"  # pinned for classroom cost


def call(prompt: str) -> str:
    r = client.messages.create(model=MODEL, max_tokens=1200,
                               messages=[{"role": "user", "content": prompt}])
    return "".join(b.text for b in r.content if b.type == "text")


ORCH = """Break this task into 2-3 distinct approaches. Task: {task}

Reply exactly as:
<tasks>
  <task><type>SHORT-LABEL</type><desc>what this version should do</desc></task>
  ...
</tasks>"""

WORKER = "Task: {task}\nApproach: {type}\nGuidelines: {desc}\nWrite it. <=120 words."


def parse(xml: str) -> list[dict]:
    return [{"type": t.strip(), "desc": d.strip()}
            for t, d in re.findall(r"<type>(.*?)</type>\s*<desc>(.*?)</desc>", xml, re.DOTALL)]


def run(task: str) -> list[tuple[str, str]]:
    plan = call(ORCH.format(task=task))
    subtasks = parse(plan) or [{"type": "default", "desc": task}]
    print(f"-- orchestrator planned {len(subtasks)} workers --")
    out = []
    for st in subtasks:
        res = call(WORKER.format(task=task, **st))
        print(f"\n== {st['type']} ==\n{res}")
        out.append((st["type"], res))
    return out


if __name__ == "__main__":
    run("Write a product description for a reusable water bottle.")
```
<!-- CODE:END -->

## Output

<!-- OUTPUT:START -->
_captured · mock run — numbers illustrative_

```text
-- orchestrator planned 1 workers --

== default ==
[mock reply] The support desk should acknowledge the issue, state the next step, and give a timeline.
```
<!-- OUTPUT:END -->

## Read the output

- Not parallelisation — you don't know the subtasks up front; the lead LLM decides them.
- Still a workflow: your code runs the loop over whatever the orchestrator returned.
- Use when the decomposition depends on the input.

## Exam hook

'Orchestrator-workers vs parallelisation' SBA; pattern-recognition scenarios.

## Your turn

Change the task to something with an obvious single approach — see the orchestrator still force 2–3.
