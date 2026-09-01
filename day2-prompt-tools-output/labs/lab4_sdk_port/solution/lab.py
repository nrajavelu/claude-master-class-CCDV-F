"""Day 2 · Lab 4 — port lookup_order to the Agent SDK (SOLUTION).

    cd aizentify-cdf-bootcamp
    python day2-prompt-tools-output/labs/lab4_sdk_port/solution/lab.py

Same tool, same description, same call/no-call decisions as Lab 2's detailed build — the
loop is now the SDK's job, not a hand-written for-loop over messages.create.
"""
import asyncio

from claude_agent_sdk import (
    AssistantMessage, ClaudeAgentOptions, query, tool, create_sdk_mcp_server, ToolUseBlock,
)

PROMPTS = [
    "Where's my order 10231?",
    "I ordered a lamp last week and it hasn't come — order 55012.",
    "What's your return window?",
    "Can you check on my recent purchase?",
    "Order number 9 — status please.",
]

DESC = (
    "Fetch the current status, line items, and totals for ONE specific order, given its "
    "numeric order id (the integer printed in the customer's confirmation email). "
    "Use this whenever the user names or unambiguously identifies a specific order and wants "
    "its status or contents. "
    "Do NOT use it for general policy questions (returns, shipping, warranty) and do NOT "
    "guess an id — if the user refers to 'my recent order' without a number, ask them for "
    "the order id instead of calling this tool."
)


@tool("lookup_order", DESC, {"order_id": int})
async def lookup_order(args):
    return {"content": [{"type": "text", "text": f"Order {args['order_id']}: shipped, 2 items, $48.10"}]}


async def main():
    server = create_sdk_mcp_server(name="orders", version="1.0.0", tools=[lookup_order])
    opts = ClaudeAgentOptions(
        mcp_servers={"orders": server},
        allowed_tools=["mcp__orders__lookup_order"],
    )
    for p in PROMPTS:
        called = False
        async for m in query(prompt=p, options=opts):
            if isinstance(m, AssistantMessage):
                for b in m.content:
                    if isinstance(b, ToolUseBlock) and b.name == "mcp__orders__lookup_order":
                        called = True
        print(f"{'call   ' if called else 'no call'}  <- {p}")


if __name__ == "__main__":
    asyncio.run(main())
