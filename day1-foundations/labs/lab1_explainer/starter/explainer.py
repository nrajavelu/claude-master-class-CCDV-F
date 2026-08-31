"""
Lab 1 — code explainer (STARTER).  Fill in every # TODO, then:

    cd day1-foundations
    python labs/lab1_explainer/starter/explainer.py labs/lab1_explainer/sample.py

Reference: ../../../day0-prework/labs/hello_claude.py for the call shape.
"""

from __future__ import annotations

import sys

from dotenv import load_dotenv

import anthropic

load_dotenv()  # reads ANTHROPIC_API_KEY from aizentify-cdf-bootcamp/.env

MODEL = "claude-haiku-4-5"  # cheap tier for training; Day 5 covers choosing models properly


def explain(path: str) -> None:
    source = open(path, "r", encoding="utf-8").read()

    client = anthropic.Anthropic()

    # TODO 1: write a system prompt. Claude's job: explain this code in plain English
    #         for a teammate who will maintain it. Ask for a short paragraph, no line-by-line.
    system = ""  # <-- replace

    # TODO 2: build the messages list. One user message. Put the file path and the
    #         source code in it. Label the code clearly (e.g. wrap it in <code> tags).
    messages = []  # <-- replace

    # TODO 3: call the Messages API. Pass model=MODEL, a sensible max_tokens (~400),
    #         system=system, messages=messages.
    response = None  # <-- replace

    # TODO 4: response.content is a LIST of blocks. Join the .text of every block
    #         whose .type == "text".
    explanation = ""  # <-- replace

    print(f"=== Explanation of {path} ===")
    print(explanation)
    print("\n--- call stats ---")
    # TODO 5: print response's model, stop_reason, and usage.input_tokens / output_tokens.


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python .../explainer.py <path-to-source-file>")
        return 2
    explain(sys.argv[1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
