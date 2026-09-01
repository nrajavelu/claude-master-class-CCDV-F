"""Day 2 · Lab 2 — the description IS the interface (STARTER). Fill the two # TODO strings.

    cd aizentify-cdf-bootcamp
    python day2-prompt-tools-output/labs/lab2_tool_description/starter/lab.py

Reference: code-snippets/strict_tool.py, ep03/tools.py
"""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"  # pinned for classroom cost — Day 5 covers model selection

PROMPTS = [
    ("order 10231", "Where's my order 10231?"),
    ("order 55012", "I ordered a lamp last week and it hasn't come — order 55012."),
    ("return window", "What's your return window?"),
    ("recent purchase", "Can you check on my recent purchase?"),
    ("order 9", "Order number 9 — status please."),
]

# TODO: a genuinely terse description
DESC_VAGUE = "TODO"

# TODO: what it returns · WHEN to use it · WHEN NOT to · what order_id means
DESC_DETAILED = "TODO"


def run(description: str):
    """Return a list of (label, called: bool, order_id) for each prompt under `description`."""
    tool = {
        "name": "lookup_order",
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "integer"}},
            "required": ["order_id"],
        },
    }
    out = []
    for label, text in PROMPTS:
        msg = client.messages.create(
            model=MODEL, max_tokens=300, tools=[tool],
            messages=[{"role": "user", "content": text}],
        )
        call = next((b for b in msg.content if b.type == "tool_use" and b.name == "lookup_order"), None)
        out.append((label, call is not None, call.input.get("order_id") if call else None))
    return out


def main():
    vague, detailed = run(DESC_VAGUE), run(DESC_DETAILED)
    want_call = {"order 10231", "order 55012", "order 9"}
    print(f"{'':22}{'VAGUE':<18}{'DETAILED'}")
    v_score = d_score = 0
    for (label, vc, vid), (_, dc, did) in zip(vague, detailed):
        expect = label in want_call
        v_ok, d_ok = (vc == expect), (dc == expect)
        v_score += v_ok; d_score += d_ok
        print(f"{label:22}{f'call({vid})' if vc else 'no call':<12}{'ok' if v_ok else 'X':<6}"
              f"{f'call({did})' if dc else 'no call':<12}{'ok' if d_ok else 'X'}")
    print(f"\nDETAILED: {d_score}/5   VAGUE: {v_score}/5")


if __name__ == "__main__":
    main()
