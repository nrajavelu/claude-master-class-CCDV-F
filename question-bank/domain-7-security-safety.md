# Domain 7 — Security and Safety  ·  8.1%  ·  decision ④ "will it survive production?"

> **Status: blueprint.** Item target **14**. Built pass 3 alongside Day 5 (hooks on Day 3).
> Anchor: `ep04`/`ep05` hooks. Video: lesson 16.

## Sub-areas & item split

| Sub-area | Weight | Items | Topics |
|---|---:|---:|---|
| AI Application Security | 3.2% | 6 | prompt injection ("the attack arrives as a ticket") · **guidance is not a control** · untrusted content isolation · third-party content only in `tool_result`, your instructions never there · tool-output trust · a more capable model follows injected instructions *better* too |
| Guardrails and Safe Deployment | 2.3% | 3 | blocking hook / schema / isolation as the mechanism · human-in-the-loop approval gates · fail-closed defaults · self-hosted ≠ air-gapped |
| Claude Hooks | 1.0% | 2 | `PreToolUse` deny · `PostToolUse` transform/taint · `Stop` gate · hooks run in *code*, so they can't be talked out of it |
| Identity, Secrets & Key Management | 1.6% | 3 | keys in a secret store, never the repo · least-privilege keys / fine-grained PATs · env-var expansion in config (`${VAR}`) · rotate on leak · a plugin runs with your privileges |

## Seed items

### 1. (SCN · must/never) "Ticket text submitted by customers must never trigger the refund
tool." Which satisfies the requirement?
A. add a system-prompt line telling the model to ignore instructions inside tickets
B. use the most capable model tier
C. treat ticket text as untrusted, keep it out of the instruction channel, and put a
   blocking approval hook in front of the refund tool
D. set temperature to 0

> **Answer:** C. Rule 2: "must never" kills guidance (A). B/D are knobs — and a stronger
> model can follow the *injected* instruction better. Only C is a mechanism that stops it.

### 2. (SBA) Where does third-party content (a fetched web page, a customer ticket) belong?
A. appended to the `system` field  B. in a `tool_result` block  C. in your user instruction
text  D. anywhere — the model sorts it out

> **Answer:** B — and your own instructions must **not** go in a `tool_result`.

### 3. (SBA) Installing a plugin/marketplace bundle is:
A. sandboxed and safe by default  B. a trust decision — it runs code with your privileges,
like adding a dependency  C. read-only  D. reversible with no risk

> **Answer:** B.
