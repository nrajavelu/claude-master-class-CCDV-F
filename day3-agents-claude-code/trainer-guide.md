# Day 3 — Trainer guide (slide-by-slide)

**Deck:** `slides/day3.html` (~22 slides) · **Recap:** `recap.html` · **Contact time:** ~6h
**Primary domains:** D1 (Agents & Workflows, 14.7%) · D8 (Tools & MCPs — MCP dev + agentic customisation) · D3 (Claude Code, 3.1%) · D7 (hooks).
**Anchor episodes:** `ep02` `ep04` `ep05` `ep09`. **Video:** walkthrough L13, L14, L15 · exam-guide D1 (7:51), D3 (15:35), D8 (26:09) · Build-along Ep 02–09.

> **Weight reality (say it):** D3 Claude Code is **3.1%** — a cameo. Don't let candidates' daily
> affection for it buy more study time than the blueprint pays for. D1 is where the points are.

---

## Before this session
- [ ] Day 2 recap quiz. `claude` signed in on your machine (needed live from Module 5).
- [ ] Dry-run `code-snippets/blocking_hook.py` and `code-snippets/mcp_server.py` (needs `claude-agent-sdk` + `mcp`).
- [ ] Pre-open: `ep05/agent.py` + `ep05/subagents.py`, `ep04/hooks.py`, `ep09/.mcp.json` + `ep09/repo_facts_server.py`.

## Timing plan
| Block | Time |
|---|---|
| Recap quiz | 09:00–09:15 |
| Module 1 — workflow vs agent · 5 patterns · four checks + guardrails | 09:15–10:10 |
| Module 2 — four ways to build an agent | 10:10–10:40 *(break)* |
| Module 3 — hooks lifecycle + a blocking hook | 10:55–11:35 |
| **Lab · blocking hook + taint hook** | 11:35–12:20 *(lunch)* |
| Module 4 — subagents & patterns | 13:20–13:55 |
| **Lab · two-subagent auditor** | 13:55–14:45 *(break)* |
| Module 5 — Claude Code operation | 15:00–15:35 |
| **Lab · operate Claude Code** | 15:35–16:10 |
| Module 6 — MCP + **Lab · build an MCP server** | 16:10–17:00 |
| Recap + exam-style Qs + quiz | 17:00–17:30 |

