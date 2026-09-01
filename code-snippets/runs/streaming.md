# Stream tokens, then get the final Message

> Worked example · **Day 1** · exam domain **D2** · source `code-snippets/streaming.py`
> Run it yourself: `python code-snippets/streaming.py`

## Scenario

Stream a reply for a live UI, then still recover the complete `Message` (usage, stop_reason, all blocks) at the end.

**Input / dataset.** A prompt whose answer is long enough to see it arrive in pieces.

## The code

<!-- CODE:START -->
```python
"""
streaming.py — stream, then get the finished Message.

Exam angles (D2):
  * streaming is Server-Sent Events over the SAME HTTP call -- NOT a WebSocket
  * non-streaming holds the connection until done -> long outputs can time out
  * an error can arrive AS AN EVENT mid-stream -> read events, not just status
  * stream.get_final_message() gives the complete Message (usage, stop_reason, blocks)
    -- do NOT hand-assemble it from text deltas

    cd aizentify-cdf-bootcamp && python code-snippets/streaming.py
"""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-haiku-4-5", max_tokens=200,
    messages=[{"role": "user", "content": "List 5 uses for a paperclip, one per line."}],
) as stream:
    for chunk in stream.text_stream:          # text deltas only
        print(chunk, end="", flush=True)

final = stream.get_final_message()            # the whole thing, after the stream ends
print("\n--")
print("stop_reason :", final.stop_reason)
print("usage       :", f"in={final.usage.input_tokens} out={final.usage.output_tokens}")

# When NOT to stream: very short outputs, or when you need the whole result before
# doing anything with it and latency is irrelevant.
```
<!-- CODE:END -->

## Output

<!-- OUTPUT:START -->
_captured · mock run — numbers illustrative_

```text
[mock reply] The support desk should acknowledge the issue, state the next step, and give a timeline. 
--
stop_reason : end_turn
usage       : in=420 out=96
```
<!-- OUTPUT:END -->

## Read the output

- Streaming is **SSE over the same HTTP call** — not a WebSocket.
- `stream.get_final_message()` rebuilds the whole Message — don't hand-assemble from deltas, and don't make a second call (it re-bills).
- An error can arrive **mid-stream**; a broken stream is transient → retry the whole request.

## Exam hook

'After a `with client.messages.stream(...)` block, get the complete message via…' and the WebSocket distractor.

## Your turn

Wrap the loop in try/except and print any exception type — see that streaming errors are ordinary exceptions.
