# Day 1 — In-class exercises

Short drills between the labs. Do them in the `day1-foundations/` folder with your venv
active. They cost fractions of a cent.

---

## Exercise A · Read the response object  (10 min, Module 1)

In an `ipython` / `python` REPL:

```python
from dotenv import load_dotenv; load_dotenv()
import anthropic
c = anthropic.Anthropic()
r = c.messages.create(
    model="claude-haiku-4-5", max_tokens=80,
    messages=[{"role": "user", "content": "Name three primary colors."}],
)
```

Answer without googling:

1. What type is `r.content`? What type is `r.content[0]`?
2. Print just the text, using a filter on `block.type`.
3. What is `r.stop_reason`? What would it be if you set `max_tokens=5`? **Try it.**
4. What are `r.usage.input_tokens` and `r.usage.output_tokens`?
5. Turn `r` into a plain dict. (Hint: `r.model_dump()`.)

> Debrief: the exam leans on knowing `content` is a *list of typed blocks* and that
> `stop_reason` drives your control flow.

---

## Exercise B · Prompt surgery  (15–20 min, Module 2)

**Starting prompt (bad):**

```
system = "Summarize this."
user   = <paste the text of ../ep01/agent.py>
```

Run it once. The output is probably a shapeless wall of text.

Now improve **only the `system` string**, in three passes. Re-run against the *same* file
each time and keep every output to compare.

| Pass | Change | Example |
|---|---|---|
| 1 | Make the **role and audience** explicit | "You are a senior Python reviewer briefing a teammate who will maintain this file." |
| 2 | Pin the **output shape** — length, format, exclusions | "Reply with exactly 3 bullets, ≤ 20 words each. No code. No preamble. Note anything unfinished or unsafe." |
| 3 | Add **one few-shot example** of the format you want | show a 3-bullet review of a *different*, tiny function, then "Now do the same for the file below." |

Debrief questions:

- Which pass gave the biggest jump in usefulness?
- Did pass 3 change the *content* or just the *format*?
- Where would each of these live if this were a real product — `system`, or per-request?

---

## Exercise C · Break it on purpose  (5 min, Module 4)

Predict, then run:

1. `model="claude-haiku-4-5-typo"` — which exception? Retryable?
2. `api_key="sk-ant-nope"` on the client — which exception? Retryable?
3. `max_tokens=1` with a question that needs a paragraph — what `stop_reason`?
4. `messages=[{"role": "assistant", "content": "hi"}]` (starts with assistant) — what happens?

> The point: match the *symptom* to the *typed exception* / `stop_reason`, and know which
> ones there's any point retrying.

---

## Exercise D · Cost estimate  (5 min, Module 5)

Using `count_tokens` only (no `messages.create`):

1. How many input tokens is `../ep01/agent.py` as a user message with a 2-line system prompt?
2. At Haiku input pricing ($1.00 / 1M), what does that input cost?
3. If the answer is ~300 output tokens at $5.00 / 1M, what's the total per call?
4. You call this 10,000 times a day. Daily cost? Now what's the single biggest lever to cut
   it? (Hold that thought for Day 5 — prompt caching.)
