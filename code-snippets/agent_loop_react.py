"""
agent_loop_react.py — the ReAct loop by hand: Thought -> Action -> Observation.

Exam angles (D1 · Agents & Workflows):
  * ReAct = CoT interleaved with tool calls across a LOOP (not one call)
  * Rule 1: after every response append {"role":"assistant","content": r.content}
  * Rule 2: on tool_use -> ONE user message, a list of tool_result blocks, ids matching
  * the MODEL emits tool_use; YOUR CODE runs the tool (the model never executes it)
  * loop until stop_reason == "end_turn"; cap the turns

    cd aizentify-cdf-bootcamp && python code-snippets/agent_loop_react.py
"""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

FILES = {
    "discount.py": (
        "def apply_discount(price, percent):\n"
        "    if percent < 0 or percent > 1:\n"
        "        raise ValueError('percent must be between 0 and 1')\n"
        "    if percent > 1:\n"
        "        return 0.0\n"
        "    return round(price * (1 - percent), 2)\n"
    ),
}

TOOLS = [{
    "name": "read_file",
    "description": "Read one file's full text by name. Use before making any claim about it.",
    "input_schema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]},
}]


def run_tool(name, args):
    if name == "read_file":
        return FILES.get(args["name"], f"Error: no file '{args['name']}'")
    return f"Error: unknown tool '{name}'"


def react(question, max_turns=6):
    messages = [{"role": "user", "content": question}]
    for turn in range(1, max_turns + 1):
        r = client.messages.create(model="claude-haiku-4-5", max_tokens=1024,
                                   tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": r.content})     # Rule 1

        # print the "Thought" (leading text) + "Action" (tool_use) for this turn
        for b in r.content:
            if b.type == "text" and b.text.strip():
                print(f"[turn {turn}] Thought: {b.text.strip()[:140]}")
            if b.type == "tool_use":
                print(f"[turn {turn}] Action : {b.name}({b.input})")

        if r.stop_reason == "tool_use":
            results = []
            for b in r.content:
                if b.type == "tool_use":
                    obs = run_tool(b.name, b.input)                      # Observation
                    print(f"[turn {turn}] Observ.: {obs.splitlines()[0][:80]} ...")
                    results.append({"type": "tool_result", "tool_use_id": b.id, "content": obs})
            messages.append({"role": "user", "content": results})        # Rule 2
            continue                                                     # -> next Thought

        if r.stop_reason == "end_turn":
            return "".join(b.text for b in r.content if b.type == "text")
        return f"[stopped: {r.stop_reason}]"
    return "[stopped: turn cap]"


if __name__ == "__main__":
    print("\nANSWER:", react("Is there a bug in discount.py? Cite the line."))
