# Domain 6 — Prompt and Context Engineering  ·  11%  ·  decision ③ "what does Claude see and say?"

> **Status: blueprint.** Item target **18**. Built pass 2/3 alongside Days 2 & 4.
> Anchor: `ep06`, `ep08`. Video: lessons 7, 8, 9.

## Sub-areas & item split

| Sub-area | Weight | Items | Topics |
|---|---:|---:|---|
| Context Engineering | 3.8% | 6 | the window holds input + tools + output · a growing conversation is a growing request · compaction (summarise) vs context-editing (clear) vs the memory tool · "a bigger window makes it worse" if filled with stale tool results · one session per task; `clear` / `compact` / `inspect` |
| Prompt Engineering | 4.6% | 8 | contract in `system`, task+data in `messages` · be explicit · XML structure separates instruction from data · zero/one/multi-shot (a.k.a. few-shot) · thinking/effort · **no `role: "system"` message** · the three surfaces and what transfers |
| Output Handling | 2.6% | 4 | steer shape in the prompt vs guarantee it with a schema · `strict` / `output_config.format` / `messages.parse()` · unsupported schema features are **rejected** · parse tool inputs with `json.loads`, never string-match |

## Seed items

### 1. (SBA · Prompt Engineering) A prototype in the chat product behaves well; the same
instructions via the API behave differently. Best explanation?
A. different model  B. the chat product adds its own system prompt that doesn't apply to the
API  C. default temperature differs  D. the API needs a `role: "system"` message

> **Answer:** B. (A and C are "reach for a knob"; D is right-word-wrong-place.)

### 2. (SBA · Context Engineering) Compaction vs context-editing:
A. same thing  B. compaction summarises earlier context; context-editing clears old
tool-results/thinking  C. both delete messages permanently  D. only compaction is server-side

> **Answer:** B.

### 3. (BUG · Output Handling) Your `strict` tool keeps failing validation on an optional
field. The schema marks it optional by omitting it from `required`. Fix?
A. remove `strict`  B. keep it in `required` and allow `null` as a type — strict mode has no
"optional", optional = nullable  C. set `additionalProperties: true`  D. lower `max_tokens`

> **Answer:** B.
