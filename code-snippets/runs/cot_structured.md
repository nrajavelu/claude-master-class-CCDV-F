# Chain-of-Thought, then a clean answer

> Worked example · **Day 1** · exam domain **D6** · source `code-snippets/cot_structured.py`
> Run it yourself: `python code-snippets/cot_structured.py`

## Scenario

A reasoning task where the model shows its work in a `<thinking>` block, then a separate final answer your code can use.

**Input / dataset.** A word problem with a deliberate trap.

## The code

<!-- CODE:START -->
```python
"""
cot_structured.py — Chain-of-Thought, two ways.

Exam angles (D6 · Prompt & Context Engineering):
  * CoT = reasoning steps BEFORE the answer, in ONE response
  * zero-shot ("think step by step") vs structured (name the steps) vs few-shot
  * Claude's adaptive thinking is CoT BUILT IN -> thinking={"type":"adaptive"}
  * distractors: "CoT always helps" (false); budget_tokens (stale/removed)

    cd aizentify-cdf-bootcamp && python code-snippets/cot_structured.py

See reasoning-patterns.md for the full CoT vs ReAct vs thinking picture.
"""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

QUESTION = (
    "10,000 documents must be processed overnight. Cost is the main concern and nobody "
    "needs the results until morning. Best approach? "
    "A) run them in parallel  B) the Batch API  C) switch to a smaller model  D) cap max_tokens"
)

# --- 1. Structured CoT via the prompt (works on any model) --------------------
print("=== structured CoT (prompt) ===")
r1 = client.messages.create(
    model="claude-haiku-4-5", max_tokens=400,
    system=(
        "Answer the multiple-choice question. Reason in three labelled steps, then end "
        "with exactly 'Answer: <letter>'.\n"
        "Step 1 - the constraint the question names.\n"
        "Step 2 - eliminate options that don't serve that constraint (generic knobs are distractors).\n"
        "Step 3 - the mechanism built for the constraint."
    ),
    messages=[{"role": "user", "content": QUESTION}],
)
print("".join(b.text for b in r1.content if b.type == "text"))

# --- 2. Claude's native CoT: adaptive thinking -------------------------------
# NOTE: budget_tokens is removed/rejected on current models. Use adaptive + effort.
print("\n=== adaptive thinking (native CoT) ===")
r2 = client.messages.create(
    model="claude-haiku-4-5", max_tokens=800,
    thinking={"type": "adaptive", "display": "summarized"},
    messages=[{"role": "user", "content": QUESTION + "\nExplain briefly, then 'Answer: <letter>'."}],
)
for b in r2.content:
    if b.type == "thinking":
        print("[thinking]", (b.thinking or "(omitted)")[:300])
    elif b.type == "text":
        print("[answer]  ", b.text)
```
<!-- CODE:END -->

## Output

<!-- OUTPUT:START -->
_captured · mock run — numbers illustrative_

```text
=== structured CoT (prompt) ===
[mock reply] The support desk should acknowledge the issue, state the next step, and give a timeline.

=== adaptive thinking (native CoT) ===
[thinking] Let me reason about this step by step. The key is to track where each amount actually goes rather than adding unrelated numbers…
[answer]   [mock reply] The support desk should acknowledge the issue, state the next step, and give a timeline.
```
<!-- OUTPUT:END -->

## Read the output

- CoT happens **inside one turn** — it is not the agentic loop (that's ReAct, across turns).
- Adaptive thinking on Claude 5 models is native CoT tuned by `effort`; here we prompt it explicitly.
- Strip the reasoning from what you show the user; keep it for logs/debugging.

## Exam hook

'Does CoT always help?' — no; it costs tokens/latency and can hurt on trivial tasks. CoT vs ReAct is a frequent confusion.

## Your turn

Ask the same question with `effort` low vs high (Day 5) and compare answer quality vs tokens.
