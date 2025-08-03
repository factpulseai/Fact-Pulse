import streamlit as st
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import os
import tempfile

st.set_page_config(page_title="🎙️ Fact Pulse AI", layout="centered")

st.title("🎙️ Fact Pulse AI - Video Generator")

script = st.text_area("Enter your script here:", value="", height=300)

aspect_ratio = st.selectbox("Choose video aspect ratio", ["16:9", "9:16"])

edit_note = st.text_area("Want to fix or change something later? Type it here (optional):")

def generate_text_image(text, size):
    width, height = size
    img = Image.new('RGB', (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 70)
    except:
        font = ImageFont.load_default()
    text_width, text_height = draw.textsize(text, font=font)
    draw.text(
        ((width - text_width) / 2, (height - text_height) / 2),
        text,
        font=font,
        fill=(255, 255, 255)
    )
    temp_img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
    img.save(temp_img_path)
    return temp_img_path

if st.button("🎬 Generate Video"):
    with st.spinner("Generating voice..."):
        tts = gTTS(script)
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio.name)

    with st.spinner("Generating captions..."):
        audio_clip = AudioFileClip(temp_audio.name)
        duration = audio_clip.duration

        words = script.split()
        word_duration = duration / len(words)

        clips = []
        current_time = 0

        size = (720, 1280 if aspect_ratio == "9:16" else 720)

        for word in words:
            img_path = generate_text_image(word, size)
            img_clip = ImageClip(img_path).set_duration(word_duration).set_start(current_time)
            clips.append(img_clip)
            current_time += word_duration

    with st.spinner("Composing final video..."):
        final = CompositeVideoClip(clips, size=size).set_audio(audio_clip)
        output_path = os.path.join(tempfile.gettempdir(), "anm_factpulse_video.mp4")
        final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

    st.video(output_path)
    st.success("✅ Video Ready!")
    st.download_button("⬇️ Download Video", data=open(output_path, "rb"), file_name="anm_factpulse_video.mp4", mime="video/mp4")
