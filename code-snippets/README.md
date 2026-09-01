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

### Adapted from the [Anthropic Claude Cookbooks](https://github.com/anthropics/claude-cookbooks) (MIT)

| File | Demonstrates | Exam domain | Cookbook source |
|---|---|---|---|
| `workflow_patterns.py` | prompt chaining · parallelisation · routing (your code owns the path) | D1 · SCN | `patterns/agents/basic_workflows.ipynb` |
| `orchestrator_workers.py` | a lead LLM decomposes at runtime, then delegates (≠ parallelisation) | D1 · SBA/SCN | `patterns/agents/orchestrator_workers.ipynb` |
| `evaluator_optimizer.py` | generate → critique → loop until PASS, with a max-rounds cap | D1·D4 · SCN | `patterns/agents/evaluator_optimizer.ipynb` |
| `cookbook_building_evals.py` | the eval loop: task → **code-graded** vs **LLM-judge** (reasoning before score) | D4 · JDG | `misc/building_evals.ipynb` |
| `usage_cost_api.py` | Admin API `usage_report/messages` + `cost_report` — cost per task, from data | D5 · SBA | `observability/usage_cost_api.ipynb` |
| `extended_thinking.py` | `thinking={"type":"enabled"}` on Haiku 4.5 · thinking blocks + signature · streamed | D5·D2 · SBA | `extended_thinking/extended_thinking.ipynb` |

Full recipe index (≈40 cookbooks mapped to CCDV-F domain / bootcamp day):
[`portal/cookbooks.html`](../portal/cookbooks.html).

### Worked-example pages — `runs/`

Each snippet has a `runs/<name>.md` page: **scenario + real input · the actual code ·
captured output · "read the output" · the exam hook · a tweak to try**. Browse them in the
portal at **`portal/examples.html`** (each has a predict-then-reveal toggle on the output),
or open a single one at `examples.html?f=<name>`.

```bash
python tools/capture_runs.py            # re-capture all output with the offline mock SDK
python tools/capture_runs.py --live     # ...with a real key (real numbers, small spend)
python tools/capture_runs.py prompt_caching workflow_patterns   # just these
```

`--mock` (default) installs `code-snippets/_mockanthropic.py` — canned, deterministic; it
shows real *program flow*, but reply text and token numbers are illustrative. Run `--live`
for genuine model output.

> These are *illustrations*, not the graded labs. The labs (`dayN/.../labs/`) have
> `starter/` + `solution/` and an expected-output contract; these are shorter and just run.
