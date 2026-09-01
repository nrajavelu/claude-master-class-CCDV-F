# Contract in `system`, task in `messages`

> Worked example · **Day 1–2** · exam domain **D6** · source `code-snippets/prompt_structure.py`
> Run it yourself: `python code-snippets/prompt_structure.py`

## Scenario

The same extraction task, prompted two ways: rules crammed into the user turn vs. a structured `system` contract + XML-delimited data.

**Input / dataset.** A short support ticket to extract fields from.

## The code

<!-- CODE:START -->
```python
"""
prompt_structure.py — contract in `system`, task+data in `messages`, XML tags, few-shot.

Exam angles (D6 · Prompt & Context Engineering):
  * durable instruction / role / output shape -> `system` (its own field; NO role:"system" message)
  * the changing task and data -> `messages`
  * wrap inputs in tags (<ticket>, <doc>) -> separates instruction from data (also anti-injection)
  * few-shot: one worked input->output pair beats a paragraph of rules for FORMAT
  * two prompts both correct -> exam prefers the shorter one with a concrete example

    cd aizentify-cdf-bootcamp && python code-snippets/prompt_structure.py
"""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

SYSTEM = (
    "You classify a support ticket's urgency as exactly one of: low, normal, high. "
    "Reply with only that word.\n"
    "<example>\n<ticket>My invoice PDF won't download but I can see the amounts.</ticket>\n"
    "normal\n</example>"
)

TICKET = "Production is down for all customers and money is being lost every minute."

resp = client.messages.create(
    model="claude-haiku-4-5", max_tokens=10,
    system=SYSTEM,
    messages=[{"role": "user", "content": f"<ticket>{TICKET}</ticket>"}],
)
print("urgency:", "".join(b.text for b in resp.content if b.type == "text").strip())
```
<!-- CODE:END -->

## Output

<!-- OUTPUT:START -->
_captured · mock run — numbers illustrative_

```text
urgency: [mock reply] The support desk should acknowledge the issue, state the next step, and give a timeline.
```
<!-- OUTPUT:END -->

## Read the output

- The structured version is shorter *and* more reliable — the contract lives in `system`, applied every turn.
- XML tags (`<ticket>…</ticket>`) separate instruction from data — also the first line of injection defence.
- Few-shot fixes *shape*, not correctness, and costs tokens every call.

## Exam hook

'Two prompts both correct → the exam prefers the shorter one with a concrete example.' Also the `role:"system"` message distractor.

## Your turn

Delete the XML tags and paste the ticket inline — see if field extraction gets sloppier.
