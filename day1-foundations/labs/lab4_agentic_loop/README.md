# Lab 4 · The agentic loop, by hand

**Domain:** 4 — building agents (the primitive loop)
**Time:** 45 min
**You will practise:** a tool definition (JSON schema), `stop_reason == "tool_use"`,
appending `response.content` as the assistant turn, replying with a `tool_result` **block**,
and the `while` loop that ties it together.

> This is the same pattern as `ep01/agent.py` in the parent repo. **Open `ep01/agent.py`
> side by side and read along** — then build this one yourself without copying it. Day 3
> replaces this hand-rolled loop with the Claude Agent SDK; today you build it so you know
> what the SDK is doing for you.

---

## Goal

A CLI agent that answers a question about a small code folder (`mini_repo/`). It can't see
the files directly — it must call a `read_project_file` tool. Your loop runs the tool and
feeds results back until Claude gives a final answer.

```
cd day1-foundations
python labs/lab4_agentic_loop/starter/agent.py "Is there a bug in mini_repo? Cite the file and line."
```

---

## The two rules of the loop (put this on the board)

1. After every API response, append **`{"role": "assistant", "content": response.content}`**
   to `messages` — the *whole* content list, blocks and all.
2. If `stop_reason == "tool_use"`, run each `tool_use` block, then append **one** user
   message whose `content` is a list of `tool_result` blocks — one per `tool_use`, each
   carrying the matching `tool_use_id`.

Then loop. Stop when `stop_reason == "end_turn"` (or handle `max_tokens` / `refusal`).

---

## Steps

1. Open `starter/agent.py`. Study the `TOOLS` schema that's already there.
2. Implement `read_project_file(path)` — read from `mini_repo/`, reject anything outside it.
3. Implement `run_agent(question)`:
   - seed `messages` with the user question,
   - `while True:` call `client.messages.create(model=..., max_tokens=1024, tools=TOOLS,
     messages=messages)`,
   - append the assistant turn (rule 1),
   - branch on `stop_reason`:
     - `"tool_use"` → build `tool_result` blocks, append them as one user message, `continue`
     - `"end_turn"` → return the joined text
     - `"max_tokens"` / `"refusal"` / anything else → return a clear marker string
4. Run it. It should read `mini_repo/discount.py`, find the bug, and cite it.

---

## Expected output

Shape (exact wording varies):

```
[tool] read_project_file(path='discount.py')
[tool] read_project_file(path='cart.py')

Yes — mini_repo/discount.py line 7: `if percent > 1:` should be `>= 1` ... the 100%
discount case is rejected. cart.py looks fine.

(3 turns, stop_reason=end_turn)
```

---

## Checkpoints

- [ ] The assistant turn appended is `response.content` (the list), **not** a stringified
      version of it.
- [ ] Each `tool_result` block has the **correct `tool_use_id`** from its `tool_use` block.
- [ ] All `tool_result` blocks for one assistant turn go in **one** user message, not several.
- [ ] `read_project_file` refuses `../` / absolute paths (path-traversal guard).
- [ ] They handle a non-`end_turn` stop reason instead of looping forever.

## Common mistakes

| Symptom | Cause |
|---|---|
| `400 messages: roles must alternate` / tool_result errors | forgot to append the assistant turn before the tool_result user turn |
| Infinite loop | not returning on `end_turn`, or `continue` missing after tool results |
| `KeyError: 'tool_use_id'` | built the result block by hand with the wrong key name |
| Claude never calls the tool | `tools=TOOLS` not passed, or the tool description is too vague |

## Going further

- Add a second tool `list_project_files()` and see Claude use it first.
- Print `response.usage` each turn and watch input tokens grow as history accumulates.
- Add a hard turn cap (e.g. 8) and return gracefully if it's hit.
