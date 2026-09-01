# Mock exam A — Claude Certified Developer: Foundations

**53 items · 90 minutes · individual · no notes.** Multiple-choice and multiple-response;
each item states how many to select. Answers + rationale in `mock-exam-A-key.md` — don't
open it until you're done. Scoring guide and per-domain tally in `README.md`.

Original illustrations of the published question style — no real exam content.

---

### 1. Which is a **separate** endpoint, not a parameter of the Messages API call?
A. tool use  B. vision (image input)  C. counting tokens for a prompt  D. extended thinking

### 2. `response.content` on a normal reply is:
A. a string  B. a list of typed blocks  C. a dict keyed by block type  D. `None` unless you request text

### 3. (Choose TWO) Valid `stop_reason` values:
A. `end_turn`  B. `tool_call`  C. `max_tokens`  D. `content_filter`  E. `token_limit`

### 4. A call returns `stop_reason: "max_tokens"`, cut off mid-sentence, for a long report feature. Best fix?
A. retry the identical request  B. stream with a higher `max_tokens`  C. lower `max_tokens`  D. add a `\n\n` stop sequence

### 5. The Messages API is stateless. Multi-turn conversation therefore means:
A. it can't do chat  B. you resend the full history every request  C. responses aren't cached  D. tools are disabled

### 6. `client.messages.count_tokens(...)` accepts:
A. `model`, `system`, `messages`, `tools`  B. `model`, `max_tokens`, `messages`  C. a single string  D. the same params as `create`, incl. `max_tokens`

### 7. After a `with client.messages.stream(...) as stream:` block, get the complete Message via:
A. concatenating `stream.text_stream`  B. `stream.get_final_message()`  C. `stream.response` mid-flight  D. a second non-streaming call

### 8. Streaming on this API uses:
A. a WebSocket  B. Server-Sent Events over the same HTTP call  C. long polling  D. gRPC

### 9. (Choose ALL that apply) Worth retrying with backoff:
A. `RateLimitError` 429  B. `AuthenticationError` 401  C. `APIStatusError` 529  D. `BadRequestError` 400  E. `APIConnectionError`

### 10. The Anthropic SDK, by default:
A. never retries  B. retries every error forever  C. retries 408/409/429/5xx + connection with backoff, `max_retries=2`  D. retries only 429, once

### 11. `overloaded_error` vs `rate_limit_error` — which is yours to fix?
A. both  B. `rate_limit_error`  C. `overloaded_error`  D. neither

### 12. HTTP 200 with `stop_reason: "refusal"`; your code does `response.content[0].text` and crashes. Why?
A. bad key — catch `AuthenticationError`  B. on a refusal `content` may lack a text block; check `stop_reason` first  C. refusals raise `APIStatusError`  D. add `max_retries=5`

### 13. A batch pipeline's outputs are cut off on the longest documents. First move?
A. rewrite the prompt shorter  B. read `stop_reason` (`max_tokens`) and raise the output limit for those docs  C. switch to a bigger-context model  D. add a second pass that stitches truncated outputs

### 14. In a manual tool loop, immediately after receiving any response you must:
A. check `stop_reason` and return on `end_turn`  B. append `{"role":"assistant","content": response.content}`  C. append a `tool_result` user message  D. log `response.model_dump()`

### 15. One assistant turn has THREE `tool_use` blocks. To continue you append:
A. three user messages, one `tool_result` each  B. one user message, a list of three `tool_result` blocks, ids matching  C. one user message with the outputs concatenated as a string  D. one assistant message with the outputs

### 16. Chain-of-Thought vs ReAct — which is true?
A. they're the same  B. CoT is reasoning inside one turn; ReAct interleaves reasoning with tool calls across a loop  C. ReAct is a single API call  D. CoT requires the model to execute tools

### 17. For a high-volume ticket-classification route, adding "think step by step" to the prompt will most likely:
A. always improve accuracy  B. add latency and cost with little benefit — CoT helps reasoning tasks, not fixed-set classification  C. cause a 400  D. disable the model's own thinking

