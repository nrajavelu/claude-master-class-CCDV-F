# Day 3 — Building agents · Claude Code · MCP

> **Status: outline + lab specs.** Full build in pass 2.

**Primary CCDV-F domains:** D1 Agents & Workflows (14.7%) · D8 Tools & MCPs (10.6%, MCP
Server Development + Agentic Customisation) · D3 Claude Code (3.1%) · D7 Security & Safety
(Claude Hooks, 1%). **Decision:** ① *what runs?* (plus ③ for Claude Code config).
**Anchor episodes:** `ep02`, `ep04`, `ep05`, `ep09`. **Video companion:** lessons 13, 14, 15
(and 5, 6 for Claude Code).

---

## Learning objectives

1. Distinguish **workflow vs agent**, and know the **four ways to build an agent** and who
   supplies the harness vs the deployment: manual loop · Tool Runner · Claude Agent SDK ·
   Managed Agents.
2. Build with the **Claude Agent SDK**: `query()` vs `ClaudeSDKClient`, `ClaudeAgentOptions`,
   `allowed_tools` scoping, `setting_sources`.
3. Use **hooks** across the lifecycle: `PreToolUse` (approval / block), `PostToolUse`
   (transform / taint), `Stop` (don't-finish-without-X), `PreCompact` (observability). A
   blocking hook is the archetypal *mechanism* answer to a *must/never* security stem.
4. Design **subagents**: `AgentDefinition`, fan-out from a coordinator, per-agent model and
   tool scoping, fresh context. "Usually fewer agents" — know when *not* to.
5. **Operate Claude Code** (D3): rules / memory (`CLAUDE.md`), skills (`.claude/skills/`),
   slash commands, the **project-config discovery hierarchy** (cwd upward), and headless /
   streaming / print modes.
6. Build a **standalone MCP server** with FastMCP (stdio), and connect a **remote MCP
   server** via `.mcp.json` (http) — "an MCP server is not a bag of tools": scope it.
7. Know that a **plugin runs code with your privileges** — installing one is a trust
   decision.

## Module plan (deck outline)

| # | Module | Domain / decision |
|---|---|---|
| 1 | Workflow vs agent · should you even build an agent? (complexity / value / viability / cost-of-error) | D1 · ① |
| 2 | The four ways to build an agent — harness vs deployment | D1 · ① |
| 3 | Agent SDK tour: `query`, `ClaudeSDKClient`, options, `allowed_tools` | D1 · ① |
| 4 | Hooks lifecycle — `PreToolUse` / `PostToolUse` / `Stop` / `PreCompact` (walk `ep04`/`ep05`/`ep06`) | D7 · ④ |
| 5 | Subagents & patterns — fan-out, scoping, "usually fewer agents" | D1 · ① |
| 6 | Claude Code operation — rules, skills, commands, memory, project-config hierarchy, headless mode | D3 · ③ |
| 7 | MCP — `.mcp.json`, stdio vs http, build a FastMCP server, scope the toolset; plugins = trust | D8 · ① |
| — | recap + exam-style questions + quiz | |

## Lab specs

### Lab 1 · Two-subagent repo auditor  ·  50 min · D1
- **Do:** a coordinator `query()` that fans out to a `docstring-reviewer` and a
  `security-reviewer` `AgentDefinition`, each with a narrow `tools=` list and its own model
  (`claude-haiku-4-5`). One custom `@tool`. Post one combined result.
- **Expected output:** trace shows two delegations, then one aggregated summary.
- **Reference:** `ep05/agent.py`, `ep05/subagents.py`.

### Lab 2 · A blocking hook that means "never"  ·  35 min · D7
- **Do:** a `PreToolUse` hook on a `post_comment` tool that **denies** the call unless it
  cites `file` + `line`; a `PostToolUse` hook that tags fetched external text as untrusted.
  Try to make the agent post without evidence — watch the hook refuse.
- **Expected output:** `permission_denials` > 0 for the un-evidenced attempts; success only
  when evidence is present.
- **Reference:** `ep04/hooks.py`, `ep05/hooks.py`.

### Lab 3 · Operate Claude Code  ·  40 min · D3
- **Do:** in a scratch project, add a `CLAUDE.md`, a `.claude/skills/<name>/SKILL.md`, and a
  slash command; run `claude` and show each being picked up. Then run **headless**
  (`claude -p "..."`) and pipe the output.
- **Expected output:** the rule is obeyed without being re-prompted; the skill triggers on
  its description; headless prints a result to stdout.
- **Reference:** `ep08/.claude/`, `ep06/CLAUDE.md`.

### Lab 4 · Build & wire an MCP server  ·  45 min · D8
- **Do:** write `facts_server.py` with FastMCP (one `@mcp.tool()`, stdio). Smoke-test it by
  piping JSON-RPC (`initialize` / `tools/list` / `tools/call`). Then add it to `.mcp.json`
  (stdio) and a remote GitHub server (http, `${GITHUB_PAT}`); scope `allowed_tools` to
  exactly one tool from each.
- **Expected output:** the raw JSON-RPC smoke test returns the tool list + a result; the
  agent can call `count_*` and one read-only GitHub tool, nothing else.
- **Reference:** `ep09/repo_facts_server.py`, `ep09/.mcp.json`, `ep09/mcp_test_input.jsonl`.

## Exam-style question targets (≥ 18)

Four-ways-to-build-an-agent (harness vs deployment) · workflow vs agent decision criteria ·
hook events and what each can do · blocking hook as the answer to a `must/never` stem ·
subagent scoping · "usually fewer agents" · Claude Code project-config discovery order ·
headless/print mode · `.mcp.json` stdio vs http · plugin = code with your privileges ·
scoping an MCP toolset.

## Quiz targets (10–12)

`query` vs `ClaudeSDKClient` · `allowed_tools` · `setting_sources=["project"]` and what it
gates · the 4 hook events · `AgentDefinition` fields · `.mcp.json` shapes · FastMCP stdio
line-buffering gotcha.
