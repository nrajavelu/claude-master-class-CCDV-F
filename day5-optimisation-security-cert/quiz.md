# Day 5 — End-of-day quiz

12 questions, ~12 min. **≥ 9/12**. Domains: **D5** Model Selection & Optimisation · **D7**
Security & Safety · **D4** reliability.

---

### Q1 (D5) The trade-off triangle — name the three corners, and the exam's preferred approach to choosing.
### Q2 (D5) A classifier handles 1M requests/day. Which tier — and what's the engineering move the scoring answer adds?
### Q3 (D5) What does streaming change? What does batch change? What does neither change?
### Q4 (D5) The five cost levers, in order of power.
### Q5 (D5) `cache_read_input_tokens` is 0 across repeated identical-prefix calls. Most likely cause, and two examples.
### Q6 (D5) Batch: cost basis, and how you must key the results.
### Q7 (D5) Why is `input_tokens` "not your input"?
### Q8 (D4) `rate_limit` vs `overloaded` — which is yours to fix?
### Q9 (D5) A PDF sent as a document block is billed how?
### Q10 (D7) "Ticket text must never trigger the refund tool." Two mechanisms that satisfy it.
### Q11 (D7) Why isn't "switch to the most capable model" a fix for prompt injection?
### Q12 (method) The four distractor species + the developer exam's specialty.

---
---
## Answer key
**Q1** — quality / latency / cost (pick 2). Approach: **start capable, measure on real
requests, step down only when quality holds.** Not "pick a tier by task type". *(D5)*

**Q2** — The **fast tier**, and **route the hard cases up a tier** (cascade — cheap first,
escalate on failure). *(D5)*

**Q3** — Streaming changes **perceived latency**. Batch changes **cost**. Neither changes
the model's **intelligence**. *(D5)*

**Q4** — 1 caching · 2 batch · 3 right-size the model per task · 4 cap output length · 5 trim
prompt fat. *(D5)*

**Q5** — A silent invalidator in the prefix. Examples: `datetime.now()` / a per-request UUID
in the system prompt; unsorted `json.dumps`; a varying tool set. *(D5)*

**Q6** — ~50% cost, for non-latency-sensitive work. Results come back in **any order** — key
them by **`custom_id`**, never position. *(D5)*

**Q7** — It includes tool schemas + system + conversation history + the generated output —
not just the text you "typed". *(D5)*

**Q8** — **`rate_limit`** — your traffic spiked, yours to fix. `overloaded` is Anthropic-side
load. Both: back off and retry. *(D4)*

**Q9** — **Twice** — once as its text, once as each page rendered to an image. If you have
the text, send the text. *(D5)*

**Q10** — Isolate the ticket text (untrusted → `tool_result`, out of the instruction
channel) **and** a **blocking `PreToolUse` hook** on `refund`. Least privilege also applies
(a summarisation agent shouldn't hold a write tool). *(D7)*

**Q11** — A more capable model follows the **injected** instruction better too. The fix is a
mechanism (isolation / hook / validation), not a knob. *(D7)*

**Q12** — Extremist · symptom-treater · true-but-irrelevant · **overbuild** (more machinery
than the problem deserves — engineers are the most vulnerable). *(method)*

---
### Scoring
| Score | Next |
|---|---|
| 10–12 | Ready for the mock. |
| 8–9 | Revise the module behind any miss before the mock. |
| ≤ 7 | Flag. `question-bank/domain-5-*.md` + `domain-7-*.md` + `code-snippets/prompt_caching.py` · `batch_custom_id.py`. |
