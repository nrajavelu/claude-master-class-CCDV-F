"""
Lab 2 — streaming explainer (SOLUTION).

    cd day1-foundations
    python labs/lab2_streaming/solution/stream_explainer.py labs/lab1_explainer/sample.py

Key idea: for anything long, stream. The `with ... as stream:` context manager yields text
as it is generated (no HTTP-timeout risk), and `stream.get_final_message()` hands you the
complete Message afterwards so you never assemble usage/stop_reason by hand.
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

    with client.messages.stream(
        model=MODEL,
        max_tokens=400,
        system=SYSTEM,
        messages=messages,
    ) as stream:
        for chunk in stream.text_stream:      # only the text deltas
            print(chunk, end="", flush=True)

    final = stream.get_final_message()         # full Message: content, usage, stop_reason

    print("\n\n--- call stats ---")
    print(f"stop_reason: {final.stop_reason}")
    print(
        f"usage:       input_tokens={final.usage.input_tokens}  "
        f"output_tokens={final.usage.output_tokens}"
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python .../stream_explainer.py <path-to-source-file>")
        return 2
    explain(sys.argv[1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
