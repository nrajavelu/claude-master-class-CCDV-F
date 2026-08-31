"""
Aizentify CDF Bootcamp — environment doctor.

Run from the `aizentify-cdf-bootcamp/` folder, with your virtualenv active:

    python day0-prework/check_env.py

It checks, in order:
  1. Python >= 3.11
  2. a virtualenv is active
  3. the required packages import
  4. a .env file exists and ANTHROPIC_API_KEY is set
  5. the Claude API is reachable (a real 1-token call)

Exit code 0 = ready for Day 1. Non-zero = fix the first FAIL and re-run.
Nothing here costs more than a fraction of a cent.
"""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

GREEN = "\033[92m"
RED = "\033[91m"
YEL = "\033[93m"
DIM = "\033[2m"
END = "\033[0m"

FAILURES: list[str] = []


def ok(msg: str) -> None:
    print(f"  {GREEN}[OK]{END}   {msg}")


def fail(msg: str, hint: str) -> None:
    print(f"  {RED}[FAIL]{END} {msg}")
    print(f"         {DIM}fix:{END} {hint}")
    FAILURES.append(msg)


def warn(msg: str) -> None:
    print(f"  {YEL}[warn]{END} {msg}")


def check_python() -> None:
    v = sys.version_info
    if (v.major, v.minor) >= (3, 11):
        ok(f"Python {v.major}.{v.minor}.{v.micro}  (>= 3.11)")
    else:
        fail(
            f"Python {v.major}.{v.minor}.{v.micro} is too old (need >= 3.11)",
            "install Python 3.11+ (see logistics/00-environment-setup.md) and recreate the venv",
        )


def check_venv() -> None:
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    if in_venv:
        ok(f"virtualenv active: {sys.prefix}")
    else:
        fail(
            "no virtualenv active (packages would install globally)",
            "python -m venv .venv  &&  source .venv/bin/activate"
            "  (Windows: .venv\\Scripts\\activate)  then  pip install -r requirements.txt",
        )


def check_packages() -> None:
    # import name -> pip name
    required = {"anthropic": "anthropic", "claude_agent_sdk": "claude-agent-sdk", "dotenv": "python-dotenv"}
    for import_name, pip_name in required.items():
        try:
            mod = importlib.import_module(import_name)
            version = getattr(mod, "__version__", "present")
            ok(f"package '{import_name}'  {version}")
        except Exception:  # noqa: BLE001 - we want any import failure
            fail(
                f"package '{import_name}' not importable",
                f"pip install -r requirements.txt   (missing: {pip_name})",
            )


def find_dotenv() -> Path | None:
    """Look for .env in the bootcamp root (this file's grandparent) and cwd."""
    candidates = [
        Path(__file__).resolve().parent.parent / ".env",
        Path.cwd() / ".env",
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def check_key() -> str | None:
    try:
        from dotenv import load_dotenv
    except Exception:  # noqa: BLE001
        warn("python-dotenv missing; relying on a pre-exported ANTHROPIC_API_KEY")
        load_dotenv = None  # type: ignore[assignment]

    env_path = find_dotenv()
    if load_dotenv is not None and env_path is not None:
        load_dotenv(env_path)

    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        where = f"found {env_path}" if env_path else "no .env file found"
        fail(
            f".env / ANTHROPIC_API_KEY not set  ({where})",
            "create aizentify-cdf-bootcamp/.env containing:  ANTHROPIC_API_KEY=sk-ant-...",
        )
        return None

    if not key.startswith("sk-ant-"):
        warn(f"ANTHROPIC_API_KEY is set but does not look like a key ({key[:6]}…)")
    tail = key[-4:] if len(key) >= 4 else "????"
    src = str(env_path) if env_path else "environment"
    ok(f".env / key set from {src}  (sk-ant-…{tail})")
    return key


def check_api(key: str) -> None:
    try:
        import anthropic
    except Exception:  # noqa: BLE001
        fail("cannot import anthropic to test the API", "pip install -r requirements.txt")
        return

    model = "claude-haiku-4-5"  # cheapest tier; bootcamp labs pin to this / sonnet-5
    try:
        client = anthropic.Anthropic(api_key=key)
        resp = client.messages.create(
            model=model,
            max_tokens=1,
            messages=[{"role": "user", "content": "ping"}],
        )
        _ = resp.usage.input_tokens
        ok(f"API reachable — 1-token call succeeded  (model: {model})")
    except anthropic.AuthenticationError:
        fail(
            "API rejected the key (401 AuthenticationError)",
            "confirm the key and that your Console workspace has credit — ask your coordinator",
        )
    except anthropic.NotFoundError:
        fail(
            f"model '{model}' not available to this key (404)",
            "your key may be scoped to a different model set — tell your coordinator",
        )
    except anthropic.RateLimitError:
        fail(
            "rate limited on the very first call (429)",
            "you are probably on a shared key — you need your own; tell your coordinator",
        )
    except anthropic.APIConnectionError as e:
        fail(
            f"could not reach api.anthropic.com ({e.__class__.__name__})",
            "corporate proxy / firewall — see the network section of logistics/01-procurement-guide.md",
        )
    except Exception as e:  # noqa: BLE001
        fail(f"unexpected API error: {e.__class__.__name__}: {e}", "capture this text and send it to your coordinator")


def main() -> int:
    print(f"\n{GREEN}Aizentify CDF{END} — environment check\n")
    check_python()
    check_venv()
    check_packages()
    key = check_key()
    if key:
        check_api(key)

    print()
    if FAILURES:
        print(f"{RED}{len(FAILURES)} check(s) failed.{END} Fix the first one, then re-run this script.\n")
        return 1
    print(f"{GREEN}All checks passed. You are ready for Day 1.{END}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
