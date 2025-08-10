import os
import whisper

def generate_subtitles(topic):
    audio_dir=f'output/{topic}/audio'
    subtitle_dir=f'output/{topic}/subtitles'
    os.makedirs(subtitle_dir, exist_ok=True)
    model = whisper.load_model("base")  # You can use 'tiny' for faster performance

    audio_files = sorted([f for f in os.listdir(audio_dir) if f.endswith('.wav')])
    print("🔍 Found audio files:", audio_files)

    if not audio_files:
        print("⚠️ No .wav files found in", audio_dir)
        return

    for audio_file in audio_files:
        audio_path = os.path.join(audio_dir, audio_file)
        print(f"⏳ Transcribing {audio_path}...")

        result = model.transcribe(audio_path)

        slide_id = os.path.splitext(audio_file)[0]
        srt_path = os.path.join(subtitle_dir, f"{slide_id}.srt")

        with open(srt_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"]):
                f.write(f"{i + 1}\n")
                f.write(f"{format_time(segment['start'])} --> {format_time(segment['end'])}\n")
                f.write(f"{segment['text'].strip()}\n\n")

        print(f"✅ Subtitle saved: {srt_path}")

def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

if __name__ == "__main__":
    generate_subtitles()
