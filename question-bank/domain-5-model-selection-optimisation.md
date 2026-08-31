# Domain 5 — Model Selection and Optimisation  ·  16.8%  ·  decision ② "how does it call Claude?"

> **Status: blueprint.** Item target **26**. Built pass 3 alongside Day 5 (some Day 1).
> Anchor: `ep10`, `ep11`. Video: lessons 2, 3, 10.

## Sub-areas & item split

| Sub-area | Weight | Items | Topics |
|---|---:|---:|---|
| LLM Fundamentals | 5.2% | 8 | next-token generation · no plan behind it · tokens ≠ words · sampling / variation · the context window is the model's whole world · stateless API |
| Technical Fundamentals | 6.1% | 9 | REST/JSON under the SDK · SSE streaming (not WebSocket) · async / parallel vs batch · retries built in · request/response fields (`stop_reason`, `usage`) · image = patches of tokens · PDF = text + page images |
| Model Selection & Trade-offs | 2.7% | 4 | quality/latency/cost triangle · "start capable, measure, step down" · `effort` levels · when thinking earns its cost |
| Cost & Token Management | 2.8% | 5 | `input_tokens` is not "your input" · usage tracking · **cost-optimisation order** (caching → input hygiene → loop/output hygiene → batch → budgets → effort → model → multi-model) · prompt caching prefix rules & silent invalidators · batch ≈ 50%, any-order results keyed by `custom_id` |

## Seed items

### 1. (SBA · LLM Fundamentals) Same prompt, run twice, different wording. This is:
A. a bug  B. expected — generation samples among plausible continuations  C. a cache miss
D. a rate-limit artefact

> **Answer:** B. Design for variation (assert on structure).

### 2. (SBA · Technical Fundamentals) Streaming on this API uses:
A. a WebSocket  B. Server-Sent Events over the same HTTP call  C. long polling  D. gRPC

> **Answer:** B. An option offering a WebSocket is a distractor wearing the guide's own word.

### 3. (SCN · Cost) 10,000 documents, processed overnight, cost is the concern, nobody needs
results until morning. Best mechanism?
A. run them in parallel with async  B. the Batch API  C. switch to Haiku  D. cap `max_tokens`

> **Answer:** B. Rule 1: the stem names the constraint (overnight, cost, not urgent) → the
> mechanism built for it. The other three are generic knobs.

### 4. (SBA · Cost) `cache_read_input_tokens` is 0 across repeated identical-prefix calls.
Most likely:
A. caching isn't supported  B. a silent invalidator in the prefix (`datetime.now()`, unsorted
JSON, varying tools)  C. the model is too small  D. you need a beta header

> **Answer:** B.
