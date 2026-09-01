# Lab 1 · Prompt surgery — three passes against a rubric

**Domain:** D6 (Prompt Engineering) · **Time:** 30 min
**Practise:** improving a weak `system` prompt in **deliberate passes** — role/audience →
output shape → one few-shot — and *measuring* each pass instead of eyeballing it.

> Reference: Day 1 `exercises.md` B · `code-snippets/prompt_structure.py`.

---

## Goal

`prompts/weak_system.txt` is a vague summariser prompt ("be thorough and make sure the
summary is good"). `sample_input.txt` is a rambling bug report. Improve the **system**
string in three passes, re-running against the same input each time and scoring with
`rubric.py` (5 structural checks). The score should climb, e.g. **2/5 → 5/5**.

```
cd aizentify-cdf-bootcamp
python day2-prompt-tools-output/labs/lab1_prompt_surgery/starter/lab.py
```

Needs `ANTHROPIC_API_KEY` in `.env`. Model pinned to `claude-haiku-4-5`.

---

## The three passes (what to change, in order)

| Pass | Add | Why |
|---|---|---|
| 1 | **role + audience + purpose** — "for the engineer who will fix this; they need the root cause, not a recap" | removes "make it good" ambiguity |
| 2 | **output shape** — "≤ 4 bullets; first bullet is the root cause; no invented specifics" | wrong shape is the #1 summariser failure |
| 3 | **one few-shot** — a tiny input→summary example in the exact target format | locks the format when instructions alone don't |

Don't skip ahead — the point is to see which pass moves the score.

---

## Steps

1. `starter/lab.py` loads `prompts/weak_system.txt`, sends `sample_input.txt` as the user
   turn, prints the summary and its rubric score.
2. Copy the weak prompt into `PASSES[0]`, then write `PASSES[1]` and `PASSES[2]` applying
   the table above (starter has `# TODO`s).
3. Run. The script scores all three and saves them to `out_pass{1,2,3}.txt` to diff.
4. `solution/lab.py` has a worked set of three prompts.

## Expected output (shape)

```
pass 1  score: 2/5   missed: <= 4 bullets · names the root cause · ends actionable
pass 2  score: 4/5   missed: mentions CI vs local timing
pass 3  score: 5/5
```
(Exact numbers vary; the trend is the lesson.)

## Checkpoints

- [ ] Score is non-decreasing across the three passes and reaches 4–5/5.
- [ ] Pass 2's prompt contains an explicit output-shape constraint.
- [ ] Pass 3 adds exactly **one** example, in the target format.
- [ ] They can name which pass helped most for *this* input and say why (diagnosis over
      elaboration — match the fix to the failure).

## Common mistakes

| Symptom | Cause |
|---|---|
| score flat across passes | each pass is rewording, not adding a *structural* technique |
| pass 3 lowers the score | the few-shot example's format doesn't match what you asked for in pass 2 |
| rubric "invented specifics" always fails | the model added a tool/port/number not in the input — tighten "only what's in the text" |
