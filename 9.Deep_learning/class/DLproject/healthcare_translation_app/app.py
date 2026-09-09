import os
import uuid
import base64
import json
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from gtts import gTTS

# Optional translation: use googletrans as a fallback if GEMINI not configured
try:
    from googletrans import Translator
    translator_fallback = Translator()
except Exception:
    translator_fallback = None

# Optional Gemini function (requires GEMINI_API_KEY to be set in env)
import requests

GEMINI_API_KEY = os.getenv("AIzaSyAjOrBi_CmhbMxwm8V1-g5oxeemoszVBIg")  # set this in your deployment env to use Gemini
GEMINI_ENDPOINT = os.getenv("GEMINI_ENDPOINT", "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-mini:generateText")

app = Flask(__name__)
CORS(app)

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "static", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

def translate_with_gemini(text, target_lang, source_lang=None):
    """
    Calls Gemini text generation for translation if GEMINI_API_KEY is present.
    This uses a simple prompt to ask Gemini to translate. Requires proper API credentials.
    """
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set")

    prompt = f"Translate the following text to {target_lang} from {source_lang or 'the input language'}.\n\nText:\n{text}\n\nReturn only the translated text."
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_API_KEY}"
    }
    payload = {
        "prompt": prompt,
        "maxOutputTokens": 1024,
    }
    # NOTE: The exact Gemini REST shape may vary; adapt to your API/SDK as needed.
    resp = requests.post(GEMINI_ENDPOINT, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # best-effort extraction depending on response shape
    if "candidates" in data and isinstance(data["candidates"], list) and data["candidates"]:
        return data["candidates"][0].get("content", {}).get("text", "").strip()
    # fallback shapes
    return data.get("output", {}).get("text", "").strip() or data.get("response", "").strip() or ""

def translate_fallback(text, target_lang, source_lang=None):
    if translator_fallback:
        try:
            # googletrans uses language codes like 'hi', 'en', etc.
            res = translator_fallback.translate(text, dest=target_lang, src=source_lang or "auto")
            return res.text
        except Exception as e:
            print("googletrans failed:", e)
    # last resort: return original text
    return text

@app.route("/api/translate_text", methods=["POST"])
def translate_text():
    """
    Receives JSON: { text: str, source_lang: 'en'|'hi'|..., target_lang: 'hi'|... }
    Returns JSON: { translated: str, audio_url: '/static/audio/xxx.mp3' }
    """
    body = request.get_json(force=True)
    text = body.get("text", "").strip()
    target_lang = body.get("target_lang", "hi")
    source_lang = body.get("source_lang", None)

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Attempt Gemini if API key is set; otherwise fallback to googletrans
    translated = None
    if GEMINI_API_KEY:
        try:
            translated = translate_with_gemini(text, target_lang, source_lang)
        except Exception as e:
            print("Gemini translate failed:", e)
            translated = None

    if not translated:
        translated = translate_fallback(text, target_lang, source_lang)

    # TTS using gTTS (no external paid API required). gTTS supports many languages by code.
    try:
        tts = gTTS(text=translated, lang=target_lang.split("-")[0])
        filename = f"tts_{uuid.uuid4().hex}.mp3"
        path = os.path.join(AUDIO_DIR, filename)
        tts.save(path)
        audio_url = f"/static/audio/{filename}"
    except Exception as e:
        print("gTTS failed:", e)
        audio_url = None

    return jsonify({"translated": translated, "audio_url": audio_url})

# Static audio serving is handled by Flask's static route (/static/...)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
