import streamlit as st
from gtts import gTTS
from moviepy.editor import *
import os
import tempfile

st.set_page_config(page_title="🎙️ Fact Pulse AI", layout="centered")

st.title("🎙️ Fact Pulse AI - Video Generator")

script = st.text_area("Enter your script here:", value="", height=300)

aspect_ratio = st.selectbox("Choose video aspect ratio", ["16:9", "9:16"])

edit_note = st.text_area("Want to fix or change something later? Type it here (optional):")

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

        text_clips = []
        current_time = 0

        for word in words:
            txt_clip = TextClip(
                word,
                fontsize=70,
                color='white',
                font='Arial-Bold',
                size=(720, 1280 if aspect_ratio == "9:16" else 720),
                method='label'  # 👈 this avoids ImageMagick errors
            ).set_position("center").set_duration(word_duration).set_start(current_time)
            txt_clip = txt_clip.margin(bottom=30)
            text_clips.append(txt_clip)
            current_time += word_duration

    with st.spinner("Composing final video..."):
        final = CompositeVideoClip(text_clips, size=(720, 1280 if aspect_ratio == "9:16" else 720))
        final = final.set_audio(audio_clip)
        output_path = os.path.join(tempfile.gettempdir(), "anm_factpulse_video.mp4")
        final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

    st.video(output_path)
    st.success("✅ Video Ready!")
    st.download_button("⬇️ Download Video", data=open(output_path, "rb"), file_name="anm_factpulse_video.mp4", mime="video/mp4")
