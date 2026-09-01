# Domain 2 — Applications and Integration  ·  sub-area: **Claude API Mechanics**

CCDV-F Domain 2 is **33.1%** of the exam. This file currently holds the **Claude API
Mechanics** sub-pool (28 items). The other D2 sub-areas — Understanding Requirements, Systems
Life Cycle, Software Engineering Foundations, Application Design, Configuration Management —
are added in the Day 4 build pass.

A handful of items below also touch **D5** (Technical Fundamentals: tokens, context, cost)
and **D4** (Debugging & Error Handling); they're tagged inline where so.

Anchor: `ep01/agent.py`; Day 1 Modules 1, 3, 4, 5.
Styles: SBA · MR · SCN · OUT · BUG · JDG. Answer + why + per-distractor rationale under each.

---

### 1. (SBA) Which endpoint does a normal Claude text generation request go to?
A. `/v1/chat/completions`  B. `/v1/messages`  C. `/v1/generate`  D. `/v1/completions`

> **Answer:** B
> **Why:** The Messages API (`POST /v1/messages`) is the single endpoint for Claude.
> **Distractors:** A — OpenAI's path (wrong system). C — invented. D — the retired legacy
> Text Completions API; not used for current models.

---

### 2. (SBA) `client = anthropic.Anthropic()` with no arguments will authenticate using:
A. nothing — it always requires `api_key=`
B. the `ANTHROPIC_API_KEY` environment variable (or another resolved credential)
C. an interactive browser login
D. a config file you must pass explicitly

> **Answer:** B
> **Why:** The zero-arg client resolves `ANTHROPIC_API_KEY` from the environment (and can
> fall back to other configured credentials).
> **Distractors:** A — false, that's the point of the default. C — that's Claude Code's OAuth
> flow, not the SDK client. D — not required.

---

### 3. (MR — choose TWO) Which are **required** on every `messages.create` call?
A. `model`  B. `system`  C. `max_tokens`  D. `temperature`  E. `tools`

> **Answer:** A, C
> **Why:** `model` and `max_tokens` are mandatory. `system`, `temperature`, `tools` are
> optional.
> **Distractors:** B/E — optional. D — optional (and removed on some current models).

---

### 4. (SBA) `max_tokens` controls:
A. the maximum size of the input prompt
B. the maximum number of tokens Claude will generate in the response
C. the context window size
D. how many tool calls are allowed

> **Answer:** B
> **Why:** It's a hard ceiling on the *output*. Hitting it yields `stop_reason: "max_tokens"`
> and truncation.
> **Distractors:** A/C — the context window is a model property, not this field. D — no such
> control.

---

### 5. (OUT) `messages=[{"role": "assistant", "content": "Hello"}]` as the only message:
A. Claude continues from "Hello"
B. HTTP 400 — the first message must be `user`
C. works but returns empty
D. the SDK inserts a `user` message automatically

> **Answer:** B
> **Why:** The conversation must begin with a `user` turn.
> **Distractors:** A/C — it errors before generating. D — no silent fix-up.

---

### 6. (SBA) `response.content` is:
A. a string
B. a list of typed content blocks
C. a dict keyed by block type
D. `None` unless you request text output

> **Answer:** B
> **Why:** Always a list; iterate and switch on `block.type` (`text`, `thinking`,
> `tool_use`, …).
> **Distractors:** A — common wrong assumption. C — not a dict. D — text is the default.

---

### 7. (SBA) To extract the assistant's text from a plain reply:
A. `response.text`
B. `response.content[0].text` (always safe)
C. `"".join(b.text for b in response.content if b.type == "text")`
D. `response.message`

> **Answer:** C
> **Why:** Robust against non-text blocks (thinking, tool_use) appearing first.
> **Distractors:** A/D — no such attribute. B — breaks whenever block 0 isn't text.

---

### 8. (MR — choose ALL valid) `stop_reason` values:
A. `end_turn`  B. `max_tokens`  C. `tool_use`  D. `stop_sequence`  E. `pause_turn`
F. `refusal`  G. `function_call`

> **Answer:** A, B, C, D, E, F
> **Why:** All six are real. `function_call` (G) is an OpenAI term — Claude uses `tool_use`.
> **Distractors:** G — wrong system.

