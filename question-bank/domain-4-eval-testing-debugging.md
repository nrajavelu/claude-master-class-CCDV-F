# Domain 4 — Eval, Testing, and Debugging  ·  2.6%  ·  decision ④

> **Status: blueprint.** Item target **8**. Built pass 2/3 (Day 1 errors + Day 4 eval).
> Anchor: `ep01` (stop_reason handling). Video: lesson 9.

## Sub-area & topics

| Sub-area | Weight | Items | Topics |
|---|---:|---:|---|
| Debugging and Error Handling | 2.6% | 8 | the **three places a call can break** (before it leaves — bad request; in transit — rate limit / overloaded / connection; after 200 — truncation / refusal / wrong shape) · typed exceptions, retry vs don't-retry · `rate_limit` (yours) vs `overloaded` (theirs) · `stop_reason` / `stop_details` · request id for support · regression testing (assert on structure, not wording) · exact-match vs LLM-as-judge |

## Seed items

### 1. (SBA) `overloaded_error` vs `rate_limit_error` — which is yours to fix?
A. both  B. `rate_limit_error` (your traffic spiked)  C. `overloaded_error`  D. neither

> **Answer:** B. `overloaded` is Anthropic-side load; back off and retry, but it's not a
> quota you own.

### 2. (SCN) A streaming response reported success but the text looks half-finished. Where do
you look?
A. the HTTP status code  B. the stream **events** — an error can arrive mid-stream, and
`message_delta` carries the real `stop_reason`  C. `max_retries`  D. the API key

> **Answer:** B.

### 3. (SBA · judgement) A regression test for a summariser should:
A. assert the exact output string  B. assert required structure + key content, not wording
C. lower `max_tokens` for determinism  D. pin `temperature`

> **Answer:** B — output wording varies by design; test the contract, not the prose.
