# Domain 5 — Model Selection and Optimisation  ·  16.8%  ·  decision ② "how does it call Claude?"

> **Status: populated (26/26).** Anchor: `ep10`, `ep11`, `code-snippets/prompt_caching.py`,
> `batch_custom_id.py`, `count_tokens.py`. Video: lessons 2, 3, 10. Taught Day 1 (tokens,
> fundamentals) + Day 5 Modules 1–4. Deeper prose: `../topic-briefings.md` · Day 1 & Day 5;
> checklist: `../blueprint-mastery-map.md` 5.1–5.4.

## Sub-areas & item split

| Sub-area | Weight | Items | Topics |
|---|---:|---:|---|
| LLM Fundamentals | 5.2% | 8 | next-token sampling · no plan behind it · tokens ≠ words, never hardcode a ratio · non-determinism (inherent, not a stream artefact) · `temperature:0` ≠ deterministic · newest models reject `temperature`/`top_p` · context window = one shared budget · two failure modes (reject-on-input / stop-mid-output) · property assertions + judges, not exact strings |
| Technical Fundamentals | 6.1% | 9 | REST/JSON under the SDK · SSE streaming (not WebSocket) · streaming `tool_use` `input_json` reassembly · async = concurrency not latency · SDK auto-retry (408/409/429/5xx, `max_retries=2`) · `stop_reason` / `usage` · image tokens `⌈w/28⌉×⌈h/28⌉` · vision source types (`base64`/`url`/`file_id`) · PDF = text + page images |
| Model Selection & Trade-offs | 2.7% | 4 | Fable5/Opus5/Sonnet5 (adaptive) vs **Haiku 4.5 (extended, the odd one out)** · **start at Sonnet 5, move on eval evidence** · `effort` levels orthogonal to model · cascading |
| Cost & Token Management | 2.8% | 5 | `input_tokens` ≠ "your input" · usage tracking · **five levers in order** (caching → batch → right-size model → cap output → trim fat) · cost per completed task · caching prefix rules & silent invalidators · batch 100k/256MB/24h, any-order, `custom_id` |

---

## Items

### 1. (SBA · LLM Fundamentals) Same prompt, run twice, different wording. This is:
A. a bug  B. expected — generation samples among plausible continuations  C. a cache miss  D. a rate-limit artefact

> **Answer:** B.
> **Distractors:** A — inherent to sampling. C/D — unrelated.

### 2. (SBA · Technical Fundamentals) Streaming on this API uses:
A. a WebSocket  B. Server-Sent Events over the same HTTP call  C. long polling  D. gRPC

> **Answer:** B.
> **Distractors:** A — **right-word-wrong-place**, the guide's own word for the wrong thing. C/D — not used.

### 3. (SCN · Cost) 10,000 documents processed overnight, cost matters, nobody waits. Best mechanism?
A. run them in parallel with async  B. the Batch API  C. switch to Haiku  D. cap `max_tokens`

> **Answer:** B — the stem names the constraint (overnight, cost, not urgent).
> **Distractors:** A/C/D — generic knobs; **right-word-wrong-place**.

### 4. (SBA · Cost) `cache_read_input_tokens` is 0 across repeated identical-prefix calls. Most likely:
A. caching isn't supported  B. a silent invalidator in the prefix (`datetime.now()`, unsorted JSON, varying tools)  C. the model is too small  D. you need a beta header

> **Answer:** B.
> **Distractors:** A/C/D — misdirect.

### 5. (SBA · LLM Fundamentals) A test asserts the model's summary equals a fixed golden string. It passes locally, fails in CI, passes on re-run. Best fix?
A. set `temperature: 0` and keep the exact-string assertion  B. assert the summary is valid, ≤ 3 sentences, mentions the two required entities; add an LLM judge for faithfulness  C. pin the model and retry the test 3×  D. record the first CI output as the new golden

> **Answer:** B.
> **Distractors:** A/C/D — **symptom-treater**: fight non-determinism instead of testing the contract. `temperature:0` isn't a guarantee.

