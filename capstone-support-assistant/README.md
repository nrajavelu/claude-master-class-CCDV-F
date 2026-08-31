# capstone-support-assistant — build one small thing, let it drag you through the blueprint

The CCDV-F exam guide's 4-week plan says: **ship one small support assistant** — an API
integration with **two tools (a lookup + an action)**, a **system prompt**, and a **cost
budget** — and let it touch every heavyweight domain. This folder is that assistant. You
flesh out `starter/assistant.py`; `assistant.py` is the reference.

```
cd aizentify-cdf-bootcamp
cp capstone-support-assistant/.env.example capstone-support-assistant/.env   # add your key (or use the repo-root .env)
python capstone-support-assistant/starter/assistant.py "Where is order A-1002? If it's lost, refund it."
```

---

## What's here

| File | Role | Domain it exercises |
|---|---|---|
| `system_prompt.txt` | the assistant's **contract** — a versioned artifact, changed deliberately | D6 · D2 (config mgmt) |
| `config.toml` | model **pinned**, per-run **cost budget** (USD), tier map | D2 (config mgmt) · D5 |
| `.env.example` | key placeholder — real key never committed | D7 (secrets) |
| `tools.py` | `lookup_order` (read) + `issue_refund` (**action**), mock data, path-safe | D8 · D7 (least privilege) |
| `assistant.py` | the **ReAct loop**: reason → act → observe; cost tracking; **budget stop**; a guardrail on `issue_refund` | D1 · D5 · D7 |
| `starter/assistant.py` | same with `# TODO`s | — |
| `golden_set.jsonl` | 8 cases for this assistant — run before every prompt/model change | D4 |
| `run_golden.py` | runs `golden_set.jsonl` through `../evals/harness.py` | D4 |

---

## The 4-week plan, mapped to this repo

| Week | Do | File(s) |
|---|---|---|
| **1 · foundations + API** | build the plain loop (messages, system, streaming); **break it** — hit the token cap and read `stop_reason`; trip a rate limit and write the backoff | `starter/assistant.py` TODO 1–4 · `../code-snippets/retry_chain.py` |
| **2 · the heavyweights** | add the **two tools**; watch the model choose them; **sabotage the `issue_refund` description** and watch it misroute; add **caching** to the system-prompt prefix and check `usage` before/after; price the assistant at **3 tiers** in `config.toml` and pick deliberately | `tools.py` · TODO 5–8 · `../code-snippets/prompt_caching.py` |
| **3 · judgement domains** | convert the "list all open orders and summarise" flow into a **routed workflow** and argue why it shouldn't be an autonomous agent; **paste an injection** into a fake order note and fix the design (structure · least privilege · a **blocking guardrail** on `issue_refund`) | TODO 9 · `hooks.py` · `../code-snippets/blocking_hook.py` |
| **4 · rehearsal** | re-read the exam guide as a checklist ("can I do this in code?"); run `golden_set.jsonl` after every change; timed practice; weakest domain gets the final hours; **book the exam while the commits are fresh** | `run_golden.py` · `portal/practice.html` · `logistics/03 §8` |

---

## The cost budget (D5)

`config.toml` sets `budget_usd` per run. `assistant.py` accumulates `usage` cost after every
turn and **stops with a clear message** if the next turn would blow the budget — the
"defined way to fail" a production agent loop needs, alongside the iteration cap.

## The guardrail (D7)

`issue_refund` is an **action** tool. `assistant.py` gates it: a refund over a threshold, or
one triggered by text that looks like an injected instruction, is **refused in code** — the
model's intent doesn't decide. Order-note text is treated as untrusted data. Least privilege:
a "just look it up" run is given only `lookup_order`.
