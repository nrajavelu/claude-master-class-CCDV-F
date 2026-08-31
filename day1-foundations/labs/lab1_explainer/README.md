# Lab 1 · Code explainer (non-streaming)

**Domain:** 1 — Claude & the API fundamentals
**Time:** 35 min
**You will practise:** `client.messages.create`, `system` prompt, the `messages` list,
reading `response.content` blocks, `response.usage`, `response.stop_reason`.

---

## Goal

A command-line tool that reads a source file and prints a plain-English explanation of what
it does, followed by the token usage of the call.

```
python labs/lab1_explainer/starter/explainer.py labs/lab1_explainer/sample.py
```

*(run from the `day1-foundations/` folder, venv active)*

---

## Steps

1. Open `starter/explainer.py`. Fill in each `# TODO`.
2. You need to:
   - build a **`system`** string that tells Claude its job (explain code for a teammate),
   - put the file's text into a **user message**,
   - call **`client.messages.create`** with a model, `max_tokens`, `system`, `messages`,
   - pull the **text** out of `response.content` (it's a *list of blocks* — filter for
     `block.type == "text"`),
   - print the explanation, then `response.usage` and `response.stop_reason`.
3. Run it against `sample.py`. Then try it on any file in the parent repo, e.g.
   `../ep01/agent.py`.

---

## Expected output

Shape (wording from Claude will vary):

```
=== Explanation of labs/lab1_explainer/sample.py ===
This script defines two helpers for working with lists of numbers. `average`
returns the mean and treats an empty list as 0.0; `find_extreme` returns the
smallest and largest values as a tuple, or None if the list is empty. ...

--- call stats ---
model:       claude-haiku-4-5
stop_reason: end_turn
usage:       input_tokens=181  output_tokens=96
```

---

## Checkpoints (trainer circulates)

- [ ] They used `system=` for the instruction, **not** a big user message. (Teaching point:
      the system prompt is the durable instruction channel.)
- [ ] They handled `response.content` as a **list**, not `response.content[0].text` blindly.
- [ ] They printed `usage` — they should *see* tokens, because Day 1 is also about cost.

## Common mistakes

| Symptom | Cause |
|---|---|
| `AttributeError: 'TextBlock' object has no attribute 'get'` | treating a response block like a dict |
| Empty explanation | filtered for the wrong `block.type`, or `max_tokens` too small |
| `FileNotFoundError` | running from the wrong folder — `cd day1-foundations` first |

## Going further (fast finishers)

- Add a `--style short|detailed` flag that changes the system prompt.
- Ask for the explanation as 3 bullet points and see how the system prompt controls format.
- Print an estimated cost using the Haiku price ($1 / $5 per million in/out).
