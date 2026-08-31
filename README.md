# Aizentify — Claude Certified Developer: Foundations (CCDV-F)
### 5-Day Instructor-Led Crash Course

> *Identify what matters. Intelligently transform how you work.*
> An Aizentify exclusive training program. © 2026 Aizentify LLP.

---

## What this is

A five-day, hands-on crash course that takes a working developer — new to Python and new to
LLMs — toward the **Claude Certified Developer – Foundations (CCDV-F)** exam.

It is built *around* the public `claude-api-masterclass` build-along (episodes `ep01`–`ep12`
in the parent folder), used **read-only** as a running case study, and it covers **all 8
CCDV-F exam domains in proportion to their weight** — with runnable labs, exercises, and
a certification-style question bank tagged to exam sub-areas.

**Nothing in `ep01`–`ep12` or the repo root is modified.** Everything new lives in this
folder.

---

## Who it is for

| Audience | Fit |
|---|---|
| Developers who read code in *some* language, new to Python | ✅ (Day 0 primer) |
| Developers new to LLMs / the Claude API | ✅ |
| Never used a terminal or git | ⚠️ Do Day 0 with extra time |
| Non-programmers | ❌ |

The **CCDV-F exam's own stated audience** is 1–5 yrs experience with **6+ months hands-on
Claude**. This bootcamp compresses that runway into an intensive week plus a supplied
revision plan — most candidates will want 1–3 weeks of practice before booking. See
`logistics/03-assessment-and-certification.md`.

Cohort size: **6–16** + 1 trainer (+ 1 assistant at 12+).

---

## The exam this prepares you for

**CCDV-F** — 53 items · multiple-choice & multiple-response · 120 min · scaled pass 720/1000
· US $125/attempt · valid 12 months. Eight domains:

| # | Domain | Weight | Day(s) |
|---|---|---:|---|
| D1 | Agents and Workflows | 14.7% | 1, **3** |
| D2 | Applications and Integration | **33.1%** | 1, 2, **4** |
| D3 | Claude Code | 3.1% | 3 |
| D4 | Eval, Testing, and Debugging | 2.6% | 1, 4 |
| D5 | Model Selection and Optimisation | 16.8% | 1, **5** |
| D6 | Prompt and Context Engineering | 11% | **2**, 4 |
| D7 | Security and Safety | 8.1% | 3, **5** |
| D8 | Tools and MCPs | 10.6% | 2, 3 |

Full sub-area breakdown and where each is taught/practised/drilled:
`logistics/03-assessment-and-certification.md`.

**The method.** Every CCDV-F item is one of **four developer decisions** — *what runs* ·
*how does it call Claude* · *what does Claude see and say* · *will it survive production* —
and two elimination rules (mechanism-beats-knob; mechanism-beats-guidance) kill the wrong
options. This is taught Day 1 and used on every practice question all week. See
`logistics/05-exam-method.md`; optional video walkthrough map in `video-companion.md`.

---

## The week at a glance

| Day | Theme | Primary domains | Anchor episodes | Headline material |
|---|---|---|---|---|
| **0** *(pre-work, ~2–3h)* | Ready your machine | — | — | Python primer, tooling, accounts, `check_env.py` |
| **1** | Foundations: LLMs, the Messages API & your first app | D5, D2, D6, D4, D1 | `ep01` | LLM & technical fundamentals · Messages API mechanics · streaming · typed errors + backoff · token & cost math · the agent loop by hand |
| **2** | Prompt & context engineering · tools · structured output | D6, D8, D2 | `ep03` `ep07` | prompt engineering · output handling · `strict` tools & `messages.parse()` · tool implementation · untrusted-content principle |
| **3** | Building agents · Claude Code · MCP | D1, D3, D8, D7 | `ep02` `ep04` `ep05` `ep09` | agent architecture & patterns · Agent SDK · subagents · **Claude Code operation** (rules/skills/commands/memory/project-config/headless) · MCP server dev · hooks |
| **4** | Applications & integration: requirements → design → lifecycle → RAG | D2, D6, D4 | `ep06` `ep08` | understanding requirements · Claude application design patterns · systems life cycle · **configuration management** · context engineering & memory · RAG · evaluation harness |
| **5** | Model selection & optimisation · security & safety · exam | D5, D7, D4 | `ep10` `ep11` `ep12` | model trade-offs · **cost-optimisation order** · prompt caching · batch · usage tracking · AI-app security · guardrails · **identity/secrets/key management** · vision/PDF · capstone · **53-item timed mock** |

