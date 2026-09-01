# Lab 4 · Build & wire an MCP server

**Domain:** D8 (MCP Server Development · Agentic Customisation) · **Time:** 45 min
**Practise:** an MCP server is *just a program that speaks JSON-RPC over stdio*; scoping the
toolset; `${VAR}` expansion for a remote server's secret.

> Runnable mechanic reference: `code-snippets/mcp_server.py`. This lab makes you write the
> server, smoke-test it with **no agent at all**, then wire it into `.mcp.json` alongside a
> remote server, each scoped to one tool.

---

## Goal

1. Write `facts_server.py` — a FastMCP **stdio** server with **one** tool, `count_todos`,
   that counts `# TODO` / `# FIXME` lines across `.py` files in a directory.
2. Smoke-test it by piping the provided `mcp_test_input.jsonl` — the server should answer
   `initialize`, `tools/list`, and `tools/call` with plain JSON-RPC. No API key, no agent.
3. Write a `.mcp.json` with **two** servers: your `facts` server (`stdio`) and a remote
   GitHub server (`http`, `Authorization: Bearer ${GITHUB_PAT}`), and an `allowed_tools`
   list scoped to **one tool each** — proving "an MCP server is not a bag of tools".

```
cd aizentify-cdf-bootcamp
python day3-agents-claude-code/labs/lab4_mcp_server/starter/facts_server.py < day3-agents-claude-code/labs/lab4_mcp_server/mcp_test_input.jsonl
```

Needs `mcp` (`pip install "mcp>=1.2.0"`).

---

## Steps

1. `starter/facts_server.py` has the FastMCP boilerplate and a `# TODO` for the tool body.
   Fill `count_todos(directory: str) -> str`: walk `*.py`, count lines matching
   `# TODO`/`# FIXME`, return a short text summary.
2. Keep `sys.stdout.reconfigure(line_buffering=True)` — without it, responses can sit in the
   buffer and the smoke test hangs.
3. Run the pipe command above. You should see three JSON-RPC responses (ids 1, 2, 3); the
   last one carries the count for `mini_repo/` (there's a planted `# TODO`).
4. Fill `starter/.mcp.json`: a `stdio` entry (`command`: `python`, `args`: the server path)
   and an `http` entry for GitHub with the `${GITHUB_PAT}` header. `solution/` has both.
5. State the scoping: `allowed_tools=["mcp__facts__count_todos",
   "mcp__github__pull_request_read"]` — nothing else.

---

## Expected output (shape)

```
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2025-06-18", ... "serverInfo":{"name":"facts", ...}}}
{"jsonrpc":"2.0","id":2,"result":{"tools":[{"name":"count_todos", ...}]}}
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"2 files, 1 TODO/FIXME line"}], ...}}
```

## Checkpoints

- [ ] The smoke test returns **three** JSON-RPC results with no agent and no API key —
      proving MCP is a transport protocol, not a Claude feature.
- [ ] `.mcp.json` has the GitHub token as `${GITHUB_PAT}`, **never** a literal.
- [ ] `allowed_tools` names exactly the two tools needed — not `mcp__facts__*`.
- [ ] They can say: build a server when a capability is **shared & independently maintained
      across apps**; a plain in-process `@tool` when it's specific to one app.

## Common mistakes

| Symptom | Cause |
|---|---|
| smoke test hangs | missing `sys.stdout.reconfigure(line_buffering=True)` |
| `tools/list` is empty | the `@mcp.tool()` decorator missing, or the function defined after `mcp.run()` |
| GitHub server 401 | `${GITHUB_PAT}` not exported in the shell / not a fine-grained read PAT |

## Going further

- Add a `resources` entry (a readable file) and show it in `resources/list`.
- Point a real `claude` session at the `.mcp.json` and call both tools; confirm it cannot
  call any tool outside `allowed_tools`.
