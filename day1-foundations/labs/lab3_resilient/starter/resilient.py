"""
Lab 3 — resilient call (STARTER).

    cd day1-foundations
    python labs/lab3_resilient/starter/resilient.py labs/lab1_explainer/sample.py
    python labs/lab3_resilient/starter/resilient.py labs/lab1_explainer/sample.py --break-key
"""

from __future__ import annotations

import random
import sys
import time

from dotenv import load_dotenv

import anthropic

load_dotenv()

MODEL = "claude-haiku-4-5"

# USD per 1,000,000 tokens  (input, output).  Source: Anthropic pricing, Haiku 4.5 tier.
PRICES = {"claude-haiku-4-5": (1.00, 5.00), "claude-sonnet-5": (3.00, 15.00)}

SYSTEM = "You explain source code to a developer who will maintain it. One tight paragraph."


def estimate_input_cost(client, messages) -> None:
    # TODO 1: call client.messages.count_tokens(model=MODEL, system=SYSTEM, messages=messages)
    #         then print "~N input tokens  ≈ $X.XXXXXX in" using PRICES[MODEL][0] / 1e6.
    ...


def call_with_retry(client, messages, max_attempts: int = 4):
    """Return a Message, retrying transient failures with exponential backoff.
    Re-raise immediately on non-retryable errors (bad request / auth / not found)."""
    for attempt in range(1, max_attempts + 1):
        print(f"[attempt {attempt}] calling {MODEL} ...")
        try:
            # TODO 2: make the call with a per-request timeout, e.g.:
            #   return client.with_options(timeout=30.0).messages.create(
            #       model=MODEL, max_tokens=400, system=SYSTEM, messages=messages)
            ...
        # TODO 3: add except clauses, MOST SPECIFIC FIRST:
        #   anthropic.AuthenticationError -> print FATAL, raise (do NOT retry)
        #   anthropic.BadRequestError     -> print FATAL, raise
        #   anthropic.NotFoundError       -> print FATAL, raise
        #   anthropic.RateLimitError      -> retryable
        #   anthropic.APIStatusError as e -> retryable only if e.status_code >= 500, else raise
        #   anthropic.APIConnectionError  -> retryable
        # For the retryable ones: if attempt == max_attempts, raise; else sleep
        #   delay = min(0.5 * 2**(attempt-1) + random.random(), 20)  and continue.
        except Exception:  # replace this
            raise


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    break_key = "--break-key" in sys.argv
    if len(args) != 1:
        print("usage: python .../resilient.py <source-file> [--break-key]")
        return 2

    source = open(args[0], "r", encoding="utf-8").read()
    messages = [{"role": "user", "content": f"<code>\n{source}\n</code>\n\nExplain this file."}]

    client = anthropic.Anthropic(api_key="sk-ant-not-a-real-key") if break_key else anthropic.Anthropic()

    estimate_input_cost(client, messages)

    try:
        resp = call_with_retry(client, messages)
    except anthropic.APIError as e:
        print(f"\ngave up: {e.__class__.__name__}")
        return 1

    print("ok.\n")
    text = "".join(b.text for b in resp.content if b.type == "text")
    print(text)

    # TODO 4: print actual cost from resp.usage and PRICES[MODEL].
    return 0


if __name__ == "__main__":
    sys.exit(main())
