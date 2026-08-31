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
