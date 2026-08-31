# Lab 3 · Make the call production-shaped

**Domain:** 1 — fundamentals · 7 — reliability
**Time:** 40 min
**You will practise:** typed exceptions (`AuthenticationError`, `RateLimitError`,
`APIStatusError`, `APIConnectionError`), retry-with-backoff (and knowing the SDK already does
some of it), per-request `timeout`, `client.messages.count_tokens`, and computing real cost
from `usage`.

---

## Goal

Wrap the explainer call so that it:

1. **Estimates input cost before sending** using `count_tokens`.
2. **Retries** transient failures (429, 5xx, connection errors) with exponential backoff,
   but **fails fast** on 400/401/404 (retrying those is pointless).
3. Uses a **timeout** so a hung request doesn't block forever.
4. Prints **actual cost** afterwards from `response.usage`.

Then prove the error path works:

```
cd day1-foundations
python labs/lab3_resilient/solution/resilient.py labs/lab1_explainer/sample.py
python labs/lab3_resilient/solution/resilient.py labs/lab1_explainer/sample.py --break-key
```

---

## Teaching points (before they code)

- The SDK **already** retries 408/409/429/5xx with backoff (`max_retries`, default 2). You
  usually tune that number rather than hand-roll a loop. This lab hand-rolls one anyway so
  you *understand* what the SDK is doing — and because sometimes you need custom logic
  (e.g. honour a `retry-after` header, or give up after a wall-clock budget).
- Catch a **chain, most-specific first**: `AuthenticationError` / `BadRequestError` /
  `NotFoundError` → don't retry. `RateLimitError` / `APIStatusError(>=500)` /
  `APIConnectionError` → retry. A single `except Exception` throws away that distinction.
- `count_tokens` is a **separate, free-ish endpoint**. Use it to predict spend before firing
  an expensive call, or to decide whether a prompt will even fit.

---

## Expected output

Normal run:

```
estimate: ~181 input tokens  ≈ $0.000181 in  (Haiku 4.5 @ $1.00/Mtok in)
[attempt 1] calling claude-haiku-4-5 ...
ok.

<explanation text>

actual cost: in=181 ($0.000181) + out=104 ($0.000520) = $0.000701
```

`--break-key` run:

```
estimate: ~181 input tokens  ≈ $0.000181 in
[attempt 1] calling claude-haiku-4-5 ...
FATAL: authentication failed (401) — bad or missing API key. Not retrying.
```

(If you force a rate-limit scenario, you'd instead see `[attempt 1] ... rate limited,
backing off 1.4s`, then `[attempt 2] ...`.)

---

## Checkpoints

- [ ] Their `except` clauses are **ordered specific → general**; 401/400/404 are **not**
      retried.
- [ ] Backoff is **exponential with jitter** (`base * 2**attempt + random`), capped.
- [ ] They call `count_tokens` **before** `messages.create`, not after.
- [ ] Cost math uses the right per-token price (divide the per-million price by 1e6).

## Common mistakes

| Symptom | Cause |
|---|---|
| Bad key still retries 3× slowly | `AuthenticationError` caught by a broad `except` and treated as transient |
| Retries hammer instantly | no `sleep`, or fixed delay instead of exponential |
| Cost is off by 1e6 | used the per-million number as a per-token number |
| `count_tokens` errors | passed `max_tokens`/`system` it doesn't accept — pass only `model`, `system`, `messages` |

## Going further

- Honour the `retry-after` header on 429 instead of your computed backoff.
- Add a total wall-clock budget: stop retrying after 30s regardless of attempt count.
- Swap `MODEL` to `claude-sonnet-5` and watch the estimate change.
