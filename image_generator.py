from PIL import Image, ImageDraw, ImageFont 
import os
import textwrap
from dalle_image_generator import generate_dalle_image

def generate_images(topic,slides, use_ai_images=True):
    print("🖼 Generating images...")

    os.makedirs(f"output/{topic}/slides", exist_ok=True)

    for slide in slides:
        slide_num = f"{slide['slide']:02d}"
        image_path = f"output/{topic}/slides/slide_{slide_num}.png"
        image_prompt = slide.get("image_prompt", "").strip()

        if use_ai_images and image_prompt:
            try:
                print(f"🎨 Generating AI image for slide {slide_num}...")
                print(f"🎨 Prompt: {image_prompt}")
                success = generate_dalle_image(image_prompt, image_path)
                if success:
                    print(f"✅ AI image saved: {image_path}")
                    continue  # Skip text fallback if successful
                else:
                    print(f"⚠️ AI image generation failed for slide {slide_num}. Using text fallback.")
                    use_ai_images = False  # Disable further AI attempts
            except Exception as e:
                print(f"❌ Exception in AI image generation for slide {slide_num}: {e}")
                use_ai_images = False

        # 🔁 Fallback to text-based image
        img = Image.new('RGB', (1280, 720), color='white')
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()

        max_width = 60
        lines = textwrap.wrap(slide["text"], width=max_width)
        y_text = 200

        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]
            x = (1280 - line_width) // 2
            draw.text((x, y_text), line, font=font, fill='black')
            y_text += line_height + 10

        img.save(image_path)
        print(f"✅ Fallback image saved: {image_path}")