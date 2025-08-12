# dalle_image_generator.py
import os
import time
import openai
import requests
from export_animated_video import export_animated_video

api_key = "yourkey"  # Set securely in your env
client = openai.OpenAI(api_key=api_key)

def download_with_retry(url, output_path, retries=3, delay=2, timeout=60):
    """Download file in chunks with retry logic."""
    for attempt in range(retries):
        try:
            with requests.get(url, timeout=timeout, stream=True) as r:
                r.raise_for_status()
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            return True
        except Exception as e:
            print(f"⚠️ Download attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return False

def generate_dalle_image(prompt_text, output_path):
    if not api_key or not api_key.startswith("sk-"):
        print("❌ Missing or invalid OpenAI API key.")
        return False

    # Shorten prompt if needed
    #short_prompt = prompt_text.strip().split('.')[0]
    #if len(short_prompt.split()) > 25:
    #    short_prompt = " ".join(short_prompt.split()[:25]) + "..."

     # ✅ Keep the full prompt, add face clarity instructions
    enhanced_prompt = (
        prompt_text.strip()
        + ", anime-meets-realism style, clean and proportional faces, expressive eyes, "
          "slightly stylized features, vivid colors, cinematic lighting, sharp focus, "
          "no distortions, dynamic composition"
    )
    
    try:
        # Generate image
        response = client.images.generate(
            model="dall-e-2",  # or "dall-e-3" if access granted
            prompt=enhanced_prompt,
            n=1,
            size="1024x1024"
        )

        image_url = response.data[0].url
        print(f"📥 Downloading from: {image_url}")

        # Download with retries
        if not download_with_retry(image_url, output_path):
            print("❌ Failed to download image after retries.")
            return False

        print(f"✅ Saved DALL·E image to: {output_path}")

        # Create animated video from image
        #animated_output = output_path.replace(".png", "_animated.mp4")
        #export_animated_video(output_path, animated_output)
        return True

    except Exception as e:
        print(f"❌ DALL·E generation failed: {e}")
        return False