### 18. `thinking={"type":"enabled","budget_tokens":8000}` on a current model returns 400. Cause?
A. `max_tokens` must be ≥ 4096  B. `budget_tokens` < `max_tokens` required  C. `budget_tokens` thinking is removed on current models — use `{"type":"adaptive"}` + `effort`  D. `thinking` must be top-level, not a dict

### 19. Triage: classify → look up customer → draft reply. Same three steps, in order, every ticket. The team proposes an autonomous agent with a dozen tools. Best guidance?
A. build the agent — more capable  B. build a routed workflow — the path is fixed  C. don't automate reply drafting  D. use a framework supervisor pattern

### 20. (Choose TWO) Reasons to prefer a **workflow** over an agent for a fixed sequence:
A. cheaper and faster  B. more capable  C. debuggable and testable  D. handles unpredictable state better

### 21. Name the five workflow patterns. Which option lists only real ones?
A. chaining, routing, parallelisation, orchestrator-workers, evaluator-optimiser  B. chaining, caching, routing, batching, streaming  C. routing, RAG, fine-tuning, chaining, hooks  D. planning, acting, observing, reflecting, escalating

### 22. An agent loops one turn too many and burns budget. Best fix?
A. add a supervising agent  B. an iteration cap + timeout + a termination condition  C. switch to a bigger model  D. lower the temperature

### 23. You want the request→execute→loop handled for you, over YOUR tools, on YOUR infra, with per-turn approval hooks. Which?
A. a manual `while` loop  B. the SDK Tool Runner  C. Managed Agents  D. the Claude Agent SDK

### 24. Which option gives you BOTH a managed harness AND managed deployment?
A. manual loop  B. Tool Runner  C. Claude Agent SDK  D. Managed Agents

### 25. (Choose TWO) True of subagents in a fan-out:
A. each gets its own fresh context  B. more subagents always parallelise better  C. each can be given a narrower toolset and a cheaper model  D. subagents can't use tools

### 26. "Should I build an agent?" fails on which check for "extract the invoice total from this PDF"?
A. viability  B. value  C. complexity  D. cost of error

### 27. A prototype behaves well in the chat product; the same instructions via the API behave differently. Best explanation?
A. the API serves a different model  B. the chat product adds its own system prompt that doesn't apply to the API  C. default temperature differs  D. the API needs a `role:"system"` message

### 28. The most reliable place for "always reply in exactly three bullets":
A. the last line of every user message  B. the `system` field  C. an assistant message prefilled with `"- "`  D. `output_config={"style":"bullets"}`

### 29. (Choose TWO) Improve output *format-following*:
A. add "please be careful"  B. one or two few-shot `input → output` examples  C. raise the temperature  D. wrap inputs in tags and name the output sections

### 30. Where does a fetched web page / customer ticket belong in the request? And where must your own instructions never go?
A. `system` field / a `user` message  B. a `tool_result` block / a `tool_result` block  C. a `user` message / the `system` field  D. anywhere / anywhere

### 31. Prefilling on the newest models:
A. is the recommended structured-output approach  B. is rejected — use `output_config.format`  C. requires a beta header  D. only works with streaming

### 32. `strict: true` on a tool: your "optional" field (left out of `required`) keeps failing validation. Fix?
A. remove `strict`  B. keep it in `required` and allow `null` as a type  C. `additionalProperties: true`  D. lower `max_tokens`

### 33. An unsupported JSON-Schema feature in a `strict` tool definition is:
A. silently ignored  B. rejected (an error)  C. applied best-effort  D. auto-converted

### 34. An app parses Claude's JSON straight into a DB; once a day the model wraps the JSON in a sentence and the pipeline crashes. Best fix?
A. "OUTPUT ONLY JSON" in capitals  B. constrain the format (structured output / prefill) AND validate before writing, retry on parse failure  C. a person reviews every record  D. switch to a bigger model

