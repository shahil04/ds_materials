# Healthcare Voice Translator (Prototype)

This prototype demonstrates a mobile-first web app that performs real-time-ish voice translation between English and Indian languages.
It uses the **browser's Web Speech API** for live speech-to-text (so use Chrome on desktop/mobile Chrome-based browsers), then sends text to the server for translation and TTS (audio playback).

## Features
- Live speech-to-text (client-side)
- Server-side translation (uses Gemini when `GEMINI_API_KEY` is set; otherwise falls back to `googletrans`)
- Server-side TTS using `gTTS` (no paid TTS required)
- Simple UI with language selection and playback

## Setup (local)

1. Clone or unzip project.
2. Create and activate a Python virtualenv.
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. (Optional) To use Gemini for translation, set `GEMINI_API_KEY` environment variable in your shell/hosting env.
   - If you set GEMINI_API_KEY, the server will attempt to call Gemini for translation. Make sure you have proper credentials.
   - **Do not** commit API keys or share them publicly. Revoke any key accidentally exposed.

5. Run the Flask app:
```bash
python app.py
```
6. Open `http://localhost:5000` in Chrome and test (allow microphone access).

## Notes / Limitations
- This prototype uses the **Web Speech API** for speech recognition; browser support is best in Chrome. Safari and Firefox have limited support.
- `googletrans` is an unofficial translator library and may have rate limits or occasional failures. For production, integrate Gemini/Vertex Translate or other paid translation APIs with a proper BAA if handling PHI.
- For TTS we use `gTTS` (free Google Text-to-Speech). For production, use a robust TTS (Gemini TTS, Google Cloud TTS) and ensure compliance for healthcare data.
- This app **does not** implement HIPAA-level protections. Do not use with real PHI without proper compliance (BAA, encrypted storage, access controls).

## Deployment
- Deploy backend to a provider like Render, Railway, or Google Cloud Run. Set environment variables in the host for `GEMINI_API_KEY` if needed.
- The frontend is served from Flask `templates/index.html` in this prototype for simplicity.

## Files
- `app.py` - Flask backend
- `templates/index.html` - Frontend UI (uses Web Speech API)
- `static/audio/` - Generated TTS audio files
- `requirements.txt` - Python dependencies

---
If you want, I can also:
- Add Dockerfile for containerized deployment
- Replace `gTTS` with Google Cloud TTS (requires OAuth/service account)
- Wire direct audio streaming (uploading recorded audio instead of using Web Speech API)
- Add speaker icons, redesign UI, or produce a short demo recording script
