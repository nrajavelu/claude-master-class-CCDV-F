# Mock exam A — answer key

`n. ANSWER — domain — one-line why [· distractor species]`. Species: **OB** overbuild ·
**ST** symptom-treater · **EX** extremist · **TBI** true-but-irrelevant · **SA** stale-API ·
**RWP** right-word-wrong-place · **WS** wrong-system.

| # | Ans | Domain | Why |
|---|---|---|---|
| 1 | C | D2 API Mechanics | token counting is its own endpoint; tools/vision/thinking are parameters |
| 2 | B | D2 | a list of typed blocks — check `block.type` |
| 3 | A, C | D2 | `tool_call`/`content_filter` are WS; `token_limit` invented |
| 4 | B | D2 | stream + more room. A retries into the same truncation; C incomplete; D truncates earlier |
| 5 | B | D2 | no server session; resend history each call |
| 6 | A | D2 | `model`/`system`/`messages`/`tools` — no `max_tokens` or sampling params |
| 7 | B | D2 | `get_final_message()` rebuilds the whole Message. D re-bills |
| 8 | B | D5 Technical Fundamentals | SSE over the same call. A is WS |
| 9 | A, C, E | D4 | transient = 429 / ≥500 / connection. 401 & 400 are caller errors |
| 10 | C | D4 | 408/409/429/5xx + connection, `max_retries=2` |
| 11 | B | D4 | `rate_limit` = your spike; `overloaded` = their load |
| 12 | B | D4 | HTTP 200, no exception; check `stop_reason` (+ `stop_details`) first |
| 13 | B | D4/D2 | evidence first, smallest fix. D = **OB**; A/C treat a non-cause |
| 14 | B | D1 Agent Construction | append the whole content list — stateless API needs full alternation |
| 15 | B | D1 | one user message, list of `tool_result` blocks, ids matching |
| 16 | B | D1 / D6 | CoT = one turn; ReAct = a loop with tool results fed back |
| 17 | B | D6 Prompt Eng | "CoT always helps" is false — costs latency, no gain on fixed-set classification |
| 18 | C | D6 / D5 | `budget_tokens` removed on current models (**SA**); use adaptive + `effort` |
| 19 | B | D1 Agents & Workflows | fixed path → workflow. A = **OB**; C = **EX**; D = **OB + TBI** |
| 20 | A, C | D1 | B/D describe an *agent's* strengths |
| 21 | A | D1 Agent Patterns | the five real workflow patterns |
| 22 | B | D1 | loop guardrails. A = **OB**; C/D generic knobs |
| 23 | B | D1 | Tool Runner = harness only, your tools, you host, per-turn hooks |
| 24 | D | D1 | only Managed Agents adds managed deployment |
| 25 | A, C | D1 | B false (coordination overhead); D false |
| 26 | C | D1 Agent Architecture | single-step, fully specifiable → no loop |
| 27 | B | D2 App Design / surfaces | the surface differs; A/C are generic knobs; D is **RWP** |
| 28 | B | D6 | durable, every-turn contract. C = **SA** (prefill); D = **WS** |
| 29 | B, D | D6 Output Handling | example + structure. A = **ST/ceremony**; C backwards |
| 30 | B | D7 / D6 | `tool_result` is the untrusted channel — and your instructions never go there |
| 31 | B | D6 | rejected on newest models; `output_config.format` replaces it (exam still references prefilling) |
| 32 | B | D2 Structured output | `strict` has no "optional" — nullable type; `additionalProperties` stays false |
| 33 | B | D2 | rejected, not ignored |
| 34 | B | D2 / D6 | guarantee the shape **and** fail safely. A = **ST**; C = **EX**; D = **TBI** with a price tag |
| 35 | B | D2 | validates against your schema; typed object or raise |
| 36 | A, D | D6 Context Eng | window = input + tool schemas + history + output (all billed) |
| 37 | B | D6 | summarise vs clear; memory tool is a third option |
| 38 | B | D6 | clear the stale context. A = **OB/knob**; C/D generic knobs |
| 39 | B | D6 / D2 (RAG) | retrieve when large / changing / must be cited. A/C = **EX** |
| 40 | B | D6 (RAG) | grounding + citation is the mechanism. A/C over-reach; D backwards |
| 41 | B | D4 | test the contract; wording varies by design |
| 42 | B | D4 | a crisp yes/no criterion is repeatable |
| 43 | B | D2 Requirements | infrastructure = what it runs on **and** what the team must do to it |
| 44 | B | D2 Systems Life Cycle | deploy where users are; credit in operate + maintain |
| 45 | C | D2 Configuration Management | pin + commit = mechanism. A = **OB**; B = **ST**; D = the cause |
| 46 | B | D7 Identity/Secrets | keys server-side only. A/C/D = **ST** (still shipped/leaks the same) |
| 47 | B | D2 App Design | an API endpoint needs its own timeout + error contract |
| 48 | A, C | D2 / D5 Cost | overnight → batch; repeated prefix → cache. B backwards; D = **ST** |
| 49 | B | D5 Cost & Token Mgmt | any order — key by `custom_id` |
| 50 | B | D5 Model Selection | fast tier + cascade the hard cases up. C = cost blowout |
| 51 | B | D5 Technical Fundamentals | streaming → perceived latency; batch → cost; neither → intelligence |
| 52 | B | D5 Cost | any byte change in the prefix invalidates everything after it |
| 53 | A, B | D7 AI App Security | least privilege + validate outputs. C = **ST/guidance**; D = **EX** |

---

## Per-domain tally (fill after marking)

| Domain | Items | Your right | % |
|---|---:|---:|---:|
| D1 Agents & Workflows | 19–26 (8) | | |
| D2 Applications & Integration | 1–7, 27, 30, 32–35, 43–48 (17) | | |
| D3 Claude Code | *(folded into D1/D2 items 23–24, 45)* | | |
| D4 Eval, Testing, Debugging | 9–13, 41–42 (7, overlaps D2) | | |
| D5 Model Selection & Optimisation | 8, 18, 36, 48–52 (9) | | |
| D6 Prompt & Context Engineering | 16–17, 28–29, 31, 36–40 (mix) | | |
| D7 Security & Safety | 30, 46, 53 (+ 45 config) | | |
| D8 Tools & MCPs | 15, 21, 23, 25, 32 *(scoring/desc/scoping)* | | |
| **Overall** | **53** | | |

> Item↔domain mapping is approximate (many items span two sub-areas — that's real). **Pass
> bar in class: ≥ 73% overall AND no domain < 60%.** Below that, the 4-week plan
> (`../../logistics/03 §8`) with your weak domains circled.
