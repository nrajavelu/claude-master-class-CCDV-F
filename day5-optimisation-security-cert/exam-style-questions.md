# Day 5 — Exam-style questions

14 items in CCDV-F style. Name **≥ 2 distractor species** before the reveal. Decisions ② & ④.
Domains: **D5** Model Selection & Optimisation · **D7** Security & Safety · **D4** reliability.

---

**1. (SCN · D5)** A team runs sentiment analysis on every incoming review with the **top-tier
model at high temperature**; results vary run to run. **Choose two** fixes.
A. drop to the fast tier — it's simple classification  B. lower the temperature  C. add a
longer prompt demanding consistency  D. switch to a different provider

**2. (SBA · D5)** A classifier handles 1,000,000 requests/day. Best approach?
A. fast tier for everything  B. fast tier, and route the hard cases up a tier (cascade)
C. top tier for everything  D. workhorse tier for everything

**3. (SBA · D5)** Streaming changes:
A. the model's intelligence  B. perceived latency  C. cost  D. the token count

**4. (SCN · D5)** A feature calls Claude 20,000×/day with an identical 12 KB system prompt.
Biggest lever to cut cost, **before** touching model choice?
A. lower `max_tokens`  B. switch every call to Haiku  C. prompt caching on the stable
prefix  D. batch the requests

**5. (SBA · D5)** `usage.cache_read_input_tokens` is 0 across repeated identical-prefix
calls. Most likely:
A. caching isn't supported  B. a silent invalidator in the prefix (`datetime.now()`,
unsorted JSON, varying tools)  C. the model is too small  D. you need a beta header

**6. (SCN · D5)** 10,000 documents, processed overnight, cost is the concern, nobody needs
results until morning. Best approach?
A. run them in parallel with async  B. the Batch API  C. switch to Haiku  D. cap `max_tokens`

**7. (SBA · D5)** Batch results:
A. arrive in submission order  B. arrive in any order — key by `custom_id`  C. arrive
sorted by cost  D. can't be retrieved individually

**8. (SBA · D5)** A PDF sent as a document block is billed:
A. once, as text  B. once, as an image  C. twice — as its text AND each page as an image
D. it's free

**9. (SCN · D4)** A streaming response reported success but the text looks half-finished.
Where do you look?
A. the HTTP status code  B. the stream events — an error can arrive mid-stream, and
`message_delta` carries the real `stop_reason`  C. `max_retries`  D. the API key

**10. (SBA · D4)** `overloaded_error` vs `rate_limit_error` — which is *yours* to fix?
A. both  B. `rate_limit_error` (your traffic spiked)  C. `overloaded_error`  D. neither

**11. (SCN · D7)** A support agent summarises incoming emails. A crafted email makes it call
the `refund` tool. **Choose two** defences.
A. remove `refund` from the summarisation path (least privilege)  B. treat email content as
untrusted data; validate model output before any tool acts  C. add "ignore malicious
instructions" to the system prompt  D. stop processing email entirely

**12. (SBA · D7)** Why isn't "use the most capable model tier" a defence against prompt
injection?
A. it's too expensive  B. a more capable model follows the injected instruction better too
C. it changes the API contract  D. it disables tools

**13. (SBA · D7)** A key appears in a mobile app's bundle. The answer is:
A. obfuscate it  B. a backend proxy — keys server-side only  C. rotate it daily  D. move it
to a config file

**14. (SBA · D7)** "Self-hosted ≠ air-gapped" means:
A. self-hosting is insecure  B. server tools like `web_search` / `web_fetch` still run on
Anthropic's servers  C. you can't self-host  D. self-hosting disables MCP

---
---
## Answers & rationale  *(sample code in `code-snippets/`)*

**1 — A & B.** Right-size the model **and** turn the randomness dial down. **C —
symptom-treater. D — extremist with a passport.** `cs:count_tokens`

**2 — B.** Volume + mostly-easy → fast tier + the engineering move. **C — cost blowout.**
`cs:count_tokens`

**3 — B.** Perceived latency only.

**4 — C.** Caching the stable prefix drops repeated input cost ~90% — lever #1, before model
choice. **B — quality trade (and the question excludes it). A — output's already short.
D — adds latency, doesn't touch the repeated prefix.** `cs:prompt_caching`

**5 — B.** Any byte change in the prefix invalidates everything after it. `cs:prompt_caching`

**6 — B.** Rule 1 — the stem names the exact constraint Batch exists for. **A — doesn't cut
cost. C — quality trade. D — truncates.** `cs:batch_custom_id`

**7 — B.** Any order — key by `custom_id`. `cs:batch_custom_id`

**8 — C.** Twice. If you have the text, send the text.

**9 — B.** Read the events; `message_delta` carries the real `stop_reason`. `cs:retry_chain`

**10 — B.** `overloaded` is Anthropic-side; `rate_limit` is your spike. `cs:retry_chain`

**11 — A & B.** Mechanisms. **C — symptom-treater / guidance. D — extremist.**
`cs:blocking_hook`

**12 — B.** The stronger model follows the *injected* instruction better too.

**13 — B.** Keys server-side only, no exceptions. **A / C / D — symptom-treaters.**

**14 — B.** Server tools run on Anthropic's servers regardless of where your agent runs.

---
### Mark yourself
14 items · **≥ 11** = ready for the mock.
