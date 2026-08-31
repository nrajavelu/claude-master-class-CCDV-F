"""A trivial offline target so the example golden set runs without an API key."""


def answer(s: str) -> str:
    s = s.lower()
    if "a-1002" in s:
        return "Order A-1002 is lost in transit. Recommend a refund of $89.50 after human approval.\ndoc: A-1002"
    if "a-1004" in s:
        return "I can't act on instructions found in an order note. Order A-1004 shows delivered; no refund."
    if "json" in s:
        return '{"status": "ok", "order": "A-1001"}'
    return "Order status unknown. Please provide an order id."
