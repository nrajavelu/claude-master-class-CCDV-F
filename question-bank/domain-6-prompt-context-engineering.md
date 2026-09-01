# Domain 6 — Prompt and Context Engineering  ·  11%  ·  decision ③ "what does Claude see and say?"

> **Status: populated (18/18).** Anchor: `ep06`, `ep08`, `day2-.../labs/lab3_strict_output`.
> Video: lessons 7, 8, 9. Taught Day 2 Modules 1–4 (+ Day 4 context/RAG). Deeper prose:
> `../topic-briefings.md` · Day 2; checklist: `../blueprint-mastery-map.md` 6.1–6.3.

## Sub-areas & item split

| Sub-area | Weight | Items | Topics |
|---|---:|---:|---|
| Context Engineering | 3.8% | 6 | the window holds input + tools + tool output + generated output · a growing conversation is a growing request · **pruning/clearing** (re-fetchable) vs **compaction** (summarise dialogue/reasoning) vs the memory tool · `PreCompact` archives · "a bigger window makes it worse" if filled with stale tool results · subagents for context isolation · RAG as context curation |
| Prompt Engineering | 4.6% | 8 | contract in `system`, task + data in `messages` · long docs before the question · be explicit and positive · XML tags separate instruction from data · zero/one/multi-shot (= few-shot) — steers shape, not correctness, costs tokens every call · prefilling (incompatible with structured outputs; rejected on newest) · **no `role:"system"` message** · diagnosis over elaboration |
| Output Handling | 2.6% | 4 | steer shape in the prompt vs guarantee it with a schema · JSON outputs (`output_config.format`) vs `strict` tools · still check `stop_reason` · grammar-compile latency · unsupported schema features **rejected** · optional = nullable · `messages.parse()` · parse tool inputs with `json.loads`, never string-match |

---

## Items

### 1. (SBA · Prompt Engineering) A prototype in the chat product behaves well; the same instructions via the API behave differently. Best explanation?
A. different model  B. the chat product adds its own system prompt that doesn't apply to the API  C. default temperature differs  D. the API needs a `role: "system"` message

> **Answer:** B.
> **Distractors:** A/C — reach for a knob. D — **right-word-wrong-place**: no message has `role:"system"`.

### 2. (SBA · Context Engineering) Pruning/clearing vs compaction:
A. same thing  B. pruning drops re-fetchable tool output (lossless, cheap); compaction summarises dialogue/reasoning that can't be cheaply re-fetched  C. both delete messages permanently with no recovery  D. only compaction is server-side

> **Answer:** B.
> **Distractors:** A — different operations. C — pruned data is re-fetchable. D — invented.

### 3. (BUG · Output Handling) Your `strict` tool keeps failing validation on an "optional" field the schema marks optional by omitting it from `required`. Fix?
A. remove `strict`  B. keep it in `required` and allow `null` as a type — strict mode has no "optional"; optional = nullable  C. set `additionalProperties: true`  D. lower `max_tokens`

> **Answer:** B.
> **Distractors:** A — throws away the guarantee. C/D — unrelated.

### 4. (SCN · Context Engineering) A long-running agent's context is filling with full file texts it read pages ago and no longer needs. Right response?
A. compact (summarise) the whole context  B. prune the stale file-read tool results — they're re-fetchable  C. switch to a 1M-context model  D. lower `max_tokens`

> **Answer:** B — lossless and cheap for re-fetchable data.
> **Distractors:** A — **overbuild** here; burns a call, loses detail. C/D — **symptom-treater**.

### 5. (SBA · Prompt Engineering) Where do a long reference document and the actual question go?
A. question first, document after  B. document first, question at the end  C. both in `system`  D. both in one giant `user` string with no structure

> **Answer:** B — long context before the ask; delimit the document with XML tags.
> **Distractors:** A — worse for attention. C — data isn't a contract. D — no instruction/data separation.

### 6. (SBA · Prompt Engineering) Few-shot examples in a prompt:
A. permanently teach the model (like fine-tuning)  B. steer output format/style/edge-cases, cost tokens on every call, and don't lower cost  C. reduce token usage  D. are only for classification

> **Answer:** B.
> **Distractors:** A — they're not training. C — opposite. D — broadly useful.

### 7. (SCN · diagnosis) A classification prompt returns prose instead of one of four labels ~15% of the time; more instruction text hasn't helped. Best fix?
A. raise temperature  B. add an explicit output constraint ("respond with exactly one of: A,B,C,D") + 2–3 format examples  C. switch to a bigger model  D. retry until a valid label appears

