# Day 2 — End-of-day quiz

10 questions, ~10 min, self-marked. **≥ 8/10** to move on comfortably. Record per-domain on
the roster. Domains: **D6** Prompt & Context · **D8** Tools & MCPs · **D2** structured output.

---

### Q1 (D6)
Where does the durable contract (role, rules, output shape) go — `system` or a `user`
message? Why?

### Q2 (D6)
Name the three prompt-engineering techniques that most improve *format-following*.

### Q3 (D2 / surfaces)
A prototype behaves well in the chat product but differently through the API. Best single
explanation?

### Q4 (D6)
True/False: you can send a message with `role: "system"` to strengthen an instruction.

### Q5 (D7)
Where does a fetched web page / a customer ticket belong in the request? And where must your
*own* instructions never go?

### Q6 (D8)
A tool is being called at the wrong time. What do you check first, and what's the *overbuild*
answer to avoid?

### Q7 (D8)
For one assistant turn with 3 `tool_use` blocks, how many user messages do you append and
what's in them?

### Q8 (D2)
Your `strict` tool keeps rejecting an "optional" field you left out of `required`. Fix?

### Q9 (D2)
True/False: an unsupported JSON-Schema feature in a `strict` tool is silently ignored.

### Q10 (D2)
What does `client.messages.parse()` do for you, and what's the status of *prefilling* on
current models?

---
---

## Answer key

**Q1** — The `system` field. It's the persistent, every-turn contract; user messages carry
the changing task + data. *(D6)*

**Q2** — Be explicit (format/length/exclusions); structure inputs with XML/delimiter tags;
few-shot (one or two `input → output` examples). *(D6)*

**Q3** — The chat product layers Anthropic's own system prompt under yours; it doesn't apply
to the API. (Not "different model", not "temperature".) *(D2 · surfaces)*

**Q4** — **False.** No message can have `role: "system"` on the API. Instructions go in the
top-level `system` field. *(D6 — right-word-wrong-place distractor)*

**Q5** — Untrusted / third-party content goes in a `tool_result` block. Your own instructions
**never** go in a `tool_result` — that channel is read with suspicion. Say it in your next
turn instead. *(D7)*

**Q6** — Check the **tool description** (what it does, *when* to use it, *when not* to,
parameter names). The overbuild answer to avoid: "add a routing model / fine-tune". *(D8)*

**Q7** — **One** user message; its `content` is a list of 3 `tool_result` blocks, each with
the matching `tool_use_id`. *(D8 / D1)*

**Q8** — Keep it in `required` and allow `null` as a type — `strict` has no "optional".
`additionalProperties` stays `false`. *(D2)*

**Q9** — **False.** It's **rejected**, not ignored. *(D2)*

**Q10** — `parse()` validates the response against your schema (returns a typed object or
raises). **Prefilling** is a classic cheap structured-output trick the *exam still
references*, but it is **rejected on the newest models** — use `output_config.format` there.
*(D2)*

---
### Scoring → next step
| Score | Guidance |
|---|---|
| 9–10 | Solid. |
| 7–8 | Re-read the module behind any miss. |
| ≤ 6 | Flag. Tonight: `ep03/tools.py` + `ep07/schemas.py` + `question-bank/domain-8-tools-mcps.md`, or Build-along Ep 03 & 07. |
