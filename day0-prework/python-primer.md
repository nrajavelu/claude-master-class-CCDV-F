# Python primer — just enough to follow the labs

You already program in *some* language. This is a phrasebook that maps what you know onto the
Python you'll see this week. ~30 minutes. You do not need to memorise it — you need to
**recognise** every pattern when a lab uses it.

Everything below runs in a Python 3.11+ REPL (`python` then Enter) if you want to try it.

---

## 1. Virtual environments (the one bit of ceremony)

A **venv** is a private copy of Python + packages for one project, so installs don't collide.

```bash
python -m venv .venv                 # create it (once)
source .venv/bin/activate            # turn it on (every new terminal)   Windows: .venv\Scripts\activate
pip install -r requirements.txt      # install this project's packages into it
python some_script.py                # now runs with those packages
deactivate                           # turn it off
```

If a lab says `No module named anthropic`, 95% of the time your venv isn't activated.

---

## 2. Values and variables

```python
name = "Ada"              # str
count = 3                 # int
ratio = 0.75              # float
ok = True                 # bool  (also: False, None)
```

No `let` / `var` / `const` / type declarations. Indentation (4 spaces) defines blocks — no
braces, no semicolons.

---

## 3. The two collections you'll see constantly

### list — ordered, like an array
```python
models = ["haiku", "sonnet", "opus"]
models[0]            # "haiku"
models.append("fable")
len(models)          # 4
for m in models:
    print(m)
```

### dict — key/value, like a JSON object / hash map
```python
msg = {"role": "user", "content": "Hello"}
msg["role"]                    # "user"
msg.get("name")                # None  (no KeyError)
msg.get("name", "anon")        # "anon" (default)
msg["name"] = "Ada"            # add / overwrite
```

**The entire Claude API is dicts and lists.** A request is a list of message dicts; a
response has a `.content` that's a list of block objects. Get comfortable here.

---

## 4. Functions

```python
def greet(who, punctuation="!"):        # punctuation has a default
    return f"Hello, {who}{punctuation}"  # f-string: {expr} is interpolated

greet("Ada")                # "Hello, Ada!"
greet("Ada", punctuation=".")  # "Hello, Ada."  (keyword argument)
```

- `f"...{x}..."` — formatted string. `f"{cost:.4f}"` formats to 4 decimals.
- `return` with nothing (or falling off the end) returns `None`.

---

## 5. Conditionals and loops

```python
if response.stop_reason == "tool_use":
    handle_tools()
elif response.stop_reason == "end_turn":
    done()
else:
    print(f"unexpected: {response.stop_reason}")

for i, block in enumerate(response.content):   # enumerate → index + item
    print(i, block.type)

while True:                                    # the agentic loop is a while True
    ...
    if should_stop:
        break
```

---

## 6. List/dict comprehensions (compact transforms)

```python
names = [m.upper() for m in models]                       # ["HAIKU", "SONNET", ...]
texts = [b.text for b in response.content if b.type == "text"]   # filter + map
first_text = next((b.text for b in response.content if b.type == "text"), "")  # first match or ""
```

You'll see the `next((... for ... if ...), default)` idiom a lot for "pull the first text
block out of a response."

---

## 7. `with` blocks (automatic cleanup)

```python
with open("sample.py") as f:      # file is closed automatically at block end
    source = f.read()

with client.messages.stream(...) as stream:   # stream is closed automatically
    for event in stream:
        ...
```

---

## 8. `import`

```python
import anthropic                          # use as anthropic.Anthropic()
from anthropic import Anthropic           # use as Anthropic()
from dotenv import load_dotenv            # a specific name from a package
```

`load_dotenv()` reads a local `.env` file and puts its keys into the environment, so
`os.environ["ANTHROPIC_API_KEY"]` works without you exporting anything.

---

## 9. `async def` / `await` (Days 3–5)

The Claude **Agent SDK** is asynchronous. You'll see:

```python
import asyncio

async def main():
    async for message in query(prompt="...", options=opts):   # stream of messages
        print(message)

asyncio.run(main())      # this line actually runs the async function
```

Rules of thumb for this course:
- `async def` marks a function that must be `await`ed or iterated with `async for`.
- You call the top one via `asyncio.run(main())`.
- Inside an `async def`, `await some_async_call()` waits for it and gives you the result.
- You will mostly **pattern-match existing async code**, not write it from scratch.

---

## 10. Objects vs dicts (a gotcha)

- **You send dicts:** `{"role": "user", "content": "hi"}`.
- **You get back objects:** `response.content[0].text`, `response.stop_reason`,
  `response.usage.input_tokens` — dot access, not `["..."]`.
- To turn a response object back into something you can print as JSON:
  `response.model_dump()` or `response.to_dict()`.

---

## 11. Running things

```bash
python path/to/script.py            # run a file
python -m package.module            # run a module (labs use this form)
python                             # interactive REPL; Ctrl-D / exit() to leave
pytest                             # run tests (Day 4)
```

---

## 12. Errors you'll meet and what they mean

| Error | Meaning |
|---|---|
| `IndentationError` | your spacing is inconsistent — use 4 spaces, never tabs |
| `NameError: name 'x' is not defined` | typo, or used before assigned |
| `KeyError: 'foo'` | `d["foo"]` where `foo` isn't a key — use `d.get("foo")` |
| `AttributeError: 'dict' object has no attribute 'text'` | you used `.text` on a dict — it's `["text"]`, or you have a dict where you expected an object |
| `ModuleNotFoundError` | package not installed / venv not active |
| `TypeError: ... missing 1 required positional argument` | you left out a function argument |

---

## That's enough

If you can read the snippets above without panic, you can follow every lab. The Python you
don't know yet, you'll pick up by pattern-matching working code — which is most of Day 1
anyway.