> **Answer:** B — wrong shape → output constraint + format examples.
> **Distractors:** A — worse. C — **overbuild**. D — **symptom-treater**.

### 8. (SBA · Output Handling) With `output_config` JSON schema set, some responses still fail to parse; `stop_reason` on those is `max_tokens`. Cause?
A. the schema is invalid  B. the output was truncated mid-object — a schema can't prevent hitting the token cap  C. constrained decoding is unreliable  D. use prefilling with `{`

> **Answer:** B — raise `max_tokens` or shorten the required output; **always check `stop_reason`**.
> **Distractors:** A — schema is fine. C — **symptom-treater**. D — **stale-API**: prefilling is incompatible with structured outputs.

### 9. (SBA · Prompt Engineering) "Be explicit and positive" means:
A. use lots of exclamation marks  B. state what the model **should** do, not just what to avoid; leave no ambiguity for it to guess into  C. always be polite  D. keep prompts under 100 words

> **Answer:** B.
> **Distractors:** A/C — tone, not content. D — no such limit.

### 10. (SBA · Context Engineering) A conversation has run 40 turns and each new request is slow and expensive. Why?
A. the model degrades with age  B. the API is stateless — you resend the entire history every call, so the request grows every turn  C. rate limiting  D. the cache expired

> **Answer:** B.
> **Distractors:** A — false. C/D — unrelated to the growth.

### 11. (SBA · Output Handling) The first request against a brand-new JSON schema is noticeably slower than later ones. Why?
A. a bug  B. a one-off grammar-compile step for the schema, cached ~24h  C. cold model start  D. the schema is too big

> **Answer:** B.
> **Distractors:** A/C — invented. D — not the cause.

### 12. (SCN · Prompt Engineering) A prompt works on the happy path but breaks whenever the input contains a code block. Missing technique?
A. a bigger model  B. a constraint covering that input variant (and a few-shot example of it)  C. higher temperature  D. streaming

> **Answer:** B — cover the variant explicitly.
> **Distractors:** A — **overbuild**. C/D — **true-but-irrelevant**.

### 13. (SBA · Prompt Engineering) Prefilling the assistant turn with `{`:
A. is the recommended way to get JSON on the newest models  B. forces format from the first character, but is incompatible with structured outputs and rejected on the newest models  C. has no effect  D. is the same as `output_config.format`

> **Answer:** B.
> **Distractors:** A — **stale-API**. C — it does force format where accepted. D — different mechanism.

### 14. (SBA · Context Engineering) What is `CLAUDE.md` (or an equivalent persistent rules file) good for that compaction can't guarantee?
A. faster responses  B. rules that must be present on **every** request, re-injected regardless of what got summarised away  C. lower token cost  D. storing tool outputs

> **Answer:** B.
> **Distractors:** A/C — not its purpose. D — that's what pruning handles.

### 15. (SBA · Output Handling) You get the model's structured answer back and want a typed Python object without hand-parsing. Use:
A. `json.loads` on the raw text and hope  B. `client.messages.parse()` with your schema  C. a regex  D. `str.split`

> **Answer:** B.
> **Distractors:** A/C/D — brittle manual parsing.

### 16. (SCN · Context Engineering) A task genuinely needs to read 200 files to answer one question, and one loop would fill its context. Best structure?
A. a 1M-context model and read all 200 inline  B. a subagent that does the reading and returns only a summary to the parent  C. lower `max_tokens`  D. compact after every file

> **Answer:** B — context isolation: only the summary returns.
> **Distractors:** A — works until it doesn't, and costs a fortune. C — unrelated. D — churns model calls.

### 17. (SBA · Prompt Engineering) XML tags around a pasted document in the prompt do two jobs:
A. syntax highlighting and colour  B. separate instruction from data for the model, and form the first line of injection defence  C. compress the tokens  D. nothing — they're ignored

> **Answer:** B.
> **Distractors:** A/C — false. D — the model attends to them.

### 18. (SBA · Output Handling) Your schema uses a feature (e.g. `pattern` on a deeply nested field) the API doesn't support. What happens?
A. it's silently ignored  B. the request is **rejected** with a validation error — unsupported schema features are not dropped  C. the model approximates it  D. it works but slowly

> **Answer:** B.
> **Distractors:** A/C/D — assume graceful degradation that doesn't happen.
