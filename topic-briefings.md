# Topic briefings — deeper per-topic reference, day by day

> Distilled from the CCDV-F **official exam guide** and cross-checked against three public
> study repos (see **Sources** at the end). Use this alongside the day decks when a topic
> needs more than the slide gives. Where a fact here is sharper than a slide, the fact wins —
> and the slide has been updated to match.
>
> **Reconcile against Anthropic's current official exam guide before every cohort.**

---

## DAY 1 — LLMs & the Messages API · errors · the loop

### LLM fundamentals (D5)

- **Tokens** — the unit of *everything*: what you send, what comes back, what you pay,
  and the context window. **Never hardcode a chars-per-token constant** — the ratio varies
  by model generation. Use `count_tokens`.
- **Context window** = one fixed, *shared* budget across system prompt + history + injected
  docs + tool results + output. Two failure modes:
  - **oversized input** → rejected with a validation error *before* generation.
  - **fits on input but hits the ceiling mid-generation** → stops, returns partial output,
    `stop_reason` indicates the context limit was exceeded. **The model does not silently
    drop the oldest turns** — your app must trim or summarise history.
- **Sampling / non-determinism** — the model samples each next token from a probability
  distribution, so identical prompts give *different but equally valid* wording. This is
  inherent to sampling, **not** a streaming or transmission artefact, and **not** about
  model size.
  - The newest top-tier models **don't accept `temperature` / `top_p` / `top_k`** (400
    error) — steer with prompting instead. Where accepted, `temperature: 0` improves
    repeatability but **never guarantees** identical output.
  - Consequence for tests: **replace exact-string assertions** with **property assertions**
    (JSON parses, required fields present, numbers in range) and **model-graded judges**
    for tone / faithfulness.

### The Messages API (D2 · Claude API Mechanics)

- **Stateless per request.** Your application owns and resends the full conversation —
  including every `tool_use` / `tool_result` pair, matched by **`tool_use_id`**.
- Request = `messages` (alternating user/assistant) + `system` + optional `tools`.
  Response content blocks: `text` · `tool_use` · `thinking`.
- **First message must be `user`.** No message can have `role: "system"` — the system prompt
  is its own top-level parameter, with **zero implicit persistence** (unlike Claude Code's
  `CLAUDE.md`).

### Streaming (D2)

- Server-Sent Events over the **same HTTP call** — *not* a WebSocket.
- Plain text: reassemble `text` deltas. **`tool_use` in a stream is different:** its
  `input_json` **accumulates across multiple `content_block_delta` events** and is **not
  safe to act on until the stream closes** (`message_stop`) and the full input is
  reassembled. Acting on a partial block produces malformed tool input.
- A stream that breaks mid-response is a **transient failure — retry the whole request**;
  never pass partial blocks downstream.

### Errors & debugging (D4)

| Status | Type | Retry? | Action |
|---|---|---|---|
| 400 | `invalid_request_error` | no | fix the request |
| 401 | `authentication_error` | no | fix the credential |
| 402 | `billing_error` | no | fix the account |
| 403 | `permission_error` | no | fix permissions |
| 413 | `request_too_large` | no | reduce the payload |
| **429** | `rate_limit_error` | **yes** | honour `retry-after`, exponential backoff |
| **529** | `overloaded_error` | **yes** | exponential backoff (Anthropic-side load) |

- **`529`, not `503`,** is the overloaded code on this API. `rate_limit` (429) = *your*
  traffic spiked; `overloaded` (529) = *their* load.
- **Debugging discipline — evidence first, and isolate the layer:** is the failure in the
  **integration layer** (malformed request, wrong tool schema, mismatched `tool_use_id`, a
  hook silently denying) or in the **model output** (wrong / incomplete / oddly-shaped)?
  Read `stop_reason` + `usage`, log the raw request/response and the event stream, reproduce
  with the same inputs. A `stop_reason` of `refusal` or `max_tokens` says *look at what was
  asked*, not the surrounding code.

