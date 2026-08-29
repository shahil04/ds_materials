Done. I created the complete **FastMCP Math Server project** as a ZIP file.

📦 **[Download Math MCP Server ZIP](sandbox:/mnt/data/math-mcp-server.zip)**

It includes:

* `server.py` with 11 math MCP tools
* MCP Resource: `math://formulas`
* MCP Prompt: `solve_math_problem`
* `pyproject.toml` for `uv`
* Test file
* `README.md`
* `.gitignore`

Run after extracting:

```bash
uv sync
uv run math-mcp
```
