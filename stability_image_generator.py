# stability_image_generator.py
import os
import requests
import base64
import json

API_KEY = "sk-VHxzg5PVaDjXZhdy4ZGxOjp6cXucH4RUFaYpQC3Y9CJJdaVn"  # Replace or use os.getenv("STABILITY_API_KEY")

def generate_stable_image(prompt_text, output_path):
    if not API_KEY or "sk-" not in API_KEY:
        print("❌ Missing or invalid Stability AI API key.")
        return False

    url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
    

    # Shorten prompt for clarity and avoid overloading
    short_prompt = prompt_text.strip().split('.')[0]
    if len(short_prompt.split()) > 25:
        short_prompt = " ".join(short_prompt.split()[:25]) + "..."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {
        "text_prompts": [{"text": short_prompt}],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            if "artifacts" in result and result["artifacts"]:
                image_data = result["artifacts"][0]["base64"]
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(image_data))
                print(f"✅ Saved AI image to: {output_path}")
                return True
            else:
                print("❌ No image data found in response.")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")

            # ✅ Detect credit/usage errors and write flag
            if response.status_code == 429 or "insufficient_balance" in response.text:
                with open("stability_credit_error.flag", "w") as flag:
                    flag.write("true")
    except Exception as e:
        print(f"❌ Exception during image generation: {e}")

    return False