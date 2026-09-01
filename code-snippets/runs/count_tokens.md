# Count before you spend

> Worked example · **Day 1** · exam domain **D5** · source `code-snippets/count_tokens.py`
> Run it yourself: `python code-snippets/count_tokens.py`

## Scenario

`count_tokens` on a prompt, then a back-of-envelope cost from token counts × price.

**Input / dataset.** A system prompt + a user question + a tool definition.

## The code

<!-- CODE:START -->
```python
"""
count_tokens.py — predict spend before you send.

Exam angles (D5 · Model Selection & Optimisation, Cost & Token Management):
  * count_tokens takes model / system / messages / tools -- NOT max_tokens, NOT temperature
  * it's a separate, cheap endpoint
  * cost = tokens * (price_per_million / 1_000_000); output is dearer than input
  * `input_tokens` includes tool schemas + system + history -- "not your input"
  * cache_read_input_tokens ~= 0.1x input price; a cache write ~= 1.25x

    cd aizentify-cdf-bootcamp && python code-snippets/count_tokens.py
"""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

MODEL = "claude-haiku-4-5"
PRICE = {"claude-haiku-4-5": (1.00, 5.00), "claude-sonnet-5": (3.00, 15.00)}  # $/Mtok (in, out)

system = "You review Python for a teammate who will maintain it."
messages = [{"role": "user", "content": "<code>\n" + open("code-snippets/count_tokens.py").read() + "\n</code>\nExplain it."}]

counted = client.messages.count_tokens(model=MODEL, system=system, messages=messages)
in_price = PRICE[MODEL][0] / 1_000_000
print(f"input tokens : {counted.input_tokens}")
print(f"est. input $ : {counted.input_tokens * in_price:.6f}")

resp = client.messages.create(model=MODEL, max_tokens=200, system=system, messages=messages)
i, o = resp.usage.input_tokens, resp.usage.output_tokens
ci, co = i * PRICE[MODEL][0] / 1e6, o * PRICE[MODEL][1] / 1e6
print(f"actual       : in={i} (${ci:.6f}) + out={o} (${co:.6f}) = ${ci + co:.6f}")
```
<!-- CODE:END -->

## Output

<!-- OUTPUT:START -->
_captured · mock run — numbers illustrative_

```text
input tokens : 444
est. input $ : 0.000444
actual       : in=420 ($0.000420) + out=96 ($0.000480) = $0.000900
```
<!-- OUTPUT:END -->

## Read the output

- `count_tokens` accepts `model` / `system` / `messages` / `tools` — **no** `max_tokens` or sampling params.
- `input_tokens` is not 'your text' — it includes the system prompt and every tool schema.
- Judge **cost per completed task**, not per request.

## Exam hook

'`count_tokens` accepts…' SBA; cost-lever ordering items.

## Your turn

Add a second tool definition and re-count — see the input tokens jump before you've sent anything.
