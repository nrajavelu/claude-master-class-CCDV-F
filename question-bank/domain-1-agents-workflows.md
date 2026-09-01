# Domain 1 — Agents and Workflows  ·  14.7%  ·  decision ① "what runs?"

> **Status: populated (24/24).** Anchor: `ep02`, `ep05`, `capstone-support-assistant/`.
> Video: lessons 14, 15. Taught Day 3 Modules 1–4. Deeper prose: `../topic-briefings.md` ·
> Day 3 · "Agent architecture / construction"; checklist: `../blueprint-mastery-map.md`
> 1.1–1.3.

## Sub-areas & item split

| Sub-area | Weight | Items | Topics |
|---|---:|---:|---|
| Agent Architecture | 4.5% | 8 | workflow vs agent · when to build an agent at all · single loop vs supervisor + subagents · subagent axes (isolation / parallelisation / specialisation) · **~15× multi-agent token cost** · memory scope (in-context / external / stateless) · dev/prod session mismatch · human-in-the-loop placement |
| Agent Construction with Claude | 5.3% | 8 | manual loop (model asks, your code runs) · raw loop vs Agent SDK vs Managed Agents (control vs responsibility) · **Managed Agents not ZDR/HIPAA-BAA eligible** · loop guardrails (`max_turns`, `max_budget_usd`, timeout, defined failure) · `ResultMessage` subtypes · `allowed_tools` scoping |
| Agent Patterns and Frameworks | 4.9% | 8 | the five patterns (prompt chaining · routing · parallelisation · orchestrator-workers · evaluator-optimiser) · which pattern a scenario describes · orchestrator-workers ≠ parallelisation · when a workflow beats an agent · third-party frameworks only for gaps |

---

## Items

### 1. (SBA · Agent Architecture) A task is "extract the invoice total from this PDF". Best build?
A. a multi-agent supervisor  B. a single agent with tools  C. one Messages API call  D. a Managed Agent session

> **Answer:** C — fully specified, single-step, low cost-of-error; no loop needed.
> **Distractors:** A/B/D — **overbuild**; stay at the simplest tier that works.

### 2. (SCN · Agent Construction) You want request→execute→loop handled for you, but only over **your own** tools, on **your own** infra. Which?
A. a manual `while` loop  B. the Claude Agent SDK (in-process)  C. Managed Agents  D. no loop at all

> **Answer:** B — the SDK provides the scaffolding and runs in your process.
> **Distractors:** A — makes you write the harness. C — Anthropic hosts the loop (extra responsibility surface). D — the task needs a loop.

### 3. (MR · Patterns — choose TWO) Reasons to prefer **fewer** agents:
A. each subagent adds context/latency/cost  B. more agents always parallelise better  C. a single loop is easier to debug and eval  D. subagents can't use tools

> **Answer:** A, C.
> **Distractors:** B — coordination overhead often dominates. D — false.

### 4. (SBA · Agent Architecture) A team wraps a 5-agent orchestra around "call one API, format the result, email it". It works but costs 12× the estimate. Best fix?
A. switch every agent to a cheaper model  B. replace it with a single prompt-chaining workflow  C. add a caching layer per agent  D. lower `max_turns` on each agent

> **Answer:** B — the steps are predetermined; it never needed agents.
> **Distractors:** A/C/D — **symptom-treater**: cut cost without removing the unnecessary architecture (**overbuild**).

### 5. (SBA · Agent Construction) A hospital needs a signed HIPAA BAA and zero data retention. Which construction option is **off the table**?
A. a raw Messages API loop on Bedrock  B. the Agent SDK in a HIPAA-eligible VPC  C. Managed Agents  D. a workflow with no agent loop

> **Answer:** C — Managed Agents are not ZDR / HIPAA-BAA eligible.
> **Distractors:** A/B/D — all deployable compliantly (**wrong-system** to pick them).

### 6. (SCN · Patterns) Support tickets arrive in five categories needing very different handling. One prompt does all five and mislabels edge cases. Minimal fix?
A. fine-tune on labelled tickets  B. a routing workflow: a classifier picks the category, then a category-specific prompt handles it  C. five agents voting  D. more few-shot examples on the mega-prompt

> **Answer:** B — textbook routing.
> **Distractors:** A/C — **overbuild**. D — **symptom-treater**.

### 7. (SBA · Patterns) Orchestrator-workers differs from parallelisation because:
A. it's slower  B. the subtasks aren't known up front — a lead LLM decomposes the problem and delegates dynamically  C. it uses only one model  D. it can't run tasks in parallel

> **Answer:** B.
> **Distractors:** A/C/D — incidental or false.

### 8. (SBA · Agent Architecture) "Should we build an agent?" — the strongest reason **not** to:
A. the task is high-value  B. the steps can be fully predetermined, so a workflow is simpler to debug and eval  C. the team knows the SDK  D. the model is capable enough

> **Answer:** B.
> **Distractors:** A/C/D — not reasons against; **true-but-irrelevant**.

### 9. (SCN · Agent Construction) An agent occasionally loops forever calling the same tool. Which set of guardrails addresses this?
A. a bigger model  B. an iteration cap (`max_turns`), a timeout, a budget cap, and a defined way to fail  C. lower temperature  D. remove the tool

