# Day 5 mock exam — blueprint

> **Status: blueprint.** `mock-exam-A.md` (the 53 items) + `mock-exam-A-key.md` +
> `exam-day-strategy.md` are written in build pass 3, drawn from `question-bank/`.

## Format (mirrors the real CCDV-F)

- **53 items**, multiple-choice **and** multiple-response (each item states how many to
  select).
- **90 minutes** timed (real exam is 120 for 53 — the tighter clock builds margin).
- No notes, no IDE. Individual, not tables.
- Immediately followed by **45 min review** — every item walked through the four-step attack
  from `../../logistics/05-exam-method.md`.

## Item allocation (by domain weight → count of 53)

| Domain | Weight | Items | Sub-area emphasis |
|---|---:|---:|---|
| D1 Agents and Workflows | 14.7% | **8** | four-ways-to-build · workflow vs agent · subagents · patterns |
| D2 Applications and Integration | 33.1% | **17** | 6 API mechanics · 4 application design · 3 SW-eng foundations · 2 requirements · 1 systems life cycle · 1 config mgmt |
| D3 Claude Code | 3.1% | **2** | project-config hierarchy · headless mode |
| D4 Eval, Testing, and Debugging | 2.6% | **2** | debugging the 3 failure points · regression testing |
| D5 Model Selection and Optimisation | 16.8% | **9** | 3 LLM/technical fundamentals · 2 model trade-offs · 4 cost & token mgmt (caching, batch, order) |
| D6 Prompt and Context Engineering | 11% | **6** | 2 context engineering · 3 prompt engineering · 1 output handling |
| D7 Security and Safety | 8.1% | **4** | 2 AI-app security (injection) · 1 guardrails/deploy · 1 secrets/keys (hooks folded into D1/D7 items) |
| D8 Tools and MCPs | 10.6% | **5** | 2 tool implementation · 1 MCP server dev · 2 agentic customisation |
| **Total** | **100%** | **53** | |

*(Re-derive these counts against the current official guide before each cohort. If a weight
moves > 2 points, re-allocate.)*

## Style mix (of the 53)

| Style | ~count |
|---|---:|
| Single best answer (SBA) | 30 |
| Multiple response (MR — "select two/three") | 12 |
| Scenario / next-step (SCN) | 8 |
| Predict output / spot the bug (OUT/BUG) | 3 |

## Passing bar used in class

Scaled 720/1000 on the real exam ≈ **~72–75% raw**. Class target: **≥ 73% overall AND no
domain < 60%.** Below that, the roster names the weak domain(s) → revision plan.

## Review protocol (the 45 min)

1. Score sheets swapped or self-marked against `mock-exam-A-key.md`.
2. Trainer projects each **missed-by-many** item. Class runs the four-step attack aloud:
   name the decision → constraint word → Rule 1/2 → mechanism.
3. For each item, name the **distractor bucket** every wrong option fell in (stale API /
   generic knob / guidance-as-control / right-word-wrong-place / wrong system).
4. Candidates log per-domain % on the roster and circle their weakest two domains.

## After

Each candidate leaves with: their per-domain %, a revision plan (weak domains →
`question-bank/domain-N-*.md` + anchor episodes + `video-companion.md` lessons), and the
advice to re-sit this mock the day before booking, and to book within 2–3 weeks.
