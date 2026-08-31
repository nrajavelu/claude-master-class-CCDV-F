"""
retry_chain.py — catch a CHAIN, most-specific first. Retry vs fail-fast.

Exam angles (D4 · Eval, Testing & Debugging):
  * RETRY (transient): RateLimitError 429 · APIStatusError >=500 · APIConnectionError
  * FAIL FAST (yours): BadRequestError 400 · AuthenticationError 401 ·
                       PermissionDeniedError 403 · NotFoundError 404
  * a single `except Exception` throws the distinction away
  * the SDK already retries 408/409/429/5xx + connection, max_retries=2 (default)
  * `overloaded` = their load; `rate_limit` = your spike (yours to fix)
  * `refusal` is NOT an exception -- it's a stop_reason

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
