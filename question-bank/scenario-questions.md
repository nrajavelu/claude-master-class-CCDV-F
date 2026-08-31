# Scenario questions — cross-domain "what do you do next?"

> **Status: blueprint.** Item target **15**. Built pass 3. These are longer, applied items
> that span decisions — the kind that most rewards the four-step attack from
> `../logistics/05-exam-method.md`.

## Format

Each item: a paragraph of situation + a demand or a symptom, then 4 options. The answer walk
always shows: **(1) which decision** ①–④ · **(2) the constraint word** · **(3) which rule
kills which options** · **(4) the surviving mechanism**.

## Coverage targets

| # | Scenario seed | Decision | Rule in play |
|---|---|---|---|
| 1 | Overnight bulk job, cost matters, not urgent | ② | R1 → Batch |
| 2 | "Ticket text must never trigger the refund tool" | ④ | R2 → isolation + blocking hook |
| 3 | Long output, must show progress, must not time out | ② | R1 → streaming |
| 4 | "Any engineer must be able to deploy and roll back" | ④ | R2 → version control + pipeline |
| 5 | Prototype works in chat product, breaks via API | ③ | R1 → surface difference (chat adds its own system prompt) |
| 6 | Dashboard needs category + urgency every time | ③ | R1 → structured output schema |
| 7 | 3 engineers, 1 repo, different behaviour each run | ③/④ | R2 → committed config + pinned version |
| 8 | Regression test must pass reliably on a summariser | ④ | R1 → assert structure, not wording |
| 9 | Repeated 40 KB system prompt, cost too high | ② | R1 → prompt caching (order: caching first) |
| 10 | Streaming call "succeeded" but text is half-done | ④ | read events, `message_delta` stop_reason |
| 11 | Tool called at the wrong time | ① | R1 → fix the description, not the model |
| 12 | Fan-out research task filling one context with reading | ① | R1 → sub-agents / cheaper worker model |
| 13 | Secret key committed to the repo | ④ | R2 → secret store + rotate + least-privilege |
| 14 | "Implement" the finished prototype | ④ | vocabulary: implement = deploy where users are |
| 15 | Business brief → sort the requirements | ④ | functional vs infrastructure |

## Seed item (full)

### 1. A nightly job reprocesses ~10,000 support transcripts to tag sentiment. Finance flags
the API bill. The job has an 8-hour window and no user waits on it. What should the developer
change **first**?

A. Run the transcripts through in parallel with async to finish faster.
B. Move the job to the Batch API.
C. Switch the model to Haiku.
D. Cap `max_tokens` at 50.

> **Decision:** ② how does it call Claude. **Constraint words:** "nightly", "8-hour window",
> "no user waits". **Rule 1:** the stem names the exact constraint Batch exists for → B.
> A/C/D are generic knobs (A doesn't cut cost; C is a quality trade the stem didn't ask for;
> D would truncate). **Answer: B.**
