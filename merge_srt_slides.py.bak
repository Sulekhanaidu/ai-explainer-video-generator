import os
import re
import ffmpeg
from datetime import timedelta

def get_audio_duration(audio_path):
    try:
        probe = ffmpeg.probe(audio_path)
        return float(probe['format']['duration'])
    except Exception as e:
        print(f"❌ Failed to read duration for {audio_path}: {e}")
        return 0.0

def shift_timestamp(timestamp, offset_seconds):
    h, m, s_ms = timestamp.split(":")
    s, ms = s_ms.split(",")
    total = timedelta(hours=int(h), minutes=int(m), seconds=int(s), milliseconds=int(ms))
    shifted = total + timedelta(seconds=offset_seconds)
    return f"{shifted.seconds//3600:02}:{(shifted.seconds//60)%60:02}:{shifted.seconds%60:02},{int(shifted.microseconds/1000):03}"

def merge_srt_slides(topic):
    audio_dir=f"output/{topic}/audio"
    subtitle_dir=f"output/{topic}/subtitles"
    output_file=f"output/{topic}/subtitles/final_subtitles.srt"
    slide_files = sorted([f for f in os.listdir(subtitle_dir) if f.startswith("slide_") and f.endswith(".srt")])
    output_lines = []
    counter = 1
    current_offset = 0.0

    for slide_srt in slide_files:
        srt_path = os.path.join(subtitle_dir, slide_srt)
        audio_name = os.path.splitext(slide_srt)[0] + ".wav"
        audio_path = os.path.join(audio_dir, audio_name)
        duration = get_audio_duration(audio_path)

        with open(srt_path, "r", encoding="utf-8") as f:
            blocks = f.read().strip().split("\n\n")
            for block in blocks:
                lines = block.splitlines()
                if len(lines) >= 3:
                    # skip original index
                    time_line = lines[1]
                    text = lines[2:]

                    start, end = time_line.split(" --> ")
                    start_shifted = shift_timestamp(start, current_offset)
                    end_shifted = shift_timestamp(end, current_offset)

                    output_lines.append(f"{counter}")
                    output_lines.append(f"{start_shifted} --> {end_shifted}")
                    output_lines.extend(text)
                    output_lines.append("")
                    counter += 1

        current_offset += duration

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("\n".join(output_lines))

    print(f"✅ Final subtitle file saved: {output_file}")

if __name__ == "__main__":
    merge_srt_slides()
