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
