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
| `domain-1-agents-workflows.md` | D1 Agents and Workflows | 14.7% | Agent Architecture · Agent Construction · Patterns & Frameworks | 24 | ✅ 24/24 |
| `domain-2-applications-integration.md` | D2 Applications and Integration | **33.1%** | Understanding Requirements · Systems Life Cycle · **Claude API Mechanics** · Software Engineering Foundations · Application Design · Configuration Management | 48 | 🟡 28/48 — API-Mechanics pool done; other sub-areas to fill |
| `domain-3-claude-code.md` | D3 Claude Code | 3.1% | Claude Code Operation | 8 | ✅ 8/8 |
| `domain-4-eval-testing-debugging.md` | D4 Eval, Testing, and Debugging | 2.6% | Debugging & Error Handling | 8 | ✅ 8/8 |
| `domain-5-model-selection-optimisation.md` | D5 Model Selection and Optimisation | 16.8% | LLM Fundamentals · Technical Fundamentals · Model Selection & Trade-offs · Cost & Token Management | 26 | ✅ 26/26 |
| `domain-6-prompt-context-engineering.md` | D6 Prompt and Context Engineering | 11% | Context Engineering · Prompt Engineering · Output Handling | 18 | ✅ 18/18 |
| `domain-7-security-safety.md` | D7 Security and Safety | 8.1% | AI Application Security · Guardrails & Safe Deployment · Claude Hooks · Identity/Secrets/Key Mgmt | 14 | ✅ 14/14 |
| `domain-8-tools-mcps.md` | D8 Tools and MCPs | 10.6% | Tool Implementation · MCP Server Development · Agentic Customisation | 16 | ✅ 16/16 |
| `scenario-questions.md` | cross-domain "what next" | — | — | 15 | 🟡 16 worked |

**~185 items** at target, allocated ≈ to domain weight. **158 written** so far
(24+28+8+8+26+18+14+16 domain items + 16 scenarios); the remaining gap is Domain 2's
non-API-Mechanics sub-areas (Requirements · Life Cycle · SW-Eng · App Design · Config Mgmt),
whose facts are already carried by `../blueprint-mastery-map.md` and the 53-item mock.

---

## Reconcile before every cohort

Domain names/weights above track the published CCDV-F blueprint (see
`../logistics/03-assessment-and-certification.md`). Pull the current **official** exam guide,
diff it, re-weight the mock sample. If domains are renamed/merged, keep the items and re-tag.

---

## Distractor species (name at least two before answering)

Teach candidates to name the species a wrong option falls in. Full treatment + examples:
`../logistics/05-exam-method.md §4`.

1. **Overbuild** ⚑ — more machinery than the problem deserves ("add a routing model" when
   the fix is a better tool description; "re-architect the pipeline" when the fix is
   caching). **The developer exam's specialty — engineers are the most vulnerable.** The
   elegant minimal fix wins, consistently.
2. **Symptom-treater** — patches the symptom, leaves the cause ("add *please respond
   correctly*"; "make the summaries shorter").
3. **Extremist** — all-or-nothing ("refuse to process external content"; "review every
   record by hand").
4. **True-but-irrelevant** — a correct statement that answers nothing asked.
5. **Stale API** — `budget_tokens`, `output_format`, assistant prefill, `claude-code-sdk`.
6. **Right word, wrong place** — a `role:"system"` message; a WebSocket for streaming;
   `tool_result` in an assistant message; volatile content before the cache breakpoint.
7. **Wrong system** — an OpenAI-ism (`tool_call`, `content_filter`, `function_call`,
   `/v1/chat/completions`).

Every item's `> Distractors:` line should tag each wrong option with its species.
