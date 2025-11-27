# def generate_video_from_text(script):
#     # TODO: Integrate AnimateDiff or ZeroScope here
#     print("🎨 Placeholder: Generating dummy video...")
#     dummy_video = "assets/temp/dummy_video.mp4"
    
#     # Generate a 5s blank video with moviepy for now
#     from moviepy.editor import ColorClip
#     clip = ColorClip(size=(720, 480), color=(0, 0, 0), duration=5)
#     clip.write_videofile(dummy_video, fps=24)
#     return dummy_video


from moviepy.editor import TextClip, CompositeVideoClip

def generate_video_from_text(script):
    print("📝 Generating video with text...")

    text_clip = TextClip(script, fontsize=24, color='white', size=(720, 480), method='caption', bg_color='black', align='center')
    text_clip = text_clip.set_duration(10)

    video = CompositeVideoClip([text_clip])
    output_path = "assets/temp/text_video.mp4"
    video.write_videofile(output_path, fps=24)

    return output_path
