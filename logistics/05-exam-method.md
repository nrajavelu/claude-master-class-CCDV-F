# The exam method — how to read and kill a CCDV-F question

> Teach this on **Day 1** and use it on **every** worked question for the rest of the week.
> It is the single highest-leverage thing in the whole program: it turns "do I remember this
> fact?" into "which decision is this, and which option is a *mechanism*?"
>
> Source of the framing: the CCDV-F exam guide's own three published sample questions and
> their printed rationales, plus the community video companion (see `../video-companion.md`).
> We are not inventing a trick — we are using the grader's own logic.

---

## 1. Every question is one of four decisions

The exam's **8 domains** and **25 weighted skill statements** map onto **four decisions you
make whenever you build with Claude**. Naming the decision sorts the options before you know
a single fact. (The public video companion builds one support-desk system across 17 lessons
in blueprint order and stamps every skill onto its decision — see `../video-companion.md`.)

| # | Decision | "It's asking about…" | Domains it draws from | ≈ items / 53 |
|---|---|---|---|---:|
| ① | **What runs?** | workflow vs agent · one loop vs supervisor + sub-agents · a capability that's built-in vs written by you vs plugged in | **D1** Agents & Workflows (14.7%) · **D8** Tools & MCPs (10.6%) | ~13 |
| ② | **How does it call Claude?** | the messages you send · stream vs batch · real-time vs overnight · which model tier · what it costs in tokens | **D2** Claude API Mechanics · **D5** Model Selection & Optimisation (16.8%) | ~12 |
| ③ | **What does Claude see and say?** | what lands in the context window · how the prompt is built · whether the output comes back in a shape your code can consume | **D6** Prompt & Context Engineering (11%) · **D2** Application Design · **D3** Claude Code (3.1%) | ~13 |
| ④ | **Will it survive production?** | requirements & life cycle · debugging when it breaks · security when someone feeds it a hostile input | **D2** Requirements / Systems Life Cycle / SW-Eng Foundations / Config Mgmt · **D4** Eval, Testing & Debugging (2.6%) · **D7** Security & Safety (8.1%) | ~15 |

**D2 (Applications & Integration) is 33.1% — the biggest domain — and its skills split across
decisions ②, ③ and ④.** That's why D2 spans Days 1, 2 and 4 of the bootcamp. And ~a quarter
of the exam (most of decision ④) is plain software engineering with no Claude in it — Day 4
owns that.

**Decision ④ is the biggest quarter, and a large slice of it is plain software engineering
with no Claude in it.** Candidates who spent the whole week in the API docs lose those
points. We do not: Day 4 is built for decision ④.

> On every practice question this week, the trainer says out loud: *"Which decision?"* — and
> the class answers before anyone looks at the options.

---

## 2. Two rules that kill wrong answers

Once you've named the decision, the options sort themselves with two rules taken straight
from the exam guide's own rationales.

### Rule 1 — the stem names a constraint; the answer is the *mechanism built for it*

A generic knob — `temperature`, model tier, `max_tokens`, "use a bigger model" — is almost
always a distractor. The keyed answer is the specific mechanism that exists **for that named
constraint**.

- *"10,000 documents overnight, cost is the concern, nobody needs it till morning"* → the
  **Batch** lane. Not "run it in parallel", not "cap the tokens", not "use a smaller model".
- *"progress must be visible immediately and long calls must not time out"* → **streaming**.
  Not "raise the client timeout", not "lower the output ceiling".

### Rule 2 — if the stem says *must / never / always / cannot*, only a *mechanism* survives

Every option that is **guidance** — "add a line to the system prompt", "write the rule
down", "ask users not to…", "tell the model to be careful" — is dead the moment the stem
demands a guarantee. *"A polite request is not an enforceable control."* Guidance is words
in the path of something that can ignore words.

What survives is something that **actually stops** the bad case:

- isolation (untrusted input never reaches the instruction channel),
- a **blocking hook** in front of a dangerous tool (code that runs before the tool and can
  refuse it),
- a **schema** the output is constrained to,
- **version control + a pipeline** instead of "a setup document".

> The rule runs in reverse too, and it's a favourite distractor: putting **your own
> instructions inside a `tool_result`** is broken, because that channel is the *untrusted*
> one — the model may ignore or flag them.

---

## 3. The four-step attack (use on every item)

1. **Name the decision** (①–④). Half the wrong options fall away — they belong to a
   different decision.
2. **Find the constraint word.** "overnight", "must never", "any engineer can roll back",
   "results in any order", "visible immediately". The stem usually states it more than once.
3. **Apply Rule 1 / Rule 2.** Kill the generic knobs (Rule 1). If there's a *must/never*, kill
   the guidance (Rule 2).
4. **Pick the mechanism** that matches the constraint. If two options both work, choose the
   one that is **cheaper / simpler / SDK-native** — the exam rewards that.

Multiple-response items tell you how many to select — select exactly that many.

---