> **Answer:** B — the standard loop guardrails.
> **Distractors:** A/C — **symptom-treater**. D — breaks the feature.

### 10. (SBA · Patterns) One model drafts a translation, a second critiques it, and it loops until the critique passes. This pattern is:
A. routing  B. prompt chaining  C. evaluator-optimiser  D. parallelisation

> **Answer:** C.
> **Distractors:** A/B/D — other patterns.

### 11. (SBA · Agent Architecture) A subagent buys you three things:
A. lower cost, always  B. context isolation, parallelisation, specialisation  C. determinism, caching, retries  D. a bigger context window

> **Answer:** B.
> **Distractors:** A — usually *higher* cost. C/D — not what subagents provide.

### 12. (SCN · Agent Architecture) A design that works as one long dev session starts dropping earlier context in production. Why?
A. the model got worse  B. production runs many short sessions; state that lived in one long context now spans sessions and needs external storage  C. rate limiting  D. a caching bug

> **Answer:** B — dev/prod memory-scope mismatch.
> **Distractors:** A/C/D — misdiagnoses.

### 13. (SBA · Patterns) A step-by-step pipeline where each stage's output feeds the next, with fixed stages, is:
A. an agent  B. prompt chaining  C. orchestrator-workers  D. evaluator-optimiser

> **Answer:** B.
> **Distractors:** A — no model-directed control. C/D — different shapes.

### 14. (SBA · Agent Construction) In a raw Messages API agent loop, who executes the tool?
A. the model  B. your application code  C. Anthropic's servers  D. the SDK harness

> **Answer:** B — the model only signals intent; your code runs it and returns the result.
> **Distractors:** A — the model never executes. C — only for Anthropic-hosted server tools. D — that's the SDK case, not raw.

### 15. (SCN · Patterns) You're unsure whether a problem needs an agent or a workflow. Best move?
A. always build the workflow  B. always build the agent  C. start with an agent, then extract workflow patterns from real traces  D. ask the model to decide at runtime

> **Answer:** C.
> **Distractors:** A/B — premature commitment. D — not a design method.

### 16. (SBA · Agent Architecture) Multi-agent systems are worth their cost when:
A. always — more agents are always better  B. the task genuinely decomposes into independent parallel parts  C. the code is tightly coupled  D. you want lower token usage

> **Answer:** B — Anthropic's own multi-agent system runs ~15× the tokens of single-agent chat.
> **Distractors:** A — false. C — coupled work makes subagents wait on each other. D — opposite.

### 17. (SCN · Agent Construction) A `ResultMessage` comes back with subtype `error_max_budget_usd`. This tells you:
A. an HTTP 402 billing error  B. the loop stopped because it hit its configured spend cap — a loop-level guard, not an API error  C. the API key is out of credit  D. a retryable rate limit

> **Answer:** B.
> **Distractors:** A/C — account-level, different thing. D — wrong category.

### 18. (SBA · Patterns) Running the same prompt N times and taking the majority answer is:
A. orchestrator-workers  B. parallelisation used for **voting / reliability**  C. evaluator-optimiser  D. routing

> **Answer:** B — parallelisation has two uses: speed and voting.
> **Distractors:** A/C/D — other patterns.

### 19. (SCN · Agent Architecture) Where should a human-in-the-loop checkpoint go in a refund agent?
A. after every model token  B. before the irreversible action (issuing the refund)  C. only at the very end  D. nowhere — trust the model

> **Answer:** B — gate before destructive/irreversible calls.
> **Distractors:** A — unusable. C — too late. D — unsafe.

### 20. (SBA · Agent Construction) Raw Messages API loop vs Agent SDK vs Managed Agents — the axis you're trading on is:
A. model quality  B. control vs responsibility — more scaffolding provided means less you own, but also less you can shape  C. context size  D. price only

> **Answer:** B.
> **Distractors:** A/C/D — not the defining trade-off.

### 21. (SCN · Patterns) A third-party framework (LangGraph, PydanticAI) is the right call when:
A. always — they're more powerful than the SDK  B. you need a pattern the Agent SDK doesn't do natively  C. never  D. the SDK's loop is fundamentally weaker

> **Answer:** B.
> **Distractors:** A/D — overstate. C — understates.

### 22. (SBA · Agent Architecture) An agent that runs independent, unrelated jobs with no shared history should use which memory scope?
A. in-context (one session)  B. external storage spanning sessions  C. stateless — each job independent  D. a 1M-context model

> **Answer:** C.
> **Distractors:** A/B — impose sharing the jobs don't need. D — **overbuild**.

### 23. (SCN · Patterns) A single mega-agent is slow because one loop reads dozens of large files before answering. Best change?
A. a faster model  B. a subagent that does the file reading and returns a summary, freeing the parent's context  C. raise `max_turns`  D. disable tools

> **Answer:** B — context isolation via a subagent.
> **Distractors:** A/C — **symptom-treater**. D — breaks it.

### 24. (SBA · Agent Construction) `allowed_tools` on an agent should be:
A. every tool available, for flexibility  B. scoped to exactly what this agent needs — least privilege bounds the blast radius  C. empty  D. set at runtime by the model

> **Answer:** B.
> **Distractors:** A — over-broad. C — non-functional. D — not how scoping works.
