# Exam day — minute by minute

The real thing: **53 items · 120 minutes · scaled pass 720 / 1000 · Pearson VUE (online or
test centre) · identity verified before the clock starts.** Our mock runs it at 90 minutes
to build margin.

---

## The day before

- **Pearson VUE system check on the actual machine you'll use.** Do it early enough to fix
  problems. If your home setup is fragile, book a test centre — it becomes someone else's
  problem.
- **Re-sit this mock.** Your recent commits (the support assistant) are the best flashcards
  that exist.
- Re-read the **official exam guide as a checklist**: for each of the 25 sub-skills, ask
  *"can I do this in code?"* Weakest two get the final hour.
- Download the **current** exam guide from the Partner Academy — version, fee, time limit,
  pass mark and retake rules move; the guide is the source of truth.
- Sleep. Set out ID.

## In the room — setup

- Quiet room, clear desk, one screen, no notes, no second monitor. Workspace photos on
  request. ID ready.
- Water within reach; you won't get up.

## In the room — the clock

**120 min / 53 items = ~2 min 15 s each**, with review time. The clock is your ally — don't
rush.

### On every item — the four-step attack

1. **Read the last sentence of the stem twice.** It carries the ask: *best* · *choose two* ·
   *will NOT*. Developer scenarios bury it under context.
2. **Name the decision** — ① what runs · ② how it calls Claude · ③ what Claude sees & says ·
   ④ will it survive production. Options that belong to a different decision fall away.
3. **Find the constraint word** — "overnight", "must never", "any engineer can roll back",
   "visible immediately", "1,000,000/day".
4. **Kill by species**, in this order:
   - **stale-API** (`budget_tokens`, `output_format`, prefill on new models, `claude-code-sdk`)
   - **wrong-system** (`function_call`, `content_filter`, `role:"system"` message, WebSocket streaming)
   - **generic knob** (temperature, model tier, `max_tokens`, "raise the timeout") — unless the stem's constraint *is* that dial
   - if the stem says **must / never / always / cannot** → every **guidance** option is dead ("tell the model to…", "write it down", "ask users to…")
   - **overbuild** — "add a routing model", "re-architect the pipeline", "a second agent to supervise" — when a smaller fix exists. *The elegant minimal fix wins.*
   - **symptom-treater** — patches the symptom, leaves the cause
   - **true-but-irrelevant** — a correct statement that answers nothing asked
5. **Two answers survive?** Hunt the planted **constraint** — latency, budget, data
   sensitivity, scale. It's there.
6. **Tie-break:** the cheaper / simpler / SDK-native option is almost always the keyed one.

### Multiple-response
The item tells you how many. Select **exactly** that many.

### Pacing
- Over **2.5 min** on an item → pick your best guess, **flag it, move on**. A complete first
  pass beats a perfect half.
- Second pass: your flags only.
- **No blanks** — there's no negative marking.

## After

- **Pass:** the badge lands with a 12-month clock and a free on-time renewal — **put the
  renewal in your calendar now**.
- **Miss:** the report shows **% correct per domain** — a map. Retake ladder is **14 → 30 →
  90 days**, **4 attempts per rolling year**. Book the next attempt while the report is
  fresh; feed the weak domains into the 4-week plan.

## The five ways people fail (so you don't)

1. Study by affection, not weight (Claude Code is 3.1%; Config Mgmt is more than Claude Code
   + Debugging combined).
2. Over-study prompting (11%).
3. Agent-everything brain — the overbuild eats you.
4. Prepare without an API key.
5. Dumps (a rules violation stapled to wrong answers; the scenarios punish memorisation
   anyway).
