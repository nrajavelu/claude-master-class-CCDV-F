# code-snippets — runnable references, keyed to exam question types

Tiny, heavily-commented, **runnable** programs. Each one demonstrates the exact behaviour a
cluster of CCDV-F questions asks about. Candidates run them to *see* the thing; trainers
project them when a table needs another rep.

```bash
cd aizentify-cdf-bootcamp          # so the shared .env is found
python code-snippets/<file>.py
```

All pinned to `claude-haiku-4-5`. Each costs a fraction of a cent.

| File | Demonstrates | Exam domain / question type |
|---|---|---|
| `messages_basics.py` | request fields · `content` is a list of blocks · `stop_reason` · `usage` | D2 · SBA / OUT |
| `prompt_structure.py` | contract in `system` vs task in `messages` · XML tags · few-shot | D6 · SBA / JDG |
| `cot_structured.py` | structured Chain-of-Thought · adaptive thinking · `thinking` block | D6 · SBA · "CoT always helps?" distractor |
| `agent_loop_react.py` | the ReAct loop by hand — Thought / Action / Observation · the two rules | D1 · BUG / SCN |
| `streaming.py` | `with client.messages.stream` · `get_final_message()` · SSE not WebSocket | D2 · SBA |
| `retry_chain.py` | typed-exception chain · retry (429/5xx/conn) vs fail-fast (400/401/404) | D4 · MR / SCN |
| `count_tokens.py` | `count_tokens` (no `max_tokens`) · cost = tokens × price/1e6 | D5 · SBA |
| `strict_tool.py` | `strict:true` tool · `additionalProperties:false` · null-for-optional · a `validate()` layer | D2 · BUG |
| `prompt_caching.py` | `cache_control` breakpoint · verify `cache_read_input_tokens` · the `datetime.now()` invalidator | D5 · SCN |
| `batch_custom_id.py` | Message Batches · poll to `ended` · **key results by `custom_id`, not position** | D2·D5 · SCN |
| `blocking_hook.py` | a `PreToolUse` hook that **denies** — the mechanism answer to a *must/never* stem | D7 · SCN (needs `claude-agent-sdk`) |
| `mcp_server.py` | a minimal FastMCP **stdio** server · smoke-test with JSON-RPC | D8 · SBA (needs `mcp`) |

> These are *illustrations*, not the graded labs. The labs (`dayN/.../labs/`) have
> `starter/` + `solution/` and an expected-output contract; these are shorter and just run.
