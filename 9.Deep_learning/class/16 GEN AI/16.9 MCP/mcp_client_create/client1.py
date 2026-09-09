import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
import json

load_dotenv()

# SERVERS = { 
#     "math": {
#         "transport": "stdio",
#         "command": "/Library/Frameworks/Python.framework/Versions/3.11/bin/uv",
#         "args": [
#             "run",
#             "fastmcp",
#             "run",
#             "/Users/nitish/Desktop/mcp-math-server/main.py"
#        ]
#     }
# }


SERVERS = { 
    "math": {
        "transport": "stdio",
        "command": "/Library/Frameworks/Python.framework/Versions/3.11/bin/uv",
        "args": [
            "run",
            "fastmcp",
            "run",
            "/Users/shahil/Desktop/mcp-math-server/main.py"
       ]
    }
}

async def main():
    
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()


    named_tools = {}
    for tool in tools:
        named_tools[tool.name] = tool

    print("Available tools:", named_tools.keys())

   

if __name__ == '__main__':
    asyncio.run(main())