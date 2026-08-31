# Day 4 — End-of-day quiz

12 questions, ~12 min. **≥ 9/12** — this is the 33% domain. Domains: **D2** Applications &
Integration · **D6** Context Engineering · **D4** Evaluation.

---

### Q1 (D2) Sort into functional vs infrastructure: "summarise every ticket"; "any engineer can roll back"; "read screenshots"; "runs on a shared server".
### Q2 (D2) What does "implement" mean in the systems life cycle?
### Q3 (D2) Where is production credit earned?
### Q4 (D2) Why is version control the mechanism behind "roll it back", and what's the guidance distractor?
### Q5 (D2) A scenario describes *where* Claude sits in a system. What is it really asking?
### Q6 (D2) Which interface needs streaming + session state your app maintains? Which is "probably a batch"?
### Q7 (D2) Three SW-eng foundations that back a production Claude integration.
### Q8 (D2) "A prompt edit IS a ___." Fill the blank, and say what that implies.
### Q9 (D2) A key is hardcoded in a mobile app. The fix?
### Q10 (D6) Name what the context window holds (four things), and the difference between compaction and context-editing.
### Q11 (D6) In RAG, what do you do when the answer isn't in the corpus?
### Q12 (D4) A regression test for a summariser should assert on ___ , not ___ . Why?

---
---
## Answer key
**Q1** — functional: "summarise every ticket", "read screenshots". infrastructure: "any
engineer can roll back", "runs on a shared server". *(D2)*

**Q2** — Deploy the finished thing **where users are** — not write the code. *(D2)*

**Q3** — In **operate + maintain**, never in develop. *(D2)*

**Q4** — VCS remembers every change, so rollback = pick the last good version (a mechanism).
The distractor: "write a setup document" — a doc is **guidance**. *(D2)*

**Q5** — Which **contract** applies: chat interface (streaming + session state) vs API
endpoint (its own timeout + error contract) vs background job (→ batch). *(D2)*

**Q6** — Chat interface → streaming + session state your app keeps. Background job →
probably a batch. *(D2)*

**Q7** — Any three of: idempotency, logging, separating the prompt layer from business
logic, validation + retries with backoff, a fallback path. *(D2)*

**Q8** — **a deployment.** So prompts are versioned artifacts, changed deliberately, tested
before rollout (run the golden set). *(D2)*

**Q9** — A **backend proxy** — keys server-side only, in env / a secrets manager. No
exceptions. *(D2)*

**Q10** — Your input + tool schemas + conversation history + the generated answer.
**Compaction** = summarise earlier context; **context-editing** = *clear* old tool-results /
thinking. *(D6)*

**Q11** — Say so ("not in the provided documents") — don't invent. *(D6)*

**Q12** — Assert on **structure + required content**, not **exact wording** — output varies
by design; test the contract. *(D4)*

---
### Scoring
| Score | Next |
|---|---|
| 10–12 | Solid on the biggest domain. |
| 8–9 | Re-read the module behind any miss. |
| ≤ 7 | Flag. Tonight: `question-bank/domain-2-applications-integration.md` + `scenario-questions.md` Q2/Q3/Q7 + walkthrough L4/L6/L8. |
