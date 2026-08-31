"""Day 2 · Lab 3 — strict output + validation (STARTER). Fill every # TODO."""
from __future__ import annotations

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"

ALLOWED = ("blocking", "warning", "nit")

FINDING_SCHEMA = {
    "type": "object",
    "properties": {
        "file_path": {"type": "string"},
        "line": {"type": "integer"},
        "severity": {"type": "string", "enum": list(ALLOWED)},
        "message": {"type": "string"},
        "suggested_fix": {"type": ["string", "null"]},
    },
    "required": ["file_path", "line", "severity", "message", "suggested_fix"],
    "additionalProperties": False,
}

FIXTURES = {
    "clean": {"file_path": "src/auth.py", "line": 12, "severity": "warning",
              "message": "check_token always returns True.", "suggested_fix": None},
    "wrong-severity": {"file_path": "src/auth.py", "line": 12, "severity": "critical",
                       "message": "check_token always returns True.", "suggested_fix": None},
    "missing-line": {"file_path": "src/auth.py", "severity": "warning",
                     "message": "check_token always returns True.", "suggested_fix": None},
}


def validate_finding(args: dict) -> list[str]:
    errors: list[str] = []
    # TODO: line must be a positive integer (and not a bool)
    # TODO: severity must be in ALLOWED  -> "severity must be one of %r -- got %r" % (list(ALLOWED), args.get("severity"))
    # TODO: message must be a non-empty string
    # TODO: suggested_fix must be PRESENT (in args) and be str or None
    return errors


def via_strict_tool():
    print("=== strict tool ===")
    for name, args in FIXTURES.items():
        errs = validate_finding(args)
        if errs:
            print(f"{name:14s} -> validate: {errs}")
        else:
            print(f"{name:14s} -> validate: OK        -> recorded [{args['severity']}] "
                  f"{args['file_path']}:{args['line']}")
    # TODO (optional): make one real API call with a strict tool that uses FINDING_SCHEMA,
    #   tool_choice={"type":"any"}, and print the tool_use block's .input (a dict).


def via_parse():
    print("\n=== messages.parse() ===")
    # TODO: call client.messages.parse(model=MODEL, max_tokens=300,
    #   messages=[{"role":"user","content": "src/auth.py line 12: check_token() always "
    #             "returns True. File a finding."}],
    #   output_config={"format": {"type": "json_schema", "schema": FINDING_SCHEMA}})
    #   print the parsed object; then send a deliberately bad instruction and print the error.
    print("TODO")


if __name__ == "__main__":
    via_strict_tool()
    via_parse()
