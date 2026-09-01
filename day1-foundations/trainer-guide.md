# Day 1 — Trainer guide (slide-by-slide)

**Deck:** `slides/day1.html` (30 slides) · **Labs:** 4 · **Contact time:** ~7h + breaks
**Anchor episode:** `ep01/agent.py` (parent `claude-api-masterclass` repo) — you'll open it live in Module 5.

---

## Project this — worked examples

Open the **worked-example page** for a snippet mid-explanation — it has the scenario, the code, and the *captured output* with a predict-then-reveal toggle: `portal/examples.html?f=<name>`. Hide the output, ask the room to predict it, then reveal.

This day's demos: `messages_basics` (blocks · stop_reason · usage) · `count_tokens` (cost per task) · `retry_chain` (bad key → AuthenticationError, not retried) · `agent_loop_react` (Thought→Action→Observation) · `streaming`.

Offline / no budget: `python tools/capture_runs.py <name>` (mock) shows real program flow; `--live` for real numbers.

---

## Before this session

- [ ] Every candidate's `check_env.py` was green at T‑3 days. Re-confirm at the door.
- [ ] You have run all four `solution/` scripts on a clean machine this week and the
      "Expected output" blocks in each lab README still match.
- [ ] Pre-open: this deck (browser, fullscreen `F`), a terminal in `day1-foundations/` with
      `.venv` active, VS Code on `day1-foundations/labs/`, a browser tab on
      `console.anthropic.com` usage, and `ep01/agent.py` in a tab for Module 5.
- [ ] Board / shared doc has: the four lab commands, the Team Project link, a parking lot.

## Materials

Candidate laptops (venv + `.env` ready), this deck on the projector, printed answer keys for
`quiz.md` and `exam-style-questions.md`.

## Timing plan

Deck is **~36 slides**. It now carries the visual layer (see `THEME.md §4`): a **slide-type
chip** top-left of every slide (`Concept` / `Try it` / `Do this now` / `Exam watch` /
`Recap`) with a **legend slide** early in Module 0; **inline-SVG diagrams** for the four
decisions, the two rules, request/response anatomy, "the API has amnesia", the retry tree,
and the agent-loop ring; **focus-code** blocks (one line spotlit); and **▶ watch** corner
chips linking the in-page player. There's also a **one-page recap** (`recap.html`) to hand
out at the end. Slide numbers below are approximate — **navigate by the slide title** in
each heading.

| Block | Slides (approx) | Time |
|---|---|---|
| Welcome + agenda | 1–2 | 09:00–09:10 |
| **Module 0 — the exam method** | 3–6 | 09:10–09:35 |
| Module 1 (Claude & the Messages API) | 7–12 | 09:35–10:20 |
| **Lab 1** | 13 | 10:20–10:55 |
| M1 recap + Module 2 | 14–19 | 10:55–11:35 *(break 11:35–11:50)* |
| Exercise: prompt surgery | 20 | 11:50–12:10 |
| M2 recap + Module 3 | 21–23 | 12:10–12:30 |
| **Lab 2** | 24 | 12:30–13:00 *(lunch 13:00–14:00)* |
| Module 4 | 25–27 | 14:00–14:40 |
| **Lab 3** | 28 | 14:40–15:25 *(break 15:25–15:40)* |
| Module 5 | 29–31 | 15:40–16:15 |
| **Lab 4** | 32 | 16:15–17:05 |
| Recap + exam-style Qs + quiz | 33–34 | 17:05–17:30 |

## If you're behind (cut from the bottom)

1. Exercise "prompt surgery" pass 3 (few-shot) — assign as homework.
2. Module 4 error-table slide — talk it, don't dwell; the lab teaches it.
3. Lab 4 "Going further" — skip.
4. **Never cut: any lab body · Module 0 · the exam-style-question block.** Module 0 is the
   spine of the whole week — protect its 25 minutes.

## Known failure modes today

| Failure | Fix in the moment |
|---|---|
| `ModuleNotFoundError: anthropic` | venv not active — `source .venv/bin/activate` |
| `FileNotFoundError` in a lab | they're not in `day1-foundations/` — `cd` there |
| One candidate 429s repeatedly | check their key in Console; swap a spare; don't let it stall the room |
| Lab 4 infinite loop | they forgot to `return` on `end_turn`, or dropped the turn cap — point at rule 1 |
| "Claude won't call my tool" (Lab 4) | `tools=TOOLS` missing from the call, or description too vague |

---

## Slide-by-slide

