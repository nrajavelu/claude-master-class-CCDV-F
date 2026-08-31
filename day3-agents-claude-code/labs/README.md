# Day 3 — labs

Run from `aizentify-cdf-bootcamp/`. `code-snippets/` holds runnable references for the
mechanics; the labs below add the graded framing (goal · steps · expected output ·
checkpoints).

| Lab | Goal | Runnable reference | Built |
|---|---|---|---|
| `lab1_subagent_auditor/` | A coordinator `query()` fans out to `docstring-reviewer` + `security-reviewer` `AgentDefinition`s (narrow tools, cheap model); one combined result | `ep05/agent.py`, `ep05/subagents.py` | spec + starter |
| **`lab2_blocking_hook/`** | A `PreToolUse` hook that **denies** `refund` unless approved; a `PostToolUse` hook that taints fetched text as untrusted; try to get past it | **`code-snippets/blocking_hook.py`** (runnable) · `ep04/hooks.py` | **starter + solution** |
| `lab3_claude_code/` | Add a `CLAUDE.md` + `.claude/skills/<n>/SKILL.md` + a slash command to a scratch project; show each picked up without re-prompting; run headless `claude -p "..."` | `ep06/CLAUDE.md`, `ep08/.claude/` | spec |
| `lab4_mcp_server/` | Write a FastMCP **stdio** server (one `@mcp.tool()`); smoke-test with JSON-RPC; wire it + a remote GitHub http server into `.mcp.json`, scoped to one tool each | **`code-snippets/mcp_server.py`** (runnable) · `ep09/` | spec + `mcp_test_input.jsonl` |

---

## lab1_subagent_auditor — spec
- **Starter:** `starter/agent.py` with `REVIEW_AGENTS` + a coordinator prompt; TODO: wire
  `agents=`, scope `allowed_tools` to `["Agent", "mcp__pr_tools__*"]` (coordinator must NOT
  hold the leaf tools), stream the delegations.
- **Expected:** trace shows two `-> delegating to:` lines, then one aggregated summary.
- **Common mistake:** the coordinator does the work itself → remove the leaf tools from its
  `allowed_tools`.

## lab2_blocking_hook — starter + solution *(flagship)*
See `lab2_blocking_hook/README.md`.

## lab3_claude_code — spec
- **Do:** in `scratch/`, add `CLAUDE.md` (one rule), `.claude/skills/greet/SKILL.md`, and
  `.claude/commands/summary.md`; `claude`, confirm each is used unprompted; then
  `claude -p "summarise the repo" | head`.
- **Expected:** the rule is obeyed without being re-typed; the skill triggers on its
  description; headless prints to stdout.
- **Exam link:** project config is discovered **cwd → repo root**; a rules file is a **user
  message**, not `system`.

## lab4_mcp_server — spec
- **Do:** `facts_server.py` (FastMCP, `sys.stdout.reconfigure(line_buffering=True)`, one
  `count_todos` tool). Smoke-test:
  `python facts_server.py < mcp_test_input.jsonl` (provided). Then `.mcp.json` with a
  `stdio` entry for it + an `http` entry for GitHub (`${GITHUB_PAT}`), and
  `allowed_tools=["mcp__facts__count_todos", "mcp__github__pull_request_read"]`.
- **Expected:** the JSON-RPC smoke test returns the tool list + a result; the agent can call
  those two tools and nothing else.
