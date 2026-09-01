# Day 3 — Exam-style questions

12 items in CCDV-F style. Name **≥ 2 distractor species** before the reveal. Decision ①.
Domains: **D1** Agents & Workflows · **D8** Tools & MCPs · **D3** Claude Code · **D7** hooks.

---

**1. (SCN · D1)** Triage: classify → look up customer → draft reply. Same three steps, in
order, every ticket. The team proposes an autonomous agent with 12 tools. Best guidance?
A. build the agent — it's more capable  B. build a routed workflow — the path is fixed
C. don't automate reply drafting  D. use an agent framework's supervisor pattern

**2. (SBA · D1)** "Should I build an agent?" fails on which check for *"extract the invoice
total from this PDF"*?
A. viability  B. value  C. complexity  D. cost of error

**3. (MR · D1 — choose TWO)** Reasons to prefer a **workflow** over an agent for a fixed
sequence?
A. cheaper and faster  B. more capable  C. debuggable and testable  D. handles unpredictable
state better

**4. (SCN · D1)** An agent loops one turn too many and burns budget. Best fix?
A. add a supervising agent  B. an iteration cap + timeout + a termination condition
C. switch to a bigger model  D. lower the temperature

**5. (SBA · D1)** You want the request→execute→loop handled for you, over **your** tools, on
**your** infra, with per-turn approval hooks. Which?
A. a manual `while` loop  B. the SDK Tool Runner  C. Managed Agents  D. the Claude Agent SDK

**6. (SCN · D7)** "Ticket text must **never** be able to trigger the `refund` tool." Which
satisfies it?
A. a system-prompt line telling the model to ignore instructions in tickets  B. the most
capable model tier  C. treat ticket text as untrusted, keep it out of the instruction
channel, and put a **blocking `PreToolUse` hook** on `refund`  D. temperature 0

**7. (SBA · D7)** `PreCompact` is best used for:
A. blocking a tool call  B. observability — logging that context is about to be summarised
C. transforming a tool result  D. ending the conversation

**8. (SBA · D3)** A rules file's content reaches the model as:
A. the top-level `system` field  B. a `user` message  C. a `role:"system"` message  D. a
tool definition

**9. (SBA · D3)** Standing conventions the coding agent needs every session belong in:
A. every session prompt  B. the project memory / `CLAUDE.md` file  C. a tool description
D. the model's fine-tune data

**10. (SBA · D8)** `.mcp.json` for a local Python server you wrote uses transport:
A. `http`  B. `stdio` with a command + args  C. `sse` with a URL  D. `websocket`

**11. (SCN · D8)** Three teams each hand-wired the same internal customer-lookup
integration, three different bugs. Best move?
A. copy the least-buggy version around  B. one shared MCP server  C. each keeps its own for
independence  D. build an agent to manage the integrations

**12. (SBA · D7/D8)** Installing a plugin / marketplace bundle is:
A. sandboxed and safe by default  B. a trust decision — it runs code with your privileges,
like a dependency  C. read-only  D. reversible with no risk

---
---
## Answers & rationale  *(sample code in `code-snippets/`)*

**1 — B.** Fixed path → a workflow (cheaper, testable). **A — overbuild.** **C — extremist.**
**D — overbuild + true-but-irrelevant.** `cs:agent_loop_react`  
`refs: CB:wf-basic`


**2 — C.** Complexity — the task is single-step and fully specifiable, so no loop is needed.  
`refs: L21 E01`

**3 — A & C.** **B / D** describe an *agent's* strengths, not a workflow's.  
`refs: L21 R:workflow-patterns CB:wf-basic`

**4 — B.** Loop guardrails are the mechanism. **A — overbuild.** **C / D — generic knobs.**  
`refs: cs:agent_loop_react L21`

**5 — B.** Tool Runner = harness only, your tools, you host, per-turn hooks. C adds hosting;
D adds built-in tools; A makes you write the harness. `cs:blocking_hook`  
`refs: CB:sdk-host`


**6 — C.** Rule 2 — "must never" kills guidance (A). **B / D — generic knobs**, and a
stronger model follows the *injected* instruction better too. Only C is a mechanism.
`cs:blocking_hook`

**7 — B.** It's observability — too late to rescue anything that only lived in the
conversation.  
`refs: L20 R:context-management`

**8 — B.** The conversation channel. **C — right-word-wrong-place** (no such message).  
`refs: L26 R:claude-code-files`

**9 — B.** Standing knowledge goes in the config file, not re-told every session.  
`refs: L27 R:claude-code-config`

**10 — B.** A local server is a program: `stdio`, command + args. `cs:mcp_server`

**11 — B.** Crosses apps/teams → an MCP server. **A — symptom-treater. C —
true-but-irrelevant. D — overbuild.** `cs:mcp_server`  
`refs: CB:skills-intro`


**12 — B.** A plugin runs code with your privileges — a trust decision.

`refs: L27`

---
### Mark yourself
12 items · **≥ 10** = on track.  
