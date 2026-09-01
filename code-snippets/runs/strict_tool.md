# A strict schema + a validation layer

> Worked example · **Day 2** · exam domain **D6/D2** · source `code-snippets/strict_tool.py`
> Run it yourself: `python code-snippets/strict_tool.py`

## Scenario

A `strict:true` tool constrains the arguments; a `validate()` function is the belt-and-braces check for the paths a schema can't express.

**Input / dataset.** Three inputs: a clean one, one with a wrong enum value, one missing a field.

## The code

<!-- CODE:START -->
```python
"""
strict_tool.py — guaranteed output shape with strict tool use + a validate() layer.

Exam angles (D2):
  * `strict: true` is a field on the TOOL DEFINITION (not on tool_choice)
  * schema needs additionalProperties:false AND every property in `required`
  * strict has no "optional" -> express optional as a nullable type ["string","null"]
  * UNSUPPORTED schema features are REJECTED, not silently ignored
  * parse tool inputs with json.loads -- never string-match the serialized input
  * client.messages.parse() validates the response against a schema for you

    cd aizentify-cdf-bootcamp && python code-snippets/strict_tool.py
"""
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

FINDING_SCHEMA = {
    "type": "object",
    "properties": {
        "file_path": {"type": "string"},
        "line": {"type": "integer"},
        "severity": {"type": "string", "enum": ["blocking", "warning", "nit"]},
        "message": {"type": "string"},
        "suggested_fix": {"type": ["string", "null"]},   # optional == nullable
    },
    "required": ["file_path", "line", "severity", "message", "suggested_fix"],
    "additionalProperties": False,
}


def validate_finding(a: dict) -> list[str]:
    errs = []
    if not isinstance(a.get("line"), int) or isinstance(a.get("line"), bool) or a["line"] < 1:
        errs.append("line must be a positive integer")
    if a.get("severity") not in ("blocking", "warning", "nit"):
        errs.append(f"severity must be blocking|warning|nit -- got {a.get('severity')!r}")
    return errs


resp = client.messages.create(
    model="claude-haiku-4-5", max_tokens=300,
    tools=[{
        "name": "submit_finding",
        "description": "Submit exactly one structured code-review finding.",
        "strict": True,
        "input_schema": FINDING_SCHEMA,
    }],
    tool_choice={"type": "any"},
    messages=[{"role": "user", "content":
               "src/auth.py line 12: check_token() always returns True. File a finding."}],
)

for b in resp.content:
    if b.type == "tool_use":
        args = b.input                      # already a dict (parsed) -- don't string-match
        print("tool input :", json.dumps(args))
        print("validate() :", validate_finding(args) or "OK")
```
<!-- CODE:END -->

## Output

<!-- OUTPUT:START -->
_captured · mock run — numbers illustrative_

```text
tool input : {"file_path": "discount.py", "line": 12, "severity": "warning", "message": "apply_discount() has no docstring", "suggested_fix": null}
validate() : OK
```
<!-- OUTPUT:END -->

## Read the output

- 'Optional' doesn't exist in strict mode — express it as a **nullable** type.
- Unsupported JSON-Schema features are **rejected, not ignored**.
- Even with a schema, check `stop_reason` — a refusal or truncation still produces non-parsing output.

## Exam hook

BUG items on a `strict` tool failing an 'optional' field; 'unsupported schema feature is…'.

## Your turn

Add `"pattern": "^[A-Z]"` on a deep field and re-run — see it rejected at request time.
