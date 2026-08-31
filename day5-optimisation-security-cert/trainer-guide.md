# Day 5 — Trainer guide (slide-by-slide)

**Deck:** `slides/day5.html` (~27 slides) · **Recap:** `recap.html` · **Contact time:** ~4h + capstone + the mock
**Primary domains:** D5 (Model Selection & Optimisation, 16.8%) · D7 (Security & Safety, 8.1%) · D4 (wrap).
**Anchor episodes:** `ep10` `ep11` `ep12`. **Video:** walkthrough L3, L10, L11, L16, L17 · exam-guide D5 (18:16), D7 (23:56), Five ways to fail (28:30), Build plan (31:14).

---

## Before this session
- [ ] Day 4 recap quiz. Print the mock + key. Load the roster scorecard.
- [ ] Dry-run `code-snippets/prompt_caching.py` and `code-snippets/batch_custom_id.py` (batch takes a few minutes to end — start it before class).
- [ ] Confirm the mock's 90 minutes is protected in the room booking.

## Timing plan
| Block | Time |
|---|---|
| Recap quiz | 09:00–09:15 |
| M1 model selection + trade-offs + cascade + latency/throughput | 09:15–10:05 |
| M2 cost & token management (the five levers) | 10:05–10:35 *(break)* |
| M3 prompt caching + **Lab · prove the cache** | 10:50–11:35 |
| M4 batch + **Lab · batch keyed by custom_id** | 11:35–12:15 *(lunch)* |
| M5 reliability · M6 vision & documents | 13:15–14:00 |
| M7 security + **Lab · injection stops at a mechanism** + **Lab · secrets** | 14:00–15:10 *(break)* |
| M8 exam-day routine | 15:25–15:45 |
| **Capstone build + 3-min presentations** | 15:45–17:15 |
| — next day / afternoon — **the 53-item mock (90 min) + 45-min review** | — |

## If behind
1. Capstone → a design exercise on paper (name the decision + mechanism for each choice), not a build.
2. Vision & documents → the recap card + one exam-style question.
3. **Never cut:** the injection lab, the exam-day routine, and **the mock's 90 minutes**.

## Known failure modes
| Failure | Fix |
|---|---|
| caching lab: reads are 0 on the good run too | a per-request field (timestamp / uuid) leaked into the prefix; or the prefix is under the min cacheable size — enlarge it |
| batch lab: candidates index results by position | that's the whole point — force a dict keyed by `custom_id` |
| injection lab: the prompt-line version "works" | run it 5×; it fails intermittently — that's the lesson. The hook never fails. |
| "switch to the biggest model" as a cost fix | it's backwards; name the species (generic knob / true-but-irrelevant with a price tag) |

---

## Slide-by-slide (navigate by title)

### Title + orientation — 4 min · Decisions ② & ④.

### M1 · The trade-off triangle (Exam watch) — 6 min
- quality / latency / cost — pick 2. **Start capable, measure, step down.** Not "pick a tier by task type".
- The exam **prices** the decision: classifier at 1M/day → fast tier **+ route the hard cases up a tier**. **Cascading** — cheap first, escalate on failure.
- *Ref:* `ep10` · Build-along Ep 10 · exam-guide D5 (18:16).

### M1 · Latency vs throughput (Exam watch) — 5 min
- Chat cares about **time-to-first-token**; a pipeline cares about **docs/hour**.
- **Streaming changes *perceived* latency. Batch changes cost. Neither changes intelligence.**
- Every requirement (real-time / overnight / high-volume / budget cap) maps to one corner. The exam hands you requirements and watches if you find the corner.

### M2 · `input_tokens` is not your input (Exam watch) — 5 min
- The window bills your text + tool schemas + system + the generated output. Read `usage` every call. **Judge cost per completed task.**

### M2 · The five cost levers, in order (Exam watch) — 7 min
- The ladder SVG: **1 caching → 2 batch → 3 right-size the model → 4 cap output length → 5 trim prompt fat.**
- A scenario hands you a bill and asks what to pull **first** — read the workload's shape (repeated prefix → cache; overnight tolerance → batch).
- *Ref:* walkthrough L10 · exam-guide D5.

