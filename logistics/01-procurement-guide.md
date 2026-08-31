# Procurement guide — what the organisation must provide per candidate

> Give this document to whoever holds the training budget and IT approval.
> Everything here must be in place **before Day 0 pre-work** (which is ~2 weeks
> before the classroom week). Items 1 and 2 have lead time — start now.

---

## TL;DR for the budget holder

To run this course effectively you need **two things per candidate that cost money**:

1. **An Anthropic API key with a small prepaid credit balance** (~US $30–50 each).
   This is what every hands-on lab actually calls. **Non-negotiable** — without it the
   course is a lecture, not a bootcamp.
2. **A Claude Team plan seat.** Strongly recommended. It is how candidates run the
   agent labs without juggling personal keys, and — more importantly — it is the tool
   they keep using at their desks after the week ends. **This is the investment that makes
   the training stick.**

Everything else is free (GitHub, Claude Code CLI, Python tooling) or optional.

---

## Full checklist (per candidate)

| # | Item | Cost | Required? | Lead time |
|---|------|------|-----------|-----------|
| 1 | Anthropic Console account + API key + prepaid credit | ~$30–50 | **Mandatory** | 1–3 days |
| 2 | Claude **Team** plan seat | ~$25–30/user/mo (annual) or ~$30/mo (monthly), **min 5 seats** | **Strongly recommended** | 1–5 days (billing + admin setup) |
| 3 | Claude Code CLI | Free | Mandatory | minutes |
| 4 | GitHub account + fine-grained **read-only** PAT | Free | Mandatory | minutes |
| 5 | Voyage AI API key (free tier) **or** accept local embeddings | Free | Optional (Day 4) | minutes |
| 6 | Laptop: 16 GB RAM, 10 GB free disk, **local admin rights** | — | Mandatory | — |
| 7 | Network: outbound HTTPS to a short allow-list | — | Mandatory | **days** (raise the ticket now) |

---

## 1. Anthropic API key + prepaid credit — MANDATORY

**What it is.** A key (`sk-ant-...`) from the **Anthropic Console** (console.anthropic.com),
backed by a credit balance. Every lab from Day 0 (`hello_claude.py`) through the Day 5
capstone makes real API calls with this key.

**Why a Team seat is not enough.** The Claude **Team** plan (item 2) is the *chat product* —
claude.ai in the browser and the Claude Code CLI. It does **not** include API credits and
cannot authenticate raw `anthropic` SDK calls (Days 1–2, and all the evaluation/RAG/vision
labs). These are different products with different billing. **You need both.**

**How to set it up (recommended shape):**

