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
