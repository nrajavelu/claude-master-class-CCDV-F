# Reasoning patterns — Chain-of-Thought, ReAct, and Claude's thinking

> **For candidates and trainers.** Read this after Day 1 Module 1. The CCDV-F exam leans on
> knowing **what each pattern is, when it helps, and how Claude implements it** — and on
> spotting the stale-API and "always helps" distractors.

---

## 1. The one-paragraph version

- **Chain-of-Thought (CoT)** = the model writes its **reasoning steps before the answer**,
  inside a **single response**. It trades output tokens for accuracy on problems that need
  working-out.
- **ReAct** (Reason + Act) = CoT **interleaved with tool calls across a loop**:
  *Thought → Action → Observation → Thought → … → Answer*. This **is** the agentic loop.
- **Claude's extended / adaptive thinking** = CoT **built into the model**. You turn it on
  with `thinking={"type": "adaptive"}`; the model decides how much to think and emits a
  `thinking` block before its answer. Combine it with ReAct → the model can think *between*
  tool calls ("interleaved thinking").

```
CoT     :  [ Reason … Reason ] → Answer                       (one turn)
ReAct   :  Reason → Act → Observe → Reason → Act → Observe → Answer   (a loop)
thinking:  Claude doing CoT natively, in a `thinking` block, at either scale
```

---

## 2. Chain-of-Thought (CoT)

### What it is
Prompting the model to **show its working**. "Reason first, answer last." The reasoning
tokens give the model room to decompose the problem instead of jumping to a guess.

### How to elicit it with Claude
| Technique | How | Note |
|---|---|---|
| **Zero-shot CoT** | add *"Think step by step, then give the answer."* to the prompt | cheapest; works for light reasoning |
| **Structured CoT** | ask for named steps: *"First list the constraints. Then check each option against them. Then answer."* | most reliable for exam-style "which option" logic |
| **Few-shot CoT** | show 1–2 worked `problem → reasoning → answer` examples | best for a specific reasoning *format* you want repeated |
| **Extended / adaptive thinking** | `thinking={"type": "adaptive"}` on a current model | **Claude's native CoT** — the model decides depth; returns a `thinking` block. Control spend with `output_config={"effort": ...}` |
| **Self-consistency** | sample the same CoT prompt N times, take the majority answer | expensive; only for high-stakes single answers |

### Practical example — structured CoT

```python
resp = client.messages.create(
    model="claude-haiku-4-5", max_tokens=400,
    system=(
        "You answer multiple-choice questions. Reason in three labelled steps, "
        "then end with exactly: 'Answer: <letter>'.\n"
        "Step 1 — the constraint the question names.\n"
        "Step 2 — eliminate options that don't serve that constraint.\n"
        "Step 3 — pick the mechanism built for it."
    ),
    messages=[{"role": "user", "content": QUESTION}],
)
```

### Practical example — Claude's native CoT (adaptive thinking)

```python
resp = client.messages.create(
    model="claude-opus-5", max_tokens=2000,
    thinking={"type": "adaptive", "display": "summarized"},   # <- built-in CoT
    output_config={"effort": "high"},
    messages=[{"role": "user", "content": HARD_PROBLEM}],
)
for b in resp.content:
    if b.type == "thinking": print("REASONING:", b.thinking)
    if b.type == "text":     print("ANSWER:", b.text)
```

### When CoT helps — and when it doesn't
| Helps | Doesn't help (skip it) |
|---|---|
| multi-step maths / logic | classification into a fixed set |
| multi-constraint "which option" | extraction of a named field |
| ambiguous or under-specified tasks | high-volume, latency-sensitive routes |
| planning before a long task | anything already trivial for the model |

> **Exam distractors:** "CoT always improves accuracy" — **false** (it adds latency/cost and
> can hurt on simple tasks). "Set `thinking={'type':'enabled','budget_tokens': N}`" — **stale**
> (removed / rejected on current models; use `adaptive` + `effort`).

---

## 3. ReAct (Reason + Act)

### What it is
CoT that can **take actions** and **see their results** before continuing. Each iteration:

```
Thought      — what do I need? what will I do next?
Action       — call a tool
Observation  — the tool's result comes back
Thought      — given that, what now?
...          — repeat
Answer       — enough information: respond
```

This is exactly the **agentic loop** from Day 1 Lab 4. The Messages API gives you the pieces:

