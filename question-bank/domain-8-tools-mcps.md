# Domain 8 — Tools and MCPs  ·  10.6%  ·  decision ① "what runs?"

> **Status: populated (16/16).** Anchor: `ep03`, `ep09`, `day3-.../labs/lab4_mcp_server`.
> Video: lessons 12, 13. Taught Day 2 Module 2 (tools) + Day 3 Module 6 (MCP, agentic
> customisation). Deeper prose: `../topic-briefings.md` · Day 2 · "Tools" and Day 3 · "MCP &
> the tool-choice framework"; checklist: `../blueprint-mastery-map.md` 8.1–8.3.

## Sub-areas & item split

| Sub-area | Weight | Items | Topics |
|---|---:|---:|---|
| Tool Implementation | 4.4% | 7 | schema (`name` / `description` / `input_schema`) · **the description is the interface** — what + when + when-NOT · overlapping descriptions → exclusion sentence or merge behind a `type` param · `tool_choice` (`auto`/`any`/`tool`/`none`) · parallel `tool_use` → one user message of `tool_result` blocks, ids matching · `is_error:true` · `readOnlyHint` · `strict` tools · client-side vs harness dispatch |
| MCP Server Development | 2.1% | 3 | MCP is a protocol, not a library · resources / tools / prompts · stdio vs http transport · `.mcp.json` shapes · env-var expansion for secrets · schemas deferred by default · build-a-server vs in-process-tool decision |
| Agentic Customisation | 4.1% | 6 | the four-way framework (built-in / custom tool / Skill / MCP) · "MCP = data, Skill = process" · hooks · sub-agents · commands · `allowed_tools` scoping · plugin = code with your privileges |

---

## Items

### 1. (SCN · Tool Implementation) The model calls your `refund` tool at the wrong time. First thing to check?
A. the model tier  B. the tool's **description** — is it specific about *when* to use it and what the inputs mean  C. `temperature`  D. `max_tokens`

> **Answer:** B — the description is by far the biggest factor in correct tool use.
> **Distractors:** A — **overbuild**. C/D — **true-but-irrelevant** knobs.

### 2. (MR · Tool Implementation — choose TWO) One assistant turn has 3 `tool_use` blocks. To continue you must:
A. reply with one user message containing 3 `tool_result` blocks  B. put each `tool_result` in its own message  C. match each `tool_result`'s `tool_use_id` to its `tool_use`  D. concatenate the outputs into one string

> **Answer:** A, C.
> **Distractors:** B — trains the model to stop parallelising. D — loses the id link.

### 3. (SBA · MCP) `.mcp.json` for a local Python server you wrote uses which transport?
A. `http`  B. `stdio` with a `command` + `args`  C. `sse` with a `url`  D. `websocket`

> **Answer:** B.
> **Distractors:** A/C — remote transports. D — not an MCP transport.

### 4. (SCN · Tool Implementation) Two tools both say "use this to look up information in the database"; the model keeps picking the wrong one. Best fix?
A. force `tool_choice: "any"`  B. rewrite each description to say what it returns and, explicitly, when to use the *other* tool instead — or merge them behind a `type` parameter  C. delete one tool  D. raise `max_tokens`

> **Answer:** B — the ambiguity is the problem; an exclusion sentence per tool, or a merge, removes it.
> **Distractors:** A — **right-word-wrong-place**: forces *a* call, not the *right* one. C — loses a capability. D — irrelevant.

### 5. (SBA · Tool Implementation) A tool fails at runtime. You return the failure to the model as:
A. an exception that aborts the loop  B. a `tool_result` block with `is_error: true` and a short message  C. an empty `tool_result`  D. a `text` block apologising

> **Answer:** B — the model can then adapt or retry.
> **Distractors:** A — kills the loop. C — the model can't tell success from failure. D — not the protocol shape.

### 6. (SBA · Tool Implementation) `tool_choice: "any"` means:
A. the model may answer without any tool  B. the model must call **some** tool this turn  C. the model must call one **specific** tool  D. tools are disabled

