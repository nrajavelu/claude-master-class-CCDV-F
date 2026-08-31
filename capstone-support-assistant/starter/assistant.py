"""
assistant.py — the capstone support assistant (STARTER). Fill every # TODO.

Build order (the 4-week plan, see ../README.md):
  W1: TODO 1-4  — the plain ReAct loop + reading stop_reason + a per-call timeout
  W2: TODO 5-6  — cost tracking + the budget stop
  W3: TODO 7-8  — the issue_refund guardrail (code decides) + untrusted-note handling
The reference is ../assistant.py — build it yourself first.

    cd aizentify-cdf-bootcamp
    python capstone-support-assistant/starter/assistant.py "Where is order A-1002? If it's lost, refund it."
"""
from __future__ import annotations

import sys
import tomllib
from pathlib import Path

from dotenv import load_dotenv

import anthropic

# tools.py is one level up
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools import TOOLS, issue_refund, lookup_order   # noqa: E402

HERE = Path(__file__).resolve().parent.parent
load_dotenv(HERE.parent / ".env")

CFG = tomllib.loads((HERE / "config.toml").read_text())
MODEL = CFG["model"]["id"]
BUDGET_USD = CFG["budget"]["usd"]
MAX_TURNS = CFG["limits"]["max_turns"]
PRICE = {k: tuple(v) for k, v in CFG["prices"].items()}
SYSTEM = (HERE / "system_prompt.txt").read_text()


def run_tool(name: str, args: dict) -> str:
    if name == "lookup_order":
        return lookup_order(args["order_id"])
    if name == "issue_refund":
        # TODO 7: the GUARDRAIL. Before calling issue_refund(), in code:
        #   - look the order up; if the note matches an injection pattern -> BLOCK
        #   - if amount_usd != the looked-up total -> BLOCK
        #   - if amount_usd > CFG["refund"]["auto_approve_max_usd"] -> BLOCK (escalate)
        # Only if all pass: return issue_refund(args["order_id"], float(args["amount_usd"]))
        return "TODO: guardrail not implemented"
    return f"Error: unknown tool '{name}'"


def run(question: str) -> str:
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]
    spent = 0.0

    for turn in range(1, MAX_TURNS + 1):
        # TODO 5: if spent >= BUDGET_USD: return a clear "budget reached" message

        # TODO 1: call the API — model=MODEL, max_tokens=600, system=SYSTEM, tools=TOOLS,
        #         messages=messages. TODO 4: wrap with client.with_options(timeout=...).
        r = None  # <-- replace

        # TODO 6: spent += cost from r.usage using PRICE[MODEL] (in, out) / 1e6

        # TODO 2: append the assistant turn: {"role":"assistant","content": r.content}

        # TODO 3: branch on r.stop_reason:
        #   "tool_use"  -> run each tool_use block, append ONE user message of tool_result
        #                  blocks (ids matching), then continue
        #   "end_turn"  -> return the joined text + a "[turns · $spent]" line
        #   "max_tokens"/"refusal"/else -> return a clear marker
        raise NotImplementedError("finish the loop")

    return f"[stopped: hit the {MAX_TURNS}-turn cap]"


def main() -> int:
    if len(sys.argv) < 2:
        print('usage: python assistant.py "your question"')
        return 2
    print(run(" ".join(sys.argv[1:])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
