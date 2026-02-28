from moviepy.editor import VideoFileClip, AudioFileClip

def merge_audio_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    final = video.set_audio(audio)
    final.write_videofile(output_path)
