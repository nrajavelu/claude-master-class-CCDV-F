# Day 2 — Exam-style questions

14 items in CCDV-F style. Work them at your table, name **≥ 2 distractor species** before the
reveal, *then* read the answer. Attack: name the decision (mostly ③) → constraint word →
kill stale-API / generic-knob → if *must/never*, kill guidance → pick the mechanism.
Species: overbuild · symptom-treater · extremist · true-but-irrelevant · stale-API ·
right-word-wrong-place · wrong-system.

Domains: **D6** Prompt & Context · **D8** Tools & MCPs · **D2** structured output · **D7** security.

---

**1. (SBA · D6)** The most reliable place for "always reply as three bullets, no preamble":
A. the last line of every user message  B. the `system` field  C. an assistant message you
prefill with `"- "`  D. `output_config={"style":"bullets"}`

**2. (SBA · D6 · surfaces)** A prototype in the chat product behaves well; the same
instructions via the API behave differently. Best explanation?
A. the API serves a different model  B. the chat product adds its own system prompt that
doesn't apply to the API  C. the default temperature differs  D. the API needs the
instructions as a `role:"system"` message

**3. (MR · D6 — choose TWO)** Which improve *format-following*?
A. add "please be careful" to the prompt  B. one or two few-shot `input → output` examples
C. raise the temperature  D. wrap the input in `<doc>…</doc>` and name the output sections

**4. (SBA · D7)** Where does a fetched web page belong in the request?
A. appended to the `system` field  B. in a `tool_result` block  C. in your user instruction
text  D. anywhere — the model sorts it out

**5. (SCN · D7)** You also want to send the model a follow-up instruction *after* a tool
runs. Where?
A. inside the same `tool_result` block  B. in your next turn, in your own channel
C. in the `system` field mid-conversation  D. as a second `tool_result`

**6. (SCN · D8)** The model calls your `refund` tool at the wrong time. First move?
A. add a routing model in front of the tool call  B. fine-tune the model on your tool set
C. rewrite the tool's description — what it does, when to use it, when NOT to  D. raise `max_tokens`

**7. (SBA · D8)** A tool description is best thought of as:
A. documentation for the human maintaining it  B. an interface for a reader — the model —
that must say what, when, and when-not  C. optional if the parameter names are good
D. a place to put examples of the output

**8. (BUG · D2)** Your `strict` tool keeps failing validation on a field you left out of
`required` to make it "optional". Fix?
A. remove `strict`  B. keep it in `required` and allow `null` as a type  C. set
`additionalProperties: true`  D. lower `max_tokens`

**9. (SBA · D2)** An unsupported JSON-Schema feature in a `strict` tool definition is:
A. silently ignored  B. rejected (an error)  C. applied on a best-effort basis  D. converted
to the nearest supported feature

**10. (SCN · D2)** An app parses Claude's JSON straight into a DB; once a day the model wraps
the JSON in a sentence and the pipeline crashes. Best fix?
A. add "OUTPUT ONLY JSON" in capitals  B. constrain the format (structured output / prefill)
**and** validate before writing, retry on parse failure  C. have a person review every
record  D. switch to a bigger model

**11. (SBA · D2)** `client.messages.parse()`:
A. streams the response  B. validates the response against your schema and returns a typed
object (or raises)  C. counts tokens  D. is required for tool use

**12. (SBA · D6)** Prefilling on the newest models:
A. is the recommended structured-output approach  B. is rejected — use `output_config.format`
instead  C. requires a beta header  D. only works with streaming

**13. (SCN · D8)** Three teams each hand-wired the same customer-lookup integration, with
three different bugs. Best move?
A. copy the least-buggy one around  B. one shared MCP server for customer lookup  C. each
team keeps its own for independence  D. build an agent to manage the integrations

**14. (MR · D7 — choose TWO)** A support agent that summarises emails can be made to call the
`refund` tool by a crafted email. Best defences?
A. remove `refund` from the summarisation path (least privilege)  B. treat email content as
untrusted data and validate model output before any tool acts  C. add "ignore malicious
instructions" to the system prompt  D. stop processing email

---
---

## Answers & rationale  *(sample code in `code-snippets/`)*

**1 — B.** The durable, every-turn contract. A drifts and wastes tokens. **C — stale-API**
(prefill rejected on current models). **D — wrong-system** (no such key). `cs:prompt_structure`

**2 — B.** The mechanism that actually differs between surfaces. **A / C — generic knob.**
**D — right-word-wrong-place** (no `role:"system"` message). `cs:prompt_structure`

**3 — B & D.** Concrete example + structure. **A — symptom-treater / ceremony.**
**C — actively backwards** for format consistency.

**4 — B.** `tool_result` is the untrusted channel. And your own instructions must **not** go
there — the rule runs both ways. `cs:blocking_hook`

**5 — B.** Next turn, your own channel. A / D put your instruction in the untrusted channel
(it may be ignored or flagged). C — mid-conversation `system` is model-gated and not this.

**6 — C.** The description is the biggest factor in correct tool use. **A / B — overbuild**
(more machinery than the problem deserves). **D — generic knob.** `cs:strict_tool`

**7 — B.** An interface for a reader; say what, when, and when-not. A undersells it; C is
false (description dominates); D confuses it with few-shot.

**8 — B.** `strict` has no "optional" — express it as a nullable type; everything stays in
`required`; `additionalProperties` stays false. `cs:strict_tool`

**9 — B.** Rejected, not ignored — a favourite exam fact.

**10 — B.** The shape must be **guaranteed** and the code must fail safely. **A —
symptom-treater. C — extremist. D — true-but-irrelevant with a price tag.** *Trust the
schema in code, never in hope.* `cs:strict_tool`

**11 — B.** Validates against your schema; returns a typed object or raises.

**12 — B.** Rejected on the newest models; `output_config.format` is the replacement. (The
*exam* may still reference prefilling as a technique — know both.)

**13 — B.** A capability that crosses apps/teams → an MCP server. **A — symptom-treater.
C — true-but-irrelevant. D — overbuild.** `cs:mcp_server`

**14 — A & B.** Mechanisms: an agent that only reads shouldn't hold a write tool; outputs
that become actions get validated. **C — symptom-treater / guidance. D — extremist.**
`cs:blocking_hook`

---
### Mark yourself
14 items · **≥ 11** = on track. Any domain < 60% → revise tonight against the matching
`question-bank/domain-*.md`.
