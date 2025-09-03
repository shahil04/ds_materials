Voice & Chat Translator - Prototype

Overview:
- Voice Mode: Use your browser (Chrome) to speak. Browser handles speech-to-text (Web Speech API). Final segments are sent to server for translation + TTS playback.
- Chat Mode: Type messages to an assistant. Server will call Gemini if GEMINI_API_KEY is set, otherwise a simple fallback is used. Replies are returned with TTS audio.

Setup:
1. Python 3.9/3.10 recommended.
2. Create venv and activate it.
3. pip install -r requirements.txt
4. (Optional) Export GEMINI_API_KEY in your environment to enable Gemini features.
   - NEVER expose API keys publicly. Revoke any key pasted into chat.
5. python app.py
6. Open http://localhost:5000 in Chrome.

Files:
- app.py: Flask backend
- templates/index.html: UI combining voice and chat
- templates/chat.html: chat-only page
- static/js/main.js: client JS
- static/css/style.css
- static/audio/: generated audio files

Notes:
- This is a prototype. For production with PHI, ensure HIPAA compliance, BAAs, encrypted storage, and avoid sending PHI to third-party APIs without agreements.
- Autoplay may be blocked by browsers until a user gesture is made. The UI attempts playback and also provides Play buttons.
