import os

API_KEY = "sk-ant-REPLACE-ME-not-a-real-key-000000000000"


def build_client(timeout=30):
    """Return a config dict for the HTTP client."""
    return {"key": API_KEY, "timeout": timeout, "base": os.environ.get("BASE_URL", "")}
