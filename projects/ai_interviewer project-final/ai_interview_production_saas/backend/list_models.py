import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path

# Robust loading logic
current_file_path = Path(__file__).resolve()
app_env_path = current_file_path.parent / "app" / ".env"
root_env_path = current_file_path.parent / ".env"

if app_env_path.exists():
    load_dotenv(dotenv_path=app_env_path, override=True)
elif root_env_path.exists():
    load_dotenv(dotenv_path=root_env_path, override=True)
else:
    load_dotenv(override=True)

api_key = os.getenv("GOOGLE_GENAI_API_KEY")

if not api_key:
    print("API Key not found in environment variables.")
else:
    genai.configure(api_key=api_key)
    print("Listing available models...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")
