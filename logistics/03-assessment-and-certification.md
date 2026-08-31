# Assessment & certification guide

> **What this is:** how the bootcamp measures readiness, and the **CCDV-F exam blueprint**
> the course is built to cover — in full, and in proportion.
>
> **Health warning:** Anthropic revises the official exam guide. The domains, sub-weights and
> format below reflect the published **Claude Certified Developer – Foundations (CCDV-F)**
> blueprint as of 2026 (cross-checked against public exam-guide summaries). **Before every
> cohort**, pull the current official guide, diff it, and re-weight `question-bank/` and the
> Day 5 mock. Official guide wins any conflict.
>
> **Read `05-exam-method.md` alongside this file.** This file is *what* is on the exam;
> `05` is *how to answer it* (the four decisions + two elimination rules) — the spine the
> whole week is taught on.

---

## 1. Exam facts (confirm against the official guide each cohort)

| | Value |
|---|---|
| Items | **53** |
| Question types | multiple-choice **and** multiple-response; each item states how many to select |
| Time | **120 minutes** |
| Passing score | **scaled 720** on a 100–1000 scale |
| Cost | **US $125 / attempt** |
| Credential validity | 12 months |
| Stated audience | AI engineers/developers, 1–5 yrs experience, **6+ months hands-on Claude**, Python/TypeScript + REST/CLI fluency |

> Our cohort baseline ("some coding, new to Python & LLMs") is **below** the exam's stated
> audience. This bootcamp is a *compression* of that 6-months-hands-on expectation into an
> intensive week + Day 0 pre-work + a revision plan. Set that expectation with candidates:
> the week makes them exam-*ready-to-prepare*; most will want 1–3 weeks of the supplied
> practice before booking.

---

## 2. The 8 domains, sub-weights, and where the bootcamp covers them

| # | Domain | Weight | Sub-areas (weight) | Bootcamp |
|---|---|---:|---|---|
| **D1** | **Agents and Workflows** | **14.7%** | Agent Architecture (4.5%) · Agent Construction with Claude (5.3%) · Agent Patterns & Frameworks (4.9%) | Day 1 (loop primitive) · **Day 3** (SDK, subagents, patterns) |
| **D2** | **Applications and Integration** | **33.1%** | Understanding Requirements (3.4%) · Systems Life Cycle (2.8%) · Claude API Mechanics (6.8%) · Software Engineering Foundations (7.4%) · Claude Application Design (8.6%) · Configuration Management (4.1%) | **Day 1** (API mechanics) · **Day 2** (structured output, output handling) · **Day 4** (requirements → design → SDLC → config mgmt → RAG) |
| **D3** | **Claude Code** | **3.1%** | Claude Code Operation (3.1%) | **Day 3** (rules, skills, commands, memory, project-config hierarchy, headless/stream/auto modes) |
| **D4** | **Eval, Testing, and Debugging** | **2.6%** | Debugging & Error Handling (2.6%) | **Day 1** (typed errors, retries) · **Day 4** (eval harness) · Day 5 (wrap) |
| **D5** | **Model Selection and Optimisation** | **16.8%** | LLM Fundamentals (5.2%) · Technical Fundamentals (6.1%) · Model Selection & Trade-offs (2.7%) · Cost & Token Management (2.8%) | **Day 1** (LLM/technical fundamentals, tokens, cost math) · **Day 5** (selection, caching, batch, cost-optimisation order, usage tracking) |
| **D6** | **Prompt and Context Engineering** | **11%** | Context Engineering (3.8%) · Prompt Engineering (4.6%) · Output Handling (2.6%) | **Day 2** (prompt + output handling) · **Day 4** (context engineering, memory) |
| **D7** | **Security and Safety** | **8.1%** | AI Application Security (3.2%) · Guardrails & Safe Deployment (2.3%) · Claude Hooks (1%) · Identity, Secrets & Key Management (1.6%) | **Day 3** (hooks, guardrails) · **Day 5** (app security, secrets/key management, safe deploy) |
| **D8** | **Tools and MCPs** | **10.6%** | Tool Implementation (4.4%) · MCP Server Development (2.1%) · Agentic Customisation (4.1%) | **Day 2** (tool implementation) · **Day 3** (MCP server, agentic customisation) |

**Coverage check:** every domain and every sub-area above is taught *and* practised (lab or
exercise) *and* drilled (`question-bank/`). D2 is a third of the exam, so it spans three
days; D3/D4 are small, so they're modules, not days.

