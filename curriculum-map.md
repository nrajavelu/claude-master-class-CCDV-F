# Curriculum map — every "Claude way" component, across all 5 days

> One row per building block Anthropic's docs / the `claude-api` skill treat as a first-class
> concept. Shows **where it's taught**, the **episode / doc it's drawn from**, the **runnable
> reference**, the **practice**, and the **exam domain**. Use it as a coverage checklist —
> if a cohort is weak somewhere, this is the map back to the material.
>
> `D1M5` = Day 1, Module 5. `L10` = video companion lesson 10. `ep06` = parent-repo episode.
> `qb:D6` = `question-bank/domain-6-*.md`. `cs:x` = `code-snippets/x.py`.

---

## Decision ② — how does it call Claude? (API mechanics · model/cost)

| Component | Taught | Source | Runnable | Practice | Exam |
|---|---|---|---|---|---|
| Messages API shape · roles · content blocks | D1M1 | `ep01` · L2 · `claude-api/README.md` | `cs:messages_basics` · Lab 1 | `qb:D2` (28) · practice d1-01..02 | D2 |
| `stop_reason` — all values, branching | D1M1 · D5M5 | `ep01` · L2 | `cs:messages_basics` · `cs:agent_loop_react` | practice d1-03 · quiz Q1 | D2·D4 |
| `usage` · input vs output pricing | D1M1 · D5M2 | `ep01` · L10 | `cs:count_tokens` | qb:D5 | D5 |
| System prompt (the `system` field) · no `role:"system"` message | D1M2 · D2M2 | `ep01` · `ep05` · L5 | `cs:prompt_structure` | practice d1-05 · d1-16 | D6·D2 |
| Streaming — SSE (not WebSocket) · `get_final_message()` · mid-stream errors | D1M3 | `ep01` · L3 · `claude-api/streaming.md` | `cs:streaming` · Lab 2 | practice d1-07..08 | D2 |
| Statelessness · multi-turn = resend history | D1M1 | `ep01` · L2 | `cs:messages_basics` | practice d1-20 | D2 |
| Token counting (`count_tokens`) | D1M5 · D5M2 | L10 · `shared/token-counting.md` | `cs:count_tokens` · Lab 3 | practice d1-15 | D5 |
| Model family · tiers · "start capable, measure, step down" | D1M1 · **D5M1** | `ep10` · L… | — | qb:D5 | D5 |
| `effort` levels (low→max, xhigh) | D1M2 · D5M1 | `claude-api` QR | `cs:cot_structured` | qb:D5 | D5 |
| Prompt caching · prefix rules · invalidators | **D5M3** | `ep11` · `shared/prompt-caching.md` | `cs:prompt_caching` · D5 Lab | practice d1-18 · qb:D5 | D5 |
| Message Batches · any-order · `custom_id` | **D5M4** | `ep11` · L11 | `cs:batch_custom_id` · D5 Lab | qb:D5 · scenario Q1 | D2·D5 |
| Cost-optimisation order (caching→hygiene→batch→…) | D5M2 | `shared/cost-optimization.md` · L10 | — | scenario Q9 | D5 |
| Error handling — typed exception chain · retry vs fail-fast | D1M4 | L9 · `shared/error-codes.md` | `cs:retry_chain` · Lab 3 | practice d1-09..10 | D4 |
| SDK built-in retries · timeouts · `with_options` | D1M4 | `claude-api` QR | `cs:retry_chain` | practice d1-10 | D4 |
| `rate_limit` vs `overloaded` | D1M4 · D5M5 | L3 · L9 | — | qb:D4 | D4 |
| `refusal` · `stop_details` · fallbacks | D1M1 · D5M5 | `claude-api` QR | — | practice d1-11 | D4·D5 |
| Vision / image input · token cost · "send the text" | **D5M6** | `ep03`-video · L3 | — | qb:D5 | D2·D5 |
| PDF / document input · billed as text + page images · citations | D5M6 | L3 · `claude-api` QR | — | qb:D5 | D2·D5 |

## Decision ③ — what does Claude see & say? (prompting · context · output)

