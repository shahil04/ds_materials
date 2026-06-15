# If you want a **full Math MCP Server** using **FastMCP**, here's a complete example with arithmetic, advanced math functions, validation, and a runnable server.

# math_server.py

from __future__ import annotations

from fastmcp import FastMCP
import math

# Create MCP Server
mcp = FastMCP("math-server")


def _as_number(x):
    """Convert input to float."""
    if isinstance(x, (int, float)):
        return float(x)

    if isinstance(x, str):
        try:
            return float(x.strip())
        except ValueError:
            pass

    raise TypeError(
        "Expected a number (int, float, or numeric string)"
    )


# -------------------------
# Basic Arithmetic
# -------------------------

@mcp.tool()
async def add(a: float, b: float) -> float:
    """Return a + b"""
    return _as_number(a) + _as_number(b)


@mcp.tool()
async def subtract(a: float, b: float) -> float:
    """Return a - b"""
    return _as_number(a) - _as_number(b)


@mcp.tool()
async def multiply(a: float, b: float) -> float:
    """Return a * b"""
    return _as_number(a) * _as_number(b)


@mcp.tool()
async def divide(a: float, b: float) -> float:
    """Return a / b"""
    b = _as_number(b)

    if b == 0:
        raise ValueError("Division by zero is not allowed")

    return _as_number(a) / b


@mcp.tool()
async def modulus(a: float, b: float) -> float:
    """Return a % b"""
    return _as_number(a) % _as_number(b)


@mcp.tool()
async def power(a: float, b: float) -> float:
    """Return a raised to power b"""
    return _as_number(a) ** _as_number(b)


# -------------------------
# Roots & Logs
# -------------------------

@mcp.tool()
async def sqrt(x: float) -> float:
    """Square root"""
    x = _as_number(x)

    if x < 0:
        raise ValueError("Cannot calculate square root of negative number")

    return math.sqrt(x)


@mcp.tool()
async def cube_root(x: float) -> float:
    """Cube root"""
    return _as_number(x) ** (1 / 3)


@mcp.tool()
async def log(x: float, base: float = math.e) -> float:
    """Logarithm"""
    x = _as_number(x)

    if x <= 0:
        raise ValueError("Log input must be positive")

    return math.log(x, _as_number(base))


# -------------------------
# Trigonometry
# -------------------------

@mcp.tool()
async def sin(angle_deg: float) -> float:
    """Sine of angle in degrees"""
    return math.sin(math.radians(_as_number(angle_deg)))


@mcp.tool()
async def cos(angle_deg: float) -> float:
    """Cosine of angle in degrees"""
    return math.cos(math.radians(_as_number(angle_deg)))


@mcp.tool()
async def tan(angle_deg: float) -> float:
    """Tangent of angle in degrees"""
    return math.tan(math.radians(_as_number(angle_deg)))


# -------------------------
# Statistics
# -------------------------

@mcp.tool()
async def average(numbers: list[float]) -> float:
    """Calculate average"""
    if not numbers:
        raise ValueError("List cannot be empty")

    nums = [_as_number(x) for x in numbers]
    return sum(nums) / len(nums)


@mcp.tool()
async def maximum(numbers: list[float]) -> float:
    """Find maximum number"""
    if not numbers:
        raise ValueError("List cannot be empty")

    return max(_as_number(x) for x in numbers)


@mcp.tool()
async def minimum(numbers: list[float]) -> float:
    """Find minimum number"""
    if not numbers:
        raise ValueError("List cannot be empty")

    return min(_as_number(x) for x in numbers)


# -------------------------
# Geometry
# -------------------------

@mcp.tool()
async def circle_area(radius: float) -> float:
    """Area of a circle"""
    r = _as_number(radius)

    if r < 0:
        raise ValueError("Radius cannot be negative")

    return math.pi * r * r


@mcp.tool()
async def rectangle_area(length: float, width: float) -> float:
    """Area of rectangle"""
    return _as_number(length) * _as_number(width)


@mcp.tool()
async def triangle_area(base: float, height: float) -> float:
    """Area of triangle"""
    return 0.5 * _as_number(base) * _as_number(height)


# -------------------------
# Constants
# -------------------------

@mcp.tool()
async def pi() -> float:
    """Return PI"""
    return math.pi


@mcp.tool()
async def e() -> float:
    """Return Euler's number"""
    return math.e


# -------------------------
# Run Server
# -------------------------

if __name__ == "__main__":
    mcp.run()


# ### Install

# ```bash
# pip install fastmcp
# ```

# ### Run

# ```bash
# python math_server.py
# ```

# ### Example MCP Tools

# Available tools:

# * add
# * subtract
# * multiply
# * divide
# * modulus
# * power
# * sqrt
# * cube_root
# * log
# * sin
# * cos
# * tan
# * average
# * maximum
# * minimum
# * circle_area
# * rectangle_area
# * triangle_area
# * pi
# * e

# This gives you a production-ready MCP math server that can be connected to MCP clients such as Claude Desktop, Cursor, Windsurf, VS Code MCP extensions, and other MCP-compatible agents.
