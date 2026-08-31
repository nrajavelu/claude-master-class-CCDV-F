# Video companion — optional pre-watch / review

A public **17-lesson video walkthrough** of the CCDV-F exam exists — ~3 hours, one video,
chapter markers per lesson, in **blueprint order**. It runs on the same method this bootcamp
teaches (`logistics/05-exam-method.md`): *every exam item is really one of four developer
decisions — **what runs** · **how does it call Claude** · **what does Claude see and say** ·
**will it survive production** — name the decision and four plausible options collapse to
two.*

- **Watch:** [youtube.com/watch?v=Lan-CbQ2IKM](https://www.youtube.com/watch?v=Lan-CbQ2IKM) —
  every row in the table below links straight to that lesson's timestamp (opens in a new tab).
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

| # | Lesson title | Watch | Bootcamp module | Domain |
|---|---|---|---|---|
| 1 | Every Question Is One of Four Decisions | [▶ 0:00](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=0s) | Day 1 M1 · `logistics/05` | method |
| 2 | One Ticket, One Call | [▶ 9:57](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=597s) | Day 1 M1 (Messages API, tokens, stateless, `stop_reason`, `usage`) | D2, D5 |
| 3 | Streaming, Vision, Thinking | [▶ 18:40](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=1120s) | Day 1 M3 (streaming); Day 5 (vision/PDF, thinking) | D2, D5 |
| 4 | The Quarter That Isn't About Claude | [▶ 28:36](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=1716s) | **Day 4** (requirements · systems life cycle · SW-eng foundations) | D2 |
| 5 | The Three Surfaces | [▶ 39:18](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=2358s) | Day 2 (system vs user vs API · untrusted content · schemas · tool descriptions); Day 3 (Claude Code surface) | D2, D6, D8 |
| 6 | Same Repo, Three Different Claudes | [▶ 50:01](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=3001s) | Day 4 (configuration management · project-config hierarchy · version pinning); Day 3 (Claude Code) | D2, D3 |
| 7 | Asking Is Not Making Sure | [▶ 1:00:52](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=3652s) | Day 2 (structured output · validation · schema-as-contract) | D6, D2 |
| 8 | A Bigger Window Makes It Worse | [▶ 1:10:36](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=4236s) | Day 4 (context engineering · compaction · memory) | D6 |
| 9 | The Three Places a Call Can Break | [▶ 1:19:58](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=4798s) | Day 1 M4 (typed errors, retries); Day 4 (debugging) | D4, D6 |
| 10 | input_tokens Is Not Your Input | [▶ 1:30:42](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=5442s) | Day 1 M5 (token/cost math); Day 5 (usage tracking, caching) | D5, D2 |
| 11 | Batch: Results in Any Order | [▶ 1:40:56](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=6056s) | Day 5 (batch API) | D2, D5 |
| 12 | The Description Is the Interface | [▶ 1:51:50](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=6710s) | Day 2 (tool implementation · tool descriptions) | D8 |
| 13 | An MCP Server Is Not a Bag of Tools | [▶ 2:02:43](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=7363s) | Day 3 (MCP server development) | D8 |
| 14 | Usually Fewer Agents | [▶ 2:12:59](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=7979s) | Day 3 (agent patterns · subagents · multi-agent) | D1 |
| 15 | Self-Hosted Is Not Air-Gapped | [▶ 2:24:14](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=8654s) | Day 3 (agent deployment surfaces); Day 5 (self-hosted vs managed) | D1 |
| 16 | The Attack Arrives as a Ticket | [▶ 2:35:19](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=9319s) | Day 2 (untrusted content); **Day 5** (AI application security · prompt injection) | D7 |
| 17 | Exam Day: Name the Decision First | [▶ 2:46:42](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=10002s) | Day 5 (exam-day routine) · `logistics/05 §6` | method |

---

## Second series — the hands-on **Build-Along course**

A separate YouTube series, *"Claude Certified Developer – Foundations · Build-Along Course"*,
walks the code. It is the **video form of the `epNN/` folders** in the parent
`claude-api-masterclass` repo — one PR-review agent grown episode by episode. Use it when a
candidate wants to *watch someone build* the thing a lab asks them to build.

- Course overview: [R3hHhqIOjA0](https://www.youtube.com/watch?v=R3hHhqIOjA0)
- Ep 01: [RheXq2HKJmY](https://www.youtube.com/watch?v=RheXq2HKJmY) — *Your First Agent on the Raw Messages API*
- **Remaining episode video IDs: TBD** — paste the playlist URL and they get wired into
  `portal/watch.html` (the "Build-along course" tab) the same way. Titles/mapping below are
  from the repo.

| Ep | Title | Repo folder | Bootcamp Day · module / lab | Watch |
|---|---|---|---|---|
| 01 | Your First Agent on the Raw Messages API | `ep01/` | **Day 1** · Lab 4 (agent loop by hand) | [▶](https://www.youtube.com/watch?v=RheXq2HKJmY) |
| 02 | Same Job on the Claude Agent SDK | `ep02/` | Day 3 · M3 (Agent SDK tour) | *TBD* |
| 03 | Custom Tool: Docstring Coverage Checker | `ep03/` | Day 2 · Lab 2; Day 3 · M7 | *TBD* |
| 04 | Hooks & Guardrails | `ep04/` | Day 3 · M4 · Lab 2 (blocking hook) | *TBD* |
| 05 | Subagents & the Coordinator | `ep05/` | Day 3 · M5 · Lab 1 (2-subagent auditor) | *TBD* |
| 06 | Memory, Sessions & Context That Survives | `ep06/` | Day 4 · M6 (context engineering) | *TBD* |
| 07 | Structured Output You Can Trust | `ep07/` | Day 2 · Lab 3 (strict schema + validation) | *TBD* |
| 08 | Skills: Reusable Agent Capabilities | `ep08/` | Day 3 · M6; Day 4 | *TBD* |
| 09 | MCP in the Real World | `ep09/` | Day 3 · M7 · Lab 4 (FastMCP server) | *TBD* |
| 10 | Choosing Your Model | `ep10/` | Day 5 · M1 (trade-off triangle) | *TBD* |
| 11 | Cost, Tokens & Reliability in Production | `ep11/` | Day 5 · M2–5 (caching, batch, fallbacks) | *TBD* |
| 12 | Managed Agents | `ep12/` | Day 5 (hand the runtime to Anthropic) | *TBD* |

> The **exam walkthrough** (series above) is for *how the exam thinks*; the **build-along**
> is for *how the code works*. Most candidates want the walkthrough for revision and the
> build-along the night before a hands-on day.

---

## Suggested viewing schedule — one-click

| When | Watch (opens at the timestamp, new tab) | Why |
|---|---|---|
| Before Day 0 *(recommended)* | [▶ L1 0:00](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=0s) | Get the "four decisions" lens first |
| Evening after Day 1 | [▶ L2 9:57](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=597s) · [▶ L3 18:40](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=1120s) · [▶ L9 1:19:58](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=4798s) · [▶ L10 1:30:42](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=5442s) | API mechanics · debugging · cost |
| Evening after Day 2 | [▶ L5 39:18](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=2358s) · [▶ L7 1:00:52](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=3652s) · [▶ L12 1:51:50](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=6710s) · [▶ L16 2:35:19](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=9319s) | Surfaces · schemas · tool descriptions · the injection attack |
| Evening after Day 3 | [▶ L13 2:02:43](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=7363s) · [▶ L14 2:12:59](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=7979s) · [▶ L15 2:24:14](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=8654s) | MCP · multi-agent · deployment surfaces |
| Evening after Day 4 | [▶ L4 28:36](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=1716s) · [▶ L6 50:01](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=3001s) · [▶ L8 1:10:36](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=4236s) | Requirements · config management · context window |
| Before the Day 5 mock | [▶ L11 1:40:56](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=6056s) · [▶ L17 2:46:42](https://www.youtube.com/watch?v=Lan-CbQ2IKM&t=10002s) | Batch · exam-day routine |

---

## Trainer note

When you cite a lesson in class, cite the **bootcamp artifact it maps to** as the primary
reference and the video as "another explanation of the same thing". The class's mental model
stays anchored to `logistics/05-exam-method.md`, which is kept in sync with the official exam
guide (the video may drift as the guide is revised).
