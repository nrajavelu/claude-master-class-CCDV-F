# Lab 2 · The description IS the interface

**Domain:** D8 (Tool Implementation) · **Time:** 35 min
**Practise:** the tool `description` is the single biggest factor in whether the model uses a
tool correctly — prove it by A/B-testing a vague vs a detailed description on the same
prompts.

> Runnable reference: `code-snippets/strict_tool.py`, `ep03/tools.py`.

---

## Goal

Define **one** tool, `lookup_order`, **twice** — once with a vague description, once with a
detailed one (what it does · **when to use it** · **when NOT to** · what each arg means). Run
the same 5 user turns through each build. The vague build skips or mis-calls; the detailed
build calls it correctly every time.

```
cd aizentify-cdf-bootcamp
python day2-prompt-tools-output/labs/lab2_tool_description/starter/lab.py
```

Needs `ANTHROPIC_API_KEY` in `.env`. Model pinned to `claude-haiku-4-5`.

---

## Steps

1. `starter/lab.py` has the 5 prompts, a `run(description)` helper that makes one
   `messages.create` call with a single tool, and two `# TODO` strings.
2. Fill `DESC_VAGUE` — e.g. `"Look up an order."`
3. Fill `DESC_DETAILED` — say it returns status + line items + totals for a **known numeric
   order id**; use it whenever the user names or clearly implies a specific order; do **not**
   use it for general policy questions or when no order id is available; `order_id` is the
   integer from the confirmation email.
4. Run. The script prints, per prompt, whether each build emitted a `tool_use` for
   `lookup_order` and with what `order_id`.
5. Write one sentence: *why* did the detailed description change the outcome?

---

## The 5 prompts

| # | Prompt | Correct behaviour |
|---|---|---|
| 1 | "Where's my order 10231?" | call, `order_id=10231` |
| 2 | "I ordered a lamp last week and it hasn't come — order 55012." | call, `order_id=55012` |
| 3 | "What's your return window?" | **no call** (policy question) |
| 4 | "Can you check on my recent purchase?" | **no call** (no id — ask the user) |
| 5 | "Order number 9— status please." | call, `order_id=9` |

## Expected output (shape)

```
                              VAGUE            DETAILED
1  order 10231            call(10231) ✓     call(10231) ✓
2  order 55012            call(55012) ✓     call(55012) ✓
3  return window          call(?)      ✗     no call     ✓
4  recent purchase        call(0)      ✗     no call     ✓
5  order 9                no call      ✗     call(9)      ✓
DETAILED: 5/5   VAGUE: 2/5
```
(Exact vague-column results vary run to run — that variance is itself the lesson.)

## Checkpoints

- [ ] The detailed build is correct on all 5; the vague build misses ≥ 2.
- [ ] `DESC_DETAILED` contains an explicit **when NOT to use it** clause.
- [ ] They can state: fixing the description is the **minimal** fix — a routing model or a
      fine-tune here is the **overbuild** distractor.

## Common mistakes

| Symptom | Cause |
|---|---|
| both builds identical | `DESC_VAGUE` and `DESC_DETAILED` are too similar — make the vague one genuinely terse |
| detailed build still calls on prompt 3/4 | add the exclusion clause and describe `order_id` as required-and-known |

## Going further

- Add a second tool `search_policy` with an overlapping "look things up" description and
  watch the model misroute; fix it with **one exclusion sentence per tool**, or by merging
  both behind a `type` parameter.
