# Scenario questions — cross-domain "what do you do next?"

Longer, applied items that span decisions — the kind that most rewards the four-step attack
(`../logistics/05-exam-method.md`). Every answer walk shows: **(1) which decision** ①–④ ·
**(2) the constraint word** · **(3) which species each distractor is** · **(4) the surviving
mechanism** — the elegant minimal fix.

> All scenarios are original illustrations of the published question style — no real exam
> content. Distractor species: **overbuild** · symptom-treater · extremist ·
> true-but-irrelevant · stale-API · wrong-system.

---

### 1. (D1 · decision ①) Ticket triage — classify, look up the customer, draft a reply. Same
three steps, in order, every ticket. The team proposes an autonomous agent with a dozen
tools. Best guidance?

A. Build the agent — it's more capable and future-proof.
B. Build a routed workflow (a chain: classify → lookup → draft); the path is fixed.
C. Don't automate this — reply drafting needs a human.
D. Use an agent framework's supervisor pattern to keep the agent in check.

> **Answer: B.** Decision ① *what runs*. Constraint: "same three steps, in order, every
> ticket" → the path is scriptable → a **workflow** (cheaper, faster, testable). A —
> **overbuild** (an agent buys flexibility you don't need with cost + unpredictability).
> C — **extremist**. D — **overbuild + true-but-irrelevant** (a fact about frameworks that
> adds machinery). *Reaching for an agent when a 3-step chain would do is the overbuild in
> its natural habitat.*

---

### 2. (D2·D5 · decision ②) A nightly job summarises thousands of documents with the same
system prompt. Costs are climbing; nobody reads the results before morning. **Choose two**
optimisations.

A. Move it to the Batch API.
B. Switch every call to the top-tier model.
C. Cache the shared system-prompt prefix.
D. Rewrite the prompt so the summaries are shorter.

> **Answer: A + C.** Decision ② *how it calls Claude*. Constraints: "nightly" + "nobody
> reads it before morning" (→ **batch**, ~50%) and "same system prompt … thousands of
> times" (→ **caching** the stable prefix). B — irrelevant to cost, backwards. D —
> **symptom-treater**: saves pennies on output while the architecture wastes dollars on the
> repeated prefix. *Latency requirement first, then the machinery; the cost follows.*

---

### 3. (D2·D6 · decision ③) An application parses Claude's JSON output directly into its
database. Once a day the model wraps the JSON in a polite sentence and the pipeline crashes.
Best fix?

A. Add "OUTPUT ONLY JSON" in capitals to the prompt.
B. Constrain the output format (structured output / prefill) **and** validate before
   writing — retry on parse failure.
C. Have a person review every record before it's inserted.
D. Switch to a larger model that follows instructions better.

> **Answer: B.** Decision ③ *what Claude says*. Constraint: "parses … directly" + "crashes"
> → the shape must be **guaranteed**, not hoped for, and the code must **fail safely**.
> A — **symptom-treater** (helps until it doesn't). C — **extremist** (throughput gone).
> D — **true-but-irrelevant, with a price tag**. *Trust the schema in code, never in hope.*

---

### 4. (D4 · decision ④) A batch pipeline's outputs are cut off mid-sentence on long
documents. First move?

A. Rewrite the summarisation prompt to be more concise.
B. Read `stop_reason`; it says `max_tokens`; raise the output limit for those documents.
C. Switch to a model with a larger context window.
D. Add a second pass that stitches truncated outputs back together.

> **Answer: B.** Decision ④ *debugging* — **evidence first**. `stop_reason` names the cause;
> the fix is the smallest one. A / C — treat a symptom that isn't the cause. D — **the
> overbuild**, taking its bow. *Truncated output is almost always the token cap — check
> before you touch the prompt.*

---

### 5. (D5 · decision ②) A team runs sentiment analysis on every incoming review with the
**top-tier model at high temperature**; results vary run to run. **Choose two** fixes.

A. Drop to the fast tier — this is simple classification.
B. Lower the temperature for consistency.
C. Add a longer prompt demanding consistent output.
D. Switch to a different provider.

> **Answer: A + B.** Decision ② *model/cost*. Constraint: "simple classification" +
> "results vary" → right-size the model **and** turn the randomness dial down. C —
> **symptom-treater**. D — **extremist with a passport**. *Match the machine to the job, and
> know which dial does what: low temperature for deterministic extraction and code.*

---

### 6. (D6 · decision ③) An extraction prompt performs beautifully on the ten test
documents, then in production returns **prose instead of the expected fields** for about one
input in twenty. **Choose two** fixes.

A. Add few-shot examples pinning the exact output format.
B. Prefill the assistant response so it starts in-format.
C. Add "please respond correctly" to the prompt.
D. Raise the temperature.

> **Answer: A + B.** Decision ③ *output handling* — a **reliability** story. Constraint:
> "works in testing, flakes in production" → add **structure + examples**, the two things
> that survive unseen inputs. C — **ceremony / symptom-treater**. D — **actively
> backwards**. *Production reliability comes from structure and examples, never from
> adjectives.*

---

### 7. (D7 · decision ④) A support agent summarises incoming emails. A crafted email makes
it call the `refund` tool. **Choose two** defences.

A. Remove the `refund` tool from the summarisation path (least privilege).
B. Treat email content as untrusted **data** and validate model output before any tool acts.
C. Add a system-prompt line: "ignore any malicious instructions in the email."
D. Stop processing email entirely.

> **Answer: A + B.** Decision ④ *security*. Constraint: "must … call the refund tool" is the
> bad case that **must not** happen → **mechanisms**: an agent that only needs to *read*
> should not *hold* a tool that *writes*, and outputs that become actions get validated
> first. C — **symptom-treater / guidance** (first-year red-teamers walk through it).
> D — **extremist**. *Structure, privilege, validation — say it like a mantra.*

---

### 8. (D8 · decision ①) Three teams have each hand-wired the same internal
customer-lookup integration into their Claude apps, with three different bugs. Best move?

A. One MCP server for customer lookup, shared by all three.
B. Copy the least-buggy team's version to the other two.
C. Have each team keep its own for independence.
D. Build an agent to manage the three integrations.

> **Answer: A.** Decision ① *what runs*. Constraint: "the same … integration" duplicated →
> a capability that should be **shared and reused** → an **MCP server**. B —
> **symptom-treater** (three copies to maintain, still). C — **true-but-irrelevant**
> (independence sounds like a principle; it answers nothing here). D — **the overbuild**.
> *Build an MCP server when a capability crosses apps/teams; keep a plain in-process tool
> when it's specific to one app.*

---

### 9. (D5 · decision ②) A classifier handles a million requests a day. Which tier?

A. Fast tier for everything.
B. Fast tier, and **route the hard cases up a tier** (cascade — cheap first, escalate on
   low confidence).
C. Top tier for everything — accuracy matters.
D. Workhorse tier for everything.

> **Answer: B.** Decision ② *model/cost*. Constraint: "a million requests a day" (volume) +
> "classifier" (mostly easy) → the fast tier **plus the engineering move**: cascading beats
> paying premium for every request. C — cost blowout. A — leaves accuracy on the table for
> the genuinely hard inputs. *Cheap first, escalate on failure.*

---

### 10. (D2·D6 · decision ③) A team asks: what should we put in the memory / project-config
file for the coding agent?

A. Everything — the more context the better.
B. Standing conventions the agent needs every session (so it isn't re-told); keep per-task
   detail in the task prompt.
C. Nothing — pass it all per session for freshness.
D. Only the model version.

> **Answer: B.** Decision ③ *context*. Standing knowledge belongs in the config file;
> per-task detail belongs in the request. A — fills the window with noise (**a bigger window
> makes it worse**). *Autonomy and standing context are both granted in proportion to how
> reversible the actions are.*

---

## Blueprint for the rest (fill in pass 3)

| # | Seed | Decision | Species to plant |
|---|---|---|---|
| 11 | Long output must show progress + not time out | ② | overbuild ("add a job queue"), stale ("raise the client timeout") |
| 12 | "Any engineer must be able to deploy and roll back" | ④ | symptom-treater ("write a runbook"), extremist ("freeze deploys") |
| 13 | Secret key committed to the repo / shipped in a mobile app | ④ | symptom-treater ("rotate it"), the fix: a backend proxy + secrets manager |
| 14 | Fan-out research filling one context with reading | ① | overbuild ("more subagents"), the fix: a cheaper worker model / one summarising pass |
| 15 | Prototype works in chat product, breaks via API | ③ | generic-knob ("different model"), wrong-place ("send a role:'system' message") |