> Format per row: **teaching points** · *say-this* · `live demo` · **Q&A** · → transition.
> **Read `../logistics/05-exam-method.md` before delivering Module 0** — you must be able to
> run the four-step attack cold.

### Module 0 · How this exam is built  ·  ~25 min (4 slides)

**Divider — "How this exam is built"**  ·  30 sec
- *Say:* "Before any Python: 20 minutes on how this exam thinks. This is the highest-leverage
  part of the whole week. It turns 'do I remember this flag?' into 'which decision is this,
  and which option is a mechanism?'"

**Every question is one of four decisions**  ·  9 min
- Walk the table. ① what runs ② how it calls Claude ③ what Claude sees/says ④ will it survive
  production. Give a one-line real example of each (agent wiring / batch vs stream / prompt
  shape / "roll it back").
- Hammer: **D2 is 33%** and **~a quarter of the exam is plain software engineering** — Day 4
  is built for that; don't let anyone treat it as filler.
- *Say:* "On every practice question this week I'll ask 'which decision?' and you answer
  before anyone reads the options."
- **Q:** "Do I still need the facts?" → "Yes, but fewer than you think. The method kills 2 of
  4 options for free; the facts pick between the last 2."

**Two rules that kill wrong answers**  ·  9 min
- Rule 1: stem names a constraint → answer is the mechanism *for that constraint*; generic
  knobs (temperature, tier, `max_tokens`, timeout) are distractors. Example: "10,000 docs
  overnight, cost matters, nobody needs it till morning" → **Batch**.
- Rule 2: stem says *must / never / always / cannot* → guidance options die; only a mechanism
  survives. Quote it verbatim: **"A polite request is not an enforceable control."** Example:
  "ticket text must never trigger the refund tool" → isolation + a **blocking hook**, not
  "add a line to the system prompt".
- *Say:* "Guidance is words in the path of something that can ignore words."

**The four-step attack**  ·  6 min
- Name the decision → find the constraint word → apply Rule 1/2 → pick the mechanism
  (tie-break to cheaper/simpler/SDK-native).
- `live demo` — put up **question 1** of `exam-style-questions.md` (or the guide's
  refund-tool sample from `logistics/05 §1`) and run the four steps out loud. Let the class
  call each step.
- → "Now the facts those mechanisms are made of — Module 1."

---

> The rows below are the **content modules 1–5**. They come *after* Module 0 in the deck, so
> the physical slide numbers are +4 from what a row says — navigate by the **slide title** in
> each heading, not the number.

### Title  ·  2 min
- Set the frame: "You learn the exam's method, then the raw layer. By lunch you call the API
  directly; by 5pm you've built an agent loop by hand — the loop the SDK hides all week."
- *Say:* "Method first, then engine, then — Wednesday — the car."
- → agenda.

### Today in six moves  ·  3 min
- Walk the table. Stress: **≥ 4 labs, all on their own key** — they will watch real spend.
- *Say:* "Open your Console usage page in a tab. We'll glance at it after each lab."
- **Q:** "Do we pay?" → "Your org pre-loaded credit. Today costs cents. Watch it yourself."
- → Module 1 divider.

### 3 · Module 1 divider  ·  30 sec

### 4 · The model family  ·  5 min
- Haiku/Sonnet/Opus by *shape of task*, then the correction: **start capable, measure down**
  is the current guidance and the exam's keyed answer. "Pick a tier by task type" is a
  distractor.
- *Say:* "We pin Haiku in labs purely for cost — a room of keys. That's a classroom
  decision, not the design principle. Day 5 does this properly."
- **Q:** "Which model for production?" → "The most capable that meets latency/cost, proven by
  an eval. Day 4 and 5."
- → slide 5.

### 5 · One endpoint  ·  5 min
- The big idea: **one call**. Tools, vision, PDFs, structured output, thinking — all
  parameters of `messages.create`. There is no separate "tools API".
- **Stateless**: you resend the whole history every turn. There's no server session. (This
  pays off in Lab 4 and again on Day 4.)
- `live demo` — in the terminal: `python ../day0-prework/labs/hello_claude.py`. Point at the
  `usage:` line.
- → slide 6.