## If behind
1. Merge the Claude Code lab into a live demo (it's 3.1%).
2. MCP lab: do the JSON-RPC smoke test together, skip wiring the GitHub server → homework.
3. **Never cut:** the blocking-hook lab, the four-ways-to-build slide, the exam-style-question block.

## Known failure modes
| Failure | Fix |
|---|---|
| blocking-hook lab: the hook doesn't fire | matcher string mismatch — `mcp__<server>__<tool>`; print `input_data["tool_name"]` |
| subagent lab: coordinator does the work itself | its `allowed_tools` includes the leaf tools — remove them, leave only `Agent` + `post_*` |
| MCP smoke test hangs | stdout not line-buffered — `sys.stdout.reconfigure(line_buffering=True)` |
| "agent-everything brain" in discussion | make them argue the *workflow* case out loud for every scenario |

---

## Slide-by-slide (navigate by title)

### Title + orientation — 3 min · Decision ① *what runs*.

### Module 1 · Workflow vs agent — who decides the path? — 5 min
- **Workflow** = your code decides the path. **Agent** = the model decides. The exam's question is **"should you"**, not "can you".
- *Ref:* exam-guide D1 (7:51).

### Module 1 · Five workflow patterns — 6 min
- Prompt chaining · routing · parallelisation · orchestrator–workers · evaluator–optimiser.
- *Say:* "Reaching for an agent when a 3-step chain would do is the **overbuild** in its natural habitat."

### Module 1 · Four checks + loop guardrails — 6 min
- The four checks (complexity / value / viability / cost-of-error) — any "no" → simpler tier.
- Production loop needs: **iteration cap · timeouts · a defined way to fail**. Agent spinning forever → the answer is **loop limits + termination**, not a supervisor agent.
- *Ref:* walkthrough L14.

### Module 2 · Harness × deployment (Exam watch) — 8 min
- The 2×2 SVG. Manual loop / Tool Runner / Agent SDK / Managed Agents. Two independent questions: **who supplies the harness**, **who supplies the deployment**.
- Hammer: **Tool Runner ≠ Claude Agent SDK** (different packages). Only Managed Agents adds managed deployment.

### Module 3 · Hook lifecycle (Exam watch) — 7 min
- The timeline SVG: `PreToolUse` (deny) → tool → `PostToolUse` (transform/taint) → `Stop` (don't-finish-without-X) · `PreCompact` (observe).
- **A blocking `PreToolUse` hook is the mechanism answer to a *must / never* security stem.** This is the D7 payoff.
- *Ref:* `ep04/hooks.py`, `ep05/hooks.py`, `ep06` `require_evidence` (moved to `Stop`) · Build-along Ep 04.

### Module 3 · A blocking hook, in code — 4 min
- The focus-code. "Runs before the tool. Returns a decision. The model's intent doesn't matter — the code decides."

### **Lab · blocking hook + taint hook** — 45 min
- A `PreToolUse` deny on `post_comment` unless it cites `file` + `line`; a `PostToolUse` hook that tags fetched text untrusted.
- Green light: `permission_denials > 0` for un-evidenced attempts; success only with evidence.
- *Ref:* `code-snippets/blocking_hook.py`.

### Module 4 · Coordinator fans out — 6 min
- The fan-out SVG. Each subagent: own fresh context, narrow tools, own (cheaper) model.
- **Usually fewer agents** — each adds context/latency/cost; a single loop is easier to debug + eval. Fan out only for true parallelism or reading-heavy sub-tasks.
- *Ref:* `ep05/subagents.py` · walkthrough L14 · Build-along Ep 05.

### **Lab · two-subagent auditor** — 50 min
- Coordinator `query()` → `docstring-reviewer` + `security-reviewer` `AgentDefinition`s, narrow tools, `claude-haiku-4-5`. One custom `@tool`. One combined result.

### Module 5 · Project config discovered cwd-upward (Exam watch) — 7 min
- The discovery SVG. `CLAUDE.md` / `.claude/skills/` / `.claude/commands/` / `.mcp.json`. **Both a subfolder and root file apply.**
- A rules file's content arrives as a **user message**, not `system`. Headless: `claude -p "..."`.
- `setting_sources=["project"]` gates all of it in the SDK.
- *Ref:* `ep06/CLAUDE.md`, `ep08/.claude/` · walkthrough L6.

### **Lab · operate Claude Code** — 40 min
- Add a `CLAUDE.md` + a `SKILL.md` + a slash command to a scratch project; run `claude`; show each picked up without re-prompting; then `claude -p "..."` piped.

### Module 6 · An MCP server is not a bag of tools (Exam watch) — 8 min
- The transports SVG (`stdio` / `http` / `sse`). MCP is a **protocol**.
- **Build a server when a capability crosses apps/teams; keep a plain in-process tool when it's specific to one app.** Least privilege: read-only agent ≠ a write tool. `${ENV_VAR}` for secrets. A plugin = code with your privileges.
- *Ref:* `ep09/repo_facts_server.py`, `ep09/.mcp.json`, `ep09/mcp_test_input.jsonl` · walkthrough L13.

### **Lab · build & wire an MCP server** — 45 min
- FastMCP stdio server + JSON-RPC smoke test + `.mcp.json` (stdio + a remote GitHub http server) scoped to one tool each.
- *Ref:* `code-snippets/mcp_server.py`.

### Recap + exam-style Qs + quiz — 30 min
- `exam-style-questions.md` → `quiz.md` → `portal/practice.html?day=3`.
