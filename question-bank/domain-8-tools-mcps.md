# Domain 8 — Tools and MCPs  ·  10.6%  ·  decision ① "what runs?"

> **Status: blueprint.** Item target **16**. Built pass 2 alongside Days 2 & 3.
> Anchor: `ep03`, `ep09`. Video: lessons 12, 13.

## Sub-areas & item split

| Sub-area | Weight | Items | Topics |
|---|---:|---:|---|
| Tool Implementation | 4.4% | 7 | tool schema (`name` / `description` / `input_schema`) · **the description is the interface** — biggest factor in correct use · `tool_choice` · parallel tool_use → one user message of `tool_result` blocks, ids matching · `is_error` · `strict` tools · client-side vs server-side (Anthropic-hosted) tools |
| MCP Server Development | 2.1% | 3 | MCP is a protocol, not a library · FastMCP stdio server · `.mcp.json` shapes (stdio / http / sse) · env-var expansion for secrets · "an MCP server is not a bag of tools" — scope the toolset |
| Agentic Customisation | 4.1% | 6 | hooks · sub-agents · skills · plugins (carry skills+hooks+subagents+servers) · `allowed_tools` scoping · marketplace → install order · plugin = code with your privileges |

## Seed items

### 1. (SCN · Tool Implementation) The model calls your `refund` tool at the wrong time.
First thing to check?
A. the model tier  B. the tool's **description** — is it detailed about *when* to use it and
what the inputs mean  C. `temperature`  D. `max_tokens`

> **Answer:** B. "An extremely detailed description is by far the biggest factor in whether
> the model uses a tool well."

### 2. (MR · Tool Implementation — choose TWO) One assistant turn has 3 `tool_use` blocks. To
continue you must:
A. reply with one user message containing 3 `tool_result` blocks
B. put each `tool_result` in its own message
C. match each `tool_result`'s `tool_use_id` to its `tool_use`
D. concatenate the outputs into one string

> **Answer:** A, C. (B trains the model to stop parallelising; D loses the id link.)

### 3. (SBA · MCP) `.mcp.json` for a local Python server you wrote uses which transport?
A. `http`  B. `stdio` with a `command` + `args`  C. `sse` with a `url`  D. `websocket`

> **Answer:** B.
