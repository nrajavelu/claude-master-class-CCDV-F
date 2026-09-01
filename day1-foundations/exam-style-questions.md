# Day 1 — Exam-style questions

18 items written in the style of the **Claude Certified Developer – Foundations (CCDV-F)**
exam. Work them at your table, argue to consensus, *then* read the answer block. The trainer
walks every distractor — that discussion is where exam skill is built.

Question styles: single best answer (SBA), multiple response (MR — "choose N"), scenario /
next-step, predict-the-output (OUT), spot-the-bug (BUG), judgement (JDG).

**Attack every item with the method from `../logistics/05-exam-method.md`:**

1. **Name the decision.** Every CCDV-F item is one of four: ① *what runs?* ② *how does it
   call Claude?* ③ *what does Claude see and say?* ④ *will it survive production?*
2. **Rule 1 — mechanism beats knob.** The stem names a constraint → the answer is the
   mechanism built for that constraint. A generic dial (temperature, model tier, max_tokens)
   is almost always a distractor.
3. **Rule 2 — mechanism beats guidance.** If the stem says *must / never / always / cannot*,
   every option that is only *advice* ("tell the model to…", "write it down", "ask users
   to…") is dead. Only something that *actually stops* the bad case survives.

Domain tags (CCDV-F): **D1** Agents & Workflows · **D2** Applications & Integration
(Claude API Mechanics) · **D4** Eval, Testing & Debugging · **D5** Model Selection &
Optimisation · **D6** Prompt & Context Engineering. Today's items sit mostly in **D2**,
with **D6**, **D4**, **D1** and a little **D5**.

---

## Questions

**1. (SBA · D2)** Every Claude capability below is invoked through the same API call
*except* one. Which is a **separate** endpoint?
A. Tool use  B. Vision (image input)  C. Extended thinking  D. Counting tokens for a prompt

**2. (SBA · D2)** `response.content[0]` on a normal text reply is:
A. a `str`
B. a dict `{"type": "text", "text": "..."}`
C. a typed block object with `.type` and `.text`
D. the raw JSON string of the whole response

**3. (MR · D2 — choose TWO)** Which are valid `stop_reason` values?
A. `end_turn`  B. `tool_call`  C. `max_tokens`  D. `content_filter`  E. `token_limit`

**4. (Scenario · D2)** Your call returns `stop_reason == "max_tokens"` and the answer is cut
off mid-sentence. Which is the **best** fix for a long report-generation feature?
A. Add a retry loop that calls the same request again
B. Switch to `client.messages.stream(...)` with a higher `max_tokens`
C. Lower `max_tokens` so it stops cleanly
D. Set `stop_sequences` to `["\n\n"]`

**5. (SBA · D6)** The most reliable place to put "always answer in exactly three bullets" is:
A. the last line of every user message
B. the `system` field
C. an assistant message you prefill with `"- "`
D. `output_config={"style": "bullets"}`

**6. (Spot-the-bug · D6)** A teammate's request:
```python
client.messages.create(
    model="claude-sonnet-5", max_tokens=1024,
    thinking={"type": "enabled", "budget_tokens": 8000},
    messages=[{"role": "user", "content": prompt}],
)
```
It returns HTTP 400. The cause is:
A. `max_tokens` must be ≥ 4096 when thinking is on
B. `budget_tokens` must be less than `max_tokens`
C. `thinking` with `budget_tokens` is not accepted on this model; use `{"type": "adaptive"}`
D. `thinking` must be a top-level sibling of `model`, not a dict

**7. (SBA · D2)** After a `with client.messages.stream(...) as stream:` block, the correct
way to get the complete message (usage, stop_reason, all blocks) is:
A. concatenate everything yielded by `stream.text_stream`
B. `stream.get_final_message()`
C. read `stream.response.usage` while streaming
D. make a second non-streaming call with the same messages

**8. (Scenario · D2)** Which situation is the **weakest** reason to stream?
A. Output may be several thousand tokens
B. You're rendering the answer live in a chat UI
C. You need the full answer before you can parse it as JSON, and latency doesn't matter
D. `max_tokens` is set to 64000

**9. (MR · D4 — choose ALL that apply)** Which errors are worth **retrying** with backoff?
A. `RateLimitError` (429)
B. `AuthenticationError` (401)
C. `APIStatusError` with `status_code == 529` (`overloaded_error`)
D. `BadRequestError` (400)
E. `APIConnectionError`

**10. (SBA · D4)** The Anthropic SDK, out of the box:
A. never retries — you must implement it
B. retries every error type indefinitely
C. retries 408/409/429/5xx and connection errors with exponential backoff, `max_retries=2`
D. retries only 429, and only once

**11. (Scenario · D4)** A request comes back with HTTP 200 and `stop_reason == "refusal"`.
Your code does `text = response.content[0].text` and crashes. Why, and what should you do?
A. The key is invalid; catch `AuthenticationError`
B. On a refusal `content` may have no text block; check `stop_reason` before reading content
C. Refusals raise `APIStatusError`; wrap in try/except
D. Add `max_retries=5`; refusals are transient

**12. (SBA · D1)** In a manual tool loop, immediately after receiving any response you must:
A. check `stop_reason` and return if it's `end_turn`
B. append `{"role": "assistant", "content": response.content}` to `messages`
C. append a `tool_result` user message
D. call `response.model_dump()` and log it

**13. (Scenario · D1)** One assistant response contains **three** `tool_use` blocks. To
continue the loop you append:
A. three separate user messages, one `tool_result` each
B. one user message whose `content` is a list of three `tool_result` blocks, ids matching
C. one user message with the concatenated tool outputs as a single string
D. one assistant message with the tool outputs

**14. (Spot-the-bug · D1)** This loop sometimes 400s with "roles must alternate":
```python
while True:
    r = client.messages.create(model=M, max_tokens=1024, tools=TOOLS, messages=messages)
    if r.stop_reason == "tool_use":
        results = [run(b) for b in r.content if b.type == "tool_use"]
        messages.append({"role": "user", "content": results})
        continue
    return text_of(r)
```
The bug is:
A. `tools=TOOLS` should only be passed on the first call
B. the assistant turn (`r.content`) is never appended before the `tool_result` user message
C. `results` should be a string, not a list
D. `continue` should be `break`

**15. (SBA · D2)** `client.messages.count_tokens(...)` accepts:
A. `model`, `system`, `messages`, `tools`
B. `model`, `max_tokens`, `messages`
C. only a single `text` string
D. the same arguments as `messages.create`, including `max_tokens` and `temperature`

**16. (Predict-the-output · D2)** `messages=[{"role": "assistant", "content": "Hi"}]` as the
*first and only* message. Result?
A. Works — Claude continues from "Hi"
B. HTTP 400 — the first message must have role `user`
C. Works, but `stop_reason` is `refusal`
D. The SDK silently inserts an empty user message

**17. (SBA · D6 · judgement)** Two prompt variants both produce correct answers. Variant A
is a 400-word system prompt with five rules; variant B is a 60-word system prompt plus one
worked example. For a format-following task, the exam's preferred answer is usually:
A. A — more explicit rules is always safer
B. B — a concrete example steers format better and costs fewer tokens
C. whichever has lower latency, regardless of quality
D. neither — use `output_config` instead

**18. (Scenario · D4 · cost)** A feature calls Claude 20,000×/day with an identical 12 KB
system prompt and a short varying question. Biggest single lever to cut cost, before
touching model choice:
A. lower `max_tokens`
B. switch every call to Haiku
C. prompt caching on the stable system-prompt prefix
D. batch the requests

---
---

## Answers & rationale

**1 — D.** Token counting is its own endpoint (`/v1/messages/count_tokens`).
- A/B/C wrong: tools, vision, and thinking are all *parameters* of `POST /v1/messages`.
  Recognising that "one endpoint, many parameters" model is a D2 staple.  
`refs: cs:count_tokens L1`

**2 — C.** A typed block object; access `.type` then `.text`.
- A: you *can* often `str()` it but `content[0]` isn't a `str`. B: that's the *input* shape
  you send, not what you get back. D: `response.model_dump_json()` would give that; not
  `content[0]`.  
`refs: cs:messages_basics L2`

**3 — A & C.** `end_turn` and `max_tokens` are real.
- B `tool_call` — the real value is `tool_use`. D `content_filter` — that's an
  OpenAI-ism; Claude uses `refusal`. E `token_limit` — invented. Distractors here are all
  "plausible name, wrong system".  
`refs: cs:messages_basics R:http-errors L2`

**4 — B.** Stream with more room — no timeout risk, no truncation.
- A: retrying an identical request just truncates again. C: "stops cleanly" but still
  incomplete — doesn't deliver the report. D: a `\n\n` stop sequence would cut it off even
  *earlier*.  
`refs: cs:messages_basics R:http-errors L5`

**5 — B.** The `system` field is the durable, every-turn contract.
- A: works but drifts and wastes tokens; not "most reliable". C: **prefill is removed on
  current models** (400). D: `output_config` has no `style` key — invented.  
`refs: cs:prompt_structure L16`

**6 — C.** `budget_tokens` is deprecated and rejected on current models; use
`{"type": "adaptive"}` + `output_config.effort`.
- A/B: no such rule. D: `thinking` *is* a dict parameter — that part is fine. This is the
  canonical "your training data is stale" exam question.  
`refs: cs:messages_basics L2`

**7 — B.** `stream.get_final_message()` reconstructs the whole `Message`.
- A: gives you text only — no usage/stop_reason/other blocks. C: `usage` isn't final
  mid-stream. D: correct data, but a wasteful second call and it re-bills you.  
`refs: cs:streaming R:streaming-events L3`

**8 — C.** If you must have the whole answer before acting and latency is irrelevant,
streaming buys you little. (Even then it avoids timeouts on huge outputs, but it's the
weakest case listed.)
- A, B, D are all *strong* reasons to stream (timeout risk, live UI, huge `max_tokens`).  
`refs: cs:streaming L3`

**9 — A, C, E.** 429, ≥ 500, and connection errors are transient.
- B (401) and D (400) are your fault — retrying can't fix a bad key or a malformed request.  
`refs: cs:retry_chain R:http-errors L5`

**10 — C.** 408/409/429/5xx + connection errors, exponential backoff, `max_retries` default
2.
- A: false — it does retry. B: never "indefinitely". D: understates it.  
`refs: cs:retry_chain R:http-errors`

**11 — B.** A refusal is HTTP 200; `content` may lack a text block. Always check
`stop_reason` (and `stop_details`) before indexing `content`.
- A: no auth error occurred. C: refusals don't raise. D: refusals aren't transient; blind
  retry can trip safety systems.  
`refs: cs:messages_basics L5`

**12 — B.** Append the assistant turn first, always — the API is stateless and needs the
full alternation in `messages`.
- A: you do check `stop_reason`, but *after* appending. C: only when `stop_reason` is
  `tool_use`. D: optional logging, not required.  
`refs: cs:agent_loop_react L6`

**13 — B.** One user message, a list of `tool_result` blocks, `tool_use_id`s matching.
- A: splitting across messages trains the model to stop parallelising. C: loses the id
  linkage; wrong block type. D: tool results go in a **user** message.  
`refs: cs:agent_loop_react L6`

**14 — B.** The assistant turn (`r.content`) is never appended, so `messages` goes
`user → user(tool_result)` — roles don't alternate.
- A: `tools` should be passed every call. C: `tool_result` content can be a list/blocks; a
  list of results is fine. D: `continue` is correct here.  
`refs: cs:agent_loop_react L6`

**15 — A.** `model`, `system`, `messages`, and `tools` (so tool tokens are counted).
- B/D: it does **not** take `max_tokens` / sampling params. C: it takes full message
  structure, not a bare string.  
`refs: cs:count_tokens`

**16 — B.** HTTP 400 — the first message must be role `user`.
- A: no. C: it errors, doesn't refuse. D: the SDK doesn't paper over this.  
`refs: cs:messages_basics L2`

**17 — B.** A concrete example usually steers format better than piling on rules, and it's
cheaper. The exam rewards "simpler / cheaper / example-driven" when quality is equal.
- A: "always" is the tell of a wrong option. C: quality isn't "regardless". D: `output_config`
  doesn't do arbitrary formatting.  
`refs: cs:prompt_structure L16`

**18 — C.** Caching the stable 12 KB prefix drops repeated input cost by ~90% for the
cached portion — huge at 20k calls/day, and it's free quality-wise.
- A: output is already short. B: changing model is a quality tradeoff and the question says
  "before touching model choice". D: batch gives 50% but adds latency and doesn't touch the
  repeated-prefix waste.

---

`refs: cs:prompt_caching R:caching-batch L14 E11`

### Mark yourself

18 items. **≥ 14** = on track for this domain cluster. Log per-domain hits/misses on the
roster. Any domain < 60%: revise it tonight against `question-bank/domain-N-*.md`.  
