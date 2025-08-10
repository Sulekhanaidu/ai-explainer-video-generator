import requests
import json
import re
import os

def generate_script(topic, num_slides=10, use_cache=True):
    print("📝 Generating script for topic:", topic)

    # ✅ Setup cache directory
    cache_dir = "cache"
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"{topic.lower().strip().replace(' ', '_')}_with_images.json")

    # ✅ If cached, return saved slides
    if use_cache and os.path.exists(cache_file):
        print("🔁 Using cached script with images...")
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    # 🎯 Prompt for Youngsters: narration + image
    prompt = f"""
Create an engaging explainer video script for school students aged 11 to 18 on the topic: "{topic}".

Return a JSON array of {num_slides} slides. Each slide should include:
- "slide": slide number
- "text": a clear and engaging narration (~80–100 words)
- "image_prompt": "Vibrant futuristic classroom with teens interacting with holographic screens, neon colors, sci-fi style, cinematic lighting, ultra-detailed, anime-inspired, cyberpunk aesthetic, high contrast shadows and glow, stylish teen fashion, modern gadgets like AR glasses and smartwatches, dynamic camera angle, glowing user interfaces, soft ambient neon reflections on surfaces, energetic and immersive atmosphere"

Output only valid JSON, like:
[
  {{
    "slide": 1,
    "text": "What if your phone could think? Artificial Intelligence (AI) helps computers learn from data. It’s like teaching a robot to think and make decisions.",
    "image_prompt": "A robot looking at a chalkboard with math formulas, next to a student doing the same"
  }},
  ...
]
"""

    # 🔐 DeepSeek API Key from Environment
    api_key = "Your key"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers=headers,
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
    )

    if response.status_code != 200:
        print("❌ DeepSeek API error details:")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        raise RuntimeError(f"❌ DeepSeek API error: {response.text}")

    output = response.json()["choices"][0]["message"]["content"]
    print("📄 Raw output received from DeepSeek.")

    # 🎯 Try parsing JSON from response
    try:
        json_match = re.search(r'\[\s*{.*?}\s*\]', output, re.DOTALL)
        if json_match:
            slides = json.loads(json_match.group(0))
        else:
            raise ValueError("No JSON detected in output.")
    except Exception as e:
        print("⚠️ JSON parsing failed:", e)
        print("🔁 Falling back to line-by-line parsing.")
        lines = [line.strip() for line in output.split("\n") if line.strip()]
        slides = [{"slide": i + 1, "text": line, "image_prompt": ""} for i, line in enumerate(lines)]

    slides = [s for s in slides if len(s.get("text", "").split()) >= 10]

    if not slides:
        raise ValueError("❌ No valid slides generated from model output.")

    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(slides, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(slides)} slides (with image prompts) generated and cached.")
    return slides
