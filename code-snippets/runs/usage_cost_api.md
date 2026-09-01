# Usage & cost from the Admin API

> Worked example · **Day 5** · exam domain **D5** · source `code-snippets/usage_cost_api.py`
> Run it yourself: `python code-snippets/usage_cost_api.py`

## Scenario

Query the organisation's token usage (`usage_report/messages`) and money (`cost_report`) for the last 7 days.

**Input / dataset.** An `sk-ant-admin-…` key and a date window.

## The code

<!-- CODE:START -->
```python
"""
usage_cost_api.py — read your org's token usage and cost from the Admin API.

Adapted from the Anthropic Claude Cookbooks (MIT):
  observability/usage_cost_api.ipynb · https://github.com/anthropics/claude-cookbooks

Exam angles (D5 · Cost & Token Management · Observability):
  * needs a separate ADMIN key (`sk-ant-admin...`), not your normal API key.
  * endpoints under https://api.anthropic.com/v1/organizations :
      usage_report/messages   — tokens: uncached input, cache-creation, cache-read, output
      cost_report             — money (minor units); bucket_width only "1d", <=31 days
  * `group_by[]=model` + pagination (`page`) to split by model.
  * this is how you answer "judge cost per completed task, not per request" with data.

    export ANTHROPIC_ADMIN_API_KEY=sk-ant-admin-...
    cd aizentify-cdf-bootcamp && python code-snippets/usage_cost_api.py
"""
import os
from datetime import datetime, time, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()
BASE = "https://api.anthropic.com/v1/organizations"


def _key() -> str:
    k = os.getenv("ANTHROPIC_ADMIN_API_KEY", "")
    if not k.startswith("sk-ant-admin"):
        raise SystemExit("Set ANTHROPIC_ADMIN_API_KEY (an sk-ant-admin-... key).")
    return k


def _get(endpoint: str, params: dict) -> dict:
    r = requests.get(f"{BASE}/{endpoint}", params=params, timeout=30, headers={
        "x-api-key": _key(), "anthropic-version": "2023-06-01",
        "content-type": "application/json"})
    r.raise_for_status()
    return r.json()


def _window(days_back: int) -> dict:
    end = datetime.combine(datetime.utcnow(), time.min)
    start = end - timedelta(days=days_back)
    return {"starting_at": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "ending_at": end.strftime("%Y-%m-%dT%H:%M:%SZ"), "bucket_width": "1d"}


def daily_usage(days_back: int = 7):
    data = _get("usage_report/messages", {**_window(days_back), "limit": days_back}).get("data", [])
    for bucket in data:
        u = ci = cr = o = 0
        for res in bucket.get("results", []):
            u += res.get("uncached_input_tokens", 0)
            ci += res.get("cache_creation_input_tokens", 0)
            cr += res.get("cache_read_input_tokens", 0)
            o += res.get("output_tokens", 0)
        print(f"{bucket['starting_at'][:10]}  in={u:>9}  cache_write={ci:>8}  cache_read={cr:>9}  out={o:>8}")


def daily_cost(days_back: int = 7):
    data = _get("cost_report", {**_window(days_back), "limit": min(days_back, 31)}).get("data", [])
    for bucket in data:
        cents = sum(float(r.get("amount", 0)) for r in bucket.get("results", []))
        print(f"{bucket['starting_at'][:10]}  ${cents / 100:.2f}")


if __name__ == "__main__":
    print("=== tokens / day ===")
    daily_usage()
    print("\n=== cost / day ===")
    daily_cost()
```
<!-- CODE:END -->

## Output

> This one needs a real key / extra dependency — capture with `--live`.

<!-- OUTPUT:START -->
_captured · mock run — numbers illustrative_

```text
[not run under --mock] needs an `sk-ant-admin-…` key + network — run with --live
```
<!-- OUTPUT:END -->

## Read the output

- Needs a separate **admin** key — not your normal API key.
- `cost_report` only supports `bucket_width: "1d"` and ≤ 31 days per request.
- `group_by[]=model` + `page` pagination to split by model — this is how you answer 'cost per task' with data.

## Exam hook

Observability / cost-management items; 'which key does the Admin API need'.

## Your turn

Add `"group_by[]": ["api_key"]` and see per-key spend — useful for a training cohort.
