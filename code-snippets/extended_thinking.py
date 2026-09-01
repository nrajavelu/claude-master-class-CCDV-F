"""
extended_thinking.py — turn on thinking, read the thinking blocks, stream them.

Adapted from the Anthropic Claude Cookbooks (MIT):
  extended_thinking/extended_thinking.ipynb · https://github.com/anthropics/claude-cookbooks

Exam angles (D5 · Model Selection · D2 API Mechanics):
  * ADAPTIVE thinking (Claude 5 — Fable/Opus/Sonnet): model chooses depth; you steer it
    with `output_config.effort` = low|medium|high|xhigh|max.
  * EXTENDED thinking (Haiku 4.5): explicit `thinking={"type":"enabled"}`, and the reply
    carries `thinking` blocks before the `text` block. "Haiku 4.5 is the odd one out."
  * `budget_tokens` is deprecated / 400s on the newest generations — this file uses the
    Haiku extended-thinking path where it still applies.
  * thinking blocks have a `signature`; pass them back UNCHANGED in multi-turn — never edit.
  * in a stream, thinking arrives as its own content block before the answer.

    cd aizentify-cdf-bootcamp && python code-snippets/extended_thinking.py
"""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"  # extended thinking lives here; Claude 5 models use adaptive

PUZZLE = ("Three guests pay $30 for a room that costs $25. The clerk sends $5 back via a "
          "bellhop who keeps $2 and returns $1 to each guest. Now each paid $9 (=$27), plus "
          "the bellhop's $2 is $29. Where is the missing dollar?")


def once():
    r = client.messages.create(
        model=MODEL, max_tokens=2000,
        thinking={"type": "enabled", "budget_tokens": 1500},
        messages=[{"role": "user", "content": PUZZLE}],
    )
    for b in r.content:
        if b.type == "thinking":
            print("🧠 THINKING (truncated):\n", b.thinking[:600], "…\n")
            print("   signature present:", bool(getattr(b, "signature", None)))
        elif b.type == "text":
            print("💬 ANSWER:\n", b.text)
    print("\nusage:", r.usage)


def streamed():
    print("\n--- streamed ---")
    with client.messages.stream(
        model=MODEL, max_tokens=2000,
        thinking={"type": "enabled", "budget_tokens": 1500},
        messages=[{"role": "user", "content": PUZZLE}],
    ) as stream:
        block = None
        for ev in stream:
            if ev.type == "content_block_start":
                block = ev.content_block.type
                print(f"\n[{block}] ", end="")
            elif ev.type == "content_block_delta":
                d = ev.delta
                print(getattr(d, "thinking", "") or getattr(d, "text", ""), end="", flush=True)
        print()


if __name__ == "__main__":
    once()
    streamed()
