# Day 3 — End-of-day quiz

10 questions, ~10 min. **≥ 8/10**. Domains: **D1** Agents & Workflows · **D8** Tools & MCPs ·
**D3** Claude Code · **D7** hooks.

---

### Q1 (D1) In a **workflow**, who decides the path? In an **agent**?
### Q2 (D1) Name the five workflow patterns.
### Q3 (D1) An agent is spinning forever and burning budget. What's the fix — and what's the *overbuild* answer to avoid?
### Q4 (D1) Tool Runner vs Claude Agent SDK — one sentence each on the difference.
### Q5 (D1) Which of the four ways to build an agent gives you *both* a managed harness and managed deployment?
### Q6 (D7) Which hook event denies a tool call before it runs? Which one is observe-only?
### Q7 (D3) A `CLAUDE.md` exists in a subfolder and at the repo root; you run Claude Code from the subfolder. Which applies?
### Q8 (D3) The content of a coding-tool rules file reaches the model as what kind of message?
### Q9 (D8) `.mcp.json` transport for a local Python server you wrote?
### Q10 (D8) When should you build an MCP server rather than a plain in-process tool?

---
---
## Answer key
**Q1** — Workflow: *your code* decides the path. Agent: *the model* decides (tools in a loop,
observing results, choosing next). *(D1)*

**Q2** — Prompt chaining · routing · parallelisation · orchestrator–workers · evaluator–optimiser. *(D1)*

**Q3** — Add **loop limits (iteration cap) + timeouts + a defined way to fail / termination
condition.** Overbuild to avoid: adding a second agent to supervise the first. *(D1)*

**Q4** — Tool Runner: the SDK drives the request→execute→loop cycle *over your own tools*,
you host. Claude Agent SDK: Claude Code as a library — *built-in* tools (read/write/bash/…),
you host. Different packages. *(D1)*

**Q5** — **Managed Agents** (Anthropic runs the loop *and* hosts a per-session sandbox). *(D1)*

**Q6** — `PreToolUse` denies (returns a `permissionDecision`). `PreCompact` is
observe-only — by the time it fires it's too late to save anything. *(D7)*

**Q7** — **Both.** Project config is discovered from the working directory up to the repo
root. *(D3)*

**Q8** — A **`user` message** — it lands in the conversation channel, so later messages sit
at the same level. Not `system`. *(D3)*

**Q9** — `stdio`, with a `command` + `args`. *(D8)*

**Q10** — When the capability should be **shared and reused across apps / teams**. Keep a
plain in-process tool when it's specific to one app. *(D8)*

---
### Scoring
| Score | Next |
|---|---|
| 9–10 | Solid. |
| 7–8 | Re-read the module behind any miss. |
| ≤ 6 | Flag. Tonight: `ep05/agent.py` + `ep04/hooks.py` + `ep09/.mcp.json` · `question-bank/domain-1-agents-workflows.md`. |
