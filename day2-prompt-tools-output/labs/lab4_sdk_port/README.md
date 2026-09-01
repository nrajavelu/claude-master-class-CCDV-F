# Lab 4 · Port the tool to the Agent SDK

**Domain:** D1 (Agent Construction) · D8 (Tool Implementation) · **Time:** 20 min
**Practise:** the same tool, same result — the difference is *who runs the loop*.

> Depends on Lab 2 (`lab2_tool_description`). Reference: `ep03/agent.py`.

---

## Goal

Take the **detailed** `lookup_order` description from Lab 2 and expose it as an
`@tool` on a `create_sdk_mcp_server`, then call it from `query()` with `allowed_tools`
scoped to just that one tool. Same 5 prompts, same call/no-call decisions — but now the
request→execute→loop is the SDK's job, not your `for` loop.

```
cd aizentify-cdf-bootcamp
python day2-prompt-tools-output/labs/lab4_sdk_port/starter/lab.py
```

Needs `claude-agent-sdk` (`pip install "claude-agent-sdk>=0.2.128"`).

---

## Steps

1. `starter/lab.py` has a `@tool("lookup_order", DESC, {schema})` stub that returns a canned
   status string, and a `query()` call with a `# TODO` on `allowed_tools`.
2. Paste your `DESC_DETAILED` from Lab 2 into `DESC`.
3. Set `allowed_tools=["mcp__orders__lookup_order"]` — nothing else.
4. Run the 5 prompts. Confirm the tool fires on 1/2/5 and not on 3/4, same as Lab 2's
   detailed build.

## Checkpoints

- [ ] Same call/no-call pattern as Lab 2 — the description carried over, the harness changed.
- [ ] `allowed_tools` is scoped to the single tool.
- [ ] They can state: raw Messages API loop → *you* own the loop; Agent SDK → the SDK owns
      it, in your process; Managed Agents → Anthropic owns it. Control vs responsibility.

## Common mistakes

| Symptom | Cause |
|---|---|
| "unknown tool" | the name must be `mcp__<server>__<tool>` — here `mcp__orders__lookup_order` |
| tool never fires | `allowed_tools` omitted or misspelled |
