# Lab 2 · Stream the response

**Domain:** 1 — fundamentals (streaming)
**Time:** 25 min
**You will practise:** `client.messages.stream`, `stream.text_stream`,
`stream.get_final_message()`, and understanding *why* streaming is the default for anything
long.

---

## Goal

Take the Lab 1 explainer and make the explanation appear **token by token** as Claude writes
it, instead of all at once after a pause. Then still report `usage` at the end.

```
cd day1-foundations
python labs/lab2_streaming/starter/stream_explainer.py labs/lab1_explainer/sample.py
```

---

## Why this matters (say it before they code)

- A non-streaming call **holds the HTTP connection open** until the whole answer is done.
  For long outputs or big `max_tokens`, that can hit the SDK's request timeout and fail.
- Streaming returns tokens as they're generated → no timeout risk, and a UI that feels alive.
- The SDK gives you a helper: `stream.get_final_message()` reconstructs the complete
  `Message` (with `usage`, `stop_reason`, all blocks) **after** the stream ends. You do not
  hand-assemble it from events.

---

## Steps

1. Open `starter/stream_explainer.py`. Fill the `# TODO`s.
2. Replace the `messages.create(...)` call with a `with client.messages.stream(...) as
   stream:` block.
3. Loop over `stream.text_stream` and `print(chunk, end="", flush=True)`.
4. After the `with` block, call `stream.get_final_message()` and print its `usage` and
   `stop_reason`.

---

## Expected output

The explanation prints **progressively** (you can watch it type), then:

```
--- call stats ---
stop_reason: end_turn
usage:       input_tokens=181  output_tokens=112
```

---

## Checkpoints

- [ ] They used the `with ... as stream:` form (context manager), not a bare call.
- [ ] They got `usage` from `get_final_message()`, not by counting characters themselves.
- [ ] They can answer: *"When would you NOT stream?"* → very short outputs, or when you need
      the whole result before doing anything with it and latency doesn't matter.

## Common mistakes

| Symptom | Cause |
|---|---|
| Output still appears all at once | forgot `flush=True`, or iterating the wrong thing |
| `usage` is `None` | read it off the stream object mid-flight instead of `get_final_message()` |
| `TypeError: 'Stream' object is not ...` | called `.stream()` without `with` |

## Going further

- Print a `▍` cursor while streaming and erase it at the end.
- Add `--no-stream` to fall back to `messages.create` and compare the feel.
