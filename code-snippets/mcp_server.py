"""
mcp_server.py — a minimal MCP server over stdio, with FastMCP.

Exam angles (D8 · Tools & MCPs):
  * MCP is a PROTOCOL, not a library -- Claude Code, Desktop, Cursor all speak it
  * a stdio server is just a program: a command + args in .mcp.json
  * "an MCP server is not a bag of tools" -- scope allowed_tools to what you need
  * secrets via ${ENV_VAR} expansion in the config, never hardcoded

Needs the mcp SDK:  pip install "mcp>=1.2.0"

Smoke-test it without any agent (proves it's just JSON-RPC over stdio):

    printf '%s\n' \\
      '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"t","version":"0"}}}' \\
      '{"jsonrpc":"2.0","method":"notifications/initialized"}' \\
      '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \\
      '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"add","arguments":{"a":2,"b":3}}}' \\
    | python code-snippets/mcp_server.py
"""
import sys
from mcp.server.fastmcp import FastMCP

# stdio must be line-buffered or responses can sit in the buffer forever
sys.stdout.reconfigure(line_buffering=True)

mcp = FastMCP("demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b


if __name__ == "__main__":
    mcp.run()   # stdio by default -- matches "type": "stdio" in .mcp.json
