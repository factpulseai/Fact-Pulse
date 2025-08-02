import streamlit as st
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import tempfile
import os
import uuid

st.set_page_config(layout="centered", page_title="Fact Pulse AI Video Generator")

st.title("🎬 Fact Pulse AI Video Generator")
st.write("Generate an AI video with voiceover, captions, and visuals — fully automated.")

# User Inputs
script = st.text_area("✍️ Enter your video script:", "Did you know the Eiffel Tower can grow taller in summer?")
prompt = st.text_input("🖼️ Describe the scene:", "Cinematic view of the Eiffel Tower at sunset with clouds")
aspect_ratio = st.selectbox("📱 Select Aspect Ratio", ["16:9", "9:16"])

if st.button("🎥 Generate Video"):
    with st.spinner("Generating voiceover..."):
        tts = gTTS(script)
        audio_path = f"/tmp/voice_{uuid.uuid4().hex}.mp3"
        tts.save(audio_path)
        audio_clip = AudioFileClip(audio_path)
        tts_duration = audio_clip.duration

    with st.spinner("Creating caption..."):
        def generate_text_image(text, width=720, height=100, font_size=30):
            img = Image.new("RGB", (width, height), color=(0, 0, 0))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
            draw.text((10, 10), text, fill="white", font=font)
            temp_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
            img.save(temp_path)
            return temp_path

        caption_path = generate_text_image(script)
        txt_clip = ImageClip(caption_path).set_duration(tts_duration).set_position("bottom")

    with st.spinner("Generating AI background..."):
        # Placeholder background — replace with real AI visuals when added
        bg_color = (10, 10, 40)
        bg_size = (1280, 720) if aspect_ratio == "16:9" else (720, 1280)
        bg = Image.new("RGB", bg_size, color=bg_color)
        temp_bg = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
        bg.save(temp_bg)
        background_clip = ImageClip(temp_bg).set_duration(tts_duration)

    with st.spinner("Adding background music..."):
        music_path = "music.mp3"
        if os.path.exists(music_path):
            music = AudioFileClip(music_path).volumex(0.2)
            final_audio = audio_clip.audio.set_duration(tts_duration).audio.set_fps(44100).volumex(1.0)
            combined_audio = music.set_duration(tts_duration).audio.set_fps(44100).volumex(0.2)
            final_audio = audio_clip.audio.volumex(1.0).fx(lambda c: c.audio_fadeout(0.5))
        else:
            final_audio = audio_clip

    with st.spinner("Rendering final video..."):
        video = CompositeVideoClip([background_clip, txt_clip])
        video = video.set_audio(final_audio)
        video_path = f"/tmp/final_video_{uuid.uuid4().hex}.mp4"
        video.write_videofile(video_path, fps=24)

    st.video(video_path)
    st.success("✅ Your video is ready!")
