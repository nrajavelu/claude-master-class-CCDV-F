"""
Lab 2 — streaming explainer (STARTER).

    cd day1-foundations
    python labs/lab2_streaming/starter/stream_explainer.py labs/lab1_explainer/sample.py
"""

from __future__ import annotations

import sys

from dotenv import load_dotenv

import anthropic

load_dotenv()

MODEL = "claude-haiku-4-5"

SYSTEM = (
    "You explain source code to a developer who will maintain it. One tight paragraph: "
    "what the file is for, what each public function does, and any surprising behaviour."
)


def explain(path: str) -> None:
    source = open(path, "r", encoding="utf-8").read()
    client = anthropic.Anthropic()

    messages = [
        {"role": "user", "content": f"File: {path}\n\n<code>\n{source}\n</code>\n\nExplain this file."}
    ]

    print(f"=== Explanation of {path} ===")

    # TODO 1: open a streaming call:
    #   with client.messages.stream(model=MODEL, max_tokens=400, system=SYSTEM,
    #                               messages=messages) as stream:
    #       for chunk in stream.text_stream:
    #           print(chunk, end="", flush=True)
    #
    # TODO 2: after the with-block, get the finished message and print its stats:
    #   final = stream.get_final_message()
    #   print stop_reason and usage.input_tokens / usage.output_tokens

    print("\n\n--- call stats ---")
    # TODO 3: print stop_reason + usage from the final message


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python .../stream_explainer.py <path-to-source-file>")
        return 2
    explain(sys.argv[1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
