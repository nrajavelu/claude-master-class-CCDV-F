# Video companion — optional pre-watch / review

A public **17-lesson video walkthrough** of the CCDV-F exam exists — ~3 hours, one video,
chapter markers per lesson, in **blueprint order**. It runs on the same method this bootcamp
teaches (`logistics/05-exam-method.md`): *every exam item is really one of four developer
decisions — **what runs** · **how does it call Claude** · **what does Claude see and say** ·
**will it survive production** — name the decision and four plausible options collapse to
two.*

- Video: `https://www.youtube.com/watch?v=Lan-CbQ2IKM` (chapter markers below)
- It builds one support-desk system across all 17 lessons, from a single API call to a
  secured, budgeted, tool-using system; each exam skill arrives as the decision that fixes a
  real incident in that build.

> **Not required.** The bootcamp's decks, labs, and question bank are the source of truth and
> are kept aligned to the official exam guide. Use the video as a second voice and an evening
> review. Lesson 1 (framework) is a good pre-course watch.

---

## Authoritative coverage map (guide order · published weights)

| Domain | Weight | Video lessons | The decision | Bootcamp day |
|---|---:|---|---|---|
| **D1 Agents and Workflows** | 14.7% | **14, 15** | *what runs* | Day 3 (Day 1 intro) |
| **D2 Applications and Integration** *(biggest)* | 33.1% | **2, 3, 4, 5, 6, 10, 11** | splits across **three** decisions | Days 1, 2, **4** |
| **D3 Claude Code** | 3.1% | **6** | *what does Claude see and say* / *survive production* | Day 3 |
| **D4 Eval, Testing, and Debugging** | 2.6% | **9** | *survive production* | Day 1 (errors) + Day 4 |
| **D5 Model Selection and Optimization** | 16.8% | **2, 3, 10** | *how does it call Claude* | Days 1, **5** |
| **D6 Prompt and Context Engineering** | 11.0% | **7, 8, 9** | *what does Claude see and say* | Days 2, 4 |
| **D7 Security and Safety** | 8.1% | **16** | *will it survive production* | Days 3, **5** |
| **D8 Tools and MCPs** | 10.6% | **12, 13** | *what runs* | Days 2, 3 |
| *(framework)* | — | **1** | the four decisions + two rules | Day 1 M1 |
| *(capstone)* | — | **17** | four items at exam speed | Day 5 mock review |

**A quarter of the exam is software engineering that never mentions Claude — video lesson 4
owns it, and so does our Day 4.**

---

## Lesson → chapter → bootcamp module

| # | Lesson title | Timestamp | Bootcamp module | Domain |
|---|---|---|---|---|
| 1 | Every Question Is One of Four Decisions | 0:00 | Day 1 M1 · `logistics/05` | method |
| 2 | One Ticket, One Call | 9:57 | Day 1 M1 (Messages API, tokens, stateless, `stop_reason`, `usage`) | D2, D5 |
| 3 | Streaming, Vision, Thinking | 18:40 | Day 1 M3 (streaming); Day 5 (vision/PDF, thinking) | D2, D5 |
| 4 | The Quarter That Isn't About Claude | 28:36 | **Day 4** (requirements · systems life cycle · SW-eng foundations) | D2 |
| 5 | The Three Surfaces | 39:18 | Day 2 (system vs user vs API · untrusted content · schemas · tool descriptions); Day 3 (Claude Code surface) | D2, D6, D8 |
| 6 | Same Repo, Three Different Claudes | 50:01 | Day 4 (configuration management · project-config hierarchy · version pinning); Day 3 (Claude Code) | D2, D3 |
| 7 | Asking Is Not Making Sure | 1:00:52 | Day 2 (structured output · validation · schema-as-contract) | D6, D2 |
| 8 | A Bigger Window Makes It Worse | 1:10:36 | Day 4 (context engineering · compaction · memory) | D6 |
| 9 | The Three Places a Call Can Break | 1:19:58 | Day 1 M4 (typed errors, retries); Day 4 (debugging) | D4, D6 |
| 10 | input_tokens Is Not Your Input | 1:30:42 | Day 1 M5 (token/cost math); Day 5 (usage tracking, caching) | D5, D2 |
| 11 | Batch: Results in Any Order | 1:40:56 | Day 5 (batch API) | D2, D5 |
| 12 | The Description Is the Interface | 1:51:50 | Day 2 (tool implementation · tool descriptions) | D8 |
| 13 | An MCP Server Is Not a Bag of Tools | 2:02:43 | Day 3 (MCP server development) | D8 |
| 14 | Usually Fewer Agents | 2:12:59 | Day 3 (agent patterns · subagents · multi-agent) | D1 |
| 15 | Self-Hosted Is Not Air-Gapped | 2:24:14 | Day 3 (agent deployment surfaces); Day 5 (self-hosted vs managed) | D1 |
| 16 | The Attack Arrives as a Ticket | 2:35:19 | Day 2 (untrusted content); **Day 5** (AI application security · prompt injection) | D7 |
| 17 | Exam Day: Name the Decision First | 2:46:42 | Day 5 (exam-day routine) · `logistics/05 §6` | method |

---

## Suggested viewing schedule

| When | Lessons | Why |
|---|---|---|
| Before Day 0 *(optional but recommended)* | 1 | Get the "four decisions" lens first |
| Evening after Day 1 | 2, 3, 9, 10 | API mechanics · debugging · cost, all just taught |
| Evening after Day 2 | 5, 7, 12, 16 | Surfaces · schemas · tool descriptions · the injection attack |
| Evening after Day 3 | 13, 14, 15 | MCP · multi-agent · deployment surfaces |
| Evening after Day 4 | 4, 6, 8 | Requirements · config management · context window |
| Before the Day 5 mock | 11, 17 | Batch · exam-day routine |

---

## Trainer note

When you cite a lesson in class, cite the **bootcamp artifact it maps to** as the primary
reference and the video as "another explanation of the same thing". The class's mental model
stays anchored to `logistics/05-exam-method.md`, which is kept in sync with the official exam
guide (the video may drift as the guide is revised).
