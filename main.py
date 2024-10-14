import streamlit as st
from pytubefix import YouTube
from pytubefix.cli import on_progress

st.set_page_config(
    page_title="YT Download",
    page_icon="⬇️",
    layout="wide",
    initial_sidebar_state="collapsed",
)
# Title of the app
st.title("YouTube Video Downloader")

#