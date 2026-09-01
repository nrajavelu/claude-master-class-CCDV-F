# Day 1 — End-of-day quiz

12 questions, ~10 minutes, self-marked. Score out of 12; **≥ 9/12** to feel comfortable
moving to Day 2. Record your score per domain on the trainer's roster.

CCDV-F domains touched today: **D2** Applications & Integration (Claude API Mechanics) ·
**D5** Model Selection & Optimisation (LLM / Technical Fundamentals) · **D6** Prompt &
Context Engineering · **D1** Agents & Workflows (the loop) · **D4** Eval, Testing &
Debugging.

---

### Q1 (D2)
Which single field on the response tells you *why* generation stopped?

### Q2 (D2)
True/False: `response.content` is always a string you can print directly.

### Q3 (D2 / D5)
You set `max_tokens=50` and the answer needs 300 tokens. What is `stop_reason`, and what are
your two reasonable fixes?

### Q4 (D6)
Where does the *durable instruction* ("you are a code reviewer, reply in 3 bullets") belong —
the `system` field or a `user` message? Why?

### Q5 (D6)
Name three prompt-engineering techniques from today that improve output *format-following*.

### Q6 (D6 / D5)
A colleague's code sets `thinking={"type": "enabled", "budget_tokens": 4000}` on
`claude-sonnet-5` and gets a 400. Why, and what's the current way to do this?

### Q7 (D2)
Give two concrete reasons to stream a response instead of using a plain `messages.create`.

### Q8 (D2)
After a streaming call, how do you get the final `usage` and `stop_reason`?

### Q9 (D4)
Sort these by "retry or not": `BadRequestError` (400), `RateLimitError` (429),
`AuthenticationError` (401), `APIStatusError` (529), `APIConnectionError`.

### Q10 (D4)
Is `stop_reason: "refusal"` something you catch in an `except` block? Explain.

### Q11 (D1)
In the hand-rolled agent loop, after every API response you must append one specific thing to
`messages` before doing anything else. What, exactly?

### Q12 (D1)
When `stop_reason == "tool_use"` and there were 2 `tool_use` blocks, how many user messages
do you append, and what's in them?

---
---

## Answer key

**Q1** — `response.stop_reason`. *(D2 · API Mechanics)*

**Q2** — **False.** It's a *list of typed blocks*. Filter on `block.type` (e.g. `== "text"`)
and read `.text`. *(D2)*

**Q3** — `stop_reason == "max_tokens"`. Fixes: raise `max_tokens`, or stream (no practical
ceiling / no timeout), or ask for a shorter answer. *(D2 / D5)*

**Q4** — The `system` field. It's the persistent contract for every turn; user messages carry
the changing task and data. Repeating instructions each turn wastes tokens and drifts.
*(D6 · Prompt Engineering)*

**Q5** — Any three of: be explicit about format/length/exclusions; structure inputs with XML
tags; provide a fill-in skeleton; give one or two few-shot `input → output` examples.
*(D6 · Output Handling)*

**Q6** — `budget_tokens` is deprecated and **rejected (400)** on current models. Use
`thinking={"type": "adaptive"}` and control depth/spend with `output_config={"effort": ...}`.
*(D6 / D5 — classic stale-API exam distractor)*

**Q7** — Any two: avoids the HTTP request timeout on long outputs / high `max_tokens`; live
responsive UI; can start processing early. *(D2 · API Mechanics)*

**Q8** — `stream.get_final_message()` after the `with` block — returns the full `Message`
(usage, stop_reason, all blocks). Don't hand-assemble from events. *(D2)*

**Q9** — **Retry:** `RateLimitError` (429), `APIStatusError` (**529 `overloaded_error`** /
any ≥ 500), `APIConnectionError`. **Don't retry:** `BadRequestError` (400),
`AuthenticationError` (401), `PermissionDeniedError` (403), `request_too_large` (413).
Note: **529**, not 503, is this API's overloaded code — 429 is *your* traffic, 529 is
*Anthropic-side* load.
*(D4 · Debugging & Error Handling)*

**Q10** — **No.** HTTP 200 with `stop_reason == "refusal"` (+ a `stop_details` category). It
never raises. Check `stop_reason` before reading `content`. *(D4)*

**Q11** — `{"role": "assistant", "content": response.content}` — the **whole content list**,
unmodified. *(D1 · Agent Construction)*

**Q12** — **One** user message. Its `content` is a **list of 2 `tool_result` blocks**, one
per `tool_use`, each with the matching `tool_use_id`. Splitting across messages trains the
model to stop parallelising. *(D1 · Agent Construction)*

---

### Scoring → next step

| Score | Guidance |
|---|---|
| 11–12 | Solid. Skim tonight's optional reading only. |
| 8–10 | Fine. Re-read the module(s) behind any miss. |
| ≤ 7 | Flag to the trainer. Tonight: `ep01/agent.py` + `question-bank/domain-2-applications-integration.md` (Claude API Mechanics) + the Day 1 deck recap slides. |
