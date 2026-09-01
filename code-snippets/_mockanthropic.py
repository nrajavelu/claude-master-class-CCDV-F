"""Offline stand-in for the `anthropic` SDK, used by tools/capture_runs.py --mock so the
worked-example pages can show a *real program run* without an API key or spend.

It is NOT a faithful model — replies are canned and deterministic. Numbers (usage, token
counts) are plausible, not real. Run `capture_runs.py --live` for genuine output.

Install BEFORE any `import anthropic`:
    import _mockanthropic; _mockanthropic.install()
"""
from __future__ import annotations

import sys
import types


# ---- exception hierarchy (mirrors the shape snippets catch) ------------------
class APIError(Exception):
    pass


class APIConnectionError(APIError):
    pass


class APIStatusError(APIError):
    def __init__(self, msg="server error", status_code=500):
        super().__init__(msg)
        self.status_code = status_code


class AuthenticationError(APIStatusError):
    def __init__(self, msg="invalid x-api-key"):
        super().__init__(msg, 401)


class BadRequestError(APIStatusError):
    def __init__(self, msg="bad request"):
        super().__init__(msg, 400)


class PermissionDeniedError(APIStatusError):
    def __init__(self, msg="forbidden"):
        super().__init__(msg, 403)


class NotFoundError(APIStatusError):
    def __init__(self, msg="not found"):
        super().__init__(msg, 404)


class RateLimitError(APIStatusError):
    def __init__(self, msg="rate limited"):
        super().__init__(msg, 429)


# ---- response objects -------------------------------------------------------
class _Block:
    def __init__(self, **kw):
        self.__dict__.update(kw)


class _Usage:
    def __init__(self, i=420, o=96, cw=0, cr=0):
        self.input_tokens = i
        self.output_tokens = o
        self.cache_creation_input_tokens = cw
        self.cache_read_input_tokens = cr

    def __repr__(self):
        return (f"Usage(input_tokens={self.input_tokens}, output_tokens={self.output_tokens}, "
                f"cache_creation_input_tokens={self.cache_creation_input_tokens}, "
                f"cache_read_input_tokens={self.cache_read_input_tokens})")


class _Message:
    def __init__(self, content, stop_reason="end_turn", usage=None, model="claude-haiku-4-5"):
        self.content = content
        self.stop_reason = stop_reason
        self.stop_sequence = None
        self.usage = usage or _Usage()
        self.model = model
        self.id = "msg_mock01"
        self.role = "assistant"
        self.type = "message"

    def model_dump(self):
        return {"id": self.id, "role": self.role, "stop_reason": self.stop_reason,
                "content": [b.__dict__ for b in self.content]}

    def model_dump_json(self, **_):
        import json
        return json.dumps(self.model_dump())


# ---- the canned "brain" ----------------------------------------------------
def _last_user_text(messages):
    for m in reversed(messages):
        if m.get("role") == "user":
            c = m["content"]
            if isinstance(c, str):
                return c
            return " ".join(b.get("text", "") for b in c if isinstance(b, dict))
    return ""


