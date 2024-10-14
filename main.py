import streamlit as st
from pytubefix import YouTube
from pytubefix.cli import on_progress

# Title of the app
st.title("YouTube Video Downloader")

# Input: YouTube video URL
video_url = st.text_input("Enter the YouTube video URL:")
allres = []

if video_url:
    try:
        # Fetch YouTube video object
        yt = YouTube(video_url, on_progress_callback=on_progress)
        st.write(f"**Title:** {yt.title}")
        st.write(f"**Views:** {yt.views:,}")
        st.write(f"**Length:** {yt.length} seconds")
        st.write(yt.channel_url)

        # Fetch video streams with highest resolution
        for i in yt.streams.filter(type="video", mime_type="video/mp4", progressive=True):
            allres.append(i)

        # Let the user select the resolution they want to download
        res_options = [f"{stream.resolution} - {stream.filesize / (1024 * 1024):.2f} MB" for stream in allres]
        selected_res = st.selectbox("Select resolution to download:", res_options)

        # Find the selected stream based on the resolution
        selected_stream = allres[res_options.index(selected_res)]

        # When the download button is clicked, show spinner and download the video
        if st.button("Download"):
            with st.spinner("Downloading video..."):
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

    except Exception as e:
        st.error(f"Error: {str(e)}")
