# Day 4 — Applications & integration: requirements → design → lifecycle → RAG → eval

> **Status: outline + lab specs.** Full build in pass 2.
> **This is the day that makes the deck superior.** D2 is 33% of the exam and most prep
> courses only teach "API mechanics". This day owns the *rest* of D2 — requirements, design,
> lifecycle, configuration management — plus context engineering and evaluation.

**Primary CCDV-F domains:** D2 Applications & Integration (33.1% — Understanding Requirements,
Systems Life Cycle, Software Engineering Foundations, Application Design, Configuration
Management) · D6 Prompt & Context Engineering (Context Engineering) · D4 Eval, Testing &
Debugging (2.6%). **Decisions:** ④ *will it survive production?* and ③ *what does Claude see
and say?* **Anchor episodes:** `ep06` (memory/sessions/CLAUDE.md), `ep08` (skills).
**Video companion:** lessons 4, 6, 8 (and 9 for debugging).

---

## Learning objectives

1. Turn a business sentence into **requirements**, sorted into **functional** (what it does)
   and **infrastructure** (what it runs on / what the team must be able to do to it), derived
   from the ask + the solution architecture.
2. Place a system in the **systems life cycle** — *develop · implement · operate · maintain*
   — and know **"implement" means deploy where users are**, not write code; production credit
   is earned in operate + maintain.
3. Apply **software engineering foundations**: version control, code review, SDLC integration
   (branch → review → test → deploy), refactoring (small- and large-scale), REST/JSON, async.
4. Choose an **application design**: which surface, prompt assembly, output shape the
   consumer needs (prose for a human, schema for a dashboard), session hygiene (one session
   per task; `clear` / `compact` / `inspect`).
5. Do **configuration management**: pin the model version, commit the rules, project-config
   hierarchy, environment-specific config, secrets kept out of the repo — so three engineers
   on one repo get *the same* behaviour ("same repo, three different Claudes").
6. **Context engineering**: the window holds input + tools + output; a growing conversation
   is a growing request; compaction vs context-editing vs the memory tool; "a bigger window
   makes it worse" if you fill it with stale tool results.
7. Build a small **RAG** pipeline: chunk → embed → similarity search → assemble grounded
   prompt → cite; and know when RAG vs long-context vs fine-tune.
8. Build an **evaluation harness**: an eval set, exact-match vs structural assertions vs
   LLM-as-judge, regression tests in `pytest`, measuring a false-positive rate.

## Module plan (deck outline)

| # | Module | Domain / decision |
|---|---|---|
| 1 | The quarter that isn't about Claude — requirements: functional vs infrastructure | D2 · ④ |
| 2 | Systems life cycle — develop/implement/operate/maintain; who owns each | D2 · ④ |
| 3 | Software engineering foundations — VCS, review, pipeline, refactoring | D2 · ④ |
| 4 | Application design — surface, prompt assembly, output shape, session hygiene | D2 · ③ |
| 5 | Configuration management — version pinning, committed rules, config hierarchy, secrets | D2 · ③/④ |
| 6 | Context engineering — the window, compaction vs context-editing vs memory | D6 · ③ |
| 7 | RAG — chunk/embed/search/ground/cite; RAG vs long context vs fine-tune | D2/D6 · ③ |
| 8 | Evaluation — eval sets, judge types, regression tests, false-positive rate | D4 · ④ |
| — | recap + exam-style questions + quiz | |

## Lab specs

### Lab 1 · Requirements split  ·  25 min · D2 (paper + a little code)
- **Given:** a one-paragraph business brief for a "contract clause checker".
- **Do:** produce two lists — functional and infrastructure requirements — and a 5-box
  architecture sketch (what talks to what). Then tag each requirement the console-style app
  already meets vs doesn't.
- **Expected output:** ~6 functional + ~5 infrastructure items, correctly sorted; a written
  one-line diagnosis ("meets all functional, fails all infrastructure").

### Lab 2 · Make it reproducible  ·  35 min · D2 (Config Management)
- **Do:** take a small agent script whose behaviour depends on uncommitted local files. Add:
  a pinned model constant, a committed `CLAUDE.md`, a `config.toml` (or `.env.example`) for
  env-specific settings, and a `.gitignore` for secrets. Two people run it → same behaviour.
- **Expected output:** a checklist showing every behaviour-affecting input is now in version
  control or an example config; secrets are not.
- **Reference:** `ep06/` (CLAUDE.md discovery, `setting_sources`).

### Lab 3 · Tiny RAG with citations  ·  50 min · D2/D6
- **Do:** index ~15 short docs (provided): chunk (~500 tokens, overlap), embed (Voyage
  **or** local `sentence-transformers` — both paths in `starter/`), cosine top-k, assemble a
  grounded prompt with `<doc id=...>` tags, ask Claude to answer **and cite doc ids**.
  Ask one question whose answer isn't in the corpus → it should say so.
- **Expected output:** correct answer with the right doc id(s) cited; the out-of-corpus
  question returns "not in the provided documents".

### Lab 4 · Eval harness + regression test  ·  45 min · D4
- **Do:** write a 12-case eval set (input → expected properties) for Lab 3's RAG answerer.
  Implement three checks: structural assertion (cited ≥ 1 doc), keyword/contains, and an
  **LLM-as-judge** ("does the answer follow only from the cited docs? yes/no"). Wire it as
  `pytest`. Then introduce a regression (drop the citation instruction) and watch tests go
  red.
- **Expected output:** `pytest` green on the good version; ≥ 3 failures after the regression,
  each naming the case and the failed check.

## Exam-style question targets (≥ 22 — this is the heavy day)

functional vs infrastructure requirement sorting · "implement" = deploy · who owns
operate/maintain · SDLC route (branch→review→test→deploy) · refactoring scale ·
version-control enables rollback (mechanism vs "write a doc") · model version pinning ·
config hierarchy · secrets out of repo · context window contents · compaction vs
context-editing vs memory tool · one-session-per-task · RAG vs long-context vs fine-tune ·
chunk/overlap · grounding & citations · eval: structural assertion vs exact match vs judge ·
regression testing · false-positive rate.

## Quiz targets (12–15)

requirement type sort · lifecycle verbs · what belongs in version control · config hierarchy
order · window holds input+tools+output · compaction ≠ context-editing · RAG pipeline steps ·
"assert on structure, not wording" · what an LLM-judge is for.
