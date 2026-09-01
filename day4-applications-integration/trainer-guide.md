# Day 4 — Trainer guide (slide-by-slide)

**Deck:** `slides/day4.html` (~26 slides) · **Recap:** `recap.html` · **Contact time:** ~7h
**Primary domains:** D2 (Applications & Integration, **33.1%** — Requirements, Systems Life Cycle, SW-Eng Foundations, Application Design, Configuration Management) · D6 (Context Engineering) · D4 (Evaluation).
**Anchor episodes:** `ep06` (memory/sessions/CLAUDE.md), `ep08` (skills). **Video:** walkthrough L4, L6, L8 · exam-guide D2 (10:28).

> **This is the 33% day.** Say it at the top: *"A quarter of this exam is software engineering
> that never mentions Claude, and it's the part most people under-study. Today is that part —
> plus context, RAG, and evals."*

---

## Project this — worked examples

Open the **worked-example page** for a snippet mid-explanation — it has the scenario, the code, and the *captured output* with a predict-then-reveal toggle: `portal/examples.html?f=<name>`. Hide the output, ask the room to predict it, then reveal.

This day's demos: `cookbook_building_evals` (code-graded vs judge on a 3-case golden set).

Offline / no budget: `python tools/capture_runs.py <name>` (mock) shows real program flow; `--live` for real numbers.

---

## Before this session
- [ ] Day 3 recap quiz. Decide the RAG embedding path (Voyage vs local) and confirm `requirements.txt`.
- [ ] Dry-run the Day 4 RAG + eval lab specs on whichever path you picked.
- [ ] Pre-open: `ep06/CLAUDE.md`, `ep06/session_index.py`, `ep06/context_check.py`, `ep08/.claude/skills/`.

## Timing plan
| Block | Time |
|---|---|
| Recap quiz | 09:00–09:15 |
| M1 requirements + **Lab · requirements split** | 09:15–10:15 |
| M2 systems life cycle | 10:15–10:40 *(break)* |
| M3 SW-eng foundations | 10:55–11:30 |
| M4 application design + config mgmt | 11:30–12:20 *(lunch)* |
| **Lab · make it reproducible** | 13:20–13:55 |
| M5 context engineering | 13:55–14:35 *(break)* |
| M6 RAG + **Lab · tiny RAG with citations** | 14:50–16:00 |
| M7 evaluation + **Lab · eval harness + regression** | 16:00–17:00 |
| Recap + exam-style Qs + quiz | 17:00–17:30 |

## If behind
1. RAG lab: index a pre-built corpus (provided) instead of building the chunker → focus on grounding + citation.
2. M3 SW-eng foundations — talk it against Rule 2, don't dwell.
3. **Never cut:** the requirements split lab, the eval lab, the exam-style-question block.

## Known failure modes
| Failure | Fix |
|---|---|
| requirements lab: everything sorted "functional" | infrastructure = what it runs on AND what the team must be able to *do to it* (deploy, roll back, monitor) |
| RAG lab: model answers from its own knowledge, ignores the docs | strengthen the grounding instruction: "answer ONLY from the provided docs; if not present, say so" |
| eval lab: LLM-judge is flaky | give it a yes/no rubric with one criterion; don't ask it to score 1–10 |
| "implement = write code" confusion | implement = deploy where users are; production credit is operate + maintain |

---

## Slide-by-slide (navigate by title)

### Title + orientation — 4 min · Decisions ③ & ④. "The 33% day."

### M1 · One sentence → two lists (Exam watch) — 6 min
- The split SVG. **Functional** = what it does. **Infrastructure** = what it runs on *and* what the team must be able to do to it.
- Every stem in this skill asks you to sort or derive one list.
- *Ref:* walkthrough L4 · exam-guide D2 (10:28).

### **Lab · requirements split** — 25 min
- Business brief → two lists + a 5-box architecture sketch → tag what the console-style app meets vs not.

### M2 · Four stages — "implement" means deploy (Exam watch) — 6 min
- develop → **implement (deploy where users are)** → operate → maintain. Production credit: operate + maintain.
- Who deploys → implement. Who gets the 2 a.m. call → operate. When retired → maintain.

### M3 · What turns code into a service anyone owns — 6 min
- Version control (→ rollback is picking the last good version) · code review · pipeline (branch→review→test→deploy) · refactoring (small & large; safe only with history + tests).
- **Rule 2 lives here:** "any engineer can roll back" kills "write a setup doc" — a doc is guidance; VCS + pipeline is the mechanism.

### M4 · Where Claude sits = which contract applies (Exam watch) — 7 min
- The 3-column SVG: chat interface (streaming + session state your app keeps) · API endpoint wrapping Claude (its own timeout + error contract) · background job (→ batch).
- *Say:* "A scenario describing *where* Claude sits is really asking *which contract* applies. Choose by latency; the cost follows."

### M4 · Application design = requirements before code — 6 min
- Interface? latency budget? **failure behaviour** (the model WILL return something unusable → validation · retries with backoff · fallback · human escalation). SW-eng: idempotency · logging · separate the prompt layer from business logic.
- **This is the single biggest D2 sub-skill** — worth more than Claude Code + Debugging combined.

### M4 · Same repo, three different Claudes (Exam watch) — 5 min
- The config SVG. Pin the model. Commit `CLAUDE.md`. Env-specific settings in a committed example config. Secrets in `.gitignore`.
- *Ref:* `ep06` (CLAUDE.md discovery, `setting_sources`) · walkthrough L6.

### M4 · A prompt edit IS a deployment (Exam watch) — 4 min
- Keys in env / a secrets manager — never in code, never in the client. **Key in a mobile app → a backend proxy, no exceptions.**
- Prompts are versioned artifacts, tested before rollout. Model choice is config — an upgrade is a decision with a test pass.

### **Lab · make it reproducible** — 35 min
- Add a pinned model constant + committed `CLAUDE.md` + `config.toml`/`.env.example` + `.gitignore` to a script whose behaviour depended on uncommitted local files. Two people → same behaviour.

### M5 · A bigger window makes it worse (Exam watch) — 7 min
- The window-contents SVG: input + tool schemas + history + the answer, all billed.
- **Compaction** = summarise · **context-editing** = clear old tool-results/thinking · **memory tool** = write to disk. One session per task.
- *Ref:* `ep06/context_check.py` · walkthrough L8.

### M6 · The RAG pipeline — 6 min
- chunk → embed → similarity search → grounded prompt (`<doc id>`) → answer **+ cite**. Out-of-corpus → say so.
- RAG vs long-context vs fine-tune: retrieve when the knowledge is large / changing / must be cited. No first-party Anthropic embeddings API (Voyage or local).

### **Lab · tiny RAG with citations** — 50 min
- ~15 docs · chunk (~500 tok, overlap) · embed · cosine top-k · grounded prompt · answer + cite · one out-of-corpus question.

### M7 · Assert on structure, not wording (Exam watch) — 6 min
- The eval-harness SVG. A **golden set** run against every prompt or model change → quality is measured, not vibed. (A prompt edit is a deployment → run the golden set.)
- Three check types: structural assertion · keyword/contains · **LLM-as-judge** (yes/no rubric). Wire as `pytest`.

### **Lab · eval harness + regression** — 45 min
- 12-case eval set · 3 checks · `pytest` · introduce a regression → ≥ 3 tests red, each naming the case + failed check.

### Recap + exam-style Qs + quiz — 30 min
- `exam-style-questions.md` → `quiz.md` → `portal/practice.html?day=4` → `question-bank/scenario-questions.md` (Q2, Q3, Q7).
