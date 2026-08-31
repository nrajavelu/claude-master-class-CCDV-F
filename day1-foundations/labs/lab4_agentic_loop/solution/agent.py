"""
Lab 4 — the agentic loop, by hand (SOLUTION).

    cd day1-foundations
    python labs/lab4_agentic_loop/solution/agent.py "Is there a bug in mini_repo? Cite file and line."

Same pattern as ep01/agent.py. The whole "agent" is:
  request -> maybe run tools -> feed results back -> repeat until end_turn.
Day 3 hands this loop to the Claude Agent SDK.
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

import anthropic

load_dotenv()

MODEL = "claude-haiku-4-5"
MAX_TURNS = 8  # safety net so a misbehaving loop can't run forever / burn budget

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mini_repo"))

TOOLS = [
    {
        "name": "read_project_file",
        "description": (
            "Read the full text of one file from the project, by path relative to the "
            "project root (e.g. 'discount.py'). Use this before making any claim about "
            "what a file contains — do not guess."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path relative to the project root."}
            },
            "required": ["path"],
        },
    }
]


def read_project_file(path: str) -> str:
    # path-traversal guard: no absolute paths, no climbing out of REPO_DIR
    if os.path.isabs(path) or ".." in path.replace("\\", "/").split("/"):
        return f"Error: '{path}' is outside the project."
    full = os.path.normpath(os.path.join(REPO_DIR, path))
    if not full.startswith(REPO_DIR):
        return f"Error: '{path}' is outside the project."
    try:
        with open(full, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: no file at '{path}'."


def run_agent(question: str) -> str:
    client = anthropic.Anthropic()
    messages: list[dict] = [{"role": "user", "content": question}]

    for turn in range(1, MAX_TURNS + 1):
        response = client.messages.create(
            model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages
        )

        # Rule 1: the whole content list becomes the assistant turn.
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "tool_use":
            # Rule 2: one user message, a list of tool_result blocks, matching ids.
            results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                print(f"[tool] {block.name}(path={block.input.get('path')!r})")
                if block.name == "read_project_file":
                    output = read_project_file(block.input["path"])
                else:
                    output = f"Error: unknown tool '{block.name}'"
                results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": output}
                )
            messages.append({"role": "user", "content": results})
            continue

        if response.stop_reason == "end_turn":
            text = "".join(b.text for b in response.content if b.type == "text")
            return f"\n{text}\n\n({turn} turns, stop_reason=end_turn)"

        if response.stop_reason == "max_tokens":
            return "[stopped: hit max_tokens — raise max_tokens or narrow the question]"
        if response.stop_reason == "refusal":
            return "[stopped: Claude declined this request]"
        return f"[stopped: unexpected stop_reason={response.stop_reason}]"

    return f"[stopped: reached the {MAX_TURNS}-turn safety cap]"


def main() -> int:
    if len(sys.argv) < 2:
        print('usage: python .../agent.py "your question about mini_repo"')
        return 2
    print(run_agent(" ".join(sys.argv[1:])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