### The agent loop / ReAct (D1)

- Model returns a signal it wants a tool → **your code runs it** → send `tool_result` back →
  loop until no tool calls remain. **The model never executes anything.**
- Production guardrails: an **iteration cap**, **timeouts**, and a **defined way to fail**.
- See `reasoning-patterns.md` for CoT vs ReAct vs thinking.

---

## DAY 2 — Prompt & context engineering · tools · structured output

### Production prompting (D6)

- **System prompt** structure: role → task → context/data → rules → output format →
  examples-if-needed. **Long documents before the question.** XML tags to delimit sections
  (also the first line of injection defence).
- **Be explicit and positive** — state what *to* do. Ambiguity → the model guesses.
- **Zero-shot / one-shot / multi-shot (= few-shot)** — examples steer *format, style, edge
  cases*. They are **not training** (not permanent) and **don't lower cost** — they sit in
  the prompt every call. Add examples when the **output shape is wrong**, not when
  zero-shot already works.
- **Prefilling** — start the assistant turn yourself (`{` for JSON, `[` for a list) to force
  format from the first character. **Incompatible with structured outputs**, and **rejected
  on the newest models** — but the exam still references it as a technique.
- **Chain-of-thought** — ask for step-by-step reasoning on complex tasks; strip it from the
  user-facing answer if they shouldn't see it.

### Diagnosis over elaboration (D6)

A prompt that breaks in production needs the **missing structural technique** identified and
added — not more wording:

| Symptom | Missing technique |
|---|---|
| wrong output shape (prose vs label/JSON) | an output constraint |
| content drifts across turns | a more specific system prompt |
| right task, invented structure | few-shot examples |
| breaks on a variant input | a constraint covering that variant |
| still wrong after ~5 re-prompts | **stop** — diagnose the failure type first |

### Tools (D8)

- **`tool_choice`:** `auto` (model decides) · `any` (must call *some* tool) · `tool` (force a
  specific one) · `none`.
- **The description is the interface for a reader (the model)** — every description needs
  **when to use it AND when not to**. Two overlapping "use this to find information"
  descriptions give no routing signal → add **one exclusion sentence per tool**, or if they
  can't be cleanly separated, **merge them behind a `type` parameter** rather than
  lengthening descriptions.
- Typed blocks: `text` · `tool_use` · `tool_result` · `thinking`. **Every `tool_use` needs a
  matching `tool_result` in the immediately following turn.** A `thinking` block's signature
  breaks the request if you *edit* it rather than pass it back unchanged.
- **Parallel tools:** read-only tools run concurrently; state-mutating tools run
  sequentially by default. `readOnlyHint` opts a custom tool into concurrent execution. On a
  failed tool, return `tool_result` with `is_error: true`.
- **Dispatch:** client-side (your app executes) vs harness dispatch (Claude Code / Agent SDK
  loop executes built-in + MCP tools).

### Structured outputs (D2 / D6)