### 6. (SBA · LLM Fundamentals) Which is true about the context window?
A. the model silently drops the oldest turns when it fills  B. it's one shared budget across system + history + docs + tool results + output; oversized input is rejected before generation, and hitting the ceiling mid-generation stops with partial output  C. output has its own separate budget  D. it grows automatically on long conversations

> **Answer:** B.
> **Distractors:** A — your app must trim; the model won't. C/D — false.

### 7. (SBA · Technical Fundamentals) A streaming integration executes a tool as soon as it sees the tool name, using whatever `input_json` has arrived. It intermittently sends malformed args. Fix?
A. retry the tool on malformed input  B. wait for `message_stop`, reassemble the full `input_json`, then execute  C. disable streaming  D. `tool_choice: "any"`

> **Answer:** B — `tool_use` input is only complete at stream end.
> **Distractors:** A — **symptom-treater**. C — **extremist**. D — unrelated.

### 8. (SBA · Model Selection) The exam-keyed model-selection workflow is:
A. always use the most capable model  B. start at Sonnet 5; move up only when an eval shows a quality gap; move down to Haiku only when an eval shows the drop is acceptable  C. pick a tier by task type from a lookup table  D. use Haiku for everything and escalate on user complaints

> **Answer:** B.
> **Distractors:** A/C — not evidence-driven. D — **symptom-treater**.

### 9. (SBA · Model Selection) Which model is the "odd one out" on reasoning mode?
A. Sonnet 5 — adaptive  B. Opus 5 — adaptive  C. Fable 5 — adaptive  D. Haiku 4.5 — **extended** thinking (`thinking.type:"enabled"`), not adaptive

> **Answer:** D.
> **Distractors:** A/B/C — all Claude 5, all adaptive.

### 10. (SBA · Cost) The five cost levers, most powerful first:
A. trim prompts → cap output → right-size model → batch → caching  B. caching → batch → right-size model → cap output length → trim prompt fat  C. right-size model → caching → batch → trim → cap output  D. batch → caching → cap output → trim → right-size model

> **Answer:** B.
> **Distractors:** A — reversed. C/D — scrambled.

### 11. (SBA · Cost) `input_tokens` in a `usage` object counts:
A. only the text you typed in `messages`  B. system prompt + tool schemas + full history + injected docs — everything the model read  C. the output  D. the cached prefix only

> **Answer:** B.
> **Distractors:** A — undercounts badly. C — that's `output_tokens`. D — partial.

### 12. (SBA · Technical Fundamentals) A 1000×1000 image costs roughly how many tokens, and by what rule?
A. a flat 85 tokens  B. `⌈w/28⌉ × ⌈h/28⌉` ≈ 1,296 — 28×28-pixel patches  C. one token per pixel  D. images are free

> **Answer:** B.
> **Distractors:** A — a different vendor's number (**wrong-system**). C/D — false.

### 13. (SBA · Technical Fundamentals) `AsyncAnthropic` / `asyncio.gather` buys you:
A. lower latency per request  B. concurrency — many requests overlap; a single call is no faster  C. lower token cost  D. automatic batching

> **Answer:** B.
> **Distractors:** A/C — false. D — chunking async calls is **not** the Batch API.

### 14. (SCN · Model Selection) A team defaults every call to Fable 5 at `effort: max`. Latency/cost triple the budget; an eval shows Sonnet 5 at `effort: medium` scores within 1 point. Best move?
A. keep Fable 5, drop `effort` to `low`  B. move to Sonnet 5 at `effort: medium` — the eval supports it  C. move straight to Haiku 4.5  D. add caching and keep Fable 5

> **Answer:** B — move in the direction the evidence supports, one step.
> **Distractors:** A/D — keep the **overbuild**. C — **extremist**: no eval for Haiku yet.

### 15. (SBA · Cost) "Optimise cost per completed task, not per request" matters because:
A. requests are free  B. a retry-heavy or loop-heavy task on a "cheaper" setup can cost more overall than a pricier setup that succeeds first time  C. per-request billing doesn't exist  D. tasks are always one request

> **Answer:** B.
> **Distractors:** A/C/D — false premises.

