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
