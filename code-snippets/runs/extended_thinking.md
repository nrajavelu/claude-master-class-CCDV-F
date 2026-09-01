# Extended thinking on Haiku 4.5

> Worked example · **Day 5** · exam domain **D5/D2** · source `code-snippets/extended_thinking.py`
> Run it yourself: `python code-snippets/extended_thinking.py`

## Scenario

Turn on extended thinking, read the `thinking` blocks (and their signature), then stream the same request and watch the thinking block arrive before the answer.

**Input / dataset.** The same trap word-problem as the CoT page.

## The code

<!-- CODE:START -->
```python
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
```
<!-- CODE:END -->

## Output

<!-- OUTPUT:START -->
_captured · mock run — numbers illustrative_

```text
🧠 THINKING (truncated):
 Let me reason about this step by step. The key is to track where each amount actually goes rather than adding unrelated numbers… …

   signature present: True
💬 ANSWER:
 There is no missing dollar. The $27 the guests paid already includes the bellhop's $2 ($25 room + $2 kept). Adding the $2 again double-counts it; $27 - $2 = $25, or $27 + $3 returned = $30.

usage: Usage(input_tokens=420, output_tokens=96, cache_creation_input_tokens=0, cache_read_input_tokens=0)

--- streamed ---

[text] There is no missing dollar. The $27 the guests paid already includes the bellhop's $2 ($25 room + $2 kept). Adding the $2 again double-counts it; $27 - $2 = $25, or $27 + $3 returned = $30.
```
<!-- OUTPUT:END -->

## Read the output

- **Adaptive** thinking (Claude 5 — Fable/Opus/Sonnet) vs **extended** thinking (Haiku 4.5) — 'Haiku is the odd one out'.
- `budget_tokens` is deprecated / 400s on the newest generations; it still applies on the Haiku extended path.
- Thinking blocks have a `signature` — pass them back **unchanged** in multi-turn, never edit.

## Exam hook

'Adaptive vs extended thinking' and 'which models use which' SBA.

## Your turn

Remove `thinking=` entirely and re-run — see the answer arrive with no thinking block.
