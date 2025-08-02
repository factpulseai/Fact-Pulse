import streamlit as st

st.set_page_config(page_title="Fact Pulse AI", layout="centered")

st.title("📊 Fact Pulse AI - Video Generator")
st.markdown("Generate AI Shorts or Ads with AI voice, captions & visuals!")

script = st.text_area("✍️ Paste your script here:", height=200)

if st.button("🎬 Generate Video"):
    if script.strip():
        st.success("✅ Your video has been generated! (This is a placeholder)")
        st.info("Full video generation feature will be added soon.")
    else:
        st.warning("Please paste your script first.")
