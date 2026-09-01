"""Day 2 · Lab 4 — port lookup_order to the Agent SDK (STARTER). Fill every # TODO.

    cd aizentify-cdf-bootcamp
    python day2-prompt-tools-output/labs/lab4_sdk_port/starter/lab.py

Reference: ep03/agent.py · your Lab 2 DESC_DETAILED
"""
import asyncio

from claude_agent_sdk import (
    AssistantMessage, ClaudeAgentOptions, ResultMessage, TextBlock, ToolUseBlock,
    create_sdk_mcp_server, query, tool,
)

PROMPTS = [
    "Where's my order 10231?",
    "I ordered a lamp last week and it hasn't come — order 55012.",
    "What's your return window?",
    "Can you check on my recent purchase?",
    "Order number 9 — status please.",
]

# TODO: paste DESC_DETAILED from lab2_tool_description
DESC = "TODO"


@tool("lookup_order", DESC, {"order_id": int})
async def lookup_order(args):
    return {"content": [{"type": "text", "text": f"Order {args['order_id']}: shipped, 2 items, $48.10"}]}


async def main():
    server = create_sdk_mcp_server(name="orders", version="1.0.0", tools=[lookup_order])
    opts = ClaudeAgentOptions(
        mcp_servers={"orders": server},
        # TODO: allowed_tools=["mcp__orders__lookup_order"],
        allowed_tools=[],
    )
    for p in PROMPTS:
        called = False
        async for m in query(prompt=p, options=opts):
            if isinstance(m, AssistantMessage):
                for b in m.content:
                    if isinstance(b, ToolUseBlock) and b.name == "mcp__orders__lookup_order":
                        called = True
        print(f"{'call ' if called else 'no call'}  <- {p}")


if __name__ == "__main__":
    asyncio.run(main())
