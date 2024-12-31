import streamlit as st
import yt_dlp
import os
import imageio_ffmpeg as ffmpeg  # Untuk muat turun automatik


# Set page title and icon
st.set_page_config(
    page_title="YouTube MP3 Downloader",  # Ganti dengan nama aplikasi anda
    page_icon="🎥",  # Ganti dengan emoji atau ikon unicode lain
)

def download_with_ytdlp(url):
    try:
        ffmpeg_path = ffmpeg.get_ffmpeg_exe()  # Muat turun FFmpeg jika tidak ada
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'ffmpeg_location': ffmpeg_path,  # Gunakan FFmpeg yang dimuat turun
        }
        st.write("Downloading ...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp3"
            st.success("Download complete!")
            return filename
    except Exception as e:
        st.error(f"yt-dlp failed: {e}")
        return None
    
# Disclaimer content
def display_disclaimer():
    st.markdown("---")  # Horizontal line
    st.markdown(
        """
        
        **Disclaimer**  
        This application is provided as is for educational and informational purposes only.  
        The author, Risz-Sgr, is not responsible for any misuse of this tool.  
        Please ensure compliance with YouTube's terms of service and copyright laws when using this application.  
        ver:0.1
        """
    )


def main():
    st.title("YouTube Audio Downloader (MP3)")
    url = st.text_input("Enter the YouTube video URL:")
    if st.button("Download"):
        if url:
            filename = download_with_ytdlp(url)
            if filename:
                with open(filename, "rb") as file:
                    st.download_button(
                        label="Click here to download the MP3 file",
                        data=file,
                        file_name=os.path.basename(filename),
                        mime="audio/mp3"
                    )

if __name__ == "__main__":
    main()
    display_disclaimer()
