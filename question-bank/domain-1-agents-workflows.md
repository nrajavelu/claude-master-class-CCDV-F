# Domain 1 — Agents and Workflows  ·  14.7%  ·  decision ① "what runs?"

> **Status: blueprint.** Item target **24**. Built in pass 2 alongside Day 3.
> Anchor: `ep02`, `ep05`. Video: lessons 14, 15.

## Sub-areas & item split

| Sub-area | Weight | Items | Topics to cover |
|---|---:|---:|---|
| Agent Architecture | 4.5% | 7 | workflow vs agent · when to build an agent (complexity / value / viability / cost-of-error) · single loop vs supervisor + sub-agents · built-in vs your tool vs plugged-in capability |
| Agent Construction with Claude | 5.3% | 9 | the manual agentic loop (two rules) · Tool Runner vs Agent SDK vs Managed Agents (harness vs deployment) · `query` vs `ClaudeSDKClient` · `allowed_tools` scoping · turn caps |
| Agent Patterns and Frameworks | 4.9% | 8 | fan-out / coordinator · "usually fewer agents" · sub-agent context isolation & per-agent model · prompt-chaining vs routing vs parallel · when a workflow beats an agent |

## Seed items (pattern for the full set)

### 1. (SBA · Agent Architecture) A task is "extract the invoice total from this PDF". Best build?
A. a multi-agent supervisor  B. a single agent with tools  C. one Messages API call
D. a Managed Agent session

> **Answer:** C
> **Why:** Fully specified, single-step, low cost-of-error — no loop needed. "Should I build
> an agent?" fails on *complexity*.
> **Distractors:** A/B/D — all over-built; the decision criteria say stay at the simplest
> tier that works.

### 2. (SCN · Agent Construction) You want the request→execute→loop handled for you but only
over **your own** tools, on **your own** infra. Which?
A. manual `while` loop  B. the SDK Tool Runner  C. Managed Agents  D. the Claude Agent SDK

> **Answer:** B
> **Why:** Tool Runner = harness only, your tools, you host. Managed Agents adds hosting;
> Agent SDK adds built-in tools; manual loop makes you write the harness.

### 3. (MR · Patterns — choose TWO) Reasons to prefer **fewer** agents:
A. each sub-agent adds context/latency/cost  B. more agents always parallelise better
C. a single loop is easier to debug and eval  D. sub-agents can't use tools

> **Answer:** A, C
> **Distractors:** B — coordination overhead often dominates. D — false.