| Component | Taught | Source | Runnable | Practice | Exam |
|---|---|---|---|---|---|
| Prompt engineering — explicit · XML structure · zero/one/multi-shot | D1M2 · D2M1 | `ep01` · `ep07` · L5·L7 | `cs:prompt_structure` | `exercises.md` B · practice d1-17 | D6 |
| **Chain-of-Thought** — zero-shot / structured / few-shot | **D1M2** | `reasoning-patterns.md` · L5 | `cs:cot_structured` | qb:D6 | D6 |
| **Adaptive / extended thinking** = Claude's native CoT · `thinking` block · **`budget_tokens` is stale** | D1M2 | `reasoning-patterns.md` · `ep03`-video (L3) | `cs:cot_structured` | practice d1-06 · quiz Q6 | D6·D5 |
| Interleaved thinking (think between tool calls) | D3M3 | `reasoning-patterns.md` §3 | — | qb:D6 | D1·D6 |
| The three surfaces · what transfers | D2M2 | `ep05` (video L5) | — | qb:D6 · qb:D2 | D2·D6 |
| Untrusted content · `tool_result` is the channel (both ways) | D2M3 · D5M7 | `ep04`/`ep05` hooks · L5·L16 | `cs:blocking_hook` | qb:D7 | D6·D7 |
| Structured output · `strict:true` · `additionalProperties:false` · null-for-optional · `messages.parse()` | **D2M5** | `ep07` · L7 · `claude-api` QR | `cs:strict_tool` · D2 Lab 3 | practice (d2) · qb:D2 | D2 |
| Validation layer ("asking is not making sure") | D2M5 | `ep07/schemas.py` | `cs:strict_tool` | qb:D2 | D2·D4 |
| Context window contents (input + tools + history + output) | **D4M5** | `ep06` · L8·L10 | — | qb:D6 | D6 |
| Compaction vs context-editing vs memory tool | D4M5 | `ep06` (`context_check.py`) · L8 · `claude-api` QRs | — | qb:D6 · practice (d4) | D6 |
| Sessions · `resume` · `fork_session` · the cwd trap | D4M4 | `ep06` (`session_index.py`) | — | qb:D3·D6 | D2·D6 |
| Skills / Agent Skills (`.claude/skills/*/SKILL.md`) | D3M5 · D4M4 | `ep08` | — | qb:D3·D8 | D3·D8 |

## Decision ① — what runs? (agents · tools · MCP)

| Component | Taught | Source | Runnable | Practice | Exam |
|---|---|---|---|---|---|
| Should you build an agent? (complexity/value/viability/cost-of-error) | D3M1 | L14 · `shared/agent-design.md` | — | practice (d3) · qb:D1 | D1 |
| **The agentic loop / ReAct** — Thought → Action → Observation · the two rules | **D1M5** · D3M2 | `ep01` · `reasoning-patterns.md` · Build-along Ep 01 | `cs:agent_loop_react` · **Lab 4** | practice d1-12..14 · quiz Q11..12 | D1 |
| Four ways to build an agent (harness × deployment) | D3M2 | `claude-api` "Building an Agent" · L… | — | qb:D1 | D1 |
| Tool Runner (`@beta_tool` / `betaZodTool`) | D3M2 | `claude-api` QR | — | qb:D1 | D1 |
| Claude Agent SDK (`query` / `ClaudeSDKClient`) | D3M3 | `ep02` | `cs:blocking_hook` | qb:D1 | D1 |
| Custom tools · **the description is the interface** · `tool_choice` · parallel · `is_error` | D2M4 | `ep03` · L12 | `cs:strict_tool` · D2 Lab 2 | qb:D8 | D8 |
| Hooks lifecycle — PreToolUse (deny) · PostToolUse (taint) · Stop · PreCompact | **D3M3** | `ep04`/`ep05`/`ep06` hooks · Build-along Ep 04 | `cs:blocking_hook` · D3 Lab 2 | qb:D7·D8 | D7·D8 |
| Subagents · fan-out · scoping · "usually fewer" | D3M4 | `ep05/subagents.py` · L14 | — | D3 Lab 1 · qb:D1 | D1 |
| MCP — protocol · `.mcp.json` stdio/http/sse · scope the toolset | **D3M6** | `ep09` · L13 | `cs:mcp_server` · D3 Lab 4 | qb:D8 | D8 |
| Building an MCP server (FastMCP, stdio) | D3M6 | `ep09/repo_facts_server.py` | `cs:mcp_server` | qb:D8 | D8 |
| Plugins = code with your privileges (trust) | D3M6 | L5 (video) | — | qb:D7·D8 | D7·D8 |
| Managed Agents (harness + deployment by Anthropic) | D3M2 · D5 | `ep12` · `shared/managed-agents-*` | — | qb:D1 | D1 |
| Claude Code operation — rules · skills · commands · project-config hierarchy · headless | **D3M5** | `ep06/CLAUDE.md` · `ep08/.claude/` · L6 | — | D3 Lab 3 · qb:D3 | D3 |

