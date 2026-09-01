"""Day 2 · Lab 1 — prompt surgery in three passes (STARTER). Fill PASSES[1] and PASSES[2].

    cd aizentify-cdf-bootcamp
    python day2-prompt-tools-output/labs/lab1_prompt_surgery/starter/lab.py

Reference: code-snippets/prompt_structure.py
"""
import pathlib
import sys

from dotenv import load_dotenv
import anthropic

HERE = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(HERE))
from rubric import score  # noqa: E402

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"

WEAK = (HERE / "prompts" / "weak_system.txt").read_text().strip()
INPUT = (HERE / "sample_input.txt").read_text().strip()

PASSES = [
    WEAK,
    # TODO pass 2: WEAK + role + audience + purpose (engineer who will fix it; wants the
    #              root cause, not a recap)
    "TODO",
    # TODO pass 3: pass-2 text + output shape (<=4 bullets, first bullet = root cause, no
    #              invented specifics) + ONE few-shot input->summary example
    "TODO",
]


def summarise(system: str) -> str:
    msg = client.messages.create(
        model=MODEL, max_tokens=400, system=system,
        messages=[{"role": "user", "content": INPUT}],
    )
    return "".join(b.text for b in msg.content if b.type == "text")


def main():
    for i, sys_prompt in enumerate(PASSES, 1):
        out = summarise(sys_prompt)
        (HERE / "starter" / f"out_pass{i}.txt").write_text(out)
        n, missed = score(out)
        print(f"pass {i}  score: {n}/5" + (f"   missed: {' · '.join(missed)}" if missed else ""))


if __name__ == "__main__":
    main()