---

### 9. (SCN) `stop_reason == "tool_use"` but `response.content` has only a text block, no
`tool_use` block. Most likely explanation?
A. impossible — the API guarantees a `tool_use` block
B. you're inspecting the wrong response, or filtered the blocks incorrectly
C. the tool failed server-side
D. you must set `tool_choice` to `"any"`

> **Answer:** B
> **Why:** `tool_use` stop_reason always comes with at least one `tool_use` block; if you
> don't see one you're looking at the wrong object or your filter is wrong.
> **Distractors:** A — it's not "impossible", it's "you have a bug". C — that's a tool_result
> concern, not this. D — unrelated.

---

### 10. (SBA) `response.usage` gives you:
A. latency in milliseconds
B. `input_tokens`, `output_tokens`, and cache token counters
C. your remaining account balance
D. the number of messages in the conversation

> **Answer:** B
> **Why:** `usage` is the billing surface for the call.
> **Distractors:** A — not reported here. C — check the Console. D — no.

---

### 11. (SBA) The Messages API is **stateless**. Practically, that means:
A. it can't be used for chat
B. you must resend the full conversation history on every request
C. responses are not cached
D. you can't use tools

> **Answer:** B
> **Why:** No server-side session; `messages` carries the entire history each call.
> **Distractors:** A — chat works fine, you just manage history. C — unrelated (prompt
> caching exists). D — unrelated.

---

### 12. (SBA) `system` is:
A. the first element of the `messages` list with `role: "system"`
B. a top-level parameter of `messages.create`, separate from `messages`
C. only available on Opus models
D. deprecated; use a user message instead

> **Answer:** B
> **Why:** It's its own field. (A separate, model-gated "mid-conversation system message"
> feature exists, but the primary system prompt is the top-level `system` param.)
> **Distractors:** A — not how the primary system prompt is passed. C/D — false.

---

### 13. (SCN) A report feature returns `stop_reason: "max_tokens"` and cuts off. Best fix?
A. retry the identical request
B. stream with a higher `max_tokens`
C. reduce `max_tokens`
D. add `stop_sequences`

> **Answer:** B
> **Why:** More room + streaming avoids both truncation and the HTTP timeout on long output.
> **Distractors:** A — truncates again. C — stops cleanly but still incomplete. D — cuts it
> off sooner.

---

### 14. (SBA) You must stream (rather than a plain call) primarily to avoid:
A. rate limits
B. the HTTP request timeout on long / high-`max_tokens` responses
C. token costs
D. refusals

> **Answer:** B
> **Why:** Non-streaming holds the connection until done; long generations can exceed the
> client timeout.
> **Distractors:** A/C/D — streaming doesn't change any of these.

---

### 15. (SBA) After `with client.messages.stream(...) as stream:`, the complete `Message`
(usage, stop_reason, all blocks) comes from:
A. `stream.text_stream` joined into a string
B. `stream.get_final_message()`
C. `stream.usage`
D. a second `messages.create` call

> **Answer:** B
> **Distractors:** A — text only. C — not final mid-stream. D — wasteful and re-bills.

---

### 16. (SBA) `client.messages.count_tokens(...)` accepts:
A. `model`, `system`, `messages`, `tools`
B. `model`, `max_tokens`, `messages`
C. a single string
D. exactly the same params as `messages.create`

> **Answer:** A
> **Why:** It counts the full prompt including tool schemas; it does **not** take
> `max_tokens` or sampling params.
> **Distractors:** B/D — no `max_tokens`. C — takes structured messages.

---

### 17. (SCN) You want to know a prompt's cost **before** sending it. You:
A. send it and read `usage`
B. call `count_tokens` and multiply by the model's per-token input price
C. estimate 4 characters per token
D. there's no way to know in advance

> **Answer:** B
> **Why:** `count_tokens` is the accurate, pre-flight way.
> **Distractors:** A — that's *after*, and it costs. C — a rough rule, not "know". D — false.

---

### 18. (SBA) Input tokens vs output tokens, on pricing:
A. same price
B. output tokens cost more than input tokens
C. input tokens cost more than output tokens
D. output tokens are free

> **Answer:** B
> **Distractors:** A/C/D — output is consistently the dearer side across the model line.

