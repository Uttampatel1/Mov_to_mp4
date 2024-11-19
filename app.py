import streamlit as st
import ffmpeg
import os
from pathlib import Path

def convert_mov_to_mp4(input_path, output_path):
    """
    Converts a MOV video file to MP4 format.
    
    :param input_path: Path to the input MOV file.
    :param output_path: Path to the output MP4 file.
    """
    try:
        ffmpeg.input(input_path).output(output_path, vcodec='libx264', acodec='aac').run(overwrite_output=True)
        return True
    except ffmpeg.Error as e:
        st.error("Error during conversion!")
        st.error(e.stderr.decode())
        return False

# Streamlit App
def main():
    # Page configuration
    st.set_page_config(page_title="MOV to MP4 Converter", page_icon="🎥", layout="centered")
    
    # Title and description
    st.title("🎥 MOV to MP4 Converter")
    st.write("Upload your MOV file, and this app will convert it to MP4 format.")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a MOV file", type=["mov"], accept_multiple_files=False)
    
    if uploaded_file:
        st.info("Processing your file...")
        
        # Save the uploaded file temporarily
        input_path = Path("temp_input.mov")
        output_path = Path("output_video.mp4")
        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())
        
        # Conversion
        if convert_mov_to_mp4(input_path, output_path):
            st.success("🎉 Conversion successful!")
            
            # Provide a download link for the MP4 file
            with open(output_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download MP4 File",
                    data=f,
                    file_name="converted_video.mp4",
                    mime="video/mp4"
                )
        
        # Cleanup temporary files
        if input_path.exists():
            os.remove(input_path)
        if output_path.exists():
            os.remove(output_path)

    # Footer
    st.markdown(
        """
        ---
        **Note**: This app processes videos locally and does not store your files.
        """,
        unsafe_allow_html=True
    )

# Run the app
if __name__ == "__main__":
    main()
