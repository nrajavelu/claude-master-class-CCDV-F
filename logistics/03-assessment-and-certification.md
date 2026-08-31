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
| Time | **120 minutes** (~2 min 15 s / item — the most generous of the four exams) |
| Passing score | **scaled 720** on a 100–1000 scale (not a percentage — don't convert). Report shows pass/fail, scaled score, **and % correct per domain** — a miss still hands you a map. |
| Cost | **US $125 / attempt** |
| Proctoring | Pearson VUE, online **or** test centre; identity verified before the clock starts |
| Registration path | Claude Partner Network → Partner Academy → Pearson VUE |
| Credential validity | 12 months · **free on-time renewal** via a lighter non-proctored assessment · full fee again if it lapses |
| Retake ladder | **14 days → 30 → 90**; **4 attempts per rolling year** — a miss is a delay, not a verdict |
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

## 7. Five ways candidates fail (warn them on Day 1)

1. **Study by affection, not by weight.** Claude Code gets a weekend and is worth **3.1%**;
   Configuration Management feels boring and is worth *more than Claude Code + Debugging
   combined*. The blueprint is a price list — spend accordingly.
2. **Over-study prompting.** It's **11%**, and the most seductive trap on the paper.
3. **Agent-everything brain.** If your default answer is "an autonomous agent", the
   **overbuild** distractor feeds on you all afternoon. The exam rewards the simplest
   sufficient structure.
4. **Prepare without an API key.** This paper is written from the builder's chair.
   Candidates who only *read* about caching, stop reasons and tool schemas lose points to
   those who *watched them happen in a terminal* — which is why every day has runnable labs.
5. **Dumps.** A rules violation stapled to wrong answers; the scenarios punish memorisation
   anyway (they test reasoning about a system you've never seen).

## 8. Post-course revision — the 4-week build plan

Hand this to every candidate. **5–6 focused hours/week** (6 weeks if newer to the API). The
organising idea: **ship one small thing and let it drag you through the blueprint** — a
little **support assistant**: an API integration with **two tools (a lookup + an action)**, a
system prompt, and a cost budget. Trivial in scope, complete in structure, touches every
heavyweight domain.

| Week | Build | Blueprint it earns |
|---|---|---|
| **1 · foundations + the API** | rate yourself on all 8 domains; set up key + repo; build the plain conversation loop (messages, system, streaming); then **deliberately break it** — hit the token cap and read `stop_reason`, trip the rate limit and write the backoff | D2 (API mechanics) · D4 (debugging) |
| **2 · the heavyweights** | add the two tools; watch the model choose them; **sabotage your own tool descriptions** and watch it misroute; add caching to the system prefix and check `usage` before/after; price the assistant at 3 tiers and pick deliberately | D2 (33%) · D5 (16.8%) · D8 |
| **3 · the judgement domains** | convert one flow into a **routed workflow** and argue out loud why it shouldn't be an autonomous agent; **paste an injection** into a fake customer message and fix the design (structure · least privilege · output validation); skim Claude Code essentials — one honest session | D1 · D7 · D3 |
| **4 · rehearsal** | re-read the guide as a checklist ("can I do this in code?"); timed practice; weakest domain gets the final hours; **book the exam while the project is fresh — your recent commits are the best flashcards** | all |

## 9. Free study stack (the fee is the only mandatory cost)

1. The **official exam guide** (25 weighted sub-skills — your syllabus *and* your final
   checklist). Download the current version from the Partner Academy **before booking**.
2. The **official documentation** — for this exam it outranks any course (API reference,
   tool-use guide, agent guidance). The exam is built from the same well.
3. **Anthropic Academy** developer courses — free, self-paced.
4. **A working project** — an API key, a scratch repo, and code you actually ran.

## 10. After the bootcamp

Each candidate leaves with: their sub-area scorecard; the 4-week plan above with their weak
domains circled; a revision list (`question-bank/` sections + anchor episodes +
`code-snippets/`); and the advice to **re-sit the Day 5 mock the day before** and **book
within 2–3 weeks** while it's fresh.
