# Question bank — Claude Certified Developer: Foundations (CCDV-F)

A growing pool of certification-style questions, organised to mirror the **8 official CCDV-F
domains** and their sub-areas. Use it for:

- **during the week** — the trainer pulls extras when a table finishes early or a sub-area
  needs another rep;
- **revision** — a candidate weak in a sub-area drills that section;
- **the Day 5 mock** — `day5-optimisation-security-cert/mock-exam/` samples **53 items** in
  the official domain mix.

Every item follows the same contract:

```
### <id>. (<style>[ · <sub-area>]) <stem>
A. ...   B. ...   C. ...   D. ...

> **Answer:** <letter(s)>
> **Why:** <one line>
> **Distractors:** A — <why wrong> · B — <why wrong> · ...
```

**Styles:** SBA (single best answer) · MR (multiple response — item says how many) ·
SCN (scenario / next-step) · OUT (predict output) · BUG (spot the bug) ·
JDG (best-practice judgement).

---

## Domains, weights & files

| File | Domain | Weight | Sub-areas | Item target | Status |
|---|---|---:|---|---:|---|
| `domain-1-agents-workflows.md` | D1 Agents and Workflows | 14.7% | Agent Architecture · Agent Construction · Patterns & Frameworks | 24 | 🟡 blueprint |
| `domain-2-applications-integration.md` | D2 Applications and Integration | **33.1%** | Understanding Requirements · Systems Life Cycle · **Claude API Mechanics** · Software Engineering Foundations · Application Design · Configuration Management | 48 | ✅ API-Mechanics pool done (28); other sub-areas 🟡 |
| `domain-3-claude-code.md` | D3 Claude Code | 3.1% | Claude Code Operation | 8 | 🟡 blueprint |
| `domain-4-eval-testing-debugging.md` | D4 Eval, Testing, and Debugging | 2.6% | Debugging & Error Handling | 8 | 🟡 blueprint |
| `domain-5-model-selection-optimisation.md` | D5 Model Selection and Optimisation | 16.8% | LLM Fundamentals · Technical Fundamentals · Model Selection & Trade-offs · Cost & Token Management | 26 | 🟡 blueprint |
| `domain-6-prompt-context-engineering.md` | D6 Prompt and Context Engineering | 11% | Context Engineering · Prompt Engineering · Output Handling | 18 | 🟡 blueprint |
| `domain-7-security-safety.md` | D7 Security and Safety | 8.1% | AI Application Security · Guardrails & Safe Deployment · Claude Hooks · Identity/Secrets/Key Mgmt | 14 | 🟡 blueprint |
| `domain-8-tools-mcps.md` | D8 Tools and MCPs | 10.6% | Tool Implementation · MCP Server Development · Agentic Customisation | 16 | 🟡 blueprint |
| `scenario-questions.md` | cross-domain "what next" | — | — | 15 | 🟡 blueprint |

**~185 items** at target, allocated ≈ to domain weight. Domain 2's **Claude API Mechanics**
sub-pool (28 items, from Day 1) is complete and is the writing pattern for the rest — built
in follow-up passes alongside Days 2–5.

---

## Reconcile before every cohort

Domain names/weights above track the published CCDV-F blueprint (see
`../logistics/03-assessment-and-certification.md`). Pull the current **official** exam guide,
diff it, re-weight the mock sample. If domains are renamed/merged, keep the items and re-tag.

---

## Distractor design (what we deliberately train against)

Teach candidates to name the bucket a wrong option falls in:

1. **Stale API** — true of an older model/SDK: `budget_tokens`, `output_format`, assistant
   prefill, `claude-code-sdk`, `web_search_20250305`.
2. **Right but not best** — works, but a cheaper / simpler / SDK-native option exists
   (`max_retries` vs a hand-rolled loop; `get_final_message()` vs a second call).
3. **Plausible-but-backwards** — volatile content *before* the cache breakpoint;
   `tool_result` in an assistant message; retrying a 400.
4. **Wrong system** — an OpenAI-ism in Claude clothing (`tool_call`, `content_filter`,
   `function_call`, `/v1/chat/completions`).
