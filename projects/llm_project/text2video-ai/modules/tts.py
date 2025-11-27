import pyttsx3

def text_to_audio(text, output_path="assets/temp/audio.wav"):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    return output_path
