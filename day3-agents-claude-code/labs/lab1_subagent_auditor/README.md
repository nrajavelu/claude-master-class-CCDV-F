# Lab 1 · Two-subagent repo auditor

**Domain:** D1 (Agent Architecture · Patterns & Frameworks) · **Time:** 50 min
**Practise:** a coordinator that **delegates** to two scoped subagents and aggregates —
without doing the leaf work itself.

> Runnable mechanic reference: `ep05/agent.py`, `ep05/subagents.py`. This lab adds the graded
> framing and the "coordinator did the work itself" failure to diagnose.

---

## Goal

A coordinator `query()` fans out to two `AgentDefinition`s:

- **`docstring-reviewer`** — narrow tools, cheap model (Haiku), reads `.py` files and reports
  missing or weak docstrings.
- **`security-reviewer`** — narrow tools, reports obvious risks (hardcoded secrets, `shell=True`,
  unvalidated input).

Each runs with its **own fresh context** and **never sees the other's history**. The
coordinator holds **only** the `Task`/delegation tool — not the file-reading tools — so it is
structurally forced to delegate. It then posts **one combined summary**.

```
cd aizentify-cdf-bootcamp
python day3-agents-claude-code/labs/lab1_subagent_auditor/starter/lab.py
```

Needs `claude-agent-sdk` (`pip install "claude-agent-sdk>=0.2.128"`).

---

## Steps

1. `starter/lab.py` has a `mini_repo/` fixture (two small `.py` files — one with a hardcoded
   key and no docstrings), two `@tool`s (`read_file`, `list_files`), and two half-written
   `AgentDefinition`s.
2. Fill each `AgentDefinition`: a tight `prompt`, `tools=` scoped to just
   `["mcp__fs__read_file", "mcp__fs__list_files"]`, and `model="claude-haiku-4-5"`.
3. Wire them into `ClaudeAgentOptions(agents={...})`.
4. Scope the **coordinator's** `allowed_tools` so it does **not** include the `fs` tools —
   only the delegation capability. This is the whole point: least privilege makes the
   architecture, not the prompt.
5. Run. Confirm the trace shows two delegations, then one aggregated summary naming findings
   from **both** reviewers.

---

## Expected output (shape)

```
[coordinator] delegating to: docstring-reviewer
[docstring-reviewer] mini_repo/discount.py: apply_discount() has no docstring; ...
[coordinator] delegating to: security-reviewer
[security-reviewer] mini_repo/config.py: hardcoded API key on line 3; ...
[coordinator] SUMMARY
  Docstrings: 2 functions undocumented in discount.py
  Security:   1 hardcoded secret in config.py
```

## Checkpoints

- [ ] The coordinator's `allowed_tools` does **not** contain the `fs` tools.
- [ ] Each subagent has its own `model=` and a `tools=` list scoped to two tools.
- [ ] The final summary contains findings from **both** subagents (proves isolation + aggregation).
- [ ] They can state the three axes a subagent buys: **context isolation · parallelisation ·
      specialisation** — and the ~15× multi-agent token-cost caveat.

## Common mistakes

| Symptom | Cause |
|---|---|
| coordinator reads files itself, never delegates | the `fs` tools are in its `allowed_tools` — remove them |
| one reviewer's findings missing from the summary | coordinator isn't collecting both `Task` results before summarising |
| "unknown tool mcp__fs__…" | matcher/name mismatch — print the tool names the server registered |

## Going further

- Run the two reviewers **in parallel** and show the wall-clock time ≈ the slower one, not
  the sum.
- Give `security-reviewer` a stronger model and `docstring-reviewer` Haiku — specialisation
  by cost.
