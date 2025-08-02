import streamlit as st
import os
import tempfile
from gtts import gTTS
from moviepy.editor import *
from PIL import Image
import random

# --- UI Layout ---
st.set_page_config(page_title="Fact Pulse AI", layout="centered")
st.title("🎬 Fact Pulse AI Video Generator")

with st.form("video_form"):
    script = st.text_area("📜 Enter your script (30s):", height=200)
    aspect = st.selectbox("📐 Choose Aspect Ratio", ["Vertical (9:16)", "Horizontal (16:9)"])
    preview = st.checkbox("👁 Preview before final video", value=True)
    fix_notes = st.text_area("✏️ Anything to fix or improve? (optional)", height=100)
    submitted = st.form_submit_button("🚀 Generate Video")

# --- Helper Functions ---
def generate_voice(script_text, filename):
    tts = gTTS(text=script_text, lang='en')
    tts.save(filename)

def generate_dummy_visuals(output_path, aspect_ratio):
    size = (720, 1280) if aspect_ratio == "Vertical (9:16)" else (1280, 720)
    color = tuple(random.randint(100, 255) for _ in range(3))
    img = Image.new('RGB', size, color=color)
    img.save(output_path)

def overlay_text_on_video(image_path, audio_path, script_text, output_path, aspect_ratio):
    image_clip = ImageClip(image_path).set_duration(30)
    audio_clip = AudioFileClip(audio_path)
    final_audio = audio_clip
    image_clip = image_clip.set_audio(final_audio)

    txt_clip = TextClip(script_text, fontsize=40, color='white', method='caption', size=image_clip.size, align='center')
    txt_clip = txt_clip.set_duration(30).set_position('center')

    final = CompositeVideoClip([image_clip, txt_clip])
    final.write_videofile(output_path, fps=24)

# --- Main Logic ---
if submitted and script:
    with st.spinner("Generating video..."):
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = os.path.join(tmpdir, "voice.mp3")
            image_path = os.path.join(tmpdir, "frame.jpg")
            video_path = os.path.join(tmpdir, "factpulse_video.mp4")

            generate_voice(script, audio_path)
            generate_dummy_visuals(image_path, aspect)
            overlay_text_on_video(image_path, audio_path, script, video_path, aspect)

            st.success("✅ Video Ready!")
            st.video(video_path)
            st.download_button("📥 Download Video", open(video_path, "rb"), file_name="factpulse_video.mp4")

    if preview:
        st.info("👁 Preview Mode Enabled — Let us know what to change below.")

    if fix_notes:
        st.text_area("Your feedback:", value=fix_notes, disabled=True)
