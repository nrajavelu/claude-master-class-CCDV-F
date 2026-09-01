# Day 2 — Trainer guide (slide-by-slide)

**Deck:** `slides/day2.html` (~19 slides) · **Recap:** `recap.html` · **Contact time:** ~6h + breaks
**Primary domains:** D6 (Prompt & Context Eng, 11%) · D8 (Tools & MCPs, 10.6% — Tool Implementation) · D2 (structured output).
**Anchor episodes:** `ep03` (custom tool), `ep07` (structured output + validation), `ep04` (guardrails).
**Video:** walkthrough L5, L7, L12, L16 · exam-guide D6 (21:39), D8 (26:09) · Build-along Ep 03, Ep 07.

---

## Project this — worked examples

Open the **worked-example page** for a snippet mid-explanation — it has the scenario, the code, and the *captured output* with a predict-then-reveal toggle: `portal/examples.html?f=<name>`. Hide the output, ask the room to predict it, then reveal.

This day's demos: `prompt_structure` (contract in system) · `strict_tool` (schema + validate() layer) · `cot_structured`.

Offline / no budget: `python tools/capture_runs.py <name>` (mock) shows real program flow; `--live` for real numbers.

---

## Before this session
- [ ] Day 1 recap quiz (10 min, live). Confirm every candidate's env still green.
- [ ] Dry-run `code-snippets/prompt_structure.py`, `cot_structured.py`, `strict_tool.py` on a clean machine.
- [ ] Pre-open: the deck, a terminal in `day2-prompt-tools-output/`, `ep03/tools.py` + `ep07/schemas.py` in tabs.

## Timing plan
| Block | Time |
|---|---|
| Recap quiz (Day 1) | 09:00–09:15 |
| Module 1 — prompt engineering + CoT recap | 09:15–10:00 |
| Module 2 — the three surfaces | 10:00–10:35 *(break)* |
| Module 3 — boundaries & untrusted content | 10:50–11:20 |
| Module 4 — tools: the description is the interface | 11:20–12:00 |
| **Lab · tool description** | 12:00–12:40 *(lunch)* |
| Module 5 — structured output + validation | 13:40–14:30 |
| **Lab · strict output + validation** | 14:30–15:20 *(break)* |
| Bridge to the SDK + **Lab · port the tool** | 15:35–16:15 |
| Recap + exam-style Qs + quiz | 16:15–17:00 |

## If behind (cut from the bottom)
1. "Bridge to the SDK" as a demo only (run `ep03/agent.py`), skip the port lab → homework.
2. Module 1 few-shot sub-point — the drill covers it.
3. **Never cut:** the strict-output lab, the three-surfaces slide, the exam-style-question block.

## Known failure modes
| Failure | Fix |
|---|---|
| `strict` lab: schema rejected | a feature the schema uses isn't supported — rejected, not ignored; simplify the schema |
| candidates put `role:"system"` in `messages` | that's the exact distractor — no such thing on the API |
| tool-description lab: model calls the tool fine even with the vague description | make the vague one vaguer (drop "when to use it"); or add a distractor tool with an overlapping name |

---

## Slide-by-slide (navigate by title)

### Title + orientation — 4 min
- Frame: "Day 1 was the engine. Today: steering it on purpose, and getting output your *code* can trust." Decision ③.

### Module 1 · Contract in `system` / task in `messages` — 6 min
- The split. Callback to Day 1: whoever put the instruction in a user message — here's why it belongs in `system`.
- *Say:* "The contract is what you'd paste every turn."

### Module 1 · Explicit · structure · show-don't-tell — 6 min
- Three cards. Stress **structure with tags** doubles as the first line of injection defence (Module 3 payoff).
- **Exam note on the slide:** two prompts both correct → the exam prefers the shorter one with a concrete example.
- *Ref:* `code-snippets/prompt_structure.py` · `exercises.md` B (Day 1) graded version is Lab 1 today.

### Module 2 · The three surfaces (Exam watch) — 8 min
- The SVG. Walk each column. The one they forget: **the coding-tool rules file arrives as a *user message*** — later messages sit at the same level, so it's a weaker promise than `system`.
- **The trap:** an option offering a message with `role:"system"`. Kill on sight.
- *Say:* "Prototype anywhere. Re-prove it on the surface it will actually run on."
- `live demo` — walkthrough L5 (39:18) if time; else the exam-guide D6 chapter.

### Module 3 · `tool_result` is the untrusted channel — both ways (Exam watch) — 7 min
- The SVG. External content **in** via `tool_result` ✓. Your own instructions **in** via `tool_result` ✗ (that channel is read with suspicion).
- Need to say something after a tool runs? Next turn, your own channel.
- Forward ref: full security pass is Day 5 M7.

### Module 4 · A tool description is a job posting — 8 min
- The tool-anatomy SVG. `description` is the glowing box: **the biggest factor** in correct use. Say what it does, **when to use it, and when NOT to**; unambiguous parameters.
- Tool called at the wrong time → fix the **description** before the model. "Add a routing model / fine-tune" is the **overbuild** — name it.
- Parallel `tool_use` → one user message of `tool_result` blocks, ids matching (Day 1 rule 2 again).
- *Ref:* `ep03/tools.py` description style · walkthrough L12 · exam-guide D8 (26:09).

### **Lab · a tool with a real description** — 35 min
- Launch: "Define `lookup_order` twice — vague, then detailed. 5 prompts through each."
- Circulate for: a vague description that's still too good (make it vaguer); not writing the "why" sentence.
- Green light: vague version mis-calls/skips ≥ 2 prompts; detailed version correct on all 5; one written sentence on why.

### Module 5 · Asking is not making sure (Exam watch) — 10 min
- The SVG (prompt-only "maybe" vs `strict` "guaranteed"). Then the four bullets:
  - `strict` is on the **tool definition**; `additionalProperties:false` + everything in `required`.
  - No "optional" → nullable type.
  - **Unsupported schema features are rejected, not ignored.**
  - `messages.parse()` validates for you.
  - **Prefilling** — the exam still references it; rejected on newest models (→ `output_config.format`). Teach both.
- *Ref:* `ep07/schemas.py` (the honest note: `strict` isn't forwarded on the SDK `@tool` path → `validate()` enforces) · walkthrough L7 · Build-along Ep 07.

### Module 5 · Validate, don't hope — 5 min
- The focus-code (`validate_finding`). Every error message goes straight back to the model → be specific so it can fix and resubmit.

### **Lab · strict output + validation** — 45 min
- `FINDING_SCHEMA` + `validate_finding()` + `messages.parse()`. 3 inputs: clean · wrong-severity · missing-line.
- Green light: clean recorded; bad ones rejected with a precise message; `parse()` path returns a typed object or raises.
- *Ref:* `code-snippets/strict_tool.py` (a runnable version to project).

### Bridge · the same tool on the SDK — 4 min + **Lab · port** 25 min
- `@tool` + `create_sdk_mcp_server` + `query()` with scoped `allowed_tools`. Run `ep03/agent.py`.
- Green light: SDK run produces the same tool call + result as the raw-API version.

### Recap + exam-style Qs + quiz — 45 min
- `exam-style-questions.md` at tables → `quiz.md` → `portal/practice.html?day=2`.
- Weak on D8? → `question-bank/domain-8-tools-mcps.md` + `ep03` + Build-along Ep 03.
