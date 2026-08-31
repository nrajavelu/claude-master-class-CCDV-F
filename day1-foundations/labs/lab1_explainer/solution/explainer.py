"""
Lab 1 — code explainer (SOLUTION).

    cd day1-foundations
    python labs/lab1_explainer/solution/explainer.py labs/lab1_explainer/sample.py

Demonstrates the four things every Messages API call has:
  model + max_tokens  ·  system  ·  messages  ·  a response you read block-by-block.
"""

from __future__ import annotations

import sys

from dotenv import load_dotenv

import anthropic

load_dotenv()

MODEL = "claude-haiku-4-5"  # cheap tier for training; Day 5 covers choosing models properly

SYSTEM = (
    "You explain source code to a developer who will have to maintain it. "
    "Give one tight paragraph: what the file is for, what each public function does, "
    "and any behaviour a caller might not expect. No line-by-line walkthrough, no "
    "restating the code, no praise."
)


def explain(path: str) -> None:
    source = open(path, "r", encoding="utf-8").read()

    client = anthropic.Anthropic()

    messages = [
        {
            "role": "user",
            "content": (
                f"File: {path}\n\n"
                f"<code>\n{source}\n</code>\n\n"
                "Explain this file."
            ),
        }
    ]

    response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        system=SYSTEM,
        messages=messages,
    )

    # response.content is a list of blocks (TextBlock, ThinkingBlock, ToolUseBlock, ...).
    # For a plain answer we want the text blocks, concatenated.
    explanation = "".join(b.text for b in response.content if b.type == "text")

    print(f"=== Explanation of {path} ===")
    print(explanation)
    print("\n--- call stats ---")
    print(f"model:       {response.model}")
    print(f"stop_reason: {response.stop_reason}")
    print(
        f"usage:       input_tokens={response.usage.input_tokens}  "
        f"output_tokens={response.usage.output_tokens}"
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python .../explainer.py <path-to-source-file>")
        return 2
    explain(sys.argv[1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
