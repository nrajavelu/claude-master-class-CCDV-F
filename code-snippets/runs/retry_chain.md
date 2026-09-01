# Retry the transient, fail fast on the rest

> Worked example · **Day 1** · exam domain **D4** · source `code-snippets/retry_chain.py`
> Run it yourself: `python code-snippets/retry_chain.py`

## Scenario

One call wrapped in a typed-exception chain: back off on 429 / 529 / ≥500 / connection; raise immediately on 400 / 401 / 403 / 404 / 413.

**Input / dataset.** A normal call, then a call with a deliberately bad key.

## The code

<!-- CODE:START -->
```python
"""
retry_chain.py — catch a CHAIN, most-specific first. Retry vs fail-fast.

Exam angles (D4 · Eval, Testing & Debugging):
  * RETRY (transient): RateLimitError 429 · overloaded_error 529 · APIStatusError >=500
                       · APIConnectionError
  * FAIL FAST (yours): BadRequestError 400 · AuthenticationError 401 · billing_error 402 ·
                       PermissionDeniedError 403 · NotFoundError 404 · request_too_large 413
  * a single `except Exception` throws the distinction away
  * the SDK already retries 408/409/429/5xx + connection, max_retries=2 (default)
  * 529 (NOT 503) is this API's overloaded code. `overloaded` (529) = Anthropic-side load;
    `rate_limit` (429) = your traffic spike (yours to fix)
  * `refusal` is NOT an exception -- it's a stop_reason (check stop_details for the category)

    cd aizentify-cdf-bootcamp && python code-snippets/retry_chain.py
"""
import random
import time
from dotenv import load_dotenv
import anthropic

load_dotenv()


def call_with_retry(client, *, model="claude-haiku-4-5", max_attempts=4, **kw):
    for attempt in range(1, max_attempts + 1):
        try:
            return client.with_options(timeout=30.0).messages.create(model=model, **kw)

        # --- non-retryable: fail fast --------------------------------------
        except anthropic.AuthenticationError:
            raise                       # 401 -- fix the key
        except anthropic.BadRequestError:
            raise                       # 400 -- fix the request
        except anthropic.NotFoundError:
            raise                       # 404 -- wrong model/endpoint

        # --- retryable: back off -----------------------------------------
        except anthropic.RateLimitError:
            reason = "429 rate_limit"
        except anthropic.APIStatusError as e:
            if e.status_code < 500:
                raise
            reason = f"{e.status_code} server"
        except anthropic.APIConnectionError as e:
            reason = e.__class__.__name__

        if attempt == max_attempts:
            raise
        delay = min(0.5 * 2 ** (attempt - 1) + random.random(), 20.0)
        print(f"  {reason}; backing off {delay:.1f}s (attempt {attempt})")
        time.sleep(delay)


if __name__ == "__main__":
    good = anthropic.Anthropic()
    r = call_with_retry(good, max_tokens=30, messages=[{"role": "user", "content": "ping"}])
    print("ok:", "".join(b.text for b in r.content if b.type == "text"))

    bad = anthropic.Anthropic(api_key="sk-ant-not-real", max_retries=0)
    try:
        call_with_retry(bad, max_tokens=30, messages=[{"role": "user", "content": "ping"}])
    except anthropic.AuthenticationError:
        print("bad key -> AuthenticationError, not retried  (correct)")
```
<!-- CODE:END -->

## Output

<!-- OUTPUT:START -->
_captured · mock run — numbers illustrative_

```text
ok: pong
bad key -> AuthenticationError, not retried  (correct)
```
<!-- OUTPUT:END -->

## Read the output

- `AuthenticationError` (401) is **not** retried — a retry can't fix a bad key.
- **529** `overloaded_error` (not 503) is Anthropic-side load — back off. 429 is *your* traffic.
- The SDK already retries 408/409/429/5xx + connection with backoff, `max_retries=2`.

## Exam hook

MR 'which are worth retrying' items; the 529-vs-503 fact; 'the SDK out of the box…'.

## Your turn

Point the bad-key client at a valid key but an unknown model id — see it raise `NotFoundError`, not retry.
