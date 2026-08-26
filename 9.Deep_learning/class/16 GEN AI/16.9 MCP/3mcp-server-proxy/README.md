
# FastMCP Remote Proxy

This project exposes the tools from the remote FastMCP server through a local
proxy. The upstream server uses Streamable HTTP and requires OAuth authentication.

## Requirements

- Python 3.11 or newer
- `uv`

## Setup

```powershell
uv sync
```

To create the project from scratch instead:

```powershell
uv init
uv add fastmcp
```

## Run With Inspector

Start the local MCP Inspector with:

```powershell
uv run fastmcp dev main.py
```

The first run opens a browser for OAuth sign-in. Complete the login, then open
the Inspector at `http://127.0.0.1:6274` and refresh the connection.

FastMCP discovers the server through the standard `mcp` variable in `main.py`.
The entrypoint can also be specified explicitly:

```powershell
uv run fastmcp dev main.py:mcp
```

## Run As A Local Stdio Server

```powershell
uv run main.py
```

This starts the proxy over stdio for an MCP client such as Claude Desktop.

## Publish Changes

```powershell
git add .
git commit -m "Update FastMCP proxy"
git push
```

The upstream server is deployed through [FastMCP Cloud](https://horizon.prefect.io/).