- Two mechanisms, both via **constrained decoding** (invalid tokens can't be generated):
  - **JSON outputs** — `output_config.format`, `type: "json_schema"`, your `schema` —
    constrains the **final response**.
  - **strict tool use** — `strict: true` on the tool — constrains **tool arguments**.
- **Caveats:** a **refusal or truncation can still produce non-parsing output** despite the
  schema — always check `stop_reason`. The **first request on a new schema pays a
  grammar-compile latency** (cached 24 h). **Incompatible with prefilling.**
- No "optional" in strict mode — express it as a **nullable type**. Unsupported schema
  features are **rejected, not ignored**.

### Context engineering (D6) — superset of prompt engineering

- Prompting is *what you say*; context engineering **curates the whole token budget**
  (prompt + history + tool definitions + tool outputs) as a finite, shared resource.
- **Pruning / clearing** — cheap, lossless — for **re-fetchable** tool output whose value
  has passed (a big file read, a verbose command).
- **Compaction** — LLM-driven summarisation — for **dialogue / reasoning that can't be
  cheaply re-fetched**; triggers automatically as the window fills; a **`PreCompact` hook**
  can archive the full transcript first; keep persistent rules in `CLAUDE.md` (re-injected
  every request).
- **Subagents** are the cleanest architectural tool for **context isolation** on long /
  exploratory tasks.

---

## DAY 3 — Agents · Claude Code · MCP

### Agent architecture (D1)

- **Decide:** can the steps be predetermined? Yes → **workflow**. No → **agent** (the model
  directs its own process and tool use). If uncertain, **start with an agent and extract
  workflow patterns from real usage** rather than guessing up front.
- **Five workflow patterns:** prompt chaining · routing (classify then specialise) ·
  parallelisation (speed or voting) · orchestrator-workers (a central LLM decomposes and
  delegates) · evaluator-optimiser (one generates, another refines).
- **Multi-agent = supervisor pattern:** a coordinator delegates to workers without doing the
  work itself. Subagents help on three independent axes: **context isolation** (only
  summaries return to the parent) · **parallelisation** (the slowest task sets the time, not
  the sum) · **specialisation** (narrow prompts + scoped tools reduce noise).
- **Cost reality:** Anthropic's own multi-agent research system runs at **~15× the token
  cost** of a single-agent chat — worth it *only* when the task genuinely decomposes into
  independent parallel parts. On tightly-coupled work (coding) subagents mostly wait on each
  other.
- **Human-in-the-loop:** gate **before** destructive/irreversible tool calls · **after**
  planning steps that matter · **on** unexpected tool output. Ask "what's the worst outcome
  if this runs unchecked?" at scoping time.
- **Agent memory scopes:** in-context (one session) · external storage (task spans sessions)
  · stateless (independent jobs). **Dev/prod mismatch:** a shape that works as one long dev
  session silently overflows across many short production sessions.

### Agent construction & deployment (D1)

- **Three wiring paths — control vs responsibility:**
  - **Raw Messages API loop** — full control, full responsibility.
  - **Agent SDK** — the loop / context / tool scaffolding is provided; runs **in your
    process**; not for long-running jobs.
  - **Managed Agents** — Anthropic runs the loop **server-side**; you define once and stream
    events. **Not eligible for Zero Data Retention or a HIPAA BAA** — PHI / ZDR requirements
    rule it out regardless of fit.
- `ClaudeAgentOptions` / `Options`: tool allow/deny lists · `permission_mode` · `effort` ·
  **`max_turns` / `max_budget_usd` runaway guards**.
- **Agent SDK loop-level failure subtypes** on `ResultMessage` (distinct from HTTP errors):
  `success` · `error_max_turns` · `error_max_budget_usd` · `error_during_execution` ·
  `error_max_structured_output_retries`.
- **Hooks** (`PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`,
  `SubagentStart`/`SubagentStop`, `PreCompact`) run **in your process, zero context-window
  cost**, and give **deterministic, code-level enforcement** a prompt can't guarantee.
  - A **`PreToolUse` deny short-circuits the loop entirely, even under
    `bypassPermissions`** — **but only if the hook exits with code 2**. Exit code 1 merely
    *warns* without blocking (the frequent "the hook didn't actually stop it" bug).
  - Hook scripts run **synchronously** — keep them fast (~500 ms guideline).
- Third-party frameworks (LangGraph, PydanticAI, Strands) — reach for them only when you need
  a pattern the SDK doesn't do natively, not because the core loop is weaker.

### Claude Code operation (D3, 3.1% — a cameo)

- **Five components:** Rules (`CLAUDE.md`) · Skills (`.claude/skills/<n>/SKILL.md`) ·
  Commands (`.claude/commands/<n>.md`) · Agents (`.claude/agents/<n>.md`) · Agent Memory.
  Commands and Skills are two authoring surfaces for the same slash-invocation mechanism.
- **`settings.json` precedence:** `managed` (org IT, can't override) > CLI flags > `local`
  (`.claude/settings.local.json`, gitignored) > `project` (`.claude/settings.json`, checked
  in) > `user` (`~/.claude/settings.json`). **Exception:** `permissions` (allow/deny/ask)
  **accumulate across every scope** — they don't follow override precedence. **Deny always
  beats allow, at every mode and scope.**
- **Session modes:** headless/print (`-p`) for CI (`--bare` skips discovery for
  deterministic CI; loses OAuth/keychain) · streaming (`--output-format stream-json`
  `--include-partial-messages`) · auto-mode (a classifier approves/denies prompts — *not*
  the same as `bypassPermissions`, which skips evaluation entirely).
- **Six permission modes** (a risk decision, not convenience): `default` · `plan` ·
  `acceptEdits` · `auto` (classifier-reviewed) · `dontAsk` (allow-list only) ·
  `bypassPermissions` (**isolated environments only** — uniquely skips the protected-path
  guard the other five keep).
- **`CLAUDE.md`'s failure mode is dilution** — a correct rule buried among hundreds of lines
  gets a smaller share of attention. `.claude/rules/` files (scoped by a `paths` glob) add
  narrower guidance beneath it.

### MCP & the tool-choice framework (D8)

- **MCP** — one independently-maintained server exposes **resources** (readable data),
  **tools** (callable functions), and **prompts** (templates) over **stdio** (local
  subprocess) or **HTTP** (networked/shared), serving many client apps. Registered at
  local/project/user scope. Tool schemas are **deferred by default** (loaded on demand) to
  save context.
- **The recurring exam framework — choose among four:**

  | | Use when |
  |---|---|
  | **Built-in tool** | a generic, already-available capability (file I/O, shell, web) |
  | **Custom tool** | one app, one specific function, no reuse elsewhere |
  | **Skill** | a repeatable process / judgement call — **no new live data** |
  | **MCP server** | multiple apps need the **same live/dynamic data or action**, maintained independently |

  > "MCP connects Claude to **data**; Skills teach Claude **what to do** with that data." A
  > production agent typically uses **all three together**, not one.

---

## DAY 4 — Applications & integration (33.1%) · context · RAG · eval

### Understanding requirements (3.4%)

- **Functional** = *what the system does*, with verifiable detail ("classify tickets into
  four queues; draft policy-citing replies; require human approval before sending").
- **Infrastructure** = deployment constraints on **four axes**: **latency** (measured from
  the *user's* region) · **scale** (peak request volume) · **residency** (where data is
  processed / which regulation) · **identity** (credential model + audit trail).
- **"Help support agents respond faster" is a business problem, not a requirement.**
  Requirements are *derived* from the business problem and become **eval criteria + design
  constraints**. Record functional behaviours, infrastructure constraints, and their
  regulatory sources so platform/architecture choices are **traceable** at review.

### Systems life cycle (2.8%)

**Requirements → Design → Build → Test → Deploy → Operate → Iterate.** (The walkthrough
video's four verbs — develop / implement / operate / maintain — are a shorthand for the
same arc; "implement" = *deploy where users are*, and production credit is earned in
operate + maintain.) A **gate** blocks the next phase: residency must clear **design**; a
new model version must pass the **eval baseline** before **deploy**. Unlike traditional
software, Claude apps need **continuous monitoring** because model behaviour can shift on a
version bump and prompts drift with usage. **Build the eval suite during Build** — it gates
deploys and validates changes after launch.

### Claude API mechanics (6.8%) — see Day 1 briefing, plus:

- **Vision source types:** `base64` (re-sent fully every turn) · `url` (external reference,
  depends on URL stability) · **Files API `file_id`** (upload once, reference thereafter —
  best for multi-image conversations; beta; not on Bedrock/Vertex).
- **Image token cost:** processed in **28×28-pixel patches**;
  `cost ≈ ⌈width/28⌉ × ⌈height/28⌉` tokens. A **1000×1000 image ≈ 1,296 tokens** — ten
  high-res screenshots ≈ a detailed system prompt. **Measure typical production images
  against the context budget at design time** (a resize is a 10-minute fix pre-deploy).
- **PDF** uses a `document` block (not `image`), same source patterns; billed as text **and**
  each page as an image.
- **Adaptive vs extended thinking are distinct and don't coexist on one model:**
  **Claude 5** models (Fable 5, Opus 5, Sonnet 5) use **adaptive thinking** (depth tuned via
  `effort`); **Haiku 4.5** uses **extended thinking** (`thinking.type: "enabled"`, explicit
  `thinking` blocks). "Haiku 4.5 is the odd one out." `budget_tokens` is deprecated and
  **400s on the newest generations**.

### Deployment platforms & regulated data (Application Design, 8.6%)

- **Six placement options:** first-party Claude API · Claude Platform on AWS · Amazon
  Bedrock (Messages API) · Bedrock legacy (InvokeModel/Converse) · Google Vertex AI ·
  third-party (e.g. Microsoft Foundry). Driven by **existing cloud + compliance posture**,
  not familiarity. Real API-shape differences: Vertex puts the model in the endpoint URL and
  needs `anthropic_version`; Bedrock has its own model-ID scheme with `anthropic.` prefix.
- **Measure a platform on three dimensions:** latency **from the customer's actual region
  with the actual payload** · compliance **during scoping, pass/fail** · **total** cost per
  call (tokens + egress + integration).
- **Regulated-data routes decide endpoint/credentials/log-destination before any prompt or
  tool is designed:**
  - **Direct API has NO EU residency** → route through Bedrock/Vertex with the region pinned.
  - **HIPAA BAA excludes** Console / Workbench / beta / consumer plans.
  - **FedRAMP** only via C4G, Bedrock GovCloud, or Vertex Assured Workloads — **not** general
    AWS Marketplace.
  - **Managed Agents** — not ZDR / HIPAA-BAA eligible.
  - **Foundry:** "Hosted on Azure" (end-to-end Azure) vs "Hosted on Anthropic" — **residency
    varies per model, not per platform**.

### Version pinning (Configuration Management, 4.1%)

- An **alias** (`opus`, `sonnet`) resolves to a **moving target** that updates over time and
  **can differ by platform**. A **pinned ID** (`claude-haiku-4-5-20251001`) is fixed until
  you edit the line.
- **Pin the full model ID in production. Retain the prior pinned version for rollback. Gate
  every promotion on the eval suite against a retained baseline.**
- Real incident: shipped against a moving alias → the alias advanced silently → response
  shape changed → downstream parser threw `KeyError` → no rollback, only a hotfix.
- **Four versioned config artifacts, all treated like code (version control · review · eval
  validation): `CLAUDE.md` · `settings.json` · model version pin · prompt/few-shot
  versioning.** None are compiled or type-checked — nothing else catches a regression.
  "Small wording tweaks" measurably shift the output distribution — **a prompt edit is a
  deployment**.

### Software-engineering foundations (7.4%)

- Messages API is **REST returning JSON** — inherit idempotency, status-code handling, schema
  validation.
- **Async** (`AsyncAnthropic` / Promises) buys **concurrency, not lower per-request
  latency**.
- Version-control **prompts and configuration**, not just code. Put **eval suites in CI** —
  a prompt/model change fails the build like a broken test.
- **Code review must cover prompts and tool schemas** — a schema change breaks every caller,
  with no compiler to catch it.
- **Refactoring:** tighten tool descriptions, split over-broad tools, migrate
  workflow ↔ agent as requirements shift.
- **Package for reuse:** separate engagement-specific values into parameterised, documented
  config with defaults; bundle the eval suite alongside the code. (Real incident: hardcoded
  customer values → the next team had nothing to configure and no eval → rewrite.)

### RAG (D2 / D6)

- chunk → embed → similarity search → grounded prompt (`<doc id>` tags) → answer **only from
  the retrieved context** → **cite doc ids** → if not present, **say so**.
- **RAG vs long-context vs fine-tune:** retrieve when the knowledge is **large / changing /
  must be cited**. Anthropic has **no first-party embeddings API** — use Voyage (hosted) or a
  local model.

### Evaluation (D4, 2.6%)

- **Grading method — a decision tree:**
  - one correct label/value, zero ambiguity → **exact / string match** (cheap, brittle).
  - structured output (JSON / code / a numeric range) → a **code-graded check** (format,
    not content quality).
  - open-ended quality (faithfulness, tone, helpfulness) → **LLM-as-judge** — *calibrate
    against human labels first*.
- **Judge technique:** ask the judge for **strengths / weaknesses / reasoning *before* the
  score**, or it drifts to a safe ~6 regardless of quality. Use a single yes/no criterion
  where you can.
- A **golden set** runs against **every prompt or model change** — quality is measured, not
  vibed. Assert on **structure + key content, not exact wording**.

---

## DAY 5 — Model selection & optimisation · security · exam

### Model lineup & selection (D5, 16.8%)

| Tier | Context | Reasoning mode | Positioning |
|---|---|---|---|
| **Fable 5** | 1M | adaptive (always on) | most capable; long-running agents; slower |
| **Opus 5** | 1M | adaptive | complex agentic / enterprise |
| **Sonnet 5** | 1M | adaptive | **the default** speed/intelligence balance |
| **Haiku 4.5** | 200K | **extended (NOT adaptive)** | fastest / cheapest, near-frontier speed |

- **Exam-keyed selection workflow: start at Sonnet 5.** Move **up** (Opus 5, then Fable 5)
  **only when an eval shows a quality gap**. Move **down** to Haiku 4.5 **only when an eval
  shows the drop is acceptable**. (Anthropic's general dev advice — "start capable, measure
  down" — points the same way; the exam's phrasing is "start at Sonnet 5".)
- Reasoning mode is **orthogonal to model choice**. `effort`: `low` / `medium` / `high` /
  `xhigh` / `max`. `budget_tokens` is deprecated (400 on newest).

### Cost & token management (D5)

- **The five cost levers, in order of power:** **1** prompt caching (the repeated prefix) →
  **2** Batch API (anything asynchronous, ~half price) → **3** right-size the model per task
  → **4** cap output length (output tokens cost more than input) → **5** trim the fat from
  prompts.
- Read `usage` every call. Judge **cost per completed task**, not per request.
- **`input_tokens` is not "your input"** — it includes tool schemas + system + history +
  generated output.

### Prompt caching (D5)

- **Automatic** — one top-level `cache_control`; the breakpoint **slides forward**
  automatically.
- **Explicit** — `cache_control` per block; **up to 4 breakpoints per request**; a
  **20-block lookback** window; a **minimum token threshold** per block (shorter prefixes
  silently don't cache).
- **TTL:** 5-minute default, or a **1-hour** option (costs more to *write*).
- **Prefix match:** render order `tools → system → messages`; any byte change in the prefix
  invalidates everything after it. Silent invalidators: `datetime.now()` in the prompt,
  unsorted `json.dumps`, a varying tool set. Verify with `usage.cache_read_input_tokens`.
  Read ≈ 0.1× input price; write ≈ 1.25×.

### Batch API (D2 / D5)

- **Up to 100,000 requests or 256 MB per batch** (whichever hits first). Submit → poll a
  `batch_id` → results in **arbitrary order** → match with **`custom_id`**. **Up to 24 h**
  turnaround, lower per-token cost.
- **Chunking a loop over the synchronous endpoint is NOT batching** — "serialisation with
  extra steps": the API sees one request per item, same rate limits, same per-request cost.
  The Message Batches API is a **different submission model**.
- Use for: offline pipelines, evals, bulk jobs where up to 24 h latency is fine.

### Reliability (D4)

- The three places a call breaks: **before it leaves** (400/401/402/403/413 — fail fast) ·
  **in transit** (429 `rate_limit` / **529** `overloaded` / connection — back off, honour
  `retry-after`) · **after HTTP 200** (truncation / `refusal` (check `stop_details`) / wrong
  shape — validate).
- SDK auto-retries 408/409/429/5xx + connection with backoff, `max_retries` default 2.
- **Agent SDK loop-level** subtypes (`error_max_turns`, `error_max_budget_usd`,
  `error_during_execution`, `error_max_structured_output_retries`) describe **why the loop
  stopped**, distinct from why one HTTP call failed.

### Security & safety (D7, 8.1%)

- **Two threat models:**
  - **Direct injection** — your own user is the adversary. Mitigate: harmlessness screens,
    input validation, hardened system prompt, repeat-offender throttling.
  - **Indirect injection** — a trusted user, but Claude processes adversarial *third-party*
    content (a document, email, tool result). Mitigate **structurally**, in order:
    1. untrusted content **only** in `tool_result` blocks — never `system` or plain `user`
       text.
    2. **label** its nature / source.
    3. state the untrusted-content **policy** explicitly in the system prompt.
    4. **JSON-encode** untrusted strings (no delimiter breakout).
    5. **never put your own instructions inside a `tool_result`** — send them in the
       following `user` turn.
    6. **screen tool outputs** with a lightweight classifier before Claude acts.
    7. **least privilege** — bound the blast radius even if 1–6 all fail.
- **No single guardrail is sufficient — defense-in-depth.** Never a substitute for input
  validation, least-privilege tool scopes, or human approval on destructive actions.
- **Hooks are the deterministic layer:** a `PreToolUse` hook can deny a dangerous call
  outright, enforcing **even under `bypassPermissions` — but only if it exits with code 2**
  (exit 1 only warns). Keep hooks fast (synchronous).
- **Identity & keys:** the key is shown **once** at creation (`sk-ant-…`) — capture it to a
  secrets manager immediately. **Prefer short-lived federated credentials** (Workload
  Identity Federation — exchange a platform OIDC token for a short-lived Anthropic token)
  over long-lived static keys. Rotate periodically; revoke on suspected leak. A key in a
  **client** (mobile app) → a **backend proxy**, no exceptions.
- Isolation discipline applies at **every seam**, not just the outer boundary — overall
  containment is bounded by the single most-privileged component.

### Exam-day method — see `logistics/05-exam-method.md` and
`day5-.../mock-exam/exam-day-strategy.md`.

---

## Sources

Cross-checked against the CCDV-F official exam guide and these public study repos (checked
2026; content and the guide both move — verify against the current official guide):

- **AndyMDH/claude_developer_foundations** — per-domain summaries, cheat sheet, flashcards,
  topic summaries, practice questions. The densest of the three; most of the sharper facts
  above (image-token formula, 529 vs 503, batch 100k/256MB/24h, the four-way tool framework,
  settings precedence, six permission modes, deployment surfaces, regulated-data routes,
  adaptive-vs-extended thinking, the judge-before-score technique) are corroborated here.
- **sumitgupta28/Claude-Certified-Developer-Foundations-Certification** — module notes
  (`M1 — MSO Foundations`): non-determinism, zero/one/multi-shot, batch-vs-sync, the
  context-window failure modes, property assertions vs exact-string.
- **ashokgows/claude-certified-developer-foundations** — `STUDY_NOTES.md`: Pearson VUE
  logistics, M1/M2 lesson maps, the "levers" exam instinct.
- **pjmgomez/claude-certified-developer-foundations** — 37 lesson HTML pages + 14 reference
  sheets, same topic taxonomy (mined for structure).
- Video companions: `Lan-CbQ2IKM` (walkthrough), `zEH83eIU5-0` (blueprint guide),
  `RheXq2HKJmY` (build-along Ep 01). See `video-companion.md`.
