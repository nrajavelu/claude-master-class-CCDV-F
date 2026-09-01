# Day 4 — Exam-style questions

15 items — this is the **33% day**, so it earns the biggest set. Name **≥ 2 distractor
species** before the reveal. Decisions ③ & ④. Domains: **D2** (Requirements · Life Cycle ·
SW-Eng · Application Design · Configuration Management) · **D6** Context Engineering ·
**D4** Evaluation.

---

**1. (SBA · D2)** "Any engineer must be able to deploy it and roll it back." This requirement
is:
A. functional  B. infrastructure  C. a bug  D. out of scope

**2. (SBA · D2)** "Implement" in the systems life cycle means:
A. write the code  B. deploy the finished thing where users are  C. design the architecture
D. retire the system

**3. (SCN · D2)** Three engineers, one repo, different behaviour every run. The team requires
every run use the same model version and rules. Best move?
A. rewrite it in a faster language  B. write a long setup document  C. pin the model version
and commit the rules/config to version control  D. add the missing features first

**4. (SBA · D2)** A key is hardcoded in a mobile app. The fix?
A. obfuscate it  B. move it to a config file shipped with the app  C. a backend proxy — keys
server-side only  D. rotate it weekly

**5. (SCN · D2)** A scenario describes Claude sitting behind a REST endpoint other services
call. What does the design most need?
A. streaming  B. its own timeout + error contract (validation, retries, a fallback)
C. a chat session store  D. a bigger model

**6. (SBA · D2)** "A prompt edit is a ___":
A. free change  B. deployment — versioned, tested before rollout  C. runtime tweak, no
review needed  D. model upgrade

**7. (SCN · D2)** A nightly job summarises thousands of documents with the same system
prompt; costs are climbing; nobody reads results before morning. **Choose two.**
A. move to the Batch API  B. switch every call to the top-tier model  C. cache the shared
prompt prefix  D. rewrite the summaries to be shorter

**8. (MR · D2 — choose TWO)** Software-engineering foundations that back a production Claude
integration:
A. idempotency  B. maximising the context window  C. logging the full request + response
D. always using the newest model

**9. (SBA · D6)** The context window holds:
A. only your input  B. your input + tool schemas + conversation history + the generated
output  C. only the system prompt and messages  D. only what you mark with `cache_control`

**10. (SBA · D6)** Compaction vs context-editing:
A. same thing  B. compaction summarises earlier context; context-editing **clears** old
tool-results / thinking  C. both delete messages permanently  D. only compaction is
server-side

**11. (SCN · D6)** A long-running agent's answers are degrading; its context is full of
hour-old tool results. Best move?
A. a bigger-context model  B. context-editing to clear stale tool results (and/or a fresh
session per task)  C. raise `max_tokens`  D. lower the temperature

**12. (SBA · D6 · RAG)** When RAG vs long-context vs fine-tuning?
A. always fine-tune for accuracy  B. retrieve when the knowledge is large / changing / must
be cited  C. always stuff everything into the context  D. RAG only works for code

**13. (SCN · D6 · RAG)** Your RAG answerer invents a fact not in the retrieved documents.
Best fix?
A. a bigger model  B. strengthen the grounding instruction: "answer only from the provided
docs; if absent, say so" — and require doc-id citations  C. retrieve more chunks  D. raise
the temperature

**14. (SBA · D4)** A regression test for a summariser should:
A. assert the exact output string  B. assert required structure + key content, not wording
C. lower `max_tokens` for determinism  D. pin the temperature

**15. (SBA · D4)** An LLM-as-judge check is best written as:
A. "score this answer 1–10"  B. a single yes/no criterion ("does the answer follow only from
the cited docs?")  C. "is this good?"  D. a free-text critique

---
---
## Answers & rationale

**1 — B.** Infrastructure = what it runs on **and** what the team must be able to do to it.  
`refs: L30`

**2 — B.** Deploy where users are. Production credit is operate + maintain.  
`refs: L30`

**3 — C.** Rule 2 — a doc is guidance; committed, pinned config is the mechanism. **A —
overbuild. B — symptom-treater. D — the story of how it got broken.**  
`refs: L29`

**4 — C.** Keys server-side only. **A / B — symptom-treaters** (still shipped). D helps but
isn't the fix.  
`refs: L35`

**5 — B.** An API endpoint needs its own timeout + error contract. **A / C** belong to a
chat interface. **D — generic knob.**  
`refs: cs:retry_chain L30`

**6 — B.** Versioned, tested before rollout — run the golden set.  
`refs: L29`

**7 — A & C.** "Nightly / nobody reads it till morning" → batch; "same system prompt … many
times" → cache the prefix. **B — backwards. D — symptom-treater** (pennies on output while
the architecture wastes dollars).  
`refs: cs:batch_custom_id cs:prompt_caching L14 L15 CB:batch`

**8 — A & C.** **B / D** are anti-patterns dressed as advice.  
`refs: L30`

**9 — B.** All of it is billed — "input_tokens is not your input".  
`refs: cs:count_tokens L19 CB:ctx-eng`

**10 — B.** Summarise vs clear. The memory tool is a third option.  
`refs: R:context-management L20 CB:ctx-eng`

**11 — B.** Clear the stale context (a mechanism). **A — overbuild.** **C / D — generic knobs.**  
`refs: R:context-management L20`

**12 — B.** Retrieve when knowledge is large / changing / must be cited. A / C are
extremist.  
`refs: L19 CB:rag`

**13 — B.** Grounding + citation is the mechanism. **A / C — overbuild-ish.** **D — backwards.**  
`refs: L19 CB:rag`

**14 — B.** Test the contract; wording varies by design. C / D try to force determinism the
model doesn't guarantee.  
`refs: L37 CB:build-evals`

**15 — B.** A crisp yes/no criterion is repeatable; a 1–10 score is not.

`refs: L37 CB:build-evals`

---
### Mark yourself
15 items · **≥ 12** = on track for the heaviest domain. Any sub-area < 60% → revise tonight.  
