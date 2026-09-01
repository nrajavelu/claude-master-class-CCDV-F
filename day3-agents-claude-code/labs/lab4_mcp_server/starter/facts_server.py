"""Day 3 · Lab 4 — a FastMCP stdio server (STARTER). Fill the # TODO.

    cd aizentify-cdf-bootcamp
    python day3-agents-claude-code/labs/lab4_mcp_server/starter/facts_server.py \\
        < day3-agents-claude-code/labs/lab4_mcp_server/mcp_test_input.jsonl

Reference: code-snippets/mcp_server.py
"""
import pathlib
import sys

from mcp.server.fastmcp import FastMCP

# stdio MUST be line-buffered or JSON-RPC responses can sit in the buffer forever
sys.stdout.reconfigure(line_buffering=True)

mcp = FastMCP("facts")


@mcp.tool()
def count_todos(directory: str) -> str:
    """Count '# TODO' and '# FIXME' comment lines across .py files under `directory`.

    Args:
        directory: path to scan, relative to the current working directory.
    Returns:
        a one-line summary: how many files, how many TODO/FIXME lines.
    """
    root = pathlib.Path(directory)
    # TODO: iterate root.rglob("*.py"); for each, count lines containing "# TODO" or "# FIXME"
    # TODO: return f"{n_files} files, {n_hits} TODO/FIXME line(s)"
    raise NotImplementedError


if __name__ == "__main__":
    mcp.run()  # stdio by default — matches "type": "stdio" in .mcp.json
