# Batch: any order, key by `custom_id`

> Worked example · **Day 5** · exam domain **D5** · source `code-snippets/batch_custom_id.py`
> Run it yourself: `python code-snippets/batch_custom_id.py`

## Scenario

Submit ~8 classification requests as one batch, poll to `ended`, then collect results into a dict keyed by `custom_id` and print them in *your* order.

**Input / dataset.** Eight short texts to classify, each with a `custom_id`.

## The code

<!-- CODE:START -->
```python
"""
batch_custom_id.py — Message Batches: hand over the pile, collect later, ANY order.

Exam angles (D2 / D5):
  * batch ~= 50% cost, for non-latency-sensitive work
  * "10,000 docs overnight, cost matters, nobody waits" -> Batch (Rule 1)
  * results come back in ANY ORDER -> key them by custom_id, NEVER by position
  * poll processing_status until "ended", then stream results

    cd aizentify-cdf-bootcamp && python code-snippets/batch_custom_id.py
"""
import time
from dotenv import load_dotenv
import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

load_dotenv()
client = anthropic.Anthropic()

TICKETS = {
    "t-101": "Production is down for everyone.",
    "t-102": "Typo on the pricing page.",
    "t-103": "Can't reset my password.",
    "t-104": "Invoice PDF won't open.",
}

batch = client.messages.batches.create(requests=[
    Request(custom_id=cid, params=MessageCreateParamsNonStreaming(
        model="claude-haiku-4-5", max_tokens=8,
        system="Classify urgency as low|normal|high. One word.",
        messages=[{"role": "user", "content": text}],
    ))
    for cid, text in TICKETS.items()
])
print("batch:", batch.id)

while True:
    b = client.messages.batches.retrieve(batch.id)
    if b.processing_status == "ended":
        break
    print("  ...", b.processing_status)
    time.sleep(5)

# results arrive in ANY order -- build a dict keyed by custom_id
out = {}
for res in client.messages.batches.results(batch.id):
    if res.result.type == "succeeded":
        text = "".join(x.text for x in res.result.message.content if x.type == "text")
        out[res.custom_id] = text.strip()

for cid in TICKETS:                       # print in OUR order, not the results' order
    print(f"{cid}: {out.get(cid, '(missing)')}")
```
<!-- CODE:END -->

## Output

<!-- OUTPUT:START -->
_captured · mock run — numbers illustrative_

```text
batch: msgbatch_mock01
t-101: [mock] t-101 -> positive
t-102: [mock] t-102 -> positive
t-103: [mock] t-103 -> positive
t-104: [mock] t-104 -> positive
```
<!-- OUTPUT:END -->

## Read the output

- Results come back in **arbitrary order** — match by `custom_id`, never by position.
- Limits: ≤ 100,000 requests or 256 MB, ≤ 24 h; ~50% cost.
- Chunking a `for` loop over the sync endpoint is **not** batching — same rate limits, same per-request cost.

## Exam hook

SCN '10,000 docs overnight, cost matters' → Batch; 'batch results are returned…' SBA.

## Your turn

Print the raw results in the order they arrive — see they're shuffled relative to submission.