| ReAct step | Messages API |
|---|---|
| Thought | a `thinking` block, or leading `text` in the assistant turn |
| Action | a `tool_use` block · `stop_reason == "tool_use"` |
| Observation | you run the tool, append a `tool_result` block in a user message |
| loop control | `stop_reason` — keep looping until `end_turn` |

### Practical example — a ReAct trace

```
Thought:      I don't know what discount.py contains — I must read it before judging.
Action:       read_project_file(path="discount.py")
Observation:  def apply_discount(price, percent):
                  if percent < 0 or percent > 1: raise ValueError(...)
                  if percent > 1: return 0.0          # <- line 7
                  return round(price * (1 - percent), 2)
Thought:      Line 7 is unreachable — line 5 already raised for percent > 1. Dead code.
Answer:       discount.py:7 — unreachable branch after the guard on line 5.
```

### Practical example — the loop that produces it

```python
messages = [{"role": "user", "content": question}]
while True:
    r = client.messages.create(model=M, max_tokens=1024, tools=TOOLS, messages=messages)
    messages.append({"role": "assistant", "content": r.content})     # Rule 1
    if r.stop_reason == "tool_use":                                  # Action taken
        results = []
        for b in r.content:
            if b.type == "tool_use":
                results.append({"type": "tool_result", "tool_use_id": b.id,
                                "content": run_tool(b.name, b.input)})   # Observation
        messages.append({"role": "user", "content": results})        # Rule 2
        continue                                                     # -> next Thought
    if r.stop_reason == "end_turn":
        return "".join(b.text for b in r.content if b.type == "text")
```

### Who runs the loop
| You use | Who writes the ReAct loop |
|---|---|
| raw Messages API (Day 1 Lab 4) | **you** — the `while` above |
| SDK Tool Runner | the SDK, over your tools |
| Claude Agent SDK | the SDK, with built-in tools |
| Managed Agents | Anthropic, on a hosted sandbox |

### Interleaved thinking
On current models you can leave `thinking` **on** during a ReAct loop → the model produces a
`thinking` block **between** tool calls, reasoning about each observation before its next
action. That's CoT *inside* ReAct.

> **Exam distractors:** "ReAct is a single API call" — **false** (it needs the loop / tool
> results fed back). "The model executes the tool" — **false** (your code / the sandbox runs
> it; the model only emits `tool_use`).

---

## 4. Other names you might meet

| Name | One line | Exam weight |
|---|---|---|
| **Zero-shot / few-shot CoT** | "think step by step" vs showing worked examples | know the terms |
| **Self-consistency** | sample many CoT paths, majority-vote the answer | rare |
| **Tree-of-Thought (ToT)** | branch and explore multiple reasoning paths, prune | rare — recognise the name |
| **Reflexion** | the agent critiques its own last attempt and retries | rare |
| **Plan-then-execute** | one planning turn, then a workflow executes the plan | common design choice |

The exam mostly tests **CoT vs ReAct**, **Claude's adaptive thinking** (and the stale
`budget_tokens`), and **who runs the loop**. The rest is vocabulary recognition.

---

## 5. Where this is taught in the bootcamp

| | Slide / lab | Doc |
|---|---|---|
| CoT intro + adaptive thinking | Day 1 · Module 2 ("Chain-of-Thought") + Module 5 | this file |
| ReAct loop + worked trace | Day 1 · Module 5 ("The loop is ReAct") + **Lab 4** | this file |
| Who runs the loop (4 ways) | Day 3 · Module 2 | `day3-.../README.md` |
| Interleaved thinking in agents | Day 3 · Module 3 | — |
| Practice | `portal/practice.html` (CoT/ReAct items) · `code-snippets/agent_loop_react.py` · `code-snippets/cot_structured.py` | `question-bank/domain-1-agents-workflows.md`, `domain-6-prompt-context-engineering.md` |

## 6. Trainer notes

- Draw the three timelines (CoT / ReAct / thinking) on the board once; refer back to it all week.
- On Day 1 Lab 4, have candidates **write the Thought/Action/Observation trace by hand** from
  their program's output before you show them the SDK equivalent on Day 3 — the point is that
  the SDK is *just this loop*.
- The highest-value exam sentence: **"ReAct is the agentic loop; CoT is the reasoning inside
  a turn; adaptive thinking is Claude doing CoT for you."**