### 6 · Anatomy of a request  ·  6 min
- Go field by field. Emphasise:
  - `max_tokens` is a **hard cap on the response** — hit it and you get truncation +
    `stop_reason: max_tokens`.
  - `system` is **its own top-level field**, not a message with `role: system` (that's a
    different, model-gated feature they'll meet later).
  - `messages` **must start with `user`**; roles are `user` / `assistant`.
- **Q:** "String or list for content?" → "Either. String for plain text; list of typed
  blocks when you mix text + images + tool results."
- → slide 7.

### 7 · Anatomy of a response  ·  6 min
- The one that trips beginners: **`response.content` is a list**. Never assume `content[0]`
  is text — filter on `block.type`.
- You **send dicts, receive objects** (dot access). `response.model_dump()` to get a dict
  back.
- `usage` = the bill. Name `input_tokens`, `output_tokens`, and mention cache counters exist.
- `live demo` (optional, ipython): show `resp.content`, `resp.stop_reason`, `resp.usage`.
- → slide 8.

### 8 · stop_reason (Exam watch)  ·  6 min
- Read the table aloud. The exam **will** test these. The two they forget: `pause_turn`
  (server tools) and `refusal` (not an exception — a `stop_reason`; `stop_details` carries
  the category).
- *Say:* "Every robust loop is a `match` on `stop_reason`. You'll write one in Lab 4."
- **Q:** "Is `refusal` an error I catch?" → "No — HTTP 200, `stop_reason: 'refusal'`. Check
  it *before* reading `content`."
- → Lab 1.

### 9 · Lab 1 cue  ·  1 min then 35 min lab
- Read the three bullets. Send them to `README.md`.
- **Facilitation** below. Call a halfway checkpoint at +18 min.

### 10 · Module 1 recap  ·  2 min
- Three lines. Ask the room to give you line 3 (branch on `stop_reason`).
- → Module 2 divider.

### 11 · Module 2 divider  ·  30 sec

### 12 · System prompt is the steering wheel  ·  5 min
- The contract/task split: **contract → `system`, task + data → `messages`**.
- Heuristic: "if you'd paste it every turn, it's a system prompt."
- Callback to Lab 1: whoever put the instruction in the user message — this is why it
  belongs in `system`.
- → slide 13.

### 13 · Explicit / structure / few-shot  ·  6 min
- Three cards. For each, a one-liner and a micro-example:
  - Explicit: "3 bullets, ≤ 15 words each, no preamble" beats "be concise".
  - Structure: wrap the file in `<code>…</code>` so instruction ≠ data — also the first line
    of defence against prompt injection (Day 2).
  - Few-shot: one `input → output` pair fixes format-following faster than prose.
- → slide 14.

### 14 · Output steering  ·  4 min
- System-prompt shape instructions + a skeleton to fill.
- Flag: **prefill is removed** on current models — a stale-answer distractor on the exam.
- For *guaranteed* JSON → Day 2 (`strict` tools / `output_config.format`). Today is
  best-effort steering.
- → slide 15.

### 15 · Thinking & effort (Exam watch)  ·  5 min
- `thinking={"type": "adaptive"}` on current models. **`budget_tokens` is deprecated /
  rejected** — high-value distractor.
- `output_config={"effort": ...}` — thoroughness vs cost dial.
- When: ambiguous/multi-step → thinking; classify/extract → skip.
- → Exercise.

### 16 · Exercise: prompt surgery  ·  1 min then 15–20 min
- `exercises.md` → "Prompt surgery". Three passes, same input each time, keep the outputs.
- Circulate. The learning is seeing output quality jump between passes.
- Debrief: 2 volunteers read their pass-1 vs pass-3 system prompts.

### 17 · Module 2 recap  ·  2 min
- → Module 3 divider. *(break before or after per timing)*

### 18 · Module 3 divider  ·  30 sec

### 19 · Why stream + the pattern  ·  7 min
- The mechanism: non-stream holds the connection → big outputs risk the request timeout.
  Stream = tokens as generated.
- The pattern: `with client.messages.stream(...) as stream:` → iterate `stream.text_stream`
  → `stream.get_final_message()` for the complete Message. **Don't hand-assemble from
  events.**
- *Say:* "Default to streaming for anything long or high `max_tokens`. It's not just UX —
  it's how you avoid timeouts."
- → Lab 2.

### 20 · Lab 2 cue  ·  1 min then 25 min
- Bullets → `README.md`. Checkpoint at +12 min.
- Debrief question for the room: **"when would you NOT stream?"** (very short outputs; when
  you need the whole result before acting and latency is irrelevant).

### 21 · Module 4 divider  ·  30 sec

### 22 · Catch a chain (Exam watch)  ·  7 min
- The table. The rule: **most-specific first**, and **retry only 429 / ≥500 / connection**.
- Anti-pattern to name explicitly: `except Exception` (or one broad `except APIStatusError`)
  — loses the retry/don't-retry distinction. The exam tests this.
- → slide 23.

### 23 · The SDK already does some of this  ·  6 min
- Built-in retries (`max_retries=2`, exp backoff, 408/409/429/5xx + conn). Built-in 10-min
  timeout, overridable.
- Hand-roll only for custom logic (`retry-after`, wall-clock budget, logging).
- **`refusal` is a `stop_reason`, not an exception.** Say it twice.
- → Lab 3.

### 24 · Lab 3 cue  ·  1 min then 40 min
- Four bullets → `README.md`. The `--break-key` run is the payoff — make sure everyone runs
  both. Checkpoint at +20 min.
- Watch for: broad `except` swallowing `AuthenticationError` (bad key then retries slowly).

### 25 · Module 5 divider  ·  30 sec

### 26 · Count before you spend  ·  6 min
- `count_tokens(model, system, messages, tools)` — separate cheap endpoint. Predict spend;
  check fit.
- Cost math: per-million ÷ 1e6. Output pricier than input. Mention `cache_read_input_tokens`
  ≈ 0.1× (forward ref to Day 5).
- → slide 27.

### 27 · The agentic loop — two rules (Exam watch)  ·  8 min
- Put the two rules on the board and leave them there for the lab:
  1. append `{"role":"assistant","content": response.content}` — the **whole list**.
  2. on `tool_use`: **one** user message, list of `tool_result` blocks, **matching
     `tool_use_id`**.
- Draw the turn sequence: `user → assistant(tool_use) → user(tool_result) → assistant(text)`.
- `live demo` — **open `ep01/agent.py`** and walk the `while True` loop against these two
  rules. "This is the whole idea. Wednesday the SDK does it for you."
- **Q:** "Why append the assistant turn if I'm just going to send tool results?" → "The API
  is stateless. It only knows what's in `messages`. Skip it and roles don't alternate → 400."
- → Lab 4.

### 28 · Lab 4 cue  ·  1 min then 45 min
- Four bullets → `README.md`. This is the day's capstone. Checkpoint at +22 min.
- Insist they **read `ep01/agent.py`, not copy it.**

### 29 · Day 1 recap  ·  3 min
- Four "you can now" bullets. Tee up Day 2 (schemas, guaranteed structured output,
  guardrails).

### 30 · Exam prep  ·  25 min
- Tables work `exam-style-questions.md` to consensus; you walk every distractor (this is
  where exam skill is built — protect the time).
- Then `quiz.md`, self-marked, 10 min. Collect per-domain scores onto the roster scorecard.
- Point weak-on-Fundamentals candidates at `ep01/agent.py` + `question-bank/domain-1-fundamentals.md`.

---

## Lab facilitation

### Lab 1 · code explainer
- **Launch:** "cd into `day1-foundations`, open `labs/lab1_explainer/starter/explainer.py`,
  fill every TODO. README has steps + expected output."
- **Circulate for:** instruction in a user message instead of `system=`; `content[0].text`
  instead of filtering the list; `max_tokens` so small the explanation truncates.
- **Green light:** prints an explanation + a `--- call stats ---` block with real token
  numbers.
- **Fast finishers:** README "Going further" — `--style` flag, or print an estimated cost.

### Lab 2 · streaming
- **Launch:** "Same tool, now streamed. `with client.messages.stream(...) as stream:`."
- **Circulate for:** missing `flush=True`; trying to read `usage` mid-stream; forgetting the
  `with`.
- **Green light:** text visibly types out, then a stats block from `get_final_message()`.

### Lab 3 · resilient call
- **Launch:** "Make the call production-shaped. Run it normally, then with `--break-key`."
- **Circulate for:** broad `except` catching auth errors; instant retries (no sleep / fixed
  delay); cost math off by 1e6; `count_tokens` called after the main call.
- **Green light:** normal run prints estimate + actual cost; `--break-key` prints
  `FATAL: authentication failed (401) … Not retrying.` with no retry spin.

### Lab 4 · agent loop by hand
- **Launch:** "Open `ep01/agent.py` beside you. Build this; don't paste. Two rules on the
  board."
- **Circulate for:** assistant turn not appended (→ 400 role errors); `tool_result` with
  wrong/missing `tool_use_id`; multiple user messages instead of one; no turn cap; not
  returning on `end_turn`.
- **Green light:** prints `[tool] read_project_file(...)` lines, then an answer citing
  `discount.py` and a line number, then `(N turns, stop_reason=end_turn)`.
- **Fast finishers:** add `list_project_files`, or print `usage` each turn to watch input
  tokens grow.
