import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# Robust loading logic
current_file_path = Path(__file__).resolve()
app_env_path = current_file_path.parent / "app" / ".env"
root_env_path = current_file_path.parent / ".env"

print(f"Checking for .env at: {app_env_path}")
if app_env_path.exists():
    print("Found app .env, loading...")
    load_dotenv(dotenv_path=app_env_path, override=True)
elif root_env_path.exists():
    print("Found root .env, loading...")
    load_dotenv(dotenv_path=root_env_path, override=True)
else:
    print("No specific .env found, using default load_dotenv...")
    load_dotenv(override=True)

api_key = os.getenv("GOOGLE_GENAI_API_KEY")

if not api_key:
    print("ERROR: GOOGLE_GENAI_API_KEY not found!")
    exit(1)

print(f"Loaded Key: {api_key[:4]}...{api_key[-4:]}") # Masked print

genai.configure(api_key=api_key)

try:
    print("Attempting to generate content with Gemini...")
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content("Hello! Are you working?")
    print("SUCCESS! API Key is valid.")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"FAILURE: API Key check failed. Error: {e}")