---

### 19. (SBA) `cache_read_input_tokens` in `usage` is billed at roughly:
A. full input price
B. ~0.1× the input price
C. ~1.25× the input price
D. free

> **Answer:** B
> **Why:** Cache *reads* are ~10% of the input rate (cache *writes* are ~1.25×).
> **Distractors:** A — that's uncached input. C — that's a cache write. D — not free.

---

### 20. (BUG) A dev reports "`AttributeError: 'dict' object has no attribute 'text'`" on
`response.content[0].text`. The cause:
A. the response is malformed JSON
B. they built the request wrong
C. nothing — that's expected; `content[0]` on a response is a block object, so this error
   means they're actually iterating something they constructed, or on an old SDK
D. `max_tokens` too low

> **Answer:** C
> **Why:** Response blocks are objects; a `dict` here means they're looking at request-shaped
> data (what you *send*), not the response.
> **Distractors:** A/B/D — don't produce this specific error.

---

### 21. (SBA) Which model id string is correctly formed for a current model?
A. `claude-sonnet-5`
B. `claude-sonnet-5-20260101`
C. `claude-3-5-sonnet`
D. `sonnet-latest`

> **Answer:** A
> **Why:** Current models use the bare alias; you do **not** append a date to the current
> aliases.
> **Distractors:** B — date-suffix form not used with current aliases. C — old naming
> scheme. D — not a valid id.

---

### 22. (SCN) You pass `model="claude-sonnet-5-typo"`. Which exception, and do you retry?
A. `RateLimitError`; retry
B. `NotFoundError` (404); do **not** retry
C. `APIConnectionError`; retry
D. `BadRequestError`; retry

> **Answer:** B
> **Why:** An unknown model is a 404 `NotFoundError`; retrying can't fix a typo.
> **Distractors:** A/C — wrong error. D — 400 also wouldn't be retried, but the error class
> here is `NotFoundError`.

---

### 23. (MR — choose ALL retryable) 
A. `RateLimitError` 429  B. `AuthenticationError` 401  C. 529 via `APIStatusError`
D. `APIConnectionError`  E. `BadRequestError` 400

> **Answer:** A, C, D
> **Why:** Transient = 429 / ≥500 / connection. 401 and 400 are caller errors.

---

### 24. (SBA) The SDK's default retry behaviour:
A. no automatic retries
B. retries 408/409/429/5xx + connection errors, exp backoff, `max_retries=2`
C. retries all 4xx and 5xx
D. retries once, fixed 1s delay

> **Answer:** B

---

### 25. (SBA) `stop_reason == "refusal"` is handled by:
A. an `except RefusalError` block
B. checking `stop_reason` before reading `content`; inspect `stop_details`
C. `except APIStatusError`
D. increasing `max_retries`

> **Answer:** B
> **Why:** HTTP 200, no exception. `stop_details.category` tells you why.
> **Distractors:** A/C — no exception is raised. D — not transient.

---

### 26. (SBA) The default request `timeout` in the SDK is about:
A. 30 seconds  B. 60 seconds  C. 10 minutes  D. no timeout

> **Answer:** C
> **Why:** ~10 minutes by default; override with `client.with_options(timeout=...)` or on
> the client.
> **Distractors:** A/B — too short. D — there is a default.

---

### 27. (JDG) You need one Claude call to classify 100k support tickets/day into 5 buckets.
Best default model?
A. Opus at `effort: max`
B. Haiku
C. Sonnet with extended thinking
D. whichever is newest, at `effort: max`

> **Answer:** B
> **Why:** High-volume, well-specified classification is the archetypal Haiku job — fast and
> cheap, and you verify the choice with a small eval.
> **Distractors:** A/C/D — over-provisioned for a bounded classification task; cost/latency
> hit with no quality need. (Note the general rule "start capable, measure down" still means
> you'd *check* Haiku is good enough with an eval — but for this shape it's the right
> starting bet.)

---

### 28. (SBA) Vision, tool use, PDF input, and extended thinking are:
A. four separate API endpoints
B. all parameters/content-block types of the one Messages API call
C. only available via Managed Agents
D. only available in the Agent SDK

> **Answer:** B
> **Why:** One endpoint, many parameters — the core mental model of Domain 1.
