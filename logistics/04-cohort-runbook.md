# Cohort runbook — running the week

Operational detail for delivery: daily shape, timings, room setup, group work, and the
"something broke" playbook. Pair with each day's `trainer-guide.md` for slide-level detail.

---

## Standard day shape (Days 1–4)

| Block | Time | What |
|---|---|---|
| Arrival / recap quiz | 09:00–09:20 | live recall from yesterday's `quiz.md` |
| Module A (lecture + demo) | 09:20–10:20 | ~2–3 slide modules |
| **Lab A** | 10:20–11:05 | hands-on, trainer + assistant circulate |
| Break | 11:05–11:20 | |
| Module B | 11:20–12:15 | |
| **Lab B** | 12:15–13:00 | |
| Lunch | 13:00–14:00 | |
| Module C | 14:00–14:50 | |
| **Lab C** | 14:50–15:35 | |
| Break | 15:35–15:50 | |
| Module D + **Lab D** | 15:50–16:45 | shorter; often "extend Lab C" |
| Exam-style questions | 16:45–17:15 | work `exam-style-questions.md` together, discuss distractors |
| Wrap + `quiz.md` | 17:15–17:30 | 10 Qs, self-marked, trainer collects domain scores |

**Day 5** replaces the afternoon with the capstone + the 90-minute mock exam + review — see
`day5-production-cert/README.md`.

Ratio target: **≥ 45% of contact time is hands-on.** If a day is drifting lecture-heavy, cut
per each guide's "if behind" list.

---

## Room setup

- **Projection:** mirror displays. Presenter zoomed so the back row reads 12px code.
- **Trainer machine:** deck in one browser window; a second window/tab with
  `console.anthropic.com` usage; VS Code; a terminal with `.venv` active in
  `aizentify-cdf-bootcamp/`.
- **Candidate machines:** VS Code + integrated terminal is enough. Discourage 3 windows.
- **Wall / shared doc:** the day's lab commands, the Team Project link, and a "parking lot"
  for questions you'll answer at the next break.
- **Seating:** tables of 3–4. Mixed ability per table on purpose (see group work).

---

## Group work

- **Pairs for labs.** One drives, one navigates, swap at the halfway checkpoint the trainer
  calls. Pairs stay for the day, re-shuffle daily.
- **Tables for exam-style questions.** Each table argues to consensus before the reveal;
  trainer then walks the distractors. This is where most exam learning happens — protect it.
- **Capstone (Day 5): tables of 3–4** build and present one agent.

---

## Per-candidate readiness scorecard (template)

Keep one row per candidate; update at each day's wrap and after exam-style questions.

```
name | D1q | D1x | D2q | D2x | D3q | D3x | D4q | D4x | D5x | MOCK | weak domains | ready?
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+------+--------------+-------
     |     |     |     |     |     |     |     |     |     |      |              |
```

`q` = end-of-day quiz %, `x` = exam-style-questions %, `MOCK` = Day 5 60-Q %.
**Ready** = MOCK ≥ 75% and no single domain < 70%. Otherwise list the 1–2 weak domains and
hand them the matching `question-bank/domain-N-*.md` + anchor episode.

---

## The "something broke" playbook

| Situation | First move | If that fails |
|---|---|---|
| A candidate's `check_env.py` went red overnight | re-activate venv; re-`pip install -r requirements.txt` | pair them with a working machine for the module; fix at lunch |
| `RateLimitError` for one person | check their key's usage in Console; top up or swap to a spare key | share the trainer's key for that one lab only, then rotate it |
| `RateLimitError` across the room | you're on a shared key by mistake, or the workspace cap hit | stop, hand out individual keys, raise the workspace limit |
| SDK/API behaviour differs from the `solution/` expected output | confirm `pip show anthropic claude-agent-sdk` versions vs `requirements.txt` | teach from the validated `solution/`; log the drift for the maintainer |
| Proxy / SSL errors mid-lab | set `HTTPS_PROXY`; point `SSL_CERT_FILE` at the corp CA | trainer hotspot for the lab; escalate to IT for the afternoon |
| A lab is taking everyone 2× the budgeted time | call the halfway checkpoint early; switch remaining pairs to "run + read the `solution/`" | move Lab D to "optional / homework"; keep the exam-question block intact |
| Whole module fell flat | don't re-teach the same way; jump to the lab and let the code make the point | assign the recap slides as reading; move on |
| Someone finished the lab in 10 minutes | point them at the lab README's **"Going further"** section, or make them the table's navigator | ask them to help a struggling pair (teaching = retention) |

---

## Daily comms to the coordinator

End of each day, one short message:

```
Day N — attendance X/Y. Green environments: X/Y.
On track: yes/no (if no: what slipped, plan to recover).
At-risk candidates (trending <60% in a domain): names + which domain.
Anything procurement needs to fix before tomorrow: ...
```

---

## Materials inventory (trainer brings / confirms)

- [ ] Laptop + charger + HDMI/USB-C adapters (both)
- [ ] Backup hotspot with data
- [ ] 1 spare provisioned laptop per 8 candidates
- [ ] Printed answer keys for all `quiz.md` + `exam-style-questions.md` (or on a second device)
- [ ] Printed or PDF copy of the current **official** exam guide
- [ ] Roster scorecard (spreadsheet)
- [ ] Whiteboard markers / sticky notes for the parking lot
