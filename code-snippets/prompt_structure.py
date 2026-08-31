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
