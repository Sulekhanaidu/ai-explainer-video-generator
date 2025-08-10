import os
import re
from TTS.api import TTS
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def clean_text_for_tts(text):
    text = text.replace('—', ' - ').replace('–', '-')
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('‘', "'").replace('’', "'")
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def trim_silence(file_path, silence_thresh=-50, min_silence_len=300):
    audio = AudioSegment.from_file(file_path, format="wav")
    nonsilent = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    if nonsilent:
        start_trim = nonsilent[0][0]
        end_trim = nonsilent[-1][1]
        trimmed = audio[start_trim:end_trim]
        trimmed.export(file_path, format="wav")
    else:
        print(f"⚠️ Only silence in {file_path}, skipping trim.")

def generate_silent_audio(file_path, duration_ms=1000):
    silence = AudioSegment.silent(duration=duration_ms)
    silence.export(file_path, format="wav")
    print(f"🧘 Generated silent fallback audio at {file_path}")

def generate_tts(topic, slides):
    os.makedirs(f'output/{topic}/audio', exist_ok=True)
    tts = TTS(model_name='tts_models/en/ljspeech/glow-tts', progress_bar=False)

    for slide in slides:
        raw_text = slide['text']
        clean_text = clean_text_for_tts(raw_text)
        audio_path = f"output/{topic}/audio/slide_{slide['slide']}.wav"

        if len(clean_text) < 10:
            print(f"⚠️ Slide {slide['slide']} text too short — inserting silent audio.")
            generate_silent_audio(audio_path)
            continue

        try:
            tts.tts_to_file(text=clean_text, file_path=audio_path)
            trim_silence(audio_path)
            print(f"✅ Slide {slide['slide']} processed")
        except Exception as e:
            print(f"❌ TTS failed for slide {slide['slide']} — using silent fallback: {e}")
            generate_silent_audio(audio_path)