1. One **Console organisation** for the cohort (or reuse the company's existing org).
2. One **Workspace** named e.g. `cdf-bootcamp-2026-03`.
3. **One API key per candidate**, named after them, all inside that workspace.
4. Set a **per-workspace spend limit** (e.g. `$50 × headcount`) and, if available, a
   **per-key monthly limit** of `$50`. This caps blast radius if a key leaks or a loop
   runs away.
5. Load prepaid credit for the whole workspace up front.

**Budget basis.** Labs are deliberately small and pinned to **Claude Haiku 4.5 / Sonnet 5**
(cheap tiers). Realistic consumption for the full week, including re-runs and the capstone,
is **well under $20/candidate**. Provision **$30–50** for headroom, experimentation, and the
optional "try it on Opus" comparisons on Day 5.

**Do NOT** distribute one shared key to the class — you lose per-candidate spend visibility
and one person's rate-limit error becomes everyone's.

---

## 2. Claude Team plan — STRONGLY RECOMMENDED (push for this)

**What it is.** claude.ai for organisations: per-seat, central billing, an admin console,
and **Projects** (shared, persistent workspaces with their own instructions and files).
Buy through claude.ai → *Settings → Plans* (or *Get Team plan*). Minimum **5 seats**.

**Why it matters for this course:**

| Benefit | Where it's used |
|---|---|
| **Claude Code sign-in via OAuth** — candidates run `claude` and the Agent SDK labs authenticate against their Team seat, no personal API key to paste or leak | Days 3–5 (every SDK lab), and the capstone |
| **Higher usage limits** than free/Pro — a room full of people running agents at once won't all hit caps | Days 3–5 |
| **Projects** — the trainer publishes one Project with the class's `CLAUDE.md` conventions, prompt patterns, and the exam blueprint; everyone works from the same base | All week; reference material |
| **Admin controls & central billing** — IT keeps visibility; no reimbursement paperwork | Procurement/IT |
| **It outlives the course** — candidates return to their teams already equipped to use Claude daily. This is the adoption flywheel the training is meant to start | After the week |

**Why to push for it even if budget is tight:** the alternative (everyone on personal
free accounts) means inconsistent limits, no shared Project, no admin visibility, and — the
real cost — the skills evaporate because people go back to desks with no tool. A Team seat is
the difference between "we sent five people on a course" and "five people now build with
Claude."

**Clarify for the buyer, so there's no surprise:** Team seats and API credit (item 1) are
**billed separately** and **do not substitute for each other**. You are buying both.

---

## 3. Claude Code CLI — MANDATORY, free

`npm install -g @anthropic-ai/claude-code`, then `claude` to sign in.
Authenticates against the Team seat (item 2) **or** an API key (item 1). Used from Day 3.
Requires **Node.js 18+** (see `00-environment-setup.md`).

---

## 4. GitHub account + fine-grained PAT — MANDATORY, free

Day 3's MCP lab connects to GitHub's official remote MCP server. Each candidate needs:

- A GitHub account (personal is fine).
- A **fine-grained personal access token**, **read-only**, scoped to **Pull requests** on
  **one** throwaway/public repo. Nothing broader.

The token is pasted into a local `.env` as `GITHUB_PAT` — never committed. The lab teaches
exactly why (env-var expansion in `.mcp.json`).

---

## 5. Embeddings for the Day 4 RAG lab — OPTIONAL

The RAG lab needs an embedding model. Two supported paths; **pick one before the cohort**:

- **Path A — Voyage AI (hosted).** Free tier (hundreds of millions of tokens) more than
  covers the lab. One `VOYAGE_API_KEY` per candidate from voyageai.com. Adds a second
  vendor to your approval list.
- **Path B — local, no key.** `pip install sentence-transformers`; first run downloads a
  ~90 MB model. No new vendor, no key, works offline after the download. Slightly slower.

If your organisation is strict about new SaaS vendors, choose **Path B** and skip item 5
entirely. The lab ships both code paths.

*(Anthropic does not offer a first-party embeddings API; Voyage is its recommended partner.
The course stays honest about this.)*

---

## 6. Laptops — MANDATORY specs

| Spec | Minimum | Notes |
|---|---|---|
| RAM | 16 GB | 8 GB works but is tight with an IDE + browser + agents |
| Free disk | 10 GB | Python, Node, venv, model download for Path B |
| OS | macOS 12+, Windows 11 (+ WSL2 recommended), or Linux | Windows-native works; WSL2 is smoother for Claude Code |
| **Admin rights** | **Required** | To install Python, Node, VS Code and create virtualenvs. Locked-down SOE machines are the #1 cause of a lost Day 0. |
| Screen | 1080p+ | Split editor + terminal + slides |

Provide **one spare fully-provisioned laptop** per 8 candidates.

---

## 7. Network / firewall — MANDATORY, has lead time

Corporate proxies and TLS-inspection break the SDKs in confusing ways. **Raise the firewall
ticket the same day you nominate candidates.** Outbound **HTTPS (443)** must be allowed to:

| Host | Used for |
|---|---|
| `api.anthropic.com` | all Claude API calls |
| `console.anthropic.com`, `claude.ai` | account setup, Claude Code OAuth |
| `registry.npmjs.org` | Claude Code install |
| `pypi.org`, `files.pythonhosted.org` | `pip install` |
| `github.com`, `api.github.com`, `api.githubcopilot.com` | Day 3 MCP lab |
| `fonts.googleapis.com`, `fonts.gstatic.com` | slide fonts (cosmetic; decks degrade gracefully) |
| `huggingface.co`, `cdn-lfs.huggingface.co` | *only if using RAG Path B* (model download) |
| `api.voyageai.com` | *only if using RAG Path A* |

If TLS inspection cannot be disabled for these hosts, candidates must be able to point
`REQUESTS_CA_BUNDLE` / `SSL_CERT_FILE` at the corporate root CA. Document your org's method
in an appendix to `00-environment-setup.md` before the cohort.

---

## Ownership & timeline

| When | Who | Action |
|---|---|---|
| **T‑2 weeks** | Training coordinator | Nominate candidates. Send them `day0-prework/`. Raise the firewall ticket (item 7). Start Team plan procurement (item 2). |
| **T‑1 week** | IT / admin | Create the Console workspace + one key per candidate + spend limits (item 1). Send Team seat invites (item 2). Confirm laptop specs + admin rights (item 6). |
| **T‑3 days** | Candidates | Complete Day 0. Run `check_env.py` until it is all-green. Report blockers to the coordinator. |
| **T‑3 days** | Trainer | Dry-run every lab on a clean machine with a real cohort key (see `02-trainer-prep-checklist.md`). |
| **T‑0** | Trainer | 15-min morning smoke test before Module 1 (see `04-cohort-runbook.md`). |

---

## 8. Exam registration — check this early (no cost, but has lead time)

The **CCDV-F exam** itself is booked separately by each candidate (~US $125/attempt — confirm
the current fee on the official page). Registration currently runs through **Anthropic's
partner academy**, which typically requires a **company email on a recognised partner
domain**. If your organisation is **not yet in Anthropic's partner network**, that enrolment
is the conversation to start *now* — the entry tier generally costs an organisation nothing
to join, but approval takes time.

Action for the coordinator at **T‑2 weeks**: confirm (a) the org is in the partner network
or has started joining, and (b) each candidate can register with their company email. Don't
let this surface on the Friday of the course.

*(Fee, time limit, pass mark, and retake policy move periodically — always read them off the
current official exam page, not from any slide or notes.)*

---

## What you are NOT buying

- No paid IDE — VS Code is free.
- No cloud VMs — everything runs on the laptop.
- No vector database — Day 4 uses an in-memory index on purpose (concept first).
- No Anthropic "Managed Agents" spend — Day 5 covers it conceptually; the one optional
  live demo is the trainer's to run, not 16 candidates'.