### Where a generic practice-test course is weak — and we are not

| Gap in typical CCDV-F prep | What this bootcamp does instead |
|---|---|
| Practice questions only; no hands-on | 20+ runnable labs on the candidate's own key |
| "API mechanics" taught, "Application Design / SDLC / Config Management" glossed | **Day 4** is a full day on D2's design/lifecycle/config sub-areas — requirements, design patterns, environment config, versioning |
| Claude Code mentioned, not operated | **Day 3** operates Claude Code: rules, skills, commands, memory, project-config hierarchy, headless mode |
| Security = "don't leak keys" | **Day 5** covers AI-app security (prompt injection, tool-output trust), guardrails, **and** identity/secrets/key management as its own topic |
| Cost = "use Haiku" | **Day 5** teaches the **cost-optimisation order** (caching → input hygiene → batch → budgets → effort → model), with `count_tokens` and usage tracking done in code |
| One flat question pool | questions tagged to **sub-area**, so a weak-area score points at an exact lab + episode |

---

## 3. Question styles the exam uses (and we drill)

| Style | Stem shape | Practised in |
|---|---|---|
| **Single best answer** | "Which field indicates Claude wants a tool run?" | every `quiz.md` |
| **Multiple response** ("select two/three") | "Which are valid `stop_reason` values?" | `exam-style-questions.md` |
| **Scenario / next-step** | "`stop_reason` is `tool_use`, `content[0]` is text — do what?" | `exam-style-questions.md`, `scenario-questions.md` |
| **Predict output / behaviour** | "2nd identical call — what's `cache_read_input_tokens`?" | Day 5 |
| **Spot the bug** | "This `tool_result` is in an assistant message — what breaks?" | Days 2–4 |
| **Best-practice judgement** | "Cheapest way to cut a repeated 12 KB system prompt?" | Day 5 |

**Distractor patterns we teach candidates to expect:** (1) **stale API** — `budget_tokens`,
`output_format`, assistant prefill, `claude-code-sdk`; (2) **right but not best** —
hand-rolled retry vs `max_retries`; (3) **plausible-but-backwards** — volatile content before
the cache breakpoint; (4) **wrong system** — `function_call`, `content_filter` (OpenAI-isms).

---

## 4. Formative vs summative

| | Formative (during the week) | Summative (exam readiness) |
|---|---|---|
| Instrument | daily labs + end-of-day `quiz.md` | per-day `exam-style-questions.md` + **Day 5 53-item timed mock** |
| Class pass bar | 70% quiz to move on comfortably | **scaled ≥ 720 equivalent (~72–75% raw)** on the mock, **and** no domain < 60% |
| Purpose | "did today land?" — adjust pace | "would this person pass?" — plan revision |

---

## 5. Per-candidate readiness scorecard

Trainer maintains one row per candidate (template in `04-cohort-runbook.md`), scored by
**sub-area** where possible:

| Domain / sub-area | Day-quiz % | Exam-style % | Mock % | Ready? |
|---|---|---|---|---|
| D2 · Claude API Mechanics | | | | ≥70 all three |
| D2 · Application Design | | | | |
| D5 · Technical Fundamentals | | | | |
| … | | | | |

**Exam-ready** = mock overall ≥ ~73% **and** every domain ≥ 60%. Below that, the scorecard
names the weak sub-area → point them at the matching `question-bank/domain-N-*.md` section,
the lab, and the anchor episode.

---

## 6. Exam-day strategy (taught in the Day 5 wrap)

- **~135 sec/item** (53 items / 120 min, with review time). Flag-and-move past anything over
  2.5 min.
- **Read the last sentence of the stem first** — it says "best", "select two", or "will
  NOT".
- **Kill the stale-API distractor** before evaluating the rest.
- **"Best" questions:** if two options both work, pick the cheaper / simpler / SDK-native
  one — usually the keyed answer.
- **Scenario questions:** the answer is usually "correctly handle the state you're in", not
  "change the request".
- **Multiple-response:** the item tells you how many — select exactly that many.
- Full pass, then flags. No blanks (no negative marking).

---

## 7. After the bootcamp

Each candidate leaves with: their sub-area scorecard; a revision plan (weakest 2–3
sub-areas → `question-bank/` sections + anchor episodes + relevant `shared/` docs from the
`claude-api` skill); and the advice to **re-sit the Day 5 mock the day before** and **book
within 2–3 weeks** while it's fresh.
