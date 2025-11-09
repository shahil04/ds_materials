import os
import uuid
import requests
from flask import Flask, render_template, request, jsonify
from gtts import gTTS

# Optional translator fallback
try:
    from googletrans import Translator
    translator = Translator()
except Exception:
    translator = None

GEMINI_API_KEY = os.getenv("AIzaSyAjOrBi_CmhbMxwm8V1-g5oxeemoszVBIg")  # set this to use Gemini/Vertex
GEMINI_ENDPOINT = os.getenv("GEMINI_ENDPOINT",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-mini:generateText")

app = Flask(__name__, static_folder="static", template_folder="templates")

AUDIO_DIR = os.path.join(app.static_folder, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

def call_gemini_text(prompt, max_tokens=512):
    if not GEMINI_API_KEY:
        raise RuntimeError("Gemini API key not set")
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"}
    payload = {"prompt": prompt, "maxOutputTokens": max_tokens}
    resp = requests.post(GEMINI_ENDPOINT, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict):
        if "candidates" in data and data["candidates"]:
            return data["candidates"][0].get("content", {}).get("text", "") or data["candidates"][0].get("content", "")
        if "output" in data and isinstance(data["output"], dict):
            return data["output"].get("text", "") or data.get("response", "")
    return str(data)

def translate_with_gemini(text, target_lang, source_lang=None):
    prompt = f"Translate to {target_lang} from {source_lang or 'auto'}:\\n\\n{text}\\n\\nOnly output the translated text."
    return call_gemini_text(prompt)

def chat_with_gemini(history, user_message):
    prompt = "You are a helpful assistant for medical conversations (non-diagnostic). Keep answers concise.\n\nConversation:\n"
    for h in history:
        prompt += f"{h.get('role', 'user')}: {h.get('content')}\n"
    prompt += f"user: {user_message}\nassistant:"
    return call_gemini_text(prompt)

def translate_fallback(text, target_lang, source_lang=None):
    if translator:
        try:
            res = translator.translate(text, dest=target_lang, src=source_lang or 'auto')
            return res.text
        except Exception as e:
            print("googletrans error:", e)
    return text

def make_tts(text, lang_code='en'):
    lang_short = lang_code.split('-')[0] if isinstance(lang_code, str) else 'en'
    filename = f"tts_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)
    try:
        tts = gTTS(text=text, lang=lang_short)
        tts.save(filepath)
        return f"/static/audio/{filename}"
    except Exception as e:
        print("gTTS error:", e)
        return None


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

@app.route("/api/translate_text", methods=["POST"])
def api_translate_text():
    data = request.get_json(force=True)
    text = data.get("text", "").strip()
    target = data.get("target_lang", "hi")
    source = data.get("source_lang", None)
    if not text:
        return jsonify({"error":"no text provided"}), 400
    translated = None
    if GEMINI_API_KEY:
        try:
            translated = translate_with_gemini(text, target, source)
        except Exception as e:
            print("Gemini translate failed:", e)
            translated = None
    if not translated:
        translated = translate_fallback(text, target, source)
    audio_url = make_tts(translated, target) or None
    return jsonify({"translated": translated, "audio_url": audio_url})

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(force=True)
    message = data.get("message", "").strip()
    history = data.get("history", [])
    if not message:
        return jsonify({"error":"no message"}), 400
    reply = None
    if GEMINI_API_KEY:
        try:
            reply = chat_with_gemini(history, message)
        except Exception as e:
            print("Gemini chat failed:", e)
            reply = None
    if not reply:
        if translator:
            try:
                tr = translator.translate(message, dest='en')
                reply = "Assistant (fallback): " + tr.text
            except Exception:
                reply = "Assistant (fallback): " + message
        else:
            reply = "Assistant (fallback): " + message
    audio_url = make_tts(reply, 'en') or None
    return jsonify({"reply": reply, "audio_url": audio_url})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
