import streamlit as st
from moviepy import VideoFileClip, concatenate_videoclips
import tempfile
import os

# App UI setup
st.set_page_config(page_title="🎞️ Video Merger", layout="centered")
st.title("🎬 Multi-Format Video Merger")

st.markdown("""
Upload **2 to 5 videos** (`.mp4`, `.mkv`, `.avi`, `.mov`, etc.)  
This tool will merge them into a single `.mp4` file.

🕐 **Note:** Merging may take time depending on file size.
""")

# Select number of videos to merge
num_videos = st.selectbox("🔢 How many videos do you want to merge?", [2, 3, 4, 5])

# Supported video formats
video_formats = ["mp4", "mkv", "avi", "mov", "flv", "webm"]

# File upload section in 2-column layout
uploaded_files = []
for i in range(0, num_videos, 2):
    cols = st.columns(2)
    for j in range(2):
        idx = i + j
        if idx < num_videos:
            with cols[j]:
                file = st.file_uploader(f"📁 Upload Video {idx + 1}", type=video_formats, key=f"vid_{idx}")
                if file:
                    uploaded_files.append(file)

# Start merging if all files are uploaded
if len(uploaded_files) == num_videos:
    if st.button("🚀 Merge Videos"):
        with st.spinner("🔄 Merging videos... It take some time... Be patient!"):
            try:
                temp_paths = []

                # Save each uploaded file temporarily
                for file in uploaded_files:
                    ext = os.path.splitext(file.name)[1]
                    temp_file_path = os.path.join(tempfile.gettempdir(), f"{file.name}")
                    with open(temp_file_path, "wb") as f:
                        f.write(file.read())
                    temp_paths.append(temp_file_path)

                # Load all video clips
                clips = [VideoFileClip(path) for path in temp_paths]

                # Merge clips
                final_clip = concatenate_videoclips(clips, method="compose")

                # Output path
                output_path = os.path.join(tempfile.gettempdir(), "merged_video.mp4")
                final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

                # Show download button
                st.success("🎉 Merging completed successfully!")
                with open(output_path, "rb") as merged:
                    st.download_button("📥 Download Merged Video", merged, file_name="merged_video.mp4", mime="video/mp4")

            except Exception as e:
                st.error(f"❌ Error during merging: {e}")
else:
    st.info(f"📂 Please upload all {num_videos} videos to enable merging.")
