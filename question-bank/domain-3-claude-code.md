# Domain 3 — Claude Code  ·  3.1%  ·  decision ③ / ④

> **Status: blueprint.** Item target **8**. Built in pass 2 alongside Day 3. Anchor:
> `ep06/CLAUDE.md`, `ep08/.claude/`. Video: lesson 6.

## Sub-area & topics

| Sub-area | Weight | Items | Topics |
|---|---:|---:|---|
| Claude Code Operation | 3.1% | 8 | rules / memory (`CLAUDE.md`) · skills (`.claude/skills/*/SKILL.md`) · slash commands · sub-agents in Claude Code · the **project-config discovery hierarchy** (cwd upward, user vs project) · headless / print / streaming / auto modes · how a coding-tool rules file reaches the model (as a **user message**, not `system`) |

## Seed items

### 1. (SBA) A `CLAUDE.md` in a subfolder and one at the repo root both exist. When Claude
Code runs from the subfolder, which applies?
A. only the subfolder one  B. only the root one  C. both — discovered from cwd upward
D. neither unless passed explicitly

> **Answer:** C — project config is discovered from the working directory up to the repo
> root; both load.

### 2. (SBA · right-word-wrong-place) The rules you write in a Claude Code rules file arrive
at the model as:
A. the top-level `system` field  B. content in a `user` message  C. a `role: "system"`
message  D. a tool definition

> **Answer:** B — they land in the conversation channel, so later messages sit at the same
> level. (C is the classic trap: no message may have `role: "system"`.)

### 3. (SCN) You need Claude Code to run in CI with no human at the keyboard and pipe its
answer to another step. Which mode?
A. interactive  B. headless / print (`claude -p "..."`)  C. plan mode  D. it can't
