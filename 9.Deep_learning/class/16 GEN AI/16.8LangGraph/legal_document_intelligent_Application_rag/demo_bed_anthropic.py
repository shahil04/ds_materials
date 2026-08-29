import os
import anthropic
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
base_url = os.getenv("ANTHROPIC_BASE_URL")
workspace_id = os.getenv("ANTHROPIC_WORKSPACE_ID")

print("API key loaded:", bool(api_key))
print("Base URL:", base_url)
print("Workspace ID:", workspace_id)

if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in .env")

client = anthropic.Anthropic(
    api_key=api_key,
    base_url=base_url,
    default_headers={
        "anthropic-workspace-id": workspace_id
    },
)

with client.messages.stream(
    model="anthropic.claude-haiku-4-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Summarize this document..."
        }
    ],
) as stream:

    for text in stream.text_stream:
        print(text, end="", flush=True)

print()
