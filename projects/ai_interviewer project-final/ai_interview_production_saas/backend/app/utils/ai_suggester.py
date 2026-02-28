import os
import time
import google.generativeai as genai
import google.api_core.exceptions
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load .env from backend/app/.env (where user is editing) AND backend/.env
current_file_path = Path(__file__).resolve()
app_env_path = current_file_path.parent.parent / ".env" 
root_env_path = current_file_path.parent.parent.parent / ".env"

if app_env_path.exists():
    load_dotenv(dotenv_path=app_env_path, override=True)
elif root_env_path.exists():
    load_dotenv(dotenv_path=root_env_path, override=True)
else:
    load_dotenv(override=True)

api_key = os.getenv("GOOGLE_GENAI_API_KEY")
if not api_key:
    print("CRITICAL WARNING: GOOGLE_GENAI_API_KEY not found in ai_suggester!")
else:
    print(f"Loaded key in ai_suggester: {api_key[:4]}...{api_key[-4:]}")

genai.configure(api_key=api_key)

def safe_generate_content(model, prompt):
    retry_delay = 30
    while True:
        try:
            return model.generate_content(prompt)
        except google.api_core.exceptions.ResourceExhausted:
            print(f"Quota reached. Sleeping for {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 1.5 
        except Exception as e:
            print(f"Error during generation: {e}")
            return None

def get_ai_advice(info: dict) -> str:
    prompt = f"""
    I'm sharing the following resume information:

    Skills:
    {', '.join(info.get('skills', []))}

    Entities / Experience:
    {', '.join(info.get('entities', []))}

    Based on the above, give me AI-generated career suggestions.
    """
    
    model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
    response = safe_generate_content(model, prompt)
    
    if response:
        return response.text
    return "Error: Could not retrieve AI suggestions."
