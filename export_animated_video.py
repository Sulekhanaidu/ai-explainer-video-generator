
from moviepy.editor import ImageClip
import os

def export_animated_video(image_path, output_path, duration=5, zoom_factor=0.1):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    print(f"🎞️ Animating image: {image_path}")

    # Create base image clip
    base_clip = ImageClip(image_path).resize(height=720).set_duration(duration)

    # Apply smooth zoom-in animation
    def zoom_in(get_frame, t):
        zoom = 1 + zoom_factor * t
        frame = get_frame(t)
        h, w = frame.shape[:2]
        new_w, new_h = int(w / zoom), int(h / zoom)
        x1 = (w - new_w) // 2
        y1 = (h - new_h) // 2
        return frame[y1:y1+new_h, x1:x1+new_w]

    animated_clip = base_clip.fl_time(lambda t: t).fl(zoom_in, apply_to=["mask"])
    animated_clip = animated_clip.resize((1280, 720))  # Restore to frame size

    # Write output video
    animated_clip.write_videofile(output_path, fps=24)
    print(f"✅ Exported animated video: {output_path}")
