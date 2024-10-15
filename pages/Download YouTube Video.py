import streamlit as st
from pytubefix import YouTube
from pytubefix.cli import on_progress

st.set_page_config(
    page_title="YT Download",
    page_icon="⬇️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

visitor_data = "apurba"  # Replace with your actual visitor data
po_token = "1234"        # Replace with your actual po_token

# Title of the app
st.html('<h1 style="text-align:center;color:#ff0000;">Youtube ▶ Video Downloader</h1>')

# Input: YouTube video URL
video_url = st.text_input("Enter the YouTube video URL:", placeholder='https://www.youtube.com/watch?v=bn0Kh9c4Zv4&ab_channel=MrBeast')
allres = []

if video_url:
    try:
        # Fetch YouTube video object
        yt = YouTube(video_url, on_progress_callback=on_progress, use_po_token= True, po_token_verifier=('apurba','1234'))
        col1,col2= st.columns(2)
        with col1:
            st.image(yt.thumbnail_url)
            st.html(f'<div class="centered-text"><h3>{yt.title}</h3></div>')
        with col2:
            col3, col4 = st.columns(2)
            with col3:
                st.html(f'<div class="centered-text" style="color:green;"><h5>Views : {yt.views}</h5></div>')
                st.html(f'<div class="centered-text" style="color:green;"><h6>Channel Name : {yt.author}</h6></div>')
            with col4:
                st.html(f'<div class="centered-text"><h5>Length : {yt.length} seconds</h5></div>')
            st.html(f'<div class="centered-text"><h6>Channel URL : {yt.channel_url}</h6></div>')

            # Fetch video streams with highest resolution
            for i in yt.streams.filter(type="video", mime_type="video/mp4", progressive=True):
                allres.append(i)

            # Let the user select the resolution they want to download
            res_options = [f"{stream.resolution} - {stream.filesize / (1024 * 1024):.2f} MB" for stream in allres]
            selected_res = st.selectbox("Select resolution to download:", res_options)

            # Find the selected stream based on the resolution
            selected_stream = allres[res_options.index(selected_res)]

            # When the download button is clicked, show spinner and download the video
            if st.button("Get Video"):
                with st.spinner("Preparing video..."):
                    # Download the video file
                    video_file = selected_stream.download()

                    # Allow user to download the file through Streamlit
                    with open(video_file, "rb") as file:
                        st.download_button(
                            label="Click to Download",
                            data=file,
                            file_name=yt.title + ".mp4",
                            mime="video/mp4"
                        )
                    st.toast("Video downloaded successfully!")

    except Exception as e:
        st.error(f"Error: {str(e)}")
