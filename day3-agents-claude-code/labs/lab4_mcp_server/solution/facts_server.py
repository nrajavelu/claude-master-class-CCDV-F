"""Day 3 · Lab 4 — a FastMCP stdio server (SOLUTION).

    cd aizentify-cdf-bootcamp
    python day3-agents-claude-code/labs/lab4_mcp_server/solution/facts_server.py \\
        < day3-agents-claude-code/labs/lab4_mcp_server/mcp_test_input.jsonl

Smoke test needs no API key and no agent — MCP is JSON-RPC over stdio.
"""
import pathlib
import sys

from mcp.server.fastmcp import FastMCP

sys.stdout.reconfigure(line_buffering=True)

mcp = FastMCP("facts")

_MARKERS = ("# TODO", "# FIXME")


@mcp.tool()
def count_todos(directory: str) -> str:
    """Count '# TODO' and '# FIXME' comment lines across .py files under `directory`.

    Args:
        directory: path to scan, relative to the current working directory.
    Returns:
        a one-line summary: how many files, how many TODO/FIXME lines.
    """
    root = pathlib.Path(directory)
    files = sorted(root.rglob("*.py"))
    hits = 0
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        hits += sum(1 for line in text.splitlines() if any(m in line for m in _MARKERS))
    return f"{len(files)} file(s), {hits} TODO/FIXME line(s)"


if __name__ == "__main__":
    mcp.run()
