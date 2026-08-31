# Trainer preparation checklist

> One trainer per 6–12 candidates; add a floating assistant at 12+.
> This checklist assumes you have delivered technical training before but are **new to this
> deck set**. Budget ~1.5 days of prep the first time you run it, ~3 hours every time after.

---

## T‑2 weeks

- [ ] Read, in order: `README.md`, `logistics/01`, `logistics/00`, `logistics/03`, then
      `day1-foundations/trainer-guide.md` end to end.
- [ ] **Reconcile the exam blueprint** (`logistics/03 §2`) against Anthropic's *current*
      official Claude Certified Developer – Foundation exam guide. Note any domain/weighting
      drift and adjust which `question-bank/` files you emphasise.
- [ ] Confirm with the coordinator that `01-procurement-guide.md` is in motion — especially
      the **firewall ticket** and the **Team plan** purchase (both have lead time).
- [ ] Send candidates `day0-prework/` and the date they must be green by (T‑3 days).
- [ ] Skim `ep01`–`ep12` in the parent repo so you can speak to the running case study. You
      do **not** teach from them directly, but Days 3–5 open episode files on screen.

## T‑1 week

- [ ] Provision **your own cohort API key** in the class workspace. You will burn more than
      a candidate (demos + dry-runs) — ask for `$100` on your key.
- [ ] Fresh-machine dry run (or a clean VM / new OS user):
  - [ ] Follow `00-environment-setup.md` exactly as written. Fix the doc if any step is
        stale — you are the last line of QA on it.
  - [ ] `python day0-prework/check_env.py` → all green.
  - [ ] **Run every Day 1 lab's `solution/`** and confirm output matches its `README.md`
        "Expected output" block. If anything drifts (model behaviour, SDK version), update
        the expected-output block and the trainer guide.
  - [ ] Open `day1-foundations/slides/day1.html`, present it start to finish, time each
        module against `trainer-guide.md`. Note where you personally run long.
- [ ] Install Claude Code, `claude` sign-in with your Team account, confirm an SDK "hello"
      works (needed live from Day 3).
- [ ] Decide the **RAG embedding path** (A: Voyage / B: local) with the coordinator and make
      sure `requirements.txt` reflects it. Do the Day 4 spec dry-run for whichever you pick.
- [ ] Build the **cohort roster spreadsheet** from the scorecard template in
      `04-cohort-runbook.md`.
- [ ] Prepare a **Claude Team Project** for the class: paste in the exam blueprint, a "house
      style" `CLAUDE.md`, and links; add all candidate seats as members.

## T‑3 days

- [ ] Collect `check_env.py` screenshots from every candidate. Chase red ones **now** — a
      broken environment on Day 1 morning costs the whole room 45 minutes.
- [ ] Re-run the full Day 1 dry run once more; it's muscle memory by exam week.
- [ ] Print or load the `quiz.md` / `exam-style-questions.md` answer keys somewhere you can
      glance at them without projecting them.
- [ ] Pre-open on your machine: the slide deck, a terminal in `aizentify-cdf-bootcamp/` with
      venv active, VS Code on the `day1-foundations/labs/` folder, and a browser tab on
      `console.anthropic.com` (to show usage climbing live — a good teaching moment).

## Morning of Day 1 (15 min, before Module 1)

- [ ] Room: projector mirrors, not extends. Font size in terminal ≥ 18pt, in VS Code ≥ 16pt.
- [ ] Your own smoke test: `python day0-prework/labs/hello_claude.py` in front of the class
      as the icebreaker — "if mine works, yours should; let's check."
- [ ] Ask for a show of hands: who did **not** get `check_env.py` green? Triage those with
      the assistant while you start Module 1 with everyone else.
- [ ] Share the Team Project link in the room chat.

---

## Each morning (Days 2–5)

- [ ] 10-min recap quiz from the *previous* day's `quiz.md` (do it live, hands up / cards).
- [ ] `git`-pull or re-share any lab fixes you made overnight.
- [ ] Check `console.anthropic.com` usage — if any candidate key is near its cap, top it up
      or reassign before they hit a wall mid-lab.
- [ ] Update the roster scorecard from yesterday's exam-style-question results.

## Each evening

- [ ] Log which slides ran long / short and any lab that confused people → note it in the
      trainer guide for next cohort.
- [ ] Mark the roster scorecard. Identify anyone trending < 60% in a domain — plan a
      targeted 1:1 at the next break.

---

## If you are running behind (in priority order, cut from the bottom)

Every day's `trainer-guide.md` has an explicit **"if behind, cut these"** list. General rule:
- **Never cut a lab.** Cut discussion, cut the second worked example, cut the recap slide.
- If a lab itself is running long, have people run the `solution/` and *read* it rather than
  finish the `starter/` — the learning is in reading working code under time pressure too.
- The Day 5 mock exam is immovable. Protect its 90 minutes even if it means trimming the
  capstone presentations to 3 minutes each.

---

## Known failure modes (whole-cohort)

| Failure | Prevention | In-the-moment fix |
|---|---|---|
| Half the room's `check_env.py` is red on Day 1 | T‑3 days screenshot gate | assistant triages in parallel; give red candidates a buddy with a working env for Module 1 |
| Corporate proxy kills the SDK mid-lab | firewall ticket at T‑2 weeks | `HTTPS_PROXY` env var; worst case, trainer's hotspot for the lab |
| One shared key → everyone rate-limited | one key per candidate (item 1) | reassign spare keys; stagger lab starts by table |
| SDK version bumped and an API shape changed | pin in `requirements.txt`; dry-run at T‑1 week | fall back to the `solution/` you validated; note the drift |
| Candidates paste their key into a lab file and commit it | `.env` + `.gitignore` taught in Day 0 | rotate the key immediately via Console; teachable moment on secrets |
