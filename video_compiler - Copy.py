import os
import ffmpeg

def compile_video(topic):
    slides_dir=f'output/{topic}/slides'
    audio_dir=f'output/{topic}/audio'
    output_file=f'output/{topic}/final_video.mp4'
    print("🎬 Starting video compilation...")

    os.makedirs(f'output/{topic}', exist_ok=True)

    # List image and audio files
    slide_files = sorted([f for f in os.listdir(slides_dir) if f.endswith('.png')])
    audio_files = sorted([f for f in os.listdir(audio_dir) if f.endswith('.mp3')])

    print(f"Found {len(slide_files)} slides and {len(audio_files)} audio files.")

    if len(slide_files) != len(audio_files):
        raise ValueError("Mismatch between number of slides and audio files")

    temp_dir = f'output/{topic}/temp'
    os.makedirs(temp_dir, exist_ok=True)

    segment_list = []
    for i, (img, aud) in enumerate(zip(slide_files, audio_files)):
        img_path = os.path.join(slides_dir, img)
        aud_path = os.path.join(audio_dir, aud)
        seg_path = os.path.join(temp_dir, f"segment_{i:02d}.mp4")

        print(f"🧩 Creating segment {i+1}: {img} + {aud}")

        # Combine image and audio into a video segment
        input_image = ffmpeg.input(img_path, loop=1)
        input_audio = ffmpeg.input(aud_path)

        (
            ffmpeg
            .output(input_image, input_audio, seg_path,
                    vcodec='libx264', acodec='aac',
                    shortest=None, pix_fmt='yuv420p')
            .overwrite_output()
            .run()
        )

        segment_list.append(seg_path)

    # Create concat list
    concat_file = os.path.join(temp_dir, "concat_list.txt")
    with open(concat_file, "w") as f:
        for seg in segment_list:
            f.write(f"file '{os.path.abspath(seg)}'\n")

    print("📦 Stitching all segments into one final video...")

    # Concatenate segments into one video
    (
        ffmpeg
        .input(concat_file, format='concat', safe=0)
        .output(output_file, c='copy')
        .overwrite_output()
        .run()
    )

    print(f"✅ Final video compiled at: {output_file}")