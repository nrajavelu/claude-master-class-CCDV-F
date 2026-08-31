# Day 2 — Prompt & context engineering · tools · structured output

> **Status: outline + lab specs.** Full build (deck, trainer guide, labs with `starter/` +
> `solution/`, exercises, quiz, exam-style questions) lands in build pass 2. This file is the
> spec that pass will execute.

**Primary CCDV-F domains:** D6 Prompt & Context Engineering (11%) · D8 Tools & MCPs (10.6%,
Tool Implementation) · D2 Applications & Integration (structured output / Application
Design). **Decisions:** mostly ③ *what does Claude see and say?*, some ① *what runs?*
**Anchor episodes:** `ep03` (custom tool), `ep07` (structured output), `ep04` (guardrails).
**Video companion:** lessons 5, 7, 12, 16.

---

## Learning objectives

By end of Day 2 a candidate can:

1. Engineer a prompt deliberately: role/contract in `system`, task+data in `messages`,
   structure with XML tags, few-shot for format, and know when to add thinking/effort.
2. Explain **the three surfaces** and their different contracts — the chat product (Anthropic's
   own system prompt underneath yours; doesn't transfer), a coding-tool rules file (arrives as
   a *user message*), and the API (`system` field; **no message may have `role: "system"`**).
3. State and apply the **untrusted-content rule in both directions**: third-party / tool
   output goes only in `tool_result` blocks; your own instructions never go there.
4. Define a tool with a schema, `tool_choice`, and a description good enough that the model
   uses it correctly — "the description is the interface".
5. Enforce **structured output**: `strict: true` on a tool definition, `additionalProperties:
   false`, all fields in `required` (optional = allow `null`), `output_config.format` /
   `client.messages.parse()`; and know that **unsupported schema features are rejected, not
   ignored**.
6. Add a **validation layer** — "asking is not making sure": a schema *guides*, code
   *enforces*.

## Module plan (deck outline)

| # | Module | Key slides | Domain / decision |
|---|---|---|---|
| 1 | Prompt engineering, deliberately | contract vs task · explicit > clever · XML structure · few-shot (zero/one/multi-shot) · thinking & effort recap | D6 · ③ |
| 2 | Output handling | ask for a shape · skeletons · why "best-effort" isn't enough | D6 · ③ |
| 3 | The three surfaces | chat product vs coding rules-file vs API · the `role:"system"` trap · what transfers and what doesn't | D2 · ③ |
| 4 | Boundaries & untrusted content | tool_result is the untrusted channel (both directions) · per-content XML tags · injection preview | D6/D7 · ④ |
| 5 | Tools: the description is the interface | schema · `tool_choice` · parallel tools · `is_error` · writing a description the model obeys | D8 · ① |
| 6 | Structured output you can trust | `strict:true` · `additionalProperties:false` · null-for-optional · `messages.parse()` · unsupported features are **rejected** | D2 · ③ |
| 7 | Validate, don't hope | a `validate()` layer · specific error messages back to the model · retry-to-correct | D2/D4 · ④ |
| 8 | Bridge to the SDK | `@tool` + `create_sdk_mcp_server`; run `ep03` | D8 · ① |
| — | recap + exam-style questions + quiz | | |

## Lab specs

### Lab 1 · Prompt surgery, scored  ·  30 min · D6
- **Given:** a weak prompt + a rubric (3–5 checks: format, length, no invented facts, cites
  input, audience-appropriate).
- **Do:** improve the `system` prompt over 3 passes (role/audience → shape → one few-shot).
  Re-run against a fixed input each pass. Score each output against the rubric with a tiny
  checker script provided in `starter/`.
- **Expected output:** rubric score climbs pass-1 → pass-3 (e.g. 2/5 → 5/5); the three
  system prompts saved for comparison.
- **Reference:** Day 1 `exercises.md` Exercise B (this is its graded version).

### Lab 2 · A tool with a real description  ·  35 min · D8
- **Do:** define a `lookup_order(order_id)` tool (mock data) with (a) a deliberately vague
  description, then (b) a detailed one. Run the same 5 prompts through each.
- **Expected output:** with the vague description the model mis-calls / skips the tool on
  ≥ 2 prompts; with the detailed one it calls correctly on all 5. Candidate writes one
  sentence on why.
- **Reference:** `ep03/tools.py` description style.

### Lab 3 · Strict structured output + validation  ·  45 min · D2
- **Do:** build a `submit_finding` tool with `strict: true` and `FINDING_SCHEMA`
  (`file_path`, `line:int`, `severity:enum`, `message`, `suggested_fix: str|null`), plus a
  `validate_finding()` function that returns *specific* errors. Feed it 3 inputs: one clean,
  one wrong-severity, one missing-line. Also do the same extraction with
  `client.messages.parse()` and compare.
- **Expected output:** clean input recorded; bad inputs rejected with a message precise
  enough for the model to fix and resubmit; `parse()` path returns a typed object or raises.
- **Reference:** `ep07/schemas.py`, `ep07/tools.py` (read-along; build fresh).

### Lab 4 · Port a tool to the SDK  ·  25 min · D8
- **Do:** wrap Lab 2's tool as `@tool` + `create_sdk_mcp_server`; call it from `query()` with
  `allowed_tools` scoped to just that tool.
- **Expected output:** SDK run produces the same tool call + result as the raw-API version.
- **Reference:** `ep03/agent.py`.

## Exam-style question targets (≥ 15 items)

Surfaces & `role:"system"` trap · untrusted content direction · `strict` schema rules ·
unsupported-feature-is-rejected · tool description quality · few-shot vocabulary
(zero/one/multi-shot vs few-shot) · schema-as-contract ("asking is not making sure") ·
`tool_choice` values · parallel tool_result packaging.

## Quiz targets (10–12)

3 surfaces / 3 contracts · where instructions live · tool_result rule both ways ·
`strict` requirements · null-for-optional · `messages.parse()` · validation vs schema.
