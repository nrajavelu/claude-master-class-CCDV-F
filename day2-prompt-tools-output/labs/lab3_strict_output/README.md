# Lab 3 · Structured output you can trust

**Domain:** D2 (structured output) · D4 (validation) · **Time:** 45 min
**Practise:** `strict: true` tool definitions · `additionalProperties:false` + null-for-optional ·
a `validate_finding()` enforcement layer · `client.messages.parse()`.

---

## Goal

A `submit_finding` tool that accepts **exactly one** structured code-review finding, and a
`validate_finding()` layer that returns *specific* problems (so the model can fix and
resubmit). Feed it three inputs: one clean, one wrong-severity, one missing-line. Then do the
same extraction with `client.messages.parse()` and compare.

```
cd aizentify-cdf-bootcamp
python day2-prompt-tools-output/labs/lab3_strict_output/starter/lab.py
```

---

## Steps

1. Open `starter/lab.py`. `FINDING_SCHEMA` is given — study it: every property in
   `required`, `additionalProperties:false`, `suggested_fix` typed `["string","null"]`.
2. Fill `validate_finding(args)` — return a list of strings, empty = good. Check: `line` is a
   positive int; `severity` in `("blocking","warning","nit")`; `message` non-empty;
   `suggested_fix` is `str` or `None` (present, not omitted).
3. Fill the raw-API call: a tool with `"strict": True` + `FINDING_SCHEMA`,
   `tool_choice={"type":"any"}`, and read the `tool_use` block's `.input` (already a dict —
   don't string-match it).
4. Run the three fixtures through `validate_finding` and print the result.
5. Fill the `messages.parse()` path: same schema via `output_config={"format": {...}}` or
   the `parse()` helper; print the typed object or the exception.

---

## Expected output (shape)

```
=== strict tool ===
clean          -> validate: OK        -> recorded [warning] src/auth.py:12
wrong-severity -> validate: ['severity must be one of ... -- got "critical"']
missing-line   -> validate: ['line must be a positive integer (got None)']

=== messages.parse() ===
parsed: Finding(file_path='src/auth.py', line=12, severity='warning', ...)
bad input -> raised: <validation error naming the field>
```

## Checkpoints (trainer circulates)

- [ ] `validate_finding` messages are **specific** (name the field + the bad value), not
      "invalid input".
- [ ] `suggested_fix` handled as *present-or-null*, never *omitted* (strict has no optional).
- [ ] They read `block.input` as a dict — no `json.loads` on it, no string matching.
- [ ] They can state: **unsupported schema features are rejected, not ignored.**

## Common mistakes

| Symptom | Cause |
|---|---|
| `strict` request 400s | a schema feature isn't supported — simplify; it's rejected, not ignored |
| `validate` passes a missing `suggested_fix` | you checked truthiness, not membership — use `"suggested_fix" not in args` |
| `parse()` import error | use `client.messages.parse(...)` (SDK ≥ recent) or `output_config={"format": {...}}` on `create` |

## Going further

- Add a `publish_review()` that builds one comment from all recorded findings, sorted by
  severity — the `ep07` pattern.
- Wire `validate_finding` as an SDK `@tool` and confirm `strict` is **not** forwarded on that
  path (so `validate()` is what enforces) — the honest note from `ep07/schemas.py`.
