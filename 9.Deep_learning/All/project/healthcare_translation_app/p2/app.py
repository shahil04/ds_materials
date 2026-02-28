from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from gtts import gTTS
import uuid

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/audio'

# Configure Gemini API
genai.configure(api_key="AIzaSyAjOrBi_CmhbMxwm8V1-g5oxeemoszVBIg")

# Function to translate text using Gemini
def translate_text(text, source_lang, target_lang):
    prompt = f"Translate the following medical text from {source_lang} to {target_lang}: {text}"
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Function to convert text to speech and save audio
def text_to_speech(text, lang='hi'):
    tts = gTTS(text=text, lang=lang)
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    tts.save(filepath)
    return filepath

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    source_lang = data.get('source_lang')
    target_lang = data.get('target_lang')

    # Translate text
    translated_text = translate_text(text, source_lang, target_lang)

    # Generate speech for translated text
    audio_file = text_to_speech(translated_text, 'hi' if target_lang.lower() == 'hindi' else 'en')

    return jsonify({
        'original_text': text,
        'translated_text': translated_text,
        'audio_url': f"/{audio_file}"
    })

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
