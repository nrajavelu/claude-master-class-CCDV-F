# Day 4 — labs

| Lab | Goal | Reference | Built |
|---|---|---|---|
| `lab1_requirements_split/` | Sort a business brief into functional vs infrastructure + a 5-box architecture sketch; tag what the console-style app meets | walkthrough L4 | spec (paper) |
| `lab2_reproducible/` | Add a pinned model constant + committed `CLAUDE.md` + `config.toml`/`.env.example` + `.gitignore` to a script whose behaviour depended on uncommitted files; two people → same behaviour | `ep06/` · `capstone-support-assistant/config.toml` | spec + starter |
| **`lab3_rag_cited/`** | chunk → embed → cosine top-k → grounded prompt with `<doc id>` tags → answer **+ cite**; one out-of-corpus question → "not in the provided documents" | — (new) | **starter + solution + corpus** |
| `lab4_eval_harness/` | A 12-case golden set for lab 3's answerer, wired through `evals/harness.py` as `pytest`; introduce a regression → ≥ 3 tests red | `evals/` | uses `evals/` (see its README) |

Run from `aizentify-cdf-bootcamp/`. Model pinned to `claude-haiku-4-5`.

---

## lab1_requirements_split — spec (paper + a little tagging)
- **Given:** `brief.md` — a one-paragraph business brief for a "contract-clause checker".
- **Do:** produce two lists (functional / infrastructure) + a 5-box "what talks to what"
  sketch; tag each requirement the console-style app already meets vs doesn't.
- **Expected:** ~6 functional + ~5 infrastructure, correctly sorted; a one-line diagnosis
  ("meets every functional requirement, fails every infrastructure one").

## lab2_reproducible — spec
- **Given:** `starter/flaky_agent.py` — behaviour depends on an uncommitted local file and a
  hardcoded model string.
- **Do:** move the model id to a committed `config.toml`; move standing rules to a committed
  `CLAUDE.md`; add `.env.example` + `.gitignore`; leave nothing behaviour-affecting outside
  version control (except secrets).
- **Expected:** a checklist showing every behaviour-affecting input is now in VCS or an
  example config; `git status` shows no secret; a second checkout runs identically.

## lab3_rag_cited — starter + solution *(flagship)*
See `lab3_rag_cited/README.md`. Ships a 15-doc corpus and **both** embedding paths
(Voyage / local `sentence-transformers`).

## lab4_eval_harness — via `evals/`
- **Do:** write `day4-.../labs/lab4_eval_harness/golden_set.jsonl` (12 cases) for lab 3's
  `answer()`; run `python -m evals.harness --cases <that file> --target
  day4-applications-integration.labs.lab3_rag_cited.solution.rag:answer`; then break the
  grounding instruction and re-run.
- **Expected:** green on the good version; ≥ 3 failures after the regression, each naming the
  case + the failed check.
