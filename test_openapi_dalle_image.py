import openai
import os

# Set your API key (or use environment variable)
api_key  = "Your key"  # Replace with your key

client = openai.OpenAI(api_key=api_key)

def test_dalle_api():
    try:
        response = client.images.generate(
            model="dall-e-2",  # or "dall-e-3" if enabled
            prompt="A cat reading a book in a library",
            n=1,
            size="256x256"
        )
        image_url = response.data[0].url
        print("✅ DALL·E API is working.")
        print("🖼️ Image URL:", image_url)
        return True

    except openai.OpenAIError as e:
        print(f"❌ OpenAI error: {e}")
        return False

# Run the test
test_dalle_api()