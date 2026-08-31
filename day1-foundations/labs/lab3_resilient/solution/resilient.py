"""
Lab 3 — resilient call (SOLUTION).

    cd day1-foundations
    python labs/lab3_resilient/solution/resilient.py labs/lab1_explainer/sample.py
    python labs/lab3_resilient/solution/resilient.py labs/lab1_explainer/sample.py --break-key

What it shows:
  * count_tokens BEFORE the call -> predicted input cost
  * a retry loop that backs off on 429 / 5xx / connection errors
    but FAILS FAST on 400 / 401 / 404 (retrying those never helps)
  * a per-request timeout via client.with_options(timeout=...)
  * real cost AFTER the call from response.usage
"""

from __future__ import annotations

import random
import sys
import time

from dotenv import load_dotenv

import anthropic

load_dotenv()

MODEL = "claude-haiku-4-5"

# USD per 1,000,000 tokens (input, output). Anthropic pricing, Haiku 4.5 / Sonnet 5 tiers.
PRICES = {"claude-haiku-4-5": (1.00, 5.00), "claude-sonnet-5": (3.00, 15.00)}

SYSTEM = "You explain source code to a developer who will maintain it. One tight paragraph."


def estimate_input_cost(client: anthropic.Anthropic, messages: list) -> None:
    # count_tokens takes only model / system / messages (and tools if you use them).
    counted = client.messages.count_tokens(model=MODEL, system=SYSTEM, messages=messages)
    in_price = PRICES[MODEL][0] / 1_000_000
    print(
        f"estimate: ~{counted.input_tokens} input tokens  "
        f"≈ ${counted.input_tokens * in_price:.6f} in  "
        f"(@ ${PRICES[MODEL][0]:.2f}/Mtok in)"
    )


def call_with_retry(
    client: anthropic.Anthropic, messages: list, max_attempts: int = 4
) -> anthropic.types.Message:
    for attempt in range(1, max_attempts + 1):
        print(f"[attempt {attempt}] calling {MODEL} ...")
        try:
            return client.with_options(timeout=30.0).messages.create(
                model=MODEL,
                max_tokens=400,
                system=SYSTEM,
                messages=messages,
            )

        # --- non-retryable: fail fast -------------------------------------------------
        except anthropic.AuthenticationError:
            print("FATAL: authentication failed (401) — bad or missing API key. Not retrying.")
            raise
        except anthropic.BadRequestError as e:
            print(f"FATAL: bad request (400) — {e.message}. Not retrying.")
            raise
        except anthropic.NotFoundError:
            print(f"FATAL: model/endpoint not found (404) — check MODEL={MODEL!r}. Not retrying.")
            raise

        # --- retryable: back off and try again --------------------------------------
        except anthropic.RateLimitError:
            reason = "rate limited (429)"
        except anthropic.APIStatusError as e:
            if e.status_code < 500:
                print(f"FATAL: API error {e.status_code} — {e.message}. Not retrying.")
                raise
            reason = f"server error ({e.status_code})"
        except anthropic.APIConnectionError as e:
            reason = f"connection error ({e.__class__.__name__})"

        if attempt == max_attempts:
            print(f"{reason}; out of attempts.")
            raise
        delay = min(0.5 * 2 ** (attempt - 1) + random.random(), 20.0)
        print(f"  {reason}; backing off {delay:.1f}s")
        time.sleep(delay)

    raise RuntimeError("unreachable")


def main() -> int:
    raw = sys.argv[1:]
    break_key = "--break-key" in raw
    args = [a for a in raw if not a.startswith("--")]
    if len(args) != 1:
        print("usage: python .../resilient.py <source-file> [--break-key]")
        return 2

    source = open(args[0], "r", encoding="utf-8").read()
    messages = [{"role": "user", "content": f"<code>\n{source}\n</code>\n\nExplain this file."}]

    client = (
        anthropic.Anthropic(api_key="sk-ant-deliberately-invalid", max_retries=0)
        if break_key
        else anthropic.Anthropic()
    )

    estimate_input_cost(client, messages)

    try:
        resp = call_with_retry(client, messages)
    except anthropic.APIError as e:
        print(f"\ngave up: {e.__class__.__name__}")
        return 1

    print("ok.\n")
    print("".join(b.text for b in resp.content if b.type == "text"))

    in_p, out_p = (p / 1_000_000 for p in PRICES[MODEL])
    ci = resp.usage.input_tokens * in_p
    co = resp.usage.output_tokens * out_p
    print(
        f"\nactual cost: in={resp.usage.input_tokens} (${ci:.6f}) + "
        f"out={resp.usage.output_tokens} (${co:.6f}) = ${ci + co:.6f}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
