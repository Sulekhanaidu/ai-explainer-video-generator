import os
import openai
import requests
from export_animated_video import export_animated_video

# 🔁 Create animated video from static image
output_path = "output/Earth/slides/slide_01.png"
animated_output = output_path.replace(".png", "_animated.mp4")
export_animated_video(output_path, animated_output)