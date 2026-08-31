"""
Lab 4 — the agentic loop, by hand (STARTER).

    cd day1-foundations
    python labs/lab4_agentic_loop/starter/agent.py "Is there a bug in mini_repo? Cite file and line."

Read ep01/agent.py in the parent repo alongside this. Build it yourself; don't paste.
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

import anthropic

load_dotenv()

MODEL = "claude-haiku-4-5"

# mini_repo lives next to the starter/ folder: .../lab4_agentic_loop/mini_repo
REPO_DIR = os.path.join(os.path.dirname(__file__), "..", "mini_repo")

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
    # TODO A: reject absolute paths and any path containing '..'. Return an error string.
    # TODO B: join REPO_DIR + path, read and return the text. On FileNotFoundError,
    #         return "Error: no file at '<path>'".
    ...


def run_agent(question: str) -> str:
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]

    while True:
        response = client.messages.create(
            model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages
        )

        # TODO 1: append the assistant turn: {"role": "assistant", "content": response.content}

        # TODO 2: if response.stop_reason == "tool_use":
        #   build a list `results`. For each block in response.content with block.type == "tool_use":
        #     print(f"[tool] {block.name}(path={block.input.get('path')!r})")
        #     run the tool -> text
        #     results.append({"type": "tool_result", "tool_use_id": block.id, "content": text})
        #   append {"role": "user", "content": results}
        #   continue

        # TODO 3: if response.stop_reason == "end_turn":
        #   return the joined text of the text blocks

        # TODO 4: any other stop_reason ("max_tokens", "refusal", ...) -> return a marker string
        raise NotImplementedError("finish the loop")


def main() -> int:
    if len(sys.argv) < 2:
        print('usage: python .../agent.py "your question about mini_repo"')
        return 2
    print(run_agent(" ".join(sys.argv[1:])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
