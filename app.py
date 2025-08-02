
import streamlit as st
from gtts import gTTS
from moviepy.editor import *
import os
import tempfile

st.set_page_config(page_title="Fact Pulse AI", layout="centered")
st.title("🎥 Fact Pulse AI - Auto Video Generator")

script = st.text_area("Enter your video script:", height=200)

aspect_ratio = st.selectbox("Choose Aspect Ratio", ["16:9", "9:16", "1:1"])

if st.button("Generate Video"):
    if script.strip() == "":
        st.warning("Please enter a script first.")
    else:
        st.info("Generating voiceover...")
        tts = gTTS(text=script, lang='en')
        temp_dir = tempfile.mkdtemp()
        audio_path = os.path.join(temp_dir, "voice.mp3")
        tts.save(audio_path)

        st.info("Generating video with captions and background music...")
        txt_clip = TextClip(script, fontsize=24, color='white', size=(720, 1280 if aspect_ratio == "9:16" else 720), method='caption')
        txt_clip = txt_clip.set_duration(30).set_position('center').set_fps(24)

        audioclip = AudioFileClip(audio_path).set_duration(30)
        final = txt_clip.set_audio(audioclip)

        output_path = os.path.join(temp_dir, "output_video.mp4")
        final.write_videofile(output_path, codec='libx264', audio_codec='aac')

        st.success("Video generated successfully!")
        with open(output_path, "rb") as file:
            st.download_button(label="📥 Download Video", data=file, file_name="fact_pulse_video.mp4", mime="video/mp4")