## Decision ④ — will it survive production? (SWE · debugging · security)

| Component | Taught | Source | Runnable | Practice | Exam |
|---|---|---|---|---|---|
| Requirements — functional vs infrastructure | **D4M1** | L4 | — | D4 Lab 1 · qb:D2 | D2 |
| Systems life cycle — develop/implement/operate/maintain ("implement" = deploy) | D4M2 | L4 | — | qb:D2 · scenario Q14 | D2 |
| SW-eng foundations — VCS · review · pipeline · refactoring | D4M3 | L4 | — | qb:D2 | D2 |
| Application design — surface · output shape · session hygiene | D4M4 | `ep05`·`ep06` · L5·L8 | — | qb:D2 | D2 |
| **Configuration management** — pin the model · commit rules · config hierarchy · secrets out | **D4M4** | `ep06` · L6 | — | D4 Lab 2 · scenario Q7 | D2·D7 |
| Evaluation — eval set · assertion vs keyword vs **LLM-as-judge** · regression tests | **D4M7** | L9 · `shared/*` | — | D4 Lab 4 · qb:D4 | D4 |
| Debugging — the three places a call can break | D1M4 · D5M5 | L9 | `cs:retry_chain` | qb:D4 | D4 |
| RAG — chunk · embed · similarity · ground · **cite** · RAG vs long-context vs fine-tune | **D4M6** | L8 · `shared/*` | — | D4 Lab 3 · qb:D2·D6 | D2·D6 |
| Embeddings (Voyage / local; no first-party API) | D4M6 | `logistics/01` | — | — | D2 |
| Prompt injection — "the attack arrives as a ticket" · **guidance vs mechanism** | D2M3 · **D5M7** | `ep04`/`ep05` · L16 · guide sample Q | `cs:blocking_hook` | scenario Q2 · qb:D7 | D7 |
| Guardrails & safe deployment · fail-closed · human-in-the-loop | D5M7 | `ep04` · L15·L16 | `cs:blocking_hook` | qb:D7 | D7 |
| Identity, secrets & key management · least privilege · `${VAR}` expansion · self-hosted ≠ air-gapped | **D5M7** | `ep09/.mcp.json` · L15 | `cs:mcp_server` | D5 Lab 4 · qb:D7 | D7 |

## The method (all decisions)

| Component | Taught | Source | Practice |
|---|---|---|---|
| Four decisions + two elimination rules | **D1M0** | `logistics/05-exam-method.md` · L1·L17 | every `exam-style-questions.md` · `scenario-questions.md` |
| Distractor buckets (stale-API · generic-knob · guidance · wrong-system) | D1M0 | `logistics/05 §4` | practice rationales |
| Exam-day routine (pacing, read-last-line-first) | **D5M8** | `logistics/05 §6` · L17 | Day 5 mock review |

---

## Gaps / lighter coverage (deliberate — note for the trainer)

| Topic | Status |
|---|---|
| Server tools (web search / fetch / code execution) | **mentioned** (D5M7 self-hosted note); not a lab. Low exam weight; expand if a cohort asks. |
| Files API | mentioned (RAG lab uses local files). Not drilled. |
| Fine-tuning | contrasted with RAG (D4M6); not built (out of Foundations scope). |
| Tree-of-Thought / Reflexion / self-consistency | named in `reasoning-patterns.md §4`; recognition only. |
| Priority Tier / Fast mode / provider clients (Bedrock/Vertex/Foundry) | out of Foundations scope; one line in D5 if asked. |

> **Reconcile this map against the official CCDV-F exam guide before each cohort** (see
> `logistics/03`). If a component's weight moves, adjust which day emphasises it.
