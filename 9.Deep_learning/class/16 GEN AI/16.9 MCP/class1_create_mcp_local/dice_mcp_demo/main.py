from fastmcp import FastMCP
import random

# Create an instance of the MCP Server
mcp = FastMCP("Demo Server")

# Define an MCP Tool using the @mcp.tool decorator
@mcp.tool()
def roll_dice(num_dice: int = 1) -> str:
    """Rolls a specified number of 6-sided dice and returns the results."""
    rolls = [random.randint(1, 6) for _ in range(num_dice)]
    return f"You rolled: {', '.join(map(str, rolls))} (Total: {sum(rolls)})"

@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Adds two numbers and returns the sum."""
    return a + b

# Run the server
if __name__ == "__main__":
    mcp.run()


# uv run fastmcp dev inspector main.py
# For running the server directly without the Inspector:
# uv run fastmcp run main.py


# C:\Users\hp\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude
# uv run fastmcp install claude-desktop main.py --config-path "C:\Users\hp\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude"

