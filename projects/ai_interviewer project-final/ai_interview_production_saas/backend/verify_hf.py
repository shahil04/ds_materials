import os
from dotenv import load_dotenv
from pathlib import Path
from huggingface_hub import InferenceClient

# Robust .env loading
current_file_path = Path(__file__).resolve()
app_env_path = current_file_path.parent / "app" / ".env"
root_env_path = current_file_path.parent / ".env"

if app_env_path.exists():
    load_dotenv(dotenv_path=app_env_path, override=True)
elif root_env_path.exists():
    load_dotenv(dotenv_path=root_env_path, override=True)
else:
    load_dotenv(override=True)

token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not token:
    print("ERROR: HUGGINGFACEHUB_API_TOKEN not found in environment!")
    print(f"Please add it to {app_env_path} or {root_env_path}")
    exit(1)

print(f"Loaded Token: {token[:4]}...{token[-4:]}")

client = InferenceClient(api_key=token)

print("Testing connection with Mistral-7B-Instruct-v0.3...")
try:
    messages = [{"role": "user", "content": "Hello! Are you working?"}]
    response = client.chat_completion(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=messages,
        max_tokens=100
    )
    print("SUCCESS! Hugging Face API is working.")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print(f"FAILURE: Error calling Hugging Face API: {e}")
