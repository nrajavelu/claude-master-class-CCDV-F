# Domain 2 — Applications and Integration  ·  sub-area: **Claude API Mechanics**

CCDV-F Domain 2 is **33.1%** of the exam — the largest domain. **Items 1–28** are the
**Claude API Mechanics** sub-pool (from Day 1). **Items 29–48** cover the other five D2
sub-areas — Understanding Requirements, Systems Life Cycle, Software Engineering Foundations,
Claude Application Design, Configuration Management (from Day 4). Deeper prose:
`../topic-briefings.md` · Day 4; checklist: `../blueprint-mastery-map.md` 2.1–2.6.

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

---

## D2 sub-areas 2–6 — Requirements · Life Cycle · SW-Eng · App Design · Config Mgmt

### 29. (SBA · Understanding Requirements) Which is an actual *requirement* you can design and test against?
A. "make the support team faster"  B. "draft replies in under 3 s p95 measured from Frankfurt, processing no customer data outside the EU"  C. "use the best model"  D. "reduce the ticket backlog"

> **Answer:** B
> **Why:** Verifiable, with latency and residency pinned; it becomes an eval criterion.
> **Distractors:** A/D — **true-but-irrelevant**: the business problem restated. C — **right-word-wrong-place**: a solution, not a requirement.

