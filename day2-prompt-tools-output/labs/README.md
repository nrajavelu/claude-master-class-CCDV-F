# Day 2 — labs

| Lab | Goal | Reference | Built |
|---|---|---|---|
| `lab1_prompt_surgery/` | Improve a weak `system` prompt over 3 passes against a fixed rubric; score each pass | Day 1 `exercises.md` B · `code-snippets/prompt_structure.py` | **starter + solution + rubric.py** |
| `lab2_tool_description/` | Define `lookup_order` twice (vague vs detailed); run 5 prompts through each; the vague one mis-calls, the detailed one doesn't | `ep03/tools.py` · `code-snippets/strict_tool.py` | **starter + solution** |
| **`lab3_strict_output/`** | `submit_finding` with `strict:true` + a `validate_finding()` layer + `messages.parse()`; feed clean / wrong-severity / missing-line | `ep07/schemas.py` · `code-snippets/strict_tool.py` | **starter + solution** |
| `lab4_sdk_port/` | Wrap lab 2's tool as `@tool` + `create_sdk_mcp_server`; call from `query()` scoped to that tool | `ep03/agent.py` | **starter + solution** |

Run everything from `aizentify-cdf-bootcamp/` with the venv active. Model pinned to
`claude-haiku-4-5`.

---

## lab1_prompt_surgery — spec
- **Given:** `prompts/weak_system.txt` (a vague summariser prompt) + `rubric.py` (5 checks:
  ≤ 3 bullets · no invented facts · cites the input · audience = maintainer · no praise).
- **Do:** improve the `system` string in 3 passes (role/audience → shape → one few-shot).
  Re-run against `sample_input.txt` each pass; score with `rubric.py`.
- **Expected:** rubric score climbs (e.g. 2/5 → 5/5); three system prompts saved to compare.

## lab2_tool_description — spec
- **Do:** in `starter/`, fill `DESC_VAGUE` and `DESC_DETAILED` for `lookup_order`; a driver
  runs 5 prompts through each build and prints which called the tool correctly.
- **Expected:** vague version mis-calls / skips on ≥ 2 prompts; detailed version correct on
  all 5. Write one sentence on why.

## lab3_strict_output — starter + solution *(flagship)*
See `lab3_strict_output/README.md`.

## lab4_sdk_port — spec
- **Do:** `@tool("lookup_order", DESC_DETAILED, {schema})` → `create_sdk_mcp_server` →
  `query(prompt, ClaudeAgentOptions(mcp_servers=..., allowed_tools=["mcp__t__lookup_order"]))`.
- **Expected:** same tool call + result as lab 2's detailed build.
