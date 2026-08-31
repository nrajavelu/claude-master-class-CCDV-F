# Environment setup — local PC / laptop

> **Audience:** every candidate, as part of Day 0 pre-work.
> **Goal:** `python day0-prework/check_env.py` prints all green, and
> `python day0-prework/labs/hello_claude.py` returns a sentence from Claude.
> **Time:** 45–90 minutes the first time. Do it at least **2 days before Day 1** so
> blockers can be fixed.

If anything here fails, **do not spend more than 20 minutes fighting it** — capture the exact
error text and send it to the training coordinator. Environment problems are common and
fixable, but not on the morning of Day 1.

---

## 0. What you will install

| Tool | Version | Why |
|---|---|---|
| **Python** | 3.11 or newer | every lab |
| **pip + venv** | bundled with Python | isolated dependencies |
| **Git** | any recent | clone the course repo, Day 3 |
| **VS Code** | latest | editor + integrated terminal |
| **Node.js** | 18 LTS or newer | Claude Code CLI (Days 3–5) |
| **Claude Code** | latest | `npm i -g @anthropic-ai/claude-code` |

And two accounts/keys from `01-procurement-guide.md`:

- `ANTHROPIC_API_KEY` — from your organisation's Console workspace.
- A **Claude Team** login for Claude Code (Days 3–5).
- *(optional)* `GITHUB_PAT`, `VOYAGE_API_KEY`.

---

## 1. Install Python 3.11+

### macOS
```bash
# Recommended: Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.12 git node
```
Or download from python.org and run the installer.

### Windows
- Install **Python** from python.org. **Tick "Add python.exe to PATH"** on the first screen.
- Install **Git for Windows** (git-scm.com) — accept defaults.
- Install **Node.js LTS** (nodejs.org) — accept defaults.
- *(Recommended)* Enable **WSL2** and do the whole course inside Ubuntu:
  `wsl --install` in an admin PowerShell, reboot, then follow the Linux steps.

### Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt install -y nodejs
```

### Verify
```bash
python3 --version     # 3.11.x or higher   (Windows: "python --version")
git --version
node --version        # v18+ 
```

---

## 2. Get the course materials

```bash
# your coordinator will give you the exact URL / zip
git clone <course-repo-url> claude-api-masterclass
cd claude-api-masterclass/aizentify-cdf-bootcamp
```

If you received a zip instead, unzip it and `cd` into
`claude-api-masterclass/aizentify-cdf-bootcamp`.

---

## 3. Create a virtual environment and install dependencies

From inside `aizentify-cdf-bootcamp/`:

```bash
python3 -m venv .venv

# activate it:
source .venv/bin/activate            # macOS / Linux / WSL
# .venv\Scripts\activate             # Windows PowerShell
# .venv\Scripts\activate.bat         # Windows cmd.exe

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Your prompt should now start with `(.venv)`. **You must activate the venv every time you
open a new terminal** for this course.

> **Day 4 RAG lab:** uncomment **one** of the two embedding lines at the bottom of
> `requirements.txt` (`voyageai` *or* `sentence-transformers`) per your coordinator's
> instruction, then `pip install -r requirements.txt` again.

---

## 4. Configure your API key

Create a file named `.env` in `aizentify-cdf-bootcamp/` (same folder as `requirements.txt`):

```
ANTHROPIC_API_KEY=sk-ant-...your-key-here...
# optional, added later in the week:
# GITHUB_PAT=github_pat_...
# VOYAGE_API_KEY=pa-...
```

- **Never commit `.env`.** A `.gitignore` in this folder already excludes it — leave that in
  place.
- Every lab loads this file with `python-dotenv`. You do **not** need to `export` anything.
- If you prefer an environment variable instead of a file, that works too:
  `export ANTHROPIC_API_KEY=sk-ant-...` (macOS/Linux) /
  `setx ANTHROPIC_API_KEY sk-ant-...` (Windows, new terminal after).

---

## 5. Install Claude Code (used from Day 3)

```bash
npm install -g @anthropic-ai/claude-code
claude --version
claude          # opens sign-in; use your Claude Team account
```

If `npm` complains about permissions on macOS/Linux, prefer a Node version manager
(`nvm`) over `sudo npm`.

---

## 6. Run the environment doctor

```bash
# from aizentify-cdf-bootcamp/, venv active
python day0-prework/check_env.py
```

Expected — **every line green / OK**:

```
Aizentify CDF — environment check
  [OK]   Python 3.12.2  (>= 3.11)
  [OK]   virtualenv active: .../aizentify-cdf-bootcamp/.venv
  [OK]   package 'anthropic'         1.x
  [OK]   package 'claude_agent_sdk'  0.2.x
  [OK]   package 'dotenv'            present
  [OK]   .env found, ANTHROPIC_API_KEY set (sk-ant-…abcd)
  [OK]   API reachable — 1-token ping succeeded  (model: claude-haiku-4-5)
All checks passed. You are ready for Day 1.
```

Then the first real call:

```bash
python day0-prework/labs/hello_claude.py
```

You should see a short reply from Claude and a `usage:` line with token counts.

---

## 7. Troubleshooting the common failures

| Symptom | Cause | Fix |
|---|---|---|
| `python: command not found` | Not on PATH (Windows: unticked the PATH box) | Reinstall Python with "Add to PATH", or use `py -3` / full path |
| `No module named anthropic` | venv not activated, or installed globally | `source .venv/bin/activate`, re-run `pip install -r requirements.txt` |
| `check_env.py` says "virtualenv NOT active" | new terminal without activation | activate the venv (step 3) |
| `AuthenticationError` / 401 on the ping | key missing, wrong, or has no credit | check `.env` spelling; confirm the key + workspace credit with the coordinator |
| `APIConnectionError` / SSL errors / hangs | corporate proxy or TLS inspection | see the network section of `01-procurement-guide.md`; set `HTTPS_PROXY` / `REQUESTS_CA_BUNDLE` per your org |
| `RateLimitError` (429) on the ping | shared key, or workspace limit hit | you should have your **own** key; tell the coordinator |
| `npm ERR! EACCES` | global npm needs root | install `nvm`, then `npm i -g @anthropic-ai/claude-code` |
| Slides show a plain system font | `fonts.googleapis.com` blocked | cosmetic only — ignore, or ask IT to allow-list it |

---

## 8. Day-0 "done" definition

You are ready for Day 1 when **all** of these are true:

- [ ] `python day0-prework/check_env.py` → *All checks passed.*
- [ ] `python day0-prework/labs/hello_claude.py` → a reply + a `usage:` line.
- [ ] `claude --version` prints a version (sign-in can wait until Day 3).
- [ ] You can open `day1-foundations/slides/day1.html` in a browser and press → to advance.
- [ ] You skimmed `day0-prework/python-primer.md` and nothing in it is a total mystery.
