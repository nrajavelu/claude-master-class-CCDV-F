# Day 0 — Pre-work (self-paced, ~2–3 hours)

> Do this **at least 2 days before Day 1.** It is not optional. Candidates who arrive
> without a green environment lose the first half of Day 1 and hold up the room.

---

## Why Day 0 exists

The bootcamp is hands-on from the first hour of Day 1. That only works if, before you walk
in, your laptop can already talk to Claude. Day 0 gets you there and gives you just enough
Python to not be lost.

---

## Checklist

Work through these in order. Tick each box.

### 1. Set up your machine  ·  ~60–90 min

- [ ] Follow **`../logistics/00-environment-setup.md`** step by step.
- [ ] `python day0-prework/check_env.py` prints **All checks passed.**
- [ ] `python day0-prework/labs/hello_claude.py` prints a reply from Claude + a `usage:` line.

> Stuck for more than 20 minutes on any step? Stop, copy the exact error, and send it to the
> training coordinator. Do not lose your evening to a proxy setting.

### 2. Read the Python primer  ·  ~30–45 min

- [ ] Read **`python-primer.md`** top to bottom.
- [ ] You don't need to memorise it. You need to recognise every construct when you see it
      in a lab: `def`, `dict`, list comprehension, f-string, `with`, `async def` / `await`,
      `import`, virtual environment.

### 3. Look around  ·  ~15 min

- [ ] Open `../day1-foundations/slides/day1.html` in a browser. Press `→`. Get a feel for
      the deck; don't study it.
- [ ] Skim `../README.md` so you know how the week is shaped and what you're working toward
      (the Claude Certified Developer – Foundation exam).
- [ ] Note your Anthropic Console usage page — you'll watch your own token spend during labs.

### 4. Accounts (confirm you have them)  ·  ~10 min

- [ ] `ANTHROPIC_API_KEY` in your `.env` — from your org (see procurement guide).
- [ ] A **Claude Team** login works at claude.ai (you'll use Claude Code from Day 3; signing
      in can wait).
- [ ] *(If your coordinator asked for it)* a GitHub account + a read-only fine-grained PAT.

---

## "Done" definition

You are ready for Day 1 when every box above is ticked **and**:

```
python day0-prework/check_env.py      →  All checks passed. You are ready for Day 1.
python day0-prework/labs/hello_claude.py
    →  Claude: <a short sentence>
       usage: input_tokens=... output_tokens=...
```

Send a screenshot of both to the coordinator by the deadline you were given.

---

## What Day 0 is **not**

- Not a Python course. The primer is a phrasebook, not a grammar.
- Not where you learn the API. That's Day 1, Module 1.
- Not graded. But an un-done Day 0 is very visible on Day 1.
