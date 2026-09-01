# Domain 4 — Eval, Testing, and Debugging  ·  2.6%  ·  decision ④

> **Status: populated (8/8).** Anchor: `ep01` (stop_reason handling), `evals/`. Video: lesson 9.
> Taught Day 1 Module 4 (errors) + Day 4 Module 5 (eval). Deeper prose:
> `../topic-briefings.md` · Day 1 · "Errors & debugging" and Day 4 · "Evaluation";
> checklist: `../blueprint-mastery-map.md` 4.1.

## Sub-area & topics

| Sub-area | Weight | Items | Topics |
|---|---:|---:|---|
| Debugging and Error Handling | 2.6% | 8 | the **three places a call can break** (before it leaves — 400/401/402/403/413; in transit — 429 / **529** / connection; after 200 — truncation / refusal / wrong shape) · typed exceptions, retry vs don't-retry · `rate_limit` (429, yours) vs `overloaded` (**529**, theirs) · `stop_reason` / `stop_details` · request id for support · integration-layer vs model-output isolation · regression testing (assert on structure, not wording) · grading decision tree (exact / code-graded / LLM-judge) · judge-before-score |

---

## Items

### 1. (SBA) `overloaded_error` vs `rate_limit_error` — which is yours to fix?
A. both  B. `rate_limit_error` (your traffic spiked)  C. `overloaded_error`  D. neither

> **Answer:** B — `overloaded` (529) is Anthropic-side load; back off and retry, but it isn't a quota you own.
> **Distractors:** A/C/D — misattribute ownership.

### 2. (SCN) A streaming response reported success but the text looks half-finished. Where do you look?
A. the HTTP status code  B. the stream **events** — an error can arrive mid-stream and `message_delta` carries the real `stop_reason`  C. `max_retries`  D. the API key

> **Answer:** B.
> **Distractors:** A — 200 was already returned. C/D — unrelated knobs.

### 3. (SBA · judgement) A regression test for a summariser should:
A. assert the exact output string  B. assert required structure + key content, not wording  C. lower `max_tokens` for determinism  D. pin `temperature`

> **Answer:** B — output wording varies by design; test the contract.
> **Distractors:** A — brittle, fails on valid paraphrases. C/D — **symptom-treater**: chase determinism instead of testing the right thing.

### 4. (MR · choose ALL retryable) Which get a backoff-and-retry?
A. `RateLimitError` 429  B. `AuthenticationError` 401  C. `APIStatusError` 529  D. `BadRequestError` 400  E. `APIConnectionError`

> **Answer:** A, C, E — transient: your traffic, their load, the network.
> **Distractors:** B — fix the key. D — fix the request. Retrying can't help either.

### 5. (SBA · which code) Anthropic's API returns which status for "servers overloaded, try again"?
A. 503  B. 500  C. 529  D. 429

> **Answer:** C — **529** `overloaded_error`. (**Right-word-wrong-place**: 503 is the generic web answer but not this API's code.)
> **Distractors:** B — generic server error, not the overloaded signal. D — that's *your* rate limit.

### 6. (BUG) Code does `text = resp.content[0].text` and crashes on some HTTP-200 responses; `resp.stop_reason` on those is `"refusal"`. Why?
A. bad key — catch `AuthenticationError`  B. on a refusal `content` may have no text block; check `stop_reason` before indexing  C. refusals raise `APIStatusError`  D. add `max_retries=5`

> **Answer:** B — a refusal is a normal 200 outcome, never an exception.
> **Distractors:** A/C — **wrong-system**: attribute a 200 outcome to an exception path. D — irrelevant.

### 7. (SCN · isolate the layer) A tool call intermittently fails with the model saying it "got no result". You find the `tool_result` you send back sometimes carries a different `tool_use_id` than the `tool_use`. This bug is in the:
A. model's reasoning  B. integration layer — the id pairing is your code's job  C. Anthropic API  D. the tool's own logic

> **Answer:** B — mismatched `tool_use_id` is an integration-layer defect; the fix is in your loop, not the prompt.
> **Distractors:** A/C/D — misdirect to layers that aren't at fault.

### 8. (SBA · grading method) You need to grade open-ended answer quality (faithfulness, tone). Best approach, and the key technique?
A. exact string match against a golden answer  B. an LLM-as-judge, prompted for strengths / weaknesses / reasoning **before** the score  C. count characters  D. check the JSON parses

> **Answer:** B — reasoning-before-score stops the judge drifting to a safe ~6; calibrate against human labels first.
> **Distractors:** A/C — can't measure quality. D — checks shape, not faithfulness.