### 16. (SCN · Cost) A support bot re-sends a 6,000-token policy doc in the system prompt every turn; costs are input-dominated. First lever?
A. switch to Haiku 4.5  B. put the policy behind a `cache_control` breakpoint so repeated turns read it from cache  C. cap `max_tokens` on the reply  D. summarise the policy to 1,000 tokens

> **Answer:** B — lever 1.
> **Distractors:** A/C/D — real levers, but not the first or biggest here (**right-word-wrong-place**).

### 17. (SBA · Cost) Batch API limits:
A. 1,000 requests, 10 MB, 1 h  B. 100,000 requests or 256 MB per batch, up to 24 h turnaround  C. unlimited requests, no size cap  D. 50 requests, real-time

> **Answer:** B.
> **Distractors:** A/C/D — wrong figures.

### 18. (SBA · Cost) Batch results must be matched to inputs by:
A. array position  B. `custom_id`  C. timestamp  D. the order you submitted

> **Answer:** B — results return in arbitrary order.
> **Distractors:** A/C/D — unreliable.

### 19. (SBA · LLM Fundamentals) On the newest top-tier models, setting `temperature: 0.2`:
A. slightly reduces randomness  B. is rejected with a 400 — those models don't accept `temperature`/`top_p`/`top_k`; steer with prompting  C. is required  D. disables sampling

> **Answer:** B.
> **Distractors:** A/C/D — assume the knob still exists.

### 20. (SBA · Technical Fundamentals) A streaming response drops the connection mid-answer. Correct handling?
A. use the partial text as-is  B. treat it as transient — retry the whole request; never pass partial blocks downstream  C. it's a 400, fix the request  D. lower `max_tokens`

> **Answer:** B.
> **Distractors:** A — malformed. C — it succeeded, then broke. D — unrelated.

### 21. (SBA · Model Selection) Capability and `effort` are:
A. the same dial  B. orthogonal — a capable model at low `effort` can beat a small model at `max` effort; measure both  C. `effort` only exists on Haiku  D. `effort` replaces model choice

> **Answer:** B.
> **Distractors:** A/C/D — conflate two independent decisions.

### 22. (SCN · Cost) A nightly job classifies 40,000 docs with `asyncio.gather` over `messages.create` in batches of 50, and the cost/rate-limit behaviour matches a plain sync loop. Why?
A. `asyncio` misconfigured — raise concurrency  B. chunking sync calls isn't batching — submit one Message Batches API job (≤100k, ≤24h, ~50% cost), match by `custom_id`  C. add caching to the loop  D. switch to streaming

> **Answer:** B.
> **Distractors:** A/C/D — optimise the wrong mechanism (**right-word-wrong-place**).

### 23. (SBA · Technical Fundamentals) The Anthropic SDK, out of the box:
A. never retries  B. retries every error forever  C. retries 408/409/429/5xx + connection errors with exponential backoff, `max_retries=2`  D. retries only 429, once

> **Answer:** C.
> **Distractors:** A/B/D — wrong policy.

### 24. (SBA · LLM Fundamentals) "The model plans its whole answer, then writes it." This is:
A. correct  B. wrong — it samples one token at a time, each conditioned on all prior tokens; there's no separate plan  C. correct only with thinking enabled  D. correct for Opus

> **Answer:** B.
> **Distractors:** A/C/D — anthropomorphise the mechanism.

### 25. (SBA · Technical Fundamentals) Best vision source type for a multi-turn conversation that refers back to the same 10 images repeatedly?
A. `base64` inline  B. Files API `file_id` — upload once, reference thereafter  C. `url` to a random image host  D. paste them as text

> **Answer:** B — `base64` is re-sent in full every turn.
> **Distractors:** A — expensive here. C — fragile. D — impossible.

### 26. (SBA · Model Selection) "Cheap model first, escalate to a stronger one only on failure" is:
A. routing  B. cascading — it beats paying premium on every request when most are easy  C. evaluator-optimiser  D. always wrong

> **Answer:** B.
> **Distractors:** A/C — different patterns. D — false.
