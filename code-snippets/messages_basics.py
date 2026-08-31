"""
messages_basics.py — the shape of one Messages API call.

Exam angles (D2 · Applications & Integration, Claude API Mechanics):
  * request = model + max_tokens (both required) + system (own field) + messages
  * response.content is a LIST of typed blocks — check block.type
  * response.stop_reason tells you WHY it stopped — you branch on this
  * response.usage is your bill — free to read, check it every call
  * you send dicts, you get back objects (dot access)

    cd aizentify-cdf-bootcamp && python code-snippets/messages_basics.py
"""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

resp = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=120,
    system="You answer in one short sentence.",           # its own top-level field
    messages=[{"role": "user", "content": "Name three primary colours."}],
)

# content is a list — filter on type, never assume content[0] is text
text = "".join(b.text for b in resp.content if b.type == "text")

print("text        :", text)
print("block types :", [b.type for b in resp.content])
print("stop_reason :", resp.stop_reason)                  # 'end_turn' here
print("usage       :", f"in={resp.usage.input_tokens} out={resp.usage.output_tokens}")

# Try it: set max_tokens=5 above and re-run -> stop_reason becomes 'max_tokens'
# Try it: messages=[{"role":"assistant","content":"hi"}] -> HTTP 400 (first must be user)