### 35. `client.messages.parse()`:
A. streams the response  B. validates the response against your schema, returning a typed object or raising  C. counts tokens  D. is required for tool use

### 36. (Choose TWO) The context window holds:
A. your input  B. tool schemas  C. only what you mark with `cache_control`  D. the generated output

### 37. Compaction vs context-editing:
A. same thing  B. compaction summarises earlier context; context-editing clears old tool-results / thinking  C. both delete messages permanently  D. only compaction is server-side

### 38. A long-running agent's answers degrade; its context is full of hour-old tool results. Best move?
A. a bigger-context model  B. context-editing to clear stale results (and/or a fresh session per task)  C. raise `max_tokens`  D. lower temperature

### 39. When RAG vs long-context vs fine-tuning?
A. always fine-tune for accuracy  B. retrieve when the knowledge is large / changing / must be cited  C. always stuff everything in  D. RAG only works for code

### 40. Your RAG answerer invents a fact not in the retrieved documents. Best fix?
A. a bigger model  B. strengthen the grounding ("answer only from the provided docs; if absent, say so") and require doc-id citations  C. retrieve more chunks  D. raise temperature

### 41. A regression test for a summariser should:
A. assert the exact output string  B. assert required structure + key content, not wording  C. lower `max_tokens` for determinism  D. pin the temperature

### 42. An LLM-as-judge check is best written as:
A. "score this 1–10"  B. a single yes/no criterion  C. "is this good?"  D. a free-text critique

### 43. "Any engineer must be able to deploy it and roll it back." This requirement is:
A. functional  B. infrastructure  C. a bug  D. out of scope

### 44. "Implement" in the systems life cycle means:
A. write the code  B. deploy the finished thing where users are  C. design the architecture  D. retire the system

### 45. Three engineers, one repo, different behaviour every run. The team requires the same model version and rules every run. Best move?
A. rewrite it in a faster language  B. write a long setup document  C. pin the model version and commit the rules/config to version control  D. add missing features first

### 46. A key appears in a mobile app's bundle. The answer is:
A. obfuscate it  B. a backend proxy — keys server-side only  C. rotate it daily  D. move it to a bundled config file

### 47. A scenario describes Claude sitting behind a REST endpoint other services call. The design most needs:
A. streaming  B. its own timeout + error contract (validation, retries, a fallback)  C. a chat session store  D. a bigger model

### 48. A nightly job summarises thousands of documents with the same system prompt; costs are climbing; nobody reads results before morning. (Choose TWO.)
A. move to the Batch API  B. switch every call to the top-tier model  C. cache the shared prompt prefix  D. rewrite the summaries shorter

### 49. Batch results:
A. arrive in submission order  B. arrive in any order — key by `custom_id`  C. arrive sorted by cost  D. can't be retrieved individually

### 50. A classifier handles 1,000,000 requests/day. Best approach?
A. fast tier for everything  B. fast tier, and route the hard cases up a tier (cascade)  C. top tier for everything  D. workhorse tier for everything

### 51. Streaming changes ___ ; batch changes ___ ; neither changes ___ .
A. cost / latency / tokens  B. perceived latency / cost / the model's intelligence  C. intelligence / latency / cost  D. tokens / tokens / tokens

### 52. `usage.cache_read_input_tokens` is 0 across repeated identical-prefix calls. Most likely:
A. caching isn't supported  B. a silent invalidator in the prefix (`datetime.now()`, unsorted JSON, varying tools)  C. the model is too small  D. you need a beta header

### 53. A support agent that summarises emails can be made to call the `refund` tool by a crafted email. (Choose TWO best defences.)
A. remove `refund` from the summarisation path (least privilege)  B. treat email content as untrusted data and validate model output before any tool acts  C. add "ignore malicious instructions" to the system prompt  D. stop processing email

---

*When you finish: mark against `mock-exam-A-key.md`, log per-domain % on the roster, then
walk every miss through the four-step attack (`../../logistics/05-exam-method.md`).*