### M3 · Prefix match — stable first (Exam watch) — 7 min
- The prefix SVG. Render order `tools → system → messages`; stable before the breakpoint, volatile after.
- Any byte change in the prefix invalidates everything after it. Silent invalidators: `datetime.now()`, unsorted `json.dumps`, varying tool set.
- Verify with `usage.cache_read_input_tokens`. Read ≈ 0.1×; write ≈ 1.25×.
- *Ref:* `ep11` · Build-along Ep 11 · `code-snippets/prompt_caching.py`.

### **Lab · prove the cache** — 30 min
- Same 12 KB system prompt + varying question ×5 with a breakpoint; print the counters; then sabotage with `datetime.now()` in the prefix.

### M4 · Results in any order (Exam watch) — 6 min
- The batch SVG. ~50%, non-urgent. Poll to `ended`. **Key results by `custom_id`, never position.**
- "10,000 docs overnight, cost matters" → Batch (Rule 1). Not "run in parallel", not "cap tokens".
- *Ref:* walkthrough L11 · `code-snippets/batch_custom_id.py`.

### **Lab · batch keyed by custom_id** — 25 min
- ~8 classification requests with `custom_id`s → poll → collect into a dict keyed by `custom_id`.

### M5 · Three places a call can break — 6 min
- Before it leaves (400, fail fast) · in transit (429 `rate_limit` yours / `overloaded` theirs / connection — back off) · after 200 (truncation / `refusal` check `stop_details` / wrong shape validate).
- SDK retries 408/409/429/5xx + connection, `max_retries=2`. On streams, an error can arrive as an event mid-stream.
- *Ref:* walkthrough L9.

### M6 · An image is built-in tokens (Exam watch) — 5 min
- Image = patches of tokens → if you have the text, send the text. A PDF is billed **twice** (text + each page as an image). Animations count by first frame. `citations:{enabled:true}` on each `document` block.
- *Ref:* walkthrough L3.

### M7 · The attack arrives as a ticket (Exam watch) — 8 min
- The injection SVG. "must never" → guidance is dead. **Isolate the untrusted text + a blocking hook** on the dangerous tool.
- **A more capable model follows the injected instruction better too — tier is not the fix.**
- Layered defence: structure (external content is data) · least privilege (read-only agent ≠ write tool) · validate outputs before acting · human on irreversible steps.
- *Ref:* `ep04`/`ep05` hooks · walkthrough L16 · exam-guide D7 (23:56).

### M7 · Identity, secrets & keys — 4 min
- Keys in a secret store / `.env` + `.gitignore`, never the repo. **Key in a mobile app → a backend proxy, no exceptions.** Least-privilege PAT. `${VAR}` expansion. Self-hosted ≠ air-gapped.

### **Lab · injection stops at a mechanism** — 35 min + **Lab · secrets** 20 min
- Prompt-line vs blocking hook (run the prompt-line 5×, it fails intermittently; the hook never fails). Then move a hardcoded key to `.env` + `${VAR}`; `git grep` proves nothing remains.

### M8 · The routine, at speed (Exam method) — 6 min
- ~135 sec/item; flag past 2.5 min. Read the last sentence first. Name the decision → kill stale-API + generic-knob → if *must/never*, kill guidance → pick the mechanism → tie-break to cheaper/simpler/SDK-native. No blanks.
- The four distractor species, plus **the overbuild** — engineers' specialty.
- *Ref:* walkthrough L17 · exam-guide (33:16).

### Capstone (teams of 3–4) — 90 min build + 3 min/team
- Extend the Day 3 agent with one new tool + one hook + a config file + a 2-case eval. Present: which of the four decisions each choice was; which mechanism answered which constraint.

### The 53-item mock
- `mock-exam/mock-exam-A.md`, 90 min timed, individual. Then 45-min review — every missed item through the four-step attack; name each wrong option's species. Log per-domain % → the 4-week revision plan (`logistics/03 §8`).
