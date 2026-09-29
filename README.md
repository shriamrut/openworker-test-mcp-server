# OpenWorker Test MCP Server

A lightweight Python MCP (Model Context Protocol) server for testing OpenWorker Spring AI connectors (both Stdio and HTTP/SSE).

## Setup Virtual Environment

```bash
cd ~/Desktop/codes/openworker-test-mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running Modes

### 1. Stdio Mode (Process-based)
Used by `openworker-spring-ai` via `mcp-servers.json`:
```bash
python server.py --transport stdio
```

### 2. HTTP / SSE Mode (Web Server)
Run an HTTP/SSE server accessible by OpenWorker's `spring.ai.mcp.client.sse`:

**Option A (CLI):**
```bash
python server.py --transport sse --port 8000
```

**Option B (Uvicorn / FastAPI direct):**
```bash
uvicorn server:app --host 127.0.0.1 --port 8000
```

Endpoint URLs:
- SSE stream: `http://localhost:8000/sse`
- Message POST: `http://localhost:8000/messages`

## Connecting from OpenWorker Spring AI 
reference: https://github.com/shriamrut/openworker-spring

In `application.yml`:
```yaml
spring:
  ai:
    mcp:
      client:
        enabled: true
        type: SYNC
        sse:
          connections:
            python-mcp:
              url: http://localhost:8000/sse
```

## Available Tools
- `calculator_add(a: float, b: float) -> float`: Adds two numbers
- `get_current_time() -> str`: Returns ISO-8601 server timestamp
- `echo_message(message: str) -> str`: Echoes back a message
- `reverse_string(text: str) -> str`: Reverses the string
