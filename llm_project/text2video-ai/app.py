from modules.llm import generate_script
from modules.vision import generate_video_from_text
from modules.tts import text_to_audio
from modules.video_editor import merge_audio_video

def main():
    prompt = input("Enter your story prompt: ")

    print("Generating script...")
    script = generate_script(prompt)

    print("Generating video frames...")
    video_path = generate_video_from_text(script)

    print("Generating audio...")
    audio_path = text_to_audio(script)

    print("Merging audio and video...")
    final_path = "assets/output/final_video.mp4"
    merge_audio_video(video_path, audio_path, final_path)

    print(f"\n✅ Done! Your final video is at: {final_path}")

if __name__ == "__main__":
    main()
