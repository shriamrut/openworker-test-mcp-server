"""
OpenWorker Test MCP Server

Supports:
    - stdio
    - SSE
    - Streamable HTTP

Usage:

    python server.py
    python server.py --transport sse --port 8000
    python server.py --transport streamable-http --port 8000

For Uvicorn:

    uvicorn server:app --host 127.0.0.1 --port 8000
"""

import argparse
import datetime
import sys

try:
    # MCP 2.x
    from mcp.server import MCPServer

    print("Using MCP 2.x MCPServer", file=sys.stderr)

except ImportError:
    # MCP 1.x
    from mcp.server.fastmcp import FastMCP as MCPServer

    print("Using MCP 1.x FastMCP", file=sys.stderr)


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp = MCPServer("OpenWorkerTestServer")


@mcp.tool()
def calculator_add(a: float, b: float) -> float:
    """Add two numbers together."""
    print("MCP is called on ", a, "+", b)
    return a + b


@mcp.tool()
def get_current_time() -> str:
    """Get current server timestamp in ISO-8601 format."""
    return datetime.datetime.now().isoformat()


@mcp.tool()
def echo_back_message_from_mcp(message: str) -> str:
    """Echo back the provided message with prefix."""
    return f"Echo from Python MCP Server: {message}"


@mcp.tool()
def reverse_string(text: str) -> str:
    """Reverse a given string."""
    return text[::-1]

@mcp.tool()
def get_today_weather() -> str:
   """ Get today's weather."""
   return "Today is a SUNNY day"

# ---------------------------------------------------------------------------
# ASGI application
# ---------------------------------------------------------------------------
#
# Streamable HTTP is the preferred HTTP transport in current MCP.
#
# This allows:
#
#     uvicorn server:app --host 127.0.0.1 --port 8000
#
# MCP endpoint:
#
#     http://127.0.0.1:8000/mcp
#
# ---------------------------------------------------------------------------

app = mcp.streamable_http_app()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="OpenWorker Test MCP Server"
    )

    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport type",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="HTTP port",
    )

    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="HTTP host",
    )

    args = parser.parse_args()

    # -----------------------------------------------------------------------
    # stdio
    # -----------------------------------------------------------------------

    if args.transport == "stdio":
        mcp.run(transport="stdio")
        return

    # -----------------------------------------------------------------------
    # SSE
    # -----------------------------------------------------------------------

    if args.transport == "sse":
        print(
            f"Starting MCP server over SSE on "
            f"http://{args.host}:{args.port}/sse",
            file=sys.stderr,
        )

        mcp.run(
            transport="sse",
            host=args.host,
            port=args.port,
        )

        return

    # -----------------------------------------------------------------------
    # Streamable HTTP
    # -----------------------------------------------------------------------

    if args.transport == "streamable-http":
        print(
            f"Starting MCP server over Streamable HTTP on "
            f"http://{args.host}:{args.port}/mcp",
            file=sys.stderr,
        )

        mcp.run(
            transport="streamable-http",
            host=args.host,
            port=args.port,
        )

        return


if __name__ == "__main__":
    main()