Contact time is **≥ 45% hands-on**. Every domain and sub-area is taught, practised, and
drilled.

---

## How to use this folder

```
aizentify-cdf-bootcamp/
├── README.md ..................... you are here
├── THEME.md ..................... Aizentify brand tokens + deck authoring
├── requirements.txt ............. pip install -r this
├── video-companion.md .......... optional 17-lesson video map (blueprint order)
├── assets/ ..................... shared deck CSS, official logo, nav script
├── logistics/ ................... FOR THE ORGANISER & TRAINER — read first
│   ├── 00-environment-setup.md
│   ├── 01-procurement-guide.md ....... give this to the budget holder (push: Claude Team)
│   ├── 02-trainer-prep-checklist.md
│   ├── 03-assessment-and-certification.md ... the 8-domain blueprint + coverage map
│   ├── 04-cohort-runbook.md
│   └── 05-exam-method.md ............. the "four decisions + two rules" — the spine
├── day0-prework/ ............... send to candidates 2 weeks out
├── day1-foundations/ .......... slides/ · trainer-guide.md · labs/ · exercises.md · quiz.md · exam-style-questions.md
├── day2-prompt-tools-output/ ... (outline + lab specs — full build in pass 2)
├── day3-agents-claude-code/ .... (outline + lab specs)
├── day4-applications-integration/ (outline + lab specs)
├── day5-optimisation-security-cert/ (outline + lab specs + mock-exam/)
└── question-bank/ ............. certification-style questions, tagged to exam sub-areas
```

**Trainer reading order:** `logistics/01` → `logistics/00` → `logistics/02` →
`logistics/03` → **`logistics/05` (the exam method — read this twice)** → `logistics/04` →
`day0-prework/README.md` → `day1-foundations/trainer-guide.md`.

**Candidate reading order:** `day0-prework/README.md` (before Day 1) → follow the trainer.

---

## Build status

| Component | Status |
|---|---|
| Brand assets (official logo), README, THEME, requirements, `video-companion.md` | ✅ complete |
| `logistics/00`–`05` (8-domain blueprint + **exam method** + procurement + runbook) | ✅ complete |
| `day0-prework/` (primer, `check_env.py`, `hello_claude.py`) | ✅ complete |
| `day1-foundations/` (deck, trainer guide, 4 labs, exercises, quiz, exam questions) | ✅ complete |
| `question-bank/` — README (8 domains) + Domain 2 pool (28 items) | ✅ complete (pattern for the rest) |
| `day2`–`day5` | 🟡 outline + lab specs; full build in follow-up passes |
| `question-bank/` domains 1, 3–8 + scenarios + 53-item mock | 🟡 blueprint |

Follow-up build passes are listed at the end of `logistics/03` and in the plan.

---

## Notes

- **Requires the parent repo.** Days 1–5 open `epNN/` files read-along. Clone
  `claude-api-masterclass` alongside this, or keep this folder inside it.
- **Blueprint is a moving target.** Reconcile the 8 domains + weights in `logistics/03`
  against Anthropic's current official CCDV-F exam guide before every cohort.
- **Lab cost policy.** Labs pin `claude-haiku-4-5` / `claude-sonnet-5` for classroom cost;
  Day 5 teaches real model selection. See `logistics/01` and `logistics/03`.
