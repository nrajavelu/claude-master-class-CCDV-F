"""
Day 0 — your first Claude API call.

    python day0-prework/labs/hello_claude.py

If this prints a sentence from Claude and a `usage:` line, your environment is ready.
This is the smallest possible Messages API call: one model, one user message, one response.
Day 1 unpacks every part of it.
"""

from __future__ import annotations

import sys

from dotenv import load_dotenv

import anthropic

# Reads ANTHROPIC_API_KEY from aizentify-cdf-bootcamp/.env (or your shell environment).
load_dotenv()


def main() -> int:
    # Anthropic() with no arguments picks up ANTHROPIC_API_KEY from the environment.
    client = anthropic.Anthropic()

    try:
        response = client.messages.create(
            model="claude-haiku-4-5",  # cheapest tier — fine for a hello
            max_tokens=60,
            system="You are greeting a developer on their first day of a Claude course. One friendly sentence.",
            messages=[
                {"role": "user", "content": "Say hello and tell me one thing I'll be able to build by Friday."}
            ],
        )
    except anthropic.AuthenticationError:
        print("Auth failed (401). Check ANTHROPIC_API_KEY in your .env and that the workspace has credit.")
        return 1
    except anthropic.APIConnectionError as e:
        print(f"Could not reach the API ({e.__class__.__name__}). Corporate proxy/firewall? See logistics/01.")
        return 1

    # response.content is a LIST of blocks. For a plain text reply, block 0 is a text block.
    text = "".join(block.text for block in response.content if block.type == "text")
    print(f"\nClaude: {text}\n")

    u = response.usage
    print(f"usage: input_tokens={u.input_tokens} output_tokens={u.output_tokens}")
    print(f"stop_reason: {response.stop_reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
