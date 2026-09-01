# Domain 3 — Claude Code  ·  3.1%  ·  decision ③ / ④

> **Status: populated (8/8).** Anchor: `ep06/CLAUDE.md`, `ep08/.claude/`. Video: lesson 6.
> Taught Day 3 Module 5. Deeper prose: `../topic-briefings.md` · Day 3 · "Claude Code
> operation"; checklist: `../blueprint-mastery-map.md` 3.1.

## Sub-area & topics

| Sub-area | Weight | Items | Topics |
|---|---:|---:|---|
| Claude Code Operation | 3.1% | 8 | rules / memory (`CLAUDE.md`) · skills (`.claude/skills/*/SKILL.md`) · slash commands · agents (`.claude/agents/*.md`) · sub-agents · the **project-config discovery hierarchy** (cwd upward) · **`settings.json` precedence** (managed > CLI > local > project > user) and the **permissions-accumulate** exception · the **six permission modes** · headless / print / streaming / auto modes · how a rules file reaches the model (as a **user message**, not `system`) · `CLAUDE.md` dilution |

---

## Items

### 1. (SBA) A `CLAUDE.md` in a subfolder and one at the repo root both exist. When Claude Code runs from the subfolder, which applies?
A. only the subfolder one  B. only the root one  C. both — discovered from cwd upward  D. neither unless passed explicitly

> **Answer:** C — project config is discovered from the working directory up to the repo root; both load.
> **Distractors:** A/B — partial discovery, not how it works. D — discovery is automatic, not explicit.

### 2. (SBA · right-word-wrong-place) The rules you write in a Claude Code rules file arrive at the model as:
A. the top-level `system` field  B. content in a `user` message  C. a `role: "system"` message  D. a tool definition

> **Answer:** B — they land in the conversation channel, so later messages sit at the same level.
> **Distractors:** A — plausible but wrong; the harness injects them as user content. C — **right-word-wrong-place**: no message may have `role: "system"`. D — wrong mechanism.

### 3. (SCN) You need Claude Code to run in CI with no human at the keyboard and pipe its answer to another step. Which mode?
A. interactive  B. headless / print (`claude -p "..."`)  C. plan mode  D. it can't

> **Answer:** B — print mode emits a result to stdout for the next CI step.
> **Distractors:** A — needs a TTY. C — still interactive. D — false.

### 4. (SBA · Claude Code Operation) A repo's `.claude/settings.json` allows `Bash(git push:*)`. A developer's `~/.claude/settings.json` denies it. On `git push`:
A. allowed — project scope outranks user scope  B. denied — permission rules accumulate across scopes and deny always wins  C. prompts each time  D. undefined

> **Answer:** B — `permissions` are the exception to override precedence; they accumulate, and deny beats allow at every scope.
> **Distractors:** A — **right-word-wrong-place**: applies normal precedence to the one key it doesn't govern. C/D — invented behaviour.

### 5. (SBA · Claude Code Operation) Which permission mode is the only one that skips the protected-path guard, and is therefore for isolated environments only?
A. `acceptEdits`  B. `plan`  C. `dontAsk`  D. `bypassPermissions`

> **Answer:** D.
> **Distractors:** A — auto-accepts file edits but keeps the guard. B — read-only planning. C — allow-list only, guard intact.

### 6. (SBA · order) The `settings.json` precedence order, highest first, is:
A. user > project > local > CLI > managed  B. managed > CLI > local > project > user  C. project > user > managed > CLI > local  D. CLI > managed > user > project > local

> **Answer:** B — org-managed settings can't be overridden; user settings are the weakest.
> **Distractors:** A — exactly reversed. C/D — scrambled.

### 7. (SCN · dilution) A 400-line `CLAUDE.md` keeps getting a specific build rule wrong even though the rule is in there. Best fix?
A. put the rule in ALL CAPS at the top  B. move narrow, path-specific guidance into `.claude/rules/*.md` scoped by a `paths` glob and keep `CLAUDE.md` short  C. repeat the rule five times  D. switch to a bigger model

> **Answer:** B — `CLAUDE.md`'s failure mode is dilution; a shorter file plus scoped rules restores attention.
> **Distractors:** A/C — **symptom-treater**, still one big file. D — **overbuild**, doesn't address attention budget.

### 8. (SBA · components) `.claude/skills/<name>/SKILL.md` and `.claude/commands/<name>.md` are:
A. the same file in two places  B. two authoring surfaces for the same slash-invocation mechanism — a Skill packages a process, a Command is a lighter prompt macro  C. Skills are deprecated  D. Commands only work in headless mode

> **Answer:** B.
> **Distractors:** A — different formats and locations. C/D — invented.
