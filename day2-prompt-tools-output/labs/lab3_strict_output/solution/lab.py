"""Day 2 · Lab 3 — strict output + validation (SOLUTION)."""
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
    """Every message is written to go straight back to the model — say exactly what's wrong."""
    errors: list[str] = []
    line = args.get("line")
    if not isinstance(line, int) or isinstance(line, bool) or line < 1:
        errors.append(f"line must be a positive integer (got {line!r})")
    sev = args.get("severity")
    if sev not in ALLOWED:
        errors.append(f"severity must be one of {list(ALLOWED)} -- got {sev!r}; do not invent a label")
    msg = args.get("message")
    if not isinstance(msg, str) or not msg.strip():
        errors.append("message must be a non-empty string")
    if "suggested_fix" not in args:
        errors.append("suggested_fix is required -- pass null if you have no confident fix, do not omit it")
    elif args["suggested_fix"] is not None and not isinstance(args["suggested_fix"], str):
        errors.append("suggested_fix must be a string or null")
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

    # a real call: strict guarantees the SHAPE; validate_finding still enforces the RULES
    r = client.messages.create(
        model=MODEL, max_tokens=300,
        tools=[{"name": "submit_finding",
                "description": "Submit exactly one structured code-review finding.",
                "strict": True, "input_schema": FINDING_SCHEMA}],
        tool_choice={"type": "any"},
        messages=[{"role": "user",
                   "content": "src/auth.py line 12: check_token() always returns True. File a finding."}],
    )
    for b in r.content:
        if b.type == "tool_use":
            print("live tool_use.input:", b.input, "| validate:", validate_finding(b.input) or "OK")


def via_parse():
    print("\n=== messages.parse() ===")
    try:
        parsed = client.messages.parse(
            model=MODEL, max_tokens=300,
            messages=[{"role": "user",
                       "content": "src/auth.py line 12: check_token() always returns True. File a finding."}],
            output_config={"format": {"type": "json_schema", "schema": FINDING_SCHEMA}},
        )
        print("parsed:", parsed.parsed_output if hasattr(parsed, "parsed_output") else parsed)
    except Exception as e:  # noqa: BLE001 — show whatever the SDK version raises
        print(f"parse() path not available on this SDK ({e.__class__.__name__}); "
              f"fall back to the strict-tool path above.")


if __name__ == "__main__":
    via_strict_tool()
    via_parse()