### 30. (SBA · Understanding Requirements) Infrastructure requirements sit on four axes:
A. cost, speed, quality, scope  B. latency (from the user's region), scale (peak volume), residency (where data is processed), identity (credential model + audit)  C. CPU, RAM, disk, network  D. uptime, latency, throughput, cost

> **Answer:** B
> **Distractors:** A — project-management triangle. C — machine specs. D — overlaps but misses residency/identity, the exam's focus.

### 31. (SCN · Understanding Requirements) A stakeholder says "we want Claude to help EU agents clear their backlog faster." First move?
A. start building a prototype  B. derive functional behaviours + infrastructure constraints (incl. the EU-residency source) and record them as eval criteria and design constraints  C. pick a model  D. choose a cloud

> **Answer:** B
> **Distractors:** A/C/D — jumping to a solution before requirements exist.

### 32. (SBA · Systems Life Cycle) The systems life cycle arc the guide uses:
A. plan → code → ship  B. Requirements → Design → Build → Test → Deploy → Operate → Iterate, with gates between phases  C. design → deploy → forget  D. build → break → fix

> **Answer:** B
> **Distractors:** A/C/D — miss the gates and the Operate/Iterate tail where production credit is earned.

### 33. (SCN · Systems Life Cycle) When should the eval suite for a Claude feature first exist?
A. after launch, once real failures appear  B. during Build — it gates Deploy and validates every later prompt/model change  C. only for regulated data  D. during Requirements, before any code

> **Answer:** B
> **Distractors:** A — **symptom-treater**: waits for production pain. C — **extremist** ("only if"). D — too early to write meaningful cases.

### 34. (SBA · Systems Life Cycle) Why do Claude apps need *continuous* monitoring where traditional software often doesn't?
A. they crash more  B. model behaviour can shift on a version bump and prompts drift with usage, so quality isn't frozen at release  C. tokens expire  D. the API changes weekly

> **Answer:** B
> **Distractors:** A/C/D — invented or exaggerated.

### 35. (SBA · SW-Eng Foundations) `AsyncAnthropic` gives you:
A. lower latency on a single call  B. concurrency — many calls overlap; one call is no faster  C. lower token cost  D. automatic batching

> **Answer:** B
> **Distractors:** A/C — false. D — chunking async calls is not the Batch API.

### 36. (SCN · SW-Eng Foundations) A team ships a "just wording" prompt tweak straight to prod with no review; reply tone shifts and a downstream classifier's accuracy drops. Root cause?
A. the model regressed  B. a prompt is code — the change needed review and a CI eval-suite run  C. the classifier needs retraining  D. temperature was too high

> **Answer:** B
> **Distractors:** A/C/D — **symptom-treater**: chase the downstream effect, not the missing process.

### 37. (SBA · SW-Eng Foundations) Code review of a Claude integration must additionally cover:
A. nothing extra  B. prompts and tool schemas — a schema change breaks every caller and no compiler catches it  C. only the model ID  D. only the tests

> **Answer:** B
> **Distractors:** A/C/D — understate the review surface.

### 38. (SCN · SW-Eng Foundations) A consultancy hardcodes one client's values throughout the code and ships no eval suite. The next engagement:
A. reuses it cleanly  B. has nothing to configure and no way to validate changes — a rewrite  C. only needs the model swapped  D. is unaffected

> **Answer:** B
> **Why:** Package for reuse — parameterise engagement-specific values, bundle the eval suite.
> **Distractors:** A/C/D — assume reusability that wasn't built.

### 39. (SBA · Application Design) The six deployment placements include first-party API, Claude Platform on AWS, Amazon Bedrock, Bedrock legacy, Google Vertex AI, and:
A. a local GPU only  B. a third-party platform such as Microsoft Foundry  C. GitHub Actions  D. a browser extension

> **Answer:** B
> **Distractors:** A/C/D — not model-hosting platforms.

### 40. (SCN · Application Design) A German insurer requires all customer data processed in the EU and runs on GCP. Which satisfies both?
A. first-party Claude API with a strict data-handling system prompt  B. Vertex AI in a europe-west region  C. Amazon Bedrock in us-east-1  D. Managed Agents

> **Answer:** B
> **Distractors:** A — **right-word-wrong-place**: a prompt is not a residency control; the direct API has no EU residency. C — wrong region. D — not residency-guaranteed here (**wrong-system**).

### 41. (SBA · Application Design) HIPAA BAA coverage for Claude **excludes**:
A. Amazon Bedrock in a HIPAA-eligible account  B. Google Vertex AI  C. the Console / Workbench / beta features / consumer plans  D. the first-party API under a signed BAA

> **Answer:** C
> **Distractors:** A/B/D — all can be covered; the Console and beta surfaces cannot.

### 42. (SBA · Application Design) Measure a deployment platform on three dimensions:
A. brand, docs, popularity  B. latency from the customer's actual region with the actual payload · compliance as a pass/fail gate at scoping · total cost per call (tokens + egress + integration)  C. only cost  D. only compliance

> **Answer:** B
> **Distractors:** A — irrelevant. C/D — single-axis.

### 43. (SBA · Application Design) A strict, detailed system prompt about "never store or transmit data outside region X" is:
A. a valid data-residency control  B. not a compliance or residency control — those are enforced by endpoint, region, and contract, decided before any prompt is written  C. sufficient with temperature 0  D. required for FedRAMP

> **Answer:** B
> **Distractors:** A/C/D — treat guidance as enforcement (**right-word-wrong-place**).

### 44. (SCN · Application Design) A workload needs FedRAMP authorisation. Valid route?
A. the standard AWS Marketplace listing  B. Claude for Government, Bedrock GovCloud, or Vertex Assured Workloads  C. the first-party API with audit logging on  D. any region if you enable ZDR

> **Answer:** B
> **Distractors:** A/C/D — none carry FedRAMP authorisation.

### 45. (SBA · Configuration Management) An alias like `claude-sonnet` vs a pinned ID like `claude-sonnet-5-YYYYMMDD`:
A. identical  B. the alias is a moving target that updates over time and can differ by platform; the pinned ID is fixed until you edit the line — production pins  C. the pinned ID auto-updates  D. aliases are safer for production

> **Answer:** B
> **Distractors:** A/C/D — invert or flatten the distinction.

### 46. (SCN · Configuration Management) Prod points at the `claude-sonnet` alias. Overnight it advances, the response JSON gains a field, a parser throws `KeyError`, and there's no fast way back. What should have been in place?
A. a broader `try/except`  B. a pinned full model ID, the prior version retained for rollback, and promotion gated on an eval run  C. a retry with backoff  D. streaming

> **Answer:** B
> **Distractors:** A/C/D — **symptom-treater**: patch the crash, not the config practice.

### 47. (SBA · Configuration Management) Which four artifacts are version-controlled, reviewed, and eval-validated like code?
A. only the source files  B. `CLAUDE.md`, `settings.json`, the model version pin, and prompt / few-shot versions  C. only the prompts  D. the API key and the endpoint URL

> **Answer:** B
> **Why:** None are compiled or type-checked — the eval suite is the only regression net.
> **Distractors:** A/C — too narrow. D — secrets, not config to commit.

### 48. (SBA · Configuration Management) "A small prompt wording tweak" is:
A. harmless, no need to track it  B. a deployment — it measurably shifts the output distribution, so it goes through review + eval like any release  C. only risky for classifiers  D. fine if temperature is 0

> **Answer:** B
> **Distractors:** A/C/D — understate that prompt edits change behaviour.