## 4. Distractor species (name at least two before you answer)

The question skeleton is **situation → symptom → ask**. Five wrong-answer species prowl the
paper. On every practice item, **pick your answer, then name the species of ≥ 2 distractors
before the reveal** — the real paper won't label them for you, and this reflex *is* the
comfortable-pass feeling.

| Species | Tell | Examples |
|---|---|---|
| **Overbuild** ⚑ | solves the problem with more machinery than it deserves — "building more feels like competence" | tool misrouting → "add a routing model / fine-tune" (fix: **better tool descriptions**); repeated-context cost → "re-architect the pipeline" (fix: **turn on caching**); fixed 3-step flow → "an autonomous agent with 12 tools" (fix: **a routed workflow**); truncation → "a second pass that stitches outputs" (fix: **raise the token cap**) |
| **Symptom-treater** | patches the symptom, leaves the cause | "add *please respond correctly* to the prompt"; "make the summaries shorter" while the architecture wastes dollars; "a sterner system prompt saying ignore malicious instructions" |
| **Extremist** | an all-or-nothing move | "refuse to process external content"; "manually review every record"; "switch providers" |
| **True-but-irrelevant** | a correct statement that answers nothing asked | a real fact about agent frameworks / MCP independence, dropped where it decides nothing |
| **Stale API** | true of an older model/SDK | `budget_tokens`, `output_format`, assistant prefill, `temperature` on newest models, `claude-code-sdk` |
| **Right word, wrong place** | correct term used incorrectly | a message with `role:"system"`; a WebSocket for streaming (it's SSE); your rules inside a `tool_result` |
| **Wrong system** | an OpenAI-ism | `function_call`, `content_filter`, `/v1/chat/completions`, `tool_call` as a `stop_reason` |

> **The overbuild is the developer exam's specialty.** Engineers are the most vulnerable to
> it. On this paper the **elegant minimal fix wins, consistently** — because in production
> the elegant minimal fix is what a senior engineer actually ships.

**When two answers both look right:** hunt the planted tie-breaker — a **constraint**:
latency, budget, data sensitivity, or scale. It's always there.

---

## 5. Facts the exam leans on (memory anchors)

These recur across the sample questions and the video companion. Each is a one-line trap.

- **The API is stateless.** Multi-turn = you resend the prior turns every call.
- **Streaming is Server-Sent Events over the same HTTP call** — not a WebSocket. Errors can
  arrive *as an event mid-stream*, so read events, not just the status code.
- **No message can have `role: "system"`.** Instructions go in the top-level `system` field.
- **`temperature` was never a guarantee of identical output and is removed on the newest
  models.** Design for variation (assert on structure, not exact wording).
- **`budget_tokens` thinking is removed on newest models**; adaptive thinking replaces it.
- **`max_tokens` is a ceiling, not a target.** Truncation shows as `stop_reason: "max_tokens"`.
- **Every response carries `stop_reason` (is it whole?) and `usage` (what did it cost?)** —
  both free to read; check them every call.
- **An image is built-in tokens** (patches); a PDF is billed as text **and** page images.
  If you already have the text, send the text.
- **`rate_limit` error = your traffic spiked (yours to fix); `overloaded` = their load
  (not yours).**
- **"Implement" in the systems life cycle means *deploy where users are*, not *write the
  code*.** Production credit is earned in *operate* and *maintain*.
- **Requirements split into *functional* (what it does) and *infrastructure* (what it runs
  on / what the team must be able to do to it).**
- **Unsupported structured-output schema features are *rejected*, not silently ignored.**
- **A plugin runs code with your privileges** — installing one is a trust decision, like a
  dependency.
- **Three surfaces, three contracts:** the chat product layers Anthropic's own system prompt
  under yours (doesn't transfer to the API); a coding-tool rules file arrives as a *user
  message*; the API uses the top-level `system` field.
- **Untrusted / third-party content belongs only in `tool_result` blocks** — and your own
  instructions never do.

---

## 6. Exam-day routine (taught in the Day 5 wrap)

- **~135 sec/item** (53 items / 120 min, leave ~10 min to review flags). Over 2.5 min → flag
  and move.
- Read the **last sentence of the stem first** — "best", "select two", "will NOT".
- Step 1: **name the decision.** Step 2: **kill stale-API + generic-knob options.** Step 3:
  if *must/never* → **kill guidance.** Step 4: pick the mechanism; tie-break to
  cheaper/simpler.
- No blanks — there's no negative marking.
- Your score report is **% per domain** → your revision plan is "rewatch the weak quarter".

---

## 7. Where the method is used in the bootcamp

- **Day 1** deck introduces the Four Decisions + Two Rules (slides in Module 1).
- **Every `exam-style-questions.md`** header restates the four-step attack; the trainer models
  it on question 1 each day.
- **`question-bank/`** rationales are written to demonstrate Rule 1 / Rule 2 explicitly.
- **Day 5** `mock-exam/` review is run entirely through this method.
