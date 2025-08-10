import shutil
import os
# Main pipeline that runs all modules sequentially
def run_pipeline(topic,add_subtitles=True, use_ai_images=True, num_slides=10, use_cache=False):
    print(f"add_subtitles - {add_subtitles}, use_ai_images - {use_ai_images}, slides - {num_slides}, use_cache - {use_cache}")

    # Clean up old output (Commenting this out for cache)
    #output_dir = "output"
    #if os.path.exists(output_dir):
        #shutil.rmtree(output_dir)  # delete old output folder

    # Create fresh subdirectories 
   # os.makedirs("output/slides", exist_ok=True)
    #os.makedirs("output/audio", exist_ok=True)
    #os.makedirs("output/temp", exist_ok=True)
    
    # Import modules
    from script_generator import generate_script
    from tts_generator import generate_tts
    from image_generator import generate_images
    from video_compiler import compile_video

     # Determine expected video path
    video_filename = "final_video_with_subs.mp4" if add_subtitles else "final_video.mp4"
    final_video_path = f"output/{topic}/{video_filename}"

     # ✅ Check cache
    if use_cache and os.path.exists(final_video_path):
        print(f"📦 Cached video found: {final_video_path}")
        print("✅ Skipping generation steps.")
        return

    print('Generating script...')
    slides = generate_script(topic, num_slides=num_slides, use_cache=use_cache)
    print('Generating audio...')
    generate_tts(topic,slides)
    print('Generating images...')
    generate_images(topic,slides, use_ai_images=use_ai_images)
    print('Compiling video...')
    compile_video(topic)
    
    if add_subtitles:
        from whisper_subtitle_generator import generate_subtitles
        from merge_srt_slides import merge_srt_slides
        from burn_subtitles import burn_subtitles

        print('Generating subtitles...')
        generate_subtitles(topic)
        print('Merging subtitles...')
        merge_srt_slides(topic)
        print('Burning subtitles...')
        burn_subtitles(topic)
    
    print('Done!')