> **Answer:** B.
> **Distractors:** A — that's `auto`. C — that's `tool` with a name. D — that's `none`.

### 7. (SBA · Tool Implementation) `readOnlyHint: true` on a custom tool:
A. makes it faster  B. opts it into concurrent execution alongside other read-only tools  C. makes its output cacheable  D. hides it from the model

> **Answer:** B — read-only tools can run in parallel; state-mutating tools run sequentially by default.
> **Distractors:** A/C/D — invented effects.

### 8. (SBA · MCP) An MCP server exposes which three kinds of capability?
A. only tools  B. resources (readable data), tools (callable functions), prompts (templates)  C. models, datasets, weights  D. endpoints, routes, handlers

> **Answer:** B.
> **Distractors:** A — undersells it. C/D — wrong vocabulary.

### 9. (SCN · MCP) Three internal apps each need the same "look up an employee in Workday" capability, and the Workday integration changes often. Build it as:
A. a copy-pasted in-process tool in each app  B. one MCP server exposing `lookup_employee`, consumed by all three  C. a vendored shared library in each app  D. a Claude Skill

> **Answer:** B — shared + frequently changing + independent maintenance = MCP server.
> **Distractors:** A/C — **duplication / overbuild**; three copies to maintain. D — **wrong-system**: a Skill adds no live data.

### 10. (SBA · MCP) "An MCP server is not a bag of tools." The practical implication:
A. servers can only have one tool  B. scope `allowed_tools` to what the app needs — a remote server may expose dozens  C. tools must be stateless  D. you can't write your own server

> **Answer:** B — least privilege at the tool level.
> **Distractors:** A/C/D — false.

### 11. (SBA · MCP) By default, an MCP server's tool schemas are:
A. loaded into context immediately at connect  B. deferred — loaded on demand to save context  C. never available to the model  D. cached for 24h

> **Answer:** B.
> **Distractors:** A — that's the cost the deferral avoids. C/D — invented.

### 12. (SCN · Agentic Customisation) A team wants Claude to always follow their 12-step incident-writeup format — no new data, just a consistent process. Best mechanism?
A. an MCP server  B. a Skill capturing the 12-step process  C. a longer system prompt pasted into every session  D. a custom tool

> **Answer:** B — repeatable process, no live data → Skill.
> **Distractors:** A/D — **wrong-system**: those are for data/actions. C — **symptom-treater**: doesn't scale, dilutes.

### 13. (SBA · Agentic Customisation) Complete the framework: "MCP connects Claude to ___; Skills teach Claude ___."
A. tools; hooks  B. data; what to do with that data  C. models; prompts  D. servers; clients

> **Answer:** B.
> **Distractors:** A/C/D — wrong pairing.

### 14. (MR · Agentic Customisation — choose the two that need *live external data*) Which needs a tool or MCP, not a Skill?
A. "check the current order status in our OMS"  B. "apply our code-review checklist"  C. "look up today's FX rate"  D. "format this text as our standard memo"

> **Answer:** A, C — both require fresh external data.
> **Distractors:** B, D — repeatable processes over content already in context → Skills.

### 15. (SBA · Tool Implementation) `strict: true` on a tool constrains:
A. the final text response  B. the tool's **arguments** to the schema via constrained decoding  C. how often the tool may be called  D. the tool's output

> **Answer:** B. (JSON outputs via `output_config.format` constrain the final response; `strict` constrains tool args.)
> **Distractors:** A — that's the other mechanism. C/D — not what `strict` does.

### 16. (SBA · dispatch) In a Claude Agent SDK loop, who executes a built-in or MCP tool call?
A. your application code, manually  B. the SDK harness  C. the model itself  D. Anthropic's servers, always

> **Answer:** B — harness dispatch; in a raw Messages API loop it's your code.
> **Distractors:** A — that's the manual-loop case. C — the model never executes. D — only for Anthropic-hosted server tools.
