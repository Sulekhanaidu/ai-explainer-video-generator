import os
import ffmpeg

def burn_subtitles(topic):
    input_video=f"output/{topic}/final_video.mp4"
    subtitle_file=f"output/{topic}/subtitles/final_subtitles.srt"
    output_video=f"output/{topic}/final_video_with_subs.mp4"
    if not os.path.exists(input_video):
        print(f"❌ Video not found: {input_video}")
        return
    if not os.path.exists(subtitle_file):
        print(f"❌ Subtitle file not found: {subtitle_file}")
        return

    print("🔥 Burning subtitles into video...")

    try:
        (
            ffmpeg
            .input(input_video)
            .output(output_video, vf=f"subtitles={subtitle_file}", vcodec="libx264", acodec="aac")
            .overwrite_output()
            .run()
        )
        print(f"✅ Subtitled video saved to: {output_video}")
    except ffmpeg.Error as e:
        print("❌ FFmpeg Error:\n", e.stderr.decode())

if __name__ == "__main__":
    burn_subtitles()