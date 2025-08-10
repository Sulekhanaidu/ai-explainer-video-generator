# AI Explainer Video Generator

## Overview
This project automates the creation of engaging explainer videos using AI.  
It generates:
- **Slide scripts** with narration text
- **AI-generated images** (DALL·E or Stability AI)
- **TTS audio** for narration
- **Animated video slides** (optional)
- **Final compiled video** with synchronized audio and visuals
- **Subtitles** for accessibility

The tool is built using **Python** and **Streamlit** for the UI, integrating multiple AI APIs.

---

## Features
1. **Topic-based Content Generation**
   - Automatically generates scripts for each slide.
   - Supports JSON-formatted output for structured video creation.

2. **Image & Animation Creation**
   - Uses DALL·E or Stability AI for high-quality, themed visuals.
   - Can use still images or animated videos per slide.

3. **Text-to-Speech Narration**
   - Converts slide text into natural-sounding audio.
   - Supports multiple voices and accents.

4. **Video Compilation**
   - Combines slides, animations, and audio according to narration length.
   - Ensures no blank screens—slides match audio duration exactly.

5. **Caching**
   - Option to reuse previously generated assets for the same topic.
   - Saves time and API costs.

6. **User Authentication**
   - Secure login using Streamlit Authenticator.
   - YAML-based credentials with optional cookie-based session persistence.

7. **Downloadable Output**
   - Final video and assets can be downloaded as a ZIP package.

---

## Requirements
- Python 3.9+
- Required Python packages:
  ```
  streamlit
  openai
  requests
  ffmpeg-python
  coqui-tts
  streamlit-authenticator==0.4.2
  pyyaml
  moviepy
  numpy
  scipy
  ```
- FFmpeg installed and accessible from the system PATH.

---

## Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/ai-explainer-video-generator.git
   cd ai-explainer-video-generator
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set API Keys**
   - Create a `.env` file or update `config.yaml` with:
     ```
     OPENAI_API_KEY=your_openai_api_key
     STABILITY_API_KEY=your_stability_api_key
     ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

---

## Usage
1. Log in using your credentials.
2. Enter a **topic** and select:
   - Number of slides
   - Image/animation style
   - Caching option (on/off)
3. Click **Generate** to:
   - Create scripts, images/animations, and audio
   - Compile the final video
4. Download the **video or ZIP** from the output section.

---

## File Structure
```
output/
    <topic>/
        slides/             # Generated images or animations
        audio/              # Narration audio files
        subtitles/          # Subtitle files (.srt)
        final_video.mp4     # Compiled video
        output.zip          # Downloadable package
```

---

## Notes
- Keep prompts descriptive for better image quality.
- API usage may incur costs based on the number of slides/images/audio files generated.
- To avoid large file issues on GitHub, exclude `output/` and environment folders from commits (`.gitignore`).

---

## License
This project is for educational and research purposes.  
You may modify and use it as per your requirements, but ensure compliance with API providers' terms of service.
