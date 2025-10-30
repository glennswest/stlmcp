#!/usr/bin/env python3
"""Minimal MCP server to test if Claude Code can connect"""

from mcp.server.fastmcp import FastMCP

# Create minimal server
mcp = FastMCP("Test Server")

@mcp.tool()
def test_hello(name: str) -> str:
    """
    Simple test tool that says hello.

    Args:
        name: Your name

    Returns:
        A greeting message
    """
    return f"Hello, {name}! The MCP server is working!"

if __name__ == "__main__":
    mcp.run()
