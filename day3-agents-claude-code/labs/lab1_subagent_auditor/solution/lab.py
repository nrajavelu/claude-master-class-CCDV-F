"""Day 3 · Lab 1 — two-subagent repo auditor (SOLUTION).

    cd aizentify-cdf-bootcamp
    python day3-agents-claude-code/labs/lab1_subagent_auditor/solution/lab.py

The coordinator holds ONLY the delegation tool ("Task"). It cannot read files itself, so it
is structurally forced to delegate to the two scoped subagents and then aggregate.
"""
import asyncio
import pathlib

from claude_agent_sdk import (
    AgentDefinition, AssistantMessage, ClaudeAgentOptions, ResultMessage, TextBlock,
    create_sdk_mcp_server, query, tool,
)

REPO = pathlib.Path(__file__).parent.parent / "mini_repo"


@tool("read_file", "Read a UTF-8 text file under mini_repo/. Arg: path (relative).", {"path": str})
async def read_file(args):
    p = (REPO / args["path"]).resolve()
    if REPO.resolve() not in p.parents and p != REPO.resolve():
        return {"content": [{"type": "text", "text": "ERROR: outside mini_repo/"}]}
    return {"content": [{"type": "text", "text": p.read_text(encoding="utf-8")}]}


@tool("list_files", "List the files in mini_repo/.", {})
async def list_files(args):
    names = "\n".join(sorted(f.name for f in REPO.glob("*.py")))
    return {"content": [{"type": "text", "text": names}]}


REVIEW_AGENTS = {
    "docstring-reviewer": AgentDefinition(
        description="Reviews Python files for missing or weak docstrings.",
        prompt=(
            "Read every .py file in mini_repo/ with list_files then read_file. For each "
            "top-level function, state whether it has a docstring and whether the docstring "
            "explains its arguments and return value. Terse bullet list. No fixes."
        ),
        tools=["mcp__fs__read_file", "mcp__fs__list_files"],
        model="claude-haiku-4-5",
    ),
    "security-reviewer": AgentDefinition(
        description="Flags obvious security risks in Python files.",
        prompt=(
            "Read every .py file in mini_repo/. Flag hardcoded secrets/API keys, shell=True, "
            "eval/exec, and unvalidated external input. Cite file and line number. Terse "
            "bullet list. No fixes."
        ),
        tools=["mcp__fs__read_file", "mcp__fs__list_files"],
        model="claude-haiku-4-5",
    ),
}


async def main():
    fs = create_sdk_mcp_server(name="fs", version="1.0.0", tools=[read_file, list_files])
    opts = ClaudeAgentOptions(
        mcp_servers={"fs": fs},
        agents=REVIEW_AGENTS,
        allowed_tools=["Task"],  # <-- the point: coordinator cannot touch the fs tools
    )
    prompt = (
        "Delegate a docstring review to docstring-reviewer and a security review to "
        "security-reviewer. Wait for both. Then print one combined SUMMARY with a "
        "'Docstrings:' line and a 'Security:' line, each citing the file(s) involved."
    )
    async for m in query(prompt=prompt, options=opts):
        if isinstance(m, AssistantMessage):
            for b in m.content:
                if isinstance(b, TextBlock):
                    print(b.text)
        elif isinstance(m, ResultMessage):
            print("---\nnum_turns:", m.num_turns, "· usd:", round(m.total_cost_usd or 0, 4))


if __name__ == "__main__":
    asyncio.run(main())
