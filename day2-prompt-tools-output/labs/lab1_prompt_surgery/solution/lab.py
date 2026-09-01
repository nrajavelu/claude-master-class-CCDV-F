"""Day 2 · Lab 1 — prompt surgery in three passes (SOLUTION).

    cd aizentify-cdf-bootcamp
    python day2-prompt-tools-output/labs/lab1_prompt_surgery/solution/lab.py

Each pass adds one STRUCTURAL technique, not more adjectives:
  pass 1  the weak prompt as-is
  pass 2  + role / audience / purpose
  pass 3  + explicit output shape + one few-shot example
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

PASS2 = (
    "You summarise engineering bug reports for the developer who will fix the issue. "
    "They do not need a retelling of the report — they need the underlying cause and enough "
    "context to act. Summarise only what is in the text; do not invent tools, ports, or "
    "numbers that are not stated."
)

PASS3 = PASS2 + (
    "\n\nFormat: at most 4 bullets. The FIRST bullet states the root cause. Later bullets "
    "give supporting context and a direction for the fix. No preamble.\n\n"
    "Example —\n"
    "Input: \"The nightly job double-charges ~1% of customers. It retries on timeout but the "
    "charge call isn't idempotent, so a retry after a slow-but-successful call bills twice.\"\n"
    "Summary:\n"
    "- Root cause: the charge call is not idempotent, so a retry after a slow success charges twice.\n"
    "- Trigger: timeout-based retries on the nightly job.\n"
    "- Impact: ~1% of customers double-charged.\n"
    "- Fix direction: make the charge call idempotent (idempotency key) before retrying."
)

PASSES = [WEAK, PASS2, PASS3]


def summarise(system: str) -> str:
    msg = client.messages.create(
        model=MODEL, max_tokens=400, system=system,
        messages=[{"role": "user", "content": INPUT}],
    )
    return "".join(b.text for b in msg.content if b.type == "text")


def main():
    for i, sys_prompt in enumerate(PASSES, 1):
        out = summarise(sys_prompt)
        (HERE / "solution" / f"out_pass{i}.txt").write_text(out)
        n, missed = score(out)
        print(f"pass {i}  score: {n}/5" + (f"   missed: {' · '.join(missed)}" if missed else ""))
        print(out.strip()[:400], "\n---")


if __name__ == "__main__":
    main()