def _has_tool_result(messages):
    for m in messages:
        c = m.get("content")
        if isinstance(c, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
            return True
    return False


def _reply_blocks(messages, tools, thinking):
    text = _last_user_text(messages).lower()
    blocks = []
    if thinking:
        blocks.append(_Block(type="thinking",
                             thinking=("Let me reason about this step by step. The key is to "
                                       "track where each amount actually goes rather than adding "
                                       "unrelated numbers…"),
                             signature="mock-sig-AAAA"))
    if tools and not _has_tool_result(messages):
        t0 = tools[0]
        name = t0["name"] if isinstance(t0, dict) else getattr(t0, "name", "tool")
        blocks.append(_Block(type="tool_use", id="toolu_mock1", name=name,
                             input={"order_id": 10231} if "order" in name else {"a": 2, "b": 3}))
        return blocks, "tool_use"
    if "<selection>" in text or "classify" in text or "route" in text or "select the most" in text:
        blocks.append(_Block(type="text", text="<reasoning>billing keywords present</reasoning>\n"
                                               "<selection>billing</selection>"))
    elif "how many legs" in text:
        blocks.append(_Block(type="text", text="4"))
    elif "value: metric" in text or "markdown table" in text:
        blocks.append(_Block(type="text",
                             text="| Metric | Value |\n|:--|--:|\n| Customer satisfaction | 92% |"))
    elif "<response>" in text or "implement a stack" in text:
        blocks.append(_Block(type="text", text="<thoughts>use an aux min-stack</thoughts>\n"
                                               "<response>class MinStack: ...</response>"))
    elif "ping" in text:
        blocks.append(_Block(type="text", text="pong"))
    else:
        blocks.append(_Block(type="text",
                             text="[mock reply] The support desk should acknowledge the issue, "
                                  "state the next step, and give a timeline."))
    return blocks, "end_turn"


# ---- client --------------------------------------------------------------
class _Stream:
    def __init__(self, msg):
        self._msg = msg

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    @property
    def text_stream(self):
        for b in self._msg.content:
            if getattr(b, "type", "") == "text":
                for chunk in b.text.split(" "):
                    yield chunk + " "

    def get_final_message(self):
        return self._msg

    def __iter__(self):
        # a couple of representative SSE-ish events
        yield _Block(type="content_block_start", content_block=_Block(type="text"))
        for b in self._msg.content:
            if getattr(b, "type", "") == "text":
                yield _Block(type="content_block_delta", delta=_Block(text=b.text))
        yield _Block(type="message_stop")


class _Messages:
    def create(self, *, model="claude-haiku-4-5", messages=None, tools=None,
               thinking=None, max_tokens=1024, system=None, **kw):
        blocks, stop = _reply_blocks(messages or [], tools, thinking)
        cr = 380 if kw.get("_cache_hit") else 0
        return _Message(blocks, stop_reason=stop, usage=_Usage(cr=cr), model=model)

    def stream(self, **kw):
        return _Stream(self.create(**kw))

    def count_tokens(self, *, model=None, system=None, messages=None, tools=None, **kw):
        n = len(_last_user_text(messages or [])) // 4 + (60 if system else 0) + (120 if tools else 0)
        return _Block(input_tokens=max(n, 8))

    @property
    def batches(self):
        return _Batches()


class _Batches:
    _store = {}

    def create(self, *, requests):
        import time
        bid = "msgbatch_mock01"
        self._store[bid] = requests
        return _Block(id=bid, processing_status="ended",
                      request_counts=_Block(succeeded=len(requests), errored=0, processing=0))

    def retrieve(self, bid):
        return _Block(id=bid, processing_status="ended",
                      request_counts=_Block(succeeded=len(self._store.get(bid, [])), errored=0, processing=0))

    def results(self, bid):
        for r in self._store.get(bid, []):
            cid = r["custom_id"] if isinstance(r, dict) else r.custom_id
            yield _Block(custom_id=cid,
                         result=_Block(type="succeeded",
                                       message=_Message([_Block(type="text", text=f"[mock] {cid} -> positive")])))


class Anthropic:
    def __init__(self, api_key=None, max_retries=2, **kw):
        if api_key and "not-real" in str(api_key):
            self._bad = True
        else:
            self._bad = False
        self.messages = _Messages()

    def with_options(self, **kw):
        return self


class AsyncAnthropic(Anthropic):
    pass


def install():
    m = types.ModuleType("anthropic")
    for name in ("Anthropic", "AsyncAnthropic", "APIError", "APIStatusError", "APIConnectionError",
                 "AuthenticationError", "BadRequestError", "PermissionDeniedError",
                 "NotFoundError", "RateLimitError"):
        setattr(m, name, globals()[name])
    m.__version__ = "0.0.0-mock"
    sys.modules["anthropic"] = m
    # also stub python-dotenv so load_dotenv() is a no-op
    d = types.ModuleType("dotenv")
    d.load_dotenv = lambda *a, **k: False
    sys.modules.setdefault("dotenv", d)
