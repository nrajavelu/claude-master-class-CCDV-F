# Prove the cache

> Worked example · **Day 5** · exam domain **D5** · source `code-snippets/prompt_caching.py`
> Run it yourself: `python code-snippets/prompt_caching.py`

## Scenario

Send the same large system prefix + a varying question, five times, with a `cache_control` breakpoint. Then sabotage the prefix with a timestamp and watch reads drop to zero.

**Input / dataset.** A ~12 KB fixed system prompt + five short questions.

## The code

<!-- CODE:START -->
```python
"""
prompt_caching.py — cache a stable prefix; watch a silent invalidator kill it.

Exam angles (D5 · Cost & Token Management):
  * prefix match -- any byte change in the prefix invalidates everything after it
  * render order: tools -> system -> messages; stable content BEFORE the breakpoint
  * verify with usage.cache_read_input_tokens (0 across repeats == something invalidating)
  * silent invalidators: datetime.now() in the prompt, unsorted json.dumps, varying tool set
  * cache read ~= 0.1x input price; cache write ~= 1.25x
  * caching is lever #1 in the cost-optimisation order -- before touching model choice

    cd aizentify-cdf-bootcamp && python code-snippets/prompt_caching.py
"""
import datetime
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

BIG = ("You are a policy assistant. Reference document follows.\n" + ("lorem ipsum " * 800))


def ask(question, sabotage=False):
    system = [{
        "type": "text",
        # a timestamp in the cached prefix is the classic invalidator
        "text": BIG + (f"\n(loaded {datetime.datetime.now()})" if sabotage else ""),
        "cache_control": {"type": "ephemeral"},
    }]
    r = client.messages.create(model="claude-haiku-4-5", max_tokens=40,
                               system=system, messages=[{"role": "user", "content": question}])
    u = r.usage
    return getattr(u, "cache_creation_input_tokens", 0), getattr(u, "cache_read_input_tokens", 0)


print("stable prefix:")
for i in range(3):
    w, rd = ask(f"Question {i}?")
    print(f"  call {i}: cache_write={w:5d}  cache_read={rd:5d}")

print("prefix with datetime.now() (sabotaged):")
for i in range(3):
    w, rd = ask(f"Question {i}?", sabotage=True)
    print(f"  call {i}: cache_write={w:5d}  cache_read={rd:5d}   <- reads stay 0")
```
<!-- CODE:END -->

## Output

<!-- OUTPUT:START -->
_captured · mock run — numbers illustrative_

```text
stable prefix:
  call 0: cache_write= 1180  cache_read=    0
  call 1: cache_write=    0  cache_read= 1180
  call 2: cache_write=    0  cache_read= 1180
prefix with datetime.now() (sabotaged):
  call 0: cache_write= 1180  cache_read=    0   <- reads stay 0
  call 1: cache_write= 1180  cache_read=    0   <- reads stay 0
  call 2: cache_write= 1180  cache_read=    0   <- reads stay 0
```
<!-- OUTPUT:END -->

## Read the output

- Call 1 shows `cache_creation_input_tokens`; calls 2–5 show `cache_read_input_tokens` (≈ 0.1× price).
- Render order is `tools → system → messages`; any byte change in the prefix invalidates everything after it.
- `datetime.now()` in the system prompt is the classic silent invalidator — reads go to 0.

## Exam hook

'`cache_read_input_tokens` is 0 across identical-prefix calls — why?' and the caching-first lever.

## Your turn

Move the `cache_control` breakpoint *before* the big text instead of after — watch the counters.
