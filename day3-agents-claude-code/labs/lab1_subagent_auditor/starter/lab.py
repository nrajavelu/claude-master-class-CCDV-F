"""Day 3 · Lab 1 — two-subagent repo auditor (STARTER). Fill every # TODO.

    cd aizentify-cdf-bootcamp
    python day3-agents-claude-code/labs/lab1_subagent_auditor/starter/lab.py

Reference: ep05/agent.py, ep05/subagents.py
Goal: a coordinator that DELEGATES to two scoped subagents and aggregates — it must not
hold the file-reading tools itself.
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
        # TODO: prompt="Read every .py file in mini_repo/. For each function, report whether "
        #              "it has a docstring and whether it explains args + return. Be terse.",
        # TODO: tools=["mcp__fs__read_file", "mcp__fs__list_files"],
        # TODO: model="claude-haiku-4-5",
        prompt="TODO",
    ),
    "security-reviewer": AgentDefinition(
        description="Flags obvious security risks in Python files.",
        # TODO: prompt="Read every .py file in mini_repo/. Flag hardcoded secrets, shell=True, "
        #              "eval/exec, and unvalidated input. Cite file + line. Be terse.",
        # TODO: tools=["mcp__fs__read_file", "mcp__fs__list_files"],
        # TODO: model="claude-haiku-4-5",
        prompt="TODO",
    ),
}


async def main():
    fs = create_sdk_mcp_server(name="fs", version="1.0.0", tools=[read_file, list_files])
    opts = ClaudeAgentOptions(
        mcp_servers={"fs": fs},
        agents=REVIEW_AGENTS,
        # TODO: the coordinator gets the delegation tool ONLY — NOT the fs tools.
        #       allowed_tools=["Task"],
        allowed_tools=["Task", "mcp__fs__read_file", "mcp__fs__list_files"],  # <-- wrong on purpose
    )
    prompt = (
        "Delegate a docstring review to docstring-reviewer and a security review to "
        "security-reviewer. Wait for both. Then print one combined SUMMARY with a "
        "'Docstrings:' line and a 'Security:' line."
    )
    async for m in query(prompt=prompt, options=opts):
        if isinstance(m, AssistantMessage):
            for b in m.content:
                if isinstance(b, TextBlock):
                    print(b.text)
        elif isinstance(m, ResultMessage):
            print("---\nnum_turns:", m.num_turns)


if __name__ == "__main__":
    asyncio.run(main())
