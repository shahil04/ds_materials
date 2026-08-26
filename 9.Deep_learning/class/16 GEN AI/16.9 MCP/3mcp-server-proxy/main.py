from fastmcp import Client, FastMCP

# Create a proxy to your remote FastMCP Cloud server
# FastMCP Cloud uses Streamable HTTP (default), so just use the /mcp URL
remote_client = Client(
    "https://mcp-demo01.fastmcp.app/mcp",
    auth="oauth",
)
mcp = FastMCP.as_proxy(remote_client, name="Shahil Server Proxy")

if __name__ == "__main__":
    mcp.run()

    